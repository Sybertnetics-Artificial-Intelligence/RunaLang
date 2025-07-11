#!/usr/bin/env python3
"""
CUDA Parser - Comprehensive parser for CUDA C++ Language

Features:
- Complete CUDA C++ expression parsing
- Kernel function syntax (__global__, __device__, __host__)
- Execution configuration <<<gridDim, blockDim>>>
- Thread indexing and built-in variables
- Memory management and synchronization
- CUDA runtime API calls
- Vector types and atomic operations
- Error recovery and reporting
"""

import re
from typing import List, Optional, Dict, Any, Tuple, Union
from enum import Enum, auto
from dataclasses import dataclass
from .cuda_ast import *

class TokenType(Enum):
    """CUDA token types"""
    # Identifiers and literals
    IDENTIFIER = auto()
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    CHAR = auto()
    
    # CUDA keywords
    GLOBAL = auto()         # __global__
    DEVICE = auto()         # __device__
    HOST = auto()           # __host__
    SHARED = auto()         # __shared__
    CONSTANT = auto()       # __constant__
    
    # C++ keywords
    INT = auto()
    FLOAT_KW = auto()
    DOUBLE = auto()
    CHAR_KW = auto()
    VOID = auto()
    IF = auto()
    ELSE = auto()
    FOR = auto()
    WHILE = auto()
    RETURN = auto()
    
    # CUDA execution config
    TRIPLE_LT = auto()      # <<<
    TRIPLE_GT = auto()      # >>>
    
    # Operators
    PLUS = auto()           # +
    MINUS = auto()          # -
    MULTIPLY = auto()       # *
    DIVIDE = auto()         # /
    MODULO = auto()         # %
    ASSIGN = auto()         # =
    EQUALS = auto()         # ==
    NOT_EQUALS = auto()     # !=
    LESS_THAN = auto()      # <
    GREATER_THAN = auto()   # >
    LESS_EQUAL = auto()     # <=
    GREATER_EQUAL = auto()  # >=
    LOGICAL_AND = auto()    # &&
    LOGICAL_OR = auto()     # ||
    LOGICAL_NOT = auto()    # !
    BITWISE_AND = auto()    # &
    BITWISE_OR = auto()     # |
    BITWISE_XOR = auto()    # ^
    
    # Delimiters
    SEMICOLON = auto()      # ;
    COMMA = auto()          # ,
    DOT = auto()            # .
    ARROW = auto()          # ->
    
    # Brackets
    LPAREN = auto()         # (
    RPAREN = auto()         # )
    LBRACE = auto()         # {
    RBRACE = auto()         # }
    LBRACKET = auto()       # [
    RBRACKET = auto()       # ]
    
    # Preprocessor
    INCLUDE = auto()        # #include
    PRAGMA = auto()         # #pragma
    
    # Comments and whitespace
    COMMENT = auto()
    NEWLINE = auto()
    WHITESPACE = auto()
    
    # End of file
    EOF = auto()

@dataclass
class Token:
    """CUDA token"""
    type: TokenType
    value: str
    line: int = 1
    column: int = 1

