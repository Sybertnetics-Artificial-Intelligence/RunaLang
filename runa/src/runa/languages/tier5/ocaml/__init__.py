#!/usr/bin/env python3
"""
OCaml Language Support for Runa

Complete OCaml language toolchain providing parsing, AST conversion, code generation,
and round-trip verification for the Runa universal translation system.
"""

from .ocaml_ast import *
from .ocaml_parser import parse_ocaml, OcamlLexer, OcamlParser
from .ocaml_converter import ocaml_to_runa, runa_to_ocaml, OcamlToRunaConverter, RunaToOcamlConverter
from .ocaml_generator import generate_ocaml, OcamlCodeGenerator, OcamlCodeStyle, OcamlFormatter
from .ocaml_toolchain import (
    OcamlToolchain,
    parse_ocaml_code,
    generate_ocaml_code,
    ocaml_round_trip_verify,
    ocaml_to_runa_translate,
    runa_to_ocaml_translate
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete OCaml language toolchain for universal code translation"

# Main toolchain instance
toolchain = OcamlToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "OcamlToolchain",
    
    # Parser components
    "parse_ocaml", "OcamlLexer", "OcamlParser",
    
    # Converters
    "ocaml_to_runa", "runa_to_ocaml", "OcamlToRunaConverter", "RunaToOcamlConverter",
    
    # Generator
    "generate_ocaml", "OcamlCodeGenerator", "OcamlCodeStyle", "OcamlFormatter",
    
    # Convenience functions
    "parse_ocaml_code", "generate_ocaml_code", "ocaml_round_trip_verify",
    "ocaml_to_runa_translate", "runa_to_ocaml_translate",
    
    # AST base classes (main ones)
    "OcamlNode", "OcamlExpression", "OcamlStatement", "OcamlDeclaration", "OcamlType",
]

# Module metadata
__language__ = "ocaml"
__tier__ = 5
__file_extensions__ = [".ml", ".mli"]
__mime_types__ = ["text/x-ocaml"]
