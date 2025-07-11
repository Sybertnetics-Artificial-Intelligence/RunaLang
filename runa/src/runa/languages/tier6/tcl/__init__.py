#!/usr/bin/env python3
"""
Tcl Language Support for Runa

Complete Tcl toolchain providing parsing, AST conversion, code generation,
and round-trip verification for the Runa universal translation system.
"""

from .tcl_ast import *
from .tcl_parser import parse_tcl, TclLexer, TclParser
from .tcl_converter import tcl_to_runa, runa_to_tcl, TclToRunaConverter, RunaToTclConverter
from .tcl_generator import generate_tcl, TclCodeGenerator, TclCodeStyle, TclFormatter
from .tcl_toolchain import (
    TclToolchain,
    parse_tcl_code,
    generate_tcl_code,
    tcl_round_trip_verify,
    tcl_to_runa_translate,
    runa_to_tcl_translate
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete Tcl language toolchain for universal code translation"

# Main toolchain instance
toolchain = TclToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "TclToolchain",
    
    # Parser components
    "parse_tcl", "TclLexer", "TclParser",
    
    # Converters
    "tcl_to_runa", "runa_to_tcl", "TclToRunaConverter", "RunaToTclConverter",
    
    # Generator
    "generate_tcl", "TclCodeGenerator", "TclCodeStyle", "TclFormatter",
    
    # Convenience functions
    "parse_tcl_code", "generate_tcl_code", "tcl_round_trip_verify",
    "tcl_to_runa_translate", "runa_to_tcl_translate",
    
    # AST base classes (main ones)
    "TclNode", "TclExpression", "TclStatement", "TclDeclaration", "TclType",
]

# Module metadata
__language__ = "tcl"
__tier__ = 6
__file_extensions__ = [".tcl", ".tk"]
__mime_types__ = ["text/x-tcl"]
