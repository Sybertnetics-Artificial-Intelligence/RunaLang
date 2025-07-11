#!/usr/bin/env python3
"""
Swift AST Node Definitions

Comprehensive Abstract Syntax Tree nodes for Swift language covering all Swift features
including classes, structs, enums, protocols, extensions, generics, optionals, closures,
async/await, actors, property wrappers, and SwiftUI DSL constructs.

Author: Sybertnetics AI Solutions
License: MIT
"""

from typing import List, Optional, Any, Union, Dict
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod

from ....core.runa_ast import ASTNode, SourceLocation, TranslationMetadata


class SwiftNodeType(Enum):
    """Swift-specific AST node types."""
    # Program structure
    SOURCE_FILE = auto()
    IMPORT_DECLARATION = auto()
    
    # Types
    TYPE_IDENTIFIER = auto()
    OPTIONAL_TYPE = auto()
    IMPLICITLY_UNWRAPPED_OPTIONAL_TYPE = auto()
    ARRAY_TYPE = auto()
    DICTIONARY_TYPE = auto()
    FUNCTION_TYPE = auto()
    TUPLE_TYPE = auto()
    PROTOCOL_COMPOSITION_TYPE = auto()
    METATYPE = auto()
    
    # Declarations
    CLASS_DECLARATION = auto()
    STRUCT_DECLARATION = auto()
    ENUM_DECLARATION = auto()
    PROTOCOL_DECLARATION = auto()
    EXTENSION_DECLARATION = auto()
    FUNCTION_DECLARATION = auto()
    INITIALIZER_DECLARATION = auto()
    DEINITIALIZER_DECLARATION = auto()
    VARIABLE_DECLARATION = auto()
    TYPEALIAS_DECLARATION = auto()
    ASSOCIATED_TYPE_DECLARATION = auto()
    OPERATOR_DECLARATION = auto()
    PRECEDENCE_GROUP_DECLARATION = auto()
    
    # Statements
    EXPRESSION_STATEMENT = auto()
    RETURN_STATEMENT = auto()
    BREAK_STATEMENT = auto()
    CONTINUE_STATEMENT = auto()
    THROW_STATEMENT = auto()
    DEFER_STATEMENT = auto()
    DO_STATEMENT = auto()
    IF_STATEMENT = auto()
    GUARD_STATEMENT = auto()
    SWITCH_STATEMENT = auto()
    FOR_IN_STATEMENT = auto()
    WHILE_STATEMENT = auto()
    REPEAT_WHILE_STATEMENT = auto()
    
    # Expressions
    IDENTIFIER_EXPRESSION = auto()
    LITERAL_EXPRESSION = auto()
    SELF_EXPRESSION = auto()
    SUPER_EXPRESSION = auto()
    CLOSURE_EXPRESSION = auto()
    PARENTHESIZED_EXPRESSION = auto()
    TUPLE_EXPRESSION = auto()
    ARRAY_EXPRESSION = auto()
    DICTIONARY_EXPRESSION = auto()
    SUBSCRIPT_EXPRESSION = auto()
    MEMBER_ACCESS_EXPRESSION = auto()
    POSTFIX_UNARY_EXPRESSION = auto()
    PREFIX_UNARY_EXPRESSION = auto()
    BINARY_EXPRESSION = auto()
    TERNARY_EXPRESSION = auto()
    ASSIGNMENT_EXPRESSION = auto()
    FUNCTION_CALL_EXPRESSION = auto()
    INITIALIZER_EXPRESSION = auto()
    EXPLICIT_MEMBER_EXPRESSION = auto()
    POSTFIX_SELF_EXPRESSION = auto()
    FORCE_VALUE_EXPRESSION = auto()
    OPTIONAL_CHAINING_EXPRESSION = auto()
    
    # Patterns
    WILDCARD_PATTERN = auto()
    IDENTIFIER_PATTERN = auto()
    VALUE_BINDING_PATTERN = auto()
    TUPLE_PATTERN = auto()
    ENUM_CASE_PATTERN = auto()
    OPTIONAL_PATTERN = auto()
    TYPE_CASTING_PATTERN = auto()
    EXPRESSION_PATTERN = auto()
    
    # Generic and associated types
    GENERIC_PARAMETER = auto()
    GENERIC_ARGUMENT = auto()
    GENERIC_WHERE_CLAUSE = auto()
    GENERIC_REQUIREMENT = auto()
    
    # Attributes
    ATTRIBUTE = auto()
    AVAILABILITY_ATTRIBUTE = auto()
    
    # Swift-specific constructs
    ACTOR_DECLARATION = auto()
    ASYNC_EXPRESSION = auto()
    AWAIT_EXPRESSION = auto()
    PROPERTY_WRAPPER = auto()
    RESULT_BUILDER = auto()


