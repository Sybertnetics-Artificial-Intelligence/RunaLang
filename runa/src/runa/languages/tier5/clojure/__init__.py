#!/usr/bin/env python3
"""
Clojure Language Support for Runa

Complete Clojure language toolchain providing parsing, AST conversion, code generation,
and round-trip verification for the Runa universal translation system.
"""

from .clojure_ast import *
from .clojure_parser import parse_clojure, ClojureLexer, ClojureParser
from .clojure_converter import clojure_to_runa, runa_to_clojure, ClojureToRunaConverter, RunaToClojureConverter
from .clojure_generator import generate_clojure, ClojureCodeGenerator, ClojureCodeStyle, ClojureFormatter
from .clojure_toolchain import (
    ClojureToolchain,
    parse_clojure_code,
    generate_clojure_code,
    clojure_round_trip_verify,
    clojure_to_runa_translate,
    runa_to_clojure_translate
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete Clojure language toolchain for universal code translation"

# Main toolchain instance
toolchain = ClojureToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "ClojureToolchain",
    
    # Parser components
    "parse_clojure", "ClojureLexer", "ClojureParser",
    
    # Converters
    "clojure_to_runa", "runa_to_clojure", "ClojureToRunaConverter", "RunaToClojureConverter",
    
    # Generator
    "generate_clojure", "ClojureCodeGenerator", "ClojureCodeStyle", "ClojureFormatter",
    
    # Convenience functions
    "parse_clojure_code", "generate_clojure_code", "clojure_round_trip_verify",
    "clojure_to_runa_translate", "runa_to_clojure_translate",
    
    # AST base classes (main ones)
    "ClojureNode", "ClojureExpression", "ClojureStatement", "ClojureDeclaration", "ClojureType",
]

# Module metadata
__language__ = "clojure"
__tier__ = 5
__file_extensions__ = [".clj", ".cljs", ".cljc", ".edn"]
__mime_types__ = ["text/x-clojure", "application/x-clojure"]
