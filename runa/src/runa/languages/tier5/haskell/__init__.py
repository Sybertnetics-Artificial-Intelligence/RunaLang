#!/usr/bin/env python3
"""
Haskell Language Support for Runa

Complete Haskell language toolchain providing parsing, AST conversion, code generation,
and round-trip verification for the Runa universal translation system.
"""

from .haskell_ast import *
from .haskell_parser import parse_haskell, HaskellLexer, HaskellParser
from .haskell_converter import haskell_to_runa, runa_to_haskell, HaskellToRunaConverter, RunaToHaskellConverter
from .haskell_generator import generate_haskell, HaskellCodeGenerator, HaskellCodeStyle, HaskellFormatter
from .haskell_toolchain import (
    HaskellToolchain,
    parse_haskell_code,
    generate_haskell_code,
    haskell_round_trip_verify,
    haskell_to_runa_translate,
    runa_to_haskell_translate
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete Haskell language toolchain for universal code translation"

# Main toolchain instance
toolchain = HaskellToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "HaskellToolchain",
    
    # Parser components
    "parse_haskell", "HaskellLexer", "HaskellParser",
    
    # Converters
    "haskell_to_runa", "runa_to_haskell", "HaskellToRunaConverter", "RunaToHaskellConverter",
    
    # Generator
    "generate_haskell", "HaskellCodeGenerator", "HaskellCodeStyle", "HaskellFormatter",
    
    # Convenience functions
    "parse_haskell_code", "generate_haskell_code", "haskell_round_trip_verify",
    "haskell_to_runa_translate", "runa_to_haskell_translate",
    
    # AST base classes (main ones)
    "HaskellNode", "HaskellExpression", "HaskellStatement", "HaskellDeclaration", "HaskellType",
]

# Module metadata
__language__ = "haskell"
__tier__ = 5
__file_extensions__ = [".hs", ".lhs"]
__mime_types__ = ["text/x-haskell"]
