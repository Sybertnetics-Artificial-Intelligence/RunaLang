#!/usr/bin/env python3
"""
AssemblyScript Parser and Lexer

Comprehensive AssemblyScript parsing implementation supporting TypeScript-like
syntax with AssemblyScript-specific extensions.

Author: Sybertnetics AI Solutions
License: MIT
"""

import re
from typing import List, Optional, Dict, Any, Union, Tuple
from dataclasses import dataclass
from enum import Enum, auto
import logging

from .assemblyscript_ast import *


class AsTokenType(Enum):
    """AssemblyScript token types."""
    # Literals
    NUMBER = auto()
    STRING = auto()
    BOOLEAN = auto()
    NULL = auto()
    
    # Identifiers and keywords
    IDENTIFIER = auto()
    KEYWORD = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    ASSIGN = auto()
    EQUALS = auto()
    NOT_EQUALS = auto()
    LESS_THAN = auto()
    GREATER_THAN = auto()
    LESS_EQUALS = auto()
    GREATER_EQUALS = auto()
    LOGICAL_AND = auto()
    LOGICAL_OR = auto()
    LOGICAL_NOT = auto()
    BITWISE_AND = auto()
    BITWISE_OR = auto()
    BITWISE_XOR = auto()
    BITWISE_NOT = auto()
    LEFT_SHIFT = auto()
    RIGHT_SHIFT = auto()
    INCREMENT = auto()
    DECREMENT = auto()
    
    # Punctuation
    SEMICOLON = auto()
    COMMA = auto()
    DOT = auto()
    COLON = auto()
    QUESTION = auto()
    
    # Brackets
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()
    
    # Special
    NEWLINE = auto()
    EOF = auto()
    COMMENT = auto()


@dataclass
class AsToken:
    """AssemblyScript token."""
    type: AsTokenType
    value: str
    line: int
    column: int


