"""
Comprehensive tests for Runa lexer functionality.

Tests all major lexer features including tokenization,
error handling, and edge cases.
"""

import pytest
from runa.lexer import RunaLexer, Token, TokenType
from runa.errors import ErrorReporter


class TestRunaLexer:
    """Test suite for RunaLexer class."""
    
    def test_lexer_initialization(self):
        """Test that lexer initializes properly."""
        source = "let x be 5"
        lexer = RunaLexer(source)
        
        assert lexer.source == source
        assert lexer.pos == 0
        assert lexer.line == 1
        assert lexer.column == 1
        assert lexer.filename is None
    
    def test_simple_keywords(self):
        """Test recognition of basic Runa keywords."""
        source = "let define set"
        lexer = RunaLexer(source)
        tokens = lexer.tokenize()
        
        expected_types = [TokenType.LET, TokenType.DEFINE, TokenType.SET, TokenType.EOF]
        actual_types = [token.type for token in tokens]
        
        assert actual_types == expected_types
    
    def test_identifiers(self):
        """Test recognition of identifiers."""
        source = "variable_name user_age count"
        lexer = RunaLexer(source)
        tokens = lexer.tokenize()
        
        # Should be 3 identifiers + EOF
        assert len(tokens) == 4
        assert all(token.type == TokenType.IDENTIFIER for token in tokens[:-1])
        assert tokens[0].value == "variable_name"
        assert tokens[1].value == "user_age"
        assert tokens[2].value == "count"
    
    def test_numbers(self):
        """Test recognition of numeric literals."""
        source = "42 3.14 0.5"
        lexer = RunaLexer(source)
        tokens = lexer.tokenize()
        
        # Should be 3 numbers + EOF
        assert len(tokens) == 4
        assert all(token.type == TokenType.NUMBER for token in tokens[:-1])
        assert tokens[0].value == "42"
        assert tokens[1].value == "3.14"
        assert tokens[2].value == "0.5"
    
    def test_strings(self):
        """Test recognition of string literals."""
        source = '"Hello World" \'Single quotes\''
        lexer = RunaLexer(source)
        tokens = lexer.tokenize()
        
        # Should be 2 strings + EOF
        assert len(tokens) == 3
        assert tokens[0].type == TokenType.STRING
        assert tokens[0].value == "Hello World"
        assert tokens[1].type == TokenType.STRING
        assert tokens[1].value == "Single quotes"
    
    def test_string_escapes(self):
        """Test string escape sequences."""
        source = r'"Hello\nWorld" "Quote: \"test\""'
        lexer = RunaLexer(source)
        tokens = lexer.tokenize()
        
        assert tokens[0].type == TokenType.STRING
        assert tokens[0].value == "Hello\nWorld"
        assert tokens[1].type == TokenType.STRING
        assert tokens[1].value == 'Quote: "test"'
    
    def test_punctuation(self):
        """Test recognition of punctuation tokens."""
        source = ": , . ( ) [ ] { }"
        lexer = RunaLexer(source)
        tokens = lexer.tokenize()
        
        expected_types = [
            TokenType.COLON, TokenType.COMMA, TokenType.DOT,
            TokenType.LPAREN, TokenType.RPAREN,
            TokenType.LBRACKET, TokenType.RBRACKET,
            TokenType.LBRACE, TokenType.RBRACE,
            TokenType.EOF
        ]
        actual_types = [token.type for token in tokens]
        assert actual_types == expected_types
    
    def test_operators(self):
        """Test recognition of operator tokens."""
        source = "+ - * / = < >"
        lexer = RunaLexer(source)
        tokens = lexer.tokenize()
        
        expected_types = [
            TokenType.PLUS_SYMBOL, TokenType.MINUS_SYMBOL,
            TokenType.MULTIPLY_SYMBOL, TokenType.DIVIDE_SYMBOL,
            TokenType.ASSIGN, TokenType.LESS_THAN, TokenType.GREATER_THAN,
            TokenType.EOF
        ]
        actual_types = [token.type for token in tokens]
        assert actual_types == expected_types
    
    def test_comments(self):
        """Test comment handling."""
        source = "let x be 5 # This is a comment\nlet y be 10"
        lexer = RunaLexer(source)
        tokens = lexer.tokenize()
        
        # Should include comment token
        comment_tokens = [token for token in tokens if token.type == TokenType.COMMENT]
        assert len(comment_tokens) == 1
        assert comment_tokens[0].value == "# This is a comment"
    
    def test_ai_keywords(self):
        """Test AI/ML specific keywords."""
        source = "neural network layer training"
        lexer = RunaLexer(source)
        tokens = lexer.tokenize()
        
        expected_types = [
            TokenType.NEURAL, TokenType.NETWORK, 
            TokenType.LAYER, TokenType.TRAINING,
            TokenType.EOF
        ]
        actual_types = [token.type for token in tokens]
        assert actual_types == expected_types
    
    def test_boolean_literals(self):
        """Test boolean literal recognition."""
        source = "true false"
        lexer = RunaLexer(source)
        tokens = lexer.tokenize()
        
        assert tokens[0].type == TokenType.BOOLEAN
        assert tokens[0].value == "true"
        assert tokens[1].type == TokenType.BOOLEAN
        assert tokens[1].value == "false"
    
    def test_null_literals(self):
        """Test null literal recognition."""
        source = "null none"
        lexer = RunaLexer(source)
        tokens = lexer.tokenize()
        
        assert tokens[0].type == TokenType.NULL
        assert tokens[0].value == "null"
        assert tokens[1].type == TokenType.NULL
        assert tokens[1].value == "none"
    
    def test_newlines(self):
        """Test newline handling."""
        source = "let x be 5\nlet y be 10"
        lexer = RunaLexer(source)
        tokens = lexer.tokenize()
        
        newline_tokens = [token for token in tokens if token.type == TokenType.NEWLINE]
        assert len(newline_tokens) == 1
    
    def test_comprehensive_program(self, hello_world_program):
        """Test lexing a complete program."""
        lexer = RunaLexer(hello_world_program)
        tokens = lexer.tokenize()
        
        # Should successfully tokenize without errors
        assert len(tokens) > 0
        assert tokens[-1].type == TokenType.EOF
        
        # Should contain display and string tokens
        token_types = [token.type for token in tokens]
        assert TokenType.DISPLAY in token_types
        assert TokenType.STRING in token_types
    
    def test_position_tracking(self):
        """Test that source positions are tracked correctly."""
        source = "let\nx\nbe\n5"
        lexer = RunaLexer(source)
        tokens = lexer.tokenize()
        
        # Check that line numbers increment correctly
        let_token = tokens[0]
        assert let_token.line == 1
        assert let_token.column == 1
        
        # Find the x token (should be on line 2)
        x_token = next(token for token in tokens if token.value == "x")
        assert x_token.line == 2
    
    def test_whitespace_handling(self):
        """Test that whitespace is handled correctly."""
        source = "  let   x   be   5  "
        lexer = RunaLexer(source)
        tokens = lexer.tokenize()
        
        # Should tokenize correctly despite extra whitespace
        expected_types = [TokenType.LET, TokenType.IDENTIFIER, TokenType.BE, TokenType.NUMBER, TokenType.EOF]
        actual_types = [token.type for token in tokens]
        assert actual_types == expected_types
    
    def test_error_reporter_integration(self):
        """Test integration with error reporter."""
        error_reporter = ErrorReporter()
        source = "let x be 5"
        lexer = RunaLexer(source, error_reporter=error_reporter)
        
        tokens = lexer.tokenize()
        
        # Should not have any errors for valid code
        assert not error_reporter.has_errors()
        assert len(tokens) > 0


