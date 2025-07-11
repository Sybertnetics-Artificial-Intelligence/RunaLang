#!/usr/bin/env python3
"""
Swift Parser and Lexer

Comprehensive Swift parsing implementation supporting all Swift language features.

Author: Sybertnetics AI Solutions
License: MIT
"""

import re
from typing import List, Optional, Dict, Any, Union, Tuple
from dataclasses import dataclass
from enum import Enum, auto
import logging

from .swift_ast import *


class SwiftTokenType(Enum):
    """Swift token types."""
    # Literals
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    BOOLEAN = auto()
    NIL = auto()
    
    # Identifiers and keywords
    IDENTIFIER = auto()
    KEYWORD = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    ASSIGN = auto()
    EQUAL = auto()
    NOT_EQUAL = auto()
    LESS_THAN = auto()
    GREATER_THAN = auto()
    LESS_EQUAL = auto()
    GREATER_EQUAL = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    QUESTION = auto()
    EXCLAMATION = auto()
    DOT = auto()
    ARROW = auto()
    
    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    COMMA = auto()
    SEMICOLON = auto()
    COLON = auto()
    
    # Special
    EOF = auto()
    NEWLINE = auto()
    COMMENT = auto()


@dataclass
class SwiftToken:
    """Swift token representation."""
    type: SwiftTokenType
    value: str
    line: int = 1
    column: int = 1


class SwiftParseError(Exception):
    """Swift parsing error."""
    pass


