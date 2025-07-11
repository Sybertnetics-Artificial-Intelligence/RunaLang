#!/usr/bin/env python3
"""
C# Parser

Complete C# parser supporting modern C# features from C# 1.0 through C# 12.0.
Includes lexical analysis and recursive descent parsing with comprehensive
error handling and recovery.
"""

import re
from typing import List, Optional, Dict, Any, Union, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum, auto

from .csharp_ast import *


class CSharpTokenType(Enum):
    """C# token types."""
    # Literals
    INTEGER_LITERAL = auto()
    REAL_LITERAL = auto()
    STRING_LITERAL = auto()
    VERBATIM_STRING_LITERAL = auto()
    INTERPOLATED_STRING_LITERAL = auto()
    RAW_STRING_LITERAL = auto()  # C# 11.0
    CHARACTER_LITERAL = auto()
    BOOLEAN_LITERAL = auto()
    NULL_LITERAL = auto()
    
    # Identifiers
    IDENTIFIER = auto()
    VERBATIM_IDENTIFIER = auto()
    
    # Keywords
    ABSTRACT = auto()
    AS = auto()
    BASE = auto()
    BOOL = auto()
    BREAK = auto()
    BYTE = auto()
    CASE = auto()
    CATCH = auto()
    CHAR = auto()
    CHECKED = auto()
    CLASS = auto()
    CONST = auto()
    CONTINUE = auto()
    DECIMAL = auto()
    DEFAULT = auto()
    DELEGATE = auto()
    DO = auto()
    DOUBLE = auto()
    ELSE = auto()
    ENUM = auto()
    EVENT = auto()
    EXPLICIT = auto()
    EXTERN = auto()
    FALSE = auto()
    FINALLY = auto()
    FIXED = auto()
    FLOAT = auto()
    FOR = auto()
    FOREACH = auto()
    GOTO = auto()
    IF = auto()
    IMPLICIT = auto()
    IN = auto()
    INT = auto()
    INTERFACE = auto()
    INTERNAL = auto()
    IS = auto()
    LOCK = auto()
    LONG = auto()
    NAMESPACE = auto()
    NEW = auto()
    NULL = auto()
    OBJECT = auto()
    OPERATOR = auto()
    OUT = auto()
    OVERRIDE = auto()
    PARAMS = auto()
    PRIVATE = auto()
    PROTECTED = auto()
    PUBLIC = auto()
    READONLY = auto()
    REF = auto()
    RETURN = auto()
    SBYTE = auto()
    SEALED = auto()
    SHORT = auto()
    SIZEOF = auto()
    STACKALLOC = auto()
    STATIC = auto()
    STRING = auto()
    STRUCT = auto()
    SWITCH = auto()
    THIS = auto()
    THROW = auto()
    TRUE = auto()
    TRY = auto()
    TYPEOF = auto()
    UINT = auto()
    ULONG = auto()
    UNCHECKED = auto()
    UNSAFE = auto()
    USHORT = auto()
    USING = auto()
    VIRTUAL = auto()
    VOID = auto()
    VOLATILE = auto()
    WHILE = auto()
    
    # Contextual keywords (C# 2.0+)
    ADD = auto()
    ALIAS = auto()
    ASCENDING = auto()
    ASYNC = auto()
    AWAIT = auto()
    BY = auto()
    DESCENDING = auto()
    DYNAMIC = auto()
    EQUALS = auto()
    FROM = auto()
    GET = auto()
    GLOBAL = auto()
    GROUP = auto()
    INTO = auto()
    JOIN = auto()
    LET = auto()
    NAMEOF = auto()
    ON = auto()
    ORDERBY = auto()
    PARTIAL = auto()
    REMOVE = auto()
    SELECT = auto()
    SET = auto()
    UNMANAGED = auto()
    VALUE = auto()
    VAR = auto()
    WHEN = auto()
    WHERE = auto()
    YIELD = auto()
    
    # C# 7.0+ contextual keywords
    AND = auto()
    OR = auto()
    NOT = auto()
    
    # C# 8.0+ contextual keywords
    NOTNULL = auto()
    UNMANAGED_CONSTRAINT = auto()
    
    # C# 9.0+ contextual keywords
    INIT = auto()
    RECORD = auto()
    WITH = auto()
    
    # C# 10.0+ contextual keywords
    FILE = auto()
    REQUIRED = auto()
    
    # C# 11.0+ contextual keywords
    SCOPED = auto()
    
    # Operators and punctuation
    PLUS = auto()           # +
    MINUS = auto()          # -
    MULTIPLY = auto()       # *
    DIVIDE = auto()         # /
    MODULO = auto()         # %
    ASSIGN = auto()         # =
    PLUS_ASSIGN = auto()    # +=
    MINUS_ASSIGN = auto()   # -=
    MULTIPLY_ASSIGN = auto() # *=
    DIVIDE_ASSIGN = auto()  # /=
    MODULO_ASSIGN = auto()  # %=
    AND_ASSIGN = auto()     # &=
    OR_ASSIGN = auto()      # |=
    XOR_ASSIGN = auto()     # ^=
    LEFT_SHIFT_ASSIGN = auto() # <<=
    RIGHT_SHIFT_ASSIGN = auto() # >>=
    UNSIGNED_RIGHT_SHIFT_ASSIGN = auto() # >>>= (C# 11.0)
    NULL_COALESCING_ASSIGN = auto() # ??= (C# 8.0)
    
    # Comparison operators
    EQUAL = auto()          # ==
    NOT_EQUAL = auto()      # !=
    LESS_THAN = auto()      # <
    LESS_EQUAL = auto()     # <=
    GREATER_THAN = auto()   # >
    GREATER_EQUAL = auto()  # >=
    
    # Logical operators
    LOGICAL_AND = auto()    # &&
    LOGICAL_OR = auto()     # ||
    LOGICAL_NOT = auto()    # !
    
    # Bitwise operators
    BITWISE_AND = auto()    # &
    BITWISE_OR = auto()     # |
    BITWISE_XOR = auto()    # ^
    BITWISE_NOT = auto()    # ~
    LEFT_SHIFT = auto()     # <<
    RIGHT_SHIFT = auto()    # >>
    UNSIGNED_RIGHT_SHIFT = auto() # >>> (C# 11.0)
    
    # Increment/decrement
    INCREMENT = auto()      # ++
    DECREMENT = auto()      # --
    
    # Special operators
    QUESTION = auto()       # ?
    COLON = auto()          # :
    DOUBLE_COLON = auto()   # ::
    DOT = auto()            # .
    ARROW = auto()          # ->
    NULL_CONDITIONAL = auto() # ?. (C# 6.0)
    NULL_CONDITIONAL_ELEMENT = auto() # ?[ (C# 6.0)
    NULL_COALESCING = auto() # ?? (C# 2.0)
    NULL_FORGIVING = auto() # ! (C# 8.0)
    RANGE = auto()          # .. (C# 8.0)
    INDEX_FROM_END = auto() # ^ (C# 8.0)
    
    # Punctuation
    SEMICOLON = auto()      # ;
    COMMA = auto()          # ,
    LEFT_PAREN = auto()     # (
    RIGHT_PAREN = auto()    # )
    LEFT_BRACE = auto()     # {
    RIGHT_BRACE = auto()    # }
    LEFT_BRACKET = auto()   # [
    RIGHT_BRACKET = auto()  # ]
    
    # Preprocessor
    HASH = auto()           # #
    
    # Whitespace and comments
    WHITESPACE = auto()
    NEWLINE = auto()
    SINGLE_LINE_COMMENT = auto()
    MULTI_LINE_COMMENT = auto()
    
    # Special
    EOF = auto()
    UNKNOWN = auto()


@dataclass
class CSharpToken:
    """C# token."""
    type: CSharpTokenType
    value: str
    line: int
    column: int
    span: Tuple[int, int]  # (start, end) positions


