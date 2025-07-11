#!/usr/bin/env python3
"""
PHP Language Support for Runa

Complete PHP toolchain providing parsing, AST conversion, code generation,
and round-trip verification for the Runa universal translation system.
"""

from .php_ast import *
from .php_parser import parse_php_code, PhpLexer, PhpParser
from .php_converter import php_to_runa, runa_to_php, PhpToRunaConverter, RunaToPhpConverter
from .php_generator import generate_php_code, PhpCodeGenerator, PhpCodeStyle, PhpFormatter
from .php_toolchain import (
    PhpToolchain,
    create_php_toolchain,
    php_to_runa_translation,
    runa_to_php_translation,
    verify_php_round_trip
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete PHP language toolchain for universal code translation"

# Main toolchain instance
toolchain = PhpToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "PhpToolchain",
    
    # Parser components
    "parse_php_code", "PhpLexer", "PhpParser",
    
    # Converters
    "php_to_runa", "runa_to_php", "PhpToRunaConverter", "RunaToPhpConverter",
    
    # Generator
    "generate_php_code", "PhpCodeGenerator", "PhpCodeStyle", "PhpFormatter",
    
    # Convenience functions
    "create_php_toolchain", "php_to_runa_translation", "runa_to_php_translation",
    "verify_php_round_trip",
    
    # AST base classes (main ones)
    "PhpNode", "PhpExpression", "PhpStatement", "PhpDeclaration", "PhpType",
]

# Module metadata
__language__ = "php"
__tier__ = 2
__file_extensions__ = [".php", ".phtml", ".php3", ".php4", ".php5", ".phps"]
__mime_types__ = ["text/x-php", "application/x-httpd-php"]