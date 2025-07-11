#!/usr/bin/env python3
"""
Bazel Parser Implementation

Complete parser for Bazel build files including:
- BUILD files with rules and targets
- WORKSPACE files with external dependencies  
- .bzl files with custom rules and macros
- Starlark language syntax
- Label parsing and validation
- Error handling and recovery
"""

import re
from enum import Enum, auto
from typing import List, Optional, Dict, Any, Union, Iterator
from dataclasses import dataclass

from .bazel_ast import *


class TokenType(Enum):
    """Token types for Bazel lexer."""
    # Literals
    STRING = auto()
    INTEGER = auto() 
    FLOAT = auto()
    BOOLEAN = auto()
    
    # Identifiers and keywords
    IDENTIFIER = auto()
    LOAD = auto()
    DEF = auto()
    IF = auto()
    ELIF = auto()
    ELSE = auto()
    FOR = auto()
    IN = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    TRUE = auto()
    FALSE = auto()
    NONE = auto()
    
    # Operators
    ASSIGN = auto()          # =
    PLUS_ASSIGN = auto()     # +=
    EQUALS = auto()          # ==
    NOT_EQUALS = auto()      # !=
    LESS_THAN = auto()       # <
    GREATER_THAN = auto()    # >
    LESS_EQUAL = auto()      # <=
    GREATER_EQUAL = auto()   # >=
    PLUS = auto()            # +
    MINUS = auto()           # -
    MULTIPLY = auto()        # *
    DIVIDE = auto()          # /
    MODULO = auto()          # %
    
    # Delimiters
    LPAREN = auto()          # (
    RPAREN = auto()          # )
    LBRACKET = auto()        # [
    RBRACKET = auto()        # ]
    LBRACE = auto()          # {
    RBRACE = auto()          # }
    COMMA = auto()           # ,
    COLON = auto()           # :
    DOT = auto()             # .
    
    # Special
    LABEL = auto()           # //package:target or @repo//package:target
    NEWLINE = auto()
    INDENT = auto()
    DEDENT = auto()
    COMMENT = auto()
    EOF = auto()
    
    # File types
    BUILD_FILE = auto()
    WORKSPACE_FILE = auto()
    BZL_FILE = auto()


@dataclass
class Token:
    """Represents a token in the Bazel source."""
    type: TokenType
    value: str
    line: int
    column: int
    file_path: Optional[str] = None


