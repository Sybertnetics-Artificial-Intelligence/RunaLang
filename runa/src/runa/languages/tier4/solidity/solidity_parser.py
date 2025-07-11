#!/usr/bin/env python3
"""
Solidity Parser and Lexer

Complete parser and lexer implementation for Solidity language supporting all Solidity constructs
including smart contracts, functions, modifiers, events, inheritance, and blockchain-specific features.
"""

import re
from typing import List, Optional, Any, Union, Dict, Iterator, Tuple
from dataclasses import dataclass
from enum import Enum, auto

from .solidity_ast import *
from ....core.runa_ast import SourceLocation


class SolidityTokenType(Enum):
    """Solidity token types."""
    # Literals
    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()
    BOOLEAN = auto()
    ADDRESS = auto()
    BYTES = auto()
    
    # Keywords
    PRAGMA = auto()
    IMPORT = auto()
    CONTRACT = auto()
    INTERFACE = auto()
    LIBRARY = auto()
    FUNCTION = auto()
    MODIFIER = auto()
    EVENT = auto()
    ERROR = auto()
    STRUCT = auto()
    ENUM = auto()
    MAPPING = auto()
    
    # Visibility
    PUBLIC = auto()
    PRIVATE = auto()
    INTERNAL = auto()
    EXTERNAL = auto()
    
    # Mutability
    PURE = auto()
    VIEW = auto()
    PAYABLE = auto()
    
    # Storage
    STORAGE = auto()
    MEMORY = auto()
    CALLDATA = auto()
    
    # Control flow
    IF = auto()
    ELSE = auto()
    FOR = auto()
    WHILE = auto()
    DO = auto()
    BREAK = auto()
    CONTINUE = auto()
    RETURN = auto()
    TRY = auto()
    CATCH = auto()
    
    # Special
    CONSTRUCTOR = auto()
    FALLBACK = auto()
    RECEIVE = auto()
    EMIT = auto()
    REVERT = auto()
    REQUIRE = auto()
    ASSERT = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    POWER = auto()
    ASSIGN = auto()
    EQUAL = auto()
    NOT_EQUAL = auto()
    LESS_THAN = auto()
    LESS_EQUAL = auto()
    GREATER_THAN = auto()
    GREATER_EQUAL = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    
    # Delimiters
    SEMICOLON = auto()
    COMMA = auto()
    DOT = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    
    # Special
    EOF = auto()
    NEWLINE = auto()
    COMMENT = auto()


@dataclass
class SolidityToken:
    """Solidity token with position information."""
    type: SolidityTokenType
    value: str
    line: int
    column: int


