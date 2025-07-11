#!/usr/bin/env python3
"""
Solidity Language Support for Runa

Complete Solidity language toolchain providing parsing, AST conversion, code generation,
and round-trip verification for the Runa universal translation system.
"""

from .solidity_ast import *
from .solidity_parser import parse_solidity, SolidityLexer, SolidityParser
from .solidity_converter import solidity_to_runa, runa_to_solidity, SolidityToRunaConverter, RunaToSolidityConverter
from .solidity_generator import generate_solidity, SolidityCodeGenerator, SolidityCodeStyle, SolidityFormatter
from .solidity_toolchain import (
    SolidityToolchain,
    parse_solidity_code,
    generate_solidity_code,
    solidity_round_trip_verify,
    solidity_to_runa_translate,
    runa_to_solidity_translate
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete Solidity language toolchain for universal code translation"

# Main toolchain instance
toolchain = SolidityToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "SolidityToolchain",
    
    # Parser components
    "parse_solidity", "SolidityLexer", "SolidityParser",
    
    # Converters
    "solidity_to_runa", "runa_to_solidity", "SolidityToRunaConverter", "RunaToSolidityConverter",
    
    # Generator
    "generate_solidity", "SolidityCodeGenerator", "SolidityCodeStyle", "SolidityFormatter",
    
    # Convenience functions
    "parse_solidity_code", "generate_solidity_code", "solidity_round_trip_verify",
    "solidity_to_runa_translate", "runa_to_solidity_translate",
    
    # AST base classes (main ones)
    "SolidityNode", "SolidityExpression", "SolidityStatement", "SolidityDeclaration", "SolidityType",
]

# Module metadata
__language__ = "solidity"
__tier__ = 4
__file_extensions__ = [".sol"]
__mime_types__ = ["text/x-solidity"]
