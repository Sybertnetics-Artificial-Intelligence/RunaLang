#!/usr/bin/env python3
"""
INI Generator - Clean INI Configuration File Generation

Provides comprehensive INI code generation with multiple formatting styles:
- Standard INI format with clean sectioning and alignment
- Windows INI format for registry and system configurations
- Git config format with subsections and special syntax
- Systemd config format for service files
- Compact format for minimal space usage
- Development format with extensive comments

Features:
- Proper section header formatting
- Key-value pair alignment and spacing
- Comment preservation and generation
- Value type-specific formatting
- Multi-line value handling
- Include directive support
- Interpolation syntax formatting
"""

from typing import List, Dict, Optional, Any, Union, TextIO
from dataclasses import dataclass
from enum import Enum
import io
import re

from .ini_ast import *


class INIFormatStyle(Enum):
    """INI code formatting styles"""
    STANDARD = "standard"          # Clean, readable INI
    WINDOWS = "windows"            # Windows INI format
    GIT_CONFIG = "git"            # Git configuration format
    SYSTEMD = "systemd"           # Systemd unit file format
    COMPACT = "compact"           # Minimal spacing
    DEVELOPMENT = "development"   # With extensive comments


@dataclass
class INIGeneratorConfig:
    """Configuration for INI code generation"""
    style: INIFormatStyle = INIFormatStyle.STANDARD
    indent_size: int = 0          # INI typically doesn't use indentation
    max_line_length: int = 80
    align_values: bool = True
    preserve_comments: bool = True
    sort_sections: bool = False
    sort_keys: bool = False
    
    # Value formatting options
    quote_strings: bool = False
    quote_style: str = '"'
    delimiter: str = "="          # or ":"
    comment_prefix: str = ";"     # or "#"
    
    # Section formatting
    section_spacing: int = 1      # Empty lines between sections
    uppercase_sections: bool = False
    bracket_style: str = "[]"     # or "()"
    
    # Windows-specific options
    windows_case_insensitive: bool = True
    windows_paths: bool = False
    
    # Git config options
    git_subsections: bool = True
    git_spacing: bool = True
    
    # Systemd options
    systemd_ordering: bool = True
    systemd_comments: bool = True
    
    # Development options
    add_type_comments: bool = False
    add_documentation: bool = False
    verbose_formatting: bool = False


