"""
Abstract Syntax Tree (AST) Node Definitions for Runa Programming Language.

This module defines the complete hierarchy of AST nodes that represent the
structure of parsed Runa programs. Each node contains source position information
for debugging and error reporting.

The AST design follows the formal grammar specification and supports:
- Statements (declarations, assignments, control flow)
- Expressions (literals, binary operations, function calls)
- Types and type annotations
- AI/ML specific constructs
- Error handling constructs
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Any, Dict, Union
from dataclasses import dataclass
from enum import Enum, auto

from .errors import SourcePosition


class NodeType(Enum):
    """Enumeration of all AST node types (30+ types required)."""
    
    # Base nodes
    PROGRAM = auto()
    BLOCK = auto()
    
    # Statement nodes
    DECLARATION = auto()
    ASSIGNMENT = auto()
    EXPRESSION_STATEMENT = auto()
    RETURN_STATEMENT = auto()
    BREAK_STATEMENT = auto()
    CONTINUE_STATEMENT = auto()
    DISPLAY_STATEMENT = auto()
    INPUT_STATEMENT = auto()
    IMPORT_STATEMENT = auto()
    
    # Control flow statements
    IF_STATEMENT = auto()
    WHILE_LOOP = auto()
    FOR_LOOP = auto()
    TRY_CATCH_STATEMENT = auto()
    
    # Function/Process definitions
    PROCESS_DEFINITION = auto()
    PARAMETER = auto()
    
    # Expression nodes
    LITERAL = auto()
    IDENTIFIER = auto()
    BINARY_EXPRESSION = auto()
    UNARY_EXPRESSION = auto()
    FUNCTION_CALL = auto()
    MEMBER_ACCESS = auto()
    INDEX_ACCESS = auto()
    
    # Collection expressions
    LIST_EXPRESSION = auto()
    DICTIONARY_EXPRESSION = auto()
    KEY_VALUE_PAIR = auto()
    
    # AI/ML specific nodes
    MODEL_DEFINITION = auto()
    LAYER_DEFINITION = auto()
    TRAINING_CONFIG = auto()
    KNOWLEDGE_QUERY = auto()
    
    # Type nodes
    TYPE_ANNOTATION = auto()
    UNION_TYPE = auto()
    GENERIC_TYPE = auto()
    
    # Special nodes
    COMMENT = auto()
    EOF_NODE = auto()


@dataclass
class ASTNode(ABC):
    """
    Base class for all AST nodes.
    
    Every AST node contains position information for error reporting
    and debugging purposes.
    """
    position: SourcePosition
    node_type: NodeType
    
    @abstractmethod
    def accept(self, visitor: 'ASTVisitor') -> Any:
        """Accept a visitor for the visitor pattern."""
        pass
    
    def __str__(self) -> str:
        """String representation for debugging."""
        return f"{self.__class__.__name__}@{self.position}"


# ========== PROGRAM STRUCTURE ==========

@dataclass
class Program(ASTNode):
    """Root node representing the entire program."""
    statements: List['Statement']
    
    def __post_init__(self):
        self.node_type = NodeType.PROGRAM
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_program(self)


@dataclass
class Block(ASTNode):
    """A block of statements with its own scope."""
    statements: List['Statement']
    
    def __post_init__(self):
        self.node_type = NodeType.BLOCK
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_block(self)


# ========== STATEMENT NODES ==========

@dataclass
class Statement(ASTNode):
    """Base class for all statement nodes."""
    pass


@dataclass
class Declaration(Statement):
    """
    Variable declaration statement.
    Examples: "Let x be 5", "Define name as 'Alex'"
    """
    identifier: str
    type_annotation: Optional['TypeAnnotation']
    initializer: 'Expression'
    is_constant: bool  # True for 'define', False for 'let'
    
    def __post_init__(self):
        self.node_type = NodeType.DECLARATION
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_declaration(self)


@dataclass
class Assignment(Statement):
    """
    Variable assignment statement.
    Example: "Set x to 10"
    """
    identifier: str
    value: 'Expression'
    
    def __post_init__(self):
        self.node_type = NodeType.ASSIGNMENT
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_assignment(self)


@dataclass
class ExpressionStatement(Statement):
    """Statement that consists of a single expression."""
    expression: 'Expression'
    
    def __post_init__(self):
        self.node_type = NodeType.EXPRESSION_STATEMENT
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_expression_statement(self)


@dataclass
class ReturnStatement(Statement):
    """Return statement in functions."""
    value: Optional['Expression']
    
    def __post_init__(self):
        self.node_type = NodeType.RETURN_STATEMENT
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_return_statement(self)


@dataclass
class BreakStatement(Statement):
    """Break statement in loops."""
    
    def __post_init__(self):
        self.node_type = NodeType.BREAK_STATEMENT
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_break_statement(self)


@dataclass
class ContinueStatement(Statement):
    """Continue statement in loops."""
    
    def __post_init__(self):
        self.node_type = NodeType.CONTINUE_STATEMENT
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_continue_statement(self)


@dataclass
class DisplayStatement(Statement):
    """
    Display statement for output.
    Example: "Display x with message 'Result:'"
    """
    expression: 'Expression'
    message: Optional['Expression']
    
    def __post_init__(self):
        self.node_type = NodeType.DISPLAY_STATEMENT
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_display_statement(self)


@dataclass
class InputStatement(Statement):
    """
    Input statement for user input.
    Example: "input with prompt 'Enter name:'"
    """
    prompt: 'Expression'
    target: Optional[str]  # Variable to store input
    
    def __post_init__(self):
        self.node_type = NodeType.INPUT_STATEMENT
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_input_statement(self)


@dataclass
class ImportStatement(Statement):
    """
    Import statement for modules.
    Examples: "Import module 'math'", "Import sin from module 'math'"
    """
    module_name: str
    import_items: Optional[List[str]]  # None for full import
    alias: Optional[str]
    
    def __post_init__(self):
        self.node_type = NodeType.IMPORT_STATEMENT
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_import_statement(self)


# ========== CONTROL FLOW STATEMENTS ==========

@dataclass
class IfStatement(Statement):
    """
    Conditional statement.
    Example: "If x is greater than 5: ... Otherwise: ..."
    """
    condition: 'Expression'
    then_block: Block
    elif_clauses: List[tuple['Expression', Block]]  # List of (condition, block) pairs
    else_block: Optional[Block]
    
    def __post_init__(self):
        self.node_type = NodeType.IF_STATEMENT
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_if_statement(self)


@dataclass
class WhileLoop(Statement):
    """
    While loop statement.
    Example: "While x is less than 10: ..."
    """
    condition: 'Expression'
    body: Block
    
    def __post_init__(self):
        self.node_type = NodeType.WHILE_LOOP
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_while_loop(self)


@dataclass
class ForLoop(Statement):
    """
    For-each loop statement.
    Example: "For each item in list: ..."
    """
    variable: str
    iterable: 'Expression'
    body: Block
    
    def __post_init__(self):
        self.node_type = NodeType.FOR_LOOP
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_for_loop(self)


@dataclass
class TryCatchStatement(Statement):
    """
    Try-catch error handling statement.
    Example: "Try: ... Catch error: ..."
    """
    try_block: Block
    catch_variable: str
    catch_block: Block
    
    def __post_init__(self):
        self.node_type = NodeType.TRY_CATCH_STATEMENT
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_try_catch_statement(self)


# ========== FUNCTION/PROCESS DEFINITIONS ==========

@dataclass
class Parameter(ASTNode):
    """Function parameter definition."""
    name: str
    type_annotation: Optional['TypeAnnotation']
    default_value: Optional['Expression']
    
    def __post_init__(self):
        self.node_type = NodeType.PARAMETER
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_parameter(self)


@dataclass
class ProcessDefinition(Statement):
    """
    Function/process definition.
    Example: "Process called 'calculate' that takes x and y returns (integer): ..."
    """
    name: str
    parameters: List[Parameter]
    return_type: Optional['TypeAnnotation']
    body: Block
    
    def __post_init__(self):
        self.node_type = NodeType.PROCESS_DEFINITION
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_process_definition(self)


# ========== EXPRESSION NODES ==========

@dataclass
class Expression(ASTNode):
    """Base class for all expression nodes."""
    pass


@dataclass
class Literal(Expression):
    """
    Literal value expression.
    Examples: 42, "hello", true, null
    """
    value: Any
    literal_type: str  # 'number', 'string', 'boolean', 'null'
    
    def __post_init__(self):
        self.node_type = NodeType.LITERAL
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_literal(self)


@dataclass
class Identifier(Expression):
    """
    Identifier expression.
    Example: variable_name
    """
    name: str
    
    def __post_init__(self):
        self.node_type = NodeType.IDENTIFIER
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_identifier(self)


class BinaryOperator(Enum):
    """Binary operators in Runa."""
    # Arithmetic
    ADD = "plus"
    SUBTRACT = "minus"
    MULTIPLY = "multiplied by"
    DIVIDE = "divided by"
    MODULO = "modulo"
    CONCATENATE = "followed by"
    
    # Comparison
    EQUALS = "is equal to"
    NOT_EQUALS = "is not equal to"
    GREATER_THAN = "is greater than"
    LESS_THAN = "is less than"
    GREATER_EQUALS = "is greater than or equal to"
    LESS_EQUALS = "is less than or equal to"
    
    # Logical
    AND = "and"
    OR = "or"
    
    # Collection
    CONTAINS = "contains"
    IN = "in"
    
    # Access
    AT_INDEX = "at index"


@dataclass
class BinaryExpression(Expression):
    """
    Binary expression.
    Example: "x plus y", "a is greater than b"
    """
    left: Expression
    operator: BinaryOperator
    right: Expression
    
    def __post_init__(self):
        self.node_type = NodeType.BINARY_EXPRESSION
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_binary_expression(self)


class UnaryOperator(Enum):
    """Unary operators in Runa."""
    NOT = "not"
    MINUS = "negative"
    LENGTH = "length of"
    TYPE_OF = "type of"


@dataclass
class UnaryExpression(Expression):
    """
    Unary expression.
    Example: "not x", "length of list"
    """
    operator: UnaryOperator
    operand: Expression
    
    def __post_init__(self):
        self.node_type = NodeType.UNARY_EXPRESSION
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_unary_expression(self)


@dataclass
class FunctionCall(Expression):
    """
    Function call expression.
    Example: "calculate with x as 5 and y as 10"
    """
    function_name: str
    arguments: List[tuple[str, Expression]]  # Named arguments: [(name, value), ...]
    positional_args: List[Expression]  # Positional arguments for compatibility
    
    def __post_init__(self):
        self.node_type = NodeType.FUNCTION_CALL
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_function_call(self)


@dataclass
class MemberAccess(Expression):
    """
    Member access expression.
    Example: "object.property"
    """
    object: Expression
    member: str
    
    def __post_init__(self):
        self.node_type = NodeType.MEMBER_ACCESS
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_member_access(self)


@dataclass
class IndexAccess(Expression):
    """
    Index access expression.
    Example: "list[0]", "array at index 5"
    """
    object: Expression
    index: Expression
    
    def __post_init__(self):
        self.node_type = NodeType.INDEX_ACCESS
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_index_access(self)


# ========== COLLECTION EXPRESSIONS ==========

@dataclass
class ListExpression(Expression):
    """
    List literal expression.
    Example: "list containing 1, 2, 3"
    """
    elements: List[Expression]
    
    def __post_init__(self):
        self.node_type = NodeType.LIST_EXPRESSION
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_list_expression(self)


@dataclass
class KeyValuePair(ASTNode):
    """Key-value pair for dictionary literals."""
    key: Expression
    value: Expression
    
    def __post_init__(self):
        self.node_type = NodeType.KEY_VALUE_PAIR
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_key_value_pair(self)


@dataclass
class DictionaryExpression(Expression):
    """
    Dictionary literal expression.
    Example: "dictionary with: 'name' as 'Alex', 'age' as 25"
    """
    pairs: List[KeyValuePair]
    
    def __post_init__(self):
        self.node_type = NodeType.DICTIONARY_EXPRESSION
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_dictionary_expression(self)


# ========== AI/ML SPECIFIC NODES ==========

@dataclass
class ModelDefinition(Statement):
    """
    Neural network model definition.
    Example: "Define neural network 'classifier': ..."
    """
    name: str
    layers: List['LayerDefinition']
    configuration: Dict[str, Any]
    
    def __post_init__(self):
        self.node_type = NodeType.MODEL_DEFINITION
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_model_definition(self)


@dataclass
class LayerDefinition(ASTNode):
    """
    Neural network layer definition.
    Example: "Input layer accepts 784 features"
    """
    layer_type: str
    properties: Dict[str, Expression]
    
    def __post_init__(self):
        self.node_type = NodeType.LAYER_DEFINITION
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_layer_definition(self)


@dataclass
class TrainingConfig(Statement):
    """
    Training configuration for models.
    Example: "Configure training for model: ..."
    """
    model_name: str
    config_options: Dict[str, Expression]
    
    def __post_init__(self):
        self.node_type = NodeType.TRAINING_CONFIG
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_training_config(self)


@dataclass
class KnowledgeQuery(Expression):
    """
    Knowledge graph query expression.
    Example: "knowledge.query('find all persons')"
    """
    query_type: str
    query_string: str
    parameters: List[Expression]
    
    def __post_init__(self):
        self.node_type = NodeType.KNOWLEDGE_QUERY
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_knowledge_query(self)


# ========== TYPE NODES ==========

@dataclass
class TypeAnnotation(ASTNode):
    """
    Type annotation for variables and functions.
    Example: (integer), (string), (list of integer)
    """
    type_name: str
    generic_args: Optional[List['TypeAnnotation']]
    
    def __post_init__(self):
        self.node_type = NodeType.TYPE_ANNOTATION
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_type_annotation(self)


@dataclass
class UnionType(TypeAnnotation):
    """
    Union type annotation.
    Example: (integer or string)
    """
    types: List[TypeAnnotation]
    
    def __post_init__(self):
        self.node_type = NodeType.UNION_TYPE
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_union_type(self)


@dataclass
class GenericType(TypeAnnotation):
    """
    Generic type annotation.
    Example: (list of T), (dictionary of string to integer)
    """
    base_type: str
    type_params: List[TypeAnnotation]
    
    def __post_init__(self):
        self.node_type = NodeType.GENERIC_TYPE
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_generic_type(self)


# ========== SPECIAL NODES ==========

@dataclass
class Comment(ASTNode):
    """Comment node."""
    text: str
    
    def __post_init__(self):
        self.node_type = NodeType.COMMENT
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_comment(self)


@dataclass
class EOFNode(ASTNode):
    """End of file marker node."""
    
    def __post_init__(self):
        self.node_type = NodeType.EOF_NODE
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_eof_node(self)


# ========== VISITOR PATTERN ==========

class ASTVisitor(ABC):
    """
    Abstract base class for AST visitors.
    Implements the visitor pattern for AST traversal.
    """
    
    @abstractmethod
    def visit_program(self, node: Program) -> Any:
        pass
    
    @abstractmethod
    def visit_block(self, node: Block) -> Any:
        pass
    
    @abstractmethod
    def visit_declaration(self, node: Declaration) -> Any:
        pass
    
    @abstractmethod
    def visit_assignment(self, node: Assignment) -> Any:
        pass
    
    @abstractmethod
    def visit_expression_statement(self, node: ExpressionStatement) -> Any:
        pass
    
    @abstractmethod
    def visit_return_statement(self, node: ReturnStatement) -> Any:
        pass
    
    @abstractmethod
    def visit_break_statement(self, node: BreakStatement) -> Any:
        pass
    
    @abstractmethod
    def visit_continue_statement(self, node: ContinueStatement) -> Any:
        pass
    
    @abstractmethod
    def visit_display_statement(self, node: DisplayStatement) -> Any:
        pass
    
    @abstractmethod
    def visit_input_statement(self, node: InputStatement) -> Any:
        pass
    
    @abstractmethod
    def visit_import_statement(self, node: ImportStatement) -> Any:
        pass
    
    @abstractmethod
    def visit_if_statement(self, node: IfStatement) -> Any:
        pass
    
    @abstractmethod
    def visit_while_loop(self, node: WhileLoop) -> Any:
        pass
    
    @abstractmethod
    def visit_for_loop(self, node: ForLoop) -> Any:
        pass
    
    @abstractmethod
    def visit_try_catch_statement(self, node: TryCatchStatement) -> Any:
        pass
    
    @abstractmethod
    def visit_parameter(self, node: Parameter) -> Any:
        pass
    
    @abstractmethod
    def visit_process_definition(self, node: ProcessDefinition) -> Any:
        pass
    
    @abstractmethod
    def visit_literal(self, node: Literal) -> Any:
        pass
    
    @abstractmethod
    def visit_identifier(self, node: Identifier) -> Any:
        pass
    
    @abstractmethod
    def visit_binary_expression(self, node: BinaryExpression) -> Any:
        pass
    
    @abstractmethod
    def visit_unary_expression(self, node: UnaryExpression) -> Any:
        pass
    
    @abstractmethod
    def visit_function_call(self, node: FunctionCall) -> Any:
        pass
    
    @abstractmethod
    def visit_member_access(self, node: MemberAccess) -> Any:
        pass
    
    @abstractmethod
    def visit_index_access(self, node: IndexAccess) -> Any:
        pass
    
    @abstractmethod
    def visit_list_expression(self, node: ListExpression) -> Any:
        pass
    
    @abstractmethod
    def visit_key_value_pair(self, node: KeyValuePair) -> Any:
        pass
    
    @abstractmethod
    def visit_dictionary_expression(self, node: DictionaryExpression) -> Any:
        pass
    
    @abstractmethod
    def visit_model_definition(self, node: ModelDefinition) -> Any:
        pass
    
    @abstractmethod
    def visit_layer_definition(self, node: LayerDefinition) -> Any:
        pass
    
    @abstractmethod
    def visit_training_config(self, node: TrainingConfig) -> Any:
        pass
    
    @abstractmethod
    def visit_knowledge_query(self, node: KnowledgeQuery) -> Any:
        pass
    
    @abstractmethod
    def visit_type_annotation(self, node: TypeAnnotation) -> Any:
        pass
    
    @abstractmethod
    def visit_union_type(self, node: UnionType) -> Any:
        pass
    
    @abstractmethod
    def visit_generic_type(self, node: GenericType) -> Any:
        pass
    
    @abstractmethod
    def visit_comment(self, node: Comment) -> Any:
        pass
    
    @abstractmethod
    def visit_eof_node(self, node: EOFNode) -> Any:
        pass


# Export all node types for easy importing
__all__ = [
    # Base classes
    'ASTNode', 'Statement', 'Expression', 'ASTVisitor',
    
    # Enums
    'NodeType', 'BinaryOperator', 'UnaryOperator',
    
    # Program structure
    'Program', 'Block',
    
    # Statement nodes
    'Declaration', 'Assignment', 'ExpressionStatement', 'ReturnStatement',
    'BreakStatement', 'ContinueStatement', 'DisplayStatement', 'InputStatement',
    'ImportStatement', 'IfStatement', 'WhileLoop', 'ForLoop', 'TryCatchStatement',
    'ProcessDefinition', 'Parameter',
    
    # Expression nodes
    'Literal', 'Identifier', 'BinaryExpression', 'UnaryExpression',
    'FunctionCall', 'MemberAccess', 'IndexAccess', 'ListExpression',
    'KeyValuePair', 'DictionaryExpression',
    
    # AI/ML nodes
    'ModelDefinition', 'LayerDefinition', 'TrainingConfig', 'KnowledgeQuery',
    
    # Type nodes
    'TypeAnnotation', 'UnionType', 'GenericType',
    
    # Special nodes
    'Comment', 'EOFNode',
] 