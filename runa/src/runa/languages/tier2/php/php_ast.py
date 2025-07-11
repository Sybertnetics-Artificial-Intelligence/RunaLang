#!/usr/bin/env python3
"""
PHP AST Node Definitions

Comprehensive Abstract Syntax Tree nodes for PHP language covering all PHP features
including classes, traits, interfaces, namespaces, functions, closures, anonymous classes,
attributes, generators, type declarations, and modern PHP 8+ features.

Author: Sybertnetics AI Solutions
License: MIT
"""

from typing import List, Optional, Any, Union, Dict
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod

from ....core.runa_ast import ASTNode, SourceLocation, TranslationMetadata


class PhpNodeType(Enum):
    """PHP-specific AST node types."""
    # Program structure
    SOURCE_FILE = auto()
    NAMESPACE_DECLARATION = auto()
    USE_DECLARATION = auto()
    
    # Types and type declarations
    TYPE_DECLARATION = auto()
    UNION_TYPE = auto()
    INTERSECTION_TYPE = auto()
    NULLABLE_TYPE = auto()
    
    # Declarations
    CLASS_DECLARATION = auto()
    INTERFACE_DECLARATION = auto()
    TRAIT_DECLARATION = auto()
    ENUM_DECLARATION = auto()
    FUNCTION_DECLARATION = auto()
    METHOD_DECLARATION = auto()
    PROPERTY_DECLARATION = auto()
    CONSTANT_DECLARATION = auto()
    
    # Statements
    EXPRESSION_STATEMENT = auto()
    ECHO_STATEMENT = auto()
    RETURN_STATEMENT = auto()
    BREAK_STATEMENT = auto()
    CONTINUE_STATEMENT = auto()
    THROW_STATEMENT = auto()
    TRY_STATEMENT = auto()
    IF_STATEMENT = auto()
    SWITCH_STATEMENT = auto()
    FOR_STATEMENT = auto()
    FOREACH_STATEMENT = auto()
    WHILE_STATEMENT = auto()
    DO_WHILE_STATEMENT = auto()
    DECLARE_STATEMENT = auto()
    GLOBAL_STATEMENT = auto()
    STATIC_STATEMENT = auto()
    UNSET_STATEMENT = auto()
    
    # Expressions
    IDENTIFIER_EXPRESSION = auto()
    VARIABLE_EXPRESSION = auto()
    LITERAL_EXPRESSION = auto()
    ARRAY_EXPRESSION = auto()
    FUNCTION_CALL_EXPRESSION = auto()
    METHOD_CALL_EXPRESSION = auto()
    STATIC_CALL_EXPRESSION = auto()
    PROPERTY_ACCESS_EXPRESSION = auto()
    STATIC_PROPERTY_ACCESS_EXPRESSION = auto()
    ARRAY_ACCESS_EXPRESSION = auto()
    BINARY_EXPRESSION = auto()
    UNARY_EXPRESSION = auto()
    TERNARY_EXPRESSION = auto()
    ASSIGNMENT_EXPRESSION = auto()
    NEW_EXPRESSION = auto()
    CLONE_EXPRESSION = auto()
    INSTANCEOF_EXPRESSION = auto()
    CLOSURE_EXPRESSION = auto()
    ARROW_FUNCTION_EXPRESSION = auto()
    YIELD_EXPRESSION = auto()
    YIELD_FROM_EXPRESSION = auto()
    MATCH_EXPRESSION = auto()
    
    # Attributes and annotations
    ATTRIBUTE = auto()
    DOC_COMMENT = auto()


class PhpVisibility(Enum):
    """PHP visibility modifiers."""
    PUBLIC = "public"
    PROTECTED = "protected"
    PRIVATE = "private"


class PhpModifier(Enum):
    """PHP declaration modifiers."""
    STATIC = "static"
    ABSTRACT = "abstract"
    FINAL = "final"
    READONLY = "readonly"


