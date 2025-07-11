#!/usr/bin/env python3
"""
JSON Code Generator

Generates JSON text from JSON AST nodes with support for multiple formatting styles.

Author: Sybertnetics AI Solutions
License: MIT
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass
from enum import Enum, auto
import logging
import json as python_json

from .json_ast import *


class JsonCodeStyle(Enum):
    """JSON code formatting styles."""
    COMPACT = "compact"
    PRETTY = "pretty"
    MINIFIED = "minified"
    READABLE = "readable"


@dataclass
class JsonFormattingOptions:
    """JSON code formatting options."""
    indent_size: int = 2
    use_tabs: bool = False
    max_line_length: int = 120
    
    # JSON-specific
    sort_keys: bool = False
    ensure_ascii: bool = False
    separators: tuple = (',', ': ')
    trailing_comma: bool = False
    quote_keys: bool = True
    allow_nan: bool = False
    escape_forward_slashes: bool = False


class JsonFormatter:
    """JSON code formatter with style presets."""
    
    @staticmethod
    def get_style_options(style: JsonCodeStyle) -> JsonFormattingOptions:
        """Get formatting options for a specific style."""
        if style == JsonCodeStyle.COMPACT:
            return JsonFormattingOptions(
                indent_size=2,
                separators=(',', ': '),
                sort_keys=False
            )
        elif style == JsonCodeStyle.PRETTY:
            return JsonFormattingOptions(
                indent_size=2,
                separators=(',', ': '),
                sort_keys=True
            )
        elif style == JsonCodeStyle.MINIFIED:
            return JsonFormattingOptions(
                indent_size=0,
                separators=(',', ':'),
                sort_keys=False
            )
        elif style == JsonCodeStyle.READABLE:
            return JsonFormattingOptions(
                indent_size=4,
                separators=(',', ': '),
                sort_keys=True,
                trailing_comma=False
            )
        else:
            return JsonFormattingOptions()


class JsonCodeGenerator(JsonVisitor):
    """JSON code generator that produces formatted JSON from AST."""
    
    def __init__(self, style: JsonCodeStyle = JsonCodeStyle.PRETTY):
        self.style = style
        self.options = JsonFormatter.get_style_options(style)
        self.logger = logging.getLogger(__name__)
        
        # Output state
        self.output = []
        self.indent_level = 0
        self.current_line_length = 0
        self.needs_indent = True
        self.in_array = False
        self.in_object = False
    
    def generate(self, node: JsonNode) -> str:
        """Generate JSON text from an AST node."""
        self.output = []
        self.indent_level = 0
        self.current_line_length = 0
        self.needs_indent = True
        self.in_array = False
        self.in_object = False
        
        try:
            node.accept(self)
            result = "".join(self.output)
            return self._post_process(result)
        except Exception as e:
            self.logger.error(f"JSON code generation failed: {e}")
            raise RuntimeError(f"Failed to generate JSON code: {e}")
    
    def _post_process(self, code: str) -> str:
        """Post-process generated code."""
        # Remove trailing whitespace from lines
        lines = code.split('\n')
        processed_lines = [line.rstrip() for line in lines]
        
        result = '\n'.join(processed_lines)
        
        # Ensure final newline for pretty styles
        if self.style != JsonCodeStyle.MINIFIED and result and not result.endswith('\n'):
            result += '\n'
        
        return result
    
    def _write(self, text: str):
        """Write text to output."""
        if self.needs_indent and text.strip() and self.style != JsonCodeStyle.MINIFIED:
            self._write_indent()
            self.needs_indent = False
        
        self.output.append(text)
        self.current_line_length += len(text)
    
    def _write_line(self, text: str = ""):
        """Write a line of text."""
        if text:
            self._write(text)
        
        if self.style != JsonCodeStyle.MINIFIED:
            self.output.append('\n')
            self.current_line_length = 0
            self.needs_indent = True
    
    def _write_indent(self):
        """Write current indentation."""
        if self.style == JsonCodeStyle.MINIFIED:
            return
        
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
    
    def _write_separator(self, separator: str):
        """Write separator (comma or colon)."""
        self._write(separator)
        
        # Add space after separator if not minified
        if self.style != JsonCodeStyle.MINIFIED and separator in [',', ':']:
            if separator == ',' and not self._should_break_line():
                self._write(' ')
            elif separator == ':':
                self._write(' ')
    
    def _should_break_line(self) -> bool:
        """Check if line should be broken."""
        if self.style == JsonCodeStyle.MINIFIED:
            return False
        
        return (self.current_line_length > self.options.max_line_length or
                self.style in [JsonCodeStyle.PRETTY, JsonCodeStyle.READABLE])
    
    def _escape_string(self, value: str) -> str:
        """Escape string for JSON output."""
        # Use Python's JSON encoder for proper escaping
        return python_json.dumps(value, ensure_ascii=self.options.ensure_ascii)[1:-1]
    
    # Visitor methods
    def visit_json_document(self, node: JsonDocument):
        """Visit JSON document."""
        node.root.accept(self)
    
    def visit_json_object(self, node: JsonObject):
        """Visit JSON object."""
        self._write('{')
        
        if node.properties:
            if self._should_break_line():
                self._write_line()
                self._increase_indent()
            
            # Sort properties if requested
            properties = node.properties
            if self.options.sort_keys:
                properties = sorted(properties, key=lambda p: p.key.value)
            
            for i, prop in enumerate(properties):
                if i > 0:
                    self._write(self.options.separators[0])  # comma
                    if self._should_break_line():
                        self._write_line()
                
                prop.accept(self)
            
            # Handle trailing comma
            if self.options.trailing_comma and properties:
                self._write(self.options.separators[0])
            
            if self._should_break_line():
                self._write_line()
                self._decrease_indent()
        
        self._write('}')
    
    def visit_json_array(self, node: JsonArray):
        """Visit JSON array."""
        self._write('[')
        
        if node.elements:
            if self._should_break_line():
                self._write_line()
                self._increase_indent()
            
            for i, element in enumerate(node.elements):
                if i > 0:
                    self._write(self.options.separators[0])  # comma
                    if self._should_break_line():
                        self._write_line()
                
                element.accept(self)
            
            # Handle trailing comma
            if self.options.trailing_comma and node.elements:
                self._write(self.options.separators[0])
            
            if self._should_break_line():
                self._write_line()
                self._decrease_indent()
        
        self._write(']')
    
    def visit_json_property(self, node: JsonProperty):
        """Visit JSON property."""
        # Write key
        node.key.accept(self)
        
        # Write colon separator
        self._write(self.options.separators[1])  # colon
        
        # Write value
        node.value.accept(self)
    
    def visit_json_string(self, node: JsonString):
        """Visit JSON string."""
        escaped_value = self._escape_string(node.value)
        self._write(f'"{escaped_value}"')
    
    def visit_json_number(self, node: JsonNumber):
        """Visit JSON number."""
        if node.is_integer:
            self._write(str(int(node.value)))
        else:
            # Format float with appropriate precision
            if abs(node.value) < 1e-6 or abs(node.value) > 1e15:
                # Use scientific notation for very small or very large numbers
                self._write(f"{node.value:e}")
            else:
                # Use regular notation, removing trailing zeros
                formatted = f"{node.value:g}"
                self._write(formatted)
    
    def visit_json_boolean(self, node: JsonBoolean):
        """Visit JSON boolean."""
        self._write('true' if node.value else 'false')
    
    def visit_json_null(self, node: JsonNull):
        """Visit JSON null."""
        self._write('null')


class JsonSchemaGenerator:
    """Generator for JSON Schema."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def infer_schema(self, json_value: JsonValue) -> Dict[str, Any]:
        """Infer JSON Schema from JSON value."""
        if isinstance(json_value, JsonNull):
            return {"type": "null"}
        elif isinstance(json_value, JsonBoolean):
            return {"type": "boolean"}
        elif isinstance(json_value, JsonString):
            return {"type": "string"}
        elif isinstance(json_value, JsonNumber):
            if json_value.is_integer:
                return {"type": "integer"}
            else:
                return {"type": "number"}
        elif isinstance(json_value, JsonArray):
            schema = {"type": "array"}
            if json_value.elements:
                # Infer schema from first element
                item_schema = self.infer_schema(json_value.elements[0])
                schema["items"] = item_schema
            return schema
        elif isinstance(json_value, JsonObject):
            schema = {
                "type": "object",
                "properties": {},
                "required": []
            }
            
            for prop in json_value.properties:
                prop_schema = self.infer_schema(prop.value)
                schema["properties"][prop.key.value] = prop_schema
                
                # Consider all properties required for now
                schema["required"].append(prop.key.value)
            
            return schema
        else:
            return {"type": "null"}
    
    def generate_schema(self, json_document: JsonDocument) -> str:
        """Generate JSON Schema for a JSON document."""
        schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "Generated Schema",
            "description": "Auto-generated JSON Schema"
        }
        
        root_schema = self.infer_schema(json_document.root)
        schema.update(root_schema)
        
        # Generate formatted JSON Schema
        generator = JsonCodeGenerator(JsonCodeStyle.PRETTY)
        schema_ast = json_value_from_python(schema)
        return generator.generate(JsonDocument(root=schema_ast))


