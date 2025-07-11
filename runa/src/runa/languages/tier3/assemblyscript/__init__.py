#!/usr/bin/env python3
"""
AssemblyScript Language Support for Runa

Complete AssemblyScript toolchain providing parsing, AST conversion, code generation,
and round-trip verification for the Runa universal translation system.
"""

from .assemblyscript_ast import *
from .assemblyscript_parser import parse_assemblyscript, parse_assemblyscript_file, AsLexer, AsParser
from .assemblyscript_converter import assemblyscript_to_runa, runa_to_assemblyscript, AssemblyScriptToRunaConverter, RunaToAssemblyScriptConverter
from .assemblyscript_generator import generate_assemblyscript_code, AssemblyScriptCodeGenerator, AssemblyScriptCodeStyle, AssemblyScriptFormatter
from .assemblyscript_toolchain import (
    AssemblyScriptToolchain,
    create_assemblyscript_toolchain,
    assemblyscript_to_runa_translation,
    runa_to_assemblyscript_translation,
    verify_assemblyscript_round_trip,
    parse_assemblyscript_code,
    generate_assemblyscript_code_from_ast
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete AssemblyScript language toolchain for universal code translation"

# Main toolchain instance
toolchain = AssemblyScriptToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "AssemblyScriptToolchain",
    
    # Parser components
    "parse_assemblyscript", "parse_assemblyscript_file", "AsLexer", "AsParser",
    
    # Converters
    "assemblyscript_to_runa", "runa_to_assemblyscript", "AssemblyScriptToRunaConverter", "RunaToAssemblyScriptConverter",
    
    # Generator
    "generate_assemblyscript_code", "AssemblyScriptCodeGenerator", "AssemblyScriptCodeStyle", "AssemblyScriptFormatter",
    
    # Convenience functions
    "create_assemblyscript_toolchain", "assemblyscript_to_runa_translation", "runa_to_assemblyscript_translation",
    "verify_assemblyscript_round_trip", "parse_assemblyscript_code", "generate_assemblyscript_code_from_ast",
    
    # AST base classes (main ones)
    "AsNode", "AsProgram", "AsFunction", "AsClass", "AsVariableDeclaration", "AsExpression", "AsType",
]

# Module metadata
__language__ = "assemblyscript"
__tier__ = 3
__file_extensions__ = [".ts", ".as"]
__mime_types__ = ["text/typescript", "application/typescript"]