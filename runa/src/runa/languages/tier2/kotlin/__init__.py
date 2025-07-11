#!/usr/bin/env python3
"""
Kotlin Language Support for Runa

Complete Kotlin toolchain providing parsing, AST conversion, code generation,
and round-trip verification for the Runa universal translation system.
"""

from .kotlin_ast import *
from .kotlin_parser import parse_kotlin, KotlinLexer, KotlinParser
from .kotlin_converter import kotlin_to_runa, runa_to_kotlin, KotlinToRunaConverter, RunaToKotlinConverter
from .kotlin_generator import generate_kotlin, KotlinCodeGenerator, KotlinCodeStyle, KotlinFormatter
from .kotlin_toolchain import (
    KotlinToolchain,
    parse_kotlin_code,
    generate_kotlin_code,
    kotlin_round_trip_verify,
    kotlin_to_runa_translate,
    runa_to_kotlin_translate
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete Kotlin language toolchain for universal code translation"

# Main toolchain instance
toolchain = KotlinToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "KotlinToolchain",
    
    # Parser components
    "parse_kotlin", "KotlinLexer", "KotlinParser",
    
    # Converters
    "kotlin_to_runa", "runa_to_kotlin", "KotlinToRunaConverter", "RunaToKotlinConverter",
    
    # Generator
    "generate_kotlin", "KotlinCodeGenerator", "KotlinCodeStyle", "KotlinFormatter",
    
    # Convenience functions
    "parse_kotlin_code", "generate_kotlin_code", "kotlin_round_trip_verify",
    "kotlin_to_runa_translate", "runa_to_kotlin_translate",
    
    # AST base classes (main ones)
    "KotlinNode", "KotlinExpression", "KotlinStatement", "KotlinDeclaration", "KotlinType",
]

# Module metadata
__language__ = "kotlin"
__tier__ = 2
__file_extensions__ = [".kt", ".kts"]
__mime_types__ = ["text/x-kotlin"]