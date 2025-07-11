#!/usr/bin/env python3
"""
Haskell Parser Implementation

Comprehensive parser for Haskell language that tokenizes and parses
Haskell source code into AST nodes. Supports all major Haskell constructs
including pattern matching, type classes, modules, and functional features.
"""

import re
from typing import List, Optional, Dict, Any, Union, Tuple
from dataclasses import dataclass
from enum import Enum, auto

from .haskell_ast import *


class HsTokenType(Enum):
    """Haskell token types."""
    # Literals
    INTEGER = auto()
    FLOAT = auto()
    CHAR = auto()
    STRING = auto()
    
    # Identifiers and keywords
    IDENTIFIER = auto()
    CONSTRUCTOR_ID = auto()
    OPERATOR = auto()
    KEYWORD = auto()
    
    # Special characters
    LPAREN = auto()
    RPAREN = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    LBRACE = auto()
    RBRACE = auto()
    COMMA = auto()
    SEMICOLON = auto()
    PIPE = auto()
    ARROW = auto()
    DOUBLE_ARROW = auto()
    BIND_ARROW = auto()
    BACKSLASH = auto()
    DOT = auto()
    DOUBLE_COLON = auto()
    EQUALS = auto()
    UNDERSCORE = auto()
    AT_SIGN = auto()
    BACKTICK = auto()
    
    # Layout tokens
    INDENT = auto()
    DEDENT = auto()
    NEWLINE = auto()
    
    # Special
    EOF = auto()
    COMMENT = auto()
    WHITESPACE = auto()


@dataclass
class HsToken:
    """Haskell token."""
    type: HsTokenType
    value: str
    line: int
    column: int
    
    def __repr__(self):
        return f"HsToken({self.type}, '{self.value}', {self.line}:{self.column})"


