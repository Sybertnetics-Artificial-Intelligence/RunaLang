#!/usr/bin/env python3
"""
XML Code Generator

Generates XML text from XML AST nodes with support for multiple formatting styles.

Author: Sybertnetics AI Solutions
License: MIT
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass
from enum import Enum, auto
import logging

from .xml_ast import *


class XmlCodeStyle(Enum):
    """XML code formatting styles."""
    STANDARD = "standard"
    COMPACT = "compact"
    PRETTY = "pretty"
    MINIFIED = "minified"


@dataclass
class XmlFormattingOptions:
    """XML code formatting options."""
    indent_size: int = 2
    use_tabs: bool = False
    max_line_length: int = 120
    
    # XML-specific
    self_closing_style: str = "/>"  # "/>" or "></tag>"
    attribute_quote_char: str = '"'  # '"' or "'"
    preserve_whitespace: bool = False
    sort_attributes: bool = False
    line_break: str = '\n'
    omit_xml_declaration: bool = False
    standalone_attributes: bool = False  # Put each attribute on new line
    compact_empty_elements: bool = True
    add_xml_declaration: bool = True
    encoding: str = "UTF-8"


class XmlFormatter:
    """XML code formatter with style presets."""
    
    @staticmethod
    def get_style_options(style: XmlCodeStyle) -> XmlFormattingOptions:
        """Get formatting options for a specific style."""
        if style == XmlCodeStyle.STANDARD:
            return XmlFormattingOptions(
                indent_size=2,
                self_closing_style="/>",
                preserve_whitespace=False
            )
        elif style == XmlCodeStyle.COMPACT:
            return XmlFormattingOptions(
                indent_size=1,
                max_line_length=200,
                compact_empty_elements=True,
                omit_xml_declaration=True
            )
        elif style == XmlCodeStyle.PRETTY:
            return XmlFormattingOptions(
                indent_size=4,
                sort_attributes=True,
                standalone_attributes=False,
                preserve_whitespace=True
            )
        elif style == XmlCodeStyle.MINIFIED:
            return XmlFormattingOptions(
                indent_size=0,
                line_break="",
                compact_empty_elements=True,
                omit_xml_declaration=True,
                preserve_whitespace=False
            )
        else:
            return XmlFormattingOptions()


class XmlCodeGenerator(XmlVisitorExtended):
    """XML code generator that produces formatted XML from AST."""
    
    def __init__(self, style: XmlCodeStyle = XmlCodeStyle.STANDARD):
        self.style = style
        self.options = XmlFormatter.get_style_options(style)
        self.logger = logging.getLogger(__name__)
        
        # Output state
        self.output = []
        self.indent_level = 0
        self.current_line_length = 0
        self.needs_indent = True
        self.in_cdata = False
    
    def generate(self, node: XmlNode) -> str:
        """Generate XML text from an AST node."""
        self.output = []
        self.indent_level = 0
        self.current_line_length = 0
        self.needs_indent = True
        self.in_cdata = False
        
        try:
            node.accept(self)
            result = "".join(self.output)
            return self._post_process(result)
        except Exception as e:
            self.logger.error(f"XML code generation failed: {e}")
            raise RuntimeError(f"Failed to generate XML code: {e}")
    
    def _post_process(self, code: str) -> str:
        """Post-process generated code."""
        if self.style == XmlCodeStyle.MINIFIED:
            # Remove unnecessary whitespace for minified style
            lines = code.split('\n')
            processed_lines = []
            for line in lines:
                line = line.strip()
                if line:
                    processed_lines.append(line)
            return ''.join(processed_lines)
        else:
            # Standard post-processing
            lines = code.split('\n')
            processed_lines = []
            
            for line in lines:
                # Remove trailing whitespace
                line = line.rstrip()
                processed_lines.append(line)
            
            # Remove trailing empty lines
            while processed_lines and not processed_lines[-1]:
                processed_lines.pop()
            
            return '\n'.join(processed_lines)
    
    def _write(self, text: str):
        """Write text to output."""
        if self.needs_indent and text.strip() and self.options.line_break:
            self._write_indent()
            self.needs_indent = False
        
        self.output.append(text)
        self.current_line_length += len(text)
    
    def _write_line(self, text: str = ""):
        """Write a line of text."""
        if text:
            self._write(text)
        if self.options.line_break:
            self.output.append(self.options.line_break)
            self.current_line_length = 0
            self.needs_indent = True
    
    def _write_indent(self):
        """Write current indentation."""
        if self.indent_level > 0:
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
    
    def _escape_xml_content(self, text: str) -> str:
        """Escape XML content."""
        if not text:
            return ""
        
        return xml_escape(text)
    
    def _escape_attribute_value(self, value: str) -> str:
        """Escape XML attribute value."""
        escaped = xml_escape(value)
        
        # Escape quotes based on chosen quote character
        if self.options.attribute_quote_char == '"':
            escaped = escaped.replace('"', '&quot;')
        else:
            escaped = escaped.replace("'", '&apos;')
        
        return escaped
    
    def _format_attributes(self, attributes: Dict[str, XmlAttribute]) -> str:
        """Format attributes string."""
        if not attributes:
            return ""
        
        attr_list = list(attributes.values())
        
        # Sort attributes if requested
        if self.options.sort_attributes:
            attr_list.sort(key=lambda attr: attr.name)
        
        parts = []
        quote_char = self.options.attribute_quote_char
        
        for attr in attr_list:
            escaped_value = self._escape_attribute_value(attr.value)
            attr_str = f"{attr.qualified_name}={quote_char}{escaped_value}{quote_char}"
            parts.append(attr_str)
        
        if self.options.standalone_attributes and len(parts) > 1:
            # Put each attribute on its own line
            separator = f"{self.options.line_break}" + " " * (self.indent_level + 1) * self.options.indent_size
            return separator + separator.join(parts)
        else:
            return " " + " ".join(parts)
    
    # Visitor methods
    def visit_xml_document(self, node: XmlDocument):
        """Visit XML document."""
        # Write XML declaration
        if not self.options.omit_xml_declaration and self.options.add_xml_declaration:
            declaration = f'<?xml version="{node.version}" encoding="{node.encoding}"'
            if node.standalone is not None:
                declaration += f' standalone="{"yes" if node.standalone else "no"}"'
            declaration += '?>'
            self._write_line(declaration)
        
        # Write DOCTYPE if present
        if node.doctype:
            node.doctype.accept(self)
            if self.options.line_break:
                self._write_line()
        
        # Write processing instructions
        for pi in node.processing_instructions:
            pi.accept(self)
            if self.options.line_break:
                self._write_line()
        
        # Write comments
        for comment in node.comments:
            comment.accept(self)
            if self.options.line_break:
                self._write_line()
        
        # Write root element
        if node.root_element:
            node.root_element.accept(self)
    
    def visit_xml_element(self, node: XmlElement):
        """Visit XML element."""
        # Opening tag
        tag_name = node.qualified_name
        self._write(f"<{tag_name}")
        
        # Attributes
        if node.attributes:
            attr_str = self._format_attributes(node.attributes)
            self._write(attr_str)
        
        # Handle self-closing elements
        if node.is_self_closing or (not node.children and self.options.compact_empty_elements):
            self._write(self.options.self_closing_style)
            if self.options.line_break:
                self._write_line()
            return
        
        self._write(">")
        
        # Handle children
        if node.children:
            has_complex_children = any(isinstance(child, XmlElement) for child in node.children)
            has_text_content = any(isinstance(child, XmlText) and child.content.strip() for child in node.children)
            
            # Mixed content or complex elements get new lines
            if has_complex_children and self.options.line_break:
                self._write_line()
                self._increase_indent()
                
                for i, child in enumerate(node.children):
                    child.accept(self)
                    # Add line break between complex children
                    if isinstance(child, XmlElement) and i < len(node.children) - 1:
                        self._write_line()
                
                self._decrease_indent()
                self._write_line()
            else:
                # Simple text content - keep inline
                for child in node.children:
                    if isinstance(child, XmlText):
                        content = child.content
                        if not self.options.preserve_whitespace:
                            content = content.strip()
                        if content:
                            self._write(self._escape_xml_content(content))
                    else:
                        child.accept(self)
        
        # Closing tag
        self._write(f"</{tag_name}>")
        if self.options.line_break:
            self._write_line()
    
    def visit_xml_text(self, node: XmlText):
        """Visit XML text."""
        content = node.content
        
        if not self.options.preserve_whitespace and not self.in_cdata:
            content = content.strip()
        
        if content:
            escaped_content = self._escape_xml_content(content)
            self._write(escaped_content)
    
    def visit_xml_comment(self, node: XmlComment):
        """Visit XML comment."""
        self._write(f"<!-- {node.content} -->")
    
    def visit_xml_cdata(self, node: XmlCData):
        """Visit XML CDATA section."""
        self.in_cdata = True
        self._write(f"<![CDATA[{node.content}]]>")
        self.in_cdata = False
    
    def visit_xml_processing_instruction(self, node: XmlProcessingInstruction):
        """Visit XML processing instruction."""
        if node.data:
            self._write(f"<?{node.target} {node.data}?>")
        else:
            self._write(f"<?{node.target}?>")
    
    def visit_xml_doctype(self, node: XmlDoctype):
        """Visit XML DOCTYPE declaration."""
        doctype = f"<!DOCTYPE {node.name}"
        
        if node.external_id:
            doctype += f" {node.external_id}"
        
        if node.system_id:
            doctype += f' "{node.system_id}"'
        
        if node.internal_subset:
            doctype += f" [{node.internal_subset}]"
        
        doctype += ">"
        self._write(doctype)
    
    def visit_xml_attribute(self, node: XmlAttribute):
        """Visit XML attribute (handled by element)."""
        pass  # Attributes are handled by elements
    
    def visit_xml_entity_reference(self, node: XmlEntityReference):
        """Visit XML entity reference."""
        self._write(f"&{node.name};")


# Convenience functions
def generate_xml_code(ast: Union[XmlDocument, XmlElement], 
                     style: XmlCodeStyle = XmlCodeStyle.STANDARD) -> str:
    """Generate XML code from AST with specified style."""
    generator = XmlCodeGenerator(style)
    return generator.generate(ast)


def format_xml_code(code: str, 
                   style: XmlCodeStyle = XmlCodeStyle.STANDARD) -> str:
    """Format existing XML code with specified style."""
    try:
        # Parse and regenerate
        from .xml_parser import parse_xml
        ast = parse_xml(code)
        return generate_xml_code(ast, style)
    except Exception as e:
        # If parsing fails, return original
        logging.getLogger(__name__).warning(f"Failed to format XML: {e}")
        return code


def xml_to_compact_style(code: str) -> str:
    """Convert XML to compact style."""
    return format_xml_code(code, XmlCodeStyle.COMPACT)


def xml_to_pretty_style(code: str) -> str:
    """Convert XML to pretty style."""
    return format_xml_code(code, XmlCodeStyle.PRETTY)


def xml_to_minified_style(code: str) -> str:
    """Convert XML to minified style."""
    return format_xml_code(code, XmlCodeStyle.MINIFIED)


def validate_xml_format(code: str) -> bool:
    """Validate XML format."""
    try:
        from .xml_parser import parse_xml
        parse_xml(code)
        return True
    except:
        return False


def prettify_xml(code: str, indent_size: int = 2) -> str:
    """Prettify XML with custom indentation."""
    try:
        from .xml_parser import parse_xml
        ast = parse_xml(code)
        
        # Create custom formatter
        generator = XmlCodeGenerator(XmlCodeStyle.PRETTY)
        generator.options.indent_size = indent_size
        
        return generator.generate(ast)
    except Exception as e:
        logging.getLogger(__name__).warning(f"Failed to prettify XML: {e}")
        return code


def minify_xml(code: str) -> str:
    """Minify XML by removing unnecessary whitespace."""
    return format_xml_code(code, XmlCodeStyle.MINIFIED)


def xml_to_dict(xml_element: XmlElement) -> Dict[str, Any]:
    """Convert XML element to dictionary representation."""
    return xml_to_dict(xml_element)


def dict_to_xml_code(data: Dict[str, Any], 
                    root_tag: str = "root",
                    style: XmlCodeStyle = XmlCodeStyle.STANDARD) -> str:
    """Convert dictionary to XML code."""
    xml_element = dict_to_xml(data, root_tag)
    xml_document = create_xml_document(xml_element)
    return generate_xml_code(xml_document, style)


def create_xml_declaration(version: str = "1.0", 
                          encoding: str = "UTF-8", 
                          standalone: bool = None) -> str:
    """Create XML declaration string."""
    declaration = f'<?xml version="{version}" encoding="{encoding}"'
    if standalone is not None:
        declaration += f' standalone="{"yes" if standalone else "no"}"'
    declaration += '?>'
    return declaration