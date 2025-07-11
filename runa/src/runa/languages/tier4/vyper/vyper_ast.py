#!/usr/bin/env python3
"""
Vyper AST Node Definitions

Comprehensive Abstract Syntax Tree nodes for Vyper language covering all Vyper features
including smart contracts with Python-like syntax, functions with security decorators,
events, interfaces, and blockchain-specific programming constructs.

This module provides complete AST representation for:
- Smart contracts with Python-like syntax
- Functions with @external, @internal, @pure, @view decorators
- Events and interface definitions
- State variables with Vyper-specific types
- Structs and enums
- Import statements and interfaces
- Security-focused programming constructs
"""

from typing import List, Optional, Any, Union, Dict
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod

from ....core.runa_ast import ASTNode, SourceLocation, TranslationMetadata


class VyperNodeType(Enum):
    """Vyper-specific AST node types."""
    # Program structure
    MODULE = auto()
    IMPORT_STATEMENT = auto()
    FROM_IMPORT = auto()
    
    # Contract structure
    CONTRACT_DEFINITION = auto()
    INTERFACE_DEFINITION = auto()
    IMPLEMENTS_STATEMENT = auto()
    
    # Functions and decorators
    FUNCTION_DEFINITION = auto()
    DECORATOR = auto()
    CONSTRUCTOR = auto()
    
    # Variables and parameters
    VARIABLE_DECLARATION = auto()
    STATE_VARIABLE = auto()
    PARAMETER_LIST = auto()
    PARAMETER = auto()
    
    # Events and logging
    EVENT_DEFINITION = auto()
    LOG_STATEMENT = auto()
    
    # Statements
    BLOCK = auto()
    EXPRESSION_STATEMENT = auto()
    ASSIGNMENT_STATEMENT = auto()
    AUGMENTED_ASSIGNMENT = auto()
    IF_STATEMENT = auto()
    FOR_LOOP = auto()
    BREAK_STATEMENT = auto()
    CONTINUE_STATEMENT = auto()
    RETURN_STATEMENT = auto()
    ASSERT_STATEMENT = auto()
    RAISE_STATEMENT = auto()
    PASS_STATEMENT = auto()
    
    # Expressions
    IDENTIFIER = auto()
    LITERAL = auto()
    BINARY_EXPRESSION = auto()
    UNARY_EXPRESSION = auto()
    FUNCTION_CALL = auto()
    ATTRIBUTE_ACCESS = auto()
    SUBSCRIPT_ACCESS = auto()
    LIST_EXPRESSION = auto()
    DICT_EXPRESSION = auto()
    TUPLE_EXPRESSION = auto()
    
    # Types
    PRIMITIVE_TYPE = auto()
    ARRAY_TYPE = auto()
    DYNARRAY_TYPE = auto()
    HASHMAP_TYPE = auto()
    STRUCT_TYPE = auto()
    INTERFACE_TYPE = auto()
    
    # Special constructs
    STRUCT_DEFINITION = auto()
    ENUM_DEFINITION = auto()
    CONSTANT_DECLARATION = auto()
    IMMUTABLE_DECLARATION = auto()
    
    # Comments
    COMMENT = auto()


class VyperFunctionType(Enum):
    """Vyper function types based on decorators."""
    EXTERNAL = "@external"
    INTERNAL = "@internal"
    PURE = "@pure"
    VIEW = "@view"


class VyperDataLocation(Enum):
    """Vyper data locations."""
    STORAGE = "storage"
    MEMORY = "memory"
    CALLDATA = "calldata"


class VyperOperator(Enum):
    """Vyper operators."""
    # Arithmetic
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    INT_DIVIDE = "//"
    MODULO = "%"
    EXPONENT = "**"
    
    # Comparison
    EQUAL = "=="
    NOT_EQUAL = "!="
    LESS_THAN = "<"
    LESS_EQUAL = "<="
    GREATER_THAN = ">"
    GREATER_EQUAL = ">="
    
    # Logical
    AND = "and"
    OR = "or"
    NOT = "not"
    
    # Bitwise
    BIT_AND = "&"
    BIT_OR = "|"
    BIT_XOR = "^"
    BIT_NOT = "~"
    SHIFT_LEFT = "<<"
    SHIFT_RIGHT = ">>"
    
    # Assignment
    ASSIGN = "="
    PLUS_ASSIGN = "+="
    MINUS_ASSIGN = "-="
    MULTIPLY_ASSIGN = "*="
    DIVIDE_ASSIGN = "/="
    INT_DIVIDE_ASSIGN = "//="
    MODULO_ASSIGN = "%="
    EXPONENT_ASSIGN = "**="
    BIT_AND_ASSIGN = "&="
    BIT_OR_ASSIGN = "|="
    BIT_XOR_ASSIGN = "^="
    SHIFT_LEFT_ASSIGN = "<<="
    SHIFT_RIGHT_ASSIGN = ">>="


