#!/usr/bin/env python3
"""
Solidity AST Node Definitions

Comprehensive Abstract Syntax Tree nodes for Solidity language covering all Solidity features
including smart contracts, functions, modifiers, events, inheritance, state variables,
and blockchain-specific programming constructs.

This module provides complete AST representation for:
- Smart contracts and interfaces
- Functions with visibility and mutability modifiers
- Events and error definitions
- State variables and storage types
- Modifiers and inheritance
- Type system with value types and reference types
- Assembly blocks and low-level operations
- Payable functions and Ether handling
"""

from typing import List, Optional, Any, Union, Dict
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod

from ....core.runa_ast import ASTNode, SourceLocation, TranslationMetadata


class SolidityNodeType(Enum):
    """Solidity-specific AST node types."""
    # Program structure
    SOURCE_UNIT = auto()
    PRAGMA_DIRECTIVE = auto()
    IMPORT_DIRECTIVE = auto()
    
    # Contracts and inheritance
    CONTRACT_DEFINITION = auto()
    INTERFACE_DEFINITION = auto()
    LIBRARY_DEFINITION = auto()
    INHERITANCE_SPECIFIER = auto()
    
    # Functions and modifiers
    FUNCTION_DEFINITION = auto()
    MODIFIER_DEFINITION = auto()
    MODIFIER_INVOCATION = auto()
    FALLBACK_FUNCTION = auto()
    RECEIVE_FUNCTION = auto()
    CONSTRUCTOR = auto()
    
    # Variables and parameters
    VARIABLE_DECLARATION = auto()
    STATE_VARIABLE = auto()
    PARAMETER_LIST = auto()
    PARAMETER = auto()
    
    # Events and errors
    EVENT_DEFINITION = auto()
    ERROR_DEFINITION = auto()
    EMIT_STATEMENT = auto()
    REVERT_STATEMENT = auto()
    
    # Statements
    BLOCK = auto()
    EXPRESSION_STATEMENT = auto()
    ASSIGNMENT_STATEMENT = auto()
    IF_STATEMENT = auto()
    WHILE_LOOP = auto()
    FOR_LOOP = auto()
    DO_WHILE_LOOP = auto()
    BREAK_STATEMENT = auto()
    CONTINUE_STATEMENT = auto()
    RETURN_STATEMENT = auto()
    TRY_STATEMENT = auto()
    THROW_STATEMENT = auto()
    
    # Expressions
    IDENTIFIER = auto()
    LITERAL = auto()
    BINARY_EXPRESSION = auto()
    UNARY_EXPRESSION = auto()
    FUNCTION_CALL = auto()
    MEMBER_ACCESS = auto()
    INDEX_ACCESS = auto()
    CONDITIONAL_EXPRESSION = auto()
    
    # Types
    ELEMENTARY_TYPE = auto()
    ARRAY_TYPE = auto()
    MAPPING_TYPE = auto()
    FUNCTION_TYPE = auto()
    USER_DEFINED_TYPE = auto()
    
    # Assembly
    INLINE_ASSEMBLY = auto()
    ASSEMBLY_BLOCK = auto()
    ASSEMBLY_IDENTIFIER = auto()
    ASSEMBLY_LITERAL = auto()
    ASSEMBLY_FUNCTION_CALL = auto()
    
    # Special constructs
    USING_FOR_DECLARATION = auto()
    STRUCT_DEFINITION = auto()
    ENUM_DEFINITION = auto()
    CONSTANT_DECLARATION = auto()
    
    # Comments
    COMMENT = auto()


class SolidityVisibility(Enum):
    """Solidity visibility specifiers."""
    PUBLIC = "public"
    PRIVATE = "private"
    INTERNAL = "internal"
    EXTERNAL = "external"


class SolidityMutability(Enum):
    """Solidity state mutability."""
    PURE = "pure"
    VIEW = "view"
    PAYABLE = "payable"
    NONPAYABLE = "nonpayable"


class SolidityStorageLocation(Enum):
    """Solidity storage locations."""
    STORAGE = "storage"
    MEMORY = "memory"
    CALLDATA = "calldata"


