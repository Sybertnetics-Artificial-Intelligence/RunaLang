#!/usr/bin/env python3
"""
C++ AST Node Definitions

Comprehensive Abstract Syntax Tree nodes for C++ covering
all language features from C++11 through C++23 including
templates, lambdas, concepts, modules, and modern C++ constructs.
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod


class CppNodeType(Enum):
    """C++ AST node types."""
    # Literals
    LITERAL = auto()
    INTEGER_LITERAL = auto()
    FLOATING_LITERAL = auto()
    STRING_LITERAL = auto()
    CHARACTER_LITERAL = auto()
    BOOLEAN_LITERAL = auto()
    NULLPTR_LITERAL = auto()
    USER_DEFINED_LITERAL = auto()
    
    # Identifiers and names
    IDENTIFIER = auto()
    QUALIFIED_NAME = auto()
    TEMPLATE_NAME = auto()
    OPERATOR_NAME = auto()
    DESTRUCTOR_NAME = auto()
    
    # Expressions
    BINARY_OP = auto()
    UNARY_OP = auto()
    CONDITIONAL = auto()  # Ternary operator
    ASSIGNMENT = auto()
    COMPOUND_ASSIGNMENT = auto()
    CALL = auto()
    MEMBER_ACCESS = auto()
    ARRAY_SUBSCRIPT = auto()
    CAST = auto()
    STATIC_CAST = auto()
    DYNAMIC_CAST = auto()
    CONST_CAST = auto()
    REINTERPRET_CAST = auto()
    SIZEOF = auto()
    ALIGNOF = auto()
    TYPEID = auto()
    NEW = auto()
    DELETE = auto()
    THROW = auto()
    LAMBDA = auto()
    PACK_EXPANSION = auto()
    FOLD_EXPRESSION = auto()  # C++17
    REQUIRES_EXPRESSION = auto()  # C++20
    
    # Statements
    EXPRESSION_STMT = auto()
    COMPOUND_STMT = auto()
    IF_STMT = auto()
    SWITCH_STMT = auto()
    WHILE_STMT = auto()
    DO_WHILE_STMT = auto()
    FOR_STMT = auto()
    RANGE_FOR_STMT = auto()  # C++11
    BREAK_STMT = auto()
    CONTINUE_STMT = auto()
    RETURN_STMT = auto()
    GOTO_STMT = auto()
    LABEL_STMT = auto()
    TRY_STMT = auto()
    DECLARATION_STMT = auto()
    
    # Declarations
    VARIABLE_DECL = auto()
    FUNCTION_DECL = auto()
    CLASS_DECL = auto()
    STRUCT_DECL = auto()
    UNION_DECL = auto()
    ENUM_DECL = auto()
    TYPEDEF_DECL = auto()
    USING_DECL = auto()
    USING_DIRECTIVE = auto()
    NAMESPACE_DECL = auto()
    TEMPLATE_DECL = auto()
    FRIEND_DECL = auto()
    STATIC_ASSERT_DECL = auto()
    ALIAS_DECL = auto()  # C++11
    
    # Template constructs
    TEMPLATE_PARAMETER = auto()
    TEMPLATE_ARGUMENT = auto()
    TEMPLATE_SPECIALIZATION = auto()
    TEMPLATE_INSTANTIATION = auto()
    CONCEPT_DECL = auto()  # C++20
    
    # Types
    BUILTIN_TYPE = auto()
    POINTER_TYPE = auto()
    REFERENCE_TYPE = auto()
    RVALUE_REFERENCE_TYPE = auto()  # C++11
    ARRAY_TYPE = auto()
    FUNCTION_TYPE = auto()
    CLASS_TYPE = auto()
    ENUM_TYPE = auto()
    TEMPLATE_TYPE = auto()
    AUTO_TYPE = auto()  # C++11
    DECLTYPE_TYPE = auto()  # C++11
    
    # Class members
    FIELD_DECL = auto()
    METHOD_DECL = auto()
    CONSTRUCTOR_DECL = auto()
    DESTRUCTOR_DECL = auto()
    CONVERSION_DECL = auto()
    ACCESS_SPECIFIER = auto()
    
    # Special constructs
    INITIALIZER_LIST = auto()  # C++11
    DESIGNATED_INITIALIZER = auto()  # C++20
    STRUCTURED_BINDING = auto()  # C++17
    COROUTINE_RETURN = auto()  # C++20
    COROUTINE_YIELD = auto()  # C++20
    COROUTINE_AWAIT = auto()  # C++20
    
    # Module constructs (C++20)
    MODULE_DECL = auto()
    IMPORT_DECL = auto()
    EXPORT_DECL = auto()
    
    # Translation unit
    TRANSLATION_UNIT = auto()


class CppOperator(Enum):
    """C++ operators."""
    # Arithmetic
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"
    MOD = "%"
    
    # Bitwise
    BIT_AND = "&"
    BIT_OR = "|"
    BIT_XOR = "^"
    BIT_NOT = "~"
    LEFT_SHIFT = "<<"
    RIGHT_SHIFT = ">>"
    
    # Logical
    LOGICAL_AND = "&&"
    LOGICAL_OR = "||"
    LOGICAL_NOT = "!"
    
    # Comparison
    EQ = "=="
    NE = "!="
    LT = "<"
    LE = "<="
    GT = ">"
    GE = ">="
    SPACESHIP = "<=>"  # C++20
    
    # Assignment
    ASSIGN = "="
    ADD_ASSIGN = "+="
    SUB_ASSIGN = "-="
    MUL_ASSIGN = "*="
    DIV_ASSIGN = "/="
    MOD_ASSIGN = "%="
    BIT_AND_ASSIGN = "&="
    BIT_OR_ASSIGN = "|="
    BIT_XOR_ASSIGN = "^="
    LEFT_SHIFT_ASSIGN = "<<="
    RIGHT_SHIFT_ASSIGN = ">>="
    
    # Increment/Decrement
    PRE_INC = "++pre"
    POST_INC = "post++"
    PRE_DEC = "--pre"
    POST_DEC = "post--"
    
    # Member access
    DOT = "."
    ARROW = "->"
    DOT_STAR = ".*"
    ARROW_STAR = "->*"
    
    # Other
    SCOPE = "::"
    TERNARY = "?:"
    COMMA = ","
    SUBSCRIPT = "[]"
    FUNCTION_CALL = "()"


class CppAccessSpecifier(Enum):
    """C++ access specifiers."""
    PUBLIC = "public"
    PRIVATE = "private"
    PROTECTED = "protected"


class CppStorageClass(Enum):
    """C++ storage class specifiers."""
    STATIC = "static"
    EXTERN = "extern"
    MUTABLE = "mutable"
    THREAD_LOCAL = "thread_local"  # C++11
    REGISTER = "register"
    AUTO = "auto"


class CppTypeQualifier(Enum):
    """C++ type qualifiers."""
    CONST = "const"
    VOLATILE = "volatile"
    RESTRICT = "restrict"


@dataclass
class CppNode(ABC):
    """Base class for all C++ AST nodes."""
    type: CppNodeType = None
    source_location: Optional[Dict[str, int]] = None
    
    @abstractmethod
    def accept(self, visitor):
        """Accept a visitor for the visitor pattern."""
        pass


@dataclass
class CppExpression(CppNode):
    """Base class for C++ expressions."""
    value_category: Optional[str] = None  # lvalue, rvalue, xvalue
    cpp_type: Optional['CppType'] = None


@dataclass
class CppStatement(CppNode):
    """Base class for C++ statements."""
    pass


@dataclass
class CppDeclaration(CppNode):
    """Base class for C++ declarations."""
    pass


@dataclass
class CppType(CppNode):
    """Base class for C++ types."""
    qualifiers: List[CppTypeQualifier] = field(default_factory=list)


# Literal nodes
@dataclass
class CppLiteral(CppExpression):
    """Base class for C++ literals."""
    value: Any
    suffix: Optional[str] = None


@dataclass
class CppIntegerLiteral(CppLiteral):
    """C++ integer literal."""
    base: int = 10  # 2, 8, 10, 16
    
    def __post_init__(self):
        self.type = CppNodeType.INTEGER_LITERAL
    
    def accept(self, visitor):
        return visitor.visit_integer_literal(self)


@dataclass
class CppFloatingLiteral(CppLiteral):
    """C++ floating point literal."""
    
    def __post_init__(self):
        self.type = CppNodeType.FLOATING_LITERAL
    
    def accept(self, visitor):
        return visitor.visit_floating_literal(self)


@dataclass
class CppStringLiteral(CppLiteral):
    """C++ string literal."""
    prefix: Optional[str] = None  # u8, u, U, L, R
    
    def __post_init__(self):
        self.type = CppNodeType.STRING_LITERAL
    
    def accept(self, visitor):
        return visitor.visit_string_literal(self)


@dataclass
class CppCharacterLiteral(CppLiteral):
    """C++ character literal."""
    prefix: Optional[str] = None  # u, U, L
    
    def __post_init__(self):
        self.type = CppNodeType.CHARACTER_LITERAL
    
    def accept(self, visitor):
        return visitor.visit_character_literal(self)


@dataclass
class CppBooleanLiteral(CppLiteral):
    """C++ boolean literal."""
    
    def __post_init__(self):
        self.type = CppNodeType.BOOLEAN_LITERAL
    
    def accept(self, visitor):
        return visitor.visit_boolean_literal(self)


@dataclass
class CppNullptrLiteral(CppLiteral):
    """C++ nullptr literal (C++11)."""
    
    def __post_init__(self):
        self.type = CppNodeType.NULLPTR_LITERAL
        self.value = None
    
    def accept(self, visitor):
        return visitor.visit_nullptr_literal(self)


# Identifier nodes
@dataclass
class CppIdentifier(CppExpression):
    """C++ identifier."""
    name: str
    
    def __post_init__(self):
        self.type = CppNodeType.IDENTIFIER
    
    def accept(self, visitor):
        return visitor.visit_identifier(self)


@dataclass
class CppQualifiedName(CppExpression):
    """C++ qualified name (e.g., std::vector)."""
    scope: Optional[CppExpression]  # Can be nested
    name: str
    
    def __post_init__(self):
        self.type = CppNodeType.QUALIFIED_NAME
    
    def accept(self, visitor):
        return visitor.visit_qualified_name(self)


# Expression nodes
@dataclass
class CppBinaryOp(CppExpression):
    """C++ binary operation."""
    left: CppExpression
    operator: CppOperator
    right: CppExpression
    
    def __post_init__(self):
        self.type = CppNodeType.BINARY_OP
    
    def accept(self, visitor):
        return visitor.visit_binary_op(self)


@dataclass
class CppUnaryOp(CppExpression):
    """C++ unary operation."""
    operator: CppOperator
    operand: CppExpression
    is_postfix: bool = False
    
    def __post_init__(self):
        self.type = CppNodeType.UNARY_OP
    
    def accept(self, visitor):
        return visitor.visit_unary_op(self)


@dataclass
class CppConditionalOp(CppExpression):
    """C++ ternary conditional operator."""
    condition: CppExpression
    true_expr: CppExpression
    false_expr: CppExpression
    
    def __post_init__(self):
        self.type = CppNodeType.CONDITIONAL
    
    def accept(self, visitor):
        return visitor.visit_conditional_op(self)


@dataclass
class CppAssignment(CppExpression):
    """C++ assignment expression."""
    left: CppExpression
    operator: CppOperator
    right: CppExpression
    
    def __post_init__(self):
        self.type = CppNodeType.ASSIGNMENT
    
    def accept(self, visitor):
        return visitor.visit_assignment(self)


@dataclass
class CppCall(CppExpression):
    """C++ function call."""
    function: CppExpression
    arguments: List[CppExpression]
    
    def __post_init__(self):
        self.type = CppNodeType.CALL
    
    def accept(self, visitor):
        return visitor.visit_call(self)


@dataclass
class CppMemberAccess(CppExpression):
    """C++ member access (. or ->)."""
    object: CppExpression
    member: str
    is_arrow: bool = False
    
    def __post_init__(self):
        self.type = CppNodeType.MEMBER_ACCESS
    
    def accept(self, visitor):
        return visitor.visit_member_access(self)


@dataclass
class CppArraySubscript(CppExpression):
    """C++ array subscript."""
    array: CppExpression
    index: CppExpression
    
    def __post_init__(self):
        self.type = CppNodeType.ARRAY_SUBSCRIPT
    
    def accept(self, visitor):
        return visitor.visit_array_subscript(self)


@dataclass
class CppCast(CppExpression):
    """C++ cast expression."""
    target_type: CppType
    operand: CppExpression
    cast_kind: str = "c_style"  # c_style, static, dynamic, const, reinterpret
    
    def __post_init__(self):
        self.type = CppNodeType.CAST
    
    def accept(self, visitor):
        return visitor.visit_cast(self)


@dataclass
class CppSizeofExpr(CppExpression):
    """C++ sizeof expression."""
    operand: Union[CppExpression, CppType]
    is_type: bool = False
    
    def __post_init__(self):
        self.type = CppNodeType.SIZEOF
    
    def accept(self, visitor):
        return visitor.visit_sizeof(self)


@dataclass
class CppNewExpr(CppExpression):
    """C++ new expression."""
    target_type: CppType
    placement_args: List[CppExpression] = field(default_factory=list)
    initializer: Optional[CppExpression] = None
    is_array: bool = False
    array_size: Optional[CppExpression] = None
    
    def __post_init__(self):
        self.type = CppNodeType.NEW
    
    def accept(self, visitor):
        return visitor.visit_new_expr(self)


@dataclass
class CppDeleteExpr(CppExpression):
    """C++ delete expression."""
    operand: CppExpression
    is_array: bool = False
    
    def __post_init__(self):
        self.type = CppNodeType.DELETE
    
    def accept(self, visitor):
        return visitor.visit_delete_expr(self)


@dataclass
class CppLambda(CppExpression):
    """C++ lambda expression (C++11)."""
    captures: List['CppLambdaCapture']
    parameters: Optional['CppParameterList'] = None
    return_type: Optional[CppType] = None
    body: 'CppStatement'
    is_mutable: bool = False
    exception_spec: Optional[str] = None
    
    def __post_init__(self):
        self.type = CppNodeType.LAMBDA
    
    def accept(self, visitor):
        return visitor.visit_lambda(self)


@dataclass
class CppLambdaCapture(CppNode):
    """C++ lambda capture."""
    name: Optional[str] = None
    is_by_reference: bool = False
    is_pack_expansion: bool = False
    is_this: bool = False
    init_expr: Optional[CppExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_lambda_capture(self)


@dataclass
class CppInitializerList(CppExpression):
    """C++ initializer list (C++11)."""
    elements: List[CppExpression]
    
    def __post_init__(self):
        self.type = CppNodeType.INITIALIZER_LIST
    
    def accept(self, visitor):
        return visitor.visit_initializer_list(self)


# Statement nodes
@dataclass
class CppExpressionStmt(CppStatement):
    """C++ expression statement."""
    expression: Optional[CppExpression]
    
    def __post_init__(self):
        self.type = CppNodeType.EXPRESSION_STMT
    
    def accept(self, visitor):
        return visitor.visit_expression_stmt(self)


@dataclass
class CppCompoundStmt(CppStatement):
    """C++ compound statement (block)."""
    statements: List[CppStatement]
    
    def __post_init__(self):
        self.type = CppNodeType.COMPOUND_STMT
    
    def accept(self, visitor):
        return visitor.visit_compound_stmt(self)


@dataclass
class CppIfStmt(CppStatement):
    """C++ if statement."""
    condition: CppExpression
    then_stmt: CppStatement
    else_stmt: Optional[CppStatement] = None
    init_stmt: Optional[CppStatement] = None  # C++17
    
    def __post_init__(self):
        self.type = CppNodeType.IF_STMT
    
    def accept(self, visitor):
        return visitor.visit_if_stmt(self)


@dataclass
class CppWhileStmt(CppStatement):
    """C++ while statement."""
    condition: CppExpression
    body: CppStatement
    
    def __post_init__(self):
        self.type = CppNodeType.WHILE_STMT
    
    def accept(self, visitor):
        return visitor.visit_while_stmt(self)


@dataclass
class CppForStmt(CppStatement):
    """C++ for statement."""
    init: Optional[CppStatement]
    condition: Optional[CppExpression]
    increment: Optional[CppExpression]
    body: CppStatement
    
    def __post_init__(self):
        self.type = CppNodeType.FOR_STMT
    
    def accept(self, visitor):
        return visitor.visit_for_stmt(self)


@dataclass
class CppRangeForStmt(CppStatement):
    """C++ range-based for statement (C++11)."""
    variable: 'CppVariableDecl'
    range: CppExpression
    body: CppStatement
    
    def __post_init__(self):
        self.type = CppNodeType.RANGE_FOR_STMT
    
    def accept(self, visitor):
        return visitor.visit_range_for_stmt(self)


@dataclass
class CppReturnStmt(CppStatement):
    """C++ return statement."""
    value: Optional[CppExpression] = None
    
    def __post_init__(self):
        self.type = CppNodeType.RETURN_STMT
    
    def accept(self, visitor):
        return visitor.visit_return_stmt(self)


@dataclass
class CppBreakStmt(CppStatement):
    """C++ break statement."""
    
    def __post_init__(self):
        self.type = CppNodeType.BREAK_STMT
    
    def accept(self, visitor):
        return visitor.visit_break_stmt(self)


@dataclass
class CppContinueStmt(CppStatement):
    """C++ continue statement."""
    
    def __post_init__(self):
        self.type = CppNodeType.CONTINUE_STMT
    
    def accept(self, visitor):
        return visitor.visit_continue_stmt(self)


# Declaration nodes
@dataclass
class CppVariableDecl(CppDeclaration):
    """C++ variable declaration."""
    name: str
    var_type: CppType
    initializer: Optional[CppExpression] = None
    storage_class: Optional[CppStorageClass] = None
    is_constexpr: bool = False
    is_consteval: bool = False  # C++20
    is_constinit: bool = False  # C++20
    
    def __post_init__(self):
        self.type = CppNodeType.VARIABLE_DECL
    
    def accept(self, visitor):
        return visitor.visit_variable_decl(self)


@dataclass
class CppFunctionDecl(CppDeclaration):
    """C++ function declaration."""
    name: str
    return_type: CppType
    parameters: 'CppParameterList'
    body: Optional[CppStatement] = None
    storage_class: Optional[CppStorageClass] = None
    is_virtual: bool = False
    is_override: bool = False  # C++11
    is_final: bool = False  # C++11
    is_pure_virtual: bool = False
    is_constexpr: bool = False
    is_consteval: bool = False  # C++20
    is_inline: bool = False
    is_explicit: bool = False
    is_friend: bool = False
    exception_spec: Optional[str] = None
    trailing_return_type: Optional[CppType] = None  # C++11
    
    def __post_init__(self):
        self.type = CppNodeType.FUNCTION_DECL
    
    def accept(self, visitor):
        return visitor.visit_function_decl(self)


@dataclass
class CppParameterList(CppNode):
    """C++ parameter list."""
    parameters: List['CppParameter']
    is_variadic: bool = False
    
    def accept(self, visitor):
        return visitor.visit_parameter_list(self)


@dataclass
class CppParameter(CppNode):
    """C++ function parameter."""
    name: Optional[str]
    param_type: CppType
    default_value: Optional[CppExpression] = None
    is_pack_expansion: bool = False
    
    def accept(self, visitor):
        return visitor.visit_parameter(self)


@dataclass
class CppClassDecl(CppDeclaration):
    """C++ class declaration."""
    name: str
    base_classes: List['CppBaseSpecifier'] = field(default_factory=list)
    members: List[CppDeclaration] = field(default_factory=list)
    template_params: Optional['CppTemplateParameterList'] = None
    is_struct: bool = False
    is_union: bool = False
    is_final: bool = False  # C++11
    
    def __post_init__(self):
        self.type = CppNodeType.CLASS_DECL
    
    def accept(self, visitor):
        return visitor.visit_class_decl(self)


@dataclass
class CppBaseSpecifier(CppNode):
    """C++ base class specifier."""
    base_type: CppType
    access: CppAccessSpecifier = CppAccessSpecifier.PUBLIC
    is_virtual: bool = False
    
    def accept(self, visitor):
        return visitor.visit_base_specifier(self)


@dataclass
class CppNamespaceDecl(CppDeclaration):
    """C++ namespace declaration."""
    name: Optional[str]  # None for anonymous namespace
    declarations: List[CppDeclaration]
    is_inline: bool = False  # C++11
    
    def __post_init__(self):
        self.type = CppNodeType.NAMESPACE_DECL
    
    def accept(self, visitor):
        return visitor.visit_namespace_decl(self)


@dataclass
class CppTemplateDecl(CppDeclaration):
    """C++ template declaration."""
    template_params: 'CppTemplateParameterList'
    declaration: CppDeclaration
    
    def __post_init__(self):
        self.type = CppNodeType.TEMPLATE_DECL
    
    def accept(self, visitor):
        return visitor.visit_template_decl(self)


@dataclass
class CppTemplateParameterList(CppNode):
    """C++ template parameter list."""
    parameters: List['CppTemplateParameter']
    
    def accept(self, visitor):
        return visitor.visit_template_parameter_list(self)


@dataclass
class CppTemplateParameter(CppNode):
    """C++ template parameter."""
    name: Optional[str]
    kind: str  # "type", "non_type", "template"
    default_value: Optional[Union[CppType, CppExpression]] = None
    is_pack: bool = False
    
    def __post_init__(self):
        self.type = CppNodeType.TEMPLATE_PARAMETER
    
    def accept(self, visitor):
        return visitor.visit_template_parameter(self)


# Type nodes
@dataclass
class CppBuiltinType(CppType):
    """C++ builtin type."""
    name: str  # int, char, float, double, void, etc.
    
    def __post_init__(self):
        self.type = CppNodeType.BUILTIN_TYPE
    
    def accept(self, visitor):
        return visitor.visit_builtin_type(self)


@dataclass
class CppPointerType(CppType):
    """C++ pointer type."""
    pointee_type: CppType
    
    def __post_init__(self):
        self.type = CppNodeType.POINTER_TYPE
    
    def accept(self, visitor):
        return visitor.visit_pointer_type(self)


@dataclass
class CppReferenceType(CppType):
    """C++ reference type."""
    referenced_type: CppType
    is_rvalue_reference: bool = False  # C++11
    
    def __post_init__(self):
        self.type = CppNodeType.REFERENCE_TYPE
    
    def accept(self, visitor):
        return visitor.visit_reference_type(self)


@dataclass
class CppArrayType(CppType):
    """C++ array type."""
    element_type: CppType
    size: Optional[CppExpression] = None
    
    def __post_init__(self):
        self.type = CppNodeType.ARRAY_TYPE
    
    def accept(self, visitor):
        return visitor.visit_array_type(self)


@dataclass
class CppFunctionType(CppType):
    """C++ function type."""
    return_type: CppType
    parameter_types: List[CppType]
    is_variadic: bool = False
    
    def __post_init__(self):
        self.type = CppNodeType.FUNCTION_TYPE
    
    def accept(self, visitor):
        return visitor.visit_function_type(self)


@dataclass
class CppAutoType(CppType):
    """C++ auto type (C++11)."""
    
    def __post_init__(self):
        self.type = CppNodeType.AUTO_TYPE
    
    def accept(self, visitor):
        return visitor.visit_auto_type(self)


@dataclass
class CppDecltypeType(CppType):
    """C++ decltype type (C++11)."""
    expression: CppExpression
    
    def __post_init__(self):
        self.type = CppNodeType.DECLTYPE_TYPE
    
    def accept(self, visitor):
        return visitor.visit_decltype_type(self)


# Translation unit
@dataclass
class CppTranslationUnit(CppNode):
    """C++ translation unit (source file)."""
    declarations: List[CppDeclaration]
    
    def __post_init__(self):
        self.type = CppNodeType.TRANSLATION_UNIT
    
    def accept(self, visitor):
        return visitor.visit_translation_unit(self)


class CppNodeVisitor(ABC):
    """Abstract base class for C++ AST visitors."""
    
    @abstractmethod
    def visit_integer_literal(self, node: CppIntegerLiteral): pass
    
    @abstractmethod
    def visit_floating_literal(self, node: CppFloatingLiteral): pass
    
    @abstractmethod
    def visit_string_literal(self, node: CppStringLiteral): pass
    
    @abstractmethod
    def visit_character_literal(self, node: CppCharacterLiteral): pass
    
    @abstractmethod
    def visit_boolean_literal(self, node: CppBooleanLiteral): pass
    
    @abstractmethod
    def visit_nullptr_literal(self, node: CppNullptrLiteral): pass
    
    @abstractmethod
    def visit_identifier(self, node: CppIdentifier): pass
    
    @abstractmethod
    def visit_qualified_name(self, node: CppQualifiedName): pass
    
    @abstractmethod
    def visit_binary_op(self, node: CppBinaryOp): pass
    
    @abstractmethod
    def visit_unary_op(self, node: CppUnaryOp): pass
    
    @abstractmethod
    def visit_conditional_op(self, node: CppConditionalOp): pass
    
    @abstractmethod
    def visit_assignment(self, node: CppAssignment): pass
    
    @abstractmethod
    def visit_call(self, node: CppCall): pass
    
    @abstractmethod
    def visit_member_access(self, node: CppMemberAccess): pass
    
    @abstractmethod
    def visit_array_subscript(self, node: CppArraySubscript): pass
    
    @abstractmethod
    def visit_cast(self, node: CppCast): pass
    
    @abstractmethod
    def visit_sizeof(self, node: CppSizeofExpr): pass
    
    @abstractmethod
    def visit_new_expr(self, node: CppNewExpr): pass
    
    @abstractmethod
    def visit_delete_expr(self, node: CppDeleteExpr): pass
    
    @abstractmethod
    def visit_lambda(self, node: CppLambda): pass
    
    @abstractmethod
    def visit_lambda_capture(self, node: CppLambdaCapture): pass
    
    @abstractmethod
    def visit_initializer_list(self, node: CppInitializerList): pass
    
    @abstractmethod
    def visit_expression_stmt(self, node: CppExpressionStmt): pass
    
    @abstractmethod
    def visit_compound_stmt(self, node: CppCompoundStmt): pass
    
    @abstractmethod
    def visit_if_stmt(self, node: CppIfStmt): pass
    
    @abstractmethod
    def visit_while_stmt(self, node: CppWhileStmt): pass
    
    @abstractmethod
    def visit_for_stmt(self, node: CppForStmt): pass
    
    @abstractmethod
    def visit_range_for_stmt(self, node: CppRangeForStmt): pass
    
    @abstractmethod
    def visit_return_stmt(self, node: CppReturnStmt): pass
    
    @abstractmethod
    def visit_break_stmt(self, node: CppBreakStmt): pass
    
    @abstractmethod
    def visit_continue_stmt(self, node: CppContinueStmt): pass
    
    @abstractmethod
    def visit_variable_decl(self, node: CppVariableDecl): pass
    
    @abstractmethod
    def visit_function_decl(self, node: CppFunctionDecl): pass
    
    @abstractmethod
    def visit_parameter_list(self, node: CppParameterList): pass
    
    @abstractmethod
    def visit_parameter(self, node: CppParameter): pass
    
    @abstractmethod
    def visit_class_decl(self, node: CppClassDecl): pass
    
    @abstractmethod
    def visit_base_specifier(self, node: CppBaseSpecifier): pass
    
    @abstractmethod
    def visit_namespace_decl(self, node: CppNamespaceDecl): pass
    
    @abstractmethod
    def visit_template_decl(self, node: CppTemplateDecl): pass
    
    @abstractmethod
    def visit_template_parameter_list(self, node: CppTemplateParameterList): pass
    
    @abstractmethod
    def visit_template_parameter(self, node: CppTemplateParameter): pass
    
    @abstractmethod
    def visit_builtin_type(self, node: CppBuiltinType): pass
    
    @abstractmethod
    def visit_pointer_type(self, node: CppPointerType): pass
    
    @abstractmethod
    def visit_reference_type(self, node: CppReferenceType): pass
    
    @abstractmethod
    def visit_array_type(self, node: CppArrayType): pass
    
    @abstractmethod
    def visit_function_type(self, node: CppFunctionType): pass
    
    @abstractmethod
    def visit_auto_type(self, node: CppAutoType): pass
    
    @abstractmethod
    def visit_decltype_type(self, node: CppDecltypeType): pass
    
    @abstractmethod
    def visit_translation_unit(self, node: CppTranslationUnit): pass