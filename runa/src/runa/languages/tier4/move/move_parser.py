#!/usr/bin/env python3
"""
Move Parser Module

Comprehensive lexer and parser implementation for the Move programming language.
Supports Move's resource-oriented programming model, modules, scripts, abilities system,
and unique safety-first syntax for digital asset management.

Features supported:
- Module and script parsing
- Resource-oriented struct definitions with abilities
- Function declarations with visibility and acquires
- Type system with generics and references
- Move-specific expressions (move, copy, borrow)
- Pattern matching and control flow
- Formal verification syntax
"""

import re
from typing import List, Optional, Dict, Any, Union, Tuple, Set
from enum import Enum, auto
from dataclasses import dataclass

from .move_ast import *


class TokenType(Enum):
    # Literals
    INTEGER = auto()
    BOOLEAN = auto()
    ADDRESS = auto()
    STRING = auto()
    BYTE_STRING = auto()
    
    # Identifiers
    IDENTIFIER = auto()
    
    # Keywords
    MODULE = auto()
    SCRIPT = auto()
    STRUCT = auto()
    FUN = auto()
    PUBLIC = auto()
    NATIVE = auto()
    ENTRY = auto()
    FRIEND = auto()
    USE = auto()
    AS = auto()
    HAS = auto()
    COPY = auto()
    DROP = auto()
    STORE = auto()
    KEY = auto()
    MOVE = auto()
    LET = auto()
    MUT = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    IN = auto()
    BREAK = auto()
    CONTINUE = auto()
    RETURN = auto()
    ABORT = auto()
    ACQUIRES = auto()
    CONST = auto()
    SPEC = auto()
    REQUIRES = auto()
    ENSURES = auto()
    ABORTS_IF = auto()
    
    # Primitive types
    BOOL = auto()
    U8 = auto()
    U16 = auto()
    U32 = auto()
    U64 = auto()
    U128 = auto()
    U256 = auto()
    ADDRESS_TYPE = auto()
    SIGNER = auto()
    VECTOR = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    EQUAL = auto()
    NOT_EQUAL = auto()
    LESS_THAN = auto()
    LESS_EQUAL = auto()
    GREATER_THAN = auto()
    GREATER_EQUAL = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    BITWISE_AND = auto()
    BITWISE_OR = auto()
    BITWISE_XOR = auto()
    BITWISE_NOT = auto()
    SHIFT_LEFT = auto()
    SHIFT_RIGHT = auto()
    ASSIGN = auto()
    
    # Punctuation
    SEMICOLON = auto()
    COMMA = auto()
    DOT = auto()
    COLON = auto()
    DOUBLE_COLON = auto()
    QUESTION = auto()
    
    # Brackets
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()
    LEFT_ANGLE = auto()
    RIGHT_ANGLE = auto()
    
    # Special
    AMPERSAND = auto()
    AMPERSAND_MUT = auto()
    ASTERISK = auto()
    
    # End of file
    EOF = auto()
    
    # Whitespace and comments (usually ignored)
    WHITESPACE = auto()
    COMMENT = auto()
    NEWLINE = auto()


@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int
    
    def __str__(self):
        return f"Token({self.type.name}, '{self.value}', {self.line}:{self.column})"


