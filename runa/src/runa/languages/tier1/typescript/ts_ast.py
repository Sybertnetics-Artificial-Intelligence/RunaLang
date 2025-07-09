#!/usr/bin/env python3
"""
TypeScript AST Node Definitions

Comprehensive Abstract Syntax Tree nodes for TypeScript covering
all language features including type annotations, generics, interfaces,
enums, and advanced TypeScript-specific constructs.
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod


class TSNodeType(Enum):
    """TypeScript AST node types."""
    # Base types (inherited from JavaScript)
    LITERAL = auto()
    IDENTIFIER = auto()
    TEMPLATE_LITERAL = auto()
    
    # Expressions
    ARRAY_EXPRESSION = auto()
    OBJECT_EXPRESSION = auto()
    FUNCTION_EXPRESSION = auto()
    ARROW_FUNCTION_EXPRESSION = auto()
    CLASS_EXPRESSION = auto()
    
    # Binary and Unary
    BINARY_EXPRESSION = auto()
    UNARY_EXPRESSION = auto()
    UPDATE_EXPRESSION = auto()
    ASSIGNMENT_EXPRESSION = auto()
    LOGICAL_EXPRESSION = auto()
    CONDITIONAL_EXPRESSION = auto()
    
    # Member and Call
    MEMBER_EXPRESSION = auto()
    CALL_EXPRESSION = auto()
    NEW_EXPRESSION = auto()
    
    # This and Super
    THIS_EXPRESSION = auto()
    SUPER = auto()
    
    # Statements
    EXPRESSION_STATEMENT = auto()
    BLOCK_STATEMENT = auto()
    EMPTY_STATEMENT = auto()
    
    # Control Flow
    IF_STATEMENT = auto()
    SWITCH_STATEMENT = auto()
    WHILE_STATEMENT = auto()
    DO_WHILE_STATEMENT = auto()
    FOR_STATEMENT = auto()
    FOR_IN_STATEMENT = auto()
    FOR_OF_STATEMENT = auto()
    
    # Jumps
    BREAK_STATEMENT = auto()
    CONTINUE_STATEMENT = auto()
    RETURN_STATEMENT = auto()
    THROW_STATEMENT = auto()
    TRY_STATEMENT = auto()
    
    # Declarations
    VARIABLE_DECLARATION = auto()
    FUNCTION_DECLARATION = auto()
    CLASS_DECLARATION = auto()
    
    # TypeScript-specific nodes
    TYPE_ANNOTATION = auto()
    TYPE_REFERENCE = auto()
    UNION_TYPE = auto()
    INTERSECTION_TYPE = auto()
    TUPLE_TYPE = auto()
    ARRAY_TYPE = auto()
    FUNCTION_TYPE = auto()
    TYPE_LITERAL = auto()
    MAPPED_TYPE = auto()
    CONDITIONAL_TYPE = auto()
    INDEX_TYPE = auto()
    TYPEOF_TYPE = auto()
    KEYOF_TYPE = auto()
    
    # Interface and Type declarations
    INTERFACE_DECLARATION = auto()
    TYPE_ALIAS_DECLARATION = auto()
    ENUM_DECLARATION = auto()
    NAMESPACE_DECLARATION = auto()
    MODULE_DECLARATION = auto()
    
    # Generics
    TYPE_PARAMETER = auto()
    TYPE_PARAMETER_DECLARATION = auto()
    TYPE_ASSERTION = auto()
    TYPE_PREDICATE = auto()
    
    # Decorators
    DECORATOR = auto()
    
    # Import/Export enhancements
    IMPORT_TYPE = auto()
    EXPORT_ASSIGNMENT = auto()
    IMPORT_EQUALS_DECLARATION = auto()
    
    # Method signatures
    METHOD_SIGNATURE = auto()
    PROPERTY_SIGNATURE = auto()
    CALL_SIGNATURE = auto()
    CONSTRUCT_SIGNATURE = auto()
    INDEX_SIGNATURE = auto()
    
    # Access modifiers
    PUBLIC_KEYWORD = auto()
    PRIVATE_KEYWORD = auto()
    PROTECTED_KEYWORD = auto()
    READONLY_KEYWORD = auto()
    STATIC_KEYWORD = auto()
    ABSTRACT_KEYWORD = auto()
    
    # Program
    PROGRAM = auto()


class TSLiteralType(Enum):
    """TypeScript literal types."""
    NULL = "null"
    UNDEFINED = "undefined"
    BOOLEAN = "boolean"
    NUMBER = "number"
    STRING = "string"
    REGEX = "regex"
    BIGINT = "bigint"
    TEMPLATE = "template"


class TSOperator(Enum):
    """TypeScript operators (extends JavaScript)."""
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
    STRICT_EQUAL = "==="
    STRICT_NOT_EQUAL = "!=="
    LESS_THAN = "<"
    LESS_EQUAL = "<="
    GREATER_THAN = ">"
    GREATER_EQUAL = ">="
    
    # Logical
    AND = "&&"
    OR = "||"
    NULLISH_COALESCING = "??"
    
    # Bitwise
    BITWISE_AND = "&"
    BITWISE_OR = "|"
    BITWISE_XOR = "^"
    BITWISE_NOT = "~"
    LEFT_SHIFT = "<<"
    RIGHT_SHIFT = ">>"
    UNSIGNED_RIGHT_SHIFT = ">>>"
    
    # Unary
    TYPEOF = "typeof"
    VOID = "void"
    DELETE = "delete"
    NOT = "!"
    UNARY_PLUS = "+"
    UNARY_MINUS = "-"
    
    # Update
    INCREMENT = "++"
    DECREMENT = "--"
    
    # Assignment
    ASSIGN = "="
    PLUS_ASSIGN = "+="
    MINUS_ASSIGN = "-="
    MULTIPLY_ASSIGN = "*="
    DIVIDE_ASSIGN = "/="
    MODULO_ASSIGN = "%="
    EXPONENT_ASSIGN = "**="
    LEFT_SHIFT_ASSIGN = "<<="
    RIGHT_SHIFT_ASSIGN = ">>="
    UNSIGNED_RIGHT_SHIFT_ASSIGN = ">>>="
    BITWISE_AND_ASSIGN = "&="
    BITWISE_OR_ASSIGN = "|="
    BITWISE_XOR_ASSIGN = "^="
    LOGICAL_AND_ASSIGN = "&&="
    LOGICAL_OR_ASSIGN = "||="
    NULLISH_COALESCING_ASSIGN = "??="
    
    # TypeScript-specific
    IN = "in"
    INSTANCEOF = "instanceof"
    KEYOF = "keyof"
    IS = "is"
    SATISFIES = "satisfies"
    AS = "as"
    NON_NULL_ASSERTION = "!"
    OPTIONAL_CHAINING = "?."


class TSVariableKind(Enum):
    """TypeScript variable declaration kinds."""
    VAR = "var"
    LET = "let"
    CONST = "const"


class TSAccessModifier(Enum):
    """TypeScript access modifiers."""
    PUBLIC = "public"
    PRIVATE = "private"
    PROTECTED = "protected"
    READONLY = "readonly"
    STATIC = "static"
    ABSTRACT = "abstract"


class TSTypeKeyword(Enum):
    """TypeScript type keywords."""
    ANY = "any"
    UNKNOWN = "unknown"
    NEVER = "never"
    VOID = "void"
    UNDEFINED = "undefined"
    NULL = "null"
    BOOLEAN = "boolean"
    NUMBER = "number"
    STRING = "string"
    SYMBOL = "symbol"
    BIGINT = "bigint"
    OBJECT = "object"


@dataclass
class TSNode(ABC):
    """Base class for all TypeScript AST nodes."""
    type: TSNodeType = None
    loc: Optional[Dict[str, Any]] = None
    range: Optional[List[int]] = None
    
    @abstractmethod
    def accept(self, visitor):
        """Accept a visitor for the visitor pattern."""
        pass


@dataclass
class TSType(TSNode):
    """Base class for TypeScript type nodes."""
    pass


@dataclass
class TSLiteral(TSNode):
    """TypeScript literal node."""
    value: Any
    raw: str
    literal_type: TSLiteralType
    
    def __post_init__(self):
        self.type = TSNodeType.LITERAL
    
    def accept(self, visitor):
        return visitor.visit_literal(self)


@dataclass
class TSIdentifier(TSNode):
    """TypeScript identifier node."""
    name: str
    
    def __post_init__(self):
        self.type = TSNodeType.IDENTIFIER
    
    def accept(self, visitor):
        return visitor.visit_identifier(self)


@dataclass
class TSTypeAnnotation(TSNode):
    """TypeScript type annotation node."""
    type_annotation: TSType
    
    def __post_init__(self):
        self.type = TSNodeType.TYPE_ANNOTATION
    
    def accept(self, visitor):
        return visitor.visit_type_annotation(self)


@dataclass
class TSTypeReference(TSType):
    """TypeScript type reference node."""
    type_name: TSIdentifier
    type_arguments: Optional[List[TSType]] = None
    
    def __post_init__(self):
        self.type = TSNodeType.TYPE_REFERENCE
        if self.type_arguments is None:
            self.type_arguments = []
    
    def accept(self, visitor):
        return visitor.visit_type_reference(self)


@dataclass
class TSUnionType(TSType):
    """TypeScript union type node."""
    types: List[TSType]
    
    def __post_init__(self):
        self.type = TSNodeType.UNION_TYPE
    
    def accept(self, visitor):
        return visitor.visit_union_type(self)


@dataclass
class TSIntersectionType(TSType):
    """TypeScript intersection type node."""
    types: List[TSType]
    
    def __post_init__(self):
        self.type = TSNodeType.INTERSECTION_TYPE
    
    def accept(self, visitor):
        return visitor.visit_intersection_type(self)


@dataclass
class TSTupleType(TSType):
    """TypeScript tuple type node."""
    element_types: List[TSType]
    
    def __post_init__(self):
        self.type = TSNodeType.TUPLE_TYPE
    
    def accept(self, visitor):
        return visitor.visit_tuple_type(self)


@dataclass
class TSArrayType(TSType):
    """TypeScript array type node."""
    element_type: TSType
    
    def __post_init__(self):
        self.type = TSNodeType.ARRAY_TYPE
    
    def accept(self, visitor):
        return visitor.visit_array_type(self)


@dataclass
class TSFunctionType(TSType):
    """TypeScript function type node."""
    parameters: List['TSParameter']
    return_type: TSType
    type_parameters: Optional[List['TSTypeParameter']] = None
    
    def __post_init__(self):
        self.type = TSNodeType.FUNCTION_TYPE
        if self.type_parameters is None:
            self.type_parameters = []
    
    def accept(self, visitor):
        return visitor.visit_function_type(self)


@dataclass
class TSTypeLiteral(TSType):
    """TypeScript type literal node."""
    members: List[TSNode]
    
    def __post_init__(self):
        self.type = TSNodeType.TYPE_LITERAL
    
    def accept(self, visitor):
        return visitor.visit_type_literal(self)


@dataclass
class TSMappedType(TSType):
    """TypeScript mapped type node."""
    type_parameter: 'TSTypeParameter'
    type_annotation: Optional[TSType] = None
    name_type: Optional[TSType] = None
    readonly_token: Optional[str] = None
    question_token: Optional[str] = None
    
    def __post_init__(self):
        self.type = TSNodeType.MAPPED_TYPE
    
    def accept(self, visitor):
        return visitor.visit_mapped_type(self)


@dataclass
class TSConditionalType(TSType):
    """TypeScript conditional type node."""
    check_type: TSType
    extends_type: TSType
    true_type: TSType
    false_type: TSType
    
    def __post_init__(self):
        self.type = TSNodeType.CONDITIONAL_TYPE
    
    def accept(self, visitor):
        return visitor.visit_conditional_type(self)


@dataclass
class TSIndexedAccessType(TSType):
    """TypeScript indexed access type node."""
    object_type: TSType
    index_type: TSType
    
    def __post_init__(self):
        self.type = TSNodeType.INDEX_TYPE
    
    def accept(self, visitor):
        return visitor.visit_indexed_access_type(self)


@dataclass
class TSTypeofType(TSType):
    """TypeScript typeof type node."""
    expression: TSNode
    
    def __post_init__(self):
        self.type = TSNodeType.TYPEOF_TYPE
    
    def accept(self, visitor):
        return visitor.visit_typeof_type(self)


@dataclass
class TSKeyofType(TSType):
    """TypeScript keyof type node."""
    type_operand: TSType
    
    def __post_init__(self):
        self.type = TSNodeType.KEYOF_TYPE
    
    def accept(self, visitor):
        return visitor.visit_keyof_type(self)


@dataclass
class TSTypeParameter(TSNode):
    """TypeScript type parameter node."""
    name: TSIdentifier
    constraint: Optional[TSType] = None
    default_type: Optional[TSType] = None
    
    def __post_init__(self):
        self.type = TSNodeType.TYPE_PARAMETER
    
    def accept(self, visitor):
        return visitor.visit_type_parameter(self)


@dataclass
class TSTypeAssertion(TSNode):
    """TypeScript type assertion node."""
    type_annotation: TSType
    expression: TSNode
    
    def __post_init__(self):
        self.type = TSNodeType.TYPE_ASSERTION
    
    def accept(self, visitor):
        return visitor.visit_type_assertion(self)


@dataclass
class TSTypePredicate(TSType):
    """TypeScript type predicate node."""
    parameter_name: TSIdentifier
    type_annotation: Optional[TSType] = None
    asserts_modifier: bool = False
    
    def __post_init__(self):
        self.type = TSNodeType.TYPE_PREDICATE
    
    def accept(self, visitor):
        return visitor.visit_type_predicate(self)


@dataclass
class TSParameter(TSNode):
    """TypeScript parameter node."""
    name: TSIdentifier
    type_annotation: Optional[TSTypeAnnotation] = None
    default_value: Optional[TSNode] = None
    optional: bool = False
    rest: bool = False
    access_modifier: Optional[TSAccessModifier] = None
    readonly: bool = False
    
    def accept(self, visitor):
        return visitor.visit_parameter(self)


@dataclass
class TSInterfaceDeclaration(TSNode):
    """TypeScript interface declaration node."""
    name: TSIdentifier
    type_parameters: Optional[List[TSTypeParameter]] = None
    extends_clause: Optional[List[TSTypeReference]] = None
    body: List[TSNode] = None
    
    def __post_init__(self):
        self.type = TSNodeType.INTERFACE_DECLARATION
        if self.type_parameters is None:
            self.type_parameters = []
        if self.extends_clause is None:
            self.extends_clause = []
        if self.body is None:
            self.body = []
    
    def accept(self, visitor):
        return visitor.visit_interface_declaration(self)


@dataclass
class TSTypeAliasDeclaration(TSNode):
    """TypeScript type alias declaration node."""
    name: TSIdentifier
    type_parameters: Optional[List[TSTypeParameter]] = None
    type_annotation: TSType = None
    
    def __post_init__(self):
        self.type = TSNodeType.TYPE_ALIAS_DECLARATION
        if self.type_parameters is None:
            self.type_parameters = []
    
    def accept(self, visitor):
        return visitor.visit_type_alias_declaration(self)


@dataclass
class TSEnumDeclaration(TSNode):
    """TypeScript enum declaration node."""
    name: TSIdentifier
    members: List['TSEnumMember']
    const: bool = False
    
    def __post_init__(self):
        self.type = TSNodeType.ENUM_DECLARATION
    
    def accept(self, visitor):
        return visitor.visit_enum_declaration(self)


@dataclass
class TSEnumMember(TSNode):
    """TypeScript enum member node."""
    name: TSIdentifier
    initializer: Optional[TSNode] = None
    
    def accept(self, visitor):
        return visitor.visit_enum_member(self)


@dataclass
class TSNamespaceDeclaration(TSNode):
    """TypeScript namespace declaration node."""
    name: TSIdentifier
    body: List[TSNode]
    
    def __post_init__(self):
        self.type = TSNodeType.NAMESPACE_DECLARATION
    
    def accept(self, visitor):
        return visitor.visit_namespace_declaration(self)


@dataclass
class TSModuleDeclaration(TSNode):
    """TypeScript module declaration node."""
    name: TSIdentifier
    body: Optional[List[TSNode]] = None
    
    def __post_init__(self):
        self.type = TSNodeType.MODULE_DECLARATION
        if self.body is None:
            self.body = []
    
    def accept(self, visitor):
        return visitor.visit_module_declaration(self)


@dataclass
class TSDecorator(TSNode):
    """TypeScript decorator node."""
    expression: TSNode
    
    def __post_init__(self):
        self.type = TSNodeType.DECORATOR
    
    def accept(self, visitor):
        return visitor.visit_decorator(self)


@dataclass
class TSMethodSignature(TSNode):
    """TypeScript method signature node."""
    name: TSIdentifier
    parameters: List[TSParameter]
    return_type: Optional[TSTypeAnnotation] = None
    type_parameters: Optional[List[TSTypeParameter]] = None
    optional: bool = False
    
    def __post_init__(self):
        self.type = TSNodeType.METHOD_SIGNATURE
        if self.type_parameters is None:
            self.type_parameters = []
    
    def accept(self, visitor):
        return visitor.visit_method_signature(self)


@dataclass
class TSPropertySignature(TSNode):
    """TypeScript property signature node."""
    name: TSIdentifier
    type_annotation: Optional[TSTypeAnnotation] = None
    optional: bool = False
    readonly: bool = False
    
    def __post_init__(self):
        self.type = TSNodeType.PROPERTY_SIGNATURE
    
    def accept(self, visitor):
        return visitor.visit_property_signature(self)


@dataclass
class TSCallSignature(TSNode):
    """TypeScript call signature node."""
    parameters: List[TSParameter]
    return_type: Optional[TSTypeAnnotation] = None
    type_parameters: Optional[List[TSTypeParameter]] = None
    
    def __post_init__(self):
        self.type = TSNodeType.CALL_SIGNATURE
        if self.type_parameters is None:
            self.type_parameters = []
    
    def accept(self, visitor):
        return visitor.visit_call_signature(self)


@dataclass
class TSConstructSignature(TSNode):
    """TypeScript construct signature node."""
    parameters: List[TSParameter]
    return_type: Optional[TSTypeAnnotation] = None
    type_parameters: Optional[List[TSTypeParameter]] = None
    
    def __post_init__(self):
        self.type = TSNodeType.CONSTRUCT_SIGNATURE
        if self.type_parameters is None:
            self.type_parameters = []
    
    def accept(self, visitor):
        return visitor.visit_construct_signature(self)


@dataclass
class TSIndexSignature(TSNode):
    """TypeScript index signature node."""
    parameters: List[TSParameter]
    type_annotation: TSTypeAnnotation
    readonly: bool = False
    
    def __post_init__(self):
        self.type = TSNodeType.INDEX_SIGNATURE
    
    def accept(self, visitor):
        return visitor.visit_index_signature(self)


# Inherit JavaScript nodes with TypeScript extensions
@dataclass
class TSVariableDeclaration(TSNode):
    """TypeScript variable declaration node."""
    declarations: List['TSVariableDeclarator']
    kind: TSVariableKind
    
    def __post_init__(self):
        self.type = TSNodeType.VARIABLE_DECLARATION
    
    def accept(self, visitor):
        return visitor.visit_variable_declaration(self)


@dataclass
class TSVariableDeclarator(TSNode):
    """TypeScript variable declarator node."""
    id: TSIdentifier
    type_annotation: Optional[TSTypeAnnotation] = None
    init: Optional[TSNode] = None
    
    def accept(self, visitor):
        return visitor.visit_variable_declarator(self)


@dataclass
class TSFunctionDeclaration(TSNode):
    """TypeScript function declaration node."""
    name: TSIdentifier
    parameters: List[TSParameter]
    body: 'TSBlockStatement'
    return_type: Optional[TSTypeAnnotation] = None
    type_parameters: Optional[List[TSTypeParameter]] = None
    generator: bool = False
    async_: bool = False
    overload: bool = False
    
    def __post_init__(self):
        self.type = TSNodeType.FUNCTION_DECLARATION
        if self.type_parameters is None:
            self.type_parameters = []
    
    def accept(self, visitor):
        return visitor.visit_function_declaration(self)


@dataclass
class TSClassDeclaration(TSNode):
    """TypeScript class declaration node."""
    name: TSIdentifier
    type_parameters: Optional[List[TSTypeParameter]] = None
    super_class: Optional[TSNode] = None
    implements_clause: Optional[List[TSTypeReference]] = None
    body: List[TSNode] = None
    decorators: Optional[List[TSDecorator]] = None
    abstract: bool = False
    
    def __post_init__(self):
        self.type = TSNodeType.CLASS_DECLARATION
        if self.type_parameters is None:
            self.type_parameters = []
        if self.implements_clause is None:
            self.implements_clause = []
        if self.body is None:
            self.body = []
        if self.decorators is None:
            self.decorators = []
    
    def accept(self, visitor):
        return visitor.visit_class_declaration(self)


@dataclass
class TSBlockStatement(TSNode):
    """TypeScript block statement node."""
    body: List[TSNode]
    
    def __post_init__(self):
        self.type = TSNodeType.BLOCK_STATEMENT
    
    def accept(self, visitor):
        return visitor.visit_block_statement(self)


@dataclass
class TSProgram(TSNode):
    """TypeScript program node."""
    body: List[TSNode]
    source_type: str = "module"  # "script" or "module"
    
    def __post_init__(self):
        self.type = TSNodeType.PROGRAM
    
    def accept(self, visitor):
        return visitor.visit_program(self)


class TSNodeVisitor(ABC):
    """Abstract base class for TypeScript AST visitors."""
    
    @abstractmethod
    def visit_literal(self, node: TSLiteral): pass
    
    @abstractmethod
    def visit_identifier(self, node: TSIdentifier): pass
    
    @abstractmethod
    def visit_type_annotation(self, node: TSTypeAnnotation): pass
    
    @abstractmethod
    def visit_type_reference(self, node: TSTypeReference): pass
    
    @abstractmethod
    def visit_union_type(self, node: TSUnionType): pass
    
    @abstractmethod
    def visit_intersection_type(self, node: TSIntersectionType): pass
    
    @abstractmethod
    def visit_tuple_type(self, node: TSTupleType): pass
    
    @abstractmethod
    def visit_array_type(self, node: TSArrayType): pass
    
    @abstractmethod
    def visit_function_type(self, node: TSFunctionType): pass
    
    @abstractmethod
    def visit_type_literal(self, node: TSTypeLiteral): pass
    
    @abstractmethod
    def visit_mapped_type(self, node: TSMappedType): pass
    
    @abstractmethod
    def visit_conditional_type(self, node: TSConditionalType): pass
    
    @abstractmethod
    def visit_indexed_access_type(self, node: TSIndexedAccessType): pass
    
    @abstractmethod
    def visit_typeof_type(self, node: TSTypeofType): pass
    
    @abstractmethod
    def visit_keyof_type(self, node: TSKeyofType): pass
    
    @abstractmethod
    def visit_type_parameter(self, node: TSTypeParameter): pass
    
    @abstractmethod
    def visit_type_assertion(self, node: TSTypeAssertion): pass
    
    @abstractmethod
    def visit_type_predicate(self, node: TSTypePredicate): pass
    
    @abstractmethod
    def visit_parameter(self, node: TSParameter): pass
    
    @abstractmethod
    def visit_interface_declaration(self, node: TSInterfaceDeclaration): pass
    
    @abstractmethod
    def visit_type_alias_declaration(self, node: TSTypeAliasDeclaration): pass
    
    @abstractmethod
    def visit_enum_declaration(self, node: TSEnumDeclaration): pass
    
    @abstractmethod
    def visit_enum_member(self, node: TSEnumMember): pass
    
    @abstractmethod
    def visit_namespace_declaration(self, node: TSNamespaceDeclaration): pass
    
    @abstractmethod
    def visit_module_declaration(self, node: TSModuleDeclaration): pass
    
    @abstractmethod
    def visit_decorator(self, node: TSDecorator): pass
    
    @abstractmethod
    def visit_method_signature(self, node: TSMethodSignature): pass
    
    @abstractmethod
    def visit_property_signature(self, node: TSPropertySignature): pass
    
    @abstractmethod
    def visit_call_signature(self, node: TSCallSignature): pass
    
    @abstractmethod
    def visit_construct_signature(self, node: TSConstructSignature): pass
    
    @abstractmethod
    def visit_index_signature(self, node: TSIndexSignature): pass
    
    @abstractmethod
    def visit_variable_declaration(self, node: TSVariableDeclaration): pass
    
    @abstractmethod
    def visit_variable_declarator(self, node: TSVariableDeclarator): pass
    
    @abstractmethod
    def visit_function_declaration(self, node: TSFunctionDeclaration): pass
    
    @abstractmethod
    def visit_class_declaration(self, node: TSClassDeclaration): pass
    
    @abstractmethod
    def visit_block_statement(self, node: TSBlockStatement): pass
    
    @abstractmethod
    def visit_program(self, node: TSProgram): pass