#!/usr/bin/env python3
"""
Nix Language Support for Runa Universal Translation System

This package provides comprehensive Nix language support including:
- Complete Nix expression language parsing (Nix 2.0+)
- Bidirectional Nix ↔ Runa AST conversion
- Clean Nix code generation with multiple style options
- Round-trip translation verification
- Functional programming and package management support
- Attribute sets, functions, derivations, string interpolation
- Complete toolchain integration with Nix package manager
"""

from .nix_ast import *
from .nix_parser import parse_nix, NixLexer, NixParser
from .nix_converter import nix_to_runa, runa_to_nix, NixToRunaConverter, RunaToNixConverter
from .nix_generator import generate_nix, NixCodeGenerator, NixCodeStyle, NixFormatter
from .nix_toolchain import (
    NixToolchain,
    parse_nix_code,
    generate_nix_code,
    nix_round_trip_verify,
    nix_to_runa_translate,
    runa_to_nix_translate
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete Nix language toolchain for universal code translation"

# Main toolchain instance
toolchain = NixToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "NixToolchain",
    
    # Parser components
    "parse_nix", "NixLexer", "NixParser",
    
    # Converters
    "nix_to_runa", "runa_to_nix", "NixToRunaConverter", "RunaToNixConverter",
    
    # Generator
    "generate_nix", "NixCodeGenerator", "NixCodeStyle", "NixFormatter",
    
    # Convenience functions
    "parse_nix_code", "generate_nix_code", "nix_round_trip_verify",
    "nix_to_runa_translate", "runa_to_nix_translate",
    
    # AST base classes (main ones)
    "NixNode", "NixExpression", "NixStatement", "NixVisitor",
]

# Module metadata
__language__ = "nix"
__tier__ = 7
__file_extensions__ = [".nix"]
__mime_types__ = ["text/x-nix"]
