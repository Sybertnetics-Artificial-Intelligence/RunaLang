#!/usr/bin/env python3
"""
Starlark Parser Implementation

This module provides a comprehensive parser for the Starlark language, converting
Starlark source code into Abstract Syntax Tree (AST) nodes.

Starlark is a Python-like configuration language with restricted syntax for determinism.
This parser handles all Starlark constructs including:
- Basic expressions (literals, identifiers, operations)
- Control flow (if, for loops)
- Function definitions and calls
- Collections (lists, dicts, tuples)
- Starlark-specific constructs (load, rule, aspect, provider)
- Comprehensions and lambda expressions

The parser is implemented as a recursive descent parser with proper error handling.
"""

import re
from typing import List, Optional, Union, Dict, Any, Iterator, Tuple
from enum import Enum
from dataclasses import dataclass

from .starlark_ast import *


class TokenType(Enum):
    """Starlark token types."""
    
    # Literals
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    STRING = "STRING"
    TRUE = "TRUE"
    FALSE = "FALSE"
    NONE = "NONE"
    
    # Identifiers and keywords
    IDENTIFIER = "IDENTIFIER"
    
    # Keywords
    AND = "AND"
    OR = "OR"
    NOT = "NOT"
    IF = "IF"
    ELSE = "ELSE"
    ELIF = "ELIF"
    FOR = "FOR"
    IN = "IN"
    BREAK = "BREAK"
    CONTINUE = "CONTINUE"
    DEF = "DEF"
    RETURN = "RETURN"
    PASS = "PASS"
    LAMBDA = "LAMBDA"
    LOAD = "LOAD"
    
    # Operators
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    FLOOR_DIVIDE = "FLOOR_DIVIDE"
    MODULO = "MODULO"
    POWER = "POWER"
    
    # Bitwise operators
    BIT_OR = "BIT_OR"
    BIT_XOR = "BIT_XOR"
    BIT_AND = "BIT_AND"
    LEFT_SHIFT = "LEFT_SHIFT"
    RIGHT_SHIFT = "RIGHT_SHIFT"
    BIT_NOT = "BIT_NOT"
    
    # Comparison operators
    EQUAL = "EQUAL"
    NOT_EQUAL = "NOT_EQUAL"
    LESS_THAN = "LESS_THAN"
    LESS_EQUAL = "LESS_EQUAL"
    GREATER_THAN = "GREATER_THAN"
    GREATER_EQUAL = "GREATER_EQUAL"
    
    # Assignment operators
    ASSIGN = "ASSIGN"
    PLUS_ASSIGN = "PLUS_ASSIGN"
    MINUS_ASSIGN = "MINUS_ASSIGN"
    MULTIPLY_ASSIGN = "MULTIPLY_ASSIGN"
    DIVIDE_ASSIGN = "DIVIDE_ASSIGN"
    FLOOR_DIVIDE_ASSIGN = "FLOOR_DIVIDE_ASSIGN"
    MODULO_ASSIGN = "MODULO_ASSIGN"
    
    # Delimiters
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"
    LEFT_BRACKET = "LEFT_BRACKET"
    RIGHT_BRACKET = "RIGHT_BRACKET"
    LEFT_BRACE = "LEFT_BRACE"
    RIGHT_BRACE = "RIGHT_BRACE"
    
    # Punctuation
    COMMA = "COMMA"
    COLON = "COLON"
    SEMICOLON = "SEMICOLON"
    DOT = "DOT"
    
    # Special
    NEWLINE = "NEWLINE"
    INDENT = "INDENT"
    DEDENT = "DEDENT"
    EOF = "EOF"
    
    # Comments
    COMMENT = "COMMENT"


@dataclass
class Token:
    """Represents a token in Starlark source code."""
    
    type: TokenType
    value: str
    line: int
    column: int
    
    def __str__(self) -> str:
        return f"Token({self.type.value}, {repr(self.value)}, {self.line}:{self.column})"


