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
    
    # Modern C++ constructs (C++17-C++23)
    STRUCTURED_BINDING_DECL = auto()  # C++17
    IF_INIT_STMT = auto()  # C++17
    SWITCH_INIT_STMT = auto()  # C++17
    CONSTEXPR_IF_STMT = auto()  # C++17
    
    # Coroutines (C++20)
    CO_AWAIT_EXPR = auto()
    CO_YIELD_EXPR = auto()
    CO_RETURN_STMT = auto()
    
    # Concepts (C++20)
    CONCEPT_DECL = auto()
    REQUIRES_CLAUSE = auto()
    CONSTRAINT_EXPR = auto()
    
    # Modules (C++20)
    MODULE_DECL = auto()
    MODULE_IMPORT_DECL = auto()
    EXPORT_DECL = auto()
    
    # Additional missing constructs
    PACK_EXPANSION_EXPR = auto()
    FOLD_EXPR = auto()  # C++17
    NOEXCEPT_EXPR = auto()
    ALIGNOF_EXPR = auto()
    TYPEID_EXPR = auto()
    DECLTYPE_EXPR = auto()
    
    # Template specializations
    TEMPLATE_SPECIALIZATION_DECL = auto()
    PARTIAL_SPECIALIZATION_DECL = auto()
    
    # More complete type system
    PLACEHOLDER_TYPE = auto()  # auto, decltype(auto)
    DEDUCED_TYPE = auto()
    DEPENDENT_TYPE = auto()
    TYPENAME_TYPE = auto()
    
    # Additional statements
    ASM_STMT = auto()
    PRAGMA_STMT = auto()
    ATTRIBUTE_STMT = auto()
    
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
    
    # Module constructs (C++20) - using definitions from line 94-96
    # MODULE_DECL = auto()  # Already defined above
    IMPORT_DECL = auto()
    # EXPORT_DECL = auto()  # Already defined above
    
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
    value: Any = None
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
    name: str = ""
    
    def __post_init__(self):
        self.type = CppNodeType.IDENTIFIER
    
    def accept(self, visitor):
        return visitor.visit_identifier(self)


@dataclass
class CppQualifiedName(CppExpression):
    """C++ qualified name (e.g., std::vector)."""
    scope: Optional[CppExpression] = None  # Can be nested
    name: str = ""
    
    def __post_init__(self):
        self.type = CppNodeType.QUALIFIED_NAME
    
    def accept(self, visitor):
        return visitor.visit_qualified_name(self)


# Expression nodes
@dataclass
class CppBinaryOp(CppExpression):
    """C++ binary operation."""
    left: Optional[CppExpression] = None
    operator: Optional[CppOperator] = None
    right: Optional[CppExpression] = None
    
    def __post_init__(self):
        self.type = CppNodeType.BINARY_OP
    
    def accept(self, visitor):
        return visitor.visit_binary_op(self)


@dataclass
class CppUnaryOp(CppExpression):
    """C++ unary operation."""
    operator: Optional[CppOperator] = None
    operand: Optional[CppExpression] = None
    is_postfix: bool = False
    
    def __post_init__(self):
        self.type = CppNodeType.UNARY_OP
    
    def accept(self, visitor):
        return visitor.visit_unary_op(self)


@dataclass
class CppConditionalOp(CppExpression):
    """C++ ternary conditional operator."""
    condition: Optional[CppExpression] = None
    true_expr: Optional[CppExpression] = None
    false_expr: Optional[CppExpression] = None
    
    def __post_init__(self):
        self.type = CppNodeType.CONDITIONAL
    
    def accept(self, visitor):
        return visitor.visit_conditional_op(self)


@dataclass
class CppAssignment(CppExpression):
    """C++ assignment expression."""
    left: Optional[CppExpression] = None
    operator: Optional[CppOperator] = None
    right: Optional[CppExpression] = None
    
    def __post_init__(self):
        self.type = CppNodeType.ASSIGNMENT
    
    def accept(self, visitor):
        return visitor.visit_assignment(self)


@dataclass
class CppCall(CppExpression):
    """C++ function call."""
    function: Optional[CppExpression] = None
    arguments: List[CppExpression] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = CppNodeType.CALL
    
    def accept(self, visitor):
        return visitor.visit_call(self)


