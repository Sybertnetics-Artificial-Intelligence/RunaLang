"""
LIGO Parser for the high-level smart contract language on Tezos.

This module provides lexical analysis and parsing capabilities for LIGO,
supporting both JsLIGO and CameLIGO syntax variants.
"""

import re
from typing import List, Optional, Union, Dict, Any
from enum import Enum
from .ligo_ast import *


class TokenType(Enum):
    """Token types for LIGO lexical analysis."""
    # Literals
    INTEGER = "INTEGER"
    STRING = "STRING"
    BYTES = "BYTES"
    
    # Keywords
    TYPE = "type"
    CONST = "const"
    LET = "let"
    FUNCTION = "function"
    ENTRY = "@entry"
    EXPORT = "export"
    IMPORT = "import"
    NAMESPACE = "namespace"
    IF = "if"
    ELSE = "else"
    MATCH = "match"
    WHEN = "when"
    RETURN = "return"
    FAILWITH = "failwith"
    
    # Types
    TYPE_NAME = "TYPE_NAME"
    
    # Operators
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    ASSIGN = "="
    ARROW = "=>"
    EQUAL = "=="
    NOT_EQUAL = "!="
    LESS = "<"
    GREATER = ">"
    LESS_EQUAL = "<="
    GREATER_EQUAL = ">="
    AND = "&&"
    OR = "||"
    NOT = "!"
    
    # Delimiters
    LBRACE = "{"
    RBRACE = "}"
    LPAREN = "("
    RPAREN = ")"
    LBRACKET = "["
    RBRACKET = "]"
    SEMICOLON = ";"
    COMMA = ","
    DOT = "."
    COLON = ":"
    PIPE = "|"
    
    # Special
    IDENTIFIER = "IDENTIFIER"
    BUILTIN = "BUILTIN"
    EOF = "EOF"
    NEWLINE = "NEWLINE"


class Token:
    """Represents a token in LIGO source code."""
    
    def __init__(self, type_: TokenType, value: str, line: int = 1, column: int = 1):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type.value}, '{self.value}', {self.line}:{self.column})"