class TestTokenClass:
    """Test suite for Token class."""
    
    def test_token_creation(self):
        """Test Token creation and properties."""
        token = Token(TokenType.LET, "let", 1, 1, "test.runa")
        
        assert token.type == TokenType.LET
        assert token.value == "let"
        assert token.line == 1
        assert token.column == 1
        assert token.filename == "test.runa"
    
    def test_token_position_property(self):
        """Test Token position property."""
        token = Token(TokenType.IDENTIFIER, "x", 5, 10, "test.runa")
        position = token.position
        
        assert position.line == 5
        assert position.column == 10
        assert position.filename == "test.runa"
    
    def test_token_string_representation(self):
        """Test Token string representation."""
        token = Token(TokenType.STRING, "Hello", 2, 5)
        string_repr = str(token)
        
        assert "STRING" in string_repr
        assert "Hello" in string_repr
        assert "2:5" in string_repr


class TestTokenTypeEnum:
    """Test suite for TokenType enum."""
    
    def test_token_type_count(self):
        """Test that we have the required number of token types."""
        # Should have 50+ token types as specified
        token_count = len(list(TokenType))
        assert token_count >= 50, f"Expected at least 50 token types, got {token_count}"
    
    def test_all_keyword_coverage(self):
        """Test that all keywords are covered in token types."""
        # Test some critical keywords
        assert TokenType.LET in TokenType
        assert TokenType.DEFINE in TokenType
        assert TokenType.IF in TokenType
        assert TokenType.PROCESS in TokenType
        assert TokenType.NEURAL in TokenType
        assert TokenType.NETWORK in TokenType