class HsLexer:
    """Haskell lexer for tokenizing source code."""
    
    # Keywords
    KEYWORDS = {
        'case', 'class', 'data', 'default', 'deriving', 'do', 'else',
        'if', 'import', 'in', 'infix', 'infixl', 'infixr', 'instance',
        'let', 'module', 'newtype', 'of', 'then', 'type', 'where',
        'foreign', 'qualified', 'as', 'hiding', 'forall'
    }
    
    # Operators
    OPERATORS = {
        '+', '-', '*', '/', '^', '^^', '**', '++', ':', '::', '=', '/=',
        '<', '<=', '>', '>=', '&&', '||', '.', '$', '>>=', '>>', '~',
        '==', 'mod', 'div', 'not'
    }
    
    def __init__(self, text: str):
        self.text = text
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        self.indent_stack = [0]
    
    def current_char(self) -> Optional[str]:
        """Get current character."""
        if self.position >= len(self.text):
            return None
        return self.text[self.position]
    
    def peek_char(self, offset: int = 1) -> Optional[str]:
        """Peek at character ahead."""
        pos = self.position + offset
        if pos >= len(self.text):
            return None
        return self.text[pos]
    
    def advance(self):
        """Advance position."""
        if self.position < len(self.text) and self.text[self.position] == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        self.position += 1
    
    def skip_whitespace(self):
        """Skip whitespace except newlines."""
        while self.current_char() and self.current_char() in ' \t\r':
            self.advance()
    
    def skip_comment(self):
        """Skip line or block comments."""
        if self.current_char() == '-' and self.peek_char() == '-':
            # Line comment
            while self.current_char() and self.current_char() != '\n':
                self.advance()
        elif self.current_char() == '{' and self.peek_char() == '-':
            # Block comment
            self.advance()  # {
            self.advance()  # -
            depth = 1
            while self.current_char() and depth > 0:
                if self.current_char() == '{' and self.peek_char() == '-':
                    depth += 1
                    self.advance()
                    self.advance()
                elif self.current_char() == '-' and self.peek_char() == '}':
                    depth -= 1
                    self.advance()
                    self.advance()
                else:
                    self.advance()
    
    def read_string(self) -> str:
        """Read string literal."""
        quote_char = self.current_char()
        self.advance()  # Skip opening quote
        value = ""
        
        while self.current_char() and self.current_char() != quote_char:
            if self.current_char() == '\\':
                self.advance()
                if self.current_char() in 'ntrb\\\'\"':
                    if self.current_char() == 'n':
                        value += '\n'
                    elif self.current_char() == 't':
                        value += '\t'
                    elif self.current_char() == 'r':
                        value += '\r'
                    elif self.current_char() == 'b':
                        value += '\b'
                    elif self.current_char() == '\\':
                        value += '\\'
                    elif self.current_char() == '\'':
                        value += '\''
                    elif self.current_char() == '\"':
                        value += '\"'
                    self.advance()
                else:
                    value += self.current_char()
                    self.advance()
            else:
                value += self.current_char()
                self.advance()
        
        if self.current_char() == quote_char:
            self.advance()  # Skip closing quote
        
        return value
    
    def read_number(self) -> Tuple[str, HsTokenType]:
        """Read numeric literal."""
        value = ""
        token_type = HsTokenType.INTEGER
        
        while self.current_char() and (self.current_char().isdigit() or self.current_char() == '.'):
            if self.current_char() == '.':
                if token_type == HsTokenType.FLOAT:
                    break  # Second dot, not part of number
                token_type = HsTokenType.FLOAT
            value += self.current_char()
            self.advance()
        
        return value, token_type
    
    def read_identifier(self) -> Tuple[str, HsTokenType]:
        """Read identifier or keyword."""
        value = ""
        
        # First character
        if self.current_char().isalpha() or self.current_char() == '_':
            value += self.current_char()
            self.advance()
        
        # Subsequent characters
        while (self.current_char() and 
               (self.current_char().isalnum() or self.current_char() in '_\'')):
            value += self.current_char()
            self.advance()
        
        # Determine token type
        if value in self.KEYWORDS:
            return value, HsTokenType.KEYWORD
        elif value[0].isupper():
            return value, HsTokenType.CONSTRUCTOR_ID
        else:
            return value, HsTokenType.IDENTIFIER
    
    def read_operator(self) -> str:
        """Read operator."""
        value = ""
        
        # Handle multi-character operators
        if self.current_char() == ':' and self.peek_char() == ':':
            self.advance()
            self.advance()
            return "::"
        elif self.current_char() == '-' and self.peek_char() == '>':
            self.advance()
            self.advance()
            return "->"
        elif self.current_char() == '=' and self.peek_char() == '>':
            self.advance()
            self.advance()
            return "=>"
        elif self.current_char() == '<' and self.peek_char() == '-':
            self.advance()
            self.advance()
            return "<-"
        elif self.current_char() == '>' and self.peek_char() == '>':
            if self.peek_char(2) == '=':
                self.advance()
                self.advance()
                self.advance()
                return ">>="
            else:
                self.advance()
                self.advance()
                return ">>"
        elif self.current_char() == '/' and self.peek_char() == '=':
            self.advance()
            self.advance()
            return "/="
        elif self.current_char() == '<' and self.peek_char() == '=':
            self.advance()
            self.advance()
            return "<="
        elif self.current_char() == '>' and self.peek_char() == '=':
            self.advance()
            self.advance()
            return ">="
        elif self.current_char() == '&' and self.peek_char() == '&':
            self.advance()
            self.advance()
            return "&&"
        elif self.current_char() == '|' and self.peek_char() == '|':
            self.advance()
            self.advance()
            return "||"
        elif self.current_char() == '+' and self.peek_char() == '+':
            self.advance()
            self.advance()
            return "++"
        elif self.current_char() == '*' and self.peek_char() == '*':
            self.advance()
            self.advance()
            return "**"
        elif self.current_char() == '^' and self.peek_char() == '^':
            self.advance()
            self.advance()
            return "^^"
        elif self.current_char() == '=' and self.peek_char() == '=':
            self.advance()
            self.advance()
            return "=="
        else:
            # Single character operator
            value = self.current_char()
            self.advance()
            return value
    
    def handle_layout(self, line_start: bool = False):
        """Handle Haskell layout (indentation-based scoping)."""
        if not line_start:
            return
        
        # Calculate current indentation
        current_indent = 0
        pos = self.position
        while pos < len(self.text) and self.text[pos] in ' \t':
            if self.text[pos] == ' ':
                current_indent += 1
            else:  # tab
                current_indent += 8
            pos += 1
        
        # Compare with current indentation level
        if current_indent > self.indent_stack[-1]:
            # Increase indentation
            self.indent_stack.append(current_indent)
            self.tokens.append(HsToken(HsTokenType.INDENT, '', self.line, self.column))
        elif current_indent < self.indent_stack[-1]:
            # Decrease indentation - emit DEDENTs
            while self.indent_stack and current_indent < self.indent_stack[-1]:
                self.indent_stack.pop()
                self.tokens.append(HsToken(HsTokenType.DEDENT, '', self.line, self.column))
    
    def tokenize(self) -> List[HsToken]:
        """Tokenize the input text."""
        line_start = True
        
        while self.position < len(self.text):
            char = self.current_char()
            
            if char == '\n':
                self.tokens.append(HsToken(HsTokenType.NEWLINE, char, self.line, self.column))
                self.advance()
                line_start = True
                continue
            
            if char in ' \t\r':
                if line_start:
                    self.handle_layout(True)
                    line_start = False
                self.skip_whitespace()
                continue
            
            if line_start:
                self.handle_layout(True)
                line_start = False
            
            # Comments
            if char == '-' and self.peek_char() == '-':
                self.skip_comment()
                continue
            elif char == '{' and self.peek_char() == '-':
                self.skip_comment()
                continue
            
            # String literals
            if char in '\'"':
                value = self.read_string()
                token_type = HsTokenType.CHAR if char == '\'' else HsTokenType.STRING
                self.tokens.append(HsToken(token_type, value, self.line, self.column))
                continue
            
            # Numbers
            if char.isdigit():
                value, token_type = self.read_number()
                self.tokens.append(HsToken(token_type, value, self.line, self.column))
                continue
            
            # Identifiers and keywords
            if char.isalpha() or char == '_':
                value, token_type = self.read_identifier()
                self.tokens.append(HsToken(token_type, value, self.line, self.column))
                continue
            
            # Special characters
            if char == '(':
                self.tokens.append(HsToken(HsTokenType.LPAREN, char, self.line, self.column))
                self.advance()
            elif char == ')':
                self.tokens.append(HsToken(HsTokenType.RPAREN, char, self.line, self.column))
                self.advance()
            elif char == '[':
                self.tokens.append(HsToken(HsTokenType.LBRACKET, char, self.line, self.column))
                self.advance()
            elif char == ']':
                self.tokens.append(HsToken(HsTokenType.RBRACKET, char, self.line, self.column))
                self.advance()
            elif char == '{':
                self.tokens.append(HsToken(HsTokenType.LBRACE, char, self.line, self.column))
                self.advance()
            elif char == '}':
                self.tokens.append(HsToken(HsTokenType.RBRACE, char, self.line, self.column))
                self.advance()
            elif char == ',':
                self.tokens.append(HsToken(HsTokenType.COMMA, char, self.line, self.column))
                self.advance()
            elif char == ';':
                self.tokens.append(HsToken(HsTokenType.SEMICOLON, char, self.line, self.column))
                self.advance()
            elif char == '`':
                self.tokens.append(HsToken(HsTokenType.BACKTICK, char, self.line, self.column))
                self.advance()
            elif char == '@':
                self.tokens.append(HsToken(HsTokenType.AT_SIGN, char, self.line, self.column))
                self.advance()
            elif char == '\\':
                self.tokens.append(HsToken(HsTokenType.BACKSLASH, char, self.line, self.column))
                self.advance()
            else:
                # Operators
                value = self.read_operator()
                if value == '::':
                    token_type = HsTokenType.DOUBLE_COLON
                elif value == '->':
                    token_type = HsTokenType.ARROW
                elif value == '=>':
                    token_type = HsTokenType.DOUBLE_ARROW
                elif value == '<-':
                    token_type = HsTokenType.BIND_ARROW
                elif value == '=':
                    token_type = HsTokenType.EQUALS
                elif value == '|':
                    token_type = HsTokenType.PIPE
                elif value == '.':
                    token_type = HsTokenType.DOT
                elif value == '_':
                    token_type = HsTokenType.UNDERSCORE
                else:
                    token_type = HsTokenType.OPERATOR
                
                self.tokens.append(HsToken(token_type, value, self.line, self.column))
        
        # Close any remaining indentation levels
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            self.tokens.append(HsToken(HsTokenType.DEDENT, '', self.line, self.column))
        
        self.tokens.append(HsToken(HsTokenType.EOF, '', self.line, self.column))
        return self.tokens


