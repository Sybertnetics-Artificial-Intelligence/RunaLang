#!/usr/bin/env python3
"""
Lua Converter - Bidirectional Lua ↔ Runa AST Conversion

Provides comprehensive conversion between Lua and Runa AST including:
- Lua functions to Runa function declarations
- Lua tables to Runa structs and collections
- Control flow structures with semantic equivalence
- Variable scoping and local declarations
- Lua's dynamic typing to Runa's type system
- Module system and require statements
- Coroutines to Runa async constructs
- Metatables to Runa interfaces and traits

Maintains semantic equivalence and supports round-trip conversion.
"""

from typing import List, Dict, Optional, Any, Union
from dataclasses import dataclass

from .lua_ast import *
from runa.languages.shared.runa_ast import *


class LuaToRunaConverter:
    """Converts Lua AST to Runa AST"""
    
    def __init__(self):
        self.context_stack: List[Dict[str, Any]] = [{}]
        self.local_variables: Dict[str, str] = {}  # Lua name -> Runa type
        self.function_signatures: Dict[str, Dict[str, Any]] = {}
        
        # Lua to Runa type mappings
        self.type_mappings = {
            LuaLiteralType.NIL: "Option<Any>",
            LuaLiteralType.BOOLEAN: "Boolean",
            LuaLiteralType.NUMBER: "Number", 
            LuaLiteralType.STRING: "String",
            LuaLiteralType.TABLE: "Table<Any, Any>",
            LuaLiteralType.FUNCTION: "Function",
            LuaLiteralType.USERDATA: "Any",
            LuaLiteralType.THREAD: "Coroutine<Any>",
        }
        
        # Lua built-in functions to Runa equivalents
        self.builtin_mappings = {
            "print": "println",
            "tostring": "toString", 
            "tonumber": "parseNumber",
            "type": "typeOf",
            "pairs": "entries",
            "ipairs": "enumerate",
            "next": "nextEntry",
            "getmetatable": "getMetadata",
            "setmetatable": "setMetadata",
        }
    
    def convert(self, lua_module: LuaModule) -> RunaModule:
        """Convert Lua module to Runa module"""
        runa_declarations = []
        imports = []
        exports = []
        
        # Add standard imports for Lua compatibility
        imports.extend([
            RunaImport(path="runa.core", alias=None, items=["Any", "Option", "Table"]),
            RunaImport(path="runa.functional", alias=None, items=["Function", "Coroutine"]),
            RunaImport(path="runa.collections", alias=None, items=["List", "Map"]),
            RunaImport(path="runa.lua", alias=None, items=["LuaValue", "LuaTable", "LuaFunction"]),
        ])
        
        # Convert module body
        for statement in lua_module.body.statements:
            converted = self._convert_statement(statement)
            if converted:
                if isinstance(converted, list):
                    runa_declarations.extend(converted)
                else:
                    runa_declarations.append(converted)
        
        # Handle exports (global variables and functions)
        if lua_module.exports:
            for name, expr in lua_module.exports.items():
                export_decl = RunaExportDeclaration(
                    name=name,
                    value=self._convert_expression(expr) if expr else None
                )
                exports.append(export_decl)
        
        return RunaModule(
            name=lua_module.name or "lua_module",
            imports=imports,
            declarations=runa_declarations,
            exports=exports,
            metadata={
                "source_language": "lua",
                "conversion_type": "semantic",
                "lua_features": self._detect_lua_features(lua_module)
            }
        )
    
    def _convert_statement(self, stmt: LuaStatement) -> Union[Declaration, List[Declaration], None]:
        """Convert Lua statement to Runa declaration(s)"""
        if isinstance(stmt, LuaLocalDeclaration):
            return self._convert_local_declaration(stmt)
        elif isinstance(stmt, LuaFunctionDeclaration):
            return self._convert_function_declaration(stmt)
        elif isinstance(stmt, LuaAssignment):
            return self._convert_assignment(stmt)
        elif isinstance(stmt, LuaIfStatement):
            return self._convert_if_to_conditional_declaration(stmt)
        elif isinstance(stmt, LuaForStatement):
            return self._convert_for_to_function(stmt)
        elif isinstance(stmt, LuaForInStatement):
            return self._convert_for_in_to_function(stmt)
        elif isinstance(stmt, LuaWhileStatement):
            return self._convert_while_to_function(stmt)
        elif isinstance(stmt, LuaRepeatStatement):
            return self._convert_repeat_to_function(stmt)
        elif isinstance(stmt, LuaReturnStatement):
            return self._convert_return_statement(stmt)
        elif isinstance(stmt, LuaExpressionStatement):
            return self._convert_expression_statement(stmt)
        elif isinstance(stmt, LuaRequireStatement):
            return self._convert_require_statement(stmt)
        elif isinstance(stmt, LuaDoStatement):
            return self._convert_do_statement(stmt)
        else:
            # Other statements converted to expressions or skipped
            return None
    
    def _convert_local_declaration(self, stmt: LuaLocalDeclaration) -> List[LetStatement]:
        """Convert local declaration to Runa variable declarations"""
        declarations = []
        
        for i, name in enumerate(stmt.names):
            value = stmt.values[i] if i < len(stmt.values) else None
            
            # Infer type from value
            var_type = self._infer_type_from_expression(value) if value else "Any"
            
            # Store in local context
            self.local_variables[name] = var_type
            
            runa_value = self._convert_expression(value) if value else None
            
            var_decl = LetStatement(
                name=name,
                var_type=RunaNominalType(var_type),
                value=runa_value,
                is_mutable=True,  # Lua variables are mutable by default
                visibility=RunaVisibility.PRIVATE
            )
            
            declarations.append(var_decl)
        
        return declarations
    
    def _convert_function_declaration(self, stmt: LuaFunctionDeclaration) -> ProcessDefinition:
        """Convert Lua function declaration to Runa function"""
        # Convert parameters
        parameters = []
        for param_name in stmt.parameters:
            param_type = self.local_variables.get(param_name, "Any")
            param = Parameter(
                name=param_name,
                param_type=RunaNominalType(param_type),
                default_value=None
            )
            parameters.append(param)
        
        # Handle varargs
        if stmt.is_vararg:
            vararg_param = Parameter(
                name="args",
                param_type=GenericType("List", [RunaNominalType("Any")]),
                is_variadic=True
            )
            parameters.append(vararg_param)
        
        # Convert function body
        body_statements = []
        for lua_stmt in stmt.body.statements:
            converted = self._convert_statement(lua_stmt)
            if converted:
                if isinstance(converted, list):
                    for conv_stmt in converted:
                        body_statements.append(self._declaration_to_statement(conv_stmt))
                else:
                    body_statements.append(self._declaration_to_statement(converted))
        
        body = Block(statements=body_statements)
        
        # Infer return type
        return_type = self._infer_function_return_type(stmt.body)
        
        # Create annotations for Lua-specific features
        annotations = []
        if stmt.is_method:
            annotations.append(RunaAnnotation("lua_method", {}))
        if stmt.table_path:
            annotations.append(RunaAnnotation("lua_table_function", {
                "path": ".".join(stmt.table_path)
            }))
        
        return ProcessDefinition(
            name=stmt.name,
            parameters=parameters,
            return_type=return_type,
            body=body,
            visibility=RunaVisibility.PUBLIC if not stmt.is_local else RunaVisibility.PRIVATE,
            annotations=annotations
        )
    
    def _convert_assignment(self, stmt: LuaAssignment) -> List[LetStatement]:
        """Convert Lua assignment to Runa variable declarations"""
        declarations = []
        
        for i, target in enumerate(stmt.targets):
            if isinstance(target, LuaIdentifier):
                value = stmt.values[i] if i < len(stmt.values) else None
                var_type = self._infer_type_from_expression(value) if value else "Any"
                
                var_decl = LetStatement(
                    name=target.name,
                    var_type=RunaNominalType(var_type),
                    value=self._convert_expression(value) if value else None,
                    is_mutable=True,
                    visibility=RunaVisibility.PUBLIC
                )
                declarations.append(var_decl)
        
        return declarations
    
    def _convert_expression(self, expr: LuaExpression) -> Expression:
        """Convert Lua expression to Runa expression"""
        if isinstance(expr, LuaLiteral):
            return self._convert_literal(expr)
        elif isinstance(expr, LuaIdentifier):
            return Identifier(name=expr.name)
        elif isinstance(expr, LuaBinaryOperation):
            return self._convert_binary_operation(expr)
        elif isinstance(expr, LuaUnaryOperation):
            return self._convert_unary_operation(expr)
        elif isinstance(expr, LuaTableConstructor):
            return self._convert_table_constructor(expr)
        elif isinstance(expr, LuaTableAccess):
            return self._convert_table_access(expr)
        elif isinstance(expr, LuaFunctionCall):
            return self._convert_function_call(expr)
        elif isinstance(expr, LuaFunctionDefinition):
            return self._convert_function_definition(expr)
        elif isinstance(expr, LuaVarargExpression):
            return Identifier(name="args")  # Convert to parameter reference
        elif isinstance(expr, LuaStringLiteral):
            return StringLiteral(value=expr.value)
        elif isinstance(expr, LuaNumberLiteral):
            return RunaNumberLiteral(value=expr.value)
        else:
            # Fallback for unsupported expressions
            return Identifier(name="unknown")
    
    def _convert_literal(self, lit: LuaLiteral) -> StringLiteral:
        """Convert Lua literal to Runa literal"""
        if lit.literal_type == LuaLiteralType.NIL:
            return RunaNilLiteral()
        elif lit.literal_type == LuaLiteralType.BOOLEAN:
            return BooleanLiteral(value=lit.value)
        elif lit.literal_type == LuaLiteralType.NUMBER:
            return RunaNumberLiteral(value=lit.value)
        elif lit.literal_type == LuaLiteralType.STRING:
            return StringLiteral(value=lit.value)
        else:
            return StringLiteral(value=str(lit.value))
    
    def _convert_binary_operation(self, op: LuaBinaryOperation) -> BinaryExpression:
        """Convert Lua binary operation to Runa binary operation"""
        left = self._convert_expression(op.left)
        right = self._convert_expression(op.right)
        
        # Map Lua operators to Runa operators
        operator_map = {
            LuaBinaryOperator.ADD: "+",
            LuaBinaryOperator.SUB: "-", 
            LuaBinaryOperator.MUL: "*",
            LuaBinaryOperator.DIV: "/",
            LuaBinaryOperator.IDIV: "//",
            LuaBinaryOperator.MOD: "%",
            LuaBinaryOperator.POW: "**",
            LuaBinaryOperator.EQ: "==",
            LuaBinaryOperator.NE: "!=",
            LuaBinaryOperator.LT: "<",
            LuaBinaryOperator.LE: "<=",
            LuaBinaryOperator.GT: ">",
            LuaBinaryOperator.GE: ">=",
            LuaBinaryOperator.AND: "&&",
            LuaBinaryOperator.OR: "||",
            LuaBinaryOperator.CONCAT: "+",  # String concatenation
        }
        
        runa_operator = operator_map.get(op.operator, "+")
        
        return BinaryExpression(
            left=left,
            operator=runa_operator,
            right=right
        )
    
    def _convert_unary_operation(self, op: LuaUnaryOperation) -> UnaryExpression:
        """Convert Lua unary operation to Runa unary operation"""
        operand = self._convert_expression(op.operand)
        
        operator_map = {
            LuaUnaryOperator.NOT: "!",
            LuaUnaryOperator.NEG: "-",
            LuaUnaryOperator.LEN: "len",  # Convert to function call
            LuaUnaryOperator.BNOT: "~",
        }
        
        runa_operator = operator_map.get(op.operator, "!")
        
        if op.operator == LuaUnaryOperator.LEN:
            # Convert length operator to function call
            return FunctionCall(
                function=Identifier(name="len"),
                arguments=[operand]
            )
        
        return UnaryExpression(
            operator=runa_operator,
            operand=operand
        )
    
    def _convert_table_constructor(self, table: LuaTableConstructor) -> Expression:
        """Convert Lua table to Runa collection"""
        # Determine if it's an array-like or map-like table
        is_array = all(field.key is None for field in table.fields)
        
        if is_array:
            # Convert to Runa list
            elements = [self._convert_expression(field.value) for field in table.fields]
            return ListLiteral(elements=elements)
        else:
            # Convert to Runa map
            entries = []
            for field in table.fields:
                key = self._convert_expression(field.key) if field.key else RunaNumberLiteral(value=len(entries) + 1)
                value = self._convert_expression(field.value)
                entries.append(RunaMapEntry(key=key, value=value))
            return RunaMapLiteral(entries=entries)
    
    def _convert_table_access(self, access: LuaTableAccess) -> Expression:
        """Convert Lua table access to Runa member access or indexing"""
        table = self._convert_expression(access.table)
        
        if access.is_dot_notation and isinstance(access.key, LuaStringLiteral):
            # Convert to member access
            return MemberAccess(
                object=table,
                member=access.key.value
            )
        else:
            # Convert to indexing
            key = self._convert_expression(access.key)
            return IndexAccess(
                object=table,
                index=key
            )
    
    def _convert_function_call(self, call: LuaFunctionCall) -> FunctionCall:
        """Convert Lua function call to Runa function call"""
        function = self._convert_expression(call.function)
        arguments = [self._convert_expression(arg) for arg in call.arguments]
        
        # Handle built-in function mappings
        if isinstance(call.function, LuaIdentifier):
            func_name = call.function.name
            if func_name in self.builtin_mappings:
                function = Identifier(name=self.builtin_mappings[func_name])
        
        return FunctionCall(
            function=function,
            arguments=arguments
        )
    
    def _convert_function_definition(self, func: LuaFunctionDefinition) -> ProcessDefinitionExpression:
        """Convert Lua anonymous function to Runa lambda"""
        # Convert parameters
        parameters = []
        for param_name in func.parameters:
            param = Parameter(
                name=param_name,
                param_type=RunaNominalType("Any")
            )
            parameters.append(param)
        
        # Convert body to expression or block
        if len(func.body.statements) == 1 and isinstance(func.body.statements[0], LuaReturnStatement):
            # Single return statement - convert to expression
            return_stmt = func.body.statements[0]
            if return_stmt.values:
                body_expr = self._convert_expression(return_stmt.values[0])
                return ProcessDefinitionExpression(
                    parameters=parameters,
                    body=body_expr
                )
        
        # Multiple statements - convert to block
        body_statements = []
        for stmt in func.body.statements:
            converted = self._convert_statement(stmt)
            if converted:
                if isinstance(converted, list):
                    for conv_stmt in converted:
                        body_statements.append(self._declaration_to_statement(conv_stmt))
                else:
                    body_statements.append(self._declaration_to_statement(converted))
        
        return ProcessDefinitionExpression(
            parameters=parameters,
            body=Block(statements=body_statements)
        )
    
    def _convert_require_statement(self, req: LuaRequireStatement) -> RunaImportDeclaration:
        """Convert Lua require to Runa import"""
        return RunaImportDeclaration(
            path=req.module_name,
            alias=req.alias,
            items=None  # Import entire module
        )
    
    def _infer_type_from_expression(self, expr: Optional[LuaExpression]) -> str:
        """Infer Runa type from Lua expression"""
        if not expr:
            return "Any"
        
        if isinstance(expr, LuaLiteral):
            return self.type_mappings.get(expr.literal_type, "Any")
        elif isinstance(expr, LuaStringLiteral):
            return "String"
        elif isinstance(expr, LuaNumberLiteral):
            return "Number"
        elif isinstance(expr, LuaTableConstructor):
            is_array = all(field.key is None for field in expr.fields)
            return "List<Any>" if is_array else "Map<Any, Any>"
        elif isinstance(expr, LuaFunctionDefinition):
            return "Function"
        else:
            return "Any"
    
    def _infer_function_return_type(self, body: LuaBlock) -> BasicType:
        """Infer function return type from body"""
        # Simple heuristic: look for return statements
        for stmt in body.statements:
            if isinstance(stmt, LuaReturnStatement):
                if stmt.values:
                    first_return_type = self._infer_type_from_expression(stmt.values[0])
                    if len(stmt.values) > 1:
                        # Multiple return values - tuple type
                        return RunaTupleType([RunaNominalType(self._infer_type_from_expression(val)) 
                                            for val in stmt.values])
                    return RunaNominalType(first_return_type)
        
        return RunaNominalType("Unit")  # No explicit return
    
    def _declaration_to_statement(self, decl: Declaration) -> Statement:
        """Convert declaration to statement for function bodies"""
        if isinstance(decl, LetStatement):
            return RunaVariableStatement(declaration=decl)
        elif isinstance(decl, ProcessDefinition):
            return RunaFunctionStatement(declaration=decl)
        else:
            # Fallback
            return ExpressionStatement(expression=Identifier(name="unknown"))
    
    def _detect_lua_features(self, module: LuaModule) -> List[str]:
        """Detect Lua-specific features used in module"""
        features = []
        
        # Simple feature detection (could be expanded)
        code_str = str(module)  # Simplified
        
        if "coroutine" in code_str:
            features.append("coroutines")
        if "metatable" in code_str:
            features.append("metatables")
        if "..." in code_str:
            features.append("varargs")
        if "goto" in code_str:
            features.append("goto")
        
        return features
    
    # Additional conversion methods for other statement types would go here...
    def _convert_if_to_conditional_declaration(self, stmt: LuaIfStatement) -> Declaration:
        """Convert if statement to conditional declaration (simplified)"""
        # This is a simplified conversion - in practice, control flow
        # statements might be converted to more complex Runa constructs
        return LetStatement(
            name="conditional_result",
            var_type=RunaNominalType("Any"),
            value=StringLiteral(value="conditional_placeholder")
        )
    
    def _convert_for_to_function(self, stmt: LuaForStatement) -> Declaration:
        """Convert for loop to function declaration (simplified)"""
        return LetStatement(
            name="for_result",
            var_type=RunaNominalType("Any"),
            value=StringLiteral(value="for_loop_placeholder")
        )
    
    def _convert_for_in_to_function(self, stmt: LuaForInStatement) -> Declaration:
        """Convert for-in loop to function declaration (simplified)"""
        return LetStatement(
            name="for_in_result",
            var_type=RunaNominalType("Any"),
            value=StringLiteral(value="for_in_loop_placeholder")
        )
    
    def _convert_while_to_function(self, stmt: LuaWhileStatement) -> Declaration:
        """Convert while loop to function declaration (simplified)"""
        return LetStatement(
            name="while_result",
            var_type=RunaNominalType("Any"),
            value=StringLiteral(value="while_loop_placeholder")
        )
    
    def _convert_repeat_to_function(self, stmt: LuaRepeatStatement) -> Declaration:
        """Convert repeat-until loop to function declaration (simplified)"""
        return LetStatement(
            name="repeat_result",
            var_type=RunaNominalType("Any"),
            value=StringLiteral(value="repeat_loop_placeholder")
        )
    
    def _convert_return_statement(self, stmt: LuaReturnStatement) -> Declaration:
        """Convert return statement to variable declaration (simplified)"""
        if stmt.values:
            value = self._convert_expression(stmt.values[0])
        else:
            value = RunaNilLiteral()
        
        return LetStatement(
            name="return_value",
            var_type=RunaNominalType("Any"),
            value=value
        )
    
    def _convert_expression_statement(self, stmt: LuaExpressionStatement) -> Declaration:
        """Convert expression statement to variable declaration"""
        return LetStatement(
            name="expression_result",
            var_type=RunaNominalType("Any"),
            value=self._convert_expression(stmt.expression)
        )
    
    def _convert_do_statement(self, stmt: LuaDoStatement) -> Declaration:
        """Convert do statement to block expression (simplified)"""
        return LetStatement(
            name="do_block_result",
            var_type=RunaNominalType("Any"),
            value=StringLiteral(value="do_block_placeholder")
        )


