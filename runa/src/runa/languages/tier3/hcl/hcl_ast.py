#!/usr/bin/env python3
"""
HCL AST - Abstract Syntax Tree for HashiCorp Configuration Language

Provides comprehensive AST node definitions for HCL including:
- Configuration blocks with labels and nested structure
- Attribute assignments with various value types
- Expressions and interpolations with ${} syntax
- Function calls and built-in functions
- Variables, locals, and data sources
- Conditional expressions and for loops
- Comments and documentation
- JSON compatibility mode

Supports HCL 1.0 and HCL 2.0 specifications as used in Terraform, Consul, Vault.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any, Union
from enum import Enum
from dataclasses import dataclass


class HCLNode(ABC):
    """Base class for all HCL AST nodes"""
    
    def __init__(self, location: Optional[Dict[str, Any]] = None):
        self.location = location or {}
        self.parent: Optional['HCLNode'] = None
        self.children: List['HCLNode'] = []
    
    @abstractmethod
    def accept(self, visitor: 'HCLVisitor') -> Any:
        """Accept visitor pattern implementation"""
        pass
    
    def add_child(self, child: 'HCLNode') -> None:
        """Add child node"""
        if child:
            child.parent = self
            self.children.append(child)


class HCLExpression(HCLNode):
    """Base class for all HCL expressions"""
    pass


class HCLValue(HCLExpression):
    """Base class for HCL values"""
    pass


class HCLStatement(HCLNode):
    """Base class for HCL statements"""
    pass


class HCLType(Enum):
    """HCL value types"""
    STRING = "string"
    NUMBER = "number"
    BOOL = "bool"
    NULL = "null"
    LIST = "list"
    MAP = "map"
    OBJECT = "object"
    TUPLE = "tuple"


# Literal Values
@dataclass
class HCLLiteral(HCLValue):
    """HCL literal value"""
    value: Any
    type: HCLType
    
    def accept(self, visitor: 'HCLVisitor') -> Any:
        return visitor.visit_literal(self)


@dataclass
class HCLString(HCLValue):
    """HCL string value with interpolation support"""
    parts: List[Union[str, 'HCLInterpolation']]
    is_heredoc: bool = False
    heredoc_identifier: Optional[str] = None
    
    def accept(self, visitor: 'HCLVisitor') -> Any:
        return visitor.visit_string(self)


@dataclass
class HCLNumber(HCLValue):
    """HCL numeric value"""
    value: Union[int, float]
    raw_text: str
    
    def accept(self, visitor: 'HCLVisitor') -> Any:
        return visitor.visit_number(self)


@dataclass
class HCLBool(HCLValue):
    """HCL boolean value"""
    value: bool
    
    def accept(self, visitor: 'HCLVisitor') -> Any:
        return visitor.visit_bool(self)


@dataclass
class HCLNull(HCLValue):
    """HCL null value"""
    
    def accept(self, visitor: 'HCLVisitor') -> Any:
        return visitor.visit_null(self)


# Collection Types
@dataclass
class HCLList(HCLValue):
    """HCL list/array value"""
    elements: List[HCLExpression]
    
    def accept(self, visitor: 'HCLVisitor') -> Any:
        return visitor.visit_list(self)


@dataclass
class HCLMap(HCLValue):
    """HCL map/object value"""
    pairs: List[tuple[HCLExpression, HCLExpression]]  # (key, value) pairs
    
    def accept(self, visitor: 'HCLVisitor') -> Any:
        return visitor.visit_map(self)


@dataclass
class HCLObject(HCLValue):
    """HCL object with named fields"""
    fields: Dict[str, HCLExpression]
    
    def accept(self, visitor: 'HCLVisitor') -> Any:
        return visitor.visit_object(self)


# Expressions
@dataclass
class HCLIdentifier(HCLExpression):
    """HCL identifier/variable reference"""
    name: str
    
    def accept(self, visitor: 'HCLVisitor') -> Any:
        return visitor.visit_identifier(self)


@dataclass
class HCLAttributeAccess(HCLExpression):
    """HCL attribute access (obj.attr)"""
    object: HCLExpression
    attribute: str
    
    def accept(self, visitor: 'HCLVisitor') -> Any:
        return visitor.visit_attribute_access(self)


@dataclass
class HCLIndexAccess(HCLExpression):
    """HCL index access (obj[index])"""
    object: HCLExpression
    index: HCLExpression
    
    def accept(self, visitor: 'HCLVisitor') -> Any:
        return visitor.visit_index_access(self)


@dataclass
class HCLFunctionCall(HCLExpression):
    """HCL function call"""
    name: str
    args: List[HCLExpression]
    
    def accept(self, visitor: 'HCLVisitor') -> Any:
        return visitor.visit_function_call(self)


@dataclass
class HCLBinaryOp(HCLExpression):
    """HCL binary operation"""
    left: HCLExpression
    operator: str
    right: HCLExpression
    
    def accept(self, visitor: 'HCLVisitor') -> Any:
        return visitor.visit_binary_op(self)


@dataclass
class HCLUnaryOp(HCLExpression):
    """HCL unary operation"""
    operator: str
    operand: HCLExpression
    
    def accept(self, visitor: 'HCLVisitor') -> Any:
        return visitor.visit_unary_op(self)


@dataclass
class HCLConditional(HCLExpression):
    """HCL conditional expression (condition ? true_val : false_val)"""
    condition: HCLExpression
    true_value: HCLExpression
    false_value: HCLExpression
    
    def accept(self, visitor: 'HCLVisitor') -> Any:
        return visitor.visit_conditional(self)


@dataclass
class HCLInterpolation(HCLExpression):
    """HCL string interpolation ${expression}"""
    expression: HCLExpression
    
    def accept(self, visitor: 'HCLVisitor') -> Any:
        return visitor.visit_interpolation(self)


@dataclass
class HCLForExpression(HCLExpression):
    """HCL for expression"""
    key_var: Optional[str]
    value_var: str
    collection: HCLExpression
    key_expr: Optional[HCLExpression]
    value_expr: HCLExpression
    condition: Optional[HCLExpression]
    is_object: bool = False  # True for {}, False for []
    
    def accept(self, visitor: 'HCLVisitor') -> Any:
        return visitor.visit_for_expression(self)


@dataclass
class HCLSplatExpression(HCLExpression):
    """HCL splat expression (list[*].attr)"""
    source: HCLExpression
    each: HCLExpression
    
    def accept(self, visitor: 'HCLVisitor') -> Any:
        return visitor.visit_splat_expression(self)


# Configuration Structure
@dataclass
class HCLAttribute(HCLStatement):
    """HCL attribute assignment"""
    name: str
    value: HCLExpression
    
    def accept(self, visitor: 'HCLVisitor') -> Any:
        return visitor.visit_attribute(self)


@dataclass
class HCLBlock(HCLStatement):
    """HCL configuration block"""
    type: str
    labels: List[str]
    body: List[Union['HCLAttribute', 'HCLBlock']]
    
    def accept(self, visitor: 'HCLVisitor') -> Any:
        return visitor.visit_block(self)


@dataclass
class HCLComment(HCLNode):
    """HCL comment"""
    text: str
    is_line_comment: bool = True  # True for //, False for /* */
    
    def accept(self, visitor: 'HCLVisitor') -> Any:
        return visitor.visit_comment(self)


# Top-level Configuration
@dataclass
class HCLConfiguration(HCLNode):
    """Complete HCL configuration file"""
    body: List[Union[HCLBlock, HCLAttribute, HCLComment]]
    filename: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    def accept(self, visitor: 'HCLVisitor') -> Any:
        return visitor.visit_configuration(self)


# Terraform-specific constructs
@dataclass
class HCLVariable(HCLBlock):
    """Terraform variable block"""
    name: str
    default: Optional[HCLExpression] = None
    type_constraint: Optional[str] = None
    description: Optional[str] = None
    validation: List['HCLValidation'] = None
    sensitive: bool = False
    nullable: bool = True
    
    def __post_init__(self):
        if self.validation is None:
            self.validation = []
    
    def accept(self, visitor: 'HCLVisitor') -> Any:
        return visitor.visit_variable(self)


@dataclass
class HCLLocal(HCLBlock):
    """Terraform locals block"""
    assignments: Dict[str, HCLExpression]
    
    def accept(self, visitor: 'HCLVisitor') -> Any:
        return visitor.visit_local(self)


@dataclass
class HCLOutput(HCLBlock):
    """Terraform output block"""
    name: str
    value: HCLExpression
    description: Optional[str] = None
    sensitive: bool = False
    depends_on: List[str] = None
    
    def __post_init__(self):
        if self.depends_on is None:
            self.depends_on = []
    
    def accept(self, visitor: 'HCLVisitor') -> Any:
        return visitor.visit_output(self)


@dataclass
class HCLResource(HCLBlock):
    """Terraform resource block"""
    type: str
    name: str
    provider: Optional[str] = None
    count: Optional[HCLExpression] = None
    for_each: Optional[HCLExpression] = None
    depends_on: List[str] = None
    lifecycle: Optional['HCLLifecycle'] = None
    
    def __post_init__(self):
        if self.depends_on is None:
            self.depends_on = []
    
    def accept(self, visitor: 'HCLVisitor') -> Any:
        return visitor.visit_resource(self)


@dataclass
class HCLDataSource(HCLBlock):
    """Terraform data source block"""
    type: str
    name: str
    provider: Optional[str] = None
    count: Optional[HCLExpression] = None
    for_each: Optional[HCLExpression] = None
    depends_on: List[str] = None
    
    def __post_init__(self):
        if self.depends_on is None:
            self.depends_on = []
    
    def accept(self, visitor: 'HCLVisitor') -> Any:
        return visitor.visit_data_source(self)


@dataclass
class HCLProvider(HCLBlock):
    """Terraform provider block"""
    name: str
    alias: Optional[str] = None
    version: Optional[str] = None
    
    def accept(self, visitor: 'HCLVisitor') -> Any:
        return visitor.visit_provider(self)


@dataclass
class HCLModule(HCLBlock):
    """Terraform module block"""
    name: str
    source: str
    version: Optional[str] = None
    
    def accept(self, visitor: 'HCLVisitor') -> Any:
        return visitor.visit_module(self)


@dataclass
class HCLValidation(HCLNode):
    """Terraform variable validation block"""
    condition: HCLExpression
    error_message: str
    
    def accept(self, visitor: 'HCLVisitor') -> Any:
        return visitor.visit_validation(self)


@dataclass
class HCLLifecycle(HCLNode):
    """Terraform lifecycle block"""
    create_before_destroy: bool = False
    prevent_destroy: bool = False
    ignore_changes: List[str] = None
    replace_triggered_by: List[str] = None
    
    def __post_init__(self):
        if self.ignore_changes is None:
            self.ignore_changes = []
        if self.replace_triggered_by is None:
            self.replace_triggered_by = []
    
    def accept(self, visitor: 'HCLVisitor') -> Any:
        return visitor.visit_lifecycle(self)


# Visitor Pattern
class HCLVisitor(ABC):
    """Abstract visitor for HCL AST traversal"""
    
    @abstractmethod
    def visit_configuration(self, node: HCLConfiguration) -> Any:
        pass
    
    @abstractmethod
    def visit_block(self, node: HCLBlock) -> Any:
        pass
    
    @abstractmethod
    def visit_attribute(self, node: HCLAttribute) -> Any:
        pass
    
    @abstractmethod
    def visit_literal(self, node: HCLLiteral) -> Any:
        pass
    
    @abstractmethod
    def visit_string(self, node: HCLString) -> Any:
        pass
    
    @abstractmethod
    def visit_number(self, node: HCLNumber) -> Any:
        pass
    
    @abstractmethod
    def visit_bool(self, node: HCLBool) -> Any:
        pass
    
    @abstractmethod
    def visit_null(self, node: HCLNull) -> Any:
        pass
    
    @abstractmethod
    def visit_list(self, node: HCLList) -> Any:
        pass
    
    @abstractmethod
    def visit_map(self, node: HCLMap) -> Any:
        pass
    
    @abstractmethod
    def visit_object(self, node: HCLObject) -> Any:
        pass
    
    @abstractmethod
    def visit_identifier(self, node: HCLIdentifier) -> Any:
        pass
    
    @abstractmethod
    def visit_attribute_access(self, node: HCLAttributeAccess) -> Any:
        pass
    
    @abstractmethod
    def visit_index_access(self, node: HCLIndexAccess) -> Any:
        pass
    
    @abstractmethod
    def visit_function_call(self, node: HCLFunctionCall) -> Any:
        pass
    
    @abstractmethod
    def visit_binary_op(self, node: HCLBinaryOp) -> Any:
        pass
    
    @abstractmethod
    def visit_unary_op(self, node: HCLUnaryOp) -> Any:
        pass
    
    @abstractmethod
    def visit_conditional(self, node: HCLConditional) -> Any:
        pass
    
    @abstractmethod
    def visit_interpolation(self, node: HCLInterpolation) -> Any:
        pass
    
    @abstractmethod
    def visit_for_expression(self, node: HCLForExpression) -> Any:
        pass
    
    @abstractmethod
    def visit_splat_expression(self, node: HCLSplatExpression) -> Any:
        pass
    
    @abstractmethod
    def visit_comment(self, node: HCLComment) -> Any:
        pass
    
    @abstractmethod
    def visit_variable(self, node: HCLVariable) -> Any:
        pass
    
    @abstractmethod
    def visit_local(self, node: HCLLocal) -> Any:
        pass
    
    @abstractmethod
    def visit_output(self, node: HCLOutput) -> Any:
        pass
    
    @abstractmethod
    def visit_resource(self, node: HCLResource) -> Any:
        pass
    
    @abstractmethod
    def visit_data_source(self, node: HCLDataSource) -> Any:
        pass
    
    @abstractmethod
    def visit_provider(self, node: HCLProvider) -> Any:
        pass
    
    @abstractmethod
    def visit_module(self, node: HCLModule) -> Any:
        pass
    
    @abstractmethod
    def visit_validation(self, node: HCLValidation) -> Any:
        pass
    
    @abstractmethod
    def visit_lifecycle(self, node: HCLLifecycle) -> Any:
        pass


class HCLBaseVisitor(HCLVisitor):
    """Base visitor with default implementations"""
    
    def visit_configuration(self, node: HCLConfiguration) -> Any:
        for item in node.body:
            item.accept(self)
    
    def visit_block(self, node: HCLBlock) -> Any:
        for item in node.body:
            item.accept(self)
    
    def visit_attribute(self, node: HCLAttribute) -> Any:
        node.value.accept(self)
    
    def visit_literal(self, node: HCLLiteral) -> Any:
        pass
    
    def visit_string(self, node: HCLString) -> Any:
        for part in node.parts:
            if isinstance(part, HCLInterpolation):
                part.accept(self)
    
    def visit_number(self, node: HCLNumber) -> Any:
        pass
    
    def visit_bool(self, node: HCLBool) -> Any:
        pass
    
    def visit_null(self, node: HCLNull) -> Any:
        pass
    
    def visit_list(self, node: HCLList) -> Any:
        for element in node.elements:
            element.accept(self)
    
    def visit_map(self, node: HCLMap) -> Any:
        for key, value in node.pairs:
            key.accept(self)
            value.accept(self)
    
    def visit_object(self, node: HCLObject) -> Any:
        for value in node.fields.values():
            value.accept(self)
    
    def visit_identifier(self, node: HCLIdentifier) -> Any:
        pass
    
    def visit_attribute_access(self, node: HCLAttributeAccess) -> Any:
        node.object.accept(self)
    
    def visit_index_access(self, node: HCLIndexAccess) -> Any:
        node.object.accept(self)
        node.index.accept(self)
    
    def visit_function_call(self, node: HCLFunctionCall) -> Any:
        for arg in node.args:
            arg.accept(self)
    
    def visit_binary_op(self, node: HCLBinaryOp) -> Any:
        node.left.accept(self)
        node.right.accept(self)
    
    def visit_unary_op(self, node: HCLUnaryOp) -> Any:
        node.operand.accept(self)
    
    def visit_conditional(self, node: HCLConditional) -> Any:
        node.condition.accept(self)
        node.true_value.accept(self)
        node.false_value.accept(self)
    
    def visit_interpolation(self, node: HCLInterpolation) -> Any:
        node.expression.accept(self)
    
    def visit_for_expression(self, node: HCLForExpression) -> Any:
        node.collection.accept(self)
        if node.key_expr:
            node.key_expr.accept(self)
        node.value_expr.accept(self)
        if node.condition:
            node.condition.accept(self)
    
    def visit_splat_expression(self, node: HCLSplatExpression) -> Any:
        node.source.accept(self)
        node.each.accept(self)
    
    def visit_comment(self, node: HCLComment) -> Any:
        pass
    
    def visit_variable(self, node: HCLVariable) -> Any:
        if node.default:
            node.default.accept(self)
        for validation in node.validation:
            validation.accept(self)
    
    def visit_local(self, node: HCLLocal) -> Any:
        for value in node.assignments.values():
            value.accept(self)
    
    def visit_output(self, node: HCLOutput) -> Any:
        node.value.accept(self)
    
    def visit_resource(self, node: HCLResource) -> Any:
        if node.count:
            node.count.accept(self)
        if node.for_each:
            node.for_each.accept(self)
        if node.lifecycle:
            node.lifecycle.accept(self)
        self.visit_block(node)
    
    def visit_data_source(self, node: HCLDataSource) -> Any:
        if node.count:
            node.count.accept(self)
        if node.for_each:
            node.for_each.accept(self)
        self.visit_block(node)
    
    def visit_provider(self, node: HCLProvider) -> Any:
        self.visit_block(node)
    
    def visit_module(self, node: HCLModule) -> Any:
        self.visit_block(node)
    
    def visit_validation(self, node: HCLValidation) -> Any:
        node.condition.accept(self)
    
    def visit_lifecycle(self, node: HCLLifecycle) -> Any:
        pass


# Built-in Functions
HCL_BUILTIN_FUNCTIONS = {
    # Numeric functions
    "abs", "ceil", "floor", "log", "max", "min", "parseint", "pow", "signum",
    
    # String functions
    "chomp", "format", "formatlist", "indent", "join", "lower", "regex", 
    "regexall", "replace", "split", "strrev", "substr", "title", "trim",
    "trimprefix", "trimsuffix", "trimspace", "upper",
    
    # Collection functions
    "alltrue", "anytrue", "chunklist", "coalesce", "coalescelist", "compact",
    "concat", "contains", "distinct", "element", "flatten", "index", "keys",
    "length", "list", "lookup", "map", "matchkeys", "merge", "range", "reverse",
    "setintersection", "setproduct", "setsubtract", "setunion", "slice", "sort",
    "sum", "transpose", "values", "zipmap",
    
    # Encoding functions
    "base64decode", "base64encode", "base64gzip", "csvdecode", "jsondecode",
    "jsonencode", "textdecodebase64", "textencodebase64", "urlencode", "yamldecode",
    "yamlencode",
    
    # Filesystem functions
    "abspath", "dirname", "pathexpand", "basename", "file", "fileexists",
    "fileset", "filebase64", "templatefile",
    
    # Date/time functions
    "formatdate", "timeadd", "timestamp",
    
    # Hash/crypto functions
    "base64sha256", "base64sha512", "bcrypt", "filebase64sha256", "filebase64sha512",
    "filemd5", "filesha1", "filesha256", "filesha512", "md5", "rsadecrypt", "sha1",
    "sha256", "sha512", "uuid", "uuidv5",
    
    # IP network functions
    "cidrhost", "cidrnetmask", "cidrsubnet", "cidrsubnets",
    
    # Type conversion functions
    "can", "nonsensitive", "sensitive", "tobool", "tolist", "tomap", "tonumber",
    "toset", "tostring", "try", "type"
}

# Common HCL block types
HCL_BLOCK_TYPES = {
    "terraform", "provider", "resource", "data", "variable", "locals", "output",
    "module", "moved", "import", "check", "removed"
} 