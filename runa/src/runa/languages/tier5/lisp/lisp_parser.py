#!/usr/bin/env python3
"""
LISP Parser

Comprehensive parser for LISP covering S-expressions, special forms,
and classical LISP language constructs.
"""

import re
from typing import List, Optional, Union, Iterator, Any
from dataclasses import dataclass
from enum import Enum, auto

from .lisp_ast import (
    LispNode, LispExpression, LispForm, LispAtom, LispSymbol, LispList, 
    LispCons, LispQuote, LispDefun, LispLambda, LispLet, LispSetq, LispIf,
    LispCond, LispProgn, LispWhen, LispUnless, LispCar, LispCdr, LispConsFunc,
    LispEq, LispEqual, LispAtomFunc, LispListp, LispLoop, LispReturn,
    LispDefmacro, LispMacroCall, LispApplication, LispProgram,
    LispSpecialForm, lisp_nil, lisp_t, lisp_number, lisp_string, lisp_symbol,
    lisp_list, lisp_application
)


class LispTokenType(Enum):
    """LISP token types."""
    # Literals
    SYMBOL = auto()
    NUMBER = auto()
    STRING = auto()
    NIL = auto()
    T = auto()
    
    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    QUOTE = auto()
    
    # Special symbols
    DOT = auto()  # For dotted pairs
    
    # Control
    EOF = auto()
    NEWLINE = auto()
    COMMENT = auto()


@dataclass
class LispToken:
    """LISP token."""
    type: LispTokenType
    value: str
    line: int = 1
    column: int = 1


class LispLexer:
    """LISP lexer for tokenizing S-expressions."""
    
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[LispToken] = []
        
        # Token patterns
        self.patterns = [
            (r';[^\n]*', LispTokenType.COMMENT),
            (r'\(', LispTokenType.LPAREN),
            (r'\)', LispTokenType.RPAREN),
            (r"'", LispTokenType.QUOTE),
            (r'\.', LispTokenType.DOT),
            (r'"[^"]*"', LispTokenType.STRING),
            (r'-?\d+\.?\d*', LispTokenType.NUMBER),
            (r'nil\b', LispTokenType.NIL),
            (r't\b', LispTokenType.T),
            (r'[a-zA-Z_+\-*/><=?!&][a-zA-Z0-9_+\-*/><=?!&]*', LispTokenType.SYMBOL),
            (r'\s+', None),  # Whitespace (ignored)
        ]
        
        self.compiled_patterns = [(re.compile(pattern), token_type) 
                                 for pattern, token_type in self.patterns]
    
    def tokenize(self) -> List[LispToken]:
        """Tokenize the input text."""
        while self.pos < len(self.text):
            if self._match_patterns():
                continue
            else:
                # Unknown character
                char = self.text[self.pos]
                raise SyntaxError(f"Unexpected character '{char}' at line {self.line}, column {self.column}")
        
        # Add EOF token
        self.tokens.append(LispToken(LispTokenType.EOF, "", self.line, self.column))
        return self.tokens
    
    def _match_patterns(self) -> bool:
        """Try to match any pattern at current position."""
        for pattern, token_type in self.compiled_patterns:
            match = pattern.match(self.text, self.pos)
            if match:
                value = match.group(0)
                
                if token_type is not None:  # Not whitespace
                    token = LispToken(token_type, value, self.line, self.column)
                    self.tokens.append(token)
                
                # Update position
                self._advance(len(value))
                return True
        return False
    
    def _advance(self, count: int):
        """Advance position and update line/column."""
        for _ in range(count):
            if self.pos < len(self.text) and self.text[self.pos] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.pos += 1


