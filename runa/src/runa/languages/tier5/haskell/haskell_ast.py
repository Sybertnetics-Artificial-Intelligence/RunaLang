#!/usr/bin/env python3
"""
Haskell AST Node Definitions

Comprehensive Abstract Syntax Tree nodes for Haskell covering
all major language features including pattern matching, type classes,
algebraic data types, modules, and advanced functional constructs.
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod


class HsNodeType(Enum):
    """Haskell AST node types."""
    # Literals
    LITERAL = auto()
    INTEGER = auto()
    FLOAT = auto()
    CHAR = auto()
    STRING = auto()
    BOOLEAN = auto()
    
    # Identifiers and variables
    VARIABLE = auto()
    CONSTRUCTOR = auto()
    OPERATOR = auto()
    QUALIFIED_NAME = auto()
    
    # Expressions
    APPLICATION = auto()
    LAMBDA = auto()
    LET = auto()
    WHERE = auto()
    IF = auto()
    CASE = auto()
    DO = auto()
    LIST = auto()
    TUPLE = auto()
    RECORD = auto()
    RECORD_UPDATE = auto()
    ARITHMETIC_SEQUENCE = auto()
    LIST_COMPREHENSION = auto()
    SECTION = auto()  # Operator sections like (+1), (`div` 2)
    
    # Patterns
    WILDCARD_PATTERN = auto()
    VARIABLE_PATTERN = auto()
    CONSTRUCTOR_PATTERN = auto()
    LITERAL_PATTERN = auto()
    LIST_PATTERN = auto()
    TUPLE_PATTERN = auto()
    RECORD_PATTERN = auto()
    AS_PATTERN = auto()
    IRREFUTABLE_PATTERN = auto()
    
    # Types
    TYPE_VARIABLE = auto()
    TYPE_CONSTRUCTOR = auto()
    TYPE_APPLICATION = auto()
    FUNCTION_TYPE = auto()
    TUPLE_TYPE = auto()
    LIST_TYPE = auto()
    FORALL_TYPE = auto()
    CONSTRAINT_TYPE = auto()
    KIND = auto()
    
    # Declarations
    TYPE_DECLARATION = auto()
    DATA_DECLARATION = auto()
    NEWTYPE_DECLARATION = auto()
    CLASS_DECLARATION = auto()
    INSTANCE_DECLARATION = auto()
    FUNCTION_DECLARATION = auto()
    VALUE_DECLARATION = auto()
    TYPE_SIGNATURE = auto()
    FOREIGN_DECLARATION = auto()
    
    # Module system
    MODULE = auto()
    IMPORT = auto()
    EXPORT = auto()
    
    # Guards and alternatives
    GUARD = auto()
    ALTERNATIVE = auto()
    GUARDED_RHS = auto()
    
    # Statements (for do notation)
    DO_STMT = auto()
    GENERATOR = auto()
    QUALIFIER = auto()
    
    # Fixity declarations
    FIXITY = auto()
    
    # Pragmas
    PRAGMA = auto()


class HsOperator(Enum):
    """Haskell operators."""
    # Arithmetic
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    MOD = "mod"
    DIV = "div"
    POWER = "^"
    POWER_INT = "^^"
    POWER_FLOAT = "**"
    
    # Comparison
    EQ = "=="
    NEQ = "/="
    LT = "<"
    LE = "<="
    GT = ">"
    GE = ">="
    
    # Logical
    AND = "&&"
    OR = "||"
    NOT = "not"
    
    # List operations
    CONS = ":"
    APPEND = "++"
    
    # Function composition
    COMPOSE = "."
    APPLY = "$"
    
    # Monadic operations
    BIND = ">>="
    THEN = ">>"
    
    # Pattern matching
    MATCH = "~"
    
    # Type operations
    HAS_TYPE = "::"


class HsAssociativity(Enum):
    """Haskell operator associativity."""
    LEFT = "infixl"
    RIGHT = "infixr"
    NONE = "infix"


@dataclass
class HsNode(ABC):
    """Base class for all Haskell AST nodes."""
    type: HsNodeType = None
    location: Optional[tuple] = None  # (line, column)
    
    @abstractmethod
    def accept(self, visitor):
        """Accept a visitor for the visitor pattern."""
        pass


@dataclass
class HsExpression(HsNode):
    """Base class for Haskell expressions."""
    pass


@dataclass
class HsPattern(HsNode):
    """Base class for Haskell patterns."""
    pass


@dataclass
class HsType(HsNode):
    """Base class for Haskell types."""
    pass


@dataclass
class HsDeclaration(HsNode):
    """Base class for Haskell declarations."""
    pass


@dataclass
class HsStatement(HsNode):
    """Base class for Haskell statements (do notation)."""
    pass


# Literals
@dataclass
class HsLiteral(HsExpression):
    """Haskell literal node."""
    value: Any
    literal_type: str  # "integer", "float", "char", "string", "boolean"
    
    def __post_init__(self):
        self.type = HsNodeType.LITERAL
    
    def accept(self, visitor):
        return visitor.visit_literal(self)


@dataclass
class HsVariable(HsExpression):
    """Haskell variable node."""
    name: str
    qualified: Optional[str] = None  # Module qualifier
    
    def __post_init__(self):
        self.type = HsNodeType.VARIABLE
    
    def accept(self, visitor):
        return visitor.visit_variable(self)


@dataclass
class HsConstructor(HsExpression):
    """Haskell constructor node."""
    name: str
    qualified: Optional[str] = None
    
    def __post_init__(self):
        self.type = HsNodeType.CONSTRUCTOR
    
    def accept(self, visitor):
        return visitor.visit_constructor(self)


@dataclass
class HsApplication(HsExpression):
    """Haskell function application node."""
    function: HsExpression
    arguments: List[HsExpression]
    
    def __post_init__(self):
        self.type = HsNodeType.APPLICATION
    
    def accept(self, visitor):
        return visitor.visit_application(self)


@dataclass
class HsLambda(HsExpression):
    """Haskell lambda expression node."""
    parameters: List[HsPattern]
    body: HsExpression
    
    def __post_init__(self):
        self.type = HsNodeType.LAMBDA
    
    def accept(self, visitor):
        return visitor.visit_lambda(self)


@dataclass
class HsLet(HsExpression):
    """Haskell let expression node."""
    bindings: List['HsBinding']
    expression: HsExpression
    
    def __post_init__(self):
        self.type = HsNodeType.LET
    
    def accept(self, visitor):
        return visitor.visit_let(self)


@dataclass
class HsWhere(HsExpression):
    """Haskell where expression node."""
    expression: HsExpression
    bindings: List['HsBinding']
    
    def __post_init__(self):
        self.type = HsNodeType.WHERE
    
    def accept(self, visitor):
        return visitor.visit_where(self)


@dataclass
class HsIf(HsExpression):
    """Haskell if expression node."""
    condition: HsExpression
    then_expr: HsExpression
    else_expr: HsExpression
    
    def __post_init__(self):
        self.type = HsNodeType.IF
    
    def accept(self, visitor):
        return visitor.visit_if(self)


@dataclass
class HsCase(HsExpression):
    """Haskell case expression node."""
    expression: HsExpression
    alternatives: List['HsAlternative']
    
    def __post_init__(self):
        self.type = HsNodeType.CASE
    
    def accept(self, visitor):
        return visitor.visit_case(self)


@dataclass
class HsDo(HsExpression):
    """Haskell do expression node."""
    statements: List[HsStatement]
    
    def __post_init__(self):
        self.type = HsNodeType.DO
    
    def accept(self, visitor):
        return visitor.visit_do(self)


@dataclass
class HsList(HsExpression):
    """Haskell list expression node."""
    elements: List[HsExpression]
    
    def __post_init__(self):
        self.type = HsNodeType.LIST
    
    def accept(self, visitor):
        return visitor.visit_list(self)


@dataclass
class HsTuple(HsExpression):
    """Haskell tuple expression node."""
    elements: List[HsExpression]
    
    def __post_init__(self):
        self.type = HsNodeType.TUPLE
    
    def accept(self, visitor):
        return visitor.visit_tuple(self)


@dataclass
class HsRecord(HsExpression):
    """Haskell record expression node."""
    constructor: HsConstructor
    fields: List['HsFieldBinding']
    
    def __post_init__(self):
        self.type = HsNodeType.RECORD
    
    def accept(self, visitor):
        return visitor.visit_record(self)


@dataclass
class HsListComprehension(HsExpression):
    """Haskell list comprehension node."""
    expression: HsExpression
    qualifiers: List['HsQualifier']
    
    def __post_init__(self):
        self.type = HsNodeType.LIST_COMPREHENSION
    
    def accept(self, visitor):
        return visitor.visit_list_comprehension(self)


# Patterns
@dataclass
class HsWildcardPattern(HsPattern):
    """Haskell wildcard pattern (_)."""
    
    def __post_init__(self):
        self.type = HsNodeType.WILDCARD_PATTERN
    
    def accept(self, visitor):
        return visitor.visit_wildcard_pattern(self)


@dataclass
class HsVariablePattern(HsPattern):
    """Haskell variable pattern."""
    name: str
    
    def __post_init__(self):
        self.type = HsNodeType.VARIABLE_PATTERN
    
    def accept(self, visitor):
        return visitor.visit_variable_pattern(self)


@dataclass
class HsConstructorPattern(HsPattern):
    """Haskell constructor pattern."""
    constructor: str
    patterns: List[HsPattern]
    
    def __post_init__(self):
        self.type = HsNodeType.CONSTRUCTOR_PATTERN
    
    def accept(self, visitor):
        return visitor.visit_constructor_pattern(self)


@dataclass
class HsLiteralPattern(HsPattern):
    """Haskell literal pattern."""
    literal: HsLiteral
    
    def __post_init__(self):
        self.type = HsNodeType.LITERAL_PATTERN
    
    def accept(self, visitor):
        return visitor.visit_literal_pattern(self)


@dataclass
class HsListPattern(HsPattern):
    """Haskell list pattern."""
    patterns: List[HsPattern]
    
    def __post_init__(self):
        self.type = HsNodeType.LIST_PATTERN
    
    def accept(self, visitor):
        return visitor.visit_list_pattern(self)


@dataclass
class HsTuplePattern(HsPattern):
    """Haskell tuple pattern."""
    patterns: List[HsPattern]
    
    def __post_init__(self):
        self.type = HsNodeType.TUPLE_PATTERN
    
    def accept(self, visitor):
        return visitor.visit_tuple_pattern(self)


@dataclass
class HsAsPattern(HsPattern):
    """Haskell as pattern (var@pattern)."""
    variable: str
    pattern: HsPattern
    
    def __post_init__(self):
        self.type = HsNodeType.AS_PATTERN
    
    def accept(self, visitor):
        return visitor.visit_as_pattern(self)


# Types
@dataclass
class HsTypeVariable(HsType):
    """Haskell type variable."""
    name: str
    kind: Optional['HsKind'] = None
    
    def __post_init__(self):
        self.type = HsNodeType.TYPE_VARIABLE
    
    def accept(self, visitor):
        return visitor.visit_type_variable(self)


@dataclass
class HsTypeConstructor(HsType):
    """Haskell type constructor."""
    name: str
    qualified: Optional[str] = None
    
    def __post_init__(self):
        self.type = HsNodeType.TYPE_CONSTRUCTOR
    
    def accept(self, visitor):
        return visitor.visit_type_constructor(self)


@dataclass
class HsTypeApplication(HsType):
    """Haskell type application."""
    constructor: HsType
    arguments: List[HsType]
    
    def __post_init__(self):
        self.type = HsNodeType.TYPE_APPLICATION
    
    def accept(self, visitor):
        return visitor.visit_type_application(self)


@dataclass
class HsFunctionType(HsType):
    """Haskell function type (a -> b)."""
    from_type: HsType
    to_type: HsType
    
    def __post_init__(self):
        self.type = HsNodeType.FUNCTION_TYPE
    
    def accept(self, visitor):
        return visitor.visit_function_type(self)


@dataclass
class HsTupleType(HsType):
    """Haskell tuple type."""
    types: List[HsType]
    
    def __post_init__(self):
        self.type = HsNodeType.TUPLE_TYPE
    
    def accept(self, visitor):
        return visitor.visit_tuple_type(self)


@dataclass
class HsListType(HsType):
    """Haskell list type [a]."""
    element_type: HsType
    
    def __post_init__(self):
        self.type = HsNodeType.LIST_TYPE
    
    def accept(self, visitor):
        return visitor.visit_list_type(self)


@dataclass
class HsForallType(HsType):
    """Haskell forall type."""
    variables: List[str]
    constraints: List['HsConstraint']
    body_type: HsType
    
    def __post_init__(self):
        self.type = HsNodeType.FORALL_TYPE
    
    def accept(self, visitor):
        return visitor.visit_forall_type(self)


# Declarations
@dataclass
class HsTypeDeclaration(HsDeclaration):
    """Haskell type declaration (type synonym)."""
    name: str
    parameters: List[str]
    body: HsType
    
    def __post_init__(self):
        self.type = HsNodeType.TYPE_DECLARATION
    
    def accept(self, visitor):
        return visitor.visit_type_declaration(self)


@dataclass
class HsDataDeclaration(HsDeclaration):
    """Haskell data declaration."""
    name: str
    parameters: List[str]
    constructors: List['HsDataConstructor']
    deriving: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = HsNodeType.DATA_DECLARATION
    
    def accept(self, visitor):
        return visitor.visit_data_declaration(self)


@dataclass
class HsClassDeclaration(HsDeclaration):
    """Haskell type class declaration."""
    name: str
    parameter: str
    constraints: List['HsConstraint'] = field(default_factory=list)
    methods: List['HsMethodSignature'] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = HsNodeType.CLASS_DECLARATION
    
    def accept(self, visitor):
        return visitor.visit_class_declaration(self)


@dataclass
class HsInstanceDeclaration(HsDeclaration):
    """Haskell instance declaration."""
    constraints: List['HsConstraint']
    class_name: str
    instance_type: HsType
    methods: List['HsBinding']
    
    def __post_init__(self):
        self.type = HsNodeType.INSTANCE_DECLARATION
    
    def accept(self, visitor):
        return visitor.visit_instance_declaration(self)


@dataclass
class HsFunctionDeclaration(HsDeclaration):
    """Haskell function declaration."""
    name: str
    clauses: List['HsClause']
    
    def __post_init__(self):
        self.type = HsNodeType.FUNCTION_DECLARATION
    
    def accept(self, visitor):
        return visitor.visit_function_declaration(self)


@dataclass
class HsTypeSignature(HsDeclaration):
    """Haskell type signature."""
    names: List[str]
    type_expr: HsType
    
    def __post_init__(self):
        self.type = HsNodeType.TYPE_SIGNATURE
    
    def accept(self, visitor):
        return visitor.visit_type_signature(self)


# Module system
@dataclass
class HsModule(HsNode):
    """Haskell module node."""
    name: Optional[str]
    exports: Optional[List['HsExport']]
    imports: List['HsImport']
    declarations: List[HsDeclaration]
    
    def __post_init__(self):
        self.type = HsNodeType.MODULE
    
    def accept(self, visitor):
        return visitor.visit_module(self)


@dataclass
class HsImport(HsNode):
    """Haskell import declaration."""
    module_name: str
    qualified: bool = False
    alias: Optional[str] = None
    hiding: bool = False
    import_list: Optional[List[str]] = None
    
    def __post_init__(self):
        self.type = HsNodeType.IMPORT
    
    def accept(self, visitor):
        return visitor.visit_import(self)


# Helper classes
@dataclass
class HsBinding:
    """Haskell binding (used in let/where)."""
    pattern: HsPattern
    expression: HsExpression
    where_bindings: List['HsBinding'] = field(default_factory=list)


@dataclass
class HsAlternative:
    """Haskell case alternative."""
    pattern: HsPattern
    guards: List['HsGuard']
    expression: HsExpression


@dataclass
class HsGuard:
    """Haskell guard."""
    condition: HsExpression
    expression: HsExpression


@dataclass
class HsClause:
    """Haskell function clause."""
    patterns: List[HsPattern]
    guards: List[HsGuard]
    expression: HsExpression
    where_bindings: List[HsBinding] = field(default_factory=list)


@dataclass
class HsDataConstructor:
    """Haskell data constructor."""
    name: str
    fields: List[HsType]
    field_names: Optional[List[str]] = None  # For record syntax


@dataclass
class HsConstraint:
    """Haskell type constraint."""
    class_name: str
    type_expr: HsType


@dataclass
class HsMethodSignature:
    """Haskell type class method signature."""
    name: str
    type_expr: HsType


@dataclass
class HsFieldBinding:
    """Haskell record field binding."""
    field: str
    expression: HsExpression


@dataclass
class HsQualifier:
    """Haskell list comprehension qualifier."""
    is_generator: bool
    pattern: Optional[HsPattern]  # For generators
    expression: HsExpression


@dataclass
class HsKind:
    """Haskell kind."""
    name: str


@dataclass
class HsExport:
    """Haskell export specification."""
    name: str
    export_type: str  # "value", "type", "module"


# Do notation statements
@dataclass
class HsDoStatement(HsStatement):
    """Base do statement."""
    pass


@dataclass
class HsGenerator(HsDoStatement):
    """Haskell generator statement (pattern <- expression)."""
    pattern: HsPattern
    expression: HsExpression
    
    def __post_init__(self):
        self.type = HsNodeType.GENERATOR
    
    def accept(self, visitor):
        return visitor.visit_generator(self)


@dataclass
class HsDoQualifier(HsDoStatement):
    """Haskell do qualifier (boolean expression)."""
    expression: HsExpression
    
    def __post_init__(self):
        self.type = HsNodeType.QUALIFIER
    
    def accept(self, visitor):
        return visitor.visit_do_qualifier(self)


@dataclass
class HsDoExpression(HsDoStatement):
    """Haskell do expression statement."""
    expression: HsExpression
    
    def __post_init__(self):
        self.type = HsNodeType.DO_STMT
    
    def accept(self, visitor):
        return visitor.visit_do_expression(self)


# Visitor pattern
class HsNodeVisitor(ABC):
    """Abstract visitor for Haskell AST nodes."""
    
    @abstractmethod
    def visit_literal(self, node: HsLiteral): pass
    
    @abstractmethod
    def visit_variable(self, node: HsVariable): pass
    
    @abstractmethod
    def visit_constructor(self, node: HsConstructor): pass
    
    @abstractmethod
    def visit_application(self, node: HsApplication): pass
    
    @abstractmethod
    def visit_lambda(self, node: HsLambda): pass
    
    @abstractmethod
    def visit_let(self, node: HsLet): pass
    
    @abstractmethod
    def visit_where(self, node: HsWhere): pass
    
    @abstractmethod
    def visit_if(self, node: HsIf): pass
    
    @abstractmethod
    def visit_case(self, node: HsCase): pass
    
    @abstractmethod
    def visit_do(self, node: HsDo): pass
    
    @abstractmethod
    def visit_list(self, node: HsList): pass
    
    @abstractmethod
    def visit_tuple(self, node: HsTuple): pass
    
    @abstractmethod
    def visit_record(self, node: HsRecord): pass
    
    @abstractmethod
    def visit_list_comprehension(self, node: HsListComprehension): pass
    
    @abstractmethod
    def visit_wildcard_pattern(self, node: HsWildcardPattern): pass
    
    @abstractmethod
    def visit_variable_pattern(self, node: HsVariablePattern): pass
    
    @abstractmethod
    def visit_constructor_pattern(self, node: HsConstructorPattern): pass
    
    @abstractmethod
    def visit_literal_pattern(self, node: HsLiteralPattern): pass
    
    @abstractmethod
    def visit_list_pattern(self, node: HsListPattern): pass
    
    @abstractmethod
    def visit_tuple_pattern(self, node: HsTuplePattern): pass
    
    @abstractmethod
    def visit_as_pattern(self, node: HsAsPattern): pass
    
    @abstractmethod
    def visit_type_variable(self, node: HsTypeVariable): pass
    
    @abstractmethod
    def visit_type_constructor(self, node: HsTypeConstructor): pass
    
    @abstractmethod
    def visit_type_application(self, node: HsTypeApplication): pass
    
    @abstractmethod
    def visit_function_type(self, node: HsFunctionType): pass
    
    @abstractmethod
    def visit_tuple_type(self, node: HsTupleType): pass
    
    @abstractmethod
    def visit_list_type(self, node: HsListType): pass
    
    @abstractmethod
    def visit_forall_type(self, node: HsForallType): pass
    
    @abstractmethod
    def visit_type_declaration(self, node: HsTypeDeclaration): pass
    
    @abstractmethod
    def visit_data_declaration(self, node: HsDataDeclaration): pass
    
    @abstractmethod
    def visit_class_declaration(self, node: HsClassDeclaration): pass
    
    @abstractmethod
    def visit_instance_declaration(self, node: HsInstanceDeclaration): pass
    
    @abstractmethod
    def visit_function_declaration(self, node: HsFunctionDeclaration): pass
    
    @abstractmethod
    def visit_type_signature(self, node: HsTypeSignature): pass
    
    @abstractmethod
    def visit_module(self, node: HsModule): pass
    
    @abstractmethod
    def visit_import(self, node: HsImport): pass
    
    @abstractmethod
    def visit_generator(self, node: HsGenerator): pass
    
    @abstractmethod
    def visit_do_qualifier(self, node: HsDoQualifier): pass
    
    @abstractmethod
    def visit_do_expression(self, node: HsDoExpression): pass


# Utility functions for AST construction
def hs_var(name: str, qualified: str = None) -> HsVariable:
    """Create a Haskell variable node."""
    return HsVariable(name=name, qualified=qualified)


def hs_con(name: str, qualified: str = None) -> HsConstructor:
    """Create a Haskell constructor node."""
    return HsConstructor(name=name, qualified=qualified)


def hs_app(func: HsExpression, *args: HsExpression) -> HsExpression:
    """Create a Haskell application node."""
    if not args:
        return func
    return HsApplication(function=func, arguments=list(args))


def hs_lambda(params: List[HsPattern], body: HsExpression) -> HsLambda:
    """Create a Haskell lambda node."""
    return HsLambda(parameters=params, body=body)


def hs_lit_int(value: int) -> HsLiteral:
    """Create a Haskell integer literal."""
    return HsLiteral(value=value, literal_type="integer")


def hs_lit_str(value: str) -> HsLiteral:
    """Create a Haskell string literal."""
    return HsLiteral(value=value, literal_type="string")


def hs_lit_bool(value: bool) -> HsLiteral:
    """Create a Haskell boolean literal."""
    return HsLiteral(value=value, literal_type="boolean")


# Export all node types and utilities
__all__ = [
    # Enums
    "HsNodeType", "HsOperator", "HsAssociativity",
    
    # Base classes
    "HsNode", "HsExpression", "HsPattern", "HsType", "HsDeclaration", "HsStatement",
    
    # Expressions
    "HsLiteral", "HsVariable", "HsConstructor", "HsApplication", "HsLambda",
    "HsLet", "HsWhere", "HsIf", "HsCase", "HsDo", "HsList", "HsTuple", "HsRecord",
    "HsListComprehension",
    
    # Patterns
    "HsWildcardPattern", "HsVariablePattern", "HsConstructorPattern", "HsLiteralPattern",
    "HsListPattern", "HsTuplePattern", "HsAsPattern",
    
    # Types
    "HsTypeVariable", "HsTypeConstructor", "HsTypeApplication", "HsFunctionType",
    "HsTupleType", "HsListType", "HsForallType",
    
    # Declarations
    "HsTypeDeclaration", "HsDataDeclaration", "HsClassDeclaration", "HsInstanceDeclaration",
    "HsFunctionDeclaration", "HsTypeSignature",
    
    # Module system
    "HsModule", "HsImport", "HsExport",
    
    # Do notation
    "HsDoStatement", "HsGenerator", "HsDoQualifier", "HsDoExpression",
    
    # Helper classes
    "HsBinding", "HsAlternative", "HsGuard", "HsClause", "HsDataConstructor",
    "HsConstraint", "HsMethodSignature", "HsFieldBinding", "HsQualifier", "HsKind",
    
    # Visitor
    "HsNodeVisitor",
    
    # Utilities
    "hs_var", "hs_con", "hs_app", "hs_lambda", "hs_lit_int", "hs_lit_str", "hs_lit_bool",
] 