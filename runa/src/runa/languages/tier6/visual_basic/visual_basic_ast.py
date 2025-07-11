#!/usr/bin/env python3
"""
Visual Basic AST Node Definitions

Comprehensive Abstract Syntax Tree nodes for Visual Basic (.NET) covering all language features
including case-insensitive syntax, COM interoperability, Windows Forms, database connectivity,
event-driven programming, late binding, and .NET Framework integration.

This module provides complete AST representation for:
- Case-insensitive language constructs
- .NET Framework integration (namespaces, assemblies)
- COM interoperability and late binding
- Windows Forms and event-driven programming
- Database connectivity (ADO.NET, SQL Server)
- Optional parameters and named arguments
- Properties with Get/Set accessors
- Modules and namespace organization
- Error handling (Try/Catch/Finally)
- LINQ expressions and query syntax
- Generics and nullable types
"""

from typing import List, Optional, Any, Union, Dict
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod

from ....core.runa_ast import ASTNode, SourceLocation, TranslationMetadata


class VBNodeType(Enum):
    """Visual Basic-specific AST node types."""
    # Program structure
    SOURCE_UNIT = auto()
    NAMESPACE = auto()
    IMPORTS_STATEMENT = auto()
    OPTION_STATEMENT = auto()
    
    # Classes and modules
    CLASS_DECLARATION = auto()
    MODULE_DECLARATION = auto()
    INTERFACE_DECLARATION = auto()
    STRUCTURE_DECLARATION = auto()
    ENUM_DECLARATION = auto()
    DELEGATE_DECLARATION = auto()
    
    # Members
    METHOD_DECLARATION = auto()
    PROPERTY_DECLARATION = auto()
    FIELD_DECLARATION = auto()
    EVENT_DECLARATION = auto()
    CONSTRUCTOR_DECLARATION = auto()
    
    # Statements
    DIM_STATEMENT = auto()
    ASSIGNMENT_STATEMENT = auto()
    CALL_STATEMENT = auto()
    IF_STATEMENT = auto()
    SELECT_CASE_STATEMENT = auto()
    FOR_STATEMENT = auto()
    FOR_EACH_STATEMENT = auto()
    WHILE_STATEMENT = auto()
    DO_STATEMENT = auto()
    TRY_STATEMENT = auto()
    THROW_STATEMENT = auto()
    RETURN_STATEMENT = auto()
    EXIT_STATEMENT = auto()
    CONTINUE_STATEMENT = auto()
    GOTO_STATEMENT = auto()
    LABEL_STATEMENT = auto()
    WITH_STATEMENT = auto()
    USING_STATEMENT = auto()
    
    # Expressions
    LITERAL_EXPRESSION = auto()
    IDENTIFIER_EXPRESSION = auto()
    MEMBER_ACCESS_EXPRESSION = auto()
    INVOCATION_EXPRESSION = auto()
    BINARY_EXPRESSION = auto()
    UNARY_EXPRESSION = auto()
    CONDITIONAL_EXPRESSION = auto()
    NEW_EXPRESSION = auto()
    TYPEOF_EXPRESSION = auto()
    GETTYPE_EXPRESSION = auto()
    DIRECTCAST_EXPRESSION = auto()
    CTYPE_EXPRESSION = auto()
    LAMBDA_EXPRESSION = auto()
    QUERY_EXPRESSION = auto()
    
    # Arrays and collections
    ARRAY_CREATION_EXPRESSION = auto()
    ARRAY_ACCESS_EXPRESSION = auto()
    COLLECTION_INITIALIZER = auto()
    
    # COM and late binding
    LATE_BINDING_EXPRESSION = auto()
    COM_INTERFACE_DECLARATION = auto()
    
    # Comments and attributes
    COMMENT = auto()
    ATTRIBUTE = auto()


class VBAccessModifier(Enum):
    """Visual Basic access modifiers."""
    PUBLIC = "Public"
    PRIVATE = "Private"
    PROTECTED = "Protected"
    FRIEND = "Friend"
    PROTECTED_FRIEND = "Protected Friend"
    PRIVATE_PROTECTED = "Private Protected"


