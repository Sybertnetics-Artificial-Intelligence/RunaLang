#!/usr/bin/env python3
"""
TOML Parser - Complete lexer and parser for TOML (Tom's Obvious Minimal Language)

Provides comprehensive parsing capabilities for TOML including:
- Basic values: strings, integers, floats, booleans, dates/times
- Collections: arrays and tables (including inline tables)
- Table structure with dotted keys and table arrays
- Comments and documentation
- Different string types (basic, multi-line, literal)
- Date/time formats (RFC 3339)

Supports TOML v1.0.0 specification.
"""

import re
from typing import List, Dict, Optional, Any, Union, Tuple
from enum import Enum
from dataclasses import dataclass
from datetime import datetime, date, time

from .toml_ast import *


class TokenType(Enum):
    """TOML token types"""
    # Literals
    IDENTIFIER = "IDENTIFIER"
    BARE_KEY = "BARE_KEY"
    QUOTED_KEY = "QUOTED_KEY"
    
    # String types
    BASIC_STRING = "BASIC_STRING"
    LITERAL_STRING = "LITERAL_STRING"
    MULTILINE_BASIC_STRING = "MULTILINE_BASIC_STRING"
    MULTILINE_LITERAL_STRING = "MULTILINE_LITERAL_STRING"
    
    # Numbers
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    
    # Booleans
    BOOL_TRUE = "true"
    BOOL_FALSE = "false"
    
    # Date/Time
    DATETIME = "DATETIME"
    DATE = "DATE"
    TIME = "TIME"
    
    # Punctuation
    DOT = "."
    COMMA = ","
    EQUAL = "="
    
    # Brackets
    LEFT_BRACKET = "["
    RIGHT_BRACKET = "]"
    LEFT_BRACE = "{"
    RIGHT_BRACE = "}"
    
    # Table headers
    TABLE_START = "["
    TABLE_END = "]"
    ARRAY_TABLE_START = "[["
    ARRAY_TABLE_END = "]]"
    
    # Special
    NEWLINE = "NEWLINE"
    WHITESPACE = "WHITESPACE"
    COMMENT = "COMMENT"
    EOF = "EOF"


@dataclass
class Token:
    """TOML token representation"""
    type: TokenType
    value: str
    line: int
    column: int
    file: Optional[str] = None


