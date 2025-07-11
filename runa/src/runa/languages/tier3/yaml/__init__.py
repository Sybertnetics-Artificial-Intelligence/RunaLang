#!/usr/bin/env python3
"""
YAML Language Support for Runa

Complete YAML toolchain providing parsing, AST conversion, code generation,
and round-trip verification for the Runa universal translation system.
"""

from .yaml_ast import *
from .yaml_parser import parse_yaml, parse_yaml_document, YamlLexer, YamlParser
from .yaml_converter import yaml_to_runa, runa_to_yaml, YamlToRunaConverter, RunaToYamlConverter
from .yaml_generator import generate_yaml_code, YamlCodeGenerator, YamlCodeStyle, YamlFormatter
from .yaml_toolchain import (
    YamlToolchain,
    create_yaml_toolchain,
    yaml_to_runa_translation,
    runa_to_yaml_translation,
    verify_yaml_round_trip,
    parse_yaml_code,
    generate_yaml_code_from_ast
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete YAML language toolchain for universal code translation"

# Main toolchain instance
toolchain = YamlToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "YamlToolchain",
    
    # Parser components
    "parse_yaml", "parse_yaml_document", "YamlLexer", "YamlParser",
    
    # Converters
    "yaml_to_runa", "runa_to_yaml", "YamlToRunaConverter", "RunaToYamlConverter",
    
    # Generator
    "generate_yaml_code", "YamlCodeGenerator", "YamlCodeStyle", "YamlFormatter",
    
    # Convenience functions
    "create_yaml_toolchain", "yaml_to_runa_translation", "runa_to_yaml_translation",
    "verify_yaml_round_trip", "parse_yaml_code", "generate_yaml_code_from_ast",
    
    # AST base classes (main ones)
    "YamlNode", "YamlValue", "YamlDocument", "YamlStream", "YamlMapping", "YamlSequence",
]

# Module metadata
__language__ = "yaml"
__tier__ = 3
__file_extensions__ = [".yaml", ".yml"]
__mime_types__ = ["application/yaml", "text/yaml", "text/x-yaml"]