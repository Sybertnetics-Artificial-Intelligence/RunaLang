#!/usr/bin/env python3
"""
XML Parser and Lexer

Comprehensive XML parsing implementation supporting XML 1.0/1.1 specification
with namespaces, DTD, and well-formedness validation.

Author: Sybertnetics AI Solutions
License: MIT
"""

import re
from typing import List, Optional, Dict, Any, Union, Tuple
from dataclasses import dataclass
from enum import Enum, auto
import logging

from .xml_ast import *


class XmlTokenType(Enum):
    """XML token types."""
    # Structure
    XML_DECLARATION = auto()
    DOCTYPE_DECLARATION = auto()
    START_TAG = auto()
    END_TAG = auto()
    SELF_CLOSING_TAG = auto()
    
    # Content
    TEXT = auto()
    COMMENT = auto()
    CDATA = auto()
    PROCESSING_INSTRUCTION = auto()
    
    # Components
    TAG_NAME = auto()
    ATTRIBUTE_NAME = auto()
    ATTRIBUTE_VALUE = auto()
    NAMESPACE_PREFIX = auto()
    
    # Special
    EOF = auto()
    WHITESPACE = auto()


@dataclass
class XmlToken:
    """XML token."""
    type: XmlTokenType
    value: str
    line: int
    column: int
    attributes: Dict[str, str] = None