class SwiftAccessLevel(Enum):
    """Swift access levels."""
    OPEN = "open"
    PUBLIC = "public"
    INTERNAL = "internal"
    FILEPRIVATE = "fileprivate"
    PRIVATE = "private"


class SwiftMutabilityKind(Enum):
    """Swift mutability kinds."""
    IMMUTABLE = "let"
    MUTABLE = "var"


@dataclass
class SwiftNode(ASTNode):
    """Base class for all Swift AST nodes."""
    swift_node_type: SwiftNodeType = SwiftNodeType.SOURCE_FILE
    
    @abstractmethod
    def accept(self, visitor):
        """Accept a visitor for AST traversal."""
        pass


@dataclass
class SwiftAttribute(SwiftNode):
    """Swift attribute: @objc, @available, etc."""
    swift_node_type: SwiftNodeType = SwiftNodeType.ATTRIBUTE
    name: str = ""
    arguments: List[str] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_swift_attribute(self)


# ============================================================================
# Types
# ============================================================================

@dataclass
class SwiftType(SwiftNode):
    """Base class for Swift types."""
    pass


@dataclass
class SwiftTypeIdentifier(SwiftType):
    """Type identifier: Int, String, MyClass<T>"""
    swift_node_type: SwiftNodeType = SwiftNodeType.TYPE_IDENTIFIER
    name: str = ""
    generic_arguments: List[SwiftType] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_swift_type_identifier(self)


@dataclass
class SwiftOptionalType(SwiftType):
    """Optional type: Int?"""
    swift_node_type: SwiftNodeType = SwiftNodeType.OPTIONAL_TYPE
    wrapped_type: Optional[SwiftType] = None
    
    def accept(self, visitor):
        return visitor.visit_swift_optional_type(self)


@dataclass
class SwiftImplicitlyUnwrappedOptionalType(SwiftType):
    """Implicitly unwrapped optional type: Int!"""
    swift_node_type: SwiftNodeType = SwiftNodeType.IMPLICITLY_UNWRAPPED_OPTIONAL_TYPE
    wrapped_type: Optional[SwiftType] = None
    
    def accept(self, visitor):
        return visitor.visit_swift_implicitly_unwrapped_optional_type(self)


@dataclass
class SwiftArrayType(SwiftType):
    """Array type: [Int]"""
    swift_node_type: SwiftNodeType = SwiftNodeType.ARRAY_TYPE
    element_type: Optional[SwiftType] = None
    
    def accept(self, visitor):
        return visitor.visit_swift_array_type(self)


@dataclass
class SwiftDictionaryType(SwiftType):
    """Dictionary type: [String: Int]"""
    swift_node_type: SwiftNodeType = SwiftNodeType.DICTIONARY_TYPE
    key_type: Optional[SwiftType] = None
    value_type: Optional[SwiftType] = None
    
    def accept(self, visitor):
        return visitor.visit_swift_dictionary_type(self)


@dataclass
class SwiftFunctionType(SwiftType):
    """Function type: (Int, String) -> Bool"""
    swift_node_type: SwiftNodeType = SwiftNodeType.FUNCTION_TYPE
    parameter_types: List[SwiftType] = field(default_factory=list)
    return_type: Optional[SwiftType] = None
    is_async: bool = False
    is_throws: bool = False
    
    def accept(self, visitor):
        return visitor.visit_swift_function_type(self)


@dataclass
class SwiftTupleType(SwiftType):
    """Tuple type: (Int, String, Bool)"""
    swift_node_type: SwiftNodeType = SwiftNodeType.TUPLE_TYPE
    element_types: List[SwiftType] = field(default_factory=list)
    element_names: List[Optional[str]] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_swift_tuple_type(self)


