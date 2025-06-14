"""
Runa Language Lexer

SECG Compliance: Full ethical validation for all tokenization operations
Performance Target: <100ms compilation for 1000-line programs  
Self-Hosting Support: Designed to tokenize Runa compiler source code

This lexer tokenizes Runa's natural language programming syntax including:
- Variable declarations (Let, Define, Set)
- Function definitions (Process called)
- Control structures (If, For each, Match)
- Type annotations and pattern matching
- Natural language expressions
"""

import re
import time
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional, Iterator, Dict, Any, Tuple
from . import (
    secg_compliance_required, PerformanceMonitor, RUNA_COMPILATION_TARGET_MS,
    OperationResult, SECGViolationError
)

class TokenType(Enum):
    """Complete token types for Runa language syntax."""
    
    # Literals
    STRING = auto()          # "text"
    INTEGER = auto()         # 42
    FLOAT = auto()           # 3.14
    BOOLEAN_TRUE = auto()    # true  
    BOOLEAN_FALSE = auto()   # false
    NONE = auto()           # None
    
    # Identifiers
    IDENTIFIER = auto()      # variable names, function names
    TYPE_NAME = auto()       # type names (String, Integer, etc.)
    
    # Variable Declaration Keywords
    LET = auto()            # Let
    DEFINE = auto()         # Define
    SET = auto()            # Set
    BE = auto()             # be
    AS = auto()             # as
    
    # Function Keywords
    PROCESS = auto()        # Process
    CALLED = auto()         # called
    THAT = auto()           # that
    TAKES = auto()          # takes
    RETURNS = auto()        # returns
    RETURN = auto()         # Return
    WITH = auto()           # with
    
    # Control Flow Keywords
    IF = auto()             # If
    OTHERWISE = auto()      # Otherwise
    ELSE = auto()           # Else
    FOR = auto()            # For
    EACH = auto()           # each
    IN = auto()             # in
    WHILE = auto()          # While
    MATCH = auto()          # Match
    WHEN = auto()           # When
    
    # Comparison Keywords  
    IS = auto()             # is
    EQUAL = auto()          # equal
    TO = auto()             # to
    GREATER = auto()        # greater
    LESS = auto()           # less
    THAN = auto()           # than
    OR_EQUAL = auto()       # or equal
    NOT = auto()            # not
    
    # Logical Keywords
    AND = auto()            # and
    OR = auto()             # or
    
    # Arithmetic Keywords
    PLUS = auto()           # plus
    MINUS = auto()          # minus
    MULTIPLIED = auto()     # multiplied
    BY = auto()             # by
    DIVIDED = auto()        # divided
    SUM = auto()            # sum
    OF = auto()             # of
    ALL = auto()            # all
    
    # Collection Keywords
    LIST = auto()           # list
    CONTAINING = auto()     # containing
    DICTIONARY = auto()     # Dictionary
    
    # Type Keywords
    TYPE = auto()           # Type
    INTEGER_TYPE = auto()   # Integer
    STRING_TYPE = auto()    # String
    FLOAT_TYPE = auto()     # Float
    BOOLEAN_TYPE = auto()   # Boolean
    LIST_TYPE = auto()      # List
    ANY_TYPE = auto()       # Any
    NONE_TYPE = auto()      # None
    
    # Pattern Matching
    WHEN_PATTERN = auto()   # When (in pattern context)
    UNDERSCORE = auto()     # _
    PIPE = auto()           # |
    
    # Display/Output
    DISPLAY = auto()        # Display
    MESSAGE = auto()        # message
    
    # Async Keywords
    ASYNC = auto()          # Async
    AWAIT = auto()          # await
    
    # Punctuation
    COLON = auto()          # :
    COMMA = auto()          # ,
    PERIOD = auto()         # .
    LEFT_PAREN = auto()     # (
    RIGHT_PAREN = auto()    # )
    LEFT_BRACKET = auto()   # [
    RIGHT_BRACKET = auto()  # ]
    LEFT_BRACE = auto()     # {
    RIGHT_BRACE = auto()    # }
    QUOTE = auto()          # "
    
    # Whitespace and Structure
    NEWLINE = auto()        # \n
    INDENT = auto()         # Indentation increase
    DEDENT = auto()         # Indentation decrease
    WHITESPACE = auto()     # Spaces, tabs (usually ignored)
    
    # Special
    EOF = auto()            # End of file
    COMMENT = auto()        # # comments
    ERROR = auto()          # Lexical errors

