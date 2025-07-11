"""
SmartPy Parser

Lexical analysis and parsing for SmartPy - Python-based smart contract language for Tezos.
"""

import re
from typing import List, Optional, Dict, Any, Union, Iterator
from dataclasses import dataclass
from enum import Enum, auto

from runa.ast.base import SourceInfo
from .smartpy_ast import *


class TokenType(Enum):
    """Token types for SmartPy lexical analysis."""
    # Literals
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    BYTES = auto()
    BOOLEAN = auto()
    NONE = auto()
    
    # Identifiers and keywords
    IDENTIFIER = auto()
    
    # Python keywords
    CLASS = auto()
    DEF = auto()
    IF = auto()
    ELIF = auto()
    ELSE = auto()
    FOR = auto()
    WHILE = auto()
    BREAK = auto()
    CONTINUE = auto()
    RETURN = auto()
    PASS = auto()
    IMPORT = auto()
    FROM = auto()
    AS = auto()
    WITH = auto()
    TRY = auto()
    EXCEPT = auto()
    FINALLY = auto()
    RAISE = auto()
    ASSERT = auto()
    LAMBDA = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    IN = auto()
    IS = auto()
    
    # SmartPy specific keywords
    SP_ENTRY_POINT = auto()
    SP_ADD_TEST = auto()
    SP_CONTRACT = auto()
    SP_VERIFY = auto()
    SP_FAILWITH = auto()
    SP_IF = auto()
    SP_ELSE = auto()
    SP_FOR = auto()
    SP_WHILE = auto()
    SP_RESULT = auto()
    SP_TRANSFER = auto()
    SP_SET_DELEGATE = auto()
    SP_CREATE_CONTRACT = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    FLOOR_DIVIDE = auto()
    MODULO = auto()
    POWER = auto()
    
    # Comparison operators
    EQUAL = auto()
    NOT_EQUAL = auto()
    LESS_THAN = auto()
    LESS_EQUAL = auto()
    GREATER_THAN = auto()
    GREATER_EQUAL = auto()
    
    # Assignment operators
    ASSIGN = auto()
    PLUS_ASSIGN = auto()
    MINUS_ASSIGN = auto()
    MULTIPLY_ASSIGN = auto()
    DIVIDE_ASSIGN = auto()
    MODULO_ASSIGN = auto()
    
    # Bitwise operators
    BIT_AND = auto()
    BIT_OR = auto()
    BIT_XOR = auto()
    BIT_NOT = auto()
    LEFT_SHIFT = auto()
    RIGHT_SHIFT = auto()
    
    # Delimiters
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    COLON = auto()
    SEMICOLON = auto()
    DOT = auto()
    ARROW = auto()
    
    # Special tokens
    NEWLINE = auto()
    INDENT = auto()
    DEDENT = auto()
    EOF = auto()
    
    # Comments
    COMMENT = auto()


@dataclass
class Token:
    """Token representation."""
    type: TokenType
    value: str
    source_info: SourceInfo


