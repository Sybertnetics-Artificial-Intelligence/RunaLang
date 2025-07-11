#!/usr/bin/env python3
"""
R ↔ Runa AST Converter

Bidirectional AST conversion between R and Runa with complete semantic mapping
for statistical computing constructs, data structures, and R-specific features.
"""

from typing import List, Optional, Any, Union, Dict
from dataclasses import dataclass

from .r_ast import *
from ....core.runa_ast import (
    ASTNode, NodeType, Expression, Statement, Declaration,
    Identifier, LiteralExpression, BinaryExpression, UnaryExpression,
    FunctionDeclaration, FunctionCall, VariableDeclaration,
    IfStatement, ForLoop, WhileLoop, ReturnStatement,
    Block, Program
)


class RToRunaConverter:
    """Convert R AST to Runa AST."""
    
    def __init__(self):
        self.variable_mappings: Dict[str, str] = {}
        self.function_mappings: Dict[str, str] = {}
    
    def convert(self, r_node: RNode) -> ASTNode:
        """Convert R AST node to Runa AST node."""
        if isinstance(r_node, RProgram):
            return self.convert_program(r_node)
        elif isinstance(r_node, RScript):
            return self.convert_script(r_node)
        elif isinstance(r_node, RFunctionDefinition):
            return self.convert_function_definition(r_node)
        elif isinstance(r_node, RFunctionCall):
            return self.convert_function_call(r_node)
        elif isinstance(r_node, RIdentifier):
            return self.convert_identifier(r_node)
        elif isinstance(r_node, RAssignment):
            return self.convert_assignment(r_node)
        elif isinstance(r_node, RBinaryExpression):
            return self.convert_binary_expression(r_node)
        elif isinstance(r_node, RUnaryExpression):
            return self.convert_unary_expression(r_node)
        elif isinstance(r_node, RNumericLiteral):
            return self.convert_numeric_literal(r_node)
        elif isinstance(r_node, RStringLiteral):
            return self.convert_string_literal(r_node)
        elif isinstance(r_node, RLogicalLiteral):
            return self.convert_logical_literal(r_node)
        elif isinstance(r_node, RNullLiteral):
            return self.convert_null_literal(r_node)
        elif isinstance(r_node, RVector):
            return self.convert_vector(r_node)
        elif isinstance(r_node, RList):
            return self.convert_list(r_node)
        elif isinstance(r_node, RDataFrame):
            return self.convert_data_frame(r_node)
        elif isinstance(r_node, RMatrix):
            return self.convert_matrix(r_node)
        elif isinstance(r_node, RIfStatement):
            return self.convert_if_statement(r_node)
        elif isinstance(r_node, RForLoop):
            return self.convert_for_loop(r_node)
        elif isinstance(r_node, RWhileLoop):
            return self.convert_while_loop(r_node)
        elif isinstance(r_node, RReturnStatement):
            return self.convert_return_statement(r_node)
        elif isinstance(r_node, RIndexExpression):
            return self.convert_index_expression(r_node)
        elif isinstance(r_node, RFormula):
            return self.convert_formula(r_node)
        else:
            # Fallback for unsupported nodes
            return self.create_comment_node(f"# Unsupported R construct: {type(r_node).__name__}")
    
    def convert_program(self, r_program: RProgram) -> Program:
        """Convert R program to Runa program."""
        statements = []
        for stmt in r_program.statements:
            runa_stmt = self.convert(stmt)
            if runa_stmt:
                statements.append(runa_stmt)
        
        return Program(statements=statements)
    
    def convert_script(self, r_script: RScript) -> Program:
        """Convert R script to Runa program."""
        statements = []
        for stmt in r_script.statements:
            runa_stmt = self.convert(stmt)
            if runa_stmt:
                statements.append(runa_stmt)
        
        return Program(statements=statements)
    
    def convert_function_definition(self, r_func: RFunctionDefinition) -> FunctionDeclaration:
        """Convert R function definition to Runa function declaration."""
        # Convert parameters
        parameters = []
        for param in r_func.parameters:
            param_name = param.name
            param_type = "Any"  # R is dynamically typed
            
            # Handle default values
            default_value = None
            if param.default_value:
                default_value = self.convert(param.default_value)
            
            parameters.append({
                'name': param_name,
                'type': param_type,
                'default_value': default_value
            })
        
        # Convert function body
        body_statements = []
        for stmt in r_func.body:
            runa_stmt = self.convert(stmt)
            if runa_stmt:
                body_statements.append(runa_stmt)
        
        body = Block(statements=body_statements)
        
        return FunctionDeclaration(
            name="anonymous_function",
            parameters=parameters,
            return_type="Any",
            body=body
        )
    
    def convert_function_call(self, r_call: RFunctionCall) -> FunctionCall:
        """Convert R function call to Runa function call."""
        function = self.convert(r_call.function)
        
        arguments = []
        for arg in r_call.arguments:
            arg_value = self.convert(arg.value)
            
            # Handle named arguments
            if arg.name:
                arguments.append({
                    'name': arg.name,
                    'value': arg_value
                })
            else:
                arguments.append({
                    'value': arg_value
                })
        
        return FunctionCall(
            function=function,
            arguments=arguments
        )
    
    def convert_identifier(self, r_id: RIdentifier) -> Identifier:
        """Convert R identifier to Runa identifier."""
        # Map R-specific identifiers to Runa equivalents
        name_mappings = {
            'TRUE': 'true',
            'FALSE': 'false',
            'NULL': 'null',
            'c': 'list',  # R's c() function maps to list creation
            'length': 'len',
            'nrow': 'rows',
            'ncol': 'cols'
        }
        
        mapped_name = name_mappings.get(r_id.name, r_id.name)
        return Identifier(name=mapped_name)
    
    def convert_assignment(self, r_assign: RAssignment) -> Statement:
        """Convert R assignment to Runa variable declaration or assignment."""
        target = self.convert(r_assign.target)
        value = self.convert(r_assign.value)
        
        # R assignments can be variable declarations
        if isinstance(target, Identifier):
            return VariableDeclaration(
                name=target.name,
                type="Any",  # R is dynamically typed
                value=value
            )
        else:
            # Complex assignment (e.g., array indexing)
            return Statement(
                type=NodeType.ASSIGNMENT,
                target=target,
                value=value
            )
    
    def convert_binary_expression(self, r_expr: RBinaryExpression) -> BinaryExpression:
        """Convert R binary expression to Runa binary expression."""
        left = self.convert(r_expr.left)
        right = self.convert(r_expr.right)
        
        # Map R operators to Runa operators
        operator_mappings = {
            ROperator.PLUS: '+',
            ROperator.MINUS: '-',
            ROperator.MULTIPLY: '*',
            ROperator.DIVIDE: '/',
            ROperator.POWER: '**',
            ROperator.MODULO: '%',
            ROperator.EQUAL: '==',
            ROperator.NOT_EQUAL: '!=',
            ROperator.LESS_THAN: '<',
            ROperator.LESS_EQUAL: '<=',
            ROperator.GREATER_THAN: '>',
            ROperator.GREATER_EQUAL: '>=',
            ROperator.AND: 'and',
            ROperator.OR: 'or',
            ROperator.IN: 'in'
        }
        
        operator = operator_mappings.get(r_expr.operator, str(r_expr.operator.value))
        
        return BinaryExpression(
            left=left,
            operator=operator,
            right=right
        )
    
    def convert_unary_expression(self, r_expr: RUnaryExpression) -> UnaryExpression:
        """Convert R unary expression to Runa unary expression."""
        expression = self.convert(r_expr.expression)
        
        operator_mappings = {
            ROperator.MINUS: '-',
            ROperator.PLUS: '+',
            ROperator.NOT: 'not'
        }
        
        operator = operator_mappings.get(r_expr.operator, str(r_expr.operator.value))
        
        return UnaryExpression(
            operator=operator,
            expression=expression
        )
    
    def convert_numeric_literal(self, r_num: RNumericLiteral) -> LiteralExpression:
        """Convert R numeric literal to Runa literal."""
        return LiteralExpression(
            value=r_num.value,
            type="number"
        )
    
    def convert_string_literal(self, r_str: RStringLiteral) -> LiteralExpression:
        """Convert R string literal to Runa literal."""
        return LiteralExpression(
            value=r_str.value,
            type="string"
        )
    
    def convert_logical_literal(self, r_bool: RLogicalLiteral) -> LiteralExpression:
        """Convert R logical literal to Runa literal."""
        return LiteralExpression(
            value=r_bool.value,
            type="boolean"
        )
    
    def convert_null_literal(self, r_null: RNullLiteral) -> LiteralExpression:
        """Convert R NULL to Runa null."""
        return LiteralExpression(
            value=None,
            type="null"
        )
    
    def convert_vector(self, r_vec: RVector) -> Expression:
        """Convert R vector to Runa list."""
        elements = []
        for elem in r_vec.elements:
            elements.append(self.convert(elem))
        
        # Use Runa's list creation
        return FunctionCall(
            function=Identifier(name="list"),
            arguments=[{'value': elem} for elem in elements]
        )
    
    def convert_list(self, r_list: RList) -> Expression:
        """Convert R list to Runa dictionary or list."""
        # If all elements have names, create a dictionary
        has_names = all(elem.name for elem in r_list.elements)
        
        if has_names:
            # Create dictionary
            pairs = []
            for elem in r_list.elements:
                key = LiteralExpression(value=elem.name, type="string")
                value = self.convert(elem.value)
                pairs.append((key, value))
            
            return Expression(
                type=NodeType.DICTIONARY,
                pairs=pairs
            )
        else:
            # Create list
            elements = []
            for elem in r_list.elements:
                elements.append(self.convert(elem.value))
            
            return FunctionCall(
                function=Identifier(name="list"),
                arguments=[{'value': elem} for elem in elements]
            )
    
    def convert_data_frame(self, r_df: RDataFrame) -> Expression:
        """Convert R data.frame to Runa structured data."""
        # Create a dictionary representing the data frame
        columns = {}
        for col in r_df.columns:
            col_data = self.convert(col.values)
            columns[col.name] = col_data
        
        return Expression(
            type=NodeType.DICTIONARY,
            value=columns
        )
    
    def convert_matrix(self, r_matrix: RMatrix) -> Expression:
        """Convert R matrix to Runa multidimensional array."""
        data = self.convert(r_matrix.data)
        
        # Create matrix construction call
        return FunctionCall(
            function=Identifier(name="matrix"),
            arguments=[
                {'name': 'data', 'value': data},
                {'name': 'rows', 'value': self.convert(r_matrix.nrow) if r_matrix.nrow else None},
                {'name': 'cols', 'value': self.convert(r_matrix.ncol) if r_matrix.ncol else None}
            ]
        )
    
    def convert_if_statement(self, r_if: RIfStatement) -> IfStatement:
        """Convert R if statement to Runa if statement."""
        condition = self.convert(r_if.condition)
        then_stmt = self.convert(r_if.then_expr)
        else_stmt = self.convert(r_if.else_expr) if r_if.else_expr else None
        
        return IfStatement(
            condition=condition,
            then_statement=then_stmt,
            else_statement=else_stmt
        )
    
    def convert_for_loop(self, r_for: RForLoop) -> ForLoop:
        """Convert R for loop to Runa for loop."""
        variable = r_for.variable
        iterable = self.convert(r_for.iterable)
        body = self.convert(r_for.body)
        
        return ForLoop(
            variable=variable,
            iterable=iterable,
            body=body
        )
    
    def convert_while_loop(self, r_while: RWhileLoop) -> WhileLoop:
        """Convert R while loop to Runa while loop."""
        condition = self.convert(r_while.condition)
        body = self.convert(r_while.body)
        
        return WhileLoop(
            condition=condition,
            body=body
        )
    
    def convert_return_statement(self, r_return: RReturnStatement) -> ReturnStatement:
        """Convert R return statement to Runa return statement."""
        value = self.convert(r_return.value) if r_return.value else None
        
        return ReturnStatement(value=value)
    
    def convert_index_expression(self, r_index: RIndexExpression) -> Expression:
        """Convert R indexing to Runa indexing."""
        object_expr = self.convert(r_index.object)
        
        if len(r_index.indices) == 1:
            index = self.convert(r_index.indices[0])
            return Expression(
                type=NodeType.INDEX_ACCESS,
                object=object_expr,
                index=index
            )
        else:
            # Multiple indices - convert to function call
            indices = [self.convert(idx) for idx in r_index.indices]
            return FunctionCall(
                function=Identifier(name="get_item"),
                arguments=[{'value': object_expr}] + [{'value': idx} for idx in indices]
            )
    
    def convert_formula(self, r_formula: RFormula) -> Expression:
        """Convert R formula to Runa expression."""
        # Formulas are R-specific, represent as a special structure
        left = self.convert(r_formula.left) if r_formula.left else None
        right = self.convert(r_formula.right)
        
        return Expression(
            type=NodeType.FORMULA,
            response=left,
            predictors=right
        )
    
    def create_comment_node(self, text: str) -> Statement:
        """Create a comment statement for unsupported constructs."""
        return Statement(
            type=NodeType.COMMENT,
            text=text
        )


