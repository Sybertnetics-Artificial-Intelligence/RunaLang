"""
Comprehensive Parser Tests for Runa Programming Language.

This module contains extensive tests for the recursive descent parser,
covering all grammar constructs, error handling, and edge cases.

Test Categories:
- Basic syntax parsing
- Statement parsing (declarations, assignments, etc.)
- Expression parsing (literals, binary ops, function calls)
- Control flow structures
- Function definitions
- Error handling and recovery
- Natural language constructs
- AI/ML specific syntax
"""

import pytest
from unittest.mock import Mock
from typing import List, Any

from runa.lexer import RunaLexer, Token, TokenType
from runa.parser import RunaParser, ParseResult
from runa.ast_nodes import *
from runa.errors import SourcePosition, RunaSyntaxError, ErrorReporter


class TestParserBasics:
    """Test basic parser functionality and simple constructs."""
    
    def setup_method(self):
        """Set up test environment."""
        self.error_reporter = ErrorReporter()
    
    def parse_code(self, code: str) -> ParseResult:
        """Helper to parse code string and return result."""
        lexer = RunaLexer(code)
        tokens = lexer.tokenize()
        
        if not tokens.success:
            pytest.fail(f"Lexer failed: {tokens.errors}")
        
        parser = RunaParser(tokens.tokens, self.error_reporter)
        return parser.parse()
    
    def test_empty_program(self):
        """Test parsing an empty program."""
        result = self.parse_code("")
        
        assert result.success
        assert isinstance(result.node, Program)
        assert len(result.node.statements) == 0
    
    def test_simple_literal(self):
        """Test parsing a simple literal."""
        result = self.parse_code("42")
        
        assert result.success
        assert isinstance(result.node, Program)
        assert len(result.node.statements) == 1
        
        stmt = result.node.statements[0]
        assert isinstance(stmt, ExpressionStatement)
        assert isinstance(stmt.expression, Literal)
        assert stmt.expression.value == 42
        assert stmt.expression.literal_type == "number"
    
    def test_string_literal(self):
        """Test parsing string literals."""
        result = self.parse_code('"Hello, World!"')
        
        assert result.success
        stmt = result.node.statements[0]
        assert isinstance(stmt.expression, Literal)
        assert stmt.expression.value == "Hello, World!"
        assert stmt.expression.literal_type == "string"
    
    def test_boolean_literal(self):
        """Test parsing boolean literals."""
        result = self.parse_code("true")
        
        assert result.success
        stmt = result.node.statements[0]
        assert isinstance(stmt.expression, Literal)
        assert stmt.expression.value is True
        assert stmt.expression.literal_type == "boolean"
    
    def test_null_literal(self):
        """Test parsing null literal."""
        result = self.parse_code("null")
        
        assert result.success
        stmt = result.node.statements[0]
        assert isinstance(stmt.expression, Literal)
        assert stmt.expression.value is None
        assert stmt.expression.literal_type == "null"
    
    def test_identifier(self):
        """Test parsing identifiers."""
        result = self.parse_code("variable_name")
        
        assert result.success
        stmt = result.node.statements[0]
        assert isinstance(stmt.expression, Identifier)
        assert stmt.expression.name == "variable_name"