class SmartPyLexer:
    """Lexical analyzer for SmartPy."""
    
    def __init__(self):
        self.keywords = {
            # Python keywords
            'class': TokenType.CLASS,
            'def': TokenType.DEF,
            'if': TokenType.IF,
            'elif': TokenType.ELIF,
            'else': TokenType.ELSE,
            'for': TokenType.FOR,
            'while': TokenType.WHILE,
            'break': TokenType.BREAK,
            'continue': TokenType.CONTINUE,
            'return': TokenType.RETURN,
            'pass': TokenType.PASS,
            'import': TokenType.IMPORT,
            'from': TokenType.FROM,
            'as': TokenType.AS,
            'with': TokenType.WITH,
            'try': TokenType.TRY,
            'except': TokenType.EXCEPT,
            'finally': TokenType.FINALLY,
            'raise': TokenType.RAISE,
            'assert': TokenType.ASSERT,
            'lambda': TokenType.LAMBDA,
            'and': TokenType.AND,
            'or': TokenType.OR,
            'not': TokenType.NOT,
            'in': TokenType.IN,
            'is': TokenType.IS,
            'True': TokenType.BOOLEAN,
            'False': TokenType.BOOLEAN,
            'None': TokenType.NONE,
        }
        
        self.operators = {
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '*': TokenType.MULTIPLY,
            '/': TokenType.DIVIDE,
            '//': TokenType.FLOOR_DIVIDE,
            '%': TokenType.MODULO,
            '**': TokenType.POWER,
            '=': TokenType.ASSIGN,
            '+=': TokenType.PLUS_ASSIGN,
            '-=': TokenType.MINUS_ASSIGN,
            '*=': TokenType.MULTIPLY_ASSIGN,
            '/=': TokenType.DIVIDE_ASSIGN,
            '%=': TokenType.MODULO_ASSIGN,
            '==': TokenType.EQUAL,
            '!=': TokenType.NOT_EQUAL,
            '<': TokenType.LESS_THAN,
            '<=': TokenType.LESS_EQUAL,
            '>': TokenType.GREATER_THAN,
            '>=': TokenType.GREATER_EQUAL,
            '&': TokenType.BIT_AND,
            '|': TokenType.BIT_OR,
            '^': TokenType.BIT_XOR,
            '~': TokenType.BIT_NOT,
            '<<': TokenType.LEFT_SHIFT,
            '>>': TokenType.RIGHT_SHIFT,
            '->': TokenType.ARROW,
        }
        
        self.delimiters = {
            '(': TokenType.LEFT_PAREN,
            ')': TokenType.RIGHT_PAREN,
            '[': TokenType.LEFT_BRACKET,
            ']': TokenType.RIGHT_BRACKET,
            '{': TokenType.LEFT_BRACE,
            '}': TokenType.RIGHT_BRACE,
            ',': TokenType.COMMA,
            ':': TokenType.COLON,
            ';': TokenType.SEMICOLON,
            '.': TokenType.DOT,
        }
    
    def tokenize(self, source_code: str, filename: str = "unknown") -> List[Token]:
        """Tokenize SmartPy source code."""
        tokens = []
        lines = source_code.split('\n')
        
        indent_stack = [0]  # Stack to track indentation levels
        
        for line_no, line in enumerate(lines, 1):
            tokens.extend(self._tokenize_line(line, line_no, filename, indent_stack))
        
        # Add final dedents
        while len(indent_stack) > 1:
            indent_stack.pop()
            tokens.append(Token(
                TokenType.DEDENT, 
                "", 
                SourceInfo(filename, len(lines), 0)
            ))
        
        # Add EOF token
        tokens.append(Token(
            TokenType.EOF, 
            "", 
            SourceInfo(filename, len(lines), 0)
        ))
        
        return tokens
    
    def _tokenize_line(self, line: str, line_no: int, filename: str, 
                      indent_stack: List[int]) -> List[Token]:
        """Tokenize a single line."""
        tokens = []
        
        # Handle indentation
        if line.strip():  # Non-empty line
            indent_level = len(line) - len(line.lstrip())
            
            if indent_level > indent_stack[-1]:
                # Increased indentation
                indent_stack.append(indent_level)
                tokens.append(Token(
                    TokenType.INDENT,
                    "",
                    SourceInfo(filename, line_no, 0)
                ))
            elif indent_level < indent_stack[-1]:
                # Decreased indentation
                while indent_stack and indent_level < indent_stack[-1]:
                    indent_stack.pop()
                    tokens.append(Token(
                        TokenType.DEDENT,
                        "",
                        SourceInfo(filename, line_no, 0)
                    ))
        
        # Tokenize the line content
        i = 0
        line = line.strip()
        
        while i < len(line):
            # Skip whitespace
            if line[i].isspace():
                i += 1
                continue
            
            # Comments
            if line[i] == '#':
                comment_text = line[i:]
                tokens.append(Token(
                    TokenType.COMMENT,
                    comment_text,
                    SourceInfo(filename, line_no, i)
                ))
                break
            
            # String literals
            if line[i] in '"\'':
                token, new_i = self._parse_string(line, i, line_no, filename)
                tokens.append(token)
                i = new_i
                continue
            
            # Byte literals
            if line[i:i+2] in ['b"', "b'"]:
                token, new_i = self._parse_bytes(line, i, line_no, filename)
                tokens.append(token)
                i = new_i
                continue
            
            # Numbers
            if line[i].isdigit() or (line[i] == '.' and i+1 < len(line) and line[i+1].isdigit()):
                token, new_i = self._parse_number(line, i, line_no, filename)
                tokens.append(token)
                i = new_i
                continue
            
            # Multi-character operators
            two_char = line[i:i+2] if i+1 < len(line) else ""
            if two_char in self.operators:
                tokens.append(Token(
                    self.operators[two_char],
                    two_char,
                    SourceInfo(filename, line_no, i)
                ))
                i += 2
                continue
            
            # Single character operators and delimiters
            if line[i] in self.operators:
                tokens.append(Token(
                    self.operators[line[i]],
                    line[i],
                    SourceInfo(filename, line_no, i)
                ))
                i += 1
                continue
            
            if line[i] in self.delimiters:
                tokens.append(Token(
                    self.delimiters[line[i]],
                    line[i],
                    SourceInfo(filename, line_no, i)
                ))
                i += 1
                continue
            
            # Identifiers and keywords
            if line[i].isalpha() or line[i] == '_':
                token, new_i = self._parse_identifier(line, i, line_no, filename)
                tokens.append(token)
                i = new_i
                continue
            
            # Unknown character
            i += 1
        
        # Add newline token for non-empty lines
        if line.strip():
            tokens.append(Token(
                TokenType.NEWLINE,
                "",
                SourceInfo(filename, line_no, len(line))
            ))
        
        return tokens
    
    def _parse_string(self, line: str, start: int, line_no: int, 
                     filename: str) -> tuple[Token, int]:
        """Parse string literal."""
        quote = line[start]
        i = start + 1
        value = ""
        
        while i < len(line):
            if line[i] == quote:
                break
            elif line[i] == '\\' and i + 1 < len(line):
                # Handle escape sequences
                next_char = line[i + 1]
                if next_char == 'n':
                    value += '\n'
                elif next_char == 't':
                    value += '\t'
                elif next_char == 'r':
                    value += '\r'
                elif next_char == '\\':
                    value += '\\'
                elif next_char == quote:
                    value += quote
                else:
                    value += next_char
                i += 2
            else:
                value += line[i]
                i += 1
        
        return Token(
            TokenType.STRING,
            value,
            SourceInfo(filename, line_no, start)
        ), i + 1
    
    def _parse_bytes(self, line: str, start: int, line_no: int, 
                    filename: str) -> tuple[Token, int]:
        """Parse bytes literal."""
        quote = line[start + 1]  # Skip 'b'
        i = start + 2
        value = ""
        
        while i < len(line):
            if line[i] == quote:
                break
            value += line[i]
            i += 1
        
        return Token(
            TokenType.BYTES,
            value,
            SourceInfo(filename, line_no, start)
        ), i + 1
    
    def _parse_number(self, line: str, start: int, line_no: int, 
                     filename: str) -> tuple[Token, int]:
        """Parse numeric literal."""
        i = start
        value = ""
        is_float = False
        
        while i < len(line) and (line[i].isdigit() or line[i] == '.'):
            if line[i] == '.':
                if is_float:  # Second dot
                    break
                is_float = True
            value += line[i]
            i += 1
        
        token_type = TokenType.FLOAT if is_float else TokenType.INTEGER
        return Token(
            token_type,
            value,
            SourceInfo(filename, line_no, start)
        ), i
    
    def _parse_identifier(self, line: str, start: int, line_no: int, 
                         filename: str) -> tuple[Token, int]:
        """Parse identifier or keyword."""
        i = start
        value = ""
        
        while i < len(line) and (line[i].isalnum() or line[i] == '_'):
            value += line[i]
            i += 1
        
        # Check for SmartPy decorators and special forms
        if value in self.keywords:
            token_type = self.keywords[value]
        else:
            token_type = TokenType.IDENTIFIER
        
        return Token(
            token_type,
            value,
            SourceInfo(filename, line_no, start)
        ), i


