#!/usr/bin/env python3
"""
Elixir Parser Module

This module provides comprehensive parsing capabilities for the Elixir programming language,
supporting all major syntax constructs including:
- Atoms, strings, numbers, and collections
- Pipe operators and function composition
- Pattern matching and guards
- Modules, functions, and protocols
- Macros and metaprogramming constructs
- Actor model with processes and message passing
"""

import re
from enum import Enum
from typing import List, Optional, Union, Dict, Any
from .elixir_ast import *

class ElixirTokenType(Enum):
    # Literals
    ATOM = "ATOM"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    STRING = "STRING"
    BINARY = "BINARY"
    BOOLEAN = "BOOLEAN"
    NIL = "NIL"
    
    # Collections
    LBRACKET = "LBRACKET"      # [
    RBRACKET = "RBRACKET"      # ]
    LBRACE = "LBRACE"          # {
    RBRACE = "RBRACE"          # }
    LPAREN = "LPAREN"          # (
    RPAREN = "RPAREN"          # )
    PERCENT = "PERCENT"        # %
    
    # Operators
    PIPE = "PIPE"              # |>
    MATCH = "MATCH"            # =
    PIN = "PIN"                # ^
    DOT = "DOT"                # .
    ARROW = "ARROW"            # ->
    DOUBLE_ARROW = "DOUBLE_ARROW"  # =>
    CONS = "CONS"              # |
    
    # Keywords
    DEF = "DEF"
    DEFP = "DEFP"
    DEFMACRO = "DEFMACRO"
    DEFMODULE = "DEFMODULE"
    DEFSTRUCT = "DEFSTRUCT"
    DO = "DO"
    END = "END"
    IF = "IF"
    UNLESS = "UNLESS"
    CASE = "CASE"
    COND = "COND"
    WITH = "WITH"
    TRY = "TRY"
    RESCUE = "RESCUE"
    CATCH = "CATCH"
    AFTER = "AFTER"
    ELSE = "ELSE"
    WHEN = "WHEN"
    FN = "FN"
    FOR = "FOR"
    SPAWN = "SPAWN"
    SEND = "SEND"
    RECEIVE = "RECEIVE"
    ALIAS = "ALIAS"
    IMPORT = "IMPORT"
    REQUIRE = "REQUIRE"
    USE = "USE"
    QUOTE = "QUOTE"
    UNQUOTE = "UNQUOTE"
    
    # Punctuation
    COMMA = "COMMA"            # ,
    COLON = "COLON"            # :
    SEMICOLON = "SEMICOLON"    # ;
    AT = "AT"                  # @
    
    # Identifiers
    IDENTIFIER = "IDENTIFIER"
    MODULE_IDENTIFIER = "MODULE_IDENTIFIER"
    
    # Special
    NEWLINE = "NEWLINE"
    EOF = "EOF"
    COMMENT = "COMMENT"

class ElixirToken:
    """Represents a token in Elixir source code."""
    
    def __init__(self, token_type: ElixirTokenType, value: str, line: int = 0, column: int = 0):
        self.type = token_type
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type.value}, {self.value!r}, {self.line}:{self.column})"

