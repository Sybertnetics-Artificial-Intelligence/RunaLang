"""
Runa Language Abstract Syntax Tree Nodes

SECG Compliance: All AST nodes support ethical validation and transparency
Self-Hosting Support: AST nodes designed to represent Runa compiler source code
Type Safety: Complete type annotations for all nodes

This module defines AST nodes for all Runa language constructs including:
- Variable declarations (Let, Define, Set)
- Function definitions (Process)
- Control structures (If, For, Match)
- Pattern matching and type definitions
- Natural language expressions
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Union, Any, Dict, Type
from enum import Enum, auto

# Base AST Node Classes
class ASTNode(ABC):
    """
    Base class for all AST nodes.
    
    Provides common functionality including source position tracking,
    SECG compliance validation, and visitor pattern support.
    """
    
    def __init__(self, line: int = 0, column: int = 0):
        self.line = line
        self.column = column
        self.parent: Optional['ASTNode'] = None
        self.metadata: Dict[str, Any] = {}
    
    @abstractmethod
    def accept(self, visitor: 'ASTVisitor') -> Any:
        """Accept visitor for traversal."""
        pass
    
    def get_children(self) -> List['ASTNode']:
        """Get all child nodes."""
        children = []
        for attr_name in dir(self):
            if not attr_name.startswith('_'):
                attr = getattr(self, attr_name)
                if isinstance(attr, ASTNode):
                    children.append(attr)
                elif isinstance(attr, list):
                    children.extend([item for item in attr if isinstance(item, ASTNode)])
        return children
    
    def set_parent_references(self):
        """Set parent references for all child nodes."""
        for child in self.get_children():
            child.parent = self
            child.set_parent_references()

# Expression Nodes
class Expression(ASTNode):
    """Base class for all expressions."""
    pass

@dataclass
class Identifier(Expression):
    """Identifier expression (variable name, function name, etc.)."""
    name: str
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_identifier(self)

@dataclass
class Literal(Expression):
    """Base class for literal values."""
    value: Any
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_literal(self)

@dataclass
class StringLiteral(Literal):
    """String literal expression."""
    value: str
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_string_literal(self)

@dataclass
class IntegerLiteral(Literal):
    """Integer literal expression."""
    value: int
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_integer_literal(self)

@dataclass
class FloatLiteral(Literal):
    """Float literal expression."""
    value: float
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_float_literal(self)

@dataclass
class BooleanLiteral(Literal):
    """Boolean literal expression."""
    value: bool
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_boolean_literal(self)

@dataclass
class NoneLiteral(Literal):
    """None literal expression."""
    value: None = None
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_none_literal(self)

# Binary Operations (Natural Language)
class BinaryOperator(Enum):
    """Binary operators in natural language form."""
    PLUS = "plus"
    MINUS = "minus"
    MULTIPLIED_BY = "multiplied by"
    DIVIDED_BY = "divided by"
    IS_EQUAL = "is equal to"
    IS_GREATER_THAN = "is greater than"
    IS_LESS_THAN = "is less than"
    IS_GREATER_OR_EQUAL = "is greater than or equal to"
    IS_LESS_OR_EQUAL = "is less than or equal to"
    AND = "and"
    OR = "or"

@dataclass
class BinaryOperation(Expression):
    """Binary operation expression (e.g., 'a plus b', 'x is equal to y')."""
    left: Expression
    operator: BinaryOperator
    right: Expression
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_binary_operation(self)

@dataclass
class UnaryOperation(Expression):
    """Unary operation expression (e.g., 'not x')."""
    operator: str
    operand: Expression
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_unary_operation(self)

# Function Calls
@dataclass
class FunctionCall(Expression):
    """Function call expression with Runa's 'with' syntax."""
    function_name: str
    arguments: List['Argument']
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_function_call(self)

@dataclass
class Argument:
    """Function argument with optional name."""
    name: Optional[str]  # For 'param as value' syntax
    value: Expression
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_argument(self)

# Collection Expressions
@dataclass
class ListExpression(Expression):
    """List expression (e.g., 'list containing "a", "b", "c"')."""
    elements: List[Expression]
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_list_expression(self)

@dataclass
class DictionaryExpression(Expression):
    """Dictionary expression with key-value pairs."""
    pairs: List['DictionaryPair']
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_dictionary_expression(self)

@dataclass
class DictionaryPair:
    """Key-value pair in dictionary."""
    key: Expression
    value: Expression
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_dictionary_pair(self)

# Statements
class Statement(ASTNode):
    """Base class for all statements."""
    pass

# Variable Declarations
@dataclass
class VariableDeclaration(Statement):
    """Variable declaration statement."""
    name: str
    value: Optional[Expression]
    type_annotation: Optional['TypeExpression']
    declaration_type: str  # "Let", "Define", "Set"
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_variable_declaration(self)

# Function Definitions
@dataclass
class Parameter:
    """Function parameter."""
    name: str
    type_annotation: Optional['TypeExpression'] = None
    default_value: Optional[Expression] = None

