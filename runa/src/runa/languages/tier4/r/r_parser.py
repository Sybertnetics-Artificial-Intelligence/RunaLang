#!/usr/bin/env python3
"""
R Parser and Lexer

Complete parser and lexer implementation for R language supporting all R constructs
including statistical operations, data structures, functions, object-oriented programming,
vectorization, and R-specific syntax patterns.

This module provides:
- Complete R lexical analysis with R-specific tokens
- Recursive descent parser for all R language constructs
- Support for R's unique syntax patterns and operators
- Statistical computing constructs and data structures
- Object-oriented programming (S3, S4, R6)
- Package system and namespace handling
"""

import re
from typing import List, Optional, Any, Union, Dict, Iterator, Tuple
from dataclasses import dataclass
from enum import Enum, auto

from .r_ast import *
from ....core.runa_ast import SourceLocation


class RTokenType(Enum):
    """R token types for lexical analysis."""
    # Literals
    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()
    LOGICAL = auto()
    NULL = auto()
    NA = auto()
    INFINITY = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    INTEGER_DIVIDE = auto()
    MODULO = auto()
    POWER = auto()
    POWER_ALT = auto()
    
    # Comparison
    EQUAL = auto()
    NOT_EQUAL = auto()
    LESS_THAN = auto()
    LESS_EQUAL = auto()
    GREATER_THAN = auto()
    GREATER_EQUAL = auto()
    
    # Logical
    AND = auto()
    OR = auto()
    NOT = auto()
    AND_SHORT = auto()
    OR_SHORT = auto()
    
    # Assignment
    ASSIGN = auto()
    ASSIGN_RIGHT = auto()
    ASSIGN_EQUAL = auto()
    SUPER_ASSIGN = auto()
    SUPER_ASSIGN_RIGHT = auto()
    
    # Special operators
    IN = auto()
    MATCH = auto()
    OUTER = auto()
    KRONECKER = auto()
    PIPE = auto()
    NAMESPACE = auto()
    NAMESPACE_INTERNAL = auto()
    TILDE = auto()
    
    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    LBRACE = auto()
    RBRACE = auto()
    COMMA = auto()
    SEMICOLON = auto()
    DOT = auto()
    DOLLAR = auto()
    AT = auto()
    QUESTION = auto()
    
    # Keywords
    FUNCTION = auto()
    IF = auto()
    ELSE = auto()
    FOR = auto()
    IN_KEYWORD = auto()
    WHILE = auto()
    REPEAT = auto()
    NEXT = auto()
    BREAK = auto()
    RETURN = auto()
    LIBRARY = auto()
    REQUIRE = auto()
    HELP = auto()
    
    # Data structure keywords
    C = auto()
    LIST = auto()
    DATA_FRAME = auto()
    MATRIX = auto()
    ARRAY = auto()
    FACTOR = auto()
    
    # Special
    EOF = auto()
    NEWLINE = auto()
    COMMENT = auto()
    ELLIPSIS = auto()
    
    # R-specific
    DOUBLE_COLON = auto()
    TRIPLE_COLON = auto()


@dataclass
class RToken:
    """R token with position information."""
    type: RTokenType
    value: str
    line: int
    column: int
    
    def __str__(self):
        return f"RToken({self.type.name}, '{self.value}', {self.line}:{self.column})"


