#!/usr/bin/env python3
"""
HCL Parser - Complete lexer and parser for HashiCorp Configuration Language

Provides comprehensive parsing capabilities for HCL including:
- Configuration blocks with labels and nested structure
- Attribute assignments with expressions
- String interpolation with ${} syntax
- Function calls and built-in functions
- Conditional expressions and for loops
- List and map literals
- Comments and documentation
- JSON compatibility mode

Supports HCL 1.0 and HCL 2.0 specifications as used in Terraform, Consul, Vault.
"""

import re
from typing import List, Dict, Optional, Any, Union, Tuple
from enum import Enum
from dataclasses import dataclass

from .hcl_ast import *


class TokenType(Enum):
    """HCL token types"""
    # Literals
    IDENTIFIER = "IDENTIFIER"
    STRING = "STRING"
    NUMBER = "NUMBER"
    BOOL_TRUE = "true"
    BOOL_FALSE = "false"
    NULL = "null"
    
    # String interpolation
    INTERPOLATION_START = "${"
    INTERPOLATION_END = "}"
    
    # Operators
    ASSIGN = "="
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    MODULO = "%"
    
    # Comparison
    EQUAL = "=="
    NOT_EQUAL = "!="
    LESS_THAN = "<"
    LESS_EQUAL = "<="
    GREATER_THAN = ">"
    GREATER_EQUAL = ">="
    
    # Logical
    AND = "&&"
    OR = "||"
    NOT = "!"
    
    # Conditional
    QUESTION = "?"
    COLON = ":"
    
    # Access
    DOT = "."
    ARROW = "=>"
    
    # Punctuation
    COMMA = ","
    SEMICOLON = ";"
    
    # Brackets
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
    LEFT_BRACKET = "["
    RIGHT_BRACKET = "]"
    LEFT_BRACE = "{"
    RIGHT_BRACE = "}"
    
    # Keywords
    FOR = "for"
    IN = "in"
    IF = "if"
    
    # Special
    NEWLINE = "NEWLINE"
    WHITESPACE = "WHITESPACE"
    COMMENT = "COMMENT"
    EOF = "EOF"
    
    # Heredoc
    HEREDOC_START = "<<"
    HEREDOC_IDENTIFIER = "HEREDOC_IDENTIFIER"


@dataclass
class Token:
    """HCL token representation"""
    type: TokenType
    value: str
    line: int
    column: int
    file: Optional[str] = None