@dataclass
class PhpNode(ASTNode):
    """Base class for all PHP AST nodes."""
    php_node_type: PhpNodeType = PhpNodeType.SOURCE_FILE
    
    @abstractmethod
    def accept(self, visitor):
        """Accept a visitor for AST traversal."""
        pass


@dataclass
class PhpAttribute(PhpNode):
    """PHP attribute: #[AttributeName(args)]"""
    php_node_type: PhpNodeType = PhpNodeType.ATTRIBUTE
    name: str = ""
    arguments: List['PhpExpression'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_php_attribute(self)


# ============================================================================
# Types
# ============================================================================

@dataclass
class PhpType(PhpNode):
    """Base class for PHP types."""
    pass


@dataclass
class PhpTypeDeclaration(PhpType):
    """Type declaration: int, string, MyClass"""
    php_node_type: PhpNodeType = PhpNodeType.TYPE_DECLARATION
    name: str = ""
    
    def accept(self, visitor):
        return visitor.visit_php_type_declaration(self)


@dataclass
class PhpUnionType(PhpType):
    """Union type: int|string|null"""
    php_node_type: PhpNodeType = PhpNodeType.UNION_TYPE
    types: List[PhpType] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_php_union_type(self)


@dataclass
class PhpIntersectionType(PhpType):
    """Intersection type: A&B&C"""
    php_node_type: PhpNodeType = PhpNodeType.INTERSECTION_TYPE
    types: List[PhpType] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_php_intersection_type(self)


@dataclass
class PhpNullableType(PhpType):
    """Nullable type: ?int"""
    php_node_type: PhpNodeType = PhpNodeType.NULLABLE_TYPE
    inner_type: Optional[PhpType] = None
    
    def accept(self, visitor):
        return visitor.visit_php_nullable_type(self)


# ============================================================================
# Declarations
# ============================================================================

@dataclass
class PhpDeclaration(PhpNode):
    """Base class for PHP declarations."""
    attributes: List[PhpAttribute] = field(default_factory=list)
    modifiers: List[PhpModifier] = field(default_factory=list)
    visibility: Optional[PhpVisibility] = None


@dataclass
class PhpNamespaceDeclaration(PhpDeclaration):
    """Namespace declaration: namespace MyNamespace;"""
    php_node_type: PhpNodeType = PhpNodeType.NAMESPACE_DECLARATION
    name: str = ""
    statements: List['PhpStatement'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_php_namespace_declaration(self)


@dataclass
class PhpUseDeclaration(PhpDeclaration):
    """Use declaration: use My\\Namespace\\Class;"""
    php_node_type: PhpNodeType = PhpNodeType.USE_DECLARATION
    name: str = ""
    alias: Optional[str] = None
    kind: str = "class"  # class, function, const
    
    def accept(self, visitor):
        return visitor.visit_php_use_declaration(self)


@dataclass
class PhpClassDeclaration(PhpDeclaration):
    """Class declaration: class MyClass extends Parent implements Interface"""
    php_node_type: PhpNodeType = PhpNodeType.CLASS_DECLARATION
    name: str = ""
    extends: Optional[str] = None
    implements: List[str] = field(default_factory=list)
    members: List['PhpMember'] = field(default_factory=list)
    is_abstract: bool = False
    is_final: bool = False
    is_readonly: bool = False
    
    def accept(self, visitor):
        return visitor.visit_php_class_declaration(self)


@dataclass
class PhpInterfaceDeclaration(PhpDeclaration):
    """Interface declaration: interface MyInterface extends ParentInterface"""
    php_node_type: PhpNodeType = PhpNodeType.INTERFACE_DECLARATION
    name: str = ""
    extends: List[str] = field(default_factory=list)
    members: List['PhpMember'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_php_interface_declaration(self)


@dataclass
class PhpTraitDeclaration(PhpDeclaration):
    """Trait declaration: trait MyTrait"""
    php_node_type: PhpNodeType = PhpNodeType.TRAIT_DECLARATION
    name: str = ""
    members: List['PhpMember'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_php_trait_declaration(self)


@dataclass
class PhpEnumDeclaration(PhpDeclaration):
    """Enum declaration: enum Status: int"""
    php_node_type: PhpNodeType = PhpNodeType.ENUM_DECLARATION
    name: str = ""
    backed_type: Optional[PhpType] = None
    implements: List[str] = field(default_factory=list)
    cases: List['PhpEnumCase'] = field(default_factory=list)
    members: List['PhpMember'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_php_enum_declaration(self)


@dataclass
class PhpFunctionDeclaration(PhpDeclaration):
    """Function declaration: function myFunction(int $param): string"""
    php_node_type: PhpNodeType = PhpNodeType.FUNCTION_DECLARATION
    name: str = ""
    parameters: List['PhpParameter'] = field(default_factory=list)
    return_type: Optional[PhpType] = None
    body: Optional['PhpBlock'] = None
    is_generator: bool = False
    
    def accept(self, visitor):
        return visitor.visit_php_function_declaration(self)


@dataclass
class PhpMethodDeclaration(PhpDeclaration):
    """Method declaration: public function method(): void"""
    php_node_type: PhpNodeType = PhpNodeType.METHOD_DECLARATION
    name: str = ""
    parameters: List['PhpParameter'] = field(default_factory=list)
    return_type: Optional[PhpType] = None
    body: Optional['PhpBlock'] = None
    is_abstract: bool = False
    is_static: bool = False
    is_final: bool = False
    
    def accept(self, visitor):
        return visitor.visit_php_method_declaration(self)


@dataclass
class PhpPropertyDeclaration(PhpDeclaration):
    """Property declaration: public string $property = "value";"""
    php_node_type: PhpNodeType = PhpNodeType.PROPERTY_DECLARATION
    name: str = ""
    type_hint: Optional[PhpType] = None
    default_value: Optional['PhpExpression'] = None
    is_static: bool = False
    is_readonly: bool = False
    
    def accept(self, visitor):
        return visitor.visit_php_property_declaration(self)


@dataclass
class PhpConstantDeclaration(PhpDeclaration):
    """Constant declaration: const CONSTANT = 'value';"""
    php_node_type: PhpNodeType = PhpNodeType.CONSTANT_DECLARATION
    name: str = ""
    value: Optional['PhpExpression'] = None
    
    def accept(self, visitor):
        return visitor.visit_php_constant_declaration(self)


# ============================================================================
# Statements
# ============================================================================

@dataclass
class PhpStatement(PhpNode):
    """Base class for PHP statements."""
    pass


@dataclass
class PhpBlock(PhpStatement):
    """Block statement: { statements }"""
    statements: List[PhpStatement] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_php_block(self)


@dataclass
class PhpExpressionStatement(PhpStatement):
    """Expression statement: expression;"""
    php_node_type: PhpNodeType = PhpNodeType.EXPRESSION_STATEMENT
    expression: Optional['PhpExpression'] = None
    
    def accept(self, visitor):
        return visitor.visit_php_expression_statement(self)


@dataclass
class PhpEchoStatement(PhpStatement):
    """Echo statement: echo $value;"""
    php_node_type: PhpNodeType = PhpNodeType.ECHO_STATEMENT
    expressions: List['PhpExpression'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_php_echo_statement(self)


@dataclass
class PhpReturnStatement(PhpStatement):
    """Return statement: return $value;"""
    php_node_type: PhpNodeType = PhpNodeType.RETURN_STATEMENT
    expression: Optional['PhpExpression'] = None
    
    def accept(self, visitor):
        return visitor.visit_php_return_statement(self)


@dataclass
class PhpIfStatement(PhpStatement):
    """If statement: if ($condition) { } elseif ($condition2) { } else { }"""
    php_node_type: PhpNodeType = PhpNodeType.IF_STATEMENT
    condition: Optional['PhpExpression'] = None
    then_statement: Optional[PhpStatement] = None
    elseif_clauses: List['PhpElseIfClause'] = field(default_factory=list)
    else_statement: Optional[PhpStatement] = None
    
    def accept(self, visitor):
        return visitor.visit_php_if_statement(self)


@dataclass
class PhpSwitchStatement(PhpStatement):
    """Switch statement: switch ($expr) { case $value: ... }"""
    php_node_type: PhpNodeType = PhpNodeType.SWITCH_STATEMENT
    expression: Optional['PhpExpression'] = None
    cases: List['PhpSwitchCase'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_php_switch_statement(self)


@dataclass
class PhpForStatement(PhpStatement):
    """For statement: for ($i = 0; $i < 10; $i++) { }"""
    php_node_type: PhpNodeType = PhpNodeType.FOR_STATEMENT
    init: List['PhpExpression'] = field(default_factory=list)
    condition: List['PhpExpression'] = field(default_factory=list)
    update: List['PhpExpression'] = field(default_factory=list)
    body: Optional[PhpStatement] = None
    
    def accept(self, visitor):
        return visitor.visit_php_for_statement(self)


@dataclass
class PhpForeachStatement(PhpStatement):
    """Foreach statement: foreach ($array as $key => $value) { }"""
    php_node_type: PhpNodeType = PhpNodeType.FOREACH_STATEMENT
    iterable: Optional['PhpExpression'] = None
    key_variable: Optional['PhpVariable'] = None
    value_variable: Optional['PhpVariable'] = None
    body: Optional[PhpStatement] = None
    by_reference: bool = False
    
    def accept(self, visitor):
        return visitor.visit_php_foreach_statement(self)


@dataclass
class PhpWhileStatement(PhpStatement):
    """While statement: while ($condition) { }"""
    php_node_type: PhpNodeType = PhpNodeType.WHILE_STATEMENT
    condition: Optional['PhpExpression'] = None
    body: Optional[PhpStatement] = None
    
    def accept(self, visitor):
        return visitor.visit_php_while_statement(self)


@dataclass
class PhpTryStatement(PhpStatement):
    """Try statement: try { } catch (Exception $e) { } finally { }"""
    php_node_type: PhpNodeType = PhpNodeType.TRY_STATEMENT
    try_block: Optional[PhpStatement] = None
    catch_clauses: List['PhpCatchClause'] = field(default_factory=list)
    finally_block: Optional[PhpStatement] = None
    
    def accept(self, visitor):
        return visitor.visit_php_try_statement(self)


# ============================================================================
# Expressions
# ============================================================================

@dataclass
class PhpExpression(PhpNode):
    """Base class for PHP expressions."""
    pass


@dataclass
class PhpIdentifier(PhpExpression):
    """Identifier expression: MyClass"""
    php_node_type: PhpNodeType = PhpNodeType.IDENTIFIER_EXPRESSION
    name: str = ""
    
    def accept(self, visitor):
        return visitor.visit_php_identifier(self)


@dataclass
class PhpVariable(PhpExpression):
    """Variable expression: $variable"""
    php_node_type: PhpNodeType = PhpNodeType.VARIABLE_EXPRESSION
    name: str = ""
    
    def accept(self, visitor):
        return visitor.visit_php_variable(self)


@dataclass
class PhpLiteral(PhpExpression):
    """Literal expression: 42, "string", true, null"""
    php_node_type: PhpNodeType = PhpNodeType.LITERAL_EXPRESSION
    value: Any = None
    literal_type: str = "string"  # int, float, string, bool, null
    
    def accept(self, visitor):
        return visitor.visit_php_literal(self)


@dataclass
class PhpArrayExpression(PhpExpression):
    """Array expression: [1, 2, 3] or ['key' => 'value']"""
    php_node_type: PhpNodeType = PhpNodeType.ARRAY_EXPRESSION
    elements: List['PhpArrayElement'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_php_array_expression(self)


@dataclass
class PhpFunctionCall(PhpExpression):
    """Function call: func($arg1, $arg2)"""
    php_node_type: PhpNodeType = PhpNodeType.FUNCTION_CALL_EXPRESSION
    function: Optional[PhpExpression] = None
    arguments: List['PhpArgument'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_php_function_call(self)


@dataclass
class PhpMethodCall(PhpExpression):
    """Method call: $object->method($args)"""
    php_node_type: PhpNodeType = PhpNodeType.METHOD_CALL_EXPRESSION
    object: Optional[PhpExpression] = None
    method: str = ""
    arguments: List['PhpArgument'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_php_method_call(self)


@dataclass
class PhpStaticCall(PhpExpression):
    """Static call: Class::method($args)"""
    php_node_type: PhpNodeType = PhpNodeType.STATIC_CALL_EXPRESSION
    class_name: Optional[PhpExpression] = None
    method: str = ""
    arguments: List['PhpArgument'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_php_static_call(self)


@dataclass
class PhpPropertyAccess(PhpExpression):
    """Property access: $object->property"""
    php_node_type: PhpNodeType = PhpNodeType.PROPERTY_ACCESS_EXPRESSION
    object: Optional[PhpExpression] = None
    property: str = ""
    
    def accept(self, visitor):
        return visitor.visit_php_property_access(self)


@dataclass
class PhpStaticPropertyAccess(PhpExpression):
    """Static property access: Class::$property"""
    php_node_type: PhpNodeType = PhpNodeType.STATIC_PROPERTY_ACCESS_EXPRESSION
    class_name: Optional[PhpExpression] = None
    property: str = ""
    
    def accept(self, visitor):
        return visitor.visit_php_static_property_access(self)


@dataclass
class PhpArrayAccess(PhpExpression):
    """Array access: $array[$index]"""
    php_node_type: PhpNodeType = PhpNodeType.ARRAY_ACCESS_EXPRESSION
    array: Optional[PhpExpression] = None
    index: Optional[PhpExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_php_array_access(self)


@dataclass
class PhpBinaryExpression(PhpExpression):
    """Binary expression: $a + $b"""
    php_node_type: PhpNodeType = PhpNodeType.BINARY_EXPRESSION
    left: Optional[PhpExpression] = None
    operator: str = ""
    right: Optional[PhpExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_php_binary_expression(self)


@dataclass
class PhpUnaryExpression(PhpExpression):
    """Unary expression: !$condition, ++$i"""
    php_node_type: PhpNodeType = PhpNodeType.UNARY_EXPRESSION
    operator: str = ""
    operand: Optional[PhpExpression] = None
    is_prefix: bool = True
    
    def accept(self, visitor):
        return visitor.visit_php_unary_expression(self)


@dataclass
class PhpTernaryExpression(PhpExpression):
    """Ternary expression: $condition ? $true : $false"""
    php_node_type: PhpNodeType = PhpNodeType.TERNARY_EXPRESSION
    condition: Optional[PhpExpression] = None
    true_expression: Optional[PhpExpression] = None
    false_expression: Optional[PhpExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_php_ternary_expression(self)


@dataclass
class PhpAssignmentExpression(PhpExpression):
    """Assignment expression: $var = $value"""
    php_node_type: PhpNodeType = PhpNodeType.ASSIGNMENT_EXPRESSION
    target: Optional[PhpExpression] = None
    operator: str = "="
    value: Optional[PhpExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_php_assignment_expression(self)


@dataclass
class PhpNewExpression(PhpExpression):
    """New expression: new MyClass($args)"""
    php_node_type: PhpNodeType = PhpNodeType.NEW_EXPRESSION
    class_name: Optional[PhpExpression] = None
    arguments: List['PhpArgument'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_php_new_expression(self)


@dataclass
class PhpClosureExpression(PhpExpression):
    """Closure expression: function($param) use ($var) { }"""
    php_node_type: PhpNodeType = PhpNodeType.CLOSURE_EXPRESSION
    parameters: List['PhpParameter'] = field(default_factory=list)
    uses: List['PhpUseVariable'] = field(default_factory=list)
    return_type: Optional[PhpType] = None
    body: Optional[PhpStatement] = None
    is_static: bool = False
    
    def accept(self, visitor):
        return visitor.visit_php_closure_expression(self)


@dataclass
class PhpArrowFunction(PhpExpression):
    """Arrow function: fn($x) => $x * 2"""
    php_node_type: PhpNodeType = PhpNodeType.ARROW_FUNCTION_EXPRESSION
    parameters: List['PhpParameter'] = field(default_factory=list)
    return_type: Optional[PhpType] = None
    body: Optional[PhpExpression] = None
    is_static: bool = False
    
    def accept(self, visitor):
        return visitor.visit_php_arrow_function(self)


@dataclass
class PhpYieldExpression(PhpExpression):
    """Yield expression: yield $key => $value"""
    php_node_type: PhpNodeType = PhpNodeType.YIELD_EXPRESSION
    key: Optional[PhpExpression] = None
    value: Optional[PhpExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_php_yield_expression(self)


@dataclass
class PhpMatchExpression(PhpExpression):
    """Match expression: match($value) { 1 => 'one', default => 'other' }"""
    php_node_type: PhpNodeType = PhpNodeType.MATCH_EXPRESSION
    subject: Optional[PhpExpression] = None
    arms: List['PhpMatchArm'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_php_match_expression(self)


# ============================================================================
# Support Structures
# ============================================================================

@dataclass
class PhpParameter:
    """Function parameter"""
    name: str = ""
    type_hint: Optional[PhpType] = None
    default_value: Optional[PhpExpression] = None
    is_variadic: bool = False
    is_reference: bool = False
    visibility: Optional[PhpVisibility] = None  # For constructor property promotion
    is_readonly: bool = False
    
    def accept(self, visitor):
        return visitor.visit_php_parameter(self)


@dataclass
class PhpArgument:
    """Function call argument"""
    name: Optional[str] = None  # Named argument
    value: Optional[PhpExpression] = None
    is_unpacked: bool = False
    
    def accept(self, visitor):
        return visitor.visit_php_argument(self)


@dataclass
class PhpArrayElement:
    """Array element"""
    key: Optional[PhpExpression] = None
    value: Optional[PhpExpression] = None
    is_unpacked: bool = False
    
    def accept(self, visitor):
        return visitor.visit_php_array_element(self)


@dataclass
class PhpEnumCase:
    """Enum case"""
    name: str = ""
    value: Optional[PhpExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_php_enum_case(self)


@dataclass
class PhpSwitchCase:
    """Switch case"""
    conditions: List[PhpExpression] = field(default_factory=list)
    statements: List[PhpStatement] = field(default_factory=list)
    is_default: bool = False
    
    def accept(self, visitor):
        return visitor.visit_php_switch_case(self)


@dataclass
class PhpCatchClause:
    """Catch clause"""
    types: List[PhpType] = field(default_factory=list)
    variable: Optional[PhpVariable] = None
    body: Optional[PhpStatement] = None
    
    def accept(self, visitor):
        return visitor.visit_php_catch_clause(self)


@dataclass
class PhpElseIfClause:
    """ElseIf clause"""
    condition: Optional[PhpExpression] = None
    statement: Optional[PhpStatement] = None
    
    def accept(self, visitor):
        return visitor.visit_php_elseif_clause(self)


@dataclass
class PhpMatchArm:
    """Match arm"""
    conditions: List[PhpExpression] = field(default_factory=list)
    expression: Optional[PhpExpression] = None
    is_default: bool = False
    
    def accept(self, visitor):
        return visitor.visit_php_match_arm(self)


@dataclass
class PhpUseVariable:
    """Use variable in closure"""
    variable: Optional[PhpVariable] = None
    by_reference: bool = False
    
    def accept(self, visitor):
        return visitor.visit_php_use_variable(self)


# ============================================================================
# File Structure and Members
# ============================================================================

@dataclass
class PhpMember(PhpNode):
    """Base class for class/interface/trait members."""
    pass


@dataclass
class PhpSourceFile(PhpNode):
    """PHP source file"""
    php_node_type: PhpNodeType = PhpNodeType.SOURCE_FILE
    declarations: List[PhpDeclaration] = field(default_factory=list)
    statements: List[PhpStatement] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_php_source_file(self)


# ============================================================================
# Visitor Pattern
# ============================================================================

class PhpVisitor(ABC):
    """Abstract visitor for PHP AST nodes."""
    
    @abstractmethod
    def visit_php_source_file(self, node: PhpSourceFile): pass
    
    @abstractmethod
    def visit_php_class_declaration(self, node: PhpClassDeclaration): pass
    
    @abstractmethod
    def visit_php_function_declaration(self, node: PhpFunctionDeclaration): pass
    
    @abstractmethod
    def visit_php_variable(self, node: PhpVariable): pass
    
    @abstractmethod
    def visit_php_literal(self, node: PhpLiteral): pass
    
    @abstractmethod
    def visit_php_block(self, node: PhpBlock): pass


# ============================================================================
# Utility Functions
# ============================================================================

def create_php_variable(name: str) -> PhpVariable:
    """Create a PHP variable expression."""
    return PhpVariable(name=name)


def create_php_literal(value: Any, literal_type: str = "string") -> PhpLiteral:
    """Create a PHP literal expression."""
    return PhpLiteral(value=value, literal_type=literal_type)


def create_php_class(name: str) -> PhpClassDeclaration:
    """Create a PHP class declaration."""
    return PhpClassDeclaration(name=name)


def create_php_function(name: str) -> PhpFunctionDeclaration:
    """Create a PHP function declaration."""
    return PhpFunctionDeclaration(name=name)


# ============================================================================
# Constants
# ============================================================================

# PHP keywords
PHP_KEYWORDS = {
    "abstract", "and", "array", "as", "break", "callable", "case", "catch", "class",
    "clone", "const", "continue", "declare", "default", "die", "do", "echo", "else",
    "elseif", "empty", "enddeclare", "endfor", "endforeach", "endif", "endswitch",
    "endwhile", "eval", "exit", "extends", "final", "finally", "fn", "for", "foreach",
    "function", "global", "goto", "if", "implements", "include", "include_once",
    "instanceof", "insteadof", "interface", "isset", "list", "match", "namespace",
    "new", "or", "print", "private", "protected", "public", "readonly", "require",
    "require_once", "return", "static", "switch", "throw", "trait", "try", "unset",
    "use", "var", "while", "xor", "yield", "yield_from", "enum"
}

# PHP magic methods
PHP_MAGIC_METHODS = {
    "__construct", "__destruct", "__call", "__callStatic", "__get", "__set",
    "__isset", "__unset", "__sleep", "__wakeup", "__serialize", "__unserialize",
    "__toString", "__invoke", "__set_state", "__clone", "__debugInfo"
}

# PHP superglobals
PHP_SUPERGLOBALS = {
    "$GLOBALS", "$_SERVER", "$_GET", "$_POST", "$_FILES", "$_COOKIE", "$_SESSION",
    "$_REQUEST", "$_ENV"
}

# PHP operators
PHP_OPERATORS = {
    "+", "-", "*", "/", "%", "**", "=", "+=", "-=", "*=", "/=", "%=", "**=",
    ".=", "==", "!=", "<>", "===", "!==", "<", ">", "<=", ">=", "<=>",
    "&&", "||", "and", "or", "xor", "!", "?:", "??", "??=", "?->",
    "&", "|", "^", "~", "<<", ">>", "++", "--", ".", "=>", "->", "::",
    "instanceof", "match"
}