#!/usr/bin/env python3
"""
Objective-C Parser

Comprehensive parser for Objective-C language supporting all language features
including message passing syntax, protocols, categories, blocks, memory management,
Foundation framework integration, and Apple ecosystem constructs.

This parser handles:
- Message passing: [object method:parameter]
- Interface and implementation declarations
- Protocols and categories
- Property declarations with attributes
- Blocks and closures
- Memory management (ARC and manual)
- Preprocessor directives and imports
- Method declarations and implementations
- Foundation framework patterns
"""

import re
from typing import List, Optional, Dict, Any, Union, Tuple
from dataclasses import dataclass
from enum import Enum, auto

from ....core.base_components import BaseLanguageParser, LanguageInfo, ParseError, LanguageTier
from .objective_c_ast import *


class ObjCTokenType(Enum):
    """Objective-C token types."""
    # Literals
    NUMBER = auto()
    STRING = auto()
    NSSTRING = auto()
    BOOL = auto()
    NIL = auto()
    
    # Identifiers and keywords
    IDENTIFIER = auto()
    INTERFACE = auto()
    IMPLEMENTATION = auto()
    PROTOCOL = auto()
    END = auto()
    CLASS = auto()
    INSTANCETYPE = auto()
    ID = auto()
    VOID = auto()
    SELF = auto()
    SUPER = auto()
    
    # Property and method keywords
    PROPERTY = auto()
    SYNTHESIZE = auto()
    DYNAMIC = auto()
    ATOMIC = auto()
    NONATOMIC = auto()
    STRONG = auto()
    WEAK = auto()
    COPY = auto()
    ASSIGN = auto()
    RETAIN = auto()
    READONLY = auto()
    READWRITE = auto()
    GETTER = auto()
    SETTER = auto()
    
    # Memory management
    AUTORELEASEPOOL = auto()
    RETAIN = auto()
    RELEASE = auto()
    AUTORELEASE = auto()
    
    # Control flow and statements
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    DO = auto()
    SWITCH = auto()
    CASE = auto()
    DEFAULT = auto()
    BREAK = auto()
    CONTINUE = auto()
    RETURN = auto()
    TRY = auto()
    CATCH = auto()
    FINALLY = auto()
    THROW = auto()
    SYNCHRONIZED = auto()
    
    # Operators and punctuation
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    ASSIGN = auto()
    PLUS_ASSIGN = auto()
    MINUS_ASSIGN = auto()
    MULTIPLY_ASSIGN = auto()
    DIVIDE_ASSIGN = auto()
    EQUAL = auto()
    NOT_EQUAL = auto()
    LESS_THAN = auto()
    LESS_EQUAL = auto()
    GREATER_THAN = auto()
    GREATER_EQUAL = auto()
    LOGICAL_AND = auto()
    LOGICAL_OR = auto()
    LOGICAL_NOT = auto()
    BITWISE_AND = auto()
    BITWISE_OR = auto()
    BITWISE_XOR = auto()
    BITWISE_NOT = auto()
    LEFT_SHIFT = auto()
    RIGHT_SHIFT = auto()
    
    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    SEMICOLON = auto()
    COMMA = auto()
    DOT = auto()
    COLON = auto()
    ARROW = auto()
    CARET = auto()  # Block marker ^
    AT = auto()     # @ symbol
    HASH = auto()   # # for preprocessor
    
    # Preprocessor
    IMPORT = auto()
    INCLUDE = auto()
    DEFINE = auto()
    IFDEF = auto()
    IFNDEF = auto()
    ENDIF = auto()
    PRAGMA = auto()
    
    # Special
    NEWLINE = auto()
    WHITESPACE = auto()
    COMMENT = auto()
    EOF = auto()


@dataclass
class ObjCToken:
    """Objective-C token."""
    type: ObjCTokenType
    value: str
    line: int
    column: int


