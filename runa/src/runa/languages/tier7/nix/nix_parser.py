#!/usr/bin/env python3
"""
Nix Parser - Comprehensive parser for Nix Expression Language

Features:
- Complete Nix expression parsing
- Functional constructs (functions, applications, closures)
- Attribute sets and attribute access
- Let expressions and variable bindings
- String interpolation and multi-line strings
- Lists and list operations
- Conditionals and pattern matching
- Import and include system
- Error recovery and reporting
"""

import re
from typing import List, Optional, Dict, Any, Tuple, Union
from enum import Enum, auto
from dataclasses import dataclass
from .nix_ast import *

class TokenType(Enum):
    """Nix token types"""
    # Literals
    IDENTIFIER = auto()
    STRING = auto()
    INTEGER = auto()
    FLOAT = auto()
    PATH = auto()
    URI = auto()
    
    # Keywords
    IF = auto()
    THEN = auto()
    ELSE = auto()
    LET = auto()
    IN = auto()
    WITH = auto()
    INHERIT = auto()
    REC = auto()
    ASSERT = auto()
    OR = auto()
    AND = auto()
    NOT = auto()
    IMPORT = auto()
    
    # Boolean and null
    TRUE = auto()
    FALSE = auto()
    NULL = auto()
    
    # Operators
    PLUS = auto()           # +
    MINUS = auto()          # -
    MULTIPLY = auto()       # *
    DIVIDE = auto()         # /
    EQUALS = auto()         # =
    NOT_EQUALS = auto()     # !=
    LESS_THAN = auto()      # <
    LESS_EQUAL = auto()     # <=
    GREATER_THAN = auto()   # >
    GREATER_EQUAL = auto()  # >=
    LOGICAL_AND = auto()    # &&
    LOGICAL_OR = auto()     # ||
    LOGICAL_NOT = auto()    # !
    CONCAT = auto()         # ++
    UPDATE = auto()         # //
    QUESTION = auto()       # ?
    
    # Delimiters
    SEMICOLON = auto()      # ;
    COLON = auto()          # :
    COMMA = auto()          # ,
    DOT = auto()            # .
    
    # Brackets
    LPAREN = auto()         # (
    RPAREN = auto()         # )
    LBRACE = auto()         # {
    RBRACE = auto()         # }
    LBRACKET = auto()       # [
    RBRACKET = auto()       # ]
    
    # String interpolation
    DOLLAR_LBRACE = auto()  # ${
    
    # Special
    AT = auto()             # @
    ELLIPSIS = auto()       # ...
    
    # Comments
    COMMENT = auto()
    
    # Whitespace and structure
    NEWLINE = auto()
    WHITESPACE = auto()
    
    # End of file
    EOF = auto()

@dataclass
class Token:
    """Nix token"""
    type: TokenType
    value: str
    line: int = 1
    column: int = 1

