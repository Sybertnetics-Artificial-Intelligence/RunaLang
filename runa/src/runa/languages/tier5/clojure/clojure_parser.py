#!/usr/bin/env python3
"""
Clojure Parser

Parses Clojure source code into AST. Handles S-expressions, special forms,
collections, reader macros, and all core Clojure syntax.
"""

from typing import List, Optional, Dict, Any, Union, Iterator
from dataclasses import dataclass
from enum import Enum, auto
import re

from .clojure_ast import *


class ClojureTokenType(Enum):
    """Clojure token types."""
    # Literals
    NIL = auto()
    BOOLEAN = auto()
    NUMBER = auto()
    STRING = auto()
    CHARACTER = auto()
    KEYWORD = auto()
    
    # Identifiers
    SYMBOL = auto()
    QUALIFIED_SYMBOL = auto()
    
    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    LBRACE = auto()
    RBRACE = auto()
    
    # Reader macros
    QUOTE = auto()
    SYNTAX_QUOTE = auto()
    UNQUOTE = auto()
    UNQUOTE_SPLICING = auto()
    DEREF = auto()
    METADATA = auto()
    
    # Special characters
    HASH = auto()
    COMMA = auto()
    
    # End of file
    EOF = auto()
    
    # Comments
    COMMENT = auto()


@dataclass
class ClojureToken:
    """Clojure token."""
    type: ClojureTokenType
    value: str
    line: int = 1
    column: int = 1


