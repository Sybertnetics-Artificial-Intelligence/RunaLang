#!/usr/bin/env python3
"""
SQL Language Support for Runa Universal Translation Platform

Complete SQL toolchain providing parsing, AST conversion, code generation,
and round-trip verification for the Runa universal translation system.
"""

from .sql_ast import *
from .sql_parser import parse_sql, SQLLexer, SQLParser
from .sql_converter import sql_to_runa, runa_to_sql, SQLToRunaConverter, RunaToSQLConverter
from .sql_generator import generate_sql, SQLCodeGenerator, SQLCodeStyle, SQLFormatter
from .sql_toolchain import (
    SQLToolchain,
    parse_sql_code,
    generate_sql_code,
    sql_round_trip_verify,
    sql_to_runa_translate,
    runa_to_sql_translate
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete SQL language toolchain for universal code translation"

# Main toolchain instance
toolchain = SQLToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "SQLToolchain",
    
    # Parser components
    "parse_sql", "SQLLexer", "SQLParser",
    
    # Converters
    "sql_to_runa", "runa_to_sql", "SQLToRunaConverter", "RunaToSQLConverter",
    
    # Generator
    "generate_sql", "SQLCodeGenerator", "SQLCodeStyle", "SQLFormatter",
    
    # Convenience functions
    "parse_sql_code", "generate_sql_code", "sql_round_trip_verify",
    "sql_to_runa_translate", "runa_to_sql_translate",
    
    # AST base classes (main ones)
    "SQLNode", "SQLExpression", "SQLStatement", "SQLDeclaration",
]

# Module metadata
__language__ = "sql"
__tier__ = 1
__file_extensions__ = [".sql"]
__mime_types__ = ["application/sql", "text/x-sql"]