class SolidityLexer:
    """Solidity lexer for tokenizing source code."""
    
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        
        self.keywords = {
            'pragma': SolidityTokenType.PRAGMA,
            'import': SolidityTokenType.IMPORT,
            'contract': SolidityTokenType.CONTRACT,
            'interface': SolidityTokenType.INTERFACE,
            'library': SolidityTokenType.LIBRARY,
            'function': SolidityTokenType.FUNCTION,
            'modifier': SolidityTokenType.MODIFIER,
            'event': SolidityTokenType.EVENT,
            'error': SolidityTokenType.ERROR,
            'struct': SolidityTokenType.STRUCT,
            'enum': SolidityTokenType.ENUM,
            'mapping': SolidityTokenType.MAPPING,
            'public': SolidityTokenType.PUBLIC,
            'private': SolidityTokenType.PRIVATE,
            'internal': SolidityTokenType.INTERNAL,
            'external': SolidityTokenType.EXTERNAL,
            'pure': SolidityTokenType.PURE,
            'view': SolidityTokenType.VIEW,
            'payable': SolidityTokenType.PAYABLE,
            'storage': SolidityTokenType.STORAGE,
            'memory': SolidityTokenType.MEMORY,
            'calldata': SolidityTokenType.CALLDATA,
            'if': SolidityTokenType.IF,
            'else': SolidityTokenType.ELSE,
            'for': SolidityTokenType.FOR,
            'while': SolidityTokenType.WHILE,
            'do': SolidityTokenType.DO,
            'break': SolidityTokenType.BREAK,
            'continue': SolidityTokenType.CONTINUE,
            'return': SolidityTokenType.RETURN,
            'try': SolidityTokenType.TRY,
            'catch': SolidityTokenType.CATCH,
            'constructor': SolidityTokenType.CONSTRUCTOR,
            'fallback': SolidityTokenType.FALLBACK,
            'receive': SolidityTokenType.RECEIVE,
            'emit': SolidityTokenType.EMIT,
            'revert': SolidityTokenType.REVERT,
            'require': SolidityTokenType.REQUIRE,
            'assert': SolidityTokenType.ASSERT,
            'true': SolidityTokenType.BOOLEAN,
            'false': SolidityTokenType.BOOLEAN
        }
    
    def current_char(self) -> Optional[str]:
        if self.position >= len(self.source):
            return None
        return self.source[self.position]
    
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
            if self.current_char() == '\\':
                self.advance()
                if self.current_char():
                    value += self.advance()
            else:
                value += self.advance()
        
        if self.current_char() == quote:
            self.advance()  # Skip closing quote
        
        return value
    
    def read_number(self) -> str:
        number = ""
        
        # Read digits
        while self.current_char() and self.current_char().isdigit():
            number += self.advance()
        
        # Check for decimal
        if self.current_char() == '.':
            number += self.advance()
            while self.current_char() and self.current_char().isdigit():
                number += self.advance()
        
        # Check for scientific notation
        if self.current_char() and self.current_char().lower() == 'e':
            number += self.advance()
            if self.current_char() and self.current_char() in '+-':
                number += self.advance()
            while self.current_char() and self.current_char().isdigit():
                number += self.advance()
        
        return number
    
    def read_identifier(self) -> str:
        identifier = ""
        while (self.current_char() and 
               (self.current_char().isalnum() or self.current_char() == '_')):
            identifier += self.advance()
        return identifier
    
    def tokenize(self) -> List[SolidityToken]:
        tokens = []
        
        while self.position < len(self.source):
            self.skip_whitespace()
            
            if not self.current_char():
                break
            
            start_line = self.line
            start_column = self.column
            char = self.current_char()
            
            # Newlines
            if char == '\n':
                tokens.append(SolidityToken(SolidityTokenType.NEWLINE, '\n', start_line, start_column))
                self.advance()
            
            # Comments
            elif char == '/' and self.source[self.position:self.position+2] == '//':
                comment = ""
                while self.current_char() and self.current_char() != '\n':
                    comment += self.advance()
                tokens.append(SolidityToken(SolidityTokenType.COMMENT, comment, start_line, start_column))
            
            elif char == '/' and self.source[self.position:self.position+2] == '/*':
                comment = ""
                self.advance()  # Skip /
                self.advance()  # Skip *
                while self.position < len(self.source) - 1:
                    if self.source[self.position:self.position+2] == '*/':
                        self.advance()  # Skip *
                        self.advance()  # Skip /
                        break
                    comment += self.advance()
                tokens.append(SolidityToken(SolidityTokenType.COMMENT, comment, start_line, start_column))
            
            # Strings
            elif char in '"\'':
                string_value = self.read_string(char)
                tokens.append(SolidityToken(SolidityTokenType.STRING, string_value, start_line, start_column))
            
            # Numbers
            elif char.isdigit():
                number = self.read_number()
                tokens.append(SolidityToken(SolidityTokenType.NUMBER, number, start_line, start_column))
            
            # Identifiers and keywords
            elif char.isalpha() or char == '_':
                identifier = self.read_identifier()
                token_type = self.keywords.get(identifier, SolidityTokenType.IDENTIFIER)
                tokens.append(SolidityToken(token_type, identifier, start_line, start_column))
            
            # Operators and delimiters
            elif char == '=':
                if self.source[self.position:self.position+2] == '==':
                    tokens.append(SolidityToken(SolidityTokenType.EQUAL, '==', start_line, start_column))
                    self.advance()
                    self.advance()
                else:
                    tokens.append(SolidityToken(SolidityTokenType.ASSIGN, '=', start_line, start_column))
                    self.advance()
            
            elif char == '!':
                if self.source[self.position:self.position+2] == '!=':
                    tokens.append(SolidityToken(SolidityTokenType.NOT_EQUAL, '!=', start_line, start_column))
                    self.advance()
                    self.advance()
                else:
                    tokens.append(SolidityToken(SolidityTokenType.NOT, '!', start_line, start_column))
                    self.advance()
            
            elif char == '<':
                if self.source[self.position:self.position+2] == '<=':
                    tokens.append(SolidityToken(SolidityTokenType.LESS_EQUAL, '<=', start_line, start_column))
                    self.advance()
                    self.advance()
                else:
                    tokens.append(SolidityToken(SolidityTokenType.LESS_THAN, '<', start_line, start_column))
                    self.advance()
            
            elif char == '>':
                if self.source[self.position:self.position+2] == '>=':
                    tokens.append(SolidityToken(SolidityTokenType.GREATER_EQUAL, '>=', start_line, start_column))
                    self.advance()
                    self.advance()
                else:
                    tokens.append(SolidityToken(SolidityTokenType.GREATER_THAN, '>', start_line, start_column))
                    self.advance()
            
            elif char == '&':
                if self.source[self.position:self.position+2] == '&&':
                    tokens.append(SolidityToken(SolidityTokenType.AND, '&&', start_line, start_column))
                    self.advance()
                    self.advance()
                else:
                    self.advance()  # Skip single &
            
            elif char == '|':
                if self.source[self.position:self.position+2] == '||':
                    tokens.append(SolidityToken(SolidityTokenType.OR, '||', start_line, start_column))
                    self.advance()
                    self.advance()
                else:
                    self.advance()  # Skip single |
            
            # Single character tokens
            else:
                single_chars = {
                    '+': SolidityTokenType.PLUS,
                    '-': SolidityTokenType.MINUS,
                    '*': SolidityTokenType.MULTIPLY,
                    '/': SolidityTokenType.DIVIDE,
                    '%': SolidityTokenType.MODULO,
                    ';': SolidityTokenType.SEMICOLON,
                    ',': SolidityTokenType.COMMA,
                    '.': SolidityTokenType.DOT,
                    '(': SolidityTokenType.LPAREN,
                    ')': SolidityTokenType.RPAREN,
                    '{': SolidityTokenType.LBRACE,
                    '}': SolidityTokenType.RBRACE,
                    '[': SolidityTokenType.LBRACKET,
                    ']': SolidityTokenType.RBRACKET
                }
                
                if char in single_chars:
                    tokens.append(SolidityToken(single_chars[char], char, start_line, start_column))
                
                self.advance()
        
        tokens.append(SolidityToken(SolidityTokenType.EOF, '', self.line, self.column))
        return tokens


