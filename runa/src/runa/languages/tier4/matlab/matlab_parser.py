#!/usr/bin/env python3
"""
Matlab Parser and Lexer

Complete lexical analysis and parsing for Matlab language including matrix operations,
functions, scripts, classes, and scientific computing constructs.
"""

from typing import List, Optional, Dict, Any, Union, Tuple
from enum import Enum, auto
import re
from dataclasses import dataclass

from .matlab_ast import *
from ....core.runa_ast import SourceLocation


class MatlabTokenType(Enum):
    """Token types for Matlab lexer."""
    # Literals
    NUMBER = auto()
    STRING = auto()
    CHAR_ARRAY = auto()
    LOGICAL = auto()
    
    # Identifiers
    IDENTIFIER = auto()
    
    # Keywords
    FUNCTION = auto()
    END = auto()
    IF = auto()
    ELSE = auto()
    ELSEIF = auto()
    SWITCH = auto()
    CASE = auto()
    OTHERWISE = auto()
    FOR = auto()
    WHILE = auto()
    TRY = auto()
    CATCH = auto()
    BREAK = auto()
    CONTINUE = auto()
    RETURN = auto()
    CLASSDEF = auto()
    PROPERTIES = auto()
    METHODS = auto()
    EVENTS = auto()
    ENUMERATION = auto()
    GLOBAL = auto()
    PERSISTENT = auto()
    CLEAR = auto()
    LOAD = auto()
    SAVE = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    POWER = auto()
    DOT_MULTIPLY = auto()
    DOT_DIVIDE = auto()
    DOT_POWER = auto()
    LEFT_DIVIDE = auto()
    DOT_LEFT_DIVIDE = auto()
    
    # Logical operators
    AND = auto()
    OR = auto()
    NOT = auto()
    
    # Comparison operators
    EQ = auto()
    NE = auto()
    LT = auto()
    LE = auto()
    GT = auto()
    GE = auto()
    
    # Assignment
    ASSIGN = auto()
    
    # Punctuation
    SEMICOLON = auto()
    COMMA = auto()
    COLON = auto()
    DOT = auto()
    TRANSPOSE = auto()
    
    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    LBRACE = auto()
    RBRACE = auto()
    
    # Special
    AT = auto()
    NEWLINE = auto()
    COMMENT = auto()
    BLOCK_COMMENT = auto()
    EOF = auto()


@dataclass
class MatlabToken:
    """Token for Matlab lexer."""
    type: MatlabTokenType
    value: str = ""
    location: Optional[SourceLocation] = None