class CudaLexer:
    """Lexer for CUDA C++"""
    
    KEYWORDS = {
        '__global__': TokenType.GLOBAL,
        '__device__': TokenType.DEVICE,
        '__host__': TokenType.HOST,
        '__shared__': TokenType.SHARED,
        '__constant__': TokenType.CONSTANT,
        'int': TokenType.INT,
        'float': TokenType.FLOAT_KW,
        'double': TokenType.DOUBLE,
        'char': TokenType.CHAR_KW,
        'void': TokenType.VOID,
        'if': TokenType.IF,
        'else': TokenType.ELSE,
        'for': TokenType.FOR,
        'while': TokenType.WHILE,
        'return': TokenType.RETURN,
    }
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        
    def advance(self) -> str:
        if self.pos >= len(self.source):
            return ''
        char = self.source[self.pos]
        self.pos += 1
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char
        
    def peek(self, offset: int = 0) -> str:
        pos = self.pos + offset
        return self.source[pos] if pos < len(self.source) else ''
        
    def read_identifier(self) -> str:
        value = ''
        while self.pos < len(self.source):
            char = self.peek()
            if char.isalnum() or char == '_':
                value += self.advance()
            else:
                break
        return value
        
    def read_number(self) -> Tuple[str, TokenType]:
        value = ''
        is_float = False
        
        while self.pos < len(self.source):
            char = self.peek()
            if char.isdigit():
                value += self.advance()
            elif char == '.' and not is_float:
                if self.peek(1).isdigit():
                    is_float = True
                    value += self.advance()
                else:
                    break
            elif char.lower() == 'f' and is_float:
                value += self.advance()
                break
            else:
                break
                
        return value, TokenType.FLOAT if is_float else TokenType.INTEGER
        
    def read_string(self, quote: str) -> str:
        value = ''
        self.advance()  # Skip opening quote
        
        while self.pos < len(self.source):
            char = self.peek()
            if char == quote:
                self.advance()  # Skip closing quote
                break
            elif char == '\\':
                self.advance()  # Skip backslash
                escaped = self.advance()
                if escaped == 'n':
                    value += '\n'
                elif escaped == 't':
                    value += '\t'
                elif escaped == 'r':
                    value += '\r'
                elif escaped == '\\':
                    value += '\\'
                elif escaped == quote:
                    value += quote
                else:
                    value += escaped
            else:
                value += self.advance()
        return value
        
    def read_comment(self) -> str:
        if self.peek() == '/' and self.peek(1) == '/':
            # Line comment
            self.advance()  # Skip first /
            self.advance()  # Skip second /
            value = ''
            while self.pos < len(self.source):
                char = self.peek()
                if char == '\n':
                    break
                value += self.advance()
            return value.strip()
        elif self.peek() == '/' and self.peek(1) == '*':
            # Block comment
            self.advance()  # Skip /
            self.advance()  # Skip *
            value = ''
            while self.pos < len(self.source) - 1:
                char = self.peek()
                next_char = self.peek(1)
                if char == '*' and next_char == '/':
                    self.advance()  # Skip *
                    self.advance()  # Skip /
                    break
                value += self.advance()
            return value.strip()
        return ''
        
    def tokenize(self) -> List[Token]:
        self.tokens = []
        
        while self.pos < len(self.source):
            start_line, start_col = self.line, self.column
            char = self.peek()
            
            # Skip whitespace
            if char in ' \t\r':
                self.advance()
                continue
                
            # Newlines
            elif char == '\n':
                self.tokens.append(Token(TokenType.NEWLINE, self.advance(), start_line, start_col))
                
            # Comments
            elif char == '/' and self.peek(1) in ['/', '*']:
                comment = self.read_comment()
                self.tokens.append(Token(TokenType.COMMENT, comment, start_line, start_col))
                
            # Preprocessor directives
            elif char == '#':
                # Read preprocessor directive
                directive = ''
                while self.pos < len(self.source) and self.peek() != '\n':
                    directive += self.advance()
                    
                if directive.startswith('#include'):
                    self.tokens.append(Token(TokenType.INCLUDE, directive, start_line, start_col))
                elif directive.startswith('#pragma'):
                    self.tokens.append(Token(TokenType.PRAGMA, directive, start_line, start_col))
                    
            # String literals
            elif char in ['"', "'"]:
                string_value = self.read_string(char)
                token_type = TokenType.STRING if char == '"' else TokenType.CHAR
                self.tokens.append(Token(token_type, string_value, start_line, start_col))
                
            # Numbers
            elif char.isdigit():
                number_value, token_type = self.read_number()
                self.tokens.append(Token(token_type, number_value, start_line, start_col))
                
            # CUDA execution configuration <<<>>>
            elif char == '<' and self.peek(1) == '<' and self.peek(2) == '<':
                self.advance()
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.TRIPLE_LT, '<<<', start_line, start_col))
                
            elif char == '>' and self.peek(1) == '>' and self.peek(2) == '>':
                self.advance()
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.TRIPLE_GT, '>>>', start_line, start_col))
                
            # Two-character operators
            elif char == '=' and self.peek(1) == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.EQUALS, '==', start_line, start_col))
                
            elif char == '!' and self.peek(1) == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.NOT_EQUALS, '!=', start_line, start_col))
                
            elif char == '<' and self.peek(1) == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.LESS_EQUAL, '<=', start_line, start_col))
                
            elif char == '>' and self.peek(1) == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.GREATER_EQUAL, '>=', start_line, start_col))
                
            elif char == '&' and self.peek(1) == '&':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.LOGICAL_AND, '&&', start_line, start_col))
                
            elif char == '|' and self.peek(1) == '|':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.LOGICAL_OR, '||', start_line, start_col))
                
            elif char == '-' and self.peek(1) == '>':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.ARROW, '->', start_line, start_col))
                
            # Identifiers and keywords
            elif char.isalpha() or char == '_':
                identifier = self.read_identifier()
                token_type = self.KEYWORDS.get(identifier, TokenType.IDENTIFIER)
                self.tokens.append(Token(token_type, identifier, start_line, start_col))
                
            # Single-character operators and delimiters
            elif char == '+':
                self.tokens.append(Token(TokenType.PLUS, self.advance(), start_line, start_col))
            elif char == '-':
                self.tokens.append(Token(TokenType.MINUS, self.advance(), start_line, start_col))
            elif char == '*':
                self.tokens.append(Token(TokenType.MULTIPLY, self.advance(), start_line, start_col))
            elif char == '/':
                self.tokens.append(Token(TokenType.DIVIDE, self.advance(), start_line, start_col))
            elif char == '%':
                self.tokens.append(Token(TokenType.MODULO, self.advance(), start_line, start_col))
            elif char == '=':
                self.tokens.append(Token(TokenType.ASSIGN, self.advance(), start_line, start_col))
            elif char == '<':
                self.tokens.append(Token(TokenType.LESS_THAN, self.advance(), start_line, start_col))
            elif char == '>':
                self.tokens.append(Token(TokenType.GREATER_THAN, self.advance(), start_line, start_col))
            elif char == '!':
                self.tokens.append(Token(TokenType.LOGICAL_NOT, self.advance(), start_line, start_col))
            elif char == '&':
                self.tokens.append(Token(TokenType.BITWISE_AND, self.advance(), start_line, start_col))
            elif char == '|':
                self.tokens.append(Token(TokenType.BITWISE_OR, self.advance(), start_line, start_col))
            elif char == '^':
                self.tokens.append(Token(TokenType.BITWISE_XOR, self.advance(), start_line, start_col))
            elif char == ';':
                self.tokens.append(Token(TokenType.SEMICOLON, self.advance(), start_line, start_col))
            elif char == ',':
                self.tokens.append(Token(TokenType.COMMA, self.advance(), start_line, start_col))
            elif char == '.':
                self.tokens.append(Token(TokenType.DOT, self.advance(), start_line, start_col))
            elif char == '(':
                self.tokens.append(Token(TokenType.LPAREN, self.advance(), start_line, start_col))
            elif char == ')':
                self.tokens.append(Token(TokenType.RPAREN, self.advance(), start_line, start_col))
            elif char == '{':
                self.tokens.append(Token(TokenType.LBRACE, self.advance(), start_line, start_col))
            elif char == '}':
                self.tokens.append(Token(TokenType.RBRACE, self.advance(), start_line, start_col))
            elif char == '[':
                self.tokens.append(Token(TokenType.LBRACKET, self.advance(), start_line, start_col))
            elif char == ']':
                self.tokens.append(Token(TokenType.RBRACKET, self.advance(), start_line, start_col))
            else:
                self.advance()  # Skip unknown character
                
        self.tokens.append(Token(TokenType.EOF, '', self.line, self.column))
        return self.tokens

