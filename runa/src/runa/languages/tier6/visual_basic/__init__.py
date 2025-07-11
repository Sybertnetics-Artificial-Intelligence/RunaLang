#!/usr/bin/env python3
"""
Visual Basic Language Support for Runa

Complete Visual Basic toolchain providing parsing, AST conversion, code generation,
and round-trip verification for the Runa universal translation system.
"""

from .visual_basic_ast import *
from .visual_basic_parser import parse_visual_basic, VisualBasicLexer, VisualBasicParser
from .visual_basic_converter import visual_basic_to_runa, runa_to_visual_basic, VisualBasicToRunaConverter, RunaToVisualBasicConverter
from .visual_basic_generator import generate_visual_basic, VisualBasicCodeGenerator, VisualBasicCodeStyle, VisualBasicFormatter
from .visual_basic_toolchain import (
    VisualBasicToolchain,
    parse_visual_basic_code,
    generate_visual_basic_code,
    visual_basic_round_trip_verify,
    visual_basic_to_runa_translate,
    runa_to_visual_basic_translate
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete Visual Basic language toolchain for universal code translation"

# Main toolchain instance
toolchain = VisualBasicToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "VisualBasicToolchain",
    
    # Parser components
    "parse_visual_basic", "VisualBasicLexer", "VisualBasicParser",
    
    # Converters
    "visual_basic_to_runa", "runa_to_visual_basic", "VisualBasicToRunaConverter", "RunaToVisualBasicConverter",
    
    # Generator
    "generate_visual_basic", "VisualBasicCodeGenerator", "VisualBasicCodeStyle", "VisualBasicFormatter",
    
    # Convenience functions
    "parse_visual_basic_code", "generate_visual_basic_code", "visual_basic_round_trip_verify",
    "visual_basic_to_runa_translate", "runa_to_visual_basic_translate",
    
    # AST base classes (main ones)
    "VisualBasicNode", "VisualBasicExpression", "VisualBasicStatement", "VisualBasicDeclaration", "VisualBasicType",
]

# Module metadata
__language__ = "visual_basic"
__tier__ = 6
__file_extensions__ = [".vb", ".vbs", ".bas", ".cls", ".frm"]
__mime_types__ = ["text/x-vb"]
