"""
Scilla Parser Implementation

This module provides lexical analysis and parsing for the Scilla smart contract language.
Scilla is a functional programming language with safety guarantees for smart contracts
on the Zilliqa blockchain.

Features:
- Functional programming constructs (let, match, lambda)
- Pattern matching and algebraic data types
- Contract definitions with fields and transitions  
- Type safety and dependent types
- Gas-bounded computation model
"""

import re
from typing import List, Optional, Union, Dict, Any, Tuple
from dataclasses import dataclass
from enum import Enum, auto

from .scilla_ast import *


class ScillaTokenType(Enum):
    """Scilla token types"""
    # Literals
    INTEGER = auto()
    STRING = auto()
    BYSTR = auto()
    ADDRESS = auto()
    BOOLEAN = auto()
    
    # Identifiers
    IDENTIFIER = auto()
    TYPE_IDENTIFIER = auto()
    BUILTIN = auto()
    
    # Keywords
    SCILLA_VERSION = auto()
    LIBRARY = auto()
    IMPORT = auto()
    CONTRACT = auto()
    FIELD = auto()
    TRANSITION = auto()
    PROCEDURE = auto()
    LET = auto()
    IN = auto()
    MATCH = auto()
    WITH = auto()
    FUN = auto()
    TFUN = auto()
    TYPE = auto()
    OF = auto()
    END = auto()
    SEND = auto()
    EVENT = auto()
    THROW = auto()
    ACCEPT = auto()
    DELETE = auto()
    FORALL = auto()
    EXISTS = auto()
    
    # Types
    UINT32 = auto()
    UINT64 = auto()
    UINT128 = auto()
    UINT256 = auto()
    INT32 = auto()
    INT64 = auto()
    INT128 = auto()
    INT256 = auto()
    STRING_TYPE = auto()
    BYSTR_TYPE = auto()
    BNUM = auto()
    MAP = auto()
    LIST = auto()
    OPTION = auto()
    PAIR = auto()
    MESSAGE = auto()
    EVENT_TYPE = auto()
    EXCEPTION = auto()
    
    # Operators
    ARROW = auto()          # =>
    TYPE_ARROW = auto()     # ->
    ASSIGN = auto()         # :=
    LOAD = auto()           # <-
    PIPE = auto()           # |
    AT = auto()             # @
    AMPERSAND = auto()      # &
    
    # Punctuation
    LPAREN = auto()         # (
    RPAREN = auto()         # )
    LBRACE = auto()         # {
    RBRACE = auto()         # }
    LBRACKET = auto()       # [
    RBRACKET = auto()       # ]
    SEMICOLON = auto()      # ;
    COLON = auto()          # :
    COMMA = auto()          # ,
    DOT = auto()            # .
    UNDERSCORE = auto()     # _
    APOSTROPHE = auto()     # '
    DOLLAR = auto()         # $
    
    # Special
    EOF = auto()
    NEWLINE = auto()
    COMMENT = auto()
    

@dataclass
class ScillaToken:
    """Scilla token"""
    type: ScillaTokenType
    value: str
    line: int
    column: int


