#!/usr/bin/env python3
"""
R Language Support for Runa

Complete R language toolchain providing parsing, AST conversion, code generation,
and round-trip verification for the Runa universal translation system.
"""

from .r_ast import *
from .r_parser import parse_r, RLexer, RParser
from .r_converter import r_to_runa, runa_to_r, RToRunaConverter, RunaToRConverter
from .r_generator import generate_r, RCodeGenerator, RCodeStyle, RFormatter
from .r_toolchain import (
    RToolchain,
    parse_r_code,
    generate_r_code,
    r_round_trip_verify,
    r_to_runa_translate,
    runa_to_r_translate
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete R language toolchain for universal code translation"

# Main toolchain instance
toolchain = RToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "RToolchain",
    
    # Parser components
    "parse_r", "RLexer", "RParser",
    
    # Converters
    "r_to_runa", "runa_to_r", "RToRunaConverter", "RunaToRConverter",
    
    # Generator
    "generate_r", "RCodeGenerator", "RCodeStyle", "RFormatter",
    
    # Convenience functions
    "parse_r_code", "generate_r_code", "r_round_trip_verify",
    "r_to_runa_translate", "runa_to_r_translate",
    
    # AST base classes (main ones)
    "RNode", "RExpression", "RStatement", "RDeclaration",
]

# Module metadata
__language__ = "r"
__tier__ = 4
__file_extensions__ = [".r", ".R"]
__mime_types__ = ["text/x-r"]