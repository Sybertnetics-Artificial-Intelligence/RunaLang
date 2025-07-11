#!/usr/bin/env python3
"""
TOML Language Support for Runa Universal Translation System

This package provides comprehensive TOML language support including:
- TOML v1.0.0 parsing and validation
- Bidirectional TOML ↔ Runa AST conversion
- Clean TOML code generation with multiple style options
- Round-trip translation verification
- Configuration-specific validation and analysis
- Project-specific TOML handling (Cargo, Poetry, etc.)
- Complete toolchain integration with TOML tools
"""

from .toml_ast import *
from .toml_parser import parse_toml, TOMLLexer, TOMLParser
from .toml_converter import toml_to_runa, runa_to_toml, TOMLToRunaConverter, RunaToTOMLConverter
from .toml_generator import generate_toml, TOMLCodeGenerator, TOMLFormatStyle, TOMLFormatter
from .toml_toolchain import (
    TOMLToolchain,
    parse_toml_code,
    generate_toml_code,
    toml_round_trip_verify,
    toml_to_runa_translate,
    runa_to_toml_translate
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete TOML language toolchain for universal code translation"

# Main toolchain instance
toolchain = TOMLToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "TOMLToolchain",
    
    # Parser components
    "parse_toml", "TOMLLexer", "TOMLParser",
    
    # Converters
    "toml_to_runa", "runa_to_toml", "TOMLToRunaConverter", "RunaToTOMLConverter",
    
    # Generator
    "generate_toml", "TOMLCodeGenerator", "TOMLFormatStyle", "TOMLFormatter",
    
    # Convenience functions
    "parse_toml_code", "generate_toml_code", "toml_round_trip_verify",
    "toml_to_runa_translate", "runa_to_toml_translate",
    
    # AST base classes (main ones)
    "TOMLNode", "TOMLValue", "TOMLStatement", "TOMLDocument", "TOMLTable",
    "TOMLKeyValue", "TOMLKey", "TOMLString", "TOMLInteger", "TOMLFloat",
    "TOMLBoolean", "TOMLDateTime", "TOMLDate", "TOMLTime", "TOMLArray",
    "TOMLInlineTable", "TOMLComment",
    
    # Enums and types
    "TOMLType", "TOMLStringType", "TOMLFormatStyle",
    
    # Helper functions
    "create_string", "create_integer", "create_float", "create_boolean",
    "create_array", "create_inline_table", "create_key", "create_key_value",
    "create_table", "create_comment", "create_document",
]

# Module metadata
__language__ = "toml"
__tier__ = 3
__file_extensions__ = [".toml"]
__mime_types__ = ["application/toml", "text/x-toml"]
