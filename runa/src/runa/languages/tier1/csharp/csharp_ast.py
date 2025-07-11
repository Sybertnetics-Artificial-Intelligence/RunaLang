#!/usr/bin/env python3
"""
C# AST Node Definitions

Comprehensive Abstract Syntax Tree nodes for C# covering
all language features from C# 1.0 through C# 12.0 including
generics, LINQ, async/await, nullable reference types, and modern C# constructs.
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod


class CSharpNodeType(Enum):
    """C# AST node types."""
    # Literals
    LITERAL = auto()
    INTEGER_LITERAL = auto()
    FLOATING_LITERAL = auto()
    STRING_LITERAL = auto()
    CHARACTER_LITERAL = auto()
    BOOLEAN_LITERAL = auto()
    NULL_LITERAL = auto()
    VERBATIM_STRING = auto()
    INTERPOLATED_STRING = auto()  # C# 6.0
    RAW_STRING = auto()  # C# 11.0
    
    # Identifiers and names
    IDENTIFIER = auto()
    QUALIFIED_NAME = auto()
    SIMPLE_NAME = auto()
    GENERIC_NAME = auto()
    ALIAS_QUALIFIED_NAME = auto()
    
    # Expressions
    BINARY_EXPRESSION = auto()
    UNARY_EXPRESSION = auto()
    CONDITIONAL_EXPRESSION = auto()
    ASSIGNMENT_EXPRESSION = auto()
    COMPOUND_ASSIGNMENT_EXPRESSION = auto()
    INVOCATION_EXPRESSION = auto()
    MEMBER_ACCESS_EXPRESSION = auto()
    ELEMENT_ACCESS_EXPRESSION = auto()
    CAST_EXPRESSION = auto()
    IS_EXPRESSION = auto()
    AS_EXPRESSION = auto()
    THIS_EXPRESSION = auto()
    BASE_EXPRESSION = auto()
    TYPEOF_EXPRESSION = auto()
    SIZEOF_EXPRESSION = auto()
    NAMEOF_EXPRESSION = auto()  # C# 6.0
    DEFAULT_EXPRESSION = auto()
    OBJECT_CREATION_EXPRESSION = auto()
    ARRAY_CREATION_EXPRESSION = auto()
    IMPLICIT_ARRAY_CREATION_EXPRESSION = auto()
    ANONYMOUS_OBJECT_CREATION_EXPRESSION = auto()
    LAMBDA_EXPRESSION = auto()  # C# 3.0
    ANONYMOUS_METHOD_EXPRESSION = auto()  # C# 2.0
    QUERY_EXPRESSION = auto()  # C# 3.0 (LINQ)
    AWAIT_EXPRESSION = auto()  # C# 5.0
    TUPLE_EXPRESSION = auto()  # C# 7.0
    THROW_EXPRESSION = auto()  # C# 7.0
    RANGE_EXPRESSION = auto()  # C# 8.0
    INDEX_EXPRESSION = auto()  # C# 8.0
    SWITCH_EXPRESSION = auto()  # C# 8.0
    WITH_EXPRESSION = auto()  # C# 9.0
    PATTERN_EXPRESSION = auto()  # C# 7.0+
    
    # Statements
    EXPRESSION_STATEMENT = auto()
    BLOCK_STATEMENT = auto()
    IF_STATEMENT = auto()
    WHILE_STATEMENT = auto()
    FOR_STATEMENT = auto()
    FOREACH_STATEMENT = auto()
    DO_STATEMENT = auto()
    SWITCH_STATEMENT = auto()
    BREAK_STATEMENT = auto()
    CONTINUE_STATEMENT = auto()
    RETURN_STATEMENT = auto()
    THROW_STATEMENT = auto()
    TRY_STATEMENT = auto()
    LOCK_STATEMENT = auto()
    USING_STATEMENT = auto()
    YIELD_STATEMENT = auto()  # C# 2.0
    EMPTY_STATEMENT = auto()
    LABELED_STATEMENT = auto()
    GOTO_STATEMENT = auto()
    CHECKED_STATEMENT = auto()
    UNCHECKED_STATEMENT = auto()
    UNSAFE_STATEMENT = auto()
    FIXED_STATEMENT = auto()
    LOCAL_DECLARATION_STATEMENT = auto()
    
    # Declarations
    COMPILATION_UNIT = auto()
    NAMESPACE_DECLARATION = auto()
    USING_DIRECTIVE = auto()
    EXTERN_ALIAS_DIRECTIVE = auto()
    CLASS_DECLARATION = auto()
    STRUCT_DECLARATION = auto()
    INTERFACE_DECLARATION = auto()
    ENUM_DECLARATION = auto()
    DELEGATE_DECLARATION = auto()
    RECORD_DECLARATION = auto()  # C# 9.0
    RECORD_STRUCT_DECLARATION = auto()  # C# 10.0
    FIELD_DECLARATION = auto()
    METHOD_DECLARATION = auto()
    CONSTRUCTOR_DECLARATION = auto()
    DESTRUCTOR_DECLARATION = auto()
    PROPERTY_DECLARATION = auto()
    INDEXER_DECLARATION = auto()
    EVENT_DECLARATION = auto()
    OPERATOR_DECLARATION = auto()
    CONVERSION_OPERATOR_DECLARATION = auto()
    VARIABLE_DECLARATION = auto()
    PARAMETER_DECLARATION = auto()
    TYPE_PARAMETER_DECLARATION = auto()
    GLOBAL_STATEMENT = auto()  # C# 9.0 (top-level programs)
    
    # Types
    PREDEFINED_TYPE = auto()
    NULLABLE_TYPE = auto()
    ARRAY_TYPE = auto()
    POINTER_TYPE = auto()
    REFERENCE_TYPE = auto()
    GENERIC_TYPE = auto()
    TUPLE_TYPE = auto()  # C# 7.0
    FUNCTION_POINTER_TYPE = auto()  # C# 9.0
    SCOPED_TYPE = auto()  # C# 11.0
    
    # Attributes
    ATTRIBUTE = auto()
    ATTRIBUTE_LIST = auto()
    ATTRIBUTE_ARGUMENT = auto()
    
    # Generics
    TYPE_PARAMETER = auto()
    TYPE_PARAMETER_CONSTRAINT = auto()
    TYPE_ARGUMENT_LIST = auto()
    
    # LINQ
    QUERY_BODY = auto()
    QUERY_CLAUSE = auto()
    FROM_CLAUSE = auto()
    WHERE_CLAUSE = auto()
    SELECT_CLAUSE = auto()
    GROUP_CLAUSE = auto()
    ORDER_BY_CLAUSE = auto()
    JOIN_CLAUSE = auto()
    LET_CLAUSE = auto()
    
    # Patterns (C# 7.0+)
    CONSTANT_PATTERN = auto()
    DECLARATION_PATTERN = auto()
    VAR_PATTERN = auto()
    WILDCARD_PATTERN = auto()
    TUPLE_PATTERN = auto()
    POSITIONAL_PATTERN = auto()
    PROPERTY_PATTERN = auto()
    RELATIONAL_PATTERN = auto()  # C# 9.0
    LOGICAL_PATTERN = auto()  # C# 9.0
    LIST_PATTERN = auto()  # C# 11.0
    
    # Async/await
    ASYNC_MODIFIER = auto()
    AWAIT_EXPRESSION_ASYNC = auto()
    
    # Nullable reference types (C# 8.0)
    NULLABLE_REFERENCE_TYPE = auto()
    NULL_FORGIVING_OPERATOR = auto()
    
    # Raw string literals (C# 11.0)
    RAW_STRING_LITERAL = auto()
    
    # Required members (C# 11.0)
    REQUIRED_MODIFIER = auto()
    
    # File-scoped namespaces (C# 10.0)
    FILE_SCOPED_NAMESPACE = auto()


class CSharpAccessibility(Enum):
    """C# accessibility levels."""
    PRIVATE = auto()
    PROTECTED = auto()
    INTERNAL = auto()
    PROTECTED_INTERNAL = auto()
    PRIVATE_PROTECTED = auto()  # C# 7.2
    PUBLIC = auto()
    FILE = auto()  # C# 11.0


class CSharpModifier(Enum):
    """C# modifiers."""
    ABSTRACT = auto()
    ASYNC = auto()
    CONST = auto()
    EXTERN = auto()
    OVERRIDE = auto()
    PARTIAL = auto()
    READONLY = auto()
    SEALED = auto()
    STATIC = auto()
    UNSAFE = auto()
    VIRTUAL = auto()
    VOLATILE = auto()
    NEW = auto()
    REQUIRED = auto()  # C# 11.0
    SCOPED = auto()  # C# 11.0
    REF = auto()
    OUT = auto()
    IN = auto()
    PARAMS = auto()


