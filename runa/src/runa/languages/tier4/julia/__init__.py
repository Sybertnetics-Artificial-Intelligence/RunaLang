#!/usr/bin/env python3
"""
Julia Language Support for Runa

Complete Julia language toolchain providing parsing, AST conversion, code generation,
and round-trip verification for the Runa universal translation system.
"""

from .julia_ast import *
from .julia_parser import parse_julia, JuliaLexer, JuliaParser
from .julia_converter import julia_to_runa, runa_to_julia, JuliaToRunaConverter, RunaToJuliaConverter
from .julia_generator import generate_julia, JuliaCodeGenerator, JuliaCodeStyle, JuliaFormatter
from .julia_toolchain import (
    JuliaToolchain,
    parse_julia_code,
    generate_julia_code,
    julia_round_trip_verify,
    julia_to_runa_translate,
    runa_to_julia_translate
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete Julia language toolchain for universal code translation"

# Main toolchain instance
toolchain = JuliaToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "JuliaToolchain",
    
    # Parser components
    "parse_julia", "JuliaLexer", "JuliaParser",
    
    # Converters
    "julia_to_runa", "runa_to_julia", "JuliaToRunaConverter", "RunaToJuliaConverter",
    
    # Generator
    "generate_julia", "JuliaCodeGenerator", "JuliaCodeStyle", "JuliaFormatter",
    
    # Convenience functions
    "parse_julia_code", "generate_julia_code", "julia_round_trip_verify",
    "julia_to_runa_translate", "runa_to_julia_translate",
    
    # AST base classes (main ones)
    "JuliaNode", "JuliaExpression", "JuliaStatement", "JuliaDeclaration", "JuliaType",
]

# Module metadata
__language__ = "julia"
__tier__ = 4
__file_extensions__ = [".jl"]
__mime_types__ = ["text/x-julia"]
