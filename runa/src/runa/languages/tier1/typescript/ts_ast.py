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


# ------------------ Base Node Classes (must come first) -------------------

@dataclass
class TSNode(ABC):
    """Base class for all TypeScript AST nodes."""
    type: 'TSNodeType' = field(default=None, init=False)
    loc: Optional[Dict[str, Any]] = field(default=None, init=False)
    range: Optional[List[int]] = field(default=None, init=False)
    
    @abstractmethod
    def accept(self, visitor):
        """Accept a visitor for the visitor pattern."""
        pass


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
    
    # Additional missing node types
    PROPERTY = auto()
    AWAIT_EXPRESSION = auto()
    YIELD_EXPRESSION = auto()
    SEQUENCE_EXPRESSION = auto()
    CATCH_CLAUSE = auto()
    SWITCH_CASE = auto()
    TEMPLATE_ELEMENT = auto()
    DEBUGGER_STATEMENT = auto()
    
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

# ------------------ Added concrete expression/statement nodes -------------

class TSExpression(TSNode):
    """Base class for TS expression nodes (matches JSExpression style)."""
    pass

class TSStatement(TSNode):
    """Base class for TS statement nodes."""
    pass

class TSDeclaration(TSNode):
    """Base class for TS declaration nodes."""
    pass

@dataclass
class TSBinaryExpression(TSExpression):
    """TypeScript binary expression node (e.g., a + b, x === y)."""
    left: TSNode = None
    operator: TSOperator = None
    right: TSNode = None
    def __post_init__(self):
        self.type = TSNodeType.BINARY_EXPRESSION
    def accept(self, visitor):
        return visitor.visit_binary_expression(self) if hasattr(visitor, "visit_binary_expression") else None

@dataclass
class TSLogicalExpression(TSExpression):
    """Logical expression (&&, ||, ??)."""
    left: TSNode = None
    operator: TSOperator = None
    right: TSNode = None
    def __post_init__(self):
        self.type = TSNodeType.LOGICAL_EXPRESSION
    def accept(self, visitor):
        return visitor.visit_logical_expression(self) if hasattr(visitor, "visit_logical_expression") else None

@dataclass
class TSUnaryExpression(TSExpression):
    """Unary expression (!a, -b, +c)."""
    operator: TSOperator = None
    argument: TSNode = None
    prefix: bool = True
    def __post_init__(self):
        self.type = TSNodeType.UNARY_EXPRESSION
    def accept(self, visitor):
        return visitor.visit_unary_expression(self) if hasattr(visitor, "visit_unary_expression") else None

@dataclass
class TSAssignmentExpression(TSExpression):
    """Assignment expression (a = b, x += y)."""
    left: TSNode = None
    operator: TSOperator = None
    right: TSNode = None
    def __post_init__(self):
        self.type = TSNodeType.ASSIGNMENT_EXPRESSION
    def accept(self, visitor):
        return visitor.visit_assignment_expression(self) if hasattr(visitor, "visit_assignment_expression") else None

@dataclass
class TSUpdateExpression(TSExpression):
    """Update expression (++a, b--)."""
    operator: TSOperator  # INCREMENT or DECREMENT
    argument: TSNode = None
    prefix: bool = True
    def __post_init__(self):
        self.type = TSNodeType.UPDATE_EXPRESSION
    def accept(self, visitor):
        return visitor.visit_update_expression(self) if hasattr(visitor, "visit_update_expression") else None

@dataclass 
class TSConditionalExpression(TSExpression):
    """Conditional expression (ternary: test ? consequent : alternate)."""
    test: TSNode = None
    consequent: TSNode = None
    alternate: TSNode = None
    def __post_init__(self):
        self.type = TSNodeType.CONDITIONAL_EXPRESSION
    def accept(self, visitor):
        return visitor.visit_conditional_expression(self) if hasattr(visitor, "visit_conditional_expression") else None

@dataclass
class TSCallExpression(TSExpression):
    """Call expression (func(args))."""
    callee: TSNode = None
    arguments: List[TSNode] = None
    type_arguments: Optional[List['TSType']] = None
    def __post_init__(self):
        self.type = TSNodeType.CALL_EXPRESSION
        if self.type_arguments is None:
            self.type_arguments = []
    def accept(self, visitor):
        return visitor.visit_call_expression(self) if hasattr(visitor, "visit_call_expression") else None

