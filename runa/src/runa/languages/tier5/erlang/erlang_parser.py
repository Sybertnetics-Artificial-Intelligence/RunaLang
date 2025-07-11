#!/usr/bin/env python3
"""
Erlang Parser

Comprehensive parser for Erlang covering actor model concurrency,
pattern matching, functional programming, and distributed systems features.
"""

import re
from typing import List, Optional, Union, Iterator, Any
from dataclasses import dataclass
from enum import Enum, auto

from .erlang_ast import *


class ErlangTokenType(Enum):
    """Erlang token types."""
    # Literals
    ATOM = auto()
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    VARIABLE = auto()
    
    # Keywords
    MODULE = auto()
    EXPORT = auto()
    IMPORT = auto()
    FUN = auto()
    CASE = auto()
    IF = auto()
    WHEN = auto()
    BEGIN = auto()
    END = auto()
    RECEIVE = auto()
    AFTER = auto()
    TRY = auto()
    CATCH = auto()
    THROW = auto()
    SPAWN = auto()
    
    # Operators
    MATCH = auto()      # =
    SEND = auto()       # !
    ARROW = auto()      # ->
    PLUS = auto()       # +
    MINUS = auto()      # -
    MULTIPLY = auto()   # *
    DIVIDE = auto()     # /
    EQ = auto()         # ==
    NE = auto()         # /=
    LT = auto()         # <
    LE = auto()         # =<
    GT = auto()         # >
    GE = auto()         # >=
    AND = auto()        # and
    OR = auto()         # or
    NOT = auto()        # not
    
    # Delimiters
    LPAREN = auto()     # (
    RPAREN = auto()     # )
    LBRACKET = auto()   # [
    RBRACKET = auto()   # ]
    LBRACE = auto()     # {
    RBRACE = auto()     # }
    DOT = auto()        # .
    COMMA = auto()      # ,
    SEMICOLON = auto()  # ;
    COLON = auto()      # :
    PIPE = auto()       # |
    HASH = auto()       # #
    
    # Special
    EOF = auto()
    NEWLINE = auto()
    COMMENT = auto()


@dataclass
class ErlangToken:
    """Erlang token."""
    type: ErlangTokenType
    value: str
    line: int = 1
    column: int = 1


class ErlangLexer:
    """Erlang lexer."""
    
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[ErlangToken] = []
        
        # Keywords
        self.keywords = {
            'module', 'export', 'import', 'fun', 'case', 'if', 'when',
            'begin', 'end', 'receive', 'after', 'try', 'catch', 'throw',
            'spawn', 'and', 'or', 'not', 'true', 'false'
        }
        
        # Token patterns
        self.patterns = [
            (r'%.*', ErlangTokenType.COMMENT),
            (r'->', ErlangTokenType.ARROW),
            (r'==', ErlangTokenType.EQ),
            (r'/=', ErlangTokenType.NE),
            (r'=<', ErlangTokenType.LE),
            (r'>=', ErlangTokenType.GE),
            (r'=', ErlangTokenType.MATCH),
            (r'!', ErlangTokenType.SEND),
            (r'\+', ErlangTokenType.PLUS),
            (r'-', ErlangTokenType.MINUS),
            (r'\*', ErlangTokenType.MULTIPLY),
            (r'/', ErlangTokenType.DIVIDE),
            (r'<', ErlangTokenType.LT),
            (r'>', ErlangTokenType.GT),
            (r'\(', ErlangTokenType.LPAREN),
            (r'\)', ErlangTokenType.RPAREN),
            (r'\[', ErlangTokenType.LBRACKET),
            (r'\]', ErlangTokenType.RBRACKET),
            (r'\{', ErlangTokenType.LBRACE),
            (r'\}', ErlangTokenType.RBRACE),
            (r'\.', ErlangTokenType.DOT),
            (r',', ErlangTokenType.COMMA),
            (r';', ErlangTokenType.SEMICOLON),
            (r':', ErlangTokenType.COLON),
            (r'\|', ErlangTokenType.PIPE),
            (r'#', ErlangTokenType.HASH),
            (r'"[^"]*"', ErlangTokenType.STRING),
            (r'-?\d+\.\d+', ErlangTokenType.FLOAT),
            (r'-?\d+', ErlangTokenType.INTEGER),
            (r'[A-Z][a-zA-Z0-9_]*', ErlangTokenType.VARIABLE),
            (r'[a-z][a-zA-Z0-9_]*', ErlangTokenType.ATOM),
            (r'\s+', None),  # Whitespace
        ]
        
        self.compiled_patterns = [(re.compile(pattern), token_type) 
                                 for pattern, token_type in self.patterns]
    
    def tokenize(self) -> List[ErlangToken]:
        """Tokenize the input text."""
        while self.pos < len(self.text):
            if self._match_patterns():
                continue
            else:
                char = self.text[self.pos]
                raise SyntaxError(f"Unexpected character '{char}' at line {self.line}, column {self.column}")
        
        self.tokens.append(ErlangToken(ErlangTokenType.EOF, "", self.line, self.column))
        return self.tokens
    
    def _match_patterns(self) -> bool:
        """Try to match patterns at current position."""
        for pattern, token_type in self.compiled_patterns:
            match = pattern.match(self.text, self.pos)
            if match:
                value = match.group(0)
                
                if token_type is not None:  # Not whitespace
                    # Check for keywords
                    if token_type == ErlangTokenType.ATOM and value in self.keywords:
                        token_type = getattr(ErlangTokenType, value.upper(), ErlangTokenType.ATOM)
                    
                    token = ErlangToken(token_type, value, self.line, self.column)
                    self.tokens.append(token)
                
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


