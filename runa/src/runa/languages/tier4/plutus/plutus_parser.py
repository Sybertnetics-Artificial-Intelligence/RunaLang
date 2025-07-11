#!/usr/bin/env python3
"""
Plutus Parser Implementation

Comprehensive parser for Cardano's Plutus smart contract language.
Supports Haskell-based syntax, UPLC compilation targets, and Cardano-specific constructs.
"""

import re
from typing import List, Optional, Union, Dict, Any, Tuple
from enum import Enum
from dataclasses import dataclass
from .plutus_ast import *


class PlutusTokenType(Enum):
    """Token types for Plutus lexer."""
    # Literals
    INTEGER = "INTEGER"
    RATIONAL = "RATIONAL"
    STRING = "STRING"
    CHAR = "CHAR"
    
    # Identifiers and keywords
    IDENTIFIER = "IDENTIFIER"
    CONSTRUCTOR = "CONSTRUCTOR"
    QUALIFIED_IDENTIFIER = "QUALIFIED_IDENTIFIER"
    
    # Haskell keywords
    MODULE = "module"
    IMPORT = "import"
    QUALIFIED = "qualified"
    AS = "as"
    HIDING = "hiding"
    WHERE = "where"
    LET = "let"
    IN = "in"
    CASE = "case"
    OF = "of"
    IF = "if"
    THEN = "then"
    ELSE = "else"
    DO = "do"
    DATA = "data"
    NEWTYPE = "newtype"
    TYPE = "type"
    CLASS = "class"
    INSTANCE = "instance"
    DERIVING = "deriving"
    
    # Plutus-specific keywords
    VALIDATOR = "validator"
    MINTING_POLICY = "mintingPolicy"
    STAKE_VALIDATOR = "stakeValidator"
    BUILTIN = "builtin"
    
    # Symbols and operators
    LAMBDA = "\\"
    ARROW = "->"
    DOUBLE_ARROW = "=>"
    EQUALS = "="
    DOUBLE_COLON = "::"
    COLON = ":"
    SEMICOLON = ";"
    COMMA = ","
    DOT = "."
    PIPE = "|"
    UNDERSCORE = "_"
    AT = "@"
    
    # Brackets and parentheses
    LPAREN = "("
    RPAREN = ")"
    LBRACKET = "["
    RBRACKET = "]"
    LBRACE = "{"
    RBRACE = "}"
    
    # Arithmetic operators
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    MODULO = "%"
    POWER = "^"
    
    # Comparison operators
    EQUAL = "=="
    NOT_EQUAL = "/="
    LESS_THAN = "<"
    GREATER_THAN = ">"
    LESS_EQUAL = "<="
    GREATER_EQUAL = ">="
    
    # Logical operators
    AND = "&&"
    OR = "||"
    NOT = "not"
    
    # List operators
    CONS = ":"
    APPEND = "++"
    
    # Function composition
    COMPOSE = "."
    DOLLAR = "$"
    
    # Special
    NEWLINE = "NEWLINE"
    INDENT = "INDENT"
    DEDENT = "DEDENT"
    EOF = "EOF"
    COMMENT = "COMMENT"
    
    # UPLC-specific
    UPLC_PROGRAM = "program"
    UPLC_VERSION = "version"
    UPLC_TERM = "term"
    UPLC_VAR = "var"
    UPLC_LAMBDA_ABS = "lam"
    UPLC_APPLY = "apply"
    UPLC_CONSTANT = "con"
    UPLC_BUILTIN = "builtin"
    UPLC_FORCE = "force"
    UPLC_DELAY = "delay"
    UPLC_ERROR = "error"


@dataclass
class PlutusToken:
    """Represents a token in Plutus source code."""
    type: PlutusTokenType
    value: str
    line: int
    column: int
    position: int


