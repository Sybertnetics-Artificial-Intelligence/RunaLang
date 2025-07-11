#!/usr/bin/env python3
"""
INI Parser - Complete lexer and parser for INI Configuration Files

Provides comprehensive parsing capabilities for INI files including:
- Section headers with square bracket syntax
- Key-value pairs with various delimiters (=, :)
- Comments with different prefixes (; #)
- Multi-line values and continuation
- Value type inference (string, number, boolean, list)
- Case sensitivity options
- Environment variable interpolation
- Include file directives
- Extended formats (Git config, systemd, etc.)

Supports standard INI, Windows INI, Git config, and systemd unit files.
"""

import re
import os
from typing import List, Dict, Optional, Any, Union, Tuple
from enum import Enum
from dataclasses import dataclass

from .ini_ast import *


class TokenType(Enum):
    """INI token types"""
    # Literals
    IDENTIFIER = "IDENTIFIER"
    STRING = "STRING"
    NUMBER = "NUMBER"
    BOOLEAN = "BOOLEAN"
    
    # Structure
    SECTION_START = "["
    SECTION_END = "]"
    EQUALS = "="
    COLON = ":"
    
    # Special
    COMMENT = "COMMENT"
    NEWLINE = "NEWLINE"
    WHITESPACE = "WHITESPACE"
    EOF = "EOF"
    
    # Extended
    INTERPOLATION_START = "${"
    INTERPOLATION_END = "}"
    CONTINUATION = "\\"
    INCLUDE = "include"


@dataclass
class Token:
    """INI token representation"""
    type: TokenType
    value: str
    line: int
    column: int
    file: Optional[str] = None