class CSharpOperator(Enum):
    """C# operators."""
    # Arithmetic
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    
    # Assignment
    ASSIGN = auto()
    PLUS_ASSIGN = auto()
    MINUS_ASSIGN = auto()
    MULTIPLY_ASSIGN = auto()
    DIVIDE_ASSIGN = auto()
    MODULO_ASSIGN = auto()
    AND_ASSIGN = auto()
    OR_ASSIGN = auto()
    XOR_ASSIGN = auto()
    LEFT_SHIFT_ASSIGN = auto()
    RIGHT_SHIFT_ASSIGN = auto()
    UNSIGNED_RIGHT_SHIFT_ASSIGN = auto()  # C# 11.0
    NULL_COALESCING_ASSIGN = auto()  # C# 8.0
    
    # Comparison
    EQUAL = auto()
    NOT_EQUAL = auto()
    LESS_THAN = auto()
    LESS_EQUAL = auto()
    GREATER_THAN = auto()
    GREATER_EQUAL = auto()
    
    # Logical
    LOGICAL_AND = auto()
    LOGICAL_OR = auto()
    LOGICAL_NOT = auto()
    
    # Bitwise
    BITWISE_AND = auto()
    BITWISE_OR = auto()
    BITWISE_XOR = auto()
    BITWISE_NOT = auto()
    LEFT_SHIFT = auto()
    RIGHT_SHIFT = auto()
    UNSIGNED_RIGHT_SHIFT = auto()  # C# 11.0
    
    # Unary
    UNARY_PLUS = auto()
    UNARY_MINUS = auto()
    INCREMENT = auto()
    DECREMENT = auto()
    
    # Special
    CONDITIONAL = auto()  # ?
    NULL_COALESCING = auto()  # ??
    NULL_CONDITIONAL = auto()  # ?.
    MEMBER_BINDING = auto()  # .
    POINTER_MEMBER_ACCESS = auto()  # ->
    RANGE = auto()  # .. (C# 8.0)
    INDEX_FROM_END = auto()  # ^ (C# 8.0)
    NULL_FORGIVING = auto()  # ! (C# 8.0)
    PATTERN_MATCHING = auto()  # is
    TYPE_TESTING = auto()  # as


@dataclass
class CSharpNode(ABC):
    """Base class for all C# AST nodes."""
    type: Optional[CSharpNodeType] = field(default=None)
    span: Optional[Dict[str, Any]] = field(default=None)
    parent: Optional['CSharpNode'] = field(default=None)
    leading_trivia: List[str] = field(default_factory=list)
    trailing_trivia: List[str] = field(default_factory=list)
    
    @abstractmethod
    def accept(self, visitor):
        """Accept a visitor for the visitor pattern."""
        pass
    
    def get_children(self) -> List['CSharpNode']:
        """Get all child nodes."""
        children = []
        for field_name, field_value in self.__dict__.items():
            if isinstance(field_value, CSharpNode):
                children.append(field_value)
            elif isinstance(field_value, list):
                for item in field_value:
                    if isinstance(item, CSharpNode):
                        children.append(item)
        return children
    
    def get_descendants(self) -> List['CSharpNode']:
        """Get all descendant nodes."""
        descendants = []
        for child in self.get_children():
            descendants.append(child)
            descendants.extend(child.get_descendants())
        return descendants


# Expressions
@dataclass
class CSharpExpression(CSharpNode):
    """Base class for C# expressions."""
    pass


@dataclass
class CSharpLiteral(CSharpExpression):
    """C# literal expression."""
    value: Any = field(default=None)
    literal_type: str = field(default="string")  # "int", "string", "bool", etc.
    type: Optional[CSharpNodeType] = field(default=CSharpNodeType.LITERAL, init=False)
    
    def accept(self, visitor):
        return visitor.visit_literal(self)


@dataclass
class CSharpIdentifier(CSharpExpression):
    """C# identifier expression."""
    name: str = ""
    is_verbatim: bool = False  # @identifier
    
    def accept(self, visitor):
        return visitor.visit_identifier(self)


