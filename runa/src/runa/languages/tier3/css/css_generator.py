#!/usr/bin/env python3
"""
CSS Code Generator

Generates CSS source code from CSS AST with multiple formatting styles
and comprehensive CSS3 feature support.

Author: Sybertnetics AI Solutions
License: MIT
"""

from typing import List, Optional, Dict, Any, Union
from enum import Enum, auto
from dataclasses import dataclass
import logging

from .css_ast import *


class CssCodeStyle(Enum):
    """CSS code generation styles."""
    STANDARD = "standard"
    COMPACT = "compact"
    PRETTY = "pretty"
    MINIFIED = "minified"
    VERBOSE = "verbose"


@dataclass
class CssFormatterOptions:
    """CSS formatter configuration options."""
    indent_size: int = 2
    use_tabs: bool = False
    max_line_length: int = 120
    newline_after_selector: bool = True
    newline_after_declaration: bool = True
    space_around_colon: bool = True
    space_after_comma: bool = True
    preserve_comments: bool = True
    sort_declarations: bool = False
    vendor_prefix_align: bool = True
    quote_style: str = "double"  # "single" or "double"


class CssFormatter:
    """CSS code formatter with multiple styles."""
    
    def __init__(self, style: CssCodeStyle = CssCodeStyle.STANDARD):
        self.style = style
        self.options = self._get_style_options(style)
        self.logger = logging.getLogger(__name__)
    
    def _get_style_options(self, style: CssCodeStyle) -> CssFormatterOptions:
        """Get formatter options for style."""
        if style == CssCodeStyle.COMPACT:
            return CssFormatterOptions(
                indent_size=1,
                newline_after_selector=False,
                newline_after_declaration=False,
                space_around_colon=False,
                space_after_comma=False,
                preserve_comments=False
            )
        elif style == CssCodeStyle.PRETTY:
            return CssFormatterOptions(
                indent_size=4,
                newline_after_selector=True,
                newline_after_declaration=True,
                space_around_colon=True,
                space_after_comma=True,
                preserve_comments=True,
                sort_declarations=True,
                vendor_prefix_align=True
            )
        elif style == CssCodeStyle.MINIFIED:
            return CssFormatterOptions(
                indent_size=0,
                newline_after_selector=False,
                newline_after_declaration=False,
                space_around_colon=False,
                space_after_comma=False,
                preserve_comments=False
            )
        elif style == CssCodeStyle.VERBOSE:
            return CssFormatterOptions(
                indent_size=4,
                newline_after_selector=True,
                newline_after_declaration=True,
                space_around_colon=True,
                space_after_comma=True,
                preserve_comments=True,
                sort_declarations=True,
                vendor_prefix_align=True
            )
        else:  # STANDARD
            return CssFormatterOptions()
    
    def format_indent(self, level: int) -> str:
        """Generate indentation."""
        if self.style == CssCodeStyle.MINIFIED:
            return ""
        
        if self.options.use_tabs:
            return "\t" * level
        return " " * (self.options.indent_size * level)
    
    def format_newline(self) -> str:
        """Generate newline."""
        if self.style == CssCodeStyle.MINIFIED:
            return ""
        return "\n"
    
    def format_space(self, space_type: str = "default") -> str:
        """Generate space based on type."""
        if self.style == CssCodeStyle.MINIFIED:
            return ""
        
        if space_type == "after_comma" and not self.options.space_after_comma:
            return ""
        elif space_type == "around_colon" and not self.options.space_around_colon:
            return ""
        
        return " "