class LigoLexer:
    """Lexer for LIGO language."""
    
    def __init__(self, source: str, syntax: LigoSyntax = LigoSyntax.JSLIGO):
        self.source = source
        self.syntax = syntax
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        
        # Keywords based on syntax
        if syntax == LigoSyntax.JSLIGO:
            self.keywords = {
                "type", "const", "let", "function", "export", "import", "namespace",
                "if", "else", "match", "when", "return", "failwith"
            }
        else:  # CameLIGO
            self.keywords = {
                "type", "let", "function", "if", "then", "else", "match", "with",
                "failwith", "module", "open"
            }
        
        # Built-in functions
        self.builtins = {
            "Tezos.get_amount", "Tezos.get_balance", "Tezos.get_sender",
            "Map.find", "Map.update", "List.map", "Set.add"
        }
        
        # Type names
        self.type_names = {
            "unit", "int", "nat", "string", "bool", "tez", "mutez",
            "address", "list", "map", "set", "option"
        }
    
    def error(self, message: str):
        """Raise a lexer error."""
        raise SyntaxError(f"Lexer error at line {self.line}, column {self.column}: {message}")
    
    def current_char(self) -> Optional[str]:
        """Get current character."""
        return self.source[self.position] if self.position < len(self.source) else None
    
    def advance(self):
        """Advance position."""
        if self.position < len(self.source):
            if self.source[self.position] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.position += 1
    
    def skip_whitespace(self):
        """Skip whitespace characters."""
        while self.current_char() and self.current_char().isspace():
            self.advance()
    
    def read_string(self) -> str:
        """Read string literal."""
        quote = self.current_char()
        self.advance()  # Skip opening quote
        
        value = ""
        while self.current_char() and self.current_char() != quote:
            if self.current_char() == '\\':
                self.advance()
                escape = self.current_char()
                if escape == 'n':
                    value += '\n'
                elif escape == 't':
                    value += '\t'
                elif escape == '\\':
                    value += '\\'
                elif escape == quote:
                    value += quote
                else:
                    value += escape or ""
                self.advance()
            else:
                value += self.current_char()
                self.advance()
        
        if not self.current_char():
            self.error("Unterminated string literal")
        
        self.advance()  # Skip closing quote
        return value
    
    def read_number(self) -> str:
        """Read number literal."""
        value = ""
        while self.current_char() and (self.current_char().isdigit() or self.current_char() == '_'):
            if self.current_char() != '_':
                value += self.current_char()
            self.advance()
        return value
    
    def read_identifier(self) -> str:
        """Read identifier."""
        value = ""
        while (self.current_char() and 
               (self.current_char().isalnum() or self.current_char() in "_.")):
            value += self.current_char()
            self.advance()
        return value
    
    def tokenize(self) -> List[Token]:
        """Tokenize the source code."""
        self.tokens = []
        
        while self.position < len(self.source):
            char = self.current_char()
            
            if not char:
                break
            
            # Skip whitespace
            if char.isspace():
                self.skip_whitespace()
                continue
            
            # Comments
            if char == '/' and self.position + 1 < len(self.source):
                next_char = self.source[self.position + 1]
                if next_char == '/':
                    # Skip line comment
                    while self.current_char() and self.current_char() != '\n':
                        self.advance()
                    continue
                elif next_char == '*':
                    # Skip block comment
                    self.advance()  # Skip '/'
                    self.advance()  # Skip '*'
                    while (self.position + 1 < len(self.source) and 
                           not (self.current_char() == '*' and self.source[self.position + 1] == '/')):
                        self.advance()
                    if self.position + 1 < len(self.source):
                        self.advance()  # Skip '*'
                        self.advance()  # Skip '/'
                    continue
            
            # String literals
            if char in ['"', "'"]:
                string_value = self.read_string()
                self.tokens.append(Token(TokenType.STRING, string_value, self.line, self.column))
                continue
            
            # Numbers
            if char.isdigit():
                number_value = self.read_number()
                self.tokens.append(Token(TokenType.INTEGER, number_value, self.line, self.column))
                continue
            
            # Operators and punctuation
            if char == '+':
                self.tokens.append(Token(TokenType.PLUS, char, self.line, self.column))
                self.advance()
            elif char == '-':
                self.tokens.append(Token(TokenType.MINUS, char, self.line, self.column))
                self.advance()
            elif char == '*':
                self.tokens.append(Token(TokenType.MULTIPLY, char, self.line, self.column))
                self.advance()
            elif char == '/':
                self.tokens.append(Token(TokenType.DIVIDE, char, self.line, self.column))
                self.advance()
            elif char == '=' and self.position + 1 < len(self.source) and self.source[self.position + 1] == '=':
                self.tokens.append(Token(TokenType.EQUAL, "==", self.line, self.column))
                self.advance()
                self.advance()
            elif char == '=' and self.position + 1 < len(self.source) and self.source[self.position + 1] == '>':
                self.tokens.append(Token(TokenType.ARROW, "=>", self.line, self.column))
                self.advance()
                self.advance()
            elif char == '=':
                self.tokens.append(Token(TokenType.ASSIGN, char, self.line, self.column))
                self.advance()
            elif char == '!':
                if self.position + 1 < len(self.source) and self.source[self.position + 1] == '=':
                    self.tokens.append(Token(TokenType.NOT_EQUAL, "!=", self.line, self.column))
                    self.advance()
                    self.advance()
                else:
                    self.tokens.append(Token(TokenType.NOT, char, self.line, self.column))
                    self.advance()
            elif char == '<':
                if self.position + 1 < len(self.source) and self.source[self.position + 1] == '=':
                    self.tokens.append(Token(TokenType.LESS_EQUAL, "<=", self.line, self.column))
                    self.advance()
                    self.advance()
                else:
                    self.tokens.append(Token(TokenType.LESS, char, self.line, self.column))
                    self.advance()
            elif char == '>':
                if self.position + 1 < len(self.source) and self.source[self.position + 1] == '=':
                    self.tokens.append(Token(TokenType.GREATER_EQUAL, ">=", self.line, self.column))
                    self.advance()
                    self.advance()
                else:
                    self.tokens.append(Token(TokenType.GREATER, char, self.line, self.column))
                    self.advance()
            elif char == '&' and self.position + 1 < len(self.source) and self.source[self.position + 1] == '&':
                self.tokens.append(Token(TokenType.AND, "&&", self.line, self.column))
                self.advance()
                self.advance()
            elif char == '|' and self.position + 1 < len(self.source) and self.source[self.position + 1] == '|':
                self.tokens.append(Token(TokenType.OR, "||", self.line, self.column))
                self.advance()
                self.advance()
            elif char == '{':
                self.tokens.append(Token(TokenType.LBRACE, char, self.line, self.column))
                self.advance()
            elif char == '}':
                self.tokens.append(Token(TokenType.RBRACE, char, self.line, self.column))
                self.advance()
            elif char == '(':
                self.tokens.append(Token(TokenType.LPAREN, char, self.line, self.column))
                self.advance()
            elif char == ')':
                self.tokens.append(Token(TokenType.RPAREN, char, self.line, self.column))
                self.advance()
            elif char == '[':
                self.tokens.append(Token(TokenType.LBRACKET, char, self.line, self.column))
                self.advance()
            elif char == ']':
                self.tokens.append(Token(TokenType.RBRACKET, char, self.line, self.column))
                self.advance()
            elif char == ';':
                self.tokens.append(Token(TokenType.SEMICOLON, char, self.line, self.column))
                self.advance()
            elif char == ',':
                self.tokens.append(Token(TokenType.COMMA, char, self.line, self.column))
                self.advance()
            elif char == '.':
                self.tokens.append(Token(TokenType.DOT, char, self.line, self.column))
                self.advance()
            elif char == ':':
                self.tokens.append(Token(TokenType.COLON, char, self.line, self.column))
                self.advance()
            elif char == '|':
                self.tokens.append(Token(TokenType.PIPE, char, self.line, self.column))
                self.advance()
            elif char == '@':
                # Entry annotation
                identifier = self.read_identifier()
                if identifier == "entry":
                    self.tokens.append(Token(TokenType.ENTRY, "@entry", self.line, self.column))
                else:
                    self.tokens.append(Token(TokenType.IDENTIFIER, f"@{identifier}", self.line, self.column))
            elif char.isalpha() or char == '_':
                identifier = self.read_identifier()
                
                if identifier in self.keywords:
                    token_type = getattr(TokenType, identifier.upper(), TokenType.IDENTIFIER)
                    self.tokens.append(Token(token_type, identifier, self.line, self.column))
                elif identifier in self.type_names:
                    self.tokens.append(Token(TokenType.TYPE_NAME, identifier, self.line, self.column))
                elif identifier in self.builtins:
                    self.tokens.append(Token(TokenType.BUILTIN, identifier, self.line, self.column))
                else:
                    self.tokens.append(Token(TokenType.IDENTIFIER, identifier, self.line, self.column))
            else:
                self.error(f"Unknown character: '{char}'")
        
        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return self.tokens


