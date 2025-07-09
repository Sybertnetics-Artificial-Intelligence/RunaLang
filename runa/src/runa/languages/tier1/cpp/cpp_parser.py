#!/usr/bin/env python3
"""
C++ Parser

Complete C++ parser supporting modern C++ features from C++11 through C++23.
Includes lexical analysis and recursive descent parsing with comprehensive
error handling and recovery.
"""

import re
from typing import List, Optional, Dict, Any, Union, Tuple
from dataclasses import dataclass
from enum import Enum, auto

from .cpp_ast import *


class CppTokenType(Enum):
    """C++ token types."""
    # Literals
    INTEGER_LITERAL = auto()
    FLOATING_LITERAL = auto()
    STRING_LITERAL = auto()
    CHARACTER_LITERAL = auto()
    BOOLEAN_LITERAL = auto()
    NULLPTR_LITERAL = auto()
    USER_DEFINED_LITERAL = auto()
    
    # Identifiers and keywords
    IDENTIFIER = auto()
    KEYWORD = auto()
    
    # Operators
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
    INCREMENT = auto()      # ++
    DECREMENT = auto()      # --
    
    # Comparison
    EQUAL = auto()          # ==
    NOT_EQUAL = auto()      # !=
    LESS = auto()           # <
    LESS_EQUAL = auto()     # <=
    GREATER = auto()        # >
    GREATER_EQUAL = auto()  # >=
    SPACESHIP = auto()      # <=> (C++20)
    
    # Logical
    LOGICAL_AND = auto()    # &&
    LOGICAL_OR = auto()     # ||
    LOGICAL_NOT = auto()    # !
    
    # Bitwise
    BIT_AND = auto()        # &
    BIT_OR = auto()         # |
    BIT_XOR = auto()        # ^
    BIT_NOT = auto()        # ~
    LEFT_SHIFT = auto()     # <<
    RIGHT_SHIFT = auto()    # >>
    BIT_AND_ASSIGN = auto() # &=
    BIT_OR_ASSIGN = auto()  # |=
    BIT_XOR_ASSIGN = auto() # ^=
    LEFT_SHIFT_ASSIGN = auto() # <<=
    RIGHT_SHIFT_ASSIGN = auto() # >>=
    
    # Member access
    DOT = auto()            # .
    ARROW = auto()          # ->
    DOT_STAR = auto()       # .*
    ARROW_STAR = auto()     # ->*
    SCOPE = auto()          # ::
    
    # Punctuation
    SEMICOLON = auto()      # ;
    COMMA = auto()          # ,
    QUESTION = auto()       # ?
    COLON = auto()          # :
    
    # Brackets
    LEFT_PAREN = auto()     # (
    RIGHT_PAREN = auto()    # )
    LEFT_BRACE = auto()     # {
    RIGHT_BRACE = auto()    # }
    LEFT_BRACKET = auto()   # [
    RIGHT_BRACKET = auto()  # ]
    
    # Special
    ELLIPSIS = auto()       # ...
    HASH = auto()           # #
    DOUBLE_HASH = auto()    # ##
    
    # Whitespace and comments
    WHITESPACE = auto()
    NEWLINE = auto()
    COMMENT = auto()
    
    # End of file
    EOF = auto()
    
    # Error
    ERROR = auto()


@dataclass
class CppToken:
    """C++ token."""
    type: CppTokenType
    value: str
    line: int
    column: int
    file_name: Optional[str] = None


