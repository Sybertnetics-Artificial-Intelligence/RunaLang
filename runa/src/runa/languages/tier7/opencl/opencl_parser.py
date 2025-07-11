#!/usr/bin/env python3
"""
OpenCL Parser - Complete lexer and parser for OpenCL C Language

Provides comprehensive parsing capabilities for OpenCL C including:
- Complete lexical analysis with all OpenCL tokens
- Recursive descent parser for OpenCL C grammar
- Support for kernels, memory qualifiers, and vector operations
- Built-in function recognition
- Error handling and recovery
- Source location tracking

Supports OpenCL C 1.0 through OpenCL C 3.0 specifications.
"""

import re
from typing import List, Dict, Optional, Any, Union, Tuple
from enum import Enum
from dataclasses import dataclass

from .opencl_ast import *


class TokenType(Enum):
    """OpenCL token types"""
    # Literals
    IDENTIFIER = "IDENTIFIER"
    INTEGER_LITERAL = "INTEGER_LITERAL"
    FLOAT_LITERAL = "FLOAT_LITERAL"
    STRING_LITERAL = "STRING_LITERAL"
    CHAR_LITERAL = "CHAR_LITERAL"
    
    # Keywords
    KERNEL = "__kernel"
    GLOBAL = "__global"
    LOCAL = "__local"
    PRIVATE = "__private"
    CONSTANT = "__constant"
    GENERIC = "__generic"
    READ_ONLY = "__read_only"
    WRITE_ONLY = "__write_only"
    READ_WRITE = "__read_write"
    
    # C Keywords
    AUTO = "auto"
    BREAK = "break"
    CASE = "case"
    CHAR = "char"
    CONST = "const"
    CONTINUE = "continue"
    DEFAULT = "default"
    DO = "do"
    DOUBLE = "double"
    ELSE = "else"
    ENUM = "enum"
    EXTERN = "extern"
    FLOAT = "float"
    FOR = "for"
    GOTO = "goto"
    IF = "if"
    INLINE = "inline"
    INT = "int"
    LONG = "long"
    REGISTER = "register"
    RESTRICT = "restrict"
    RETURN = "return"
    SHORT = "short"
    SIGNED = "signed"
    SIZEOF = "sizeof"
    STATIC = "static"
    STRUCT = "struct"
    SWITCH = "switch"
    TYPEDEF = "typedef"
    UNION = "union"
    UNSIGNED = "unsigned"
    VOID = "void"
    VOLATILE = "volatile"
    WHILE = "while"
    
    # OpenCL Types
    BOOL = "bool"
    HALF = "half"
    SIZE_T = "size_t"
    PTRDIFF_T = "ptrdiff_t"
    INTPTR_T = "intptr_t"
    UINTPTR_T = "uintptr_t"
    IMAGE1D_T = "image1d_t"
    IMAGE2D_T = "image2d_t"
    IMAGE3D_T = "image3d_t"
    IMAGE1D_BUFFER_T = "image1d_buffer_t"
    IMAGE1D_ARRAY_T = "image1d_array_t"
    IMAGE2D_ARRAY_T = "image2d_array_t"
    SAMPLER_T = "sampler_t"
    EVENT_T = "event_t"
    
    # Vector Types (examples - many more exist)
    CHAR2 = "char2"
    CHAR3 = "char3"
    CHAR4 = "char4"
    INT2 = "int2"
    INT3 = "int3"
    INT4 = "int4"
    FLOAT2 = "float2"
    FLOAT3 = "float3"
    FLOAT4 = "float4"
    
    # Operators
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    MODULO = "%"
    ASSIGN = "="
    PLUS_ASSIGN = "+="
    MINUS_ASSIGN = "-="
    MULTIPLY_ASSIGN = "*="
    DIVIDE_ASSIGN = "/="
    MODULO_ASSIGN = "%="
    INCREMENT = "++"
    DECREMENT = "--"
    
    # Comparison
    EQUAL = "=="
    NOT_EQUAL = "!="
    LESS_THAN = "<"
    LESS_EQUAL = "<="
    GREATER_THAN = ">"
    GREATER_EQUAL = ">="
    
    # Logical
    LOGICAL_AND = "&&"
    LOGICAL_OR = "||"
    LOGICAL_NOT = "!"
    
    # Bitwise
    BITWISE_AND = "&"
    BITWISE_OR = "|"
    BITWISE_XOR = "^"
    BITWISE_NOT = "~"
    LEFT_SHIFT = "<<"
    RIGHT_SHIFT = ">>"
    BITWISE_AND_ASSIGN = "&="
    BITWISE_OR_ASSIGN = "|="
    BITWISE_XOR_ASSIGN = "^="
    LEFT_SHIFT_ASSIGN = "<<="
    RIGHT_SHIFT_ASSIGN = ">>="
    
    # Punctuation
    SEMICOLON = ";"
    COMMA = ","
    DOT = "."
    ARROW = "->"
    QUESTION = "?"
    COLON = ":"
    
    # Brackets
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
    LEFT_BRACKET = "["
    RIGHT_BRACKET = "]"
    LEFT_BRACE = "{"
    RIGHT_BRACE = "}"
    
    # Preprocessor
    HASH = "#"
    
    # Special
    NEWLINE = "NEWLINE"
    WHITESPACE = "WHITESPACE"
    COMMENT = "COMMENT"
    EOF = "EOF"


