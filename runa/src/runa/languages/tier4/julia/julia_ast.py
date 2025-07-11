#!/usr/bin/env python3
"""
Julia AST Node Definitions

Comprehensive Abstract Syntax Tree nodes for Julia language covering all Julia features
including multiple dispatch, metaprogramming, macros, types, modules, packages, 
broadcasting, vectorization, and scientific computing constructs.

This module provides complete AST representation for:
- Functions with multiple dispatch and method signatures
- Type system with parametric types, unions, and abstract types
- Modules and packages with namespace management
- Macros and metaprogramming with code generation
- Arrays and broadcasting operations
- Control flow with exception handling
- Structs and mutable/immutable types
- Coroutines and parallel computing
- Foreign function interface (FFI)
- String interpolation and symbols
"""

from typing import List, Optional, Any, Union, Dict
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod

from ....core.runa_ast import ASTNode, SourceLocation, TranslationMetadata


class JuliaNodeType(Enum):
    """Julia-specific AST node types."""
    # Module and package structure
    MODULE_DECLARATION = auto()
    IMPORT_DECLARATION = auto()
    USING_DECLARATION = auto()
    EXPORT_DECLARATION = auto()
    
    # Types
    TYPE_DECLARATION = auto()
    STRUCT_DECLARATION = auto()
    MUTABLE_STRUCT_DECLARATION = auto()
    ABSTRACT_TYPE_DECLARATION = auto()
    PRIMITIVE_TYPE_DECLARATION = auto()
    TYPE_ALIAS = auto()
    UNION_TYPE = auto()
    PARAMETRIC_TYPE = auto()
    WHERE_CLAUSE = auto()
    
    # Functions and methods
    FUNCTION_DECLARATION = auto()
    METHOD_DECLARATION = auto()
    FUNCTION_SIGNATURE = auto()
    PARAMETER_LIST = auto()
    PARAMETER = auto()
    KEYWORD_PARAMETER = auto()
    VARARGS_PARAMETER = auto()
    
    # Expressions
    IDENTIFIER = auto()
    LITERAL_EXPRESSION = auto()
    STRING_INTERPOLATION = auto()
    SYMBOL_EXPRESSION = auto()
    ARRAY_EXPRESSION = auto()
    TUPLE_EXPRESSION = auto()
    DICT_EXPRESSION = auto()
    RANGE_EXPRESSION = auto()
    COMPREHENSION = auto()
    GENERATOR_EXPRESSION = auto()
    BINARY_EXPRESSION = auto()
    UNARY_EXPRESSION = auto()
    CALL_EXPRESSION = auto()
    INDEX_EXPRESSION = auto()
    DOT_EXPRESSION = auto()
    BROADCAST_EXPRESSION = auto()
    ASSIGNMENT_EXPRESSION = auto()
    
    # Control flow
    IF_EXPRESSION = auto()
    TERNARY_EXPRESSION = auto()
    TRY_EXPRESSION = auto()
    LET_EXPRESSION = auto()
    BEGIN_BLOCK = auto()
    FOR_LOOP = auto()
    WHILE_LOOP = auto()
    BREAK_STATEMENT = auto()
    CONTINUE_STATEMENT = auto()
    RETURN_STATEMENT = auto()
    
    # Metaprogramming
    MACRO_DECLARATION = auto()
    MACRO_CALL = auto()
    QUOTE_EXPRESSION = auto()
    INTERPOLATION = auto()
    EVAL_EXPRESSION = auto()
    
    # Special constructs
    GLOBAL_DECLARATION = auto()
    LOCAL_DECLARATION = auto()
    CONST_DECLARATION = auto()
    BAREMODULE_DECLARATION = auto()
    
    # File structure
    FILE = auto()
    PROGRAM = auto()


class JuliaVisibility(Enum):
    """Julia visibility modifiers."""
    PUBLIC = "public"
    PRIVATE = "private"  # Not explicitly used in Julia but conceptually exists