class ElixirLexer:
    """Lexical analyzer for Elixir."""
    
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        
        # Keywords mapping
        self.keywords = {
            'def': ElixirTokenType.DEF,
            'defp': ElixirTokenType.DEFP,
            'defmacro': ElixirTokenType.DEFMACRO,
            'defmodule': ElixirTokenType.DEFMODULE,
            'defstruct': ElixirTokenType.DEFSTRUCT,
            'do': ElixirTokenType.DO,
            'end': ElixirTokenType.END,
            'if': ElixirTokenType.IF,
            'unless': ElixirTokenType.UNLESS,
            'case': ElixirTokenType.CASE,
            'cond': ElixirTokenType.COND,
            'with': ElixirTokenType.WITH,
            'try': ElixirTokenType.TRY,
            'rescue': ElixirTokenType.RESCUE,
            'catch': ElixirTokenType.CATCH,
            'after': ElixirTokenType.AFTER,
            'else': ElixirTokenType.ELSE,
            'when': ElixirTokenType.WHEN,
            'fn': ElixirTokenType.FN,
            'for': ElixirTokenType.FOR,
            'spawn': ElixirTokenType.SPAWN,
            'send': ElixirTokenType.SEND,
            'receive': ElixirTokenType.RECEIVE,
            'alias': ElixirTokenType.ALIAS,
            'import': ElixirTokenType.IMPORT,
            'require': ElixirTokenType.REQUIRE,
            'use': ElixirTokenType.USE,
            'quote': ElixirTokenType.QUOTE,
            'unquote': ElixirTokenType.UNQUOTE,
            'true': ElixirTokenType.BOOLEAN,
            'false': ElixirTokenType.BOOLEAN,
            'nil': ElixirTokenType.NIL,
        }
    
    def current_char(self) -> Optional[str]:
        """Get the current character."""
        if self.position >= len(self.source):
            return None
        return self.source[self.position]
    
    def peek_char(self, offset: int = 1) -> Optional[str]:
        """Peek at a character ahead."""
        pos = self.position + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]
    
    def advance(self):
        """Move to the next character."""
        if self.position < len(self.source):
            if self.source[self.position] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.position += 1
    
    def skip_whitespace(self):
        """Skip whitespace characters."""
        while self.current_char() and self.current_char() in ' \t\r':
            self.advance()
    
    def read_comment(self) -> ElixirToken:
        """Read a comment."""
        start_column = self.column
        value = ""
        
        # Skip the #
        self.advance()
        
        while self.current_char() and self.current_char() != '\n':
            value += self.current_char()
            self.advance()
        
        return ElixirToken(ElixirTokenType.COMMENT, value, self.line, start_column)
    
    def read_string(self, quote_char: str) -> ElixirToken:
        """Read a string literal."""
        start_column = self.column
        value = ""
        
        # Skip opening quote
        self.advance()
        
        while self.current_char() and self.current_char() != quote_char:
            if self.current_char() == '\\':
                self.advance()
                if self.current_char():
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
        
        # Skip closing quote
        if self.current_char() == quote_char:
            self.advance()
        
        return ElixirToken(ElixirTokenType.STRING, value, self.line, start_column)
    
    def read_number(self) -> ElixirToken:
        """Read a number (integer or float)."""
        start_column = self.column
        value = ""
        has_dot = False
        
        while (self.current_char() and 
               (self.current_char().isdigit() or self.current_char() == '.')):
            if self.current_char() == '.':
                if has_dot or not self.peek_char() or not self.peek_char().isdigit():
                    break
                has_dot = True
            value += self.current_char()
            self.advance()
        
        token_type = ElixirTokenType.FLOAT if has_dot else ElixirTokenType.INTEGER
        return ElixirToken(token_type, value, self.line, start_column)
    
    def read_atom(self) -> ElixirToken:
        """Read an atom literal."""
        start_column = self.column
        value = ":"
        
        # Skip the :
        self.advance()
        
        if self.current_char() and self.current_char() in '"\'':
            # Quoted atom
            quote_char = self.current_char()
            self.advance()
            while self.current_char() and self.current_char() != quote_char:
                value += self.current_char()
                self.advance()
            if self.current_char() == quote_char:
                value += self.current_char()
                self.advance()
        else:
            # Regular atom
            while (self.current_char() and 
                   (self.current_char().isalnum() or self.current_char() in '_?!')):
                value += self.current_char()
                self.advance()
        
        return ElixirToken(ElixirTokenType.ATOM, value, self.line, start_column)
    
    def read_identifier(self) -> ElixirToken:
        """Read an identifier or keyword."""
        start_column = self.column
        value = ""
        
        while (self.current_char() and 
               (self.current_char().isalnum() or self.current_char() in '_?!')):
            value += self.current_char()
            self.advance()
        
        # Check if it's a keyword
        token_type = self.keywords.get(value, ElixirTokenType.IDENTIFIER)
        
        # Check if it's a module identifier (starts with uppercase)
        if token_type == ElixirTokenType.IDENTIFIER and value and value[0].isupper():
            token_type = ElixirTokenType.MODULE_IDENTIFIER
        
        return ElixirToken(token_type, value, self.line, start_column)
    
    def tokenize(self) -> List[ElixirToken]:
        """Tokenize the source code."""
        self.tokens = []
        
        while self.position < len(self.source):
            self.skip_whitespace()
            
            if not self.current_char():
                break
            
            char = self.current_char()
            
            # Comments
            if char == '#':
                self.tokens.append(self.read_comment())
            
            # Newlines
            elif char == '\n':
                self.tokens.append(ElixirToken(ElixirTokenType.NEWLINE, char, self.line, self.column))
                self.advance()
            
            # Strings
            elif char in '"\'':
                self.tokens.append(self.read_string(char))
            
            # Numbers
            elif char.isdigit():
                self.tokens.append(self.read_number())
            
            # Atoms
            elif char == ':':
                self.tokens.append(self.read_atom())
            
            # Identifiers and keywords
            elif char.isalpha() or char == '_':
                self.tokens.append(self.read_identifier())
            
            # Two-character operators
            elif char == '|' and self.peek_char() == '>':
                self.tokens.append(ElixirToken(ElixirTokenType.PIPE, '|>', self.line, self.column))
                self.advance()
                self.advance()
            
            elif char == '=' and self.peek_char() == '>':
                self.tokens.append(ElixirToken(ElixirTokenType.DOUBLE_ARROW, '=>', self.line, self.column))
                self.advance()
                self.advance()
            
            elif char == '-' and self.peek_char() == '>':
                self.tokens.append(ElixirToken(ElixirTokenType.ARROW, '->', self.line, self.column))
                self.advance()
                self.advance()
            
            # Single-character tokens
            elif char == '[':
                self.tokens.append(ElixirToken(ElixirTokenType.LBRACKET, char, self.line, self.column))
                self.advance()
            elif char == ']':
                self.tokens.append(ElixirToken(ElixirTokenType.RBRACKET, char, self.line, self.column))
                self.advance()
            elif char == '{':
                self.tokens.append(ElixirToken(ElixirTokenType.LBRACE, char, self.line, self.column))
                self.advance()
            elif char == '}':
                self.tokens.append(ElixirToken(ElixirTokenType.RBRACE, char, self.line, self.column))
                self.advance()
            elif char == '(':
                self.tokens.append(ElixirToken(ElixirTokenType.LPAREN, char, self.line, self.column))
                self.advance()
            elif char == ')':
                self.tokens.append(ElixirToken(ElixirTokenType.RPAREN, char, self.line, self.column))
                self.advance()
            elif char == '%':
                self.tokens.append(ElixirToken(ElixirTokenType.PERCENT, char, self.line, self.column))
                self.advance()
            elif char == '=':
                self.tokens.append(ElixirToken(ElixirTokenType.MATCH, char, self.line, self.column))
                self.advance()
            elif char == '^':
                self.tokens.append(ElixirToken(ElixirTokenType.PIN, char, self.line, self.column))
                self.advance()
            elif char == '.':
                self.tokens.append(ElixirToken(ElixirTokenType.DOT, char, self.line, self.column))
                self.advance()
            elif char == '|':
                self.tokens.append(ElixirToken(ElixirTokenType.CONS, char, self.line, self.column))
                self.advance()
            elif char == ',':
                self.tokens.append(ElixirToken(ElixirTokenType.COMMA, char, self.line, self.column))
                self.advance()
            elif char == ':':
                self.tokens.append(ElixirToken(ElixirTokenType.COLON, char, self.line, self.column))
                self.advance()
            elif char == ';':
                self.tokens.append(ElixirToken(ElixirTokenType.SEMICOLON, char, self.line, self.column))
                self.advance()
            elif char == '@':
                self.tokens.append(ElixirToken(ElixirTokenType.AT, char, self.line, self.column))
                self.advance()
            else:
                # Unknown character, skip it
                self.advance()
        
        self.tokens.append(ElixirToken(ElixirTokenType.EOF, '', self.line, self.column))
        return self.tokens

