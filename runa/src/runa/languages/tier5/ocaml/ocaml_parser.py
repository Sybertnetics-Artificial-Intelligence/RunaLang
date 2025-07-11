#!/usr/bin/env python3
"""
OCaml Parser Implementation
"""

from typing import List, Optional, Dict, Any, Union, Tuple
from dataclasses import dataclass
from enum import Enum, auto
import re

from .ocaml_ast import *


class OcamlTokenType(Enum):
    """OCaml token types."""
    # Literals
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    CHAR = auto()
    BOOLEAN = auto()
    
    # Identifiers
    IDENTIFIER = auto()
    CONSTRUCTOR_ID = auto()
    
    # Keywords
    LET = auto()
    REC = auto()
    IN = auto()
    IF = auto()
    THEN = auto()
    ELSE = auto()
    MATCH = auto()
    WITH = auto()
    FUNCTION = auto()
    FUN = auto()
    TYPE = auto()
    MODULE = auto()
    
    # Operators and punctuation
    ARROW = auto()        # ->
    DOUBLE_ARROW = auto() # =>
    EQUALS = auto()       # =
    PIPE = auto()         # |
    SEMICOLON = auto()    # ;
    COMMA = auto()        # ,
    LPAREN = auto()       # (
    RPAREN = auto()       # )
    LBRACKET = auto()     # [
    RBRACKET = auto()     # ]
    LBRACE = auto()       # {
    RBRACE = auto()       # }
    DOT = auto()          # .
    
    # Special
    EOF = auto()
    NEWLINE = auto()


@dataclass
class OcamlToken:
    """OCaml token."""
    type: OcamlTokenType
    value: str
    line: int
    column: int


class OcamlLexer:
    """OCaml lexer."""
    
    KEYWORDS = {
        'let': OcamlTokenType.LET,
        'rec': OcamlTokenType.REC,
        'in': OcamlTokenType.IN,
        'if': OcamlTokenType.IF,
        'then': OcamlTokenType.THEN,
        'else': OcamlTokenType.ELSE,
        'match': OcamlTokenType.MATCH,
        'with': OcamlTokenType.WITH,
        'function': OcamlTokenType.FUNCTION,
        'fun': OcamlTokenType.FUN,
        'type': OcamlTokenType.TYPE,
        'module': OcamlTokenType.MODULE,
        'true': OcamlTokenType.BOOLEAN,
        'false': OcamlTokenType.BOOLEAN,
    }
    
    def __init__(self, text: str):
        self.text = text
        self.position = 0
        self.line = 1
        self.column = 1
    
    def current_char(self) -> Optional[str]:
        if self.position >= len(self.text):
            return None
        return self.text[self.position]
    
    def advance(self):
        if self.position < len(self.text) and self.text[self.position] == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        self.position += 1
    
    def skip_whitespace(self):
        while self.current_char() and self.current_char() in ' \t\r':
            self.advance()
    
    def read_string(self) -> str:
        self.advance()  # Skip opening quote
        value = ""
        while self.current_char() and self.current_char() != '"':
            if self.current_char() == '\\':
                self.advance()
                if self.current_char():
                    value += self.current_char()
                    self.advance()
            else:
                value += self.current_char()
                self.advance()
        if self.current_char() == '"':
            self.advance()
        return value
    
    def read_number(self) -> Tuple[str, OcamlTokenType]:
        value = ""
        token_type = OcamlTokenType.INTEGER
        
        while self.current_char() and (self.current_char().isdigit() or self.current_char() == '.'):
            if self.current_char() == '.':
                token_type = OcamlTokenType.FLOAT
            value += self.current_char()
            self.advance()
        
        return value, token_type
    
    def read_identifier(self) -> Tuple[str, OcamlTokenType]:
        value = ""
        while (self.current_char() and 
               (self.current_char().isalnum() or self.current_char() in '_\'')):
            value += self.current_char()
            self.advance()
        
        # Check if it's a keyword
        if value in self.KEYWORDS:
            return value, self.KEYWORDS[value]
        elif value[0].isupper():
            return value, OcamlTokenType.CONSTRUCTOR_ID
        else:
            return value, OcamlTokenType.IDENTIFIER
    
    def tokenize(self) -> List[OcamlToken]:
        tokens = []
        
        while self.position < len(self.text):
            char = self.current_char()
            
            if char == '\n':
                tokens.append(OcamlToken(OcamlTokenType.NEWLINE, char, self.line, self.column))
                self.advance()
                continue
            
            if char in ' \t\r':
                self.skip_whitespace()
                continue
            
            # Comments
            if char == '(' and self.position + 1 < len(self.text) and self.text[self.position + 1] == '*':
                self.advance()  # (
                self.advance()  # *
                while (self.position + 1 < len(self.text) and 
                       not (self.text[self.position] == '*' and self.text[self.position + 1] == ')')):
                    self.advance()
                if self.position + 1 < len(self.text):
                    self.advance()  # *
                    self.advance()  # )
                continue
            
            # Strings
            if char == '"':
                value = self.read_string()
                tokens.append(OcamlToken(OcamlTokenType.STRING, value, self.line, self.column))
                continue
            
            # Numbers
            if char.isdigit():
                value, token_type = self.read_number()
                tokens.append(OcamlToken(token_type, value, self.line, self.column))
                continue
            
            # Identifiers
            if char.isalpha() or char == '_':
                value, token_type = self.read_identifier()
                tokens.append(OcamlToken(token_type, value, self.line, self.column))
                continue
            
            # Two-character operators
            if (self.position + 1 < len(self.text)):
                two_char = char + self.text[self.position + 1]
                if two_char == '->':
                    tokens.append(OcamlToken(OcamlTokenType.ARROW, two_char, self.line, self.column))
                    self.advance()
                    self.advance()
                    continue
                elif two_char == '=>':
                    tokens.append(OcamlToken(OcamlTokenType.DOUBLE_ARROW, two_char, self.line, self.column))
                    self.advance()
                    self.advance()
                    continue
            
            # Single character tokens
            if char == '(':
                tokens.append(OcamlToken(OcamlTokenType.LPAREN, char, self.line, self.column))
                self.advance()
            elif char == ')':
                tokens.append(OcamlToken(OcamlTokenType.RPAREN, char, self.line, self.column))
                self.advance()
            elif char == '[':
                tokens.append(OcamlToken(OcamlTokenType.LBRACKET, char, self.line, self.column))
                self.advance()
            elif char == ']':
                tokens.append(OcamlToken(OcamlTokenType.RBRACKET, char, self.line, self.column))
                self.advance()
            elif char == '{':
                tokens.append(OcamlToken(OcamlTokenType.LBRACE, char, self.line, self.column))
                self.advance()
            elif char == '}':
                tokens.append(OcamlToken(OcamlTokenType.RBRACE, char, self.line, self.column))
                self.advance()
            elif char == '=':
                tokens.append(OcamlToken(OcamlTokenType.EQUALS, char, self.line, self.column))
                self.advance()
            elif char == '|':
                tokens.append(OcamlToken(OcamlTokenType.PIPE, char, self.line, self.column))
                self.advance()
            elif char == ';':
                tokens.append(OcamlToken(OcamlTokenType.SEMICOLON, char, self.line, self.column))
                self.advance()
            elif char == ',':
                tokens.append(OcamlToken(OcamlTokenType.COMMA, char, self.line, self.column))
                self.advance()
            elif char == '.':
                tokens.append(OcamlToken(OcamlTokenType.DOT, char, self.line, self.column))
                self.advance()
            else:
                self.advance()  # Skip unknown characters
        
        tokens.append(OcamlToken(OcamlTokenType.EOF, '', self.line, self.column))
        return tokens