class MatlabLexer:
    """Lexer for Matlab language."""
    
    KEYWORDS = {
        'function': MatlabTokenType.FUNCTION,
        'end': MatlabTokenType.END,
        'if': MatlabTokenType.IF,
        'else': MatlabTokenType.ELSE,
        'elseif': MatlabTokenType.ELSEIF,
        'switch': MatlabTokenType.SWITCH,
        'case': MatlabTokenType.CASE,
        'otherwise': MatlabTokenType.OTHERWISE,
        'for': MatlabTokenType.FOR,
        'while': MatlabTokenType.WHILE,
        'try': MatlabTokenType.TRY,
        'catch': MatlabTokenType.CATCH,
        'break': MatlabTokenType.BREAK,
        'continue': MatlabTokenType.CONTINUE,
        'return': MatlabTokenType.RETURN,
        'classdef': MatlabTokenType.CLASSDEF,
        'properties': MatlabTokenType.PROPERTIES,
        'methods': MatlabTokenType.METHODS,
        'events': MatlabTokenType.EVENTS,
        'enumeration': MatlabTokenType.ENUMERATION,
        'global': MatlabTokenType.GLOBAL,
        'persistent': MatlabTokenType.PERSISTENT,
        'clear': MatlabTokenType.CLEAR,
        'load': MatlabTokenType.LOAD,
        'save': MatlabTokenType.SAVE,
        'true': MatlabTokenType.LOGICAL,
        'false': MatlabTokenType.LOGICAL,
    }
    
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
    
    def current_char(self) -> Optional[str]:
        """Get current character."""
        if self.position >= len(self.source):
            return None
        return self.source[self.position]
    
    def peek_char(self, offset: int = 1) -> Optional[str]:
        """Peek at character ahead."""
        pos = self.position + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]
    
    def advance(self) -> None:
        """Advance position."""
        if self.position < len(self.source):
            if self.source[self.position] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.position += 1
    
    def skip_whitespace(self) -> None:
        """Skip whitespace except newlines."""
        while self.current_char() and self.current_char() in ' \t\r':
            self.advance()
    
    def read_number(self) -> MatlabToken:
        """Read numeric literal."""
        start_pos = self.position
        start_col = self.column
        
        # Handle complex numbers and scientific notation
        value = ""
        while self.current_char() and (self.current_char().isdigit() or 
                                     self.current_char() in '.eE+-i'):
            value += self.current_char()
            self.advance()
        
        return MatlabToken(
            MatlabTokenType.NUMBER,
            value,
            SourceLocation(self.line, start_col, self.line, self.column - 1)
        )
    
    def read_string(self, quote_char: str) -> MatlabToken:
        """Read string literal."""
        start_col = self.column
        value = ""
        self.advance()  # Skip opening quote
        
        while self.current_char() and self.current_char() != quote_char:
            if self.current_char() == '\\':
                self.advance()
                if self.current_char():
                    value += self.current_char()
                    self.advance()
            else:
                value += self.current_char()
                self.advance()
        
        if self.current_char() == quote_char:
            self.advance()  # Skip closing quote
        
        token_type = MatlabTokenType.CHAR_ARRAY if quote_char == "'" else MatlabTokenType.STRING
        
        return MatlabToken(
            token_type,
            value,
            SourceLocation(self.line, start_col, self.line, self.column - 1)
        )
    
    def read_identifier(self) -> MatlabToken:
        """Read identifier or keyword."""
        start_col = self.column
        value = ""
        
        while (self.current_char() and 
               (self.current_char().isalnum() or self.current_char() == '_')):
            value += self.current_char()
            self.advance()
        
        token_type = self.KEYWORDS.get(value, MatlabTokenType.IDENTIFIER)
        
        return MatlabToken(
            token_type,
            value,
            SourceLocation(self.line, start_col, self.line, self.column - 1)
        )
    
    def read_comment(self) -> MatlabToken:
        """Read comment."""
        start_col = self.column
        
        if self.current_char() == '%' and self.peek_char() == '{':
            # Block comment
            self.advance()  # Skip %
            self.advance()  # Skip {
            value = ""
            
            while self.current_char():
                if self.current_char() == '%' and self.peek_char() == '}':
                    self.advance()  # Skip %
                    self.advance()  # Skip }
                    break
                value += self.current_char()
                self.advance()
            
            return MatlabToken(
                MatlabTokenType.BLOCK_COMMENT,
                value,
                SourceLocation(self.line, start_col, self.line, self.column - 1)
            )
        else:
            # Line comment
            self.advance()  # Skip %
            value = ""
            
            while self.current_char() and self.current_char() != '\n':
                value += self.current_char()
                self.advance()
            
            return MatlabToken(
                MatlabTokenType.COMMENT,
                value,
                SourceLocation(self.line, start_col, self.line, self.column - 1)
            )
    
    def tokenize(self) -> List[MatlabToken]:
        """Tokenize the source code."""
        tokens = []
        
        while self.position < len(self.source):
            self.skip_whitespace()
            
            char = self.current_char()
            if not char:
                break
            
            start_col = self.column
            
            # Numbers
            if char.isdigit() or (char == '.' and self.peek_char() and self.peek_char().isdigit()):
                tokens.append(self.read_number())
            
            # Strings and char arrays
            elif char in '"\'':
                tokens.append(self.read_string(char))
            
            # Comments
            elif char == '%':
                tokens.append(self.read_comment())
            
            # Identifiers and keywords
            elif char.isalpha() or char == '_':
                tokens.append(self.read_identifier())
            
            # Operators and punctuation
            else:
                self.advance()
                
                if char == '+':
                    tokens.append(MatlabToken(MatlabTokenType.PLUS, char))
                elif char == '-':
                    tokens.append(MatlabToken(MatlabTokenType.MINUS, char))
                elif char == '*':
                    tokens.append(MatlabToken(MatlabTokenType.MULTIPLY, char))
                elif char == '/':
                    tokens.append(MatlabToken(MatlabTokenType.DIVIDE, char))
                elif char == '^':
                    tokens.append(MatlabToken(MatlabTokenType.POWER, char))
                elif char == '\\':
                    tokens.append(MatlabToken(MatlabTokenType.LEFT_DIVIDE, char))
                elif char == '.' and self.current_char() == '*':
                    self.advance()
                    tokens.append(MatlabToken(MatlabTokenType.DOT_MULTIPLY, '.*'))
                elif char == '.' and self.current_char() == '/':
                    self.advance()
                    tokens.append(MatlabToken(MatlabTokenType.DOT_DIVIDE, './'))
                elif char == '.' and self.current_char() == '^':
                    self.advance()
                    tokens.append(MatlabToken(MatlabTokenType.DOT_POWER, '.^'))
                elif char == '.' and self.current_char() == '\\':
                    self.advance()
                    tokens.append(MatlabToken(MatlabTokenType.DOT_LEFT_DIVIDE, '.\\'))
                elif char == '.' and self.current_char() == "'":
                    self.advance()
                    tokens.append(MatlabToken(MatlabTokenType.TRANSPOSE, ".'"))
                elif char == '.':
                    tokens.append(MatlabToken(MatlabTokenType.DOT, char))
                elif char == '=' and self.current_char() == '=':
                    self.advance()
                    tokens.append(MatlabToken(MatlabTokenType.EQ, '=='))
                elif char == '~' and self.current_char() == '=':
                    self.advance()
                    tokens.append(MatlabToken(MatlabTokenType.NE, '~='))
                elif char == '<' and self.current_char() == '=':
                    self.advance()
                    tokens.append(MatlabToken(MatlabTokenType.LE, '<='))
                elif char == '>' and self.current_char() == '=':
                    self.advance()
                    tokens.append(MatlabToken(MatlabTokenType.GE, '>='))
                elif char == '&' and self.current_char() == '&':
                    self.advance()
                    tokens.append(MatlabToken(MatlabTokenType.AND, '&&'))
                elif char == '|' and self.current_char() == '|':
                    self.advance()
                    tokens.append(MatlabToken(MatlabTokenType.OR, '||'))
                elif char == '=':
                    tokens.append(MatlabToken(MatlabTokenType.ASSIGN, char))
                elif char == '<':
                    tokens.append(MatlabToken(MatlabTokenType.LT, char))
                elif char == '>':
                    tokens.append(MatlabToken(MatlabTokenType.GT, char))
                elif char == '~':
                    tokens.append(MatlabToken(MatlabTokenType.NOT, char))
                elif char == '&':
                    tokens.append(MatlabToken(MatlabTokenType.AND, char))
                elif char == '|':
                    tokens.append(MatlabToken(MatlabTokenType.OR, char))
                elif char == ';':
                    tokens.append(MatlabToken(MatlabTokenType.SEMICOLON, char))
                elif char == ',':
                    tokens.append(MatlabToken(MatlabTokenType.COMMA, char))
                elif char == ':':
                    tokens.append(MatlabToken(MatlabTokenType.COLON, char))
                elif char == '(':
                    tokens.append(MatlabToken(MatlabTokenType.LPAREN, char))
                elif char == ')':
                    tokens.append(MatlabToken(MatlabTokenType.RPAREN, char))
                elif char == '[':
                    tokens.append(MatlabToken(MatlabTokenType.LBRACKET, char))
                elif char == ']':
                    tokens.append(MatlabToken(MatlabTokenType.RBRACKET, char))
                elif char == '{':
                    tokens.append(MatlabToken(MatlabTokenType.LBRACE, char))
                elif char == '}':
                    tokens.append(MatlabToken(MatlabTokenType.RBRACE, char))
                elif char == '@':
                    tokens.append(MatlabToken(MatlabTokenType.AT, char))
                elif char == "'":
                    tokens.append(MatlabToken(MatlabTokenType.TRANSPOSE, char))
                elif char == '\n':
                    tokens.append(MatlabToken(MatlabTokenType.NEWLINE, char))
        
        tokens.append(MatlabToken(MatlabTokenType.EOF, ""))
        return tokens