class ClojureLexer:
    """Clojure lexer."""
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        
        # Token patterns
        self.patterns = {
            ClojureTokenType.NIL: r'\bnil\b',
            ClojureTokenType.BOOLEAN: r'\b(true|false)\b',
            ClojureTokenType.NUMBER: r'-?\d+(\.\d+)?([eE][+-]?\d+)?',
            ClojureTokenType.STRING: r'"(?:[^"\\]|\\.)*"',
            ClojureTokenType.CHARACTER: r'\\(?:newline|space|tab|return|[a-zA-Z0-9])',
            ClojureTokenType.KEYWORD: r':[a-zA-Z_*+!?-][a-zA-Z0-9_*+!?-]*(?:/[a-zA-Z_*+!?-][a-zA-Z0-9_*+!?-]*)?',
            ClojureTokenType.QUALIFIED_SYMBOL: r'[a-zA-Z_*+!?-][a-zA-Z0-9_*+!?-]*/[a-zA-Z_*+!?-][a-zA-Z0-9_*+!?-]*',
            ClojureTokenType.SYMBOL: r'[a-zA-Z_*+!?-][a-zA-Z0-9_*+!?-]*',
            ClojureTokenType.COMMENT: r';[^\n]*',
        }
        
        # Single character tokens
        self.single_chars = {
            '(': ClojureTokenType.LPAREN,
            ')': ClojureTokenType.RPAREN,
            '[': ClojureTokenType.LBRACKET,
            ']': ClojureTokenType.RBRACKET,
            '{': ClojureTokenType.LBRACE,
            '}': ClojureTokenType.RBRACE,
            "'": ClojureTokenType.QUOTE,
            '`': ClojureTokenType.SYNTAX_QUOTE,
            '~': ClojureTokenType.UNQUOTE,
            '@': ClojureTokenType.DEREF,
            '^': ClojureTokenType.METADATA,
            '#': ClojureTokenType.HASH,
            ',': ClojureTokenType.COMMA,
        }
    
    def tokenize(self) -> List[ClojureToken]:
        """Tokenize the source code."""
        while self.pos < len(self.source):
            self._skip_whitespace()
            
            if self.pos >= len(self.source):
                break
            
            # Check for comments
            if self.source[self.pos] == ';':
                self._scan_comment()
                continue
            
            # Check for unquote splicing (~@)
            if self.pos + 1 < len(self.source) and self.source[self.pos:self.pos+2] == '~@':
                self.tokens.append(ClojureToken(ClojureTokenType.UNQUOTE_SPLICING, '~@', self.line, self.column))
                self._advance(2)
                continue
            
            # Check single character tokens
            char = self.source[self.pos]
            if char in self.single_chars:
                self.tokens.append(ClojureToken(self.single_chars[char], char, self.line, self.column))
                self._advance()
                continue
            
            # Check for strings
            if char == '"':
                self._scan_string()
                continue
            
            # Check for keywords, symbols, numbers, etc.
            token = self._scan_atom()
            if token:
                self.tokens.append(token)
                continue
            
            # Unknown character
            raise ValueError(f"Unexpected character '{char}' at line {self.line}, column {self.column}")
        
        self.tokens.append(ClojureToken(ClojureTokenType.EOF, '', self.line, self.column))
        return self.tokens
    
    def _advance(self, count: int = 1):
        """Advance position and update line/column."""
        for _ in range(count):
            if self.pos < len(self.source):
                if self.source[self.pos] == '\n':
                    self.line += 1
                    self.column = 1
                else:
                    self.column += 1
                self.pos += 1
    
    def _skip_whitespace(self):
        """Skip whitespace characters."""
        while self.pos < len(self.source) and self.source[self.pos] in ' \t\n\r,':
            self._advance()
    
    def _scan_comment(self):
        """Scan comment."""
        start_pos = self.pos
        while self.pos < len(self.source) and self.source[self.pos] != '\n':
            self._advance()
        
        comment_text = self.source[start_pos:self.pos]
        # Comments are typically ignored, but we can store them for formatting
        # self.tokens.append(ClojureToken(ClojureTokenType.COMMENT, comment_text, self.line, self.column))
    
    def _scan_string(self):
        """Scan string literal."""
        start_line = self.line
        start_col = self.column
        start_pos = self.pos
        
        self._advance()  # Skip opening quote
        
        while self.pos < len(self.source):
            char = self.source[self.pos]
            if char == '"':
                self._advance()  # Skip closing quote
                break
            elif char == '\\':
                self._advance()  # Skip escape
                if self.pos < len(self.source):
                    self._advance()  # Skip escaped character
            else:
                self._advance()
        
        string_value = self.source[start_pos:self.pos]
        self.tokens.append(ClojureToken(ClojureTokenType.STRING, string_value, start_line, start_col))
    
    def _scan_atom(self) -> Optional[ClojureToken]:
        """Scan atomic values (numbers, symbols, keywords, etc.)."""
        start_pos = self.pos
        start_line = self.line
        start_col = self.column
        
        # Find end of atom
        while (self.pos < len(self.source) and 
               self.source[self.pos] not in ' \t\n\r()[]{}";,'):
            self._advance()
        
        if start_pos == self.pos:
            return None
        
        atom_text = self.source[start_pos:self.pos]
        
        # Determine token type
        for token_type, pattern in self.patterns.items():
            if re.fullmatch(pattern, atom_text):
                return ClojureToken(token_type, atom_text, start_line, start_col)
        
        # Default to symbol
        return ClojureToken(ClojureTokenType.SYMBOL, atom_text, start_line, start_col)


