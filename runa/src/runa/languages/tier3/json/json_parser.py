#!/usr/bin/env python3
"""
JSON Parser and Lexer

Comprehensive JSON parsing implementation with error handling and extensions support.

Author: Sybertnetics AI Solutions
License: MIT
"""

import re
import json as python_json
from typing import List, Optional, Dict, Any, Union, Tuple
from dataclasses import dataclass
from enum import Enum, auto
import logging

from .json_ast import *


class JsonTokenType(Enum):
    """JSON token types."""
    # Literals
    STRING = auto()
    NUMBER = auto()
    BOOLEAN_TRUE = auto()
    BOOLEAN_FALSE = auto()
    NULL = auto()
    
    # Delimiters
    LBRACE = auto()      # {
    RBRACE = auto()      # }
    LBRACKET = auto()    # [
    RBRACKET = auto()    # ]
    COMMA = auto()       # ,
    COLON = auto()       # :
    
    # Special
    EOF = auto()
    WHITESPACE = auto()
    COMMENT = auto()     # For JSON with comments extension


@dataclass
class JsonToken:
    """JSON token."""
    type: JsonTokenType
    value: str
    line: int
    column: int
    position: int


class JsonLexer:
    """JSON lexer for tokenizing JSON text."""
    
    def __init__(self, allow_comments: bool = False, allow_trailing_commas: bool = False):
        self.allow_comments = allow_comments
        self.allow_trailing_commas = allow_trailing_commas
        
        # Token patterns
        self.token_patterns = [
            (r'//.*$', JsonTokenType.COMMENT),
            (r'/\*.*?\*/', JsonTokenType.COMMENT),
            (r'\s+', JsonTokenType.WHITESPACE),
            (r'\{', JsonTokenType.LBRACE),
            (r'\}', JsonTokenType.RBRACE),
            (r'\[', JsonTokenType.LBRACKET),
            (r'\]', JsonTokenType.RBRACKET),
            (r',', JsonTokenType.COMMA),
            (r':', JsonTokenType.COLON),
            (r'true\b', JsonTokenType.BOOLEAN_TRUE),
            (r'false\b', JsonTokenType.BOOLEAN_FALSE),
            (r'null\b', JsonTokenType.NULL),
            (r'-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?', JsonTokenType.NUMBER),
            (r'"(?:[^"\\]|\\.)*"', JsonTokenType.STRING),
        ]
    
    def tokenize(self, text: str) -> List[JsonToken]:
        """Tokenize JSON text."""
        tokens = []
        lines = text.split('\n')
        position = 0
        
        for line_num, line in enumerate(lines, 1):
            column = 1
            pos = 0
            
            while pos < len(line):
                matched = False
                
                for pattern, token_type in self.token_patterns:
                    regex = re.compile(pattern)
                    match = regex.match(line, pos)
                    
                    if match:
                        value = match.group(0)
                        
                        # Skip whitespace and comments (unless comments are enabled)
                        if token_type == JsonTokenType.WHITESPACE:
                            pos = match.end()
                            column += len(value)
                            position += len(value)
                            matched = True
                            break
                        elif token_type == JsonTokenType.COMMENT:
                            if self.allow_comments:
                                tokens.append(JsonToken(
                                    type=token_type,
                                    value=value,
                                    line=line_num,
                                    column=column,
                                    position=position
                                ))
                            pos = match.end()
                            column += len(value)
                            position += len(value)
                            matched = True
                            break
                        else:
                            tokens.append(JsonToken(
                                type=token_type,
                                value=value,
                                line=line_num,
                                column=column,
                                position=position
                            ))
                            pos = match.end()
                            column += len(value)
                            position += len(value)
                            matched = True
                            break
                
                if not matched:
                    # Unknown character
                    raise ValueError(f"Unexpected character '{line[pos]}' at line {line_num}, column {column}")
            
            # Add newline to position for next line
            position += 1
        
        tokens.append(JsonToken(JsonTokenType.EOF, '', len(lines), 1, position))
        return tokens


