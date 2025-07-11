#!/usr/bin/env python3
"""
JSON Language Support for Runa

Complete JSON toolchain providing parsing, AST conversion, code generation,
and round-trip verification for the Runa universal translation system.
"""

from .json_ast import *
from .json_parser import parse_json, parse_json_strict, parse_json_relaxed, JsonLexer, JsonParser
from .json_converter import json_to_runa, runa_to_json, JsonToRunaConverter, RunaToJsonConverter
from .json_generator import generate_json_code, JsonCodeGenerator, JsonCodeStyle, JsonFormatter
from .json_toolchain import (
    JsonToolchain,
    create_json_toolchain,
    json_to_runa_translation,
    runa_to_json_translation,
    verify_json_round_trip,
    parse_json_code,
    generate_json_code_from_ast
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete JSON language toolchain for universal code translation"

# Main toolchain instance
toolchain = JsonToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "JsonToolchain",
    
    # Parser components
    "parse_json", "parse_json_strict", "parse_json_relaxed", "JsonLexer", "JsonParser",
    
    # Converters
    "json_to_runa", "runa_to_json", "JsonToRunaConverter", "RunaToJsonConverter",
    
    # Generator
    "generate_json_code", "JsonCodeGenerator", "JsonCodeStyle", "JsonFormatter",
    
    # Convenience functions
    "create_json_toolchain", "json_to_runa_translation", "runa_to_json_translation",
    "verify_json_round_trip", "parse_json_code", "generate_json_code_from_ast",
    
    # AST base classes (main ones)
    "JsonNode", "JsonValue", "JsonDocument", "JsonObject", "JsonArray",
]

# Module metadata
__language__ = "json"
__tier__ = 3
__file_extensions__ = [".json", ".jsonc", ".json5"]
__mime_types__ = ["application/json", "application/json5", "text/json"]