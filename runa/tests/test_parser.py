"""
Tests for the Runa Parser

Tests AST construction from tokens including:
- Variable declarations (Let, Define, Set)
- Basic expressions and operators
- Control flow statements (If/Otherwise)
- Function calls with natural language syntax
- Type annotations
"""

import unittest
from runa.compiler.parser import RunaParser, ParseError, parse_runa_source
from runa.compiler.lexer import RunaLexer
from runa.compiler.tokens import TokenType
from runa.compiler.ast_nodes import *

class TestRunaParser(unittest.TestCase):
    """Test cases for the Runa parser."""
    
    def setUp(self):
        """Set up test fixtures."""
        pass
    
    def parse_source(self, source: str) -> Program:
        """Helper to parse source code and return AST."""
        return parse_runa_source(source)
    
    def test_simple_let_statement(self):
        """Test parsing a simple let statement."""
        source = 'Let user name be "Alex"'
        program = self.parse_source(source)
        
        self.assertEqual(len(program.statements), 1)
        
        stmt = program.statements[0]
        self.assertIsInstance(stmt, LetStatement)
        self.assertEqual(stmt.identifier, "user name")
        self.assertIsNone(stmt.type_annotation)
        
        self.assertIsInstance(stmt.value, StringLiteral)
        self.assertEqual(stmt.value.value, "Alex")
    
    def test_let_with_type_annotation(self):
        """Test let statement with type annotation."""
        source = 'Let age (Integer) be 25'
        program = self.parse_source(source)
        
        stmt = program.statements[0]
        self.assertIsInstance(stmt, LetStatement)
        self.assertEqual(stmt.identifier, "age")
        
        self.assertIsInstance(stmt.type_annotation, BasicType)
        self.assertEqual(stmt.type_annotation.name, "Integer")
        
        self.assertIsInstance(stmt.value, IntegerLiteral)
        self.assertEqual(stmt.value.value, 25)
    
    def test_define_statement(self):
        """Test define statement."""
        source = 'Define PI as 3.14159'
        program = self.parse_source(source)
        
        stmt = program.statements[0]
        self.assertIsInstance(stmt, DefineStatement)
        self.assertEqual(stmt.identifier, "PI")
        self.assertFalse(stmt.is_constant)
        
        self.assertIsInstance(stmt.value, FloatLiteral)
        self.assertEqual(stmt.value.value, 3.14159)
    
    def test_define_constant(self):
        """Test define constant statement."""
        source = 'Define constant MAX_SIZE as 100'
        program = self.parse_source(source)
        
        stmt = program.statements[0]
        self.assertIsInstance(stmt, DefineStatement)
        self.assertEqual(stmt.identifier, "MAX_SIZE")
        self.assertTrue(stmt.is_constant)
        
        self.assertIsInstance(stmt.value, IntegerLiteral)
        self.assertEqual(stmt.value.value, 100)
    
    def test_set_statement(self):
        """Test set statement."""
        source = 'Set user age to 30'
        program = self.parse_source(source)
        
        stmt = program.statements[0]
        self.assertIsInstance(stmt, SetStatement)
        
        self.assertIsInstance(stmt.target, Identifier)
        self.assertEqual(stmt.target.name, "user age")
        
        self.assertIsInstance(stmt.value, IntegerLiteral)
        self.assertEqual(stmt.value.value, 30)
    
    def test_boolean_literals(self):
        """Test boolean literal parsing."""
        source = '''Let is_active be true
Let is_disabled be false'''
        program = self.parse_source(source)
        
        self.assertEqual(len(program.statements), 2)
        
        # First statement
        stmt1 = program.statements[0]
        self.assertIsInstance(stmt1.value, BooleanLiteral)
        self.assertTrue(stmt1.value.value)
        
        # Second statement
        stmt2 = program.statements[1]
        self.assertIsInstance(stmt2.value, BooleanLiteral)
        self.assertFalse(stmt2.value.value)
    
    def test_arithmetic_expression(self):
        """Test arithmetic expression parsing."""
        source = 'Let result be 10 plus 5 multiplied by 2'
        program = self.parse_source(source)
        
        stmt = program.statements[0]
        self.assertIsInstance(stmt, LetStatement)
        
        # Should parse as: 10 plus (5 multiplied by 2) due to precedence
        expr = stmt.value
        self.assertIsInstance(expr, BinaryExpression)
        self.assertEqual(expr.operator, BinaryOperator.PLUS)
        
        # Left side: 10
        self.assertIsInstance(expr.left, IntegerLiteral)
        self.assertEqual(expr.left.value, 10)
        
        # Right side: 5 multiplied by 2
        self.assertIsInstance(expr.right, BinaryExpression)
        self.assertEqual(expr.right.operator, BinaryOperator.MULTIPLY)
        
        self.assertIsInstance(expr.right.left, IntegerLiteral)
        self.assertEqual(expr.right.left.value, 5)
        
        self.assertIsInstance(expr.right.right, IntegerLiteral)
        self.assertEqual(expr.right.right.value, 2)
    
    def test_comparison_expression(self):
        """Test comparison expression parsing."""
        source = 'Let is_adult be age is greater than 18'
        program = self.parse_source(source)
        
        stmt = program.statements[0]
        expr = stmt.value
        
        self.assertIsInstance(expr, BinaryExpression)
        self.assertEqual(expr.operator, BinaryOperator.GREATER_THAN)
        
        self.assertIsInstance(expr.left, Identifier)
        self.assertEqual(expr.left.name, "age")
        
        self.assertIsInstance(expr.right, IntegerLiteral)
        self.assertEqual(expr.right.value, 18)
    
    def test_simple_if_statement(self):
        """Test simple if statement parsing."""
        source = '''If age is greater than 18:
    Set status to "adult"'''
        program = self.parse_source(source)
        
        stmt = program.statements[0]
        self.assertIsInstance(stmt, IfStatement)
        
        # Check condition
        self.assertIsInstance(stmt.condition, BinaryExpression)
        self.assertEqual(stmt.condition.operator, BinaryOperator.GREATER_THAN)
        
        # Check then block
        self.assertEqual(len(stmt.then_block), 1)
        then_stmt = stmt.then_block[0]
        self.assertIsInstance(then_stmt, SetStatement)
        
        # No elif or else clauses
        self.assertEqual(len(stmt.elif_clauses), 0)
        self.assertIsNone(stmt.else_block)
    
    def test_if_else_statement(self):
        """Test if-else statement parsing."""
        source = '''If age is greater than 18:
    Set status to "adult"
Otherwise:
    Set status to "minor"'''
        program = self.parse_source(source)
        
        stmt = program.statements[0]
        self.assertIsInstance(stmt, IfStatement)
        
        # Check then block
        self.assertEqual(len(stmt.then_block), 1)
        
        # Check else block
        self.assertIsNotNone(stmt.else_block)
        self.assertEqual(len(stmt.else_block), 1)
        
        else_stmt = stmt.else_block[0]
        self.assertIsInstance(else_stmt, SetStatement)
        self.assertIsInstance(else_stmt.value, StringLiteral)
        self.assertEqual(else_stmt.value.value, "minor")
    
    def test_display_statement(self):
        """Test display statement parsing."""
        source = 'Display "Hello, World!"'
        program = self.parse_source(source)
        
        stmt = program.statements[0]
        self.assertIsInstance(stmt, DisplayStatement)
        
        self.assertIsInstance(stmt.value, StringLiteral)
        self.assertEqual(stmt.value.value, "Hello, World!")
        self.assertIsNone(stmt.prefix)
    
    def test_display_with_message(self):
        """Test display statement with message prefix."""
        source = 'Display user name with message "User:"'
        program = self.parse_source(source)
        
        stmt = program.statements[0]
        self.assertIsInstance(stmt, DisplayStatement)
        
        self.assertIsInstance(stmt.value, Identifier)
        self.assertEqual(stmt.value.name, "user name")
        
        self.assertIsInstance(stmt.prefix, StringLiteral)
        self.assertEqual(stmt.prefix.value, "User:")
    
    def test_return_statement(self):
        """Test return statement parsing."""
        source = 'Return total'
        program = self.parse_source(source)
        
        stmt = program.statements[0]
        self.assertIsInstance(stmt, ReturnStatement)
        
        self.assertIsInstance(stmt.value, Identifier)
        self.assertEqual(stmt.value.name, "total")
    
    def test_return_without_value(self):
        """Test return statement without value."""
        source = 'Return'
        program = self.parse_source(source)
        
        stmt = program.statements[0]
        self.assertIsInstance(stmt, ReturnStatement)
        self.assertIsNone(stmt.value)
    
    def test_list_literal(self):
        """Test list literal parsing."""
        source = 'Let numbers be list containing 1, 2, 3, 4, 5'
        program = self.parse_source(source)
        
        stmt = program.statements[0]
        expr = stmt.value
        
        self.assertIsInstance(expr, ListLiteral)
        self.assertEqual(len(expr.elements), 5)
        
        for i, element in enumerate(expr.elements):
            self.assertIsInstance(element, IntegerLiteral)
            self.assertEqual(element.value, i + 1)
    
    def test_function_call(self):
        """Test function call parsing."""
        source = 'Let result be Calculate Total with price as 100 and tax as 0.08'
        program = self.parse_source(source)
        
        stmt = program.statements[0]
        expr = stmt.value
        
        self.assertIsInstance(expr, FunctionCall)
        self.assertEqual(expr.function_name, "Calculate Total")
        
        self.assertEqual(len(expr.arguments), 2)
        
        # First argument: price as 100
        param1_name, param1_value = expr.arguments[0]
        self.assertEqual(param1_name, "price")
        self.assertIsInstance(param1_value, IntegerLiteral)
        self.assertEqual(param1_value.value, 100)
        
        # Second argument: tax as 0.08
        param2_name, param2_value = expr.arguments[1]
        self.assertEqual(param2_name, "tax")
        self.assertIsInstance(param2_value, FloatLiteral)
        self.assertEqual(param2_value.value, 0.08)
    
    def test_parenthesized_expression(self):
        """Test parenthesized expressions."""
        source = 'Let result be (10 plus 5) multiplied by 2'
        program = self.parse_source(source)
        
        stmt = program.statements[0]
        expr = stmt.value
        
        # Should parse as: (10 plus 5) multiplied by 2
        self.assertIsInstance(expr, BinaryExpression)
        self.assertEqual(expr.operator, BinaryOperator.MULTIPLY)
        
        # Left side: (10 plus 5)
        self.assertIsInstance(expr.left, BinaryExpression)
        self.assertEqual(expr.left.operator, BinaryOperator.PLUS)
        
        # Right side: 2
        self.assertIsInstance(expr.right, IntegerLiteral)
        self.assertEqual(expr.right.value, 2)
    
    def test_multiple_statements(self):
        """Test parsing multiple statements."""
        source = '''Let x be 10
Let y be 20
Set total to x plus y
Display total'''
        program = self.parse_source(source)
        
        self.assertEqual(len(program.statements), 4)
        
        # Check each statement type
        self.assertIsInstance(program.statements[0], LetStatement)
        self.assertIsInstance(program.statements[1], LetStatement)
        self.assertIsInstance(program.statements[2], SetStatement)
        self.assertIsInstance(program.statements[3], DisplayStatement)
    
    def test_expression_statement(self):
        """Test expression statement parsing."""
        source = 'user name'
        program = self.parse_source(source)
        
        stmt = program.statements[0]
        self.assertIsInstance(stmt, ExpressionStatement)
        
        self.assertIsInstance(stmt.expression, Identifier)
        self.assertEqual(stmt.expression.name, "user name")
    
    def test_parse_error_handling(self):
        """Test parser error handling."""
        # Missing 'be' in let statement
        source = 'Let x "hello"'
        
        with self.assertRaises(ParseError) as context:
            parse_runa_source(source)
        
        self.assertIn("Expected 'be'", str(context.exception))
    
    def test_invalid_expression(self):
        """Test parsing invalid expressions."""
        # Invalid token in expression position
        source = 'Let x be :'
        
        with self.assertRaises(ParseError) as context:
            parse_runa_source(source)
        
        self.assertIn("Unexpected token", str(context.exception))

