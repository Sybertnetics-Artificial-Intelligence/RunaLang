#!/usr/bin/env python3
"""
Java Language Support for Runa Universal Translation System

This package provides comprehensive Java language support including:
- Modern Java parsing (Java 8 through Java 21)
- Bidirectional Java ” Runa AST conversion
- Clean Java code generation with multiple style options
- Round-trip translation verification
- Generics and type system support
- Lambda expressions and functional programming features
- Complete toolchain integration
"""

from .java_ast import *
from .java_parser import parse_java, JavaLexer, JavaParser
from .java_converter import java_to_runa, runa_to_java, JavaToRunaConverter, RunaToJavaConverter
from .java_generator import generate_java, JavaCodeGenerator, JavaCodeStyle, JavaFormatter
from .java_toolchain import (
    JavaToolchain,
    parse_java_code,
    generate_java_code,
    java_round_trip_verify,
    java_to_runa_translate,
    runa_to_java_translate
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Runa Universal Translation System"
__description__ = "Complete Java language toolchain for universal code translation"

# Main toolchain instance
toolchain = JavaToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "JavaToolchain",
    
    # Parser components
    "parse_java", "JavaLexer", "JavaParser",
    
    # Converters
    "java_to_runa", "runa_to_java", "JavaToRunaConverter", "RunaToJavaConverter",
    
    # Generator
    "generate_java", "JavaCodeGenerator", "JavaCodeStyle", "JavaFormatter",
    
    # Convenience functions
    "parse_java_code", "generate_java_code", "java_round_trip_verify",
    "java_to_runa_translate", "runa_to_java_translate",
]