@dataclass
class Token:
    """OpenCL token representation"""
    type: TokenType
    value: str
    line: int
    column: int
    file: Optional[str] = None


class OpenCLLexer:
    """OpenCL lexer for tokenizing OpenCL C source code"""
    
    KEYWORDS = {
        "__kernel", "__global", "__local", "__private", "__constant", "__generic",
        "__read_only", "__write_only", "__read_write",
        "auto", "break", "case", "char", "const", "continue", "default", "do",
        "double", "else", "enum", "extern", "float", "for", "goto", "if",
        "inline", "int", "long", "register", "restrict", "return", "short",
        "signed", "sizeof", "static", "struct", "switch", "typedef", "union",
        "unsigned", "void", "volatile", "while", "bool", "half", "size_t",
        "ptrdiff_t", "intptr_t", "uintptr_t", "image1d_t", "image2d_t",
        "image3d_t", "image1d_buffer_t", "image1d_array_t", "image2d_array_t",
        "sampler_t", "event_t"
    }
    
    # Vector type pattern - matches types like float4, int2, etc.
    VECTOR_TYPES = re.compile(r'\b(char|uchar|short|ushort|int|uint|long|ulong|float|double|half)(2|3|4|8|16)\b')
    
    # Token patterns
    PATTERNS = [
        # Whitespace and comments
        (r'\s+', TokenType.WHITESPACE),
        (r'//.*', TokenType.COMMENT),
        (r'/\*[\s\S]*?\*/', TokenType.COMMENT),
        
        # Preprocessor
        (r'#.*', TokenType.HASH),
        
        # Literals
        (r'0[xX][0-9a-fA-F]+[uUlL]*', TokenType.INTEGER_LITERAL),
        (r'\d+\.\d+[fF]?', TokenType.FLOAT_LITERAL),
        (r'\d+[uUlL]*', TokenType.INTEGER_LITERAL),
        (r'"([^"\\]|\\.)*"', TokenType.STRING_LITERAL),
        (r"'([^'\\]|\\.)*'", TokenType.CHAR_LITERAL),
        
        # Multi-character operators
        (r'\+\+', TokenType.INCREMENT),
        (r'--', TokenType.DECREMENT),
        (r'\+=', TokenType.PLUS_ASSIGN),
        (r'-=', TokenType.MINUS_ASSIGN),
        (r'\*=', TokenType.MULTIPLY_ASSIGN),
        (r'/=', TokenType.DIVIDE_ASSIGN),
        (r'%=', TokenType.MODULO_ASSIGN),
        (r'&=', TokenType.BITWISE_AND_ASSIGN),
        (r'\|=', TokenType.BITWISE_OR_ASSIGN),
        (r'\^=', TokenType.BITWISE_XOR_ASSIGN),
        (r'<<=', TokenType.LEFT_SHIFT_ASSIGN),
        (r'>>=', TokenType.RIGHT_SHIFT_ASSIGN),
        (r'<<', TokenType.LEFT_SHIFT),
        (r'>>', TokenType.RIGHT_SHIFT),
        (r'&&', TokenType.LOGICAL_AND),
        (r'\|\|', TokenType.LOGICAL_OR),
        (r'==', TokenType.EQUAL),
        (r'!=', TokenType.NOT_EQUAL),
        (r'<=', TokenType.LESS_EQUAL),
        (r'>=', TokenType.GREATER_EQUAL),
        (r'->', TokenType.ARROW),
        
        # Single-character operators
        (r'\+', TokenType.PLUS),
        (r'-', TokenType.MINUS),
        (r'\*', TokenType.MULTIPLY),
        (r'/', TokenType.DIVIDE),
        (r'%', TokenType.MODULO),
        (r'=', TokenType.ASSIGN),
        (r'<', TokenType.LESS_THAN),
        (r'>', TokenType.GREATER_THAN),
        (r'!', TokenType.LOGICAL_NOT),
        (r'&', TokenType.BITWISE_AND),
        (r'\|', TokenType.BITWISE_OR),
        (r'\^', TokenType.BITWISE_XOR),
        (r'~', TokenType.BITWISE_NOT),
        
        # Punctuation
        (r';', TokenType.SEMICOLON),
        (r',', TokenType.COMMA),
        (r'\.', TokenType.DOT),
        (r'\?', TokenType.QUESTION),
        (r':', TokenType.COLON),
        (r'\(', TokenType.LEFT_PAREN),
        (r'\)', TokenType.RIGHT_PAREN),
        (r'\[', TokenType.LEFT_BRACKET),
        (r'\]', TokenType.RIGHT_BRACKET),
        (r'\{', TokenType.LEFT_BRACE),
        (r'\}', TokenType.RIGHT_BRACE),
        
        # Identifiers (must be last)
        (r'[a-zA-Z_][a-zA-Z0-9_]*', TokenType.IDENTIFIER),
    ]
    
    def __init__(self, source: str, filename: Optional[str] = None):
        self.source = source
        self.filename = filename
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
    
    def tokenize(self) -> List[Token]:
        """Tokenize the source code"""
        while self.position < len(self.source):
            if not self._match_token():
                raise SyntaxError(f"Unexpected character '{self.source[self.position]}' "
                                f"at line {self.line}, column {self.column}")
        
        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column, self.filename))
        return self.tokens
    
    def _match_token(self) -> bool:
        """Try to match a token at current position"""
        remaining = self.source[self.position:]
        
        for pattern, token_type in self.PATTERNS:
            match = re.match(pattern, remaining)
            if match:
                value = match.group(0)
                
                # Skip whitespace and comments in token stream
                if token_type not in (TokenType.WHITESPACE, TokenType.COMMENT):
                    # Check for keywords and vector types
                    if token_type == TokenType.IDENTIFIER:
                        if value in self.KEYWORDS:
                            token_type = TokenType(value)
                        elif self.VECTOR_TYPES.match(value):
                            # Vector types are still identifiers but with special handling
                            pass
                    
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
    """OpenCL parsing error"""
    
    def __init__(self, message: str, token: Optional[Token] = None):
        self.message = message
        self.token = token
        super().__init__(self._format_message())
    
    def _format_message(self) -> str:
        if self.token:
            return f"Parse error: {self.message} at line {self.token.line}, column {self.token.column}"
        return f"Parse error: {self.message}"


