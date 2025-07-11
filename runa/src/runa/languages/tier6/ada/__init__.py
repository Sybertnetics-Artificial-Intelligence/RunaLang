#!/usr/bin/env python3
"""
Ada Language Support for Runa

Complete Ada toolchain providing parsing, AST conversion, code generation,
and round-trip verification for the Runa universal translation system.
"""

from .ada_ast import *
from .ada_parser import parse_ada, AdaLexer, AdaParser
from .ada_converter import ada_to_runa, runa_to_ada, AdaToRunaConverter, RunaToAdaConverter
from .ada_generator import generate_ada, AdaCodeGenerator, AdaCodeStyle, AdaFormatter
from .ada_toolchain import (
    AdaToolchain,
    parse_ada_code,
    generate_ada_code,
    ada_round_trip_verify,
    ada_to_runa_translate,
    runa_to_ada_translate
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete Ada language toolchain for universal code translation"

# Main toolchain instance
toolchain = AdaToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "AdaToolchain",
    
    # Parser components
    "parse_ada", "AdaLexer", "AdaParser",
    
    # Converters
    "ada_to_runa", "runa_to_ada", "AdaToRunaConverter", "RunaToAdaConverter",
    
    # Generator
    "generate_ada", "AdaCodeGenerator", "AdaCodeStyle", "AdaFormatter",
    
    # Convenience functions
    "parse_ada_code", "generate_ada_code", "ada_round_trip_verify",
    "ada_to_runa_translate", "runa_to_ada_translate",
    
    # AST base classes (main ones)
    "AdaNode", "AdaExpression", "AdaStatement", "AdaDeclaration", "AdaType",
]

# Module metadata
__language__ = "ada"
__tier__ = 6
__file_extensions__ = [".ada", ".adb", ".ads"]
__mime_types__ = ["text/x-ada"]
