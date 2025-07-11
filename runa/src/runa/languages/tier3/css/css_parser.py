#!/usr/bin/env python3
"""
CSS Parser and Lexer

Comprehensive CSS parsing implementation supporting CSS3 specification
with error recovery and modern CSS features.

Author: Sybertnetics AI Solutions
License: MIT
"""

import re
from typing import List, Optional, Dict, Any, Union, Tuple
from dataclasses import dataclass
from enum import Enum, auto
import logging

from .css_ast import *


class CssTokenType(Enum):
    """CSS token types."""
    # Identifiers and keywords
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()
    DIMENSION = auto()
    PERCENTAGE = auto()
    HASH = auto()
    URL = auto()
    
    # Operators and punctuation
    COLON = auto()
    SEMICOLON = auto()
    COMMA = auto()
    DOT = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    EQUALS = auto()
    
    # Brackets and braces
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()
    
    # CSS-specific
    AT_KEYWORD = auto()
    IMPORTANT = auto()
    
    # Special
    WHITESPACE = auto()
    COMMENT = auto()
    EOF = auto()


@dataclass
class CssToken:
    """CSS token."""
    type: CssTokenType
    value: str
    line: int
    column: int


class CssLexer:
    """CSS lexer for tokenizing CSS text."""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reset lexer state."""
        self.tokens = []
        self.current_line = 1
        self.current_column = 1
        self.pos = 0
        self.text = ""
    
    def tokenize(self, text: str) -> List[CssToken]:
        """Tokenize CSS text."""
        self.reset()
        self.text = text
        
        while self.pos < len(self.text):
            if self._is_whitespace():
                self._skip_whitespace()
            elif self._match('/*'):
                self._tokenize_comment()
            elif self._match('@'):
                self._tokenize_at_keyword()
            elif self._match('#'):
                self._tokenize_hash()
            elif self._match_string_start():
                self._tokenize_string()
            elif self._match('url('):
                self._tokenize_url()
            elif self._is_number_start():
                self._tokenize_number()
            elif self._is_identifier_start():
                self._tokenize_identifier()
            else:
                self._tokenize_single_char()
        
        self._add_token(CssTokenType.EOF, '')
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
    
    def _match(self, pattern: str) -> bool:
        """Check if text at current position matches pattern."""
        return self.text[self.pos:self.pos + len(pattern)] == pattern
    
    def _is_whitespace(self) -> bool:
        """Check if current character is whitespace."""
        return self.pos < len(self.text) and self.text[self.pos].isspace()
    
    def _is_identifier_start(self) -> bool:
        """Check if current character can start an identifier."""
        char = self._peek()
        return char.isalpha() or char in '_-'
    
    def _is_identifier_char(self) -> bool:
        """Check if current character can be part of an identifier."""
        char = self._peek()
        return char.isalnum() or char in '_-'
    
    def _is_number_start(self) -> bool:
        """Check if current character can start a number."""
        char = self._peek()
        return char.isdigit() or (char == '.' and self._peek(1).isdigit())
    
    def _match_string_start(self) -> bool:
        """Check if at start of string."""
        return self._peek() in ('"', "'")
    
    def _skip_whitespace(self):
        """Skip whitespace characters."""
        while self._is_whitespace():
            self._advance()
    
    def _tokenize_comment(self):
        """Tokenize CSS comment."""
        self._advance()  # Skip /
        self._advance()  # Skip *
        
        comment_text = ""
        while self.pos < len(self.text):
            if self._match('*/'):
                self._advance()  # Skip *
                self._advance()  # Skip /
                break
            comment_text += self._advance()
        
        self._add_token(CssTokenType.COMMENT, comment_text)
    
    def _tokenize_at_keyword(self):
        """Tokenize at-keyword."""
        self._advance()  # Skip @
        
        keyword = ""
        while self._is_identifier_char():
            keyword += self._advance()
        
        self._add_token(CssTokenType.AT_KEYWORD, keyword)
    
    def _tokenize_hash(self):
        """Tokenize hash token (#)."""
        self._advance()  # Skip #
        
        hash_value = ""
        while self._is_identifier_char() or self._peek().isdigit():
            hash_value += self._advance()
        
        self._add_token(CssTokenType.HASH, hash_value)
    
    def _tokenize_string(self):
        """Tokenize string literal."""
        quote_char = self._advance()  # Get quote character
        string_value = ""
        
        while self.pos < len(self.text):
            char = self._peek()
            if char == quote_char:
                self._advance()  # Skip closing quote
                break
            elif char == '\\':
                self._advance()  # Skip escape character
                escaped = self._advance()
                if escaped == 'n':
                    string_value += '\n'
                elif escaped == 't':
                    string_value += '\t'
                elif escaped == 'r':
                    string_value += '\r'
                elif escaped == '\\':
                    string_value += '\\'
                elif escaped == quote_char:
                    string_value += quote_char
                else:
                    string_value += escaped
            else:
                string_value += self._advance()
        
        self._add_token(CssTokenType.STRING, string_value)
    
    def _tokenize_url(self):
        """Tokenize URL function."""
        # Skip 'url('
        for _ in range(4):
            self._advance()
        
        url_value = ""
        while self.pos < len(self.text):
            char = self._peek()
            if char == ')':
                self._advance()  # Skip closing paren
                break
            elif char in ('"', "'"):
                # Handle quoted URL
                quote = self._advance()
                while self.pos < len(self.text) and self._peek() != quote:
                    url_value += self._advance()
                if self._peek() == quote:
                    self._advance()  # Skip closing quote
            else:
                url_value += self._advance()
        
        self._add_token(CssTokenType.URL, url_value.strip())
    
    def _tokenize_number(self):
        """Tokenize number, dimension, or percentage."""
        number_str = ""
        
        # Read integer part
        while self._peek().isdigit():
            number_str += self._advance()
        
        # Read decimal part
        if self._peek() == '.' and self._peek(1).isdigit():
            number_str += self._advance()  # decimal point
            while self._peek().isdigit():
                number_str += self._advance()
        
        # Check for unit or percentage
        if self._peek() == '%':
            self._advance()
            self._add_token(CssTokenType.PERCENTAGE, number_str)
        elif self._is_identifier_start():
            # Read unit
            unit = ""
            while self._is_identifier_char():
                unit += self._advance()
            self._add_token(CssTokenType.DIMENSION, f"{number_str}{unit}")
        else:
            self._add_token(CssTokenType.NUMBER, number_str)
    
    def _tokenize_identifier(self):
        """Tokenize identifier."""
        identifier = ""
        while self._is_identifier_char():
            identifier += self._advance()
        
        # Check for !important
        if identifier == "important" and self.tokens and self.tokens[-1].type == CssTokenType.IMPORTANT:
            # This is part of !important
            self.tokens[-1] = CssToken(CssTokenType.IMPORTANT, "!important", 
                                     self.tokens[-1].line, self.tokens[-1].column)
        else:
            self._add_token(CssTokenType.IDENTIFIER, identifier)
    
    def _tokenize_single_char(self):
        """Tokenize single character tokens."""
        char = self._advance()
        
        single_char_tokens = {
            ':': CssTokenType.COLON,
            ';': CssTokenType.SEMICOLON,
            ',': CssTokenType.COMMA,
            '.': CssTokenType.DOT,
            '+': CssTokenType.PLUS,
            '-': CssTokenType.MINUS,
            '*': CssTokenType.MULTIPLY,
            '/': CssTokenType.DIVIDE,
            '=': CssTokenType.EQUALS,
            '(': CssTokenType.LEFT_PAREN,
            ')': CssTokenType.RIGHT_PAREN,
            '{': CssTokenType.LEFT_BRACE,
            '}': CssTokenType.RIGHT_BRACE,
            '[': CssTokenType.LEFT_BRACKET,
            ']': CssTokenType.RIGHT_BRACKET,
        }
        
        if char == '!' and self._peek().isalpha():
            # Start of !important
            self._add_token(CssTokenType.IMPORTANT, "!")
        elif char in single_char_tokens:
            self._add_token(single_char_tokens[char], char)
        else:
            # Unknown character - skip it
            pass
    
    def _add_token(self, token_type: CssTokenType, value: str):
        """Add token to list."""
        self.tokens.append(CssToken(
            type=token_type,
            value=value,
            line=self.current_line,
            column=self.current_column
        ))


class CssParser:
    """CSS parser."""
    
    def __init__(self):
        self.tokens = []
        self.pos = 0
        self.logger = logging.getLogger(__name__)
    
    def parse(self, text: str) -> CssStylesheet:
        """Parse CSS text into AST."""
        try:
            lexer = CssLexer()
            self.tokens = lexer.tokenize(text)
            self.pos = 0
            
            return self._parse_stylesheet()
            
        except Exception as e:
            self.logger.error(f"CSS parsing failed: {e}")
            raise RuntimeError(f"Failed to parse CSS: {e}")
    
    def _current_token(self) -> CssToken:
        """Get current token."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return CssToken(CssTokenType.EOF, '', 0, 0)
    
    def _advance(self) -> CssToken:
        """Advance to next token."""
        token = self._current_token()
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return token
    
    def _match(self, *types: CssTokenType) -> bool:
        """Check if current token matches any of the given types."""
        return self._current_token().type in types
    
    def _match_value(self, value: str) -> bool:
        """Check if current token has specific value."""
        return self._current_token().value == value
    
    def _is_at_end(self) -> bool:
        """Check if at end of tokens."""
        return self._match(CssTokenType.EOF)
    
    def _skip_whitespace_and_comments(self):
        """Skip whitespace and comment tokens."""
        while self._match(CssTokenType.WHITESPACE, CssTokenType.COMMENT):
            self._advance()
    
    def _parse_stylesheet(self) -> CssStylesheet:
        """Parse CSS stylesheet."""
        stylesheet = CssStylesheet()
        
        self._skip_whitespace_and_comments()
        
        while not self._is_at_end():
            self._skip_whitespace_and_comments()
            
            if self._is_at_end():
                break
            
            if self._match(CssTokenType.AT_KEYWORD):
                at_rule = self._parse_at_rule()
                if at_rule:
                    stylesheet.add_at_rule(at_rule)
            elif self._match(CssTokenType.COMMENT):
                comment = self._parse_comment()
                stylesheet.add_comment(comment)
            else:
                rule = self._parse_rule()
                if rule:
                    stylesheet.add_rule(rule)
            
            self._skip_whitespace_and_comments()
        
        return stylesheet
    
    def _parse_at_rule(self) -> Optional[CssAtRule]:
        """Parse at-rule."""
        if not self._match(CssTokenType.AT_KEYWORD):
            return None
        
        at_keyword = self._advance().value
        
        # Parse parameters
        params = ""
        while not self._match(CssTokenType.LEFT_BRACE, CssTokenType.SEMICOLON, CssTokenType.EOF):
            if self._match(CssTokenType.COMMENT):
                self._advance()
            else:
                token = self._advance()
                params += token.value + " "
        
        params = params.strip()
        
        at_rule = CssAtRule(name=at_keyword, params=params)
        
        # Handle block-based at-rules
        if self._match(CssTokenType.LEFT_BRACE):
            self._advance()  # consume {
            
            # Parse rules inside at-rule
            while not self._match(CssTokenType.RIGHT_BRACE, CssTokenType.EOF):
                self._skip_whitespace_and_comments()
                
                if self._match(CssTokenType.RIGHT_BRACE, CssTokenType.EOF):
                    break
                
                if self._match(CssTokenType.AT_KEYWORD):
                    nested_at_rule = self._parse_at_rule()
                    if nested_at_rule:
                        at_rule.rules.append(CssRule())  # Placeholder
                else:
                    rule = self._parse_rule()
                    if rule:
                        at_rule.rules.append(rule)
            
            if self._match(CssTokenType.RIGHT_BRACE):
                self._advance()  # consume }
        
        elif self._match(CssTokenType.SEMICOLON):
            self._advance()  # consume ;
        
        return at_rule
    
    def _parse_rule(self) -> Optional[CssRule]:
        """Parse CSS rule."""
        # Parse selectors
        selectors = self._parse_selectors()
        if not selectors:
            return None
        
        # Expect opening brace
        if not self._match(CssTokenType.LEFT_BRACE):
            return None
        
        self._advance()  # consume {
        
        # Parse declarations
        declarations = self._parse_declarations()
        
        # Expect closing brace
        if self._match(CssTokenType.RIGHT_BRACE):
            self._advance()  # consume }
        
        rule = CssRule(selectors=selectors, declarations=declarations)
        return rule
    
    def _parse_selectors(self) -> List[CssSelector]:
        """Parse CSS selectors."""
        selectors = []
        
        current_selector = ""
        while not self._match(CssTokenType.LEFT_BRACE, CssTokenType.EOF):
            if self._match(CssTokenType.COMMA):
                if current_selector.strip():
                    selectors.append(CssSelector(text=current_selector.strip()))
                current_selector = ""
                self._advance()  # consume comma
            elif self._match(CssTokenType.COMMENT):
                self._advance()  # skip comment
            else:
                token = self._advance()
                current_selector += token.value
                
                # Add space for readability (except for certain tokens)
                if not self._match(CssTokenType.DOT, CssTokenType.HASH, CssTokenType.COLON, 
                                 CssTokenType.LEFT_BRACKET, CssTokenType.RIGHT_BRACKET):
                    current_selector += " "
        
        # Add final selector
        if current_selector.strip():
            selectors.append(CssSelector(text=current_selector.strip()))
        
        return selectors
    
    def _parse_declarations(self) -> List[CssDeclaration]:
        """Parse CSS declarations."""
        declarations = []
        
        while not self._match(CssTokenType.RIGHT_BRACE, CssTokenType.EOF):
            self._skip_whitespace_and_comments()
            
            if self._match(CssTokenType.RIGHT_BRACE, CssTokenType.EOF):
                break
            
            declaration = self._parse_declaration()
            if declaration:
                declarations.append(declaration)
            
            # Skip semicolon if present
            if self._match(CssTokenType.SEMICOLON):
                self._advance()
            
            self._skip_whitespace_and_comments()
        
        return declarations
    
    def _parse_declaration(self) -> Optional[CssDeclaration]:
        """Parse CSS declaration."""
        # Parse property
        if not self._match(CssTokenType.IDENTIFIER):
            return None
        
        property_name = self._advance().value
        
        # Expect colon
        if not self._match(CssTokenType.COLON):
            return None
        
        self._advance()  # consume :
        self._skip_whitespace_and_comments()
        
        # Parse value
        value_parts = []
        important = False
        
        while not self._match(CssTokenType.SEMICOLON, CssTokenType.RIGHT_BRACE, 
                            CssTokenType.IMPORTANT, CssTokenType.EOF):
            if self._match(CssTokenType.COMMENT):
                self._advance()
                continue
            
            token = self._advance()
            value_parts.append(token.value)
        
        # Check for !important
        if self._match(CssTokenType.IMPORTANT):
            important = True
            self._advance()
            # Skip any additional tokens that might be part of !important
            while self._match(CssTokenType.IDENTIFIER) and self._current_token().value == "important":
                self._advance()
        
        value = " ".join(value_parts).strip()
        
        if property_name and value:
            return CssDeclaration(property=property_name, value=value, important=important)
        
        return None
    
    def _parse_comment(self) -> CssComment:
        """Parse CSS comment."""
        comment_token = self._advance()
        return CssComment(text=comment_token.value)


# Convenience functions
def parse_css(text: str) -> CssStylesheet:
    """Parse CSS text into AST."""
    parser = CssParser()
    return parser.parse(text)


def parse_css_file(file_path: str) -> CssStylesheet:
    """Parse CSS file into AST."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return parse_css(f.read())


def parse_css_rule(text: str) -> Optional[CssRule]:
    """Parse single CSS rule."""
    try:
        stylesheet = parse_css(text)
        return stylesheet.rules[0] if stylesheet.rules else None
    except:
        return None


def parse_css_declaration(text: str) -> Optional[CssDeclaration]:
    """Parse single CSS declaration."""
    try:
        # Wrap in a rule for parsing
        rule_text = f"dummy {{ {text} }}"
        rule = parse_css_rule(rule_text)
        return rule.declarations[0] if rule and rule.declarations else None
    except:
        return None


def validate_css_syntax(text: str) -> Tuple[bool, Optional[str]]:
    """Validate CSS syntax."""
    try:
        parse_css(text)
        return True, None
    except Exception as e:
        return False, str(e)


def extract_css_selectors(text: str) -> List[str]:
    """Extract all selectors from CSS."""
    try:
        stylesheet = parse_css(text)
        selectors = []
        for rule in stylesheet.rules:
            for selector in rule.selectors:
                selectors.append(selector.text)
        return selectors
    except:
        return []


def extract_css_properties(text: str) -> List[str]:
    """Extract all property names from CSS."""
    try:
        stylesheet = parse_css(text)
        properties = set()
        for rule in stylesheet.rules:
            for decl in rule.declarations:
                properties.add(decl.property)
        return list(properties)
    except:
        return []


def minify_css_simple(text: str) -> str:
    """Simple CSS minification."""
    try:
        stylesheet = parse_css(text)
        from .css_generator import generate_css_code, CssCodeStyle
        return generate_css_code(stylesheet, CssCodeStyle.MINIFIED)
    except:
        # Fallback: simple regex-based minification
        minified = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)  # Remove comments
        minified = re.sub(r'\s+', ' ', minified)  # Collapse whitespace
        minified = re.sub(r'\s*{\s*', '{', minified)  # Remove space around {
        minified = re.sub(r'\s*}\s*', '}', minified)  # Remove space around }
        minified = re.sub(r'\s*:\s*', ':', minified)  # Remove space around :
        minified = re.sub(r'\s*;\s*', ';', minified)  # Remove space around ;
        return minified.strip()


def prettify_css_simple(text: str) -> str:
    """Simple CSS prettification."""
    try:
        stylesheet = parse_css(text)
        from .css_generator import generate_css_code, CssCodeStyle
        return generate_css_code(stylesheet, CssCodeStyle.PRETTY)
    except:
        return text