class SmartPyParser:
    """Parser for SmartPy language."""
    
    def __init__(self):
        self.tokens = []
        self.current = 0
        self.filename = "unknown"
    
    def parse(self, tokens: List[Token], filename: str = "unknown") -> SmartPyModule:
        """Parse tokens into SmartPy AST."""
        self.tokens = tokens
        self.current = 0
        self.filename = filename
        
        declarations = []
        imports = []
        
        while not self._is_at_end():
            if self._check(TokenType.IMPORT, TokenType.FROM):
                imports.append(self._parse_import())
            else:
                decl = self._parse_declaration()
                if decl:
                    declarations.append(decl)
        
        return SmartPyModule(
            declarations=declarations,
            imports=imports,
            source_info=SourceInfo(filename, 1, 0)
        )
    
    def _parse_import(self) -> SmartPyImport:
        """Parse import statement."""
        if self._match(TokenType.IMPORT):
            module = self._consume(TokenType.IDENTIFIER, "Expected module name").value
            alias = None
            
            if self._match(TokenType.AS):
                alias = self._consume(TokenType.IDENTIFIER, "Expected alias name").value
            
            return SmartPyImport(module=module, alias=alias)
        
        elif self._match(TokenType.FROM):
            module = self._consume(TokenType.IDENTIFIER, "Expected module name").value
            self._consume(TokenType.IMPORT, "Expected 'import'")
            
            names = []
            names.append(self._consume(TokenType.IDENTIFIER, "Expected import name").value)
            
            while self._match(TokenType.COMMA):
                names.append(self._consume(TokenType.IDENTIFIER, "Expected import name").value)
            
            return SmartPyImport(module=module, names=names)
        
        raise ParseError("Expected import statement")
    
    def _parse_declaration(self) -> Optional[SmartPyDeclaration]:
        """Parse top-level declaration."""
        # Skip comments and newlines
        if self._check(TokenType.COMMENT, TokenType.NEWLINE):
            self._advance()
            return None
        
        # Class declaration (contract)
        if self._check(TokenType.CLASS):
            return self._parse_class()
        
        # Function declaration
        if self._check(TokenType.DEF):
            return self._parse_function()
        
        # Test declaration (decorated function)
        if self._check_decorator():
            return self._parse_decorated_function()
        
        # Variable assignment
        if self._check(TokenType.IDENTIFIER) and self._check_ahead(TokenType.ASSIGN):
            return self._parse_variable_def()
        
        # Skip unknown tokens
        self._advance()
        return None
    
    def _parse_class(self) -> SmartPyContractDef:
        """Parse class definition (smart contract)."""
        self._consume(TokenType.CLASS, "Expected 'class'")
        name = self._consume(TokenType.IDENTIFIER, "Expected class name").value
        
        # Base classes
        base_classes = []
        if self._match(TokenType.LEFT_PAREN):
            if not self._check(TokenType.RIGHT_PAREN):
                base_classes.append(self._consume(TokenType.IDENTIFIER, "Expected base class").value)
                while self._match(TokenType.COMMA):
                    base_classes.append(self._consume(TokenType.IDENTIFIER, "Expected base class").value)
            self._consume(TokenType.RIGHT_PAREN, "Expected ')'")
        
        self._consume(TokenType.COLON, "Expected ':'")
        self._consume(TokenType.NEWLINE, "Expected newline")
        self._consume(TokenType.INDENT, "Expected indentation")
        
        # Parse class body
        methods = []
        entry_points = []
        init_method = None
        
        while not self._check(TokenType.DEDENT) and not self._is_at_end():
            if self._check(TokenType.DEF):
                method = self._parse_method()
                if method.name == "__init__":
                    init_method = method
                elif method.is_entry_point:
                    entry_points.append(method)
                else:
                    methods.append(method)
            else:
                self._advance()  # Skip unknown content
        
        self._consume(TokenType.DEDENT, "Expected dedent")
        
        return SmartPyContractDef(
            name=name,
            base_classes=base_classes,
            methods=methods,
            entry_points=entry_points,
            init_method=init_method,
            source_info=self._get_source_info()
        )
    
    def _parse_method(self) -> SmartPyMethodDef:
        """Parse method definition."""
        decorators = []
        
        # Check for decorators
        while self._check_decorator():
            decorators.append(self._parse_decorator())
        
        self._consume(TokenType.DEF, "Expected 'def'")
        name = self._consume(TokenType.IDENTIFIER, "Expected method name").value
        
        # Parameters
        self._consume(TokenType.LEFT_PAREN, "Expected '('")
        parameters = []
        
        if not self._check(TokenType.RIGHT_PAREN):
            parameters.append(self._consume(TokenType.IDENTIFIER, "Expected parameter").value)
            while self._match(TokenType.COMMA):
                parameters.append(self._consume(TokenType.IDENTIFIER, "Expected parameter").value)
        
        self._consume(TokenType.RIGHT_PAREN, "Expected ')'")
        self._consume(TokenType.COLON, "Expected ':'")
        self._consume(TokenType.NEWLINE, "Expected newline")
        
        # Method body
        body = self._parse_block()
        
        is_entry_point = "@sp.entry_point" in decorators
        
        return SmartPyMethodDef(
            name=name,
            parameters=parameters,
            body=body,
            decorators=decorators,
            is_entry_point=is_entry_point,
            source_info=self._get_source_info()
        )
    
    def _parse_function(self) -> SmartPyFunctionDef:
        """Parse function definition."""
        self._consume(TokenType.DEF, "Expected 'def'")
        name = self._consume(TokenType.IDENTIFIER, "Expected function name").value
        
        # Parameters
        self._consume(TokenType.LEFT_PAREN, "Expected '('")
        parameters = []
        
        if not self._check(TokenType.RIGHT_PAREN):
            parameters.append(self._consume(TokenType.IDENTIFIER, "Expected parameter").value)
            while self._match(TokenType.COMMA):
                parameters.append(self._consume(TokenType.IDENTIFIER, "Expected parameter").value)
        
        self._consume(TokenType.RIGHT_PAREN, "Expected ')'")
        self._consume(TokenType.COLON, "Expected ':'")
        self._consume(TokenType.NEWLINE, "Expected newline")
        
        # Function body
        body = self._parse_block()
        
        return SmartPyFunctionDef(
            name=name,
            parameters=parameters,
            body=body,
            decorators=[],
            source_info=self._get_source_info()
        )
    
    def _parse_decorated_function(self) -> SmartPyDeclaration:
        """Parse decorated function (test)."""
        decorators = []
        
        while self._check_decorator():
            decorators.append(self._parse_decorator())
        
        if "@sp.add_test" in decorators:
            return self._parse_test_function(decorators)
        else:
            # Regular function with decorators
            func = self._parse_function()
            func.decorators = decorators
            return func
    
    def _parse_test_function(self, decorators: List[str]) -> SmartPyTestDef:
        """Parse test function."""
        self._consume(TokenType.DEF, "Expected 'def'")
        name = self._consume(TokenType.IDENTIFIER, "Expected test function name").value
        
        self._consume(TokenType.LEFT_PAREN, "Expected '('")
        self._consume(TokenType.RIGHT_PAREN, "Expected ')'")
        self._consume(TokenType.COLON, "Expected ':'")
        self._consume(TokenType.NEWLINE, "Expected newline")
        
        body = self._parse_block()
        
        return SmartPyTestDef(
            name=name,
            body=body,
            source_info=self._get_source_info()
        )
    
    def _parse_decorator(self) -> str:
        """Parse decorator."""
        # Assume decorator is on its own line starting with @
        token = self._advance()
        decorator_text = "@"
        
        # Parse decorator name and potential arguments
        while not self._check(TokenType.NEWLINE) and not self._is_at_end():
            token = self._advance()
            decorator_text += token.value
        
        self._match(TokenType.NEWLINE)  # Consume newline after decorator
        return decorator_text
    
    def _parse_block(self) -> List[SmartPyStatement]:
        """Parse indented block of statements."""
        statements = []
        
        self._consume(TokenType.INDENT, "Expected indentation")
        
        while not self._check(TokenType.DEDENT) and not self._is_at_end():
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
        
        self._consume(TokenType.DEDENT, "Expected dedent")
        
        return statements
    
    def _parse_statement(self) -> Optional[SmartPyStatement]:
        """Parse statement."""
        # Skip comments and empty lines
        if self._check(TokenType.COMMENT, TokenType.NEWLINE):
            self._advance()
            return None
        
        # Assignment
        if self._check(TokenType.IDENTIFIER) and self._check_ahead(TokenType.ASSIGN):
            return self._parse_assignment()
        
        # Augmented assignment
        if self._check(TokenType.IDENTIFIER) and self._check_ahead_augmented_assign():
            return self._parse_augmented_assignment()
        
        # Control flow
        if self._check(TokenType.IF):
            return self._parse_if()
        
        if self._check(TokenType.FOR):
            return self._parse_for()
        
        if self._check(TokenType.WHILE):
            return self._parse_while()
        
        if self._check(TokenType.RETURN):
            return self._parse_return()
        
        # Expression statement
        expr = self._parse_expression()
        if expr:
            self._match(TokenType.NEWLINE)  # Optional newline
            return SmartPyExpressionStatement(expression=expr)
        
        # Skip unknown tokens
        self._advance()
        return None
    
    def _parse_assignment(self) -> SmartPyAssignment:
        """Parse assignment statement."""
        target = self._parse_expression()
        self._consume(TokenType.ASSIGN, "Expected '='")
        value = self._parse_expression()
        self._match(TokenType.NEWLINE)
        
        return SmartPyAssignment(
            target=target,
            value=value,
            source_info=self._get_source_info()
        )
    
    def _parse_augmented_assignment(self) -> SmartPyAugmentedAssignment:
        """Parse augmented assignment statement."""
        target = self._parse_expression()
        
        operator = ""
        if self._match(TokenType.PLUS_ASSIGN):
            operator = "+="
        elif self._match(TokenType.MINUS_ASSIGN):
            operator = "-="
        elif self._match(TokenType.MULTIPLY_ASSIGN):
            operator = "*="
        elif self._match(TokenType.DIVIDE_ASSIGN):
            operator = "/="
        
        value = self._parse_expression()
        self._match(TokenType.NEWLINE)
        
        return SmartPyAugmentedAssignment(
            target=target,
            operator=operator,
            value=value,
            source_info=self._get_source_info()
        )
    
    def _parse_if(self) -> SmartPyIf:
        """Parse if statement."""
        self._consume(TokenType.IF, "Expected 'if'")
        test = self._parse_expression()
        self._consume(TokenType.COLON, "Expected ':'")
        self._consume(TokenType.NEWLINE, "Expected newline")
        
        body = self._parse_block()
        orelse = []
        
        if self._match(TokenType.ELSE):
            self._consume(TokenType.COLON, "Expected ':'")
            self._consume(TokenType.NEWLINE, "Expected newline")
            orelse = self._parse_block()
        
        return SmartPyIf(
            test=test,
            body=body,
            orelse=orelse,
            source_info=self._get_source_info()
        )
    
    def _parse_for(self) -> SmartPyFor:
        """Parse for statement."""
        self._consume(TokenType.FOR, "Expected 'for'")
        target = self._consume(TokenType.IDENTIFIER, "Expected loop variable").value
        self._consume(TokenType.IN, "Expected 'in'")
        iter_expr = self._parse_expression()
        self._consume(TokenType.COLON, "Expected ':'")
        self._consume(TokenType.NEWLINE, "Expected newline")
        
        body = self._parse_block()
        
        return SmartPyFor(
            target=target,
            iter=iter_expr,
            body=body,
            source_info=self._get_source_info()
        )
    
    def _parse_while(self) -> SmartPyWhile:
        """Parse while statement."""
        self._consume(TokenType.WHILE, "Expected 'while'")
        test = self._parse_expression()
        self._consume(TokenType.COLON, "Expected ':'")
        self._consume(TokenType.NEWLINE, "Expected newline")
        
        body = self._parse_block()
        
        return SmartPyWhile(
            test=test,
            body=body,
            source_info=self._get_source_info()
        )
    
    def _parse_return(self) -> SmartPyReturn:
        """Parse return statement."""
        self._consume(TokenType.RETURN, "Expected 'return'")
        
        value = None
        if not self._check(TokenType.NEWLINE):
            value = self._parse_expression()
        
        self._match(TokenType.NEWLINE)
        
        return SmartPyReturn(
            value=value,
            source_info=self._get_source_info()
        )
    
    def _parse_expression(self) -> SmartPyExpression:
        """Parse expression."""
        return self._parse_or()
    
    def _parse_or(self) -> SmartPyExpression:
        """Parse logical OR expression."""
        expr = self._parse_and()
        
        while self._match(TokenType.OR):
            operator = "or"
            right = self._parse_and()
            expr = SmartPyBinaryOp(
                left=expr,
                operator=operator,
                right=right,
                source_info=self._get_source_info()
            )
        
        return expr
    
    def _parse_and(self) -> SmartPyExpression:
        """Parse logical AND expression."""
        expr = self._parse_not()
        
        while self._match(TokenType.AND):
            operator = "and"
            right = self._parse_not()
            expr = SmartPyBinaryOp(
                left=expr,
                operator=operator,
                right=right,
                source_info=self._get_source_info()
            )
        
        return expr
    
    def _parse_not(self) -> SmartPyExpression:
        """Parse logical NOT expression."""
        if self._match(TokenType.NOT):
            operand = self._parse_not()
            return SmartPyUnaryOp(
                operator="not",
                operand=operand,
                source_info=self._get_source_info()
            )
        
        return self._parse_comparison()
    
    def _parse_comparison(self) -> SmartPyExpression:
        """Parse comparison expression."""
        expr = self._parse_addition()
        
        while True:
            if self._match(TokenType.EQUAL):
                operator = "=="
            elif self._match(TokenType.NOT_EQUAL):
                operator = "!="
            elif self._match(TokenType.LESS_THAN):
                operator = "<"
            elif self._match(TokenType.LESS_EQUAL):
                operator = "<="
            elif self._match(TokenType.GREATER_THAN):
                operator = ">"
            elif self._match(TokenType.GREATER_EQUAL):
                operator = ">="
            else:
                break
            
            right = self._parse_addition()
            expr = SmartPyBinaryOp(
                left=expr,
                operator=operator,
                right=right,
                source_info=self._get_source_info()
            )
        
        return expr
    
    def _parse_addition(self) -> SmartPyExpression:
        """Parse addition/subtraction expression."""
        expr = self._parse_multiplication()
        
        while True:
            if self._match(TokenType.PLUS):
                operator = "+"
            elif self._match(TokenType.MINUS):
                operator = "-"
            else:
                break
            
            right = self._parse_multiplication()
            expr = SmartPyBinaryOp(
                left=expr,
                operator=operator,
                right=right,
                source_info=self._get_source_info()
            )
        
        return expr
    
    def _parse_multiplication(self) -> SmartPyExpression:
        """Parse multiplication/division expression."""
        expr = self._parse_unary()
        
        while True:
            if self._match(TokenType.MULTIPLY):
                operator = "*"
            elif self._match(TokenType.DIVIDE):
                operator = "/"
            elif self._match(TokenType.MODULO):
                operator = "%"
            else:
                break
            
            right = self._parse_unary()
            expr = SmartPyBinaryOp(
                left=expr,
                operator=operator,
                right=right,
                source_info=self._get_source_info()
            )
        
        return expr
    
    def _parse_unary(self) -> SmartPyExpression:
        """Parse unary expression."""
        if self._match(TokenType.MINUS):
            operand = self._parse_unary()
            return SmartPyUnaryOp(
                operator="-",
                operand=operand,
                source_info=self._get_source_info()
            )
        
        if self._match(TokenType.PLUS):
            operand = self._parse_unary()
            return SmartPyUnaryOp(
                operator="+",
                operand=operand,
                source_info=self._get_source_info()
            )
        
        return self._parse_call()
    
    def _parse_call(self) -> SmartPyExpression:
        """Parse function call and attribute access."""
        expr = self._parse_primary()
        
        while True:
            if self._match(TokenType.LEFT_PAREN):
                # Function call
                args = []
                keywords = {}
                
                if not self._check(TokenType.RIGHT_PAREN):
                    args.append(self._parse_expression())
                    while self._match(TokenType.COMMA):
                        args.append(self._parse_expression())
                
                self._consume(TokenType.RIGHT_PAREN, "Expected ')'")
                expr = SmartPyFunctionCall(
                    function=expr,
                    args=args,
                    keywords=keywords,
                    source_info=self._get_source_info()
                )
            
            elif self._match(TokenType.DOT):
                # Attribute access
                attribute = self._consume(TokenType.IDENTIFIER, "Expected attribute name").value
                expr = SmartPyAttributeAccess(
                    object=expr,
                    attribute=attribute,
                    source_info=self._get_source_info()
                )
            
            elif self._match(TokenType.LEFT_BRACKET):
                # Index access
                index = self._parse_expression()
                self._consume(TokenType.RIGHT_BRACKET, "Expected ']'")
                expr = SmartPyIndexAccess(
                    object=expr,
                    index=index,
                    source_info=self._get_source_info()
                )
            
            else:
                break
        
        return expr
    
    def _parse_primary(self) -> SmartPyExpression:
        """Parse primary expression."""
        # Literals
        if self._match(TokenType.INTEGER):
            value = int(self._previous().value)
            return SmartPyLiteral(value=value, source_info=self._get_source_info())
        
        if self._match(TokenType.FLOAT):
            value = float(self._previous().value)
            return SmartPyLiteral(value=value, source_info=self._get_source_info())
        
        if self._match(TokenType.STRING):
            value = self._previous().value
            return SmartPyLiteral(value=value, source_info=self._get_source_info())
        
        if self._match(TokenType.BOOLEAN):
            value = self._previous().value == "True"
            return SmartPyLiteral(value=value, source_info=self._get_source_info())
        
        if self._match(TokenType.NONE):
            return SmartPyLiteral(value=None, source_info=self._get_source_info())
        
        # Identifiers
        if self._match(TokenType.IDENTIFIER):
            name = self._previous().value
            return SmartPyIdentifier(name=name, source_info=self._get_source_info())
        
        # Parenthesized expression
        if self._match(TokenType.LEFT_PAREN):
            expr = self._parse_expression()
            self._consume(TokenType.RIGHT_PAREN, "Expected ')'")
            return expr
        
        # List literal
        if self._match(TokenType.LEFT_BRACKET):
            elements = []
            
            if not self._check(TokenType.RIGHT_BRACKET):
                elements.append(self._parse_expression())
                while self._match(TokenType.COMMA):
                    elements.append(self._parse_expression())
            
            self._consume(TokenType.RIGHT_BRACKET, "Expected ']'")
            return SmartPyListLiteral(elements=elements, source_info=self._get_source_info())
        
        # Dict/Map literal
        if self._match(TokenType.LEFT_BRACE):
            pairs = []
            
            if not self._check(TokenType.RIGHT_BRACE):
                key = self._parse_expression()
                self._consume(TokenType.COLON, "Expected ':'")
                value = self._parse_expression()
                pairs.append((key, value))
                
                while self._match(TokenType.COMMA):
                    key = self._parse_expression()
                    self._consume(TokenType.COLON, "Expected ':'")
                    value = self._parse_expression()
                    pairs.append((key, value))
            
            self._consume(TokenType.RIGHT_BRACE, "Expected '}'")
            return SmartPyMapLiteral(pairs=pairs, source_info=self._get_source_info())
        
        raise ParseError(f"Unexpected token: {self._peek().value}")
    
    def _parse_variable_def(self) -> SmartPyVariableDef:
        """Parse variable definition."""
        name = self._consume(TokenType.IDENTIFIER, "Expected variable name").value
        self._consume(TokenType.ASSIGN, "Expected '='")
        value = self._parse_expression()
        self._match(TokenType.NEWLINE)
        
        return SmartPyVariableDef(
            name=name,
            value=value,
            source_info=self._get_source_info()
        )
    
    # Helper methods
    def _match(self, *types: TokenType) -> bool:
        """Check if current token matches any of the given types."""
        for token_type in types:
            if self._check(token_type):
                self._advance()
                return True
        return False
    
    def _check(self, *types: TokenType) -> bool:
        """Check if current token is of given type."""
        if self._is_at_end():
            return False
        return self._peek().type in types
    
    def _check_ahead(self, token_type: TokenType, offset: int = 1) -> bool:
        """Check token at offset ahead."""
        if self.current + offset >= len(self.tokens):
            return False
        return self.tokens[self.current + offset].type == token_type
    
    def _check_ahead_augmented_assign(self) -> bool:
        """Check if next token is augmented assignment."""
        return self._check_ahead(TokenType.PLUS_ASSIGN) or \
               self._check_ahead(TokenType.MINUS_ASSIGN) or \
               self._check_ahead(TokenType.MULTIPLY_ASSIGN) or \
               self._check_ahead(TokenType.DIVIDE_ASSIGN)
    
    def _check_decorator(self) -> bool:
        """Check if current position has a decorator."""
        return self._check(TokenType.IDENTIFIER) and self._peek().value == "@"
    
    def _advance(self) -> Token:
        """Consume current token and return it."""
        if not self._is_at_end():
            self.current += 1
        return self._previous()
    
    def _is_at_end(self) -> bool:
        """Check if we're at end of tokens."""
        return self._peek().type == TokenType.EOF
    
    def _peek(self) -> Token:
        """Return current token without advancing."""
        return self.tokens[self.current]
    
    def _previous(self) -> Token:
        """Return previous token."""
        return self.tokens[self.current - 1]
    
    def _consume(self, token_type: TokenType, message: str) -> Token:
        """Consume token of expected type or raise error."""
        if self._check(token_type):
            return self._advance()
        
        current = self._peek()
        raise ParseError(f"{message}. Got {current.type} at line {current.source_info.line}")
    
    def _get_source_info(self) -> SourceInfo:
        """Get source info for current position."""
        token = self._peek() if not self._is_at_end() else self._previous()
        return token.source_info


class ParseError(Exception):
    """Exception raised during parsing."""
    pass 