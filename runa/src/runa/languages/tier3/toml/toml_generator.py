#!/usr/bin/env python3
"""
TOML Generator - Clean TOML Code Generation

Provides comprehensive TOML code generation with multiple formatting styles:
- Standard TOML format with proper spacing and alignment
- Compact format for minimal space usage
- Pretty format with enhanced readability
- Development format with extensive comments
- Config format optimized for configuration files

Features:
- Proper table and key-value formatting
- Multi-line string handling
- Array formatting with proper indentation
- Comment preservation and generation
- Key quoting when necessary
- Date/time formatting
- Inline table formatting
"""

from typing import List, Dict, Optional, Any, Union, TextIO
from dataclasses import dataclass
from enum import Enum
import io
import re
from datetime import datetime, date, time

from .toml_ast import *


class TOMLFormatStyle(Enum):
    """TOML code formatting styles"""
    STANDARD = "standard"          # Clean, readable TOML
    COMPACT = "compact"            # Minimal spacing
    PRETTY = "pretty"              # Enhanced readability
    DEVELOPMENT = "development"    # With extensive comments
    CONFIG = "config"              # Optimized for config files


@dataclass
class TOMLGeneratorConfig:
    """Configuration for TOML code generation"""
    style: TOMLFormatStyle = TOMLFormatStyle.STANDARD
    indent_size: int = 2
    max_line_length: int = 80
    align_values: bool = True
    preserve_comments: bool = True
    add_trailing_commas: bool = False
    sort_keys: bool = False
    quote_keys: bool = False  # Quote all keys
    
    # Array formatting
    array_multiline_threshold: int = 4  # Elements before going multiline
    array_item_per_line: bool = False
    
    # String formatting
    prefer_literal_strings: bool = False
    multiline_string_threshold: int = 60  # Characters before multiline
    
    # Table formatting
    group_array_tables: bool = True
    separate_tables: bool = True
    table_header_spacing: bool = True
    
    # Development options
    add_type_comments: bool = False
    add_section_headers: bool = False
    verbose_comments: bool = False


