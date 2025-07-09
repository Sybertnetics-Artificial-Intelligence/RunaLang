#!/usr/bin/env python3
"""
TypeScript Language Support for Runa

Complete TypeScript toolchain providing parsing, AST conversion, code generation,
and round-trip verification for the Runa universal translation system.
"""

from .ts_ast import *
from .ts_parser import parse_typescript
from .ts_converter import ts_to_runa, runa_to_ts
from .ts_generator import TSCodeGenerator, generate_typescript
from .ts_toolchain import (
    TypeScriptToolchain,
    parse_ts,
    generate_ts,
    ts_round_trip_verify,
    ts_to_runa_translate,
    runa_to_ts_translate
)

__all__ = [
    # AST classes
    "TSNode",
    "TSProgram",
    "TSLiteral",
    "TSIdentifier",
    "TSType",
    "TSTypeAnnotation",
    "TSTypeReference",
    "TSUnionType",
    "TSIntersectionType",
    "TSTupleType",
    "TSArrayType",
    "TSFunctionType",
    "TSTypeLiteral",
    "TSMappedType",
    "TSConditionalType",
    "TSIndexedAccessType",
    "TSTypeofType",
    "TSKeyofType",
    "TSTypeParameter",
    "TSTypeAssertion",
    "TSTypePredicate",
    "TSParameter",
    "TSInterfaceDeclaration",
    "TSTypeAliasDeclaration",
    "TSEnumDeclaration",
    "TSEnumMember",
    "TSNamespaceDeclaration",
    "TSModuleDeclaration",
    "TSDecorator",
    "TSMethodSignature",
    "TSPropertySignature",
    "TSCallSignature",
    "TSConstructSignature",
    "TSIndexSignature",
    "TSVariableDeclaration",
    "TSVariableDeclarator",
    "TSFunctionDeclaration",
    "TSClassDeclaration",
    "TSBlockStatement",
    
    # Enums
    "TSNodeType",
    "TSLiteralType",
    "TSOperator",
    "TSVariableKind",
    "TSAccessModifier",
    "TSTypeKeyword",
    
    # Parser
    "parse_typescript",
    
    # Converter
    "ts_to_runa",
    "runa_to_ts",
    
    # Generator
    "TSCodeGenerator",
    "generate_typescript",
    
    # Toolchain
    "TypeScriptToolchain",
    "parse_ts",
    "generate_ts",
    "ts_round_trip_verify",
    "ts_to_runa_translate",
    "runa_to_ts_translate",
]

# Module metadata
__version__ = "1.0.0"
__author__ = "Runa Development Team"
__description__ = "TypeScript language support for Runa universal translation system"
__language__ = "typescript"
__tier__ = 1
__file_extensions__ = [".ts", ".tsx", ".d.ts"]
__mime_types__ = ["application/typescript", "text/typescript"]