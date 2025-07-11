#!/usr/bin/env python3
"""
Rholang Language Support for Runa

Complete Rholang language toolchain providing parsing, AST conversion, code generation,
and round-trip verification for the Runa universal translation system.
"""

from .rholang_ast import *
from .rholang_parser import parse_rholang, RholangLexer, RholangParser
from .rholang_converter import rholang_to_runa, runa_to_rholang, RholangToRunaConverter, RunaToRholangConverter
from .rholang_generator import generate_rholang, RholangCodeGenerator, RholangCodeStyle, RholangFormatter
from .rholang_toolchain import (
    RholangToolchain,
    parse_rholang_code,
    generate_rholang_code,
    rholang_round_trip_verify,
    rholang_to_runa_translate,
    runa_to_rholang_translate
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete Rholang language toolchain for universal code translation"

# Main toolchain instance
toolchain = RholangToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "RholangToolchain",
    
    # Parser components
    "parse_rholang", "RholangLexer", "RholangParser",
    
    # Converters
    "rholang_to_runa", "runa_to_rholang", "RholangToRunaConverter", "RunaToRholangConverter",
    
    # Generator
    "generate_rholang", "RholangCodeGenerator", "RholangCodeStyle", "RholangFormatter",
    
    # Convenience functions
    "parse_rholang_code", "generate_rholang_code", "rholang_round_trip_verify",
    "rholang_to_runa_translate", "runa_to_rholang_translate",
    
    # AST base classes (main ones)
    "RholangNode", "RholangExpression", "RholangStatement", "RholangDeclaration", "RholangType",
]

# Module metadata
__language__ = "rholang"
__tier__ = 5
__file_extensions__ = [".rho"]
__mime_types__ = ["text/x-rholang", "application/x-rholang"]
