"""
Base AST Nodes for Runa
=======================

Base AST node classes to avoid circular imports.
"""

from typing import Optional
from dataclasses import dataclass
from enum import Enum, auto


class NodeType(Enum):
    """AST node types for comprehensive language support."""
    
    # Program Structure
    PROGRAM = auto()
    MODULE = auto()
    IMPORT = auto()
    EXPORT = auto()
    
    # Declarations
    VARIABLE_DECLARATION = auto()
    FUNCTION_DECLARATION = auto()
    TYPE_DECLARATION = auto()
    CONSTANT_DECLARATION = auto()
    
    # Statements
    EXPRESSION_STATEMENT = auto()
    IF_STATEMENT = auto()
    FOR_STATEMENT = auto()
    WHILE_STATEMENT = auto()
    RETURN_STATEMENT = auto()
    BREAK_STATEMENT = auto()
    CONTINUE_STATEMENT = auto()
    TRY_STATEMENT = auto()
    THROW_STATEMENT = auto()
    DISPLAY_STATEMENT = auto()
    
    # Expressions
    BINARY_EXPRESSION = auto()
    UNARY_EXPRESSION = auto()
    CALL_EXPRESSION = auto()
    MEMBER_EXPRESSION = auto()
    ARRAY_EXPRESSION = auto()
    DICTIONARY_EXPRESSION = auto()
    LITERAL = auto()
    IDENTIFIER = auto()
    
    # AI-Specific Nodes
    REASONING_BLOCK = auto()
    IMPLEMENTATION_BLOCK = auto()
    VERIFICATION_BLOCK = auto()
    LLM_COMMUNICATION = auto()
    AI_AGENT_DEFINITION = auto()
    NEURAL_NETWORK_DEFINITION = auto()
    KNOWLEDGE_QUERY = auto()
    SELF_MODIFICATION = auto()
    
    # Type System
    TYPE_ANNOTATION = auto()
    GENERIC_TYPE = auto()
    UNION_TYPE = auto()
    INTERSECTION_TYPE = auto()
    FUNCTION_TYPE = auto()
    
    # Control Flow
    CONDITIONAL_EXPRESSION = auto()
    PATTERN_MATCHING = auto()
    GUARD_CLAUSE = auto()
    
    # Special Constructs
    UNCERTAINTY_EXPRESSION = auto()
    CONFIDENCE_EXPRESSION = auto()
    ANNOTATION = auto()


class ASTNode:
    """Base AST node with comprehensive metadata."""
    def __init__(self, node_type: NodeType, line: int, column: int, source_file: Optional[str] = None):
        self.node_type = node_type
        self.line = line
        self.column = column
        self.source_file = source_file
    
    def __str__(self) -> str:
        return f"{self.node_type.name}(line={self.line}, col={self.column})"


class Statement:
    """Base statement node."""
    def __init__(self, node_type: NodeType, line: int, column: int, source_file: Optional[str] = None):
        self.node_type = node_type
        self.line = line
        self.column = column
        self.source_file = source_file


class Expression:
    """Base expression node."""
    def __init__(self, node_type: NodeType, line: int, column: int, source_file: Optional[str] = None):
        self.node_type = node_type
        self.line = line
        self.column = column
        self.source_file = source_file 