class INILexer:
    """INI lexer for tokenizing INI source code"""
    
    def __init__(self, source: str, filename: Optional[str] = None, 
                 comment_prefixes: Optional[List[str]] = None,
                 delimiters: Optional[List[str]] = None,
                 case_sensitive: bool = True):
        self.source = source
        self.filename = filename
        self.comment_prefixes = comment_prefixes or [';', '#']
        self.delimiters = delimiters or ['=', ':']
        self.case_sensitive = case_sensitive
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
    
    def tokenize(self) -> List[Token]:
        """Tokenize the source code"""
        while self.position < len(self.source):
            if not self._match_token():
                raise SyntaxError(f"Unexpected character '{self.source[self.position]}' "
                                f"at line {self.line}, column {self.column}")
        
        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column, self.filename))
        return self.tokens
    
    def _match_token(self) -> bool:
        """Try to match a token at current position"""
        remaining = self.source[self.position:]
        
        # Skip whitespace (except newlines)
        if self._match_whitespace():
            return True
        
        # Newlines
        if remaining.startswith('\n'):
            self._add_token(TokenType.NEWLINE, '\n')
            self._advance(1)
            return True
        
        if remaining.startswith('\r\n'):
            self._add_token(TokenType.NEWLINE, '\r\n')
            self._advance(2)
            return True
        
        # Comments
        for prefix in self.comment_prefixes:
            if remaining.startswith(prefix):
                return self._match_comment(prefix)
        
        # Section brackets
        if remaining.startswith('['):
            self._add_token(TokenType.SECTION_START, '[')
            self._advance(1)
            return True
        
        if remaining.startswith(']'):
            self._add_token(TokenType.SECTION_END, ']')
            self._advance(1)
            return True
        
        # Delimiters
        for delimiter in self.delimiters:
            if remaining.startswith(delimiter):
                if delimiter == '=':
                    self._add_token(TokenType.EQUALS, delimiter)
                elif delimiter == ':':
                    self._add_token(TokenType.COLON, delimiter)
                else:
                    self._add_token(TokenType.IDENTIFIER, delimiter)
                self._advance(len(delimiter))
                return True
        
        # Line continuation
        if remaining.startswith('\\'):
            self._add_token(TokenType.CONTINUATION, '\\')
            self._advance(1)
            return True
        
        # Interpolation
        if remaining.startswith('${'):
            self._add_token(TokenType.INTERPOLATION_START, '${')
            self._advance(2)
            return True
        
        if remaining.startswith('}'):
            self._add_token(TokenType.INTERPOLATION_END, '}')
            self._advance(1)
            return True
        
        # Quoted strings
        if remaining.startswith('"') or remaining.startswith("'"):
            return self._match_quoted_string()
        
        # Numbers
        if self._match_number():
            return True
        
        # Identifiers and unquoted values
        if self._match_identifier():
            return True
        
        return False
    
    def _match_whitespace(self) -> bool:
        """Match whitespace (but not newlines)"""
        start_pos = self.position
        while (self.position < len(self.source) and 
               self.source[self.position] in ' \t'):
            self.column += 1
            self.position += 1
        
        if self.position > start_pos:
            # Don't emit whitespace tokens for now
            return True
        return False
    
    def _match_comment(self, prefix: str) -> bool:
        """Match comment line"""
        start_pos = self.position
        
        # Skip comment prefix
        self.position += len(prefix)
        self.column += len(prefix)
        
        # Read until end of line
        while (self.position < len(self.source) and 
               self.source[self.position] not in '\n\r'):
            self.position += 1
            self.column += 1
        
        comment_text = self.source[start_pos + len(prefix):self.position].strip()
        self._add_token(TokenType.COMMENT, comment_text)
        return True
    
    def _match_quoted_string(self) -> bool:
        """Match quoted string"""
        quote_char = self.source[self.position]
        start_pos = self.position
        self.position += 1
        self.column += 1
        
        value = ""
        while self.position < len(self.source):
            char = self.source[self.position]
            
            if char == quote_char:
                # End of string
                self.position += 1
                self.column += 1
                self._add_token(TokenType.STRING, value)
                return True
            
            elif char == '\\' and self.position + 1 < len(self.source):
                # Escape sequence
                self.position += 1
                self.column += 1
                next_char = self.source[self.position]
                
                if next_char == 'n':
                    value += '\n'
                elif next_char == 't':
                    value += '\t'
                elif next_char == 'r':
                    value += '\r'
                elif next_char == '\\':
                    value += '\\'
                elif next_char == quote_char:
                    value += quote_char
                else:
                    value += next_char
                
                self.position += 1
                self.column += 1
            
            elif char == '\n':
                # Newline in string
                value += char
                self.line += 1
                self.column = 1
                self.position += 1
            
            else:
                value += char
                self.position += 1
                self.column += 1
        
        # Unterminated string
        raise SyntaxError(f"Unterminated string at line {self.line}")
    
    def _match_number(self) -> bool:
        """Match numeric literal"""
        remaining = self.source[self.position:]
        
        # Integer or float pattern
        number_pattern = r'^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?'
        match = re.match(number_pattern, remaining)
        
        if match:
            value = match.group(0)
            self._add_token(TokenType.NUMBER, value)
            self._advance(len(value))
            return True
        
        return False
    
    def _match_identifier(self) -> bool:
        """Match identifier or unquoted value"""
        start_pos = self.position
        
        # Read until delimiter, comment, or special character
        while self.position < len(self.source):
            char = self.source[self.position]
            
            # Stop at delimiters, brackets, comments, or newlines
            if (char in '=:[]#;\n\r' or 
                (self.position + 1 < len(self.source) and 
                 self.source[self.position:self.position + 2] == '${') or
                any(self.source[self.position:].startswith(prefix) 
                    for prefix in self.comment_prefixes)):
                break
            
            self.position += 1
            self.column += 1
        
        if self.position > start_pos:
            value = self.source[start_pos:self.position].strip()
            if value:
                # Check if it's a boolean
                lower_value = value.lower()
                if lower_value in ('true', 'false', 'yes', 'no', 'on', 'off', '1', '0'):
                    self._add_token(TokenType.BOOLEAN, value)
                else:
                    self._add_token(TokenType.IDENTIFIER, value)
                return True
        
        return False
    
    def _add_token(self, token_type: TokenType, value: str) -> None:
        """Add token to list"""
        token = Token(token_type, value, self.line, self.column - len(value), self.filename)
        self.tokens.append(token)
    
    def _advance(self, count: int) -> None:
        """Advance position"""
        for _ in range(count):
            if self.position < len(self.source) and self.source[self.position] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.position += 1


