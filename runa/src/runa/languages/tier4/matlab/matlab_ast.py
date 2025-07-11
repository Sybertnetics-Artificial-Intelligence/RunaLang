#!/usr/bin/env python3
"""
Matlab AST Node Definitions

Comprehensive Abstract Syntax Tree nodes for Matlab language covering all Matlab features
including matrix operations, functions, scripts, classes, object-oriented programming,
toolboxes, and scientific computing constructs.

This module provides complete AST representation for:
- Matrix and array operations with vectorization
- Functions with multiple inputs/outputs and variable arguments
- Scripts and live scripts with cell mode execution
- Classes with properties, methods, and inheritance
- Control flow with specialized Matlab constructs
- Toolbox-specific functions and operations
- File I/O and data import/export
- Graphics and plotting commands
- Signal processing and mathematical operations
"""

from typing import List, Optional, Any, Union, Dict
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod

from ....core.runa_ast import ASTNode, SourceLocation, TranslationMetadata


class MatlabNodeType(Enum):
    """Matlab-specific AST node types."""
    # File structure
    SCRIPT = auto()
    FUNCTION_FILE = auto()
    CLASS_FILE = auto()
    LIVE_SCRIPT = auto()
    
    # Functions
    FUNCTION_DECLARATION = auto()
    NESTED_FUNCTION = auto()
    ANONYMOUS_FUNCTION = auto()
    FUNCTION_HANDLE = auto()
    
    # Classes and objects
    CLASS_DECLARATION = auto()
    PROPERTIES_BLOCK = auto()
    METHODS_BLOCK = auto()
    EVENTS_BLOCK = auto()
    ENUMERATION_BLOCK = auto()
    PROPERTY_DECLARATION = auto()
    METHOD_DECLARATION = auto()
    
    # Variables and data types
    VARIABLE_DECLARATION = auto()
    GLOBAL_DECLARATION = auto()
    PERSISTENT_DECLARATION = auto()
    
    # Matrix and array operations
    MATRIX_EXPRESSION = auto()
    CELL_ARRAY = auto()
    STRUCT_EXPRESSION = auto()
    INDEXING_EXPRESSION = auto()
    SLICE_EXPRESSION = auto()
    
    # Expressions
    IDENTIFIER = auto()
    LITERAL_EXPRESSION = auto()
    STRING_EXPRESSION = auto()
    BINARY_EXPRESSION = auto()
    UNARY_EXPRESSION = auto()
    FUNCTION_CALL = auto()
    METHOD_CALL = auto()
    FIELD_ACCESS = auto()
    ASSIGNMENT_EXPRESSION = auto()
    
    # Control flow
    IF_STATEMENT = auto()
    ELSEIF_CLAUSE = auto()
    SWITCH_STATEMENT = auto()
    CASE_CLAUSE = auto()
    OTHERWISE_CLAUSE = auto()
    FOR_LOOP = auto()
    WHILE_LOOP = auto()
    TRY_CATCH_STATEMENT = auto()
    BREAK_STATEMENT = auto()
    CONTINUE_STATEMENT = auto()
    RETURN_STATEMENT = auto()
    
    # Special constructs
    COMMAND_FORM = auto()
    CLEAR_STATEMENT = auto()
    LOAD_STATEMENT = auto()
    SAVE_STATEMENT = auto()
    
    # Comments and documentation
    COMMENT = auto()
    HELP_COMMENT = auto()
    
    # Program structure
    PROGRAM = auto()


class MatlabVisibility(Enum):
    """Matlab visibility modifiers."""
    PUBLIC = "public"
    PRIVATE = "private"
    PROTECTED = "protected"


class MatlabPropertyAttributes(Enum):
    """Matlab property attributes."""
    CONSTANT = "Constant"
    ABSTRACT = "Abstract"
    ACCESS = "Access"
    GET_ACCESS = "GetAccess"
    SET_ACCESS = "SetAccess"
    DEPENDENT = "Dependent"
    TRANSIENT = "Transient"
    HIDDEN = "Hidden"


class MatlabMethodAttributes(Enum):
    """Matlab method attributes."""
    STATIC = "Static"
    ABSTRACT = "Abstract"
    ACCESS = "Access"
    HIDDEN = "Hidden"
    SEALED = "Sealed"


@dataclass
class MatlabNode(ASTNode):
    """Base class for all Matlab AST nodes."""
    matlab_node_type: MatlabNodeType = MatlabNodeType.PROGRAM
    
    @abstractmethod
    def accept(self, visitor):
        """Accept a visitor for AST traversal."""
        pass


