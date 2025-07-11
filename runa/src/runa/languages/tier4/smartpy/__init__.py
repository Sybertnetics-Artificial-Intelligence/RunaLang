#!/usr/bin/env python3
"""
SmartPy Language Support for Runa

Complete SmartPy language toolchain providing parsing, AST conversion, code generation,
and round-trip verification for the Runa universal translation system.
"""

from .smartpy_ast import *
from .smartpy_parser import parse_smartpy, SmartPyLexer, SmartPyParser
from .smartpy_converter import smartpy_to_runa, runa_to_smartpy, SmartPyToRunaConverter, RunaToSmartPyConverter
from .smartpy_generator import generate_smartpy, SmartPyCodeGenerator, SmartPyCodeStyle, SmartPyFormatter
from .smartpy_toolchain import (
    SmartPyToolchain,
    parse_smartpy_code,
    generate_smartpy_code,
    smartpy_round_trip_verify,
    smartpy_to_runa_translate,
    runa_to_smartpy_translate
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete SmartPy language toolchain for universal code translation"

# Main toolchain instance
toolchain = SmartPyToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "SmartPyToolchain",
    
    # Parser components
    "parse_smartpy", "SmartPyLexer", "SmartPyParser",
    
    # Converters
    "smartpy_to_runa", "runa_to_smartpy", "SmartPyToRunaConverter", "RunaToSmartPyConverter",
    
    # Generator
    "generate_smartpy", "SmartPyCodeGenerator", "SmartPyCodeStyle", "SmartPyFormatter",
    
    # Convenience functions
    "parse_smartpy_code", "generate_smartpy_code", "smartpy_round_trip_verify",
    "smartpy_to_runa_translate", "runa_to_smartpy_translate",
    
    # AST base classes (main ones)
    "SmartPyNode", "SmartPyExpression", "SmartPyStatement", "SmartPyDeclaration", "SmartPyType",
]

# Module metadata
__language__ = "smartpy"
__tier__ = 4
__file_extensions__ = [".py", ".sp.py"]
__mime_types__ = ["text/x-python", "text/x-smartpy"]