class SolidityOperator(Enum):
    """Solidity operators."""
    # Arithmetic
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
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
    AND = "&&"
    OR = "||"
    NOT = "!"
    
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
    MODULO_ASSIGN = "%="
    BIT_AND_ASSIGN = "&="
    BIT_OR_ASSIGN = "|="
    BIT_XOR_ASSIGN = "^="
    SHIFT_LEFT_ASSIGN = "<<="
    SHIFT_RIGHT_ASSIGN = ">>="


@dataclass
class SolidityNode(ASTNode):
    """Base class for all Solidity AST nodes."""
    solidity_node_type: SolidityNodeType = SolidityNodeType.SOURCE_UNIT
    
    @abstractmethod
    def accept(self, visitor):
        """Accept a visitor for AST traversal."""
        pass


# ============================================================================
# Program Structure
# ============================================================================

@dataclass
class SoliditySourceUnit(SolidityNode):
    """Solidity source unit (file)"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.SOURCE_UNIT
    pragma_directives: List['SolidityPragmaDirective'] = field(default_factory=list)
    import_directives: List['SolidityImportDirective'] = field(default_factory=list)
    contracts: List['SolidityContractDefinition'] = field(default_factory=list)
    interfaces: List['SolidityInterfaceDefinition'] = field(default_factory=list)
    libraries: List['SolidityLibraryDefinition'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_solidity_source_unit(self)


@dataclass
class SolidityPragmaDirective(SolidityNode):
    """Pragma directive: pragma solidity ^0.8.0;"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.PRAGMA_DIRECTIVE
    name: str = ""
    value: str = ""
    
    def accept(self, visitor):
        return visitor.visit_solidity_pragma_directive(self)


