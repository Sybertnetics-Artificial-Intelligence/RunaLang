#!/usr/bin/env python3
"""
Python Language Support for Runa Universal Translation System

This package provides comprehensive Python language support including:
- Modern Python parsing (Python 3.6 through Python 3.12)
- Bidirectional Python ↔ Runa AST conversion
- Clean Python code generation with multiple style options
- Round-trip translation verification
- Type hints and modern Python features support
- Async/await, dataclasses, match statements, walrus operator
- Complete toolchain integration
"""

from .py_ast import *
from .py_parser import parse_python, PythonLexer, PythonParser
from .py_converter import python_to_runa, runa_to_python, PythonToRunaConverter, RunaToPythonConverter
from .py_generator import generate_python, PythonCodeGenerator, PythonCodeStyle, PythonFormatter
from .py_toolchain import (
    PythonToolchain,
    parse_python_code,
    generate_python_code,
    python_round_trip_verify,
    python_to_runa_translate,
    runa_to_python_translate
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete Python language toolchain for universal code translation"

# Main toolchain instance
toolchain = PythonToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "PythonToolchain",
    
    # Parser components
    "parse_python", "PythonLexer", "PythonParser",
    
    # Converters
    "python_to_runa", "runa_to_python", "PythonToRunaConverter", "RunaToPythonConverter",
    
    # Generator
    "generate_python", "PythonCodeGenerator", "PythonCodeStyle", "PythonFormatter",
    
    # Convenience functions
    "parse_python_code", "generate_python_code", "python_round_trip_verify",
    "python_to_runa_translate", "runa_to_python_translate",
    
    # AST base classes (main ones)
    "PythonNode", "PythonExpression", "PythonStatement", "PythonDeclaration", "PythonType",
]

# Module metadata
__language__ = "python"
__tier__ = 1
__file_extensions__ = [".py", ".pyi", ".pyw"]
__mime_types__ = ["text/x-python", "application/x-python-code"]
