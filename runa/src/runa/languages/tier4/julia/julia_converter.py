#!/usr/bin/env python3
"""
Julia ↔ Runa Converter

Bidirectional converter between Julia and Runa AST nodes, supporting all Julia
language features including multiple dispatch, metaprogramming, and scientific computing.
"""

from typing import List, Optional, Any, Union, Dict
from .julia_ast import *
from ....core.runa_ast import *


class JuliaToRunaConverter:
    """Converts Julia AST nodes to Runa AST nodes."""
    
    def __init__(self):
        self.type_mapping = {
            'Int': 'integer',
            'Float64': 'float',
            'String': 'string',
            'Bool': 'boolean',
            'Nothing': 'null',
            'Array': 'List',
            'Dict': 'Dictionary',
            'Vector': 'List',
            'Matrix': 'Array2D'
        }
    
    def convert_program(self, julia_program: JuliaProgram) -> Program:
        """Convert Julia program to Runa program."""
        files = [self.convert_file(file) for file in julia_program.files]
        return Program(files=files)
    
    def convert_file(self, julia_file: JuliaFile) -> FileNode:
        """Convert Julia file to Runa file."""
        imports = []
        declarations = []
        
        # Convert imports
        for imp in julia_file.imports:
            if isinstance(imp, JuliaImportDeclaration):
                imports.append(ImportDeclaration(
                    module_name=imp.package,
                    imported_names=imp.symbols if imp.symbols else ["*"],
                    alias=imp.alias
                ))
            elif isinstance(imp, JuliaUsingDeclaration):
                imports.append(ImportDeclaration(
                    module_name=imp.package,
                    imported_names=imp.symbols if imp.symbols else ["*"]
                ))
        
        # Convert exports (as comments for now since Runa doesn't have direct exports)
        for export in julia_file.exports:
            comment = f"# Export: {', '.join(export.symbols)}"
            declarations.append(CommentNode(content=comment))
        
        # Convert module or file declarations
        if julia_file.module_declaration:
            module_decl = self.convert_module(julia_file.module_declaration)
            declarations.append(module_decl)
        else:
            # Convert top-level declarations
            for decl in julia_file.declarations:
                runa_decl = self.convert_declaration(decl)
                if runa_decl:
                    declarations.append(runa_decl)
        
        return FileNode(imports=imports, declarations=declarations)
    
    def convert_module(self, julia_module: JuliaModuleDeclaration) -> ClassDeclaration:
        """Convert Julia module to Runa class (namespace-like)."""
        body_declarations = []
        
        for item in julia_module.body:
            decl = self.convert_declaration(item)
            if decl:
                body_declarations.append(decl)
        
        return ClassDeclaration(
            name=julia_module.name,
            body=body_declarations,
            is_static=True  # Modules are like static classes
        )
    
    def convert_declaration(self, julia_decl: JuliaNode) -> Optional[ASTNode]:
        """Convert Julia declaration to Runa declaration."""
        if isinstance(julia_decl, JuliaFunctionDeclaration):
            return self.convert_function(julia_decl)
        elif isinstance(julia_decl, JuliaStructDeclaration):
            return self.convert_struct(julia_decl)
        elif isinstance(julia_decl, JuliaConstDeclaration):
            return self.convert_const(julia_decl)
        elif isinstance(julia_decl, JuliaTypeAlias):
            return self.convert_type_alias(julia_decl)
        elif isinstance(julia_decl, JuliaAbstractTypeDeclaration):
            return self.convert_abstract_type(julia_decl)
        elif isinstance(julia_decl, JuliaMacroDeclaration):
            return self.convert_macro(julia_decl)
        elif isinstance(julia_decl, JuliaExpression):
            return self.convert_expression(julia_decl)
        
        return None
    
    def convert_function(self, julia_func: JuliaFunctionDeclaration) -> FunctionDeclaration:
        """Convert Julia function to Runa function."""
        parameters = []
        
        if julia_func.signature:
            for param in julia_func.signature.parameters:
                param_type = None
                if param.type:
                    param_type = self.convert_type(param.type)
                
                runa_param = ParameterDeclaration(
                    name=param.name,
                    type=param_type,
                    default_value=self.convert_expression(param.default_value) if param.default_value else None
                )
                parameters.append(runa_param)
        
        # Convert function body
        body_statements = []
        for stmt in julia_func.body:
            runa_stmt = self.convert_statement(stmt)
            if runa_stmt:
                body_statements.append(runa_stmt)
        
        return_type = None
        if julia_func.return_type:
            return_type = self.convert_type(julia_func.return_type)
        
        return FunctionDeclaration(
            name=julia_func.name,
            parameters=parameters,
            return_type=return_type,
            body=body_statements
        )
    
    def convert_struct(self, julia_struct: JuliaStructDeclaration) -> ClassDeclaration:
        """Convert Julia struct to Runa class."""
        fields = []
        
        for field in julia_struct.fields:
            field_type = None
            if field.type:
                field_type = self.convert_type(field.type)
            
            runa_field = VariableDeclaration(
                name=field.name,
                type=field_type,
                initial_value=self.convert_expression(field.default_value) if field.default_value else None,
                is_mutable=julia_struct.is_mutable
            )
            fields.append(runa_field)
        
        return ClassDeclaration(
            name=julia_struct.name,
            body=fields,
            is_mutable=julia_struct.is_mutable
        )
    
    def convert_const(self, julia_const: JuliaConstDeclaration) -> VariableDeclaration:
        """Convert Julia const to Runa constant."""
        return VariableDeclaration(
            name=julia_const.name,
            type=self.convert_type(julia_const.type) if julia_const.type else None,
            initial_value=self.convert_expression(julia_const.value) if julia_const.value else None,
            is_constant=True
        )
    
    def convert_type_alias(self, julia_alias: JuliaTypeAlias) -> TypeAliasDeclaration:
        """Convert Julia type alias to Runa type alias."""
        return TypeAliasDeclaration(
            name=julia_alias.name,
            target_type=self.convert_type(julia_alias.target_type) if julia_alias.target_type else None
        )
    
    def convert_abstract_type(self, julia_abstract: JuliaAbstractTypeDeclaration) -> InterfaceDeclaration:
        """Convert Julia abstract type to Runa interface."""
        return InterfaceDeclaration(
            name=julia_abstract.name,
            methods=[],  # Abstract types don't have concrete methods
            extends=self.convert_type(julia_abstract.supertype) if julia_abstract.supertype else None
        )
    
    def convert_macro(self, julia_macro: JuliaMacroDeclaration) -> FunctionDeclaration:
        """Convert Julia macro to Runa function (with annotation)."""
        parameters = []
        for param in julia_macro.parameters:
            param_type = self.convert_type(param.type) if param.type else None
            runa_param = ParameterDeclaration(
                name=param.name,
                type=param_type
            )
            parameters.append(runa_param)
        
        body_statements = []
        for stmt in julia_macro.body:
            runa_stmt = self.convert_statement(stmt)
            if runa_stmt:
                body_statements.append(runa_stmt)
        
        # Add annotation to indicate this was a macro
        func_decl = FunctionDeclaration(
            name=julia_macro.name,
            parameters=parameters,
            body=body_statements
        )
        func_decl.annotations = [AnnotationNode(name="Macro")]
        return func_decl
    
    def convert_type(self, julia_type: JuliaType) -> Optional[TypeReference]:
        """Convert Julia type to Runa type."""
        if isinstance(julia_type, JuliaParametricType):
            base_name = self.type_mapping.get(julia_type.base_type, julia_type.base_type)
            
            if julia_type.parameters:
                type_args = [self.convert_type(param) for param in julia_type.parameters]
                return TypeReference(name=base_name, type_arguments=type_args)
            
            return TypeReference(name=base_name)
        
        elif isinstance(julia_type, JuliaUnionType):
            # Convert to Runa union type
            types = [self.convert_type(t) for t in julia_type.types]
            return UnionType(types=types)
        
        return TypeReference(name="Any")
    
    def convert_statement(self, julia_stmt: JuliaNode) -> Optional[ASTNode]:
        """Convert Julia statement to Runa statement."""
        if isinstance(julia_stmt, JuliaReturnStatement):
            return ReturnStatement(
                expression=self.convert_expression(julia_stmt.expression) if julia_stmt.expression else None
            )
        elif isinstance(julia_stmt, JuliaIfExpression):
            return self.convert_if(julia_stmt)
        elif isinstance(julia_stmt, JuliaForLoop):
            return self.convert_for(julia_stmt)
        elif isinstance(julia_stmt, JuliaWhileLoop):
            return self.convert_while(julia_stmt)
        elif isinstance(julia_stmt, JuliaBreakStatement):
            return BreakStatement()
        elif isinstance(julia_stmt, JuliaContinueStatement):
            return ContinueStatement()
        elif isinstance(julia_stmt, JuliaExpression):
            return ExpressionStatement(expression=self.convert_expression(julia_stmt))
        
        return None
    
    def convert_if(self, julia_if: JuliaIfExpression) -> IfStatement:
        """Convert Julia if expression to Runa if statement."""
        condition = self.convert_expression(julia_if.condition)
        
        then_statements = []
        for stmt in julia_if.then_body:
            runa_stmt = self.convert_statement(stmt)
            if runa_stmt:
                then_statements.append(runa_stmt)
        
        else_statements = []
        for stmt in julia_if.else_body:
            runa_stmt = self.convert_statement(stmt)
            if runa_stmt:
                else_statements.append(runa_stmt)
        
        return IfStatement(
            condition=condition,
            then_body=then_statements,
            else_body=else_statements if else_statements else None
        )
    
    def convert_for(self, julia_for: JuliaForLoop) -> ForStatement:
        """Convert Julia for loop to Runa for statement."""
        iterable = self.convert_expression(julia_for.iterable)
        
        body_statements = []
        for stmt in julia_for.body:
            runa_stmt = self.convert_statement(stmt)
            if runa_stmt:
                body_statements.append(runa_stmt)
        
        return ForStatement(
            variable=julia_for.variable,
            iterable=iterable,
            body=body_statements
        )
    
    def convert_while(self, julia_while: JuliaWhileLoop) -> WhileStatement:
        """Convert Julia while loop to Runa while statement."""
        condition = self.convert_expression(julia_while.condition)
        
        body_statements = []
        for stmt in julia_while.body:
            runa_stmt = self.convert_statement(stmt)
            if runa_stmt:
                body_statements.append(runa_stmt)
        
        return WhileStatement(
            condition=condition,
            body=body_statements
        )
    
    def convert_expression(self, julia_expr: Optional[JuliaExpression]) -> Optional[Expression]:
        """Convert Julia expression to Runa expression."""
        if julia_expr is None:
            return None
        
        if isinstance(julia_expr, JuliaIdentifier):
            return Identifier(name=julia_expr.name)
        
        elif isinstance(julia_expr, JuliaLiteralExpression):
            return LiteralExpression(
                value=julia_expr.value,
                literal_type=self.type_mapping.get(julia_expr.literal_type, julia_expr.literal_type)
            )
        
        elif isinstance(julia_expr, JuliaStringInterpolation):
            # Convert to string concatenation for now
            parts = []
            for part in julia_expr.parts:
                if isinstance(part, str):
                    parts.append(LiteralExpression(value=part, literal_type="string"))
                else:
                    parts.append(self.convert_expression(part))
            
            # Chain string additions
            if len(parts) == 1:
                return parts[0]
            
            result = parts[0]
            for part in parts[1:]:
                result = BinaryExpression(left=result, operator="+", right=part)
            return result
        
        elif isinstance(julia_expr, JuliaSymbolExpression):
            # Convert symbols to string literals with special annotation
            return LiteralExpression(value=f":{julia_expr.name}", literal_type="symbol")
        
        elif isinstance(julia_expr, JuliaArrayExpression):
            elements = [self.convert_expression(elem) for elem in julia_expr.elements]
            return ArrayLiteral(elements=elements)
        
        elif isinstance(julia_expr, JuliaTupleExpression):
            elements = [self.convert_expression(elem) for elem in julia_expr.elements]
            return TupleLiteral(elements=elements)
        
        elif isinstance(julia_expr, JuliaDictExpression):
            pairs = []
            for key_expr, value_expr in julia_expr.pairs:
                key = self.convert_expression(key_expr)
                value = self.convert_expression(value_expr)
                pairs.append((key, value))
            return DictionaryLiteral(pairs=pairs)
        
        elif isinstance(julia_expr, JuliaRangeExpression):
            # Convert range to function call: range(start, stop, step)
            args = []
            if julia_expr.start:
                args.append(self.convert_expression(julia_expr.start))
            if julia_expr.stop:
                args.append(self.convert_expression(julia_expr.stop))
            if julia_expr.step:
                # Insert step as second argument
                args.insert(1, self.convert_expression(julia_expr.step))
            
            return FunctionCall(
                function=Identifier(name="range"),
                arguments=args
            )
        
        elif isinstance(julia_expr, JuliaComprehension):
            # Convert to list comprehension
            element_expr = self.convert_expression(julia_expr.expression)
            
            # For now, convert first generator only
            if julia_expr.generators:
                gen = julia_expr.generators[0]
                iterable = self.convert_expression(gen.iterable)
                condition = self.convert_expression(gen.condition) if gen.condition else None
                
                return ListComprehension(
                    element=element_expr,
                    variable=gen.variable,
                    iterable=iterable,
                    condition=condition
                )
            
            return element_expr
        
        elif isinstance(julia_expr, JuliaBinaryExpression):
            left = self.convert_expression(julia_expr.left)
            right = self.convert_expression(julia_expr.right)
            
            # Map Julia operators to Runa operators
            operator_map = {
                '&&': 'and', '||': 'or', '!': 'not',
                '==': '==', '!=': '!=', 
                '<': '<', '>': '>', '<=': '<=', '>=': '>=',
                '+': '+', '-': '-', '*': '*', '/': '/', '^': '**', '%': '%'
            }
            
            op = operator_map.get(julia_expr.operator, julia_expr.operator)
            return BinaryExpression(left=left, operator=op, right=right)
        
        elif isinstance(julia_expr, JuliaUnaryExpression):
            operand = self.convert_expression(julia_expr.expression)
            
            operator_map = {'!': 'not', '-': '-', '+': '+'}
            op = operator_map.get(julia_expr.operator, julia_expr.operator)
            
            return UnaryExpression(operator=op, operand=operand)
        
        elif isinstance(julia_expr, JuliaCallExpression):
            function = self.convert_expression(julia_expr.function)
            arguments = [self.convert_expression(arg) for arg in julia_expr.arguments]
            
            # Handle keyword arguments by converting to named arguments
            for name, expr in julia_expr.keyword_arguments.items():
                arg = NamedArgument(name=name, value=self.convert_expression(expr))
                arguments.append(arg)
            
            return FunctionCall(function=function, arguments=arguments)
        
        elif isinstance(julia_expr, JuliaIndexExpression):
            object_expr = self.convert_expression(julia_expr.object)
            indices = [self.convert_expression(idx) for idx in julia_expr.indices]
            
            if len(indices) == 1:
                return IndexExpression(object=object_expr, index=indices[0])
            else:
                # Multiple indices - use tuple
                index_tuple = TupleLiteral(elements=indices)
                return IndexExpression(object=object_expr, index=index_tuple)
        
        elif isinstance(julia_expr, JuliaDotExpression):
            object_expr = self.convert_expression(julia_expr.object)
            return MemberAccess(object=object_expr, member=julia_expr.field)
        
        elif isinstance(julia_expr, JuliaBroadcastExpression):
            # Convert broadcasting to map function call
            if julia_expr.function:
                func = self.convert_expression(julia_expr.function)
                args = [self.convert_expression(arg) for arg in julia_expr.arguments]
                
                # map(function, iterable)
                return FunctionCall(
                    function=Identifier(name="map"),
                    arguments=[func] + args
                )
            
            return None
        
        elif isinstance(julia_expr, JuliaAssignmentExpression):
            target = self.convert_expression(julia_expr.target)
            value = self.convert_expression(julia_expr.value)
            
            return AssignmentExpression(
                target=target,
                operator=julia_expr.operator,
                value=value
            )
        
        elif isinstance(julia_expr, JuliaTernaryExpression):
            condition = self.convert_expression(julia_expr.condition)
            true_expr = self.convert_expression(julia_expr.true_expression)
            false_expr = self.convert_expression(julia_expr.false_expression)
            
            return ConditionalExpression(
                condition=condition,
                true_expression=true_expr,
                false_expression=false_expr
            )
        
        elif isinstance(julia_expr, JuliaMacroCall):
            # Convert macro calls to function calls with special annotation
            args = [self.convert_expression(arg) for arg in julia_expr.arguments]
            
            call = FunctionCall(
                function=Identifier(name=julia_expr.macro_name),
                arguments=args
            )
            call.annotations = [AnnotationNode(name="MacroCall")]
            return call
        
        elif isinstance(julia_expr, JuliaQuoteExpression):
            # Convert quoted expressions to string literals for now
            return LiteralExpression(value=f"quote_block", literal_type="quoted")
        
        return None