class JsonParser:
    """JSON parser."""
    
    def __init__(self, allow_comments: bool = False, allow_trailing_commas: bool = False):
        self.allow_comments = allow_comments
        self.allow_trailing_commas = allow_trailing_commas
        self.tokens = []
        self.pos = 0
        self.logger = logging.getLogger(__name__)
    
    def parse(self, text: str) -> JsonDocument:
        """Parse JSON text into AST."""
        try:
            lexer = JsonLexer(self.allow_comments, self.allow_trailing_commas)
            self.tokens = lexer.tokenize(text)
            self.pos = 0
            
            # Skip initial comments
            self._skip_comments()
            
            # Parse root value
            root_value = self._parse_value()
            
            # Ensure we've consumed all tokens (except EOF)
            self._skip_comments()
            if not self._is_at_end():
                current = self._current_token()
                raise ValueError(f"Unexpected token '{current.value}' at line {current.line}")
            
            return JsonDocument(root=root_value)
        except Exception as e:
            self.logger.error(f"JSON parsing failed: {e}")
            raise RuntimeError(f"Failed to parse JSON: {e}")
    
    def _current_token(self) -> JsonToken:
        """Get current token."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return JsonToken(JsonTokenType.EOF, '', 0, 0, 0)
    
    def _advance(self) -> JsonToken:
        """Advance to next token."""
        token = self._current_token()
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return token
    
    def _match(self, *types: JsonTokenType) -> bool:
        """Check if current token matches any of the given types."""
        return self._current_token().type in types
    
    def _consume(self, expected: JsonTokenType, message: str = None) -> JsonToken:
        """Consume token of expected type."""
        if not self._match(expected):
            current = self._current_token()
            error_msg = message or f"Expected {expected}, got {current.type} at line {current.line}"
            raise ValueError(error_msg)
        return self._advance()
    
    def _is_at_end(self) -> bool:
        """Check if at end of tokens."""
        return self._match(JsonTokenType.EOF)
    
    def _skip_comments(self):
        """Skip comment tokens."""
        while self._match(JsonTokenType.COMMENT):
            self._advance()
    
    def _parse_value(self) -> JsonValue:
        """Parse a JSON value."""
        self._skip_comments()
        
        if self._match(JsonTokenType.STRING):
            return self._parse_string()
        elif self._match(JsonTokenType.NUMBER):
            return self._parse_number()
        elif self._match(JsonTokenType.BOOLEAN_TRUE, JsonTokenType.BOOLEAN_FALSE):
            return self._parse_boolean()
        elif self._match(JsonTokenType.NULL):
            return self._parse_null()
        elif self._match(JsonTokenType.LBRACE):
            return self._parse_object()
        elif self._match(JsonTokenType.LBRACKET):
            return self._parse_array()
        else:
            current = self._current_token()
            raise ValueError(f"Unexpected token '{current.value}' at line {current.line}")
    
    def _parse_string(self) -> JsonString:
        """Parse a JSON string."""
        token = self._consume(JsonTokenType.STRING)
        # Remove quotes and unescape
        value = token.value[1:-1]  # Remove surrounding quotes
        value = self._unescape_string(value)
        return JsonString(value=value)
    
    def _parse_number(self) -> JsonNumber:
        """Parse a JSON number."""
        token = self._consume(JsonTokenType.NUMBER)
        value_str = token.value
        
        # Parse as int or float
        if '.' in value_str or 'e' in value_str.lower():
            value = float(value_str)
        else:
            value = int(value_str)
        
        return JsonNumber(value=value)
    
    def _parse_boolean(self) -> JsonBoolean:
        """Parse a JSON boolean."""
        if self._match(JsonTokenType.BOOLEAN_TRUE):
            self._advance()
            return JsonBoolean(value=True)
        else:
            self._consume(JsonTokenType.BOOLEAN_FALSE)
            return JsonBoolean(value=False)
    
    def _parse_null(self) -> JsonNull:
        """Parse a JSON null."""
        self._consume(JsonTokenType.NULL)
        return JsonNull()
    
    def _parse_object(self) -> JsonObject:
        """Parse a JSON object."""
        self._consume(JsonTokenType.LBRACE)
        self._skip_comments()
        
        properties = []
        
        # Handle empty object
        if self._match(JsonTokenType.RBRACE):
            self._advance()
            return JsonObject(properties=properties)
        
        # Parse properties
        while True:
            self._skip_comments()
            
            # Parse key
            if not self._match(JsonTokenType.STRING):
                current = self._current_token()
                raise ValueError(f"Expected string key at line {current.line}")
            
            key = self._parse_string()
            
            self._skip_comments()
            self._consume(JsonTokenType.COLON, "Expected ':' after object key")
            self._skip_comments()
            
            # Parse value
            value = self._parse_value()
            
            properties.append(JsonProperty(key=key, value=value))
            
            self._skip_comments()
            
            if self._match(JsonTokenType.COMMA):
                self._advance()
                self._skip_comments()
                
                # Handle trailing comma
                if self._match(JsonTokenType.RBRACE):
                    if self.allow_trailing_commas:
                        break
                    else:
                        current = self._current_token()
                        raise ValueError(f"Trailing comma not allowed at line {current.line}")
            elif self._match(JsonTokenType.RBRACE):
                break
            else:
                current = self._current_token()
                raise ValueError(f"Expected ',' or '}}' at line {current.line}")
        
        self._consume(JsonTokenType.RBRACE)
        return JsonObject(properties=properties)
    
    def _parse_array(self) -> JsonArray:
        """Parse a JSON array."""
        self._consume(JsonTokenType.LBRACKET)
        self._skip_comments()
        
        elements = []
        
        # Handle empty array
        if self._match(JsonTokenType.RBRACKET):
            self._advance()
            return JsonArray(elements=elements)
        
        # Parse elements
        while True:
            self._skip_comments()
            
            # Parse element
            element = self._parse_value()
            elements.append(element)
            
            self._skip_comments()
            
            if self._match(JsonTokenType.COMMA):
                self._advance()
                self._skip_comments()
                
                # Handle trailing comma
                if self._match(JsonTokenType.RBRACKET):
                    if self.allow_trailing_commas:
                        break
                    else:
                        current = self._current_token()
                        raise ValueError(f"Trailing comma not allowed at line {current.line}")
            elif self._match(JsonTokenType.RBRACKET):
                break
            else:
                current = self._current_token()
                raise ValueError(f"Expected ',' or ']' at line {current.line}")
        
        self._consume(JsonTokenType.RBRACKET)
        return JsonArray(elements=elements)
    
    def _unescape_string(self, value: str) -> str:
        """Unescape JSON string."""
        result = []
        i = 0
        while i < len(value):
            if value[i] == '\\' and i + 1 < len(value):
                next_char = value[i + 1]
                if next_char == '"':
                    result.append('"')
                elif next_char == '\\':
                    result.append('\\')
                elif next_char == '/':
                    result.append('/')
                elif next_char == 'b':
                    result.append('\b')
                elif next_char == 'f':
                    result.append('\f')
                elif next_char == 'n':
                    result.append('\n')
                elif next_char == 'r':
                    result.append('\r')
                elif next_char == 't':
                    result.append('\t')
                elif next_char == 'u' and i + 5 < len(value):
                    # Unicode escape
                    hex_digits = value[i + 2:i + 6]
                    try:
                        unicode_char = chr(int(hex_digits, 16))
                        result.append(unicode_char)
                        i += 4  # Skip the extra characters
                    except ValueError:
                        result.append(value[i])
                else:
                    result.append(value[i])
                i += 2
            else:
                result.append(value[i])
                i += 1
        
        return ''.join(result)


# Convenience functions
def parse_json(text: str, allow_comments: bool = False, allow_trailing_commas: bool = False) -> JsonDocument:
    """Parse JSON text into AST."""
    parser = JsonParser(allow_comments, allow_trailing_commas)
    return parser.parse(text)


def parse_json_file(file_path: str, allow_comments: bool = False, allow_trailing_commas: bool = False) -> JsonDocument:
    """Parse JSON file into AST."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return parse_json(f.read(), allow_comments, allow_trailing_commas)


