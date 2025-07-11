#!/usr/bin/env python3
"""
Go AST Node Definitions

Comprehensive Abstract Syntax Tree nodes for Go language covering all Go features
including packages, functions, structs, interfaces, goroutines, channels, slices,
maps, pointers, error handling, concurrency, and modern Go features.

This module provides complete AST representation for:
- Package declarations and imports
- Type system (basic types, structs, interfaces, pointers, slices, maps, channels)
- Functions and methods with multiple return values
- Control flow (if, for, switch, select, defer, go)
- Goroutines and channel operations
- Error handling patterns
- Type assertions and type switches
- Closures and function literals
- Embedded types and composition
- Constants and variables with type inference
"""

from typing import List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod

from ....core.runa_ast import ASTNode, SourceLocation, TranslationMetadata


class GoNodeType(Enum):
    """Go-specific AST node types."""
    # Package and imports
    PACKAGE_DECLARATION = auto()
    IMPORT_DECLARATION = auto()
    IMPORT_SPEC = auto()
    
    # Types
    BASIC_TYPE = auto()
    ARRAY_TYPE = auto()
    SLICE_TYPE = auto()
    STRUCT_TYPE = auto()
    POINTER_TYPE = auto()
    FUNCTION_TYPE = auto()
    INTERFACE_TYPE = auto()
    MAP_TYPE = auto()
    CHANNEL_TYPE = auto()
    TYPE_ASSERTION = auto()
    TYPE_SWITCH = auto()
    TYPE_SPEC = auto()
    
    # Declarations
    CONST_DECLARATION = auto()
    VAR_DECLARATION = auto()
    TYPE_DECLARATION = auto()
    FUNCTION_DECLARATION = auto()
    METHOD_DECLARATION = auto()
    
    # Statements
    EXPRESSION_STATEMENT = auto()
    ASSIGNMENT_STATEMENT = auto()
    SHORT_VAR_DECLARATION = auto()
    INC_DEC_STATEMENT = auto()
    IF_STATEMENT = auto()
    FOR_STATEMENT = auto()
    RANGE_STATEMENT = auto()
    SWITCH_STATEMENT = auto()
    TYPE_SWITCH_STATEMENT = auto()
    SELECT_STATEMENT = auto()
    DEFER_STATEMENT = auto()
    GO_STATEMENT = auto()
    RETURN_STATEMENT = auto()
    BREAK_STATEMENT = auto()
    CONTINUE_STATEMENT = auto()
    GOTO_STATEMENT = auto()
    FALLTHROUGH_STATEMENT = auto()
    BLOCK_STATEMENT = auto()
    LABELED_STATEMENT = auto()
    
    # Expressions
    IDENTIFIER = auto()
    BASIC_LITERAL = auto()
    COMPOSITE_LITERAL = auto()
    FUNCTION_LITERAL = auto()
    UNARY_EXPRESSION = auto()
    BINARY_EXPRESSION = auto()
    CALL_EXPRESSION = auto()
    INDEX_EXPRESSION = auto()
    SLICE_EXPRESSION = auto()
    SELECTOR_EXPRESSION = auto()
    STAR_EXPRESSION = auto()
    TYPE_ASSERTION_EXPRESSION = auto()
    PAREN_EXPRESSION = auto()
    
    # Channel operations
    SEND_STATEMENT = auto()
    RECEIVE_EXPRESSION = auto()
    
    # Struct and interface elements
    FIELD = auto()
    METHOD_SPEC = auto()
    
    # Switch/Select cases
    CASE_CLAUSE = auto()
    COMM_CLAUSE = auto()
    
    # Misc
    FILE = auto()
    PROGRAM = auto()


@dataclass
class GoNode(ASTNode):
    """Base class for all Go AST nodes."""
    go_node_type: GoNodeType = GoNodeType.PROGRAM
    
    @abstractmethod
    def accept(self, visitor):
        """Accept a visitor for AST traversal."""
        pass


# ============================================================================
# Package and Import Declarations
# ============================================================================

