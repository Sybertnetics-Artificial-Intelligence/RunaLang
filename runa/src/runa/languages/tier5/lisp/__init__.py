#!/usr/bin/env python3
"""
LISP Language Support for Runa

Complete LISP language toolchain providing parsing, AST conversion, code generation,
and round-trip verification for the Runa universal translation system.
"""

from .lisp_ast import *
from .lisp_parser import parse_lisp, LispLexer, LispParser
from .lisp_converter import lisp_to_runa, runa_to_lisp, LispToRunaConverter, RunaToLispConverter
from .lisp_generator import generate_lisp, LispCodeGenerator, LispCodeStyle, LispFormatter
from .lisp_toolchain import (
    LispToolchain,
    parse_lisp_code,
    generate_lisp_code,
    lisp_round_trip_verify,
    lisp_to_runa_translate,
    runa_to_lisp_translate
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete LISP language toolchain for universal code translation"

# Main toolchain instance
toolchain = LispToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "LispToolchain",
    
    # Parser components
    "parse_lisp", "LispLexer", "LispParser",
    
    # Converters
    "lisp_to_runa", "runa_to_lisp", "LispToRunaConverter", "RunaToLispConverter",
    
    # Generator
    "generate_lisp", "LispCodeGenerator", "LispCodeStyle", "LispFormatter",
    
    # Convenience functions
    "parse_lisp_code", "generate_lisp_code", "lisp_round_trip_verify",
    "lisp_to_runa_translate", "runa_to_lisp_translate",
    
    # AST base classes (main ones)
    "LispNode", "LispExpression", "LispStatement", "LispDeclaration", "LispType",
]

# Module metadata
__language__ = "lisp"
__tier__ = 5
__file_extensions__ = [".lisp", ".lsp", ".l", ".cl"]
__mime_types__ = ["text/x-lisp", "application/x-lisp"]
