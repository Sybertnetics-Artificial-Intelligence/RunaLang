"""
Runa Token Definitions

Defines all token types for the Runa natural language syntax according to 
the Runa Formal Grammar Specifications.
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Any, Optional

class TokenType(Enum):
    # Literals
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    BOOLEAN = auto()
    IDENTIFIER = auto()
    
    # Keywords - Variable declarations
    LET = auto()           # "Let"
    DEFINE = auto()        # "Define"  
    SET = auto()           # "Set"
    CONSTANT = auto()      # "constant"
    
    # Keywords - Control flow
    IF = auto()            # "If"
    OTHERWISE = auto()     # "Otherwise"
    UNLESS = auto()        # "Unless"
    WHEN = auto()          # "When"
    MATCH = auto()         # "Match"
    SWITCH = auto()        # "Switch"
    CASE = auto()          # "Case"
    DEFAULT = auto()       # "Default"
    
    # Keywords - Loops
    FOR = auto()           # "For"
    EACH = auto()          # "each"
    IN = auto()            # "in"
    WHILE = auto()         # "While"
    DO = auto()            # "Do"
    REPEAT = auto()        # "Repeat"
    TIMES = auto()         # "times"
    LOOP = auto()          # "Loop"
    FOREVER = auto()       # "forever"
    FROM = auto()          # "from"
    TO = auto()            # "to"
    STEP = auto()          # "step"
    BY = auto()            # "by"
    
    # Keywords - Functions/Processes
    PROCESS = auto()       # "Process"
    CALLED = auto()        # "called"
    THAT = auto()          # "that"
    TAKES = auto()         # "takes"
    RETURNS = auto()       # "returns"
    RETURN = auto()        # "Return"
    YIELD = auto()         # "Yield"
    
    # Keywords - Connecting words
    BE = auto()            # "be"
    AS = auto()            # "as"
    WITH = auto()          # "with"
    AND = auto()           # "and"
    OR = auto()            # "or"
    OF = auto()            # "of"
    THE = auto()           # "the"
    A = auto()             # "a"
    AN = auto()            # "an"
    
    # Keywords - Type annotations
    TYPE = auto()          # "Type"
    INTEGER_TYPE = auto()  # "Integer"
    FLOAT_TYPE = auto()    # "Float"
    STRING_TYPE = auto()   # "String"
    BOOLEAN_TYPE = auto()  # "Boolean"
    CHARACTER = auto()     # "Character"
    BYTE = auto()          # "Byte"
    ANY = auto()           # "Any"
    VOID = auto()          # "Void"
    NEVER = auto()         # "Never"
    OPTIONAL = auto()      # "Optional"
    ARRAY = auto()         # "Array"
    LIST = auto()          # "List"
    TUPLE = auto()         # "Tuple"
    DICTIONARY = auto()    # "Dictionary"
    RECORD = auto()        # "Record"
    FUNCTION = auto()      # "Function"
    
    # Keywords - Collections
    CONTAINING = auto()    # "containing"
    EMPTY = auto()         # "empty"
    
    # Keywords - Natural language operators
    IS = auto()            # "is"
    EQUALS = auto()        # "equal to" / "equals"
    NOT_EQUALS = auto()    # "not equal to"
    GREATER_THAN = auto()  # "greater than"
    LESS_THAN = auto()     # "less than"
    GREATER_EQUAL = auto() # "greater than or equal to"
    LESS_EQUAL = auto()    # "less than or equal to"
    PLUS = auto()          # "plus"
    MINUS = auto()         # "minus"
    MULTIPLY = auto()      # "multiplied by"
    DIVIDE = auto()        # "divided by"
    MODULO = auto()        # "modulo"
    POWER = auto()         # "to the power of"
    FOLLOWED = auto()      # "followed by"
    
    # Keywords - Logical operators  
    NOT = auto()           # "not"
    
    # Keywords - Control flow
    BREAK = auto()         # "Break"
    CONTINUE = auto()      # "Continue"
    THROW = auto()         # "Throw"
    TRY = auto()           # "Try"
    CATCH = auto()         # "Catch"
    FINALLY = auto()       # "Finally"
    
    # Keywords - Memory and concurrency
    AWAIT = auto()         # "Await"
    ASYNC = auto()         # "Async"
    SEND = auto()          # "Send"
    ATOMIC = auto()        # "Atomic"
    LOCK = auto()          # "Lock"
    OWNED = auto()         # "owned"
    BORROWED = auto()      # "borrowed"
    SHARED = auto()        # "shared"
    LIFETIME = auto()      # "lifetime"
    
    # Keywords - Modules
    IMPORT = auto()        # "Import"
    EXPORT = auto()        # "Export"
    MODULE = auto()        # "Module"
    EXPOSING = auto()      # "exposing"
    ALL = auto()           # "all"
    
    # Keywords - Other
    DISPLAY = auto()       # "Display"
    MESSAGE = auto()       # "message"
    NOTE = auto()          # "Note"
    ASSERT = auto()        # "Assert"
    DELETE = auto()        # "Delete"
    WHERE = auto()         # "where"
    FALLTHROUGH = auto()   # "Fallthrough"
    
    # Punctuation
    COLON = auto()         # ":"
    COMMA = auto()         # ","
    DOT = auto()           # "."
    SEMICOLON = auto()     # ";"
    QUESTION = auto()      # "?"
    EXCLAMATION = auto()   # "!"
    AT = auto()            # "@"
    
    # Brackets
    LPAREN = auto()        # "("
    RPAREN = auto()        # ")"
    LBRACKET = auto()      # "["
    RBRACKET = auto()      # "]"
    LBRACE = auto()        # "{"
    RBRACE = auto()        # "}"
    
    # Special tokens
    NEWLINE = auto()
    INDENT = auto()
    DEDENT = auto()
    EOF = auto()
    WILDCARD = auto()      # "_"
    PIPE = auto()          # "|"

@dataclass
class Token:
    """Represents a token in the Runa source code."""
    type: TokenType
    value: Any
    line: int
    column: int
    length: int = 1
    
    def __str__(self) -> str:
        return f"Token({self.type.name}, {repr(self.value)}, {self.line}:{self.column})"
    
    def __repr__(self) -> str:
        return self.__str__()

# Multi-word token mappings for natural language syntax
MULTI_WORD_TOKENS = {
    # Natural language operators
    "is equal to": TokenType.EQUALS,
    "is not equal to": TokenType.NOT_EQUALS, 
    "is greater than": TokenType.GREATER_THAN,
    "is less than": TokenType.LESS_THAN,
    "is greater than or equal to": TokenType.GREATER_EQUAL,
    "is less than or equal to": TokenType.LESS_EQUAL,
    "equal to": TokenType.EQUALS,
    "not equal to": TokenType.NOT_EQUALS,
    "greater than": TokenType.GREATER_THAN,
    "less than": TokenType.LESS_THAN, 
    "greater than or equal to": TokenType.GREATER_EQUAL,
    "less than or equal to": TokenType.LESS_EQUAL,
    "multiplied by": TokenType.MULTIPLY,
    "divided by": TokenType.DIVIDE,
    "followed by": TokenType.FOLLOWED,
    "to the power of": TokenType.POWER,
    
    # Function/Process syntax - these should be separate tokens
    # "Process called": (TokenType.PROCESS, TokenType.CALLED),
    # "that takes": (TokenType.THAT, TokenType.TAKES),
    "For each": (TokenType.FOR, TokenType.EACH),
    
    # Type syntax
    "list containing": (TokenType.LIST, TokenType.CONTAINING),
    "dictionary with": (TokenType.DICTIONARY, TokenType.WITH),
    "of type": (TokenType.OF, TokenType.TYPE),
}

# Single word token mappings
KEYWORDS = {
    # Variable declarations
    "Let": TokenType.LET,
    "Define": TokenType.DEFINE,
    "Set": TokenType.SET,
    "constant": TokenType.CONSTANT,
    
    # Control flow
    "If": TokenType.IF,
    "Otherwise": TokenType.OTHERWISE,
    "Unless": TokenType.UNLESS,
    "When": TokenType.WHEN,
    "Match": TokenType.MATCH,
    "Switch": TokenType.SWITCH,
    "Case": TokenType.CASE,
    "Default": TokenType.DEFAULT,
    
    # Loops
    "For": TokenType.FOR,
    "each": TokenType.EACH,
    "in": TokenType.IN,
    "While": TokenType.WHILE,
    "Do": TokenType.DO,
    "Repeat": TokenType.REPEAT,
    "times": TokenType.TIMES,
    "Loop": TokenType.LOOP,
    "forever": TokenType.FOREVER,
    "from": TokenType.FROM,
    "to": TokenType.TO,
    "step": TokenType.STEP,
    "by": TokenType.BY,
    
    # Functions/Processes
    "Process": TokenType.PROCESS,
    "called": TokenType.CALLED,
    "that": TokenType.THAT,
    "takes": TokenType.TAKES,
    "returns": TokenType.RETURNS,
    "Return": TokenType.RETURN,
    "Yield": TokenType.YIELD,
    
    # Connecting words
    "be": TokenType.BE,
    "as": TokenType.AS,
    "with": TokenType.WITH,
    "and": TokenType.AND,
    "or": TokenType.OR,
    "of": TokenType.OF,
    "the": TokenType.THE,
    "a": TokenType.A,
    "an": TokenType.AN,
    
    # Types
    "Type": TokenType.TYPE,
    "Integer": TokenType.INTEGER_TYPE,
    "Float": TokenType.FLOAT_TYPE,
    "String": TokenType.STRING_TYPE,
    "Boolean": TokenType.BOOLEAN_TYPE,
    "Character": TokenType.CHARACTER,
    "Byte": TokenType.BYTE,
    "Any": TokenType.ANY,
    "Void": TokenType.VOID,
    "Never": TokenType.NEVER,
    "Optional": TokenType.OPTIONAL,
    "Array": TokenType.ARRAY,
    "List": TokenType.LIST,
    "Tuple": TokenType.TUPLE,
    "Dictionary": TokenType.DICTIONARY,
    "Record": TokenType.RECORD,
    "Function": TokenType.FUNCTION,
    
    # Collections
    "containing": TokenType.CONTAINING,
    "empty": TokenType.EMPTY,
    
    # Operators
    "is": TokenType.IS,
    "equals": TokenType.EQUALS,
    "plus": TokenType.PLUS,
    "minus": TokenType.MINUS,
    "modulo": TokenType.MODULO,
    "not": TokenType.NOT,
    
    # Control flow
    "Break": TokenType.BREAK,
    "Continue": TokenType.CONTINUE,
    "Throw": TokenType.THROW,
    "Try": TokenType.TRY,
    "Catch": TokenType.CATCH,
    "Finally": TokenType.FINALLY,
    
    # Concurrency
    "Await": TokenType.AWAIT,
    "Async": TokenType.ASYNC,
    "Send": TokenType.SEND,
    "Atomic": TokenType.ATOMIC,
    "Lock": TokenType.LOCK,
    "owned": TokenType.OWNED,
    "borrowed": TokenType.BORROWED,
    "shared": TokenType.SHARED,
    "lifetime": TokenType.LIFETIME,
    
    # Modules
    "Import": TokenType.IMPORT,
    "Export": TokenType.EXPORT,
    "Module": TokenType.MODULE,
    "exposing": TokenType.EXPOSING,
    "all": TokenType.ALL,
    
    # Other
    "Display": TokenType.DISPLAY,
    "message": TokenType.MESSAGE,
    "Note": TokenType.NOTE,
    "Assert": TokenType.ASSERT,
    "Delete": TokenType.DELETE,
    "where": TokenType.WHERE,
    "Fallthrough": TokenType.FALLTHROUGH,
    
    # Boolean literals
    "true": TokenType.BOOLEAN,
    "false": TokenType.BOOLEAN,
    "True": TokenType.BOOLEAN,
    "False": TokenType.BOOLEAN,
} 