#!/usr/bin/env python3
"""
HTML Parser and Lexer

Comprehensive HTML parsing implementation supporting HTML5 specification
with flexible parsing modes for real-world HTML.

Author: Sybertnetics AI Solutions
License: MIT
"""

import re
from typing import List, Optional, Dict, Any, Union, Tuple
from dataclasses import dataclass
from enum import Enum, auto
import logging

from .html_ast import *


class HtmlTokenType(Enum):
    """HTML token types."""
    # Structure
    DOCTYPE = auto()
    START_TAG = auto()
    END_TAG = auto()
    SELF_CLOSING_TAG = auto()
    
    # Content
    TEXT = auto()
    COMMENT = auto()
    CDATA = auto()
    
    # Components
    TAG_NAME = auto()
    ATTRIBUTE_NAME = auto()
    ATTRIBUTE_VALUE = auto()
    
    # Special
    EOF = auto()
    WHITESPACE = auto()


@dataclass
class HtmlToken:
    """HTML token."""
    type: HtmlTokenType
    value: str
    line: int
    column: int
    attributes: Dict[str, str] = None
    is_self_closing: bool = False


class HtmlLexer:
    """HTML lexer for tokenizing HTML text."""
    
    def __init__(self, strict_mode: bool = False):
        self.strict_mode = strict_mode
        self.reset()
    
    def reset(self):
        """Reset lexer state."""
        self.tokens = []
        self.current_line = 1
        self.current_column = 1
        self.pos = 0
        self.text = ""
    
    def tokenize(self, text: str) -> List[HtmlToken]:
        """Tokenize HTML text."""
        self.reset()
        self.text = text
        
        while self.pos < len(self.text):
            if self._match('<!DOCTYPE') or self._match('<!doctype'):
                self._tokenize_doctype()
            elif self._match('<!--'):
                self._tokenize_comment()
            elif self._match('<![CDATA['):
                self._tokenize_cdata()
            elif self._match('</'):
                self._tokenize_end_tag()
            elif self._match('<'):
                self._tokenize_start_tag()
            else:
                self._tokenize_text()
        
        self._add_token(HtmlTokenType.EOF, '')
        return self.tokens
    
    def _match(self, pattern: str) -> bool:
        """Check if text at current position matches pattern (case-insensitive)."""
        return self.text[self.pos:self.pos + len(pattern)].lower() == pattern.lower()
    
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
    
    def _read_until(self, delimiter: str) -> str:
        """Read text until delimiter is found."""
        start_pos = self.pos
        while self.pos < len(self.text):
            if self._match(delimiter):
                break
            self._advance()
        
        return self.text[start_pos:self.pos]
    
    def _read_quoted_string(self, quote_char: str) -> str:
        """Read quoted string."""
        self._advance()  # Skip opening quote
        value = ""
        
        while self.pos < len(self.text):
            char = self._peek()
            if char == quote_char:
                self._advance()  # Skip closing quote
                break
            elif char == '\\' and not self.strict_mode:
                self._advance()  # Skip escape char
                escaped = self._advance()
                value += escaped
            else:
                value += self._advance()
        
        return value
    
    def _tokenize_doctype(self):
        """Tokenize DOCTYPE declaration."""
        start_pos = self.pos
        self._read_until('>')
        if self._peek() == '>':
            self.pos += 1  # Skip >
        
        declaration = self.text[start_pos:self.pos]
        self._add_token(HtmlTokenType.DOCTYPE, declaration)
    
    def _tokenize_comment(self):
        """Tokenize HTML comment."""
        self.pos += 4  # Skip <!--
        content = self._read_until('-->')
        self.pos += 3  # Skip -->
        
        self._add_token(HtmlTokenType.COMMENT, content)
    
    def _tokenize_cdata(self):
        """Tokenize CDATA section."""
        self.pos += 9  # Skip <![CDATA[
        content = self._read_until(']]>')
        self.pos += 3  # Skip ]]>
        
        self._add_token(HtmlTokenType.CDATA, content)
    
    def _tokenize_start_tag(self):
        """Tokenize start tag."""
        self._advance()  # Skip <
        
        # Read tag name
        tag_name = ""
        while self.pos < len(self.text) and self._peek() not in ' \t\n\r/>':
            tag_name += self._advance()
        
        if not tag_name:
            return
        
        # Parse attributes
        attributes = {}
        self._skip_whitespace()
        
        while self.pos < len(self.text) and self._peek() not in '/>':
            # Read attribute name
            attr_name = ""
            while self.pos < len(self.text) and self._peek() not in ' \t\n\r=/>':
                attr_name += self._advance()
            
            if not attr_name:
                break
            
            self._skip_whitespace()
            
            # Check for attribute value
            attr_value = ""
            if self._peek() == '=':
                self._advance()  # Skip =
                self._skip_whitespace()
                
                # Read attribute value
                quote_char = self._peek()
                if quote_char in ('"', "'"):
                    attr_value = self._read_quoted_string(quote_char)
                else:
                    # Unquoted value (common in real-world HTML)
                    while self.pos < len(self.text) and self._peek() not in ' \t\n\r/>':
                        attr_value += self._advance()
            
            attributes[attr_name.lower()] = attr_value
            self._skip_whitespace()
        
        # Check if self-closing
        is_self_closing = False
        if self._peek() == '/':
            is_self_closing = True
            self._advance()
        
        if self._peek() == '>':
            self._advance()
        
        # Check if this is a void element
        tag_lower = tag_name.lower()
        if tag_lower in HTML5_VOID_ELEMENTS:
            is_self_closing = True
        
        token_type = HtmlTokenType.SELF_CLOSING_TAG if is_self_closing else HtmlTokenType.START_TAG
        self._add_token(token_type, tag_name.lower(), attributes, is_self_closing)
    
    def _tokenize_end_tag(self):
        """Tokenize end tag."""
        self.pos += 2  # Skip </
        
        tag_name = ""
        while self.pos < len(self.text) and self._peek() not in ' \t\n\r>':
            tag_name += self._advance()
        
        self._skip_whitespace()
        
        if self._peek() == '>':
            self._advance()
        
        self._add_token(HtmlTokenType.END_TAG, tag_name.lower())
    
    def _tokenize_text(self):
        """Tokenize text content."""
        text = ""
        
        while self.pos < len(self.text) and self._peek() != '<':
            text += self._advance()
        
        if text:
            self._add_token(HtmlTokenType.TEXT, text)
    
    def _skip_whitespace(self):
        """Skip whitespace characters."""
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self._advance()
    
    def _add_token(self, token_type: HtmlTokenType, value: str, 
                   attributes: Dict[str, str] = None, is_self_closing: bool = False):
        """Add token to list."""
        self.tokens.append(HtmlToken(
            type=token_type,
            value=value,
            line=self.current_line,
            column=self.current_column,
            attributes=attributes or {},
            is_self_closing=is_self_closing
        ))