@dataclass
class GoPackageDeclaration(GoNode):
    """Package declaration: package main"""
    go_node_type: GoNodeType = GoNodeType.PACKAGE_DECLARATION
    name: str = ""
    
    def accept(self, visitor):
        return visitor.visit_go_package_declaration(self)


@dataclass
class GoImportSpec(GoNode):
    """Import specification within import declaration."""
    go_node_type: GoNodeType = GoNodeType.IMPORT_SPEC
    name: Optional[str] = None  # Package alias or . for dot import
    path: str = ""  # Import path string
    
    def accept(self, visitor):
        return visitor.visit_go_import_spec(self)


@dataclass
class GoImportDeclaration(GoNode):
    """Import declaration: import "fmt" or import ( ... )"""
    go_node_type: GoNodeType = GoNodeType.IMPORT_DECLARATION
    specs: List[GoImportSpec] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_go_import_declaration(self)


# ============================================================================
# Type System
# ============================================================================

@dataclass
class GoType(GoNode):
    """Base class for Go type expressions."""
    pass


@dataclass
class GoBasicType(GoType):
    """Basic type: int, string, bool, etc."""
    go_node_type: GoNodeType = GoNodeType.BASIC_TYPE
    name: str = ""
    
    def accept(self, visitor):
        return visitor.visit_go_basic_type(self)


@dataclass
class GoArrayType(GoType):
    """Array type: [10]int"""
    go_node_type: GoNodeType = GoNodeType.ARRAY_TYPE
    length: Optional['GoExpression'] = None  # None for slice
    element_type: Optional[GoType] = None
    
    def accept(self, visitor):
        return visitor.visit_go_array_type(self)


@dataclass
class GoSliceType(GoType):
    """Slice type: []int"""
    go_node_type: GoNodeType = GoNodeType.SLICE_TYPE
    element_type: Optional[GoType] = None
    
    def accept(self, visitor):
        return visitor.visit_go_slice_type(self)


@dataclass
class GoField(GoNode):
    """Struct field or function parameter."""
    go_node_type: GoNodeType = GoNodeType.FIELD
    names: List[str] = field(default_factory=list)  # Can be empty for embedded fields
    type: Optional[GoType] = None
    tag: Optional[str] = None  # Struct tag
    
    def accept(self, visitor):
        return visitor.visit_go_field(self)


@dataclass
class GoStructType(GoType):
    """Struct type: struct { ... }"""
    go_node_type: GoNodeType = GoNodeType.STRUCT_TYPE
    fields: List[GoField] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_go_struct_type(self)


@dataclass
class GoPointerType(GoType):
    """Pointer type: *int"""
    go_node_type: GoNodeType = GoNodeType.POINTER_TYPE
    base_type: Optional[GoType] = None
    
    def accept(self, visitor):
        return visitor.visit_go_pointer_type(self)


@dataclass
class GoFunctionType(GoType):
    """Function type: func(int, string) error"""
    go_node_type: GoNodeType = GoNodeType.FUNCTION_TYPE
    params: List[GoField] = field(default_factory=list)
    results: List[GoField] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_go_function_type(self)


@dataclass
class GoMethodSpec(GoNode):
    """Interface method specification."""
    go_node_type: GoNodeType = GoNodeType.METHOD_SPEC
    name: str = ""
    type: Optional[GoFunctionType] = None
    
    def accept(self, visitor):
        return visitor.visit_go_method_spec(self)


@dataclass
class GoInterfaceType(GoType):
    """Interface type: interface { ... }"""
    go_node_type: GoNodeType = GoNodeType.INTERFACE_TYPE
    methods: List[GoMethodSpec] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_go_interface_type(self)


@dataclass
class GoMapType(GoType):
    """Map type: map[string]int"""
    go_node_type: GoNodeType = GoNodeType.MAP_TYPE
    key_type: Optional[GoType] = None
    value_type: Optional[GoType] = None
    
    def accept(self, visitor):
        return visitor.visit_go_map_type(self)