class TestDeclarations:
    """Test variable and constant declarations."""
    
    def setup_method(self):
        """Set up test environment."""
        self.error_reporter = ErrorReporter()
    
    def parse_code(self, code: str) -> ParseResult:
        """Helper to parse code string and return result."""
        lexer = RunaLexer(code)
        tokens = lexer.tokenize()
        
        if not tokens.success:
            pytest.fail(f"Lexer failed: {tokens.errors}")
        
        parser = RunaParser(tokens.tokens, self.error_reporter)
        return parser.parse()
    
    def test_simple_variable_declaration(self):
        """Test simple variable declaration."""
        result = self.parse_code("Let x be 5")
        
        assert result.success
        stmt = result.node.statements[0]
        assert isinstance(stmt, Declaration)
        assert stmt.identifier == "x"
        assert not stmt.is_constant
        assert stmt.type_annotation is None
        assert isinstance(stmt.initializer, Literal)
        assert stmt.initializer.value == 5
    
    def test_constant_declaration(self):
        """Test constant declaration."""
        result = self.parse_code('Define name as "Alex"')
        
        assert result.success
        stmt = result.node.statements[0]
        assert isinstance(stmt, Declaration)
        assert stmt.identifier == "name"
        assert stmt.is_constant
        assert isinstance(stmt.initializer, Literal)
        assert stmt.initializer.value == "Alex"
    
    def test_typed_declaration(self):
        """Test declaration with type annotation."""
        result = self.parse_code("Let count (integer) be 0")
        
        assert result.success
        stmt = result.node.statements[0]
        assert isinstance(stmt, Declaration)
        assert stmt.identifier == "count"
        assert stmt.type_annotation is not None
        assert stmt.type_annotation.type_name == "integer"
    
    def test_generic_type_declaration(self):
        """Test declaration with generic type."""
        result = self.parse_code("Let numbers (list of integer) be list containing 1, 2, 3")
        
        assert result.success
        stmt = result.node.statements[0]
        assert isinstance(stmt, Declaration)
        assert stmt.type_annotation is not None
        assert stmt.type_annotation.type_name == "list"
        assert len(stmt.type_annotation.generic_args) == 1
        assert stmt.type_annotation.generic_args[0].type_name == "integer"


class TestAssignments:
    """Test assignment statements."""
    
    def setup_method(self):
        """Set up test environment."""
        self.error_reporter = ErrorReporter()
    
    def parse_code(self, code: str) -> ParseResult:
        """Helper to parse code string and return result."""
        lexer = RunaLexer(code)
        tokens = lexer.tokenize()
        
        if not tokens.success:
            pytest.fail(f"Lexer failed: {tokens.errors}")
        
        parser = RunaParser(tokens.tokens, self.error_reporter)
        return parser.parse()
    
    def test_simple_assignment(self):
        """Test simple assignment."""
        result = self.parse_code("Set x to 10")
        
        assert result.success
        stmt = result.node.statements[0]
        assert isinstance(stmt, Assignment)
        assert stmt.identifier == "x"
        assert isinstance(stmt.value, Literal)
        assert stmt.value.value == 10
    
    def test_expression_assignment(self):
        """Test assignment with expression."""
        result = self.parse_code("Set result to x plus y")
        
        assert result.success
        stmt = result.node.statements[0]
        assert isinstance(stmt, Assignment)
        assert stmt.identifier == "result"
        assert isinstance(stmt.value, BinaryExpression)
        assert stmt.value.operator == BinaryOperator.ADD


