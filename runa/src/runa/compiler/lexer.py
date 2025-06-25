"""
Runa Lexer - Production-Ready Tokenizer

Implements comprehensive lexical analysis for Runa programming language with:
- 50+ token types covering all language constructs
- Natural language-like syntax support
- Comprehensive error handling and reporting
- Performance optimization for <100ms compilation target
"""

import re
from typing import Iterator, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    """Comprehensive token types for Runa language constructs."""
    
    # Literals
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    BOOLEAN = auto()
    TRUE = auto()  # Added for parser compatibility
    FALSE = auto()  # Added for parser compatibility
    NULL = auto()
    
    # Identifiers
    IDENTIFIER = auto()
    TYPE_IDENTIFIER = auto()
    
    # Keywords - Core Language
    LET = auto()
    DEFINE = auto()
    SET = auto()
    TO = auto()
    AS = auto()
    BE = auto()
    CONTAINING = auto()
    PROCESS = auto()
    CALLED = auto()
    THAT = auto()
    TAKES = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    IF = auto()
    OTHERWISE = auto()
    FOR = auto()
    EACH = auto()
    WHILE = auto()
    RETURN = auto()
    RETURNING = auto()  # Added for function return type
    IMPORT = auto()
    FROM = auto()
    EXPORT = auto()
    DISPLAY = auto()
    IN = auto()  # Added for 'in' keyword in for loops
    
    # Natural Language Operators
    BY = auto()
    IS = auto()
    EQUAL = auto()
    GREATER = auto()
    THAN = auto()
    LESS = auto()
    FOLLOWED = auto()
    
    # AI Block Tokens
    AT_SYMBOL = auto()  # @ symbol for AI blocks
    END = auto()  # @end for AI blocks
    
    # Keywords - AI-Specific
    REASONING = auto()
    END_REASONING = auto()
    IMPLEMENTATION = auto()
    END_IMPLEMENTATION = auto()
    VERIFY = auto()
    END_VERIFY = auto()
    SEND = auto()
    WITH = auto()
    CONTEXT = auto()
    TASK = auto()
    INCLUDE = auto()
    REQUEST = auto()
    DEFINE_AI = auto()
    AGENT = auto()
    PURPOSE = auto()
    CAPABILITY = auto()
    MODIFY = auto()
    SAFETY = auto()
    CONSTRAINT = auto()
    VALIDATION = auto()
    
    # AI Communication Keywords
    ASK = auto()
    TELL = auto()
    QUERY = auto()
    INSTRUCT = auto()
    DELEGATE = auto()
    WAIT = auto()
    BROADCAST = auto()
    COORDINATE = auto()
    ABOUT = auto()
    RELATIONSHIP = auto()
    
    # Keywords - Control Flow
    BREAK = auto()
    CONTINUE = auto()
    TRY = auto()
    CATCH = auto()
    FINALLY = auto()
    THROW = auto()
    RAISE = auto()
    
    # Keywords - Types
    INTEGER_TYPE = auto()
    FLOAT_TYPE = auto()
    STRING_TYPE = auto()
    BOOLEAN_TYPE = auto()
    LIST_TYPE = auto()
    DICTIONARY_TYPE = auto()
    FUNCTION_TYPE = auto()
    VOID_TYPE = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    POWER = auto()
    ASSIGN = auto()
    EQUALS = auto()
    NOT_EQUALS = auto()
    LESS_THAN = auto()
    LESS_EQUALS = auto()
    GREATER_THAN = auto()
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
    
    # Delimiters
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    SEMICOLON = auto()
    COLON = auto()
    COMMA = auto()
    DOT = auto()
    ARROW = auto()
    PIPE = auto()
    
    # Special
    NEWLINE = auto()
    INDENT = auto()
    DEDENT = auto()
    EOF = auto()
    ERROR = auto()
    
    # Comments and Documentation
    COMMENT = auto()
    DOCSTRING = auto()
    
    # Uncertainty and Confidence
    UNCERTAINTY = auto()
    CONFIDENCE = auto()
    
    # Knowledge Graph
    KNOWLEDGE = auto()
    GRAPH = auto()
    
    # Neural Network
    NEURAL = auto()
    NETWORK = auto()
    LAYER = auto()
    ACTIVATION = auto()
    LOSS = auto()
    OPTIMIZER = auto()