class MatlabParser:
    """Parser for Matlab language."""
    
    def __init__(self, tokens: List[MatlabToken]):
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[0] if tokens else None
    
    def advance(self) -> None:
        """Advance to next token."""
        if self.position < len(self.tokens) - 1:
            self.position += 1
            self.current_token = self.tokens[self.position]
    
    def peek(self, offset: int = 1) -> Optional[MatlabToken]:
        """Peek at token ahead."""
        pos = self.position + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return None
    
    def match(self, token_type: MatlabTokenType) -> bool:
        """Check if current token matches type."""
        return self.current_token and self.current_token.type == token_type
    
    def consume(self, token_type: MatlabTokenType) -> MatlabToken:
        """Consume token of expected type."""
        if not self.match(token_type):
            raise SyntaxError(f"Expected {token_type}, got {self.current_token.type if self.current_token else 'EOF'}")
        token = self.current_token
        self.advance()
        return token
    
    def skip_newlines(self) -> None:
        """Skip newline tokens."""
        while self.match(MatlabTokenType.NEWLINE):
            self.advance()
    
    def parse_script(self) -> MatlabScript:
        """Parse a Matlab script."""
        statements = []
        comments = []
        
        while not self.match(MatlabTokenType.EOF):
            self.skip_newlines()
            
            if self.match(MatlabTokenType.EOF):
                break
            
            if self.match(MatlabTokenType.COMMENT) or self.match(MatlabTokenType.BLOCK_COMMENT):
                comment = MatlabComment(
                    text=self.current_token.value,
                    is_block_comment=self.match(MatlabTokenType.BLOCK_COMMENT)
                )
                comments.append(comment)
                self.advance()
            else:
                stmt = self.parse_statement()
                if stmt:
                    statements.append(stmt)
        
        return MatlabScript(statements=statements, comments=comments)
    
    def parse_statement(self) -> Optional[MatlabNode]:
        """Parse a statement."""
        if self.match(MatlabTokenType.FUNCTION):
            return self.parse_function()
        elif self.match(MatlabTokenType.CLASSDEF):
            return self.parse_class()
        elif self.match(MatlabTokenType.IF):
            return self.parse_if_statement()
        elif self.match(MatlabTokenType.FOR):
            return self.parse_for_loop()
        elif self.match(MatlabTokenType.WHILE):
            return self.parse_while_loop()
        elif self.match(MatlabTokenType.TRY):
            return self.parse_try_catch()
        elif self.match(MatlabTokenType.SWITCH):
            return self.parse_switch_statement()
        elif self.match(MatlabTokenType.GLOBAL):
            return self.parse_global_declaration()
        elif self.match(MatlabTokenType.PERSISTENT):
            return self.parse_persistent_declaration()
        elif self.match(MatlabTokenType.BREAK):
            self.advance()
            return MatlabBreakStatement()
        elif self.match(MatlabTokenType.CONTINUE):
            self.advance()
            return MatlabContinueStatement()
        elif self.match(MatlabTokenType.RETURN):
            self.advance()
            return MatlabReturnStatement()
        else:
            return self.parse_expression_statement()
    
    def parse_function(self) -> MatlabFunctionDeclaration:
        """Parse function declaration."""
        self.consume(MatlabTokenType.FUNCTION)
        
        # Parse output parameters
        outputs = []
        if self.match(MatlabTokenType.LBRACKET):
            self.advance()
            while not self.match(MatlabTokenType.RBRACKET):
                if self.match(MatlabTokenType.IDENTIFIER):
                    outputs.append(self.current_token.value)
                    self.advance()
                if self.match(MatlabTokenType.COMMA):
                    self.advance()
            self.consume(MatlabTokenType.RBRACKET)
            self.consume(MatlabTokenType.ASSIGN)
        elif self.match(MatlabTokenType.IDENTIFIER) and self.peek() and self.peek().type == MatlabTokenType.ASSIGN:
            outputs.append(self.current_token.value)
            self.advance()
            self.consume(MatlabTokenType.ASSIGN)
        
        # Parse function name
        name = self.consume(MatlabTokenType.IDENTIFIER).value
        
        # Parse input parameters
        inputs = []
        if self.match(MatlabTokenType.LPAREN):
            self.advance()
            while not self.match(MatlabTokenType.RPAREN):
                if self.match(MatlabTokenType.IDENTIFIER):
                    inputs.append(self.current_token.value)
                    self.advance()
                if self.match(MatlabTokenType.COMMA):
                    self.advance()
            self.consume(MatlabTokenType.RPAREN)
        
        self.skip_newlines()
        
        # Parse function body
        body = []
        while not self.match(MatlabTokenType.END) and not self.match(MatlabTokenType.EOF):
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            self.skip_newlines()
        
        self.consume(MatlabTokenType.END)
        
        return MatlabFunctionDeclaration(
            name=name,
            input_parameters=inputs,
            output_parameters=outputs,
            body=body
        )
    
    def parse_expression_statement(self) -> Optional[MatlabNode]:
        """Parse expression statement."""
        expr = self.parse_expression()
        
        # Skip optional semicolon or newline
        if self.match(MatlabTokenType.SEMICOLON):
            self.advance()
        elif self.match(MatlabTokenType.NEWLINE):
            self.advance()
        
        return expr
    
    def parse_expression(self) -> MatlabExpression:
        """Parse expression."""
        return self.parse_assignment()
    
    def parse_assignment(self) -> MatlabExpression:
        """Parse assignment expression."""
        expr = self.parse_logical_or()
        
        if self.match(MatlabTokenType.ASSIGN):
            self.advance()
            value = self.parse_assignment()
            
            # Handle multiple assignment targets
            targets = [expr] if not isinstance(expr, MatlabMatrixExpression) else expr.rows[0]
            return MatlabAssignmentExpression(targets=targets, value=value)
        
        return expr
    
    def parse_logical_or(self) -> MatlabExpression:
        """Parse logical OR expression."""
        expr = self.parse_logical_and()
        
        while self.match(MatlabTokenType.OR):
            op = self.current_token.value
            self.advance()
            right = self.parse_logical_and()
            expr = MatlabBinaryExpression(left=expr, operator=op, right=right)
        
        return expr
    
    def parse_logical_and(self) -> MatlabExpression:
        """Parse logical AND expression."""
        expr = self.parse_equality()
        
        while self.match(MatlabTokenType.AND):
            op = self.current_token.value
            self.advance()
            right = self.parse_equality()
            expr = MatlabBinaryExpression(left=expr, operator=op, right=right)
        
        return expr
    
    def parse_equality(self) -> MatlabExpression:
        """Parse equality expression."""
        expr = self.parse_comparison()
        
        while self.match(MatlabTokenType.EQ) or self.match(MatlabTokenType.NE):
            op = self.current_token.value
            self.advance()
            right = self.parse_comparison()
            expr = MatlabBinaryExpression(left=expr, operator=op, right=right)
        
        return expr
    
    def parse_comparison(self) -> MatlabExpression:
        """Parse comparison expression."""
        expr = self.parse_addition()
        
        while (self.match(MatlabTokenType.LT) or self.match(MatlabTokenType.LE) or
               self.match(MatlabTokenType.GT) or self.match(MatlabTokenType.GE)):
            op = self.current_token.value
            self.advance()
            right = self.parse_addition()
            expr = MatlabBinaryExpression(left=expr, operator=op, right=right)
        
        return expr
    
    def parse_addition(self) -> MatlabExpression:
        """Parse addition/subtraction."""
        expr = self.parse_multiplication()
        
        while self.match(MatlabTokenType.PLUS) or self.match(MatlabTokenType.MINUS):
            op = self.current_token.value
            self.advance()
            right = self.parse_multiplication()
            expr = MatlabBinaryExpression(left=expr, operator=op, right=right)
        
        return expr
    
    def parse_multiplication(self) -> MatlabExpression:
        """Parse multiplication/division."""
        expr = self.parse_power()
        
        while (self.match(MatlabTokenType.MULTIPLY) or self.match(MatlabTokenType.DIVIDE) or
               self.match(MatlabTokenType.DOT_MULTIPLY) or self.match(MatlabTokenType.DOT_DIVIDE) or
               self.match(MatlabTokenType.LEFT_DIVIDE) or self.match(MatlabTokenType.DOT_LEFT_DIVIDE)):
            op = self.current_token.value
            is_elementwise = op.startswith('.')
            self.advance()
            right = self.parse_power()
            expr = MatlabBinaryExpression(left=expr, operator=op, right=right, is_elementwise=is_elementwise)
        
        return expr
    
    def parse_power(self) -> MatlabExpression:
        """Parse power expression."""
        expr = self.parse_unary()
        
        while self.match(MatlabTokenType.POWER) or self.match(MatlabTokenType.DOT_POWER):
            op = self.current_token.value
            is_elementwise = op.startswith('.')
            self.advance()
            right = self.parse_unary()
            expr = MatlabBinaryExpression(left=expr, operator=op, right=right, is_elementwise=is_elementwise)
        
        return expr
    
    def parse_unary(self) -> MatlabExpression:
        """Parse unary expression."""
        if self.match(MatlabTokenType.MINUS) or self.match(MatlabTokenType.NOT):
            op = self.current_token.value
            self.advance()
            expr = self.parse_unary()
            return MatlabUnaryExpression(operator=op, expression=expr)
        
        return self.parse_postfix()
    
    def parse_postfix(self) -> MatlabExpression:
        """Parse postfix expression (transpose, indexing, field access)."""
        expr = self.parse_primary()
        
        while True:
            if self.match(MatlabTokenType.TRANSPOSE):
                self.advance()
                expr = MatlabUnaryExpression(operator="'", expression=expr, is_postfix=True)
            elif self.match(MatlabTokenType.LPAREN):
                # Function call or indexing
                self.advance()
                args = []
                while not self.match(MatlabTokenType.RPAREN):
                    args.append(self.parse_expression())
                    if self.match(MatlabTokenType.COMMA):
                        self.advance()
                self.consume(MatlabTokenType.RPAREN)
                
                if isinstance(expr, MatlabIdentifier):
                    expr = MatlabFunctionCall(function=expr, arguments=args)
                else:
                    expr = MatlabIndexingExpression(array=expr, indices=args, indexing_type="paren")
            elif self.match(MatlabTokenType.LBRACE):
                # Cell indexing
                self.advance()
                indices = []
                while not self.match(MatlabTokenType.RBRACE):
                    indices.append(self.parse_expression())
                    if self.match(MatlabTokenType.COMMA):
                        self.advance()
                self.consume(MatlabTokenType.RBRACE)
                expr = MatlabIndexingExpression(array=expr, indices=indices, indexing_type="brace")
            elif self.match(MatlabTokenType.DOT) and self.peek() and self.peek().type == MatlabTokenType.IDENTIFIER:
                # Field access
                self.advance()
                field_name = self.consume(MatlabTokenType.IDENTIFIER).value
                expr = MatlabFieldAccess(object=expr, field_name=field_name)
            else:
                break
        
        return expr
    
    def parse_primary(self) -> MatlabExpression:
        """Parse primary expression."""
        if self.match(MatlabTokenType.NUMBER):
            value = self.current_token.value
            self.advance()
            return MatlabLiteralExpression(value=float(value) if '.' in value else int(value))
        
        elif self.match(MatlabTokenType.STRING):
            value = self.current_token.value
            self.advance()
            return MatlabStringExpression(value=value, is_char_array=False)
        
        elif self.match(MatlabTokenType.CHAR_ARRAY):
            value = self.current_token.value
            self.advance()
            return MatlabStringExpression(value=value, is_char_array=True)
        
        elif self.match(MatlabTokenType.LOGICAL):
            value = self.current_token.value == 'true'
            self.advance()
            return MatlabLiteralExpression(value=value, literal_type="logical")
        
        elif self.match(MatlabTokenType.IDENTIFIER):
            name = self.current_token.value
            self.advance()
            return MatlabIdentifier(name=name)
        
        elif self.match(MatlabTokenType.LBRACKET):
            return self.parse_matrix()
        
        elif self.match(MatlabTokenType.LBRACE):
            return self.parse_cell_array()
        
        elif self.match(MatlabTokenType.LPAREN):
            self.advance()
            expr = self.parse_expression()
            self.consume(MatlabTokenType.RPAREN)
            return expr
        
        elif self.match(MatlabTokenType.AT):
            return self.parse_function_handle()
        
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token.type if self.current_token else 'EOF'}")
    
    def parse_matrix(self) -> MatlabMatrixExpression:
        """Parse matrix expression."""
        self.consume(MatlabTokenType.LBRACKET)
        rows = []
        
        if not self.match(MatlabTokenType.RBRACKET):
            # Parse first row
            row = []
            row.append(self.parse_expression())
            
            while self.match(MatlabTokenType.COMMA) or (self.match(MatlabTokenType.IDENTIFIER) and not self.match(MatlabTokenType.SEMICOLON)):
                if self.match(MatlabTokenType.COMMA):
                    self.advance()
                row.append(self.parse_expression())
            
            rows.append(row)
            
            # Parse additional rows
            while self.match(MatlabTokenType.SEMICOLON):
                self.advance()
                if self.match(MatlabTokenType.RBRACKET):
                    break
                
                row = []
                row.append(self.parse_expression())
                
                while self.match(MatlabTokenType.COMMA):
                    self.advance()
                    row.append(self.parse_expression())
                
                rows.append(row)
        
        self.consume(MatlabTokenType.RBRACKET)
        return MatlabMatrixExpression(rows=rows)
    
    def parse_cell_array(self) -> MatlabCellArray:
        """Parse cell array expression."""
        self.consume(MatlabTokenType.LBRACE)
        rows = []
        
        if not self.match(MatlabTokenType.RBRACE):
            # Parse first row
            row = []
            row.append(self.parse_expression())
            
            while self.match(MatlabTokenType.COMMA):
                self.advance()
                row.append(self.parse_expression())
            
            rows.append(row)
            
            # Parse additional rows
            while self.match(MatlabTokenType.SEMICOLON):
                self.advance()
                if self.match(MatlabTokenType.RBRACE):
                    break
                
                row = []
                row.append(self.parse_expression())
                
                while self.match(MatlabTokenType.COMMA):
                    self.advance()
                    row.append(self.parse_expression())
                
                rows.append(row)
        
        self.consume(MatlabTokenType.RBRACE)
        return MatlabCellArray(rows=rows)
    
    def parse_function_handle(self) -> Union[MatlabFunctionHandle, MatlabAnonymousFunction]:
        """Parse function handle or anonymous function."""
        self.consume(MatlabTokenType.AT)
        
        if self.match(MatlabTokenType.LPAREN):
            # Anonymous function
            self.advance()
            params = []
            
            while not self.match(MatlabTokenType.RPAREN):
                if self.match(MatlabTokenType.IDENTIFIER):
                    params.append(self.current_token.value)
                    self.advance()
                if self.match(MatlabTokenType.COMMA):
                    self.advance()
            
            self.consume(MatlabTokenType.RPAREN)
            expression = self.parse_expression()
            
            return MatlabAnonymousFunction(parameters=params, expression=expression)
        
        elif self.match(MatlabTokenType.IDENTIFIER):
            # Function handle
            name = self.current_token.value
            self.advance()
            return MatlabFunctionHandle(function_name=name)
        
        else:
            raise SyntaxError("Expected function name or anonymous function after @")


def parse_matlab_source(source: str) -> MatlabScript:
    """Parse Matlab source code into AST."""
    lexer = MatlabLexer(source)
    tokens = lexer.tokenize()
    
    # Filter out comments for parsing (but keep them for documentation)
    parsing_tokens = [t for t in tokens if t.type not in [MatlabTokenType.COMMENT, MatlabTokenType.BLOCK_COMMENT]]
    
    parser = MatlabParser(parsing_tokens)
    return parser.parse_script() 