class HCLLexer:
    """HCL lexer for tokenizing HCL source code"""
    
    KEYWORDS = {
        "true": TokenType.BOOL_TRUE,
        "false": TokenType.BOOL_FALSE,
        "null": TokenType.NULL,
        "for": TokenType.FOR,
        "in": TokenType.IN,
        "if": TokenType.IF,
    }
    
    # Token patterns
    PATTERNS = [
        # Whitespace and comments
        (r'\s+', TokenType.WHITESPACE),
        (r'#.*', TokenType.COMMENT),
        (r'//.*', TokenType.COMMENT),
        (r'/\*[\s\S]*?\*/', TokenType.COMMENT),
        
        # String interpolation
        (r'\$\{', TokenType.INTERPOLATION_START),
        
        # Heredoc
        (r'<<([A-Z_][A-Z0-9_]*)', TokenType.HEREDOC_START),
        
        # Multi-character operators
        (r'=>', TokenType.ARROW),
        (r'==', TokenType.EQUAL),
        (r'!=', TokenType.NOT_EQUAL),
        (r'<=', TokenType.LESS_EQUAL),
        (r'>=', TokenType.GREATER_EQUAL),
        (r'&&', TokenType.AND),
        (r'\|\|', TokenType.OR),
        
        # String literals (quoted)
        (r'"([^"\\]|\\.)*"', TokenType.STRING),
        (r"'([^'\\]|\\.)*'", TokenType.STRING),
        
        # Numeric literals
        (r'0[xX][0-9a-fA-F]+', TokenType.NUMBER),  # Hexadecimal
        (r'\d+\.\d+([eE][+-]?\d+)?', TokenType.NUMBER),  # Float
        (r'\d+([eE][+-]?\d+)?', TokenType.NUMBER),  # Integer
        
        # Single-character operators
        (r'=', TokenType.ASSIGN),
        (r'\+', TokenType.PLUS),
        (r'-', TokenType.MINUS),
        (r'\*', TokenType.MULTIPLY),
        (r'/', TokenType.DIVIDE),
        (r'%', TokenType.MODULO),
        (r'<', TokenType.LESS_THAN),
        (r'>', TokenType.GREATER_THAN),
        (r'!', TokenType.NOT),
        (r'\?', TokenType.QUESTION),
        (r':', TokenType.COLON),
        (r'\.', TokenType.DOT),
        (r',', TokenType.COMMA),
        (r';', TokenType.SEMICOLON),
        (r'\(', TokenType.LEFT_PAREN),
        (r'\)', TokenType.RIGHT_PAREN),
        (r'\[', TokenType.LEFT_BRACKET),
        (r'\]', TokenType.RIGHT_BRACKET),
        (r'\{', TokenType.LEFT_BRACE),
        (r'\}', TokenType.RIGHT_BRACE),
        
        # Identifiers (must be last)
        (r'[a-zA-Z_][a-zA-Z0-9_\-]*', TokenType.IDENTIFIER),
    ]
    
    def __init__(self, source: str, filename: Optional[str] = None):
        self.source = source
        self.filename = filename
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        self.interpolation_depth = 0
        self.heredoc_mode = False
        self.heredoc_identifier = ""
    
    def tokenize(self) -> List[Token]:
        """Tokenize the source code"""
        while self.position < len(self.source):
            if self.heredoc_mode:
                if not self._handle_heredoc():
                    break
            else:
                if not self._match_token():
                    raise SyntaxError(f"Unexpected character '{self.source[self.position]}' "
                                    f"at line {self.line}, column {self.column}")
        
        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column, self.filename))
        return self.tokens
    
    def _handle_heredoc(self) -> bool:
        """Handle heredoc content"""
        start_pos = self.position
        
        # Look for end of heredoc
        while self.position < len(self.source):
            line_start = self.position
            
            # Read to end of line
            while (self.position < len(self.source) and 
                   self.source[self.position] != '\n'):
                self.position += 1
            
            line_content = self.source[line_start:self.position]
            
            # Check if this line is the heredoc terminator
            if line_content.strip() == self.heredoc_identifier:
                # Add the heredoc content as a string token
                content = self.source[start_pos:line_start]
                self.tokens.append(Token(
                    TokenType.STRING, 
                    content.rstrip('\n'), 
                    self.line, 
                    self.column, 
                    self.filename
                ))
                
                # Add the terminator
                self.tokens.append(Token(
                    TokenType.HEREDOC_IDENTIFIER,
                    self.heredoc_identifier,
                    self.line,
                    self.column,
                    self.filename
                ))
                
                self.heredoc_mode = False
                self.heredoc_identifier = ""
                
                if self.position < len(self.source):
                    self._advance(1)  # Skip newline
                return True
            
            if self.position < len(self.source):
                self._advance(1)  # Skip newline
        
        # If we reach here, heredoc was not properly terminated
        raise SyntaxError(f"Unterminated heredoc starting at line {self.line}")
    
    def _match_token(self) -> bool:
        """Try to match a token at current position"""
        remaining = self.source[self.position:]
        
        # Handle interpolation end specially
        if (self.interpolation_depth > 0 and 
            remaining.startswith('}')):
            self.interpolation_depth -= 1
            token = Token(TokenType.RIGHT_BRACE, "}", self.line, self.column, self.filename)
            self.tokens.append(token)
            self._advance(1)
            return True
        
        for pattern, token_type in self.PATTERNS:
            match = re.match(pattern, remaining)
            if match:
                value = match.group(0)
                
                # Skip whitespace and comments in token stream
                if token_type not in (TokenType.WHITESPACE, TokenType.COMMENT):
                    # Handle special cases
                    if token_type == TokenType.IDENTIFIER:
                        # Check if it's a keyword
                        if value in self.KEYWORDS:
                            token_type = self.KEYWORDS[value]
                    
                    elif token_type == TokenType.INTERPOLATION_START:
                        self.interpolation_depth += 1
                    
                    elif token_type == TokenType.HEREDOC_START:
                        # Extract heredoc identifier
                        heredoc_match = re.match(r'<<([A-Z_][A-Z0-9_]*)', value)
                        if heredoc_match:
                            self.heredoc_identifier = heredoc_match.group(1)
                            self.heredoc_mode = True
                            # Add the heredoc start token
                            token = Token(token_type, "<<", self.line, self.column, self.filename)
                            self.tokens.append(token)
                            # Add the identifier token
                            self._advance(2)  # Skip <<
                            self.tokens.append(Token(
                                TokenType.HEREDOC_IDENTIFIER,
                                self.heredoc_identifier,
                                self.line,
                                self.column,
                                self.filename
                            ))
                            self._advance(len(self.heredoc_identifier))
                            return True
                    
                    # Create and add token
                    token = Token(token_type, value, self.line, self.column, self.filename)
                    self.tokens.append(token)
                
                # Update position
                self._advance(len(value))
                return True
        
        return False
    
    def _advance(self, count: int) -> None:
        """Advance position and update line/column"""
        for i in range(count):
            if self.position < len(self.source) and self.source[self.position] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.position += 1