class TestExpressions:
    """Test expression parsing."""
    
    def setup_method(self):
        """Set up test environment."""
        self.error_reporter = ErrorReporter()
    
    def parse_code(self, code: str) -> ParseResult:
        """Helper to parse code string and return result."""
        lexer = RunaLexer(code)
        tokens = lexer.tokenize()
        
        if not tokens.success:
            pytest.fail(f"Lexer failed: {tokens.errors}")
        
        parser = RunaParser(tokens.tokens, self.error_reporter)
        return parser.parse()
    
    def test_binary_addition(self):
        """Test binary addition expression."""
        result = self.parse_code("x plus y")
        
        assert result.success
        stmt = result.node.statements[0]
        expr = stmt.expression
        assert isinstance(expr, BinaryExpression)
        assert expr.operator == BinaryOperator.ADD
        assert isinstance(expr.left, Identifier)
        assert expr.left.name == "x"
        assert isinstance(expr.right, Identifier)
        assert expr.right.name == "y"
    
    def test_binary_comparison(self):
        """Test binary comparison expression."""
        result = self.parse_code("a is greater than b")
        
        assert result.success
        stmt = result.node.statements[0]
        expr = stmt.expression
        assert isinstance(expr, BinaryExpression)
        assert expr.operator == BinaryOperator.GREATER_THAN
    
    def test_complex_expression(self):
        """Test complex expression with multiple operators."""
        result = self.parse_code("x plus y multiplied by z")
        
        assert result.success
        stmt = result.node.statements[0]
        expr = stmt.expression
        assert isinstance(expr, BinaryExpression)
        assert expr.operator == BinaryOperator.ADD
        
        # Right side should be multiplication (higher precedence)
        assert isinstance(expr.right, BinaryExpression)
        assert expr.right.operator == BinaryOperator.MULTIPLY
    
    def test_parenthesized_expression(self):
        """Test parenthesized expressions."""
        result = self.parse_code("(x plus y) multiplied by z")
        
        assert result.success
        stmt = result.node.statements[0]
        expr = stmt.expression
        assert isinstance(expr, BinaryExpression)
        assert expr.operator == BinaryOperator.MULTIPLY
        
        # Left side should be addition (due to parentheses)
        assert isinstance(expr.left, BinaryExpression)
        assert expr.left.operator == BinaryOperator.ADD
    
    def test_unary_expression(self):
        """Test unary expressions."""
        result = self.parse_code("not condition")
        
        assert result.success
        stmt = result.node.statements[0]
        expr = stmt.expression
        assert isinstance(expr, UnaryExpression)
        assert expr.operator == UnaryOperator.NOT
        assert isinstance(expr.operand, Identifier)
        assert expr.operand.name == "condition"


class TestFunctionCalls:
    """Test function call parsing."""
    
    def setup_method(self):
        """Set up test environment."""
        self.error_reporter = ErrorReporter()
    
    def parse_code(self, code: str) -> ParseResult:
        """Helper to parse code string and return result."""
        lexer = RunaLexer(code)
        tokens = lexer.tokenize()
        
        if not tokens.success:
            pytest.fail(f"Lexer failed: {tokens.errors}")
        
        parser = RunaParser(tokens.tokens, self.error_reporter)
        return parser.parse()
    
    def test_simple_function_call(self):
        """Test simple function call."""
        result = self.parse_code("calculate with x as 5")
        
        assert result.success
        stmt = result.node.statements[0]
        expr = stmt.expression
        assert isinstance(expr, FunctionCall)
        assert expr.function_name == "calculate"
        assert len(expr.arguments) == 1
        assert expr.arguments[0][0] == "x"
        assert isinstance(expr.arguments[0][1], Literal)
        assert expr.arguments[0][1].value == 5
    
    def test_multiple_argument_function_call(self):
        """Test function call with multiple arguments."""
        result = self.parse_code("process with x as 10 and y as 20")
        
        assert result.success
        stmt = result.node.statements[0]
        expr = stmt.expression
        assert isinstance(expr, FunctionCall)
        assert expr.function_name == "process"
        assert len(expr.arguments) == 2
        assert expr.arguments[0][0] == "x"
        assert expr.arguments[1][0] == "y"