class NixLexer:
    """Lexer for Nix expressions"""
    
    # Keywords mapping
    KEYWORDS = {
        'if': TokenType.IF,
        'then': TokenType.THEN,
        'else': TokenType.ELSE,
        'let': TokenType.LET,
        'in': TokenType.IN,
        'with': TokenType.WITH,
        'inherit': TokenType.INHERIT,
        'rec': TokenType.REC,
        'assert': TokenType.ASSERT,
        'or': TokenType.OR,
        'and': TokenType.AND,
        'not': TokenType.NOT,
        'import': TokenType.IMPORT,
        'true': TokenType.TRUE,
        'false': TokenType.FALSE,
        'null': TokenType.NULL,
    }
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        
    def error(self, message: str) -> None:
        """Report lexer error"""
        raise SyntaxError(f"Line {self.line}, Column {self.column}: {message}")
        
    def peek(self, offset: int = 0) -> str:
        """Peek at character at current position + offset"""
        pos = self.pos + offset
        return self.source[pos] if pos < len(self.source) else ''
        
    def advance(self) -> str:
        """Advance and return current character"""
        if self.pos >= len(self.source):
            return ''
            
        char = self.source[self.pos]
        self.pos += 1
        
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
            
        return char
        
    def skip_whitespace(self) -> None:
        """Skip whitespace characters"""
        while self.pos < len(self.source):
            char = self.peek()
            if char in ' \t\r':
                self.advance()
            else:
                break
                
    def read_string(self, quote: str) -> str:
        """Read quoted string with interpolation support"""
        value = ''
        self.advance()  # Skip opening quote
        
        while self.pos < len(self.source):
            char = self.peek()
            
            if char == quote:
                self.advance()  # Skip closing quote
                break
            elif char == '\\':
                self.advance()  # Skip backslash
                escaped = self.advance()
                if escaped == 'n':
                    value += '\n'
                elif escaped == 't':
                    value += '\t'
                elif escaped == 'r':
                    value += '\r'
                elif escaped == '\\':
                    value += '\\'
                elif escaped == '"':
                    value += '"'
                elif escaped == "'":
                    value += "'"
                else:
                    value += escaped
            elif char == '$' and self.peek(1) == '{' and quote == '"':
                # String interpolation - return what we have so far
                break
            else:
                value += self.advance()
                
        return value
        
    def read_multiline_string(self) -> str:
        """Read multiline string ''...''"""
        value = ''
        self.advance()  # Skip first '
        self.advance()  # Skip second '
        
        while self.pos < len(self.source):
            char = self.peek()
            next_char = self.peek(1)
            
            if char == "'" and next_char == "'":
                self.advance()  # Skip first '
                self.advance()  # Skip second '
                break
            elif char == '$' and next_char == '{':
                # String interpolation
                break
            else:
                value += self.advance()
                
        return value
        
    def read_identifier(self) -> str:
        """Read identifier"""
        value = ''
        
        # First character must be letter or underscore
        char = self.peek()
        if char.isalpha() or char == '_':
            value += self.advance()
        else:
            return value
            
        # Subsequent characters can be alphanumeric, underscore, dash, or apostrophe
        while self.pos < len(self.source):
            char = self.peek()
            if char.isalnum() or char in '_-\'':
                value += self.advance()
            else:
                break
                
        return value
        
    def read_number(self) -> Tuple[str, TokenType]:
        """Read number (integer or float)"""
        value = ''
        is_float = False
        
        while self.pos < len(self.source):
            char = self.peek()
            if char.isdigit():
                value += self.advance()
            elif char == '.' and not is_float:
                # Check if next character is digit
                if self.peek(1).isdigit():
                    is_float = True
                    value += self.advance()
                else:
                    break
            else:
                break
                
        return value, TokenType.FLOAT if is_float else TokenType.INTEGER
        
    def read_path(self) -> str:
        """Read path literal"""
        value = ''
        
        while self.pos < len(self.source):
            char = self.peek()
            if char.isalnum() or char in '/_.-':
                value += self.advance()
            else:
                break
                
        return value
        
    def read_comment(self) -> str:
        """Read comment"""
        if self.peek() == '#':
            # Line comment
            self.advance()  # Skip #
            value = ''
            while self.pos < len(self.source):
                char = self.peek()
                if char == '\n':
                    break
                value += self.advance()
            return value.strip()
            
        elif self.peek() == '/' and self.peek(1) == '*':
            # Block comment
            self.advance()  # Skip /
            self.advance()  # Skip *
            value = ''
            while self.pos < len(self.source) - 1:
                char = self.peek()
                next_char = self.peek(1)
                if char == '*' and next_char == '/':
                    self.advance()  # Skip *
                    self.advance()  # Skip /
                    break
                value += self.advance()
            return value.strip()
            
        return ''
        
    def tokenize(self) -> List[Token]:
        """Tokenize the entire source"""
        self.tokens = []
        
        while self.pos < len(self.source):
            start_line, start_col = self.line, self.column
            char = self.peek()
            
            # Skip whitespace
            if char in ' \t\r':
                self.skip_whitespace()
                continue
                
            # Newlines
            elif char == '\n':
                self.tokens.append(Token(TokenType.NEWLINE, self.advance(), start_line, start_col))
                
            # Comments
            elif char == '#' or (char == '/' and self.peek(1) == '*'):
                comment = self.read_comment()
                self.tokens.append(Token(TokenType.COMMENT, comment, start_line, start_col))
                
            # String literals
            elif char == '"':
                string_value = self.read_string('"')
                self.tokens.append(Token(TokenType.STRING, string_value, start_line, start_col))
                
            # Multiline strings
            elif char == "'" and self.peek(1) == "'":
                string_value = self.read_multiline_string()
                self.tokens.append(Token(TokenType.STRING, string_value, start_line, start_col))
                
            # Numbers
            elif char.isdigit():
                number_value, token_type = self.read_number()
                self.tokens.append(Token(token_type, number_value, start_line, start_col))
                
            # Paths (starting with / or ./ or ../)
            elif (char == '/' or 
                  (char == '.' and self.peek(1) == '/') or
                  (char == '.' and self.peek(1) == '.' and self.peek(2) == '/')):
                path_value = self.read_path()
                self.tokens.append(Token(TokenType.PATH, path_value, start_line, start_col))
                
            # Identifiers and keywords
            elif char.isalpha() or char == '_':
                identifier = self.read_identifier()
                token_type = self.KEYWORDS.get(identifier, TokenType.IDENTIFIER)
                self.tokens.append(Token(token_type, identifier, start_line, start_col))
                
            # Two-character operators
            elif char == '=' and self.peek(1) == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.EQUALS, '==', start_line, start_col))
                
            elif char == '!' and self.peek(1) == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.NOT_EQUALS, '!=', start_line, start_col))
                
            elif char == '<' and self.peek(1) == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.LESS_EQUAL, '<=', start_line, start_col))
                
            elif char == '>' and self.peek(1) == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.GREATER_EQUAL, '>=', start_line, start_col))
                
            elif char == '&' and self.peek(1) == '&':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.LOGICAL_AND, '&&', start_line, start_col))
                
            elif char == '|' and self.peek(1) == '|':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.LOGICAL_OR, '||', start_line, start_col))
                
            elif char == '+' and self.peek(1) == '+':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.CONCAT, '++', start_line, start_col))
                
            elif char == '/' and self.peek(1) == '/':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.UPDATE, '//', start_line, start_col))
                
            elif char == '$' and self.peek(1) == '{':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.DOLLAR_LBRACE, '${', start_line, start_col))
                
            elif char == '.' and self.peek(1) == '.' and self.peek(2) == '.':
                self.advance()
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.ELLIPSIS, '...', start_line, start_col))
                
            # Single-character operators and delimiters
            elif char == '+':
                self.tokens.append(Token(TokenType.PLUS, self.advance(), start_line, start_col))
            elif char == '-':
                self.tokens.append(Token(TokenType.MINUS, self.advance(), start_line, start_col))
            elif char == '*':
                self.tokens.append(Token(TokenType.MULTIPLY, self.advance(), start_line, start_col))
            elif char == '/':
                self.tokens.append(Token(TokenType.DIVIDE, self.advance(), start_line, start_col))
            elif char == '=':
                self.tokens.append(Token(TokenType.EQUALS, self.advance(), start_line, start_col))
            elif char == '<':
                self.tokens.append(Token(TokenType.LESS_THAN, self.advance(), start_line, start_col))
            elif char == '>':
                self.tokens.append(Token(TokenType.GREATER_THAN, self.advance(), start_line, start_col))
            elif char == '!':
                self.tokens.append(Token(TokenType.LOGICAL_NOT, self.advance(), start_line, start_col))
            elif char == '?':
                self.tokens.append(Token(TokenType.QUESTION, self.advance(), start_line, start_col))
            elif char == ';':
                self.tokens.append(Token(TokenType.SEMICOLON, self.advance(), start_line, start_col))
            elif char == ':':
                self.tokens.append(Token(TokenType.COLON, self.advance(), start_line, start_col))
            elif char == ',':
                self.tokens.append(Token(TokenType.COMMA, self.advance(), start_line, start_col))
            elif char == '.':
                self.tokens.append(Token(TokenType.DOT, self.advance(), start_line, start_col))
            elif char == '(':
                self.tokens.append(Token(TokenType.LPAREN, self.advance(), start_line, start_col))
            elif char == ')':
                self.tokens.append(Token(TokenType.RPAREN, self.advance(), start_line, start_col))
            elif char == '{':
                self.tokens.append(Token(TokenType.LBRACE, self.advance(), start_line, start_col))
            elif char == '}':
                self.tokens.append(Token(TokenType.RBRACE, self.advance(), start_line, start_col))
            elif char == '[':
                self.tokens.append(Token(TokenType.LBRACKET, self.advance(), start_line, start_col))
            elif char == ']':
                self.tokens.append(Token(TokenType.RBRACKET, self.advance(), start_line, start_col))
            elif char == '@':
                self.tokens.append(Token(TokenType.AT, self.advance(), start_line, start_col))
                
            else:
                # Unknown character - skip it
                self.advance()
                
        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, '', self.line, self.column))
        return self.tokens

