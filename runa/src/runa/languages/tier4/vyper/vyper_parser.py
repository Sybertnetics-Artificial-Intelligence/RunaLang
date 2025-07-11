#!/usr/bin/env python3
"""
Vyper Parser and Lexer

Complete parser and lexer implementation for Vyper language supporting all Vyper constructs
including smart contracts with Python-like syntax, functions with decorators, events, 
interfaces, and blockchain-specific features.
"""

import re
from typing import List, Optional, Any, Union, Dict, Iterator, Tuple
from dataclasses import dataclass
from enum import Enum, auto

from .vyper_ast import *
from ....core.runa_ast import SourceLocation


class VyperTokenType(Enum):
    """Vyper token types."""
    # Literals
    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()
    BOOLEAN = auto()
    BYTES = auto()
    
    # Keywords
    IMPORT = auto()
    FROM = auto()
    AS = auto()
    INTERFACE = auto()
    IMPLEMENTS = auto()
    DEF = auto()
    EVENT = auto()
    STRUCT = auto()
    ENUM = auto()
    CONSTANT = auto()
    IMMUTABLE = auto()
    PUBLIC = auto()
    
    # Decorators
    EXTERNAL = auto()
    INTERNAL = auto()
    PURE = auto()
    VIEW = auto()
    PAYABLE = auto()
    NONPAYABLE = auto()
    
    # Control flow
    IF = auto()
    ELSE = auto()
    ELIF = auto()
    FOR = auto()
    IN = auto()
    RANGE = auto()
    BREAK = auto()
    CONTINUE = auto()
    RETURN = auto()
    ASSERT = auto()
    RAISE = auto()
    PASS = auto()
    
    # Special
    LOG = auto()
    SELF = auto()
    MSG = auto()
    BLOCK = auto()
    TX = auto()
    
    # Types
    UINT8 = auto()
    UINT16 = auto()
    UINT32 = auto()
    UINT64 = auto()
    UINT128 = auto()
    UINT256 = auto()
    INT8 = auto()
    INT16 = auto()
    INT32 = auto()
    INT64 = auto()
    INT128 = auto()
    INT256 = auto()
    BOOL = auto()
    ADDRESS = auto()
    BYTES32 = auto()
    BYTES_TYPE = auto()
    STRING_TYPE = auto()
    DECIMAL = auto()
    HASHMAP = auto()
    DYNARRAY = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    INT_DIVIDE = auto()
    MODULO = auto()
    POWER = auto()
    ASSIGN = auto()
    PLUS_ASSIGN = auto()
    MINUS_ASSIGN = auto()
    MULTIPLY_ASSIGN = auto()
    DIVIDE_ASSIGN = auto()
    MODULO_ASSIGN = auto()
    POWER_ASSIGN = auto()
    EQUAL = auto()
    NOT_EQUAL = auto()
    LESS_THAN = auto()
    LESS_EQUAL = auto()
    GREATER_THAN = auto()
    GREATER_EQUAL = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    BIT_AND = auto()
    BIT_OR = auto()
    BIT_XOR = auto()
    BIT_NOT = auto()
    SHIFT_LEFT = auto()
    SHIFT_RIGHT = auto()
    
    # Delimiters
    COLON = auto()
    SEMICOLON = auto()
    COMMA = auto()
    DOT = auto()
    ARROW = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    
    # Special
    EOF = auto()
    NEWLINE = auto()
    INDENT = auto()
    DEDENT = auto()
    COMMENT = auto()
    AT = auto()


@dataclass
class VyperToken:
    """Vyper token with position information."""
    type: VyperTokenType
    value: str
    line: int
    column: int
    indent_level: int = 0


