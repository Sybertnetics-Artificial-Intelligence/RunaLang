#!/usr/bin/env python3
"""
Move AST Module

Comprehensive Abstract Syntax Tree definitions for the Move programming language,
supporting resource-oriented programming, modules, scripts, abilities system, and 
Move's unique safety-first approach to digital asset management.

Move language features supported:
- Resource-oriented programming with first-class resources
- Abilities system (copy, drop, store, key)
- Modules and scripts organizational model
- Strong static typing with generics
- Move semantics and ownership
- Pattern matching and control flow
- Formal verification support
- Bytecode verification
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Optional, Any, Union, Dict, Set, Tuple
import uuid


class MoveAbility(Enum):
    """Move abilities that define what operations can be performed on a type."""
    COPY = "copy"       # Value can be copied
    DROP = "drop"       # Value can be dropped/discarded
    STORE = "store"     # Value can be stored in global storage
    KEY = "key"         # Value can be used as a key for global storage


class MoveVisibility(Enum):
    """Function and struct visibility modifiers."""
    PRIVATE = "private"
    PUBLIC = "public"
    PUBLIC_FRIEND = "public(friend)"
    PUBLIC_SCRIPT = "public(script)"
    PUBLIC_ENTRY = "public(entry)"


class MovePrimitiveType(Enum):
    """Move primitive types."""
    BOOL = "bool"
    U8 = "u8"
    U16 = "u16"
    U32 = "u32"
    U64 = "u64"
    U128 = "u128"
    U256 = "u256"
    ADDRESS = "address"
    SIGNER = "signer"
    VECTOR = "vector"


class MoveOperator(Enum):
    """Move operators."""
    # Arithmetic
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"
    MOD = "%"
    
    # Comparison
    EQ = "=="
    NE = "!="
    LT = "<"
    LE = "<="
    GT = ">"
    GE = ">="
    
    # Logical
    AND = "&&"
    OR = "||"
    NOT = "!"
    
    # Bitwise
    BITWISE_AND = "&"
    BITWISE_OR = "|"
    BITWISE_XOR = "^"
    BITWISE_NOT = "~"
    SHL = "<<"
    SHR = ">>"
    
    # Assignment
    ASSIGN = "="
    
    # Move-specific
    BORROW = "&"
    BORROW_MUT = "&mut"
    MOVE = "move"
    COPY = "copy"


class MoveNode(ABC):
    """Base class for all Move AST nodes."""
    
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.line_number: Optional[int] = None
        self.column_number: Optional[int] = None
        self.source_file: Optional[str] = None
    
    @abstractmethod
    def accept(self, visitor):
        """Accept a visitor for traversal."""
        pass


# Type Definitions

@dataclass
class MoveType(MoveNode):
    """Base class for Move types."""
    pass


@dataclass
class MovePrimitive(MoveType):
    """Primitive type in Move."""
    type_name: MovePrimitiveType
    
    def accept(self, visitor):
        return visitor.visit_primitive(self)


@dataclass
class MoveGenericType(MoveType):
    """Generic type parameter."""
    name: str
    constraints: List[MoveAbility] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_generic_type(self)


@dataclass
class MoveStructType(MoveType):
    """Reference to a struct type."""
    module_name: Optional[str]
    struct_name: str
    type_arguments: List[MoveType] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_struct_type(self)


@dataclass
class MoveVectorType(MoveType):
    """Vector type."""
    element_type: MoveType
    
    def accept(self, visitor):
        return visitor.visit_vector_type(self)


@dataclass
class MoveReferenceType(MoveType):
    """Reference type (&T or &mut T)."""
    referenced_type: MoveType
    is_mutable: bool = False
    
    def accept(self, visitor):
        return visitor.visit_reference_type(self)


@dataclass
class MoveTupleType(MoveType):
    """Tuple type."""
    element_types: List[MoveType]
    
    def accept(self, visitor):
        return visitor.visit_tuple_type(self)


@dataclass
class MoveFunctionType(MoveType):
    """Function type."""
    parameters: List[MoveType]
    return_type: Optional[MoveType]
    
    def accept(self, visitor):
        return visitor.visit_function_type(self)


# Expressions

@dataclass
class MoveExpression(MoveNode):
    """Base class for Move expressions."""
    expression_type: Optional[MoveType] = None


@dataclass
class MoveLiteral(MoveExpression):
    """Literal value."""
    value: Any
    literal_type: MovePrimitiveType
    
    def accept(self, visitor):
        return visitor.visit_literal(self)


@dataclass
class MoveIdentifier(MoveExpression):
    """Variable or function identifier."""
    name: str
    
    def accept(self, visitor):
        return visitor.visit_identifier(self)


@dataclass
class MoveBinaryOp(MoveExpression):
    """Binary operation."""
    left: MoveExpression
    operator: MoveOperator
    right: MoveExpression
    
    def accept(self, visitor):
        return visitor.visit_binary_op(self)


@dataclass
class MoveUnaryOp(MoveExpression):
    """Unary operation."""
    operator: MoveOperator
    operand: MoveExpression
    
    def accept(self, visitor):
        return visitor.visit_unary_op(self)


@dataclass
class MoveFunctionCall(MoveExpression):
    """Function call expression."""
    module_name: Optional[str]
    function_name: str
    type_arguments: List[MoveType] = field(default_factory=list)
    arguments: List[MoveExpression] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_function_call(self)


@dataclass
class MoveMethodCall(MoveExpression):
    """Method call on a value."""
    receiver: MoveExpression
    method_name: str
    type_arguments: List[MoveType] = field(default_factory=list)
    arguments: List[MoveExpression] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_method_call(self)


@dataclass
class MoveFieldAccess(MoveExpression):
    """Field access on a struct."""
    object: MoveExpression
    field_name: str
    
    def accept(self, visitor):
        return visitor.visit_field_access(self)


@dataclass
class MoveIndexAccess(MoveExpression):
    """Vector index access."""
    object: MoveExpression
    index: MoveExpression
    
    def accept(self, visitor):
        return visitor.visit_index_access(self)


@dataclass
class MoveStructConstruction(MoveExpression):
    """Struct construction expression."""
    struct_type: MoveStructType
    fields: List[Tuple[str, MoveExpression]]  # field_name, value
    
    def accept(self, visitor):
        return visitor.visit_struct_construction(self)


@dataclass
class MoveVectorConstruction(MoveExpression):
    """Vector construction expression."""
    element_type: MoveType
    elements: List[MoveExpression]
    
    def accept(self, visitor):
        return visitor.visit_vector_construction(self)


@dataclass
class MoveTupleConstruction(MoveExpression):
    """Tuple construction expression."""
    elements: List[MoveExpression]
    
    def accept(self, visitor):
        return visitor.visit_tuple_construction(self)


@dataclass
class MoveBorrow(MoveExpression):
    """Borrow expression (&expr or &mut expr)."""
    expression: MoveExpression
    is_mutable: bool = False
    
    def accept(self, visitor):
        return visitor.visit_borrow(self)


@dataclass
class MoveDereference(MoveExpression):
    """Dereference expression (*expr)."""
    expression: MoveExpression
    
    def accept(self, visitor):
        return visitor.visit_dereference(self)


@dataclass
class MoveCopy(MoveExpression):
    """Copy expression (copy expr)."""
    expression: MoveExpression
    
    def accept(self, visitor):
        return visitor.visit_copy(self)


@dataclass
class MoveMove(MoveExpression):
    """Move expression (move expr)."""
    expression: MoveExpression
    
    def accept(self, visitor):
        return visitor.visit_move(self)


@dataclass
class MoveConditional(MoveExpression):
    """Conditional expression (if condition then_expr else else_expr)."""
    condition: MoveExpression
    then_expr: MoveExpression
    else_expr: Optional[MoveExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_conditional(self)


@dataclass
class MoveBlock(MoveExpression):
    """Block expression."""
    statements: List['MoveStatement']
    return_expression: Optional[MoveExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_block(self)


@dataclass
class MovePattern(MoveNode):
    """Base class for patterns in pattern matching."""
    pass


@dataclass
class MoveIdentifierPattern(MovePattern):
    """Identifier pattern for binding."""
    name: str
    is_mutable: bool = False
    
    def accept(self, visitor):
        return visitor.visit_identifier_pattern(self)


@dataclass
class MoveStructPattern(MovePattern):
    """Struct destructuring pattern."""
    struct_type: MoveStructType
    field_patterns: List[Tuple[str, MovePattern]]  # field_name, pattern
    
    def accept(self, visitor):
        return visitor.visit_struct_pattern(self)


@dataclass
class MoveTuplePattern(MovePattern):
    """Tuple destructuring pattern."""
    element_patterns: List[MovePattern]
    
    def accept(self, visitor):
        return visitor.visit_tuple_pattern(self)


@dataclass
class MoveWildcardPattern(MovePattern):
    """Wildcard pattern (_)."""
    
    def accept(self, visitor):
        return visitor.visit_wildcard_pattern(self)


# Statements

@dataclass
class MoveStatement(MoveNode):
    """Base class for Move statements."""
    pass


@dataclass
class MoveExpressionStatement(MoveStatement):
    """Expression used as a statement."""
    expression: MoveExpression
    
    def accept(self, visitor):
        return visitor.visit_expression_statement(self)


@dataclass
class MoveVariableDeclaration(MoveStatement):
    """Variable declaration statement."""
    pattern: MovePattern
    type_annotation: Optional[MoveType] = None
    initializer: Optional[MoveExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_variable_declaration(self)


@dataclass
class MoveAssignment(MoveStatement):
    """Assignment statement."""
    target: MoveExpression
    value: MoveExpression
    
    def accept(self, visitor):
        return visitor.visit_assignment(self)


@dataclass
class MoveIfStatement(MoveStatement):
    """If statement."""
    condition: MoveExpression
    then_block: MoveBlock
    else_block: Optional[MoveBlock] = None
    
    def accept(self, visitor):
        return visitor.visit_if_statement(self)


@dataclass
class MoveWhileLoop(MoveStatement):
    """While loop statement."""
    condition: MoveExpression
    body: MoveBlock
    
    def accept(self, visitor):
        return visitor.visit_while_loop(self)


@dataclass
class MoveForLoop(MoveStatement):
    """For loop statement (for item in iterator)."""
    pattern: MovePattern
    iterator: MoveExpression
    body: MoveBlock
    
    def accept(self, visitor):
        return visitor.visit_for_loop(self)


@dataclass
class MoveBreak(MoveStatement):
    """Break statement."""
    
    def accept(self, visitor):
        return visitor.visit_break(self)


@dataclass
class MoveContinue(MoveStatement):
    """Continue statement."""
    
    def accept(self, visitor):
        return visitor.visit_continue(self)


@dataclass
class MoveReturn(MoveStatement):
    """Return statement."""
    value: Optional[MoveExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_return(self)


@dataclass
class MoveAbort(MoveStatement):
    """Abort statement."""
    code: MoveExpression
    
    def accept(self, visitor):
        return visitor.visit_abort(self)


# Declarations

@dataclass
class MoveDeclaration(MoveNode):
    """Base class for Move declarations."""
    pass


@dataclass
class MoveField(MoveNode):
    """Struct field definition."""
    name: str
    field_type: MoveType
    
    def accept(self, visitor):
        return visitor.visit_field(self)


@dataclass
class MoveStructDeclaration(MoveDeclaration):
    """Struct declaration."""
    name: str
    type_parameters: List[MoveGenericType] = field(default_factory=list)
    abilities: List[MoveAbility] = field(default_factory=list)
    fields: List[MoveField] = field(default_factory=list)
    is_native: bool = False
    
    def accept(self, visitor):
        return visitor.visit_struct_declaration(self)


@dataclass
class MoveParameter(MoveNode):
    """Function parameter."""
    name: str
    parameter_type: MoveType
    
    def accept(self, visitor):
        return visitor.visit_parameter(self)


@dataclass
class MoveFunctionDeclaration(MoveDeclaration):
    """Function declaration."""
    name: str
    visibility: MoveVisibility = MoveVisibility.PRIVATE
    type_parameters: List[MoveGenericType] = field(default_factory=list)
    parameters: List[MoveParameter] = field(default_factory=list)
    return_type: Optional[MoveType] = None
    acquires: List[MoveStructType] = field(default_factory=list)  # Resources this function acquires
    body: Optional[MoveBlock] = None
    is_native: bool = False
    is_entry: bool = False
    
    def accept(self, visitor):
        return visitor.visit_function_declaration(self)


@dataclass
class MoveUseDeclaration(MoveDeclaration):
    """Use/import declaration."""
    module_address: Optional[str]
    module_name: str
    import_name: Optional[str] = None  # Alias for the import
    imported_items: List[str] = field(default_factory=list)  # Specific items to import
    
    def accept(self, visitor):
        return visitor.visit_use_declaration(self)


@dataclass
class MoveFriendDeclaration(MoveDeclaration):
    """Friend declaration for access control."""
    module_address: str
    module_name: str
    
    def accept(self, visitor):
        return visitor.visit_friend_declaration(self)


@dataclass
class MoveConstantDeclaration(MoveDeclaration):
    """Constant declaration."""
    name: str
    constant_type: MoveType
    value: MoveExpression
    
    def accept(self, visitor):
        return visitor.visit_constant_declaration(self)


# Top-level constructs

@dataclass
class MoveModule(MoveNode):
    """Move module definition."""
    address: str
    name: str
    use_declarations: List[MoveUseDeclaration] = field(default_factory=list)
    friend_declarations: List[MoveFriendDeclaration] = field(default_factory=list)
    constants: List[MoveConstantDeclaration] = field(default_factory=list)
    structs: List[MoveStructDeclaration] = field(default_factory=list)
    functions: List[MoveFunctionDeclaration] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_module(self)


@dataclass
class MoveScript(MoveNode):
    """Move script definition."""
    use_declarations: List[MoveUseDeclaration] = field(default_factory=list)
    constants: List[MoveConstantDeclaration] = field(default_factory=list)
    main_function: MoveFunctionDeclaration
    
    def accept(self, visitor):
        return visitor.visit_script(self)


# Specification constructs (for formal verification)

@dataclass
class MoveCondition(MoveNode):
    """Base class for Move specifications."""
    kind: str  # "requires", "ensures", "aborts_if", etc.
    expression: MoveExpression
    
    def accept(self, visitor):
        return visitor.visit_condition(self)


@dataclass
class MoveSpecification(MoveNode):
    """Function or module specification."""
    target: str  # Function or module name
    conditions: List[MoveCondition] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_specification(self)


# Program root

@dataclass
class MoveProgram(MoveNode):
    """Root node representing a complete Move program."""
    modules: List[MoveModule] = field(default_factory=list)
    scripts: List[MoveScript] = field(default_factory=list)
    specifications: List[MoveSpecification] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_program(self)


# Visitor interface

class MoveVisitor(ABC):
    """Abstract visitor for Move AST traversal."""
    
    @abstractmethod
    def visit_program(self, node: MoveProgram): pass
    
    @abstractmethod
    def visit_module(self, node: MoveModule): pass
    
    @abstractmethod
    def visit_script(self, node: MoveScript): pass
    
    @abstractmethod
    def visit_struct_declaration(self, node: MoveStructDeclaration): pass
    
    @abstractmethod
    def visit_function_declaration(self, node: MoveFunctionDeclaration): pass
    
    @abstractmethod
    def visit_use_declaration(self, node: MoveUseDeclaration): pass
    
    @abstractmethod
    def visit_friend_declaration(self, node: MoveFriendDeclaration): pass
    
    @abstractmethod
    def visit_constant_declaration(self, node: MoveConstantDeclaration): pass
    
    @abstractmethod
    def visit_field(self, node: MoveField): pass
    
    @abstractmethod
    def visit_parameter(self, node: MoveParameter): pass
    
    # Type visitors
    @abstractmethod
    def visit_primitive(self, node: MovePrimitive): pass
    
    @abstractmethod
    def visit_generic_type(self, node: MoveGenericType): pass
    
    @abstractmethod
    def visit_struct_type(self, node: MoveStructType): pass
    
    @abstractmethod
    def visit_vector_type(self, node: MoveVectorType): pass
    
    @abstractmethod
    def visit_reference_type(self, node: MoveReferenceType): pass
    
    @abstractmethod
    def visit_tuple_type(self, node: MoveTupleType): pass
    
    @abstractmethod
    def visit_function_type(self, node: MoveFunctionType): pass
    
    # Expression visitors
    @abstractmethod
    def visit_literal(self, node: MoveLiteral): pass
    
    @abstractmethod
    def visit_identifier(self, node: MoveIdentifier): pass
    
    @abstractmethod
    def visit_binary_op(self, node: MoveBinaryOp): pass
    
    @abstractmethod
    def visit_unary_op(self, node: MoveUnaryOp): pass
    
    @abstractmethod
    def visit_function_call(self, node: MoveFunctionCall): pass
    
    @abstractmethod
    def visit_method_call(self, node: MoveMethodCall): pass
    
    @abstractmethod
    def visit_field_access(self, node: MoveFieldAccess): pass
    
    @abstractmethod
    def visit_index_access(self, node: MoveIndexAccess): pass
    
    @abstractmethod
    def visit_struct_construction(self, node: MoveStructConstruction): pass
    
    @abstractmethod
    def visit_vector_construction(self, node: MoveVectorConstruction): pass
    
    @abstractmethod
    def visit_tuple_construction(self, node: MoveTupleConstruction): pass
    
    @abstractmethod
    def visit_borrow(self, node: MoveBorrow): pass
    
    @abstractmethod
    def visit_dereference(self, node: MoveDereference): pass
    
    @abstractmethod
    def visit_copy(self, node: MoveCopy): pass
    
    @abstractmethod
    def visit_move(self, node: MoveMove): pass
    
    @abstractmethod
    def visit_conditional(self, node: MoveConditional): pass
    
    @abstractmethod
    def visit_block(self, node: MoveBlock): pass
    
    # Pattern visitors
    @abstractmethod
    def visit_identifier_pattern(self, node: MoveIdentifierPattern): pass
    
    @abstractmethod
    def visit_struct_pattern(self, node: MoveStructPattern): pass
    
    @abstractmethod
    def visit_tuple_pattern(self, node: MoveTuplePattern): pass
    
    @abstractmethod
    def visit_wildcard_pattern(self, node: MoveWildcardPattern): pass
    
    # Statement visitors
    @abstractmethod
    def visit_expression_statement(self, node: MoveExpressionStatement): pass
    
    @abstractmethod
    def visit_variable_declaration(self, node: MoveVariableDeclaration): pass
    
    @abstractmethod
    def visit_assignment(self, node: MoveAssignment): pass
    
    @abstractmethod
    def visit_if_statement(self, node: MoveIfStatement): pass
    
    @abstractmethod
    def visit_while_loop(self, node: MoveWhileLoop): pass
    
    @abstractmethod
    def visit_for_loop(self, node: MoveForLoop): pass
    
    @abstractmethod
    def visit_break(self, node: MoveBreak): pass
    
    @abstractmethod
    def visit_continue(self, node: MoveContinue): pass
    
    @abstractmethod
    def visit_return(self, node: MoveReturn): pass
    
    @abstractmethod
    def visit_abort(self, node: MoveAbort): pass
    
    # Specification visitors
    @abstractmethod
    def visit_condition(self, node: MoveCondition): pass
    
    @abstractmethod
    def visit_specification(self, node: MoveSpecification): pass


# Utility functions for AST construction

def create_move_module(address: str, name: str, **kwargs) -> MoveModule:
    """Create a Move module with default empty collections."""
    return MoveModule(address=address, name=name, **kwargs)


def create_move_function(name: str, visibility: MoveVisibility = MoveVisibility.PRIVATE, **kwargs) -> MoveFunctionDeclaration:
    """Create a Move function declaration with defaults."""
    return MoveFunctionDeclaration(name=name, visibility=visibility, **kwargs)


def create_move_struct(name: str, abilities: List[MoveAbility] = None, **kwargs) -> MoveStructDeclaration:
    """Create a Move struct declaration with defaults."""
    if abilities is None:
        abilities = []
    return MoveStructDeclaration(name=name, abilities=abilities, **kwargs)


def create_primitive_type(type_name: MovePrimitiveType) -> MovePrimitive:
    """Create a primitive type."""
    return MovePrimitive(type_name=type_name)


def create_struct_type(struct_name: str, module_name: str = None, type_arguments: List[MoveType] = None) -> MoveStructType:
    """Create a struct type reference."""
    if type_arguments is None:
        type_arguments = []
    return MoveStructType(module_name=module_name, struct_name=struct_name, type_arguments=type_arguments)


# Type aliases for commonly used types
MoveNode = Union[
    MoveProgram, MoveModule, MoveScript,
    MoveStructDeclaration, MoveFunctionDeclaration, MoveUseDeclaration, MoveFriendDeclaration, MoveConstantDeclaration,
    MoveField, MoveParameter,
    MoveType, MovePrimitive, MoveGenericType, MoveStructType, MoveVectorType, MoveReferenceType, MoveTupleType, MoveFunctionType,
    MoveExpression, MoveLiteral, MoveIdentifier, MoveBinaryOp, MoveUnaryOp, MoveFunctionCall, MoveMethodCall,
    MoveFieldAccess, MoveIndexAccess, MoveStructConstruction, MoveVectorConstruction, MoveTupleConstruction,
    MoveBorrow, MoveDereference, MoveCopy, MoveMove, MoveConditional, MoveBlock,
    MovePattern, MoveIdentifierPattern, MoveStructPattern, MoveTuplePattern, MoveWildcardPattern,
    MoveStatement, MoveExpressionStatement, MoveVariableDeclaration, MoveAssignment, MoveIfStatement,
    MoveWhileLoop, MoveForLoop, MoveBreak, MoveContinue, MoveReturn, MoveAbort,
    MoveCondition, MoveSpecification
] 