@dataclass
class TSMemberExpression(TSExpression):
    """Member expression (obj.prop, obj[key])."""
    object: TSNode = None
    property: TSNode = None
    computed: bool = False  # True for obj[key], False for obj.prop
    optional: bool = False  # True for obj?.prop
    def __post_init__(self):
        self.type = TSNodeType.MEMBER_EXPRESSION
    def accept(self, visitor):
        return visitor.visit_member_expression(self) if hasattr(visitor, "visit_member_expression") else None

@dataclass
class TSNewExpression(TSExpression):
    """New expression (new Constructor(args))."""
    callee: TSNode = None
    arguments: List[TSNode] = None
    type_arguments: Optional[List['TSType']] = None
    def __post_init__(self):
        self.type = TSNodeType.NEW_EXPRESSION
        if self.type_arguments is None:
            self.type_arguments = []
    def accept(self, visitor):
        return visitor.visit_new_expression(self) if hasattr(visitor, "visit_new_expression") else None

@dataclass
class TSThisExpression(TSExpression):
    """This expression."""
    def __post_init__(self):
        self.type = TSNodeType.THIS_EXPRESSION
    def accept(self, visitor):
        return visitor.visit_this_expression(self) if hasattr(visitor, "visit_this_expression") else None

@dataclass
class TSSuper(TSExpression):
    """Super expression."""
    def __post_init__(self):
        self.type = TSNodeType.SUPER
    def accept(self, visitor):
        return visitor.visit_super(self) if hasattr(visitor, "visit_super") else None

@dataclass
class TSArrayExpression(TSExpression):
    """Array expression ([1, 2, 3])."""
    elements: List[Optional[TSNode]]  # Optional allows for sparse arrays
    def __post_init__(self):
        self.type = TSNodeType.ARRAY_EXPRESSION
    def accept(self, visitor):
        return visitor.visit_array_expression(self) if hasattr(visitor, "visit_array_expression") else None

@dataclass
class TSObjectExpression(TSExpression):
    """Object expression ({key: value})."""
    properties: List['TSProperty'] = None
    def __post_init__(self):
        self.type = TSNodeType.OBJECT_EXPRESSION
    def accept(self, visitor):
        return visitor.visit_object_expression(self) if hasattr(visitor, "visit_object_expression") else None

@dataclass
class TSProperty(TSNode):
    """Object property."""
    key: TSNode = None
    value: TSNode = None
    kind: str = "init"  # "init", "get", "set"
    method: bool = False
    shorthand: bool = False
    computed: bool = False
    def __post_init__(self):
        self.type = TSNodeType.PROPERTY
    def accept(self, visitor):
        return visitor.visit_property(self) if hasattr(visitor, "visit_property") else None

@dataclass
class TSFunctionExpression(TSExpression):
    """Function expression."""
    id: Optional['TSIdentifier'] = None
    params: List['TSParameter'] = None
    body: 'TSBlockStatement' = None
    generator: bool = False
    async_: bool = False
    return_type: Optional['TSTypeAnnotation'] = None
    type_parameters: Optional[List['TSTypeParameter']] = None
    def __post_init__(self):
        self.type = TSNodeType.FUNCTION_EXPRESSION
        if self.type_parameters is None:
            self.type_parameters = []
    def accept(self, visitor):
        return visitor.visit_function_expression(self) if hasattr(visitor, "visit_function_expression") else None

@dataclass
class TSArrowFunctionExpression(TSExpression):
    """Arrow function expression."""
    params: List['TSParameter'] = None
    body: Union['TSBlockStatement', TSNode] = None  # Can be expression or block
    async_: bool = False
    return_type: Optional['TSTypeAnnotation'] = None
    type_parameters: Optional[List['TSTypeParameter']] = None
    def __post_init__(self):
        self.type = TSNodeType.ARROW_FUNCTION_EXPRESSION
        if self.type_parameters is None:
            self.type_parameters = []
    def accept(self, visitor):
        return visitor.visit_arrow_function_expression(self) if hasattr(visitor, "visit_arrow_function_expression") else None

@dataclass
class TSSequenceExpression(TSExpression):
    """Sequence expression (a, b, c)."""
    expressions: List[TSNode] = None
    def __post_init__(self):
        self.type = TSNodeType.SEQUENCE_EXPRESSION
    def accept(self, visitor):
        return visitor.visit_sequence_expression(self) if hasattr(visitor, "visit_sequence_expression") else None

