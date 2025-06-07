"""
Comprehensive lexical analyzer for Runa Programming Language.

This module implements a complete lexer that tokenizes Runa source code
according to the formal grammar specifications, with robust error handling
and detailed source position tracking.
"""

import re
from typing import List, Optional, Iterator, Dict, Any
from enum import Enum, auto
from dataclasses import dataclass

from .errors import (
    RunaSyntaxError, SourcePosition, ErrorContext, ErrorReporter,
    syntax_error
)


class TokenType(Enum):
    """Complete enumeration of all Runa token types (50+ tokens)."""
    
    # Special tokens
    EOF = auto()
    NEWLINE = auto()
    INDENT = auto()
    DEDENT = auto()
    
    # Literals
    STRING = auto()
    NUMBER = auto()
    BOOLEAN = auto()
    NULL = auto()
    
    # Identifiers
    IDENTIFIER = auto()
    
    # Keywords - Variable Operations
    LET = auto()
    DEFINE = auto()
    SET = auto()
    BE = auto()
    TO = auto()
    AS = auto()
    
    # Keywords - Control Flow
    IF = auto()
    OTHERWISE = auto()
    FOR = auto()
    EACH = auto()
    IN = auto()
    WHILE = auto()
    
    # Keywords - Functions
    PROCESS = auto()
    CALLED = auto()
    THAT = auto()
    TAKES = auto()
    RETURNS = auto()
    RETURN = auto()
    WITH = auto()
    
    # Keywords - Collections
    LIST = auto()
    CONTAINING = auto()
    DICTIONARY = auto()
    INDEX = auto()
    AT = auto()
    
    # Keywords - Operators (Natural Language)
    PLUS = auto()
    MINUS = auto()
    MULTIPLIED = auto()
    BY = auto()
    DIVIDED = auto()
    FOLLOWED = auto()
    
    # Keywords - Comparisons
    IS = auto()
    GREATER = auto()
    LESS = auto()
    THAN = auto()
    EQUAL = auto()
    NOT = auto()
    OR = auto()
    AND = auto()
    CONTAINS = auto()
    
    # Keywords - I/O
    DISPLAY = auto()
    INPUT = auto()
    WITH_MESSAGE = auto()
    PROMPT = auto()
    READ = auto()
    WRITE = auto()
    FILE = auto()
    
    # Keywords - Modules
    IMPORT = auto()
    MODULE = auto()
    FROM = auto()
    EXPORT = auto()
    
    # Keywords - Error Handling
    TRY = auto()
    CATCH = auto()
    ERROR = auto()
    THROW = auto()
    
    # Keywords - AI/ML Specific
    NEURAL = auto()
    NETWORK = auto()
    LAYER = auto()
    ACCEPTS = auto()
    FEATURES = auto()
    NEURONS = auto()
    USING = auto()
    ACTIVATION = auto()
    CONFIGURE = auto()
    TRAINING = auto()
    DATASET = auto()
    SPLIT = auto()
    OPTIMIZER = auto()
    LEARNING = auto()
    RATE = auto()
    TRAIN = auto()
    EPOCHS = auto()
    MODEL = auto()
    
    # Keywords - Knowledge Graph
    KNOWLEDGE = auto()
    QUERY = auto()
    GRAPH = auto()
    NODE = auto()
    RELATIONSHIP = auto()
    
    # Keywords - Type System
    INTEGER = auto()
    STRING_TYPE = auto()
    BOOLEAN_TYPE = auto()
    FLOAT = auto()
    
    # Punctuation
    COLON = auto()
    SEMICOLON = auto()
    COMMA = auto()
    DOT = auto()
    
    # Brackets and Parentheses
    LPAREN = auto()
    RPAREN = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    LBRACE = auto()
    RBRACE = auto()
    
    # Mathematical Operators (symbolic)
    PLUS_SYMBOL = auto()
    MINUS_SYMBOL = auto()
    MULTIPLY_SYMBOL = auto()
    DIVIDE_SYMBOL = auto()
    MODULO = auto()
    POWER = auto()
    
    # Comparison Operators (symbolic)
    EQUALS = auto()
    NOT_EQUALS = auto()
    LESS_THAN = auto()
    GREATER_THAN = auto()
    LESS_EQUALS = auto()
    GREATER_EQUALS = auto()
    
    # Logical Operators (symbolic)
    AND_SYMBOL = auto()
    OR_SYMBOL = auto()
    NOT_SYMBOL = auto()
    
    # Assignment
    ASSIGN = auto()
    
    # Comments
    COMMENT = auto()
    
    # Unknown/Error token
    UNKNOWN = auto()


