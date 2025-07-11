#!/usr/bin/env python3
"""
INI Language Support for Runa Universal Translation System

This package provides comprehensive INI language support including:
- Standard INI configuration file parsing
- Windows INI, Git config, and systemd unit file support
- Bidirectional INI ↔ Runa AST conversion
- Clean INI code generation with multiple style options
- Round-trip translation verification
- Format-specific validation and tooling
- Configuration analysis and optimization
- Complete toolchain integration with common INI tools
"""

from .ini_ast import *
from .ini_parser import INIParser, INILexer
from .ini_converter import ini_to_runa, runa_to_ini, INIToRunaConverter, RunaToINIConverter
from .ini_generator import generate_ini, INICodeGenerator, INIFormatStyle, INIFormatter
from .ini_toolchain import (
    INIToolchain,
    parse_ini_code,
    generate_ini_code,
    ini_round_trip_verify,
    ini_to_runa_translate,
    runa_to_ini_translate
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete INI language toolchain for universal code translation"

# Main toolchain instance
toolchain = INIToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "INIToolchain",
    
    # Parser components
    "INIParser", "INILexer",
    
    # Converters
    "ini_to_runa", "runa_to_ini", "INIToRunaConverter", "RunaToINIConverter",
    
    # Generator
    "generate_ini", "INICodeGenerator", "INIFormatStyle", "INIFormatter",
    
    # Convenience functions
    "parse_ini_code", "generate_ini_code", "ini_round_trip_verify",
    "ini_to_runa_translate", "runa_to_ini_translate",
    
    # AST base classes (main ones)
    "ININode", "INIConfiguration", "INISection", "INIKeyValuePair", "INIValue",
    "INIComment", "INIInterpolation", "INIInclude", "INIArray",
    
    # Special section types
    "WindowsINISection", "GitConfigSection", "SystemdConfigSection",
    
    # Enums and types
    "INIValueType", "INIDelimiterType", "INICommentStyle",
    
    # Visitor pattern
    "INIVisitor", "INIBaseVisitor",
]

# Module metadata
__language__ = "ini"
__tier__ = 3
__file_extensions__ = [".ini", ".cfg", ".conf", ".config", ".service", ".timer", ".socket"]
__mime_types__ = ["text/plain", "application/x-ini", "text/x-ini"]