class LigoParser:
    """Parser for LIGO language."""
    
    def __init__(self, tokens: List[Token], syntax: LigoSyntax = LigoSyntax.JSLIGO):
        self.tokens = tokens
        self.syntax = syntax
        self.position = 0
        self.current_token = tokens[0] if tokens else None
    
    def error(self, message: str):
        """Raise parser error."""
        token = self.current_token
        raise SyntaxError(f"Parser error at line {token.line}, column {token.column}: {message}")
    
    def advance(self):
        """Advance to next token."""
        self.position += 1
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
        else:
            self.current_token = None
    
    def match(self, token_type: TokenType) -> bool:
        """Check if current token matches type."""
        return self.current_token and self.current_token.type == token_type
    
    def expect(self, token_type: TokenType) -> Token:
        """Expect specific token type."""
        if not self.match(token_type):
            self.error(f"Expected {token_type.value}, got {self.current_token.type.value if self.current_token else 'EOF'}")
        
        token = self.current_token
        self.advance()
        return token
    
    def parse_type(self) -> LigoType_Node:
        """Parse LIGO type."""
        if self.match(TokenType.TYPE_NAME):
            type_name = LigoType(self.current_token.value)
            self.advance()
            
            # Handle generic types
            if self.match(TokenType.LESS):
                self.advance()
                args = []
                while not self.match(TokenType.GREATER):
                    args.append(self.parse_type())
                    if self.match(TokenType.COMMA):
                        self.advance()
                self.expect(TokenType.GREATER)
                return LigoType_Node(type_name, args, syntax=self.syntax)
            
            return LigoType_Node(type_name, syntax=self.syntax)
        
        self.error("Expected type")
    
    def parse_literal(self) -> LigoLiteral:
        """Parse literal expression."""
        if self.match(TokenType.INTEGER):
            value = int(self.current_token.value)
            self.advance()
            return LigoLiteral(value, LigoType.INT, syntax=self.syntax)
        elif self.match(TokenType.STRING):
            value = self.current_token.value
            self.advance()
            return LigoLiteral(value, LigoType.STRING, syntax=self.syntax)
        
        self.error("Expected literal")
    
    def parse_primary_expression(self) -> LigoExpression:
        """Parse primary expression."""
        if self.match(TokenType.INTEGER) or self.match(TokenType.STRING):
            return self.parse_literal()
        elif self.match(TokenType.IDENTIFIER):
            name = self.current_token.value
            self.advance()
            return LigoIdentifier(name, syntax=self.syntax)
        elif self.match(TokenType.LPAREN):
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        
        self.error("Expected expression")
    
    def parse_expression(self) -> LigoExpression:
        """Parse expression with precedence."""
        return self.parse_equality()
    
    def parse_equality(self) -> LigoExpression:
        """Parse equality expressions."""
        expr = self.parse_comparison()
        
        while self.match(TokenType.EQUAL) or self.match(TokenType.NOT_EQUAL):
            operator = LigoOperator.EQUAL if self.match(TokenType.EQUAL) else LigoOperator.NOT_EQUAL
            self.advance()
            right = self.parse_comparison()
            expr = LigoBinaryOperation(expr, operator, right, syntax=self.syntax)
        
        return expr
    
    def parse_comparison(self) -> LigoExpression:
        """Parse comparison expressions."""
        expr = self.parse_addition()
        
        while (self.match(TokenType.LESS) or self.match(TokenType.GREATER) or 
               self.match(TokenType.LESS_EQUAL) or self.match(TokenType.GREATER_EQUAL)):
            
            if self.match(TokenType.LESS):
                operator = LigoOperator.LESS_THAN
            elif self.match(TokenType.GREATER):
                operator = LigoOperator.GREATER_THAN
            elif self.match(TokenType.LESS_EQUAL):
                operator = LigoOperator.LESS_EQUAL
            else:
                operator = LigoOperator.GREATER_EQUAL
            
            self.advance()
            right = self.parse_addition()
            expr = LigoBinaryOperation(expr, operator, right, syntax=self.syntax)
        
        return expr
    
    def parse_addition(self) -> LigoExpression:
        """Parse addition/subtraction."""
        expr = self.parse_multiplication()
        
        while self.match(TokenType.PLUS) or self.match(TokenType.MINUS):
            operator = LigoOperator.ADD if self.match(TokenType.PLUS) else LigoOperator.SUBTRACT
            self.advance()
            right = self.parse_multiplication()
            expr = LigoBinaryOperation(expr, operator, right, syntax=self.syntax)
        
        return expr
    
    def parse_multiplication(self) -> LigoExpression:
        """Parse multiplication/division."""
        expr = self.parse_primary_expression()
        
        while self.match(TokenType.MULTIPLY) or self.match(TokenType.DIVIDE):
            operator = LigoOperator.MULTIPLY if self.match(TokenType.MULTIPLY) else LigoOperator.DIVIDE
            self.advance()
            right = self.parse_primary_expression()
            expr = LigoBinaryOperation(expr, operator, right, syntax=self.syntax)
        
        return expr
    
    def parse_function_declaration(self) -> LigoFunctionDeclaration:
        """Parse function declaration."""
        is_entry = False
        
        # Check for @entry decorator
        if self.match(TokenType.ENTRY):
            is_entry = True
            self.advance()
        
        self.expect(TokenType.FUNCTION)
        name = self.expect(TokenType.IDENTIFIER).value
        
        self.expect(TokenType.LPAREN)
        parameters = []
        
        while not self.match(TokenType.RPAREN):
            param_name = self.expect(TokenType.IDENTIFIER).value
            self.expect(TokenType.COLON)
            param_type = self.parse_type()
            parameters.append(LigoParameter(param_name, param_type, syntax=self.syntax))
            
            if self.match(TokenType.COMMA):
                self.advance()
        
        self.expect(TokenType.RPAREN)
        
        # Return type
        return_type = None
        if self.match(TokenType.COLON):
            self.advance()
            return_type = self.parse_type()
        
        # Function body
        self.expect(TokenType.LBRACE)
        statements = []
        
        while not self.match(TokenType.RBRACE):
            if self.match(TokenType.RETURN):
                self.advance()
                expr = self.parse_expression()
                statements.append(LigoReturnStatement(expr, syntax=self.syntax))
                if self.match(TokenType.SEMICOLON):
                    self.advance()
            else:
                expr = self.parse_expression()
                statements.append(LigoExpressionStatement(expr, syntax=self.syntax))
                if self.match(TokenType.SEMICOLON):
                    self.advance()
        
        self.expect(TokenType.RBRACE)
        
        body = LigoBlockStatement(statements, syntax=self.syntax)
        return LigoFunctionDeclaration(name, parameters, return_type, body, is_entry, syntax=self.syntax)
    
    def parse_type_declaration(self) -> LigoTypeDeclaration:
        """Parse type declaration."""
        self.expect(TokenType.TYPE)
        name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.ASSIGN)
        type_def = self.parse_type()
        self.expect(TokenType.SEMICOLON)
        
        return LigoTypeDeclaration(name, type_def, syntax=self.syntax)
    
    def parse_declaration(self) -> LigoDeclaration:
        """Parse top-level declaration."""
        if self.match(TokenType.TYPE):
            return self.parse_type_declaration()
        elif self.match(TokenType.ENTRY) or self.match(TokenType.FUNCTION):
            return self.parse_function_declaration()
        elif self.match(TokenType.CONST) or self.match(TokenType.LET):
            # Variable declaration
            is_const = self.match(TokenType.CONST)
            self.advance()
            
            name = self.expect(TokenType.IDENTIFIER).value
            
            var_type = None
            if self.match(TokenType.COLON):
                self.advance()
                var_type = self.parse_type()
            
            initializer = None
            if self.match(TokenType.ASSIGN):
                self.advance()
                initializer = self.parse_expression()
            
            self.expect(TokenType.SEMICOLON)
            
            return LigoVariableDeclaration(name, var_type, initializer, not is_const, syntax=self.syntax)
        
        self.error("Expected declaration")
    
    def parse_module(self) -> LigoModule:
        """Parse complete LIGO module."""
        imports = []
        declarations = []
        
        while not self.match(TokenType.EOF):
            if self.match(TokenType.IMPORT):
                # Parse import (simplified)
                self.advance()
                path = self.expect(TokenType.STRING).value
                imports.append(LigoImport(path, syntax=self.syntax))
                if self.match(TokenType.SEMICOLON):
                    self.advance()
            else:
                declarations.append(self.parse_declaration())
        
        return LigoModule(imports, declarations, self.syntax)


def parse_ligo(source: str, syntax: LigoSyntax = LigoSyntax.JSLIGO) -> LigoModule:
    """Parse LIGO source code into AST."""
    lexer = LigoLexer(source, syntax)
    tokens = lexer.tokenize()
    
    parser = LigoParser(tokens, syntax)
    return parser.parse_module()


def parse_ligo_expression(source: str, syntax: LigoSyntax = LigoSyntax.JSLIGO) -> LigoExpression:
    """Parse single LIGO expression."""
    lexer = LigoLexer(source, syntax)
    tokens = lexer.tokenize()
    
    parser = LigoParser(tokens, syntax)
    return parser.parse_expression() 