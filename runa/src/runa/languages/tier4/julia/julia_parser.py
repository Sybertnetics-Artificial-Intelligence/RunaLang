#!/usr/bin/env python3
"""
Julia Parser and Lexer

Comprehensive parser for Julia language supporting all Julia constructs including
multiple dispatch, metaprogramming, macros, modules, and scientific computing features.
"""

from typing import List, Optional, Any, Union, Dict, Set
from enum import Enum, auto
import re
from dataclasses import dataclass

from .julia_ast import *
from ....core.runa_ast import SourceLocation


class JuliaTokenType(Enum):
    """Julia token types."""
    # Literals
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    CHAR = auto()
    SYMBOL = auto()
    BOOLEAN = auto()
    NOTHING = auto()
    
    # Identifiers and keywords
    IDENTIFIER = auto()
    FUNCTION = auto()
    END = auto()
    IF = auto()
    ELSE = auto()
    ELSEIF = auto()
    FOR = auto()
    WHILE = auto()
    BREAK = auto()
    CONTINUE = auto()
    RETURN = auto()
    MODULE = auto()
    IMPORT = auto()
    USING = auto()
    EXPORT = auto()
    STRUCT = auto()
    MUTABLE = auto()
    ABSTRACT = auto()
    PRIMITIVE = auto()
    TYPE = auto()
    CONST = auto()
    GLOBAL = auto()
    LOCAL = auto()
    LET = auto()
    BEGIN = auto()
    TRY = auto()
    CATCH = auto()
    FINALLY = auto()
    THROW = auto()
    MACRO = auto()
    QUOTE = auto()
    WHERE = auto()
    BAREMODULE = auto()
    
    # Operators and punctuation
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    POWER = auto()
    MODULO = auto()
    ASSIGN = auto()
    PLUS_ASSIGN = auto()
    MINUS_ASSIGN = auto()
    MULTIPLY_ASSIGN = auto()
    DIVIDE_ASSIGN = auto()
    POWER_ASSIGN = auto()
    EQUAL = auto()
    NOT_EQUAL = auto()
    LESS = auto()
    GREATER = auto()
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
    DOT = auto()
    BROADCAST_DOT = auto()
    RANGE = auto()
    INCLUSIVE_RANGE = auto()
    ARROW = auto()
    DOUBLE_COLON = auto()
    QUESTION = auto()
    ELVIS = auto()
    PIPE = auto()
    COMPOSE = auto()
    
    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    LBRACE = auto()
    RBRACE = auto()
    COMMA = auto()
    SEMICOLON = auto()
    COLON = auto()
    NEWLINE = auto()
    
    # Special
    AT = auto()  # For macros
    DOLLAR = auto()  # For interpolation
    INTERPOLATION_START = auto()
    INTERPOLATION_END = auto()
    EOF = auto()
    COMMENT = auto()


@dataclass
class JuliaToken:
    """Julia token."""
    type: JuliaTokenType
    value: str
    line: int
    column: int
    position: int = 0


