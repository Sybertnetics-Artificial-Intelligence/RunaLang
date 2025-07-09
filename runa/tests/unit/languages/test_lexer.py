"""
Tests for the Runa Lexer

Tests natural language tokenization including:
- Multi-word tokens
- Keywords and identifiers
- Natural language operators
- Indentation handling
- String and numeric literals
"""

import unittest
from runa.compiler.lexer import RunaLexer, LexerError
from runa.compiler.tokens import TokenType, Token

class TestRunaLexer(unittest.TestCase):
    """Test cases for the Runa lexer."""
    
    def setUp(self):
        """Set up test fixtures."""
        pass
    
    def test_basic_keywords(self):
        """Test recognition of basic keywords."""
        source = "Let Define Set If Otherwise"
        lexer = RunaLexer(source)
        tokens = lexer.tokenize()
        
        expected_types = [
            TokenType.LET,
            TokenType.DEFINE,
            TokenType.SET,
            TokenType.IF,
            TokenType.OTHERWISE,
            TokenType.EOF
        ]
        
        actual_types = [token.type for token in tokens]
        self.assertEqual(actual_types, expected_types)
    
    def test_multi_word_operators(self):
        """Test recognition of multi-word natural language operators."""
        source = "is greater than is equal to multiplied by divided by"
        lexer = RunaLexer(source)
        tokens = lexer.tokenize()
        
        expected_types = [
            TokenType.GREATER_THAN,
            TokenType.EQUALS,
            TokenType.MULTIPLY,
            TokenType.DIVIDE,
            TokenType.EOF
        ]
        
        actual_types = [token.type for token in tokens]
        self.assertEqual(actual_types, expected_types)
    
    def test_string_literals(self):
        """Test string literal parsing."""
        source = '"Hello, World!" "String with \\"quotes\\"" "Multi\\nline"'
        lexer = RunaLexer(source)
        tokens = lexer.tokenize()
        
        string_tokens = [t for t in tokens if t.type == TokenType.STRING]
        self.assertEqual(len(string_tokens), 3)
        self.assertEqual(string_tokens[0].value, "Hello, World!")
        self.assertEqual(string_tokens[1].value, 'String with "quotes"')
        self.assertEqual(string_tokens[2].value, "Multi\nline")
    
    def test_numeric_literals(self):
        """Test numeric literal parsing."""
        source = "42 3.14159 0 100.0"
        lexer = RunaLexer(source)
        tokens = lexer.tokenize()
        
        numeric_tokens = [t for t in tokens if t.type in (TokenType.INTEGER, TokenType.FLOAT)]
        self.assertEqual(len(numeric_tokens), 4)
        
        self.assertEqual(numeric_tokens[0].type, TokenType.INTEGER)
        self.assertEqual(numeric_tokens[0].value, 42)
        
        self.assertEqual(numeric_tokens[1].type, TokenType.FLOAT)
        self.assertEqual(numeric_tokens[1].value, 3.14159)
        
        self.assertEqual(numeric_tokens[2].type, TokenType.INTEGER)
        self.assertEqual(numeric_tokens[2].value, 0)
        
        self.assertEqual(numeric_tokens[3].type, TokenType.FLOAT)
        self.assertEqual(numeric_tokens[3].value, 100.0)
    
    def test_boolean_literals(self):
        """Test boolean literal parsing."""
        source = "true false True False"
        lexer = RunaLexer(source)
        tokens = lexer.tokenize()
        
        bool_tokens = [t for t in tokens if t.type == TokenType.BOOLEAN]
        self.assertEqual(len(bool_tokens), 4)
        
        self.assertEqual(bool_tokens[0].value, True)
        self.assertEqual(bool_tokens[1].value, False)
        self.assertEqual(bool_tokens[2].value, True)
        self.assertEqual(bool_tokens[3].value, False)
    
    def test_identifiers(self):
        """Test identifier parsing."""
        source = "user_name totalPrice item count_of_items"
        lexer = RunaLexer(source)
        tokens = lexer.tokenize()
        
        identifier_tokens = [t for t in tokens if t.type == TokenType.IDENTIFIER]
        self.assertEqual(len(identifier_tokens), 4)
        
        expected_names = ["user_name", "totalPrice", "item", "count_of_items"]
        actual_names = [t.value for t in identifier_tokens]
        self.assertEqual(actual_names, expected_names)
    
    def test_comments(self):
        """Test comment handling."""
        source = """Let x be 5
Note: This is a comment
Set y to 10"""
        lexer = RunaLexer(source)
        tokens = lexer.tokenize()
        
        # Comments should be skipped, no NOTE tokens should appear
        token_types = [t.type for t in tokens]
        self.assertNotIn(TokenType.NOTE, token_types)
        
        # Should have LET, identifier, BE, integer, NEWLINE, SET, identifier, TO, integer, EOF
        expected_significant_types = [
            TokenType.LET, TokenType.IDENTIFIER, TokenType.BE, TokenType.INTEGER,
            TokenType.NEWLINE, TokenType.SET, TokenType.IDENTIFIER, TokenType.TO, TokenType.INTEGER,
            TokenType.EOF
        ]
        
        # Filter out newlines for easier comparison
        significant_tokens = [t for t in tokens if t.type != TokenType.NEWLINE]
        significant_types = [t.type for t in significant_tokens]
        
        self.assertEqual(significant_types, [
            TokenType.LET, TokenType.IDENTIFIER, TokenType.BE, TokenType.INTEGER,
            TokenType.SET, TokenType.IDENTIFIER, TokenType.TO, TokenType.INTEGER,
            TokenType.EOF
        ])
    
    def test_simple_let_statement(self):
        """Test tokenizing a simple let statement."""
        source = 'Let user name be "Alex"'
        lexer = RunaLexer(source)
        tokens = lexer.tokenize()
        
        expected_types = [
            TokenType.LET,
            TokenType.IDENTIFIER,  # "user name" (identifier with space)
            TokenType.BE,
            TokenType.STRING,
            TokenType.EOF
        ]
        
        actual_types = [token.type for token in tokens]
        self.assertEqual(actual_types, expected_types)
        
        # Check the identifier value includes the space
        identifier_token = tokens[1]
        self.assertEqual(identifier_token.value, "user name")
        
        # Check string value
        string_token = tokens[3]
        self.assertEqual(string_token.value, "Alex")
    
    def test_natural_comparison(self):
        """Test natural language comparison expression."""
        source = "user age is greater than 21"
        lexer = RunaLexer(source)
        tokens = lexer.tokenize()
        
        expected_types = [
            TokenType.IDENTIFIER,     # "user age"
            TokenType.GREATER_THAN,   # "is greater than"
            TokenType.INTEGER,        # 21
            TokenType.EOF
        ]
        
        actual_types = [token.type for token in tokens]
        self.assertEqual(actual_types, expected_types)
    
    def test_process_definition_start(self):
        """Test the start of a process definition."""
        source = 'Process called "Calculate Total"'
        lexer = RunaLexer(source)
        tokens = lexer.tokenize()
        
        expected_types = [
            TokenType.PROCESS,
            TokenType.CALLED,
            TokenType.STRING,
            TokenType.EOF
        ]
        
        actual_types = [token.type for token in tokens]
        self.assertEqual(actual_types, expected_types)
        
        string_token = tokens[2]
        self.assertEqual(string_token.value, "Calculate Total")
    
    def test_punctuation(self):
        """Test punctuation tokenization."""
        source = "(): []{}, .;"
        lexer = RunaLexer(source)
        tokens = lexer.tokenize()
        
        expected_types = [
            TokenType.LPAREN,
            TokenType.RPAREN,
            TokenType.COLON,
            TokenType.LBRACKET,
            TokenType.RBRACKET,
            TokenType.LBRACE,
            TokenType.RBRACE,
            TokenType.COMMA,
            TokenType.DOT,
            TokenType.SEMICOLON,
            TokenType.EOF
        ]
        
        actual_types = [token.type for token in tokens]
        self.assertEqual(actual_types, expected_types)
    
    def test_arithmetic_operations(self):
        """Test arithmetic operation tokenization."""
        source = "x plus y minus z multiplied by 2 divided by 3"
        lexer = RunaLexer(source)
        tokens = lexer.tokenize()
        
        expected_types = [
            TokenType.IDENTIFIER,  # x
            TokenType.PLUS,        # plus
            TokenType.IDENTIFIER,  # y
            TokenType.MINUS,       # minus
            TokenType.IDENTIFIER,  # z
            TokenType.MULTIPLY,    # multiplied by
            TokenType.INTEGER,     # 2
            TokenType.DIVIDE,      # divided by
            TokenType.INTEGER,     # 3
            TokenType.EOF
        ]
        
        actual_types = [token.type for token in tokens]
        self.assertEqual(actual_types, expected_types)
    
    def test_error_handling(self):
        """Test lexer error handling."""
        source = "Let x be @invalid"  # @ is not a valid character
        lexer = RunaLexer(source)
        
        with self.assertRaises(LexerError) as context:
            lexer.tokenize()
        
        self.assertIn("Unexpected character", str(context.exception))
    
    def test_unterminated_string(self):
        """Test unterminated string error."""
        source = 'Let x be "unterminated string'
        lexer = RunaLexer(source)
        
        with self.assertRaises(LexerError) as context:
            lexer.tokenize()
        
        self.assertIn("Unterminated string literal", str(context.exception))

