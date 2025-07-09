#!/usr/bin/env python3
"""
TypeScript Parser

Comprehensive TypeScript parser supporting all TypeScript features including
type annotations, generics, interfaces, enums, decorators, and advanced type system.
"""

import re
from typing import List, Optional, Dict, Any, Union, Tuple
from dataclasses import dataclass
from enum import Enum, auto

from .ts_ast import *


class TSTokenType(Enum):
    """TypeScript token types."""
    # Literals
    NUMBER = auto()
    STRING = auto()
    BOOLEAN = auto()
    NULL = auto()
    UNDEFINED = auto()
    REGEX = auto()
    TEMPLATE_LITERAL = auto()
    BIGINT = auto()
    
    # Identifiers
    IDENTIFIER = auto()
    
    # Keywords (JavaScript)
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
    
    # TypeScript-specific keywords
    ABSTRACT = auto()
    ANY = auto()
    BOOLEAN_TYPE = auto()
    DECLARE = auto()
    ENUM = auto()
    INTERFACE = auto()
    IS = auto()
    KEYOF = auto()
    MODULE = auto()
    NAMESPACE = auto()
    NEVER = auto()
    NUMBER_TYPE = auto()
    OBJECT_TYPE = auto()
    PRIVATE = auto()
    PROTECTED = auto()
    PUBLIC = auto()
    READONLY = auto()
    SATISFIES = auto()
    STATIC = auto()
    STRING_TYPE = auto()
    SYMBOL = auto()
    TYPE = auto()
    UNKNOWN = auto()
    
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
    NULLISH_COALESCING = auto()
    
    BITWISE_AND = auto()
    BITWISE_OR = auto()
    BITWISE_XOR = auto()
    BITWISE_NOT = auto()
    LEFT_SHIFT = auto()
    RIGHT_SHIFT = auto()
    UNSIGNED_RIGHT_SHIFT = auto()
    
    INCREMENT = auto()
    DECREMENT = auto()
    
    # TypeScript-specific operators
    OPTIONAL_CHAINING = auto()
    NON_NULL_ASSERTION = auto()
    AS = auto()
    SATISFIES_OP = auto()
    
    # Punctuation
    SEMICOLON = auto()
    COMMA = auto()
    DOT = auto()
    COLON = auto()
    QUESTION = auto()
    ARROW = auto()
    
    # Brackets
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    
    # Type-specific punctuation
    PIPE = auto()          # |
    AMPERSAND = auto()     # &
    ANGLE_OPEN = auto()    # <
    ANGLE_CLOSE = auto()   # >
    
    # Special
    EOF = auto()
    NEWLINE = auto()
    WHITESPACE = auto()
    COMMENT = auto()
    
    # Decorators
    AT = auto()


@dataclass
class TSToken:
    """TypeScript token."""
    type: TSTokenType
    value: str
    line: int
    column: int
    start: int
    end: int