class VyperPrimitiveType(Enum):
    """Vyper primitive types."""
    # Integers
    UINT8 = "uint8"
    UINT16 = "uint16"
    UINT32 = "uint32"
    UINT64 = "uint64"
    UINT128 = "uint128"
    UINT256 = "uint256"
    INT8 = "int8"
    INT16 = "int16"
    INT32 = "int32"
    INT64 = "int64"
    INT128 = "int128"
    INT256 = "int256"
    
    # Other types
    BOOL = "bool"
    ADDRESS = "address"
    BYTES32 = "bytes32"
    BYTES = "Bytes"
    STRING = "String"
    DECIMAL = "decimal"


@dataclass
class VyperNode(ASTNode):
    """Base class for all Vyper AST nodes."""
    vyper_node_type: VyperNodeType = VyperNodeType.MODULE
    
    @abstractmethod
    def accept(self, visitor):
        """Accept a visitor for AST traversal."""
        pass


# ============================================================================
# Program Structure
# ============================================================================

@dataclass
class VyperModule(VyperNode):
    """Vyper module (file)"""
    vyper_node_type: VyperNodeType = VyperNodeType.MODULE
    imports: List['VyperImportStatement'] = field(default_factory=list)
    from_imports: List['VyperFromImport'] = field(default_factory=list)
    interfaces: List['VyperInterfaceDefinition'] = field(default_factory=list)
    implements: List['VyperImplementsStatement'] = field(default_factory=list)
    constants: List['VyperConstantDeclaration'] = field(default_factory=list)
    immutables: List['VyperImmutableDeclaration'] = field(default_factory=list)
    state_variables: List['VyperStateVariable'] = field(default_factory=list)
    structs: List['VyperStructDefinition'] = field(default_factory=list)
    enums: List['VyperEnumDefinition'] = field(default_factory=list)
    events: List['VyperEventDefinition'] = field(default_factory=list)
    functions: List['VyperFunctionDefinition'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vyper_module(self)


@dataclass
class VyperImportStatement(VyperNode):
    """Import statement: import interfaces"""
    vyper_node_type: VyperNodeType = VyperNodeType.IMPORT_STATEMENT
    module: str = ""
    alias: Optional[str] = None
    
    def accept(self, visitor):
        return visitor.visit_vyper_import_statement(self)


@dataclass
class VyperFromImport(VyperNode):
    """From import: from vyper.interfaces import ERC20"""
    vyper_node_type: VyperNodeType = VyperNodeType.FROM_IMPORT
    module: str = ""
    names: List[str] = field(default_factory=list)
    aliases: List[Optional[str]] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vyper_from_import(self)


# ============================================================================
# Contract Structure
# ============================================================================

@dataclass
class VyperInterfaceDefinition(VyperNode):
    """Interface definition: interface ERC20:"""
    vyper_node_type: VyperNodeType = VyperNodeType.INTERFACE_DEFINITION
    name: str = ""
    functions: List['VyperFunctionDefinition'] = field(default_factory=list)
    events: List['VyperEventDefinition'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vyper_interface_definition(self)


@dataclass
class VyperImplementsStatement(VyperNode):
    """Implements statement: implements: ERC20"""
    vyper_node_type: VyperNodeType = VyperNodeType.IMPLEMENTS_STATEMENT
    interface_name: str = ""
    
    def accept(self, visitor):
        return visitor.visit_vyper_implements_statement(self)


# ============================================================================
# Functions and Decorators
# ============================================================================

@dataclass
class VyperFunctionDefinition(VyperNode):
    """Function definition with decorators"""
    vyper_node_type: VyperNodeType = VyperNodeType.FUNCTION_DEFINITION
    name: str = ""
    decorators: List['VyperDecorator'] = field(default_factory=list)
    parameters: 'VyperParameterList' = None
    return_type: Optional['VyperTypeName'] = None
    body: List['VyperStatement'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vyper_function_definition(self)


@dataclass
class VyperDecorator(VyperNode):
    """Function decorator: @external, @internal, @pure, @view, @payable, @nonpayable"""
    vyper_node_type: VyperNodeType = VyperNodeType.DECORATOR
    name: str = ""
    
    def accept(self, visitor):
        return visitor.visit_vyper_decorator(self)


@dataclass
class VyperConstructor(VyperNode):
    """Constructor function: def __init__(self, ...):"""
    vyper_node_type: VyperNodeType = VyperNodeType.CONSTRUCTOR
    parameters: 'VyperParameterList' = None
    body: List['VyperStatement'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vyper_constructor(self)


# ============================================================================
# Variables and Parameters
# ============================================================================

@dataclass
class VyperVariableDeclaration(VyperNode):
    """Variable declaration"""
    vyper_node_type: VyperNodeType = VyperNodeType.VARIABLE_DECLARATION
    name: str = ""
    type_annotation: 'VyperTypeName' = None
    initial_value: Optional['VyperExpression'] = None
    is_public: bool = False
    
    def accept(self, visitor):
        return visitor.visit_vyper_variable_declaration(self)


@dataclass
class VyperStateVariable(VyperVariableDeclaration):
    """State variable: balance: public(uint256)"""
    vyper_node_type: VyperNodeType = VyperNodeType.STATE_VARIABLE
    
    def accept(self, visitor):
        return visitor.visit_vyper_state_variable(self)


@dataclass
class VyperParameterList(VyperNode):
    """Parameter list: (self, amount: uint256, recipient: address)"""
    vyper_node_type: VyperNodeType = VyperNodeType.PARAMETER_LIST
    parameters: List['VyperParameter'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vyper_parameter_list(self)


@dataclass
class VyperParameter(VyperNode):
    """Parameter: amount: uint256"""
    vyper_node_type: VyperNodeType = VyperNodeType.PARAMETER
    name: str = ""
    type_annotation: 'VyperTypeName' = None
    default_value: Optional['VyperExpression'] = None
    
    def accept(self, visitor):
        return visitor.visit_vyper_parameter(self)


# ============================================================================
# Events and Logging
# ============================================================================

@dataclass
class VyperEventDefinition(VyperNode):
    """Event definition: event Transfer:"""
    vyper_node_type: VyperNodeType = VyperNodeType.EVENT_DEFINITION
    name: str = ""
    parameters: List['VyperParameter'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vyper_event_definition(self)


@dataclass
class VyperLogStatement(VyperNode):
    """Log statement: log Transfer(sender, receiver, amount)"""
    vyper_node_type: VyperNodeType = VyperNodeType.LOG_STATEMENT
    event_call: 'VyperFunctionCall' = None
    
    def accept(self, visitor):
        return visitor.visit_vyper_log_statement(self)


# ============================================================================
# Statements
# ============================================================================

@dataclass
class VyperStatement(VyperNode):
    """Base class for statements"""
    pass


@dataclass
class VyperBlock(VyperStatement):
    """Block of statements"""
    vyper_node_type: VyperNodeType = VyperNodeType.BLOCK
    statements: List[VyperStatement] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vyper_block(self)


@dataclass
class VyperExpressionStatement(VyperStatement):
    """Expression statement"""
    vyper_node_type: VyperNodeType = VyperNodeType.EXPRESSION_STATEMENT
    expression: 'VyperExpression' = None
    
    def accept(self, visitor):
        return visitor.visit_vyper_expression_statement(self)


@dataclass
class VyperAssignmentStatement(VyperStatement):
    """Assignment statement: x = 5"""
    vyper_node_type: VyperNodeType = VyperNodeType.ASSIGNMENT_STATEMENT
    target: 'VyperExpression' = None
    value: 'VyperExpression' = None
    
    def accept(self, visitor):
        return visitor.visit_vyper_assignment_statement(self)


@dataclass
class VyperAugmentedAssignment(VyperStatement):
    """Augmented assignment: x += 5"""
    vyper_node_type: VyperNodeType = VyperNodeType.AUGMENTED_ASSIGNMENT
    target: 'VyperExpression' = None
    operator: VyperOperator = VyperOperator.PLUS_ASSIGN
    value: 'VyperExpression' = None
    
    def accept(self, visitor):
        return visitor.visit_vyper_augmented_assignment(self)


@dataclass
class VyperIfStatement(VyperStatement):
    """If statement: if condition:"""
    vyper_node_type: VyperNodeType = VyperNodeType.IF_STATEMENT
    condition: 'VyperExpression' = None
    body: List[VyperStatement] = field(default_factory=list)
    orelse: List[VyperStatement] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vyper_if_statement(self)


@dataclass
class VyperForLoop(VyperStatement):
    """For loop: for i in range(10):"""
    vyper_node_type: VyperNodeType = VyperNodeType.FOR_LOOP
    target: 'VyperExpression' = None
    iter: 'VyperExpression' = None
    body: List[VyperStatement] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vyper_for_loop(self)


@dataclass
class VyperBreakStatement(VyperStatement):
    """Break statement: break"""
    vyper_node_type: VyperNodeType = VyperNodeType.BREAK_STATEMENT
    
    def accept(self, visitor):
        return visitor.visit_vyper_break_statement(self)


@dataclass
class VyperContinueStatement(VyperStatement):
    """Continue statement: continue"""
    vyper_node_type: VyperNodeType = VyperNodeType.CONTINUE_STATEMENT
    
    def accept(self, visitor):
        return visitor.visit_vyper_continue_statement(self)


@dataclass
class VyperReturnStatement(VyperStatement):
    """Return statement: return value"""
    vyper_node_type: VyperNodeType = VyperNodeType.RETURN_STATEMENT
    value: Optional['VyperExpression'] = None
    
    def accept(self, visitor):
        return visitor.visit_vyper_return_statement(self)


@dataclass
class VyperAssertStatement(VyperStatement):
    """Assert statement: assert condition, "error message" """
    vyper_node_type: VyperNodeType = VyperNodeType.ASSERT_STATEMENT
    test: 'VyperExpression' = None
    msg: Optional['VyperExpression'] = None
    
    def accept(self, visitor):
        return visitor.visit_vyper_assert_statement(self)


@dataclass
class VyperRaiseStatement(VyperStatement):
    """Raise statement: raise "error message" """
    vyper_node_type: VyperNodeType = VyperNodeType.RAISE_STATEMENT
    exc: Optional['VyperExpression'] = None
    
    def accept(self, visitor):
        return visitor.visit_vyper_raise_statement(self)


@dataclass
class VyperPassStatement(VyperStatement):
    """Pass statement: pass"""
    vyper_node_type: VyperNodeType = VyperNodeType.PASS_STATEMENT
    
    def accept(self, visitor):
        return visitor.visit_vyper_pass_statement(self)


# ============================================================================
# Expressions
# ============================================================================

@dataclass
class VyperExpression(VyperNode):
    """Base class for expressions"""
    pass


@dataclass
class VyperIdentifier(VyperExpression):
    """Identifier: myVariable"""
    vyper_node_type: VyperNodeType = VyperNodeType.IDENTIFIER
    name: str = ""
    
    def accept(self, visitor):
        return visitor.visit_vyper_identifier(self)


@dataclass
class VyperLiteral(VyperExpression):
    """Literal: 42, "hello", True, 0x123..."""
    vyper_node_type: VyperNodeType = VyperNodeType.LITERAL
    value: Any = None
    type_name: str = ""
    
    def accept(self, visitor):
        return visitor.visit_vyper_literal(self)


@dataclass
class VyperBinaryExpression(VyperExpression):
    """Binary expression: a + b, x and y"""
    vyper_node_type: VyperNodeType = VyperNodeType.BINARY_EXPRESSION
    left: VyperExpression = None
    operator: VyperOperator = VyperOperator.PLUS
    right: VyperExpression = None
    
    def accept(self, visitor):
        return visitor.visit_vyper_binary_expression(self)


@dataclass
class VyperUnaryExpression(VyperExpression):
    """Unary expression: not flag, -value"""
    vyper_node_type: VyperNodeType = VyperNodeType.UNARY_EXPRESSION
    operator: VyperOperator = VyperOperator.NOT
    operand: VyperExpression = None
    
    def accept(self, visitor):
        return visitor.visit_vyper_unary_expression(self)


@dataclass
class VyperFunctionCall(VyperExpression):
    """Function call: func(arg1, arg2)"""
    vyper_node_type: VyperNodeType = VyperNodeType.FUNCTION_CALL
    func: VyperExpression = None
    args: List[VyperExpression] = field(default_factory=list)
    keywords: List['VyperKeyword'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vyper_function_call(self)


@dataclass
class VyperKeyword(VyperNode):
    """Keyword argument: name=value"""
    arg: str = ""
    value: VyperExpression = None
    
    def accept(self, visitor):
        return visitor.visit_vyper_keyword(self)


@dataclass
class VyperAttributeAccess(VyperExpression):
    """Attribute access: obj.attr"""
    vyper_node_type: VyperNodeType = VyperNodeType.ATTRIBUTE_ACCESS
    value: VyperExpression = None
    attr: str = ""
    
    def accept(self, visitor):
        return visitor.visit_vyper_attribute_access(self)


@dataclass
class VyperSubscriptAccess(VyperExpression):
    """Subscript access: array[index]"""
    vyper_node_type: VyperNodeType = VyperNodeType.SUBSCRIPT_ACCESS
    value: VyperExpression = None
    slice: 'VyperSlice' = None
    
    def accept(self, visitor):
        return visitor.visit_vyper_subscript_access(self)


@dataclass
class VyperSlice(VyperNode):
    """Slice: [start:end:step] or [index]"""
    lower: Optional[VyperExpression] = None
    upper: Optional[VyperExpression] = None
    step: Optional[VyperExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_vyper_slice(self)


@dataclass
class VyperListExpression(VyperExpression):
    """List expression: [1, 2, 3]"""
    vyper_node_type: VyperNodeType = VyperNodeType.LIST_EXPRESSION
    elements: List[VyperExpression] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vyper_list_expression(self)


@dataclass
class VyperDictExpression(VyperExpression):
    """Dictionary expression: {key1: value1, key2: value2}"""
    vyper_node_type: VyperNodeType = VyperNodeType.DICT_EXPRESSION
    keys: List[VyperExpression] = field(default_factory=list)
    values: List[VyperExpression] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vyper_dict_expression(self)


@dataclass
class VyperTupleExpression(VyperExpression):
    """Tuple expression: (a, b, c)"""
    vyper_node_type: VyperNodeType = VyperNodeType.TUPLE_EXPRESSION
    elements: List[VyperExpression] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vyper_tuple_expression(self)


# ============================================================================
# Types
# ============================================================================

@dataclass
class VyperTypeName(VyperNode):
    """Base class for type names"""
    pass


@dataclass
class VyperPrimitiveTypeName(VyperTypeName):
    """Primitive type: uint256, bool, address"""
    vyper_node_type: VyperNodeType = VyperNodeType.PRIMITIVE_TYPE
    name: VyperPrimitiveType = VyperPrimitiveType.UINT256
    
    def accept(self, visitor):
        return visitor.visit_vyper_primitive_type(self)


@dataclass
class VyperArrayType(VyperTypeName):
    """Array type: uint256[10]"""
    vyper_node_type: VyperNodeType = VyperNodeType.ARRAY_TYPE
    element_type: VyperTypeName = None
    size: Optional[VyperExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_vyper_array_type(self)


@dataclass
class VyperDynArrayType(VyperTypeName):
    """Dynamic array type: DynArray[uint256, 100]"""
    vyper_node_type: VyperNodeType = VyperNodeType.DYNARRAY_TYPE
    element_type: VyperTypeName = None
    max_size: VyperExpression = None
    
    def accept(self, visitor):
        return visitor.visit_vyper_dynarray_type(self)


@dataclass
class VyperHashMapType(VyperTypeName):
    """HashMap type: HashMap[address, uint256]"""
    vyper_node_type: VyperNodeType = VyperNodeType.HASHMAP_TYPE
    key_type: VyperTypeName = None
    value_type: VyperTypeName = None
    
    def accept(self, visitor):
        return visitor.visit_vyper_hashmap_type(self)


@dataclass
class VyperStructType(VyperTypeName):
    """Struct type: MyStruct"""
    vyper_node_type: VyperNodeType = VyperNodeType.STRUCT_TYPE
    name: str = ""
    
    def accept(self, visitor):
        return visitor.visit_vyper_struct_type(self)


@dataclass
class VyperInterfaceType(VyperTypeName):
    """Interface type: ERC20"""
    vyper_node_type: VyperNodeType = VyperNodeType.INTERFACE_TYPE
    name: str = ""
    
    def accept(self, visitor):
        return visitor.visit_vyper_interface_type(self)


# ============================================================================
# Special Constructs
# ============================================================================

@dataclass
class VyperStructDefinition(VyperNode):
    """Struct definition"""
    vyper_node_type: VyperNodeType = VyperNodeType.STRUCT_DEFINITION
    name: str = ""
    fields: List[VyperParameter] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vyper_struct_definition(self)


@dataclass
class VyperEnumDefinition(VyperNode):
    """Enum definition"""
    vyper_node_type: VyperNodeType = VyperNodeType.ENUM_DEFINITION
    name: str = ""
    values: List[str] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vyper_enum_definition(self)


@dataclass
class VyperConstantDeclaration(VyperNode):
    """Constant declaration: MAX_SUPPLY: constant(uint256) = 1000000"""
    vyper_node_type: VyperNodeType = VyperNodeType.CONSTANT_DECLARATION
    name: str = ""
    type_annotation: VyperTypeName = None
    value: VyperExpression = None
    
    def accept(self, visitor):
        return visitor.visit_vyper_constant_declaration(self)


@dataclass
class VyperImmutableDeclaration(VyperNode):
    """Immutable declaration: owner: immutable(address)"""
    vyper_node_type: VyperNodeType = VyperNodeType.IMMUTABLE_DECLARATION
    name: str = ""
    type_annotation: VyperTypeName = None
    
    def accept(self, visitor):
        return visitor.visit_vyper_immutable_declaration(self)


@dataclass
class VyperComment(VyperNode):
    """Comment: # This is a comment"""
    vyper_node_type: VyperNodeType = VyperNodeType.COMMENT
    text: str = ""
    
    def accept(self, visitor):
        return visitor.visit_vyper_comment(self)


# ============================================================================
# Convenience Factory Functions
# ============================================================================

def create_vyper_identifier(name: str) -> VyperIdentifier:
    """Create a Vyper identifier node."""
    return VyperIdentifier(name=name)


def create_vyper_literal(value: Any, type_name: str) -> VyperLiteral:
    """Create a Vyper literal node."""
    return VyperLiteral(value=value, type_name=type_name)


def create_vyper_primitive_type(type_name: VyperPrimitiveType) -> VyperPrimitiveTypeName:
    """Create a Vyper primitive type node."""
    return VyperPrimitiveTypeName(name=type_name)


def create_vyper_function_call(func: VyperExpression, args: List[VyperExpression]) -> VyperFunctionCall:
    """Create a Vyper function call node."""
    return VyperFunctionCall(func=func, args=args)


def create_vyper_binary_expression(left: VyperExpression, operator: VyperOperator, right: VyperExpression) -> VyperBinaryExpression:
    """Create a Vyper binary expression node."""
    return VyperBinaryExpression(left=left, operator=operator, right=right)


def create_vyper_variable_declaration(name: str, type_annotation: VyperTypeName, is_public: bool = False) -> VyperVariableDeclaration:
    """Create a Vyper variable declaration node."""
    return VyperVariableDeclaration(name=name, type_annotation=type_annotation, is_public=is_public)


def create_vyper_function_definition(name: str, decorators: List[VyperDecorator], parameters: VyperParameterList) -> VyperFunctionDefinition:
    """Create a Vyper function definition node."""
    return VyperFunctionDefinition(name=name, decorators=decorators, parameters=parameters)


def create_vyper_event_definition(name: str, parameters: List[VyperParameter]) -> VyperEventDefinition:
    """Create a Vyper event definition node."""
    return VyperEventDefinition(name=name, parameters=parameters)


def create_vyper_hashmap_type(key_type: VyperTypeName, value_type: VyperTypeName) -> VyperHashMapType:
    """Create a Vyper HashMap type node."""
    return VyperHashMapType(key_type=key_type, value_type=value_type)


def create_vyper_array_type(element_type: VyperTypeName, size: Optional[VyperExpression]) -> VyperArrayType:
    """Create a Vyper array type node."""
    return VyperArrayType(element_type=element_type, size=size) 