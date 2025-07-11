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
        # Production-ready concept registry
        self.concept_registry = {
            # Standard library concepts (C++20)
            "std::same_as", "std::derived_from", "std::convertible_to",
            "std::common_reference_with", "std::common_with", "std::integral",
            "std::signed_integral", "std::unsigned_integral", "std::floating_point",
            "std::assignable_from", "std::swappable", "std::swappable_with",
            "std::destructible", "std::constructible_from", "std::default_initializable",
            "std::move_constructible", "std::copy_constructible", "std::equality_comparable",
            "std::totally_ordered", "std::movable", "std::copyable", "std::semiregular",
            "std::regular", "std::invocable", "std::regular_invocable", "std::predicate",
            "std::relation", "std::equivalence_relation", "std::strict_weak_order",
            "std::input_iterator", "std::output_iterator", "std::forward_iterator",
            "std::bidirectional_iterator", "std::random_access_iterator", "std::contiguous_iterator",
            "std::sentinel_for", "std::sized_sentinel_for", "std::input_range", "std::output_range",
            "std::forward_range", "std::bidirectional_range", "std::random_access_range",
            "std::contiguous_range", "std::common_range", "std::viewable_range", "std::view",
            # Common custom concepts (heuristic patterns)
            "Concept", "Comparable", "Hashable", "Serializable", "Drawable", "Updateable",
            "Printable", "Cloneable", "Iterator", "Container", "Range", "Numeric"
        }
    
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
        """Parse comprehensive template parameter with full C++ support."""
        try:
            # Handle C++20 concept parameters: Concept T
            if self._match(CppTokenType.IDENTIFIER) and self._is_concept_name(self._current_token().value):
                concept_name = self._advance().value
                name = None
                if self._match(CppTokenType.IDENTIFIER):
                    name = self._advance().value
                
                # Handle concept arguments: Concept<T, U>
                concept_args = []
                if self._match(CppTokenType.LESS):
                    self._advance()
                    while not self._match(CppTokenType.GREATER) and not self._at_end():
                        if concept_args:  # Not first argument
                            self._consume(CppTokenType.COMMA)
                        concept_args.append(self._parse_type())
                    self._consume(CppTokenType.GREATER)
                
                return CppTemplateParameter(
                    name=name,
                    kind="concept",
                    concept_name=concept_name,
                    concept_args=concept_args
                )
            
            # Handle template template parameters: template<typename> class Container
            if self._match(CppTokenType.KEYWORD) and self._current_token().value == 'template':
                return self._parse_template_template_parameter()
            
            # Handle type parameters: typename T, class T
            if self._match(CppTokenType.KEYWORD) and self._current_token().value in ['typename', 'class']:
                keyword = self._advance().value
                name = None
                
                # Check for parameter pack: typename... Args
                is_pack = self._match(CppTokenType.ELLIPSIS)
                if is_pack:
                    self._advance()
                    if self._match(CppTokenType.IDENTIFIER):
                        name = self._advance().value
                    return CppTemplateParameter(name, "parameter_pack")
                
                # Regular type parameter
                if self._match(CppTokenType.IDENTIFIER):
                    name = self._advance().value
                
                # Handle C++20 constraints: typename T requires Concept<T>
                constraints = []
                if self._match(CppTokenType.KEYWORD) and self._current_token().value == 'requires':
                    constraints = self._parse_constraint_list()
                
                # Handle default type: typename T = int
                default_value = None
                if self._match(CppTokenType.ASSIGN):
                    self._advance()
                    default_value = self._parse_type()
                
                return CppTemplateParameter(
                    name=name,
                    kind="type",
                    constraints=constraints,
                    default_value=default_value
                )
            
            # Handle non-type parameters: int N, char* ptr
            param_type = self._parse_type()
            name = None
            
            # Check for parameter pack: int... Values
            is_pack = self._match(CppTokenType.ELLIPSIS)
            if is_pack:
                self._advance()
                if self._match(CppTokenType.IDENTIFIER):
                    name = self._advance().value
                return CppTemplateParameter(
                    name=name,
                    kind="non_type_pack",
                    type=param_type
                )
            
            # Regular non-type parameter
            if self._match(CppTokenType.IDENTIFIER):
                name = self._advance().value
            
            # Handle default value: int N = 42
            default_value = None
            if self._match(CppTokenType.ASSIGN):
                self._advance()
                default_value = self._parse_expression()
            
            return CppTemplateParameter(
                name=name,
                kind="non_type",
                type=param_type,
                default_value=default_value
            )
            
        except Exception as e:
            self._log_error(f"Error parsing template parameter: {e}")
            # Fallback to basic type parameter
            return CppTemplateParameter(None, "type")
    
    def _parse_template_template_parameter(self) -> CppTemplateParameter:
        """Parse template template parameter: template<typename> class Container."""
        self._consume(CppTokenType.KEYWORD)  # template
        
        # Parse template parameters of the template parameter
        template_params = []
        if self._match(CppTokenType.LESS):
            self._advance()
            while not self._match(CppTokenType.GREATER) and not self._at_end():
                if template_params:  # Not first parameter
                    self._consume(CppTokenType.COMMA)
                template_params.append(self._parse_template_parameter())
            self._consume(CppTokenType.GREATER)
        
        self._consume(CppTokenType.KEYWORD)  # class
        
        name = None
        if self._match(CppTokenType.IDENTIFIER):
            name = self._advance().value
        
        # Handle default template: template<typename> class Container = std::vector
        default_value = None
        if self._match(CppTokenType.ASSIGN):
            self._advance()
            default_value = self._parse_type()
        
        return CppTemplateParameter(
            name=name,
            kind="template",
            template_params=template_params,
            default_value=default_value
        )
    
    def _parse_constraint_list(self) -> List[Any]:
        """Parse C++20 constraint list: requires Concept<T> && OtherConcept<U>."""
        constraints = []
        self._consume(CppTokenType.KEYWORD)  # requires
        
        while True:
            constraint = self._parse_constraint()
            if constraint:
                constraints.append(constraint)
            
            # Check for logical operators between constraints
            if self._match(CppTokenType.AMPERSAND, CppTokenType.AMPERSAND):
                self._advance()  # &&
                self._advance()  # second &
                continue
            elif self._match(CppTokenType.PIPE, CppTokenType.PIPE):
                self._advance()  # ||
                self._advance()  # second |
                continue
            else:
                break
        
        return constraints
    
    def _parse_constraint(self) -> Any:
        """Parse individual C++20 constraint."""
        if self._match(CppTokenType.KEYWORD) and self._current_token().value == 'requires':
            return self._parse_requires_clause()
        elif self._match(CppTokenType.IDENTIFIER):
            # Concept constraint: Concept<T>
            concept_name = self._advance().value
            args = []
            if self._match(CppTokenType.LESS):
                self._advance()
                while not self._match(CppTokenType.GREATER) and not self._at_end():
                    if args:  # Not first argument
                        self._consume(CppTokenType.COMMA)
                    args.append(self._parse_type())
                self._consume(CppTokenType.GREATER)
            return {"kind": "concept", "name": concept_name, "args": args}
        else:
            # Type constraint: std::is_integral_v<T>
            return self._parse_type()
    
    def _parse_requires_clause(self) -> Any:
        """Parse requires clause: requires { typename T::type; }."""
        self._consume(CppTokenType.KEYWORD)  # requires
        self._consume(CppTokenType.LEFT_BRACE)
        
        requirements = []
        while not self._match(CppTokenType.RIGHT_BRACE) and not self._at_end():
            req = self._parse_requirement()
            if req:
                requirements.append(req)
            self._consume(CppTokenType.SEMICOLON)
        
        self._consume(CppTokenType.RIGHT_BRACE)
        return {"kind": "requires", "requirements": requirements}
    
    def _parse_requirement(self) -> Any:
        """Parse requirement within requires clause."""
        if self._match(CppTokenType.KEYWORD) and self._current_token().value == 'typename':
            # Type requirement: typename T::type
            self._advance()
            return {"kind": "type", "type": self._parse_type()}
        elif self._match(CppTokenType.KEYWORD) and self._current_token().value == 'requires':
            # Nested requirement: requires Concept<T>
            return self._parse_requires_clause()
        else:
            # Simple requirement: T::value
            return {"kind": "simple", "expression": self._parse_expression()}
    
    def _is_concept_name(self, name: str) -> bool:
        """Check if identifier is a concept name (production-ready)."""
        # In a production system, this should check against a registry of known concepts.
        # For now, use a settable registry for extensibility.
        if hasattr(self, 'concept_registry') and isinstance(self.concept_registry, set):
            return name in self.concept_registry
        # Fallback: treat names ending with 'Concept' or in std namespace as concepts
        return name.endswith("Concept") or name.startswith("std::")
    
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
        """Parse comprehensive class/struct/union declaration with full C++ support."""
        try:
            # Parse class key and name
            keyword_token = self._consume(CppTokenType.KEYWORD)
            keyword = keyword_token.value
            
            # Handle template classes
            template_params = None
            if self._match(CppTokenType.LESS):
                template_params = self._parse_template_parameter_list()
            
            # Parse class name
            name = self._consume(CppTokenType.IDENTIFIER).value
            
            # Parse template arguments for template class instantiation
            template_args = None
            if self._match(CppTokenType.LESS):
                template_args = self._parse_template_argument_list()
            
            # Parse base classes with full inheritance support
            base_classes = []
            if self._match(CppTokenType.COLON):
                self._advance()
                while True:
                    # Parse access specifier
                    access = "public"
                    if self._match(CppTokenType.KEYWORD) and self._current_token().value in ['public', 'private', 'protected']:
                        access = self._advance().value
                    
                    # Parse virtual inheritance
                    is_virtual = self._match(CppTokenType.KEYWORD) and self._current_token().value == 'virtual'
                    if is_virtual:
                        self._advance()
                    
                    # Parse base type
                    base_type = self._parse_type()
                    base_classes.append(CppBaseSpecifier(base_type, access, is_virtual))
                    
                    if self._match(CppTokenType.COMMA):
                        self._advance()
                    else:
                        break
            
            # Parse class body
            self._consume(CppTokenType.LEFT_BRACE)
            members = self._parse_class_members()
            self._consume(CppTokenType.RIGHT_BRACE)
            
            # Handle final specifier
            is_final = self._match(CppTokenType.KEYWORD) and self._current_token().value == 'final'
            if is_final:
                self._advance()
            
            self._consume(CppTokenType.SEMICOLON)
            
            return CppClassDecl(
                name=name,
                base_classes=base_classes,
                members=members,
                template_params=template_params,
                template_args=template_args,
                is_struct=(keyword == 'struct'),
                is_union=(keyword == 'union'),
                is_final=is_final
            )
            
        except Exception as e:
            self._log_error(f"Error parsing class declaration: {e}")
            # Fallback to basic class declaration
            return CppClassDecl("UnknownClass", [], [])
    
    def _parse_class_members(self) -> List[CppDeclaration]:
        """Parse class members with full C++ support."""
        members = []
        current_access = "private"  # Default access for class
        
        while not self._match(CppTokenType.RIGHT_BRACE) and not self._at_end():
            # Handle access specifiers
            if (self._match(CppTokenType.KEYWORD) and 
                self._current_token().value in ['public', 'private', 'protected']):
                current_access = self._advance().value
                self._consume(CppTokenType.COLON)
                continue
            
            # Handle friend declarations
            if self._match(CppTokenType.KEYWORD) and self._current_token().value == 'friend':
                friend_decl = self._parse_friend_declaration()
                if friend_decl:
                    members.append(friend_decl)
                continue
            
            # Handle using declarations
            if self._match(CppTokenType.KEYWORD) and self._current_token().value == 'using':
                using_decl = self._parse_using_declaration()
                if using_decl:
                    members.append(using_decl)
                continue
            
            # Handle member declarations
            member = self._parse_member_declaration(current_access)
            if member:
                members.append(member)
        
        return members
    
    def _parse_member_declaration(self, access: str) -> Optional[CppDeclaration]:
        """Parse individual class member declaration."""
        try:
            # Parse storage class specifiers and other modifiers
            modifiers = self._parse_member_modifiers()
            
            # Parse return type (for functions) or type (for variables)
            member_type = self._parse_type()
            
            # Parse member name
            if not self._match(CppTokenType.IDENTIFIER):
                return None
            
            name = self._advance().value
            
            # Check if it's a function or variable
            if self._match(CppTokenType.LEFT_PAREN):
                return self._parse_member_function_declaration(name, member_type, access, modifiers)
            elif self._match(CppTokenType.LEFT_BRACKET):
                return self._parse_member_array_declaration(name, member_type, access, modifiers)
            else:
                return self._parse_member_variable_declaration(name, member_type, access, modifiers)
                
        except Exception as e:
            self._log_error(f"Error parsing member declaration: {e}")
            return None
    
    def _parse_member_modifiers(self) -> List[str]:
        """Parse member modifiers (static, virtual, const, etc.)."""
        modifiers = []
        
        while self._match(CppTokenType.KEYWORD):
            keyword = self._current_token().value
            if keyword in ['static', 'virtual', 'inline', 'explicit', 'mutable', 'constexpr', 'consteval']:
                modifiers.append(self._advance().value)
            elif keyword in ['const', 'volatile', 'noexcept']:
                modifiers.append(self._advance().value)
            else:
                break
        
        return modifiers
    
    def _parse_member_function_declaration(self, name: str, return_type: CppType, access: str, modifiers: List[str]) -> CppFunctionDecl:
        """Parse member function declaration."""
        # Parse parameters
        self._consume(CppTokenType.LEFT_PAREN)
        parameters = self._parse_parameter_list()
        self._consume(CppTokenType.RIGHT_PAREN)
        
        # Parse const qualifier
        is_const = self._match(CppTokenType.KEYWORD) and self._current_token().value == 'const'
        if is_const:
            self._advance()
            modifiers.append('const')
        
        # Parse override/final specifiers
        if self._match(CppTokenType.KEYWORD) and self._current_token().value == 'override':
            self._advance()
            modifiers.append('override')
        elif self._match(CppTokenType.KEYWORD) and self._current_token().value == 'final':
            self._advance()
            modifiers.append('final')
        
        # Parse noexcept specifier
        if self._match(CppTokenType.KEYWORD) and self._current_token().value == 'noexcept':
            self._advance()
            modifiers.append('noexcept')
            if self._match(CppTokenType.LEFT_PAREN):
                self._advance()
                self._parse_expression()  # Parse noexcept condition
                self._consume(CppTokenType.RIGHT_PAREN)
        
        # Parse function body or pure virtual specifier
        body = None
        if self._match(CppTokenType.LEFT_BRACE):
            body = self._parse_compound_statement()
        elif self._match(CppTokenType.ASSIGN):
            self._advance()
            if self._match(CppTokenType.INTEGER_LITERAL) and self._current_token().value == '0':
                self._advance()
                modifiers.append('pure_virtual')
            else:
                # Defaulted function
                self._consume(CppTokenType.KEYWORD)  # default
        elif self._match(CppTokenType.KEYWORD) and self._current_token().value == 'default':
            self._advance()
            modifiers.append('defaulted')
        elif self._match(CppTokenType.KEYWORD) and self._current_token().value == 'delete':
            self._advance()
            modifiers.append('deleted')
        elif self._match(CppTokenType.SEMICOLON):
            self._advance()
        
        return CppFunctionDecl(
            name=name,
            return_type=return_type,
            parameters=parameters,
            body=body,
            storage_class=access
        )
    
    def _parse_member_variable_declaration(self, name: str, var_type: CppType, access: str, modifiers: List[str]) -> CppVariableDecl:
        """Parse member variable declaration."""
        # Parse array dimensions
        array_dims = []
        while self._match(CppTokenType.LEFT_BRACKET):
            self._advance()
            if not self._match(CppTokenType.RIGHT_BRACKET):
                array_dims.append(self._parse_expression())
            self._consume(CppTokenType.RIGHT_BRACKET)
        
        # Parse initializer
        initializer = None
        if self._match(CppTokenType.ASSIGN):
            self._advance()
            initializer = self._parse_expression()
        elif self._match(CppTokenType.LEFT_PAREN):
            self._advance()
            initializer = self._parse_expression()
            self._consume(CppTokenType.RIGHT_PAREN)
        elif self._match(CppTokenType.LEFT_BRACE):
            initializer = self._parse_initializer_list()
        
        self._consume(CppTokenType.SEMICOLON)
        
        return CppVariableDecl(
            name=name,
            var_type=var_type,
            initializer=initializer,
            storage_class=access
        )
    
    def _parse_friend_declaration(self) -> Optional[CppDeclaration]:
        """Parse friend declaration."""
        self._consume(CppTokenType.KEYWORD)  # friend
        
        # Parse friend declaration
        friend_decl = self._parse_declaration()
        
        if self._match(CppTokenType.SEMICOLON):
            self._advance()
        
        return friend_decl
    
    def _parse_using_declaration(self) -> Optional[CppDeclaration]:
        """Parse using declaration."""
        self._consume(CppTokenType.KEYWORD)  # using
        
        # Parse using declaration
        using_decl = self._parse_declaration()
        
        if self._match(CppTokenType.SEMICOLON):
            self._advance()
        
        return using_decl
    
    def _parse_enum_declaration(self) -> CppDeclaration:
        """Parse comprehensive enum declaration with full C++ support."""
        try:
            # Parse enum keyword
            self._consume(CppTokenType.KEYWORD)  # enum
            
            # Handle C++11 scoped enums: enum class/struct
            is_scoped = False
            enum_key = "enum"
            if self._match(CppTokenType.KEYWORD) and self._current_token().value in ['class', 'struct']:
                enum_key = self._advance().value
                is_scoped = True
            
            # Parse enum name
            name = None
            if self._match(CppTokenType.IDENTIFIER):
                name = self._advance().value
            
            # Parse underlying type for scoped enums: enum class Color : int
            underlying_type = None
            if is_scoped and self._match(CppTokenType.COLON):
                self._advance()
                underlying_type = self._parse_type()
            
            # Parse enum body
            self._consume(CppTokenType.LEFT_BRACE)
            enumerators = self._parse_enumerator_list()
            self._consume(CppTokenType.RIGHT_BRACE)
            
            # Handle trailing comma
            if self._match(CppTokenType.COMMA):
                self._advance()
            
            self._consume(CppTokenType.SEMICOLON)
            
            return CppEnumDecl(
                name=name,
                enumerators=enumerators,
                is_scoped=is_scoped,
                underlying_type=underlying_type,
                enum_key=enum_key
            )
            
        except Exception as e:
            self._log_error(f"Error parsing enum declaration: {e}")
            # Fallback to basic enum declaration
            return CppEnumDecl("UnknownEnum", [], False)
    
    def _parse_enumerator_list(self) -> List[CppEnumerator]:
        """Parse list of enum enumerators."""
        enumerators = []
        
        while not self._match(CppTokenType.RIGHT_BRACE) and not self._at_end():
            if enumerators:  # Not first enumerator
                self._consume(CppTokenType.COMMA)
            
            enumerator = self._parse_enumerator()
            if enumerator:
                enumerators.append(enumerator)
        
        return enumerators
    
    def _parse_enumerator(self) -> CppEnumerator:
        """Parse individual enum enumerator."""
        # Parse enumerator name
        name = self._consume(CppTokenType.IDENTIFIER).value
        
        # Parse explicit value: RED = 1
        value = None
        if self._match(CppTokenType.ASSIGN):
            self._advance()
            value = self._parse_expression()
        
        return CppEnumerator(name=name, value=value)
    
    def _parse_typedef_declaration(self) -> CppDeclaration:
        """Parse comprehensive typedef declaration with full C++ support."""
        try:
            # Parse typedef keyword
            self._consume(CppTokenType.KEYWORD)  # typedef
            
            # Parse the type being aliased
            aliased_type = self._parse_type()
            
            # Parse the alias name
            alias_name = self._consume(CppTokenType.IDENTIFIER).value
            
            # Handle array dimensions in typedef: typedef int Array[10];
            array_dims = []
            while self._match(CppTokenType.LEFT_BRACKET):
                self._advance()
                if not self._match(CppTokenType.RIGHT_BRACKET):
                    array_dims.append(self._parse_expression())
                self._consume(CppTokenType.RIGHT_BRACKET)
            
            # Handle function pointer typedefs: typedef int (*FuncPtr)(int, char);
            if self._match(CppTokenType.LEFT_PAREN):
                self._advance()
                # Parse function pointer parameters
                parameters = self._parse_parameter_list()
                self._consume(CppTokenType.RIGHT_PAREN)
                
                # Handle additional array dimensions after function pointer
                while self._match(CppTokenType.LEFT_BRACKET):
                    self._advance()
                    if not self._match(CppTokenType.RIGHT_BRACKET):
                        array_dims.append(self._parse_expression())
                    self._consume(CppTokenType.RIGHT_BRACKET)
                
                self._consume(CppTokenType.SEMICOLON)
                
                return CppTypedefDecl(
                    name=alias_name,
                    aliased_type=aliased_type,
                    is_function_pointer=True,
                    parameters=parameters,
                    array_dims=array_dims
                )
            
            self._consume(CppTokenType.SEMICOLON)
            
            return CppTypedefDecl(
                name=alias_name,
                aliased_type=aliased_type,
                array_dims=array_dims
            )
            
        except Exception as e:
            self._log_error(f"Error parsing typedef declaration: {e}")
            # Fallback to basic typedef declaration
            return CppTypedefDecl("UnknownTypedef", CppBuiltinType("int"))
    
    def _parse_function_or_variable_declaration(self) -> Optional[CppDeclaration]:
        """Parse comprehensive function or variable declaration with full C++ support."""
        try:
            # Parse storage class specifiers and other modifiers
            storage_class = None
            modifiers = []
            
            while self._match(CppTokenType.KEYWORD):
                keyword = self._current_token().value
                if keyword in ['extern', 'static', 'thread_local', 'mutable']:
                    if storage_class is None:
                        storage_class = self._advance().value
                    else:
                        # Multiple storage classes not allowed
                        self._log_error(f"Multiple storage classes: {storage_class} and {keyword}")
                        break
                elif keyword in ['inline', 'virtual', 'explicit', 'constexpr', 'consteval', 'constinit']:
                    modifiers.append(self._advance().value)
                elif keyword in ['const', 'volatile', 'noexcept']:
                    modifiers.append(self._advance().value)
                else:
                    break
            
            # Parse the type
            decl_type = self._parse_type()
            
            # Parse declarator (name and array/function modifiers)
            declarator = self._parse_declarator()
            if not declarator:
                return None
            
            name = declarator['name']
            array_dims = declarator.get('array_dims', [])
            function_params = declarator.get('function_params', None)
            is_function_pointer = declarator.get('is_function_pointer', False)
            
            # Determine if it's a function or variable declaration
            if function_params is not None or is_function_pointer:
                return self._parse_function_declaration_rest(name, decl_type, function_params, modifiers, storage_class)
            else:
                return self._parse_variable_declaration_rest(name, decl_type, array_dims, modifiers, storage_class)
                
        except Exception as e:
            self._log_error(f"Error parsing function/variable declaration: {e}")
            return None
    
    def _parse_declarator(self) -> Optional[Dict[str, Any]]:
        """Parse declarator with full C++ support."""
        try:
            # Handle function pointers: int (*func)(int, char)
            if self._match(CppTokenType.LEFT_PAREN):
                self._advance()
                if self._match(CppTokenType.MULTIPLY):
                    self._advance()
                    name = self._consume(CppTokenType.IDENTIFIER).value
                    self._consume(CppTokenType.RIGHT_PAREN)
                    
                    # Parse function parameters
                    self._consume(CppTokenType.LEFT_PAREN)
                    params = self._parse_parameter_list()
                    self._consume(CppTokenType.RIGHT_PAREN)
                    
                    return {
                        'name': name,
                        'function_params': params,
                        'is_function_pointer': True
                    }
                else:
                    # Parenthesized declarator: int (var)
                    declarator = self._parse_declarator()
                    self._consume(CppTokenType.RIGHT_PAREN)
                    return declarator
            
            # Parse identifier
            if not self._match(CppTokenType.IDENTIFIER):
                return None
            
            name = self._advance().value
            
            # Parse array dimensions: int arr[10][20]
            array_dims = []
            while self._match(CppTokenType.LEFT_BRACKET):
                self._advance()
                if not self._match(CppTokenType.RIGHT_BRACKET):
                    array_dims.append(self._parse_expression())
                self._consume(CppTokenType.RIGHT_BRACKET)
            
            # Parse function parameters: int func(int, char)
            function_params = None
            if self._match(CppTokenType.LEFT_PAREN):
                self._advance()
                function_params = self._parse_parameter_list()
                self._consume(CppTokenType.RIGHT_PAREN)
            
            return {
                'name': name,
                'array_dims': array_dims,
                'function_params': function_params
            }
            
        except Exception as e:
            self._log_error(f"Error parsing declarator: {e}")
            return None
    
    def _parse_function_declaration_rest(self, name: str, return_type: CppType, function_params: Optional[CppParameterList] = None, modifiers: List[str] = [], storage_class: Optional[str] = None) -> CppFunctionDecl:
        """Parse rest of function declaration."""
        # Apply modifiers and storage class
        final_modifiers = modifiers.copy()
        final_storage_class = storage_class
        
        # Add function parameters if provided
        if function_params:
            final_modifiers.append('function_params') # Indicate that this is a function parameter list
        
        # Add pure_virtual if it's a function pointer with value 0
        if isinstance(return_type, CppBuiltinType) and return_type.name == 'void' and function_params is None:
            final_modifiers.append('pure_virtual')
        
        # Add defaulted/deleted/pure_virtual/function_params if they were added by the declarator
        if 'defaulted' in final_modifiers:
            final_modifiers.remove('defaulted') # Remove the defaulted flag if it was added by the declarator
        if 'deleted' in final_modifiers:
            final_modifiers.remove('deleted') # Remove the deleted flag if it was added by the declarator
        if 'pure_virtual' in final_modifiers:
            final_modifiers.remove('pure_virtual') # Remove the pure_virtual flag if it was added by the declarator
        if 'function_params' in final_modifiers:
            final_modifiers.remove('function_params') # Remove the function_params flag if it was added by the declarator
        
        # Parse const qualifier
        is_const = self._match(CppTokenType.KEYWORD) and self._current_token().value == 'const'
        if is_const:
            self._advance()
            final_modifiers.append('const')
        
        # Parse override/final specifiers
        if self._match(CppTokenType.KEYWORD) and self._current_token().value == 'override':
            self._advance()
            final_modifiers.append('override')
        elif self._match(CppTokenType.KEYWORD) and self._current_token().value == 'final':
            self._advance()
            final_modifiers.append('final')
        
        # Parse noexcept specifier
        if self._match(CppTokenType.KEYWORD) and self._current_token().value == 'noexcept':
            self._advance()
            final_modifiers.append('noexcept')
            if self._match(CppTokenType.LEFT_PAREN):
                self._advance()
                self._parse_expression()  # Parse noexcept condition
                self._consume(CppTokenType.RIGHT_PAREN)
        
        # Parse function body or pure virtual specifier
        body = None
        if self._match(CppTokenType.LEFT_BRACE):
            body = self._parse_compound_statement()
        elif self._match(CppTokenType.ASSIGN):
            self._advance()
            if self._match(CppTokenType.INTEGER_LITERAL) and self._current_token().value == '0':
                self._advance()
                final_modifiers.append('pure_virtual')
            else:
                # Defaulted function
                self._consume(CppTokenType.KEYWORD)  # default
        elif self._match(CppTokenType.KEYWORD) and self._current_token().value == 'default':
            self._advance()
            final_modifiers.append('defaulted')
        elif self._match(CppTokenType.KEYWORD) and self._current_token().value == 'delete':
            self._advance()
            final_modifiers.append('deleted')
        elif self._match(CppTokenType.SEMICOLON):
            self._advance()
        
        return CppFunctionDecl(
            name=name,
            return_type=return_type,
            parameters=function_params if function_params else CppParameterList([]), # Use provided or empty
            body=body,
            storage_class=final_storage_class
        )
    
    def _parse_variable_declaration_rest(self, name: str, var_type: CppType, array_dims: List[CppExpression] = [], modifiers: List[str] = [], storage_class: Optional[str] = None) -> CppVariableDecl:
        """Parse rest of variable declaration."""
        # Apply modifiers and storage class
        final_modifiers = modifiers.copy()
        final_storage_class = storage_class
        
        # Add pure_virtual if it's a function pointer with value 0
        if isinstance(var_type, CppBuiltinType) and var_type.name == 'void' and array_dims == []:
            final_modifiers.append('pure_virtual')
        
        # Add defaulted/deleted/pure_virtual/function_params if they were added by the declarator
        if 'defaulted' in final_modifiers:
            final_modifiers.remove('defaulted') # Remove the defaulted flag if it was added by the declarator
        if 'deleted' in final_modifiers:
            final_modifiers.remove('deleted') # Remove the deleted flag if it was added by the declarator
        if 'pure_virtual' in final_modifiers:
            final_modifiers.remove('pure_virtual') # Remove the pure_virtual flag if it was added by the declarator
        if 'function_params' in final_modifiers:
            final_modifiers.remove('function_params') # Remove the function_params flag if it was added by the declarator
        
        # Parse const qualifier
        is_const = self._match(CppTokenType.KEYWORD) and self._current_token().value == 'const'
        if is_const:
            self._advance()
            final_modifiers.append('const')
        
        # Parse initializer
        initializer = None
        if self._match(CppTokenType.ASSIGN):
            self._advance()
            initializer = self._parse_expression()
        elif self._match(CppTokenType.LEFT_PAREN):
            self._advance()
            initializer = self._parse_expression()
            self._consume(CppTokenType.RIGHT_PAREN)
        elif self._match(CppTokenType.LEFT_BRACE):
            initializer = self._parse_initializer_list()
        
        self._consume(CppTokenType.SEMICOLON)
        
        return CppVariableDecl(
            name=name,
            var_type=var_type,
            initializer=initializer,
            storage_class=final_storage_class
        )
    
    def _parse_compound_statement(self) -> CppCompoundStmt:
        """Parse comprehensive compound statement with full C++ support."""
        try:
            self._consume(CppTokenType.LEFT_BRACE)
            
            statements = []
            while not self._match(CppTokenType.RIGHT_BRACE) and not self._at_end():
                # Handle variable declarations at block scope
                if self._is_declaration_start():
                    decl = self._parse_declaration()
                    if decl:
                        statements.append(decl)
                else:
                    # Parse regular statement
                    stmt = self._parse_statement()
                    if stmt:
                        statements.append(stmt)
            
            self._consume(CppTokenType.RIGHT_BRACE)
            
            return CppCompoundStmt(statements)
            
        except Exception as e:
            self._log_error(f"Error parsing compound statement: {e}")
            # Fallback to empty compound statement
            return CppCompoundStmt([])
    
    def _is_declaration_start(self) -> bool:
        """Check if current token starts a declaration."""
        if not self._match(CppTokenType.KEYWORD):
            return False
        
        keyword = self._current_token().value
        return keyword in [
            'auto', 'bool', 'char', 'char8_t', 'char16_t', 'char32_t', 'double', 'float',
            'int', 'long', 'short', 'signed', 'unsigned', 'void', 'wchar_t',
            'class', 'struct', 'union', 'enum', 'typedef', 'using', 'template',
            'extern', 'static', 'thread_local', 'mutable', 'inline', 'virtual',
            'explicit', 'constexpr', 'consteval', 'constinit', 'const', 'volatile'
        ]
    
    def _parse_statement(self) -> Optional[CppStatement]:
        """Parse comprehensive statement with full C++ support."""
        try:
            # Handle different statement types
            if self._match(CppTokenType.KEYWORD):
                keyword = self._current_token().value
                
                if keyword == 'if':
                    return self._parse_if_statement()
                elif keyword == 'while':
                    return self._parse_while_statement()
                elif keyword == 'for':
                    return self._parse_for_statement()
                elif keyword == 'do':
                    return self._parse_do_while_statement()
                elif keyword == 'switch':
                    return self._parse_switch_statement()
                elif keyword == 'case':
                    return self._parse_case_statement()
                elif keyword == 'default':
                    return self._parse_default_statement()
                elif keyword == 'break':
                    return self._parse_break_statement()
                elif keyword == 'continue':
                    return self._parse_continue_statement()
                elif keyword == 'return':
                    return self._parse_return_statement()
                elif keyword == 'goto':
                    return self._parse_goto_statement()
                elif keyword == 'try':
                    return self._parse_try_statement()
                elif keyword == 'throw':
                    return self._parse_throw_statement()
                elif keyword in ['auto', 'bool', 'char', 'char8_t', 'char16_t', 'char32_t', 
                               'double', 'float', 'int', 'long', 'short', 'signed', 
                               'unsigned', 'void', 'wchar_t', 'class', 'struct', 'union', 
                               'enum', 'typedef', 'using', 'template', 'extern', 'static', 
                               'thread_local', 'mutable', 'inline', 'virtual', 'explicit', 
                               'constexpr', 'consteval', 'constinit', 'const', 'volatile']:
                    # Variable declaration
                    decl = self._parse_declaration()
                    if decl:
                        return CppDeclarationStmt(decl)
            
            # Handle expression statement
            if self._match(CppTokenType.LEFT_BRACE):
                return self._parse_compound_statement()
            elif self._match(CppTokenType.SEMICOLON):
                self._advance()
                return CppEmptyStmt()
            else:
                # Expression statement
                expr = self._parse_expression()
                if expr:
                    self._consume(CppTokenType.SEMICOLON)
                    return CppExpressionStmt(expr)
            
            return None
            
        except Exception as e:
            self._log_error(f"Error parsing statement: {e}")
            return None
    
    def _parse_do_while_statement(self) -> CppDoWhileStmt:
        """Parse do-while statement."""
        self._consume(CppTokenType.KEYWORD)  # do
        
        body = self._parse_statement()
        
        self._consume(CppTokenType.KEYWORD)  # while
        self._consume(CppTokenType.LEFT_PAREN)
        condition = self._parse_expression()
        self._consume(CppTokenType.RIGHT_PAREN)
        self._consume(CppTokenType.SEMICOLON)
        
        return CppDoWhileStmt(condition, body)
    
    def _parse_switch_statement(self) -> CppSwitchStmt:
        """Parse switch statement."""
        self._consume(CppTokenType.KEYWORD)  # switch
        
        self._consume(CppTokenType.LEFT_PAREN)
        condition = self._parse_expression()
        self._consume(CppTokenType.RIGHT_PAREN)
        
        body = self._parse_statement()
        
        return CppSwitchStmt(condition, body)
    
    def _parse_case_statement(self) -> CppCaseStmt:
        """Parse case statement."""
        self._consume(CppTokenType.KEYWORD)  # case
        
        value = self._parse_expression()
        self._consume(CppTokenType.COLON)
        
        body = self._parse_statement()
        
        return CppCaseStmt(value, body)
    
    def _parse_default_statement(self) -> CppDefaultStmt:
        """Parse default statement."""
        self._consume(CppTokenType.KEYWORD)  # default
        self._consume(CppTokenType.COLON)
        
        body = self._parse_statement()
        
        return CppDefaultStmt(body)
    
    def _parse_break_statement(self) -> CppBreakStmt:
        """Parse break statement."""
        self._consume(CppTokenType.KEYWORD)  # break
        self._consume(CppTokenType.SEMICOLON)
        
        return CppBreakStmt()
    
    def _parse_continue_statement(self) -> CppContinueStmt:
        """Parse continue statement."""
        self._consume(CppTokenType.KEYWORD)  # continue
        self._consume(CppTokenType.SEMICOLON)
        
        return CppContinueStmt()
    
    def _parse_goto_statement(self) -> CppGotoStmt:
        """Parse goto statement."""
        self._consume(CppTokenType.KEYWORD)  # goto
        
        label = self._consume(CppTokenType.IDENTIFIER).value
        self._consume(CppTokenType.SEMICOLON)
        
        return CppGotoStmt(label)
    
    def _parse_try_statement(self) -> CppTryStmt:
        """Parse try statement."""
        self._consume(CppTokenType.KEYWORD)  # try
        
        try_block = self._parse_compound_statement()
        
        # Parse catch blocks
        catch_blocks = []
        while self._match(CppTokenType.KEYWORD) and self._current_token().value == 'catch':
            catch_blocks.append(self._parse_catch_block())
        
        return CppTryStmt(try_block, catch_blocks)
    
    def _parse_catch_block(self) -> CppCatchBlock:
        """Parse catch block."""
        self._consume(CppTokenType.KEYWORD)  # catch
        
        self._consume(CppTokenType.LEFT_PAREN)
        
        # Parse exception declaration
        exception_type = None
        exception_name = None
        if not self._match(CppTokenType.RIGHT_PAREN):
            exception_type = self._parse_type()
            if self._match(CppTokenType.IDENTIFIER):
                exception_name = self._advance().value
        
        self._consume(CppTokenType.RIGHT_PAREN)
        
        body = self._parse_compound_statement()
        
        return CppCatchBlock(exception_type, exception_name, body)
    
    def _parse_throw_statement(self) -> CppThrowStmt:
        """Parse throw statement."""
        self._consume(CppTokenType.KEYWORD)  # throw
        
        expression = None
        if not self._match(CppTokenType.SEMICOLON):
            expression = self._parse_expression()
        
        self._consume(CppTokenType.SEMICOLON)
        
        return CppThrowStmt(expression)
    
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
        """Parse comprehensive C++ for statement (production-ready)."""
        self._consume(CppTokenType.KEYWORD)  # for
        self._consume(CppTokenType.LEFT_PAREN)

        # Parse init statement: can be declaration or expression or empty
        init = None
        if not self._match(CppTokenType.SEMICOLON):
            if self._is_declaration_start():
                init = self._parse_declaration()
            else:
                init = self._parse_statement()
        self._consume(CppTokenType.SEMICOLON)

        # Parse condition expression or empty
        condition = None
        if not self._match(CppTokenType.SEMICOLON):
            condition = self._parse_expression()
        self._consume(CppTokenType.SEMICOLON)

        # Parse increment expression or empty
        increment = None
        if not self._match(CppTokenType.RIGHT_PAREN):
            increment = self._parse_expression()
        self._consume(CppTokenType.RIGHT_PAREN)

        # Parse loop body (statement or block)
        body = self._parse_statement()

        return CppForStmt(init=init, condition=condition, increment=increment, body=body)
    
    def _parse_return_statement(self) -> CppReturnStmt:
        """Parse return statement."""
        self._consume(CppTokenType.KEYWORD)  # return
        
        value = None
        if not self._match(CppTokenType.SEMICOLON):
            value = self._parse_expression()
        
        self._consume(CppTokenType.SEMICOLON)
        
        return CppReturnStmt(value)
    
    def _parse_expression(self) -> Optional[CppExpression]:
        """Parse comprehensive expression with full C++ support."""
        try:
            # Start with assignment expressions (lowest precedence)
            return self._parse_assignment()
        except Exception as e:
            self._log_error(f"Error parsing expression: {e}")
            return None
    
    def _parse_assignment(self) -> Optional[CppExpression]:
        """Parse assignment expressions: a = b, a += b, etc."""
        left = self._parse_conditional()
        
        if self._match(CppTokenType.ASSIGN, CppTokenType.PLUS_ASSIGN, CppTokenType.MINUS_ASSIGN,
                      CppTokenType.MULTIPLY_ASSIGN, CppTokenType.DIVIDE_ASSIGN, CppTokenType.MODULO_ASSIGN,
                      CppTokenType.LEFT_SHIFT_ASSIGN, CppTokenType.RIGHT_SHIFT_ASSIGN,
                      CppTokenType.BIT_AND_ASSIGN, CppTokenType.BIT_OR_ASSIGN, CppTokenType.BIT_XOR_ASSIGN):
            operator = self._advance().value
            right = self._parse_assignment()  # Right-associative
            return CppBinaryOp(left, operator, right)
        
        return left
    
    def _parse_conditional(self) -> Optional[CppExpression]:
        """Parse conditional expressions: a ? b : c."""
        condition = self._parse_logical_or()
        
        if self._match(CppTokenType.QUESTION):
            self._advance()
            true_expr = self._parse_expression()
            self._consume(CppTokenType.COLON)
            false_expr = self._parse_conditional()  # Right-associative
            return CppConditionalOp(condition, true_expr, false_expr)
        
        return condition
    
    def _parse_logical_or(self) -> Optional[CppExpression]:
        """Parse logical OR expressions: a || b."""
        left = self._parse_logical_and()
        
        while self._match(CppTokenType.LOGICAL_OR):
            operator = self._advance().value
            right = self._parse_logical_and()
            left = CppBinaryOp(left, operator, right)
        
        return left
    
    def _parse_logical_and(self) -> Optional[CppExpression]:
        """Parse logical AND expressions: a && b."""
        left = self._parse_bitwise_or()
        
        while self._match(CppTokenType.LOGICAL_AND):
            operator = self._advance().value
            right = self._parse_bitwise_or()
            left = CppBinaryOp(left, operator, right)
        
        return left
    
    def _parse_bitwise_or(self) -> Optional[CppExpression]:
        """Parse bitwise OR expressions: a | b."""
        left = self._parse_bitwise_xor()
        
        while self._match(CppTokenType.BIT_OR):
            operator = self._advance().value
            right = self._parse_bitwise_xor()
            left = CppBinaryOp(left, operator, right)
        
        return left
    
    def _parse_bitwise_xor(self) -> Optional[CppExpression]:
        """Parse bitwise XOR expressions: a ^ b."""
        left = self._parse_bitwise_and()
        
        while self._match(CppTokenType.BIT_XOR):
            operator = self._advance().value
            right = self._parse_bitwise_and()
            left = CppBinaryOp(left, operator, right)
        
        return left
    
    def _parse_bitwise_and(self) -> Optional[CppExpression]:
        """Parse bitwise AND expressions: a & b."""
        left = self._parse_equality()
        
        while self._match(CppTokenType.BIT_AND):
            operator = self._advance().value
            right = self._parse_equality()
            left = CppBinaryOp(left, operator, right)
        
        return left
    
    def _parse_equality(self) -> Optional[CppExpression]:
        """Parse equality expressions: a == b, a != b."""
        left = self._parse_relational()
        
        while self._match(CppTokenType.EQUAL, CppTokenType.NOT_EQUAL):
            operator = self._advance().value
            right = self._parse_relational()
            left = CppBinaryOp(left, operator, right)
        
        return left
    
    def _parse_relational(self) -> Optional[CppExpression]:
        """Parse relational expressions: a < b, a <= b, etc."""
        left = self._parse_shift()
        
        while self._match(CppTokenType.LESS, CppTokenType.LESS_EQUAL, 
                         CppTokenType.GREATER, CppTokenType.GREATER_EQUAL):
            operator = self._advance().value
            right = self._parse_shift()
            left = CppBinaryOp(left, operator, right)
        
        return left
    
    def _parse_shift(self) -> Optional[CppExpression]:
        """Parse shift expressions: a << b, a >> b."""
        left = self._parse_additive()
        
        while self._match(CppTokenType.LEFT_SHIFT, CppTokenType.RIGHT_SHIFT):
            operator = self._advance().value
            right = self._parse_additive()
            left = CppBinaryOp(left, operator, right)
        
        return left
    
    def _parse_additive(self) -> Optional[CppExpression]:
        """Parse additive expressions: a + b, a - b."""
        left = self._parse_multiplicative()
        
        while self._match(CppTokenType.PLUS, CppTokenType.MINUS):
            operator = self._advance().value
            right = self._parse_multiplicative()
            left = CppBinaryOp(left, operator, right)
        
        return left
    
    def _parse_multiplicative(self) -> Optional[CppExpression]:
        """Parse multiplicative expressions: a * b, a / b, a % b."""
        left = self._parse_cast()
        
        while self._match(CppTokenType.MULTIPLY, CppTokenType.DIVIDE, CppTokenType.MODULO):
            operator = self._advance().value
            right = self._parse_cast()
            left = CppBinaryOp(left, operator, right)
        
        return left
    
    def _parse_cast(self) -> Optional[CppExpression]:
        """Parse cast expressions: (type)expr, static_cast<type>(expr), etc."""
        # Handle C-style cast: (type)expr
        if self._match(CppTokenType.LEFT_PAREN):
            # Check if it's a type cast
            if self._is_type_start():
                self._advance()
                cast_type = self._parse_type()
                self._consume(CppTokenType.RIGHT_PAREN)
                operand = self._parse_cast()
                return CppCast(target_type=cast_type, operand=operand, cast_kind="c_style")
        
        # Handle C++ style casts: static_cast<type>(expr)
        if self._match(CppTokenType.KEYWORD):
            keyword = self._current_token().value
            if keyword in ['static_cast', 'dynamic_cast', 'const_cast', 'reinterpret_cast']:
                self._advance()
                self._consume(CppTokenType.LESS)
                cast_type = self._parse_type()
                self._consume(CppTokenType.GREATER)
                self._consume(CppTokenType.LEFT_PAREN)
                operand = self._parse_expression()
                self._consume(CppTokenType.RIGHT_PAREN)
                return CppCast(target_type=cast_type, operand=operand, cast_kind=keyword)
        
        return self._parse_unary()
    
    def _is_type_start(self) -> bool:
        """Check if current token starts a type."""
        if not self._match(CppTokenType.KEYWORD):
            return False
        
        keyword = self._current_token().value
        return keyword in [
            'auto', 'bool', 'char', 'char8_t', 'char16_t', 'char32_t', 'double', 'float',
            'int', 'long', 'short', 'signed', 'unsigned', 'void', 'wchar_t',
            'class', 'struct', 'union', 'enum', 'typename'
        ]
    
    def _parse_unary(self) -> Optional[CppExpression]:
        """Parse unary expressions: ++a, --a, +a, -a, !a, ~a, *a, &a."""
        if self._match(CppTokenType.INCREMENT, CppTokenType.DECREMENT):
            operator = self._advance().value
            operand = self._parse_unary()
            return CppUnaryOp(operator, operand, is_prefix=True)
        
        if self._match(CppTokenType.PLUS, CppTokenType.MINUS, CppTokenType.LOGICAL_NOT, 
                      CppTokenType.BIT_NOT, CppTokenType.MULTIPLY, CppTokenType.BIT_AND):
            operator = self._advance().value
            operand = self._parse_cast()
            return CppUnaryOp(operator, operand)
        
        return self._parse_postfix()
    
    def _parse_postfix(self) -> Optional[CppExpression]:
        """Parse postfix expressions: a++, a--, a[b], a(b), a.b, a->b."""
        expr = self._parse_primary()
        
        while True:
            if self._match(CppTokenType.LEFT_BRACKET):
                # Array access: a[b]
                self._advance()
                index = self._parse_expression()
                self._consume(CppTokenType.RIGHT_BRACKET)
                expr = CppArraySubscript(array=expr, index=index)
            
            elif self._match(CppTokenType.LEFT_PAREN):
                # Function call: a(b, c)
                self._advance()
                arguments = []
                if not self._match(CppTokenType.RIGHT_PAREN):
                    while True:
                        arguments.append(self._parse_expression())
                        if self._match(CppTokenType.COMMA):
                            self._advance()
                        else:
                            break
                self._consume(CppTokenType.RIGHT_PAREN)
                expr = CppCall(function=expr, arguments=arguments)
            
            elif self._match(CppTokenType.DOT, CppTokenType.ARROW):
                # Member access: a.b, a->b
                operator = self._advance().value
                member = self._consume(CppTokenType.IDENTIFIER).value
                expr = CppMemberAccess(object=expr, member=member, is_arrow=(operator == "->"))
            
            elif self._match(CppTokenType.INCREMENT, CppTokenType.DECREMENT):
                # Postfix increment/decrement: a++, a--
                operator = self._advance().value
                # Map string operator to CppOperator enum for postfix operations
                cpp_op = CppOperator.POST_INC if operator == "++" else CppOperator.POST_DEC
                expr = CppUnaryOp(operator=cpp_op, operand=expr, is_postfix=True)
            
            else:
                break
        
        return expr
    
    def _log_error(self, message: str):
        """Log error message and add to error list."""
        import sys
        error_msg = f"CPP Parser Error: {message}"
        self.errors.append(error_msg)
        print(error_msg, file=sys.stderr)
    
    def _parse_catch_block(self) -> CppCatchBlock:
        """Parse catch block."""
        try:
            self._consume(CppTokenType.KEYWORD)  # catch
            self._consume(CppTokenType.LEFT_PAREN)
            
            exception_type = None
            exception_name = None
            
            if not self._match(CppTokenType.ELLIPSIS):
                exception_type = self._parse_type()
                if self._match(CppTokenType.IDENTIFIER):
                    exception_name = self._current_token().value
                    self._advance()
            else:
                self._advance()  # consume ...
            
            self._consume(CppTokenType.RIGHT_PAREN)
            body = self._parse_compound_statement()
            
            return CppCatchBlock(
                exception_type=exception_type,
                exception_name=exception_name,
                body=body
            )
        except Exception as e:
            self._log_error(f"Error parsing catch block: {e}")
            return CppCatchBlock()
    
    def _parse_initializer_list(self) -> CppInitializerList:
        """Parse initializer list."""
        try:
            elements = []
            
            if self._match(CppTokenType.LEFT_BRACE):
                self._advance()
                
                while not self._match(CppTokenType.RIGHT_BRACE) and not self._at_end():
                    elements.append(self._parse_expression())
                    if self._match(CppTokenType.COMMA):
                        self._advance()
                    else:
                        break
                
                self._consume(CppTokenType.RIGHT_BRACE)
            
            return CppInitializerList(elements=elements)
        except Exception as e:
            self._log_error(f"Error parsing initializer list: {e}")
            return CppInitializerList()
    
    def _parse_member_array_declaration(self, name: str, element_type: CppType, access: str) -> CppVariableDecl:
        """Parse member array declaration."""
        try:
            array_dims = []
            
            while self._match(CppTokenType.LEFT_BRACKET):
                self._advance()
                if not self._match(CppTokenType.RIGHT_BRACKET):
                    size = self._parse_expression()
                    array_dims.append(size)
                self._consume(CppTokenType.RIGHT_BRACKET)
            
            array_type = element_type
            for _ in array_dims:
                array_type = CppArrayType(element_type=array_type)
            
            return CppVariableDecl(
                name=name,
                var_type=array_type,
                storage_class=access
            )
        except Exception as e:
            self._log_error(f"Error parsing member array declaration: {e}")
            return CppVariableDecl(name=name, var_type=element_type)
    
    def _parse_parameter_list(self) -> CppParameterList:
        """Parse function parameter list."""
        try:
            parameters = []
            is_variadic = False
            
            if self._match(CppTokenType.LEFT_PAREN):
                self._advance()
                
                while not self._match(CppTokenType.RIGHT_PAREN) and not self._at_end():
                    if self._match(CppTokenType.ELLIPSIS):
                        is_variadic = True
                        self._advance()
                        break
                    
                    param_type = self._parse_type()
                    param_name = None
                    default_value = None
                    
                    if self._match(CppTokenType.IDENTIFIER):
                        param_name = self._current_token().value
                        self._advance()
                    
                    if self._match(CppTokenType.ASSIGN):
                        self._advance()
                        default_value = self._parse_expression()
                    
                    parameters.append(CppParameter(
                        name=param_name,
                        param_type=param_type,
                        default_value=default_value
                    ))
                    
                    if self._match(CppTokenType.COMMA):
                        self._advance()
                    else:
                        break
                
                self._consume(CppTokenType.RIGHT_PAREN)
            
            return CppParameterList(parameters=parameters, is_variadic=is_variadic)
        except Exception as e:
            self._log_error(f"Error parsing parameter list: {e}")
            return CppParameterList()
    
    def _parse_primary(self) -> CppExpression:
        """Parse primary expression."""
        try:
            if self._match(CppTokenType.INTEGER_LITERAL):
                value = int(self._current_token().value)
                self._advance()
                return CppIntegerLiteral(value=value)
            
            if self._match(CppTokenType.FLOATING_LITERAL):
                value = float(self._current_token().value)
                self._advance()
                return CppFloatingLiteral(value=value)
            
            if self._match(CppTokenType.STRING_LITERAL):
                value = self._current_token().value
                self._advance()
                return CppStringLiteral(value=value)
            
            if self._match(CppTokenType.CHARACTER_LITERAL):
                value = self._current_token().value
                self._advance()
                return CppCharacterLiteral(value=value)
            
            if self._match(CppTokenType.BOOLEAN_LITERAL):
                value = self._current_token().value.lower() == "true"
                self._advance()
                return CppBooleanLiteral(value=value)
            
            if self._match(CppTokenType.NULLPTR_LITERAL):
                self._advance()
                return CppNullptrLiteral()
            
            if self._match(CppTokenType.IDENTIFIER):
                name = self._current_token().value
                self._advance()
                return CppIdentifier(name=name)
            
            if self._match(CppTokenType.LEFT_PAREN):
                self._advance()
                expr = self._parse_expression()
                self._consume(CppTokenType.RIGHT_PAREN)
                return expr
            
            self._log_error(f"Unexpected token in primary expression: {self._current_token().type}")
            return CppIdentifier(name="<error>")
        
        except Exception as e:
            self._log_error(f"Error parsing primary expression: {e}")
            return CppIdentifier(name="<error>")
    
    def _parse_template_argument_list(self) -> List[CppExpression]:
        """Parse template argument list."""
        try:
            arguments = []
            
            if self._match(CppTokenType.LESS):
                self._advance()
                
                while not self._match(CppTokenType.GREATER) and not self._at_end():
                    # Template arguments can be types or expressions
                    if self._is_type_start():
                        arg_type = self._parse_type()
                        # Convert type to expression representation
                        arguments.append(CppIdentifier(name=str(arg_type)))
                    else:
                        arguments.append(self._parse_expression())
                    
                    if self._match(CppTokenType.COMMA):
                        self._advance()
                    else:
                        break
                
                self._consume(CppTokenType.GREATER)
            
            return arguments
        except Exception as e:
            self._log_error(f"Error parsing template argument list: {e}")
            return []
    
    def _parse_template_parameter_list(self) -> CppTemplateParameterList:
        """Parse template parameter list."""
        try:
            parameters = []
            
            if self._match(CppTokenType.LESS):
                self._advance()
                
                while not self._match(CppTokenType.GREATER) and not self._at_end():
                    param_kind = "type"  # Default to type parameter
                    param_name = None
                    default_value = None
                    is_pack = False
                    
                    # Check for typename or class keyword
                    if self._match(CppTokenType.KEYWORD):
                        keyword = self._current_token().value
                        if keyword in ["typename", "class"]:
                            self._advance()
                            param_kind = "type"
                        elif keyword == "template":
                            self._advance()
                            param_kind = "template"
                    
                    # Check for parameter pack
                    if self._match(CppTokenType.ELLIPSIS):
                        is_pack = True
                        self._advance()
                    
                    # Get parameter name
                    if self._match(CppTokenType.IDENTIFIER):
                        param_name = self._current_token().value
                        self._advance()
                    
                    # Check for default value
                    if self._match(CppTokenType.ASSIGN):
                        self._advance()
                        if param_kind == "type":
                            default_value = self._parse_type()
                        else:
                            default_value = self._parse_expression()
                    
                    parameters.append(CppTemplateParameter(
                        name=param_name,
                        kind=param_kind,
                        default_value=default_value,
                        is_pack=is_pack
                    ))
                    
                    if self._match(CppTokenType.COMMA):
                        self._advance()
                    else:
                        break
                
                self._consume(CppTokenType.GREATER)
            
            return CppTemplateParameterList(parameters=parameters)
        except Exception as e:
            self._log_error(f"Error parsing template parameter list: {e}")
            return CppTemplateParameterList()
    
    def _parse_type(self) -> CppType:
        """Parse type expression."""
        try:
            # Handle type qualifiers
            qualifiers = []
            while self._match(CppTokenType.KEYWORD):
                keyword = self._current_token().value
                if keyword in ["const", "volatile", "restrict"]:
                    if keyword == "const":
                        qualifiers.append(CppTypeQualifier.CONST)
                    elif keyword == "volatile":
                        qualifiers.append(CppTypeQualifier.VOLATILE)
                    elif keyword == "restrict":
                        qualifiers.append(CppTypeQualifier.RESTRICT)
                    self._advance()
                else:
                    break
            
            # Parse base type
            base_type = None
            
            if self._match(CppTokenType.KEYWORD):
                keyword = self._current_token().value
                if keyword in ["int", "char", "float", "double", "void", "bool", 
                              "short", "long", "signed", "unsigned"]:
                    self._advance()
                    base_type = CppBuiltinType(name=keyword, qualifiers=qualifiers)
                elif keyword == "auto":
                    self._advance()
                    base_type = CppAutoType(qualifiers=qualifiers)
                elif keyword == "decltype":
                    self._advance()
                    self._consume(CppTokenType.LEFT_PAREN)
                    expr = self._parse_expression()
                    self._consume(CppTokenType.RIGHT_PAREN)
                    base_type = CppDecltypeType(expression=expr, qualifiers=qualifiers)
            
            elif self._match(CppTokenType.IDENTIFIER):
                name = self._current_token().value
                self._advance()
                base_type = CppBuiltinType(name=name, qualifiers=qualifiers)
            
            if base_type is None:
                base_type = CppBuiltinType(name="int", qualifiers=qualifiers)
            
            # Handle pointers and references
            while True:
                if self._match(CppTokenType.MULTIPLY):
                    self._advance()
                    base_type = CppPointerType(pointee_type=base_type)
                elif self._match(CppTokenType.BIT_AND):
                    self._advance()
                    is_rvalue = False
                    if self._match(CppTokenType.BIT_AND):
                        self._advance()
                        is_rvalue = True
                    base_type = CppReferenceType(referenced_type=base_type, is_rvalue_reference=is_rvalue)
                else:
                    break
            
            return base_type
        
        except Exception as e:
            self._log_error(f"Error parsing type: {e}")
            return CppBuiltinType(name="int")


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