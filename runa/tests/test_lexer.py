"""
Tests for the Runa lexer.

This module contains tests for the Runa lexical analyzer (lexer).
"""

import pytest
from runa.src.lexer.lexer import Lexer, RunaLexicalError
from runa.src.lexer.tokens import TokenType, Token


def test_lexer_empty_string():
    """Test lexer with an empty string."""
    lexer = Lexer("")
    tokens = lexer.tokenize()
    assert len(tokens) == 1
    assert tokens[0].token_type == TokenType.EOF


def test_lexer_whitespace():
    """Test lexer with whitespace."""
    lexer = Lexer("   \t   \n   ")
    tokens = lexer.tokenize()
    assert len(tokens) >= 2  # At least NEWLINE and EOF
    assert tokens[-1].token_type == TokenType.EOF


def test_lexer_comments():
    """Test lexer with comments."""
    lexer = Lexer("# This is a comment\n# This is another comment")
    tokens = lexer.tokenize()
    
    # Find the comment tokens
    comment_tokens = [t for t in tokens if t.token_type == TokenType.COMMENT]
    assert len(comment_tokens) == 2
    assert comment_tokens[0].lexeme.strip() == "# This is a comment"
    assert comment_tokens[1].lexeme.strip() == "# This is another comment"


def test_lexer_string_literals():
    """Test lexer with string literals."""
    lexer = Lexer('"Hello, World!" \'Another string\'')
    tokens = lexer.tokenize()
    
    # Find the string tokens
    string_tokens = [t for t in tokens if t.token_type == TokenType.STRING]
    assert len(string_tokens) == 2
    assert string_tokens[0].value == "Hello, World!"
    assert string_tokens[1].value == "Another string"


def test_lexer_number_literals():
    """Test lexer with number literals."""
    lexer = Lexer("42 3.14 0.5")
    tokens = lexer.tokenize()
    
    # Find the number tokens
    number_tokens = [t for t in tokens if t.token_type == TokenType.NUMBER]
    assert len(number_tokens) == 3
    assert number_tokens[0].value == 42
    assert number_tokens[1].value == 3.14
    assert number_tokens[2].value == 0.5


def test_lexer_identifiers():
    """Test lexer with identifiers."""
    lexer = Lexer("x y123 user_name")
    tokens = lexer.tokenize()
    
    # Find the identifier tokens
    identifier_tokens = [t for t in tokens if t.token_type == TokenType.IDENTIFIER]
    assert len(identifier_tokens) == 3
    assert identifier_tokens[0].lexeme == "x"
    assert identifier_tokens[1].lexeme == "y123"
    assert identifier_tokens[2].lexeme == "user_name"


def test_lexer_multi_word_identifiers():
    """Test lexer with multi-word identifiers."""
    lexer = Lexer("user name")
    tokens = lexer.tokenize()
    
    # Check for multi-word identifiers
    identifier_tokens = [t for t in tokens if t.token_type == TokenType.IDENTIFIER]
    assert len(identifier_tokens) == 1
    assert identifier_tokens[0].lexeme == "user name"


def test_lexer_keywords():
    """Test lexer with keywords."""
    lexer = Lexer("Let If Process Return While For Each")
    tokens = lexer.tokenize()
    
    # Check for the keyword tokens
    assert tokens[0].token_type == TokenType.LET
    assert tokens[1].token_type == TokenType.IF
    assert tokens[2].token_type == TokenType.PROCESS
    assert tokens[3].token_type == TokenType.RETURN
    assert tokens[4].token_type == TokenType.WHILE
    assert tokens[5].token_type == TokenType.FOR
    assert tokens[6].token_type == TokenType.EACH


def test_lexer_punctuation():
    """Test lexer with punctuation."""
    lexer = Lexer("()[]{},.:;")
    tokens = lexer.tokenize()
    
    # Check for punctuation tokens
    assert tokens[0].token_type == TokenType.LEFT_PAREN
    assert tokens[1].token_type == TokenType.RIGHT_PAREN
    assert tokens[2].token_type == TokenType.LEFT_BRACKET
    assert tokens[3].token_type == TokenType.RIGHT_BRACKET
    assert tokens[4].token_type == TokenType.LEFT_BRACE
    assert tokens[5].token_type == TokenType.RIGHT_BRACE
    assert tokens[6].token_type == TokenType.COMMA
    assert tokens[7].token_type == TokenType.DOT
    assert tokens[8].token_type == TokenType.COLON


def test_lexer_indentation():
    """Test lexer with indentation."""
    lexer = Lexer("If x:\n    y\n    z\n")
    tokens = lexer.tokenize()
    
    # Find the indentation tokens
    token_types = [t.token_type for t in tokens]
    assert TokenType.INDENT in token_types
    assert TokenType.DEDENT in token_types


def test_lexer_operators():
    """Test lexer with operators."""
    lexer = Lexer("is greater than is less than is equal to is not equal to")
    tokens = lexer.tokenize()
    
    # Check for compound operators
    assert tokens[0].token_type == TokenType.IS
    assert tokens[0].lexeme == "is greater than"
    assert tokens[1].token_type == TokenType.IS
    assert tokens[1].lexeme == "is less than"
    assert tokens[2].token_type == TokenType.IS
    assert tokens[2].lexeme == "is equal to"
    assert tokens[3].token_type == TokenType.IS
    assert tokens[3].lexeme == "is not equal to"


