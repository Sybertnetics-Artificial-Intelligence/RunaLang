#!/usr/bin/env python3
"""
Rust AST Node Definitions

Comprehensive Abstract Syntax Tree nodes for Rust language covering all Rust features
including structs, enums, traits, impl blocks, generics, lifetimes, ownership, borrowing,
pattern matching, async/await, macros, and advanced type system features.

This module provides complete AST representation for:
- Module system and use declarations
- Structs, enums, unions, and traits
- Functions and methods with generics and lifetimes
- Ownership, borrowing, and lifetime annotations
- Pattern matching and destructuring
- Async/await and futures
- Macro definitions and invocations
- Advanced type system (associated types, higher-ranked trait bounds)
- Unsafe code and FFI
- Attributes and derive macros

Author: Sybertnetics AI Solutions
License: MIT
"""

from typing import List, Optional, Any, Union, Dict
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod

from ....core.runa_ast import ASTNode, SourceLocation, TranslationMetadata


class RustNodeType(Enum):
    """Rust-specific AST node types."""
    # Module and imports
    CRATE = auto()
    MODULE = auto()
    USE_DECLARATION = auto()
    
    # Items
    FUNCTION = auto()
    STRUCT = auto()
    ENUM = auto()
    UNION = auto()
    TRAIT = auto()
    IMPL = auto()
    TYPE_ALIAS = auto()
    CONST = auto()
    STATIC = auto()
    EXTERN_CRATE = auto()
    EXTERN_BLOCK = auto()
    
    # Types
    TYPE_REFERENCE = auto()
    SLICE_TYPE = auto()
    ARRAY_TYPE = auto()
    TUPLE_TYPE = auto()
    FUNCTION_TYPE = auto()
    TRAIT_OBJECT = auto()
    IMPL_TRAIT = auto()
    NEVER_TYPE = auto()
    REFERENCE_TYPE = auto()
    POINTER_TYPE = auto()
    
    # Generics and lifetimes
    GENERIC_PARAM = auto()
    TYPE_PARAM = auto()
    LIFETIME_PARAM = auto()
    CONST_PARAM = auto()
    WHERE_CLAUSE = auto()
    LIFETIME = auto()
    
    # Expressions
    IDENTIFIER = auto()
    LITERAL = auto()
    PATH = auto()
    STRUCT_EXPRESSION = auto()
    TUPLE_EXPRESSION = auto()
    ARRAY_EXPRESSION = auto()
    INDEX_EXPRESSION = auto()
    CALL_EXPRESSION = auto()
    METHOD_CALL = auto()
    FIELD_ACCESS = auto()
    TRY_EXPRESSION = auto()
    AWAIT_EXPRESSION = auto()
    ASYNC_BLOCK = auto()
    CLOSURE = auto()
    IF_EXPRESSION = auto()
    MATCH_EXPRESSION = auto()
    LOOP_EXPRESSION = auto()
    WHILE_EXPRESSION = auto()
    FOR_EXPRESSION = auto()
    BREAK_EXPRESSION = auto()
    CONTINUE_EXPRESSION = auto()
    RETURN_EXPRESSION = auto()
    YIELD_EXPRESSION = auto()
    BECOME_EXPRESSION = auto()
    BLOCK_EXPRESSION = auto()
    UNSAFE_BLOCK = auto()
    CONST_BLOCK = auto()
    MACRO_CALL = auto()
    
    # Statements
    EXPRESSION_STATEMENT = auto()
    LET_STATEMENT = auto()
    ITEM_STATEMENT = auto()
    
    # Patterns
    IDENTIFIER_PATTERN = auto()
    WILDCARD_PATTERN = auto()
    REST_PATTERN = auto()
    LITERAL_PATTERN = auto()
    PATH_PATTERN = auto()
    STRUCT_PATTERN = auto()
    TUPLE_PATTERN = auto()
    SLICE_PATTERN = auto()
    REFERENCE_PATTERN = auto()
    OR_PATTERN = auto()
    RANGE_PATTERN = auto()
    
    # Attributes and macros
    ATTRIBUTE = auto()
    MACRO_DEFINITION = auto()


class RustVisibility(Enum):
    """Rust visibility modifiers."""
    PRIVATE = "private"
    PUBLIC = "pub"
    PUBLIC_CRATE = "pub(crate)"
    PUBLIC_SUPER = "pub(super)"
    PUBLIC_SELF = "pub(self)"
    PUBLIC_IN = "pub(in path)"