@dataclass
class SolidityImportDirective(SolidityNode):
    """Import directive: import "./Contract.sol";"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.IMPORT_DIRECTIVE
    path: str = ""
    alias: Optional[str] = None
    symbols: List[str] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_solidity_import_directive(self)


# ============================================================================
# Contracts and Inheritance
# ============================================================================

@dataclass
class SolidityContractDefinition(SolidityNode):
    """Contract definition: contract MyContract is BaseContract { ... }"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.CONTRACT_DEFINITION
    name: str = ""
    is_abstract: bool = False
    inheritance: List['SolidityInheritanceSpecifier'] = field(default_factory=list)
    state_variables: List['SolidityStateVariable'] = field(default_factory=list)
    functions: List['SolidityFunctionDefinition'] = field(default_factory=list)
    modifiers: List['SolidityModifierDefinition'] = field(default_factory=list)
    events: List['SolidityEventDefinition'] = field(default_factory=list)
    errors: List['SolidityErrorDefinition'] = field(default_factory=list)
    structs: List['SolidityStructDefinition'] = field(default_factory=list)
    enums: List['SolidityEnumDefinition'] = field(default_factory=list)
    using_for: List['SolidityUsingForDeclaration'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_solidity_contract_definition(self)


@dataclass
class SolidityInterfaceDefinition(SolidityNode):
    """Interface definition: interface IMyInterface { ... }"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.INTERFACE_DEFINITION
    name: str = ""
    inheritance: List['SolidityInheritanceSpecifier'] = field(default_factory=list)
    functions: List['SolidityFunctionDefinition'] = field(default_factory=list)
    events: List['SolidityEventDefinition'] = field(default_factory=list)
    errors: List['SolidityErrorDefinition'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_solidity_interface_definition(self)


@dataclass
class SolidityLibraryDefinition(SolidityNode):
    """Library definition: library MyLibrary { ... }"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.LIBRARY_DEFINITION
    name: str = ""
    functions: List['SolidityFunctionDefinition'] = field(default_factory=list)
    structs: List['SolidityStructDefinition'] = field(default_factory=list)
    enums: List['SolidityEnumDefinition'] = field(default_factory=list)
    constants: List['SolidityConstantDeclaration'] = field(default_factory=list)
    using_for: List['SolidityUsingForDeclaration'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_solidity_library_definition(self)


@dataclass
class SolidityInheritanceSpecifier(SolidityNode):
    """Inheritance specifier: BaseContract(arg1, arg2)"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.INHERITANCE_SPECIFIER
    base_name: str = ""
    arguments: List['SolidityExpression'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_solidity_inheritance_specifier(self)


# ============================================================================
# Functions and Modifiers
# ============================================================================

@dataclass
class SolidityFunctionDefinition(SolidityNode):
    """Function definition: function myFunc() public payable returns (uint256) { ... }"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.FUNCTION_DEFINITION
    name: str = ""
    parameters: 'SolidityParameterList' = None
    return_parameters: Optional['SolidityParameterList'] = None
    visibility: SolidityVisibility = SolidityVisibility.INTERNAL
    mutability: SolidityMutability = SolidityMutability.NONPAYABLE
    is_virtual: bool = False
    is_override: bool = False
    modifiers: List['SolidityModifierInvocation'] = field(default_factory=list)
    body: Optional['SolidityBlock'] = None
    
    def accept(self, visitor):
        return visitor.visit_solidity_function_definition(self)


@dataclass
class SolidityModifierDefinition(SolidityNode):
    """Modifier definition: modifier onlyOwner() { require(msg.sender == owner); _; }"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.MODIFIER_DEFINITION
    name: str = ""
    parameters: 'SolidityParameterList' = None
    is_virtual: bool = False
    is_override: bool = False
    body: 'SolidityBlock' = None
    
    def accept(self, visitor):
        return visitor.visit_solidity_modifier_definition(self)


@dataclass
class SolidityModifierInvocation(SolidityNode):
    """Modifier invocation: onlyOwner, onlyRole(ADMIN_ROLE)"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.MODIFIER_INVOCATION
    name: str = ""
    arguments: List['SolidityExpression'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_solidity_modifier_invocation(self)


@dataclass
class SolidityConstructor(SolidityNode):
    """Constructor: constructor(uint256 _value) payable { ... }"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.CONSTRUCTOR
    parameters: 'SolidityParameterList' = None
    visibility: SolidityVisibility = SolidityVisibility.INTERNAL
    mutability: SolidityMutability = SolidityMutability.NONPAYABLE
    modifiers: List['SolidityModifierInvocation'] = field(default_factory=list)
    body: 'SolidityBlock' = None
    
    def accept(self, visitor):
        return visitor.visit_solidity_constructor(self)


@dataclass
class SolidityFallbackFunction(SolidityNode):
    """Fallback function: fallback() external payable { ... }"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.FALLBACK_FUNCTION
    parameters: Optional['SolidityParameterList'] = None
    return_parameters: Optional['SolidityParameterList'] = None
    visibility: SolidityVisibility = SolidityVisibility.EXTERNAL
    mutability: SolidityMutability = SolidityMutability.NONPAYABLE
    modifiers: List['SolidityModifierInvocation'] = field(default_factory=list)
    body: 'SolidityBlock' = None
    
    def accept(self, visitor):
        return visitor.visit_solidity_fallback_function(self)


@dataclass
class SolidityReceiveFunction(SolidityNode):
    """Receive function: receive() external payable { ... }"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.RECEIVE_FUNCTION
    visibility: SolidityVisibility = SolidityVisibility.EXTERNAL
    mutability: SolidityMutability = SolidityMutability.PAYABLE
    modifiers: List['SolidityModifierInvocation'] = field(default_factory=list)
    body: 'SolidityBlock' = None
    
    def accept(self, visitor):
        return visitor.visit_solidity_receive_function(self)


# ============================================================================
# Variables and Parameters
# ============================================================================

@dataclass
class SolidityVariableDeclaration(SolidityNode):
    """Variable declaration: uint256 public balance;"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.VARIABLE_DECLARATION
    type_name: 'SolidityTypeName' = None
    name: str = ""
    visibility: Optional[SolidityVisibility] = None
    storage_location: Optional[SolidityStorageLocation] = None
    is_constant: bool = False
    is_immutable: bool = False
    initial_value: Optional['SolidityExpression'] = None
    
    def accept(self, visitor):
        return visitor.visit_solidity_variable_declaration(self)


@dataclass
class SolidityStateVariable(SolidityVariableDeclaration):
    """State variable: uint256 public balance = 100;"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.STATE_VARIABLE
    
    def accept(self, visitor):
        return visitor.visit_solidity_state_variable(self)


@dataclass
class SolidityParameterList(SolidityNode):
    """Parameter list: (uint256 a, string memory b)"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.PARAMETER_LIST
    parameters: List['SolidityParameter'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_solidity_parameter_list(self)


@dataclass
class SolidityParameter(SolidityNode):
    """Parameter: uint256 value, string memory name"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.PARAMETER
    type_name: 'SolidityTypeName' = None
    name: str = ""
    storage_location: Optional[SolidityStorageLocation] = None
    
    def accept(self, visitor):
        return visitor.visit_solidity_parameter(self)


# ============================================================================
# Events and Errors
# ============================================================================

@dataclass
class SolidityEventDefinition(SolidityNode):
    """Event definition: event Transfer(address indexed from, address indexed to, uint256 value);"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.EVENT_DEFINITION
    name: str = ""
    parameters: 'SolidityParameterList' = None
    is_anonymous: bool = False
    
    def accept(self, visitor):
        return visitor.visit_solidity_event_definition(self)


@dataclass
class SolidityErrorDefinition(SolidityNode):
    """Error definition: error InsufficientBalance(uint256 available, uint256 required);"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.ERROR_DEFINITION
    name: str = ""
    parameters: 'SolidityParameterList' = None
    
    def accept(self, visitor):
        return visitor.visit_solidity_error_definition(self)


@dataclass
class SolidityEmitStatement(SolidityNode):
    """Emit statement: emit Transfer(from, to, amount);"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.EMIT_STATEMENT
    event_call: 'SolidityFunctionCall' = None
    
    def accept(self, visitor):
        return visitor.visit_solidity_emit_statement(self)


@dataclass
class SolidityRevertStatement(SolidityNode):
    """Revert statement: revert InsufficientBalance(balance, amount);"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.REVERT_STATEMENT
    error_call: Optional['SolidityFunctionCall'] = None
    message: Optional['SolidityExpression'] = None
    
    def accept(self, visitor):
        return visitor.visit_solidity_revert_statement(self)


# ============================================================================
# Statements
# ============================================================================

@dataclass
class SolidityStatement(SolidityNode):
    """Base class for statements"""
    pass


@dataclass
class SolidityBlock(SolidityStatement):
    """Block statement: { ... }"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.BLOCK
    statements: List[SolidityStatement] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_solidity_block(self)


@dataclass
class SolidityExpressionStatement(SolidityStatement):
    """Expression statement: func();"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.EXPRESSION_STATEMENT
    expression: 'SolidityExpression' = None
    
    def accept(self, visitor):
        return visitor.visit_solidity_expression_statement(self)


@dataclass
class SolidityAssignmentStatement(SolidityStatement):
    """Assignment statement: x = 5;"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.ASSIGNMENT_STATEMENT
    left: 'SolidityExpression' = None
    operator: SolidityOperator = SolidityOperator.ASSIGN
    right: 'SolidityExpression' = None
    
    def accept(self, visitor):
        return visitor.visit_solidity_assignment_statement(self)


@dataclass
class SolidityIfStatement(SolidityStatement):
    """If statement: if (condition) { ... } else { ... }"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.IF_STATEMENT
    condition: 'SolidityExpression' = None
    then_statement: SolidityStatement = None
    else_statement: Optional[SolidityStatement] = None
    
    def accept(self, visitor):
        return visitor.visit_solidity_if_statement(self)


@dataclass
class SolidityWhileLoop(SolidityStatement):
    """While loop: while (condition) { ... }"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.WHILE_LOOP
    condition: 'SolidityExpression' = None
    body: SolidityStatement = None
    
    def accept(self, visitor):
        return visitor.visit_solidity_while_loop(self)


@dataclass
class SolidityForLoop(SolidityStatement):
    """For loop: for (uint i = 0; i < 10; i++) { ... }"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.FOR_LOOP
    init_statement: Optional[SolidityStatement] = None
    condition: Optional['SolidityExpression'] = None
    update_expression: Optional['SolidityExpression'] = None
    body: SolidityStatement = None
    
    def accept(self, visitor):
        return visitor.visit_solidity_for_loop(self)


@dataclass
class SolidityDoWhileLoop(SolidityStatement):
    """Do-while loop: do { ... } while (condition);"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.DO_WHILE_LOOP
    body: SolidityStatement = None
    condition: 'SolidityExpression' = None
    
    def accept(self, visitor):
        return visitor.visit_solidity_do_while_loop(self)


@dataclass
class SolidityBreakStatement(SolidityStatement):
    """Break statement: break;"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.BREAK_STATEMENT
    
    def accept(self, visitor):
        return visitor.visit_solidity_break_statement(self)


@dataclass
class SolidityContinueStatement(SolidityStatement):
    """Continue statement: continue;"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.CONTINUE_STATEMENT
    
    def accept(self, visitor):
        return visitor.visit_solidity_continue_statement(self)


@dataclass
class SolidityReturnStatement(SolidityStatement):
    """Return statement: return value;"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.RETURN_STATEMENT
    expression: Optional['SolidityExpression'] = None
    
    def accept(self, visitor):
        return visitor.visit_solidity_return_statement(self)


@dataclass
class SolidityTryStatement(SolidityStatement):
    """Try statement: try external.call() returns (uint result) { ... } catch { ... }"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.TRY_STATEMENT
    expression: 'SolidityExpression' = None
    return_parameters: Optional['SolidityParameterList'] = None
    try_block: SolidityBlock = None
    catch_clauses: List['SolidityCatchClause'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_solidity_try_statement(self)


@dataclass
class SolidityCatchClause(SolidityNode):
    """Catch clause: catch Error(string memory reason) { ... }"""
    identifier: Optional[str] = None
    parameters: Optional['SolidityParameterList'] = None
    block: SolidityBlock = None
    
    def accept(self, visitor):
        return visitor.visit_solidity_catch_clause(self)


# ============================================================================
# Expressions
# ============================================================================

@dataclass
class SolidityExpression(SolidityNode):
    """Base class for expressions"""
    pass


@dataclass
class SolidityIdentifier(SolidityExpression):
    """Identifier: myVariable"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.IDENTIFIER
    name: str = ""
    
    def accept(self, visitor):
        return visitor.visit_solidity_identifier(self)


@dataclass
class SolidityLiteral(SolidityExpression):
    """Literal: 42, "hello", true, 0x123..."""
    solidity_node_type: SolidityNodeType = SolidityNodeType.LITERAL
    value: Any = None
    type_name: str = ""  # uint256, string, bool, address, etc.
    
    def accept(self, visitor):
        return visitor.visit_solidity_literal(self)


@dataclass
class SolidityBinaryExpression(SolidityExpression):
    """Binary expression: a + b, x && y"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.BINARY_EXPRESSION
    left: SolidityExpression = None
    operator: SolidityOperator = SolidityOperator.PLUS
    right: SolidityExpression = None
    
    def accept(self, visitor):
        return visitor.visit_solidity_binary_expression(self)


@dataclass
class SolidityUnaryExpression(SolidityExpression):
    """Unary expression: !flag, ++counter"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.UNARY_EXPRESSION
    operator: SolidityOperator = SolidityOperator.NOT
    expression: SolidityExpression = None
    is_prefix: bool = True
    
    def accept(self, visitor):
        return visitor.visit_solidity_unary_expression(self)


@dataclass
class SolidityFunctionCall(SolidityExpression):
    """Function call: func(arg1, arg2)"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.FUNCTION_CALL
    expression: SolidityExpression = None
    arguments: List[SolidityExpression] = field(default_factory=list)
    names: List[str] = field(default_factory=list)  # For named arguments
    
    def accept(self, visitor):
        return visitor.visit_solidity_function_call(self)


@dataclass
class SolidityMemberAccess(SolidityExpression):
    """Member access: obj.member"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.MEMBER_ACCESS
    expression: SolidityExpression = None
    member_name: str = ""
    
    def accept(self, visitor):
        return visitor.visit_solidity_member_access(self)


@dataclass
class SolidityIndexAccess(SolidityExpression):
    """Index access: array[index]"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.INDEX_ACCESS
    base: SolidityExpression = None
    index: Optional[SolidityExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_solidity_index_access(self)


@dataclass
class SolidityConditionalExpression(SolidityExpression):
    """Conditional expression: condition ? value1 : value2"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.CONDITIONAL_EXPRESSION
    condition: SolidityExpression = None
    true_expression: SolidityExpression = None
    false_expression: SolidityExpression = None
    
    def accept(self, visitor):
        return visitor.visit_solidity_conditional_expression(self)


# ============================================================================
# Types
# ============================================================================

@dataclass
class SolidityTypeName(SolidityNode):
    """Base class for type names"""
    pass


@dataclass
class SolidityElementaryType(SolidityTypeName):
    """Elementary type: uint256, bool, address, bytes32"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.ELEMENTARY_TYPE
    name: str = ""
    
    def accept(self, visitor):
        return visitor.visit_solidity_elementary_type(self)


@dataclass
class SolidityArrayType(SolidityTypeName):
    """Array type: uint256[], bytes[32]"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.ARRAY_TYPE
    base_type: SolidityTypeName = None
    length: Optional[SolidityExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_solidity_array_type(self)


@dataclass
class SolidityMappingType(SolidityTypeName):
    """Mapping type: mapping(address => uint256)"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.MAPPING_TYPE
    key_type: SolidityTypeName = None
    value_type: SolidityTypeName = None
    
    def accept(self, visitor):
        return visitor.visit_solidity_mapping_type(self)


@dataclass
class SolidityFunctionType(SolidityTypeName):
    """Function type: function(uint256) external pure returns (bool)"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.FUNCTION_TYPE
    parameters: 'SolidityParameterList' = None
    return_parameters: Optional['SolidityParameterList'] = None
    visibility: SolidityVisibility = SolidityVisibility.INTERNAL
    mutability: SolidityMutability = SolidityMutability.NONPAYABLE
    
    def accept(self, visitor):
        return visitor.visit_solidity_function_type(self)


@dataclass
class SolidityUserDefinedType(SolidityTypeName):
    """User-defined type: MyStruct, MyContract"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.USER_DEFINED_TYPE
    name: str = ""
    
    def accept(self, visitor):
        return visitor.visit_solidity_user_defined_type(self)


# ============================================================================
# Assembly
# ============================================================================

@dataclass
class SolidityInlineAssembly(SolidityStatement):
    """Inline assembly: assembly { ... }"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.INLINE_ASSEMBLY
    dialect: str = "evmasm"
    flags: List[str] = field(default_factory=list)
    body: 'SolidityAssemblyBlock' = None
    
    def accept(self, visitor):
        return visitor.visit_solidity_inline_assembly(self)


@dataclass
class SolidityAssemblyBlock(SolidityNode):
    """Assembly block containing assembly statements"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.ASSEMBLY_BLOCK
    statements: List['SolidityAssemblyItem'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_solidity_assembly_block(self)


@dataclass
class SolidityAssemblyItem(SolidityNode):
    """Base class for assembly items"""
    pass


@dataclass
class SolidityAssemblyIdentifier(SolidityAssemblyItem):
    """Assembly identifier"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.ASSEMBLY_IDENTIFIER
    name: str = ""
    
    def accept(self, visitor):
        return visitor.visit_solidity_assembly_identifier(self)


@dataclass
class SolidityAssemblyLiteral(SolidityAssemblyItem):
    """Assembly literal"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.ASSEMBLY_LITERAL
    value: Any = None
    type_name: str = ""
    
    def accept(self, visitor):
        return visitor.visit_solidity_assembly_literal(self)


@dataclass
class SolidityAssemblyFunctionCall(SolidityAssemblyItem):
    """Assembly function call"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.ASSEMBLY_FUNCTION_CALL
    function_name: str = ""
    arguments: List[SolidityAssemblyItem] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_solidity_assembly_function_call(self)


# ============================================================================
# Special Constructs
# ============================================================================

@dataclass
class SolidityUsingForDeclaration(SolidityNode):
    """Using for declaration: using SafeMath for uint256;"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.USING_FOR_DECLARATION
    library_name: str = ""
    type_name: Optional[SolidityTypeName] = None  # None for '*'
    
    def accept(self, visitor):
        return visitor.visit_solidity_using_for_declaration(self)


@dataclass
class SolidityStructDefinition(SolidityNode):
    """Struct definition: struct Person { string name; uint age; }"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.STRUCT_DEFINITION
    name: str = ""
    members: List[SolidityVariableDeclaration] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_solidity_struct_definition(self)


@dataclass
class SolidityEnumDefinition(SolidityNode):
    """Enum definition: enum State { Active, Inactive }"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.ENUM_DEFINITION
    name: str = ""
    members: List[str] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_solidity_enum_definition(self)


@dataclass
class SolidityConstantDeclaration(SolidityNode):
    """Constant declaration: uint256 constant MAX_SUPPLY = 1000000;"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.CONSTANT_DECLARATION
    type_name: SolidityTypeName = None
    name: str = ""
    value: SolidityExpression = None
    
    def accept(self, visitor):
        return visitor.visit_solidity_constant_declaration(self)


# ============================================================================
# Comments
# ============================================================================

@dataclass
class SolidityComment(SolidityNode):
    """Comment: // or /* */"""
    solidity_node_type: SolidityNodeType = SolidityNodeType.COMMENT
    text: str = ""
    is_block_comment: bool = False
    
    def accept(self, visitor):
        return visitor.visit_solidity_comment(self)


# ============================================================================
# Utility Functions
# ============================================================================

def create_solidity_identifier(name: str) -> SolidityIdentifier:
    """Create a Solidity identifier node."""
    return SolidityIdentifier(name=name)


def create_solidity_literal(value: Any, type_name: str) -> SolidityLiteral:
    """Create a Solidity literal node."""
    return SolidityLiteral(value=value, type_name=type_name)


def create_solidity_elementary_type(name: str) -> SolidityElementaryType:
    """Create a Solidity elementary type node."""
    return SolidityElementaryType(name=name)


def create_solidity_function_call(expression: SolidityExpression, arguments: List[SolidityExpression]) -> SolidityFunctionCall:
    """Create a Solidity function call node."""
    return SolidityFunctionCall(expression=expression, arguments=arguments)


def create_solidity_binary_expression(left: SolidityExpression, operator: SolidityOperator, right: SolidityExpression) -> SolidityBinaryExpression:
    """Create a Solidity binary expression node."""
    return SolidityBinaryExpression(left=left, operator=operator, right=right)


def create_solidity_variable_declaration(type_name: SolidityTypeName, name: str, visibility: SolidityVisibility = None) -> SolidityVariableDeclaration:
    """Create a Solidity variable declaration node."""
    return SolidityVariableDeclaration(type_name=type_name, name=name, visibility=visibility)


def create_solidity_function_definition(name: str, parameters: SolidityParameterList, visibility: SolidityVisibility, mutability: SolidityMutability) -> SolidityFunctionDefinition:
    """Create a Solidity function definition node."""
    return SolidityFunctionDefinition(
        name=name,
        parameters=parameters,
        visibility=visibility,
        mutability=mutability
    )


def create_solidity_contract_definition(name: str, is_abstract: bool = False) -> SolidityContractDefinition:
    """Create a Solidity contract definition node."""
    return SolidityContractDefinition(name=name, is_abstract=is_abstract)


def create_solidity_event_definition(name: str, parameters: SolidityParameterList, is_anonymous: bool = False) -> SolidityEventDefinition:
    """Create a Solidity event definition node."""
    return SolidityEventDefinition(name=name, parameters=parameters, is_anonymous=is_anonymous)


def create_solidity_mapping_type(key_type: SolidityTypeName, value_type: SolidityTypeName) -> SolidityMappingType:
    """Create a Solidity mapping type node."""
    return SolidityMappingType(key_type=key_type, value_type=value_type) 