class TestLexerPerformance:
    """Performance tests for the lexer."""
    
    @pytest.mark.benchmark
    def test_lexer_performance(self, benchmark):
        """Benchmark lexer performance."""
        # Create a moderately sized program for benchmarking
        source = """
        let user_name be "Alice"
        let age be 30
        
        if age is greater than 18:
            display "Adult"
        otherwise:
            display "Minor"
            
        for each number in list containing 1, 2, 3, 4, 5:
            display number
        """
        
        def tokenize_source():
            lexer = RunaLexer(source)
            return lexer.tokenize()
        
        # Benchmark the tokenization
        result = benchmark(tokenize_source)
        
        # Verify result is correct
        assert len(result) > 0
        assert result[-1].type == TokenType.EOF
    
    @pytest.mark.benchmark
    def test_large_program_performance(self, benchmark):
        """Test performance on larger programs."""
        # Generate a larger program
        lines = []
        for i in range(100):
            lines.append(f'let variable_{i} be {i}')
            lines.append(f'display variable_{i}')
        
        source = '\n'.join(lines)
        
        def tokenize_large_source():
            lexer = RunaLexer(source)
            return lexer.tokenize()
        
        result = benchmark(tokenize_large_source)
        
        # Verify result
        assert len(result) > 0
        assert result[-1].type == TokenType.EOF


@pytest.mark.integration
class TestLexerIntegration:
    """Integration tests for lexer with different program types."""
    
    def test_variable_program(self, variables_program):
        """Test lexing variable operations program."""
        lexer = RunaLexer(variables_program)
        tokens = lexer.tokenize()
        
        token_types = [token.type for token in tokens]
        assert TokenType.LET in token_types
        assert TokenType.SET in token_types
        assert TokenType.DISPLAY in token_types
    
    def test_control_flow_program(self, control_flow_program):
        """Test lexing control flow program."""
        lexer = RunaLexer(control_flow_program)
        tokens = lexer.tokenize()
        
        token_types = [token.type for token in tokens]
        assert TokenType.IF in token_types
        assert TokenType.OTHERWISE in token_types
        assert TokenType.GREATER in token_types
        assert TokenType.THAN in token_types
    
    def test_ai_model_program(self, ai_model_program):
        """Test lexing AI model definition program."""
        lexer = RunaLexer(ai_model_program)
        tokens = lexer.tokenize()
        
        token_types = [token.type for token in tokens]
        assert TokenType.DEFINE in token_types
        assert TokenType.NEURAL in token_types
        assert TokenType.NETWORK in token_types
        assert TokenType.CONFIGURE in token_types
        assert TokenType.TRAINING in token_types 