class VBMemberModifier(Enum):
    """Visual Basic member modifiers."""
    SHARED = "Shared"
    OVERRIDABLE = "Overridable"
    OVERRIDES = "Overrides"
    NOTOVERRIDABLE = "NotOverridable"
    MUSTOVERRIDE = "MustOverride"
    SHADOWS = "Shadows"
    READONLY = "ReadOnly"
    WRITEONLY = "WriteOnly"
    WITHEVENTS = "WithEvents"
    HANDLES = "Handles"


class VBOperator(Enum):
    """Visual Basic operators."""
    # Arithmetic
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    INTEGER_DIVIDE = "\\"
    MODULO = "Mod"
    EXPONENT = "^"
    
    # Comparison
    EQUALS = "="
    NOT_EQUALS = "<>"
    LESS_THAN = "<"
    LESS_EQUAL = "<="
    GREATER_THAN = ">"
    GREATER_EQUAL = ">="
    LIKE = "Like"
    IS = "Is"
    ISNOT = "IsNot"
    
    # Logical
    AND = "And"
    OR = "Or"
    XOR = "Xor"
    NOT = "Not"
    ANDALSO = "AndAlso"
    ORELSE = "OrElse"
    
    # String
    CONCATENATE = "&"
    
    # Assignment
    ASSIGN = "="
    PLUS_ASSIGN = "+="
    MINUS_ASSIGN = "-="
    MULTIPLY_ASSIGN = "*="
    DIVIDE_ASSIGN = "/="
    INTEGER_DIVIDE_ASSIGN = "\\="
    CONCATENATE_ASSIGN = "&="
    EXPONENT_ASSIGN = "^="


class VBExitType(Enum):
    """Visual Basic Exit statement types."""
    FUNCTION = "Function"
    SUB = "Sub"
    PROPERTY = "Property"
    DO = "Do"
    FOR = "For"
    WHILE = "While"
    SELECT = "Select"
    TRY = "Try"


@dataclass
class VBNode(ASTNode):
    """Base class for all Visual Basic AST nodes."""
    vb_node_type: VBNodeType = VBNodeType.SOURCE_UNIT
    
    @abstractmethod
    def accept(self, visitor):
        """Accept a visitor for AST traversal."""
        pass


# ============================================================================
# Program Structure
# ============================================================================

