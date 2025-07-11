#!/usr/bin/env python3
"""
Kotlin AST Node Definitions

Comprehensive Abstract Syntax Tree nodes for Kotlin language covering all Kotlin features
including classes, objects, functions, properties, coroutines, DSLs, data classes, sealed classes,
type inference, null safety, lambdas, higher-order functions, and Java interoperability.

This module provides complete AST representation for:
- Package declarations and imports
- Classes, objects, interfaces, enums
- Functions and properties with modifiers
- Coroutines and suspend functions
- Data classes, sealed classes, inline classes
- Type system with nullability and generics
- Lambda expressions and higher-order functions
- DSL constructs and operator overloading
- Java interoperability features
- Control flow and pattern matching
"""

from typing import List, Optional, Any, Union, Dict
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod

from ....core.runa_ast import ASTNode, SourceLocation, TranslationMetadata


class KotlinNodeType(Enum):
    """Kotlin-specific AST node types."""
    # Package and imports
    PACKAGE_DECLARATION = auto()
    IMPORT_DECLARATION = auto()
    
    # Classes and objects
    CLASS_DECLARATION = auto()
    OBJECT_DECLARATION = auto()
    INTERFACE_DECLARATION = auto()
    ENUM_CLASS_DECLARATION = auto()
    ANNOTATION_CLASS_DECLARATION = auto()
    
    # Class members
    PROPERTY_DECLARATION = auto()
    FUNCTION_DECLARATION = auto()
    CONSTRUCTOR_DECLARATION = auto()
    INIT_BLOCK = auto()
    
    # Types
    TYPE_REFERENCE = auto()
    NULLABLE_TYPE = auto()
    FUNCTION_TYPE = auto()
    USER_TYPE = auto()
    TYPE_PROJECTION = auto()
    TYPE_PARAMETER = auto()
    
    # Expressions
    IDENTIFIER = auto()
    LITERAL_EXPRESSION = auto()
    STRING_TEMPLATE = auto()
    LAMBDA_EXPRESSION = auto()
    FUNCTION_LITERAL = auto()
    OBJECT_LITERAL = auto()
    THIS_EXPRESSION = auto()
    SUPER_EXPRESSION = auto()
    IF_EXPRESSION = auto()
    WHEN_EXPRESSION = auto()
    TRY_EXPRESSION = auto()
    BINARY_EXPRESSION = auto()
    UNARY_EXPRESSION = auto()
    POSTFIX_EXPRESSION = auto()
    CALL_EXPRESSION = auto()
    ARRAY_ACCESS_EXPRESSION = auto()
    MEMBER_ACCESS_EXPRESSION = auto()
    SAFE_ACCESS_EXPRESSION = auto()
    ELVIS_EXPRESSION = auto()
    IS_EXPRESSION = auto()
    AS_EXPRESSION = auto()
    
    # Statements
    EXPRESSION_STATEMENT = auto()
    ASSIGNMENT = auto()
    BLOCK = auto()
    IF_STATEMENT = auto()
    WHEN_STATEMENT = auto()
    FOR_STATEMENT = auto()
    WHILE_STATEMENT = auto()
    DO_WHILE_STATEMENT = auto()
    TRY_STATEMENT = auto()
    RETURN_STATEMENT = auto()
    BREAK_STATEMENT = auto()
    CONTINUE_STATEMENT = auto()
    THROW_STATEMENT = auto()
    
    # Coroutines
    SUSPEND_FUNCTION = auto()
    COROUTINE_SCOPE = auto()
    ASYNC_EXPRESSION = auto()
    AWAIT_EXPRESSION = auto()
    
    # Special constructs
    DELEGATION = auto()
    DESTRUCTURING_DECLARATION = auto()
    PROPERTY_DELEGATE = auto()
    ANNOTATION = auto()
    
    # File structure
    FILE = auto()
    PROGRAM = auto()


class KotlinVisibility(Enum):
    """Kotlin visibility modifiers."""
    PUBLIC = "public"
    PRIVATE = "private"
    PROTECTED = "protected"
    INTERNAL = "internal"


class KotlinModality(Enum):
    """Kotlin modality modifiers."""
    FINAL = "final"
    OPEN = "open"
    ABSTRACT = "abstract"
    SEALED = "sealed"


