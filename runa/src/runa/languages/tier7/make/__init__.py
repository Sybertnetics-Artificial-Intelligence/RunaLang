#!/usr/bin/env python3
"""
Make Language Support for Runa Universal Translation System

This package provides comprehensive Make language support including:
- Make syntax parsing (Makefile, *.mk files)
- Bidirectional Make ↔ Runa AST conversion
- Clean Make code generation with proper formatting
- Round-trip translation verification
- Build system integration (GNU Make, POSIX Make)
- Dependency analysis and optimization
- Complete toolchain integration
"""

from .make_ast import *
from .make_parser import parse_make, MakeLexer, MakeParser
from .make_converter import make_to_runa, runa_to_make, MakeToRunaConverter, RunaToMakeConverter
from .make_generator import generate_make, MakeCodeGenerator, MakeCodeStyle, MakeFormatter
from .make_toolchain import (
    MakeToolchain,
    parse_make_code,
    generate_make_code,
    make_round_trip_verify,
    make_to_runa_translate,
    runa_to_make_translate
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete Make language toolchain for universal code translation"

# Main toolchain instance
toolchain = MakeToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "MakeToolchain",
    
    # Parser components
    "parse_make", "MakeLexer", "MakeParser",
    
    # Converters
    "make_to_runa", "runa_to_make", "MakeToRunaConverter", "RunaToMakeConverter",
    
    # Generator
    "generate_make", "MakeCodeGenerator", "MakeCodeStyle", "MakeFormatter",
    
    # Convenience functions
    "parse_make_code", "generate_make_code", "make_round_trip_verify",
    "make_to_runa_translate", "runa_to_make_translate",
    
    # AST base classes (main ones)
    "MakeNode", "MakeExpression", "MakeStatement", "MakeFile", "MakeRule",
]

# Module metadata
__language__ = "make"
__tier__ = 7
__file_extensions__ = [".mk", "Makefile", "makefile", "GNUmakefile"]
__mime_types__ = ["text/x-makefile"]