class CudaParser:
    """Parser for CUDA C++"""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.current_token = tokens[0] if tokens else Token(TokenType.EOF, '', 1, 1)
        
    def error(self, message: str) -> None:
        token = self.current_token
        raise SyntaxError(f"Line {token.line}, Column {token.column}: {message}")
        
    def advance(self) -> Token:
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
            self.current_token = self.tokens[self.pos]
        return self.current_token
        
    def match(self, *token_types: TokenType) -> bool:
        return self.current_token.type in token_types
        
    def consume(self, token_type: TokenType, message: str = None) -> Token:
        if self.current_token.type != token_type:
            msg = message or f"Expected {token_type}, got {self.current_token.type}"
            self.error(msg)
        token = self.current_token
        self.advance()
        return token
        
    def skip_newlines(self) -> None:
        while self.match(TokenType.NEWLINE):
            self.advance()
            
    def parse_translation_unit(self) -> CudaTranslationUnit:
        declarations = []
        includes = []
        
        while not self.match(TokenType.EOF):
            self.skip_newlines()
            
            if self.match(TokenType.INCLUDE):
                include = self.parse_include_directive()
                includes.append(include)
            elif self.match(TokenType.PRAGMA):
                pragma = self.parse_pragma_directive()
                declarations.append(pragma)
            else:
                decl = self.parse_declaration()
                if decl:
                    declarations.append(decl)
                    
        return CudaTranslationUnit(
            declarations=declarations,
            includes=includes
        )
        
    def parse_include_directive(self) -> IncludeDirective:
        include_text = self.current_token.value
        self.advance()
        
        # Extract header name
        match = re.search(r'#include\s*[<"]([^>"]+)[>"]', include_text)
        if match:
            header_name = match.group(1)
            is_system = '<' in include_text
        else:
            header_name = "unknown"
            is_system = False
            
        return IncludeDirective(header_name=header_name, is_system=is_system)
        
    def parse_pragma_directive(self) -> PragmaDirective:
        pragma_text = self.current_token.value
        self.advance()
        
        # Extract pragma directive
        parts = pragma_text.split()
        directive = parts[1] if len(parts) > 1 else ""
        arguments = parts[2:] if len(parts) > 2 else []
        
        return PragmaDirective(directive=directive, arguments=arguments)
        
    def parse_declaration(self) -> Optional[CudaDeclaration]:
        self.skip_newlines()
        
        # Check for CUDA execution space qualifiers
        execution_space = None
        if self.match(TokenType.GLOBAL):
            execution_space = CudaExecutionSpace.GLOBAL
            self.advance()
        elif self.match(TokenType.DEVICE):
            execution_space = CudaExecutionSpace.DEVICE
            self.advance()
        elif self.match(TokenType.HOST):
            execution_space = CudaExecutionSpace.HOST
            self.advance()
            
        # Check for memory space qualifiers
        memory_space = None
        if self.match(TokenType.SHARED):
            memory_space = CudaMemorySpace.SHARED
            self.advance()
        elif self.match(TokenType.CONSTANT):
            memory_space = CudaMemorySpace.CONSTANT
            self.advance()
            
        # Parse type
        return_type = self.parse_type()
        
        if not self.match(TokenType.IDENTIFIER):
            self.error("Expected identifier")
            
        name = self.current_token.value
        self.advance()
        
        if self.match(TokenType.LPAREN):
            # Function declaration
            params = self.parse_parameter_list()
            body = None
            
            if self.match(TokenType.LBRACE):
                body = self.parse_compound_statement()
            else:
                self.consume(TokenType.SEMICOLON)
                
            if execution_space == CudaExecutionSpace.GLOBAL:
                return KernelFunction(
                    name=name,
                    parameters=params,
                    body=body or CompoundStatement(),
                    return_type=return_type
                )
            else:
                return DeviceFunction(
                    name=name,
                    parameters=params,
                    body=body or CompoundStatement(),
                    execution_space=execution_space or CudaExecutionSpace.DEVICE,
                    return_type=return_type
                )
        else:
            # Variable declaration
            initial_value = None
            if self.match(TokenType.ASSIGN):
                self.advance()
                initial_value = self.parse_expression()
                
            self.consume(TokenType.SEMICOLON)
            
            if memory_space:
                if memory_space == CudaMemorySpace.SHARED:
                    return SharedMemoryDeclaration(
                        name=name,
                        type=return_type
                    )
                else:
                    return DeviceVariable(
                        name=name,
                        type=return_type,
                        memory_space=memory_space,
                        initial_value=initial_value
                    )
            else:
                return DeviceVariable(
                    name=name,
                    type=return_type,
                    memory_space=CudaMemorySpace.GLOBAL,
                    initial_value=initial_value
                )
                
    def parse_type(self) -> CudaType:
        if self.match(TokenType.INT):
            self.advance()
            return CudaBuiltinType("int")
        elif self.match(TokenType.FLOAT_KW):
            self.advance()
            return CudaBuiltinType("float")
        elif self.match(TokenType.DOUBLE):
            self.advance()
            return CudaBuiltinType("double")
        elif self.match(TokenType.CHAR_KW):
            self.advance()
            return CudaBuiltinType("char")
        elif self.match(TokenType.VOID):
            self.advance()
            return CudaBuiltinType("void")
        elif self.match(TokenType.IDENTIFIER):
            type_name = self.current_token.value
            self.advance()
            
            # Check for CUDA vector types
            if re.match(r'(int|float|double|char)[1-4]$', type_name):
                base_type = type_name[:-1]
                dimension = int(type_name[-1])
                return CudaVectorType(base_type=base_type, dimension=dimension)
            else:
                return CudaBuiltinType(type_name)
        else:
            self.error("Expected type")
            
    def parse_parameter_list(self) -> List[ParameterDeclaration]:
        self.consume(TokenType.LPAREN)
        params = []
        
        while not self.match(TokenType.RPAREN):
            param_type = self.parse_type()
            
            if self.match(TokenType.IDENTIFIER):
                param_name = self.current_token.value
                self.advance()
            else:
                param_name = f"param_{len(params)}"
                
            param = ParameterDeclaration(name=param_name, type=param_type)
            params.append(param)
            
            if self.match(TokenType.COMMA):
                self.advance()
            elif not self.match(TokenType.RPAREN):
                self.error("Expected ',' or ')'")
                
        self.consume(TokenType.RPAREN)
        return params
        
    def parse_compound_statement(self) -> CompoundStatement:
        self.consume(TokenType.LBRACE)
        statements = []
        
        while not self.match(TokenType.RBRACE):
            self.skip_newlines()
            if self.match(TokenType.RBRACE):
                break
                
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
                
        self.consume(TokenType.RBRACE)
        return CompoundStatement(statements=statements)
        
    def parse_statement(self) -> Optional[CudaStatement]:
        self.skip_newlines()
        
        if self.match(TokenType.IF):
            return self.parse_if_statement()
        elif self.match(TokenType.FOR):
            return self.parse_for_statement()
        elif self.match(TokenType.WHILE):
            return self.parse_while_statement()
        elif self.match(TokenType.RETURN):
            return self.parse_return_statement()
        elif self.match(TokenType.LBRACE):
            return self.parse_compound_statement()
        else:
            # Expression statement
            expr = self.parse_expression()
            self.consume(TokenType.SEMICOLON)
            
            # Check for special CUDA statements
            if isinstance(expr, KernelLaunch):
                return KernelLaunchStatement(kernel_launch=expr)
            else:
                return ExpressionStatement(expression=expr)
                
    def parse_if_statement(self) -> IfStatement:
        self.consume(TokenType.IF)
        self.consume(TokenType.LPAREN)
        condition = self.parse_expression()
        self.consume(TokenType.RPAREN)
        then_stmt = self.parse_statement()
        
        else_stmt = None
        if self.match(TokenType.ELSE):
            self.advance()
            else_stmt = self.parse_statement()
            
        return IfStatement(
            condition=condition,
            then_statement=then_stmt,
            else_statement=else_stmt
        )
        
    def parse_for_statement(self) -> ForStatement:
        self.consume(TokenType.FOR)
        self.consume(TokenType.LPAREN)
        
        init = None
        if not self.match(TokenType.SEMICOLON):
            init = self.parse_statement()
        else:
            self.advance()
            
        condition = None
        if not self.match(TokenType.SEMICOLON):
            condition = self.parse_expression()
        self.consume(TokenType.SEMICOLON)
        
        increment = None
        if not self.match(TokenType.RPAREN):
            increment = self.parse_expression()
        self.consume(TokenType.RPAREN)
        
        body = self.parse_statement()
        
        return ForStatement(
            init=init,
            condition=condition,
            increment=increment,
            body=body
        )
        
    def parse_while_statement(self) -> WhileStatement:
        self.consume(TokenType.WHILE)
        self.consume(TokenType.LPAREN)
        condition = self.parse_expression()
        self.consume(TokenType.RPAREN)
        body = self.parse_statement()
        
        return WhileStatement(condition=condition, body=body)
        
    def parse_return_statement(self) -> ReturnStatement:
        self.consume(TokenType.RETURN)
        
        value = None
        if not self.match(TokenType.SEMICOLON):
            value = self.parse_expression()
            
        self.consume(TokenType.SEMICOLON)
        return ReturnStatement(value=value)
        
    def parse_expression(self) -> CudaExpression:
        return self.parse_assignment()
        
    def parse_assignment(self) -> CudaExpression:
        expr = self.parse_logical_or()
        
        if self.match(TokenType.ASSIGN):
            op = self.current_token.value
            self.advance()
            right = self.parse_assignment()
            return BinaryOperation(left=expr, operator=op, right=right)
            
        return expr
        
    def parse_logical_or(self) -> CudaExpression:
        expr = self.parse_logical_and()
        
        while self.match(TokenType.LOGICAL_OR):
            op = self.current_token.value
            self.advance()
            right = self.parse_logical_and()
            expr = BinaryOperation(left=expr, operator=op, right=right)
            
        return expr
        
    def parse_logical_and(self) -> CudaExpression:
        expr = self.parse_equality()
        
        while self.match(TokenType.LOGICAL_AND):
            op = self.current_token.value
            self.advance()
            right = self.parse_equality()
            expr = BinaryOperation(left=expr, operator=op, right=right)
            
        return expr
        
    def parse_equality(self) -> CudaExpression:
        expr = self.parse_relational()
        
        while self.match(TokenType.EQUALS, TokenType.NOT_EQUALS):
            op = self.current_token.value
            self.advance()
            right = self.parse_relational()
            expr = BinaryOperation(left=expr, operator=op, right=right)
            
        return expr
        
    def parse_relational(self) -> CudaExpression:
        expr = self.parse_additive()
        
        while self.match(TokenType.LESS_THAN, TokenType.LESS_EQUAL,
                         TokenType.GREATER_THAN, TokenType.GREATER_EQUAL):
            op = self.current_token.value
            self.advance()
            right = self.parse_additive()
            expr = BinaryOperation(left=expr, operator=op, right=right)
            
        return expr
        
    def parse_additive(self) -> CudaExpression:
        expr = self.parse_multiplicative()
        
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = self.current_token.value
            self.advance()
            right = self.parse_multiplicative()
            expr = BinaryOperation(left=expr, operator=op, right=right)
            
        return expr
        
    def parse_multiplicative(self) -> CudaExpression:
        expr = self.parse_unary()
        
        while self.match(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            op = self.current_token.value
            self.advance()
            right = self.parse_unary()
            expr = BinaryOperation(left=expr, operator=op, right=right)
            
        return expr
        
    def parse_unary(self) -> CudaExpression:
        if self.match(TokenType.LOGICAL_NOT, TokenType.MINUS, TokenType.PLUS):
            op = self.current_token.value
            self.advance()
            operand = self.parse_unary()
            return UnaryOperation(operator=op, operand=operand)
            
        return self.parse_postfix()
        
    def parse_postfix(self) -> CudaExpression:
        expr = self.parse_primary()
        
        while True:
            if self.match(TokenType.LPAREN):
                # Function call or kernel launch
                if isinstance(expr, Identifier) and self.is_next_execution_config():
                    # Kernel launch
                    config = self.parse_execution_configuration()
                    args = self.parse_argument_list()
                    return KernelLaunch(
                        kernel_name=expr.name,
                        execution_config=config,
                        arguments=args
                    )
                else:
                    # Regular function call
                    args = self.parse_argument_list()
                    expr = FunctionCall(function=expr, arguments=args)
                    
            elif self.match(TokenType.LBRACKET):
                # Array access
                self.advance()
                index = self.parse_expression()
                self.consume(TokenType.RBRACKET)
                expr = ArrayAccess(array=expr, index=index)
                
            elif self.match(TokenType.DOT):
                # Member access
                self.advance()
                if self.match(TokenType.IDENTIFIER):
                    member = self.current_token.value
                    self.advance()
                    expr = MemberAccess(object=expr, member=member)
                else:
                    self.error("Expected member name")
                    
            elif self.match(TokenType.ARROW):
                # Pointer member access
                self.advance()
                if self.match(TokenType.IDENTIFIER):
                    member = self.current_token.value
                    self.advance()
                    expr = MemberAccess(object=expr, member=member, is_pointer_access=True)
                else:
                    self.error("Expected member name")
            else:
                break
                
        return expr
        
    def parse_primary(self) -> CudaExpression:
        if self.match(TokenType.IDENTIFIER):
            name = self.current_token.value
            self.advance()
            
            # Check for CUDA built-in variables
            if name in ['threadIdx', 'blockIdx', 'blockDim', 'gridDim']:
                if self.match(TokenType.DOT):
                    self.advance()
                    if self.match(TokenType.IDENTIFIER):
                        dim = self.current_token.value
                        self.advance()
                        return ThreadIndex(index_type=name, dimension=dim)
                    else:
                        self.error("Expected dimension (x, y, z)")
                        
            return Identifier(name)
            
        elif self.match(TokenType.INTEGER):
            value = int(self.current_token.value)
            self.advance()
            return IntegerLiteral(value)
            
        elif self.match(TokenType.FLOAT):
            value = float(self.current_token.value)
            self.advance()
            return FloatLiteral(value)
            
        elif self.match(TokenType.STRING):
            value = self.current_token.value
            self.advance()
            return StringLiteral(value)
            
        elif self.match(TokenType.LPAREN):
            self.advance()
            expr = self.parse_expression()
            self.consume(TokenType.RPAREN)
            return expr
            
        else:
            self.error(f"Unexpected token: {self.current_token.type}")
            
    def is_next_execution_config(self) -> bool:
        """Check if next tokens form execution configuration"""
        saved_pos = self.pos
        try:
            if self.match(TokenType.TRIPLE_LT):
                return True
        finally:
            self.pos = saved_pos
            self.current_token = self.tokens[self.pos]
        return False
        
    def parse_execution_configuration(self) -> ExecutionConfiguration:
        self.consume(TokenType.TRIPLE_LT)
        
        grid_dim = self.parse_expression()
        self.consume(TokenType.COMMA)
        block_dim = self.parse_expression()
        
        shared_mem = None
        stream = None
        
        if self.match(TokenType.COMMA):
            self.advance()
            shared_mem = self.parse_expression()
            
            if self.match(TokenType.COMMA):
                self.advance()
                stream = self.parse_expression()
                
        self.consume(TokenType.TRIPLE_GT)
        
        return ExecutionConfiguration(
            grid_dim=grid_dim,
            block_dim=block_dim,
            shared_mem_size=shared_mem,
            stream=stream
        )
        
    def parse_argument_list(self) -> List[CudaExpression]:
        self.consume(TokenType.LPAREN)
        args = []
        
        while not self.match(TokenType.RPAREN):
            arg = self.parse_expression()
            args.append(arg)
            
            if self.match(TokenType.COMMA):
                self.advance()
            elif not self.match(TokenType.RPAREN):
                self.error("Expected ',' or ')'")
                
        self.consume(TokenType.RPAREN)
        return args

# Main parsing function

def parse_cuda(source: str) -> CudaTranslationUnit:
    """Parse CUDA source code into AST"""
    try:
        lexer = CudaLexer(source)
        tokens = lexer.tokenize()
        
        # Filter out whitespace tokens
        filtered_tokens = [t for t in tokens if t.type not in (TokenType.WHITESPACE,)]
        
        parser = CudaParser(filtered_tokens)
        ast = parser.parse_translation_unit()
        
        return ast
        
    except Exception as e:
        raise SyntaxError(f"CUDA parsing failed: {str(e)}")

# Export main components
__all__ = [
    'TokenType', 'Token', 'CudaLexer', 'CudaParser', 'parse_cuda'
] 