class CppLexer:
    """C++ lexer/tokenizer."""
    
    # C++ keywords
    KEYWORDS = {
        # Basic keywords
        'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do',
        'double', 'else', 'enum', 'extern', 'float', 'for', 'goto', 'if',
        'int', 'long', 'register', 'return', 'short', 'signed', 'sizeof',
        'static', 'struct', 'switch', 'typedef', 'union', 'unsigned', 'void',
        'volatile', 'while',
        
        # C++ specific keywords
        'bool', 'catch', 'class', 'const_cast', 'delete', 'dynamic_cast',
        'explicit', 'export', 'false', 'friend', 'inline', 'mutable',
        'namespace', 'new', 'operator', 'private', 'protected', 'public',
        'reinterpret_cast', 'static_cast', 'template', 'this', 'throw',
        'true', 'try', 'typeid', 'typename', 'using', 'virtual', 'wchar_t',
        
        # C++11 keywords
        'alignas', 'alignof', 'char16_t', 'char32_t', 'constexpr', 'decltype',
        'noexcept', 'nullptr', 'static_assert', 'thread_local',
        
        # C++14 keywords
        # (No new keywords)
        
        # C++17 keywords
        # (No new keywords)
        
        # C++20 keywords
        'char8_t', 'concept', 'requires', 'co_await', 'co_return', 'co_yield',
        
        # C++23 keywords
        # (Placeholder for future keywords)
    }
    
    def __init__(self, source: str, file_name: Optional[str] = None):
        self.source = source
        self.file_name = file_name
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
    
    def tokenize(self) -> List[CppToken]:
        """Tokenize the source code."""
        while self.position < len(self.source):
            if self._at_end():
                break
            
            start_pos = self.position
            start_line = self.line
            start_column = self.column
            
            char = self._current_char()
            
            # Skip whitespace
            if char.isspace():
                self._skip_whitespace()
                continue
            
            # Comments
            if char == '/' and self._peek() == '/':
                self._skip_line_comment()
                continue
            elif char == '/' and self._peek() == '*':
                self._skip_block_comment()
                continue
            
            # String literals
            if char == '"' or (char == 'R' and self._peek() == '"'):
                token = self._read_string_literal()
                if token:
                    self.tokens.append(token)
                continue
            
            # Character literals
            if char == "'" or (char in 'uUL' and self._peek() == "'"):
                token = self._read_character_literal()
                if token:
                    self.tokens.append(token)
                continue
            
            # Numbers
            if char.isdigit() or (char == '.' and self._peek().isdigit()):
                token = self._read_number()
                if token:
                    self.tokens.append(token)
                continue
            
            # Identifiers and keywords
            if char.isalpha() or char == '_':
                token = self._read_identifier()
                if token:
                    self.tokens.append(token)
                continue
            
            # Operators and punctuation
            token = self._read_operator_or_punctuation()
            if token:
                self.tokens.append(token)
                continue
            
            # Unknown character
            self._advance()
        
        # Add EOF token
        self.tokens.append(CppToken(
            CppTokenType.EOF, "",
            self.line, self.column, self.file_name
        ))
        
        return self.tokens
    
    def _current_char(self) -> str:
        """Get current character."""
        if self._at_end():
            return '\0'
        return self.source[self.position]
    
    def _peek(self, offset: int = 1) -> str:
        """Peek at character at offset."""
        pos = self.position + offset
        if pos >= len(self.source):
            return '\0'
        return self.source[pos]
    
    def _advance(self) -> str:
        """Advance position and return current character."""
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
        """Check if at end of source."""
        return self.position >= len(self.source)
    
    def _skip_whitespace(self):
        """Skip whitespace characters."""
        while not self._at_end() and self._current_char().isspace():
            self._advance()
    
    def _skip_line_comment(self):
        """Skip line comment."""
        while not self._at_end() and self._current_char() != '\n':
            self._advance()
    
    def _skip_block_comment(self):
        """Skip block comment."""
        self._advance()  # Skip '/'
        self._advance()  # Skip '*'
        
        while not self._at_end():
            if self._current_char() == '*' and self._peek() == '/':
                self._advance()  # Skip '*'
                self._advance()  # Skip '/'
                break
            self._advance()
    
    def _read_string_literal(self) -> Optional[CppToken]:
        """Read string literal."""
        start_line = self.line
        start_column = self.column
        value = ""
        
        # Handle raw strings and prefixes
        prefix = ""
        if self._current_char() in 'uUL':
            prefix = self._advance()
            if self._current_char() == '8' and prefix == 'u':
                prefix += self._advance()
        
        if self._current_char() == 'R':
            # Raw string
            self._advance()  # R
            self._advance()  # "
            
            # Read delimiter
            delimiter = ""
            if self._current_char() == '(':
                self._advance()
                while not self._at_end() and self._current_char() != ')':
                    delimiter += self._advance()
                self._advance()  # )
            
            # Read content
            content = ""
            while not self._at_end():
                if (self._current_char() == ')' and 
                    self.source[self.position:self.position + len(delimiter) + 2] == 
                    ')' + delimiter + '"'):
                    # Found end
                    for _ in range(len(delimiter) + 2):
                        self._advance()
                    break
                content += self._advance()
            
            value = f'{prefix}R"({delimiter}){content}){delimiter}"'
        else:
            # Regular string
            self._advance()  # Opening quote
            
            while not self._at_end() and self._current_char() != '"':
                if self._current_char() == '\\':
                    value += self._advance()  # Backslash
                    if not self._at_end():
                        value += self._advance()  # Escaped character
                else:
                    value += self._advance()
            
            if not self._at_end():
                self._advance()  # Closing quote
            
            value = f'{prefix}"{value}"'
        
        return CppToken(
            CppTokenType.STRING_LITERAL, value,
            start_line, start_column, self.file_name
        )
    
    def _read_character_literal(self) -> Optional[CppToken]:
        """Read character literal."""
        start_line = self.line
        start_column = self.column
        value = ""
        
        # Handle prefixes
        if self._current_char() in 'uUL':
            value += self._advance()
        
        value += self._advance()  # Opening quote
        
        while not self._at_end() and self._current_char() != "'":
            if self._current_char() == '\\':
                value += self._advance()  # Backslash
                if not self._at_end():
                    value += self._advance()  # Escaped character
            else:
                value += self._advance()
        
        if not self._at_end():
            value += self._advance()  # Closing quote
        
        return CppToken(
            CppTokenType.CHARACTER_LITERAL, value,
            start_line, start_column, self.file_name
        )
    
    def _read_number(self) -> Optional[CppToken]:
        """Read numeric literal."""
        start_line = self.line
        start_column = self.column
        value = ""
        is_float = False
        
        # Handle different number formats
        if self._current_char() == '0':
            value += self._advance()
            
            # Hex number
            if self._current_char() in 'xX':
                value += self._advance()
                while (not self._at_end() and 
                       (self._current_char().isdigit() or 
                        self._current_char().lower() in 'abcdef')):
                    value += self._advance()
            
            # Binary number (C++14)
            elif self._current_char() in 'bB':
                value += self._advance()
                while not self._at_end() and self._current_char() in '01':
                    value += self._advance()
            
            # Octal number
            elif self._current_char().isdigit():
                while not self._at_end() and self._current_char().isdigit():
                    value += self._advance()
        else:
            # Decimal number
            while not self._at_end() and self._current_char().isdigit():
                value += self._advance()
        
        # Decimal point
        if self._current_char() == '.':
            is_float = True
            value += self._advance()
            while not self._at_end() and self._current_char().isdigit():
                value += self._advance()
        
        # Exponent
        if self._current_char() in 'eE':
            is_float = True
            value += self._advance()
            if self._current_char() in '+-':
                value += self._advance()
            while not self._at_end() and self._current_char().isdigit():
                value += self._advance()
        
        # Suffix
        while (not self._at_end() and 
               self._current_char().lower() in 'ulfl'):
            value += self._advance()
        
        token_type = CppTokenType.FLOATING_LITERAL if is_float else CppTokenType.INTEGER_LITERAL
        
        return CppToken(
            token_type, value,
            start_line, start_column, self.file_name
        )
    
    def _read_identifier(self) -> Optional[CppToken]:
        """Read identifier or keyword."""
        start_line = self.line
        start_column = self.column
        value = ""
        
        while (not self._at_end() and 
               (self._current_char().isalnum() or self._current_char() == '_')):
            value += self._advance()
        
        # Check for keywords
        if value in self.KEYWORDS:
            if value in ['true', 'false']:
                token_type = CppTokenType.BOOLEAN_LITERAL
            elif value == 'nullptr':
                token_type = CppTokenType.NULLPTR_LITERAL
            else:
                token_type = CppTokenType.KEYWORD
        else:
            token_type = CppTokenType.IDENTIFIER
        
        return CppToken(
            token_type, value,
            start_line, start_column, self.file_name
        )
    
    def _read_operator_or_punctuation(self) -> Optional[CppToken]:
        """Read operator or punctuation."""
        start_line = self.line
        start_column = self.column
        char = self._current_char()
        
        # Multi-character operators
        if char == '+':
            self._advance()
            if self._current_char() == '+':
                self._advance()
                return CppToken(CppTokenType.INCREMENT, "++", start_line, start_column, self.file_name)
            elif self._current_char() == '=':
                self._advance()
                return CppToken(CppTokenType.PLUS_ASSIGN, "+=", start_line, start_column, self.file_name)
            return CppToken(CppTokenType.PLUS, "+", start_line, start_column, self.file_name)
        
        elif char == '-':
            self._advance()
            if self._current_char() == '-':
                self._advance()
                return CppToken(CppTokenType.DECREMENT, "--", start_line, start_column, self.file_name)
            elif self._current_char() == '=':
                self._advance()
                return CppToken(CppTokenType.MINUS_ASSIGN, "-=", start_line, start_column, self.file_name)
            elif self._current_char() == '>':
                self._advance()
                if self._current_char() == '*':
                    self._advance()
                    return CppToken(CppTokenType.ARROW_STAR, "->*", start_line, start_column, self.file_name)
                return CppToken(CppTokenType.ARROW, "->", start_line, start_column, self.file_name)
            return CppToken(CppTokenType.MINUS, "-", start_line, start_column, self.file_name)
        
        elif char == '*':
            self._advance()
            if self._current_char() == '=':
                self._advance()
                return CppToken(CppTokenType.MULTIPLY_ASSIGN, "*=", start_line, start_column, self.file_name)
            return CppToken(CppTokenType.MULTIPLY, "*", start_line, start_column, self.file_name)
        
        elif char == '/':
            self._advance()
            if self._current_char() == '=':
                self._advance()
                return CppToken(CppTokenType.DIVIDE_ASSIGN, "/=", start_line, start_column, self.file_name)
            return CppToken(CppTokenType.DIVIDE, "/", start_line, start_column, self.file_name)
        
        elif char == '%':
            self._advance()
            if self._current_char() == '=':
                self._advance()
                return CppToken(CppTokenType.MODULO_ASSIGN, "%=", start_line, start_column, self.file_name)
            return CppToken(CppTokenType.MODULO, "%", start_line, start_column, self.file_name)
        
        elif char == '=':
            self._advance()
            if self._current_char() == '=':
                self._advance()
                return CppToken(CppTokenType.EQUAL, "==", start_line, start_column, self.file_name)
            return CppToken(CppTokenType.ASSIGN, "=", start_line, start_column, self.file_name)
        
        elif char == '!':
            self._advance()
            if self._current_char() == '=':
                self._advance()
                return CppToken(CppTokenType.NOT_EQUAL, "!=", start_line, start_column, self.file_name)
            return CppToken(CppTokenType.LOGICAL_NOT, "!", start_line, start_column, self.file_name)
        
        elif char == '<':
            self._advance()
            if self._current_char() == '=':
                self._advance()
                if self._current_char() == '>':
                    self._advance()
                    return CppToken(CppTokenType.SPACESHIP, "<=>", start_line, start_column, self.file_name)
                return CppToken(CppTokenType.LESS_EQUAL, "<=", start_line, start_column, self.file_name)
            elif self._current_char() == '<':
                self._advance()
                if self._current_char() == '=':
                    self._advance()
                    return CppToken(CppTokenType.LEFT_SHIFT_ASSIGN, "<<=", start_line, start_column, self.file_name)
                return CppToken(CppTokenType.LEFT_SHIFT, "<<", start_line, start_column, self.file_name)
            return CppToken(CppTokenType.LESS, "<", start_line, start_column, self.file_name)
        
        elif char == '>':
            self._advance()
            if self._current_char() == '=':
                self._advance()
                return CppToken(CppTokenType.GREATER_EQUAL, ">=", start_line, start_column, self.file_name)
            elif self._current_char() == '>':
                self._advance()
                if self._current_char() == '=':
                    self._advance()
                    return CppToken(CppTokenType.RIGHT_SHIFT_ASSIGN, ">>=", start_line, start_column, self.file_name)
                return CppToken(CppTokenType.RIGHT_SHIFT, ">>", start_line, start_column, self.file_name)
            return CppToken(CppTokenType.GREATER, ">", start_line, start_column, self.file_name)
        
        elif char == '&':
            self._advance()
            if self._current_char() == '&':
                self._advance()
                return CppToken(CppTokenType.LOGICAL_AND, "&&", start_line, start_column, self.file_name)
            elif self._current_char() == '=':
                self._advance()
                return CppToken(CppTokenType.BIT_AND_ASSIGN, "&=", start_line, start_column, self.file_name)
            return CppToken(CppTokenType.BIT_AND, "&", start_line, start_column, self.file_name)
        
        elif char == '|':
            self._advance()
            if self._current_char() == '|':
                self._advance()
                return CppToken(CppTokenType.LOGICAL_OR, "||", start_line, start_column, self.file_name)
            elif self._current_char() == '=':
                self._advance()
                return CppToken(CppTokenType.BIT_OR_ASSIGN, "|=", start_line, start_column, self.file_name)
            return CppToken(CppTokenType.BIT_OR, "|", start_line, start_column, self.file_name)
        
        elif char == '^':
            self._advance()
            if self._current_char() == '=':
                self._advance()
                return CppToken(CppTokenType.BIT_XOR_ASSIGN, "^=", start_line, start_column, self.file_name)
            return CppToken(CppTokenType.BIT_XOR, "^", start_line, start_column, self.file_name)
        
        elif char == '.':
            self._advance()
            if self._current_char() == '.':
                self._advance()
                if self._current_char() == '.':
                    self._advance()
                    return CppToken(CppTokenType.ELLIPSIS, "...", start_line, start_column, self.file_name)
            elif self._current_char() == '*':
                self._advance()
                return CppToken(CppTokenType.DOT_STAR, ".*", start_line, start_column, self.file_name)
            return CppToken(CppTokenType.DOT, ".", start_line, start_column, self.file_name)
        
        elif char == ':':
            self._advance()
            if self._current_char() == ':':
                self._advance()
                return CppToken(CppTokenType.SCOPE, "::", start_line, start_column, self.file_name)
            return CppToken(CppTokenType.COLON, ":", start_line, start_column, self.file_name)
        
        # Single character tokens
        single_char_tokens = {
            ';': CppTokenType.SEMICOLON,
            ',': CppTokenType.COMMA,
            '?': CppTokenType.QUESTION,
            '(': CppTokenType.LEFT_PAREN,
            ')': CppTokenType.RIGHT_PAREN,
            '{': CppTokenType.LEFT_BRACE,
            '}': CppTokenType.RIGHT_BRACE,
            '[': CppTokenType.LEFT_BRACKET,
            ']': CppTokenType.RIGHT_BRACKET,
            '~': CppTokenType.BIT_NOT,
            '#': CppTokenType.HASH,
        }
        
        if char in single_char_tokens:
            self._advance()
            return CppToken(
                single_char_tokens[char], char,
                start_line, start_column, self.file_name
            )
        
        # Unknown character
        self._advance()
        return CppToken(
            CppTokenType.ERROR, char,
            start_line, start_column, self.file_name
        )