class StarlarkLexer:
    """Lexical analyzer for Starlark source code."""
    
    KEYWORDS = {
        'and': TokenType.AND,
        'or': TokenType.OR,
        'not': TokenType.NOT,
        'if': TokenType.IF,
        'else': TokenType.ELSE,
        'elif': TokenType.ELIF,
        'for': TokenType.FOR,
        'in': TokenType.IN,
        'break': TokenType.BREAK,
        'continue': TokenType.CONTINUE,
        'def': TokenType.DEF,
        'return': TokenType.RETURN,
        'pass': TokenType.PASS,
        'lambda': TokenType.LAMBDA,
        'load': TokenType.LOAD,
        'True': TokenType.TRUE,
        'False': TokenType.FALSE,
        'None': TokenType.NONE,
    }
    
    OPERATORS = {
        '+': TokenType.PLUS,
        '-': TokenType.MINUS,
        '*': TokenType.MULTIPLY,
        '/': TokenType.DIVIDE,
        '//': TokenType.FLOOR_DIVIDE,
        '%': TokenType.MODULO,
        '**': TokenType.POWER,
        '|': TokenType.BIT_OR,
        '^': TokenType.BIT_XOR,
        '&': TokenType.BIT_AND,
        '<<': TokenType.LEFT_SHIFT,
        '>>': TokenType.RIGHT_SHIFT,
        '~': TokenType.BIT_NOT,
        '==': TokenType.EQUAL,
        '!=': TokenType.NOT_EQUAL,
        '<': TokenType.LESS_THAN,
        '<=': TokenType.LESS_EQUAL,
        '>': TokenType.GREATER_THAN,
        '>=': TokenType.GREATER_EQUAL,
        '=': TokenType.ASSIGN,
        '+=': TokenType.PLUS_ASSIGN,
        '-=': TokenType.MINUS_ASSIGN,
        '*=': TokenType.MULTIPLY_ASSIGN,
        '/=': TokenType.DIVIDE_ASSIGN,
        '//=': TokenType.FLOOR_DIVIDE_ASSIGN,
        '%=': TokenType.MODULO_ASSIGN,
    }
    
    DELIMITERS = {
        '(': TokenType.LEFT_PAREN,
        ')': TokenType.RIGHT_PAREN,
        '[': TokenType.LEFT_BRACKET,
        ']': TokenType.RIGHT_BRACKET,
        '{': TokenType.LEFT_BRACE,
        '}': TokenType.RIGHT_BRACE,
        ',': TokenType.COMMA,
        ':': TokenType.COLON,
        ';': TokenType.SEMICOLON,
        '.': TokenType.DOT,
    }
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        self.indent_stack = [0]
    
    def error(self, message: str) -> Exception:
        """Create a lexer error with position information."""
        return SyntaxError(f"Line {self.line}, Column {self.column}: {message}")
    
    def peek(self, offset: int = 0) -> str:
        """Peek at a character without consuming it."""
        pos = self.pos + offset
        if pos >= len(self.source):
            return '\0'
        return self.source[pos]
    
    def advance(self) -> str:
        """Consume and return the current character."""
        if self.pos >= len(self.source):
            return '\0'
        
        char = self.source[self.pos]
        self.pos += 1
        
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        
        return char
    
    def skip_whitespace(self) -> None:
        """Skip whitespace characters (except newlines)."""
        while self.peek() in ' \t\r':
            self.advance()
    
    def read_string(self) -> str:
        """Read a string literal."""
        quote = self.advance()  # Opening quote
        value = ""
        
        # Handle triple-quoted strings
        if self.peek() == quote and self.peek(1) == quote:
            self.advance()  # Second quote
            self.advance()  # Third quote
            triple_quote = True
        else:
            triple_quote = False
        
        while True:
            char = self.peek()
            
            if char == '\0':
                raise self.error("Unterminated string literal")
            
            if triple_quote:
                if char == quote and self.peek(1) == quote and self.peek(2) == quote:
                    self.advance()  # First quote
                    self.advance()  # Second quote
                    self.advance()  # Third quote
                    break
            else:
                if char == quote:
                    self.advance()
                    break
                if char == '\n':
                    raise self.error("Unterminated string literal")
            
            if char == '\\':
                self.advance()
                escape_char = self.advance()
                escape_sequences = {
                    'n': '\n',
                    't': '\t',
                    'r': '\r',
                    '\\': '\\',
                    '\'': '\'',
                    '"': '"',
                    '0': '\0'
                }
                value += escape_sequences.get(escape_char, escape_char)
            else:
                value += self.advance()
        
        return value
    
    def read_number(self) -> Union[int, float]:
        """Read a numeric literal."""
        value = ""
        is_float = False
        
        # Handle negative numbers
        if self.peek() == '-':
            value += self.advance()
        
        while self.peek().isdigit():
            value += self.advance()
        
        # Check for decimal point
        if self.peek() == '.':
            is_float = True
            value += self.advance()
            while self.peek().isdigit():
                value += self.advance()
        
        # Check for scientific notation
        if self.peek().lower() == 'e':
            is_float = True
            value += self.advance()
            if self.peek() in '+-':
                value += self.advance()
            while self.peek().isdigit():
                value += self.advance()
        
        return float(value) if is_float else int(value)
    
    def read_identifier(self) -> str:
        """Read an identifier or keyword."""
        value = ""
        
        while self.peek().isalnum() or self.peek() == '_':
            value += self.advance()
        
        return value
    
    def read_comment(self) -> str:
        """Read a comment."""
        comment = ""
        self.advance()  # Skip '#'
        
        while self.peek() != '\n' and self.peek() != '\0':
            comment += self.advance()
        
        return comment
    
    def handle_indentation(self, line: str) -> List[Token]:
        """Handle indentation for a line."""
        tokens = []
        indent_level = 0
        
        for char in line:
            if char == ' ':
                indent_level += 1
            elif char == '\t':
                indent_level += 8  # Tab = 8 spaces
            else:
                break
        
        current_indent = self.indent_stack[-1]
        
        if indent_level > current_indent:
            self.indent_stack.append(indent_level)
            tokens.append(Token(TokenType.INDENT, "", self.line, 1))
        elif indent_level < current_indent:
            while len(self.indent_stack) > 1 and self.indent_stack[-1] > indent_level:
                self.indent_stack.pop()
                tokens.append(Token(TokenType.DEDENT, "", self.line, 1))
            
            if self.indent_stack[-1] != indent_level:
                raise self.error("Indentation error")
        
        return tokens
    
    def tokenize(self) -> List[Token]:
        """Tokenize the source code."""
        lines = self.source.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            self.line = line_num
            self.column = 1
            self.pos = 0
            
            # Skip empty lines
            if line.strip() == "":
                continue
            
            # Handle indentation
            indent_tokens = self.handle_indentation(line)
            self.tokens.extend(indent_tokens)
            
            # Reset position for line processing
            line_source = line
            self.pos = 0
            self.column = 1
            
            while self.pos < len(line_source):
                char = self.peek()
                
                if char == '\0':
                    break
                
                # Skip whitespace
                if char in ' \t':
                    self.skip_whitespace()
                    continue
                
                # Comments
                if char == '#':
                    comment = self.read_comment()
                    self.tokens.append(Token(TokenType.COMMENT, comment, self.line, self.column))
                    break
                
                # String literals
                if char in '"\'':
                    string_value = self.read_string()
                    self.tokens.append(Token(TokenType.STRING, string_value, self.line, self.column))
                    continue
                
                # Numbers
                if char.isdigit() or (char == '.' and self.peek(1).isdigit()):
                    number = self.read_number()
                    token_type = TokenType.FLOAT if isinstance(number, float) else TokenType.INTEGER
                    self.tokens.append(Token(token_type, str(number), self.line, self.column))
                    continue
                
                # Identifiers and keywords
                if char.isalpha() or char == '_':
                    identifier = self.read_identifier()
                    token_type = self.KEYWORDS.get(identifier, TokenType.IDENTIFIER)
                    self.tokens.append(Token(token_type, identifier, self.line, self.column))
                    continue
                
                # Multi-character operators
                two_char = char + self.peek(1)
                three_char = two_char + self.peek(2)
                
                if three_char in self.OPERATORS:
                    self.advance()
                    self.advance()
                    self.advance()
                    self.tokens.append(Token(self.OPERATORS[three_char], three_char, self.line, self.column))
                    continue
                
                if two_char in self.OPERATORS:
                    self.advance()
                    self.advance()
                    self.tokens.append(Token(self.OPERATORS[two_char], two_char, self.line, self.column))
                    continue
                
                # Single-character operators and delimiters
                if char in self.OPERATORS:
                    self.advance()
                    self.tokens.append(Token(self.OPERATORS[char], char, self.line, self.column))
                    continue
                
                if char in self.DELIMITERS:
                    self.advance()
                    self.tokens.append(Token(self.DELIMITERS[char], char, self.line, self.column))
                    continue
                
                # Unknown character
                raise self.error(f"Unexpected character: {char}")
            
            # Add newline token at end of line (except last line)
            if line_num < len(lines):
                self.tokens.append(Token(TokenType.NEWLINE, "\n", self.line, self.column))
        
        # Add remaining DEDENT tokens
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            self.tokens.append(Token(TokenType.DEDENT, "", self.line, self.column))
        
        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        
        return self.tokens


