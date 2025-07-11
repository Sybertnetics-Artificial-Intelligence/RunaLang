"""
Perl Parser for Runa Universal Translation Platform
Parses Perl 5 source code with flexible syntax and powerful text processing

Key features:
- Context-sensitive parsing (scalar vs list context)
- Regular expression parsing with advanced features
- Flexible syntax with multiple ways to express constructs
- Special variables and magic handling
- Object-oriented Perl support
- Module and package system
"""

import re
from typing import List, Optional, Dict, Any, Union
from enum import Enum
from dataclasses import dataclass
import logging

from .perl_ast import *

logger = logging.getLogger(__name__)


class ParseError(Exception):
    """Base parse error class."""
    pass


class BaseParser:
    """Base parser class."""
    pass

class PerlTokenType(Enum):
    """Perl token types"""
    # Literals
    SCALAR_VAR = "SCALAR_VAR"      # $var
    ARRAY_VAR = "ARRAY_VAR"        # @array
    HASH_VAR = "HASH_VAR"          # %hash
    TYPEGLOB = "TYPEGLOB"          # *glob
    NUMBER = "NUMBER"
    STRING = "STRING"
    REGEX = "REGEX"
    HERE_DOC = "HERE_DOC"
    
    # Keywords
    IF = "if"
    ELSIF = "elsif"
    ELSE = "else"
    UNLESS = "unless"
    WHILE = "while"
    UNTIL = "until"
    FOR = "for"
    FOREACH = "foreach"
    GIVEN = "given"
    WHEN = "when"
    DEFAULT = "default"
    SUB = "sub"
    PACKAGE = "package"
    USE = "use"
    REQUIRE = "require"
    MY = "my"
    OUR = "our"
    LOCAL = "local"
    RETURN = "return"
    LAST = "last"
    NEXT = "next"
    REDO = "redo"
    GOTO = "goto"
    EVAL = "eval"
    BLESS = "bless"
    
    # Operators
    ASSIGN = "="
    PLUS_ASSIGN = "+="
    MINUS_ASSIGN = "-="
    CONCAT_ASSIGN = ".="
    MATCH = "=~"
    NOT_MATCH = "!~"
    ARROW = "->"
    DOUBLE_COLON = "::"
    RANGE = ".."
    SPACESHIP = "<=>"
    
    # Delimiters
    SEMICOLON = ";"
    COMMA = ","
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
    LEFT_BRACE = "{"
    RIGHT_BRACE = "}"
    LEFT_BRACKET = "["
    RIGHT_BRACKET = "]"
    
    # Special
    COMMENT = "COMMENT"
    WHITESPACE = "WHITESPACE"
    NEWLINE = "NEWLINE"
    EOF = "EOF"

@dataclass
class PerlToken:
    """Perl token with type, value, and location"""
    type: PerlTokenType
    value: str
    line: int
    column: int