@dataclass
class FunctionDefinition(Statement):
    """Function definition ('Process called')."""
    name: str
    parameters: List[Parameter]
    return_type: Optional['TypeExpression']
    body: List[Statement]
    is_async: bool = False
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_function_definition(self)

@dataclass
class ReturnStatement(Statement):
    """Return statement."""
    value: Optional[Expression]
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_return_statement(self)

# Control Flow Statements
@dataclass
class IfStatement(Statement):
    """If-Otherwise statement."""
    condition: Expression
    then_block: List[Statement]
    else_block: Optional[List[Statement]] = None
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_if_statement(self)

@dataclass
class ForStatement(Statement):
    """For each statement."""
    variable: str
    iterable: Expression
    body: List[Statement]
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_for_statement(self)

@dataclass
class WhileStatement(Statement):
    """While statement."""
    condition: Expression
    body: List[Statement]
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_while_statement(self)

# Pattern Matching
@dataclass
class MatchStatement(Statement):
    """Match statement with pattern cases."""
    value: Expression
    cases: List['MatchCase']
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_match_statement(self)

@dataclass
class MatchCase:
    """Individual case in match statement."""
    pattern: 'Pattern'
    body: List[Statement]
    guard: Optional[Expression] = None  # Optional when condition
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_match_case(self)

# Patterns for Pattern Matching
class Pattern(ASTNode):
    """Base class for patterns in match statements."""
    pass

@dataclass
class LiteralPattern(Pattern):
    """Literal pattern (e.g., When "admin":)."""
    value: Literal
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_literal_pattern(self)

@dataclass
class IdentifierPattern(Pattern):
    """Identifier pattern for binding variables."""
    name: str
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_identifier_pattern(self)

@dataclass
class WildcardPattern(Pattern):
    """Wildcard pattern (_)."""
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_wildcard_pattern(self)

@dataclass
class ConstructorPattern(Pattern):
    """Constructor pattern for algebraic data types."""
    constructor: str
    fields: List[Pattern]
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_constructor_pattern(self)

@dataclass
class ListPattern(Pattern):
    """List pattern for matching list structure."""
    elements: List[Pattern]
    has_rest: bool = False  # For patterns like [first, rest...]
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_list_pattern(self)

# Type System
class TypeExpression(ASTNode):
    """Base class for type expressions."""
    pass

@dataclass
class SimpleType(TypeExpression):
    """Simple type (Integer, String, etc.)."""
    name: str
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_simple_type(self)

@dataclass
class GenericType(TypeExpression):
    """Generic type (List[String], Dictionary[String, Integer])."""
    base_type: str
    type_parameters: List[TypeExpression]
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_generic_type(self)

@dataclass
class UnionType(TypeExpression):
    """Union type (Integer OR String)."""
    types: List[TypeExpression]
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_union_type(self)

@dataclass
class FunctionType(TypeExpression):
    """Function type annotation."""
    parameter_types: List[TypeExpression]
    return_type: TypeExpression
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_function_type(self)

# Type Definitions
@dataclass
class TypeDefinition(Statement):
    """Type definition statement."""
    name: str
    definition: 'TypeDefinitionBody'
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_type_definition(self)

class TypeDefinitionBody(ASTNode):
    """Base class for type definition bodies."""
    pass

@dataclass
class StructTypeDefinition(TypeDefinitionBody):
    """Struct-like type definition."""
    fields: List['TypeField']
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_struct_type_definition(self)

@dataclass
class TypeField:
    """Field in struct type definition."""
    name: str
    type_annotation: TypeExpression
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_type_field(self)

@dataclass
class VariantTypeDefinition(TypeDefinitionBody):
    """Variant/ADT type definition."""
    variants: List['TypeVariant']
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_variant_type_definition(self)

@dataclass
class TypeVariant:
    """Individual variant in variant type."""
    name: str
    fields: Optional[List[TypeField]] = None
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_type_variant(self)

# Display/Output Statements
@dataclass
class DisplayStatement(Statement):
    """Display statement for output."""
    expressions: List[Expression]
    message: Optional[str] = None  # For 'with message' syntax
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_display_statement(self)

# Async/Await
@dataclass
class AwaitExpression(Expression):
    """Await expression for async operations."""
    expression: Expression
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_await_expression(self)

# Program Structure
@dataclass
class Program(ASTNode):
    """Root node representing entire program."""
    statements: List[Statement]
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_program(self)

