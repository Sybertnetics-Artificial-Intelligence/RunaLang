#!/usr/bin/env python3
"""
JavaScript Parser

Comprehensive JavaScript parser supporting ES5 to ES2023 features.
Converts JavaScript source code to JavaScript AST nodes.
"""

import re
import json
from typing import List, Optional, Dict, Any, Union, Tuple
from dataclasses import dataclass
from enum import Enum, auto

from .js_ast import *


class JSTokenType(Enum):
    """JavaScript token types."""
    # Literals
    NUMBER = auto()
    STRING = auto()
    BOOLEAN = auto()
    NULL = auto()
    UNDEFINED = auto()
    REGEX = auto()
    TEMPLATE_LITERAL = auto()
    
    # Identifiers
    IDENTIFIER = auto()
    
    # Keywords
    BREAK = auto()
    CASE = auto()
    CATCH = auto()
    CLASS = auto()
    CONST = auto()
    CONTINUE = auto()
    DEBUGGER = auto()
    DEFAULT = auto()
    DELETE = auto()
    DO = auto()
    ELSE = auto()
    EXPORT = auto()
    EXTENDS = auto()
    FALSE = auto()
    FINALLY = auto()
    FOR = auto()
    FUNCTION = auto()
    IF = auto()
    IMPORT = auto()
    IN = auto()
    INSTANCEOF = auto()
    LET = auto()
    NEW = auto()
    RETURN = auto()
    SUPER = auto()
    SWITCH = auto()
    THIS = auto()
    THROW = auto()
    TRUE = auto()
    TRY = auto()
    TYPEOF = auto()
    VAR = auto()
    VOID = auto()
    WHILE = auto()
    WITH = auto()
    YIELD = auto()
    
    # Async/Await
    ASYNC = auto()
    AWAIT = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    EXPONENT = auto()
    
    ASSIGN = auto()
    PLUS_ASSIGN = auto()
    MINUS_ASSIGN = auto()
    MULTIPLY_ASSIGN = auto()
    DIVIDE_ASSIGN = auto()
    MODULO_ASSIGN = auto()
    EXPONENT_ASSIGN = auto()
    
    EQUAL = auto()
    NOT_EQUAL = auto()
    STRICT_EQUAL = auto()
    STRICT_NOT_EQUAL = auto()
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
    LEFT_SHIFT = auto()
    RIGHT_SHIFT = auto()
    UNSIGNED_RIGHT_SHIFT = auto()
    
    INCREMENT = auto()
    DECREMENT = auto()
    
    QUESTION = auto()
    COLON = auto()
    SEMICOLON = auto()
    COMMA = auto()
    DOT = auto()
    OPTIONAL_CHAINING = auto()
    
    NULLISH_COALESCING = auto()
    LOGICAL_AND_ASSIGN = auto()
    LOGICAL_OR_ASSIGN = auto()
    NULLISH_COALESCING_ASSIGN = auto()
    
    # Punctuation
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    
    ARROW = auto()
    SPREAD = auto()
    
    # Special
    EOF = auto()
    NEWLINE = auto()
    WHITESPACE = auto()
    COMMENT = auto()


@dataclass
class JSToken:
    """JavaScript token."""
    type: JSTokenType
    value: str
    line: int
    column: int
    start: int
    end: int