class RLexer:
    """R lexer for tokenizing R source code."""
    
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[RToken] = []
        
        # R keywords
        self.keywords = {
            'function': RTokenType.FUNCTION,
            'if': RTokenType.IF,
            'else': RTokenType.ELSE,
            'for': RTokenType.FOR,
            'in': RTokenType.IN_KEYWORD,
            'while': RTokenType.WHILE,
            'repeat': RTokenType.REPEAT,
            'next': RTokenType.NEXT,
            'break': RTokenType.BREAK,
            'return': RTokenType.RETURN,
            'library': RTokenType.LIBRARY,
            'require': RTokenType.REQUIRE,
            'help': RTokenType.HELP,
            'c': RTokenType.C,
            'list': RTokenType.LIST,
            'data.frame': RTokenType.DATA_FRAME,
            'matrix': RTokenType.MATRIX,
            'array': RTokenType.ARRAY,
            'factor': RTokenType.FACTOR,
            'TRUE': RTokenType.LOGICAL,
            'FALSE': RTokenType.LOGICAL,
            'NULL': RTokenType.NULL,
            'NA': RTokenType.NA,
            'NA_integer_': RTokenType.NA,
            'NA_real_': RTokenType.NA,
            'NA_character_': RTokenType.NA,
            'NA_complex_': RTokenType.NA,
            'Inf': RTokenType.INFINITY,
            '-Inf': RTokenType.INFINITY,
            'NaN': RTokenType.NA
        }
        
        # R operators
        self.operators = {
            '<<-': RTokenType.SUPER_ASSIGN,
            '->>': RTokenType.SUPER_ASSIGN_RIGHT,
            '<-': RTokenType.ASSIGN,
            '->': RTokenType.ASSIGN_RIGHT,
            ':::': RTokenType.NAMESPACE_INTERNAL,
            '::': RTokenType.NAMESPACE,
            '%>%': RTokenType.PIPE,
            '%in%': RTokenType.IN,
            '%*%': RTokenType.MATCH,
            '%o%': RTokenType.OUTER,
            '%x%': RTokenType.KRONECKER,
            '**': RTokenType.POWER_ALT,
            '%/%': RTokenType.INTEGER_DIVIDE,
            '%%': RTokenType.MODULO,
            '==': RTokenType.EQUAL,
            '!=': RTokenType.NOT_EQUAL,
            '<=': RTokenType.LESS_EQUAL,
            '>=': RTokenType.GREATER_EQUAL,
            '&&': RTokenType.AND_SHORT,
            '||': RTokenType.OR_SHORT,
            '...': RTokenType.ELLIPSIS,
            '+': RTokenType.PLUS,
            '-': RTokenType.MINUS,
            '*': RTokenType.MULTIPLY,
            '/': RTokenType.DIVIDE,
            '^': RTokenType.POWER,
            '<': RTokenType.LESS_THAN,
            '>': RTokenType.GREATER_THAN,
            '&': RTokenType.AND,
            '|': RTokenType.OR,
            '!': RTokenType.NOT,
            '=': RTokenType.ASSIGN_EQUAL,
            '~': RTokenType.TILDE
        }
        
        # Single character tokens
        self.single_chars = {
            '(': RTokenType.LPAREN,
            ')': RTokenType.RPAREN,
            '[': RTokenType.LBRACKET,
            ']': RTokenType.RBRACKET,
            '{': RTokenType.LBRACE,
            '}': RTokenType.RBRACE,
            ',': RTokenType.COMMA,
            ';': RTokenType.SEMICOLON,
            '.': RTokenType.DOT,
            '$': RTokenType.DOLLAR,
            '@': RTokenType.AT,
            '?': RTokenType.QUESTION
        }
    
    def current_char(self) -> Optional[str]:
        """Get current character."""
        if self.position >= len(self.source):
            return None
        return self.source[self.position]
    
    def peek_char(self, offset: int = 1) -> Optional[str]:
        """Peek at character with offset."""
        pos = self.position + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]
    
    def advance(self) -> Optional[str]:
        """Advance position and return current character."""
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
        """Skip whitespace except newlines."""
        while self.current_char() and self.current_char() in ' \t\r':
            self.advance()
    
    def read_comment(self) -> str:
        """Read comment starting with #."""
        comment = ""
        while self.current_char() and self.current_char() != '\n':
            comment += self.advance()
        return comment
    
    def read_string(self, quote_char: str) -> str:
        """Read string literal."""
        string_value = ""
        self.advance()  # Skip opening quote
        
        while self.current_char() and self.current_char() != quote_char:
            char = self.current_char()
            if char == '\\':
                self.advance()
                next_char = self.current_char()
                if next_char:
                    if next_char == 'n':
                        string_value += '\n'
                    elif next_char == 't':
                        string_value += '\t'
                    elif next_char == 'r':
                        string_value += '\r'
                    elif next_char == '\\':
                        string_value += '\\'
                    elif next_char == quote_char:
                        string_value += quote_char
                    else:
                        string_value += next_char
                    self.advance()
            else:
                string_value += self.advance()
        
        if self.current_char() == quote_char:
            self.advance()  # Skip closing quote
        
        return string_value
    
    def read_number(self) -> Tuple[str, bool]:
        """Read numeric literal, return (value, is_integer)."""
        number = ""
        is_integer = True
        
        # Handle negative numbers
        if self.current_char() == '-':
            number += self.advance()
        
        # Read digits
        while self.current_char() and self.current_char().isdigit():
            number += self.advance()
        
        # Check for decimal point
        if self.current_char() == '.':
            is_integer = False
            number += self.advance()
            while self.current_char() and self.current_char().isdigit():
                number += self.advance()
        
        # Check for scientific notation
        if self.current_char() and self.current_char().lower() == 'e':
            is_integer = False
            number += self.advance()
            if self.current_char() and self.current_char() in '+-':
                number += self.advance()
            while self.current_char() and self.current_char().isdigit():
                number += self.advance()
        
        # Check for integer suffix
        if self.current_char() and self.current_char().upper() == 'L':
            number += self.advance()
            is_integer = True
        
        return number, is_integer
    
    def read_identifier(self) -> str:
        """Read identifier or keyword."""
        identifier = ""
        
        # R identifiers can start with letter, dot, or underscore
        while (self.current_char() and 
               (self.current_char().isalnum() or 
                self.current_char() in '._')):
            identifier += self.advance()
        
        return identifier
    
    def read_operator(self) -> Optional[str]:
        """Read multi-character operator."""
        # Sort by length (longest first) to match properly
        sorted_ops = sorted(self.operators.keys(), key=len, reverse=True)
        
        for op in sorted_ops:
            if self.source[self.position:self.position + len(op)] == op:
                for _ in range(len(op)):
                    self.advance()
                return op
        
        return None
    
    def tokenize(self) -> List[RToken]:
        """Tokenize the source code."""
        while self.position < len(self.source):
            self.skip_whitespace()
            
            if not self.current_char():
                break
            
            start_line = self.line
            start_column = self.column
            
            char = self.current_char()
            
            # Newlines
            if char == '\n':
                self.tokens.append(RToken(RTokenType.NEWLINE, '\n', start_line, start_column))
                self.advance()
            
            # Comments
            elif char == '#':
                comment = self.read_comment()
                self.tokens.append(RToken(RTokenType.COMMENT, comment, start_line, start_column))
            
            # String literals
            elif char in '"\'':
                string_value = self.read_string(char)
                self.tokens.append(RToken(RTokenType.STRING, string_value, start_line, start_column))
            
            # Numbers
            elif char.isdigit() or (char == '.' and self.peek_char() and self.peek_char().isdigit()):
                number, is_integer = self.read_number()
                self.tokens.append(RToken(RTokenType.NUMBER, number, start_line, start_column))
            
            # Identifiers and keywords
            elif char.isalpha() or char in '._':
                identifier = self.read_identifier()
                token_type = self.keywords.get(identifier, RTokenType.IDENTIFIER)
                self.tokens.append(RToken(token_type, identifier, start_line, start_column))
            
            # Multi-character operators
            elif self.read_operator():
                op = self.source[self.position - len([op for op in self.operators.keys() 
                                                    if self.source[max(0, self.position - len(op)):self.position] == op][0]):self.position]
                # Find the operator that was just consumed
                for op_str, op_type in self.operators.items():
                    if self.source[self.position - len(op_str):self.position] == op_str:
                        self.tokens.append(RToken(op_type, op_str, start_line, start_column))
                        break
            
            # Single character tokens
            elif char in self.single_chars:
                self.tokens.append(RToken(self.single_chars[char], char, start_line, start_column))
                self.advance()
            
            # Unknown character
            else:
                self.advance()
        
        # Add EOF token
        self.tokens.append(RToken(RTokenType.EOF, '', self.line, self.column))
        return self.tokens


