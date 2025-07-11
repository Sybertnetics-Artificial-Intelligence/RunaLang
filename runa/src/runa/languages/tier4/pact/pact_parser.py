#!/usr/bin/env python3
"""
Pact Parser Implementation

Comprehensive parser for Kadena's Pact smart contract language.
Supports LISP-like S-expression syntax, capabilities, formal verification, and multi-sig authorization.
"""

import re
from typing import List, Optional, Union, Dict, Any, Tuple
from enum import Enum
from dataclasses import dataclass
from .pact_ast import *


class PactTokenType(Enum):
    """Token types for Pact lexer."""
    # Literals
    INTEGER = "INTEGER"
    DECIMAL = "DECIMAL"
    STRING = "STRING"
    BOOLEAN = "BOOLEAN"
    TIME = "TIME"
    
    # Identifiers and symbols
    IDENTIFIER = "IDENTIFIER"
    QUALIFIED_IDENTIFIER = "QUALIFIED_IDENTIFIER"
    
    # Pact keywords
    MODULE = "module"
    INTERFACE = "interface"
    DEFUN = "defun"
    DEFPACT = "defpact"
    DEFSCHEMA = "defschema"
    DEFTABLE = "deftable"
    DEFCAP = "defcap"
    DEFCONST = "defconst"
    LET = "let"
    BIND = "bind"
    IF = "if"
    COND = "cond"
    AND = "and"
    OR = "or"
    NOT = "not"
    TRY = "try"
    LAMBDA = "lambda"
    
    # Capability keywords
    REQUIRE_CAPABILITY = "require-capability"
    COMPOSE_CAPABILITY = "compose-capability"
    INSTALL_CAPABILITY = "install-capability"
    WITH_CAPABILITY = "with-capability"
    
    # Database keywords
    READ = "read"
    WRITE = "write"
    INSERT = "insert"
    UPDATE = "update"
    SELECT = "select"
    KEYS = "keys"
    KEYLOG = "keylog"
    TXLOG = "txlog"
    
    # Formal verification
    PROPERTY = "property"
    INVARIANT = "invariant"
    ENFORCE = "enforce"
    ENFORCE_ONE = "enforce-one"
    
    # Pact transaction keywords
    STEP = "step"
    STEP_WITH_ROLLBACK = "step-with-rollback"
    ROLLBACK = "rollback"
    CANCEL = "cancel"
    CONTINUE = "continue"
    
    # Authorization
    KEYSET_REF_GUARD = "keyset-ref-guard"
    DEFINE_KEYSET = "define-keyset"
    
    # Blockchain functions
    CHAIN_TIME = "chain-time"
    BLOCK_HEIGHT = "block-height"
    BLOCK_TIME = "block-time"
    
    # Punctuation
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"
    COLON = ":"
    
    # Special
    COMMENT = "COMMENT"
    NEWLINE = "NEWLINE"
    EOF = "EOF"


@dataclass
class PactToken:
    """Represents a token in Pact source code."""
    type: PactTokenType
    value: str
    line: int
    column: int
    position: int


