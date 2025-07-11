#!/usr/bin/env python3
"""
OpenCL Language Support for Runa Universal Translation System

This package provides comprehensive OpenCL C language support including:
- Complete OpenCL C parsing (OpenCL 1.0 through OpenCL 3.0)
- Bidirectional OpenCL ↔ Runa AST conversion
- Clean OpenCL C code generation with multiple style options
- Round-trip translation verification
- Kernel function and memory qualifier support
- Vector operations and built-in function support
- Complete toolchain integration with OpenCL SDK
"""

from .opencl_ast import *
from .opencl_parser import parse_opencl, OpenCLLexer, OpenCLParser
from .opencl_converter import opencl_to_runa, runa_to_opencl, OpenCLToRunaConverter, RunaToOpenCLConverter
from .opencl_generator import generate_opencl, OpenCLCodeGenerator, OpenCLCodeStyle, OpenCLFormatter
from .opencl_toolchain import (
    OpenCLToolchain,
    parse_opencl_code,
    generate_opencl_code,
    opencl_round_trip_verify,
    opencl_to_runa_translate,
    runa_to_opencl_translate
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete OpenCL language toolchain for universal code translation"

# Main toolchain instance
toolchain = OpenCLToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "OpenCLToolchain",
    
    # Parser components
    "parse_opencl", "OpenCLLexer", "OpenCLParser",
    
    # Converters
    "opencl_to_runa", "runa_to_opencl", "OpenCLToRunaConverter", "RunaToOpenCLConverter",
    
    # Generator
    "generate_opencl", "OpenCLCodeGenerator", "OpenCLCodeStyle", "OpenCLFormatter",
    
    # Convenience functions
    "parse_opencl_code", "generate_opencl_code", "opencl_round_trip_verify",
    "opencl_to_runa_translate", "runa_to_opencl_translate",
    
    # AST base classes (main ones)
    "OpenCLNode", "OpenCLExpression", "OpenCLStatement", "OpenCLDeclaration", "OpenCLType",
]

# Module metadata
__language__ = "opencl"
__tier__ = 7
__file_extensions__ = [".cl", ".ocl"]
__mime_types__ = ["text/x-opencl", "application/x-opencl-source"]
