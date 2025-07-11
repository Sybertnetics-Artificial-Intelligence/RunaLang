#!/usr/bin/env python3
"""
Bazel Language Support for Runa

Complete Bazel toolchain providing parsing, AST conversion, code generation,
and round-trip verification for the Runa universal translation system.
"""

from .bazel_ast import *
from .bazel_parser import parse_bazel, BazelLexer, BazelParser
from .bazel_converter import bazel_to_runa, runa_to_bazel, BazelToRunaConverter, RunaToBazelConverter
from .bazel_generator import generate_bazel, BazelCodeGenerator, BazelCodeStyle, BazelFormatter
from .bazel_toolchain import (
    BazelToolchain,
    parse_bazel_code,
    generate_bazel_code,
    bazel_round_trip_verify,
    bazel_to_runa_translate,
    runa_to_bazel_translate
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete Bazel language toolchain for universal code translation"

# Main toolchain instance
toolchain = BazelToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "BazelToolchain",
    
    # Parser components
    "parse_bazel", "BazelLexer", "BazelParser",
    
    # Converters
    "bazel_to_runa", "runa_to_bazel", "BazelToRunaConverter", "RunaToBazelConverter",
    
    # Generator
    "generate_bazel", "BazelCodeGenerator", "BazelCodeStyle", "BazelFormatter",
    
    # Convenience functions
    "parse_bazel_code", "generate_bazel_code", "bazel_round_trip_verify",
    "bazel_to_runa_translate", "runa_to_bazel_translate",
    
    # AST base classes (main ones)
    "BazelNode", "BazelExpression", "BazelStatement", "BazelDeclaration", "BazelNodeType",
]

# Module metadata
__language__ = "bazel"
__tier__ = 7
__file_extensions__ = [".bzl", "BUILD", "WORKSPACE"]
__mime_types__ = ["text/x-bazel"]