# ============================================================================
# Declarations
# ============================================================================

@dataclass
class SwiftDeclaration(SwiftNode):
    """Base class for Swift declarations."""
    attributes: List[SwiftAttribute] = field(default_factory=list)
    modifiers: List[str] = field(default_factory=list)
    access_level: SwiftAccessLevel = SwiftAccessLevel.INTERNAL


@dataclass
class SwiftImportDeclaration(SwiftDeclaration):
    """Import declaration: import Foundation"""
    swift_node_type: SwiftNodeType = SwiftNodeType.IMPORT_DECLARATION
    module_name: str = ""
    import_kind: Optional[str] = None  # class, struct, enum, protocol, typealias, func, var
    
    def accept(self, visitor):
        return visitor.visit_swift_import_declaration(self)


@dataclass
class SwiftClassDeclaration(SwiftDeclaration):
    """Class declaration: class MyClass: SuperClass { ... }"""
    swift_node_type: SwiftNodeType = SwiftNodeType.CLASS_DECLARATION
    name: str = ""
    generic_parameters: List['SwiftGenericParameter'] = field(default_factory=list)
    superclass: Optional[SwiftType] = None
    protocols: List[SwiftType] = field(default_factory=list)
    members: List[SwiftDeclaration] = field(default_factory=list)
    is_final: bool = False
    
    def accept(self, visitor):
        return visitor.visit_swift_class_declaration(self)


@dataclass
class SwiftStructDeclaration(SwiftDeclaration):
    """Struct declaration: struct MyStruct { ... }"""
    swift_node_type: SwiftNodeType = SwiftNodeType.STRUCT_DECLARATION
    name: str = ""
    generic_parameters: List['SwiftGenericParameter'] = field(default_factory=list)
    protocols: List[SwiftType] = field(default_factory=list)
    members: List[SwiftDeclaration] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_swift_struct_declaration(self)


@dataclass
class SwiftEnumDeclaration(SwiftDeclaration):
    """Enum declaration: enum MyEnum { case value1, value2 }"""
    swift_node_type: SwiftNodeType = SwiftNodeType.ENUM_DECLARATION
    name: str = ""
    generic_parameters: List['SwiftGenericParameter'] = field(default_factory=list)
    raw_type: Optional[SwiftType] = None
    protocols: List[SwiftType] = field(default_factory=list)
    cases: List['SwiftEnumCase'] = field(default_factory=list)
    members: List[SwiftDeclaration] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_swift_enum_declaration(self)


@dataclass
class SwiftProtocolDeclaration(SwiftDeclaration):
    """Protocol declaration: protocol MyProtocol { ... }"""
    swift_node_type: SwiftNodeType = SwiftNodeType.PROTOCOL_DECLARATION
    name: str = ""
    generic_parameters: List['SwiftGenericParameter'] = field(default_factory=list)
    protocols: List[SwiftType] = field(default_factory=list)
    members: List[SwiftDeclaration] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_swift_protocol_declaration(self)


@dataclass
class SwiftExtensionDeclaration(SwiftDeclaration):
    """Extension declaration: extension MyType { ... }"""
    swift_node_type: SwiftNodeType = SwiftNodeType.EXTENSION_DECLARATION
    extended_type: Optional[SwiftType] = None
    generic_parameters: List['SwiftGenericParameter'] = field(default_factory=list)
    protocols: List[SwiftType] = field(default_factory=list)
    members: List[SwiftDeclaration] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_swift_extension_declaration(self)


@dataclass
class SwiftFunctionDeclaration(SwiftDeclaration):
    """Function declaration: func myFunction(param: Int) -> String { ... }"""
    swift_node_type: SwiftNodeType = SwiftNodeType.FUNCTION_DECLARATION
    name: str = ""
    generic_parameters: List['SwiftGenericParameter'] = field(default_factory=list)
    parameters: List['SwiftParameter'] = field(default_factory=list)
    return_type: Optional[SwiftType] = None
    body: Optional['SwiftCodeBlock'] = None
    is_async: bool = False
    is_throws: bool = False
    is_static: bool = False
    is_mutating: bool = False
    
    def accept(self, visitor):
        return visitor.visit_swift_function_declaration(self)