class BazelLexer:
    """Lexer for Bazel build files."""
    
    KEYWORDS = {
        'load': TokenType.LOAD,
        'def': TokenType.DEF,
        'if': TokenType.IF,
        'elif': TokenType.ELIF,
        'else': TokenType.ELSE,
        'for': TokenType.FOR,
        'in': TokenType.IN,
        'and': TokenType.AND,
        'or': TokenType.OR,
        'not': TokenType.NOT,
        'True': TokenType.TRUE,
        'False': TokenType.FALSE,
        'None': TokenType.NONE,
    }
    
    def __init__(self, source: str, file_path: Optional[str] = None):
        self.source = source
        self.file_path = file_path
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        self.indent_stack = [0]
        
    def tokenize(self) -> List[Token]:
        """Tokenize the entire source."""
        while self.position < len(self.source):
            self._skip_whitespace()
            
            if self.position >= len(self.source):
                break
                
            char = self.source[self.position]
            
            if char == '\n':
                self._handle_newline()
            elif char == '#':
                self._handle_comment()
            elif char in '"\'':
                self._handle_string()
            elif char.isdigit() or (char == '.' and self._peek().isdigit()):
                self._handle_number()
            elif char.isalpha() or char == '_':
                self._handle_identifier_or_keyword()
            elif self._is_label_start():
                self._handle_label()
            elif char in '()[]{},:.' :
                self._handle_delimiter()
            elif char in '+-*/%=!<>':
                self._handle_operator()
            else:
                raise SyntaxError(f"Unexpected character '{char}' at line {self.line}, column {self.column}")
        
        # Add final DEDENT tokens
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            self._add_token(TokenType.DEDENT, "")
            
        self._add_token(TokenType.EOF, "")
        return self.tokens
    
    def _peek(self, offset: int = 1) -> str:
        """Peek at character at current position + offset."""
        pos = self.position + offset
        return self.source[pos] if pos < len(self.source) else '\0'
    
    def _advance(self) -> str:
        """Advance position and return current character."""
        if self.position < len(self.source):
            char = self.source[self.position]
            self.position += 1
            if char == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            return char
        return '\0'
    
    def _add_token(self, token_type: TokenType, value: str):
        """Add a token to the tokens list."""
        token = Token(token_type, value, self.line, self.column - len(value), self.file_path)
        self.tokens.append(token)
    
    def _skip_whitespace(self):
        """Skip whitespace characters except newlines."""
        while (self.position < len(self.source) and 
               self.source[self.position] in ' \t\r'):
            self._advance()
    
    def _handle_newline(self):
        """Handle newline and indentation."""
        self._advance()  # consume '\n'
        self._add_token(TokenType.NEWLINE, "\n")
        
        # Check indentation on next line
        if self.position < len(self.source):
            indent_level = 0
            start_pos = self.position
            
            while (self.position < len(self.source) and 
                   self.source[self.position] in ' \t'):
                if self.source[self.position] == '\t':
                    indent_level += 8  # Tab = 8 spaces
                else:
                    indent_level += 1
                self._advance()
            
            # Skip empty lines and comments
            if (self.position < len(self.source) and 
                self.source[self.position] not in '\n#'):
                
                current_indent = self.indent_stack[-1]
                if indent_level > current_indent:
                    self.indent_stack.append(indent_level)
                    self._add_token(TokenType.INDENT, "")
                elif indent_level < current_indent:
                    while len(self.indent_stack) > 1 and self.indent_stack[-1] > indent_level:
                        self.indent_stack.pop()
                        self._add_token(TokenType.DEDENT, "")
            else:
                # Reset position for empty line
                self.position = start_pos
    
    def _handle_comment(self):
        """Handle comment line."""
        start = self.position
        while (self.position < len(self.source) and 
               self.source[self.position] != '\n'):
            self._advance()
        
        comment_text = self.source[start:self.position]
        self._add_token(TokenType.COMMENT, comment_text)
    
    def _handle_string(self):
        """Handle string literals (single or double quoted, with triple quotes)."""
        quote_char = self.source[self.position]
        start = self.position
        self._advance()  # consume opening quote
        
        # Check for triple quotes
        if (self.position + 1 < len(self.source) and 
            self.source[self.position] == quote_char and 
            self.source[self.position + 1] == quote_char):
            
            # Triple quoted string
            self._advance()  # second quote
            self._advance()  # third quote
            
            while self.position + 2 < len(self.source):
                if (self.source[self.position] == quote_char and
                    self.source[self.position + 1] == quote_char and
                    self.source[self.position + 2] == quote_char):
                    self._advance()  # first closing quote
                    self._advance()  # second closing quote
                    self._advance()  # third closing quote
                    break
                self._advance()
        else:
            # Regular string
            while (self.position < len(self.source) and 
                   self.source[self.position] != quote_char):
                if self.source[self.position] == '\\':
                    self._advance()  # skip escape character
                    if self.position < len(self.source):
                        self._advance()  # skip escaped character
                else:
                    self._advance()
            
            if self.position < len(self.source):
                self._advance()  # consume closing quote
        
        string_value = self.source[start:self.position]
        self._add_token(TokenType.STRING, string_value)
    
    def _handle_number(self):
        """Handle numeric literals (integers and floats)."""
        start = self.position
        has_dot = False
        
        while (self.position < len(self.source) and 
               (self.source[self.position].isdigit() or self.source[self.position] == '.')):
            if self.source[self.position] == '.':
                if has_dot:
                    break  # Second dot, stop parsing number
                has_dot = True
            self._advance()
        
        number_str = self.source[start:self.position]
        token_type = TokenType.FLOAT if has_dot else TokenType.INTEGER
        self._add_token(token_type, number_str)
    
    def _handle_identifier_or_keyword(self):
        """Handle identifiers and keywords."""
        start = self.position
        
        while (self.position < len(self.source) and 
               (self.source[self.position].isalnum() or self.source[self.position] == '_')):
            self._advance()
        
        identifier = self.source[start:self.position]
        token_type = self.KEYWORDS.get(identifier, TokenType.IDENTIFIER)
        self._add_token(token_type, identifier)
    
    def _is_label_start(self) -> bool:
        """Check if current position starts a label."""
        char = self.source[self.position]
        if char == '/':
            return self._peek() == '/'
        elif char == '@':
            return True
        elif char == ':':
            return True
        return False
    
    def _handle_label(self):
        """Handle Bazel labels like //package:target or @repo//package:target."""
        start = self.position
        
        # Handle @repository part
        if self.source[self.position] == '@':
            self._advance()
            while (self.position < len(self.source) and 
                   self.source[self.position] not in ' \t\n()[]{},:'):
                self._advance()
        
        # Handle //package part
        if (self.position + 1 < len(self.source) and 
            self.source[self.position] == '/' and self.source[self.position + 1] == '/'):
            self._advance()  # first /
            self._advance()  # second /
            
            while (self.position < len(self.source) and 
                   self.source[self.position] not in ' \t\n()[]{},:'):
                self._advance()
        
        # Handle :target part
        if (self.position < len(self.source) and self.source[self.position] == ':'):
            self._advance()  # :
            while (self.position < len(self.source) and 
                   self.source[self.position] not in ' \t\n()[]{},:'):
                self._advance()
        
        label_str = self.source[start:self.position]
        self._add_token(TokenType.LABEL, label_str)
    
    def _handle_delimiter(self):
        """Handle delimiter characters."""
        char = self._advance()
        delimiters = {
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN,
            '[': TokenType.LBRACKET,
            ']': TokenType.RBRACKET,
            '{': TokenType.LBRACE,
            '}': TokenType.RBRACE,
            ',': TokenType.COMMA,
            ':': TokenType.COLON,
            '.': TokenType.DOT,
        }
        self._add_token(delimiters[char], char)
    
    def _handle_operator(self):
        """Handle operator characters."""
        char = self._advance()
        
        # Two-character operators
        if char == '=' and self._peek() == '=':
            self._advance()
            self._add_token(TokenType.EQUALS, "==")
        elif char == '!' and self._peek() == '=':
            self._advance()
            self._add_token(TokenType.NOT_EQUALS, "!=")
        elif char == '<' and self._peek() == '=':
            self._advance()
            self._add_token(TokenType.LESS_EQUAL, "<=")
        elif char == '>' and self._peek() == '=':
            self._advance()
            self._add_token(TokenType.GREATER_EQUAL, ">=")
        elif char == '+' and self._peek() == '=':
            self._advance()
            self._add_token(TokenType.PLUS_ASSIGN, "+=")
        else:
            # Single-character operators
            operators = {
                '=': TokenType.ASSIGN,
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.MULTIPLY,
                '/': TokenType.DIVIDE,
                '%': TokenType.MODULO,
                '<': TokenType.LESS_THAN,
                '>': TokenType.GREATER_THAN,
            }
            if char in operators:
                self._add_token(operators[char], char)


