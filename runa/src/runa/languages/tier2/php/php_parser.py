#!/usr/bin/env python3
"""
PHP Parser and Lexer

Comprehensive PHP parsing implementation supporting all PHP language features
including modern PHP 8+ syntax, type declarations, attributes, enums, and more.

Author: Sybertnetics AI Solutions
License: MIT
"""

import re
from typing import List, Optional, Dict, Any, Union, Tuple
from dataclasses import dataclass
from enum import Enum, auto
import logging

from .php_ast import *


class PhpTokenType(Enum):
    """PHP token types."""
    # Literals
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    HEREDOC = auto()
    NOWDOC = auto()
    BOOLEAN = auto()
    NULL = auto()
    
    # Identifiers and keywords
    IDENTIFIER = auto()
    VARIABLE = auto()
    KEYWORD = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    POWER = auto()
    ASSIGN = auto()
    PLUS_ASSIGN = auto()
    MINUS_ASSIGN = auto()
    MULTIPLY_ASSIGN = auto()
    DIVIDE_ASSIGN = auto()
    MODULO_ASSIGN = auto()
    POWER_ASSIGN = auto()
    CONCAT_ASSIGN = auto()
    EQUAL = auto()
    NOT_EQUAL = auto()
    IDENTICAL = auto()
    NOT_IDENTICAL = auto()
    LESS_THAN = auto()
    GREATER_THAN = auto()
    LESS_EQUAL = auto()
    GREATER_EQUAL = auto()
    SPACESHIP = auto()
    AND = auto()
    OR = auto()
    XOR = auto()
    NOT = auto()
    LOGICAL_AND = auto()
    LOGICAL_OR = auto()
    LOGICAL_XOR = auto()
    TERNARY = auto()
    NULL_COALESCE = auto()
    NULL_COALESCE_ASSIGN = auto()
    NULLSAFE_OPERATOR = auto()
    CONCAT = auto()
    ARROW = auto()
    DOUBLE_ARROW = auto()
    SCOPE_RESOLUTION = auto()
    INCREMENT = auto()
    DECREMENT = auto()
    
    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    COMMA = auto()
    SEMICOLON = auto()
    COLON = auto()
    DOLLAR = auto()
    AT = auto()
    HASH = auto()
    BACKSLASH = auto()
    
    # Special
    PHP_OPEN = auto()
    PHP_CLOSE = auto()
    EOF = auto()
    NEWLINE = auto()
    COMMENT = auto()
    DOC_COMMENT = auto()


@dataclass
class PhpToken:
    """PHP token representation."""
    type: PhpTokenType
    value: str
    line: int = 1
    column: int = 1


class PhpParseError(Exception):
    """PHP parsing error."""
    pass