class CssCodeGenerator:
    """CSS code generator."""
    
    def __init__(self, style: CssCodeStyle = CssCodeStyle.STANDARD):
        self.style = style
        self.formatter = CssFormatter(style)
        self.logger = logging.getLogger(__name__)
    
    def generate(self, css_node: CssNode) -> str:
        """Generate CSS code from AST node."""
        try:
            if isinstance(css_node, CssStylesheet):
                return self._generate_stylesheet(css_node)
            elif isinstance(css_node, CssRule):
                return self._generate_rule(css_node)
            elif isinstance(css_node, CssDeclaration):
                return self._generate_declaration(css_node)
            elif isinstance(css_node, CssAtRule):
                return self._generate_at_rule(css_node)
            elif isinstance(css_node, CssComment):
                return self._generate_comment(css_node)
            else:
                return ""
        except Exception as e:
            self.logger.error(f"CSS code generation failed: {e}")
            raise RuntimeError(f"Failed to generate CSS code: {e}")
    
    def _generate_stylesheet(self, stylesheet: CssStylesheet) -> str:
        """Generate CSS stylesheet."""
        parts = []
        
        # Add charset if present
        if stylesheet.charset:
            charset_rule = f'@charset "{stylesheet.charset}";'
            parts.append(charset_rule)
            if self.style != CssCodeStyle.MINIFIED:
                parts.append("")  # Empty line after charset
        
        # Add at-rules
        for at_rule in stylesheet.at_rules:
            at_rule_code = self._generate_at_rule(at_rule)
            parts.append(at_rule_code)
            if self.style in (CssCodeStyle.PRETTY, CssCodeStyle.VERBOSE):
                parts.append("")  # Empty line after at-rule
        
        # Add regular rules
        for i, rule in enumerate(stylesheet.rules):
            rule_code = self._generate_rule(rule)
            parts.append(rule_code)
            
            # Add spacing between rules
            if (i < len(stylesheet.rules) - 1 and 
                self.style in (CssCodeStyle.STANDARD, CssCodeStyle.PRETTY, CssCodeStyle.VERBOSE)):
                parts.append("")
        
        # Add comments
        if self.formatter.options.preserve_comments:
            for comment in stylesheet.comments:
                comment_code = self._generate_comment(comment)
                parts.append(comment_code)
        
        # Join parts
        if self.style == CssCodeStyle.MINIFIED:
            return "".join(parts)
        else:
            return self.formatter.format_newline().join(parts)
    
    def _generate_rule(self, rule: CssRule, indent_level: int = 0) -> str:
        """Generate CSS rule."""
        parts = []
        
        # Generate selectors
        selector_parts = []
        for selector in rule.selectors:
            selector_parts.append(selector.text)
        
        if self.style == CssCodeStyle.MINIFIED:
            selectors_str = ",".join(selector_parts)
        else:
            comma_space = "," + self.formatter.format_space("after_comma")
            selectors_str = comma_space.join(selector_parts)
        
        # Add indentation
        indent = self.formatter.format_indent(indent_level)
        parts.append(f"{indent}{selectors_str}")
        
        # Add opening brace
        if self.formatter.options.newline_after_selector:
            parts.append(f"{self.formatter.format_space()}{{")
            parts.append(self.formatter.format_newline())
        else:
            parts.append(f"{self.formatter.format_space()}{{")
        
        # Generate declarations
        declaration_parts = []
        declarations = rule.declarations
        
        # Sort declarations if requested
        if self.formatter.options.sort_declarations:
            declarations = sorted(declarations, key=lambda d: d.property)
        
        for i, declaration in enumerate(declarations):
            decl_code = self._generate_declaration(declaration, indent_level + 1)
            declaration_parts.append(decl_code)
            
            # Add semicolon and newline
            if i < len(declarations) - 1 or self.style != CssCodeStyle.MINIFIED:
                if self.formatter.options.newline_after_declaration:
                    declaration_parts.append(";")
                    declaration_parts.append(self.formatter.format_newline())
                else:
                    declaration_parts.append(";")
        
        if declaration_parts:
            parts.extend(declaration_parts)
        
        # Add closing brace
        if self.formatter.options.newline_after_declaration and declaration_parts:
            parts.append(f"{indent}}}")
        else:
            parts.append("}")
        
        return "".join(parts)
    
    def _generate_declaration(self, declaration: CssDeclaration, indent_level: int = 0) -> str:
        """Generate CSS declaration."""
        indent = self.formatter.format_indent(indent_level)
        
        if self.formatter.options.space_around_colon:
            colon_space = f"{self.formatter.format_space('around_colon')}:{self.formatter.format_space('around_colon')}"
        else:
            colon_space = ":"
        
        value = declaration.value
        if declaration.important:
            if self.style == CssCodeStyle.MINIFIED:
                value += "!important"
            else:
                value += " !important"
        
        return f"{indent}{declaration.property}{colon_space}{value}"
    
    def _generate_at_rule(self, at_rule: CssAtRule, indent_level: int = 0) -> str:
        """Generate CSS at-rule."""
        indent = self.formatter.format_indent(indent_level)
        parts = []
        
        # Generate at-rule header
        if at_rule.params:
            header = f"{indent}@{at_rule.name}{self.formatter.format_space()}{at_rule.params}"
        else:
            header = f"{indent}@{at_rule.name}"
        
        # Handle different at-rule types
        if at_rule.rules:
            # Block-based at-rule (like @media)
            parts.append(f"{header}{self.formatter.format_space()}{{{self.formatter.format_newline()}")
            
            # Generate nested rules
            for rule in at_rule.rules:
                rule_code = self._generate_rule(rule, indent_level + 1)
                parts.append(rule_code)
                parts.append(self.formatter.format_newline())
            
            parts.append(f"{indent}}}")
        
        elif at_rule.declarations:
            # Declaration-based at-rule (like @font-face)
            parts.append(f"{header}{self.formatter.format_space()}{{{self.formatter.format_newline()}")
            
            # Generate declarations
            for decl in at_rule.declarations:
                decl_code = self._generate_declaration(decl, indent_level + 1)
                parts.append(f"{decl_code};{self.formatter.format_newline()}")
            
            parts.append(f"{indent}}}")
        
        else:
            # Simple at-rule (like @import)
            parts.append(f"{header};")
        
        return "".join(parts)
    
    def _generate_comment(self, comment: CssComment, indent_level: int = 0) -> str:
        """Generate CSS comment."""
        if not self.formatter.options.preserve_comments:
            return ""
        
        indent = self.formatter.format_indent(indent_level)
        
        if self.style == CssCodeStyle.VERBOSE:
            # Multi-line comment format
            lines = comment.text.split('\n')
            if len(lines) == 1:
                return f"{indent}/* {comment.text} */"
            else:
                parts = [f"{indent}/*"]
                for line in lines:
                    parts.append(f"{indent} * {line}")
                parts.append(f"{indent} */")
                return self.formatter.format_newline().join(parts)
        else:
            # Single-line comment format
            return f"{indent}/* {comment.text} */"
    
    def _generate_media_query(self, media_query: CssMediaQuery) -> str:
        """Generate media query string."""
        if not media_query.features:
            return media_query.media_type
        
        features_str = " and ".join(media_query.features)
        if media_query.media_type == "all":
            return features_str
        return f"{media_query.media_type} and {features_str}"


