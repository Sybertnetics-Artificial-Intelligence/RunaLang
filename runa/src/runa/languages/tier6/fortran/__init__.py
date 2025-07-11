#!/usr/bin/env python3
"""
Fortran Language Support for Runa

Complete Fortran toolchain providing parsing, AST conversion, code generation,
and round-trip verification for the Runa universal translation system.
"""

from .fortran_ast import *
from .fortran_parser import parse_fortran, FortranLexer, FortranParser
from .fortran_converter import fortran_to_runa, runa_to_fortran, FortranToRunaConverter, RunaToFortranConverter
from .fortran_generator import generate_fortran, FortranCodeGenerator, FortranCodeStyle, FortranFormatter
from .fortran_toolchain import (
    FortranToolchain,
    parse_fortran_code,
    generate_fortran_code,
    fortran_round_trip_verify,
    fortran_to_runa_translate,
    runa_to_fortran_translate
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete Fortran language toolchain for universal code translation"

# Main toolchain instance
toolchain = FortranToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "FortranToolchain",
    
    # Parser components
    "parse_fortran", "FortranLexer", "FortranParser",
    
    # Converters
    "fortran_to_runa", "runa_to_fortran", "FortranToRunaConverter", "RunaToFortranConverter",
    
    # Generator
    "generate_fortran", "FortranCodeGenerator", "FortranCodeStyle", "FortranFormatter",
    
    # Convenience functions
    "parse_fortran_code", "generate_fortran_code", "fortran_round_trip_verify",
    "fortran_to_runa_translate", "runa_to_fortran_translate",
    
    # AST base classes (main ones)
    "FortranNode", "FortranExpression", "FortranStatement", "FortranDeclaration", "FortranType",
]

# Module metadata
__language__ = "fortran"
__tier__ = 6
__file_extensions__ = [".f", ".f90", ".f95", ".f03", ".f08", ".f18", ".for", ".ftn"]
__mime_types__ = ["text/x-fortran"]