class TOMLLexer:
    """TOML lexer for tokenizing TOML source code"""
    
    KEYWORDS = {
        "true": TokenType.BOOL_TRUE,
        "false": TokenType.BOOL_FALSE,
    }
    
    # Date/time patterns (RFC 3339)
    DATETIME_PATTERN = re.compile(
        r'\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?'
    )
    DATE_PATTERN = re.compile(r'\d{4}-\d{2}-\d{2}')
    TIME_PATTERN = re.compile(r'\d{2}:\d{2}:\d{2}(?:\.\d+)?')
    
    # Number patterns
    INTEGER_PATTERN = re.compile(r'[+-]?(?:0|[1-9](?:[0-9_]*[0-9])?)(?:[eE][+-]?[0-9]+)?')
    FLOAT_PATTERN = re.compile(r'[+-]?(?:0|[1-9](?:[0-9_]*[0-9])?)(?:\.[0-9_]*[0-9])?(?:[eE][+-]?[0-9]+)?')
    
    # Special float values
    SPECIAL_FLOATS = {
        'inf': float('inf'),
        '+inf': float('inf'),
        '-inf': float('-inf'),
        'nan': float('nan'),
        '+nan': float('nan'),
        '-nan': float('nan'),
    }
    
    def __init__(self, source: str, filename: Optional[str] = None):
        self.source = source
        self.filename = filename
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
    
    def tokenize(self) -> List[Token]:
        """Tokenize the source code"""
        while self.position < len(self.source):
            if not self._match_token():
                char = self.source[self.position] if self.position < len(self.source) else 'EOF'
                raise SyntaxError(f"Unexpected character '{char}' "
                                f"at line {self.line}, column {self.column}")
        
        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column, self.filename))
        return self.tokens
    
    def _match_token(self) -> bool:
        """Match and consume a token"""
        if self._at_end():
            return False
        
        # Skip whitespace
        if self._match_whitespace():
            return True
        
        # Comments
        if self._peek() == '#':
            self._handle_comment()
            return True
        
        # Newlines
        if self._peek() == '\n':
            self._add_token(TokenType.NEWLINE, '\n')
            self._advance()
            return True
        
        # Array table start [[
        if self._peek() == '[' and self._peek_next() == '[':
            self._add_token(TokenType.ARRAY_TABLE_START, '[[')
            self._advance()
            self._advance()
            return True
        
        # Table start [
        if self._peek() == '[':
            self._add_token(TokenType.TABLE_START, '[')
            self._advance()
            return True
        
        # Table/array end ]
        if self._peek() == ']':
            # Check for array table end ]]
            if self._peek_next() == ']':
                self._add_token(TokenType.ARRAY_TABLE_END, ']]')
                self._advance()
                self._advance()
            else:
                self._add_token(TokenType.TABLE_END, ']')
                self._advance()
            return True
        
        # Inline table braces
        if self._peek() == '{':
            self._add_token(TokenType.LEFT_BRACE, '{')
            self._advance()
            return True
        
        if self._peek() == '}':
            self._add_token(TokenType.RIGHT_BRACE, '}')
            self._advance()
            return True
        
        # Basic punctuation
        if self._peek() == '=':
            self._add_token(TokenType.EQUAL, '=')
            self._advance()
            return True
        
        if self._peek() == '.':
            self._add_token(TokenType.DOT, '.')
            self._advance()
            return True
        
        if self._peek() == ',':
            self._add_token(TokenType.COMMA, ',')
            self._advance()
            return True
        
        # Strings
        if self._peek() == '"':
            return self._handle_basic_string()
        
        if self._peek() == "'":
            return self._handle_literal_string()
        
        # Numbers, dates, booleans, and bare keys
        return self._handle_value_or_key()
    
    def _match_whitespace(self) -> bool:
        """Match whitespace (except newlines)"""
        start = self.position
        while not self._at_end() and self._peek() in ' \t\r':
            self._advance()
        
        if self.position > start:
            return True
        return False
    
    def _handle_comment(self) -> None:
        """Handle comment starting with #"""
        start = self.position
        self._advance()  # Skip #
        
        while not self._at_end() and self._peek() != '\n':
            self._advance()
        
        comment_text = self.source[start+1:self.position]
        self._add_token(TokenType.COMMENT, comment_text)
    
    def _handle_basic_string(self) -> bool:
        """Handle basic string (quoted with ")"""
        if self._peek() == '"' and self._peek_next() == '"' and self._peek_offset(2) == '"':
            return self._handle_multiline_basic_string()
        
        start = self.position
        self._advance()  # Skip opening quote
        
        value = ""
        while not self._at_end() and self._peek() != '"':
            if self._peek() == '\\':
                self._advance()
                if self._at_end():
                    raise SyntaxError(f"Unterminated string at line {self.line}")
                
                # Handle escape sequences
                escape_char = self._peek()
                if escape_char in '"\\bnfrt':
                    escape_map = {
                        '"': '"', '\\': '\\', 'b': '\b', 'n': '\n',
                        'f': '\f', 'r': '\r', 't': '\t'
                    }
                    value += escape_map[escape_char]
                elif escape_char == 'u':
                    # Unicode escape \uXXXX
                    self._advance()
                    unicode_digits = self._read_n_chars(4)
                    value += chr(int(unicode_digits, 16))
                    continue
                elif escape_char == 'U':
                    # Unicode escape \UXXXXXXXX
                    self._advance()
                    unicode_digits = self._read_n_chars(8)
                    value += chr(int(unicode_digits, 16))
                    continue
                else:
                    raise SyntaxError(f"Invalid escape sequence \\{escape_char} at line {self.line}")
                self._advance()
            else:
                value += self._peek()
                self._advance()
        
        if self._at_end():
            raise SyntaxError(f"Unterminated string at line {self.line}")
        
        self._advance()  # Skip closing quote
        self._add_token(TokenType.BASIC_STRING, value)
        return True
    
    def _handle_multiline_basic_string(self) -> bool:
        """Handle multiline basic string (""")"""
        start_line = self.line
        self._advance()  # Skip first "
        self._advance()  # Skip second "
        self._advance()  # Skip third "
        
        # Skip immediate newline if present
        if self._peek() == '\n':
            self._advance()
        
        value = ""
        while not self._at_end():
            if self._peek() == '"' and self._peek_next() == '"' and self._peek_offset(2) == '"':
                self._advance()  # Skip first "
                self._advance()  # Skip second "
                self._advance()  # Skip third "
                break
            
            if self._peek() == '\\':
                self._advance()
                if self._peek() == '\n':
                    # Line ending backslash - trim whitespace
                    self._advance()
                    while not self._at_end() and self._peek() in ' \t\n':
                        self._advance()
                    continue
                
                # Handle other escape sequences same as basic string
                if self._at_end():
                    raise SyntaxError(f"Unterminated string starting at line {start_line}")
                
                escape_char = self._peek()
                if escape_char in '"\\bnfrt':
                    escape_map = {
                        '"': '"', '\\': '\\', 'b': '\b', 'n': '\n',
                        'f': '\f', 'r': '\r', 't': '\t'
                    }
                    value += escape_map[escape_char]
                elif escape_char == 'u':
                    self._advance()
                    unicode_digits = self._read_n_chars(4)
                    value += chr(int(unicode_digits, 16))
                    continue
                elif escape_char == 'U':
                    self._advance()
                    unicode_digits = self._read_n_chars(8)
                    value += chr(int(unicode_digits, 16))
                    continue
                self._advance()
            else:
                value += self._peek()
                self._advance()
        else:
            raise SyntaxError(f"Unterminated multiline string starting at line {start_line}")
        
        self._add_token(TokenType.MULTILINE_BASIC_STRING, value)
        return True
    
    def _handle_literal_string(self) -> bool:
        """Handle literal string (quoted with ')"""
        if self._peek() == "'" and self._peek_next() == "'" and self._peek_offset(2) == "'":
            return self._handle_multiline_literal_string()
        
        start = self.position
        self._advance()  # Skip opening quote
        
        value = ""
        while not self._at_end() and self._peek() != "'":
            value += self._peek()
            self._advance()
        
        if self._at_end():
            raise SyntaxError(f"Unterminated literal string at line {self.line}")
        
        self._advance()  # Skip closing quote
        self._add_token(TokenType.LITERAL_STRING, value)
        return True
    
    def _handle_multiline_literal_string(self) -> bool:
        """Handle multiline literal string (''')"""
        start_line = self.line
        self._advance()  # Skip first '
        self._advance()  # Skip second '
        self._advance()  # Skip third '
        
        # Skip immediate newline if present
        if self._peek() == '\n':
            self._advance()
        
        value = ""
        while not self._at_end():
            if self._peek() == "'" and self._peek_next() == "'" and self._peek_offset(2) == "'":
                self._advance()  # Skip first '
                self._advance()  # Skip second '
                self._advance()  # Skip third '
                break
            
            value += self._peek()
            self._advance()
        else:
            raise SyntaxError(f"Unterminated multiline literal string starting at line {start_line}")
        
        self._add_token(TokenType.MULTILINE_LITERAL_STRING, value)
        return True
    
    def _handle_value_or_key(self) -> bool:
        """Handle numbers, dates, booleans, or bare keys"""
        start = self.position
        
        # Read until delimiter
        while (not self._at_end() and 
               self._peek() not in ' \t\n\r#=,.[]{}'):
            self._advance()
        
        if self.position == start:
            return False
        
        value = self.source[start:self.position]
        
        # Try to parse as date/time first
        if self._try_parse_datetime(value):
            return True
        
        # Try to parse as number
        if self._try_parse_number(value):
            return True
        
        # Try to parse as boolean
        if value in self.KEYWORDS:
            self._add_token(self.KEYWORDS[value], value)
            return True
        
        # Special float values
        if value in self.SPECIAL_FLOATS:
            self._add_token(TokenType.FLOAT, value)
            return True
        
        # Otherwise it's a bare key
        if self._is_valid_bare_key(value):
            self._add_token(TokenType.BARE_KEY, value)
            return True
        
        return False
    
    def _try_parse_datetime(self, value: str) -> bool:
        """Try to parse as date/time"""
        if self.DATETIME_PATTERN.fullmatch(value):
            self._add_token(TokenType.DATETIME, value)
            return True
        elif self.DATE_PATTERN.fullmatch(value):
            self._add_token(TokenType.DATE, value)
            return True
        elif self.TIME_PATTERN.fullmatch(value):
            self._add_token(TokenType.TIME, value)
            return True
        return False
    
    def _try_parse_number(self, value: str) -> bool:
        """Try to parse as number"""
        # Remove underscores for parsing
        clean_value = value.replace('_', '')
        
        try:
            # Check for hex, oct, bin
            if value.startswith('0x'):
                int(clean_value, 16)
                self._add_token(TokenType.INTEGER, value)
                return True
            elif value.startswith('0o'):
                int(clean_value, 8)
                self._add_token(TokenType.INTEGER, value)
                return True
            elif value.startswith('0b'):
                int(clean_value, 2)
                self._add_token(TokenType.INTEGER, value)
                return True
            
            # Try integer first
            if '.' not in clean_value and 'e' not in clean_value.lower():
                int(clean_value)
                self._add_token(TokenType.INTEGER, value)
                return True
            
            # Try float
            float(clean_value)
            self._add_token(TokenType.FLOAT, value)
            return True
            
        except ValueError:
            pass
        
        return False
    
    def _is_valid_bare_key(self, value: str) -> bool:
        """Check if value is a valid bare key"""
        if not value:
            return False
        
        # Bare keys can contain A-Z, a-z, 0-9, -, _
        return all(c.isalnum() or c in '-_' for c in value)
    
    def _read_n_chars(self, n: int) -> str:
        """Read n characters"""
        chars = ""
        for _ in range(n):
            if self._at_end():
                raise SyntaxError(f"Unexpected end of input")
            chars += self._peek()
            self._advance()
        return chars
    
    def _peek(self) -> str:
        """Peek at current character"""
        if self._at_end():
            return '\0'
        return self.source[self.position]
    
    def _peek_next(self) -> str:
        """Peek at next character"""
        return self._peek_offset(1)
    
    def _peek_offset(self, offset: int) -> str:
        """Peek at character at offset"""
        pos = self.position + offset
        if pos >= len(self.source):
            return '\0'
        return self.source[pos]
    
    def _advance(self) -> str:
        """Advance position and return current character"""
        if self._at_end():
            return '\0'
        
        char = self.source[self.position]
        self.position += 1
        
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        
        return char
    
    def _at_end(self) -> bool:
        """Check if at end of source"""
        return self.position >= len(self.source)
    
    def _add_token(self, token_type: TokenType, value: str) -> None:
        """Add token to list"""
        token = Token(token_type, value, self.line, self.column, self.filename)
        self.tokens.append(token)


class ParseError(Exception):
    """TOML parsing error"""
    
    def __init__(self, message: str, token: Optional[Token] = None):
        self.message = message
        self.token = token
        super().__init__(self._format_message())
    
    def _format_message(self) -> str:
        if self.token:
            return f"{self.message} at line {self.token.line}, column {self.token.column}"
        return self.message


class TOMLParser:
    """TOML parser using recursive descent"""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = [t for t in tokens if t.type not in (TokenType.WHITESPACE,)]
        self.current = 0
    
    def parse(self) -> TOMLDocument:
        """Parse tokens into TOML document"""
        items = []
        
        while not self._is_at_end():
            # Skip newlines and comments at top level
            if self._check(TokenType.NEWLINE):
                self._advance()
                continue
            
            if self._check(TokenType.COMMENT):
                comment = TOMLComment(text=self._advance().value)
                items.append(comment)
                continue
            
            # Parse table headers or key-value pairs
            if self._check(TokenType.ARRAY_TABLE_START):
                table = self._parse_array_table()
                items.append(table)
            elif self._check(TokenType.TABLE_START):
                table = self._parse_table()
                items.append(table)
            else:
                # Key-value pair
                kv = self._parse_key_value()
                items.append(kv)
        
        return TOMLDocument(items=items)
    
    def _parse_table(self) -> TOMLTable:
        """Parse table header [table.name]"""
        self._consume(TokenType.TABLE_START, "Expected '['")
        key = self._parse_key()
        self._consume(TokenType.TABLE_END, "Expected ']'")
        
        return TOMLTable(key=key, is_array_table=False)
    
    def _parse_array_table(self) -> TOMLTable:
        """Parse array table header [[table.name]]"""
        self._consume(TokenType.ARRAY_TABLE_START, "Expected '[['")
        key = self._parse_key()
        self._consume(TokenType.ARRAY_TABLE_END, "Expected ']]'")
        
        return TOMLTable(key=key, is_array_table=True)
    
    def _parse_key_value(self) -> TOMLKeyValue:
        """Parse key = value"""
        key = self._parse_key()
        self._consume(TokenType.EQUAL, "Expected '='")
        value = self._parse_value()
        
        return TOMLKeyValue(key=key, value=value)
    
    def _parse_key(self) -> TOMLKey:
        """Parse key (possibly dotted)"""
        parts = []
        is_quoted = []
        
        # First part
        if self._check(TokenType.BARE_KEY):
            parts.append(self._advance().value)
            is_quoted.append(False)
        elif self._check(TokenType.BASIC_STRING):
            parts.append(self._advance().value)
            is_quoted.append(True)
        elif self._check(TokenType.LITERAL_STRING):
            parts.append(self._advance().value)
            is_quoted.append(True)
        else:
            raise ParseError("Expected key", self._peek())
        
        # Additional dotted parts
        while self._match(TokenType.DOT):
            if self._check(TokenType.BARE_KEY):
                parts.append(self._advance().value)
                is_quoted.append(False)
            elif self._check(TokenType.BASIC_STRING):
                parts.append(self._advance().value)
                is_quoted.append(True)
            elif self._check(TokenType.LITERAL_STRING):
                parts.append(self._advance().value)
                is_quoted.append(True)
            else:
                raise ParseError("Expected key after '.'", self._peek())
        
        return TOMLKey(parts=parts, is_quoted=is_quoted)
    
    def _parse_value(self) -> TOMLValue:
        """Parse a value"""
        if self._check(TokenType.BASIC_STRING):
            value = self._advance().value
            return TOMLString(value=value, string_type=TOMLStringType.BASIC)
        
        if self._check(TokenType.LITERAL_STRING):
            value = self._advance().value
            return TOMLString(value=value, string_type=TOMLStringType.LITERAL)
        
        if self._check(TokenType.MULTILINE_BASIC_STRING):
            value = self._advance().value
            return TOMLString(value=value, string_type=TOMLStringType.MULTILINE_BASIC)
        
        if self._check(TokenType.MULTILINE_LITERAL_STRING):
            value = self._advance().value
            return TOMLString(value=value, string_type=TOMLStringType.MULTILINE_LITERAL)
        
        if self._check(TokenType.INTEGER):
            token = self._advance()
            value = self._parse_integer_value(token.value)
            return TOMLInteger(value=value, raw_text=token.value)
        
        if self._check(TokenType.FLOAT):
            token = self._advance()
            value = self._parse_float_value(token.value)
            return TOMLFloat(value=value, raw_text=token.value)
        
        if self._check(TokenType.BOOL_TRUE):
            self._advance()
            return TOMLBoolean(value=True)
        
        if self._check(TokenType.BOOL_FALSE):
            self._advance()
            return TOMLBoolean(value=False)
        
        if self._check(TokenType.DATETIME):
            token = self._advance()
            dt = self._parse_datetime_value(token.value)
            return TOMLDateTime(value=dt, raw_text=token.value)
        
        if self._check(TokenType.DATE):
            token = self._advance()
            d = self._parse_date_value(token.value)
            return TOMLDate(value=d, raw_text=token.value)
        
        if self._check(TokenType.TIME):
            token = self._advance()
            t = self._parse_time_value(token.value)
            return TOMLTime(value=t, raw_text=token.value)
        
        if self._check(TokenType.LEFT_BRACKET):
            return self._parse_array()
        
        if self._check(TokenType.LEFT_BRACE):
            return self._parse_inline_table()
        
        raise ParseError("Expected value", self._peek())
    
    def _parse_array(self) -> TOMLArray:
        """Parse array [...]"""
        self._consume(TokenType.LEFT_BRACKET, "Expected '['")
        
        elements = []
        is_multiline = False
        
        while not self._check(TokenType.RIGHT_BRACKET) and not self._is_at_end():
            if self._check(TokenType.NEWLINE):
                is_multiline = True
                self._advance()
                continue
            
            if self._check(TokenType.COMMENT):
                self._advance()
                continue
            
            value = self._parse_value()
            elements.append(value)
            
            if self._match(TokenType.COMMA):
                continue
            elif self._check(TokenType.RIGHT_BRACKET):
                break
            else:
                raise ParseError("Expected ',' or ']' in array", self._peek())
        
        self._consume(TokenType.RIGHT_BRACKET, "Expected ']'")
        
        return TOMLArray(elements=elements, is_multiline=is_multiline)
    
    def _parse_inline_table(self) -> TOMLInlineTable:
        """Parse inline table {...}"""
        self._consume(TokenType.LEFT_BRACE, "Expected '{'")
        
        pairs = []
        
        while not self._check(TokenType.RIGHT_BRACE) and not self._is_at_end():
            key = self._parse_key()
            self._consume(TokenType.EQUAL, "Expected '='")
            value = self._parse_value()
            
            pairs.append((key.dotted_key, value))
            
            if self._match(TokenType.COMMA):
                continue
            elif self._check(TokenType.RIGHT_BRACE):
                break
            else:
                raise ParseError("Expected ',' or '}' in inline table", self._peek())
        
        self._consume(TokenType.RIGHT_BRACE, "Expected '}'")
        
        return TOMLInlineTable(pairs=pairs)
    
    def _parse_integer_value(self, text: str) -> int:
        """Parse integer from text"""
        clean_text = text.replace('_', '')
        
        if text.startswith('0x'):
            return int(clean_text, 16)
        elif text.startswith('0o'):
            return int(clean_text, 8)
        elif text.startswith('0b'):
            return int(clean_text, 2)
        else:
            return int(clean_text)
    
    def _parse_float_value(self, text: str) -> float:
        """Parse float from text"""
        if text in TOMLLexer.SPECIAL_FLOATS:
            return TOMLLexer.SPECIAL_FLOATS[text]
        
        clean_text = text.replace('_', '')
        return float(clean_text)
    
    def _parse_datetime_value(self, text: str) -> datetime:
        """Parse datetime from text"""
        # Handle different datetime formats
        try:
            # Try with 'T' separator
            if 'T' in text:
                if text.endswith('Z'):
                    return datetime.fromisoformat(text.replace('Z', '+00:00'))
                else:
                    return datetime.fromisoformat(text)
            # Try with space separator
            else:
                return datetime.fromisoformat(text.replace(' ', 'T'))
        except ValueError:
            raise ParseError(f"Invalid datetime format: {text}")
    
    def _parse_date_value(self, text: str) -> date:
        """Parse date from text"""
        try:
            return date.fromisoformat(text)
        except ValueError:
            raise ParseError(f"Invalid date format: {text}")
    
    def _parse_time_value(self, text: str) -> time:
        """Parse time from text"""
        try:
            return time.fromisoformat(text)
        except ValueError:
            raise ParseError(f"Invalid time format: {text}")
    
    def _match(self, *types: TokenType) -> bool:
        """Check if current token matches any of the given types and advance"""
        for token_type in types:
            if self._check(token_type):
                self._advance()
                return True
        return False
    
    def _check(self, token_type: TokenType) -> bool:
        """Check if current token is of given type"""
        if self._is_at_end():
            return False
        return self._peek().type == token_type
    
    def _advance(self) -> Token:
        """Consume current token and return it"""
        if not self._is_at_end():
            self.current += 1
        return self._previous()
    
    def _is_at_end(self) -> bool:
        """Check if at end of tokens"""
        return self._peek().type == TokenType.EOF
    
    def _peek(self) -> Token:
        """Return current token"""
        return self.tokens[self.current]
    
    def _previous(self) -> Token:
        """Return previous token"""
        return self.tokens[self.current - 1]
    
    def _consume(self, token_type: TokenType, message: str) -> Token:
        """Consume token of expected type or raise error"""
        if self._check(token_type):
            return self._advance()
        
        raise ParseError(message, self._peek())


def parse_toml(source: str, filename: Optional[str] = None) -> TOMLDocument:
    """Parse TOML source code"""
    lexer = TOMLLexer(source, filename)
    tokens = lexer.tokenize()
    parser = TOMLParser(tokens)
    return parser.parse() 