#!/usr/bin/env python3
"""
Lua Language Support for Runa Universal Translation System

This package provides comprehensive Lua language support including:
- Complete Lua 5.1-5.4 parsing with LuaJIT compatibility
- Tables, functions, coroutines, and metatable support
- Bidirectional Lua ↔ Runa AST conversion
- Clean Lua code generation with multiple style options
- Round-trip translation verification
- Love2D, OpenResty, and LuaRocks project support
- Comprehensive toolchain integration with Lua interpreters
- Testing framework integration (busted, luaunit)
- Static analysis and linting with luacheck
"""

from .lua_ast import *
from .lua_parser import parse_lua, LuaParser, LuaLexer
from .lua_converter import lua_to_runa, runa_to_lua, LuaToRunaConverter, RunaToLuaConverter
from .lua_generator import generate_lua, LuaCodeGenerator, LuaFormatStyle, LuaFormatter
from .lua_toolchain import (
    LuaToolchain,
    parse_lua_code,
    generate_lua_code,
    lua_round_trip_verify,
    lua_to_runa_translate,
    runa_to_lua_translate
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete Lua language toolchain for universal code translation"

# Main toolchain instance
toolchain = LuaToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "LuaToolchain",
    
    # Parser components
    "parse_lua", "LuaParser", "LuaLexer",
    
    # Converters
    "lua_to_runa", "runa_to_lua", "LuaToRunaConverter", "RunaToLuaConverter",
    
    # Generator
    "generate_lua", "LuaCodeGenerator", "LuaFormatStyle", "LuaFormatter",
    
    # Convenience functions
    "parse_lua_code", "generate_lua_code", "lua_round_trip_verify",
    "lua_to_runa_translate", "runa_to_lua_translate",
    
    # AST base classes (main ones)
    "LuaNode", "LuaExpression", "LuaStatement", "LuaModule", "LuaBlock",
    
    # Core expressions
    "LuaLiteral", "LuaIdentifier", "LuaBinaryOperation", "LuaUnaryOperation",
    "LuaTableConstructor", "LuaTableField", "LuaTableAccess", "LuaFunctionCall",
    "LuaFunctionDefinition", "LuaVarargExpression",
    
    # Core statements
    "LuaAssignment", "LuaLocalDeclaration", "LuaFunctionDeclaration",
    "LuaIfStatement", "LuaElseIfClause", "LuaWhileStatement", "LuaRepeatStatement",
    "LuaForStatement", "LuaForInStatement", "LuaBreakStatement", "LuaContinueStatement",
    "LuaReturnStatement", "LuaGotoStatement", "LuaLabelStatement", 
    "LuaExpressionStatement", "LuaDoStatement",
    
    # Literals
    "LuaStringLiteral", "LuaNumberLiteral",
    
    # Comments and modules
    "LuaComment", "LuaRequireStatement",
    
    # Advanced features
    "LuaMetatableOperation", "LuaCoroutineExpression", "LuaStringInterpolation",
    
    # Enums and types
    "LuaBinaryOperator", "LuaUnaryOperator", "LuaLiteralType",
    
    # Visitor pattern
    "LuaVisitor", "LuaBaseVisitor",
    
    # Helper functions
    "create_lua_identifier", "create_lua_number", "create_lua_string",
    "create_lua_table", "create_lua_function", "create_lua_block", "create_lua_module",
]

# Module metadata
__language__ = "lua"
__tier__ = 3
__file_extensions__ = [".lua"]
__mime_types__ = ["text/x-lua", "application/x-lua"]
