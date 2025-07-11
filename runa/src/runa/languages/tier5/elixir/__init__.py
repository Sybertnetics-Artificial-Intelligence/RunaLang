#!/usr/bin/env python3
"""
Elixir Language Support for Runa

Complete Elixir language toolchain providing parsing, AST conversion, code generation,
and round-trip verification for the Runa universal translation system.
"""

from .elixir_ast import *
from .elixir_parser import parse_elixir, ElixirLexer, ElixirParser
from .elixir_converter import elixir_to_runa, runa_to_elixir, ElixirToRunaConverter, RunaToElixirConverter
from .elixir_generator import generate_elixir, ElixirCodeGenerator, ElixirCodeStyle, ElixirFormatter
from .elixir_toolchain import (
    ElixirToolchain,
    parse_elixir_code,
    generate_elixir_code,
    elixir_round_trip_verify,
    elixir_to_runa_translate,
    runa_to_elixir_translate
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete Elixir language toolchain for universal code translation"

# Main toolchain instance
toolchain = ElixirToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "ElixirToolchain",
    
    # Parser components
    "parse_elixir", "ElixirLexer", "ElixirParser",
    
    # Converters
    "elixir_to_runa", "runa_to_elixir", "ElixirToRunaConverter", "RunaToElixirConverter",
    
    # Generator
    "generate_elixir", "ElixirCodeGenerator", "ElixirCodeStyle", "ElixirFormatter",
    
    # Convenience functions
    "parse_elixir_code", "generate_elixir_code", "elixir_round_trip_verify",
    "elixir_to_runa_translate", "runa_to_elixir_translate",
    
    # AST base classes (main ones)
    "ElixirNode", "ElixirExpression", "ElixirStatement", "ElixirDeclaration", "ElixirType",
]

# Module metadata
__language__ = "elixir"
__tier__ = 5
__file_extensions__ = [".ex", ".exs"]
__mime_types__ = ["text/x-elixir", "application/x-elixir"]