@dataclass
class CppMemberAccess(CppExpression):
    """C++ member access (. or ->)."""
    object: Optional[CppExpression] = None
    member: str = ""
    is_arrow: bool = False
    
    def __post_init__(self):
        self.type = CppNodeType.MEMBER_ACCESS
    
    def accept(self, visitor):
        return visitor.visit_member_access(self)


@dataclass
class CppArraySubscript(CppExpression):
    """C++ array subscript."""
    array: Optional[CppExpression] = None
    index: Optional[CppExpression] = None
    
    def __post_init__(self):
        self.type = CppNodeType.ARRAY_SUBSCRIPT
    
    def accept(self, visitor):
        return visitor.visit_array_subscript(self)


@dataclass
class CppCast(CppExpression):
    """C++ cast expression."""
    target_type: Optional[CppType] = None
    operand: Optional[CppExpression] = None
    cast_kind: str = "c_style"  # c_style, static, dynamic, const, reinterpret
    
    def __post_init__(self):
        self.type = CppNodeType.CAST
    
    def accept(self, visitor):
        return visitor.visit_cast(self)


@dataclass
class CppSizeofExpr(CppExpression):
    """C++ sizeof expression."""
    operand: Union[CppExpression, CppType] = None
    is_type: bool = False
    
    def __post_init__(self):
        self.type = CppNodeType.SIZEOF
    
    def accept(self, visitor):
        return visitor.visit_sizeof(self)


@dataclass
class CppNewExpr(CppExpression):
    """C++ new expression."""
    target_type: Optional[CppType] = None
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
    operand: Optional[CppExpression] = None
    is_array: bool = False
    
    def __post_init__(self):
        self.type = CppNodeType.DELETE
    
    def accept(self, visitor):
        return visitor.visit_delete_expr(self)


@dataclass
class CppLambda(CppExpression):
    """C++ lambda expression (C++11)."""
    captures: List['CppLambdaCapture'] = field(default_factory=list)
    parameters: Optional['CppParameterList'] = None
    return_type: Optional[CppType] = None
    body: Optional['CppStatement'] = None
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
    elements: List[CppExpression] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = CppNodeType.INITIALIZER_LIST
    
    def accept(self, visitor):
        return visitor.visit_initializer_list(self)


# Statement nodes
@dataclass
class CppExpressionStmt(CppStatement):
    """C++ expression statement."""
    expression: Optional[CppExpression] = None
    
    def __post_init__(self):
        self.type = CppNodeType.EXPRESSION_STMT
    
    def accept(self, visitor):
        return visitor.visit_expression_stmt(self)


@dataclass
class CppCompoundStmt(CppStatement):
    """C++ compound statement (block)."""
    statements: List[CppStatement] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = CppNodeType.COMPOUND_STMT
    
    def accept(self, visitor):
        return visitor.visit_compound_stmt(self)


@dataclass
class CppIfStmt(CppStatement):
    """C++ if statement."""
    condition: Optional[CppExpression] = None
    then_stmt: Optional[CppStatement] = None
    else_stmt: Optional[CppStatement] = None
    init_stmt: Optional[CppStatement] = None  # C++17
    
    def __post_init__(self):
        self.type = CppNodeType.IF_STMT
    
    def accept(self, visitor):
        return visitor.visit_if_stmt(self)


@dataclass
class CppWhileStmt(CppStatement):
    """C++ while statement."""
    condition: Optional[CppExpression] = None
    body: Optional[CppStatement] = None
    
    def __post_init__(self):
        self.type = CppNodeType.WHILE_STMT
    
    def accept(self, visitor):
        return visitor.visit_while_stmt(self)


@dataclass
class CppForStmt(CppStatement):
    """C++ for statement."""
    init: Optional[CppStatement] = None
    condition: Optional[CppExpression] = None
    increment: Optional[CppExpression] = None
    body: Optional[CppStatement] = None
    
    def __post_init__(self):
        self.type = CppNodeType.FOR_STMT
    
    def accept(self, visitor):
        return visitor.visit_for_stmt(self)


