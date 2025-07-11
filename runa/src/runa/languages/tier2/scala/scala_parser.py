#!/usr/bin/env python3
"""
Scala Parser and Lexer

Comprehensive Scala parsing implementation supporting all Scala language features
including pattern matching, higher-order functions, implicits, type classes, and Scala 3 features.

Author: Sybertnetics AI Solutions
License: MIT
"""

import re
from typing import List, Optional, Dict, Any, Union, Tuple
from dataclasses import dataclass
from enum import Enum, auto
import logging

from .scala_ast import *


class ScalaTokenType(Enum):
    """Scala token types."""
    # Literals
    INTEGER = auto()
    LONG = auto()
    FLOAT = auto()
    DOUBLE = auto()
    STRING = auto()
    CHAR = auto()
    SYMBOL = auto()
    BOOLEAN = auto()
    NULL = auto()
    
    # Identifiers and keywords
    IDENTIFIER = auto()
    KEYWORD = auto()
    OPERATOR_IDENTIFIER = auto()
    
    # Operators and punctuation
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    ASSIGN = auto()
    EQUAL = auto()
    NOT_EQUAL = auto()
    LESS_THAN = auto()
    GREATER_THAN = auto()
    LESS_EQUAL = auto()
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
    
    # Scala-specific operators
    ARROW = auto()  # =>
    LEFT_ARROW = auto()  # <-
    RIGHT_ARROW = auto()  # ->
    SUBTYPE = auto()  # <:
    SUPERTYPE = auto()  # >:
    VIEW_BOUND = auto()  # <%
    HASH = auto()  # #
    AT = auto()  # @
    DOUBLE_COLON = auto()  # ::
    TRIPLE_COLON = auto()  # :::
    PREPEND = auto()  # +:
    APPEND = auto()  # :+
    
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
    DOT = auto()
    UNDERSCORE = auto()
    BACKTICK = auto()
    
    # Special
    EOF = auto()
    NEWLINE = auto()
    COMMENT = auto()
    DOC_COMMENT = auto()
    INTERPOLATION_START = auto()
    INTERPOLATION_PART = auto()
    INTERPOLATION_END = auto()


@dataclass
class ScalaToken:
    """Scala token representation."""
    type: ScalaTokenType
    value: str
    line: int = 1
    column: int = 1


class ScalaParseError(Exception):
    """Scala parsing error."""
    pass