@dataclass
class VBSourceUnit(VBNode):
    """Visual Basic source unit (file)"""
    vb_node_type: VBNodeType = VBNodeType.SOURCE_UNIT
    option_statements: List['VBOptionStatement'] = field(default_factory=list)
    imports_statements: List['VBImportsStatement'] = field(default_factory=list)
    global_attributes: List['VBAttribute'] = field(default_factory=list)
    namespace_declarations: List['VBNamespace'] = field(default_factory=list)
    type_declarations: List['VBTypeDeclaration'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vb_source_unit(self)


@dataclass
class VBNamespace(VBNode):
    """Namespace declaration: Namespace MyNamespace ... End Namespace"""
    vb_node_type: VBNodeType = VBNodeType.NAMESPACE
    name: str = ""
    type_declarations: List['VBTypeDeclaration'] = field(default_factory=list)
    nested_namespaces: List['VBNamespace'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vb_namespace(self)


@dataclass
class VBImportsStatement(VBNode):
    """Imports statement: Imports System.Data"""
    vb_node_type: VBNodeType = VBNodeType.IMPORTS_STATEMENT
    namespace: str = ""
    alias: Optional[str] = None
    
    def accept(self, visitor):
        return visitor.visit_vb_imports_statement(self)


@dataclass
class VBOptionStatement(VBNode):
    """Option statement: Option Strict On"""
    vb_node_type: VBNodeType = VBNodeType.OPTION_STATEMENT
    option_type: str = ""  # Strict, Explicit, Compare, Infer
    value: str = ""        # On, Off, Binary, Text
    
    def accept(self, visitor):
        return visitor.visit_vb_option_statement(self)


# ============================================================================
# Type Declarations
# ============================================================================

@dataclass
class VBTypeDeclaration(VBNode):
    """Base class for type declarations."""
    name: str = ""
    access_modifier: VBAccessModifier = VBAccessModifier.PUBLIC
    attributes: List['VBAttribute'] = field(default_factory=list)


@dataclass
class VBClassDeclaration(VBTypeDeclaration):
    """Class declaration: Public Class MyClass ... End Class"""
    vb_node_type: VBNodeType = VBNodeType.CLASS_DECLARATION
    inherits_from: Optional[str] = None
    implements: List[str] = field(default_factory=list)
    is_partial: bool = False
    is_mustinherit: bool = False
    is_notinheritable: bool = False
    type_parameters: List['VBTypeParameter'] = field(default_factory=list)
    members: List['VBMemberDeclaration'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vb_class_declaration(self)


@dataclass
class VBModuleDeclaration(VBTypeDeclaration):
    """Module declaration: Module MyModule ... End Module"""
    vb_node_type: VBNodeType = VBNodeType.MODULE_DECLARATION
    members: List['VBMemberDeclaration'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vb_module_declaration(self)


@dataclass
class VBInterfaceDeclaration(VBTypeDeclaration):
    """Interface declaration: Interface IMyInterface ... End Interface"""
    vb_node_type: VBNodeType = VBNodeType.INTERFACE_DECLARATION
    inherits_from: List[str] = field(default_factory=list)
    type_parameters: List['VBTypeParameter'] = field(default_factory=list)
    members: List['VBMemberDeclaration'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vb_interface_declaration(self)


@dataclass
class VBStructureDeclaration(VBTypeDeclaration):
    """Structure declaration: Structure MyStruct ... End Structure"""
    vb_node_type: VBNodeType = VBNodeType.STRUCTURE_DECLARATION
    implements: List[str] = field(default_factory=list)
    type_parameters: List['VBTypeParameter'] = field(default_factory=list)
    members: List['VBMemberDeclaration'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vb_structure_declaration(self)


@dataclass
class VBEnumDeclaration(VBTypeDeclaration):
    """Enum declaration: Enum MyEnum ... End Enum"""
    vb_node_type: VBNodeType = VBNodeType.ENUM_DECLARATION
    underlying_type: Optional['VBType'] = None
    members: List['VBEnumMember'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vb_enum_declaration(self)


@dataclass
class VBEnumMember(VBNode):
    """Enum member: Value1 = 1"""
    name: str = ""
    value: Optional['VBExpression'] = None
    attributes: List['VBAttribute'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vb_enum_member(self)


@dataclass
class VBDelegateDeclaration(VBTypeDeclaration):
    """Delegate declaration: Delegate Sub MyDelegate(param As String)"""
    vb_node_type: VBNodeType = VBNodeType.DELEGATE_DECLARATION
    is_function: bool = False  # False for Sub, True for Function
    parameters: List['VBParameter'] = field(default_factory=list)
    return_type: Optional['VBType'] = None
    type_parameters: List['VBTypeParameter'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vb_delegate_declaration(self)


# ============================================================================
# Member Declarations
# ============================================================================

@dataclass
class VBMemberDeclaration(VBNode):
    """Base class for member declarations."""
    name: str = ""
    access_modifier: VBAccessModifier = VBAccessModifier.PUBLIC
    member_modifiers: List[VBMemberModifier] = field(default_factory=list)
    attributes: List['VBAttribute'] = field(default_factory=list)


@dataclass
class VBMethodDeclaration(VBMemberDeclaration):
    """Method declaration: Public Sub/Function MyMethod(...)"""
    vb_node_type: VBNodeType = VBNodeType.METHOD_DECLARATION
    is_function: bool = False  # False for Sub, True for Function
    parameters: List['VBParameter'] = field(default_factory=list)
    return_type: Optional['VBType'] = None
    type_parameters: List['VBTypeParameter'] = field(default_factory=list)
    body: List['VBStatement'] = field(default_factory=list)
    handles_clause: List[str] = field(default_factory=list)  # Event handlers
    implements_clause: List[str] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vb_method_declaration(self)


@dataclass
class VBPropertyDeclaration(VBMemberDeclaration):
    """Property declaration: Public Property MyProperty As String"""
    vb_node_type: VBNodeType = VBNodeType.PROPERTY_DECLARATION
    property_type: 'VBType' = None
    parameters: List['VBParameter'] = field(default_factory=list)  # For indexed properties
    getter: Optional['VBAccessorDeclaration'] = None
    setter: Optional['VBAccessorDeclaration'] = None
    auto_implemented: bool = False
    initial_value: Optional['VBExpression'] = None
    
    def accept(self, visitor):
        return visitor.visit_vb_property_declaration(self)


@dataclass
class VBAccessorDeclaration(VBNode):
    """Property accessor: Get ... End Get"""
    is_getter: bool = True  # True for Get, False for Set
    access_modifier: Optional[VBAccessModifier] = None
    body: List['VBStatement'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vb_accessor_declaration(self)


@dataclass
class VBFieldDeclaration(VBMemberDeclaration):
    """Field declaration: Public MyField As String"""
    vb_node_type: VBNodeType = VBNodeType.FIELD_DECLARATION
    field_type: 'VBType' = None
    initial_value: Optional['VBExpression'] = None
    is_constant: bool = False
    
    def accept(self, visitor):
        return visitor.visit_vb_field_declaration(self)


@dataclass
class VBEventDeclaration(VBMemberDeclaration):
    """Event declaration: Public Event MyEvent(sender As Object, e As EventArgs)"""
    vb_node_type: VBNodeType = VBNodeType.EVENT_DECLARATION
    event_type: Optional['VBType'] = None
    parameters: List['VBParameter'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vb_event_declaration(self)


@dataclass
class VBConstructorDeclaration(VBMemberDeclaration):
    """Constructor declaration: Public Sub New(...)"""
    vb_node_type: VBNodeType = VBNodeType.CONSTRUCTOR_DECLARATION
    parameters: List['VBParameter'] = field(default_factory=list)
    body: List['VBStatement'] = field(default_factory=list)
    base_constructor_arguments: List['VBExpression'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vb_constructor_declaration(self)


# ============================================================================
# Statements
# ============================================================================

@dataclass
class VBStatement(VBNode):
    """Base class for statements."""
    pass


@dataclass
class VBDimStatement(VBStatement):
    """Dim statement: Dim x As Integer = 5"""
    vb_node_type: VBNodeType = VBNodeType.DIM_STATEMENT
    variables: List['VBVariableDeclarator'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vb_dim_statement(self)


@dataclass
class VBVariableDeclarator(VBNode):
    """Variable declarator: x As Integer = 5"""
    name: str = ""
    variable_type: Optional['VBType'] = None
    initializer: Optional['VBExpression'] = None
    
    def accept(self, visitor):
        return visitor.visit_vb_variable_declarator(self)


@dataclass
class VBAssignmentStatement(VBStatement):
    """Assignment statement: x = 5"""
    vb_node_type: VBNodeType = VBNodeType.ASSIGNMENT_STATEMENT
    left: 'VBExpression' = None
    operator: VBOperator = VBOperator.ASSIGN
    right: 'VBExpression' = None
    
    def accept(self, visitor):
        return visitor.visit_vb_assignment_statement(self)


@dataclass
class VBCallStatement(VBStatement):
    """Call statement: Call MyMethod() or MyMethod()"""
    vb_node_type: VBNodeType = VBNodeType.CALL_STATEMENT
    expression: 'VBExpression' = None
    
    def accept(self, visitor):
        return visitor.visit_vb_call_statement(self)


@dataclass
class VBIfStatement(VBStatement):
    """If statement: If condition Then ... End If"""
    vb_node_type: VBNodeType = VBNodeType.IF_STATEMENT
    condition: 'VBExpression' = None
    then_statements: List[VBStatement] = field(default_factory=list)
    elseif_clauses: List['VBElseIfClause'] = field(default_factory=list)
    else_statements: List[VBStatement] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vb_if_statement(self)


@dataclass
class VBElseIfClause(VBNode):
    """ElseIf clause: ElseIf condition Then"""
    condition: 'VBExpression' = None
    statements: List[VBStatement] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vb_elseif_clause(self)


@dataclass
class VBSelectCaseStatement(VBStatement):
    """Select Case statement: Select Case expression ... End Select"""
    vb_node_type: VBNodeType = VBNodeType.SELECT_CASE_STATEMENT
    expression: 'VBExpression' = None
    case_clauses: List['VBCaseClause'] = field(default_factory=list)
    case_else_statements: List[VBStatement] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vb_select_case_statement(self)


@dataclass
class VBCaseClause(VBNode):
    """Case clause: Case value1, value2 To value3"""
    case_values: List['VBCaseValue'] = field(default_factory=list)
    statements: List[VBStatement] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vb_case_clause(self)


@dataclass
class VBCaseValue(VBNode):
    """Case value: single value, range (To), or comparison"""
    expression: 'VBExpression' = None
    is_range: bool = False
    range_end: Optional['VBExpression'] = None
    comparison_operator: Optional[VBOperator] = None
    
    def accept(self, visitor):
        return visitor.visit_vb_case_value(self)


@dataclass
class VBForStatement(VBStatement):
    """For statement: For i = 1 To 10 Step 2 ... Next"""
    vb_node_type: VBNodeType = VBNodeType.FOR_STATEMENT
    variable: str = ""
    start_value: 'VBExpression' = None
    end_value: 'VBExpression' = None
    step_value: Optional['VBExpression'] = None
    body: List[VBStatement] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vb_for_statement(self)


@dataclass
class VBForEachStatement(VBStatement):
    """For Each statement: For Each item In collection ... Next"""
    vb_node_type: VBNodeType = VBNodeType.FOR_EACH_STATEMENT
    variable: str = ""
    variable_type: Optional['VBType'] = None
    collection: 'VBExpression' = None
    body: List[VBStatement] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vb_for_each_statement(self)


@dataclass
class VBWhileStatement(VBStatement):
    """While statement: While condition ... End While"""
    vb_node_type: VBNodeType = VBNodeType.WHILE_STATEMENT
    condition: 'VBExpression' = None
    body: List[VBStatement] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vb_while_statement(self)


@dataclass
class VBDoStatement(VBStatement):
    """Do statement: Do While/Until condition ... Loop"""
    vb_node_type: VBNodeType = VBNodeType.DO_STATEMENT
    condition: Optional['VBExpression'] = None
    is_while: bool = True  # True for While, False for Until
    is_condition_at_top: bool = True  # True for Do While, False for Do...Loop While
    body: List[VBStatement] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vb_do_statement(self)


@dataclass
class VBTryStatement(VBStatement):
    """Try statement: Try ... Catch ... Finally ... End Try"""
    vb_node_type: VBNodeType = VBNodeType.TRY_STATEMENT
    try_statements: List[VBStatement] = field(default_factory=list)
    catch_clauses: List['VBCatchClause'] = field(default_factory=list)
    finally_statements: List[VBStatement] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vb_try_statement(self)


@dataclass
class VBCatchClause(VBNode):
    """Catch clause: Catch ex As Exception When condition"""
    exception_type: Optional['VBType'] = None
    exception_variable: Optional[str] = None
    when_condition: Optional['VBExpression'] = None
    statements: List[VBStatement] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vb_catch_clause(self)


@dataclass
class VBThrowStatement(VBStatement):
    """Throw statement: Throw exception"""
    vb_node_type: VBNodeType = VBNodeType.THROW_STATEMENT
    expression: Optional['VBExpression'] = None
    
    def accept(self, visitor):
        return visitor.visit_vb_throw_statement(self)


@dataclass
class VBReturnStatement(VBStatement):
    """Return statement: Return value"""
    vb_node_type: VBNodeType = VBNodeType.RETURN_STATEMENT
    expression: Optional['VBExpression'] = None
    
    def accept(self, visitor):
        return visitor.visit_vb_return_statement(self)


@dataclass
class VBExitStatement(VBStatement):
    """Exit statement: Exit For, Exit Sub, etc."""
    vb_node_type: VBNodeType = VBNodeType.EXIT_STATEMENT
    exit_type: VBExitType = VBExitType.SUB
    
    def accept(self, visitor):
        return visitor.visit_vb_exit_statement(self)


@dataclass
class VBContinueStatement(VBStatement):
    """Continue statement: Continue For, Continue While, etc."""
    vb_node_type: VBNodeType = VBNodeType.CONTINUE_STATEMENT
    continue_type: str = ""  # For, While, Do
    
    def accept(self, visitor):
        return visitor.visit_vb_continue_statement(self)


@dataclass
class VBWithStatement(VBStatement):
    """With statement: With object ... End With"""
    vb_node_type: VBNodeType = VBNodeType.WITH_STATEMENT
    expression: 'VBExpression' = None
    body: List[VBStatement] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vb_with_statement(self)


@dataclass
class VBUsingStatement(VBStatement):
    """Using statement: Using resource As Type ... End Using"""
    vb_node_type: VBNodeType = VBNodeType.USING_STATEMENT
    resource: 'VBExpression' = None
    body: List[VBStatement] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vb_using_statement(self)


# ============================================================================
# Expressions
# ============================================================================

@dataclass
class VBExpression(VBNode):
    """Base class for expressions."""
    pass


@dataclass
class VBLiteralExpression(VBExpression):
    """Literal expression: 42, "Hello", True, Nothing"""
    vb_node_type: VBNodeType = VBNodeType.LITERAL_EXPRESSION
    value: Any = None
    literal_type: str = ""  # String, Integer, Boolean, Nothing, etc.
    
    def accept(self, visitor):
        return visitor.visit_vb_literal_expression(self)


@dataclass
class VBIdentifierExpression(VBExpression):
    """Identifier expression: variableName"""
    vb_node_type: VBNodeType = VBNodeType.IDENTIFIER_EXPRESSION
    name: str = ""
    
    def accept(self, visitor):
        return visitor.visit_vb_identifier_expression(self)


@dataclass
class VBMemberAccessExpression(VBExpression):
    """Member access: object.member"""
    vb_node_type: VBNodeType = VBNodeType.MEMBER_ACCESS_EXPRESSION
    expression: VBExpression = None
    member_name: str = ""
    
    def accept(self, visitor):
        return visitor.visit_vb_member_access_expression(self)


@dataclass
class VBInvocationExpression(VBExpression):
    """Method invocation: method(args)"""
    vb_node_type: VBNodeType = VBNodeType.INVOCATION_EXPRESSION
    expression: VBExpression = None
    arguments: List['VBArgument'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vb_invocation_expression(self)


@dataclass
class VBArgument(VBNode):
    """Method argument: value or name:=value"""
    expression: VBExpression = None
    name: Optional[str] = None  # For named arguments
    is_byref: bool = False
    
    def accept(self, visitor):
        return visitor.visit_vb_argument(self)


@dataclass
class VBBinaryExpression(VBExpression):
    """Binary expression: left operator right"""
    vb_node_type: VBNodeType = VBNodeType.BINARY_EXPRESSION
    left: VBExpression = None
    operator: VBOperator = VBOperator.PLUS
    right: VBExpression = None
    
    def accept(self, visitor):
        return visitor.visit_vb_binary_expression(self)


@dataclass
class VBUnaryExpression(VBExpression):
    """Unary expression: Not expression, -expression"""
    vb_node_type: VBNodeType = VBNodeType.UNARY_EXPRESSION
    operator: VBOperator = VBOperator.NOT
    expression: VBExpression = None
    
    def accept(self, visitor):
        return visitor.visit_vb_unary_expression(self)


@dataclass
class VBNewExpression(VBExpression):
    """New expression: New Type(args)"""
    vb_node_type: VBNodeType = VBNodeType.NEW_EXPRESSION
    type_expression: 'VBType' = None
    arguments: List[VBArgument] = field(default_factory=list)
    initializer: Optional['VBCollectionInitializer'] = None
    
    def accept(self, visitor):
        return visitor.visit_vb_new_expression(self)


@dataclass
class VBLambdaExpression(VBExpression):
    """Lambda expression: Function(x) x * 2"""
    vb_node_type: VBNodeType = VBNodeType.LAMBDA_EXPRESSION
    is_function: bool = True  # True for Function, False for Sub
    parameters: List['VBParameter'] = field(default_factory=list)
    body: Union[VBExpression, List[VBStatement]] = None
    
    def accept(self, visitor):
        return visitor.visit_vb_lambda_expression(self)


# ============================================================================
# Types and Parameters
# ============================================================================

@dataclass
class VBType(VBNode):
    """Base class for type expressions."""
    pass


@dataclass
class VBNamedType(VBType):
    """Named type: String, Integer, MyClass"""
    name: str = ""
    type_arguments: List[VBType] = field(default_factory=list)
    is_nullable: bool = False
    
    def accept(self, visitor):
        return visitor.visit_vb_named_type(self)


@dataclass
class VBArrayType(VBType):
    """Array type: Integer(), String(,)"""
    element_type: VBType = None
    rank: int = 1  # Number of dimensions
    
    def accept(self, visitor):
        return visitor.visit_vb_array_type(self)


@dataclass
class VBParameter(VBNode):
    """Parameter: ByVal name As Type = defaultValue"""
    name: str = ""
    parameter_type: Optional[VBType] = None
    is_byref: bool = False
    is_optional: bool = False
    default_value: Optional[VBExpression] = None
    is_paramarray: bool = False
    attributes: List['VBAttribute'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vb_parameter(self)


@dataclass
class VBTypeParameter(VBNode):
    """Generic type parameter: T As {Class, New}"""
    name: str = ""
    constraints: List[str] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vb_type_parameter(self)


# ============================================================================
# Attributes and Comments
# ============================================================================

@dataclass
class VBAttribute(VBNode):
    """Attribute: <AttributeName(args)>"""
    vb_node_type: VBNodeType = VBNodeType.ATTRIBUTE
    name: str = ""
    arguments: List[VBArgument] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vb_attribute(self)


@dataclass
class VBComment(VBNode):
    """Comment: ' This is a comment"""
    vb_node_type: VBNodeType = VBNodeType.COMMENT
    text: str = ""
    is_documentation: bool = False
    
    def accept(self, visitor):
        return visitor.visit_vb_comment(self)


# ============================================================================
# Collections and Special Constructs
# ============================================================================

@dataclass
class VBCollectionInitializer(VBNode):
    """Collection initializer: {1, 2, 3}"""
    vb_node_type: VBNodeType = VBNodeType.COLLECTION_INITIALIZER
    elements: List[VBExpression] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vb_collection_initializer(self)


@dataclass
class VBArrayCreationExpression(VBExpression):
    """Array creation: New Integer() {1, 2, 3}"""
    vb_node_type: VBNodeType = VBNodeType.ARRAY_CREATION_EXPRESSION
    array_type: VBArrayType = None
    size_expressions: List[VBExpression] = field(default_factory=list)
    initializer: Optional[VBCollectionInitializer] = None
    
    def accept(self, visitor):
        return visitor.visit_vb_array_creation_expression(self)


@dataclass
class VBArrayAccessExpression(VBExpression):
    """Array access: array(index1, index2)"""
    vb_node_type: VBNodeType = VBNodeType.ARRAY_ACCESS_EXPRESSION
    array: VBExpression = None
    indices: List[VBExpression] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_vb_array_access_expression(self)


# ============================================================================
# Factory Functions
# ============================================================================

def create_vb_class(name: str, access_modifier: VBAccessModifier = VBAccessModifier.PUBLIC) -> VBClassDeclaration:
    """Create a Visual Basic class declaration."""
    return VBClassDeclaration(name=name, access_modifier=access_modifier)


def create_vb_module(name: str, access_modifier: VBAccessModifier = VBAccessModifier.PUBLIC) -> VBModuleDeclaration:
    """Create a Visual Basic module declaration."""
    return VBModuleDeclaration(name=name, access_modifier=access_modifier)


def create_vb_method(name: str, is_function: bool = False, 
                    access_modifier: VBAccessModifier = VBAccessModifier.PUBLIC) -> VBMethodDeclaration:
    """Create a Visual Basic method declaration."""
    return VBMethodDeclaration(name=name, is_function=is_function, access_modifier=access_modifier)


def create_vb_property(name: str, property_type: VBType,
                      access_modifier: VBAccessModifier = VBAccessModifier.PUBLIC) -> VBPropertyDeclaration:
    """Create a Visual Basic property declaration."""
    return VBPropertyDeclaration(name=name, property_type=property_type, access_modifier=access_modifier)


def create_vb_literal(value: Any, literal_type: str = "Object") -> VBLiteralExpression:
    """Create a Visual Basic literal expression."""
    return VBLiteralExpression(value=value, literal_type=literal_type)


def create_vb_identifier(name: str) -> VBIdentifierExpression:
    """Create a Visual Basic identifier expression."""
    return VBIdentifierExpression(name=name)


def create_vb_string_literal(value: str) -> VBLiteralExpression:
    """Create a Visual Basic string literal."""
    return VBLiteralExpression(value=value, literal_type="String")


def create_vb_integer_literal(value: int) -> VBLiteralExpression:
    """Create a Visual Basic integer literal."""
    return VBLiteralExpression(value=value, literal_type="Integer")


def create_vb_boolean_literal(value: bool) -> VBLiteralExpression:
    """Create a Visual Basic boolean literal."""
    return VBLiteralExpression(value=value, literal_type="Boolean")


def create_vb_nothing_literal() -> VBLiteralExpression:
    """Create a Visual Basic Nothing literal."""
    return VBLiteralExpression(value=None, literal_type="Nothing") 