@dataclass
class SwiftVariableDeclaration(SwiftDeclaration):
    """Variable declaration: var name: String = "value" """
    swift_node_type: SwiftNodeType = SwiftNodeType.VARIABLE_DECLARATION
    name: str = ""
    type_annotation: Optional[SwiftType] = None
    initializer: Optional['SwiftExpression'] = None
    mutability: SwiftMutabilityKind = SwiftMutabilityKind.IMMUTABLE
    getter: Optional['SwiftAccessor'] = None
    setter: Optional['SwiftAccessor'] = None
    
    def accept(self, visitor):
        return visitor.visit_swift_variable_declaration(self)


@dataclass
class SwiftActorDeclaration(SwiftDeclaration):
    """Actor declaration: actor MyActor { ... }"""
    swift_node_type: SwiftNodeType = SwiftNodeType.ACTOR_DECLARATION
    name: str = ""
    generic_parameters: List['SwiftGenericParameter'] = field(default_factory=list)
    protocols: List[SwiftType] = field(default_factory=list)
    members: List[SwiftDeclaration] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_swift_actor_declaration(self)


# ============================================================================
# Statements
# ============================================================================

@dataclass
class SwiftStatement(SwiftNode):
    """Base class for Swift statements."""
    pass


@dataclass
class SwiftCodeBlock(SwiftStatement):
    """Code block: { statements }"""
    statements: List[SwiftStatement] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_swift_code_block(self)


@dataclass
class SwiftIfStatement(SwiftStatement):
    """If statement: if condition { ... } else { ... }"""
    swift_node_type: SwiftNodeType = SwiftNodeType.IF_STATEMENT
    condition: Optional['SwiftExpression'] = None
    then_statement: Optional[SwiftStatement] = None
    else_statement: Optional[SwiftStatement] = None
    
    def accept(self, visitor):
        return visitor.visit_swift_if_statement(self)


@dataclass
class SwiftGuardStatement(SwiftStatement):
    """Guard statement: guard condition else { ... }"""
    swift_node_type: SwiftNodeType = SwiftNodeType.GUARD_STATEMENT
    condition: Optional['SwiftExpression'] = None
    else_statement: Optional[SwiftStatement] = None
    
    def accept(self, visitor):
        return visitor.visit_swift_guard_statement(self)