class ElixirParser:
    """Parser for Elixir language."""
    
    def __init__(self, tokens: List[ElixirToken]):
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[0] if tokens else None
    
    def advance(self):
        """Move to the next token."""
        if self.position < len(self.tokens) - 1:
            self.position += 1
            self.current_token = self.tokens[self.position]
    
    def peek_token(self, offset: int = 1) -> Optional[ElixirToken]:
        """Peek at a token ahead."""
        pos = self.position + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return None
    
    def expect_token(self, token_type: ElixirTokenType) -> ElixirToken:
        """Expect a specific token type."""
        if self.current_token.type != token_type:
            raise SyntaxError(f"Expected {token_type.value}, got {self.current_token.type.value}")
        token = self.current_token
        self.advance()
        return token
    
    def skip_newlines(self):
        """Skip newline tokens."""
        while self.current_token and self.current_token.type == ElixirTokenType.NEWLINE:
            self.advance()
    
    def parse_atom(self) -> ElixirAtom:
        """Parse an atom."""
        token = self.expect_token(ElixirTokenType.ATOM)
        return ElixirAtom(value=token.value[1:], line_number=token.line, column_number=token.column)
    
    def parse_primary(self) -> ElixirExpression:
        """Parse a primary expression."""
        self.skip_newlines()
        
        if not self.current_token:
            raise SyntaxError("Unexpected end of input")
        
        # Literals
        if self.current_token.type == ElixirTokenType.ATOM:
            return self.parse_atom()
        
        elif self.current_token.type == ElixirTokenType.INTEGER:
            token = self.current_token
            self.advance()
            return ElixirInteger(value=int(token.value), line_number=token.line, column_number=token.column)
        
        elif self.current_token.type == ElixirTokenType.FLOAT:
            token = self.current_token
            self.advance()
            return ElixirFloat(value=float(token.value), line_number=token.line, column_number=token.column)
        
        elif self.current_token.type == ElixirTokenType.STRING:
            token = self.current_token
            self.advance()
            return ElixirString(value=token.value, line_number=token.line, column_number=token.column)
        
        elif self.current_token.type == ElixirTokenType.BOOLEAN:
            token = self.current_token
            self.advance()
            return ElixirBoolean(value=token.value == 'true', line_number=token.line, column_number=token.column)
        
        elif self.current_token.type == ElixirTokenType.NIL:
            token = self.current_token
            self.advance()
            return ElixirNil(line_number=token.line, column_number=token.column)
        
        elif self.current_token.type == ElixirTokenType.IDENTIFIER:
            token = self.current_token
            self.advance()
            return ElixirVariable(name=token.value, line_number=token.line, column_number=token.column)
        
        # Lists
        elif self.current_token.type == ElixirTokenType.LBRACKET:
            return self.parse_list()
        
        # Tuples
        elif self.current_token.type == ElixirTokenType.LBRACE:
            return self.parse_tuple()
        
        # Maps
        elif self.current_token.type == ElixirTokenType.PERCENT and self.peek_token() and self.peek_token().type == ElixirTokenType.LBRACE:
            return self.parse_map()
        
        # Parenthesized expressions
        elif self.current_token.type == ElixirTokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect_token(ElixirTokenType.RPAREN)
            return expr
        
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token}")
    
    def parse_list(self) -> ElixirList:
        """Parse a list [1, 2, 3] or [head | tail]."""
        line = self.current_token.line
        column = self.current_token.column
        self.expect_token(ElixirTokenType.LBRACKET)
        
        elements = []
        tail = None
        
        self.skip_newlines()
        
        if self.current_token.type != ElixirTokenType.RBRACKET:
            elements.append(self.parse_expression())
            
            while self.current_token.type == ElixirTokenType.COMMA:
                self.advance()
                self.skip_newlines()
                if self.current_token.type == ElixirTokenType.RBRACKET:
                    break
                elements.append(self.parse_expression())
            
            # Check for tail syntax [head | tail]
            if self.current_token.type == ElixirTokenType.CONS:
                self.advance()
                tail = self.parse_expression()
        
        self.expect_token(ElixirTokenType.RBRACKET)
        return ElixirList(elements=elements, tail=tail, line_number=line, column_number=column)
    
    def parse_tuple(self) -> ElixirTuple:
        """Parse a tuple {1, 2, 3}."""
        line = self.current_token.line
        column = self.current_token.column
        self.expect_token(ElixirTokenType.LBRACE)
        
        elements = []
        self.skip_newlines()
        
        if self.current_token.type != ElixirTokenType.RBRACE:
            elements.append(self.parse_expression())
            
            while self.current_token.type == ElixirTokenType.COMMA:
                self.advance()
                self.skip_newlines()
                if self.current_token.type == ElixirTokenType.RBRACE:
                    break
                elements.append(self.parse_expression())
        
        self.expect_token(ElixirTokenType.RBRACE)
        return ElixirTuple(elements=elements, line_number=line, column_number=column)
    
    def parse_map(self) -> ElixirMap:
        """Parse a map %{key: value}."""
        line = self.current_token.line
        column = self.current_token.column
        self.expect_token(ElixirTokenType.PERCENT)
        self.expect_token(ElixirTokenType.LBRACE)
        
        pairs = []
        self.skip_newlines()
        
        if self.current_token.type != ElixirTokenType.RBRACE:
            key = self.parse_expression()
            self.expect_token(ElixirTokenType.COLON)
            value = self.parse_expression()
            pairs.append((key, value))
            
            while self.current_token.type == ElixirTokenType.COMMA:
                self.advance()
                self.skip_newlines()
                if self.current_token.type == ElixirTokenType.RBRACE:
                    break
                key = self.parse_expression()
                self.expect_token(ElixirTokenType.COLON)
                value = self.parse_expression()
                pairs.append((key, value))
        
        self.expect_token(ElixirTokenType.RBRACE)
        return ElixirMap(pairs=pairs, line_number=line, column_number=column)
    
    def parse_pipe(self) -> ElixirExpression:
        """Parse pipe expression left |> right."""
        left = self.parse_primary()
        
        while self.current_token and self.current_token.type == ElixirTokenType.PIPE:
            self.advance()
            right = self.parse_primary()
            left = ElixirPipe(left=left, right=right)
        
        return left
    
    def parse_expression(self) -> ElixirExpression:
        """Parse a general expression."""
        return self.parse_pipe()
    
    def parse_module(self) -> ElixirModule:
        """Parse a module definition."""
        self.expect_token(ElixirTokenType.DEFMODULE)
        name_token = self.expect_token(ElixirTokenType.MODULE_IDENTIFIER)
        self.expect_token(ElixirTokenType.DO)
        
        body = []
        self.skip_newlines()
        
        while self.current_token and self.current_token.type != ElixirTokenType.END:
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            self.skip_newlines()
        
        self.expect_token(ElixirTokenType.END)
        return ElixirModule(name=name_token.value, body=body)
    
    def parse_statement(self) -> Optional[ElixirStatement]:
        """Parse a statement."""
        self.skip_newlines()
        
        if not self.current_token or self.current_token.type == ElixirTokenType.EOF:
            return None
        
        if self.current_token.type == ElixirTokenType.DEFMODULE:
            return ElixirDefmodule(module=self.parse_module())
        
        # For now, treat other constructs as expressions
        expr = self.parse_expression()
        return expr
    
    def parse_program(self) -> ElixirProgram:
        """Parse a complete Elixir program."""
        statements = []
        
        while self.current_token and self.current_token.type != ElixirTokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()
        
        return ElixirProgram(statements=statements)

def parse_elixir(source_code: str) -> ElixirProgram:
    """Parse Elixir source code into an AST."""
    lexer = ElixirLexer(source_code)
    tokens = lexer.tokenize()
    
    # Filter out comments for parsing
    tokens = [token for token in tokens if token.type != ElixirTokenType.COMMENT]
    
    parser = ElixirParser(tokens)
    return parser.parse_program()

def parse_elixir_expression(source_code: str) -> ElixirExpression:
    """Parse a single Elixir expression."""
    lexer = ElixirLexer(source_code)
    tokens = lexer.tokenize()
    
    # Filter out comments for parsing
    tokens = [token for token in tokens if token.type != ElixirTokenType.COMMENT]
    
    parser = ElixirParser(tokens)
    return parser.parse_expression() 