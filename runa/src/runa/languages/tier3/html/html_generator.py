#!/usr/bin/env python3
"""
HTML Code Generator

Generates HTML text from HTML AST nodes with support for multiple formatting styles.

Author: Sybertnetics AI Solutions
License: MIT
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass
from enum import Enum, auto
import logging

from .html_ast import *


class HtmlCodeStyle(Enum):
    """HTML code formatting styles."""
    STANDARD = "standard"
    COMPACT = "compact"
    PRETTY = "pretty"
    MINIFIED = "minified"


@dataclass
class HtmlFormattingOptions:
    """HTML code formatting options."""
    indent_size: int = 2
    use_tabs: bool = False
    max_line_length: int = 120
    
    # HTML-specific
    self_closing_style: str = "/>"  # "/>" or "></tag>"
    attribute_quote_char: str = '"'  # '"' or "'"
    lowercase_tags: bool = True
    lowercase_attributes: bool = True
    sort_attributes: bool = False
    line_break: str = '\n'
    omit_optional_tags: bool = False  # Omit optional closing tags like </li>
    void_element_style: str = "self_closing"  # "self_closing" or "open"
    boolean_attribute_style: str = "minimized"  # "minimized" or "explicit"
    preserve_whitespace: bool = False
    add_doctype: bool = True
    
    # Formatting preferences
    inline_elements_on_same_line: bool = True
    block_elements_on_new_lines: bool = True
    empty_elements_on_same_line: bool = True


class HtmlFormatter:
    """HTML code formatter with style presets."""
    
    @staticmethod
    def get_style_options(style: HtmlCodeStyle) -> HtmlFormattingOptions:
        """Get formatting options for a specific style."""
        if style == HtmlCodeStyle.STANDARD:
            return HtmlFormattingOptions(
                indent_size=2,
                lowercase_tags=True,
                lowercase_attributes=True
            )
        elif style == HtmlCodeStyle.COMPACT:
            return HtmlFormattingOptions(
                indent_size=1,
                max_line_length=200,
                inline_elements_on_same_line=True,
                empty_elements_on_same_line=True
            )
        elif style == HtmlCodeStyle.PRETTY:
            return HtmlFormattingOptions(
                indent_size=4,
                sort_attributes=True,
                block_elements_on_new_lines=True,
                preserve_whitespace=True
            )
        elif style == HtmlCodeStyle.MINIFIED:
            return HtmlFormattingOptions(
                indent_size=0,
                line_break="",
                preserve_whitespace=False,
                omit_optional_tags=True,
                inline_elements_on_same_line=True,
                empty_elements_on_same_line=True
            )
        else:
            return HtmlFormattingOptions()


class HtmlCodeGenerator(HtmlVisitorExtended):
    """HTML code generator that produces formatted HTML from AST."""
    
    def __init__(self, style: HtmlCodeStyle = HtmlCodeStyle.STANDARD):
        self.style = style
        self.options = HtmlFormatter.get_style_options(style)
        self.logger = logging.getLogger(__name__)
        
        # Output state
        self.output = []
        self.indent_level = 0
        self.current_line_length = 0
        self.needs_indent = True
        self.in_pre_element = False
    
    def generate(self, node: HtmlNode) -> str:
        """Generate HTML text from an AST node."""
        self.output = []
        self.indent_level = 0
        self.current_line_length = 0
        self.needs_indent = True
        self.in_pre_element = False
        
        try:
            node.accept(self)
            result = "".join(self.output)
            return self._post_process(result)
        except Exception as e:
            self.logger.error(f"HTML code generation failed: {e}")
            raise RuntimeError(f"Failed to generate HTML code: {e}")
    
    def _post_process(self, code: str) -> str:
        """Post-process generated code."""
        if self.style == HtmlCodeStyle.MINIFIED:
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
    
    def _escape_html_content(self, text: str) -> str:
        """Escape HTML content."""
        if not text:
            return ""
        
        return html_escape(text)
    
    def _escape_attribute_value(self, value: str) -> str:
        """Escape HTML attribute value."""
        escaped = html_escape(value)
        
        # Escape quotes based on chosen quote character
        if self.options.attribute_quote_char == '"':
            escaped = escaped.replace('"', '&quot;')
        else:
            escaped = escaped.replace("'", '&#39;')
        
        return escaped
    
    def _format_tag_name(self, tag_name: str) -> str:
        """Format tag name according to options."""
        if self.options.lowercase_tags:
            return tag_name.lower()
        return tag_name
    
    def _format_attribute_name(self, attr_name: str) -> str:
        """Format attribute name according to options."""
        if self.options.lowercase_attributes:
            return attr_name.lower()
        return attr_name
    
    def _format_attributes(self, attributes: Dict[str, HtmlAttribute]) -> str:
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
            attr_name = self._format_attribute_name(attr.name)
            
            if attr.is_boolean and self.options.boolean_attribute_style == "minimized":
                # Boolean attributes like 'disabled', 'checked'
                parts.append(attr_name)
            else:
                escaped_value = self._escape_attribute_value(attr.value)
                attr_str = f"{attr_name}={quote_char}{escaped_value}{quote_char}"
                parts.append(attr_str)
        
        return " " + " ".join(parts) if parts else ""
    
    def _is_inline_element(self, tag_name: str) -> bool:
        """Check if element is inline."""
        return tag_name.lower() in HTML5_INLINE_ELEMENTS
    
    def _is_block_element(self, tag_name: str) -> bool:
        """Check if element is block-level."""
        return tag_name.lower() in HTML5_BLOCK_ELEMENTS
    
    def _should_format_inline(self, element: HtmlElement) -> bool:
        """Determine if element should be formatted inline."""
        if self.in_pre_element:
            return True
        
        if self._is_inline_element(element.tag_name):
            return self.options.inline_elements_on_same_line
        
        if element.is_empty and self.options.empty_elements_on_same_line:
            return True
        
        return False
    
    # Visitor methods
    def visit_html_document(self, node: HtmlDocument):
        """Visit HTML document."""
        # Write DOCTYPE
        if node.doctype and self.options.add_doctype:
            node.doctype.accept(self)
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
    
    def visit_html_element(self, node: HtmlElement):
        """Visit HTML element."""
        tag_name = self._format_tag_name(node.tag_name)
        
        # Track if we're in a <pre> element for whitespace preservation
        was_in_pre = self.in_pre_element
        if tag_name.lower() in ['pre', 'script', 'style']:
            self.in_pre_element = True
        
        # Opening tag
        self._write(f"<{tag_name}")
        
        # Attributes
        if node.attributes:
            attr_str = self._format_attributes(node.attributes)
            self._write(attr_str)
        
        # Handle void elements
        if node.is_void_element:
            if self.options.void_element_style == "self_closing":
                self._write(" />")
            else:
                self._write(">")
            
            if self.options.line_break and not self._should_format_inline(node):
                self._write_line()
            
            self.in_pre_element = was_in_pre
            return
        
        # Handle self-closing elements
        if node.is_self_closing:
            self._write(" />")
            if self.options.line_break and not self._should_format_inline(node):
                self._write_line()
            
            self.in_pre_element = was_in_pre
            return
        
        self._write(">")
        
        # Handle children
        if node.children:
            should_format_inline = self._should_format_inline(node)
            has_block_children = any(
                isinstance(child, HtmlElement) and self._is_block_element(child.tag_name)
                for child in node.children
            )
            has_only_text = all(isinstance(child, HtmlText) for child in node.children)
            
            if has_only_text and should_format_inline:
                # Simple text content - keep inline
                for child in node.children:
                    if isinstance(child, HtmlText):
                        content = child.content
                        if not self.options.preserve_whitespace and not self.in_pre_element:
                            content = content.strip()
                        if content:
                            self._write(self._escape_html_content(content))
            elif has_block_children or not should_format_inline:
                # Block content - use new lines and indentation
                if self.options.line_break:
                    self._write_line()
                    self._increase_indent()
                
                for i, child in enumerate(node.children):
                    child.accept(self)
                    
                    # Add line break between block children
                    if (isinstance(child, HtmlElement) and 
                        self._is_block_element(child.tag_name) and 
                        i < len(node.children) - 1 and
                        self.options.line_break):
                        self._write_line()
                
                if self.options.line_break:
                    self._decrease_indent()
                    self._write_line()
            else:
                # Mixed or inline content
                for child in node.children:
                    child.accept(self)
        
        # Closing tag
        if not self.options.omit_optional_tags or not self._is_optional_closing_tag(tag_name):
            self._write(f"</{tag_name}>")
        
        if self.options.line_break and not self._should_format_inline(node):
            self._write_line()
        
        self.in_pre_element = was_in_pre
    
    def _is_optional_closing_tag(self, tag_name: str) -> bool:
        """Check if closing tag is optional in HTML5."""
        optional_tags = {'li', 'dt', 'dd', 'p', 'rt', 'rp', 'optgroup', 'option', 
                        'colgroup', 'thead', 'tbody', 'tfoot', 'tr', 'td', 'th'}
        return tag_name.lower() in optional_tags
    
    def visit_html_text(self, node: HtmlText):
        """Visit HTML text."""
        content = node.content
        
        if not self.options.preserve_whitespace and not self.in_pre_element:
            # Normalize whitespace unless in <pre> or preserve_whitespace is set
            if not node.preserve_whitespace:
                content = ' '.join(content.split())
        
        if content:
            escaped_content = self._escape_html_content(content)
            self._write(escaped_content)
    
    def visit_html_comment(self, node: HtmlComment):
        """Visit HTML comment."""
        self._write(f"<!-- {node.content} -->")
    
    def visit_html_doctype(self, node: HtmlDoctype):
        """Visit HTML DOCTYPE declaration."""
        if node.is_html5:
            self._write("<!DOCTYPE html>")
        else:
            self._write(f"<!DOCTYPE {node.doctype_string}>")
    
    def visit_html_attribute(self, node: HtmlAttribute):
        """Visit HTML attribute (handled by element)."""
        pass  # Attributes are handled by elements


# Convenience functions
def generate_html_code(ast: Union[HtmlDocument, HtmlElement], 
                      style: HtmlCodeStyle = HtmlCodeStyle.STANDARD) -> str:
    """Generate HTML code from AST with specified style."""
    generator = HtmlCodeGenerator(style)
    return generator.generate(ast)


def format_html_code(code: str, 
                    style: HtmlCodeStyle = HtmlCodeStyle.STANDARD) -> str:
    """Format existing HTML code with specified style."""
    try:
        # Parse and regenerate
        from .html_parser import parse_html
        ast = parse_html(code)
        return generate_html_code(ast, style)
    except Exception as e:
        # If parsing fails, return original
        logging.getLogger(__name__).warning(f"Failed to format HTML: {e}")
        return code


def html_to_compact_style(code: str) -> str:
    """Convert HTML to compact style."""
    return format_html_code(code, HtmlCodeStyle.COMPACT)


def html_to_pretty_style(code: str) -> str:
    """Convert HTML to pretty style."""
    return format_html_code(code, HtmlCodeStyle.PRETTY)


def html_to_minified_style(code: str) -> str:
    """Convert HTML to minified style."""
    return format_html_code(code, HtmlCodeStyle.MINIFIED)


def validate_html_format(code: str) -> bool:
    """Validate HTML format."""
    try:
        from .html_parser import parse_html
        parse_html(code)
        return True
    except:
        return False


def prettify_html(code: str, indent_size: int = 2) -> str:
    """Prettify HTML with custom indentation."""
    try:
        from .html_parser import parse_html
        ast = parse_html(code)
        
        # Create custom formatter
        generator = HtmlCodeGenerator(HtmlCodeStyle.PRETTY)
        generator.options.indent_size = indent_size
        
        return generator.generate(ast)
    except Exception as e:
        logging.getLogger(__name__).warning(f"Failed to prettify HTML: {e}")
        return code


def minify_html(code: str) -> str:
    """Minify HTML by removing unnecessary whitespace."""
    return format_html_code(code, HtmlCodeStyle.MINIFIED)


def html_to_dict(html_element: HtmlElement) -> Dict[str, Any]:
    """Convert HTML element to dictionary representation."""
    return html_to_dict(html_element)


def dict_to_html_code(data: Dict[str, Any], 
                     style: HtmlCodeStyle = HtmlCodeStyle.STANDARD) -> str:
    """Convert dictionary to HTML code."""
    html_element = dict_to_html(data)
    
    # Create a basic document structure
    document = create_html_document()
    if html_element.tag_name.lower() == 'html':
        document.root_element = html_element
    else:
        # Wrap in basic HTML structure
        html_root = create_html_element('html')
        head = create_html_element('head')
        head.add_child(create_html_element('title', content="Generated HTML"))
        body = create_html_element('body')
        body.add_child(html_element)
        html_root.add_child(head)
        html_root.add_child(body)
        document.root_element = html_root
    
    return generate_html_code(document, style)


def create_html5_boilerplate(title: str = "Document", 
                            lang: str = "en",
                            style: HtmlCodeStyle = HtmlCodeStyle.STANDARD) -> str:
    """Create HTML5 boilerplate."""
    html_elem = create_html_element('html', {'lang': lang})
    
    # Head section
    head = create_html_element('head')
    head.add_child(create_html_element('meta', {'charset': 'UTF-8'}))
    head.add_child(create_html_element('meta', {
        'name': 'viewport', 
        'content': 'width=device-width, initial-scale=1.0'
    }))
    head.add_child(create_html_element('title', content=title))
    
    # Body section
    body = create_html_element('body')
    body.add_child(create_html_element('h1', content=title))
    body.add_child(create_html_element('p', content="Hello, World!"))
    
    html_elem.add_child(head)
    html_elem.add_child(body)
    
    document = create_html_document(html_elem)
    return generate_html_code(document, style)


def extract_css_from_html(code: str) -> List[str]:
    """Extract CSS from HTML (from <style> tags and style attributes)."""
    css_blocks = []
    
    try:
        from .html_parser import parse_html
        document = parse_html(code)
        
        if document.root_element:
            # Extract from <style> tags
            style_elements = document.root_element.find_descendants_by_tag('style')
            for style_elem in style_elements:
                css_content = style_elem.get_text_content()
                if css_content.strip():
                    css_blocks.append(css_content.strip())
            
            # Extract from style attributes
            all_elements = document.root_element.find_descendants_by_tag('*')
            for elem in all_elements:
                if isinstance(elem, HtmlElement):
                    style_attr = elem.get_attribute('style')
                    if style_attr and style_attr.value.strip():
                        css_blocks.append(style_attr.value.strip())
    except:
        pass
    
    return css_blocks


def extract_javascript_from_html(code: str) -> List[str]:
    """Extract JavaScript from HTML (from <script> tags)."""
    js_blocks = []
    
    try:
        from .html_parser import parse_html
        document = parse_html(code)
        
        if document.root_element:
            script_elements = document.root_element.find_descendants_by_tag('script')
            for script_elem in script_elements:
                js_content = script_elem.get_text_content()
                if js_content.strip():
                    js_blocks.append(js_content.strip())
    except:
        pass
    
    return js_blocks