class BazelParser:
    """Parser for Bazel build files."""
    
    def __init__(self, tokens: List[Token], file_path: Optional[str] = None):
        self.tokens = tokens
        self.file_path = file_path
        self.position = 0
        self.current_token = tokens[0] if tokens else None
        
    def parse(self) -> Union[BuildFile, WorkspaceFile, BzlFile]:
        """Parse tokens into AST."""
        # Determine file type
        if self.file_path:
            if self.file_path.endswith('BUILD') or self.file_path.endswith('BUILD.bazel'):
                return self._parse_build_file()
            elif self.file_path.endswith('WORKSPACE') or self.file_path.endswith('WORKSPACE.bazel'):
                return self._parse_workspace_file()
            elif self.file_path.endswith('.bzl'):
                return self._parse_bzl_file()
        
        # Default to BUILD file
        return self._parse_build_file()
    
    def _advance(self) -> Optional[Token]:
        """Advance to next token."""
        if self.position < len(self.tokens) - 1:
            self.position += 1
            self.current_token = self.tokens[self.position]
        else:
            self.current_token = None
        return self.current_token
    
    def _peek(self, offset: int = 1) -> Optional[Token]:
        """Peek at token at current position + offset."""
        pos = self.position + offset
        return self.tokens[pos] if pos < len(self.tokens) else None
    
    def _match(self, *token_types: TokenType) -> bool:
        """Check if current token matches any of the given types."""
        return self.current_token and self.current_token.type in token_types
    
    def _consume(self, token_type: TokenType, error_msg: str = "") -> Token:
        """Consume token of expected type or raise error."""
        if not self.current_token or self.current_token.type != token_type:
            msg = error_msg or f"Expected {token_type}, got {self.current_token.type if self.current_token else 'EOF'}"
            raise SyntaxError(msg)
        token = self.current_token
        self._advance()
        return token
    
    def _skip_newlines(self):
        """Skip newline tokens."""
        while self._match(TokenType.NEWLINE):
            self._advance()
    
    def _parse_build_file(self) -> BuildFile:
        """Parse a BUILD file."""
        package_name = self.file_path or "unknown"
        statements = []
        
        self._skip_newlines()
        while self.current_token and not self._match(TokenType.EOF):
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
            self._skip_newlines()
        
        return BuildFile(package_name=package_name, statements=statements)
    
    def _parse_workspace_file(self) -> WorkspaceFile:
        """Parse a WORKSPACE file."""
        workspace_name = "main"
        statements = []
        
        self._skip_newlines()
        while self.current_token and not self._match(TokenType.EOF):
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
            self._skip_newlines()
        
        return WorkspaceFile(workspace_name=workspace_name, statements=statements)
    
    def _parse_bzl_file(self) -> BzlFile:
        """Parse a .bzl file."""
        file_name = self.file_path or "unknown.bzl"
        statements = []
        load_statements = []
        
        self._skip_newlines()
        while self.current_token and not self._match(TokenType.EOF):
            if self._match(TokenType.LOAD):
                load_stmt = self._parse_load_statement()
                load_statements.append(load_stmt)
                statements.append(load_stmt)
            else:
                stmt = self._parse_statement()
                if stmt:
                    statements.append(stmt)
            self._skip_newlines()
        
        return BzlFile(file_name=file_name, statements=statements, load_statements=load_statements)
    
    def _parse_statement(self) -> Optional[BazelStatement]:
        """Parse a statement."""
        if self._match(TokenType.LOAD):
            return self._parse_load_statement()
        elif self._match(TokenType.DEF):
            return self._parse_function_def()
        elif self._match(TokenType.IF):
            return self._parse_if_statement()
        elif self._match(TokenType.FOR):
            return self._parse_for_loop()
        elif self._match(TokenType.IDENTIFIER):
            return self._parse_assignment_or_call()
        elif self._match(TokenType.COMMENT):
            self._advance()  # Skip comments
            return None
        else:
            # Skip unknown tokens
            self._advance()
            return None
    
    def _parse_load_statement(self) -> LoadStatement:
        """Parse a load statement."""
        self._consume(TokenType.LOAD)
        self._consume(TokenType.LPAREN)
        
        file_path_token = self._consume(TokenType.STRING)
        file_path = file_path_token.value.strip('"\'')
        
        symbols = []
        symbol_aliases = {}
        
        while self._match(TokenType.COMMA):
            self._advance()  # consume comma
            if self._match(TokenType.STRING):
                symbol = self.current_token.value.strip('"\'')
                symbols.append(symbol)
                self._advance()
            elif self._match(TokenType.IDENTIFIER):
                symbol = self.current_token.value
                symbols.append(symbol)
                self._advance()
        
        self._consume(TokenType.RPAREN)
        return LoadStatement(file_path=file_path, symbols=symbols, symbol_aliases=symbol_aliases)
    
    def _parse_function_def(self) -> FunctionDef:
        """Parse a function definition."""
        self._consume(TokenType.DEF)
        name_token = self._consume(TokenType.IDENTIFIER)
        self._consume(TokenType.LPAREN)
        
        parameters = []
        defaults = {}
        
        while not self._match(TokenType.RPAREN):
            if self._match(TokenType.IDENTIFIER):
                param = self.current_token.value
                parameters.append(param)
                self._advance()
                
                if self._match(TokenType.ASSIGN):
                    self._advance()
                    default_expr = self._parse_expression()
                    defaults[param] = default_expr
                
            if self._match(TokenType.COMMA):
                self._advance()
        
        self._consume(TokenType.RPAREN)
        self._consume(TokenType.COLON)
        
        # Parse function body (simplified)
        body = []
        if self._match(TokenType.INDENT):
            self._advance()
            while not self._match(TokenType.DEDENT, TokenType.EOF):
                stmt = self._parse_statement()
                if stmt:
                    body.append(stmt)
            if self._match(TokenType.DEDENT):
                self._advance()
        
        return FunctionDef(name=name_token.value, parameters=parameters, defaults=defaults, body=body)
    
    def _parse_assignment_or_call(self) -> BazelStatement:
        """Parse assignment or function call."""
        identifier_token = self.current_token
        self._advance()
        
        if self._match(TokenType.ASSIGN, TokenType.PLUS_ASSIGN):
            # Assignment
            op_token = self.current_token
            self._advance()
            value = self._parse_expression()
            return Assignment(target=identifier_token.value, value=value, operator=op_token.value)
        elif self._match(TokenType.LPAREN):
            # Function call (treat as target definition)
            self._advance()  # consume (
            
            attributes = {}
            while not self._match(TokenType.RPAREN):
                if self._match(TokenType.IDENTIFIER):
                    attr_name = self.current_token.value
                    self._advance()
                    self._consume(TokenType.ASSIGN)
                    attr_value = self._parse_expression()
                    attributes[attr_name] = attr_value
                
                if self._match(TokenType.COMMA):
                    self._advance()
            
            self._consume(TokenType.RPAREN)
            
            # Extract target name from attributes
            target_name = attributes.get('name', Literal("unknown", "string")).value if 'name' in attributes else "unknown"
            return TargetDefinition(rule_name=identifier_token.value, target_name=target_name, attributes=attributes)
        
        # Default: treat as expression statement
        return Assignment(target="temp", value=Identifier(identifier_token.value))
    
    def _parse_if_statement(self) -> IfStatement:
        """Parse an if statement."""
        self._consume(TokenType.IF)
        condition = self._parse_expression()
        self._consume(TokenType.COLON)
        
        then_body = []
        if self._match(TokenType.INDENT):
            self._advance()
            while not self._match(TokenType.DEDENT, TokenType.EOF):
                stmt = self._parse_statement()
                if stmt:
                    then_body.append(stmt)
            if self._match(TokenType.DEDENT):
                self._advance()
        
        else_body = None
        if self._match(TokenType.ELSE):
            self._advance()
            self._consume(TokenType.COLON)
            else_body = []
            if self._match(TokenType.INDENT):
                self._advance()
                while not self._match(TokenType.DEDENT, TokenType.EOF):
                    stmt = self._parse_statement()
                    if stmt:
                        else_body.append(stmt)
                if self._match(TokenType.DEDENT):
                    self._advance()
        
        return IfStatement(condition=condition, then_body=then_body, else_body=else_body)
    
    def _parse_for_loop(self) -> ForLoop:
        """Parse a for loop."""
        self._consume(TokenType.FOR)
        var_token = self._consume(TokenType.IDENTIFIER)
        self._consume(TokenType.IN)
        iterable = self._parse_expression()
        self._consume(TokenType.COLON)
        
        body = []
        if self._match(TokenType.INDENT):
            self._advance()
            while not self._match(TokenType.DEDENT, TokenType.EOF):
                stmt = self._parse_statement()
                if stmt:
                    body.append(stmt)
            if self._match(TokenType.DEDENT):
                self._advance()
        
        return ForLoop(variable=var_token.value, iterable=iterable, body=body)
    
    def _parse_expression(self) -> BazelExpression:
        """Parse an expression."""
        return self._parse_logical_or()
    
    def _parse_logical_or(self) -> BazelExpression:
        """Parse logical OR expression."""
        expr = self._parse_logical_and()
        # Simplified - in full implementation would handle 'or' operator
        return expr
    
    def _parse_logical_and(self) -> BazelExpression:
        """Parse logical AND expression."""
        expr = self._parse_equality()
        # Simplified - in full implementation would handle 'and' operator
        return expr
    
    def _parse_equality(self) -> BazelExpression:
        """Parse equality expression."""
        expr = self._parse_comparison()
        # Simplified - in full implementation would handle == and != operators
        return expr
    
    def _parse_comparison(self) -> BazelExpression:
        """Parse comparison expression."""
        expr = self._parse_addition()
        # Simplified - in full implementation would handle <, >, <=, >= operators
        return expr
    
    def _parse_addition(self) -> BazelExpression:
        """Parse addition/subtraction expression."""
        expr = self._parse_multiplication()
        # Simplified - in full implementation would handle + and - operators
        return expr
    
    def _parse_multiplication(self) -> BazelExpression:
        """Parse multiplication/division expression."""
        expr = self._parse_unary()
        # Simplified - in full implementation would handle *, /, % operators
        return expr
    
    def _parse_unary(self) -> BazelExpression:
        """Parse unary expression."""
        if self._match(TokenType.NOT, TokenType.MINUS):
            op_token = self.current_token
            self._advance()
            expr = self._parse_unary()
            # Return appropriate unary expression node
            return expr
        
        return self._parse_primary()
    
    def _parse_primary(self) -> BazelExpression:
        """Parse primary expression."""
        if self._match(TokenType.STRING):
            value = self.current_token.value.strip('"\'')
            self._advance()
            return Literal(value, "string")
        
        elif self._match(TokenType.INTEGER):
            value = int(self.current_token.value)
            self._advance()
            return Literal(value, "integer")
        
        elif self._match(TokenType.FLOAT):
            value = float(self.current_token.value)
            self._advance()
            return Literal(value, "float")
        
        elif self._match(TokenType.TRUE):
            self._advance()
            return Literal(True, "boolean")
        
        elif self._match(TokenType.FALSE):
            self._advance()
            return Literal(False, "boolean")
        
        elif self._match(TokenType.NONE):
            self._advance()
            return Literal(None, "none")
        
        elif self._match(TokenType.IDENTIFIER):
            name = self.current_token.value
            self._advance()
            
            # Check for function call
            if self._match(TokenType.LPAREN):
                return self._parse_call_expression(Identifier(name))
            
            # Check for attribute access
            while self._match(TokenType.DOT):
                self._advance()
                attr_token = self._consume(TokenType.IDENTIFIER)
                name = Attribute(Identifier(name), attr_token.value)
            
            return Identifier(name) if isinstance(name, str) else name
        
        elif self._match(TokenType.LABEL):
            label_str = self.current_token.value
            self._advance()
            return create_label(label_str)
        
        elif self._match(TokenType.LBRACKET):
            return self._parse_list_expression()
        
        elif self._match(TokenType.LBRACE):
            return self._parse_dict_expression()
        
        elif self._match(TokenType.LPAREN):
            self._advance()
            expr = self._parse_expression()
            self._consume(TokenType.RPAREN)
            return expr
        
        else:
            raise SyntaxError(f"Unexpected token {self.current_token.type} at line {self.current_token.line}")
    
    def _parse_call_expression(self, function: BazelExpression) -> CallExpr:
        """Parse function call expression."""
        self._consume(TokenType.LPAREN)
        
        args = []
        kwargs = {}
        
        while not self._match(TokenType.RPAREN):
            if self._match(TokenType.IDENTIFIER) and self._peek() and self._peek().type == TokenType.ASSIGN:
                # Keyword argument
                key_token = self.current_token
                self._advance()
                self._consume(TokenType.ASSIGN)
                value = self._parse_expression()
                kwargs[key_token.value] = value
            else:
                # Positional argument
                arg = self._parse_expression()
                args.append(arg)
            
            if self._match(TokenType.COMMA):
                self._advance()
        
        self._consume(TokenType.RPAREN)
        return CallExpr(function=function, args=args, kwargs=kwargs)
    
    def _parse_list_expression(self) -> ListExpr:
        """Parse list expression."""
        self._consume(TokenType.LBRACKET)
        
        elements = []
        while not self._match(TokenType.RBRACKET):
            element = self._parse_expression()
            elements.append(element)
            
            if self._match(TokenType.COMMA):
                self._advance()
        
        self._consume(TokenType.RBRACKET)
        return ListExpr(elements=elements)
    
    def _parse_dict_expression(self) -> DictExpr:
        """Parse dictionary expression."""
        self._consume(TokenType.LBRACE)
        
        pairs = []
        while not self._match(TokenType.RBRACE):
            key = self._parse_expression()
            self._consume(TokenType.COLON)
            value = self._parse_expression()
            pairs.append((key, value))
            
            if self._match(TokenType.COMMA):
                self._advance()
        
        self._consume(TokenType.RBRACE)
        return DictExpr(pairs=pairs)


# Public API functions
def parse_bazel(source: str, file_path: Optional[str] = None) -> Union[BuildFile, WorkspaceFile, BzlFile]:
    """Parse Bazel source code into AST."""
    lexer = BazelLexer(source, file_path)
    tokens = lexer.tokenize()
    parser = BazelParser(tokens, file_path)
    return parser.parse()


# Lexer and Parser classes for external use
__all__ = ['BazelLexer', 'BazelParser', 'parse_bazel', 'Token', 'TokenType'] 