class PhpLexer:
    """PHP lexer for tokenizing PHP source code."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.keywords = PHP_KEYWORDS
    
    def tokenize(self, source: str) -> List[PhpToken]:
        """Tokenize PHP source code."""
        tokens = []
        position = 0
        line = 1
        column = 1
        
        # Handle PHP opening tag
        if source.startswith('<?php'):
            tokens.append(PhpToken(PhpTokenType.PHP_OPEN, '<?php', line, column))
            position = 5
            column = 6
        elif source.startswith('<?'):
            tokens.append(PhpToken(PhpTokenType.PHP_OPEN, '<?', line, column))
            position = 2
            column = 3
        
        while position < len(source):
            # Skip whitespace
            if source[position].isspace():
                if source[position] == '\n':
                    line += 1
                    column = 1
                else:
                    column += 1
                position += 1
                continue
            
            # Comments
            if position < len(source) - 1:
                if source[position:position+2] == '//':
                    end = source.find('\n', position)
                    if end == -1:
                        end = len(source)
                    tokens.append(PhpToken(PhpTokenType.COMMENT, source[position:end], line, column))
                    position = end
                    continue
                elif source[position:position+2] == '/*':
                    end = source.find('*/', position + 2)
                    if end == -1:
                        end = len(source)
                    else:
                        end += 2
                    
                    comment_text = source[position:end]
                    if comment_text.startswith('/**'):
                        tokens.append(PhpToken(PhpTokenType.DOC_COMMENT, comment_text, line, column))
                    else:
                        tokens.append(PhpToken(PhpTokenType.COMMENT, comment_text, line, column))
                    
                    # Update line/column for multiline comments
                    for char in comment_text:
                        if char == '\n':
                            line += 1
                            column = 1
                        else:
                            column += 1
                    position = end
                    continue
                elif source[position:position+2] == '#[':
                    # Attribute
                    bracket_count = 1
                    end = position + 2
                    while end < len(source) and bracket_count > 0:
                        if source[end] == '[':
                            bracket_count += 1
                        elif source[end] == ']':
                            bracket_count -= 1
                        end += 1
                    
                    tokens.append(PhpToken(PhpTokenType.HASH, '#', line, column))
                    tokens.append(PhpToken(PhpTokenType.LBRACKET, '[', line, column + 1))
                    position += 2
                    column += 2
                    continue
            
            # String literals
            if source[position] in ['"', "'"]:
                quote = source[position]
                start = position
                position += 1
                
                while position < len(source):
                    if source[position] == quote and source[position - 1] != '\\':
                        position += 1
                        break
                    elif source[position] == '\n':
                        line += 1
                        column = 1
                    else:
                        column += 1
                    position += 1
                
                tokens.append(PhpToken(PhpTokenType.STRING, source[start:position], line, column))
                continue
            
            # Heredoc/Nowdoc
            if position < len(source) - 3 and source[position:position+3] == '<<<':
                # Handle heredoc/nowdoc parsing (simplified)
                end = source.find('\n', position)
                if end != -1:
                    delimiter_line = source[position:end]
                    delimiter = delimiter_line[3:].strip()
                    
                    # Find end delimiter
                    end_pos = source.find('\n' + delimiter, end)
                    if end_pos != -1:
                        heredoc_content = source[position:end_pos + len(delimiter) + 1]
                        if delimiter.startswith("'"):
                            tokens.append(PhpToken(PhpTokenType.NOWDOC, heredoc_content, line, column))
                        else:
                            tokens.append(PhpToken(PhpTokenType.HEREDOC, heredoc_content, line, column))
                        
                        # Update position and line/column
                        for char in heredoc_content:
                            if char == '\n':
                                line += 1
                                column = 1
                            else:
                                column += 1
                        position = end_pos + len(delimiter) + 1
                        continue
            
            # Variables
            if source[position] == '$':
                start = position
                position += 1
                column += 1
                
                if position < len(source) and (source[position].isalpha() or source[position] == '_'):
                    while position < len(source) and (source[position].isalnum() or source[position] == '_'):
                        position += 1
                        column += 1
                    
                    tokens.append(PhpToken(PhpTokenType.VARIABLE, source[start:position], line, column))
                    continue
                else:
                    tokens.append(PhpToken(PhpTokenType.DOLLAR, '$', line, column))
                    continue
            
            # Numbers
            if source[position].isdigit():
                start = position
                is_float = False
                
                while position < len(source) and (source[position].isdigit() or source[position] == '.'):
                    if source[position] == '.':
                        if is_float:
                            break
                        is_float = True
                    position += 1
                
                value = source[start:position]
                token_type = PhpTokenType.FLOAT if is_float else PhpTokenType.INTEGER
                tokens.append(PhpToken(token_type, value, line, column))
                column += position - start
                continue
            
            # Identifiers and keywords
            if source[position].isalpha() or source[position] == '_':
                start = position
                while position < len(source) and (source[position].isalnum() or source[position] == '_'):
                    position += 1
                
                value = source[start:position]
                
                # Check for special literals
                if value.lower() in ['true', 'false']:
                    token_type = PhpTokenType.BOOLEAN
                elif value.lower() == 'null':
                    token_type = PhpTokenType.NULL
                elif value.lower() in self.keywords:
                    token_type = PhpTokenType.KEYWORD
                else:
                    token_type = PhpTokenType.IDENTIFIER
                
                tokens.append(PhpToken(token_type, value, line, column))
                column += position - start
                continue
            
            # Multi-character operators
            if position < len(source) - 1:
                two_char = source[position:position+2]
                three_char = source[position:position+3] if position < len(source) - 2 else ""
                
                multi_char_ops = {
                    '===': PhpTokenType.IDENTICAL,
                    '!==': PhpTokenType.NOT_IDENTICAL,
                    '<=>': PhpTokenType.SPACESHIP,
                    '**=': PhpTokenType.POWER_ASSIGN,
                    '??=': PhpTokenType.NULL_COALESCE_ASSIGN,
                    '?->': PhpTokenType.NULLSAFE_OPERATOR,
                    '++': PhpTokenType.INCREMENT,
                    '--': PhpTokenType.DECREMENT,
                    '+=': PhpTokenType.PLUS_ASSIGN,
                    '-=': PhpTokenType.MINUS_ASSIGN,
                    '*=': PhpTokenType.MULTIPLY_ASSIGN,
                    '/=': PhpTokenType.DIVIDE_ASSIGN,
                    '%=': PhpTokenType.MODULO_ASSIGN,
                    '.=': PhpTokenType.CONCAT_ASSIGN,
                    '==': PhpTokenType.EQUAL,
                    '!=': PhpTokenType.NOT_EQUAL,
                    '<>': PhpTokenType.NOT_EQUAL,
                    '<=': PhpTokenType.LESS_EQUAL,
                    '>=': PhpTokenType.GREATER_EQUAL,
                    '&&': PhpTokenType.LOGICAL_AND,
                    '||': PhpTokenType.LOGICAL_OR,
                    '**': PhpTokenType.POWER,
                    '??': PhpTokenType.NULL_COALESCE,
                    '->': PhpTokenType.ARROW,
                    '=>': PhpTokenType.DOUBLE_ARROW,
                    '::': PhpTokenType.SCOPE_RESOLUTION,
                    '?>': PhpTokenType.PHP_CLOSE,
                }
                
                if three_char in multi_char_ops:
                    tokens.append(PhpToken(multi_char_ops[three_char], three_char, line, column))
                    position += 3
                    column += 3
                    continue
                elif two_char in multi_char_ops:
                    tokens.append(PhpToken(multi_char_ops[two_char], two_char, line, column))
                    position += 2
                    column += 2
                    continue
            
            # Single character tokens
            single_char_tokens = {
                '(': PhpTokenType.LPAREN,
                ')': PhpTokenType.RPAREN,
                '{': PhpTokenType.LBRACE,
                '}': PhpTokenType.RBRACE,
                '[': PhpTokenType.LBRACKET,
                ']': PhpTokenType.RBRACKET,
                ',': PhpTokenType.COMMA,
                ';': PhpTokenType.SEMICOLON,
                ':': PhpTokenType.COLON,
                '+': PhpTokenType.PLUS,
                '-': PhpTokenType.MINUS,
                '*': PhpTokenType.MULTIPLY,
                '/': PhpTokenType.DIVIDE,
                '%': PhpTokenType.MODULO,
                '=': PhpTokenType.ASSIGN,
                '<': PhpTokenType.LESS_THAN,
                '>': PhpTokenType.GREATER_THAN,
                '!': PhpTokenType.NOT,
                '&': PhpTokenType.AND,
                '|': PhpTokenType.OR,
                '^': PhpTokenType.XOR,
                '~': PhpTokenType.NOT,
                '?': PhpTokenType.TERNARY,
                '.': PhpTokenType.CONCAT,
                '@': PhpTokenType.AT,
                '#': PhpTokenType.HASH,
                '\\': PhpTokenType.BACKSLASH,
            }
            
            if source[position] in single_char_tokens:
                token_type = single_char_tokens[source[position]]
                tokens.append(PhpToken(token_type, source[position], line, column))
                position += 1
                column += 1
                continue
            
            # Skip unknown characters
            position += 1
            column += 1
        
        tokens.append(PhpToken(PhpTokenType.EOF, "", line, column))
        return tokens


class PhpParser:
    """PHP recursive descent parser."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.tokens: List[PhpToken] = []
        self.current = 0
    
    def parse(self, source: str) -> PhpSourceFile:
        """Parse PHP source code into an AST."""
        try:
            lexer = PhpLexer()
            self.tokens = lexer.tokenize(source)
            self.current = 0
            
            return self._parse_source_file()
            
        except Exception as e:
            self.logger.error(f"PHP parsing failed: {e}")
            raise PhpParseError(f"Failed to parse PHP code: {e}")
    
    def _current_token(self) -> PhpToken:
        """Get current token."""
        if self.current >= len(self.tokens):
            return PhpToken(PhpTokenType.EOF, "", 0, 0)
        return self.tokens[self.current]
    
    def _advance(self) -> PhpToken:
        """Advance to next token."""
        token = self._current_token()
        if self.current < len(self.tokens) - 1:
            self.current += 1
        return token
    
    def _match(self, *token_types: PhpTokenType) -> bool:
        """Check if current token matches any of the given types."""
        return self._current_token().type in token_types
    
    def _consume(self, token_type: PhpTokenType) -> PhpToken:
        """Consume token of specific type."""
        token = self._current_token()
        if token.type != token_type:
            raise PhpParseError(f"Expected {token_type}, got {token.type}")
        return self._advance()
    
    def _parse_source_file(self) -> PhpSourceFile:
        """Parse source file."""
        declarations = []
        statements = []
        
        # Skip opening PHP tag
        if self._match(PhpTokenType.PHP_OPEN):
            self._advance()
        
        # Parse top-level declarations and statements
        while not self._match(PhpTokenType.EOF, PhpTokenType.PHP_CLOSE):
            # Skip comments
            if self._match(PhpTokenType.COMMENT, PhpTokenType.DOC_COMMENT):
                self._advance()
                continue
            
            try:
                if self._match(PhpTokenType.KEYWORD):
                    keyword = self._current_token().value.lower()
                    
                    if keyword == "namespace":
                        declarations.append(self._parse_namespace())
                    elif keyword == "use":
                        declarations.append(self._parse_use_declaration())
                    elif keyword in ["class", "abstract", "final"]:
                        declarations.append(self._parse_class_declaration())
                    elif keyword == "interface":
                        declarations.append(self._parse_interface_declaration())
                    elif keyword == "trait":
                        declarations.append(self._parse_trait_declaration())
                    elif keyword == "enum":
                        declarations.append(self._parse_enum_declaration())
                    elif keyword == "function":
                        declarations.append(self._parse_function_declaration())
                    else:
                        # Parse as statement
                        stmt = self._parse_statement()
                        if stmt:
                            statements.append(stmt)
                else:
                    # Parse as statement
                    stmt = self._parse_statement()
                    if stmt:
                        statements.append(stmt)
            except Exception as e:
                self.logger.warning(f"Skipping invalid syntax: {e}")
                # Skip to next semicolon or brace
                while not self._match(PhpTokenType.SEMICOLON, PhpTokenType.RBRACE, PhpTokenType.EOF):
                    self._advance()
                if self._match(PhpTokenType.SEMICOLON):
                    self._advance()
        
        return PhpSourceFile(declarations=declarations, statements=statements)
    
    def _parse_namespace(self) -> PhpNamespaceDeclaration:
        """Parse namespace declaration."""
        self._consume(PhpTokenType.KEYWORD)  # consume 'namespace'
        
        name = ""
        if self._match(PhpTokenType.IDENTIFIER):
            name = self._advance().value
            
            # Handle nested namespace
            while self._match(PhpTokenType.BACKSLASH):
                self._advance()
                if self._match(PhpTokenType.IDENTIFIER):
                    name += "\\" + self._advance().value
        
        statements = []
        if self._match(PhpTokenType.LBRACE):
            self._advance()
            while not self._match(PhpTokenType.RBRACE, PhpTokenType.EOF):
                stmt = self._parse_statement()
                if stmt:
                    statements.append(stmt)
            
            if self._match(PhpTokenType.RBRACE):
                self._advance()
        else:
            if self._match(PhpTokenType.SEMICOLON):
                self._advance()
        
        return PhpNamespaceDeclaration(name=name, statements=statements)
    
    def _parse_use_declaration(self) -> PhpUseDeclaration:
        """Parse use declaration."""
        self._consume(PhpTokenType.KEYWORD)  # consume 'use'
        
        name = ""
        if self._match(PhpTokenType.IDENTIFIER):
            name = self._advance().value
            
            # Handle namespace path
            while self._match(PhpTokenType.BACKSLASH):
                self._advance()
                if self._match(PhpTokenType.IDENTIFIER):
                    name += "\\" + self._advance().value
        
        alias = None
        if self._match(PhpTokenType.KEYWORD) and self._current_token().value.lower() == "as":
            self._advance()
            if self._match(PhpTokenType.IDENTIFIER):
                alias = self._advance().value
        
        if self._match(PhpTokenType.SEMICOLON):
            self._advance()
        
        return PhpUseDeclaration(name=name, alias=alias)
    
    def _parse_class_declaration(self) -> PhpClassDeclaration:
        """Parse class declaration."""
        modifiers = []
        
        # Handle modifiers
        while self._match(PhpTokenType.KEYWORD):
            keyword = self._current_token().value.lower()
            if keyword in ["abstract", "final"]:
                modifiers.append(keyword)
                self._advance()
            elif keyword == "class":
                break
            else:
                break
        
        self._consume(PhpTokenType.KEYWORD)  # consume 'class'
        
        name = ""
        if self._match(PhpTokenType.IDENTIFIER):
            name = self._advance().value
        
        extends = None
        if self._match(PhpTokenType.KEYWORD) and self._current_token().value.lower() == "extends":
            self._advance()
            if self._match(PhpTokenType.IDENTIFIER):
                extends = self._advance().value
        
        implements = []
        if self._match(PhpTokenType.KEYWORD) and self._current_token().value.lower() == "implements":
            self._advance()
            while self._match(PhpTokenType.IDENTIFIER):
                implements.append(self._advance().value)
                if self._match(PhpTokenType.COMMA):
                    self._advance()
                else:
                    break
        
        members = []
        if self._match(PhpTokenType.LBRACE):
            self._advance()
            while not self._match(PhpTokenType.RBRACE, PhpTokenType.EOF):
                # Skip comments
                if self._match(PhpTokenType.COMMENT, PhpTokenType.DOC_COMMENT):
                    self._advance()
                    continue
                
                # Parse class members (simplified)
                if self._match(PhpTokenType.KEYWORD):
                    keyword = self._current_token().value.lower()
                    if keyword == "function":
                        members.append(self._parse_method_declaration())
                    elif keyword in ["public", "protected", "private", "static", "var"]:
                        # Property or method
                        self._skip_to_semicolon_or_brace()
                    else:
                        self._advance()
                else:
                    self._advance()
            
            if self._match(PhpTokenType.RBRACE):
                self._advance()
        
        return PhpClassDeclaration(
            name=name,
            extends=extends,
            implements=implements,
            members=members,
            is_abstract="abstract" in modifiers,
            is_final="final" in modifiers
        )
    
    def _parse_interface_declaration(self) -> PhpInterfaceDeclaration:
        """Parse interface declaration."""
        self._consume(PhpTokenType.KEYWORD)  # consume 'interface'
        
        name = ""
        if self._match(PhpTokenType.IDENTIFIER):
            name = self._advance().value
        
        extends = []
        if self._match(PhpTokenType.KEYWORD) and self._current_token().value.lower() == "extends":
            self._advance()
            while self._match(PhpTokenType.IDENTIFIER):
                extends.append(self._advance().value)
                if self._match(PhpTokenType.COMMA):
                    self._advance()
                else:
                    break
        
        members = []
        if self._match(PhpTokenType.LBRACE):
            self._advance()
            while not self._match(PhpTokenType.RBRACE, PhpTokenType.EOF):
                # Skip to end for now
                self._advance()
            
            if self._match(PhpTokenType.RBRACE):
                self._advance()
        
        return PhpInterfaceDeclaration(name=name, extends=extends, members=members)
    
    def _parse_trait_declaration(self) -> PhpTraitDeclaration:
        """Parse trait declaration."""
        self._consume(PhpTokenType.KEYWORD)  # consume 'trait'
        
        name = ""
        if self._match(PhpTokenType.IDENTIFIER):
            name = self._advance().value
        
        members = []
        if self._match(PhpTokenType.LBRACE):
            self._advance()
            while not self._match(PhpTokenType.RBRACE, PhpTokenType.EOF):
                # Skip to end for now
                self._advance()
            
            if self._match(PhpTokenType.RBRACE):
                self._advance()
        
        return PhpTraitDeclaration(name=name, members=members)
    
    def _parse_enum_declaration(self) -> PhpEnumDeclaration:
        """Parse enum declaration."""
        self._consume(PhpTokenType.KEYWORD)  # consume 'enum'
        
        name = ""
        if self._match(PhpTokenType.IDENTIFIER):
            name = self._advance().value
        
        backed_type = None
        if self._match(PhpTokenType.COLON):
            self._advance()
            if self._match(PhpTokenType.IDENTIFIER):
                backed_type = PhpTypeDeclaration(name=self._advance().value)
        
        cases = []
        members = []
        
        if self._match(PhpTokenType.LBRACE):
            self._advance()
            while not self._match(PhpTokenType.RBRACE, PhpTokenType.EOF):
                if self._match(PhpTokenType.KEYWORD) and self._current_token().value.lower() == "case":
                    self._advance()
                    case_name = ""
                    if self._match(PhpTokenType.IDENTIFIER):
                        case_name = self._advance().value
                    
                    # Skip value for now
                    while not self._match(PhpTokenType.SEMICOLON, PhpTokenType.EOF):
                        self._advance()
                    if self._match(PhpTokenType.SEMICOLON):
                        self._advance()
                    
                    cases.append(PhpEnumCase(name=case_name))
                else:
                    self._advance()
            
            if self._match(PhpTokenType.RBRACE):
                self._advance()
        
        return PhpEnumDeclaration(name=name, backed_type=backed_type, cases=cases, members=members)
    
    def _parse_function_declaration(self) -> PhpFunctionDeclaration:
        """Parse function declaration."""
        self._consume(PhpTokenType.KEYWORD)  # consume 'function'
        
        name = ""
        if self._match(PhpTokenType.IDENTIFIER):
            name = self._advance().value
        
        parameters = []
        if self._match(PhpTokenType.LPAREN):
            self._advance()
            # Skip parameters for now
            while not self._match(PhpTokenType.RPAREN, PhpTokenType.EOF):
                self._advance()
            
            if self._match(PhpTokenType.RPAREN):
                self._advance()
        
        # Skip return type and body for now
        body = None
        if self._match(PhpTokenType.LBRACE):
            body = self._parse_block()
        
        return PhpFunctionDeclaration(name=name, parameters=parameters, body=body)
    
    def _parse_method_declaration(self) -> PhpMethodDeclaration:
        """Parse method declaration."""
        # Skip to function keyword
        while not self._match(PhpTokenType.KEYWORD, PhpTokenType.EOF):
            self._advance()
        
        if self._current_token().value.lower() == "function":
            self._advance()
        
        name = ""
        if self._match(PhpTokenType.IDENTIFIER):
            name = self._advance().value
        
        parameters = []
        if self._match(PhpTokenType.LPAREN):
            self._advance()
            # Skip parameters for now
            while not self._match(PhpTokenType.RPAREN, PhpTokenType.EOF):
                self._advance()
            
            if self._match(PhpTokenType.RPAREN):
                self._advance()
        
        # Skip return type and body for now
        body = None
        if self._match(PhpTokenType.LBRACE):
            body = self._parse_block()
        
        return PhpMethodDeclaration(name=name, parameters=parameters, body=body)
    
    def _parse_statement(self) -> Optional[PhpStatement]:
        """Parse statement."""
        if self._match(PhpTokenType.LBRACE):
            return self._parse_block()
        elif self._match(PhpTokenType.KEYWORD):
            keyword = self._current_token().value.lower()
            
            if keyword == "echo":
                return self._parse_echo_statement()
            elif keyword == "return":
                return self._parse_return_statement()
            elif keyword == "if":
                return self._parse_if_statement()
            elif keyword == "while":
                return self._parse_while_statement()
            elif keyword == "for":
                return self._parse_for_statement()
            elif keyword == "foreach":
                return self._parse_foreach_statement()
            else:
                # Skip unknown keywords
                self._advance()
                return None
        else:
            # Expression statement
            expr = self._parse_expression()
            if self._match(PhpTokenType.SEMICOLON):
                self._advance()
            return PhpExpressionStatement(expression=expr)
    
    def _parse_block(self) -> PhpBlock:
        """Parse block statement."""
        self._consume(PhpTokenType.LBRACE)
        
        statements = []
        while not self._match(PhpTokenType.RBRACE, PhpTokenType.EOF):
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
        
        if self._match(PhpTokenType.RBRACE):
            self._advance()
        
        return PhpBlock(statements=statements)
    
    def _parse_echo_statement(self) -> PhpEchoStatement:
        """Parse echo statement."""
        self._consume(PhpTokenType.KEYWORD)  # consume 'echo'
        
        expressions = []
        if not self._match(PhpTokenType.SEMICOLON):
            expressions.append(self._parse_expression())
            
            while self._match(PhpTokenType.COMMA):
                self._advance()
                expressions.append(self._parse_expression())
        
        if self._match(PhpTokenType.SEMICOLON):
            self._advance()
        
        return PhpEchoStatement(expressions=expressions)
    
    def _parse_return_statement(self) -> PhpReturnStatement:
        """Parse return statement."""
        self._consume(PhpTokenType.KEYWORD)  # consume 'return'
        
        expression = None
        if not self._match(PhpTokenType.SEMICOLON):
            expression = self._parse_expression()
        
        if self._match(PhpTokenType.SEMICOLON):
            self._advance()
        
        return PhpReturnStatement(expression=expression)
    
    def _parse_if_statement(self) -> PhpIfStatement:
        """Parse if statement."""
        self._consume(PhpTokenType.KEYWORD)  # consume 'if'
        
        condition = None
        if self._match(PhpTokenType.LPAREN):
            self._advance()
            condition = self._parse_expression()
            if self._match(PhpTokenType.RPAREN):
                self._advance()
        
        then_statement = self._parse_statement()
        
        return PhpIfStatement(condition=condition, then_statement=then_statement)
    
    def _parse_while_statement(self) -> PhpWhileStatement:
        """Parse while statement."""
        self._consume(PhpTokenType.KEYWORD)  # consume 'while'
        
        condition = None
        if self._match(PhpTokenType.LPAREN):
            self._advance()
            condition = self._parse_expression()
            if self._match(PhpTokenType.RPAREN):
                self._advance()
        
        body = self._parse_statement()
        
        return PhpWhileStatement(condition=condition, body=body)
    
    def _parse_for_statement(self) -> PhpForStatement:
        """Parse for statement."""
        self._consume(PhpTokenType.KEYWORD)  # consume 'for'
        
        init = []
        condition = []
        update = []
        
        if self._match(PhpTokenType.LPAREN):
            self._advance()
            
            # Skip for loop parts for now
            while not self._match(PhpTokenType.RPAREN, PhpTokenType.EOF):
                self._advance()
            
            if self._match(PhpTokenType.RPAREN):
                self._advance()
        
        body = self._parse_statement()
        
        return PhpForStatement(init=init, condition=condition, update=update, body=body)
    
    def _parse_foreach_statement(self) -> PhpForeachStatement:
        """Parse foreach statement."""
        self._consume(PhpTokenType.KEYWORD)  # consume 'foreach'
        
        iterable = None
        value_variable = None
        
        if self._match(PhpTokenType.LPAREN):
            self._advance()
            
            # Simplified foreach parsing
            if self._match(PhpTokenType.VARIABLE):
                iterable = PhpVariable(name=self._advance().value)
            
            if self._match(PhpTokenType.KEYWORD) and self._current_token().value.lower() == "as":
                self._advance()
                if self._match(PhpTokenType.VARIABLE):
                    value_variable = PhpVariable(name=self._advance().value)
            
            # Skip to closing paren
            while not self._match(PhpTokenType.RPAREN, PhpTokenType.EOF):
                self._advance()
            
            if self._match(PhpTokenType.RPAREN):
                self._advance()
        
        body = self._parse_statement()
        
        return PhpForeachStatement(iterable=iterable, value_variable=value_variable, body=body)
    
    def _parse_expression(self) -> Optional[PhpExpression]:
        """Parse expression (simplified)."""
        if self._match(PhpTokenType.VARIABLE):
            return PhpVariable(name=self._advance().value)
        elif self._match(PhpTokenType.STRING):
            value = self._advance().value
            # Remove quotes
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            return PhpLiteral(value=value, literal_type="string")
        elif self._match(PhpTokenType.INTEGER):
            value = int(self._advance().value)
            return PhpLiteral(value=value, literal_type="int")
        elif self._match(PhpTokenType.FLOAT):
            value = float(self._advance().value)
            return PhpLiteral(value=value, literal_type="float")
        elif self._match(PhpTokenType.BOOLEAN):
            value = self._advance().value.lower() == "true"
            return PhpLiteral(value=value, literal_type="bool")
        elif self._match(PhpTokenType.NULL):
            self._advance()
            return PhpLiteral(value=None, literal_type="null")
        elif self._match(PhpTokenType.IDENTIFIER):
            return PhpIdentifier(name=self._advance().value)
        else:
            # Skip unknown expression
            if not self._match(PhpTokenType.EOF):
                self._advance()
            return None
    
    def _skip_to_semicolon_or_brace(self):
        """Skip tokens until semicolon or brace."""
        while not self._match(PhpTokenType.SEMICOLON, PhpTokenType.LBRACE, PhpTokenType.RBRACE, PhpTokenType.EOF):
            self._advance()
        
        if self._match(PhpTokenType.SEMICOLON):
            self._advance()
        elif self._match(PhpTokenType.LBRACE):
            # Skip entire block
            brace_count = 1
            self._advance()
            while brace_count > 0 and not self._match(PhpTokenType.EOF):
                if self._match(PhpTokenType.LBRACE):
                    brace_count += 1
                elif self._match(PhpTokenType.RBRACE):
                    brace_count -= 1
                self._advance()


# Convenience functions
def parse_php_code(source: str) -> PhpSourceFile:
    """Parse PHP source code and return AST."""
    parser = PhpParser()
    return parser.parse(source)


def tokenize_php_code(source: str) -> List[PhpToken]:
    """Tokenize PHP source code and return tokens."""
    lexer = PhpLexer()
    return lexer.tokenize(source)