@dataclass
class TSAwaitExpression(TSExpression):
    """Await expression (await promise)."""
    argument: TSNode = None
    def __post_init__(self):
        self.type = TSNodeType.AWAIT_EXPRESSION
    def accept(self, visitor):
        return visitor.visit_await_expression(self) if hasattr(visitor, "visit_await_expression") else None

@dataclass
class TSYieldExpression(TSExpression):
    """Yield expression (yield value)."""
    argument: Optional[TSNode] = None
    delegate: bool = False  # yield* vs yield
    def __post_init__(self):
        self.type = TSNodeType.YIELD_EXPRESSION
    def accept(self, visitor):
        return visitor.visit_yield_expression(self) if hasattr(visitor, "visit_yield_expression") else None

@dataclass
class TSTemplateLiteral(TSExpression):
    """Template literal (`hello ${name}`)."""
    quasis: List['TSTemplateElement'] = None
    expressions: List[TSNode] = None
    def __post_init__(self):
        self.type = TSNodeType.TEMPLATE_LITERAL
    def accept(self, visitor):
        return visitor.visit_template_literal(self) if hasattr(visitor, "visit_template_literal") else None

@dataclass
class TSTemplateElement(TSNode):
    """Template literal element."""
    value: Dict[str, str]  # {"raw": "...", "cooked": "..."}
    tail: bool = False
    def __post_init__(self):
        self.type = TSNodeType.TEMPLATE_ELEMENT
    def accept(self, visitor):
        return visitor.visit_template_element(self) if hasattr(visitor, "visit_template_element") else None

@dataclass
class TSExpressionStatement(TSStatement):
    """Expression wrapped as a statement terminated by semicolon."""
    expression: TSNode = None
    def __post_init__(self):
        self.type = TSNodeType.EXPRESSION_STATEMENT
    def accept(self, visitor):
        return visitor.visit_expression_statement(self) if hasattr(visitor, "visit_expression_statement") else None

@dataclass
class TSIfStatement(TSStatement):
    """If statement."""
    test: TSNode = None
    consequent: TSNode = None
    alternate: Optional[TSNode] = None
    def __post_init__(self):
        self.type = TSNodeType.IF_STATEMENT
    def accept(self, visitor):
        return visitor.visit_if_statement(self) if hasattr(visitor, "visit_if_statement") else None

@dataclass
class TSWhileStatement(TSStatement):
    """While statement."""
    test: TSNode = None
    body: TSNode = None
    def __post_init__(self):
        self.type = TSNodeType.WHILE_STATEMENT
    def accept(self, visitor):
        return visitor.visit_while_statement(self) if hasattr(visitor, "visit_while_statement") else None

@dataclass
class TSDoWhileStatement(TSStatement):
    """Do-while statement."""
    body: TSNode = None
    test: TSNode = None
    def __post_init__(self):
        self.type = TSNodeType.DO_WHILE_STATEMENT
    def accept(self, visitor):
        return visitor.visit_do_while_statement(self) if hasattr(visitor, "visit_do_while_statement") else None

@dataclass
class TSForStatement(TSStatement):
    """For statement."""
    init: Optional[TSNode] = None
    test: Optional[TSNode] = None
    update: Optional[TSNode] = None
    body: Optional[TSNode] = None
    def __post_init__(self):
        self.type = TSNodeType.FOR_STATEMENT
    def accept(self, visitor):
        return visitor.visit_for_statement(self) if hasattr(visitor, "visit_for_statement") else None

@dataclass
class TSForInStatement(TSStatement):
    """For-in statement."""
    left: TSNode = None
    right: TSNode = None
    body: TSNode = None
    def __post_init__(self):
        self.type = TSNodeType.FOR_IN_STATEMENT
    def accept(self, visitor):
        return visitor.visit_for_in_statement(self) if hasattr(visitor, "visit_for_in_statement") else None

@dataclass
class TSForOfStatement(TSStatement):
    """For-of statement."""
    left: TSNode = None
    right: TSNode = None
    body: TSNode = None
    await_: bool = False  # for await...of
    def __post_init__(self):
        self.type = TSNodeType.FOR_OF_STATEMENT
    def accept(self, visitor):
        return visitor.visit_for_of_statement(self) if hasattr(visitor, "visit_for_of_statement") else None

