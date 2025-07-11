#!/usr/bin/env python3
"""
Move Language Support for Runa Universal Translation System

This package provides comprehensive Move language support including:
- Resource-oriented smart contract parsing
- Bidirectional Move ↔ Runa AST conversion
- Clean Move code generation with resource-oriented syntax
- Round-trip translation verification
- Abilities system validation and analysis
- Move semantics and ownership tracking
- Gas optimization analysis
- Formal verification support
- Complete toolchain integration
"""

from .move_ast import *
from .move_parser import parse_move_source, MoveLexer, MoveParser
from .move_converter import move_to_runa, runa_to_move, MoveToRunaConverter, RunaToMoveConverter
from .move_generator import generate_move_code, MoveCodeGenerator, MoveCodeStyle
from .move_toolchain import (
    MoveToolchain,
    parse_move_code,
    generate_move_code,
    move_round_trip_verify,
    move_to_runa_translate,
    runa_to_move_translate,
    create_move_toolchain,
    parse_move_file,
    validate_move_file,
    analyze_contract_security,
    optimize_move_file
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete Move language toolchain for universal resource-oriented smart contract translation"

# Main toolchain instance
toolchain = MoveToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "MoveToolchain",
    
    # Parser components
    "parse_move_source", "MoveLexer", "MoveParser",
    
    # Converters
    "move_to_runa", "runa_to_move", "MoveToRunaConverter", "RunaToMoveConverter",
    
    # Generator
    "generate_move_code", "MoveCodeGenerator", "MoveCodeStyle",
    
    # Convenience functions
    "parse_move_code", "move_round_trip_verify",
    "move_to_runa_translate", "runa_to_move_translate",
    "create_move_toolchain", "parse_move_file", "validate_move_file",
    "analyze_contract_security", "optimize_move_file",
    
    # AST base classes (main ones)
    "MoveNode", "MoveExpression", "MoveStatement", "MoveDeclaration", "MoveType",
    
    # Move-specific classes
    "MoveAbility", "MoveVisibility", "MovePrimitiveType", "MoveOperator",
    "MoveModule", "MoveScript", "MoveProgram",
    "MoveStructDeclaration", "MoveFunctionDeclaration", "MoveParameter", "MoveField",
    "MovePrimitive", "MoveStructType", "MoveVectorType", "MoveReferenceType",
    "MoveLiteral", "MoveIdentifier", "MoveFunctionCall", "MoveBorrow", "MoveMove", "MoveCopy",
    "MoveBlock", "MoveVariableDeclaration", "MoveAssignment", "MoveReturn", "MoveAbort"
]

# Module metadata
__language__ = "move"
__tier__ = 4
__file_extensions__ = [".move"]
__mime_types__ = ["text/x-move"]
