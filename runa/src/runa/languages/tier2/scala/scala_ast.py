#!/usr/bin/env python3
"""
Scala AST Node Definitions

Comprehensive Abstract Syntax Tree nodes for Scala language covering all Scala features
including classes, traits, objects, case classes, pattern matching, higher-order functions,
implicits, type classes, macros, and functional programming constructs.

Author: Sybertnetics AI Solutions
License: MIT
"""

from typing import List, Optional, Any, Union, Dict
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod

from ....core.runa_ast import ASTNode, SourceLocation, TranslationMetadata


class ScalaNodeType(Enum):
    """Scala-specific AST node types."""
    # Program structure
    SOURCE_FILE = auto()
    PACKAGE_DECLARATION = auto()
    IMPORT_DECLARATION = auto()
    
    # Type system
    TYPE_IDENTIFIER = auto()
    TYPE_PARAMETER = auto()
    TYPE_PROJECTION = auto()
    COMPOUND_TYPE = auto()
    FUNCTION_TYPE = auto()
    TUPLE_TYPE = auto()
    EXISTENTIAL_TYPE = auto()
    SINGLETON_TYPE = auto()
    REFINED_TYPE = auto()
    
    # Declarations
    CLASS_DECLARATION = auto()
    TRAIT_DECLARATION = auto()
    OBJECT_DECLARATION = auto()
    CASE_CLASS_DECLARATION = auto()
    ENUM_DECLARATION = auto()
    FUNCTION_DECLARATION = auto()
    VALUE_DECLARATION = auto()
    VARIABLE_DECLARATION = auto()
    TYPE_ALIAS_DECLARATION = auto()
    
    # Expressions
    IDENTIFIER_EXPRESSION = auto()
    LITERAL_EXPRESSION = auto()
    THIS_EXPRESSION = auto()
    SUPER_EXPRESSION = auto()
    BLOCK_EXPRESSION = auto()
    IF_EXPRESSION = auto()
    MATCH_EXPRESSION = auto()
    TRY_EXPRESSION = auto()
    FOR_EXPRESSION = auto()
    WHILE_EXPRESSION = auto()
    DO_WHILE_EXPRESSION = auto()
    FUNCTION_CALL_EXPRESSION = auto()
    METHOD_CALL_EXPRESSION = auto()
    LAMBDA_EXPRESSION = auto()
    TUPLE_EXPRESSION = auto()
    LIST_EXPRESSION = auto()
    MAP_EXPRESSION = auto()
    SET_EXPRESSION = auto()
    INTERPOLATED_STRING = auto()
    TYPE_ASCRIPTION = auto()
    ASSIGNMENT_EXPRESSION = auto()
    BINARY_EXPRESSION = auto()
    UNARY_EXPRESSION = auto()
    POSTFIX_EXPRESSION = auto()
    NEW_EXPRESSION = auto()
    
    # Patterns
    WILDCARD_PATTERN = auto()
    IDENTIFIER_PATTERN = auto()
    LITERAL_PATTERN = auto()
    CONSTRUCTOR_PATTERN = auto()
    TUPLE_PATTERN = auto()
    LIST_PATTERN = auto()
    TYPED_PATTERN = auto()
    GUARD_PATTERN = auto()
    ALTERNATIVE_PATTERN = auto()
    
    # Modifiers and annotations
    MODIFIER = auto()
    ANNOTATION = auto()
    
    # Scala-specific constructs
    IMPLICIT_PARAMETER = auto()
    IMPLICIT_CONVERSION = auto()
    TYPE_CLASS = auto()
    MACRO = auto()
    GIVEN_INSTANCE = auto()
    USING_PARAMETER = auto()


class ScalaAccessModifier(Enum):
    """Scala access modifiers."""
    PUBLIC = "public"
    PRIVATE = "private"
    PROTECTED = "protected"


class ScalaModifier(Enum):
    """Scala modifiers."""
    ABSTRACT = "abstract"
    FINAL = "final"
    SEALED = "sealed"
    IMPLICIT = "implicit"
    LAZY = "lazy"
    OVERRIDE = "override"
    CASE = "case"
    GIVEN = "given"  # Scala 3
    USING = "using"  # Scala 3
    EXTENSION = "extension"  # Scala 3