class RunaToRConverter:
    """Convert Runa AST to R AST."""
    
    def __init__(self):
        self.variable_mappings: Dict[str, str] = {}
    
    def convert(self, runa_node: ASTNode) -> RNode:
        """Convert Runa AST node to R AST node."""
        if isinstance(runa_node, Program):
            return self.convert_program(runa_node)
        elif isinstance(runa_node, FunctionDeclaration):
            return self.convert_function_declaration(runa_node)
        elif isinstance(runa_node, FunctionCall):
            return self.convert_function_call(runa_node)
        elif isinstance(runa_node, Identifier):
            return self.convert_identifier(runa_node)
        elif isinstance(runa_node, VariableDeclaration):
            return self.convert_variable_declaration(runa_node)
        elif isinstance(runa_node, BinaryExpression):
            return self.convert_binary_expression(runa_node)
        elif isinstance(runa_node, UnaryExpression):
            return self.convert_unary_expression(runa_node)
        elif isinstance(runa_node, LiteralExpression):
            return self.convert_literal_expression(runa_node)
        elif isinstance(runa_node, IfStatement):
            return self.convert_if_statement(runa_node)
        elif isinstance(runa_node, ForLoop):
            return self.convert_for_loop(runa_node)
        elif isinstance(runa_node, WhileLoop):
            return self.convert_while_loop(runa_node)
        elif isinstance(runa_node, ReturnStatement):
            return self.convert_return_statement(runa_node)
        else:
            # Fallback
            return RComment(text=f"# Unsupported Runa construct: {type(runa_node).__name__}")
    
    def convert_program(self, runa_program: Program) -> RProgram:
        """Convert Runa program to R program."""
        statements = []
        for stmt in runa_program.statements:
            r_stmt = self.convert(stmt)
            if r_stmt:
                statements.append(r_stmt)
        
        return RProgram(statements=statements)
    
    def convert_function_declaration(self, runa_func: FunctionDeclaration) -> RFunctionDefinition:
        """Convert Runa function declaration to R function definition."""
        # Convert parameters
        parameters = []
        for param in runa_func.parameters:
            param_name = param.get('name', 'param')
            default_value = None
            
            if 'default_value' in param and param['default_value']:
                default_value = self.convert(param['default_value'])
            
            parameters.append(RParameter(
                name=param_name,
                default_value=default_value
            ))
        
        # Convert body
        body = []
        if hasattr(runa_func, 'body') and runa_func.body:
            if hasattr(runa_func.body, 'statements'):
                for stmt in runa_func.body.statements:
                    r_stmt = self.convert(stmt)
                    if r_stmt:
                        body.append(r_stmt)
            else:
                r_stmt = self.convert(runa_func.body)
                if r_stmt:
                    body.append(r_stmt)
        
        return RFunctionDefinition(
            parameters=parameters,
            body=body
        )
    
    def convert_function_call(self, runa_call: FunctionCall) -> RFunctionCall:
        """Convert Runa function call to R function call."""
        function = self.convert(runa_call.function)
        
        arguments = []
        for arg in runa_call.arguments:
            if isinstance(arg, dict):
                name = arg.get('name')
                value = self.convert(arg['value'])
                arguments.append(RArgument(name=name, value=value))
            else:
                value = self.convert(arg)
                arguments.append(RArgument(value=value))
        
        return RFunctionCall(
            function=function,
            arguments=arguments
        )
    
    def convert_identifier(self, runa_id: Identifier) -> RIdentifier:
        """Convert Runa identifier to R identifier."""
        # Map Runa identifiers to R equivalents
        name_mappings = {
            'true': 'TRUE',
            'false': 'FALSE',
            'null': 'NULL',
            'list': 'c',
            'len': 'length',
            'rows': 'nrow',
            'cols': 'ncol'
        }
        
        mapped_name = name_mappings.get(runa_id.name, runa_id.name)
        return RIdentifier(name=mapped_name)
    
    def convert_variable_declaration(self, runa_var: VariableDeclaration) -> RAssignment:
        """Convert Runa variable declaration to R assignment."""
        target = RIdentifier(name=runa_var.name)
        value = self.convert(runa_var.value) if runa_var.value else RNullLiteral()
        
        return RAssignment(
            target=target,
            value=value,
            operator=ROperator.ASSIGN
        )
    
    def convert_binary_expression(self, runa_expr: BinaryExpression) -> RBinaryExpression:
        """Convert Runa binary expression to R binary expression."""
        left = self.convert(runa_expr.left)
        right = self.convert(runa_expr.right)
        
        # Map Runa operators to R operators
        operator_mappings = {
            '+': ROperator.PLUS,
            '-': ROperator.MINUS,
            '*': ROperator.MULTIPLY,
            '/': ROperator.DIVIDE,
            '**': ROperator.POWER,
            '%': ROperator.MODULO,
            '==': ROperator.EQUAL,
            '!=': ROperator.NOT_EQUAL,
            '<': ROperator.LESS_THAN,
            '<=': ROperator.LESS_EQUAL,
            '>': ROperator.GREATER_THAN,
            '>=': ROperator.GREATER_EQUAL,
            'and': ROperator.AND,
            'or': ROperator.OR,
            'in': ROperator.IN
        }
        
        operator = operator_mappings.get(runa_expr.operator, ROperator.PLUS)
        
        return RBinaryExpression(
            left=left,
            operator=operator,
            right=right
        )
    
    def convert_unary_expression(self, runa_expr: UnaryExpression) -> RUnaryExpression:
        """Convert Runa unary expression to R unary expression."""
        expression = self.convert(runa_expr.expression)
        
        operator_mappings = {
            '-': ROperator.MINUS,
            '+': ROperator.PLUS,
            'not': ROperator.NOT
        }
        
        operator = operator_mappings.get(runa_expr.operator, ROperator.MINUS)
        
        return RUnaryExpression(
            operator=operator,
            expression=expression
        )
    
    def convert_literal_expression(self, runa_lit: LiteralExpression) -> RNode:
        """Convert Runa literal to R literal."""
        if runa_lit.type == "number":
            is_integer = isinstance(runa_lit.value, int)
            return RNumericLiteral(value=runa_lit.value, is_integer=is_integer)
        elif runa_lit.type == "string":
            return RStringLiteral(value=runa_lit.value)
        elif runa_lit.type == "boolean":
            return RLogicalLiteral(value=runa_lit.value)
        elif runa_lit.type == "null":
            return RNullLiteral()
        else:
            return RStringLiteral(value=str(runa_lit.value))
    
    def convert_if_statement(self, runa_if: IfStatement) -> RIfStatement:
        """Convert Runa if statement to R if statement."""
        condition = self.convert(runa_if.condition)
        then_expr = self.convert(runa_if.then_statement)
        else_expr = self.convert(runa_if.else_statement) if runa_if.else_statement else None
        
        return RIfStatement(
            condition=condition,
            then_expr=then_expr,
            else_expr=else_expr
        )
    
    def convert_for_loop(self, runa_for: ForLoop) -> RForLoop:
        """Convert Runa for loop to R for loop."""
        variable = runa_for.variable
        iterable = self.convert(runa_for.iterable)
        body = self.convert(runa_for.body)
        
        return RForLoop(
            variable=variable,
            iterable=iterable,
            body=body
        )
    
    def convert_while_loop(self, runa_while: WhileLoop) -> RWhileLoop:
        """Convert Runa while loop to R while loop."""
        condition = self.convert(runa_while.condition)
        body = self.convert(runa_while.body)
        
        return RWhileLoop(
            condition=condition,
            body=body
        )
    
    def convert_return_statement(self, runa_return: ReturnStatement) -> RReturnStatement:
        """Convert Runa return statement to R return statement."""
        value = self.convert(runa_return.value) if runa_return.value else None
        
        return RReturnStatement(value=value)


# Convenience functions
def r_to_runa(r_ast: RNode) -> ASTNode:
    """Convert R AST to Runa AST."""
    converter = RToRunaConverter()
    return converter.convert(r_ast)


def runa_to_r(runa_ast: ASTNode) -> RNode:
    """Convert Runa AST to R AST."""
    converter = RunaToRConverter()
    return converter.convert(runa_ast) 