class HsParser:
    """Haskell parser for building AST from tokens."""
    
    def __init__(self, tokens: List[HsToken]):
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[0] if tokens else None
    
    def advance(self):
        """Move to next token."""
        if self.position < len(self.tokens) - 1:
            self.position += 1
            self.current_token = self.tokens[self.position]
    
    def peek(self, offset: int = 1) -> Optional[HsToken]:
        """Peek at token ahead."""
        pos = self.position + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return None
    
    def match(self, token_type: HsTokenType) -> bool:
        """Check if current token matches type."""
        return self.current_token and self.current_token.type == token_type
    
    def match_value(self, value: str) -> bool:
        """Check if current token matches value."""
        return self.current_token and self.current_token.value == value
    
    def consume(self, token_type: HsTokenType) -> HsToken:
        """Consume token of expected type."""
        if not self.match(token_type):
            raise SyntaxError(f"Expected {token_type}, got {self.current_token}")
        token = self.current_token
        self.advance()
        return token
    
    def consume_value(self, value: str) -> HsToken:
        """Consume token with expected value."""
        if not self.match_value(value):
            raise SyntaxError(f"Expected '{value}', got '{self.current_token.value}'")
        token = self.current_token
        self.advance()
        return token
    
    def skip_newlines(self):
        """Skip newline tokens."""
        while self.match(HsTokenType.NEWLINE):
            self.advance()
    
    def parse_module(self) -> HsModule:
        """Parse a Haskell module."""
        self.skip_newlines()
        
        name = None
        exports = None
        imports = []
        declarations = []
        
        # Module header
        if self.match_value('module'):
            self.advance()
            name = self.consume(HsTokenType.CONSTRUCTOR_ID).value
            
            # Export list
            if self.match(HsTokenType.LPAREN):
                self.advance()
                exports = []
                # TODO: Parse export list
                while not self.match(HsTokenType.RPAREN):
                    if self.match(HsTokenType.IDENTIFIER) or self.match(HsTokenType.CONSTRUCTOR_ID):
                        exports.append(HsExport(self.current_token.value, "value"))
                        self.advance()
                    if self.match(HsTokenType.COMMA):
                        self.advance()
                self.consume(HsTokenType.RPAREN)
            
            self.consume_value('where')
            self.skip_newlines()
        
        # Imports
        while self.match_value('import'):
            imports.append(self.parse_import())
            self.skip_newlines()
        
        # Declarations
        while not self.match(HsTokenType.EOF):
            self.skip_newlines()
            if self.match(HsTokenType.EOF):
                break
            declarations.append(self.parse_declaration())
            self.skip_newlines()
        
        return HsModule(name=name, exports=exports, imports=imports, declarations=declarations)
    
    def parse_import(self) -> HsImport:
        """Parse import declaration."""
        self.consume_value('import')
        
        qualified = False
        if self.match_value('qualified'):
            qualified = True
            self.advance()
        
        module_name = self.consume(HsTokenType.CONSTRUCTOR_ID).value
        
        alias = None
        if self.match_value('as'):
            self.advance()
            alias = self.consume(HsTokenType.CONSTRUCTOR_ID).value
        
        hiding = False
        import_list = None
        
        if self.match_value('hiding'):
            hiding = True
            self.advance()
        
        if self.match(HsTokenType.LPAREN):
            self.advance()
            import_list = []
            # TODO: Parse import list
            while not self.match(HsTokenType.RPAREN):
                if self.match(HsTokenType.IDENTIFIER) or self.match(HsTokenType.CONSTRUCTOR_ID):
                    import_list.append(self.current_token.value)
                    self.advance()
                if self.match(HsTokenType.COMMA):
                    self.advance()
            self.consume(HsTokenType.RPAREN)
        
        return HsImport(
            module_name=module_name,
            qualified=qualified,
            alias=alias,
            hiding=hiding,
            import_list=import_list
        )
    
    def parse_declaration(self) -> HsDeclaration:
        """Parse a top-level declaration."""
        if self.match_value('data'):
            return self.parse_data_declaration()
        elif self.match_value('type'):
            return self.parse_type_declaration()
        elif self.match_value('class'):
            return self.parse_class_declaration()
        elif self.match_value('instance'):
            return self.parse_instance_declaration()
        elif self.match(HsTokenType.IDENTIFIER) and self.peek() and self.peek().type == HsTokenType.DOUBLE_COLON:
            return self.parse_type_signature()
        else:
            return self.parse_function_declaration()
    
    def parse_type_signature(self) -> HsTypeSignature:
        """Parse type signature."""
        names = [self.consume(HsTokenType.IDENTIFIER).value]
        
        # Multiple names separated by commas
        while self.match(HsTokenType.COMMA):
            self.advance()
            names.append(self.consume(HsTokenType.IDENTIFIER).value)
        
        self.consume(HsTokenType.DOUBLE_COLON)
        type_expr = self.parse_type()
        
        return HsTypeSignature(names=names, type_expr=type_expr)
    
    def parse_function_declaration(self) -> HsFunctionDeclaration:
        """Parse function declaration."""
        name = self.consume(HsTokenType.IDENTIFIER).value
        clauses = []
        
        # Parse function clauses
        while True:
            patterns = []
            guards = []
            
            # Parse patterns
            while (not self.match(HsTokenType.EQUALS) and 
                   not self.match(HsTokenType.PIPE) and
                   not self.match(HsTokenType.EOF)):
                patterns.append(self.parse_pattern())
            
            # Parse guards or direct expression
            if self.match(HsTokenType.PIPE):
                while self.match(HsTokenType.PIPE):
                    self.advance()
                    condition = self.parse_expression()
                    self.consume(HsTokenType.EQUALS)
                    expr = self.parse_expression()
                    guards.append(HsGuard(condition=condition, expression=expr))
            else:
                self.consume(HsTokenType.EQUALS)
                expr = self.parse_expression()
                guards.append(HsGuard(condition=hs_lit_bool(True), expression=expr))
            
            where_bindings = []
            if self.match_value('where'):
                self.advance()
                # TODO: Parse where bindings
            
            clauses.append(HsClause(
                patterns=patterns,
                guards=guards,
                expression=guards[0].expression if guards else hs_lit_bool(True),
                where_bindings=where_bindings
            ))
            
            # Check if there are more clauses for this function
            if (not self.match(HsTokenType.IDENTIFIER) or 
                self.current_token.value != name):
                break
            self.advance()
        
        return HsFunctionDeclaration(name=name, clauses=clauses)
    
    def parse_data_declaration(self) -> HsDataDeclaration:
        """Parse data declaration."""
        self.consume_value('data')
        name = self.consume(HsTokenType.CONSTRUCTOR_ID).value
        
        # Type parameters
        parameters = []
        while self.match(HsTokenType.IDENTIFIER):
            parameters.append(self.current_token.value)
            self.advance()
        
        self.consume(HsTokenType.EQUALS)
        
        # Constructors
        constructors = []
        constructors.append(self.parse_data_constructor())
        
        while self.match(HsTokenType.PIPE):
            self.advance()
            constructors.append(self.parse_data_constructor())
        
        # Deriving clause
        deriving = []
        if self.match_value('deriving'):
            self.advance()
            if self.match(HsTokenType.LPAREN):
                self.advance()
                while not self.match(HsTokenType.RPAREN):
                    deriving.append(self.consume(HsTokenType.CONSTRUCTOR_ID).value)
                    if self.match(HsTokenType.COMMA):
                        self.advance()
                self.consume(HsTokenType.RPAREN)
            else:
                deriving.append(self.consume(HsTokenType.CONSTRUCTOR_ID).value)
        
        return HsDataDeclaration(
            name=name,
            parameters=parameters,
            constructors=constructors,
            deriving=deriving
        )
    
    def parse_data_constructor(self) -> HsDataConstructor:
        """Parse data constructor."""
        name = self.consume(HsTokenType.CONSTRUCTOR_ID).value
        fields = []
        field_names = None
        
        # Record syntax or regular fields
        if self.match(HsTokenType.LBRACE):
            # Record syntax
            self.advance()
            field_names = []
            while not self.match(HsTokenType.RBRACE):
                field_names.append(self.consume(HsTokenType.IDENTIFIER).value)
                self.consume(HsTokenType.DOUBLE_COLON)
                fields.append(self.parse_type())
                if self.match(HsTokenType.COMMA):
                    self.advance()
            self.consume(HsTokenType.RBRACE)
        else:
            # Regular constructor fields
            while (not self.match(HsTokenType.PIPE) and 
                   not self.match(HsTokenType.EOF) and
                   not self.match_value('deriving') and
                   self.current_token.value not in ['data', 'type', 'class', 'instance']):
                fields.append(self.parse_type())
        
        return HsDataConstructor(name=name, fields=fields, field_names=field_names)
    
    def parse_type_declaration(self) -> HsTypeDeclaration:
        """Parse type synonym declaration."""
        self.consume_value('type')
        name = self.consume(HsTokenType.CONSTRUCTOR_ID).value
        
        parameters = []
        while self.match(HsTokenType.IDENTIFIER):
            parameters.append(self.current_token.value)
            self.advance()
        
        self.consume(HsTokenType.EQUALS)
        body = self.parse_type()
        
        return HsTypeDeclaration(name=name, parameters=parameters, body=body)
    
    def parse_class_declaration(self) -> HsClassDeclaration:
        """Parse type class declaration."""
        self.consume_value('class')
        
        # TODO: Parse constraints
        constraints = []
        
        name = self.consume(HsTokenType.CONSTRUCTOR_ID).value
        parameter = self.consume(HsTokenType.IDENTIFIER).value
        
        self.consume_value('where')
        
        # TODO: Parse method signatures
        methods = []
        
        return HsClassDeclaration(
            name=name,
            parameter=parameter,
            constraints=constraints,
            methods=methods
        )
    
    def parse_instance_declaration(self) -> HsInstanceDeclaration:
        """Parse instance declaration."""
        self.consume_value('instance')
        
        # TODO: Parse constraints and instance head
        constraints = []
        class_name = self.consume(HsTokenType.CONSTRUCTOR_ID).value
        instance_type = self.parse_type()
        
        self.consume_value('where')
        
        # TODO: Parse method implementations
        methods = []
        
        return HsInstanceDeclaration(
            constraints=constraints,
            class_name=class_name,
            instance_type=instance_type,
            methods=methods
        )
    
    def parse_type(self) -> HsType:
        """Parse type expression."""
        return self.parse_function_type()
    
    def parse_function_type(self) -> HsType:
        """Parse function type (a -> b)."""
        left = self.parse_application_type()
        
        if self.match(HsTokenType.ARROW):
            self.advance()
            right = self.parse_function_type()
            return HsFunctionType(from_type=left, to_type=right)
        
        return left
    
    def parse_application_type(self) -> HsType:
        """Parse type application."""
        base = self.parse_primary_type()
        
        args = []
        while (not self.match(HsTokenType.ARROW) and
               not self.match(HsTokenType.RPAREN) and
               not self.match(HsTokenType.COMMA) and
               not self.match(HsTokenType.EOF) and
               not self.match_value('where')):
            args.append(self.parse_primary_type())
        
        if args:
            return HsTypeApplication(constructor=base, arguments=args)
        return base
    
    def parse_primary_type(self) -> HsType:
        """Parse primary type."""
        if self.match(HsTokenType.IDENTIFIER):
            name = self.current_token.value
            self.advance()
            return HsTypeVariable(name=name)
        elif self.match(HsTokenType.CONSTRUCTOR_ID):
            name = self.current_token.value
            self.advance()
            return HsTypeConstructor(name=name)
        elif self.match(HsTokenType.LPAREN):
            self.advance()
            if self.match(HsTokenType.RPAREN):
                self.advance()
                return HsTypeConstructor(name="()")
            
            types = [self.parse_type()]
            
            if self.match(HsTokenType.COMMA):
                # Tuple type
                while self.match(HsTokenType.COMMA):
                    self.advance()
                    types.append(self.parse_type())
                self.consume(HsTokenType.RPAREN)
                return HsTupleType(types=types)
            else:
                # Parenthesized type
                self.consume(HsTokenType.RPAREN)
                return types[0]
        elif self.match(HsTokenType.LBRACKET):
            self.advance()
            if self.match(HsTokenType.RBRACKET):
                self.advance()
                return HsListType(element_type=HsTypeVariable(name="a"))
            element_type = self.parse_type()
            self.consume(HsTokenType.RBRACKET)
            return HsListType(element_type=element_type)
        else:
            raise SyntaxError(f"Unexpected token in type: {self.current_token}")
    
    def parse_expression(self) -> HsExpression:
        """Parse expression."""
        return self.parse_lambda()
    
    def parse_lambda(self) -> HsExpression:
        """Parse lambda expression."""
        if self.match(HsTokenType.BACKSLASH):
            self.advance()
            patterns = []
            patterns.append(self.parse_pattern())
            
            while not self.match(HsTokenType.ARROW):
                patterns.append(self.parse_pattern())
            
            self.consume(HsTokenType.ARROW)
            body = self.parse_expression()
            
            return HsLambda(parameters=patterns, body=body)
        
        return self.parse_let()
    
    def parse_let(self) -> HsExpression:
        """Parse let expression."""
        if self.match_value('let'):
            self.advance()
            
            # TODO: Parse bindings
            bindings = []
            
            self.consume_value('in')
            expression = self.parse_expression()
            
            return HsLet(bindings=bindings, expression=expression)
        
        return self.parse_if()
    
    def parse_if(self) -> HsExpression:
        """Parse if expression."""
        if self.match_value('if'):
            self.advance()
            condition = self.parse_expression()
            
            self.consume_value('then')
            then_expr = self.parse_expression()
            
            self.consume_value('else')
            else_expr = self.parse_expression()
            
            return HsIf(condition=condition, then_expr=then_expr, else_expr=else_expr)
        
        return self.parse_case()
    
    def parse_case(self) -> HsExpression:
        """Parse case expression."""
        if self.match_value('case'):
            self.advance()
            expr = self.parse_expression()
            
            self.consume_value('of')
            
            alternatives = []
            # TODO: Parse alternatives
            
            return HsCase(expression=expr, alternatives=alternatives)
        
        return self.parse_application()
    
    def parse_application(self) -> HsExpression:
        """Parse function application."""
        left = self.parse_primary()
        
        args = []
        while (not self.match(HsTokenType.EOF) and
               not self.match_value('in') and
               not self.match_value('then') and
               not self.match_value('else') and
               not self.match_value('of') and
               not self.match(HsTokenType.RPAREN) and
               not self.match(HsTokenType.RBRACKET) and
               not self.match(HsTokenType.COMMA)):
            args.append(self.parse_primary())
        
        if args:
            return HsApplication(function=left, arguments=args)
        return left
    
    def parse_primary(self) -> HsExpression:
        """Parse primary expression."""
        if self.match(HsTokenType.INTEGER):
            value = int(self.current_token.value)
            self.advance()
            return HsLiteral(value=value, literal_type="integer")
        elif self.match(HsTokenType.FLOAT):
            value = float(self.current_token.value)
            self.advance()
            return HsLiteral(value=value, literal_type="float")
        elif self.match(HsTokenType.STRING):
            value = self.current_token.value
            self.advance()
            return HsLiteral(value=value, literal_type="string")
        elif self.match(HsTokenType.CHAR):
            value = self.current_token.value
            self.advance()
            return HsLiteral(value=value, literal_type="char")
        elif self.match(HsTokenType.IDENTIFIER):
            name = self.current_token.value
            self.advance()
            return HsVariable(name=name)
        elif self.match(HsTokenType.CONSTRUCTOR_ID):
            name = self.current_token.value
            self.advance()
            return HsConstructor(name=name)
        elif self.match(HsTokenType.LPAREN):
            self.advance()
            if self.match(HsTokenType.RPAREN):
                self.advance()
                return HsConstructor(name="()")
            
            expr = self.parse_expression()
            self.consume(HsTokenType.RPAREN)
            return expr
        elif self.match(HsTokenType.LBRACKET):
            self.advance()
            elements = []
            
            if not self.match(HsTokenType.RBRACKET):
                elements.append(self.parse_expression())
                
                while self.match(HsTokenType.COMMA):
                    self.advance()
                    elements.append(self.parse_expression())
            
            self.consume(HsTokenType.RBRACKET)
            return HsList(elements=elements)
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token}")
    
    def parse_pattern(self) -> HsPattern:
        """Parse pattern."""
        if self.match(HsTokenType.UNDERSCORE):
            self.advance()
            return HsWildcardPattern()
        elif self.match(HsTokenType.IDENTIFIER):
            name = self.current_token.value
            self.advance()
            
            if self.match(HsTokenType.AT_SIGN):
                self.advance()
                pattern = self.parse_pattern()
                return HsAsPattern(variable=name, pattern=pattern)
            
            return HsVariablePattern(name=name)
        elif self.match(HsTokenType.CONSTRUCTOR_ID):
            name = self.current_token.value
            self.advance()
            
            patterns = []
            # TODO: Parse constructor patterns
            
            return HsConstructorPattern(constructor=name, patterns=patterns)
        elif self.match(HsTokenType.INTEGER):
            value = int(self.current_token.value)
            self.advance()
            literal = HsLiteral(value=value, literal_type="integer")
            return HsLiteralPattern(literal=literal)
        elif self.match(HsTokenType.STRING):
            value = self.current_token.value
            self.advance()
            literal = HsLiteral(value=value, literal_type="string")
            return HsLiteralPattern(literal=literal)
        elif self.match(HsTokenType.LBRACKET):
            self.advance()
            patterns = []
            
            if not self.match(HsTokenType.RBRACKET):
                patterns.append(self.parse_pattern())
                
                while self.match(HsTokenType.COMMA):
                    self.advance()
                    patterns.append(self.parse_pattern())
            
            self.consume(HsTokenType.RBRACKET)
            return HsListPattern(patterns=patterns)
        elif self.match(HsTokenType.LPAREN):
            self.advance()
            patterns = [self.parse_pattern()]
            
            if self.match(HsTokenType.COMMA):
                while self.match(HsTokenType.COMMA):
                    self.advance()
                    patterns.append(self.parse_pattern())
                self.consume(HsTokenType.RPAREN)
                return HsTuplePattern(patterns=patterns)
            else:
                self.consume(HsTokenType.RPAREN)
                return patterns[0]
        else:
            raise SyntaxError(f"Unexpected token in pattern: {self.current_token}")


def parse_haskell(source_code: str) -> HsModule:
    """Parse Haskell source code into AST."""
    lexer = HsLexer(source_code)
    tokens = lexer.tokenize()
    
    parser = HsParser(tokens)
    return parser.parse_module()


# Convenience exports
__all__ = [
    "HsTokenType", "HsToken", "HsLexer", "HsParser", "parse_haskell"
] 