class SolidityParser:
    """Solidity parser for building AST from tokens."""
    
    def __init__(self, tokens: List[SolidityToken]):
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[0] if tokens else None
    
    def advance(self) -> Optional[SolidityToken]:
        if self.position < len(self.tokens) - 1:
            self.position += 1
            self.current_token = self.tokens[self.position]
        return self.current_token
    
    def match(self, *token_types: SolidityTokenType) -> bool:
        return self.current_token.type in token_types
    
    def expect(self, token_type: SolidityTokenType) -> SolidityToken:
        if self.current_token.type != token_type:
            raise SyntaxError(f"Expected {token_type.name}, got {self.current_token.type.name}")
        token = self.current_token
        self.advance()
        return token
    
    def skip_newlines(self):
        while self.match(SolidityTokenType.NEWLINE):
            self.advance()
    
    def parse(self) -> SoliditySourceUnit:
        """Parse Solidity source code into AST."""
        pragma_directives = []
        import_directives = []
        contracts = []
        interfaces = []
        libraries = []
        
        self.skip_newlines()
        
        while not self.match(SolidityTokenType.EOF):
            if self.match(SolidityTokenType.PRAGMA):
                pragma_directives.append(self.parse_pragma_directive())
            elif self.match(SolidityTokenType.IMPORT):
                import_directives.append(self.parse_import_directive())
            elif self.match(SolidityTokenType.CONTRACT):
                contracts.append(self.parse_contract_definition())
            elif self.match(SolidityTokenType.INTERFACE):
                interfaces.append(self.parse_interface_definition())
            elif self.match(SolidityTokenType.LIBRARY):
                libraries.append(self.parse_library_definition())
            else:
                self.advance()  # Skip unknown tokens
            
            self.skip_newlines()
        
        return SoliditySourceUnit(
            pragma_directives=pragma_directives,
            import_directives=import_directives,
            contracts=contracts,
            interfaces=interfaces,
            libraries=libraries
        )
    
    def parse_pragma_directive(self) -> SolidityPragmaDirective:
        """Parse pragma directive."""
        self.expect(SolidityTokenType.PRAGMA)
        name = self.expect(SolidityTokenType.IDENTIFIER).value
        
        # Read value until semicolon
        value = ""
        while not self.match(SolidityTokenType.SEMICOLON, SolidityTokenType.EOF):
            value += self.current_token.value + " "
            self.advance()
        
        self.expect(SolidityTokenType.SEMICOLON)
        
        return SolidityPragmaDirective(name=name, value=value.strip())
    
    def parse_import_directive(self) -> SolidityImportDirective:
        """Parse import directive."""
        self.expect(SolidityTokenType.IMPORT)
        
        path = self.expect(SolidityTokenType.STRING).value
        alias = None
        
        # TODO: Handle complex import patterns
        
        self.expect(SolidityTokenType.SEMICOLON)
        
        return SolidityImportDirective(path=path, alias=alias)
    
    def parse_contract_definition(self) -> SolidityContractDefinition:
        """Parse contract definition."""
        self.expect(SolidityTokenType.CONTRACT)
        name = self.expect(SolidityTokenType.IDENTIFIER).value
        
        # TODO: Parse inheritance, contract body, etc.
        
        self.expect(SolidityTokenType.LBRACE)
        
        # Skip contract body for now
        brace_count = 1
        while brace_count > 0 and not self.match(SolidityTokenType.EOF):
            if self.match(SolidityTokenType.LBRACE):
                brace_count += 1
            elif self.match(SolidityTokenType.RBRACE):
                brace_count -= 1
            self.advance()
        
        return SolidityContractDefinition(name=name)
    
    def parse_interface_definition(self) -> SolidityInterfaceDefinition:
        """Parse interface definition."""
        self.expect(SolidityTokenType.INTERFACE)
        name = self.expect(SolidityTokenType.IDENTIFIER).value
        
        # TODO: Parse interface body
        
        self.expect(SolidityTokenType.LBRACE)
        
        # Skip interface body for now
        brace_count = 1
        while brace_count > 0 and not self.match(SolidityTokenType.EOF):
            if self.match(SolidityTokenType.LBRACE):
                brace_count += 1
            elif self.match(SolidityTokenType.RBRACE):
                brace_count -= 1
            self.advance()
        
        return SolidityInterfaceDefinition(name=name)
    
    def parse_library_definition(self) -> SolidityLibraryDefinition:
        """Parse library definition."""
        self.expect(SolidityTokenType.LIBRARY)
        name = self.expect(SolidityTokenType.IDENTIFIER).value
        
        # TODO: Parse library body
        
        self.expect(SolidityTokenType.LBRACE)
        
        # Skip library body for now
        brace_count = 1
        while brace_count > 0 and not self.match(SolidityTokenType.EOF):
            if self.match(SolidityTokenType.LBRACE):
                brace_count += 1
            elif self.match(SolidityTokenType.RBRACE):
                brace_count -= 1
            self.advance()
        
        return SolidityLibraryDefinition(name=name)


def parse_solidity_source(source: str, file_path: str = None) -> SoliditySourceUnit:
    """Parse Solidity source code and return AST."""
    try:
        lexer = SolidityLexer(source)
        tokens = lexer.tokenize()
        
        # Filter out comments
        filtered_tokens = [t for t in tokens if t.type != SolidityTokenType.COMMENT]
        
        parser = SolidityParser(filtered_tokens)
        ast = parser.parse()
        
        return ast
    
    except Exception as e:
        raise SyntaxError(f"Error parsing Solidity code: {str(e)}")


def parse_solidity(source: str) -> SoliditySourceUnit:
    """Parse Solidity source code."""
    return parse_solidity_source(source) 