class LispParser:
    """LISP parser for building AST from tokens."""
    
    def __init__(self, tokens: List[LispToken]):
        self.tokens = tokens
        self.pos = 0
        self.current_token = tokens[0] if tokens else None
        
        # Special form handlers
        self.special_forms = {
            'defun': self._parse_defun,
            'lambda': self._parse_lambda,
            'let': self._parse_let,
            'setq': self._parse_setq,
            'if': self._parse_if,
            'cond': self._parse_cond,
            'progn': self._parse_progn,
            'when': self._parse_when,
            'unless': self._parse_unless,
            'quote': self._parse_quote_form,
            'defmacro': self._parse_defmacro,
            'loop': self._parse_loop,
            'return': self._parse_return,
        }
        
        # Built-in function handlers
        self.builtin_functions = {
            'car': self._parse_car,
            'cdr': self._parse_cdr,
            'cons': self._parse_cons_func,
            'eq': self._parse_eq,
            'equal': self._parse_equal,
            'atom': self._parse_atom_func,
            'listp': self._parse_listp,
        }
    
    def parse(self) -> LispProgram:
        """Parse tokens into a LISP program."""
        forms = []
        
        while not self._is_at_end():
            if self.current_token.type == LispTokenType.COMMENT:
                self._advance()
                continue
            
            form = self._parse_form()
            if form:
                forms.append(form)
        
        return LispProgram(forms)
    
    def _parse_form(self) -> Optional[LispExpression]:
        """Parse a top-level form."""
        if self._is_at_end():
            return None
        
        return self._parse_expression()
    
    def _parse_expression(self) -> Optional[LispExpression]:
        """Parse any LISP expression."""
        if self._is_at_end():
            return None
        
        token = self.current_token
        
        if token.type == LispTokenType.LPAREN:
            return self._parse_list()
        elif token.type == LispTokenType.QUOTE:
            return self._parse_quote()
        else:
            return self._parse_atom()
    
    def _parse_atom(self) -> LispExpression:
        """Parse an atomic expression."""
        token = self.current_token
        self._advance()
        
        if token.type == LispTokenType.NIL:
            return lisp_nil()
        elif token.type == LispTokenType.T:
            return lisp_t()
        elif token.type == LispTokenType.NUMBER:
            try:
                if '.' in token.value:
                    value = float(token.value)
                else:
                    value = int(token.value)
                return lisp_number(value)
            except ValueError:
                raise SyntaxError(f"Invalid number: {token.value}")
        elif token.type == LispTokenType.STRING:
            # Remove quotes
            value = token.value[1:-1]
            return lisp_string(value)
        elif token.type == LispTokenType.SYMBOL:
            return lisp_symbol(token.value)
        else:
            raise SyntaxError(f"Unexpected token: {token.value}")
    
    def _parse_list(self) -> LispExpression:
        """Parse a list expression."""
        self._consume(LispTokenType.LPAREN)
        
        if self._check(LispTokenType.RPAREN):
            self._advance()
            return lisp_list()  # Empty list
        
        # Check for special forms or built-ins
        if self.current_token.type == LispTokenType.SYMBOL:
            symbol_name = self.current_token.value
            
            if symbol_name in self.special_forms:
                return self.special_forms[symbol_name]()
            elif symbol_name in self.builtin_functions:
                return self.builtin_functions[symbol_name]()
        
        # Regular function application or list
        elements = []
        
        while not self._check(LispTokenType.RPAREN) and not self._is_at_end():
            # Check for dotted pair
            if self._check(LispTokenType.DOT):
                if len(elements) != 1:
                    raise SyntaxError("Dotted pair must have exactly one element before dot")
                self._advance()  # consume dot
                cdr = self._parse_expression()
                self._consume(LispTokenType.RPAREN)
                return LispCons(elements[0], cdr)
            
            expr = self._parse_expression()
            if expr:
                elements.append(expr)
        
        self._consume(LispTokenType.RPAREN)
        
        # If first element is a function, create application
        if elements and isinstance(elements[0], (LispSymbol, LispLambda)):
            return lisp_application(elements[0], *elements[1:])
        
        return lisp_list(*elements)
    
    def _parse_quote(self) -> LispQuote:
        """Parse a quote expression."""
        self._consume(LispTokenType.QUOTE)
        expr = self._parse_expression()
        return LispQuote(expr)
    
    # Special form parsers
    def _parse_defun(self) -> LispDefun:
        """Parse defun special form."""
        self._consume_symbol('defun')
        
        name = self._parse_symbol()
        params = self._parse_parameter_list()
        
        # Optional doc string
        doc_string = None
        if (self.current_token.type == LispTokenType.STRING and 
            not self._check(LispTokenType.RPAREN)):
            doc_string = self.current_token.value[1:-1]  # Remove quotes
            self._advance()
        
        body = []
        while not self._check(LispTokenType.RPAREN) and not self._is_at_end():
            expr = self._parse_expression()
            if expr:
                body.append(expr)
        
        self._consume(LispTokenType.RPAREN)
        return LispDefun(name, params, body, doc_string)
    
    def _parse_lambda(self) -> LispLambda:
        """Parse lambda special form."""
        self._consume_symbol('lambda')
        
        params = self._parse_parameter_list()
        
        body = []
        while not self._check(LispTokenType.RPAREN) and not self._is_at_end():
            expr = self._parse_expression()
            if expr:
                body.append(expr)
        
        self._consume(LispTokenType.RPAREN)
        return LispLambda(params, body)
    
    def _parse_let(self) -> LispLet:
        """Parse let special form."""
        self._consume_symbol('let')
        
        # Parse bindings
        self._consume(LispTokenType.LPAREN)
        bindings = []
        
        while not self._check(LispTokenType.RPAREN) and not self._is_at_end():
            self._consume(LispTokenType.LPAREN)
            symbol = self._parse_symbol()
            value = self._parse_expression()
            self._consume(LispTokenType.RPAREN)
            bindings.append((symbol, value))
        
        self._consume(LispTokenType.RPAREN)
        
        # Parse body
        body = []
        while not self._check(LispTokenType.RPAREN) and not self._is_at_end():
            expr = self._parse_expression()
            if expr:
                body.append(expr)
        
        self._consume(LispTokenType.RPAREN)
        return LispLet(bindings, body)
    
    def _parse_setq(self) -> LispSetq:
        """Parse setq special form."""
        self._consume_symbol('setq')
        
        symbol = self._parse_symbol()
        value = self._parse_expression()
        
        self._consume(LispTokenType.RPAREN)
        return LispSetq(symbol, value)
    
    def _parse_if(self) -> LispIf:
        """Parse if special form."""
        self._consume_symbol('if')
        
        test = self._parse_expression()
        then_expr = self._parse_expression()
        
        else_expr = None
        if not self._check(LispTokenType.RPAREN):
            else_expr = self._parse_expression()
        
        self._consume(LispTokenType.RPAREN)
        return LispIf(test, then_expr, else_expr)
    
    def _parse_cond(self) -> LispCond:
        """Parse cond special form."""
        self._consume_symbol('cond')
        
        clauses = []
        while not self._check(LispTokenType.RPAREN) and not self._is_at_end():
            self._consume(LispTokenType.LPAREN)
            test = self._parse_expression()
            expr = self._parse_expression()
            self._consume(LispTokenType.RPAREN)
            clauses.append((test, expr))
        
        self._consume(LispTokenType.RPAREN)
        return LispCond(clauses)
    
    def _parse_progn(self) -> LispProgn:
        """Parse progn special form."""
        self._consume_symbol('progn')
        
        expressions = []
        while not self._check(LispTokenType.RPAREN) and not self._is_at_end():
            expr = self._parse_expression()
            if expr:
                expressions.append(expr)
        
        self._consume(LispTokenType.RPAREN)
        return LispProgn(expressions)
    
    def _parse_when(self) -> LispWhen:
        """Parse when special form."""
        self._consume_symbol('when')
        
        test = self._parse_expression()
        
        body = []
        while not self._check(LispTokenType.RPAREN) and not self._is_at_end():
            expr = self._parse_expression()
            if expr:
                body.append(expr)
        
        self._consume(LispTokenType.RPAREN)
        return LispWhen(test, body)
    
    def _parse_unless(self) -> LispUnless:
        """Parse unless special form."""
        self._consume_symbol('unless')
        
        test = self._parse_expression()
        
        body = []
        while not self._check(LispTokenType.RPAREN) and not self._is_at_end():
            expr = self._parse_expression()
            if expr:
                body.append(expr)
        
        self._consume(LispTokenType.RPAREN)
        return LispUnless(test, body)
    
    def _parse_quote_form(self) -> LispQuote:
        """Parse quote special form."""
        self._consume_symbol('quote')
        
        expr = self._parse_expression()
        
        self._consume(LispTokenType.RPAREN)
        return LispQuote(expr)
    
    def _parse_defmacro(self) -> LispDefmacro:
        """Parse defmacro special form."""
        self._consume_symbol('defmacro')
        
        name = self._parse_symbol()
        params = self._parse_parameter_list()
        
        body = []
        while not self._check(LispTokenType.RPAREN) and not self._is_at_end():
            expr = self._parse_expression()
            if expr:
                body.append(expr)
        
        self._consume(LispTokenType.RPAREN)
        return LispDefmacro(name, params, body)
    
    def _parse_loop(self) -> LispLoop:
        """Parse loop special form."""
        self._consume_symbol('loop')
        
        body = []
        while not self._check(LispTokenType.RPAREN) and not self._is_at_end():
            expr = self._parse_expression()
            if expr:
                body.append(expr)
        
        self._consume(LispTokenType.RPAREN)
        return LispLoop(body)
    
    def _parse_return(self) -> LispReturn:
        """Parse return special form."""
        self._consume_symbol('return')
        
        value = None
        if not self._check(LispTokenType.RPAREN):
            value = self._parse_expression()
        
        self._consume(LispTokenType.RPAREN)
        return LispReturn(value)
    
    # Built-in function parsers
    def _parse_car(self) -> LispCar:
        """Parse car function call."""
        self._consume_symbol('car')
        
        expr = self._parse_expression()
        
        self._consume(LispTokenType.RPAREN)
        return LispCar(expr)
    
    def _parse_cdr(self) -> LispCdr:
        """Parse cdr function call."""
        self._consume_symbol('cdr')
        
        expr = self._parse_expression()
        
        self._consume(LispTokenType.RPAREN)
        return LispCdr(expr)
    
    def _parse_cons_func(self) -> LispConsFunc:
        """Parse cons function call."""
        self._consume_symbol('cons')
        
        car = self._parse_expression()
        cdr = self._parse_expression()
        
        self._consume(LispTokenType.RPAREN)
        return LispConsFunc(car, cdr)
    
    def _parse_eq(self) -> LispEq:
        """Parse eq function call."""
        self._consume_symbol('eq')
        
        left = self._parse_expression()
        right = self._parse_expression()
        
        self._consume(LispTokenType.RPAREN)
        return LispEq(left, right)
    
    def _parse_equal(self) -> LispEqual:
        """Parse equal function call."""
        self._consume_symbol('equal')
        
        left = self._parse_expression()
        right = self._parse_expression()
        
        self._consume(LispTokenType.RPAREN)
        return LispEqual(left, right)
    
    def _parse_atom_func(self) -> LispAtomFunc:
        """Parse atom function call."""
        self._consume_symbol('atom')
        
        expr = self._parse_expression()
        
        self._consume(LispTokenType.RPAREN)
        return LispAtomFunc(expr)
    
    def _parse_listp(self) -> LispListp:
        """Parse listp function call."""
        self._consume_symbol('listp')
        
        expr = self._parse_expression()
        
        self._consume(LispTokenType.RPAREN)
        return LispListp(expr)
    
    # Helper methods
    def _parse_parameter_list(self) -> List[LispSymbol]:
        """Parse a parameter list."""
        self._consume(LispTokenType.LPAREN)
        
        params = []
        while not self._check(LispTokenType.RPAREN) and not self._is_at_end():
            param = self._parse_symbol()
            params.append(param)
        
        self._consume(LispTokenType.RPAREN)
        return params
    
    def _parse_symbol(self) -> LispSymbol:
        """Parse a symbol."""
        if self.current_token.type != LispTokenType.SYMBOL:
            raise SyntaxError(f"Expected symbol, got {self.current_token.value}")
        
        name = self.current_token.value
        self._advance()
        return lisp_symbol(name)
    
    def _advance(self):
        """Move to the next token."""
        if not self._is_at_end():
            self.pos += 1
            if self.pos < len(self.tokens):
                self.current_token = self.tokens[self.pos]
    
    def _is_at_end(self) -> bool:
        """Check if we're at the end of tokens."""
        return (self.current_token is None or 
                self.current_token.type == LispTokenType.EOF)
    
    def _check(self, token_type: LispTokenType) -> bool:
        """Check if current token is of given type."""
        if self._is_at_end():
            return False
        return self.current_token.type == token_type
    
    def _consume(self, token_type: LispTokenType):
        """Consume a token of the given type."""
        if self._check(token_type):
            self._advance()
        else:
            expected = token_type.name
            actual = self.current_token.value if self.current_token else "EOF"
            raise SyntaxError(f"Expected {expected}, got {actual}")
    
    def _consume_symbol(self, expected: str):
        """Consume a specific symbol."""
        if (self.current_token.type == LispTokenType.SYMBOL and 
            self.current_token.value == expected):
            self._advance()
        else:
            actual = self.current_token.value if self.current_token else "EOF"
            raise SyntaxError(f"Expected '{expected}', got '{actual}'")


def parse_lisp(source_code: str) -> LispProgram:
    """Parse LISP source code into AST."""
    try:
        lexer = LispLexer(source_code)
        tokens = lexer.tokenize()
        
        # Filter out comments
        tokens = [t for t in tokens if t.type != LispTokenType.COMMENT]
        
        parser = LispParser(tokens)
        return parser.parse()
    
    except Exception as e:
        raise SyntaxError(f"LISP parsing error: {e}")


def parse_lisp_expression(source_code: str) -> LispExpression:
    """Parse a single LISP expression."""
    try:
        lexer = LispLexer(source_code)
        tokens = lexer.tokenize()
        
        # Filter out comments
        tokens = [t for t in tokens if t.type != LispTokenType.COMMENT]
        
        parser = LispParser(tokens)
        return parser._parse_expression()
    
    except Exception as e:
        raise SyntaxError(f"LISP expression parsing error: {e}") 