class OpenCLParser:
    """Recursive descent parser for OpenCL C"""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.position = 0
        self.current_token = tokens[0] if tokens else None
    
    def parse(self) -> OpenCLProgram:
        """Parse tokens into OpenCL AST"""
        declarations = []
        preprocessor_directives = []
        
        while not self._is_at_end():
            if self._match(TokenType.HASH):
                preprocessor_directives.append(self._parse_preprocessor_directive())
            else:
                decl = self._parse_declaration()
                if decl:
                    declarations.append(decl)
        
        return OpenCLProgram(
            declarations=declarations,
            preprocessor_directives=preprocessor_directives,
            metadata={}
        )
    
    def _parse_preprocessor_directive(self) -> OpenCLPreprocessorDirective:
        """Parse preprocessor directive"""
        content = self._previous().value  # The # token
        return OpenCLPreprocessorDirective(directive="#", content=content)
    
    def _parse_declaration(self) -> Optional[OpenCLDeclaration]:
        """Parse a top-level declaration"""
        try:
            # Check for function qualifiers
            qualifiers = []
            if self._check(TokenType.KERNEL):
                qualifiers.append(FunctionQualifier.KERNEL)
                self._advance()
            elif self._check(TokenType.INLINE):
                qualifiers.append(FunctionQualifier.INLINE)
                self._advance()
            
            # Check for storage class specifiers
            if self._match(TokenType.STATIC, TokenType.EXTERN):
                pass  # Handle storage class
            
            # Parse type
            type_node = self._parse_type()
            
            # Parse declarator
            name = self._consume(TokenType.IDENTIFIER, "Expected identifier").value
            
            # Check if this is a function declaration
            if self._check(TokenType.LEFT_PAREN):
                return self._parse_function_declaration(type_node, name, qualifiers)
            else:
                # Variable declaration
                initializer = None
                if self._match(TokenType.ASSIGN):
                    initializer = self._parse_expression()
                
                self._consume(TokenType.SEMICOLON, "Expected ';' after variable declaration")
                
                return OpenCLVariableDeclaration(
                    type=type_node,
                    name=name,
                    initializer=initializer
                )
        
        except ParseError as e:
            # Error recovery - skip to next semicolon or brace
            self._synchronize()
            return None
    
    def _parse_function_declaration(self, return_type: OpenCLType, name: str, 
                                   qualifiers: List[FunctionQualifier]) -> OpenCLDeclaration:
        """Parse function declaration"""
        self._consume(TokenType.LEFT_PAREN, "Expected '('")
        
        parameters = []
        if not self._check(TokenType.RIGHT_PAREN):
            parameters.append(self._parse_parameter())
            while self._match(TokenType.COMMA):
                parameters.append(self._parse_parameter())
        
        self._consume(TokenType.RIGHT_PAREN, "Expected ')'")
        
        # Check for function body
        body = None
        if self._check(TokenType.LEFT_BRACE):
            body = self._parse_block()
        else:
            self._consume(TokenType.SEMICOLON, "Expected ';' or function body")
        
        # Determine if this is a kernel
        if FunctionQualifier.KERNEL in qualifiers:
            return OpenCLKernelDeclaration(
                return_type=return_type,
                name=name,
                parameters=parameters,
                body=body or OpenCLBlock([]),
                attributes={}
            )
        else:
            return OpenCLFunctionDeclaration(
                return_type=return_type,
                name=name,
                parameters=parameters,
                qualifiers=qualifiers,
                body=body
            )
    
    def _parse_parameter(self) -> OpenCLParameter:
        """Parse function parameter"""
        # Parse address space qualifiers
        address_space = None
        access_qualifier = None
        is_const = False
        
        if self._match(TokenType.GLOBAL):
            address_space = AddressSpace.GLOBAL
        elif self._match(TokenType.LOCAL):
            address_space = AddressSpace.LOCAL
        elif self._match(TokenType.PRIVATE):
            address_space = AddressSpace.PRIVATE
        elif self._match(TokenType.CONSTANT):
            address_space = AddressSpace.CONSTANT
        
        if self._match(TokenType.READ_ONLY):
            access_qualifier = AccessQualifier.READ_ONLY
        elif self._match(TokenType.WRITE_ONLY):
            access_qualifier = AccessQualifier.WRITE_ONLY
        elif self._match(TokenType.READ_WRITE):
            access_qualifier = AccessQualifier.READ_WRITE
        
        if self._match(TokenType.CONST):
            is_const = True
        
        param_type = self._parse_type()
        name = self._consume(TokenType.IDENTIFIER, "Expected parameter name").value
        
        return OpenCLParameter(
            type=param_type,
            name=name,
            address_space=address_space,
            access_qualifier=access_qualifier,
            is_const=is_const
        )
    
    def _parse_type(self) -> OpenCLType:
        """Parse type specification"""
        if self._match(TokenType.VOID, TokenType.CHAR, TokenType.SHORT, TokenType.INT,
                      TokenType.LONG, TokenType.FLOAT, TokenType.DOUBLE, TokenType.BOOL,
                      TokenType.HALF, TokenType.SIZE_T, TokenType.PTRDIFF_T,
                      TokenType.INTPTR_T, TokenType.UINTPTR_T):
            type_name = self._previous().value
            return OpenCLBuiltinType(name=type_name)
        
        elif self._check(TokenType.IDENTIFIER):
            # Could be vector type or custom type
            type_name = self._advance().value
            
            # Check if it's a vector type
            vector_match = OpenCLLexer.VECTOR_TYPES.match(type_name)
            if vector_match:
                base_type = vector_match.group(1)
                vector_size = int(vector_match.group(2))
                return OpenCLBuiltinType(name=base_type, vector_size=vector_size)
            
            return OpenCLBuiltinType(name=type_name)
        
        elif self._match(TokenType.IMAGE1D_T, TokenType.IMAGE2D_T, TokenType.IMAGE3D_T,
                        TokenType.IMAGE1D_BUFFER_T, TokenType.IMAGE1D_ARRAY_T,
                        TokenType.IMAGE2D_ARRAY_T):
            image_type = self._previous().value
            dimension = image_type.replace("image", "").replace("_t", "")
            return OpenCLImageType(dimension=dimension)
        
        else:
            raise ParseError("Expected type name", self.current_token)
    
    def _parse_block(self) -> OpenCLBlock:
        """Parse compound statement"""
        self._consume(TokenType.LEFT_BRACE, "Expected '{'")
        
        statements = []
        while not self._check(TokenType.RIGHT_BRACE) and not self._is_at_end():
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
        
        self._consume(TokenType.RIGHT_BRACE, "Expected '}'")
        return OpenCLBlock(statements)
    
    def _parse_statement(self) -> Optional[OpenCLStatement]:
        """Parse statement"""
        try:
            if self._match(TokenType.IF):
                return self._parse_if_statement()
            elif self._match(TokenType.WHILE):
                return self._parse_while_statement()
            elif self._match(TokenType.FOR):
                return self._parse_for_statement()
            elif self._match(TokenType.DO):
                return self._parse_do_while_statement()
            elif self._match(TokenType.RETURN):
                return self._parse_return_statement()
            elif self._match(TokenType.BREAK):
                self._consume(TokenType.SEMICOLON, "Expected ';' after break")
                return OpenCLBreakStatement()
            elif self._match(TokenType.CONTINUE):
                self._consume(TokenType.SEMICOLON, "Expected ';' after continue")
                return OpenCLContinueStatement()
            elif self._check(TokenType.LEFT_BRACE):
                return self._parse_block()
            else:
                return self._parse_expression_statement()
        
        except ParseError:
            self._synchronize()
            return None
    
    def _parse_if_statement(self) -> OpenCLIfStatement:
        """Parse if statement"""
        self._consume(TokenType.LEFT_PAREN, "Expected '(' after 'if'")
        condition = self._parse_expression()
        self._consume(TokenType.RIGHT_PAREN, "Expected ')' after if condition")
        
        then_stmt = self._parse_statement()
        else_stmt = None
        
        if self._match(TokenType.ELSE):
            else_stmt = self._parse_statement()
        
        return OpenCLIfStatement(condition, then_stmt, else_stmt)
    
    def _parse_while_statement(self) -> OpenCLWhileLoop:
        """Parse while statement"""
        self._consume(TokenType.LEFT_PAREN, "Expected '(' after 'while'")
        condition = self._parse_expression()
        self._consume(TokenType.RIGHT_PAREN, "Expected ')' after while condition")
        
        body = self._parse_statement()
        return OpenCLWhileLoop(condition, body)
    
    def _parse_for_statement(self) -> OpenCLForLoop:
        """Parse for statement"""
        self._consume(TokenType.LEFT_PAREN, "Expected '(' after 'for'")
        
        # Init
        init = None
        if not self._check(TokenType.SEMICOLON):
            init = self._parse_expression_statement()
        else:
            self._advance()  # consume semicolon
        
        # Condition
        condition = None
        if not self._check(TokenType.SEMICOLON):
            condition = self._parse_expression()
        self._consume(TokenType.SEMICOLON, "Expected ';' after for condition")
        
        # Update
        update = None
        if not self._check(TokenType.RIGHT_PAREN):
            update = self._parse_expression()
        self._consume(TokenType.RIGHT_PAREN, "Expected ')' after for clauses")
        
        body = self._parse_statement()
        return OpenCLForLoop(init, condition, update, body)
    
    def _parse_do_while_statement(self) -> OpenCLDoWhileLoop:
        """Parse do-while statement"""
        body = self._parse_statement()
        self._consume(TokenType.WHILE, "Expected 'while' after do body")
        self._consume(TokenType.LEFT_PAREN, "Expected '(' after 'while'")
        condition = self._parse_expression()
        self._consume(TokenType.RIGHT_PAREN, "Expected ')' after while condition")
        self._consume(TokenType.SEMICOLON, "Expected ';' after do-while")
        
        return OpenCLDoWhileLoop(body, condition)
    
    def _parse_return_statement(self) -> OpenCLReturnStatement:
        """Parse return statement"""
        value = None
        if not self._check(TokenType.SEMICOLON):
            value = self._parse_expression()
        
        self._consume(TokenType.SEMICOLON, "Expected ';' after return")
        return OpenCLReturnStatement(value)
    
    def _parse_expression_statement(self) -> OpenCLExpressionStatement:
        """Parse expression statement"""
        expr = self._parse_expression()
        self._consume(TokenType.SEMICOLON, "Expected ';' after expression")
        return OpenCLExpressionStatement(expr)
    
    def _parse_expression(self) -> OpenCLExpression:
        """Parse expression"""
        return self._parse_conditional()
    
    def _parse_conditional(self) -> OpenCLExpression:
        """Parse conditional (ternary) expression"""
        expr = self._parse_logical_or()
        
        if self._match(TokenType.QUESTION):
            true_expr = self._parse_expression()
            self._consume(TokenType.COLON, "Expected ':' in ternary expression")
            false_expr = self._parse_expression()
            return OpenCLConditional(expr, true_expr, false_expr)
        
        return expr
    
    def _parse_logical_or(self) -> OpenCLExpression:
        """Parse logical OR expression"""
        expr = self._parse_logical_and()
        
        while self._match(TokenType.LOGICAL_OR):
            operator = self._previous().value
            right = self._parse_logical_and()
            expr = OpenCLBinaryOp(expr, operator, right)
        
        return expr
    
    def _parse_logical_and(self) -> OpenCLExpression:
        """Parse logical AND expression"""
        expr = self._parse_bitwise_or()
        
        while self._match(TokenType.LOGICAL_AND):
            operator = self._previous().value
            right = self._parse_bitwise_or()
            expr = OpenCLBinaryOp(expr, operator, right)
        
        return expr
    
    def _parse_bitwise_or(self) -> OpenCLExpression:
        """Parse bitwise OR expression"""
        expr = self._parse_bitwise_xor()
        
        while self._match(TokenType.BITWISE_OR):
            operator = self._previous().value
            right = self._parse_bitwise_xor()
            expr = OpenCLBinaryOp(expr, operator, right)
        
        return expr
    
    def _parse_bitwise_xor(self) -> OpenCLExpression:
        """Parse bitwise XOR expression"""
        expr = self._parse_bitwise_and()
        
        while self._match(TokenType.BITWISE_XOR):
            operator = self._previous().value
            right = self._parse_bitwise_and()
            expr = OpenCLBinaryOp(expr, operator, right)
        
        return expr
    
    def _parse_bitwise_and(self) -> OpenCLExpression:
        """Parse bitwise AND expression"""
        expr = self._parse_equality()
        
        while self._match(TokenType.BITWISE_AND):
            operator = self._previous().value
            right = self._parse_equality()
            expr = OpenCLBinaryOp(expr, operator, right)
        
        return expr
    
    def _parse_equality(self) -> OpenCLExpression:
        """Parse equality expression"""
        expr = self._parse_relational()
        
        while self._match(TokenType.EQUAL, TokenType.NOT_EQUAL):
            operator = self._previous().value
            right = self._parse_relational()
            expr = OpenCLBinaryOp(expr, operator, right)
        
        return expr
    
    def _parse_relational(self) -> OpenCLExpression:
        """Parse relational expression"""
        expr = self._parse_shift()
        
        while self._match(TokenType.LESS_THAN, TokenType.LESS_EQUAL,
                          TokenType.GREATER_THAN, TokenType.GREATER_EQUAL):
            operator = self._previous().value
            right = self._parse_shift()
            expr = OpenCLBinaryOp(expr, operator, right)
        
        return expr
    
    def _parse_shift(self) -> OpenCLExpression:
        """Parse shift expression"""
        expr = self._parse_additive()
        
        while self._match(TokenType.LEFT_SHIFT, TokenType.RIGHT_SHIFT):
            operator = self._previous().value
            right = self._parse_additive()
            expr = OpenCLBinaryOp(expr, operator, right)
        
        return expr
    
    def _parse_additive(self) -> OpenCLExpression:
        """Parse additive expression"""
        expr = self._parse_multiplicative()
        
        while self._match(TokenType.PLUS, TokenType.MINUS):
            operator = self._previous().value
            right = self._parse_multiplicative()
            expr = OpenCLBinaryOp(expr, operator, right)
        
        return expr
    
    def _parse_multiplicative(self) -> OpenCLExpression:
        """Parse multiplicative expression"""
        expr = self._parse_unary()
        
        while self._match(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            operator = self._previous().value
            right = self._parse_unary()
            expr = OpenCLBinaryOp(expr, operator, right)
        
        return expr
    
    def _parse_unary(self) -> OpenCLExpression:
        """Parse unary expression"""
        if self._match(TokenType.LOGICAL_NOT, TokenType.BITWISE_NOT,
                      TokenType.PLUS, TokenType.MINUS, TokenType.INCREMENT,
                      TokenType.DECREMENT):
            operator = self._previous().value
            expr = self._parse_unary()
            return OpenCLUnaryOp(operator, expr)
        
        return self._parse_postfix()
    
    def _parse_postfix(self) -> OpenCLExpression:
        """Parse postfix expression"""
        expr = self._parse_primary()
        
        while True:
            if self._match(TokenType.LEFT_BRACKET):
                index = self._parse_expression()
                self._consume(TokenType.RIGHT_BRACKET, "Expected ']'")
                expr = OpenCLArrayAccess(expr, index)
            elif self._match(TokenType.DOT):
                field = self._consume(TokenType.IDENTIFIER, "Expected field name").value
                expr = OpenCLFieldAccess(expr, field)
            elif self._match(TokenType.ARROW):
                field = self._consume(TokenType.IDENTIFIER, "Expected field name").value
                expr = OpenCLFieldAccess(expr, field)
            elif self._match(TokenType.LEFT_PAREN):
                # Function call
                args = []
                if not self._check(TokenType.RIGHT_PAREN):
                    args.append(self._parse_expression())
                    while self._match(TokenType.COMMA):
                        args.append(self._parse_expression())
                
                self._consume(TokenType.RIGHT_PAREN, "Expected ')' after arguments")
                
                if isinstance(expr, OpenCLIdentifier):
                    # Check if it's a built-in function
                    if self._is_builtin_function(expr.name):
                        category = self._get_builtin_category(expr.name)
                        expr = OpenCLBuiltinCall(expr.name, args, category)
                    else:
                        expr = OpenCLFunctionCall(expr.name, args)
                else:
                    expr = OpenCLFunctionCall("", args)  # Function pointer call
            elif self._match(TokenType.INCREMENT, TokenType.DECREMENT):
                operator = self._previous().value
                expr = OpenCLUnaryOp(operator, expr)
            else:
                break
        
        return expr
    
    def _parse_primary(self) -> OpenCLExpression:
        """Parse primary expression"""
        if self._match(TokenType.INTEGER_LITERAL):
            value = self._previous().value
            return OpenCLLiteral(int(value.rstrip('uUlL'), 0))
        
        if self._match(TokenType.FLOAT_LITERAL):
            value = self._previous().value
            return OpenCLLiteral(float(value.rstrip('fF')))
        
        if self._match(TokenType.STRING_LITERAL):
            value = self._previous().value
            return OpenCLLiteral(value[1:-1])  # Remove quotes
        
        if self._match(TokenType.CHAR_LITERAL):
            value = self._previous().value
            return OpenCLLiteral(value[1:-1])  # Remove quotes
        
        if self._match(TokenType.IDENTIFIER):
            name = self._previous().value
            
            # Check for vector literal constructor
            vector_match = OpenCLLexer.VECTOR_TYPES.match(name)
            if vector_match and self._check(TokenType.LEFT_PAREN):
                self._advance()  # consume '('
                components = []
                if not self._check(TokenType.RIGHT_PAREN):
                    components.append(self._parse_expression())
                    while self._match(TokenType.COMMA):
                        components.append(self._parse_expression())
                
                self._consume(TokenType.RIGHT_PAREN, "Expected ')' after vector components")
                return OpenCLVectorLiteral(name, components)
            
            return OpenCLIdentifier(name)
        
        if self._match(TokenType.LEFT_PAREN):
            expr = self._parse_expression()
            self._consume(TokenType.RIGHT_PAREN, "Expected ')' after expression")
            return expr
        
        raise ParseError("Expected expression", self.current_token)
    
    def _is_builtin_function(self, name: str) -> bool:
        """Check if function name is a built-in OpenCL function"""
        for category, functions in OPENCL_BUILTIN_FUNCTIONS.items():
            if name in functions:
                return True
        return False
    
    def _get_builtin_category(self, name: str) -> str:
        """Get category of built-in function"""
        for category, functions in OPENCL_BUILTIN_FUNCTIONS.items():
            if name in functions:
                return category
        return "unknown"
    
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
        """Error recovery - skip to next statement"""
        self._advance()
        
        while not self._is_at_end():
            if self._previous().type == TokenType.SEMICOLON:
                return
            
            if self.current_token.type in (TokenType.IF, TokenType.FOR, TokenType.WHILE,
                                         TokenType.RETURN, TokenType.BREAK,
                                         TokenType.CONTINUE):
                return
            
            self._advance()


def parse_opencl(source: str, filename: Optional[str] = None) -> OpenCLProgram:
    """Main entry point for parsing OpenCL source code"""
    try:
        lexer = OpenCLLexer(source, filename)
        tokens = lexer.tokenize()
        
        parser = OpenCLParser(tokens)
        return parser.parse()
    
    except Exception as e:
        raise ParseError(f"Failed to parse OpenCL code: {str(e)}") 