class GoChannelDirection(Enum):
    """Channel direction."""
    SEND = auto()      # chan<-
    RECEIVE = auto()   # <-chan
    BIDIRECTIONAL = auto()  # chan


@dataclass
class GoChannelType(GoType):
    """Channel type: chan int, <-chan int, chan<- int"""
    go_node_type: GoNodeType = GoNodeType.CHANNEL_TYPE
    direction: GoChannelDirection = GoChannelDirection.BIDIRECTIONAL
    value_type: Optional[GoType] = None
    
    def accept(self, visitor):
        return visitor.visit_go_channel_type(self)


# ============================================================================
# Expressions
# ============================================================================

@dataclass
class GoExpression(GoNode):
    """Base class for Go expressions."""
    pass


@dataclass
class GoIdentifier(GoExpression):
    """Identifier: name"""
    go_node_type: GoNodeType = GoNodeType.IDENTIFIER
    name: str = ""
    
    def accept(self, visitor):
        return visitor.visit_go_identifier(self)


class GoBasicLiteralKind(Enum):
    """Basic literal kinds."""
    INT = auto()
    FLOAT = auto()
    IMAG = auto()
    CHAR = auto()
    STRING = auto()


@dataclass
class GoBasicLiteral(GoExpression):
    """Basic literal: 42, 3.14, "hello", 'c'"""
    go_node_type: GoNodeType = GoNodeType.BASIC_LITERAL
    kind: GoBasicLiteralKind = GoBasicLiteralKind.INT
    value: str = ""
    
    def accept(self, visitor):
        return visitor.visit_go_basic_literal(self)