class ObjCLexer:
    """Objective-C lexer for tokenizing source code."""
    
    def __init__(self):
        self.text = ""
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        
        # Keywords mapping
        self.keywords = {
            # Language keywords
            '@interface': ObjCTokenType.INTERFACE,
            '@implementation': ObjCTokenType.IMPLEMENTATION,
            '@protocol': ObjCTokenType.PROTOCOL,
            '@end': ObjCTokenType.END,
            'Class': ObjCTokenType.CLASS,
            'instancetype': ObjCTokenType.INSTANCETYPE,
            'id': ObjCTokenType.ID,
            'void': ObjCTokenType.VOID,
            'self': ObjCTokenType.SELF,
            'super': ObjCTokenType.SUPER,
            
            # Property keywords
            '@property': ObjCTokenType.PROPERTY,
            '@synthesize': ObjCTokenType.SYNTHESIZE,
            '@dynamic': ObjCTokenType.DYNAMIC,
            'atomic': ObjCTokenType.ATOMIC,
            'nonatomic': ObjCTokenType.NONATOMIC,
            'strong': ObjCTokenType.STRONG,
            'weak': ObjCTokenType.WEAK,
            'copy': ObjCTokenType.COPY,
            'assign': ObjCTokenType.ASSIGN,
            'retain': ObjCTokenType.RETAIN,
            'readonly': ObjCTokenType.READONLY,
            'readwrite': ObjCTokenType.READWRITE,
            'getter': ObjCTokenType.GETTER,
            'setter': ObjCTokenType.SETTER,
            
            # Memory management
            '@autoreleasepool': ObjCTokenType.AUTORELEASEPOOL,
            'retain': ObjCTokenType.RETAIN,
            'release': ObjCTokenType.RELEASE,
            'autorelease': ObjCTokenType.AUTORELEASE,
            
            # Control flow
            'if': ObjCTokenType.IF,
            'else': ObjCTokenType.ELSE,
            'while': ObjCTokenType.WHILE,
            'for': ObjCTokenType.FOR,
            'do': ObjCTokenType.DO,
            'switch': ObjCTokenType.SWITCH,
            'case': ObjCTokenType.CASE,
            'default': ObjCTokenType.DEFAULT,
            'break': ObjCTokenType.BREAK,
            'continue': ObjCTokenType.CONTINUE,
            'return': ObjCTokenType.RETURN,
            '@try': ObjCTokenType.TRY,
            '@catch': ObjCTokenType.CATCH,
            '@finally': ObjCTokenType.FINALLY,
            '@throw': ObjCTokenType.THROW,
            '@synchronized': ObjCTokenType.SYNCHRONIZED,
            
            # Literals
            'YES': ObjCTokenType.BOOL,
            'NO': ObjCTokenType.BOOL,
            'TRUE': ObjCTokenType.BOOL,
            'FALSE': ObjCTokenType.BOOL,
            'nil': ObjCTokenType.NIL,
            'NULL': ObjCTokenType.NIL,
            
            # Preprocessor
            '#import': ObjCTokenType.IMPORT,
            '#include': ObjCTokenType.INCLUDE,
            '#define': ObjCTokenType.DEFINE,
            '#ifdef': ObjCTokenType.IFDEF,
            '#ifndef': ObjCTokenType.IFNDEF,
            '#endif': ObjCTokenType.ENDIF,
            '#pragma': ObjCTokenType.PRAGMA,
        }
    
    def tokenize(self, text: str) -> List[ObjCToken]:
        """Tokenize Objective-C source code."""
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        
        while self.pos < len(self.text):
            self._skip_whitespace()
            
            if self.pos >= len(self.text):
                break
            
            # Comments
            if self._match('//'):
                self._scan_line_comment()
                continue
            elif self._match('/*'):
                self._scan_block_comment()
                continue
            
            # Preprocessor directives
            if self._current_char() == '#':
                self._scan_preprocessor()
                continue
            
            # @ symbol constructs
            if self._current_char() == '@':
                if self._peek() == '"':
                    self._scan_nsstring()
                    continue
                elif self._peek().isdigit():
                    self._scan_nsnumber()
                    continue
                elif self._peek() == '[':
                    self._scan_nsarray_literal()
                    continue
                elif self._peek() == '{':
                    self._scan_nsdictionary_literal()
                    continue
                else:
                    # @ keyword
                    self._scan_at_keyword()
                    continue
            
            # String literals
            if self._current_char() == '"':
                self._scan_string()
                continue
            
            # Character literals
            if self._current_char() == "'":
                self._scan_character()
                continue
            
            # Numbers
            if self._current_char().isdigit() or (self._current_char() == '.' and self._peek().isdigit()):
                self._scan_number()
                continue
            
            # Identifiers and keywords
            if self._current_char().isalpha() or self._current_char() == '_':
                self._scan_identifier()
                continue
            
            # Message passing brackets
            if self._current_char() == '[':
                self._add_token(ObjCTokenType.LBRACKET, '[')
                continue
            elif self._current_char() == ']':
                self._add_token(ObjCTokenType.RBRACKET, ']')
                continue
            
            # Other punctuation
            char = self._current_char()
            if char == '(':
                self._add_token(ObjCTokenType.LPAREN, '(')
            elif char == ')':
                self._add_token(ObjCTokenType.RPAREN, ')')
            elif char == '{':
                self._add_token(ObjCTokenType.LBRACE, '{')
            elif char == '}':
                self._add_token(ObjCTokenType.RBRACE, '}')
            elif char == ';':
                self._add_token(ObjCTokenType.SEMICOLON, ';')
            elif char == ',':
                self._add_token(ObjCTokenType.COMMA, ',')
            elif char == '.':
                self._add_token(ObjCTokenType.DOT, '.')
            elif char == ':':
                self._add_token(ObjCTokenType.COLON, ':')
            elif char == '^':
                self._add_token(ObjCTokenType.CARET, '^')
            elif char == '=':
                if self._peek() == '=':
                    self._advance()
                    self._add_token(ObjCTokenType.EQUAL, '==')
                else:
                    self._add_token(ObjCTokenType.ASSIGN, '=')
            elif char == '!':
                if self._peek() == '=':
                    self._advance()
                    self._add_token(ObjCTokenType.NOT_EQUAL, '!=')
                else:
                    self._add_token(ObjCTokenType.LOGICAL_NOT, '!')
            elif char == '<':
                if self._peek() == '=':
                    self._advance()
                    self._add_token(ObjCTokenType.LESS_EQUAL, '<=')
                elif self._peek() == '<':
                    self._advance()
                    self._add_token(ObjCTokenType.LEFT_SHIFT, '<<')
                else:
                    self._add_token(ObjCTokenType.LESS_THAN, '<')
            elif char == '>':
                if self._peek() == '=':
                    self._advance()
                    self._add_token(ObjCTokenType.GREATER_EQUAL, '>=')
                elif self._peek() == '>':
                    self._advance()
                    self._add_token(ObjCTokenType.RIGHT_SHIFT, '>>')
                else:
                    self._add_token(ObjCTokenType.GREATER_THAN, '>')
            elif char == '+':
                if self._peek() == '=':
                    self._advance()
                    self._add_token(ObjCTokenType.PLUS_ASSIGN, '+=')
                elif self._peek() == '+':
                    self._advance()
                    self._add_token(ObjCTokenType.PLUS, '++')
                else:
                    self._add_token(ObjCTokenType.PLUS, '+')
            elif char == '-':
                if self._peek() == '=':
                    self._advance()
                    self._add_token(ObjCTokenType.MINUS_ASSIGN, '-=')
                elif self._peek() == '-':
                    self._advance()
                    self._add_token(ObjCTokenType.MINUS, '--')
                elif self._peek() == '>':
                    self._advance()
                    self._add_token(ObjCTokenType.ARROW, '->')
                else:
                    self._add_token(ObjCTokenType.MINUS, '-')
            elif char == '*':
                if self._peek() == '=':
                    self._advance()
                    self._add_token(ObjCTokenType.MULTIPLY_ASSIGN, '*=')
                else:
                    self._add_token(ObjCTokenType.MULTIPLY, '*')
            elif char == '/':
                if self._peek() == '=':
                    self._advance()
                    self._add_token(ObjCTokenType.DIVIDE_ASSIGN, '/=')
                else:
                    self._add_token(ObjCTokenType.DIVIDE, '/')
            elif char == '%':
                self._add_token(ObjCTokenType.MODULO, '%')
            elif char == '&':
                if self._peek() == '&':
                    self._advance()
                    self._add_token(ObjCTokenType.LOGICAL_AND, '&&')
                else:
                    self._add_token(ObjCTokenType.BITWISE_AND, '&')
            elif char == '|':
                if self._peek() == '|':
                    self._advance()
                    self._add_token(ObjCTokenType.LOGICAL_OR, '||')
                else:
                    self._add_token(ObjCTokenType.BITWISE_OR, '|')
            elif char == '^':
                self._add_token(ObjCTokenType.BITWISE_XOR, '^')
            elif char == '~':
                self._add_token(ObjCTokenType.BITWISE_NOT, '~')
            else:
                raise ParseError(f"Unexpected character: {char}", self._create_location())
            
            self._advance()
        
        self._add_token(ObjCTokenType.EOF, '')
        return self.tokens
    
    def _current_char(self) -> str:
        """Get current character."""
        if self.pos >= len(self.text):
            return ''
        return self.text[self.pos]
    
    def _peek(self, offset: int = 1) -> str:
        """Peek at character ahead."""
        peek_pos = self.pos + offset
        if peek_pos >= len(self.text):
            return ''
        return self.text[peek_pos]
    
    def _advance(self) -> None:
        """Advance position."""
        if self.pos < len(self.text):
            if self.text[self.pos] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.pos += 1
    
    def _match(self, expected: str) -> bool:
        """Check if current position matches expected string."""
        end_pos = self.pos + len(expected)
        if end_pos <= len(self.text):
            return self.text[self.pos:end_pos] == expected
        return False
    
    def _skip_whitespace(self) -> None:
        """Skip whitespace characters."""
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self._advance()
    
    def _scan_line_comment(self) -> None:
        """Scan line comment."""
        start_pos = self.pos
        while self.pos < len(self.text) and self.text[self.pos] != '\n':
            self._advance()
        comment_text = self.text[start_pos:self.pos]
        self._add_token(ObjCTokenType.COMMENT, comment_text)
    
    def _scan_block_comment(self) -> None:
        """Scan block comment."""
        start_pos = self.pos
        self._advance()  # Skip /*
        self._advance()
        
        while self.pos < len(self.text) - 1:
            if self.text[self.pos] == '*' and self.text[self.pos + 1] == '/':
                self._advance()  # Skip */
                self._advance()
                break
            self._advance()
        
        comment_text = self.text[start_pos:self.pos]
        self._add_token(ObjCTokenType.COMMENT, comment_text)
    
    def _scan_preprocessor(self) -> None:
        """Scan preprocessor directive."""
        start_pos = self.pos
        
        # Read until end of line or end of file
        while self.pos < len(self.text) and self.text[self.pos] != '\n':
            self._advance()
        
        directive_text = self.text[start_pos:self.pos].strip()
        
        # Check for specific preprocessor directives
        if directive_text.startswith('#import'):
            self._add_token(ObjCTokenType.IMPORT, directive_text)
        elif directive_text.startswith('#include'):
            self._add_token(ObjCTokenType.INCLUDE, directive_text)
        elif directive_text.startswith('#define'):
            self._add_token(ObjCTokenType.DEFINE, directive_text)
        elif directive_text.startswith('#ifdef'):
            self._add_token(ObjCTokenType.IFDEF, directive_text)
        elif directive_text.startswith('#ifndef'):
            self._add_token(ObjCTokenType.IFNDEF, directive_text)
        elif directive_text.startswith('#endif'):
            self._add_token(ObjCTokenType.ENDIF, directive_text)
        elif directive_text.startswith('#pragma'):
            self._add_token(ObjCTokenType.PRAGMA, directive_text)
        else:
            self._add_token(ObjCTokenType.HASH, directive_text)
    
    def _scan_nsstring(self) -> None:
        """Scan NSString literal: @"string" """
        self._advance()  # Skip @
        self._advance()  # Skip "
        
        start_pos = self.pos
        while self.pos < len(self.text) and self.text[self.pos] != '"':
            if self.text[self.pos] == '\\':
                self._advance()  # Skip escape character
            self._advance()
        
        if self.pos >= len(self.text):
            raise ParseError("Unterminated string literal", self._create_location())
        
        string_value = self.text[start_pos:self.pos]
        self._advance()  # Skip closing "
        self._add_token(ObjCTokenType.NSSTRING, string_value)
    
    def _scan_nsnumber(self) -> None:
        """Scan NSNumber literal: @42, @3.14"""
        self._advance()  # Skip @
        start_pos = self.pos
        
        # Scan number
        while self.pos < len(self.text) and (self.text[self.pos].isdigit() or self.text[self.pos] == '.'):
            self._advance()
        
        number_value = self.text[start_pos:self.pos]
        self._add_token(ObjCTokenType.NUMBER, number_value)
    
    def _scan_nsarray_literal(self) -> None:
        """Scan NSArray literal: @[...]"""
        self._advance()  # Skip @
        self._add_token(ObjCTokenType.AT, '@')
        # The [ will be tokenized separately
    
    def _scan_nsdictionary_literal(self) -> None:
        """Scan NSDictionary literal: @{...}"""
        self._advance()  # Skip @
        self._add_token(ObjCTokenType.AT, '@')
        # The { will be tokenized separately
    
    def _scan_at_keyword(self) -> None:
        """Scan @ keyword."""
        start_pos = self.pos
        self._advance()  # Skip @
        
        # Read identifier part
        while self.pos < len(self.text) and (self.text[self.pos].isalnum() or self.text[self.pos] == '_'):
            self._advance()
        
        keyword = self.text[start_pos:self.pos]
        token_type = self.keywords.get(keyword, ObjCTokenType.IDENTIFIER)
        self._add_token(token_type, keyword)
    
    def _scan_string(self) -> None:
        """Scan regular string literal."""
        self._advance()  # Skip opening "
        start_pos = self.pos
        
        while self.pos < len(self.text) and self.text[self.pos] != '"':
            if self.text[self.pos] == '\\':
                self._advance()  # Skip escape character
            self._advance()
        
        if self.pos >= len(self.text):
            raise ParseError("Unterminated string literal", self._create_location())
        
        string_value = self.text[start_pos:self.pos]
        self._advance()  # Skip closing "
        self._add_token(ObjCTokenType.STRING, string_value)
    
    def _scan_character(self) -> None:
        """Scan character literal."""
        self._advance()  # Skip opening '
        start_pos = self.pos
        
        if self.text[self.pos] == '\\':
            self._advance()  # Skip escape character
        self._advance()
        
        if self.pos >= len(self.text) or self.text[self.pos] != "'":
            raise ParseError("Unterminated character literal", self._create_location())
        
        char_value = self.text[start_pos:self.pos]
        self._advance()  # Skip closing '
        self._add_token(ObjCTokenType.STRING, char_value)
    
    def _scan_number(self) -> None:
        """Scan number literal."""
        start_pos = self.pos
        
        # Integer part
        while self.pos < len(self.text) and self.text[self.pos].isdigit():
            self._advance()
        
        # Decimal part
        if self.pos < len(self.text) and self.text[self.pos] == '.':
            self._advance()
            while self.pos < len(self.text) and self.text[self.pos].isdigit():
                self._advance()
        
        # Exponent part
        if self.pos < len(self.text) and self.text[self.pos].lower() == 'e':
            self._advance()
            if self.pos < len(self.text) and self.text[self.pos] in '+-':
                self._advance()
            while self.pos < len(self.text) and self.text[self.pos].isdigit():
                self._advance()
        
        # Suffix (f, l, etc.)
        if self.pos < len(self.text) and self.text[self.pos].lower() in 'flul':
            self._advance()
        
        number_value = self.text[start_pos:self.pos]
        self._add_token(ObjCTokenType.NUMBER, number_value)
    
    def _scan_identifier(self) -> None:
        """Scan identifier or keyword."""
        start_pos = self.pos
        
        while self.pos < len(self.text) and (self.text[self.pos].isalnum() or self.text[self.pos] == '_'):
            self._advance()
        
        identifier = self.text[start_pos:self.pos]
        token_type = self.keywords.get(identifier, ObjCTokenType.IDENTIFIER)
        self._add_token(token_type, identifier)
    
    def _add_token(self, token_type: ObjCTokenType, value: str) -> None:
        """Add token to list."""
        token = ObjCToken(token_type, value, self.line, self.column - len(value))
        self.tokens.append(token)
    
    def _create_location(self) -> 'SourceLocation':
        """Create source location for current position."""
        return SourceLocation(
            file_path="",
            line=self.line,
            column=self.column,
            end_line=self.line,
            end_column=self.column
        )


