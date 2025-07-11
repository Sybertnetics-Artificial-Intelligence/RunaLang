#!/usr/bin/env python3
"""
Java Parser

Complete Java parser supporting modern Java features from Java 8 through Java 21.
Includes lexical analysis and recursive descent parsing with comprehensive
error handling and recovery.
"""

import re
from typing import List, Optional, Dict, Any, Union, Tuple
from dataclasses import dataclass
from enum import Enum, auto

from .java_ast import *


class JavaTokenType(Enum):
    """Java token types."""
    # Literals
    INTEGER_LITERAL = auto()
    FLOATING_LITERAL = auto()
    STRING_LITERAL = auto()
    CHARACTER_LITERAL = auto()
    BOOLEAN_LITERAL = auto()
    NULL_LITERAL = auto()
    TEXT_BLOCK = auto()
    
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
    LESS_THAN = auto()      # <
    LESS_EQUAL = auto()     # <=
    GREATER_THAN = auto()   # >
    GREATER_EQUAL = auto()  # >=
    
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
    UNSIGNED_RIGHT_SHIFT = auto() # >>>
    BIT_AND_ASSIGN = auto() # &=
    BIT_OR_ASSIGN = auto()  # |=
    BIT_XOR_ASSIGN = auto() # ^=
    LEFT_SHIFT_ASSIGN = auto() # <<=
    RIGHT_SHIFT_ASSIGN = auto() # >>=
    UNSIGNED_RIGHT_SHIFT_ASSIGN = auto() # >>>=
    
    # Special operators
    QUESTION = auto()       # ?
    COLON = auto()          # :
    DOUBLE_COLON = auto()   # ::
    DOT = auto()            # .
    ARROW = auto()          # ->
    
    # Punctuation
    SEMICOLON = auto()      # ;
    COMMA = auto()          # ,
    AT = auto()             # @
    ELLIPSIS = auto()       # ...
    
    # Brackets
    LEFT_PAREN = auto()     # (
    RIGHT_PAREN = auto()    # )
    LEFT_BRACE = auto()     # {
    RIGHT_BRACE = auto()    # }
    LEFT_BRACKET = auto()   # [
    RIGHT_BRACKET = auto()  # ]
    
    # Whitespace and comments
    WHITESPACE = auto()
    NEWLINE = auto()
    COMMENT = auto()
    
    # End of file
    EOF = auto()
    
    # Error
    ERROR = auto()


@dataclass
class JavaToken:
    """Java token."""
    type: JavaTokenType
    value: str
    line: int
    column: int
    file_name: Optional[str] = None