class AsLexer:
    """AssemblyScript lexer for tokenizing source code."""
    
    KEYWORDS = {
        'abstract', 'as', 'break', 'case', 'catch', 'class', 'const', 'continue',
        'declare', 'default', 'delete', 'do', 'else', 'enum', 'export', 'extends',
        'false', 'finally', 'for', 'function', 'if', 'implements', 'import', 'in',
        'instanceof', 'interface', 'let', 'new', 'null', 'package', 'private',
        'protected', 'public', 'return', 'static', 'super', 'switch', 'this',
        'throw', 'true', 'try', 'typeof', 'var', 'void', 'while', 'with', 'yield',
        'async', 'await', 'readonly', 'namespace', 'module', 'type', 'from',
        'operator', 'inline', 'get', 'set', 'constructor'
    }
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reset lexer state."""
        self.tokens = []
        self.current_line = 1
        self.current_column = 1
        self.pos = 0
        self.text = ""
    
    def tokenize(self, text: str) -> List[AsToken]:
        """Tokenize AssemblyScript source code."""
        self.reset()
        self.text = text
        
        while self.pos < len(self.text):
            self._skip_whitespace()
            
            if self.pos >= len(self.text):
                break
            
            char = self._peek()
            
            # Comments
            if char == '/' and self._peek(1) == '/':
                self._skip_line_comment()
            elif char == '/' and self._peek(1) == '*':
                self._skip_block_comment()
            # String literals
            elif char in ('"', "'", '`'):
                self._tokenize_string()
            # Number literals
            elif char.isdigit() or (char == '.' and self._peek(1).isdigit()):
                self._tokenize_number()
            # Identifiers and keywords
            elif char.isalpha() or char == '_' or char == '$':
                self._tokenize_identifier()
            # Two-character operators
            elif self._match_two_char_operator():
                pass  # Already handled in method
            # Single-character tokens
            else:
                self._tokenize_single_char()
        
        self._add_token(AsTokenType.EOF, '')
        return self.tokens
    
    def _peek(self, offset: int = 0) -> str:
        """Peek at character at current position + offset."""
        pos = self.pos + offset
        return self.text[pos] if pos < len(self.text) else ''
    
    def _advance(self) -> str:
        """Advance position and return current character."""
        if self.pos < len(self.text):
            char = self.text[self.pos]
            self.pos += 1
            if char == '\n':
                self.current_line += 1
                self.current_column = 1
            else:
                self.current_column += 1
            return char
        return ''
    
    def _skip_whitespace(self):
        """Skip whitespace characters except newlines."""
        while self.pos < len(self.text) and self.text[self.pos] in ' \t\r':
            self._advance()
    
    def _skip_line_comment(self):
        """Skip single-line comment."""
        while self.pos < len(self.text) and self._peek() != '\n':
            self._advance()
    
    def _skip_block_comment(self):
        """Skip block comment."""
        self._advance()  # Skip /
        self._advance()  # Skip *
        
        while self.pos < len(self.text):
            if self._peek() == '*' and self._peek(1) == '/':
                self._advance()  # Skip *
                self._advance()  # Skip /
                break
            self._advance()
    
    def _tokenize_string(self):
        """Tokenize string literal."""
        quote_char = self._advance()
        value = ""
        
        while self.pos < len(self.text):
            char = self._peek()
            if char == quote_char:
                self._advance()
                break
            elif char == '\\':
                self._advance()  # Skip backslash
                escaped = self._advance()
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
            else:
                value += self._advance()
        
        self._add_token(AsTokenType.STRING, value)
    
    def _tokenize_number(self):
        """Tokenize number literal."""
        value = ""
        
        # Handle decimal numbers
        while self.pos < len(self.text) and (self._peek().isdigit() or self._peek() == '.'):
            value += self._advance()
        
        # Handle scientific notation
        if self.pos < len(self.text) and self._peek().lower() == 'e':
            value += self._advance()
            if self.pos < len(self.text) and self._peek() in '+-':
                value += self._advance()
            while self.pos < len(self.text) and self._peek().isdigit():
                value += self._advance()
        
        # Handle type suffixes (f, d, L, etc.)
        if self.pos < len(self.text) and self._peek().lower() in 'fld':
            value += self._advance()
        
        self._add_token(AsTokenType.NUMBER, value)
    
    def _tokenize_identifier(self):
        """Tokenize identifier or keyword."""
        value = ""
        
        while self.pos < len(self.text) and (self._peek().isalnum() or self._peek() in '_$'):
            value += self._advance()
        
        # Check if it's a keyword
        if value in self.KEYWORDS:
            token_type = AsTokenType.KEYWORD
        elif value in ('true', 'false'):
            token_type = AsTokenType.BOOLEAN
        elif value == 'null':
            token_type = AsTokenType.NULL
        else:
            token_type = AsTokenType.IDENTIFIER
        
        self._add_token(token_type, value)
    
    def _match_two_char_operator(self) -> bool:
        """Check and tokenize two-character operators."""
        char1 = self._peek()
        char2 = self._peek(1)
        two_char = char1 + char2
        
        operators = {
            '==': AsTokenType.EQUALS,
            '!=': AsTokenType.NOT_EQUALS,
            '<=': AsTokenType.LESS_EQUALS,
            '>=': AsTokenType.GREATER_EQUALS,
            '&&': AsTokenType.LOGICAL_AND,
            '||': AsTokenType.LOGICAL_OR,
            '<<': AsTokenType.LEFT_SHIFT,
            '>>': AsTokenType.RIGHT_SHIFT,
            '++': AsTokenType.INCREMENT,
            '--': AsTokenType.DECREMENT,
        }
        
        if two_char in operators:
            self._advance()
            self._advance()
            self._add_token(operators[two_char], two_char)
            return True
        
        return False
    
    def _tokenize_single_char(self):
        """Tokenize single character tokens."""
        char = self._advance()
        
        single_char_tokens = {
            '+': AsTokenType.PLUS,
            '-': AsTokenType.MINUS,
            '*': AsTokenType.MULTIPLY,
            '/': AsTokenType.DIVIDE,
            '%': AsTokenType.MODULO,
            '=': AsTokenType.ASSIGN,
            '<': AsTokenType.LESS_THAN,
            '>': AsTokenType.GREATER_THAN,
            '!': AsTokenType.LOGICAL_NOT,
            '&': AsTokenType.BITWISE_AND,
            '|': AsTokenType.BITWISE_OR,
            '^': AsTokenType.BITWISE_XOR,
            '~': AsTokenType.BITWISE_NOT,
            ';': AsTokenType.SEMICOLON,
            ',': AsTokenType.COMMA,
            '.': AsTokenType.DOT,
            ':': AsTokenType.COLON,
            '?': AsTokenType.QUESTION,
            '(': AsTokenType.LEFT_PAREN,
            ')': AsTokenType.RIGHT_PAREN,
            '{': AsTokenType.LEFT_BRACE,
            '}': AsTokenType.RIGHT_BRACE,
            '[': AsTokenType.LEFT_BRACKET,
            ']': AsTokenType.RIGHT_BRACKET,
            '\n': AsTokenType.NEWLINE,
        }
        
        if char in single_char_tokens:
            self._add_token(single_char_tokens[char], char)
        else:
            # Unknown character - skip it
            pass
    
    def _add_token(self, token_type: AsTokenType, value: str):
        """Add token to list."""
        self.tokens.append(AsToken(
            type=token_type,
            value=value,
            line=self.current_line,
            column=self.current_column
        ))


class AsParser:
    """AssemblyScript parser."""
    
    def __init__(self):
        self.tokens = []
        self.pos = 0
        self.logger = logging.getLogger(__name__)
    
    def parse(self, text: str) -> AsProgram:
        """Parse AssemblyScript source code into AST."""
        try:
            lexer = AsLexer()
            self.tokens = lexer.tokenize(text)
            self.pos = 0
            
            return self._parse_program()
            
        except Exception as e:
            self.logger.error(f"AssemblyScript parsing failed: {e}")
            raise RuntimeError(f"Failed to parse AssemblyScript: {e}")
    
    def _current_token(self) -> AsToken:
        """Get current token."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return AsToken(AsTokenType.EOF, '', 0, 0)
    
    def _advance(self) -> AsToken:
        """Advance to next token."""
        token = self._current_token()
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return token
    
    def _match(self, *types: AsTokenType) -> bool:
        """Check if current token matches any of the given types."""
        return self._current_token().type in types
    
    def _match_keyword(self, keyword: str) -> bool:
        """Check if current token is a specific keyword."""
        token = self._current_token()
        return token.type == AsTokenType.KEYWORD and token.value == keyword
    
    def _is_at_end(self) -> bool:
        """Check if at end of tokens."""
        return self._match(AsTokenType.EOF)
    
    def _consume(self, token_type: AsTokenType, message: str = "") -> AsToken:
        """Consume token of expected type or raise error."""
        if self._match(token_type):
            return self._advance()
        
        current = self._current_token()
        raise RuntimeError(f"Expected {token_type}, got {current.type} at line {current.line}: {message}")
    
    def _skip_newlines(self):
        """Skip newline tokens."""
        while self._match(AsTokenType.NEWLINE):
            self._advance()
    
    def _parse_program(self) -> AsProgram:
        """Parse top-level program."""
        statements = []
        imports = []
        exports = []
        
        self._skip_newlines()
        
        while not self._is_at_end():
            self._skip_newlines()
            
            if self._is_at_end():
                break
            
            if self._match_keyword('import'):
                imports.append(self._parse_import())
            elif self._match_keyword('export'):
                exports.append(self._parse_export())
            else:
                stmt = self._parse_statement()
                if stmt:
                    statements.append(stmt)
            
            self._skip_newlines()
        
        return AsProgram(statements=statements, imports=imports, exports=exports)
    
    def _parse_import(self) -> AsImport:
        """Parse import statement."""
        self._advance()  # consume 'import'
        
        specifiers = []
        source = ""
        
        # Parse import specifiers (simplified)
        if self._match(AsTokenType.IDENTIFIER):
            # Default import or named import
            name = self._advance().value
            specifiers.append(AsImportSpecifier(imported=name))
        
        if self._match_keyword('from'):
            self._advance()
            if self._match(AsTokenType.STRING):
                source = self._advance().value
        
        self._optional_semicolon()
        
        return AsImport(source=source, specifiers=specifiers)
    
    def _parse_export(self) -> AsExport:
        """Parse export statement."""
        self._advance()  # consume 'export'
        
        if self._match_keyword('default'):
            self._advance()
            # Export default (simplified)
            return AsExport(export_type="default")
        else:
            # Parse exported declaration
            declaration = self._parse_statement()
            return AsExport(declaration=declaration)
    
    def _parse_statement(self) -> Optional[AsStatement]:
        """Parse statement."""
        if self._match_keyword('function'):
            return self._parse_function()
        elif self._match_keyword('class'):
            return self._parse_class()
        elif self._match_keyword('interface'):
            return self._parse_interface()
        elif self._match_keyword('let') or self._match_keyword('const') or self._match_keyword('var'):
            return self._parse_variable_declaration()
        elif self._match_keyword('if'):
            return self._parse_if_statement()
        elif self._match_keyword('while'):
            return self._parse_while_statement()
        elif self._match_keyword('for'):
            return self._parse_for_statement()
        elif self._match_keyword('return'):
            return self._parse_return_statement()
        elif self._match(AsTokenType.LEFT_BRACE):
            return self._parse_block()
        else:
            # Expression statement
            expr = self._parse_expression()
            self._optional_semicolon()
            return AsExpressionStatement(expression=expr)
    
    def _parse_function(self) -> AsFunction:
        """Parse function declaration."""
        self._advance()  # consume 'function'
        
        name = ""
        if self._match(AsTokenType.IDENTIFIER):
            name = self._advance().value
        
        self._consume(AsTokenType.LEFT_PAREN)
        parameters = self._parse_parameter_list()
        self._consume(AsTokenType.RIGHT_PAREN)
        
        return_type = None
        if self._match(AsTokenType.COLON):
            self._advance()
            return_type = self._parse_type()
        
        body = []
        if self._match(AsTokenType.LEFT_BRACE):
            block = self._parse_block()
            body = block.statements if isinstance(block, AsBlock) else []
        
        return AsFunction(name=name, parameters=parameters, return_type=return_type, body=body)
    
    def _parse_class(self) -> AsClass:
        """Parse class declaration."""
        self._advance()  # consume 'class'
        
        name = ""
        if self._match(AsTokenType.IDENTIFIER):
            name = self._advance().value
        
        super_class = None
        if self._match_keyword('extends'):
            self._advance()
            if self._match(AsTokenType.IDENTIFIER):
                super_class = self._advance().value
        
        members = []
        if self._match(AsTokenType.LEFT_BRACE):
            self._advance()
            self._skip_newlines()
            
            while not self._match(AsTokenType.RIGHT_BRACE) and not self._is_at_end():
                # Simplified member parsing
                member_name = ""
                if self._match(AsTokenType.IDENTIFIER):
                    member_name = self._advance().value
                
                if self._match(AsTokenType.LEFT_PAREN):
                    # Method
                    method = AsFunction(name=member_name)
                    member = AsClassMember(name=member_name, member_type="method", method=method)
                    members.append(member)
                    
                    # Skip method body for now
                    paren_count = 1
                    self._advance()  # consume (
                    while paren_count > 0 and not self._is_at_end():
                        if self._match(AsTokenType.LEFT_PAREN):
                            paren_count += 1
                        elif self._match(AsTokenType.RIGHT_PAREN):
                            paren_count -= 1
                        self._advance()
                else:
                    # Field
                    field_type = None
                    if self._match(AsTokenType.COLON):
                        self._advance()
                        field_type = self._parse_type()
                    
                    member = AsClassMember(name=member_name, member_type="field", field_type=field_type)
                    members.append(member)
                
                self._optional_semicolon()
                self._skip_newlines()
            
            if self._match(AsTokenType.RIGHT_BRACE):
                self._advance()
        
        return AsClass(name=name, super_class=super_class, members=members)
    
    def _parse_interface(self) -> AsInterface:
        """Parse interface declaration."""
        self._advance()  # consume 'interface'
        
        name = ""
        if self._match(AsTokenType.IDENTIFIER):
            name = self._advance().value
        
        members = []
        if self._match(AsTokenType.LEFT_BRACE):
            self._advance()
            # Simplified interface member parsing
            while not self._match(AsTokenType.RIGHT_BRACE) and not self._is_at_end():
                if self._match(AsTokenType.IDENTIFIER):
                    member_name = self._advance().value
                    member = AsInterfaceMember(name=member_name, member_type="property")
                    members.append(member)
                
                self._optional_semicolon()
                self._skip_newlines()
            
            if self._match(AsTokenType.RIGHT_BRACE):
                self._advance()
        
        return AsInterface(name=name, members=members)
    
    def _parse_variable_declaration(self) -> AsVariableDeclaration:
        """Parse variable declaration."""
        keyword = self._advance().value  # let, const, or var
        
        name = ""
        if self._match(AsTokenType.IDENTIFIER):
            name = self._advance().value
        
        var_type = None
        if self._match(AsTokenType.COLON):
            self._advance()
            var_type = self._parse_type()
        
        initial_value = None
        if self._match(AsTokenType.ASSIGN):
            self._advance()
            initial_value = self._parse_expression()
        
        self._optional_semicolon()
        
        return AsVariableDeclaration(
            name=name,
            var_type=var_type,
            initial_value=initial_value,
            is_const=(keyword == 'const'),
            is_let=(keyword == 'let')
        )
    
    def _parse_parameter_list(self) -> List[AsParameter]:
        """Parse function parameter list."""
        parameters = []
        
        while not self._match(AsTokenType.RIGHT_PAREN) and not self._is_at_end():
            if self._match(AsTokenType.IDENTIFIER):
                name = self._advance().value
                
                param_type = create_as_type("any")  # Default type
                if self._match(AsTokenType.COLON):
                    self._advance()
                    param_type = self._parse_type()
                
                parameters.append(AsParameter(name=name, param_type=param_type))
            
            if self._match(AsTokenType.COMMA):
                self._advance()
            else:
                break
        
        return parameters
    
    def _parse_type(self) -> AsType:
        """Parse type annotation."""
        if self._match(AsTokenType.IDENTIFIER):
            type_name = self._advance().value
            
            # Handle generic types (simplified)
            generic_args = []
            if self._match(AsTokenType.LESS_THAN):
                self._advance()
                while not self._match(AsTokenType.GREATER_THAN) and not self._is_at_end():
                    generic_args.append(self._parse_type())
                    if self._match(AsTokenType.COMMA):
                        self._advance()
                    else:
                        break
                
                if self._match(AsTokenType.GREATER_THAN):
                    self._advance()
            
            # Handle array types
            is_array = False
            if self._match(AsTokenType.LEFT_BRACKET):
                self._advance()
                if self._match(AsTokenType.RIGHT_BRACKET):
                    self._advance()
                    is_array = True
            
            return AsType(name=type_name, generic_args=generic_args, is_array=is_array)
        
        return create_as_type("unknown")
    
    def _parse_if_statement(self) -> AsIfStatement:
        """Parse if statement."""
        self._advance()  # consume 'if'
        
        self._consume(AsTokenType.LEFT_PAREN)
        condition = self._parse_expression()
        self._consume(AsTokenType.RIGHT_PAREN)
        
        then_statement = self._parse_statement()
        
        else_statement = None
        if self._match_keyword('else'):
            self._advance()
            else_statement = self._parse_statement()
        
        return AsIfStatement(condition=condition, then_statement=then_statement, else_statement=else_statement)
    
    def _parse_while_statement(self) -> AsWhileStatement:
        """Parse while statement."""
        self._advance()  # consume 'while'
        
        self._consume(AsTokenType.LEFT_PAREN)
        condition = self._parse_expression()
        self._consume(AsTokenType.RIGHT_PAREN)
        
        body = self._parse_statement()
        
        return AsWhileStatement(condition=condition, body=body)
    
    def _parse_for_statement(self) -> AsForStatement:
        """Parse for statement."""
        self._advance()  # consume 'for'
        
        self._consume(AsTokenType.LEFT_PAREN)
        
        init = None
        if not self._match(AsTokenType.SEMICOLON):
            init = self._parse_statement()
        else:
            self._advance()  # consume semicolon
        
        condition = None
        if not self._match(AsTokenType.SEMICOLON):
            condition = self._parse_expression()
        self._consume(AsTokenType.SEMICOLON)
        
        update = None
        if not self._match(AsTokenType.RIGHT_PAREN):
            update = self._parse_expression()
        self._consume(AsTokenType.RIGHT_PAREN)
        
        body = self._parse_statement()
        
        return AsForStatement(init=init, condition=condition, update=update, body=body)
    
    def _parse_return_statement(self) -> AsReturnStatement:
        """Parse return statement."""
        self._advance()  # consume 'return'
        
        value = None
        if not self._match(AsTokenType.SEMICOLON) and not self._match(AsTokenType.NEWLINE):
            value = self._parse_expression()
        
        self._optional_semicolon()
        
        return AsReturnStatement(value=value)
    
    def _parse_block(self) -> AsBlock:
        """Parse block statement."""
        self._consume(AsTokenType.LEFT_BRACE)
        
        statements = []
        self._skip_newlines()
        
        while not self._match(AsTokenType.RIGHT_BRACE) and not self._is_at_end():
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
            self._skip_newlines()
        
        self._consume(AsTokenType.RIGHT_BRACE)
        
        return AsBlock(statements=statements)
    
    def _parse_expression(self) -> AsExpression:
        """Parse expression (simplified)."""
        return self._parse_logical_or()
    
    def _parse_logical_or(self) -> AsExpression:
        """Parse logical OR expression."""
        expr = self._parse_logical_and()
        
        while self._match(AsTokenType.LOGICAL_OR):
            operator = self._advance().value
            right = self._parse_logical_and()
            expr = AsBinaryExpression(left=expr, operator=operator, right=right)
        
        return expr
    
    def _parse_logical_and(self) -> AsExpression:
        """Parse logical AND expression."""
        expr = self._parse_equality()
        
        while self._match(AsTokenType.LOGICAL_AND):
            operator = self._advance().value
            right = self._parse_equality()
            expr = AsBinaryExpression(left=expr, operator=operator, right=right)
        
        return expr
    
    def _parse_equality(self) -> AsExpression:
        """Parse equality expression."""
        expr = self._parse_comparison()
        
        while self._match(AsTokenType.EQUALS, AsTokenType.NOT_EQUALS):
            operator = self._advance().value
            right = self._parse_comparison()
            expr = AsBinaryExpression(left=expr, operator=operator, right=right)
        
        return expr
    
    def _parse_comparison(self) -> AsExpression:
        """Parse comparison expression."""
        expr = self._parse_addition()
        
        while self._match(AsTokenType.LESS_THAN, AsTokenType.GREATER_THAN, 
                          AsTokenType.LESS_EQUALS, AsTokenType.GREATER_EQUALS):
            operator = self._advance().value
            right = self._parse_addition()
            expr = AsBinaryExpression(left=expr, operator=operator, right=right)
        
        return expr
    
    def _parse_addition(self) -> AsExpression:
        """Parse addition/subtraction expression."""
        expr = self._parse_multiplication()
        
        while self._match(AsTokenType.PLUS, AsTokenType.MINUS):
            operator = self._advance().value
            right = self._parse_multiplication()
            expr = AsBinaryExpression(left=expr, operator=operator, right=right)
        
        return expr
    
    def _parse_multiplication(self) -> AsExpression:
        """Parse multiplication/division expression."""
        expr = self._parse_unary()
        
        while self._match(AsTokenType.MULTIPLY, AsTokenType.DIVIDE, AsTokenType.MODULO):
            operator = self._advance().value
            right = self._parse_unary()
            expr = AsBinaryExpression(left=expr, operator=operator, right=right)
        
        return expr
    
    def _parse_unary(self) -> AsExpression:
        """Parse unary expression."""
        if self._match(AsTokenType.LOGICAL_NOT, AsTokenType.MINUS, AsTokenType.PLUS):
            operator = self._advance().value
            operand = self._parse_unary()
            return AsUnaryExpression(operator=operator, operand=operand)
        
        return self._parse_postfix()
    
    def _parse_postfix(self) -> AsExpression:
        """Parse postfix expression."""
        expr = self._parse_primary()
        
        while True:
            if self._match(AsTokenType.LEFT_PAREN):
                # Function call
                self._advance()
                arguments = []
                
                while not self._match(AsTokenType.RIGHT_PAREN) and not self._is_at_end():
                    arguments.append(self._parse_expression())
                    if self._match(AsTokenType.COMMA):
                        self._advance()
                    else:
                        break
                
                self._consume(AsTokenType.RIGHT_PAREN)
                expr = AsCallExpression(function=expr, arguments=arguments)
            
            elif self._match(AsTokenType.DOT):
                # Member access
                self._advance()
                if self._match(AsTokenType.IDENTIFIER):
                    property_name = self._advance().value
                    property_expr = AsIdentifier(name=property_name)
                    expr = AsMemberExpression(object=expr, property=property_expr, computed=False)
                else:
                    break
            
            elif self._match(AsTokenType.LEFT_BRACKET):
                # Computed member access
                self._advance()
                property_expr = self._parse_expression()
                self._consume(AsTokenType.RIGHT_BRACKET)
                expr = AsMemberExpression(object=expr, property=property_expr, computed=True)
            
            else:
                break
        
        return expr
    
    def _parse_primary(self) -> AsExpression:
        """Parse primary expression."""
        if self._match(AsTokenType.NUMBER):
            value = self._advance().value
            try:
                if '.' in value:
                    return AsLiteral(value=float(value), literal_type="number")
                else:
                    return AsLiteral(value=int(value), literal_type="number")
            except ValueError:
                return AsLiteral(value=value, literal_type="number")
        
        if self._match(AsTokenType.STRING):
            value = self._advance().value
            return AsLiteral(value=value, literal_type="string")
        
        if self._match(AsTokenType.BOOLEAN):
            value = self._advance().value
            return AsLiteral(value=(value == "true"), literal_type="boolean")
        
        if self._match(AsTokenType.NULL):
            self._advance()
            return AsLiteral(value=None, literal_type="null")
        
        if self._match(AsTokenType.IDENTIFIER):
            name = self._advance().value
            return AsIdentifier(name=name)
        
        if self._match(AsTokenType.LEFT_PAREN):
            self._advance()
            expr = self._parse_expression()
            self._consume(AsTokenType.RIGHT_PAREN)
            return expr
        
        # Default: create identifier with empty name
        return AsIdentifier(name="unknown")
    
    def _optional_semicolon(self):
        """Optionally consume semicolon."""
        if self._match(AsTokenType.SEMICOLON):
            self._advance()


# Convenience functions
def parse_assemblyscript(text: str) -> AsProgram:
    """Parse AssemblyScript source code into AST."""
    parser = AsParser()
    return parser.parse(text)


def parse_assemblyscript_file(file_path: str) -> AsProgram:
    """Parse AssemblyScript file into AST."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return parse_assemblyscript(f.read())


def validate_assemblyscript_syntax(text: str) -> Tuple[bool, Optional[str]]:
    """Validate AssemblyScript syntax."""
    try:
        parse_assemblyscript(text)
        return True, None
    except Exception as e:
        return False, str(e)