@dataclass
class CppRangeForStmt(CppStatement):
    """C++ range-based for statement (C++11)."""
    variable: Optional['CppVariableDecl'] = None
    range: Optional[CppExpression] = None
    body: Optional[CppStatement] = None
    
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
    name: str = ""
    var_type: Optional[CppType] = None
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
    name: str = ""
    return_type: Optional[CppType] = None
    parameters: Optional['CppParameterList'] = None
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
    parameters: List['CppParameter'] = field(default_factory=list)
    is_variadic: bool = False
    
    def accept(self, visitor):
        return visitor.visit_parameter_list(self)


@dataclass
class CppParameter(CppNode):
    """C++ function parameter."""
    name: Optional[str] = None
    param_type: Optional[CppType] = None
    default_value: Optional[CppExpression] = None
    is_pack_expansion: bool = False
    
    def accept(self, visitor):
        return visitor.visit_parameter(self)


@dataclass
class CppClassDecl(CppDeclaration):
    """C++ class declaration."""
    name: str = ""
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
    base_type: Optional[CppType] = None
    access: CppAccessSpecifier = CppAccessSpecifier.PUBLIC
    is_virtual: bool = False
    
    def accept(self, visitor):
        return visitor.visit_base_specifier(self)


@dataclass
class CppNamespaceDecl(CppDeclaration):
    """C++ namespace declaration."""
    name: Optional[str] = None  # None for anonymous namespace
    declarations: List[CppDeclaration] = field(default_factory=list)
    is_inline: bool = False  # C++11
    
    def __post_init__(self):
        self.type = CppNodeType.NAMESPACE_DECL
    
    def accept(self, visitor):
        return visitor.visit_namespace_decl(self)


@dataclass
class CppTemplateDecl(CppDeclaration):
    """C++ template declaration."""
    template_params: Optional['CppTemplateParameterList'] = None
    declaration: Optional[CppDeclaration] = None
    
    def __post_init__(self):
        self.type = CppNodeType.TEMPLATE_DECL
    
    def accept(self, visitor):
        return visitor.visit_template_decl(self)


