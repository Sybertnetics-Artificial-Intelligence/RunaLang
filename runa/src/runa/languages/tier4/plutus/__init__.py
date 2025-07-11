#!/usr/bin/env python3
"""
Plutus Language Support for Runa

Complete Plutus language toolchain providing parsing, AST conversion, code generation,
and round-trip verification for the Runa universal translation system.
"""

from .plutus_ast import *
from .plutus_parser import parse_plutus, PlutusLexer, PlutusParser
from .plutus_converter import plutus_to_runa, runa_to_plutus, PlutusToRunaConverter, RunaToPlutusConverter
from .plutus_generator import generate_plutus, PlutusCodeGenerator, PlutusCodeStyle, PlutusFormatter
from .plutus_toolchain import (
    PlutusToolchain,
    parse_plutus_code,
    generate_plutus_code,
    plutus_round_trip_verify,
    plutus_to_runa_translate,
    runa_to_plutus_translate
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete Plutus language toolchain for universal code translation"

# Main toolchain instance
toolchain = PlutusToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "PlutusToolchain",
    
    # Parser components
    "parse_plutus", "PlutusLexer", "PlutusParser",
    
    # Converters
    "plutus_to_runa", "runa_to_plutus", "PlutusToRunaConverter", "RunaToPlutusConverter",
    
    # Generator
    "generate_plutus", "PlutusCodeGenerator", "PlutusCodeStyle", "PlutusFormatter",
    
    # Convenience functions
    "parse_plutus_code", "generate_plutus_code", "plutus_round_trip_verify",
    "plutus_to_runa_translate", "runa_to_plutus_translate",
    
    # AST base classes (main ones)
    "PlutusNode", "PlutusExpression", "PlutusStatement", "PlutusDeclaration", "PlutusType",
]

# Module metadata
__language__ = "plutus"
__tier__ = 4
__file_extensions__ = [".hs", ".lhs"]
__mime_types__ = ["text/x-haskell", "text/x-plutus"]