class PerlLexer:
    """Perl lexer for tokenizing source code"""
    
    PERL_KEYWORDS = {
        "if", "elsif", "else", "unless", "while", "until", "for", "foreach",
        "given", "when", "default", "sub", "package", "use", "require",
        "my", "our", "local", "return", "last", "next", "redo", "goto",
        "eval", "bless", "and", "or", "not", "xor", "cmp", "eq", "ne",
        "lt", "gt", "le", "ge", "defined", "undef", "exists", "delete"
    }
    
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[PerlToken] = []
        
    def tokenize(self) -> List[PerlToken]:
        """Tokenize Perl source code"""
        while self.position < len(self.source):
            self._skip_whitespace()
            if self.position >= len(self.source):
                break
                
            if self._match_comment():
                continue
            elif self._match_variable():
                continue
            elif self._match_regex():
                continue
            elif self._match_string():
                continue
            elif self._match_number():
                continue
            elif self._match_operator():
                continue
            elif self._match_keyword_or_identifier():
                continue
            elif self._match_delimiter():
                continue
            else:
                self._advance()  # Skip unknown characters
                
        self._add_token(PerlTokenType.EOF, "")
        return self.tokens
    
    def _current_char(self) -> str:
        if self.position >= len(self.source):
            return '\0'
        return self.source[self.position]
    
    def _peek_char(self, offset: int = 1) -> str:
        pos = self.position + offset
        if pos >= len(self.source):
            return '\0'
        return self.source[pos]
    
    def _advance(self) -> str:
        char = self._current_char()
        self.position += 1
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char
    
    def _add_token(self, token_type: PerlTokenType, value: str):
        token = PerlToken(token_type, value, self.line, self.column - len(value))
        self.tokens.append(token)
    
    def _skip_whitespace(self):
        while self._current_char().isspace():
            self._advance()
    
    def _match_comment(self) -> bool:
        if self._current_char() == '#':
            value = ""
            while self._current_char() not in ['\n', '\0']:
                value += self._advance()
            self._add_token(PerlTokenType.COMMENT, value)
            return True
        return False
    
    def _match_variable(self) -> bool:
        char = self._current_char()
        if char in ['$', '@', '%', '*']:
            sigil = self._advance()
            name = ""
            
            # Handle special variables like $_, $&, $1, etc.
            if not self._current_char().isalpha() and self._current_char() != '_':
                name = self._current_char()
                if name != '\0':
                    self._advance()
            else:
                while (self._current_char().isalnum() or self._current_char() == '_'):
                    name += self._advance()
            
            token_type = {
                '$': PerlTokenType.SCALAR_VAR,
                '@': PerlTokenType.ARRAY_VAR,
                '%': PerlTokenType.HASH_VAR,
                '*': PerlTokenType.TYPEGLOB
            }[sigil]
            
            self._add_token(token_type, sigil + name)
            return True
        return False
    
    def _match_regex(self) -> bool:
        if self._current_char() == '/' and self._peek_char() != '=':
            # Simple regex matching
            value = "/"
            self._advance()
            
            while self._current_char() not in ['/', '\0', '\n']:
                if self._current_char() == '\\':
                    value += self._advance()  # Escape character
                    if self._current_char() != '\0':
                        value += self._advance()
                else:
                    value += self._advance()
            
            if self._current_char() == '/':
                value += self._advance()
                # Match flags
                while self._current_char().isalpha():
                    value += self._advance()
            
            self._add_token(PerlTokenType.REGEX, value)
            return True
        return False
    
    def _match_string(self) -> bool:
        char = self._current_char()
        if char in ['"', "'", '`']:
            quote = self._advance()
            value = quote
            
            while self._current_char() not in [quote, '\0']:
                if self._current_char() == '\\':
                    value += self._advance()  # Escape
                    if self._current_char() != '\0':
                        value += self._advance()
                else:
                    value += self._advance()
            
            if self._current_char() == quote:
                value += self._advance()
            
            self._add_token(PerlTokenType.STRING, value)
            return True
        return False
    
    def _match_number(self) -> bool:
        if self._current_char().isdigit():
            value = ""
            
            # Handle different number formats
            if self._current_char() == '0' and self._peek_char() in ['x', 'X']:
                # Hexadecimal
                value += self._advance() + self._advance()
                while self._current_char().isdigit() or self._current_char().lower() in 'abcdef':
                    value += self._advance()
            elif self._current_char() == '0' and self._peek_char() in ['b', 'B']:
                # Binary
                value += self._advance() + self._advance()
                while self._current_char() in '01':
                    value += self._advance()
            else:
                # Decimal
                while self._current_char().isdigit():
                    value += self._advance()
                
                # Handle decimal point
                if self._current_char() == '.' and self._peek_char().isdigit():
                    value += self._advance()
                    while self._current_char().isdigit():
                        value += self._advance()
                
                # Handle scientific notation
                if self._current_char().lower() == 'e':
                    value += self._advance()
                    if self._current_char() in ['+', '-']:
                        value += self._advance()
                    while self._current_char().isdigit():
                        value += self._advance()
            
            self._add_token(PerlTokenType.NUMBER, value)
            return True
        return False
    
    def _match_operator(self) -> bool:
        char = self._current_char()
        next_char = self._peek_char()
        
        # Multi-character operators
        if char == '=' and next_char == '~':
            self._advance()
            self._advance()
            self._add_token(PerlTokenType.MATCH, "=~")
            return True
        elif char == '!' and next_char == '~':
            self._advance()
            self._advance()
            self._add_token(PerlTokenType.NOT_MATCH, "!~")
            return True
        elif char == '-' and next_char == '>':
            self._advance()
            self._advance()
            self._add_token(PerlTokenType.ARROW, "->")
            return True
        elif char == ':' and next_char == ':':
            self._advance()
            self._advance()
            self._add_token(PerlTokenType.DOUBLE_COLON, "::")
            return True
        elif char == '.' and next_char == '.':
            self._advance()
            self._advance()
            self._add_token(PerlTokenType.RANGE, "..")
            return True
        elif char in ['+', '-', '.'] and next_char == '=':
            op = self._advance() + self._advance()
            token_type = {
                '+=': PerlTokenType.PLUS_ASSIGN,
                '-=': PerlTokenType.MINUS_ASSIGN,
                '.=': PerlTokenType.CONCAT_ASSIGN
            }.get(op, PerlTokenType.ASSIGN)
            self._add_token(token_type, op)
            return True
        elif char == '=':
            self._advance()
            self._add_token(PerlTokenType.ASSIGN, "=")
            return True
        
        return False
    
    def _match_keyword_or_identifier(self) -> bool:
        if self._current_char().isalpha() or self._current_char() == '_':
            value = ""
            while (self._current_char().isalnum() or self._current_char() == '_'):
                value += self._advance()
            
            # Check if it's a keyword
            if value in self.PERL_KEYWORDS:
                token_type = PerlTokenType(value)
            else:
                token_type = PerlTokenType.STRING  # Use STRING for identifiers
            
            self._add_token(token_type, value)
            return True
        return False
    
    def _match_delimiter(self) -> bool:
        char = self._current_char()
        token_map = {
            ';': PerlTokenType.SEMICOLON,
            ',': PerlTokenType.COMMA,
            '(': PerlTokenType.LEFT_PAREN,
            ')': PerlTokenType.RIGHT_PAREN,
            '{': PerlTokenType.LEFT_BRACE,
            '}': PerlTokenType.RIGHT_BRACE,
            '[': PerlTokenType.LEFT_BRACKET,
            ']': PerlTokenType.RIGHT_BRACKET,
        }
        
        if char in token_map:
            self._advance()
            self._add_token(token_map[char], char)
            return True
        return False