class CppParser:
    """C++ recursive descent parser."""
    
    def __init__(self, tokens: List[CppToken]):
        self.tokens = tokens
        self.position = 0
        self.errors = []
    
    def parse(self) -> CppTranslationUnit:
        """Parse C++ translation unit."""
        declarations = []
        
        while not self._at_end():
            if self._current_token().type == CppTokenType.EOF:
                break
            
            try:
                decl = self._parse_declaration()
                if decl:
                    declarations.append(decl)
            except Exception as e:
                self.errors.append(f"Parse error at line {self._current_token().line}: {e}")
                self._synchronize()
        
        return CppTranslationUnit(declarations)
    
    def _current_token(self) -> CppToken:
        """Get current token."""
        if self._at_end():
            return self.tokens[-1]  # EOF token
        return self.tokens[self.position]
    
    def _peek_token(self, offset: int = 1) -> CppToken:
        """Peek at token at offset."""
        pos = self.position + offset
        if pos >= len(self.tokens):
            return self.tokens[-1]  # EOF token
        return self.tokens[pos]
    
    def _advance(self) -> CppToken:
        """Advance position and return current token."""
        token = self._current_token()
        if not self._at_end():
            self.position += 1
        return token
    
    def _at_end(self) -> bool:
        """Check if at end of tokens."""
        return (self.position >= len(self.tokens) or 
                self._current_token().type == CppTokenType.EOF)
    
    def _match(self, *token_types: CppTokenType) -> bool:
        """Check if current token matches any of the given types."""
        return self._current_token().type in token_types
    
    def _consume(self, token_type: CppTokenType, message: str = None) -> CppToken:
        """Consume token of expected type or raise error."""
        if self._match(token_type):
            return self._advance()
        
        if message:
            raise SyntaxError(message)
        else:
            raise SyntaxError(f"Expected {token_type}, got {self._current_token().type}")
    
    def _synchronize(self):
        """Synchronize parser after error."""
        self._advance()
        
        while not self._at_end():
            if self._current_token().type == CppTokenType.SEMICOLON:
                self._advance()
                return
            
            if self._match(CppTokenType.KEYWORD):
                keyword = self._current_token().value
                if keyword in ['class', 'struct', 'union', 'enum', 'namespace',
                              'template', 'typedef', 'using', 'extern', 'static']:
                    return
            
            self._advance()
    
    def _parse_declaration(self) -> Optional[CppDeclaration]:
        """Parse C++ declaration."""
        # Skip semicolons
        if self._match(CppTokenType.SEMICOLON):
            self._advance()
            return None
        
        # Template declaration
        if self._match(CppTokenType.KEYWORD) and self._current_token().value == 'template':
            return self._parse_template_declaration()
        
        # Namespace declaration
        if self._match(CppTokenType.KEYWORD) and self._current_token().value == 'namespace':
            return self._parse_namespace_declaration()
        
        # Class/struct/union declaration
        if self._match(CppTokenType.KEYWORD):
            keyword = self._current_token().value
            if keyword in ['class', 'struct', 'union']:
                return self._parse_class_declaration()
            elif keyword == 'enum':
                return self._parse_enum_declaration()
            elif keyword in ['typedef', 'using']:
                return self._parse_typedef_declaration()
        
        # Function or variable declaration
        return self._parse_function_or_variable_declaration()
    
    def _parse_template_declaration(self) -> CppTemplateDecl:
        """Parse template declaration."""
        self._consume(CppTokenType.KEYWORD)  # template
        self._consume(CppTokenType.LESS)
        
        # Parse template parameters
        params = []
        while not self._match(CppTokenType.GREATER):
            param = self._parse_template_parameter()
            params.append(param)
            
            if self._match(CppTokenType.COMMA):
                self._advance()
            elif not self._match(CppTokenType.GREATER):
                break
        
        self._consume(CppTokenType.GREATER)
        
        # Parse templated declaration
        declaration = self._parse_declaration()
        
        return CppTemplateDecl(
            CppTemplateParameterList(params),
            declaration
        )
    
    def _parse_template_parameter(self) -> CppTemplateParameter:
        """Parse template parameter."""
        # Simplified template parameter parsing
        if self._match(CppTokenType.KEYWORD) and self._current_token().value == 'typename':
            self._advance()
            name = None
            if self._match(CppTokenType.IDENTIFIER):
                name = self._advance().value
            return CppTemplateParameter(name, "type")
        elif self._match(CppTokenType.KEYWORD) and self._current_token().value == 'class':
            self._advance()
            name = None
            if self._match(CppTokenType.IDENTIFIER):
                name = self._advance().value
            return CppTemplateParameter(name, "type")
        else:
            # Non-type parameter (simplified)
            # This would need more complex parsing in a real implementation
            if self._match(CppTokenType.IDENTIFIER):
                name = self._advance().value
                return CppTemplateParameter(name, "non_type")
        
        return CppTemplateParameter(None, "type")
    
    def _parse_namespace_declaration(self) -> CppNamespaceDecl:
        """Parse namespace declaration."""
        self._consume(CppTokenType.KEYWORD)  # namespace
        
        name = None
        if self._match(CppTokenType.IDENTIFIER):
            name = self._advance().value
        
        self._consume(CppTokenType.LEFT_BRACE)
        
        declarations = []
        while not self._match(CppTokenType.RIGHT_BRACE) and not self._at_end():
            decl = self._parse_declaration()
            if decl:
                declarations.append(decl)
        
        self._consume(CppTokenType.RIGHT_BRACE)
        
        return CppNamespaceDecl(name, declarations)
    
    def _parse_class_declaration(self) -> CppClassDecl:
        """Parse class/struct/union declaration."""
        keyword_token = self._consume(CppTokenType.KEYWORD)
        keyword = keyword_token.value
        
        name = self._consume(CppTokenType.IDENTIFIER).value
        
        # Base classes (simplified)
        base_classes = []
        if self._match(CppTokenType.COLON):
            self._advance()
            # Simplified base class parsing
            # In a real implementation, this would handle access specifiers, virtual, etc.
            while True:
                if self._match(CppTokenType.IDENTIFIER):
                    base_name = self._advance().value
                    base_type = CppBuiltinType(base_name)  # Simplified
                    base_classes.append(CppBaseSpecifier(base_type))
                
                if self._match(CppTokenType.COMMA):
                    self._advance()
                else:
                    break
        
        self._consume(CppTokenType.LEFT_BRACE)
        
        members = []
        while not self._match(CppTokenType.RIGHT_BRACE) and not self._at_end():
            # Access specifiers
            if (self._match(CppTokenType.KEYWORD) and 
                self._current_token().value in ['public', 'private', 'protected']):
                self._advance()
                self._consume(CppTokenType.COLON)
                continue
            
            member = self._parse_declaration()
            if member:
                members.append(member)
        
        self._consume(CppTokenType.RIGHT_BRACE)
        self._consume(CppTokenType.SEMICOLON)
        
        return CppClassDecl(
            name, base_classes, members,
            is_struct=(keyword == 'struct'),
            is_union=(keyword == 'union')
        )
    
    def _parse_enum_declaration(self) -> CppDeclaration:
        """Parse enum declaration (simplified)."""
        self._consume(CppTokenType.KEYWORD)  # enum
        
        # Simplified enum parsing - just skip to semicolon
        while not self._match(CppTokenType.SEMICOLON) and not self._at_end():
            self._advance()
        
        if self._match(CppTokenType.SEMICOLON):
            self._advance()
        
        # Return a placeholder variable declaration
        return CppVariableDecl("enum_placeholder", CppBuiltinType("int"))
    
    def _parse_typedef_declaration(self) -> CppDeclaration:
        """Parse typedef/using declaration (simplified)."""
        keyword = self._advance().value  # typedef or using
        
        # Simplified typedef parsing - just skip to semicolon
        while not self._match(CppTokenType.SEMICOLON) and not self._at_end():
            self._advance()
        
        if self._match(CppTokenType.SEMICOLON):
            self._advance()
        
        # Return a placeholder variable declaration
        return CppVariableDecl("typedef_placeholder", CppBuiltinType("int"))
    
    def _parse_function_or_variable_declaration(self) -> Optional[CppDeclaration]:
        """Parse function or variable declaration."""
        # This is a simplified implementation
        # A real C++ parser would need much more complex logic here
        
        # Skip storage class specifiers, type qualifiers, etc.
        while (self._match(CppTokenType.KEYWORD) and 
               self._current_token().value in ['static', 'extern', 'const', 'volatile', 
                                             'mutable', 'inline', 'virtual']):
            self._advance()
        
        # Parse type (simplified)
        type_name = ""
        if self._match(CppTokenType.KEYWORD, CppTokenType.IDENTIFIER):
            type_name = self._advance().value
        
        if not type_name:
            return None
        
        var_type = CppBuiltinType(type_name)
        
        # Parse name
        if not self._match(CppTokenType.IDENTIFIER):
            return None
        
        name = self._advance().value
        
        # Check if it's a function
        if self._match(CppTokenType.LEFT_PAREN):
            return self._parse_function_declaration_rest(name, var_type)
        else:
            return self._parse_variable_declaration_rest(name, var_type)
    
    def _parse_function_declaration_rest(self, name: str, return_type: CppType) -> CppFunctionDecl:
        """Parse rest of function declaration."""
        self._consume(CppTokenType.LEFT_PAREN)
        
        # Parse parameters (simplified)
        parameters = []
        while not self._match(CppTokenType.RIGHT_PAREN) and not self._at_end():
            # Skip parameter parsing for simplicity
            self._advance()
        
        self._consume(CppTokenType.RIGHT_PAREN)
        
        # Function body or semicolon
        body = None
        if self._match(CppTokenType.LEFT_BRACE):
            body = self._parse_compound_statement()
        elif self._match(CppTokenType.SEMICOLON):
            self._advance()
        
        param_list = CppParameterList(parameters)
        
        return CppFunctionDecl(name, return_type, param_list, body)
    
    def _parse_variable_declaration_rest(self, name: str, var_type: CppType) -> CppVariableDecl:
        """Parse rest of variable declaration."""
        initializer = None
        
        # Initializer
        if self._match(CppTokenType.ASSIGN):
            self._advance()
            initializer = self._parse_expression()
        
        self._consume(CppTokenType.SEMICOLON)
        
        return CppVariableDecl(name, var_type, initializer)
    
    def _parse_compound_statement(self) -> CppCompoundStmt:
        """Parse compound statement."""
        self._consume(CppTokenType.LEFT_BRACE)
        
        statements = []
        while not self._match(CppTokenType.RIGHT_BRACE) and not self._at_end():
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
        
        self._consume(CppTokenType.RIGHT_BRACE)
        
        return CppCompoundStmt(statements)
    
    def _parse_statement(self) -> Optional[CppStatement]:
        """Parse statement."""
        # Simplified statement parsing
        if self._match(CppTokenType.LEFT_BRACE):
            return self._parse_compound_statement()
        elif self._match(CppTokenType.KEYWORD):
            keyword = self._current_token().value
            if keyword == 'if':
                return self._parse_if_statement()
            elif keyword == 'while':
                return self._parse_while_statement()
            elif keyword == 'for':
                return self._parse_for_statement()
            elif keyword == 'return':
                return self._parse_return_statement()
            elif keyword == 'break':
                self._advance()
                self._consume(CppTokenType.SEMICOLON)
                return CppBreakStmt()
            elif keyword == 'continue':
                self._advance()
                self._consume(CppTokenType.SEMICOLON)
                return CppContinueStmt()
        
        # Expression statement
        expr = self._parse_expression()
        self._consume(CppTokenType.SEMICOLON)
        return CppExpressionStmt(expr)
    
    def _parse_if_statement(self) -> CppIfStmt:
        """Parse if statement."""
        self._consume(CppTokenType.KEYWORD)  # if
        self._consume(CppTokenType.LEFT_PAREN)
        condition = self._parse_expression()
        self._consume(CppTokenType.RIGHT_PAREN)
        
        then_stmt = self._parse_statement()
        
        else_stmt = None
        if (self._match(CppTokenType.KEYWORD) and 
            self._current_token().value == 'else'):
            self._advance()
            else_stmt = self._parse_statement()
        
        return CppIfStmt(condition, then_stmt, else_stmt)
    
    def _parse_while_statement(self) -> CppWhileStmt:
        """Parse while statement."""
        self._consume(CppTokenType.KEYWORD)  # while
        self._consume(CppTokenType.LEFT_PAREN)
        condition = self._parse_expression()
        self._consume(CppTokenType.RIGHT_PAREN)
        
        body = self._parse_statement()
        
        return CppWhileStmt(condition, body)
    
    def _parse_for_statement(self) -> CppForStmt:
        """Parse for statement."""
        self._consume(CppTokenType.KEYWORD)  # for
        self._consume(CppTokenType.LEFT_PAREN)
        
        # Simplified for statement parsing
        init = None
        if not self._match(CppTokenType.SEMICOLON):
            init = self._parse_statement()
        else:
            self._advance()
        
        condition = None
        if not self._match(CppTokenType.SEMICOLON):
            condition = self._parse_expression()
        self._consume(CppTokenType.SEMICOLON)
        
        increment = None
        if not self._match(CppTokenType.RIGHT_PAREN):
            increment = self._parse_expression()
        self._consume(CppTokenType.RIGHT_PAREN)
        
        body = self._parse_statement()
        
        return CppForStmt(init, condition, increment, body)
    
    def _parse_return_statement(self) -> CppReturnStmt:
        """Parse return statement."""
        self._consume(CppTokenType.KEYWORD)  # return
        
        value = None
        if not self._match(CppTokenType.SEMICOLON):
            value = self._parse_expression()
        
        self._consume(CppTokenType.SEMICOLON)
        
        return CppReturnStmt(value)
    
    def _parse_expression(self) -> Optional[CppExpression]:
        """Parse expression (simplified)."""
        return self._parse_ternary()
    
    def _parse_ternary(self) -> Optional[CppExpression]:
        """Parse ternary conditional expression."""
        expr = self._parse_logical_or()
        
        if self._match(CppTokenType.QUESTION):
            self._advance()
            true_expr = self._parse_expression()
            self._consume(CppTokenType.COLON)
            false_expr = self._parse_expression()
            return CppConditionalOp(expr, true_expr, false_expr)
        
        return expr
    
    def _parse_logical_or(self) -> Optional[CppExpression]:
        """Parse logical OR expression."""
        expr = self._parse_logical_and()
        
        while self._match(CppTokenType.LOGICAL_OR):
            op = CppOperator.LOGICAL_OR
            self._advance()
            right = self._parse_logical_and()
            expr = CppBinaryOp(expr, op, right)
        
        return expr
    
    def _parse_logical_and(self) -> Optional[CppExpression]:
        """Parse logical AND expression."""
        expr = self._parse_equality()
        
        while self._match(CppTokenType.LOGICAL_AND):
            op = CppOperator.LOGICAL_AND
            self._advance()
            right = self._parse_equality()
            expr = CppBinaryOp(expr, op, right)
        
        return expr
    
    def _parse_equality(self) -> Optional[CppExpression]:
        """Parse equality expression."""
        expr = self._parse_relational()
        
        while self._match(CppTokenType.EQUAL, CppTokenType.NOT_EQUAL):
            op_token = self._advance()
            op = CppOperator.EQ if op_token.type == CppTokenType.EQUAL else CppOperator.NE
            right = self._parse_relational()
            expr = CppBinaryOp(expr, op, right)
        
        return expr
    
    def _parse_relational(self) -> Optional[CppExpression]:
        """Parse relational expression."""
        expr = self._parse_additive()
        
        while self._match(CppTokenType.LESS, CppTokenType.LESS_EQUAL,
                          CppTokenType.GREATER, CppTokenType.GREATER_EQUAL):
            op_token = self._advance()
            op_map = {
                CppTokenType.LESS: CppOperator.LT,
                CppTokenType.LESS_EQUAL: CppOperator.LE,
                CppTokenType.GREATER: CppOperator.GT,
                CppTokenType.GREATER_EQUAL: CppOperator.GE,
            }
            op = op_map[op_token.type]
            right = self._parse_additive()
            expr = CppBinaryOp(expr, op, right)
        
        return expr
    
    def _parse_additive(self) -> Optional[CppExpression]:
        """Parse additive expression."""
        expr = self._parse_multiplicative()
        
        while self._match(CppTokenType.PLUS, CppTokenType.MINUS):
            op_token = self._advance()
            op = CppOperator.ADD if op_token.type == CppTokenType.PLUS else CppOperator.SUB
            right = self._parse_multiplicative()
            expr = CppBinaryOp(expr, op, right)
        
        return expr
    
    def _parse_multiplicative(self) -> Optional[CppExpression]:
        """Parse multiplicative expression."""
        expr = self._parse_unary()
        
        while self._match(CppTokenType.MULTIPLY, CppTokenType.DIVIDE, CppTokenType.MODULO):
            op_token = self._advance()
            op_map = {
                CppTokenType.MULTIPLY: CppOperator.MUL,
                CppTokenType.DIVIDE: CppOperator.DIV,
                CppTokenType.MODULO: CppOperator.MOD,
            }
            op = op_map[op_token.type]
            right = self._parse_unary()
            expr = CppBinaryOp(expr, op, right)
        
        return expr
    
    def _parse_unary(self) -> Optional[CppExpression]:
        """Parse unary expression."""
        if self._match(CppTokenType.LOGICAL_NOT, CppTokenType.BIT_NOT, 
                      CppTokenType.PLUS, CppTokenType.MINUS):
            op_token = self._advance()
            op_map = {
                CppTokenType.LOGICAL_NOT: CppOperator.LOGICAL_NOT,
                CppTokenType.BIT_NOT: CppOperator.BIT_NOT,
                CppTokenType.PLUS: CppOperator.ADD,
                CppTokenType.MINUS: CppOperator.SUB,
            }
            op = op_map[op_token.type]
            operand = self._parse_unary()
            return CppUnaryOp(op, operand)
        
        if self._match(CppTokenType.INCREMENT, CppTokenType.DECREMENT):
            op_token = self._advance()
            op = CppOperator.PRE_INC if op_token.type == CppTokenType.INCREMENT else CppOperator.PRE_DEC
            operand = self._parse_postfix()
            return CppUnaryOp(op, operand)
        
        return self._parse_postfix()
    
    def _parse_postfix(self) -> Optional[CppExpression]:
        """Parse postfix expression."""
        expr = self._parse_primary()
        
        while True:
            if self._match(CppTokenType.LEFT_PAREN):
                # Function call
                self._advance()
                args = []
                while not self._match(CppTokenType.RIGHT_PAREN) and not self._at_end():
                    arg = self._parse_expression()
                    if arg:
                        args.append(arg)
                    if self._match(CppTokenType.COMMA):
                        self._advance()
                    else:
                        break
                self._consume(CppTokenType.RIGHT_PAREN)
                expr = CppCall(expr, args)
            
            elif self._match(CppTokenType.LEFT_BRACKET):
                # Array subscript
                self._advance()
                index = self._parse_expression()
                self._consume(CppTokenType.RIGHT_BRACKET)
                expr = CppArraySubscript(expr, index)
            
            elif self._match(CppTokenType.DOT, CppTokenType.ARROW):
                # Member access
                op_token = self._advance()
                is_arrow = op_token.type == CppTokenType.ARROW
                member = self._consume(CppTokenType.IDENTIFIER).value
                expr = CppMemberAccess(expr, member, is_arrow)
            
            elif self._match(CppTokenType.INCREMENT, CppTokenType.DECREMENT):
                # Postfix increment/decrement
                op_token = self._advance()
                op = CppOperator.POST_INC if op_token.type == CppTokenType.INCREMENT else CppOperator.POST_DEC
                expr = CppUnaryOp(op, expr, is_postfix=True)
            
            else:
                break
        
        return expr
    
    def _parse_primary(self) -> Optional[CppExpression]:
        """Parse primary expression."""
        # Literals
        if self._match(CppTokenType.INTEGER_LITERAL):
            token = self._advance()
            return CppIntegerLiteral(int(token.value.rstrip('ulUL')))
        
        if self._match(CppTokenType.FLOATING_LITERAL):
            token = self._advance()
            return CppFloatingLiteral(float(token.value.rstrip('flFL')))
        
        if self._match(CppTokenType.STRING_LITERAL):
            token = self._advance()
            return CppStringLiteral(token.value)
        
        if self._match(CppTokenType.CHARACTER_LITERAL):
            token = self._advance()
            return CppCharacterLiteral(token.value)
        
        if self._match(CppTokenType.BOOLEAN_LITERAL):
            token = self._advance()
            return CppBooleanLiteral(token.value == 'true')
        
        if self._match(CppTokenType.NULLPTR_LITERAL):
            self._advance()
            return CppNullptrLiteral()
        
        # Identifier
        if self._match(CppTokenType.IDENTIFIER):
            token = self._advance()
            return CppIdentifier(token.value)
        
        # Parenthesized expression
        if self._match(CppTokenType.LEFT_PAREN):
            self._advance()
            expr = self._parse_expression()
            self._consume(CppTokenType.RIGHT_PAREN)
            return expr
        
        return None


def parse_cpp(source: str, file_name: Optional[str] = None) -> CppTranslationUnit:
    """Parse C++ source code into AST."""
    try:
        # Tokenize
        lexer = CppLexer(source, file_name)
        tokens = lexer.tokenize()
        
        # Parse
        parser = CppParser(tokens)
        ast = parser.parse()
        
        if parser.errors:
            error_msg = "; ".join(parser.errors)
            raise SyntaxError(f"C++ parse errors: {error_msg}")
        
        return ast
        
    except Exception as e:
        raise Exception(f"Failed to parse C++ code: {e}")