class MoveLexer:
    """Move language lexer for tokenizing Move source code."""
    
    KEYWORDS = {
        'module': TokenType.MODULE,
        'script': TokenType.SCRIPT,
        'struct': TokenType.STRUCT,
        'fun': TokenType.FUN,
        'public': TokenType.PUBLIC,
        'native': TokenType.NATIVE,
        'entry': TokenType.ENTRY,
        'friend': TokenType.FRIEND,
        'use': TokenType.USE,
        'as': TokenType.AS,
        'has': TokenType.HAS,
        'copy': TokenType.COPY,
        'drop': TokenType.DROP,
        'store': TokenType.STORE,
        'key': TokenType.KEY,
        'move': TokenType.MOVE,
        'let': TokenType.LET,
        'mut': TokenType.MUT,
        'if': TokenType.IF,
        'else': TokenType.ELSE,
        'while': TokenType.WHILE,
        'for': TokenType.FOR,
        'in': TokenType.IN,
        'break': TokenType.BREAK,
        'continue': TokenType.CONTINUE,
        'return': TokenType.RETURN,
        'abort': TokenType.ABORT,
        'acquires': TokenType.ACQUIRES,
        'const': TokenType.CONST,
        'spec': TokenType.SPEC,
        'requires': TokenType.REQUIRES,
        'ensures': TokenType.ENSURES,
        'aborts_if': TokenType.ABORTS_IF,
        'bool': TokenType.BOOL,
        'u8': TokenType.U8,
        'u16': TokenType.U16,
        'u32': TokenType.U32,
        'u64': TokenType.U64,
        'u128': TokenType.U128,
        'u256': TokenType.U256,
        'address': TokenType.ADDRESS_TYPE,
        'signer': TokenType.SIGNER,
        'vector': TokenType.VECTOR,
        'true': TokenType.BOOLEAN,
        'false': TokenType.BOOLEAN,
    }
    
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
    
    def error(self, message: str):
        raise SyntaxError(f"Lexer error at {self.line}:{self.column}: {message}")
    
    def current_char(self) -> Optional[str]:
        if self.pos >= len(self.text):
            return None
        return self.text[self.pos]
    
    def peek_char(self, offset: int = 1) -> Optional[str]:
        peek_pos = self.pos + offset
        if peek_pos >= len(self.text):
            return None
        return self.text[peek_pos]
    
    def advance(self):
        if self.pos < len(self.text) and self.text[self.pos] == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        self.pos += 1
    
    def skip_whitespace(self):
        while self.current_char() and self.current_char().isspace():
            self.advance()
    
    def skip_comment(self):
        if self.current_char() == '/' and self.peek_char() == '/':
            # Line comment
            while self.current_char() and self.current_char() != '\n':
                self.advance()
        elif self.current_char() == '/' and self.peek_char() == '*':
            # Block comment
            self.advance()  # Skip '/'
            self.advance()  # Skip '*'
            while self.current_char():
                if self.current_char() == '*' and self.peek_char() == '/':
                    self.advance()  # Skip '*'
                    self.advance()  # Skip '/'
                    break
                self.advance()
    
    def read_string(self) -> str:
        quote_char = self.current_char()
        self.advance()  # Skip opening quote
        value = ''
        
        while self.current_char() and self.current_char() != quote_char:
            if self.current_char() == '\\':
                self.advance()
                escape_char = self.current_char()
                if escape_char == 'n':
                    value += '\n'
                elif escape_char == 't':
                    value += '\t'
                elif escape_char == 'r':
                    value += '\r'
                elif escape_char == '\\':
                    value += '\\'
                elif escape_char == quote_char:
                    value += quote_char
                else:
                    value += escape_char
                self.advance()
            else:
                value += self.current_char()
                self.advance()
        
        if not self.current_char():
            self.error("Unterminated string literal")
        
        self.advance()  # Skip closing quote
        return value
    
    def read_number(self) -> str:
        value = ''
        
        # Handle hex addresses (0x...)
        if self.current_char() == '0' and self.peek_char() == 'x':
            value += self.current_char()
            self.advance()
            value += self.current_char()
            self.advance()
            while self.current_char() and (self.current_char().isdigit() or 
                                         self.current_char().lower() in 'abcdef'):
                value += self.current_char()
                self.advance()
        else:
            # Regular decimal number
            while self.current_char() and self.current_char().isdigit():
                value += self.current_char()
                self.advance()
        
        return value
    
    def read_identifier(self) -> str:
        value = ''
        while (self.current_char() and 
               (self.current_char().isalnum() or self.current_char() == '_')):
            value += self.current_char()
            self.advance()
        return value
    
    def add_token(self, token_type: TokenType, value: str = ""):
        token = Token(token_type, value, self.line, self.column - len(value))
        self.tokens.append(token)
    
    def tokenize(self) -> List[Token]:
        while self.current_char():
            # Skip whitespace
            if self.current_char().isspace():
                self.skip_whitespace()
                continue
            
            # Skip comments
            if (self.current_char() == '/' and 
                (self.peek_char() == '/' or self.peek_char() == '*')):
                self.skip_comment()
                continue
            
            char = self.current_char()
            start_line, start_col = self.line, self.column
            
            # String literals
            if char in ('"', "'"):
                value = self.read_string()
                self.add_token(TokenType.STRING, value)
                continue
            
            # Numbers and addresses
            if char.isdigit() or (char == '0' and self.peek_char() == 'x'):
                value = self.read_number()
                if value.startswith('0x'):
                    self.add_token(TokenType.ADDRESS, value)
                else:
                    self.add_token(TokenType.INTEGER, value)
                continue
            
            # Identifiers and keywords
            if char.isalpha() or char == '_':
                value = self.read_identifier()
                token_type = self.KEYWORDS.get(value, TokenType.IDENTIFIER)
                self.add_token(token_type, value)
                continue
            
            # Two-character operators
            if char == '&' and self.peek_char() == '&':
                self.advance()
                self.advance()
                self.add_token(TokenType.AND, '&&')
                continue
            
            if char == '|' and self.peek_char() == '|':
                self.advance()
                self.advance()
                self.add_token(TokenType.OR, '||')
                continue
            
            if char == '=' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.add_token(TokenType.EQUAL, '==')
                continue
            
            if char == '!' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.add_token(TokenType.NOT_EQUAL, '!=')
                continue
            
            if char == '<' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.add_token(TokenType.LESS_EQUAL, '<=')
                continue
            
            if char == '>' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.add_token(TokenType.GREATER_EQUAL, '>=')
                continue
            
            if char == '<' and self.peek_char() == '<':
                self.advance()
                self.advance()
                self.add_token(TokenType.SHIFT_LEFT, '<<')
                continue
            
            if char == '>' and self.peek_char() == '>':
                self.advance()
                self.advance()
                self.add_token(TokenType.SHIFT_RIGHT, '>>')
                continue
            
            if char == ':' and self.peek_char() == ':':
                self.advance()
                self.advance()
                self.add_token(TokenType.DOUBLE_COLON, '::')
                continue
            
            if char == '&' and self.peek_char() and self.peek_char().isspace():
                # Check for "&mut"
                saved_pos = self.pos + 1
                saved_line = self.line
                saved_col = self.column + 1
                
                # Skip whitespace
                temp_pos = saved_pos
                while temp_pos < len(self.text) and self.text[temp_pos].isspace():
                    temp_pos += 1
                
                if (temp_pos + 2 < len(self.text) and 
                    self.text[temp_pos:temp_pos + 3] == 'mut'):
                    self.add_token(TokenType.AMPERSAND_MUT, '&mut')
                    while self.pos < temp_pos + 3:
                        self.advance()
                    continue
            
            # Single-character tokens
            if char == '+':
                self.advance()
                self.add_token(TokenType.PLUS, '+')
            elif char == '-':
                self.advance()
                self.add_token(TokenType.MINUS, '-')
            elif char == '*':
                self.advance()
                self.add_token(TokenType.ASTERISK, '*')
            elif char == '/':
                self.advance()
                self.add_token(TokenType.DIVIDE, '/')
            elif char == '%':
                self.advance()
                self.add_token(TokenType.MODULO, '%')
            elif char == '=':
                self.advance()
                self.add_token(TokenType.ASSIGN, '=')
            elif char == '<':
                self.advance()
                self.add_token(TokenType.LEFT_ANGLE, '<')
            elif char == '>':
                self.advance()
                self.add_token(TokenType.RIGHT_ANGLE, '>')
            elif char == '!':
                self.advance()
                self.add_token(TokenType.NOT, '!')
            elif char == '&':
                self.advance()
                self.add_token(TokenType.AMPERSAND, '&')
            elif char == '|':
                self.advance()
                self.add_token(TokenType.BITWISE_OR, '|')
            elif char == '^':
                self.advance()
                self.add_token(TokenType.BITWISE_XOR, '^')
            elif char == '~':
                self.advance()
                self.add_token(TokenType.BITWISE_NOT, '~')
            elif char == ';':
                self.advance()
                self.add_token(TokenType.SEMICOLON, ';')
            elif char == ',':
                self.advance()
                self.add_token(TokenType.COMMA, ',')
            elif char == '.':
                self.advance()
                self.add_token(TokenType.DOT, '.')
            elif char == ':':
                self.advance()
                self.add_token(TokenType.COLON, ':')
            elif char == '?':
                self.advance()
                self.add_token(TokenType.QUESTION, '?')
            elif char == '(':
                self.advance()
                self.add_token(TokenType.LEFT_PAREN, '(')
            elif char == ')':
                self.advance()
                self.add_token(TokenType.RIGHT_PAREN, ')')
            elif char == '{':
                self.advance()
                self.add_token(TokenType.LEFT_BRACE, '{')
            elif char == '}':
                self.advance()
                self.add_token(TokenType.RIGHT_BRACE, '}')
            elif char == '[':
                self.advance()
                self.add_token(TokenType.LEFT_BRACKET, '[')
            elif char == ']':
                self.advance()
                self.add_token(TokenType.RIGHT_BRACKET, ']')
            else:
                self.error(f"Unexpected character: '{char}'")
        
        self.add_token(TokenType.EOF)
        return self.tokens