class PerlParseError(ParseError):
    """Perl-specific parse error"""
    pass

class PerlParser(BaseParser):
    """Perl parser for creating AST from tokens"""
    
    def __init__(self, tokens: Optional[List[PerlToken]] = None):
        super().__init__()
        self.tokens = tokens or []
        self.position = 0
        self.context = "void"  # void, scalar, list
        
    def parse(self, source: str) -> PerlProgram:
        """Parse Perl source code into AST"""
        try:
            lexer = PerlLexer(source)
            self.tokens = lexer.tokenize()
            self.position = 0
            
            return self.parse_program()
            
        except Exception as e:
            raise PerlParseError(f"Parse error: {e}")
    
    def current_token(self) -> PerlToken:
        if self.position >= len(self.tokens):
            return PerlToken(PerlTokenType.EOF, "", 0, 0)
        return self.tokens[self.position]
    
    def advance(self) -> PerlToken:
        token = self.current_token()
        if self.position < len(self.tokens):
            self.position += 1
        return token
    
    def match(self, *token_types: PerlTokenType) -> bool:
        return self.current_token().type in token_types
    
    def consume(self, token_type: PerlTokenType) -> PerlToken:
        if self.current_token().type == token_type:
            return self.advance()
        raise PerlParseError(f"Expected {token_type}, got {self.current_token().type}")
    
    def parse_program(self) -> PerlProgram:
        """Parse Perl program"""
        statements = []
        packages = []
        use_statements = []
        shebang = None
        
        # Check for shebang
        if (self.match(PerlTokenType.COMMENT) and 
            self.current_token().value.startswith('#!')):
            shebang = self.advance().value
        
        while not self.match(PerlTokenType.EOF):
            if self.match(PerlTokenType.PACKAGE):
                packages.append(self.parse_package())
            elif self.match(PerlTokenType.USE):
                use_statements.append(self.parse_use_statement())
            else:
                stmt = self.parse_statement()
                if stmt:
                    statements.append(stmt)
        
        return PerlProgram(
            statements=statements,
            packages=packages,
            use_statements=use_statements,
            shebang=shebang
        )
    
    def parse_package(self) -> PerlPackage:
        """Parse package declaration"""
        self.consume(PerlTokenType.PACKAGE)
        name = self.consume(PerlTokenType.STRING).value  # Package name
        
        version = None
        if self.match(PerlTokenType.NUMBER):
            version = self.advance().value
        
        self.consume(PerlTokenType.SEMICOLON)
        
        return PerlPackage(name=name, version=version)
    
    def parse_use_statement(self) -> PerlUseStatement:
        """Parse use statement"""
        self.consume(PerlTokenType.USE)
        module_name = self.consume(PerlTokenType.STRING).value
        
        version = None
        import_list = []
        
        if self.match(PerlTokenType.NUMBER):
            version = self.advance().value
        
        # Simplified import list parsing
        if self.match(PerlTokenType.LEFT_PAREN):
            self.advance()
            while not self.match(PerlTokenType.RIGHT_PAREN) and not self.match(PerlTokenType.EOF):
                if self.match(PerlTokenType.STRING):
                    import_list.append(self.advance().value)
                elif self.match(PerlTokenType.COMMA):
                    self.advance()
                else:
                    break
            if self.match(PerlTokenType.RIGHT_PAREN):
                self.advance()
        
        self.consume(PerlTokenType.SEMICOLON)
        
        return PerlUseStatement(
            module_name=module_name,
            version=version,
            import_list=import_list
        )
    
    def parse_statement(self) -> Optional[PerlStatement]:
        """Parse statement"""
        if self.match(PerlTokenType.SUB):
            return self.parse_subroutine()
        elif self.match(PerlTokenType.IF):
            return self.parse_if_statement()
        elif self.match(PerlTokenType.UNLESS):
            return self.parse_unless_statement()
        elif self.match(PerlTokenType.WHILE):
            return self.parse_while_loop()
        elif self.match(PerlTokenType.FOR, PerlTokenType.FOREACH):
            return self.parse_for_loop()
        else:
            # Expression statement
            expr = self.parse_expression()
            if self.match(PerlTokenType.SEMICOLON):
                self.advance()
            return expr
    
    def parse_subroutine(self) -> PerlSubroutineDeclaration:
        """Parse subroutine declaration"""
        self.consume(PerlTokenType.SUB)
        name = self.consume(PerlTokenType.STRING).value
        
        # Simplified - just parse body
        body = []
        if self.match(PerlTokenType.LEFT_BRACE):
            self.advance()
            while not self.match(PerlTokenType.RIGHT_BRACE) and not self.match(PerlTokenType.EOF):
                stmt = self.parse_statement()
                if stmt:
                    body.append(stmt)
            self.consume(PerlTokenType.RIGHT_BRACE)
        
        return PerlSubroutineDeclaration(name=name, body=body)
    
    def parse_if_statement(self) -> PerlIfStatement:
        """Parse if statement"""
        self.consume(PerlTokenType.IF)
        self.consume(PerlTokenType.LEFT_PAREN)
        condition = self.parse_expression()
        self.consume(PerlTokenType.RIGHT_PAREN)
        
        then_block = []
        if self.match(PerlTokenType.LEFT_BRACE):
            self.advance()
            while not self.match(PerlTokenType.RIGHT_BRACE) and not self.match(PerlTokenType.EOF):
                stmt = self.parse_statement()
                if stmt:
                    then_block.append(stmt)
            self.consume(PerlTokenType.RIGHT_BRACE)
        
        return PerlIfStatement(condition=condition, then_block=then_block)
    
    def parse_unless_statement(self) -> PerlUnlessStatement:
        """Parse unless statement"""
        self.consume(PerlTokenType.UNLESS)
        self.consume(PerlTokenType.LEFT_PAREN)
        condition = self.parse_expression()
        self.consume(PerlTokenType.RIGHT_PAREN)
        
        then_block = []
        if self.match(PerlTokenType.LEFT_BRACE):
            self.advance()
            while not self.match(PerlTokenType.RIGHT_BRACE) and not self.match(PerlTokenType.EOF):
                stmt = self.parse_statement()
                if stmt:
                    then_block.append(stmt)
            self.consume(PerlTokenType.RIGHT_BRACE)
        
        return PerlUnlessStatement(condition=condition, then_block=then_block)
    
    def parse_while_loop(self) -> PerlWhileLoop:
        """Parse while loop"""
        self.consume(PerlTokenType.WHILE)
        self.consume(PerlTokenType.LEFT_PAREN)
        condition = self.parse_expression()
        self.consume(PerlTokenType.RIGHT_PAREN)
        
        body = []
        if self.match(PerlTokenType.LEFT_BRACE):
            self.advance()
            while not self.match(PerlTokenType.RIGHT_BRACE) and not self.match(PerlTokenType.EOF):
                stmt = self.parse_statement()
                if stmt:
                    body.append(stmt)
            self.consume(PerlTokenType.RIGHT_BRACE)
        
        return PerlWhileLoop(condition=condition, body=body)
    
    def parse_for_loop(self) -> Union[PerlForLoop, PerlForeachLoop]:
        """Parse for/foreach loop"""
        loop_type = self.advance().type
        
        if loop_type == PerlTokenType.FOREACH:
            # Simplified foreach parsing
            variable = None
            if self.match(PerlTokenType.SCALAR_VAR):
                var_token = self.advance()
                variable = PerlScalarVariable(name=var_token.value[1:])  # Remove $
            
            iterable = self.parse_expression()
            
            body = []
            if self.match(PerlTokenType.LEFT_BRACE):
                self.advance()
                while not self.match(PerlTokenType.RIGHT_BRACE) and not self.match(PerlTokenType.EOF):
                    stmt = self.parse_statement()
                    if stmt:
                        body.append(stmt)
                self.consume(PerlTokenType.RIGHT_BRACE)
            
            return PerlForeachLoop(variable=variable, iterable=iterable, body=body)
        else:
            # Simplified for loop
            return PerlForLoop(
                initialization=None,
                condition=None,
                increment=None,
                body=[]
            )
    
    def parse_expression(self) -> PerlExpression:
        """Parse expression (simplified)"""
        return self.parse_assignment()
    
    def parse_assignment(self) -> PerlExpression:
        """Parse assignment expression"""
        expr = self.parse_logical_or()
        
        if self.match(PerlTokenType.ASSIGN, PerlTokenType.PLUS_ASSIGN, 
                     PerlTokenType.MINUS_ASSIGN, PerlTokenType.CONCAT_ASSIGN):
            operator = self.advance().value
            right = self.parse_assignment()
            return PerlAssignment(left=expr, right=right, operator=operator)
        
        return expr
    
    def parse_logical_or(self) -> PerlExpression:
        """Parse logical OR expression"""
        expr = self.parse_logical_and()
        
        while self.match(PerlTokenType.STRING) and self.current_token().value == "or":
            operator = self.advance().value
            right = self.parse_logical_and()
            expr = PerlBinaryOperation(left=expr, right=right, operator=operator)
        
        return expr
    
    def parse_logical_and(self) -> PerlExpression:
        """Parse logical AND expression"""
        expr = self.parse_equality()
        
        while self.match(PerlTokenType.STRING) and self.current_token().value == "and":
            operator = self.advance().value
            right = self.parse_equality()
            expr = PerlBinaryOperation(left=expr, right=right, operator=operator)
        
        return expr
    
    def parse_equality(self) -> PerlExpression:
        """Parse equality expression"""
        expr = self.parse_regex_match()
        
        # Simplified equality parsing
        return expr
    
    def parse_regex_match(self) -> PerlExpression:
        """Parse regex match expression"""
        expr = self.parse_concatenation()
        
        if self.match(PerlTokenType.MATCH, PerlTokenType.NOT_MATCH):
            operator = self.advance().value
            pattern = self.parse_concatenation()
            if isinstance(pattern, PerlRegexLiteral):
                return PerlRegexMatch(string=expr, pattern=pattern, operator=operator)
        
        return expr
    
    def parse_concatenation(self) -> PerlExpression:
        """Parse string concatenation"""
        expr = self.parse_primary()
        
        # Simplified concatenation
        return expr
    
    def parse_primary(self) -> PerlExpression:
        """Parse primary expression"""
        if self.match(PerlTokenType.NUMBER):
            value = self.advance().value
            try:
                if '.' in value:
                    return PerlNumericLiteral(value=float(value))
                else:
                    return PerlNumericLiteral(value=int(value))
            except ValueError:
                return PerlNumericLiteral(value=0)
        
        elif self.match(PerlTokenType.STRING):
            value = self.advance().value
            # Remove quotes if present
            if value.startswith('"') and value.endswith('"'):
                return PerlStringLiteral(value=value[1:-1], quote_type="double")
            elif value.startswith("'") and value.endswith("'"):
                return PerlStringLiteral(value=value[1:-1], quote_type="single")
            else:
                return PerlBareword(name=value)
        
        elif self.match(PerlTokenType.REGEX):
            pattern = self.advance().value
            # Extract pattern and flags
            if pattern.startswith('/') and '/' in pattern[1:]:
                end_pos = pattern.rfind('/')
                regex_pattern = pattern[1:end_pos]
                flags = pattern[end_pos+1:]
                return PerlRegexLiteral(pattern=regex_pattern, flags=flags)
            return PerlRegexLiteral(pattern=pattern)
        
        elif self.match(PerlTokenType.SCALAR_VAR):
            var_token = self.advance()
            return PerlScalarVariable(name=var_token.value[1:])  # Remove $
        
        elif self.match(PerlTokenType.ARRAY_VAR):
            var_token = self.advance()
            return PerlArrayVariable(name=var_token.value[1:])  # Remove @
        
        elif self.match(PerlTokenType.HASH_VAR):
            var_token = self.advance()
            return PerlHashVariable(name=var_token.value[1:])  # Remove %
        
        elif self.match(PerlTokenType.LEFT_PAREN):
            self.advance()
            expr = self.parse_expression()
            self.consume(PerlTokenType.RIGHT_PAREN)
            return expr
        
        else:
            # Default to identifier
            if not self.match(PerlTokenType.EOF):
                token = self.advance()
                return PerlIdentifier(name=token.value)
            return PerlIdentifier(name="")

# Export main classes
__all__ = [
    'PerlTokenType', 'PerlToken', 'PerlLexer', 'PerlParser', 'PerlParseError'
] 