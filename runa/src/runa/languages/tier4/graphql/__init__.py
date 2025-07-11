#!/usr/bin/env python3
"""
GraphQL Language Support for Runa

Complete GraphQL language toolchain providing parsing, AST conversion, code generation,
and round-trip verification for the Runa universal translation system.
"""

from .graphql_ast import *
from .graphql_parser import parse_graphql, GraphQLLexer, GraphQLParser
from .graphql_converter import graphql_to_runa, runa_to_graphql, GraphQLToRunaConverter, RunaToGraphQLConverter
from .graphql_generator import generate_graphql, GraphQLCodeGenerator, GraphQLCodeStyle, GraphQLFormatter
from .graphql_toolchain import (
    GraphQLToolchain,
    parse_graphql_code,
    generate_graphql_code,
    graphql_round_trip_verify,
    graphql_to_runa_translate,
    runa_to_graphql_translate
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete GraphQL language toolchain for universal code translation"

# Main toolchain instance
toolchain = GraphQLToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "GraphQLToolchain",
    
    # Parser components
    "parse_graphql", "GraphQLLexer", "GraphQLParser",
    
    # Converters
    "graphql_to_runa", "runa_to_graphql", "GraphQLToRunaConverter", "RunaToGraphQLConverter",
    
    # Generator
    "generate_graphql", "GraphQLCodeGenerator", "GraphQLCodeStyle", "GraphQLFormatter",
    
    # Convenience functions
    "parse_graphql_code", "generate_graphql_code", "graphql_round_trip_verify",
    "graphql_to_runa_translate", "runa_to_graphql_translate",
    
    # AST base classes (main ones)
    "GraphQLNode", "GraphQLExpression", "GraphQLStatement", "GraphQLDeclaration",
]

# Module metadata
__language__ = "graphql"
__tier__ = 4
__file_extensions__ = [".graphql", ".gql"]
__mime_types__ = ["application/graphql"]