class TestListExpressions:
    """Test list expression parsing."""
    
    def setup_method(self):
        """Set up test environment."""
        self.error_reporter = ErrorReporter()
    
    def parse_code(self, code: str) -> ParseResult:
        """Helper to parse code string and return result."""
        lexer = RunaLexer(code)
        tokens = lexer.tokenize()
        
        if not tokens.success:
            pytest.fail(f"Lexer failed: {tokens.errors}")
        
        parser = RunaParser(tokens.tokens, self.error_reporter)
        return parser.parse()
    
    def test_empty_list(self):
        """Test empty list expression."""
        result = self.parse_code("list containing")
        
        assert result.success
        stmt = result.node.statements[0]
        expr = stmt.expression
        assert isinstance(expr, ListExpression)
        assert len(expr.elements) == 0
    
    def test_simple_list(self):
        """Test simple list expression."""
        result = self.parse_code("list containing 1, 2, 3")
        
        assert result.success
        stmt = result.node.statements[0]
        expr = stmt.expression
        assert isinstance(expr, ListExpression)
        assert len(expr.elements) == 3
        
        for i, element in enumerate(expr.elements):
            assert isinstance(element, Literal)
            assert element.value == i + 1
    
    def test_mixed_list(self):
        """Test list with mixed types."""
        result = self.parse_code('list containing 1, "hello", true')
        
        assert result.success
        stmt = result.node.statements[0]
        expr = stmt.expression
        assert isinstance(expr, ListExpression)
        assert len(expr.elements) == 3
        
        assert expr.elements[0].value == 1
        assert expr.elements[1].value == "hello"
        assert expr.elements[2].value is True


class TestDisplayStatements:
    """Test display statement parsing."""
    
    def setup_method(self):
        """Set up test environment."""
        self.error_reporter = ErrorReporter()
    
    def parse_code(self, code: str) -> ParseResult:
        """Helper to parse code string and return result."""
        lexer = RunaLexer(code)
        tokens = lexer.tokenize()
        
        if not tokens.success:
            pytest.fail(f"Lexer failed: {tokens.errors}")
        
        parser = RunaParser(tokens.tokens, self.error_reporter)
        return parser.parse()
    
    def test_simple_display(self):
        """Test simple display statement."""
        result = self.parse_code("Display x")
        
        assert result.success
        stmt = result.node.statements[0]
        assert isinstance(stmt, DisplayStatement)
        assert isinstance(stmt.expression, Identifier)
        assert stmt.expression.name == "x"
        assert stmt.message is None
    
    def test_display_with_message(self):
        """Test display statement with message."""
        result = self.parse_code('Display x with "Result:"')
        
        assert result.success
        stmt = result.node.statements[0]
        assert isinstance(stmt, DisplayStatement)
        assert isinstance(stmt.expression, Identifier)
        assert stmt.expression.name == "x"
        assert isinstance(stmt.message, Literal)
        assert stmt.message.value == "Result:"


class TestComments:
    """Test comment parsing."""
    
    def setup_method(self):
        """Set up test environment."""
        self.error_reporter = ErrorReporter()
    
    def parse_code(self, code: str) -> ParseResult:
        """Helper to parse code string and return result."""
        lexer = RunaLexer(code)
        tokens = lexer.tokenize()
        
        if not tokens.success:
            pytest.fail(f"Lexer failed: {tokens.errors}")
        
        parser = RunaParser(tokens.tokens, self.error_reporter)
        return parser.parse()
    
    def test_simple_comment(self):
        """Test simple comment."""
        result = self.parse_code("# This is a comment")
        
        assert result.success
        stmt = result.node.statements[0]
        assert isinstance(stmt, Comment)
        assert "This is a comment" in stmt.text


class TestErrorHandling:
    """Test parser error handling and recovery."""
    
    def setup_method(self):
        """Set up test environment."""
        self.error_reporter = ErrorReporter()
    
    def parse_code(self, code: str) -> ParseResult:
        """Helper to parse code string and return result."""
        lexer = RunaLexer(code)
        tokens = lexer.tokenize()
        
        if not tokens.success:
            pytest.fail(f"Lexer failed: {tokens.errors}")
        
        parser = RunaParser(tokens.tokens, self.error_reporter)
        return parser.parse()
    
    def test_missing_identifier(self):
        """Test error when identifier is missing."""
        result = self.parse_code("Let be 5")
        
        assert not result.success
        assert len(result.errors) > 0
        assert "Expected identifier" in str(result.errors[0])
    
    def test_missing_value(self):
        """Test error when value is missing."""
        result = self.parse_code("Let x be")
        
        assert not result.success
        assert len(result.errors) > 0
    
    def test_invalid_token(self):
        """Test error with invalid token."""
        result = self.parse_code("Let x be @@@")
        
        # This would be caught by lexer, but test parser robustness
        # if somehow an invalid token gets through
        assert not result.success
    
    def test_incomplete_binary_expression(self):
        """Test error with incomplete binary expression."""
        result = self.parse_code("x plus")
        
        assert not result.success
        assert len(result.errors) > 0


