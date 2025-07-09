#!/usr/bin/env python3
"""
C# Language Support for Runa Universal Translation System

This package provides comprehensive C# language support including:
- Modern C# parsing (C# 1.0 through C# 12.0)
- Bidirectional C# ↔ Runa AST conversion
- Clean C# code generation with multiple style options
- Round-trip translation verification
- Generics and nullable reference types support
- Modern C# features: records, pattern matching, switch expressions
- Complete toolchain integration
"""

from .csharp_ast import *
from .csharp_parser import parse_csharp, CSharpLexer, CSharpParser
from .csharp_converter import csharp_to_runa, runa_to_csharp, CSharpToRunaConverter, RunaToCSharpConverter
from .csharp_generator import generate_csharp, CSharpCodeGenerator, CSharpCodeStyle, CSharpFormatter
from .csharp_toolchain import (
    CSharpToolchain,
    parse_csharp_code,
    generate_csharp_code,
    csharp_round_trip_verify,
    csharp_to_runa_translate,
    runa_to_csharp_translate
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete C# language toolchain for universal code translation"

# Main toolchain instance
toolchain = CSharpToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "CSharpToolchain",
    
    # Parser components
    "parse_csharp", "CSharpLexer", "CSharpParser",
    
    # Converters
    "csharp_to_runa", "runa_to_csharp", "CSharpToRunaConverter", "RunaToCSharpConverter",
    
    # Generator
    "generate_csharp", "CSharpCodeGenerator", "CSharpCodeStyle", "CSharpFormatter",
    
    # Convenience functions
    "parse_csharp_code", "generate_csharp_code", "csharp_round_trip_verify",
    "csharp_to_runa_translate", "runa_to_csharp_translate",
    
    # AST base classes (main ones)
    "CSharpNode", "CSharpExpression", "CSharpStatement", "CSharpDeclaration", "CSharpType",
]

# Module metadata
__language__ = "csharp"
__tier__ = 1
__file_extensions__ = [".cs", ".csx"]
__mime_types__ = ["text/x-csharp"]