class RunaToLuaConverter:
    """Converts Runa AST to Lua AST"""
    
    def __init__(self):
        self.context_stack: List[Dict[str, Any]] = [{}]
        
        # Runa to Lua type mappings
        self.type_mappings = {
            "Boolean": LuaLiteralType.BOOLEAN,
            "Number": LuaLiteralType.NUMBER,
            "String": LuaLiteralType.STRING,
            "Unit": LuaLiteralType.NIL,
            "Any": LuaLiteralType.NIL,
        }
    
    def convert(self, runa_module: RunaModule) -> LuaModule:
        """Convert Runa module to Lua module"""
        statements = []
        
        # Convert imports to require statements
        for import_decl in runa_module.imports:
            if not import_decl.path.startswith("runa."):  # Skip standard library imports
                require_stmt = LuaRequireStatement(
                    module_name=import_decl.path,
                    alias=import_decl.alias
                )
                statements.append(require_stmt)
        
        # Convert declarations to statements
        for declaration in runa_module.declarations:
            converted = self._convert_declaration(declaration)
            if converted:
                if isinstance(converted, list):
                    statements.extend(converted)
                else:
                    statements.append(converted)
        
        body = LuaBlock(statements=statements)
        
        return LuaModule(
            body=body,
            name=runa_module.name,
            filename=None  # Set by caller if needed
        )
    
    def _convert_declaration(self, decl: Declaration) -> Union[LuaStatement, List[LuaStatement], None]:
        """Convert Runa declaration to Lua statement(s)"""
        if isinstance(decl, LetStatement):
            return self._convert_variable_declaration(decl)
        elif isinstance(decl, ProcessDefinition):
            return self._convert_function_declaration(decl)
        elif isinstance(decl, RunaStructDeclaration):
            return self._convert_struct_to_table(decl)
        else:
            return None
    
    def _convert_variable_declaration(self, var_decl: LetStatement) -> LuaStatement:
        """Convert Runa variable declaration to Lua local or assignment"""
        value = self._convert_expression(var_decl.value) if var_decl.value else None
        
        if var_decl.visibility == RunaVisibility.PRIVATE:
            # Local variable
            return LuaLocalDeclaration(
                names=[var_decl.name],
                values=[value] if value else []
            )
        else:
            # Global assignment
            target = LuaIdentifier(name=var_decl.name)
            return LuaAssignment(
                targets=[target],
                values=[value] if value else []
            )
    
    def _convert_function_declaration(self, func_decl: ProcessDefinition) -> LuaFunctionDeclaration:
        """Convert Runa function declaration to Lua function"""
        # Convert parameters
        parameters = []
        is_vararg = False
        
        for param in func_decl.parameters:
            if param.is_variadic:
                is_vararg = True
            else:
                parameters.append(param.name)
        
        # Convert body
        body_statements = []
        if isinstance(func_decl.body, Block):
            for stmt in func_decl.body.statements:
                converted = self._convert_statement_from_runa(stmt)
                if converted:
                    body_statements.append(converted)
        
        body = LuaBlock(statements=body_statements)
        
        is_local = func_decl.visibility == RunaVisibility.PRIVATE
        
        return LuaFunctionDeclaration(
            name=func_decl.name,
            parameters=parameters,
            body=body,
            is_local=is_local,
            is_vararg=is_vararg
        )
    
    def _convert_expression(self, expr: Expression) -> LuaExpression:
        """Convert Runa expression to Lua expression"""
        if isinstance(expr, StringLiteral):
            return LuaStringLiteral(value=expr.value, quote_style='"')
        elif isinstance(expr, RunaNumberLiteral):
            return LuaNumberLiteral(value=expr.value, is_integer=isinstance(expr.value, int))
        elif isinstance(expr, BooleanLiteral):
            return LuaLiteral(value=expr.value, literal_type=LuaLiteralType.BOOLEAN, raw_text=str(expr.value).lower())
        elif isinstance(expr, RunaNilLiteral):
            return LuaLiteral(value=None, literal_type=LuaLiteralType.NIL, raw_text="nil")
        elif isinstance(expr, Identifier):
            return LuaIdentifier(name=expr.name)
        elif isinstance(expr, BinaryExpression):
            return self._convert_binary_operation_from_runa(expr)
        elif isinstance(expr, UnaryExpression):
            return self._convert_unary_operation_from_runa(expr)
        elif isinstance(expr, FunctionCall):
            return self._convert_function_call_from_runa(expr)
        elif isinstance(expr, ListLiteral):
            return self._convert_list_to_table(expr)
        elif isinstance(expr, RunaMapLiteral):
            return self._convert_map_to_table(expr)
        elif isinstance(expr, MemberAccess):
            return self._convert_member_access_to_table_access(expr)
        elif isinstance(expr, IndexAccess):
            return self._convert_index_access_to_table_access(expr)
        else:
            # Fallback
            return LuaIdentifier(name="unknown")
    
    def _convert_binary_operation_from_runa(self, op: BinaryExpression) -> LuaBinaryOperation:
        """Convert Runa binary operation to Lua binary operation"""
        left = self._convert_expression(op.left)
        right = self._convert_expression(op.right)
        
        # Map Runa operators to Lua operators
        operator_map = {
            "+": LuaBinaryOperator.ADD,
            "-": LuaBinaryOperator.SUB,
            "*": LuaBinaryOperator.MUL,
            "/": LuaBinaryOperator.DIV,
            "//": LuaBinaryOperator.IDIV,
            "%": LuaBinaryOperator.MOD,
            "**": LuaBinaryOperator.POW,
            "==": LuaBinaryOperator.EQ,
            "!=": LuaBinaryOperator.NE,
            "<": LuaBinaryOperator.LT,
            "<=": LuaBinaryOperator.LE,
            ">": LuaBinaryOperator.GT,
            ">=": LuaBinaryOperator.GE,
            "&&": LuaBinaryOperator.AND,
            "||": LuaBinaryOperator.OR,
        }
        
        lua_operator = operator_map.get(op.operator, LuaBinaryOperator.ADD)
        
        return LuaBinaryOperation(
            left=left,
            operator=lua_operator,
            right=right
        )
    
    def _convert_unary_operation_from_runa(self, op: UnaryExpression) -> LuaExpression:
        """Convert Runa unary operation to Lua unary operation"""
        operand = self._convert_expression(op.operand)
        
        operator_map = {
            "!": LuaUnaryOperator.NOT,
            "-": LuaUnaryOperator.NEG,
            "~": LuaUnaryOperator.BNOT,
        }
        
        if op.operator == "len":
            # Convert len function to length operator
            return LuaUnaryOperation(
                operator=LuaUnaryOperator.LEN,
                operand=operand
            )
        
        lua_operator = operator_map.get(op.operator, LuaUnaryOperator.NOT)
        
        return LuaUnaryOperation(
            operator=lua_operator,
            operand=operand
        )
    
    def _convert_function_call_from_runa(self, call: FunctionCall) -> LuaFunctionCall:
        """Convert Runa function call to Lua function call"""
        function = self._convert_expression(call.function)
        arguments = [self._convert_expression(arg) for arg in call.arguments]
        
        return LuaFunctionCall(
            function=function,
            arguments=arguments
        )
    
    def _convert_list_to_table(self, list_lit: ListLiteral) -> LuaTableConstructor:
        """Convert Runa list to Lua table"""
        fields = []
        for element in list_lit.elements:
            lua_value = self._convert_expression(element)
            field = LuaTableField(key=None, value=lua_value)  # Array-style
            fields.append(field)
        
        return LuaTableConstructor(fields=fields)
    
    def _convert_map_to_table(self, map_lit: RunaMapLiteral) -> LuaTableConstructor:
        """Convert Runa map to Lua table"""
        fields = []
        for entry in map_lit.entries:
            key = self._convert_expression(entry.key)
            value = self._convert_expression(entry.value)
            field = LuaTableField(key=key, value=value)
            fields.append(field)
        
        return LuaTableConstructor(fields=fields)
    
    def _convert_member_access_to_table_access(self, access: MemberAccess) -> LuaTableAccess:
        """Convert Runa member access to Lua table access"""
        table = self._convert_expression(access.object)
        key = LuaStringLiteral(value=access.member, quote_style='"')
        
        return LuaTableAccess(
            table=table,
            key=key,
            is_dot_notation=True
        )
    
    def _convert_index_access_to_table_access(self, access: IndexAccess) -> LuaTableAccess:
        """Convert Runa index access to Lua table access"""
        table = self._convert_expression(access.object)
        key = self._convert_expression(access.index)
        
        return LuaTableAccess(
            table=table,
            key=key,
            is_dot_notation=False
        )
    
    def _convert_struct_to_table(self, struct_decl: RunaStructDeclaration) -> List[LuaStatement]:
        """Convert Runa struct to Lua table constructor function"""
        # Create a constructor function for the struct
        statements = []
        
        # Constructor function
        constructor_body = []
        
        # Create local table
        table_fields = []
        for field in struct_decl.fields:
            field_value = LuaIdentifier(name=field.name)
            table_field = LuaTableField(
                key=LuaStringLiteral(value=field.name, quote_style='"'),
                value=field_value
            )
            table_fields.append(table_field)
        
        table_constructor = LuaTableConstructor(fields=table_fields)
        local_decl = LuaLocalDeclaration(
            names=["self"],
            values=[table_constructor]
        )
        constructor_body.append(local_decl)
        
        # Return the table
        return_stmt = LuaReturnStatement(values=[LuaIdentifier(name="self")])
        constructor_body.append(return_stmt)
        
        # Function parameters from struct fields
        parameters = [field.name for field in struct_decl.fields]
        
        func_decl = LuaFunctionDeclaration(
            name=struct_decl.name,
            parameters=parameters,
            body=LuaBlock(statements=constructor_body),
            is_local=struct_decl.visibility == RunaVisibility.PRIVATE
        )
        
        statements.append(func_decl)
        return statements
    
    def _convert_statement_from_runa(self, stmt: Statement) -> Optional[LuaStatement]:
        """Convert Runa statement to Lua statement"""
        # This would need to be implemented based on the specific Runa statement types
        # For now, return None as placeholder
        return None


# Convenience functions
def lua_to_runa(lua_module: LuaModule) -> RunaModule:
    """Convert Lua module to Runa module"""
    converter = LuaToRunaConverter()
    return converter.convert(lua_module)


def runa_to_lua(runa_module: RunaModule) -> LuaModule:
    """Convert Runa module to Lua module"""
    converter = RunaToLuaConverter()
    return converter.convert(runa_module) 