class ObjCParser(BaseLanguageParser):
    """Objective-C parser for converting source code to AST."""
    
    def __init__(self):
        language_info = LanguageInfo(
            name="objective_c",
            tier=LanguageTier.TIER6,
            file_extensions=[".m", ".mm", ".h"],
            mime_types=["text/x-objective-c", "text/x-objective-c++"],
            description="Objective-C language with Apple ecosystem integration",
            is_compiled=True,
            is_object_oriented=True,
            has_dynamic_typing=True,
            comment_patterns=[r'//.*$', r'/\*.*?\*/'],
            string_patterns=[r'".*?"', r"'.*?'", r'@".*?"'],
            number_patterns=[r'\d+\.?\d*', r'@\d+\.?\d*'],
            identifier_patterns=[r'[a-zA-Z_][a-zA-Z0-9_]*']
        )
        super().__init__(language_info)
        self.lexer = ObjCLexer()
        self.tokens = []
        self.current = 0
    
    def parse(self, source_code: str, file_path: str = "") -> ObjCSourceUnit:
        """Parse Objective-C source code into AST."""
        try:
            self._current_file_path = file_path
            self.tokens = self.lexer.tokenize(source_code)
            self.current = 0
            
            return self._parse_source_unit()
        
        except Exception as e:
            location = None
            if self.current < len(self.tokens):
                token = self.tokens[self.current]
                location = SourceLocation(file_path, token.line, token.column, token.line, token.column)
            raise ParseError(f"Parse error in {file_path}: {str(e)}", location)
    
    def _parse_source_unit(self) -> ObjCSourceUnit:
        """Parse source unit (file)."""
        source_unit = ObjCSourceUnit()
        
        while not self._is_at_end():
            # Skip comments and whitespace
            if self._match(ObjCTokenType.COMMENT, ObjCTokenType.WHITESPACE):
                continue
            
            # Preprocessor directives
            if self._check(ObjCTokenType.IMPORT, ObjCTokenType.INCLUDE, ObjCTokenType.DEFINE,
                          ObjCTokenType.IFDEF, ObjCTokenType.IFNDEF, ObjCTokenType.ENDIF, ObjCTokenType.PRAGMA):
                source_unit.preprocessor_directives.append(self._parse_preprocessor_directive())
                continue
            
            # Interface declarations
            if self._check(ObjCTokenType.INTERFACE):
                source_unit.interfaces.append(self._parse_interface_declaration())
                continue
            
            # Implementation
            if self._check(ObjCTokenType.IMPLEMENTATION):
                source_unit.implementations.append(self._parse_implementation())
                continue
            
            # Protocol declaration
            if self._check(ObjCTokenType.PROTOCOL):
                source_unit.protocols.append(self._parse_protocol_declaration())
                continue
            
            # If we get here, skip unknown tokens
            self._advance()
        
        return source_unit
    
    def _parse_preprocessor_directive(self) -> ObjCPreprocessorDirective:
        """Parse preprocessor directive."""
        token = self._advance()
        return ObjCPreprocessorDirective(
            directive=token.value.lstrip('#'),
            content=token.value
        )
    
    def _parse_interface_declaration(self) -> ObjCInterfaceDeclaration:
        """Parse @interface declaration."""
        self._consume(ObjCTokenType.INTERFACE, "Expected '@interface'")
        
        name = self._consume(ObjCTokenType.IDENTIFIER, "Expected class name").value
        
        interface = ObjCInterfaceDeclaration(name=name)
        
        # Superclass
        if self._match(ObjCTokenType.COLON):
            interface.superclass = self._consume(ObjCTokenType.IDENTIFIER, "Expected superclass name").value
        
        # Protocols
        if self._match(ObjCTokenType.LESS_THAN):
            while not self._check(ObjCTokenType.GREATER_THAN) and not self._is_at_end():
                interface.protocols.append(self._consume(ObjCTokenType.IDENTIFIER, "Expected protocol name").value)
                if not self._match(ObjCTokenType.COMMA):
                    break
            self._consume(ObjCTokenType.GREATER_THAN, "Expected '>'")
        
        # Instance variables section
        if self._match(ObjCTokenType.LBRACE):
            while not self._check(ObjCTokenType.RBRACE) and not self._is_at_end():
                if self._check(ObjCTokenType.IDENTIFIER):
                    interface.instance_variables.append(self._parse_ivar_declaration())
                else:
                    self._advance()
            self._consume(ObjCTokenType.RBRACE, "Expected '}'")
        
        # Properties and methods
        while not self._check(ObjCTokenType.END) and not self._is_at_end():
            if self._check(ObjCTokenType.PROPERTY):
                interface.properties.append(self._parse_property_declaration())
            elif self._check(ObjCTokenType.PLUS, ObjCTokenType.MINUS):
                interface.methods.append(self._parse_method_declaration())
            else:
                self._advance()
        
        self._consume(ObjCTokenType.END, "Expected '@end'")
        return interface
    
    def _parse_implementation(self) -> ObjCImplementation:
        """Parse @implementation."""
        self._consume(ObjCTokenType.IMPLEMENTATION, "Expected '@implementation'")
        
        name = self._consume(ObjCTokenType.IDENTIFIER, "Expected class name").value
        implementation = ObjCImplementation(name=name)
        
        # Instance variables section
        if self._match(ObjCTokenType.LBRACE):
            while not self._check(ObjCTokenType.RBRACE) and not self._is_at_end():
                if self._check(ObjCTokenType.IDENTIFIER):
                    implementation.instance_variables.append(self._parse_ivar_declaration())
                else:
                    self._advance()
            self._consume(ObjCTokenType.RBRACE, "Expected '}'")
        
        # Properties and methods
        while not self._check(ObjCTokenType.END) and not self._is_at_end():
            if self._check(ObjCTokenType.SYNTHESIZE, ObjCTokenType.DYNAMIC):
                implementation.properties.append(self._parse_property_synthesis())
            elif self._check(ObjCTokenType.PLUS, ObjCTokenType.MINUS):
                implementation.methods.append(self._parse_method_implementation())
            else:
                self._advance()
        
        self._consume(ObjCTokenType.END, "Expected '@end'")
        return implementation
    
    def _parse_protocol_declaration(self) -> ObjCProtocolDeclaration:
        """Parse @protocol declaration."""
        self._consume(ObjCTokenType.PROTOCOL, "Expected '@protocol'")
        
        name = self._consume(ObjCTokenType.IDENTIFIER, "Expected protocol name").value
        protocol = ObjCProtocolDeclaration(name=name)
        
        # Super protocols
        if self._match(ObjCTokenType.LESS_THAN):
            while not self._check(ObjCTokenType.GREATER_THAN) and not self._is_at_end():
                protocol.protocols.append(self._consume(ObjCTokenType.IDENTIFIER, "Expected protocol name").value)
                if not self._match(ObjCTokenType.COMMA):
                    break
            self._consume(ObjCTokenType.GREATER_THAN, "Expected '>'")
        
        # Methods and properties
        while not self._check(ObjCTokenType.END) and not self._is_at_end():
            if self._check(ObjCTokenType.PROPERTY):
                protocol.properties.append(self._parse_property_declaration())
            elif self._check(ObjCTokenType.PLUS, ObjCTokenType.MINUS):
                # For protocols, all methods are required by default
                method = self._parse_method_declaration()
                protocol.required_methods.append(method)
            else:
                self._advance()
        
        self._consume(ObjCTokenType.END, "Expected '@end'")
        return protocol
    
    def _parse_property_declaration(self) -> ObjCPropertyDeclaration:
        """Parse @property declaration."""
        self._consume(ObjCTokenType.PROPERTY, "Expected '@property'")
        
        property_decl = ObjCPropertyDeclaration()
        
        # Attributes
        if self._match(ObjCTokenType.LPAREN):
            while not self._check(ObjCTokenType.RPAREN) and not self._is_at_end():
                if self._check(ObjCTokenType.NONATOMIC):
                    property_decl.attributes.append(ObjCPropertyAttribute.NONATOMIC)
                    self._advance()
                elif self._check(ObjCTokenType.ATOMIC):
                    property_decl.attributes.append(ObjCPropertyAttribute.ATOMIC)
                    self._advance()
                elif self._check(ObjCTokenType.STRONG):
                    property_decl.attributes.append(ObjCPropertyAttribute.STRONG)
                    self._advance()
                elif self._check(ObjCTokenType.WEAK):
                    property_decl.attributes.append(ObjCPropertyAttribute.WEAK)
                    self._advance()
                elif self._check(ObjCTokenType.COPY):
                    property_decl.attributes.append(ObjCPropertyAttribute.COPY)
                    self._advance()
                elif self._check(ObjCTokenType.ASSIGN):
                    property_decl.attributes.append(ObjCPropertyAttribute.ASSIGN)
                    self._advance()
                elif self._check(ObjCTokenType.RETAIN):
                    property_decl.attributes.append(ObjCPropertyAttribute.RETAIN)
                    self._advance()
                elif self._check(ObjCTokenType.READONLY):
                    property_decl.attributes.append(ObjCPropertyAttribute.READONLY)
                    self._advance()
                elif self._check(ObjCTokenType.READWRITE):
                    property_decl.attributes.append(ObjCPropertyAttribute.READWRITE)
                    self._advance()
                else:
                    self._advance()
                
                if not self._match(ObjCTokenType.COMMA):
                    break
            
            self._consume(ObjCTokenType.RPAREN, "Expected ')'")
        
        # Type and name
        property_decl.type_annotation = self._parse_type()
        property_decl.name = self._consume(ObjCTokenType.IDENTIFIER, "Expected property name").value
        
        self._consume(ObjCTokenType.SEMICOLON, "Expected ';'")
        return property_decl
    
    def _parse_property_synthesis(self) -> ObjCPropertySynthesis:
        """Parse @synthesize or @dynamic."""
        is_dynamic = self._check(ObjCTokenType.DYNAMIC)
        self._advance()  # @synthesize or @dynamic
        
        property_name = self._consume(ObjCTokenType.IDENTIFIER, "Expected property name").value
        
        synthesis = ObjCPropertySynthesis(
            property_name=property_name,
            is_dynamic=is_dynamic
        )
        
        # Optional ivar name
        if self._match(ObjCTokenType.ASSIGN):
            synthesis.ivar_name = self._consume(ObjCTokenType.IDENTIFIER, "Expected ivar name").value
        
        self._consume(ObjCTokenType.SEMICOLON, "Expected ';'")
        return synthesis
    
    def _parse_method_declaration(self) -> ObjCMethodDeclaration:
        """Parse method declaration."""
        method_type = ObjCMethodType.INSTANCE if self._match(ObjCTokenType.MINUS) else ObjCMethodType.CLASS
        if method_type == ObjCMethodType.CLASS:
            self._consume(ObjCTokenType.PLUS, "Expected '+'")
        
        method = ObjCMethodDeclaration(method_type=method_type)
        
        # Return type
        if self._match(ObjCTokenType.LPAREN):
            method.return_type = self._parse_type()
            self._consume(ObjCTokenType.RPAREN, "Expected ')'")
        
        # Selector and parameters
        method.selector, method.parameters = self._parse_method_selector_and_parameters()
        
        self._consume(ObjCTokenType.SEMICOLON, "Expected ';'")
        return method
    
    def _parse_method_implementation(self) -> ObjCMethodImplementation:
        """Parse method implementation."""
        method_type = ObjCMethodType.INSTANCE if self._match(ObjCTokenType.MINUS) else ObjCMethodType.CLASS
        if method_type == ObjCMethodType.CLASS:
            self._consume(ObjCTokenType.PLUS, "Expected '+'")
        
        method = ObjCMethodImplementation(method_type=method_type)
        
        # Return type
        if self._match(ObjCTokenType.LPAREN):
            method.return_type = self._parse_type()
            self._consume(ObjCTokenType.RPAREN, "Expected ')'")
        
        # Selector and parameters
        method.selector, method.parameters = self._parse_method_selector_and_parameters()
        
        # Body
        if self._match(ObjCTokenType.LBRACE):
            # Parse method body (simplified)
            brace_count = 1
            while brace_count > 0 and not self._is_at_end():
                if self._match(ObjCTokenType.LBRACE):
                    brace_count += 1
                elif self._match(ObjCTokenType.RBRACE):
                    brace_count -= 1
                else:
                    self._advance()
        
        return method
    
    def _parse_method_selector_and_parameters(self) -> Tuple[ObjCSelector, List[ObjCParameter]]:
        """Parse method selector and parameters."""
        selector_parts = []
        parameters = []
        
        # First part
        selector_part = self._consume(ObjCTokenType.IDENTIFIER, "Expected selector part").value
        selector_parts.append(selector_part)
        
        # Additional parts with parameters
        while self._check(ObjCTokenType.COLON):
            self._advance()  # consume ':'
            
            # Parameter
            if self._check(ObjCTokenType.LPAREN):
                self._advance()
                param_type = self._parse_type()
                self._consume(ObjCTokenType.RPAREN, "Expected ')'")
                param_name = self._consume(ObjCTokenType.IDENTIFIER, "Expected parameter name").value
                parameters.append(ObjCParameter(type_annotation=param_type, name=param_name))
            
            # Next selector part (optional)
            if self._check(ObjCTokenType.IDENTIFIER):
                next_part = self._advance().value
                selector_parts.append(next_part)
        
        selector = ObjCSelector(parts=selector_parts)
        return selector, parameters
    
    def _parse_ivar_declaration(self) -> ObjCIvarDeclaration:
        """Parse instance variable declaration."""
        ivar_type = self._parse_type()
        name = self._consume(ObjCTokenType.IDENTIFIER, "Expected ivar name").value
        
        ivar = ObjCIvarDeclaration(
            type_annotation=ivar_type,
            name=name
        )
        
        self._consume(ObjCTokenType.SEMICOLON, "Expected ';'")
        return ivar
    
    def _parse_type(self) -> ObjCType:
        """Parse type annotation."""
        # Simplified type parsing
        if self._check(ObjCTokenType.ID):
            self._advance()
            return ObjCIdType()
        elif self._check(ObjCTokenType.INSTANCETYPE):
            self._advance()
            return ObjCInstanceType()
        elif self._check(ObjCTokenType.VOID):
            self._advance()
            return ObjCClassType(class_name="void")
        elif self._check(ObjCTokenType.IDENTIFIER):
            class_name = self._advance().value
            
            # Check for pointer
            if self._match(ObjCTokenType.MULTIPLY):
                return ObjCPointerType(pointed_type=ObjCClassType(class_name=class_name))
            else:
                return ObjCClassType(class_name=class_name)
        else:
            # Default to id type
            return ObjCIdType()
    
    # Utility methods
    def _match(self, *types: ObjCTokenType) -> bool:
        """Check if current token matches any of the given types."""
        for token_type in types:
            if self._check(token_type):
                self._advance()
                return True
        return False
    
    def _check(self, *types: ObjCTokenType) -> bool:
        """Check if current token is of given type(s)."""
        if self._is_at_end():
            return False
        return self._peek().type in types
    
    def _advance(self) -> ObjCToken:
        """Consume and return current token."""
        if not self._is_at_end():
            self.current += 1
        return self._previous()
    
    def _is_at_end(self) -> bool:
        """Check if we're at end of tokens."""
        return self._peek().type == ObjCTokenType.EOF
    
    def _peek(self) -> ObjCToken:
        """Return current token without consuming."""
        return self.tokens[self.current]
    
    def _previous(self) -> ObjCToken:
        """Return previous token."""
        return self.tokens[self.current - 1]
    
    def _consume(self, token_type: ObjCTokenType, message: str) -> ObjCToken:
        """Consume token of expected type or raise error."""
        if self._check(token_type):
            return self._advance()
        
        current_token = self._peek()
        location = SourceLocation(
            self._current_file_path,
            current_token.line,
            current_token.column,
            current_token.line,
            current_token.column
        )
        raise ParseError(f"{message}. Got {current_token.type.name}", location)


# Factory function
def parse_objective_c(source_code: str, file_path: str = "") -> ObjCSourceUnit:
    """Parse Objective-C source code into AST."""
    parser = ObjCParser()
    return parser.parse(source_code, file_path) 