# ============================================================================
# File Structure
# ============================================================================

@dataclass
class MatlabScript(MatlabNode):
    """Matlab script file (.m file without function declaration)"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.SCRIPT
    statements: List[MatlabNode] = field(default_factory=list)
    comments: List['MatlabComment'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_matlab_script(self)


@dataclass
class MatlabFunctionFile(MatlabNode):
    """Matlab function file (.m file with function declaration)"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.FUNCTION_FILE
    main_function: 'MatlabFunctionDeclaration' = None
    nested_functions: List['MatlabFunctionDeclaration'] = field(default_factory=list)
    comments: List['MatlabComment'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_matlab_function_file(self)


@dataclass
class MatlabClassFile(MatlabNode):
    """Matlab class file (.m file with classdef)"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.CLASS_FILE
    class_declaration: 'MatlabClassDeclaration' = None
    comments: List['MatlabComment'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_matlab_class_file(self)


@dataclass
class MatlabLiveScript(MatlabNode):
    """Matlab live script (.mlx file)"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.LIVE_SCRIPT
    cells: List['MatlabCell'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_matlab_live_script(self)


@dataclass
class MatlabCell(MatlabNode):
    """Cell in a live script"""
    cell_type: str = "code"  # "code", "text", "markdown"
    content: str = ""
    statements: List[MatlabNode] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_matlab_cell(self)


# ============================================================================
# Functions
# ============================================================================

@dataclass
class MatlabFunctionDeclaration(MatlabNode):
    """Function declaration: function [out1, out2] = fname(in1, in2)"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.FUNCTION_DECLARATION
    name: str = ""
    input_parameters: List[str] = field(default_factory=list)
    output_parameters: List[str] = field(default_factory=list)
    body: List[MatlabNode] = field(default_factory=list)
    help_comments: List[str] = field(default_factory=list)
    is_nested: bool = False
    
    def accept(self, visitor):
        return visitor.visit_matlab_function_declaration(self)


@dataclass
class MatlabAnonymousFunction(MatlabNode):
    """Anonymous function: @(x,y) x + y"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.ANONYMOUS_FUNCTION
    parameters: List[str] = field(default_factory=list)
    expression: Optional['MatlabExpression'] = None
    
    def accept(self, visitor):
        return visitor.visit_matlab_anonymous_function(self)


@dataclass
class MatlabFunctionHandle(MatlabNode):
    """Function handle: @functionName"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.FUNCTION_HANDLE
    function_name: str = ""
    
    def accept(self, visitor):
        return visitor.visit_matlab_function_handle(self)


# ============================================================================
# Classes and Object-Oriented Programming
# ============================================================================

@dataclass
class MatlabClassDeclaration(MatlabNode):
    """Class declaration: classdef ClassName < SuperClass"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.CLASS_DECLARATION
    name: str = ""
    superclasses: List[str] = field(default_factory=list)
    attributes: Dict[str, Any] = field(default_factory=dict)
    properties_blocks: List['MatlabPropertiesBlock'] = field(default_factory=list)
    methods_blocks: List['MatlabMethodsBlock'] = field(default_factory=list)
    events_blocks: List['MatlabEventsBlock'] = field(default_factory=list)
    enumeration_blocks: List['MatlabEnumerationBlock'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_matlab_class_declaration(self)


@dataclass
class MatlabPropertiesBlock(MatlabNode):
    """Properties block in class"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.PROPERTIES_BLOCK
    attributes: Dict[str, Any] = field(default_factory=dict)
    properties: List['MatlabPropertyDeclaration'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_matlab_properties_block(self)


@dataclass
class MatlabMethodsBlock(MatlabNode):
    """Methods block in class"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.METHODS_BLOCK
    attributes: Dict[str, Any] = field(default_factory=dict)
    methods: List['MatlabMethodDeclaration'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_matlab_methods_block(self)


@dataclass
class MatlabEventsBlock(MatlabNode):
    """Events block in class"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.EVENTS_BLOCK
    attributes: Dict[str, Any] = field(default_factory=dict)
    events: List[str] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_matlab_events_block(self)


@dataclass
class MatlabEnumerationBlock(MatlabNode):
    """Enumeration block in class"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.ENUMERATION_BLOCK
    values: List[str] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_matlab_enumeration_block(self)


@dataclass
class MatlabPropertyDeclaration(MatlabNode):
    """Property declaration in class"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.PROPERTY_DECLARATION
    name: str = ""
    default_value: Optional['MatlabExpression'] = None
    attributes: Dict[str, Any] = field(default_factory=dict)
    
    def accept(self, visitor):
        return visitor.visit_matlab_property_declaration(self)


@dataclass
class MatlabMethodDeclaration(MatlabNode):
    """Method declaration in class"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.METHOD_DECLARATION
    name: str = ""
    input_parameters: List[str] = field(default_factory=list)
    output_parameters: List[str] = field(default_factory=list)
    body: List[MatlabNode] = field(default_factory=list)
    attributes: Dict[str, Any] = field(default_factory=dict)
    
    def accept(self, visitor):
        return visitor.visit_matlab_method_declaration(self)


# ============================================================================
# Variables and Data Types
# ============================================================================

@dataclass
class MatlabVariableDeclaration(MatlabNode):
    """Variable declaration (implicit in Matlab)"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.VARIABLE_DECLARATION
    name: str = ""
    initial_value: Optional['MatlabExpression'] = None
    
    def accept(self, visitor):
        return visitor.visit_matlab_variable_declaration(self)


@dataclass
class MatlabGlobalDeclaration(MatlabNode):
    """Global variable declaration: global var1 var2"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.GLOBAL_DECLARATION
    variables: List[str] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_matlab_global_declaration(self)


@dataclass
class MatlabPersistentDeclaration(MatlabNode):
    """Persistent variable declaration: persistent var1 var2"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.PERSISTENT_DECLARATION
    variables: List[str] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_matlab_persistent_declaration(self)


# ============================================================================
# Matrix and Array Operations
# ============================================================================

@dataclass
class MatlabMatrixExpression(MatlabNode):
    """Matrix expression: [1, 2; 3, 4]"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.MATRIX_EXPRESSION
    rows: List[List['MatlabExpression']] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_matlab_matrix_expression(self)


@dataclass
class MatlabCellArray(MatlabNode):
    """Cell array: {1, 'hello'; 2, 'world'}"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.CELL_ARRAY
    rows: List[List['MatlabExpression']] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_matlab_cell_array(self)


@dataclass
class MatlabStructExpression(MatlabNode):
    """Struct expression: struct('field1', value1, 'field2', value2)"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.STRUCT_EXPRESSION
    fields: Dict[str, 'MatlabExpression'] = field(default_factory=dict)
    
    def accept(self, visitor):
        return visitor.visit_matlab_struct_expression(self)


@dataclass
class MatlabIndexingExpression(MatlabNode):
    """Array indexing: A(i, j), A{i}, A.field"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.INDEXING_EXPRESSION
    array: Optional['MatlabExpression'] = None
    indices: List['MatlabExpression'] = field(default_factory=list)
    indexing_type: str = "paren"  # "paren" (), "brace" {}, "dot" .
    
    def accept(self, visitor):
        return visitor.visit_matlab_indexing_expression(self)


@dataclass
class MatlabSliceExpression(MatlabNode):
    """Array slicing: A(1:end, :)"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.SLICE_EXPRESSION
    start: Optional['MatlabExpression'] = None
    step: Optional['MatlabExpression'] = None
    stop: Optional['MatlabExpression'] = None
    is_colon: bool = False  # : means all elements
    
    def accept(self, visitor):
        return visitor.visit_matlab_slice_expression(self)


# ============================================================================
# Expressions
# ============================================================================

@dataclass
class MatlabExpression(MatlabNode):
    """Base class for Matlab expressions."""
    pass


@dataclass
class MatlabIdentifier(MatlabExpression):
    """Identifier: variable_name"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.IDENTIFIER
    name: str = ""
    
    def accept(self, visitor):
        return visitor.visit_matlab_identifier(self)


@dataclass
class MatlabLiteralExpression(MatlabExpression):
    """Literal expression: 42, 3.14, true, 'hello'"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.LITERAL_EXPRESSION
    value: Any = None
    literal_type: str = "double"  # double, logical, char, string
    
    def accept(self, visitor):
        return visitor.visit_matlab_literal_expression(self)


@dataclass
class MatlabStringExpression(MatlabExpression):
    """String expression: "hello" or 'hello'"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.STRING_EXPRESSION
    value: str = ""
    is_char_array: bool = True  # true for 'hello', false for "hello"
    
    def accept(self, visitor):
        return visitor.visit_matlab_string_expression(self)


@dataclass
class MatlabBinaryExpression(MatlabExpression):
    """Binary expression: a + b, a .* b"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.BINARY_EXPRESSION
    left: Optional[MatlabExpression] = None
    operator: str = ""
    right: Optional[MatlabExpression] = None
    is_elementwise: bool = False  # true for .*, ./, .^
    
    def accept(self, visitor):
        return visitor.visit_matlab_binary_expression(self)


@dataclass
class MatlabUnaryExpression(MatlabExpression):
    """Unary expression: -x, ~flag, x'"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.UNARY_EXPRESSION
    operator: str = ""
    expression: Optional[MatlabExpression] = None
    is_postfix: bool = False
    
    def accept(self, visitor):
        return visitor.visit_matlab_unary_expression(self)


@dataclass
class MatlabFunctionCall(MatlabExpression):
    """Function call: func(arg1, arg2)"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.FUNCTION_CALL
    function: Optional[MatlabExpression] = None
    arguments: List[MatlabExpression] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_matlab_function_call(self)


@dataclass
class MatlabMethodCall(MatlabExpression):
    """Method call: obj.method(args)"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.METHOD_CALL
    object: Optional[MatlabExpression] = None
    method_name: str = ""
    arguments: List[MatlabExpression] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_matlab_method_call(self)


@dataclass
class MatlabFieldAccess(MatlabExpression):
    """Field access: obj.field"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.FIELD_ACCESS
    object: Optional[MatlabExpression] = None
    field_name: str = ""
    
    def accept(self, visitor):
        return visitor.visit_matlab_field_access(self)


@dataclass
class MatlabAssignmentExpression(MatlabExpression):
    """Assignment: x = y, [a, b] = func()"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.ASSIGNMENT_EXPRESSION
    targets: List[MatlabExpression] = field(default_factory=list)  # Can be multiple for [a,b] = 
    value: Optional[MatlabExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_matlab_assignment_expression(self)


# ============================================================================
# Control Flow
# ============================================================================

@dataclass
class MatlabIfStatement(MatlabNode):
    """If statement: if condition ... elseif ... else ... end"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.IF_STATEMENT
    condition: Optional[MatlabExpression] = None
    then_body: List[MatlabNode] = field(default_factory=list)
    elseif_clauses: List['MatlabElseifClause'] = field(default_factory=list)
    else_body: List[MatlabNode] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_matlab_if_statement(self)


@dataclass
class MatlabElseifClause(MatlabNode):
    """Elseif clause: elseif condition"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.ELSEIF_CLAUSE
    condition: Optional[MatlabExpression] = None
    body: List[MatlabNode] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_matlab_elseif_clause(self)


@dataclass
class MatlabSwitchStatement(MatlabNode):
    """Switch statement: switch expression case ... otherwise ... end"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.SWITCH_STATEMENT
    expression: Optional[MatlabExpression] = None
    case_clauses: List['MatlabCaseClause'] = field(default_factory=list)
    otherwise_clause: Optional['MatlabOtherwiseClause'] = None
    
    def accept(self, visitor):
        return visitor.visit_matlab_switch_statement(self)


@dataclass
class MatlabCaseClause(MatlabNode):
    """Case clause: case value"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.CASE_CLAUSE
    values: List[MatlabExpression] = field(default_factory=list)  # Can have multiple values
    body: List[MatlabNode] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_matlab_case_clause(self)


@dataclass
class MatlabOtherwiseClause(MatlabNode):
    """Otherwise clause: otherwise"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.OTHERWISE_CLAUSE
    body: List[MatlabNode] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_matlab_otherwise_clause(self)


@dataclass
class MatlabForLoop(MatlabNode):
    """For loop: for i = 1:10 ... end"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.FOR_LOOP
    variable: str = ""
    iterable: Optional[MatlabExpression] = None
    body: List[MatlabNode] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_matlab_for_loop(self)


@dataclass
class MatlabWhileLoop(MatlabNode):
    """While loop: while condition ... end"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.WHILE_LOOP
    condition: Optional[MatlabExpression] = None
    body: List[MatlabNode] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_matlab_while_loop(self)


@dataclass
class MatlabTryCatchStatement(MatlabNode):
    """Try-catch statement: try ... catch exception ... end"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.TRY_CATCH_STATEMENT
    try_body: List[MatlabNode] = field(default_factory=list)
    catch_body: List[MatlabNode] = field(default_factory=list)
    exception_variable: Optional[str] = None
    
    def accept(self, visitor):
        return visitor.visit_matlab_try_catch_statement(self)


@dataclass
class MatlabBreakStatement(MatlabNode):
    """Break statement: break"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.BREAK_STATEMENT
    
    def accept(self, visitor):
        return visitor.visit_matlab_break_statement(self)


@dataclass
class MatlabContinueStatement(MatlabNode):
    """Continue statement: continue"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.CONTINUE_STATEMENT
    
    def accept(self, visitor):
        return visitor.visit_matlab_continue_statement(self)


@dataclass
class MatlabReturnStatement(MatlabNode):
    """Return statement: return"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.RETURN_STATEMENT
    
    def accept(self, visitor):
        return visitor.visit_matlab_return_statement(self)


# ============================================================================
# Special Constructs
# ============================================================================

@dataclass
class MatlabCommandForm(MatlabNode):
    """Command form: command arg1 arg2 (without parentheses)"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.COMMAND_FORM
    command: str = ""
    arguments: List[str] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_matlab_command_form(self)


@dataclass
class MatlabClearStatement(MatlabNode):
    """Clear statement: clear variables"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.CLEAR_STATEMENT
    variables: List[str] = field(default_factory=list)
    clear_all: bool = False
    
    def accept(self, visitor):
        return visitor.visit_matlab_clear_statement(self)


@dataclass
class MatlabLoadStatement(MatlabNode):
    """Load statement: load filename variables"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.LOAD_STATEMENT
    filename: str = ""
    variables: List[str] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_matlab_load_statement(self)


@dataclass
class MatlabSaveStatement(MatlabNode):
    """Save statement: save filename variables"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.SAVE_STATEMENT
    filename: str = ""
    variables: List[str] = field(default_factory=list)
    options: List[str] = field(default_factory=list)  # -ascii, -mat, etc.
    
    def accept(self, visitor):
        return visitor.visit_matlab_save_statement(self)


# ============================================================================
# Comments and Documentation
# ============================================================================

@dataclass
class MatlabComment(MatlabNode):
    """Comment: % This is a comment"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.COMMENT
    text: str = ""
    is_block_comment: bool = False  # %{ ... %}
    
    def accept(self, visitor):
        return visitor.visit_matlab_comment(self)


@dataclass
class MatlabHelpComment(MatlabNode):
    """Help comment (function documentation)"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.HELP_COMMENT
    text: str = ""
    
    def accept(self, visitor):
        return visitor.visit_matlab_help_comment(self)


# ============================================================================
# Program Structure
# ============================================================================

@dataclass
class MatlabProgram(MatlabNode):
    """Complete Matlab program"""
    matlab_node_type: MatlabNodeType = MatlabNodeType.PROGRAM
    files: List[Union[MatlabScript, MatlabFunctionFile, MatlabClassFile, MatlabLiveScript]] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_matlab_program(self)


# ============================================================================
# Utility Functions
# ============================================================================

def create_matlab_identifier(name: str) -> MatlabIdentifier:
    """Create a Matlab identifier node."""
    return MatlabIdentifier(name=name)


def create_matlab_literal(value: Any, literal_type: str = "double") -> MatlabLiteralExpression:
    """Create a Matlab literal expression node."""
    return MatlabLiteralExpression(value=value, literal_type=literal_type)


def create_matlab_matrix(rows: List[List[MatlabExpression]]) -> MatlabMatrixExpression:
    """Create a Matlab matrix expression node."""
    return MatlabMatrixExpression(rows=rows)


def create_matlab_function(name: str, inputs: List[str] = None, outputs: List[str] = None) -> MatlabFunctionDeclaration:
    """Create a Matlab function declaration node."""
    return MatlabFunctionDeclaration(
        name=name,
        input_parameters=inputs or [],
        output_parameters=outputs or []
    )


def create_matlab_class(name: str, superclasses: List[str] = None) -> MatlabClassDeclaration:
    """Create a Matlab class declaration node."""
    return MatlabClassDeclaration(
        name=name,
        superclasses=superclasses or []
    )


def create_matlab_assignment(targets: List[MatlabExpression], value: MatlabExpression) -> MatlabAssignmentExpression:
    """Create a Matlab assignment expression node."""
    return MatlabAssignmentExpression(targets=targets, value=value)


def create_matlab_function_call(function: MatlabExpression, arguments: List[MatlabExpression]) -> MatlabFunctionCall:
    """Create a Matlab function call expression node."""
    return MatlabFunctionCall(function=function, arguments=arguments) 