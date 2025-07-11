#!/usr/bin/env python3
"""
Rholang Parser Implementation

This module provides a comprehensive parser for the Rholang language, converting
Rholang source code into Abstract Syntax Tree (AST) nodes.

Rholang is a process-oriented language for the RChain blockchain with:
- Process calculus based on rho-calculus
- Concurrent execution with channel communication
- Pattern matching and destructuring
- Smart contract capabilities
- Message passing and synchronization

The parser handles all Rholang constructs including processes, names, patterns,
and blockchain-specific features.
"""

import re
from typing import List, Optional, Union, Dict, Any, Iterator, Tuple
from enum import Enum
from dataclasses import dataclass

from .rholang_ast import *


class TokenType(Enum):
    """Rholang token types."""
    
    # Literals
    INTEGER = "INTEGER"
    STRING = "STRING"
    BOOL = "BOOL"
    BYTES = "BYTES"
    URI = "URI"
    
    # Identifiers and names
    IDENTIFIER = "IDENTIFIER"
    UNFORGEABLE = "UNFORGEABLE"
    WILDCARD = "WILDCARD"
    
    # Keywords
    NEW = "NEW"
    CONTRACT = "CONTRACT"
    MATCH = "MATCH"
    FOR = "FOR"
    IF = "IF"
    ELSE = "ELSE"
    NIL = "NIL"
    BUNDLE = "BUNDLE"
    TRUE = "TRUE"
    FALSE = "FALSE"
    
    # Operators
    SEND = "!"
    RECEIVE = "?"
    PARALLEL = "|"
    QUOTE = "@"
    
    # Arithmetic operators
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    MODULO = "%"
    POWER = "**"
    
    # Comparison operators
    EQUAL = "=="
    NOT_EQUAL = "!="
    LESS_THAN = "<"
    LESS_EQUAL = "<="
    GREATER_THAN = ">"
    GREATER_EQUAL = ">="
    
    # Logical operators
    AND = "and"
    OR = "or"
    NOT = "not"
    
    # Delimiters
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
    LEFT_BRACKET = "["
    RIGHT_BRACKET = "]"
    LEFT_BRACE = "{"
    RIGHT_BRACE = "}"
    
    # Punctuation
    COMMA = ","
    DOT = "."
    COLON = ":"
    SEMICOLON = ";"
    ARROW = "=>"
    BIND = "<-"
    
    # Special
    NEWLINE = "NEWLINE"
    EOF = "EOF"
    COMMENT = "COMMENT"


@dataclass
class Token:
    """Represents a token in Rholang source code."""
    
    type: TokenType
    value: str
    line: int
    column: int
    
    def __str__(self) -> str:
        return f"Token({self.type.value}, {repr(self.value)}, {self.line}:{self.column})"