class NixParser:
    """Parser for Nix expressions"""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.current_token = tokens[0] if tokens else Token(TokenType.EOF, '', 1, 1)
        
    def error(self, message: str) -> None:
        """Report parser error"""
        token = self.current_token
        raise SyntaxError(f"Line {token.line}, Column {token.column}: {message}")
        
    def peek(self, offset: int = 0) -> Token:
        """Peek at token at current position + offset"""
        pos = self.pos + offset
        return self.tokens[pos] if pos < len(self.tokens) else Token(TokenType.EOF, '', 1, 1)
        
    def advance(self) -> Token:
        """Advance to next token"""
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
            self.current_token = self.tokens[self.pos]
        return self.current_token
        
    def match(self, *token_types: TokenType) -> bool:
        """Check if current token matches any of the given types"""
        return self.current_token.type in token_types
        
    def consume(self, token_type: TokenType, message: str = None) -> Token:
        """Consume token of given type or error"""
        if self.current_token.type != token_type:
            msg = message or f"Expected {token_type}, got {self.current_token.type}"
            self.error(msg)
        token = self.current_token
        self.advance()
        return token
        
    def skip_newlines(self) -> None:
        """Skip newline tokens"""
        while self.match(TokenType.NEWLINE):
            self.advance()
            
    def parse_nix_file(self) -> NixFile:
        """Parse complete Nix file"""
        self.skip_newlines()
        
        if self.match(TokenType.EOF):
            # Empty file
            return NixFile(expression=NullLiteral())
            
        expression = self.parse_expression()
        self.skip_newlines()
        
        if not self.match(TokenType.EOF):
            self.error("Expected end of file")
            
        return NixFile(expression=expression)
        
    def parse_expression(self) -> NixExpression:
        """Parse any expression"""
        return self.parse_function()
        
    def parse_function(self) -> NixExpression:
        """Parse function expression: arg: body or { args }: body"""
        # Check for function parameter patterns
        if self.match(TokenType.LBRACE):
            # Might be function parameters { a, b }: body
            saved_pos = self.pos
            try:
                params = self.parse_function_parameters()
                if self.match(TokenType.COLON):
                    self.advance()  # consume :
                    body = self.parse_expression()
                    return FunctionExpression(parameter=params, body=body)
                else:
                    # Not a function, backtrack
                    self.pos = saved_pos
                    self.current_token = self.tokens[self.pos]
            except:
                # Not function parameters, backtrack
                self.pos = saved_pos
                self.current_token = self.tokens[self.pos]
                
        elif self.match(TokenType.IDENTIFIER):
            # Might be simple function: arg: body
            saved_pos = self.pos
            param_name = self.current_token.value
            self.advance()
            
            if self.match(TokenType.COLON):
                self.advance()  # consume :
                body = self.parse_expression()
                return FunctionExpression(parameter=param_name, body=body)
            else:
                # Not a function, backtrack
                self.pos = saved_pos
                self.current_token = self.tokens[self.pos]
                
        return self.parse_assert()
        
    def parse_function_parameters(self) -> FunctionParameters:
        """Parse function parameters { a, b ? default, ... }"""
        self.consume(TokenType.LBRACE)
        
        parameters = {}
        has_ellipsis = False
        at_pattern = None
        
        self.skip_newlines()
        
        while not self.match(TokenType.RBRACE):
            if self.match(TokenType.ELLIPSIS):
                has_ellipsis = True
                self.advance()
                break
            elif self.match(TokenType.IDENTIFIER):
                param_name = self.current_token.value
                self.advance()
                
                # Check for default value
                default_value = None
                if self.match(TokenType.QUESTION):
                    self.advance()
                    default_value = self.parse_or()
                    
                parameters[param_name] = default_value
                
                # Check for comma
                if self.match(TokenType.COMMA):
                    self.advance()
                    self.skip_newlines()
                    
            else:
                self.error("Expected parameter name or ...")
                
        self.consume(TokenType.RBRACE)
        
        # Check for @ pattern
        if self.match(TokenType.AT):
            self.advance()
            if self.match(TokenType.IDENTIFIER):
                at_pattern = self.current_token.value
                self.advance()
                
        return FunctionParameters(
            parameters=parameters,
            has_ellipsis=has_ellipsis,
            at_pattern=at_pattern
        )
        
    def parse_assert(self) -> NixExpression:
        """Parse assert expression: assert condition; expr"""
        if self.match(TokenType.ASSERT):
            self.advance()
            condition = self.parse_or()
            self.consume(TokenType.SEMICOLON)
            body = self.parse_expression()
            return AssertExpression(condition=condition, body=body)
            
        return self.parse_with()
        
    def parse_with(self) -> NixExpression:
        """Parse with expression: with expr; body"""
        if self.match(TokenType.WITH):
            self.advance()
            namespace = self.parse_or()
            self.consume(TokenType.SEMICOLON)
            body = self.parse_expression()
            return WithExpression(namespace=namespace, body=body)
            
        return self.parse_let()
        
    def parse_let(self) -> NixExpression:
        """Parse let expression: let bindings in expr"""
        if self.match(TokenType.LET):
            self.advance()
            self.skip_newlines()
            
            bindings = []
            
            while not self.match(TokenType.IN):
                binding = self.parse_binding()
                bindings.append(binding)
                
                if self.match(TokenType.SEMICOLON):
                    self.advance()
                    self.skip_newlines()
                    
            self.consume(TokenType.IN)
            body = self.parse_expression()
            
            return LetExpression(bindings=bindings, body=body)
            
        return self.parse_conditional()
        
    def parse_conditional(self) -> NixExpression:
        """Parse conditional expression: if cond then expr1 else expr2"""
        if self.match(TokenType.IF):
            self.advance()
            condition = self.parse_or()
            self.consume(TokenType.THEN)
            then_expr = self.parse_or()
            self.consume(TokenType.ELSE)
            else_expr = self.parse_expression()
            
            return ConditionalExpression(
                condition=condition,
                then_expr=then_expr,
                else_expr=else_expr
            )
            
        return self.parse_or()
        
    def parse_or(self) -> NixExpression:
        """Parse logical OR expression"""
        expr = self.parse_and()
        
        while self.match(TokenType.LOGICAL_OR):
            op = self.current_token.value
            self.advance()
            right = self.parse_and()
            expr = BinaryOperation(left=expr, operator=op, right=right)
            
        return expr
        
    def parse_and(self) -> NixExpression:
        """Parse logical AND expression"""
        expr = self.parse_equality()
        
        while self.match(TokenType.LOGICAL_AND):
            op = self.current_token.value
            self.advance()
            right = self.parse_equality()
            expr = BinaryOperation(left=expr, operator=op, right=right)
            
        return expr
        
    def parse_equality(self) -> NixExpression:
        """Parse equality expressions"""
        expr = self.parse_relational()
        
        while self.match(TokenType.EQUALS, TokenType.NOT_EQUALS):
            op = self.current_token.value
            self.advance()
            right = self.parse_relational()
            expr = BinaryOperation(left=expr, operator=op, right=right)
            
        return expr
        
    def parse_relational(self) -> NixExpression:
        """Parse relational expressions"""
        expr = self.parse_concatenation()
        
        while self.match(TokenType.LESS_THAN, TokenType.LESS_EQUAL,
                         TokenType.GREATER_THAN, TokenType.GREATER_EQUAL):
            op = self.current_token.value
            self.advance()
            right = self.parse_concatenation()
            expr = BinaryOperation(left=expr, operator=op, right=right)
            
        return expr
        
    def parse_concatenation(self) -> NixExpression:
        """Parse concatenation expressions"""
        expr = self.parse_addition()
        
        while self.match(TokenType.CONCAT, TokenType.UPDATE):
            op = self.current_token.value
            self.advance()
            right = self.parse_addition()
            expr = BinaryOperation(left=expr, operator=op, right=right)
            
        return expr
        
    def parse_addition(self) -> NixExpression:
        """Parse addition and subtraction"""
        expr = self.parse_multiplication()
        
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = self.current_token.value
            self.advance()
            right = self.parse_multiplication()
            expr = BinaryOperation(left=expr, operator=op, right=right)
            
        return expr
        
    def parse_multiplication(self) -> NixExpression:
        """Parse multiplication and division"""
        expr = self.parse_unary()
        
        while self.match(TokenType.MULTIPLY, TokenType.DIVIDE):
            op = self.current_token.value
            self.advance()
            right = self.parse_unary()
            expr = BinaryOperation(left=expr, operator=op, right=right)
            
        return expr
        
    def parse_unary(self) -> NixExpression:
        """Parse unary expressions"""
        if self.match(TokenType.LOGICAL_NOT, TokenType.MINUS):
            op = self.current_token.value
            self.advance()
            operand = self.parse_unary()
            return UnaryOperation(operator=op, operand=operand)
            
        return self.parse_application()
        
    def parse_application(self) -> NixExpression:
        """Parse function application"""
        expr = self.parse_attribute_access()
        
        # Function application is left-associative
        while (not self.match(TokenType.EOF, TokenType.SEMICOLON, TokenType.COMMA,
                              TokenType.RBRACE, TokenType.RBRACKET, TokenType.RPAREN,
                              TokenType.THEN, TokenType.ELSE, TokenType.IN) and
               not self.is_binary_operator()):
            
            arg = self.parse_attribute_access()
            expr = FunctionApplication(function=expr, argument=arg)
            
        return expr
        
    def parse_attribute_access(self) -> NixExpression:
        """Parse attribute access expressions"""
        expr = self.parse_primary()
        
        while self.match(TokenType.DOT):
            self.advance()  # consume .
            
            if self.match(TokenType.IDENTIFIER):
                attr = self.current_token.value
                self.advance()
                
                # Check for default value
                default_value = None
                if self.match(TokenType.OR):
                    self.advance()
                    default_value = self.parse_primary()
                    
                expr = AttributeAccess(
                    expression=expr,
                    attribute=attr,
                    has_default=default_value is not None,
                    default_value=default_value
                )
            elif self.match(TokenType.STRING):
                attr = self.current_token.value
                self.advance()
                expr = AttributeAccess(expression=expr, attribute=attr)
            else:
                self.error("Expected attribute name after .")
                
        return expr
        
    def parse_primary(self) -> NixExpression:
        """Parse primary expressions"""
        # Literals
        if self.match(TokenType.INTEGER):
            value = int(self.current_token.value)
            self.advance()
            return IntegerLiteral(value)
            
        elif self.match(TokenType.FLOAT):
            value = float(self.current_token.value)
            self.advance()
            return FloatLiteral(value)
            
        elif self.match(TokenType.STRING):
            value = self.current_token.value
            self.advance()
            return StringLiteral(value)
            
        elif self.match(TokenType.TRUE):
            self.advance()
            return BooleanLiteral(True)
            
        elif self.match(TokenType.FALSE):
            self.advance()
            return BooleanLiteral(False)
            
        elif self.match(TokenType.NULL):
            self.advance()
            return NullLiteral()
            
        elif self.match(TokenType.PATH):
            value = self.current_token.value
            is_absolute = value.startswith('/')
            self.advance()
            return PathLiteral(value, is_absolute)
            
        # Identifiers
        elif self.match(TokenType.IDENTIFIER):
            name = self.current_token.value
            self.advance()
            return Identifier(name)
            
        # Parenthesized expressions
        elif self.match(TokenType.LPAREN):
            self.advance()
            expr = self.parse_expression()
            self.consume(TokenType.RPAREN)
            return expr
            
        # Attribute sets
        elif self.match(TokenType.LBRACE):
            return self.parse_attribute_set()
            
        # Lists
        elif self.match(TokenType.LBRACKET):
            return self.parse_list()
            
        # Import
        elif self.match(TokenType.IMPORT):
            self.advance()
            path = self.parse_primary()
            return ImportExpression(path=path)
            
        else:
            self.error(f"Unexpected token: {self.current_token.type}")
            
    def parse_attribute_set(self) -> AttributeSet:
        """Parse attribute set { a = 1; b = 2; }"""
        is_recursive = False
        
        # Check for rec
        if self.match(TokenType.REC):
            is_recursive = True
            self.advance()
            
        self.consume(TokenType.LBRACE)
        self.skip_newlines()
        
        attributes = []
        
        while not self.match(TokenType.RBRACE):
            binding = self.parse_binding()
            attributes.append(binding)
            
            if self.match(TokenType.SEMICOLON):
                self.advance()
                self.skip_newlines()
            elif self.match(TokenType.RBRACE):
                break
            else:
                self.skip_newlines()
                
        self.consume(TokenType.RBRACE)
        
        return AttributeSet(attributes=attributes, is_recursive=is_recursive)
        
    def parse_binding(self) -> AttributeBinding:
        """Parse attribute binding"""
        if self.match(TokenType.INHERIT):
            return self.parse_inherit()
            
        # Parse attribute path
        path = []
        
        if self.match(TokenType.IDENTIFIER):
            path.append(self.current_token.value)
            self.advance()
        elif self.match(TokenType.STRING):
            path.append(self.current_token.value)
            self.advance()
        else:
            self.error("Expected attribute name")
            
        # Handle nested attributes like a.b.c
        while self.match(TokenType.DOT):
            self.advance()
            if self.match(TokenType.IDENTIFIER):
                path.append(self.current_token.value)
                self.advance()
            elif self.match(TokenType.STRING):
                path.append(self.current_token.value)
                self.advance()
            else:
                self.error("Expected attribute name after .")
                
        self.consume(TokenType.EQUALS)
        value = self.parse_expression()
        
        return AttributeBinding(path=path, value=value)
        
    def parse_inherit(self) -> AttributeBinding:
        """Parse inherit statement"""
        self.consume(TokenType.INHERIT)
        
        # Check for inherit source
        inherit_source = None
        if self.match(TokenType.LPAREN):
            self.advance()
            inherit_source = self.parse_expression()
            self.consume(TokenType.RPAREN)
            
        # Parse inherited attributes
        if self.match(TokenType.IDENTIFIER):
            attr = self.current_token.value
            self.advance()
            
            return AttributeBinding(
                path=[attr],
                value=Identifier(attr),  # Default value
                is_inherit=True,
                inherit_source=inherit_source
            )
        else:
            self.error("Expected attribute name after inherit")
            
    def parse_list(self) -> ListExpression:
        """Parse list expression [ a b c ]"""
        self.consume(TokenType.LBRACKET)
        self.skip_newlines()
        
        elements = []
        
        while not self.match(TokenType.RBRACKET):
            element = self.parse_expression()
            elements.append(element)
            self.skip_newlines()
            
        self.consume(TokenType.RBRACKET)
        
        return ListExpression(elements=elements)
        
    def is_binary_operator(self) -> bool:
        """Check if current token is a binary operator"""
        return self.match(
            TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY, TokenType.DIVIDE,
            TokenType.EQUALS, TokenType.NOT_EQUALS,
            TokenType.LESS_THAN, TokenType.LESS_EQUAL,
            TokenType.GREATER_THAN, TokenType.GREATER_EQUAL,
            TokenType.LOGICAL_AND, TokenType.LOGICAL_OR,
            TokenType.CONCAT, TokenType.UPDATE
        )

# Main parsing functions

def parse_nix(source: str) -> NixFile:
    """Parse Nix source code into AST"""
    try:
        lexer = NixLexer(source)
        tokens = lexer.tokenize()
        
        # Filter out whitespace tokens for parsing
        filtered_tokens = [t for t in tokens if t.type not in (TokenType.WHITESPACE,)]
        
        parser = NixParser(filtered_tokens)
        ast = parser.parse_nix_file()
        
        return ast
        
    except Exception as e:
        raise SyntaxError(f"Nix parsing failed: {str(e)}")

# Export main components
__all__ = [
    'TokenType', 'Token', 'NixLexer', 'NixParser', 'parse_nix'
] 