# Convenience functions
def generate_json_code(ast: JsonDocument, 
                      style: JsonCodeStyle = JsonCodeStyle.PRETTY) -> str:
    """Generate JSON code from AST with specified style."""
    generator = JsonCodeGenerator(style)
    return generator.generate(ast)


def format_json_code(code: str, 
                    style: JsonCodeStyle = JsonCodeStyle.PRETTY) -> str:
    """Format existing JSON code with specified style."""
    try:
        # Parse and regenerate
        from .json_parser import parse_json_strict
        ast = parse_json_strict(code)
        return generate_json_code(ast, style)
    except Exception as e:
        # If parsing fails, return original
        logging.getLogger(__name__).warning(f"Failed to format JSON: {e}")
        return code


def minify_json(code: str) -> str:
    """Minify JSON code."""
    return format_json_code(code, JsonCodeStyle.MINIFIED)


def prettify_json(code: str) -> str:
    """Prettify JSON code."""
    return format_json_code(code, JsonCodeStyle.PRETTY)


def generate_json_schema(json_document: JsonDocument) -> str:
    """Generate JSON Schema for a JSON document."""
    generator = JsonSchemaGenerator()
    return generator.generate_schema(json_document)


def validate_json_format(code: str) -> bool:
    """Validate JSON format."""
    try:
        python_json.loads(code)
        return True
    except:
        return False


def json_to_python_dict(json_document: JsonDocument) -> Any:
    """Convert JSON document to Python dictionary/list."""
    return json_value_to_python(json_document.root)


def python_dict_to_json_code(data: Any, style: JsonCodeStyle = JsonCodeStyle.PRETTY) -> str:
    """Convert Python data to JSON code."""
    json_value = json_value_from_python(data)
    json_document = JsonDocument(root=json_value)
    return generate_json_code(json_document, style)