class RholangLexer:
    """Lexical analyzer for Rholang source code."""
    
    KEYWORDS = {
        'new': TokenType.NEW,
        'contract': TokenType.CONTRACT,
        'match': TokenType.MATCH,
        'for': TokenType.FOR,
        'if': TokenType.IF,
        'else': TokenType.ELSE,
        'Nil': TokenType.NIL,
        'bundle': TokenType.BUNDLE,
        'true': TokenType.TRUE,
        'false': TokenType.FALSE,
        'and': TokenType.AND,
        'or': TokenType.OR,
        'not': TokenType.NOT,
    }
    
    OPERATORS = {
        '!': TokenType.SEND,
        '?': TokenType.RECEIVE,
        '|': TokenType.PARALLEL,
        '@': TokenType.QUOTE,
        '+': TokenType.PLUS,
        '-': TokenType.MINUS,
        '*': TokenType.MULTIPLY,
        '/': TokenType.DIVIDE,
        '%': TokenType.MODULO,
        '**': TokenType.POWER,
        '==': TokenType.EQUAL,
        '!=': TokenType.NOT_EQUAL,
        '<': TokenType.LESS_THAN,
        '<=': TokenType.LESS_EQUAL,
        '>': TokenType.GREATER_THAN,
        '>=': TokenType.GREATER_EQUAL,
        '=>': TokenType.ARROW,
        '<-': TokenType.BIND,
    }
    
    DELIMITERS = {
        '(': TokenType.LEFT_PAREN,
        ')': TokenType.RIGHT_PAREN,
        '[': TokenType.LEFT_BRACKET,
        ']': TokenType.RIGHT_BRACKET,
        '{': TokenType.LEFT_BRACE,
        '}': TokenType.RIGHT_BRACE,
        ',': TokenType.COMMA,
        '.': TokenType.DOT,
        ':': TokenType.COLON,
        ';': TokenType.SEMICOLON,
    }
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
    
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
        """Skip whitespace characters."""
        while self.peek() in ' \t\r':
            self.advance()
    
    def read_string(self) -> str:
        """Read a string literal."""
        quote = self.advance()  # Opening quote
        value = ""
        
        while True:
            char = self.peek()
            
            if char == '\0':
                raise self.error("Unterminated string literal")
            
            if char == quote:
                self.advance()
                break
            
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
        
        while self.peek().isdigit():
            value += self.advance()
        
        # Check for decimal point
        if self.peek() == '.':
            is_float = True
            value += self.advance()
            while self.peek().isdigit():
                value += self.advance()
        
        return float(value) if is_float else int(value)
    
    def read_identifier(self) -> str:
        """Read an identifier or keyword."""
        value = ""
        
        while self.peek().isalnum() or self.peek() in '_':
            value += self.advance()
        
        return value
    
    def read_unforgeable(self) -> str:
        """Read an unforgeable name."""
        value = ""
        self.advance()  # Skip '`'
        
        while self.peek() != '`' and self.peek() != '\0':
            value += self.advance()
        
        if self.peek() == '`':
            self.advance()  # Closing backtick
        else:
            raise self.error("Unterminated unforgeable name")
        
        return value
    
    def read_comment(self) -> str:
        """Read a comment."""
        comment = ""
        
        if self.peek() == '/' and self.peek(1) == '/':
            # Single line comment
            self.advance()  # First /
            self.advance()  # Second /
            
            while self.peek() != '\n' and self.peek() != '\0':
                comment += self.advance()
        
        elif self.peek() == '/' and self.peek(1) == '*':
            # Multi-line comment
            self.advance()  # /
            self.advance()  # *
            
            while True:
                char = self.peek()
                if char == '\0':
                    raise self.error("Unterminated comment")
                if char == '*' and self.peek(1) == '/':
                    self.advance()  # *
                    self.advance()  # /
                    break
                comment += self.advance()
        
        return comment
    
    def tokenize(self) -> List[Token]:
        """Tokenize the source code."""
        tokens = []
        
        while self.pos < len(self.source):
            char = self.peek()
            
            if char == '\0':
                break
            
            # Skip whitespace
            if char in ' \t\r':
                self.skip_whitespace()
                continue
            
            # Newlines
            if char == '\n':
                tokens.append(Token(TokenType.NEWLINE, char, self.line, self.column))
                self.advance()
                continue
            
            # Comments
            if char == '/' and self.peek(1) in '/*':
                comment = self.read_comment()
                tokens.append(Token(TokenType.COMMENT, comment, self.line, self.column))
                continue
            
            # String literals
            if char in '"\'':
                string_value = self.read_string()
                tokens.append(Token(TokenType.STRING, string_value, self.line, self.column))
                continue
            
            # Numbers
            if char.isdigit():
                number = self.read_number()
                token_type = TokenType.INTEGER if isinstance(number, int) else TokenType.INTEGER
                tokens.append(Token(token_type, str(number), self.line, self.column))
                continue
            
            # Unforgeable names
            if char == '`':
                unforgeable = self.read_unforgeable()
                tokens.append(Token(TokenType.UNFORGEABLE, unforgeable, self.line, self.column))
                continue
            
            # Wildcard
            if char == '_':
                self.advance()
                tokens.append(Token(TokenType.WILDCARD, '_', self.line, self.column))
                continue
            
            # Identifiers and keywords
            if char.isalpha() or char == '_':
                identifier = self.read_identifier()
                token_type = self.KEYWORDS.get(identifier, TokenType.IDENTIFIER)
                tokens.append(Token(token_type, identifier, self.line, self.column))
                continue
            
            # Multi-character operators
            two_char = char + self.peek(1)
            if two_char in self.OPERATORS:
                self.advance()
                self.advance()
                tokens.append(Token(self.OPERATORS[two_char], two_char, self.line, self.column))
                continue
            
            # Single-character operators and delimiters
            if char in self.OPERATORS:
                self.advance()
                tokens.append(Token(self.OPERATORS[char], char, self.line, self.column))
                continue
            
            if char in self.DELIMITERS:
                self.advance()
                tokens.append(Token(self.DELIMITERS[char], char, self.line, self.column))
                continue
            
            # Unknown character
            raise self.error(f"Unexpected character: {char}")
        
        # Add EOF token
        tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        
        return tokens