@dataclass
class CSharpQualifiedName(CSharpExpression):
    """C# qualified name expression."""
    left: Optional[CSharpExpression] = None
    right: Optional[CSharpExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_qualified_name(self)


@dataclass
class CSharpGenericName(CSharpExpression):
    """C# generic name expression."""
    name: str = ""
    type_arguments: List['CSharpType'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_generic_name(self)


@dataclass
class CSharpBinaryExpression(CSharpExpression):
    """C# binary expression."""
    left: Optional[CSharpExpression] = field(default=None)
    operator: Optional[CSharpOperator] = field(default=CSharpOperator.PLUS)
    right: Optional[CSharpExpression] = field(default=None)
    type: Optional[CSharpNodeType] = field(default=CSharpNodeType.BINARY_EXPRESSION, init=False)
    
    def accept(self, visitor):
        return visitor.visit_binary_expression(self)


@dataclass
class CSharpUnaryExpression(CSharpExpression):
    """C# unary expression."""
    operator: Optional[CSharpOperator] = field(default=CSharpOperator.LOGICAL_NOT)
    operand: Optional[CSharpExpression] = field(default=None)
    is_prefix: bool = field(default=True)
    type: Optional[CSharpNodeType] = field(default=CSharpNodeType.UNARY_EXPRESSION, init=False)
    
    def accept(self, visitor):
        return visitor.visit_unary_expression(self)


@dataclass
class CSharpConditionalExpression(CSharpExpression):
    """C# conditional expression (ternary operator)."""
    condition: Optional[CSharpExpression] = None
    when_true: Optional[CSharpExpression] = None
    when_false: Optional[CSharpExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_conditional_expression(self)


@dataclass
class CSharpAssignmentExpression(CSharpExpression):
    """C# assignment expression."""
    left: Optional[CSharpExpression] = field(default=None)
    operator: Optional[CSharpOperator] = field(default=CSharpOperator.ASSIGN)
    right: Optional[CSharpExpression] = field(default=None)
    type: Optional[CSharpNodeType] = field(default=CSharpNodeType.ASSIGNMENT_EXPRESSION, init=False)
    
    def accept(self, visitor):
        return visitor.visit_assignment_expression(self)


@dataclass
class CSharpInvocationExpression(CSharpExpression):
    """C# method invocation expression."""
    expression: Optional[CSharpExpression] = None
    arguments: List[CSharpExpression] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_invocation_expression(self)


@dataclass
class CSharpMethodInvocationExpression(CSharpExpression):
    """C# method invocation expression."""
    method_name: str = ""
    arguments: List[CSharpExpression] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_method_invocation_expression(self)


@dataclass
class CSharpMemberAccessExpression(CSharpExpression):
    """C# member access expression."""
    expression: Optional[CSharpExpression] = None
    name: str = ""
    is_conditional: bool = False  # ?. operator
    
    def accept(self, visitor):
        return visitor.visit_member_access_expression(self)


@dataclass
class CSharpIndexerAccessExpression(CSharpExpression):
    """C# indexer access expression."""
    target: str = ""
    arguments: List[CSharpExpression] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_indexer_access_expression(self)


@dataclass
class CSharpCastExpression(CSharpExpression):
    """C# cast expression."""
    target_type: Optional['CSharpType'] = None
    expression: Optional[CSharpExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_cast_expression(self)


@dataclass
class CSharpIsExpression(CSharpExpression):
    """C# is expression."""
    expression: Optional[CSharpExpression] = None
    type_or_pattern: Optional[Union['CSharpType', 'CSharpPattern']] = None
    
    def accept(self, visitor):
        return visitor.visit_is_expression(self)


@dataclass
class CSharpAsExpression(CSharpExpression):
    """C# as expression."""
    expression: Optional[CSharpExpression] = None
    target_type: Optional['CSharpType'] = None
    
    def accept(self, visitor):
        return visitor.visit_as_expression(self)


@dataclass
class CSharpThisExpression(CSharpExpression):
    """C# this expression."""
    
    def accept(self, visitor):
        return visitor.visit_this_expression(self)


@dataclass
class CSharpBaseExpression(CSharpExpression):
    """C# base expression."""
    
    def accept(self, visitor):
        return visitor.visit_base_expression(self)


@dataclass
class CSharpTypeofExpression(CSharpExpression):
    """C# typeof expression."""
    target_type: Optional['CSharpType'] = None
    
    def accept(self, visitor):
        return visitor.visit_typeof_expression(self)


@dataclass
class CSharpSizeofExpression(CSharpExpression):
    """C# sizeof expression."""
    target_type: Optional['CSharpType'] = None
    
    def accept(self, visitor):
        return visitor.visit_sizeof_expression(self)


@dataclass
class CSharpNameofExpression(CSharpExpression):
    """C# nameof expression (C# 6.0)."""
    expression: Optional[CSharpExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_nameof_expression(self)


@dataclass
class CSharpDefaultExpression(CSharpExpression):
    """C# default expression."""
    target_type: Optional['CSharpType'] = None  # Can be null for default literals
    
    def accept(self, visitor):
        return visitor.visit_default_expression(self)


@dataclass
class CSharpObjectCreationExpression(CSharpExpression):
    """C# object creation expression."""
    type: Optional['CSharpType'] = None  # Can be null for anonymous types
    arguments: List[CSharpExpression] = field(default_factory=list)
    initializer: Optional['CSharpInitializerExpression'] = None
    
    def accept(self, visitor):
        return visitor.visit_object_creation_expression(self)


@dataclass
class CSharpObjectInitializerExpression(CSharpExpression):
    """C# object initializer expression."""
    initializers: List['CSharpInitializerAssignment'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_object_initializer_expression(self)


@dataclass
class CSharpInitializerAssignment(CSharpNode):
    """C# initializer assignment."""
    property_name: str = ""
    value: Optional[CSharpExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_initializer_assignment(self)


@dataclass
class CSharpArrayCreationExpression(CSharpExpression):
    """C# array creation expression."""
    type: Optional['CSharpType'] = None
    rank_specifiers: List[List[CSharpExpression]] = field(default_factory=list)  # Dimensions
    initializer: Optional['CSharpInitializerExpression'] = None
    
    def accept(self, visitor):
        return visitor.visit_array_creation_expression(self)


@dataclass
class CSharpImplicitArrayCreationExpression(CSharpExpression):
    """C# implicit array creation expression."""
    commas: int = 0  # Number of commas (determines dimensions)
    initializer: Optional['CSharpInitializerExpression'] = None
    
    def accept(self, visitor):
        return visitor.visit_implicit_array_creation_expression(self)


@dataclass
class CSharpAnonymousObjectCreationExpression(CSharpExpression):
    """C# anonymous object creation expression."""
    initializers: List['CSharpAnonymousObjectMemberDeclarator'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_anonymous_object_creation_expression(self)


@dataclass
class CSharpAnonymousObjectMemberDeclarator(CSharpNode):
    """C# anonymous object member declarator."""
    name: Optional[str] = None  # Can be null for implicit naming
    expression: Optional[CSharpExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_anonymous_object_member_declarator(self)


@dataclass
class CSharpInitializerExpression(CSharpExpression):
    """C# initializer expression."""
    expressions: List[CSharpExpression] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_initializer_expression(self)


@dataclass
class CSharpLambdaExpression(CSharpExpression):
    """C# lambda expression."""
    parameters: List['CSharpParameter'] = field(default_factory=list)
    body: Optional[Union[CSharpExpression, 'CSharpStatement']] = None
    is_async: bool = False
    modifiers: List[CSharpModifier] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_lambda_expression(self)


@dataclass
class CSharpAnonymousMethodExpression(CSharpExpression):
    """C# anonymous method expression."""
    parameters: Optional[List['CSharpParameter']] = None
    body: Optional['CSharpStatement'] = None
    is_async: bool = False
    
    def accept(self, visitor):
        return visitor.visit_anonymous_method_expression(self)


@dataclass
class CSharpAwaitExpression(CSharpExpression):
    """C# await expression."""
    expression: Optional[CSharpExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_await_expression(self)


@dataclass
class CSharpTupleExpression(CSharpExpression):
    """C# tuple expression."""
    arguments: List['CSharpArgument'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_tuple_expression(self)


@dataclass
class CSharpThrowExpression(CSharpExpression):
    """C# throw expression."""
    expression: Optional[CSharpExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_throw_expression(self)


@dataclass
class CSharpRangeExpression(CSharpExpression):
    """C# range expression (..)."""
    left: Optional[CSharpExpression] = None  # Can be null for open range
    right: Optional[CSharpExpression] = None  # Can be null for open range
    
    def accept(self, visitor):
        return visitor.visit_range_expression(self)


@dataclass
class CSharpIndexExpression(CSharpExpression):
    """C# index expression (^)."""
    operand: Optional[CSharpExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_index_expression(self)


@dataclass
class CSharpSwitchExpression(CSharpExpression):
    """C# switch expression."""
    governing_expression: Optional[CSharpExpression] = None
    arms: List['CSharpSwitchExpressionArm'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_switch_expression(self)


@dataclass
class CSharpSwitchExpressionArm(CSharpNode):
    """C# switch expression arm."""
    pattern: Optional['CSharpPattern'] = None
    when_clause: Optional[CSharpExpression] = None
    expression: Optional[CSharpExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_switch_expression_arm(self)


@dataclass
class CSharpWithExpression(CSharpExpression):
    """C# with expression (records)."""
    expression: Optional[CSharpExpression] = None
    initializer: Optional['CSharpInitializerExpression'] = None
    
    def accept(self, visitor):
        return visitor.visit_with_expression(self)


@dataclass
class CSharpInterpolatedStringExpression(CSharpExpression):
    """C# interpolated string expression."""
    parts: List[Union[str, 'CSharpInterpolationExpression']] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_interpolated_string_expression(self)


@dataclass
class CSharpInterpolationExpression(CSharpNode):
    """C# interpolation expression inside interpolated string."""
    expression: Optional[CSharpExpression] = None
    alignment: Optional[CSharpExpression] = None
    format_string: Optional[str] = None
    
    def accept(self, visitor):
        return visitor.visit_interpolation_expression(self)


# Statements
@dataclass
class CSharpStatement(CSharpNode):
    """Base class for C# statements."""
    pass


@dataclass
class CSharpExpressionStatement(CSharpStatement):
    """C# expression statement."""
    expression: Optional[CSharpExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_expression_statement(self)


@dataclass
class CSharpBlock(CSharpStatement):
    """C# block statement."""
    statements: List[CSharpStatement] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_block(self)


@dataclass
class CSharpIfStatement(CSharpStatement):
    """C# if statement."""
    condition: Optional[CSharpExpression] = None
    statement: Optional[CSharpStatement] = None
    else_statement: Optional[CSharpStatement] = None
    
    def accept(self, visitor):
        return visitor.visit_if_statement(self)


@dataclass
class CSharpWhileStatement(CSharpStatement):
    """C# while statement."""
    condition: Optional[CSharpExpression] = None
    statement: Optional[CSharpStatement] = None
    
    def accept(self, visitor):
        return visitor.visit_while_statement(self)


@dataclass
class CSharpForStatement(CSharpStatement):
    """C# for statement."""
    declaration: Optional['CSharpVariableDeclaration'] = None
    initializers: List[CSharpExpression] = field(default_factory=list)
    condition: Optional[CSharpExpression] = None
    incrementors: List[CSharpExpression] = field(default_factory=list)
    statement: Optional[CSharpStatement] = None
    
    def accept(self, visitor):
        return visitor.visit_for_statement(self)


@dataclass
class CSharpForEachStatement(CSharpStatement):
    """C# foreach statement."""
    type: Optional['CSharpType'] = None  # Can be null for var
    identifier: str = ""
    expression: Optional[CSharpExpression] = None
    statement: Optional[CSharpStatement] = None
    await_keyword: bool = False  # C# 8.0
    
    def accept(self, visitor):
        return visitor.visit_foreach_statement(self)


@dataclass
class CSharpDoStatement(CSharpStatement):
    """C# do statement."""
    statement: Optional[CSharpStatement] = None
    condition: Optional[CSharpExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_do_statement(self)


@dataclass
class CSharpSwitchStatement(CSharpStatement):
    """C# switch statement."""
    expression: Optional[CSharpExpression] = None
    sections: List['CSharpSwitchSection'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_switch_statement(self)


@dataclass
class CSharpSwitchSection(CSharpNode):
    """C# switch section."""
    labels: List['CSharpSwitchLabel'] = field(default_factory=list)
    statements: List[CSharpStatement] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_switch_section(self)


@dataclass
class CSharpSwitchLabel(CSharpNode):
    """C# switch label."""
    pass


@dataclass
class CSharpCaseSwitchLabel(CSharpSwitchLabel):
    """C# case switch label."""
    value: Optional[CSharpExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_case_switch_label(self)


@dataclass
class CSharpDefaultSwitchLabel(CSharpSwitchLabel):
    """C# default switch label."""
    
    def accept(self, visitor):
        return visitor.visit_default_switch_label(self)


@dataclass
class CSharpCasePatternSwitchLabel(CSharpSwitchLabel):
    """C# case pattern switch label."""
    pattern: Optional['CSharpPattern'] = None
    when_clause: Optional[CSharpExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_case_pattern_switch_label(self)


@dataclass
class CSharpBreakStatement(CSharpStatement):
    """C# break statement."""
    
    def accept(self, visitor):
        return visitor.visit_break_statement(self)


@dataclass
class CSharpContinueStatement(CSharpStatement):
    """C# continue statement."""
    
    def accept(self, visitor):
        return visitor.visit_continue_statement(self)


@dataclass
class CSharpReturnStatement(CSharpStatement):
    """C# return statement."""
    expression: Optional[CSharpExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_return_statement(self)


@dataclass
class CSharpThrowStatement(CSharpStatement):
    """C# throw statement."""
    expression: Optional[CSharpExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_throw_statement(self)


@dataclass
class CSharpTryStatement(CSharpStatement):
    """C# try statement."""
    block: Optional[CSharpBlock] = None
    catches: List['CSharpCatchClause'] = field(default_factory=list)
    finally_block: Optional[CSharpBlock] = None
    
    def accept(self, visitor):
        return visitor.visit_try_statement(self)


@dataclass
class CSharpCatchClause(CSharpNode):
    """C# catch clause."""
    declaration: Optional['CSharpCatchDeclaration'] = None
    filter: Optional['CSharpCatchFilterClause'] = None
    block: Optional[CSharpBlock] = None
    
    def accept(self, visitor):
        return visitor.visit_catch_clause(self)


@dataclass
class CSharpCatchDeclaration(CSharpNode):
    """C# catch declaration."""
    type: Optional['CSharpType'] = None
    identifier: Optional[str] = None
    
    def accept(self, visitor):
        return visitor.visit_catch_declaration(self)


@dataclass
class CSharpCatchFilterClause(CSharpNode):
    """C# catch filter clause."""
    expression: Optional[CSharpExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_catch_filter_clause(self)


@dataclass
class CSharpLockStatement(CSharpStatement):
    """C# lock statement."""
    expression: Optional[CSharpExpression] = None
    statement: Optional[CSharpStatement] = None
    
    def accept(self, visitor):
        return visitor.visit_lock_statement(self)


@dataclass
class CSharpUsingStatement(CSharpStatement):
    """C# using statement."""
    declaration: Optional['CSharpVariableDeclaration'] = None
    expression: Optional[CSharpExpression] = None
    statement: Optional[CSharpStatement] = None
    await_keyword: bool = False  # C# 8.0
    
    def accept(self, visitor):
        return visitor.visit_using_statement(self)


@dataclass
class CSharpYieldStatement(CSharpStatement):
    """C# yield statement."""
    expression: Optional[CSharpExpression] = None  # null for yield break
    is_break: bool = False
    
    def accept(self, visitor):
        return visitor.visit_yield_statement(self)


@dataclass
class CSharpEmptyStatement(CSharpStatement):
    """C# empty statement."""
    
    def accept(self, visitor):
        return visitor.visit_empty_statement(self)


@dataclass
class CSharpLabeledStatement(CSharpStatement):
    """C# labeled statement."""
    identifier: str = ""
    statement: Optional[CSharpStatement] = None
    
    def accept(self, visitor):
        return visitor.visit_labeled_statement(self)


@dataclass
class CSharpGotoStatement(CSharpStatement):
    """C# goto statement."""
    label: str = ""
    
    def accept(self, visitor):
        return visitor.visit_goto_statement(self)


@dataclass
class CSharpCheckedStatement(CSharpStatement):
    """C# checked statement."""
    block: Optional[CSharpBlock] = None
    
    def accept(self, visitor):
        return visitor.visit_checked_statement(self)


@dataclass
class CSharpUncheckedStatement(CSharpStatement):
    """C# unchecked statement."""
    block: Optional[CSharpBlock] = None
    
    def accept(self, visitor):
        return visitor.visit_unchecked_statement(self)


@dataclass
class CSharpUnsafeStatement(CSharpStatement):
    """C# unsafe statement."""
    block: Optional[CSharpBlock] = None
    
    def accept(self, visitor):
        return visitor.visit_unsafe_statement(self)


@dataclass
class CSharpFixedStatement(CSharpStatement):
    """C# fixed statement."""
    declaration: Optional['CSharpVariableDeclaration'] = None
    statement: Optional[CSharpStatement] = None
    
    def accept(self, visitor):
        return visitor.visit_fixed_statement(self)


@dataclass
class CSharpLocalDeclarationStatement(CSharpStatement):
    """C# local declaration statement."""
    declaration: Optional['CSharpVariableDeclaration'] = None
    await_keyword: bool = False  # C# 8.0
    using_keyword: bool = False  # C# 8.0
    
    def accept(self, visitor):
        return visitor.visit_local_declaration_statement(self)


# Declarations
@dataclass
class CSharpDeclaration(CSharpNode):
    """Base class for C# declarations."""
    pass


@dataclass
class CSharpCompilationUnit(CSharpDeclaration):
    """C# compilation unit (file)."""
    extern_alias_directives: List['CSharpExternAliasDirective'] = field(default_factory=list)
    using_directives: List['CSharpUsingDirective'] = field(default_factory=list)
    global_attributes: List['CSharpAttributeList'] = field(default_factory=list)
    members: List[CSharpDeclaration] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_compilation_unit(self)


@dataclass
class CSharpNamespaceDeclaration(CSharpDeclaration):
    """C# namespace declaration."""
    name: Optional[CSharpExpression] = None
    extern_alias_directives: List['CSharpExternAliasDirective'] = field(default_factory=list)
    using_directives: List['CSharpUsingDirective'] = field(default_factory=list)
    members: List[CSharpDeclaration] = field(default_factory=list)
    is_file_scoped: bool = False  # C# 10.0
    
    def accept(self, visitor):
        return visitor.visit_namespace_declaration(self)


@dataclass
class CSharpUsingDirective(CSharpDeclaration):
    """C# using directive."""
    name: Optional[CSharpExpression] = None
    alias: Optional[str] = None
    static_keyword: bool = False  # C# 6.0
    global_keyword: bool = False  # C# 10.0
    
    def accept(self, visitor):
        return visitor.visit_using_directive(self)


@dataclass
class CSharpExternAliasDirective(CSharpDeclaration):
    """C# extern alias directive."""
    identifier: str = ""
    
    def accept(self, visitor):
        return visitor.visit_extern_alias_directive(self)


@dataclass
class CSharpTypeDeclaration(CSharpDeclaration):
    """Base class for C# type declarations."""
    attributes: List['CSharpAttributeList'] = field(default_factory=list)
    modifiers: List[CSharpModifier] = field(default_factory=list)
    identifier: str = ""
    type_parameter_list: Optional['CSharpTypeParameterList'] = None
    constraint_clauses: List['CSharpTypeParameterConstraintClause'] = field(default_factory=list)
    
    def get_accessibility(self) -> Optional[CSharpAccessibility]:
        """Get the accessibility of this type declaration."""
        for modifier in self.modifiers:
            if modifier in [CSharpModifier.PUBLIC, CSharpModifier.PRIVATE, 
                           CSharpModifier.PROTECTED, CSharpModifier.INTERNAL]:
                return CSharpAccessibility[modifier.name]
        return None


@dataclass
class CSharpClassDeclaration(CSharpTypeDeclaration):
    """C# class declaration."""
    base_list: Optional['CSharpBaseList'] = None
    members: List['CSharpMemberDeclaration'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_class_declaration(self)


@dataclass
class CSharpStructDeclaration(CSharpTypeDeclaration):
    """C# struct declaration."""
    base_list: Optional['CSharpBaseList'] = None
    members: List['CSharpMemberDeclaration'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_struct_declaration(self)


@dataclass
class CSharpInterfaceDeclaration(CSharpTypeDeclaration):
    """C# interface declaration."""
    base_list: Optional['CSharpBaseList'] = None
    members: List['CSharpMemberDeclaration'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_interface_declaration(self)


@dataclass
class CSharpEnumDeclaration(CSharpTypeDeclaration):
    """C# enum declaration."""
    base_list: Optional['CSharpBaseList'] = None
    members: List['CSharpEnumMemberDeclaration'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_enum_declaration(self)


@dataclass
class CSharpEnumMemberDeclaration(CSharpDeclaration):
    """C# enum member declaration."""
    attributes: List['CSharpAttributeList'] = field(default_factory=list)
    identifier: str = ""
    equals_value: Optional[CSharpExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_enum_member_declaration(self)


@dataclass
class CSharpDelegateDeclaration(CSharpTypeDeclaration):
    """C# delegate declaration."""
    return_type: Optional['CSharpType'] = None
    parameter_list: Optional['CSharpParameterList'] = None
    
    def accept(self, visitor):
        return visitor.visit_delegate_declaration(self)


@dataclass
class CSharpRecordDeclaration(CSharpTypeDeclaration):
    """C# record declaration."""
    class_or_struct_keyword: str = ""  # "class" or "struct"
    parameter_list: Optional['CSharpParameterList'] = None
    base_list: Optional['CSharpBaseList'] = None
    members: List['CSharpMemberDeclaration'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_record_declaration(self)


@dataclass
class CSharpBaseList(CSharpNode):
    """C# base list."""
    types: List['CSharpType'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_base_list(self)


@dataclass
class CSharpMemberDeclaration(CSharpDeclaration):
    """Base class for C# member declarations."""
    attributes: List['CSharpAttributeList'] = field(default_factory=list)
    modifiers: List[CSharpModifier] = field(default_factory=list)


@dataclass
class CSharpFieldDeclaration(CSharpMemberDeclaration):
    """C# field declaration."""
    declaration: Optional['CSharpVariableDeclaration'] = None
    
    def accept(self, visitor):
        return visitor.visit_field_declaration(self)


@dataclass
class CSharpMethodDeclaration(CSharpMemberDeclaration):
    """C# method declaration."""
    return_type: Optional['CSharpType'] = None
    identifier: str = ""
    type_parameter_list: Optional['CSharpTypeParameterList'] = None
    parameter_list: Optional['CSharpParameterList'] = None
    constraint_clauses: List['CSharpTypeParameterConstraintClause'] = field(default_factory=list)
    body: Optional[CSharpBlock] = None
    expression_body: Optional[CSharpExpression] = None
    semicolon_token: bool = False
    
    def accept(self, visitor):
        return visitor.visit_method_declaration(self)


@dataclass
class CSharpConstructorDeclaration(CSharpMemberDeclaration):
    """C# constructor declaration."""
    identifier: str = ""
    parameter_list: Optional['CSharpParameterList'] = None
    initializer: Optional['CSharpConstructorInitializer'] = None
    body: Optional[CSharpBlock] = None
    expression_body: Optional[CSharpExpression] = None
    semicolon_token: bool = False
    
    def accept(self, visitor):
        return visitor.visit_constructor_declaration(self)


@dataclass
class CSharpConstructorInitializer(CSharpNode):
    """C# constructor initializer."""
    this_or_base: str = ""  # "this" or "base"
    arguments: List[CSharpExpression] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_constructor_initializer(self)


@dataclass
class CSharpDestructorDeclaration(CSharpMemberDeclaration):
    """C# destructor declaration."""
    identifier: str = ""
    parameter_list: Optional['CSharpParameterList'] = None
    body: Optional[CSharpBlock] = None
    expression_body: Optional[CSharpExpression] = None
    semicolon_token: bool = False
    
    def accept(self, visitor):
        return visitor.visit_destructor_declaration(self)


@dataclass
class CSharpPropertyDeclaration(CSharpMemberDeclaration):
    """C# property declaration."""
    type: Optional['CSharpType'] = None
    identifier: str = ""
    accessor_list: Optional['CSharpAccessorList'] = None
    expression_body: Optional[CSharpExpression] = None
    initializer: Optional['CSharpEqualsValueClause'] = None
    
    def accept(self, visitor):
        return visitor.visit_property_declaration(self)


@dataclass
class CSharpIndexerDeclaration(CSharpMemberDeclaration):
    """C# indexer declaration."""
    type: Optional['CSharpType'] = None
    parameter_list: Optional['CSharpBracketedParameterList'] = None
    accessor_list: Optional['CSharpAccessorList'] = None
    expression_body: Optional[CSharpExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_indexer_declaration(self)


@dataclass
class CSharpEventDeclaration(CSharpMemberDeclaration):
    """C# event declaration."""
    type: Optional['CSharpType'] = None
    identifier: str = ""
    accessor_list: Optional['CSharpAccessorList'] = None
    initializer: Optional['CSharpEqualsValueClause'] = None
    
    def accept(self, visitor):
        return visitor.visit_event_declaration(self)


@dataclass
class CSharpEventFieldDeclaration(CSharpMemberDeclaration):
    """C# event field declaration."""
    declaration: Optional['CSharpVariableDeclaration'] = None
    
    def accept(self, visitor):
        return visitor.visit_event_field_declaration(self)


@dataclass
class CSharpOperatorDeclaration(CSharpMemberDeclaration):
    """C# operator declaration."""
    return_type: Optional['CSharpType'] = None
    operator_token: str = ""
    parameter_list: Optional['CSharpParameterList'] = None
    body: Optional[CSharpBlock] = None
    expression_body: Optional[CSharpExpression] = None
    semicolon_token: bool = False
    
    def accept(self, visitor):
        return visitor.visit_operator_declaration(self)


@dataclass
class CSharpConversionOperatorDeclaration(CSharpMemberDeclaration):
    """C# conversion operator declaration."""
    implicit_or_explicit: str = ""  # "implicit" or "explicit"
    type: Optional['CSharpType'] = None
    parameter_list: Optional['CSharpParameterList'] = None
    body: Optional[CSharpBlock] = None
    expression_body: Optional[CSharpExpression] = None
    semicolon_token: bool = False
    
    def accept(self, visitor):
        return visitor.visit_conversion_operator_declaration(self)


@dataclass
class CSharpAccessorList(CSharpNode):
    """C# accessor list."""
    accessors: List['CSharpAccessorDeclaration'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_accessor_list(self)


@dataclass
class CSharpAccessorDeclaration(CSharpNode):
    """C# accessor declaration."""
    attributes: List['CSharpAttributeList'] = field(default_factory=list)
    modifiers: List[CSharpModifier] = field(default_factory=list)
    keyword: str = ""  # "get", "set", "add", "remove"
    body: Optional[CSharpBlock] = None
    expression_body: Optional[CSharpExpression] = None
    semicolon_token: bool = False
    
    def accept(self, visitor):
        return visitor.visit_accessor_declaration(self)


# Types
@dataclass
class CSharpType(CSharpNode):
    """Base class for C# types."""
    pass


@dataclass
class CSharpPredefinedType(CSharpType):
    """C# predefined type."""
    keyword: str = ""  # "int", "string", "bool", etc.
    
    def accept(self, visitor):
        return visitor.visit_predefined_type(self)


@dataclass
class CSharpIdentifierName(CSharpType):
    """C# identifier name type."""
    identifier: str = ""
    
    def accept(self, visitor):
        return visitor.visit_identifier_name(self)


@dataclass
class CSharpQualifiedNameType(CSharpType):
    """C# qualified name type."""
    left: Optional[CSharpType] = None
    right: Optional[CSharpType] = None
    
    def accept(self, visitor):
        return visitor.visit_qualified_name_type(self)


@dataclass
class CSharpGenericNameType(CSharpType):
    """C# generic name type."""
    identifier: str = ""
    type_argument_list: Optional['CSharpTypeArgumentList'] = None
    
    def accept(self, visitor):
        return visitor.visit_generic_name_type(self)


@dataclass
class CSharpGenericType(CSharpType):
    """C# generic type."""
    identifier: str = ""
    type_arguments: List['CSharpType'] = field(default_factory=list)
    array_rank: int = 0
    
    def accept(self, visitor):
        return visitor.visit_generic_type(self)


@dataclass
class CSharpArrayType(CSharpType):
    """C# array type."""
    element_type: Optional[CSharpType] = None
    rank_specifiers: List['CSharpArrayRankSpecifier'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_array_type(self)


@dataclass
class CSharpArrayRankSpecifier(CSharpNode):
    """C# array rank specifier."""
    sizes: List[Optional[CSharpExpression]] = field(default_factory=list)  # None for omitted dimensions
    
    def accept(self, visitor):
        return visitor.visit_array_rank_specifier(self)


@dataclass
class CSharpPointerType(CSharpType):
    """C# pointer type."""
    element_type: Optional[CSharpType] = None
    
    def accept(self, visitor):
        return visitor.visit_pointer_type(self)


@dataclass
class CSharpNullableType(CSharpType):
    """C# nullable type."""
    element_type: Optional[CSharpType] = None
    
    def accept(self, visitor):
        return visitor.visit_nullable_type(self)


@dataclass
class CSharpTupleType(CSharpType):
    """C# tuple type."""
    elements: List['CSharpTupleElement'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_tuple_type(self)


@dataclass
class CSharpTupleElement(CSharpNode):
    """C# tuple element."""
    type: Optional[CSharpType] = None
    identifier: Optional[str] = None
    
    def accept(self, visitor):
        return visitor.visit_tuple_element(self)


@dataclass
class CSharpFunctionPointerType(CSharpType):
    """C# function pointer type."""
    calling_convention: Optional[str] = None
    parameter_list: Optional['CSharpFunctionPointerParameterList'] = None
    
    def accept(self, visitor):
        return visitor.visit_function_pointer_type(self)


@dataclass
class CSharpScopedType(CSharpType):
    """C# scoped type."""
    type: Optional[CSharpType] = None
    
    def accept(self, visitor):
        return visitor.visit_scoped_type(self)


# Parameters
@dataclass
class CSharpParameterList(CSharpNode):
    """C# parameter list."""
    parameters: List['CSharpParameter'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_parameter_list(self)


@dataclass
class CSharpBracketedParameterList(CSharpNode):
    """C# bracketed parameter list."""
    parameters: List['CSharpParameter'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_bracketed_parameter_list(self)


@dataclass
class CSharpFunctionPointerParameterList(CSharpNode):
    """C# function pointer parameter list."""
    parameters: List['CSharpFunctionPointerParameter'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_function_pointer_parameter_list(self)


@dataclass
class CSharpParameter(CSharpNode):
    """C# parameter."""
    attributes: List['CSharpAttributeList'] = field(default_factory=list)
    modifiers: List[CSharpModifier] = field(default_factory=list)
    type: Optional[CSharpType] = None  # Can be null for implicit typing
    identifier: str = ""
    default_value: Optional['CSharpEqualsValueClause'] = None
    
    def accept(self, visitor):
        return visitor.visit_parameter(self)


@dataclass
class CSharpFunctionPointerParameter(CSharpNode):
    """C# function pointer parameter."""
    attributes: List['CSharpAttributeList'] = field(default_factory=list)
    modifiers: List[CSharpModifier] = field(default_factory=list)
    type: Optional[CSharpType] = None
    
    def accept(self, visitor):
        return visitor.visit_function_pointer_parameter(self)


@dataclass
class CSharpArgument(CSharpNode):
    """C# argument."""
    name_colon: Optional[str] = None  # Named argument
    ref_kind_keyword: Optional[str] = None  # "ref", "out", "in"
    expression: Optional[CSharpExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_argument(self)


@dataclass
class CSharpArgumentList(CSharpNode):
    """C# argument list."""
    arguments: List[CSharpArgument] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_argument_list(self)


# Type parameters and constraints
@dataclass
class CSharpTypeParameterList(CSharpNode):
    """C# type parameter list."""
    parameters: List['CSharpTypeParameter'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_type_parameter_list(self)


@dataclass
class CSharpTypeParameter(CSharpNode):
    """C# type parameter."""
    attributes: List['CSharpAttributeList'] = field(default_factory=list)
    variance_keyword: Optional[str] = None  # "in", "out"
    identifier: str = ""
    
    def accept(self, visitor):
        return visitor.visit_type_parameter(self)


@dataclass
class CSharpTypeArgumentList(CSharpNode):
    """C# type argument list."""
    arguments: List[CSharpType] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_type_argument_list(self)


@dataclass
class CSharpTypeParameterConstraintClause(CSharpNode):
    """C# type parameter constraint clause."""
    name: str = ""
    constraints: List['CSharpTypeParameterConstraint'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_type_parameter_constraint_clause(self)


@dataclass
class CSharpTypeParameterConstraint(CSharpNode):
    """Base class for C# type parameter constraints."""
    pass


@dataclass
class CSharpClassOrStructConstraint(CSharpTypeParameterConstraint):
    """C# class or struct constraint."""
    class_or_struct_keyword: str = ""  # "class" or "struct"
    question_token: bool = False  # For nullable class constraint
    
    def accept(self, visitor):
        return visitor.visit_class_or_struct_constraint(self)


@dataclass
class CSharpTypeConstraint(CSharpTypeParameterConstraint):
    """C# type constraint."""
    type: Optional[CSharpType] = None
    
    def accept(self, visitor):
        return visitor.visit_type_constraint(self)


@dataclass
class CSharpConstructorConstraint(CSharpTypeParameterConstraint):
    """C# constructor constraint."""
    
    def accept(self, visitor):
        return visitor.visit_constructor_constraint(self)


@dataclass
class CSharpDefaultConstraint(CSharpTypeParameterConstraint):
    """C# default constraint."""
    
    def accept(self, visitor):
        return visitor.visit_default_constraint(self)


# Attributes
@dataclass
class CSharpAttributeList(CSharpNode):
    """C# attribute list."""
    target: Optional[str] = None  # "assembly", "module", "type", etc.
    attributes: List['CSharpAttribute'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_attribute_list(self)


@dataclass
class CSharpAttribute(CSharpNode):
    """C# attribute."""
    name: Optional[CSharpType] = None
    argument_list: Optional['CSharpAttributeArgumentList'] = None
    
    def accept(self, visitor):
        return visitor.visit_attribute(self)


@dataclass
class CSharpAttributeArgumentList(CSharpNode):
    """C# attribute argument list."""
    arguments: List['CSharpAttributeArgument'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_attribute_argument_list(self)


@dataclass
class CSharpAttributeArgument(CSharpNode):
    """C# attribute argument."""
    name_equals: Optional[str] = None  # Named argument
    name_colon: Optional[str] = None  # Named argument
    expression: Optional[CSharpExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_attribute_argument(self)


# Variable declarations
@dataclass
class CSharpVariableDeclaration(CSharpNode):
    """C# variable declaration."""
    type: Optional[CSharpType] = None
    variables: List['CSharpVariableDeclarator'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_variable_declaration(self)


@dataclass
class CSharpVariableDeclarator(CSharpNode):
    """C# variable declarator."""
    identifier: str = ""
    bracket_list: Optional['CSharpBracketedArgumentList'] = None
    initializer: Optional['CSharpEqualsValueClause'] = None
    
    def accept(self, visitor):
        return visitor.visit_variable_declarator(self)


@dataclass
class CSharpEqualsValueClause(CSharpNode):
    """C# equals value clause."""
    value: Optional[CSharpExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_equals_value_clause(self)


@dataclass
class CSharpBracketedArgumentList(CSharpNode):
    """C# bracketed argument list."""
    arguments: List[CSharpArgument] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_bracketed_argument_list(self)


# Patterns (C# 7.0+)
@dataclass
class CSharpPattern(CSharpNode):
    """Base class for C# patterns."""
    pass


@dataclass
class CSharpConstantPattern(CSharpPattern):
    """C# constant pattern."""
    expression: Optional[CSharpExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_constant_pattern(self)


@dataclass
class CSharpDeclarationPattern(CSharpPattern):
    """C# declaration pattern."""
    type: Optional[CSharpType] = None
    designation: Optional['CSharpVariableDesignation'] = None
    
    def accept(self, visitor):
        return visitor.visit_declaration_pattern(self)


@dataclass
class CSharpTypePattern(CSharpPattern):
    """C# type pattern (for is expressions and switch patterns)."""
    type: Optional[CSharpType] = None
    
    def accept(self, visitor):
        return visitor.visit_type_pattern(self)


@dataclass
class CSharpVarPattern(CSharpPattern):
    """C# var pattern."""
    designation: Optional['CSharpVariableDesignation'] = None
    
    def accept(self, visitor):
        return visitor.visit_var_pattern(self)


@dataclass
class CSharpDiscardPattern(CSharpPattern):
    """C# discard pattern."""
    
    def accept(self, visitor):
        return visitor.visit_discard_pattern(self)


@dataclass
class CSharpTuplePattern(CSharpPattern):
    """C# tuple pattern."""
    subpatterns: List['CSharpSubpattern'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_tuple_pattern(self)


@dataclass
class CSharpPositionalPattern(CSharpPattern):
    """C# positional pattern."""
    type: Optional[CSharpType] = None
    subpatterns: List['CSharpSubpattern'] = field(default_factory=list)
    designation: Optional['CSharpVariableDesignation'] = None
    
    def accept(self, visitor):
        return visitor.visit_positional_pattern(self)


@dataclass
class CSharpPropertyPattern(CSharpPattern):
    """C# property pattern."""
    type: Optional[CSharpType] = None
    subpatterns: List['CSharpSubpattern'] = field(default_factory=list)
    designation: Optional['CSharpVariableDesignation'] = None
    
    def accept(self, visitor):
        return visitor.visit_property_pattern(self)


@dataclass
class CSharpRelationalPattern(CSharpPattern):
    """C# relational pattern."""
    operator: Optional[CSharpOperator] = CSharpOperator.GREATER_THAN
    expression: Optional[CSharpExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_relational_pattern(self)


@dataclass
class CSharpLogicalPattern(CSharpPattern):
    """C# logical pattern."""
    operator: Optional[CSharpOperator] = CSharpOperator.LOGICAL_AND  # "and", "or", "not"
    left: Optional[CSharpPattern] = None
    right: Optional[CSharpPattern] = None
    
    def accept(self, visitor):
        return visitor.visit_logical_pattern(self)


@dataclass
class CSharpListPattern(CSharpPattern):
    """C# list pattern."""
    patterns: List[CSharpPattern] = field(default_factory=list)
    designation: Optional['CSharpVariableDesignation'] = None
    
    def accept(self, visitor):
        return visitor.visit_list_pattern(self)


@dataclass
class CSharpSubpattern(CSharpNode):
    """C# subpattern."""
    name_colon: Optional[str] = None
    pattern: Optional[CSharpPattern] = None
    
    def accept(self, visitor):
        return visitor.visit_subpattern(self)


@dataclass
class CSharpVariableDesignation(CSharpNode):
    """Base class for C# variable designations."""
    pass


@dataclass
class CSharpSingleVariableDesignation(CSharpVariableDesignation):
    """C# single variable designation."""
    identifier: str = ""
    
    def accept(self, visitor):
        return visitor.visit_single_variable_designation(self)


@dataclass
class CSharpDiscardDesignation(CSharpVariableDesignation):
    """C# discard designation."""
    
    def accept(self, visitor):
        return visitor.visit_discard_designation(self)


@dataclass
class CSharpParenthesizedVariableDesignation(CSharpVariableDesignation):
    """C# parenthesized variable designation."""
    variables: List[CSharpVariableDesignation] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_parenthesized_variable_designation(self)


# LINQ Query expressions
@dataclass
class CSharpQueryExpression(CSharpExpression):
    """C# query expression."""
    from_clause: Optional['CSharpFromClause'] = None
    body: Optional['CSharpQueryBody'] = None
    
    def accept(self, visitor):
        return visitor.visit_query_expression(self)


@dataclass
class CSharpQueryBody(CSharpNode):
    """C# query body."""
    clauses: List['CSharpQueryClause'] = field(default_factory=list)
    select_or_group: Optional[Union['CSharpSelectClause', 'CSharpGroupClause']] = None
    continuation: Optional['CSharpQueryContinuation'] = None
    
    def accept(self, visitor):
        return visitor.visit_query_body(self)


@dataclass
class CSharpQueryClause(CSharpNode):
    """Base class for C# query clauses."""
    pass


@dataclass
class CSharpFromClause(CSharpQueryClause):
    """C# from clause."""
    type: Optional[CSharpType] = None
    identifier: str = ""
    expression: Optional[CSharpExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_from_clause(self)


@dataclass
class CSharpLetClause(CSharpQueryClause):
    """C# let clause."""
    identifier: str = ""
    expression: Optional[CSharpExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_let_clause(self)


@dataclass
class CSharpWhereClause(CSharpQueryClause):
    """C# where clause."""
    condition: Optional[CSharpExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_where_clause(self)


@dataclass
class CSharpJoinClause(CSharpQueryClause):
    """C# join clause."""
    type: Optional[CSharpType] = None
    identifier: str = ""
    in_expression: Optional[CSharpExpression] = None
    left_expression: Optional[CSharpExpression] = None
    right_expression: Optional[CSharpExpression] = None
    into: Optional['CSharpJoinIntoClause'] = None
    
    def accept(self, visitor):
        return visitor.visit_join_clause(self)


@dataclass
class CSharpJoinIntoClause(CSharpNode):
    """C# join into clause."""
    identifier: str = ""
    
    def accept(self, visitor):
        return visitor.visit_join_into_clause(self)


@dataclass
class CSharpOrderByClause(CSharpQueryClause):
    """C# order by clause."""
    orderings: List['CSharpOrdering'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_order_by_clause(self)


@dataclass
class CSharpOrdering(CSharpNode):
    """C# ordering."""
    expression: Optional[CSharpExpression] = None
    ascending_or_descending: Optional[str] = None  # "ascending" or "descending"
    
    def accept(self, visitor):
        return visitor.visit_ordering(self)


@dataclass
class CSharpSelectClause(CSharpNode):
    """C# select clause."""
    expression: Optional[CSharpExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_select_clause(self)


@dataclass
class CSharpGroupClause(CSharpNode):
    """C# group clause."""
    group_expression: Optional[CSharpExpression] = None
    by_expression: Optional[CSharpExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_group_clause(self)


@dataclass
class CSharpQueryContinuation(CSharpNode):
    """C# query continuation."""
    identifier: str = ""
    body: Optional[CSharpQueryBody] = None
    
    def accept(self, visitor):
        return visitor.visit_query_continuation(self)


# Visitor interface
class CSharpVisitor(ABC):
    """Abstract visitor for C# AST nodes."""
    
    # Expression visitor methods
    @abstractmethod
    def visit_literal(self, node: CSharpLiteral): pass
    
    @abstractmethod
    def visit_identifier(self, node: CSharpIdentifier): pass
    
    @abstractmethod
    def visit_qualified_name(self, node: CSharpQualifiedName): pass
    
    @abstractmethod
    def visit_generic_name(self, node: CSharpGenericName): pass
    
    @abstractmethod
    def visit_binary_expression(self, node: CSharpBinaryExpression): pass
    
    @abstractmethod
    def visit_unary_expression(self, node: CSharpUnaryExpression): pass
    
    @abstractmethod
    def visit_conditional_expression(self, node: CSharpConditionalExpression): pass
    
    @abstractmethod
    def visit_assignment_expression(self, node: CSharpAssignmentExpression): pass
    
    @abstractmethod
    def visit_invocation_expression(self, node: CSharpInvocationExpression): pass
    
    @abstractmethod
    def visit_member_access_expression(self, node: CSharpMemberAccessExpression): pass
    
    @abstractmethod
    def visit_element_access_expression(self, node: CSharpIndexerAccessExpression): pass
    
    @abstractmethod
    def visit_cast_expression(self, node: CSharpCastExpression): pass
    
    @abstractmethod
    def visit_is_expression(self, node: CSharpIsExpression): pass
    
    @abstractmethod
    def visit_as_expression(self, node: CSharpAsExpression): pass
    
    @abstractmethod
    def visit_this_expression(self, node: CSharpThisExpression): pass
    
    @abstractmethod
    def visit_base_expression(self, node: CSharpBaseExpression): pass
    
    @abstractmethod
    def visit_typeof_expression(self, node: CSharpTypeofExpression): pass
    
    @abstractmethod
    def visit_sizeof_expression(self, node: CSharpSizeofExpression): pass
    
    @abstractmethod
    def visit_nameof_expression(self, node: CSharpNameofExpression): pass
    
    @abstractmethod
    def visit_default_expression(self, node: CSharpDefaultExpression): pass
    
    @abstractmethod
    def visit_object_creation_expression(self, node: CSharpObjectCreationExpression): pass
    
    @abstractmethod
    def visit_array_creation_expression(self, node: CSharpArrayCreationExpression): pass
    
    @abstractmethod
    def visit_implicit_array_creation_expression(self, node: CSharpImplicitArrayCreationExpression): pass
    
    @abstractmethod
    def visit_anonymous_object_creation_expression(self, node: CSharpAnonymousObjectCreationExpression): pass
    
    @abstractmethod
    def visit_anonymous_object_member_declarator(self, node: CSharpAnonymousObjectMemberDeclarator): pass
    
    @abstractmethod
    def visit_initializer_expression(self, node: CSharpInitializerExpression): pass
    
    @abstractmethod
    def visit_lambda_expression(self, node: CSharpLambdaExpression): pass
    
    @abstractmethod
    def visit_anonymous_method_expression(self, node: CSharpAnonymousMethodExpression): pass
    
    @abstractmethod
    def visit_await_expression(self, node: CSharpAwaitExpression): pass
    
    @abstractmethod
    def visit_tuple_expression(self, node: CSharpTupleExpression): pass
    
    @abstractmethod
    def visit_throw_expression(self, node: CSharpThrowExpression): pass
    
    @abstractmethod
    def visit_range_expression(self, node: CSharpRangeExpression): pass
    
    @abstractmethod
    def visit_index_expression(self, node: CSharpIndexExpression): pass
    
    @abstractmethod
    def visit_switch_expression(self, node: CSharpSwitchExpression): pass
    
    @abstractmethod
    def visit_switch_expression_arm(self, node: CSharpSwitchExpressionArm): pass
    
    @abstractmethod
    def visit_with_expression(self, node: CSharpWithExpression): pass
    
    @abstractmethod
    def visit_interpolated_string_expression(self, node: CSharpInterpolatedStringExpression): pass
    
    @abstractmethod
    def visit_interpolation_expression(self, node: CSharpInterpolationExpression): pass
    
    # Statement visitor methods
    @abstractmethod
    def visit_expression_statement(self, node: CSharpExpressionStatement): pass
    
    @abstractmethod
    def visit_block(self, node: CSharpBlock): pass
    
    @abstractmethod
    def visit_if_statement(self, node: CSharpIfStatement): pass
    
    @abstractmethod
    def visit_while_statement(self, node: CSharpWhileStatement): pass
    
    @abstractmethod
    def visit_for_statement(self, node: CSharpForStatement): pass
    
    @abstractmethod
    def visit_for_each_statement(self, node: CSharpForEachStatement): pass
    
    @abstractmethod
    def visit_do_statement(self, node: CSharpDoStatement): pass
    
    @abstractmethod
    def visit_switch_statement(self, node: CSharpSwitchStatement): pass
    
    @abstractmethod
    def visit_switch_section(self, node: CSharpSwitchSection): pass
    
    @abstractmethod
    def visit_switch_label(self, node: CSharpSwitchLabel): pass
    
    @abstractmethod
    def visit_case_switch_label(self, node: CSharpCaseSwitchLabel): pass
    
    @abstractmethod
    def visit_default_switch_label(self, node: CSharpDefaultSwitchLabel): pass
    
    @abstractmethod
    def visit_case_pattern_switch_label(self, node: CSharpCasePatternSwitchLabel): pass
    
    @abstractmethod
    def visit_break_statement(self, node: CSharpBreakStatement): pass
    
    @abstractmethod
    def visit_continue_statement(self, node: CSharpContinueStatement): pass
    
    @abstractmethod
    def visit_return_statement(self, node: CSharpReturnStatement): pass
    
    @abstractmethod
    def visit_throw_statement(self, node: CSharpThrowStatement): pass
    
    @abstractmethod
    def visit_try_statement(self, node: CSharpTryStatement): pass
    
    @abstractmethod
    def visit_catch_clause(self, node: CSharpCatchClause): pass
    
    @abstractmethod
    def visit_catch_declaration(self, node: CSharpCatchDeclaration): pass
    
    @abstractmethod
    def visit_catch_filter_clause(self, node: CSharpCatchFilterClause): pass
    
    @abstractmethod
    def visit_lock_statement(self, node: CSharpLockStatement): pass
    
    @abstractmethod
    def visit_using_statement(self, node: CSharpUsingStatement): pass
    
    @abstractmethod
    def visit_yield_statement(self, node: CSharpYieldStatement): pass
    
    @abstractmethod
    def visit_empty_statement(self, node: CSharpEmptyStatement): pass
    
    @abstractmethod
    def visit_labeled_statement(self, node: CSharpLabeledStatement): pass
    
    @abstractmethod
    def visit_goto_statement(self, node: CSharpGotoStatement): pass
    
    @abstractmethod
    def visit_checked_statement(self, node: CSharpCheckedStatement): pass
    
    @abstractmethod
    def visit_unchecked_statement(self, node: CSharpUncheckedStatement): pass
    
    @abstractmethod
    def visit_unsafe_statement(self, node: CSharpUnsafeStatement): pass
    
    @abstractmethod
    def visit_fixed_statement(self, node: CSharpFixedStatement): pass
    
    @abstractmethod
    def visit_local_declaration_statement(self, node: CSharpLocalDeclarationStatement): pass
    
    # Declaration visitor methods
    @abstractmethod
    def visit_compilation_unit(self, node: CSharpCompilationUnit): pass
    
    @abstractmethod
    def visit_namespace_declaration(self, node: CSharpNamespaceDeclaration): pass
    
    @abstractmethod
    def visit_using_directive(self, node: CSharpUsingDirective): pass
    
    @abstractmethod
    def visit_extern_alias_directive(self, node: CSharpExternAliasDirective): pass
    
    @abstractmethod
    def visit_class_declaration(self, node: CSharpClassDeclaration): pass
    
    @abstractmethod
    def visit_struct_declaration(self, node: CSharpStructDeclaration): pass
    
    @abstractmethod
    def visit_interface_declaration(self, node: CSharpInterfaceDeclaration): pass
    
    @abstractmethod
    def visit_enum_declaration(self, node: CSharpEnumDeclaration): pass
    
    @abstractmethod
    def visit_enum_member_declaration(self, node: CSharpEnumMemberDeclaration): pass
    
    @abstractmethod
    def visit_delegate_declaration(self, node: CSharpDelegateDeclaration): pass
    
    @abstractmethod
    def visit_record_declaration(self, node: CSharpRecordDeclaration): pass
    
    @abstractmethod
    def visit_base_list(self, node: CSharpBaseList): pass
    
    @abstractmethod
    def visit_field_declaration(self, node: CSharpFieldDeclaration): pass
    
    @abstractmethod
    def visit_method_declaration(self, node: CSharpMethodDeclaration): pass
    
    @abstractmethod
    def visit_constructor_declaration(self, node: CSharpConstructorDeclaration): pass
    
    @abstractmethod
    def visit_constructor_initializer(self, node: CSharpConstructorInitializer): pass
    
    @abstractmethod
    def visit_destructor_declaration(self, node: CSharpDestructorDeclaration): pass
    
    @abstractmethod
    def visit_property_declaration(self, node: CSharpPropertyDeclaration): pass
    
    @abstractmethod
    def visit_indexer_declaration(self, node: CSharpIndexerDeclaration): pass
    
    @abstractmethod
    def visit_event_declaration(self, node: CSharpEventDeclaration): pass
    
    @abstractmethod
    def visit_event_field_declaration(self, node: CSharpEventFieldDeclaration): pass
    
    @abstractmethod
    def visit_operator_declaration(self, node: CSharpOperatorDeclaration): pass
    
    @abstractmethod
    def visit_conversion_operator_declaration(self, node: CSharpConversionOperatorDeclaration): pass
    
    @abstractmethod
    def visit_accessor_list(self, node: CSharpAccessorList): pass
    
    @abstractmethod
    def visit_accessor_declaration(self, node: CSharpAccessorDeclaration): pass
    
    # Type visitor methods
    @abstractmethod
    def visit_predefined_type(self, node: CSharpPredefinedType): pass
    
    @abstractmethod
    def visit_identifier_name(self, node: CSharpIdentifierName): pass
    
    @abstractmethod
    def visit_qualified_name_type(self, node: CSharpQualifiedNameType): pass
    
    @abstractmethod
    def visit_generic_name_type(self, node: CSharpGenericNameType): pass
    
    @abstractmethod
    def visit_generic_type(self, node: CSharpGenericType): pass
    
    @abstractmethod
    def visit_array_type(self, node: CSharpArrayType): pass
    
    @abstractmethod
    def visit_array_rank_specifier(self, node: CSharpArrayRankSpecifier): pass
    
    @abstractmethod
    def visit_pointer_type(self, node: CSharpPointerType): pass
    
    @abstractmethod
    def visit_nullable_type(self, node: CSharpNullableType): pass
    
    @abstractmethod
    def visit_tuple_type(self, node: CSharpTupleType): pass
    
    @abstractmethod
    def visit_tuple_element(self, node: CSharpTupleElement): pass
    
    @abstractmethod
    def visit_function_pointer_type(self, node: CSharpFunctionPointerType): pass
    
    @abstractmethod
    def visit_scoped_type(self, node: CSharpScopedType): pass
    
    # Parameter and argument visitor methods
    @abstractmethod
    def visit_parameter_list(self, node: CSharpParameterList): pass
    
    @abstractmethod
    def visit_bracketed_parameter_list(self, node: CSharpBracketedParameterList): pass
    
    @abstractmethod
    def visit_function_pointer_parameter_list(self, node: CSharpFunctionPointerParameterList): pass
    
    @abstractmethod
    def visit_parameter(self, node: CSharpParameter): pass
    
    @abstractmethod
    def visit_function_pointer_parameter(self, node: CSharpFunctionPointerParameter): pass
    
    @abstractmethod
    def visit_argument(self, node: CSharpArgument): pass
    
    @abstractmethod
    def visit_argument_list(self, node: CSharpArgumentList): pass
    
    @abstractmethod
    def visit_bracketed_argument_list(self, node: CSharpBracketedArgumentList): pass
    
    # Generic type visitor methods
    @abstractmethod
    def visit_type_parameter_list(self, node: CSharpTypeParameterList): pass
    
    @abstractmethod
    def visit_type_parameter(self, node: CSharpTypeParameter): pass
    
    @abstractmethod
    def visit_type_argument_list(self, node: CSharpTypeArgumentList): pass
    
    @abstractmethod
    def visit_type_parameter_constraint_clause(self, node: CSharpTypeParameterConstraintClause): pass
    
    @abstractmethod
    def visit_class_or_struct_constraint(self, node: CSharpClassOrStructConstraint): pass
    
    @abstractmethod
    def visit_type_constraint(self, node: CSharpTypeConstraint): pass
    
    @abstractmethod
    def visit_constructor_constraint(self, node: CSharpConstructorConstraint): pass
    
    @abstractmethod
    def visit_default_constraint(self, node: CSharpDefaultConstraint): pass
    
    # Attribute visitor methods
    @abstractmethod
    def visit_attribute_list(self, node: CSharpAttributeList): pass
    
    @abstractmethod
    def visit_attribute(self, node: CSharpAttribute): pass
    
    @abstractmethod
    def visit_attribute_argument_list(self, node: CSharpAttributeArgumentList): pass
    
    @abstractmethod
    def visit_attribute_argument(self, node: CSharpAttributeArgument): pass
    
    # Variable declaration visitor methods
    @abstractmethod
    def visit_variable_declaration(self, node: CSharpVariableDeclaration): pass
    
    @abstractmethod
    def visit_variable_declarator(self, node: CSharpVariableDeclarator): pass
    
    @abstractmethod
    def visit_equals_value_clause(self, node: CSharpEqualsValueClause): pass
    
    # Pattern visitor methods
    @abstractmethod
    def visit_constant_pattern(self, node: CSharpConstantPattern): pass
    
    @abstractmethod
    def visit_declaration_pattern(self, node: CSharpDeclarationPattern): pass
    
    @abstractmethod
    def visit_type_pattern(self, node: CSharpTypePattern): pass
    
    @abstractmethod
    def visit_var_pattern(self, node: CSharpVarPattern): pass
    
    @abstractmethod
    def visit_discard_pattern(self, node: CSharpDiscardPattern): pass
    
    @abstractmethod
    def visit_tuple_pattern(self, node: CSharpTuplePattern): pass
    
    @abstractmethod
    def visit_positional_pattern(self, node: CSharpPositionalPattern): pass
    
    @abstractmethod
    def visit_property_pattern(self, node: CSharpPropertyPattern): pass
    
    @abstractmethod
    def visit_relational_pattern(self, node: CSharpRelationalPattern): pass
    
    @abstractmethod
    def visit_logical_pattern(self, node: CSharpLogicalPattern): pass
    
    @abstractmethod
    def visit_list_pattern(self, node: CSharpListPattern): pass
    
    @abstractmethod
    def visit_subpattern(self, node: CSharpSubpattern): pass
    
    # Variable designation visitor methods
    @abstractmethod
    def visit_single_variable_designation(self, node: CSharpSingleVariableDesignation): pass
    
    @abstractmethod
    def visit_discard_designation(self, node: CSharpDiscardDesignation): pass
    
    @abstractmethod
    def visit_parenthesized_variable_designation(self, node: CSharpParenthesizedVariableDesignation): pass
    
    # LINQ query visitor methods
    @abstractmethod
    def visit_query_expression(self, node: CSharpQueryExpression): pass
    
    @abstractmethod
    def visit_query_body(self, node: CSharpQueryBody): pass
    
    @abstractmethod
    def visit_from_clause(self, node: CSharpFromClause): pass
    
    @abstractmethod
    def visit_let_clause(self, node: CSharpLetClause): pass
    
    @abstractmethod
    def visit_where_clause(self, node: CSharpWhereClause): pass
    
    @abstractmethod
    def visit_join_clause(self, node: CSharpJoinClause): pass
    
    @abstractmethod
    def visit_join_into_clause(self, node: CSharpJoinIntoClause): pass
    
    @abstractmethod
    def visit_order_by_clause(self, node: CSharpOrderByClause): pass
    
    @abstractmethod
    def visit_ordering(self, node: CSharpOrdering): pass
    
    @abstractmethod
    def visit_select_clause(self, node: CSharpSelectClause): pass
    
    @abstractmethod
    def visit_group_clause(self, node: CSharpGroupClause): pass
    
    @abstractmethod
    def visit_query_continuation(self, node: CSharpQueryContinuation): pass


# Utility functions
def create_simple_identifier(name: str) -> CSharpIdentifier:
    """Create a simple identifier node."""
    return CSharpIdentifier(CSharpNodeType.IDENTIFIER, name=name)


def create_literal(value: Any, literal_type: str) -> CSharpLiteral:
    """Create a literal node."""
    return CSharpLiteral(CSharpNodeType.LITERAL, value=value, literal_type=literal_type)


def create_binary_expression(left: Optional[CSharpExpression] = None, operator: Optional[CSharpOperator] = None, 
                            right: Optional[CSharpExpression] = None) -> CSharpBinaryExpression:
    """Create a binary expression node."""
    return CSharpBinaryExpression(
        CSharpNodeType.BINARY_EXPRESSION,
        left=left,
        operator=operator,
        right=right
    )


def create_method_declaration(name: str, return_type: Optional[CSharpType] = None, 
                            parameters: Optional[List[CSharpParameter]] = None,
                            modifiers: Optional[List[CSharpModifier]] = None) -> CSharpMethodDeclaration:
    """Create a method declaration node."""
    return CSharpMethodDeclaration(
        CSharpNodeType.METHOD_DECLARATION,
        attributes=[],
        modifiers=modifiers or [],
        return_type=return_type,
        identifier=name,
        parameter_list=CSharpParameterList(
            CSharpNodeType.PARAMETER_LIST,
            parameters=parameters or []
        ) if parameters else None
    )


def create_class_declaration(name: str, members: Optional[List[CSharpMemberDeclaration]] = None,
                           modifiers: Optional[List[CSharpModifier]] = None) -> CSharpClassDeclaration:
    """Create a class declaration node."""
    return CSharpClassDeclaration(
        CSharpNodeType.CLASS_DECLARATION,
        attributes=[],
        modifiers=modifiers or [],
        identifier=name,
        members=members or []
    )