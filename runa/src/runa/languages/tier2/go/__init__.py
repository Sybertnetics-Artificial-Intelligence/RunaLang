#!/usr/bin/env python3
"""
Go Language Support for Runa

Complete Go toolchain providing parsing, AST conversion, code generation,
and round-trip verification for the Runa universal translation system.
"""

from .go_ast import *
from .go_parser import parse_go, GoLexer, GoParser
from .go_converter import go_to_runa, runa_to_go, GoToRunaConverter, RunaToGoConverter
from .go_generator import generate_go, GoCodeGenerator, GoCodeStyle, GoFormatter
from .go_toolchain import (
    GoToolchain,
    parse_go_code,
    generate_go_code,
    go_round_trip_verify,
    go_to_runa_translate,
    runa_to_go_translate
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete Go language toolchain for universal code translation"

# Main toolchain instance
toolchain = GoToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "GoToolchain",
    
    # Parser components
    "parse_go", "GoLexer", "GoParser",
    
    # Converters
    "go_to_runa", "runa_to_go", "GoToRunaConverter", "RunaToGoConverter",
    
    # Generator
    "generate_go", "GoCodeGenerator", "GoCodeStyle", "GoFormatter",
    
    # Convenience functions
    "parse_go_code", "generate_go_code", "go_round_trip_verify",
    "go_to_runa_translate", "runa_to_go_translate",
    
    # AST base classes (main ones)
    "GoNode", "GoExpression", "GoStatement", "GoDeclaration", "GoType",
]

# Module metadata
__language__ = "go"
__tier__ = 2
__file_extensions__ = [".go"]
__mime_types__ = ["text/x-go", "application/x-go"]