class KotlinClassKind(Enum):
    """Kotlin class kinds."""
    CLASS = "class"
    INTERFACE = "interface"
    ENUM_CLASS = "enum class"
    ANNOTATION_CLASS = "annotation class"
    OBJECT = "object"
    DATA_CLASS = "data class"
    SEALED_CLASS = "sealed class"
    INLINE_CLASS = "inline class"


@dataclass
class KotlinNode(ASTNode):
    """Base class for all Kotlin AST nodes."""
    kotlin_node_type: KotlinNodeType = KotlinNodeType.PROGRAM
    
    @abstractmethod
    def accept(self, visitor):
        """Accept a visitor for AST traversal."""
        pass


@dataclass
class KotlinModifier:
    """Kotlin modifier (visibility, modality, etc.)."""
    keyword: str
    visibility: Optional[KotlinVisibility] = None
    modality: Optional[KotlinModality] = None
    is_suspend: bool = False
    is_inline: bool = False
    is_external: bool = False
    is_operator: bool = False
    is_infix: bool = False


# ============================================================================
# Package and Import Declarations
# ============================================================================

@dataclass
class KotlinPackageDeclaration(KotlinNode):
    """Package declaration: package com.example"""
    kotlin_node_type: KotlinNodeType = KotlinNodeType.PACKAGE_DECLARATION
    name: str = ""
    
    def accept(self, visitor):
        return visitor.visit_kotlin_package_declaration(self)


@dataclass
class KotlinImportDeclaration(KotlinNode):
    """Import declaration: import com.example.Class"""
    kotlin_node_type: KotlinNodeType = KotlinNodeType.IMPORT_DECLARATION
    name: str = ""
    alias: Optional[str] = None
    is_all_under: bool = False  # import com.example.*
    
    def accept(self, visitor):
        return visitor.visit_kotlin_import_declaration(self)


# ============================================================================
# Type System
# ============================================================================

@dataclass
class KotlinType(KotlinNode):
    """Base class for Kotlin type expressions."""
    pass