# Visitor Pattern Interface
class ASTVisitor(ABC):
    """Abstract visitor for AST traversal."""
    
    @abstractmethod
    def visit_program(self, node: Program) -> Any: pass
    
    @abstractmethod
    def visit_identifier(self, node: Identifier) -> Any: pass
    
    @abstractmethod
    def visit_string_literal(self, node: StringLiteral) -> Any: pass
    
    @abstractmethod
    def visit_integer_literal(self, node: IntegerLiteral) -> Any: pass
    
    @abstractmethod
    def visit_float_literal(self, node: FloatLiteral) -> Any: pass
    
    @abstractmethod
    def visit_boolean_literal(self, node: BooleanLiteral) -> Any: pass
    
    @abstractmethod
    def visit_none_literal(self, node: NoneLiteral) -> Any: pass
    
    @abstractmethod
    def visit_binary_operation(self, node: BinaryOperation) -> Any: pass
    
    @abstractmethod
    def visit_unary_operation(self, node: UnaryOperation) -> Any: pass
    
    @abstractmethod
    def visit_function_call(self, node: FunctionCall) -> Any: pass
    
    @abstractmethod
    def visit_list_expression(self, node: ListExpression) -> Any: pass
    
    @abstractmethod
    def visit_dictionary_expression(self, node: DictionaryExpression) -> Any: pass
    
    @abstractmethod
    def visit_variable_declaration(self, node: VariableDeclaration) -> Any: pass
    
    @abstractmethod
    def visit_function_definition(self, node: FunctionDefinition) -> Any: pass
    
    @abstractmethod
    def visit_return_statement(self, node: ReturnStatement) -> Any: pass
    
    @abstractmethod
    def visit_if_statement(self, node: IfStatement) -> Any: pass
    
    @abstractmethod
    def visit_for_statement(self, node: ForStatement) -> Any: pass
    
    @abstractmethod
    def visit_while_statement(self, node: WhileStatement) -> Any: pass
    
    @abstractmethod
    def visit_match_statement(self, node: MatchStatement) -> Any: pass
    
    @abstractmethod
    def visit_display_statement(self, node: DisplayStatement) -> Any: pass
    
    @abstractmethod
    def visit_type_definition(self, node: TypeDefinition) -> Any: pass
    
    # Additional visit methods for completeness
    def visit_literal(self, node: Literal) -> Any:
        """Generic literal visitor."""
        return None
    
    def visit_argument(self, node: Argument) -> Any:
        """Visit function argument."""
        return None
    
    def visit_dictionary_pair(self, node: DictionaryPair) -> Any:
        """Visit dictionary key-value pair."""
        return None
    
    def visit_match_case(self, node: MatchCase) -> Any:
        """Visit match case."""
        return None
    
    def visit_literal_pattern(self, node: LiteralPattern) -> Any:
        """Visit literal pattern."""
        return None
    
    def visit_identifier_pattern(self, node: IdentifierPattern) -> Any:
        """Visit identifier pattern."""
        return None
    
    def visit_wildcard_pattern(self, node: WildcardPattern) -> Any:
        """Visit wildcard pattern."""
        return None
    
    def visit_constructor_pattern(self, node: ConstructorPattern) -> Any:
        """Visit constructor pattern."""
        return None
    
    def visit_list_pattern(self, node: ListPattern) -> Any:
        """Visit list pattern."""
        return None
    
    def visit_simple_type(self, node: SimpleType) -> Any:
        """Visit simple type."""
        return None
    
    def visit_generic_type(self, node: GenericType) -> Any:
        """Visit generic type."""
        return None
    
    def visit_union_type(self, node: UnionType) -> Any:
        """Visit union type."""
        return None
    
    def visit_function_type(self, node: FunctionType) -> Any:
        """Visit function type."""
        return None
    
    def visit_struct_type_definition(self, node: StructTypeDefinition) -> Any:
        """Visit struct type definition."""
        return None
    
    def visit_type_field(self, node: TypeField) -> Any:
        """Visit type field."""
        return None
    
    def visit_variant_type_definition(self, node: VariantTypeDefinition) -> Any:
        """Visit variant type definition."""
        return None
    
    def visit_type_variant(self, node: TypeVariant) -> Any:
        """Visit type variant."""
        return None
    
    def visit_await_expression(self, node: AwaitExpression) -> Any:
        """Visit await expression."""
        return None

# Export all AST node types
__all__ = [
    'ASTNode', 'Expression', 'Statement', 'Program',
    'Identifier', 'Literal', 'StringLiteral', 'IntegerLiteral', 'FloatLiteral',
    'BooleanLiteral', 'NoneLiteral', 'BinaryOperation', 'UnaryOperation',
    'FunctionCall', 'Argument', 'ListExpression', 'DictionaryExpression',
    'DictionaryPair', 'VariableDeclaration', 'FunctionDefinition', 'Parameter',
    'ReturnStatement', 'IfStatement', 'ForStatement', 'WhileStatement',
    'MatchStatement', 'MatchCase', 'Pattern', 'LiteralPattern', 'IdentifierPattern',
    'WildcardPattern', 'ConstructorPattern', 'ListPattern', 'TypeExpression',
    'SimpleType', 'GenericType', 'UnionType', 'FunctionType', 'TypeDefinition',
    'StructTypeDefinition', 'TypeField', 'VariantTypeDefinition', 'TypeVariant',
    'DisplayStatement', 'AwaitExpression', 'ASTVisitor', 'BinaryOperator'
]
