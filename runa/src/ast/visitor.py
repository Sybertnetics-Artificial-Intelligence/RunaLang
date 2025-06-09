"""
AST visitor interface and implementations.

This module defines the ASTVisitor interface and implementations for traversing
and processing the Abstract Syntax Tree (AST).
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

from .expressions import (
    BinaryExpression, BooleanLiteral, DictionaryExpression, Expression,
    FunctionCall, FunctionExpression, Identifier, IndexAccess, ListExpression,
    Literal, MemberAccess, NullLiteral, NumberLiteral, StringLiteral
)
from .statements import (
    Assignment, Block, Declaration, DisplayStatement, ExportStatement,
    FunctionDefinition, IfStatement, ImportStatement, LoopStatement,
    MatchStatement, Program, ReturnStatement, Statement, TryCatchStatement,
    WhileStatement
)
from .patterns import (
    DictionaryPattern, ListPattern, LiteralPattern, Pattern,
    TypePattern, VariablePattern, WildcardPattern
)
from .types import TypeAnnotation


class ASTVisitor(ABC):
    """Abstract base class for AST visitors."""

    # Program structure
    @abstractmethod
    def visit_program(self, node: Program) -> Any:
        """Visit a Program node."""
        pass

    # Statements
    @abstractmethod
    def visit_statement(self, node: Statement) -> Any:
        """Visit a Statement node."""
        pass

    @abstractmethod
    def visit_declaration(self, node: Declaration) -> Any:
        """Visit a Declaration node."""
        pass

    @abstractmethod
    def visit_assignment(self, node: Assignment) -> Any:
        """Visit an Assignment node."""
        pass

    @abstractmethod
    def visit_if_statement(self, node: IfStatement) -> Any:
        """Visit an IfStatement node."""
        pass

    @abstractmethod
    def visit_loop_statement(self, node: LoopStatement) -> Any:
        """Visit a LoopStatement node."""
        pass

    @abstractmethod
    def visit_while_statement(self, node: WhileStatement) -> Any:
        """Visit a WhileStatement node."""
        pass

    @abstractmethod
    def visit_function_definition(self, node: FunctionDefinition) -> Any:
        """Visit a FunctionDefinition node."""
        pass

    @abstractmethod
    def visit_return_statement(self, node: ReturnStatement) -> Any:
        """Visit a ReturnStatement node."""
        pass

    @abstractmethod
    def visit_display_statement(self, node: DisplayStatement) -> Any:
        """Visit a DisplayStatement node."""
        pass

    @abstractmethod
    def visit_block(self, node: Block) -> Any:
        """Visit a Block node."""
        pass

    @abstractmethod
    def visit_import_statement(self, node: ImportStatement) -> Any:
        """Visit an ImportStatement node."""
        pass

    @abstractmethod
    def visit_export_statement(self, node: ExportStatement) -> Any:
        """Visit an ExportStatement node."""
        pass

    @abstractmethod
    def visit_try_catch_statement(self, node: TryCatchStatement) -> Any:
        """Visit a TryCatchStatement node."""
        pass

    @abstractmethod
    def visit_match_statement(self, node: MatchStatement) -> Any:
        """Visit a MatchStatement node."""
        pass

    # Expressions
    @abstractmethod
    def visit_expression(self, node: Expression) -> Any:
        """Visit an Expression node."""
        pass

    @abstractmethod
    def visit_literal(self, node: Literal) -> Any:
        """Visit a Literal node."""
        pass

    @abstractmethod
    def visit_string_literal(self, node: StringLiteral) -> Any:
        """Visit a StringLiteral node."""
        pass

    @abstractmethod
    def visit_number_literal(self, node: NumberLiteral) -> Any:
        """Visit a NumberLiteral node."""
        pass

    @abstractmethod
    def visit_boolean_literal(self, node: BooleanLiteral) -> Any:
        """Visit a BooleanLiteral node."""
        pass

    @abstractmethod
    def visit_null_literal(self, node: NullLiteral) -> Any:
        """Visit a NullLiteral node."""
        pass

    @abstractmethod
    def visit_identifier(self, node: Identifier) -> Any:
        """Visit an Identifier node."""
        pass

    @abstractmethod
    def visit_binary_expression(self, node: BinaryExpression) -> Any:
        """Visit a BinaryExpression node."""
        pass

    @abstractmethod
    def visit_function_call(self, node: FunctionCall) -> Any:
        """Visit a FunctionCall node."""
        pass

    @abstractmethod
    def visit_list_expression(self, node: ListExpression) -> Any:
        """Visit a ListExpression node."""
        pass

    @abstractmethod
    def visit_dictionary_expression(self, node: DictionaryExpression) -> Any:
        """Visit a DictionaryExpression node."""
        pass

    @abstractmethod
    def visit_index_access(self, node: IndexAccess) -> Any:
        """Visit an IndexAccess node."""
        pass

    @abstractmethod
    def visit_member_access(self, node: MemberAccess) -> Any:
        """Visit a MemberAccess node."""
        pass

    @abstractmethod
    def visit_function_expression(self, node: FunctionExpression) -> Any:
        """Visit a FunctionExpression node."""
        pass

    @abstractmethod
    def visit_type_annotation(self, node: TypeAnnotation) -> Any:
        """Visit a TypeAnnotation node."""
        pass

    # Patterns
    @abstractmethod
    def visit_pattern(self, node: Pattern) -> Any:
        """Visit a Pattern node."""
        pass

    @abstractmethod
    def visit_literal_pattern(self, node: LiteralPattern) -> Any:
        """Visit a LiteralPattern node."""
        pass

    @abstractmethod
    def visit_variable_pattern(self, node: VariablePattern) -> Any:
        """Visit a VariablePattern node."""
        pass

    @abstractmethod
    def visit_wildcard_pattern(self, node: WildcardPattern) -> Any:
        """Visit a WildcardPattern node."""
        pass

    @abstractmethod
    def visit_list_pattern(self, node: ListPattern) -> Any:
        """Visit a ListPattern node."""
        pass

    @abstractmethod
    def visit_dictionary_pattern(self, node: DictionaryPattern) -> Any:
        """Visit a DictionaryPattern node."""
        pass

    @abstractmethod
    def visit_type_pattern(self, node: TypePattern) -> Any:
        """Visit a TypePattern node."""
        pass
        
    # AI-specific nodes
    @abstractmethod
    def visit_model_definition(self, node: 'ModelDefinition') -> Any:
        """Visit a ModelDefinition node."""
        pass
        
    @abstractmethod
    def visit_model_statement(self, node: 'ModelStatement') -> Any:
        """Visit a ModelStatement node."""
        pass
        
    @abstractmethod
    def visit_training_config(self, node: 'TrainingConfig') -> Any:
        """Visit a TrainingConfig node."""
        pass
        
    @abstractmethod
    def visit_training_statement(self, node: 'TrainingStatement') -> Any:
        """Visit a TrainingStatement node."""
        pass
        
    @abstractmethod
    def visit_knowledge_query(self, node: 'KnowledgeQuery') -> Any:
        """Visit a KnowledgeQuery node."""
        pass 