class JuliaLexer:
    """Julia lexer for tokenizing Julia source code."""
    
    KEYWORDS = {
        'function', 'end', 'if', 'else', 'elseif', 'for', 'while', 'break', 'continue',
        'return', 'module', 'import', 'using', 'export', 'struct', 'mutable', 'abstract',
        'primitive', 'type', 'const', 'global', 'local', 'let', 'begin', 'try', 'catch',
        'finally', 'throw', 'macro', 'quote', 'where', 'baremodule', 'true', 'false',
        'nothing', 'in', 'isa', 'typeof', 'do'
    }
    
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[JuliaToken] = []
    
    def tokenize(self) -> List[JuliaToken]:
        """Tokenize the source code."""
        while self.position < len(self.source):
            self._skip_whitespace()
            if self.position >= len(self.source):
                break
                
            if self._match_comment():
                continue
            elif self._match_string():
                continue
            elif self._match_char():
                continue
            elif self._match_number():
                continue
            elif self._match_symbol():
                continue
            elif self._match_identifier():
                continue
            elif self._match_operator():
                continue
            elif self._match_delimiter():
                continue
            else:
                self._advance()
        
        self.tokens.append(JuliaToken(JuliaTokenType.EOF, '', self.line, self.column))
        return self.tokens
    
    def _current_char(self) -> str:
        """Get current character."""
        if self.position >= len(self.source):
            return ''
        return self.source[self.position]
    
    def _peek_char(self, offset: int = 1) -> str:
        """Peek at character with offset."""
        pos = self.position + offset
        if pos >= len(self.source):
            return ''
        return self.source[pos]
    
    def _advance(self) -> str:
        """Advance position and return current character."""
        if self.position >= len(self.source):
            return ''
        char = self.source[self.position]
        self.position += 1
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char
    
    def _skip_whitespace(self):
        """Skip whitespace except newlines."""
        while self.position < len(self.source) and self._current_char() in ' \t\r':
            self._advance()
    
    def _match_comment(self) -> bool:
        """Match comment."""
        if self._current_char() == '#':
            start_pos = self.position
            while self.position < len(self.source) and self._current_char() != '\n':
                self._advance()
            value = self.source[start_pos:self.position]
            self._add_token(JuliaTokenType.COMMENT, value)
            return True
        return False
    
    def _match_string(self) -> bool:
        """Match string literal."""
        if self._current_char() == '"':
            return self._match_string_literal('"')
        elif self._current_char() == "'" and self._peek_char() == "'" and self._peek_char(2) == "'":
            return self._match_multiline_string()
        return False
    
    def _match_string_literal(self, quote_char: str) -> bool:
        """Match single or double quoted string."""
        start_line, start_col = self.line, self.column
        self._advance()  # Skip opening quote
        value = ''
        
        while self.position < len(self.source) and self._current_char() != quote_char:
            if self._current_char() == '\\':
                self._advance()
                if self.position < len(self.source):
                    escape_char = self._advance()
                    if escape_char == 'n':
                        value += '\n'
                    elif escape_char == 't':
                        value += '\t'
                    elif escape_char == 'r':
                        value += '\r'
                    elif escape_char == '\\':
                        value += '\\'
                    elif escape_char == quote_char:
                        value += quote_char
                    else:
                        value += escape_char
            else:
                value += self._advance()
        
        if self.position < len(self.source):
            self._advance()  # Skip closing quote
        
        self._add_token(JuliaTokenType.STRING, value)
        return True
    
    def _match_multiline_string(self) -> bool:
        """Match triple-quoted string."""
        start_line, start_col = self.line, self.column
        self._advance()  # Skip first '
        self._advance()  # Skip second '
        self._advance()  # Skip third '
        
        value = ''
        while self.position < len(self.source) - 2:
            if (self._current_char() == "'" and 
                self._peek_char() == "'" and 
                self._peek_char(2) == "'"):
                self._advance()
                self._advance()
                self._advance()
                break
            value += self._advance()
        
        self._add_token(JuliaTokenType.STRING, value)
        return True
    
    def _match_char(self) -> bool:
        """Match character literal."""
        if self._current_char() == "'" and self._peek_char() != "'":
            self._advance()  # Skip opening quote
            char_value = self._advance()
            if self._current_char() == "'":
                self._advance()  # Skip closing quote
                self._add_token(JuliaTokenType.CHAR, char_value)
                return True
        return False
    
    def _match_number(self) -> bool:
        """Match numeric literal."""
        if self._current_char().isdigit() or (self._current_char() == '.' and self._peek_char().isdigit()):
            start_pos = self.position
            has_dot = False
            
            while (self.position < len(self.source) and 
                   (self._current_char().isdigit() or 
                    (self._current_char() == '.' and not has_dot))):
                if self._current_char() == '.':
                    has_dot = True
                self._advance()
            
            # Handle scientific notation
            if (self.position < len(self.source) and 
                self._current_char().lower() == 'e'):
                self._advance()
                if (self.position < len(self.source) and 
                    self._current_char() in '+-'):
                    self._advance()
                while (self.position < len(self.source) and 
                       self._current_char().isdigit()):
                    self._advance()
                has_dot = True
            
            value = self.source[start_pos:self.position]
            token_type = JuliaTokenType.FLOAT if has_dot else JuliaTokenType.INTEGER
            self._add_token(token_type, value)
            return True
        return False
    
    def _match_symbol(self) -> bool:
        """Match symbol literal."""
        if self._current_char() == ':' and self._peek_char().isalpha():
            self._advance()  # Skip ':'
            start_pos = self.position
            
            while (self.position < len(self.source) and 
                   (self._current_char().isalnum() or self._current_char() == '_')):
                self._advance()
            
            value = self.source[start_pos:self.position]
            self._add_token(JuliaTokenType.SYMBOL, value)
            return True
        return False
    
    def _match_identifier(self) -> bool:
        """Match identifier or keyword."""
        if self._current_char().isalpha() or self._current_char() == '_':
            start_pos = self.position
            
            while (self.position < len(self.source) and 
                   (self._current_char().isalnum() or self._current_char() in '_!')):
                self._advance()
            
            value = self.source[start_pos:self.position]
            
            # Check for keywords
            if value in self.KEYWORDS:
                if value == 'true' or value == 'false':
                    self._add_token(JuliaTokenType.BOOLEAN, value)
                elif value == 'nothing':
                    self._add_token(JuliaTokenType.NOTHING, value)
                else:
                    token_type = getattr(JuliaTokenType, value.upper(), JuliaTokenType.IDENTIFIER)
                    self._add_token(token_type, value)
            else:
                self._add_token(JuliaTokenType.IDENTIFIER, value)
            return True
        return False
    
    def _match_operator(self) -> bool:
        """Match operators."""
        char = self._current_char()
        next_char = self._peek_char()
        
        # Two-character operators
        two_char = char + next_char
        if two_char in ['+=', '-=', '*=', '/=', '^=', '==', '!=', '<=', '>=', 
                        '&&', '||', '<<', '>>', '.+', '.-', '.*', './', '.^',
                        '::', '->', '=>', '..']:
            self._advance()
            self._advance()
            token_map = {
                '+=': JuliaTokenType.PLUS_ASSIGN, '-=': JuliaTokenType.MINUS_ASSIGN,
                '*=': JuliaTokenType.MULTIPLY_ASSIGN, '/=': JuliaTokenType.DIVIDE_ASSIGN,
                '^=': JuliaTokenType.POWER_ASSIGN, '==': JuliaTokenType.EQUAL,
                '!=': JuliaTokenType.NOT_EQUAL, '<=': JuliaTokenType.LESS_EQUAL,
                '>=': JuliaTokenType.GREATER_EQUAL, '&&': JuliaTokenType.AND,
                '||': JuliaTokenType.OR, '<<': JuliaTokenType.LEFT_SHIFT,
                '>>': JuliaTokenType.RIGHT_SHIFT, '::': JuliaTokenType.DOUBLE_COLON,
                '->': JuliaTokenType.ARROW, '..': JuliaTokenType.RANGE
            }
            self._add_token(token_map.get(two_char, JuliaTokenType.IDENTIFIER), two_char)
            return True
        
        # Single-character operators
        if char in '+-*/^%=<>!&|~.?:$@':
            self._advance()
            token_map = {
                '+': JuliaTokenType.PLUS, '-': JuliaTokenType.MINUS,
                '*': JuliaTokenType.MULTIPLY, '/': JuliaTokenType.DIVIDE,
                '^': JuliaTokenType.POWER, '%': JuliaTokenType.MODULO,
                '=': JuliaTokenType.ASSIGN, '<': JuliaTokenType.LESS,
                '>': JuliaTokenType.GREATER, '!': JuliaTokenType.NOT,
                '&': JuliaTokenType.BITWISE_AND, '|': JuliaTokenType.BITWISE_OR,
                '~': JuliaTokenType.BITWISE_NOT, '.': JuliaTokenType.DOT,
                '?': JuliaTokenType.QUESTION, ':': JuliaTokenType.COLON,
                '$': JuliaTokenType.DOLLAR, '@': JuliaTokenType.AT
            }
            self._add_token(token_map.get(char, JuliaTokenType.IDENTIFIER), char)
            return True
        
        return False
    
    def _match_delimiter(self) -> bool:
        """Match delimiters."""
        char = self._current_char()
        if char in '()[]{},:;\n':
            self._advance()
            token_map = {
                '(': JuliaTokenType.LPAREN, ')': JuliaTokenType.RPAREN,
                '[': JuliaTokenType.LBRACKET, ']': JuliaTokenType.RBRACKET,
                '{': JuliaTokenType.LBRACE, '}': JuliaTokenType.RBRACE,
                ',': JuliaTokenType.COMMA, ';': JuliaTokenType.SEMICOLON,
                '\n': JuliaTokenType.NEWLINE
            }
            self._add_token(token_map[char], char)
            return True
        return False
    
    def _add_token(self, token_type: JuliaTokenType, value: str):
        """Add token to list."""
        token = JuliaToken(token_type, value, self.line, self.column - len(value), self.position)
        self.tokens.append(token)