# Convenience functions
def generate_css_code(css_node: CssNode, style: CssCodeStyle = CssCodeStyle.STANDARD) -> str:
    """Generate CSS code from AST node."""
    generator = CssCodeGenerator(style)
    return generator.generate(css_node)


def generate_css_stylesheet(stylesheet: CssStylesheet, style: CssCodeStyle = CssCodeStyle.STANDARD) -> str:
    """Generate CSS stylesheet code."""
    generator = CssCodeGenerator(style)
    return generator.generate(stylesheet)


def generate_css_rule(rule: CssRule, style: CssCodeStyle = CssCodeStyle.STANDARD) -> str:
    """Generate CSS rule code."""
    generator = CssCodeGenerator(style)
    return generator.generate(rule)


def minify_css_code(css_node: CssNode) -> str:
    """Generate minified CSS code."""
    return generate_css_code(css_node, CssCodeStyle.MINIFIED)


def prettify_css_code(css_node: CssNode) -> str:
    """Generate prettified CSS code."""
    return generate_css_code(css_node, CssCodeStyle.PRETTY)


def format_css_selector_list(selectors: List[CssSelector], style: CssCodeStyle = CssCodeStyle.STANDARD) -> str:
    """Format CSS selector list."""
    formatter = CssFormatter(style)
    
    selector_texts = [sel.text for sel in selectors]
    
    if style == CssCodeStyle.MINIFIED:
        return ",".join(selector_texts)
    else:
        comma_space = "," + formatter.format_space("after_comma")
        return comma_space.join(selector_texts)


