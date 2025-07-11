#!/usr/bin/env python3
"""
Objective-C Language Support for Runa

Complete Objective-C toolchain providing parsing, AST conversion, code generation,
and round-trip verification for the Runa universal translation system.
"""

from .objective_c_ast import *
from .objective_c_parser import parse_objective_c, ObjectiveCLexer, ObjectiveCParser
from .objective_c_converter import objective_c_to_runa, runa_to_objective_c, ObjectiveCToRunaConverter, RunaToObjectiveCConverter
from .objective_c_generator import generate_objective_c, ObjectiveCCodeGenerator, ObjectiveCCodeStyle, ObjectiveCFormatter
from .objective_c_toolchain import (
    ObjectiveCToolchain,
    parse_objective_c_code,
    generate_objective_c_code,
    objective_c_round_trip_verify,
    objective_c_to_runa_translate,
    runa_to_objective_c_translate
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete Objective-C language toolchain for universal code translation"

# Main toolchain instance
toolchain = ObjectiveCToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "ObjectiveCToolchain",
    
    # Parser components
    "parse_objective_c", "ObjectiveCLexer", "ObjectiveCParser",
    
    # Converters
    "objective_c_to_runa", "runa_to_objective_c", "ObjectiveCToRunaConverter", "RunaToObjectiveCConverter",
    
    # Generator
    "generate_objective_c", "ObjectiveCCodeGenerator", "ObjectiveCCodeStyle", "ObjectiveCFormatter",
    
    # Convenience functions
    "parse_objective_c_code", "generate_objective_c_code", "objective_c_round_trip_verify",
    "objective_c_to_runa_translate", "runa_to_objective_c_translate",
    
    # AST base classes (main ones)
    "ObjectiveCNode", "ObjectiveCExpression", "ObjectiveCStatement", "ObjectiveCDeclaration", "ObjectiveCType",
]

# Module metadata
__language__ = "objective_c"
__tier__ = 6
__file_extensions__ = [".m", ".mm", ".h"]
__mime_types__ = ["text/x-objc"]
