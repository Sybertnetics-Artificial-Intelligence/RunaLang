#!/usr/bin/env python3
"""
R AST Node Definitions

Comprehensive Abstract Syntax Tree nodes for R language covering all R features
including data structures, functions, statistical operations, vectorization,
packages, and R-specific programming constructs.

This module provides complete AST representation for:
- Data structures: vectors, lists, data frames, matrices, factors
- Functions and closures with lazy evaluation
- Statistical operations and modeling
- Control flow with vectorization
- Package system and namespaces
- Object-oriented programming (S3, S4, R6)
- Expression evaluation and environments
"""

from typing import List, Optional, Any, Union, Dict
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod

from ....core.runa_ast import ASTNode, SourceLocation, TranslationMetadata


class RNodeType(Enum):
    """R-specific AST node types."""
    # Program structure
    PROGRAM = auto()
    SCRIPT = auto()
    PACKAGE = auto()
    
    # Functions
    FUNCTION_DEFINITION = auto()
    FUNCTION_CALL = auto()
    METHOD_CALL = auto()
    
    # Variables and assignment
    IDENTIFIER = auto()
    ASSIGNMENT = auto()
    LEFT_ASSIGNMENT = auto()
    RIGHT_ASSIGNMENT = auto()
    SUPER_ASSIGNMENT = auto()
    
    # Data structures
    VECTOR = auto()
    LIST = auto()
    DATA_FRAME = auto()
    MATRIX = auto()
    ARRAY = auto()
    FACTOR = auto()
    
    # Expressions
    LITERAL_EXPRESSION = auto()
    NUMERIC_LITERAL = auto()
    STRING_LITERAL = auto()
    LOGICAL_LITERAL = auto()
    NULL_LITERAL = auto()
    NA_LITERAL = auto()
    BINARY_EXPRESSION = auto()
    UNARY_EXPRESSION = auto()
    
    # Indexing and subsetting
    INDEX_EXPRESSION = auto()
    SUBSET_EXPRESSION = auto()
    MEMBER_ACCESS = auto()
    DOLLAR_ACCESS = auto()
    AT_ACCESS = auto()
    
    # Control flow
    IF_STATEMENT = auto()
    FOR_LOOP = auto()
    WHILE_LOOP = auto()
    REPEAT_LOOP = auto()
    NEXT_STATEMENT = auto()
    BREAK_STATEMENT = auto()
    RETURN_STATEMENT = auto()
    
    # Special constructs
    FORMULA = auto()
    HELP_EXPRESSION = auto()
    NAMESPACE_ACCESS = auto()
    PACKAGE_LOAD = auto()
    
    # Statistical operations
    PIPE_EXPRESSION = auto()
    TILDE_EXPRESSION = auto()
    
    # Object-oriented
    S3_METHOD = auto()
    S4_CLASS = auto()
    S4_METHOD = auto()
    R6_CLASS = auto()
    
    # Comments
    COMMENT = auto()


class ROperator(Enum):
    """R operators."""
    # Arithmetic
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    INTEGER_DIVIDE = "%/%"
    MODULO = "%%"
    POWER = "^"
    POWER_ALT = "**"
    
    # Comparison
    EQUAL = "=="
    NOT_EQUAL = "!="
    LESS_THAN = "<"
    LESS_EQUAL = "<="
    GREATER_THAN = ">"
    GREATER_EQUAL = ">="
    
    # Logical
    AND = "&"
    OR = "|"
    NOT = "!"
    AND_SHORT = "&&"
    OR_SHORT = "||"
    
    # Assignment
    ASSIGN = "<-"
    ASSIGN_RIGHT = "->"
    ASSIGN_EQUAL = "="
    SUPER_ASSIGN = "<<-"
    SUPER_ASSIGN_RIGHT = "->>"
    
    # Special
    IN = "%in%"
    MATCH = "%*%"
    OUTER = "%o%"
    KRONECKER = "%x%"
    PIPE = "%>%"
    NAMESPACE = "::"
    NAMESPACE_INTERNAL = ":::"


@dataclass
class RNode(ASTNode):
    """Base class for all R AST nodes."""
    r_node_type: RNodeType = RNodeType.PROGRAM
    
    @abstractmethod
    def accept(self, visitor):
        """Accept a visitor for AST traversal."""
        pass


# ============================================================================
# Program Structure
# ============================================================================

@dataclass
class RProgram(RNode):
    """R program containing statements"""
    r_node_type: RNodeType = RNodeType.PROGRAM
    statements: List[RNode] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_r_program(self)


