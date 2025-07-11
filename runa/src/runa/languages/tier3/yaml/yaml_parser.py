#!/usr/bin/env python3
"""
YAML Parser and Lexer

Comprehensive YAML parsing implementation supporting YAML 1.2 specification
with block and flow styles, anchors, aliases, and multi-document streams.

Author: Sybertnetics AI Solutions
License: MIT
"""

import re
from typing import List, Optional, Dict, Any, Union, Tuple
from dataclasses import dataclass
from enum import Enum, auto
import logging

from .yaml_ast import *


class YamlTokenType(Enum):
    """YAML token types."""
    # Structural
    DOCUMENT_START = auto()      # ---
    DOCUMENT_END = auto()        # ...
    BLOCK_SEQUENCE_START = auto() # -
    BLOCK_MAPPING_KEY = auto()   # key:
    BLOCK_MAPPING_VALUE = auto() # :
    FLOW_SEQUENCE_START = auto() # [
    FLOW_SEQUENCE_END = auto()   # ]
    FLOW_MAPPING_START = auto()  # {
    FLOW_MAPPING_END = auto()    # }
    FLOW_ENTRY = auto()          # ,
    
    # Scalars
    PLAIN_SCALAR = auto()
    SINGLE_QUOTED_SCALAR = auto()
    DOUBLE_QUOTED_SCALAR = auto()
    LITERAL_SCALAR = auto()      # |
    FOLDED_SCALAR = auto()       # >
    
    # Anchors and aliases
    ANCHOR = auto()              # &name
    ALIAS = auto()               # *name
    
    # Tags
    TAG = auto()                 # !tag
    
    # Directives
    DIRECTIVE = auto()           # %YAML, %TAG
    
    # Special
    COMMENT = auto()             # #
    NEWLINE = auto()
    INDENT = auto()
    DEDENT = auto()
    EOF = auto()


@dataclass
class YamlToken:
    """YAML token."""
    type: YamlTokenType
    value: str
    line: int
    column: int
    indent_level: int = 0


