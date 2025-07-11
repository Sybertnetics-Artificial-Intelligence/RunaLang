#!/usr/bin/env python3
"""
HTML Language Support for Runa

Complete HTML toolchain providing parsing, AST conversion, code generation,
and round-trip verification for the Runa universal translation system.
"""

from .html_ast import *
from .html_parser import parse_html, parse_html_file, parse_html_fragment, HtmlLexer, HtmlParser
from .html_converter import html_to_runa, runa_to_html, HtmlToRunaConverter, RunaToHtmlConverter
from .html_generator import generate_html_code, HtmlCodeGenerator, HtmlCodeStyle, HtmlFormatter
from .html_toolchain import (
    HtmlToolchain,
    create_html_toolchain,
    html_to_runa_translation,
    runa_to_html_translation,
    verify_html_round_trip,
    parse_html_code,
    generate_html_code_from_ast
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete HTML language toolchain for universal code translation"

# Main toolchain instance
toolchain = HtmlToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "HtmlToolchain",
    
    # Parser components
    "parse_html", "parse_html_file", "parse_html_fragment", "HtmlLexer", "HtmlParser",
    
    # Converters
    "html_to_runa", "runa_to_html", "HtmlToRunaConverter", "RunaToHtmlConverter",
    
    # Generator
    "generate_html_code", "HtmlCodeGenerator", "HtmlCodeStyle", "HtmlFormatter",
    
    # Convenience functions
    "create_html_toolchain", "html_to_runa_translation", "runa_to_html_translation",
    "verify_html_round_trip", "parse_html_code", "generate_html_code_from_ast",
    
    # AST base classes (main ones)
    "HtmlNode", "HtmlDocument", "HtmlElement", "HtmlText", "HtmlComment", "HtmlDoctype",
]

# Module metadata
__language__ = "html"
__tier__ = 3
__file_extensions__ = [".html", ".htm", ".xhtml"]
__mime_types__ = ["text/html", "application/xhtml+xml"]