class ParseError(Exception):
    """HCL parsing error"""
    
    def __init__(self, message: str, token: Optional[Token] = None):
        self.message = message
        self.token = token
        super().__init__(self._format_message())
    
    def _format_message(self) -> str:
        if self.token:
            return f"Parse error: {self.message} at line {self.token.line}, column {self.token.column}"
        return f"Parse error: {self.message}"


class HCLParser:
    """Recursive descent parser for HCL"""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.position = 0
        self.current_token = tokens[0] if tokens else None
    
    def parse(self) -> HCLConfiguration:
        """Parse tokens into HCL AST"""
        body = []
        
        while not self._is_at_end():
            item = self._parse_body_item()
            if item:
                body.append(item)
        
        return HCLConfiguration(body=body)
    
    def _parse_body_item(self) -> Optional[Union[HCLBlock, HCLAttribute, HCLComment]]:
        """Parse a body item (block, attribute, or comment)"""
        try:
            # Check if this is a block (identifier followed by labels and {)
            if self._check(TokenType.IDENTIFIER):
                # Look ahead to determine if this is a block or attribute
                if self._is_block_start():
                    return self._parse_block()
                else:
                    return self._parse_attribute()
            
            return None
        
        except ParseError as e:
            # Error recovery - skip to next item
            self._synchronize()
            return None
    
    def _is_block_start(self) -> bool:
        """Check if current position starts a block"""
        saved_pos = self.position
        
        # Skip block type identifier
        if self._check(TokenType.IDENTIFIER):
            self._advance()
            
            # Skip any labels (identifiers or strings)
            while (self._check(TokenType.IDENTIFIER) or self._check(TokenType.STRING)):
                self._advance()
            
            # Check if we see an opening brace
            is_block = self._check(TokenType.LEFT_BRACE)
            
            # Restore position
            self.position = saved_pos
            self.current_token = self.tokens[self.position]
            
            return is_block
        
        return False
    
    def _parse_block(self) -> HCLBlock:
        """Parse configuration block"""
        block_type = self._consume(TokenType.IDENTIFIER, "Expected block type").value
        
        # Parse labels
        labels = []
        while (self._check(TokenType.IDENTIFIER) or self._check(TokenType.STRING)):
            if self._check(TokenType.STRING):
                label = self._advance().value[1:-1]  # Remove quotes
            else:
                label = self._advance().value
            labels.append(label)
        
        # Parse body
        self._consume(TokenType.LEFT_BRACE, "Expected '{' to start block body")
        
        body = []
        while not self._check(TokenType.RIGHT_BRACE) and not self._is_at_end():
            item = self._parse_body_item()
            if item:
                body.append(item)
        
        self._consume(TokenType.RIGHT_BRACE, "Expected '}' to end block body")
        
        # Create specific block types for Terraform constructs
        if block_type == "variable" and len(labels) == 1:
            return self._create_variable_block(labels[0], body)
        elif block_type == "resource" and len(labels) == 2:
            return self._create_resource_block(labels[0], labels[1], body)
        elif block_type == "data" and len(labels) == 2:
            return self._create_data_source_block(labels[0], labels[1], body)
        elif block_type == "provider" and len(labels) <= 1:
            provider_name = labels[0] if labels else block_type
            return self._create_provider_block(provider_name, body)
        elif block_type == "output" and len(labels) == 1:
            return self._create_output_block(labels[0], body)
        elif block_type == "locals":
            return self._create_locals_block(body)
        elif block_type == "module" and len(labels) == 1:
            return self._create_module_block(labels[0], body)
        else:
            return HCLBlock(type=block_type, labels=labels, body=body)
    
    def _create_variable_block(self, name: str, body: List) -> HCLVariable:
        """Create Terraform variable block"""
        default = None
        description = None
        type_constraint = None
        sensitive = False
        nullable = True
        validation = []
        
        for item in body:
            if isinstance(item, HCLAttribute):
                if item.name == "default":
                    default = item.value
                elif item.name == "description":
                    if isinstance(item.value, HCLString):
                        description = "".join(str(p) for p in item.value.parts)
                elif item.name == "type":
                    type_constraint = str(item.value)
                elif item.name == "sensitive":
                    if isinstance(item.value, HCLBool):
                        sensitive = item.value.value
                elif item.name == "nullable":
                    if isinstance(item.value, HCLBool):
                        nullable = item.value.value
        
        return HCLVariable(
            type="variable",
            labels=[name],
            body=body,
            name=name,
            default=default,
            description=description,
            type_constraint=type_constraint,
            sensitive=sensitive,
            nullable=nullable,
            validation=validation
        )
    
    def _create_resource_block(self, resource_type: str, name: str, body: List) -> HCLResource:
        """Create Terraform resource block"""
        count = None
        for_each = None
        depends_on = []
        lifecycle = None
        provider = None
        
        for item in body:
            if isinstance(item, HCLAttribute):
                if item.name == "count":
                    count = item.value
                elif item.name == "for_each":
                    for_each = item.value
                elif item.name == "provider":
                    provider = str(item.value)
        
        return HCLResource(
            type="resource",
            labels=[resource_type, name],
            body=body,
            type=resource_type,
            name=name,
            provider=provider,
            count=count,
            for_each=for_each,
            depends_on=depends_on,
            lifecycle=lifecycle
        )
    
    def _create_data_source_block(self, data_type: str, name: str, body: List) -> HCLDataSource:
        """Create Terraform data source block"""
        count = None
        for_each = None
        depends_on = []
        provider = None
        
        for item in body:
            if isinstance(item, HCLAttribute):
                if item.name == "count":
                    count = item.value
                elif item.name == "for_each":
                    for_each = item.value
                elif item.name == "provider":
                    provider = str(item.value)
        
        return HCLDataSource(
            type="data",
            labels=[data_type, name],
            body=body,
            type=data_type,
            name=name,
            provider=provider,
            count=count,
            for_each=for_each,
            depends_on=depends_on
        )
    
    def _create_provider_block(self, name: str, body: List) -> HCLProvider:
        """Create Terraform provider block"""
        alias = None
        version = None
        
        for item in body:
            if isinstance(item, HCLAttribute):
                if item.name == "alias":
                    if isinstance(item.value, HCLString):
                        alias = "".join(str(p) for p in item.value.parts)
                elif item.name == "version":
                    if isinstance(item.value, HCLString):
                        version = "".join(str(p) for p in item.value.parts)
        
        return HCLProvider(
            type="provider",
            labels=[name],
            body=body,
            name=name,
            alias=alias,
            version=version
        )
    
    def _create_output_block(self, name: str, body: List) -> HCLOutput:
        """Create Terraform output block"""
        value = None
        description = None
        sensitive = False
        depends_on = []
        
        for item in body:
            if isinstance(item, HCLAttribute):
                if item.name == "value":
                    value = item.value
                elif item.name == "description":
                    if isinstance(item.value, HCLString):
                        description = "".join(str(p) for p in item.value.parts)
                elif item.name == "sensitive":
                    if isinstance(item.value, HCLBool):
                        sensitive = item.value.value
        
        return HCLOutput(
            type="output",
            labels=[name],
            body=body,
            name=name,
            value=value or HCLNull(),
            description=description,
            sensitive=sensitive,
            depends_on=depends_on
        )
    
    def _create_locals_block(self, body: List) -> HCLLocal:
        """Create Terraform locals block"""
        assignments = {}
        
        for item in body:
            if isinstance(item, HCLAttribute):
                assignments[item.name] = item.value
        
        return HCLLocal(
            type="locals",
            labels=[],
            body=body,
            assignments=assignments
        )
    
    def _create_module_block(self, name: str, body: List) -> HCLModule:
        """Create Terraform module block"""
        source = ""
        version = None
        
        for item in body:
            if isinstance(item, HCLAttribute):
                if item.name == "source":
                    if isinstance(item.value, HCLString):
                        source = "".join(str(p) for p in item.value.parts)
                elif item.name == "version":
                    if isinstance(item.value, HCLString):
                        version = "".join(str(p) for p in item.value.parts)
        
        return HCLModule(
            type="module",
            labels=[name],
            body=body,
            name=name,
            source=source,
            version=version
        )
    
    def _parse_attribute(self) -> HCLAttribute:
        """Parse attribute assignment"""
        name = self._consume(TokenType.IDENTIFIER, "Expected attribute name").value
        self._consume(TokenType.ASSIGN, "Expected '=' after attribute name")
        value = self._parse_expression()
        
        return HCLAttribute(name=name, value=value)
    
    def _parse_expression(self) -> HCLExpression:
        """Parse expression"""
        return self._parse_conditional()
    
    def _parse_conditional(self) -> HCLExpression:
        """Parse conditional expression (condition ? true_val : false_val)"""
        expr = self._parse_logical_or()
        
        if self._match(TokenType.QUESTION):
            true_value = self._parse_expression()
            self._consume(TokenType.COLON, "Expected ':' in conditional expression")
            false_value = self._parse_expression()
            return HCLConditional(expr, true_value, false_value)
        
        return expr
    
    def _parse_logical_or(self) -> HCLExpression:
        """Parse logical OR expression"""
        expr = self._parse_logical_and()
        
        while self._match(TokenType.OR):
            operator = self._previous().value
            right = self._parse_logical_and()
            expr = HCLBinaryOp(expr, operator, right)
        
        return expr
    
    def _parse_logical_and(self) -> HCLExpression:
        """Parse logical AND expression"""
        expr = self._parse_equality()
        
        while self._match(TokenType.AND):
            operator = self._previous().value
            right = self._parse_equality()
            expr = HCLBinaryOp(expr, operator, right)
        
        return expr
    
    def _parse_equality(self) -> HCLExpression:
        """Parse equality expression"""
        expr = self._parse_comparison()
        
        while self._match(TokenType.EQUAL, TokenType.NOT_EQUAL):
            operator = self._previous().value
            right = self._parse_comparison()
            expr = HCLBinaryOp(expr, operator, right)
        
        return expr
    
    def _parse_comparison(self) -> HCLExpression:
        """Parse comparison expression"""
        expr = self._parse_addition()
        
        while self._match(TokenType.LESS_THAN, TokenType.LESS_EQUAL,
                          TokenType.GREATER_THAN, TokenType.GREATER_EQUAL):
            operator = self._previous().value
            right = self._parse_addition()
            expr = HCLBinaryOp(expr, operator, right)
        
        return expr
    
    def _parse_addition(self) -> HCLExpression:
        """Parse addition/subtraction expression"""
        expr = self._parse_multiplication()
        
        while self._match(TokenType.PLUS, TokenType.MINUS):
            operator = self._previous().value
            right = self._parse_multiplication()
            expr = HCLBinaryOp(expr, operator, right)
        
        return expr
    
    def _parse_multiplication(self) -> HCLExpression:
        """Parse multiplication/division expression"""
        expr = self._parse_unary()
        
        while self._match(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            operator = self._previous().value
            right = self._parse_unary()
            expr = HCLBinaryOp(expr, operator, right)
        
        return expr
    
    def _parse_unary(self) -> HCLExpression:
        """Parse unary expression"""
        if self._match(TokenType.NOT, TokenType.MINUS):
            operator = self._previous().value
            expr = self._parse_unary()
            return HCLUnaryOp(operator, expr)
        
        return self._parse_postfix()
    
    def _parse_postfix(self) -> HCLExpression:
        """Parse postfix expression (function calls, indexing, field access)"""
        expr = self._parse_primary()
        
        while True:
            if self._match(TokenType.LEFT_BRACKET):
                # Index access
                index = self._parse_expression()
                self._consume(TokenType.RIGHT_BRACKET, "Expected ']' after index")
                expr = HCLIndexAccess(expr, index)
            
            elif self._match(TokenType.DOT):
                # Attribute access
                name = self._consume(TokenType.IDENTIFIER, "Expected attribute name").value
                expr = HCLAttributeAccess(expr, name)
            
            elif self._match(TokenType.LEFT_PAREN):
                # Function call
                args = []
                if not self._check(TokenType.RIGHT_PAREN):
                    args.append(self._parse_expression())
                    while self._match(TokenType.COMMA):
                        args.append(self._parse_expression())
                
                self._consume(TokenType.RIGHT_PAREN, "Expected ')' after arguments")
                
                # Convert identifier to function call
                if isinstance(expr, HCLIdentifier):
                    expr = HCLFunctionCall(expr.name, args)
                else:
                    # This shouldn't happen in valid HCL
                    raise ParseError("Invalid function call")
            
            else:
                break
        
        return expr
    
    def _parse_primary(self) -> HCLExpression:
        """Parse primary expression"""
        # Literals
        if self._match(TokenType.BOOL_TRUE):
            return HCLBool(True)
        
        if self._match(TokenType.BOOL_FALSE):
            return HCLBool(False)
        
        if self._match(TokenType.NULL):
            return HCLNull()
        
        if self._match(TokenType.NUMBER):
            value = self._previous().value
            try:
                if '.' in value or 'e' in value.lower():
                    return HCLNumber(float(value), value)
                else:
                    return HCLNumber(int(value, 0), value)  # Support hex with base 0
            except ValueError:
                raise ParseError(f"Invalid number: {value}")
        
        if self._match(TokenType.STRING):
            return self._parse_string_literal()
        
        if self._match(TokenType.IDENTIFIER):
            return HCLIdentifier(self._previous().value)
        
        # Collections
        if self._match(TokenType.LEFT_BRACKET):
            return self._parse_list()
        
        if self._match(TokenType.LEFT_BRACE):
            return self._parse_map_or_object()
        
        # Parenthesized expression
        if self._match(TokenType.LEFT_PAREN):
            expr = self._parse_expression()
            self._consume(TokenType.RIGHT_PAREN, "Expected ')' after expression")
            return expr
        
        # For expression
        if self._match(TokenType.FOR):
            return self._parse_for_expression()
        
        raise ParseError("Expected expression", self.current_token)
    
    def _parse_string_literal(self) -> HCLString:
        """Parse string literal with interpolation support"""
        raw_value = self._previous().value
        
        # Remove quotes
        if raw_value.startswith('"') and raw_value.endswith('"'):
            content = raw_value[1:-1]
        elif raw_value.startswith("'") and raw_value.endswith("'"):
            content = raw_value[1:-1]
        else:
            content = raw_value
        
        # Parse interpolations
        parts = []
        current = ""
        i = 0
        
        while i < len(content):
            if i < len(content) - 1 and content[i:i+2] == "${":
                # Found interpolation start
                if current:
                    parts.append(current)
                    current = ""
                
                # Find matching }
                brace_count = 1
                j = i + 2
                while j < len(content) and brace_count > 0:
                    if content[j] == '{':
                        brace_count += 1
                    elif content[j] == '}':
                        brace_count -= 1
                    j += 1
                
                if brace_count == 0:
                    # Parse the expression inside ${}
                    expr_text = content[i+2:j-1]
                    expr_tokens = HCLLexer(expr_text).tokenize()
                    expr_parser = HCLParser(expr_tokens)
                    expr = expr_parser._parse_expression()
                    parts.append(HCLInterpolation(expr))
                    i = j
                else:
                    # Unmatched brace, treat as literal
                    current += content[i]
                    i += 1
            else:
                current += content[i]
                i += 1
        
        if current:
            parts.append(current)
        
        return HCLString(parts)
    
    def _parse_list(self) -> HCLList:
        """Parse list literal"""
        elements = []
        
        if not self._check(TokenType.RIGHT_BRACKET):
            elements.append(self._parse_expression())
            while self._match(TokenType.COMMA):
                # Allow trailing comma
                if self._check(TokenType.RIGHT_BRACKET):
                    break
                elements.append(self._parse_expression())
        
        self._consume(TokenType.RIGHT_BRACKET, "Expected ']' after list elements")
        return HCLList(elements)
    
    def _parse_map_or_object(self) -> Union[HCLMap, HCLObject]:
        """Parse map or object literal"""
        pairs = []
        
        if not self._check(TokenType.RIGHT_BRACE):
            # Parse first key-value pair
            key = self._parse_expression()
            
            if self._match(TokenType.ASSIGN):
                # Object syntax: { key = value }
                value = self._parse_expression()
                pairs.append((key, value))
                
                while self._match(TokenType.COMMA):
                    if self._check(TokenType.RIGHT_BRACE):
                        break
                    key = self._parse_expression()
                    self._consume(TokenType.ASSIGN, "Expected '=' in object")
                    value = self._parse_expression()
                    pairs.append((key, value))
                
                self._consume(TokenType.RIGHT_BRACE, "Expected '}' after object")
                
                # Convert to object if all keys are identifiers or strings
                if all(isinstance(k, (HCLIdentifier, HCLString)) for k, v in pairs):
                    fields = {}
                    for k, v in pairs:
                        if isinstance(k, HCLIdentifier):
                            fields[k.name] = v
                        elif isinstance(k, HCLString):
                            key_str = "".join(str(p) for p in k.parts)
                            fields[key_str] = v
                    return HCLObject(fields)
                else:
                    return HCLMap(pairs)
            
            elif self._match(TokenType.COLON):
                # Map syntax: { key: value }
                value = self._parse_expression()
                pairs.append((key, value))
                
                while self._match(TokenType.COMMA):
                    if self._check(TokenType.RIGHT_BRACE):
                        break
                    key = self._parse_expression()
                    self._consume(TokenType.COLON, "Expected ':' in map")
                    value = self._parse_expression()
                    pairs.append((key, value))
                
                self._consume(TokenType.RIGHT_BRACE, "Expected '}' after map")
                return HCLMap(pairs)
            
            else:
                raise ParseError("Expected '=' or ':' after key in map/object")
        
        self._consume(TokenType.RIGHT_BRACE, "Expected '}' after empty map/object")
        return HCLObject({})
    
    def _parse_for_expression(self) -> HCLForExpression:
        """Parse for expression"""
        # Parse variable(s)
        value_var = self._consume(TokenType.IDENTIFIER, "Expected variable name").value
        key_var = None
        
        if self._match(TokenType.COMMA):
            key_var = value_var
            value_var = self._consume(TokenType.IDENTIFIER, "Expected value variable").value
        
        self._consume(TokenType.IN, "Expected 'in' in for expression")
        
        # Parse collection
        collection = self._parse_expression()
        
        self._consume(TokenType.COLON, "Expected ':' after collection")
        
        # Parse result expression
        key_expr = None
        value_expr = self._parse_expression()
        
        # Check for conditional
        condition = None
        if self._match(TokenType.IF):
            condition = self._parse_expression()
        
        # Determine if this is object or list for expression
        is_object = key_expr is not None
        
        return HCLForExpression(
            key_var=key_var,
            value_var=value_var,
            collection=collection,
            key_expr=key_expr,
            value_expr=value_expr,
            condition=condition,
            is_object=is_object
        )
    
    # Utility methods
    def _match(self, *types: TokenType) -> bool:
        """Check if current token matches any of the given types"""
        for token_type in types:
            if self._check(token_type):
                self._advance()
                return True
        return False
    
    def _check(self, token_type: TokenType) -> bool:
        """Check if current token is of given type"""
        if self._is_at_end():
            return False
        return self.current_token.type == token_type
    
    def _advance(self) -> Token:
        """Consume current token and return it"""
        if not self._is_at_end():
            self.position += 1
            if self.position < len(self.tokens):
                self.current_token = self.tokens[self.position]
        return self._previous()
    
    def _is_at_end(self) -> bool:
        """Check if we've reached end of tokens"""
        return self.current_token.type == TokenType.EOF
    
    def _previous(self) -> Token:
        """Return previous token"""
        return self.tokens[self.position - 1]
    
    def _consume(self, token_type: TokenType, message: str) -> Token:
        """Consume token of expected type or raise error"""
        if self._check(token_type):
            return self._advance()
        
        raise ParseError(message, self.current_token)
    
    def _synchronize(self) -> None:
        """Error recovery - skip to next block or attribute"""
        self._advance()
        
        while not self._is_at_end():
            if (self._check(TokenType.IDENTIFIER) or 
                self._check(TokenType.LEFT_BRACE) or
                self._check(TokenType.RIGHT_BRACE)):
                return
            
            self._advance()


def parse_hcl(source: str, filename: Optional[str] = None) -> HCLConfiguration:
    """Main entry point for parsing HCL source code"""
    try:
        lexer = HCLLexer(source, filename)
        tokens = lexer.tokenize()
        
        parser = HCLParser(tokens)
        return parser.parse()
    
    except Exception as e:
        raise ParseError(f"Failed to parse HCL code: {str(e)}") 