class PlutusLexer:
    """Lexer for Plutus smart contract language."""
    
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        self.indent_stack = [0]
        
        # Haskell keywords
        self.keywords = {
            'module', 'import', 'qualified', 'as', 'hiding', 'where',
            'let', 'in', 'case', 'of', 'if', 'then', 'else', 'do',
            'data', 'newtype', 'type', 'class', 'instance', 'deriving',
            'validator', 'mintingPolicy', 'stakeValidator', 'builtin',
            'program', 'version', 'term', 'var', 'lam', 'apply',
            'con', 'force', 'delay', 'error', 'not'
        }
        
        # Builtin functions
        self.plutus_builtins = {
            'addInteger', 'subtractInteger', 'multiplyInteger', 'divideInteger',
            'quotientInteger', 'remainderInteger', 'modInteger', 'equalsInteger',
            'lessThanInteger', 'lessThanEqualsInteger', 'appendByteString',
            'consByteString', 'sliceByteString', 'lengthOfByteString',
            'indexByteString', 'equalsByteString', 'lessThanByteString',
            'lessThanEqualsByteString', 'sha2_256', 'sha3_256', 'blake2b_256',
            'verifyEd25519Signature', 'verifyEcdsaSecp256k1Signature',
            'appendString', 'equalsString', 'encodeUtf8', 'decodeUtf8',
            'ifThenElse', 'chooseUnit', 'trace', 'fstPair', 'sndPair',
            'chooseList', 'mkCons', 'headList', 'tailList', 'nullList',
            'chooseData', 'constrData', 'mapData', 'listData', 'iData', 'bData',
            'unConstrData', 'unMapData', 'unListData', 'unIData', 'unBData',
            'equalsData', 'mkPairData', 'mkNilData', 'mkNilPairData'
        }
    
    def current_char(self) -> Optional[str]:
        """Get current character."""
        if self.position >= len(self.source):
            return None
        return self.source[self.position]
    
    def peek_char(self, offset: int = 1) -> Optional[str]:
        """Peek at character ahead."""
        pos = self.position + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]
    
    def advance(self) -> None:
        """Advance position and update line/column."""
        if self.position < len(self.source):
            if self.source[self.position] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.position += 1
    
    def skip_whitespace(self) -> None:
        """Skip whitespace except newlines."""
        while self.current_char() and self.current_char() in ' \t\r':
            self.advance()
    
    def read_string(self, quote_char: str) -> str:
        """Read string literal."""
        value = ""
        self.advance()  # Skip opening quote
        
        while self.current_char() and self.current_char() != quote_char:
            if self.current_char() == '\\':
                self.advance()
                escaped = self.current_char()
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
                self.advance()
            else:
                value += self.current_char()
                self.advance()
        
        if self.current_char() == quote_char:
            self.advance()  # Skip closing quote
        
        return value
    
    def read_number(self) -> Tuple[str, PlutusTokenType]:
        """Read numeric literal."""
        value = ""
        token_type = PlutusTokenType.INTEGER
        
        # Read integer part
        while self.current_char() and self.current_char().isdigit():
            value += self.current_char()
            self.advance()
        
        # Check for rational number
        if self.current_char() == '.' and self.peek_char() and self.peek_char().isdigit():
            token_type = PlutusTokenType.RATIONAL
            value += self.current_char()
            self.advance()
            
            while self.current_char() and self.current_char().isdigit():
                value += self.current_char()
                self.advance()
        
        # Check for scientific notation
        if self.current_char() and self.current_char().lower() == 'e':
            token_type = PlutusTokenType.RATIONAL
            value += self.current_char()
            self.advance()
            
            if self.current_char() and self.current_char() in '+-':
                value += self.current_char()
                self.advance()
            
            while self.current_char() and self.current_char().isdigit():
                value += self.current_char()
                self.advance()
        
        return value, token_type
    
    def read_identifier(self) -> Tuple[str, PlutusTokenType]:
        """Read identifier or keyword."""
        value = ""
        
        # First character must be letter or underscore
        if self.current_char() and (self.current_char().isalpha() or self.current_char() == '_'):
            value += self.current_char()
            self.advance()
        
        # Subsequent characters can be alphanumeric, underscore, or apostrophe
        while (self.current_char() and 
               (self.current_char().isalnum() or self.current_char() in "_'")):
            value += self.current_char()
            self.advance()
        
        # Check for qualified identifier
        if self.current_char() == '.' and self.peek_char() and self.peek_char().isalpha():
            value += self.current_char()
            self.advance()
            
            while (self.current_char() and 
                   (self.current_char().isalnum() or self.current_char() in "_'")):
                value += self.current_char()
                self.advance()
            
            return value, PlutusTokenType.QUALIFIED_IDENTIFIER
        
        # Determine token type
        if value in self.keywords:
            return value, PlutusTokenType(value)
        elif value in self.plutus_builtins:
            return value, PlutusTokenType.BUILTIN
        elif value and value[0].isupper():
            return value, PlutusTokenType.CONSTRUCTOR
        else:
            return value, PlutusTokenType.IDENTIFIER
    
    def read_comment(self) -> str:
        """Read comment."""
        value = ""
        
        if self.current_char() == '-' and self.peek_char() == '-':
            # Line comment
            while self.current_char() and self.current_char() != '\n':
                value += self.current_char()
                self.advance()
        elif self.current_char() == '{' and self.peek_char() == '-':
            # Block comment
            self.advance()  # Skip {
            self.advance()  # Skip -
            value = "{-"
            
            while self.current_char():
                if self.current_char() == '-' and self.peek_char() == '}':
                    value += "-}"
                    self.advance()  # Skip -
                    self.advance()  # Skip }
                    break
                value += self.current_char()
                self.advance()
        
        return value
    
    def handle_indentation(self) -> List[PlutusToken]:
        """Handle indentation-based scoping."""
        tokens = []
        
        # Count leading whitespace
        indent_level = 0
        while self.current_char() and self.current_char() in ' \t':
            if self.current_char() == ' ':
                indent_level += 1
            else:  # tab
                indent_level += 8  # Assume tab = 8 spaces
            self.advance()
        
        current_indent = self.indent_stack[-1]
        
        if indent_level > current_indent:
            # Increased indentation
            self.indent_stack.append(indent_level)
            tokens.append(PlutusToken(
                PlutusTokenType.INDENT, "", self.line, self.column, self.position
            ))
        elif indent_level < current_indent:
            # Decreased indentation
            while self.indent_stack and self.indent_stack[-1] > indent_level:
                self.indent_stack.pop()
                tokens.append(PlutusToken(
                    PlutusTokenType.DEDENT, "", self.line, self.column, self.position
                ))
        
        return tokens
    
    def tokenize(self) -> List[PlutusToken]:
        """Tokenize the source code."""
        tokens = []
        
        while self.position < len(self.source):
            start_line = self.line
            start_column = self.column
            start_position = self.position
            
            char = self.current_char()
            
            if char is None:
                break
            
            # Handle newlines and indentation
            if char == '\n':
                tokens.append(PlutusToken(
                    PlutusTokenType.NEWLINE, char, start_line, start_column, start_position
                ))
                self.advance()
                
                # Handle indentation on next line
                if self.current_char() and self.current_char() in ' \t':
                    indent_tokens = self.handle_indentation()
                    tokens.extend(indent_tokens)
                continue
            
            # Skip whitespace
            if char in ' \t\r':
                self.skip_whitespace()
                continue
            
            # Comments
            if char == '-' and self.peek_char() == '-':
                comment = self.read_comment()
                tokens.append(PlutusToken(
                    PlutusTokenType.COMMENT, comment, start_line, start_column, start_position
                ))
                continue
            
            if char == '{' and self.peek_char() == '-':
                comment = self.read_comment()
                tokens.append(PlutusToken(
                    PlutusTokenType.COMMENT, comment, start_line, start_column, start_position
                ))
                continue
            
            # String literals
            if char in '"\'':
                string_value = self.read_string(char)
                token_type = PlutusTokenType.STRING if char == '"' else PlutusTokenType.CHAR
                tokens.append(PlutusToken(
                    token_type, string_value, start_line, start_column, start_position
                ))
                continue
            
            # Numbers
            if char.isdigit():
                number_value, number_type = self.read_number()
                tokens.append(PlutusToken(
                    number_type, number_value, start_line, start_column, start_position
                ))
                continue
            
            # Identifiers and keywords
            if char.isalpha() or char == '_':
                identifier, token_type = self.read_identifier()
                tokens.append(PlutusToken(
                    token_type, identifier, start_line, start_column, start_position
                ))
                continue
            
            # Two-character operators
            two_char = char + (self.peek_char() or '')
            if two_char in ['->','=>','::','==','/=','<=','>=','&&','||','++']:
                token_type = {
                    '->': PlutusTokenType.ARROW,
                    '=>': PlutusTokenType.DOUBLE_ARROW,
                    '::': PlutusTokenType.DOUBLE_COLON,
                    '==': PlutusTokenType.EQUAL,
                    '/=': PlutusTokenType.NOT_EQUAL,
                    '<=': PlutusTokenType.LESS_EQUAL,
                    '>=': PlutusTokenType.GREATER_EQUAL,
                    '&&': PlutusTokenType.AND,
                    '||': PlutusTokenType.OR,
                    '++': PlutusTokenType.APPEND,
                }[two_char]
                
                tokens.append(PlutusToken(
                    token_type, two_char, start_line, start_column, start_position
                ))
                self.advance()
                self.advance()
                continue
            
            # Single-character tokens
            single_char_tokens = {
                '(': PlutusTokenType.LPAREN,
                ')': PlutusTokenType.RPAREN,
                '[': PlutusTokenType.LBRACKET,
                ']': PlutusTokenType.RBRACKET,
                '{': PlutusTokenType.LBRACE,
                '}': PlutusTokenType.RBRACE,
                ',': PlutusTokenType.COMMA,
                ';': PlutusTokenType.SEMICOLON,
                ':': PlutusTokenType.COLON,
                '=': PlutusTokenType.EQUALS,
                '|': PlutusTokenType.PIPE,
                '_': PlutusTokenType.UNDERSCORE,
                '@': PlutusTokenType.AT,
                '\\': PlutusTokenType.LAMBDA,
                '.': PlutusTokenType.DOT,
                '+': PlutusTokenType.PLUS,
                '-': PlutusTokenType.MINUS,
                '*': PlutusTokenType.MULTIPLY,
                '/': PlutusTokenType.DIVIDE,
                '%': PlutusTokenType.MODULO,
                '^': PlutusTokenType.POWER,
                '<': PlutusTokenType.LESS_THAN,
                '>': PlutusTokenType.GREATER_THAN,
                '$': PlutusTokenType.DOLLAR,
            }
            
            if char in single_char_tokens:
                tokens.append(PlutusToken(
                    single_char_tokens[char], char, start_line, start_column, start_position
                ))
                self.advance()
                continue
            
            # Unknown character
            self.advance()
        
        # Close any remaining indentation levels
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            tokens.append(PlutusToken(
                PlutusTokenType.DEDENT, "", self.line, self.column, self.position
            ))
        
        tokens.append(PlutusToken(
            PlutusTokenType.EOF, "", self.line, self.column, self.position
        ))
        
        return tokens