class StarlarkParser:
    """Parser for Starlark source code."""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[0] if tokens else None
    
    def error(self, message: str) -> Exception:
        """Create a parser error with token position information."""
        if self.current_token:
            return SyntaxError(f"Line {self.current_token.line}, Column {self.current_token.column}: {message}")
        return SyntaxError(message)
    
    def advance(self) -> Token:
        """Move to the next token."""
        token = self.current_token
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
            self.current_token = self.tokens[self.pos]
        return token
    
    def peek(self, offset: int = 0) -> Optional[Token]:
        """Peek at a token without consuming it."""
        pos = self.pos + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return None
    
    def match(self, *token_types: TokenType) -> bool:
        """Check if current token matches any of the given types."""
        return self.current_token and self.current_token.type in token_types
    
    def expect(self, token_type: TokenType) -> Token:
        """Expect a specific token type and consume it."""
        if not self.match(token_type):
            raise self.error(f"Expected {token_type.value}, got {self.current_token.type.value if self.current_token else 'EOF'}")
        return self.advance()
    
    def skip_newlines(self) -> None:
        """Skip newline tokens."""
        while self.match(TokenType.NEWLINE):
            self.advance()
    
    def parse_module(self) -> StarlarkModule:
        """Parse a complete Starlark module."""
        statements = []
        docstring = None
        
        self.skip_newlines()
        
        # Check for module docstring
        if self.match(TokenType.STRING):
            docstring = self.current_token.value
            self.advance()
            self.skip_newlines()
        
        while not self.match(TokenType.EOF):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()
        
        return StarlarkModule(body=statements, docstring=docstring)
    
    def parse_statement(self) -> Optional[StarlarkStatement]:
        """Parse a statement."""
        self.skip_newlines()
        
        if self.match(TokenType.EOF):
            return None
        
        # Function definition
        if self.match(TokenType.DEF):
            return self.parse_function_def()
        
        # Load statement
        if self.match(TokenType.LOAD):
            return self.parse_load()
        
        # Control flow
        if self.match(TokenType.IF):
            return self.parse_if()
        
        if self.match(TokenType.FOR):
            return self.parse_for()
        
        if self.match(TokenType.RETURN):
            return self.parse_return()
        
        if self.match(TokenType.BREAK):
            self.advance()
            return StarlarkBreak()
        
        if self.match(TokenType.CONTINUE):
            self.advance()
            return StarlarkContinue()
        
        if self.match(TokenType.PASS):
            self.advance()
            return StarlarkPass()
        
        # Assignment or expression statement
        return self.parse_assignment_or_expression()
    
    def parse_function_def(self) -> StarlarkFunctionDef:
        """Parse a function definition."""
        self.expect(TokenType.DEF)
        name = self.expect(TokenType.IDENTIFIER).value
        
        self.expect(TokenType.LEFT_PAREN)
        
        args = []
        defaults = []
        
        while not self.match(TokenType.RIGHT_PAREN):
            arg_name = self.expect(TokenType.IDENTIFIER).value
            args.append(arg_name)
            
            if self.match(TokenType.ASSIGN):
                self.advance()
                default_value = self.parse_expression()
                defaults.append(default_value)
            elif defaults:
                raise self.error("Non-default argument follows default argument")
            
            if not self.match(TokenType.RIGHT_PAREN):
                self.expect(TokenType.COMMA)
        
        self.expect(TokenType.RIGHT_PAREN)
        self.expect(TokenType.COLON)
        
        body = self.parse_block()
        
        return StarlarkFunctionDef(name=name, args=args, defaults=defaults, body=body)
    
    def parse_load(self) -> StarlarkLoad:
        """Parse a load statement."""
        self.expect(TokenType.LOAD)
        
        module = self.parse_expression()
        if not isinstance(module, StarlarkLiteral) or module.literal_type != "string":
            raise self.error("Load module must be a string literal")
        
        self.expect(TokenType.COMMA)
        
        symbols = []
        aliases = {}
        
        while not self.match(TokenType.NEWLINE, TokenType.EOF):
            if self.match(TokenType.STRING):
                symbol = self.current_token.value
                self.advance()
                
                if self.match(TokenType.ASSIGN):
                    self.advance()
                    alias = self.expect(TokenType.IDENTIFIER).value
                    aliases[symbol] = alias
                    symbols.append(symbol)
                else:
                    symbols.append(symbol)
            else:
                symbol = self.expect(TokenType.IDENTIFIER).value
                symbols.append(symbol)
            
            if not self.match(TokenType.NEWLINE, TokenType.EOF):
                self.expect(TokenType.COMMA)
        
        return StarlarkLoad(module=module.value, symbols=symbols, aliases=aliases)
    
    def parse_if(self) -> StarlarkIf:
        """Parse an if statement."""
        self.expect(TokenType.IF)
        test = self.parse_expression()
        self.expect(TokenType.COLON)
        
        body = self.parse_block()
        orelse = []
        
        if self.match(TokenType.ELSE):
            self.advance()
            self.expect(TokenType.COLON)
            orelse = self.parse_block()
        elif self.match(TokenType.ELIF):
            orelse = [self.parse_if()]
        
        return StarlarkIf(test=test, body=body, orelse=orelse)
    
    def parse_for(self) -> StarlarkFor:
        """Parse a for loop."""
        self.expect(TokenType.FOR)
        target = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.IN)
        iter_expr = self.parse_expression()
        self.expect(TokenType.COLON)
        
        body = self.parse_block()
        
        return StarlarkFor(target=target, iter=iter_expr, body=body)
    
    def parse_return(self) -> StarlarkReturn:
        """Parse a return statement."""
        self.expect(TokenType.RETURN)
        
        value = None
        if not self.match(TokenType.NEWLINE, TokenType.EOF):
            value = self.parse_expression()
        
        return StarlarkReturn(value=value)
    
    def parse_assignment_or_expression(self) -> StarlarkStatement:
        """Parse assignment or expression statement."""
        expr = self.parse_expression()
        
        # Check for assignment
        if self.match(TokenType.ASSIGN):
            self.advance()
            value = self.parse_expression()
            return StarlarkAssign(targets=[expr], value=value)
        
        # Check for augmented assignment
        aug_ops = {
            TokenType.PLUS_ASSIGN: StarlarkOperator.ADD,
            TokenType.MINUS_ASSIGN: StarlarkOperator.SUB,
            TokenType.MULTIPLY_ASSIGN: StarlarkOperator.MUL,
            TokenType.DIVIDE_ASSIGN: StarlarkOperator.DIV,
            TokenType.FLOOR_DIVIDE_ASSIGN: StarlarkOperator.FLOOR_DIV,
            TokenType.MODULO_ASSIGN: StarlarkOperator.MOD,
        }
        
        if self.current_token and self.current_token.type in aug_ops:
            op = aug_ops[self.current_token.type]
            self.advance()
            value = self.parse_expression()
            return StarlarkAugAssign(target=expr, operator=op, value=value)
        
        # Expression statement (not allowed in Starlark, but we'll handle it)
        return expr
    
    def parse_block(self) -> List[StarlarkStatement]:
        """Parse a block of statements."""
        self.skip_newlines()
        self.expect(TokenType.INDENT)
        
        statements = []
        
        while not self.match(TokenType.DEDENT, TokenType.EOF):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()
        
        if self.match(TokenType.DEDENT):
            self.advance()
        
        return statements
    
    def parse_expression(self) -> StarlarkExpression:
        """Parse an expression."""
        return self.parse_conditional_expr()
    
    def parse_conditional_expr(self) -> StarlarkExpression:
        """Parse conditional expression (ternary operator)."""
        expr = self.parse_or_expr()
        
        if self.match(TokenType.IF):
            self.advance()
            test = self.parse_or_expr()
            self.expect(TokenType.ELSE)
            orelse = self.parse_conditional_expr()
            return StarlarkConditionalExpr(test=test, body=expr, orelse=orelse)
        
        return expr
    
    def parse_or_expr(self) -> StarlarkExpression:
        """Parse logical OR expression."""
        left = self.parse_and_expr()
        
        while self.match(TokenType.OR):
            self.advance()
            right = self.parse_and_expr()
            left = StarlarkBoolOp(operator=StarlarkOperator.OR, values=[left, right])
        
        return left
    
    def parse_and_expr(self) -> StarlarkExpression:
        """Parse logical AND expression."""
        left = self.parse_not_expr()
        
        while self.match(TokenType.AND):
            self.advance()
            right = self.parse_not_expr()
            left = StarlarkBoolOp(operator=StarlarkOperator.AND, values=[left, right])
        
        return left
    
    def parse_not_expr(self) -> StarlarkExpression:
        """Parse logical NOT expression."""
        if self.match(TokenType.NOT):
            self.advance()
            operand = self.parse_not_expr()
            return StarlarkUnaryOp(operator=StarlarkOperator.NOT, operand=operand)
        
        return self.parse_comparison()
    
    def parse_comparison(self) -> StarlarkExpression:
        """Parse comparison expression."""
        left = self.parse_bitwise_or()
        
        ops = []
        comparators = []
        
        comparison_ops = {
            TokenType.EQUAL: StarlarkOperator.EQ,
            TokenType.NOT_EQUAL: StarlarkOperator.NE,
            TokenType.LESS_THAN: StarlarkOperator.LT,
            TokenType.LESS_EQUAL: StarlarkOperator.LE,
            TokenType.GREATER_THAN: StarlarkOperator.GT,
            TokenType.GREATER_EQUAL: StarlarkOperator.GE,
            TokenType.IN: StarlarkOperator.IN,
        }
        
        while self.current_token and self.current_token.type in comparison_ops:
            op = comparison_ops[self.current_token.type]
            self.advance()
            
            # Handle "not in"
            if op == StarlarkOperator.IN and self.match(TokenType.NOT):
                self.advance()
                op = StarlarkOperator.NOT_IN
            
            ops.append(op)
            comparators.append(self.parse_bitwise_or())
        
        if ops:
            return StarlarkComparison(left=left, operators=ops, comparators=comparators)
        
        return left
    
    def parse_bitwise_or(self) -> StarlarkExpression:
        """Parse bitwise OR expression."""
        left = self.parse_bitwise_xor()
        
        while self.match(TokenType.BIT_OR):
            op = StarlarkOperator.BIT_OR
            self.advance()
            right = self.parse_bitwise_xor()
            left = StarlarkBinaryOp(left=left, operator=op, right=right)
        
        return left
    
    def parse_bitwise_xor(self) -> StarlarkExpression:
        """Parse bitwise XOR expression."""
        left = self.parse_bitwise_and()
        
        while self.match(TokenType.BIT_XOR):
            op = StarlarkOperator.BIT_XOR
            self.advance()
            right = self.parse_bitwise_and()
            left = StarlarkBinaryOp(left=left, operator=op, right=right)
        
        return left
    
    def parse_bitwise_and(self) -> StarlarkExpression:
        """Parse bitwise AND expression."""
        left = self.parse_shift()
        
        while self.match(TokenType.BIT_AND):
            op = StarlarkOperator.BIT_AND
            self.advance()
            right = self.parse_shift()
            left = StarlarkBinaryOp(left=left, operator=op, right=right)
        
        return left
    
    def parse_shift(self) -> StarlarkExpression:
        """Parse shift expression."""
        left = self.parse_arithmetic()
        
        shift_ops = {
            TokenType.LEFT_SHIFT: StarlarkOperator.LEFT_SHIFT,
            TokenType.RIGHT_SHIFT: StarlarkOperator.RIGHT_SHIFT,
        }
        
        while self.current_token and self.current_token.type in shift_ops:
            op = shift_ops[self.current_token.type]
            self.advance()
            right = self.parse_arithmetic()
            left = StarlarkBinaryOp(left=left, operator=op, right=right)
        
        return left
    
    def parse_arithmetic(self) -> StarlarkExpression:
        """Parse arithmetic expression (+ -)."""
        left = self.parse_term()
        
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = StarlarkOperator.ADD if self.match(TokenType.PLUS) else StarlarkOperator.SUB
            self.advance()
            right = self.parse_term()
            left = StarlarkBinaryOp(left=left, operator=op, right=right)
        
        return left
    
    def parse_term(self) -> StarlarkExpression:
        """Parse term expression (* / // %)."""
        left = self.parse_factor()
        
        term_ops = {
            TokenType.MULTIPLY: StarlarkOperator.MUL,
            TokenType.DIVIDE: StarlarkOperator.DIV,
            TokenType.FLOOR_DIVIDE: StarlarkOperator.FLOOR_DIV,
            TokenType.MODULO: StarlarkOperator.MOD,
        }
        
        while self.current_token and self.current_token.type in term_ops:
            op = term_ops[self.current_token.type]
            self.advance()
            right = self.parse_factor()
            left = StarlarkBinaryOp(left=left, operator=op, right=right)
        
        return left
    
    def parse_factor(self) -> StarlarkExpression:
        """Parse factor expression (unary operators)."""
        unary_ops = {
            TokenType.PLUS: StarlarkOperator.UADD,
            TokenType.MINUS: StarlarkOperator.USUB,
            TokenType.BIT_NOT: StarlarkOperator.INVERT,
        }
        
        if self.current_token and self.current_token.type in unary_ops:
            op = unary_ops[self.current_token.type]
            self.advance()
            operand = self.parse_factor()
            return StarlarkUnaryOp(operator=op, operand=operand)
        
        return self.parse_power()
    
    def parse_power(self) -> StarlarkExpression:
        """Parse power expression (**)."""
        left = self.parse_primary()
        
        if self.match(TokenType.POWER):
            self.advance()
            right = self.parse_factor()  # Right associative
            return StarlarkBinaryOp(left=left, operator=StarlarkOperator.POW, right=right)
        
        return left
    
    def parse_primary(self) -> StarlarkExpression:
        """Parse primary expression."""
        expr = self.parse_atom()
        
        while True:
            if self.match(TokenType.DOT):
                self.advance()
                attr = self.expect(TokenType.IDENTIFIER).value
                expr = StarlarkAttribute(value=expr, attr=attr)
            
            elif self.match(TokenType.LEFT_BRACKET):
                self.advance()
                
                # Check for slice
                start = None
                end = None
                step = None
                
                if not self.match(TokenType.COLON):
                    start = self.parse_expression()
                
                if self.match(TokenType.COLON):
                    self.advance()
                    if not self.match(TokenType.RIGHT_BRACKET, TokenType.COLON):
                        end = self.parse_expression()
                    
                    if self.match(TokenType.COLON):
                        self.advance()
                        if not self.match(TokenType.RIGHT_BRACKET):
                            step = self.parse_expression()
                
                self.expect(TokenType.RIGHT_BRACKET)
                
                if end is not None or step is not None:
                    expr = StarlarkSlice(value=expr, start=start, end=end, step=step)
                else:
                    expr = StarlarkIndex(value=expr, index=start)
            
            elif self.match(TokenType.LEFT_PAREN):
                args, keywords = self.parse_call_args()
                expr = StarlarkCall(func=expr, args=args, keywords=keywords)
            
            else:
                break
        
        return expr
    
    def parse_atom(self) -> StarlarkExpression:
        """Parse atomic expression."""
        # Literals
        if self.match(TokenType.INTEGER):
            value = int(self.current_token.value)
            self.advance()
            return StarlarkLiteral(value=value, literal_type="int")
        
        if self.match(TokenType.FLOAT):
            value = float(self.current_token.value)
            self.advance()
            return StarlarkLiteral(value=value, literal_type="float")
        
        if self.match(TokenType.STRING):
            value = self.current_token.value
            self.advance()
            return StarlarkLiteral(value=value, literal_type="string")
        
        if self.match(TokenType.TRUE):
            self.advance()
            return StarlarkLiteral(value=True, literal_type="bool")
        
        if self.match(TokenType.FALSE):
            self.advance()
            return StarlarkLiteral(value=False, literal_type="bool")
        
        if self.match(TokenType.NONE):
            self.advance()
            return StarlarkLiteral(value=None, literal_type="none")
        
        # Identifier
        if self.match(TokenType.IDENTIFIER):
            name = self.current_token.value
            self.advance()
            return StarlarkIdentifier(name=name)
        
        # Parenthesized expression
        if self.match(TokenType.LEFT_PAREN):
            self.advance()
            
            # Empty tuple
            if self.match(TokenType.RIGHT_PAREN):
                self.advance()
                return StarlarkTuple(elements=[])
            
            expr = self.parse_expression()
            
            # Check for tuple
            if self.match(TokenType.COMMA):
                elements = [expr]
                while self.match(TokenType.COMMA):
                    self.advance()
                    if self.match(TokenType.RIGHT_PAREN):
                        break
                    elements.append(self.parse_expression())
                
                self.expect(TokenType.RIGHT_PAREN)
                return StarlarkTuple(elements=elements)
            
            self.expect(TokenType.RIGHT_PAREN)
            return expr
        
        # List
        if self.match(TokenType.LEFT_BRACKET):
            return self.parse_list()
        
        # Dictionary
        if self.match(TokenType.LEFT_BRACE):
            return self.parse_dict()
        
        # Lambda
        if self.match(TokenType.LAMBDA):
            return self.parse_lambda()
        
        raise self.error(f"Unexpected token: {self.current_token.type.value if self.current_token else 'EOF'}")
    
    def parse_call_args(self) -> Tuple[List[StarlarkExpression], List[StarlarkKeyword]]:
        """Parse function call arguments."""
        self.expect(TokenType.LEFT_PAREN)
        
        args = []
        keywords = []
        
        while not self.match(TokenType.RIGHT_PAREN):
            # Check for keyword argument
            if (self.match(TokenType.IDENTIFIER) and 
                self.peek(1) and self.peek(1).type == TokenType.ASSIGN):
                
                keyword = self.current_token.value
                self.advance()
                self.expect(TokenType.ASSIGN)
                value = self.parse_expression()
                keywords.append(StarlarkKeyword(arg=keyword, value=value))
            else:
                if keywords:
                    raise self.error("Positional argument follows keyword argument")
                args.append(self.parse_expression())
            
            if not self.match(TokenType.RIGHT_PAREN):
                self.expect(TokenType.COMMA)
        
        self.expect(TokenType.RIGHT_PAREN)
        return args, keywords
    
    def parse_list(self) -> StarlarkExpression:
        """Parse list literal or list comprehension."""
        self.expect(TokenType.LEFT_BRACKET)
        
        if self.match(TokenType.RIGHT_BRACKET):
            self.advance()
            return StarlarkList(elements=[])
        
        first_element = self.parse_expression()
        
        # Check for list comprehension
        if self.match(TokenType.FOR):
            self.advance()
            target = self.expect(TokenType.IDENTIFIER).value
            self.expect(TokenType.IN)
            iter_expr = self.parse_expression()
            
            ifs = []
            while self.match(TokenType.IF):
                self.advance()
                ifs.append(self.parse_expression())
            
            self.expect(TokenType.RIGHT_BRACKET)
            return StarlarkListComp(element=first_element, target=target, iter=iter_expr, ifs=ifs)
        
        # Regular list
        elements = [first_element]
        while self.match(TokenType.COMMA):
            self.advance()
            if self.match(TokenType.RIGHT_BRACKET):
                break
            elements.append(self.parse_expression())
        
        self.expect(TokenType.RIGHT_BRACKET)
        return StarlarkList(elements=elements)
    
    def parse_dict(self) -> StarlarkExpression:
        """Parse dictionary literal or dictionary comprehension."""
        self.expect(TokenType.LEFT_BRACE)
        
        if self.match(TokenType.RIGHT_BRACE):
            self.advance()
            return StarlarkDict(keys=[], values=[])
        
        first_key = self.parse_expression()
        self.expect(TokenType.COLON)
        first_value = self.parse_expression()
        
        # Check for dictionary comprehension
        if self.match(TokenType.FOR):
            self.advance()
            target = self.expect(TokenType.IDENTIFIER).value
            self.expect(TokenType.IN)
            iter_expr = self.parse_expression()
            
            ifs = []
            while self.match(TokenType.IF):
                self.advance()
                ifs.append(self.parse_expression())
            
            self.expect(TokenType.RIGHT_BRACE)
            return StarlarkDictComp(key=first_key, value=first_value, target=target, iter=iter_expr, ifs=ifs)
        
        # Regular dictionary
        keys = [first_key]
        values = [first_value]
        
        while self.match(TokenType.COMMA):
            self.advance()
            if self.match(TokenType.RIGHT_BRACE):
                break
            
            key = self.parse_expression()
            self.expect(TokenType.COLON)
            value = self.parse_expression()
            
            keys.append(key)
            values.append(value)
        
        self.expect(TokenType.RIGHT_BRACE)
        return StarlarkDict(keys=keys, values=values)
    
    def parse_lambda(self) -> StarlarkLambda:
        """Parse lambda expression."""
        self.expect(TokenType.LAMBDA)
        
        args = []
        if not self.match(TokenType.COLON):
            args.append(self.expect(TokenType.IDENTIFIER).value)
            while self.match(TokenType.COMMA):
                self.advance()
                args.append(self.expect(TokenType.IDENTIFIER).value)
        
        self.expect(TokenType.COLON)
        body = self.parse_expression()
        
        return StarlarkLambda(args=args, body=body)


def parse_starlark(source: str) -> StarlarkModule:
    """Parse Starlark source code into an AST."""
    lexer = StarlarkLexer(source)
    tokens = lexer.tokenize()
    
    # Filter out comments for parsing
    tokens = [token for token in tokens if token.type != TokenType.COMMENT]
    
    parser = StarlarkParser(tokens)
    return parser.parse_module()


def lex_starlark(source: str) -> List[Token]:
    """Tokenize Starlark source code."""
    lexer = StarlarkLexer(source)
    return lexer.tokenize()


__all__ = [
    "TokenType", "Token", "StarlarkLexer", "StarlarkParser",
    "parse_starlark", "lex_starlark"
] 