@dataclass
class CppTemplateParameterList(CppNode):
    """C++ template parameter list."""
    parameters: List['CppTemplateParameter'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_template_parameter_list(self)


@dataclass
class CppTemplateParameter(CppNode):
    """C++ template parameter."""
    name: Optional[str] = None
    kind: str = ""  # "type", "non_type", "template"
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
    name: str = ""  # int, char, float, double, void, etc.
    
    def __post_init__(self):
        self.type = CppNodeType.BUILTIN_TYPE
    
    def accept(self, visitor):
        return visitor.visit_builtin_type(self)


@dataclass
class CppPointerType(CppType):
    """C++ pointer type."""
    pointee_type: Optional[CppType] = None
    
    def __post_init__(self):
        self.type = CppNodeType.POINTER_TYPE
    
    def accept(self, visitor):
        return visitor.visit_pointer_type(self)


@dataclass
class CppReferenceType(CppType):
    """C++ reference type."""
    referenced_type: Optional[CppType] = None
    is_rvalue_reference: bool = False  # C++11
    
    def __post_init__(self):
        self.type = CppNodeType.REFERENCE_TYPE
    
    def accept(self, visitor):
        return visitor.visit_reference_type(self)


@dataclass
class CppArrayType(CppType):
    """C++ array type."""
    element_type: Optional[CppType] = None
    size: Optional[CppExpression] = None
    
    def __post_init__(self):
        self.type = CppNodeType.ARRAY_TYPE
    
    def accept(self, visitor):
        return visitor.visit_array_type(self)


@dataclass
class CppFunctionType(CppType):
    """C++ function type."""
    return_type: Optional[CppType] = None
    parameter_types: List[CppType] = field(default_factory=list)
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
    expression: Optional[CppExpression] = None
    
    def __post_init__(self):
        self.type = CppNodeType.DECLTYPE_TYPE
    
    def accept(self, visitor):
        return visitor.visit_decltype_type(self)


# Translation unit
@dataclass
class CppTranslationUnit(CppNode):
    """C++ translation unit (source file)."""
    declarations: List[CppDeclaration] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = CppNodeType.TRANSLATION_UNIT
    
    def accept(self, visitor):
        return visitor.visit_translation_unit(self)


# Additional statement and declaration nodes needed by parser
@dataclass
class CppDoWhileStmt(CppStatement):
    """C++ do-while statement."""
    body: Optional[CppStatement] = None
    condition: Optional[CppExpression] = None
    
    def __post_init__(self):
        self.type = CppNodeType.DO_WHILE_STMT
    
    def accept(self, visitor):
        return visitor.visit_do_while_stmt(self)


@dataclass
class CppSwitchStmt(CppStatement):
    """C++ switch statement."""
    condition: Optional[CppExpression] = None
    body: Optional[CppStatement] = None
    
    def __post_init__(self):
        self.type = CppNodeType.SWITCH_STMT
    
    def accept(self, visitor):
        return visitor.visit_switch_stmt(self)


@dataclass
class CppCaseStmt(CppStatement):
    """C++ case statement."""
    value: Optional[CppExpression] = None
    statement: Optional[CppStatement] = None
    
    def accept(self, visitor):
        return visitor.visit_case_stmt(self)


@dataclass
class CppDefaultStmt(CppStatement):
    """C++ default statement."""
    statement: Optional[CppStatement] = None
    
    def accept(self, visitor):
        return visitor.visit_default_stmt(self)


@dataclass
class CppGotoStmt(CppStatement):
    """C++ goto statement."""
    label: str = ""
    
    def __post_init__(self):
        self.type = CppNodeType.GOTO_STMT
    
    def accept(self, visitor):
        return visitor.visit_goto_stmt(self)


@dataclass
class CppEmptyStmt(CppStatement):
    """C++ empty statement."""
    
    def accept(self, visitor):
        return visitor.visit_empty_stmt(self)


@dataclass
class CppDeclarationStmt(CppStatement):
    """C++ declaration statement."""
    declaration: Optional[CppDeclaration] = None
    
    def __post_init__(self):
        self.type = CppNodeType.DECLARATION_STMT
    
    def accept(self, visitor):
        return visitor.visit_declaration_stmt(self)


@dataclass
class CppThrowStmt(CppStatement):
    """C++ throw statement."""
    expression: Optional[CppExpression] = None
    
    def __post_init__(self):
        self.type = CppNodeType.THROW_STMT
    
    def accept(self, visitor):
        return visitor.visit_throw_stmt(self)


@dataclass
class CppTryStmt(CppStatement):
    """C++ try statement."""
    body: Optional[CppStatement] = None
    catch_blocks: List['CppCatchBlock'] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = CppNodeType.TRY_STMT
    
    def accept(self, visitor):
        return visitor.visit_try_stmt(self)


@dataclass
class CppCatchBlock(CppNode):
    """C++ catch block."""
    exception_type: Optional[CppType] = None
    exception_name: Optional[str] = None
    body: Optional[CppStatement] = None
    
    def accept(self, visitor):
        return visitor.visit_catch_block(self)


@dataclass
class CppEnumDecl(CppDeclaration):
    """C++ enum declaration."""
    name: str = ""
    enumerators: List['CppEnumerator'] = field(default_factory=list)
    underlying_type: Optional[CppType] = None
    is_scoped: bool = False  # enum class
    
    def __post_init__(self):
        self.type = CppNodeType.ENUM_DECL
    
    def accept(self, visitor):
        return visitor.visit_enum_decl(self)


@dataclass
class CppEnumerator(CppNode):
    """C++ enumerator."""
    name: str = ""
    value: Optional[CppExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_enumerator(self)


@dataclass
class CppTypedefDecl(CppDeclaration):
    """C++ typedef declaration."""
    name: str = ""
    aliased_type: Optional[CppType] = None
    
    def __post_init__(self):
        self.type = CppNodeType.TYPEDEF_DECL
    
    def accept(self, visitor):
        return visitor.visit_typedef_decl(self)


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


# ============================================================================
# Modern C++ Constructs (C++17-C++23) - Production Ready Extensions
# ============================================================================

@dataclass
class CppStructuredBinding(CppDeclaration):
    """C++ structured binding declaration (C++17)."""
    identifiers: List[str] = field(default_factory=list)
    initializer: Optional[CppExpression] = None
    cv_qualifiers: List[CppTypeQualifier] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = CppNodeType.STRUCTURED_BINDING_DECL
    
    def accept(self, visitor):
        return visitor.visit_structured_binding(self)


@dataclass
class CppIfInitStatement(CppStatement):
    """C++ if statement with init (C++17)."""
    init_stmt: Optional[CppStatement] = None
    condition: Optional[CppExpression] = None
    then_stmt: Optional[CppStatement] = None
    else_stmt: Optional[CppStatement] = None
    is_constexpr: bool = False  # constexpr if (C++17)
    
    def __post_init__(self):
        self.type = CppNodeType.IF_INIT_STMT
    
    def accept(self, visitor):
        return visitor.visit_if_init_stmt(self)


@dataclass
class CppCoAwaitExpr(CppExpression):
    """C++ co_await expression (C++20)."""
    operand: Optional[CppExpression] = None
    
    def __post_init__(self):
        self.type = CppNodeType.CO_AWAIT_EXPR
    
    def accept(self, visitor):
        return visitor.visit_co_await_expr(self)


@dataclass
class CppCoYieldExpr(CppExpression):
    """C++ co_yield expression (C++20)."""
    operand: Optional[CppExpression] = None
    
    def __post_init__(self):
        self.type = CppNodeType.CO_YIELD_EXPR
    
    def accept(self, visitor):
        return visitor.visit_co_yield_expr(self)


@dataclass
class CppCoReturnStmt(CppStatement):
    """C++ co_return statement (C++20)."""
    value: Optional[CppExpression] = None
    
    def __post_init__(self):
        self.type = CppNodeType.CO_RETURN_STMT
    
    def accept(self, visitor):
        return visitor.visit_co_return_stmt(self)


@dataclass
class CppConceptDecl(CppDeclaration):
    """C++ concept declaration (C++20)."""
    name: str = ""
    template_params: Optional[CppTemplateParameterList] = None
    constraint: Optional[CppExpression] = None
    
    def __post_init__(self):
        self.type = CppNodeType.CONCEPT_DECL
    
    def accept(self, visitor):
        return visitor.visit_concept_decl(self)


@dataclass
class CppRequiresClause(CppExpression):
    """C++ requires clause (C++20)."""
    constraint: Optional[CppExpression] = None
    
    def __post_init__(self):
        self.type = CppNodeType.REQUIRES_CLAUSE
    
    def accept(self, visitor):
        return visitor.visit_requires_clause(self)


@dataclass
class CppRequiresExpr(CppExpression):
    """C++ requires expression (C++20)."""
    parameters: Optional[CppParameterList] = None
    requirements: List[CppExpression] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = CppNodeType.CONSTRAINT_EXPR
    
    def accept(self, visitor):
        return visitor.visit_requires_expr(self)


@dataclass
class CppModuleDecl(CppDeclaration):
    """C++ module declaration (C++20)."""
    name: str = ""
    partition_name: Optional[str] = None
    is_interface: bool = True
    
    def __post_init__(self):
        self.type = CppNodeType.MODULE_DECL
    
    def accept(self, visitor):
        return visitor.visit_module_decl(self)


@dataclass
class CppModuleImportDecl(CppDeclaration):
    """C++ import declaration (C++20)."""
    module_name: str = ""
    partition_name: Optional[str] = None
    is_header_unit: bool = False
    
    def __post_init__(self):
        self.type = CppNodeType.MODULE_IMPORT_DECL
    
    def accept(self, visitor):
        return visitor.visit_module_import_decl(self)


@dataclass
class CppExportDecl(CppDeclaration):
    """C++ export declaration (C++20)."""
    declaration: Optional[CppDeclaration] = None
    is_module: bool = False
    module_name: Optional[str] = None
    
    def __post_init__(self):
        self.type = CppNodeType.EXPORT_DECL
    
    def accept(self, visitor):
        return visitor.visit_export_decl(self)


@dataclass
class CppFoldExpr(CppExpression):
    """C++ fold expression (C++17)."""
    pattern: Optional[CppExpression] = None
    operator: Optional[CppOperator] = None
    is_left_fold: bool = True
    init_expr: Optional[CppExpression] = None
    
    def __post_init__(self):
        self.type = CppNodeType.FOLD_EXPR
    
    def accept(self, visitor):
        return visitor.visit_fold_expr(self)


@dataclass
class CppPackExpansion(CppExpression):
    """C++ pack expansion expression."""
    pattern: Optional[CppExpression] = None
    
    def __post_init__(self):
        self.type = CppNodeType.PACK_EXPANSION_EXPR
    
    def accept(self, visitor):
        return visitor.visit_pack_expansion(self)


@dataclass
class CppNoexceptExpr(CppExpression):
    """C++ noexcept expression."""
    operand: Optional[CppExpression] = None
    
    def __post_init__(self):
        self.type = CppNodeType.NOEXCEPT_EXPR
    
    def accept(self, visitor):
        return visitor.visit_noexcept_expr(self)


@dataclass
class CppAlignofExpr(CppExpression):
    """C++ alignof expression."""
    operand: Union[CppExpression, CppType] = None
    is_type: bool = False
    
    def __post_init__(self):
        self.type = CppNodeType.ALIGNOF_EXPR
    
    def accept(self, visitor):
        return visitor.visit_alignof_expr(self)


@dataclass
class CppTypeidExpr(CppExpression):
    """C++ typeid expression."""
    operand: Union[CppExpression, CppType] = None
    is_type: bool = False
    
    def __post_init__(self):
        self.type = CppNodeType.TYPEID_EXPR
    
    def accept(self, visitor):
        return visitor.visit_typeid_expr(self)


@dataclass
class CppDecltypeExpr(CppExpression):
    """C++ decltype expression."""
    operand: Optional[CppExpression] = None
    is_decltype_auto: bool = False
    
    def __post_init__(self):
        self.type = CppNodeType.DECLTYPE_EXPR
    
    def accept(self, visitor):
        return visitor.visit_decltype_expr(self)


@dataclass
class CppTemplateSpecialization(CppDeclaration):
    """C++ template specialization."""
    template_decl: Optional[CppTemplateDecl] = None
    specialization_args: List[Union[CppType, CppExpression]] = field(default_factory=list)
    declaration: Optional[CppDeclaration] = None
    is_partial: bool = False
    
    def __post_init__(self):
        self.type = CppNodeType.TEMPLATE_SPECIALIZATION_DECL
    
    def accept(self, visitor):
        return visitor.visit_template_specialization(self)


@dataclass
class CppDesignatedInitializer(CppExpression):
    """C++ designated initializer (C++20)."""
    designators: List[Union[str, CppExpression]] = field(default_factory=list)  # field names or array indices
    value: Optional[CppExpression] = None
    
    def __post_init__(self):
        self.type = CppNodeType.DESIGNATED_INITIALIZER
    
    def accept(self, visitor):
        return visitor.visit_designated_initializer(self)


@dataclass
class CppAsmStmt(CppStatement):
    """C++ inline assembly statement."""
    assembly_code: str = ""
    outputs: List[str] = field(default_factory=list)
    inputs: List[str] = field(default_factory=list)
    clobbers: List[str] = field(default_factory=list)
    is_volatile: bool = False
    
    def __post_init__(self):
        self.type = CppNodeType.ASM_STMT
    
    def accept(self, visitor):
        return visitor.visit_asm_stmt(self)


@dataclass
class CppAttribute(CppNode):
    """C++ attribute (C++11)."""
    namespace: Optional[str] = None
    name: str = ""
    arguments: List[CppExpression] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_attribute(self)


@dataclass
class CppStaticAssertDecl(CppDeclaration):
    """C++ static_assert declaration."""
    condition: Optional[CppExpression] = None
    message: Optional[CppExpression] = None
    
    def __post_init__(self):
        self.type = CppNodeType.STATIC_ASSERT_DECL
    
    def accept(self, visitor):
        return visitor.visit_static_assert_decl(self)


# Helper functions for creating common C++ constructs
def create_cpp_identifier(name: str) -> CppIdentifier:
    """Create a C++ identifier."""
    return CppIdentifier(name=name)


def create_cpp_binary_op(left: CppExpression, operator: CppOperator, right: CppExpression) -> CppBinaryOp:
    """Create a C++ binary operation."""
    return CppBinaryOp(left=left, operator=operator, right=right)


def create_cpp_function_decl(name: str, return_type: CppType = None, 
                            parameters: CppParameterList = None) -> CppFunctionDecl:
    """Create a C++ function declaration."""
    return CppFunctionDecl(
        name=name,
        return_type=return_type or CppBuiltinType(name="void"),
        parameters=parameters or CppParameterList()
    )


def create_cpp_class_decl(name: str, base_classes: List[CppBaseSpecifier] = None) -> CppClassDecl:
    """Create a C++ class declaration."""
    return CppClassDecl(
        name=name,
        base_classes=base_classes or []
    )