class TestRunaLexerIntegration(unittest.TestCase):
    """Integration tests for the lexer with realistic Runa code."""
    
    def test_complete_program(self):
        """Test lexing a complete small Runa program."""
        source = '''Let user name be "Alex"
Let user age be 28

If user age is greater than 21:
    Display "User is an adult"
Otherwise:
    Display "User is a minor"'''
        
        lexer = RunaLexer(source)
        tokens = lexer.tokenize()
        
        # Should successfully tokenize without errors
        self.assertTrue(len(tokens) > 0)
        self.assertEqual(tokens[-1].type, TokenType.EOF)
        
        # Check that we have the major token types we expect
        token_types = [t.type for t in tokens]
        
        self.assertIn(TokenType.LET, token_types)
        self.assertIn(TokenType.IF, token_types)
        self.assertIn(TokenType.OTHERWISE, token_types)
        self.assertIn(TokenType.DISPLAY, token_types)
        self.assertIn(TokenType.GREATER_THAN, token_types)
        self.assertIn(TokenType.STRING, token_types)
        self.assertIn(TokenType.INTEGER, token_types)
    
    def test_function_definition(self):
        """Test lexing a function definition."""
        source = '''Process called "Calculate Total Price" that takes items and tax rate:
    Let subtotal be the sum of all prices in items
    Return subtotal plus tax amount'''
        
        lexer = RunaLexer(source)
        tokens = lexer.tokenize()
        
        # Should successfully tokenize
        self.assertTrue(len(tokens) > 0)
        self.assertEqual(tokens[-1].type, TokenType.EOF)
        
        # Check for function-related tokens
        token_types = [t.type for t in tokens]
        self.assertIn(TokenType.PROCESS, token_types)
        self.assertIn(TokenType.CALLED, token_types)
        self.assertIn(TokenType.THAT, token_types)
        self.assertIn(TokenType.TAKES, token_types)
        self.assertIn(TokenType.RETURN, token_types)

if __name__ == '__main__':
    unittest.main() 