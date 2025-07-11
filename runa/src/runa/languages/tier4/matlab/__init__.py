#!/usr/bin/env python3
"""
Matlab Language Support for Runa

Complete Matlab language toolchain providing parsing, AST conversion, code generation,
and round-trip verification for the Runa universal translation system.
"""

from .matlab_ast import *
from .matlab_parser import parse_matlab, MatlabLexer, MatlabParser
from .matlab_converter import matlab_to_runa, runa_to_matlab, MatlabToRunaConverter, RunaToMatlabConverter
from .matlab_generator import generate_matlab, MatlabCodeGenerator, MatlabCodeStyle, MatlabFormatter
from .matlab_toolchain import (
    MatlabToolchain,
    parse_matlab_code,
    generate_matlab_code,
    matlab_round_trip_verify,
    matlab_to_runa_translate,
    runa_to_matlab_translate
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete Matlab language toolchain for universal code translation"

# Main toolchain instance
toolchain = MatlabToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "MatlabToolchain",
    
    # Parser components
    "parse_matlab", "MatlabLexer", "MatlabParser",
    
    # Converters
    "matlab_to_runa", "runa_to_matlab", "MatlabToRunaConverter", "RunaToMatlabConverter",
    
    # Generator
    "generate_matlab", "MatlabCodeGenerator", "MatlabCodeStyle", "MatlabFormatter",
    
    # Convenience functions
    "parse_matlab_code", "generate_matlab_code", "matlab_round_trip_verify",
    "matlab_to_runa_translate", "runa_to_matlab_translate",
    
    # AST base classes (main ones)
    "MatlabNode", "MatlabExpression", "MatlabStatement", "MatlabDeclaration",
]

# Module metadata
__language__ = "matlab"
__tier__ = 4
__file_extensions__ = [".m"]
__mime_types__ = ["text/x-matlab"]