class VyperLexer:
    """Vyper lexer for tokenizing source code with Python-like indentation."""
    
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.indent_stack = [0]
        
        self.keywords = {
            'import': VyperTokenType.IMPORT,
            'from': VyperTokenType.FROM,
            'as': VyperTokenType.AS,
            'interface': VyperTokenType.INTERFACE,
            'implements': VyperTokenType.IMPLEMENTS,
            'def': VyperTokenType.DEF,
            'event': VyperTokenType.EVENT,
            'struct': VyperTokenType.STRUCT,
            'enum': VyperTokenType.ENUM,
            'constant': VyperTokenType.CONSTANT,
            'immutable': VyperTokenType.IMMUTABLE,
            'public': VyperTokenType.PUBLIC,
            'external': VyperTokenType.EXTERNAL,
            'internal': VyperTokenType.INTERNAL,
            'pure': VyperTokenType.PURE,
            'view': VyperTokenType.VIEW,
            'payable': VyperTokenType.PAYABLE,
            'nonpayable': VyperTokenType.NONPAYABLE,
            'if': VyperTokenType.IF,
            'else': VyperTokenType.ELSE,
            'elif': VyperTokenType.ELIF,
            'for': VyperTokenType.FOR,
            'in': VyperTokenType.IN,
            'range': VyperTokenType.RANGE,
            'break': VyperTokenType.BREAK,
            'continue': VyperTokenType.CONTINUE,
            'return': VyperTokenType.RETURN,
            'assert': VyperTokenType.ASSERT,
            'raise': VyperTokenType.RAISE,
            'pass': VyperTokenType.PASS,
            'log': VyperTokenType.LOG,
            'self': VyperTokenType.SELF,
            'msg': VyperTokenType.MSG,
            'block': VyperTokenType.BLOCK,
            'tx': VyperTokenType.TX,
            'True': VyperTokenType.BOOLEAN,
            'False': VyperTokenType.BOOLEAN,
            'uint8': VyperTokenType.UINT8,
            'uint16': VyperTokenType.UINT16,
            'uint32': VyperTokenType.UINT32,
            'uint64': VyperTokenType.UINT64,
            'uint128': VyperTokenType.UINT128,
            'uint256': VyperTokenType.UINT256,
            'int8': VyperTokenType.INT8,
            'int16': VyperTokenType.INT16,
            'int32': VyperTokenType.INT32,
            'int64': VyperTokenType.INT64,
            'int128': VyperTokenType.INT128,
            'int256': VyperTokenType.INT256,
            'bool': VyperTokenType.BOOL,
            'address': VyperTokenType.ADDRESS,
            'bytes32': VyperTokenType.BYTES32,
            'Bytes': VyperTokenType.BYTES_TYPE,
            'String': VyperTokenType.STRING_TYPE,
            'decimal': VyperTokenType.DECIMAL,
            'HashMap': VyperTokenType.HASHMAP,
            'DynArray': VyperTokenType.DYNARRAY,
            'and': VyperTokenType.AND,
            'or': VyperTokenType.OR,
            'not': VyperTokenType.NOT
        }
    
    def current_char(self) -> Optional[str]:
        if self.position >= len(self.source):
            return None
        return self.source[self.position]
    
    def peek_char(self, offset: int = 1) -> Optional[str]:
        pos = self.position + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]
    
    def advance(self) -> Optional[str]:
        if self.position >= len(self.source):
            return None
        char = self.source[self.position]
        self.position += 1
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char
    
    def skip_whitespace(self):
        while self.current_char() and self.current_char() in ' \t\r':
            self.advance()
    
    def read_string(self, quote: str) -> str:
        value = ""
        self.advance()  # Skip opening quote
        
        while self.current_char() and self.current_char() != quote:
            char = self.current_char()
            if char == '\\':
                self.advance()
                escaped = self.current_char()
                if escaped == 'n':
                    value += '\n'
                elif escaped == 't':
                    value += '\t'
                elif escaped == 'r':
                    value += '\r'
                elif escaped == '\\':
                    value += '\\'
                elif escaped == quote:
                    value += quote
                else:
                    value += escaped if escaped else ''
            else:
                value += char
            self.advance()
        
        if self.current_char() == quote:
            self.advance()  # Skip closing quote
        
        return value
    
    def read_number(self) -> str:
        value = ""
        
        # Handle hex numbers
        if self.current_char() == '0' and self.peek_char() and self.peek_char().lower() == 'x':
            value += self.advance()  # '0'
            value += self.advance()  # 'x'
            while self.current_char() and self.current_char().lower() in '0123456789abcdef':
                value += self.advance()
            return value
        
        # Handle decimal numbers
        while self.current_char() and (self.current_char().isdigit() or self.current_char() == '.'):
            value += self.advance()
        
        # Handle scientific notation
        if self.current_char() and self.current_char().lower() == 'e':
            value += self.advance()
            if self.current_char() and self.current_char() in '+-':
                value += self.advance()
            while self.current_char() and self.current_char().isdigit():
                value += self.advance()
        
        return value
    
    def read_identifier(self) -> str:
        value = ""
        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            value += self.advance()
        return value
    
    def read_comment(self) -> str:
        value = ""
        while self.current_char() and self.current_char() != '\n':
            value += self.advance()
        return value
    
    def handle_indentation(self, tokens: List[VyperToken]):
        """Handle Python-like indentation."""
        indent_level = 0
        pos = self.position
        
        # Count leading spaces/tabs
        while pos < len(self.source) and self.source[pos] in ' \t':
            if self.source[pos] == ' ':
                indent_level += 1
            else:  # tab
                indent_level += 8  # Treat tab as 8 spaces
            pos += 1
        
        # Skip to actual indentation position
        while self.current_char() and self.current_char() in ' \t':
            self.advance()
        
        current_indent = self.indent_stack[-1]
        
        if indent_level > current_indent:
            self.indent_stack.append(indent_level)
            tokens.append(VyperToken(VyperTokenType.INDENT, '', self.line, self.column, indent_level))
        elif indent_level < current_indent:
            while self.indent_stack and self.indent_stack[-1] > indent_level:
                self.indent_stack.pop()
                tokens.append(VyperToken(VyperTokenType.DEDENT, '', self.line, self.column, indent_level))
    
    def tokenize(self) -> List[VyperToken]:
        tokens = []
        at_line_start = True
        
        while self.position < len(self.source):
            char = self.current_char()
            
            if char is None:
                break
            
            # Handle indentation at start of line
            if at_line_start and char in ' \t':
                self.handle_indentation(tokens)
                at_line_start = False
                continue
            
            # Skip whitespace (except newlines)
            if char in ' \t\r':
                self.skip_whitespace()
                continue
            
            # Handle newlines
            if char == '\n':
                if tokens and tokens[-1].type != VyperTokenType.NEWLINE:
                    tokens.append(VyperToken(VyperTokenType.NEWLINE, char, self.line, self.column))
                self.advance()
                at_line_start = True
                continue
            
            at_line_start = False
            
            # Handle comments
            if char == '#':
                comment = self.read_comment()
                tokens.append(VyperToken(VyperTokenType.COMMENT, comment, self.line, self.column))
                continue
            
            # Handle strings
            if char in '"\'':
                quote_type = char
                # Handle triple quotes
                if self.peek_char() == quote_type and self.peek_char(2) == quote_type:
                    self.advance()  # Skip first quote
                    self.advance()  # Skip second quote
                    self.advance()  # Skip third quote
                    value = ""
                    while (self.current_char() and 
                           not (self.current_char() == quote_type and 
                                self.peek_char() == quote_type and 
                                self.peek_char(2) == quote_type)):
                        value += self.advance()
                    # Skip closing triple quotes
                    if self.current_char() == quote_type:
                        self.advance()
                        if self.current_char() == quote_type:
                            self.advance()
                            if self.current_char() == quote_type:
                                self.advance()
                else:
                    value = self.read_string(quote_type)
                tokens.append(VyperToken(VyperTokenType.STRING, value, self.line, self.column))
                continue
            
            # Handle numbers
            if char.isdigit() or (char == '0' and self.peek_char() and self.peek_char().lower() == 'x'):
                number = self.read_number()
                tokens.append(VyperToken(VyperTokenType.NUMBER, number, self.line, self.column))
                continue
            
            # Handle identifiers and keywords
            if char.isalpha() or char == '_':
                identifier = self.read_identifier()
                token_type = self.keywords.get(identifier, VyperTokenType.IDENTIFIER)
                tokens.append(VyperToken(token_type, identifier, self.line, self.column))
                continue
            
            # Handle operators and delimiters
            if char == '+':
                if self.peek_char() == '=':
                    self.advance()
                    self.advance()
                    tokens.append(VyperToken(VyperTokenType.PLUS_ASSIGN, '+=', self.line, self.column))
                else:
                    tokens.append(VyperToken(VyperTokenType.PLUS, char, self.line, self.column))
                    self.advance()
                continue
            
            if char == '-':
                if self.peek_char() == '=':
                    self.advance()
                    self.advance()
                    tokens.append(VyperToken(VyperTokenType.MINUS_ASSIGN, '-=', self.line, self.column))
                elif self.peek_char() == '>':
                    self.advance()
                    self.advance()
                    tokens.append(VyperToken(VyperTokenType.ARROW, '->', self.line, self.column))
                else:
                    tokens.append(VyperToken(VyperTokenType.MINUS, char, self.line, self.column))
                    self.advance()
                continue
            
            if char == '*':
                if self.peek_char() == '*':
                    if self.peek_char(2) == '=':
                        self.advance()
                        self.advance()
                        self.advance()
                        tokens.append(VyperToken(VyperTokenType.POWER_ASSIGN, '**=', self.line, self.column))
                    else:
                        self.advance()
                        self.advance()
                        tokens.append(VyperToken(VyperTokenType.POWER, '**', self.line, self.column))
                elif self.peek_char() == '=':
                    self.advance()
                    self.advance()
                    tokens.append(VyperToken(VyperTokenType.MULTIPLY_ASSIGN, '*=', self.line, self.column))
                else:
                    tokens.append(VyperToken(VyperTokenType.MULTIPLY, char, self.line, self.column))
                    self.advance()
                continue
            
            if char == '/':
                if self.peek_char() == '/':
                    if self.peek_char(2) == '=':
                        self.advance()
                        self.advance()
                        self.advance()
                        tokens.append(VyperToken(VyperTokenType.DIVIDE_ASSIGN, '//=', self.line, self.column))
                    else:
                        self.advance()
                        self.advance()
                        tokens.append(VyperToken(VyperTokenType.INT_DIVIDE, '//', self.line, self.column))
                elif self.peek_char() == '=':
                    self.advance()
                    self.advance()
                    tokens.append(VyperToken(VyperTokenType.DIVIDE_ASSIGN, '/=', self.line, self.column))
                else:
                    tokens.append(VyperToken(VyperTokenType.DIVIDE, char, self.line, self.column))
                    self.advance()
                continue
            
            if char == '%':
                if self.peek_char() == '=':
                    self.advance()
                    self.advance()
                    tokens.append(VyperToken(VyperTokenType.MODULO_ASSIGN, '%=', self.line, self.column))
                else:
                    tokens.append(VyperToken(VyperTokenType.MODULO, char, self.line, self.column))
                    self.advance()
                continue
            
            if char == '=':
                if self.peek_char() == '=':
                    self.advance()
                    self.advance()
                    tokens.append(VyperToken(VyperTokenType.EQUAL, '==', self.line, self.column))
                else:
                    tokens.append(VyperToken(VyperTokenType.ASSIGN, char, self.line, self.column))
                    self.advance()
                continue
            
            if char == '!':
                if self.peek_char() == '=':
                    self.advance()
                    self.advance()
                    tokens.append(VyperToken(VyperTokenType.NOT_EQUAL, '!=', self.line, self.column))
                else:
                    self.advance()  # Skip unknown character
                continue
            
            if char == '<':
                if self.peek_char() == '=':
                    self.advance()
                    self.advance()
                    tokens.append(VyperToken(VyperTokenType.LESS_EQUAL, '<=', self.line, self.column))
                elif self.peek_char() == '<':
                    self.advance()
                    self.advance()
                    tokens.append(VyperToken(VyperTokenType.SHIFT_LEFT, '<<', self.line, self.column))
                else:
                    tokens.append(VyperToken(VyperTokenType.LESS_THAN, char, self.line, self.column))
                    self.advance()
                continue
            
            if char == '>':
                if self.peek_char() == '=':
                    self.advance()
                    self.advance()
                    tokens.append(VyperToken(VyperTokenType.GREATER_EQUAL, '>=', self.line, self.column))
                elif self.peek_char() == '>':
                    self.advance()
                    self.advance()
                    tokens.append(VyperToken(VyperTokenType.SHIFT_RIGHT, '>>', self.line, self.column))
                else:
                    tokens.append(VyperToken(VyperTokenType.GREATER_THAN, char, self.line, self.column))
                    self.advance()
                continue
            
            if char == '&':
                tokens.append(VyperToken(VyperTokenType.BIT_AND, char, self.line, self.column))
                self.advance()
                continue
            
            if char == '|':
                tokens.append(VyperToken(VyperTokenType.BIT_OR, char, self.line, self.column))
                self.advance()
                continue
            
            if char == '^':
                tokens.append(VyperToken(VyperTokenType.BIT_XOR, char, self.line, self.column))
                self.advance()
                continue
            
            if char == '~':
                tokens.append(VyperToken(VyperTokenType.BIT_NOT, char, self.line, self.column))
                self.advance()
                continue
            
            # Delimiters
            simple_chars = {
                ':': VyperTokenType.COLON,
                ';': VyperTokenType.SEMICOLON,
                ',': VyperTokenType.COMMA,
                '.': VyperTokenType.DOT,
                '(': VyperTokenType.LPAREN,
                ')': VyperTokenType.RPAREN,
                '{': VyperTokenType.LBRACE,
                '}': VyperTokenType.RBRACE,
                '[': VyperTokenType.LBRACKET,
                ']': VyperTokenType.RBRACKET,
                '@': VyperTokenType.AT
            }
            
            if char in simple_chars:
                tokens.append(VyperToken(simple_chars[char], char, self.line, self.column))
                self.advance()
                continue
            
            # Unknown character - skip it
            self.advance()
        
        # Add final DEDENT tokens for any remaining indentation
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            tokens.append(VyperToken(VyperTokenType.DEDENT, '', self.line, self.column))
        
        tokens.append(VyperToken(VyperTokenType.EOF, '', self.line, self.column))
        return tokens