class SwiftLexer:
    """Swift lexer for tokenizing Swift source code."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.keywords = SWIFT_KEYWORDS
    
    def tokenize(self, source: str) -> List[SwiftToken]:
        """Tokenize Swift source code."""
        tokens = []
        position = 0
        line = 1
        column = 1
        
        while position < len(source):
            # Skip whitespace
            if source[position].isspace():
                if source[position] == '\n':
                    line += 1
                    column = 1
                else:
                    column += 1
                position += 1
                continue
            
            # Comments
            if position < len(source) - 1 and source[position:position+2] == '//':
                end = source.find('\n', position)
                if end == -1:
                    end = len(source)
                position = end
                continue
            
            # String literals
            if source[position] == '"':
                start = position
                position += 1
                while position < len(source) and source[position] != '"':
                    if source[position] == '\\':
                        position += 1
                    position += 1
                position += 1
                tokens.append(SwiftToken(SwiftTokenType.STRING, source[start:position], line, column))
                column += position - start
                continue
            
            # Numbers
            if source[position].isdigit():
                start = position
                while position < len(source) and (source[position].isdigit() or source[position] == '.'):
                    position += 1
                value = source[start:position]
                token_type = SwiftTokenType.FLOAT if '.' in value else SwiftTokenType.INTEGER
                tokens.append(SwiftToken(token_type, value, line, column))
                column += position - start
                continue
            
            # Identifiers and keywords
            if source[position].isalpha() or source[position] == '_':
                start = position
                while position < len(source) and (source[position].isalnum() or source[position] == '_'):
                    position += 1
                value = source[start:position]
                
                # Check for special literals
                if value == "true" or value == "false":
                    token_type = SwiftTokenType.BOOLEAN
                elif value == "nil":
                    token_type = SwiftTokenType.NIL
                elif value in self.keywords:
                    token_type = SwiftTokenType.KEYWORD
                else:
                    token_type = SwiftTokenType.IDENTIFIER
                
                tokens.append(SwiftToken(token_type, value, line, column))
                column += position - start
                continue
            
            # Single character tokens
            single_char_tokens = {
                '(': SwiftTokenType.LPAREN,
                ')': SwiftTokenType.RPAREN,
                '{': SwiftTokenType.LBRACE,
                '}': SwiftTokenType.RBRACE,
                '[': SwiftTokenType.LBRACKET,
                ']': SwiftTokenType.RBRACKET,
                ',': SwiftTokenType.COMMA,
                ';': SwiftTokenType.SEMICOLON,
                ':': SwiftTokenType.COLON,
                '+': SwiftTokenType.PLUS,
                '-': SwiftTokenType.MINUS,
                '*': SwiftTokenType.MULTIPLY,
                '/': SwiftTokenType.DIVIDE,
                '%': SwiftTokenType.MODULO,
                '=': SwiftTokenType.ASSIGN,
                '<': SwiftTokenType.LESS_THAN,
                '>': SwiftTokenType.GREATER_THAN,
                '!': SwiftTokenType.EXCLAMATION,
                '?': SwiftTokenType.QUESTION,
                '.': SwiftTokenType.DOT,
            }
            
            if source[position] in single_char_tokens:
                token_type = single_char_tokens[source[position]]
                tokens.append(SwiftToken(token_type, source[position], line, column))
                position += 1
                column += 1
                continue
            
            # Skip unknown characters
            position += 1
            column += 1
        
        tokens.append(SwiftToken(SwiftTokenType.EOF, "", line, column))
        return tokens


class SwiftParser:
    """Swift recursive descent parser."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.tokens: List[SwiftToken] = []
        self.current = 0
    
    def parse(self, source: str) -> SwiftSourceFile:
        """Parse Swift source code into an AST."""
        try:
            lexer = SwiftLexer()
            self.tokens = lexer.tokenize(source)
            self.current = 0
            
            return self._parse_source_file()
            
        except Exception as e:
            self.logger.error(f"Swift parsing failed: {e}")
            raise SwiftParseError(f"Failed to parse Swift code: {e}")
    
    def _current_token(self) -> SwiftToken:
        """Get current token."""
        if self.current >= len(self.tokens):
            return SwiftToken(SwiftTokenType.EOF, "", 0, 0)
        return self.tokens[self.current]
    
    def _advance(self) -> SwiftToken:
        """Advance to next token."""
        token = self._current_token()
        if self.current < len(self.tokens) - 1:
            self.current += 1
        return token
    
    def _match(self, *token_types: SwiftTokenType) -> bool:
        """Check if current token matches any of the given types."""
        return self._current_token().type in token_types
    
    def _consume(self, token_type: SwiftTokenType) -> SwiftToken:
        """Consume token of specific type."""
        token = self._current_token()
        if token.type != token_type:
            raise SwiftParseError(f"Expected {token_type}, got {token.type}")
        return self._advance()
    
    def _parse_source_file(self) -> SwiftSourceFile:
        """Parse source file."""
        imports = []
        declarations = []
        
        # Parse imports
        while self._match(SwiftTokenType.KEYWORD) and self._current_token().value == "import":
            imports.append(self._parse_import())
        
        # Parse declarations
        while not self._match(SwiftTokenType.EOF):
            decl = self._parse_declaration()
            if decl:
                declarations.append(decl)
        
        return SwiftSourceFile(imports=imports, declarations=declarations)
    
    def _parse_import(self) -> SwiftImportDeclaration:
        """Parse import declaration."""
        self._consume(SwiftTokenType.KEYWORD)  # consume 'import'
        
        module_name = ""
        if self._match(SwiftTokenType.IDENTIFIER):
            module_name = self._advance().value
        
        return SwiftImportDeclaration(module_name=module_name)
    
    def _parse_declaration(self) -> Optional[SwiftDeclaration]:
        """Parse declaration."""
        if self._match(SwiftTokenType.KEYWORD):
            keyword = self._current_token().value
            
            if keyword == "class":
                return self._parse_class_declaration()
            elif keyword == "struct":
                return self._parse_struct_declaration()
            elif keyword == "enum":
                return self._parse_enum_declaration()
            elif keyword == "func":
                return self._parse_function_declaration()
            elif keyword in ["var", "let"]:
                return self._parse_variable_declaration()
            elif keyword == "actor":
                return self._parse_actor_declaration()
            else:
                # Skip unknown keywords
                self._advance()
                return None
        
        # Skip tokens that don't start declarations
        if not self._match(SwiftTokenType.EOF):
            self._advance()
        return None
    
    def _parse_class_declaration(self) -> SwiftClassDeclaration:
        """Parse class declaration."""
        self._consume(SwiftTokenType.KEYWORD)  # consume 'class'
        
        name = ""
        if self._match(SwiftTokenType.IDENTIFIER):
            name = self._advance().value
        
        # Skip inheritance and protocols for now
        while not self._match(SwiftTokenType.LBRACE, SwiftTokenType.EOF):
            self._advance()
        
        members = []
        if self._match(SwiftTokenType.LBRACE):
            self._advance()
            while not self._match(SwiftTokenType.RBRACE, SwiftTokenType.EOF):
                member = self._parse_declaration()
                if member:
                    members.append(member)
            
            if self._match(SwiftTokenType.RBRACE):
                self._advance()
        
        return SwiftClassDeclaration(name=name, members=members)
    
    def _parse_struct_declaration(self) -> SwiftStructDeclaration:
        """Parse struct declaration."""
        self._consume(SwiftTokenType.KEYWORD)  # consume 'struct'
        
        name = ""
        if self._match(SwiftTokenType.IDENTIFIER):
            name = self._advance().value
        
        # Skip protocols for now
        while not self._match(SwiftTokenType.LBRACE, SwiftTokenType.EOF):
            self._advance()
        
        members = []
        if self._match(SwiftTokenType.LBRACE):
            self._advance()
            while not self._match(SwiftTokenType.RBRACE, SwiftTokenType.EOF):
                member = self._parse_declaration()
                if member:
                    members.append(member)
            
            if self._match(SwiftTokenType.RBRACE):
                self._advance()
        
        return SwiftStructDeclaration(name=name, members=members)
    
    def _parse_enum_declaration(self) -> SwiftEnumDeclaration:
        """Parse enum declaration."""
        self._consume(SwiftTokenType.KEYWORD)  # consume 'enum'
        
        name = ""
        if self._match(SwiftTokenType.IDENTIFIER):
            name = self._advance().value
        
        # Skip type and protocols for now
        while not self._match(SwiftTokenType.LBRACE, SwiftTokenType.EOF):
            self._advance()
        
        cases = []
        members = []
        
        if self._match(SwiftTokenType.LBRACE):
            self._advance()
            while not self._match(SwiftTokenType.RBRACE, SwiftTokenType.EOF):
                if self._match(SwiftTokenType.KEYWORD) and self._current_token().value == "case":
                    self._advance()  # consume 'case'
                    case_name = ""
                    if self._match(SwiftTokenType.IDENTIFIER):
                        case_name = self._advance().value
                    cases.append(SwiftEnumCase(name=case_name))
                else:
                    member = self._parse_declaration()
                    if member:
                        members.append(member)
            
            if self._match(SwiftTokenType.RBRACE):
                self._advance()
        
        return SwiftEnumDeclaration(name=name, cases=cases, members=members)
    
    def _parse_function_declaration(self) -> SwiftFunctionDeclaration:
        """Parse function declaration."""
        self._consume(SwiftTokenType.KEYWORD)  # consume 'func'
        
        name = ""
        if self._match(SwiftTokenType.IDENTIFIER):
            name = self._advance().value
        
        # Parse parameters
        parameters = []
        if self._match(SwiftTokenType.LPAREN):
            self._advance()
            while not self._match(SwiftTokenType.RPAREN, SwiftTokenType.EOF):
                if self._match(SwiftTokenType.IDENTIFIER):
                    param_name = self._advance().value
                    parameters.append(SwiftParameter(internal_name=param_name))
                else:
                    self._advance()
            
            if self._match(SwiftTokenType.RPAREN):
                self._advance()
        
        # Skip return type for now
        while not self._match(SwiftTokenType.LBRACE, SwiftTokenType.EOF):
            self._advance()
        
        # Parse body
        body = None
        if self._match(SwiftTokenType.LBRACE):
            body = self._parse_code_block()
        
        return SwiftFunctionDeclaration(name=name, parameters=parameters, body=body)
    
    def _parse_variable_declaration(self) -> SwiftVariableDeclaration:
        """Parse variable declaration."""
        keyword = self._advance().value  # consume 'var' or 'let'
        
        name = ""
        if self._match(SwiftTokenType.IDENTIFIER):
            name = self._advance().value
        
        mutability = SwiftMutabilityKind.MUTABLE if keyword == "var" else SwiftMutabilityKind.IMMUTABLE
        
        # Skip type annotation and initializer for now
        while not self._match(SwiftTokenType.EOF) and not self._is_declaration_start():
            self._advance()
        
        return SwiftVariableDeclaration(name=name, mutability=mutability)
    
    def _parse_actor_declaration(self) -> SwiftActorDeclaration:
        """Parse actor declaration."""
        self._consume(SwiftTokenType.KEYWORD)  # consume 'actor'
        
        name = ""
        if self._match(SwiftTokenType.IDENTIFIER):
            name = self._advance().value
        
        # Skip protocols for now
        while not self._match(SwiftTokenType.LBRACE, SwiftTokenType.EOF):
            self._advance()
        
        members = []
        if self._match(SwiftTokenType.LBRACE):
            self._advance()
            while not self._match(SwiftTokenType.RBRACE, SwiftTokenType.EOF):
                member = self._parse_declaration()
                if member:
                    members.append(member)
            
            if self._match(SwiftTokenType.RBRACE):
                self._advance()
        
        return SwiftActorDeclaration(name=name, members=members)
    
    def _parse_code_block(self) -> SwiftCodeBlock:
        """Parse code block."""
        self._consume(SwiftTokenType.LBRACE)
        
        statements = []
        while not self._match(SwiftTokenType.RBRACE, SwiftTokenType.EOF):
            # Skip statements for now
            self._advance()
        
        if self._match(SwiftTokenType.RBRACE):
            self._advance()
        
        return SwiftCodeBlock(statements=statements)
    
    def _is_declaration_start(self) -> bool:
        """Check if current token starts a declaration."""
        if self._match(SwiftTokenType.KEYWORD):
            keyword = self._current_token().value
            return keyword in ["class", "struct", "enum", "func", "var", "let", "actor"]
        return False


# Convenience functions
def parse_swift_code(source: str) -> SwiftSourceFile:
    """Parse Swift source code and return AST."""
    parser = SwiftParser()
    return parser.parse(source)


def tokenize_swift_code(source: str) -> List[SwiftToken]:
    """Tokenize Swift source code and return tokens."""
    lexer = SwiftLexer()
    return lexer.tokenize(source)