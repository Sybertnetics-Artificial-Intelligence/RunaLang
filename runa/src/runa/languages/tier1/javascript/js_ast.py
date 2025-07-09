#!/usr/bin/env python3
"""
JavaScript AST Node Definitions

Comprehensive Abstract Syntax Tree nodes for JavaScript covering
all language features from ES5 to ES2023 including modern features
like async/await, destructuring, modules, and more.
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod


class JSNodeType(Enum):
    """JavaScript AST node types."""
    # Literals
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
    
    # Destructuring
    ARRAY_PATTERN = auto()
    OBJECT_PATTERN = auto()
    ASSIGNMENT_PATTERN = auto()
    REST_ELEMENT = auto()
    
    # Statements
    EXPRESSION_STATEMENT = auto()
    BLOCK_STATEMENT = auto()
    EMPTY_STATEMENT = auto()
    DEBUGGER_STATEMENT = auto()
    
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
    
    # Modules
    IMPORT_DECLARATION = auto()
    EXPORT_NAMED_DECLARATION = auto()
    EXPORT_DEFAULT_DECLARATION = auto()
    EXPORT_ALL_DECLARATION = auto()
    
    # Async/Await
    AWAIT_EXPRESSION = auto()
    YIELD_EXPRESSION = auto()
    
    # Program
    PROGRAM = auto()
    
    # Switch Case
    SWITCH_CASE = auto()
    CATCH_CLAUSE = auto()
    
    # Property
    PROPERTY = auto()
    METHOD_DEFINITION = auto()
    
    # Import/Export Specifiers
    IMPORT_SPECIFIER = auto()
    IMPORT_DEFAULT_SPECIFIER = auto()
    IMPORT_NAMESPACE_SPECIFIER = auto()
    EXPORT_SPECIFIER = auto()
    
    # Variable Declarator
    VARIABLE_DECLARATOR = auto()
    
    # Sequence
    SEQUENCE_EXPRESSION = auto()
    
    # Tagged Template
    TAGGED_TEMPLATE_EXPRESSION = auto()
    
    # MetaProperty
    META_PROPERTY = auto()


class JSLiteralType(Enum):
    """JavaScript literal types."""
    NULL = "null"
    BOOLEAN = "boolean"
    NUMBER = "number"
    STRING = "string"
    REGEX = "regex"
    BIGINT = "bigint"


class JSOperator(Enum):
    """JavaScript operators."""
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
    
    # Others
    IN = "in"
    INSTANCEOF = "instanceof"
    OPTIONAL_CHAINING = "?."


class JSVariableKind(Enum):
    """JavaScript variable declaration kinds."""
    VAR = "var"
    LET = "let"
    CONST = "const"


class JSFunctionKind(Enum):
    """JavaScript function kinds."""
    FUNCTION = "function"
    ASYNC = "async"
    GENERATOR = "generator"
    ASYNC_GENERATOR = "async_generator"


class JSPropertyKind(Enum):
    """JavaScript property kinds."""
    INIT = "init"
    GET = "get"
    SET = "set"
    METHOD = "method"
    CONSTRUCTOR = "constructor"


class JSModuleKind(Enum):
    """JavaScript module kinds."""
    COMMONJS = "commonjs"
    ES_MODULE = "es_module"


@dataclass
class JSNode(ABC):
    """Base class for all JavaScript AST nodes."""
    type: JSNodeType = None
    loc: Optional[Dict[str, Any]] = None
    range: Optional[List[int]] = None
    
    @abstractmethod
    def accept(self, visitor):
        """Accept a visitor for the visitor pattern."""
        pass


@dataclass
class JSLiteral(JSNode):
    """JavaScript literal node."""
    value: Any
    raw: str
    literal_type: JSLiteralType
    
    def __post_init__(self):
        self.type = JSNodeType.LITERAL
    
    def accept(self, visitor):
        return visitor.visit_literal(self)


@dataclass
class JSIdentifier(JSNode):
    """JavaScript identifier node."""
    name: str
    
    def __post_init__(self):
        self.type = JSNodeType.IDENTIFIER
    
    def accept(self, visitor):
        return visitor.visit_identifier(self)


@dataclass
class JSTemplateLiteral(JSNode):
    """JavaScript template literal node."""
    quasis: List[JSNode]
    expressions: List[JSNode]
    
    def __init__(self, quasis: List[JSNode], expressions: List[JSNode]):
        super().__init__(JSNodeType.TEMPLATE_LITERAL)
        self.quasis = quasis
        self.expressions = expressions
    
    def accept(self, visitor):
        return visitor.visit_template_literal(self)


@dataclass
class JSArrayExpression(JSNode):
    """JavaScript array expression node."""
    elements: List[Optional[JSNode]]
    
    def __init__(self, elements: List[Optional[JSNode]]):
        super().__init__(JSNodeType.ARRAY_EXPRESSION)
        self.elements = elements
    
    def accept(self, visitor):
        return visitor.visit_array_expression(self)


@dataclass
class JSObjectExpression(JSNode):
    """JavaScript object expression node."""
    properties: List[JSNode]
    
    def __init__(self, properties: List[JSNode]):
        super().__init__(JSNodeType.OBJECT_EXPRESSION)
        self.properties = properties
    
    def accept(self, visitor):
        return visitor.visit_object_expression(self)


@dataclass
class JSProperty(JSNode):
    """JavaScript property node."""
    key: JSNode
    value: JSNode
    kind: JSPropertyKind
    computed: bool = False
    shorthand: bool = False
    method: bool = False
    
    def __init__(self, key: JSNode, value: JSNode, kind: JSPropertyKind, 
                 computed: bool = False, shorthand: bool = False, method: bool = False):
        super().__init__(JSNodeType.PROPERTY)
        self.key = key
        self.value = value
        self.kind = kind
        self.computed = computed
        self.shorthand = shorthand
        self.method = method
    
    def accept(self, visitor):
        return visitor.visit_property(self)


@dataclass
class JSFunctionExpression(JSNode):
    """JavaScript function expression node."""
    id: Optional[JSIdentifier]
    params: List[JSNode]
    body: JSNode
    generator: bool = False
    async_: bool = False
    
    def __init__(self, id: Optional[JSIdentifier], params: List[JSNode], body: JSNode,
                 generator: bool = False, async_: bool = False):
        super().__init__(JSNodeType.FUNCTION_EXPRESSION)
        self.id = id
        self.params = params
        self.body = body
        self.generator = generator
        self.async_ = async_
    
    def accept(self, visitor):
        return visitor.visit_function_expression(self)


@dataclass
class JSArrowFunctionExpression(JSNode):
    """JavaScript arrow function expression node."""
    params: List[JSNode]
    body: JSNode
    expression: bool = False
    async_: bool = False
    
    def __init__(self, params: List[JSNode], body: JSNode, expression: bool = False, async_: bool = False):
        super().__init__(JSNodeType.ARROW_FUNCTION_EXPRESSION)
        self.params = params
        self.body = body
        self.expression = expression
        self.async_ = async_
    
    def accept(self, visitor):
        return visitor.visit_arrow_function_expression(self)


@dataclass
class JSBinaryExpression(JSNode):
    """JavaScript binary expression node."""
    left: JSNode
    operator: JSOperator
    right: JSNode
    
    def __init__(self, left: JSNode, operator: JSOperator, right: JSNode):
        super().__init__(JSNodeType.BINARY_EXPRESSION)
        self.left = left
        self.operator = operator
        self.right = right
    
    def accept(self, visitor):
        return visitor.visit_binary_expression(self)


@dataclass
class JSUnaryExpression(JSNode):
    """JavaScript unary expression node."""
    operator: JSOperator
    argument: JSNode
    prefix: bool = True
    
    def __init__(self, operator: JSOperator, argument: JSNode, prefix: bool = True):
        super().__init__(JSNodeType.UNARY_EXPRESSION)
        self.operator = operator
        self.argument = argument
        self.prefix = prefix
    
    def accept(self, visitor):
        return visitor.visit_unary_expression(self)


@dataclass
class JSUpdateExpression(JSNode):
    """JavaScript update expression node."""
    operator: JSOperator
    argument: JSNode
    prefix: bool = True
    
    def __init__(self, operator: JSOperator, argument: JSNode, prefix: bool = True):
        super().__init__(JSNodeType.UPDATE_EXPRESSION)
        self.operator = operator
        self.argument = argument
        self.prefix = prefix
    
    def accept(self, visitor):
        return visitor.visit_update_expression(self)


@dataclass
class JSAssignmentExpression(JSNode):
    """JavaScript assignment expression node."""
    left: JSNode
    operator: JSOperator
    right: JSNode
    
    def __init__(self, left: JSNode, operator: JSOperator, right: JSNode):
        super().__init__(JSNodeType.ASSIGNMENT_EXPRESSION)
        self.left = left
        self.operator = operator
        self.right = right
    
    def accept(self, visitor):
        return visitor.visit_assignment_expression(self)


@dataclass
class JSLogicalExpression(JSNode):
    """JavaScript logical expression node."""
    left: JSNode
    operator: JSOperator
    right: JSNode
    
    def __init__(self, left: JSNode, operator: JSOperator, right: JSNode):
        super().__init__(JSNodeType.LOGICAL_EXPRESSION)
        self.left = left
        self.operator = operator
        self.right = right
    
    def accept(self, visitor):
        return visitor.visit_logical_expression(self)


@dataclass
class JSConditionalExpression(JSNode):
    """JavaScript conditional expression node."""
    test: JSNode
    consequent: JSNode
    alternate: JSNode
    
    def __init__(self, test: JSNode, consequent: JSNode, alternate: JSNode):
        super().__init__(JSNodeType.CONDITIONAL_EXPRESSION)
        self.test = test
        self.consequent = consequent
        self.alternate = alternate
    
    def accept(self, visitor):
        return visitor.visit_conditional_expression(self)


@dataclass
class JSMemberExpression(JSNode):
    """JavaScript member expression node."""
    object: JSNode
    property: JSNode
    computed: bool = False
    optional: bool = False
    
    def __init__(self, object: JSNode, property: JSNode, computed: bool = False, optional: bool = False):
        super().__init__(JSNodeType.MEMBER_EXPRESSION)
        self.object = object
        self.property = property
        self.computed = computed
        self.optional = optional
    
    def accept(self, visitor):
        return visitor.visit_member_expression(self)


@dataclass
class JSCallExpression(JSNode):
    """JavaScript call expression node."""
    callee: JSNode
    arguments: List[JSNode]
    optional: bool = False
    
    def __init__(self, callee: JSNode, arguments: List[JSNode], optional: bool = False):
        super().__init__(JSNodeType.CALL_EXPRESSION)
        self.callee = callee
        self.arguments = arguments
        self.optional = optional
    
    def accept(self, visitor):
        return visitor.visit_call_expression(self)


@dataclass
class JSNewExpression(JSNode):
    """JavaScript new expression node."""
    callee: JSNode
    arguments: List[JSNode]
    
    def __init__(self, callee: JSNode, arguments: List[JSNode]):
        super().__init__(JSNodeType.NEW_EXPRESSION)
        self.callee = callee
        self.arguments = arguments
    
    def accept(self, visitor):
        return visitor.visit_new_expression(self)


@dataclass
class JSThisExpression(JSNode):
    """JavaScript this expression node."""
    
    def __init__(self):
        super().__init__(JSNodeType.THIS_EXPRESSION)
    
    def accept(self, visitor):
        return visitor.visit_this_expression(self)


@dataclass
class JSSuper(JSNode):
    """JavaScript super node."""
    
    def __init__(self):
        super().__init__(JSNodeType.SUPER)
    
    def accept(self, visitor):
        return visitor.visit_super(self)


@dataclass
class JSSequenceExpression(JSNode):
    """JavaScript sequence expression node."""
    expressions: List[JSNode]
    
    def __init__(self, expressions: List[JSNode]):
        super().__init__(JSNodeType.SEQUENCE_EXPRESSION)
        self.expressions = expressions
    
    def accept(self, visitor):
        return visitor.visit_sequence_expression(self)


@dataclass
class JSAwaitExpression(JSNode):
    """JavaScript await expression node."""
    argument: JSNode
    
    def __init__(self, argument: JSNode):
        super().__init__(JSNodeType.AWAIT_EXPRESSION)
        self.argument = argument
    
    def accept(self, visitor):
        return visitor.visit_await_expression(self)


@dataclass
class JSYieldExpression(JSNode):
    """JavaScript yield expression node."""
    argument: Optional[JSNode]
    delegate: bool = False
    
    def __init__(self, argument: Optional[JSNode], delegate: bool = False):
        super().__init__(JSNodeType.YIELD_EXPRESSION)
        self.argument = argument
        self.delegate = delegate
    
    def accept(self, visitor):
        return visitor.visit_yield_expression(self)


# Statement nodes

@dataclass
class JSExpressionStatement(JSNode):
    """JavaScript expression statement node."""
    expression: JSNode
    
    def __init__(self, expression: JSNode):
        super().__init__(JSNodeType.EXPRESSION_STATEMENT)
        self.expression = expression
    
    def accept(self, visitor):
        return visitor.visit_expression_statement(self)


@dataclass
class JSBlockStatement(JSNode):
    """JavaScript block statement node."""
    body: List[JSNode]
    
    def __init__(self, body: List[JSNode]):
        super().__init__(JSNodeType.BLOCK_STATEMENT)
        self.body = body
    
    def accept(self, visitor):
        return visitor.visit_block_statement(self)


@dataclass
class JSEmptyStatement(JSNode):
    """JavaScript empty statement node."""
    
    def __init__(self):
        super().__init__(JSNodeType.EMPTY_STATEMENT)
    
    def accept(self, visitor):
        return visitor.visit_empty_statement(self)


@dataclass
class JSDebuggerStatement(JSNode):
    """JavaScript debugger statement node."""
    
    def __init__(self):
        super().__init__(JSNodeType.DEBUGGER_STATEMENT)
    
    def accept(self, visitor):
        return visitor.visit_debugger_statement(self)


@dataclass
class JSIfStatement(JSNode):
    """JavaScript if statement node."""
    test: JSNode
    consequent: JSNode
    alternate: Optional[JSNode] = None
    
    def __init__(self, test: JSNode, consequent: JSNode, alternate: Optional[JSNode] = None):
        super().__init__(JSNodeType.IF_STATEMENT)
        self.test = test
        self.consequent = consequent
        self.alternate = alternate
    
    def accept(self, visitor):
        return visitor.visit_if_statement(self)


@dataclass
class JSWhileStatement(JSNode):
    """JavaScript while statement node."""
    test: JSNode
    body: JSNode
    
    def __init__(self, test: JSNode, body: JSNode):
        super().__init__(JSNodeType.WHILE_STATEMENT)
        self.test = test
        self.body = body
    
    def accept(self, visitor):
        return visitor.visit_while_statement(self)


@dataclass
class JSForStatement(JSNode):
    """JavaScript for statement node."""
    init: Optional[JSNode]
    test: Optional[JSNode]
    update: Optional[JSNode]
    body: JSNode
    
    def __init__(self, init: Optional[JSNode], test: Optional[JSNode], 
                 update: Optional[JSNode], body: JSNode):
        super().__init__(JSNodeType.FOR_STATEMENT)
        self.init = init
        self.test = test
        self.update = update
        self.body = body
    
    def accept(self, visitor):
        return visitor.visit_for_statement(self)


@dataclass
class JSReturnStatement(JSNode):
    """JavaScript return statement node."""
    argument: Optional[JSNode] = None
    
    def __init__(self, argument: Optional[JSNode] = None):
        super().__init__(JSNodeType.RETURN_STATEMENT)
        self.argument = argument
    
    def accept(self, visitor):
        return visitor.visit_return_statement(self)


@dataclass
class JSBreakStatement(JSNode):
    """JavaScript break statement node."""
    label: Optional[JSIdentifier] = None
    
    def __init__(self, label: Optional[JSIdentifier] = None):
        super().__init__(JSNodeType.BREAK_STATEMENT)
        self.label = label
    
    def accept(self, visitor):
        return visitor.visit_break_statement(self)


@dataclass
class JSContinueStatement(JSNode):
    """JavaScript continue statement node."""
    label: Optional[JSIdentifier] = None
    
    def __init__(self, label: Optional[JSIdentifier] = None):
        super().__init__(JSNodeType.CONTINUE_STATEMENT)
        self.label = label
    
    def accept(self, visitor):
        return visitor.visit_continue_statement(self)


@dataclass
class JSThrowStatement(JSNode):
    """JavaScript throw statement node."""
    argument: JSNode
    
    def __init__(self, argument: JSNode):
        super().__init__(JSNodeType.THROW_STATEMENT)
        self.argument = argument
    
    def accept(self, visitor):
        return visitor.visit_throw_statement(self)


@dataclass
class JSTryStatement(JSNode):
    """JavaScript try statement node."""
    block: JSNode
    handler: Optional[JSNode] = None
    finalizer: Optional[JSNode] = None
    
    def __init__(self, block: JSNode, handler: Optional[JSNode] = None, 
                 finalizer: Optional[JSNode] = None):
        super().__init__(JSNodeType.TRY_STATEMENT)
        self.block = block
        self.handler = handler
        self.finalizer = finalizer
    
    def accept(self, visitor):
        return visitor.visit_try_statement(self)


@dataclass
class JSCatchClause(JSNode):
    """JavaScript catch clause node."""
    param: Optional[JSNode]
    body: JSNode
    
    def __init__(self, param: Optional[JSNode], body: JSNode):
        super().__init__(JSNodeType.CATCH_CLAUSE)
        self.param = param
        self.body = body
    
    def accept(self, visitor):
        return visitor.visit_catch_clause(self)


@dataclass
class JSVariableDeclaration(JSNode):
    """JavaScript variable declaration node."""
    declarations: List[JSNode]
    kind: JSVariableKind
    
    def __init__(self, declarations: List[JSNode], kind: JSVariableKind):
        super().__init__(JSNodeType.VARIABLE_DECLARATION)
        self.declarations = declarations
        self.kind = kind
    
    def accept(self, visitor):
        return visitor.visit_variable_declaration(self)


@dataclass
class JSVariableDeclarator(JSNode):
    """JavaScript variable declarator node."""
    id: JSNode
    init: Optional[JSNode] = None
    
    def __init__(self, id: JSNode, init: Optional[JSNode] = None):
        super().__init__(JSNodeType.VARIABLE_DECLARATOR)
        self.id = id
        self.init = init
    
    def accept(self, visitor):
        return visitor.visit_variable_declarator(self)


@dataclass
class JSFunctionDeclaration(JSNode):
    """JavaScript function declaration node."""
    id: JSIdentifier
    params: List[JSNode]
    body: JSNode
    generator: bool = False
    async_: bool = False
    
    def __init__(self, id: JSIdentifier, params: List[JSNode], body: JSNode,
                 generator: bool = False, async_: bool = False):
        super().__init__(JSNodeType.FUNCTION_DECLARATION)
        self.id = id
        self.params = params
        self.body = body
        self.generator = generator
        self.async_ = async_
    
    def accept(self, visitor):
        return visitor.visit_function_declaration(self)


@dataclass
class JSProgram(JSNode):
    """JavaScript program node."""
    body: List[JSNode]
    source_type: str = "script"  # "script" or "module"
    
    def __init__(self, body: List[JSNode], source_type: str = "script"):
        super().__init__(JSNodeType.PROGRAM)
        self.body = body
        self.source_type = source_type
    
    def accept(self, visitor):
        return visitor.visit_program(self)


class JSNodeVisitor(ABC):
    """Abstract base class for JavaScript AST visitors."""
    
    @abstractmethod
    def visit_literal(self, node: JSLiteral): pass
    
    @abstractmethod
    def visit_identifier(self, node: JSIdentifier): pass
    
    @abstractmethod
    def visit_binary_expression(self, node: JSBinaryExpression): pass
    
    @abstractmethod
    def visit_unary_expression(self, node: JSUnaryExpression): pass
    
    @abstractmethod
    def visit_call_expression(self, node: JSCallExpression): pass
    
    @abstractmethod
    def visit_member_expression(self, node: JSMemberExpression): pass
    
    @abstractmethod
    def visit_function_expression(self, node: JSFunctionExpression): pass
    
    @abstractmethod
    def visit_arrow_function_expression(self, node: JSArrowFunctionExpression): pass
    
    @abstractmethod
    def visit_object_expression(self, node: JSObjectExpression): pass
    
    @abstractmethod
    def visit_array_expression(self, node: JSArrayExpression): pass
    
    @abstractmethod
    def visit_property(self, node: JSProperty): pass
    
    @abstractmethod
    def visit_assignment_expression(self, node: JSAssignmentExpression): pass
    
    @abstractmethod
    def visit_update_expression(self, node: JSUpdateExpression): pass
    
    @abstractmethod
    def visit_logical_expression(self, node: JSLogicalExpression): pass
    
    @abstractmethod
    def visit_conditional_expression(self, node: JSConditionalExpression): pass
    
    @abstractmethod
    def visit_new_expression(self, node: JSNewExpression): pass
    
    @abstractmethod
    def visit_this_expression(self, node: JSThisExpression): pass
    
    @abstractmethod
    def visit_super(self, node: JSSuper): pass
    
    @abstractmethod
    def visit_sequence_expression(self, node: JSSequenceExpression): pass
    
    @abstractmethod
    def visit_await_expression(self, node: JSAwaitExpression): pass
    
    @abstractmethod
    def visit_yield_expression(self, node: JSYieldExpression): pass
    
    @abstractmethod
    def visit_template_literal(self, node: JSTemplateLiteral): pass
    
    @abstractmethod
    def visit_expression_statement(self, node: JSExpressionStatement): pass
    
    @abstractmethod
    def visit_block_statement(self, node: JSBlockStatement): pass
    
    @abstractmethod
    def visit_empty_statement(self, node: JSEmptyStatement): pass
    
    @abstractmethod
    def visit_debugger_statement(self, node: JSDebuggerStatement): pass
    
    @abstractmethod
    def visit_if_statement(self, node: JSIfStatement): pass
    
    @abstractmethod
    def visit_while_statement(self, node: JSWhileStatement): pass
    
    @abstractmethod
    def visit_for_statement(self, node: JSForStatement): pass
    
    @abstractmethod
    def visit_return_statement(self, node: JSReturnStatement): pass
    
    @abstractmethod
    def visit_break_statement(self, node: JSBreakStatement): pass
    
    @abstractmethod
    def visit_continue_statement(self, node: JSContinueStatement): pass
    
    @abstractmethod
    def visit_throw_statement(self, node: JSThrowStatement): pass
    
    @abstractmethod
    def visit_try_statement(self, node: JSTryStatement): pass
    
    @abstractmethod
    def visit_catch_clause(self, node: JSCatchClause): pass
    
    @abstractmethod
    def visit_variable_declaration(self, node: JSVariableDeclaration): pass
    
    @abstractmethod
    def visit_variable_declarator(self, node: JSVariableDeclarator): pass
    
    @abstractmethod
    def visit_function_declaration(self, node: JSFunctionDeclaration): pass
    
    @abstractmethod
    def visit_program(self, node: JSProgram): pass