@dataclass
class SwiftSwitchStatement(SwiftStatement):
    """Switch statement: switch value { case pattern: ... }"""
    swift_node_type: SwiftNodeType = SwiftNodeType.SWITCH_STATEMENT
    expression: Optional['SwiftExpression'] = None
    cases: List['SwiftSwitchCase'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_swift_switch_statement(self)


@dataclass
class SwiftForInStatement(SwiftStatement):
    """For-in statement: for item in sequence { ... }"""
    swift_node_type: SwiftNodeType = SwiftNodeType.FOR_IN_STATEMENT
    pattern: Optional['SwiftPattern'] = None
    sequence: Optional['SwiftExpression'] = None
    body: Optional[SwiftStatement] = None
    
    def accept(self, visitor):
        return visitor.visit_swift_for_in_statement(self)


@dataclass
class SwiftWhileStatement(SwiftStatement):
    """While statement: while condition { ... }"""
    swift_node_type: SwiftNodeType = SwiftNodeType.WHILE_STATEMENT
    condition: Optional['SwiftExpression'] = None
    body: Optional[SwiftStatement] = None
    
    def accept(self, visitor):
        return visitor.visit_swift_while_statement(self)


@dataclass
class SwiftReturnStatement(SwiftStatement):
    """Return statement: return expression"""
    swift_node_type: SwiftNodeType = SwiftNodeType.RETURN_STATEMENT
    expression: Optional['SwiftExpression'] = None
    
    def accept(self, visitor):
        return visitor.visit_swift_return_statement(self)


@dataclass
class SwiftThrowStatement(SwiftStatement):
    """Throw statement: throw error"""
    swift_node_type: SwiftNodeType = SwiftNodeType.THROW_STATEMENT
    expression: Optional['SwiftExpression'] = None
    
    def accept(self, visitor):
        return visitor.visit_swift_throw_statement(self)


@dataclass
class SwiftDeferStatement(SwiftStatement):
    """Defer statement: defer { ... }"""
    swift_node_type: SwiftNodeType = SwiftNodeType.DEFER_STATEMENT
    body: Optional[SwiftStatement] = None
    
    def accept(self, visitor):
        return visitor.visit_swift_defer_statement(self)


# ============================================================================
# Expressions
# ============================================================================

@dataclass
class SwiftExpression(SwiftNode):
    """Base class for Swift expressions."""
    pass


@dataclass
class SwiftIdentifierExpression(SwiftExpression):
    """Identifier expression: variableName"""
    swift_node_type: SwiftNodeType = SwiftNodeType.IDENTIFIER_EXPRESSION
    name: str = ""
    
    def accept(self, visitor):
        return visitor.visit_swift_identifier_expression(self)


@dataclass
class SwiftLiteralExpression(SwiftExpression):
    """Literal expression: 42, "hello", true"""
    swift_node_type: SwiftNodeType = SwiftNodeType.LITERAL_EXPRESSION
    value: Any = None
    literal_type: str = "string"  # int, float, string, bool, nil
    
    def accept(self, visitor):
        return visitor.visit_swift_literal_expression(self)


@dataclass
class SwiftClosureExpression(SwiftExpression):
    """Closure expression: { parameters in statements }"""
    swift_node_type: SwiftNodeType = SwiftNodeType.CLOSURE_EXPRESSION
    parameters: List['SwiftParameter'] = field(default_factory=list)
    body: Optional[SwiftStatement] = None
    is_async: bool = False
    is_throws: bool = False
    
    def accept(self, visitor):
        return visitor.visit_swift_closure_expression(self)


@dataclass
class SwiftFunctionCallExpression(SwiftExpression):
    """Function call: function(arguments)"""
    swift_node_type: SwiftNodeType = SwiftNodeType.FUNCTION_CALL_EXPRESSION
    function: Optional[SwiftExpression] = None
    arguments: List['SwiftArgument'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_swift_function_call_expression(self)


@dataclass
class SwiftMemberAccessExpression(SwiftExpression):
    """Member access: object.property"""
    swift_node_type: SwiftNodeType = SwiftNodeType.MEMBER_ACCESS_EXPRESSION
    base: Optional[SwiftExpression] = None
    member: str = ""
    
    def accept(self, visitor):
        return visitor.visit_swift_member_access_expression(self)


@dataclass
class SwiftOptionalChainingExpression(SwiftExpression):
    """Optional chaining: object?.property"""
    swift_node_type: SwiftNodeType = SwiftNodeType.OPTIONAL_CHAINING_EXPRESSION
    base: Optional[SwiftExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_swift_optional_chaining_expression(self)


@dataclass
class SwiftForceValueExpression(SwiftExpression):
    """Force value expression: optional!"""
    swift_node_type: SwiftNodeType = SwiftNodeType.FORCE_VALUE_EXPRESSION
    expression: Optional[SwiftExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_swift_force_value_expression(self)


@dataclass
class SwiftBinaryExpression(SwiftExpression):
    """Binary expression: a + b"""
    swift_node_type: SwiftNodeType = SwiftNodeType.BINARY_EXPRESSION
    left: Optional[SwiftExpression] = None
    operator: str = ""
    right: Optional[SwiftExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_swift_binary_expression(self)


@dataclass
class SwiftTernaryExpression(SwiftExpression):
    """Ternary expression: condition ? true_value : false_value"""
    swift_node_type: SwiftNodeType = SwiftNodeType.TERNARY_EXPRESSION
    condition: Optional[SwiftExpression] = None
    true_expression: Optional[SwiftExpression] = None
    false_expression: Optional[SwiftExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_swift_ternary_expression(self)


@dataclass
class SwiftArrayExpression(SwiftExpression):
    """Array expression: [element1, element2]"""
    swift_node_type: SwiftNodeType = SwiftNodeType.ARRAY_EXPRESSION
    elements: List[SwiftExpression] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_swift_array_expression(self)


@dataclass
class SwiftDictionaryExpression(SwiftExpression):
    """Dictionary expression: [key1: value1, key2: value2]"""
    swift_node_type: SwiftNodeType = SwiftNodeType.DICTIONARY_EXPRESSION
    elements: List['SwiftDictionaryElement'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_swift_dictionary_expression(self)


@dataclass
class SwiftAwaitExpression(SwiftExpression):
    """Await expression: await asyncFunction()"""
    swift_node_type: SwiftNodeType = SwiftNodeType.AWAIT_EXPRESSION
    expression: Optional[SwiftExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_swift_await_expression(self)


@dataclass
class SwiftAsyncExpression(SwiftExpression):
    """Async expression: async { ... }"""
    swift_node_type: SwiftNodeType = SwiftNodeType.ASYNC_EXPRESSION
    body: Optional[SwiftStatement] = None
    
    def accept(self, visitor):
        return visitor.visit_swift_async_expression(self)


# ============================================================================
# Patterns
# ============================================================================

@dataclass
class SwiftPattern(SwiftNode):
    """Base class for Swift patterns."""
    pass


@dataclass
class SwiftIdentifierPattern(SwiftPattern):
    """Identifier pattern: name"""
    swift_node_type: SwiftNodeType = SwiftNodeType.IDENTIFIER_PATTERN
    name: str = ""
    
    def accept(self, visitor):
        return visitor.visit_swift_identifier_pattern(self)


@dataclass
class SwiftWildcardPattern(SwiftPattern):
    """Wildcard pattern: _"""
    swift_node_type: SwiftNodeType = SwiftNodeType.WILDCARD_PATTERN
    
    def accept(self, visitor):
        return visitor.visit_swift_wildcard_pattern(self)


@dataclass
class SwiftTuplePattern(SwiftPattern):
    """Tuple pattern: (pattern1, pattern2)"""
    swift_node_type: SwiftNodeType = SwiftNodeType.TUPLE_PATTERN
    elements: List[SwiftPattern] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_swift_tuple_pattern(self)


@dataclass
class SwiftOptionalPattern(SwiftPattern):
    """Optional pattern: pattern?"""
    swift_node_type: SwiftNodeType = SwiftNodeType.OPTIONAL_PATTERN
    pattern: Optional[SwiftPattern] = None
    
    def accept(self, visitor):
        return visitor.visit_swift_optional_pattern(self)


# ============================================================================
# Support Structures
# ============================================================================

@dataclass
class SwiftParameter:
    """Function parameter"""
    external_name: Optional[str] = None
    internal_name: str = ""
    type_annotation: Optional[SwiftType] = None
    default_value: Optional[SwiftExpression] = None
    is_variadic: bool = False
    is_inout: bool = False
    
    def accept(self, visitor):
        return visitor.visit_swift_parameter(self)


@dataclass
class SwiftArgument:
    """Function call argument"""
    label: Optional[str] = None
    expression: Optional[SwiftExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_swift_argument(self)


@dataclass
class SwiftEnumCase:
    """Enum case"""
    name: str = ""
    associated_values: List[SwiftType] = field(default_factory=list)
    raw_value: Optional[SwiftExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_swift_enum_case(self)


@dataclass
class SwiftSwitchCase:
    """Switch case"""
    patterns: List[SwiftPattern] = field(default_factory=list)
    guard_expression: Optional[SwiftExpression] = None
    body: Optional[SwiftStatement] = None
    is_default: bool = False
    
    def accept(self, visitor):
        return visitor.visit_swift_switch_case(self)


@dataclass
class SwiftDictionaryElement:
    """Dictionary element"""
    key: Optional[SwiftExpression] = None
    value: Optional[SwiftExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_swift_dictionary_element(self)


@dataclass
class SwiftGenericParameter:
    """Generic parameter"""
    name: str = ""
    constraints: List[SwiftType] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_swift_generic_parameter(self)


@dataclass
class SwiftAccessor:
    """Property accessor (getter/setter)"""
    kind: str = "get"  # get, set, willSet, didSet
    body: Optional[SwiftStatement] = None
    
    def accept(self, visitor):
        return visitor.visit_swift_accessor(self)


# ============================================================================
# File Structure
# ============================================================================

@dataclass
class SwiftSourceFile(SwiftNode):
    """Swift source file"""
    swift_node_type: SwiftNodeType = SwiftNodeType.SOURCE_FILE
    imports: List[SwiftImportDeclaration] = field(default_factory=list)
    declarations: List[SwiftDeclaration] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_swift_source_file(self)


# ============================================================================
# Visitor Pattern
# ============================================================================

class SwiftVisitor(ABC):
    """Abstract visitor for Swift AST nodes."""
    
    @abstractmethod
    def visit_swift_source_file(self, node: SwiftSourceFile): pass
    
    @abstractmethod
    def visit_swift_class_declaration(self, node: SwiftClassDeclaration): pass
    
    @abstractmethod
    def visit_swift_struct_declaration(self, node: SwiftStructDeclaration): pass
    
    @abstractmethod
    def visit_swift_enum_declaration(self, node: SwiftEnumDeclaration): pass
    
    @abstractmethod
    def visit_swift_function_declaration(self, node: SwiftFunctionDeclaration): pass
    
    @abstractmethod
    def visit_swift_variable_declaration(self, node: SwiftVariableDeclaration): pass
    
    @abstractmethod
    def visit_swift_identifier_expression(self, node: SwiftIdentifierExpression): pass
    
    @abstractmethod
    def visit_swift_literal_expression(self, node: SwiftLiteralExpression): pass
    
    @abstractmethod
    def visit_swift_code_block(self, node: SwiftCodeBlock): pass


# ============================================================================
# Utility Functions
# ============================================================================

def create_swift_identifier(name: str) -> SwiftIdentifierExpression:
    """Create a Swift identifier expression."""
    return SwiftIdentifierExpression(name=name)


def create_swift_literal(value: Any, literal_type: str = "string") -> SwiftLiteralExpression:
    """Create a Swift literal expression."""
    return SwiftLiteralExpression(value=value, literal_type=literal_type)


def create_swift_class(name: str) -> SwiftClassDeclaration:
    """Create a Swift class declaration."""
    return SwiftClassDeclaration(name=name)


def create_swift_struct(name: str) -> SwiftStructDeclaration:
    """Create a Swift struct declaration."""
    return SwiftStructDeclaration(name=name)


def create_swift_function(name: str) -> SwiftFunctionDeclaration:
    """Create a Swift function declaration."""
    return SwiftFunctionDeclaration(name=name)


# ============================================================================
# Constants
# ============================================================================

# Swift keywords
SWIFT_KEYWORDS = {
    "associatedtype", "class", "deinit", "enum", "extension", "fileprivate", "func",
    "import", "init", "inout", "internal", "let", "open", "operator", "private",
    "protocol", "public", "rethrows", "static", "struct", "subscript", "typealias",
    "var", "break", "case", "continue", "default", "defer", "do", "else", "fallthrough",
    "for", "guard", "if", "in", "repeat", "return", "switch", "where", "while",
    "as", "Any", "catch", "false", "is", "nil", "super", "self", "Self", "throw",
    "throws", "true", "try", "async", "await", "actor", "some", "inout", "mutating",
    "nonmutating", "override", "convenience", "dynamic", "didSet", "final", "get",
    "indirect", "lazy", "optional", "required", "set", "Type", "unowned", "weak",
    "willSet"
}

# Swift primitive types
SWIFT_PRIMITIVE_TYPES = {
    "Bool", "Int", "Int8", "Int16", "Int32", "Int64", "UInt", "UInt8", "UInt16",
    "UInt32", "UInt64", "Float", "Double", "String", "Character", "Void", "Any",
    "AnyObject", "Array", "Dictionary", "Set", "Optional"
}

# Swift operators
SWIFT_OPERATORS = {
    "+", "-", "*", "/", "%", "=", "==", "!=", "<", ">", "<=", ">=", "&&", "||",
    "!", "&", "|", "^", "~", "<<", ">>", "+=", "-=", "*=", "/=", "%=", "&=",
    "|=", "^=", "<<=", ">>=", "?", "??", "?.", "!", "...", "..<", "->", "=>",
    "@", "#", "$", "++", "--"
}