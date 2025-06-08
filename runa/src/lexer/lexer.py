"""
Lexer for the Runa programming language.

This module implements a complete lexical analyzer for Runa, which converts
source code text into a stream of tokens for the parser.
"""

from typing import List, Optional, Dict, Tuple, Set
import re
from dataclasses import dataclass

from runa.src.lexer.tokens import Token, TokenType, KEYWORDS


class RunaLexicalError(Exception):
    """Exception raised for lexical errors in Runa source code."""
    
    def __init__(self, line: int, column: int, message: str, source_line: str = ""):
        self.line = line
        self.column = column
        self.message = message
        self.source_line = source_line
        
        # Format the error message with source line context if provided
        error_msg = f"Line {line}, column {column}: {message}"
        if source_line:
            # Add a caret pointing to the error position
            pointer = " " * (column - 1) + "^"
            error_msg += f"\n{source_line}\n{pointer}"
        
        super().__init__(error_msg)


@dataclass
class LexerPosition:
    """Tracks position in the source code for error reporting and token creation."""
    line: int = 1
    column: int = 1
    offset: int = 0


class Lexer:
    """
    Lexical analyzer for the Runa programming language.
    
    This class transforms Runa source code into a stream of tokens
    for further processing by the parser.
    """
    
    def __init__(self, source: str, filename: str = "<stdin>"):
        """
        Initialize the lexer with source code.
        
        Args:
            source: The Runa source code to tokenize
            filename: Name of the source file for error reporting
        """
        self.source = source
        self.filename = filename
        self.tokens: List[Token] = []
        self.source_lines = source.splitlines() if source else [""]
        
        # Position tracking
        self.start = 0
        self.current = 0
        self.line = 1
        self.column = 1
        self.indent_stack = [0]  # Stack to track indentation levels
        
        # Special handling for multi-word identifiers
        self.identifier_buffer: List[str] = []
        self.identifier_line = 0
        self.identifier_column = 0
        
        # Compound operators recognition
        self.compound_words: Dict[str, Set[str]] = {
            "is": {"greater", "less", "equal", "not"},
            "greater": {"than", "than or equal to"},
            "less": {"than", "than or equal to"},
            "equal": {"to"},
            "not": {"equal"},
            "multiplied": {"by"},
            "divided": {"by"},
            "followed": {"by"},
            "at": {"index"},
            "the": {"sum", "length"},
            "sum": {"of", "of all"},
            "length": {"of"},
            "all": {"in"},
        }
        
        # For handling multi-line strings and string escaping
        self.string_start_line = 0
        self.string_start_column = 0
    
    def tokenize(self) -> List[Token]:
        """
        Tokenize the source code.
        
        Returns:
            A list of Token objects representing the tokens in the source code
        
        Raises:
            RunaLexicalError: If an error occurs during tokenization
        """
        try:
            while not self._is_at_end():
                self.start = self.current
                self._scan_token()
            
            # Handle any remaining indentation at the end of the file
            while len(self.indent_stack) > 1:
                self.indent_stack.pop()
                self.tokens.append(Token(TokenType.DEDENT, "", None, self.line, self.column))
            
            # Add EOF token
            self.tokens.append(Token(TokenType.EOF, "", None, self.line, self.column))
            return self.tokens
            
        except RunaLexicalError as e:
            # Re-raise the exception
            raise
        except Exception as e:
            # Convert any unexpected errors to RunaLexicalError with position information
            source_line = self._get_current_line()
            raise RunaLexicalError(
                self.line, self.column, 
                f"Unexpected error during lexical analysis: {str(e)}", 
                source_line
            ) from e
    
    def _scan_token(self) -> None:
        """Scan a single token from the source code."""
        char = self._advance()
        
        # Handle whitespace
        if char == ' ' or char == '\t':
            return
        
        # Handle newlines and indentation
        if char == '\n':
            self.tokens.append(Token(TokenType.NEWLINE, '\n', None, self.line, self.column - 1))
            self.line += 1
            self.column = 1
            
            # Handle indentation
            indent_level = 0
            while self._peek() == ' ' or self._peek() == '\t':
                char = self._advance()
                if char == ' ':
                    indent_level += 1
                else:  # tab
                    indent_level += 4  # Count tabs as 4 spaces
            
            current_indent = self.indent_stack[-1]
            
            if indent_level > current_indent:
                # New indentation level
                self.indent_stack.append(indent_level)
                self.tokens.append(Token(TokenType.INDENT, " " * indent_level, None, self.line, 1))
            elif indent_level < current_indent:
                # Dedent (possibly multiple levels)
                while indent_level < self.indent_stack[-1]:
                    self.indent_stack.pop()
                    self.tokens.append(Token(TokenType.DEDENT, "", None, self.line, 1))
                
                if indent_level != self.indent_stack[-1]:
                    source_line = self._get_current_line()
                    raise RunaLexicalError(
                        self.line, self.column, 
                        f"Inconsistent indentation: {indent_level} spaces, expected {self.indent_stack[-1]}",
                        source_line
                    )
            
            return
        
        # Handle string literals
        if char == '"' or char == "'":
            self._string(char)
            return
        
        # Handle numbers
        if char.isdigit():
            self._number()
            return
        
        # Handle comments
        if char == '#':
            self._comment()
            return
        
        # Handle punctuation
        if char == ':':
            self._add_token(TokenType.COLON)
        elif char == ',':
            self._add_token(TokenType.COMMA)
        elif char == '.':
            self._add_token(TokenType.DOT)
        elif char == '[':
            self._add_token(TokenType.LEFT_BRACKET)
        elif char == ']':
            self._add_token(TokenType.RIGHT_BRACKET)
        elif char == '{':
            self._add_token(TokenType.LEFT_BRACE)
        elif char == '}':
            self._add_token(TokenType.RIGHT_BRACE)
        elif char == '(':
            self._add_token(TokenType.LEFT_PAREN)
        elif char == ')':
            self._add_token(TokenType.RIGHT_PAREN)
        
        # Handle identifiers and keywords
        elif char.isalpha() or char == '_':
            self._identifier()
        
        # Handle unknown characters
        else:
            source_line = self._get_current_line()
            raise RunaLexicalError(
                self.line, self.column - 1, 
                f"Unexpected character: '{char}'",
                source_line
            )
    
    def _string(self, quote_char: str) -> None:
        """
        Scan a string literal with support for escape sequences and multi-line strings.
        
        Args:
            quote_char: The character that started the string (single or double quote)
        """
        # Track starting position
        self.string_start_line = self.line
        self.string_start_column = self.column - 1
        escaped = False
        result = ""
        
        while True:
            if self._is_at_end():
                source_line = self._get_line(self.string_start_line)
                raise RunaLexicalError(
                    self.string_start_line, self.string_start_column, 
                    "Unterminated string.",
                    source_line
                )
                
            c = self._peek()
            
            # Handle end of string
            if c == quote_char and not escaped:
                self._advance()  # Consume the closing quote
                break
                
            # Handle escape sequences
            if c == '\\' and not escaped:
                escaped = True
                self._advance()
                continue
                
            if escaped:
                # Handle common escape sequences
                if c == 'n':
                    result += '\n'
                elif c == 't':
                    result += '\t'
                elif c == 'r':
                    result += '\r'
                elif c == '\\':
                    result += '\\'
                elif c == quote_char:
                    result += quote_char
                else:
                    # Unknown escape sequence
                    source_line = self._get_current_line()
                    raise RunaLexicalError(
                        self.line, self.column,
                        f"Invalid escape sequence: '\\{c}'",
                        source_line
                    )
                escaped = False
            else:
                # Regular character
                result += c
                
                # Handle newlines in multi-line strings
                if c == '\n':
                    self.line += 1
                    self.column = 0
            
            self._advance()
        
        self._add_token(TokenType.STRING, result)
    
    def _number(self) -> None:
        """Scan a number literal with support for different numeric formats."""
        # Scan integer part
        while self._peek().isdigit():
            self._advance()
        
        # Check for decimal part
        if self._peek() == '.' and self._peek_next().isdigit():
            # Consume the decimal point
            self._advance()
            
            # Scan fractional part
            while self._peek().isdigit():
                self._advance()
        
        # Check for exponential notation (e.g., 1e6, 1.5e-3)
        if self._peek().lower() == 'e':
            # Consume the 'e'
            self._advance()
            
            # Check for sign
            if self._peek() in ['+', '-']:
                self._advance()
            
            # Ensure there are digits in the exponent
            if not self._peek().isdigit():
                source_line = self._get_current_line()
                raise RunaLexicalError(
                    self.line, self.column,
                    "Expected digits after exponent.",
                    source_line
                )
            
            # Scan exponent part
            while self._peek().isdigit():
                self._advance()
        
        # Parse the number
        value_str = self.source[self.start:self.current]
        try:
            # Try to convert to float first, then to int if it's a whole number
            value = float(value_str)
            if value.is_integer() and 'e' not in value_str.lower() and '.' not in value_str:
                value = int(value)
        except ValueError:
            source_line = self._get_current_line()
            raise RunaLexicalError(
                self.line, self.column,
                f"Invalid number format: {value_str}",
                source_line
            )
        
        self._add_token(TokenType.NUMBER, value)
    
    def _identifier(self) -> None:
        """
        Scan an identifier or keyword with support for multi-word identifiers.
        
        Handles complex multi-word identifiers and compound operators.
        """
        # If we're continuing a multi-word identifier
        if self.identifier_buffer:
            # Check if this is a continuation (after a space)
            if self.current >= 2 and self.source[self.current - 2] == ' ':
                # Continue building the identifier
                while self._peek().isalnum() or self._peek() == '_':
                    self._advance()
                
                word = self.source[self.start:self.current]
                self.identifier_buffer.append(word)
                
                # Check if this could be part of a compound operator
                if len(self.identifier_buffer) >= 2:
                    first_word = self.identifier_buffer[0].lower()
                    joined_rest = " ".join(self.identifier_buffer[1:]).lower()
                    
                    if first_word in self.compound_words and joined_rest in self.compound_words[first_word]:
                        # This is a compound operator, not a multi-word identifier
                        compound_op = " ".join(self.identifier_buffer).lower()
                        
                        # Map to specific token types based on the compound
                        if compound_op == "is greater than":
                            self._add_token_at_position(TokenType.IS, "is greater than", None, 
                                                      self.identifier_line, self.identifier_column)
                        elif compound_op == "is less than":
                            self._add_token_at_position(TokenType.IS, "is less than", None, 
                                                      self.identifier_line, self.identifier_column)
                        elif compound_op == "is equal to":
                            self._add_token_at_position(TokenType.IS, "is equal to", None, 
                                                      self.identifier_line, self.identifier_column)
                        elif compound_op == "is not equal to":
                            self._add_token_at_position(TokenType.IS, "is not equal to", None, 
                                                      self.identifier_line, self.identifier_column)
                        elif compound_op == "greater than or equal to":
                            self._add_token_at_position(TokenType.GREATER, "greater than or equal to", None, 
                                                      self.identifier_line, self.identifier_column)
                        elif compound_op == "less than or equal to":
                            self._add_token_at_position(TokenType.LESS, "less than or equal to", None, 
                                                      self.identifier_line, self.identifier_column)
                        elif compound_op == "multiplied by":
                            self._add_token_at_position(TokenType.MULTIPLIED, "multiplied by", None, 
                                                      self.identifier_line, self.identifier_column)
                        elif compound_op == "divided by":
                            self._add_token_at_position(TokenType.DIVIDED, "divided by", None, 
                                                      self.identifier_line, self.identifier_column)
                        elif compound_op == "followed by":
                            self._add_token_at_position(TokenType.FOLLOWED, "followed by", None, 
                                                      self.identifier_line, self.identifier_column)
                        elif compound_op == "at index":
                            self._add_token_at_position(TokenType.AT, "at index", None, 
                                                      self.identifier_line, self.identifier_column)
                        elif compound_op == "the sum of":
                            self._add_token_at_position(TokenType.SUM, "the sum of", None, 
                                                      self.identifier_line, self.identifier_column)
                        elif compound_op == "the sum of all":
                            self._add_token_at_position(TokenType.SUM, "the sum of all", None, 
                                                      self.identifier_line, self.identifier_column)
                        elif compound_op == "the length of":
                            self._add_token_at_position(TokenType.LENGTH, "the length of", None, 
                                                      self.identifier_line, self.identifier_column)
                        else:
                            # Check if part of it is a keyword
                            keyword_found = False
                            for i in range(len(self.identifier_buffer)):
                                word_to_check = self.identifier_buffer[i].lower()
                                if word_to_check in KEYWORDS:
                                    # Process the keyword
                                    self._add_token_at_position(
                                        KEYWORDS[word_to_check], 
                                        self.identifier_buffer[i], 
                                        None,
                                        self.identifier_line, 
                                        self.identifier_column
                                    )
                                    keyword_found = True
                                    break
                            
                            if not keyword_found:
                                # Default to treating it as a multi-word identifier
                                identifier = " ".join(self.identifier_buffer)
                                self._add_token_at_position(
                                    TokenType.IDENTIFIER, 
                                    identifier, 
                                    None,
                                    self.identifier_line, 
                                    self.identifier_column
                                )
                        
                        self.identifier_buffer = []
                        return
                
                # Check if the next character is a space and if the following is alphabetic or underscore
                if self._peek() == ' ' and (self._peek_next().isalpha() or self._peek_next() == '_'):
                    return  # Continue building the identifier
                
                # Not continuing, combine the buffered words into a single identifier
                identifier = " ".join(self.identifier_buffer)
                self._add_token_at_position(
                    TokenType.IDENTIFIER, 
                    identifier, 
                    None,
                    self.identifier_line, 
                    self.identifier_column
                )
                self.identifier_buffer = []
                return
            else:
                # Not a continuation, process the buffered identifier
                identifier = " ".join(self.identifier_buffer)
                self._add_token_at_position(
                    TokenType.IDENTIFIER, 
                    identifier, 
                    None,
                    self.identifier_line, 
                    self.identifier_column
                )
                self.identifier_buffer = []
                # Continue to process the current character
        
        # Process a normal identifier
        while self._peek().isalnum() or self._peek() == '_':
            self._advance()
        
        # Extract the text
        text = self.source[self.start:self.current]
        
        # Check if it's a keyword
        text_lower = text.lower()
        if text_lower in KEYWORDS:
            self._add_token(KEYWORDS[text_lower])
        else:
            # Save the start of a potential multi-word identifier
            if self._peek() == ' ' and (self._peek_next().isalpha() or self._peek_next() == '_'):
                self.identifier_buffer = [text]
                self.identifier_line = self.line
                self.identifier_column = self.column - len(text)
            else:
                self._add_token(TokenType.IDENTIFIER)
    
    def _comment(self) -> None:
        """Scan a comment."""
        # Scan until the end of the line
        while self._peek() != '\n' and not self._is_at_end():
            self._advance()
        
        # Extract the comment text
        text = self.source[self.start:self.current].strip()
        self._add_token(TokenType.COMMENT, text)
    
    def _add_token(self, token_type: TokenType, literal: Optional[object] = None) -> None:
        """
        Add a token to the token list.
        
        Args:
            token_type: The type of token
            literal: The literal value for the token (for strings, numbers, etc.)
        """
        text = self.source[self.start:self.current]
        self.tokens.append(
            Token(token_type, text, literal, self.line, self.column - len(text))
        )
    
    def _add_token_at_position(
        self, 
        token_type: TokenType, 
        lexeme: str, 
        literal: Optional[object], 
        line: int, 
        column: int
    ) -> None:
        """
        Add a token with a specific position.
        
        Args:
            token_type: The type of token
            lexeme: The text of the token
            literal: The literal value for the token
            line: The line number
            column: The column number
        """
        self.tokens.append(Token(token_type, lexeme, literal, line, column))
    
    def _advance(self) -> str:
        """
        Advance to the next character and return the current one.
        
        Returns:
            The current character
        """
        char = self.source[self.current]
        self.current += 1
        self.column += 1
        return char
    
    def _peek(self) -> str:
        """
        Look at the current character without advancing.
        
        Returns:
            The current character, or '\0' if at the end of the source
        """
        if self._is_at_end():
            return '\0'
        return self.source[self.current]
    
    def _peek_next(self) -> str:
        """
        Look at the next character without advancing.
        
        Returns:
            The next character, or '\0' if at the end of the source
        """
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]
    
    def _is_at_end(self) -> bool:
        """
        Check if we've reached the end of the source.
        
        Returns:
            True if at the end of the source, False otherwise
        """
        return self.current >= len(self.source)
    
    def _get_current_line(self) -> str:
        """
        Get the current line of source code for error reporting.
        
        Returns:
            The current line of source code
        """
        return self._get_line(self.line)
    
    def _get_line(self, line_number: int) -> str:
        """
        Get a specific line of source code for error reporting.
        
        Args:
            line_number: The 1-based line number to retrieve
            
        Returns:
            The specified line of source code
        """
        if 1 <= line_number <= len(self.source_lines):
            return self.source_lines[line_number - 1]
        return "" 