class JuliaTypeKind(Enum):
    """Julia type kinds."""
    STRUCT = "struct"
    MUTABLE_STRUCT = "mutable struct"
    ABSTRACT_TYPE = "abstract type"
    PRIMITIVE_TYPE = "primitive type"


@dataclass
class JuliaNode(ASTNode):
    """Base class for all Julia AST nodes."""
    julia_node_type: JuliaNodeType = JuliaNodeType.PROGRAM
    
    @abstractmethod
    def accept(self, visitor):
        """Accept a visitor for AST traversal."""
        pass


# ============================================================================
# Module and Package System
# ============================================================================

@dataclass
class JuliaModuleDeclaration(JuliaNode):
    """Module declaration: module MyModule ... end"""
    julia_node_type: JuliaNodeType = JuliaNodeType.MODULE_DECLARATION
    name: str = ""
    body: List[JuliaNode] = field(default_factory=list)
    is_baremodule: bool = False
    
    def accept(self, visitor):
        return visitor.visit_julia_module_declaration(self)


@dataclass
class JuliaImportDeclaration(JuliaNode):
    """Import declaration: import Package, import Package: func"""
    julia_node_type: JuliaNodeType = JuliaNodeType.IMPORT_DECLARATION
    package: str = ""
    symbols: List[str] = field(default_factory=list)  # Empty means import all
    alias: Optional[str] = None
    
    def accept(self, visitor):
        return visitor.visit_julia_import_declaration(self)


@dataclass
class JuliaUsingDeclaration(JuliaNode):
    """Using declaration: using Package, using Package: func"""
    julia_node_type: JuliaNodeType = JuliaNodeType.USING_DECLARATION
    package: str = ""
    symbols: List[str] = field(default_factory=list)  # Empty means using all
    
    def accept(self, visitor):
        return visitor.visit_julia_using_declaration(self)


@dataclass
class JuliaExportDeclaration(JuliaNode):
    """Export declaration: export func1, func2"""
    julia_node_type: JuliaNodeType = JuliaNodeType.EXPORT_DECLARATION
    symbols: List[str] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_julia_export_declaration(self)


# ============================================================================
# Type System
# ============================================================================

@dataclass
class JuliaType(JuliaNode):
    """Base class for Julia type expressions."""
    pass


@dataclass
class JuliaTypeDeclaration(JuliaNode):
    """Base class for type declarations."""
    name: str = ""
    type_parameters: List['JuliaTypeParameter'] = field(default_factory=list)
    supertype: Optional[JuliaType] = None
    where_clauses: List['JuliaWhereClause'] = field(default_factory=list)


@dataclass
class JuliaStructDeclaration(JuliaTypeDeclaration):
    """Struct declaration: struct Point{T} x::T; y::T end"""
    julia_node_type: JuliaNodeType = JuliaNodeType.STRUCT_DECLARATION
    fields: List['JuliaFieldDeclaration'] = field(default_factory=list)
    is_mutable: bool = False
    
    def accept(self, visitor):
        return visitor.visit_julia_struct_declaration(self)


@dataclass
class JuliaAbstractTypeDeclaration(JuliaTypeDeclaration):
    """Abstract type declaration: abstract type Number{T} end"""
    julia_node_type: JuliaNodeType = JuliaNodeType.ABSTRACT_TYPE_DECLARATION
    
    def accept(self, visitor):
        return visitor.visit_julia_abstract_type_declaration(self)


@dataclass
class JuliaPrimitiveTypeDeclaration(JuliaTypeDeclaration):
    """Primitive type declaration: primitive type Float64 <: AbstractFloat 64 end"""
    julia_node_type: JuliaNodeType = JuliaNodeType.PRIMITIVE_TYPE_DECLARATION
    size_bits: int = 64
    
    def accept(self, visitor):
        return visitor.visit_julia_primitive_type_declaration(self)