class ScillaLexer:
    """Scilla lexical analyzer"""
    
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        
        # Keywords mapping
        self.keywords = {
            'scilla_version': ScillaTokenType.SCILLA_VERSION,
            'library': ScillaTokenType.LIBRARY,
            'import': ScillaTokenType.IMPORT,
            'contract': ScillaTokenType.CONTRACT,
            'field': ScillaTokenType.FIELD,
            'transition': ScillaTokenType.TRANSITION,
            'procedure': ScillaTokenType.PROCEDURE,
            'let': ScillaTokenType.LET,
            'in': ScillaTokenType.IN,
            'match': ScillaTokenType.MATCH,
            'with': ScillaTokenType.WITH,
            'fun': ScillaTokenType.FUN,
            'tfun': ScillaTokenType.TFUN,
            'type': ScillaTokenType.TYPE,
            'of': ScillaTokenType.OF,
            'end': ScillaTokenType.END,
            'send': ScillaTokenType.SEND,
            'event': ScillaTokenType.EVENT,
            'throw': ScillaTokenType.THROW,
            'accept': ScillaTokenType.ACCEPT,
            'delete': ScillaTokenType.DELETE,
            'forall': ScillaTokenType.FORALL,
            'exists': ScillaTokenType.EXISTS,
            'True': ScillaTokenType.BOOLEAN,
            'False': ScillaTokenType.BOOLEAN,
            
            # Type keywords
            'Uint32': ScillaTokenType.UINT32,
            'Uint64': ScillaTokenType.UINT64, 
            'Uint128': ScillaTokenType.UINT128,
            'Uint256': ScillaTokenType.UINT256,
            'Int32': ScillaTokenType.INT32,
            'Int64': ScillaTokenType.INT64,
            'Int128': ScillaTokenType.INT128,
            'Int256': ScillaTokenType.INT256,
            'String': ScillaTokenType.STRING_TYPE,
            'ByStr': ScillaTokenType.BYSTR_TYPE,
            'BNum': ScillaTokenType.BNUM,
            'Map': ScillaTokenType.MAP,
            'List': ScillaTokenType.LIST,
            'Option': ScillaTokenType.OPTION,
            'Pair': ScillaTokenType.PAIR,
            'Message': ScillaTokenType.MESSAGE,
            'Event': ScillaTokenType.EVENT_TYPE,
            'Exception': ScillaTokenType.EXCEPTION,
        }
        
        # Built-in functions
        self.builtins = {
            'eq', 'lt', 'le', 'gt', 'ge', 'add', 'sub', 'mul', 'div', 'rem',
            'and', 'or', 'not', 'concat', 'substr', 'strlen', 'to_string',
            'to_bystr', 'to_nat', 'sha256hash', 'keccak256hash', 'ripemd160hash',
            'schnorr_verify', 'ecdsa_verify', 'some', 'none', 'nil', 'cons',
            'list_head', 'list_tail', 'list_length', 'list_reverse', 'list_append',
            'list_concat', 'list_filter', 'list_exists', 'list_forall', 'list_sort',
            'contains', 'get', 'put', 'remove', 'to_list', 'size'
        }
    
    def error(self, message: str):
        """Raise a lexer error"""
        raise SyntaxError(f"Lexer error at line {self.line}, column {self.column}: {message}")
    
    def peek(self, offset: int = 0) -> Optional[str]:
        """Peek at character at current position + offset"""
        pos = self.pos + offset
        if pos >= len(self.text):
            return None
        return self.text[pos]
    
    def advance(self) -> Optional[str]:
        """Advance position and return current character"""
        if self.pos >= len(self.text):
            return None
        
        char = self.text[self.pos]
        self.pos += 1
        
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
            
        return char
    
    def skip_whitespace(self):
        """Skip whitespace characters"""
        while self.peek() and self.peek() in ' \t\r':
            self.advance()
    
    def read_comment(self) -> ScillaToken:
        """Read single-line comment"""
        start_line = self.line
        start_column = self.column
        value = ""
        
        # Skip '(*'
        self.advance()  # (
        self.advance()  # *
        
        depth = 1
        while depth > 0 and self.peek():
            if self.peek() == '(' and self.peek(1) == '*':
                depth += 1
                value += self.advance()
                value += self.advance()
            elif self.peek() == '*' and self.peek(1) == ')':
                depth -= 1
                if depth > 0:
                    value += self.advance()
                    value += self.advance()
                else:
                    self.advance()  # *
                    self.advance()  # )
            else:
                value += self.advance()
        
        return ScillaToken(ScillaTokenType.COMMENT, value, start_line, start_column)
    
    def read_string(self) -> ScillaToken:
        """Read string literal"""
        start_line = self.line
        start_column = self.column
        value = ""
        
        # Skip opening quote
        quote_char = self.advance()
        
        while self.peek() and self.peek() != quote_char:
            if self.peek() == '\\':
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
                elif escaped == quote_char:
                    value += quote_char
                else:
                    value += escaped
            else:
                value += self.advance()
        
        if not self.peek():
            self.error("Unterminated string literal")
        
        # Skip closing quote
        self.advance()
        
        return ScillaToken(ScillaTokenType.STRING, value, start_line, start_column)
    
    def read_number(self) -> ScillaToken:
        """Read integer literal"""
        start_line = self.line
        start_column = self.column
        value = ""
        
        while self.peek() and (self.peek().isdigit() or self.peek() == '_'):
            if self.peek() != '_':  # Skip underscores in numbers
                value += self.advance()
            else:
                self.advance()
        
        return ScillaToken(ScillaTokenType.INTEGER, value, start_line, start_column)
    
    def read_hex_bystr(self) -> ScillaToken:
        """Read hex byte string literal"""
        start_line = self.line
        start_column = self.column
        value = ""
        
        # Skip '0x'
        self.advance()
        self.advance()
        
        while self.peek() and self.peek().lower() in '0123456789abcdef':
            value += self.advance()
        
        return ScillaToken(ScillaTokenType.BYSTR, "0x" + value, start_line, start_column)
    
    def read_identifier(self) -> ScillaToken:
        """Read identifier or keyword"""
        start_line = self.line
        start_column = self.column
        value = ""
        
        # First character (letter or underscore)
        value += self.advance()
        
        # Subsequent characters (letters, digits, underscores, apostrophes)
        while (self.peek() and 
               (self.peek().isalnum() or self.peek() in "_'")):
            value += self.advance()
        
        # Check if it's a keyword
        token_type = self.keywords.get(value, ScillaTokenType.IDENTIFIER)
        
        # Check if it's a builtin
        if value in self.builtins:
            token_type = ScillaTokenType.BUILTIN
        
        # Check if it's a type identifier (starts with uppercase)
        if token_type == ScillaTokenType.IDENTIFIER and value[0].isupper():
            token_type = ScillaTokenType.TYPE_IDENTIFIER
        
        return ScillaToken(token_type, value, start_line, start_column)
    
    def tokenize(self) -> List[ScillaToken]:
        """Tokenize the input text"""
        while self.pos < len(self.text):
            self.skip_whitespace()
            
            if self.pos >= len(self.text):
                break
            
            char = self.peek()
            start_line = self.line
            start_column = self.column
            
            # Comments
            if char == '(' and self.peek(1) == '*':
                self.tokens.append(self.read_comment())
                continue
            
            # Newlines
            if char == '\n':
                self.tokens.append(ScillaToken(ScillaTokenType.NEWLINE, char, start_line, start_column))
                self.advance()
                continue
            
            # Strings
            if char in '"\'':
                self.tokens.append(self.read_string())
                continue
            
            # Numbers
            if char.isdigit():
                self.tokens.append(self.read_number())
                continue
            
            # Hex byte strings
            if char == '0' and self.peek(1) == 'x':
                self.tokens.append(self.read_hex_bystr())
                continue
            
            # Identifiers and keywords
            if char.isalpha() or char == '_':
                self.tokens.append(self.read_identifier())
                continue
            
            # Two-character operators
            if char == '=' and self.peek(1) == '>':
                self.tokens.append(ScillaToken(ScillaTokenType.ARROW, '=>', start_line, start_column))
                self.advance()
                self.advance()
                continue
            
            if char == '-' and self.peek(1) == '>':
                self.tokens.append(ScillaToken(ScillaTokenType.TYPE_ARROW, '->', start_line, start_column))
                self.advance()
                self.advance()
                continue
            
            if char == ':' and self.peek(1) == '=':
                self.tokens.append(ScillaToken(ScillaTokenType.ASSIGN, ':=', start_line, start_column))
                self.advance()
                self.advance()
                continue
            
            if char == '<' and self.peek(1) == '-':
                self.tokens.append(ScillaToken(ScillaTokenType.LOAD, '<-', start_line, start_column))
                self.advance()
                self.advance()
                continue
            
            # Single-character tokens
            single_tokens = {
                '(': ScillaTokenType.LPAREN,
                ')': ScillaTokenType.RPAREN,
                '{': ScillaTokenType.LBRACE,
                '}': ScillaTokenType.RBRACE,
                '[': ScillaTokenType.LBRACKET,
                ']': ScillaTokenType.RBRACKET,
                ';': ScillaTokenType.SEMICOLON,
                ':': ScillaTokenType.COLON,
                ',': ScillaTokenType.COMMA,
                '.': ScillaTokenType.DOT,
                '_': ScillaTokenType.UNDERSCORE,
                "'": ScillaTokenType.APOSTROPHE,
                '$': ScillaTokenType.DOLLAR,
                '|': ScillaTokenType.PIPE,
                '@': ScillaTokenType.AT,
                '&': ScillaTokenType.AMPERSAND,
            }
            
            if char in single_tokens:
                self.tokens.append(ScillaToken(single_tokens[char], char, start_line, start_column))
                self.advance()
                continue
            
            # Unknown character
            self.error(f"Unexpected character: {char}")
        
        # Add EOF token
        self.tokens.append(ScillaToken(ScillaTokenType.EOF, "", self.line, self.column))
        return self.tokens