class RholangParser:
    """Parser for Rholang source code."""
    
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
    
    def parse_module(self) -> RholangModule:
        """Parse a complete Rholang module."""
        processes = []
        imports = []
        
        self.skip_newlines()
        
        while not self.match(TokenType.EOF):
            process = self.parse_process()
            if process:
                processes.append(process)
            self.skip_newlines()
        
        return RholangModule(body=processes, imports=imports)
    
    def parse_process(self) -> Optional[RholangProcess]:
        """Parse a process."""
        self.skip_newlines()
        
        if self.match(TokenType.EOF):
            return None
        
        return self.parse_parallel()
    
    def parse_parallel(self) -> RholangProcess:
        """Parse parallel composition."""
        processes = [self.parse_primary_process()]
        
        while self.match(TokenType.PARALLEL):
            self.advance()
            processes.append(self.parse_primary_process())
        
        if len(processes) == 1:
            return processes[0]
        else:
            return RholangPar(processes=processes)
    
    def parse_primary_process(self) -> RholangProcess:
        """Parse primary process constructs."""
        if self.match(TokenType.NIL):
            self.advance()
            return RholangNil()
        
        elif self.match(TokenType.NEW):
            return self.parse_new()
        
        elif self.match(TokenType.CONTRACT):
            return self.parse_contract()
        
        elif self.match(TokenType.MATCH):
            return self.parse_match()
        
        elif self.match(TokenType.IF):
            return self.parse_if()
        
        elif self.match(TokenType.FOR):
            return self.parse_for()
        
        elif self.match(TokenType.BUNDLE):
            return self.parse_bundle()
        
        elif self.match(TokenType.LEFT_PAREN):
            self.advance()
            process = self.parse_parallel()
            self.expect(TokenType.RIGHT_PAREN)
            return process
        
        else:
            # Parse send/receive or expression
            return self.parse_send_receive()
    
    def parse_new(self) -> RholangNew:
        """Parse new construct."""
        self.expect(TokenType.NEW)
        
        names = []
        names.append(self.expect(TokenType.IDENTIFIER).value)
        
        while self.match(TokenType.COMMA):
            self.advance()
            names.append(self.expect(TokenType.IDENTIFIER).value)
        
        self.expect(TokenType.COLON)
        process = self.parse_process()
        
        return RholangNew(names=names, process=process)
    
    def parse_contract(self) -> RholangContract:
        """Parse contract definition."""
        self.expect(TokenType.CONTRACT)
        
        name = self.parse_expression()
        
        self.expect(TokenType.LEFT_PAREN)
        parameters = []
        
        while not self.match(TokenType.RIGHT_PAREN):
            pattern = self.parse_pattern()
            parameters.append(pattern)
            
            if not self.match(TokenType.RIGHT_PAREN):
                self.expect(TokenType.COMMA)
        
        self.expect(TokenType.RIGHT_PAREN)
        self.expect(TokenType.ARROW)
        
        body = self.parse_process()
        
        return RholangContract(name=name, parameters=parameters, body=body)
    
    def parse_match(self) -> RholangMatch:
        """Parse match expression."""
        self.expect(TokenType.MATCH)
        
        target = self.parse_expression()
        self.expect(TokenType.LEFT_BRACE)
        
        cases = []
        while not self.match(TokenType.RIGHT_BRACE):
            pattern = self.parse_pattern()
            condition = None
            
            if self.match(TokenType.IF):
                self.advance()
                condition = self.parse_expression()
            
            self.expect(TokenType.ARROW)
            body = self.parse_process()
            
            cases.append(RholangMatchCase(pattern=pattern, condition=condition, body=body))
            
            if not self.match(TokenType.RIGHT_BRACE):
                self.expect(TokenType.SEMICOLON)
        
        self.expect(TokenType.RIGHT_BRACE)
        
        return RholangMatch(target=target, cases=cases)
    
    def parse_if(self) -> RholangIf:
        """Parse if process."""
        self.expect(TokenType.IF)
        self.expect(TokenType.LEFT_PAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RIGHT_PAREN)
        
        then_process = self.parse_process()
        else_process = None
        
        if self.match(TokenType.ELSE):
            self.advance()
            else_process = self.parse_process()
        
        return RholangIf(condition=condition, then_process=then_process, else_process=else_process)
    
    def parse_for(self) -> RholangFor:
        """Parse for comprehension."""
        self.expect(TokenType.FOR)
        self.expect(TokenType.LEFT_PAREN)
        
        variables = []
        generators = []
        
        pattern = self.parse_pattern()
        self.expect(TokenType.BIND)
        generator = self.parse_expression()
        
        variables.append(pattern)
        generators.append(generator)
        
        while self.match(TokenType.SEMICOLON):
            self.advance()
            pattern = self.parse_pattern()
            self.expect(TokenType.BIND)
            generator = self.parse_expression()
            
            variables.append(pattern)
            generators.append(generator)
        
        self.expect(TokenType.RIGHT_PAREN)
        body = self.parse_process()
        
        return RholangFor(variables=variables, generators=generators, body=body)
    
    def parse_bundle(self) -> RholangBundle:
        """Parse bundle construct."""
        self.expect(TokenType.BUNDLE)
        bundle_type = self.expect(TokenType.IDENTIFIER).value
        
        if bundle_type not in ["read", "write", "readWrite"]:
            raise self.error(f"Invalid bundle type: {bundle_type}")
        
        self.expect(TokenType.LEFT_PAREN)
        process = self.parse_process()
        self.expect(TokenType.RIGHT_PAREN)
        
        return RholangBundle(bundle_type=bundle_type, process=process)
    
    def parse_send_receive(self) -> RholangProcess:
        """Parse send/receive or expression statement."""
        expr = self.parse_expression()
        
        if self.match(TokenType.SEND):
            # Send operation
            self.advance()
            self.expect(TokenType.LEFT_PAREN)
            
            data = []
            while not self.match(TokenType.RIGHT_PAREN):
                data.append(self.parse_expression())
                if not self.match(TokenType.RIGHT_PAREN):
                    self.expect(TokenType.COMMA)
            
            self.expect(TokenType.RIGHT_PAREN)
            
            return RholangSend(channel=expr, data=data)
        
        elif self.match(TokenType.RECEIVE):
            # Receive operation  
            self.advance()
            self.expect(TokenType.LEFT_PAREN)
            
            receives = []
            patterns = []
            
            while not self.match(TokenType.RIGHT_PAREN):
                pattern = self.parse_pattern()
                patterns.append(pattern)
                if not self.match(TokenType.RIGHT_PAREN):
                    self.expect(TokenType.COMMA)
            
            self.expect(TokenType.RIGHT_PAREN)
            self.expect(TokenType.ARROW)
            
            continuation = self.parse_process()
            
            receive_pattern = RholangReceivePattern(channel=expr, patterns=patterns)
            receives.append(receive_pattern)
            
            return RholangReceive(receives=receives, continuation=continuation)
        
        else:
            # Expression as process (not standard Rholang, but useful for parsing)
            return expr
    
    def parse_expression(self) -> RholangExpression:
        """Parse an expression."""
        return self.parse_or()
    
    def parse_or(self) -> RholangExpression:
        """Parse logical OR expression."""
        left = self.parse_and()
        
        while self.match(TokenType.OR):
            op = RholangOperator.OR
            self.advance()
            right = self.parse_and()
            left = RholangBinaryOp(left=left, operator=op, right=right)
        
        return left
    
    def parse_and(self) -> RholangExpression:
        """Parse logical AND expression."""
        left = self.parse_equality()
        
        while self.match(TokenType.AND):
            op = RholangOperator.AND
            self.advance()
            right = self.parse_equality()
            left = RholangBinaryOp(left=left, operator=op, right=right)
        
        return left
    
    def parse_equality(self) -> RholangExpression:
        """Parse equality expression."""
        left = self.parse_comparison()
        
        while self.match(TokenType.EQUAL, TokenType.NOT_EQUAL):
            op = RholangOperator.EQ if self.match(TokenType.EQUAL) else RholangOperator.NE
            self.advance()
            right = self.parse_comparison()
            left = RholangBinaryOp(left=left, operator=op, right=right)
        
        return left
    
    def parse_comparison(self) -> RholangExpression:
        """Parse comparison expression."""
        left = self.parse_addition()
        
        comp_ops = {
            TokenType.LESS_THAN: RholangOperator.LT,
            TokenType.LESS_EQUAL: RholangOperator.LE,
            TokenType.GREATER_THAN: RholangOperator.GT,
            TokenType.GREATER_EQUAL: RholangOperator.GE,
        }
        
        while self.current_token and self.current_token.type in comp_ops:
            op = comp_ops[self.current_token.type]
            self.advance()
            right = self.parse_addition()
            left = RholangBinaryOp(left=left, operator=op, right=right)
        
        return left
    
    def parse_addition(self) -> RholangExpression:
        """Parse addition/subtraction expression."""
        left = self.parse_multiplication()
        
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = RholangOperator.ADD if self.match(TokenType.PLUS) else RholangOperator.SUB
            self.advance()
            right = self.parse_multiplication()
            left = RholangBinaryOp(left=left, operator=op, right=right)
        
        return left
    
    def parse_multiplication(self) -> RholangExpression:
        """Parse multiplication/division expression."""
        left = self.parse_unary()
        
        mult_ops = {
            TokenType.MULTIPLY: RholangOperator.MUL,
            TokenType.DIVIDE: RholangOperator.DIV,
            TokenType.MODULO: RholangOperator.MOD,
        }
        
        while self.current_token and self.current_token.type in mult_ops:
            op = mult_ops[self.current_token.type]
            self.advance()
            right = self.parse_unary()
            left = RholangBinaryOp(left=left, operator=op, right=right)
        
        return left
    
    def parse_unary(self) -> RholangExpression:
        """Parse unary expression."""
        if self.match(TokenType.NOT):
            self.advance()
            operand = self.parse_unary()
            return RholangUnaryOp(operator=RholangOperator.NOT, operand=operand)
        
        if self.match(TokenType.MINUS):
            self.advance()
            operand = self.parse_unary()
            return RholangUnaryOp(operator=RholangOperator.USUB, operand=operand)
        
        if self.match(TokenType.PLUS):
            self.advance()
            operand = self.parse_unary()
            return RholangUnaryOp(operator=RholangOperator.UADD, operand=operand)
        
        if self.match(TokenType.QUOTE):
            self.advance()
            process = self.parse_primary_process()
            return RholangQuote(process=process)
        
        return self.parse_primary_expression()
    
    def parse_primary_expression(self) -> RholangExpression:
        """Parse primary expression."""
        # Literals
        if self.match(TokenType.INTEGER):
            value = int(self.current_token.value)
            self.advance()
            return RholangLiteral(value=value, literal_type="int")
        
        if self.match(TokenType.STRING):
            value = self.current_token.value
            self.advance()
            return RholangLiteral(value=value, literal_type="string")
        
        if self.match(TokenType.TRUE):
            self.advance()
            return RholangLiteral(value=True, literal_type="bool")
        
        if self.match(TokenType.FALSE):
            self.advance()
            return RholangLiteral(value=False, literal_type="bool")
        
        # Names
        if self.match(TokenType.IDENTIFIER):
            name = self.current_token.value
            self.advance()
            return RholangName(name=name)
        
        if self.match(TokenType.UNFORGEABLE):
            name = self.current_token.value
            self.advance()
            return RholangUnforgeableName(name=name)
        
        if self.match(TokenType.WILDCARD):
            self.advance()
            return RholangName(name="_", is_wildcard=True)
        
        # Collections
        if self.match(TokenType.LEFT_BRACKET):
            return self.parse_list()
        
        if self.match(TokenType.LEFT_BRACE):
            return self.parse_map()
        
        # Parenthesized expression
        if self.match(TokenType.LEFT_PAREN):
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RIGHT_PAREN)
            return expr
        
        raise self.error(f"Unexpected token: {self.current_token.type.value if self.current_token else 'EOF'}")
    
    def parse_list(self) -> RholangList:
        """Parse list literal."""
        self.expect(TokenType.LEFT_BRACKET)
        
        elements = []
        while not self.match(TokenType.RIGHT_BRACKET):
            elements.append(self.parse_expression())
            if not self.match(TokenType.RIGHT_BRACKET):
                self.expect(TokenType.COMMA)
        
        self.expect(TokenType.RIGHT_BRACKET)
        return RholangList(elements=elements)
    
    def parse_map(self) -> RholangMap:
        """Parse map literal."""
        self.expect(TokenType.LEFT_BRACE)
        
        pairs = []
        while not self.match(TokenType.RIGHT_BRACE):
            key = self.parse_expression()
            self.expect(TokenType.COLON)
            value = self.parse_expression()
            
            pairs.append(RholangMapPair(key=key, value=value))
            
            if not self.match(TokenType.RIGHT_BRACE):
                self.expect(TokenType.COMMA)
        
        self.expect(TokenType.RIGHT_BRACE)
        return RholangMap(pairs=pairs)
    
    def parse_pattern(self) -> RholangPattern:
        """Parse a pattern."""
        if self.match(TokenType.WILDCARD):
            self.advance()
            return RholangWildcardPattern()
        
        elif self.match(TokenType.IDENTIFIER):
            name = self.current_token.value
            self.advance()
            return RholangVarPattern(name=name)
        
        elif self.match(TokenType.LEFT_BRACKET):
            return self.parse_list_pattern()
        
        elif self.match(TokenType.LEFT_PAREN):
            return self.parse_tuple_pattern()
        
        else:
            raise self.error("Expected pattern")
    
    def parse_list_pattern(self) -> RholangListPattern:
        """Parse list pattern."""
        self.expect(TokenType.LEFT_BRACKET)
        
        patterns = []
        remainder = None
        
        while not self.match(TokenType.RIGHT_BRACKET):
            pattern = self.parse_pattern()
            patterns.append(pattern)
            
            if not self.match(TokenType.RIGHT_BRACKET):
                self.expect(TokenType.COMMA)
        
        self.expect(TokenType.RIGHT_BRACKET)
        return RholangListPattern(patterns=patterns, remainder=remainder)
    
    def parse_tuple_pattern(self) -> RholangTuplePattern:
        """Parse tuple pattern."""
        self.expect(TokenType.LEFT_PAREN)
        
        patterns = []
        while not self.match(TokenType.RIGHT_PAREN):
            patterns.append(self.parse_pattern())
            if not self.match(TokenType.RIGHT_PAREN):
                self.expect(TokenType.COMMA)
        
        self.expect(TokenType.RIGHT_PAREN)
        return RholangTuplePattern(patterns=patterns)


def parse_rholang(source: str) -> RholangModule:
    """Parse Rholang source code into an AST."""
    lexer = RholangLexer(source)
    tokens = lexer.tokenize()
    
    # Filter out comments for parsing
    tokens = [token for token in tokens if token.type != TokenType.COMMENT]
    
    parser = RholangParser(tokens)
    return parser.parse_module()


def lex_rholang(source: str) -> List[Token]:
    """Tokenize Rholang source code."""
    lexer = RholangLexer(source)
    return lexer.tokenize()


__all__ = [
    "TokenType", "Token", "RholangLexer", "RholangParser",
    "parse_rholang", "lex_rholang"
] 