@dataclass
class JuliaTypeAlias(JuliaNode):
    """Type alias: const Vector{T} = Array{T,1}"""
    julia_node_type: JuliaNodeType = JuliaNodeType.TYPE_ALIAS
    name: str = ""
    type_parameters: List['JuliaTypeParameter'] = field(default_factory=list)
    target_type: Optional[JuliaType] = None
    
    def accept(self, visitor):
        return visitor.visit_julia_type_alias(self)


@dataclass
class JuliaUnionType(JuliaType):
    """Union type: Union{Int, String}"""
    julia_node_type: JuliaNodeType = JuliaNodeType.UNION_TYPE
    types: List[JuliaType] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_julia_union_type(self)


@dataclass
class JuliaParametricType(JuliaType):
    """Parametric type: Array{T,N}"""
    julia_node_type: JuliaNodeType = JuliaNodeType.PARAMETRIC_TYPE
    base_type: str = ""
    parameters: List[JuliaType] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_julia_parametric_type(self)


@dataclass
class JuliaTypeParameter(JuliaNode):
    """Type parameter: T <: Number"""
    name: str = ""
    upper_bound: Optional[JuliaType] = None
    lower_bound: Optional[JuliaType] = None
    
    def accept(self, visitor):
        return visitor.visit_julia_type_parameter(self)


@dataclass
class JuliaWhereClause(JuliaNode):
    """Where clause: where T <: Number"""
    julia_node_type: JuliaNodeType = JuliaNodeType.WHERE_CLAUSE
    parameters: List[JuliaTypeParameter] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_julia_where_clause(self)


@dataclass
class JuliaFieldDeclaration(JuliaNode):
    """Struct field: name::Type"""
    name: str = ""
    type: Optional[JuliaType] = None
    default_value: Optional['JuliaExpression'] = None
    
    def accept(self, visitor):
        return visitor.visit_julia_field_declaration(self)


# ============================================================================
# Functions and Methods
# ============================================================================

@dataclass
class JuliaFunctionDeclaration(JuliaNode):
    """Function declaration: function f(x::T) where T ... end"""
    julia_node_type: JuliaNodeType = JuliaNodeType.FUNCTION_DECLARATION
    name: str = ""
    signature: Optional['JuliaFunctionSignature'] = None
    body: List[JuliaNode] = field(default_factory=list)
    return_type: Optional[JuliaType] = None
    where_clauses: List[JuliaWhereClause] = field(default_factory=list)
    is_short_form: bool = False  # f(x) = x + 1
    
    def accept(self, visitor):
        return visitor.visit_julia_function_declaration(self)


@dataclass
class JuliaMethodDeclaration(JuliaNode):
    """Method declaration (specific to multiple dispatch)"""
    julia_node_type: JuliaNodeType = JuliaNodeType.METHOD_DECLARATION
    function_name: str = ""
    signature: Optional['JuliaFunctionSignature'] = None
    body: List[JuliaNode] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_julia_method_declaration(self)


@dataclass
class JuliaFunctionSignature(JuliaNode):
    """Function signature with parameters"""
    julia_node_type: JuliaNodeType = JuliaNodeType.FUNCTION_SIGNATURE
    parameters: List['JuliaParameter'] = field(default_factory=list)
    keyword_parameters: List['JuliaKeywordParameter'] = field(default_factory=list)
    varargs: Optional['JuliaVarargsParameter'] = None
    
    def accept(self, visitor):
        return visitor.visit_julia_function_signature(self)


@dataclass
class JuliaParameter(JuliaNode):
    """Function parameter: x::Type"""
    julia_node_type: JuliaNodeType = JuliaNodeType.PARAMETER
    name: str = ""
    type: Optional[JuliaType] = None
    default_value: Optional['JuliaExpression'] = None
    
    def accept(self, visitor):
        return visitor.visit_julia_parameter(self)


