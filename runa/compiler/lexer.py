"""
Runa Lexer

Tokenizes Runa source code with natural language syntax support.
Handles multi-word tokens, indentation-based scoping, and natural language operators.

Following the Runa Formal Grammar Specifications exactly.
"""

import re
from typing import List, Iterator, Optional, Tuple
from .tokens import Token, TokenType, KEYWORDS, MULTI_WORD_TOKENS

class LexerError(Exception):
    """Exception raised for lexical analysis errors."""
    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Lexer error at line {line}, column {column}: {message}")

class RunaLexer:
    """
    Lexer for the Runa natural language programming syntax.
    
    Handles:
    - Natural language keywords and multi-word tokens
    - Indentation-based scoping with INDENT/DEDENT tokens
    - String literals with escape sequences
    - Numeric literals (integers and floats)
    - Identifiers following naming conventions
    - Comments using "Note:" syntax
    """
    
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.indent_stack = [0]  # Stack to track indentation levels
        self.tokens: List[Token] = []
        
        # Regex patterns for token recognition
        self.patterns = {
            'whitespace': re.compile(r'[ \t]+'),
            'newline': re.compile(r'\r?\n'),
            'comment': re.compile(r'Note:.*'),
            'string': re.compile(r'"([^"\\]|\\.)*"'),
            'float': re.compile(r'\d+\.\d+'),
            'integer': re.compile(r'\d+'),
            'identifier': re.compile(r'[a-zA-Z_][a-zA-Z0-9_]*'),
            'punctuation': re.compile(r'[:,;.?!()[\]{}|]'),
        }
    
    def current_char(self) -> Optional[str]:
        """Get the current character, or None if at end."""
        if self.position >= len(self.source):
            return None
        return self.source[self.position]
    
    def peek_char(self, offset: int = 1) -> Optional[str]:
        """Peek at a character ahead by offset positions."""
        pos = self.position + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]
    
    def advance(self) -> None:
        """Advance to the next character."""
        if self.position < len(self.source) and self.source[self.position] == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        self.position += 1
    
    def peek_ahead(self, count: int) -> str:
        """Peek ahead count characters."""
        end_pos = min(self.position + count, len(self.source))
        return self.source[self.position:end_pos]
    
    def match_multi_word_token(self) -> Optional[Tuple[TokenType, int]]:
        """Try to match multi-word tokens like 'is greater than'."""
        # Try longest matches first
        for phrase in sorted(MULTI_WORD_TOKENS.keys(), key=len, reverse=True):
            if self.source[self.position:self.position+len(phrase)].lower() == phrase.lower():
                # Check that it's a complete word boundary
                next_pos = self.position + len(phrase)
                if (next_pos >= len(self.source) or 
                    self.source[next_pos] in ' \t\n\r:(),;.[]{}'):
                    token_type = MULTI_WORD_TOKENS[phrase]
                    if isinstance(token_type, tuple):
                        # Return the first token type for compound tokens
                        return token_type[0], len(phrase)
                    return token_type, len(phrase)
        return None
    
    def tokenize_string(self) -> Token:
        """Tokenize a string literal."""
        start_line, start_column = self.line, self.column
        quote_char = self.current_char()
        self.advance()  # Skip opening quote
        
        value = ""
        while self.current_char() and self.current_char() != quote_char:
            if self.current_char() == '\\':
                self.advance()
                # Handle escape sequences
                escape_char = self.current_char()
                if escape_char == 'n':
                    value += '\n'
                elif escape_char == 't':
                    value += '\t'
                elif escape_char == 'r':
                    value += '\r'
                elif escape_char == '\\':
                    value += '\\'
                elif escape_char == '"':
                    value += '"'
                elif escape_char == "'":
                    value += "'"
                else:
                    value += escape_char or ''
                self.advance()
            else:
                value += self.current_char()
                self.advance()
        
        if not self.current_char():
            raise LexerError("Unterminated string literal", start_line, start_column)
        
        self.advance()  # Skip closing quote
        return Token(TokenType.STRING, value, start_line, start_column)
    
    def tokenize_number(self) -> Token:
        """Tokenize a numeric literal (integer or float)."""
        start_line, start_column = self.line, self.column
        
        # Check for float first (contains decimal point)
        float_match = self.patterns['float'].match(self.source, self.position)
        if float_match:
            value = float_match.group()
            for _ in range(len(value)):
                self.advance()
            return Token(TokenType.FLOAT, float(value), start_line, start_column)
        
        # Otherwise, it's an integer
        int_match = self.patterns['integer'].match(self.source, self.position)
        if int_match:
            value = int_match.group()
            for _ in range(len(value)):
                self.advance()
            return Token(TokenType.INTEGER, int(value), start_line, start_column)
        
        raise LexerError("Invalid number format", start_line, start_column)
    
    def tokenize_identifier_or_keyword(self) -> Token:
        """Tokenize an identifier or keyword."""
        start_line, start_column = self.line, self.column
        
        # First try multi-word tokens
        multi_word = self.match_multi_word_token()
        if multi_word:
            token_type, length = multi_word
            value = self.source[self.position:self.position + length]
            for _ in range(length):
                self.advance()
            return Token(token_type, value, start_line, start_column)
        
        # Check for specific multi-word identifier patterns
        multi_word_patterns = [
            "user name", "user age", "tax rate", "total price", 
            "shopping cart", "file name", "last name", "first name"
        ]
        
        for pattern in multi_word_patterns:
            if (self.source[self.position:self.position+len(pattern)] == pattern and
                (self.position + len(pattern) >= len(self.source) or 
                 self.source[self.position + len(pattern)] in ' \t\n\r:(),;.[]{}beisgrlto')):
                # It's the pattern followed by a delimiter or keyword
                for _ in range(len(pattern)):
                    self.advance()
                return Token(TokenType.IDENTIFIER, pattern, start_line, start_column)
        
        # Single word identifier/keyword
        identifier_match = self.patterns['identifier'].match(self.source, self.position)
        if identifier_match:
            value = identifier_match.group()
            for _ in range(len(value)):
                self.advance()
            
            # Check if it's a keyword
            if value in KEYWORDS:
                token_type = KEYWORDS[value]
                # Handle boolean literals specially
                if token_type == TokenType.BOOLEAN:
                    bool_value = value.lower() == 'true'
                    return Token(TokenType.BOOLEAN, bool_value, start_line, start_column)
                return Token(token_type, value, start_line, start_column)
            
            # It's an identifier  
            return Token(TokenType.IDENTIFIER, value, start_line, start_column)
        
        raise LexerError(f"Invalid identifier: {self.current_char()}", start_line, start_column)
    

    
    def handle_indentation(self, indent_level: int) -> List[Token]:
        """Handle indentation changes and generate INDENT/DEDENT tokens."""
        tokens = []
        current_indent = self.indent_stack[-1]
        
        if indent_level > current_indent:
            # Increase in indentation
            self.indent_stack.append(indent_level)
            tokens.append(Token(TokenType.INDENT, indent_level, self.line, 1))
        elif indent_level < current_indent:
            # Decrease in indentation - may need multiple DEDENTs
            while self.indent_stack and self.indent_stack[-1] > indent_level:
                self.indent_stack.pop()
                tokens.append(Token(TokenType.DEDENT, indent_level, self.line, 1))
            
            if not self.indent_stack or self.indent_stack[-1] != indent_level:
                raise LexerError("Inconsistent indentation", self.line, 1)
        
        return tokens
    
    def tokenize(self) -> List[Token]:
        """
        Tokenize the entire source code.
        
        Returns:
            List of tokens representing the source code
            
        Raises:
            LexerError: If lexical analysis fails
        """
        self.tokens = []
        
        while self.position < len(self.source):
            # Handle newlines and indentation
            if self.current_char() == '\n':
                # Add newline token
                self.tokens.append(Token(TokenType.NEWLINE, '\n', self.line, self.column))
                self.advance()
                
                # Check indentation on next line
                if self.position < len(self.source):
                    indent_level = 0
                    while (self.position < len(self.source) and 
                           self.current_char() in ' \t'):
                        if self.current_char() == ' ':
                            indent_level += 1
                        elif self.current_char() == '\t':
                            indent_level += 4  # Tab = 4 spaces
                        self.advance()
                    
                    # Skip empty lines
                    if (self.position < len(self.source) and 
                        self.current_char() not in '\n\r'):
                        # Handle indentation changes
                        indent_tokens = self.handle_indentation(indent_level)
                        self.tokens.extend(indent_tokens)
                continue
            
            # Skip whitespace (but not newlines)
            if self.current_char() in ' \t':
                self.advance()
                continue
            
            # Handle comments
            if self.source[self.position:].startswith('Note:'):
                comment_match = self.patterns['comment'].match(self.source, self.position)
                if comment_match:
                    # Skip the entire comment
                    for _ in range(len(comment_match.group())):
                        self.advance()
                continue
            
            # Handle string literals
            if self.current_char() in '"\'':
                self.tokens.append(self.tokenize_string())
                continue
            
            # Handle numeric literals
            if self.current_char().isdigit():
                self.tokens.append(self.tokenize_number())
                continue
            
            # Handle punctuation
            if self.current_char() in '(),;.?![]{}:':
                char = self.current_char()
                token_type = {
                    '(': TokenType.LPAREN,
                    ')': TokenType.RPAREN,
                    '[': TokenType.LBRACKET,
                    ']': TokenType.RBRACKET,
                    '{': TokenType.LBRACE,
                    '}': TokenType.RBRACE,
                    ':': TokenType.COLON,
                    ',': TokenType.COMMA,
                    '.': TokenType.DOT,
                    ';': TokenType.SEMICOLON,
                    '?': TokenType.QUESTION,
                    '!': TokenType.EXCLAMATION,
                }[char]
                
                self.tokens.append(Token(token_type, char, self.line, self.column))
                self.advance()
                continue
            
            # Handle pipe for pattern matching
            if self.current_char() == '|':
                self.tokens.append(Token(TokenType.PIPE, '|', self.line, self.column))
                self.advance()
                continue
            
            # Handle underscore wildcard
            if self.current_char() == '_':
                # Check if it's standalone wildcard or part of identifier
                if (self.peek_char() is None or 
                    not self.peek_char().isalnum()):
                    self.tokens.append(Token(TokenType.WILDCARD, '_', self.line, self.column))
                    self.advance()
                    continue
            
            # Handle identifiers and keywords
            if self.current_char().isalpha() or self.current_char() == '_':
                self.tokens.append(self.tokenize_identifier_or_keyword())
                continue
            
            # Unknown character
            raise LexerError(f"Unexpected character: {self.current_char()}", 
                           self.line, self.column)
        
        # Add final DEDENTs to close all indentation levels
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            self.tokens.append(Token(TokenType.DEDENT, 0, self.line, self.column))
        
        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        
        return self.tokens
    
    def __iter__(self) -> Iterator[Token]:
        """Allow iteration over tokens."""
        if not self.tokens:
            self.tokenize()
        return iter(self.tokens) 