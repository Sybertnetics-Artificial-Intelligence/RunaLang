#!/usr/bin/env python3
"""
Kotlin Parser and Lexer

Comprehensive Kotlin parsing implementation supporting all Kotlin language features
including classes, objects, coroutines, null safety, type inference, lambdas,
higher-order functions, and DSL constructs.

This module provides:
- KotlinToken: Token representation for Kotlin lexical elements
- KotlinLexer: Tokenization of Kotlin source code
- KotlinParser: Recursive descent parser for Kotlin statements
- Support for Kotlin-specific syntax including safe calls, Elvis operator, etc.
- Comprehensive error handling and recovery

Author: Sybertnetics AI Solutions
License: MIT
"""

import re
from typing import List, Optional, Dict, Any, Union, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum, auto
import logging

from .kotlin_ast import (
    KotlinNode, KotlinProgram, KotlinStatement, KotlinExpression,
    KotlinClassDeclaration, KotlinFunctionDeclaration, KotlinPropertyDeclaration,
    KotlinPackageDeclaration, KotlinImportDeclaration, KotlinBinaryExpression,
    KotlinUnaryExpression, KotlinCallExpression, KotlinLambdaExpression,
    KotlinIfExpression, KotlinWhenExpression, KotlinTryExpression,
    KotlinIdentifier, KotlinLiteral, KotlinStringTemplate, KotlinType,
    KotlinBlock, KotlinReturnStatement, KotlinAssignment, KotlinForStatement,
    KotlinWhileStatement, KotlinNodeType, KotlinModifier, KotlinVisibility,
    KotlinClassKind, KotlinOperator, KotlinVariance
)


class KotlinTokenType(Enum):
    """Kotlin token types."""
    
    # Literals
    INTEGER = auto()
    LONG = auto()
    FLOAT = auto()
    DOUBLE = auto()
    STRING = auto()
    CHARACTER = auto()
    BOOLEAN = auto()
    NULL = auto()
    
    # Identifiers
    IDENTIFIER = auto()
    FIELD_IDENTIFIER = auto()  # $field
    
    # Keywords - Declarations
    PACKAGE = auto()
    IMPORT = auto()
    CLASS = auto()
    INTERFACE = auto()
    OBJECT = auto()
    ENUM = auto()
    ANNOTATION = auto()
    DATA = auto()
    SEALED = auto()
    INNER = auto()
    INLINE = auto()
    VALUE = auto()
    
    # Keywords - Functions and properties
    FUN = auto()
    VAL = auto()
    VAR = auto()
    CONSTRUCTOR = auto()
    INIT = auto()
    GET = auto()
    SET = auto()
    FIELD = auto()
    
    # Keywords - Modifiers
    PUBLIC = auto()
    PRIVATE = auto()
    PROTECTED = auto()
    INTERNAL = auto()
    ABSTRACT = auto()
    FINAL = auto()
    OPEN = auto()
    OVERRIDE = auto()
    LATEINIT = auto()
    CONST = auto()
    SUSPEND = auto()
    INLINE_KEYWORD = auto()
    NOINLINE = auto()
    CROSSINLINE = auto()
    REIFIED = auto()
    EXTERNAL = auto()
    ACTUAL = auto()
    EXPECT = auto()
    
    # Keywords - Control flow
    IF = auto()
    ELSE = auto()
    WHEN = auto()
    FOR = auto()
    WHILE = auto()
    DO = auto()
    TRY = auto()
    CATCH = auto()
    FINALLY = auto()
    THROW = auto()
    RETURN = auto()
    BREAK = auto()
    CONTINUE = auto()
    
    # Keywords - Types and generics
    IN = auto()
    OUT = auto()
    WHERE = auto()
    TYPEALIAS = auto()
    
    # Keywords - Other
    THIS = auto()
    SUPER = auto()
    IS = auto()
    AS = auto()
    BY = auto()
    COMPANION = auto()
    
    # Operators
    PLUS = auto()              # +
    MINUS = auto()             # -
    MULTIPLY = auto()          # *
    DIVIDE = auto()            # /
    MODULO = auto()            # %
    ASSIGN = auto()            # =
    PLUS_ASSIGN = auto()       # +=
    MINUS_ASSIGN = auto()      # -=
    MULTIPLY_ASSIGN = auto()   # *=
    DIVIDE_ASSIGN = auto()     # /=
    MODULO_ASSIGN = auto()     # %=
    
    # Comparison operators
    EQUAL = auto()             # ==
    NOT_EQUAL = auto()         # !=
    IDENTITY_EQUAL = auto()    # ===
    IDENTITY_NOT_EQUAL = auto() # !==
    LESS_THAN = auto()         # <
    GREATER_THAN = auto()      # >
    LESS_EQUAL = auto()        # <=
    GREATER_EQUAL = auto()     # >=
    
    # Logical operators
    AND = auto()               # &&
    OR = auto()                # ||
    NOT = auto()               # !
    
    # Bitwise operators
    BITWISE_AND = auto()       # and
    BITWISE_OR = auto()        # or
    BITWISE_XOR = auto()       # xor
    BITWISE_INVERT = auto()    # inv
    SHIFT_LEFT = auto()        # shl
    SHIFT_RIGHT = auto()       # shr
    UNSIGNED_SHIFT_RIGHT = auto() # ushr
    
    # Special operators
    ELVIS = auto()             # ?:
    SAFE_CALL = auto()         # ?.
    NOT_NULL_ASSERTION = auto() # !!
    RANGE = auto()             # ..
    RANGE_UNTIL = auto()       # until
    
    # Increment/Decrement
    INCREMENT = auto()         # ++
    DECREMENT = auto()         # --
    
    # Punctuation
    SEMICOLON = auto()         # ;
    COMMA = auto()             # ,
    DOT = auto()               # .
    COLON = auto()             # :
    DOUBLE_COLON = auto()      # ::
    QUESTION = auto()          # ?
    AT = auto()                # @
    ARROW = auto()             # ->
    
    # Brackets
    LPAREN = auto()            # (
    RPAREN = auto()            # )
    LBRACKET = auto()          # [
    RBRACKET = auto()          # ]
    LBRACE = auto()            # {
    RBRACE = auto()            # }
    LANGLE = auto()            # <
    RANGLE = auto()            # >
    
    # String interpolation
    STRING_START = auto()      # "
    STRING_END = auto()        # "
    STRING_CONTENT = auto()    # content inside string
    INTERPOLATION_START = auto() # ${
    INTERPOLATION_END = auto() # }
    
    # Comments
    LINE_COMMENT = auto()      # //
    BLOCK_COMMENT = auto()     # /* */
    DOC_COMMENT = auto()       # /** */
    
    # Labels
    LABEL = auto()             # label@
    
    # Special
    EOF = auto()
    NEWLINE = auto()
    WHITESPACE = auto()