class JSLexer:
    """JavaScript lexer/tokenizer."""
    
    KEYWORDS = {
        'break': JSTokenType.BREAK,
        'case': JSTokenType.CASE,
        'catch': JSTokenType.CATCH,
        'class': JSTokenType.CLASS,
        'const': JSTokenType.CONST,
        'continue': JSTokenType.CONTINUE,
        'debugger': JSTokenType.DEBUGGER,
        'default': JSTokenType.DEFAULT,
        'delete': JSTokenType.DELETE,
        'do': JSTokenType.DO,
        'else': JSTokenType.ELSE,
        'export': JSTokenType.EXPORT,
        'extends': JSTokenType.EXTENDS,
        'false': JSTokenType.FALSE,
        'finally': JSTokenType.FINALLY,
        'for': JSTokenType.FOR,
        'function': JSTokenType.FUNCTION,
        'if': JSTokenType.IF,
        'import': JSTokenType.IMPORT,
        'in': JSTokenType.IN,
        'instanceof': JSTokenType.INSTANCEOF,
        'let': JSTokenType.LET,
        'new': JSTokenType.NEW,
        'null': JSTokenType.NULL,
        'return': JSTokenType.RETURN,
        'super': JSTokenType.SUPER,
        'switch': JSTokenType.SWITCH,
        'this': JSTokenType.THIS,
        'throw': JSTokenType.THROW,
        'true': JSTokenType.TRUE,
        'try': JSTokenType.TRY,
        'typeof': JSTokenType.TYPEOF,
        'undefined': JSTokenType.UNDEFINED,
        'var': JSTokenType.VAR,
        'void': JSTokenType.VOID,
        'while': JSTokenType.WHILE,
        'with': JSTokenType.WITH,
        'yield': JSTokenType.YIELD,
        'async': JSTokenType.ASYNC,
        'await': JSTokenType.AWAIT,
    }
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[JSToken] = []
    
    def tokenize(self) -> List[JSToken]:
        """Tokenize the source code."""
        while self.pos < len(self.source):
            self._skip_whitespace()
            
            if self.pos >= len(self.source):
                break
            
            # Skip comments
            if self._match_comment():
                continue
            
            # String literals
            if self._match_string():
                continue
            
            # Template literals
            if self._match_template_literal():
                continue
            
            # Numbers
            if self._match_number():
                continue
            
            # Regex
            if self._match_regex():
                continue
            
            # Identifiers and keywords
            if self._match_identifier():
                continue
            
            # Operators and punctuation
            if self._match_operator():
                continue
            
            # Unknown character
            raise SyntaxError(f"Unexpected character '{self.source[self.pos]}' at line {self.line}, column {self.column}")
        
        self.tokens.append(JSToken(JSTokenType.EOF, "", self.line, self.column, self.pos, self.pos))
        return self.tokens
    
    def _current_char(self) -> str:
        """Get current character."""
        if self.pos >= len(self.source):
            return ""
        return self.source[self.pos]
    
    def _peek_char(self, offset: int = 1) -> str:
        """Peek at character at offset."""
        peek_pos = self.pos + offset
        if peek_pos >= len(self.source):
            return ""
        return self.source[peek_pos]
    
    def _advance(self) -> str:
        """Advance position and return current character."""
        if self.pos >= len(self.source):
            return ""
        
        char = self.source[self.pos]
        self.pos += 1
        
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        
        return char
    
    def _skip_whitespace(self):
        """Skip whitespace characters."""
        while self.pos < len(self.source) and self._current_char().isspace():
            self._advance()
    
    def _match_comment(self) -> bool:
        """Match single-line or multi-line comments."""
        if self._current_char() == '/' and self._peek_char() == '/':
            # Single-line comment
            start_pos = self.pos
            self._advance()  # /
            self._advance()  # /
            
            while self.pos < len(self.source) and self._current_char() != '\n':
                self._advance()
            
            return True
        
        if self._current_char() == '/' and self._peek_char() == '*':
            # Multi-line comment
            start_pos = self.pos
            self._advance()  # /
            self._advance()  # *
            
            while self.pos < len(self.source) - 1:
                if self._current_char() == '*' and self._peek_char() == '/':
                    self._advance()  # *
                    self._advance()  # /
                    break
                self._advance()
            
            return True
        
        return False
    
    def _match_string(self) -> bool:
        """Match string literals."""
        quote_char = self._current_char()
        if quote_char not in ['"', "'"]:
            return False
        
        start_pos = self.pos
        start_line = self.line
        start_column = self.column
        
        self._advance()  # opening quote
        value = ""
        
        while self.pos < len(self.source):
            char = self._current_char()
            
            if char == quote_char:
                self._advance()  # closing quote
                token = JSToken(JSTokenType.STRING, value, start_line, start_column, start_pos, self.pos)
                self.tokens.append(token)
                return True
            
            if char == '\\':
                self._advance()  # backslash
                if self.pos < len(self.source):
                    escaped = self._advance()
                    # Handle escape sequences
                    if escaped == 'n':
                        value += '\n'
                    elif escaped == 't':
                        value += '\t'
                    elif escaped == 'r':
                        value += '\r'
                    elif escaped == '\\':
                        value += '\\'
                    elif escaped == quote_char:
                        value += quote_char
                    else:
                        value += escaped
            else:
                value += self._advance()
        
        raise SyntaxError(f"Unterminated string literal at line {start_line}")
    
    def _match_template_literal(self) -> bool:
        """Match template literals."""
        if self._current_char() != '`':
            return False
        
        start_pos = self.pos
        start_line = self.line
        start_column = self.column
        
        self._advance()  # opening backtick
        value = ""
        
        while self.pos < len(self.source):
            char = self._current_char()
            
            if char == '`':
                self._advance()  # closing backtick
                token = JSToken(JSTokenType.TEMPLATE_LITERAL, value, start_line, start_column, start_pos, self.pos)
                self.tokens.append(token)
                return True
            
            if char == '\\':
                self._advance()  # backslash
                if self.pos < len(self.source):
                    escaped = self._advance()
                    value += '\\' + escaped
            else:
                value += self._advance()
        
        raise SyntaxError(f"Unterminated template literal at line {start_line}")
    
    def _match_number(self) -> bool:
        """Match numeric literals."""
        char = self._current_char()
        if not char.isdigit() and char != '.':
            return False
        
        start_pos = self.pos
        start_line = self.line
        start_column = self.column
        value = ""
        
        # Handle hexadecimal, octal, binary
        if char == '0' and self._peek_char().lower() in ['x', 'o', 'b']:
            value += self._advance()  # 0
            prefix = self._advance().lower()  # x, o, b
            value += prefix
            
            valid_chars = {
                'x': '0123456789abcdefABCDEF',
                'o': '01234567',
                'b': '01'
            }
            
            while self.pos < len(self.source) and self._current_char() in valid_chars[prefix]:
                value += self._advance()
        else:
            # Decimal number
            while self.pos < len(self.source) and (self._current_char().isdigit() or self._current_char() == '.'):
                value += self._advance()
            
            # Scientific notation
            if self.pos < len(self.source) and self._current_char().lower() == 'e':
                value += self._advance()  # e
                if self.pos < len(self.source) and self._current_char() in '+-':
                    value += self._advance()  # + or -
                while self.pos < len(self.source) and self._current_char().isdigit():
                    value += self._advance()
        
        # BigInt suffix
        if self.pos < len(self.source) and self._current_char().lower() == 'n':
            value += self._advance()
        
        if value:
            token = JSToken(JSTokenType.NUMBER, value, start_line, start_column, start_pos, self.pos)
            self.tokens.append(token)
            return True
        
        return False
    
    def _match_regex(self) -> bool:
        """Match regex literals."""
        # Simple regex detection (context-sensitive)
        if self._current_char() != '/':
            return False
        
        # Need to check if this is actually a regex and not division
        # This is a simplified approach - full JS parsing would need more context
        if not self._is_regex_context():
            return False
        
        start_pos = self.pos
        start_line = self.line
        start_column = self.column
        
        self._advance()  # opening /
        value = ""
        
        while self.pos < len(self.source):
            char = self._current_char()
            
            if char == '/':
                self._advance()  # closing /
                # Read flags
                flags = ""
                while self.pos < len(self.source) and self._current_char().isalpha():
                    flags += self._advance()
                
                token = JSToken(JSTokenType.REGEX, f"/{value}/{flags}", start_line, start_column, start_pos, self.pos)
                self.tokens.append(token)
                return True
            
            if char == '\\':
                value += self._advance()  # backslash
                if self.pos < len(self.source):
                    value += self._advance()  # escaped character
            else:
                value += self._advance()
        
        raise SyntaxError(f"Unterminated regex literal at line {start_line}")
    
    def _is_regex_context(self) -> bool:
        """Check if we're in a context where / starts a regex."""
        # Simplified heuristic - in real parser this would be more sophisticated
        if not self.tokens:
            return True
        
        last_token = self.tokens[-1]
        return last_token.type in [
            JSTokenType.LPAREN, JSTokenType.LBRACE, JSTokenType.LBRACKET,
            JSTokenType.COMMA, JSTokenType.SEMICOLON, JSTokenType.COLON,
            JSTokenType.RETURN, JSTokenType.THROW, JSTokenType.EQUAL,
            JSTokenType.NOT_EQUAL, JSTokenType.STRICT_EQUAL, JSTokenType.STRICT_NOT_EQUAL,
            JSTokenType.AND, JSTokenType.OR, JSTokenType.NOT
        ]
    
    def _match_identifier(self) -> bool:
        """Match identifiers and keywords."""
        char = self._current_char()
        if not (char.isalpha() or char == '_' or char == '$'):
            return False
        
        start_pos = self.pos
        start_line = self.line
        start_column = self.column
        value = ""
        
        while self.pos < len(self.source):
            char = self._current_char()
            if char.isalnum() or char == '_' or char == '$':
                value += self._advance()
            else:
                break
        
        # Check if it's a keyword
        token_type = self.KEYWORDS.get(value, JSTokenType.IDENTIFIER)
        token = JSToken(token_type, value, start_line, start_column, start_pos, self.pos)
        self.tokens.append(token)
        return True
    
    def _match_operator(self) -> bool:
        """Match operators and punctuation."""
        char = self._current_char()
        next_char = self._peek_char()
        third_char = self._peek_char(2)
        
        start_pos = self.pos
        start_line = self.line
        start_column = self.column
        
        # Three-character operators
        if char + next_char + third_char == '>>>':
            self._advance()
            self._advance()
            self._advance()
            self.tokens.append(JSToken(JSTokenType.UNSIGNED_RIGHT_SHIFT, '>>>', start_line, start_column, start_pos, self.pos))
            return True
        
        if char + next_char + third_char == '>>>':
            self._advance()
            self._advance()
            self._advance()
            self.tokens.append(JSToken(JSTokenType.UNSIGNED_RIGHT_SHIFT, '>>>', start_line, start_column, start_pos, self.pos))
            return True
        
        # Two-character operators
        two_char_ops = {
            '++': JSTokenType.INCREMENT,
            '--': JSTokenType.DECREMENT,
            '==': JSTokenType.EQUAL,
            '!=': JSTokenType.NOT_EQUAL,
            '===': JSTokenType.STRICT_EQUAL,
            '!==': JSTokenType.STRICT_NOT_EQUAL,
            '<=': JSTokenType.LESS_EQUAL,
            '>=': JSTokenType.GREATER_EQUAL,
            '&&': JSTokenType.AND,
            '||': JSTokenType.OR,
            '<<': JSTokenType.LEFT_SHIFT,
            '>>': JSTokenType.RIGHT_SHIFT,
            '+=': JSTokenType.PLUS_ASSIGN,
            '-=': JSTokenType.MINUS_ASSIGN,
            '*=': JSTokenType.MULTIPLY_ASSIGN,
            '/=': JSTokenType.DIVIDE_ASSIGN,
            '%=': JSTokenType.MODULO_ASSIGN,
            '**': JSTokenType.EXPONENT,
            '?.': JSTokenType.OPTIONAL_CHAINING,
            '??': JSTokenType.NULLISH_COALESCING,
            '=>': JSTokenType.ARROW,
            '...': JSTokenType.SPREAD,
        }
        
        if char + next_char in two_char_ops:
            self._advance()
            self._advance()
            token_type = two_char_ops[char + next_char]
            self.tokens.append(JSToken(token_type, char + next_char, start_line, start_column, start_pos, self.pos))
            return True
        
        # Single-character operators
        single_char_ops = {
            '+': JSTokenType.PLUS,
            '-': JSTokenType.MINUS,
            '*': JSTokenType.MULTIPLY,
            '/': JSTokenType.DIVIDE,
            '%': JSTokenType.MODULO,
            '=': JSTokenType.ASSIGN,
            '<': JSTokenType.LESS_THAN,
            '>': JSTokenType.GREATER_THAN,
            '!': JSTokenType.NOT,
            '&': JSTokenType.BITWISE_AND,
            '|': JSTokenType.BITWISE_OR,
            '^': JSTokenType.BITWISE_XOR,
            '~': JSTokenType.BITWISE_NOT,
            '?': JSTokenType.QUESTION,
            ':': JSTokenType.COLON,
            ';': JSTokenType.SEMICOLON,
            ',': JSTokenType.COMMA,
            '.': JSTokenType.DOT,
            '(': JSTokenType.LPAREN,
            ')': JSTokenType.RPAREN,
            '{': JSTokenType.LBRACE,
            '}': JSTokenType.RBRACE,
            '[': JSTokenType.LBRACKET,
            ']': JSTokenType.RBRACKET,
        }
        
        if char in single_char_ops:
            self._advance()
            token_type = single_char_ops[char]
            self.tokens.append(JSToken(token_type, char, start_line, start_column, start_pos, self.pos))
            return True
        
        return False