@dataclass
class JuliaKeywordParameter(JuliaNode):
    """Keyword parameter: x=default"""
    julia_node_type: JuliaNodeType = JuliaNodeType.KEYWORD_PARAMETER
    name: str = ""
    type: Optional[JuliaType] = None
    default_value: Optional['JuliaExpression'] = None
    
    def accept(self, visitor):
        return visitor.visit_julia_keyword_parameter(self)


@dataclass
class JuliaVarargsParameter(JuliaNode):
    """Varargs parameter: args..."""
    julia_node_type: JuliaNodeType = JuliaNodeType.VARARGS_PARAMETER
    name: str = ""
    type: Optional[JuliaType] = None
    
    def accept(self, visitor):
        return visitor.visit_julia_varargs_parameter(self)


# ============================================================================
# Expressions
# ============================================================================

@dataclass
class JuliaExpression(JuliaNode):
    """Base class for Julia expressions."""
    pass


@dataclass
class JuliaIdentifier(JuliaExpression):
    """Identifier: variable_name"""
    julia_node_type: JuliaNodeType = JuliaNodeType.IDENTIFIER
    name: str = ""
    
    def accept(self, visitor):
        return visitor.visit_julia_identifier(self)


@dataclass
class JuliaLiteralExpression(JuliaExpression):
    """Literal expression: 42, 3.14, true, "hello" """
    julia_node_type: JuliaNodeType = JuliaNodeType.LITERAL_EXPRESSION
    value: Any = None
    literal_type: str = "string"  # int, float, string, boolean, char, nothing
    
    def accept(self, visitor):
        return visitor.visit_julia_literal_expression(self)


@dataclass
class JuliaStringInterpolation(JuliaExpression):
    """String interpolation: "Hello $name" """
    julia_node_type: JuliaNodeType = JuliaNodeType.STRING_INTERPOLATION
    parts: List[Union[str, JuliaExpression]] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_julia_string_interpolation(self)


@dataclass
class JuliaSymbolExpression(JuliaExpression):
    """Symbol expression: :symbol"""
    julia_node_type: JuliaNodeType = JuliaNodeType.SYMBOL_EXPRESSION
    name: str = ""
    
    def accept(self, visitor):
        return visitor.visit_julia_symbol_expression(self)


@dataclass
class JuliaArrayExpression(JuliaExpression):
    """Array expression: [1, 2, 3]"""
    julia_node_type: JuliaNodeType = JuliaNodeType.ARRAY_EXPRESSION
    elements: List[JuliaExpression] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_julia_array_expression(self)


@dataclass
class JuliaTupleExpression(JuliaExpression):
    """Tuple expression: (1, 2, 3)"""
    julia_node_type: JuliaNodeType = JuliaNodeType.TUPLE_EXPRESSION
    elements: List[JuliaExpression] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_julia_tuple_expression(self)


@dataclass
class JuliaDictExpression(JuliaExpression):
    """Dictionary expression: Dict("a" => 1, "b" => 2)"""
    julia_node_type: JuliaNodeType = JuliaNodeType.DICT_EXPRESSION
    pairs: List[tuple[JuliaExpression, JuliaExpression]] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_julia_dict_expression(self)