class TestComplexPrograms:
    """Test parsing of complex, multi-statement programs."""
    
    def setup_method(self):
        """Set up test environment."""
        self.error_reporter = ErrorReporter()
    
    def parse_code(self, code: str) -> ParseResult:
        """Helper to parse code string and return result."""
        lexer = RunaLexer(code)
        tokens = lexer.tokenize()
        
        if not tokens.success:
            pytest.fail(f"Lexer failed: {tokens.errors}")
        
        parser = RunaParser(tokens.tokens, self.error_reporter)
        return parser.parse()
    
    def test_multiple_statements(self):
        """Test program with multiple statements."""
        code = '''
        Let x be 5
        Let y be 10
        Set x to x plus y
        Display x
        '''
        
        result = self.parse_code(code)
        
        assert result.success
        assert len(result.node.statements) == 4
        
        # Check each statement type
        assert isinstance(result.node.statements[0], Declaration)
        assert isinstance(result.node.statements[1], Declaration)
        assert isinstance(result.node.statements[2], Assignment)
        assert isinstance(result.node.statements[3], DisplayStatement)
    
    def test_complex_expression_program(self):
        """Test program with complex expressions."""
        code = '''
        Let a be 1
        Let b be 2
        Let c be 3
        Let result be (a plus b) multiplied by c
        Display result
        '''
        
        result = self.parse_code(code)
        
        assert result.success
        assert len(result.node.statements) == 5
        
        # Check the complex expression in the fourth statement
        complex_decl = result.node.statements[3]
        assert isinstance(complex_decl, Declaration)
        assert isinstance(complex_decl.initializer, BinaryExpression)
        assert complex_decl.initializer.operator == BinaryOperator.MULTIPLY
    
    def test_function_call_program(self):
        """Test program with function calls."""
        code = '''
        Let x be 5
        Let y be calculate with value as x
        Display y
        '''
        
        result = self.parse_code(code)
        
        assert result.success
        assert len(result.node.statements) == 3
        
        # Check function call in second statement
        func_decl = result.node.statements[1]
        assert isinstance(func_decl, Declaration)
        assert isinstance(func_decl.initializer, FunctionCall)
        assert func_decl.initializer.function_name == "calculate"


class TestNaturalLanguageConstructs:
    """Test parsing of natural language constructs specific to Runa."""
    
    def setup_method(self):
        """Set up test environment."""
        self.error_reporter = ErrorReporter()
    
    def parse_code(self, code: str) -> ParseResult:
        """Helper to parse code string and return result."""
        lexer = RunaLexer(code)
        tokens = lexer.tokenize()
        
        if not tokens.success:
            pytest.fail(f"Lexer failed: {tokens.errors}")
        
        parser = RunaParser(tokens.tokens, self.error_reporter)
        return parser.parse()
    
    def test_natural_comparison(self):
        """Test natural language comparison operators."""
        result = self.parse_code("age is greater than 18")
        
        assert result.success
        stmt = result.node.statements[0]
        expr = stmt.expression
        assert isinstance(expr, BinaryExpression)
        assert expr.operator == BinaryOperator.GREATER_THAN
    
    def test_natural_equality(self):
        """Test natural language equality."""
        result = self.parse_code("name is equal to 'John'")
        
        assert result.success
        stmt = result.node.statements[0]
        expr = stmt.expression
        assert isinstance(expr, BinaryExpression)
        assert expr.operator == BinaryOperator.EQUALS
    
    def test_natural_arithmetic(self):
        """Test natural language arithmetic."""
        result = self.parse_code("total multiplied by rate")
        
        assert result.success
        stmt = result.node.statements[0]
        expr = stmt.expression
        assert isinstance(expr, BinaryExpression)
        assert expr.operator == BinaryOperator.MULTIPLY
    
    def test_string_concatenation(self):
        """Test natural language string concatenation."""
        result = self.parse_code("first_name followed by last_name")
        
        assert result.success
        stmt = result.node.statements[0]
        expr = stmt.expression
        assert isinstance(expr, BinaryExpression)
        assert expr.operator == BinaryOperator.CONCATENATE