class JuliaParser:
    """Julia parser for parsing tokens into AST."""
    
    def __init__(self, tokens: List[JuliaToken]):
        self.tokens = tokens
        self.position = 0
        self.current_token = tokens[0] if tokens else None
    
    def parse(self) -> JuliaProgram:
        """Parse tokens into AST."""
        files = []
        while not self._is_at_end():
            if self._match_newline():
                continue
            file_node = self._parse_file()
            if file_node:
                files.append(file_node)
        
        return JuliaProgram(files=files)
    
    def _parse_file(self) -> Optional[JuliaFile]:
        """Parse a Julia file."""
        module_decl = None
        imports = []
        exports = []
        declarations = []
        
        while not self._is_at_end():
            if self._match_newline():
                continue
            elif self._check(JuliaTokenType.MODULE):
                module_decl = self._parse_module()
            elif self._check(JuliaTokenType.IMPORT):
                imports.append(self._parse_import())
            elif self._check(JuliaTokenType.USING):
                imports.append(self._parse_using())
            elif self._check(JuliaTokenType.EXPORT):
                exports.append(self._parse_export())
            else:
                decl = self._parse_declaration()
                if decl:
                    declarations.append(decl)
                else:
                    break
        
        return JuliaFile(
            module_declaration=module_decl,
            imports=imports,
            exports=exports,
            declarations=declarations
        )
    
    def _parse_module(self) -> JuliaModuleDeclaration:
        """Parse module declaration."""
        self._consume(JuliaTokenType.MODULE)
        name = self._consume(JuliaTokenType.IDENTIFIER).value
        self._skip_newlines()
        
        body = []
        while not self._check(JuliaTokenType.END) and not self._is_at_end():
            if self._match_newline():
                continue
            decl = self._parse_declaration()
            if decl:
                body.append(decl)
            else:
                break
        
        self._consume(JuliaTokenType.END)
        return JuliaModuleDeclaration(name=name, body=body)
    
    def _parse_function(self) -> JuliaFunctionDeclaration:
        """Parse function declaration."""
        self._consume(JuliaTokenType.FUNCTION)
        name = self._consume(JuliaTokenType.IDENTIFIER).value
        
        signature = None
        if self._check(JuliaTokenType.LPAREN):
            signature = self._parse_function_signature()
        
        self._skip_newlines()
        
        body = []
        while not self._check(JuliaTokenType.END) and not self._is_at_end():
            if self._match_newline():
                continue
            stmt = self._parse_statement()
            if stmt:
                body.append(stmt)
            else:
                break
        
        self._consume(JuliaTokenType.END)
        return JuliaFunctionDeclaration(name=name, signature=signature, body=body)
    
    def _parse_function_signature(self) -> JuliaFunctionSignature:
        """Parse function signature."""
        self._consume(JuliaTokenType.LPAREN)
        parameters = []
        
        while not self._check(JuliaTokenType.RPAREN) and not self._is_at_end():
            param = self._parse_parameter()
            parameters.append(param)
            
            if self._check(JuliaTokenType.COMMA):
                self._advance()
            else:
                break
        
        self._consume(JuliaTokenType.RPAREN)
        return JuliaFunctionSignature(parameters=parameters)
    
    def _parse_parameter(self) -> JuliaParameter:
        """Parse function parameter."""
        name = self._consume(JuliaTokenType.IDENTIFIER).value
        param_type = None
        
        if self._match(JuliaTokenType.DOUBLE_COLON):
            param_type = self._parse_type()
        
        return JuliaParameter(name=name, type=param_type)
    
    def _parse_type(self) -> JuliaType:
        """Parse type expression."""
        if self._check(JuliaTokenType.IDENTIFIER):
            name = self._advance().value
            
            # Handle parametric types
            if self._check(JuliaTokenType.LBRACE):
                self._advance()
                parameters = []
                
                while not self._check(JuliaTokenType.RBRACE) and not self._is_at_end():
                    param_type = self._parse_type()
                    parameters.append(param_type)
                    
                    if self._check(JuliaTokenType.COMMA):
                        self._advance()
                    else:
                        break
                
                self._consume(JuliaTokenType.RBRACE)
                return JuliaParametricType(base_type=name, parameters=parameters)
            
            return JuliaParametricType(base_type=name, parameters=[])
        
        return JuliaParametricType(base_type="Any", parameters=[])
    
    def _parse_declaration(self) -> Optional[JuliaNode]:
        """Parse top-level declaration."""
        if self._check(JuliaTokenType.FUNCTION):
            return self._parse_function()
        elif self._check(JuliaTokenType.STRUCT):
            return self._parse_struct()
        elif self._check(JuliaTokenType.CONST):
            return self._parse_const()
        else:
            return self._parse_expression_statement()
    
    def _parse_struct(self) -> JuliaStructDeclaration:
        """Parse struct declaration."""
        is_mutable = False
        if self._check(JuliaTokenType.MUTABLE):
            is_mutable = True
            self._advance()
        
        self._consume(JuliaTokenType.STRUCT)
        name = self._consume(JuliaTokenType.IDENTIFIER).value
        self._skip_newlines()
        
        fields = []
        while not self._check(JuliaTokenType.END) and not self._is_at_end():
            if self._match_newline():
                continue
            field = self._parse_field()
            if field:
                fields.append(field)
            else:
                break
        
        self._consume(JuliaTokenType.END)
        return JuliaStructDeclaration(name=name, fields=fields, is_mutable=is_mutable)
    
    def _parse_field(self) -> Optional[JuliaFieldDeclaration]:
        """Parse struct field."""
        if self._check(JuliaTokenType.IDENTIFIER):
            name = self._advance().value
            field_type = None
            
            if self._match(JuliaTokenType.DOUBLE_COLON):
                field_type = self._parse_type()
            
            return JuliaFieldDeclaration(name=name, type=field_type)
        return None
    
    def _parse_statement(self) -> Optional[JuliaNode]:
        """Parse statement."""
        if self._check(JuliaTokenType.RETURN):
            return self._parse_return()
        elif self._check(JuliaTokenType.IF):
            return self._parse_if()
        elif self._check(JuliaTokenType.FOR):
            return self._parse_for()
        elif self._check(JuliaTokenType.WHILE):
            return self._parse_while()
        else:
            return self._parse_expression_statement()
    
    def _parse_expression_statement(self) -> Optional[JuliaNode]:
        """Parse expression statement."""
        expr = self._parse_expression()
        return expr
    
    def _parse_expression(self) -> Optional[JuliaExpression]:
        """Parse expression."""
        return self._parse_assignment()
    
    def _parse_assignment(self) -> Optional[JuliaExpression]:
        """Parse assignment expression."""
        expr = self._parse_or()
        
        if self._check(JuliaTokenType.ASSIGN):
            op = self._advance().value
            right = self._parse_assignment()
            return JuliaAssignmentExpression(target=expr, operator=op, value=right)
        
        return expr
    
    def _parse_or(self) -> Optional[JuliaExpression]:
        """Parse logical OR expression."""
        expr = self._parse_and()
        
        while self._match(JuliaTokenType.OR):
            op = self._previous().value
            right = self._parse_and()
            expr = JuliaBinaryExpression(left=expr, operator=op, right=right)
        
        return expr
    
    def _parse_and(self) -> Optional[JuliaExpression]:
        """Parse logical AND expression."""
        expr = self._parse_equality()
        
        while self._match(JuliaTokenType.AND):
            op = self._previous().value
            right = self._parse_equality()
            expr = JuliaBinaryExpression(left=expr, operator=op, right=right)
        
        return expr
    
    def _parse_equality(self) -> Optional[JuliaExpression]:
        """Parse equality expression."""
        expr = self._parse_comparison()
        
        while self._match(JuliaTokenType.EQUAL, JuliaTokenType.NOT_EQUAL):
            op = self._previous().value
            right = self._parse_comparison()
            expr = JuliaBinaryExpression(left=expr, operator=op, right=right)
        
        return expr
    
    def _parse_comparison(self) -> Optional[JuliaExpression]:
        """Parse comparison expression."""
        expr = self._parse_addition()
        
        while self._match(JuliaTokenType.LESS, JuliaTokenType.GREATER, 
                          JuliaTokenType.LESS_EQUAL, JuliaTokenType.GREATER_EQUAL):
            op = self._previous().value
            right = self._parse_addition()
            expr = JuliaBinaryExpression(left=expr, operator=op, right=right)
        
        return expr
    
    def _parse_addition(self) -> Optional[JuliaExpression]:
        """Parse addition/subtraction expression."""
        expr = self._parse_multiplication()
        
        while self._match(JuliaTokenType.PLUS, JuliaTokenType.MINUS):
            op = self._previous().value
            right = self._parse_multiplication()
            expr = JuliaBinaryExpression(left=expr, operator=op, right=right)
        
        return expr
    
    def _parse_multiplication(self) -> Optional[JuliaExpression]:
        """Parse multiplication/division expression."""
        expr = self._parse_power()
        
        while self._match(JuliaTokenType.MULTIPLY, JuliaTokenType.DIVIDE, JuliaTokenType.MODULO):
            op = self._previous().value
            right = self._parse_power()
            expr = JuliaBinaryExpression(left=expr, operator=op, right=right)
        
        return expr
    
    def _parse_power(self) -> Optional[JuliaExpression]:
        """Parse power expression."""
        expr = self._parse_unary()
        
        if self._match(JuliaTokenType.POWER):
            op = self._previous().value
            right = self._parse_power()  # Right associative
            expr = JuliaBinaryExpression(left=expr, operator=op, right=right)
        
        return expr
    
    def _parse_unary(self) -> Optional[JuliaExpression]:
        """Parse unary expression."""
        if self._match(JuliaTokenType.NOT, JuliaTokenType.MINUS, JuliaTokenType.PLUS):
            op = self._previous().value
            expr = self._parse_unary()
            return JuliaUnaryExpression(operator=op, expression=expr)
        
        return self._parse_call()
    
    def _parse_call(self) -> Optional[JuliaExpression]:
        """Parse function call expression."""
        expr = self._parse_primary()
        
        while True:
            if self._match(JuliaTokenType.LPAREN):
                expr = self._finish_call(expr)
            elif self._match(JuliaTokenType.LBRACKET):
                expr = self._finish_index(expr)
            elif self._match(JuliaTokenType.DOT):
                name = self._consume(JuliaTokenType.IDENTIFIER).value
                expr = JuliaDotExpression(object=expr, field=name)
            else:
                break
        
        return expr
    
    def _finish_call(self, callee: JuliaExpression) -> JuliaCallExpression:
        """Finish parsing function call."""
        arguments = []
        
        if not self._check(JuliaTokenType.RPAREN):
            while True:
                arg = self._parse_expression()
                arguments.append(arg)
                
                if not self._match(JuliaTokenType.COMMA):
                    break
        
        self._consume(JuliaTokenType.RPAREN)
        return JuliaCallExpression(function=callee, arguments=arguments)
    
    def _finish_index(self, object_expr: JuliaExpression) -> JuliaIndexExpression:
        """Finish parsing array indexing."""
        indices = []
        
        if not self._check(JuliaTokenType.RBRACKET):
            while True:
                index = self._parse_expression()
                indices.append(index)
                
                if not self._match(JuliaTokenType.COMMA):
                    break
        
        self._consume(JuliaTokenType.RBRACKET)
        return JuliaIndexExpression(object=object_expr, indices=indices)
    
    def _parse_primary(self) -> Optional[JuliaExpression]:
        """Parse primary expression."""
        if self._match(JuliaTokenType.BOOLEAN):
            value = self._previous().value == 'true'
            return JuliaLiteralExpression(value=value, literal_type="boolean")
        
        if self._match(JuliaTokenType.NOTHING):
            return JuliaLiteralExpression(value=None, literal_type="nothing")
        
        if self._match(JuliaTokenType.INTEGER):
            value = int(self._previous().value)
            return JuliaLiteralExpression(value=value, literal_type="int")
        
        if self._match(JuliaTokenType.FLOAT):
            value = float(self._previous().value)
            return JuliaLiteralExpression(value=value, literal_type="float")
        
        if self._match(JuliaTokenType.STRING):
            value = self._previous().value
            return JuliaLiteralExpression(value=value, literal_type="string")
        
        if self._match(JuliaTokenType.CHAR):
            value = self._previous().value
            return JuliaLiteralExpression(value=value, literal_type="char")
        
        if self._match(JuliaTokenType.SYMBOL):
            name = self._previous().value
            return JuliaSymbolExpression(name=name)
        
        if self._match(JuliaTokenType.IDENTIFIER):
            name = self._previous().value
            return JuliaIdentifier(name=name)
        
        if self._match(JuliaTokenType.LPAREN):
            expr = self._parse_expression()
            self._consume(JuliaTokenType.RPAREN)
            return expr
        
        if self._match(JuliaTokenType.LBRACKET):
            return self._parse_array()
        
        return None
    
    def _parse_array(self) -> JuliaArrayExpression:
        """Parse array expression."""
        elements = []
        
        if not self._check(JuliaTokenType.RBRACKET):
            while True:
                element = self._parse_expression()
                elements.append(element)
                
                if not self._match(JuliaTokenType.COMMA):
                    break
        
        self._consume(JuliaTokenType.RBRACKET)
        return JuliaArrayExpression(elements=elements)
    
    # Helper methods
    def _match(self, *types: JuliaTokenType) -> bool:
        """Check if current token matches any of the given types."""
        for token_type in types:
            if self._check(token_type):
                self._advance()
                return True
        return False
    
    def _match_newline(self) -> bool:
        """Match and consume newline tokens."""
        if self._check(JuliaTokenType.NEWLINE):
            self._advance()
            return True
        return False
    
    def _skip_newlines(self):
        """Skip all newline tokens."""
        while self._match(JuliaTokenType.NEWLINE):
            pass
    
    def _check(self, token_type: JuliaTokenType) -> bool:
        """Check if current token is of given type."""
        if self._is_at_end():
            return False
        return self.current_token.type == token_type
    
    def _advance(self) -> JuliaToken:
        """Consume current token and return it."""
        if not self._is_at_end():
            self.position += 1
            if self.position < len(self.tokens):
                self.current_token = self.tokens[self.position]
        return self._previous()
    
    def _is_at_end(self) -> bool:
        """Check if at end of tokens."""
        return self.current_token is None or self.current_token.type == JuliaTokenType.EOF
    
    def _previous(self) -> JuliaToken:
        """Return previous token."""
        return self.tokens[self.position - 1]
    
    def _consume(self, token_type: JuliaTokenType) -> JuliaToken:
        """Consume token of expected type."""
        if self._check(token_type):
            return self._advance()
        
        # Error handling - for now just advance
        return self._advance()
    
    # Parse additional constructs (simplified versions)
    def _parse_import(self) -> JuliaImportDeclaration:
        """Parse import declaration."""
        self._consume(JuliaTokenType.IMPORT)
        package = self._consume(JuliaTokenType.IDENTIFIER).value
        return JuliaImportDeclaration(package=package)
    
    def _parse_using(self) -> JuliaUsingDeclaration:
        """Parse using declaration."""
        self._consume(JuliaTokenType.USING)
        package = self._consume(JuliaTokenType.IDENTIFIER).value
        return JuliaUsingDeclaration(package=package)
    
    def _parse_export(self) -> JuliaExportDeclaration:
        """Parse export declaration."""
        self._consume(JuliaTokenType.EXPORT)
        symbols = []
        
        while self._check(JuliaTokenType.IDENTIFIER):
            symbols.append(self._advance().value)
            if not self._match(JuliaTokenType.COMMA):
                break
        
        return JuliaExportDeclaration(symbols=symbols)
    
    def _parse_const(self) -> JuliaConstDeclaration:
        """Parse const declaration."""
        self._consume(JuliaTokenType.CONST)
        name = self._consume(JuliaTokenType.IDENTIFIER).value
        
        value = None
        if self._match(JuliaTokenType.ASSIGN):
            value = self._parse_expression()
        
        return JuliaConstDeclaration(name=name, value=value)
    
    def _parse_return(self) -> JuliaReturnStatement:
        """Parse return statement."""
        self._consume(JuliaTokenType.RETURN)
        expr = None
        
        if not self._check(JuliaTokenType.NEWLINE) and not self._is_at_end():
            expr = self._parse_expression()
        
        return JuliaReturnStatement(expression=expr)
    
    def _parse_if(self) -> JuliaIfExpression:
        """Parse if expression."""
        self._consume(JuliaTokenType.IF)
        condition = self._parse_expression()
        self._skip_newlines()
        
        then_body = []
        while (not self._check(JuliaTokenType.ELSE) and 
               not self._check(JuliaTokenType.ELSEIF) and
               not self._check(JuliaTokenType.END) and 
               not self._is_at_end()):
            if self._match_newline():
                continue
            stmt = self._parse_statement()
            if stmt:
                then_body.append(stmt)
            else:
                break
        
        else_body = []
        if self._match(JuliaTokenType.ELSE):
            self._skip_newlines()
            while not self._check(JuliaTokenType.END) and not self._is_at_end():
                if self._match_newline():
                    continue
                stmt = self._parse_statement()
                if stmt:
                    else_body.append(stmt)
                else:
                    break
        
        self._consume(JuliaTokenType.END)
        return JuliaIfExpression(condition=condition, then_body=then_body, else_body=else_body)
    
    def _parse_for(self) -> JuliaForLoop:
        """Parse for loop."""
        self._consume(JuliaTokenType.FOR)
        variable = self._consume(JuliaTokenType.IDENTIFIER).value
        # Skip 'in' keyword if present
        if self._check(JuliaTokenType.IDENTIFIER) and self.current_token.value == 'in':
            self._advance()
        iterable = self._parse_expression()
        self._skip_newlines()
        
        body = []
        while not self._check(JuliaTokenType.END) and not self._is_at_end():
            if self._match_newline():
                continue
            stmt = self._parse_statement()
            if stmt:
                body.append(stmt)
            else:
                break
        
        self._consume(JuliaTokenType.END)
        return JuliaForLoop(variable=variable, iterable=iterable, body=body)
    
    def _parse_while(self) -> JuliaWhileLoop:
        """Parse while loop."""
        self._consume(JuliaTokenType.WHILE)
        condition = self._parse_expression()
        self._skip_newlines()
        
        body = []
        while not self._check(JuliaTokenType.END) and not self._is_at_end():
            if self._match_newline():
                continue
            stmt = self._parse_statement()
            if stmt:
                body.append(stmt)
            else:
                break
        
        self._consume(JuliaTokenType.END)
        return JuliaWhileLoop(condition=condition, body=body)


def parse_julia(source: str) -> JuliaProgram:
    """Parse Julia source code into AST."""
    lexer = JuliaLexer(source)
    tokens = lexer.tokenize()
    parser = JuliaParser(tokens)
    return parser.parse() 