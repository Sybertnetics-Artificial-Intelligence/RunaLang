#!/usr/bin/env python3
"""
Rust Language Support for Runa

Complete Rust toolchain providing parsing, AST conversion, code generation,
and round-trip verification for the Runa universal translation system.
"""

from .rust_ast import *
from .rust_parser import parse_rust, RustLexer, RustParser
from .rust_converter import rust_to_runa, runa_to_rust, RustToRunaConverter, RunaToRustConverter
from .rust_generator import generate_rust, RustCodeGenerator, RustCodeStyle, RustFormatter
from .rust_toolchain import (
    RustToolchain,
    parse_rust_code,
    generate_rust_code,
    rust_round_trip_verify,
    rust_to_runa_translate,
    runa_to_rust_translate
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete Rust language toolchain for universal code translation"

# Main toolchain instance
toolchain = RustToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "RustToolchain",
    
    # Parser components
    "parse_rust", "RustLexer", "RustParser",
    
    # Converters
    "rust_to_runa", "runa_to_rust", "RustToRunaConverter", "RunaToRustConverter",
    
    # Generator
    "generate_rust", "RustCodeGenerator", "RustCodeStyle", "RustFormatter",
    
    # Convenience functions
    "parse_rust_code", "generate_rust_code", "rust_round_trip_verify",
    "rust_to_runa_translate", "runa_to_rust_translate",
    
    # AST base classes (main ones)
    "RustNode", "RustExpression", "RustStatement", "RustDeclaration", "RustType",
]

# Module metadata
__language__ = "rust"
__tier__ = 2
__file_extensions__ = [".rs"]
__mime_types__ = ["text/x-rust"]