@dataclass
class ScalaNode(ASTNode):
    """Base class for all Scala AST nodes."""
    scala_node_type: ScalaNodeType = ScalaNodeType.SOURCE_FILE
    
    @abstractmethod
    def accept(self, visitor):
        """Accept a visitor for AST traversal."""
        pass


@dataclass
class ScalaAnnotation(ScalaNode):
    """Scala annotation: @annotation(args)"""
    scala_node_type: ScalaNodeType = ScalaNodeType.ANNOTATION
    name: str = ""
    arguments: List['ScalaExpression'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_scala_annotation(self)


@dataclass
class ScalaModifierNode(ScalaNode):
    """Scala modifier node."""
    scala_node_type: ScalaNodeType = ScalaNodeType.MODIFIER
    modifier: ScalaModifier = ScalaModifier.PUBLIC
    access_qualifier: Optional[str] = None  # For private[this], protected[package]
    
    def accept(self, visitor):
        return visitor.visit_scala_modifier(self)


# ============================================================================
# Types
# ============================================================================

@dataclass
class ScalaType(ScalaNode):
    """Base class for Scala types."""
    pass


@dataclass
class ScalaTypeIdentifier(ScalaType):
    """Type identifier: Int, String, MyClass[T]"""
    scala_node_type: ScalaNodeType = ScalaNodeType.TYPE_IDENTIFIER
    name: str = ""
    type_arguments: List[ScalaType] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_scala_type_identifier(self)


@dataclass
class ScalaTypeParameter(ScalaType):
    """Type parameter: [T <: UpperBound >: LowerBound]"""
    scala_node_type: ScalaNodeType = ScalaNodeType.TYPE_PARAMETER
    name: str = ""
    variance: Optional[str] = None  # +, -, None
    upper_bound: Optional[ScalaType] = None
    lower_bound: Optional[ScalaType] = None
    context_bounds: List[ScalaType] = field(default_factory=list)
    view_bounds: List[ScalaType] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_scala_type_parameter(self)


@dataclass
class ScalaFunctionType(ScalaType):
    """Function type: (A, B) => C"""
    scala_node_type: ScalaNodeType = ScalaNodeType.FUNCTION_TYPE
    parameter_types: List[ScalaType] = field(default_factory=list)
    return_type: Optional[ScalaType] = None
    
    def accept(self, visitor):
        return visitor.visit_scala_function_type(self)


@dataclass
class ScalaTupleType(ScalaType):
    """Tuple type: (A, B, C)"""
    scala_node_type: ScalaNodeType = ScalaNodeType.TUPLE_TYPE
    element_types: List[ScalaType] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_scala_tuple_type(self)


@dataclass
class ScalaCompoundType(ScalaType):
    """Compound type: A with B with C"""
    scala_node_type: ScalaNodeType = ScalaNodeType.COMPOUND_TYPE
    types: List[ScalaType] = field(default_factory=list)
    refinements: List['ScalaDeclaration'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_scala_compound_type(self)


@dataclass
class ScalaRefinedType(ScalaType):
    """Refined type: A { def method: B }"""
    scala_node_type: ScalaNodeType = ScalaNodeType.REFINED_TYPE
    base_type: Optional[ScalaType] = None
    refinements: List['ScalaDeclaration'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_scala_refined_type(self)


@dataclass
class ScalaExistentialType(ScalaType):
    """Existential type: A forSome { type T }"""
    scala_node_type: ScalaNodeType = ScalaNodeType.EXISTENTIAL_TYPE
    base_type: Optional[ScalaType] = None
    quantified: List['ScalaDeclaration'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_scala_existential_type(self)


# ============================================================================
# Declarations
# ============================================================================

@dataclass
class ScalaDeclaration(ScalaNode):
    """Base class for Scala declarations."""
    annotations: List[ScalaAnnotation] = field(default_factory=list)
    modifiers: List[ScalaModifierNode] = field(default_factory=list)


@dataclass
class ScalaPackageDeclaration(ScalaDeclaration):
    """Package declaration: package com.example"""
    scala_node_type: ScalaNodeType = ScalaNodeType.PACKAGE_DECLARATION
    name: str = ""
    
    def accept(self, visitor):
        return visitor.visit_scala_package_declaration(self)


@dataclass
class ScalaImportDeclaration(ScalaDeclaration):
    """Import declaration: import scala.collection._"""
    scala_node_type: ScalaNodeType = ScalaNodeType.IMPORT_DECLARATION
    path: str = ""
    selectors: List[str] = field(default_factory=list)  # For import a.{b, c => d}
    
    def accept(self, visitor):
        return visitor.visit_scala_import_declaration(self)


@dataclass
class ScalaClassDeclaration(ScalaDeclaration):
    """Class declaration: class MyClass[T](param: T) extends SuperClass with Trait"""
    scala_node_type: ScalaNodeType = ScalaNodeType.CLASS_DECLARATION
    name: str = ""
    type_parameters: List[ScalaTypeParameter] = field(default_factory=list)
    constructor_parameters: List['ScalaParameter'] = field(default_factory=list)
    extends_clause: Optional[ScalaType] = None
    with_clauses: List[ScalaType] = field(default_factory=list)
    members: List['ScalaMember'] = field(default_factory=list)
    is_abstract: bool = False
    is_final: bool = False
    is_sealed: bool = False
    is_case: bool = False
    
    def accept(self, visitor):
        return visitor.visit_scala_class_declaration(self)


@dataclass
class ScalaTraitDeclaration(ScalaDeclaration):
    """Trait declaration: trait MyTrait[T] extends SuperTrait"""
    scala_node_type: ScalaNodeType = ScalaNodeType.TRAIT_DECLARATION
    name: str = ""
    type_parameters: List[ScalaTypeParameter] = field(default_factory=list)
    extends_clause: Optional[ScalaType] = None
    with_clauses: List[ScalaType] = field(default_factory=list)
    members: List['ScalaMember'] = field(default_factory=list)
    is_sealed: bool = False
    
    def accept(self, visitor):
        return visitor.visit_scala_trait_declaration(self)


@dataclass
class ScalaObjectDeclaration(ScalaDeclaration):
    """Object declaration: object MyObject extends SuperClass"""
    scala_node_type: ScalaNodeType = ScalaNodeType.OBJECT_DECLARATION
    name: str = ""
    extends_clause: Optional[ScalaType] = None
    with_clauses: List[ScalaType] = field(default_factory=list)
    members: List['ScalaMember'] = field(default_factory=list)
    is_case: bool = False
    
    def accept(self, visitor):
        return visitor.visit_scala_object_declaration(self)


@dataclass
class ScalaEnumDeclaration(ScalaDeclaration):
    """Enum declaration: enum Color { case Red, Green, Blue }"""
    scala_node_type: ScalaNodeType = ScalaNodeType.ENUM_DECLARATION
    name: str = ""
    type_parameters: List[ScalaTypeParameter] = field(default_factory=list)
    cases: List['ScalaEnumCase'] = field(default_factory=list)
    members: List['ScalaMember'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_scala_enum_declaration(self)


@dataclass
class ScalaFunctionDeclaration(ScalaDeclaration):
    """Function declaration: def myFunction[T](param: T): Unit = body"""
    scala_node_type: ScalaNodeType = ScalaNodeType.FUNCTION_DECLARATION
    name: str = ""
    type_parameters: List[ScalaTypeParameter] = field(default_factory=list)
    parameter_lists: List[List['ScalaParameter']] = field(default_factory=list)
    return_type: Optional[ScalaType] = None
    body: Optional['ScalaExpression'] = None
    is_abstract: bool = False
    is_override: bool = False
    is_implicit: bool = False
    is_inline: bool = False  # Scala 3
    
    def accept(self, visitor):
        return visitor.visit_scala_function_declaration(self)


@dataclass
class ScalaValueDeclaration(ScalaDeclaration):
    """Value declaration: val name: Type = value"""
    scala_node_type: ScalaNodeType = ScalaNodeType.VALUE_DECLARATION
    name: str = ""
    type_annotation: Optional[ScalaType] = None
    value: Optional['ScalaExpression'] = None
    is_lazy: bool = False
    is_implicit: bool = False
    is_override: bool = False
    
    def accept(self, visitor):
        return visitor.visit_scala_value_declaration(self)


@dataclass
class ScalaVariableDeclaration(ScalaDeclaration):
    """Variable declaration: var name: Type = value"""
    scala_node_type: ScalaNodeType = ScalaNodeType.VARIABLE_DECLARATION
    name: str = ""
    type_annotation: Optional[ScalaType] = None
    value: Optional['ScalaExpression'] = None
    is_override: bool = False
    
    def accept(self, visitor):
        return visitor.visit_scala_variable_declaration(self)


@dataclass
class ScalaTypeAliasDeclaration(ScalaDeclaration):
    """Type alias declaration: type MyType[T] = SomeType[T]"""
    scala_node_type: ScalaNodeType = ScalaNodeType.TYPE_ALIAS_DECLARATION
    name: str = ""
    type_parameters: List[ScalaTypeParameter] = field(default_factory=list)
    alias_type: Optional[ScalaType] = None
    
    def accept(self, visitor):
        return visitor.visit_scala_type_alias_declaration(self)


# ============================================================================
# Expressions
# ============================================================================

@dataclass
class ScalaExpression(ScalaNode):
    """Base class for Scala expressions."""
    pass


@dataclass
class ScalaIdentifier(ScalaExpression):
    """Identifier expression: myVariable"""
    scala_node_type: ScalaNodeType = ScalaNodeType.IDENTIFIER_EXPRESSION
    name: str = ""
    
    def accept(self, visitor):
        return visitor.visit_scala_identifier(self)


@dataclass
class ScalaLiteral(ScalaExpression):
    """Literal expression: 42, "string", true, null"""
    scala_node_type: ScalaNodeType = ScalaNodeType.LITERAL_EXPRESSION
    value: Any = None
    literal_type: str = "string"  # int, long, float, double, string, char, bool, null, symbol
    
    def accept(self, visitor):
        return visitor.visit_scala_literal(self)


@dataclass
class ScalaThisExpression(ScalaExpression):
    """This expression: this or this[Type]"""
    scala_node_type: ScalaNodeType = ScalaNodeType.THIS_EXPRESSION
    qualifier: Optional[ScalaType] = None
    
    def accept(self, visitor):
        return visitor.visit_scala_this_expression(self)


@dataclass
class ScalaSuperExpression(ScalaExpression):
    """Super expression: super or super[Type]"""
    scala_node_type: ScalaNodeType = ScalaNodeType.SUPER_EXPRESSION
    qualifier: Optional[ScalaType] = None
    
    def accept(self, visitor):
        return visitor.visit_scala_super_expression(self)


@dataclass
class ScalaBlockExpression(ScalaExpression):
    """Block expression: { statements; expression }"""
    scala_node_type: ScalaNodeType = ScalaNodeType.BLOCK_EXPRESSION
    statements: List['ScalaStatement'] = field(default_factory=list)
    result_expression: Optional[ScalaExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_scala_block_expression(self)


@dataclass
class ScalaIfExpression(ScalaExpression):
    """If expression: if (condition) thenExpr else elseExpr"""
    scala_node_type: ScalaNodeType = ScalaNodeType.IF_EXPRESSION
    condition: Optional[ScalaExpression] = None
    then_expression: Optional[ScalaExpression] = None
    else_expression: Optional[ScalaExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_scala_if_expression(self)


@dataclass
class ScalaMatchExpression(ScalaExpression):
    """Match expression: expr match { case pattern => expr }"""
    scala_node_type: ScalaNodeType = ScalaNodeType.MATCH_EXPRESSION
    scrutinee: Optional[ScalaExpression] = None
    cases: List['ScalaMatchCase'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_scala_match_expression(self)


@dataclass
class ScalaTryExpression(ScalaExpression):
    """Try expression: try expr catch { cases } finally expr"""
    scala_node_type: ScalaNodeType = ScalaNodeType.TRY_EXPRESSION
    try_expression: Optional[ScalaExpression] = None
    catch_cases: List['ScalaMatchCase'] = field(default_factory=list)
    finally_expression: Optional[ScalaExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_scala_try_expression(self)


@dataclass
class ScalaForExpression(ScalaExpression):
    """For expression: for { generators } yield expr"""
    scala_node_type: ScalaNodeType = ScalaNodeType.FOR_EXPRESSION
    generators: List['ScalaGenerator'] = field(default_factory=list)
    yield_expression: Optional[ScalaExpression] = None
    is_yield: bool = True  # True for for-yield, False for for-do
    
    def accept(self, visitor):
        return visitor.visit_scala_for_expression(self)


@dataclass
class ScalaWhileExpression(ScalaExpression):
    """While expression: while (condition) body"""
    scala_node_type: ScalaNodeType = ScalaNodeType.WHILE_EXPRESSION
    condition: Optional[ScalaExpression] = None
    body: Optional[ScalaExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_scala_while_expression(self)


@dataclass
class ScalaFunctionCallExpression(ScalaExpression):
    """Function call: func(args)"""
    scala_node_type: ScalaNodeType = ScalaNodeType.FUNCTION_CALL_EXPRESSION
    function: Optional[ScalaExpression] = None
    arguments: List[List['ScalaArgument']] = field(default_factory=list)  # Multiple argument lists
    type_arguments: List[ScalaType] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_scala_function_call_expression(self)


@dataclass
class ScalaMethodCallExpression(ScalaExpression):
    """Method call: obj.method(args)"""
    scala_node_type: ScalaNodeType = ScalaNodeType.METHOD_CALL_EXPRESSION
    receiver: Optional[ScalaExpression] = None
    method_name: str = ""
    arguments: List[List['ScalaArgument']] = field(default_factory=list)
    type_arguments: List[ScalaType] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_scala_method_call_expression(self)


@dataclass
class ScalaLambdaExpression(ScalaExpression):
    """Lambda expression: (x, y) => x + y"""
    scala_node_type: ScalaNodeType = ScalaNodeType.LAMBDA_EXPRESSION
    parameters: List['ScalaParameter'] = field(default_factory=list)
    body: Optional[ScalaExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_scala_lambda_expression(self)


@dataclass
class ScalaTupleExpression(ScalaExpression):
    """Tuple expression: (a, b, c)"""
    scala_node_type: ScalaNodeType = ScalaNodeType.TUPLE_EXPRESSION
    elements: List[ScalaExpression] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_scala_tuple_expression(self)


@dataclass
class ScalaListExpression(ScalaExpression):
    """List expression: List(1, 2, 3)"""
    scala_node_type: ScalaNodeType = ScalaNodeType.LIST_EXPRESSION
    elements: List[ScalaExpression] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_scala_list_expression(self)


@dataclass
class ScalaBinaryExpression(ScalaExpression):
    """Binary expression: a + b"""
    scala_node_type: ScalaNodeType = ScalaNodeType.BINARY_EXPRESSION
    left: Optional[ScalaExpression] = None
    operator: str = ""
    right: Optional[ScalaExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_scala_binary_expression(self)


@dataclass
class ScalaUnaryExpression(ScalaExpression):
    """Unary expression: !condition, -number"""
    scala_node_type: ScalaNodeType = ScalaNodeType.UNARY_EXPRESSION
    operator: str = ""
    operand: Optional[ScalaExpression] = None
    is_prefix: bool = True
    
    def accept(self, visitor):
        return visitor.visit_scala_unary_expression(self)


@dataclass
class ScalaAssignmentExpression(ScalaExpression):
    """Assignment expression: variable = value"""
    scala_node_type: ScalaNodeType = ScalaNodeType.ASSIGNMENT_EXPRESSION
    target: Optional[ScalaExpression] = None
    value: Optional[ScalaExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_scala_assignment_expression(self)


@dataclass
class ScalaNewExpression(ScalaExpression):
    """New expression: new MyClass(args)"""
    scala_node_type: ScalaNodeType = ScalaNodeType.NEW_EXPRESSION
    class_type: Optional[ScalaType] = None
    arguments: List[List['ScalaArgument']] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_scala_new_expression(self)


@dataclass
class ScalaTypeAscription(ScalaExpression):
    """Type ascription: expr: Type"""
    scala_node_type: ScalaNodeType = ScalaNodeType.TYPE_ASCRIPTION
    expression: Optional[ScalaExpression] = None
    ascribed_type: Optional[ScalaType] = None
    
    def accept(self, visitor):
        return visitor.visit_scala_type_ascription(self)


@dataclass
class ScalaInterpolatedString(ScalaExpression):
    """Interpolated string: s"Hello $name" """
    scala_node_type: ScalaNodeType = ScalaNodeType.INTERPOLATED_STRING
    interpolator: str = "s"  # s, f, raw, etc.
    parts: List[str] = field(default_factory=list)
    expressions: List[ScalaExpression] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_scala_interpolated_string(self)


# ============================================================================
# Patterns
# ============================================================================

@dataclass
class ScalaPattern(ScalaNode):
    """Base class for Scala patterns."""
    pass


@dataclass
class ScalaWildcardPattern(ScalaPattern):
    """Wildcard pattern: _"""
    scala_node_type: ScalaNodeType = ScalaNodeType.WILDCARD_PATTERN
    
    def accept(self, visitor):
        return visitor.visit_scala_wildcard_pattern(self)


@dataclass
class ScalaIdentifierPattern(ScalaPattern):
    """Identifier pattern: name"""
    scala_node_type: ScalaNodeType = ScalaNodeType.IDENTIFIER_PATTERN
    name: str = ""
    
    def accept(self, visitor):
        return visitor.visit_scala_identifier_pattern(self)


@dataclass
class ScalaLiteralPattern(ScalaPattern):
    """Literal pattern: 42, "string", true"""
    scala_node_type: ScalaNodeType = ScalaNodeType.LITERAL_PATTERN
    literal: Optional[ScalaLiteral] = None
    
    def accept(self, visitor):
        return visitor.visit_scala_literal_pattern(self)


@dataclass
class ScalaConstructorPattern(ScalaPattern):
    """Constructor pattern: Case(pattern1, pattern2)"""
    scala_node_type: ScalaNodeType = ScalaNodeType.CONSTRUCTOR_PATTERN
    constructor: Optional[ScalaExpression] = None
    patterns: List[ScalaPattern] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_scala_constructor_pattern(self)


@dataclass
class ScalaTuplePattern(ScalaPattern):
    """Tuple pattern: (pattern1, pattern2)"""
    scala_node_type: ScalaNodeType = ScalaNodeType.TUPLE_PATTERN
    patterns: List[ScalaPattern] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_scala_tuple_pattern(self)


@dataclass
class ScalaTypedPattern(ScalaPattern):
    """Typed pattern: name: Type"""
    scala_node_type: ScalaNodeType = ScalaNodeType.TYPED_PATTERN
    pattern: Optional[ScalaPattern] = None
    pattern_type: Optional[ScalaType] = None
    
    def accept(self, visitor):
        return visitor.visit_scala_typed_pattern(self)


@dataclass
class ScalaGuardPattern(ScalaPattern):
    """Guard pattern: pattern if condition"""
    scala_node_type: ScalaNodeType = ScalaNodeType.GUARD_PATTERN
    pattern: Optional[ScalaPattern] = None
    guard: Optional[ScalaExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_scala_guard_pattern(self)


@dataclass
class ScalaAlternativePattern(ScalaPattern):
    """Alternative pattern: pattern1 | pattern2"""
    scala_node_type: ScalaNodeType = ScalaNodeType.ALTERNATIVE_PATTERN
    patterns: List[ScalaPattern] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_scala_alternative_pattern(self)


# ============================================================================
# Support Structures
# ============================================================================

@dataclass
class ScalaParameter:
    """Function/method parameter"""
    name: str = ""
    parameter_type: Optional[ScalaType] = None
    default_value: Optional[ScalaExpression] = None
    is_implicit: bool = False
    is_by_name: bool = False  # => Type
    is_varargs: bool = False  # Type*
    is_using: bool = False  # Scala 3 using parameters
    
    def accept(self, visitor):
        return visitor.visit_scala_parameter(self)


@dataclass
class ScalaArgument:
    """Function call argument"""
    name: Optional[str] = None  # Named argument
    value: Optional[ScalaExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_scala_argument(self)


@dataclass
class ScalaMatchCase:
    """Match case: case pattern => expression"""
    pattern: Optional[ScalaPattern] = None
    guard: Optional[ScalaExpression] = None
    body: Optional[ScalaExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_scala_match_case(self)


@dataclass
class ScalaGenerator:
    """For generator: pattern <- expression"""
    pattern: Optional[ScalaPattern] = None
    expression: Optional[ScalaExpression] = None
    guards: List[ScalaExpression] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_scala_generator(self)


@dataclass
class ScalaEnumCase:
    """Enum case"""
    name: str = ""
    parameters: List[ScalaParameter] = field(default_factory=list)
    extends_clauses: List[ScalaType] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_scala_enum_case(self)


@dataclass
class ScalaMember(ScalaNode):
    """Base class for class/trait/object members."""
    pass


@dataclass
class ScalaStatement(ScalaNode):
    """Base class for Scala statements."""
    pass


# ============================================================================
# File Structure
# ============================================================================

@dataclass
class ScalaSourceFile(ScalaNode):
    """Scala source file"""
    scala_node_type: ScalaNodeType = ScalaNodeType.SOURCE_FILE
    package_declaration: Optional[ScalaPackageDeclaration] = None
    imports: List[ScalaImportDeclaration] = field(default_factory=list)
    declarations: List[ScalaDeclaration] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_scala_source_file(self)


# ============================================================================
# Visitor Pattern
# ============================================================================

class ScalaVisitor(ABC):
    """Abstract visitor for Scala AST nodes."""
    
    @abstractmethod
    def visit_scala_source_file(self, node: ScalaSourceFile): pass
    
    @abstractmethod
    def visit_scala_class_declaration(self, node: ScalaClassDeclaration): pass
    
    @abstractmethod
    def visit_scala_trait_declaration(self, node: ScalaTraitDeclaration): pass
    
    @abstractmethod
    def visit_scala_object_declaration(self, node: ScalaObjectDeclaration): pass
    
    @abstractmethod
    def visit_scala_function_declaration(self, node: ScalaFunctionDeclaration): pass
    
    @abstractmethod
    def visit_scala_identifier(self, node: ScalaIdentifier): pass
    
    @abstractmethod
    def visit_scala_literal(self, node: ScalaLiteral): pass
    
    @abstractmethod
    def visit_scala_block_expression(self, node: ScalaBlockExpression): pass


# ============================================================================
# Utility Functions
# ============================================================================

def create_scala_identifier(name: str) -> ScalaIdentifier:
    """Create a Scala identifier expression."""
    return ScalaIdentifier(name=name)


def create_scala_literal(value: Any, literal_type: str = "string") -> ScalaLiteral:
    """Create a Scala literal expression."""
    return ScalaLiteral(value=value, literal_type=literal_type)


def create_scala_class(name: str) -> ScalaClassDeclaration:
    """Create a Scala class declaration."""
    return ScalaClassDeclaration(name=name)


def create_scala_trait(name: str) -> ScalaTraitDeclaration:
    """Create a Scala trait declaration."""
    return ScalaTraitDeclaration(name=name)


def create_scala_object(name: str) -> ScalaObjectDeclaration:
    """Create a Scala object declaration."""
    return ScalaObjectDeclaration(name=name)


def create_scala_function(name: str) -> ScalaFunctionDeclaration:
    """Create a Scala function declaration."""
    return ScalaFunctionDeclaration(name=name)


# ============================================================================
# Constants
# ============================================================================

# Scala keywords
SCALA_KEYWORDS = {
    "abstract", "case", "catch", "class", "def", "do", "else", "extends", "final",
    "finally", "for", "forSome", "if", "implicit", "import", "lazy", "macro",
    "match", "new", "object", "override", "package", "private", "protected",
    "return", "sealed", "super", "this", "throw", "trait", "try", "type", "val",
    "var", "while", "with", "yield", "true", "false", "null", "_",
    # Scala 3 keywords
    "enum", "export", "extension", "given", "inline", "opaque", "open", "then",
    "transparent", "using", "as", "derives", "end", "infix", "throws", "erased"
}

# Scala operators
SCALA_OPERATORS = {
    "+", "-", "*", "/", "%", "==", "!=", "<", ">", "<=", ">=", "&&", "||", "!",
    "&", "|", "^", "~", "<<", ">>", ">>>", "++", "--", "+=", "-=", "*=", "/=",
    "%=", "&=", "|=", "^=", "<<=", ">>=", ">>>=", "=>", "<-", "->", "<:", ">:",
    "<%", "#", "@", "::", ":::", "++:", ":+", "+:", "++", ":::+", "+:::", "???",
    "=:=", "=!=", "<~<", ">~>"
}

# Scala built-in types
SCALA_BUILTIN_TYPES = {
    "Any", "AnyRef", "AnyVal", "Nothing", "Null", "Unit", "Boolean", "Byte",
    "Short", "Int", "Long", "Float", "Double", "Char", "String", "Symbol",
    "Array", "List", "Vector", "Set", "Map", "Option", "Some", "None",
    "Either", "Left", "Right", "Try", "Success", "Failure", "Future"
}