class PlutusParser:
    """Recursive descent parser for Plutus smart contract language."""
    
    def __init__(self, tokens: List[PlutusToken]):
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[0] if tokens else None
        self.errors = []
    
    def error(self, message: str) -> None:
        """Add error message."""
        token_info = f"at line {self.current_token.line}, column {self.current_token.column}" if self.current_token else "at end of file"
        self.errors.append(f"Parser error {token_info}: {message}")
    
    def advance(self) -> None:
        """Advance to next token."""
        if self.position < len(self.tokens) - 1:
            self.position += 1
            self.current_token = self.tokens[self.position]
    
    def peek(self, offset: int = 1) -> Optional[PlutusToken]:
        """Peek at token ahead."""
        pos = self.position + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return None
    
    def match(self, token_type: PlutusTokenType) -> bool:
        """Check if current token matches type."""
        return self.current_token and self.current_token.type == token_type
    
    def consume(self, token_type: PlutusTokenType) -> Optional[PlutusToken]:
        """Consume token of expected type."""
        if self.match(token_type):
            token = self.current_token
            self.advance()
            return token
        else:
            expected = token_type.value if hasattr(token_type, 'value') else str(token_type)
            actual = self.current_token.type.value if self.current_token else "EOF"
            self.error(f"Expected {expected}, got {actual}")
            return None
    
    def skip_newlines(self) -> None:
        """Skip newline tokens."""
        while self.match(PlutusTokenType.NEWLINE):
            self.advance()
    
    def parse_program(self) -> PlutusProgram:
        """Parse complete Plutus program."""
        modules = []
        
        while not self.match(PlutusTokenType.EOF):
            self.skip_newlines()
            
            if self.match(PlutusTokenType.MODULE):
                module = self.parse_module()
                if module:
                    modules.append(module)
            else:
                # If no explicit module, create default module
                declarations = self.parse_declarations()
                default_module = PlutusModule(
                    name="Main",
                    imports=[],
                    exports=[],
                    declarations=declarations
                )
                modules.append(default_module)
                break
        
        return PlutusProgram(modules=modules)
    
    def parse_module(self) -> Optional[PlutusModule]:
        """Parse module declaration."""
        if not self.consume(PlutusTokenType.MODULE):
            return None
        
        # Module name
        if not self.match(PlutusTokenType.CONSTRUCTOR):
            self.error("Expected module name")
            return None
        
        module_name = self.current_token.value
        self.advance()
        
        # Optional export list
        exports = []
        if self.match(PlutusTokenType.LPAREN):
            exports = self.parse_export_list()
        
        if not self.consume(PlutusTokenType.WHERE):
            return None
        
        self.skip_newlines()
        
        # Parse imports and declarations
        imports = []
        declarations = []
        
        while not self.match(PlutusTokenType.EOF):
            self.skip_newlines()
            
            if self.match(PlutusTokenType.IMPORT):
                import_stmt = self.parse_import()
                if import_stmt:
                    imports.append(import_stmt)
            else:
                # Parse remaining declarations
                decl_list = self.parse_declarations()
                declarations.extend(decl_list)
                break
        
        return PlutusModule(
            name=module_name,
            imports=imports,
            exports=exports,
            declarations=declarations
        )
    
    def parse_import(self) -> Optional[PlutusImport]:
        """Parse import statement."""
        if not self.consume(PlutusTokenType.IMPORT):
            return None
        
        qualified = False
        if self.match(PlutusTokenType.QUALIFIED):
            qualified = True
            self.advance()
        
        # Module name
        if not self.match(PlutusTokenType.CONSTRUCTOR):
            self.error("Expected module name in import")
            return None
        
        module_name = self.current_token.value
        self.advance()
        
        # Optional alias
        alias = None
        if self.match(PlutusTokenType.AS):
            self.advance()
            if self.match(PlutusTokenType.CONSTRUCTOR):
                alias = self.current_token.value
                self.advance()
        
        # Optional import list
        imports = None
        if self.match(PlutusTokenType.LPAREN):
            imports = self.parse_import_list()
        
        return PlutusImport(
            module_name=module_name,
            qualified=qualified,
            alias=alias,
            imports=imports
        )
    
    def parse_declarations(self) -> List[PlutusDeclaration]:
        """Parse declaration list."""
        declarations = []
        
        while not self.match(PlutusTokenType.EOF):
            self.skip_newlines()
            
            if self.match(PlutusTokenType.DATA):
                decl = self.parse_data_declaration()
            elif self.match(PlutusTokenType.NEWTYPE):
                decl = self.parse_newtype_declaration()
            elif self.match(PlutusTokenType.TYPE):
                decl = self.parse_type_declaration()
            elif self.match(PlutusTokenType.VALIDATOR):
                decl = self.parse_validator()
            elif self.match(PlutusTokenType.MINTING_POLICY):
                decl = self.parse_minting_policy()
            elif self.match(PlutusTokenType.IDENTIFIER):
                # Could be function or value declaration
                decl = self.parse_value_or_function_declaration()
            else:
                break
            
            if decl:
                declarations.append(decl)
        
        return declarations
    
    def parse_data_declaration(self) -> Optional[PlutusDataDeclaration]:
        """Parse data type declaration."""
        if not self.consume(PlutusTokenType.DATA):
            return None
        
        # Type name
        if not self.match(PlutusTokenType.CONSTRUCTOR):
            self.error("Expected type name")
            return None
        
        type_name = self.current_token.value
        self.advance()
        
        # Type parameters
        type_params = []
        while self.match(PlutusTokenType.IDENTIFIER):
            type_params.append(self.current_token.value)
            self.advance()
        
        if not self.consume(PlutusTokenType.EQUALS):
            return None
        
        # Parse constructors
        constructors = self.parse_constructors()
        
        # Optional deriving clause
        deriving = []
        if self.match(PlutusTokenType.DERIVING):
            deriving = self.parse_deriving_clause()
        
        return PlutusDataDeclaration(
            name=type_name,
            type_parameters=type_params,
            constructors=constructors,
            deriving=deriving
        )
    
    def parse_constructors(self) -> List[PlutusConstructor]:
        """Parse data constructors."""
        constructors = []
        
        # First constructor
        constructor = self.parse_constructor()
        if constructor:
            constructors.append(constructor)
        
        # Additional constructors
        while self.match(PlutusTokenType.PIPE):
            self.advance()
            constructor = self.parse_constructor()
            if constructor:
                constructors.append(constructor)
        
        return constructors
    
    def parse_constructor(self) -> Optional[PlutusConstructor]:
        """Parse single constructor."""
        if not self.match(PlutusTokenType.CONSTRUCTOR):
            self.error("Expected constructor name")
            return None
        
        name = self.current_token.value
        self.advance()
        
        # Parse field types
        fields = []
        while (not self.match(PlutusTokenType.PIPE) and 
               not self.match(PlutusTokenType.DERIVING) and
               not self.match(PlutusTokenType.NEWLINE) and
               not self.match(PlutusTokenType.EOF)):
            
            field_type = self.parse_type()
            if field_type:
                fields.append(field_type)
            else:
                break
        
        return PlutusConstructor(name=name, fields=fields)
    
    def parse_type(self) -> Optional[PlutusType]:
        """Parse type expression."""
        return self.parse_function_type()
    
    def parse_function_type(self) -> Optional[PlutusType]:
        """Parse function type (with -> operator)."""
        left = self.parse_application_type()
        
        if self.match(PlutusTokenType.ARROW):
            self.advance()
            right = self.parse_function_type()
            if right:
                return PlutusFunctionType(domain=left, codomain=right)
        
        return left
    
    def parse_application_type(self) -> Optional[PlutusType]:
        """Parse type application."""
        base = self.parse_primary_type()
        
        args = []
        while (self.match(PlutusTokenType.CONSTRUCTOR) or 
               self.match(PlutusTokenType.IDENTIFIER) or
               self.match(PlutusTokenType.LPAREN)):
            arg = self.parse_primary_type()
            if arg:
                args.append(arg)
            else:
                break
        
        if args and isinstance(base, PlutusTypeConstructor):
            base.arguments.extend(args)
        
        return base
    
    def parse_primary_type(self) -> Optional[PlutusType]:
        """Parse primary type."""
        if self.match(PlutusTokenType.CONSTRUCTOR):
            name = self.current_token.value
            self.advance()
            return PlutusTypeConstructor(name=name)
        
        elif self.match(PlutusTokenType.IDENTIFIER):
            name = self.current_token.value
            self.advance()
            return PlutusTypeVariable(name=name)
        
        elif self.match(PlutusTokenType.LPAREN):
            self.advance()
            type_expr = self.parse_type()
            self.consume(PlutusTokenType.RPAREN)
            return type_expr
        
        return None
    
    def parse_validator(self) -> Optional[PlutusValidator]:
        """Parse validator declaration."""
        if not self.consume(PlutusTokenType.VALIDATOR):
            return None
        
        # Validator name
        if not self.match(PlutusTokenType.IDENTIFIER):
            self.error("Expected validator name")
            return None
        
        name = self.current_token.value
        self.advance()
        
        # Parameters
        params = []
        while self.match(PlutusTokenType.IDENTIFIER):
            params.append(self.current_token.value)
            self.advance()
        
        if not self.consume(PlutusTokenType.EQUALS):
            return None
        
        # Body expression
        body = self.parse_expression()
        
        return PlutusValidator(
            name=name,
            validator_type="spending",
            parameters=params,
            body=body
        )
    
    def parse_minting_policy(self) -> Optional[PlutusMintingPolicy]:
        """Parse minting policy declaration."""
        if not self.consume(PlutusTokenType.MINTING_POLICY):
            return None
        
        # Policy name
        if not self.match(PlutusTokenType.IDENTIFIER):
            self.error("Expected minting policy name")
            return None
        
        name = self.current_token.value
        self.advance()
        
        # Parameters
        params = []
        while self.match(PlutusTokenType.IDENTIFIER):
            params.append(self.current_token.value)
            self.advance()
        
        if not self.consume(PlutusTokenType.EQUALS):
            return None
        
        # Body expression
        body = self.parse_expression()
        
        return PlutusMintingPolicy(
            name=name,
            parameters=params,
            body=body
        )
    
    def parse_expression(self) -> Optional[PlutusExpression]:
        """Parse expression."""
        return self.parse_let_expression()
    
    def parse_let_expression(self) -> Optional[PlutusExpression]:
        """Parse let expression."""
        if self.match(PlutusTokenType.LET):
            self.advance()
            
            bindings = self.parse_bindings()
            
            if not self.consume(PlutusTokenType.IN):
                return None
            
            expr = self.parse_expression()
            
            return PlutusLetBinding(bindings=bindings, expression=expr)
        
        return self.parse_case_expression()
    
    def parse_case_expression(self) -> Optional[PlutusExpression]:
        """Parse case expression."""
        if self.match(PlutusTokenType.CASE):
            self.advance()
            
            expr = self.parse_expression()
            
            if not self.consume(PlutusTokenType.OF):
                return None
            
            alternatives = self.parse_alternatives()
            
            return PlutusCaseExpression(expression=expr, alternatives=alternatives)
        
        return self.parse_if_expression()
    
    def parse_if_expression(self) -> Optional[PlutusExpression]:
        """Parse if expression."""
        if self.match(PlutusTokenType.IF):
            self.advance()
            
            condition = self.parse_expression()
            
            if not self.consume(PlutusTokenType.THEN):
                return None
            
            then_expr = self.parse_expression()
            
            if not self.consume(PlutusTokenType.ELSE):
                return None
            
            else_expr = self.parse_expression()
            
            return PlutusIfExpression(
                condition=condition,
                then_expression=then_expr,
                else_expression=else_expr
            )
        
        return self.parse_lambda_expression()
    
    def parse_lambda_expression(self) -> Optional[PlutusExpression]:
        """Parse lambda expression."""
        if self.match(PlutusTokenType.LAMBDA):
            self.advance()
            
            params = []
            while self.match(PlutusTokenType.IDENTIFIER):
                params.append(self.current_token.value)
                self.advance()
            
            if not self.consume(PlutusTokenType.ARROW):
                return None
            
            body = self.parse_expression()
            
            return PlutusLambdaExpression(parameters=params, body=body)
        
        return self.parse_application_expression()
    
    def parse_application_expression(self) -> Optional[PlutusExpression]:
        """Parse function application."""
        left = self.parse_primary_expression()
        
        while (self.match(PlutusTokenType.IDENTIFIER) or
               self.match(PlutusTokenType.CONSTRUCTOR) or
               self.match(PlutusTokenType.INTEGER) or
               self.match(PlutusTokenType.STRING) or
               self.match(PlutusTokenType.LPAREN)):
            
            arg = self.parse_primary_expression()
            if arg:
                if isinstance(left, PlutusApplication):
                    left.arguments.append(arg)
                else:
                    left = PlutusApplication(function=left, arguments=[arg])
            else:
                break
        
        return left
    
    def parse_primary_expression(self) -> Optional[PlutusExpression]:
        """Parse primary expression."""
        # Literals
        if self.match(PlutusTokenType.INTEGER):
            value = int(self.current_token.value)
            self.advance()
            return PlutusLiteral(value=value, literal_type="integer")
        
        elif self.match(PlutusTokenType.RATIONAL):
            value = float(self.current_token.value)
            self.advance()
            return PlutusLiteral(value=value, literal_type="rational")
        
        elif self.match(PlutusTokenType.STRING):
            value = self.current_token.value
            self.advance()
            return PlutusLiteral(value=value, literal_type="string")
        
        elif self.match(PlutusTokenType.CHAR):
            value = self.current_token.value
            self.advance()
            return PlutusLiteral(value=value, literal_type="char")
        
        # Identifiers
        elif self.match(PlutusTokenType.IDENTIFIER):
            name = self.current_token.value
            self.advance()
            return PlutusVariableReference(name=name)
        
        elif self.match(PlutusTokenType.CONSTRUCTOR):
            name = self.current_token.value
            self.advance()
            return PlutusVariableReference(name=name)
        
        elif self.match(PlutusTokenType.BUILTIN):
            name = self.current_token.value
            self.advance()
            return PlutusBuiltinFunction(name=name, builtin_type="plutus")
        
        # Parenthesized expression
        elif self.match(PlutusTokenType.LPAREN):
            self.advance()
            expr = self.parse_expression()
            self.consume(PlutusTokenType.RPAREN)
            return expr
        
        return None
    
    def parse_bindings(self) -> List[PlutusBinding]:
        """Parse let bindings."""
        bindings = []
        
        # First binding
        binding = self.parse_binding()
        if binding:
            bindings.append(binding)
        
        # Additional bindings (separated by semicolons or newlines)
        while (self.match(PlutusTokenType.SEMICOLON) or 
               self.match(PlutusTokenType.NEWLINE)):
            self.advance()
            
            if (self.match(PlutusTokenType.IN) or 
                self.match(PlutusTokenType.EOF)):
                break
            
            binding = self.parse_binding()
            if binding:
                bindings.append(binding)
        
        return bindings
    
    def parse_binding(self) -> Optional[PlutusBinding]:
        """Parse single binding."""
        if not self.match(PlutusTokenType.IDENTIFIER):
            return None
        
        name = self.current_token.value
        self.advance()
        
        # Optional type signature
        type_sig = None
        if self.match(PlutusTokenType.DOUBLE_COLON):
            self.advance()
            type_sig = self.parse_type()
        
        if not self.consume(PlutusTokenType.EQUALS):
            return None
        
        expr = self.parse_expression()
        
        return PlutusBinding(
            name=name,
            expression=expr,
            type_signature=type_sig
        )
    
    def parse_alternatives(self) -> List[PlutusAlternative]:
        """Parse case alternatives."""
        alternatives = []
        
        # Parse alternatives with proper indentation handling
        while (not self.match(PlutusTokenType.EOF) and
               not self.match(PlutusTokenType.DEDENT)):
            
            pattern = self.parse_pattern()
            
            if not self.consume(PlutusTokenType.ARROW):
                break
            
            expr = self.parse_expression()
            
            if pattern and expr:
                alternatives.append(PlutusAlternative(pattern=pattern, expression=expr))
            
            # Skip optional semicolon or newline
            if self.match(PlutusTokenType.SEMICOLON):
                self.advance()
            self.skip_newlines()
        
        return alternatives
    
    def parse_pattern(self) -> Optional[PlutusPattern]:
        """Parse pattern."""
        if self.match(PlutusTokenType.IDENTIFIER):
            name = self.current_token.value
            self.advance()
            return PlutusVariablePattern(name=name)
        
        elif self.match(PlutusTokenType.CONSTRUCTOR):
            constructor = self.current_token.value
            self.advance()
            
            patterns = []
            while (self.match(PlutusTokenType.IDENTIFIER) or
                   self.match(PlutusTokenType.CONSTRUCTOR) or
                   self.match(PlutusTokenType.INTEGER) or
                   self.match(PlutusTokenType.LPAREN)):
                
                sub_pattern = self.parse_pattern()
                if sub_pattern:
                    patterns.append(sub_pattern)
                else:
                    break
            
            return PlutusConstructorPattern(constructor=constructor, patterns=patterns)
        
        elif self.match(PlutusTokenType.INTEGER):
            value = int(self.current_token.value)
            self.advance()
            return PlutusLiteralPattern(value=value, literal_type="integer")
        
        elif self.match(PlutusTokenType.UNDERSCORE):
            self.advance()
            return PlutusVariablePattern(name="_")
        
        return None


def parse_plutus(source: str) -> Tuple[Optional[PlutusProgram], List[str]]:
    """Parse Plutus source code."""
    lexer = PlutusLexer(source)
    tokens = lexer.tokenize()
    
    parser = PlutusParser(tokens)
    program = parser.parse_program()
    
    return program, parser.errors 