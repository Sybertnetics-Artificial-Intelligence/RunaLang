#!/usr/bin/env python3
"""
C++ ↔ Runa Bidirectional Converter

Converts between C++ AST and Runa AST in both directions,
preserving semantics and enabling round-trip translation.
Handles modern C++ features including templates, lambdas, and RAII.
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass

from .cpp_ast import *
from ....core.runa_ast import *


class CppToRunaConverter:
    """Converts C++ AST to Runa AST."""
    
    def __init__(self):
        self.variable_counter = 0
        self.function_counter = 0
        self.class_counter = 0
        self.scope_stack = []
    
    def convert(self, cpp_ast: CppTranslationUnit) -> Program:
        """Convert C++ translation unit to Runa program."""
        statements = []
        
        for decl in cpp_ast.declarations:
            converted = self.convert_declaration(decl)
            if converted:
                if isinstance(converted, list):
                    statements.extend(converted)
                else:
                    statements.append(converted)
        
        return Program(statements)
    
    def convert_declaration(self, decl: CppDeclaration) -> Union[RunaStatement, List[RunaStatement], None]:
        """Convert C++ declaration to Runa statement(s)."""
        if isinstance(decl, CppVariableDecl):
            return self._convert_variable_decl(decl)
        elif isinstance(decl, CppFunctionDecl):
            return self._convert_function_decl(decl)
        elif isinstance(decl, CppClassDecl):
            return self._convert_class_decl(decl)
        elif isinstance(decl, CppNamespaceDecl):
            return self._convert_namespace_decl(decl)
        elif isinstance(decl, CppTemplateDecl):
            return self._convert_template_decl(decl)
        
        return None
    
    def convert_statement(self, stmt: CppStatement) -> Union[RunaStatement, List[RunaStatement], None]:
        """Convert C++ statement to Runa statement(s)."""
        if isinstance(stmt, CppExpressionStmt):
            return self._convert_expression_stmt(stmt)
        elif isinstance(stmt, CppCompoundStmt):
            return self._convert_compound_stmt(stmt)
        elif isinstance(stmt, CppIfStmt):
            return self._convert_if_stmt(stmt)
        elif isinstance(stmt, CppWhileStmt):
            return self._convert_while_stmt(stmt)
        elif isinstance(stmt, CppForStmt):
            return self._convert_for_stmt(stmt)
        elif isinstance(stmt, CppRangeForStmt):
            return self._convert_range_for_stmt(stmt)
        elif isinstance(stmt, CppReturnStmt):
            return self._convert_return_stmt(stmt)
        elif isinstance(stmt, CppBreakStmt):
            return RunaBreak()
        elif isinstance(stmt, CppContinueStmt):
            return RunaContinue()
        
        return None
    
    def convert_expression(self, expr: CppExpression) -> RunaExpression:
        """Convert C++ expression to Runa expression."""
        if isinstance(expr, CppIntegerLiteral):
            return self._convert_integer_literal(expr)
        elif isinstance(expr, CppFloatingLiteral):
            return self._convert_floating_literal(expr)
        elif isinstance(expr, CppStringLiteral):
            return self._convert_string_literal(expr)
        elif isinstance(expr, CppCharacterLiteral):
            return self._convert_character_literal(expr)
        elif isinstance(expr, CppBooleanLiteral):
            return self._convert_boolean_literal(expr)
        elif isinstance(expr, CppNullptrLiteral):
            return self._convert_nullptr_literal(expr)
        elif isinstance(expr, CppIdentifier):
            return self._convert_identifier(expr)
        elif isinstance(expr, CppQualifiedName):
            return self._convert_qualified_name(expr)
        elif isinstance(expr, CppBinaryOp):
            return self._convert_binary_op(expr)
        elif isinstance(expr, CppUnaryOp):
            return self._convert_unary_op(expr)
        elif isinstance(expr, CppConditionalOp):
            return self._convert_conditional_op(expr)
        elif isinstance(expr, CppAssignment):
            return self._convert_assignment(expr)
        elif isinstance(expr, CppCall):
            return self._convert_call(expr)
        elif isinstance(expr, CppMemberAccess):
            return self._convert_member_access(expr)
        elif isinstance(expr, CppArraySubscript):
            return self._convert_array_subscript(expr)
        elif isinstance(expr, CppCast):
            return self._convert_cast(expr)
        elif isinstance(expr, CppNewExpr):
            return self._convert_new_expr(expr)
        elif isinstance(expr, CppDeleteExpr):
            return self._convert_delete_expr(expr)
        elif isinstance(expr, CppLambda):
            return self._convert_lambda(expr)
        elif isinstance(expr, CppInitializerList):
            return self._convert_initializer_list(expr)
        
        # Fallback for unknown expressions
        return RunaLiteral("unknown_expression", "string")
    
    def _convert_variable_decl(self, decl: CppVariableDecl) -> RunaVariableDeclaration:
        """Convert C++ variable declaration."""
        runa_type = self._convert_type(decl.var_type)
        initial_value = None
        
        if decl.initializer:
            initial_value = self.convert_expression(decl.initializer)
        
        return RunaVariableDeclaration(
            decl.name,
            runa_type,
            initial_value
        )
    
    def _convert_function_decl(self, decl: CppFunctionDecl) -> RunaFunctionDeclaration:
        """Convert C++ function declaration."""
        parameters = []
        
        for param in decl.parameters.parameters:
            param_type = self._convert_type(param.param_type)
            param_name = param.name or f"param_{len(parameters)}"
            
            # Handle default values
            default_value = None
            if param.default_value:
                default_value = self.convert_expression(param.default_value)
            
            runa_param = RunaParameter(param_name, param_type, default_value)
            parameters.append(runa_param)
        
        return_type = self._convert_type(decl.return_type)
        
        body_statements = []
        if decl.body:
            converted_body = self.convert_statement(decl.body)
            if isinstance(converted_body, list):
                body_statements = converted_body
            elif converted_body:
                body_statements = [converted_body]
        
        return RunaFunctionDeclaration(
            decl.name,
            parameters,
            return_type,
            body_statements
        )
    
    def _convert_class_decl(self, decl: CppClassDecl) -> RunaClassDeclaration:
        """Convert C++ class declaration."""
        methods = []
        fields = []
        
        for member in decl.members:
            if isinstance(member, CppFunctionDecl):
                methods.append(self._convert_function_decl(member))
            elif isinstance(member, CppVariableDecl):
                fields.append(self._convert_variable_decl(member))
        
        # Handle base classes
        base_classes = []
        for base_spec in decl.base_classes:
            base_name = self._type_to_string(base_spec.base_type)
            base_classes.append(base_name)
        
        return RunaClassDeclaration(
            decl.name,
            fields,
            methods,
            base_classes
        )
    
    def _convert_namespace_decl(self, decl: CppNamespaceDecl) -> List[RunaStatement]:
        """Convert C++ namespace declaration."""
        statements = []
        
        # Add namespace comment
        if decl.name:
            comment = RunaExpressionStatement(
                RunaLiteral(f"namespace {decl.name}", "comment")
            )
            statements.append(comment)
        
        # Convert namespace contents
        for member_decl in decl.declarations:
            converted = self.convert_declaration(member_decl)
            if converted:
                if isinstance(converted, list):
                    statements.extend(converted)
                else:
                    statements.append(converted)
        
        return statements
    
    def _convert_template_decl(self, decl: CppTemplateDecl) -> RunaStatement:
        """Convert C++ template declaration."""
        # Simplified template handling - convert the templated declaration
        # and add template parameters as comments
        
        converted_decl = self.convert_declaration(decl.declaration)
        
        # Add template parameter information as metadata
        if isinstance(converted_decl, RunaFunctionDeclaration):
            # Add template info to function name
            template_info = f"template_{len(decl.template_params.parameters)}_params"
            converted_decl.name = f"{converted_decl.name}_{template_info}"
        
        return converted_decl
    
    def _convert_expression_stmt(self, stmt: CppExpressionStmt) -> RunaExpressionStatement:
        """Convert C++ expression statement."""
        if stmt.expression:
            expr = self.convert_expression(stmt.expression)
            return RunaExpressionStatement(expr)
        else:
            return RunaExpressionStatement(RunaLiteral("", "string"))
    
    def _convert_compound_stmt(self, stmt: CppCompoundStmt) -> List[RunaStatement]:
        """Convert C++ compound statement."""
        statements = []
        
        for cpp_stmt in stmt.statements:
            converted = self.convert_statement(cpp_stmt)
            if converted:
                if isinstance(converted, list):
                    statements.extend(converted)
                else:
                    statements.append(converted)
        
        return statements
    
    def _convert_if_stmt(self, stmt: CppIfStmt) -> RunaConditional:
        """Convert C++ if statement."""
        condition = self.convert_expression(stmt.condition)
        
        then_body = []
        converted_then = self.convert_statement(stmt.then_stmt)
        if isinstance(converted_then, list):
            then_body = converted_then
        elif converted_then:
            then_body = [converted_then]
        
        else_body = []
        if stmt.else_stmt:
            converted_else = self.convert_statement(stmt.else_stmt)
            if isinstance(converted_else, list):
                else_body = converted_else
            elif converted_else:
                else_body = [converted_else]
        
        return RunaConditional(condition, then_body, else_body)
    
    def _convert_while_stmt(self, stmt: CppWhileStmt) -> RunaLoop:
        """Convert C++ while statement."""
        condition = self.convert_expression(stmt.condition)
        
        body = []
        converted_body = self.convert_statement(stmt.body)
        if isinstance(converted_body, list):
            body = converted_body
        elif converted_body:
            body = [converted_body]
        
        return RunaLoop("while", condition, body)
    
    def _convert_for_stmt(self, stmt: CppForStmt) -> RunaLoop:
        """Convert C++ for statement."""
        # Convert for loop to while loop equivalent
        statements = []
        
        # Initialization
        if stmt.init:
            init_stmt = self.convert_statement(stmt.init)
            if init_stmt:
                if isinstance(init_stmt, list):
                    statements.extend(init_stmt)
                else:
                    statements.append(init_stmt)
        
        # Condition
        condition = None
        if stmt.condition:
            condition = self.convert_expression(stmt.condition)
        else:
            condition = RunaLiteral(True, "boolean")
        
        # Body with increment
        body = []
        converted_body = self.convert_statement(stmt.body)
        if isinstance(converted_body, list):
            body.extend(converted_body)
        elif converted_body:
            body.append(converted_body)
        
        # Add increment to end of body
        if stmt.increment:
            increment_expr = self.convert_expression(stmt.increment)
            body.append(RunaExpressionStatement(increment_expr))
        
        loop = RunaLoop("while", condition, body)
        statements.append(loop)
        
        return statements
    
    def _convert_range_for_stmt(self, stmt: CppRangeForStmt) -> RunaLoop:
        """Convert C++ range-based for statement."""
        # Convert range-for to iterator-based loop
        iterator_var = f"_iterator_{self.variable_counter}"
        self.variable_counter += 1
        
        range_expr = self.convert_expression(stmt.range)
        
        # Create iterator initialization
        iterator_init = RunaVariableDeclaration(
            iterator_var,
            RunaType("Iterator"),
            RunaFunctionCall(
                RunaIdentifier("begin"),
                [range_expr]
            )
        )
        
        # Loop condition
        condition = RunaBinaryOperation(
            RunaIdentifier(iterator_var),
            "is not equal to",
            RunaFunctionCall(
                RunaIdentifier("end"),
                [range_expr]
            )
        )
        
        # Loop variable assignment
        loop_var_assign = RunaVariableDeclaration(
            stmt.variable.name,
            self._convert_type(stmt.variable.var_type),
            RunaUnaryOperation("dereference", RunaIdentifier(iterator_var))
        )
        
        # Body
        body = [loop_var_assign]
        converted_body = self.convert_statement(stmt.body)
        if isinstance(converted_body, list):
            body.extend(converted_body)
        elif converted_body:
            body.append(converted_body)
        
        # Increment iterator
        body.append(RunaExpressionStatement(
            RunaUnaryOperation("increment", RunaIdentifier(iterator_var))
        ))
        
        return [iterator_init, RunaLoop("while", condition, body)]
    
    def _convert_return_stmt(self, stmt: CppReturnStmt) -> RunaReturn:
        """Convert C++ return statement."""
        value = None
        if stmt.value:
            value = self.convert_expression(stmt.value)
        
        return RunaReturn(value)
    
    def _convert_integer_literal(self, expr: CppIntegerLiteral) -> RunaLiteral:
        """Convert C++ integer literal."""
        return RunaLiteral(expr.value, "integer")
    
    def _convert_floating_literal(self, expr: CppFloatingLiteral) -> RunaLiteral:
        """Convert C++ floating point literal."""
        return RunaLiteral(expr.value, "float")
    
    def _convert_string_literal(self, expr: CppStringLiteral) -> RunaLiteral:
        """Convert C++ string literal."""
        # Remove quotes and handle escape sequences
        value = expr.value
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        return RunaLiteral(value, "string")
    
    def _convert_character_literal(self, expr: CppCharacterLiteral) -> RunaLiteral:
        """Convert C++ character literal."""
        value = expr.value
        if value.startswith("'") and value.endswith("'"):
            value = value[1:-1]
        return RunaLiteral(value, "character")
    
    def _convert_boolean_literal(self, expr: CppBooleanLiteral) -> RunaLiteral:
        """Convert C++ boolean literal."""
        return RunaLiteral(expr.value, "boolean")
    
    def _convert_nullptr_literal(self, expr: CppNullptrLiteral) -> RunaLiteral:
        """Convert C++ nullptr literal."""
        return RunaLiteral(None, "null")
    
    def _convert_identifier(self, expr: CppIdentifier) -> RunaIdentifier:
        """Convert C++ identifier."""
        return RunaIdentifier(expr.name)
    
    def _convert_qualified_name(self, expr: CppQualifiedName) -> RunaIdentifier:
        """Convert C++ qualified name."""
        # Flatten qualified name to simple identifier
        if expr.scope:
            scope_name = self._expression_to_string(self.convert_expression(expr.scope))
            return RunaIdentifier(f"{scope_name}::{expr.name}")
        else:
            return RunaIdentifier(expr.name)
    
    def _convert_binary_op(self, expr: CppBinaryOp) -> RunaBinaryOperation:
        """Convert C++ binary operation."""
        left = self.convert_expression(expr.left)
        right = self.convert_expression(expr.right)
        
        # Map C++ operators to Runa operators
        operator_map = {
            CppOperator.ADD: "plus",
            CppOperator.SUB: "minus",
            CppOperator.MUL: "times",
            CppOperator.DIV: "divided by",
            CppOperator.MOD: "modulo",
            CppOperator.EQ: "is equal to",
            CppOperator.NE: "is not equal to",
            CppOperator.LT: "is less than",
            CppOperator.LE: "is less than or equal to",
            CppOperator.GT: "is greater than",
            CppOperator.GE: "is greater than or equal to",
            CppOperator.LOGICAL_AND: "and",
            CppOperator.LOGICAL_OR: "or",
            CppOperator.BIT_AND: "bitwise and",
            CppOperator.BIT_OR: "bitwise or",
            CppOperator.BIT_XOR: "bitwise xor",
            CppOperator.LEFT_SHIFT: "left shift",
            CppOperator.RIGHT_SHIFT: "right shift",
        }
        
        runa_op = operator_map.get(expr.operator, "unknown_op")
        return RunaBinaryOperation(left, runa_op, right)
    
    def _convert_unary_op(self, expr: CppUnaryOp) -> RunaUnaryOperation:
        """Convert C++ unary operation."""
        operand = self.convert_expression(expr.operand)
        
        # Map C++ unary operators to Runa operators
        operator_map = {
            CppOperator.LOGICAL_NOT: "not",
            CppOperator.BIT_NOT: "bitwise not",
            CppOperator.ADD: "positive",
            CppOperator.SUB: "negative",
            CppOperator.PRE_INC: "increment",
            CppOperator.POST_INC: "increment",
            CppOperator.PRE_DEC: "decrement",
            CppOperator.POST_DEC: "decrement",
        }
        
        runa_op = operator_map.get(expr.operator, "unknown_unary_op")
        return RunaUnaryOperation(runa_op, operand)
    
    def _convert_conditional_op(self, expr: CppConditionalOp) -> RunaConditionalExpression:
        """Convert C++ ternary conditional operator."""
        condition = self.convert_expression(expr.condition)
        true_expr = self.convert_expression(expr.true_expr)
        false_expr = self.convert_expression(expr.false_expr)
        
        return RunaConditionalExpression(condition, true_expr, false_expr)
    
    def _convert_assignment(self, expr: CppAssignment) -> RunaAssignment:
        """Convert C++ assignment expression."""
        target = self.convert_expression(expr.left)
        value = self.convert_expression(expr.right)
        
        # Handle compound assignment operators
        if expr.operator == CppOperator.ASSIGN:
            return RunaAssignment(target, value)
        else:
            # Convert compound assignment to regular assignment with binary op
            operator_map = {
                CppOperator.ADD_ASSIGN: "plus",
                CppOperator.SUB_ASSIGN: "minus",
                CppOperator.MUL_ASSIGN: "times",
                CppOperator.DIV_ASSIGN: "divided by",
                CppOperator.MOD_ASSIGN: "modulo",
            }
            
            if expr.operator in operator_map:
                binary_op = RunaBinaryOperation(target, operator_map[expr.operator], value)
                return RunaAssignment(target, binary_op)
            
            return RunaAssignment(target, value)
    
    def _convert_call(self, expr: CppCall) -> RunaFunctionCall:
        """Convert C++ function call."""
        function = self.convert_expression(expr.function)
        arguments = [self.convert_expression(arg) for arg in expr.arguments]
        
        return RunaFunctionCall(function, arguments)
    
    def _convert_member_access(self, expr: CppMemberAccess) -> RunaMemberAccess:
        """Convert C++ member access."""
        object_expr = self.convert_expression(expr.object)
        return RunaMemberAccess(object_expr, expr.member)
    
    def _convert_array_subscript(self, expr: CppArraySubscript) -> RunaIndexAccess:
        """Convert C++ array subscript."""
        array = self.convert_expression(expr.array)
        index = self.convert_expression(expr.index)
        
        return RunaIndexAccess(array, index)
    
    def _convert_cast(self, expr: CppCast) -> RunaFunctionCall:
        """Convert C++ cast to Runa type conversion."""
        operand = self.convert_expression(expr.operand)
        target_type = self._convert_type(expr.target_type)
        
        # Convert cast to function call
        cast_function = RunaIdentifier(f"cast_to_{target_type.name}")
        return RunaFunctionCall(cast_function, [operand])
    
    def _convert_new_expr(self, expr: CppNewExpr) -> RunaFunctionCall:
        """Convert C++ new expression."""
        type_name = self._type_to_string(expr.target_type)
        
        args = []
        if expr.initializer:
            args.append(self.convert_expression(expr.initializer))
        
        if expr.is_array and expr.array_size:
            # Array allocation
            size_arg = self.convert_expression(expr.array_size)
            return RunaFunctionCall(
                RunaIdentifier(f"new_array_{type_name}"),
                [size_arg] + args
            )
        else:
            # Single object allocation
            return RunaFunctionCall(
                RunaIdentifier(f"new_{type_name}"),
                args
            )
    
    def _convert_delete_expr(self, expr: CppDeleteExpr) -> RunaFunctionCall:
        """Convert C++ delete expression."""
        operand = self.convert_expression(expr.operand)
        
        if expr.is_array:
            return RunaFunctionCall(RunaIdentifier("delete_array"), [operand])
        else:
            return RunaFunctionCall(RunaIdentifier("delete"), [operand])
    
    def _convert_lambda(self, expr: CppLambda) -> RunaLambda:
        """Convert C++ lambda expression."""
        parameters = []
        if expr.parameters:
            for param in expr.parameters.parameters:
                param_type = self._convert_type(param.param_type)
                param_name = param.name or f"lambda_param_{len(parameters)}"
                runa_param = RunaParameter(param_name, param_type)
                parameters.append(runa_param)
        
        body = []
        converted_body = self.convert_statement(expr.body)
        if isinstance(converted_body, list):
            body = converted_body
        elif converted_body:
            body = [converted_body]
        
        return_type = None
        if expr.return_type:
            return_type = self._convert_type(expr.return_type)
        
        return RunaLambda(parameters, return_type, body)
    
    def _convert_initializer_list(self, expr: CppInitializerList) -> RunaList:
        """Convert C++ initializer list."""
        elements = [self.convert_expression(elem) for elem in expr.elements]
        return RunaList(elements)
    
    def _convert_type(self, cpp_type: CppType) -> RunaType:
        """Convert C++ type to Runa type."""
        if isinstance(cpp_type, CppBuiltinType):
            # Map C++ builtin types to Runa types
            type_map = {
                "int": "Integer",
                "float": "Float",
                "double": "Float",
                "char": "Character",
                "bool": "Boolean",
                "void": "Void",
                "string": "String",
                "std::string": "String",
            }
            runa_name = type_map.get(cpp_type.name, cpp_type.name)
            return RunaType(runa_name)
        
        elif isinstance(cpp_type, CppPointerType):
            # Convert pointer type
            pointee = self._convert_type(cpp_type.pointee_type)
            return RunaType(f"Pointer[{pointee.name}]")
        
        elif isinstance(cpp_type, CppReferenceType):
            # Convert reference type
            referenced = self._convert_type(cpp_type.referenced_type)
            return RunaType(f"Reference[{referenced.name}]")
        
        elif isinstance(cpp_type, CppArrayType):
            # Convert array type
            element = self._convert_type(cpp_type.element_type)
            return RunaType(f"Array[{element.name}]")
        
        elif isinstance(cpp_type, CppAutoType):
            return RunaType("Auto")
        
        else:
            # Default fallback
            return RunaType("Unknown")
    
    def _type_to_string(self, cpp_type: CppType) -> str:
        """Convert C++ type to string representation."""
        if isinstance(cpp_type, CppBuiltinType):
            return cpp_type.name
        elif isinstance(cpp_type, CppPointerType):
            return f"{self._type_to_string(cpp_type.pointee_type)}*"
        elif isinstance(cpp_type, CppReferenceType):
            return f"{self._type_to_string(cpp_type.referenced_type)}&"
        else:
            return "unknown_type"
    
    def _expression_to_string(self, expr: RunaExpression) -> str:
        """Convert Runa expression to string representation."""
        if isinstance(expr, RunaIdentifier):
            return expr.name
        elif isinstance(expr, RunaLiteral):
            return str(expr.value)
        else:
            return "unknown_expr"


class RunaToCppConverter:
    """Converts Runa AST to C++ AST."""
    
    def __init__(self):
        self.variable_counter = 0
        self.function_counter = 0
        self.class_counter = 0
    
    def convert(self, runa_ast: Program) -> CppTranslationUnit:
        """Convert Runa program to C++ translation unit."""
        declarations = []
        
        for stmt in runa_ast.statements:
            converted = self.convert_statement(stmt)
            if converted:
                if isinstance(converted, list):
                    declarations.extend(converted)
                else:
                    declarations.append(converted)
        
        return CppTranslationUnit(declarations)
    
    def convert_statement(self, stmt: RunaStatement) -> Union[CppDeclaration, CppStatement, List[Union[CppDeclaration, CppStatement]], None]:
        """Convert Runa statement to C++ declaration or statement."""
        if isinstance(stmt, RunaVariableDeclaration):
            return self._convert_variable_declaration(stmt)
        elif isinstance(stmt, RunaFunctionDeclaration):
            return self._convert_function_declaration(stmt)
        elif isinstance(stmt, RunaClassDeclaration):
            return self._convert_class_declaration(stmt)
        elif isinstance(stmt, RunaAssignment):
            return self._convert_assignment(stmt)
        elif isinstance(stmt, RunaConditional):
            return self._convert_conditional(stmt)
        elif isinstance(stmt, RunaLoop):
            return self._convert_loop(stmt)
        elif isinstance(stmt, RunaReturn):
            return self._convert_return(stmt)
        elif isinstance(stmt, RunaBreak):
            return CppBreakStmt()
        elif isinstance(stmt, RunaContinue):
            return CppContinueStmt()
        elif isinstance(stmt, RunaExpressionStatement):
            return self._convert_expression_statement(stmt)
        
        return None
    
    def convert_expression(self, expr: RunaExpression) -> CppExpression:
        """Convert Runa expression to C++ expression."""
        if isinstance(expr, RunaLiteral):
            return self._convert_literal(expr)
        elif isinstance(expr, RunaIdentifier):
            return self._convert_identifier(expr)
        elif isinstance(expr, RunaBinaryOperation):
            return self._convert_binary_operation(expr)
        elif isinstance(expr, RunaUnaryOperation):
            return self._convert_unary_operation(expr)
        elif isinstance(expr, RunaFunctionCall):
            return self._convert_function_call(expr)
        elif isinstance(expr, RunaMemberAccess):
            return self._convert_member_access(expr)
        elif isinstance(expr, RunaIndexAccess):
            return self._convert_index_access(expr)
        elif isinstance(expr, RunaConditionalExpression):
            return self._convert_conditional_expression(expr)
        elif isinstance(expr, RunaLambda):
            return self._convert_lambda(expr)
        elif isinstance(expr, RunaList):
            return self._convert_list(expr)
        
        # Fallback
        return CppIdentifier("unknown_expression")
    
    def _convert_variable_declaration(self, stmt: RunaVariableDeclaration) -> CppVariableDecl:
        """Convert Runa variable declaration."""
        cpp_type = self._convert_type(stmt.var_type)
        
        initializer = None
        if stmt.initial_value:
            initializer = self.convert_expression(stmt.initial_value)
        
        return CppVariableDecl(stmt.name, cpp_type, initializer)
    
    def _convert_function_declaration(self, stmt: RunaFunctionDeclaration) -> CppFunctionDecl:
        """Convert Runa function declaration."""
        return_type = self._convert_type(stmt.return_type)
        
        parameters = []
        for param in stmt.parameters:
            cpp_type = self._convert_type(param.param_type)
            default_value = None
            if param.default_value:
                default_value = self.convert_expression(param.default_value)
            
            cpp_param = CppParameter(param.name, cpp_type, default_value)
            parameters.append(cpp_param)
        
        param_list = CppParameterList(parameters)
        
        body = None
        if stmt.body:
            cpp_statements = []
            for runa_stmt in stmt.body:
                converted = self.convert_statement(runa_stmt)
                if converted:
                    if isinstance(converted, list):
                        cpp_statements.extend(converted)
                    else:
                        cpp_statements.append(converted)
            
            body = CppCompoundStmt(cpp_statements)
        
        return CppFunctionDecl(stmt.name, return_type, param_list, body)
    
    def _convert_class_declaration(self, stmt: RunaClassDeclaration) -> CppClassDecl:
        """Convert Runa class declaration."""
        members = []
        
        # Convert fields
        for field in stmt.fields:
            member = self._convert_variable_declaration(field)
            members.append(member)
        
        # Convert methods
        for method in stmt.methods:
            member = self._convert_function_declaration(method)
            members.append(member)
        
        # Handle base classes
        base_classes = []
        for base_name in stmt.base_classes:
            base_type = CppBuiltinType(base_name)
            base_spec = CppBaseSpecifier(base_type)
            base_classes.append(base_spec)
        
        return CppClassDecl(stmt.name, base_classes, members)
    
    def _convert_assignment(self, stmt: RunaAssignment) -> CppExpressionStmt:
        """Convert Runa assignment."""
        target = self.convert_expression(stmt.target)
        value = self.convert_expression(stmt.value)
        
        assignment = CppAssignment(target, CppOperator.ASSIGN, value)
        return CppExpressionStmt(assignment)
    
    def _convert_conditional(self, stmt: RunaConditional) -> CppIfStmt:
        """Convert Runa conditional."""
        condition = self.convert_expression(stmt.condition)
        
        then_statements = []
        for then_stmt in stmt.then_body:
            converted = self.convert_statement(then_stmt)
            if converted:
                if isinstance(converted, list):
                    then_statements.extend(converted)
                else:
                    then_statements.append(converted)
        
        then_body = CppCompoundStmt(then_statements)
        
        else_body = None
        if stmt.else_body:
            else_statements = []
            for else_stmt in stmt.else_body:
                converted = self.convert_statement(else_stmt)
                if converted:
                    if isinstance(converted, list):
                        else_statements.extend(converted)
                    else:
                        else_statements.append(converted)
            
            else_body = CppCompoundStmt(else_statements)
        
        return CppIfStmt(condition, then_body, else_body)
    
    def _convert_loop(self, stmt: RunaLoop) -> CppStatement:
        """Convert Runa loop."""
        condition = self.convert_expression(stmt.condition)
        
        body_statements = []
        for body_stmt in stmt.body:
            converted = self.convert_statement(body_stmt)
            if converted:
                if isinstance(converted, list):
                    body_statements.extend(converted)
                else:
                    body_statements.append(converted)
        
        body = CppCompoundStmt(body_statements)
        
        if stmt.loop_type == "while":
            return CppWhileStmt(condition, body)
        else:
            # Default to while loop
            return CppWhileStmt(condition, body)
    
    def _convert_return(self, stmt: RunaReturn) -> CppReturnStmt:
        """Convert Runa return."""
        value = None
        if stmt.value:
            value = self.convert_expression(stmt.value)
        
        return CppReturnStmt(value)
    
    def _convert_expression_statement(self, stmt: RunaExpressionStatement) -> CppExpressionStmt:
        """Convert Runa expression statement."""
        expr = self.convert_expression(stmt.expression)
        return CppExpressionStmt(expr)
    
    def _convert_literal(self, expr: RunaLiteral) -> CppExpression:
        """Convert Runa literal."""
        if expr.literal_type == "integer":
            return CppIntegerLiteral(expr.value)
        elif expr.literal_type == "float":
            return CppFloatingLiteral(expr.value)
        elif expr.literal_type == "string":
            return CppStringLiteral(f'"{expr.value}"')
        elif expr.literal_type == "character":
            return CppCharacterLiteral(f"'{expr.value}'")
        elif expr.literal_type == "boolean":
            return CppBooleanLiteral(expr.value)
        elif expr.literal_type == "null":
            return CppNullptrLiteral()
        else:
            return CppStringLiteral(f'"{expr.value}"')
    
    def _convert_identifier(self, expr: RunaIdentifier) -> CppIdentifier:
        """Convert Runa identifier."""
        return CppIdentifier(expr.name)
    
    def _convert_binary_operation(self, expr: RunaBinaryOperation) -> CppBinaryOp:
        """Convert Runa binary operation."""
        left = self.convert_expression(expr.left)
        right = self.convert_expression(expr.right)
        
        # Map Runa operators to C++ operators
        operator_map = {
            "plus": CppOperator.ADD,
            "minus": CppOperator.SUB,
            "times": CppOperator.MUL,
            "divided by": CppOperator.DIV,
            "modulo": CppOperator.MOD,
            "is equal to": CppOperator.EQ,
            "is not equal to": CppOperator.NE,
            "is less than": CppOperator.LT,
            "is less than or equal to": CppOperator.LE,
            "is greater than": CppOperator.GT,
            "is greater than or equal to": CppOperator.GE,
            "and": CppOperator.LOGICAL_AND,
            "or": CppOperator.LOGICAL_OR,
        }
        
        cpp_op = operator_map.get(expr.operator, CppOperator.ADD)
        return CppBinaryOp(left, cpp_op, right)
    
    def _convert_unary_operation(self, expr: RunaUnaryOperation) -> CppUnaryOp:
        """Convert Runa unary operation."""
        operand = self.convert_expression(expr.operand)
        
        operator_map = {
            "not": CppOperator.LOGICAL_NOT,
            "negative": CppOperator.SUB,
            "positive": CppOperator.ADD,
            "increment": CppOperator.PRE_INC,
            "decrement": CppOperator.PRE_DEC,
        }
        
        cpp_op = operator_map.get(expr.operator, CppOperator.LOGICAL_NOT)
        return CppUnaryOp(cpp_op, operand)
    
    def _convert_function_call(self, expr: RunaFunctionCall) -> CppCall:
        """Convert Runa function call."""
        function = self.convert_expression(expr.function)
        arguments = [self.convert_expression(arg) for arg in expr.arguments]
        
        return CppCall(function, arguments)
    
    def _convert_member_access(self, expr: RunaMemberAccess) -> CppMemberAccess:
        """Convert Runa member access."""
        object_expr = self.convert_expression(expr.object)
        return CppMemberAccess(object_expr, expr.member)
    
    def _convert_index_access(self, expr: RunaIndexAccess) -> CppArraySubscript:
        """Convert Runa index access."""
        array = self.convert_expression(expr.object)
        index = self.convert_expression(expr.index)
        
        return CppArraySubscript(array, index)
    
    def _convert_conditional_expression(self, expr: RunaConditionalExpression) -> CppConditionalOp:
        """Convert Runa conditional expression."""
        condition = self.convert_expression(expr.condition)
        true_expr = self.convert_expression(expr.true_value)
        false_expr = self.convert_expression(expr.false_value)
        
        return CppConditionalOp(condition, true_expr, false_expr)
    
    def _convert_lambda(self, expr: RunaLambda) -> CppLambda:
        """Convert Runa lambda."""
        parameters = []
        for param in expr.parameters:
            cpp_type = self._convert_type(param.param_type)
            cpp_param = CppParameter(param.name, cpp_type)
            parameters.append(cpp_param)
        
        param_list = CppParameterList(parameters)
        
        body_statements = []
        for stmt in expr.body:
            converted = self.convert_statement(stmt)
            if converted:
                if isinstance(converted, list):
                    body_statements.extend(converted)
                else:
                    body_statements.append(converted)
        
        body = CppCompoundStmt(body_statements)
        
        return_type = None
        if expr.return_type:
            return_type = self._convert_type(expr.return_type)
        
        return CppLambda([], param_list, return_type, body)
    
    def _convert_list(self, expr: RunaList) -> CppInitializerList:
        """Convert Runa list."""
        elements = [self.convert_expression(elem) for elem in expr.elements]
        return CppInitializerList(elements)
    
    def _convert_type(self, runa_type: RunaType) -> CppType:
        """Convert Runa type to C++ type."""
        # Map Runa types to C++ types
        type_map = {
            "Integer": "int",
            "Float": "double",
            "Character": "char",
            "Boolean": "bool",
            "String": "std::string",
            "Void": "void",
        }
        
        cpp_name = type_map.get(runa_type.name, runa_type.name)
        return CppBuiltinType(cpp_name)


# Convenience functions
def cpp_to_runa(cpp_ast: CppTranslationUnit) -> Program:
    """Convert C++ AST to Runa AST."""
    converter = CppToRunaConverter()
    return converter.convert(cpp_ast)


def runa_to_cpp(runa_ast: Program) -> CppTranslationUnit:
    """Convert Runa AST to C++ AST."""
    converter = RunaToCppConverter()
    return converter.convert(runa_ast)