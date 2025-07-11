#!/usr/bin/env python3
"""
YAML Code Generator

Generates YAML text from YAML AST nodes with support for multiple formatting styles.

Author: Sybertnetics AI Solutions
License: MIT
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass
from enum import Enum, auto
import logging

from .yaml_ast import *


class YamlCodeStyle(Enum):
    """YAML code formatting styles."""
    STANDARD = "standard"
    COMPACT = "compact"
    EXPANDED = "expanded"
    FLOW = "flow"
    BLOCK = "block"


@dataclass
class YamlFormattingOptions:
    """YAML code formatting options."""
    indent_size: int = 2
    use_tabs: bool = False
    max_line_length: int = 120
    
    # YAML-specific
    prefer_block_style: bool = True
    prefer_flow_scalars: bool = False
    sort_keys: bool = False
    preserve_quotes: bool = False
    canonical: bool = False
    allow_unicode: bool = True
    line_break: str = '\n'
    explicit_start: bool = False
    explicit_end: bool = False
    default_style: Optional[str] = None
    default_flow_style: Optional[bool] = None


class YamlFormatter:
    """YAML code formatter with style presets."""
    
    @staticmethod
    def get_style_options(style: YamlCodeStyle) -> YamlFormattingOptions:
        """Get formatting options for a specific style."""
        if style == YamlCodeStyle.STANDARD:
            return YamlFormattingOptions(
                indent_size=2,
                prefer_block_style=True,
                sort_keys=False
            )
        elif style == YamlCodeStyle.COMPACT:
            return YamlFormattingOptions(
                indent_size=2,
                prefer_block_style=False,
                max_line_length=200,
                default_flow_style=True
            )
        elif style == YamlCodeStyle.EXPANDED:
            return YamlFormattingOptions(
                indent_size=4,
                prefer_block_style=True,
                sort_keys=True,
                explicit_start=True
            )
        elif style == YamlCodeStyle.FLOW:
            return YamlFormattingOptions(
                indent_size=2,
                prefer_block_style=False,
                default_flow_style=True
            )
        elif style == YamlCodeStyle.BLOCK:
            return YamlFormattingOptions(
                indent_size=2,
                prefer_block_style=True,
                default_flow_style=False
            )
        else:
            return YamlFormattingOptions()


class YamlCodeGenerator(YamlVisitorExtended):
    """YAML code generator that produces formatted YAML from AST."""
    
    def __init__(self, style: YamlCodeStyle = YamlCodeStyle.STANDARD):
        self.style = style
        self.options = YamlFormatter.get_style_options(style)
        self.logger = logging.getLogger(__name__)
        
        # Output state
        self.output = []
        self.indent_level = 0
        self.current_line_length = 0
        self.needs_indent = True
        self.in_flow_context = False
        self.anchors_written = set()
    
    def generate(self, node: YamlNode) -> str:
        """Generate YAML text from an AST node."""
        self.output = []
        self.indent_level = 0
        self.current_line_length = 0
        self.needs_indent = True
        self.in_flow_context = False
        self.anchors_written = set()
        
        try:
            node.accept(self)
            result = "".join(self.output)
            return self._post_process(result)
        except Exception as e:
            self.logger.error(f"YAML code generation failed: {e}")
            raise RuntimeError(f"Failed to generate YAML code: {e}")
    
    def _post_process(self, code: str) -> str:
        """Post-process generated code."""
        lines = code.split('\n')
        processed_lines = []
        
        for line in lines:
            # Remove trailing whitespace
            line = line.rstrip()
            processed_lines.append(line)
        
        # Remove trailing empty lines
        while processed_lines and not processed_lines[-1]:
            processed_lines.pop()
        
        result = '\n'.join(processed_lines)
        
        if result and not result.endswith('\n'):
            result += '\n'
        
        return result
    
    def _write(self, text: str):
        """Write text to output."""
        if self.needs_indent and text.strip():
            self._write_indent()
            self.needs_indent = False
        
        self.output.append(text)
        self.current_line_length += len(text)
    
    def _write_line(self, text: str = ""):
        """Write a line of text."""
        if text:
            self._write(text)
        self.output.append('\n')
        self.current_line_length = 0
        self.needs_indent = True
    
    def _write_indent(self):
        """Write current indentation."""
        if self.options.use_tabs:
            indent = '\t' * self.indent_level
        else:
            indent = ' ' * (self.indent_level * self.options.indent_size)
        
        self.output.append(indent)
        self.current_line_length += len(indent)
    
    def _increase_indent(self):
        """Increase indentation level."""
        self.indent_level += 1
    
    def _decrease_indent(self):
        """Decrease indentation level."""
        self.indent_level = max(0, self.indent_level - 1)
    
    def _should_use_flow_style(self, node: YamlValue) -> bool:
        """Determine if node should use flow style."""
        if self.in_flow_context:
            return True
        
        if self.options.default_flow_style is not None:
            return self.options.default_flow_style
        
        # Use flow for simple, short collections
        if isinstance(node, YamlMapping):
            if hasattr(node, 'style') and node.style == YamlMappingStyle.FLOW:
                return True
            return len(node.items) <= 3 and all(self._is_simple_value(item.value) for item in node.items)
        elif isinstance(node, YamlSequence):
            if hasattr(node, 'style') and node.style == YamlSequenceStyle.FLOW:
                return True
            return len(node.items) <= 5 and all(self._is_simple_value(item) for item in node.items)
        
        return False
    
    def _is_simple_value(self, value: YamlValue) -> bool:
        """Check if value is simple (scalar or short collection)."""
        if isinstance(value, YamlScalar):
            return True
        elif isinstance(value, (YamlMapping, YamlSequence)):
            return False  # Consider all collections complex for this check
        return True
    
    def _escape_scalar(self, value: str, style: YamlScalarStyle) -> str:
        """Escape scalar value based on style."""
        if style == YamlScalarStyle.SINGLE_QUOTED:
            return "'" + value.replace("'", "''") + "'"
        elif style == YamlScalarStyle.DOUBLE_QUOTED:
            escaped = value.replace('\\', '\\\\').replace('"', '\\"')
            escaped = escaped.replace('\n', '\\n').replace('\t', '\\t').replace('\r', '\\r')
            return '"' + escaped + '"'
        else:
            # Plain style - check if escaping is needed
            if self._needs_quoting(value):
                return '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'
            return value
    
    def _needs_quoting(self, value: str) -> bool:
        """Check if scalar value needs quoting."""
        if not value:
            return True
        
        # Check for special YAML values
        if value.lower() in ('true', 'false', 'null', 'nil', '~', 'yes', 'no', 'on', 'off'):
            return True
        
        # Check for numeric values
        try:
            float(value)
            return True
        except ValueError:
            pass
        
        # Check for special characters
        if any(char in value for char in '[]{},:*&!|>#@`'):
            return True
        
        # Check if starts with special characters
        if value[0] in '-?:':
            return True
        
        return False
    
    # Visitor methods
    def visit_yaml_stream(self, node: YamlStream):
        """Visit YAML stream."""
        for i, document in enumerate(node.documents):
            if i > 0 or self.options.explicit_start:
                self._write_line('---')
            
            document.accept(self)
            
            if document.explicit_end or self.options.explicit_end:
                self._write_line('...')
            
            if i < len(node.documents) - 1:
                self._write_line()
    
    def visit_yaml_document(self, node: YamlDocument):
        """Visit YAML document."""
        if node.explicit_start or self.options.explicit_start:
            self._write_line('---')
        
        # Write directives
        for directive in node.directives:
            directive.accept(self)
            self._write_line()
        
        # Write content
        if node.content:
            node.content.accept(self)
        
        if node.explicit_end or self.options.explicit_end:
            self._write_line()
            self._write_line('...')
    
    def visit_yaml_directive(self, node: YamlDirective):
        """Visit YAML directive."""
        self._write(f'%{node.name}')
        for param in node.parameters:
            self._write(f' {param}')
    
    def visit_yaml_mapping(self, node: YamlMapping):
        """Visit YAML mapping."""
        if not node.items:
            self._write('{}')
            return
        
        # Sort items if requested
        items = node.items
        if self.options.sort_keys:
            items = sorted(items, key=lambda item: str(self._extract_key_value(item.key)))
        
        use_flow = self._should_use_flow_style(node)
        
        if use_flow:
            self._write_flow_mapping(items)
        else:
            self._write_block_mapping(items)
    
    def _write_flow_mapping(self, items: List[YamlMappingItem]):
        """Write mapping in flow style."""
        self._write('{')
        old_flow_context = self.in_flow_context
        self.in_flow_context = True
        
        for i, item in enumerate(items):
            if i > 0:
                self._write(', ')
            
            item.key.accept(self)
            self._write(': ')
            item.value.accept(self)
        
        self.in_flow_context = old_flow_context
        self._write('}')
    
    def _write_block_mapping(self, items: List[YamlMappingItem]):
        """Write mapping in block style."""
        for i, item in enumerate(items):
            if i > 0:
                self._write_line()
            
            # Write key
            item.key.accept(self)
            self._write(':')
            
            # Check if value is complex
            if isinstance(item.value, (YamlMapping, YamlSequence)) and not self._should_use_flow_style(item.value):
                self._write_line()
                self._increase_indent()
                item.value.accept(self)
                self._decrease_indent()
            else:
                self._write(' ')
                item.value.accept(self)
    
    def visit_yaml_sequence(self, node: YamlSequence):
        """Visit YAML sequence."""
        if not node.items:
            self._write('[]')
            return
        
        use_flow = self._should_use_flow_style(node)
        
        if use_flow:
            self._write_flow_sequence(node.items)
        else:
            self._write_block_sequence(node.items)
    
    def _write_flow_sequence(self, items: List[YamlValue]):
        """Write sequence in flow style."""
        self._write('[')
        old_flow_context = self.in_flow_context
        self.in_flow_context = True
        
        for i, item in enumerate(items):
            if i > 0:
                self._write(', ')
            item.accept(self)
        
        self.in_flow_context = old_flow_context
        self._write(']')
    
    def _write_block_sequence(self, items: List[YamlValue]):
        """Write sequence in block style."""
        for i, item in enumerate(items):
            if i > 0:
                self._write_line()
            
            self._write('- ')
            
            # Check if item is complex
            if isinstance(item, (YamlMapping, YamlSequence)) and not self._should_use_flow_style(item):
                self._increase_indent()
                item.accept(self)
                self._decrease_indent()
            else:
                old_needs_indent = self.needs_indent
                self.needs_indent = False
                item.accept(self)
                self.needs_indent = old_needs_indent
    
    def visit_yaml_mapping_item(self, node: YamlMappingItem):
        """Visit YAML mapping item."""
        node.key.accept(self)
        self._write(': ')
        node.value.accept(self)
    
    def visit_yaml_scalar(self, node: YamlScalar):
        """Visit YAML scalar."""
        if node.value is None:
            self._write('null')
        elif isinstance(node.value, bool):
            self._write('true' if node.value else 'false')
        elif isinstance(node.value, (int, float)):
            self._write(str(node.value))
        elif isinstance(node.value, str):
            if node.style == YamlScalarStyle.LITERAL:
                self._write_literal_scalar(node.value)
            elif node.style == YamlScalarStyle.FOLDED:
                self._write_folded_scalar(node.value)
            else:
                escaped = self._escape_scalar(node.value, node.style)
                self._write(escaped)
        elif isinstance(node.value, bytes):
            # Convert bytes to base64 representation
            import base64
            b64_value = base64.b64encode(node.value).decode('ascii')
            self._write(f'!!binary "{b64_value}"')
        else:
            self._write(str(node.value))
    
    def _write_literal_scalar(self, value: str):
        """Write literal scalar (|)."""
        self._write('|')
        self._write_line()
        self._increase_indent()
        
        lines = value.split('\n')
        for line in lines:
            self._write_line(line)
        
        self._decrease_indent()
    
    def _write_folded_scalar(self, value: str):
        """Write folded scalar (>)."""
        self._write('>')
        self._write_line()
        self._increase_indent()
        
        # Simple folding - just write lines
        lines = value.split('\n')
        for line in lines:
            self._write_line(line)
        
        self._decrease_indent()
    
    def visit_yaml_alias(self, node: YamlAlias):
        """Visit YAML alias."""
        self._write(f'*{node.name}')
    
    def visit_yaml_anchor(self, node: YamlAnchor):
        """Visit YAML anchor."""
        if node.name not in self.anchors_written:
            self._write(f'&{node.name} ')
            self.anchors_written.add(node.name)
        
        node.value.accept(self)
    
    def visit_yaml_comment(self, node: YamlComment):
        """Visit YAML comment."""
        if node.inline:
            self._write(f' # {node.text}')
        else:
            self._write(f'# {node.text}')
            self._write_line()
    
    def _extract_key_value(self, key: YamlValue) -> Any:
        """Extract sortable value from key."""
        if isinstance(key, YamlScalar):
            return key.value
        return str(key)


# Convenience functions
def generate_yaml_code(ast: Union[YamlDocument, YamlStream], 
                      style: YamlCodeStyle = YamlCodeStyle.STANDARD) -> str:
    """Generate YAML code from AST with specified style."""
    generator = YamlCodeGenerator(style)
    return generator.generate(ast)


def format_yaml_code(code: str, 
                    style: YamlCodeStyle = YamlCodeStyle.STANDARD) -> str:
    """Format existing YAML code with specified style."""
    try:
        # Parse and regenerate
        from .yaml_parser import parse_yaml_document
        ast = parse_yaml_document(code)
        return generate_yaml_code(ast, style)
    except Exception as e:
        # If parsing fails, return original
        logging.getLogger(__name__).warning(f"Failed to format YAML: {e}")
        return code


def yaml_to_flow_style(code: str) -> str:
    """Convert YAML to flow style."""
    return format_yaml_code(code, YamlCodeStyle.FLOW)


def yaml_to_block_style(code: str) -> str:
    """Convert YAML to block style."""
    return format_yaml_code(code, YamlCodeStyle.BLOCK)


def validate_yaml_format(code: str) -> bool:
    """Validate YAML format."""
    try:
        from .yaml_parser import parse_yaml
        parse_yaml(code)
        return True
    except:
        return False


def yaml_to_python_dict(yaml_document: YamlDocument) -> Any:
    """Convert YAML document to Python dictionary/list."""
    return yaml_value_to_python(yaml_document.content)


def python_dict_to_yaml_code(data: Any, style: YamlCodeStyle = YamlCodeStyle.STANDARD) -> str:
    """Convert Python data to YAML code."""
    yaml_value = yaml_value_from_python(data)
    yaml_document = YamlDocument(content=yaml_value)
    return generate_yaml_code(yaml_document, style)