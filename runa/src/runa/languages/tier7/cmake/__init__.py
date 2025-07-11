#!/usr/bin/env python3
"""
CMake Language Support for Runa Universal Translation System

This package provides comprehensive CMake language support including:
- CMake syntax parsing (CMakeLists.txt and .cmake files)
- Bidirectional CMake ↔ Runa AST conversion
- Clean CMake code generation with proper formatting
- Round-trip translation verification
- Modern CMake features (targets, properties, generator expressions)
- Cross-platform build system support
- Complete toolchain integration
"""

from .cmake_ast import *
from .cmake_parser import parse_cmake, CMakeLexer, CMakeParser
from .cmake_converter import cmake_to_runa, runa_to_cmake, CMakeToRunaConverter, RunaToCMakeConverter
from .cmake_generator import generate_cmake, CMakeCodeGenerator, CMakeCodeStyle, CMakeFormatter
from .cmake_toolchain import (
    CMakeToolchain,
    parse_cmake_code,
    generate_cmake_code,
    cmake_round_trip_verify,
    cmake_to_runa_translate,
    runa_to_cmake_translate
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete CMake language toolchain for universal code translation"

# Main toolchain instance
toolchain = CMakeToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "CMakeToolchain",
    
    # Parser components
    "parse_cmake", "CMakeLexer", "CMakeParser",
    
    # Converters
    "cmake_to_runa", "runa_to_cmake", "CMakeToRunaConverter", "RunaToCMakeConverter",
    
    # Generator
    "generate_cmake", "CMakeCodeGenerator", "CMakeCodeStyle", "CMakeFormatter",
    
    # Convenience functions
    "parse_cmake_code", "generate_cmake_code", "cmake_round_trip_verify",
    "cmake_to_runa_translate", "runa_to_cmake_translate",
    
    # AST base classes (main ones)
    "CMakeNode", "CMakeCommand", "CMakeExpression", "CMakeVariable", "CMakeTarget",
]

# Module metadata
__language__ = "cmake"
__tier__ = 7
__file_extensions__ = [".cmake", "CMakeLists.txt"]
__mime_types__ = ["text/x-cmake"]