class TOMLCodeGenerator:
    """Generates clean TOML code from AST"""
    
    def __init__(self, config: Optional[TOMLGeneratorConfig] = None):
        self.config = config or TOMLGeneratorConfig()
        self.output = io.StringIO()
        self.indent_level = 0
        self.current_line_length = 0
        self.needs_newline = False
        self.in_table_context = False
        self.current_table = None
        
        # Track key alignment for pretty formatting
        self.key_column_width = 0
        self.pending_key_values: List[tuple] = []
    
    def generate(self, node: TOMLNode) -> str:
        """Generate TOML code from AST node"""
        self.output = io.StringIO()
        self.indent_level = 0
        self.current_line_length = 0
        self.needs_newline = False
        self.in_table_context = False
        self.current_table = None
        
        if isinstance(node, TOMLDocument):
            self._generate_document(node)
        else:
            node.accept(self)
        
        return self.output.getvalue().rstrip() + '\n'
    
    def _generate_document(self, doc: TOMLDocument) -> None:
        """Generate complete TOML document"""
        if self.config.style == TOMLFormatStyle.DEVELOPMENT:
            self._write_line("# Generated TOML Configuration")
            self._write_line(f"# TOML Version: {TOML_VERSION}")
            self._write_line("")
        
        # Group items for better organization
        if self.config.style in (TOMLFormatStyle.PRETTY, TOMLFormatStyle.CONFIG):
            self._generate_grouped_document(doc)
        else:
            self._generate_sequential_document(doc)
    
    def _generate_grouped_document(self, doc: TOMLDocument) -> None:
        """Generate document with grouped sections"""
        # Separate items by type
        root_kvs = []
        tables = []
        array_tables = []
        comments = []
        
        current_table = None
        table_kvs = []
        
        for item in doc.items:
            if isinstance(item, TOMLKeyValue):
                if current_table is None:
                    root_kvs.append(item)
                else:
                    table_kvs.append(item)
            elif isinstance(item, TOMLTable):
                if current_table and table_kvs:
                    if current_table.is_array_table:
                        array_tables.append((current_table, table_kvs))
                    else:
                        tables.append((current_table, table_kvs))
                    table_kvs = []
                
                current_table = item
            elif isinstance(item, TOMLComment):
                comments.append(item)
        
        # Handle last table
        if current_table and table_kvs:
            if current_table.is_array_table:
                array_tables.append((current_table, table_kvs))
            else:
                tables.append((current_table, table_kvs))
        
        # Generate sections
        sections_written = 0
        
        # Root key-value pairs
        if root_kvs:
            if self.config.add_section_headers:
                self._write_line("# Root Configuration")
                self._write_line("")
            
            self._generate_key_value_section(root_kvs)
            sections_written += 1
        
        # Regular tables
        if tables:
            if sections_written > 0 and self.config.separate_tables:
                self._write_line("")
            
            for i, (table, kvs) in enumerate(tables):
                if i > 0 and self.config.separate_tables:
                    self._write_line("")
                
                self._generate_table_section(table, kvs)
            
            sections_written += 1
        
        # Array tables
        if array_tables:
            if sections_written > 0 and self.config.separate_tables:
                self._write_line("")
            
            # Group array tables by name if configured
            if self.config.group_array_tables:
                grouped = {}
                for table, kvs in array_tables:
                    name = table.key.dotted_key
                    if name not in grouped:
                        grouped[name] = []
                    grouped[name].append((table, kvs))
                
                for i, (name, group) in enumerate(grouped.items()):
                    if i > 0 and self.config.separate_tables:
                        self._write_line("")
                    
                    for j, (table, kvs) in enumerate(group):
                        if j > 0:
                            self._write_line("")
                        self._generate_table_section(table, kvs)
            else:
                for i, (table, kvs) in enumerate(array_tables):
                    if i > 0 and self.config.separate_tables:
                        self._write_line("")
                    
                    self._generate_table_section(table, kvs)
    
    def _generate_sequential_document(self, doc: TOMLDocument) -> None:
        """Generate document in original order"""
        for i, item in enumerate(doc.items):
            if (i > 0 and isinstance(item, TOMLTable) and 
                self.config.separate_tables):
                self._write_line("")
            
            item.accept(self)
    
    def _generate_key_value_section(self, kvs: List[TOMLKeyValue]) -> None:
        """Generate a section of key-value pairs with alignment"""
        if self.config.align_values and len(kvs) > 1:
            # Calculate maximum key width for alignment
            max_key_width = max(len(self._format_key(kv.key)) for kv in kvs)
            self.key_column_width = min(max_key_width, 40)  # Cap at 40 chars
            
            for kv in kvs:
                self._generate_aligned_key_value(kv)
        else:
            for kv in kvs:
                kv.accept(self)
    
    def _generate_table_section(self, table: TOMLTable, kvs: List[TOMLKeyValue]) -> None:
        """Generate table header and its key-value pairs"""
        self.current_table = table
        self.in_table_context = True
        
        table.accept(self)
        
        if kvs:
            if self.config.style != TOMLFormatStyle.COMPACT:
                self._write_line("")
            
            self._generate_key_value_section(kvs)
        
        self.in_table_context = False
        self.current_table = None
    
    def _generate_aligned_key_value(self, kv: TOMLKeyValue) -> None:
        """Generate key-value pair with alignment"""
        key_str = self._format_key(kv.key)
        padding = self.key_column_width - len(key_str)
        
        self._write_indent()
        self._write(key_str)
        self._write(" " * max(1, padding))
        self._write("= ")
        kv.value.accept(self)
        self._write_line()
    
    # Visitor methods
    def visit_document(self, node: TOMLDocument) -> None:
        self._generate_document(node)
    
    def visit_key_value(self, node: TOMLKeyValue) -> None:
        """Generate key-value pair"""
        if not self.config.align_values or self.in_table_context:
            self._write_indent()
            self._write(self._format_key(node.key))
            self._write(" = ")
            node.value.accept(self)
            self._write_line()
        else:
            self._generate_aligned_key_value(node)
    
    def visit_table(self, node: TOMLTable) -> None:
        """Generate table header"""
        if self.config.table_header_spacing and self.output.tell() > 0:
            # Add spacing before table if not first item
            last_content = self.output.getvalue().rstrip()
            if last_content and not last_content.endswith('\n\n'):
                self._write_line("")
        
        self._write_indent()
        if node.is_array_table:
            self._write("[[")
        else:
            self._write("[")
        
        self._write(self._format_key(node.key))
        
        if node.is_array_table:
            self._write("]]")
        else:
            self._write("]")
        
        self._write_line()
        
        if self.config.add_type_comments:
            self._write_indent()
            table_type = "array table" if node.is_array_table else "table"
            self._write_line(f"# Type: {table_type}")
    
    def visit_key(self, node: TOMLKey) -> None:
        """This shouldn't be called directly"""
        pass
    
    def visit_string(self, node: TOMLString) -> None:
        """Generate string value"""
        if node.string_type == TOMLStringType.BASIC:
            self._write_basic_string(node.value)
        elif node.string_type == TOMLStringType.LITERAL:
            self._write_literal_string(node.value)
        elif node.string_type == TOMLStringType.MULTILINE_BASIC:
            self._write_multiline_basic_string(node.value)
        elif node.string_type == TOMLStringType.MULTILINE_LITERAL:
            self._write_multiline_literal_string(node.value)
    
    def visit_integer(self, node: TOMLInteger) -> None:
        """Generate integer value"""
        if self.config.style == TOMLFormatStyle.COMPACT:
            # Use minimal representation
            self._write(str(node.value))
        else:
            # Preserve original formatting if available
            self._write(node.raw_text)
    
    def visit_float(self, node: TOMLFloat) -> None:
        """Generate float value"""
        if node.is_inf:
            self._write("inf" if node.value > 0 else "-inf")
        elif node.is_nan:
            self._write("nan")
        else:
            if self.config.style == TOMLFormatStyle.COMPACT:
                self._write(str(node.value))
            else:
                self._write(node.raw_text)
    
    def visit_boolean(self, node: TOMLBoolean) -> None:
        """Generate boolean value"""
        self._write("true" if node.value else "false")
    
    def visit_datetime(self, node: TOMLDateTime) -> None:
        """Generate datetime value"""
        self._write(node.raw_text)
    
    def visit_date(self, node: TOMLDate) -> None:
        """Generate date value"""
        self._write(node.raw_text)
    
    def visit_time(self, node: TOMLTime) -> None:
        """Generate time value"""
        self._write(node.raw_text)
    
    def visit_array(self, node: TOMLArray) -> None:
        """Generate array value"""
        if not node.elements:
            self._write("[]")
            return
        
        # Determine if array should be multiline
        should_be_multiline = (
            node.is_multiline or
            len(node.elements) >= self.config.array_multiline_threshold or
            self.config.array_item_per_line or
            self._estimate_array_width(node) > self.config.max_line_length
        )
        
        if should_be_multiline:
            self._write_multiline_array(node)
        else:
            self._write_inline_array(node)
    
    def visit_inline_table(self, node: TOMLInlineTable) -> None:
        """Generate inline table value"""
        if not node.pairs:
            self._write("{}")
            return
        
        self._write("{ ")
        
        for i, (key, value) in enumerate(node.pairs):
            if i > 0:
                self._write(", ")
            
            self._write(self._format_bare_key(key))
            self._write(" = ")
            value.accept(self)
        
        self._write(" }")
    
    def visit_comment(self, node: TOMLComment) -> None:
        """Generate comment"""
        if self.config.preserve_comments:
            self._write_indent()
            self._write("# ")
            self._write(node.text)
            self._write_line()
    
    # Helper methods
    def _format_key(self, key: TOMLKey) -> str:
        """Format a key (possibly dotted)"""
        parts = []
        for i, part in enumerate(key.parts):
            if key.is_quoted[i] or self.config.quote_keys or self._needs_quoting(part):
                parts.append(f'"{self._escape_string(part)}"')
            else:
                parts.append(part)
        
        return '.'.join(parts)
    
    def _format_bare_key(self, key: str) -> str:
        """Format a bare key (for inline tables)"""
        if self.config.quote_keys or self._needs_quoting(key):
            return f'"{self._escape_string(key)}"'
        return key
    
    def _needs_quoting(self, key: str) -> bool:
        """Check if a key needs quoting"""
        if not key:
            return True
        
        # Check if it's a valid bare key (A-Z, a-z, 0-9, -, _)
        return not re.match(r'^[A-Za-z0-9_-]+$', key)
    
    def _write_basic_string(self, value: str) -> None:
        """Write basic string with escaping"""
        self._write('"')
        self._write(self._escape_string(value))
        self._write('"')
    
    def _write_literal_string(self, value: str) -> None:
        """Write literal string"""
        self._write("'")
        self._write(value)
        self._write("'")
    
    def _write_multiline_basic_string(self, value: str) -> None:
        """Write multiline basic string"""
        self._write('"""')
        if value.startswith('\n'):
            self._write_line()
        
        # Split into lines and handle indentation
        lines = value.split('\n')
        for i, line in enumerate(lines):
            if i > 0:
                self._write_line()
            if line.strip():  # Don't indent empty lines
                self._write_indent()
                self._write(self._escape_string(line))
        
        if not value.endswith('\n'):
            self._write_line()
        self._write_indent()
        self._write('"""')
    
    def _write_multiline_literal_string(self, value: str) -> None:
        """Write multiline literal string"""
        self._write("'''")
        if value.startswith('\n'):
            self._write_line()
        
        lines = value.split('\n')
        for i, line in enumerate(lines):
            if i > 0:
                self._write_line()
            if line.strip():
                self._write_indent()
                self._write(line)
        
        if not value.endswith('\n'):
            self._write_line()
        self._write_indent()
        self._write("'''")
    
    def _write_inline_array(self, node: TOMLArray) -> None:
        """Write array on a single line"""
        self._write("[")
        
        for i, element in enumerate(node.elements):
            if i > 0:
                self._write(", ")
            element.accept(self)
        
        if node.trailing_comma and len(node.elements) > 0:
            self._write(",")
        
        self._write("]")
    
    def _write_multiline_array(self, node: TOMLArray) -> None:
        """Write array across multiple lines"""
        self._write("[")
        self._write_line()
        
        self.indent_level += 1
        
        for i, element in enumerate(node.elements):
            self._write_indent()
            element.accept(self)
            
            if i < len(node.elements) - 1 or node.trailing_comma:
                self._write(",")
            
            self._write_line()
        
        self.indent_level -= 1
        self._write_indent()
        self._write("]")
    
    def _estimate_array_width(self, node: TOMLArray) -> int:
        """Estimate the width of an array if written inline"""
        width = 2  # [ and ]
        
        for i, element in enumerate(node.elements):
            if i > 0:
                width += 2  # ", "
            
            # Rough estimate of element width
            if isinstance(element, TOMLString):
                width += len(element.value) + 2  # quotes
            elif isinstance(element, (TOMLInteger, TOMLFloat)):
                width += len(str(element.value))
            elif isinstance(element, TOMLBoolean):
                width += 5  # "false"
            else:
                width += 10  # rough estimate
        
        return width
    
    def _escape_string(self, value: str) -> str:
        """Escape string for basic string format"""
        return (value
                .replace('\\', '\\\\')
                .replace('"', '\\"')
                .replace('\b', '\\b')
                .replace('\f', '\\f')
                .replace('\n', '\\n')
                .replace('\r', '\\r')
                .replace('\t', '\\t'))
    
    def _write(self, text: str) -> None:
        """Write text to output"""
        self.output.write(text)
        self.current_line_length += len(text)
    
    def _write_line(self, text: str = "") -> None:
        """Write line with newline"""
        if text:
            self._write(text)
        self.output.write('\n')
        self.current_line_length = 0
        self.needs_newline = False
    
    def _write_indent(self) -> None:
        """Write current indentation"""
        indent = ' ' * (self.indent_level * self.config.indent_size)
        self._write(indent)