@dataclass
class TSReturnStatement(TSStatement):
    """Return statement."""
    argument: Optional[TSNode] = None
    def __post_init__(self):
        self.type = TSNodeType.RETURN_STATEMENT
    def accept(self, visitor):
        return visitor.visit_return_statement(self) if hasattr(visitor, "visit_return_statement") else None

@dataclass
class TSBreakStatement(TSStatement):
    """Break statement."""
    label: Optional['TSIdentifier'] = None
    def __post_init__(self):
        self.type = TSNodeType.BREAK_STATEMENT
    def accept(self, visitor):
        return visitor.visit_break_statement(self) if hasattr(visitor, "visit_break_statement") else None

@dataclass
class TSContinueStatement(TSStatement):
    """Continue statement."""
    label: Optional['TSIdentifier'] = None
    def __post_init__(self):
        self.type = TSNodeType.CONTINUE_STATEMENT
    def accept(self, visitor):
        return visitor.visit_continue_statement(self) if hasattr(visitor, "visit_continue_statement") else None

@dataclass
class TSThrowStatement(TSStatement):
    """Throw statement."""
    argument: TSNode = None
    def __post_init__(self):
        self.type = TSNodeType.THROW_STATEMENT
    def accept(self, visitor):
        return visitor.visit_throw_statement(self) if hasattr(visitor, "visit_throw_statement") else None

@dataclass
class TSTryStatement(TSStatement):
    """Try statement."""
    block: 'TSBlockStatement' = None
    handler: Optional['TSCatchClause'] = None
    finalizer: Optional['TSBlockStatement'] = None
    def __post_init__(self):
        self.type = TSNodeType.TRY_STATEMENT
    def accept(self, visitor):
        return visitor.visit_try_statement(self) if hasattr(visitor, "visit_try_statement") else None

@dataclass
class TSCatchClause(TSNode):
    """Catch clause."""
    param: Optional[TSNode] = None
    body: 'TSBlockStatement' = None
    def __post_init__(self):
        self.type = TSNodeType.CATCH_CLAUSE
    def accept(self, visitor):
        return visitor.visit_catch_clause(self) if hasattr(visitor, "visit_catch_clause") else None

@dataclass
class TSSwitchStatement(TSStatement):
    """Switch statement."""
    discriminant: TSNode = None
    cases: List['TSSwitchCase'] = None
    def __post_init__(self):
        self.type = TSNodeType.SWITCH_STATEMENT
    def accept(self, visitor):
        return visitor.visit_switch_statement(self) if hasattr(visitor, "visit_switch_statement") else None

@dataclass
class TSSwitchCase(TSNode):
    """Switch case."""
    test: Optional[TSNode] = None  # None for default case
    consequent: List[TSNode] = None
    def __post_init__(self):
        self.type = TSNodeType.SWITCH_CASE
        if self.consequent is None:
            self.consequent = []
    def accept(self, visitor):
        return visitor.visit_switch_case(self) if hasattr(visitor, "visit_switch_case") else None

@dataclass
class TSEmptyStatement(TSStatement):
    """Empty statement (;)."""
    def __post_init__(self):
        self.type = TSNodeType.EMPTY_STATEMENT
    def accept(self, visitor):
        return visitor.visit_empty_statement(self) if hasattr(visitor, "visit_empty_statement") else None

@dataclass
class TSDebuggerStatement(TSStatement):
    """Debugger statement."""
    def __post_init__(self):
        self.type = TSNodeType.DEBUGGER_STATEMENT
    def accept(self, visitor):
        return visitor.visit_debugger_statement(self) if hasattr(visitor, "visit_debugger_statement") else None


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
class TSType(TSNode):
    """Base class for TypeScript type nodes."""
    pass


@dataclass
class TSLiteral(TSNode):
    """TypeScript literal node."""
    value: Any = None
    raw: str = ""
    literal_type: TSLiteralType = None
    
    def __post_init__(self):
        self.type = TSNodeType.LITERAL
    
    def accept(self, visitor):
        return visitor.visit_literal(self)


@dataclass
class TSIdentifier(TSNode):
    """TypeScript identifier node."""
    name: str = ""
    
    def __post_init__(self):
        self.type = TSNodeType.IDENTIFIER
    
    def accept(self, visitor):
        return visitor.visit_identifier(self)


