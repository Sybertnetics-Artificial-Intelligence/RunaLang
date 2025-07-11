#!/usr/bin/env python3
"""
Scala Language Support for Runa

Complete Scala toolchain providing parsing, AST conversion, code generation,
and round-trip verification for the Runa universal translation system.
"""

from .scala_ast import *
from .scala_parser import parse_scala_code, ScalaLexer, ScalaParser
from .scala_converter import scala_to_runa, runa_to_scala, ScalaToRunaConverter, RunaToScalaConverter
from .scala_generator import generate_scala_code, ScalaCodeGenerator, ScalaCodeStyle, ScalaFormatter
from .scala_toolchain import (
    ScalaToolchain,
    create_scala_toolchain,
    scala_to_runa_translation,
    runa_to_scala_translation,
    verify_scala_round_trip
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete Scala language toolchain for universal code translation"

# Main toolchain instance
toolchain = ScalaToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "ScalaToolchain",
    
    # Parser components
    "parse_scala_code", "ScalaLexer", "ScalaParser",
    
    # Converters
    "scala_to_runa", "runa_to_scala", "ScalaToRunaConverter", "RunaToScalaConverter",
    
    # Generator
    "generate_scala_code", "ScalaCodeGenerator", "ScalaCodeStyle", "ScalaFormatter",
    
    # Convenience functions
    "create_scala_toolchain", "scala_to_runa_translation", "runa_to_scala_translation",
    "verify_scala_round_trip",
    
    # AST base classes (main ones)
    "ScalaNode", "ScalaExpression", "ScalaStatement", "ScalaDeclaration", "ScalaType",
]

# Module metadata
__language__ = "scala"
__tier__ = 2
__file_extensions__ = [".scala", ".sc"]
__mime_types__ = ["text/x-scala"]