class ParseError(Exception):
    """INI parsing error"""
    
    def __init__(self, message: str, token: Optional[Token] = None):
        self.message = message
        self.token = token
        super().__init__(self._format_message())
    
    def _format_message(self) -> str:
        if self.token:
            return f"Parse error: {self.message} at line {self.token.line}, column {self.token.column}"
        return f"Parse error: {self.message}"


class INIParser:
    """INI parser using recursive descent parsing"""
    
    def __init__(self, tokens: List[Token], 
                 case_sensitive: bool = True,
                 allow_multiline: bool = True,
                 interpolation: bool = False):
        self.tokens = tokens
        self.case_sensitive = case_sensitive
        self.allow_multiline = allow_multiline
        self.interpolation = interpolation
        self.position = 0
        self.current_token = tokens[0] if tokens else None
    
    def parse(self) -> INIConfiguration:
        """Parse tokens into INI AST"""
        global_entries = []
        sections = []
        current_section = None
        
        while not self._is_at_end():
            # Skip newlines at top level
            if self._match(TokenType.NEWLINE):
                continue
            
            # Comments
            if self._check(TokenType.COMMENT):
                comment = self._parse_comment()
                if current_section:
                    current_section.add_entry(comment)
                else:
                    global_entries.append(comment)
                continue
            
            # Section headers
            if self._check(TokenType.SECTION_START):
                current_section = self._parse_section()
                sections.append(current_section)
                continue
            
            # Key-value pairs
            if self._check(TokenType.IDENTIFIER):
                key_value = self._parse_key_value_pair()
                if current_section:
                    current_section.add_entry(key_value)
                else:
                    global_entries.append(key_value)
                continue
            
            # Unexpected token
            self._advance()
        
        return INIConfiguration(
            sections=sections,
            global_entries=global_entries,
            case_sensitive=self.case_sensitive,
            allow_multiline=self.allow_multiline
        )
    
    def _parse_section(self) -> INISection:
        """Parse section header"""
        self._consume(TokenType.SECTION_START, "Expected '['")
        
        section_name = ""
        subsection = None
        
        # Parse section name
        if self._check(TokenType.IDENTIFIER):
            section_name = self._advance().value
        else:
            raise ParseError("Expected section name", self.current_token)
        
        # Check for subsection (Git config style)
        if self._check(TokenType.STRING):
            subsection = self._advance().value
        
        self._consume(TokenType.SECTION_END, "Expected ']'")
        
        # Skip to end of line
        while not self._check(TokenType.NEWLINE) and not self._is_at_end():
            if self._check(TokenType.COMMENT):
                break
            self._advance()
        
        if subsection:
            return GitConfigSection(
                name=section_name,
                subsection=subsection,
                entries=[],
                is_case_sensitive=self.case_sensitive
            )
        else:
            return INISection(
                name=section_name,
                entries=[],
                is_case_sensitive=self.case_sensitive
            )
    
    def _parse_key_value_pair(self) -> INIKeyValuePair:
        """Parse key-value pair"""
        # Parse key
        key_token = self._consume(TokenType.IDENTIFIER, "Expected key name")
        key = INIKey(key_token.value, self.case_sensitive)
        
        # Parse delimiter
        delimiter = INIDelimiterType.EQUALS
        if self._match(TokenType.EQUALS):
            delimiter = INIDelimiterType.EQUALS
        elif self._match(TokenType.COLON):
            delimiter = INIDelimiterType.COLON
        else:
            raise ParseError("Expected '=' or ':'", self.current_token)
        
        # Parse value
        value = self._parse_value()
        
        # Check for inline comment
        inline_comment = None
        if self._check(TokenType.COMMENT):
            inline_comment = self._parse_comment()
        
        return INIKeyValuePair(
            key=key,
            value=value,
            delimiter=delimiter,
            inline_comment=inline_comment
        )
    
    def _parse_value(self) -> INIValue:
        """Parse value with type inference"""
        raw_text = ""
        value = None
        value_type = INIValueType.STRING
        is_quoted = False
        quote_style = '"'
        
        # Handle different value types
        if self._check(TokenType.STRING):
            token = self._advance()
            value = token.value
            raw_text = f'"{token.value}"'
            value_type = INIValueType.STRING
            is_quoted = True
        
        elif self._check(TokenType.NUMBER):
            token = self._advance()
            raw_text = token.value
            try:
                if '.' in token.value or 'e' in token.value.lower():
                    value = float(token.value)
                else:
                    value = int(token.value)
                value_type = INIValueType.NUMBER
            except ValueError:
                value = token.value
                value_type = INIValueType.STRING
        
        elif self._check(TokenType.BOOLEAN):
            token = self._advance()
            raw_text = token.value
            value = self._parse_boolean_value(token.value)
            value_type = INIValueType.BOOLEAN
        
        elif self._check(TokenType.IDENTIFIER):
            # Unquoted string value
            value_parts = []
            
            while (self._check(TokenType.IDENTIFIER) or 
                   (self.interpolation and self._check(TokenType.INTERPOLATION_START))):
                
                if self._check(TokenType.INTERPOLATION_START):
                    # Handle interpolation
                    interpolation = self._parse_interpolation()
                    value_parts.append(interpolation)
                else:
                    token = self._advance()
                    value_parts.append(token.value)
                
                # Check for continuation
                if (self.allow_multiline and self._check(TokenType.CONTINUATION) and 
                    self._peek_next() and self._peek_next().type == TokenType.NEWLINE):
                    self._advance()  # Skip continuation
                    self._advance()  # Skip newline
                    continue
                
                break
            
            if value_parts:
                if len(value_parts) == 1 and isinstance(value_parts[0], str):
                    value = value_parts[0]
                    raw_text = value
                    
                    # Try to infer type
                    if self._looks_like_list(value):
                        value = self._parse_list_value(value)
                        value_type = INIValueType.LIST
                    elif '\n' in value:
                        value_type = INIValueType.MULTILINE
                else:
                    # Mixed content with interpolation
                    value = value_parts
                    raw_text = str(value_parts)
            else:
                value = ""
                raw_text = ""
        
        else:
            # Empty value
            value = ""
            raw_text = ""
        
        return INIValue(
            value=value,
            value_type=value_type,
            raw_text=raw_text,
            is_quoted=is_quoted,
            quote_style=quote_style
        )
    
    def _parse_interpolation(self) -> INIInterpolation:
        """Parse variable interpolation"""
        self._consume(TokenType.INTERPOLATION_START, "Expected '${'")
        
        var_name = ""
        if self._check(TokenType.IDENTIFIER):
            var_name = self._advance().value
        
        default_value = None
        # TODO: Handle default values like ${VAR:-default}
        
        self._consume(TokenType.INTERPOLATION_END, "Expected '}'")
        
        return INIInterpolation(
            variable_name=var_name,
            default_value=default_value,
            format_style="${}"
        )
    
    def _parse_comment(self) -> INIComment:
        """Parse comment"""
        token = self._consume(TokenType.COMMENT, "Expected comment")
        
        # Determine comment style based on the token's context
        style = INICommentStyle.SEMICOLON  # Default
        if token.value.startswith('#'):
            style = INICommentStyle.HASH
        
        return INIComment(
            text=token.value,
            style=style
        )
    
    def _parse_boolean_value(self, value: str) -> bool:
        """Parse boolean value from string"""
        lower_value = value.lower()
        if lower_value in ('true', 'yes', 'on', '1'):
            return True
        elif lower_value in ('false', 'no', 'off', '0'):
            return False
        else:
            # Fallback to string representation
            return bool(value)
    
    def _looks_like_list(self, value: str) -> bool:
        """Check if value looks like a list"""
        return ',' in value or ';' in value or '\n' in value
    
    def _parse_list_value(self, value: str) -> List[str]:
        """Parse list value from string"""
        if '\n' in value:
            # Multi-line list
            return [line.strip() for line in value.split('\n') if line.strip()]
        elif ',' in value:
            # Comma-separated list
            return [item.strip() for item in value.split(',') if item.strip()]
        elif ';' in value:
            # Semicolon-separated list
            return [item.strip() for item in value.split(';') if item.strip()]
        else:
            return [value]
    
    # Utility methods
    def _match(self, *types: TokenType) -> bool:
        """Check if current token matches any of the given types"""
        for token_type in types:
            if self._check(token_type):
                self._advance()
                return True
        return False
    
    def _check(self, token_type: TokenType) -> bool:
        """Check if current token is of given type"""
        if self._is_at_end():
            return False
        return self.current_token.type == token_type
    
    def _advance(self) -> Token:
        """Consume current token and return it"""
        if not self._is_at_end():
            self.position += 1
            if self.position < len(self.tokens):
                self.current_token = self.tokens[self.position]
        return self._previous()
    
    def _is_at_end(self) -> bool:
        """Check if we've reached end of tokens"""
        return self.current_token.type == TokenType.EOF
    
    def _previous(self) -> Token:
        """Return previous token"""
        return self.tokens[self.position - 1]
    
    def _peek_next(self) -> Optional[Token]:
        """Peek at next token without consuming"""
        if self.position + 1 < len(self.tokens):
            return self.tokens[self.position + 1]
        return None
    
    def _consume(self, token_type: TokenType, message: str) -> Token:
        """Consume token of expected type or raise error"""
        if self._check(token_type):
            return self._advance()
        
        raise ParseError(message, self.current_token)


