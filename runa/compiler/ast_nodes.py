"""
Runa Abstract Syntax Tree Node Definitions

Defines all AST node types according to the Runa Formal Grammar Specifications.
Each node represents a syntactic construct in the Runa language.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Any, Union, Dict
from enum import Enum, auto

# Base classes
class ASTNode(ABC):
    """Base class for all AST nodes."""
    
    @abstractmethod
    def accept(self, visitor):
        """Accept a visitor for AST traversal."""
        pass

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
    name: str
    
    def accept(self, visitor):
        return visitor.visit_basic_type(self)

@dataclass
class GenericType(TypeExpression):
    """Generic type like List[Integer] or Dictionary[String, Integer]."""
    base_type: str
    type_args: List[TypeExpression]
    
    def accept(self, visitor):
        return visitor.visit_generic_type(self)

@dataclass
class UnionType(TypeExpression):
    """Union type like Integer OR String."""
    types: List[TypeExpression]
    
    def accept(self, visitor):
        return visitor.visit_union_type(self)

@dataclass
class IntersectionType(TypeExpression):
    """Intersection type like Serializable AND Validatable."""
    types: List[TypeExpression]
    
    def accept(self, visitor):
        return visitor.visit_intersection_type(self)

@dataclass
class OptionalType(TypeExpression):
    """Optional type like Optional[String]."""
    inner_type: TypeExpression
    
    def accept(self, visitor):
        return visitor.visit_optional_type(self)

@dataclass
class FunctionType(TypeExpression):
    """Function type like Function[List[Integer], Integer]."""
    param_types: List[TypeExpression]
    return_type: TypeExpression
    
    def accept(self, visitor):
        return visitor.visit_function_type(self)

# Literal nodes
@dataclass
class IntegerLiteral(Expression):
    """Integer literal like 42."""
    value: int
    
    def accept(self, visitor):
        return visitor.visit_integer_literal(self)

@dataclass
class FloatLiteral(Expression):
    """Float literal like 3.14."""
    value: float
    
    def accept(self, visitor):
        return visitor.visit_float_literal(self)

@dataclass
class StringLiteral(Expression):
    """String literal like "Hello, World!"."""
    value: str
    
    def accept(self, visitor):
        return visitor.visit_string_literal(self)

@dataclass
class BooleanLiteral(Expression):
    """Boolean literal like true or false."""
    value: bool
    
    def accept(self, visitor):
        return visitor.visit_boolean_literal(self)

@dataclass
class ListLiteral(Expression):
    """List literal like list containing 1, 2, 3."""
    elements: List[Expression]
    
    def accept(self, visitor):
        return visitor.visit_list_literal(self)

@dataclass
class DictionaryLiteral(Expression):
    """Dictionary literal."""
    pairs: List[tuple[Expression, Expression]]
    
    def accept(self, visitor):
        return visitor.visit_dictionary_literal(self)

# Variable and identifier nodes
@dataclass
class Identifier(Expression):
    """Variable identifier like user_name."""
    name: str
    
    def accept(self, visitor):
        return visitor.visit_identifier(self)

@dataclass
class MemberAccess(Expression):
    """Member access like user.name."""
    object: Expression
    member: str
    
    def accept(self, visitor):
        return visitor.visit_member_access(self)

@dataclass
class IndexAccess(Expression):
    """Index access like items[0]."""
    object: Expression
    index: Expression
    
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
    left: Expression
    operator: BinaryOperator
    right: Expression
    
    def accept(self, visitor):
        return visitor.visit_binary_expression(self)

@dataclass
class UnaryExpression(Expression):
    """Unary expression like not condition."""
    operator: str
    operand: Expression
    
    def accept(self, visitor):
        return visitor.visit_unary_expression(self)

# Function call
@dataclass
class FunctionCall(Expression):
    """Function call like Calculate Total Price with items as cart."""
    function_name: str
    arguments: List[tuple[str, Expression]]  # List of (param_name, value) pairs
    
    def accept(self, visitor):
        return visitor.visit_function_call(self)

# Variable declarations
@dataclass
class LetStatement(Declaration):
    """Let statement like Let user name be "Alex"."""
    identifier: str
    type_annotation: Optional[TypeExpression]
    value: Expression
    
    def accept(self, visitor):
        return visitor.visit_let_statement(self)

@dataclass
class DefineStatement(Declaration):
    """Define statement like Define constant PI as 3.14159."""
    identifier: str
    type_annotation: Optional[TypeExpression]
    value: Expression
    is_constant: bool = False
    
    def accept(self, visitor):
        return visitor.visit_define_statement(self)

@dataclass
class SetStatement(Statement):
    """Set statement like Set user age to 28."""
    target: Expression  # Can be identifier, member access, or index access
    value: Expression
    
    def accept(self, visitor):
        return visitor.visit_set_statement(self)

# Control flow statements
@dataclass
class IfStatement(Statement):
    """If statement with optional else if and else clauses."""
    condition: Expression
    then_block: List[Statement]
    elif_clauses: List[tuple[Expression, List[Statement]]] = field(default_factory=list)
    else_block: Optional[List[Statement]] = None
    
    def accept(self, visitor):
        return visitor.visit_if_statement(self)

@dataclass
class UnlessStatement(Statement):
    """Unless statement like Unless condition: block."""
    condition: Expression
    block: List[Statement]
    
    def accept(self, visitor):
        return visitor.visit_unless_statement(self)

@dataclass
class WhenStatement(Statement):
    """When statement like When condition: block."""
    condition: Expression
    block: List[Statement]
    
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
    value: Expression
    
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
    value: Expression
    cases: List[MatchCase]
    
    def accept(self, visitor):
        return visitor.visit_match_statement(self)

# Loop statements
@dataclass
class ForEachLoop(Statement):
    """For each loop like For each item in collection: block."""
    variable: str
    iterable: Expression
    block: List[Statement]
    
    def accept(self, visitor):
        return visitor.visit_for_each_loop(self)

@dataclass
class ForRangeLoop(Statement):
    """For range loop like For i from 1 to 10: block."""
    variable: str
    start: Expression
    end: Expression
    step: Optional[Expression]
    block: List[Statement]
    
    def accept(self, visitor):
        return visitor.visit_for_range_loop(self)

@dataclass
class WhileLoop(Statement):
    """While loop like While condition: block."""
    condition: Expression
    block: List[Statement]
    
    def accept(self, visitor):
        return visitor.visit_while_loop(self)

@dataclass
class DoWhileLoop(Statement):
    """Do-while loop like Do: block While condition."""
    block: List[Statement]
    condition: Expression
    
    def accept(self, visitor):
        return visitor.visit_do_while_loop(self)

@dataclass
class RepeatLoop(Statement):
    """Repeat loop like Repeat 5 times: block."""
    count: Expression
    block: List[Statement]
    
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
    name: str
    parameters: List[Parameter]
    return_type: Optional[TypeExpression]
    body: List[Statement]
    
    def accept(self, visitor):
        return visitor.visit_process_definition(self)

# Control flow statements
@dataclass
class ReturnStatement(Statement):
    """Return statement like Return value."""
    value: Optional[Expression]
    
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

# I/O statements
@dataclass
class DisplayStatement(Statement):
    """Display statement like Display "Hello" or Display message with "prefix"."""
    value: Expression
    prefix: Optional[Expression] = None
    
    def accept(self, visitor):
        return visitor.visit_display_statement(self)

# Type definitions
@dataclass
class TypeDefinition(Declaration):
    """Type definition like Type Person is Dictionary with: fields."""
    name: str
    definition: TypeExpression
    
    def accept(self, visitor):
        return visitor.visit_type_definition(self)

# Program root
@dataclass
class Program(ASTNode):
    """Root node representing the entire program."""
    statements: List[Statement]
    
    def accept(self, visitor):
        return visitor.visit_program(self)

# Expression statement
@dataclass
class ExpressionStatement(Statement):
    """Statement that consists of a single expression."""
    expression: Expression
    
    def accept(self, visitor):
        return visitor.visit_expression_statement(self)

# Block statement
@dataclass
class Block(Statement):
    """Block of statements."""
    statements: List[Statement]
    
    def accept(self, visitor):
        return visitor.visit_block(self) 