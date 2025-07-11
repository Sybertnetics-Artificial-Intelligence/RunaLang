#!/usr/bin/env python3
"""
Perl Language Support for Runa

Complete Perl toolchain providing parsing, AST conversion, code generation,
and round-trip verification for the Runa universal translation system.
"""

from .perl_ast import *
from .perl_parser import parse_perl, PerlLexer, PerlParser
from .perl_converter import perl_to_runa, runa_to_perl, PerlToRunaConverter, RunaToPerlConverter
from .perl_generator import generate_perl, PerlCodeGenerator, PerlCodeStyle, PerlFormatter
from .perl_toolchain import (
    PerlToolchain,
    parse_perl_code,
    generate_perl_code,
    perl_round_trip_verify,
    perl_to_runa_translate,
    runa_to_perl_translate
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete Perl language toolchain for universal code translation"

# Main toolchain instance
toolchain = PerlToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "PerlToolchain",
    
    # Parser components
    "parse_perl", "PerlLexer", "PerlParser",
    
    # Converters
    "perl_to_runa", "runa_to_perl", "PerlToRunaConverter", "RunaToPerlConverter",
    
    # Generator
    "generate_perl", "PerlCodeGenerator", "PerlCodeStyle", "PerlFormatter",
    
    # Convenience functions
    "parse_perl_code", "generate_perl_code", "perl_round_trip_verify",
    "perl_to_runa_translate", "runa_to_perl_translate",
    
    # AST base classes (main ones)
    "PerlNode", "PerlExpression", "PerlStatement", "PerlDeclaration", "PerlType",
]

# Module metadata
__language__ = "perl"
__tier__ = 6
__file_extensions__ = [".pl", ".pm", ".t", ".pod"]
__mime_types__ = ["text/x-perl", "application/x-perl"]