@dataclass
class TSTypeAnnotation(TSNode):
    """TypeScript type annotation node."""
    type_annotation: TSType = None
    
    def __post_init__(self):
        self.type = TSNodeType.TYPE_ANNOTATION
    
    def accept(self, visitor):
        return visitor.visit_type_annotation(self)


@dataclass
class TSTypeReference(TSType):
    """TypeScript type reference node."""
    type_name: TSIdentifier = None
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
    types: List[TSType] = None
    
    def __post_init__(self):
        self.type = TSNodeType.UNION_TYPE
    
    def accept(self, visitor):
        return visitor.visit_union_type(self)


@dataclass
class TSIntersectionType(TSType):
    """TypeScript intersection type node."""
    types: List[TSType] = None
    
    def __post_init__(self):
        self.type = TSNodeType.INTERSECTION_TYPE
    
    def accept(self, visitor):
        return visitor.visit_intersection_type(self)


@dataclass
class TSTupleType(TSType):
    """TypeScript tuple type node."""
    element_types: List[TSType] = None
    
    def __post_init__(self):
        self.type = TSNodeType.TUPLE_TYPE
    
    def accept(self, visitor):
        return visitor.visit_tuple_type(self)


@dataclass
class TSArrayType(TSType):
    """TypeScript array type node."""
    element_type: TSType = None
    
    def __post_init__(self):
        self.type = TSNodeType.ARRAY_TYPE
    
    def accept(self, visitor):
        return visitor.visit_array_type(self)


@dataclass
class TSFunctionType(TSType):
    """TypeScript function type node."""
    parameters: List['TSParameter'] = None
    return_type: TSType = None
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
    members: List[TSNode] = None
    
    def __post_init__(self):
        self.type = TSNodeType.TYPE_LITERAL
    
    def accept(self, visitor):
        return visitor.visit_type_literal(self)


@dataclass
class TSMappedType(TSType):
    """TypeScript mapped type node."""
    type_parameter: 'TSTypeParameter' = None
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
    check_type: TSType = None
    extends_type: TSType = None
    true_type: TSType = None
    false_type: TSType = None
    
    def __post_init__(self):
        self.type = TSNodeType.CONDITIONAL_TYPE
    
    def accept(self, visitor):
        return visitor.visit_conditional_type(self)


@dataclass
class TSIndexedAccessType(TSType):
    """TypeScript indexed access type node."""
    object_type: TSType = None
    index_type: TSType = None
    
    def __post_init__(self):
        self.type = TSNodeType.INDEX_TYPE
    
    def accept(self, visitor):
        return visitor.visit_indexed_access_type(self)


@dataclass
class TSTypeofType(TSType):
    """TypeScript typeof type node."""
    expression: TSNode = None
    
    def __post_init__(self):
        self.type = TSNodeType.TYPEOF_TYPE
    
    def accept(self, visitor):
        return visitor.visit_typeof_type(self)


@dataclass
class TSKeyofType(TSType):
    """TypeScript keyof type node."""
    type_operand: TSType = None
    
    def __post_init__(self):
        self.type = TSNodeType.KEYOF_TYPE
    
    def accept(self, visitor):
        return visitor.visit_keyof_type(self)


@dataclass
class TSTypeParameter(TSNode):
    """TypeScript type parameter node."""
    name: TSIdentifier = None
    constraint: Optional[TSType] = None
    default_type: Optional[TSType] = None
    
    def __post_init__(self):
        self.type = TSNodeType.TYPE_PARAMETER
    
    def accept(self, visitor):
        return visitor.visit_type_parameter(self)


@dataclass
class TSTypeAssertion(TSNode):
    """TypeScript type assertion node."""
    type_annotation: TSType = None
    expression: TSNode = None
    
    def __post_init__(self):
        self.type = TSNodeType.TYPE_ASSERTION
    
    def accept(self, visitor):
        return visitor.visit_type_assertion(self)


@dataclass
class TSTypePredicate(TSType):
    """TypeScript type predicate node."""
    parameter_name: TSIdentifier = None
    type_annotation: Optional[TSType] = None
    asserts_modifier: bool = False
    
    def __post_init__(self):
        self.type = TSNodeType.TYPE_PREDICATE
    
    def accept(self, visitor):
        return visitor.visit_type_predicate(self)


