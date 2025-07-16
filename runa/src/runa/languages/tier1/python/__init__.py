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
from .py_parser import parse_python, PythonASTConverter
from .py_converter import py_to_runa, runa_to_py, PyToRunaConverter, RunaToPyConverter
from .py_generator import generate_python, PyCodeGenerator
from .py_toolchain import (
    PythonToolchain,
    parse_py,
    generate_py,
    py_round_trip_verify,
    py_to_runa_translate,
    runa_to_py_translate
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
    "parse_python", "PythonASTConverter",
    
    # Converters
    "py_to_runa", "runa_to_py", "PyToRunaConverter", "RunaToPyConverter",
    
    # Generator
    "generate_python", "PyCodeGenerator",
    
    # Convenience functions
    "parse_py", "generate_py", "py_round_trip_verify",
    "py_to_runa_translate", "runa_to_py_translate",
    
    # AST base classes (main ones)
    "PythonNode", "PythonExpression", "PythonStatement", "PythonDeclaration", "PythonType",
]

# Module metadata
__language__ = "python"
__tier__ = 1
__file_extensions__ = [".py", ".pyi", ".pyw"]
__mime_types__ = ["text/x-python", "application/x-python-code"]