@dataclass
class Token:
    """Token representation with comprehensive metadata."""
    type: TokenType
    value: str
    line: int
    column: int
    source_file: Optional[str] = None
    
    def __str__(self) -> str:
        return f"Token({self.type.name}, '{self.value}', line={self.line}, col={self.column})"
    
    def __repr__(self) -> str:
        return self.__str__()


class LexerError(Exception):
    """Lexer-specific error with detailed context."""
    
    def __init__(self, message: str, line: int, column: int, source_file: Optional[str] = None):
        self.message = message
        self.line = line
        self.column = column
        self.source_file = source_file
        super().__init__(f"LexerError at line {line}, column {column}: {message}")


class RunaLexer:
    """
    Production-ready lexer for Runa programming language.
    
    Features:
    - 50+ token types for comprehensive language support
    - Natural language-like syntax recognition
    - AI-specific constructs (reasoning, implementation, verification)
    - Comprehensive error handling with helpful diagnostics
    - Performance optimized for <100ms compilation target
    """
    
    def __init__(self, source: str = "", source_file: Optional[str] = None):
        self.source = source
        self.source_file = source_file
        self.position = 0
        self.line = 1
        self.column = 1
        self.indent_stack = [0]
        self.tokens: List[Token] = []
        self.errors: List[str] = []
        
        # Performance optimization: pre-compile regex patterns
        self._compile_patterns()
    
    @classmethod
    def create_for_testing(cls) -> 'RunaLexer':
        """Factory method for creating lexer instances for testing."""
        return cls()
    
    def set_source(self, source: str, source_file: Optional[str] = None):
        """Set source code for tokenization."""
        self.source = source
        self.source_file = source_file
        self.position = 0
        self.line = 1
        self.column = 1
        self.indent_stack = [0]
        self.tokens.clear()
        self.errors.clear()  # Clear errors when setting new source
    
    def _compile_patterns(self):
        """Pre-compile regex patterns for performance optimization."""
        # Keywords mapping (both capitalized and lowercase for flexibility)
        self.keywords = {
            # Core Language - both cases
            'Let': TokenType.LET, 'let': TokenType.LET,
            'Define': TokenType.DEFINE, 'define': TokenType.DEFINE,
            'Set': TokenType.SET, 'set': TokenType.SET,
            'To': TokenType.TO, 'to': TokenType.TO,
            'As': TokenType.AS, 'as': TokenType.AS,
            'Be': TokenType.BE, 'be': TokenType.BE,
            'Containing': TokenType.CONTAINING, 'containing': TokenType.CONTAINING,
            'Process': TokenType.PROCESS, 'process': TokenType.PROCESS,
            'Called': TokenType.CALLED, 'called': TokenType.CALLED,
            'That': TokenType.THAT, 'that': TokenType.THAT,
            'Takes': TokenType.TAKES, 'takes': TokenType.TAKES,
            'Returns': TokenType.RETURNING, 'returns': TokenType.RETURNING,
            'Nothing': TokenType.NULL, 'nothing': TokenType.NULL,
            'And': TokenType.AND, 'and': TokenType.AND,
            'Or': TokenType.OR, 'or': TokenType.OR,
            'Not': TokenType.NOT, 'not': TokenType.NOT,
            'If': TokenType.IF, 'if': TokenType.IF,
            'Otherwise': TokenType.OTHERWISE, 'otherwise': TokenType.OTHERWISE,
            'For': TokenType.FOR, 'for': TokenType.FOR,
            'Each': TokenType.EACH, 'each': TokenType.EACH,
            'While': TokenType.WHILE, 'while': TokenType.WHILE,
            'Return': TokenType.RETURN, 'return': TokenType.RETURN,
            'Returning': TokenType.RETURNING, 'returning': TokenType.RETURNING,
            'Import': TokenType.IMPORT, 'import': TokenType.IMPORT,
            'From': TokenType.FROM, 'from': TokenType.FROM,
            'Export': TokenType.EXPORT, 'export': TokenType.EXPORT,
            'Display': TokenType.DISPLAY, 'display': TokenType.DISPLAY,
            'In': TokenType.IN, 'in': TokenType.IN,
            
            # Natural Language Operators
            'multiplied': TokenType.MULTIPLY,
            'by': TokenType.BY,
            'plus': TokenType.PLUS,
            'minus': TokenType.MINUS,
            'divided': TokenType.DIVIDE,
            'modulo': TokenType.MODULO,
            'power': TokenType.POWER,
            'is': TokenType.IS,
            'equal': TokenType.EQUAL,
            'to': TokenType.TO,
            'greater': TokenType.GREATER,
            'than': TokenType.THAN,
            'less': TokenType.LESS,
            'followed': TokenType.FOLLOWED,
            
            # Control Flow
            'Break': TokenType.BREAK, 'break': TokenType.BREAK,
            'Continue': TokenType.CONTINUE, 'continue': TokenType.CONTINUE,
            'Try': TokenType.TRY, 'try': TokenType.TRY,
            'Catch': TokenType.CATCH, 'catch': TokenType.CATCH,
            'Finally': TokenType.FINALLY, 'finally': TokenType.FINALLY,
            'Throw': TokenType.THROW, 'throw': TokenType.THROW,
            'Raise': TokenType.RAISE, 'raise': TokenType.RAISE,
            
            # Literals
            'True': TokenType.TRUE, 'true': TokenType.TRUE,
            'False': TokenType.FALSE, 'false': TokenType.FALSE,
            'None': TokenType.NULL, 'none': TokenType.NULL,
            
            # Types
            'Void': TokenType.VOID_TYPE, 'void': TokenType.VOID_TYPE,
            'Integer': TokenType.INTEGER_TYPE, 'integer': TokenType.INTEGER_TYPE,
            'Float': TokenType.FLOAT_TYPE, 'float': TokenType.FLOAT_TYPE,
            'String': TokenType.STRING_TYPE, 'string': TokenType.STRING_TYPE,
            'Boolean': TokenType.BOOLEAN_TYPE, 'boolean': TokenType.BOOLEAN_TYPE,
            'List': TokenType.LIST_TYPE, 'list': TokenType.LIST_TYPE,
            'Dictionary': TokenType.DICTIONARY_TYPE, 'dictionary': TokenType.DICTIONARY_TYPE,
            'Function': TokenType.FUNCTION_TYPE, 'function': TokenType.FUNCTION_TYPE,
            
            # AI-specific keywords
            'End_reasoning': TokenType.END_REASONING, 'end_reasoning': TokenType.END_REASONING,
            'Implementation': TokenType.IMPLEMENTATION, 'implementation': TokenType.IMPLEMENTATION,
            'End_implementation': TokenType.END_IMPLEMENTATION, 'end_implementation': TokenType.END_IMPLEMENTATION,
            'Verify': TokenType.VERIFY, 'verify': TokenType.VERIFY,
            'End_verify': TokenType.END_VERIFY, 'end_verify': TokenType.END_VERIFY,
            'Send': TokenType.SEND, 'send': TokenType.SEND,
            'With': TokenType.WITH, 'with': TokenType.WITH,
            'Context': TokenType.CONTEXT, 'context': TokenType.CONTEXT,
            'Task': TokenType.TASK, 'task': TokenType.TASK,
            'Include': TokenType.INCLUDE, 'include': TokenType.INCLUDE,
            'Request': TokenType.REQUEST, 'request': TokenType.REQUEST,
            'Define_ai': TokenType.DEFINE_AI, 'define_ai': TokenType.DEFINE_AI,
            'Agent': TokenType.AGENT, 'agent': TokenType.AGENT,
            'Purpose': TokenType.PURPOSE, 'purpose': TokenType.PURPOSE,
            'Capability': TokenType.CAPABILITY, 'capability': TokenType.CAPABILITY,
            'Modify': TokenType.MODIFY, 'modify': TokenType.MODIFY,
            'Safety': TokenType.SAFETY, 'safety': TokenType.SAFETY,
            'Constraint': TokenType.CONSTRAINT, 'constraint': TokenType.CONSTRAINT,
            'Validation': TokenType.VALIDATION, 'validation': TokenType.VALIDATION,
            'Knowledge': TokenType.KNOWLEDGE, 'knowledge': TokenType.KNOWLEDGE,
            'Query': TokenType.QUERY, 'query': TokenType.QUERY,
            'Graph': TokenType.GRAPH, 'graph': TokenType.GRAPH,
            'Neural': TokenType.NEURAL, 'neural': TokenType.NEURAL,
            'Network': TokenType.NETWORK, 'network': TokenType.NETWORK,
            'Layer': TokenType.LAYER, 'layer': TokenType.LAYER,
            'Activation': TokenType.ACTIVATION, 'activation': TokenType.ACTIVATION,
            'Loss': TokenType.LOSS, 'loss': TokenType.LOSS,
            'Optimizer': TokenType.OPTIMIZER, 'optimizer': TokenType.OPTIMIZER,
            
            # AI Communication keywords
            'Ask': TokenType.ASK, 'ask': TokenType.ASK,
            'Tell': TokenType.TELL, 'tell': TokenType.TELL,
            'Instruct': TokenType.INSTRUCT, 'instruct': TokenType.INSTRUCT,
            'Delegate': TokenType.DELEGATE, 'delegate': TokenType.DELEGATE,
            'Wait': TokenType.WAIT, 'wait': TokenType.WAIT,
            'Broadcast': TokenType.BROADCAST, 'broadcast': TokenType.BROADCAST,
            'Coordinate': TokenType.COORDINATE, 'coordinate': TokenType.COORDINATE,
            'About': TokenType.ABOUT, 'about': TokenType.ABOUT,
            'Relationship': TokenType.RELATIONSHIP, 'relationship': TokenType.RELATIONSHIP,
        }
        
        # Regex patterns for performance
        self.patterns = {
            'whitespace': re.compile(r'\s+'),
            'comment': re.compile(r'#.*'),
            'docstring': re.compile(r'"""[\s\S]*?"""'),
            'string': re.compile(r'"[^"]*"'),
            'integer': re.compile(r'\d+'),
            'float': re.compile(r'\d+\.\d+'),
            'identifier': re.compile(r'[a-zA-Z_][a-zA-Z0-9_]*'),
            'operator': re.compile(r'[+\-*/%=<>!&|^~]+'),
            'delimiter': re.compile(r'[(){}\[\];:,.]'),
            'arrow': re.compile(r'->'),
            'pipe': re.compile(r'\|'),
        }
    
    def tokenize(self, source: Optional[str] = None) -> List[Token]:
        """
        Tokenize the source code into a list of tokens.
        
        Args:
            source: Optional source code to tokenize. If not provided, uses instance source.
            
        Returns:
            List of tokens with comprehensive metadata
            
        Raises:
            LexerError: For lexical errors with detailed context
        """
        if source is not None:
            self.set_source(source)
        
        self.tokens = []
        
        # Handle initial indentation if the file starts with spaces
        if self.source and self.source[0].isspace():
            indent_level = self._calculate_indent()
            self._handle_indentation(indent_level)
        
        while self.position < len(self.source):
            char = self.source[self.position]
            
            # Skip whitespace (but track for indentation)
            if char.isspace():
                self._handle_whitespace()
                continue
            
            # Handle comments
            if char == '#':
                self._handle_comment()
                continue
            
            # Handle docstrings
            if self._peek(3) == '"""':
                self._handle_docstring()
                continue
            
            # Handle strings
            if char == '"' or char == "'":
                self._handle_string()
                continue
            
            # Handle numbers
            if char.isdigit():
                self._handle_number()
                continue
            
            # Handle identifiers and keywords
            if char.isalpha() or char == '_':
                self._handle_identifier()
                continue
            
            # Handle operators and delimiters
            if char in '+-*/%=<>!&|^~(){}[];:,.':
                self._handle_operator_or_delimiter()
                continue
            
            # Handle @ symbols for AI blocks
            if char == '@':
                self._handle_at_symbol()
                continue
            
            # Handle arrows and pipes
            if char == '-' and self._peek(1) == '>':
                self._add_token(TokenType.ARROW, '->')
                self.position += 2
                self.column += 2
                continue
            
            if char == '|':
                self._add_token(TokenType.PIPE, '|')
                self.position += 1
                self.column += 1
                continue
            
            # Unknown character
            self._error(f"Unexpected character: '{char}'")
        
        # Add final dedent tokens for any remaining indentation levels
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            self._add_token(TokenType.DEDENT, '')
        
        # Add EOF token
        self._add_token(TokenType.EOF, '')
        
        return self.tokens
    
    def _handle_whitespace(self):
        """Handle whitespace and track indentation."""
        start_pos = self.position
        start_column = self.column
        
        while (self.position < len(self.source) and 
               self.source[self.position].isspace()):
            char = self.source[self.position]
            
            if char == '\n':
                # Add newline token
                self._add_token(TokenType.NEWLINE, '\n')
                self.line += 1
                self.column = 1
                self.position += 1
                
                # Handle indentation on next line
                if self.position < len(self.source):
                    indent_level = self._calculate_indent()
                    self._handle_indentation(indent_level)
            else:
                self.column += 1
                self.position += 1
    
    def _calculate_indent(self) -> int:
        """Calculate indentation level for current line."""
        indent = 0
        pos = self.position
        
        while pos < len(self.source) and self.source[pos] == ' ':
            indent += 1
            pos += 1
        
        return indent
    
    def _handle_indentation(self, indent_level: int):
        """Handle indentation tokens (INDENT/DEDENT)."""
        current_indent = self.indent_stack[-1]
        
        if indent_level > current_indent:
            # Indent
            self.indent_stack.append(indent_level)
            self._add_token(TokenType.INDENT, '')
        elif indent_level < current_indent:
            # Dedent
            while self.indent_stack[-1] > indent_level:
                self.indent_stack.pop()
                self._add_token(TokenType.DEDENT, '')
            
            if self.indent_stack[-1] != indent_level:
                self._error(f"Inconsistent indentation: expected {self.indent_stack[-1]}, got {indent_level}")
    
    def _handle_comment(self):
        """Handle single-line comments."""
        start_pos = self.position
        start_column = self.column
        
        while (self.position < len(self.source) and 
               self.source[self.position] != '\n'):
            self.position += 1
            self.column += 1
        
        comment = self.source[start_pos:self.position]
        self._add_token(TokenType.COMMENT, comment)
    
    def _handle_docstring(self):
        """Handle multi-line docstrings."""
        start_pos = self.position
        start_column = self.column
        
        # Skip opening """
        self.position += 3
        self.column += 3
        
        # Find closing """
        while self.position < len(self.source):
            if self._peek(3) == '"""':
                self.position += 3
                self.column += 3
                break
            
            char = self.source[self.position]
            if char == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            
            self.position += 1
        else:
            self._error("Unterminated docstring")
        
        docstring = self.source[start_pos:self.position]
        self._add_token(TokenType.DOCSTRING, docstring)
    
    def _handle_string(self):
        """Handle string literals."""
        start_pos = self.position
        start_column = self.column
        quote_char = self.source[self.position]  # Get the quote character (' or ")
        
        # Skip opening quote
        self.position += 1
        self.column += 1
        
        # Find closing quote
        while (self.position < len(self.source) and 
               self.source[self.position] != quote_char):
            char = self.source[self.position]
            if char == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            
            self.position += 1
        
        if self.position >= len(self.source):
            self._error("Unterminated string")
        
        # Skip closing quote
        self.position += 1
        self.column += 1
        
        string_value = self.source[start_pos:self.position]
        self._add_token(TokenType.STRING, string_value)
    
    def _handle_number(self):
        """Handle numeric literals (integers and floats)."""
        start_pos = self.position
        start_column = self.column
        
        # Check for float
        is_float = False
        
        while (self.position < len(self.source) and 
               (self.source[self.position].isdigit() or 
                self.source[self.position] == '.')):
            if self.source[self.position] == '.':
                if is_float:
                    self._error("Invalid number: multiple decimal points")
                is_float = True
            
            self.position += 1
            self.column += 1
        
        number_value = self.source[start_pos:self.position]
        token_type = TokenType.FLOAT if is_float else TokenType.INTEGER
        self._add_token(token_type, number_value)
    
    def _handle_identifier(self):
        """Handle identifiers and keywords."""
        start_pos = self.position
        start_column = self.column
        
        while (self.position < len(self.source) and 
               (self.source[self.position].isalnum() or 
                self.source[self.position] == '_')):
            self.position += 1
            self.column += 1
        
        identifier = self.source[start_pos:self.position]
        
        # Check for multi-word natural language operators
        if identifier == "followed":
            # Look ahead for "by"
            if self._peek(3) == " by":
                self.position += 3
                self.column += 3
                self._add_token(TokenType.FOLLOWED, "followed by")
                return
        
        # Check if it's a keyword (case-sensitive)
        if identifier in self.keywords:
            token_type = self.keywords[identifier]
            # Special handling for boolean literals
            if token_type == TokenType.BOOLEAN:
                self._add_token(token_type, identifier.lower())
            else:
                self._add_token(token_type, identifier)
        else:
            # Check if it's a type identifier (starts with capital letter)
            if identifier[0].isupper():
                self._add_token(TokenType.TYPE_IDENTIFIER, identifier)
            else:
                self._add_token(TokenType.IDENTIFIER, identifier)
    
    def _handle_operator_or_delimiter(self):
        """Handle operators and delimiters."""
        char = self.source[self.position]
        
        # Single character delimiters
        delimiter_map = {
            '(': TokenType.LEFT_PAREN,
            ')': TokenType.RIGHT_PAREN,
            '[': TokenType.LEFT_BRACKET,
            ']': TokenType.RIGHT_BRACKET,
            '{': TokenType.LEFT_BRACE,
            '}': TokenType.RIGHT_BRACE,
            ';': TokenType.SEMICOLON,
            ':': TokenType.COLON,
            ',': TokenType.COMMA,
            '.': TokenType.DOT,
        }
        
        if char in delimiter_map:
            self._add_token(delimiter_map[char], char)
            self.position += 1
            self.column += 1
            return
        
        # Multi-character operators
        operator_map = {
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '*': TokenType.MULTIPLY,
            '/': TokenType.DIVIDE,
            '%': TokenType.MODULO,
            '**': TokenType.POWER,
            '=': TokenType.ASSIGN,
            '==': TokenType.EQUALS,
            '!=': TokenType.NOT_EQUALS,
            '<': TokenType.LESS_THAN,
            '<=': TokenType.LESS_EQUALS,
            '>': TokenType.GREATER_THAN,
            '>=': TokenType.GREATER_EQUALS,
            '&&': TokenType.LOGICAL_AND,
            '||': TokenType.LOGICAL_OR,
            '!': TokenType.LOGICAL_NOT,
            '&': TokenType.BITWISE_AND,
            '|': TokenType.BITWISE_OR,
            '^': TokenType.BITWISE_XOR,
            '~': TokenType.BITWISE_NOT,
            '<<': TokenType.LEFT_SHIFT,
            '>>': TokenType.RIGHT_SHIFT,
        }
        
        # Try multi-character operators first
        for op, token_type in operator_map.items():
            if self._peek(len(op)) == op:
                self._add_token(token_type, op)
                self.position += len(op)
                self.column += len(op)
                return
        
        # Single character operators
        if char in operator_map:
            self._add_token(operator_map[char], char)
            self.position += 1
            self.column += 1
            return
        
        # Unknown character
        self._error(f"Unexpected character: '{char}'")
    
    def _peek(self, length: int) -> str:
        """Peek ahead in the source without advancing position."""
        if self.position + length <= len(self.source):
            return self.source[self.position:self.position + length]
        return ''
    
    def _add_token(self, token_type: TokenType, value: str):
        """Add a token to the token list."""
        token = Token(
            type=token_type,
            value=value,
            line=self.line,
            column=self.column,
            source_file=self.source_file
        )
        self.tokens.append(token)
    
    def _error(self, message: str):
        """Raise a lexer error with detailed context."""
        raise LexerError(message, self.line, self.column, self.source_file)
    
    def _handle_at_symbol(self):
        """Handle @ symbols for AI blocks."""
        start_pos = self.position
        start_column = self.column
        
        # Skip the @ symbol
        self.position += 1
        self.column += 1
        
        # Read the identifier after @
        while (self.position < len(self.source) and 
               (self.source[self.position].isalnum() or 
                self.source[self.position] == '_')):
            self.position += 1
            self.column += 1
        
        identifier = self.source[start_pos + 1:self.position]
        
        # Check for specific AI block keywords
        if identifier == 'reasoning':
            self._add_token(TokenType.REASONING, '@reasoning')
        elif identifier == 'implementation':
            self._add_token(TokenType.IMPLEMENTATION, '@implementation')
        elif identifier == 'verify':
            self._add_token(TokenType.VERIFY, '@verify')
        elif identifier == 'end':
            self._add_token(TokenType.END, '@end')
        else:
            # Generic @ symbol with identifier
            self._add_token(TokenType.AT_SYMBOL, f"@{identifier}") 