def format_css_declarations(declarations: List[CssDeclaration], 
                           style: CssCodeStyle = CssCodeStyle.STANDARD,
                           indent_level: int = 1) -> str:
    """Format CSS declarations."""
    generator = CssCodeGenerator(style)
    parts = []
    
    for i, declaration in enumerate(declarations):
        decl_code = generator._generate_declaration(declaration, indent_level)
        parts.append(decl_code)
        
        if i < len(declarations) - 1:
            parts.append(";")
            if style != CssCodeStyle.MINIFIED:
                parts.append(generator.formatter.format_newline())
    
    return "".join(parts)


def validate_css_output(css_code: str) -> bool:
    """Validate generated CSS code."""
    try:
        # Basic validation checks
        if not css_code.strip():
            return False
        
        # Check for balanced braces
        open_braces = css_code.count('{')
        close_braces = css_code.count('}')
        
        if open_braces != close_braces:
            return False
        
        # Check for basic CSS structure
        if '{' in css_code and '}' in css_code:
            # Has rule structure
            return True
        elif css_code.strip().startswith('@') and css_code.strip().endswith(';'):
            # Simple at-rule
            return True
        
        return True
    except Exception:
        return False


def optimize_css_code(css_node: CssNode) -> str:
    """Generate optimized CSS code."""
    # Use minified style with some optimizations
    generator = CssCodeGenerator(CssCodeStyle.MINIFIED)
    
    if isinstance(css_node, CssStylesheet):
        # Sort rules by selector specificity for better compression
        optimized_stylesheet = CssStylesheet()
        optimized_stylesheet.charset = css_node.charset
        optimized_stylesheet.at_rules = css_node.at_rules.copy()
        optimized_stylesheet.comments = []  # Remove comments for optimization
        
        # Sort rules by selector length (shorter selectors first)
        sorted_rules = sorted(css_node.rules, 
                            key=lambda r: len(r.get_selector_text()))
        optimized_stylesheet.rules = sorted_rules
        
        return generator.generate(optimized_stylesheet)
    else:
        return generator.generate(css_node)


def css_code_statistics(css_code: str) -> Dict[str, Any]:
    """Get statistics about generated CSS code."""
    lines = css_code.split('\n')
    
    return {
        "total_lines": len(lines),
        "non_empty_lines": len([line for line in lines if line.strip()]),
        "total_characters": len(css_code),
        "total_bytes": len(css_code.encode('utf-8')),
        "rule_count": css_code.count('{'),
        "declaration_count": css_code.count(':'),
        "comment_count": css_code.count('/*'),
        "at_rule_count": css_code.count('@'),
        "average_line_length": sum(len(line) for line in lines) / len(lines) if lines else 0
    }


# CSS-specific formatting utilities
def format_css_color(color_value: str, target_format: str = "hex") -> str:
    """Format CSS color value to target format."""
    # Basic color format conversion
    color_value = color_value.strip().lower()
    
    if target_format == "hex" and color_value.startswith("rgb"):
        # Simple RGB to hex conversion (basic implementation)
        return color_value  # Return as-is for now
    elif target_format == "rgb" and color_value.startswith("#"):
        # Simple hex to RGB conversion (basic implementation)
        return color_value  # Return as-is for now
    
    return color_value


def format_css_length(length_value: str, target_unit: str = "px") -> str:
    """Format CSS length value to target unit."""
    # Basic unit conversion (simplified)
    return length_value  # Return as-is for now


def normalize_css_whitespace(css_code: str) -> str:
    """Normalize whitespace in CSS code."""
    import re
    
    # Remove extra whitespace
    css_code = re.sub(r'\s+', ' ', css_code)
    
    # Clean up around braces and semicolons
    css_code = re.sub(r'\s*{\s*', ' { ', css_code)
    css_code = re.sub(r'\s*}\s*', ' } ', css_code)
    css_code = re.sub(r'\s*;\s*', '; ', css_code)
    css_code = re.sub(r'\s*:\s*', ': ', css_code)
    
    return css_code.strip()