#!/usr/bin/env python3
"""
TypeScript Language Support for Runa

Complete TypeScript toolchain providing parsing, AST conversion, code generation,
and round-trip verification for the Runa universal translation system.
"""

from .ts_ast import *
from .ts_parser import parse_typescript, TSLexer, TSParser
from .ts_converter import ts_to_runa, runa_to_ts, TSToRunaConverter, RunaToTSConverter
from .ts_generator import generate_typescript, TSCodeGenerator, TSFormatter
from .ts_toolchain import (
    TypeScriptToolchain,
    parse_ts,
    generate_ts,
    ts_round_trip_verify,
    ts_to_runa_translate,
    runa_to_ts_translate
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete TypeScript language toolchain for universal code translation"

# Main toolchain instance
toolchain = TypeScriptToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "TypeScriptToolchain",
    
    # Parser components
    "parse_typescript", "TSLexer", "TSParser",
    
    # Converters
    "ts_to_runa", "runa_to_ts", "TSToRunaConverter", "RunaToTSConverter",
    
    # Generator
    "generate_typescript", "TSCodeGenerator", "TSFormatter",
    
    # Convenience functions
    "parse_ts", "generate_ts", "ts_round_trip_verify",
    "ts_to_runa_translate", "runa_to_ts_translate",
    
    # AST base classes (main ones)
    "TSNode", "TSExpression", "TSStatement", "TSDeclaration", "TSType",
]

# Module metadata
__language__ = "typescript"
__tier__ = 1
__file_extensions__ = [".ts", ".tsx", ".d.ts"]
__mime_types__ = ["application/typescript", "text/typescript"]