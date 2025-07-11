#!/usr/bin/env python3
"""
Assembly Language Support for Runa

Complete Assembly language toolchain providing parsing, AST conversion, code generation,
and round-trip verification for the Runa universal translation system.
"""

from .assembly_ast import *
from .assembly_parser import parse_assembly, AssemblyLexer, AssemblyParser
from .assembly_converter import assembly_to_runa, runa_to_assembly, AssemblyToRunaConverter, RunaToAssemblyConverter
from .assembly_generator import generate_assembly, AssemblyCodeGenerator, AssemblyCodeStyle, AssemblyFormatter
from .assembly_toolchain import (
    AssemblyToolchain,
    parse_assembly_code,
    generate_assembly_code,
    assembly_round_trip_verify,
    assembly_to_runa_translate,
    runa_to_assembly_translate
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete Assembly language toolchain for universal code translation"

# Main toolchain instance
toolchain = AssemblyToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "AssemblyToolchain",
    
    # Parser components
    "parse_assembly", "AssemblyLexer", "AssemblyParser",
    
    # Converters
    "assembly_to_runa", "runa_to_assembly", "AssemblyToRunaConverter", "RunaToAssemblyConverter",
    
    # Generator
    "generate_assembly", "AssemblyCodeGenerator", "AssemblyCodeStyle", "AssemblyFormatter",
    
    # Convenience functions
    "parse_assembly_code", "generate_assembly_code", "assembly_round_trip_verify",
    "assembly_to_runa_translate", "runa_to_assembly_translate",
    
    # AST base classes (main ones)
    "AssemblyNode", "AssemblyExpression", "AssemblyStatement", "AssemblyDeclaration", "AssemblyType",
]

# Module metadata
__language__ = "assembly"
__tier__ = 5
__file_extensions__ = [".asm", ".s", ".S", ".inc"]
__mime_types__ = ["text/x-asm", "application/x-assembly"]
