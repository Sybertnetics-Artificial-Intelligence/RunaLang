#!/usr/bin/env python3
"""
CSS Language Support for Runa

Complete CSS toolchain providing parsing, AST conversion, code generation,
and round-trip verification for the Runa universal translation system.
"""

from .css_ast import *
from .css_parser import parse_css, parse_css_file, CssLexer, CssParser
from .css_converter import css_to_runa, runa_to_css, CssToRunaConverter, RunaToCssConverter
from .css_generator import generate_css_code, CssCodeGenerator, CssCodeStyle, CssFormatter
from .css_toolchain import (
    CssToolchain,
    create_css_toolchain,
    css_to_runa_translation,
    runa_to_css_translation,
    verify_css_round_trip,
    parse_css_code,
    generate_css_code_from_ast
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete CSS language toolchain for universal code translation"

# Main toolchain instance
toolchain = CssToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "CssToolchain",
    
    # Parser components
    "parse_css", "parse_css_file", "CssLexer", "CssParser",
    
    # Converters
    "css_to_runa", "runa_to_css", "CssToRunaConverter", "RunaToCssConverter",
    
    # Generator
    "generate_css_code", "CssCodeGenerator", "CssCodeStyle", "CssFormatter",
    
    # Convenience functions
    "create_css_toolchain", "css_to_runa_translation", "runa_to_css_translation",
    "verify_css_round_trip", "parse_css_code", "generate_css_code_from_ast",
    
    # AST base classes (main ones)
    "CssNode", "CssStylesheet", "CssRule", "CssSelector", "CssDeclaration", "CssAtRule", "CssComment",
]

# Module metadata
__language__ = "css"
__tier__ = 3
__file_extensions__ = [".css"]
__mime_types__ = ["text/css"]