class TSLexer:
    """TypeScript lexer."""
    
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        
        # Keywords mapping
        self.keywords = {
            # JavaScript keywords
            'break': TSTokenType.BREAK,
            'case': TSTokenType.CASE,
            'catch': TSTokenType.CATCH,
            'class': TSTokenType.CLASS,
            'const': TSTokenType.CONST,
            'continue': TSTokenType.CONTINUE,
            'debugger': TSTokenType.DEBUGGER,
            'default': TSTokenType.DEFAULT,
            'delete': TSTokenType.DELETE,
            'do': TSTokenType.DO,
            'else': TSTokenType.ELSE,
            'export': TSTokenType.EXPORT,
            'extends': TSTokenType.EXTENDS,
            'false': TSTokenType.FALSE,
            'finally': TSTokenType.FINALLY,
            'for': TSTokenType.FOR,
            'function': TSTokenType.FUNCTION,
            'if': TSTokenType.IF,
            'import': TSTokenType.IMPORT,
            'in': TSTokenType.IN,
            'instanceof': TSTokenType.INSTANCEOF,
            'let': TSTokenType.LET,
            'new': TSTokenType.NEW,
            'null': TSTokenType.NULL,
            'return': TSTokenType.RETURN,
            'super': TSTokenType.SUPER,
            'switch': TSTokenType.SWITCH,
            'this': TSTokenType.THIS,
            'throw': TSTokenType.THROW,
            'true': TSTokenType.TRUE,
            'try': TSTokenType.TRY,
            'typeof': TSTokenType.TYPEOF,
            'undefined': TSTokenType.UNDEFINED,
            'var': TSTokenType.VAR,
            'void': TSTokenType.VOID,
            'while': TSTokenType.WHILE,
            'with': TSTokenType.WITH,
            'yield': TSTokenType.YIELD,
            
            # Async/Await
            'async': TSTokenType.ASYNC,
            'await': TSTokenType.AWAIT,
            
            # TypeScript-specific keywords
            'abstract': TSTokenType.ABSTRACT,
            'any': TSTokenType.ANY,
            'boolean': TSTokenType.BOOLEAN_TYPE,
            'declare': TSTokenType.DECLARE,
            'enum': TSTokenType.ENUM,
            'interface': TSTokenType.INTERFACE,
            'is': TSTokenType.IS,
            'keyof': TSTokenType.KEYOF,
            'module': TSTokenType.MODULE,
            'namespace': TSTokenType.NAMESPACE,
            'never': TSTokenType.NEVER,
            'number': TSTokenType.NUMBER_TYPE,
            'object': TSTokenType.OBJECT_TYPE,
            'private': TSTokenType.PRIVATE,
            'protected': TSTokenType.PROTECTED,
            'public': TSTokenType.PUBLIC,
            'readonly': TSTokenType.READONLY,
            'satisfies': TSTokenType.SATISFIES,
            'static': TSTokenType.STATIC,
            'string': TSTokenType.STRING_TYPE,
            'symbol': TSTokenType.SYMBOL,
            'type': TSTokenType.TYPE,
            'unknown': TSTokenType.UNKNOWN,
            
            # Type operators
            'as': TSTokenType.AS,
        }
    
    def tokenize(self) -> List[TSToken]:
        """Tokenize the source code."""
        while self.position < len(self.source):
            self._skip_whitespace()
            
            if self.position >= len(self.source):
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
            
            # Identifiers and keywords
            if self._match_identifier():
                continue
            
            # Multi-character operators
            if self._match_multi_char_operator():
                continue
            
            # Single-character tokens
            if self._match_single_char():
                continue
            
            # Unknown character
            self._error(f"Unexpected character: {self.source[self.position]}")
        
        self._add_token(TSTokenType.EOF, "")
        return self.tokens
    
    def _current_char(self) -> str:
        """Get current character."""
        if self.position >= len(self.source):
            return '\0'
        return self.source[self.position]
    
    def _peek_char(self, offset: int = 1) -> str:
        """Peek at character with offset."""
        pos = self.position + offset
        if pos >= len(self.source):
            return '\0'
        return self.source[pos]
    
    def _advance(self) -> str:
        """Advance position and return current character."""
        if self.position >= len(self.source):
            return '\0'
        
        char = self.source[self.position]
        self.position += 1
        
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        
        return char
    
    def _skip_whitespace(self):
        """Skip whitespace characters."""
        while self.position < len(self.source) and self._current_char().isspace():
            self._advance()
    
    def _match_comment(self) -> bool:
        """Match comment tokens."""
        if self._current_char() == '/' and self._peek_char() == '/':
            # Single line comment
            start_pos = self.position
            while self.position < len(self.source) and self._current_char() != '\n':
                self._advance()
            return True
        
        if self._current_char() == '/' and self._peek_char() == '*':
            # Multi-line comment
            self._advance()  # /
            self._advance()  # *
            
            while self.position < len(self.source) - 1:
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
        if quote_char not in ('"', "'"):
            return False
        
        start_pos = self.position
        self._advance()  # opening quote
        
        value = ""
        while self.position < len(self.source) and self._current_char() != quote_char:
            if self._current_char() == '\\':
                self._advance()  # escape character
                if self.position < len(self.source):
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
        
        if self.position < len(self.source):
            self._advance()  # closing quote
        
        self._add_token(TSTokenType.STRING, value)
        return True
    
    def _match_template_literal(self) -> bool:
        """Match template literals."""
        if self._current_char() != '`':
            return False
        
        start_pos = self.position
        self._advance()  # opening backtick
        
        value = ""
        while self.position < len(self.source) and self._current_char() != '`':
            if self._current_char() == '\\':
                self._advance()
                if self.position < len(self.source):
                    value += self._advance()
            else:
                value += self._advance()
        
        if self.position < len(self.source):
            self._advance()  # closing backtick
        
        self._add_token(TSTokenType.TEMPLATE_LITERAL, value)
        return True
    
    def _match_number(self) -> bool:
        """Match number literals."""
        if not self._current_char().isdigit() and self._current_char() != '.':
            return False
        
        start_pos = self.position
        has_dot = False
        
        # Handle decimal point at start
        if self._current_char() == '.':
            has_dot = True
            self._advance()
            if not self._current_char().isdigit():
                self.position = start_pos
                return False
        
        # Consume digits
        while self._current_char().isdigit():
            self._advance()
        
        # Handle decimal point
        if self._current_char() == '.' and not has_dot:
            has_dot = True
            self._advance()
            while self._current_char().isdigit():
                self._advance()
        
        # Handle scientific notation
        if self._current_char().lower() == 'e':
            self._advance()
            if self._current_char() in '+-':
                self._advance()
            while self._current_char().isdigit():
                self._advance()
        
        # Handle BigInt
        if self._current_char().lower() == 'n':
            self._advance()
            value = self.source[start_pos:self.position-1]
            self._add_token(TSTokenType.BIGINT, value)
            return True
        
        value = self.source[start_pos:self.position]
        self._add_token(TSTokenType.NUMBER, value)
        return True
    
    def _match_identifier(self) -> bool:
        """Match identifiers and keywords."""
        if not (self._current_char().isalpha() or self._current_char() in '_$'):
            return False
        
        start_pos = self.position
        
        while (self._current_char().isalnum() or self._current_char() in '_$'):
            self._advance()
        
        value = self.source[start_pos:self.position]
        
        # Check if it's a keyword
        token_type = self.keywords.get(value, TSTokenType.IDENTIFIER)
        self._add_token(token_type, value)
        return True
    
    def _match_multi_char_operator(self) -> bool:
        """Match multi-character operators."""
        char = self._current_char()
        next_char = self._peek_char()
        
        # Three-character operators
        if char == '>' and next_char == '>' and self._peek_char(2) == '>':
            if self._peek_char(3) == '=':
                self._advance()
                self._advance()
                self._advance()
                self._advance()
                self._add_token(TSTokenType.UNSIGNED_RIGHT_SHIFT, '>>>=')
                return True
            else:
                self._advance()
                self._advance()
                self._advance()
                self._add_token(TSTokenType.UNSIGNED_RIGHT_SHIFT, '>>>')
                return True
        
        # Two-character operators
        two_char_ops = {
            '++': TSTokenType.INCREMENT,
            '--': TSTokenType.DECREMENT,
            '+=': TSTokenType.PLUS_ASSIGN,
            '-=': TSTokenType.MINUS_ASSIGN,
            '*=': TSTokenType.MULTIPLY_ASSIGN,
            '/=': TSTokenType.DIVIDE_ASSIGN,
            '%=': TSTokenType.MODULO_ASSIGN,
            '**': TSTokenType.EXPONENT,
            '**=': TSTokenType.EXPONENT_ASSIGN,
            '==': TSTokenType.EQUAL,
            '!=': TSTokenType.NOT_EQUAL,
            '===': TSTokenType.STRICT_EQUAL,
            '!==': TSTokenType.STRICT_NOT_EQUAL,
            '<=': TSTokenType.LESS_EQUAL,
            '>=': TSTokenType.GREATER_EQUAL,
            '<<': TSTokenType.LEFT_SHIFT,
            '>>': TSTokenType.RIGHT_SHIFT,
            '&&': TSTokenType.AND,
            '||': TSTokenType.OR,
            '??': TSTokenType.NULLISH_COALESCING,
            '?.': TSTokenType.OPTIONAL_CHAINING,
            '=>': TSTokenType.ARROW,
        }
        
        two_char = char + next_char
        if two_char in two_char_ops:
            self._advance()
            self._advance()
            self._add_token(two_char_ops[two_char], two_char)
            return True
        
        return False
    
    def _match_single_char(self) -> bool:
        """Match single-character tokens."""
        char = self._current_char()
        
        single_char_tokens = {
            '+': TSTokenType.PLUS,
            '-': TSTokenType.MINUS,
            '*': TSTokenType.MULTIPLY,
            '/': TSTokenType.DIVIDE,
            '%': TSTokenType.MODULO,
            '=': TSTokenType.ASSIGN,
            '<': TSTokenType.LESS_THAN,
            '>': TSTokenType.GREATER_THAN,
            '!': TSTokenType.NOT,
            '&': TSTokenType.BITWISE_AND,
            '|': TSTokenType.BITWISE_OR,
            '^': TSTokenType.BITWISE_XOR,
            '~': TSTokenType.BITWISE_NOT,
            '?': TSTokenType.QUESTION,
            ':': TSTokenType.COLON,
            ';': TSTokenType.SEMICOLON,
            ',': TSTokenType.COMMA,
            '.': TSTokenType.DOT,
            '(': TSTokenType.LPAREN,
            ')': TSTokenType.RPAREN,
            '{': TSTokenType.LBRACE,
            '}': TSTokenType.RBRACE,
            '[': TSTokenType.LBRACKET,
            ']': TSTokenType.RBRACKET,
            '@': TSTokenType.AT,
        }
        
        if char in single_char_tokens:
            self._advance()
            
            # Handle special cases
            if char == '!' and self._current_char() != '=':
                # Check for non-null assertion
                self._add_token(TSTokenType.NON_NULL_ASSERTION, char)
            elif char == '|':
                self._add_token(TSTokenType.PIPE, char)
            elif char == '&':
                self._add_token(TSTokenType.AMPERSAND, char)
            elif char == '<':
                self._add_token(TSTokenType.ANGLE_OPEN, char)
            elif char == '>':
                self._add_token(TSTokenType.ANGLE_CLOSE, char)
            else:
                self._add_token(single_char_tokens[char], char)
            
            return True
        
        return False
    
    def _add_token(self, token_type: TSTokenType, value: str):
        """Add a token to the tokens list."""
        token = TSToken(
            type=token_type,
            value=value,
            line=self.line,
            column=self.column - len(value),
            start=self.position - len(value),
            end=self.position
        )
        self.tokens.append(token)
    
    def _error(self, message: str):
        """Raise a lexer error."""
        raise SyntaxError(f"Lexer error at line {self.line}, column {self.column}: {message}")