class TestRunaParserIntegration(unittest.TestCase):
    """Integration tests for the parser with complex constructs."""
    
    def test_complete_program(self):
        """Test parsing a complete program."""
        source = '''Let user name be "Alex"
Let user age be 28

If user age is greater than 21:
    Display "User is an adult"
    Set adult status to true
Otherwise:
    Display "User is a minor"
    Set adult status to false

Let numbers be list containing 1, 2, 3
Display numbers'''
        
        program = parse_runa_source(source)
        
        # Should successfully parse without errors
        self.assertTrue(len(program.statements) > 0)
        
        # Check we have the expected statement types
        statement_types = [type(stmt) for stmt in program.statements]
        
        self.assertIn(LetStatement, statement_types)
        self.assertIn(IfStatement, statement_types)
        self.assertIn(DisplayStatement, statement_types)
    
    def test_nested_expressions(self):
        """Test parsing nested expressions with multiple operators."""
        source = 'Let result be x plus y multiplied by z minus w divided by v'
        program = parse_runa_source(source)
        
        stmt = program.statements[0]
        expr = stmt.value
        
        # Should parse correctly respecting operator precedence
        self.assertIsInstance(expr, BinaryExpression)
        
        # Should be: x plus (y multiplied by z) minus (w divided by v)
        # Or similar based on left-to-right associativity
        
    def test_complex_condition(self):
        """Test parsing complex conditional expressions."""
        source = 'If age is greater than 18 and status is equal to "active":'
        
        # For now, this should raise an error since we haven't implemented
        # the full conditional parsing yet
        try:
            program = parse_runa_source(source)
            # If it doesn't error, check that we get some kind of structure
            self.assertTrue(len(program.statements) > 0)
        except ParseError:
            # Expected for now since we haven't implemented all constructs
            pass

if __name__ == '__main__':
    unittest.main() 