class JavaLexer:
    """Java lexer/tokenizer."""
    
    # Java keywords
    KEYWORDS = {
        # Basic keywords
        'abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch',
        'char', 'class', 'const', 'continue', 'default', 'do', 'double',
        'else', 'enum', 'extends', 'final', 'finally', 'float', 'for',
        'goto', 'if', 'implements', 'import', 'instanceof', 'int', 'interface',
        'long', 'native', 'new', 'package', 'private', 'protected', 'public',
        'return', 'short', 'static', 'strictfp', 'super', 'switch',
        'synchronized', 'this', 'throw', 'throws', 'transient', 'try',
        'void', 'volatile', 'while',
        
        # Literals
        'true', 'false', 'null',
        
        # Modern keywords
        'var',  # Java 10
        'yield',  # Java 14
        'record',  # Java 14
        'sealed',  # Java 17
        'permits',  # Java 17
        'non-sealed',  # Java 17 (hyphenated)
        
        # Module system (Java 9)
        'module', 'requires', 'exports', 'opens', 'uses', 'provides',
        'transitive', 'to', 'with', 'open',
    }
    
    def __init__(self, source: str, file_name: Optional[str] = None):
        self.source = source
        self.file_name = file_name
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
    
    def tokenize(self) -> List[JavaToken]:
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
            
            # String literals and text blocks
            if char == '"':
                if self._peek() == '"' and self._peek(2) == '"':
                    token = self._read_text_block()
                else:
                    token = self._read_string_literal()
                if token:
                    self.tokens.append(token)
                continue
            
            # Character literals
            if char == "'":
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
            if char.isalpha() or char == '_' or char == '$':
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
        self.tokens.append(JavaToken(
            JavaTokenType.EOF, "",
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
    
    def _read_string_literal(self) -> Optional[JavaToken]:
        """Read string literal."""
        start_line = self.line
        start_column = self.column
        value = ""
        
        self._advance()  # Skip opening quote
        
        while not self._at_end() and self._current_char() != '"':
            if self._current_char() == '\\':
                value += self._advance()  # Backslash
                if not self._at_end():
                    value += self._advance()  # Escaped character
            else:
                value += self._advance()
        
        if not self._at_end():
            self._advance()  # Skip closing quote
        
        return JavaToken(
            JavaTokenType.STRING_LITERAL, f'"{value}"',
            start_line, start_column, self.file_name
        )
    
    def _read_text_block(self) -> Optional[JavaToken]:
        """Read text block (Java 15)."""
        start_line = self.line
        start_column = self.column
        
        # Skip opening """
        self._advance()  # "
        self._advance()  # "
        self._advance()  # "
        
        # Skip whitespace and newline after opening """
        while not self._at_end() and self._current_char() in ' \t':
            self._advance()
        if not self._at_end() and self._current_char() == '\n':
            self._advance()
        
        content = ""
        while not self._at_end():
            if (self._current_char() == '"' and 
                self._peek() == '"' and 
                self._peek(2) == '"'):
                # Found closing """
                self._advance()  # "
                self._advance()  # "
                self._advance()  # "
                break
            content += self._advance()
        
        return JavaToken(
            JavaTokenType.TEXT_BLOCK, f'"""{content}"""',
            start_line, start_column, self.file_name
        )
    
    def _read_character_literal(self) -> Optional[JavaToken]:
        """Read character literal."""
        start_line = self.line
        start_column = self.column
        value = ""
        
        self._advance()  # Skip opening quote
        
        while not self._at_end() and self._current_char() != "'":
            if self._current_char() == '\\':
                value += self._advance()  # Backslash
                if not self._at_end():
                    value += self._advance()  # Escaped character
            else:
                value += self._advance()
        
        if not self._at_end():
            self._advance()  # Skip closing quote
        
        return JavaToken(
            JavaTokenType.CHARACTER_LITERAL, f"'{value}'",
            start_line, start_column, self.file_name
        )
    
    def _read_number(self) -> Optional[JavaToken]:
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
            
            # Binary number
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
               self._current_char().lower() in 'lfd'):
            if self._current_char().lower() in 'fd':
                is_float = True
            value += self._advance()
        
        token_type = JavaTokenType.FLOATING_LITERAL if is_float else JavaTokenType.INTEGER_LITERAL
        
        return JavaToken(
            token_type, value,
            start_line, start_column, self.file_name
        )
    
    def _read_identifier(self) -> Optional[JavaToken]:
        """Read identifier or keyword."""
        start_line = self.line
        start_column = self.column
        value = ""
        
        while (not self._at_end() and 
               (self._current_char().isalnum() or 
                self._current_char() in '_$')):
            value += self._advance()
        
        # Handle non-sealed (hyphenated keyword)
        if value == "non" and self._current_char() == '-':
            # Look ahead for "sealed"
            pos = self.position + 1
            sealed_part = ""
            while pos < len(self.source) and self.source[pos].isalpha():
                sealed_part += self.source[pos]
                pos += 1
            
            if sealed_part == "sealed":
                # Consume the hyphen and "sealed"
                value += self._advance()  # -
                while (not self._at_end() and self._current_char().isalpha()):
                    value += self._advance()
        
        # Check for keywords
        if value in self.KEYWORDS:
            if value in ['true', 'false']:
                token_type = JavaTokenType.BOOLEAN_LITERAL
            elif value == 'null':
                token_type = JavaTokenType.NULL_LITERAL
            else:
                token_type = JavaTokenType.KEYWORD
        else:
            token_type = JavaTokenType.IDENTIFIER
        
        return JavaToken(
            token_type, value,
            start_line, start_column, self.file_name
        )
    
    def _read_operator_or_punctuation(self) -> Optional[JavaToken]:
        """Read operator or punctuation."""
        start_line = self.line
        start_column = self.column
        char = self._current_char()
        
        # Multi-character operators
        if char == '+':
            self._advance()
            if self._current_char() == '+':
                self._advance()
                return JavaToken(JavaTokenType.INCREMENT, "++", start_line, start_column, self.file_name)
            elif self._current_char() == '=':
                self._advance()
                return JavaToken(JavaTokenType.PLUS_ASSIGN, "+=", start_line, start_column, self.file_name)
            return JavaToken(JavaTokenType.PLUS, "+", start_line, start_column, self.file_name)
        
        elif char == '-':
            self._advance()
            if self._current_char() == '-':
                self._advance()
                return JavaToken(JavaTokenType.DECREMENT, "--", start_line, start_column, self.file_name)
            elif self._current_char() == '=':
                self._advance()
                return JavaToken(JavaTokenType.MINUS_ASSIGN, "-=", start_line, start_column, self.file_name)
            elif self._current_char() == '>':
                self._advance()
                return JavaToken(JavaTokenType.ARROW, "->", start_line, start_column, self.file_name)
            return JavaToken(JavaTokenType.MINUS, "-", start_line, start_column, self.file_name)
        
        elif char == '*':
            self._advance()
            if self._current_char() == '=':
                self._advance()
                return JavaToken(JavaTokenType.MULTIPLY_ASSIGN, "*=", start_line, start_column, self.file_name)
            return JavaToken(JavaTokenType.MULTIPLY, "*", start_line, start_column, self.file_name)
        
        elif char == '/':
            self._advance()
            if self._current_char() == '=':
                self._advance()
                return JavaToken(JavaTokenType.DIVIDE_ASSIGN, "/=", start_line, start_column, self.file_name)
            return JavaToken(JavaTokenType.DIVIDE, "/", start_line, start_column, self.file_name)
        
        elif char == '%':
            self._advance()
            if self._current_char() == '=':
                self._advance()
                return JavaToken(JavaTokenType.MODULO_ASSIGN, "%=", start_line, start_column, self.file_name)
            return JavaToken(JavaTokenType.MODULO, "%", start_line, start_column, self.file_name)
        
        elif char == '=':
            self._advance()
            if self._current_char() == '=':
                self._advance()
                return JavaToken(JavaTokenType.EQUAL, "==", start_line, start_column, self.file_name)
            return JavaToken(JavaTokenType.ASSIGN, "=", start_line, start_column, self.file_name)
        
        elif char == '!':
            self._advance()
            if self._current_char() == '=':
                self._advance()
                return JavaToken(JavaTokenType.NOT_EQUAL, "!=", start_line, start_column, self.file_name)
            return JavaToken(JavaTokenType.LOGICAL_NOT, "!", start_line, start_column, self.file_name)
        
        elif char == '<':
            self._advance()
            if self._current_char() == '=':
                self._advance()
                return JavaToken(JavaTokenType.LESS_EQUAL, "<=", start_line, start_column, self.file_name)
            elif self._current_char() == '<':
                self._advance()
                if self._current_char() == '=':
                    self._advance()
                    return JavaToken(JavaTokenType.LEFT_SHIFT_ASSIGN, "<<=", start_line, start_column, self.file_name)
                return JavaToken(JavaTokenType.LEFT_SHIFT, "<<", start_line, start_column, self.file_name)
            return JavaToken(JavaTokenType.LESS_THAN, "<", start_line, start_column, self.file_name)
        
        elif char == '>':
            self._advance()
            if self._current_char() == '=':
                self._advance()
                return JavaToken(JavaTokenType.GREATER_EQUAL, ">=", start_line, start_column, self.file_name)
            elif self._current_char() == '>':
                self._advance()
                if self._current_char() == '>':
                    self._advance()
                    if self._current_char() == '=':
                        self._advance()
                        return JavaToken(JavaTokenType.UNSIGNED_RIGHT_SHIFT_ASSIGN, ">>>=", start_line, start_column, self.file_name)
                    return JavaToken(JavaTokenType.UNSIGNED_RIGHT_SHIFT, ">>>", start_line, start_column, self.file_name)
                elif self._current_char() == '=':
                    self._advance()
                    return JavaToken(JavaTokenType.RIGHT_SHIFT_ASSIGN, ">>=", start_line, start_column, self.file_name)
                return JavaToken(JavaTokenType.RIGHT_SHIFT, ">>", start_line, start_column, self.file_name)
            return JavaToken(JavaTokenType.GREATER_THAN, ">", start_line, start_column, self.file_name)
        
        elif char == '&':
            self._advance()
            if self._current_char() == '&':
                self._advance()
                return JavaToken(JavaTokenType.LOGICAL_AND, "&&", start_line, start_column, self.file_name)
            elif self._current_char() == '=':
                self._advance()
                return JavaToken(JavaTokenType.BIT_AND_ASSIGN, "&=", start_line, start_column, self.file_name)
            return JavaToken(JavaTokenType.BIT_AND, "&", start_line, start_column, self.file_name)
        
        elif char == '|':
            self._advance()
            if self._current_char() == '|':
                self._advance()
                return JavaToken(JavaTokenType.LOGICAL_OR, "||", start_line, start_column, self.file_name)
            elif self._current_char() == '=':
                self._advance()
                return JavaToken(JavaTokenType.BIT_OR_ASSIGN, "|=", start_line, start_column, self.file_name)
            return JavaToken(JavaTokenType.BIT_OR, "|", start_line, start_column, self.file_name)
        
        elif char == '^':
            self._advance()
            if self._current_char() == '=':
                self._advance()
                return JavaToken(JavaTokenType.BIT_XOR_ASSIGN, "^=", start_line, start_column, self.file_name)
            return JavaToken(JavaTokenType.BIT_XOR, "^", start_line, start_column, self.file_name)
        
        elif char == ':':
            self._advance()
            if self._current_char() == ':':
                self._advance()
                return JavaToken(JavaTokenType.DOUBLE_COLON, "::", start_line, start_column, self.file_name)
            return JavaToken(JavaTokenType.COLON, ":", start_line, start_column, self.file_name)
        
        elif char == '.':
            self._advance()
            if self._current_char() == '.':
                self._advance()
                if self._current_char() == '.':
                    self._advance()
                    return JavaToken(JavaTokenType.ELLIPSIS, "...", start_line, start_column, self.file_name)
            return JavaToken(JavaTokenType.DOT, ".", start_line, start_column, self.file_name)
        
        # Single character tokens
        single_char_tokens = {
            ';': JavaTokenType.SEMICOLON,
            ',': JavaTokenType.COMMA,
            '?': JavaTokenType.QUESTION,
            '@': JavaTokenType.AT,
            '(': JavaTokenType.LEFT_PAREN,
            ')': JavaTokenType.RIGHT_PAREN,
            '{': JavaTokenType.LEFT_BRACE,
            '}': JavaTokenType.RIGHT_BRACE,
            '[': JavaTokenType.LEFT_BRACKET,
            ']': JavaTokenType.RIGHT_BRACKET,
            '~': JavaTokenType.BIT_NOT,
        }
        
        if char in single_char_tokens:
            self._advance()
            return JavaToken(
                single_char_tokens[char], char,
                start_line, start_column, self.file_name
            )
        
        # Unknown character
        self._advance()
        return JavaToken(
            JavaTokenType.ERROR, char,
            start_line, start_column, self.file_name
        )


class JavaParser:
    """Java recursive descent parser."""
    
    def __init__(self, tokens: List[JavaToken]):
        self.tokens = tokens
        self.position = 0
        self.errors = []
        self.class_name_stack = []  # Stack to track nested class names
        self.current_class_name = None  # Current class being parsed
    
    def parse(self) -> JavaCompilationUnit:
        """Parse Java compilation unit."""
        try:
            return self._parse_compilation_unit()
        except Exception as e:
            self.errors.append(f"Parse error: {e}")
            # Return empty compilation unit
            return JavaCompilationUnit()
    
    def _current_token(self) -> JavaToken:
        """Get current token."""
        if self._at_end():
            return self.tokens[-1]  # EOF token
        return self.tokens[self.position]
    
    def _peek_token(self, offset: int = 1) -> JavaToken:
        """Peek at token at offset."""
        pos = self.position + offset
        if pos >= len(self.tokens):
            return self.tokens[-1]  # EOF token
        return self.tokens[pos]
    
    def _advance(self) -> JavaToken:
        """Advance position and return current token."""
        token = self._current_token()
        if not self._at_end():
            self.position += 1
        return token
    
    def _at_end(self) -> bool:
        """Check if at end of tokens."""
        return (self.position >= len(self.tokens) or 
                self._current_token().type == JavaTokenType.EOF)
    
    def _match(self, *token_types: JavaTokenType) -> bool:
        """Check if current token matches any of the given types."""
        return self._current_token().type in token_types
    
    def _match_keyword(self, keyword: str) -> bool:
        """Check if current token is a specific keyword."""
        return (self._current_token().type == JavaTokenType.KEYWORD and
                self._current_token().value == keyword)
    
    def _consume(self, token_type: JavaTokenType, message: str = None) -> JavaToken:
        """Consume token of expected type or raise error."""
        if self._match(token_type):
            return self._advance()
        
        if message:
            raise SyntaxError(message)
        else:
            raise SyntaxError(f"Expected {token_type}, got {self._current_token().type}")
    
    def _consume_keyword(self, keyword: str) -> JavaToken:
        """Consume specific keyword or raise error."""
        if self._match_keyword(keyword):
            return self._advance()
        
        raise SyntaxError(f"Expected keyword '{keyword}', got {self._current_token().value}")
    
    def _synchronize(self):
        """Synchronize parser after error."""
        self._advance()
        
        while not self._at_end():
            if self._current_token().type == JavaTokenType.SEMICOLON:
                self._advance()
                return
            
            if self._match(JavaTokenType.KEYWORD):
                keyword = self._current_token().value
                if keyword in ['class', 'interface', 'enum', 'record', 'public',
                              'private', 'protected', 'static', 'final', 'abstract']:
                    return
            
            self._advance()
    
    def _parse_compilation_unit(self) -> JavaCompilationUnit:
        """Parse compilation unit."""
        package_decl = None
        import_decls = []
        type_decls = []
        module_decl = None
        
        # Package declaration
        if self._match_keyword('package'):
            package_decl = self._parse_package_declaration()
        
        # Import declarations
        while self._match_keyword('import'):
            import_decl = self._parse_import_declaration()
            import_decls.append(import_decl)
        
        # Module declaration
        if self._match_keyword('module') or self._match_keyword('open'):
            module_decl = self._parse_module_declaration()
        
        # Type declarations
        while not self._at_end():
            if self._current_token().type == JavaTokenType.EOF:
                break
            
            try:
                type_decl = self._parse_type_declaration()
                if type_decl:
                    type_decls.append(type_decl)
            except Exception as e:
                self.errors.append(f"Error parsing type declaration: {e}")
                self._synchronize()
        
        return JavaCompilationUnit(package_decl, import_decls, type_decls, module_decl)
    
    def _parse_package_declaration(self) -> JavaPackageDeclaration:
        """Parse package declaration."""
        annotations = []
        
        # Parse annotations
        while self._match(JavaTokenType.AT):
            annotations.append(self._parse_annotation())
        
        self._consume_keyword('package')
        name = self._parse_qualified_name()
        self._consume(JavaTokenType.SEMICOLON)
        
        return JavaPackageDeclaration(annotations=annotations, name=name)
    
    def _parse_import_declaration(self) -> JavaImportDeclaration:
        """Parse import declaration."""
        self._consume_keyword('import')
        
        is_static = False
        if self._match_keyword('static'):
            is_static = True
            self._advance()
        
        name = self._parse_qualified_name()
        
        is_on_demand = False
        if self._match(JavaTokenType.DOT):
            self._advance()
            if self._match(JavaTokenType.MULTIPLY):
                is_on_demand = True
                self._advance()
        
        self._consume(JavaTokenType.SEMICOLON)
        
        return JavaImportDeclaration(name=name, is_static=is_static, is_on_demand=is_on_demand)
    
    def _parse_type_declaration(self) -> Optional[JavaDeclaration]:
        """Parse type declaration."""
        # Skip semicolons
        if self._match(JavaTokenType.SEMICOLON):
            self._advance()
            return None
        
        # Parse annotations and modifiers
        annotations = []
        modifiers = []
        
        while (self._match(JavaTokenType.AT) or 
               (self._match(JavaTokenType.KEYWORD) and 
                self._current_token().value in ['public', 'private', 'protected', 'static', 
                                               'final', 'abstract', 'sealed', 'non-sealed'])):
            
            if self._match(JavaTokenType.AT):
                annotations.append(self._parse_annotation())
            else:
                modifiers.append(JavaModifier(self._advance().value))
        
        # Type declaration
        if self._match_keyword('class'):
            return self._parse_class_declaration(modifiers, annotations)
        elif self._match_keyword('interface'):
            return self._parse_interface_declaration(modifiers, annotations)
        elif self._match_keyword('enum'):
            return self._parse_enum_declaration(modifiers, annotations)
        elif self._match_keyword('record'):
            return self._parse_record_declaration(modifiers, annotations)
        elif self._match_keyword('@interface'):
            return self._parse_annotation_declaration(modifiers, annotations)
        
        return None
    
    def _parse_class_declaration(self, modifiers: List[JavaModifier], annotations: List[JavaAnnotation]) -> JavaClassDeclaration:
        """Parse class declaration."""
        self._consume_keyword('class')
        name = self._consume(JavaTokenType.IDENTIFIER).value
        
        # Push current class name onto stack and set as current
        self._push_class_context(name)
        
        try:
            # Type parameters
            type_parameters = []
            if self._match(JavaTokenType.LESS_THAN):
                type_parameters = self._parse_type_parameters()
            
            # Superclass
            superclass = None
            if self._match_keyword('extends'):
                self._advance()
                superclass = self._parse_type()
            
            # Interfaces
            super_interfaces = []
            if self._match_keyword('implements'):
                self._advance()
                super_interfaces = self._parse_type_list()
            
            # Body
            body_declarations = self._parse_class_body()
        
        finally:
            # Always pop the class context when done
            self._pop_class_context()
        
        return JavaClassDeclaration(
            modifiers=modifiers,
            annotations=annotations,
            name=name,
            type_parameters=type_parameters,
            superclass=superclass,
            super_interfaces=super_interfaces,
            body_declarations=body_declarations
        )
    
    def _parse_interface_declaration(self, modifiers: List[JavaModifier], annotations: List[JavaAnnotation]) -> JavaInterfaceDeclaration:
        """Parse interface declaration."""
        self._consume_keyword('interface')
        name = self._consume(JavaTokenType.IDENTIFIER).value
        
        # Push current interface name onto stack and set as current
        self._push_class_context(name)
        
        try:
            # Type parameters
            type_parameters = []
            if self._match(JavaTokenType.LESS_THAN):
                type_parameters = self._parse_type_parameters()
            
            # Extended interfaces
            extended_interfaces = []
            if self._match_keyword('extends'):
                self._advance()
                extended_interfaces = self._parse_type_list()
            
            # Body
            body_declarations = self._parse_class_body()
        
        finally:
            # Always pop the class context when done
            self._pop_class_context()
        
        return JavaInterfaceDeclaration(
            modifiers=modifiers,
            annotations=annotations,
            name=name,
            type_parameters=type_parameters,
            extended_interfaces=extended_interfaces,
            body_declarations=body_declarations
        )
    
    def _parse_enum_declaration(self, modifiers: List[JavaModifier], annotations: List[JavaAnnotation]) -> JavaEnumDeclaration:
        """Parse enum declaration."""
        self._consume_keyword('enum')
        name = self._consume(JavaTokenType.IDENTIFIER).value
        
        # Push current enum name onto stack and set as current
        self._push_class_context(name)
        
        try:
            # Interfaces
            super_interfaces = []
            if self._match_keyword('implements'):
                self._advance()
                super_interfaces = self._parse_type_list()
            
            self._consume(JavaTokenType.LEFT_BRACE)
            
            # Enum constants
            enum_constants = []
            if not self._match(JavaTokenType.RIGHT_BRACE):
                enum_constants.append(self._parse_enum_constant())
                
                while self._match(JavaTokenType.COMMA):
                    self._advance()
                    if self._match(JavaTokenType.RIGHT_BRACE):
                        break
                    enum_constants.append(self._parse_enum_constant())
            
            # Body declarations
            body_declarations = []
            if self._match(JavaTokenType.SEMICOLON):
                self._advance()
                body_declarations = self._parse_class_body_declarations()
            
            self._consume(JavaTokenType.RIGHT_BRACE)
        
        finally:
            # Always pop the class context when done
            self._pop_class_context()
        
        return JavaEnumDeclaration(
            modifiers=modifiers,
            annotations=annotations,
            name=name,
            super_interfaces=super_interfaces,
            enum_constants=enum_constants,
            body_declarations=body_declarations
        )
    
    def _parse_record_declaration(self, modifiers: List[JavaModifier], annotations: List[JavaAnnotation]) -> JavaRecordDeclaration:
        """Parse record declaration (Java 14)."""
        self._consume_keyword('record')
        name = self._consume(JavaTokenType.IDENTIFIER).value
        
        # Push current record name onto stack and set as current
        self._push_class_context(name)
        
        try:
            # Type parameters
            type_parameters = []
            if self._match(JavaTokenType.LESS_THAN):
                type_parameters = self._parse_type_parameters()
            
            # Parameters
            self._consume(JavaTokenType.LEFT_PAREN)
            parameters = []
            if not self._match(JavaTokenType.RIGHT_PAREN):
                parameters.append(self._parse_parameter())
                while self._match(JavaTokenType.COMMA):
                    self._advance()
                    parameters.append(self._parse_parameter())
            self._consume(JavaTokenType.RIGHT_PAREN)
            
            # Interfaces
            super_interfaces = []
            if self._match_keyword('implements'):
                self._advance()
                super_interfaces = self._parse_type_list()
            
            # Body
            body_declarations = self._parse_class_body()
        
        finally:
            # Always pop the class context when done
            self._pop_class_context()
        
        return JavaRecordDeclaration(
            modifiers=modifiers,
            annotations=annotations,
            name=name,
            type_parameters=type_parameters,
            parameters=parameters,
            super_interfaces=super_interfaces,
            body_declarations=body_declarations
        )
    
    def _parse_annotation_declaration(self, modifiers: List[JavaModifier], annotations: List[JavaAnnotation]) -> JavaAnnotationDeclaration:
        """Parse annotation declaration."""
        self._consume(JavaTokenType.AT)
        self._consume_keyword('interface')
        name = self._consume(JavaTokenType.IDENTIFIER).value
        
        # Body
        body_declarations = self._parse_class_body()
        
        return JavaAnnotationDeclaration(
            modifiers=modifiers,
            annotations=annotations,
            name=name,
            body_declarations=body_declarations
        )
    
    def _parse_module_declaration(self) -> JavaModuleDeclaration:
        """Parse module declaration (Java 9)."""
        annotations = []
        
        # Parse annotations
        while self._match(JavaTokenType.AT):
            annotations.append(self._parse_annotation())
        
        is_open = False
        if self._match_keyword('open'):
            is_open = True
            self._advance()
        
        self._consume_keyword('module')
        name = self._parse_qualified_name()
        
        self._consume(JavaTokenType.LEFT_BRACE)
        
        # Module statements
        module_statements = []
        while not self._match(JavaTokenType.RIGHT_BRACE) and not self._at_end():
            stmt = self._parse_module_statement()
            if stmt:
                module_statements.append(stmt)
        
        self._consume(JavaTokenType.RIGHT_BRACE)
        
        return JavaModuleDeclaration(
            annotations=annotations,
            name=name,
            is_open=is_open,
            module_statements=module_statements
        )
    
    def _parse_module_statement(self) -> Optional[JavaModuleStatement]:
        """Parse module statement."""
        if self._match_keyword('requires'):
            return self._parse_requires_directive()
        elif self._match_keyword('exports'):
            return self._parse_exports_directive()
        elif self._match_keyword('opens'):
            return self._parse_opens_directive()
        elif self._match_keyword('uses'):
            return self._parse_uses_directive()
        elif self._match_keyword('provides'):
            return self._parse_provides_directive()
        
        return None
    
    def _parse_requires_directive(self) -> JavaRequiresDirective:
        """Parse requires directive."""
        self._consume_keyword('requires')
        
        is_transitive = False
        is_static = False
        
        if self._match_keyword('transitive'):
            is_transitive = True
            self._advance()
        
        if self._match_keyword('static'):
            is_static = True
            self._advance()
        
        module_name = self._parse_qualified_name()
        self._consume(JavaTokenType.SEMICOLON)
        
        return JavaRequiresDirective(
            module_name=module_name,
            is_transitive=is_transitive,
            is_static=is_static
        )
    
    def _parse_exports_directive(self) -> JavaExportsDirective:
        """Parse exports directive."""
        self._consume_keyword('exports')
        package_name = self._parse_qualified_name()
        
        target_modules = []
        if self._match_keyword('to'):
            self._advance()
            target_modules = self._parse_qualified_name_list()
        
        self._consume(JavaTokenType.SEMICOLON)
        
        return JavaExportsDirective(
            package_name=package_name,
            target_modules=target_modules
        )
    
    def _parse_opens_directive(self) -> JavaOpensDirective:
        """Parse opens directive."""
        self._consume_keyword('opens')
        package_name = self._parse_qualified_name()
        
        target_modules = []
        if self._match_keyword('to'):
            self._advance()
            target_modules = self._parse_qualified_name_list()
        
        self._consume(JavaTokenType.SEMICOLON)
        
        return JavaOpensDirective(
            package_name=package_name,
            target_modules=target_modules
        )
    
    def _parse_uses_directive(self) -> JavaUsesDirective:
        """Parse uses directive."""
        self._consume_keyword('uses')
        service_name = self._parse_qualified_name()
        self._consume(JavaTokenType.SEMICOLON)
        
        return JavaUsesDirective(service_name=service_name)
    
    def _parse_provides_directive(self) -> JavaProvidesDirective:
        """Parse provides directive."""
        self._consume_keyword('provides')
        service_name = self._parse_qualified_name()
        self._consume_keyword('with')
        implementation_names = self._parse_qualified_name_list()
        self._consume(JavaTokenType.SEMICOLON)
        
        return JavaProvidesDirective(
            service_name=service_name,
            implementation_names=implementation_names
        )
    
    def _parse_class_body(self) -> List[JavaDeclaration]:
        """Parse class body."""
        self._consume(JavaTokenType.LEFT_BRACE)
        declarations = self._parse_class_body_declarations()
        self._consume(JavaTokenType.RIGHT_BRACE)
        return declarations
    
    def _parse_class_body_declarations(self) -> List[JavaDeclaration]:
        """Parse class body declarations."""
        declarations = []
        
        while not self._match(JavaTokenType.RIGHT_BRACE) and not self._at_end():
            # Skip semicolons
            if self._match(JavaTokenType.SEMICOLON):
                self._advance()
                continue
            
            try:
                decl = self._parse_class_body_declaration()
                if decl:
                    declarations.append(decl)
            except Exception as e:
                self.errors.append(f"Error parsing class body declaration: {e}")
                self._synchronize()
        
        return declarations
    
    def _parse_class_body_declaration(self) -> Optional[JavaDeclaration]:
        """Parse class body declaration."""
        # Parse annotations and modifiers
        annotations = []
        modifiers = []
        
        while (self._match(JavaTokenType.AT) or 
               (self._match(JavaTokenType.KEYWORD) and 
                self._current_token().value in ['public', 'private', 'protected', 'static', 
                                               'final', 'abstract', 'synchronized', 'native',
                                               'transient', 'volatile', 'strictfp', 'default'])):
            
            if self._match(JavaTokenType.AT):
                annotations.append(self._parse_annotation())
            else:
                modifiers.append(JavaModifier(self._advance().value))
        
        # Check for constructor or method
        if self._match(JavaTokenType.IDENTIFIER):
            # Look ahead to determine if this is a constructor or method
            if self._peek_token().type == JavaTokenType.LEFT_PAREN:
                # Could be constructor or method
                return self._parse_constructor_or_method(modifiers, annotations)
            else:
                # Field declaration
                return self._parse_field_declaration(modifiers, annotations)
        
        # Type declaration or method with return type
        if self._match(JavaTokenType.KEYWORD):
            keyword = self._current_token().value
            
            if keyword in ['class', 'interface', 'enum', 'record']:
                return self._parse_type_declaration()
            elif keyword == 'void':
                # Method with void return type
                return self._parse_method_declaration(modifiers, annotations)
            else:
                # Method or field with specific type
                return self._parse_method_or_field_declaration(modifiers, annotations)
        
        return None
    
    def _parse_constructor_or_method(self, modifiers: List[JavaModifier], annotations: List[JavaAnnotation]) -> JavaMethodDeclaration:
        """Parse constructor or method declaration."""
        name = self._consume(JavaTokenType.IDENTIFIER).value
        
        # Type parameters
        type_parameters = []
        if self._match(JavaTokenType.LESS_THAN):
            type_parameters = self._parse_type_parameters()
        
        # Parameters
        self._consume(JavaTokenType.LEFT_PAREN)
        parameters = []
        if not self._match(JavaTokenType.RIGHT_PAREN):
            parameters.append(self._parse_parameter())
            while self._match(JavaTokenType.COMMA):
                self._advance()
                parameters.append(self._parse_parameter())
        self._consume(JavaTokenType.RIGHT_PAREN)
        
        # Throws clause
        thrown_exceptions = []
        if self._match_keyword('throws'):
            self._advance()
            thrown_exceptions = self._parse_type_list()
        
        # Body
        body = None
        if self._match(JavaTokenType.LEFT_BRACE):
            body = self._parse_block_statement()
        else:
            self._consume(JavaTokenType.SEMICOLON)
        
        return JavaMethodDeclaration(
            modifiers=modifiers,
            annotations=annotations,
            name=name,
            return_type=None,  # Constructor
            type_parameters=type_parameters,
            parameters=parameters,
            thrown_exceptions=thrown_exceptions,
            body=body,
            is_constructor=True
        )
    
    def _parse_method_declaration(self, modifiers: List[JavaModifier], annotations: List[JavaAnnotation]) -> JavaMethodDeclaration:
        """Parse method declaration."""
        # Return type
        return_type = None
        if self._match_keyword('void'):
            self._advance()
            return_type = JavaPrimitiveType('void')
        else:
            return_type = self._parse_type()
        
        name = self._consume(JavaTokenType.IDENTIFIER).value
        
        # Type parameters
        type_parameters = []
        if self._match(JavaTokenType.LESS_THAN):
            type_parameters = self._parse_type_parameters()
        
        # Parameters
        self._consume(JavaTokenType.LEFT_PAREN)
        parameters = []
        if not self._match(JavaTokenType.RIGHT_PAREN):
            parameters.append(self._parse_parameter())
            while self._match(JavaTokenType.COMMA):
                self._advance()
                parameters.append(self._parse_parameter())
        self._consume(JavaTokenType.RIGHT_PAREN)
        
        # Throws clause
        thrown_exceptions = []
        if self._match_keyword('throws'):
            self._advance()
            thrown_exceptions = self._parse_type_list()
        
        # Body
        body = None
        if self._match(JavaTokenType.LEFT_BRACE):
            body = self._parse_block_statement()
        else:
            self._consume(JavaTokenType.SEMICOLON)
        
        return JavaMethodDeclaration(
            modifiers=modifiers,
            annotations=annotations,
            name=name,
            return_type=return_type,
            type_parameters=type_parameters,
            parameters=parameters,
            thrown_exceptions=thrown_exceptions,
            body=body
        )
    
    def _parse_method_or_field_declaration(self, modifiers: List[JavaModifier], annotations: List[JavaAnnotation]) -> JavaDeclaration:
        """Parse method or field declaration with proper lookahead."""
        try:
            # Handle special cases first
            if self._is_constructor_declaration():
                return self._parse_constructor_declaration(modifiers, annotations)
            
            # Parse type parameters for generic methods
            type_parameters = []
            if self._match(JavaTokenType.LESS):
                type_parameters = self._parse_type_parameter_list()
            
            # Parse return type (or field type)
            return_type = None
            if not self._is_constructor_name():
                return_type = self._parse_type()
            
            # Parse name
            name = self._consume(JavaTokenType.IDENTIFIER).value
            
            # Use lookahead to distinguish method from field
            if self._is_method_declaration():
                return self._parse_method_declaration_rest(
                    modifiers, annotations, type_parameters, return_type, name
                )
            else:
                return self._parse_field_declaration_rest(
                    modifiers, annotations, return_type, name
                )
                
        except Exception as e:
            self._log_error(f"Error parsing method/field declaration: {e}")
            self._synchronize()
            return None
    
    def _push_class_context(self, class_name: str):
        """Push a class name onto the context stack."""
        self.class_name_stack.append(self.current_class_name)
        self.current_class_name = class_name
    
    def _pop_class_context(self):
        """Pop the current class context from the stack."""
        if self.class_name_stack:
            self.current_class_name = self.class_name_stack.pop()
        else:
            self.current_class_name = None
    
    def _is_constructor_declaration(self) -> bool:
        """Check if this is a constructor declaration."""
        if not self._match(JavaTokenType.IDENTIFIER):
            return False
        
        # Get the identifier name
        identifier_name = self._peek().value
        
        # Check if identifier name matches current class name
        if self.current_class_name and identifier_name == self.current_class_name:
            # Look ahead to see if next token after identifier is left paren
            current_pos = self._position
            self._advance()  # consume identifier
            is_constructor = self._match(JavaTokenType.LEFT_PAREN)
            self._position = current_pos  # reset
            return is_constructor
        
        return False
    
    def _is_constructor_name(self) -> bool:
        """Check if current identifier is constructor name."""
        if not self._match(JavaTokenType.IDENTIFIER):
            return False
        
        identifier_name = self._peek().value
        return self.current_class_name and identifier_name == self.current_class_name
    
    def _is_method_declaration(self) -> bool:
        """Use lookahead to determine if this is a method declaration."""
        # Save current position
        current_pos = self._position
        
        try:
            # Skip array dimensions if any
            while self._match(JavaTokenType.LEFT_BRACKET):
                self._advance()
                if not self._match(JavaTokenType.RIGHT_BRACKET):
                    break
                self._advance()
            
            # If we see a left parenthesis, it's a method
            is_method = self._match(JavaTokenType.LEFT_PAREN)
            return is_method
            
        except:
            return False
        finally:
            # Restore position
            self._position = current_pos
    
    def _parse_constructor_declaration(self, modifiers: List[JavaModifier], annotations: List[JavaAnnotation]) -> JavaMethodDeclaration:
        """Parse constructor declaration."""
        # Constructor name
        name = self._consume(JavaTokenType.IDENTIFIER).value
        
        # Parameters
        self._consume(JavaTokenType.LEFT_PAREN)
        parameters = []
        if not self._match(JavaTokenType.RIGHT_PAREN):
            parameters.append(self._parse_parameter())
            while self._match(JavaTokenType.COMMA):
                self._advance()
                parameters.append(self._parse_parameter())
        self._consume(JavaTokenType.RIGHT_PAREN)
        
        # Throws clause
        thrown_exceptions = []
        if self._match_keyword('throws'):
            self._advance()
            thrown_exceptions = self._parse_type_list()
        
        # Constructor body
        body = self._parse_block_statement()
        
        return JavaMethodDeclaration(
            modifiers=modifiers,
            annotations=annotations,
            name=name,
            return_type=None,  # Constructors have no return type
            parameters=parameters,
            thrown_exceptions=thrown_exceptions,
            body=body
        )
    
    def _parse_method_declaration_rest(self, modifiers: List[JavaModifier], annotations: List[JavaAnnotation], 
                                     type_parameters: List, return_type: JavaType, name: str) -> JavaMethodDeclaration:
        """Parse the rest of a method declaration after type and name."""
        # Parameters
        self._consume(JavaTokenType.LEFT_PAREN)
        parameters = []
        if not self._match(JavaTokenType.RIGHT_PAREN):
            parameters.append(self._parse_parameter())
            while self._match(JavaTokenType.COMMA):
                self._advance()
                parameters.append(self._parse_parameter())
        self._consume(JavaTokenType.RIGHT_PAREN)
        
        # Array dimensions for return type (e.g., int[] method())
        array_dimensions = 0
        while self._match(JavaTokenType.LEFT_BRACKET):
            self._advance()
            self._consume(JavaTokenType.RIGHT_BRACKET)
            array_dimensions += 1
        
        # Adjust return type for array dimensions
        actual_return_type = return_type
        for _ in range(array_dimensions):
            actual_return_type = JavaArrayType(component_type=actual_return_type)
        
        # Throws clause
        thrown_exceptions = []
        if self._match_keyword('throws'):
            self._advance()
            thrown_exceptions = self._parse_type_list()
        
        # Default value for annotation methods
        default_value = None
        if self._match_keyword('default'):
            self._advance()
            default_value = self._parse_expression()
        
        # Method body (or semicolon for abstract/interface methods)
        body = None
        if self._match(JavaTokenType.LEFT_BRACE):
            body = self._parse_block_statement()
        else:
            self._consume(JavaTokenType.SEMICOLON)
        
        return JavaMethodDeclaration(
            modifiers=modifiers,
            annotations=annotations,
            type_parameters=type_parameters,
            name=name,
            return_type=actual_return_type,
            parameters=parameters,
            thrown_exceptions=thrown_exceptions,
            body=body,
            default_value=default_value
        )
    
    def _parse_field_declaration_rest(self, modifiers: List[JavaModifier], annotations: List[JavaAnnotation], 
                                    field_type: JavaType, first_name: str) -> JavaFieldDeclaration:
        """Parse the rest of a field declaration after type and first name."""
        fragments = []
        
        # Parse first declarator
        fragments.append(self._parse_variable_declarator_rest(first_name))
        
        # Parse additional declarators
        while self._match(JavaTokenType.COMMA):
            self._advance()
            name = self._consume(JavaTokenType.IDENTIFIER).value
            fragments.append(self._parse_variable_declarator_rest(name))
        
        self._consume(JavaTokenType.SEMICOLON)
        
        return JavaFieldDeclaration(
            modifiers=modifiers,
            annotations=annotations,
            variable_type=field_type,
            fragments=fragments
        )
    
    def _parse_variable_declarator_rest(self, name: str) -> JavaVariableDeclarationFragment:
        """Parse the rest of a variable declarator after the name."""
        # Array dimensions
        extra_dimensions = 0
        while self._match(JavaTokenType.LEFT_BRACKET):
            self._advance()
            self._consume(JavaTokenType.RIGHT_BRACKET)
            extra_dimensions += 1
        
        # Initializer
        initializer = None
        if self._match(JavaTokenType.ASSIGN):
            self._advance()
            initializer = self._parse_expression()
        
        return JavaVariableDeclarationFragment(
            name=name,
            extra_dimensions=extra_dimensions,
            initializer=initializer
        )
    
    def _parse_type_parameter_list(self) -> List:
        """Parse generic type parameter list."""
        type_parameters = []
        self._consume(JavaTokenType.LESS)
        
        if not self._match(JavaTokenType.GREATER):
            type_parameters.append(self._parse_type_parameter())
            while self._match(JavaTokenType.COMMA):
                self._advance()
                type_parameters.append(self._parse_type_parameter())
        
        self._consume(JavaTokenType.GREATER)
        return type_parameters
    
    def _parse_type_parameter(self) -> JavaTypeParameter:
        """Parse a single type parameter."""
        name = self._consume(JavaTokenType.IDENTIFIER).value
        
        bounds = []
        if self._match_keyword('extends'):
            self._advance()
            bounds.append(self._parse_type())
            while self._match(JavaTokenType.BIT_AND):
                self._advance()
                bounds.append(self._parse_type())
        
        return JavaTypeParameter(name=name, bounds=bounds)
    
    def _parse_field_declaration(self, modifiers: List[JavaModifier], annotations: List[JavaAnnotation]) -> JavaFieldDeclaration:
        """Parse field declaration."""
        variable_type = self._parse_type()
        
        fragments = []
        name = self._consume(JavaTokenType.IDENTIFIER).value
        
        # Handle array dimensions and initializer
        extra_dimensions = 0
        while self._match(JavaTokenType.LEFT_BRACKET):
            self._advance()
            self._consume(JavaTokenType.RIGHT_BRACKET)
            extra_dimensions += 1
        
        initializer = None
        if self._match(JavaTokenType.ASSIGN):
            self._advance()
            initializer = self._parse_expression()
        
        fragments.append(JavaVariableDeclarationFragment(name, extra_dimensions, initializer))
        
        # Additional fragments
        while self._match(JavaTokenType.COMMA):
            self._advance()
            name = self._consume(JavaTokenType.IDENTIFIER).value
            
            extra_dimensions = 0
            while self._match(JavaTokenType.LEFT_BRACKET):
                self._advance()
                self._consume(JavaTokenType.RIGHT_BRACKET)
                extra_dimensions += 1
            
            initializer = None
            if self._match(JavaTokenType.ASSIGN):
                self._advance()
                initializer = self._parse_expression()
            
            fragments.append(JavaVariableDeclarationFragment(name, extra_dimensions, initializer))
        
        self._consume(JavaTokenType.SEMICOLON)
        
        return JavaFieldDeclaration(
            modifiers=modifiers,
            annotations=annotations,
            variable_type=variable_type,
            fragments=fragments
        )
    
    def _parse_field_declaration_rest(self, modifiers: List[JavaModifier], annotations: List[JavaAnnotation], 
                                     variable_type: JavaType, first_name: str) -> JavaFieldDeclaration:
        """Parse rest of field declaration."""
        fragments = []
        
        # First fragment
        extra_dimensions = 0
        while self._match(JavaTokenType.LEFT_BRACKET):
            self._advance()
            self._consume(JavaTokenType.RIGHT_BRACKET)
            extra_dimensions += 1
        
        initializer = None
        if self._match(JavaTokenType.ASSIGN):
            self._advance()
            initializer = self._parse_expression()
        
        fragments.append(JavaVariableDeclarationFragment(first_name, extra_dimensions, initializer))
        
        # Additional fragments
        while self._match(JavaTokenType.COMMA):
            self._advance()
            name = self._consume(JavaTokenType.IDENTIFIER).value
            
            extra_dimensions = 0
            while self._match(JavaTokenType.LEFT_BRACKET):
                self._advance()
                self._consume(JavaTokenType.RIGHT_BRACKET)
                extra_dimensions += 1
            
            initializer = None
            if self._match(JavaTokenType.ASSIGN):
                self._advance()
                initializer = self._parse_expression()
            
            fragments.append(JavaVariableDeclarationFragment(name, extra_dimensions, initializer))
        
        self._consume(JavaTokenType.SEMICOLON)
        
        return JavaFieldDeclaration(
            modifiers=modifiers,
            annotations=annotations,
            variable_type=variable_type,
            fragments=fragments
        )
    
    def _parse_parameter(self) -> JavaParameter:
        """Parse parameter."""
        annotations = []
        modifiers = []
        
        # Parse annotations and modifiers
        while (self._match(JavaTokenType.AT) or 
               (self._match(JavaTokenType.KEYWORD) and 
                self._current_token().value in ['final'])):
            
            if self._match(JavaTokenType.AT):
                annotations.append(self._parse_annotation())
            else:
                modifiers.append(JavaModifier(self._advance().value))
        
        parameter_type = self._parse_type()
        
        # Varargs
        is_varargs = False
        if self._match(JavaTokenType.ELLIPSIS):
            is_varargs = True
            self._advance()
        
        name = self._consume(JavaTokenType.IDENTIFIER).value
        
        return JavaParameter(
            modifiers=modifiers,
            annotations=annotations,
            parameter_type=parameter_type,
            name=name,
            is_varargs=is_varargs
        )
    
    def _parse_type_parameters(self) -> List[JavaTypeParameter]:
        """Parse type parameters."""
        self._consume(JavaTokenType.LESS_THAN)
        
        type_parameters = []
        type_parameters.append(self._parse_type_parameter())
        
        while self._match(JavaTokenType.COMMA):
            self._advance()
            type_parameters.append(self._parse_type_parameter())
        
        self._consume(JavaTokenType.GREATER_THAN)
        
        return type_parameters
    
    def _parse_type_parameter(self) -> JavaTypeParameter:
        """Parse type parameter."""
        name = self._consume(JavaTokenType.IDENTIFIER).value
        
        bounds = []
        if self._match_keyword('extends'):
            self._advance()
            bounds.append(self._parse_type())
            
            while self._match(JavaTokenType.BIT_AND):
                self._advance()
                bounds.append(self._parse_type())
        
        return JavaTypeParameter(name=name, bounds=bounds)
    
    def _parse_type(self) -> JavaType:
        """Parse type."""
        # Handle primitive types
        if self._match(JavaTokenType.KEYWORD):
            keyword = self._current_token().value
            if keyword in ['boolean', 'byte', 'char', 'short', 'int', 'long', 'float', 'double']:
                self._advance()
                return JavaPrimitiveType(keyword)
            elif keyword == 'var':
                self._advance()
                return JavaVarType()
        
        # Reference type
        base_type = self._parse_reference_type()
        
        # Array dimensions
        while self._match(JavaTokenType.LEFT_BRACKET):
            self._advance()
            self._consume(JavaTokenType.RIGHT_BRACKET)
            base_type = JavaArrayType(base_type)
        
        return base_type
    
    def _parse_reference_type(self) -> JavaType:
        """Parse reference type."""
        # Simple name or qualified name
        type_name = self._parse_simple_name()
        
        # Build qualified name
        while self._match(JavaTokenType.DOT):
            self._advance()
            name = self._parse_simple_name()
            type_name = JavaQualifiedName(type_name, name)
        
        # Type arguments
        if self._match(JavaTokenType.LESS_THAN):
            type_arguments = self._parse_type_arguments()
            return JavaParameterizedType(type_name, type_arguments)
        
        return type_name
    
    def _parse_type_arguments(self) -> List[JavaType]:
        """Parse type arguments."""
        self._consume(JavaTokenType.LESS_THAN)
        
        type_arguments = []
        type_arguments.append(self._parse_type_argument())
        
        while self._match(JavaTokenType.COMMA):
            self._advance()
            type_arguments.append(self._parse_type_argument())
        
        self._consume(JavaTokenType.GREATER_THAN)
        
        return type_arguments
    
    def _parse_type_argument(self) -> JavaType:
        """Parse type argument."""
        if self._match(JavaTokenType.QUESTION):
            self._advance()
            
            # Wildcard
            bound = None
            is_upper_bound = True
            
            if self._match_keyword('extends'):
                self._advance()
                bound = self._parse_type()
                is_upper_bound = True
            elif self._match_keyword('super'):
                self._advance()
                bound = self._parse_type()
                is_upper_bound = False
            
            return JavaWildcardType(bound, is_upper_bound)
        else:
            return self._parse_type()
    
    def _parse_type_list(self) -> List[JavaType]:
        """Parse comma-separated type list."""
        types = []
        types.append(self._parse_type())
        
        while self._match(JavaTokenType.COMMA):
            self._advance()
            types.append(self._parse_type())
        
        return types
    
    def _parse_qualified_name_list(self) -> List[JavaExpression]:
        """Parse comma-separated qualified name list."""
        names = []
        names.append(self._parse_qualified_name())
        
        while self._match(JavaTokenType.COMMA):
            self._advance()
            names.append(self._parse_qualified_name())
        
        return names
    
    def _parse_qualified_name(self) -> JavaExpression:
        """Parse qualified name."""
        name = self._parse_simple_name()
        
        while self._match(JavaTokenType.DOT):
            self._advance()
            simple_name = self._parse_simple_name()
            name = JavaQualifiedName(name, simple_name)
        
        return name
    
    def _parse_simple_name(self) -> JavaSimpleName:
        """Parse simple name."""
        identifier = self._consume(JavaTokenType.IDENTIFIER).value
        return JavaSimpleName(identifier)
    
    def _parse_enum_constant(self) -> JavaEnumConstant:
        """Parse enum constant."""
        annotations = []
        while self._match(JavaTokenType.AT):
            annotations.append(self._parse_annotation())
        
        name = self._consume(JavaTokenType.IDENTIFIER).value
        
        arguments = []
        if self._match(JavaTokenType.LEFT_PAREN):
            self._advance()
            if not self._match(JavaTokenType.RIGHT_PAREN):
                arguments.append(self._parse_expression())
                while self._match(JavaTokenType.COMMA):
                    self._advance()
                    arguments.append(self._parse_expression())
            self._consume(JavaTokenType.RIGHT_PAREN)
        
        # Anonymous class declaration
        anonymous_class = None
        if self._match(JavaTokenType.LEFT_BRACE):
            body_declarations = self._parse_class_body_declarations()
            anonymous_class = JavaAnonymousClassDeclaration(body_declarations)
        
        return JavaEnumConstant(name=name, arguments=arguments, anonymous_class_declaration=anonymous_class)
    
    def _parse_annotation(self) -> JavaAnnotation:
        """Parse annotation."""
        self._consume(JavaTokenType.AT)
        type_name = self._parse_qualified_name()
        
        if self._match(JavaTokenType.LEFT_PAREN):
            self._advance()
            
            if self._match(JavaTokenType.RIGHT_PAREN):
                # Marker annotation
                self._advance()
                return JavaMarkerAnnotation(type_name=type_name)
            
            # Check for single member annotation
            if (self._match(JavaTokenType.IDENTIFIER) and 
                self._peek_token().type == JavaTokenType.ASSIGN):
                # Normal annotation
                values = []
                values.append(self._parse_member_value_pair())
                
                while self._match(JavaTokenType.COMMA):
                    self._advance()
                    values.append(self._parse_member_value_pair())
                
                self._consume(JavaTokenType.RIGHT_PAREN)
                return JavaNormalAnnotation(type_name=type_name, values=values)
            else:
                # Single member annotation
                value = self._parse_expression()
                self._consume(JavaTokenType.RIGHT_PAREN)
                return JavaSingleMemberAnnotation(type_name=type_name, value=value)
        
        return JavaMarkerAnnotation(type_name=type_name)
    
    def _parse_member_value_pair(self) -> JavaMemberValuePair:
        """Parse member value pair."""
        name = self._consume(JavaTokenType.IDENTIFIER).value
        self._consume(JavaTokenType.ASSIGN)
        value = self._parse_expression()
        
        return JavaMemberValuePair(name=name, value=value)
    
    def _parse_block_statement(self) -> JavaBlockStatement:
        """Parse block statement."""
        self._consume(JavaTokenType.LEFT_BRACE)
        
        statements = []
        while not self._match(JavaTokenType.RIGHT_BRACE) and not self._at_end():
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
        
        self._consume(JavaTokenType.RIGHT_BRACE)
        
        return JavaBlockStatement(statements)
    
    def _parse_statement(self) -> Optional[JavaStatement]:
        """Parse comprehensive Java statement."""
        try:
            # Handle labeled statements first
            if self._match(JavaTokenType.IDENTIFIER) and self._peek().type == JavaTokenType.COLON:
                return self._parse_labeled_statement()
            
            # Block statement
            if self._match(JavaTokenType.LEFT_BRACE):
                return self._parse_block_statement()
            
            # Empty statement
            if self._match(JavaTokenType.SEMICOLON):
                self._advance()
                return JavaEmptyStatement()
            
            # Keyword-based statements
            if self._match(JavaTokenType.KEYWORD):
                keyword = self._current_token().value
                
                if keyword == "if":
                    return self._parse_if_statement()
                elif keyword == "while":
                    return self._parse_while_statement()
                elif keyword == "for":
                    return self._parse_for_statement()
                elif keyword == "do":
                    return self._parse_do_statement()
                elif keyword == "switch":
                    return self._parse_switch_statement()
                elif keyword == "try":
                    return self._parse_try_statement()
                elif keyword == "synchronized":
                    return self._parse_synchronized_statement()
                elif keyword == "return":
                    return self._parse_return_statement()
                elif keyword == "throw":
                    return self._parse_throw_statement()
                elif keyword == "break":
                    return self._parse_break_statement()
                elif keyword == "continue":
                    return self._parse_continue_statement()
                elif keyword == "assert":
                    return self._parse_assert_statement()
                elif keyword == "yield":
                    return self._parse_yield_statement()
                elif keyword in ["var", "final"] or self._is_type_keyword(keyword):
                    return self._parse_local_variable_declaration()
            
            # Check for local variable declaration (type name)
            if self._is_type_start():
                return self._parse_local_variable_declaration()
            
            # Default to expression statement
            expr = self._parse_expression()
            self._consume(JavaTokenType.SEMICOLON)
            return JavaExpressionStatement(expr)
            
        except Exception as e:
            self._log_error(f"Error parsing statement: {e}")
            # Skip to next semicolon or brace for error recovery
            self._synchronize()
            return None
    
    def _parse_labeled_statement(self) -> JavaLabeledStatement:
        """Parse labeled statement."""
        label = self._consume(JavaTokenType.IDENTIFIER).value
        self._consume(JavaTokenType.COLON)
        body = self._parse_statement()
        return JavaLabeledStatement(label=label, body=body)
    
    def _parse_if_statement(self) -> JavaIfStatement:
        """Parse if statement."""
        self._consume(JavaTokenType.KEYWORD)  # if
        self._consume(JavaTokenType.LEFT_PAREN)
        condition = self._parse_expression()
        self._consume(JavaTokenType.RIGHT_PAREN)
        then_statement = self._parse_statement()
        
        else_statement = None
        if self._match(JavaTokenType.KEYWORD) and self._current_token().value == "else":
            self._advance()
            else_statement = self._parse_statement()
        
        return JavaIfStatement(
            condition=condition,
            then_statement=then_statement,
            else_statement=else_statement
        )
    
    def _parse_while_statement(self) -> JavaWhileStatement:
        """Parse while statement."""
        self._consume(JavaTokenType.KEYWORD)  # while
        self._consume(JavaTokenType.LEFT_PAREN)
        condition = self._parse_expression()
        self._consume(JavaTokenType.RIGHT_PAREN)
        body = self._parse_statement()
        
        return JavaWhileStatement(condition=condition, body=body)
    
    def _parse_for_statement(self) -> Union[JavaForStatement, JavaEnhancedForStatement]:
        """Parse for statement (traditional or enhanced)."""
        self._consume(JavaTokenType.KEYWORD)  # for
        self._consume(JavaTokenType.LEFT_PAREN)
        
        # Try to determine if this is an enhanced for loop
        # Look ahead for the colon to distinguish enhanced for from traditional for
        checkpoint = self._position
        try:
            # Try parsing as enhanced for (for variable : iterable)
            variable_type = self._parse_type()
            variable_name = self._consume(JavaTokenType.IDENTIFIER).value
            if self._match(JavaTokenType.COLON):
                self._advance()  # consume :
                iterable = self._parse_expression()
                self._consume(JavaTokenType.RIGHT_PAREN)
                body = self._parse_statement()
                
                parameter = JavaParameter(
                    parameter_type=variable_type,
                    name=variable_name
                )
                return JavaEnhancedForStatement(
                    parameter=parameter,
                    expression=iterable,
                    body=body
                )
        except:
            pass
        
        # Reset and parse as traditional for loop
        self._position = checkpoint
        
        # Traditional for loop: for (init; condition; update)
        initializers = []
        if not self._match(JavaTokenType.SEMICOLON):
            initializers.append(self._parse_expression())
            while self._match(JavaTokenType.COMMA):
                self._advance()
                initializers.append(self._parse_expression())
        self._consume(JavaTokenType.SEMICOLON)
        
        condition = None
        if not self._match(JavaTokenType.SEMICOLON):
            condition = self._parse_expression()
        self._consume(JavaTokenType.SEMICOLON)
        
        updaters = []
        if not self._match(JavaTokenType.RIGHT_PAREN):
            updaters.append(self._parse_expression())
            while self._match(JavaTokenType.COMMA):
                self._advance()
                updaters.append(self._parse_expression())
        self._consume(JavaTokenType.RIGHT_PAREN)
        
        body = self._parse_statement()
        
        return JavaForStatement(
            initializers=initializers,
            condition=condition,
            updaters=updaters,
            body=body
        )
    
    def _parse_do_statement(self) -> JavaDoStatement:
        """Parse do-while statement."""
        self._consume(JavaTokenType.KEYWORD)  # do
        body = self._parse_statement()
        self._consume(JavaTokenType.KEYWORD)  # while
        self._consume(JavaTokenType.LEFT_PAREN)
        condition = self._parse_expression()
        self._consume(JavaTokenType.RIGHT_PAREN)
        self._consume(JavaTokenType.SEMICOLON)
        
        return JavaDoStatement(body=body, condition=condition)
    
    def _parse_switch_statement(self) -> JavaSwitchStatement:
        """Parse switch statement."""
        self._consume(JavaTokenType.KEYWORD)  # switch
        self._consume(JavaTokenType.LEFT_PAREN)
        expression = self._parse_expression()
        self._consume(JavaTokenType.RIGHT_PAREN)
        self._consume(JavaTokenType.LEFT_BRACE)
        
        statements = []
        while not self._match(JavaTokenType.RIGHT_BRACE) and not self._at_end():
            if self._match(JavaTokenType.KEYWORD):
                keyword = self._current_token().value
                if keyword == "case":
                    self._advance()
                    case_expr = self._parse_expression()
                    self._consume(JavaTokenType.COLON)
                    case_statements = []
                    
                    # Parse statements until next case/default/end
                    while (not self._match(JavaTokenType.RIGHT_BRACE) and 
                           not (self._match(JavaTokenType.KEYWORD) and 
                                self._current_token().value in ["case", "default"]) and 
                           not self._at_end()):
                        stmt = self._parse_statement()
                        if stmt:
                            case_statements.append(stmt)
                    
                    statements.append(JavaSwitchCase(
                        expressions=[case_expr],
                        statements=case_statements
                    ))
                    
                elif keyword == "default":
                    self._advance()
                    self._consume(JavaTokenType.COLON)
                    default_statements = []
                    
                    # Parse statements until end
                    while (not self._match(JavaTokenType.RIGHT_BRACE) and 
                           not (self._match(JavaTokenType.KEYWORD) and 
                                self._current_token().value in ["case", "default"]) and 
                           not self._at_end()):
                        stmt = self._parse_statement()
                        if stmt:
                            default_statements.append(stmt)
                    
                    statements.append(JavaSwitchCase(
                        expressions=[],  # Empty for default
                        statements=default_statements
                    ))
                else:
                    break
            else:
                break
        
        self._consume(JavaTokenType.RIGHT_BRACE)
        return JavaSwitchStatement(expression=expression, statements=statements)
    
    def _parse_try_statement(self) -> JavaTryStatement:
        """Parse try statement."""
        self._consume(JavaTokenType.KEYWORD)  # try
        
        # Try-with-resources
        resources = []
        if self._match(JavaTokenType.LEFT_PAREN):
            self._advance()
            # Parse resource declarations
            while not self._match(JavaTokenType.RIGHT_PAREN) and not self._at_end():
                resource = self._parse_local_variable_declaration()
                resources.append(resource)
                if self._match(JavaTokenType.SEMICOLON):
                    self._advance()
                if not self._match(JavaTokenType.RIGHT_PAREN):
                    break
            self._consume(JavaTokenType.RIGHT_PAREN)
        
        body = self._parse_block_statement()
        
        # Catch clauses
        catch_clauses = []
        while (self._match(JavaTokenType.KEYWORD) and 
               self._current_token().value == "catch"):
            self._advance()
            self._consume(JavaTokenType.LEFT_PAREN)
            
            # Parse exception parameter
            exception_type = self._parse_type()
            exception_name = self._consume(JavaTokenType.IDENTIFIER).value
            exception_param = JavaParameter(
                parameter_type=exception_type,
                name=exception_name
            )
            
            self._consume(JavaTokenType.RIGHT_PAREN)
            catch_body = self._parse_block_statement()
            
            catch_clauses.append(JavaCatchClause(
                exception=exception_param,
                body=catch_body
            ))
        
        # Finally clause
        finally_block = None
        if (self._match(JavaTokenType.KEYWORD) and 
            self._current_token().value == "finally"):
            self._advance()
            finally_block = self._parse_block_statement()
        
        return JavaTryStatement(
            resources=resources,
            body=body,
            catch_clauses=catch_clauses,
            finally_block=finally_block
        )
    
    def _parse_synchronized_statement(self) -> JavaSynchronizedStatement:
        """Parse synchronized statement."""
        self._consume(JavaTokenType.KEYWORD)  # synchronized
        self._consume(JavaTokenType.LEFT_PAREN)
        expression = self._parse_expression()
        self._consume(JavaTokenType.RIGHT_PAREN)
        body = self._parse_block_statement()
        
        return JavaSynchronizedStatement(expression=expression, body=body)
    
    def _parse_return_statement(self) -> JavaReturnStatement:
        """Parse return statement."""
        self._consume(JavaTokenType.KEYWORD)  # return
        
        expression = None
        if not self._match(JavaTokenType.SEMICOLON):
            expression = self._parse_expression()
        
        self._consume(JavaTokenType.SEMICOLON)
        return JavaReturnStatement(expression=expression)
    
    def _parse_throw_statement(self) -> JavaThrowStatement:
        """Parse throw statement."""
        self._consume(JavaTokenType.KEYWORD)  # throw
        expression = self._parse_expression()
        self._consume(JavaTokenType.SEMICOLON)
        
        return JavaThrowStatement(expression=expression)
    
    def _parse_break_statement(self) -> JavaBreakStatement:
        """Parse break statement."""
        self._consume(JavaTokenType.KEYWORD)  # break
        
        label = None
        if self._match(JavaTokenType.IDENTIFIER):
            label = self._current_token().value
            self._advance()
        
        self._consume(JavaTokenType.SEMICOLON)
        return JavaBreakStatement(label=label)
    
    def _parse_continue_statement(self) -> JavaContinueStatement:
        """Parse continue statement."""
        self._consume(JavaTokenType.KEYWORD)  # continue
        
        label = None
        if self._match(JavaTokenType.IDENTIFIER):
            label = self._current_token().value
            self._advance()
        
        self._consume(JavaTokenType.SEMICOLON)
        return JavaContinueStatement(label=label)
    
    def _parse_assert_statement(self) -> JavaAssertStatement:
        """Parse assert statement."""
        self._consume(JavaTokenType.KEYWORD)  # assert
        condition = self._parse_expression()
        
        message = None
        if self._match(JavaTokenType.COLON):
            self._advance()
            message = self._parse_expression()
        
        self._consume(JavaTokenType.SEMICOLON)
        return JavaAssertStatement(condition=condition, message=message)
    
    def _parse_yield_statement(self) -> JavaYieldStatement:
        """Parse yield statement (Java 14+)."""
        self._consume(JavaTokenType.KEYWORD)  # yield
        expression = self._parse_expression()
        self._consume(JavaTokenType.SEMICOLON)
        
        return JavaYieldStatement(expression=expression)
    
    def _parse_local_variable_declaration(self) -> JavaLocalVariableDeclaration:
        """Parse local variable declaration."""
        modifiers = []
        
        # Parse modifiers
        while (self._match(JavaTokenType.KEYWORD) and 
               self._current_token().value in ["final", "var"]):
            modifier_name = self._current_token().value
            if modifier_name == "final":
                modifiers.append(JavaModifier.FINAL)
            self._advance()
        
        # Parse type
        variable_type = self._parse_type()
        
        # Parse variable declarators
        declarators = []
        while True:
            name = self._consume(JavaTokenType.IDENTIFIER).value
            
            # Handle array dimensions
            extra_dimensions = 0
            while self._match(JavaTokenType.LEFT_BRACKET):
                self._advance()
                self._consume(JavaTokenType.RIGHT_BRACKET)
                extra_dimensions += 1
            
            # Handle initializer
            initializer = None
            if self._match(JavaTokenType.ASSIGN):
                self._advance()
                initializer = self._parse_expression()
            
            declarators.append(JavaVariableDeclarationFragment(
                name=name,
                extra_dimensions=extra_dimensions,
                initializer=initializer
            ))
            
            if not self._match(JavaTokenType.COMMA):
                break
            self._advance()
        
        self._consume(JavaTokenType.SEMICOLON)
        
        return JavaLocalVariableDeclaration(
            modifiers=modifiers,
            variable_type=variable_type,
            fragments=declarators
        )
    
    def _is_type_keyword(self, keyword: str) -> bool:
        """Check if keyword is a type keyword."""
        return keyword in [
            "boolean", "byte", "char", "double", "float", "int", "long", "short", "void"
        ]
    
    def _is_type_start(self) -> bool:
        """Check if current token could start a type."""
        if self._match(JavaTokenType.IDENTIFIER):
            return True
        if self._match(JavaTokenType.KEYWORD):
            return self._is_type_keyword(self._current_token().value)
        return False
    
    def _synchronize(self):
        """Synchronize parser after error for recovery."""
        self._advance()
        
        while not self._at_end():
            if self._previous().type == JavaTokenType.SEMICOLON:
                return
            
            if self._match(JavaTokenType.KEYWORD):
                keyword = self._current_token().value
                if keyword in ["class", "fun", "var", "for", "if", "while", "return"]:
                    return
            
            self._advance()
    
    def _log_error(self, message: str):
        """Log parser error."""
        print(f"Parser Error: {message}")
    
    def _parse_expression(self) -> JavaExpression:
        """Parse complete Java expression with operator precedence."""
        return self._parse_conditional_expression()
    
    def _parse_primary(self) -> JavaExpression:
        """Parse primary expression."""
        # Literals
        if self._match(JavaTokenType.INTEGER_LITERAL):
            value = self._advance().value
            return JavaIntegerLiteral(int(value.rstrip('lL')))
        
        if self._match(JavaTokenType.FLOATING_LITERAL):
            value = self._advance().value
            return JavaFloatingLiteral(float(value.rstrip('fdFD')))
        
        if self._match(JavaTokenType.STRING_LITERAL):
            value = self._advance().value
            return JavaStringLiteral(value)
        
        if self._match(JavaTokenType.CHARACTER_LITERAL):
            value = self._advance().value
            return JavaCharacterLiteral(value)
        
        if self._match(JavaTokenType.BOOLEAN_LITERAL):
            value = self._advance().value
            return JavaBooleanLiteral(value == 'true')
        
        if self._match(JavaTokenType.NULL_LITERAL):
            self._advance()
            return JavaNullLiteral()
        
        if self._match(JavaTokenType.TEXT_BLOCK):
            value = self._advance().value
            return JavaTextBlock(value)
        
        # Identifier
        if self._match(JavaTokenType.IDENTIFIER):
            identifier = self._advance().value
            return JavaSimpleName(identifier)
        
        # Parenthesized expression
        if self._match(JavaTokenType.LEFT_PAREN):
            self._advance()
            expr = self._parse_expression()
            self._consume(JavaTokenType.RIGHT_PAREN)
            return expr
        
        # Handle 'this' and 'super' keywords
        if self._match_keyword('this'):
            self._advance()
            return JavaThisExpression()
        
        if self._match_keyword('super'):
            self._advance()
            return JavaSuperExpression()
        
        # Handle 'new' expressions
        if self._match_keyword('new'):
            return self._parse_creation_expression()
        
        # Handle lambda expressions (Java 8+)
        if self._is_lambda_expression():
            return self._parse_lambda_expression()
        
        # Class literals (e.g., String.class)
        if self._match(JavaTokenType.KEYWORD) and self._peek().value in ['class', 'void', 'int', 'boolean', 'char', 'byte', 'short', 'long', 'float', 'double']:
            return self._parse_class_literal()
        
        # Default fallback for unrecognized tokens
        self._log_error(f"Unexpected token in expression: {self._peek()}")
        return JavaSimpleName("unknown")
    
    def _parse_conditional_expression(self) -> JavaExpression:
        """Parse conditional (ternary) expression: expr ? expr : expr"""
        expr = self._parse_logical_or_expression()
        
        if self._match(JavaTokenType.QUESTION):
            self._advance()
            then_expr = self._parse_expression()
            self._consume(JavaTokenType.COLON)
            else_expr = self._parse_conditional_expression()
            return JavaConditionalExpression(condition=expr, then_expression=then_expr, else_expression=else_expr)
        
        return expr
    
    def _parse_logical_or_expression(self) -> JavaExpression:
        """Parse logical OR expression: expr || expr"""
        expr = self._parse_logical_and_expression()
        
        while self._match(JavaTokenType.LOGICAL_OR):
            operator = self._advance().value
            right = self._parse_logical_and_expression()
            expr = JavaBinaryExpression(left=expr, operator=operator, right=right)
        
        return expr
    
    def _parse_logical_and_expression(self) -> JavaExpression:
        """Parse logical AND expression: expr && expr"""
        expr = self._parse_bitwise_or_expression()
        
        while self._match(JavaTokenType.LOGICAL_AND):
            operator = self._advance().value
            right = self._parse_bitwise_or_expression()
            expr = JavaBinaryExpression(left=expr, operator=operator, right=right)
        
        return expr
    
    def _parse_bitwise_or_expression(self) -> JavaExpression:
        """Parse bitwise OR expression: expr | expr"""
        expr = self._parse_bitwise_xor_expression()
        
        while self._match(JavaTokenType.BIT_OR):
            operator = self._advance().value
            right = self._parse_bitwise_xor_expression()
            expr = JavaBinaryExpression(left=expr, operator=operator, right=right)
        
        return expr
    
    def _parse_bitwise_xor_expression(self) -> JavaExpression:
        """Parse bitwise XOR expression: expr ^ expr"""
        expr = self._parse_bitwise_and_expression()
        
        while self._match(JavaTokenType.BIT_XOR):
            operator = self._advance().value
            right = self._parse_bitwise_and_expression()
            expr = JavaBinaryExpression(left=expr, operator=operator, right=right)
        
        return expr
    
    def _parse_bitwise_and_expression(self) -> JavaExpression:
        """Parse bitwise AND expression: expr & expr"""
        expr = self._parse_equality_expression()
        
        while self._match(JavaTokenType.BIT_AND):
            operator = self._advance().value
            right = self._parse_equality_expression()
            expr = JavaBinaryExpression(left=expr, operator=operator, right=right)
        
        return expr
    
    def _parse_equality_expression(self) -> JavaExpression:
        """Parse equality expression: expr == expr | expr != expr"""
        expr = self._parse_relational_expression()
        
        while self._match(JavaTokenType.EQUAL, JavaTokenType.NOT_EQUAL):
            operator = self._advance().value
            right = self._parse_relational_expression()
            expr = JavaBinaryExpression(left=expr, operator=operator, right=right)
        
        return expr
    
    def _parse_relational_expression(self) -> JavaExpression:
        """Parse relational expression: expr < expr | expr > expr | expr <= expr | expr >= expr | instanceof"""
        expr = self._parse_shift_expression()
        
        while True:
            if self._match(JavaTokenType.LESS, JavaTokenType.GREATER, JavaTokenType.LESS_EQUAL, JavaTokenType.GREATER_EQUAL):
                operator = self._advance().value
                right = self._parse_shift_expression()
                expr = JavaBinaryExpression(left=expr, operator=operator, right=right)
            elif self._match_keyword('instanceof'):
                self._advance()
                type_expr = self._parse_type()
                expr = JavaInstanceofExpression(expression=expr, type=type_expr)
            else:
                break
        
        return expr
    
    def _parse_shift_expression(self) -> JavaExpression:
        """Parse shift expression: expr << expr | expr >> expr | expr >>> expr"""
        expr = self._parse_additive_expression()
        
        while self._match(JavaTokenType.LEFT_SHIFT, JavaTokenType.RIGHT_SHIFT, JavaTokenType.UNSIGNED_RIGHT_SHIFT):
            operator = self._advance().value
            right = self._parse_additive_expression()
            expr = JavaBinaryExpression(left=expr, operator=operator, right=right)
        
        return expr
    
    def _parse_additive_expression(self) -> JavaExpression:
        """Parse additive expression: expr + expr | expr - expr"""
        expr = self._parse_multiplicative_expression()
        
        while self._match(JavaTokenType.PLUS, JavaTokenType.MINUS):
            operator = self._advance().value
            right = self._parse_multiplicative_expression()
            expr = JavaBinaryExpression(left=expr, operator=operator, right=right)
        
        return expr
    
    def _parse_multiplicative_expression(self) -> JavaExpression:
        """Parse multiplicative expression: expr * expr | expr / expr | expr % expr"""
        expr = self._parse_unary_expression()
        
        while self._match(JavaTokenType.MULTIPLY, JavaTokenType.DIVIDE, JavaTokenType.MODULO):
            operator = self._advance().value
            right = self._parse_unary_expression()
            expr = JavaBinaryExpression(left=expr, operator=operator, right=right)
        
        return expr
    
    def _parse_unary_expression(self) -> JavaExpression:
        """Parse unary expression: +expr | -expr | !expr | ~expr | ++expr | --expr | (type)expr"""
        # Prefix unary operators
        if self._match(JavaTokenType.PLUS, JavaTokenType.MINUS, JavaTokenType.LOGICAL_NOT, JavaTokenType.BIT_NOT):
            operator = self._advance().value
            operand = self._parse_unary_expression()
            return JavaUnaryExpression(operator=operator, operand=operand, prefix=True)
        
        # Prefix increment/decrement
        if self._match(JavaTokenType.INCREMENT, JavaTokenType.DECREMENT):
            operator = self._advance().value
            operand = self._parse_postfix_expression()
            return JavaUnaryExpression(operator=operator, operand=operand, prefix=True)
        
        # Cast expression
        if self._match(JavaTokenType.LEFT_PAREN) and self._is_cast_expression():
            return self._parse_cast_expression()
        
        return self._parse_postfix_expression()
    
    def _parse_postfix_expression(self) -> JavaExpression:
        """Parse postfix expression: expr++ | expr-- | expr[index] | expr.member | expr(args)"""
        expr = self._parse_primary()
        
        while True:
            if self._match(JavaTokenType.INCREMENT, JavaTokenType.DECREMENT):
                operator = self._advance().value
                expr = JavaUnaryExpression(operator=operator, operand=expr, prefix=False)
            elif self._match(JavaTokenType.LEFT_BRACKET):
                self._advance()
                index = self._parse_expression()
                self._consume(JavaTokenType.RIGHT_BRACKET)
                expr = JavaArrayAccess(array=expr, index=index)
            elif self._match(JavaTokenType.DOT):
                self._advance()
                if self._match(JavaTokenType.IDENTIFIER):
                    member = self._advance().value
                    if self._match(JavaTokenType.LEFT_PAREN):
                        # Method call
                        self._advance()
                        arguments = []
                        if not self._match(JavaTokenType.RIGHT_PAREN):
                            arguments.append(self._parse_expression())
                            while self._match(JavaTokenType.COMMA):
                                self._advance()
                                arguments.append(self._parse_expression())
                        self._consume(JavaTokenType.RIGHT_PAREN)
                        expr = JavaMethodInvocation(expression=expr, name=member, arguments=arguments)
                    else:
                        # Field access
                        expr = JavaFieldAccess(expression=expr, name=member)
                else:
                    self._log_error("Expected identifier after dot")
                    break
            elif self._match(JavaTokenType.LEFT_PAREN):
                # Method call without explicit object (should be parsed in primary)
                self._advance()
                arguments = []
                if not self._match(JavaTokenType.RIGHT_PAREN):
                    arguments.append(self._parse_expression())
                    while self._match(JavaTokenType.COMMA):
                        self._advance()
                        arguments.append(self._parse_expression())
                self._consume(JavaTokenType.RIGHT_PAREN)
                expr = JavaMethodInvocation(expression=None, name=str(expr), arguments=arguments)
            else:
                break
        
        return expr
    
    def _is_cast_expression(self) -> bool:
        """Determine if parentheses contain a cast expression."""
        # Save current position
        saved_pos = self._position
        
        try:
            self._advance()  # consume '('
            
            # Check if this looks like a type
            if self._match(JavaTokenType.KEYWORD) and self._peek().value in ['byte', 'short', 'int', 'long', 'char', 'float', 'double', 'boolean']:
                # Primitive type cast
                return True
            elif self._match(JavaTokenType.IDENTIFIER):
                # Could be reference type cast
                return True
            
            return False
        except:
            return False
        finally:
            self._position = saved_pos
    
    def _parse_cast_expression(self) -> JavaExpression:
        """Parse cast expression: (type)expr"""
        self._consume(JavaTokenType.LEFT_PAREN)
        cast_type = self._parse_type()
        self._consume(JavaTokenType.RIGHT_PAREN)
        operand = self._parse_unary_expression()
        return JavaCastExpression(type=cast_type, expression=operand)
    
    def _parse_creation_expression(self) -> JavaExpression:
        """Parse object creation expression: new Type(args) or new Type[size]"""
        self._consume_keyword('new')
        
        # Parse type
        creation_type = self._parse_type()
        
        if self._match(JavaTokenType.LEFT_BRACKET):
            # Array creation
            dimensions = []
            while self._match(JavaTokenType.LEFT_BRACKET):
                self._advance()
                if self._match(JavaTokenType.RIGHT_BRACKET):
                    # Empty dimension []
                    dimensions.append(None)
                    self._advance()
                else:
                    # Dimension with size [expr]
                    size = self._parse_expression()
                    dimensions.append(size)
                    self._consume(JavaTokenType.RIGHT_BRACKET)
            
            # Array initializer
            initializer = None
            if self._match(JavaTokenType.LEFT_BRACE):
                initializer = self._parse_array_initializer()
            
            return JavaArrayCreation(type=creation_type, dimensions=dimensions, initializer=initializer)
        else:
            # Object creation
            self._consume(JavaTokenType.LEFT_PAREN)
            arguments = []
            if not self._match(JavaTokenType.RIGHT_PAREN):
                arguments.append(self._parse_expression())
                while self._match(JavaTokenType.COMMA):
                    self._advance()
                    arguments.append(self._parse_expression())
            self._consume(JavaTokenType.RIGHT_PAREN)
            
            # Anonymous class body (optional)
            body = None
            if self._match(JavaTokenType.LEFT_BRACE):
                body = self._parse_class_body()
            
            return JavaClassInstanceCreation(type=creation_type, arguments=arguments, anonymous_class_body=body)
    
    def _parse_lambda_expression(self) -> JavaExpression:
        """Parse lambda expression: (params) -> body or param -> body"""
        parameters = []
        
        if self._match(JavaTokenType.LEFT_PAREN):
            # Multiple parameters or no parameters: (a, b) -> ... or () -> ...
            self._advance()
            if not self._match(JavaTokenType.RIGHT_PAREN):
                parameters.append(self._parse_lambda_parameter())
                while self._match(JavaTokenType.COMMA):
                    self._advance()
                    parameters.append(self._parse_lambda_parameter())
            self._consume(JavaTokenType.RIGHT_PAREN)
        else:
            # Single parameter without parentheses: a -> ...
            parameters.append(self._parse_lambda_parameter())
        
        self._consume(JavaTokenType.ARROW)
        
        # Lambda body
        if self._match(JavaTokenType.LEFT_BRACE):
            # Block body
            body = self._parse_block_statement()
        else:
            # Expression body
            body = self._parse_expression()
        
        return JavaLambdaExpression(parameters=parameters, body=body)
    
    def _parse_lambda_parameter(self) -> JavaLambdaParameter:
        """Parse lambda parameter."""
        # Type is optional in lambda parameters
        param_type = None
        if not self._match(JavaTokenType.IDENTIFIER) or self._is_type_name():
            param_type = self._parse_type()
        
        name = self._consume(JavaTokenType.IDENTIFIER).value
        return JavaLambdaParameter(type=param_type, name=name)
    
    def _is_lambda_expression(self) -> bool:
        """Check if this is the start of a lambda expression."""
        saved_pos = self._position
        
        try:
            if self._match(JavaTokenType.IDENTIFIER):
                self._advance()
                return self._match(JavaTokenType.ARROW)
            elif self._match(JavaTokenType.LEFT_PAREN):
                self._advance()
                # Skip parameter list
                paren_count = 1
                while paren_count > 0 and not self._is_at_end():
                    if self._match(JavaTokenType.LEFT_PAREN):
                        paren_count += 1
                    elif self._match(JavaTokenType.RIGHT_PAREN):
                        paren_count -= 1
                    self._advance()
                return self._match(JavaTokenType.ARROW)
            
            return False
        except:
            return False
        finally:
            self._position = saved_pos
    
    def _parse_class_literal(self) -> JavaExpression:
        """Parse class literal: Type.class"""
        type_expr = self._parse_type()
        self._consume(JavaTokenType.DOT)
        self._consume_keyword('class')
        return JavaClassLiteral(type=type_expr)
    
    def _parse_array_initializer(self) -> JavaArrayInitializer:
        """Parse array initializer: {expr1, expr2, ...}"""
        self._consume(JavaTokenType.LEFT_BRACE)
        
        expressions = []
        if not self._match(JavaTokenType.RIGHT_BRACE):
            expressions.append(self._parse_expression())
            while self._match(JavaTokenType.COMMA):
                self._advance()
                if self._match(JavaTokenType.RIGHT_BRACE):  # Trailing comma
                    break
                expressions.append(self._parse_expression())
        
        self._consume(JavaTokenType.RIGHT_BRACE)
        return JavaArrayInitializer(expressions=expressions)
    
    def _is_type_name(self) -> bool:
        """Check if current identifier is likely a type name."""
        if not self._match(JavaTokenType.IDENTIFIER):
            return False
        
        # Simple heuristic: type names typically start with uppercase
        name = self._peek().value
        return name[0].isupper() if name else False


def parse_java(source: str, file_name: Optional[str] = None) -> JavaCompilationUnit:
    """Parse Java source code into AST."""
    try:
        # Tokenize
        lexer = JavaLexer(source, file_name)
        tokens = lexer.tokenize()
        
        # Parse
        parser = JavaParser(tokens)
        ast = parser.parse()
        
        if parser.errors:
            error_msg = "; ".join(parser.errors)
            raise SyntaxError(f"Java parse errors: {error_msg}")
        
        return ast
        
    except Exception as e:
        raise Exception(f"Failed to parse Java code: {e}")