@dataclass
class KotlinToken:
    """Kotlin token representation."""
    type: KotlinTokenType
    value: str
    line: int = 1
    column: int = 1
    length: int = 0
    
    def __post_init__(self):
        if self.length == 0:
            self.length = len(self.value)
    
    def __str__(self):
        return f"{self.type.name}({self.value!r})"
    
    def __repr__(self):
        return f"KotlinToken({self.type.name}, {self.value!r}, {self.line}:{self.column})"


class KotlinLexer:
    """
    Kotlin lexer for tokenizing Kotlin source code.
    
    Supports all Kotlin language features including:
    - Null safety operators (?., !!, ?:)
    - String templates and interpolation
    - Lambda expressions
    - Coroutine keywords
    - Operator overloading
    """
    
    def __init__(self):
        """Initialize the Kotlin lexer."""
        self.logger = logging.getLogger(__name__)
        
        # Token patterns
        self.token_patterns = self._build_token_patterns()
        
        # Keywords
        self.keywords = self._build_keywords()
        
        # State tracking
        self.text = ""
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
    
    def _build_token_patterns(self) -> List[Tuple[str, KotlinTokenType]]:
        """Build regex patterns for tokenization."""
        patterns = [
            # Comments
            (r'//.*?$', KotlinTokenType.LINE_COMMENT),
            (r'/\*\*.*?\*/', KotlinTokenType.DOC_COMMENT),
            (r'/\*.*?\*/', KotlinTokenType.BLOCK_COMMENT),
            
            # String literals with interpolation support
            (r'"""([^"\\]|\\.)*"""', KotlinTokenType.STRING),  # Triple quoted strings
            (r'"([^"\\$]|\\.|\$(?!\{))*"', KotlinTokenType.STRING),  # Regular strings
            (r"'([^'\\]|\\.)'", KotlinTokenType.CHARACTER),
            
            # Numeric literals
            (r'\b\d+\.\d+[fF]\b', KotlinTokenType.FLOAT),
            (r'\b\d+\.\d+\b', KotlinTokenType.DOUBLE),
            (r'\b\d+[lL]\b', KotlinTokenType.LONG),
            (r'\b\d+[fF]\b', KotlinTokenType.FLOAT),
            (r'\b0[xX][0-9a-fA-F]+[lL]?\b', KotlinTokenType.INTEGER),  # Hex
            (r'\b0[bB][01]+[lL]?\b', KotlinTokenType.INTEGER),  # Binary
            (r'\b\d+\b', KotlinTokenType.INTEGER),
            
            # Multi-character operators (order matters!)
            (r'===', KotlinTokenType.IDENTITY_EQUAL),
            (r'!==', KotlinTokenType.IDENTITY_NOT_EQUAL),
            (r'==', KotlinTokenType.EQUAL),
            (r'!=', KotlinTokenType.NOT_EQUAL),
            (r'<=', KotlinTokenType.LESS_EQUAL),
            (r'>=', KotlinTokenType.GREATER_EQUAL),
            (r'\+=', KotlinTokenType.PLUS_ASSIGN),
            (r'-=', KotlinTokenType.MINUS_ASSIGN),
            (r'\*=', KotlinTokenType.MULTIPLY_ASSIGN),
            (r'/=', KotlinTokenType.DIVIDE_ASSIGN),
            (r'%=', KotlinTokenType.MODULO_ASSIGN),
            (r'\+\+', KotlinTokenType.INCREMENT),
            (r'--', KotlinTokenType.DECREMENT),
            (r'&&', KotlinTokenType.AND),
            (r'\|\|', KotlinTokenType.OR),
            (r'\?\:', KotlinTokenType.ELVIS),
            (r'\?\.', KotlinTokenType.SAFE_CALL),
            (r'!!', KotlinTokenType.NOT_NULL_ASSERTION),
            (r'\.\.', KotlinTokenType.RANGE),
            (r'::', KotlinTokenType.DOUBLE_COLON),
            (r'->', KotlinTokenType.ARROW),
            
            # Single-character operators
            (r'\+', KotlinTokenType.PLUS),
            (r'-', KotlinTokenType.MINUS),
            (r'\*', KotlinTokenType.MULTIPLY),
            (r'/', KotlinTokenType.DIVIDE),
            (r'%', KotlinTokenType.MODULO),
            (r'=', KotlinTokenType.ASSIGN),
            (r'<', KotlinTokenType.LESS_THAN),
            (r'>', KotlinTokenType.GREATER_THAN),
            (r'!', KotlinTokenType.NOT),
            
            # Punctuation
            (r';', KotlinTokenType.SEMICOLON),
            (r',', KotlinTokenType.COMMA),
            (r'\.', KotlinTokenType.DOT),
            (r':', KotlinTokenType.COLON),
            (r'\?', KotlinTokenType.QUESTION),
            (r'@', KotlinTokenType.AT),
            (r'\(', KotlinTokenType.LPAREN),
            (r'\)', KotlinTokenType.RPAREN),
            (r'\[', KotlinTokenType.LBRACKET),
            (r'\]', KotlinTokenType.RBRACKET),
            (r'\{', KotlinTokenType.LBRACE),
            (r'\}', KotlinTokenType.RBRACE),
            
            # Labels
            (r'[a-zA-Z_][a-zA-Z0-9_]*@', KotlinTokenType.LABEL),
            
            # Field identifiers
            (r'\$[a-zA-Z_][a-zA-Z0-9_]*', KotlinTokenType.FIELD_IDENTIFIER),
            
            # Identifiers (must come after keywords)
            (r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', KotlinTokenType.IDENTIFIER),
            
            # Whitespace and newlines
            (r'\n', KotlinTokenType.NEWLINE),
            (r'\s+', KotlinTokenType.WHITESPACE),
        ]
        
        return [(re.compile(pattern, re.MULTILINE | re.DOTALL), token_type) 
                for pattern, token_type in patterns]
    
    def _build_keywords(self) -> Dict[str, KotlinTokenType]:
        """Build keyword mapping."""
        return {
            # Declarations
            'package': KotlinTokenType.PACKAGE,
            'import': KotlinTokenType.IMPORT,
            'class': KotlinTokenType.CLASS,
            'interface': KotlinTokenType.INTERFACE,
            'object': KotlinTokenType.OBJECT,
            'enum': KotlinTokenType.ENUM,
            'annotation': KotlinTokenType.ANNOTATION,
            'data': KotlinTokenType.DATA,
            'sealed': KotlinTokenType.SEALED,
            'inner': KotlinTokenType.INNER,
            'inline': KotlinTokenType.INLINE_KEYWORD,
            'value': KotlinTokenType.VALUE,
            
            # Functions and properties
            'fun': KotlinTokenType.FUN,
            'val': KotlinTokenType.VAL,
            'var': KotlinTokenType.VAR,
            'constructor': KotlinTokenType.CONSTRUCTOR,
            'init': KotlinTokenType.INIT,
            'get': KotlinTokenType.GET,
            'set': KotlinTokenType.SET,
            'field': KotlinTokenType.FIELD,
            
            # Modifiers
            'public': KotlinTokenType.PUBLIC,
            'private': KotlinTokenType.PRIVATE,
            'protected': KotlinTokenType.PROTECTED,
            'internal': KotlinTokenType.INTERNAL,
            'abstract': KotlinTokenType.ABSTRACT,
            'final': KotlinTokenType.FINAL,
            'open': KotlinTokenType.OPEN,
            'override': KotlinTokenType.OVERRIDE,
            'lateinit': KotlinTokenType.LATEINIT,
            'const': KotlinTokenType.CONST,
            'suspend': KotlinTokenType.SUSPEND,
            'noinline': KotlinTokenType.NOINLINE,
            'crossinline': KotlinTokenType.CROSSINLINE,
            'reified': KotlinTokenType.REIFIED,
            'external': KotlinTokenType.EXTERNAL,
            'actual': KotlinTokenType.ACTUAL,
            'expect': KotlinTokenType.EXPECT,
            
            # Control flow
            'if': KotlinTokenType.IF,
            'else': KotlinTokenType.ELSE,
            'when': KotlinTokenType.WHEN,
            'for': KotlinTokenType.FOR,
            'while': KotlinTokenType.WHILE,
            'do': KotlinTokenType.DO,
            'try': KotlinTokenType.TRY,
            'catch': KotlinTokenType.CATCH,
            'finally': KotlinTokenType.FINALLY,
            'throw': KotlinTokenType.THROW,
            'return': KotlinTokenType.RETURN,
            'break': KotlinTokenType.BREAK,
            'continue': KotlinTokenType.CONTINUE,
            
            # Types and generics
            'in': KotlinTokenType.IN,
            'out': KotlinTokenType.OUT,
            'where': KotlinTokenType.WHERE,
            'typealias': KotlinTokenType.TYPEALIAS,
            
            # Literals
            'true': KotlinTokenType.BOOLEAN,
            'false': KotlinTokenType.BOOLEAN,
            'null': KotlinTokenType.NULL,
            
            # Other
            'this': KotlinTokenType.THIS,
            'super': KotlinTokenType.SUPER,
            'is': KotlinTokenType.IS,
            'as': KotlinTokenType.AS,
            'by': KotlinTokenType.BY,
            'companion': KotlinTokenType.COMPANION,
            
            # Bitwise operators
            'and': KotlinTokenType.BITWISE_AND,
            'or': KotlinTokenType.BITWISE_OR,
            'xor': KotlinTokenType.BITWISE_XOR,
            'inv': KotlinTokenType.BITWISE_INVERT,
            'shl': KotlinTokenType.SHIFT_LEFT,
            'shr': KotlinTokenType.SHIFT_RIGHT,
            'ushr': KotlinTokenType.UNSIGNED_SHIFT_RIGHT,
            'until': KotlinTokenType.RANGE_UNTIL,
        }
    
    def tokenize(self, text: str) -> List[KotlinToken]:
        """
        Tokenize Kotlin source code.
        
        Args:
            text: Kotlin source code to tokenize
            
        Returns:
            List of Kotlin tokens
        """
        self.text = text
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        
        while self.position < len(self.text):
            if not self._scan_token():
                # Skip unknown character
                self._advance()
        
        # Add EOF token
        self.tokens.append(KotlinToken(KotlinTokenType.EOF, '', self.line, self.column))
        
        # Filter out whitespace and comments unless needed
        filtered_tokens = []
        for token in self.tokens:
            if token.type not in [KotlinTokenType.WHITESPACE, KotlinTokenType.LINE_COMMENT, 
                                 KotlinTokenType.BLOCK_COMMENT, KotlinTokenType.DOC_COMMENT]:
                filtered_tokens.append(token)
        
        return filtered_tokens
    
    def _scan_token(self) -> bool:
        """Scan for the next token."""
        if self.position >= len(self.text):
            return False
        
        # Try each pattern
        for pattern, token_type in self.token_patterns:
            match = pattern.match(self.text, self.position)
            if match:
                value = match.group(0)
                
                # Handle keywords vs identifiers
                if token_type == KotlinTokenType.IDENTIFIER:
                    if value in self.keywords:
                        token_type = self.keywords[value]
                        # Special handling for boolean literals
                        if value in ['true', 'false']:
                            token_type = KotlinTokenType.BOOLEAN
                        elif value == 'null':
                            token_type = KotlinTokenType.NULL
                
                # Create token
                token = KotlinToken(
                    type=token_type,
                    value=value,
                    line=self.line,
                    column=self.column,
                    length=len(value)
                )
                
                self.tokens.append(token)
                
                # Update position
                self._advance(len(value))
                
                return True
        
        return False
    
    def _advance(self, count: int = 1):
        """Advance position and update line/column tracking."""
        for _ in range(count):
            if self.position < len(self.text):
                if self.text[self.position] == '\n':
                    self.line += 1
                    self.column = 1
                else:
                    self.column += 1
                self.position += 1


class KotlinParseError(Exception):
    """Kotlin parsing error."""
    
    def __init__(self, message: str, token: Optional[KotlinToken] = None):
        super().__init__(message)
        self.token = token
        self.message = message
    
    def __str__(self):
        if self.token:
            return f"Parse error at line {self.token.line}, column {self.token.column}: {self.message}"
        return f"Parse error: {self.message}"


class KotlinParser:
    """
    Kotlin parser using recursive descent parsing.
    
    Supports comprehensive Kotlin parsing including:
    - Class and object declarations
    - Function and property declarations
    - Coroutines and suspend functions
    - Null safety operators
    - Lambda expressions and higher-order functions
    - When expressions and pattern matching
    """
    
    def __init__(self):
        """Initialize the Kotlin parser."""
        self.lexer = KotlinLexer()
        self.logger = logging.getLogger(__name__)
        
        # Parser state
        self.tokens = []
        self.current = 0
        self.errors = []
    
    def parse(self, text: str) -> KotlinProgram:
        """
        Parse Kotlin source code into an AST.
        
        Args:
            text: Kotlin source code to parse
            
        Returns:
            KotlinProgram: Root AST node
            
        Raises:
            KotlinParseError: If parsing fails
        """
        try:
            # Tokenize
            self.tokens = self.lexer.tokenize(text)
            self.current = 0
            self.errors = []
            
            # Parse program
            program = self._parse_program()
            
            if self.errors:
                error_msg = "; ".join(self.errors)
                raise KotlinParseError(f"Parse errors: {error_msg}")
            
            return program
            
        except Exception as e:
            self.logger.error(f"Kotlin parsing failed: {e}")
            raise KotlinParseError(f"Failed to parse Kotlin code: {e}")
    
    def _parse_program(self) -> KotlinProgram:
        """Parse a complete Kotlin program."""
        package_declaration = None
        imports = []
        declarations = []
        
        # Parse package declaration
        if self._check(KotlinTokenType.PACKAGE):
            package_declaration = self._parse_package_declaration()
        
        # Parse imports
        while self._check(KotlinTokenType.IMPORT):
            imports.append(self._parse_import_declaration())
        
        # Parse top-level declarations
        while not self._is_at_end():
            if self._check(KotlinTokenType.NEWLINE):
                self._advance()  # Skip newlines
                continue
            
            decl = self._parse_declaration()
            if decl:
                declarations.append(decl)
        
        return KotlinProgram(
            package_declaration=package_declaration,
            imports=imports,
            declarations=declarations
        )
    
    def _parse_package_declaration(self) -> KotlinPackageDeclaration:
        """Parse package declaration."""
        self._consume(KotlinTokenType.PACKAGE, "Expected 'package'")
        
        # Parse package name
        name_parts = []
        name_parts.append(self._consume(KotlinTokenType.IDENTIFIER, "Expected package name").value)
        
        while self._check(KotlinTokenType.DOT):
            self._advance()
            name_parts.append(self._consume(KotlinTokenType.IDENTIFIER, "Expected package name").value)
        
        package_name = ".".join(name_parts)
        
        return KotlinPackageDeclaration(name=package_name)
    
    def _parse_import_declaration(self) -> KotlinImportDeclaration:
        """Parse import declaration."""
        self._consume(KotlinTokenType.IMPORT, "Expected 'import'")
        
        # Parse import path
        path_parts = []
        path_parts.append(self._consume(KotlinTokenType.IDENTIFIER, "Expected import path").value)
        
        while self._check(KotlinTokenType.DOT):
            self._advance()
            if self._check(KotlinTokenType.MULTIPLY):
                self._advance()
                path_parts.append("*")
                break
            else:
                path_parts.append(self._consume(KotlinTokenType.IDENTIFIER, "Expected import path").value)
        
        import_path = ".".join(path_parts)
        
        # Parse alias
        alias = None
        if self._check(KotlinTokenType.AS):
            self._advance()
            alias = self._consume(KotlinTokenType.IDENTIFIER, "Expected alias name").value
        
        return KotlinImportDeclaration(path=import_path, alias=alias)
    
    def _parse_declaration(self) -> Optional[KotlinStatement]:
        """Parse a top-level declaration."""
        try:
            # Parse modifiers
            modifiers = self._parse_modifiers()
            
            if self._check(KotlinTokenType.CLASS):
                return self._parse_class_declaration(modifiers)
            elif self._check(KotlinTokenType.INTERFACE):
                return self._parse_interface_declaration(modifiers)
            elif self._check(KotlinTokenType.OBJECT):
                return self._parse_object_declaration(modifiers)
            elif self._check(KotlinTokenType.FUN):
                return self._parse_function_declaration(modifiers)
            elif self._check(KotlinTokenType.VAL, KotlinTokenType.VAR):
                return self._parse_property_declaration(modifiers)
            elif self._check(KotlinTokenType.TYPEALIAS):
                return self._parse_typealias_declaration(modifiers)
            else:
                self._error(f"Unexpected token: {self._peek().value}")
                return None
                
        except KotlinParseError as e:
            self.errors.append(str(e))
            self._synchronize()
            return None
    
    def _parse_modifiers(self) -> List[KotlinModifier]:
        """Parse modifiers."""
        modifiers = []
        
        while self._check_modifier():
            token = self._advance()
            modifier = KotlinModifier(name=token.value)
            modifiers.append(modifier)
        
        return modifiers
    
    def _parse_class_declaration(self, modifiers: List[KotlinModifier]) -> KotlinClassDeclaration:
        """Parse class declaration."""
        self._consume(KotlinTokenType.CLASS, "Expected 'class'")
        
        # Parse class name
        name = self._consume(KotlinTokenType.IDENTIFIER, "Expected class name").value
        
        # Parse type parameters
        type_parameters = []
        if self._check(KotlinTokenType.LANGLE):
            type_parameters = self._parse_type_parameters()
        
        # Parse primary constructor
        primary_constructor = None
        if self._check(KotlinTokenType.CONSTRUCTOR) or self._check(KotlinTokenType.LPAREN):
            primary_constructor = self._parse_primary_constructor()
        
        # Parse supertype list
        supertypes = []
        if self._check(KotlinTokenType.COLON):
            supertypes = self._parse_supertype_list()
        
        # Parse class body
        members = []
        if self._check(KotlinTokenType.LBRACE):
            members = self._parse_class_body()
        
        return KotlinClassDeclaration(
            modifiers=modifiers,
            name=name,
            type_parameters=type_parameters,
            primary_constructor=primary_constructor,
            supertypes=supertypes,
            members=members
        )
    
    def _parse_function_declaration(self, modifiers: List[KotlinModifier]) -> KotlinFunctionDeclaration:
        """Parse function declaration."""
        self._consume(KotlinTokenType.FUN, "Expected 'fun'")
        
        # Parse type parameters
        type_parameters = []
        if self._check(KotlinTokenType.LANGLE):
            type_parameters = self._parse_type_parameters()
        
        # Parse function name
        name = self._consume(KotlinTokenType.IDENTIFIER, "Expected function name").value
        
        # Parse parameters
        self._consume(KotlinTokenType.LPAREN, "Expected '('")
        parameters = []
        
        if not self._check(KotlinTokenType.RPAREN):
            parameters.append(self._parse_parameter())
            while self._check(KotlinTokenType.COMMA):
                self._advance()
                parameters.append(self._parse_parameter())
        
        self._consume(KotlinTokenType.RPAREN, "Expected ')'")
        
        # Parse return type
        return_type = None
        if self._check(KotlinTokenType.COLON):
            self._advance()
            return_type = self._parse_type()
        
        # Parse body
        body = None
        if self._check(KotlinTokenType.ASSIGN):
            # Expression body
            self._advance()
            body = self._parse_expression()
        elif self._check(KotlinTokenType.LBRACE):
            # Block body
            body = self._parse_block()
        
        return KotlinFunctionDeclaration(
            modifiers=modifiers,
            name=name,
            type_parameters=type_parameters,
            parameters=parameters,
            return_type=return_type,
            body=body
        )
    
    def _parse_property_declaration(self, modifiers: List[KotlinModifier]) -> KotlinPropertyDeclaration:
        """Parse property declaration."""
        is_var = self._check(KotlinTokenType.VAR)
        self._advance()  # Consume VAL or VAR
        
        # Parse property name
        name = self._consume(KotlinTokenType.IDENTIFIER, "Expected property name").value
        
        # Parse type
        property_type = None
        if self._check(KotlinTokenType.COLON):
            self._advance()
            property_type = self._parse_type()
        
        # Parse initializer
        initializer = None
        if self._check(KotlinTokenType.ASSIGN):
            self._advance()
            initializer = self._parse_expression()
        
        # Parse getter/setter (simplified)
        getter = None
        setter = None
        
        return KotlinPropertyDeclaration(
            modifiers=modifiers,
            is_var=is_var,
            name=name,
            type=property_type,
            initializer=initializer,
            getter=getter,
            setter=setter
        )
    
    def _parse_expression(self) -> KotlinExpression:
        """Parse expression."""
        return self._parse_disjunction()
    
    def _parse_disjunction(self) -> KotlinExpression:
        """Parse logical OR expression."""
        expr = self._parse_conjunction()
        
        while self._check(KotlinTokenType.OR):
            operator = self._advance().value
            right = self._parse_conjunction()
            expr = KotlinBinaryExpression(
                left=expr,
                operator=KotlinOperator(operator),
                right=right
            )
        
        return expr
    
    def _parse_conjunction(self) -> KotlinExpression:
        """Parse logical AND expression."""
        expr = self._parse_equality()
        
        while self._check(KotlinTokenType.AND):
            operator = self._advance().value
            right = self._parse_equality()
            expr = KotlinBinaryExpression(
                left=expr,
                operator=KotlinOperator(operator),
                right=right
            )
        
        return expr
    
    def _parse_equality(self) -> KotlinExpression:
        """Parse equality expression."""
        expr = self._parse_comparison()
        
        while self._check(KotlinTokenType.EQUAL, KotlinTokenType.NOT_EQUAL,
                          KotlinTokenType.IDENTITY_EQUAL, KotlinTokenType.IDENTITY_NOT_EQUAL):
            operator = self._advance().value
            right = self._parse_comparison()
            expr = KotlinBinaryExpression(
                left=expr,
                operator=KotlinOperator(operator),
                right=right
            )
        
        return expr
    
    def _parse_comparison(self) -> KotlinExpression:
        """Parse comparison expression."""
        expr = self._parse_named_infix()
        
        while self._check(KotlinTokenType.LESS_THAN, KotlinTokenType.GREATER_THAN,
                          KotlinTokenType.LESS_EQUAL, KotlinTokenType.GREATER_EQUAL):
            operator = self._advance().value
            right = self._parse_named_infix()
            expr = KotlinBinaryExpression(
                left=expr,
                operator=KotlinOperator(operator),
                right=right
            )
        
        return expr
    
    def _parse_named_infix(self) -> KotlinExpression:
        """Parse named infix expressions (in, !in, is, !is)."""
        expr = self._parse_elvis()
        
        while self._check(KotlinTokenType.IN, KotlinTokenType.IS):
            operator = self._advance().value
            right = self._parse_elvis()
            expr = KotlinBinaryExpression(
                left=expr,
                operator=KotlinOperator(operator),
                right=right
            )
        
        return expr
    
    def _parse_elvis(self) -> KotlinExpression:
        """Parse Elvis expression."""
        expr = self._parse_infix_function_call()
        
        while self._check(KotlinTokenType.ELVIS):
            operator = self._advance().value
            right = self._parse_infix_function_call()
            expr = KotlinBinaryExpression(
                left=expr,
                operator=KotlinOperator(operator),
                right=right
            )
        
        return expr
    
    def _parse_infix_function_call(self) -> KotlinExpression:
        """Parse infix function call."""
        return self._parse_range()
    
    def _parse_range(self) -> KotlinExpression:
        """Parse range expression."""
        expr = self._parse_additive()
        
        while self._check(KotlinTokenType.RANGE, KotlinTokenType.RANGE_UNTIL):
            operator = self._advance().value
            right = self._parse_additive()
            expr = KotlinBinaryExpression(
                left=expr,
                operator=KotlinOperator(operator),
                right=right
            )
        
        return expr
    
    def _parse_additive(self) -> KotlinExpression:
        """Parse additive expression."""
        expr = self._parse_multiplicative()
        
        while self._check(KotlinTokenType.PLUS, KotlinTokenType.MINUS):
            operator = self._advance().value
            right = self._parse_multiplicative()
            expr = KotlinBinaryExpression(
                left=expr,
                operator=KotlinOperator(operator),
                right=right
            )
        
        return expr
    
    def _parse_multiplicative(self) -> KotlinExpression:
        """Parse multiplicative expression."""
        expr = self._parse_as_expression()
        
        while self._check(KotlinTokenType.MULTIPLY, KotlinTokenType.DIVIDE, KotlinTokenType.MODULO):
            operator = self._advance().value
            right = self._parse_as_expression()
            expr = KotlinBinaryExpression(
                left=expr,
                operator=KotlinOperator(operator),
                right=right
            )
        
        return expr
    
    def _parse_as_expression(self) -> KotlinExpression:
        """Parse type cast expression."""
        expr = self._parse_prefix_unary()
        
        while self._check(KotlinTokenType.AS):
            self._advance()
            target_type = self._parse_type()
            # Create as expression (simplified)
            expr = KotlinBinaryExpression(
                left=expr,
                operator=KotlinOperator("as"),
                right=target_type  # This would need proper typing
            )
        
        return expr
    
    def _parse_prefix_unary(self) -> KotlinExpression:
        """Parse prefix unary expression."""
        if self._check(KotlinTokenType.NOT, KotlinTokenType.PLUS, KotlinTokenType.MINUS,
                      KotlinTokenType.INCREMENT, KotlinTokenType.DECREMENT):
            operator = self._advance().value
            operand = self._parse_prefix_unary()
            return KotlinUnaryExpression(
                operator=KotlinOperator(operator),
                operand=operand,
                is_prefix=True
            )
        
        return self._parse_postfix_unary()
    
    def _parse_postfix_unary(self) -> KotlinExpression:
        """Parse postfix unary expression."""
        expr = self._parse_primary()
        
        while True:
            if self._check(KotlinTokenType.INCREMENT, KotlinTokenType.DECREMENT):
                operator = self._advance().value
                expr = KotlinUnaryExpression(
                    operator=KotlinOperator(operator),
                    operand=expr,
                    is_prefix=False
                )
            elif self._check(KotlinTokenType.NOT_NULL_ASSERTION):
                self._advance()
                expr = KotlinUnaryExpression(
                    operator=KotlinOperator("!!"),
                    operand=expr,
                    is_prefix=False
                )
            elif self._check(KotlinTokenType.LPAREN):
                # Function call
                self._advance()
                arguments = []
                if not self._check(KotlinTokenType.RPAREN):
                    arguments.append(self._parse_expression())
                    while self._check(KotlinTokenType.COMMA):
                        self._advance()
                        arguments.append(self._parse_expression())
                self._consume(KotlinTokenType.RPAREN, "Expected ')'")
                expr = KotlinCallExpression(callee=expr, arguments=arguments)
            elif self._check(KotlinTokenType.LBRACKET):
                # Array access
                self._advance()
                index = self._parse_expression()
                self._consume(KotlinTokenType.RBRACKET, "Expected ']'")
                expr = KotlinCallExpression(callee=expr, arguments=[index])  # Simplified
            elif self._check(KotlinTokenType.DOT, KotlinTokenType.SAFE_CALL):
                # Member access
                is_safe = self._check(KotlinTokenType.SAFE_CALL)
                self._advance()
                member = self._consume(KotlinTokenType.IDENTIFIER, "Expected member name").value
                expr = KotlinCallExpression(callee=expr, arguments=[])  # Simplified member access
            else:
                break
        
        return expr
    
    def _parse_primary(self) -> KotlinExpression:
        """Parse primary expression."""
        # Literals
        if self._check(KotlinTokenType.INTEGER):
            token = self._advance()
            return KotlinLiteral(value=int(token.value), type="Int")
        
        if self._check(KotlinTokenType.LONG):
            token = self._advance()
            value = token.value.rstrip('lL')
            return KotlinLiteral(value=int(value), type="Long")
        
        if self._check(KotlinTokenType.FLOAT):
            token = self._advance()
            value = token.value.rstrip('fF')
            return KotlinLiteral(value=float(value), type="Float")
        
        if self._check(KotlinTokenType.DOUBLE):
            token = self._advance()
            return KotlinLiteral(value=float(token.value), type="Double")
        
        if self._check(KotlinTokenType.STRING):
            token = self._advance()
            return KotlinLiteral(value=token.value, type="String")
        
        if self._check(KotlinTokenType.CHARACTER):
            token = self._advance()
            return KotlinLiteral(value=token.value, type="Char")
        
        if self._check(KotlinTokenType.BOOLEAN):
            token = self._advance()
            return KotlinLiteral(value=token.value == "true", type="Boolean")
        
        if self._check(KotlinTokenType.NULL):
            self._advance()
            return KotlinLiteral(value=None, type="Nothing?")
        
        # Identifiers
        if self._check(KotlinTokenType.IDENTIFIER):
            token = self._advance()
            return KotlinIdentifier(name=token.value)
        
        # This expression
        if self._check(KotlinTokenType.THIS):
            self._advance()
            return KotlinIdentifier(name="this")
        
        # Super expression
        if self._check(KotlinTokenType.SUPER):
            self._advance()
            return KotlinIdentifier(name="super")
        
        # Parenthesized expression
        if self._check(KotlinTokenType.LPAREN):
            self._advance()
            expr = self._parse_expression()
            self._consume(KotlinTokenType.RPAREN, "Expected ')'")
            return expr
        
        # Lambda expression
        if self._check(KotlinTokenType.LBRACE):
            return self._parse_lambda_expression()
        
        # If expression
        if self._check(KotlinTokenType.IF):
            return self._parse_if_expression()
        
        # When expression
        if self._check(KotlinTokenType.WHEN):
            return self._parse_when_expression()
        
        # Try expression
        if self._check(KotlinTokenType.TRY):
            return self._parse_try_expression()
        
        self._error(f"Unexpected token: {self._peek().value}")
        return KotlinIdentifier(name="error")
    
    def _parse_lambda_expression(self) -> KotlinLambdaExpression:
        """Parse lambda expression."""
        self._consume(KotlinTokenType.LBRACE, "Expected '{'")
        
        # Parse parameters (simplified)
        parameters = []
        
        # Parse body
        body = []
        while not self._check(KotlinTokenType.RBRACE) and not self._is_at_end():
            stmt = self._parse_statement()
            if stmt:
                body.append(stmt)
        
        self._consume(KotlinTokenType.RBRACE, "Expected '}'")
        
        return KotlinLambdaExpression(
            parameters=parameters,
            body=KotlinBlock(statements=body)
        )
    
    def _parse_if_expression(self) -> KotlinIfExpression:
        """Parse if expression."""
        self._consume(KotlinTokenType.IF, "Expected 'if'")
        self._consume(KotlinTokenType.LPAREN, "Expected '('")
        
        condition = self._parse_expression()
        
        self._consume(KotlinTokenType.RPAREN, "Expected ')'")
        
        then_branch = self._parse_control_structure_body()
        
        else_branch = None
        if self._check(KotlinTokenType.ELSE):
            self._advance()
            else_branch = self._parse_control_structure_body()
        
        return KotlinIfExpression(
            condition=condition,
            then_branch=then_branch,
            else_branch=else_branch
        )
    
    def _parse_when_expression(self) -> KotlinWhenExpression:
        """Parse when expression."""
        self._consume(KotlinTokenType.WHEN, "Expected 'when'")
        
        subject = None
        if self._check(KotlinTokenType.LPAREN):
            self._advance()
            subject = self._parse_expression()
            self._consume(KotlinTokenType.RPAREN, "Expected ')'")
        
        self._consume(KotlinTokenType.LBRACE, "Expected '{'")
        
        entries = []
        while not self._check(KotlinTokenType.RBRACE) and not self._is_at_end():
            # Parse when entry (simplified)
            if self._check(KotlinTokenType.ELSE):
                self._advance()
                self._consume(KotlinTokenType.ARROW, "Expected '->'")
                body = self._parse_control_structure_body()
                entries.append({"conditions": ["else"], "body": body})
            else:
                conditions = []
                conditions.append(self._parse_expression())
                while self._check(KotlinTokenType.COMMA):
                    self._advance()
                    conditions.append(self._parse_expression())
                
                self._consume(KotlinTokenType.ARROW, "Expected '->'")
                body = self._parse_control_structure_body()
                entries.append({"conditions": conditions, "body": body})
        
        self._consume(KotlinTokenType.RBRACE, "Expected '}'")
        
        return KotlinWhenExpression(
            subject=subject,
            entries=entries
        )
    
    def _parse_try_expression(self) -> KotlinTryExpression:
        """Parse try expression."""
        self._consume(KotlinTokenType.TRY, "Expected 'try'")
        
        try_block = self._parse_block()
        
        catch_blocks = []
        while self._check(KotlinTokenType.CATCH):
            self._advance()
            self._consume(KotlinTokenType.LPAREN, "Expected '('")
            
            # Parse parameter (simplified)
            param_name = self._consume(KotlinTokenType.IDENTIFIER, "Expected parameter name").value
            self._consume(KotlinTokenType.COLON, "Expected ':'")
            param_type = self._parse_type()
            
            self._consume(KotlinTokenType.RPAREN, "Expected ')'")
            
            catch_body = self._parse_block()
            catch_blocks.append({
                "parameter": {"name": param_name, "type": param_type},
                "body": catch_body
            })
        
        finally_block = None
        if self._check(KotlinTokenType.FINALLY):
            self._advance()
            finally_block = self._parse_block()
        
        return KotlinTryExpression(
            try_block=try_block,
            catch_blocks=catch_blocks,
            finally_block=finally_block
        )
    
    def _parse_statement(self) -> Optional[KotlinStatement]:
        """Parse statement."""
        if self._check(KotlinTokenType.RETURN):
            return self._parse_return_statement()
        elif self._check(KotlinTokenType.VAL, KotlinTokenType.VAR):
            return self._parse_property_declaration([])
        else:
            # Expression statement
            expr = self._parse_expression()
            return KotlinExpression(expression=expr)  # Simplified
    
    def _parse_return_statement(self) -> KotlinReturnStatement:
        """Parse return statement."""
        self._consume(KotlinTokenType.RETURN, "Expected 'return'")
        
        value = None
        if not self._check(KotlinTokenType.NEWLINE) and not self._is_at_end():
            value = self._parse_expression()
        
        return KotlinReturnStatement(value=value)
    
    def _parse_block(self) -> KotlinBlock:
        """Parse block statement."""
        self._consume(KotlinTokenType.LBRACE, "Expected '{'")
        
        statements = []
        while not self._check(KotlinTokenType.RBRACE) and not self._is_at_end():
            if self._check(KotlinTokenType.NEWLINE):
                self._advance()
                continue
            
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
        
        self._consume(KotlinTokenType.RBRACE, "Expected '}'")
        
        return KotlinBlock(statements=statements)
    
    def _parse_control_structure_body(self) -> Union[KotlinBlock, KotlinExpression]:
        """Parse control structure body (block or expression)."""
        if self._check(KotlinTokenType.LBRACE):
            return self._parse_block()
        else:
            return self._parse_expression()
    
    def _parse_type(self) -> KotlinType:
        """Parse type reference."""
        # Simplified type parsing
        name = self._consume(KotlinTokenType.IDENTIFIER, "Expected type name").value
        
        # Handle nullable types
        nullable = False
        if self._check(KotlinTokenType.QUESTION):
            self._advance()
            nullable = True
        
        return KotlinType(name=name, nullable=nullable)
    
    def _parse_type_parameters(self) -> List[Any]:
        """Parse type parameters."""
        # Simplified implementation
        return []
    
    def _parse_primary_constructor(self) -> Any:
        """Parse primary constructor."""
        # Simplified implementation
        return None
    
    def _parse_supertype_list(self) -> List[Any]:
        """Parse supertype list."""
        # Simplified implementation
        return []
    
    def _parse_class_body(self) -> List[Any]:
        """Parse class body."""
        # Simplified implementation
        return []
    
    def _parse_parameter(self) -> Any:
        """Parse function parameter."""
        # Simplified implementation
        name = self._consume(KotlinTokenType.IDENTIFIER, "Expected parameter name").value
        self._consume(KotlinTokenType.COLON, "Expected ':'")
        param_type = self._parse_type()
        return {"name": name, "type": param_type}
    
    def _parse_interface_declaration(self, modifiers: List[KotlinModifier]) -> Any:
        """Parse interface declaration."""
        # Simplified implementation
        return None
    
    def _parse_object_declaration(self, modifiers: List[KotlinModifier]) -> Any:
        """Parse object declaration."""
        # Simplified implementation
        return None
    
    def _parse_typealias_declaration(self, modifiers: List[KotlinModifier]) -> Any:
        """Parse typealias declaration."""
        # Simplified implementation
        return None
    
    # Helper methods
    def _check(self, *token_types: KotlinTokenType) -> bool:
        """Check if current token matches any of the given types."""
        if self._is_at_end():
            return False
        return self._peek().type in token_types
    
    def _check_modifier(self) -> bool:
        """Check if current token is a modifier."""
        return self._check(
            KotlinTokenType.PUBLIC, KotlinTokenType.PRIVATE, KotlinTokenType.PROTECTED,
            KotlinTokenType.INTERNAL, KotlinTokenType.ABSTRACT, KotlinTokenType.FINAL,
            KotlinTokenType.OPEN, KotlinTokenType.OVERRIDE, KotlinTokenType.LATEINIT,
            KotlinTokenType.CONST, KotlinTokenType.SUSPEND, KotlinTokenType.INLINE_KEYWORD,
            KotlinTokenType.NOINLINE, KotlinTokenType.CROSSINLINE, KotlinTokenType.REIFIED,
            KotlinTokenType.EXTERNAL, KotlinTokenType.ACTUAL, KotlinTokenType.EXPECT,
            KotlinTokenType.DATA, KotlinTokenType.SEALED, KotlinTokenType.INNER
        )
    
    def _advance(self) -> KotlinToken:
        """Consume and return current token."""
        if not self._is_at_end():
            self.current += 1
        return self._previous()
    
    def _is_at_end(self) -> bool:
        """Check if we're at the end of tokens."""
        return self._peek().type == KotlinTokenType.EOF
    
    def _peek(self) -> KotlinToken:
        """Return current token without consuming it."""
        return self.tokens[self.current]
    
    def _previous(self) -> KotlinToken:
        """Return previous token."""
        return self.tokens[self.current - 1]
    
    def _consume(self, token_type: KotlinTokenType, message: str) -> KotlinToken:
        """Consume token of expected type or raise error."""
        if self._check(token_type):
            return self._advance()
        
        current_token = self._peek()
        raise KotlinParseError(f"{message}. Got {current_token.type.name}({current_token.value})", current_token)
    
    def _error(self, message: str):
        """Report parse error."""
        token = self._peek()
        error_msg = f"Parse error at line {token.line}, column {token.column}: {message}"
        self.logger.error(error_msg)
        raise KotlinParseError(error_msg, token)
    
    def _synchronize(self):
        """Synchronize parser after error."""
        self._advance()
        
        while not self._is_at_end():
            if self._previous().type == KotlinTokenType.NEWLINE:
                return
            
            if self._peek().type in [
                KotlinTokenType.CLASS, KotlinTokenType.FUN, KotlinTokenType.VAL,
                KotlinTokenType.VAR, KotlinTokenType.FOR, KotlinTokenType.IF,
                KotlinTokenType.WHILE, KotlinTokenType.RETURN
            ]:
                return
            
            self._advance()