@dataclass
class JuliaRangeExpression(JuliaExpression):
    """Range expression: 1:5, 1:2:10"""
    julia_node_type: JuliaNodeType = JuliaNodeType.RANGE_EXPRESSION
    start: Optional[JuliaExpression] = None
    step: Optional[JuliaExpression] = None
    stop: Optional[JuliaExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_julia_range_expression(self)


@dataclass
class JuliaComprehension(JuliaExpression):
    """Array comprehension: [x^2 for x in 1:10 if x % 2 == 0]"""
    julia_node_type: JuliaNodeType = JuliaNodeType.COMPREHENSION
    expression: Optional[JuliaExpression] = None
    generators: List['JuliaGenerator'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_julia_comprehension(self)


@dataclass
class JuliaGenerator(JuliaNode):
    """Generator in comprehension: x in 1:10 if x % 2 == 0"""
    variable: str = ""
    iterable: Optional[JuliaExpression] = None
    condition: Optional[JuliaExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_julia_generator(self)


@dataclass
class JuliaBinaryExpression(JuliaExpression):
    """Binary expression: a + b, a && b"""
    julia_node_type: JuliaNodeType = JuliaNodeType.BINARY_EXPRESSION
    left: Optional[JuliaExpression] = None
    operator: str = ""
    right: Optional[JuliaExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_julia_binary_expression(self)


@dataclass
class JuliaUnaryExpression(JuliaExpression):
    """Unary expression: -x, !flag"""
    julia_node_type: JuliaNodeType = JuliaNodeType.UNARY_EXPRESSION
    operator: str = ""
    expression: Optional[JuliaExpression] = None
    is_postfix: bool = False
    
    def accept(self, visitor):
        return visitor.visit_julia_unary_expression(self)


@dataclass
class JuliaCallExpression(JuliaExpression):
    """Function call: f(x, y; z=3)"""
    julia_node_type: JuliaNodeType = JuliaNodeType.CALL_EXPRESSION
    function: Optional[JuliaExpression] = None
    arguments: List[JuliaExpression] = field(default_factory=list)
    keyword_arguments: Dict[str, JuliaExpression] = field(default_factory=dict)
    
    def accept(self, visitor):
        return visitor.visit_julia_call_expression(self)


@dataclass
class JuliaIndexExpression(JuliaExpression):
    """Array indexing: a[i], a[i, j]"""
    julia_node_type: JuliaNodeType = JuliaNodeType.INDEX_EXPRESSION
    object: Optional[JuliaExpression] = None
    indices: List[JuliaExpression] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_julia_index_expression(self)


@dataclass
class JuliaDotExpression(JuliaExpression):
    """Dot access: obj.field"""
    julia_node_type: JuliaNodeType = JuliaNodeType.DOT_EXPRESSION
    object: Optional[JuliaExpression] = None
    field: str = ""
    
    def accept(self, visitor):
        return visitor.visit_julia_dot_expression(self)


@dataclass
class JuliaBroadcastExpression(JuliaExpression):
    """Broadcasting: f.(x), a .+ b"""
    julia_node_type: JuliaNodeType = JuliaNodeType.BROADCAST_EXPRESSION
    function: Optional[JuliaExpression] = None
    arguments: List[JuliaExpression] = field(default_factory=list)
    operator: Optional[str] = None  # For broadcast operators like .+
    
    def accept(self, visitor):
        return visitor.visit_julia_broadcast_expression(self)


@dataclass
class JuliaAssignmentExpression(JuliaExpression):
    """Assignment: x = y, x += y"""
    julia_node_type: JuliaNodeType = JuliaNodeType.ASSIGNMENT_EXPRESSION
    target: Optional[JuliaExpression] = None
    operator: str = "="
    value: Optional[JuliaExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_julia_assignment_expression(self)


# ============================================================================
# Control Flow
# ============================================================================

@dataclass
class JuliaIfExpression(JuliaExpression):
    """If expression: if condition expr1 else expr2 end"""
    julia_node_type: JuliaNodeType = JuliaNodeType.IF_EXPRESSION
    condition: Optional[JuliaExpression] = None
    then_body: List[JuliaNode] = field(default_factory=list)
    elseif_clauses: List['JuliaElseifClause'] = field(default_factory=list)
    else_body: List[JuliaNode] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_julia_if_expression(self)


@dataclass
class JuliaElseifClause(JuliaNode):
    """Elseif clause: elseif condition ... """
    condition: Optional[JuliaExpression] = None
    body: List[JuliaNode] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_julia_elseif_clause(self)


@dataclass
class JuliaTernaryExpression(JuliaExpression):
    """Ternary expression: condition ? expr1 : expr2"""
    julia_node_type: JuliaNodeType = JuliaNodeType.TERNARY_EXPRESSION
    condition: Optional[JuliaExpression] = None
    true_expression: Optional[JuliaExpression] = None
    false_expression: Optional[JuliaExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_julia_ternary_expression(self)


@dataclass
class JuliaTryExpression(JuliaExpression):
    """Try expression: try ... catch e ... finally ... end"""
    julia_node_type: JuliaNodeType = JuliaNodeType.TRY_EXPRESSION
    try_body: List[JuliaNode] = field(default_factory=list)
    catch_clauses: List['JuliaCatchClause'] = field(default_factory=list)
    finally_body: List[JuliaNode] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_julia_try_expression(self)


@dataclass
class JuliaCatchClause(JuliaNode):
    """Catch clause: catch e::Exception"""
    variable: Optional[str] = None
    exception_type: Optional[JuliaType] = None
    body: List[JuliaNode] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_julia_catch_clause(self)


@dataclass
class JuliaLetExpression(JuliaExpression):
    """Let expression: let x = 1, y = 2; ... end"""
    julia_node_type: JuliaNodeType = JuliaNodeType.LET_EXPRESSION
    bindings: List[JuliaAssignmentExpression] = field(default_factory=list)
    body: List[JuliaNode] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_julia_let_expression(self)


@dataclass
class JuliaBeginBlock(JuliaExpression):
    """Begin block: begin ... end"""
    julia_node_type: JuliaNodeType = JuliaNodeType.BEGIN_BLOCK
    body: List[JuliaNode] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_julia_begin_block(self)


@dataclass
class JuliaForLoop(JuliaNode):
    """For loop: for i in 1:10 ... end"""
    julia_node_type: JuliaNodeType = JuliaNodeType.FOR_LOOP
    variable: str = ""
    iterable: Optional[JuliaExpression] = None
    body: List[JuliaNode] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_julia_for_loop(self)


@dataclass
class JuliaWhileLoop(JuliaNode):
    """While loop: while condition ... end"""
    julia_node_type: JuliaNodeType = JuliaNodeType.WHILE_LOOP
    condition: Optional[JuliaExpression] = None
    body: List[JuliaNode] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_julia_while_loop(self)


@dataclass
class JuliaReturnStatement(JuliaNode):
    """Return statement: return expr"""
    julia_node_type: JuliaNodeType = JuliaNodeType.RETURN_STATEMENT
    expression: Optional[JuliaExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_julia_return_statement(self)


@dataclass
class JuliaBreakStatement(JuliaNode):
    """Break statement: break"""
    julia_node_type: JuliaNodeType = JuliaNodeType.BREAK_STATEMENT
    
    def accept(self, visitor):
        return visitor.visit_julia_break_statement(self)


@dataclass
class JuliaContinueStatement(JuliaNode):
    """Continue statement: continue"""
    julia_node_type: JuliaNodeType = JuliaNodeType.CONTINUE_STATEMENT
    
    def accept(self, visitor):
        return visitor.visit_julia_continue_statement(self)


# ============================================================================
# Metaprogramming
# ============================================================================

@dataclass
class JuliaMacroDeclaration(JuliaNode):
    """Macro declaration: macro mymacro(expr) ... end"""
    julia_node_type: JuliaNodeType = JuliaNodeType.MACRO_DECLARATION
    name: str = ""
    parameters: List[JuliaParameter] = field(default_factory=list)
    body: List[JuliaNode] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_julia_macro_declaration(self)


@dataclass
class JuliaMacroCall(JuliaExpression):
    """Macro call: @mymacro expr"""
    julia_node_type: JuliaNodeType = JuliaNodeType.MACRO_CALL
    macro_name: str = ""
    arguments: List[JuliaExpression] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_julia_macro_call(self)


@dataclass
class JuliaQuoteExpression(JuliaExpression):
    """Quote expression: quote ... end or :(expr)"""
    julia_node_type: JuliaNodeType = JuliaNodeType.QUOTE_EXPRESSION
    body: List[JuliaNode] = field(default_factory=list)
    is_short_form: bool = False  # :(expr) vs quote ... end
    
    def accept(self, visitor):
        return visitor.visit_julia_quote_expression(self)


@dataclass
class JuliaInterpolation(JuliaExpression):
    """Interpolation in quote: $expr"""
    julia_node_type: JuliaNodeType = JuliaNodeType.INTERPOLATION
    expression: Optional[JuliaExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_julia_interpolation(self)


# ============================================================================
# Special Declarations
# ============================================================================

@dataclass
class JuliaGlobalDeclaration(JuliaNode):
    """Global declaration: global x"""
    julia_node_type: JuliaNodeType = JuliaNodeType.GLOBAL_DECLARATION
    variables: List[str] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_julia_global_declaration(self)


@dataclass
class JuliaLocalDeclaration(JuliaNode):
    """Local declaration: local x"""
    julia_node_type: JuliaNodeType = JuliaNodeType.LOCAL_DECLARATION
    variables: List[str] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_julia_local_declaration(self)


@dataclass
class JuliaConstDeclaration(JuliaNode):
    """Const declaration: const x = 42"""
    julia_node_type: JuliaNodeType = JuliaNodeType.CONST_DECLARATION
    name: str = ""
    value: Optional[JuliaExpression] = None
    type: Optional[JuliaType] = None
    
    def accept(self, visitor):
        return visitor.visit_julia_const_declaration(self)


# ============================================================================
# File Structure
# ============================================================================

@dataclass
class JuliaFile(JuliaNode):
    """Julia source file"""
    julia_node_type: JuliaNodeType = JuliaNodeType.FILE
    module_declaration: Optional[JuliaModuleDeclaration] = None
    imports: List[Union[JuliaImportDeclaration, JuliaUsingDeclaration]] = field(default_factory=list)
    exports: List[JuliaExportDeclaration] = field(default_factory=list)
    declarations: List[JuliaNode] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_julia_file(self)


@dataclass
class JuliaProgram(JuliaNode):
    """Complete Julia program"""
    julia_node_type: JuliaNodeType = JuliaNodeType.PROGRAM
    files: List[JuliaFile] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_julia_program(self)


# ============================================================================
# Utility Functions
# ============================================================================

def create_julia_identifier(name: str) -> JuliaIdentifier:
    """Create a Julia identifier node."""
    return JuliaIdentifier(name=name)


def create_julia_literal(value: Any, literal_type: str = "string") -> JuliaLiteralExpression:
    """Create a Julia literal expression node."""
    return JuliaLiteralExpression(value=value, literal_type=literal_type)


def create_julia_struct(name: str, is_mutable: bool = False) -> JuliaStructDeclaration:
    """Create a Julia struct declaration node."""
    return JuliaStructDeclaration(name=name, is_mutable=is_mutable)


def create_julia_function(name: str) -> JuliaFunctionDeclaration:
    """Create a Julia function declaration node."""
    return JuliaFunctionDeclaration(name=name)


def create_julia_module(name: str, is_baremodule: bool = False) -> JuliaModuleDeclaration:
    """Create a Julia module declaration node."""
    return JuliaModuleDeclaration(name=name, is_baremodule=is_baremodule)


def create_julia_array(elements: List[JuliaExpression]) -> JuliaArrayExpression:
    """Create a Julia array expression node."""
    return JuliaArrayExpression(elements=elements)


def create_julia_call(function: JuliaExpression, arguments: List[JuliaExpression]) -> JuliaCallExpression:
    """Create a Julia function call expression node."""
    return JuliaCallExpression(function=function, arguments=arguments) 