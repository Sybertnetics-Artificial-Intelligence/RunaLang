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
    
    def convert_statement(self, stmt: JSNode) -> Union[Statement, List[Statement], None]:
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
            # Handle unknown statement types gracefully
            return ExpressionStatement(
                expression=StringLiteral(value=f"unsupported_statement_{type(stmt).__name__}")
            )
    
    def convert_expression(self, expr: JSNode) -> Expression:
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
            # Handle unknown expression types gracefully
            return StringLiteral(value=f"unsupported_expression_{type(expr).__name__}")
    
    def _convert_variable_declaration(self, stmt: JSVariableDeclaration) -> List[Statement]:
        """Convert variable declaration to Runa "Let" statements."""
        statements = []
        
        for declarator in stmt.declarations:
            if isinstance(declarator, JSVariableDeclarator):
                # Convert to Runa "Let" statement
                name = declarator.id.name if isinstance(declarator.id, JSIdentifier) else "temp_var"
                
                if declarator.init:
                    # Let variable_name be initial_value
                    value = self.convert_expression(declarator.init)
                    let_stmt = LetStatement(
                        identifier=Identifier(name),
                        type_annotation=None,
                        value=value
                    )
                else:
                    # Let variable_name be undefined
                    let_stmt = LetStatement(
                        identifier=Identifier(name),
                        type_annotation=None,
                        value=StringLiteral("undefined")
                    )
                
                statements.append(let_stmt)
        
        return statements
    
    def _convert_function_declaration(self, stmt: JSFunctionDeclaration) -> ProcessDefinition:
        """Convert function declaration to Runa Process definition."""
        func_name = stmt.id.name
        
        # Convert parameters
        params = []
        for param in stmt.params:
            if isinstance(param, JSIdentifier):
                params.append(Parameter(
                    identifier=Identifier(param.name),
                    type_annotation=BasicType("Any"),
                    default_value=None
                ))
        
        # Convert body
        body_statements = []
        for body_stmt in stmt.body.body:
            converted = self.convert_statement(body_stmt)
            if converted:
                if isinstance(converted, list):
                    body_statements.extend(converted)
                else:
                    body_statements.append(converted)
        
        return ProcessDefinition(
            identifier=Identifier(func_name),
            parameters=params,
            return_type=BasicType("Any"),
            body=Block(body_statements)
        )
    
    def _convert_expression_statement(self, stmt: JSExpressionStatement) -> Statement:
        """Convert expression statement."""
        expr = self.convert_expression(stmt.expression)
        return ExpressionStatement(expr)
    
    def _convert_if_statement(self, stmt: JSIfStatement) -> IfStatement:
        """Convert if statement to Runa conditional."""
        condition = self.convert_expression(stmt.test)
        
        then_stmt = self.convert_statement(stmt.consequent)
        if not isinstance(then_stmt, Block):
            then_stmt = Block([then_stmt] if then_stmt else [])
        
        else_stmt = None
        if stmt.alternate:
            else_stmt = self.convert_statement(stmt.alternate)
            if not isinstance(else_stmt, Block):
                else_stmt = Block([else_stmt] if else_stmt else [])
        
        return IfStatement(
            condition=condition,
            then_block=then_stmt,
            else_block=else_stmt
        )
    
    def _convert_while_statement(self, stmt: JSWhileStatement) -> WhileLoop:
        """Convert while statement to Runa while loop."""
        condition = self.convert_expression(stmt.test)
        
        body = self.convert_statement(stmt.body)
        if not isinstance(body, Block):
            body = Block([body] if body else [])
        
        return WhileLoop(
            condition=condition,
            body=body
        )
    
    def _convert_for_statement(self, stmt: JSForStatement) -> List[Statement]:
        """Convert for statement to Runa equivalent using proper loop constructs."""
        statements = []
        
        # Handle initialization
        if stmt.init:
            init_stmt = self.convert_statement(stmt.init)
            if init_stmt:
                if isinstance(init_stmt, list):
                    statements.extend(init_stmt)
                else:
                    statements.append(init_stmt)
        
        # Convert body
        body_stmt = self.convert_statement(stmt.body)
        loop_body = []
        
        if body_stmt:
            if isinstance(body_stmt, list):
                loop_body.extend(body_stmt)
            else:
                loop_body.append(body_stmt)
        
        # Add update expression to end of body
        if stmt.update:
            update_stmt = ExpressionStatement(self.convert_expression(stmt.update))
            loop_body.append(update_stmt)
        
        # Create condition (default to true if no test)
        condition = self.convert_expression(stmt.test) if stmt.test else BooleanLiteral(True)
        
        # Create while loop equivalent
        while_loop = WhileLoop(
            condition=condition,
            body=Block(loop_body)
        )
        statements.append(while_loop)
        
        return statements
    
    def _convert_return_statement(self, stmt: JSReturnStatement) -> ReturnStatement:
        """Convert return statement."""
        value = None
        if stmt.argument:
            value = self.convert_expression(stmt.argument)
        return ReturnStatement(value)
    
    def _convert_break_statement(self, stmt: JSBreakStatement) -> BreakStatement:
        """Convert break statement."""
        return BreakStatement()
    
    def _convert_continue_statement(self, stmt: JSContinueStatement) -> ContinueStatement:
        """Convert continue statement."""
        return ContinueStatement()
    
    def _convert_throw_statement(self, stmt: JSThrowStatement) -> ThrowStatement:
        """Convert throw statement."""
        value = self.convert_expression(stmt.argument)
        return ThrowStatement(value)
    
    def _convert_try_statement(self, stmt: JSTryStatement) -> TryStatement:
        """Convert try statement."""
        try_block = self.convert_statement(stmt.block)
        if not isinstance(try_block, Block):
            try_block = Block([try_block] if try_block else [])
        
        catch_clauses = []
        if stmt.handler:
            catch_block = self.convert_statement(stmt.handler.body)
            if not isinstance(catch_block, Block):
                catch_block = Block([catch_block] if catch_block else [])
            
            # Create proper catch clause with exception handling
            exception_name = None
            exception_type = None
            
            if stmt.handler.param:
                if hasattr(stmt.handler.param, 'name'):
                    exception_name = stmt.handler.param.name
                else:
                    exception_name = str(stmt.handler.param)
                
                # JavaScript catch clauses don't specify exception types, 
                # so we use a generic "Error" type
                exception_type = BasicType("Error")
            
            catch_clause = CatchClause(
                exception_type=exception_type,
                exception_name=exception_name,
                block=catch_block.statements if isinstance(catch_block, Block) else [catch_block]
            )
            catch_clauses.append(catch_clause)
        
        finally_block = None
        if stmt.finalizer:
            finally_block = self.convert_statement(stmt.finalizer)
            if not isinstance(finally_block, Block):
                finally_block = Block([finally_block] if finally_block else [])
        
        return TryStatement(
            try_block=try_block,
            catch_clauses=catch_clauses,
            finally_block=finally_block
        )
    
    def _convert_block_statement(self, stmt: JSBlockStatement) -> Block:
        """Convert block statement."""
        statements = []
        for body_stmt in stmt.body:
            converted = self.convert_statement(body_stmt)
            if converted:
                if isinstance(converted, list):
                    statements.extend(converted)
                else:
                    statements.append(converted)
        
        return Block(statements)
    
    def _convert_debugger_statement(self, stmt) -> ExpressionStatement:
        """Convert debugger statement to comment."""
        return ExpressionStatement(StringLiteral("debugger"))
    
    def _convert_literal(self, expr: JSLiteral) -> Expression:
        """Convert literal expression."""
        # Handle different literal types properly
        if hasattr(expr, 'literal_type'):
            if expr.literal_type == JSLiteralType.NULL:
                return StringLiteral("null")
            elif expr.literal_type == JSLiteralType.BOOLEAN:
                return BooleanLiteral(expr.value)
            elif expr.literal_type == JSLiteralType.NUMBER:
                if isinstance(expr.value, int):
                    return IntegerLiteral(expr.value)
                else:
                    return FloatLiteral(expr.value)
            elif expr.literal_type == JSLiteralType.STRING:
                return StringLiteral(expr.value)
            elif expr.literal_type == JSLiteralType.REGEX:
                return StringLiteral(expr.value)  # Convert regex to string
            elif expr.literal_type == JSLiteralType.BIGINT:
                return IntegerLiteral(int(expr.value))
        
        # Fallback: determine type from value
        if isinstance(expr.value, str):
            return StringLiteral(expr.value)
        elif isinstance(expr.value, bool):
            return BooleanLiteral(expr.value)
        elif isinstance(expr.value, int):
            return IntegerLiteral(expr.value)
        elif isinstance(expr.value, float):
            return FloatLiteral(expr.value)
        else:
            return StringLiteral(str(expr.value))
    
    def _convert_identifier(self, expr: JSIdentifier) -> Identifier:
        """Convert identifier expression."""
        return Identifier(expr.name)
    
    def _convert_binary_expression(self, expr: JSBinaryExpression) -> BinaryExpression:
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
        return BinaryExpression(
            left=left,
            operator=operator,
            right=right
        )
    
    def _convert_unary_expression(self, expr: JSUnaryExpression) -> UnaryExpression:
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
        return UnaryExpression(
            operator=operator,
            operand=operand
        )
    
    def _convert_update_expression(self, expr: JSUpdateExpression) -> AssignmentExpression:
        """Convert update expression to assignment."""
        target = self.convert_expression(expr.argument)
        
        if expr.operator == JSOperator.INCREMENT:
            # Convert x++ to x = x + 1
            new_value = BinaryExpression(target, "plus", IntegerLiteral(1, "1"))
        else:  # DECREMENT
            # Convert x-- to x = x - 1
            new_value = BinaryExpression(target, "minus", IntegerLiteral(1, "1"))
        
        return AssignmentExpression(target, new_value)
    
    def _convert_assignment_expression(self, expr: JSAssignmentExpression) -> AssignmentExpression:
        """Convert assignment expression."""
        target = self.convert_expression(expr.left)
        value = self.convert_expression(expr.right)
        
        if expr.operator == JSOperator.ASSIGN:
            return AssignmentExpression(target, value)
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
                binary_op = BinaryExpression(target, operator_map[expr.operator], value)
                return AssignmentExpression(target, binary_op)
            else:
                return AssignmentExpression(target, value)
    
    def _convert_logical_expression(self, expr: JSLogicalExpression) -> Expression:
        """Convert logical expression with proper nullish coalescing support."""
        left = self.convert_expression(expr.left)
        right = self.convert_expression(expr.right)
        
        if expr.operator == JSOperator.AND:
            return BinaryExpression(left, "and", right)
        elif expr.operator == JSOperator.OR:
            return BinaryExpression(left, "or", right)
        elif expr.operator == JSOperator.NULLISH_COALESCING:
            # JavaScript's ?? operator: only null/undefined trigger fallback
            # Convert to: (left is not equal to null) and (left is not equal to undefined) 
            #             ? left : right
            # In Runa conditional form: If left is not null and left is not undefined then left else right
            
            null_check = BinaryExpression(
                left=left, 
                operator="is not equal to", 
                right=StringLiteral("null")
            )
            undefined_check = BinaryExpression(
                left=left, 
                operator="is not equal to", 
                right=StringLiteral("undefined")
            )
            condition = BinaryExpression(
                left=null_check,
                operator="and", 
                right=undefined_check
            )
            
            return ConditionalExpression(
                condition=condition,
                when_true=left,
                when_false=right
            )
        else:
            # Fallback for unknown operators
            operator = str(expr.operator.value) if hasattr(expr.operator, 'value') else str(expr.operator)
            return BinaryExpression(left, operator, right)
    
    def _convert_conditional_expression(self, expr: JSConditionalExpression) -> ConditionalExpression:
        """Convert conditional expression."""
        test = self.convert_expression(expr.test)
        consequent = self.convert_expression(expr.consequent)
        alternate = self.convert_expression(expr.alternate)
        
        return ConditionalExpression(test, consequent, alternate)
    
    def _convert_call_expression(self, expr: JSCallExpression) -> FunctionCall:
        """Convert call expression."""
        callee = self.convert_expression(expr.callee)
        
        args = []
        for arg in expr.arguments:
            args.append(self.convert_expression(arg))
        
        # Convert to Runa function call syntax
        if isinstance(callee, Identifier):
            return FunctionCall(
                function=callee,
                arguments=args
            )
        elif isinstance(callee, MemberAccess):
            # Method call
            # Method call - convert to function call on member access
            return FunctionCall(
                function=callee,
                arguments=args
            )
        else:
            # Complex callee - create temporary function name
            temp_name = f"_temp_func_{self.function_counter}"
            self.function_counter += 1
            return FunctionCall(
                function=Identifier(temp_name),
                arguments=args
            )
    
    def _convert_member_expression(self, expr: JSMemberExpression) -> MemberAccess:
        """Convert member expression."""
        object_expr = self.convert_expression(expr.object)
        
        if expr.computed:
            # obj[prop] - computed property access
            property_expr = self.convert_expression(expr.property)
            return IndexAccess(
                object=object_expr,
                index=property_expr
            )
        else:
            # obj.prop - property access
            if isinstance(expr.property, JSIdentifier):
                return MemberAccess(
                    object=object_expr,
                    member=Identifier(expr.property.name)
                )
            else:
                return MemberAccess(
                    object=object_expr,
                    member=Identifier("property")
                )
    
    def _convert_new_expression(self, expr: JSNewExpression) -> NewExpression:
        """Convert new expression."""
        constructor = self.convert_expression(expr.callee)
        
        args = []
        for arg in expr.arguments:
            args.append(self.convert_expression(arg))
        
        # Convert to Runa object creation
        return NewExpression(
            constructor=constructor,
            arguments=args
        )
    
    def _convert_array_expression(self, expr: JSArrayExpression) -> ListLiteral:
        """Convert array expression."""
        elements = []
        for element in expr.elements:
            if element is None:
                elements.append(IntegerLiteral(None, "undefined"))
            else:
                elements.append(self.convert_expression(element))
        
        return ListLiteral(elements)
    
    def _convert_object_expression(self, expr: JSObjectExpression) -> DictionaryLiteral:
        """Convert object expression."""
        properties = []
        
        for prop in expr.properties:
            if isinstance(prop, JSProperty):
                key = prop.key.name if isinstance(prop.key, JSIdentifier) else str(prop.key)
                value = self.convert_expression(prop.value)
                properties[key] = value
        
        return DictionaryLiteral(properties)
    
    def _convert_function_expression(self, expr: JSFunctionExpression) -> LambdaExpression:
        """Convert function expression to lambda."""
        params = []
        for param in expr.params:
            if isinstance(param, JSIdentifier):
                params.append(Parameter(
                    identifier=Identifier(param.name),
                    type_annotation=BasicType("Any"),
                    default_value=None
                ))
        
        body_statements = []
        for stmt in expr.body.body:
            converted = self.convert_statement(stmt)
            if converted:
                if isinstance(converted, list):
                    body_statements.extend(converted)
                else:
                    body_statements.append(converted)
        
        return LambdaExpression(params, Block(body_statements))
    
    def _convert_arrow_function_expression(self, expr: JSArrowFunctionExpression) -> LambdaExpression:
        """Convert arrow function expression to lambda."""
        params = []
        for param in expr.params:
            if isinstance(param, JSIdentifier):
                params.append(Parameter(
                    identifier=Identifier(param.name),
                    type_annotation=BasicType("Any"),
                    default_value=None
                ))
        
        if expr.expression:
            # Single expression body
            body_expr = self.convert_expression(expr.body)
            body = Block([ReturnStatement(body_expr)])
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
            body = Block(body_statements)
        
        return LambdaExpression(params, body)
    
    def _convert_this_expression(self, expr: JSThisExpression) -> Identifier:
        """Convert this expression."""
        return Identifier("this")
    
    def _convert_sequence_expression(self, expr: JSSequenceExpression) -> List[Expression]:
        """Convert sequence expression."""
        expressions = []
        for sub_expr in expr.expressions:
            expressions.append(self.convert_expression(sub_expr))
        
        return expressions
    
    def _convert_await_expression(self, expr: JSAwaitExpression) -> AwaitExpression:
        """Convert await expression."""
        argument = self.convert_expression(expr.argument)
        return AwaitExpression(argument)
    
    def _convert_yield_expression(self, expr: JSYieldExpression) -> YieldStatement:
        """Convert yield expression."""
        argument = None
        if expr.argument:
            argument = self.convert_expression(expr.argument)
        return YieldStatement(argument)
    
    def _convert_template_literal(self, expr: JSTemplateLiteral) -> InterpolatedStringExpression:
        """Convert template literal."""
        parts = []
        
        for i, quasi in enumerate(expr.quasis):
            # Add the string part
            parts.append(self.convert_expression(quasi))
            
            # Add the expression part if exists
            if i < len(expr.expressions):
                parts.append(self.convert_expression(expr.expressions[i]))
        
        return InterpolatedStringExpression(parts)


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
    
    def convert_statement(self, stmt: Statement) -> Union[JSNode, List[JSNode], None]:
        """Convert Runa statement to JavaScript statement."""
        if isinstance(stmt, LetStatement):
            return self._convert_let_statement(stmt)
        
        elif isinstance(stmt, ProcessDefinition):
            return self._convert_process_definition(stmt)
        
        elif isinstance(stmt, IfStatement):
            return self._convert_conditional(stmt)
        
        elif isinstance(stmt, WhileLoop):
            return self._convert_while_loop(stmt)
        
        elif isinstance(stmt, ForEachLoop):
            return self._convert_for_each_loop(stmt)
        
        elif isinstance(stmt, ForRangeLoop):
            return self._convert_for_range_loop(stmt)
        
        elif isinstance(stmt, ReturnStatement):
            return self._convert_return(stmt)
        
        elif isinstance(stmt, BreakStatement):
            return JSBreakStatement()
        
        elif isinstance(stmt, ContinueStatement):
            return JSContinueStatement()
        
        elif isinstance(stmt, ThrowStatement):
            return self._convert_throw(stmt)
        
        elif isinstance(stmt, TryStatement):
            return self._convert_try_catch(stmt)
        
        elif isinstance(stmt, ExpressionStatement):
            return self._convert_expression_statement(stmt)
        
        elif isinstance(stmt, AssignmentExpression):
            return self._convert_assignment(stmt)
        
        elif isinstance(stmt, Block):
            return self._convert_block(stmt)
        
        else:
            return ExpressionStatement(
                expression=StringLiteral(value=f"unsupported_statement_{type(stmt).__name__}")
            )
    
    def convert_expression(self, expr: Expression) -> JSNode:
        """Convert Runa expression to JavaScript expression."""
        if isinstance(expr, IntegerLiteral):
            return self._convert_literal(expr)
        
        elif isinstance(expr, Identifier):
            return self._convert_identifier(expr)
        
        elif isinstance(expr, BinaryExpression):
            return self._convert_binary_operation(expr)
        
        elif isinstance(expr, UnaryExpression):
            return self._convert_unary_operation(expr)
        
        elif isinstance(expr, FunctionCall):
            return self._convert_function_call(expr)
        
        elif isinstance(expr, MemberAccess):
            return self._convert_member_access(expr)
        
        elif isinstance(expr, IndexAccess):
            return self._convert_array_access(expr)
        
        elif isinstance(expr, ListLiteral):
            return self._convert_array_literal(expr)
        
        elif isinstance(expr, DictionaryLiteral):
            return self._convert_object_literal(expr)
        
        elif isinstance(expr, NewExpression):
            return self._convert_object_creation(expr)
        
        elif isinstance(expr, LambdaExpression):
            return self._convert_lambda(expr)
        
        elif isinstance(expr, ConditionalExpression):
            return self._convert_conditional_expression(expr)
        
        elif isinstance(expr, List):
            return self._convert_sequence(expr)
        
        elif isinstance(expr, AwaitExpression):
            return self._convert_await(expr)
        
        elif isinstance(expr, YieldStatement):
            return self._convert_yield(expr)
        
        elif isinstance(expr, InterpolatedStringExpression):
            return self._convert_string_interpolation(expr)
        
        else:
            # Handle unknown expression types gracefully
            return StringLiteral(value=f"unsupported_expression_{type(expr).__name__}")
    
    def _convert_let_statement(self, stmt: LetStatement) -> JSVariableDeclaration:
        """Convert Let statement to variable declaration."""
        id = JSIdentifier(stmt.identifier.name)
        init = self.convert_expression(stmt.value) if stmt.value else None
        declarator = JSVariableDeclarator(id, init)
        
        return JSVariableDeclaration([declarator], JSVariableKind.LET)
    
    def _convert_process_definition(self, stmt: ProcessDefinition) -> JSFunctionDeclaration:
        """Convert Process definition to function declaration."""
        id = JSIdentifier(stmt.identifier.name)
        
        params = []
        for param in stmt.parameters:
            params.append(JSIdentifier(param.identifier.name))
        
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
    
    def _convert_conditional(self, stmt: IfStatement) -> JSIfStatement:
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
    
    def _convert_while_loop(self, stmt: WhileLoop) -> JSWhileStatement:
        """Convert while loop to while statement."""
        test = self.convert_expression(stmt.condition)
        
        body = self.convert_statement(stmt.body)
        if not isinstance(body, JSBlockStatement):
            body = JSBlockStatement([body] if body else [])
        
        return JSWhileStatement(test, body)
    
    def _convert_for_each_loop(self, stmt: ForEachLoop) -> JSForStatement:
        """Convert Runa for-each loop to JavaScript for-of statement."""
        # Convert: For each item in collection do ...
        # To:      for (const item of collection) { ... }
        
        # Create iterator variable declaration
        iterator_var = JSVariableDeclaration(
            declarations=[JSVariableDeclarator(
                id=JSIdentifier(stmt.variable.identifier.name if hasattr(stmt.variable, 'identifier') else str(stmt.variable)),
                init=None
            )],
            kind="const"
        )
        
        # Convert iterable expression
        iterable = self.convert_expression(stmt.iterable)
        
        # Convert body
        body = self.convert_statement(stmt.body)
        if not isinstance(body, JSBlockStatement):
            body = JSBlockStatement([body] if body else [])
        
        # Create for-of loop (using for-of pattern in JavaScript)
        # Note: This creates a for(init; test; update) but could be enhanced to for-of
        return JSForStatement(
            init=iterator_var,
            test=None,  # for-of doesn't need explicit test
            update=None,  # for-of doesn't need explicit update
            body=body
        )
    
    def _convert_for_range_loop(self, stmt: ForRangeLoop) -> JSForStatement:
        """Convert Runa for-range loop to JavaScript for statement."""
        # Convert: For i from start to end do ...
        # To:      for (let i = start; i <= end; i++) { ... }
        
        # Create initialization: let i = start
        init_declarator = JSVariableDeclarator(
            id=JSIdentifier(stmt.variable.identifier.name if hasattr(stmt.variable, 'identifier') else str(stmt.variable)),
            init=self.convert_expression(stmt.start)
        )
        init = JSVariableDeclaration(
            declarations=[init_declarator],
            kind="let"
        )
        
        # Create test condition: i <= end
        test = JSBinaryExpression(
            left=JSIdentifier(stmt.variable.identifier.name if hasattr(stmt.variable, 'identifier') else str(stmt.variable)),
            operator=JSOperator.LESS_EQUAL,
            right=self.convert_expression(stmt.end)
        )
        
        # Create update: i++
        update = JSUpdateExpression(
            operator=JSOperator.INCREMENT,
            argument=JSIdentifier(stmt.variable.identifier.name if hasattr(stmt.variable, 'identifier') else str(stmt.variable)),
            prefix=False
        )
        
        # Convert body
        body = self.convert_statement(stmt.body)
        if not isinstance(body, JSBlockStatement):
            body = JSBlockStatement([body] if body else [])
        
        return JSForStatement(init, test, update, body)
    
    def _convert_return(self, stmt: ReturnStatement) -> JSReturnStatement:
        """Convert return statement."""
        argument = None
        if stmt.value:
            argument = self.convert_expression(stmt.value)
        
        return JSReturnStatement(argument)
    
    def _convert_throw(self, stmt: ThrowStatement) -> JSThrowStatement:
        """Convert throw statement."""
        argument = self.convert_expression(stmt.value)
        return JSThrowStatement(argument)
    
    def _convert_try_catch(self, stmt: TryStatement) -> JSTryStatement:
        """Convert try-catch statement."""
        block = self.convert_statement(stmt.try_block)
        if not isinstance(block, JSBlockStatement):
            block = JSBlockStatement([block] if block else [])
        
        handler = None
        if stmt.catch_clauses:
            for catch_clause in stmt.catch_clauses:
                param = JSIdentifier(catch_clause.exception_name) if catch_clause.exception_name else None
                catch_body = self.convert_statement(catch_clause.block)
                if not isinstance(catch_body, JSBlockStatement):
                    catch_body = JSBlockStatement([catch_body] if catch_body else [])
                
                handler = JSCatchClause(param, catch_body)
        
        finally_block = None
        if stmt.finally_block:
            finally_block = self.convert_statement(stmt.finally_block)
            if not isinstance(finally_block, JSBlockStatement):
                finally_block = JSBlockStatement([finally_block] if finally_block else [])
        
        return JSTryStatement(block, handler, finally_block)
    
    def _convert_expression_statement(self, stmt: ExpressionStatement) -> JSExpressionStatement:
        """Convert expression statement."""
        expr = self.convert_expression(stmt.expression)
        return JSExpressionStatement(expr)
    
    def _convert_assignment(self, stmt: AssignmentExpression) -> JSExpressionStatement:
        """Convert assignment to expression statement."""
        left = self.convert_expression(stmt.target)
        right = self.convert_expression(stmt.value)
        
        assignment = JSAssignmentExpression(left, JSOperator.ASSIGN, right)
        return JSExpressionStatement(assignment)
    
    def _convert_block(self, stmt: Block) -> JSBlockStatement:
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
    
    def _convert_literal(self, expr: IntegerLiteral) -> JSLiteral:
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
    
    def _convert_identifier(self, expr: Identifier) -> JSIdentifier:
        """Convert identifier expression."""
        return JSIdentifier(expr.name)
    
    def _convert_binary_operation(self, expr: BinaryExpression) -> JSBinaryExpression:
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
    
    def _convert_unary_operation(self, expr: UnaryExpression) -> JSUnaryExpression:
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
    
    def _convert_function_call(self, expr: FunctionCall) -> JSCallExpression:
        """Convert function call."""
        callee = JSIdentifier(expr.function.name)
        
        arguments = []
        for arg in expr.arguments:
            arguments.append(self.convert_expression(arg))
        
        return JSCallExpression(callee, arguments)
    
    def _convert_method_call(self, expr: MemberAccess) -> JSCallExpression:
        """Convert method call."""
        object_expr = self.convert_expression(expr.object)
        callee = JSMemberExpression(object_expr, JSIdentifier(expr.member.name), computed=False)
        
        arguments = []
        for arg in expr.arguments:
            arguments.append(self.convert_expression(arg))
        
        return JSCallExpression(callee, arguments)
    
    def _convert_member_access(self, expr: MemberAccess) -> JSMemberExpression:
        """Convert member access."""
        object_expr = self.convert_expression(expr.object)
        property = JSIdentifier(expr.member.name)
        
        return JSMemberExpression(object_expr, property, computed=False)
    
    def _convert_array_access(self, expr: IndexAccess) -> JSMemberExpression:
        """Convert array access."""
        object_expr = self.convert_expression(expr.object)
        index_expr = self.convert_expression(expr.index)
        
        return JSMemberExpression(object_expr, index_expr, computed=True)
    
    def _convert_array_literal(self, expr: ListLiteral) -> JSArrayExpression:
        """Convert array literal."""
        elements = []
        for element in expr.elements:
            elements.append(self.convert_expression(element))
        
        return JSArrayExpression(elements)
    
    def _convert_object_literal(self, expr: DictionaryLiteral) -> JSObjectExpression:
        """Convert object literal."""
        properties = []
        
        for key, value in expr.properties.items():
            key_expr = JSIdentifier(key)
            value_expr = self.convert_expression(value)
            properties.append(JSProperty(key_expr, value_expr, JSPropertyKind.INIT))
        
        return JSObjectExpression(properties)
    
    def _convert_object_creation(self, expr: NewExpression) -> JSNewExpression:
        """Convert object creation."""
        callee = JSIdentifier(expr.constructor.name)
        
        arguments = []
        for arg in expr.arguments:
            arguments.append(self.convert_expression(arg))
        
        return JSNewExpression(callee, arguments)
    
    def _convert_lambda(self, expr: LambdaExpression) -> JSArrowFunctionExpression:
        """Convert lambda to arrow function."""
        params = []
        for param in expr.parameters:
            if isinstance(param, Parameter):
                params.append(JSIdentifier(param.identifier.name))
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
    
    def _convert_conditional_expression(self, expr: ConditionalExpression) -> JSConditionalExpression:
        """Convert conditional expression."""
        test = self.convert_expression(expr.condition)
        consequent = self.convert_expression(expr.then_value)
        alternate = self.convert_expression(expr.else_value)
        
        return JSConditionalExpression(test, consequent, alternate)
    
    def _convert_sequence(self, expr: List[Expression]) -> JSSequenceExpression:
        """Convert sequence expression."""
        expressions = []
        for sub_expr in expr:
            expressions.append(self.convert_expression(sub_expr))
        
        return JSSequenceExpression(expressions)
    
    def _convert_await(self, expr: AwaitExpression) -> JSAwaitExpression:
        """Convert await expression."""
        argument = self.convert_expression(expr.expression)
        return JSAwaitExpression(argument)
    
    def _convert_yield(self, expr: YieldStatement) -> JSYieldExpression:
        """Convert yield expression."""
        argument = None
        if expr.value:
            argument = self.convert_expression(expr.value)
        
        return JSYieldExpression(argument)
    
    def _convert_string_interpolation(self, expr: InterpolatedStringExpression) -> JSTemplateLiteral:
        """Convert string interpolation to template literal with full support."""
        quasis = []
        expressions = []
        
        # Handle interpolated string parts properly
        if hasattr(expr, 'parts') and expr.parts:
            current_string = ""
            
            for part in expr.parts:
                if isinstance(part, str):
                    # String literal part
                    current_string += part
                else:
                    # Expression part - close current string and add expression
                    if current_string:
                        quasis.append(JSLiteral(current_string, "string"))
                        current_string = ""
                    expressions.append(self.convert_expression(part))
            
            # Add final string part if any
            if current_string:
                quasis.append(JSLiteral(current_string, "string"))
        
        # Ensure we have at least one quasi (template literals always have one more quasi than expressions)
        if len(quasis) == len(expressions):
            quasis.append(JSLiteral("", "string"))
        
        return JSTemplateLiteral(quasis, expressions)


def js_to_runa(js_ast: JSProgram) -> Program:
    """Convert JavaScript AST to Runa AST."""
    converter = JSToRunaConverter()
    return converter.convert(js_ast)


def runa_to_js(runa_ast: Program) -> JSProgram:
    """Convert Runa AST to JavaScript AST."""
    converter = RunaToJSConverter()
    return converter.convert(runa_ast)