class RustMutability(Enum):
    """Rust mutability modifiers."""
    IMMUTABLE = "immutable"
    MUTABLE = "mut"


class RustSafety(Enum):
    """Rust safety modifiers."""
    SAFE = "safe"
    UNSAFE = "unsafe"


class RustAsyncness(Enum):
    """Rust async modifiers."""
    SYNC = "sync"
    ASYNC = "async"


@dataclass
class RustNode(ASTNode):
    """Base class for all Rust AST nodes."""
    rust_node_type: RustNodeType = RustNodeType.CRATE
    
    @abstractmethod
    def accept(self, visitor):
        """Accept a visitor for AST traversal."""
        pass


# ============================================================================
# Module System
# ============================================================================

@dataclass
class RustModule(RustNode):
    """Module declaration: mod name { ... }"""
    rust_node_type: RustNodeType = RustNodeType.MODULE
    name: str = ""
    items: List['RustItem'] = field(default_factory=list)
    visibility: RustVisibility = RustVisibility.PRIVATE
    
    def accept(self, visitor):
        return visitor.visit_rust_module(self)


@dataclass
class RustUseDeclaration(RustNode):
    """Use declaration: use std::collections::HashMap;"""
    rust_node_type: RustNodeType = RustNodeType.USE_DECLARATION
    path: str = ""
    alias: Optional[str] = None
    is_glob: bool = False  # use std::*;
    visibility: RustVisibility = RustVisibility.PRIVATE
    
    def accept(self, visitor):
        return visitor.visit_rust_use_declaration(self)


@dataclass
class RustExternCrate(RustNode):
    """External crate declaration: extern crate serde;"""
    rust_node_type: RustNodeType = RustNodeType.EXTERN_CRATE
    name: str = ""
    alias: Optional[str] = None
    
    def accept(self, visitor):
        return visitor.visit_rust_extern_crate(self)


# ============================================================================
# Type System
# ============================================================================

@dataclass
class RustType(RustNode):
    """Base class for Rust types."""
    pass