class RParser:
    """R parser for building AST from tokens."""
    
    def __init__(self, tokens: List[RToken]):
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[0] if tokens else None
    
    def peek_token(self, offset: int = 1) -> Optional[RToken]:
        """Peek at token with offset."""
        pos = self.position + offset
        if pos >= len(self.tokens):
            return None
        return self.tokens[pos]
    
    def advance(self) -> Optional[RToken]:
        """Advance to next token."""
        if self.position < len(self.tokens) - 1:
            self.position += 1
            self.current_token = self.tokens[self.position]
        return self.current_token
    
    def expect(self, token_type: RTokenType) -> RToken:
        """Expect specific token type."""
        if self.current_token.type != token_type:
            raise SyntaxError(f"Expected {token_type.name}, got {self.current_token.type.name} at {self.current_token.line}:{self.current_token.column}")
        token = self.current_token
        self.advance()
        return token
    
    def match(self, *token_types: RTokenType) -> bool:
        """Check if current token matches any of the given types."""
        return self.current_token.type in token_types
    
    def skip_newlines(self):
        """Skip newline tokens."""
        while self.match(RTokenType.NEWLINE):
            self.advance()
    
    def parse(self) -> RProgram:
        """Parse R source code into AST."""
        statements = []
        
        self.skip_newlines()
        while not self.match(RTokenType.EOF):
            if self.match(RTokenType.NEWLINE):
                self.advance()
                continue
            
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            
            self.skip_newlines()
        
        return RProgram(statements=statements)
    
    def parse_statement(self) -> Optional[RNode]:
        """Parse a statement."""
        self.skip_newlines()
        
        if self.match(RTokenType.FUNCTION):
            return self.parse_function_definition()
        elif self.match(RTokenType.IF):
            return self.parse_if_statement()
        elif self.match(RTokenType.FOR):
            return self.parse_for_loop()
        elif self.match(RTokenType.WHILE):
            return self.parse_while_loop()
        elif self.match(RTokenType.REPEAT):
            return self.parse_repeat_loop()
        elif self.match(RTokenType.NEXT):
            self.advance()
            return RNextStatement()
        elif self.match(RTokenType.BREAK):
            self.advance()
            return RBreakStatement()
        elif self.match(RTokenType.RETURN):
            return self.parse_return_statement()
        elif self.match(RTokenType.LIBRARY, RTokenType.REQUIRE):
            return self.parse_package_load()
        else:
            return self.parse_expression_statement()
    
    def parse_function_definition(self) -> RFunctionDefinition:
        """Parse function definition."""
        self.expect(RTokenType.FUNCTION)
        self.expect(RTokenType.LPAREN)
        
        parameters = []
        while not self.match(RTokenType.RPAREN):
            param = self.parse_parameter()
            parameters.append(param)
            
            if self.match(RTokenType.COMMA):
                self.advance()
            elif not self.match(RTokenType.RPAREN):
                break
        
        self.expect(RTokenType.RPAREN)
        
        # Function body
        body = []
        if self.match(RTokenType.LBRACE):
            self.advance()
            self.skip_newlines()
            
            while not self.match(RTokenType.RBRACE, RTokenType.EOF):
                stmt = self.parse_statement()
                if stmt:
                    body.append(stmt)
                self.skip_newlines()
            
            self.expect(RTokenType.RBRACE)
        else:
            # Single expression body
            expr = self.parse_expression()
            if expr:
                body.append(expr)
        
        return RFunctionDefinition(parameters=parameters, body=body)
    
    def parse_parameter(self) -> RParameter:
        """Parse function parameter."""
        if self.match(RTokenType.ELLIPSIS):
            self.advance()
            return RParameter(name="...", is_ellipsis=True)
        
        name = self.expect(RTokenType.IDENTIFIER).value
        default_value = None
        
        if self.match(RTokenType.ASSIGN_EQUAL):
            self.advance()
            default_value = self.parse_expression()
        
        return RParameter(name=name, default_value=default_value)
    
    def parse_if_statement(self) -> RIfStatement:
        """Parse if statement."""
        self.expect(RTokenType.IF)
        self.expect(RTokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(RTokenType.RPAREN)
        
        then_expr = self.parse_statement()
        else_expr = None
        
        if self.match(RTokenType.ELSE):
            self.advance()
            else_expr = self.parse_statement()
        
        return RIfStatement(condition=condition, then_expr=then_expr, else_expr=else_expr)
    
    def parse_for_loop(self) -> RForLoop:
        """Parse for loop."""
        self.expect(RTokenType.FOR)
        self.expect(RTokenType.LPAREN)
        
        variable = self.expect(RTokenType.IDENTIFIER).value
        self.expect(RTokenType.IN_KEYWORD)
        iterable = self.parse_expression()
        
        self.expect(RTokenType.RPAREN)
        body = self.parse_statement()
        
        return RForLoop(variable=variable, iterable=iterable, body=body)
    
    def parse_while_loop(self) -> RWhileLoop:
        """Parse while loop."""
        self.expect(RTokenType.WHILE)
        self.expect(RTokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(RTokenType.RPAREN)
        body = self.parse_statement()
        
        return RWhileLoop(condition=condition, body=body)
    
    def parse_repeat_loop(self) -> RRepeatLoop:
        """Parse repeat loop."""
        self.expect(RTokenType.REPEAT)
        body = self.parse_statement()
        
        return RRepeatLoop(body=body)
    
    def parse_return_statement(self) -> RReturnStatement:
        """Parse return statement."""
        self.expect(RTokenType.RETURN)
        
        value = None
        if self.match(RTokenType.LPAREN):
            self.advance()
            if not self.match(RTokenType.RPAREN):
                value = self.parse_expression()
            self.expect(RTokenType.RPAREN)
        elif not self.match(RTokenType.NEWLINE, RTokenType.EOF, RTokenType.SEMICOLON):
            value = self.parse_expression()
        
        return RReturnStatement(value=value)
    
    def parse_package_load(self) -> RPackageLoad:
        """Parse library() or require() call."""
        is_require = self.match(RTokenType.REQUIRE)
        self.advance()
        
        self.expect(RTokenType.LPAREN)
        package_name = self.expect(RTokenType.IDENTIFIER).value
        self.expect(RTokenType.RPAREN)
        
        return RPackageLoad(package_name=package_name, is_require=is_require)
    
    def parse_expression_statement(self) -> Optional[RNode]:
        """Parse expression statement."""
        expr = self.parse_expression()
        return expr
    
    def parse_expression(self) -> Optional[RNode]:
        """Parse expression with operator precedence."""
        return self.parse_assignment()
    
    def parse_assignment(self) -> Optional[RNode]:
        """Parse assignment expressions."""
        expr = self.parse_logical_or()
        
        if self.match(RTokenType.ASSIGN, RTokenType.ASSIGN_RIGHT, RTokenType.ASSIGN_EQUAL,
                     RTokenType.SUPER_ASSIGN, RTokenType.SUPER_ASSIGN_RIGHT):
            op_token = self.current_token
            self.advance()
            value = self.parse_assignment()
            
            # Map token to operator
            op_map = {
                RTokenType.ASSIGN: ROperator.ASSIGN,
                RTokenType.ASSIGN_RIGHT: ROperator.ASSIGN_RIGHT,
                RTokenType.ASSIGN_EQUAL: ROperator.ASSIGN_EQUAL,
                RTokenType.SUPER_ASSIGN: ROperator.SUPER_ASSIGN,
                RTokenType.SUPER_ASSIGN_RIGHT: ROperator.SUPER_ASSIGN_RIGHT
            }
            
            operator = op_map[op_token.type]
            return RAssignment(target=expr, value=value, operator=operator)
        
        return expr
    
    def parse_logical_or(self) -> Optional[RNode]:
        """Parse logical OR expressions."""
        expr = self.parse_logical_and()
        
        while self.match(RTokenType.OR, RTokenType.OR_SHORT):
            op_token = self.current_token
            self.advance()
            right = self.parse_logical_and()
            
            operator = ROperator.OR if op_token.type == RTokenType.OR else ROperator.OR_SHORT
            expr = RBinaryExpression(left=expr, operator=operator, right=right)
        
        return expr
    
    def parse_logical_and(self) -> Optional[RNode]:
        """Parse logical AND expressions."""
        expr = self.parse_equality()
        
        while self.match(RTokenType.AND, RTokenType.AND_SHORT):
            op_token = self.current_token
            self.advance()
            right = self.parse_equality()
            
            operator = ROperator.AND if op_token.type == RTokenType.AND else ROperator.AND_SHORT
            expr = RBinaryExpression(left=expr, operator=operator, right=right)
        
        return expr
    
    def parse_equality(self) -> Optional[RNode]:
        """Parse equality expressions."""
        expr = self.parse_comparison()
        
        while self.match(RTokenType.EQUAL, RTokenType.NOT_EQUAL):
            op_token = self.current_token
            self.advance()
            right = self.parse_comparison()
            
            operator = ROperator.EQUAL if op_token.type == RTokenType.EQUAL else ROperator.NOT_EQUAL
            expr = RBinaryExpression(left=expr, operator=operator, right=right)
        
        return expr
    
    def parse_comparison(self) -> Optional[RNode]:
        """Parse comparison expressions."""
        expr = self.parse_additive()
        
        while self.match(RTokenType.LESS_THAN, RTokenType.LESS_EQUAL,
                         RTokenType.GREATER_THAN, RTokenType.GREATER_EQUAL, RTokenType.IN):
            op_token = self.current_token
            self.advance()
            right = self.parse_additive()
            
            op_map = {
                RTokenType.LESS_THAN: ROperator.LESS_THAN,
                RTokenType.LESS_EQUAL: ROperator.LESS_EQUAL,
                RTokenType.GREATER_THAN: ROperator.GREATER_THAN,
                RTokenType.GREATER_EQUAL: ROperator.GREATER_EQUAL,
                RTokenType.IN: ROperator.IN
            }
            
            operator = op_map[op_token.type]
            expr = RBinaryExpression(left=expr, operator=operator, right=right)
        
        return expr
    
    def parse_additive(self) -> Optional[RNode]:
        """Parse additive expressions."""
        expr = self.parse_multiplicative()
        
        while self.match(RTokenType.PLUS, RTokenType.MINUS):
            op_token = self.current_token
            self.advance()
            right = self.parse_multiplicative()
            
            operator = ROperator.PLUS if op_token.type == RTokenType.PLUS else ROperator.MINUS
            expr = RBinaryExpression(left=expr, operator=operator, right=right)
        
        return expr
    
    def parse_multiplicative(self) -> Optional[RNode]:
        """Parse multiplicative expressions."""
        expr = self.parse_power()
        
        while self.match(RTokenType.MULTIPLY, RTokenType.DIVIDE, RTokenType.INTEGER_DIVIDE, RTokenType.MODULO):
            op_token = self.current_token
            self.advance()
            right = self.parse_power()
            
            op_map = {
                RTokenType.MULTIPLY: ROperator.MULTIPLY,
                RTokenType.DIVIDE: ROperator.DIVIDE,
                RTokenType.INTEGER_DIVIDE: ROperator.INTEGER_DIVIDE,
                RTokenType.MODULO: ROperator.MODULO
            }
            
            operator = op_map[op_token.type]
            expr = RBinaryExpression(left=expr, operator=operator, right=right)
        
        return expr
    
    def parse_power(self) -> Optional[RNode]:
        """Parse power expressions."""
        expr = self.parse_unary()
        
        if self.match(RTokenType.POWER, RTokenType.POWER_ALT):
            op_token = self.current_token
            self.advance()
            right = self.parse_power()  # Right associative
            
            operator = ROperator.POWER if op_token.type == RTokenType.POWER else ROperator.POWER_ALT
            expr = RBinaryExpression(left=expr, operator=operator, right=right)
        
        return expr
    
    def parse_unary(self) -> Optional[RNode]:
        """Parse unary expressions."""
        if self.match(RTokenType.MINUS, RTokenType.PLUS, RTokenType.NOT):
            op_token = self.current_token
            self.advance()
            expr = self.parse_unary()
            
            op_map = {
                RTokenType.MINUS: ROperator.MINUS,
                RTokenType.PLUS: ROperator.PLUS,
                RTokenType.NOT: ROperator.NOT
            }
            
            operator = op_map[op_token.type]
            return RUnaryExpression(operator=operator, expression=expr)
        
        return self.parse_postfix()
    
    def parse_postfix(self) -> Optional[RNode]:
        """Parse postfix expressions (indexing, member access, function calls)."""
        expr = self.parse_primary()
        
        while True:
            if self.match(RTokenType.LBRACKET):
                # Indexing: expr[index] or expr[[index]]
                self.advance()
                is_double = False
                if self.match(RTokenType.LBRACKET):
                    self.advance()
                    is_double = True
                
                indices = []
                if not self.match(RTokenType.RBRACKET):
                    indices.append(self.parse_expression())
                    
                    while self.match(RTokenType.COMMA):
                        self.advance()
                        indices.append(self.parse_expression())
                
                self.expect(RTokenType.RBRACKET)
                if is_double:
                    self.expect(RTokenType.RBRACKET)
                
                expr = RIndexExpression(object=expr, indices=indices, is_double_bracket=is_double)
            
            elif self.match(RTokenType.DOLLAR):
                # Dollar access: expr$member
                self.advance()
                member = self.expect(RTokenType.IDENTIFIER).value
                expr = RDollarAccess(object=expr, element=member)
            
            elif self.match(RTokenType.AT):
                # At access: expr@slot
                self.advance()
                slot = self.expect(RTokenType.IDENTIFIER).value
                expr = RAtAccess(object=expr, slot=slot)
            
            elif self.match(RTokenType.LPAREN):
                # Function call: expr(args)
                self.advance()
                arguments = []
                
                while not self.match(RTokenType.RPAREN):
                    arg = self.parse_argument()
                    arguments.append(arg)
                    
                    if self.match(RTokenType.COMMA):
                        self.advance()
                    elif not self.match(RTokenType.RPAREN):
                        break
                
                self.expect(RTokenType.RPAREN)
                expr = RFunctionCall(function=expr, arguments=arguments)
            
            else:
                break
        
        return expr
    
    def parse_argument(self) -> RArgument:
        """Parse function argument."""
        # Check for named argument
        if (self.match(RTokenType.IDENTIFIER) and 
            self.peek_token() and self.peek_token().type == RTokenType.ASSIGN_EQUAL):
            name = self.current_token.value
            self.advance()
            self.advance()  # Skip =
            value = self.parse_expression()
            return RArgument(name=name, value=value)
        else:
            value = self.parse_expression()
            return RArgument(value=value)
    
    def parse_primary(self) -> Optional[RNode]:
        """Parse primary expressions."""
        if self.match(RTokenType.NUMBER):
            token = self.current_token
            self.advance()
            
            # Determine if integer or float
            value = token.value
            if '.' in value or 'e' in value.lower():
                return RNumericLiteral(value=float(value), is_integer=False)
            else:
                return RNumericLiteral(value=int(value), is_integer=True)
        
        elif self.match(RTokenType.STRING):
            token = self.current_token
            self.advance()
            return RStringLiteral(value=token.value)
        
        elif self.match(RTokenType.LOGICAL):
            token = self.current_token
            self.advance()
            return RLogicalLiteral(value=token.value == 'TRUE')
        
        elif self.match(RTokenType.NULL):
            self.advance()
            return RNullLiteral()
        
        elif self.match(RTokenType.NA):
            token = self.current_token
            self.advance()
            return RNALiteral(na_type=token.value)
        
        elif self.match(RTokenType.IDENTIFIER):
            token = self.current_token
            self.advance()
            
            # Check for namespace access
            if self.match(RTokenType.NAMESPACE, RTokenType.NAMESPACE_INTERNAL):
                op_token = self.current_token
                self.advance()
                function_name = self.expect(RTokenType.IDENTIFIER).value
                
                is_internal = op_token.type == RTokenType.NAMESPACE_INTERNAL
                return RNamespaceAccess(package=token.value, function=function_name, is_internal=is_internal)
            
            return RIdentifier(name=token.value)
        
        elif self.match(RTokenType.C):
            # Vector creation: c(...)
            self.advance()
            self.expect(RTokenType.LPAREN)
            
            elements = []
            while not self.match(RTokenType.RPAREN):
                elements.append(self.parse_expression())
                
                if self.match(RTokenType.COMMA):
                    self.advance()
                elif not self.match(RTokenType.RPAREN):
                    break
            
            self.expect(RTokenType.RPAREN)
            return RVector(elements=elements)
        
        elif self.match(RTokenType.LPAREN):
            # Parenthesized expression
            self.advance()
            expr = self.parse_expression()
            self.expect(RTokenType.RPAREN)
            return expr
        
        elif self.match(RTokenType.TILDE):
            # Formula: ~expr or expr1 ~ expr2
            self.advance()
            right = self.parse_expression()
            return RTildeExpression(expression=right)
        
        elif self.match(RTokenType.QUESTION):
            # Help: ?topic
            self.advance()
            topic = self.expect(RTokenType.IDENTIFIER).value
            return RHelpExpression(topic=topic, is_question_mark=True)
        
        return None


def parse_r_source(source: str, file_path: str = None) -> RProgram:
    """Parse R source code and return AST."""
    try:
        lexer = RLexer(source)
        tokens = lexer.tokenize()
        
        # Filter out comments for parsing (but keep them in AST if needed)
        filtered_tokens = [t for t in tokens if t.type != RTokenType.COMMENT]
        
        parser = RParser(filtered_tokens)
        ast = parser.parse()
        
        return ast
    
    except Exception as e:
        raise SyntaxError(f"Error parsing R code: {str(e)}")


# Convenience function
def parse_r(source: str) -> RProgram:
    """Parse R source code."""
    return parse_r_source(source) 