class INICodeGenerator:
    """Generates clean INI code from AST"""
    
    def __init__(self, config: Optional[INIGeneratorConfig] = None):
        self.config = config or INIGeneratorConfig()
        self.output = io.StringIO()
        self.current_line_length = 0
        self.needs_newline = False
        
        # Adjust config based on style
        self._adjust_config_for_style()
        
        # Value alignment tracking
        self.max_key_length = 0
        self.section_keys: Dict[str, int] = {}
    
    def _adjust_config_for_style(self) -> None:
        """Adjust configuration based on selected style"""
        if self.config.style == INIFormatStyle.WINDOWS:
            self.config.comment_prefix = ";"
            self.config.delimiter = "="
            self.config.windows_case_insensitive = True
            self.config.section_spacing = 1
        elif self.config.style == INIFormatStyle.GIT_CONFIG:
            self.config.comment_prefix = "#"
            self.config.delimiter = "="
            self.config.git_subsections = True
            self.config.section_spacing = 1
        elif self.config.style == INIFormatStyle.SYSTEMD:
            self.config.comment_prefix = "#"
            self.config.delimiter = "="
            self.config.systemd_ordering = True
            self.config.section_spacing = 0
        elif self.config.style == INIFormatStyle.COMPACT:
            self.config.section_spacing = 0
            self.config.align_values = False
            self.config.preserve_comments = False
        elif self.config.style == INIFormatStyle.DEVELOPMENT:
            self.config.add_type_comments = True
            self.config.add_documentation = True
            self.config.verbose_formatting = True
            self.config.section_spacing = 2
    
    def generate(self, node: ININode) -> str:
        """Generate INI code from AST node"""
        self.output = io.StringIO()
        self.current_line_length = 0
        self.needs_newline = False
        
        # Calculate alignment if needed
        if self.config.align_values and isinstance(node, INIConfiguration):
            self._calculate_alignment(node)
        
        if isinstance(node, INIConfiguration):
            self._generate_configuration(node)
        else:
            node.accept(self)
        
        return self.output.getvalue().rstrip() + "\n"
    
    def _calculate_alignment(self, config: INIConfiguration) -> None:
        """Calculate key alignment for value formatting"""
        for section in config.sections:
            section_max = 0
            for entry in section.entries:
                if isinstance(entry, INIKeyValuePair):
                    section_max = max(section_max, len(entry.key.name))
            self.section_keys[section.name] = section_max
            self.max_key_length = max(self.max_key_length, section_max)
    
    def _generate_configuration(self, config: INIConfiguration) -> None:
        """Generate complete INI configuration"""
        if self.config.style == INIFormatStyle.DEVELOPMENT:
            self._write_line(f"{self.config.comment_prefix} Generated INI Configuration")
            self._write_line(f"{self.config.comment_prefix} Format: {self.config.style.value}")
            if config.filename:
                self._write_line(f"{self.config.comment_prefix} File: {config.filename}")
            self._write_line("")
        
        # Generate global entries first
        if config.global_entries:
            for i, entry in enumerate(config.global_entries):
                if i > 0 and isinstance(entry, INIKeyValuePair):
                    self._write_line("")
                entry.accept(self)
            
            if config.sections:
                for _ in range(self.config.section_spacing + 1):
                    self._write_line("")
        
        # Generate sections
        sections = config.sections
        if self.config.sort_sections:
            sections = sorted(sections, key=lambda s: s.name.lower())
        
        for i, section in enumerate(sections):
            if i > 0:
                for _ in range(self.config.section_spacing):
                    self._write_line("")
            section.accept(self)
    
    # Visitor methods
    def visit_configuration(self, node: INIConfiguration) -> None:
        self._generate_configuration(node)
    
    def visit_section(self, node: INISection) -> None:
        """Generate INI section"""
        if not node.is_root:
            # Generate section header
            section_name = node.name
            if self.config.uppercase_sections:
                section_name = section_name.upper()
            
            if isinstance(node, GitConfigSection) and node.subsection:
                self._write_line(f'[{section_name} "{node.subsection}"]')
            else:
                self._write_line(f'[{section_name}]')
            
            if self.config.style == INIFormatStyle.DEVELOPMENT and self.config.add_documentation:
                self._write_line(f"{self.config.comment_prefix} Section: {node.name}")
                if hasattr(node, 'metadata') and node.metadata:
                    for key, value in node.metadata.items():
                        self._write_line(f"{self.config.comment_prefix} {key}: {value}")
        
        # Generate section entries
        entries = node.entries
        if self.config.sort_keys:
            entries = sorted([e for e in entries if isinstance(e, INIKeyValuePair)], 
                           key=lambda e: e.key.name.lower()) + \
                     [e for e in entries if not isinstance(e, INIKeyValuePair)]
        
        for i, entry in enumerate(entries):
            # Add spacing for readability in development mode
            if (i > 0 and self.config.style == INIFormatStyle.DEVELOPMENT and 
                isinstance(entry, INIKeyValuePair) and 
                isinstance(entries[i-1], INIKeyValuePair)):
                if self.config.verbose_formatting:
                    self._write_line("")
            
            entry.accept(self)
    
    def visit_subsection(self, node: INISubSection) -> None:
        """Generate INI subsection"""
        self._write_line(f'[{node.parent_section}.{node.name}]')
        
        for entry in node.entries:
            entry.accept(self)
    
    def visit_key_value_pair(self, node: INIKeyValuePair) -> None:
        """Generate INI key-value pair"""
        key = node.key.name
        value_str = self._format_value(node.value)
        delimiter = self.config.delimiter
        
        # Apply delimiter from node if specified
        if node.delimiter != INIDelimiterType.EQUALS:
            delimiter = node.delimiter.value
        
        # Format with alignment
        if self.config.align_values:
            section_max = self.section_keys.get("current", self.max_key_length)
            key_part = key.ljust(section_max)
            line = f"{key_part} {delimiter} {value_str}"
        else:
            line = f"{key}{delimiter}{value_str}"
        
        # Add inline comment
        if node.inline_comment and self.config.preserve_comments:
            line += f"  {self.config.comment_prefix} {node.inline_comment.text}"
        
        # Add type comment in development mode
        if self.config.add_type_comments:
            type_comment = self._get_type_comment(node.value)
            if type_comment:
                line += f"  {self.config.comment_prefix} {type_comment}"
        
        self._write_line(line)
    
    def visit_key(self, node: INIKey) -> None:
        """Generate INI key (standalone)"""
        self._write(node.name)
    
    def visit_value(self, node: INIValue) -> None:
        """Generate INI value (standalone)"""
        self._write(self._format_value(node))
    
    def visit_comment(self, node: INIComment) -> None:
        """Generate INI comment"""
        if not self.config.preserve_comments:
            return
        
        prefix = self.config.comment_prefix
        if node.style == INICommentStyle.HASH:
            prefix = "#"
        elif node.style == INICommentStyle.SEMICOLON:
            prefix = ";"
        
        if node.is_inline:
            self._write(f"  {prefix} {node.text}")
        else:
            self._write_line(f"{prefix} {node.text}")
    
    def visit_interpolation(self, node: INIInterpolation) -> None:
        """Generate INI variable interpolation"""
        if node.format_style == "${}":
            self._write(f"${{{node.variable_name}}}")
        elif node.format_style == "%(...)s":
            self._write(f"%({node.variable_name})s")
        elif node.format_style == "%{}":
            self._write(f"%{{{node.variable_name}}}")
        else:
            self._write(f"${{{node.variable_name}}}")
        
        if node.default_value:
            self._write(f":-{node.default_value}")
    
    def visit_include(self, node: INIInclude) -> None:
        """Generate INI include directive"""
        if self.config.style == INIFormatStyle.GIT_CONFIG:
            self._write_line(f"[include]")
            self._write_line(f"    path = {node.file_path}")
        else:
            self._write_line(f"include = {node.file_path}")
    
    def visit_array(self, node: INIArray) -> None:
        """Generate INI array value"""
        if node.is_multiline:
            # Multi-line array format
            for i, element in enumerate(node.elements):
                if i == 0:
                    self._write(self._format_value(element))
                else:
                    self._write_line("")
                    self._write(f"    {self._format_value(element)}")
        else:
            # Single-line comma-separated format
            values = [self._format_value(elem) for elem in node.elements]
            self._write(node.separator.join(values))
    
    def visit_conditional(self, node: INIConditional) -> None:
        """Generate INI conditional (implementation-specific)"""
        self._write_line(f"{self.config.comment_prefix} Conditional: {node.condition}")
        for entry in node.true_entries:
            entry.accept(self)
    
    def visit_loop(self, node: INILoop) -> None:
        """Generate INI loop (implementation-specific)"""
        self._write_line(f"{self.config.comment_prefix} Loop: {node.variable} in {node.iterable}")
        for entry in node.template_entries:
            entry.accept(self)
    
    def visit_macro(self, node: INIMacro) -> None:
        """Generate INI macro definition"""
        self._write_line(f"{self.config.comment_prefix} Macro: {node.name}({', '.join(node.parameters)})")
    
    def visit_macro_call(self, node: INIMacroCall) -> None:
        """Generate INI macro call"""
        args = ', '.join(f"{k}={v}" for k, v in node.arguments.items())
        self._write_line(f"{self.config.comment_prefix} Call: {node.macro_name}({args})")
    
    def visit_windows_section(self, node: WindowsINISection) -> None:
        """Generate Windows INI section"""
        self.visit_section(node)
        
        if self.config.add_documentation and node.registry_path:
            self._write_line(f"{self.config.comment_prefix} Registry: {node.registry_path}")
    
    def visit_git_section(self, node: GitConfigSection) -> None:
        """Generate Git config section"""
        self.visit_section(node)
    
    def visit_systemd_section(self, node: SystemdConfigSection) -> None:
        """Generate systemd config section"""
        self.visit_section(node)
        
        if self.config.add_documentation and node.unit_type:
            self._write_line(f"{self.config.comment_prefix} Unit Type: {node.unit_type}")
    
    def _format_value(self, value: INIValue) -> str:
        """Format INI value according to type and style"""
        if value.value_type == INIValueType.STRING:
            return self._format_string_value(value)
        elif value.value_type == INIValueType.NUMBER:
            return str(value.value)
        elif value.value_type == INIValueType.BOOLEAN:
            return self._format_boolean_value(value.value)
        elif value.value_type == INIValueType.LIST:
            if isinstance(value.value, list):
                return self._format_list_value(value.value)
            return str(value.value)
        elif value.value_type == INIValueType.MULTILINE:
            return self._format_multiline_value(value.value)
        else:
            return str(value.value)
    
    def _format_string_value(self, value: INIValue) -> str:
        """Format string value with proper quoting"""
        text = str(value.value)
        
        # Preserve original quoting if specified
        if value.is_quoted:
            return f"{value.quote_style}{text}{value.quote_style}"
        
        # Auto-quote if needed or configured
        needs_quotes = (
            self.config.quote_strings or
            ' ' in text or
            text.startswith('#') or
            text.startswith(';') or
            '=' in text or
            ':' in text
        )
        
        if needs_quotes:
            return f"{self.config.quote_style}{text}{self.config.quote_style}"
        
        return text
    
    def _format_boolean_value(self, value: bool) -> str:
        """Format boolean value according to style"""
        if self.config.style == INIFormatStyle.WINDOWS:
            return "1" if value else "0"
        elif self.config.style == INIFormatStyle.SYSTEMD:
            return "yes" if value else "no"
        else:
            return "true" if value else "false"
    
    def _format_list_value(self, values: List[Any]) -> str:
        """Format list value as comma-separated"""
        formatted_values = []
        for val in values:
            if isinstance(val, str):
                formatted_values.append(self._format_string_for_list(val))
            else:
                formatted_values.append(str(val))
        return ", ".join(formatted_values)
    
    def _format_string_for_list(self, text: str) -> str:
        """Format string within a list context"""
        if ',' in text or ' ' in text:
            return f'"{text}"'
        return text
    
    def _format_multiline_value(self, text: str) -> str:
        """Format multiline value"""
        lines = text.split('\n')
        if len(lines) <= 1:
            return text
        
        # First line on same line as key
        result = lines[0]
        for line in lines[1:]:
            result += f"\n    {line}"  # Indent continuation lines
        return result
    
    def _get_type_comment(self, value: INIValue) -> str:
        """Get type comment for development mode"""
        type_name = value.value_type.value
        if value.value_type == INIValueType.LIST and isinstance(value.value, list):
            if value.value:
                element_type = type(value.value[0]).__name__
                return f"List<{element_type}>"
        return type_name
    
    def _write(self, text: str) -> None:
        """Write text to output"""
        self.output.write(text)
        self.current_line_length += len(text)
    
    def _write_line(self, text: str = "") -> None:
        """Write line to output"""
        if text:
            self.output.write(text)
        self.output.write("\n")
        self.current_line_length = 0