class ScillaParser:
    """Scilla parser"""
    
    def __init__(self, tokens: List[ScillaToken]):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[0] if tokens else None
    
    def error(self, message: str):
        """Raise a parser error"""
        token = self.current_token
        raise SyntaxError(f"Parse error at line {token.line}, column {token.column}: {message}")
    
    def peek(self, offset: int = 0) -> Optional[ScillaToken]:
        """Peek at token at current position + offset"""
        pos = self.pos + offset
        if pos >= len(self.tokens):
            return None
        return self.tokens[pos]
    
    def advance(self) -> Optional[ScillaToken]:
        """Advance to next token"""
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
            self.current_token = self.tokens[self.pos]
        return self.current_token
    
    def expect(self, token_type: ScillaTokenType) -> ScillaToken:
        """Expect a specific token type"""
        if not self.current_token or self.current_token.type != token_type:
            self.error(f"Expected {token_type}, got {self.current_token.type if self.current_token else 'EOF'}")
        
        token = self.current_token
        self.advance()
        return token
    
    def match(self, *token_types: ScillaTokenType) -> bool:
        """Check if current token matches any of the given types"""
        return self.current_token and self.current_token.type in token_types
    
    def skip_newlines(self):
        """Skip newline tokens"""
        while self.match(ScillaTokenType.NEWLINE, ScillaTokenType.COMMENT):
            self.advance()
    
    def parse_type(self) -> ScillaType:
        """Parse a type expression"""
        self.skip_newlines()
        
        if self.match(ScillaTokenType.UINT32, ScillaTokenType.UINT64, ScillaTokenType.UINT128, ScillaTokenType.UINT256,
                      ScillaTokenType.INT32, ScillaTokenType.INT64, ScillaTokenType.INT128, ScillaTokenType.INT256,
                      ScillaTokenType.STRING_TYPE, ScillaTokenType.BYSTR_TYPE, ScillaTokenType.BNUM,
                      ScillaTokenType.MESSAGE, ScillaTokenType.EVENT_TYPE, ScillaTokenType.EXCEPTION):
            
            type_map = {
                ScillaTokenType.UINT32: ScillaPrimitiveType.UINT32,
                ScillaTokenType.UINT64: ScillaPrimitiveType.UINT64,
                ScillaTokenType.UINT128: ScillaPrimitiveType.UINT128,
                ScillaTokenType.UINT256: ScillaPrimitiveType.UINT256,
                ScillaTokenType.INT32: ScillaPrimitiveType.INT32,
                ScillaTokenType.INT64: ScillaPrimitiveType.INT64,
                ScillaTokenType.INT128: ScillaPrimitiveType.INT128,
                ScillaTokenType.INT256: ScillaPrimitiveType.INT256,
                ScillaTokenType.STRING_TYPE: ScillaPrimitiveType.STRING,
                ScillaTokenType.BYSTR_TYPE: ScillaPrimitiveType.BYSTR,
                ScillaTokenType.BNUM: ScillaPrimitiveType.BNUM,
                ScillaTokenType.MESSAGE: ScillaPrimitiveType.MESSAGE,
                ScillaTokenType.EVENT_TYPE: ScillaPrimitiveType.EVENT,
                ScillaTokenType.EXCEPTION: ScillaPrimitiveType.EXCEPTION,
            }
            
            token = self.current_token
            self.advance()
            return ScillaPrimitive(type=type_map[token.type])
        
        elif self.match(ScillaTokenType.MAP):
            self.advance()  # MAP
            key_type = self.parse_type()
            value_type = self.parse_type()
            return ScillaMapType(key_type=key_type, value_type=value_type)
        
        elif self.match(ScillaTokenType.LIST):
            self.advance()  # LIST
            element_type = self.parse_type()
            return ScillaListType(element_type=element_type)
        
        elif self.match(ScillaTokenType.OPTION):
            self.advance()  # OPTION
            element_type = self.parse_type()
            return ScillaOptionType(element_type=element_type)
        
        elif self.match(ScillaTokenType.PAIR):
            self.advance()  # PAIR
            first_type = self.parse_type()
            second_type = self.parse_type()
            return ScillaPairType(first_type=first_type, second_type=second_type)
        
        elif self.match(ScillaTokenType.TYPE_IDENTIFIER):
            name = self.current_token.value
            self.advance()
            
            # Check for type arguments
            type_args = []
            while self.match(ScillaTokenType.UINT32, ScillaTokenType.UINT64, ScillaTokenType.TYPE_IDENTIFIER, 
                           ScillaTokenType.MAP, ScillaTokenType.LIST, ScillaTokenType.OPTION, ScillaTokenType.PAIR):
                type_args.append(self.parse_type())
            
            return ScillaCustomType(name=name, type_args=type_args)
        
        elif self.match(ScillaTokenType.LPAREN):
            self.advance()  # (
            self.skip_newlines()
            
            # Parse function type or parenthesized type
            first_type = self.parse_type()
            
            if self.match(ScillaTokenType.TYPE_ARROW):
                # Function type
                self.advance()  # ->
                return_type = self.parse_type()
                self.expect(ScillaTokenType.RPAREN)
                return ScillaFunctionType(arg_types=[first_type], return_type=return_type)
            else:
                # Parenthesized type
                self.expect(ScillaTokenType.RPAREN)
                return first_type
        
        else:
            self.error(f"Expected type, got {self.current_token.type}")
    
    def parse_pattern(self) -> ScillaPattern:
        """Parse a pattern"""
        self.skip_newlines()
        
        if self.match(ScillaTokenType.UNDERSCORE):
            self.advance()
            return ScillaWildcardPattern()
        
        elif self.match(ScillaTokenType.IDENTIFIER):
            name = self.current_token.value
            self.advance()
            return ScillaVariablePattern(name=name)
        
        elif self.match(ScillaTokenType.TYPE_IDENTIFIER):
            constructor = self.current_token.value
            self.advance()
            
            args = []
            while (self.match(ScillaTokenType.IDENTIFIER, ScillaTokenType.TYPE_IDENTIFIER, 
                             ScillaTokenType.UNDERSCORE, ScillaTokenType.INTEGER, 
                             ScillaTokenType.STRING, ScillaTokenType.BOOLEAN)):
                args.append(self.parse_pattern())
            
            return ScillaConstructorPattern(constructor=constructor, args=args)
        
        elif self.match(ScillaTokenType.INTEGER):
            value = self.current_token.value
            self.advance()
            literal = ScillaIntLiteral(value=value)
            return ScillaLiteralPattern(literal=literal)
        
        elif self.match(ScillaTokenType.STRING):
            value = self.current_token.value
            self.advance()
            literal = ScillaStringLiteral(value=value)
            return ScillaLiteralPattern(literal=literal)
        
        elif self.match(ScillaTokenType.BOOLEAN):
            value = self.current_token.value == "True"
            self.advance()
            literal = ScillaBoolLiteral(value=value)
            return ScillaLiteralPattern(literal=literal)
        
        else:
            self.error(f"Expected pattern, got {self.current_token.type}")
    
    def parse_expression(self) -> ScillaExpression:
        """Parse an expression"""
        return self.parse_let_expression()
    
    def parse_let_expression(self) -> ScillaExpression:
        """Parse let expression"""
        if self.match(ScillaTokenType.LET):
            self.advance()  # let
            
            bindings = []
            while True:
                pattern = self.parse_pattern()
                self.expect(ScillaTokenType.ASSIGN)
                expr = self.parse_expression()
                bindings.append((pattern, expr))
                
                if self.match(ScillaTokenType.IN):
                    break
                # Continue parsing more bindings
            
            self.advance()  # in
            body = self.parse_expression()
            
            return ScillaLet(bindings=bindings, body=body)
        
        return self.parse_match_expression()
    
    def parse_match_expression(self) -> ScillaExpression:
        """Parse match expression"""
        if self.match(ScillaTokenType.MATCH):
            self.advance()  # match
            expr = self.parse_expression()
            self.expect(ScillaTokenType.WITH)
            
            branches = []
            while not self.match(ScillaTokenType.END, ScillaTokenType.EOF):
                self.skip_newlines()
                if self.match(ScillaTokenType.PIPE):
                    self.advance()  # |
                
                pattern = self.parse_pattern()
                self.expect(ScillaTokenType.ARROW)
                branch_expr = self.parse_expression()
                branches.append((pattern, branch_expr))
                
                self.skip_newlines()
            
            if self.match(ScillaTokenType.END):
                self.advance()  # end
            
            return ScillaMatch(expr=expr, branches=branches)
        
        return self.parse_application()
    
    def parse_application(self) -> ScillaExpression:
        """Parse function application"""
        expr = self.parse_primary()
        
        while (self.match(ScillaTokenType.IDENTIFIER, ScillaTokenType.TYPE_IDENTIFIER,
                          ScillaTokenType.INTEGER, ScillaTokenType.STRING, 
                          ScillaTokenType.BOOLEAN, ScillaTokenType.BYSTR,
                          ScillaTokenType.LPAREN, ScillaTokenType.LBRACE)):
            
            if self.match(ScillaTokenType.AT):
                # Type application
                self.advance()  # @
                type_args = [self.parse_type()]
                expr = ScillaTApp(expr=expr, type_args=type_args)
            else:
                # Regular application
                arg = self.parse_primary()
                if isinstance(expr, ScillaApplication):
                    expr.args.append(arg)
                else:
                    expr = ScillaApplication(function=expr, args=[arg])
        
        return expr
    
    def parse_primary(self) -> ScillaExpression:
        """Parse primary expression"""
        self.skip_newlines()
        
        if self.match(ScillaTokenType.IDENTIFIER):
            name = self.current_token.value
            self.advance()
            return ScillaIdentifier(name=name)
        
        elif self.match(ScillaTokenType.BUILTIN):
            name = self.current_token.value
            self.advance()
            
            # Parse type arguments if present
            type_args = []
            if self.match(ScillaTokenType.LBRACE):
                self.advance()  # {
                while not self.match(ScillaTokenType.RBRACE):
                    type_args.append(self.parse_type())
                    if self.match(ScillaTokenType.COMMA):
                        self.advance()
                self.advance()  # }
            
            # Parse arguments
            args = []
            while (self.match(ScillaTokenType.IDENTIFIER, ScillaTokenType.INTEGER, 
                             ScillaTokenType.STRING, ScillaTokenType.BOOLEAN, 
                             ScillaTokenType.BYSTR, ScillaTokenType.LPAREN)):
                args.append(self.parse_primary())
            
            return ScillaBuiltinCall(builtin=name, args=args, type_args=type_args)
        
        elif self.match(ScillaTokenType.INTEGER):
            value = self.current_token.value
            self.advance()
            literal = ScillaIntLiteral(value=value)
            return ScillaLiteral(literal=literal)
        
        elif self.match(ScillaTokenType.STRING):
            value = self.current_token.value
            self.advance()
            literal = ScillaStringLiteral(value=value)
            return ScillaLiteral(literal=literal)
        
        elif self.match(ScillaTokenType.BOOLEAN):
            value = self.current_token.value == "True"
            self.advance()
            literal = ScillaBoolLiteral(value=value)
            return ScillaLiteral(literal=literal)
        
        elif self.match(ScillaTokenType.BYSTR):
            value = self.current_token.value
            self.advance()
            literal = ScillaByStrLiteral(value=value)
            return ScillaLiteral(literal=literal)
        
        elif self.match(ScillaTokenType.LPAREN):
            self.advance()  # (
            expr = self.parse_expression()
            self.expect(ScillaTokenType.RPAREN)
            return expr
        
        elif self.match(ScillaTokenType.LBRACE):
            # Constructor or message
            self.advance()  # {
            
            if self.match(ScillaTokenType.TYPE_IDENTIFIER):
                # Constructor
                name = self.current_token.value
                self.advance()
                
                args = []
                while not self.match(ScillaTokenType.RBRACE):
                    args.append(self.parse_expression())
                    if self.match(ScillaTokenType.SEMICOLON):
                        self.advance()
                
                self.expect(ScillaTokenType.RBRACE)
                return ScillaConstructor(name=name, args=args)
            
            else:
                # Message construction
                fields = {}
                while not self.match(ScillaTokenType.RBRACE):
                    if self.match(ScillaTokenType.IDENTIFIER):
                        field_name = self.current_token.value
                        self.advance()
                        self.expect(ScillaTokenType.COLON)
                        field_value = self.parse_expression()
                        fields[field_name] = field_value
                        
                        if self.match(ScillaTokenType.SEMICOLON):
                            self.advance()
                
                self.expect(ScillaTokenType.RBRACE)
                return ScillaMessageConstruction(fields=fields)
        
        elif self.match(ScillaTokenType.FUN):
            # Lambda expression
            self.advance()  # fun
            self.expect(ScillaTokenType.LPAREN)
            
            params = []
            while not self.match(ScillaTokenType.RPAREN):
                name = self.expect(ScillaTokenType.IDENTIFIER).value
                self.expect(ScillaTokenType.COLON)
                param_type = self.parse_type()
                params.append((name, param_type))
                
                if self.match(ScillaTokenType.COMMA):
                    self.advance()
            
            self.expect(ScillaTokenType.RPAREN)
            self.expect(ScillaTokenType.ARROW)
            body = self.parse_expression()
            
            return ScillaLambda(params=params, body=body)
        
        elif self.match(ScillaTokenType.TFUN):
            # Type abstraction
            self.advance()  # tfun
            
            type_vars = []
            while self.match(ScillaTokenType.APOSTROPHE):
                self.advance()  # '
                type_var = self.expect(ScillaTokenType.IDENTIFIER).value
                type_vars.append(type_var)
            
            self.expect(ScillaTokenType.ARROW)
            body = self.parse_expression()
            
            return ScillaTFun(type_vars=type_vars, body=body)
        
        else:
            self.error(f"Expected expression, got {self.current_token.type}")
    
    def parse_statement(self) -> ScillaStatement:
        """Parse a statement"""
        self.skip_newlines()
        
        if self.match(ScillaTokenType.IDENTIFIER):
            # Could be assignment, load, or bind
            var_name = self.current_token.value
            self.advance()
            
            if self.match(ScillaTokenType.LOAD):
                # Load statement: x <- field
                self.advance()  # <-
                field = self.expect(ScillaTokenType.IDENTIFIER).value
                return ScillaLoad(var=var_name, field=field)
            
            elif self.match(ScillaTokenType.ASSIGN):
                # Store statement: field := expr OR bind: x = expr
                self.advance()  # := or =
                value = self.parse_expression()
                
                # Assume it's a store to a field
                return ScillaStore(field=var_name, value=value)
            
            else:
                self.error(f"Expected assignment operator after identifier")
        
        elif self.match(ScillaTokenType.SEND):
            self.advance()  # send
            messages = self.parse_expression()
            return ScillaSend(messages=messages)
        
        elif self.match(ScillaTokenType.EVENT):
            self.advance()  # event
            event = self.parse_expression()
            return ScillaEvent(event=event)
        
        elif self.match(ScillaTokenType.THROW):
            self.advance()  # throw
            exception = self.parse_expression()
            return ScillaThrow(exception=exception)
        
        elif self.match(ScillaTokenType.ACCEPT):
            self.advance()  # accept
            return ScillaAccept()
        
        elif self.match(ScillaTokenType.DELETE):
            self.advance()  # delete
            map_name = self.expect(ScillaTokenType.IDENTIFIER).value
            self.expect(ScillaTokenType.LBRACKET)
            key = self.parse_expression()
            self.expect(ScillaTokenType.RBRACKET)
            return ScillaMapDelete(map_name=map_name, key=key)
        
        elif self.match(ScillaTokenType.MATCH):
            # Match statement
            self.advance()  # match
            expr = self.parse_expression()
            self.expect(ScillaTokenType.WITH)
            
            branches = []
            while not self.match(ScillaTokenType.END, ScillaTokenType.EOF):
                self.skip_newlines()
                if self.match(ScillaTokenType.PIPE):
                    self.advance()  # |
                
                pattern = self.parse_pattern()
                self.expect(ScillaTokenType.ARROW)
                
                # Parse statements until next pattern or end
                statements = []
                while not self.match(ScillaTokenType.PIPE, ScillaTokenType.END, ScillaTokenType.EOF):
                    self.skip_newlines()
                    if self.match(ScillaTokenType.PIPE, ScillaTokenType.END, ScillaTokenType.EOF):
                        break
                    statements.append(self.parse_statement())
                
                branches.append((pattern, statements))
                self.skip_newlines()
            
            if self.match(ScillaTokenType.END):
                self.advance()  # end
            
            return ScillaMatchStmt(expr=expr, branches=branches)
        
        else:
            self.error(f"Expected statement, got {self.current_token.type}")
    
    def parse_contract(self) -> ScillaContract:
        """Parse contract definition"""
        self.expect(ScillaTokenType.CONTRACT)
        contract_name = self.expect(ScillaTokenType.TYPE_IDENTIFIER).value
        
        # Parse contract parameters
        self.expect(ScillaTokenType.LPAREN)
        immutable_params = []
        
        while not self.match(ScillaTokenType.RPAREN):
            param_name = self.expect(ScillaTokenType.IDENTIFIER).value
            self.expect(ScillaTokenType.COLON)
            param_type = self.parse_type()
            immutable_params.append(ScillaParameter(name=param_name, type=param_type))
            
            if self.match(ScillaTokenType.COMMA):
                self.advance()
        
        self.expect(ScillaTokenType.RPAREN)
        self.skip_newlines()
        
        # Parse fields
        fields = []
        while self.match(ScillaTokenType.FIELD):
            self.advance()  # field
            field_name = self.expect(ScillaTokenType.IDENTIFIER).value
            self.expect(ScillaTokenType.COLON)
            field_type = self.parse_type()
            
            # Default to mutable
            mutability = ScillaFieldType.MUTABLE
            
            # Optional initialization
            init_value = None
            if self.match(ScillaTokenType.ASSIGN):
                self.advance()
                init_value = self.parse_expression()
            
            fields.append(ScillaFieldDeclaration(
                name=field_name, 
                type=field_type, 
                mutability=mutability,
                init_value=init_value
            ))
            self.skip_newlines()
        
        # Parse transitions and procedures
        transitions = []
        procedures = []
        
        while self.match(ScillaTokenType.TRANSITION, ScillaTokenType.PROCEDURE):
            if self.match(ScillaTokenType.TRANSITION):
                self.advance()  # transition
                transition_name = self.expect(ScillaTokenType.IDENTIFIER).value
                
                # Parse parameters
                self.expect(ScillaTokenType.LPAREN)
                params = []
                
                while not self.match(ScillaTokenType.RPAREN):
                    param_name = self.expect(ScillaTokenType.IDENTIFIER).value
                    self.expect(ScillaTokenType.COLON)
                    param_type = self.parse_type()
                    params.append(ScillaParameter(name=param_name, type=param_type))
                    
                    if self.match(ScillaTokenType.COMMA):
                        self.advance()
                
                self.expect(ScillaTokenType.RPAREN)
                self.skip_newlines()
                
                # Parse statements
                statements = []
                while not self.match(ScillaTokenType.TRANSITION, ScillaTokenType.PROCEDURE, 
                                   ScillaTokenType.EOF, ScillaTokenType.END):
                    self.skip_newlines()
                    if self.match(ScillaTokenType.TRANSITION, ScillaTokenType.PROCEDURE, 
                                 ScillaTokenType.EOF, ScillaTokenType.END):
                        break
                    statements.append(self.parse_statement())
                
                transitions.append(ScillaTransition(
                    name=transition_name,
                    params=params,
                    statements=statements
                ))
            
            elif self.match(ScillaTokenType.PROCEDURE):
                self.advance()  # procedure
                proc_name = self.expect(ScillaTokenType.IDENTIFIER).value
                
                # Parse parameters
                self.expect(ScillaTokenType.LPAREN)
                params = []
                
                while not self.match(ScillaTokenType.RPAREN):
                    param_name = self.expect(ScillaTokenType.IDENTIFIER).value
                    self.expect(ScillaTokenType.COLON)
                    param_type = self.parse_type()
                    params.append(ScillaParameter(name=param_name, type=param_type))
                    
                    if self.match(ScillaTokenType.COMMA):
                        self.advance()
                
                self.expect(ScillaTokenType.RPAREN)
                self.skip_newlines()
                
                # Parse statements
                statements = []
                while not self.match(ScillaTokenType.TRANSITION, ScillaTokenType.PROCEDURE, 
                                   ScillaTokenType.EOF, ScillaTokenType.END):
                    self.skip_newlines()
                    if self.match(ScillaTokenType.TRANSITION, ScillaTokenType.PROCEDURE, 
                                 ScillaTokenType.EOF, ScillaTokenType.END):
                        break
                    statements.append(self.parse_statement())
                
                procedures.append(ScillaProcedure(
                    name=proc_name,
                    params=params,
                    statements=statements
                ))
        
        return ScillaContract(
            name=contract_name,
            library=None,  # Will be set if library is parsed
            imports=[],    # Will be set if imports are parsed
            type_params=[],
            immutable_params=immutable_params,
            fields=fields,
            transitions=transitions,
            procedures=procedures
        )
    
    def parse_program(self) -> ScillaProgram:
        """Parse complete Scilla program"""
        self.skip_newlines()
        
        # Parse scilla_version
        self.expect(ScillaTokenType.SCILLA_VERSION)
        version = self.expect(ScillaTokenType.INTEGER).value
        self.skip_newlines()
        
        # Parse imports
        imports = []
        while self.match(ScillaTokenType.IMPORT):
            self.advance()  # import
            module = self.expect(ScillaTokenType.IDENTIFIER).value
            imports.append(ScillaImport(module=module))
            self.skip_newlines()
        
        # Parse library (optional)
        library = None
        if self.match(ScillaTokenType.LIBRARY):
            self.advance()  # library
            lib_name = self.expect(ScillaTokenType.IDENTIFIER).value
            # For simplicity, create empty library
            library = ScillaLibrary(
                name=lib_name,
                imports=imports,
                type_declarations=[],
                function_declarations=[]
            )
            self.skip_newlines()
        
        # Parse contract
        contract = self.parse_contract()
        contract.library = library
        contract.imports = imports
        
        return ScillaProgram(
            scilla_version=version,
            libraries=[library] if library else [],
            contract=contract
        )


def parse_scilla(text: str) -> ScillaProgram:
    """Parse Scilla source code"""
    lexer = ScillaLexer(text)
    tokens = lexer.tokenize()
    
    # Filter out comments for parsing
    tokens = [t for t in tokens if t.type != ScillaTokenType.COMMENT]
    
    parser = ScillaParser(tokens)
    return parser.parse_program() 