class RunaToJuliaConverter:
    """Converts Runa AST nodes to Julia AST nodes."""
    
    def __init__(self):
        self.type_mapping = {
            'integer': 'Int',
            'float': 'Float64',
            'string': 'String',
            'boolean': 'Bool',
            'null': 'Nothing',
            'List': 'Array',
            'Dictionary': 'Dict',
            'Array2D': 'Matrix'
        }
    
    def convert_program(self, runa_program: Program) -> JuliaProgram:
        """Convert Runa program to Julia program."""
        files = [self.convert_file(file) for file in runa_program.files]
        return JuliaProgram(files=files)
    
    def convert_file(self, runa_file: FileNode) -> JuliaFile:
        """Convert Runa file to Julia file."""
        imports = []
        declarations = []
        
        # Convert imports
        for imp in runa_file.imports:
            if imp.imported_names and "*" in imp.imported_names:
                julia_import = JuliaUsingDeclaration(package=imp.module_name)
            else:
                julia_import = JuliaImportDeclaration(
                    package=imp.module_name,
                    symbols=imp.imported_names or [],
                    alias=imp.alias
                )
            imports.append(julia_import)
        
        # Convert declarations
        for decl in runa_file.declarations:
            julia_decl = self.convert_declaration(decl)
            if julia_decl:
                declarations.append(julia_decl)
        
        return JuliaFile(imports=imports, declarations=declarations)
    
    def convert_declaration(self, runa_decl: ASTNode) -> Optional[JuliaNode]:
        """Convert Runa declaration to Julia declaration."""
        if isinstance(runa_decl, FunctionDeclaration):
            return self.convert_function(runa_decl)
        elif isinstance(runa_decl, ClassDeclaration):
            return self.convert_class(runa_decl)
        elif isinstance(runa_decl, VariableDeclaration):
            return self.convert_variable(runa_decl)
        elif isinstance(runa_decl, TypeAliasDeclaration):
            return self.convert_type_alias(runa_decl)
        elif isinstance(runa_decl, InterfaceDeclaration):
            return self.convert_interface(runa_decl)
        
        return None
    
    def convert_function(self, runa_func: FunctionDeclaration) -> JuliaFunctionDeclaration:
        """Convert Runa function to Julia function."""
        parameters = []
        
        for param in runa_func.parameters:
            julia_type = None
            if param.type:
                julia_type = self.convert_type(param.type)
            
            julia_param = JuliaParameter(
                name=param.name,
                type=julia_type,
                default_value=self.convert_expression(param.default_value) if param.default_value else None
            )
            parameters.append(julia_param)
        
        signature = JuliaFunctionSignature(parameters=parameters)
        
        # Convert function body
        body_statements = []
        for stmt in runa_func.body:
            julia_stmt = self.convert_statement(stmt)
            if julia_stmt:
                body_statements.append(julia_stmt)
        
        return_type = None
        if runa_func.return_type:
            return_type = self.convert_type(runa_func.return_type)
        
        return JuliaFunctionDeclaration(
            name=runa_func.name,
            signature=signature,
            body=body_statements,
            return_type=return_type
        )
    
    def convert_class(self, runa_class: ClassDeclaration) -> JuliaStructDeclaration:
        """Convert Runa class to Julia struct."""
        fields = []
        
        for member in runa_class.body:
            if isinstance(member, VariableDeclaration):
                julia_type = None
                if member.type:
                    julia_type = self.convert_type(member.type)
                
                field = JuliaFieldDeclaration(
                    name=member.name,
                    type=julia_type,
                    default_value=self.convert_expression(member.initial_value) if member.initial_value else None
                )
                fields.append(field)
        
        return JuliaStructDeclaration(
            name=runa_class.name,
            fields=fields,
            is_mutable=getattr(runa_class, 'is_mutable', False)
        )
    
    def convert_variable(self, runa_var: VariableDeclaration) -> JuliaNode:
        """Convert Runa variable to Julia variable or const."""
        if runa_var.is_constant:
            return JuliaConstDeclaration(
                name=runa_var.name,
                type=self.convert_type(runa_var.type) if runa_var.type else None,
                value=self.convert_expression(runa_var.initial_value) if runa_var.initial_value else None
            )
        else:
            # Regular assignment
            target = JuliaIdentifier(name=runa_var.name)
            value = self.convert_expression(runa_var.initial_value) if runa_var.initial_value else None
            
            return JuliaAssignmentExpression(
                target=target,
                operator="=",
                value=value
            )
    
    def convert_type_alias(self, runa_alias: TypeAliasDeclaration) -> JuliaTypeAlias:
        """Convert Runa type alias to Julia type alias."""
        return JuliaTypeAlias(
            name=runa_alias.name,
            target_type=self.convert_type(runa_alias.target_type) if runa_alias.target_type else None
        )
    
    def convert_interface(self, runa_interface: InterfaceDeclaration) -> JuliaAbstractTypeDeclaration:
        """Convert Runa interface to Julia abstract type."""
        supertype = None
        if runa_interface.extends:
            supertype = self.convert_type(runa_interface.extends)
        
        return JuliaAbstractTypeDeclaration(
            name=runa_interface.name,
            supertype=supertype
        )
    
    def convert_type(self, runa_type: TypeReference) -> JuliaType:
        """Convert Runa type to Julia type."""
        if isinstance(runa_type, UnionType):
            julia_types = [self.convert_type(t) for t in runa_type.types]
            return JuliaUnionType(types=julia_types)
        
        base_name = self.type_mapping.get(runa_type.name, runa_type.name)
        
        if runa_type.type_arguments:
            type_params = [self.convert_type(arg) for arg in runa_type.type_arguments]
            return JuliaParametricType(base_type=base_name, parameters=type_params)
        
        return JuliaParametricType(base_type=base_name, parameters=[])
    
    def convert_statement(self, runa_stmt: ASTNode) -> Optional[JuliaNode]:
        """Convert Runa statement to Julia statement."""
        if isinstance(runa_stmt, ReturnStatement):
            return JuliaReturnStatement(
                expression=self.convert_expression(runa_stmt.expression) if runa_stmt.expression else None
            )
        elif isinstance(runa_stmt, IfStatement):
            return self.convert_if(runa_stmt)
        elif isinstance(runa_stmt, ForStatement):
            return self.convert_for(runa_stmt)
        elif isinstance(runa_stmt, WhileStatement):
            return self.convert_while(runa_stmt)
        elif isinstance(runa_stmt, BreakStatement):
            return JuliaBreakStatement()
        elif isinstance(runa_stmt, ContinueStatement):
            return JuliaContinueStatement()
        elif isinstance(runa_stmt, ExpressionStatement):
            return self.convert_expression(runa_stmt.expression)
        
        return None
    
    def convert_if(self, runa_if: IfStatement) -> JuliaIfExpression:
        """Convert Runa if statement to Julia if expression."""
        condition = self.convert_expression(runa_if.condition)
        
        then_body = []
        for stmt in runa_if.then_body:
            julia_stmt = self.convert_statement(stmt)
            if julia_stmt:
                then_body.append(julia_stmt)
        
        else_body = []
        if runa_if.else_body:
            for stmt in runa_if.else_body:
                julia_stmt = self.convert_statement(stmt)
                if julia_stmt:
                    else_body.append(julia_stmt)
        
        return JuliaIfExpression(
            condition=condition,
            then_body=then_body,
            else_body=else_body
        )
    
    def convert_for(self, runa_for: ForStatement) -> JuliaForLoop:
        """Convert Runa for statement to Julia for loop."""
        iterable = self.convert_expression(runa_for.iterable)
        
        body = []
        for stmt in runa_for.body:
            julia_stmt = self.convert_statement(stmt)
            if julia_stmt:
                body.append(julia_stmt)
        
        return JuliaForLoop(
            variable=runa_for.variable,
            iterable=iterable,
            body=body
        )
    
    def convert_while(self, runa_while: WhileStatement) -> JuliaWhileLoop:
        """Convert Runa while statement to Julia while loop."""
        condition = self.convert_expression(runa_while.condition)
        
        body = []
        for stmt in runa_while.body:
            julia_stmt = self.convert_statement(stmt)
            if julia_stmt:
                body.append(julia_stmt)
        
        return JuliaWhileLoop(condition=condition, body=body)
    
    def convert_expression(self, runa_expr: Optional[Expression]) -> Optional[JuliaExpression]:
        """Convert Runa expression to Julia expression."""
        if runa_expr is None:
            return None
        
        if isinstance(runa_expr, Identifier):
            return JuliaIdentifier(name=runa_expr.name)
        
        elif isinstance(runa_expr, LiteralExpression):
            literal_type = self.type_mapping.get(runa_expr.literal_type, runa_expr.literal_type)
            
            if runa_expr.literal_type == "symbol":
                # Extract symbol name from :name format
                symbol_name = runa_expr.value
                if symbol_name.startswith(':'):
                    symbol_name = symbol_name[1:]
                return JuliaSymbolExpression(name=symbol_name)
            
            return JuliaLiteralExpression(
                value=runa_expr.value,
                literal_type=literal_type
            )
        
        elif isinstance(runa_expr, ArrayLiteral):
            elements = [self.convert_expression(elem) for elem in runa_expr.elements]
            return JuliaArrayExpression(elements=elements)
        
        elif isinstance(runa_expr, TupleLiteral):
            elements = [self.convert_expression(elem) for elem in runa_expr.elements]
            return JuliaTupleExpression(elements=elements)
        
        elif isinstance(runa_expr, DictionaryLiteral):
            pairs = []
            for key, value in runa_expr.pairs:
                julia_key = self.convert_expression(key)
                julia_value = self.convert_expression(value)
                pairs.append((julia_key, julia_value))
            return JuliaDictExpression(pairs=pairs)
        
        elif isinstance(runa_expr, BinaryExpression):
            left = self.convert_expression(runa_expr.left)
            right = self.convert_expression(runa_expr.right)
            
            # Map Runa operators to Julia operators
            operator_map = {
                'and': '&&', 'or': '||', 'not': '!',
                '==': '==', '!=': '!=',
                '<': '<', '>': '>', '<=': '<=', '>=': '>=',
                '+': '+', '-': '-', '*': '*', '/': '/', '**': '^', '%': '%'
            }
            
            op = operator_map.get(runa_expr.operator, runa_expr.operator)
            return JuliaBinaryExpression(left=left, operator=op, right=right)
        
        elif isinstance(runa_expr, UnaryExpression):
            operand = self.convert_expression(runa_expr.operand)
            
            operator_map = {'not': '!', '-': '-', '+': '+'}
            op = operator_map.get(runa_expr.operator, runa_expr.operator)
            
            return JuliaUnaryExpression(operator=op, expression=operand)
        
        elif isinstance(runa_expr, FunctionCall):
            function = self.convert_expression(runa_expr.function)
            arguments = []
            keyword_args = {}
            
            for arg in runa_expr.arguments:
                if isinstance(arg, NamedArgument):
                    keyword_args[arg.name] = self.convert_expression(arg.value)
                else:
                    arguments.append(self.convert_expression(arg))
            
            return JuliaCallExpression(
                function=function,
                arguments=arguments,
                keyword_arguments=keyword_args
            )
        
        elif isinstance(runa_expr, IndexExpression):
            object_expr = self.convert_expression(runa_expr.object)
            
            if isinstance(runa_expr.index, TupleLiteral):
                # Multiple indices
                indices = [self.convert_expression(elem) for elem in runa_expr.index.elements]
            else:
                indices = [self.convert_expression(runa_expr.index)]
            
            return JuliaIndexExpression(object=object_expr, indices=indices)
        
        elif isinstance(runa_expr, MemberAccess):
            object_expr = self.convert_expression(runa_expr.object)
            return JuliaDotExpression(object=object_expr, field=runa_expr.member)
        
        elif isinstance(runa_expr, AssignmentExpression):
            target = self.convert_expression(runa_expr.target)
            value = self.convert_expression(runa_expr.value)
            
            return JuliaAssignmentExpression(
                target=target,
                operator=runa_expr.operator,
                value=value
            )
        
        elif isinstance(runa_expr, ConditionalExpression):
            condition = self.convert_expression(runa_expr.condition)
            true_expr = self.convert_expression(runa_expr.true_expression)
            false_expr = self.convert_expression(runa_expr.false_expression)
            
            return JuliaTernaryExpression(
                condition=condition,
                true_expression=true_expr,
                false_expression=false_expr
            )
        
        elif isinstance(runa_expr, ListComprehension):
            # Convert to Julia array comprehension
            element = self.convert_expression(runa_expr.element)
            iterable = self.convert_expression(runa_expr.iterable)
            condition = self.convert_expression(runa_expr.condition) if runa_expr.condition else None
            
            generator = JuliaGenerator(
                variable=runa_expr.variable,
                iterable=iterable,
                condition=condition
            )
            
            return JuliaComprehension(
                expression=element,
                generators=[generator]
            )
        
        return None 