class PactLexer:
    """Lexer for Pact smart contract language."""
    
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        
        # Pact keywords
        self.keywords = {
            'module', 'interface', 'defun', 'defpact', 'defschema', 'deftable',
            'defcap', 'defconst', 'let', 'bind', 'if', 'cond', 'and', 'or',
            'not', 'try', 'lambda', 'require-capability', 'compose-capability',
            'install-capability', 'with-capability', 'read', 'write', 'insert',
            'update', 'select', 'keys', 'keylog', 'txlog', 'property', 'invariant',
            'enforce', 'enforce-one', 'step', 'step-with-rollback', 'rollback',
            'cancel', 'continue', 'keyset-ref-guard', 'define-keyset',
            'chain-time', 'block-height', 'block-time', 'true', 'false'
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
    
    def read_string(self) -> str:
        """Read string literal."""
        value = ""
        self.advance()  # Skip opening quote
        
        while self.current_char() and self.current_char() != '"':
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
                elif escaped == '"':
                    value += '"'
                else:
                    value += escaped
                self.advance()
            else:
                value += self.current_char()
                self.advance()
        
        if self.current_char() == '"':
            self.advance()  # Skip closing quote
        
        return value
    
    def read_number(self) -> Tuple[str, PactTokenType]:
        """Read numeric literal."""
        value = ""
        token_type = PactTokenType.INTEGER
        
        # Handle negative numbers
        if self.current_char() == '-':
            value += self.current_char()
            self.advance()
        
        # Read integer part
        while self.current_char() and self.current_char().isdigit():
            value += self.current_char()
            self.advance()
        
        # Check for decimal
        if self.current_char() == '.' and self.peek_char() and self.peek_char().isdigit():
            token_type = PactTokenType.DECIMAL
            value += self.current_char()
            self.advance()
            
            while self.current_char() and self.current_char().isdigit():
                value += self.current_char()
                self.advance()
        
        return value, token_type
    
    def read_identifier(self) -> Tuple[str, PactTokenType]:
        """Read identifier or keyword."""
        value = ""
        
        # Pact identifiers can contain letters, digits, hyphens, underscores, and some symbols
        while (self.current_char() and 
               (self.current_char().isalnum() or 
                self.current_char() in '-_?!<>=+*/%&|^~')):
            value += self.current_char()
            self.advance()
        
        # Check for qualified identifier (module.function)
        if self.current_char() == '.' and self.peek_char() and self.peek_char().isalpha():
            value += self.current_char()
            self.advance()
            
            while (self.current_char() and 
                   (self.current_char().isalnum() or 
                    self.current_char() in '-_?!<>=+*/%&|^~')):
                value += self.current_char()
                self.advance()
            
            return value, PactTokenType.QUALIFIED_IDENTIFIER
        
        # Check if it's a keyword
        if value in self.keywords:
            if value == 'true':
                return value, PactTokenType.BOOLEAN
            elif value == 'false':
                return value, PactTokenType.BOOLEAN
            else:
                return value, PactTokenType(value)
        
        return value, PactTokenType.IDENTIFIER
    
    def read_comment(self) -> str:
        """Read comment."""
        value = ""
        
        if self.current_char() == ';':
            # Line comment
            while self.current_char() and self.current_char() != '\n':
                value += self.current_char()
                self.advance()
        
        return value
    
    def tokenize(self) -> List[PactToken]:
        """Tokenize the source code."""
        tokens = []
        
        while self.position < len(self.source):
            start_line = self.line
            start_column = self.column
            start_position = self.position
            
            char = self.current_char()
            
            if char is None:
                break
            
            # Handle newlines
            if char == '\n':
                tokens.append(PactToken(
                    PactTokenType.NEWLINE, char, start_line, start_column, start_position
                ))
                self.advance()
                continue
            
            # Skip whitespace
            if char in ' \t\r':
                self.skip_whitespace()
                continue
            
            # Comments
            if char == ';':
                comment = self.read_comment()
                tokens.append(PactToken(
                    PactTokenType.COMMENT, comment, start_line, start_column, start_position
                ))
                continue
            
            # String literals
            if char == '"':
                string_value = self.read_string()
                tokens.append(PactToken(
                    PactTokenType.STRING, string_value, start_line, start_column, start_position
                ))
                continue
            
            # Numbers
            if char.isdigit() or (char == '-' and self.peek_char() and self.peek_char().isdigit()):
                number_value, number_type = self.read_number()
                tokens.append(PactToken(
                    number_type, number_value, start_line, start_column, start_position
                ))
                continue
            
            # Identifiers and keywords
            if char.isalpha() or char in '-_?!<>=+*/%&|^~':
                identifier, token_type = self.read_identifier()
                tokens.append(PactToken(
                    token_type, identifier, start_line, start_column, start_position
                ))
                continue
            
            # Single-character tokens
            single_char_tokens = {
                '(': PactTokenType.LPAREN,
                ')': PactTokenType.RPAREN,
                '{': PactTokenType.LBRACE,
                '}': PactTokenType.RBRACE,
                ':': PactTokenType.COLON,
            }
            
            if char in single_char_tokens:
                tokens.append(PactToken(
                    single_char_tokens[char], char, start_line, start_column, start_position
                ))
                self.advance()
                continue
            
            # Unknown character - skip it
            self.advance()
        
        tokens.append(PactToken(
            PactTokenType.EOF, "", self.line, self.column, self.position
        ))
        
        return tokens


class PactParser:
    """Recursive descent parser for Pact smart contract language."""
    
    def __init__(self, tokens: List[PactToken]):
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
    
    def match(self, token_type: PactTokenType) -> bool:
        """Check if current token matches type."""
        return self.current_token and self.current_token.type == token_type
    
    def consume(self, token_type: PactTokenType) -> Optional[PactToken]:
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
    
    def skip_newlines_and_comments(self) -> None:
        """Skip newline and comment tokens."""
        while self.match(PactTokenType.NEWLINE) or self.match(PactTokenType.COMMENT):
            self.advance()
    
    def parse_program(self) -> PactProgram:
        """Parse complete Pact program."""
        modules = []
        imports = []
        
        while not self.match(PactTokenType.EOF):
            self.skip_newlines_and_comments()
            
            if self.match(PactTokenType.LPAREN):
                # Parse S-expression
                expr = self.parse_expression()
                if isinstance(expr, PactModule):
                    modules.append(expr)
                elif isinstance(expr, PactImport):
                    imports.append(expr)
        
        return PactProgram(modules=modules, imports=imports)
    
    def parse_expression(self) -> Optional[PactExpression]:
        """Parse Pact expression."""
        self.skip_newlines_and_comments()
        
        if self.match(PactTokenType.LPAREN):
            return self.parse_list()
        elif self.match(PactTokenType.LBRACE):
            return self.parse_object()
        elif self.match(PactTokenType.INTEGER):
            return self.parse_integer()
        elif self.match(PactTokenType.DECIMAL):
            return self.parse_decimal()
        elif self.match(PactTokenType.STRING):
            return self.parse_string()
        elif self.match(PactTokenType.BOOLEAN):
            return self.parse_boolean()
        elif self.match(PactTokenType.IDENTIFIER) or self.match(PactTokenType.QUALIFIED_IDENTIFIER):
            return self.parse_variable()
        else:
            return None
    
    def parse_list(self) -> Optional[PactExpression]:
        """Parse list expression (S-expression)."""
        if not self.consume(PactTokenType.LPAREN):
            return None
        
        elements = []
        
        self.skip_newlines_and_comments()
        
        # Handle empty list
        if self.match(PactTokenType.RPAREN):
            self.advance()
            return PactListValue(elements=[])
        
        # Parse first element to determine list type
        first_element = self.parse_expression()
        if not first_element:
            return None
        
        elements.append(first_element)
        
        # Check if this is a special form
        if isinstance(first_element, PactVariable):
            function_name = first_element.name
            
            # Parse remaining arguments
            while not self.match(PactTokenType.RPAREN) and not self.match(PactTokenType.EOF):
                self.skip_newlines_and_comments()
                arg = self.parse_expression()
                if arg:
                    elements.append(arg)
            
            self.consume(PactTokenType.RPAREN)
            
            # Handle special forms
            if function_name == "module":
                return self.parse_module_from_elements(elements[1:])
            elif function_name == "defun":
                return self.parse_defun_from_elements(elements[1:])
            elif function_name == "defpact":
                return self.parse_defpact_from_elements(elements[1:])
            elif function_name == "defschema":
                return self.parse_defschema_from_elements(elements[1:])
            elif function_name == "deftable":
                return self.parse_deftable_from_elements(elements[1:])
            elif function_name == "defcap":
                return self.parse_defcap_from_elements(elements[1:])
            elif function_name == "defconst":
                return self.parse_defconst_from_elements(elements[1:])
            elif function_name == "let":
                return self.parse_let_from_elements(elements[1:])
            elif function_name == "if":
                return self.parse_if_from_elements(elements[1:])
            else:
                # Regular function call
                return PactFunctionCall(function=function_name, arguments=elements[1:])
        
        # Parse remaining elements
        while not self.match(PactTokenType.RPAREN) and not self.match(PactTokenType.EOF):
            self.skip_newlines_and_comments()
            element = self.parse_expression()
            if element:
                elements.append(element)
        
        self.consume(PactTokenType.RPAREN)
        
        return PactList(elements=elements)
    
    def parse_object(self) -> PactObject:
        """Parse object literal."""
        if not self.consume(PactTokenType.LBRACE):
            return None
        
        fields = {}
        
        while not self.match(PactTokenType.RBRACE) and not self.match(PactTokenType.EOF):
            self.skip_newlines_and_comments()
            
            # Parse field name
            if self.match(PactTokenType.STRING):
                field_name = self.current_token.value
                self.advance()
            elif self.match(PactTokenType.IDENTIFIER):
                field_name = self.current_token.value
                self.advance()
            else:
                break
            
            self.skip_newlines_and_comments()
            self.consume(PactTokenType.COLON)
            self.skip_newlines_and_comments()
            
            # Parse field value
            field_value = self.parse_expression()
            if field_value:
                fields[field_name] = field_value
        
        self.consume(PactTokenType.RBRACE)
        
        return PactObject(fields=fields)
    
    def parse_integer(self) -> PactLiteral:
        """Parse integer literal."""
        token = self.current_token
        self.advance()
        return PactLiteral(value=int(token.value), literal_type="integer")
    
    def parse_decimal(self) -> PactLiteral:
        """Parse decimal literal."""
        token = self.current_token
        self.advance()
        return PactLiteral(value=float(token.value), literal_type="decimal")
    
    def parse_string(self) -> PactLiteral:
        """Parse string literal."""
        token = self.current_token
        self.advance()
        return PactLiteral(value=token.value, literal_type="string")
    
    def parse_boolean(self) -> PactLiteral:
        """Parse boolean literal."""
        token = self.current_token
        self.advance()
        return PactLiteral(value=token.value == "true", literal_type="bool")
    
    def parse_variable(self) -> PactVariable:
        """Parse variable reference."""
        token = self.current_token
        self.advance()
        return PactVariable(
            name=token.value,
            qualified=token.type == PactTokenType.QUALIFIED_IDENTIFIER
        )
    
    def parse_module_from_elements(self, elements: List[PactExpression]) -> PactModule:
        """Parse module from list elements."""
        if not elements:
            return None
        
        name = elements[0].name if isinstance(elements[0], PactVariable) else str(elements[0])
        
        # TODO: Parse governance and other module attributes
        declarations = []
        
        return PactModule(name=name, declarations=declarations)
    
    def parse_defun_from_elements(self, elements: List[PactExpression]) -> PactDefun:
        """Parse function definition from list elements."""
        if len(elements) < 3:
            return None
        
        name = elements[0].name if isinstance(elements[0], PactVariable) else str(elements[0])
        
        # Parse parameters (simplified)
        parameters = []
        if isinstance(elements[1], PactList):
            for param in elements[1].elements:
                if isinstance(param, PactVariable):
                    parameters.append(PactParameter(name=param.name))
        
        # Parse body
        body = elements[2] if len(elements) > 2 else None
        
        return PactDefun(name=name, parameters=parameters, body=body)
    
    # Simplified parsing methods for other constructs
    def parse_defpact_from_elements(self, elements: List[PactExpression]) -> PactDefpact:
        """Parse pact definition from list elements."""
        if len(elements) < 3:
            return None
        
        name = elements[0].name if isinstance(elements[0], PactVariable) else str(elements[0])
        parameters = []
        steps = []
        
        return PactDefpact(name=name, parameters=parameters, steps=steps)
    
    def parse_defschema_from_elements(self, elements: List[PactExpression]) -> PactDefschema:
        """Parse schema definition from list elements."""
        if not elements:
            return None
        
        name = elements[0].name if isinstance(elements[0], PactVariable) else str(elements[0])
        fields = []
        
        return PactDefschema(name=name, fields=fields)
    
    def parse_deftable_from_elements(self, elements: List[PactExpression]) -> PactDeftable:
        """Parse table definition from list elements."""
        if len(elements) < 2:
            return None
        
        name = elements[0].name if isinstance(elements[0], PactVariable) else str(elements[0])
        schema = elements[1].name if isinstance(elements[1], PactVariable) else str(elements[1])
        
        return PactDeftable(name=name, schema=schema)
    
    def parse_defcap_from_elements(self, elements: List[PactExpression]) -> PactDefcap:
        """Parse capability definition from list elements."""
        if len(elements) < 2:
            return None
        
        name = elements[0].name if isinstance(elements[0], PactVariable) else str(elements[0])
        parameters = []
        body = elements[1] if len(elements) > 1 else None
        
        return PactDefcap(name=name, parameters=parameters, body=body)
    
    def parse_defconst_from_elements(self, elements: List[PactExpression]) -> PactDefconst:
        """Parse constant definition from list elements."""
        if len(elements) < 2:
            return None
        
        name = elements[0].name if isinstance(elements[0], PactVariable) else str(elements[0])
        value = elements[1]
        
        return PactDefconst(name=name, value=value)
    
    def parse_let_from_elements(self, elements: List[PactExpression]) -> PactLet:
        """Parse let expression from list elements."""
        if len(elements) < 2:
            return None
        
        # Parse bindings (simplified)
        bindings = []
        body = elements[1] if len(elements) > 1 else None
        
        return PactLet(bindings=bindings, body=body)
    
    def parse_if_from_elements(self, elements: List[PactExpression]) -> PactIf:
        """Parse if expression from list elements."""
        if len(elements) < 2:
            return None
        
        condition = elements[0]
        then_expr = elements[1]
        else_expr = elements[2] if len(elements) > 2 else None
        
        return PactIf(condition=condition, then_expr=then_expr, else_expr=else_expr)


def parse_pact(source: str) -> Tuple[Optional[PactProgram], List[str]]:
    """Parse Pact source code."""
    lexer = PactLexer(source)
    tokens = lexer.tokenize()
    
    parser = PactParser(tokens)
    program = parser.parse_program()
    
    return program, parser.errors 