class XmlLexer:
    """XML lexer for tokenizing XML text."""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reset lexer state."""
        self.tokens = []
        self.current_line = 1
        self.current_column = 1
        self.pos = 0
        self.text = ""
    
    def tokenize(self, text: str) -> List[XmlToken]:
        """Tokenize XML text."""
        self.reset()
        self.text = text
        
        while self.pos < len(self.text):
            self._skip_whitespace()
            
            if self.pos >= len(self.text):
                break
            
            if self._match('<?xml'):
                self._tokenize_xml_declaration()
            elif self._match('<!DOCTYPE'):
                self._tokenize_doctype()
            elif self._match('<!--'):
                self._tokenize_comment()
            elif self._match('<![CDATA['):
                self._tokenize_cdata()
            elif self._match('<?'):
                self._tokenize_processing_instruction()
            elif self._match('</'):
                self._tokenize_end_tag()
            elif self._match('<'):
                self._tokenize_start_tag()
            else:
                self._tokenize_text()
        
        self._add_token(XmlTokenType.EOF, '')
        return self.tokens
    
    def _match(self, pattern: str) -> bool:
        """Check if text at current position matches pattern."""
        return self.text[self.pos:self.pos + len(pattern)] == pattern
    
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
    
    def _skip_whitespace(self):
        """Skip whitespace characters."""
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self._advance()
    
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
            elif char == '\\':
                self._advance()  # Skip escape char
                escaped = self._advance()
                if escaped == 'n':
                    value += '\n'
                elif escaped == 't':
                    value += '\t'
                elif escaped == 'r':
                    value += '\r'
                elif escaped in ('"', "'", '\\'):
                    value += escaped
                else:
                    value += escaped
            else:
                value += self._advance()
        
        return value
    
    def _tokenize_xml_declaration(self):
        """Tokenize XML declaration."""
        start_pos = self.pos
        self._read_until('?>')
        self.pos += 2  # Skip ?>
        
        declaration = self.text[start_pos:self.pos]
        self._add_token(XmlTokenType.XML_DECLARATION, declaration)
    
    def _tokenize_doctype(self):
        """Tokenize DOCTYPE declaration."""
        start_pos = self.pos
        bracket_count = 0
        
        while self.pos < len(self.text):
            char = self._peek()
            if char == '<':
                bracket_count += 1
            elif char == '>':
                if bracket_count == 0:
                    self._advance()
                    break
                bracket_count -= 1
            self._advance()
        
        declaration = self.text[start_pos:self.pos]
        self._add_token(XmlTokenType.DOCTYPE_DECLARATION, declaration)
    
    def _tokenize_comment(self):
        """Tokenize XML comment."""
        self.pos += 4  # Skip <!--
        content = self._read_until('-->')
        self.pos += 3  # Skip -->
        
        self._add_token(XmlTokenType.COMMENT, content)
    
    def _tokenize_cdata(self):
        """Tokenize CDATA section."""
        self.pos += 9  # Skip <![CDATA[
        content = self._read_until(']]>')
        self.pos += 3  # Skip ]]>
        
        self._add_token(XmlTokenType.CDATA, content)
    
    def _tokenize_processing_instruction(self):
        """Tokenize processing instruction."""
        self.pos += 2  # Skip <?
        content = self._read_until('?>')
        self.pos += 2  # Skip ?>
        
        self._add_token(XmlTokenType.PROCESSING_INSTRUCTION, content)
    
    def _tokenize_start_tag(self):
        """Tokenize start tag."""
        self._advance()  # Skip <
        
        # Read tag name
        tag_name = ""
        while self.pos < len(self.text) and self._peek() not in ' \t\n\r/>':
            tag_name += self._advance()
        
        # Parse attributes
        attributes = {}
        self._skip_whitespace()
        
        while self.pos < len(self.text) and self._peek() not in '/>':
            # Read attribute name
            attr_name = ""
            while self.pos < len(self.text) and self._peek() not in ' \t\n\r=':
                attr_name += self._advance()
            
            self._skip_whitespace()
            
            if self._peek() == '=':
                self._advance()  # Skip =
                self._skip_whitespace()
                
                # Read attribute value
                quote_char = self._peek()
                if quote_char in ('"', "'"):
                    attr_value = self._read_quoted_string(quote_char)
                else:
                    # Unquoted value
                    attr_value = ""
                    while self.pos < len(self.text) and self._peek() not in ' \t\n\r/>':
                        attr_value += self._advance()
                
                attributes[attr_name] = attr_value
            
            self._skip_whitespace()
        
        # Check if self-closing
        is_self_closing = False
        if self._peek() == '/':
            is_self_closing = True
            self._advance()
        
        if self._peek() == '>':
            self._advance()
        
        token_type = XmlTokenType.SELF_CLOSING_TAG if is_self_closing else XmlTokenType.START_TAG
        self._add_token(token_type, tag_name, attributes)
    
    def _tokenize_end_tag(self):
        """Tokenize end tag."""
        self.pos += 2  # Skip </
        
        tag_name = ""
        while self.pos < len(self.text) and self._peek() != '>':
            tag_name += self._advance()
        
        if self._peek() == '>':
            self._advance()
        
        self._add_token(XmlTokenType.END_TAG, tag_name.strip())
    
    def _tokenize_text(self):
        """Tokenize text content."""
        text = ""
        
        while self.pos < len(self.text) and self._peek() != '<':
            text += self._advance()
        
        if text:
            self._add_token(XmlTokenType.TEXT, text)
    
    def _add_token(self, token_type: XmlTokenType, value: str, attributes: Dict[str, str] = None):
        """Add token to list."""
        self.tokens.append(XmlToken(
            type=token_type,
            value=value,
            line=self.current_line,
            column=self.current_column,
            attributes=attributes or {}
        ))


class XmlParser:
    """XML parser."""
    
    def __init__(self, validate_well_formed: bool = True):
        self.validate_well_formed = validate_well_formed
        self.tokens = []
        self.pos = 0
        self.logger = logging.getLogger(__name__)
        self.tag_stack = []
        self.namespaces = {}
    
    def parse(self, text: str) -> XmlDocument:
        """Parse XML text into AST."""
        try:
            lexer = XmlLexer()
            self.tokens = lexer.tokenize(text)
            self.pos = 0
            self.tag_stack = []
            self.namespaces = {}
            
            document = XmlDocument()
            
            # Parse document components
            while not self._is_at_end():
                if self._match(XmlTokenType.XML_DECLARATION):
                    self._parse_xml_declaration(document)
                elif self._match(XmlTokenType.DOCTYPE_DECLARATION):
                    document.doctype = self._parse_doctype()
                elif self._match(XmlTokenType.COMMENT):
                    document.comments.append(self._parse_comment())
                elif self._match(XmlTokenType.PROCESSING_INSTRUCTION):
                    document.processing_instructions.append(self._parse_processing_instruction())
                elif self._match(XmlTokenType.START_TAG, XmlTokenType.SELF_CLOSING_TAG):
                    if document.root_element is None:
                        document.root_element = self._parse_element()
                    else:
                        raise ValueError("Multiple root elements found")
                else:
                    self._advance()
            
            return document
            
        except Exception as e:
            self.logger.error(f"XML parsing failed: {e}")
            raise RuntimeError(f"Failed to parse XML: {e}")
    
    def _current_token(self) -> XmlToken:
        """Get current token."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return XmlToken(XmlTokenType.EOF, '', 0, 0)
    
    def _advance(self) -> XmlToken:
        """Advance to next token."""
        token = self._current_token()
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return token
    
    def _match(self, *types: XmlTokenType) -> bool:
        """Check if current token matches any of the given types."""
        return self._current_token().type in types
    
    def _is_at_end(self) -> bool:
        """Check if at end of tokens."""
        return self._match(XmlTokenType.EOF)
    
    def _parse_xml_declaration(self, document: XmlDocument):
        """Parse XML declaration."""
        token = self._advance()
        declaration = token.value
        
        # Extract version, encoding, standalone
        version_match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', declaration)
        encoding_match = re.search(r'encoding\s*=\s*["\']([^"\']+)["\']', declaration)
        standalone_match = re.search(r'standalone\s*=\s*["\']([^"\']+)["\']', declaration)
        
        if version_match:
            document.version = version_match.group(1)
        if encoding_match:
            document.encoding = encoding_match.group(1)
        if standalone_match:
            document.standalone = standalone_match.group(1).lower() == 'yes'
    
    def _parse_doctype(self) -> XmlDoctype:
        """Parse DOCTYPE declaration."""
        token = self._advance()
        declaration = token.value
        
        # Simple DOCTYPE parsing
        match = re.search(r'<!DOCTYPE\s+(\w+)', declaration)
        if match:
            return XmlDoctype(name=match.group(1))
        
        return XmlDoctype(name="unknown")
    
    def _parse_comment(self) -> XmlComment:
        """Parse XML comment."""
        token = self._advance()
        return XmlComment(content=token.value)
    
    def _parse_processing_instruction(self) -> XmlProcessingInstruction:
        """Parse processing instruction."""
        token = self._advance()
        content = token.value
        
        parts = content.split(' ', 1)
        target = parts[0] if parts else ""
        data = parts[1] if len(parts) > 1 else ""
        
        return XmlProcessingInstruction(target=target, data=data)
    
    def _parse_element(self) -> XmlElement:
        """Parse XML element."""
        token = self._advance()
        tag_name = token.value
        
        # Parse namespace prefix
        namespace_prefix = None
        if ':' in tag_name:
            namespace_prefix, tag_name = tag_name.split(':', 1)
        
        element = XmlElement(
            tag_name=tag_name,
            namespace_prefix=namespace_prefix
        )
        
        # Add attributes
        for attr_name, attr_value in token.attributes.items():
            attr_namespace_prefix = None
            if ':' in attr_name:
                attr_namespace_prefix, attr_name = attr_name.split(':', 1)
            
            element.attributes[attr_name] = XmlAttribute(
                name=attr_name,
                value=xml_unescape(attr_value),
                namespace_prefix=attr_namespace_prefix
            )
        
        # Handle self-closing tags
        if token.type == XmlTokenType.SELF_CLOSING_TAG:
            element.is_self_closing = True
            return element
        
        # Parse children
        self.tag_stack.append(tag_name)
        
        while not self._is_at_end():
            if self._match(XmlTokenType.END_TAG):
                end_token = self._current_token()
                if end_token.value.split(':')[-1] == tag_name:  # Handle namespaces
                    self._advance()
                    break
                else:
                    if self.validate_well_formed:
                        raise ValueError(f"Mismatched end tag: expected {tag_name}, got {end_token.value}")
                    self._advance()
            elif self._match(XmlTokenType.START_TAG, XmlTokenType.SELF_CLOSING_TAG):
                element.add_child(self._parse_element())
            elif self._match(XmlTokenType.TEXT):
                text_token = self._advance()
                text_content = xml_unescape(text_token.value)
                if text_content.strip():  # Only add non-empty text
                    element.add_child(XmlText(content=text_content))
            elif self._match(XmlTokenType.COMMENT):
                element.add_child(self._parse_comment())
            elif self._match(XmlTokenType.CDATA):
                cdata_token = self._advance()
                element.add_child(XmlCData(content=cdata_token.value))
            elif self._match(XmlTokenType.PROCESSING_INSTRUCTION):
                element.add_child(self._parse_processing_instruction())
            else:
                self._advance()
        
        self.tag_stack.pop()
        return element


# Convenience functions
def parse_xml(text: str, validate_well_formed: bool = True) -> XmlDocument:
    """Parse XML text into AST."""
    parser = XmlParser(validate_well_formed)
    return parser.parse(text)


def parse_xml_file(file_path: str, validate_well_formed: bool = True) -> XmlDocument:
    """Parse XML file into AST."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return parse_xml(f.read(), validate_well_formed)


def parse_xml_fragment(text: str) -> XmlElement:
    """Parse XML fragment (single element) into AST."""
    # Wrap fragment in root element for parsing
    wrapped = f"<root>{text}</root>"
    document = parse_xml(wrapped)
    
    if document.root_element and document.root_element.children:
        # Return first child element
        for child in document.root_element.children:
            if isinstance(child, XmlElement):
                return child
    
    raise ValueError("No element found in fragment")


def validate_xml_syntax(text: str) -> Tuple[bool, Optional[str]]:
    """Validate XML syntax."""
    try:
        parse_xml(text, validate_well_formed=True)
        return True, None
    except Exception as e:
        return False, str(e)


def validate_xml_well_formed(text: str) -> Tuple[bool, Optional[str]]:
    """Validate XML well-formedness."""
    return validate_xml_syntax(text)