#!/usr/bin/env python3
"""
Erlang Language Support for Runa

Complete Erlang language toolchain providing parsing, AST conversion, code generation,
and round-trip verification for the Runa universal translation system.
"""

from .erlang_ast import *
from .erlang_parser import parse_erlang, ErlangLexer, ErlangParser
from .erlang_converter import erlang_to_runa, runa_to_erlang, ErlangToRunaConverter, RunaToErlangConverter
from .erlang_generator import generate_erlang, ErlangCodeGenerator, ErlangCodeStyle, ErlangFormatter
from .erlang_toolchain import (
    ErlangToolchain,
    parse_erlang_code,
    generate_erlang_code,
    erlang_round_trip_verify,
    erlang_to_runa_translate,
    runa_to_erlang_translate
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete Erlang language toolchain for universal code translation"

# Main toolchain instance
toolchain = ErlangToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "ErlangToolchain",
    
    # Parser components
    "parse_erlang", "ErlangLexer", "ErlangParser",
    
    # Converters
    "erlang_to_runa", "runa_to_erlang", "ErlangToRunaConverter", "RunaToErlangConverter",
    
    # Generator
    "generate_erlang", "ErlangCodeGenerator", "ErlangCodeStyle", "ErlangFormatter",
    
    # Convenience functions
    "parse_erlang_code", "generate_erlang_code", "erlang_round_trip_verify",
    "erlang_to_runa_translate", "runa_to_erlang_translate",
    
    # AST base classes (main ones)
    "ErlangNode", "ErlangExpression", "ErlangStatement", "ErlangDeclaration", "ErlangType",
]

# Module metadata
__language__ = "erlang"
__tier__ = 5
__file_extensions__ = [".erl", ".hrl"]
__mime_types__ = ["text/x-erlang", "application/x-erlang"]