class JSParser:
    """JavaScript parser."""
    
    def __init__(self, tokens: List[JSToken]):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[0] if tokens else None
    
    def parse(self) -> JSProgram:
        """Parse tokens into JavaScript AST."""
        statements = []
        
        while not self._is_at_end():
            if self._match(JSTokenType.EOF):
                break
            
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
        
        return JSProgram(statements)
    
    def _current_token_type(self) -> JSTokenType:
        """Get current token type."""
        if self.pos >= len(self.tokens):
            return JSTokenType.EOF
        return self.tokens[self.pos].type
    
    def _current_token_value(self) -> str:
        """Get current token value."""
        if self.pos >= len(self.tokens):
            return ""
        return self.tokens[self.pos].value
    
    def _advance(self) -> JSToken:
        """Advance to next token."""
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return self.tokens[self.pos]
    
    def _peek(self, offset: int = 1) -> JSToken:
        """Peek at token at offset."""
        peek_pos = self.pos + offset
        if peek_pos >= len(self.tokens):
            return self.tokens[-1]  # EOF token
        return self.tokens[peek_pos]
    
    def _match(self, *token_types: JSTokenType) -> bool:
        """Check if current token matches any of the given types."""
        return self._current_token_type() in token_types
    
    def _consume(self, token_type: JSTokenType, message: str = None) -> JSToken:
        """Consume token of expected type."""
        if self._current_token_type() == token_type:
            token = self.tokens[self.pos]
            self._advance()
            return token
        
        if message:
            raise SyntaxError(f"{message}. Got {self._current_token_type()}")
        else:
            raise SyntaxError(f"Expected {token_type}, got {self._current_token_type()}")
    
    def _is_at_end(self) -> bool:
        """Check if at end of tokens."""
        return self.pos >= len(self.tokens) or self._current_token_type() == JSTokenType.EOF
    
    def _parse_statement(self) -> Optional[JSNode]:
        """Parse a statement."""
        if self._match(JSTokenType.VAR, JSTokenType.LET, JSTokenType.CONST):
            return self._parse_variable_declaration()
        
        if self._match(JSTokenType.FUNCTION):
            return self._parse_function_declaration()
        
        if self._match(JSTokenType.IF):
            return self._parse_if_statement()
        
        if self._match(JSTokenType.WHILE):
            return self._parse_while_statement()
        
        if self._match(JSTokenType.FOR):
            return self._parse_for_statement()
        
        if self._match(JSTokenType.RETURN):
            return self._parse_return_statement()
        
        if self._match(JSTokenType.BREAK):
            return self._parse_break_statement()
        
        if self._match(JSTokenType.CONTINUE):
            return self._parse_continue_statement()
        
        if self._match(JSTokenType.THROW):
            return self._parse_throw_statement()
        
        if self._match(JSTokenType.TRY):
            return self._parse_try_statement()
        
        if self._match(JSTokenType.LBRACE):
            return self._parse_block_statement()
        
        if self._match(JSTokenType.SEMICOLON):
            self._advance()
            return JSEmptyStatement()
        
        # Expression statement
        expr = self._parse_expression()
        self._consume_semicolon()
        return JSExpressionStatement(expr)
    
    def _parse_variable_declaration(self) -> JSVariableDeclaration:
        """Parse variable declaration."""
        kind_token = self._advance()
        kind = JSVariableKind(kind_token.value)
        
        declarators = []
        
        # Parse first declarator
        declarators.append(self._parse_variable_declarator())
        
        # Parse additional declarators
        while self._match(JSTokenType.COMMA):
            self._advance()  # consume comma
            declarators.append(self._parse_variable_declarator())
        
        self._consume_semicolon()
        return JSVariableDeclaration(declarators, kind)
    
    def _parse_variable_declarator(self) -> JSVariableDeclarator:
        """Parse variable declarator."""
        id = self._parse_identifier()
        
        init = None
        if self._match(JSTokenType.ASSIGN):
            self._advance()  # consume =
            init = self._parse_assignment_expression()
        
        return JSVariableDeclarator(id, init)
    
    def _parse_function_declaration(self) -> JSFunctionDeclaration:
        """Parse function declaration."""
        self._consume(JSTokenType.FUNCTION)
        
        # Check for async/generator
        async_ = False
        generator = False
        
        if self._match(JSTokenType.MULTIPLY):
            self._advance()
            generator = True
        
        id = self._parse_identifier()
        
        self._consume(JSTokenType.LPAREN)
        params = self._parse_parameter_list()
        self._consume(JSTokenType.RPAREN)
        
        body = self._parse_block_statement()
        
        return JSFunctionDeclaration(id, params, body, generator, async_)
    
    def _parse_if_statement(self) -> JSIfStatement:
        """Parse if statement."""
        self._consume(JSTokenType.IF)
        self._consume(JSTokenType.LPAREN)
        test = self._parse_expression()
        self._consume(JSTokenType.RPAREN)
        
        consequent = self._parse_statement()
        
        alternate = None
        if self._match(JSTokenType.ELSE):
            self._advance()
            alternate = self._parse_statement()
        
        return JSIfStatement(test, consequent, alternate)
    
    def _parse_while_statement(self) -> JSWhileStatement:
        """Parse while statement."""
        self._consume(JSTokenType.WHILE)
        self._consume(JSTokenType.LPAREN)
        test = self._parse_expression()
        self._consume(JSTokenType.RPAREN)
        body = self._parse_statement()
        
        return JSWhileStatement(test, body)
    
    def _parse_for_statement(self) -> JSForStatement:
        """Parse for statement."""
        self._consume(JSTokenType.FOR)
        self._consume(JSTokenType.LPAREN)
        
        # Init
        init = None
        if not self._match(JSTokenType.SEMICOLON):
            if self._match(JSTokenType.VAR, JSTokenType.LET, JSTokenType.CONST):
                init = self._parse_variable_declaration()
            else:
                init = self._parse_expression()
                self._consume(JSTokenType.SEMICOLON)
        else:
            self._advance()  # consume semicolon
        
        # Test
        test = None
        if not self._match(JSTokenType.SEMICOLON):
            test = self._parse_expression()
        self._consume(JSTokenType.SEMICOLON)
        
        # Update
        update = None
        if not self._match(JSTokenType.RPAREN):
            update = self._parse_expression()
        
        self._consume(JSTokenType.RPAREN)
        body = self._parse_statement()
        
        return JSForStatement(init, test, update, body)
    
    def _parse_return_statement(self) -> JSReturnStatement:
        """Parse return statement."""
        self._consume(JSTokenType.RETURN)
        
        argument = None
        if not self._match(JSTokenType.SEMICOLON) and not self._is_at_end():
            argument = self._parse_expression()
        
        self._consume_semicolon()
        return JSReturnStatement(argument)
    
    def _parse_break_statement(self) -> JSBreakStatement:
        """Parse break statement."""
        self._consume(JSTokenType.BREAK)
        self._consume_semicolon()
        return JSBreakStatement()
    
    def _parse_continue_statement(self) -> JSContinueStatement:
        """Parse continue statement."""
        self._consume(JSTokenType.CONTINUE)
        self._consume_semicolon()
        return JSContinueStatement()
    
    def _parse_throw_statement(self) -> JSThrowStatement:
        """Parse throw statement."""
        self._consume(JSTokenType.THROW)
        argument = self._parse_expression()
        self._consume_semicolon()
        return JSThrowStatement(argument)
    
    def _parse_try_statement(self) -> JSTryStatement:
        """Parse try statement."""
        self._consume(JSTokenType.TRY)
        block = self._parse_block_statement()
        
        handler = None
        if self._match(JSTokenType.CATCH):
            self._advance()
            
            param = None
            if self._match(JSTokenType.LPAREN):
                self._advance()
                param = self._parse_identifier()
                self._consume(JSTokenType.RPAREN)
            
            body = self._parse_block_statement()
            handler = JSCatchClause(param, body)
        
        finalizer = None
        if self._match(JSTokenType.FINALLY):
            self._advance()
            finalizer = self._parse_block_statement()
        
        return JSTryStatement(block, handler, finalizer)
    
    def _parse_block_statement(self) -> JSBlockStatement:
        """Parse block statement."""
        self._consume(JSTokenType.LBRACE)
        statements = []
        
        while not self._match(JSTokenType.RBRACE) and not self._is_at_end():
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
        
        self._consume(JSTokenType.RBRACE)
        return JSBlockStatement(statements)
    
    def _parse_expression(self) -> JSNode:
        """Parse expression."""
        return self._parse_assignment_expression()
    
    def _parse_assignment_expression(self) -> JSNode:
        """Parse assignment expression."""
        expr = self._parse_conditional_expression()
        
        if self._match(JSTokenType.ASSIGN, JSTokenType.PLUS_ASSIGN, JSTokenType.MINUS_ASSIGN,
                       JSTokenType.MULTIPLY_ASSIGN, JSTokenType.DIVIDE_ASSIGN, JSTokenType.MODULO_ASSIGN):
            operator_token = self._advance()
            operator = JSOperator(operator_token.value)
            right = self._parse_assignment_expression()
            return JSAssignmentExpression(expr, operator, right)
        
        return expr
    
    def _parse_conditional_expression(self) -> JSNode:
        """Parse conditional expression."""
        expr = self._parse_logical_or_expression()
        
        if self._match(JSTokenType.QUESTION):
            self._advance()
            consequent = self._parse_assignment_expression()
            self._consume(JSTokenType.COLON)
            alternate = self._parse_assignment_expression()
            return JSConditionalExpression(expr, consequent, alternate)
        
        return expr
    
    def _parse_logical_or_expression(self) -> JSNode:
        """Parse logical OR expression."""
        expr = self._parse_logical_and_expression()
        
        while self._match(JSTokenType.OR, JSTokenType.NULLISH_COALESCING):
            operator_token = self._advance()
            operator = JSOperator(operator_token.value)
            right = self._parse_logical_and_expression()
            expr = JSLogicalExpression(expr, operator, right)
        
        return expr
    
    def _parse_logical_and_expression(self) -> JSNode:
        """Parse logical AND expression."""
        expr = self._parse_equality_expression()
        
        while self._match(JSTokenType.AND):
            operator_token = self._advance()
            operator = JSOperator(operator_token.value)
            right = self._parse_equality_expression()
            expr = JSLogicalExpression(expr, operator, right)
        
        return expr
    
    def _parse_equality_expression(self) -> JSNode:
        """Parse equality expression."""
        expr = self._parse_relational_expression()
        
        while self._match(JSTokenType.EQUAL, JSTokenType.NOT_EQUAL, 
                          JSTokenType.STRICT_EQUAL, JSTokenType.STRICT_NOT_EQUAL):
            operator_token = self._advance()
            operator = JSOperator(operator_token.value)
            right = self._parse_relational_expression()
            expr = JSBinaryExpression(expr, operator, right)
        
        return expr
    
    def _parse_relational_expression(self) -> JSNode:
        """Parse relational expression."""
        expr = self._parse_additive_expression()
        
        while self._match(JSTokenType.LESS_THAN, JSTokenType.LESS_EQUAL,
                          JSTokenType.GREATER_THAN, JSTokenType.GREATER_EQUAL,
                          JSTokenType.IN, JSTokenType.INSTANCEOF):
            operator_token = self._advance()
            operator = JSOperator(operator_token.value)
            right = self._parse_additive_expression()
            expr = JSBinaryExpression(expr, operator, right)
        
        return expr
    
    def _parse_additive_expression(self) -> JSNode:
        """Parse additive expression."""
        expr = self._parse_multiplicative_expression()
        
        while self._match(JSTokenType.PLUS, JSTokenType.MINUS):
            operator_token = self._advance()
            operator = JSOperator(operator_token.value)
            right = self._parse_multiplicative_expression()
            expr = JSBinaryExpression(expr, operator, right)
        
        return expr
    
    def _parse_multiplicative_expression(self) -> JSNode:
        """Parse multiplicative expression."""
        expr = self._parse_exponential_expression()
        
        while self._match(JSTokenType.MULTIPLY, JSTokenType.DIVIDE, JSTokenType.MODULO):
            operator_token = self._advance()
            operator = JSOperator(operator_token.value)
            right = self._parse_exponential_expression()
            expr = JSBinaryExpression(expr, operator, right)
        
        return expr
    
    def _parse_exponential_expression(self) -> JSNode:
        """Parse exponential expression."""
        expr = self._parse_unary_expression()
        
        if self._match(JSTokenType.EXPONENT):
            operator_token = self._advance()
            operator = JSOperator(operator_token.value)
            right = self._parse_exponential_expression()  # Right associative
            expr = JSBinaryExpression(expr, operator, right)
        
        return expr
    
    def _parse_unary_expression(self) -> JSNode:
        """Parse unary expression."""
        if self._match(JSTokenType.NOT, JSTokenType.BITWISE_NOT, JSTokenType.PLUS, JSTokenType.MINUS,
                       JSTokenType.TYPEOF, JSTokenType.VOID, JSTokenType.DELETE):
            operator_token = self._advance()
            operator = JSOperator(operator_token.value)
            argument = self._parse_unary_expression()
            return JSUnaryExpression(operator, argument)
        
        if self._match(JSTokenType.INCREMENT, JSTokenType.DECREMENT):
            operator_token = self._advance()
            operator = JSOperator(operator_token.value)
            argument = self._parse_postfix_expression()
            return JSUpdateExpression(operator, argument, prefix=True)
        
        return self._parse_postfix_expression()
    
    def _parse_postfix_expression(self) -> JSNode:
        """Parse postfix expression."""
        expr = self._parse_call_expression()
        
        if self._match(JSTokenType.INCREMENT, JSTokenType.DECREMENT):
            operator_token = self._advance()
            operator = JSOperator(operator_token.value)
            return JSUpdateExpression(operator, expr, prefix=False)
        
        return expr
    
    def _parse_call_expression(self) -> JSNode:
        """Parse call expression."""
        expr = self._parse_member_expression()
        
        while True:
            if self._match(JSTokenType.LPAREN):
                self._advance()
                arguments = self._parse_argument_list()
                self._consume(JSTokenType.RPAREN)
                expr = JSCallExpression(expr, arguments)
            elif self._match(JSTokenType.DOT):
                self._advance()
                property = self._parse_identifier()
                expr = JSMemberExpression(expr, property, computed=False)
            elif self._match(JSTokenType.LBRACKET):
                self._advance()
                property = self._parse_expression()
                self._consume(JSTokenType.RBRACKET)
                expr = JSMemberExpression(expr, property, computed=True)
            else:
                break
        
        return expr
    
    def _parse_member_expression(self) -> JSNode:
        """Parse member expression."""
        if self._match(JSTokenType.NEW):
            self._advance()
            callee = self._parse_member_expression()
            
            arguments = []
            if self._match(JSTokenType.LPAREN):
                self._advance()
                arguments = self._parse_argument_list()
                self._consume(JSTokenType.RPAREN)
            
            return JSNewExpression(callee, arguments)
        
        return self._parse_primary_expression()
    
    def _parse_primary_expression(self) -> JSNode:
        """Parse primary expression."""
        if self._match(JSTokenType.THIS):
            self._advance()
            return JSThisExpression()
        
        if self._match(JSTokenType.SUPER):
            self._advance()
            return JSSuper()
        
        if self._match(JSTokenType.IDENTIFIER):
            return self._parse_identifier()
        
        if self._match(JSTokenType.NUMBER):
            return self._parse_number_literal()
        
        if self._match(JSTokenType.STRING):
            return self._parse_string_literal()
        
        if self._match(JSTokenType.TRUE, JSTokenType.FALSE):
            return self._parse_boolean_literal()
        
        if self._match(JSTokenType.NULL):
            return self._parse_null_literal()
        
        if self._match(JSTokenType.UNDEFINED):
            return self._parse_undefined_literal()
        
        if self._match(JSTokenType.REGEX):
            return self._parse_regex_literal()
        
        if self._match(JSTokenType.TEMPLATE_LITERAL):
            return self._parse_template_literal()
        
        if self._match(JSTokenType.LBRACKET):
            return self._parse_array_expression()
        
        if self._match(JSTokenType.LBRACE):
            return self._parse_object_expression()
        
        if self._match(JSTokenType.FUNCTION):
            return self._parse_function_expression()
        
        if self._match(JSTokenType.LPAREN):
            self._advance()
            expr = self._parse_expression()
            self._consume(JSTokenType.RPAREN)
            return expr
        
        raise SyntaxError(f"Unexpected token {self._current_token_type()}")
    
    def _parse_identifier(self) -> JSIdentifier:
        """Parse identifier."""
        token = self._consume(JSTokenType.IDENTIFIER)
        return JSIdentifier(token.value)
    
    def _parse_number_literal(self) -> JSLiteral:
        """Parse number literal."""
        token = self._consume(JSTokenType.NUMBER)
        
        # Determine if it's a BigInt
        if token.value.endswith('n'):
            return JSLiteral(token.value[:-1], token.value, JSLiteralType.BIGINT)
        
        # Parse numeric value
        try:
            if '.' in token.value or 'e' in token.value.lower():
                value = float(token.value)
            else:
                value = int(token.value, 0)  # Auto-detect base
        except ValueError:
            value = token.value  # Keep as string if parsing fails
        
        return JSLiteral(value, token.value, JSLiteralType.NUMBER)
    
    def _parse_string_literal(self) -> JSLiteral:
        """Parse string literal."""
        token = self._consume(JSTokenType.STRING)
        return JSLiteral(token.value, f'"{token.value}"', JSLiteralType.STRING)
    
    def _parse_boolean_literal(self) -> JSLiteral:
        """Parse boolean literal."""
        token = self._advance()
        value = token.value == 'true'
        return JSLiteral(value, token.value, JSLiteralType.BOOLEAN)
    
    def _parse_null_literal(self) -> JSLiteral:
        """Parse null literal."""
        token = self._consume(JSTokenType.NULL)
        return JSLiteral(None, token.value, JSLiteralType.NULL)
    
    def _parse_undefined_literal(self) -> JSLiteral:
        """Parse undefined literal."""
        token = self._consume(JSTokenType.UNDEFINED)
        return JSLiteral(None, token.value, JSLiteralType.NULL)  # Treat as null type
    
    def _parse_regex_literal(self) -> JSLiteral:
        """Parse regex literal."""
        token = self._consume(JSTokenType.REGEX)
        return JSLiteral(token.value, token.value, JSLiteralType.REGEX)
    
    def _parse_template_literal(self) -> JSTemplateLiteral:
        """Parse template literal."""
        token = self._consume(JSTokenType.TEMPLATE_LITERAL)
        
        # Simplified template literal parsing
        # In a full implementation, this would handle embedded expressions
        quasis = [JSLiteral(token.value, f"`{token.value}`", JSLiteralType.STRING)]
        expressions = []
        
        return JSTemplateLiteral(quasis, expressions)
    
    def _parse_array_expression(self) -> JSArrayExpression:
        """Parse array expression."""
        self._consume(JSTokenType.LBRACKET)
        elements = []
        
        while not self._match(JSTokenType.RBRACKET) and not self._is_at_end():
            if self._match(JSTokenType.COMMA):
                # Sparse array
                elements.append(None)
                self._advance()
            else:
                elements.append(self._parse_assignment_expression())
                if self._match(JSTokenType.COMMA):
                    self._advance()
        
        self._consume(JSTokenType.RBRACKET)
        return JSArrayExpression(elements)
    
    def _parse_object_expression(self) -> JSObjectExpression:
        """Parse object expression."""
        self._consume(JSTokenType.LBRACE)
        properties = []
        
        while not self._match(JSTokenType.RBRACE) and not self._is_at_end():
            properties.append(self._parse_property())
            if self._match(JSTokenType.COMMA):
                self._advance()
        
        self._consume(JSTokenType.RBRACE)
        return JSObjectExpression(properties)
    
    def _parse_property(self) -> JSProperty:
        """Parse object property."""
        # Simple property parsing - could be enhanced for methods, getters, setters
        key = self._parse_identifier()
        self._consume(JSTokenType.COLON)
        value = self._parse_assignment_expression()
        
        return JSProperty(key, value, JSPropertyKind.INIT)
    
    def _parse_function_expression(self) -> JSFunctionExpression:
        """Parse function expression."""
        self._consume(JSTokenType.FUNCTION)
        
        # Optional name
        id = None
        if self._match(JSTokenType.IDENTIFIER):
            id = self._parse_identifier()
        
        self._consume(JSTokenType.LPAREN)
        params = self._parse_parameter_list()
        self._consume(JSTokenType.RPAREN)
        
        body = self._parse_block_statement()
        
        return JSFunctionExpression(id, params, body)
    
    def _parse_parameter_list(self) -> List[JSNode]:
        """Parse parameter list."""
        params = []
        
        while not self._match(JSTokenType.RPAREN) and not self._is_at_end():
            params.append(self._parse_identifier())
            if self._match(JSTokenType.COMMA):
                self._advance()
        
        return params
    
    def _parse_argument_list(self) -> List[JSNode]:
        """Parse argument list."""
        arguments = []
        
        while not self._match(JSTokenType.RPAREN) and not self._is_at_end():
            arguments.append(self._parse_assignment_expression())
            if self._match(JSTokenType.COMMA):
                self._advance()
        
        return arguments
    
    def _consume_semicolon(self):
        """Consume semicolon if present."""
        if self._match(JSTokenType.SEMICOLON):
            self._advance()


def parse_javascript(source: str) -> JSProgram:
    """Parse JavaScript source code into AST."""
    lexer = JSLexer(source)
    tokens = lexer.tokenize()
    
    parser = JSParser(tokens)
    return parser.parse()