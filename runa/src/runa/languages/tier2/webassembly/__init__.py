#!/usr/bin/env python3
"""
WebAssembly Language Support for Runa

Complete WebAssembly toolchain providing parsing, AST conversion, code generation,
and round-trip verification for the Runa universal translation system.
"""

from .wasm_ast import *
from .wasm_parser import parse_wasm, WasmLexer, WasmParser
from .wasm_converter import wasm_to_runa, runa_to_wasm, WasmToRunaConverter, RunaToWasmConverter
from .wasm_generator import generate_wasm_code, WasmCodeGenerator, WasmCodeStyle, WasmFormatter
from .wasm_toolchain import (
    WasmToolchain,
    create_wasm_toolchain,
    wasm_to_runa_translation,
    runa_to_wasm_translation,
    verify_wasm_round_trip,
    parse_wasm_code,
    generate_wasm_code_from_ast
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete WebAssembly language toolchain for universal code translation"

# Main toolchain instance
toolchain = WasmToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "WasmToolchain",
    
    # Parser components
    "parse_wasm", "WasmLexer", "WasmParser",
    
    # Converters
    "wasm_to_runa", "runa_to_wasm", "WasmToRunaConverter", "RunaToWasmConverter",
    
    # Generator
    "generate_wasm_code", "WasmCodeGenerator", "WasmCodeStyle", "WasmFormatter",
    
    # Convenience functions
    "create_wasm_toolchain", "wasm_to_runa_translation", "runa_to_wasm_translation",
    "verify_wasm_round_trip", "parse_wasm_code", "generate_wasm_code_from_ast",
    
    # AST base classes (main ones)
    "WasmNode", "WasmModule", "WasmFunction", "WasmInstruction", "WasmType",
]

# Module metadata
__language__ = "webassembly"
__tier__ = 2
__file_extensions__ = [".wat", ".wast", ".wasm"]
__mime_types__ = ["application/wasm", "text/webassembly"]