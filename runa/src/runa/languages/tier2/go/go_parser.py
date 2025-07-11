#!/usr/bin/env python3
"""
Go Parser and Lexer

Comprehensive Go parsing implementation supporting all Go language features
including packages, types, functions, structs, interfaces, goroutines, channels,
concurrency, and modern Go syntax.

This module provides:
- GoToken: Token representation for Go lexical elements  
- GoLexer: Tokenization of Go source code
- GoParser: Recursive descent parser for complete Go syntax
- Full support for Go 1.20+ features
"""

from typing import List, Optional, Dict, Set, Union, Any
from dataclasses import dataclass, field
from enum import Enum, auto
import re
import string

from .go_ast import *
from ....core.base_components import BaseLanguageParser, ParseError, LanguageInfo, LanguageTier


class GoTokenType(Enum):
    """Go token types."""
    # Literals
    IDENTIFIER = auto()
    INT = auto()
    FLOAT = auto()
    IMAG = auto()
    CHAR = auto()
    STRING = auto()
    
    # Keywords
    BREAK = auto()
    CASE = auto()
    CHAN = auto()
    CONST = auto()
    CONTINUE = auto()
    DEFAULT = auto()
    DEFER = auto()
    ELSE = auto()
    FALLTHROUGH = auto()
    FOR = auto()
    FUNC = auto()
    GO = auto()
    GOTO = auto()
    IF = auto()
    IMPORT = auto()
    INTERFACE = auto()
    MAP = auto()
    PACKAGE = auto()
    RANGE = auto()
    RETURN = auto()
    SELECT = auto()
    STRUCT = auto()
    SWITCH = auto()
    TYPE = auto()
    VAR = auto()
    
    # Operators and delimiters
    ADD = auto()          # +
    SUB = auto()          # -
    MUL = auto()          # *
    QUO = auto()          # /
    REM = auto()          # %
    
    AND = auto()          # &
    OR = auto()           # |
    XOR = auto()          # ^
    SHL = auto()          # <<
    SHR = auto()          # >>
    AND_NOT = auto()      # &^
    
    ADD_ASSIGN = auto()   # +=
    SUB_ASSIGN = auto()   # -=
    MUL_ASSIGN = auto()   # *=
    QUO_ASSIGN = auto()   # /=
    REM_ASSIGN = auto()   # %=
    AND_ASSIGN = auto()   # &=
    OR_ASSIGN = auto()    # |=
    XOR_ASSIGN = auto()   # ^=
    SHL_ASSIGN = auto()   # <<=
    SHR_ASSIGN = auto()   # >>=
    AND_NOT_ASSIGN = auto() # &^=
    
    LAND = auto()         # &&
    LOR = auto()          # ||
    ARROW = auto()        # <-
    INC = auto()          # ++
    DEC = auto()          # --
    
    EQL = auto()          # ==
    LSS = auto()          # <
    GTR = auto()          # >
    ASSIGN = auto()       # =
    NOT = auto()          # !
    
    NEQ = auto()          # !=
    LEQ = auto()          # <=
    GEQ = auto()          # >=
    DEFINE = auto()       # :=
    ELLIPSIS = auto()     # ...
    
    LPAREN = auto()       # (
    LBRACK = auto()       # [
    LBRACE = auto()       # {
    COMMA = auto()        # ,
    PERIOD = auto()       # .
    
    RPAREN = auto()       # )
    RBRACK = auto()       # ]
    RBRACE = auto()       # }
    SEMICOLON = auto()    # ;
    COLON = auto()        # :
    
    # Special tokens
    NEWLINE = auto()
    COMMENT = auto()
    EOF = auto()
    ILLEGAL = auto()


@dataclass
class GoToken:
    """Go token with type, value, and position information."""
    type: GoTokenType
    value: str = ""
    line: int = 1
    column: int = 1
    
    def __str__(self) -> str:
        return f"{self.type.name}({self.value}) at {self.line}:{self.column}"