@dataclass
class GoCompositeLiteral(GoExpression):
    """Composite literal: []int{1, 2, 3}, Point{x: 1, y: 2}"""
    go_node_type: GoNodeType = GoNodeType.COMPOSITE_LITERAL
    type: Optional[GoType] = None
    elements: List['GoExpression'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_go_composite_literal(self)


@dataclass
class GoFunctionLiteral(GoExpression):
    """Function literal (closure): func(x int) int { return x * 2 }"""
    go_node_type: GoNodeType = GoNodeType.FUNCTION_LITERAL
    type: Optional[GoFunctionType] = None
    body: Optional['GoBlockStatement'] = None
    
    def accept(self, visitor):
        return visitor.visit_go_function_literal(self)


class GoUnaryOperator(Enum):
    """Unary operators."""
    PLUS = "+"
    MINUS = "-"
    NOT = "!"
    XOR = "^"
    ADDR = "&"      # Address-of
    DEREF = "*"     # Dereference
    ARROW = "<-"    # Channel receive


@dataclass
class GoUnaryExpression(GoExpression):
    """Unary expression: -x, !flag, &ptr, <-ch"""
    go_node_type: GoNodeType = GoNodeType.UNARY_EXPRESSION
    operator: GoUnaryOperator = GoUnaryOperator.PLUS
    operand: Optional[GoExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_go_unary_expression(self)


class GoBinaryOperator(Enum):
    """Binary operators."""
    # Arithmetic
    ADD = "+"
    SUB = "-"
    MUL = "*"
    QUO = "/"
    REM = "%"
    
    # Bitwise
    AND = "&"
    OR = "|"
    XOR = "^"
    SHL = "<<"
    SHR = ">>"
    AND_NOT = "&^"
    
    # Comparison
    EQL = "=="
    NEQ = "!="
    LSS = "<"
    LEQ = "<="
    GTR = ">"
    GEQ = ">="
    
    # Logical
    LAND = "&&"
    LOR = "||"


@dataclass
class GoBinaryExpression(GoExpression):
    """Binary expression: x + y, a && b, x == y"""
    go_node_type: GoNodeType = GoNodeType.BINARY_EXPRESSION
    left: Optional[GoExpression] = None
    operator: GoBinaryOperator = GoBinaryOperator.ADD
    right: Optional[GoExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_go_binary_expression(self)


@dataclass
class GoCallExpression(GoExpression):
    """Function call: f(x, y), make([]int, 10)"""
    go_node_type: GoNodeType = GoNodeType.CALL_EXPRESSION
    function: Optional[GoExpression] = None
    args: List[GoExpression] = field(default_factory=list)
    ellipsis: bool = False  # For variadic calls: f(args...)
    
    def accept(self, visitor):
        return visitor.visit_go_call_expression(self)


@dataclass
class GoIndexExpression(GoExpression):
    """Index expression: a[i], m[key]"""
    go_node_type: GoNodeType = GoNodeType.INDEX_EXPRESSION
    expr: Optional[GoExpression] = None
    index: Optional[GoExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_go_index_expression(self)


@dataclass
class GoSliceExpression(GoExpression):
    """Slice expression: a[low:high], a[low:high:max]"""
    go_node_type: GoNodeType = GoNodeType.SLICE_EXPRESSION
    expr: Optional[GoExpression] = None
    low: Optional[GoExpression] = None
    high: Optional[GoExpression] = None
    max: Optional[GoExpression] = None  # For 3-index slices
    slice3: bool = False  # True for 3-index slice
    
    def accept(self, visitor):
        return visitor.visit_go_slice_expression(self)


@dataclass
class GoSelectorExpression(GoExpression):
    """Selector expression: obj.field, pkg.Func"""
    go_node_type: GoNodeType = GoNodeType.SELECTOR_EXPRESSION
    expr: Optional[GoExpression] = None
    selector: str = ""
    
    def accept(self, visitor):
        return visitor.visit_go_selector_expression(self)


@dataclass
class GoTypeAssertionExpression(GoExpression):
    """Type assertion: x.(T), x.(type)"""
    go_node_type: GoNodeType = GoNodeType.TYPE_ASSERTION_EXPRESSION
    expr: Optional[GoExpression] = None
    type: Optional[GoType] = None  # None for x.(type) in type switch
    
    def accept(self, visitor):
        return visitor.visit_go_type_assertion_expression(self)


@dataclass
class GoParenExpression(GoExpression):
    """Parenthesized expression: (x + y)"""
    go_node_type: GoNodeType = GoNodeType.PAREN_EXPRESSION
    expr: Optional[GoExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_go_paren_expression(self)


# ============================================================================
# Statements
# ============================================================================

@dataclass
class GoStatement(GoNode):
    """Base class for Go statements."""
    pass


@dataclass
class GoExpressionStatement(GoStatement):
    """Expression statement: f()"""
    go_node_type: GoNodeType = GoNodeType.EXPRESSION_STATEMENT
    expr: Optional[GoExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_go_expression_statement(self)


class GoAssignmentOperator(Enum):
    """Assignment operators."""
    ASSIGN = "="
    ADD_ASSIGN = "+="
    SUB_ASSIGN = "-="
    MUL_ASSIGN = "*="
    QUO_ASSIGN = "/="
    REM_ASSIGN = "%="
    AND_ASSIGN = "&="
    OR_ASSIGN = "|="
    XOR_ASSIGN = "^="
    SHL_ASSIGN = "<<="
    SHR_ASSIGN = ">>="
    AND_NOT_ASSIGN = "&^="


@dataclass
class GoAssignmentStatement(GoStatement):
    """Assignment statement: x = y, a, b = f()"""
    go_node_type: GoNodeType = GoNodeType.ASSIGNMENT_STATEMENT
    left: List[GoExpression] = field(default_factory=list)
    operator: GoAssignmentOperator = GoAssignmentOperator.ASSIGN
    right: List[GoExpression] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_go_assignment_statement(self)


@dataclass
class GoShortVarDeclaration(GoStatement):
    """Short variable declaration: x := 42, a, b := f()"""
    go_node_type: GoNodeType = GoNodeType.SHORT_VAR_DECLARATION
    left: List[GoExpression] = field(default_factory=list)
    right: List[GoExpression] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_go_short_var_declaration(self)


class GoIncDecOperator(Enum):
    """Increment/decrement operators."""
    INC = "++"
    DEC = "--"


@dataclass
class GoIncDecStatement(GoStatement):
    """Increment/decrement statement: x++, y--"""
    go_node_type: GoNodeType = GoNodeType.INC_DEC_STATEMENT
    expr: Optional[GoExpression] = None
    operator: GoIncDecOperator = GoIncDecOperator.INC
    
    def accept(self, visitor):
        return visitor.visit_go_inc_dec_statement(self)


@dataclass
class GoBlockStatement(GoStatement):
    """Block statement: { ... }"""
    go_node_type: GoNodeType = GoNodeType.BLOCK_STATEMENT
    statements: List[GoStatement] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_go_block_statement(self)


@dataclass
class GoIfStatement(GoStatement):
    """If statement: if init; cond { ... } else { ... }"""
    go_node_type: GoNodeType = GoNodeType.IF_STATEMENT
    init: Optional[GoStatement] = None  # Optional initialization statement
    condition: Optional[GoExpression] = None
    body: Optional[GoBlockStatement] = None
    else_stmt: Optional[GoStatement] = None  # Can be another if or block
    
    def accept(self, visitor):
        return visitor.visit_go_if_statement(self)


@dataclass
class GoForStatement(GoStatement):
    """For statement: for init; cond; post { ... }"""
    go_node_type: GoNodeType = GoNodeType.FOR_STATEMENT
    init: Optional[GoStatement] = None
    condition: Optional[GoExpression] = None
    post: Optional[GoStatement] = None
    body: Optional[GoBlockStatement] = None
    
    def accept(self, visitor):
        return visitor.visit_go_for_statement(self)


@dataclass
class GoRangeStatement(GoStatement):
    """Range statement: for key, value := range expr { ... }"""
    go_node_type: GoNodeType = GoNodeType.RANGE_STATEMENT
    key: Optional[GoExpression] = None
    value: Optional[GoExpression] = None
    assign_token: str = ":="  # ":=" or "="
    expr: Optional[GoExpression] = None
    body: Optional[GoBlockStatement] = None
    
    def accept(self, visitor):
        return visitor.visit_go_range_statement(self)


@dataclass
class GoCaseClause(GoNode):
    """Case clause in switch statement."""
    go_node_type: GoNodeType = GoNodeType.CASE_CLAUSE
    values: List[GoExpression] = field(default_factory=list)  # Empty for default
    body: List[GoStatement] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_go_case_clause(self)


@dataclass
class GoSwitchStatement(GoStatement):
    """Switch statement: switch init; tag { case ...: ... }"""
    go_node_type: GoNodeType = GoNodeType.SWITCH_STATEMENT
    init: Optional[GoStatement] = None
    tag: Optional[GoExpression] = None
    body: List[GoCaseClause] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_go_switch_statement(self)


@dataclass
class GoTypeSwitchStatement(GoStatement):
    """Type switch: switch x := v.(type) { case T: ... }"""
    go_node_type: GoNodeType = GoNodeType.TYPE_SWITCH_STATEMENT
    init: Optional[GoStatement] = None
    assign: Optional[GoAssignmentStatement] = None  # x := v.(type)
    body: List[GoCaseClause] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_go_type_switch_statement(self)


@dataclass
class GoCommClause(GoNode):
    """Communication clause in select statement."""
    go_node_type: GoNodeType = GoNodeType.COMM_CLAUSE
    comm: Optional[GoStatement] = None  # Send/receive or assignment with receive
    body: List[GoStatement] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_go_comm_clause(self)


@dataclass
class GoSelectStatement(GoStatement):
    """Select statement: select { case <-ch: ... }"""
    go_node_type: GoNodeType = GoNodeType.SELECT_STATEMENT
    body: List[GoCommClause] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_go_select_statement(self)


@dataclass
class GoDeferStatement(GoStatement):
    """Defer statement: defer f()"""
    go_node_type: GoNodeType = GoNodeType.DEFER_STATEMENT
    call: Optional[GoCallExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_go_defer_statement(self)


@dataclass
class GoGoStatement(GoStatement):
    """Go statement (goroutine): go f()"""
    go_node_type: GoNodeType = GoNodeType.GO_STATEMENT
    call: Optional[GoCallExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_go_go_statement(self)


@dataclass
class GoReturnStatement(GoStatement):
    """Return statement: return, return x, return x, y"""
    go_node_type: GoNodeType = GoNodeType.RETURN_STATEMENT
    results: List[GoExpression] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_go_return_statement(self)


@dataclass
class GoBreakStatement(GoStatement):
    """Break statement: break, break label"""
    go_node_type: GoNodeType = GoNodeType.BREAK_STATEMENT
    label: Optional[str] = None
    
    def accept(self, visitor):
        return visitor.visit_go_break_statement(self)


@dataclass
class GoContinueStatement(GoStatement):
    """Continue statement: continue, continue label"""
    go_node_type: GoNodeType = GoNodeType.CONTINUE_STATEMENT
    label: Optional[str] = None
    
    def accept(self, visitor):
        return visitor.visit_go_continue_statement(self)


@dataclass
class GoGotoStatement(GoStatement):
    """Goto statement: goto label"""
    go_node_type: GoNodeType = GoNodeType.GOTO_STATEMENT
    label: str = ""
    
    def accept(self, visitor):
        return visitor.visit_go_goto_statement(self)


@dataclass
class GoFallthroughStatement(GoStatement):
    """Fallthrough statement in switch"""
    go_node_type: GoNodeType = GoNodeType.FALLTHROUGH_STATEMENT
    
    def accept(self, visitor):
        return visitor.visit_go_fallthrough_statement(self)


@dataclass
class GoLabeledStatement(GoStatement):
    """Labeled statement: label: stmt"""
    go_node_type: GoNodeType = GoNodeType.LABELED_STATEMENT
    label: str = ""
    stmt: Optional[GoStatement] = None
    
    def accept(self, visitor):
        return visitor.visit_go_labeled_statement(self)


@dataclass
class GoSendStatement(GoStatement):
    """Send statement: ch <- x"""
    go_node_type: GoNodeType = GoNodeType.SEND_STATEMENT
    channel: Optional[GoExpression] = None
    value: Optional[GoExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_go_send_statement(self)


# ============================================================================
# Declarations
# ============================================================================

@dataclass
class GoDeclaration(GoNode):
    """Base class for Go declarations."""
    pass


@dataclass
class GoValueSpec(GoNode):
    """Value specification in const/var declaration."""
    names: List[str] = field(default_factory=list)
    type: Optional[GoType] = None
    values: List[GoExpression] = field(default_factory=list)
    comment: Optional[str] = None
    
    def accept(self, visitor):
        return visitor.visit_go_value_spec(self)


@dataclass
class GoConstDeclaration(GoDeclaration):
    """Const declaration: const x = 42, const ( ... )"""
    go_node_type: GoNodeType = GoNodeType.CONST_DECLARATION
    specs: List[GoValueSpec] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_go_const_declaration(self)


@dataclass
class GoVarDeclaration(GoDeclaration):
    """Var declaration: var x int, var ( ... )"""
    go_node_type: GoNodeType = GoNodeType.VAR_DECLARATION
    specs: List[GoValueSpec] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_go_var_declaration(self)


@dataclass
class GoTypeSpec(GoNode):
    """Type specification in type declaration."""
    go_node_type: GoNodeType = GoNodeType.TYPE_SPEC
    name: str = ""
    type: Optional[GoType] = None
    comment: Optional[str] = None
    
    def accept(self, visitor):
        return visitor.visit_go_type_spec(self)


@dataclass
class GoTypeDeclaration(GoDeclaration):
    """Type declaration: type T int, type ( ... )"""
    go_node_type: GoNodeType = GoNodeType.TYPE_DECLARATION
    specs: List[GoTypeSpec] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_go_type_declaration(self)


@dataclass
class GoFunctionDeclaration(GoDeclaration):
    """Function declaration: func f(x int) int { ... }"""
    go_node_type: GoNodeType = GoNodeType.FUNCTION_DECLARATION
    name: str = ""
    type: Optional[GoFunctionType] = None
    body: Optional[GoBlockStatement] = None
    comment: Optional[str] = None
    
    def accept(self, visitor):
        return visitor.visit_go_function_declaration(self)


@dataclass
class GoMethodDeclaration(GoDeclaration):
    """Method declaration: func (r Receiver) Method() { ... }"""
    go_node_type: GoNodeType = GoNodeType.METHOD_DECLARATION
    receiver: Optional[GoField] = None
    name: str = ""
    type: Optional[GoFunctionType] = None
    body: Optional[GoBlockStatement] = None
    comment: Optional[str] = None
    
    def accept(self, visitor):
        return visitor.visit_go_method_declaration(self)


# ============================================================================
# File and Program Structure
# ============================================================================

@dataclass
class GoFile(GoNode):
    """Go source file."""
    go_node_type: GoNodeType = GoNodeType.FILE
    package: Optional[GoPackageDeclaration] = None
    imports: List[GoImportDeclaration] = field(default_factory=list)
    declarations: List[GoDeclaration] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_go_file(self)


@dataclass
class GoProgram(GoNode):
    """Complete Go program (collection of files/packages)."""
    go_node_type: GoNodeType = GoNodeType.PROGRAM
    files: List[GoFile] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_go_program(self)


# ============================================================================
# Utility Functions
# ============================================================================

def create_go_identifier(name: str) -> GoIdentifier:
    """Create a Go identifier node."""
    return GoIdentifier(name=name)


def create_go_basic_literal(kind: GoBasicLiteralKind, value: str) -> GoBasicLiteral:
    """Create a Go basic literal node."""
    return GoBasicLiteral(kind=kind, value=value)


def create_go_function_type(params: List[GoField] = None, results: List[GoField] = None) -> GoFunctionType:
    """Create a Go function type node."""
    return GoFunctionType(
        params=params or [],
        results=results or []
    )


def create_go_block_statement(statements: List[GoStatement] = None) -> GoBlockStatement:
    """Create a Go block statement node."""
    return GoBlockStatement(statements=statements or [])


def create_go_package_declaration(name: str) -> GoPackageDeclaration:
    """Create a Go package declaration node."""
    return GoPackageDeclaration(name=name)


def create_go_import_spec(path: str, name: str = None) -> GoImportSpec:
    """Create a Go import specification node."""
    return GoImportSpec(path=path, name=name)


# ============================================================================
# Constants and Built-ins
# ============================================================================

# Go built-in types
GO_BUILTIN_TYPES = {
    # Numeric types
    "int", "int8", "int16", "int32", "int64",
    "uint", "uint8", "uint16", "uint32", "uint64",
    "float32", "float64",
    "complex64", "complex128",
    "byte", "rune",
    
    # String and boolean
    "string", "bool",
    
    # Special types
    "error", "any",
    
    # Pointer types
    "uintptr", "unsafe.Pointer"
}

# Go built-in functions
GO_BUILTIN_FUNCTIONS = {
    "make", "new", "len", "cap", "append", "copy", "delete",
    "panic", "recover", "close", "real", "imag", "complex"
}

# Go keywords
GO_KEYWORDS = {
    "break", "case", "chan", "const", "continue", "default", "defer",
    "else", "fallthrough", "for", "func", "go", "goto", "if",
    "import", "interface", "map", "package", "range", "return",
    "select", "struct", "switch", "type", "var"
}

# Go operators
GO_OPERATORS = {
    "+", "-", "*", "/", "%", "&", "|", "^", "<<", ">>", "&^",
    "+=", "-=", "*=", "/=", "%=", "&=", "|=", "^=", "<<=", ">>=", "&^=",
    "&&", "||", "<-", "++", "--", "==", "<", ">", "=", "!", "!=", "<=", ">=",
    ":=", "...", "(", ")", "[", "]", "{", "}", ",", ";", ".", ":"
} 