class VyperParser:
    """Vyper parser for building AST from tokens."""
    
    def __init__(self, tokens: List[VyperToken]):
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[0] if tokens else None
    
    def advance(self) -> Optional[VyperToken]:
        if self.position < len(self.tokens) - 1:
            self.position += 1
            self.current_token = self.tokens[self.position]
            return self.current_token
        return None
    
    def match(self, *token_types: VyperTokenType) -> bool:
        return self.current_token and self.current_token.type in token_types
    
    def expect(self, token_type: VyperTokenType) -> VyperToken:
        if not self.match(token_type):
            raise ValueError(f"Expected {token_type}, got {self.current_token.type if self.current_token else 'EOF'}")
        token = self.current_token
        self.advance()
        return token
    
    def skip_newlines(self):
        while self.match(VyperTokenType.NEWLINE):
            self.advance()
    
    def parse(self) -> VyperModule:
        """Parse a complete Vyper module."""
        module = VyperModule()
        
        self.skip_newlines()
        
        while not self.match(VyperTokenType.EOF):
            if self.match(VyperTokenType.IMPORT):
                module.imports.append(self.parse_import())
            elif self.match(VyperTokenType.FROM):
                module.from_imports.append(self.parse_from_import())
            elif self.match(VyperTokenType.INTERFACE):
                module.interfaces.append(self.parse_interface())
            elif self.match(VyperTokenType.IMPLEMENTS):
                module.implements.append(self.parse_implements())
            elif self.match(VyperTokenType.STRUCT):
                module.structs.append(self.parse_struct())
            elif self.match(VyperTokenType.ENUM):
                module.enums.append(self.parse_enum())
            elif self.match(VyperTokenType.EVENT):
                module.events.append(self.parse_event())
            elif self.match(VyperTokenType.AT):
                # Function with decorators
                module.functions.append(self.parse_function())
            elif self.match(VyperTokenType.DEF):
                # Function without decorators
                module.functions.append(self.parse_function())
            elif self.match(VyperTokenType.IDENTIFIER):
                # Could be state variable, constant, or immutable
                if self.peek_declaration_type():
                    var = self.parse_variable_declaration()
                    if isinstance(var, VyperConstantDeclaration):
                        module.constants.append(var)
                    elif isinstance(var, VyperImmutableDeclaration):
                        module.immutables.append(var)
                    else:
                        module.state_variables.append(var)
                else:
                    self.advance()  # Skip unknown
            else:
                self.advance()  # Skip unknown tokens
            
            self.skip_newlines()
        
        return module
    
    def peek_declaration_type(self) -> bool:
        """Check if current position is a variable declaration."""
        # Look ahead for colon (type annotation)
        pos = self.position + 1
        while pos < len(self.tokens) and self.tokens[pos].type in [VyperTokenType.NEWLINE]:
            pos += 1
        return pos < len(self.tokens) and self.tokens[pos].type == VyperTokenType.COLON
    
    def parse_import(self) -> VyperImportStatement:
        """Parse import statement: import module [as alias]"""
        self.expect(VyperTokenType.IMPORT)
        module = self.expect(VyperTokenType.IDENTIFIER).value
        
        alias = None
        if self.match(VyperTokenType.AS):
            self.advance()
            alias = self.expect(VyperTokenType.IDENTIFIER).value
        
        return VyperImportStatement(module=module, alias=alias)
    
    def parse_from_import(self) -> VyperFromImport:
        """Parse from import: from module import name1 [as alias1], name2 [as alias2]"""
        self.expect(VyperTokenType.FROM)
        module = self.expect(VyperTokenType.IDENTIFIER).value
        self.expect(VyperTokenType.IMPORT)
        
        names = []
        aliases = []
        
        while True:
            name = self.expect(VyperTokenType.IDENTIFIER).value
            names.append(name)
            
            alias = None
            if self.match(VyperTokenType.AS):
                self.advance()
                alias = self.expect(VyperTokenType.IDENTIFIER).value
            aliases.append(alias)
            
            if not self.match(VyperTokenType.COMMA):
                break
            self.advance()
        
        return VyperFromImport(module=module, names=names, aliases=aliases)

    def parse_interface(self) -> VyperInterfaceDefinition:
        """Parse interface definition: interface ERC20:"""
        self.expect(VyperTokenType.INTERFACE)
        name = self.expect(VyperTokenType.IDENTIFIER).value
        self.expect(VyperTokenType.COLON)
        self.skip_newlines()
        
        interface = VyperInterfaceDefinition(name=name)
        
        if self.match(VyperTokenType.INDENT):
            self.advance()
            
            while not self.match(VyperTokenType.DEDENT, VyperTokenType.EOF):
                if self.match(VyperTokenType.AT, VyperTokenType.DEF):
                    interface.functions.append(self.parse_function())
                elif self.match(VyperTokenType.EVENT):
                    interface.events.append(self.parse_event())
                else:
                    self.advance()  # Skip unknown
                self.skip_newlines()
            
            if self.match(VyperTokenType.DEDENT):
                self.advance()
        
        return interface
    
    def parse_implements(self) -> VyperImplementsStatement:
        """Parse implements statement: implements: ERC20"""
        self.expect(VyperTokenType.IMPLEMENTS)
        self.expect(VyperTokenType.COLON)
        interface_name = self.expect(VyperTokenType.IDENTIFIER).value
        
        return VyperImplementsStatement(interface_name=interface_name)
    
    def parse_struct(self) -> VyperStructDefinition:
        """Parse struct definition"""
        self.expect(VyperTokenType.STRUCT)
        name = self.expect(VyperTokenType.IDENTIFIER).value
        self.expect(VyperTokenType.COLON)
        self.skip_newlines()
        
        struct = VyperStructDefinition(name=name)
        
        if self.match(VyperTokenType.INDENT):
            self.advance()
            
            while not self.match(VyperTokenType.DEDENT, VyperTokenType.EOF):
                if self.match(VyperTokenType.IDENTIFIER):
                    field = self.parse_parameter()
                    struct.fields.append(field)
                else:
                    self.advance()  # Skip unknown
                self.skip_newlines()
            
            if self.match(VyperTokenType.DEDENT):
                self.advance()
        
        return struct
    
    def parse_enum(self) -> VyperEnumDefinition:
        """Parse enum definition"""
        self.expect(VyperTokenType.ENUM)
        name = self.expect(VyperTokenType.IDENTIFIER).value
        self.expect(VyperTokenType.COLON)
        self.skip_newlines()
        
        enum = VyperEnumDefinition(name=name)
        
        if self.match(VyperTokenType.INDENT):
            self.advance()
            
            while not self.match(VyperTokenType.DEDENT, VyperTokenType.EOF):
                if self.match(VyperTokenType.IDENTIFIER):
                    value = self.expect(VyperTokenType.IDENTIFIER).value
                    enum.values.append(value)
                else:
                    self.advance()  # Skip unknown
                self.skip_newlines()
            
            if self.match(VyperTokenType.DEDENT):
                self.advance()
        
        return enum
    
    def parse_event(self) -> VyperEventDefinition:
        """Parse event definition: event Transfer:"""
        self.expect(VyperTokenType.EVENT)
        name = self.expect(VyperTokenType.IDENTIFIER).value
        self.expect(VyperTokenType.COLON)
        self.skip_newlines()
        
        event = VyperEventDefinition(name=name)
        
        if self.match(VyperTokenType.INDENT):
            self.advance()
            
            while not self.match(VyperTokenType.DEDENT, VyperTokenType.EOF):
                if self.match(VyperTokenType.IDENTIFIER):
                    param = self.parse_parameter()
                    event.parameters.append(param)
                else:
                    self.advance()  # Skip unknown
                self.skip_newlines()
            
            if self.match(VyperTokenType.DEDENT):
                self.advance()
        
        return event
    
    def parse_function(self) -> VyperFunctionDefinition:
        """Parse function definition with decorators"""
        decorators = []
        
        # Parse decorators
        while self.match(VyperTokenType.AT):
            self.advance()
            decorator_name = self.expect(VyperTokenType.IDENTIFIER).value
            decorators.append(VyperDecorator(name=decorator_name))
            self.skip_newlines()
        
        self.expect(VyperTokenType.DEF)
        name = self.expect(VyperTokenType.IDENTIFIER).value
        
        # Parse parameters
        self.expect(VyperTokenType.LPAREN)
        parameters = self.parse_parameter_list()
        self.expect(VyperTokenType.RPAREN)
        
        # Parse return type
        return_type = None
        if self.match(VyperTokenType.ARROW):
            self.advance()
            return_type = self.parse_type()
        
        self.expect(VyperTokenType.COLON)
        self.skip_newlines()
        
        # Parse function body
        body = []
        if self.match(VyperTokenType.INDENT):
            self.advance()
            body = self.parse_statement_list()
            if self.match(VyperTokenType.DEDENT):
                self.advance()
        
        return VyperFunctionDefinition(
            name=name,
            decorators=decorators,
            parameters=parameters,
            return_type=return_type,
            body=body
        )
    
    def parse_parameter_list(self) -> VyperParameterList:
        """Parse parameter list"""
        parameters = []
        
        while not self.match(VyperTokenType.RPAREN, VyperTokenType.EOF):
            if self.match(VyperTokenType.IDENTIFIER):
                param = self.parse_parameter()
                parameters.append(param)
                
                if self.match(VyperTokenType.COMMA):
                    self.advance()
                elif not self.match(VyperTokenType.RPAREN):
                    break
            else:
                self.advance()  # Skip unknown
        
        return VyperParameterList(parameters=parameters)
    
    def parse_parameter(self) -> VyperParameter:
        """Parse parameter: name: type"""
        name = self.expect(VyperTokenType.IDENTIFIER).value
        self.expect(VyperTokenType.COLON)
        type_annotation = self.parse_type()
        
        default_value = None
        if self.match(VyperTokenType.ASSIGN):
            self.advance()
            default_value = self.parse_expression()
        
        return VyperParameter(
            name=name,
            type_annotation=type_annotation,
            default_value=default_value
        )
    
    def parse_type(self) -> VyperTypeName:
        """Parse type annotation"""
        if self.match(VyperTokenType.UINT8, VyperTokenType.UINT16, VyperTokenType.UINT32,
                     VyperTokenType.UINT64, VyperTokenType.UINT128, VyperTokenType.UINT256,
                     VyperTokenType.INT8, VyperTokenType.INT16, VyperTokenType.INT32,
                     VyperTokenType.INT64, VyperTokenType.INT128, VyperTokenType.INT256,
                     VyperTokenType.BOOL, VyperTokenType.ADDRESS, VyperTokenType.BYTES32,
                     VyperTokenType.BYTES_TYPE, VyperTokenType.STRING_TYPE, VyperTokenType.DECIMAL):
            type_name = self.current_token.value
            self.advance()
            return VyperPrimitiveTypeName(name=VyperPrimitiveType(type_name))
        
        elif self.match(VyperTokenType.HASHMAP):
            self.advance()
            self.expect(VyperTokenType.LBRACKET)
            key_type = self.parse_type()
            self.expect(VyperTokenType.COMMA)
            value_type = self.parse_type()
            self.expect(VyperTokenType.RBRACKET)
            return VyperHashMapType(key_type=key_type, value_type=value_type)
        
        elif self.match(VyperTokenType.DYNARRAY):
            self.advance()
            self.expect(VyperTokenType.LBRACKET)
            element_type = self.parse_type()
            self.expect(VyperTokenType.COMMA)
            max_size = self.parse_expression()
            self.expect(VyperTokenType.RBRACKET)
            return VyperDynArrayType(element_type=element_type, max_size=max_size)
        
        elif self.match(VyperTokenType.IDENTIFIER):
            name = self.current_token.value
            self.advance()
            
            # Check for array notation
            if self.match(VyperTokenType.LBRACKET):
                self.advance()
                if self.match(VyperTokenType.RBRACKET):
                    # Dynamic array
                    self.advance()
                    base_type = VyperStructType(name=name) if name not in ['uint256', 'bool'] else VyperPrimitiveTypeName(name=VyperPrimitiveType(name))
                    return VyperArrayType(element_type=base_type, size=None)
                else:
                    # Fixed array
                    size = self.parse_expression()
                    self.expect(VyperTokenType.RBRACKET)
                    base_type = VyperStructType(name=name) if name not in ['uint256', 'bool'] else VyperPrimitiveTypeName(name=VyperPrimitiveType(name))
                    return VyperArrayType(element_type=base_type, size=size)
            
            # Struct or interface type
            return VyperStructType(name=name)
        
        else:
            raise ValueError(f"Expected type, got {self.current_token.type if self.current_token else 'EOF'}")
    
    def parse_variable_declaration(self) -> Union[VyperStateVariable, VyperConstantDeclaration, VyperImmutableDeclaration]:
        """Parse variable declaration"""
        name = self.expect(VyperTokenType.IDENTIFIER).value
        self.expect(VyperTokenType.COLON)
        
        # Check for constant or immutable
        if self.match(VyperTokenType.CONSTANT):
            self.advance()
            self.expect(VyperTokenType.LPAREN)
            type_annotation = self.parse_type()
            self.expect(VyperTokenType.RPAREN)
            self.expect(VyperTokenType.ASSIGN)
            value = self.parse_expression()
            return VyperConstantDeclaration(name=name, type_annotation=type_annotation, value=value)
        
        elif self.match(VyperTokenType.IMMUTABLE):
            self.advance()
            self.expect(VyperTokenType.LPAREN)
            type_annotation = self.parse_type()
            self.expect(VyperTokenType.RPAREN)
            return VyperImmutableDeclaration(name=name, type_annotation=type_annotation)
        
        elif self.match(VyperTokenType.PUBLIC):
            self.advance()
            self.expect(VyperTokenType.LPAREN)
            type_annotation = self.parse_type()
            self.expect(VyperTokenType.RPAREN)
            
            initial_value = None
            if self.match(VyperTokenType.ASSIGN):
                self.advance()
                initial_value = self.parse_expression()
            
            return VyperStateVariable(
                name=name,
                type_annotation=type_annotation,
                initial_value=initial_value,
                is_public=True
            )
        
        else:
            # Regular state variable
            type_annotation = self.parse_type()
            
            initial_value = None
            if self.match(VyperTokenType.ASSIGN):
                self.advance()
                initial_value = self.parse_expression()
            
            return VyperStateVariable(
                name=name,
                type_annotation=type_annotation,
                initial_value=initial_value,
                is_public=False
            )
    
    def parse_statement_list(self) -> List[VyperStatement]:
        """Parse a list of statements"""
        statements = []
        
        while not self.match(VyperTokenType.DEDENT, VyperTokenType.EOF):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()
        
        return statements
    
    def parse_statement(self) -> Optional[VyperStatement]:
        """Parse a single statement"""
        if self.match(VyperTokenType.IF):
            return self.parse_if_statement()
        elif self.match(VyperTokenType.FOR):
            return self.parse_for_statement()
        elif self.match(VyperTokenType.RETURN):
            return self.parse_return_statement()
        elif self.match(VyperTokenType.ASSERT):
            return self.parse_assert_statement()
        elif self.match(VyperTokenType.RAISE):
            return self.parse_raise_statement()
        elif self.match(VyperTokenType.PASS):
            self.advance()
            return VyperPassStatement()
        elif self.match(VyperTokenType.BREAK):
            self.advance()
            return VyperBreakStatement()
        elif self.match(VyperTokenType.CONTINUE):
            self.advance()
            return VyperContinueStatement()
        elif self.match(VyperTokenType.LOG):
            return self.parse_log_statement()
        else:
            # Expression statement or assignment
            expr = self.parse_expression()
            if self.match(VyperTokenType.ASSIGN):
                self.advance()
                value = self.parse_expression()
                return VyperAssignmentStatement(target=expr, value=value)
            elif self.match(VyperTokenType.PLUS_ASSIGN, VyperTokenType.MINUS_ASSIGN,
                           VyperTokenType.MULTIPLY_ASSIGN, VyperTokenType.DIVIDE_ASSIGN,
                           VyperTokenType.MODULO_ASSIGN, VyperTokenType.POWER_ASSIGN):
                op_token = self.current_token
                self.advance()
                value = self.parse_expression()
                operator = VyperOperator(op_token.value)
                return VyperAugmentedAssignment(target=expr, operator=operator, value=value)
            else:
                return VyperExpressionStatement(expression=expr)
    
    def parse_if_statement(self) -> VyperIfStatement:
        """Parse if statement"""
        self.expect(VyperTokenType.IF)
        condition = self.parse_expression()
        self.expect(VyperTokenType.COLON)
        self.skip_newlines()
        
        body = []
        if self.match(VyperTokenType.INDENT):
            self.advance()
            body = self.parse_statement_list()
            if self.match(VyperTokenType.DEDENT):
                self.advance()
        
        orelse = []
        if self.match(VyperTokenType.ELSE):
            self.advance()
            self.expect(VyperTokenType.COLON)
            self.skip_newlines()
            
            if self.match(VyperTokenType.INDENT):
                self.advance()
                orelse = self.parse_statement_list()
                if self.match(VyperTokenType.DEDENT):
                    self.advance()
        
        return VyperIfStatement(condition=condition, body=body, orelse=orelse)
    
    def parse_for_statement(self) -> VyperForLoop:
        """Parse for statement"""
        self.expect(VyperTokenType.FOR)
        target = self.parse_expression()
        self.expect(VyperTokenType.IN)
        iter_expr = self.parse_expression()
        self.expect(VyperTokenType.COLON)
        self.skip_newlines()
        
        body = []
        if self.match(VyperTokenType.INDENT):
            self.advance()
            body = self.parse_statement_list()
            if self.match(VyperTokenType.DEDENT):
                self.advance()
        
        return VyperForLoop(target=target, iter=iter_expr, body=body)
    
    def parse_return_statement(self) -> VyperReturnStatement:
        """Parse return statement"""
        self.expect(VyperTokenType.RETURN)
        
        value = None
        if not self.match(VyperTokenType.NEWLINE, VyperTokenType.EOF):
            value = self.parse_expression()
        
        return VyperReturnStatement(value=value)
    
    def parse_assert_statement(self) -> VyperAssertStatement:
        """Parse assert statement"""
        self.expect(VyperTokenType.ASSERT)
        test = self.parse_expression()
        
        msg = None
        if self.match(VyperTokenType.COMMA):
            self.advance()
            msg = self.parse_expression()
        
        return VyperAssertStatement(test=test, msg=msg)
    
    def parse_raise_statement(self) -> VyperRaiseStatement:
        """Parse raise statement"""
        self.expect(VyperTokenType.RAISE)
        
        exc = None
        if not self.match(VyperTokenType.NEWLINE, VyperTokenType.EOF):
            exc = self.parse_expression()
        
        return VyperRaiseStatement(exc=exc)
    
    def parse_log_statement(self) -> VyperLogStatement:
        """Parse log statement"""
        self.expect(VyperTokenType.LOG)
        event_call = self.parse_expression()
        
        if not isinstance(event_call, VyperFunctionCall):
            raise ValueError("Expected function call after 'log'")
        
        return VyperLogStatement(event_call=event_call)
    
    def parse_expression(self) -> VyperExpression:
        """Parse expression with operator precedence"""
        return self.parse_or_expression()
    
    def parse_or_expression(self) -> VyperExpression:
        """Parse 'or' expression"""
        expr = self.parse_and_expression()
        
        while self.match(VyperTokenType.OR):
            op = VyperOperator(self.current_token.value)
            self.advance()
            right = self.parse_and_expression()
            expr = VyperBinaryExpression(left=expr, operator=op, right=right)
        
        return expr
    
    def parse_and_expression(self) -> VyperExpression:
        """Parse 'and' expression"""
        expr = self.parse_not_expression()
        
        while self.match(VyperTokenType.AND):
            op = VyperOperator(self.current_token.value)
            self.advance()
            right = self.parse_not_expression()
            expr = VyperBinaryExpression(left=expr, operator=op, right=right)
        
        return expr
    
    def parse_not_expression(self) -> VyperExpression:
        """Parse 'not' expression"""
        if self.match(VyperTokenType.NOT):
            op = VyperOperator(self.current_token.value)
            self.advance()
            operand = self.parse_not_expression()
            return VyperUnaryExpression(operator=op, operand=operand)
        
        return self.parse_comparison()
    
    def parse_comparison(self) -> VyperExpression:
        """Parse comparison expression"""
        expr = self.parse_bitwise_or()
        
        while self.match(VyperTokenType.EQUAL, VyperTokenType.NOT_EQUAL,
                         VyperTokenType.LESS_THAN, VyperTokenType.LESS_EQUAL,
                         VyperTokenType.GREATER_THAN, VyperTokenType.GREATER_EQUAL):
            op = VyperOperator(self.current_token.value)
            self.advance()
            right = self.parse_bitwise_or()
            expr = VyperBinaryExpression(left=expr, operator=op, right=right)
        
        return expr
    
    def parse_bitwise_or(self) -> VyperExpression:
        """Parse bitwise or expression"""
        expr = self.parse_bitwise_xor()
        
        while self.match(VyperTokenType.BIT_OR):
            op = VyperOperator(self.current_token.value)
            self.advance()
            right = self.parse_bitwise_xor()
            expr = VyperBinaryExpression(left=expr, operator=op, right=right)
        
        return expr
    
    def parse_bitwise_xor(self) -> VyperExpression:
        """Parse bitwise xor expression"""
        expr = self.parse_bitwise_and()
        
        while self.match(VyperTokenType.BIT_XOR):
            op = VyperOperator(self.current_token.value)
            self.advance()
            right = self.parse_bitwise_and()
            expr = VyperBinaryExpression(left=expr, operator=op, right=right)
        
        return expr
    
    def parse_bitwise_and(self) -> VyperExpression:
        """Parse bitwise and expression"""
        expr = self.parse_shift()
        
        while self.match(VyperTokenType.BIT_AND):
            op = VyperOperator(self.current_token.value)
            self.advance()
            right = self.parse_shift()
            expr = VyperBinaryExpression(left=expr, operator=op, right=right)
        
        return expr
    
    def parse_shift(self) -> VyperExpression:
        """Parse shift expression"""
        expr = self.parse_additive()
        
        while self.match(VyperTokenType.SHIFT_LEFT, VyperTokenType.SHIFT_RIGHT):
            op = VyperOperator(self.current_token.value)
            self.advance()
            right = self.parse_additive()
            expr = VyperBinaryExpression(left=expr, operator=op, right=right)
        
        return expr
    
    def parse_additive(self) -> VyperExpression:
        """Parse additive expression"""
        expr = self.parse_multiplicative()
        
        while self.match(VyperTokenType.PLUS, VyperTokenType.MINUS):
            op = VyperOperator(self.current_token.value)
            self.advance()
            right = self.parse_multiplicative()
            expr = VyperBinaryExpression(left=expr, operator=op, right=right)
        
        return expr
    
    def parse_multiplicative(self) -> VyperExpression:
        """Parse multiplicative expression"""
        expr = self.parse_unary()
        
        while self.match(VyperTokenType.MULTIPLY, VyperTokenType.DIVIDE,
                         VyperTokenType.INT_DIVIDE, VyperTokenType.MODULO):
            op = VyperOperator(self.current_token.value)
            self.advance()
            right = self.parse_unary()
            expr = VyperBinaryExpression(left=expr, operator=op, right=right)
        
        return expr
    
    def parse_unary(self) -> VyperExpression:
        """Parse unary expression"""
        if self.match(VyperTokenType.MINUS, VyperTokenType.BIT_NOT):
            op = VyperOperator(self.current_token.value)
            self.advance()
            operand = self.parse_unary()
            return VyperUnaryExpression(operator=op, operand=operand)
        
        return self.parse_power()
    
    def parse_power(self) -> VyperExpression:
        """Parse power expression"""
        expr = self.parse_postfix()
        
        if self.match(VyperTokenType.POWER):
            op = VyperOperator(self.current_token.value)
            self.advance()
            right = self.parse_unary()  # Right associative
            expr = VyperBinaryExpression(left=expr, operator=op, right=right)
        
        return expr
    
    def parse_postfix(self) -> VyperExpression:
        """Parse postfix expression (function calls, attribute access, subscripts)"""
        expr = self.parse_primary()
        
        while True:
            if self.match(VyperTokenType.LPAREN):
                # Function call
                self.advance()
                args = []
                keywords = []
                
                while not self.match(VyperTokenType.RPAREN, VyperTokenType.EOF):
                    # Check for keyword argument
                    if (self.match(VyperTokenType.IDENTIFIER) and 
                        self.position + 1 < len(self.tokens) and 
                        self.tokens[self.position + 1].type == VyperTokenType.ASSIGN):
                        
                        name = self.expect(VyperTokenType.IDENTIFIER).value
                        self.expect(VyperTokenType.ASSIGN)
                        value = self.parse_expression()
                        keywords.append(VyperKeyword(arg=name, value=value))
                    else:
                        args.append(self.parse_expression())
                    
                    if self.match(VyperTokenType.COMMA):
                        self.advance()
                    elif not self.match(VyperTokenType.RPAREN):
                        break
                
                self.expect(VyperTokenType.RPAREN)
                expr = VyperFunctionCall(func=expr, args=args, keywords=keywords)
            
            elif self.match(VyperTokenType.DOT):
                # Attribute access
                self.advance()
                attr = self.expect(VyperTokenType.IDENTIFIER).value
                expr = VyperAttributeAccess(value=expr, attr=attr)
            
            elif self.match(VyperTokenType.LBRACKET):
                # Subscript access
                self.advance()
                if self.match(VyperTokenType.RBRACKET):
                    # Empty slice
                    slice_obj = VyperSlice()
                else:
                    # Parse slice or index
                    lower = self.parse_expression()
                    
                    if self.match(VyperTokenType.COLON):
                        # Slice
                        self.advance()
                        upper = None
                        if not self.match(VyperTokenType.RBRACKET, VyperTokenType.COLON):
                            upper = self.parse_expression()
                        
                        step = None
                        if self.match(VyperTokenType.COLON):
                            self.advance()
                            if not self.match(VyperTokenType.RBRACKET):
                                step = self.parse_expression()
                        
                        slice_obj = VyperSlice(lower=lower, upper=upper, step=step)
                    else:
                        # Simple index
                        slice_obj = VyperSlice(lower=lower)
                
                self.expect(VyperTokenType.RBRACKET)
                expr = VyperSubscriptAccess(value=expr, slice=slice_obj)
            
            else:
                break
        
        return expr
    
    def parse_primary(self) -> VyperExpression:
        """Parse primary expression"""
        if self.match(VyperTokenType.NUMBER):
            value = self.current_token.value
            self.advance()
            return VyperLiteral(value=value, type_name="number")
        
        elif self.match(VyperTokenType.STRING):
            value = self.current_token.value
            self.advance()
            return VyperLiteral(value=value, type_name="string")
        
        elif self.match(VyperTokenType.BOOLEAN):
            value = self.current_token.value == "True"
            self.advance()
            return VyperLiteral(value=value, type_name="bool")
        
        elif self.match(VyperTokenType.IDENTIFIER):
            name = self.current_token.value
            self.advance()
            return VyperIdentifier(name=name)
        
        elif self.match(VyperTokenType.LPAREN):
            # Parenthesized expression or tuple
            self.advance()
            
            if self.match(VyperTokenType.RPAREN):
                # Empty tuple
                self.advance()
                return VyperTupleExpression(elements=[])
            
            elements = [self.parse_expression()]
            
            while self.match(VyperTokenType.COMMA):
                self.advance()
                if self.match(VyperTokenType.RPAREN):
                    break
                elements.append(self.parse_expression())
            
            self.expect(VyperTokenType.RPAREN)
            
            if len(elements) == 1 and not self.match(VyperTokenType.COMMA):
                # Parenthesized expression
                return elements[0]
            else:
                # Tuple
                return VyperTupleExpression(elements=elements)
        
        elif self.match(VyperTokenType.LBRACKET):
            # List expression
            self.advance()
            elements = []
            
            while not self.match(VyperTokenType.RBRACKET, VyperTokenType.EOF):
                elements.append(self.parse_expression())
                if self.match(VyperTokenType.COMMA):
                    self.advance()
                elif not self.match(VyperTokenType.RBRACKET):
                    break
            
            self.expect(VyperTokenType.RBRACKET)
            return VyperListExpression(elements=elements)
        
        elif self.match(VyperTokenType.LBRACE):
            # Dictionary expression
            self.advance()
            keys = []
            values = []
            
            while not self.match(VyperTokenType.RBRACE, VyperTokenType.EOF):
                key = self.parse_expression()
                self.expect(VyperTokenType.COLON)
                value = self.parse_expression()
                keys.append(key)
                values.append(value)
                
                if self.match(VyperTokenType.COMMA):
                    self.advance()
                elif not self.match(VyperTokenType.RBRACE):
                    break
            
            self.expect(VyperTokenType.RBRACE)
            return VyperDictExpression(keys=keys, values=values)
        
        else:
            raise ValueError(f"Unexpected token: {self.current_token.type if self.current_token else 'EOF'}")


# Convenience functions for external use
def parse_vyper_source(source: str, file_path: str = None) -> VyperModule:
    """Parse Vyper source code into an AST."""
    try:
        lexer = VyperLexer(source)
        tokens = lexer.tokenize()
        
        # Filter out comment tokens for parsing
        tokens = [t for t in tokens if t.type != VyperTokenType.COMMENT]
        
        parser = VyperParser(tokens)
        ast = parser.parse()
        
        if file_path:
            ast.source_location = SourceLocation(file_path, 1, 1)
        
        return ast
    except Exception as e:
        raise ValueError(f"Vyper parsing failed: {str(e)}")


def parse_vyper(source: str) -> VyperModule:
    """Parse Vyper source code (convenience function)."""
    return parse_vyper_source(source) 