@dataclass
class Token:
    """Token representation with position information."""
    type: TokenType
    value: str
    line: int
    column: int
    start_pos: int
    end_pos: int

@dataclass
class LexerState:
    """Current state of the lexer."""
    source: str
    position: int
    line: int
    column: int
    indent_stack: List[int]
    tokens: List[Token]

class LexerError(Exception):
    """Lexer-specific errors."""
    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"Lexer error at line {line}, column {column}: {message}")
        self.line = line
        self.column = column

@secg_compliance_required
class RunaLexer:
    """
    Complete lexer for Runa programming language.
    
    Tokenizes natural language programming constructs with full SECG compliance
    and performance validation. Supports all documented Runa syntax including
    variable declarations, functions, control flow, and pattern matching.
    """
    
    def __init__(self):
        """Initialize lexer with keyword mappings and performance monitoring."""
        self.performance_monitor = PerformanceMonitor()
        
        # Keyword mapping for natural language constructs
        self.keywords = {
            # Variable declarations
            'Let': TokenType.LET,
            'Define': TokenType.DEFINE, 
            'Set': TokenType.SET,
            'be': TokenType.BE,
            'as': TokenType.AS,
            
            # Functions
            'Process': TokenType.PROCESS,
            'called': TokenType.CALLED,
            'that': TokenType.THAT,
            'takes': TokenType.TAKES,
            'returns': TokenType.RETURNS,
            'Return': TokenType.RETURN,
            'with': TokenType.WITH,
            
            # Control flow
            'If': TokenType.IF,
            'Otherwise': TokenType.OTHERWISE,
            'Else': TokenType.ELSE,
            'For': TokenType.FOR,
            'each': TokenType.EACH,
            'in': TokenType.IN,
            'While': TokenType.WHILE,
            'Match': TokenType.MATCH,
            'When': TokenType.WHEN,
            
            # Comparisons
            'is': TokenType.IS,
            'equal': TokenType.EQUAL,
            'to': TokenType.TO,
            'greater': TokenType.GREATER,
            'less': TokenType.LESS,
            'than': TokenType.THAN,
            'not': TokenType.NOT,
            
            # Logical
            'and': TokenType.AND,
            'or': TokenType.OR,
            
            # Arithmetic
            'plus': TokenType.PLUS,
            'minus': TokenType.MINUS,
            'multiplied': TokenType.MULTIPLIED,
            'by': TokenType.BY,
            'divided': TokenType.DIVIDED,
            'sum': TokenType.SUM,
            'of': TokenType.OF,
            'all': TokenType.ALL,
            
            # Collections
            'list': TokenType.LIST,
            'containing': TokenType.CONTAINING,
            'Dictionary': TokenType.DICTIONARY,
            
            # Types
            'Type': TokenType.TYPE,
            'Integer': TokenType.INTEGER_TYPE,
            'String': TokenType.STRING_TYPE,
            'Float': TokenType.FLOAT_TYPE,
            'Boolean': TokenType.BOOLEAN_TYPE,
            'List': TokenType.LIST_TYPE,
            'Any': TokenType.ANY_TYPE,
            
            # Literals
            'true': TokenType.BOOLEAN_TRUE,
            'false': TokenType.BOOLEAN_FALSE,
            'None': TokenType.NONE,
            
            # Display
            'Display': TokenType.DISPLAY,
            'message': TokenType.MESSAGE,
            
            # Async
            'Async': TokenType.ASYNC,
            'await': TokenType.AWAIT,
        }
        
        # Multi-word keyword patterns
        self.multi_word_patterns = [
            (r'or\s+equal', TokenType.OR_EQUAL),
            (r'greater\s+than', TokenType.GREATER),
            (r'less\s+than', TokenType.LESS),
        ]
        
        # Regular expressions for different token types
        self.token_patterns = [
            # String literals
            (r'"([^"\\]|\\.)*"', TokenType.STRING),
            
            # Numeric literals
            (r'\d+\.\d+', TokenType.FLOAT),
            (r'\d+', TokenType.INTEGER),
            
            # Identifiers (must come after keywords)
            (r'[a-zA-Z_][a-zA-Z0-9_]*', TokenType.IDENTIFIER),
            
            # Punctuation
            (r':', TokenType.COLON),
            (r',', TokenType.COMMA),
            (r'\.', TokenType.PERIOD),
            (r'\(', TokenType.LEFT_PAREN),
            (r'\)', TokenType.RIGHT_PAREN),
            (r'\[', TokenType.LEFT_BRACKET),
            (r'\]', TokenType.RIGHT_BRACKET),
            (r'\{', TokenType.LEFT_BRACE),
            (r'\}', TokenType.RIGHT_BRACE),
            (r'"', TokenType.QUOTE),
            (r'_', TokenType.UNDERSCORE),
            (r'\|', TokenType.PIPE),
            
            # Comments
            (r'#.*', TokenType.COMMENT),
            
            # Whitespace (spaces and tabs, not newlines)
            (r'[ \t]+', TokenType.WHITESPACE),
        ]
        
        # Compile patterns for performance
        self.compiled_patterns = [
            (re.compile(pattern), token_type) 
            for pattern, token_type in self.token_patterns
        ]
    
    @PerformanceMonitor().enforce_target(RUNA_COMPILATION_TARGET_MS)
    def tokenize(self, source_code: str) -> OperationResult:
        """
        Tokenize Runa source code into tokens.
        
        Args:
            source_code: Runa source code to tokenize
            
        Returns:
            OperationResult containing list of tokens or error information
            
        Raises:
            SECGViolationError: If SECG compliance is violated
            PerformanceViolationError: If tokenization exceeds time limit
        """
        if not isinstance(source_code, str):
            return OperationResult(
                success=False,
                error=f"Expected str, got {type(source_code)}"
            )
        
        if not source_code.strip():
            return OperationResult(
                success=True,
                value=[Token(TokenType.EOF, "", 1, 1, 0, 0)],
                secg_compliant=True
            )
        
        try:
            start_time = time.perf_counter()
            
            state = LexerState(
                source=source_code,
                position=0,
                line=1,
                column=1,
                indent_stack=[0],
                tokens=[]
            )
            
            while state.position < len(state.source):
                if not self._scan_token(state):
                    break
            
            # Handle final dedents
            while len(state.indent_stack) > 1:
                state.indent_stack.pop()
                state.tokens.append(Token(
                    TokenType.DEDENT, "", state.line, state.column,
                    state.position, state.position
                ))
            
            # Add EOF token
            state.tokens.append(Token(
                TokenType.EOF, "", state.line, state.column,
                state.position, state.position
            ))
            
            end_time = time.perf_counter()
            execution_time = (end_time - start_time) * 1000
            
            return OperationResult(
                success=True,
                value=state.tokens,
                execution_time_ms=execution_time,
                secg_compliant=True
            )
            
        except LexerError as e:
            return OperationResult(
                success=False,
                error=str(e),
                secg_compliant=True
            )
        except Exception as e:
            return OperationResult(
                success=False,
                error=f"Unexpected lexer error: {e}",
                secg_compliant=True
            )
    
    def _scan_token(self, state: LexerState) -> bool:
        """Scan next token from source code."""
        if state.position >= len(state.source):
            return False
        
        current_char = state.source[state.position]
        
        # Handle newlines and indentation
        if current_char == '\n':
            self._handle_newline(state)
            return True
        
        # Skip whitespace (except significant indentation)
        if current_char in ' \t' and state.column > 1:
            self._skip_whitespace(state)
            return True
        
        # Handle indentation at start of line
        if state.column == 1 and current_char in ' \t':
            self._handle_indentation(state)
            return True
        
        # Try multi-word patterns first
        for pattern, token_type in self.multi_word_patterns:
            match = re.match(pattern, state.source[state.position:], re.IGNORECASE)
            if match:
                self._add_token(state, token_type, match.group(0))
                self._advance_position(state, len(match.group(0)))
                return True
        
        # Try single token patterns
        for pattern, token_type in self.compiled_patterns:
            match = pattern.match(state.source, state.position)
            if match:
                matched_text = match.group(0)
                
                # Handle keywords vs identifiers
                if token_type == TokenType.IDENTIFIER:
                    token_type = self.keywords.get(matched_text, TokenType.IDENTIFIER)
                
                # Skip whitespace tokens (but not other tokens)
                if token_type != TokenType.WHITESPACE:
                    self._add_token(state, token_type, matched_text)
                
                self._advance_position(state, len(matched_text))
                return True
        
        # Handle unknown character
        self._add_token(state, TokenType.ERROR, current_char)
        self._advance_position(state, 1)
        return True
    
    def _handle_newline(self, state: LexerState):
        """Handle newline character and advance to next line."""
        self._add_token(state, TokenType.NEWLINE, '\n')
        state.position += 1
        state.line += 1
        state.column = 1
    
    def _skip_whitespace(self, state: LexerState):
        """Skip whitespace characters."""
        while (state.position < len(state.source) and 
               state.source[state.position] in ' \t'):
            state.position += 1
            state.column += 1
    
    def _handle_indentation(self, state: LexerState):
        """Handle indentation for block structure."""
        indent_level = 0
        start_pos = state.position
        
        while (state.position < len(state.source) and 
               state.source[state.position] in ' \t'):
            if state.source[state.position] == ' ':
                indent_level += 1
            elif state.source[state.position] == '\t':
                indent_level += 4  # Tab = 4 spaces
            state.position += 1
        
        state.column = indent_level + 1
        
        # Compare with current indentation level
        current_indent = state.indent_stack[-1]
        
        if indent_level > current_indent:
            # Increased indentation
            state.indent_stack.append(indent_level)
            self._add_token(state, TokenType.INDENT, 
                          state.source[start_pos:state.position])
        elif indent_level < current_indent:
            # Decreased indentation - may need multiple dedents
            while (len(state.indent_stack) > 1 and 
                   state.indent_stack[-1] > indent_level):
                state.indent_stack.pop()
                self._add_token(state, TokenType.DEDENT, "")
            
            if state.indent_stack[-1] != indent_level:
                raise LexerError(
                    f"Inconsistent indentation level {indent_level}",
                    state.line, state.column
                )
    
    def _add_token(self, state: LexerState, token_type: TokenType, value: str):
        """Add token to token list."""
        token = Token(
            type=token_type,
            value=value,
            line=state.line,
            column=state.column,
            start_pos=state.position,
            end_pos=state.position + len(value)
        )
        state.tokens.append(token)
    
    def _advance_position(self, state: LexerState, count: int):
        """Advance position by count characters."""
        for _ in range(count):
            if state.position < len(state.source):
                if state.source[state.position] == '\n':
                    state.line += 1
                    state.column = 1
                else:
                    state.column += 1
                state.position += 1

# Export for use by other modules
__all__ = ['RunaLexer', 'Token', 'TokenType', 'LexerError']
