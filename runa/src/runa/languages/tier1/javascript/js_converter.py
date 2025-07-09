#!/usr/bin/env python3
"""
JavaScript ↔ Runa Bidirectional Converter

Converts between JavaScript AST and Runa AST in both directions,
preserving semantics and enabling round-trip translation.
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass

from .js_ast import *
from ....core.runa_ast import *


class JSToRunaConverter:
    """Converts JavaScript AST to Runa AST."""
    
    def __init__(self):
        self.variable_counter = 0
        self.function_counter = 0
        self.scope_stack = []
        self.converted_functions = {}
    
    def convert(self, js_ast: JSProgram) -> Program:
        """Convert JavaScript program to Runa program."""
        statements = []
        
        for stmt in js_ast.body:
            converted = self.convert_statement(stmt)
            if converted:
                if isinstance(converted, list):
                    statements.extend(converted)
                else:
                    statements.append(converted)
        
        return Program(statements)
    
    def convert_statement(self, stmt: JSNode) -> Union[RunaStatement, List[RunaStatement], None]:
        """Convert JavaScript statement to Runa statement."""
        if isinstance(stmt, JSVariableDeclaration):
            return self._convert_variable_declaration(stmt)
        
        elif isinstance(stmt, JSFunctionDeclaration):
            return self._convert_function_declaration(stmt)
        
        elif isinstance(stmt, JSExpressionStatement):
            return self._convert_expression_statement(stmt)
        
        elif isinstance(stmt, JSIfStatement):
            return self._convert_if_statement(stmt)
        
        elif isinstance(stmt, JSWhileStatement):
            return self._convert_while_statement(stmt)
        
        elif isinstance(stmt, JSForStatement):
            return self._convert_for_statement(stmt)
        
        elif isinstance(stmt, JSReturnStatement):
            return self._convert_return_statement(stmt)
        
        elif isinstance(stmt, JSBreakStatement):
            return self._convert_break_statement(stmt)
        
        elif isinstance(stmt, JSContinueStatement):
            return self._convert_continue_statement(stmt)
        
        elif isinstance(stmt, JSThrowStatement):
            return self._convert_throw_statement(stmt)
        
        elif isinstance(stmt, JSTryStatement):
            return self._convert_try_statement(stmt)
        
        elif isinstance(stmt, JSBlockStatement):
            return self._convert_block_statement(stmt)
        
        elif isinstance(stmt, JSEmptyStatement):
            return None  # Skip empty statements
        
        elif isinstance(stmt, JSDebuggerStatement):
            return self._convert_debugger_statement(stmt)
        
        else:
            raise NotImplementedError(f"Statement conversion not implemented for {type(stmt)}")
    
    def convert_expression(self, expr: JSNode) -> RunaExpression:
        """Convert JavaScript expression to Runa expression."""
        if isinstance(expr, JSLiteral):
            return self._convert_literal(expr)
        
        elif isinstance(expr, JSIdentifier):
            return self._convert_identifier(expr)
        
        elif isinstance(expr, JSBinaryExpression):
            return self._convert_binary_expression(expr)
        
        elif isinstance(expr, JSUnaryExpression):
            return self._convert_unary_expression(expr)
        
        elif isinstance(expr, JSUpdateExpression):
            return self._convert_update_expression(expr)
        
        elif isinstance(expr, JSAssignmentExpression):
            return self._convert_assignment_expression(expr)
        
        elif isinstance(expr, JSLogicalExpression):
            return self._convert_logical_expression(expr)
        
        elif isinstance(expr, JSConditionalExpression):
            return self._convert_conditional_expression(expr)
        
        elif isinstance(expr, JSCallExpression):
            return self._convert_call_expression(expr)
        
        elif isinstance(expr, JSMemberExpression):
            return self._convert_member_expression(expr)
        
        elif isinstance(expr, JSNewExpression):
            return self._convert_new_expression(expr)
        
        elif isinstance(expr, JSArrayExpression):
            return self._convert_array_expression(expr)
        
        elif isinstance(expr, JSObjectExpression):
            return self._convert_object_expression(expr)
        
        elif isinstance(expr, JSFunctionExpression):
            return self._convert_function_expression(expr)
        
        elif isinstance(expr, JSArrowFunctionExpression):
            return self._convert_arrow_function_expression(expr)
        
        elif isinstance(expr, JSThisExpression):
            return self._convert_this_expression(expr)
        
        elif isinstance(expr, JSSequenceExpression):
            return self._convert_sequence_expression(expr)
        
        elif isinstance(expr, JSAwaitExpression):
            return self._convert_await_expression(expr)
        
        elif isinstance(expr, JSYieldExpression):
            return self._convert_yield_expression(expr)
        
        elif isinstance(expr, JSTemplateLiteral):
            return self._convert_template_literal(expr)
        
        else:
            raise NotImplementedError(f"Expression conversion not implemented for {type(expr)}")
    
    def _convert_variable_declaration(self, stmt: JSVariableDeclaration) -> List[RunaStatement]:
        """Convert variable declaration to Runa Let statements."""
        statements = []
        
        for declarator in stmt.declarations:
            if isinstance(declarator, JSVariableDeclarator):
                # Convert to Runa "Let" statement
                name = declarator.id.name if isinstance(declarator.id, JSIdentifier) else "temp_var"
                
                if declarator.init:
                    # Let variable_name be initial_value
                    value = self.convert_expression(declarator.init)
                    let_stmt = RunaLet(name, value)
                else:
                    # Let variable_name be undefined
                    let_stmt = RunaLet(name, RunaLiteral(None, "undefined"))
                
                statements.append(let_stmt)
        
        return statements
    
    def _convert_function_declaration(self, stmt: JSFunctionDeclaration) -> RunaProcessDefinition:
        """Convert function declaration to Runa Process definition."""
        func_name = stmt.id.name
        
        # Convert parameters
        params = []
        for param in stmt.params:
            if isinstance(param, JSIdentifier):
                params.append(RunaParameter(param.name, RunaType("Any")))
        
        # Convert body
        body_statements = []
        for body_stmt in stmt.body.body:
            converted = self.convert_statement(body_stmt)
            if converted:
                if isinstance(converted, list):
                    body_statements.extend(converted)
                else:
                    body_statements.append(converted)
        
        return RunaProcessDefinition(
            name=func_name,
            parameters=params,
            return_type=RunaType("Any"),
            body=RunaBlock(body_statements)
        )
    
    def _convert_expression_statement(self, stmt: JSExpressionStatement) -> RunaStatement:
        """Convert expression statement."""
        expr = self.convert_expression(stmt.expression)
        return RunaExpressionStatement(expr)
    
    def _convert_if_statement(self, stmt: JSIfStatement) -> RunaConditional:
        """Convert if statement to Runa conditional."""
        condition = self.convert_expression(stmt.test)
        
        then_stmt = self.convert_statement(stmt.consequent)
        if not isinstance(then_stmt, RunaBlock):
            then_stmt = RunaBlock([then_stmt] if then_stmt else [])
        
        else_stmt = None
        if stmt.alternate:
            else_stmt = self.convert_statement(stmt.alternate)
            if not isinstance(else_stmt, RunaBlock):
                else_stmt = RunaBlock([else_stmt] if else_stmt else [])
        
        return RunaConditional(condition, then_stmt, else_stmt)
    
    def _convert_while_statement(self, stmt: JSWhileStatement) -> RunaWhileLoop:
        """Convert while statement to Runa while loop."""
        condition = self.convert_expression(stmt.test)
        
        body = self.convert_statement(stmt.body)
        if not isinstance(body, RunaBlock):
            body = RunaBlock([body] if body else [])
        
        return RunaWhileLoop(condition, body)
    
    def _convert_for_statement(self, stmt: JSForStatement) -> List[RunaStatement]:
        """Convert for statement to Runa equivalent."""
        statements = []
        
        # Initialize
        if stmt.init:
            init_stmt = self.convert_statement(stmt.init)
            if init_stmt:
                if isinstance(init_stmt, list):
                    statements.extend(init_stmt)
                else:
                    statements.append(init_stmt)
        
        # Create while loop for the main logic
        loop_body = []
        
        # Add the original body
        body_stmt = self.convert_statement(stmt.body)
        if body_stmt:
            if isinstance(body_stmt, list):
                loop_body.extend(body_stmt)
            else:
                loop_body.append(body_stmt)
        
        # Add update expression
        if stmt.update:
            update_stmt = RunaExpressionStatement(self.convert_expression(stmt.update))
            loop_body.append(update_stmt)
        
        # Create condition
        condition = self.convert_expression(stmt.test) if stmt.test else RunaLiteral(True, "true")
        
        # Create while loop
        while_loop = RunaWhileLoop(condition, RunaBlock(loop_body))
        statements.append(while_loop)
        
        return statements
    
    def _convert_return_statement(self, stmt: JSReturnStatement) -> RunaReturn:
        """Convert return statement."""
        value = None
        if stmt.argument:
            value = self.convert_expression(stmt.argument)
        return RunaReturn(value)
    
    def _convert_break_statement(self, stmt: JSBreakStatement) -> RunaBreak:
        """Convert break statement."""
        return RunaBreak()
    
    def _convert_continue_statement(self, stmt: JSContinueStatement) -> RunaContinue:
        """Convert continue statement."""
        return RunaContinue()
    
    def _convert_throw_statement(self, stmt: JSThrowStatement) -> RunaThrow:
        """Convert throw statement."""
        value = self.convert_expression(stmt.argument)
        return RunaThrow(value)
    
    def _convert_try_statement(self, stmt: JSTryStatement) -> RunaTryCatch:
        """Convert try statement."""
        try_block = self.convert_statement(stmt.block)
        if not isinstance(try_block, RunaBlock):
            try_block = RunaBlock([try_block] if try_block else [])
        
        catch_block = None
        catch_param = None
        if stmt.handler:
            catch_block = self.convert_statement(stmt.handler.body)
            if not isinstance(catch_block, RunaBlock):
                catch_block = RunaBlock([catch_block] if catch_block else [])
            
            if stmt.handler.param and isinstance(stmt.handler.param, JSIdentifier):
                catch_param = stmt.handler.param.name
        
        return RunaTryCatch(try_block, catch_block, catch_param)
    
    def _convert_block_statement(self, stmt: JSBlockStatement) -> RunaBlock:
        """Convert block statement."""
        statements = []
        for body_stmt in stmt.body:
            converted = self.convert_statement(body_stmt)
            if converted:
                if isinstance(converted, list):
                    statements.extend(converted)
                else:
                    statements.append(converted)
        
        return RunaBlock(statements)
    
    def _convert_debugger_statement(self, stmt: JSDebuggerStatement) -> RunaExpressionStatement:
        """Convert debugger statement to comment."""
        return RunaExpressionStatement(RunaLiteral("debugger", "debugger"))
    
    def _convert_literal(self, expr: JSLiteral) -> RunaLiteral:
        """Convert literal expression."""
        if expr.literal_type == JSLiteralType.NULL:
            return RunaLiteral(None, "null")
        elif expr.literal_type == JSLiteralType.BOOLEAN:
            return RunaLiteral(expr.value, "true" if expr.value else "false")
        elif expr.literal_type == JSLiteralType.NUMBER:
            return RunaLiteral(expr.value, str(expr.value))
        elif expr.literal_type == JSLiteralType.STRING:
            return RunaLiteral(expr.value, f'"{expr.value}"')
        elif expr.literal_type == JSLiteralType.REGEX:
            return RunaLiteral(expr.value, expr.raw)
        elif expr.literal_type == JSLiteralType.BIGINT:
            return RunaLiteral(expr.value, str(expr.value))
        else:
            return RunaLiteral(expr.value, expr.raw)
    
    def _convert_identifier(self, expr: JSIdentifier) -> RunaIdentifier:
        """Convert identifier expression."""
        return RunaIdentifier(expr.name)
    
    def _convert_binary_expression(self, expr: JSBinaryExpression) -> RunaBinaryOperation:
        """Convert binary expression."""
        left = self.convert_expression(expr.left)
        right = self.convert_expression(expr.right)
        
        # Map JavaScript operators to Runa operators
        operator_map = {
            JSOperator.PLUS: "plus",
            JSOperator.MINUS: "minus",
            JSOperator.MULTIPLY: "times",
            JSOperator.DIVIDE: "divided by",
            JSOperator.MODULO: "modulo",
            JSOperator.EQUAL: "is equal to",
            JSOperator.NOT_EQUAL: "is not equal to",
            JSOperator.STRICT_EQUAL: "is equal to",
            JSOperator.STRICT_NOT_EQUAL: "is not equal to",
            JSOperator.LESS_THAN: "is less than",
            JSOperator.LESS_EQUAL: "is less than or equal to",
            JSOperator.GREATER_THAN: "is greater than",
            JSOperator.GREATER_EQUAL: "is greater than or equal to",
            JSOperator.AND: "and",
            JSOperator.OR: "or",
            JSOperator.BITWISE_AND: "bitwise and",
            JSOperator.BITWISE_OR: "bitwise or",
            JSOperator.BITWISE_XOR: "bitwise xor",
            JSOperator.LEFT_SHIFT: "left shift",
            JSOperator.RIGHT_SHIFT: "right shift",
            JSOperator.UNSIGNED_RIGHT_SHIFT: "unsigned right shift",
            JSOperator.IN: "in",
            JSOperator.INSTANCEOF: "instanceof",
        }
        
        operator = operator_map.get(expr.operator, str(expr.operator.value))
        return RunaBinaryOperation(left, operator, right)
    
    def _convert_unary_expression(self, expr: JSUnaryExpression) -> RunaUnaryOperation:
        """Convert unary expression."""
        operand = self.convert_expression(expr.argument)
        
        operator_map = {
            JSOperator.NOT: "not",
            JSOperator.UNARY_MINUS: "negative",
            JSOperator.UNARY_PLUS: "positive",
            JSOperator.TYPEOF: "typeof",
            JSOperator.VOID: "void",
            JSOperator.DELETE: "delete",
            JSOperator.BITWISE_NOT: "bitwise not",
        }
        
        operator = operator_map.get(expr.operator, str(expr.operator.value))
        return RunaUnaryOperation(operator, operand)
    
    def _convert_update_expression(self, expr: JSUpdateExpression) -> RunaAssignment:
        """Convert update expression to assignment."""
        target = self.convert_expression(expr.argument)
        
        if expr.operator == JSOperator.INCREMENT:
            # Convert x++ to x = x + 1
            new_value = RunaBinaryOperation(target, "plus", RunaLiteral(1, "1"))
        else:  # DECREMENT
            # Convert x-- to x = x - 1
            new_value = RunaBinaryOperation(target, "minus", RunaLiteral(1, "1"))
        
        return RunaAssignment(target, new_value)
    
    def _convert_assignment_expression(self, expr: JSAssignmentExpression) -> RunaAssignment:
        """Convert assignment expression."""
        target = self.convert_expression(expr.left)
        value = self.convert_expression(expr.right)
        
        if expr.operator == JSOperator.ASSIGN:
            return RunaAssignment(target, value)
        else:
            # Convert compound assignment (e.g., x += 1 to x = x + 1)
            operator_map = {
                JSOperator.PLUS_ASSIGN: "plus",
                JSOperator.MINUS_ASSIGN: "minus",
                JSOperator.MULTIPLY_ASSIGN: "times",
                JSOperator.DIVIDE_ASSIGN: "divided by",
                JSOperator.MODULO_ASSIGN: "modulo",
            }
            
            if expr.operator in operator_map:
                binary_op = RunaBinaryOperation(target, operator_map[expr.operator], value)
                return RunaAssignment(target, binary_op)
            else:
                return RunaAssignment(target, value)
    
    def _convert_logical_expression(self, expr: JSLogicalExpression) -> RunaBinaryOperation:
        """Convert logical expression."""
        left = self.convert_expression(expr.left)
        right = self.convert_expression(expr.right)
        
        operator_map = {
            JSOperator.AND: "and",
            JSOperator.OR: "or",
            JSOperator.NULLISH_COALESCING: "or",  # Simplified
        }
        
        operator = operator_map.get(expr.operator, str(expr.operator.value))
        return RunaBinaryOperation(left, operator, right)
    
    def _convert_conditional_expression(self, expr: JSConditionalExpression) -> RunaConditionalExpression:
        """Convert conditional expression."""
        test = self.convert_expression(expr.test)
        consequent = self.convert_expression(expr.consequent)
        alternate = self.convert_expression(expr.alternate)
        
        return RunaConditionalExpression(test, consequent, alternate)
    
    def _convert_call_expression(self, expr: JSCallExpression) -> RunaFunctionCall:
        """Convert call expression."""
        callee = self.convert_expression(expr.callee)
        
        args = []
        for arg in expr.arguments:
            args.append(self.convert_expression(arg))
        
        # Convert to Runa function call syntax
        if isinstance(callee, RunaIdentifier):
            return RunaFunctionCall(callee.name, args)
        elif isinstance(callee, RunaMemberAccess):
            # Method call
            return RunaMethodCall(callee.object, callee.member, args)
        else:
            # Complex callee - create temporary function name
            temp_name = f"_temp_func_{self.function_counter}"
            self.function_counter += 1
            return RunaFunctionCall(temp_name, args)
    
    def _convert_member_expression(self, expr: JSMemberExpression) -> RunaMemberAccess:
        """Convert member expression."""
        object_expr = self.convert_expression(expr.object)
        
        if expr.computed:
            # obj[prop] - computed property access
            property_expr = self.convert_expression(expr.property)
            return RunaArrayAccess(object_expr, property_expr)
        else:
            # obj.prop - property access
            if isinstance(expr.property, JSIdentifier):
                return RunaMemberAccess(object_expr, expr.property.name)
            else:
                return RunaMemberAccess(object_expr, "property")
    
    def _convert_new_expression(self, expr: JSNewExpression) -> RunaObjectCreation:
        """Convert new expression."""
        constructor = self.convert_expression(expr.callee)
        
        args = []
        for arg in expr.arguments:
            args.append(self.convert_expression(arg))
        
        # Convert to Runa object creation
        if isinstance(constructor, RunaIdentifier):
            return RunaObjectCreation(constructor.name, args)
        else:
            return RunaObjectCreation("Object", args)
    
    def _convert_array_expression(self, expr: JSArrayExpression) -> RunaArrayLiteral:
        """Convert array expression."""
        elements = []
        for element in expr.elements:
            if element is None:
                elements.append(RunaLiteral(None, "undefined"))
            else:
                elements.append(self.convert_expression(element))
        
        return RunaArrayLiteral(elements)
    
    def _convert_object_expression(self, expr: JSObjectExpression) -> RunaObjectLiteral:
        """Convert object expression."""
        properties = []
        
        for prop in expr.properties:
            if isinstance(prop, JSProperty):
                key = prop.key.name if isinstance(prop.key, JSIdentifier) else str(prop.key)
                value = self.convert_expression(prop.value)
                properties.append(RunaObjectProperty(key, value))
        
        return RunaObjectLiteral(properties)
    
    def _convert_function_expression(self, expr: JSFunctionExpression) -> RunaLambda:
        """Convert function expression to lambda."""
        params = []
        for param in expr.params:
            if isinstance(param, JSIdentifier):
                params.append(RunaParameter(
                    name=param.name,
                    type=RunaType("Any")
                ))
        
        body_statements = []
        for stmt in expr.body.body:
            converted = self.convert_statement(stmt)
            if converted:
                if isinstance(converted, list):
                    body_statements.extend(converted)
                else:
                    body_statements.append(converted)
        
        return RunaLambda(params, RunaBlock(body_statements))
    
    def _convert_arrow_function_expression(self, expr: JSArrowFunctionExpression) -> RunaLambda:
        """Convert arrow function expression to lambda."""
        params = []
        for param in expr.params:
            if isinstance(param, JSIdentifier):
                params.append(RunaParameter(
                    name=param.name,
                    type=RunaType("Any")
                ))
        
        if expr.expression:
            # Single expression body
            body_expr = self.convert_expression(expr.body)
            body = RunaBlock([RunaReturn(body_expr)])
        else:
            # Block body
            body_statements = []
            for stmt in expr.body.body:
                converted = self.convert_statement(stmt)
                if converted:
                    if isinstance(converted, list):
                        body_statements.extend(converted)
                    else:
                        body_statements.append(converted)
            body = RunaBlock(body_statements)
        
        return RunaLambda(params, body)
    
    def _convert_this_expression(self, expr: JSThisExpression) -> RunaIdentifier:
        """Convert this expression."""
        return RunaIdentifier("this")
    
    def _convert_sequence_expression(self, expr: JSSequenceExpression) -> RunaSequence:
        """Convert sequence expression."""
        expressions = []
        for sub_expr in expr.expressions:
            expressions.append(self.convert_expression(sub_expr))
        
        return RunaSequence(expressions)
    
    def _convert_await_expression(self, expr: JSAwaitExpression) -> RunaAwait:
        """Convert await expression."""
        argument = self.convert_expression(expr.argument)
        return RunaAwait(argument)
    
    def _convert_yield_expression(self, expr: JSYieldExpression) -> RunaYield:
        """Convert yield expression."""
        argument = None
        if expr.argument:
            argument = self.convert_expression(expr.argument)
        return RunaYield(argument)
    
    def _convert_template_literal(self, expr: JSTemplateLiteral) -> RunaStringInterpolation:
        """Convert template literal."""
        parts = []
        
        for i, quasi in enumerate(expr.quasis):
            # Add the string part
            parts.append(self.convert_expression(quasi))
            
            # Add the expression part if exists
            if i < len(expr.expressions):
                parts.append(self.convert_expression(expr.expressions[i]))
        
        return RunaStringInterpolation(parts)


class RunaToJSConverter:
    """Converts Runa AST to JavaScript AST."""
    
    def __init__(self):
        self.variable_counter = 0
        self.function_counter = 0
    
    def convert(self, runa_ast: Program) -> JSProgram:
        """Convert Runa program to JavaScript program."""
        statements = []
        
        for stmt in runa_ast.statements:
            converted = self.convert_statement(stmt)
            if converted:
                if isinstance(converted, list):
                    statements.extend(converted)
                else:
                    statements.append(converted)
        
        return JSProgram(statements, "module")
    
    def convert_statement(self, stmt: RunaStatement) -> Union[JSNode, List[JSNode], None]:
        """Convert Runa statement to JavaScript statement."""
        if isinstance(stmt, RunaLet):
            return self._convert_let_statement(stmt)
        
        elif isinstance(stmt, RunaProcessDefinition):
            return self._convert_process_definition(stmt)
        
        elif isinstance(stmt, RunaConditional):
            return self._convert_conditional(stmt)
        
        elif isinstance(stmt, RunaWhileLoop):
            return self._convert_while_loop(stmt)
        
        elif isinstance(stmt, RunaForLoop):
            return self._convert_for_loop(stmt)
        
        elif isinstance(stmt, RunaReturn):
            return self._convert_return(stmt)
        
        elif isinstance(stmt, RunaBreak):
            return JSBreakStatement()
        
        elif isinstance(stmt, RunaContinue):
            return JSContinueStatement()
        
        elif isinstance(stmt, RunaThrow):
            return self._convert_throw(stmt)
        
        elif isinstance(stmt, RunaTryCatch):
            return self._convert_try_catch(stmt)
        
        elif isinstance(stmt, RunaExpressionStatement):
            return self._convert_expression_statement(stmt)
        
        elif isinstance(stmt, RunaAssignment):
            return self._convert_assignment(stmt)
        
        elif isinstance(stmt, RunaBlock):
            return self._convert_block(stmt)
        
        else:
            raise NotImplementedError(f"Statement conversion not implemented for {type(stmt)}")
    
    def convert_expression(self, expr: RunaExpression) -> JSNode:
        """Convert Runa expression to JavaScript expression."""
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
        
        elif isinstance(expr, RunaMethodCall):
            return self._convert_method_call(expr)
        
        elif isinstance(expr, RunaMemberAccess):
            return self._convert_member_access(expr)
        
        elif isinstance(expr, RunaArrayAccess):
            return self._convert_array_access(expr)
        
        elif isinstance(expr, RunaArrayLiteral):
            return self._convert_array_literal(expr)
        
        elif isinstance(expr, RunaObjectLiteral):
            return self._convert_object_literal(expr)
        
        elif isinstance(expr, RunaObjectCreation):
            return self._convert_object_creation(expr)
        
        elif isinstance(expr, RunaLambda):
            return self._convert_lambda(expr)
        
        elif isinstance(expr, RunaConditionalExpression):
            return self._convert_conditional_expression(expr)
        
        elif isinstance(expr, RunaSequence):
            return self._convert_sequence(expr)
        
        elif isinstance(expr, RunaAwait):
            return self._convert_await(expr)
        
        elif isinstance(expr, RunaYield):
            return self._convert_yield(expr)
        
        elif isinstance(expr, RunaStringInterpolation):
            return self._convert_string_interpolation(expr)
        
        else:
            raise NotImplementedError(f"Expression conversion not implemented for {type(expr)}")
    
    def _convert_let_statement(self, stmt: RunaLet) -> JSVariableDeclaration:
        """Convert Let statement to variable declaration."""
        id = JSIdentifier(stmt.name)
        init = self.convert_expression(stmt.value) if stmt.value else None
        declarator = JSVariableDeclarator(id, init)
        
        return JSVariableDeclaration([declarator], JSVariableKind.LET)
    
    def _convert_process_definition(self, stmt: RunaProcessDefinition) -> JSFunctionDeclaration:
        """Convert Process definition to function declaration."""
        id = JSIdentifier(stmt.name)
        
        params = []
        for param in stmt.parameters:
            params.append(JSIdentifier(param.name))
        
        body_statements = []
        for body_stmt in stmt.body.statements:
            converted = self.convert_statement(body_stmt)
            if converted:
                if isinstance(converted, list):
                    body_statements.extend(converted)
                else:
                    body_statements.append(converted)
        
        body = JSBlockStatement(body_statements)
        
        return JSFunctionDeclaration(id, params, body)
    
    def _convert_conditional(self, stmt: RunaConditional) -> JSIfStatement:
        """Convert conditional to if statement."""
        test = self.convert_expression(stmt.condition)
        
        consequent = self.convert_statement(stmt.then_branch)
        if not isinstance(consequent, JSBlockStatement):
            consequent = JSBlockStatement([consequent] if consequent else [])
        
        alternate = None
        if stmt.else_branch:
            alternate = self.convert_statement(stmt.else_branch)
            if not isinstance(alternate, JSBlockStatement):
                alternate = JSBlockStatement([alternate] if alternate else [])
        
        return JSIfStatement(test, consequent, alternate)
    
    def _convert_while_loop(self, stmt: RunaWhileLoop) -> JSWhileStatement:
        """Convert while loop to while statement."""
        test = self.convert_expression(stmt.condition)
        
        body = self.convert_statement(stmt.body)
        if not isinstance(body, JSBlockStatement):
            body = JSBlockStatement([body] if body else [])
        
        return JSWhileStatement(test, body)
    
    def _convert_for_loop(self, stmt: RunaForLoop) -> JSForStatement:
        """Convert for loop to for statement."""
        # This is a simplified conversion
        # Would need more sophisticated handling for different for loop types
        init = None
        if hasattr(stmt, 'init') and stmt.init:
            init = self.convert_statement(stmt.init)
        
        test = self.convert_expression(stmt.condition)
        
        update = None
        if hasattr(stmt, 'update') and stmt.update:
            update = self.convert_expression(stmt.update)
        
        body = self.convert_statement(stmt.body)
        if not isinstance(body, JSBlockStatement):
            body = JSBlockStatement([body] if body else [])
        
        return JSForStatement(init, test, update, body)
    
    def _convert_return(self, stmt: RunaReturn) -> JSReturnStatement:
        """Convert return statement."""
        argument = None
        if stmt.value:
            argument = self.convert_expression(stmt.value)
        
        return JSReturnStatement(argument)
    
    def _convert_throw(self, stmt: RunaThrow) -> JSThrowStatement:
        """Convert throw statement."""
        argument = self.convert_expression(stmt.value)
        return JSThrowStatement(argument)
    
    def _convert_try_catch(self, stmt: RunaTryCatch) -> JSTryStatement:
        """Convert try-catch statement."""
        block = self.convert_statement(stmt.try_block)
        if not isinstance(block, JSBlockStatement):
            block = JSBlockStatement([block] if block else [])
        
        handler = None
        if stmt.catch_block:
            param = JSIdentifier(stmt.catch_parameter) if stmt.catch_parameter else None
            catch_body = self.convert_statement(stmt.catch_block)
            if not isinstance(catch_body, JSBlockStatement):
                catch_body = JSBlockStatement([catch_body] if catch_body else [])
            
            handler = JSCatchClause(param, catch_body)
        
        return JSTryStatement(block, handler)
    
    def _convert_expression_statement(self, stmt: RunaExpressionStatement) -> JSExpressionStatement:
        """Convert expression statement."""
        expr = self.convert_expression(stmt.expression)
        return JSExpressionStatement(expr)
    
    def _convert_assignment(self, stmt: RunaAssignment) -> JSExpressionStatement:
        """Convert assignment to expression statement."""
        left = self.convert_expression(stmt.target)
        right = self.convert_expression(stmt.value)
        
        assignment = JSAssignmentExpression(left, JSOperator.ASSIGN, right)
        return JSExpressionStatement(assignment)
    
    def _convert_block(self, stmt: RunaBlock) -> JSBlockStatement:
        """Convert block statement."""
        statements = []
        for sub_stmt in stmt.statements:
            converted = self.convert_statement(sub_stmt)
            if converted:
                if isinstance(converted, list):
                    statements.extend(converted)
                else:
                    statements.append(converted)
        
        return JSBlockStatement(statements)
    
    def _convert_literal(self, expr: RunaLiteral) -> JSLiteral:
        """Convert literal expression."""
        if expr.value is None:
            return JSLiteral(None, "null", JSLiteralType.NULL)
        elif isinstance(expr.value, bool):
            return JSLiteral(expr.value, str(expr.value).lower(), JSLiteralType.BOOLEAN)
        elif isinstance(expr.value, (int, float)):
            return JSLiteral(expr.value, str(expr.value), JSLiteralType.NUMBER)
        elif isinstance(expr.value, str):
            return JSLiteral(expr.value, f'"{expr.value}"', JSLiteralType.STRING)
        else:
            return JSLiteral(expr.value, str(expr.value), JSLiteralType.STRING)
    
    def _convert_identifier(self, expr: RunaIdentifier) -> JSIdentifier:
        """Convert identifier expression."""
        return JSIdentifier(expr.name)
    
    def _convert_binary_operation(self, expr: RunaBinaryOperation) -> JSBinaryExpression:
        """Convert binary operation."""
        left = self.convert_expression(expr.left)
        right = self.convert_expression(expr.right)
        
        # Map Runa operators to JavaScript operators
        operator_map = {
            "plus": JSOperator.PLUS,
            "minus": JSOperator.MINUS,
            "times": JSOperator.MULTIPLY,
            "divided by": JSOperator.DIVIDE,
            "modulo": JSOperator.MODULO,
            "is equal to": JSOperator.STRICT_EQUAL,
            "is not equal to": JSOperator.STRICT_NOT_EQUAL,
            "is less than": JSOperator.LESS_THAN,
            "is less than or equal to": JSOperator.LESS_EQUAL,
            "is greater than": JSOperator.GREATER_THAN,
            "is greater than or equal to": JSOperator.GREATER_EQUAL,
            "and": JSOperator.AND,
            "or": JSOperator.OR,
            "bitwise and": JSOperator.BITWISE_AND,
            "bitwise or": JSOperator.BITWISE_OR,
            "bitwise xor": JSOperator.BITWISE_XOR,
            "left shift": JSOperator.LEFT_SHIFT,
            "right shift": JSOperator.RIGHT_SHIFT,
            "unsigned right shift": JSOperator.UNSIGNED_RIGHT_SHIFT,
            "in": JSOperator.IN,
            "instanceof": JSOperator.INSTANCEOF,
        }
        
        js_operator = operator_map.get(expr.operator, JSOperator.PLUS)
        
        # Use appropriate expression type based on operator
        if js_operator in [JSOperator.AND, JSOperator.OR]:
            return JSLogicalExpression(left, js_operator, right)
        else:
            return JSBinaryExpression(left, js_operator, right)
    
    def _convert_unary_operation(self, expr: RunaUnaryOperation) -> JSUnaryExpression:
        """Convert unary operation."""
        operand = self.convert_expression(expr.operand)
        
        operator_map = {
            "not": JSOperator.NOT,
            "negative": JSOperator.UNARY_MINUS,
            "positive": JSOperator.UNARY_PLUS,
            "typeof": JSOperator.TYPEOF,
            "void": JSOperator.VOID,
            "delete": JSOperator.DELETE,
            "bitwise not": JSOperator.BITWISE_NOT,
        }
        
        js_operator = operator_map.get(expr.operator, JSOperator.NOT)
        return JSUnaryExpression(js_operator, operand)
    
    def _convert_function_call(self, expr: RunaFunctionCall) -> JSCallExpression:
        """Convert function call."""
        callee = JSIdentifier(expr.function_name)
        
        arguments = []
        for arg in expr.arguments:
            arguments.append(self.convert_expression(arg))
        
        return JSCallExpression(callee, arguments)
    
    def _convert_method_call(self, expr: RunaMethodCall) -> JSCallExpression:
        """Convert method call."""
        object_expr = self.convert_expression(expr.object)
        callee = JSMemberExpression(object_expr, JSIdentifier(expr.method), computed=False)
        
        arguments = []
        for arg in expr.arguments:
            arguments.append(self.convert_expression(arg))
        
        return JSCallExpression(callee, arguments)
    
    def _convert_member_access(self, expr: RunaMemberAccess) -> JSMemberExpression:
        """Convert member access."""
        object_expr = self.convert_expression(expr.object)
        property = JSIdentifier(expr.member)
        
        return JSMemberExpression(object_expr, property, computed=False)
    
    def _convert_array_access(self, expr: RunaArrayAccess) -> JSMemberExpression:
        """Convert array access."""
        object_expr = self.convert_expression(expr.array)
        index_expr = self.convert_expression(expr.index)
        
        return JSMemberExpression(object_expr, index_expr, computed=True)
    
    def _convert_array_literal(self, expr: RunaArrayLiteral) -> JSArrayExpression:
        """Convert array literal."""
        elements = []
        for element in expr.elements:
            elements.append(self.convert_expression(element))
        
        return JSArrayExpression(elements)
    
    def _convert_object_literal(self, expr: RunaObjectLiteral) -> JSObjectExpression:
        """Convert object literal."""
        properties = []
        
        for prop in expr.properties:
            key = JSIdentifier(prop.key)
            value = self.convert_expression(prop.value)
            properties.append(JSProperty(key, value, JSPropertyKind.INIT))
        
        return JSObjectExpression(properties)
    
    def _convert_object_creation(self, expr: RunaObjectCreation) -> JSNewExpression:
        """Convert object creation."""
        callee = JSIdentifier(expr.class_name)
        
        arguments = []
        for arg in expr.arguments:
            arguments.append(self.convert_expression(arg))
        
        return JSNewExpression(callee, arguments)
    
    def _convert_lambda(self, expr: RunaLambda) -> JSArrowFunctionExpression:
        """Convert lambda to arrow function."""
        params = []
        for param in expr.parameters:
            if isinstance(param, RunaParameter):
                params.append(JSIdentifier(param.name))
            else:
                params.append(JSIdentifier(str(param)))
        
        body_statements = []
        for stmt in expr.body.statements:
            converted = self.convert_statement(stmt)
            if converted:
                if isinstance(converted, list):
                    body_statements.extend(converted)
                else:
                    body_statements.append(converted)
        
        body = JSBlockStatement(body_statements)
        
        return JSArrowFunctionExpression(params, body)
    
    def _convert_conditional_expression(self, expr: RunaConditionalExpression) -> JSConditionalExpression:
        """Convert conditional expression."""
        test = self.convert_expression(expr.condition)
        consequent = self.convert_expression(expr.then_value)
        alternate = self.convert_expression(expr.else_value)
        
        return JSConditionalExpression(test, consequent, alternate)
    
    def _convert_sequence(self, expr: RunaSequence) -> JSSequenceExpression:
        """Convert sequence expression."""
        expressions = []
        for sub_expr in expr.expressions:
            expressions.append(self.convert_expression(sub_expr))
        
        return JSSequenceExpression(expressions)
    
    def _convert_await(self, expr: RunaAwait) -> JSAwaitExpression:
        """Convert await expression."""
        argument = self.convert_expression(expr.expression)
        return JSAwaitExpression(argument)
    
    def _convert_yield(self, expr: RunaYield) -> JSYieldExpression:
        """Convert yield expression."""
        argument = None
        if expr.value:
            argument = self.convert_expression(expr.value)
        
        return JSYieldExpression(argument)
    
    def _convert_string_interpolation(self, expr: RunaStringInterpolation) -> JSTemplateLiteral:
        """Convert string interpolation to template literal."""
        # Simplified conversion - would need more sophisticated handling
        quasis = []
        expressions = []
        
        for i, part in enumerate(expr.parts):
            if i % 2 == 0:
                # String part
                quasis.append(self.convert_expression(part))
            else:
                # Expression part
                expressions.append(self.convert_expression(part))
        
        return JSTemplateLiteral(quasis, expressions)


def js_to_runa(js_ast: JSProgram) -> Program:
    """Convert JavaScript AST to Runa AST."""
    converter = JSToRunaConverter()
    return converter.convert(js_ast)


def runa_to_js(runa_ast: Program) -> JSProgram:
    """Convert Runa AST to JavaScript AST."""
    converter = RunaToJSConverter()
    return converter.convert(runa_ast)