@dataclass
class RScript(RNode):
    """R script file"""
    r_node_type: RNodeType = RNodeType.SCRIPT
    statements: List[RNode] = field(default_factory=list)
    comments: List['RComment'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_r_script(self)


@dataclass
class RPackage(RNode):
    """R package definition"""
    r_node_type: RNodeType = RNodeType.PACKAGE
    name: str = ""
    version: str = ""
    functions: List['RFunctionDefinition'] = field(default_factory=list)
    data: List[RNode] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_r_package(self)


# ============================================================================
# Functions
# ============================================================================

@dataclass
class RFunctionDefinition(RNode):
    """Function definition: function(x, y = 1) { x + y }"""
    r_node_type: RNodeType = RNodeType.FUNCTION_DEFINITION
    parameters: List['RParameter'] = field(default_factory=list)
    body: List[RNode] = field(default_factory=list)
    environment: Optional[str] = None
    
    def accept(self, visitor):
        return visitor.visit_r_function_definition(self)


@dataclass
class RParameter(RNode):
    """Function parameter: x, y = default"""
    name: str = ""
    default_value: Optional[RNode] = None
    is_ellipsis: bool = False  # For ... parameter
    
    def accept(self, visitor):
        return visitor.visit_r_parameter(self)


@dataclass
class RFunctionCall(RNode):
    """Function call: func(arg1, arg2, name = value)"""
    r_node_type: RNodeType = RNodeType.FUNCTION_CALL
    function: RNode = None
    arguments: List['RArgument'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_r_function_call(self)


@dataclass
class RArgument(RNode):
    """Function argument: positional or named"""
    name: Optional[str] = None  # None for positional arguments
    value: RNode = None
    
    def accept(self, visitor):
        return visitor.visit_r_argument(self)


@dataclass
class RMethodCall(RNode):
    """Method call for S3/S4/R6: object$method(args)"""
    r_node_type: RNodeType = RNodeType.METHOD_CALL
    object: RNode = None
    method_name: str = ""
    arguments: List[RArgument] = field(default_factory=list)
    method_type: str = "S3"  # S3, S4, or R6
    
    def accept(self, visitor):
        return visitor.visit_r_method_call(self)


# ============================================================================
# Variables and Assignment
# ============================================================================

@dataclass
class RIdentifier(RNode):
    """Identifier: variable_name"""
    r_node_type: RNodeType = RNodeType.IDENTIFIER
    name: str = ""
    
    def accept(self, visitor):
        return visitor.visit_r_identifier(self)


@dataclass
class RAssignment(RNode):
    """Assignment: x <- value, x = value, value -> x"""
    r_node_type: RNodeType = RNodeType.ASSIGNMENT
    target: RNode = None
    value: RNode = None
    operator: ROperator = ROperator.ASSIGN
    
    def accept(self, visitor):
        return visitor.visit_r_assignment(self)


# ============================================================================
# Data Structures
# ============================================================================

@dataclass
class RVector(RNode):
    """Vector: c(1, 2, 3) or 1:10"""
    r_node_type: RNodeType = RNodeType.VECTOR
    elements: List[RNode] = field(default_factory=list)
    is_sequence: bool = False  # True for 1:10 syntax
    
    def accept(self, visitor):
        return visitor.visit_r_vector(self)


@dataclass
class RList(RNode):
    """List: list(a = 1, b = 2)"""
    r_node_type: RNodeType = RNodeType.LIST
    elements: List['RListElement'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_r_list(self)


@dataclass
class RListElement(RNode):
    """List element with optional name"""
    name: Optional[str] = None
    value: RNode = None
    
    def accept(self, visitor):
        return visitor.visit_r_list_element(self)


@dataclass
class RDataFrame(RNode):
    """Data frame: data.frame(x = 1:3, y = c('a', 'b', 'c'))"""
    r_node_type: RNodeType = RNodeType.DATA_FRAME
    columns: List['RDataFrameColumn'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_r_data_frame(self)


@dataclass
class RDataFrameColumn(RNode):
    """Data frame column"""
    name: str = ""
    values: RNode = None
    
    def accept(self, visitor):
        return visitor.visit_r_data_frame_column(self)


@dataclass
class RMatrix(RNode):
    """Matrix: matrix(1:6, nrow = 2, ncol = 3)"""
    r_node_type: RNodeType = RNodeType.MATRIX
    data: RNode = None
    nrow: Optional[RNode] = None
    ncol: Optional[RNode] = None
    byrow: bool = False
    
    def accept(self, visitor):
        return visitor.visit_r_matrix(self)


@dataclass
class RArray(RNode):
    """Array: array(1:24, dim = c(2, 3, 4))"""
    r_node_type: RNodeType = RNodeType.ARRAY
    data: RNode = None
    dimensions: RNode = None
    
    def accept(self, visitor):
        return visitor.visit_r_array(self)


@dataclass
class RFactor(RNode):
    """Factor: factor(c('low', 'medium', 'high'))"""
    r_node_type: RNodeType = RNodeType.FACTOR
    values: RNode = None
    levels: Optional[RNode] = None
    ordered: bool = False
    
    def accept(self, visitor):
        return visitor.visit_r_factor(self)


# ============================================================================
# Literals and Expressions
# ============================================================================

@dataclass
class RLiteralExpression(RNode):
    """Base class for literal expressions"""
    r_node_type: RNodeType = RNodeType.LITERAL_EXPRESSION
    value: Any = None
    
    def accept(self, visitor):
        return visitor.visit_r_literal_expression(self)


@dataclass
class RNumericLiteral(RLiteralExpression):
    """Numeric literal: 42, 3.14, 1e-5"""
    r_node_type: RNodeType = RNodeType.NUMERIC_LITERAL
    value: Union[int, float] = 0
    is_integer: bool = False
    
    def accept(self, visitor):
        return visitor.visit_r_numeric_literal(self)


@dataclass
class RStringLiteral(RLiteralExpression):
    """String literal: 'hello' or "world" """
    r_node_type: RNodeType = RNodeType.STRING_LITERAL
    value: str = ""
    quote_type: str = "single"  # "single" or "double"
    
    def accept(self, visitor):
        return visitor.visit_r_string_literal(self)


@dataclass
class RLogicalLiteral(RLiteralExpression):
    """Logical literal: TRUE, FALSE"""
    r_node_type: RNodeType = RNodeType.LOGICAL_LITERAL
    value: bool = False
    
    def accept(self, visitor):
        return visitor.visit_r_logical_literal(self)


@dataclass
class RNullLiteral(RLiteralExpression):
    """NULL literal"""
    r_node_type: RNodeType = RNodeType.NULL_LITERAL
    
    def accept(self, visitor):
        return visitor.visit_r_null_literal(self)


@dataclass
class RNALiteral(RLiteralExpression):
    """NA literal: NA, NA_integer_, NA_real_, NA_character_, NA_complex_"""
    r_node_type: RNodeType = RNodeType.NA_LITERAL
    na_type: str = "NA"  # NA, NA_integer_, etc.
    
    def accept(self, visitor):
        return visitor.visit_r_na_literal(self)


@dataclass
class RBinaryExpression(RNode):
    """Binary expression: x + y, a %in% b"""
    r_node_type: RNodeType = RNodeType.BINARY_EXPRESSION
    left: RNode = None
    operator: ROperator = ROperator.PLUS
    right: RNode = None
    
    def accept(self, visitor):
        return visitor.visit_r_binary_expression(self)


@dataclass
class RUnaryExpression(RNode):
    """Unary expression: -x, !flag"""
    r_node_type: RNodeType = RNodeType.UNARY_EXPRESSION
    operator: ROperator = ROperator.MINUS
    expression: RNode = None
    
    def accept(self, visitor):
        return visitor.visit_r_unary_expression(self)


# ============================================================================
# Indexing and Subsetting
# ============================================================================

@dataclass
class RIndexExpression(RNode):
    """Index expression: x[i], x[i, j], x[[i]]"""
    r_node_type: RNodeType = RNodeType.INDEX_EXPRESSION
    object: RNode = None
    indices: List[RNode] = field(default_factory=list)
    is_double_bracket: bool = False  # True for [[ ]]
    
    def accept(self, visitor):
        return visitor.visit_r_index_expression(self)


@dataclass
class RSubsetExpression(RNode):
    """Subset expression with conditions: x[x > 0]"""
    r_node_type: RNodeType = RNodeType.SUBSET_EXPRESSION
    object: RNode = None
    condition: RNode = None
    
    def accept(self, visitor):
        return visitor.visit_r_subset_expression(self)


@dataclass
class RMemberAccess(RNode):
    """Member access: object$member"""
    r_node_type: RNodeType = RNodeType.MEMBER_ACCESS
    object: RNode = None
    member: str = ""
    
    def accept(self, visitor):
        return visitor.visit_r_member_access(self)


@dataclass
class RDollarAccess(RNode):
    """Dollar access: list$element"""
    r_node_type: RNodeType = RNodeType.DOLLAR_ACCESS
    object: RNode = None
    element: str = ""
    
    def accept(self, visitor):
        return visitor.visit_r_dollar_access(self)


@dataclass
class RAtAccess(RNode):
    """At access for S4 objects: object@slot"""
    r_node_type: RNodeType = RNodeType.AT_ACCESS
    object: RNode = None
    slot: str = ""
    
    def accept(self, visitor):
        return visitor.visit_r_at_access(self)


# ============================================================================
# Control Flow
# ============================================================================

@dataclass
class RIfStatement(RNode):
    """If statement: if (condition) expr1 else expr2"""
    r_node_type: RNodeType = RNodeType.IF_STATEMENT
    condition: RNode = None
    then_expr: RNode = None
    else_expr: Optional[RNode] = None
    
    def accept(self, visitor):
        return visitor.visit_r_if_statement(self)


@dataclass
class RForLoop(RNode):
    """For loop: for (var in iterable) expr"""
    r_node_type: RNodeType = RNodeType.FOR_LOOP
    variable: str = ""
    iterable: RNode = None
    body: RNode = None
    
    def accept(self, visitor):
        return visitor.visit_r_for_loop(self)


@dataclass
class RWhileLoop(RNode):
    """While loop: while (condition) expr"""
    r_node_type: RNodeType = RNodeType.WHILE_LOOP
    condition: RNode = None
    body: RNode = None
    
    def accept(self, visitor):
        return visitor.visit_r_while_loop(self)


@dataclass
class RRepeatLoop(RNode):
    """Repeat loop: repeat expr"""
    r_node_type: RNodeType = RNodeType.REPEAT_LOOP
    body: RNode = None
    
    def accept(self, visitor):
        return visitor.visit_r_repeat_loop(self)


@dataclass
class RNextStatement(RNode):
    """Next statement (continue): next"""
    r_node_type: RNodeType = RNodeType.NEXT_STATEMENT
    
    def accept(self, visitor):
        return visitor.visit_r_next_statement(self)


@dataclass
class RBreakStatement(RNode):
    """Break statement: break"""
    r_node_type: RNodeType = RNodeType.BREAK_STATEMENT
    
    def accept(self, visitor):
        return visitor.visit_r_break_statement(self)


@dataclass
class RReturnStatement(RNode):
    """Return statement: return(value)"""
    r_node_type: RNodeType = RNodeType.RETURN_STATEMENT
    value: Optional[RNode] = None
    
    def accept(self, visitor):
        return visitor.visit_r_return_statement(self)


# ============================================================================
# Special Constructs
# ============================================================================

@dataclass
class RFormula(RNode):
    """Formula: y ~ x + z"""
    r_node_type: RNodeType = RNodeType.FORMULA
    left: Optional[RNode] = None  # Response variable (optional)
    right: RNode = None  # Predictor expression
    
    def accept(self, visitor):
        return visitor.visit_r_formula(self)


@dataclass
class RHelpExpression(RNode):
    """Help expression: ?function or help(function)"""
    r_node_type: RNodeType = RNodeType.HELP_EXPRESSION
    topic: str = ""
    is_question_mark: bool = True  # True for ?, False for help()
    
    def accept(self, visitor):
        return visitor.visit_r_help_expression(self)


@dataclass
class RNamespaceAccess(RNode):
    """Namespace access: package::function"""
    r_node_type: RNodeType = RNodeType.NAMESPACE_ACCESS
    package: str = ""
    function: str = ""
    is_internal: bool = False  # True for :::
    
    def accept(self, visitor):
        return visitor.visit_r_namespace_access(self)


@dataclass
class RPackageLoad(RNode):
    """Package loading: library(package) or require(package)"""
    r_node_type: RNodeType = RNodeType.PACKAGE_LOAD
    package_name: str = ""
    is_require: bool = False  # True for require(), False for library()
    character_only: bool = False
    
    def accept(self, visitor):
        return visitor.visit_r_package_load(self)


@dataclass
class RPipeExpression(RNode):
    """Pipe expression: x %>% f() %>% g()"""
    r_node_type: RNodeType = RNodeType.PIPE_EXPRESSION
    left: RNode = None
    right: RNode = None
    
    def accept(self, visitor):
        return visitor.visit_r_pipe_expression(self)


@dataclass
class RTildeExpression(RNode):
    """Tilde expression for formulas: ~ x + y"""
    r_node_type: RNodeType = RNodeType.TILDE_EXPRESSION
    expression: RNode = None
    
    def accept(self, visitor):
        return visitor.visit_r_tilde_expression(self)


# ============================================================================
# Object-Oriented Programming
# ============================================================================

@dataclass
class RS3Method(RNode):
    """S3 method definition"""
    r_node_type: RNodeType = RNodeType.S3_METHOD
    generic_name: str = ""
    class_name: str = ""
    function_def: RFunctionDefinition = None
    
    def accept(self, visitor):
        return visitor.visit_r_s3_method(self)


@dataclass
class RS4Class(RNode):
    """S4 class definition: setClass()"""
    r_node_type: RNodeType = RNodeType.S4_CLASS
    class_name: str = ""
    slots: List['RS4Slot'] = field(default_factory=list)
    contains: List[str] = field(default_factory=list)  # Inheritance
    
    def accept(self, visitor):
        return visitor.visit_r_s4_class(self)


@dataclass
class RS4Slot(RNode):
    """S4 class slot"""
    name: str = ""
    type: str = ""
    
    def accept(self, visitor):
        return visitor.visit_r_s4_slot(self)


@dataclass
class RS4Method(RNode):
    """S4 method definition: setMethod()"""
    r_node_type: RNodeType = RNodeType.S4_METHOD
    generic_name: str = ""
    signature: List[str] = field(default_factory=list)
    function_def: RFunctionDefinition = None
    
    def accept(self, visitor):
        return visitor.visit_r_s4_method(self)


@dataclass
class RR6Class(RNode):
    """R6 class definition"""
    r_node_type: RNodeType = RNodeType.R6_CLASS
    class_name: str = ""
    public: List[RNode] = field(default_factory=list)
    private: List[RNode] = field(default_factory=list)
    active: List[RNode] = field(default_factory=list)
    inherit: Optional[str] = None
    
    def accept(self, visitor):
        return visitor.visit_r_r6_class(self)


# ============================================================================
# Comments
# ============================================================================

@dataclass
class RComment(RNode):
    """Comment: # This is a comment"""
    r_node_type: RNodeType = RNodeType.COMMENT
    text: str = ""
    
    def accept(self, visitor):
        return visitor.visit_r_comment(self)


# ============================================================================
# Utility Functions
# ============================================================================

def create_r_identifier(name: str) -> RIdentifier:
    """Create an R identifier node."""
    return RIdentifier(name=name)


def create_r_numeric_literal(value: Union[int, float]) -> RNumericLiteral:
    """Create an R numeric literal node."""
    return RNumericLiteral(value=value, is_integer=isinstance(value, int))


def create_r_string_literal(value: str, quote_type: str = "single") -> RStringLiteral:
    """Create an R string literal node."""
    return RStringLiteral(value=value, quote_type=quote_type)


def create_r_logical_literal(value: bool) -> RLogicalLiteral:
    """Create an R logical literal node."""
    return RLogicalLiteral(value=value)


def create_r_vector(elements: List[RNode], is_sequence: bool = False) -> RVector:
    """Create an R vector node."""
    return RVector(elements=elements, is_sequence=is_sequence)


def create_r_assignment(target: RNode, value: RNode, operator: ROperator = ROperator.ASSIGN) -> RAssignment:
    """Create an R assignment node."""
    return RAssignment(target=target, value=value, operator=operator)


def create_r_function_call(function: RNode, arguments: List[RArgument]) -> RFunctionCall:
    """Create an R function call node."""
    return RFunctionCall(function=function, arguments=arguments)


def create_r_function_definition(parameters: List[RParameter], body: List[RNode]) -> RFunctionDefinition:
    """Create an R function definition node."""
    return RFunctionDefinition(parameters=parameters, body=body)


def create_r_binary_expression(left: RNode, operator: ROperator, right: RNode) -> RBinaryExpression:
    """Create an R binary expression node."""
    return RBinaryExpression(left=left, operator=operator, right=right)


def create_r_if_statement(condition: RNode, then_expr: RNode, else_expr: RNode = None) -> RIfStatement:
    """Create an R if statement node."""
    return RIfStatement(condition=condition, then_expr=then_expr, else_expr=else_expr)


def create_r_for_loop(variable: str, iterable: RNode, body: RNode) -> RForLoop:
    """Create an R for loop node."""
    return RForLoop(variable=variable, iterable=iterable, body=body)


def create_r_data_frame(columns: List[RDataFrameColumn]) -> RDataFrame:
    """Create an R data frame node."""
    return RDataFrame(columns=columns)


def create_r_formula(left: RNode, right: RNode) -> RFormula:
    """Create an R formula node."""
    return RFormula(left=left, right=right) 