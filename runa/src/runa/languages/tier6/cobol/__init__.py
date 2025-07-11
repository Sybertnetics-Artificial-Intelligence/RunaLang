#!/usr/bin/env python3
"""
COBOL Language Support for Runa

Complete COBOL toolchain providing parsing, AST conversion, code generation,
and round-trip verification for the Runa universal translation system.
"""

from .cobol_ast import *
from .cobol_parser import parse_cobol, CobolLexer, CobolParser
from .cobol_converter import cobol_to_runa, runa_to_cobol, CobolToRunaConverter, RunaToCobolConverter
from .cobol_generator import generate_cobol, CobolCodeGenerator, CobolCodeStyle, CobolFormatter
from .cobol_toolchain import (
    CobolToolchain,
    parse_cobol_code,
    generate_cobol_code,
    cobol_round_trip_verify,
    cobol_to_runa_translate,
    runa_to_cobol_translate
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete COBOL language toolchain for universal code translation"

# Main toolchain instance
toolchain = CobolToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "CobolToolchain",
    
    # Parser components
    "parse_cobol", "CobolLexer", "CobolParser",
    
    # Converters
    "cobol_to_runa", "runa_to_cobol", "CobolToRunaConverter", "RunaToCobolConverter",
    
    # Generator
    "generate_cobol", "CobolCodeGenerator", "CobolCodeStyle", "CobolFormatter",
    
    # Convenience functions
    "parse_cobol_code", "generate_cobol_code", "cobol_round_trip_verify",
    "cobol_to_runa_translate", "runa_to_cobol_translate",
    
    # AST base classes (main ones)
    "CobolNode", "CobolExpression", "CobolStatement", "CobolDeclaration", "CobolType",
]

# Module metadata
__language__ = "cobol"
__tier__ = 6
__file_extensions__ = [".cob", ".cbl", ".cpy"]
__mime_types__ = ["text/x-cobol"]