class TOMLFormatter:
    """TOML code formatter with various styles"""
    
    @staticmethod
    def format_toml(code: str, style: TOMLFormatStyle = TOMLFormatStyle.STANDARD) -> str:
        """Format TOML code with specified style"""
        from .toml_parser import parse_toml
        
        try:
            doc = parse_toml(code)
            config = TOMLGeneratorConfig(style=style)
            generator = TOMLCodeGenerator(config)
            return generator.generate(doc)
        except Exception as e:
            # If parsing fails, return original code
            return code
    
    @staticmethod
    def minify_toml(code: str) -> str:
        """Minify TOML code for compact representation"""
        config = TOMLGeneratorConfig(
            style=TOMLFormatStyle.COMPACT,
            align_values=False,
            separate_tables=False,
            table_header_spacing=False,
            add_trailing_commas=False
        )
        
        from .toml_parser import parse_toml
        
        try:
            doc = parse_toml(code)
            generator = TOMLCodeGenerator(config)
            return generator.generate(doc)
        except Exception as e:
            return code
    
    @staticmethod
    def prettify_toml(code: str) -> str:
        """Prettify TOML code for enhanced readability"""
        config = TOMLGeneratorConfig(
            style=TOMLFormatStyle.PRETTY,
            align_values=True,
            separate_tables=True,
            table_header_spacing=True,
            sort_keys=True,
            array_item_per_line=True,
            add_section_headers=True
        )
        
        from .toml_parser import parse_toml
        
        try:
            doc = parse_toml(code)
            generator = TOMLCodeGenerator(config)
            return generator.generate(doc)
        except Exception as e:
            return code


def generate_toml(node: TOMLNode, style: TOMLFormatStyle = TOMLFormatStyle.STANDARD) -> str:
    """Generate TOML code from AST node"""
    config = TOMLGeneratorConfig(style=style)
    generator = TOMLCodeGenerator(config)
    return generator.generate(node)


def format_toml_code(code: str, style: TOMLFormatStyle = TOMLFormatStyle.STANDARD) -> str:
    """Format TOML code string"""
    return TOMLFormatter.format_toml(code, style) 