class HtmlParser:
    """HTML parser with support for both strict and lenient parsing."""
    
    def __init__(self, strict_mode: bool = False, auto_close_tags: bool = True):
        self.strict_mode = strict_mode
        self.auto_close_tags = auto_close_tags
        self.tokens = []
        self.pos = 0
        self.logger = logging.getLogger(__name__)
        self.tag_stack = []
    
    def parse(self, text: str) -> HtmlDocument:
        """Parse HTML text into AST."""
        try:
            lexer = HtmlLexer(self.strict_mode)
            self.tokens = lexer.tokenize(text)
            self.pos = 0
            self.tag_stack = []
            
            document = HtmlDocument()
            
            # Parse document components
            while not self._is_at_end():
                if self._match(HtmlTokenType.DOCTYPE):
                    document.doctype = self._parse_doctype()
                elif self._match(HtmlTokenType.COMMENT):
                    document.comments.append(self._parse_comment())
                elif self._match(HtmlTokenType.START_TAG, HtmlTokenType.SELF_CLOSING_TAG):
                    # First element becomes root
                    if document.root_element is None:
                        document.root_element = self._parse_element()
                    else:
                        # Multiple root elements - wrap in html if not already html
                        if document.root_element.tag_name != 'html':
                            html_element = create_html_element('html')
                            html_element.add_child(document.root_element)
                            document.root_element = html_element
                        document.root_element.add_child(self._parse_element())
                else:
                    self._advance()
            
            # If no root element found, create a basic HTML structure
            if document.root_element is None:
                document.root_element = create_html_element('html')
                body = create_html_element('body')
                body.add_child(create_html_text("Empty HTML document"))
                document.root_element.add_child(body)
            
            return document
            
        except Exception as e:
            self.logger.error(f"HTML parsing failed: {e}")
            raise RuntimeError(f"Failed to parse HTML: {e}")
    
    def _current_token(self) -> HtmlToken:
        """Get current token."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return HtmlToken(HtmlTokenType.EOF, '', 0, 0)
    
    def _advance(self) -> HtmlToken:
        """Advance to next token."""
        token = self._current_token()
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return token
    
    def _match(self, *types: HtmlTokenType) -> bool:
        """Check if current token matches any of the given types."""
        return self._current_token().type in types
    
    def _is_at_end(self) -> bool:
        """Check if at end of tokens."""
        return self._match(HtmlTokenType.EOF)
    
    def _parse_doctype(self) -> HtmlDoctype:
        """Parse DOCTYPE declaration."""
        token = self._advance()
        
        # Extract doctype string (simplified)
        declaration = token.value.lower()
        if 'html' in declaration:
            return HtmlDoctype(doctype_string="html")
        else:
            return HtmlDoctype(doctype_string=declaration)
    
    def _parse_comment(self) -> HtmlComment:
        """Parse HTML comment."""
        token = self._advance()
        return HtmlComment(content=token.value)
    
    def _parse_element(self) -> HtmlElement:
        """Parse HTML element."""
        token = self._advance()
        tag_name = token.value.lower()
        
        element = HtmlElement(
            tag_name=tag_name,
            is_void_element=tag_name in HTML5_VOID_ELEMENTS,
            is_self_closing=token.is_self_closing
        )
        
        # Add attributes
        for attr_name, attr_value in token.attributes.items():
            element.attributes[attr_name] = HtmlAttribute(
                name=attr_name,
                value=html_unescape(attr_value),
                is_boolean=attr_value == ""
            )
        
        # Handle self-closing or void elements
        if element.is_self_closing or element.is_void_element:
            return element
        
        # Parse children
        self.tag_stack.append(tag_name)
        
        while not self._is_at_end():
            if self._match(HtmlTokenType.END_TAG):
                end_token = self._current_token()
                if end_token.value.lower() == tag_name:
                    self._advance()
                    break
                elif self.auto_close_tags and end_token.value.lower() in self.tag_stack:
                    # Auto-close intervening tags
                    break
                else:
                    # Skip unmatched end tag
                    self._advance()
            elif self._match(HtmlTokenType.START_TAG, HtmlTokenType.SELF_CLOSING_TAG):
                child_element = self._parse_element()
                element.add_child(child_element)
            elif self._match(HtmlTokenType.TEXT):
                text_token = self._advance()
                text_content = html_unescape(text_token.value)
                if text_content.strip() or element.tag_name in ['pre', 'script', 'style']:
                    element.add_child(HtmlText(content=text_content))
            elif self._match(HtmlTokenType.COMMENT):
                element.add_child(self._parse_comment())
            elif self._match(HtmlTokenType.CDATA):
                cdata_token = self._advance()
                element.add_child(HtmlText(content=cdata_token.value))
            else:
                self._advance()
        
        if self.tag_stack and self.tag_stack[-1] == tag_name:
            self.tag_stack.pop()
        
        return element


# Convenience functions
def parse_html(text: str, strict_mode: bool = False) -> HtmlDocument:
    """Parse HTML text into AST."""
    parser = HtmlParser(strict_mode)
    return parser.parse(text)


def parse_html_file(file_path: str, strict_mode: bool = False) -> HtmlDocument:
    """Parse HTML file into AST."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return parse_html(f.read(), strict_mode)