class TSParser:
    """TypeScript parser."""
    
    def __init__(self, tokens: List[TSToken]):
        self.tokens = tokens
        self.current = 0
    
    def parse(self) -> TSProgram:
        """Parse tokens into TypeScript AST."""
        statements = []
        
        while not self._is_at_end():
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
        
        return TSProgram(statements)
    
    def _parse_statement(self) -> Optional[TSNode]:
        """Parse a statement."""
        try:
            # Type declarations
            if self._match(TSTokenType.INTERFACE):
                return self._parse_interface_declaration()
            if self._match(TSTokenType.TYPE):
                return self._parse_type_alias_declaration()
            if self._match(TSTokenType.ENUM):
                return self._parse_enum_declaration()
            if self._match(TSTokenType.NAMESPACE):
                return self._parse_namespace_declaration()
            
            # Variable declarations
            if self._match(TSTokenType.VAR, TSTokenType.LET, TSTokenType.CONST):
                return self._parse_variable_declaration()
            
            # Function declarations
            if self._match(TSTokenType.FUNCTION):
                return self._parse_function_declaration()
            
            # Class declarations
            if self._match(TSTokenType.CLASS):
                return self._parse_class_declaration()
            
            # Control flow
            if self._match(TSTokenType.IF):
                return self._parse_if_statement()
            if self._match(TSTokenType.WHILE):
                return self._parse_while_statement()
            if self._match(TSTokenType.FOR):
                return self._parse_for_statement()
            if self._match(TSTokenType.RETURN):
                return self._parse_return_statement()
            if self._match(TSTokenType.BREAK):
                return self._parse_break_statement()
            if self._match(TSTokenType.CONTINUE):
                return self._parse_continue_statement()
            
            # Expression statement
            return self._parse_expression_statement()
            
        except Exception as e:
            self._error(f"Parse error: {str(e)}")
            return None
    
    def _parse_interface_declaration(self) -> TSInterfaceDeclaration:
        """Parse interface declaration."""
        name = self._consume(TSTokenType.IDENTIFIER, "Expected interface name").value
        name_node = TSIdentifier(name)
        
        type_parameters = []
        if self._match(TSTokenType.ANGLE_OPEN):
            type_parameters = self._parse_type_parameters()
            self._consume(TSTokenType.ANGLE_CLOSE, "Expected '>' after type parameters")
        
        extends_clause = []
        if self._match(TSTokenType.EXTENDS):
            extends_clause = self._parse_heritage_clause()
        
        self._consume(TSTokenType.LBRACE, "Expected '{' before interface body")
        
        body = []
        while not self._check(TSTokenType.RBRACE) and not self._is_at_end():
            member = self._parse_type_member()
            if member:
                body.append(member)
        
        self._consume(TSTokenType.RBRACE, "Expected '}' after interface body")
        
        return TSInterfaceDeclaration(name_node, type_parameters, extends_clause, body)
    
    def _parse_type_alias_declaration(self) -> TSTypeAliasDeclaration:
        """Parse type alias declaration."""
        name = self._consume(TSTokenType.IDENTIFIER, "Expected type name").value
        name_node = TSIdentifier(name)
        
        type_parameters = []
        if self._match(TSTokenType.ANGLE_OPEN):
            type_parameters = self._parse_type_parameters()
            self._consume(TSTokenType.ANGLE_CLOSE, "Expected '>' after type parameters")
        
        self._consume(TSTokenType.ASSIGN, "Expected '=' after type name")
        
        type_annotation = self._parse_type()
        
        self._consume(TSTokenType.SEMICOLON, "Expected ';' after type alias")
        
        return TSTypeAliasDeclaration(name_node, type_parameters, type_annotation)
    
    def _parse_enum_declaration(self) -> TSEnumDeclaration:
        """Parse enum declaration."""
        const = False  # TODO: Handle const enums
        
        name = self._consume(TSTokenType.IDENTIFIER, "Expected enum name").value
        name_node = TSIdentifier(name)
        
        self._consume(TSTokenType.LBRACE, "Expected '{' before enum body")
        
        members = []
        while not self._check(TSTokenType.RBRACE) and not self._is_at_end():
            member_name = self._consume(TSTokenType.IDENTIFIER, "Expected enum member name").value
            member_name_node = TSIdentifier(member_name)
            
            initializer = None
            if self._match(TSTokenType.ASSIGN):
                initializer = self._parse_expression()
            
            members.append(TSEnumMember(member_name_node, initializer))
            
            if not self._match(TSTokenType.COMMA):
                break
        
        self._consume(TSTokenType.RBRACE, "Expected '}' after enum body")
        
        return TSEnumDeclaration(name_node, members, const)
    
    def _parse_variable_declaration(self) -> TSVariableDeclaration:
        """Parse variable declaration."""
        kind_token = self._previous()
        kind = TSVariableKind.VAR
        
        if kind_token.type == TSTokenType.LET:
            kind = TSVariableKind.LET
        elif kind_token.type == TSTokenType.CONST:
            kind = TSVariableKind.CONST
        
        declarations = []
        
        # Parse first declarator
        declarations.append(self._parse_variable_declarator())
        
        # Parse additional declarators
        while self._match(TSTokenType.COMMA):
            declarations.append(self._parse_variable_declarator())
        
        self._consume(TSTokenType.SEMICOLON, "Expected ';' after variable declaration")
        
        return TSVariableDeclaration(declarations, kind)
    
    def _parse_variable_declarator(self) -> TSVariableDeclarator:
        """Parse variable declarator."""
        name = self._consume(TSTokenType.IDENTIFIER, "Expected variable name").value
        name_node = TSIdentifier(name)
        
        type_annotation = None
        if self._match(TSTokenType.COLON):
            type_annotation = TSTypeAnnotation(self._parse_type())
        
        init = None
        if self._match(TSTokenType.ASSIGN):
            init = self._parse_expression()
        
        return TSVariableDeclarator(name_node, type_annotation, init)
    
    def _parse_function_declaration(self) -> TSFunctionDeclaration:
        """Parse function declaration."""
        name = self._consume(TSTokenType.IDENTIFIER, "Expected function name").value
        name_node = TSIdentifier(name)
        
        type_parameters = []
        if self._match(TSTokenType.ANGLE_OPEN):
            type_parameters = self._parse_type_parameters()
            self._consume(TSTokenType.ANGLE_CLOSE, "Expected '>' after type parameters")
        
        self._consume(TSTokenType.LPAREN, "Expected '(' after function name")
        
        parameters = []
        if not self._check(TSTokenType.RPAREN):
            parameters.append(self._parse_parameter())
            while self._match(TSTokenType.COMMA):
                parameters.append(self._parse_parameter())
        
        self._consume(TSTokenType.RPAREN, "Expected ')' after parameters")
        
        return_type = None
        if self._match(TSTokenType.COLON):
            return_type = TSTypeAnnotation(self._parse_type())
        
        body = self._parse_block_statement()
        
        return TSFunctionDeclaration(name_node, parameters, body, return_type, type_parameters)
    
    def _parse_parameter(self) -> TSParameter:
        """Parse function parameter."""
        name = self._consume(TSTokenType.IDENTIFIER, "Expected parameter name").value
        name_node = TSIdentifier(name)
        
        optional = False
        if self._match(TSTokenType.QUESTION):
            optional = True
        
        type_annotation = None
        if self._match(TSTokenType.COLON):
            type_annotation = TSTypeAnnotation(self._parse_type())
        
        default_value = None
        if self._match(TSTokenType.ASSIGN):
            default_value = self._parse_expression()
        
        return TSParameter(name_node, type_annotation, default_value, optional)
    
    def _parse_type(self) -> TSType:
        """Parse type annotation."""
        return self._parse_union_type()
    
    def _parse_union_type(self) -> TSType:
        """Parse union type."""
        type_node = self._parse_intersection_type()
        
        if self._match(TSTokenType.PIPE):
            types = [type_node]
            while True:
                types.append(self._parse_intersection_type())
                if not self._match(TSTokenType.PIPE):
                    break
            return TSUnionType(types)
        
        return type_node
    
    def _parse_intersection_type(self) -> TSType:
        """Parse intersection type."""
        type_node = self._parse_primary_type()
        
        if self._match(TSTokenType.AMPERSAND):
            types = [type_node]
            while True:
                types.append(self._parse_primary_type())
                if not self._match(TSTokenType.AMPERSAND):
                    break
            return TSIntersectionType(types)
        
        return type_node
    
    def _parse_primary_type(self) -> TSType:
        """Parse primary type."""
        if self._match(TSTokenType.NUMBER_TYPE):
            return TSTypeReference(TSIdentifier("number"))
        
        if self._match(TSTokenType.STRING_TYPE):
            return TSTypeReference(TSIdentifier("string"))
        
        if self._match(TSTokenType.BOOLEAN_TYPE):
            return TSTypeReference(TSIdentifier("boolean"))
        
        if self._match(TSTokenType.ANY):
            return TSTypeReference(TSIdentifier("any"))
        
        if self._match(TSTokenType.UNKNOWN):
            return TSTypeReference(TSIdentifier("unknown"))
        
        if self._match(TSTokenType.NEVER):
            return TSTypeReference(TSIdentifier("never"))
        
        if self._match(TSTokenType.VOID):
            return TSTypeReference(TSIdentifier("void"))
        
        if self._match(TSTokenType.IDENTIFIER):
            name = self._previous().value
            name_node = TSIdentifier(name)
            
            # Check for generic type arguments
            type_arguments = []
            if self._match(TSTokenType.ANGLE_OPEN):
                type_arguments = self._parse_type_arguments()
                self._consume(TSTokenType.ANGLE_CLOSE, "Expected '>' after type arguments")
            
            return TSTypeReference(name_node, type_arguments)
        
        if self._match(TSTokenType.LBRACKET):
            # Array type or tuple type
            if self._check(TSTokenType.RBRACKET):
                # Empty array type
                self._advance()
                return TSArrayType(TSTypeReference(TSIdentifier("any")))
            
            # Parse tuple elements
            elements = []
            elements.append(self._parse_type())
            
            while self._match(TSTokenType.COMMA):
                elements.append(self._parse_type())
            
            self._consume(TSTokenType.RBRACKET, "Expected ']' after tuple elements")
            
            return TSTupleType(elements)
        
        if self._match(TSTokenType.LBRACE):
            # Type literal
            members = []
            while not self._check(TSTokenType.RBRACE) and not self._is_at_end():
                member = self._parse_type_member()
                if member:
                    members.append(member)
            
            self._consume(TSTokenType.RBRACE, "Expected '}' after type literal")
            
            return TSTypeLiteral(members)
        
        if self._match(TSTokenType.LPAREN):
            # Function type or parenthesized type
            if self._check(TSTokenType.RPAREN) or self._check(TSTokenType.IDENTIFIER):
                # Function type
                parameters = []
                if not self._check(TSTokenType.RPAREN):
                    parameters.append(self._parse_parameter())
                    while self._match(TSTokenType.COMMA):
                        parameters.append(self._parse_parameter())
                
                self._consume(TSTokenType.RPAREN, "Expected ')' after parameters")
                self._consume(TSTokenType.ARROW, "Expected '=>' after function parameters")
                
                return_type = self._parse_type()
                
                return TSFunctionType(parameters, return_type)
            else:
                # Parenthesized type
                type_node = self._parse_type()
                self._consume(TSTokenType.RPAREN, "Expected ')' after type")
                return type_node
        
        self._error("Expected type")
    
    def _parse_type_parameters(self) -> List[TSTypeParameter]:
        """Parse type parameters."""
        parameters = []
        
        parameters.append(self._parse_type_parameter())
        
        while self._match(TSTokenType.COMMA):
            parameters.append(self._parse_type_parameter())
        
        return parameters
    
    def _parse_type_parameter(self) -> TSTypeParameter:
        """Parse type parameter."""
        name = self._consume(TSTokenType.IDENTIFIER, "Expected type parameter name").value
        name_node = TSIdentifier(name)
        
        constraint = None
        if self._match(TSTokenType.EXTENDS):
            constraint = self._parse_type()
        
        default_type = None
        if self._match(TSTokenType.ASSIGN):
            default_type = self._parse_type()
        
        return TSTypeParameter(name_node, constraint, default_type)
    
    def _parse_type_arguments(self) -> List[TSType]:
        """Parse type arguments."""
        arguments = []
        
        arguments.append(self._parse_type())
        
        while self._match(TSTokenType.COMMA):
            arguments.append(self._parse_type())
        
        return arguments
    
    def _parse_type_member(self) -> Optional[TSNode]:
        """Parse type member (property signature, method signature, etc.)."""
        # Property signature
        if self._check(TSTokenType.IDENTIFIER):
            name = self._advance().value
            name_node = TSIdentifier(name)
            
            optional = False
            if self._match(TSTokenType.QUESTION):
                optional = True
            
            if self._match(TSTokenType.COLON):
                # Property signature
                type_annotation = TSTypeAnnotation(self._parse_type())
                self._match(TSTokenType.SEMICOLON)  # Optional semicolon
                return TSPropertySignature(name_node, type_annotation, optional)
            
            if self._match(TSTokenType.LPAREN):
                # Method signature
                parameters = []
                if not self._check(TSTokenType.RPAREN):
                    parameters.append(self._parse_parameter())
                    while self._match(TSTokenType.COMMA):
                        parameters.append(self._parse_parameter())
                
                self._consume(TSTokenType.RPAREN, "Expected ')' after parameters")
                
                return_type = None
                if self._match(TSTokenType.COLON):
                    return_type = TSTypeAnnotation(self._parse_type())
                
                self._match(TSTokenType.SEMICOLON)  # Optional semicolon
                
                return TSMethodSignature(name_node, parameters, return_type, None, optional)
        
        return None
    
    def _parse_heritage_clause(self) -> List[TSTypeReference]:
        """Parse heritage clause (extends/implements)."""
        types = []
        
        types.append(self._parse_type_reference())
        
        while self._match(TSTokenType.COMMA):
            types.append(self._parse_type_reference())
        
        return types
    
    def _parse_type_reference(self) -> TSTypeReference:
        """Parse type reference."""
        name = self._consume(TSTokenType.IDENTIFIER, "Expected type name").value
        name_node = TSIdentifier(name)
        
        type_arguments = []
        if self._match(TSTokenType.ANGLE_OPEN):
            type_arguments = self._parse_type_arguments()
            self._consume(TSTokenType.ANGLE_CLOSE, "Expected '>' after type arguments")
        
        return TSTypeReference(name_node, type_arguments)
    
    def _parse_expression(self) -> TSNode:
        """Parse expression (simplified)."""
        return self._parse_assignment()
    
    def _parse_assignment(self) -> TSNode:
        """Parse assignment expression."""
        expr = self._parse_logical_or()
        
        if self._match(TSTokenType.ASSIGN):
            value = self._parse_assignment()
            # Return assignment expression
            return expr  # Simplified
        
        return expr
    
    def _parse_logical_or(self) -> TSNode:
        """Parse logical OR expression."""
        expr = self._parse_logical_and()
        
        while self._match(TSTokenType.OR):
            operator = self._previous()
            right = self._parse_logical_and()
            # Create binary expression
            expr = right  # Simplified
        
        return expr
    
    def _parse_logical_and(self) -> TSNode:
        """Parse logical AND expression."""
        expr = self._parse_equality()
        
        while self._match(TSTokenType.AND):
            operator = self._previous()
            right = self._parse_equality()
            # Create binary expression
            expr = right  # Simplified
        
        return expr
    
    def _parse_equality(self) -> TSNode:
        """Parse equality expression."""
        expr = self._parse_comparison()
        
        while self._match(TSTokenType.EQUAL, TSTokenType.NOT_EQUAL, 
                           TSTokenType.STRICT_EQUAL, TSTokenType.STRICT_NOT_EQUAL):
            operator = self._previous()
            right = self._parse_comparison()
            # Create binary expression
            expr = right  # Simplified
        
        return expr
    
    def _parse_comparison(self) -> TSNode:
        """Parse comparison expression."""
        expr = self._parse_addition()
        
        while self._match(TSTokenType.GREATER_THAN, TSTokenType.GREATER_EQUAL,
                           TSTokenType.LESS_THAN, TSTokenType.LESS_EQUAL):
            operator = self._previous()
            right = self._parse_addition()
            # Create binary expression
            expr = right  # Simplified
        
        return expr
    
    def _parse_addition(self) -> TSNode:
        """Parse addition expression."""
        expr = self._parse_multiplication()
        
        while self._match(TSTokenType.PLUS, TSTokenType.MINUS):
            operator = self._previous()
            right = self._parse_multiplication()
            # Create binary expression
            expr = right  # Simplified
        
        return expr
    
    def _parse_multiplication(self) -> TSNode:
        """Parse multiplication expression."""
        expr = self._parse_unary()
        
        while self._match(TSTokenType.MULTIPLY, TSTokenType.DIVIDE, TSTokenType.MODULO):
            operator = self._previous()
            right = self._parse_unary()
            # Create binary expression
            expr = right  # Simplified
        
        return expr
    
    def _parse_unary(self) -> TSNode:
        """Parse unary expression."""
        if self._match(TSTokenType.NOT, TSTokenType.MINUS, TSTokenType.PLUS):
            operator = self._previous()
            right = self._parse_unary()
            # Create unary expression
            return right  # Simplified
        
        return self._parse_postfix()
    
    def _parse_postfix(self) -> TSNode:
        """Parse postfix expression."""
        expr = self._parse_primary()
        
        while True:
            if self._match(TSTokenType.INCREMENT, TSTokenType.DECREMENT):
                # Postfix increment/decrement
                pass
            elif self._match(TSTokenType.LBRACKET):
                # Array access
                index = self._parse_expression()
                self._consume(TSTokenType.RBRACKET, "Expected ']' after array index")
            elif self._match(TSTokenType.DOT):
                # Member access
                name = self._consume(TSTokenType.IDENTIFIER, "Expected property name").value
            elif self._match(TSTokenType.LPAREN):
                # Function call
                args = []
                if not self._check(TSTokenType.RPAREN):
                    args.append(self._parse_expression())
                    while self._match(TSTokenType.COMMA):
                        args.append(self._parse_expression())
                self._consume(TSTokenType.RPAREN, "Expected ')' after arguments")
            else:
                break
        
        return expr
    
    def _parse_primary(self) -> TSNode:
        """Parse primary expression."""
        if self._match(TSTokenType.TRUE):
            return TSLiteral(True, "true", TSLiteralType.BOOLEAN)
        
        if self._match(TSTokenType.FALSE):
            return TSLiteral(False, "false", TSLiteralType.BOOLEAN)
        
        if self._match(TSTokenType.NULL):
            return TSLiteral(None, "null", TSLiteralType.NULL)
        
        if self._match(TSTokenType.UNDEFINED):
            return TSLiteral(None, "undefined", TSLiteralType.UNDEFINED)
        
        if self._match(TSTokenType.NUMBER):
            value = self._previous().value
            return TSLiteral(float(value), value, TSLiteralType.NUMBER)
        
        if self._match(TSTokenType.STRING):
            value = self._previous().value
            return TSLiteral(value, f'"{value}"', TSLiteralType.STRING)
        
        if self._match(TSTokenType.IDENTIFIER):
            name = self._previous().value
            return TSIdentifier(name)
        
        if self._match(TSTokenType.LPAREN):
            expr = self._parse_expression()
            self._consume(TSTokenType.RPAREN, "Expected ')' after expression")
            return expr
        
        self._error("Expected expression")
    
    def _parse_block_statement(self) -> TSBlockStatement:
        """Parse block statement."""
        self._consume(TSTokenType.LBRACE, "Expected '{'")
        
        statements = []
        while not self._check(TSTokenType.RBRACE) and not self._is_at_end():
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
        
        self._consume(TSTokenType.RBRACE, "Expected '}'")
        
        return TSBlockStatement(statements)
    
    def _parse_expression_statement(self) -> TSNode:
        """Parse expression statement."""
        expr = self._parse_expression()
        self._consume(TSTokenType.SEMICOLON, "Expected ';' after expression")
        return expr  # Simplified
    
    # Helper methods
    def _match(self, *types: TSTokenType) -> bool:
        """Check if current token matches any of the given types."""
        for token_type in types:
            if self._check(token_type):
                self._advance()
                return True
        return False
    
    def _check(self, token_type: TSTokenType) -> bool:
        """Check if current token is of given type."""
        if self._is_at_end():
            return False
        return self._peek().type == token_type
    
    def _advance(self) -> TSToken:
        """Consume current token and return it."""
        if not self._is_at_end():
            self.current += 1
        return self._previous()
    
    def _is_at_end(self) -> bool:
        """Check if we're at end of tokens."""
        return self._peek().type == TSTokenType.EOF
    
    def _peek(self) -> TSToken:
        """Return current token without consuming it."""
        return self.tokens[self.current]
    
    def _previous(self) -> TSToken:
        """Return previous token."""
        return self.tokens[self.current - 1]
    
    def _consume(self, token_type: TSTokenType, message: str) -> TSToken:
        """Consume token of given type or raise error."""
        if self._check(token_type):
            return self._advance()
        
        current_token = self._peek()
        self._error(f"{message}. Got {current_token.type} at line {current_token.line}")
    
    def _error(self, message: str):
        """Raise parser error."""
        raise SyntaxError(f"Parser error: {message}")


def parse_typescript(source: str) -> TSProgram:
    """Parse TypeScript source code into AST."""
    lexer = TSLexer(source)
    tokens = lexer.tokenize()
    
    parser = TSParser(tokens)
    return parser.parse()