class ClojureParser:
    """Clojure parser."""
    
    def __init__(self, tokens: List[ClojureToken]):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[0] if tokens else None
    
    def parse(self) -> ClojureModule:
        """Parse tokens into AST."""
        forms = []
        namespace = None
        
        while not self._is_at_end():
            if self._check(ClojureTokenType.EOF):
                break
            
            form = self._parse_form()
            if form:
                # Check if this is a namespace declaration
                if isinstance(form, ClojureNs):
                    namespace = form
                else:
                    forms.append(form)
        
        return ClojureModule(namespace=namespace, forms=forms)
    
    def _parse_form(self) -> Optional[ClojureExpression]:
        """Parse a top-level form."""
        if self._check(ClojureTokenType.LPAREN):
            return self._parse_list()
        elif self._check(ClojureTokenType.LBRACKET):
            return self._parse_vector()
        elif self._check(ClojureTokenType.LBRACE):
            return self._parse_map()
        elif self._check(ClojureTokenType.HASH):
            return self._parse_set()
        elif self._check(ClojureTokenType.QUOTE):
            return self._parse_quote()
        elif self._check(ClojureTokenType.SYNTAX_QUOTE):
            return self._parse_syntax_quote()
        elif self._check(ClojureTokenType.UNQUOTE):
            return self._parse_unquote()
        elif self._check(ClojureTokenType.UNQUOTE_SPLICING):
            return self._parse_unquote_splicing()
        elif self._check(ClojureTokenType.DEREF):
            return self._parse_deref()
        else:
            return self._parse_atom()
    
    def _parse_list(self) -> ClojureExpression:
        """Parse list expression."""
        self._consume(ClojureTokenType.LPAREN)
        
        if self._check(ClojureTokenType.RPAREN):
            self._advance()
            return ClojureList([])
        
        elements = []
        first_element = self._parse_form()
        
        # Check for special forms
        if isinstance(first_element, ClojureSymbol):
            if first_element.name == 'def':
                return self._parse_def_form(elements)
            elif first_element.name == 'defn':
                return self._parse_defn_form(elements)
            elif first_element.name == 'fn':
                return self._parse_fn_form(elements)
            elif first_element.name == 'let':
                return self._parse_let_form(elements)
            elif first_element.name == 'if':
                return self._parse_if_form(elements)
            elif first_element.name == 'do':
                return self._parse_do_form(elements)
            elif first_element.name == 'loop':
                return self._parse_loop_form(elements)
            elif first_element.name == 'recur':
                return self._parse_recur_form(elements)
            elif first_element.name == 'ns':
                return self._parse_ns_form(elements)
        
        # Regular list
        elements.append(first_element)
        while not self._check(ClojureTokenType.RPAREN) and not self._is_at_end():
            elements.append(self._parse_form())
        
        self._consume(ClojureTokenType.RPAREN)
        return ClojureList(elements)
    
    def _parse_def_form(self, elements: List) -> ClojureDef:
        """Parse def form."""
        symbol = self._parse_form()
        value = self._parse_form()
        self._consume(ClojureTokenType.RPAREN)
        
        if not isinstance(symbol, ClojureSymbol):
            raise ValueError("def requires a symbol")
        
        return ClojureDef(symbol=symbol, value=value)
    
    def _parse_defn_form(self, elements: List) -> ClojureDefn:
        """Parse defn form."""
        name = self._parse_form()
        
        if not isinstance(name, ClojureSymbol):
            raise ValueError("defn requires a symbol name")
        
        # Optional docstring
        doc_string = None
        next_form = self._parse_form()
        if isinstance(next_form, ClojureLiteral) and next_form.literal_type == "string":
            doc_string = next_form.value
            next_form = self._parse_form()
        
        # Parse function body (simplified - assumes single arity)
        if isinstance(next_form, ClojureVector):
            params = [elem for elem in next_form.elements if isinstance(elem, ClojureSymbol)]
            body = []
            while not self._check(ClojureTokenType.RPAREN) and not self._is_at_end():
                body.append(self._parse_form())
            
            arity = ClojureFnArity(params=params, body=body)
            self._consume(ClojureTokenType.RPAREN)
            return ClojureDefn(name=name, doc_string=doc_string, arities=[arity])
        
        raise ValueError("Invalid defn form")
    
    def _parse_fn_form(self, elements: List) -> ClojureFn:
        """Parse fn form."""
        # Simplified fn parsing
        params_form = self._parse_form()
        if not isinstance(params_form, ClojureVector):
            raise ValueError("fn requires parameter vector")
        
        params = [elem for elem in params_form.elements if isinstance(elem, ClojureSymbol)]
        body = []
        while not self._check(ClojureTokenType.RPAREN) and not self._is_at_end():
            body.append(self._parse_form())
        
        arity = ClojureFnArity(params=params, body=body)
        self._consume(ClojureTokenType.RPAREN)
        return ClojureFn(arities=[arity])
    
    def _parse_let_form(self, elements: List) -> ClojureLet:
        """Parse let form."""
        bindings_form = self._parse_form()
        if not isinstance(bindings_form, ClojureVector):
            raise ValueError("let requires binding vector")
        
        # Parse bindings (symbol value pairs)
        bindings = []
        binding_elements = bindings_form.elements
        for i in range(0, len(binding_elements), 2):
            if i + 1 < len(binding_elements):
                symbol = binding_elements[i]
                value = binding_elements[i + 1]
                if isinstance(symbol, ClojureSymbol):
                    bindings.append((symbol, value))
        
        # Parse body
        body = []
        while not self._check(ClojureTokenType.RPAREN) and not self._is_at_end():
            body.append(self._parse_form())
        
        self._consume(ClojureTokenType.RPAREN)
        return ClojureLet(bindings=bindings, body=body)
    
    def _parse_if_form(self, elements: List) -> ClojureIf:
        """Parse if form."""
        test = self._parse_form()
        then_expr = self._parse_form()
        
        else_expr = None
        if not self._check(ClojureTokenType.RPAREN):
            else_expr = self._parse_form()
        
        self._consume(ClojureTokenType.RPAREN)
        return ClojureIf(test=test, then_expr=then_expr, else_expr=else_expr)
    
    def _parse_do_form(self, elements: List) -> ClojureDo:
        """Parse do form."""
        expressions = []
        while not self._check(ClojureTokenType.RPAREN) and not self._is_at_end():
            expressions.append(self._parse_form())
        
        self._consume(ClojureTokenType.RPAREN)
        return ClojureDo(expressions=expressions)
    
    def _parse_loop_form(self, elements: List) -> ClojureLoop:
        """Parse loop form."""
        bindings_form = self._parse_form()
        if not isinstance(bindings_form, ClojureVector):
            raise ValueError("loop requires binding vector")
        
        # Parse bindings
        bindings = []
        binding_elements = bindings_form.elements
        for i in range(0, len(binding_elements), 2):
            if i + 1 < len(binding_elements):
                symbol = binding_elements[i]
                value = binding_elements[i + 1]
                if isinstance(symbol, ClojureSymbol):
                    bindings.append((symbol, value))
        
        # Parse body
        body = []
        while not self._check(ClojureTokenType.RPAREN) and not self._is_at_end():
            body.append(self._parse_form())
        
        self._consume(ClojureTokenType.RPAREN)
        return ClojureLoop(bindings=bindings, body=body)
    
    def _parse_recur_form(self, elements: List) -> ClojureRecur:
        """Parse recur form."""
        args = []
        while not self._check(ClojureTokenType.RPAREN) and not self._is_at_end():
            args.append(self._parse_form())
        
        self._consume(ClojureTokenType.RPAREN)
        return ClojureRecur(args=args)
    
    def _parse_ns_form(self, elements: List) -> ClojureNs:
        """Parse namespace form."""
        name = self._parse_form()
        if not isinstance(name, ClojureSymbol):
            raise ValueError("ns requires a symbol name")
        
        # Skip remaining forms for now (simplified)
        while not self._check(ClojureTokenType.RPAREN) and not self._is_at_end():
            self._parse_form()
        
        self._consume(ClojureTokenType.RPAREN)
        return ClojureNs(name=name)
    
    def _parse_vector(self) -> ClojureVector:
        """Parse vector."""
        self._consume(ClojureTokenType.LBRACKET)
        
        elements = []
        while not self._check(ClojureTokenType.RBRACKET) and not self._is_at_end():
            elements.append(self._parse_form())
        
        self._consume(ClojureTokenType.RBRACKET)
        return ClojureVector(elements)
    
    def _parse_map(self) -> ClojureMap:
        """Parse map."""
        self._consume(ClojureTokenType.LBRACE)
        
        pairs = []
        while not self._check(ClojureTokenType.RBRACE) and not self._is_at_end():
            key = self._parse_form()
            if self._check(ClojureTokenType.RBRACE):
                break
            value = self._parse_form()
            pairs.append((key, value))
        
        self._consume(ClojureTokenType.RBRACE)
        return ClojureMap(pairs)
    
    def _parse_set(self) -> ClojureSet:
        """Parse set."""
        self._consume(ClojureTokenType.HASH)
        self._consume(ClojureTokenType.LBRACE)
        
        elements = []
        while not self._check(ClojureTokenType.RBRACE) and not self._is_at_end():
            elements.append(self._parse_form())
        
        self._consume(ClojureTokenType.RBRACE)
        return ClojureSet(elements)
    
    def _parse_quote(self) -> ClojureQuote:
        """Parse quote."""
        self._consume(ClojureTokenType.QUOTE)
        expression = self._parse_form()
        return ClojureQuote(expression)
    
    def _parse_syntax_quote(self) -> ClojureSyntaxQuote:
        """Parse syntax quote."""
        self._consume(ClojureTokenType.SYNTAX_QUOTE)
        expression = self._parse_form()
        return ClojureSyntaxQuote(expression)
    
    def _parse_unquote(self) -> ClojureUnquote:
        """Parse unquote."""
        self._consume(ClojureTokenType.UNQUOTE)
        expression = self._parse_form()
        return ClojureUnquote(expression)
    
    def _parse_unquote_splicing(self) -> ClojureUnquoteSplicing:
        """Parse unquote splicing."""
        self._consume(ClojureTokenType.UNQUOTE_SPLICING)
        expression = self._parse_form()
        return ClojureUnquoteSplicing(expression)
    
    def _parse_deref(self) -> ClojureDeref:
        """Parse deref."""
        self._consume(ClojureTokenType.DEREF)
        expression = self._parse_form()
        return ClojureDeref(expression)
    
    def _parse_atom(self) -> ClojureExpression:
        """Parse atomic value."""
        token = self.current_token
        
        if token.type == ClojureTokenType.NIL:
            self._advance()
            return ClojureLiteral(None, "nil")
        elif token.type == ClojureTokenType.BOOLEAN:
            self._advance()
            return ClojureLiteral(token.value == "true", "boolean")
        elif token.type == ClojureTokenType.NUMBER:
            self._advance()
            if '.' in token.value:
                return ClojureLiteral(float(token.value), "number")
            else:
                return ClojureLiteral(int(token.value), "number")
        elif token.type == ClojureTokenType.STRING:
            self._advance()
            # Remove quotes and handle escape sequences
            string_value = token.value[1:-1]
            return ClojureLiteral(string_value, "string")
        elif token.type == ClojureTokenType.CHARACTER:
            self._advance()
            return ClojureLiteral(token.value, "char")
        elif token.type == ClojureTokenType.KEYWORD:
            self._advance()
            return ClojureLiteral(token.value, "keyword")
        elif token.type in (ClojureTokenType.SYMBOL, ClojureTokenType.QUALIFIED_SYMBOL):
            self._advance()
            if '/' in token.value:
                namespace, name = token.value.split('/', 1)
                return ClojureSymbol(name, namespace)
            else:
                return ClojureSymbol(token.value)
        
        raise ValueError(f"Unexpected token: {token.value}")
    
    def _advance(self):
        """Advance to next token."""
        if not self._is_at_end():
            self.pos += 1
            if self.pos < len(self.tokens):
                self.current_token = self.tokens[self.pos]
    
    def _check(self, token_type: ClojureTokenType) -> bool:
        """Check if current token is of given type."""
        return not self._is_at_end() and self.current_token.type == token_type
    
    def _consume(self, token_type: ClojureTokenType):
        """Consume token of given type or raise error."""
        if self._check(token_type):
            self._advance()
        else:
            raise ValueError(f"Expected {token_type}, got {self.current_token.type}")
    
    def _is_at_end(self) -> bool:
        """Check if at end of tokens."""
        return self.pos >= len(self.tokens) or self.current_token.type == ClojureTokenType.EOF


def parse_clojure(source_code: str) -> ClojureModule:
    """Parse Clojure source code into AST."""
    lexer = ClojureLexer(source_code)
    tokens = lexer.tokenize()
    parser = ClojureParser(tokens)
    return parser.parse() 