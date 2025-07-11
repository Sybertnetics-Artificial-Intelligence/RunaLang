#!/usr/bin/env python3
"""
Swift Language Support for Runa

Complete Swift toolchain providing parsing, AST conversion, code generation,
and round-trip verification for the Runa universal translation system.
"""

from .swift_ast import *
from .swift_parser import parse_swift, SwiftLexer, SwiftParser
from .swift_converter import swift_to_runa, runa_to_swift, SwiftToRunaConverter, RunaToSwiftConverter
from .swift_generator import generate_swift, SwiftCodeGenerator, SwiftCodeStyle, SwiftFormatter
from .swift_toolchain import (
    SwiftToolchain,
    parse_swift_code,
    generate_swift_code,
    swift_round_trip_verify,
    swift_to_runa_translate,
    runa_to_swift_translate
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete Swift language toolchain for universal code translation"

# Main toolchain instance
toolchain = SwiftToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "SwiftToolchain",
    
    # Parser components
    "parse_swift", "SwiftLexer", "SwiftParser",
    
    # Converters
    "swift_to_runa", "runa_to_swift", "SwiftToRunaConverter", "RunaToSwiftConverter",
    
    # Generator
    "generate_swift", "SwiftCodeGenerator", "SwiftCodeStyle", "SwiftFormatter",
    
    # Convenience functions
    "parse_swift_code", "generate_swift_code", "swift_round_trip_verify",
    "swift_to_runa_translate", "runa_to_swift_translate",
    
    # AST base classes (main ones)
    "SwiftNode", "SwiftExpression", "SwiftStatement", "SwiftDeclaration", "SwiftType",
]

# Module metadata
__language__ = "swift"
__tier__ = 2
__file_extensions__ = [".swift"]
__mime_types__ = ["text/x-swift"]