class OcamlParser:
    """OCaml parser."""
    
    def __init__(self, tokens: List[OcamlToken]):
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[0] if tokens else None
    
    def advance(self):
        if self.position < len(self.tokens) - 1:
            self.position += 1
            self.current_token = self.tokens[self.position]
    
    def match(self, token_type: OcamlTokenType) -> bool:
        return self.current_token and self.current_token.type == token_type
    
    def consume(self, token_type: OcamlTokenType) -> OcamlToken:
        if not self.match(token_type):
            raise SyntaxError(f"Expected {token_type}, got {self.current_token}")
        token = self.current_token
        self.advance()
        return token
    
    def skip_newlines(self):
        while self.match(OcamlTokenType.NEWLINE):
            self.advance()
    
    def parse_module(self) -> OcamlModule:
        """Parse OCaml module."""
        declarations = []
        
        while not self.match(OcamlTokenType.EOF):
            self.skip_newlines()
            if self.match(OcamlTokenType.EOF):
                break
            declarations.append(self.parse_declaration())
            self.skip_newlines()
        
        return OcamlModule(declarations=declarations)
    
    def parse_declaration(self) -> OcamlDeclaration:
        """Parse declaration."""
        if self.match(OcamlTokenType.LET):
            return self.parse_value_declaration()
        elif self.match(OcamlTokenType.TYPE):
            return self.parse_type_declaration()
        else:
            # Default to value declaration
            return self.parse_value_declaration()
    
    def parse_value_declaration(self) -> OcamlValueDeclaration:
        """Parse value declaration."""
        self.consume(OcamlTokenType.LET)
        
        recursive = False
        if self.match(OcamlTokenType.REC):
            recursive = True
            self.advance()
        
        pattern = self.parse_pattern()
        self.consume(OcamlTokenType.EQUALS)
        expression = self.parse_expression()
        
        return OcamlValueDeclaration(pattern=pattern, expression=expression, recursive=recursive)
    
    def parse_type_declaration(self) -> OcamlTypeDeclaration:
        """Parse type declaration."""
        self.consume(OcamlTokenType.TYPE)
        name = self.consume(OcamlTokenType.IDENTIFIER).value
        
        # Simple type declaration
        parameters = []
        definition = None
        
        if self.match(OcamlTokenType.EQUALS):
            self.advance()
            definition = self.parse_type()
        
        return OcamlTypeDeclaration(name=name, parameters=parameters, definition=definition)
    
    def parse_expression(self) -> OcamlExpression:
        """Parse expression."""
        return self.parse_let_expression()
    
    def parse_let_expression(self) -> OcamlExpression:
        """Parse let expression."""
        if self.match(OcamlTokenType.LET):
            self.advance()
            
            recursive = False
            if self.match(OcamlTokenType.REC):
                recursive = True
                self.advance()
            
            pattern = self.parse_pattern()
            self.consume(OcamlTokenType.EQUALS)
            value = self.parse_expression()
            self.consume(OcamlTokenType.IN)
            body = self.parse_expression()
            
            return OcamlLet(pattern=pattern, value=value, body=body, recursive=recursive)
        
        return self.parse_if_expression()
    
    def parse_if_expression(self) -> OcamlExpression:
        """Parse if expression."""
        if self.match(OcamlTokenType.IF):
            self.advance()
            condition = self.parse_expression()
            self.consume(OcamlTokenType.THEN)
            then_expr = self.parse_expression()
            
            else_expr = None
            if self.match(OcamlTokenType.ELSE):
                self.advance()
                else_expr = self.parse_expression()
            
            return OcamlIf(condition=condition, then_expr=then_expr, else_expr=else_expr)
        
        return self.parse_match_expression()
    
    def parse_match_expression(self) -> OcamlExpression:
        """Parse match expression."""
        if self.match(OcamlTokenType.MATCH):
            self.advance()
            expression = self.parse_expression()
            self.consume(OcamlTokenType.WITH)
            
            cases = []
            # Parse match cases (simplified)
            
            return OcamlMatch(expression=expression, cases=cases)
        
        return self.parse_application()
    
    def parse_application(self) -> OcamlExpression:
        """Parse function application."""
        left = self.parse_primary()
        
        args = []
        while (not self.match(OcamlTokenType.EOF) and
               not self.match(OcamlTokenType.IN) and
               not self.match(OcamlTokenType.THEN) and
               not self.match(OcamlTokenType.ELSE) and
               not self.match(OcamlTokenType.RPAREN)):
            args.append(self.parse_primary())
        
        if args:
            return OcamlApplication(function=left, arguments=args)
        return left
    
    def parse_primary(self) -> OcamlExpression:
        """Parse primary expression."""
        if self.match(OcamlTokenType.INTEGER):
            value = int(self.current_token.value)
            self.advance()
            return OcamlLiteral(value=value, literal_type="int")
        elif self.match(OcamlTokenType.FLOAT):
            value = float(self.current_token.value)
            self.advance()
            return OcamlLiteral(value=value, literal_type="float")
        elif self.match(OcamlTokenType.STRING):
            value = self.current_token.value
            self.advance()
            return OcamlLiteral(value=value, literal_type="string")
        elif self.match(OcamlTokenType.BOOLEAN):
            value = self.current_token.value == "true"
            self.advance()
            return OcamlLiteral(value=value, literal_type="bool")
        elif self.match(OcamlTokenType.IDENTIFIER):
            name = self.current_token.value
            self.advance()
            return OcamlIdentifier(name=name)
        elif self.match(OcamlTokenType.CONSTRUCTOR_ID):
            name = self.current_token.value
            self.advance()
            return OcamlConstructor(name=name)
        elif self.match(OcamlTokenType.LPAREN):
            self.advance()
            expr = self.parse_expression()
            self.consume(OcamlTokenType.RPAREN)
            return expr
        elif self.match(OcamlTokenType.LBRACKET):
            self.advance()
            elements = []
            
            if not self.match(OcamlTokenType.RBRACKET):
                elements.append(self.parse_expression())
                while self.match(OcamlTokenType.SEMICOLON):
                    self.advance()
                    elements.append(self.parse_expression())
            
            self.consume(OcamlTokenType.RBRACKET)
            return OcamlList(elements=elements)
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token}")
    
    def parse_pattern(self) -> OcamlPattern:
        """Parse pattern."""
        if self.match(OcamlTokenType.IDENTIFIER):
            name = self.current_token.value
            self.advance()
            return OcamlVariablePattern(name=name)
        elif self.match(OcamlTokenType.CONSTRUCTOR_ID):
            name = self.current_token.value
            self.advance()
            return OcamlConstructorPattern(constructor=name, patterns=[])
        else:
            return OcamlWildcardPattern()
    
    def parse_type(self) -> OcamlType:
        """Parse type expression."""
        if self.match(OcamlTokenType.IDENTIFIER):
            name = self.current_token.value
            self.advance()
            return OcamlTypeVariable(name=name)
        elif self.match(OcamlTokenType.CONSTRUCTOR_ID):
            name = self.current_token.value
            self.advance()
            return OcamlTypeConstructor(name=name)
        else:
            return OcamlTypeVariable(name="'a")


def parse_ocaml(source_code: str) -> OcamlModule:
    """Parse OCaml source code."""
    lexer = OcamlLexer(source_code)
    tokens = lexer.tokenize()
    parser = OcamlParser(tokens)
    return parser.parse_module()


__all__ = [
    "OcamlTokenType", "OcamlToken", "OcamlLexer", "OcamlParser", "parse_ocaml"
] 