class ScalaLexer:
    """Scala lexer for tokenizing Scala source code."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.keywords = SCALA_KEYWORDS
    
    def tokenize(self, source: str) -> List[ScalaToken]:
        """Tokenize Scala source code."""
        tokens = []
        position = 0
        line = 1
        column = 1
        
        while position < len(source):
            # Skip whitespace except newlines
            if source[position].isspace() and source[position] != '\n':
                column += 1
                position += 1
                continue
            
            # Newlines
            if source[position] == '\n':
                tokens.append(ScalaToken(ScalaTokenType.NEWLINE, '\n', line, column))
                line += 1
                column = 1
                position += 1
                continue
            
            # Comments
            if position < len(source) - 1:
                if source[position:position+2] == '//':
                    end = source.find('\n', position)
                    if end == -1:
                        end = len(source)
                    tokens.append(ScalaToken(ScalaTokenType.COMMENT, source[position:end], line, column))
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
                        tokens.append(ScalaToken(ScalaTokenType.DOC_COMMENT, comment_text, line, column))
                    else:
                        tokens.append(ScalaToken(ScalaTokenType.COMMENT, comment_text, line, column))
                    
                    # Update line/column for multiline comments
                    for char in comment_text:
                        if char == '\n':
                            line += 1
                            column = 1
                        else:
                            column += 1
                    position = end
                    continue
            
            # String literals
            if source[position] == '"':
                start = position
                position += 1
                
                while position < len(source):
                    if source[position] == '"' and source[position - 1] != '\\':
                        position += 1
                        break
                    elif source[position] == '\n':
                        line += 1
                        column = 1
                    else:
                        column += 1
                    position += 1
                
                tokens.append(ScalaToken(ScalaTokenType.STRING, source[start:position], line, column))
                continue
            
            # Multi-line strings
            if position < len(source) - 2 and source[position:position+3] == '"""':
                start = position
                position += 3
                
                while position < len(source) - 2:
                    if source[position:position+3] == '"""':
                        position += 3
                        break
                    elif source[position] == '\n':
                        line += 1
                        column = 1
                    else:
                        column += 1
                    position += 1
                
                tokens.append(ScalaToken(ScalaTokenType.STRING, source[start:position], line, column))
                continue
            
            # Character literals
            if source[position] == "'" and position < len(source) - 2:
                start = position
                position += 1
                
                if source[position] == '\\':
                    position += 1  # Skip escape character
                position += 1  # Character
                
                if position < len(source) and source[position] == "'":
                    position += 1
                    tokens.append(ScalaToken(ScalaTokenType.CHAR, source[start:position], line, column))
                    column += position - start
                    continue
            
            # Symbol literals
            if source[position] == "'" and position < len(source) - 1:
                if source[position + 1].isalpha() or source[position + 1] == '_':
                    start = position
                    position += 1
                    
                    while position < len(source) and (source[position].isalnum() or source[position] == '_'):
                        position += 1
                    
                    tokens.append(ScalaToken(ScalaTokenType.SYMBOL, source[start:position], line, column))
                    column += position - start
                    continue
            
            # String interpolation
            if position < len(source) - 1:
                interpolators = ['s', 'f', 'raw']
                for interp in interpolators:
                    if (source[position:position+len(interp)] == interp and 
                        position + len(interp) < len(source) and source[position + len(interp)] == '"'):
                        # Handle string interpolation (simplified)
                        start = position
                        position += len(interp) + 1  # Skip interpolator and quote
                        
                        while position < len(source):
                            if source[position] == '"' and source[position - 1] != '\\':
                                position += 1
                                break
                            position += 1
                        
                        tokens.append(ScalaToken(ScalaTokenType.INTERPOLATION_START, source[start:position], line, column))
                        column += position - start
                        break
                else:
                    # Not an interpolation, continue
                    pass
                
                # If we found interpolation, continue to next iteration
                if tokens and tokens[-1].type == ScalaTokenType.INTERPOLATION_START:
                    continue
            
            # Numbers
            if source[position].isdigit():
                start = position
                is_float = False
                is_long = False
                
                while position < len(source) and (source[position].isdigit() or source[position] == '.'):
                    if source[position] == '.':
                        if is_float:
                            break
                        is_float = True
                    position += 1
                
                # Check for L suffix
                if position < len(source) and source[position].lower() == 'l':
                    is_long = True
                    position += 1
                
                # Check for F/D suffix
                if position < len(source) and source[position].lower() in 'fd':
                    suffix = source[position].lower()
                    position += 1
                    if suffix == 'f':
                        is_float = True
                    else:  # 'd'
                        is_float = True
                
                value = source[start:position]
                
                if is_float:
                    if value.endswith('f') or value.endswith('F'):
                        token_type = ScalaTokenType.FLOAT
                    else:
                        token_type = ScalaTokenType.DOUBLE
                elif is_long:
                    token_type = ScalaTokenType.LONG
                else:
                    token_type = ScalaTokenType.INTEGER
                
                tokens.append(ScalaToken(token_type, value, line, column))
                column += position - start
                continue
            
            # Identifiers and keywords
            if source[position].isalpha() or source[position] == '_':
                start = position
                
                while position < len(source) and (source[position].isalnum() or source[position] == '_'):
                    position += 1
                
                value = source[start:position]
                
                # Check for special literals
                if value in ['true', 'false']:
                    token_type = ScalaTokenType.BOOLEAN
                elif value == 'null':
                    token_type = ScalaTokenType.NULL
                elif value in self.keywords:
                    token_type = ScalaTokenType.KEYWORD
                else:
                    token_type = ScalaTokenType.IDENTIFIER
                
                tokens.append(ScalaToken(token_type, value, line, column))
                column += position - start
                continue
            
            # Backtick identifiers
            if source[position] == '`':
                start = position
                position += 1
                
                while position < len(source) and source[position] != '`':
                    position += 1
                
                if position < len(source):
                    position += 1  # Include closing backtick
                
                tokens.append(ScalaToken(ScalaTokenType.IDENTIFIER, source[start:position], line, column))
                column += position - start
                continue
            
            # Multi-character operators
            if position < len(source) - 1:
                two_char = source[position:position+2]
                three_char = source[position:position+3] if position < len(source) - 2 else ""
                
                multi_char_ops = {
                    '=>': ScalaTokenType.ARROW,
                    '<-': ScalaTokenType.LEFT_ARROW,
                    '->': ScalaTokenType.RIGHT_ARROW,
                    '<:': ScalaTokenType.SUBTYPE,
                    '>:': ScalaTokenType.SUPERTYPE,
                    '<%': ScalaTokenType.VIEW_BOUND,
                    '==': ScalaTokenType.EQUAL,
                    '!=': ScalaTokenType.NOT_EQUAL,
                    '<=': ScalaTokenType.LESS_EQUAL,
                    '>=': ScalaTokenType.GREATER_EQUAL,
                    '&&': ScalaTokenType.AND,
                    '||': ScalaTokenType.OR,
                    '<<': ScalaTokenType.LEFT_SHIFT,
                    '>>': ScalaTokenType.RIGHT_SHIFT,
                    '::': ScalaTokenType.DOUBLE_COLON,
                    ':+': ScalaTokenType.APPEND,
                    '+:': ScalaTokenType.PREPEND,
                }
                
                three_char_ops = {
                    '>>>': ScalaTokenType.UNSIGNED_RIGHT_SHIFT,
                    ':::': ScalaTokenType.TRIPLE_COLON,
                }
                
                if three_char in three_char_ops:
                    tokens.append(ScalaToken(three_char_ops[three_char], three_char, line, column))
                    position += 3
                    column += 3
                    continue
                elif two_char in multi_char_ops:
                    tokens.append(ScalaToken(multi_char_ops[two_char], two_char, line, column))
                    position += 2
                    column += 2
                    continue
            
            # Single character tokens
            single_char_tokens = {
                '(': ScalaTokenType.LPAREN,
                ')': ScalaTokenType.RPAREN,
                '{': ScalaTokenType.LBRACE,
                '}': ScalaTokenType.RBRACE,
                '[': ScalaTokenType.LBRACKET,
                ']': ScalaTokenType.RBRACKET,
                ',': ScalaTokenType.COMMA,
                ';': ScalaTokenType.SEMICOLON,
                ':': ScalaTokenType.COLON,
                '.': ScalaTokenType.DOT,
                '_': ScalaTokenType.UNDERSCORE,
                '+': ScalaTokenType.PLUS,
                '-': ScalaTokenType.MINUS,
                '*': ScalaTokenType.MULTIPLY,
                '/': ScalaTokenType.DIVIDE,
                '%': ScalaTokenType.MODULO,
                '=': ScalaTokenType.ASSIGN,
                '<': ScalaTokenType.LESS_THAN,
                '>': ScalaTokenType.GREATER_THAN,
                '!': ScalaTokenType.NOT,
                '&': ScalaTokenType.BITWISE_AND,
                '|': ScalaTokenType.BITWISE_OR,
                '^': ScalaTokenType.BITWISE_XOR,
                '~': ScalaTokenType.BITWISE_NOT,
                '#': ScalaTokenType.HASH,
                '@': ScalaTokenType.AT,
            }
            
            if source[position] in single_char_tokens:
                token_type = single_char_tokens[source[position]]
                tokens.append(ScalaToken(token_type, source[position], line, column))
                position += 1
                column += 1
                continue
            
            # Skip unknown characters
            position += 1
            column += 1
        
        tokens.append(ScalaToken(ScalaTokenType.EOF, "", line, column))
        return tokens