@dataclass
class RustTypeReference(RustType):
    """Type reference: String, Vec<T>"""
    rust_node_type: RustNodeType = RustNodeType.TYPE_REFERENCE
    path: str = ""
    type_arguments: List['RustType'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_rust_type_reference(self)


@dataclass
class RustReferenceType(RustType):
    """Reference type: &T, &mut T"""
    rust_node_type: RustNodeType = RustNodeType.REFERENCE_TYPE
    inner_type: Optional[RustType] = None
    mutability: RustMutability = RustMutability.IMMUTABLE
    lifetime: Optional['RustLifetime'] = None
    
    def accept(self, visitor):
        return visitor.visit_rust_reference_type(self)


@dataclass
class RustPointerType(RustType):
    """Raw pointer type: *const T, *mut T"""
    rust_node_type: RustNodeType = RustNodeType.POINTER_TYPE
    inner_type: Optional[RustType] = None
    mutability: RustMutability = RustMutability.IMMUTABLE
    
    def accept(self, visitor):
        return visitor.visit_rust_pointer_type(self)


@dataclass
class RustArrayType(RustType):
    """Array type: [T; N]"""
    rust_node_type: RustNodeType = RustNodeType.ARRAY_TYPE
    element_type: Optional[RustType] = None
    size: Optional['RustExpression'] = None
    
    def accept(self, visitor):
        return visitor.visit_rust_array_type(self)


@dataclass
class RustSliceType(RustType):
    """Slice type: [T]"""
    rust_node_type: RustNodeType = RustNodeType.SLICE_TYPE
    element_type: Optional[RustType] = None
    
    def accept(self, visitor):
        return visitor.visit_rust_slice_type(self)


@dataclass
class RustTupleType(RustType):
    """Tuple type: (T, U, V)"""
    rust_node_type: RustNodeType = RustNodeType.TUPLE_TYPE
    element_types: List[RustType] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_rust_tuple_type(self)


@dataclass
class RustFunctionType(RustType):
    """Function type: fn(T, U) -> V"""
    rust_node_type: RustNodeType = RustNodeType.FUNCTION_TYPE
    parameters: List[RustType] = field(default_factory=list)
    return_type: Optional[RustType] = None
    is_unsafe: bool = False
    is_extern: bool = False
    abi: Optional[str] = None
    
    def accept(self, visitor):
        return visitor.visit_rust_function_type(self)


@dataclass
class RustTraitObject(RustType):
    """Trait object: dyn Display + Send"""
    rust_node_type: RustNodeType = RustNodeType.TRAIT_OBJECT
    traits: List[str] = field(default_factory=list)
    lifetime: Optional['RustLifetime'] = None
    
    def accept(self, visitor):
        return visitor.visit_rust_trait_object(self)


@dataclass
class RustImplTrait(RustType):
    """Impl trait: impl Display + Send"""
    rust_node_type: RustNodeType = RustNodeType.IMPL_TRAIT
    traits: List[str] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_rust_impl_trait(self)


# ============================================================================
# Generics and Lifetimes
# ============================================================================

@dataclass
class RustLifetime(RustNode):
    """Lifetime: 'a, 'static"""
    rust_node_type: RustNodeType = RustNodeType.LIFETIME
    name: str = ""
    
    def accept(self, visitor):
        return visitor.visit_rust_lifetime(self)


@dataclass
class RustGenericParam(RustNode):
    """Generic parameter base class."""
    pass


@dataclass
class RustTypeParam(RustGenericParam):
    """Type parameter: T: Display + Send"""
    rust_node_type: RustNodeType = RustNodeType.TYPE_PARAM
    name: str = ""
    bounds: List[str] = field(default_factory=list)
    default: Optional[RustType] = None
    
    def accept(self, visitor):
        return visitor.visit_rust_type_param(self)


@dataclass
class RustLifetimeParam(RustGenericParam):
    """Lifetime parameter: 'a: 'b + 'c"""
    rust_node_type: RustNodeType = RustNodeType.LIFETIME_PARAM
    lifetime: RustLifetime = field(default_factory=lambda: RustLifetime())
    bounds: List[RustLifetime] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_rust_lifetime_param(self)


@dataclass
class RustConstParam(RustGenericParam):
    """Const parameter: const N: usize"""
    rust_node_type: RustNodeType = RustNodeType.CONST_PARAM
    name: str = ""
    param_type: Optional[RustType] = None
    default: Optional['RustExpression'] = None
    
    def accept(self, visitor):
        return visitor.visit_rust_const_param(self)


@dataclass
class RustWhereClause(RustNode):
    """Where clause: where T: Clone, U: Display"""
    rust_node_type: RustNodeType = RustNodeType.WHERE_CLAUSE
    predicates: List[str] = field(default_factory=list)  # Simplified for now
    
    def accept(self, visitor):
        return visitor.visit_rust_where_clause(self)


# ============================================================================
# Items (Top-level declarations)
# ============================================================================

@dataclass
class RustItem(RustNode):
    """Base class for Rust items."""
    visibility: RustVisibility = RustVisibility.PRIVATE
    attributes: List['RustAttribute'] = field(default_factory=list)


@dataclass
class RustFunction(RustItem):
    """Function declaration: fn name<T>(param: T) -> U { ... }"""
    rust_node_type: RustNodeType = RustNodeType.FUNCTION
    name: str = ""
    generics: List[RustGenericParam] = field(default_factory=list)
    parameters: List['RustParameter'] = field(default_factory=list)
    return_type: Optional[RustType] = None
    body: Optional['RustBlock'] = None
    is_async: bool = False
    is_unsafe: bool = False
    is_extern: bool = False
    is_const: bool = False
    abi: Optional[str] = None
    where_clause: Optional[RustWhereClause] = None
    
    def accept(self, visitor):
        return visitor.visit_rust_function(self)


@dataclass
class RustStruct(RustItem):
    """Struct declaration: struct Name<T> { field: T }"""
    rust_node_type: RustNodeType = RustNodeType.STRUCT
    name: str = ""
    generics: List[RustGenericParam] = field(default_factory=list)
    fields: List['RustField'] = field(default_factory=list)
    is_tuple: bool = False
    is_unit: bool = False
    where_clause: Optional[RustWhereClause] = None
    
    def accept(self, visitor):
        return visitor.visit_rust_struct(self)


@dataclass
class RustEnum(RustItem):
    """Enum declaration: enum Option<T> { Some(T), None }"""
    rust_node_type: RustNodeType = RustNodeType.ENUM
    name: str = ""
    generics: List[RustGenericParam] = field(default_factory=list)
    variants: List['RustEnumVariant'] = field(default_factory=list)
    where_clause: Optional[RustWhereClause] = None
    
    def accept(self, visitor):
        return visitor.visit_rust_enum(self)


@dataclass
class RustUnion(RustItem):
    """Union declaration: union MyUnion { field1: i32, field2: f64 }"""
    rust_node_type: RustNodeType = RustNodeType.UNION
    name: str = ""
    generics: List[RustGenericParam] = field(default_factory=list)
    fields: List['RustField'] = field(default_factory=list)
    where_clause: Optional[RustWhereClause] = None
    
    def accept(self, visitor):
        return visitor.visit_rust_union(self)


@dataclass
class RustTrait(RustItem):
    """Trait declaration: trait Clone { fn clone(&self) -> Self; }"""
    rust_node_type: RustNodeType = RustNodeType.TRAIT
    name: str = ""
    generics: List[RustGenericParam] = field(default_factory=list)
    supertraits: List[str] = field(default_factory=list)
    items: List['RustTraitItem'] = field(default_factory=list)
    is_unsafe: bool = False
    is_auto: bool = False
    where_clause: Optional[RustWhereClause] = None
    
    def accept(self, visitor):
        return visitor.visit_rust_trait(self)


@dataclass
class RustImpl(RustItem):
    """Impl block: impl<T> Clone for Vec<T> where T: Clone { ... }"""
    rust_node_type: RustNodeType = RustNodeType.IMPL
    generics: List[RustGenericParam] = field(default_factory=list)
    trait_ref: Optional[str] = None  # Trait being implemented
    self_type: Optional[RustType] = None  # Type being implemented for
    items: List['RustImplItem'] = field(default_factory=list)
    is_unsafe: bool = False
    where_clause: Optional[RustWhereClause] = None
    
    def accept(self, visitor):
        return visitor.visit_rust_impl(self)


@dataclass
class RustTypeAlias(RustItem):
    """Type alias: type MyType<T> = Vec<T>;"""
    rust_node_type: RustNodeType = RustNodeType.TYPE_ALIAS
    name: str = ""
    generics: List[RustGenericParam] = field(default_factory=list)
    type_def: Optional[RustType] = None
    where_clause: Optional[RustWhereClause] = None
    
    def accept(self, visitor):
        return visitor.visit_rust_type_alias(self)


@dataclass
class RustConst(RustItem):
    """Const declaration: const PI: f64 = 3.14159;"""
    rust_node_type: RustNodeType = RustNodeType.CONST
    name: str = ""
    const_type: Optional[RustType] = None
    value: Optional['RustExpression'] = None
    
    def accept(self, visitor):
        return visitor.visit_rust_const(self)


@dataclass
class RustStatic(RustItem):
    """Static declaration: static COUNTER: AtomicUsize = AtomicUsize::new(0);"""
    rust_node_type: RustNodeType = RustNodeType.STATIC
    name: str = ""
    static_type: Optional[RustType] = None
    value: Optional['RustExpression'] = None
    mutability: RustMutability = RustMutability.IMMUTABLE
    
    def accept(self, visitor):
        return visitor.visit_rust_static(self)


# ============================================================================
# Struct and Enum Components
# ============================================================================

@dataclass
class RustField(RustNode):
    """Struct field: name: Type"""
    name: str = ""
    field_type: Optional[RustType] = None
    visibility: RustVisibility = RustVisibility.PRIVATE
    attributes: List['RustAttribute'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_rust_field(self)


@dataclass
class RustEnumVariant(RustNode):
    """Enum variant: Some(T), None, Point { x: i32, y: i32 }"""
    name: str = ""
    fields: List[RustField] = field(default_factory=list)
    discriminant: Optional['RustExpression'] = None
    is_tuple: bool = False
    is_unit: bool = False
    attributes: List['RustAttribute'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_rust_enum_variant(self)


@dataclass
class RustParameter(RustNode):
    """Function parameter: name: Type"""
    name: str = ""
    param_type: Optional[RustType] = None
    is_self: bool = False
    self_kind: Optional[str] = None  # "&self", "&mut self", "self"
    attributes: List['RustAttribute'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_rust_parameter(self)


# ============================================================================
# Expressions
# ============================================================================

@dataclass
class RustExpression(RustNode):
    """Base class for Rust expressions."""
    pass


@dataclass
class RustIdentifier(RustExpression):
    """Identifier: name"""
    rust_node_type: RustNodeType = RustNodeType.IDENTIFIER
    name: str = ""
    
    def accept(self, visitor):
        return visitor.visit_rust_identifier(self)


@dataclass
class RustLiteral(RustExpression):
    """Literal: 42, "hello", true"""
    rust_node_type: RustNodeType = RustNodeType.LITERAL
    value: Any = None
    literal_type: str = "integer"  # integer, float, string, char, boolean, byte_string
    suffix: Optional[str] = None  # Type suffix like i32, f64
    
    def accept(self, visitor):
        return visitor.visit_rust_literal(self)


@dataclass
class RustPath(RustExpression):
    """Path: std::collections::HashMap"""
    rust_node_type: RustNodeType = RustNodeType.PATH
    segments: List[str] = field(default_factory=list)
    type_arguments: List[List[RustType]] = field(default_factory=list)  # Per segment
    
    def accept(self, visitor):
        return visitor.visit_rust_path(self)


@dataclass
class RustBlock(RustExpression):
    """Block expression: { statements; expr }"""
    rust_node_type: RustNodeType = RustNodeType.BLOCK_EXPRESSION
    statements: List['RustStatement'] = field(default_factory=list)
    expression: Optional[RustExpression] = None
    is_unsafe: bool = False
    is_async: bool = False
    is_const: bool = False
    
    def accept(self, visitor):
        return visitor.visit_rust_block(self)


@dataclass
class RustIfExpression(RustExpression):
    """If expression: if condition { then_branch } else { else_branch }"""
    rust_node_type: RustNodeType = RustNodeType.IF_EXPRESSION
    condition: Optional[RustExpression] = None
    then_branch: Optional[RustBlock] = None
    else_branch: Optional[RustExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_rust_if_expression(self)


@dataclass
class RustMatchExpression(RustExpression):
    """Match expression: match expr { pattern => body, ... }"""
    rust_node_type: RustNodeType = RustNodeType.MATCH_EXPRESSION
    expression: Optional[RustExpression] = None
    arms: List['RustMatchArm'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_rust_match_expression(self)


@dataclass
class RustLoopExpression(RustExpression):
    """Loop expression: loop { ... }"""
    rust_node_type: RustNodeType = RustNodeType.LOOP_EXPRESSION
    body: Optional[RustBlock] = None
    label: Optional[str] = None
    
    def accept(self, visitor):
        return visitor.visit_rust_loop_expression(self)


@dataclass
class RustWhileExpression(RustExpression):
    """While expression: while condition { ... }"""
    rust_node_type: RustNodeType = RustNodeType.WHILE_EXPRESSION
    condition: Optional[RustExpression] = None
    body: Optional[RustBlock] = None
    label: Optional[str] = None
    
    def accept(self, visitor):
        return visitor.visit_rust_while_expression(self)


@dataclass
class RustForExpression(RustExpression):
    """For expression: for pattern in iterable { ... }"""
    rust_node_type: RustNodeType = RustNodeType.FOR_EXPRESSION
    pattern: Optional['RustPattern'] = None
    iterable: Optional[RustExpression] = None
    body: Optional[RustBlock] = None
    label: Optional[str] = None
    
    def accept(self, visitor):
        return visitor.visit_rust_for_expression(self)


@dataclass
class RustCallExpression(RustExpression):
    """Function call: func(args)"""
    rust_node_type: RustNodeType = RustNodeType.CALL_EXPRESSION
    function: Optional[RustExpression] = None
    arguments: List[RustExpression] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_rust_call_expression(self)


@dataclass
class RustMethodCall(RustExpression):
    """Method call: obj.method(args)"""
    rust_node_type: RustNodeType = RustNodeType.METHOD_CALL
    receiver: Optional[RustExpression] = None
    method_name: str = ""
    arguments: List[RustExpression] = field(default_factory=list)
    type_arguments: List[RustType] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_rust_method_call(self)


@dataclass
class RustFieldAccess(RustExpression):
    """Field access: obj.field"""
    rust_node_type: RustNodeType = RustNodeType.FIELD_ACCESS
    receiver: Optional[RustExpression] = None
    field_name: str = ""
    
    def accept(self, visitor):
        return visitor.visit_rust_field_access(self)


@dataclass
class RustIndexExpression(RustExpression):
    """Index expression: array[index]"""
    rust_node_type: RustNodeType = RustNodeType.INDEX_EXPRESSION
    receiver: Optional[RustExpression] = None
    index: Optional[RustExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_rust_index_expression(self)


@dataclass
class RustTupleExpression(RustExpression):
    """Tuple expression: (expr1, expr2, ...)"""
    rust_node_type: RustNodeType = RustNodeType.TUPLE_EXPRESSION
    elements: List[RustExpression] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_rust_tuple_expression(self)


@dataclass
class RustArrayExpression(RustExpression):
    """Array expression: [expr1, expr2, ...] or [expr; count]"""
    rust_node_type: RustNodeType = RustNodeType.ARRAY_EXPRESSION
    elements: List[RustExpression] = field(default_factory=list)
    repeat_element: Optional[RustExpression] = None
    repeat_count: Optional[RustExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_rust_array_expression(self)


@dataclass
class RustStructExpression(RustExpression):
    """Struct expression: Point { x: 1, y: 2 }"""
    rust_node_type: RustNodeType = RustNodeType.STRUCT_EXPRESSION
    path: Optional[RustPath] = None
    fields: List['RustFieldExpression'] = field(default_factory=list)
    base: Optional[RustExpression] = None  # For struct update syntax
    
    def accept(self, visitor):
        return visitor.visit_rust_struct_expression(self)


@dataclass
class RustClosure(RustExpression):
    """Closure: |params| body"""
    rust_node_type: RustNodeType = RustNodeType.CLOSURE
    parameters: List[RustParameter] = field(default_factory=list)
    body: Optional[RustExpression] = None
    is_async: bool = False
    is_move: bool = False
    
    def accept(self, visitor):
        return visitor.visit_rust_closure(self)


@dataclass
class RustAwaitExpression(RustExpression):
    """Await expression: expr.await"""
    rust_node_type: RustNodeType = RustNodeType.AWAIT_EXPRESSION
    expression: Optional[RustExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_rust_await_expression(self)


@dataclass
class RustTryExpression(RustExpression):
    """Try expression: expr?"""
    rust_node_type: RustNodeType = RustNodeType.TRY_EXPRESSION
    expression: Optional[RustExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_rust_try_expression(self)


@dataclass
class RustReturnExpression(RustExpression):
    """Return expression: return expr"""
    rust_node_type: RustNodeType = RustNodeType.RETURN_EXPRESSION
    expression: Optional[RustExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_rust_return_expression(self)


@dataclass
class RustBreakExpression(RustExpression):
    """Break expression: break label expr"""
    rust_node_type: RustNodeType = RustNodeType.BREAK_EXPRESSION
    label: Optional[str] = None
    expression: Optional[RustExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_rust_break_expression(self)


@dataclass
class RustContinueExpression(RustExpression):
    """Continue expression: continue label"""
    rust_node_type: RustNodeType = RustNodeType.CONTINUE_EXPRESSION
    label: Optional[str] = None
    
    def accept(self, visitor):
        return visitor.visit_rust_continue_expression(self)


@dataclass
class RustMacroCall(RustExpression):
    """Macro call: println!("Hello")"""
    rust_node_type: RustNodeType = RustNodeType.MACRO_CALL
    path: Optional[RustPath] = None
    tokens: List[str] = field(default_factory=list)  # Simplified token representation
    
    def accept(self, visitor):
        return visitor.visit_rust_macro_call(self)


# ============================================================================
# Statements
# ============================================================================

@dataclass
class RustStatement(RustNode):
    """Base class for Rust statements."""
    pass


@dataclass
class RustExpressionStatement(RustStatement):
    """Expression statement"""
    rust_node_type: RustNodeType = RustNodeType.EXPRESSION_STATEMENT
    expression: Optional[RustExpression] = None
    has_semicolon: bool = False
    
    def accept(self, visitor):
        return visitor.visit_rust_expression_statement(self)


@dataclass
class RustLetStatement(RustStatement):
    """Let statement: let pattern: Type = expr;"""
    rust_node_type: RustNodeType = RustNodeType.LET_STATEMENT
    pattern: Optional['RustPattern'] = None
    type_annotation: Optional[RustType] = None
    initializer: Optional[RustExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_rust_let_statement(self)


@dataclass
class RustItemStatement(RustStatement):
    """Item statement (item within a function)"""
    rust_node_type: RustNodeType = RustNodeType.ITEM_STATEMENT
    item: Optional[RustItem] = None
    
    def accept(self, visitor):
        return visitor.visit_rust_item_statement(self)


# ============================================================================
# Patterns
# ============================================================================

@dataclass
class RustPattern(RustNode):
    """Base class for Rust patterns."""
    pass


@dataclass
class RustIdentifierPattern(RustPattern):
    """Identifier pattern: name, mut name"""
    rust_node_type: RustNodeType = RustNodeType.IDENTIFIER_PATTERN
    name: str = ""
    mutability: RustMutability = RustMutability.IMMUTABLE
    
    def accept(self, visitor):
        return visitor.visit_rust_identifier_pattern(self)


@dataclass
class RustWildcardPattern(RustPattern):
    """Wildcard pattern: _"""
    rust_node_type: RustNodeType = RustNodeType.WILDCARD_PATTERN
    
    def accept(self, visitor):
        return visitor.visit_rust_wildcard_pattern(self)


@dataclass
class RustLiteralPattern(RustPattern):
    """Literal pattern: 42, "hello", true"""
    rust_node_type: RustNodeType = RustNodeType.LITERAL_PATTERN
    literal: Optional[RustLiteral] = None
    
    def accept(self, visitor):
        return visitor.visit_rust_literal_pattern(self)


@dataclass
class RustStructPattern(RustPattern):
    """Struct pattern: Point { x, y }"""
    rust_node_type: RustNodeType = RustNodeType.STRUCT_PATTERN
    path: Optional[RustPath] = None
    fields: List['RustFieldPattern'] = field(default_factory=list)
    has_rest: bool = False  # .. pattern
    
    def accept(self, visitor):
        return visitor.visit_rust_struct_pattern(self)


@dataclass
class RustTuplePattern(RustPattern):
    """Tuple pattern: (a, b, ..)"""
    rust_node_type: RustNodeType = RustNodeType.TUPLE_PATTERN
    elements: List[RustPattern] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_rust_tuple_pattern(self)


@dataclass
class RustReferencePattern(RustPattern):
    """Reference pattern: &pattern, &mut pattern"""
    rust_node_type: RustNodeType = RustNodeType.REFERENCE_PATTERN
    pattern: Optional[RustPattern] = None
    mutability: RustMutability = RustMutability.IMMUTABLE
    
    def accept(self, visitor):
        return visitor.visit_rust_reference_pattern(self)


@dataclass
class RustOrPattern(RustPattern):
    """Or pattern: pattern1 | pattern2"""
    rust_node_type: RustNodeType = RustNodeType.OR_PATTERN
    patterns: List[RustPattern] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_rust_or_pattern(self)


@dataclass
class RustRangePattern(RustPattern):
    """Range pattern: 1..=10, 'a'..='z'"""
    rust_node_type: RustNodeType = RustNodeType.RANGE_PATTERN
    start: Optional[RustExpression] = None
    end: Optional[RustExpression] = None
    is_inclusive: bool = True
    
    def accept(self, visitor):
        return visitor.visit_rust_range_pattern(self)


# ============================================================================
# Special Constructs
# ============================================================================

@dataclass
class RustAttribute(RustNode):
    """Attribute: #[derive(Debug)], #![feature(async_await)]"""
    rust_node_type: RustNodeType = RustNodeType.ATTRIBUTE
    path: str = ""
    tokens: List[str] = field(default_factory=list)
    is_inner: bool = False  # #! vs #
    
    def accept(self, visitor):
        return visitor.visit_rust_attribute(self)


@dataclass
class RustMatchArm(RustNode):
    """Match arm: pattern if guard => body"""
    pattern: Optional[RustPattern] = None
    guard: Optional[RustExpression] = None
    body: Optional[RustExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_rust_match_arm(self)


@dataclass
class RustFieldExpression(RustNode):
    """Field in struct expression: field: expr"""
    name: str = ""
    expression: Optional[RustExpression] = None
    is_shorthand: bool = False  # { field } vs { field: expr }
    
    def accept(self, visitor):
        return visitor.visit_rust_field_expression(self)


@dataclass
class RustFieldPattern(RustNode):
    """Field in struct pattern: field: pattern"""
    name: str = ""
    pattern: Optional[RustPattern] = None
    is_shorthand: bool = False  # { field } vs { field: pattern }
    
    def accept(self, visitor):
        return visitor.visit_rust_field_pattern(self)


@dataclass
class RustTraitItem(RustNode):
    """Item in trait definition."""
    pass


@dataclass
class RustImplItem(RustNode):
    """Item in impl block."""
    pass


# ============================================================================
# File and Program Structure
# ============================================================================

@dataclass
class RustCrate(RustNode):
    """Rust crate (compilation unit)"""
    rust_node_type: RustNodeType = RustNodeType.CRATE
    name: str = ""
    items: List[RustItem] = field(default_factory=list)
    attributes: List[RustAttribute] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_rust_crate(self)


# ============================================================================
# Visitor Pattern
# ============================================================================

class RustVisitor(ABC):
    """Abstract visitor for Rust AST nodes."""
    
    @abstractmethod
    def visit_rust_crate(self, node: RustCrate): pass
    
    @abstractmethod
    def visit_rust_module(self, node: RustModule): pass
    
    @abstractmethod
    def visit_rust_function(self, node: RustFunction): pass
    
    @abstractmethod
    def visit_rust_struct(self, node: RustStruct): pass
    
    @abstractmethod
    def visit_rust_enum(self, node: RustEnum): pass
    
    @abstractmethod
    def visit_rust_trait(self, node: RustTrait): pass
    
    @abstractmethod
    def visit_rust_impl(self, node: RustImpl): pass
    
    @abstractmethod
    def visit_rust_identifier(self, node: RustIdentifier): pass
    
    @abstractmethod
    def visit_rust_literal(self, node: RustLiteral): pass
    
    @abstractmethod
    def visit_rust_block(self, node: RustBlock): pass


# ============================================================================
# Utility Functions
# ============================================================================

def create_rust_identifier(name: str) -> RustIdentifier:
    """Create a Rust identifier node."""
    return RustIdentifier(name=name)


def create_rust_literal(value: Any, literal_type: str = "integer") -> RustLiteral:
    """Create a Rust literal node."""
    return RustLiteral(value=value, literal_type=literal_type)


def create_rust_function(name: str, is_async: bool = False) -> RustFunction:
    """Create a Rust function node."""
    return RustFunction(name=name, is_async=is_async)


def create_rust_struct(name: str) -> RustStruct:
    """Create a Rust struct node."""
    return RustStruct(name=name)


def create_rust_enum(name: str) -> RustEnum:
    """Create a Rust enum node."""
    return RustEnum(name=name)


# ============================================================================
# Constants
# ============================================================================

# Rust keywords
RUST_KEYWORDS = {
    "as", "async", "await", "break", "const", "continue", "crate", "dyn", "else",
    "enum", "extern", "false", "fn", "for", "if", "impl", "in", "let", "loop",
    "match", "mod", "move", "mut", "pub", "ref", "return", "self", "Self", "static",
    "struct", "super", "trait", "true", "type", "union", "unsafe", "use", "where",
    "while", "abstract", "become", "box", "do", "final", "macro", "override",
    "priv", "typeof", "unsized", "virtual", "yield", "try"
}

# Rust primitive types
RUST_PRIMITIVE_TYPES = {
    "bool", "char", "str", "i8", "i16", "i32", "i64", "i128", "isize",
    "u8", "u16", "u32", "u64", "u128", "usize", "f32", "f64"
}

# Rust operators
RUST_OPERATORS = {
    "+", "-", "*", "/", "%", "=", "==", "!=", "<", ">", "<=", ">=",
    "&&", "||", "!", "&", "|", "^", "<<", ">>", "+=", "-=", "*=", "/=",
    "%=", "&=", "|=", "^=", "<<=", ">>=", "?", "->", "=>", "..", "..=",
    "::", ".", "..", "...", ";", ",", "(", ")", "[", "]", "{", "}"
}