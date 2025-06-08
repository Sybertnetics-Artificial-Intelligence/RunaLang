"""
Token definitions for the Runa programming language.

This module defines all token types used in the Runa lexical analysis.
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional, Any


class TokenType(Enum):
    """Enumeration of all token types in the Runa language."""
    
    # Keywords
    LET = auto()
    DEFINE = auto()
    SET = auto()
    IF = auto()
    OTHERWISE = auto()
    FOR = auto()
    EACH = auto()
    IN = auto()
    WHILE = auto()
    PROCESS = auto()
    CALLED = auto()
    THAT = auto()
    TAKES = auto()
    RETURNS = auto()
    RETURN = auto()
    DISPLAY = auto()
    WITH = auto()
    MESSAGE = auto()
    IMPORT = auto()
    MODULE = auto()
    FROM = auto()
    TRY = auto()
    CATCH = auto()
    
    # Collection keywords
    LIST = auto()
    CONTAINING = auto()
    DICTIONARY = auto()
    
    # Operators
    IS = auto()
    BE = auto()
    AS = auto()
    TO = auto()
    GREATER = auto()
    LESS = auto()
    THAN = auto()
    EQUAL = auto()
    NOT = auto()
    OR = auto()
    AND = auto()
    
    # Special expressions
    LENGTH = auto()
    OF = auto()
    SUM = auto()
    ALL = auto()
    MULTIPLIED = auto()
    BY = auto()
    PLUS = auto()
    MINUS = auto()
    DIVIDED = auto()
    FOLLOWED = auto()
    AT = auto()
    INDEX = auto()
    CONVERT = auto()
    
    # Literals
    STRING = auto()
    NUMBER = auto()
    TRUE = auto()
    FALSE = auto()
    NULL = auto()
    
    # Punctuation
    COLON = auto()
    COMMA = auto()
    DOT = auto()
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    
    # Other
    IDENTIFIER = auto()
    INDENT = auto()
    DEDENT = auto()
    NEWLINE = auto()
    COMMENT = auto()
    EOF = auto()
    ERROR = auto()


@dataclass
class Token:
    """
    Represents a token in the Runa language.
    
    Attributes:
        type: The type of the token
        lexeme: The string value of the token
        literal: The literal value for literals (numbers, strings, etc.)
        line: Line number in the source code
        column: Column number in the source code
    """
    
    type: TokenType
    lexeme: str
    literal: Optional[Any] = None
    line: int = 0
    column: int = 0
    
    def __str__(self) -> str:
        if self.literal is not None:
            return f"{self.type.name}({self.lexeme}, {self.literal})"
        return f"{self.type.name}({self.lexeme})"


# Mapping of keywords to token types
KEYWORDS = {
    "let": TokenType.LET,
    "define": TokenType.DEFINE,
    "set": TokenType.SET,
    "if": TokenType.IF,
    "otherwise": TokenType.OTHERWISE,
    "for": TokenType.FOR,
    "each": TokenType.EACH,
    "in": TokenType.IN,
    "while": TokenType.WHILE,
    "process": TokenType.PROCESS,
    "called": TokenType.CALLED,
    "that": TokenType.THAT,
    "takes": TokenType.TAKES,
    "returns": TokenType.RETURNS,
    "return": TokenType.RETURN,
    "display": TokenType.DISPLAY,
    "with": TokenType.WITH,
    "message": TokenType.MESSAGE,
    "import": TokenType.IMPORT,
    "module": TokenType.MODULE,
    "from": TokenType.FROM,
    "try": TokenType.TRY,
    "catch": TokenType.CATCH,
    "list": TokenType.LIST,
    "containing": TokenType.CONTAINING,
    "dictionary": TokenType.DICTIONARY,
    "is": TokenType.IS,
    "be": TokenType.BE,
    "as": TokenType.AS,
    "to": TokenType.TO,
    "greater": TokenType.GREATER,
    "less": TokenType.LESS,
    "than": TokenType.THAN,
    "equal": TokenType.EQUAL,
    "not": TokenType.NOT,
    "or": TokenType.OR,
    "and": TokenType.AND,
    "length": TokenType.LENGTH,
    "of": TokenType.OF,
    "sum": TokenType.SUM,
    "all": TokenType.ALL,
    "multiplied": TokenType.MULTIPLIED,
    "by": TokenType.BY,
    "plus": TokenType.PLUS,
    "minus": TokenType.MINUS,
    "divided": TokenType.DIVIDED,
    "followed": TokenType.FOLLOWED,
    "at": TokenType.AT,
    "index": TokenType.INDEX,
    "convert": TokenType.CONVERT,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "null": TokenType.NULL,
    "none": TokenType.NULL
} 