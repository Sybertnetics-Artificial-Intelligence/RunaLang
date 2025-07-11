#!/usr/bin/env python3
"""
OCaml AST Node Definitions

Comprehensive Abstract Syntax Tree nodes for OCaml covering
functional programming with objects, modules, functors, and
advanced ML-family language features.
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod


class OcamlNodeType(Enum):
    """OCaml AST node types."""
    # Literals
    LITERAL = auto()
    UNIT = auto()
    
    # Identifiers
    IDENTIFIER = auto()
    CONSTRUCTOR = auto()
    OPERATOR = auto()
    
    # Expressions
    APPLICATION = auto()
    FUNCTION = auto()
    LET = auto()
    LET_REC = auto()
    IF = auto()
    MATCH = auto()
    TRY = auto()
    SEQUENCE = auto()
    TUPLE = auto()
    LIST = auto()
    ARRAY = auto()
    RECORD = auto()
    FIELD_ACCESS = auto()
    OBJECT = auto()
    METHOD_CALL = auto()
    
    # Patterns
    WILDCARD_PATTERN = auto()
    VARIABLE_PATTERN = auto()
    CONSTRUCTOR_PATTERN = auto()
    TUPLE_PATTERN = auto()
    RECORD_PATTERN = auto()
    ARRAY_PATTERN = auto()
    OR_PATTERN = auto()
    GUARD_PATTERN = auto()
    
    # Types
    TYPE_VARIABLE = auto()
    TYPE_CONSTRUCTOR = auto()
    FUNCTION_TYPE = auto()
    TUPLE_TYPE = auto()
    VARIANT_TYPE = auto()
    RECORD_TYPE = auto()
    OBJECT_TYPE = auto()
    CLASS_TYPE = auto()
    
    # Declarations
    VALUE_DECLARATION = auto()
    TYPE_DECLARATION = auto()
    EXCEPTION_DECLARATION = auto()
    MODULE_DECLARATION = auto()
    MODULE_TYPE_DECLARATION = auto()
    CLASS_DECLARATION = auto()
    
    # Module system
    MODULE = auto()
    SIGNATURE = auto()
    FUNCTOR = auto()
    MODULE_BINDING = auto()
    
    # Classes and objects
    CLASS = auto()
    OBJECT_EXPR = auto()
    METHOD = auto()
    INSTANCE_VARIABLE = auto()


class OcamlOperator(Enum):
    """OCaml operators."""
    # Arithmetic
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    MOD = "mod"
    POWER = "**"
    
    # Comparison
    EQ = "="
    NEQ = "<>"
    LT = "<"
    LE = "<="
    GT = ">"
    GE = ">="
    PHYS_EQ = "=="
    PHYS_NEQ = "!="
    
    # Logical
    AND = "&&"
    OR = "||"
    NOT = "not"
    
    # List operations
    CONS = "::"
    APPEND = "@"
    
    # Reference operations
    REF = "ref"
    DEREF = "!"
    ASSIGN = ":="


@dataclass
class OcamlNode(ABC):
    """Base class for all OCaml AST nodes."""
    type: OcamlNodeType = None
    location: Optional[tuple] = None
    
    @abstractmethod
    def accept(self, visitor):
        """Accept a visitor for the visitor pattern."""
        pass


@dataclass
class OcamlExpression(OcamlNode):
    """Base class for OCaml expressions."""
    pass


@dataclass
class OcamlPattern(OcamlNode):
    """Base class for OCaml patterns."""
    pass


@dataclass
class OcamlType(OcamlNode):
    """Base class for OCaml types."""
    pass


@dataclass
class OcamlDeclaration(OcamlNode):
    """Base class for OCaml declarations."""
    pass


# Literals and basic expressions
@dataclass
class OcamlLiteral(OcamlExpression):
    """OCaml literal."""
    value: Any
    literal_type: str  # "int", "float", "string", "char", "bool"
    
    def __post_init__(self):
        self.type = OcamlNodeType.LITERAL
    
    def accept(self, visitor):
        return visitor.visit_literal(self)


@dataclass
class OcamlIdentifier(OcamlExpression):
    """OCaml identifier."""
    name: str
    module_path: Optional[List[str]] = None
    
    def __post_init__(self):
        self.type = OcamlNodeType.IDENTIFIER
    
    def accept(self, visitor):
        return visitor.visit_identifier(self)


@dataclass
class OcamlConstructor(OcamlExpression):
    """OCaml constructor."""
    name: str
    module_path: Optional[List[str]] = None
    
    def __post_init__(self):
        self.type = OcamlNodeType.CONSTRUCTOR
    
    def accept(self, visitor):
        return visitor.visit_constructor(self)


@dataclass
class OcamlApplication(OcamlExpression):
    """OCaml function application."""
    function: OcamlExpression
    arguments: List[OcamlExpression]
    
    def __post_init__(self):
        self.type = OcamlNodeType.APPLICATION
    
    def accept(self, visitor):
        return visitor.visit_application(self)


@dataclass
class OcamlFunction(OcamlExpression):
    """OCaml function expression."""
    parameters: List[OcamlPattern]
    body: OcamlExpression
    
    def __post_init__(self):
        self.type = OcamlNodeType.FUNCTION
    
    def accept(self, visitor):
        return visitor.visit_function(self)


@dataclass
class OcamlLet(OcamlExpression):
    """OCaml let expression."""
    pattern: OcamlPattern
    value: OcamlExpression
    body: OcamlExpression
    recursive: bool = False
    
    def __post_init__(self):
        self.type = OcamlNodeType.LET_REC if self.recursive else OcamlNodeType.LET
    
    def accept(self, visitor):
        return visitor.visit_let(self)


@dataclass
class OcamlIf(OcamlExpression):
    """OCaml if expression."""
    condition: OcamlExpression
    then_expr: OcamlExpression
    else_expr: Optional[OcamlExpression] = None
    
    def __post_init__(self):
        self.type = OcamlNodeType.IF
    
    def accept(self, visitor):
        return visitor.visit_if(self)


@dataclass
class OcamlMatch(OcamlExpression):
    """OCaml match expression."""
    expression: OcamlExpression
    cases: List['OcamlMatchCase']
    
    def __post_init__(self):
        self.type = OcamlNodeType.MATCH
    
    def accept(self, visitor):
        return visitor.visit_match(self)


@dataclass
class OcamlTuple(OcamlExpression):
    """OCaml tuple expression."""
    elements: List[OcamlExpression]
    
    def __post_init__(self):
        self.type = OcamlNodeType.TUPLE
    
    def accept(self, visitor):
        return visitor.visit_tuple(self)


@dataclass
class OcamlList(OcamlExpression):
    """OCaml list expression."""
    elements: List[OcamlExpression]
    
    def __post_init__(self):
        self.type = OcamlNodeType.LIST
    
    def accept(self, visitor):
        return visitor.visit_list(self)


@dataclass
class OcamlRecord(OcamlExpression):
    """OCaml record expression."""
    fields: List['OcamlFieldBinding']
    base: Optional[OcamlExpression] = None
    
    def __post_init__(self):
        self.type = OcamlNodeType.RECORD
    
    def accept(self, visitor):
        return visitor.visit_record(self)


@dataclass
class OcamlFieldAccess(OcamlExpression):
    """OCaml field access."""
    expression: OcamlExpression
    field: str
    
    def __post_init__(self):
        self.type = OcamlNodeType.FIELD_ACCESS
    
    def accept(self, visitor):
        return visitor.visit_field_access(self)


# Patterns
@dataclass
class OcamlWildcardPattern(OcamlPattern):
    """OCaml wildcard pattern (_)."""
    
    def __post_init__(self):
        self.type = OcamlNodeType.WILDCARD_PATTERN
    
    def accept(self, visitor):
        return visitor.visit_wildcard_pattern(self)


@dataclass
class OcamlVariablePattern(OcamlPattern):
    """OCaml variable pattern."""
    name: str
    
    def __post_init__(self):
        self.type = OcamlNodeType.VARIABLE_PATTERN
    
    def accept(self, visitor):
        return visitor.visit_variable_pattern(self)


@dataclass
class OcamlConstructorPattern(OcamlPattern):
    """OCaml constructor pattern."""
    constructor: str
    patterns: List[OcamlPattern]
    module_path: Optional[List[str]] = None
    
    def __post_init__(self):
        self.type = OcamlNodeType.CONSTRUCTOR_PATTERN
    
    def accept(self, visitor):
        return visitor.visit_constructor_pattern(self)


@dataclass
class OcamlTuplePattern(OcamlPattern):
    """OCaml tuple pattern."""
    patterns: List[OcamlPattern]
    
    def __post_init__(self):
        self.type = OcamlNodeType.TUPLE_PATTERN
    
    def accept(self, visitor):
        return visitor.visit_tuple_pattern(self)


# Types
@dataclass
class OcamlTypeVariable(OcamlType):
    """OCaml type variable."""
    name: str
    
    def __post_init__(self):
        self.type = OcamlNodeType.TYPE_VARIABLE
    
    def accept(self, visitor):
        return visitor.visit_type_variable(self)


@dataclass
class OcamlTypeConstructor(OcamlType):
    """OCaml type constructor."""
    name: str
    arguments: List[OcamlType] = field(default_factory=list)
    module_path: Optional[List[str]] = None
    
    def __post_init__(self):
        self.type = OcamlNodeType.TYPE_CONSTRUCTOR
    
    def accept(self, visitor):
        return visitor.visit_type_constructor(self)


@dataclass
class OcamlFunctionType(OcamlType):
    """OCaml function type."""
    parameter_type: OcamlType
    return_type: OcamlType
    
    def __post_init__(self):
        self.type = OcamlNodeType.FUNCTION_TYPE
    
    def accept(self, visitor):
        return visitor.visit_function_type(self)


@dataclass
class OcamlTupleType(OcamlType):
    """OCaml tuple type."""
    types: List[OcamlType]
    
    def __post_init__(self):
        self.type = OcamlNodeType.TUPLE_TYPE
    
    def accept(self, visitor):
        return visitor.visit_tuple_type(self)


# Declarations
@dataclass
class OcamlValueDeclaration(OcamlDeclaration):
    """OCaml value declaration."""
    pattern: OcamlPattern
    expression: OcamlExpression
    recursive: bool = False
    
    def __post_init__(self):
        self.type = OcamlNodeType.VALUE_DECLARATION
    
    def accept(self, visitor):
        return visitor.visit_value_declaration(self)


@dataclass
class OcamlTypeDeclaration(OcamlDeclaration):
    """OCaml type declaration."""
    name: str
    parameters: List[str]
    definition: Optional[OcamlType] = None
    variants: Optional[List['OcamlVariant']] = None
    fields: Optional[List['OcamlRecordField']] = None
    
    def __post_init__(self):
        self.type = OcamlNodeType.TYPE_DECLARATION
    
    def accept(self, visitor):
        return visitor.visit_type_declaration(self)


@dataclass
class OcamlModuleDeclaration(OcamlDeclaration):
    """OCaml module declaration."""
    name: str
    body: 'OcamlModule'
    signature: Optional['OcamlSignature'] = None
    
    def __post_init__(self):
        self.type = OcamlNodeType.MODULE_DECLARATION
    
    def accept(self, visitor):
        return visitor.visit_module_declaration(self)


# Module system
@dataclass
class OcamlModule(OcamlNode):
    """OCaml module."""
    declarations: List[OcamlDeclaration]
    
    def __post_init__(self):
        self.type = OcamlNodeType.MODULE
    
    def accept(self, visitor):
        return visitor.visit_module(self)


@dataclass
class OcamlSignature(OcamlNode):
    """OCaml module signature."""
    declarations: List['OcamlSignatureItem']
    
    def __post_init__(self):
        self.type = OcamlNodeType.SIGNATURE
    
    def accept(self, visitor):
        return visitor.visit_signature(self)


# Helper classes
@dataclass
class OcamlMatchCase:
    """OCaml match case."""
    pattern: OcamlPattern
    guard: Optional[OcamlExpression]
    expression: OcamlExpression


@dataclass
class OcamlFieldBinding:
    """OCaml record field binding."""
    field: str
    expression: OcamlExpression


@dataclass
class OcamlVariant:
    """OCaml variant constructor."""
    name: str
    parameters: List[OcamlType]


@dataclass
class OcamlRecordField:
    """OCaml record field."""
    name: str
    type_expr: OcamlType
    mutable: bool = False


@dataclass
class OcamlSignatureItem:
    """OCaml signature item."""
    name: str
    item_type: str  # "value", "type", "module"
    type_expr: Optional[OcamlType] = None


# Visitor pattern
class OcamlNodeVisitor(ABC):
    """Abstract visitor for OCaml AST nodes."""
    
    @abstractmethod
    def visit_literal(self, node: OcamlLiteral): pass
    
    @abstractmethod
    def visit_identifier(self, node: OcamlIdentifier): pass
    
    @abstractmethod
    def visit_constructor(self, node: OcamlConstructor): pass
    
    @abstractmethod
    def visit_application(self, node: OcamlApplication): pass
    
    @abstractmethod
    def visit_function(self, node: OcamlFunction): pass
    
    @abstractmethod
    def visit_let(self, node: OcamlLet): pass
    
    @abstractmethod
    def visit_if(self, node: OcamlIf): pass
    
    @abstractmethod
    def visit_match(self, node: OcamlMatch): pass
    
    @abstractmethod
    def visit_tuple(self, node: OcamlTuple): pass
    
    @abstractmethod
    def visit_list(self, node: OcamlList): pass
    
    @abstractmethod
    def visit_record(self, node: OcamlRecord): pass
    
    @abstractmethod
    def visit_field_access(self, node: OcamlFieldAccess): pass
    
    @abstractmethod
    def visit_wildcard_pattern(self, node: OcamlWildcardPattern): pass
    
    @abstractmethod
    def visit_variable_pattern(self, node: OcamlVariablePattern): pass
    
    @abstractmethod
    def visit_constructor_pattern(self, node: OcamlConstructorPattern): pass
    
    @abstractmethod
    def visit_tuple_pattern(self, node: OcamlTuplePattern): pass
    
    @abstractmethod
    def visit_type_variable(self, node: OcamlTypeVariable): pass
    
    @abstractmethod
    def visit_type_constructor(self, node: OcamlTypeConstructor): pass
    
    @abstractmethod
    def visit_function_type(self, node: OcamlFunctionType): pass
    
    @abstractmethod
    def visit_tuple_type(self, node: OcamlTupleType): pass
    
    @abstractmethod
    def visit_value_declaration(self, node: OcamlValueDeclaration): pass
    
    @abstractmethod
    def visit_type_declaration(self, node: OcamlTypeDeclaration): pass
    
    @abstractmethod
    def visit_module_declaration(self, node: OcamlModuleDeclaration): pass
    
    @abstractmethod
    def visit_module(self, node: OcamlModule): pass
    
    @abstractmethod
    def visit_signature(self, node: OcamlSignature): pass


# Utility functions
def ocaml_lit_int(value: int) -> OcamlLiteral:
    """Create integer literal."""
    return OcamlLiteral(value=value, literal_type="int")


def ocaml_lit_string(value: str) -> OcamlLiteral:
    """Create string literal."""
    return OcamlLiteral(value=value, literal_type="string")


def ocaml_lit_bool(value: bool) -> OcamlLiteral:
    """Create boolean literal."""
    return OcamlLiteral(value=value, literal_type="bool")


def ocaml_var(name: str) -> OcamlIdentifier:
    """Create variable."""
    return OcamlIdentifier(name=name)


def ocaml_con(name: str) -> OcamlConstructor:
    """Create constructor."""
    return OcamlConstructor(name=name)


def ocaml_app(func: OcamlExpression, *args: OcamlExpression) -> OcamlApplication:
    """Create application."""
    return OcamlApplication(function=func, arguments=list(args))


# Export all
__all__ = [
    # Enums
    "OcamlNodeType", "OcamlOperator",
    
    # Base classes
    "OcamlNode", "OcamlExpression", "OcamlPattern", "OcamlType", "OcamlDeclaration",
    
    # Expressions
    "OcamlLiteral", "OcamlIdentifier", "OcamlConstructor", "OcamlApplication",
    "OcamlFunction", "OcamlLet", "OcamlIf", "OcamlMatch", "OcamlTuple", "OcamlList",
    "OcamlRecord", "OcamlFieldAccess",
    
    # Patterns
    "OcamlWildcardPattern", "OcamlVariablePattern", "OcamlConstructorPattern",
    "OcamlTuplePattern",
    
    # Types
    "OcamlTypeVariable", "OcamlTypeConstructor", "OcamlFunctionType", "OcamlTupleType",
    
    # Declarations
    "OcamlValueDeclaration", "OcamlTypeDeclaration", "OcamlModuleDeclaration",
    
    # Module system
    "OcamlModule", "OcamlSignature",
    
    # Helper classes
    "OcamlMatchCase", "OcamlFieldBinding", "OcamlVariant", "OcamlRecordField",
    "OcamlSignatureItem",
    
    # Visitor
    "OcamlNodeVisitor",
    
    # Utilities
    "ocaml_lit_int", "ocaml_lit_string", "ocaml_lit_bool", "ocaml_var", "ocaml_con", "ocaml_app",
] 