class ErlangParser:
    """Erlang parser."""
    
    def __init__(self, tokens: List[ErlangToken]):
        self.tokens = tokens
        self.pos = 0
        self.current_token = tokens[0] if tokens else None
    
    def parse(self) -> ErlangProgram:
        """Parse tokens into Erlang program."""
        module = self._parse_module()
        return ErlangProgram(module)
    
    def _parse_module(self) -> ErlangModule:
        """Parse module definition."""
        # Expect: -module(name).
        self._consume_atom('-')
        self._consume_atom('module')
        self._consume(ErlangTokenType.LPAREN)
        name = self._parse_atom().value
        self._consume(ErlangTokenType.RPAREN)
        self._consume(ErlangTokenType.DOT)
        
        attributes = []
        functions = []
        
        # Parse attributes and functions
        while not self._is_at_end():
            if self._check(ErlangTokenType.MINUS):
                attr = self._parse_attribute()
                attributes.append(attr)
            else:
                func = self._parse_function()
                functions.append(func)
        
        return ErlangModule(name, attributes, functions)
    
    def _parse_attribute(self) -> ErlangAttribute:
        """Parse module attribute."""
        self._consume_atom('-')
        
        if self._check_atom('export'):
            return self._parse_export()
        elif self._check_atom('import'):
            return self._parse_import()
        else:
            # Generic attribute
            name = self._parse_atom().value
            self._consume(ErlangTokenType.LPAREN)
            value = self._parse_expression()
            self._consume(ErlangTokenType.RPAREN)
            self._consume(ErlangTokenType.DOT)
            return ErlangAttribute(name, value)
    
    def _parse_export(self) -> ErlangExport:
        """Parse export attribute."""
        self._consume_atom('export')
        self._consume(ErlangTokenType.LPAREN)
        self._consume(ErlangTokenType.LBRACKET)
        
        functions = []
        while not self._check(ErlangTokenType.RBRACKET):
            name = self._parse_atom().value
            self._consume(ErlangTokenType.DIVIDE)
            arity = int(self._consume(ErlangTokenType.INTEGER).value)
            functions.append((name, arity))
            
            if self._check(ErlangTokenType.COMMA):
                self._advance()
        
        self._consume(ErlangTokenType.RBRACKET)
        self._consume(ErlangTokenType.RPAREN)
        self._consume(ErlangTokenType.DOT)
        
        return ErlangExport(functions)
    
    def _parse_import(self) -> ErlangImport:
        """Parse import attribute."""
        self._consume_atom('import')
        self._consume(ErlangTokenType.LPAREN)
        module_name = self._parse_atom().value
        self._consume(ErlangTokenType.COMMA)
        self._consume(ErlangTokenType.LBRACKET)
        
        functions = []
        while not self._check(ErlangTokenType.RBRACKET):
            name = self._parse_atom().value
            self._consume(ErlangTokenType.DIVIDE)
            arity = int(self._consume(ErlangTokenType.INTEGER).value)
            functions.append((name, arity))
            
            if self._check(ErlangTokenType.COMMA):
                self._advance()
        
        self._consume(ErlangTokenType.RBRACKET)
        self._consume(ErlangTokenType.RPAREN)
        self._consume(ErlangTokenType.DOT)
        
        return ErlangImport(module_name, functions)
    
    def _parse_function(self) -> ErlangFunction:
        """Parse function definition."""
        clauses = []
        name = self._parse_atom().value
        
        # Parse all clauses for this function
        while self._check_atom(name):
            clause = self._parse_clause()
            clauses.append(clause)
            
            if self._check(ErlangTokenType.DOT):
                self._advance()
                break
            elif self._check(ErlangTokenType.SEMICOLON):
                self._advance()
        
        arity = len(clauses[0].patterns) if clauses else 0
        return ErlangFunction(name, arity, clauses)
    
    def _parse_clause(self) -> ErlangClause:
        """Parse function clause."""
        # Skip function name (already parsed)
        self._advance()
        
        # Parse patterns
        self._consume(ErlangTokenType.LPAREN)
        patterns = []
        
        while not self._check(ErlangTokenType.RPAREN):
            pattern = self._parse_expression()
            patterns.append(pattern)
            
            if self._check(ErlangTokenType.COMMA):
                self._advance()
        
        self._consume(ErlangTokenType.RPAREN)
        
        # Parse guards (optional)
        guards = None
        if self._check_atom('when'):
            self._advance()
            guards = [self._parse_guard()]
        
        # Parse body
        self._consume(ErlangTokenType.ARROW)
        body = []
        
        while not self._check(ErlangTokenType.SEMICOLON) and not self._check(ErlangTokenType.DOT):
            expr = self._parse_expression()
            body.append(expr)
            
            if self._check(ErlangTokenType.COMMA):
                self._advance()
        
        return ErlangClause(patterns, guards, body)
    
    def _parse_guard(self) -> ErlangGuard:
        """Parse guard expression."""
        tests = []
        
        while True:
            test = self._parse_expression()
            tests.append(test)
            
            if self._check(ErlangTokenType.COMMA):
                self._advance()
            else:
                break
        
        return ErlangGuard(tests)
    
    def _parse_expression(self) -> ErlangExpression:
        """Parse expression."""
        return self._parse_match()
    
    def _parse_match(self) -> ErlangExpression:
        """Parse match expression."""
        left = self._parse_send()
        
        if self._check(ErlangTokenType.MATCH):
            self._advance()
            right = self._parse_match()
            return ErlangMatch(left, right)
        
        return left
    
    def _parse_send(self) -> ErlangExpression:
        """Parse send expression."""
        left = self._parse_or()
        
        if self._check(ErlangTokenType.SEND):
            self._advance()
            right = self._parse_send()
            return ErlangSend(left, right)
        
        return left
    
    def _parse_or(self) -> ErlangExpression:
        """Parse logical or."""
        left = self._parse_and()
        
        while self._check_atom('or'):
            op = self.current_token.value
            self._advance()
            right = self._parse_and()
            left = ErlangBinaryOp(left, op, right)
        
        return left
    
    def _parse_and(self) -> ErlangExpression:
        """Parse logical and."""
        left = self._parse_equality()
        
        while self._check_atom('and'):
            op = self.current_token.value
            self._advance()
            right = self._parse_equality()
            left = ErlangBinaryOp(left, op, right)
        
        return left
    
    def _parse_equality(self) -> ErlangExpression:
        """Parse equality expressions."""
        left = self._parse_comparison()
        
        while self._check(ErlangTokenType.EQ) or self._check(ErlangTokenType.NE):
            op = self.current_token.value
            self._advance()
            right = self._parse_comparison()
            left = ErlangBinaryOp(left, op, right)
        
        return left
    
    def _parse_comparison(self) -> ErlangExpression:
        """Parse comparison expressions."""
        left = self._parse_addition()
        
        while (self._check(ErlangTokenType.LT) or self._check(ErlangTokenType.LE) or
               self._check(ErlangTokenType.GT) or self._check(ErlangTokenType.GE)):
            op = self.current_token.value
            self._advance()
            right = self._parse_addition()
            left = ErlangBinaryOp(left, op, right)
        
        return left
    
    def _parse_addition(self) -> ErlangExpression:
        """Parse addition/subtraction."""
        left = self._parse_multiplication()
        
        while self._check(ErlangTokenType.PLUS) or self._check(ErlangTokenType.MINUS):
            op = self.current_token.value
            self._advance()
            right = self._parse_multiplication()
            left = ErlangBinaryOp(left, op, right)
        
        return left
    
    def _parse_multiplication(self) -> ErlangExpression:
        """Parse multiplication/division."""
        left = self._parse_unary()
        
        while self._check(ErlangTokenType.MULTIPLY) or self._check(ErlangTokenType.DIVIDE):
            op = self.current_token.value
            self._advance()
            right = self._parse_unary()
            left = ErlangBinaryOp(left, op, right)
        
        return left
    
    def _parse_unary(self) -> ErlangExpression:
        """Parse unary expressions."""
        if self._check(ErlangTokenType.MINUS) or self._check_atom('not'):
            op = self.current_token.value
            self._advance()
            expr = self._parse_unary()
            return ErlangUnaryOp(op, expr)
        
        return self._parse_primary()
    
    def _parse_primary(self) -> ErlangExpression:
        """Parse primary expressions."""
        if self._check(ErlangTokenType.INTEGER):
            value = int(self.current_token.value)
            self._advance()
            return ErlangInteger(value)
        
        elif self._check(ErlangTokenType.FLOAT):
            value = float(self.current_token.value)
            self._advance()
            return ErlangFloat(value)
        
        elif self._check(ErlangTokenType.STRING):
            value = self.current_token.value[1:-1]  # Remove quotes
            self._advance()
            return ErlangString(value)
        
        elif self._check(ErlangTokenType.ATOM):
            if self._check_atom('true'):
                self._advance()
                return ErlangBoolean(True)
            elif self._check_atom('false'):
                self._advance()
                return ErlangBoolean(False)
            elif self._check_atom('case'):
                return self._parse_case()
            elif self._check_atom('if'):
                return self._parse_if()
            elif self._check_atom('fun'):
                return self._parse_fun()
            elif self._check_atom('spawn'):
                return self._parse_spawn()
            elif self._check_atom('receive'):
                return self._parse_receive()
            else:
                atom = ErlangAtom(self.current_token.value)
                self._advance()
                
                # Check for function call
                if self._check(ErlangTokenType.COLON):
                    self._advance()
                    func = self._parse_atom()
                    self._consume(ErlangTokenType.LPAREN)
                    args = self._parse_arguments()
                    self._consume(ErlangTokenType.RPAREN)
                    return ErlangFunctionCall(atom, func, args)
                elif self._check(ErlangTokenType.LPAREN):
                    self._advance()
                    args = self._parse_arguments()
                    self._consume(ErlangTokenType.RPAREN)
                    return ErlangFunctionCall(None, atom, args)
                else:
                    return atom
        
        elif self._check(ErlangTokenType.VARIABLE):
            name = self.current_token.value
            self._advance()
            return ErlangVariable(name)
        
        elif self._check(ErlangTokenType.LBRACKET):
            return self._parse_list()
        
        elif self._check(ErlangTokenType.LBRACE):
            return self._parse_tuple()
        
        elif self._check(ErlangTokenType.LPAREN):
            self._advance()
            expr = self._parse_expression()
            self._consume(ErlangTokenType.RPAREN)
            return expr
        
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token.value}")
    
    def _parse_case(self) -> ErlangCase:
        """Parse case expression."""
        self._consume_atom('case')
        expr = self._parse_expression()
        self._consume_atom('of')
        
        clauses = []
        while not self._check_atom('end'):
            clause = self._parse_clause()
            clauses.append(clause)
            
            if self._check(ErlangTokenType.SEMICOLON):
                self._advance()
        
        self._consume_atom('end')
        return ErlangCase(expr, clauses)
    
    def _parse_if(self) -> ErlangIf:
        """Parse if expression."""
        self._consume_atom('if')
        
        clauses = []
        while not self._check_atom('end'):
            guard = self._parse_guard()
            self._consume(ErlangTokenType.ARROW)
            
            body = []
            while not self._check(ErlangTokenType.SEMICOLON) and not self._check_atom('end'):
                expr = self._parse_expression()
                body.append(expr)
                
                if self._check(ErlangTokenType.COMMA):
                    self._advance()
            
            clause = ErlangClause([], [guard], body)
            clauses.append(clause)
            
            if self._check(ErlangTokenType.SEMICOLON):
                self._advance()
        
        self._consume_atom('end')
        return ErlangIf(clauses)
    
    def _parse_fun(self) -> ErlangLambda:
        """Parse fun expression."""
        self._consume_atom('fun')
        
        clauses = []
        while not self._check_atom('end'):
            self._consume(ErlangTokenType.LPAREN)
            
            patterns = []
            while not self._check(ErlangTokenType.RPAREN):
                pattern = self._parse_expression()
                patterns.append(pattern)
                
                if self._check(ErlangTokenType.COMMA):
                    self._advance()
            
            self._consume(ErlangTokenType.RPAREN)
            self._consume(ErlangTokenType.ARROW)
            
            body = []
            while not self._check(ErlangTokenType.SEMICOLON) and not self._check_atom('end'):
                expr = self._parse_expression()
                body.append(expr)
                
                if self._check(ErlangTokenType.COMMA):
                    self._advance()
            
            clause = ErlangClause(patterns, None, body)
            clauses.append(clause)
            
            if self._check(ErlangTokenType.SEMICOLON):
                self._advance()
        
        self._consume_atom('end')
        return ErlangLambda(clauses)
    
    def _parse_spawn(self) -> ErlangSpawn:
        """Parse spawn expression."""
        self._consume_atom('spawn')
        self._consume(ErlangTokenType.LPAREN)
        
        # Check for module:function syntax
        first_arg = self._parse_expression()
        
        if self._check(ErlangTokenType.COMMA):
            self._advance()
            function = self._parse_expression()
            self._consume(ErlangTokenType.COMMA)
            args_list = self._parse_expression()  # Should be a list
            self._consume(ErlangTokenType.RPAREN)
            return ErlangSpawn(first_arg, function, [args_list])
        else:
            # spawn(Fun)
            self._consume(ErlangTokenType.RPAREN)
            return ErlangSpawn(None, first_arg, [])
    
    def _parse_receive(self) -> ErlangReceive:
        """Parse receive expression."""
        self._consume_atom('receive')
        
        clauses = []
        while not self._check_atom('after') and not self._check_atom('end'):
            clause = self._parse_clause()
            clauses.append(clause)
            
            if self._check(ErlangTokenType.SEMICOLON):
                self._advance()
        
        after_clause = None
        if self._check_atom('after'):
            self._advance()
            timeout = self._parse_expression()
            self._consume(ErlangTokenType.ARROW)
            
            body = []
            while not self._check_atom('end'):
                expr = self._parse_expression()
                body.append(expr)
                
                if self._check(ErlangTokenType.COMMA):
                    self._advance()
            
            after_clause = (timeout, body)
        
        self._consume_atom('end')
        return ErlangReceive(clauses, after_clause)
    
    def _parse_list(self) -> ErlangList:
        """Parse list literal."""
        self._consume(ErlangTokenType.LBRACKET)
        
        if self._check(ErlangTokenType.RBRACKET):
            self._advance()
            return ErlangList([])
        
        elements = []
        tail = None
        
        while not self._check(ErlangTokenType.RBRACKET):
            elem = self._parse_expression()
            elements.append(elem)
            
            if self._check(ErlangTokenType.PIPE):
                self._advance()
                tail = self._parse_expression()
                break
            elif self._check(ErlangTokenType.COMMA):
                self._advance()
        
        self._consume(ErlangTokenType.RBRACKET)
        return ErlangList(elements, tail)
    
    def _parse_tuple(self) -> ErlangTuple:
        """Parse tuple literal."""
        self._consume(ErlangTokenType.LBRACE)
        
        elements = []
        while not self._check(ErlangTokenType.RBRACE):
            elem = self._parse_expression()
            elements.append(elem)
            
            if self._check(ErlangTokenType.COMMA):
                self._advance()
        
        self._consume(ErlangTokenType.RBRACE)
        return ErlangTuple(elements)
    
    def _parse_arguments(self) -> List[ErlangExpression]:
        """Parse function arguments."""
        args = []
        
        while not self._check(ErlangTokenType.RPAREN):
            arg = self._parse_expression()
            args.append(arg)
            
            if self._check(ErlangTokenType.COMMA):
                self._advance()
        
        return args
    
    def _parse_atom(self) -> ErlangAtom:
        """Parse atom."""
        if self.current_token.type != ErlangTokenType.ATOM:
            raise SyntaxError(f"Expected atom, got {self.current_token.value}")
        
        value = self.current_token.value
        self._advance()
        return ErlangAtom(value)
    
    # Helper methods
    def _advance(self):
        """Move to next token."""
        if not self._is_at_end():
            self.pos += 1
            if self.pos < len(self.tokens):
                self.current_token = self.tokens[self.pos]
    
    def _is_at_end(self) -> bool:
        """Check if at end of tokens."""
        return (self.current_token is None or 
                self.current_token.type == ErlangTokenType.EOF)
    
    def _check(self, token_type: ErlangTokenType) -> bool:
        """Check if current token is of given type."""
        if self._is_at_end():
            return False
        return self.current_token.type == token_type
    
    def _check_atom(self, value: str) -> bool:
        """Check if current token is specific atom."""
        return (self._check(ErlangTokenType.ATOM) and 
                self.current_token.value == value)
    
    def _consume(self, token_type: ErlangTokenType) -> ErlangToken:
        """Consume token of given type."""
        if self._check(token_type):
            token = self.current_token
            self._advance()
            return token
        else:
            expected = token_type.name
            actual = self.current_token.value if self.current_token else "EOF"
            raise SyntaxError(f"Expected {expected}, got {actual}")
    
    def _consume_atom(self, value: str) -> ErlangToken:
        """Consume specific atom."""
        if self._check_atom(value):
            token = self.current_token
            self._advance()
            return token
        else:
            actual = self.current_token.value if self.current_token else "EOF"
            raise SyntaxError(f"Expected '{value}', got '{actual}'")


def parse_erlang(source_code: str) -> ErlangProgram:
    """Parse Erlang source code into AST."""
    try:
        lexer = ErlangLexer(source_code)
        tokens = lexer.tokenize()
        
        # Filter out comments
        tokens = [t for t in tokens if t.type != ErlangTokenType.COMMENT]
        
        parser = ErlangParser(tokens)
        return parser.parse()
    
    except Exception as e:
        raise SyntaxError(f"Erlang parsing error: {e}")


def parse_erlang_expression(source_code: str) -> ErlangExpression:
    """Parse single Erlang expression."""
    try:
        lexer = ErlangLexer(source_code)
        tokens = lexer.tokenize()
        
        tokens = [t for t in tokens if t.type != ErlangTokenType.COMMENT]
        
        parser = ErlangParser(tokens)
        return parser._parse_expression()
    
    except Exception as e:
        raise SyntaxError(f"Erlang expression parsing error: {e}") 