def parse_ini(source: str, filename: Optional[str] = None, 
              format_type: str = "standard") -> INIConfiguration:
    """Main entry point for parsing INI source code"""
    try:
        # Get format configuration
        format_config = INI_FORMATS.get(format_type, INI_FORMATS["standard"])
        
        # Create lexer
        lexer = INILexer(
            source=source,
            filename=filename,
            comment_prefixes=format_config["comment_prefixes"],
            delimiters=format_config["delimiters"],
            case_sensitive=format_config["case_sensitive"]
        )
        tokens = lexer.tokenize()
        
        # Create parser
        parser = INIParser(
            tokens=tokens,
            case_sensitive=format_config["case_sensitive"],
            allow_multiline=format_config["allow_multiline"],
            interpolation=format_config.get("interpolation", False)
        )
        
        return parser.parse()
    
    except Exception as e:
        raise ParseError(f"Failed to parse INI code: {str(e)}")


def parse_ini_file(file_path: str, format_type: str = "standard") -> INIConfiguration:
    """Parse INI file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    return parse_ini(content, file_path, format_type)


# Format-specific parsers
def parse_windows_ini(source: str, filename: Optional[str] = None) -> INIConfiguration:
    """Parse Windows INI format"""
    return parse_ini(source, filename, "windows")


def parse_git_config(source: str, filename: Optional[str] = None) -> INIConfiguration:
    """Parse Git config format"""
    return parse_ini(source, filename, "git")


def parse_systemd_config(source: str, filename: Optional[str] = None) -> INIConfiguration:
    """Parse systemd unit file format"""
    return parse_ini(source, filename, "systemd")


def parse_python_config(source: str, filename: Optional[str] = None) -> INIConfiguration:
    """Parse Python ConfigParser format"""
    return parse_ini(source, filename, "python") 