def parse_json_strict(text: str) -> JsonDocument:
    """Parse JSON text with strict compliance."""
    return parse_json(text, allow_comments=False, allow_trailing_commas=False)


def parse_json_relaxed(text: str) -> JsonDocument:
    """Parse JSON text with relaxed rules (comments and trailing commas allowed)."""
    return parse_json(text, allow_comments=True, allow_trailing_commas=True)


def validate_json_syntax(text: str) -> Tuple[bool, Optional[str]]:
    """Validate JSON syntax."""
    try:
        parse_json_strict(text)
        return True, None
    except Exception as e:
        return False, str(e)


def parse_json_with_python_fallback(text: str) -> JsonDocument:
    """Parse JSON with Python's built-in parser as fallback."""
    try:
        # Try our parser first
        return parse_json_strict(text)
    except:
        try:
            # Fallback to Python's parser
            python_value = python_json.loads(text)
            json_value = json_value_from_python(python_value)
            return JsonDocument(root=json_value)
        except Exception as e:
            raise RuntimeError(f"Failed to parse JSON with both parsers: {e}")


# JSON5 extensions support
def parse_json5(text: str) -> JsonDocument:
    """Parse JSON5 (relaxed JSON) format."""
    # JSON5 allows:
    # - Comments (// and /* */)
    # - Trailing commas
    # - Unquoted object keys
    # - Single quotes for strings
    # - Multi-line strings
    # - Additional number formats
    
    # For now, use relaxed parser
    return parse_json_relaxed(text)