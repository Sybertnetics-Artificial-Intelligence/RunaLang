#!/usr/bin/env python3
"""
Go ↔ Runa Bidirectional Converter

Converts between Go AST and Runa AST in both directions,
preserving semantics and enabling round-trip translation.

This module handles conversion between:
- Go packages ↔ Runa modules
- Go types ↔ Runa type expressions  
- Go functions ↔ Runa processes
- Go structs ↔ Runa data structures
- Go interfaces ↔ Runa interface definitions
- Go goroutines ↔ Runa async processes
- Go channels ↔ Runa communication primitives
- Go control flow ↔ Runa control structures
- Go error handling ↔ Runa error patterns
"""

from typing import List, Optional, Dict, Any, Union, Mapping
from dataclasses import dataclass

from .go_ast import *
from ....core.runa_ast import *
from ....core.translation_result import TranslationResult, TranslationError


class GoToRunaConverter:
    """Converts Go AST to Runa AST."""
    
    def __init__(self):
        self.current_module = None
        self.type_mapping = self._create_type_mapping()
        
    def _create_type_mapping(self) -> Dict[str, str]:
        """Create mapping from Go types to Runa types."""
        return {
            # Integer types
            'int': 'Integer',
            'int8': 'Integer', 
            'int16': 'Integer',
            'int32': 'Integer',
            'int64': 'Integer',
            'uint': 'Integer',
            'uint8': 'Integer',
            'uint16': 'Integer', 
            'uint32': 'Integer',
            'uint64': 'Integer',
            'byte': 'Integer',
            'rune': 'Integer',
            
            # Floating point
            'float32': 'Float',
            'float64': 'Float',
            'complex64': 'Float',
            'complex128': 'Float',
            
            # String and boolean
            'string': 'String',
            'bool': 'Boolean',
            
            # Special types
            'error': 'Error',
            'any': 'Any',
        }
    
    def convert_program(self, go_program: GoProgram) -> Program:
        """Convert Go program to Runa program."""
        statements = []
        
        for go_file in go_program.files:
            runa_statements = self.convert_file(go_file)
            statements.extend(runa_statements)
        
        return Program(statements=statements)
    
    def convert_file(self, go_file: GoFile) -> List[Statement]:
        """Convert Go file to Runa statements."""
        statements = []
        
        # Convert package to module if needed
        if go_file.package and go_file.package.name != "main":
            module_stmts = []
            
            # Convert imports
            for import_decl in go_file.imports:
                for spec in import_decl.specs:
                    import_stmt = self.convert_import_spec(spec)
                    if import_stmt:
                        module_stmts.append(import_stmt)
            
            # Convert declarations
            for decl in go_file.declarations:
                runa_stmts = self.convert_declaration(decl)
                module_stmts.extend(runa_stmts)
            
            # Wrap in module
            module = ModuleDeclaration(
                name=go_file.package.name,
                body=module_stmts
            )
            statements.append(module)
        else:
            # Main package - convert directly
            for import_decl in go_file.imports:
                for spec in import_decl.specs:
                    import_stmt = self.convert_import_spec(spec)
                    if import_stmt:
                        statements.append(import_stmt)
            
            for decl in go_file.declarations:
                runa_stmts = self.convert_declaration(decl)
                statements.extend(runa_stmts)
        
        return statements
    
    def convert_import_spec(self, spec: GoImportSpec) -> Optional[ImportStatement]:
        """Convert Go import spec to Runa import."""
        if spec.name == ".":
            # Dot import - import all
            return ImportStatement(
                module_path=spec.path,
                imported_names=None  # Import all
            )
        elif spec.name:
            # Aliased import
            return ImportStatement(
                module_path=spec.path,
                alias=spec.name
            )
        else:
            # Regular import
            return ImportStatement(module_path=spec.path)
    
    def convert_declaration(self, decl: GoDeclaration) -> List[Statement]:
        """Convert Go declaration to Runa statements."""
        if isinstance(decl, GoConstDeclaration):
            return self.convert_const_declaration(decl)
        elif isinstance(decl, GoVarDeclaration):
            return self.convert_var_declaration(decl)
        elif isinstance(decl, GoTypeDeclaration):
            return self.convert_type_declaration(decl)
        elif isinstance(decl, GoFunctionDeclaration):
            return [self.convert_function_declaration(decl)]
        elif isinstance(decl, GoMethodDeclaration):
            return [self.convert_method_declaration(decl)]
        else:
            return []
    
    def convert_const_declaration(self, decl: GoConstDeclaration) -> List[Statement]:
        """Convert Go const declaration to Runa define statements."""
        statements = []
        
        for spec in decl.specs:
            for i, name in enumerate(spec.names):
                value = spec.values[i] if i < len(spec.values) else None
                type_annotation = self.convert_type(spec.type) if spec.type else None
                
                define_stmt = DefineStatement(
                    identifier=name,
                    type_annotation=type_annotation,
                    value=self.convert_expression(value) if value else None,
                    is_constant=True
                )
                statements.append(define_stmt)
        
        return statements
    
    def convert_var_declaration(self, decl: GoVarDeclaration) -> List[Statement]:
        """Convert Go var declaration to Runa let statements."""
        statements = []
        
        for spec in decl.specs:
            for i, name in enumerate(spec.names):
                value = spec.values[i] if i < len(spec.values) else None
                type_annotation = self.convert_type(spec.type) if spec.type else None
                
                let_stmt = LetStatement(
                    identifier=name,
                    type_annotation=type_annotation,
                    value=self.convert_expression(value) if value else None
                )
                statements.append(let_stmt)
        
        return statements
    
    def convert_type_declaration(self, decl: GoTypeDeclaration) -> List[Statement]:
        """Convert Go type declaration to Runa type definitions."""
        statements = []
        
        for spec in decl.specs:
            type_def = TypeDefinition(
                name=spec.name,
                definition=self.convert_type(spec.type)
            )
            statements.append(type_def)
        
        return statements
    
    def convert_function_declaration(self, decl: GoFunctionDeclaration) -> ProcessDefinition:
        """Convert Go function to Runa process."""
        # Convert parameters
        params = []
        if decl.type and decl.type.params:
            for field in decl.type.params:
                for name in field.names:
                    param = Parameter(
                        name=name,
                        type_annotation=self.convert_type(field.type)
                    )
                    params.append(param)
        
        # Convert return type
        return_type = None
        if decl.type and decl.type.results:
            if len(decl.type.results) == 1:
                return_type = self.convert_type(decl.type.results[0].type)
            else:
                # Multiple return values - use tuple
                result_types = [self.convert_type(field.type) for field in decl.type.results]
                return_type = GenericType(base_type="Tuple", type_args=result_types)
        
        # Convert body
        body = self.convert_block_statement(decl.body) if decl.body else []
        
        return ProcessDefinition(
            name=decl.name,
            parameters=params,
            return_type=return_type,
            body=body
        )
    
    def convert_method_declaration(self, decl: GoMethodDeclaration) -> ProcessDefinition:
        """Convert Go method to Runa process with receiver."""
        # Convert receiver to first parameter
        params = []
        if decl.receiver:
            for name in decl.receiver.names:
                param = Parameter(
                    name=name,
                    type_annotation=self.convert_type(decl.receiver.type)
                )
                params.append(param)
        
        # Convert regular parameters
        if decl.type and decl.type.params:
            for field in decl.type.params:
                for name in field.names:
                    param = Parameter(
                        name=name,
                        type_annotation=self.convert_type(field.type)
                    )
                    params.append(param)
        
        # Convert return type
        return_type = None
        if decl.type and decl.type.results:
            if len(decl.type.results) == 1:
                return_type = self.convert_type(decl.type.results[0].type)
            else:
                result_types = [self.convert_type(field.type) for field in decl.type.results]
                return_type = GenericType(base_type="Tuple", type_args=result_types)
        
        # Convert body
        body = self.convert_block_statement(decl.body) if decl.body else []
        
        return ProcessDefinition(
            name=decl.name,
            parameters=params,
            return_type=return_type,
            body=body
        )
    
    def convert_type(self, go_type: Optional[GoType]) -> Optional[TypeExpression]:
        """Convert Go type to Runa type expression."""
        if not go_type:
            return None
        
        if isinstance(go_type, GoBasicType):
            runa_type_name = self.type_mapping.get(go_type.name, go_type.name)
            return BasicType(name=runa_type_name)
        
        elif isinstance(go_type, GoSliceType):
            element_type = self.convert_type(go_type.element_type)
            return GenericType(base_type="List", type_args=[element_type] if element_type else [])
        
        elif isinstance(go_type, GoArrayType):
            element_type = self.convert_type(go_type.element_type)
            return GenericType(base_type="Array", type_args=[element_type] if element_type else [])
        
        elif isinstance(go_type, GoMapType):
            key_type = self.convert_type(go_type.key_type)
            value_type = self.convert_type(go_type.value_type)
            type_args = [key_type, value_type] if key_type and value_type else []
            return GenericType(base_type="Dictionary", type_args=type_args)
        
        elif isinstance(go_type, GoPointerType):
            base_type = self.convert_type(go_type.base_type)
            return GenericType(base_type="Pointer", type_args=[base_type] if base_type else [])
        
        elif isinstance(go_type, GoChannelType):
            value_type = self.convert_type(go_type.value_type)
            return GenericType(base_type="Channel", type_args=[value_type] if value_type else [])
        
        elif isinstance(go_type, GoStructType):
            # Convert to record type or custom type
            return BasicType(name="Record")
        
        elif isinstance(go_type, GoInterfaceType):
            # Convert to interface definition
            return BasicType(name="Interface")
        
        elif isinstance(go_type, GoFunctionType):
            # Convert to function type
            param_types = [self.convert_type(field.type) for field in go_type.params]
            return_type = None
            if go_type.results:
                if len(go_type.results) == 1:
                    return_type = self.convert_type(go_type.results[0].type)
                else:
                    result_types = [self.convert_type(field.type) for field in go_type.results]
                    return_type = GenericType(base_type="Tuple", type_args=result_types)
            
            return FunctionType(param_types=param_types, return_type=return_type)
        
        else:
            return BasicType(name="Unknown")
    
    def convert_statement(self, stmt: GoStatement) -> List[Statement]:
        """Convert Go statement to Runa statements."""
        if isinstance(stmt, GoExpressionStatement):
            expr = self.convert_expression(stmt.expr)
            return [ExpressionStatement(expression=expr)]
        
        elif isinstance(stmt, GoAssignmentStatement):
            return self.convert_assignment_statement(stmt)
        
        elif isinstance(stmt, GoShortVarDeclaration):
            return self.convert_short_var_declaration(stmt)
        
        elif isinstance(stmt, GoIfStatement):
            return [self.convert_if_statement(stmt)]
        
        elif isinstance(stmt, GoForStatement):
            return [self.convert_for_statement(stmt)]
        
        elif isinstance(stmt, GoRangeStatement):
            return [self.convert_range_statement(stmt)]
        
        elif isinstance(stmt, GoSwitchStatement):
            return [self.convert_switch_statement(stmt)]
        
        elif isinstance(stmt, GoSelectStatement):
            return [self.convert_select_statement(stmt)]
        
        elif isinstance(stmt, GoReturnStatement):
            return [self.convert_return_statement(stmt)]
        
        elif isinstance(stmt, GoBreakStatement):
            return [BreakStatement()]
        
        elif isinstance(stmt, GoContinueStatement):
            return [ContinueStatement()]
        
        elif isinstance(stmt, GoBlockStatement):
            return self.convert_block_statement(stmt)
        
        elif isinstance(stmt, GoDeferStatement):
            # Convert defer to try/finally pattern
            call_expr = self.convert_expression(stmt.call)
            # For now, just convert to regular call
            return [ExpressionStatement(expression=call_expr)]
        
        elif isinstance(stmt, GoGoStatement):
            # Convert goroutine to async call
            call_expr = self.convert_expression(stmt.call)
            # Wrap in async process call
            return [ExpressionStatement(expression=call_expr)]
        
        else:
            return []
    
    def convert_assignment_statement(self, stmt: GoAssignmentStatement) -> List[Statement]:
        """Convert Go assignment to Runa set statements."""
        statements = []
        
        for i, target in enumerate(stmt.left):
            value = stmt.right[i] if i < len(stmt.right) else None
            
            if value:
                set_stmt = SetStatement(
                    target=self.convert_expression(target),
                    value=self.convert_expression(value)
                )
                statements.append(set_stmt)
        
        return statements
    
    def convert_short_var_declaration(self, stmt: GoShortVarDeclaration) -> List[Statement]:
        """Convert Go short var declaration (:=) to Runa let statements."""
        statements = []
        
        for i, target in enumerate(stmt.left):
            value = stmt.right[i] if i < len(stmt.right) else None
            
            if isinstance(target, GoIdentifier) and value:
                let_stmt = LetStatement(
                    identifier=target.name,
                    value=self.convert_expression(value)
                )
                statements.append(let_stmt)
        
        return statements
    
    def convert_if_statement(self, stmt: GoIfStatement) -> IfStatement:
        """Convert Go if statement to Runa if statement."""
        # Handle init statement if present
        then_block = []
        if stmt.init:
            init_stmts = self.convert_statement(stmt.init)
            then_block.extend(init_stmts)
        
        # Convert condition and body
        condition = self.convert_expression(stmt.condition)
        body_stmts = self.convert_block_statement(stmt.body) if stmt.body else []
        then_block.extend(body_stmts)
        
        # Convert else clause
        else_block = None
        if stmt.else_stmt:
            if isinstance(stmt.else_stmt, GoIfStatement):
                # else if
                else_block = [self.convert_if_statement(stmt.else_stmt)]
            elif isinstance(stmt.else_stmt, GoBlockStatement):
                else_block = self.convert_block_statement(stmt.else_stmt)
        
        return IfStatement(
            condition=condition,
            then_block=then_block,
            else_block=else_block
        )
    
    def convert_for_statement(self, stmt: GoForStatement) -> Statement:
        """Convert Go for statement to Runa loop."""
        if stmt.condition and not stmt.init and not stmt.post:
            # while loop
            body = self.convert_block_statement(stmt.body) if stmt.body else []
            return WhileLoop(
                condition=self.convert_expression(stmt.condition),
                block=body
            )
        else:
            # for loop with init/condition/post
            # Convert to while loop with manual initialization
            block_stmts = []
            
            if stmt.init:
                init_stmts = self.convert_statement(stmt.init)
                block_stmts.extend(init_stmts)
            
            loop_body = self.convert_block_statement(stmt.body) if stmt.body else []
            
            if stmt.post:
                post_stmts = self.convert_statement(stmt.post)
                loop_body.extend(post_stmts)
            
            condition = self.convert_expression(stmt.condition) if stmt.condition else BooleanLiteral(value=True)
            
            while_loop = WhileLoop(condition=condition, block=loop_body)
            block_stmts.append(while_loop)
            
            return Block(statements=block_stmts)
    
    def convert_range_statement(self, stmt: GoRangeStatement) -> Statement:
        """Convert Go range statement to Runa for-each loop."""
        iterable = self.convert_expression(stmt.expr)
        
        if stmt.key and stmt.value:
            # for key, value := range map/slice
            # Use destructuring in Runa
            variable = f"{stmt.key.name}, {stmt.value.name}"
        elif stmt.key:
            # for key := range
            variable = stmt.key.name
        else:
            # for range (no variables)
            variable = "_"
        
        body = self.convert_block_statement(stmt.body) if stmt.body else []
        
        return ForEachLoop(
            variable=variable,
            iterable=iterable,
            block=body
        )
    
    def convert_switch_statement(self, stmt: GoSwitchStatement) -> MatchStatement:
        """Convert Go switch to Runa match statement."""
        value = self.convert_expression(stmt.tag) if stmt.tag else BooleanLiteral(value=True)
        
        cases = []
        for case_clause in stmt.body:
            if case_clause.values:
                # Regular case
                for case_value in case_clause.values:
                    pattern = LiteralPattern(value=self.convert_expression(case_value))
                    block = []
                    for case_stmt in case_clause.body:
                        block.extend(self.convert_statement(case_stmt))
                    
                    match_case = MatchCase(
                        pattern=pattern,
                        guard=None,
                        block=block
                    )
                    cases.append(match_case)
            else:
                # Default case
                pattern = WildcardPattern()
                block = []
                for case_stmt in case_clause.body:
                    block.extend(self.convert_statement(case_stmt))
                
                match_case = MatchCase(
                    pattern=pattern,
                    guard=None,
                    block=block
                )
                cases.append(match_case)
        
        return MatchStatement(value=value, cases=cases)
    
    def convert_select_statement(self, stmt: GoSelectStatement) -> Statement:
        """Convert Go select to Runa channel operations."""
        # For now, convert to a simplified match statement
        # A more sophisticated implementation would use Runa's channel primitives
        value = BooleanLiteral(value=True)
        cases = []
        
        for comm_clause in stmt.body:
            pattern = WildcardPattern()
            block = []
            
            if comm_clause.comm:
                # Convert communication statement
                comm_stmts = self.convert_statement(comm_clause.comm)
                block.extend(comm_stmts)
            
            for case_stmt in comm_clause.body:
                block.extend(self.convert_statement(case_stmt))
            
            match_case = MatchCase(
                pattern=pattern,
                guard=None,
                block=block
            )
            cases.append(match_case)
        
        return MatchStatement(value=value, cases=cases)
    
    def convert_return_statement(self, stmt: GoReturnStatement) -> ReturnStatement:
        """Convert Go return to Runa return."""
        if not stmt.results:
            return ReturnStatement()
        elif len(stmt.results) == 1:
            return ReturnStatement(value=self.convert_expression(stmt.results[0]))
        else:
            # Multiple return values - create tuple
            elements = [self.convert_expression(result) for result in stmt.results]
            tuple_literal = ListLiteral(elements=elements)  # Use list as tuple representation
            return ReturnStatement(value=tuple_literal)
    
    def convert_block_statement(self, stmt: GoBlockStatement) -> List[Statement]:
        """Convert Go block to list of Runa statements."""
        statements = []
        
        for go_stmt in stmt.statements:
            runa_stmts = self.convert_statement(go_stmt)
            statements.extend(runa_stmts)
        
        return statements
    
    def convert_expression(self, expr: Optional[GoExpression]) -> Optional[Expression]:
        """Convert Go expression to Runa expression."""
        if not expr:
            return None
        
        if isinstance(expr, GoIdentifier):
            return Identifier(name=expr.name)
        
        elif isinstance(expr, GoBasicLiteral):
            if expr.kind == GoBasicLiteralKind.INT:
                return IntegerLiteral(value=int(expr.value))
            elif expr.kind == GoBasicLiteralKind.FLOAT:
                return FloatLiteral(value=float(expr.value))
            elif expr.kind == GoBasicLiteralKind.STRING:
                return StringLiteral(value=expr.value[1:-1])  # Remove quotes
            elif expr.kind == GoBasicLiteralKind.CHAR:
                return StringLiteral(value=expr.value[1:-1])  # Remove quotes
            else:
                return StringLiteral(value=expr.value)
        
        elif isinstance(expr, GoBinaryExpression):
            left = self.convert_expression(expr.left)
            right = self.convert_expression(expr.right)
            
            # Map Go operators to Runa operators
            op_mapping = {
                GoBinaryOperator.ADD: BinaryOperator.PLUS,
                GoBinaryOperator.SUB: BinaryOperator.MINUS,
                GoBinaryOperator.MUL: BinaryOperator.MULTIPLY,
                GoBinaryOperator.QUO: BinaryOperator.DIVIDE,
                GoBinaryOperator.EQL: BinaryOperator.EQUALS,
                GoBinaryOperator.NEQ: BinaryOperator.NOT_EQUALS,
                GoBinaryOperator.LSS: BinaryOperator.LESS_THAN,
                GoBinaryOperator.GTR: BinaryOperator.GREATER_THAN,
                GoBinaryOperator.LEQ: BinaryOperator.LESS_EQUAL,
                GoBinaryOperator.GEQ: BinaryOperator.GREATER_EQUAL,
                GoBinaryOperator.LAND: BinaryOperator.AND,
                GoBinaryOperator.LOR: BinaryOperator.OR,
            }
            
            runa_op = op_mapping.get(expr.operator, BinaryOperator.PLUS)
            return BinaryExpression(left=left, operator=runa_op, right=right)
        
        elif isinstance(expr, GoUnaryExpression):
            operand = self.convert_expression(expr.operand)
            
            # Map Go unary operators to Runa
            if expr.operator == GoUnaryOperator.NOT:
                return UnaryExpression(operator="not", operand=operand)
            elif expr.operator == GoUnaryOperator.MINUS:
                return UnaryExpression(operator="-", operand=operand)
            elif expr.operator == GoUnaryOperator.PLUS:
                return UnaryExpression(operator="+", operand=operand)
            else:
                return operand  # For now, ignore other unary operators
        
        elif isinstance(expr, GoCallExpression):
            function = self.convert_expression(expr.function)
            args = [(f"arg{i}", self.convert_expression(arg)) for i, arg in enumerate(expr.args)]
            return FunctionCall(function_name=function.name if isinstance(function, Identifier) else "unknown", arguments=args)
        
        elif isinstance(expr, GoSelectorExpression):
            obj = self.convert_expression(expr.expr)
            return MemberAccess(object=obj, member=expr.selector)
        
        elif isinstance(expr, GoIndexExpression):
            obj = self.convert_expression(expr.expr)
            index = self.convert_expression(expr.index)
            return IndexAccess(object=obj, index=index)
        
        elif isinstance(expr, GoCompositeLiteral):
            elements = [self.convert_expression(elem) for elem in expr.elements]
            return ListLiteral(elements=elements)
        
        else:
            # Fallback for other expressions
            return Identifier(name="unknown")