@dataclass
class KotlinTypeReference(KotlinType):
    """Type reference: String, List<Int>"""
    kotlin_node_type: KotlinNodeType = KotlinNodeType.TYPE_REFERENCE
    name: str = ""
    type_arguments: List['KotlinTypeProjection'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_kotlin_type_reference(self)


@dataclass
class KotlinNullableType(KotlinType):
    """Nullable type: String?"""
    kotlin_node_type: KotlinNodeType = KotlinNodeType.NULLABLE_TYPE
    type: Optional[KotlinType] = None
    
    def accept(self, visitor):
        return visitor.visit_kotlin_nullable_type(self)


@dataclass
class KotlinFunctionType(KotlinType):
    """Function type: (Int, String) -> Boolean"""
    kotlin_node_type: KotlinNodeType = KotlinNodeType.FUNCTION_TYPE
    parameters: List['KotlinParameter'] = field(default_factory=list)
    return_type: Optional[KotlinType] = None
    is_suspend: bool = False
    
    def accept(self, visitor):
        return visitor.visit_kotlin_function_type(self)


@dataclass
class KotlinTypeProjection(KotlinNode):
    """Type projection for generics: out T, in T, *"""
    kotlin_node_type: KotlinNodeType = KotlinNodeType.TYPE_PROJECTION
    variance: Optional[str] = None  # "in", "out", or None
    type: Optional[KotlinType] = None
    is_star: bool = False
    
    def accept(self, visitor):
        return visitor.visit_kotlin_type_projection(self)


@dataclass
class KotlinTypeParameter(KotlinNode):
    """Type parameter: T : Comparable<T>"""
    kotlin_node_type: KotlinNodeType = KotlinNodeType.TYPE_PARAMETER
    name: str = ""
    bounds: List[KotlinType] = field(default_factory=list)
    variance: Optional[str] = None  # "in", "out"
    is_reified: bool = False
    
    def accept(self, visitor):
        return visitor.visit_kotlin_type_parameter(self)


# ============================================================================
# Expressions
# ============================================================================

@dataclass
class KotlinExpression(KotlinNode):
    """Base class for Kotlin expressions."""
    pass


@dataclass
class KotlinIdentifier(KotlinExpression):
    """Identifier: name"""
    kotlin_node_type: KotlinNodeType = KotlinNodeType.IDENTIFIER
    name: str = ""
    
    def accept(self, visitor):
        return visitor.visit_kotlin_identifier(self)


@dataclass
class KotlinLiteralExpression(KotlinExpression):
    """Literal expression: 42, "hello", true, null"""
    kotlin_node_type: KotlinNodeType = KotlinNodeType.LITERAL_EXPRESSION
    value: Any = None
    literal_type: str = "string"  # int, float, string, boolean, null, char
    
    def accept(self, visitor):
        return visitor.visit_kotlin_literal_expression(self)


@dataclass
class KotlinStringTemplate(KotlinExpression):
    """String template: "Hello $name" """
    kotlin_node_type: KotlinNodeType = KotlinNodeType.STRING_TEMPLATE
    entries: List[Union[str, KotlinExpression]] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_kotlin_string_template(self)


@dataclass
class KotlinLambdaExpression(KotlinExpression):
    """Lambda expression: { x, y -> x + y }"""
    kotlin_node_type: KotlinNodeType = KotlinNodeType.LAMBDA_EXPRESSION
    parameters: List['KotlinParameter'] = field(default_factory=list)
    body: Optional['KotlinBlock'] = None
    
    def accept(self, visitor):
        return visitor.visit_kotlin_lambda_expression(self)


@dataclass
class KotlinBinaryExpression(KotlinExpression):
    """Binary expression: a + b, a && b"""
    kotlin_node_type: KotlinNodeType = KotlinNodeType.BINARY_EXPRESSION
    left: Optional[KotlinExpression] = None
    operator: str = ""
    right: Optional[KotlinExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_kotlin_binary_expression(self)


@dataclass
class KotlinUnaryExpression(KotlinExpression):
    """Unary expression: -x, !flag, ++i"""
    kotlin_node_type: KotlinNodeType = KotlinNodeType.UNARY_EXPRESSION
    operator: str = ""
    expression: Optional[KotlinExpression] = None
    is_postfix: bool = False
    
    def accept(self, visitor):
        return visitor.visit_kotlin_unary_expression(self)


@dataclass
class KotlinCallExpression(KotlinExpression):
    """Function call: f(x, y)"""
    kotlin_node_type: KotlinNodeType = KotlinNodeType.CALL_EXPRESSION
    callee: Optional[KotlinExpression] = None
    arguments: List['KotlinArgument'] = field(default_factory=list)
    type_arguments: List[KotlinType] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_kotlin_call_expression(self)


@dataclass
class KotlinMemberAccessExpression(KotlinExpression):
    """Member access: obj.property"""
    kotlin_node_type: KotlinNodeType = KotlinNodeType.MEMBER_ACCESS_EXPRESSION
    receiver: Optional[KotlinExpression] = None
    selector: str = ""
    
    def accept(self, visitor):
        return visitor.visit_kotlin_member_access_expression(self)


@dataclass
class KotlinSafeAccessExpression(KotlinExpression):
    """Safe access: obj?.property"""
    kotlin_node_type: KotlinNodeType = KotlinNodeType.SAFE_ACCESS_EXPRESSION
    receiver: Optional[KotlinExpression] = None
    selector: str = ""
    
    def accept(self, visitor):
        return visitor.visit_kotlin_safe_access_expression(self)


@dataclass
class KotlinElvisExpression(KotlinExpression):
    """Elvis expression: a ?: b"""
    kotlin_node_type: KotlinNodeType = KotlinNodeType.ELVIS_EXPRESSION
    left: Optional[KotlinExpression] = None
    right: Optional[KotlinExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_kotlin_elvis_expression(self)


@dataclass
class KotlinIsExpression(KotlinExpression):
    """Type check: obj is String"""
    kotlin_node_type: KotlinNodeType = KotlinNodeType.IS_EXPRESSION
    expression: Optional[KotlinExpression] = None
    type: Optional[KotlinType] = None
    is_negated: bool = False  # !is
    
    def accept(self, visitor):
        return visitor.visit_kotlin_is_expression(self)


@dataclass
class KotlinAsExpression(KotlinExpression):
    """Type cast: obj as String, obj as? String"""
    kotlin_node_type: KotlinNodeType = KotlinNodeType.AS_EXPRESSION
    expression: Optional[KotlinExpression] = None
    type: Optional[KotlinType] = None
    is_safe: bool = False  # as?
    
    def accept(self, visitor):
        return visitor.visit_kotlin_as_expression(self)


@dataclass
class KotlinWhenExpression(KotlinExpression):
    """When expression: when(x) { ... }"""
    kotlin_node_type: KotlinNodeType = KotlinNodeType.WHEN_EXPRESSION
    subject: Optional[KotlinExpression] = None
    entries: List['KotlinWhenEntry'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_kotlin_when_expression(self)


@dataclass
class KotlinIfExpression(KotlinExpression):
    """If expression: if (condition) expr1 else expr2"""
    kotlin_node_type: KotlinNodeType = KotlinNodeType.IF_EXPRESSION
    condition: Optional[KotlinExpression] = None
    then_expression: Optional[KotlinExpression] = None
    else_expression: Optional[KotlinExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_kotlin_if_expression(self)


@dataclass
class KotlinTryExpression(KotlinExpression):
    """Try expression: try { ... } catch { ... }"""
    kotlin_node_type: KotlinNodeType = KotlinNodeType.TRY_EXPRESSION
    try_block: Optional['KotlinBlock'] = None
    catch_clauses: List['KotlinCatchClause'] = field(default_factory=list)
    finally_block: Optional['KotlinBlock'] = None
    
    def accept(self, visitor):
        return visitor.visit_kotlin_try_expression(self)


# ============================================================================
# Statements
# ============================================================================

@dataclass
class KotlinStatement(KotlinNode):
    """Base class for Kotlin statements."""
    pass


@dataclass
class KotlinBlock(KotlinStatement):
    """Block statement: { ... }"""
    kotlin_node_type: KotlinNodeType = KotlinNodeType.BLOCK
    statements: List[KotlinStatement] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_kotlin_block(self)


@dataclass
class KotlinExpressionStatement(KotlinStatement):
    """Expression statement"""
    kotlin_node_type: KotlinNodeType = KotlinNodeType.EXPRESSION_STATEMENT
    expression: Optional[KotlinExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_kotlin_expression_statement(self)


@dataclass
class KotlinAssignment(KotlinStatement):
    """Assignment: x = y, x += y"""
    kotlin_node_type: KotlinNodeType = KotlinNodeType.ASSIGNMENT
    target: Optional[KotlinExpression] = None
    operator: str = "="
    value: Optional[KotlinExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_kotlin_assignment(self)


@dataclass
class KotlinReturnStatement(KotlinStatement):
    """Return statement: return expr"""
    kotlin_node_type: KotlinNodeType = KotlinNodeType.RETURN_STATEMENT
    expression: Optional[KotlinExpression] = None
    label: Optional[str] = None
    
    def accept(self, visitor):
        return visitor.visit_kotlin_return_statement(self)


@dataclass
class KotlinThrowStatement(KotlinStatement):
    """Throw statement: throw Exception()"""
    kotlin_node_type: KotlinNodeType = KotlinNodeType.THROW_STATEMENT
    expression: Optional[KotlinExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_kotlin_throw_statement(self)


@dataclass
class KotlinForStatement(KotlinStatement):
    """For statement: for (x in list) { ... }"""
    kotlin_node_type: KotlinNodeType = KotlinNodeType.FOR_STATEMENT
    parameter: Optional['KotlinParameter'] = None
    iterable: Optional[KotlinExpression] = None
    body: Optional[KotlinStatement] = None
    
    def accept(self, visitor):
        return visitor.visit_kotlin_for_statement(self)


@dataclass
class KotlinWhileStatement(KotlinStatement):
    """While statement: while (condition) { ... }"""
    kotlin_node_type: KotlinNodeType = KotlinNodeType.WHILE_STATEMENT
    condition: Optional[KotlinExpression] = None
    body: Optional[KotlinStatement] = None
    
    def accept(self, visitor):
        return visitor.visit_kotlin_while_statement(self)


# ============================================================================
# Declarations
# ============================================================================

@dataclass
class KotlinDeclaration(KotlinNode):
    """Base class for Kotlin declarations."""
    modifiers: List[KotlinModifier] = field(default_factory=list)
    annotations: List['KotlinAnnotation'] = field(default_factory=list)


@dataclass
class KotlinParameter(KotlinNode):
    """Function/constructor parameter"""
    name: str = ""
    type: Optional[KotlinType] = None
    default_value: Optional[KotlinExpression] = None
    is_vararg: bool = False
    is_crossinline: bool = False
    is_noinline: bool = False
    
    def accept(self, visitor):
        return visitor.visit_kotlin_parameter(self)


@dataclass
class KotlinArgument(KotlinNode):
    """Function call argument"""
    name: Optional[str] = None  # Named argument
    expression: Optional[KotlinExpression] = None
    is_spread: bool = False  # *args
    
    def accept(self, visitor):
        return visitor.visit_kotlin_argument(self)


@dataclass
class KotlinPropertyDeclaration(KotlinDeclaration):
    """Property declaration: val/var name: Type = value"""
    kotlin_node_type: KotlinNodeType = KotlinNodeType.PROPERTY_DECLARATION
    name: str = ""
    type: Optional[KotlinType] = None
    initializer: Optional[KotlinExpression] = None
    is_mutable: bool = False  # var vs val
    getter: Optional['KotlinPropertyAccessor'] = None
    setter: Optional['KotlinPropertyAccessor'] = None
    delegate: Optional[KotlinExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_kotlin_property_declaration(self)


@dataclass
class KotlinFunctionDeclaration(KotlinDeclaration):
    """Function declaration: fun name(params): ReturnType { ... }"""
    kotlin_node_type: KotlinNodeType = KotlinNodeType.FUNCTION_DECLARATION
    name: str = ""
    type_parameters: List[KotlinTypeParameter] = field(default_factory=list)
    parameters: List[KotlinParameter] = field(default_factory=list)
    return_type: Optional[KotlinType] = None
    body: Optional[KotlinStatement] = None
    is_suspend: bool = False
    is_inline: bool = False
    is_operator: bool = False
    is_infix: bool = False
    
    def accept(self, visitor):
        return visitor.visit_kotlin_function_declaration(self)


@dataclass
class KotlinClassDeclaration(KotlinDeclaration):
    """Class declaration: class Name(params) : SuperType { ... }"""
    kotlin_node_type: KotlinNodeType = KotlinNodeType.CLASS_DECLARATION
    name: str = ""
    kind: KotlinClassKind = KotlinClassKind.CLASS
    type_parameters: List[KotlinTypeParameter] = field(default_factory=list)
    primary_constructor: Optional['KotlinConstructorDeclaration'] = None
    super_types: List[KotlinType] = field(default_factory=list)
    body: List[KotlinDeclaration] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_kotlin_class_declaration(self)


@dataclass
class KotlinObjectDeclaration(KotlinDeclaration):
    """Object declaration: object Name { ... }"""
    kotlin_node_type: KotlinNodeType = KotlinNodeType.OBJECT_DECLARATION
    name: str = ""
    super_types: List[KotlinType] = field(default_factory=list)
    body: List[KotlinDeclaration] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_kotlin_object_declaration(self)


@dataclass
class KotlinConstructorDeclaration(KotlinDeclaration):
    """Constructor declaration"""
    kotlin_node_type: KotlinNodeType = KotlinNodeType.CONSTRUCTOR_DECLARATION
    parameters: List[KotlinParameter] = field(default_factory=list)
    body: Optional[KotlinBlock] = None
    is_primary: bool = False
    
    def accept(self, visitor):
        return visitor.visit_kotlin_constructor_declaration(self)


# ============================================================================
# Special Constructs
# ============================================================================

@dataclass
class KotlinAnnotation(KotlinNode):
    """Annotation: @Test, @Inject"""
    kotlin_node_type: KotlinNodeType = KotlinNodeType.ANNOTATION
    name: str = ""
    arguments: List[KotlinArgument] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_kotlin_annotation(self)


@dataclass
class KotlinWhenEntry(KotlinNode):
    """When entry: condition -> expression"""
    conditions: List[KotlinExpression] = field(default_factory=list)
    expression: Optional[KotlinExpression] = None
    is_else: bool = False
    
    def accept(self, visitor):
        return visitor.visit_kotlin_when_entry(self)


@dataclass
class KotlinCatchClause(KotlinNode):
    """Catch clause: catch (e: Exception) { ... }"""
    parameter: Optional[KotlinParameter] = None
    block: Optional[KotlinBlock] = None
    
    def accept(self, visitor):
        return visitor.visit_kotlin_catch_clause(self)


@dataclass
class KotlinPropertyAccessor(KotlinNode):
    """Property getter/setter"""
    body: Optional[KotlinStatement] = None
    is_getter: bool = True
    modifiers: List[KotlinModifier] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_kotlin_property_accessor(self)


# ============================================================================
# File and Program Structure
# ============================================================================

@dataclass
class KotlinFile(KotlinNode):
    """Kotlin source file"""
    kotlin_node_type: KotlinNodeType = KotlinNodeType.FILE
    package_declaration: Optional[KotlinPackageDeclaration] = None
    imports: List[KotlinImportDeclaration] = field(default_factory=list)
    declarations: List[KotlinDeclaration] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_kotlin_file(self)


@dataclass
class KotlinProgram(KotlinNode):
    """Complete Kotlin program"""
    kotlin_node_type: KotlinNodeType = KotlinNodeType.PROGRAM
    files: List[KotlinFile] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_kotlin_program(self)


# ============================================================================
# Utility Functions
# ============================================================================

def create_kotlin_identifier(name: str) -> KotlinIdentifier:
    """Create a Kotlin identifier node."""
    return KotlinIdentifier(name=name)


def create_kotlin_literal(value: Any, literal_type: str = "string") -> KotlinLiteralExpression:
    """Create a Kotlin literal expression node."""
    return KotlinLiteralExpression(value=value, literal_type=literal_type)


def create_kotlin_class(name: str, kind: KotlinClassKind = KotlinClassKind.CLASS) -> KotlinClassDeclaration:
    """Create a Kotlin class declaration node."""
    return KotlinClassDeclaration(name=name, kind=kind)


def create_kotlin_function(name: str, is_suspend: bool = False) -> KotlinFunctionDeclaration:
    """Create a Kotlin function declaration node."""
    return KotlinFunctionDeclaration(name=name, is_suspend=is_suspend)


def create_kotlin_property(name: str, is_mutable: bool = False) -> KotlinPropertyDeclaration:
    """Create a Kotlin property declaration node."""
    return KotlinPropertyDeclaration(name=name, is_mutable=is_mutable)


# ============================================================================
# Constants and Built-ins
# ============================================================================

# Kotlin built-in types
KOTLIN_BUILTIN_TYPES = {
    # Number types
    "Byte", "Short", "Int", "Long", "Float", "Double",
    
    # Character and boolean
    "Char", "Boolean",
    
    # String
    "String",
    
    # Collections
    "Array", "List", "MutableList", "Set", "MutableSet", 
    "Map", "MutableMap", "Collection", "MutableCollection",
    
    # Special types
    "Any", "Nothing", "Unit",
    
    # Function types
    "Function", "Function0", "Function1", "Function2",
    
    # Nullable versions (automatically handled)
}

# Kotlin keywords
KOTLIN_KEYWORDS = {
    "as", "as?", "break", "class", "continue", "do", "else", "false", "for",
    "fun", "if", "in", "!in", "interface", "is", "!is", "null", "object",
    "package", "return", "super", "this", "throw", "true", "try", "typealias",
    "typeof", "val", "var", "when", "while", "by", "catch", "constructor",
    "delegate", "dynamic", "field", "file", "finally", "get", "import",
    "init", "param", "property", "receiver", "set", "setparam", "where",
    
    # Soft keywords
    "abstract", "annotation", "companion", "const", "crossinline", "data",
    "enum", "external", "final", "infix", "inline", "inner", "internal",
    "lateinit", "noinline", "open", "operator", "out", "override", "private",
    "protected", "public", "reified", "sealed", "suspend", "tailrec", "vararg",
    
    # Coroutines
    "async", "await", "yield", "suspend"
}

# Kotlin operators
KOTLIN_OPERATORS = {
    # Arithmetic
    "+", "-", "*", "/", "%",
    
    # Assignment
    "=", "+=", "-=", "*=", "/=", "%=",
    
    # Comparison
    "==", "!=", "<", ">", "<=", ">=",
    
    # Logical
    "&&", "||", "!",
    
    # Bitwise
    "and", "or", "xor", "inv", "shl", "shr", "ushr",
    
    # Special Kotlin operators
    "?:", "!!", "?.", "..", "...", "in", "!in", "is", "!is", "as", "as?",
    
    # Increment/decrement
    "++", "--",
    
    # Range
    "..", "until", "downTo", "step",
    
    # Invoke
    "()", "[]", "get", "set", "contains", "iterator", "next", "hasNext"
} 