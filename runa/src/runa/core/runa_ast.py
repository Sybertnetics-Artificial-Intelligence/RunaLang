"""
Runa Abstract Syntax Tree - The Central Hub

This is THE central AST definition for all language translations in the hub-and-spoke system.
All languages (Python, JavaScript, C#, etc.) translate to/from this universal Runa AST.

Key Features:
- Universal node identification with UUIDs
- Source location tracking for debugging
- Metadata support for translation context
- Language-agnostic representation
- Verification and comparison support
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Any, Union, Dict, Set
from enum import Enum, auto
import uuid
from datetime import datetime

# === CORE INFRASTRUCTURE ===

@dataclass
class SourceLocation:
    """Source code location for debugging and error reporting."""
    file_path: str = ""
    line: int = 0
    column: int = 0
    end_line: int = 0
    end_column: int = 0
    
    def __str__(self) -> str:
        if self.end_line and self.end_line != self.line:
            return f"{self.file_path}:{self.line}:{self.column}-{self.end_line}:{self.end_column}"
        elif self.end_column and self.end_column != self.column:
            return f"{self.file_path}:{self.line}:{self.column}-{self.end_column}"
        return f"{self.file_path}:{self.line}:{self.column}"

@dataclass
class TranslationMetadata:
    """Metadata for tracking translation context and history."""
    source_language: str = ""  # Original language (e.g., "python", "javascript")
    target_language: str = ""  # Target language (empty for Runa)
    translation_time: datetime = field(default_factory=datetime.now)
    translator_version: str = "0.3.0"
    confidence_score: float = 1.0  # 0.0-1.0 confidence in translation accuracy
    notes: Dict[str, Any] = field(default_factory=dict)
    
    def add_note(self, key: str, value: Any):
        """Add a translation note."""
        self.notes[key] = value

# Base classes
@dataclass
class ASTNode(ABC):
    """
    Base class for all Runa AST nodes.
    
    This is the foundation of the hub-and-spoke system. Every node has:
    - Unique identification for tracking through translation pipeline
    - Source location for debugging
    - Translation metadata for context
    - Support for verification and comparison
    """
    
    # Universal node identification
    node_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    # Source location tracking
    location: Optional[SourceLocation] = field(default_factory=SourceLocation)
    
    # Translation metadata
    metadata: TranslationMetadata = field(default_factory=TranslationMetadata)
    
    # Parent node reference (set during tree construction)
    parent: Optional['ASTNode'] = field(default=None, init=False, repr=False)
    
    # Child nodes (automatically populated by subclasses)
    _children: Set['ASTNode'] = field(default_factory=set, init=False, repr=False)
    
    def __post_init__(self):
        """Post-initialization setup for parent-child relationships."""
        self._establish_parent_child_relationships()
    
    def _establish_parent_child_relationships(self):
        """Establish parent-child relationships for tree navigation."""
        for field_name, field_value in self.__dict__.items():
            if isinstance(field_value, ASTNode):
                field_value.parent = self
                self._children.add(field_value)
            elif isinstance(field_value, (list, tuple)):
                for item in field_value:
                    if isinstance(item, ASTNode):
                        item.parent = self
                        self._children.add(item)
    
    @abstractmethod
    def accept(self, visitor):
        """Accept a visitor for AST traversal."""
        pass
    
    def get_children(self) -> List['ASTNode']:
        """Get all child nodes."""
        return list(self._children)
    
    def get_descendants(self) -> List['ASTNode']:
        """Get all descendant nodes (children, grandchildren, etc.)."""
        descendants = []
        for child in self._children:
            descendants.append(child)
            descendants.extend(child.get_descendants())
        return descendants
    
    def find_nodes_by_type(self, node_type: type) -> List['ASTNode']:
        """Find all descendant nodes of a specific type."""
        return [node for node in self.get_descendants() if isinstance(node, node_type)]
    
    def find_node_by_id(self, node_id: str) -> Optional['ASTNode']:
        """Find a descendant node by its ID."""
        if self.node_id == node_id:
            return self
        for child in self._children:
            result = child.find_node_by_id(node_id)
            if result:
                return result
        return None
    
    def clone(self) -> 'ASTNode':
        """Create a deep copy of this node with new IDs."""
        # This will be implemented by subclasses as needed
        raise NotImplementedError(f"Clone not implemented for {type(self).__name__}")
    
    def get_path_to_root(self) -> List['ASTNode']:
        """Get the path from this node to the root."""
        path = [self]
        current = self.parent
        while current:
            path.append(current)
            current = current.parent
        return path
    
    def get_common_ancestor(self, other: 'ASTNode') -> Optional['ASTNode']:
        """Find the lowest common ancestor with another node."""
        self_path = set(self.get_path_to_root())
        other_path = other.get_path_to_root()
        
        for node in other_path:
            if node in self_path:
                return node
        return None

class Statement(ASTNode):
    """Base class for all statement nodes."""
    pass

class Expression(ASTNode):
    """Base class for all expression nodes."""
    pass

class Declaration(Statement):
    """Base class for all declaration nodes."""
    pass

# Type system nodes
@dataclass
class TypeExpression(ASTNode):
    """Base class for type expressions."""
    pass

@dataclass
class BasicType(TypeExpression):
    """Basic type like Integer, String, Boolean."""
    name: str = ""
    def accept(self, visitor):
        return visitor.visit_basic_type(self)

@dataclass
class GenericType(TypeExpression):
    """Generic type like List[Integer] or Dictionary[String, Integer]."""
    base_type: str = ""
    type_args: List[TypeExpression] = field(default_factory=list)
    def accept(self, visitor):
        return visitor.visit_generic_type(self)

@dataclass
class UnionType(TypeExpression):
    """Union type like Integer OR String."""
    types: List[TypeExpression] = field(default_factory=list)
    def accept(self, visitor):
        return visitor.visit_union_type(self)

@dataclass
class IntersectionType(TypeExpression):
    """Intersection type like Serializable AND Validatable."""
    types: List[TypeExpression] = field(default_factory=list)
    def accept(self, visitor):
        return visitor.visit_intersection_type(self)

@dataclass
class OptionalType(TypeExpression):
    """Optional type like Optional[String]."""
    inner_type: Optional[TypeExpression] = None
    def accept(self, visitor):
        return visitor.visit_optional_type(self)

@dataclass
class FunctionType(TypeExpression):
    """Function type like Function[List[Integer], Integer]."""
    param_types: List[TypeExpression] = field(default_factory=list)
    return_type: Optional[TypeExpression] = None
    def accept(self, visitor):
        return visitor.visit_function_type(self)

# Literal nodes
@dataclass
class IntegerLiteral(Expression):
    """Integer literal like 42."""
    value: int = 0
    def accept(self, visitor):
        return visitor.visit_integer_literal(self)

@dataclass
class FloatLiteral(Expression):
    """Float literal like 3.14."""
    value: float = 0.0
    def accept(self, visitor):
        return visitor.visit_float_literal(self)

@dataclass
class StringLiteral(Expression):
    """String literal like "Hello, World!"."""
    value: str = ""
    def accept(self, visitor):
        return visitor.visit_string_literal(self)

@dataclass
class BooleanLiteral(Expression):
    """Boolean literal like true or false."""
    value: bool = False
    def accept(self, visitor):
        return visitor.visit_boolean_literal(self)

@dataclass
class ListLiteral(Expression):
    """List literal like list containing 1, 2, 3."""
    elements: List[Expression] = field(default_factory=list)
    def accept(self, visitor):
        return visitor.visit_list_literal(self)

@dataclass
class DictionaryLiteral(Expression):
    """Dictionary literal."""
    pairs: List[tuple[Expression, Expression]] = field(default_factory=list)
    def accept(self, visitor):
        return visitor.visit_dictionary_literal(self)

# Variable and identifier nodes
@dataclass
class Identifier(Expression):
    """Variable identifier like user_name."""
    name: str = ""
    def accept(self, visitor):
        return visitor.visit_identifier(self)

@dataclass
class MemberAccess(Expression):
    """Member access like user.name."""
    object: Optional[Expression] = None
    member: str = ""
    def accept(self, visitor):
        return visitor.visit_member_access(self)

@dataclass
class IndexAccess(Expression):
    """Index access like items[0]."""
    object: Optional[Expression] = None
    index: Optional[Expression] = None
    def accept(self, visitor):
        return visitor.visit_index_access(self)

# Binary and unary expressions
class BinaryOperator(Enum):
    """Binary operators in natural language form."""
    PLUS = "plus"
    MINUS = "minus"
    MULTIPLY = "multiplied by"
    DIVIDE = "divided by"
    MODULO = "modulo"
    POWER = "to the power of"
    EQUALS = "is equal to"
    NOT_EQUALS = "is not equal to"
    GREATER_THAN = "is greater than"
    LESS_THAN = "is less than"
    GREATER_EQUAL = "is greater than or equal to"
    LESS_EQUAL = "is less than or equal to"
    AND = "and"
    OR = "or"
    FOLLOWED_BY = "followed by"

@dataclass
class BinaryExpression(Expression):
    """Binary expression like x is greater than y."""
    left: Optional[Expression] = None
    operator: Optional[BinaryOperator] = None
    right: Optional[Expression] = None
    def accept(self, visitor):
        return visitor.visit_binary_expression(self)

@dataclass
class UnaryExpression(Expression):
    """Unary expression like not condition."""
    operator: str = ""
    operand: Optional[Expression] = None
    def accept(self, visitor):
        return visitor.visit_unary_expression(self)

# Function call
@dataclass
class FunctionCall(Expression):
    """Function call like Calculate Total Price with items as cart."""
    function_name: str = ""
    arguments: List[tuple[str, Expression]]  # List of (param_name, value) pairs = field(default_factory=list)
    def accept(self, visitor):
        return visitor.visit_function_call(self)

# Variable declarations
@dataclass
class LetStatement(Declaration):
    """Let statement like Let user name be "Alex"."""
    identifier: str = ""
    type_annotation: Optional[TypeExpression] = None
    value: Expression = None
    def accept(self, visitor):
        return visitor.visit_let_statement(self)

@dataclass
class DefineStatement(Declaration):
    """Define statement like Define constant PI as 3.14159."""
    identifier: str = ""
    type_annotation: Optional[TypeExpression] = None
    value: Expression = None
    is_constant: bool = False
    def accept(self, visitor):
        return visitor.visit_define_statement(self)

@dataclass
class SetStatement(Statement):
    """Set statement like Set user age to 28."""
    target: Optional[Expression] = None  # Can be identifier, member access, or index access
    value: Expression = None
    def accept(self, visitor):
        return visitor.visit_set_statement(self)

# Control flow statements
@dataclass
class IfStatement(Statement):
    """If statement with optional else if and else clauses."""
    condition: Expression = None
    then_block: List[Statement] = field(default_factory=list)
    elif_clauses: List[tuple[Expression, List[Statement]]] = field(default_factory=list)
    else_block: Optional[List[Statement]] = None
    def accept(self, visitor):
        return visitor.visit_if_statement(self)

@dataclass
class UnlessStatement(Statement):
    """Unless statement like Unless condition: block."""
    condition: Expression = None
    block: List[Statement] = field(default_factory=list)
    def accept(self, visitor):
        return visitor.visit_unless_statement(self)

@dataclass
class WhenStatement(Statement):
    """When statement like When condition: block."""
    condition: Expression = None
    block: List[Statement] = field(default_factory=list)
    def accept(self, visitor):
        return visitor.visit_when_statement(self)

# Pattern matching
@dataclass
class Pattern(ASTNode):
    """Base class for pattern matching patterns."""
    pass

@dataclass
class LiteralPattern(Pattern):
    """Literal pattern like 42 or "hello"."""
    value: Expression = None
    def accept(self, visitor):
        return visitor.visit_literal_pattern(self)

@dataclass
class IdentifierPattern(Pattern):
    """Identifier pattern like x."""
    name: str
    
    def accept(self, visitor):
        return visitor.visit_identifier_pattern(self)

@dataclass
class WildcardPattern(Pattern):
    """Wildcard pattern like _."""
    
    def accept(self, visitor):
        return visitor.visit_wildcard_pattern(self)

@dataclass
class ListPattern(Pattern):
    """List pattern like [head, tail...]."""
    elements: List[Pattern]
    rest: Optional[str] = None  # Variable name for rest elements
    
    def accept(self, visitor):
        return visitor.visit_list_pattern(self)

@dataclass
class MatchCase:
    """A single case in a match statement."""
    pattern: Pattern
    guard: Optional[Expression]
    block: List[Statement]

@dataclass
class MatchStatement(Statement):
    """Match statement for pattern matching."""
    value: Expression = None
    cases: List[MatchCase] = field(default_factory=list)
    def accept(self, visitor):
        return visitor.visit_match_statement(self)

# Loop statements
@dataclass
class ForEachLoop(Statement):
    """For each loop like For each item in collection: block."""
    variable: str = ""
    iterable: Expression = None
    block: List[Statement] = field(default_factory=list)
    def accept(self, visitor):
        return visitor.visit_for_each_loop(self)

@dataclass
class ForRangeLoop(Statement):
    """For range loop like For i from 1 to 10: block."""
    variable: str = ""
    start: Expression = None
    end: Expression = None
    step: Optional[Expression] = None
    block: List[Statement] = field(default_factory=list)
    def accept(self, visitor):
        return visitor.visit_for_range_loop(self)

@dataclass
class WhileLoop(Statement):
    """While loop like While condition: block."""
    condition: Expression = None
    block: List[Statement] = field(default_factory=list)
    def accept(self, visitor):
        return visitor.visit_while_loop(self)

@dataclass
class DoWhileLoop(Statement):
    """Do-while loop like Do: block While condition."""
    block: List[Statement] = field(default_factory=list)
    condition: Expression = None
    def accept(self, visitor):
        return visitor.visit_do_while_loop(self)

@dataclass
class RepeatLoop(Statement):
    """Repeat loop like Repeat 5 times: block."""
    count: Expression = None
    block: List[Statement] = field(default_factory=list)
    def accept(self, visitor):
        return visitor.visit_repeat_loop(self)

# Function/Process definition
@dataclass
class Parameter:
    """Function parameter with optional type annotation."""
    name: str
    type_annotation: Optional[TypeExpression] = None

@dataclass
class ProcessDefinition(Declaration):
    """Process definition like Process called "name" that takes params: block."""
    name: str = ""
    parameters: List[Parameter] = field(default_factory=list)
    return_type: Optional[TypeExpression] = None
    body: List[Statement] = field(default_factory=list)
    def accept(self, visitor):
        return visitor.visit_process_definition(self)

# Control flow statements
@dataclass
class ReturnStatement(Statement):
    """Return statement like Return value."""
    value: Optional[Expression] = None
    def accept(self, visitor):
        return visitor.visit_return_statement(self)

@dataclass
class BreakStatement(Statement):
    """Break statement."""
    def accept(self, visitor):
        return visitor.visit_break_statement(self)

@dataclass
class ContinueStatement(Statement):
    """Continue statement."""
    def accept(self, visitor):
        return visitor.visit_continue_statement(self)

# Error handling statements
@dataclass
class CatchClause:
    """A catch clause in a try statement."""
    exception_type: Optional[TypeExpression]
    exception_name: Optional[str] 
    block: List[Statement]

@dataclass
class TryStatement(Statement):
    """Try statement for error handling."""
    try_block: List[Statement] = field(default_factory=list)
    catch_clauses: List[CatchClause] = field(default_factory=list)
    finally_block: Optional[List[Statement]] = None
    def accept(self, visitor):
        return visitor.visit_try_statement(self)

@dataclass
class ThrowStatement(Statement):
    """Throw statement to raise exceptions."""
    exception: Expression = None
    def accept(self, visitor):
        return visitor.visit_throw_statement(self)

# I/O statements
@dataclass
class DisplayStatement(Statement):
    """Display statement like Display "Hello" or Display message with "prefix"."""
    value: Expression = None
    prefix: Optional[Expression] = None
    def accept(self, visitor):
        return visitor.visit_display_statement(self)

# Type definitions
@dataclass
class TypeDefinition(Declaration):
    """Type definition like Type Person is Dictionary with: fields."""
    name: str = ""
    definition: TypeExpression = None
    def accept(self, visitor):
        return visitor.visit_type_definition(self)

# Program root
@dataclass
class Program(ASTNode):
    """Root node representing the entire program."""
    statements: List[Statement] = field(default_factory=list)
    def accept(self, visitor):
        return visitor.visit_program(self)

# Expression statement
@dataclass
class ExpressionStatement(Statement):
    """Statement that consists of a single expression."""
    expression: Expression = None
    def accept(self, visitor):
        return visitor.visit_expression_statement(self)

# Block statement
@dataclass
class Block(Statement):
    """Block of statements."""
    statements: List[Statement] = field(default_factory=list)
    def accept(self, visitor):
        return visitor.visit_block(self)

# Module system
@dataclass
class ImportStatement(Statement):
    """Import statement like Import "math" as math_module or Import "utils" exposing calculate, format."""
    module_path: str = ""
    alias: Optional[str] = None
    imported_names: Optional[List[str]] = None  # For selective imports
    def accept(self, visitor):
        return visitor.visit_import_statement(self)

@dataclass
class ExportStatement(Statement):
    """Export statement like Export calculate, format or Export all."""
    exported_names: Optional[List[str]] = None  # None means export all
    def accept(self, visitor):
        return visitor.visit_export_statement(self)

@dataclass
class ModuleDeclaration(Statement):
    """Module declaration like Module "utils" with: body."""
    name: str = ""
    body: List[Statement] = field(default_factory=list)
    def accept(self, visitor):
        return visitor.visit_module_declaration(self)

# Async/await and concurrency
@dataclass
class AwaitExpression(Expression):
    """Await expression like Await some_future."""
    expression: Expression = None
    def accept(self, visitor):
        return visitor.visit_await_expression(self)

@dataclass
class AsyncProcessDefinition(Declaration):
    """Async process definition like Async Process called "name": body."""
    name: str = ""
    parameters: List[Parameter] = field(default_factory=list)
    return_type: Optional[TypeExpression] = None
    body: List[Statement] = field(default_factory=list)
    def accept(self, visitor):
        return visitor.visit_async_process_definition(self)

@dataclass
class SendStatement(Statement):
    """Send statement for actor-like concurrency: Send message to actor."""
    message: Expression = None
    target: Expression = None
    def accept(self, visitor):
        return visitor.visit_send_statement(self)

@dataclass
class AtomicBlock(Statement):
    """Atomic block for thread-safe operations: Atomic: body."""
    body: List[Statement] = field(default_factory=list)
    def accept(self, visitor):
        return visitor.visit_atomic_block(self)

@dataclass
class LockStatement(Statement):
    """Lock statement: Lock resource: body."""
    resource: Expression = None
    body: List[Statement] = field(default_factory=list)
    def accept(self, visitor):
        return visitor.visit_lock_statement(self)

# Memory management annotations
@dataclass
class MemoryAnnotation:
    """Base class for memory annotations."""
    annotation_type: str
    
@dataclass
class OwnershipAnnotation(MemoryAnnotation):
    """Ownership annotation like @owned, @borrowed, @shared."""
    def __init__(self, annotation_type: str):
        super().__init__(annotation_type)

@dataclass
class LifetimeAnnotation(MemoryAnnotation):
    """Lifetime annotation like @lifetime('a)."""
    lifetime_name: str
    
    def __init__(self, lifetime_name: str):
        super().__init__("lifetime")
        self.lifetime_name = lifetime_name

@dataclass
class DeleteStatement(Statement):
    """Delete statement for explicit memory management: Delete resource."""
    target: Expression = None
    def accept(self, visitor):
        return visitor.visit_delete_statement(self)

@dataclass
class AnnotatedVariableDeclaration(Declaration):
    """Variable declaration with memory annotations."""
    base_declaration: Union[LetStatement, DefineStatement] = None
    memory_annotations: List[MemoryAnnotation] = field(default_factory=list)
    def accept(self, visitor):
        return visitor.visit_annotated_variable_declaration(self) 