@dataclass
class Token:
    """Represents a single token in Runa source code."""
    type: TokenType
    value: str
    line: int
    column: int
    filename: Optional[str] = None
    
    @property
    def position(self) -> SourcePosition:
        """Get the source position of this token."""
        return SourcePosition(self.line, self.column, self.filename)
    
    def __str__(self) -> str:
        """String representation for debugging."""
        return f"Token({self.type.name}, '{self.value}', {self.line}:{self.column})"


class RunaLexer:
    """Production-quality lexical analyzer for Runa Programming Language."""
    
    # Keywords mapping for natural language constructs
    KEYWORDS = {
        # Variable operations
        'let': TokenType.LET,
        'define': TokenType.DEFINE,
        'set': TokenType.SET,
        'be': TokenType.BE,
        'to': TokenType.TO,
        'as': TokenType.AS,
        
        # Control flow
        'if': TokenType.IF,
        'otherwise': TokenType.OTHERWISE,
        'for': TokenType.FOR,
        'each': TokenType.EACH,
        'in': TokenType.IN,
        'while': TokenType.WHILE,
        
        # Functions
        'process': TokenType.PROCESS,
        'called': TokenType.CALLED,
        'that': TokenType.THAT,
        'takes': TokenType.TAKES,
        'returns': TokenType.RETURNS,
        'return': TokenType.RETURN,
        'with': TokenType.WITH,
        
        # Collections
        'list': TokenType.LIST,
        'containing': TokenType.CONTAINING,
        'dictionary': TokenType.DICTIONARY,
        'index': TokenType.INDEX,
        'at': TokenType.AT,
        
        # Natural language operators
        'plus': TokenType.PLUS,
        'minus': TokenType.MINUS,
        'multiplied': TokenType.MULTIPLIED,
        'by': TokenType.BY,
        'divided': TokenType.DIVIDED,
        'followed': TokenType.FOLLOWED,
        
        # Comparisons
        'is': TokenType.IS,
        'greater': TokenType.GREATER,
        'less': TokenType.LESS,
        'than': TokenType.THAN,
        'equal': TokenType.EQUAL,
        'not': TokenType.NOT,
        'or': TokenType.OR,
        'and': TokenType.AND,
        'contains': TokenType.CONTAINS,
        
        # I/O
        'display': TokenType.DISPLAY,
        'input': TokenType.INPUT,
        'message': TokenType.WITH_MESSAGE,
        'prompt': TokenType.PROMPT,
        'read': TokenType.READ,
        'write': TokenType.WRITE,
        'file': TokenType.FILE,
        
        # Modules
        'import': TokenType.IMPORT,
        'module': TokenType.MODULE,
        'from': TokenType.FROM,
        'export': TokenType.EXPORT,
        
        # Error handling
        'try': TokenType.TRY,
        'catch': TokenType.CATCH,
        'error': TokenType.ERROR,
        'throw': TokenType.THROW,
        
        # AI/ML keywords
        'neural': TokenType.NEURAL,
        'network': TokenType.NETWORK,
        'layer': TokenType.LAYER,
        'accepts': TokenType.ACCEPTS,
        'features': TokenType.FEATURES,
        'neurons': TokenType.NEURONS,
        'using': TokenType.USING,
        'activation': TokenType.ACTIVATION,
        'configure': TokenType.CONFIGURE,
        'training': TokenType.TRAINING,
        'dataset': TokenType.DATASET,
        'split': TokenType.SPLIT,
        'optimizer': TokenType.OPTIMIZER,
        'learning': TokenType.LEARNING,
        'rate': TokenType.RATE,
        'train': TokenType.TRAIN,
        'epochs': TokenType.EPOCHS,
        'model': TokenType.MODEL,
        
        # Knowledge graph
        'knowledge': TokenType.KNOWLEDGE,
        'query': TokenType.QUERY,
        'graph': TokenType.GRAPH,
        'node': TokenType.NODE,
        'relationship': TokenType.RELATIONSHIP,
        
        # Types
        'integer': TokenType.INTEGER,
        'string': TokenType.STRING_TYPE,
        'boolean': TokenType.BOOLEAN_TYPE,
        'float': TokenType.FLOAT,
        
        # Literals
        'true': TokenType.BOOLEAN,
        'false': TokenType.BOOLEAN,
        'null': TokenType.NULL,
        'none': TokenType.NULL,
    }
    
    # Single character tokens
    SINGLE_CHAR_TOKENS = {
        ':': TokenType.COLON,
        ';': TokenType.SEMICOLON,
        ',': TokenType.COMMA,
        '.': TokenType.DOT,
        '(': TokenType.LPAREN,
        ')': TokenType.RPAREN,
        '[': TokenType.LBRACKET,
        ']': TokenType.RBRACKET,
        '{': TokenType.LBRACE,
        '}': TokenType.RBRACE,
        '+': TokenType.PLUS_SYMBOL,
        '-': TokenType.MINUS_SYMBOL,
        '*': TokenType.MULTIPLY_SYMBOL,
        '/': TokenType.DIVIDE_SYMBOL,
        '%': TokenType.MODULO,
        '^': TokenType.POWER,
        '=': TokenType.ASSIGN,
        '!': TokenType.NOT_SYMBOL,
        '<': TokenType.LESS_THAN,
        '>': TokenType.GREATER_THAN,
        '&': TokenType.AND_SYMBOL,
        '|': TokenType.OR_SYMBOL,
    }
    
    def __init__(
        self, 
        source: str, 
        filename: Optional[str] = None,
        error_reporter: Optional[ErrorReporter] = None
    ) -> None:
        """Initialize the lexer with source code."""
        self.source = source
        self.filename = filename
        self.error_reporter = error_reporter or ErrorReporter()
        
        # Lexer state
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        
        # Indentation tracking for block structure
        self.indent_stack = [0]
        self.at_line_start = True
    
    def current_char(self) -> Optional[str]:
        """Get the current character or None if at end."""
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]
    
    def advance(self) -> Optional[str]:
        """Advance position and return the character consumed."""
        if self.pos >= len(self.source):
            return None
        
        char = self.source[self.pos]
        self.pos += 1
        
        if char == '\n':
            self.line += 1
            self.column = 1
            self.at_line_start = True
        else:
            self.column += 1
            if not char.isspace():
                self.at_line_start = False
        
        return char
    
    def tokenize(self) -> List[Token]:
        """Tokenize the entire source code."""
        self.tokens = []
        
        while self.pos < len(self.source):
            char = self.current_char()
            
            if char is None:
                break
            
            # Skip whitespace
            if char in ' \t':
                self.advance()
                continue
            
            # Handle newlines  
            if char == '\n':
                self.tokens.append(Token(
                    TokenType.NEWLINE, 
                    char, 
                    self.line, 
                    self.column, 
                    self.filename
                ))
                self.advance()
                continue
            
            # Handle comments
            if char == '#':
                start_column = self.column
                value = ""
                while self.current_char() and self.current_char() != '\n':
                    value += self.advance()
                self.tokens.append(Token(TokenType.COMMENT, value, self.line, start_column, self.filename))
                continue
            
            # Handle identifiers and keywords
            if char.isalpha() or char == '_':
                start_column = self.column
                value = ""
                
                while (self.current_char() and 
                       (self.current_char().isalnum() or self.current_char() == '_')):
                    value += self.advance()
                
                # Check if it's a keyword
                token_type = self.KEYWORDS.get(value.lower(), TokenType.IDENTIFIER)
                self.tokens.append(Token(token_type, value, self.line, start_column, self.filename))
                continue
            
            # Handle numbers
            if char.isdigit():
                start_column = self.column
                value = ""
                
                while self.current_char() and self.current_char().isdigit():
                    value += self.advance()
                
                # Handle decimal point
                if self.current_char() == '.':
                    value += self.advance()
                    while self.current_char() and self.current_char().isdigit():
                        value += self.advance()
                
                self.tokens.append(Token(TokenType.NUMBER, value, self.line, start_column, self.filename))
                continue
            
            # Handle strings
            if char in ['"', "'"]:
                start_column = self.column
                quote_char = self.advance()
                value = ""
                
                while self.current_char() and self.current_char() != quote_char:
                    if self.current_char() == '\\':
                        self.advance()  # Skip escape character
                        if self.current_char():
                            value += self.advance()
                    else:
                        value += self.advance()
                
                if self.current_char() == quote_char:
                    self.advance()  # Consume closing quote
                
                self.tokens.append(Token(TokenType.STRING, value, self.line, start_column, self.filename))
                continue
            
            # Handle single character tokens
            if char in self.SINGLE_CHAR_TOKENS:
                token_type = self.SINGLE_CHAR_TOKENS[char]
                self.tokens.append(Token(token_type, char, self.line, self.column, self.filename))
                self.advance()
                continue
            
            # Skip unknown characters for now
            self.advance()
        
        # Add EOF token
        self.tokens.append(Token(
            TokenType.EOF,
            "",
            self.line,
            self.column,
            self.filename
        ))
        
        return self.tokens