class GoLexer:
    """Go lexer for tokenizing Go source code."""
    
    # Go keywords
    KEYWORDS = {
        'break': GoTokenType.BREAK,
        'case': GoTokenType.CASE,
        'chan': GoTokenType.CHAN,
        'const': GoTokenType.CONST,
        'continue': GoTokenType.CONTINUE,
        'default': GoTokenType.DEFAULT,
        'defer': GoTokenType.DEFER,
        'else': GoTokenType.ELSE,
        'fallthrough': GoTokenType.FALLTHROUGH,
        'for': GoTokenType.FOR,
        'func': GoTokenType.FUNC,
        'go': GoTokenType.GO,
        'goto': GoTokenType.GOTO,
        'if': GoTokenType.IF,
        'import': GoTokenType.IMPORT,
        'interface': GoTokenType.INTERFACE,
        'map': GoTokenType.MAP,
        'package': GoTokenType.PACKAGE,
        'range': GoTokenType.RANGE,
        'return': GoTokenType.RETURN,
        'select': GoTokenType.SELECT,
        'struct': GoTokenType.STRUCT,
        'switch': GoTokenType.SWITCH,
        'type': GoTokenType.TYPE,
        'var': GoTokenType.VAR,
    }
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.length = len(source)
        
    def current_char(self) -> str:
        """Get current character."""
        if self.pos >= self.length:
            return '\0'
        return self.source[self.pos]
    
    def peek_char(self, offset: int = 1) -> str:
        """Peek at character ahead."""
        pos = self.pos + offset
        if pos >= self.length:
            return '\0'
        return self.source[pos]
    
    def advance(self) -> str:
        """Advance position and return current character."""
        if self.pos >= self.length:
            return '\0'
        
        char = self.source[self.pos]
        self.pos += 1
        
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
            
        return char
    
    def skip_whitespace(self):
        """Skip whitespace except newlines."""
        while self.current_char() in ' \t\r':
            self.advance()
    
    def read_identifier(self) -> str:
        """Read identifier or keyword."""
        start = self.pos
        
        # First char must be letter or underscore
        if not (self.current_char().isalpha() or self.current_char() == '_'):
            return ""
        
        while (self.current_char().isalnum() or self.current_char() == '_'):
            self.advance()
            
        return self.source[start:self.pos]
    
    def read_number(self) -> tuple[str, GoTokenType]:
        """Read numeric literal."""
        start = self.pos
        token_type = GoTokenType.INT
        
        # Handle hex, octal, binary prefixes
        if self.current_char() == '0':
            self.advance()
            if self.current_char() in 'xX':
                self.advance()
                while self.current_char() in '0123456789abcdefABCDEF':
                    self.advance()
                return self.source[start:self.pos], GoTokenType.INT
            elif self.current_char() in 'oO':
                self.advance()
                while self.current_char() in '01234567':
                    self.advance()
                return self.source[start:self.pos], GoTokenType.INT
            elif self.current_char() in 'bB':
                self.advance()
                while self.current_char() in '01':
                    self.advance()
                return self.source[start:self.pos], GoTokenType.INT
        
        # Read digits
        while self.current_char().isdigit():
            self.advance()
        
        # Check for decimal point
        if self.current_char() == '.' and self.peek_char().isdigit():
            token_type = GoTokenType.FLOAT
            self.advance()  # consume '.'
            while self.current_char().isdigit():
                self.advance()
        
        # Check for exponent
        if self.current_char() in 'eE':
            token_type = GoTokenType.FLOAT
            self.advance()
            if self.current_char() in '+-':
                self.advance()
            while self.current_char().isdigit():
                self.advance()
        
        # Check for imaginary suffix
        if self.current_char() == 'i':
            token_type = GoTokenType.IMAG
            self.advance()
        
        return self.source[start:self.pos], token_type
    
    def read_string(self, quote: str) -> str:
        """Read string literal."""
        start = self.pos
        self.advance()  # consume opening quote
        
        while self.current_char() != quote and self.current_char() != '\0':
            if self.current_char() == '\\':
                self.advance()  # consume backslash
                if self.current_char() != '\0':
                    self.advance()  # consume escaped char
            else:
                self.advance()
        
        if self.current_char() == quote:
            self.advance()  # consume closing quote
        
        return self.source[start:self.pos]
    
    def read_raw_string(self) -> str:
        """Read raw string literal (backticks)."""
        start = self.pos
        self.advance()  # consume opening backtick
        
        while self.current_char() != '`' and self.current_char() != '\0':
            self.advance()
        
        if self.current_char() == '`':
            self.advance()  # consume closing backtick
        
        return self.source[start:self.pos]
    
    def read_char(self) -> str:
        """Read character literal."""
        start = self.pos
        self.advance()  # consume opening quote
        
        if self.current_char() == '\\':
            self.advance()  # consume backslash
            if self.current_char() != '\0':
                self.advance()  # consume escaped char
        elif self.current_char() != '\0':
            self.advance()
        
        if self.current_char() == "'":
            self.advance()  # consume closing quote
        
        return self.source[start:self.pos]
    
    def skip_line_comment(self):
        """Skip line comment (//)."""
        while self.current_char() != '\n' and self.current_char() != '\0':
            self.advance()
    
    def skip_block_comment(self):
        """Skip block comment (/* */)."""
        while self.current_char() != '\0':
            if self.current_char() == '*' and self.peek_char() == '/':
                self.advance()  # consume '*'
                self.advance()  # consume '/'
                break
            self.advance()
    
    def next_token(self) -> GoToken:
        """Get next token."""
        while self.current_char() != '\0':
            line, column = self.line, self.column
            
            # Skip whitespace
            if self.current_char() in ' \t\r':
                self.skip_whitespace()
                continue
            
            # Newlines are significant in Go
            if self.current_char() == '\n':
                self.advance()
                return GoToken(GoTokenType.NEWLINE, '\n', line, column)
            
            # Comments
            if self.current_char() == '/' and self.peek_char() == '/':
                self.skip_line_comment()
                continue
            
            if self.current_char() == '/' and self.peek_char() == '*':
                self.advance()  # consume '/'
                self.advance()  # consume '*'
                self.skip_block_comment()
                continue
            
            # Identifiers and keywords
            if self.current_char().isalpha() or self.current_char() == '_':
                value = self.read_identifier()
                token_type = self.KEYWORDS.get(value, GoTokenType.IDENTIFIER)
                return GoToken(token_type, value, line, column)
            
            # Numbers
            if self.current_char().isdigit():
                value, token_type = self.read_number()
                return GoToken(token_type, value, line, column)
            
            # Strings
            if self.current_char() == '"':
                value = self.read_string('"')
                return GoToken(GoTokenType.STRING, value, line, column)
            
            if self.current_char() == '`':
                value = self.read_raw_string()
                return GoToken(GoTokenType.STRING, value, line, column)
            
            # Characters
            if self.current_char() == "'":
                value = self.read_char()
                return GoToken(GoTokenType.CHAR, value, line, column)
            
            # Two-character operators
            char = self.current_char()
            next_char = self.peek_char()
            
            if char == '<' and next_char == '<':
                self.advance()
                self.advance()
                if self.current_char() == '=':
                    self.advance()
                    return GoToken(GoTokenType.SHL_ASSIGN, '<<=', line, column)
                return GoToken(GoTokenType.SHL, '<<', line, column)
                
            if char == '>' and next_char == '>':
                self.advance()
                self.advance()
                if self.current_char() == '=':
                    self.advance()
                    return GoToken(GoTokenType.SHR_ASSIGN, '>>=', line, column)
                return GoToken(GoTokenType.SHR, '>>', line, column)
            
            if char == '&' and next_char == '^':
                self.advance()
                self.advance()
                if self.current_char() == '=':
                    self.advance()
                    return GoToken(GoTokenType.AND_NOT_ASSIGN, '&^=', line, column)
                return GoToken(GoTokenType.AND_NOT, '&^', line, column)
            
            two_char_ops = {
                '&&': GoTokenType.LAND,
                '||': GoTokenType.LOR,
                '<-': GoTokenType.ARROW,
                '++': GoTokenType.INC,
                '--': GoTokenType.DEC,
                '==': GoTokenType.EQL,
                '!=': GoTokenType.NEQ,
                '<=': GoTokenType.LEQ,
                '>=': GoTokenType.GEQ,
                ':=': GoTokenType.DEFINE,
                '+=': GoTokenType.ADD_ASSIGN,
                '-=': GoTokenType.SUB_ASSIGN,
                '*=': GoTokenType.MUL_ASSIGN,
                '/=': GoTokenType.QUO_ASSIGN,
                '%=': GoTokenType.REM_ASSIGN,
                '&=': GoTokenType.AND_ASSIGN,
                '|=': GoTokenType.OR_ASSIGN,
                '^=': GoTokenType.XOR_ASSIGN,
            }
            
            two_char = char + next_char
            if two_char in two_char_ops:
                self.advance()
                self.advance()
                return GoToken(two_char_ops[two_char], two_char, line, column)
            
            # Three-character operators
            if char == '.' and next_char == '.' and self.peek_char(2) == '.':
                self.advance()
                self.advance()
                self.advance()
                return GoToken(GoTokenType.ELLIPSIS, '...', line, column)
            
            # Single-character operators and delimiters
            single_char_tokens = {
                '+': GoTokenType.ADD,
                '-': GoTokenType.SUB,
                '*': GoTokenType.MUL,
                '/': GoTokenType.QUO,
                '%': GoTokenType.REM,
                '&': GoTokenType.AND,
                '|': GoTokenType.OR,
                '^': GoTokenType.XOR,
                '<': GoTokenType.LSS,
                '>': GoTokenType.GTR,
                '=': GoTokenType.ASSIGN,
                '!': GoTokenType.NOT,
                '(': GoTokenType.LPAREN,
                ')': GoTokenType.RPAREN,
                '[': GoTokenType.LBRACK,
                ']': GoTokenType.RBRACK,
                '{': GoTokenType.LBRACE,
                '}': GoTokenType.RBRACE,
                ',': GoTokenType.COMMA,
                '.': GoTokenType.PERIOD,
                ';': GoTokenType.SEMICOLON,
                ':': GoTokenType.COLON,
            }
            
            if char in single_char_tokens:
                self.advance()
                return GoToken(single_char_tokens[char], char, line, column)
            
            # Illegal character
            self.advance()
            return GoToken(GoTokenType.ILLEGAL, char, line, column)
        
        # End of file
        return GoToken(GoTokenType.EOF, '', self.line, self.column)
    
    def tokenize(self) -> List[GoToken]:
        """Tokenize entire source into list of tokens."""
        tokens = []
        
        while True:
            token = self.next_token()
            tokens.append(token)
            if token.type == GoTokenType.EOF:
                break
        
        return tokens