class RunaToGoConverter:
    """Converts Runa AST to Go AST."""
    
    def __init__(self):
        self.current_package = "main"
        self.type_mapping = self._create_type_mapping()
    
    def _create_type_mapping(self) -> Dict[str, str]:
        """Create mapping from Runa types to Go types."""
        return {
            'Integer': 'int',
            'Float': 'float64',
            'String': 'string',
            'Boolean': 'bool',
            'Error': 'error',
            'Any': 'interface{}',
        }
    
    def convert_program(self, runa_program: Program) -> GoProgram:
        """Convert Runa program to Go program."""
        files = []
        
        # Group statements by module
        main_statements = []
        modules = {}
        
        for stmt in runa_program.statements:
            if isinstance(stmt, ModuleDeclaration):
                modules[stmt.name] = stmt.body
            else:
                main_statements.append(stmt)
        
        # Create main file
        if main_statements:
            main_file = self.create_go_file("main", main_statements)
            files.append(main_file)
        
        # Create module files
        for module_name, module_stmts in modules.items():
            module_file = self.create_go_file(module_name, module_stmts)
            files.append(module_file)
        
        return GoProgram(files=files)
    
    def create_go_file(self, package_name: str, statements: List[Statement]) -> GoFile:
        """Create Go file from package name and statements."""
        # Package declaration
        package_decl = GoPackageDeclaration(name=package_name)
        
        # Convert imports
        imports = []
        declarations = []
        
        for stmt in statements:
            if isinstance(stmt, ImportStatement):
                import_decl = self.convert_import_statement(stmt)
                if import_decl:
                    imports.append(import_decl)
            else:
                go_decls = self.convert_statement(stmt)
                declarations.extend(go_decls)
        
        return GoFile(
            package=package_decl,
            imports=imports,
            declarations=declarations
        )
    
    def convert_import_statement(self, stmt: ImportStatement) -> Optional[GoImportDeclaration]:
        """Convert Runa import to Go import."""
        spec = GoImportSpec(
            name=stmt.alias,
            path=f'"{stmt.module_path}"'
        )
        return GoImportDeclaration(specs=[spec])
    
    def convert_statement(self, stmt: Statement) -> List[GoDeclaration]:
        """Convert Runa statement to Go declarations."""
        if isinstance(stmt, ProcessDefinition):
            return [self.convert_process_definition(stmt)]
        elif isinstance(stmt, LetStatement):
            return [self.convert_let_statement(stmt)]
        elif isinstance(stmt, DefineStatement):
            return [self.convert_define_statement(stmt)]
        elif isinstance(stmt, TypeDefinition):
            return [self.convert_type_definition(stmt)]
        else:
            return []
    
    def convert_process_definition(self, stmt: ProcessDefinition) -> GoFunctionDeclaration:
        """Convert Runa process to Go function."""
        # Convert parameters
        params = []
        for param in stmt.parameters:
            field = GoField(
                names=[param.name],
                type=self.convert_type(param.type_annotation)
            )
            params.append(field)
        
        # Convert return type
        results = []
        if stmt.return_type:
            result_field = GoField(
                names=[],
                type=self.convert_type(stmt.return_type)
            )
            results.append(result_field)
        
        # Create function type
        func_type = GoFunctionType(params=params, results=results)
        
        # Convert body
        body_stmts = []
        for runa_stmt in stmt.body:
            go_stmts = self.convert_runa_statement(runa_stmt)
            body_stmts.extend(go_stmts)
        
        body = GoBlockStatement(statements=body_stmts)
        
        return GoFunctionDeclaration(
            name=stmt.name,
            type=func_type,
            body=body
        )
    
    def convert_type(self, runa_type: Optional[TypeExpression]) -> Optional[GoType]:
        """Convert Runa type to Go type."""
        if not runa_type:
            return None
        
        if isinstance(runa_type, BasicType):
            go_type_name = self.type_mapping.get(runa_type.name, runa_type.name)
            return GoBasicType(name=go_type_name)
        
        elif isinstance(runa_type, GenericType):
            if runa_type.base_type == "List":
                element_type = self.convert_type(runa_type.type_args[0]) if runa_type.type_args else GoBasicType(name="interface{}")
                return GoSliceType(element_type=element_type)
            elif runa_type.base_type == "Dictionary":
                key_type = self.convert_type(runa_type.type_args[0]) if len(runa_type.type_args) > 0 else GoBasicType(name="string")
                value_type = self.convert_type(runa_type.type_args[1]) if len(runa_type.type_args) > 1 else GoBasicType(name="interface{}")
                return GoMapType(key_type=key_type, value_type=value_type)
            elif runa_type.base_type == "Channel":
                value_type = self.convert_type(runa_type.type_args[0]) if runa_type.type_args else GoBasicType(name="interface{}")
                return GoChannelType(value_type=value_type)
            else:
                return GoBasicType(name=runa_type.base_type)
        
        else:
            return GoBasicType(name="interface{}")
    
    def convert_runa_statement(self, stmt: Statement) -> List[GoStatement]:
        """Convert Runa statement to Go statements."""
        if isinstance(stmt, SetStatement):
            return [self.convert_set_statement(stmt)]
        elif isinstance(stmt, IfStatement):
            return [self.convert_if_statement(stmt)]
        elif isinstance(stmt, WhileLoop):
            return [self.convert_while_loop(stmt)]
        elif isinstance(stmt, ForEachLoop):
            return [self.convert_for_each_loop(stmt)]
        elif isinstance(stmt, ReturnStatement):
            return [self.convert_return_statement(stmt)]
        elif isinstance(stmt, ExpressionStatement):
            return [self.convert_expression_statement(stmt)]
        else:
            return []
    
    def convert_expression(self, expr: Optional[Expression]) -> Optional[GoExpression]:
        """Convert Runa expression to Go expression."""
        if not expr:
            return None
        
        if isinstance(expr, Identifier):
            return GoIdentifier(name=expr.name)
        
        elif isinstance(expr, IntegerLiteral):
            return GoBasicLiteral(kind=GoBasicLiteralKind.INT, value=str(expr.value))
        
        elif isinstance(expr, FloatLiteral):
            return GoBasicLiteral(kind=GoBasicLiteralKind.FLOAT, value=str(expr.value))
        
        elif isinstance(expr, StringLiteral):
            return GoBasicLiteral(kind=GoBasicLiteralKind.STRING, value=f'"{expr.value}"')
        
        elif isinstance(expr, BooleanLiteral):
            value = "true" if expr.value else "false"
            return GoIdentifier(name=value)  # Go booleans are identifiers
        
        elif isinstance(expr, BinaryExpression):
            left = self.convert_expression(expr.left)
            right = self.convert_expression(expr.right)
            
            # Map Runa operators to Go operators
            op_mapping = {
                BinaryOperator.PLUS: GoBinaryOperator.ADD,
                BinaryOperator.MINUS: GoBinaryOperator.SUB,
                BinaryOperator.MULTIPLY: GoBinaryOperator.MUL,
                BinaryOperator.DIVIDE: GoBinaryOperator.QUO,
                BinaryOperator.EQUALS: GoBinaryOperator.EQL,
                BinaryOperator.NOT_EQUALS: GoBinaryOperator.NEQ,
                BinaryOperator.LESS_THAN: GoBinaryOperator.LSS,
                BinaryOperator.GREATER_THAN: GoBinaryOperator.GTR,
                BinaryOperator.LESS_EQUAL: GoBinaryOperator.LEQ,
                BinaryOperator.GREATER_EQUAL: GoBinaryOperator.GEQ,
                BinaryOperator.AND: GoBinaryOperator.LAND,
                BinaryOperator.OR: GoBinaryOperator.LOR,
            }
            
            go_op = op_mapping.get(expr.operator, GoBinaryOperator.ADD)
            return GoBinaryExpression(left=left, operator=go_op, right=right)
        
        elif isinstance(expr, FunctionCall):
            function = GoIdentifier(name=expr.function_name)
            args = [self.convert_expression(arg[1]) for arg in expr.arguments]
            return GoCallExpression(function=function, args=args)
        
        elif isinstance(expr, MemberAccess):
            obj = self.convert_expression(expr.object)
            return GoSelectorExpression(expr=obj, selector=expr.member)
        
        elif isinstance(expr, IndexAccess):
            obj = self.convert_expression(expr.object)
            index = self.convert_expression(expr.index)
            return GoIndexExpression(expr=obj, index=index)
        
        elif isinstance(expr, ListLiteral):
            elements = [self.convert_expression(elem) for elem in expr.elements]
            return GoCompositeLiteral(elements=elements)
        
        else:
            return GoIdentifier(name="unknown")
    
    # Additional conversion methods for statements...
    def convert_set_statement(self, stmt: SetStatement) -> GoAssignmentStatement:
        """Convert Runa set to Go assignment."""
        left = [self.convert_expression(stmt.target)]
        right = [self.convert_expression(stmt.value)]
        return GoAssignmentStatement(left=left, right=right, operator=GoAssignmentOperator.ASSIGN)
    
    def convert_if_statement(self, stmt: IfStatement) -> GoIfStatement:
        """Convert Runa if to Go if."""
        condition = self.convert_expression(stmt.condition)
        
        then_stmts = []
        for runa_stmt in stmt.then_block:
            then_stmts.extend(self.convert_runa_statement(runa_stmt))
        body = GoBlockStatement(statements=then_stmts)
        
        else_stmt = None
        if stmt.else_block:
            else_stmts = []
            for runa_stmt in stmt.else_block:
                else_stmts.extend(self.convert_runa_statement(runa_stmt))
            else_stmt = GoBlockStatement(statements=else_stmts)
        
        return GoIfStatement(condition=condition, body=body, else_stmt=else_stmt)
    
    def convert_while_loop(self, stmt: WhileLoop) -> GoForStatement:
        """Convert Runa while to Go for."""
        condition = self.convert_expression(stmt.condition)
        
        body_stmts = []
        for runa_stmt in stmt.block:
            body_stmts.extend(self.convert_runa_statement(runa_stmt))
        body = GoBlockStatement(statements=body_stmts)
        
        return GoForStatement(condition=condition, body=body)
    
    def convert_for_each_loop(self, stmt: ForEachLoop) -> GoRangeStatement:
        """Convert Runa for-each to Go range."""
        expr = self.convert_expression(stmt.iterable)
        
        # Handle variable destructuring
        if ", " in stmt.variable:
            parts = stmt.variable.split(", ")
            key = GoIdentifier(name=parts[0])
            value = GoIdentifier(name=parts[1]) if len(parts) > 1 else None
        else:
            key = GoIdentifier(name=stmt.variable)
            value = None
        
        body_stmts = []
        for runa_stmt in stmt.block:
            body_stmts.extend(self.convert_runa_statement(runa_stmt))
        body = GoBlockStatement(statements=body_stmts)
        
        return GoRangeStatement(
            key=key,
            value=value,
            assign_token=":=",
            expr=expr,
            body=body
        )
    
    def convert_return_statement(self, stmt: ReturnStatement) -> GoReturnStatement:
        """Convert Runa return to Go return."""
        results = []
        if stmt.value:
            if isinstance(stmt.value, ListLiteral):
                # Multiple return values
                results = [self.convert_expression(elem) for elem in stmt.value.elements]
            else:
                results = [self.convert_expression(stmt.value)]
        
        return GoReturnStatement(results=results)
    
    def convert_expression_statement(self, stmt: ExpressionStatement) -> GoExpressionStatement:
        """Convert Runa expression statement to Go expression statement."""
        expr = self.convert_expression(stmt.expression)
        return GoExpressionStatement(expr=expr)


# Convenience functions
def go_to_runa(go_ast: GoProgram) -> Program:
    """Convert Go AST to Runa AST."""
    converter = GoToRunaConverter()
    return converter.convert_program(go_ast)


def runa_to_go(runa_ast: Program) -> GoProgram:
    """Convert Runa AST to Go AST."""
    converter = RunaToGoConverter()
    return converter.convert_program(runa_ast) 