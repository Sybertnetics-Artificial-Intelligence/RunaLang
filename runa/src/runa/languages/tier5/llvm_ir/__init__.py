#!/usr/bin/env python3
"""
LLVM IR Language Support for Runa

Complete LLVM IR language toolchain providing parsing, AST conversion, code generation,
and round-trip verification for the Runa universal translation system.
"""

from .llvm_ir_ast import *
from .llvm_ir_parser import parse_llvm_ir, LlvmIrLexer, LlvmIrParser
from .llvm_ir_converter import llvm_ir_to_runa, runa_to_llvm_ir, LlvmIrToRunaConverter, RunaToLlvmIrConverter
from .llvm_ir_generator import generate_llvm_ir, LlvmIrCodeGenerator, LlvmIrCodeStyle, LlvmIrFormatter
from .llvm_ir_toolchain import (
    LlvmIrToolchain,
    parse_llvm_ir_code,
    generate_llvm_ir_code,
    llvm_ir_round_trip_verify,
    llvm_ir_to_runa_translate,
    runa_to_llvm_ir_translate
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete LLVM IR language toolchain for universal code translation"

# Main toolchain instance
toolchain = LlvmIrToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "LlvmIrToolchain",
    
    # Parser components
    "parse_llvm_ir", "LlvmIrLexer", "LlvmIrParser",
    
    # Converters
    "llvm_ir_to_runa", "runa_to_llvm_ir", "LlvmIrToRunaConverter", "RunaToLlvmIrConverter",
    
    # Generator
    "generate_llvm_ir", "LlvmIrCodeGenerator", "LlvmIrCodeStyle", "LlvmIrFormatter",
    
    # Convenience functions
    "parse_llvm_ir_code", "generate_llvm_ir_code", "llvm_ir_round_trip_verify",
    "llvm_ir_to_runa_translate", "runa_to_llvm_ir_translate",
    
    # AST base classes (main ones)
    "LlvmIrNode", "LlvmIrExpression", "LlvmIrStatement", "LlvmIrDeclaration", "LlvmIrType",
]

# Module metadata
__language__ = "llvm_ir"
__tier__ = 5
__file_extensions__ = [".ll", ".bc"]
__mime_types__ = ["text/x-llvm", "application/x-llvm"]