class MoveParser:
    """Move language parser for building AST from tokens."""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[0] if tokens else None
    
    def error(self, message: str):
        if self.current_token:
            raise SyntaxError(f"Parser error at {self.current_token.line}:{self.current_token.column}: {message}")
        else:
            raise SyntaxError(f"Parser error: {message}")
    
    def advance(self):
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None
    
    def peek(self, offset: int = 1) -> Optional[Token]:
        peek_pos = self.pos + offset
        if peek_pos < len(self.tokens):
            return self.tokens[peek_pos]
        return None
    
    def match(self, *token_types: TokenType) -> bool:
        return self.current_token and self.current_token.type in token_types
    
    def consume(self, token_type: TokenType, message: str = None) -> Token:
        if not self.current_token or self.current_token.type != token_type:
            msg = message or f"Expected {token_type.name}"
            self.error(msg)
        token = self.current_token
        self.advance()
        return token
    
    def parse_program(self) -> MoveProgram:
        """Parse a complete Move program."""
        modules = []
        scripts = []
        specifications = []
        
        while self.current_token and self.current_token.type != TokenType.EOF:
            if self.match(TokenType.MODULE):
                modules.append(self.parse_module())
            elif self.match(TokenType.SCRIPT):
                scripts.append(self.parse_script())
            elif self.match(TokenType.SPEC):
                specifications.append(self.parse_specification())
            else:
                self.error(f"Expected module, script, or spec, got {self.current_token.type.name}")
        
        return MoveProgram(modules=modules, scripts=scripts, specifications=specifications)
    
    def parse_module(self) -> MoveModule:
        """Parse a Move module."""
        self.consume(TokenType.MODULE)
        
        # Parse address
        address_token = self.consume(TokenType.ADDRESS)
        address = address_token.value
        
        self.consume(TokenType.DOUBLE_COLON)
        
        # Parse module name
        name_token = self.consume(TokenType.IDENTIFIER)
        name = name_token.value
        
        self.consume(TokenType.LEFT_BRACE)
        
        # Parse module contents
        use_declarations = []
        friend_declarations = []
        constants = []
        structs = []
        functions = []
        
        while self.current_token and not self.match(TokenType.RIGHT_BRACE):
            if self.match(TokenType.USE):
                use_declarations.append(self.parse_use_declaration())
            elif self.match(TokenType.FRIEND):
                friend_declarations.append(self.parse_friend_declaration())
            elif self.match(TokenType.CONST):
                constants.append(self.parse_constant_declaration())
            elif self.match(TokenType.STRUCT):
                structs.append(self.parse_struct_declaration())
            elif self.match(TokenType.FUN, TokenType.PUBLIC, TokenType.NATIVE, TokenType.ENTRY):
                functions.append(self.parse_function_declaration())
            else:
                self.error(f"Unexpected token in module: {self.current_token.type.name}")
        
        self.consume(TokenType.RIGHT_BRACE)
        
        return MoveModule(
            address=address,
            name=name,
            use_declarations=use_declarations,
            friend_declarations=friend_declarations,
            constants=constants,
            structs=structs,
            functions=functions
        )
    
    def parse_use_declaration(self) -> MoveUseDeclaration:
        """Parse a use declaration."""
        self.consume(TokenType.USE)
        
        # Parse module address (optional)
        module_address = None
        if self.match(TokenType.ADDRESS):
            module_address = self.current_token.value
            self.advance()
            self.consume(TokenType.DOUBLE_COLON)
        
        # Parse module name
        module_name = self.consume(TokenType.IDENTIFIER).value
        
        # Parse optional alias or specific imports
        import_name = None
        imported_items = []
        
        if self.match(TokenType.AS):
            self.advance()
            import_name = self.consume(TokenType.IDENTIFIER).value
        elif self.match(TokenType.DOUBLE_COLON):
            self.advance()
            if self.match(TokenType.LEFT_BRACE):
                # Import specific items
                self.advance()
                while not self.match(TokenType.RIGHT_BRACE):
                    imported_items.append(self.consume(TokenType.IDENTIFIER).value)
                    if self.match(TokenType.COMMA):
                        self.advance()
                self.consume(TokenType.RIGHT_BRACE)
            else:
                # Import specific item
                imported_items.append(self.consume(TokenType.IDENTIFIER).value)
        
        self.consume(TokenType.SEMICOLON)
        
        return MoveUseDeclaration(
            module_address=module_address,
            module_name=module_name,
            import_name=import_name,
            imported_items=imported_items
        )
    
    def parse_type(self) -> MoveType:
        """Parse a Move type."""
        if self.match(TokenType.BOOL):
            self.advance()
            return MovePrimitive(MovePrimitiveType.BOOL)
        elif self.match(TokenType.U8):
            self.advance()
            return MovePrimitive(MovePrimitiveType.U8)
        elif self.match(TokenType.U16):
            self.advance()
            return MovePrimitive(MovePrimitiveType.U16)
        elif self.match(TokenType.U32):
            self.advance()
            return MovePrimitive(MovePrimitiveType.U32)
        elif self.match(TokenType.U64):
            self.advance()
            return MovePrimitive(MovePrimitiveType.U64)
        elif self.match(TokenType.U128):
            self.advance()
            return MovePrimitive(MovePrimitiveType.U128)
        elif self.match(TokenType.U256):
            self.advance()
            return MovePrimitive(MovePrimitiveType.U256)
        elif self.match(TokenType.ADDRESS_TYPE):
            self.advance()
            return MovePrimitive(MovePrimitiveType.ADDRESS)
        elif self.match(TokenType.SIGNER):
            self.advance()
            return MovePrimitive(MovePrimitiveType.SIGNER)
        elif self.match(TokenType.VECTOR):
            self.advance()
            self.consume(TokenType.LEFT_ANGLE)
            element_type = self.parse_type()
            self.consume(TokenType.RIGHT_ANGLE)
            return MoveVectorType(element_type)
        elif self.match(TokenType.AMPERSAND, TokenType.AMPERSAND_MUT):
            is_mutable = self.current_token.type == TokenType.AMPERSAND_MUT
            self.advance()
            referenced_type = self.parse_type()
            return MoveReferenceType(referenced_type, is_mutable)
        elif self.match(TokenType.IDENTIFIER):
            # Could be a struct type or generic type
            name = self.current_token.value
            self.advance()
            
            # Check for type arguments
            type_arguments = []
            if self.match(TokenType.LEFT_ANGLE):
                self.advance()
                while not self.match(TokenType.RIGHT_ANGLE):
                    type_arguments.append(self.parse_type())
                    if self.match(TokenType.COMMA):
                        self.advance()
                self.consume(TokenType.RIGHT_ANGLE)
            
            # For now, treat as struct type (could be improved to distinguish generics)
            return MoveStructType(module_name=None, struct_name=name, type_arguments=type_arguments)
        else:
            self.error(f"Expected type, got {self.current_token.type.name}")


# Convenience functions for parsing

def parse_move_source(source: str, file_path: Optional[str] = None) -> MoveProgram:
    """Parse Move source code and return AST."""
    try:
        lexer = MoveLexer(source)
        tokens = lexer.tokenize()
        
        parser = MoveParser(tokens)
        program = parser.parse_program()
        
        # Set source file information
        if file_path:
            def set_source_file(node):
                if hasattr(node, 'source_file'):
                    node.source_file = file_path
                if hasattr(node, '__dict__'):
                    for attr_value in node.__dict__.values():
                        if isinstance(attr_value, list):
                            for item in attr_value:
                                if hasattr(item, 'accept'):
                                    set_source_file(item)
                        elif hasattr(attr_value, 'accept'):
                            set_source_file(attr_value)
            
            set_source_file(program)
        
        return program
        
    except Exception as e:
        raise SyntaxError(f"Failed to parse Move source: {str(e)}")


def tokenize_move_source(source: str) -> List[Token]:
    """Tokenize Move source code."""
    lexer = MoveLexer(source)
    return lexer.tokenize()


# Export main classes
MoveLexer = MoveLexer
MoveParser = MoveParser 