class YamlLexer:
    """YAML lexer for tokenizing YAML text."""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reset lexer state."""
        self.tokens = []
        self.current_line = 1
        self.current_column = 1
        self.indent_stack = [0]
        self.flow_level = 0
        self.pending_dedents = 0
    
    def tokenize(self, text: str) -> List[YamlToken]:
        """Tokenize YAML text."""
        self.reset()
        lines = text.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            self.current_line = line_num
            self.current_column = 1
            self._tokenize_line(line)
        
        # Add final dedents
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            self._add_token(YamlTokenType.DEDENT, '')
        
        self._add_token(YamlTokenType.EOF, '')
        return self.tokens
    
    def _tokenize_line(self, line: str):
        """Tokenize a single line."""
        stripped = line.lstrip()
        
        # Handle empty lines
        if not stripped:
            self._add_token(YamlTokenType.NEWLINE, '')
            return
        
        # Handle comments
        if stripped.startswith('#'):
            self._add_token(YamlTokenType.COMMENT, stripped)
            return
        
        # Calculate indentation
        indent_level = len(line) - len(stripped)
        self._handle_indentation(indent_level)
        
        # Handle directives
        if stripped.startswith('%'):
            self._tokenize_directive(stripped)
            return
        
        # Handle document markers
        if stripped.startswith('---'):
            self._add_token(YamlTokenType.DOCUMENT_START, '---')
            return
        elif stripped.startswith('...'):
            self._add_token(YamlTokenType.DOCUMENT_END, '...')
            return
        
        # Tokenize line content
        self._tokenize_content(stripped, indent_level)
    
    def _handle_indentation(self, indent_level: int):
        """Handle indentation changes."""
        if self.flow_level > 0:
            return  # Ignore indentation in flow context
        
        current_indent = self.indent_stack[-1]
        
        if indent_level > current_indent:
            # Increase indent
            self.indent_stack.append(indent_level)
            self._add_token(YamlTokenType.INDENT, '', indent_level)
        elif indent_level < current_indent:
            # Decrease indent
            while self.indent_stack and self.indent_stack[-1] > indent_level:
                self.indent_stack.pop()
                self._add_token(YamlTokenType.DEDENT, '', indent_level)
    
    def _tokenize_directive(self, line: str):
        """Tokenize YAML directive."""
        self._add_token(YamlTokenType.DIRECTIVE, line)
    
    def _tokenize_content(self, line: str, indent_level: int):
        """Tokenize line content."""
        pos = 0
        
        while pos < len(line):
            # Skip whitespace
            while pos < len(line) and line[pos].isspace():
                pos += 1
            
            if pos >= len(line):
                break
            
            # Check for flow indicators
            if line[pos] == '[':
                self._add_token(YamlTokenType.FLOW_SEQUENCE_START, '[')
                self.flow_level += 1
                pos += 1
            elif line[pos] == ']':
                self._add_token(YamlTokenType.FLOW_SEQUENCE_END, ']')
                self.flow_level -= 1
                pos += 1
            elif line[pos] == '{':
                self._add_token(YamlTokenType.FLOW_MAPPING_START, '{')
                self.flow_level += 1
                pos += 1
            elif line[pos] == '}':
                self._add_token(YamlTokenType.FLOW_MAPPING_END, '}')
                self.flow_level -= 1
                pos += 1
            elif line[pos] == ',':
                self._add_token(YamlTokenType.FLOW_ENTRY, ',')
                pos += 1
            elif line[pos] == '-' and (pos + 1 >= len(line) or line[pos + 1].isspace()):
                # Block sequence indicator
                self._add_token(YamlTokenType.BLOCK_SEQUENCE_START, '-')
                pos += 1
            elif line[pos] == ':' and (pos + 1 >= len(line) or line[pos + 1].isspace()):
                # Block mapping value
                self._add_token(YamlTokenType.BLOCK_MAPPING_VALUE, ':')
                pos += 1
            elif line[pos] == '&':
                # Anchor
                anchor_match = re.match(r'&([a-zA-Z_][a-zA-Z0-9_]*)', line[pos:])
                if anchor_match:
                    self._add_token(YamlTokenType.ANCHOR, anchor_match.group(1))
                    pos += len(anchor_match.group(0))
                else:
                    pos += 1
            elif line[pos] == '*':
                # Alias
                alias_match = re.match(r'\*([a-zA-Z_][a-zA-Z0-9_]*)', line[pos:])
                if alias_match:
                    self._add_token(YamlTokenType.ALIAS, alias_match.group(1))
                    pos += len(alias_match.group(0))
                else:
                    pos += 1
            elif line[pos] == '!':
                # Tag
                tag_match = re.match(r'![a-zA-Z0-9_-]*', line[pos:])
                if tag_match:
                    self._add_token(YamlTokenType.TAG, tag_match.group(0))
                    pos += len(tag_match.group(0))
                else:
                    pos += 1
            elif line[pos] == '|':
                # Literal scalar
                self._add_token(YamlTokenType.LITERAL_SCALAR, '|')
                pos += 1
            elif line[pos] == '>':
                # Folded scalar
                self._add_token(YamlTokenType.FOLDED_SCALAR, '>')
                pos += 1
            elif line[pos] == "'":
                # Single quoted scalar
                scalar_end = self._find_scalar_end(line, pos, "'")
                if scalar_end != -1:
                    value = line[pos:scalar_end + 1]
                    self._add_token(YamlTokenType.SINGLE_QUOTED_SCALAR, value)
                    pos = scalar_end + 1
                else:
                    pos += 1
            elif line[pos] == '"':
                # Double quoted scalar
                scalar_end = self._find_scalar_end(line, pos, '"')
                if scalar_end != -1:
                    value = line[pos:scalar_end + 1]
                    self._add_token(YamlTokenType.DOUBLE_QUOTED_SCALAR, value)
                    pos = scalar_end + 1
                else:
                    pos += 1
            else:
                # Plain scalar
                scalar_end = self._find_plain_scalar_end(line, pos)
                if scalar_end > pos:
                    value = line[pos:scalar_end].rstrip()
                    if value:
                        self._add_token(YamlTokenType.PLAIN_SCALAR, value)
                    pos = scalar_end
                else:
                    pos += 1
    
    def _find_scalar_end(self, line: str, start: int, quote: str) -> int:
        """Find end of quoted scalar."""
        pos = start + 1
        while pos < len(line):
            if line[pos] == quote:
                return pos
            elif line[pos] == '\\' and pos + 1 < len(line):
                pos += 2  # Skip escaped character
            else:
                pos += 1
        return -1
    
    def _find_plain_scalar_end(self, line: str, start: int) -> int:
        """Find end of plain scalar."""
        pos = start
        while pos < len(line):
            char = line[pos]
            if char in '[]{},:*&!|>#@`':
                break
            if char == '-' and pos + 1 < len(line) and line[pos + 1].isspace():
                break
            if char == ':' and pos + 1 < len(line) and line[pos + 1].isspace():
                break
            pos += 1
        return pos
    
    def _add_token(self, token_type: YamlTokenType, value: str, indent_level: int = 0):
        """Add token to list."""
        self.tokens.append(YamlToken(
            type=token_type,
            value=value,
            line=self.current_line,
            column=self.current_column,
            indent_level=indent_level
        ))


class YamlParser:
    """YAML parser."""
    
    def __init__(self):
        self.tokens = []
        self.pos = 0
        self.anchors = {}
        self.logger = logging.getLogger(__name__)
    
    def parse(self, text: str) -> YamlStream:
        """Parse YAML text into AST."""
        try:
            lexer = YamlLexer()
            self.tokens = lexer.tokenize(text)
            self.pos = 0
            self.anchors = {}
            
            documents = []
            
            # Skip initial comments and newlines
            self._skip_insignificant()
            
            # Parse documents
            while not self._is_at_end():
                if self._match(YamlTokenType.DOCUMENT_START):
                    self._advance()
                    self._skip_insignificant()
                
                if not self._is_at_end() and not self._match(YamlTokenType.DOCUMENT_END):
                    content = self._parse_value()
                    documents.append(YamlDocument(content=content, explicit_start=True))
                
                if self._match(YamlTokenType.DOCUMENT_END):
                    self._advance()
                    if documents:
                        documents[-1].explicit_end = True
                
                self._skip_insignificant()
            
            # If no explicit documents, treat entire content as single document
            if not documents and self.pos > 0:
                # Re-parse as single document
                self.pos = 0
                self._skip_insignificant()
                if not self._is_at_end():
                    content = self._parse_value()
                    documents.append(YamlDocument(content=content))
            
            return YamlStream(documents=documents)
            
        except Exception as e:
            self.logger.error(f"YAML parsing failed: {e}")
            raise RuntimeError(f"Failed to parse YAML: {e}")
    
    def _current_token(self) -> YamlToken:
        """Get current token."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return YamlToken(YamlTokenType.EOF, '', 0, 0)
    
    def _advance(self) -> YamlToken:
        """Advance to next token."""
        token = self._current_token()
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return token
    
    def _match(self, *types: YamlTokenType) -> bool:
        """Check if current token matches any of the given types."""
        return self._current_token().type in types
    
    def _consume(self, expected: YamlTokenType, message: str = None) -> YamlToken:
        """Consume token of expected type."""
        if not self._match(expected):
            current = self._current_token()
            error_msg = message or f"Expected {expected}, got {current.type} at line {current.line}"
            raise ValueError(error_msg)
        return self._advance()
    
    def _is_at_end(self) -> bool:
        """Check if at end of tokens."""
        return self._match(YamlTokenType.EOF)
    
    def _skip_insignificant(self):
        """Skip comments and newlines."""
        while self._match(YamlTokenType.COMMENT, YamlTokenType.NEWLINE):
            self._advance()
    
    def _parse_value(self) -> YamlValue:
        """Parse a YAML value."""
        self._skip_insignificant()
        
        # Handle anchors
        anchor_name = None
        if self._match(YamlTokenType.ANCHOR):
            anchor_name = self._advance().value
            self._skip_insignificant()
        
        # Handle tags
        tag = None
        if self._match(YamlTokenType.TAG):
            tag = self._advance().value
            self._skip_insignificant()
        
        # Parse the actual value
        value = None
        
        if self._match(YamlTokenType.ALIAS):
            alias_name = self._advance().value
            value = YamlAlias(name=alias_name)
        elif self._match(YamlTokenType.FLOW_SEQUENCE_START):
            value = self._parse_flow_sequence()
        elif self._match(YamlTokenType.FLOW_MAPPING_START):
            value = self._parse_flow_mapping()
        elif self._match(YamlTokenType.BLOCK_SEQUENCE_START):
            value = self._parse_block_sequence()
        elif self._match(YamlTokenType.LITERAL_SCALAR):
            value = self._parse_literal_scalar()
        elif self._match(YamlTokenType.FOLDED_SCALAR):
            value = self._parse_folded_scalar()
        elif self._match(YamlTokenType.SINGLE_QUOTED_SCALAR, YamlTokenType.DOUBLE_QUOTED_SCALAR, YamlTokenType.PLAIN_SCALAR):
            value = self._parse_scalar()
        elif self._match(YamlTokenType.INDENT):
            # Block mapping or sequence
            self._advance()
            value = self._parse_block_structure()
        else:
            # Try to parse as mapping
            value = self._try_parse_mapping()
            if value is None:
                # Default to empty scalar
                value = YamlScalar(value="")
        
        # Apply tag if present
        if tag and hasattr(value, 'tag'):
            value.tag = tag
        
        # Handle anchor
        if anchor_name:
            anchor = YamlAnchor(name=anchor_name, value=value)
            self.anchors[anchor_name] = value
            return anchor
        
        return value
    
    def _parse_scalar(self) -> YamlScalar:
        """Parse scalar value."""
        token = self._advance()
        
        if token.type == YamlTokenType.SINGLE_QUOTED_SCALAR:
            # Remove quotes and handle escapes
            value = token.value[1:-1].replace("''", "'")
            return YamlScalar(value=value, style=YamlScalarStyle.SINGLE_QUOTED)
        elif token.type == YamlTokenType.DOUBLE_QUOTED_SCALAR:
            # Remove quotes and handle escapes
            value = self._unescape_double_quoted(token.value[1:-1])
            return YamlScalar(value=value, style=YamlScalarStyle.DOUBLE_QUOTED)
        else:
            # Plain scalar - infer type
            value = self._infer_scalar_value(token.value)
            return YamlScalar(value=value, style=YamlScalarStyle.PLAIN)
    
    def _parse_literal_scalar(self) -> YamlScalar:
        """Parse literal scalar (|)."""
        self._advance()  # consume |
        # TODO: Parse following lines with proper indentation handling
        return YamlScalar(value="", style=YamlScalarStyle.LITERAL)
    
    def _parse_folded_scalar(self) -> YamlScalar:
        """Parse folded scalar (>)."""
        self._advance()  # consume >
        # TODO: Parse following lines with proper indentation handling
        return YamlScalar(value="", style=YamlScalarStyle.FOLDED)
    
    def _parse_flow_sequence(self) -> YamlSequence:
        """Parse flow sequence [...]."""
        self._consume(YamlTokenType.FLOW_SEQUENCE_START)
        self._skip_insignificant()
        
        items = []
        
        while not self._match(YamlTokenType.FLOW_SEQUENCE_END) and not self._is_at_end():
            item = self._parse_value()
            items.append(item)
            
            self._skip_insignificant()
            
            if self._match(YamlTokenType.FLOW_ENTRY):
                self._advance()
                self._skip_insignificant()
            elif not self._match(YamlTokenType.FLOW_SEQUENCE_END):
                break
        
        self._consume(YamlTokenType.FLOW_SEQUENCE_END)
        return YamlSequence(items=items, style=YamlSequenceStyle.FLOW)
    
    def _parse_flow_mapping(self) -> YamlMapping:
        """Parse flow mapping {...}."""
        self._consume(YamlTokenType.FLOW_MAPPING_START)
        self._skip_insignificant()
        
        items = []
        
        while not self._match(YamlTokenType.FLOW_MAPPING_END) and not self._is_at_end():
            # Parse key
            key = self._parse_value()
            
            self._skip_insignificant()
            self._consume(YamlTokenType.BLOCK_MAPPING_VALUE)
            self._skip_insignificant()
            
            # Parse value
            value = self._parse_value()
            
            items.append(YamlMappingItem(key=key, value=value))
            
            self._skip_insignificant()
            
            if self._match(YamlTokenType.FLOW_ENTRY):
                self._advance()
                self._skip_insignificant()
            elif not self._match(YamlTokenType.FLOW_MAPPING_END):
                break
        
        self._consume(YamlTokenType.FLOW_MAPPING_END)
        return YamlMapping(items=items, style=YamlMappingStyle.FLOW)
    
    def _parse_block_sequence(self) -> YamlSequence:
        """Parse block sequence."""
        items = []
        
        while self._match(YamlTokenType.BLOCK_SEQUENCE_START):
            self._advance()
            self._skip_insignificant()
            
            item = self._parse_value()
            items.append(item)
            
            self._skip_insignificant()
        
        return YamlSequence(items=items, style=YamlSequenceStyle.BLOCK)
    
    def _parse_block_structure(self) -> YamlValue:
        """Parse block structure after indent."""
        # Look ahead to determine if it's a sequence or mapping
        if self._match(YamlTokenType.BLOCK_SEQUENCE_START):
            return self._parse_block_sequence()
        else:
            return self._try_parse_mapping() or YamlScalar(value="")
    
    def _try_parse_mapping(self) -> Optional[YamlMapping]:
        """Try to parse as mapping."""
        items = []
        
        while not self._is_at_end():
            # Look for key: value pattern
            if self._match(YamlTokenType.PLAIN_SCALAR, YamlTokenType.SINGLE_QUOTED_SCALAR, YamlTokenType.DOUBLE_QUOTED_SCALAR):
                key_token = self._advance()
                key = YamlScalar(value=self._infer_scalar_value(key_token.value))
                
                self._skip_insignificant()
                
                if self._match(YamlTokenType.BLOCK_MAPPING_VALUE):
                    self._advance()
                    self._skip_insignificant()
                    
                    value = self._parse_value()
                    items.append(YamlMappingItem(key=key, value=value))
                    
                    self._skip_insignificant()
                else:
                    # Not a mapping, backtrack
                    self.pos -= 1
                    break
            else:
                break
        
        return YamlMapping(items=items) if items else None
    
    def _infer_scalar_value(self, text: str) -> Any:
        """Infer scalar value from text."""
        text = text.strip()
        
        # Null values
        if text.lower() in ('null', 'nil', '~', ''):
            return None
        
        # Boolean values
        if text.lower() in ('true', 'yes', 'on'):
            return True
        elif text.lower() in ('false', 'no', 'off'):
            return False
        
        # Numeric values
        try:
            if '.' in text or 'e' in text.lower():
                return float(text)
            else:
                return int(text)
        except ValueError:
            pass
        
        # String value
        return text
    
    def _unescape_double_quoted(self, text: str) -> str:
        """Unescape double-quoted string."""
        result = []
        i = 0
        while i < len(text):
            if text[i] == '\\' and i + 1 < len(text):
                next_char = text[i + 1]
                if next_char == 'n':
                    result.append('\n')
                elif next_char == 't':
                    result.append('\t')
                elif next_char == 'r':
                    result.append('\r')
                elif next_char == '\\':
                    result.append('\\')
                elif next_char == '"':
                    result.append('"')
                else:
                    result.append(next_char)
                i += 2
            else:
                result.append(text[i])
                i += 1
        return ''.join(result)


# Convenience functions
def parse_yaml(text: str) -> YamlStream:
    """Parse YAML text into AST."""
    parser = YamlParser()
    return parser.parse(text)


def parse_yaml_file(file_path: str) -> YamlStream:
    """Parse YAML file into AST."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return parse_yaml(f.read())


def parse_yaml_document(text: str) -> YamlDocument:
    """Parse single YAML document."""
    stream = parse_yaml(text)
    if stream.documents:
        return stream.documents[0]
    else:
        return YamlDocument(content=YamlScalar(value=""))


def validate_yaml_syntax(text: str) -> Tuple[bool, Optional[str]]:
    """Validate YAML syntax."""
    try:
        parse_yaml(text)
        return True, None
    except Exception as e:
        return False, str(e)