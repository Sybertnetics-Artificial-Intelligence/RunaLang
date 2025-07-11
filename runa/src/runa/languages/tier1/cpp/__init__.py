#!/usr/bin/env python3
"""
C++ Language Support for Runa Universal Translation System

This package provides comprehensive C++ language support including:
- Modern C++ parsing (C++11 through C++23)
- Bidirectional C++ ↔ Runa AST conversion
- Clean C++ code generation with multiple style options
- Round-trip translation verification
- Template and generic programming support
- RAII and smart pointer handling
- Complete toolchain integration
"""

from .cpp_ast import *
from .cpp_parser import parse_cpp, CppLexer, CppParser
from .cpp_converter import cpp_to_runa, runa_to_cpp, CppToRunaConverter, RunaToCppConverter
from .cpp_generator import generate_cpp, CppCodeGenerator, CppCodeStyle, CppFormatter
from .cpp_toolchain import (
    CppToolchain,
    parse_cpp_code,
    generate_cpp_code,
    cpp_round_trip_verify,
    cpp_to_runa_translate,
    runa_to_cpp_translate
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete C++ language toolchain for universal code translation"

# Main toolchain instance
toolchain = CppToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "CppToolchain",
    
    # Parser components
    "parse_cpp", "CppLexer", "CppParser",
    
    # Converters
    "cpp_to_runa", "runa_to_cpp", "CppToRunaConverter", "RunaToCppConverter",
    
    # Generator
    "generate_cpp", "CppCodeGenerator", "CppCodeStyle", "CppFormatter",
    
    # Convenience functions
    "parse_cpp_code", "generate_cpp_code", "cpp_round_trip_verify",
    "cpp_to_runa_translate", "runa_to_cpp_translate",
    
    # AST base classes (main ones)
    "CppNode", "CppExpression", "CppStatement", "CppDeclaration", "CppType",
]

# Module metadata
__language__ = "cpp"
__tier__ = 1
__file_extensions__ = [".cpp", ".cxx", ".cc", ".hpp", ".hxx", ".h"]
__mime_types__ = ["text/x-c++src", "text/x-c++hdr"]