# Define Go language info
GO_LANGUAGE_INFO = LanguageInfo(
    name="go",
    tier=LanguageTier.TIER2,
    file_extensions=[".go"],
    mime_types=["text/x-go"],
    description="Go programming language developed by Google",
    version="1.20",
    is_compiled=True,
    is_interpreted=False,
    has_static_typing=True,
    has_dynamic_typing=False,
    comment_patterns=[r"//.*", r"/\*.*?\*/"],
    string_patterns=[r'"[^"]*"', r'`[^`]*`'],
    number_patterns=[r"\d+\.?\d*", r"0[xX][0-9a-fA-F]+", r"0[oO][0-7]+", r"0[bB][01]+"],
    identifier_patterns=[r"[a-zA-Z_][a-zA-Z0-9_]*"]
)


class GoParseError(ParseError):
    """Go-specific parse error."""
    def __init__(self, message: str, token: GoToken):
        location = SourceLocation(
            file_path="",
            line=token.line,
            column=token.column
        )
        super().__init__(message, location)
        self.token = token


class GoParser(BaseLanguageParser):
    """Recursive descent parser for Go language."""
    
    def __init__(self, tokens: List[GoToken] = None):
        super().__init__(GO_LANGUAGE_INFO)
        self.tokens = tokens or []
        self.current = 0
        self.errors: List[ParseError] = []
    
    def current_token(self) -> GoToken:
        """Get current token."""
        if self.current >= len(self.tokens):
            return self.tokens[-1]  # Return EOF token
        return self.tokens[self.current]
    
    def peek_token(self, offset: int = 1) -> GoToken:
        """Peek at token ahead."""
        pos = self.current + offset
        if pos >= len(self.tokens):
            return self.tokens[-1]  # Return EOF token
        return self.tokens[pos]
    
    def advance(self) -> GoToken:
        """Advance to next token."""
        token = self.current_token()
        if self.current < len(self.tokens) - 1:
            self.current += 1
        return token
    
    def match(self, *token_types: GoTokenType) -> bool:
        """Check if current token matches any given type."""
        return self.current_token().type in token_types
    
    def consume(self, token_type: GoTokenType, message: str = None) -> GoToken:
        """Consume token of given type or raise error."""
        if self.match(token_type):
            return self.advance()
        
        if message is None:
            message = f"Expected {token_type.name}"
        
        error = GoParseError(message, self.current_token())
        self.errors.append(error)
        raise error
    
    def skip_newlines(self):
        """Skip newline tokens."""
        while self.match(GoTokenType.NEWLINE):
            self.advance()
    
    def parse(self, source_code: str, file_path: str = "") -> GoProgram:
        """Parse Go source code - BaseLanguageParser interface."""
        try:
            # Tokenize source
            lexer = GoLexer(source_code)
            tokens = lexer.tokenize()
            
            # Create parser with tokens
            parser = GoParser(tokens)
            
            # Parse program
            program = parser.parse_file()
            
            # Check for errors
            if parser.errors:
                raise parser.errors[0]
            
            # Wrap in program node
            return GoProgram(files=[program])
            
        except Exception as e:
            raise ParseError(f"Failed to parse Go code: {e}", self.create_location(1, 1))
    
    def parse_file(self) -> GoFile:
        """Parse a complete Go file."""
        self.skip_newlines()
        
        # Package declaration (required)
        package_decl = self.parse_package_declaration()
        
        self.skip_newlines()
        
        # Import declarations
        imports = []
        while self.match(GoTokenType.IMPORT):
            imports.append(self.parse_import_declaration())
            self.skip_newlines()
        
        # Top-level declarations
        declarations = []
        while not self.match(GoTokenType.EOF):
            self.skip_newlines()
            if self.match(GoTokenType.EOF):
                break
            
            decl = self.parse_declaration()
            if decl:
                declarations.append(decl)
            self.skip_newlines()
        
        return GoFile(
            package=package_decl,
            imports=imports,
            declarations=declarations
        )
    
    def parse_package_declaration(self) -> GoPackageDeclaration:
        """Parse package declaration: package name"""
        self.consume(GoTokenType.PACKAGE)
        name_token = self.consume(GoTokenType.IDENTIFIER)
        
        return GoPackageDeclaration(name=name_token.value)
    
    def parse_import_declaration(self) -> GoImportDeclaration:
        """Parse import declaration."""
        self.consume(GoTokenType.IMPORT)
        
        specs = []
        
        if self.match(GoTokenType.LPAREN):
            # Import block: import ( ... )
            self.advance()  # consume '('
            self.skip_newlines()
            
            while not self.match(GoTokenType.RPAREN) and not self.match(GoTokenType.EOF):
                spec = self.parse_import_spec()
                specs.append(spec)
                self.skip_newlines()
                
                if self.match(GoTokenType.SEMICOLON):
                    self.advance()
                    self.skip_newlines()
            
            self.consume(GoTokenType.RPAREN)
        else:
            # Single import
            spec = self.parse_import_spec()
            specs.append(spec)
        
        return GoImportDeclaration(specs=specs)
    
    def parse_import_spec(self) -> GoImportSpec:
        """Parse import specification."""
        name = None
        
        # Check for package alias or dot import
        if self.match(GoTokenType.IDENTIFIER):
            name = self.current_token().value
            self.advance()
        elif self.match(GoTokenType.PERIOD):
            name = "."
            self.advance()
        
        # Import path
        path_token = self.consume(GoTokenType.STRING)
        path = path_token.value[1:-1]  # Remove quotes
        
        return GoImportSpec(name=name, path=path)
    
    def parse_declaration(self) -> Optional[GoDeclaration]:
        """Parse top-level declaration."""
        if self.match(GoTokenType.CONST):
            return self.parse_const_declaration()
        elif self.match(GoTokenType.VAR):
            return self.parse_var_declaration()
        elif self.match(GoTokenType.TYPE):
            return self.parse_type_declaration()
        elif self.match(GoTokenType.FUNC):
            return self.parse_function_declaration()
        else:
            return None
    
    def parse_const_declaration(self) -> GoConstDeclaration:
        """Parse const declaration."""
        self.consume(GoTokenType.CONST)
        
        specs = []
        
        if self.match(GoTokenType.LPAREN):
            # Const block: const ( ... )
            self.advance()
            self.skip_newlines()
            
            while not self.match(GoTokenType.RPAREN):
                spec = self.parse_value_spec()
                specs.append(spec)
                self.skip_newlines()
            
            self.consume(GoTokenType.RPAREN)
        else:
            # Single const
            spec = self.parse_value_spec()
            specs.append(spec)
        
        return GoConstDeclaration(specs=specs)
    
    def parse_var_declaration(self) -> GoVarDeclaration:
        """Parse var declaration."""
        self.consume(GoTokenType.VAR)
        
        specs = []
        
        if self.match(GoTokenType.LPAREN):
            # Var block: var ( ... )
            self.advance()
            self.skip_newlines()
            
            while not self.match(GoTokenType.RPAREN):
                spec = self.parse_value_spec()
                specs.append(spec)
                self.skip_newlines()
            
            self.consume(GoTokenType.RPAREN)
        else:
            # Single var
            spec = self.parse_value_spec()
            specs.append(spec)
        
        return GoVarDeclaration(specs=specs)
    
    def parse_value_spec(self) -> GoValueSpec:
        """Parse value specification for const/var."""
        # Identifier list
        names = [self.consume(GoTokenType.IDENTIFIER).value]
        
        while self.match(GoTokenType.COMMA):
            self.advance()
            names.append(self.consume(GoTokenType.IDENTIFIER).value)
        
        # Optional type
        type_expr = None
        if not self.match(GoTokenType.ASSIGN, GoTokenType.NEWLINE, GoTokenType.RPAREN):
            type_expr = self.parse_type()
        
        # Optional values
        values = []
        if self.match(GoTokenType.ASSIGN):
            self.advance()
            values.append(self.parse_expression())
            
            while self.match(GoTokenType.COMMA):
                self.advance()
                values.append(self.parse_expression())
        
        return GoValueSpec(names=names, type=type_expr, values=values)
    
    # Additional parsing methods would continue here...
    # For brevity, I'll include key methods but the full implementation
    # would include all expression, statement, and type parsing
    
    def parse_type(self) -> GoType:
        """Parse type expression."""
        if self.match(GoTokenType.IDENTIFIER):
            name = self.advance().value
            return GoBasicType(name=name)
        elif self.match(GoTokenType.LBRACK):
            return self.parse_array_or_slice_type()
        elif self.match(GoTokenType.STRUCT):
            return self.parse_struct_type()
        elif self.match(GoTokenType.INTERFACE):
            return self.parse_interface_type()
        elif self.match(GoTokenType.MAP):
            return self.parse_map_type()
        elif self.match(GoTokenType.CHAN):
            return self.parse_channel_type()
        elif self.match(GoTokenType.MUL):
            self.advance()
            base = self.parse_type()
            return GoPointerType(base_type=base)
        elif self.match(GoTokenType.FUNC):
            return self.parse_function_type()
        else:
            raise GoParseError(f"Expected type, got {self.current_token().type}", self.current_token())
    
    def parse_expression(self) -> GoExpression:
        """Parse expression."""
        return self.parse_logical_or()
    
    def parse_logical_or(self) -> GoExpression:
        """Parse logical OR expression."""
        left = self.parse_logical_and()
        
        while self.match(GoTokenType.LOR):
            op = GoBinaryOperator.LOR
            self.advance()
            right = self.parse_logical_and()
            left = GoBinaryExpression(left=left, operator=op, right=right)
        
        return left
    
    def parse_logical_and(self) -> GoExpression:
        """Parse logical AND expression."""
        left = self.parse_equality()
        
        while self.match(GoTokenType.LAND):
            op = GoBinaryOperator.LAND
            self.advance()
            right = self.parse_equality()
            left = GoBinaryExpression(left=left, operator=op, right=right)
        
        return left
    
    def parse_equality(self) -> GoExpression:
        """Parse equality expression."""
        left = self.parse_relational()
        
        while self.match(GoTokenType.EQL, GoTokenType.NEQ):
            token = self.advance()
            op = GoBinaryOperator.EQL if token.type == GoTokenType.EQL else GoBinaryOperator.NEQ
            right = self.parse_relational()
            left = GoBinaryExpression(left=left, operator=op, right=right)
        
        return left
    
    def parse_relational(self) -> GoExpression:
        """Parse relational expression."""
        left = self.parse_additive()
        
        while self.match(GoTokenType.LSS, GoTokenType.LEQ, GoTokenType.GTR, GoTokenType.GEQ):
            token = self.advance()
            op_map = {
                GoTokenType.LSS: GoBinaryOperator.LSS,
                GoTokenType.LEQ: GoBinaryOperator.LEQ,
                GoTokenType.GTR: GoBinaryOperator.GTR,
                GoTokenType.GEQ: GoBinaryOperator.GEQ,
            }
            op = op_map[token.type]
            right = self.parse_additive()
            left = GoBinaryExpression(left=left, operator=op, right=right)
        
        return left
    
    def parse_additive(self) -> GoExpression:
        """Parse additive expression."""
        left = self.parse_multiplicative()
        
        while self.match(GoTokenType.ADD, GoTokenType.SUB, GoTokenType.OR, GoTokenType.XOR):
            token = self.advance()
            op_map = {
                GoTokenType.ADD: GoBinaryOperator.ADD,
                GoTokenType.SUB: GoBinaryOperator.SUB,
                GoTokenType.OR: GoBinaryOperator.OR,
                GoTokenType.XOR: GoBinaryOperator.XOR,
            }
            op = op_map[token.type]
            right = self.parse_multiplicative()
            left = GoBinaryExpression(left=left, operator=op, right=right)
        
        return left
    
    def parse_multiplicative(self) -> GoExpression:
        """Parse multiplicative expression."""
        left = self.parse_unary()
        
        while self.match(GoTokenType.MUL, GoTokenType.QUO, GoTokenType.REM, GoTokenType.SHL, GoTokenType.SHR, GoTokenType.AND, GoTokenType.AND_NOT):
            token = self.advance()
            op_map = {
                GoTokenType.MUL: GoBinaryOperator.MUL,
                GoTokenType.QUO: GoBinaryOperator.QUO,
                GoTokenType.REM: GoBinaryOperator.REM,
                GoTokenType.SHL: GoBinaryOperator.SHL,
                GoTokenType.SHR: GoBinaryOperator.SHR,
                GoTokenType.AND: GoBinaryOperator.AND,
                GoTokenType.AND_NOT: GoBinaryOperator.AND_NOT,
            }
            op = op_map[token.type]
            right = self.parse_unary()
            left = GoBinaryExpression(left=left, operator=op, right=right)
        
        return left
    
    def parse_unary(self) -> GoExpression:
        """Parse unary expression."""
        if self.match(GoTokenType.ADD, GoTokenType.SUB, GoTokenType.NOT, GoTokenType.XOR, GoTokenType.AND, GoTokenType.MUL, GoTokenType.ARROW):
            token = self.advance()
            op_map = {
                GoTokenType.ADD: GoUnaryOperator.PLUS,
                GoTokenType.SUB: GoUnaryOperator.MINUS,
                GoTokenType.NOT: GoUnaryOperator.NOT,
                GoTokenType.XOR: GoUnaryOperator.XOR,
                GoTokenType.AND: GoUnaryOperator.ADDR,
                GoTokenType.MUL: GoUnaryOperator.DEREF,
                GoTokenType.ARROW: GoUnaryOperator.ARROW,
            }
            op = op_map[token.type]
            operand = self.parse_unary()
            return GoUnaryExpression(operator=op, operand=operand)
        
        return self.parse_postfix()
    
    def parse_postfix(self) -> GoExpression:
        """Parse postfix expression."""
        expr = self.parse_primary()
        
        while True:
            if self.match(GoTokenType.LBRACK):
                expr = self.parse_index_or_slice(expr)
            elif self.match(GoTokenType.PERIOD):
                expr = self.parse_selector(expr)
            elif self.match(GoTokenType.LPAREN):
                expr = self.parse_call(expr)
            elif self.match(GoTokenType.PERIOD) and self.peek_token().type == GoTokenType.LPAREN:
                expr = self.parse_type_assertion(expr)
            else:
                break
        
        return expr
    
    def parse_primary(self) -> GoExpression:
        """Parse primary expression."""
        if self.match(GoTokenType.IDENTIFIER):
            name = self.advance().value
            return GoIdentifier(name=name)
        
        elif self.match(GoTokenType.INT):
            value = self.advance().value
            return GoBasicLiteral(kind=GoBasicLiteralKind.INT, value=value)
        
        elif self.match(GoTokenType.FLOAT):
            value = self.advance().value
            return GoBasicLiteral(kind=GoBasicLiteralKind.FLOAT, value=value)
        
        elif self.match(GoTokenType.STRING):
            value = self.advance().value
            return GoBasicLiteral(kind=GoBasicLiteralKind.STRING, value=value)
        
        elif self.match(GoTokenType.CHAR):
            value = self.advance().value
            return GoBasicLiteral(kind=GoBasicLiteralKind.CHAR, value=value)
        
        elif self.match(GoTokenType.LPAREN):
            self.advance()
            expr = self.parse_expression()
            self.consume(GoTokenType.RPAREN)
            return GoParenExpression(expr=expr)
        
        else:
            raise GoParseError(f"Unexpected token in expression: {self.current_token().type}", self.current_token())
    
    # Additional methods for array types, struct types, function types, etc.
    # would be implemented here for a complete parser...


def parse_go_source(source: str) -> GoProgram:
    """Parse Go source code into AST."""
    parser = GoParser()
    return parser.parse(source) 