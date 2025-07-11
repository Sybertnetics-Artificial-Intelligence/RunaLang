#!/usr/bin/env python3
"""
Starlark Language Support for Runa

Complete Starlark language toolchain providing parsing, AST conversion, code generation,
and round-trip verification for the Runa universal translation system.
"""

from .starlark_ast import *
from .starlark_parser import parse_starlark, StarlarkLexer, StarlarkParser
from .starlark_converter import starlark_to_runa, runa_to_starlark, StarlarkToRunaConverter, RunaToStarlarkConverter
from .starlark_generator import generate_starlark, StarlarkCodeGenerator, StarlarkCodeStyle, StarlarkFormatter
from .starlark_toolchain import (
    StarlarkToolchain,
    parse_starlark_code,
    generate_starlark_code,
    starlark_round_trip_verify,
    starlark_to_runa_translate,
    runa_to_starlark_translate
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete Starlark language toolchain for universal code translation"

# Main toolchain instance
toolchain = StarlarkToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "StarlarkToolchain",
    
    # Parser components
    "parse_starlark", "StarlarkLexer", "StarlarkParser",
    
    # Converters
    "starlark_to_runa", "runa_to_starlark", "StarlarkToRunaConverter", "RunaToStarlarkConverter",
    
    # Generator
    "generate_starlark", "StarlarkCodeGenerator", "StarlarkCodeStyle", "StarlarkFormatter",
    
    # Convenience functions
    "parse_starlark_code", "generate_starlark_code", "starlark_round_trip_verify",
    "starlark_to_runa_translate", "runa_to_starlark_translate",
    
    # AST base classes (main ones)
    "StarlarkNode", "StarlarkExpression", "StarlarkStatement", "StarlarkDeclaration", "StarlarkType",
]

# Module metadata
__language__ = "starlark"
__tier__ = 5
__file_extensions__ = [".star", ".sky", ".bzl"]
__mime_types__ = ["text/x-starlark", "application/x-starlark"]