class INIFormatter:
    """Utility class for INI code formatting"""
    
    @staticmethod
    def format_ini(code: str, style: INIFormatStyle = INIFormatStyle.STANDARD) -> str:
        """Format INI code string"""
        from .ini_parser import INIParser
        
        parser = INIParser()
        config = parser.parse(code)
        
        generator_config = INIGeneratorConfig(style=style)
        generator = INICodeGenerator(generator_config)
        
        return generator.generate(config)
    
    @staticmethod
    def minify_ini(code: str) -> str:
        """Minify INI code by removing unnecessary whitespace"""
        lines = []
        for line in code.split('\n'):
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith(';'):
                lines.append(line)
        return '\n'.join(lines)
    
    @staticmethod
    def windows_format(code: str) -> str:
        """Format INI code for Windows compatibility"""
        config = INIGeneratorConfig(
            style=INIFormatStyle.WINDOWS,
            comment_prefix=";",
            delimiter="=",
            windows_case_insensitive=True
        )
        
        from .ini_parser import INIParser
        parser = INIParser()
        ini_config = parser.parse(code)
        
        generator = INICodeGenerator(config)
        return generator.generate(ini_config)
    
    @staticmethod
    def git_config_format(code: str) -> str:
        """Format INI code as Git configuration"""
        config = INIGeneratorConfig(
            style=INIFormatStyle.GIT_CONFIG,
            comment_prefix="#",
            git_subsections=True
        )
        
        from .ini_parser import INIParser
        parser = INIParser()
        ini_config = parser.parse(code)
        
        generator = INICodeGenerator(config)
        return generator.generate(ini_config)


def generate_ini(node: ININode, style: INIFormatStyle = INIFormatStyle.STANDARD) -> str:
    """Generate INI code from AST node"""
    config = INIGeneratorConfig(style=style)
    generator = INICodeGenerator(config)
    return generator.generate(node)


def format_ini_code(code: str, style: INIFormatStyle = INIFormatStyle.STANDARD) -> str:
    """Format INI code string"""
    return INIFormatter.format_ini(code, style) 