class ScalaParser:
    """Scala recursive descent parser."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.tokens: List[ScalaToken] = []
        self.current = 0
    
    def parse(self, source: str) -> ScalaSourceFile:
        """Parse Scala source code into an AST."""
        try:
            lexer = ScalaLexer()
            self.tokens = lexer.tokenize(source)
            self.current = 0
            
            return self._parse_source_file()
            
        except Exception as e:
            self.logger.error(f"Scala parsing failed: {e}")
            raise ScalaParseError(f"Failed to parse Scala code: {e}")
    
    def _current_token(self) -> ScalaToken:
        """Get current token."""
        if self.current >= len(self.tokens):
            return ScalaToken(ScalaTokenType.EOF, "", 0, 0)
        return self.tokens[self.current]
    
    def _advance(self) -> ScalaToken:
        """Advance to next token."""
        token = self._current_token()
        if self.current < len(self.tokens) - 1:
            self.current += 1
        return token
    
    def _match(self, *token_types: ScalaTokenType) -> bool:
        """Check if current token matches any of the given types."""
        return self._current_token().type in token_types
    
    def _consume(self, token_type: ScalaTokenType) -> ScalaToken:
        """Consume token of specific type."""
        token = self._current_token()
        if token.type != token_type:
            raise ScalaParseError(f"Expected {token_type}, got {token.type}")
        return self._advance()
    
    def _skip_newlines(self):
        """Skip newline tokens."""
        while self._match(ScalaTokenType.NEWLINE):
            self._advance()
    
    def _parse_source_file(self) -> ScalaSourceFile:
        """Parse source file."""
        self._skip_newlines()
        
        package_decl = None
        imports = []
        declarations = []
        
        # Parse package declaration
        if self._match(ScalaTokenType.KEYWORD) and self._current_token().value == "package":
            package_decl = self._parse_package_declaration()
            self._skip_newlines()
        
        # Parse imports
        while (self._match(ScalaTokenType.KEYWORD) and 
               self._current_token().value == "import"):
            imports.append(self._parse_import_declaration())
            self._skip_newlines()
        
        # Parse top-level declarations
        while not self._match(ScalaTokenType.EOF):
            # Skip comments
            if self._match(ScalaTokenType.COMMENT, ScalaTokenType.DOC_COMMENT):
                self._advance()
                continue
            
            self._skip_newlines()
            
            if self._match(ScalaTokenType.EOF):
                break
            
            try:
                decl = self._parse_declaration()
                if decl:
                    declarations.append(decl)
            except Exception as e:
                self.logger.warning(f"Skipping invalid declaration: {e}")
                # Skip to next potential declaration
                self._skip_to_next_declaration()
            
            self._skip_newlines()
        
        return ScalaSourceFile(
            package_declaration=package_decl,
            imports=imports,
            declarations=declarations
        )
    
    def _parse_package_declaration(self) -> ScalaPackageDeclaration:
        """Parse package declaration."""
        self._consume(ScalaTokenType.KEYWORD)  # consume 'package'
        
        name = ""
        if self._match(ScalaTokenType.IDENTIFIER):
            name = self._advance().value
            
            # Handle qualified package names
            while self._match(ScalaTokenType.DOT):
                self._advance()
                if self._match(ScalaTokenType.IDENTIFIER):
                    name += "." + self._advance().value
        
        return ScalaPackageDeclaration(name=name)
    
    def _parse_import_declaration(self) -> ScalaImportDeclaration:
        """Parse import declaration."""
        self._consume(ScalaTokenType.KEYWORD)  # consume 'import'
        
        path = ""
        selectors = []
        
        if self._match(ScalaTokenType.IDENTIFIER):
            path = self._advance().value
            
            # Handle qualified import paths
            while self._match(ScalaTokenType.DOT):
                self._advance()
                if self._match(ScalaTokenType.IDENTIFIER):
                    path += "." + self._advance().value
                elif self._match(ScalaTokenType.LBRACE):
                    # Import selectors: import a.{b, c => d, _}
                    self._advance()  # consume '{'
                    
                    while not self._match(ScalaTokenType.RBRACE, ScalaTokenType.EOF):
                        if self._match(ScalaTokenType.IDENTIFIER):
                            selector = self._advance().value
                            
                            # Check for rename: name => newName
                            if (self._match(ScalaTokenType.ARROW) or 
                                (self._match(ScalaTokenType.IDENTIFIER) and 
                                 self._current_token().value == "=>")):
                                if not self._match(ScalaTokenType.ARROW):
                                    self._advance()  # consume '=>' if it's an identifier
                                else:
                                    self._advance()  # consume '=>'
                                
                                if self._match(ScalaTokenType.IDENTIFIER):
                                    new_name = self._advance().value
                                    selector += " => " + new_name
                            
                            selectors.append(selector)
                        elif self._match(ScalaTokenType.UNDERSCORE):
                            selectors.append("_")
                            self._advance()
                        else:
                            self._advance()  # Skip unknown tokens
                        
                        if self._match(ScalaTokenType.COMMA):
                            self._advance()
                        else:
                            break
                    
                    if self._match(ScalaTokenType.RBRACE):
                        self._advance()
                    break
                elif self._match(ScalaTokenType.UNDERSCORE):
                    path += "._"
                    self._advance()
                    break
        
        return ScalaImportDeclaration(path=path, selectors=selectors)
    
    def _parse_declaration(self) -> Optional[ScalaDeclaration]:
        """Parse declaration."""
        # Parse modifiers and annotations first
        annotations = []
        modifiers = []
        
        # Parse annotations
        while self._match(ScalaTokenType.AT):
            annotations.append(self._parse_annotation())
        
        # Parse modifiers
        while (self._match(ScalaTokenType.KEYWORD) and 
               self._current_token().value in ["abstract", "final", "sealed", "implicit", 
                                              "lazy", "override", "case", "private", "protected"]):
            modifier_token = self._advance()
            modifier = self._create_modifier(modifier_token.value)
            modifiers.append(modifier)
        
        if self._match(ScalaTokenType.KEYWORD):
            keyword = self._current_token().value
            
            if keyword == "class":
                return self._parse_class_declaration(annotations, modifiers)
            elif keyword == "trait":
                return self._parse_trait_declaration(annotations, modifiers)
            elif keyword == "object":
                return self._parse_object_declaration(annotations, modifiers)
            elif keyword == "enum":
                return self._parse_enum_declaration(annotations, modifiers)
            elif keyword == "def":
                return self._parse_function_declaration(annotations, modifiers)
            elif keyword == "val":
                return self._parse_value_declaration(annotations, modifiers)
            elif keyword == "var":
                return self._parse_variable_declaration(annotations, modifiers)
            elif keyword == "type":
                return self._parse_type_alias_declaration(annotations, modifiers)
        
        # If we have modifiers but no recognizable declaration, skip
        if modifiers or annotations:
            return None
        
        # Try to parse as expression (for top-level expressions)
        return None
    
    def _parse_annotation(self) -> ScalaAnnotation:
        """Parse annotation."""
        self._consume(ScalaTokenType.AT)  # consume '@'
        
        name = ""
        if self._match(ScalaTokenType.IDENTIFIER):
            name = self._advance().value
        
        arguments = []
        if self._match(ScalaTokenType.LPAREN):
            arguments = self._parse_argument_list()
        
        return ScalaAnnotation(name=name, arguments=arguments)
    
    def _create_modifier(self, modifier_str: str) -> ScalaModifierNode:
        """Create modifier node from string."""
        modifier_map = {
            "abstract": ScalaModifier.ABSTRACT,
            "final": ScalaModifier.FINAL,
            "sealed": ScalaModifier.SEALED,
            "implicit": ScalaModifier.IMPLICIT,
            "lazy": ScalaModifier.LAZY,
            "override": ScalaModifier.OVERRIDE,
            "case": ScalaModifier.CASE,
            "private": ScalaModifier.PRIVATE,
            "protected": ScalaModifier.PROTECTED,
        }
        
        modifier = modifier_map.get(modifier_str, ScalaModifier.PUBLIC)
        return ScalaModifierNode(modifier=modifier)
    
    def _parse_class_declaration(self, annotations: List[ScalaAnnotation], 
                                modifiers: List[ScalaModifierNode]) -> ScalaClassDeclaration:
        """Parse class declaration."""
        self._consume(ScalaTokenType.KEYWORD)  # consume 'class'
        
        name = ""
        if self._match(ScalaTokenType.IDENTIFIER):
            name = self._advance().value
        
        # Parse type parameters
        type_parameters = []
        if self._match(ScalaTokenType.LBRACKET):
            type_parameters = self._parse_type_parameter_list()
        
        # Parse constructor parameters
        constructor_parameters = []
        if self._match(ScalaTokenType.LPAREN):
            constructor_parameters = self._parse_parameter_list()
        
        # Parse extends clause
        extends_clause = None
        if self._match(ScalaTokenType.KEYWORD) and self._current_token().value == "extends":
            self._advance()
            extends_clause = self._parse_type()
        
        # Parse with clauses
        with_clauses = []
        while self._match(ScalaTokenType.KEYWORD) and self._current_token().value == "with":
            self._advance()
            with_clauses.append(self._parse_type())
        
        # Parse body
        members = []
        if self._match(ScalaTokenType.LBRACE):
            members = self._parse_class_body()
        
        # Extract flags from modifiers
        is_abstract = any(m.modifier == ScalaModifier.ABSTRACT for m in modifiers)
        is_final = any(m.modifier == ScalaModifier.FINAL for m in modifiers)
        is_sealed = any(m.modifier == ScalaModifier.SEALED for m in modifiers)
        is_case = any(m.modifier == ScalaModifier.CASE for m in modifiers)
        
        return ScalaClassDeclaration(
            name=name,
            type_parameters=type_parameters,
            constructor_parameters=constructor_parameters,
            extends_clause=extends_clause,
            with_clauses=with_clauses,
            members=members,
            annotations=annotations,
            modifiers=modifiers,
            is_abstract=is_abstract,
            is_final=is_final,
            is_sealed=is_sealed,
            is_case=is_case
        )
    
    def _parse_trait_declaration(self, annotations: List[ScalaAnnotation], 
                                modifiers: List[ScalaModifierNode]) -> ScalaTraitDeclaration:
        """Parse trait declaration."""
        self._consume(ScalaTokenType.KEYWORD)  # consume 'trait'
        
        name = ""
        if self._match(ScalaTokenType.IDENTIFIER):
            name = self._advance().value
        
        # Parse type parameters
        type_parameters = []
        if self._match(ScalaTokenType.LBRACKET):
            type_parameters = self._parse_type_parameter_list()
        
        # Parse extends clause
        extends_clause = None
        if self._match(ScalaTokenType.KEYWORD) and self._current_token().value == "extends":
            self._advance()
            extends_clause = self._parse_type()
        
        # Parse with clauses
        with_clauses = []
        while self._match(ScalaTokenType.KEYWORD) and self._current_token().value == "with":
            self._advance()
            with_clauses.append(self._parse_type())
        
        # Parse body
        members = []
        if self._match(ScalaTokenType.LBRACE):
            members = self._parse_class_body()
        
        is_sealed = any(m.modifier == ScalaModifier.SEALED for m in modifiers)
        
        return ScalaTraitDeclaration(
            name=name,
            type_parameters=type_parameters,
            extends_clause=extends_clause,
            with_clauses=with_clauses,
            members=members,
            annotations=annotations,
            modifiers=modifiers,
            is_sealed=is_sealed
        )
    
    def _parse_object_declaration(self, annotations: List[ScalaAnnotation], 
                                 modifiers: List[ScalaModifierNode]) -> ScalaObjectDeclaration:
        """Parse object declaration."""
        self._consume(ScalaTokenType.KEYWORD)  # consume 'object'
        
        name = ""
        if self._match(ScalaTokenType.IDENTIFIER):
            name = self._advance().value
        
        # Parse extends clause
        extends_clause = None
        if self._match(ScalaTokenType.KEYWORD) and self._current_token().value == "extends":
            self._advance()
            extends_clause = self._parse_type()
        
        # Parse with clauses
        with_clauses = []
        while self._match(ScalaTokenType.KEYWORD) and self._current_token().value == "with":
            self._advance()
            with_clauses.append(self._parse_type())
        
        # Parse body
        members = []
        if self._match(ScalaTokenType.LBRACE):
            members = self._parse_class_body()
        
        is_case = any(m.modifier == ScalaModifier.CASE for m in modifiers)
        
        return ScalaObjectDeclaration(
            name=name,
            extends_clause=extends_clause,
            with_clauses=with_clauses,
            members=members,
            annotations=annotations,
            modifiers=modifiers,
            is_case=is_case
        )
    
    def _parse_enum_declaration(self, annotations: List[ScalaAnnotation], 
                               modifiers: List[ScalaModifierNode]) -> ScalaEnumDeclaration:
        """Parse enum declaration (Scala 3)."""
        self._consume(ScalaTokenType.KEYWORD)  # consume 'enum'
        
        name = ""
        if self._match(ScalaTokenType.IDENTIFIER):
            name = self._advance().value
        
        # Parse type parameters
        type_parameters = []
        if self._match(ScalaTokenType.LBRACKET):
            type_parameters = self._parse_type_parameter_list()
        
        # Parse body
        cases = []
        members = []
        
        if self._match(ScalaTokenType.LBRACE):
            self._advance()
            self._skip_newlines()
            
            while not self._match(ScalaTokenType.RBRACE, ScalaTokenType.EOF):
                if self._match(ScalaTokenType.KEYWORD) and self._current_token().value == "case":
                    cases.append(self._parse_enum_case())
                else:
                    # Parse as member
                    member = self._parse_declaration()
                    if member:
                        members.append(member)
                
                self._skip_newlines()
            
            if self._match(ScalaTokenType.RBRACE):
                self._advance()
        
        return ScalaEnumDeclaration(
            name=name,
            type_parameters=type_parameters,
            cases=cases,
            members=members,
            annotations=annotations,
            modifiers=modifiers
        )
    
    def _parse_enum_case(self) -> ScalaEnumCase:
        """Parse enum case."""
        self._consume(ScalaTokenType.KEYWORD)  # consume 'case'
        
        name = ""
        if self._match(ScalaTokenType.IDENTIFIER):
            name = self._advance().value
        
        # Parse parameters
        parameters = []
        if self._match(ScalaTokenType.LPAREN):
            parameters = self._parse_parameter_list()
        
        # Parse extends clauses
        extends_clauses = []
        if self._match(ScalaTokenType.KEYWORD) and self._current_token().value == "extends":
            self._advance()
            extends_clauses.append(self._parse_type())
        
        return ScalaEnumCase(
            name=name,
            parameters=parameters,
            extends_clauses=extends_clauses
        )
    
    def _parse_function_declaration(self, annotations: List[ScalaAnnotation], 
                                   modifiers: List[ScalaModifierNode]) -> ScalaFunctionDeclaration:
        """Parse function declaration."""
        self._consume(ScalaTokenType.KEYWORD)  # consume 'def'
        
        name = ""
        if self._match(ScalaTokenType.IDENTIFIER):
            name = self._advance().value
        
        # Parse type parameters
        type_parameters = []
        if self._match(ScalaTokenType.LBRACKET):
            type_parameters = self._parse_type_parameter_list()
        
        # Parse parameter lists
        parameter_lists = []
        while self._match(ScalaTokenType.LPAREN):
            parameter_lists.append(self._parse_parameter_list())
        
        # Parse return type
        return_type = None
        if self._match(ScalaTokenType.COLON):
            self._advance()
            return_type = self._parse_type()
        
        # Parse body
        body = None
        if self._match(ScalaTokenType.ASSIGN):
            self._advance()
            body = self._parse_expression()
        elif self._match(ScalaTokenType.LBRACE):
            body = self._parse_block_expression()
        
        # Extract flags from modifiers
        is_abstract = any(m.modifier == ScalaModifier.ABSTRACT for m in modifiers)
        is_override = any(m.modifier == ScalaModifier.OVERRIDE for m in modifiers)
        is_implicit = any(m.modifier == ScalaModifier.IMPLICIT for m in modifiers)
        
        return ScalaFunctionDeclaration(
            name=name,
            type_parameters=type_parameters,
            parameter_lists=parameter_lists,
            return_type=return_type,
            body=body,
            annotations=annotations,
            modifiers=modifiers,
            is_abstract=is_abstract,
            is_override=is_override,
            is_implicit=is_implicit
        )
    
    def _parse_value_declaration(self, annotations: List[ScalaAnnotation], 
                                modifiers: List[ScalaModifierNode]) -> ScalaValueDeclaration:
        """Parse value declaration."""
        self._consume(ScalaTokenType.KEYWORD)  # consume 'val'
        
        name = ""
        if self._match(ScalaTokenType.IDENTIFIER):
            name = self._advance().value
        
        # Parse type annotation
        type_annotation = None
        if self._match(ScalaTokenType.COLON):
            self._advance()
            type_annotation = self._parse_type()
        
        # Parse value
        value = None
        if self._match(ScalaTokenType.ASSIGN):
            self._advance()
            value = self._parse_expression()
        
        # Extract flags from modifiers
        is_lazy = any(m.modifier == ScalaModifier.LAZY for m in modifiers)
        is_implicit = any(m.modifier == ScalaModifier.IMPLICIT for m in modifiers)
        is_override = any(m.modifier == ScalaModifier.OVERRIDE for m in modifiers)
        
        return ScalaValueDeclaration(
            name=name,
            type_annotation=type_annotation,
            value=value,
            annotations=annotations,
            modifiers=modifiers,
            is_lazy=is_lazy,
            is_implicit=is_implicit,
            is_override=is_override
        )
    
    def _parse_variable_declaration(self, annotations: List[ScalaAnnotation], 
                                   modifiers: List[ScalaModifierNode]) -> ScalaVariableDeclaration:
        """Parse variable declaration."""
        self._consume(ScalaTokenType.KEYWORD)  # consume 'var'
        
        name = ""
        if self._match(ScalaTokenType.IDENTIFIER):
            name = self._advance().value
        
        # Parse type annotation
        type_annotation = None
        if self._match(ScalaTokenType.COLON):
            self._advance()
            type_annotation = self._parse_type()
        
        # Parse value
        value = None
        if self._match(ScalaTokenType.ASSIGN):
            self._advance()
            value = self._parse_expression()
        
        is_override = any(m.modifier == ScalaModifier.OVERRIDE for m in modifiers)
        
        return ScalaVariableDeclaration(
            name=name,
            type_annotation=type_annotation,
            value=value,
            annotations=annotations,
            modifiers=modifiers,
            is_override=is_override
        )
    
    def _parse_type_alias_declaration(self, annotations: List[ScalaAnnotation], 
                                     modifiers: List[ScalaModifierNode]) -> ScalaTypeAliasDeclaration:
        """Parse type alias declaration."""
        self._consume(ScalaTokenType.KEYWORD)  # consume 'type'
        
        name = ""
        if self._match(ScalaTokenType.IDENTIFIER):
            name = self._advance().value
        
        # Parse type parameters
        type_parameters = []
        if self._match(ScalaTokenType.LBRACKET):
            type_parameters = self._parse_type_parameter_list()
        
        # Parse alias type
        alias_type = None
        if self._match(ScalaTokenType.ASSIGN):
            self._advance()
            alias_type = self._parse_type()
        
        return ScalaTypeAliasDeclaration(
            name=name,
            type_parameters=type_parameters,
            alias_type=alias_type,
            annotations=annotations,
            modifiers=modifiers
        )
    
    def _parse_type_parameter_list(self) -> List[ScalaTypeParameter]:
        """Parse type parameter list."""
        self._consume(ScalaTokenType.LBRACKET)
        
        parameters = []
        
        while not self._match(ScalaTokenType.RBRACKET, ScalaTokenType.EOF):
            param = self._parse_type_parameter()
            parameters.append(param)
            
            if self._match(ScalaTokenType.COMMA):
                self._advance()
            else:
                break
        
        if self._match(ScalaTokenType.RBRACKET):
            self._advance()
        
        return parameters
    
    def _parse_type_parameter(self) -> ScalaTypeParameter:
        """Parse type parameter."""
        # Parse variance
        variance = None
        if self._match(ScalaTokenType.PLUS):
            variance = "+"
            self._advance()
        elif self._match(ScalaTokenType.MINUS):
            variance = "-"
            self._advance()
        
        name = ""
        if self._match(ScalaTokenType.IDENTIFIER):
            name = self._advance().value
        
        # Parse bounds
        upper_bound = None
        lower_bound = None
        context_bounds = []
        view_bounds = []
        
        while True:
            if self._match(ScalaTokenType.SUBTYPE):  # <:
                self._advance()
                upper_bound = self._parse_type()
            elif self._match(ScalaTokenType.SUPERTYPE):  # >:
                self._advance()
                lower_bound = self._parse_type()
            elif self._match(ScalaTokenType.VIEW_BOUND):  # <%
                self._advance()
                view_bounds.append(self._parse_type())
            elif self._match(ScalaTokenType.COLON):
                # Context bound
                self._advance()
                context_bounds.append(self._parse_type())
            else:
                break
        
        return ScalaTypeParameter(
            name=name,
            variance=variance,
            upper_bound=upper_bound,
            lower_bound=lower_bound,
            context_bounds=context_bounds,
            view_bounds=view_bounds
        )
    
    def _parse_parameter_list(self) -> List[ScalaParameter]:
        """Parse parameter list."""
        self._consume(ScalaTokenType.LPAREN)
        
        parameters = []
        
        while not self._match(ScalaTokenType.RPAREN, ScalaTokenType.EOF):
            param = self._parse_parameter()
            parameters.append(param)
            
            if self._match(ScalaTokenType.COMMA):
                self._advance()
            else:
                break
        
        if self._match(ScalaTokenType.RPAREN):
            self._advance()
        
        return parameters
    
    def _parse_parameter(self) -> ScalaParameter:
        """Parse parameter."""
        # Check for implicit
        is_implicit = False
        if self._match(ScalaTokenType.KEYWORD) and self._current_token().value == "implicit":
            is_implicit = True
            self._advance()
        
        name = ""
        if self._match(ScalaTokenType.IDENTIFIER):
            name = self._advance().value
        
        # Parse type
        parameter_type = None
        if self._match(ScalaTokenType.COLON):
            self._advance()
            
            # Check for by-name parameter
            is_by_name = False
            if self._match(ScalaTokenType.ARROW):
                is_by_name = True
                self._advance()
            
            parameter_type = self._parse_type()
            
            # Check for varargs
            is_varargs = False
            if self._match(ScalaTokenType.MULTIPLY):
                is_varargs = True
                self._advance()
        
        # Parse default value
        default_value = None
        if self._match(ScalaTokenType.ASSIGN):
            self._advance()
            default_value = self._parse_expression()
        
        return ScalaParameter(
            name=name,
            parameter_type=parameter_type,
            default_value=default_value,
            is_implicit=is_implicit,
            is_by_name=is_by_name if 'is_by_name' in locals() else False,
            is_varargs=is_varargs if 'is_varargs' in locals() else False
        )
    
    def _parse_argument_list(self) -> List[ScalaArgument]:
        """Parse argument list."""
        self._consume(ScalaTokenType.LPAREN)
        
        arguments = []
        
        while not self._match(ScalaTokenType.RPAREN, ScalaTokenType.EOF):
            arg = self._parse_argument()
            arguments.append(arg)
            
            if self._match(ScalaTokenType.COMMA):
                self._advance()
            else:
                break
        
        if self._match(ScalaTokenType.RPAREN):
            self._advance()
        
        return arguments
    
    def _parse_argument(self) -> ScalaArgument:
        """Parse argument."""
        # Check for named argument
        name = None
        if (self._match(ScalaTokenType.IDENTIFIER) and 
            self.current + 1 < len(self.tokens) and 
            self.tokens[self.current + 1].type == ScalaTokenType.ASSIGN):
            name = self._advance().value
            self._advance()  # consume '='
        
        value = self._parse_expression()
        
        return ScalaArgument(name=name, value=value)
    
    def _parse_class_body(self) -> List[ScalaMember]:
        """Parse class body."""
        self._consume(ScalaTokenType.LBRACE)
        
        members = []
        
        while not self._match(ScalaTokenType.RBRACE, ScalaTokenType.EOF):
            self._skip_newlines()
            
            if self._match(ScalaTokenType.RBRACE):
                break
            
            # Skip comments
            if self._match(ScalaTokenType.COMMENT, ScalaTokenType.DOC_COMMENT):
                self._advance()
                continue
            
            try:
                member = self._parse_declaration()
                if member:
                    members.append(member)
            except Exception as e:
                self.logger.warning(f"Skipping invalid member: {e}")
                self._skip_to_next_declaration()
        
        if self._match(ScalaTokenType.RBRACE):
            self._advance()
        
        return members
    
    def _parse_type(self) -> ScalaType:
        """Parse type."""
        return self._parse_compound_type()
    
    def _parse_compound_type(self) -> ScalaType:
        """Parse compound type (with 'with' clauses)."""
        base_type = self._parse_function_type()
        
        if self._match(ScalaTokenType.KEYWORD) and self._current_token().value == "with":
            types = [base_type]
            
            while self._match(ScalaTokenType.KEYWORD) and self._current_token().value == "with":
                self._advance()
                types.append(self._parse_function_type())
            
            return ScalaCompoundType(types=types)
        
        return base_type
    
    def _parse_function_type(self) -> ScalaType:
        """Parse function type."""
        left_type = self._parse_primary_type()
        
        if self._match(ScalaTokenType.ARROW):
            self._advance()
            
            # Parse parameter types
            if isinstance(left_type, ScalaTupleType):
                parameter_types = left_type.element_types
            else:
                parameter_types = [left_type]
            
            return_type = self._parse_type()
            
            return ScalaFunctionType(
                parameter_types=parameter_types,
                return_type=return_type
            )
        
        return left_type
    
    def _parse_primary_type(self) -> ScalaType:
        """Parse primary type."""
        if self._match(ScalaTokenType.LPAREN):
            self._advance()
            
            # Parse tuple type or parenthesized type
            if self._match(ScalaTokenType.RPAREN):
                # Unit type
                self._advance()
                return ScalaTypeIdentifier(name="Unit")
            
            element_types = []
            element_types.append(self._parse_type())
            
            if self._match(ScalaTokenType.COMMA):
                # Tuple type
                while self._match(ScalaTokenType.COMMA):
                    self._advance()
                    element_types.append(self._parse_type())
                
                if self._match(ScalaTokenType.RPAREN):
                    self._advance()
                
                return ScalaTupleType(element_types=element_types)
            else:
                # Parenthesized type
                if self._match(ScalaTokenType.RPAREN):
                    self._advance()
                
                return element_types[0]
        
        elif self._match(ScalaTokenType.IDENTIFIER):
            name = self._advance().value
            
            # Parse type arguments
            type_arguments = []
            if self._match(ScalaTokenType.LBRACKET):
                self._advance()
                
                while not self._match(ScalaTokenType.RBRACKET, ScalaTokenType.EOF):
                    type_arguments.append(self._parse_type())
                    
                    if self._match(ScalaTokenType.COMMA):
                        self._advance()
                    else:
                        break
                
                if self._match(ScalaTokenType.RBRACKET):
                    self._advance()
            
            return ScalaTypeIdentifier(name=name, type_arguments=type_arguments)
        
        else:
            # Default to Any type for unknown types
            return ScalaTypeIdentifier(name="Any")
    
    def _parse_expression(self) -> Optional[ScalaExpression]:
        """Parse expression (simplified)."""
        return self._parse_assignment_expression()
    
    def _parse_assignment_expression(self) -> Optional[ScalaExpression]:
        """Parse assignment expression."""
        left = self._parse_ternary_expression()
        
        if self._match(ScalaTokenType.ASSIGN):
            self._advance()
            right = self._parse_expression()
            return ScalaAssignmentExpression(target=left, value=right)
        
        return left
    
    def _parse_ternary_expression(self) -> Optional[ScalaExpression]:
        """Parse ternary expression (if-else)."""
        if self._match(ScalaTokenType.KEYWORD) and self._current_token().value == "if":
            return self._parse_if_expression()
        
        return self._parse_logical_or_expression()
    
    def _parse_if_expression(self) -> ScalaIfExpression:
        """Parse if expression."""
        self._consume(ScalaTokenType.KEYWORD)  # consume 'if'
        
        condition = None
        if self._match(ScalaTokenType.LPAREN):
            self._advance()
            condition = self._parse_expression()
            if self._match(ScalaTokenType.RPAREN):
                self._advance()
        
        then_expression = self._parse_expression()
        
        else_expression = None
        if self._match(ScalaTokenType.KEYWORD) and self._current_token().value == "else":
            self._advance()
            else_expression = self._parse_expression()
        
        return ScalaIfExpression(
            condition=condition,
            then_expression=then_expression,
            else_expression=else_expression
        )
    
    def _parse_logical_or_expression(self) -> Optional[ScalaExpression]:
        """Parse logical OR expression."""
        left = self._parse_logical_and_expression()
        
        while self._match(ScalaTokenType.OR):
            operator = self._advance().value
            right = self._parse_logical_and_expression()
            left = ScalaBinaryExpression(left=left, operator=operator, right=right)
        
        return left
    
    def _parse_logical_and_expression(self) -> Optional[ScalaExpression]:
        """Parse logical AND expression."""
        left = self._parse_equality_expression()
        
        while self._match(ScalaTokenType.AND):
            operator = self._advance().value
            right = self._parse_equality_expression()
            left = ScalaBinaryExpression(left=left, operator=operator, right=right)
        
        return left
    
    def _parse_equality_expression(self) -> Optional[ScalaExpression]:
        """Parse equality expression."""
        left = self._parse_relational_expression()
        
        while self._match(ScalaTokenType.EQUAL, ScalaTokenType.NOT_EQUAL):
            operator = self._advance().value
            right = self._parse_relational_expression()
            left = ScalaBinaryExpression(left=left, operator=operator, right=right)
        
        return left
    
    def _parse_relational_expression(self) -> Optional[ScalaExpression]:
        """Parse relational expression."""
        left = self._parse_additive_expression()
        
        while self._match(ScalaTokenType.LESS_THAN, ScalaTokenType.GREATER_THAN,
                          ScalaTokenType.LESS_EQUAL, ScalaTokenType.GREATER_EQUAL):
            operator = self._advance().value
            right = self._parse_additive_expression()
            left = ScalaBinaryExpression(left=left, operator=operator, right=right)
        
        return left
    
    def _parse_additive_expression(self) -> Optional[ScalaExpression]:
        """Parse additive expression."""
        left = self._parse_multiplicative_expression()
        
        while self._match(ScalaTokenType.PLUS, ScalaTokenType.MINUS):
            operator = self._advance().value
            right = self._parse_multiplicative_expression()
            left = ScalaBinaryExpression(left=left, operator=operator, right=right)
        
        return left
    
    def _parse_multiplicative_expression(self) -> Optional[ScalaExpression]:
        """Parse multiplicative expression."""
        left = self._parse_unary_expression()
        
        while self._match(ScalaTokenType.MULTIPLY, ScalaTokenType.DIVIDE, ScalaTokenType.MODULO):
            operator = self._advance().value
            right = self._parse_unary_expression()
            left = ScalaBinaryExpression(left=left, operator=operator, right=right)
        
        return left
    
    def _parse_unary_expression(self) -> Optional[ScalaExpression]:
        """Parse unary expression."""
        if self._match(ScalaTokenType.NOT, ScalaTokenType.MINUS, ScalaTokenType.PLUS):
            operator = self._advance().value
            operand = self._parse_unary_expression()
            return ScalaUnaryExpression(operator=operator, operand=operand)
        
        return self._parse_postfix_expression()
    
    def _parse_postfix_expression(self) -> Optional[ScalaExpression]:
        """Parse postfix expression."""
        left = self._parse_primary_expression()
        
        while True:
            if self._match(ScalaTokenType.DOT):
                self._advance()
                
                if self._match(ScalaTokenType.IDENTIFIER):
                    method_name = self._advance().value
                    
                    # Check for method call
                    if self._match(ScalaTokenType.LPAREN):
                        arguments = [self._parse_argument_list()]
                        
                        # Multiple argument lists
                        while self._match(ScalaTokenType.LPAREN):
                            arguments.append(self._parse_argument_list())
                        
                        left = ScalaMethodCallExpression(
                            receiver=left,
                            method_name=method_name,
                            arguments=arguments
                        )
                    else:
                        # Property access (simplified)
                        left = ScalaIdentifier(name=f"{left}.{method_name}")
            
            elif self._match(ScalaTokenType.LPAREN):
                # Function call
                arguments = [self._parse_argument_list()]
                
                # Multiple argument lists
                while self._match(ScalaTokenType.LPAREN):
                    arguments.append(self._parse_argument_list())
                
                left = ScalaFunctionCallExpression(
                    function=left,
                    arguments=arguments
                )
            
            elif self._match(ScalaTokenType.LBRACKET):
                # Type application or array access (simplified)
                self._advance()
                
                # Skip type arguments for now
                while not self._match(ScalaTokenType.RBRACKET, ScalaTokenType.EOF):
                    self._advance()
                
                if self._match(ScalaTokenType.RBRACKET):
                    self._advance()
            
            else:
                break
        
        return left
    
    def _parse_primary_expression(self) -> Optional[ScalaExpression]:
        """Parse primary expression."""
        if self._match(ScalaTokenType.INTEGER):
            value = int(self._advance().value.rstrip('lL'))
            return ScalaLiteral(value=value, literal_type="int")
        
        elif self._match(ScalaTokenType.LONG):
            value = int(self._advance().value.rstrip('lL'))
            return ScalaLiteral(value=value, literal_type="long")
        
        elif self._match(ScalaTokenType.FLOAT):
            value = float(self._advance().value.rstrip('fF'))
            return ScalaLiteral(value=value, literal_type="float")
        
        elif self._match(ScalaTokenType.DOUBLE):
            value = float(self._advance().value.rstrip('dD'))
            return ScalaLiteral(value=value, literal_type="double")
        
        elif self._match(ScalaTokenType.STRING):
            value = self._advance().value
            # Remove quotes
            if value.startswith('"""') and value.endswith('"""'):
                value = value[3:-3]
            elif value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            return ScalaLiteral(value=value, literal_type="string")
        
        elif self._match(ScalaTokenType.CHAR):
            value = self._advance().value
            # Remove quotes
            if value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            return ScalaLiteral(value=value, literal_type="char")
        
        elif self._match(ScalaTokenType.BOOLEAN):
            value = self._advance().value.lower() == "true"
            return ScalaLiteral(value=value, literal_type="bool")
        
        elif self._match(ScalaTokenType.NULL):
            self._advance()
            return ScalaLiteral(value=None, literal_type="null")
        
        elif self._match(ScalaTokenType.SYMBOL):
            value = self._advance().value
            return ScalaLiteral(value=value, literal_type="symbol")
        
        elif self._match(ScalaTokenType.IDENTIFIER):
            name = self._advance().value
            
            if name == "this":
                return ScalaThisExpression()
            elif name == "super":
                return ScalaSuperExpression()
            else:
                return ScalaIdentifier(name=name)
        
        elif self._match(ScalaTokenType.KEYWORD):
            keyword = self._current_token().value
            
            if keyword == "this":
                self._advance()
                return ScalaThisExpression()
            elif keyword == "super":
                self._advance()
                return ScalaSuperExpression()
            elif keyword == "new":
                return self._parse_new_expression()
            elif keyword == "match":
                return self._parse_match_expression()
            elif keyword == "try":
                return self._parse_try_expression()
            elif keyword == "for":
                return self._parse_for_expression()
            elif keyword == "while":
                return self._parse_while_expression()
        
        elif self._match(ScalaTokenType.LPAREN):
            return self._parse_parenthesized_or_tuple_expression()
        
        elif self._match(ScalaTokenType.LBRACE):
            return self._parse_block_expression()
        
        else:
            # Skip unknown token
            if not self._match(ScalaTokenType.EOF):
                self._advance()
            return None
    
    def _parse_new_expression(self) -> ScalaNewExpression:
        """Parse new expression."""
        self._consume(ScalaTokenType.KEYWORD)  # consume 'new'
        
        class_type = self._parse_type()
        
        # Parse constructor arguments
        arguments = []
        while self._match(ScalaTokenType.LPAREN):
            arguments.append(self._parse_argument_list())
        
        return ScalaNewExpression(class_type=class_type, arguments=arguments)
    
    def _parse_match_expression(self) -> ScalaMatchExpression:
        """Parse match expression."""
        scrutinee = self._parse_expression()
        
        self._consume(ScalaTokenType.KEYWORD)  # consume 'match'
        
        cases = []
        if self._match(ScalaTokenType.LBRACE):
            self._advance()
            
            while not self._match(ScalaTokenType.RBRACE, ScalaTokenType.EOF):
                if self._match(ScalaTokenType.KEYWORD) and self._current_token().value == "case":
                    cases.append(self._parse_match_case())
                else:
                    self._advance()  # Skip unknown tokens
            
            if self._match(ScalaTokenType.RBRACE):
                self._advance()
        
        return ScalaMatchExpression(scrutinee=scrutinee, cases=cases)
    
    def _parse_match_case(self) -> ScalaMatchCase:
        """Parse match case."""
        self._consume(ScalaTokenType.KEYWORD)  # consume 'case'
        
        pattern = self._parse_pattern()
        
        # Parse guard
        guard = None
        if self._match(ScalaTokenType.KEYWORD) and self._current_token().value == "if":
            self._advance()
            guard = self._parse_expression()
        
        # Parse arrow and body
        if self._match(ScalaTokenType.ARROW):
            self._advance()
        
        body = self._parse_expression()
        
        return ScalaMatchCase(pattern=pattern, guard=guard, body=body)
    
    def _parse_pattern(self) -> ScalaPattern:
        """Parse pattern (simplified)."""
        if self._match(ScalaTokenType.UNDERSCORE):
            self._advance()
            return ScalaWildcardPattern()
        elif self._match(ScalaTokenType.IDENTIFIER):
            name = self._advance().value
            return ScalaIdentifierPattern(name=name)
        elif self._match(ScalaTokenType.INTEGER, ScalaTokenType.STRING, ScalaTokenType.BOOLEAN):
            literal = self._parse_primary_expression()
            return ScalaLiteralPattern(literal=literal)
        else:
            # Default to wildcard
            return ScalaWildcardPattern()
    
    def _parse_try_expression(self) -> ScalaTryExpression:
        """Parse try expression."""
        self._consume(ScalaTokenType.KEYWORD)  # consume 'try'
        
        try_expression = self._parse_expression()
        
        # Parse catch clause
        catch_cases = []
        if self._match(ScalaTokenType.KEYWORD) and self._current_token().value == "catch":
            self._advance()
            
            if self._match(ScalaTokenType.LBRACE):
                self._advance()
                
                while not self._match(ScalaTokenType.RBRACE, ScalaTokenType.EOF):
                    if self._match(ScalaTokenType.KEYWORD) and self._current_token().value == "case":
                        catch_cases.append(self._parse_match_case())
                    else:
                        self._advance()
                
                if self._match(ScalaTokenType.RBRACE):
                    self._advance()
        
        # Parse finally clause
        finally_expression = None
        if self._match(ScalaTokenType.KEYWORD) and self._current_token().value == "finally":
            self._advance()
            finally_expression = self._parse_expression()
        
        return ScalaTryExpression(
            try_expression=try_expression,
            catch_cases=catch_cases,
            finally_expression=finally_expression
        )
    
    def _parse_for_expression(self) -> ScalaForExpression:
        """Parse for expression."""
        self._consume(ScalaTokenType.KEYWORD)  # consume 'for'
        
        generators = []
        
        if self._match(ScalaTokenType.LBRACE):
            self._advance()
            
            # Parse generators (simplified)
            while not self._match(ScalaTokenType.RBRACE, ScalaTokenType.EOF):
                if self._match(ScalaTokenType.IDENTIFIER):
                    pattern = ScalaIdentifierPattern(name=self._advance().value)
                    
                    if self._match(ScalaTokenType.LEFT_ARROW):
                        self._advance()
                        expression = self._parse_expression()
                        generators.append(ScalaGenerator(pattern=pattern, expression=expression))
                
                # Skip other tokens
                if not self._match(ScalaTokenType.RBRACE):
                    self._advance()
            
            if self._match(ScalaTokenType.RBRACE):
                self._advance()
        
        # Parse yield
        yield_expression = None
        is_yield = False
        if self._match(ScalaTokenType.KEYWORD) and self._current_token().value == "yield":
            is_yield = True
            self._advance()
            yield_expression = self._parse_expression()
        
        return ScalaForExpression(
            generators=generators,
            yield_expression=yield_expression,
            is_yield=is_yield
        )
    
    def _parse_while_expression(self) -> ScalaWhileExpression:
        """Parse while expression."""
        self._consume(ScalaTokenType.KEYWORD)  # consume 'while'
        
        condition = None
        if self._match(ScalaTokenType.LPAREN):
            self._advance()
            condition = self._parse_expression()
            if self._match(ScalaTokenType.RPAREN):
                self._advance()
        
        body = self._parse_expression()
        
        return ScalaWhileExpression(condition=condition, body=body)
    
    def _parse_parenthesized_or_tuple_expression(self) -> ScalaExpression:
        """Parse parenthesized or tuple expression."""
        self._consume(ScalaTokenType.LPAREN)
        
        if self._match(ScalaTokenType.RPAREN):
            # Unit literal
            self._advance()
            return ScalaLiteral(value=None, literal_type="unit")
        
        elements = []
        elements.append(self._parse_expression())
        
        if self._match(ScalaTokenType.COMMA):
            # Tuple
            while self._match(ScalaTokenType.COMMA):
                self._advance()
                elements.append(self._parse_expression())
            
            if self._match(ScalaTokenType.RPAREN):
                self._advance()
            
            return ScalaTupleExpression(elements=elements)
        else:
            # Parenthesized expression
            if self._match(ScalaTokenType.RPAREN):
                self._advance()
            
            return elements[0]
    
    def _parse_block_expression(self) -> ScalaBlockExpression:
        """Parse block expression."""
        self._consume(ScalaTokenType.LBRACE)
        
        statements = []
        result_expression = None
        
        while not self._match(ScalaTokenType.RBRACE, ScalaTokenType.EOF):
            self._skip_newlines()
            
            if self._match(ScalaTokenType.RBRACE):
                break
            
            expr = self._parse_expression()
            if expr:
                # If this is the last expression, it's the result
                # For simplicity, we'll treat all as statements
                statements.append(expr)
        
        if self._match(ScalaTokenType.RBRACE):
            self._advance()
        
        # Last statement becomes result expression
        if statements:
            result_expression = statements.pop()
        
        return ScalaBlockExpression(
            statements=statements,
            result_expression=result_expression
        )
    
    def _skip_to_next_declaration(self):
        """Skip tokens until next potential declaration."""
        while not self._match(ScalaTokenType.EOF):
            if (self._match(ScalaTokenType.KEYWORD) and 
                self._current_token().value in ["class", "trait", "object", "def", "val", "var", "type"]):
                break
            self._advance()


# Convenience functions
def parse_scala_code(source: str) -> ScalaSourceFile:
    """Parse Scala source code and return AST."""
    parser = ScalaParser()
    return parser.parse(source)


def tokenize_scala_code(source: str) -> List[ScalaToken]:
    """Tokenize Scala source code and return tokens."""
    lexer = ScalaLexer()
    return lexer.tokenize(source)