class TestSourcePositions:
    """Test that source positions are correctly tracked."""
    
    def setup_method(self):
        """Set up test environment."""
        self.error_reporter = ErrorReporter()
    
    def parse_code(self, code: str) -> ParseResult:
        """Helper to parse code string and return result."""
        lexer = RunaLexer(code)
        tokens = lexer.tokenize()
        
        if not tokens.success:
            pytest.fail(f"Lexer failed: {tokens.errors}")
        
        parser = RunaParser(tokens.tokens, self.error_reporter)
        return parser.parse()
    
    def test_position_tracking(self):
        """Test that AST nodes have correct source positions."""
        result = self.parse_code("Let x be 5")
        
        assert result.success
        stmt = result.node.statements[0]
        
        # Check that positions are set
        assert stmt.position is not None
        assert stmt.position.line >= 1
        assert stmt.position.column >= 1
        
        # Check initializer position
        assert stmt.initializer.position is not None
    
    def test_multiline_positions(self):
        """Test position tracking across multiple lines."""
        code = '''Let x be 5
Let y be 10'''
        
        result = self.parse_code(code)
        
        assert result.success
        assert len(result.node.statements) == 2
        
        # First statement should be on line 1
        stmt1 = result.node.statements[0]
        assert stmt1.position.line == 1
        
        # Second statement should be on line 2
        stmt2 = result.node.statements[1]
        assert stmt2.position.line == 2


# Additional integration tests
class TestParserIntegration:
    """Integration tests combining multiple parser features."""
    
    def setup_method(self):
        """Set up test environment."""
        self.error_reporter = ErrorReporter()
    
    def parse_code(self, code: str) -> ParseResult:
        """Helper to parse code string and return result."""
        lexer = RunaLexer(code)
        tokens = lexer.tokenize()
        
        if not tokens.success:
            pytest.fail(f"Lexer failed: {tokens.errors}")
        
        parser = RunaParser(tokens.tokens, self.error_reporter)
        return parser.parse()
    
    def test_comprehensive_program(self):
        """Test a comprehensive program using multiple features."""
        code = '''
        # Initialize variables
        Let x be 10
        Let y be 20
        Define pi as 3.14159
        
        # Calculate area
        Let area be x multiplied by y
        
        # Display results
        Display area with "Area is:"
        
        # Function call
        Let formatted be format with value as area and precision as 2
        Display formatted
        
        # List operations
        Let numbers be list containing 1, 2, 3, 4, 5
        Display numbers
        '''
        
        result = self.parse_code(code)
        
        assert result.success
        program = result.node
        
        # Should have multiple statements
        assert len(program.statements) > 5
        
        # Check for different statement types
        statement_types = [type(stmt).__name__ for stmt in program.statements]
        assert "Comment" in statement_types
        assert "Declaration" in statement_types
        assert "DisplayStatement" in statement_types
    
    def test_error_recovery(self):
        """Test that parser can recover from errors and continue parsing."""
        code = '''
        Let x be 5
        Let invalid syntax here
        Let y be 10
        Display y
        '''
        
        result = self.parse_code(code)
        
        # Should have errors but still parse some statements
        assert not result.success
        assert len(result.errors) > 0
        
        # Should still have parsed the valid statements
        assert result.node is not None
        assert isinstance(result.node, Program)


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"]) 