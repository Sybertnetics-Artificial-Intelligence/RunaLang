#!/usr/bin/env python3
"""
Java AST Node Definitions

Comprehensive Abstract Syntax Tree nodes for Java covering
all language features from Java 8 through Java 21 including
lambdas, streams, modules, pattern matching, and modern Java constructs.
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod


class JavaNodeType(Enum):
    """Java AST node types."""
    # Literals
    LITERAL = auto()
    INTEGER_LITERAL = auto()
    FLOATING_LITERAL = auto()
    STRING_LITERAL = auto()
    CHARACTER_LITERAL = auto()
    BOOLEAN_LITERAL = auto()
    NULL_LITERAL = auto()
    TEXT_BLOCK = auto()  # Java 15
    
    # Identifiers and names
    IDENTIFIER = auto()
    QUALIFIED_NAME = auto()
    SIMPLE_NAME = auto()
    
    # Expressions
    BINARY_EXPRESSION = auto()
    UNARY_EXPRESSION = auto()
    CONDITIONAL_EXPRESSION = auto()
    ASSIGNMENT_EXPRESSION = auto()
    METHOD_INVOCATION = auto()
    FIELD_ACCESS = auto()
    ARRAY_ACCESS = auto()
    CAST_EXPRESSION = auto()
    INSTANCEOF_EXPRESSION = auto()
    THIS_EXPRESSION = auto()
    SUPER_EXPRESSION = auto()
    CLASS_LITERAL = auto()
    ARRAY_CREATION = auto()
    ARRAY_INITIALIZER = auto()
    LAMBDA_EXPRESSION = auto()  # Java 8
    METHOD_REFERENCE = auto()  # Java 8
    
    # Statements
    EXPRESSION_STATEMENT = auto()
    BLOCK_STATEMENT = auto()
    IF_STATEMENT = auto()
    WHILE_STATEMENT = auto()
    FOR_STATEMENT = auto()
    ENHANCED_FOR_STATEMENT = auto()  # for-each
    DO_STATEMENT = auto()
    SWITCH_STATEMENT = auto()
    SWITCH_EXPRESSION = auto()  # Java 14
    BREAK_STATEMENT = auto()
    CONTINUE_STATEMENT = auto()
    RETURN_STATEMENT = auto()
    THROW_STATEMENT = auto()
    TRY_STATEMENT = auto()
    SYNCHRONIZED_STATEMENT = auto()
    ASSERT_STATEMENT = auto()
    EMPTY_STATEMENT = auto()
    LABELED_STATEMENT = auto()
    YIELD_STATEMENT = auto()  # Java 14
    
    # Declarations
    COMPILATION_UNIT = auto()
    PACKAGE_DECLARATION = auto()
    IMPORT_DECLARATION = auto()
    CLASS_DECLARATION = auto()
    INTERFACE_DECLARATION = auto()
    ENUM_DECLARATION = auto()
    ANNOTATION_DECLARATION = auto()
    RECORD_DECLARATION = auto()  # Java 14
    FIELD_DECLARATION = auto()
    METHOD_DECLARATION = auto()
    CONSTRUCTOR_DECLARATION = auto()
    VARIABLE_DECLARATION = auto()
    LOCAL_VARIABLE_DECLARATION = auto()
    PARAMETER_DECLARATION = auto()
    TYPE_PARAMETER = auto()
    
    # Types
    PRIMITIVE_TYPE = auto()
    ARRAY_TYPE = auto()
    PARAMETERIZED_TYPE = auto()  # Generics
    WILDCARD_TYPE = auto()
    UNION_TYPE = auto()  # Multi-catch
    INTERSECTION_TYPE = auto()
    VAR_TYPE = auto()  # Java 10
    
    # Annotations
    ANNOTATION = auto()
    NORMAL_ANNOTATION = auto()
    MARKER_ANNOTATION = auto()
    SINGLE_MEMBER_ANNOTATION = auto()
    
    # Modifiers
    MODIFIER = auto()
    
    # Other constructs
    CATCH_CLAUSE = auto()
    SWITCH_CASE = auto()
    ENUM_CONSTANT = auto()
    ANONYMOUS_CLASS_DECLARATION = auto()
    DIMENSION = auto()
    JAVADOC = auto()
    
    # Pattern matching (Java 17+)
    PATTERN = auto()
    TYPE_PATTERN = auto()
    GUARDED_PATTERN = auto()
    
    # Modules (Java 9)
    MODULE_DECLARATION = auto()
    REQUIRES_DIRECTIVE = auto()
    EXPORTS_DIRECTIVE = auto()
    OPENS_DIRECTIVE = auto()
    USES_DIRECTIVE = auto()
    PROVIDES_DIRECTIVE = auto()


class JavaOperator(Enum):
    """Java operators."""
    # Arithmetic
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    MODULO = "%"
    
    # Bitwise
    BIT_AND = "&"
    BIT_OR = "|"
    BIT_XOR = "^"
    BIT_NOT = "~"
    LEFT_SHIFT = "<<"
    RIGHT_SHIFT = ">>"
    UNSIGNED_RIGHT_SHIFT = ">>>"
    
    # Logical
    LOGICAL_AND = "&&"
    LOGICAL_OR = "||"
    LOGICAL_NOT = "!"
    
    # Comparison
    EQUAL = "=="
    NOT_EQUAL = "!="
    LESS_THAN = "<"
    LESS_EQUAL = "<="
    GREATER_THAN = ">"
    GREATER_EQUAL = ">="
    
    # Assignment
    ASSIGN = "="
    PLUS_ASSIGN = "+="
    MINUS_ASSIGN = "-="
    MULTIPLY_ASSIGN = "*="
    DIVIDE_ASSIGN = "/="
    MODULO_ASSIGN = "%="
    BIT_AND_ASSIGN = "&="
    BIT_OR_ASSIGN = "|="
    BIT_XOR_ASSIGN = "^="
    LEFT_SHIFT_ASSIGN = "<<="
    RIGHT_SHIFT_ASSIGN = ">>="
    UNSIGNED_RIGHT_SHIFT_ASSIGN = ">>>="
    
    # Unary
    PRE_INCREMENT = "++pre"
    POST_INCREMENT = "post++"
    PRE_DECREMENT = "--pre"
    POST_DECREMENT = "post--"
    UNARY_PLUS = "+"
    UNARY_MINUS = "-"
    
    # Special
    INSTANCEOF = "instanceof"
    CONDITIONAL = "?:"


class JavaModifier(Enum):
    """Java modifiers."""
    PUBLIC = "public"
    PRIVATE = "private"
    PROTECTED = "protected"
    STATIC = "static"
    FINAL = "final"
    ABSTRACT = "abstract"
    SYNCHRONIZED = "synchronized"
    NATIVE = "native"
    TRANSIENT = "transient"
    VOLATILE = "volatile"
    STRICTFP = "strictfp"
    DEFAULT = "default"  # Interface default methods
    SEALED = "sealed"  # Java 17
    NON_SEALED = "non-sealed"  # Java 17


@dataclass
class JavaNode(ABC):
    """Base class for all Java AST nodes."""
    type: JavaNodeType = None
    source_range: Optional[Dict[str, int]] = None
    
    # Code representation for source code preservation
    source_code: str = ""  # Original source code for this node
    formatted_code: str = ""  # Formatted/pretty-printed code
    
    @abstractmethod
    def accept(self, visitor):
        """Accept a visitor for the visitor pattern."""
        pass
    
    def get_source_code(self) -> str:
        """Get the original source code for this node."""
        return self.source_code
    
    def set_source_code(self, code: str):
        """Set the original source code for this node."""
        self.source_code = code
    
    def get_formatted_code(self) -> str:
        """Get the formatted code for this node."""
        return self.formatted_code
    
    def set_formatted_code(self, code: str):
        """Set the formatted code for this node."""
        self.formatted_code = code


@dataclass
class JavaExpression(JavaNode):
    """Base class for Java expressions."""
    pass


@dataclass
class JavaStatement(JavaNode):
    """Base class for Java statements."""
    pass


@dataclass
class JavaDeclaration(JavaNode):
    """Base class for Java declarations."""
    modifiers: List[JavaModifier] = field(default_factory=list)
    annotations: List['JavaAnnotation'] = field(default_factory=list)


@dataclass
class JavaType(JavaNode):
    """Base class for Java types."""
    pass


# Literal nodes
@dataclass
class JavaLiteral(JavaExpression):
    """Base class for Java literals."""
    value: Any = None


@dataclass
class JavaIntegerLiteral(JavaLiteral):
    """Java integer literal."""
    
    def __post_init__(self):
        self.type = JavaNodeType.INTEGER_LITERAL
    
    def accept(self, visitor):
        return visitor.visit_integer_literal(self)


@dataclass
class JavaFloatingLiteral(JavaLiteral):
    """Java floating point literal."""
    
    def __post_init__(self):
        self.type = JavaNodeType.FLOATING_LITERAL
    
    def accept(self, visitor):
        return visitor.visit_floating_literal(self)


@dataclass
class JavaStringLiteral(JavaLiteral):
    """Java string literal."""
    
    def __post_init__(self):
        self.type = JavaNodeType.STRING_LITERAL
    
    def accept(self, visitor):
        return visitor.visit_string_literal(self)


@dataclass
class JavaCharacterLiteral(JavaLiteral):
    """Java character literal."""
    
    def __post_init__(self):
        self.type = JavaNodeType.CHARACTER_LITERAL
    
    def accept(self, visitor):
        return visitor.visit_character_literal(self)


@dataclass
class JavaBooleanLiteral(JavaLiteral):
    """Java boolean literal."""
    
    def __post_init__(self):
        self.type = JavaNodeType.BOOLEAN_LITERAL
    
    def accept(self, visitor):
        return visitor.visit_boolean_literal(self)


@dataclass
class JavaNullLiteral(JavaLiteral):
    """Java null literal."""
    
    def __post_init__(self):
        self.type = JavaNodeType.NULL_LITERAL
        self.value = None
    
    def accept(self, visitor):
        return visitor.visit_null_literal(self)


@dataclass
class JavaTextBlock(JavaLiteral):
    """Java text block literal (Java 15)."""
    
    def __post_init__(self):
        self.type = JavaNodeType.TEXT_BLOCK
    
    def accept(self, visitor):
        return visitor.visit_text_block(self)


# Name nodes
@dataclass
class JavaSimpleName(JavaExpression):
    """Java simple name."""
    identifier: str = ""
    
    def __post_init__(self):
        self.type = JavaNodeType.SIMPLE_NAME
    
    def accept(self, visitor):
        return visitor.visit_simple_name(self)


@dataclass
class JavaQualifiedName(JavaExpression):
    """Java qualified name."""
    qualifier: JavaExpression = None
    name: 'JavaSimpleName' = None
    
    def __post_init__(self):
        self.type = JavaNodeType.QUALIFIED_NAME
    
    def accept(self, visitor):
        return visitor.visit_qualified_name(self)


# Expression nodes
@dataclass
class JavaBinaryExpression(JavaExpression):
    """Java binary expression."""
    left: JavaExpression = None
    operator: JavaOperator = None
    right: JavaExpression = None
    
    def __post_init__(self):
        self.type = JavaNodeType.BINARY_EXPRESSION
    
    def accept(self, visitor):
        return visitor.visit_binary_expression(self)


@dataclass
class JavaUnaryExpression(JavaExpression):
    """Java unary expression."""
    operator: JavaOperator = None
    operand: JavaExpression = None
    is_postfix: bool = False
    
    def __post_init__(self):
        self.type = JavaNodeType.UNARY_EXPRESSION
    
    def accept(self, visitor):
        return visitor.visit_unary_expression(self)


@dataclass
class JavaConditionalExpression(JavaExpression):
    """Java conditional expression (ternary operator)."""
    condition: JavaExpression = None
    then_expression: JavaExpression = None
    else_expression: JavaExpression = None
    
    def __post_init__(self):
        self.type = JavaNodeType.CONDITIONAL_EXPRESSION
    
    def accept(self, visitor):
        return visitor.visit_conditional_expression(self)


@dataclass
class JavaAssignmentExpression(JavaExpression):
    """Java assignment expression."""
    left: JavaExpression = None
    operator: JavaOperator = None
    right: JavaExpression = None
    
    def __post_init__(self):
        self.type = JavaNodeType.ASSIGNMENT_EXPRESSION
    
    def accept(self, visitor):
        return visitor.visit_assignment_expression(self)


@dataclass
class JavaMethodInvocation(JavaExpression):
    """Java method invocation."""
    expression: Optional[JavaExpression] = None  # Object or class
    method_name: str = ""
    type_arguments: List[JavaType] = field(default_factory=list)
    arguments: List[JavaExpression] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = JavaNodeType.METHOD_INVOCATION
    
    def accept(self, visitor):
        return visitor.visit_method_invocation(self)


@dataclass
class JavaFieldAccess(JavaExpression):
    """Java field access."""
    expression: JavaExpression = None
    field_name: str = ""
    
    def __post_init__(self):
        self.type = JavaNodeType.FIELD_ACCESS
    
    def accept(self, visitor):
        return visitor.visit_field_access(self)


@dataclass
class JavaArrayAccess(JavaExpression):
    """Java array access."""
    array: JavaExpression = None
    index: JavaExpression = None
    
    def __post_init__(self):
        self.type = JavaNodeType.ARRAY_ACCESS
    
    def accept(self, visitor):
        return visitor.visit_array_access(self)


@dataclass
class JavaCastExpression(JavaExpression):
    """Java cast expression."""
    target_type: JavaType = None
    expression: JavaExpression = None
    
    def __post_init__(self):
        self.type = JavaNodeType.CAST_EXPRESSION
    
    def accept(self, visitor):
        return visitor.visit_cast_expression(self)


@dataclass
class JavaInstanceofExpression(JavaExpression):
    """Java instanceof expression."""
    expression: JavaExpression = None
    target_type: JavaType = None
    
    def __post_init__(self):
        self.type = JavaNodeType.INSTANCEOF_EXPRESSION
    
    def accept(self, visitor):
        return visitor.visit_instanceof_expression(self)


@dataclass
class JavaThisExpression(JavaExpression):
    """Java this expression."""
    qualifier: Optional[JavaExpression] = None
    
    def __post_init__(self):
        self.type = JavaNodeType.THIS_EXPRESSION
    
    def accept(self, visitor):
        return visitor.visit_this_expression(self)


@dataclass
class JavaSuperExpression(JavaExpression):
    """Java super expression."""
    qualifier: Optional[JavaExpression] = None
    
    def __post_init__(self):
        self.type = JavaNodeType.SUPER_EXPRESSION
    
    def accept(self, visitor):
        return visitor.visit_super_expression(self)


@dataclass
class JavaClassLiteral(JavaExpression):
    """Java class literal (e.g., String.class)."""
    target_type: JavaType = None
    
    def __post_init__(self):
        self.type = JavaNodeType.CLASS_LITERAL
    
    def accept(self, visitor):
        return visitor.visit_class_literal(self)


@dataclass
class JavaArrayCreation(JavaExpression):
    """Java array creation expression."""
    element_type: JavaType = None
    dimensions: List['JavaDimension'] = field(default_factory=list)
    initializer: Optional['JavaArrayInitializer'] = None
    
    def __post_init__(self):
        self.type = JavaNodeType.ARRAY_CREATION
    
    def accept(self, visitor):
        return visitor.visit_array_creation(self)


@dataclass
class JavaArrayInitializer(JavaExpression):
    """Java array initializer."""
    expressions: List[JavaExpression] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = JavaNodeType.ARRAY_INITIALIZER
    
    def accept(self, visitor):
        return visitor.visit_array_initializer(self)


@dataclass
class JavaLambdaExpression(JavaExpression):
    """Java lambda expression (Java 8)."""
    parameters: List['JavaParameter'] = field(default_factory=list)
    body: Union[JavaExpression, 'JavaBlockStatement'] = None
    
    def __post_init__(self):
        self.type = JavaNodeType.LAMBDA_EXPRESSION
    
    def accept(self, visitor):
        return visitor.visit_lambda_expression(self)


@dataclass
class JavaMethodReference(JavaExpression):
    """Java method reference (Java 8)."""
    expression: Optional[JavaExpression] = None
    method_name: str = ""
    type_arguments: List[JavaType] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = JavaNodeType.METHOD_REFERENCE
    
    def accept(self, visitor):
        return visitor.visit_method_reference(self)


# Statement nodes
@dataclass
class JavaExpressionStatement(JavaStatement):
    """Java expression statement."""
    expression: JavaExpression = None
    
    def __post_init__(self):
        self.type = JavaNodeType.EXPRESSION_STATEMENT
    
    def accept(self, visitor):
        return visitor.visit_expression_statement(self)


@dataclass
class JavaBlockStatement(JavaStatement):
    """Java block statement."""
    statements: List[JavaStatement] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = JavaNodeType.BLOCK_STATEMENT
    
    def accept(self, visitor):
        return visitor.visit_block_statement(self)


@dataclass
class JavaIfStatement(JavaStatement):
    """Java if statement."""
    condition: JavaExpression = None
    then_statement: JavaStatement = None
    else_statement: Optional[JavaStatement] = None
    
    def __post_init__(self):
        self.type = JavaNodeType.IF_STATEMENT
    
    def accept(self, visitor):
        return visitor.visit_if_statement(self)


@dataclass
class JavaWhileStatement(JavaStatement):
    """Java while statement."""
    condition: JavaExpression = None
    body: JavaStatement = None
    
    def __post_init__(self):
        self.type = JavaNodeType.WHILE_STATEMENT
    
    def accept(self, visitor):
        return visitor.visit_while_statement(self)


@dataclass
class JavaForStatement(JavaStatement):
    """Java for statement."""
    initializers: List[JavaExpression] = field(default_factory=list)
    condition: Optional[JavaExpression] = None
    updaters: List[JavaExpression] = field(default_factory=list)
    body: JavaStatement = None
    
    def __post_init__(self):
        self.type = JavaNodeType.FOR_STATEMENT
    
    def accept(self, visitor):
        return visitor.visit_for_statement(self)


@dataclass
class JavaEnhancedForStatement(JavaStatement):
    """Java enhanced for statement (for-each)."""
    parameter: 'JavaSingleVariableDeclaration' = None
    expression: JavaExpression = None
    body: JavaStatement = None
    
    def __post_init__(self):
        self.type = JavaNodeType.ENHANCED_FOR_STATEMENT
    
    def accept(self, visitor):
        return visitor.visit_enhanced_for_statement(self)


@dataclass
class JavaDoStatement(JavaStatement):
    """Java do-while statement."""
    body: JavaStatement = None
    condition: JavaExpression = None
    
    def __post_init__(self):
        self.type = JavaNodeType.DO_STATEMENT
    
    def accept(self, visitor):
        return visitor.visit_do_statement(self)


@dataclass
class JavaSwitchStatement(JavaStatement):
    """Java switch statement."""
    expression: JavaExpression = None
    statements: List[JavaStatement] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = JavaNodeType.SWITCH_STATEMENT
    
    def accept(self, visitor):
        return visitor.visit_switch_statement(self)


@dataclass
class JavaSwitchExpression(JavaExpression):
    """Java switch expression (Java 14)."""
    expression: JavaExpression = None
    statements: List[JavaStatement] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = JavaNodeType.SWITCH_EXPRESSION
    
    def accept(self, visitor):
        return visitor.visit_switch_expression(self)


@dataclass
class JavaBreakStatement(JavaStatement):
    """Java break statement."""
    label: Optional[str] = None
    
    def __post_init__(self):
        self.type = JavaNodeType.BREAK_STATEMENT
    
    def accept(self, visitor):
        return visitor.visit_break_statement(self)


@dataclass
class JavaContinueStatement(JavaStatement):
    """Java continue statement."""
    label: Optional[str] = None
    
    def __post_init__(self):
        self.type = JavaNodeType.CONTINUE_STATEMENT
    
    def accept(self, visitor):
        return visitor.visit_continue_statement(self)


@dataclass
class JavaReturnStatement(JavaStatement):
    """Java return statement."""
    expression: Optional[JavaExpression] = None
    
    def __post_init__(self):
        self.type = JavaNodeType.RETURN_STATEMENT
    
    def accept(self, visitor):
        return visitor.visit_return_statement(self)


@dataclass
class JavaThrowStatement(JavaStatement):
    """Java throw statement."""
    expression: Optional[JavaExpression] = None
    
    def __post_init__(self):
        self.type = JavaNodeType.THROW_STATEMENT
    
    def accept(self, visitor):
        return visitor.visit_throw_statement(self)


@dataclass
class JavaTryStatement(JavaStatement):
    """Java try statement."""
    body: Optional[JavaBlockStatement] = None
    resources: List['JavaVariableDeclaration'] = field(default_factory=list)  # Try-with-resources
    catch_clauses: List['JavaCatchClause'] = field(default_factory=list)
    finally_block: Optional[JavaBlockStatement] = None
    
    def __post_init__(self):
        self.type = JavaNodeType.TRY_STATEMENT
    
    def accept(self, visitor):
        return visitor.visit_try_statement(self)


@dataclass
class JavaSynchronizedStatement(JavaStatement):
    """Java synchronized statement."""
    expression: Optional[JavaExpression] = None
    body: Optional[JavaBlockStatement] = None
    
    def __post_init__(self):
        self.type = JavaNodeType.SYNCHRONIZED_STATEMENT
    
    def accept(self, visitor):
        return visitor.visit_synchronized_statement(self)


@dataclass
class JavaAssertStatement(JavaStatement):
    """Java assert statement."""
    condition: Optional[JavaExpression] = None
    message: Optional[JavaExpression] = None
    
    def __post_init__(self):
        self.type = JavaNodeType.ASSERT_STATEMENT
    
    def accept(self, visitor):
        return visitor.visit_assert_statement(self)


@dataclass
class JavaEmptyStatement(JavaStatement):
    """Java empty statement."""
    
    def __post_init__(self):
        self.type = JavaNodeType.EMPTY_STATEMENT
    
    def accept(self, visitor):
        return visitor.visit_empty_statement(self)


@dataclass
class JavaLabeledStatement(JavaStatement):
    """Java labeled statement."""
    label: Optional[str] = None
    body: Optional[JavaStatement] = None
    
    def __post_init__(self):
        self.type = JavaNodeType.LABELED_STATEMENT
    
    def accept(self, visitor):
        return visitor.visit_labeled_statement(self)


@dataclass
class JavaYieldStatement(JavaStatement):
    """Java yield statement (Java 14)."""
    expression: Optional[JavaExpression] = None
    
    def __post_init__(self):
        self.type = JavaNodeType.YIELD_STATEMENT
    
    def accept(self, visitor):
        return visitor.visit_yield_statement(self)


# Declaration nodes
@dataclass
class JavaCompilationUnit(JavaNode):
    """Java compilation unit (source file)."""
    package_declaration: Optional['JavaPackageDeclaration'] = None
    import_declarations: List['JavaImportDeclaration'] = field(default_factory=list)
    type_declarations: List[JavaDeclaration] = field(default_factory=list)
    module_declaration: Optional['JavaModuleDeclaration'] = None
    
    def __post_init__(self):
        self.type = JavaNodeType.COMPILATION_UNIT
    
    def accept(self, visitor):
        return visitor.visit_compilation_unit(self)


@dataclass
class JavaPackageDeclaration(JavaDeclaration):
    """Java package declaration."""
    name: Optional[JavaExpression] = None
    
    def __post_init__(self):
        self.type = JavaNodeType.PACKAGE_DECLARATION
    
    def accept(self, visitor):
        return visitor.visit_package_declaration(self)


@dataclass
class JavaImportDeclaration(JavaDeclaration):
    """Java import declaration."""
    name: Optional[JavaExpression] = None
    is_static: bool = False
    is_on_demand: bool = False  # import foo.*;
    
    def __post_init__(self):
        self.type = JavaNodeType.IMPORT_DECLARATION
    
    def accept(self, visitor):
        return visitor.visit_import_declaration(self)


@dataclass
class JavaTypeDeclaration(JavaDeclaration):
    """Base class for Java type declarations."""
    name: Optional[str] = None
    type_parameters: List['JavaTypeParameter'] = field(default_factory=list)
    body_declarations: List[JavaDeclaration] = field(default_factory=list)


@dataclass
class JavaClassDeclaration(JavaTypeDeclaration):
    """Java class declaration."""
    superclass: Optional[JavaType] = None
    super_interfaces: List[JavaType] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = JavaNodeType.CLASS_DECLARATION
    
    def accept(self, visitor):
        return visitor.visit_class_declaration(self)


@dataclass
class JavaInterfaceDeclaration(JavaTypeDeclaration):
    """Java interface declaration."""
    extended_interfaces: List[JavaType] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = JavaNodeType.INTERFACE_DECLARATION
    
    def accept(self, visitor):
        return visitor.visit_interface_declaration(self)


@dataclass
class JavaEnumDeclaration(JavaTypeDeclaration):
    """Java enum declaration."""
    super_interfaces: List[JavaType] = field(default_factory=list)
    enum_constants: List['JavaEnumConstant'] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = JavaNodeType.ENUM_DECLARATION
    
    def accept(self, visitor):
        return visitor.visit_enum_declaration(self)


@dataclass
class JavaAnnotationDeclaration(JavaTypeDeclaration):
    """Java annotation declaration."""
    
    def __post_init__(self):
        self.type = JavaNodeType.ANNOTATION_DECLARATION
    
    def accept(self, visitor):
        return visitor.visit_annotation_declaration(self)


@dataclass
class JavaRecordDeclaration(JavaTypeDeclaration):
    """Java record declaration (Java 14)."""
    parameters: List['JavaParameter'] = field(default_factory=list)
    super_interfaces: List[JavaType] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = JavaNodeType.RECORD_DECLARATION
    
    def accept(self, visitor):
        return visitor.visit_record_declaration(self)


@dataclass
class JavaFieldDeclaration(JavaDeclaration):
    """Java field declaration."""
    variable_type: JavaType = None
    fragments: List['JavaVariableDeclarationFragment'] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = JavaNodeType.FIELD_DECLARATION
    
    def accept(self, visitor):
        return visitor.visit_field_declaration(self)


@dataclass
class JavaMethodDeclaration(JavaDeclaration):
    """Java method declaration."""
    name: str = ""
    return_type: Optional[JavaType] = None  # None for constructors
    type_parameters: List['JavaTypeParameter'] = field(default_factory=list)
    parameters: List['JavaParameter'] = field(default_factory=list)
    thrown_exceptions: List[JavaType] = field(default_factory=list)
    body: Optional[JavaBlockStatement] = None
    is_constructor: bool = False
    is_compact_constructor: bool = False  # Records
    
    def __post_init__(self):
        self.type = JavaNodeType.METHOD_DECLARATION
    
    def accept(self, visitor):
        return visitor.visit_method_declaration(self)


@dataclass
class JavaVariableDeclaration(JavaDeclaration):
    """Java variable declaration."""
    variable_type: JavaType = None
    fragments: List['JavaVariableDeclarationFragment'] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = JavaNodeType.VARIABLE_DECLARATION
    
    def accept(self, visitor):
        return visitor.visit_variable_declaration(self)


@dataclass
class JavaVariableDeclarationFragment(JavaNode):
    """Java variable declaration fragment."""
    name: Optional[str] = None
    extra_dimensions: int = 0
    initializer: Optional[JavaExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_variable_declaration_fragment(self)


@dataclass
class JavaSingleVariableDeclaration(JavaDeclaration):
    """Java single variable declaration (for parameters, catch clauses, etc.)."""
    variable_type: JavaType = None
    name: str = ""
    extra_dimensions: int = 0
    initializer: Optional[JavaExpression] = None
    is_varargs: bool = False
    
    def __post_init__(self):
        self.type = JavaNodeType.PARAMETER_DECLARATION
    
    def accept(self, visitor):
        return visitor.visit_single_variable_declaration(self)


@dataclass
class JavaParameter(JavaNode):
    """Java parameter."""
    modifiers: List[JavaModifier] = field(default_factory=list)
    annotations: List['JavaAnnotation'] = field(default_factory=list)
    parameter_type: JavaType = None
    name: str = ""
    is_varargs: bool = False
    
    def accept(self, visitor):
        return visitor.visit_parameter(self)


@dataclass
class JavaTypeParameter(JavaNode):
    """Java type parameter."""
    name: str = ""
    bounds: List[JavaType] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = JavaNodeType.TYPE_PARAMETER
    
    def accept(self, visitor):
        return visitor.visit_type_parameter(self)


# Type nodes
@dataclass
class JavaPrimitiveType(JavaType):
    """Java primitive type."""
    primitive_type: str = ""  # boolean, byte, char, double, float, int, long, short
    
    def __post_init__(self):
        self.type = JavaNodeType.PRIMITIVE_TYPE
    
    def accept(self, visitor):
        return visitor.visit_primitive_type(self)


@dataclass
class JavaArrayType(JavaType):
    """Java array type."""
    component_type: JavaType = None
    dimensions: List['JavaDimension'] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = JavaNodeType.ARRAY_TYPE
    
    def accept(self, visitor):
        return visitor.visit_array_type(self)


@dataclass
class JavaParameterizedType(JavaType):
    """Java parameterized type (generics)."""
    raw_type: JavaType = None
    type_arguments: List[JavaType] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = JavaNodeType.PARAMETERIZED_TYPE
    
    def accept(self, visitor):
        return visitor.visit_parameterized_type(self)


@dataclass
class JavaWildcardType(JavaType):
    """Java wildcard type."""
    bound: Optional[JavaType] = None
    is_upper_bound: bool = True  # ? extends vs ? super
    
    def __post_init__(self):
        self.type = JavaNodeType.WILDCARD_TYPE
    
    def accept(self, visitor):
        return visitor.visit_wildcard_type(self)


@dataclass
class JavaUnionType(JavaType):
    """Java union type (multi-catch)."""
    types: List[JavaType] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = JavaNodeType.UNION_TYPE
    
    def accept(self, visitor):
        return visitor.visit_union_type(self)


@dataclass
class JavaIntersectionType(JavaType):
    """Java intersection type."""
    types: List[JavaType] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = JavaNodeType.INTERSECTION_TYPE
    
    def accept(self, visitor):
        return visitor.visit_intersection_type(self)


@dataclass
class JavaVarType(JavaType):
    """Java var type (Java 10)."""
    
    def __post_init__(self):
        self.type = JavaNodeType.VAR_TYPE
    
    def accept(self, visitor):
        return visitor.visit_var_type(self)


# Helper nodes
@dataclass
class JavaAnnotation(JavaNode):
    """Java annotation."""
    type_name: Optional[JavaExpression] = None
    
    def __post_init__(self):
        self.type = JavaNodeType.ANNOTATION
    
    def accept(self, visitor):
        return visitor.visit_annotation(self)


@dataclass
class JavaNormalAnnotation(JavaAnnotation):
    """Java normal annotation."""
    values: List['JavaMemberValuePair'] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = JavaNodeType.NORMAL_ANNOTATION
    
    def accept(self, visitor):
        return visitor.visit_normal_annotation(self)


@dataclass
class JavaMarkerAnnotation(JavaAnnotation):
    """Java marker annotation."""
    
    def __post_init__(self):
        self.type = JavaNodeType.MARKER_ANNOTATION
    
    def accept(self, visitor):
        return visitor.visit_marker_annotation(self)


@dataclass
class JavaSingleMemberAnnotation(JavaAnnotation):
    """Java single member annotation."""
    value: Optional[JavaExpression] = None
    
    def __post_init__(self):
        self.type = JavaNodeType.SINGLE_MEMBER_ANNOTATION
    
    def accept(self, visitor):
        return visitor.visit_single_member_annotation(self)


@dataclass
class JavaMemberValuePair(JavaNode):
    """Java member value pair."""
    name: Optional[str] = None
    value: Optional[JavaExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_member_value_pair(self)


@dataclass
class JavaCatchClause(JavaNode):
    """Java catch clause."""
    exception: Optional['JavaSingleVariableDeclaration'] = None
    body: Optional[JavaBlockStatement] = None
    
    def accept(self, visitor):
        return visitor.visit_catch_clause(self)


@dataclass
class JavaSwitchCase(JavaStatement):
    """Java switch case."""
    expressions: List[JavaExpression] = field(default_factory=list)  # Empty for default case
    is_default: bool = False
    
    def __post_init__(self):
        self.type = JavaNodeType.SWITCH_CASE
    
    def accept(self, visitor):
        return visitor.visit_switch_case(self)


@dataclass
class JavaEnumConstant(JavaNode):
    """Java enum constant."""
    name: Optional[str] = None
    arguments: List[JavaExpression] = field(default_factory=list)
    anonymous_class_declaration: Optional['JavaAnonymousClassDeclaration'] = None
    
    def __post_init__(self):
        self.type = JavaNodeType.ENUM_CONSTANT
    
    def accept(self, visitor):
        return visitor.visit_enum_constant(self)


@dataclass
class JavaAnonymousClassDeclaration(JavaNode):
    """Java anonymous class declaration."""
    body_declarations: List[JavaDeclaration] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = JavaNodeType.ANONYMOUS_CLASS_DECLARATION
    
    def accept(self, visitor):
        return visitor.visit_anonymous_class_declaration(self)


@dataclass
class JavaDimension(JavaNode):
    """Java dimension."""
    annotations: List[JavaAnnotation] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = JavaNodeType.DIMENSION
    
    def accept(self, visitor):
        return visitor.visit_dimension(self)


@dataclass
class JavaModuleDeclaration(JavaDeclaration):
    """Java module declaration (Java 9)."""
    name: Optional[JavaExpression] = None
    is_open: bool = False
    module_statements: List['JavaModuleStatement'] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = JavaNodeType.MODULE_DECLARATION
    
    def accept(self, visitor):
        return visitor.visit_module_declaration(self)


@dataclass
class JavaModuleStatement(JavaNode):
    """Base class for Java module statements."""
    pass


@dataclass
class JavaRequiresDirective(JavaModuleStatement):
    """Java requires directive."""
    module_name: Optional[JavaExpression] = None
    is_transitive: bool = False
    is_static: bool = False
    
    def __post_init__(self):
        self.type = JavaNodeType.REQUIRES_DIRECTIVE
    
    def accept(self, visitor):
        return visitor.visit_requires_directive(self)


@dataclass
class JavaExportsDirective(JavaModuleStatement):
    """Java exports directive."""
    package_name: Optional[JavaExpression] = None
    target_modules: List[JavaExpression] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = JavaNodeType.EXPORTS_DIRECTIVE
    
    def accept(self, visitor):
        return visitor.visit_exports_directive(self)


@dataclass
class JavaOpensDirective(JavaModuleStatement):
    """Java opens directive."""
    package_name: Optional[JavaExpression] = None
    target_modules: List[JavaExpression] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = JavaNodeType.OPENS_DIRECTIVE
    
    def accept(self, visitor):
        return visitor.visit_opens_directive(self)


@dataclass
class JavaUsesDirective(JavaModuleStatement):
    """Java uses directive."""
    service_name: Optional[JavaExpression] = None
    
    def __post_init__(self):
        self.type = JavaNodeType.USES_DIRECTIVE
    
    def accept(self, visitor):
        return visitor.visit_uses_directive(self)


@dataclass
class JavaProvidesDirective(JavaModuleStatement):
    """Java provides directive."""
    service_name: Optional[JavaExpression] = None
    implementation_names: List[JavaExpression] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = JavaNodeType.PROVIDES_DIRECTIVE
    
    def accept(self, visitor):
        return visitor.visit_provides_directive(self)


# Additional missing classes for Java generator support

@dataclass
class JavaParenthesizedExpression(JavaExpression):
    """Java parenthesized expression."""
    expression: Optional[JavaExpression] = None
    
    def __post_init__(self):
        self.type = JavaNodeType.BINARY_EXPRESSION  # Reuse existing type
    
    def accept(self, visitor):
        return visitor.visit_parenthesized_expression(self)


@dataclass
class JavaBodyDeclaration(JavaDeclaration):
    """Base class for Java body declarations (fields, methods, constructors, etc.)."""
    pass


@dataclass
class JavaConstructorDeclaration(JavaBodyDeclaration):
    """Java constructor declaration."""
    name: str = ""
    type_parameters: List['JavaTypeParameter'] = field(default_factory=list)
    parameters: List['JavaParameter'] = field(default_factory=list)
    thrown_exceptions: List[JavaType] = field(default_factory=list)
    body: Optional[JavaBlockStatement] = None
    is_compact_constructor: bool = False  # For records
    
    def __post_init__(self):
        self.type = JavaNodeType.CONSTRUCTOR_DECLARATION
    
    def accept(self, visitor):
        return visitor.visit_constructor_declaration(self)


@dataclass
class JavaLocalVariableDeclaration(JavaStatement):
    """Java local variable declaration."""
    variable_type: Optional[JavaType] = None
    fragments: List['JavaVariableDeclarationFragment'] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = JavaNodeType.LOCAL_VARIABLE_DECLARATION
    
    def accept(self, visitor):
        return visitor.visit_local_variable_declaration(self)


@dataclass
class JavaLambdaParameter(JavaNode):
    """Java lambda parameter."""
    type: Optional[JavaType] = None
    name: Optional[str] = None
    
    def accept(self, visitor):
        return visitor.visit_lambda_parameter(self)


@dataclass
class JavaClassInstanceCreation(JavaExpression):
    """Java class instance creation expression (new Type(args))."""
    type: Optional[JavaType] = None
    arguments: List[JavaExpression] = field(default_factory=list)
    anonymous_class_body: Optional['JavaAnonymousClassDeclaration'] = None
    
    def __post_init__(self):
        self.type = JavaNodeType.CLASS_LITERAL  # Reuse existing node type
    
    def accept(self, visitor):
        return visitor.visit_class_instance_creation(self)


@dataclass
class JavaModuleDirective(JavaNode):
    """Base class for Java module directives."""
    pass


@dataclass
class JavaRecordComponent(JavaNode):
    """Java record component (Java 14+)."""
    modifiers: List[JavaModifier] = field(default_factory=list)
    annotations: List['JavaAnnotation'] = field(default_factory=list)
    component_type: JavaType = None
    name: str = ""
    
    def accept(self, visitor):
        return visitor.visit_record_component(self)


class JavaNodeVisitor(ABC):
    """Abstract base class for Java AST visitors."""
    
    @abstractmethod
    def visit_integer_literal(self, node: JavaIntegerLiteral): pass
    
    @abstractmethod
    def visit_floating_literal(self, node: JavaFloatingLiteral): pass
    
    @abstractmethod
    def visit_string_literal(self, node: JavaStringLiteral): pass
    
    @abstractmethod
    def visit_character_literal(self, node: JavaCharacterLiteral): pass
    
    @abstractmethod
    def visit_boolean_literal(self, node: JavaBooleanLiteral): pass
    
    @abstractmethod
    def visit_null_literal(self, node: JavaNullLiteral): pass
    
    @abstractmethod
    def visit_text_block(self, node: JavaTextBlock): pass
    
    @abstractmethod
    def visit_simple_name(self, node: JavaSimpleName): pass
    
    @abstractmethod
    def visit_qualified_name(self, node: JavaQualifiedName): pass
    
    @abstractmethod
    def visit_binary_expression(self, node: JavaBinaryExpression): pass
    
    @abstractmethod
    def visit_unary_expression(self, node: JavaUnaryExpression): pass
    
    @abstractmethod
    def visit_conditional_expression(self, node: JavaConditionalExpression): pass
    
    @abstractmethod
    def visit_assignment_expression(self, node: JavaAssignmentExpression): pass
    
    @abstractmethod
    def visit_method_invocation(self, node: JavaMethodInvocation): pass
    
    @abstractmethod
    def visit_field_access(self, node: JavaFieldAccess): pass
    
    @abstractmethod
    def visit_array_access(self, node: JavaArrayAccess): pass
    
    @abstractmethod
    def visit_cast_expression(self, node: JavaCastExpression): pass
    
    @abstractmethod
    def visit_instanceof_expression(self, node: JavaInstanceofExpression): pass
    
    @abstractmethod
    def visit_this_expression(self, node: JavaThisExpression): pass
    
    @abstractmethod
    def visit_super_expression(self, node: JavaSuperExpression): pass
    
    @abstractmethod
    def visit_class_literal(self, node: JavaClassLiteral): pass
    
    @abstractmethod
    def visit_array_creation(self, node: JavaArrayCreation): pass
    
    @abstractmethod
    def visit_array_initializer(self, node: JavaArrayInitializer): pass
    
    @abstractmethod
    def visit_lambda_expression(self, node: JavaLambdaExpression): pass
    
    @abstractmethod
    def visit_method_reference(self, node: JavaMethodReference): pass
    
    @abstractmethod
    def visit_expression_statement(self, node: JavaExpressionStatement): pass
    
    @abstractmethod
    def visit_block_statement(self, node: JavaBlockStatement): pass
    
    @abstractmethod
    def visit_if_statement(self, node: JavaIfStatement): pass
    
    @abstractmethod
    def visit_while_statement(self, node: JavaWhileStatement): pass
    
    @abstractmethod
    def visit_for_statement(self, node: JavaForStatement): pass
    
    @abstractmethod
    def visit_enhanced_for_statement(self, node: JavaEnhancedForStatement): pass
    
    @abstractmethod
    def visit_do_statement(self, node: JavaDoStatement): pass
    
    @abstractmethod
    def visit_switch_statement(self, node: JavaSwitchStatement): pass
    
    @abstractmethod
    def visit_switch_expression(self, node: JavaSwitchExpression): pass
    
    @abstractmethod
    def visit_break_statement(self, node: JavaBreakStatement): pass
    
    @abstractmethod
    def visit_continue_statement(self, node: JavaContinueStatement): pass
    
    @abstractmethod
    def visit_return_statement(self, node: JavaReturnStatement): pass
    
    @abstractmethod
    def visit_throw_statement(self, node: JavaThrowStatement): pass
    
    @abstractmethod
    def visit_try_statement(self, node: JavaTryStatement): pass
    
    @abstractmethod
    def visit_synchronized_statement(self, node: JavaSynchronizedStatement): pass
    
    @abstractmethod
    def visit_assert_statement(self, node: JavaAssertStatement): pass
    
    @abstractmethod
    def visit_empty_statement(self, node: JavaEmptyStatement): pass
    
    @abstractmethod
    def visit_labeled_statement(self, node: JavaLabeledStatement): pass
    
    @abstractmethod
    def visit_yield_statement(self, node: JavaYieldStatement): pass
    
    @abstractmethod
    def visit_compilation_unit(self, node: JavaCompilationUnit): pass
    
    @abstractmethod
    def visit_package_declaration(self, node: JavaPackageDeclaration): pass
    
    @abstractmethod
    def visit_import_declaration(self, node: JavaImportDeclaration): pass
    
    @abstractmethod
    def visit_class_declaration(self, node: JavaClassDeclaration): pass
    
    @abstractmethod
    def visit_interface_declaration(self, node: JavaInterfaceDeclaration): pass
    
    @abstractmethod
    def visit_enum_declaration(self, node: JavaEnumDeclaration): pass
    
    @abstractmethod
    def visit_annotation_declaration(self, node: JavaAnnotationDeclaration): pass
    
    @abstractmethod
    def visit_record_declaration(self, node: JavaRecordDeclaration): pass
    
    @abstractmethod
    def visit_field_declaration(self, node: JavaFieldDeclaration): pass
    
    @abstractmethod
    def visit_method_declaration(self, node: JavaMethodDeclaration): pass
    
    @abstractmethod
    def visit_variable_declaration(self, node: JavaVariableDeclaration): pass
    
    @abstractmethod
    def visit_variable_declaration_fragment(self, node: JavaVariableDeclarationFragment): pass
    
    @abstractmethod
    def visit_single_variable_declaration(self, node: JavaSingleVariableDeclaration): pass
    
    @abstractmethod
    def visit_parameter(self, node: JavaParameter): pass
    
    @abstractmethod
    def visit_type_parameter(self, node: JavaTypeParameter): pass
    
    @abstractmethod
    def visit_primitive_type(self, node: JavaPrimitiveType): pass
    
    @abstractmethod
    def visit_array_type(self, node: JavaArrayType): pass
    
    @abstractmethod
    def visit_parameterized_type(self, node: JavaParameterizedType): pass
    
    @abstractmethod
    def visit_wildcard_type(self, node: JavaWildcardType): pass
    
    @abstractmethod
    def visit_union_type(self, node: JavaUnionType): pass
    
    @abstractmethod
    def visit_intersection_type(self, node: JavaIntersectionType): pass
    
    @abstractmethod
    def visit_var_type(self, node: JavaVarType): pass
    
    @abstractmethod
    def visit_annotation(self, node: JavaAnnotation): pass
    
    @abstractmethod
    def visit_normal_annotation(self, node: JavaNormalAnnotation): pass
    
    @abstractmethod
    def visit_marker_annotation(self, node: JavaMarkerAnnotation): pass
    
    @abstractmethod
    def visit_single_member_annotation(self, node: JavaSingleMemberAnnotation): pass
    
    @abstractmethod
    def visit_member_value_pair(self, node: JavaMemberValuePair): pass
    
    @abstractmethod
    def visit_catch_clause(self, node: JavaCatchClause): pass
    
    @abstractmethod
    def visit_switch_case(self, node: JavaSwitchCase): pass
    
    @abstractmethod
    def visit_enum_constant(self, node: JavaEnumConstant): pass
    
    @abstractmethod
    def visit_anonymous_class_declaration(self, node: JavaAnonymousClassDeclaration): pass
    
    @abstractmethod
    def visit_dimension(self, node: JavaDimension): pass
    
    @abstractmethod
    def visit_module_declaration(self, node: JavaModuleDeclaration): pass
    
    @abstractmethod
    def visit_requires_directive(self, node: JavaRequiresDirective): pass
    
    @abstractmethod
    def visit_exports_directive(self, node: JavaExportsDirective): pass
    
    @abstractmethod
    def visit_opens_directive(self, node: JavaOpensDirective): pass
    
    @abstractmethod
    def visit_uses_directive(self, node: JavaUsesDirective): pass
    
    @abstractmethod
    def visit_provides_directive(self, node: JavaProvidesDirective): pass


@dataclass
class JavaRecordComponent(JavaNode):
    """Java record component (Java 14+)."""
    modifiers: List[JavaModifier] = field(default_factory=list)
    annotations: List['JavaAnnotation'] = field(default_factory=list)
    component_type: JavaType = None
    name: str = ""
    
    def accept(self, visitor):
        return visitor.visit_record_component(self)