@dataclass
class TSParameter(TSNode):
    """TypeScript parameter node."""
    name: TSIdentifier = None
    type_annotation: Optional[TSTypeAnnotation] = None
    default_value: Optional[TSNode] = None
    optional: bool = False
    rest: bool = False
    access_modifier: Optional[TSAccessModifier] = None
    readonly: bool = False
    
    def accept(self, visitor):
        return visitor.visit_parameter(self)


@dataclass
class TSInterfaceDeclaration(TSDeclaration):
    """TypeScript interface declaration node."""
    name: TSIdentifier = None
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
class TSTypeAliasDeclaration(TSDeclaration):
    """TypeScript type alias declaration node."""
    name: TSIdentifier = None
    type_parameters: Optional[List[TSTypeParameter]] = None
    type_annotation: TSType = None
    
    def __post_init__(self):
        self.type = TSNodeType.TYPE_ALIAS_DECLARATION
        if self.type_parameters is None:
            self.type_parameters = []
    
    def accept(self, visitor):
        return visitor.visit_type_alias_declaration(self)


@dataclass
class TSEnumDeclaration(TSDeclaration):
    """TypeScript enum declaration node."""
    name: TSIdentifier = None
    members: List['TSEnumMember'] = None
    const: bool = False
    
    def __post_init__(self):
        self.type = TSNodeType.ENUM_DECLARATION
    
    def accept(self, visitor):
        return visitor.visit_enum_declaration(self)


@dataclass
class TSEnumMember(TSNode):
    """TypeScript enum member node."""
    name: TSIdentifier = None
    initializer: Optional[TSNode] = None
    
    def accept(self, visitor):
        return visitor.visit_enum_member(self)


@dataclass
class TSNamespaceDeclaration(TSDeclaration):
    """TypeScript namespace declaration node."""
    name: TSIdentifier = None
    body: List[TSNode] = None
    
    def __post_init__(self):
        self.type = TSNodeType.NAMESPACE_DECLARATION
    
    def accept(self, visitor):
        return visitor.visit_namespace_declaration(self)


@dataclass
class TSModuleDeclaration(TSDeclaration):
    """TypeScript module declaration node."""
    name: TSIdentifier = None
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
    expression: TSNode = None
    
    def __post_init__(self):
        self.type = TSNodeType.DECORATOR
    
    def accept(self, visitor):
        return visitor.visit_decorator(self)


@dataclass
class TSMethodSignature(TSNode):
    """TypeScript method signature node."""
    name: TSIdentifier = None
    parameters: List[TSParameter] = None
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
    name: TSIdentifier = None
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
    parameters: List[TSParameter] = None
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
    parameters: List[TSParameter] = None
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
    parameters: List[TSParameter] = None
    type_annotation: TSTypeAnnotation = None
    readonly: bool = False
    
    def __post_init__(self):
        self.type = TSNodeType.INDEX_SIGNATURE
    
    def accept(self, visitor):
        return visitor.visit_index_signature(self)


@dataclass
class TSVariableDeclaration(TSDeclaration):
    """TypeScript variable declaration node."""
    declarations: List['TSVariableDeclarator'] = None
    kind: TSVariableKind = None
    
    def __post_init__(self):
        self.type = TSNodeType.VARIABLE_DECLARATION
    
    def accept(self, visitor):
        return visitor.visit_variable_declaration(self)


@dataclass
class TSVariableDeclarator(TSNode):
    """TypeScript variable declarator node."""
    id: TSIdentifier = None
    type_annotation: Optional[TSTypeAnnotation] = None
    init: Optional[TSNode] = None
    
    def accept(self, visitor):
        return visitor.visit_variable_declarator(self)


@dataclass
class TSFunctionDeclaration(TSDeclaration):
    """TypeScript function declaration node."""
    name: TSIdentifier = None
    parameters: List[TSParameter] = None
    body: 'TSBlockStatement' = None
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
class TSClassDeclaration(TSDeclaration):
    """TypeScript class declaration node."""
    name: TSIdentifier = None
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
    body: List[TSNode] = None
    
    def __post_init__(self):
        self.type = TSNodeType.BLOCK_STATEMENT
    
    def accept(self, visitor):
        return visitor.visit_block_statement(self)


@dataclass
class TSProgram(TSNode):
    """TypeScript program node."""
    body: List[TSNode] = None
    source_type: str = "module"  # "script" or "module"
    
    def __post_init__(self):
        self.type = TSNodeType.PROGRAM
    
    def accept(self, visitor):
        return visitor.visit_program(self)