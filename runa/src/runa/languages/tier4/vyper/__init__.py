#!/usr/bin/env python3
"""
Vyper Language Support for Runa Universal Translation System

This package provides comprehensive Vyper language support including:
- Security-focused smart contract parsing
- Bidirectional Vyper ↔ Runa AST conversion
- Clean Vyper code generation with Python-like syntax
- Round-trip translation verification
- Smart contract security analysis and validation
- Gas optimization analysis
- Python-style code formatting
- Complete toolchain integration
"""

from .vyper_ast import *
from .vyper_parser import parse_vyper_source, VyperLexer, VyperParser
from .vyper_converter import vyper_to_runa, runa_to_vyper, VyperToRunaConverter, RunaToVyperConverter
from .vyper_generator import generate_vyper_code, VyperCodeGenerator, VyperCodeStyle
from .vyper_toolchain import (
    VyperToolchain,
    parse_vyper_code,
    generate_vyper_code,
    vyper_round_trip_verify,
    vyper_to_runa_translate,
    runa_to_vyper_translate,
    create_vyper_toolchain,
    parse_vyper_file,
    validate_vyper_file,
    analyze_contract_security,
    optimize_vyper_file
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete Vyper language toolchain for universal smart contract translation"

# Main toolchain instance
toolchain = VyperToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "VyperToolchain",
    
    # Parser components
    "parse_vyper_source", "VyperLexer", "VyperParser",
    
    # Converters
    "vyper_to_runa", "runa_to_vyper", "VyperToRunaConverter", "RunaToVyperConverter",
    
    # Generator
    "generate_vyper_code", "VyperCodeGenerator", "VyperCodeStyle",
    
    # Convenience functions
    "parse_vyper_code", "vyper_round_trip_verify",
    "vyper_to_runa_translate", "runa_to_vyper_translate",
    "create_vyper_toolchain", "parse_vyper_file", "validate_vyper_file",
    "analyze_contract_security", "optimize_vyper_file",
    
    # AST base classes (main ones)
    "VyperNode", "VyperExpression", "VyperStatement", "VyperDeclaration", "VyperType",
]

# Module metadata
__language__ = "vyper"
__tier__ = 4
__file_extensions__ = [".vy"]
__mime_types__ = ["text/x-vyper"]