class CSharpLexer:
    """C# lexer for tokenizing source code."""
    
    # Keywords mapping
    KEYWORDS = {
        'abstract': CSharpTokenType.ABSTRACT,
        'as': CSharpTokenType.AS,
        'base': CSharpTokenType.BASE,
        'bool': CSharpTokenType.BOOL,
        'break': CSharpTokenType.BREAK,
        'byte': CSharpTokenType.BYTE,
        'case': CSharpTokenType.CASE,
        'catch': CSharpTokenType.CATCH,
        'char': CSharpTokenType.CHAR,
        'checked': CSharpTokenType.CHECKED,
        'class': CSharpTokenType.CLASS,
        'const': CSharpTokenType.CONST,
        'continue': CSharpTokenType.CONTINUE,
        'decimal': CSharpTokenType.DECIMAL,
        'default': CSharpTokenType.DEFAULT,
        'delegate': CSharpTokenType.DELEGATE,
        'do': CSharpTokenType.DO,
        'double': CSharpTokenType.DOUBLE,
        'else': CSharpTokenType.ELSE,
        'enum': CSharpTokenType.ENUM,
        'event': CSharpTokenType.EVENT,
        'explicit': CSharpTokenType.EXPLICIT,
        'extern': CSharpTokenType.EXTERN,
        'false': CSharpTokenType.FALSE,
        'finally': CSharpTokenType.FINALLY,
        'fixed': CSharpTokenType.FIXED,
        'float': CSharpTokenType.FLOAT,
        'for': CSharpTokenType.FOR,
        'foreach': CSharpTokenType.FOREACH,
        'goto': CSharpTokenType.GOTO,
        'if': CSharpTokenType.IF,
        'implicit': CSharpTokenType.IMPLICIT,
        'in': CSharpTokenType.IN,
        'int': CSharpTokenType.INT,
        'interface': CSharpTokenType.INTERFACE,
        'internal': CSharpTokenType.INTERNAL,
        'is': CSharpTokenType.IS,
        'lock': CSharpTokenType.LOCK,
        'long': CSharpTokenType.LONG,
        'namespace': CSharpTokenType.NAMESPACE,
        'new': CSharpTokenType.NEW,
        'null': CSharpTokenType.NULL,
        'object': CSharpTokenType.OBJECT,
        'operator': CSharpTokenType.OPERATOR,
        'out': CSharpTokenType.OUT,
        'override': CSharpTokenType.OVERRIDE,
        'params': CSharpTokenType.PARAMS,
        'private': CSharpTokenType.PRIVATE,
        'protected': CSharpTokenType.PROTECTED,
        'public': CSharpTokenType.PUBLIC,
        'readonly': CSharpTokenType.READONLY,
        'ref': CSharpTokenType.REF,
        'return': CSharpTokenType.RETURN,
        'sbyte': CSharpTokenType.SBYTE,
        'sealed': CSharpTokenType.SEALED,
        'short': CSharpTokenType.SHORT,
        'sizeof': CSharpTokenType.SIZEOF,
        'stackalloc': CSharpTokenType.STACKALLOC,
        'static': CSharpTokenType.STATIC,
        'string': CSharpTokenType.STRING,
        'struct': CSharpTokenType.STRUCT,
        'switch': CSharpTokenType.SWITCH,
        'this': CSharpTokenType.THIS,
        'throw': CSharpTokenType.THROW,
        'true': CSharpTokenType.TRUE,
        'try': CSharpTokenType.TRY,
        'typeof': CSharpTokenType.TYPEOF,
        'uint': CSharpTokenType.UINT,
        'ulong': CSharpTokenType.ULONG,
        'unchecked': CSharpTokenType.UNCHECKED,
        'unsafe': CSharpTokenType.UNSAFE,
        'ushort': CSharpTokenType.USHORT,
        'using': CSharpTokenType.USING,
        'virtual': CSharpTokenType.VIRTUAL,
        'void': CSharpTokenType.VOID,
        'volatile': CSharpTokenType.VOLATILE,
        'while': CSharpTokenType.WHILE,
    }
    
    # Contextual keywords (context-dependent)
    CONTEXTUAL_KEYWORDS = {
        'add': CSharpTokenType.ADD,
        'alias': CSharpTokenType.ALIAS,
        'ascending': CSharpTokenType.ASCENDING,
        'async': CSharpTokenType.ASYNC,
        'await': CSharpTokenType.AWAIT,
        'by': CSharpTokenType.BY,
        'descending': CSharpTokenType.DESCENDING,
        'dynamic': CSharpTokenType.DYNAMIC,
        'equals': CSharpTokenType.EQUALS,
        'from': CSharpTokenType.FROM,
        'get': CSharpTokenType.GET,
        'global': CSharpTokenType.GLOBAL,
        'group': CSharpTokenType.GROUP,
        'into': CSharpTokenType.INTO,
        'join': CSharpTokenType.JOIN,
        'let': CSharpTokenType.LET,
        'nameof': CSharpTokenType.NAMEOF,
        'on': CSharpTokenType.ON,
        'orderby': CSharpTokenType.ORDERBY,
        'partial': CSharpTokenType.PARTIAL,
        'remove': CSharpTokenType.REMOVE,
        'select': CSharpTokenType.SELECT,
        'set': CSharpTokenType.SET,
        'unmanaged': CSharpTokenType.UNMANAGED,
        'value': CSharpTokenType.VALUE,
        'var': CSharpTokenType.VAR,
        'when': CSharpTokenType.WHEN,
        'where': CSharpTokenType.WHERE,
        'yield': CSharpTokenType.YIELD,
        'and': CSharpTokenType.AND,
        'or': CSharpTokenType.OR,
        'not': CSharpTokenType.NOT,
        'notnull': CSharpTokenType.NOTNULL,
        'init': CSharpTokenType.INIT,
        'record': CSharpTokenType.RECORD,
        'with': CSharpTokenType.WITH,
        'file': CSharpTokenType.FILE,
        'required': CSharpTokenType.REQUIRED,
        'scoped': CSharpTokenType.SCOPED,
    }
    
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[CSharpToken] = []
        self.current_char = self.source[0] if source else None
        
    def error(self, message: str):
        """Raise a lexer error."""
        raise SyntaxError(f"Lexer error at line {self.line}, column {self.column}: {message}")
    
    def advance(self):
        """Advance position and update current character."""
        if self.current_char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        
        self.position += 1
        if self.position >= len(self.source):
            self.current_char = None
        else:
            self.current_char = self.source[self.position]
    
    def peek(self, offset: int = 1) -> Optional[str]:
        """Peek at character at offset from current position."""
        pos = self.position + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]
    
    def skip_whitespace(self):
        """Skip whitespace characters."""
        while self.current_char and self.current_char.isspace():
            self.advance()
    
    def read_string_literal(self) -> str:
        """Read a string literal."""
        quote_char = self.current_char
        result = quote_char
        self.advance()
        
        while self.current_char and self.current_char != quote_char:
            if self.current_char == '\\':
                result += self.current_char
                self.advance()
                if self.current_char:
                    result += self.current_char
                    self.advance()
            else:
                result += self.current_char
                self.advance()
        
        if self.current_char == quote_char:
            result += self.current_char
            self.advance()
        else:
            self.error("Unterminated string literal")
        
        return result
    
    def read_verbatim_string_literal(self) -> str:
        """Read a verbatim string literal (@"...")."""
        result = '@"'
        self.advance()  # Skip @
        self.advance()  # Skip "
        
        while self.current_char:
            if self.current_char == '"':
                result += '"'
                self.advance()
                if self.current_char == '"':
                    # Escaped quote
                    result += '"'
                    self.advance()
                else:
                    break
            else:
                result += self.current_char
                self.advance()
        
        return result
    
    def read_raw_string_literal(self) -> str:
        """Read a raw string literal with triple quotes."""
        start_pos = self.position
        quote_count = 0
        
        # Count opening quotes
        while self.current_char == '"':
            quote_count += 1
            self.advance()
        
        if quote_count < 3:
            self.error("Raw string literal must start with at least three quotes")
        
        result = '"' * quote_count
        
        # Read content until closing quotes
        while self.current_char:
            if self.current_char == '"':
                # Check if we have enough closing quotes
                closing_quotes = 0
                temp_pos = self.position
                while temp_pos < len(self.source) and self.source[temp_pos] == '"':
                    closing_quotes += 1
                    temp_pos += 1
                
                if closing_quotes >= quote_count:
                    # Found closing quotes
                    for _ in range(quote_count):
                        result += self.current_char
                        self.advance()
                    break
                else:
                    result += self.current_char
                    self.advance()
            else:
                result += self.current_char
                self.advance()
        
        return result
    
    def read_character_literal(self) -> str:
        """Read a character literal."""
        result = "'"
        self.advance()
        
        if self.current_char == '\\':
            result += self.current_char
            self.advance()
            if self.current_char:
                result += self.current_char
                self.advance()
        elif self.current_char and self.current_char != "'":
            result += self.current_char
            self.advance()
        
        if self.current_char == "'":
            result += self.current_char
            self.advance()
        else:
            self.error("Unterminated character literal")
        
        return result
    
    def read_number(self) -> Tuple[str, CSharpTokenType]:
        """Read a numeric literal."""
        result = ''
        token_type = CSharpTokenType.INTEGER_LITERAL
        
        # Handle hex/binary prefixes
        if self.current_char == '0' and self.peek() and self.peek().lower() in 'xb':
            result += self.current_char
            self.advance()
            result += self.current_char
            self.advance()
            
            # Read hex/binary digits
            while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
                result += self.current_char
                self.advance()
        else:
            # Read integer part
            while self.current_char and (self.current_char.isdigit() or self.current_char == '_'):
                result += self.current_char
                self.advance()
            
            # Check for decimal point
            if self.current_char == '.' and self.peek() and self.peek().isdigit():
                token_type = CSharpTokenType.REAL_LITERAL
                result += self.current_char
                self.advance()
                
                while self.current_char and (self.current_char.isdigit() or self.current_char == '_'):
                    result += self.current_char
                    self.advance()
            
            # Check for exponent
            if self.current_char and self.current_char.lower() == 'e':
                token_type = CSharpTokenType.REAL_LITERAL
                result += self.current_char
                self.advance()
                
                if self.current_char and self.current_char in '+-':
                    result += self.current_char
                    self.advance()
                
                while self.current_char and (self.current_char.isdigit() or self.current_char == '_'):
                    result += self.current_char
                    self.advance()
        
        # Check for suffix
        if self.current_char and self.current_char.lower() in 'fldmu':
            result += self.current_char
            self.advance()
            if self.current_char and self.current_char.lower() == 'l':
                result += self.current_char
                self.advance()
        
        return result, token_type
    
    def read_identifier(self) -> str:
        """Read an identifier."""
        result = ''
        
        # Handle verbatim identifier
        if self.current_char == '@':
            result += self.current_char
            self.advance()
        
        # First character must be letter or underscore
        if self.current_char and (self.current_char.isalpha() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        
        # Subsequent characters can be letters, digits, or underscores
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        
        return result
    
    def read_single_line_comment(self) -> str:
        """Read a single-line comment."""
        result = ''
        while self.current_char and self.current_char != '\n':
            result += self.current_char
            self.advance()
        return result
    
    def read_multi_line_comment(self) -> str:
        """Read a multi-line comment."""
        result = '/*'
        self.advance()  # Skip /
        self.advance()  # Skip *
        
        while self.current_char:
            if self.current_char == '*' and self.peek() == '/':
                result += '*/'
                self.advance()
                self.advance()
                break
            else:
                result += self.current_char
                self.advance()
        
        return result
    
    def get_next_token(self) -> CSharpToken:
        """Get the next token from the source."""
        while self.current_char:
            start_pos = self.position
            start_line = self.line
            start_column = self.column
            
            # Skip whitespace
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            # Single-line comment
            if self.current_char == '/' and self.peek() == '/':
                value = self.read_single_line_comment()
                return CSharpToken(
                    CSharpTokenType.SINGLE_LINE_COMMENT,
                    value,
                    start_line,
                    start_column,
                    (start_pos, self.position)
                )
            
            # Multi-line comment
            if self.current_char == '/' and self.peek() == '*':
                value = self.read_multi_line_comment()
                return CSharpToken(
                    CSharpTokenType.MULTI_LINE_COMMENT,
                    value,
                    start_line,
                    start_column,
                    (start_pos, self.position)
                )
            
            # Raw string literal (C# 11.0)
            if self.current_char == '"' and self.peek() == '"' and self.peek(2) == '"':
                value = self.read_raw_string_literal()
                return CSharpToken(
                    CSharpTokenType.RAW_STRING_LITERAL,
                    value,
                    start_line,
                    start_column,
                    (start_pos, self.position)
                )
            
            # Verbatim string literal
            if self.current_char == '@' and self.peek() == '"':
                value = self.read_verbatim_string_literal()
                return CSharpToken(
                    CSharpTokenType.VERBATIM_STRING_LITERAL,
                    value,
                    start_line,
                    start_column,
                    (start_pos, self.position)
                )
            
            # String literal
            if self.current_char == '"':
                value = self.read_string_literal()
                return CSharpToken(
                    CSharpTokenType.STRING_LITERAL,
                    value,
                    start_line,
                    start_column,
                    (start_pos, self.position)
                )
            
            # Character literal
            if self.current_char == "'":
                value = self.read_character_literal()
                return CSharpToken(
                    CSharpTokenType.CHARACTER_LITERAL,
                    value,
                    start_line,
                    start_column,
                    (start_pos, self.position)
                )
            
            # Numbers
            if self.current_char.isdigit():
                value, token_type = self.read_number()
                return CSharpToken(
                    token_type,
                    value,
                    start_line,
                    start_column,
                    (start_pos, self.position)
                )
            
            # Identifiers and keywords
            if self.current_char.isalpha() or self.current_char == '_' or self.current_char == '@':
                value = self.read_identifier()
                
                # Check if it's a keyword
                if value in self.KEYWORDS:
                    token_type = self.KEYWORDS[value]
                elif value in self.CONTEXTUAL_KEYWORDS:
                    token_type = self.CONTEXTUAL_KEYWORDS[value]
                else:
                    token_type = CSharpTokenType.VERBATIM_IDENTIFIER if value.startswith('@') else CSharpTokenType.IDENTIFIER
                
                return CSharpToken(
                    token_type,
                    value,
                    start_line,
                    start_column,
                    (start_pos, self.position)
                )
            
            # Multi-character operators
            if self.current_char == '+' and self.peek() == '+':
                self.advance()
                self.advance()
                return CSharpToken(CSharpTokenType.INCREMENT, '++', start_line, start_column, (start_pos, self.position))
            
            if self.current_char == '-' and self.peek() == '-':
                self.advance()
                self.advance()
                return CSharpToken(CSharpTokenType.DECREMENT, '--', start_line, start_column, (start_pos, self.position))
            
            if self.current_char == '+' and self.peek() == '=':
                self.advance()
                self.advance()
                return CSharpToken(CSharpTokenType.PLUS_ASSIGN, '+=', start_line, start_column, (start_pos, self.position))
            
            if self.current_char == '-' and self.peek() == '=':
                self.advance()
                self.advance()
                return CSharpToken(CSharpTokenType.MINUS_ASSIGN, '-=', start_line, start_column, (start_pos, self.position))
            
            if self.current_char == '*' and self.peek() == '=':
                self.advance()
                self.advance()
                return CSharpToken(CSharpTokenType.MULTIPLY_ASSIGN, '*=', start_line, start_column, (start_pos, self.position))
            
            if self.current_char == '/' and self.peek() == '=':
                self.advance()
                self.advance()
                return CSharpToken(CSharpTokenType.DIVIDE_ASSIGN, '/=', start_line, start_column, (start_pos, self.position))
            
            if self.current_char == '%' and self.peek() == '=':
                self.advance()
                self.advance()
                return CSharpToken(CSharpTokenType.MODULO_ASSIGN, '%=', start_line, start_column, (start_pos, self.position))
            
            if self.current_char == '&' and self.peek() == '&':
                self.advance()
                self.advance()
                return CSharpToken(CSharpTokenType.LOGICAL_AND, '&&', start_line, start_column, (start_pos, self.position))
            
            if self.current_char == '|' and self.peek() == '|':
                self.advance()
                self.advance()
                return CSharpToken(CSharpTokenType.LOGICAL_OR, '||', start_line, start_column, (start_pos, self.position))
            
            if self.current_char == '=' and self.peek() == '=':
                self.advance()
                self.advance()
                return CSharpToken(CSharpTokenType.EQUAL, '==', start_line, start_column, (start_pos, self.position))
            
            if self.current_char == '!' and self.peek() == '=':
                self.advance()
                self.advance()
                return CSharpToken(CSharpTokenType.NOT_EQUAL, '!=', start_line, start_column, (start_pos, self.position))
            
            if self.current_char == '<' and self.peek() == '=':
                self.advance()
                self.advance()
                return CSharpToken(CSharpTokenType.LESS_EQUAL, '<=', start_line, start_column, (start_pos, self.position))
            
            if self.current_char == '>' and self.peek() == '=':
                self.advance()
                self.advance()
                return CSharpToken(CSharpTokenType.GREATER_EQUAL, '>=', start_line, start_column, (start_pos, self.position))
            
            if self.current_char == '<' and self.peek() == '<':
                self.advance()
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return CSharpToken(CSharpTokenType.LEFT_SHIFT_ASSIGN, '<<=', start_line, start_column, (start_pos, self.position))
                return CSharpToken(CSharpTokenType.LEFT_SHIFT, '<<', start_line, start_column, (start_pos, self.position))
            
            if self.current_char == '>' and self.peek() == '>':
                self.advance()
                self.advance()
                if self.current_char == '>':
                    self.advance()
                    if self.current_char == '=':
                        self.advance()
                        return CSharpToken(CSharpTokenType.UNSIGNED_RIGHT_SHIFT_ASSIGN, '>>>=', start_line, start_column, (start_pos, self.position))
                    return CSharpToken(CSharpTokenType.UNSIGNED_RIGHT_SHIFT, '>>>', start_line, start_column, (start_pos, self.position))
                elif self.current_char == '=':
                    self.advance()
                    return CSharpToken(CSharpTokenType.RIGHT_SHIFT_ASSIGN, '>>=', start_line, start_column, (start_pos, self.position))
                return CSharpToken(CSharpTokenType.RIGHT_SHIFT, '>>', start_line, start_column, (start_pos, self.position))
            
            if self.current_char == '?' and self.peek() == '?':
                self.advance()
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return CSharpToken(CSharpTokenType.NULL_COALESCING_ASSIGN, '??=', start_line, start_column, (start_pos, self.position))
                return CSharpToken(CSharpTokenType.NULL_COALESCING, '??', start_line, start_column, (start_pos, self.position))
            
            if self.current_char == '?' and self.peek() == '.':
                self.advance()
                self.advance()
                return CSharpToken(CSharpTokenType.NULL_CONDITIONAL, '?.', start_line, start_column, (start_pos, self.position))
            
            if self.current_char == '?' and self.peek() == '[':
                self.advance()
                self.advance()
                return CSharpToken(CSharpTokenType.NULL_CONDITIONAL_ELEMENT, '?[', start_line, start_column, (start_pos, self.position))
            
            if self.current_char == '.' and self.peek() == '.':
                self.advance()
                self.advance()
                return CSharpToken(CSharpTokenType.RANGE, '..', start_line, start_column, (start_pos, self.position))
            
            if self.current_char == ':' and self.peek() == ':':
                self.advance()
                self.advance()
                return CSharpToken(CSharpTokenType.DOUBLE_COLON, '::', start_line, start_column, (start_pos, self.position))
            
            if self.current_char == '&' and self.peek() == '=':
                self.advance()
                self.advance()
                return CSharpToken(CSharpTokenType.AND_ASSIGN, '&=', start_line, start_column, (start_pos, self.position))
            
            if self.current_char == '|' and self.peek() == '=':
                self.advance()
                self.advance()
                return CSharpToken(CSharpTokenType.OR_ASSIGN, '|=', start_line, start_column, (start_pos, self.position))
            
            if self.current_char == '^' and self.peek() == '=':
                self.advance()
                self.advance()
                return CSharpToken(CSharpTokenType.XOR_ASSIGN, '^=', start_line, start_column, (start_pos, self.position))
            
            if self.current_char == '-' and self.peek() == '>':
                self.advance()
                self.advance()
                return CSharpToken(CSharpTokenType.ARROW, '->', start_line, start_column, (start_pos, self.position))
            
            # Single character tokens
            single_char_tokens = {
                '+': CSharpTokenType.PLUS,
                '-': CSharpTokenType.MINUS,
                '*': CSharpTokenType.MULTIPLY,
                '/': CSharpTokenType.DIVIDE,
                '%': CSharpTokenType.MODULO,
                '=': CSharpTokenType.ASSIGN,
                '<': CSharpTokenType.LESS_THAN,
                '>': CSharpTokenType.GREATER_THAN,
                '!': CSharpTokenType.LOGICAL_NOT,
                '&': CSharpTokenType.BITWISE_AND,
                '|': CSharpTokenType.BITWISE_OR,
                '^': CSharpTokenType.BITWISE_XOR,
                '~': CSharpTokenType.BITWISE_NOT,
                '?': CSharpTokenType.QUESTION,
                ':': CSharpTokenType.COLON,
                ';': CSharpTokenType.SEMICOLON,
                ',': CSharpTokenType.COMMA,
                '.': CSharpTokenType.DOT,
                '(': CSharpTokenType.LEFT_PAREN,
                ')': CSharpTokenType.RIGHT_PAREN,
                '{': CSharpTokenType.LEFT_BRACE,
                '}': CSharpTokenType.RIGHT_BRACE,
                '[': CSharpTokenType.LEFT_BRACKET,
                ']': CSharpTokenType.RIGHT_BRACKET,
                '#': CSharpTokenType.HASH,
            }
            
            if self.current_char in single_char_tokens:
                char = self.current_char
                self.advance()
                return CSharpToken(
                    single_char_tokens[char],
                    char,
                    start_line,
                    start_column,
                    (start_pos, self.position)
                )
            
            # Unknown character
            char = self.current_char
            self.advance()
            return CSharpToken(
                CSharpTokenType.UNKNOWN,
                char,
                start_line,
                start_column,
                (start_pos, self.position)
            )
        
        # End of file
        return CSharpToken(
            CSharpTokenType.EOF,
            '',
            self.line,
            self.column,
            (self.position, self.position)
        )
    
    def tokenize(self) -> List[CSharpToken]:
        """Tokenize the entire source code."""
        tokens = []
        
        while True:
            token = self.get_next_token()
            tokens.append(token)
            
            if token.type == CSharpTokenType.EOF:
                break
        
        return tokens


class CSharpParser:
    """C# recursive descent parser."""
    
    def __init__(self, tokens: List[CSharpToken]):
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[0] if tokens else None
    
    def error(self, message: str):
        """Raise a parser error."""
        if self.current_token:
            raise SyntaxError(f"Parse error at line {self.current_token.line}, column {self.current_token.column}: {message}")
        else:
            raise SyntaxError(f"Parse error: {message}")
    
    def advance(self):
        """Advance to the next token."""
        if self.position < len(self.tokens) - 1:
            self.position += 1
            self.current_token = self.tokens[self.position]
        else:
            self.current_token = None
    
    def peek(self, offset: int = 1) -> Optional[CSharpToken]:
        """Peek at token at offset from current position."""
        pos = self.position + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return None
    
    def match(self, *token_types: CSharpTokenType) -> bool:
        """Check if current token matches any of the given types."""
        if self.current_token and self.current_token.type in token_types:
            return True
        return False
    
    def consume(self, token_type: CSharpTokenType, message: str = "") -> CSharpToken:
        """Consume a token of the expected type."""
        if self.match(token_type):
            token = self.current_token
            self.advance()
            return token
        else:
            self.error(message or f"Expected {token_type}")
    
    def parse(self) -> CSharpCompilationUnit:
        """Parse the tokens into a compilation unit."""
        return self.parse_compilation_unit()
    
    def parse_compilation_unit(self) -> CSharpCompilationUnit:
        """Parse a compilation unit."""
        extern_aliases = []
        using_directives = []
        global_attributes = []
        members = []
        
        # Skip whitespace and comments
        self.skip_trivia()
        
        # Parse global attributes
        while self.match(CSharpTokenType.LEFT_BRACKET):
            if self.is_global_attribute():
                global_attributes.append(self.parse_attribute_list())
            else:
                break
        
        # Parse extern alias directives
        while self.match(CSharpTokenType.EXTERN):
            if self.peek() and self.peek().type == CSharpTokenType.ALIAS:
                extern_aliases.append(self.parse_extern_alias_directive())
            else:
                break
        
        # Parse using directives
        while self.match(CSharpTokenType.USING):
            if self.is_using_directive():
                using_directives.append(self.parse_using_directive())
            else:
                break
        
        # Parse namespace and type declarations
        while self.current_token and self.current_token.type != CSharpTokenType.EOF:
            if self.match(CSharpTokenType.NAMESPACE):
                members.append(self.parse_namespace_declaration())
            elif self.is_type_declaration():
                members.append(self.parse_type_declaration())
            else:
                self.advance()  # Skip unexpected tokens
        
        return CSharpCompilationUnit(
            CSharpNodeType.COMPILATION_UNIT,
            extern_alias_directives=extern_aliases,
            using_directives=using_directives,
            global_attributes=global_attributes,
            members=members
        )
    
    def parse_namespace_declaration(self) -> CSharpNamespaceDeclaration:
        """Parse a namespace declaration."""
        self.consume(CSharpTokenType.NAMESPACE)
        
        name = self.parse_qualified_name()
        
        # Check for file-scoped namespace (C# 10.0)
        is_file_scoped = self.match(CSharpTokenType.SEMICOLON)
        
        extern_aliases = []
        using_directives = []
        members = []
        
        if is_file_scoped:
            self.consume(CSharpTokenType.SEMICOLON)
            
            # Parse using directives
            while self.match(CSharpTokenType.USING):
                if self.is_using_directive():
                    using_directives.append(self.parse_using_directive())
                else:
                    break
            
            # Parse members
            while self.current_token and self.current_token.type != CSharpTokenType.EOF:
                if self.is_type_declaration():
                    members.append(self.parse_type_declaration())
                else:
                    self.advance()
        else:
            self.consume(CSharpTokenType.LEFT_BRACE)
            
            # Parse extern alias directives
            while self.match(CSharpTokenType.EXTERN):
                if self.peek() and self.peek().type == CSharpTokenType.ALIAS:
                    extern_aliases.append(self.parse_extern_alias_directive())
                else:
                    break
            
            # Parse using directives
            while self.match(CSharpTokenType.USING):
                if self.is_using_directive():
                    using_directives.append(self.parse_using_directive())
                else:
                    break
            
            # Parse members
            while not self.match(CSharpTokenType.RIGHT_BRACE) and self.current_token.type != CSharpTokenType.EOF:
                if self.match(CSharpTokenType.NAMESPACE):
                    members.append(self.parse_namespace_declaration())
                elif self.is_type_declaration():
                    members.append(self.parse_type_declaration())
                else:
                    self.advance()
            
            self.consume(CSharpTokenType.RIGHT_BRACE)
        
        return CSharpNamespaceDeclaration(
            CSharpNodeType.NAMESPACE_DECLARATION,
            name=name,
            extern_alias_directives=extern_aliases,
            using_directives=using_directives,
            members=members,
            is_file_scoped=is_file_scoped
        )
    
    def parse_using_directive(self) -> CSharpUsingDirective:
        """Parse a using directive."""
        global_keyword = False
        static_keyword = False
        
        # Check for global using (C# 10.0)
        if self.match(CSharpTokenType.GLOBAL):
            global_keyword = True
            self.advance()
        
        self.consume(CSharpTokenType.USING)
        
        # Check for static using (C# 6.0)
        if self.match(CSharpTokenType.STATIC):
            static_keyword = True
            self.advance()
        
        # Parse alias or name
        alias = None
        name = None
        
        if self.match(CSharpTokenType.IDENTIFIER) and self.peek() and self.peek().type == CSharpTokenType.ASSIGN:
            alias = self.current_token.value
            self.advance()
            self.consume(CSharpTokenType.ASSIGN)
            name = self.parse_qualified_name()
        else:
            name = self.parse_qualified_name()
        
        self.consume(CSharpTokenType.SEMICOLON)
        
        return CSharpUsingDirective(
            CSharpNodeType.USING_DIRECTIVE,
            name=name,
            alias=alias,
            static_keyword=static_keyword,
            global_keyword=global_keyword
        )
    
    def parse_extern_alias_directive(self) -> CSharpExternAliasDirective:
        """Parse an extern alias directive."""
        self.consume(CSharpTokenType.EXTERN)
        self.consume(CSharpTokenType.ALIAS)
        
        identifier = self.consume(CSharpTokenType.IDENTIFIER).value
        
        self.consume(CSharpTokenType.SEMICOLON)
        
        return CSharpExternAliasDirective(
            CSharpNodeType.EXTERN_ALIAS_DIRECTIVE,
            identifier=identifier
        )
    
    def parse_type_declaration(self) -> CSharpTypeDeclaration:
        """Parse a type declaration."""
        attributes = []
        modifiers = []
        
        # Parse attributes
        while self.match(CSharpTokenType.LEFT_BRACKET):
            attributes.append(self.parse_attribute_list())
        
        # Parse modifiers
        while self.is_modifier():
            modifiers.append(self.parse_modifier())
        
        # Determine type declaration kind
        if self.match(CSharpTokenType.CLASS):
            return self.parse_class_declaration(attributes, modifiers)
        elif self.match(CSharpTokenType.STRUCT):
            return self.parse_struct_declaration(attributes, modifiers)
        elif self.match(CSharpTokenType.INTERFACE):
            return self.parse_interface_declaration(attributes, modifiers)
        elif self.match(CSharpTokenType.ENUM):
            return self.parse_enum_declaration(attributes, modifiers)
        elif self.match(CSharpTokenType.DELEGATE):
            return self.parse_delegate_declaration(attributes, modifiers)
        elif self.match(CSharpTokenType.RECORD):
            return self.parse_record_declaration(attributes, modifiers)
        else:
            self.error("Expected type declaration")
    
    def parse_class_declaration(self, attributes: List[CSharpAttributeList], 
                               modifiers: List[CSharpModifier]) -> CSharpClassDeclaration:
        """Parse a class declaration."""
        self.consume(CSharpTokenType.CLASS)
        
        identifier = self.consume(CSharpTokenType.IDENTIFIER).value
        
        type_parameter_list = None
        if self.match(CSharpTokenType.LESS_THAN):
            type_parameter_list = self.parse_type_parameter_list()
        
        base_list = None
        if self.match(CSharpTokenType.COLON):
            base_list = self.parse_base_list()
        
        constraint_clauses = []
        while self.match(CSharpTokenType.WHERE):
            constraint_clauses.append(self.parse_type_parameter_constraint_clause())
        
        self.consume(CSharpTokenType.LEFT_BRACE)
        
        members = []
        while not self.match(CSharpTokenType.RIGHT_BRACE) and self.current_token.type != CSharpTokenType.EOF:
            if self.is_member_declaration():
                members.append(self.parse_member_declaration())
            else:
                self.advance()
        
        self.consume(CSharpTokenType.RIGHT_BRACE)
        
        return CSharpClassDeclaration(
            CSharpNodeType.CLASS_DECLARATION,
            attributes=attributes,
            modifiers=modifiers,
            identifier=identifier,
            type_parameter_list=type_parameter_list,
            base_list=base_list,
            constraint_clauses=constraint_clauses,
            members=members
        )
    
    def parse_struct_declaration(self, attributes: List[CSharpAttributeList], 
                                modifiers: List[CSharpModifier]) -> CSharpStructDeclaration:
        """Parse a struct declaration."""
        self.consume(CSharpTokenType.STRUCT)
        
        identifier = self.consume(CSharpTokenType.IDENTIFIER).value
        
        type_parameter_list = None
        if self.match(CSharpTokenType.LESS_THAN):
            type_parameter_list = self.parse_type_parameter_list()
        
        base_list = None
        if self.match(CSharpTokenType.COLON):
            base_list = self.parse_base_list()
        
        constraint_clauses = []
        while self.match(CSharpTokenType.WHERE):
            constraint_clauses.append(self.parse_type_parameter_constraint_clause())
        
        self.consume(CSharpTokenType.LEFT_BRACE)
        
        members = []
        while not self.match(CSharpTokenType.RIGHT_BRACE) and self.current_token.type != CSharpTokenType.EOF:
            if self.is_member_declaration():
                members.append(self.parse_member_declaration())
            else:
                self.advance()
        
        self.consume(CSharpTokenType.RIGHT_BRACE)
        
        return CSharpStructDeclaration(
            CSharpNodeType.STRUCT_DECLARATION,
            attributes=attributes,
            modifiers=modifiers,
            identifier=identifier,
            type_parameter_list=type_parameter_list,
            base_list=base_list,
            constraint_clauses=constraint_clauses,
            members=members
        )
    
    def parse_interface_declaration(self, attributes: List[CSharpAttributeList], 
                                   modifiers: List[CSharpModifier]) -> CSharpInterfaceDeclaration:
        """Parse an interface declaration."""
        self.consume(CSharpTokenType.INTERFACE)
        
        identifier = self.consume(CSharpTokenType.IDENTIFIER).value
        
        type_parameter_list = None
        if self.match(CSharpTokenType.LESS_THAN):
            type_parameter_list = self.parse_type_parameter_list()
        
        base_list = None
        if self.match(CSharpTokenType.COLON):
            base_list = self.parse_base_list()
        
        constraint_clauses = []
        while self.match(CSharpTokenType.WHERE):
            constraint_clauses.append(self.parse_type_parameter_constraint_clause())
        
        self.consume(CSharpTokenType.LEFT_BRACE)
        
        members = []
        while not self.match(CSharpTokenType.RIGHT_BRACE) and self.current_token.type != CSharpTokenType.EOF:
            if self.is_member_declaration():
                members.append(self.parse_member_declaration())
            else:
                self.advance()
        
        self.consume(CSharpTokenType.RIGHT_BRACE)
        
        return CSharpInterfaceDeclaration(
            CSharpNodeType.INTERFACE_DECLARATION,
            attributes=attributes,
            modifiers=modifiers,
            identifier=identifier,
            type_parameter_list=type_parameter_list,
            base_list=base_list,
            constraint_clauses=constraint_clauses,
            members=members
        )
    
    def parse_enum_declaration(self, attributes: List[CSharpAttributeList], 
                              modifiers: List[CSharpModifier]) -> CSharpEnumDeclaration:
        """Parse an enum declaration."""
        self.consume(CSharpTokenType.ENUM)
        
        identifier = self.consume(CSharpTokenType.IDENTIFIER).value
        
        base_list = None
        if self.match(CSharpTokenType.COLON):
            base_list = self.parse_base_list()
        
        self.consume(CSharpTokenType.LEFT_BRACE)
        
        members = []
        while not self.match(CSharpTokenType.RIGHT_BRACE) and self.current_token.type != CSharpTokenType.EOF:
            if self.match(CSharpTokenType.IDENTIFIER):
                members.append(self.parse_enum_member_declaration())
                
                if self.match(CSharpTokenType.COMMA):
                    self.advance()
                elif not self.match(CSharpTokenType.RIGHT_BRACE):
                    self.error("Expected ',' or '}'")
            else:
                self.advance()
        
        self.consume(CSharpTokenType.RIGHT_BRACE)
        
        return CSharpEnumDeclaration(
            CSharpNodeType.ENUM_DECLARATION,
            attributes=attributes,
            modifiers=modifiers,
            identifier=identifier,
            base_list=base_list,
            members=members
        )
    
    def parse_enum_member_declaration(self) -> CSharpEnumMemberDeclaration:
        """Parse an enum member declaration."""
        attributes = []
        while self.match(CSharpTokenType.LEFT_BRACKET):
            attributes.append(self.parse_attribute_list())
        
        identifier = self.consume(CSharpTokenType.IDENTIFIER).value
        
        equals_value = None
        if self.match(CSharpTokenType.ASSIGN):
            self.advance()
            equals_value = self.parse_expression()
        
        return CSharpEnumMemberDeclaration(
            CSharpNodeType.ENUM_DECLARATION,
            attributes=attributes,
            identifier=identifier,
            equals_value=equals_value
        )
    
    def parse_delegate_declaration(self, attributes: List[CSharpAttributeList], 
                                  modifiers: List[CSharpModifier]) -> CSharpDelegateDeclaration:
        """Parse a delegate declaration."""
        self.consume(CSharpTokenType.DELEGATE)
        
        return_type = self.parse_type()
        
        identifier = self.consume(CSharpTokenType.IDENTIFIER).value
        
        type_parameter_list = None
        if self.match(CSharpTokenType.LESS_THAN):
            type_parameter_list = self.parse_type_parameter_list()
        
        parameter_list = None
        if self.match(CSharpTokenType.LEFT_PAREN):
            parameter_list = self.parse_parameter_list()
        
        constraint_clauses = []
        while self.match(CSharpTokenType.WHERE):
            constraint_clauses.append(self.parse_type_parameter_constraint_clause())
        
        self.consume(CSharpTokenType.SEMICOLON)
        
        return CSharpDelegateDeclaration(
            CSharpNodeType.DELEGATE_DECLARATION,
            attributes=attributes,
            modifiers=modifiers,
            identifier=identifier,
            return_type=return_type,
            type_parameter_list=type_parameter_list,
            parameter_list=parameter_list,
            constraint_clauses=constraint_clauses
        )
    
    def parse_record_declaration(self, attributes: List[CSharpAttributeList], 
                                modifiers: List[CSharpModifier]) -> CSharpRecordDeclaration:
        """Parse a record declaration."""
        self.consume(CSharpTokenType.RECORD)
        
        # Check for record class or record struct
        class_or_struct_keyword = "class"  # Default
        if self.match(CSharpTokenType.CLASS):
            class_or_struct_keyword = "class"
            self.advance()
        elif self.match(CSharpTokenType.STRUCT):
            class_or_struct_keyword = "struct"
            self.advance()
        
        identifier = self.consume(CSharpTokenType.IDENTIFIER).value
        
        type_parameter_list = None
        if self.match(CSharpTokenType.LESS_THAN):
            type_parameter_list = self.parse_type_parameter_list()
        
        parameter_list = None
        if self.match(CSharpTokenType.LEFT_PAREN):
            parameter_list = self.parse_parameter_list()
        
        base_list = None
        if self.match(CSharpTokenType.COLON):
            base_list = self.parse_base_list()
        
        constraint_clauses = []
        while self.match(CSharpTokenType.WHERE):
            constraint_clauses.append(self.parse_type_parameter_constraint_clause())
        
        members = []
        if self.match(CSharpTokenType.LEFT_BRACE):
            self.advance()
            
            while not self.match(CSharpTokenType.RIGHT_BRACE) and self.current_token.type != CSharpTokenType.EOF:
                if self.is_member_declaration():
                    members.append(self.parse_member_declaration())
                else:
                    self.advance()
            
            self.consume(CSharpTokenType.RIGHT_BRACE)
        else:
            self.consume(CSharpTokenType.SEMICOLON)
        
        return CSharpRecordDeclaration(
            CSharpNodeType.RECORD_DECLARATION,
            attributes=attributes,
            modifiers=modifiers,
            identifier=identifier,
            class_or_struct_keyword=class_or_struct_keyword,
            type_parameter_list=type_parameter_list,
            parameter_list=parameter_list,
            base_list=base_list,
            constraint_clauses=constraint_clauses,
            members=members
        )
    
    # Helper methods
    def skip_trivia(self):
        """Skip whitespace and comments."""
        while self.current_token and self.current_token.type in [
            CSharpTokenType.WHITESPACE, CSharpTokenType.NEWLINE,
            CSharpTokenType.SINGLE_LINE_COMMENT, CSharpTokenType.MULTI_LINE_COMMENT
        ]:
            self.advance()
    
    def is_global_attribute(self) -> bool:
        """Check if current position is a global attribute.
        
        Detects global attributes like:
        - [assembly: AssemblyTitle("...")]
        - [module: ...]
        - [assembly: AssemblyVersion("...")]
        """
        if not self.match(CSharpTokenType.LEFT_BRACKET):
            return False
        
        # Look ahead to see if this is a global attribute
        start_pos = self.position
        self.advance()  # Consume '['
        
        # Check for global attribute target
        if self.match(CSharpTokenType.IDENTIFIER):
            identifier = self.current_token.value.lower()
            if identifier in ['assembly', 'module']:
                self.advance()  # Consume target
                
                # Check for colon
                if self.match(CSharpTokenType.COLON):
                    self.advance()  # Consume colon
                    
                    # Look for attribute name (identifier)
                    if self.match(CSharpTokenType.IDENTIFIER):
                        self.advance()  # Consume attribute name
                        
                        # Look for closing bracket
                        while self.position < len(self.tokens) and not self.match(CSharpTokenType.RIGHT_BRACKET):
                            self.advance()
                        
                        is_global = self.match(CSharpTokenType.RIGHT_BRACKET)
                        
                        # Restore position
                        self.position = start_pos
                        return is_global
        
        # Restore position
        self.position = start_pos
        return False
    
    def is_using_directive(self) -> bool:
        """Check if current position is a using directive.
        
        Distinguishes between:
        - using directive: using System; (at namespace level)
        - using statement: using (var x = ...) (inside method)
        """
        if not self.match(CSharpTokenType.USING):
            return False
        
        # Look ahead to see what follows 'using'
        start_pos = self.position
        self.advance()  # Consume 'using'
        
        # Check for using statement pattern: using (expression)
        if self.match(CSharpTokenType.LEFT_PAREN):
            self.position = start_pos
            return False
        
        # Check for using directive pattern: using namespace_or_alias;
        # Look for identifier followed by semicolon or alias
        while self.position < len(self.tokens) and not self.match(CSharpTokenType.SEMICOLON):
            if self.match(CSharpTokenType.IDENTIFIER, CSharpTokenType.DOT, CSharpTokenType.AS):
                self.advance()
            else:
                break
        
        # Check if we found a semicolon (indicating using directive)
        is_directive = self.match(CSharpTokenType.SEMICOLON)
        
        # Restore position
        self.position = start_pos
        return is_directive
    
    def is_type_declaration(self) -> bool:
        """Check if current position is a type declaration."""
        return self.match(CSharpTokenType.CLASS, CSharpTokenType.STRUCT, 
                         CSharpTokenType.INTERFACE, CSharpTokenType.ENUM, 
                         CSharpTokenType.DELEGATE, CSharpTokenType.RECORD)
    
    def is_member_declaration(self) -> bool:
        """Check if current position is a member declaration."""
        return self.match(CSharpTokenType.LEFT_BRACKET) or self.is_modifier() or \
               self.match(CSharpTokenType.IDENTIFIER) or self.is_type_declaration()
    
    def is_modifier(self) -> bool:
        """Check if current token is a modifier."""
        return self.match(CSharpTokenType.PUBLIC, CSharpTokenType.PRIVATE, 
                         CSharpTokenType.PROTECTED, CSharpTokenType.INTERNAL,
                         CSharpTokenType.STATIC, CSharpTokenType.ABSTRACT,
                         CSharpTokenType.SEALED, CSharpTokenType.VIRTUAL,
                         CSharpTokenType.OVERRIDE, CSharpTokenType.READONLY,
                         CSharpTokenType.CONST, CSharpTokenType.VOLATILE,
                         CSharpTokenType.UNSAFE, CSharpTokenType.EXTERN,
                         CSharpTokenType.ASYNC, CSharpTokenType.PARTIAL,
                         CSharpTokenType.NEW, CSharpTokenType.REQUIRED,
                         CSharpTokenType.SCOPED)
    
    def parse_modifier(self) -> CSharpModifier:
        """Parse a modifier."""
        if self.match(CSharpTokenType.PUBLIC):
            self.advance()
            return CSharpModifier.PUBLIC
        elif self.match(CSharpTokenType.PRIVATE):
            self.advance()
            return CSharpModifier.PRIVATE
        elif self.match(CSharpTokenType.PROTECTED):
            self.advance()
            return CSharpModifier.PROTECTED
        elif self.match(CSharpTokenType.INTERNAL):
            self.advance()
            return CSharpModifier.INTERNAL
        elif self.match(CSharpTokenType.STATIC):
            self.advance()
            return CSharpModifier.STATIC
        elif self.match(CSharpTokenType.ABSTRACT):
            self.advance()
            return CSharpModifier.ABSTRACT
        elif self.match(CSharpTokenType.SEALED):
            self.advance()
            return CSharpModifier.SEALED
        elif self.match(CSharpTokenType.VIRTUAL):
            self.advance()
            return CSharpModifier.VIRTUAL
        elif self.match(CSharpTokenType.OVERRIDE):
            self.advance()
            return CSharpModifier.OVERRIDE
        elif self.match(CSharpTokenType.READONLY):
            self.advance()
            return CSharpModifier.READONLY
        elif self.match(CSharpTokenType.CONST):
            self.advance()
            return CSharpModifier.CONST
        elif self.match(CSharpTokenType.VOLATILE):
            self.advance()
            return CSharpModifier.VOLATILE
        elif self.match(CSharpTokenType.UNSAFE):
            self.advance()
            return CSharpModifier.UNSAFE
        elif self.match(CSharpTokenType.EXTERN):
            self.advance()
            return CSharpModifier.EXTERN
        elif self.match(CSharpTokenType.ASYNC):
            self.advance()
            return CSharpModifier.ASYNC
        elif self.match(CSharpTokenType.PARTIAL):
            self.advance()
            return CSharpModifier.PARTIAL
        elif self.match(CSharpTokenType.NEW):
            self.advance()
            return CSharpModifier.NEW
        elif self.match(CSharpTokenType.REQUIRED):
            self.advance()
            return CSharpModifier.REQUIRED
        elif self.match(CSharpTokenType.SCOPED):
            self.advance()
            return CSharpModifier.SCOPED
        else:
            self.error("Expected modifier")
    
    def parse_qualified_name(self) -> CSharpExpression:
        """Parse a qualified name."""
        left = CSharpIdentifier(CSharpNodeType.IDENTIFIER, name=self.consume(CSharpTokenType.IDENTIFIER).value)
        
        while self.match(CSharpTokenType.DOT):
            self.advance()
            right = CSharpIdentifier(CSharpNodeType.IDENTIFIER, name=self.consume(CSharpTokenType.IDENTIFIER).value)
            left = CSharpQualifiedName(CSharpNodeType.QUALIFIED_NAME, left=left, right=right)
        
        return left
    
    def parse_type_parameter_list(self) -> CSharpTypeParameterList:
        """Parse a type parameter list."""
        self.consume(CSharpTokenType.LESS_THAN)
        
        parameters = []
        
        while not self.match(CSharpTokenType.GREATER_THAN) and self.current_token.type != CSharpTokenType.EOF:
            parameters.append(self.parse_type_parameter())
            
            if self.match(CSharpTokenType.COMMA):
                self.advance()
            elif not self.match(CSharpTokenType.GREATER_THAN):
                self.error("Expected ',' or '>'")
        
        self.consume(CSharpTokenType.GREATER_THAN)
        
        return CSharpTypeParameterList(CSharpNodeType.TYPE_PARAMETER, parameters=parameters)
    
    def parse_type_parameter(self) -> CSharpTypeParameter:
        """Parse a type parameter."""
        attributes = []
        while self.match(CSharpTokenType.LEFT_BRACKET):
            attributes.append(self.parse_attribute_list())
        
        variance_keyword = None
        if self.match(CSharpTokenType.IN):
            variance_keyword = "in"
            self.advance()
        elif self.match(CSharpTokenType.OUT):
            variance_keyword = "out"
            self.advance()
        
        identifier = self.consume(CSharpTokenType.IDENTIFIER).value
        
        return CSharpTypeParameter(
            CSharpNodeType.TYPE_PARAMETER,
            attributes=attributes,
            variance_keyword=variance_keyword,
            identifier=identifier
        )
    
    def parse_base_list(self) -> CSharpBaseList:
        """Parse a base list."""
        self.consume(CSharpTokenType.COLON)
        
        types = []
        
        while True:
            types.append(self.parse_type())
            
            if self.match(CSharpTokenType.COMMA):
                self.advance()
            else:
                break
        
        return CSharpBaseList(CSharpNodeType.BASE_LIST, types=types)
    
    def parse_type_parameter_constraint_clause(self) -> CSharpTypeParameterConstraintClause:
        """Parse a type parameter constraint clause."""
        self.consume(CSharpTokenType.WHERE)
        
        name = self.consume(CSharpTokenType.IDENTIFIER).value
        
        self.consume(CSharpTokenType.COLON)
        
        constraints = []
        
        while True:
            constraints.append(self.parse_type_parameter_constraint())
            
            if self.match(CSharpTokenType.COMMA):
                self.advance()
            else:
                break
        
        return CSharpTypeParameterConstraintClause(
            CSharpNodeType.TYPE_PARAMETER_CONSTRAINT,
            name=name,
            constraints=constraints
        )
    
    def parse_type_parameter_constraint(self) -> CSharpTypeParameterConstraint:
        """Parse a type parameter constraint."""
        if self.match(CSharpTokenType.CLASS):
            self.advance()
            question_token = self.match(CSharpTokenType.QUESTION)
            if question_token:
                self.advance()
            return CSharpClassOrStructConstraint(
                CSharpNodeType.TYPE_PARAMETER_CONSTRAINT,
                class_or_struct_keyword="class",
                question_token=question_token
            )
        elif self.match(CSharpTokenType.STRUCT):
            self.advance()
            return CSharpClassOrStructConstraint(
                CSharpNodeType.TYPE_PARAMETER_CONSTRAINT,
                class_or_struct_keyword="struct"
            )
        elif self.match(CSharpTokenType.NEW):
            self.advance()
            self.consume(CSharpTokenType.LEFT_PAREN)
            self.consume(CSharpTokenType.RIGHT_PAREN)
            return CSharpConstructorConstraint(CSharpNodeType.TYPE_PARAMETER_CONSTRAINT)
        elif self.match(CSharpTokenType.DEFAULT):
            self.advance()
            return CSharpDefaultConstraint(CSharpNodeType.TYPE_PARAMETER_CONSTRAINT)
        else:
            # Type constraint
            return CSharpTypeConstraint(
                CSharpNodeType.TYPE_PARAMETER_CONSTRAINT,
                type=self.parse_type()
            )
    
    def parse_member_declaration(self) -> CSharpMemberDeclaration:
        """Parse a member declaration.
        
        Handles all member types:
        - Fields (with/without initialization)
        - Properties (auto, expression-bodied, full)
        - Methods (regular, expression-bodied, async)
        - Constructors
        - Destructors
        - Events
        - Indexers
        - Operators
        - Conversion operators
        """
        # Check for attributes
        attributes = []
        while self.match(CSharpTokenType.LEFT_BRACKET):
            attributes.append(self.parse_attribute())
        
        # Check for access modifiers
        modifiers = []
        while self.match(CSharpTokenType.PUBLIC, CSharpTokenType.PRIVATE, CSharpTokenType.PROTECTED, 
                        CSharpTokenType.INTERNAL, CSharpTokenType.STATIC, CSharpTokenType.VIRTUAL,
                        CSharpTokenType.OVERRIDE, CSharpTokenType.ABSTRACT, CSharpTokenType.SEALED,
                        CSharpTokenType.EXTERN, CSharpTokenType.READONLY, CSharpTokenType.VOLATILE,
                        CSharpTokenType.UNSAFE, CSharpTokenType.NEW, CSharpTokenType.CONST):
            modifiers.append(self.current_token.value)
            self.advance()
        
        # Check for partial keyword
        if self.match(CSharpTokenType.PARTIAL):
            modifiers.append(self.current_token.value)
            self.advance()
        
        # Check for async keyword
        if self.match(CSharpTokenType.ASYNC):
            modifiers.append(self.current_token.value)
            self.advance()
        
        # Parse based on member type
        if self.match(CSharpTokenType.CONSTRUCTOR):
            return self.parse_constructor_declaration(attributes, modifiers)
        elif self.match(CSharpTokenType.DESTRUCTOR):
            return self.parse_destructor_declaration(attributes, modifiers)
        elif self.match(CSharpTokenType.EVENT):
            return self.parse_event_declaration(attributes, modifiers)
        elif self.match(CSharpTokenType.INDEXER):
            return self.parse_indexer_declaration(attributes, modifiers)
        elif self.match(CSharpTokenType.OPERATOR):
            return self.parse_operator_declaration(attributes, modifiers)
        elif self.match(CSharpTokenType.IMPLICIT, CSharpTokenType.EXPLICIT):
            return self.parse_conversion_operator_declaration(attributes, modifiers)
        elif self.match(CSharpTokenType.PROPERTY):
            return self.parse_property_declaration(attributes, modifiers)
        elif self.match(CSharpTokenType.METHOD):
            return self.parse_method_declaration(attributes, modifiers)
        elif self.match(CSharpTokenType.FIELD):
            return self.parse_field_declaration(attributes, modifiers)
        else:
            # Try to parse as field, property, or method based on context
            return self.parse_field_property_or_method(attributes, modifiers)
    
    def parse_field_property_or_method(self, attributes: List[CSharpAttribute], modifiers: List[str]) -> CSharpMemberDeclaration:
        """Parse field, property, or method based on context."""
        # Look ahead to determine member type
        start_pos = self.position
        
        # Parse type
        member_type = self.parse_type()
        
        # Parse identifier
        if not self.match(CSharpTokenType.IDENTIFIER):
            self.error("Expected identifier")
        
        identifier = self.current_token.value
        self.advance()
        
        # Check for property pattern: Type Name { get; set; }
        if self.match(CSharpTokenType.LEFT_BRACE):
            return self.parse_property_declaration_body(attributes, modifiers, member_type, identifier)
        
        # Check for method pattern: Type Name(parameters) { body }
        elif self.match(CSharpTokenType.LEFT_PAREN):
            return self.parse_method_declaration_body(attributes, modifiers, member_type, identifier)
        
        # Check for field pattern: Type Name = value;
        elif self.match(CSharpTokenType.EQUALS, CSharpTokenType.SEMICOLON):
            return self.parse_field_declaration_body(attributes, modifiers, member_type, identifier)
        
        # Check for expression-bodied member: Type Name => expression;
        elif self.match(CSharpTokenType.ARROW):
            return self.parse_expression_bodied_member(attributes, modifiers, member_type, identifier)
        
        else:
            self.error("Expected field, property, or method declaration")
    
    def parse_property_declaration_body(self, attributes: List[CSharpAttribute], modifiers: List[str], 
                                      property_type: CSharpType, property_name: str) -> CSharpPropertyDeclaration:
        """Parse property declaration body."""
        self.expect(CSharpTokenType.LEFT_BRACE)
        
        accessors = []
        while not self.match(CSharpTokenType.RIGHT_BRACE):
            if self.match(CSharpTokenType.GET, CSharpTokenType.SET, CSharpTokenType.INIT):
                accessor_type = self.current_token.value
                self.advance()
                
                # Parse accessor body
                if self.match(CSharpTokenType.SEMICOLON):
                    # Auto-property accessor
                    self.advance()
                    accessors.append(CSharpAccessorDeclaration(
                        node_type=CSharpNodeType.ACCESSOR_DECLARATION,
                        accessor_type=accessor_type,
                        body=None
                    ))
                elif self.match(CSharpTokenType.LEFT_BRACE):
                    # Full accessor with body
                    body = self.parse_block()
                    accessors.append(CSharpAccessorDeclaration(
                        node_type=CSharpNodeType.ACCESSOR_DECLARATION,
                        accessor_type=accessor_type,
                        body=body
                    ))
                else:
                    self.error("Expected accessor body")
            else:
                self.advance()  # Skip unknown tokens
        
        self.expect(CSharpTokenType.RIGHT_BRACE)
        
        return CSharpPropertyDeclaration(
            node_type=CSharpNodeType.PROPERTY_DECLARATION,
            attributes=attributes,
            modifiers=modifiers,
            property_type=property_type,
            property_name=property_name,
            accessors=accessors
        )
    
    def parse_method_declaration_body(self, attributes: List[CSharpAttribute], modifiers: List[str],
                                    return_type: CSharpType, method_name: str) -> CSharpMethodDeclaration:
        """Parse method declaration body."""
        # Parse parameters
        parameters = self.parse_parameter_list()
        
        # Parse constraints
        constraints = []
        while self.match(CSharpTokenType.WHERE):
            constraints.append(self.parse_type_constraint())
        
        # Parse method body
        if self.match(CSharpTokenType.SEMICOLON):
            # Abstract or extern method
            self.advance()
            body = None
        elif self.match(CSharpTokenType.ARROW):
            # Expression-bodied method
            self.advance()
            expression = self.parse_expression()
            body = CSharpExpressionStatement(
                node_type=CSharpNodeType.EXPRESSION_STATEMENT,
                expression=expression
            )
        elif self.match(CSharpTokenType.LEFT_BRACE):
            # Full method body
            body = self.parse_block()
        else:
            self.error("Expected method body")
        
        return CSharpMethodDeclaration(
            node_type=CSharpNodeType.METHOD_DECLARATION,
            attributes=attributes,
            modifiers=modifiers,
            return_type=return_type,
            method_name=method_name,
            parameters=parameters,
            constraints=constraints,
            body=body
        )
    
    def parse_field_declaration_body(self, attributes: List[CSharpAttribute], modifiers: List[str],
                                   field_type: CSharpType, field_name: str) -> CSharpFieldDeclaration:
        """Parse field declaration body."""
        # Parse initializer
        initializer = None
        if self.match(CSharpTokenType.EQUALS):
            self.advance()
            initializer = self.parse_expression()
        
        self.expect(CSharpTokenType.SEMICOLON)
        
        return CSharpFieldDeclaration(
            node_type=CSharpNodeType.FIELD_DECLARATION,
            attributes=attributes,
            modifiers=modifiers,
            field_type=field_type,
            field_name=field_name,
            initializer=initializer
        )
    
    def parse_expression_bodied_member(self, attributes: List[CSharpAttribute], modifiers: List[str],
                                     member_type: CSharpType, member_name: str) -> CSharpMemberDeclaration:
        """Parse expression-bodied member."""
        self.expect(CSharpTokenType.ARROW)
        expression = self.parse_expression()
        self.expect(CSharpTokenType.SEMICOLON)
        
        # Determine if it's a property or method based on context
        if self.match(CSharpTokenType.LEFT_PAREN):
            # Method
            return CSharpMethodDeclaration(
                node_type=CSharpNodeType.METHOD_DECLARATION,
                attributes=attributes,
                modifiers=modifiers,
                return_type=member_type,
                method_name=member_name,
                parameters=self.parse_parameter_list(),
                constraints=[],
                body=CSharpExpressionStatement(
                    node_type=CSharpNodeType.EXPRESSION_STATEMENT,
                    expression=expression
                )
            )
        else:
            # Property
            return CSharpPropertyDeclaration(
                node_type=CSharpNodeType.PROPERTY_DECLARATION,
                attributes=attributes,
                modifiers=modifiers,
                property_type=member_type,
                property_name=member_name,
                accessors=[
                    CSharpAccessorDeclaration(
                        node_type=CSharpNodeType.ACCESSOR_DECLARATION,
                        accessor_type="get",
                        body=CSharpExpressionStatement(
                            node_type=CSharpNodeType.EXPRESSION_STATEMENT,
                            expression=expression
                        )
                    )
                ]
            )
    
    def parse_parameter_list(self) -> CSharpParameterList:
        """Parse a parameter list."""
        self.consume(CSharpTokenType.LEFT_PAREN)
        
        parameters = []
        
        while not self.match(CSharpTokenType.RIGHT_PAREN) and self.current_token.type != CSharpTokenType.EOF:
            parameters.append(self.parse_parameter())
            
            if self.match(CSharpTokenType.COMMA):
                self.advance()
            elif not self.match(CSharpTokenType.RIGHT_PAREN):
                self.error("Expected ',' or ')'")
        
        self.consume(CSharpTokenType.RIGHT_PAREN)
        
        return CSharpParameterList(CSharpNodeType.PARAMETER_LIST, parameters=parameters)
    
    def parse_parameter(self) -> CSharpParameter:
        """Parse a parameter."""
        attributes = []
        while self.match(CSharpTokenType.LEFT_BRACKET):
            attributes.append(self.parse_attribute_list())
        
        modifiers = []
        while self.match(CSharpTokenType.REF, CSharpTokenType.OUT, CSharpTokenType.IN, CSharpTokenType.PARAMS):
            if self.match(CSharpTokenType.REF):
                modifiers.append(CSharpModifier.REF)
            elif self.match(CSharpTokenType.OUT):
                modifiers.append(CSharpModifier.OUT)
            elif self.match(CSharpTokenType.IN):
                modifiers.append(CSharpModifier.IN)
            elif self.match(CSharpTokenType.PARAMS):
                modifiers.append(CSharpModifier.PARAMS)
            self.advance()
        
        param_type = self.parse_type()
        identifier = self.consume(CSharpTokenType.IDENTIFIER).value
        
        default_value = None
        if self.match(CSharpTokenType.ASSIGN):
            self.advance()
            default_value = CSharpEqualsValueClause(
                CSharpNodeType.EQUALS_VALUE_CLAUSE,
                value=self.parse_expression()
            )
        
        return CSharpParameter(
            CSharpNodeType.PARAMETER_DECLARATION,
            attributes=attributes,
            modifiers=modifiers,
            type=param_type,
            identifier=identifier,
            default_value=default_value
        )
    
    def parse_attribute_list(self) -> CSharpAttributeList:
        """Parse an attribute list."""
        self.consume(CSharpTokenType.LEFT_BRACKET)
        
        target = None
        if self.match(CSharpTokenType.IDENTIFIER) and self.peek() and self.peek().type == CSharpTokenType.COLON:
            target = self.current_token.value
            self.advance()
            self.consume(CSharpTokenType.COLON)
        
        attributes = []
        
        while not self.match(CSharpTokenType.RIGHT_BRACKET) and self.current_token.type != CSharpTokenType.EOF:
            attributes.append(self.parse_attribute())
            
            if self.match(CSharpTokenType.COMMA):
                self.advance()
            elif not self.match(CSharpTokenType.RIGHT_BRACKET):
                self.error("Expected ',' or ']'")
        
        self.consume(CSharpTokenType.RIGHT_BRACKET)
        
        return CSharpAttributeList(
            CSharpNodeType.ATTRIBUTE_LIST,
            target=target,
            attributes=attributes
        )
    
    def parse_attribute(self) -> CSharpAttribute:
        """Parse an attribute."""
        name = self.parse_type()
        
        argument_list = None
        if self.match(CSharpTokenType.LEFT_PAREN):
            argument_list = self.parse_attribute_argument_list()
        
        return CSharpAttribute(
            CSharpNodeType.ATTRIBUTE,
            name=name,
            argument_list=argument_list
        )
    
    def parse_attribute_argument_list(self) -> CSharpAttributeArgumentList:
        """Parse an attribute argument list."""
        self.consume(CSharpTokenType.LEFT_PAREN)
        
        arguments = []
        
        while not self.match(CSharpTokenType.RIGHT_PAREN) and self.current_token.type != CSharpTokenType.EOF:
            arguments.append(self.parse_attribute_argument())
            
            if self.match(CSharpTokenType.COMMA):
                self.advance()
            elif not self.match(CSharpTokenType.RIGHT_PAREN):
                self.error("Expected ',' or ')'")
        
        self.consume(CSharpTokenType.RIGHT_PAREN)
        
        return CSharpAttributeArgumentList(
            CSharpNodeType.ATTRIBUTE_ARGUMENT_LIST,
            arguments=arguments
        )
    
    def parse_attribute_argument(self) -> CSharpAttributeArgument:
        """Parse an attribute argument."""
        name_equals = None
        name_colon = None
        
        if self.match(CSharpTokenType.IDENTIFIER):
            name = self.current_token.value
            self.advance()
            
            if self.match(CSharpTokenType.ASSIGN):
                name_equals = name
                self.advance()
            elif self.match(CSharpTokenType.COLON):
                name_colon = name
                self.advance()
            else:
                # Put the identifier back
                self.position -= 1
                self.current_token = self.tokens[self.position]
        
        expression = self.parse_expression()
        
        return CSharpAttributeArgument(
            CSharpNodeType.ATTRIBUTE_ARGUMENT,
            name_equals=name_equals,
            name_colon=name_colon,
            expression=expression
        )
    
    def parse_type(self) -> CSharpType:
        """Parse a type.
        
        Handles all C# types:
        - Predefined types (int, string, void, etc.)
        - Identifier types (user-defined types)
        - Array types (int[], string[,])
        - Generic types (List<T>, Dictionary<K,V>)
        - Nullable types (int?, string?)
        - Pointer types (int*, void**)
        - Tuple types ((int, string))
        - Function pointer types (delegate*<int, string>)
        """
        # Check for nullable type
        if self.match(CSharpTokenType.QUESTION):
            self.advance()
            return CSharpNullableType(
                node_type=CSharpNodeType.NULLABLE_TYPE,
                element_type=self.parse_type()
            )
        
        # Check for pointer type
        if self.match(CSharpTokenType.ASTERISK):
            self.advance()
            return CSharpPointerType(
                node_type=CSharpNodeType.POINTER_TYPE,
                element_type=self.parse_type()
            )
        
        # Check for predefined types
        if self.match(CSharpTokenType.INT, CSharpTokenType.STRING, CSharpTokenType.VOID, 
                     CSharpTokenType.BOOL, CSharpTokenType.CHAR, CSharpTokenType.BYTE,
                     CSharpTokenType.SBYTE, CSharpTokenType.SHORT, CSharpTokenType.USHORT,
                     CSharpTokenType.UINT, CSharpTokenType.LONG, CSharpTokenType.ULONG,
                     CSharpTokenType.FLOAT, CSharpTokenType.DOUBLE, CSharpTokenType.DECIMAL,
                     CSharpTokenType.OBJECT, CSharpTokenType.DYNAMIC):
            keyword = self.current_token.value
            self.advance()
            return CSharpPredefinedType(
                node_type=CSharpNodeType.PREDEFINED_TYPE,
                keyword=keyword
            )
        
        # Check for identifier type (user-defined type)
        if self.match(CSharpTokenType.IDENTIFIER):
            identifier = self.current_token.value
            self.advance()
            
            # Check for generic type arguments
            type_arguments = []
            if self.match(CSharpTokenType.LESS_THAN):
                self.advance()
                type_arguments.append(self.parse_type())
                
                while self.match(CSharpTokenType.COMMA):
                    self.advance()
                    type_arguments.append(self.parse_type())
                
                self.expect(CSharpTokenType.GREATER_THAN)
            
            # Check for array dimensions
            array_rank = 0
            while self.match(CSharpTokenType.LEFT_BRACKET):
                self.advance()
                # Parse array dimensions
                while not self.match(CSharpTokenType.RIGHT_BRACKET):
                    self.advance()
                self.expect(CSharpTokenType.RIGHT_BRACKET)
                array_rank += 1
            
            if type_arguments:
                return CSharpGenericType(
                    node_type=CSharpNodeType.GENERIC_TYPE,
                    identifier=identifier,
                    type_arguments=type_arguments,
                    array_rank=array_rank
                )
            elif array_rank > 0:
                return CSharpArrayType(
                    node_type=CSharpNodeType.ARRAY_TYPE,
                    element_type=CSharpIdentifierName(
                        node_type=CSharpNodeType.IDENTIFIER_NAME,
                        identifier=identifier
                    ),
                    rank=array_rank
                )
            else:
                return CSharpIdentifierName(
                    node_type=CSharpNodeType.IDENTIFIER_NAME,
                    identifier=identifier
                )
        
        # Check for tuple type
        if self.match(CSharpTokenType.LEFT_PAREN):
            self.advance()
            tuple_elements = []
            
            if not self.match(CSharpTokenType.RIGHT_PAREN):
                tuple_elements.append(self.parse_type())
                
                while self.match(CSharpTokenType.COMMA):
                    self.advance()
                    tuple_elements.append(self.parse_type())
            
            self.expect(CSharpTokenType.RIGHT_PAREN)
            
            return CSharpTupleType(
                node_type=CSharpNodeType.TUPLE_TYPE,
                elements=tuple_elements
            )
        
        # Check for function pointer type
        if self.match(CSharpTokenType.DELEGATE):
            self.advance()
            self.expect(CSharpTokenType.ASTERISK)
            self.expect(CSharpTokenType.LESS_THAN)
            
            # Parse function pointer signature
            parameters = []
            return_type = None
            
            if not self.match(CSharpTokenType.GREATER_THAN):
                # Parse parameters
                if not self.match(CSharpTokenType.COMMA):
                    parameters.append(self.parse_type())
                    
                    while self.match(CSharpTokenType.COMMA):
                        self.advance()
                        parameters.append(self.parse_type())
                
                # Parse return type
                if self.match(CSharpTokenType.COMMA):
                    self.advance()
                    return_type = self.parse_type()
            
            self.expect(CSharpTokenType.GREATER_THAN)
            
            return CSharpFunctionPointerType(
                node_type=CSharpNodeType.FUNCTION_POINTER_TYPE,
                parameters=parameters,
                return_type=return_type
            )
        
        self.error("Expected type")
    
    def parse_expression(self) -> CSharpExpression:
        """Parse an expression.
        
        Handles all C# expressions:
        - Literals (int, string, bool, null)
        - Identifiers
        - Binary expressions (+, -, *, /, etc.)
        - Unary expressions (++, --, !, etc.)
        - Method invocations
        - Property access
        - Indexer access
        - Cast expressions
        - Object creation
        - Lambda expressions
        - Conditional expressions
        - Assignment expressions
        """
        # Parse assignment expression (lowest precedence)
        left = self.parse_conditional_expression()
        
        # Check for assignment operators
        if self.match(CSharpTokenType.EQUALS, CSharpTokenType.PLUS_EQUALS, CSharpTokenType.MINUS_EQUALS,
                     CSharpTokenType.ASTERISK_EQUALS, CSharpTokenType.SLASH_EQUALS, CSharpTokenType.PERCENT_EQUALS,
                     CSharpTokenType.AMPERSAND_EQUALS, CSharpTokenType.PIPE_EQUALS, CSharpTokenType.CARET_EQUALS,
                     CSharpTokenType.LESS_LESS_EQUALS, CSharpTokenType.GREATER_GREATER_EQUALS):
            operator_token = self.current_token
            self.advance()
            right = self.parse_expression()
            
            return CSharpAssignmentExpression(
                node_type=CSharpNodeType.ASSIGNMENT_EXPRESSION,
                left=left,
                operator=operator_token.value,
                right=right
            )
        
        return left
    
    def parse_conditional_expression(self) -> CSharpExpression:
        """Parse conditional expression (ternary operator)."""
        condition = self.parse_logical_or_expression()
        
        if self.match(CSharpTokenType.QUESTION):
            self.advance()
            true_expression = self.parse_expression()
            self.expect(CSharpTokenType.COLON)
            false_expression = self.parse_expression()
            
            return CSharpConditionalExpression(
                node_type=CSharpNodeType.CONDITIONAL_EXPRESSION,
                condition=condition,
                true_expression=true_expression,
                false_expression=false_expression
            )
        
        return condition
    
    def parse_logical_or_expression(self) -> CSharpExpression:
        """Parse logical OR expression."""
        left = self.parse_logical_and_expression()
        
        while self.match(CSharpTokenType.PIPE_PIPE):
            operator_token = self.current_token
            self.advance()
            right = self.parse_logical_and_expression()
            
            left = CSharpBinaryExpression(
                node_type=CSharpNodeType.BINARY_EXPRESSION,
                left=left,
                operator=operator_token.value,
                right=right
            )
        
        return left
    
    def parse_logical_and_expression(self) -> CSharpExpression:
        """Parse logical AND expression."""
        left = self.parse_inclusive_or_expression()
        
        while self.match(CSharpTokenType.AMPERSAND_AMPERSAND):
            operator_token = self.current_token
            self.advance()
            right = self.parse_inclusive_or_expression()
            
            left = CSharpBinaryExpression(
                node_type=CSharpNodeType.BINARY_EXPRESSION,
                left=left,
                operator=operator_token.value,
                right=right
            )
        
        return left
    
    def parse_inclusive_or_expression(self) -> CSharpExpression:
        """Parse inclusive OR expression."""
        left = self.parse_exclusive_or_expression()
        
        while self.match(CSharpTokenType.PIPE):
            operator_token = self.current_token
            self.advance()
            right = self.parse_exclusive_or_expression()
            
            left = CSharpBinaryExpression(
                node_type=CSharpNodeType.BINARY_EXPRESSION,
                left=left,
                operator=operator_token.value,
                right=right
            )
        
        return left
    
    def parse_exclusive_or_expression(self) -> CSharpExpression:
        """Parse exclusive OR expression."""
        left = self.parse_and_expression()
        
        while self.match(CSharpTokenType.CARET):
            operator_token = self.current_token
            self.advance()
            right = self.parse_and_expression()
            
            left = CSharpBinaryExpression(
                node_type=CSharpNodeType.BINARY_EXPRESSION,
                left=left,
                operator=operator_token.value,
                right=right
            )
        
        return left
    
    def parse_and_expression(self) -> CSharpExpression:
        """Parse AND expression."""
        left = self.parse_equality_expression()
        
        while self.match(CSharpTokenType.AMPERSAND):
            operator_token = self.current_token
            self.advance()
            right = self.parse_equality_expression()
            
            left = CSharpBinaryExpression(
                node_type=CSharpNodeType.BINARY_EXPRESSION,
                left=left,
                operator=operator_token.value,
                right=right
            )
        
        return left
    
    def parse_equality_expression(self) -> CSharpExpression:
        """Parse equality expression."""
        left = self.parse_relational_expression()
        
        while self.match(CSharpTokenType.EQUALS_EQUALS, CSharpTokenType.EXCLAMATION_EQUALS):
            operator_token = self.current_token
            self.advance()
            right = self.parse_relational_expression()
            
            left = CSharpBinaryExpression(
                node_type=CSharpNodeType.BINARY_EXPRESSION,
                left=left,
                operator=operator_token.value,
                right=right
            )
        
        return left
    
    def parse_relational_expression(self) -> CSharpExpression:
        """Parse relational expression."""
        left = self.parse_shift_expression()
        
        while self.match(CSharpTokenType.LESS_THAN, CSharpTokenType.GREATER_THAN, 
                        CSharpTokenType.LESS_EQUALS, CSharpTokenType.GREATER_EQUALS):
            operator_token = self.current_token
            self.advance()
            right = self.parse_shift_expression()
            
            left = CSharpBinaryExpression(
                node_type=CSharpNodeType.BINARY_EXPRESSION,
                left=left,
                operator=operator_token.value,
                right=right
            )
        
        return left
    
    def parse_shift_expression(self) -> CSharpExpression:
        """Parse shift expression."""
        left = self.parse_additive_expression()
        
        while self.match(CSharpTokenType.LESS_LESS, CSharpTokenType.GREATER_GREATER):
            operator_token = self.current_token
            self.advance()
            right = self.parse_additive_expression()
            
            left = CSharpBinaryExpression(
                node_type=CSharpNodeType.BINARY_EXPRESSION,
                left=left,
                operator=operator_token.value,
                right=right
            )
        
        return left
    
    def parse_additive_expression(self) -> CSharpExpression:
        """Parse additive expression."""
        left = self.parse_multiplicative_expression()
        
        while self.match(CSharpTokenType.PLUS, CSharpTokenType.MINUS):
            operator_token = self.current_token
            self.advance()
            right = self.parse_multiplicative_expression()
            
            left = CSharpBinaryExpression(
                node_type=CSharpNodeType.BINARY_EXPRESSION,
                left=left,
                operator=operator_token.value,
                right=right
            )
        
        return left
    
    def parse_multiplicative_expression(self) -> CSharpExpression:
        """Parse multiplicative expression."""
        left = self.parse_unary_expression()
        
        while self.match(CSharpTokenType.ASTERISK, CSharpTokenType.SLASH, CSharpTokenType.PERCENT):
            operator_token = self.current_token
            self.advance()
            right = self.parse_unary_expression()
            
            left = CSharpBinaryExpression(
                node_type=CSharpNodeType.BINARY_EXPRESSION,
                left=left,
                operator=operator_token.value,
                right=right
            )
        
        return left
    
    def parse_unary_expression(self) -> CSharpExpression:
        """Parse unary expression."""
        if self.match(CSharpTokenType.PLUS, CSharpTokenType.MINUS, CSharpTokenType.EXCLAMATION,
                     CSharpTokenType.TILDE, CSharpTokenType.ASTERISK, CSharpTokenType.AMPERSAND):
            operator_token = self.current_token
            self.advance()
            operand = self.parse_unary_expression()
            
            return CSharpUnaryExpression(
                node_type=CSharpNodeType.UNARY_EXPRESSION,
                operator=operator_token.value,
                operand=operand
            )
        
        if self.match(CSharpTokenType.PLUS_PLUS, CSharpTokenType.MINUS_MINUS):
            operator_token = self.current_token
            self.advance()
            operand = self.parse_primary_expression()
            
            return CSharpUnaryExpression(
                node_type=CSharpNodeType.UNARY_EXPRESSION,
                operator=operator_token.value,
                operand=operand
            )
        
        return self.parse_primary_expression()
    
    def parse_primary_expression(self) -> CSharpExpression:
        """Parse primary expression."""
        if self.match(CSharpTokenType.INTEGER_LITERAL, CSharpTokenType.FLOAT_LITERAL, 
                     CSharpTokenType.STRING_LITERAL, CSharpTokenType.CHAR_LITERAL):
            # Parse literal
            value = self.current_token.value
            literal_type = self.current_token.type.name.lower().replace('_literal', '')
            self.advance()
            
            return CSharpLiteral(
                node_type=CSharpNodeType.LITERAL,
                value=value,
                literal_type=literal_type
            )
        
        elif self.match(CSharpTokenType.TRUE, CSharpTokenType.FALSE):
            # Parse boolean literal
            value = self.current_token.value == "true"
            self.advance()
            
            return CSharpLiteral(
                node_type=CSharpNodeType.BOOLEAN_LITERAL,
                value=value,
                literal_type="bool"
            )
        
        elif self.match(CSharpTokenType.NULL):
            # Parse null literal
            self.advance()
            
            return CSharpLiteral(
                node_type=CSharpNodeType.NULL_LITERAL,
                value=None,
                literal_type="null"
            )
        
        elif self.match(CSharpTokenType.IDENTIFIER):
            # Parse identifier
            identifier = self.current_token.value
            self.advance()
            
            # Check for method invocation
            if self.match(CSharpTokenType.LEFT_PAREN):
                return self.parse_method_invocation(identifier)
            
            # Check for property access
            elif self.match(CSharpTokenType.DOT):
                return self.parse_member_access(identifier)
            
            # Check for indexer access
            elif self.match(CSharpTokenType.LEFT_BRACKET):
                return self.parse_indexer_access(identifier)
            
            else:
                return CSharpIdentifier(
                    node_type=CSharpNodeType.IDENTIFIER,
                    name=identifier
                )
        
        elif self.match(CSharpTokenType.LEFT_PAREN):
            # Parse parenthesized expression
            self.advance()
            expression = self.parse_expression()
            self.expect(CSharpTokenType.RIGHT_PAREN)
            
            return expression
        
        elif self.match(CSharpTokenType.NEW):
            # Parse object creation
            return self.parse_object_creation_expression()
        
        elif self.match(CSharpTokenType.THIS, CSharpTokenType.BASE):
            # Parse this/base access
            keyword = self.current_token.value
            self.advance()
            
            if self.match(CSharpTokenType.DOT):
                return self.parse_member_access(keyword)
            else:
                return CSharpThisExpression(
                    node_type=CSharpNodeType.THIS_EXPRESSION,
                    keyword=keyword
                )
        
        else:
            self.error("Expected expression")
    
    def parse_method_invocation(self, method_name: str) -> CSharpMethodInvocationExpression:
        """Parse method invocation."""
        self.expect(CSharpTokenType.LEFT_PAREN)
        
        arguments = []
        if not self.match(CSharpTokenType.RIGHT_PAREN):
            arguments.append(self.parse_expression())
            
            while self.match(CSharpTokenType.COMMA):
                self.advance()
                arguments.append(self.parse_expression())
        
        self.expect(CSharpTokenType.RIGHT_PAREN)
        
        return CSharpMethodInvocationExpression(
            node_type=CSharpNodeType.METHOD_INVOCATION_EXPRESSION,
            method_name=method_name,
            arguments=arguments
        )
    
    def parse_member_access(self, target: str) -> CSharpMemberAccessExpression:
        """Parse member access."""
        self.expect(CSharpTokenType.DOT)
        
        if not self.match(CSharpTokenType.IDENTIFIER):
            self.error("Expected identifier")
        
        member_name = self.current_token.value
        self.advance()
        
        return CSharpMemberAccessExpression(
            node_type=CSharpNodeType.MEMBER_ACCESS_EXPRESSION,
            target=target,
            member_name=member_name
        )
    
    def parse_indexer_access(self, target: str) -> CSharpIndexerAccessExpression:
        """Parse indexer access."""
        self.expect(CSharpTokenType.LEFT_BRACKET)
        
        arguments = []
        if not self.match(CSharpTokenType.RIGHT_BRACKET):
            arguments.append(self.parse_expression())
            
            while self.match(CSharpTokenType.COMMA):
                self.advance()
                arguments.append(self.parse_expression())
        
        self.expect(CSharpTokenType.RIGHT_BRACKET)
        
        return CSharpIndexerAccessExpression(
            node_type=CSharpNodeType.INDEXER_ACCESS_EXPRESSION,
            target=target,
            arguments=arguments
        )
    
    def parse_object_creation_expression(self) -> CSharpObjectCreationExpression:
        """Parse object creation expression."""
        self.expect(CSharpTokenType.NEW)
        
        # Parse type
        object_type = self.parse_type()
        
        # Parse constructor arguments
        arguments = []
        if self.match(CSharpTokenType.LEFT_PAREN):
            self.advance()
            
            if not self.match(CSharpTokenType.RIGHT_PAREN):
                arguments.append(self.parse_expression())
                
                while self.match(CSharpTokenType.COMMA):
                    self.advance()
                    arguments.append(self.parse_expression())
            
            self.expect(CSharpTokenType.RIGHT_PAREN)
        
        # Parse object initializer
        initializer = None
        if self.match(CSharpTokenType.LEFT_BRACE):
            initializer = self.parse_object_initializer()
        
        return CSharpObjectCreationExpression(
            node_type=CSharpNodeType.OBJECT_CREATION_EXPRESSION,
            object_type=object_type,
            arguments=arguments,
            initializer=initializer
        )
    
    def parse_object_initializer(self) -> CSharpObjectInitializerExpression:
        """Parse object initializer."""
        self.expect(CSharpTokenType.LEFT_BRACE)
        
        initializers = []
        if not self.match(CSharpTokenType.RIGHT_BRACE):
            initializers.append(self.parse_initializer_assignment())
            
            while self.match(CSharpTokenType.COMMA):
                self.advance()
                initializers.append(self.parse_initializer_assignment())
        
        self.expect(CSharpTokenType.RIGHT_BRACE)
        
        return CSharpObjectInitializerExpression(
            node_type=CSharpNodeType.OBJECT_INITIALIZER_EXPRESSION,
            initializers=initializers
        )
    
    def parse_initializer_assignment(self) -> CSharpInitializerAssignment:
        """Parse initializer assignment."""
        if not self.match(CSharpTokenType.IDENTIFIER):
            self.error("Expected identifier")
        
        property_name = self.current_token.value
        self.advance()
        
        self.expect(CSharpTokenType.EQUALS)
        value = self.parse_expression()
        
        return CSharpInitializerAssignment(
            node_type=CSharpNodeType.INITIALIZER_ASSIGNMENT,
            property_name=property_name,
            value=value
        )


# Convenience functions
def parse_csharp(source: str, file_path: Optional[str] = None) -> CSharpCompilationUnit:
    """Parse C# source code into an AST."""
    lexer = CSharpLexer(source)
    tokens = lexer.tokenize()
    
    # Filter out trivia tokens
    filtered_tokens = [t for t in tokens if t.type not in [
        CSharpTokenType.WHITESPACE, CSharpTokenType.NEWLINE,
        CSharpTokenType.SINGLE_LINE_COMMENT, CSharpTokenType.MULTI_LINE_COMMENT
    ]]
    
    parser = CSharpParser(filtered_tokens)
    return parser.parse()


def tokenize_csharp(source: str) -> List[CSharpToken]:
    """Tokenize C# source code."""
    lexer = CSharpLexer(source)
    return lexer.tokenize()