def parse_html_fragment(text: str) -> HtmlElement:
    """Parse HTML fragment (single element) into AST."""
    # Wrap fragment in a div for parsing
    wrapped = f"<div>{text}</div>"
    document = parse_html(wrapped)
    
    if document.root_element and document.root_element.children:
        # Return first child element
        for child in document.root_element.children:
            if isinstance(child, HtmlElement):
                return child
    
    raise ValueError("No element found in fragment")


def validate_html_syntax(text: str, strict_mode: bool = False) -> Tuple[bool, Optional[str]]:
    """Validate HTML syntax."""
    try:
        parse_html(text, strict_mode)
        return True, None
    except Exception as e:
        return False, str(e)


def extract_html_text(text: str) -> str:
    """Extract text content from HTML."""
    try:
        document = parse_html(text)
        if document.root_element:
            return document.root_element.get_text_content()
        return ""
    except:
        # Fallback: simple regex-based text extraction
        import re
        text_without_tags = re.sub(r'<[^>]+>', '', text)
        return html_unescape(text_without_tags)


def extract_html_links(text: str) -> List[str]:
    """Extract all links from HTML."""
    try:
        document = parse_html(text)
        links = []
        
        if document.root_element:
            link_elements = document.root_element.find_descendants_by_tag('a')
            for link in link_elements:
                href_attr = link.get_attribute('href')
                if href_attr:
                    links.append(href_attr.value)
        
        return links
    except:
        return []


def extract_html_images(text: str) -> List[Dict[str, str]]:
    """Extract all images from HTML."""
    try:
        document = parse_html(text)
        images = []
        
        if document.root_element:
            img_elements = document.root_element.find_descendants_by_tag('img')
            for img in img_elements:
                img_data = {}
                src_attr = img.get_attribute('src')
                alt_attr = img.get_attribute('alt')
                
                if src_attr:
                    img_data['src'] = src_attr.value
                if alt_attr:
                    img_data['alt'] = alt_attr.value
                
                if img_data:
                    images.append(img_data)
        
        return images
    except:
        return []


def normalize_html_whitespace(text: str) -> str:
    """Normalize whitespace in HTML text."""
    # Preserve whitespace in pre, script, style elements
    preserve_tags = ['pre', 'script', 'style']
    
    try:
        document = parse_html(text)
        if document.root_element:
            _normalize_element_whitespace(document.root_element, preserve_tags)
            from .html_generator import generate_html_code
            return generate_html_code(document)
    except:
        pass
    
    return text


def _normalize_element_whitespace(element: HtmlElement, preserve_tags: List[str]):
    """Normalize whitespace in element and children."""
    if element.tag_name.lower() in preserve_tags:
        return
    
    normalized_children = []
    for child in element.children:
        if isinstance(child, HtmlText):
            normalized_content = ' '.join(child.content.split())
            if normalized_content:
                normalized_children.append(HtmlText(content=normalized_content))
        elif isinstance(child, HtmlElement):
            _normalize_element_whitespace(child, preserve_tags)
            normalized_children.append(child)
        else:
            normalized_children.append(child)
    
    element.children = normalized_children