def test_lexer_simple_program():
    """Test lexer with a simple program."""
    program = """
Let x be 42
If x is greater than 10:
    Display "x is greater than 10"
Otherwise:
    Display "x is not greater than 10"
"""
    lexer = Lexer(program)
    tokens = lexer.tokenize()
    
    # Check that we have the expected tokens
    token_types = [t.token_type for t in tokens]
    assert TokenType.LET in token_types
    assert TokenType.IDENTIFIER in token_types
    assert TokenType.BE in token_types
    assert TokenType.NUMBER in token_types
    assert TokenType.IF in token_types
    assert TokenType.IS in token_types
    assert TokenType.COLON in token_types
    assert TokenType.INDENT in token_types
    assert TokenType.DISPLAY in token_types
    assert TokenType.STRING in token_types
    assert TokenType.DEDENT in token_types
    assert TokenType.OTHERWISE in token_types
    assert TokenType.EOF in token_types


def test_lexer_error_unterminated_string():
    """Test lexer error handling for unterminated strings."""
    lexer = Lexer('"This string is not terminated')
    with pytest.raises(RunaLexicalError) as excinfo:
        lexer.tokenize()
    assert "Unterminated string" in str(excinfo.value)


def test_lexer_error_invalid_character():
    """Test lexer error handling for invalid characters."""
    lexer = Lexer("Let x be $")
    with pytest.raises(RunaLexicalError) as excinfo:
        lexer.tokenize()
    assert "Unexpected character" in str(excinfo.value)


def test_lexer_error_inconsistent_indentation():
    """Test lexer error handling for inconsistent indentation."""
    program = """
If x:
   y  # 3 spaces
    z  # 4 spaces
"""
    lexer = Lexer(program)
    with pytest.raises(RunaLexicalError) as excinfo:
        lexer.tokenize()
    assert "Inconsistent indentation" in str(excinfo.value)


def test_lexer_string_escape_sequences():
    """Test lexer handling of string escape sequences."""
    lexer = Lexer(r'"Hello\nWorld" "Tab\tCharacter" "Quote\"Character" "Backslash\\"')
    tokens = lexer.tokenize()
    
    # Find the string tokens
    string_tokens = [t for t in tokens if t.token_type == TokenType.STRING]
    assert len(string_tokens) == 4
    assert string_tokens[0].value == "Hello\nWorld"
    assert string_tokens[1].value == "Tab\tCharacter"
    assert string_tokens[2].value == 'Quote"Character'
    assert string_tokens[3].value == "Backslash\\"


def test_lexer_multiline_string():
    """Test lexer handling of multi-line strings."""
    lexer = Lexer('"This is a\nmulti-line\nstring"')
    tokens = lexer.tokenize()
    
    # Find the string tokens
    string_tokens = [t for t in tokens if t.token_type == TokenType.STRING]
    assert len(string_tokens) == 1
    assert string_tokens[0].value == "This is a\nmulti-line\nstring"


def test_lexer_position_tracking():
    """Test lexer position tracking."""
    lexer = Lexer("Let x be 42\nDisplay x")
    tokens = lexer.tokenize()
    
    # Check line and column information
    assert tokens[0].line == 1  # Let
    assert tokens[0].column == 1
    
    assert tokens[4].line == 2  # Display
    assert tokens[4].column == 1


def test_lexer_real_program(example_program):
    """Test lexer with a real Runa program."""
    lexer = Lexer(example_program)
    tokens = lexer.tokenize()
    
    # Verify we have all the expected token types
    token_types = [t.token_type for t in tokens]
    assert TokenType.LET in token_types
    assert TokenType.IDENTIFIER in token_types
    assert TokenType.BE in token_types
    assert TokenType.STRING in token_types
    assert TokenType.NUMBER in token_types
    assert TokenType.IF in token_types
    assert TokenType.IS in token_types
    assert TokenType.COLON in token_types
    assert TokenType.INDENT in token_types
    assert TokenType.DISPLAY in token_types
    assert TokenType.FOLLOWED in token_types
    assert TokenType.DEDENT in token_types
    assert TokenType.OTHERWISE in token_types
    assert TokenType.EOF in token_types


def test_lexer_complex_program(complex_program):
    """Test lexer with a complex Runa program."""
    lexer = Lexer(complex_program)
    tokens = lexer.tokenize()
    
    # Verify we have all the expected token types for a complex program
    token_types = set(t.token_type for t in tokens)
    
    # Check for function definition tokens
    assert TokenType.PROCESS in token_types
    assert TokenType.CALLED in token_types
    assert TokenType.THAT in token_types
    assert TokenType.TAKES in token_types
    assert TokenType.RETURN in token_types
    
    # Check for collection tokens
    assert TokenType.LIST in token_types
    assert TokenType.CONTAINING in token_types
    assert TokenType.DICTIONARY in token_types
    assert TokenType.WITH in token_types
    assert TokenType.AS in token_types
    
    # Check for loop tokens
    assert TokenType.FOR in token_types
    assert TokenType.EACH in token_types
    assert TokenType.IN in token_types
    
    # Check for operators
    assert TokenType.MULTIPLIED in token_types
    assert TokenType.PLUS in token_types
    assert TokenType.AT in token_types
    
    # Check for error handling tokens
    assert TokenType.TRY in token_types
    assert TokenType.CATCH in token_types 