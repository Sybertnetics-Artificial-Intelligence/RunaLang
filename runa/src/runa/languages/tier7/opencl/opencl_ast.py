#!/usr/bin/env python3
"""
OpenCL AST - Abstract Syntax Tree for OpenCL C Language

Provides comprehensive AST node definitions for OpenCL C including:
- Device/host code separation
- Kernel functions and execution model
- Memory space qualifiers (__global, __local, __private, __constant)
- Vector types and operations
- Work item and work group functions
- Built-in functions and operators
- Synchronization primitives
- OpenCL C extensions and features

Supports OpenCL C 1.0 through OpenCL C 3.0 specifications.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any, Union
from enum import Enum
from dataclasses import dataclass


class OpenCLNode(ABC):
    """Base class for all OpenCL AST nodes"""
    
    def __init__(self, location: Optional[Dict[str, Any]] = None):
        self.location = location or {}
        self.parent: Optional['OpenCLNode'] = None
        self.children: List['OpenCLNode'] = []
    
    @abstractmethod
    def accept(self, visitor: 'OpenCLVisitor') -> Any:
        """Accept visitor pattern implementation"""
        pass
    
    def add_child(self, child: 'OpenCLNode') -> None:
        """Add child node"""
        if child:
            child.parent = self
            self.children.append(child)


class OpenCLExpression(OpenCLNode):
    """Base class for all OpenCL expressions"""
    pass


class OpenCLStatement(OpenCLNode):
    """Base class for all OpenCL statements"""
    pass


class OpenCLDeclaration(OpenCLNode):
    """Base class for all OpenCL declarations"""
    pass


class OpenCLType(OpenCLNode):
    """Base class for all OpenCL type nodes"""
    pass


# Address Space Qualifiers
class AddressSpace(Enum):
    """OpenCL address space qualifiers"""
    GLOBAL = "__global"
    LOCAL = "__local"
    PRIVATE = "__private"
    CONSTANT = "__constant"
    GENERIC = "__generic"


class AccessQualifier(Enum):
    """OpenCL image access qualifiers"""
    READ_ONLY = "__read_only"
    WRITE_ONLY = "__write_only"
    READ_WRITE = "__read_write"


class FunctionQualifier(Enum):
    """OpenCL function qualifiers"""
    KERNEL = "__kernel"
    INLINE = "inline"


# Built-in Types
@dataclass
class OpenCLBuiltinType(OpenCLType):
    """OpenCL built-in scalar and vector types"""
    name: str
    vector_size: Optional[int] = None  # None for scalar, 2,3,4,8,16 for vectors
    
    def accept(self, visitor: 'OpenCLVisitor') -> Any:
        return visitor.visit_builtin_type(self)


@dataclass
class OpenCLPointerType(OpenCLType):
    """OpenCL pointer type with address space"""
    base_type: OpenCLType
    address_space: Optional[AddressSpace] = None
    
    def accept(self, visitor: 'OpenCLVisitor') -> Any:
        return visitor.visit_pointer_type(self)


@dataclass
class OpenCLArrayType(OpenCLType):
    """OpenCL array type"""
    element_type: OpenCLType
    size: Optional[OpenCLExpression] = None  # None for unsized arrays
    
    def accept(self, visitor: 'OpenCLVisitor') -> Any:
        return visitor.visit_array_type(self)


@dataclass
class OpenCLImageType(OpenCLType):
    """OpenCL image types"""
    dimension: str  # "1d", "2d", "3d", "1d_array", "2d_array", "1d_buffer"
    access_qualifier: Optional[AccessQualifier] = None
    
    def accept(self, visitor: 'OpenCLVisitor') -> Any:
        return visitor.visit_image_type(self)


# Expressions
@dataclass
class OpenCLIdentifier(OpenCLExpression):
    """OpenCL identifier"""
    name: str
    
    def accept(self, visitor: 'OpenCLVisitor') -> Any:
        return visitor.visit_identifier(self)


@dataclass
class OpenCLLiteral(OpenCLExpression):
    """OpenCL literal values"""
    value: Any
    type_hint: Optional[str] = None
    
    def accept(self, visitor: 'OpenCLVisitor') -> Any:
        return visitor.visit_literal(self)


@dataclass
class OpenCLVectorLiteral(OpenCLExpression):
    """OpenCL vector constructor expressions"""
    type_name: str
    components: List[OpenCLExpression]
    
    def accept(self, visitor: 'OpenCLVisitor') -> Any:
        return visitor.visit_vector_literal(self)


@dataclass
class OpenCLBinaryOp(OpenCLExpression):
    """OpenCL binary operations"""
    left: OpenCLExpression
    operator: str
    right: OpenCLExpression
    
    def accept(self, visitor: 'OpenCLVisitor') -> Any:
        return visitor.visit_binary_op(self)


@dataclass
class OpenCLUnaryOp(OpenCLExpression):
    """OpenCL unary operations"""
    operator: str
    operand: OpenCLExpression
    
    def accept(self, visitor: 'OpenCLVisitor') -> Any:
        return visitor.visit_unary_op(self)


@dataclass
class OpenCLArrayAccess(OpenCLExpression):
    """OpenCL array/vector element access"""
    array: OpenCLExpression
    index: OpenCLExpression
    
    def accept(self, visitor: 'OpenCLVisitor') -> Any:
        return visitor.visit_array_access(self)


@dataclass
class OpenCLFieldAccess(OpenCLExpression):
    """OpenCL struct field or vector component access"""
    object: OpenCLExpression
    field: str
    
    def accept(self, visitor: 'OpenCLVisitor') -> Any:
        return visitor.visit_field_access(self)


@dataclass
class OpenCLFunctionCall(OpenCLExpression):
    """OpenCL function call"""
    name: str
    args: List[OpenCLExpression]
    
    def accept(self, visitor: 'OpenCLVisitor') -> Any:
        return visitor.visit_function_call(self)


@dataclass
class OpenCLBuiltinCall(OpenCLExpression):
    """OpenCL built-in function call"""
    name: str
    args: List[OpenCLExpression]
    category: str  # "work_item", "math", "geometric", "relational", etc.
    
    def accept(self, visitor: 'OpenCLVisitor') -> Any:
        return visitor.visit_builtin_call(self)


@dataclass
class OpenCLCast(OpenCLExpression):
    """OpenCL type cast or conversion"""
    target_type: OpenCLType
    expression: OpenCLExpression
    explicit: bool = True
    
    def accept(self, visitor: 'OpenCLVisitor') -> Any:
        return visitor.visit_cast(self)


@dataclass
class OpenCLConditional(OpenCLExpression):
    """OpenCL ternary conditional operator"""
    condition: OpenCLExpression
    true_expr: OpenCLExpression
    false_expr: OpenCLExpression
    
    def accept(self, visitor: 'OpenCLVisitor') -> Any:
        return visitor.visit_conditional(self)


# Statements
@dataclass
class OpenCLExpressionStatement(OpenCLStatement):
    """OpenCL expression statement"""
    expression: OpenCLExpression
    
    def accept(self, visitor: 'OpenCLVisitor') -> Any:
        return visitor.visit_expression_statement(self)


@dataclass
class OpenCLBlock(OpenCLStatement):
    """OpenCL compound statement/block"""
    statements: List[OpenCLStatement]
    
    def accept(self, visitor: 'OpenCLVisitor') -> Any:
        return visitor.visit_block(self)


@dataclass
class OpenCLIfStatement(OpenCLStatement):
    """OpenCL if statement"""
    condition: OpenCLExpression
    then_stmt: OpenCLStatement
    else_stmt: Optional[OpenCLStatement] = None
    
    def accept(self, visitor: 'OpenCLVisitor') -> Any:
        return visitor.visit_if_statement(self)


@dataclass
class OpenCLWhileLoop(OpenCLStatement):
    """OpenCL while loop"""
    condition: OpenCLExpression
    body: OpenCLStatement
    
    def accept(self, visitor: 'OpenCLVisitor') -> Any:
        return visitor.visit_while_loop(self)


@dataclass
class OpenCLForLoop(OpenCLStatement):
    """OpenCL for loop"""
    init: Optional[OpenCLStatement]
    condition: Optional[OpenCLExpression]
    update: Optional[OpenCLExpression]
    body: OpenCLStatement
    
    def accept(self, visitor: 'OpenCLVisitor') -> Any:
        return visitor.visit_for_loop(self)


@dataclass
class OpenCLDoWhileLoop(OpenCLStatement):
    """OpenCL do-while loop"""
    body: OpenCLStatement
    condition: OpenCLExpression
    
    def accept(self, visitor: 'OpenCLVisitor') -> Any:
        return visitor.visit_do_while_loop(self)


@dataclass
class OpenCLBreakStatement(OpenCLStatement):
    """OpenCL break statement"""
    
    def accept(self, visitor: 'OpenCLVisitor') -> Any:
        return visitor.visit_break_statement(self)


@dataclass
class OpenCLContinueStatement(OpenCLStatement):
    """OpenCL continue statement"""
    
    def accept(self, visitor: 'OpenCLVisitor') -> Any:
        return visitor.visit_continue_statement(self)


@dataclass
class OpenCLReturnStatement(OpenCLStatement):
    """OpenCL return statement"""
    value: Optional[OpenCLExpression] = None
    
    def accept(self, visitor: 'OpenCLVisitor') -> Any:
        return visitor.visit_return_statement(self)


@dataclass
class OpenCLBarrier(OpenCLStatement):
    """OpenCL barrier synchronization"""
    memory_fence: str  # "CLK_LOCAL_MEM_FENCE", "CLK_GLOBAL_MEM_FENCE", etc.
    
    def accept(self, visitor: 'OpenCLVisitor') -> Any:
        return visitor.visit_barrier(self)


# Declarations
@dataclass
class OpenCLVariableDeclaration(OpenCLDeclaration):
    """OpenCL variable declaration"""
    type: OpenCLType
    name: str
    address_space: Optional[AddressSpace] = None
    initializer: Optional[OpenCLExpression] = None
    is_const: bool = False
    
    def accept(self, visitor: 'OpenCLVisitor') -> Any:
        return visitor.visit_variable_declaration(self)


@dataclass
class OpenCLParameter(OpenCLNode):
    """OpenCL function parameter"""
    type: OpenCLType
    name: str
    address_space: Optional[AddressSpace] = None
    access_qualifier: Optional[AccessQualifier] = None
    is_const: bool = False
    
    def accept(self, visitor: 'OpenCLVisitor') -> Any:
        return visitor.visit_parameter(self)


@dataclass
class OpenCLFunctionDeclaration(OpenCLDeclaration):
    """OpenCL function declaration"""
    return_type: OpenCLType
    name: str
    parameters: List[OpenCLParameter]
    qualifiers: List[FunctionQualifier]
    body: Optional[OpenCLBlock] = None
    
    def accept(self, visitor: 'OpenCLVisitor') -> Any:
        return visitor.visit_function_declaration(self)


@dataclass
class OpenCLKernelDeclaration(OpenCLDeclaration):
    """OpenCL kernel function declaration"""
    return_type: OpenCLType
    name: str
    parameters: List[OpenCLParameter]
    body: OpenCLBlock
    attributes: Dict[str, Any]
    
    def accept(self, visitor: 'OpenCLVisitor') -> Any:
        return visitor.visit_kernel_declaration(self)


@dataclass
class OpenCLStructDeclaration(OpenCLDeclaration):
    """OpenCL struct declaration"""
    name: str
    fields: List[OpenCLVariableDeclaration]
    is_packed: bool = False
    
    def accept(self, visitor: 'OpenCLVisitor') -> Any:
        return visitor.visit_struct_declaration(self)


@dataclass
class OpenCLTypedefDeclaration(OpenCLDeclaration):
    """OpenCL typedef declaration"""
    type: OpenCLType
    name: str
    
    def accept(self, visitor: 'OpenCLVisitor') -> Any:
        return visitor.visit_typedef_declaration(self)


@dataclass
class OpenCLEnumDeclaration(OpenCLDeclaration):
    """OpenCL enum declaration"""
    name: Optional[str]
    values: List[tuple[str, Optional[OpenCLExpression]]]  # (name, value)
    
    def accept(self, visitor: 'OpenCLVisitor') -> Any:
        return visitor.visit_enum_declaration(self)


# Preprocessor and Attributes
@dataclass
class OpenCLPreprocessorDirective(OpenCLNode):
    """OpenCL preprocessor directive"""
    directive: str
    content: str
    
    def accept(self, visitor: 'OpenCLVisitor') -> Any:
        return visitor.visit_preprocessor_directive(self)


@dataclass
class OpenCLAttribute(OpenCLNode):
    """OpenCL attribute specification"""
    name: str
    args: List[str]
    
    def accept(self, visitor: 'OpenCLVisitor') -> Any:
        return visitor.visit_attribute(self)


# Program Structure
@dataclass
class OpenCLProgram(OpenCLNode):
    """Complete OpenCL program"""
    declarations: List[OpenCLDeclaration]
    preprocessor_directives: List[OpenCLPreprocessorDirective]
    metadata: Dict[str, Any]
    
    def accept(self, visitor: 'OpenCLVisitor') -> Any:
        return visitor.visit_program(self)


# Visitor Pattern
class OpenCLVisitor(ABC):
    """Abstract visitor for OpenCL AST traversal"""
    
    @abstractmethod
    def visit_program(self, node: OpenCLProgram) -> Any:
        pass
    
    @abstractmethod
    def visit_builtin_type(self, node: OpenCLBuiltinType) -> Any:
        pass
    
    @abstractmethod
    def visit_pointer_type(self, node: OpenCLPointerType) -> Any:
        pass
    
    @abstractmethod
    def visit_array_type(self, node: OpenCLArrayType) -> Any:
        pass
    
    @abstractmethod
    def visit_image_type(self, node: OpenCLImageType) -> Any:
        pass
    
    @abstractmethod
    def visit_identifier(self, node: OpenCLIdentifier) -> Any:
        pass
    
    @abstractmethod
    def visit_literal(self, node: OpenCLLiteral) -> Any:
        pass
    
    @abstractmethod
    def visit_vector_literal(self, node: OpenCLVectorLiteral) -> Any:
        pass
    
    @abstractmethod
    def visit_binary_op(self, node: OpenCLBinaryOp) -> Any:
        pass
    
    @abstractmethod
    def visit_unary_op(self, node: OpenCLUnaryOp) -> Any:
        pass
    
    @abstractmethod
    def visit_array_access(self, node: OpenCLArrayAccess) -> Any:
        pass
    
    @abstractmethod
    def visit_field_access(self, node: OpenCLFieldAccess) -> Any:
        pass
    
    @abstractmethod
    def visit_function_call(self, node: OpenCLFunctionCall) -> Any:
        pass
    
    @abstractmethod
    def visit_builtin_call(self, node: OpenCLBuiltinCall) -> Any:
        pass
    
    @abstractmethod
    def visit_cast(self, node: OpenCLCast) -> Any:
        pass
    
    @abstractmethod
    def visit_conditional(self, node: OpenCLConditional) -> Any:
        pass
    
    @abstractmethod
    def visit_expression_statement(self, node: OpenCLExpressionStatement) -> Any:
        pass
    
    @abstractmethod
    def visit_block(self, node: OpenCLBlock) -> Any:
        pass
    
    @abstractmethod
    def visit_if_statement(self, node: OpenCLIfStatement) -> Any:
        pass
    
    @abstractmethod
    def visit_while_loop(self, node: OpenCLWhileLoop) -> Any:
        pass
    
    @abstractmethod
    def visit_for_loop(self, node: OpenCLForLoop) -> Any:
        pass
    
    @abstractmethod
    def visit_do_while_loop(self, node: OpenCLDoWhileLoop) -> Any:
        pass
    
    @abstractmethod
    def visit_break_statement(self, node: OpenCLBreakStatement) -> Any:
        pass
    
    @abstractmethod
    def visit_continue_statement(self, node: OpenCLContinueStatement) -> Any:
        pass
    
    @abstractmethod
    def visit_return_statement(self, node: OpenCLReturnStatement) -> Any:
        pass
    
    @abstractmethod
    def visit_barrier(self, node: OpenCLBarrier) -> Any:
        pass
    
    @abstractmethod
    def visit_variable_declaration(self, node: OpenCLVariableDeclaration) -> Any:
        pass
    
    @abstractmethod
    def visit_parameter(self, node: OpenCLParameter) -> Any:
        pass
    
    @abstractmethod
    def visit_function_declaration(self, node: OpenCLFunctionDeclaration) -> Any:
        pass
    
    @abstractmethod
    def visit_kernel_declaration(self, node: OpenCLKernelDeclaration) -> Any:
        pass
    
    @abstractmethod
    def visit_struct_declaration(self, node: OpenCLStructDeclaration) -> Any:
        pass
    
    @abstractmethod
    def visit_typedef_declaration(self, node: OpenCLTypedefDeclaration) -> Any:
        pass
    
    @abstractmethod
    def visit_enum_declaration(self, node: OpenCLEnumDeclaration) -> Any:
        pass
    
    @abstractmethod
    def visit_preprocessor_directive(self, node: OpenCLPreprocessorDirective) -> Any:
        pass
    
    @abstractmethod
    def visit_attribute(self, node: OpenCLAttribute) -> Any:
        pass


class OpenCLBaseVisitor(OpenCLVisitor):
    """Base visitor with default implementations"""
    
    def visit_program(self, node: OpenCLProgram) -> Any:
        for decl in node.declarations:
            decl.accept(self)
        for directive in node.preprocessor_directives:
            directive.accept(self)
    
    def visit_builtin_type(self, node: OpenCLBuiltinType) -> Any:
        pass
    
    def visit_pointer_type(self, node: OpenCLPointerType) -> Any:
        node.base_type.accept(self)
    
    def visit_array_type(self, node: OpenCLArrayType) -> Any:
        node.element_type.accept(self)
        if node.size:
            node.size.accept(self)
    
    def visit_image_type(self, node: OpenCLImageType) -> Any:
        pass
    
    def visit_identifier(self, node: OpenCLIdentifier) -> Any:
        pass
    
    def visit_literal(self, node: OpenCLLiteral) -> Any:
        pass
    
    def visit_vector_literal(self, node: OpenCLVectorLiteral) -> Any:
        for component in node.components:
            component.accept(self)
    
    def visit_binary_op(self, node: OpenCLBinaryOp) -> Any:
        node.left.accept(self)
        node.right.accept(self)
    
    def visit_unary_op(self, node: OpenCLUnaryOp) -> Any:
        node.operand.accept(self)
    
    def visit_array_access(self, node: OpenCLArrayAccess) -> Any:
        node.array.accept(self)
        node.index.accept(self)
    
    def visit_field_access(self, node: OpenCLFieldAccess) -> Any:
        node.object.accept(self)
    
    def visit_function_call(self, node: OpenCLFunctionCall) -> Any:
        for arg in node.args:
            arg.accept(self)
    
    def visit_builtin_call(self, node: OpenCLBuiltinCall) -> Any:
        for arg in node.args:
            arg.accept(self)
    
    def visit_cast(self, node: OpenCLCast) -> Any:
        node.target_type.accept(self)
        node.expression.accept(self)
    
    def visit_conditional(self, node: OpenCLConditional) -> Any:
        node.condition.accept(self)
        node.true_expr.accept(self)
        node.false_expr.accept(self)
    
    def visit_expression_statement(self, node: OpenCLExpressionStatement) -> Any:
        node.expression.accept(self)
    
    def visit_block(self, node: OpenCLBlock) -> Any:
        for stmt in node.statements:
            stmt.accept(self)
    
    def visit_if_statement(self, node: OpenCLIfStatement) -> Any:
        node.condition.accept(self)
        node.then_stmt.accept(self)
        if node.else_stmt:
            node.else_stmt.accept(self)
    
    def visit_while_loop(self, node: OpenCLWhileLoop) -> Any:
        node.condition.accept(self)
        node.body.accept(self)
    
    def visit_for_loop(self, node: OpenCLForLoop) -> Any:
        if node.init:
            node.init.accept(self)
        if node.condition:
            node.condition.accept(self)
        if node.update:
            node.update.accept(self)
        node.body.accept(self)
    
    def visit_do_while_loop(self, node: OpenCLDoWhileLoop) -> Any:
        node.body.accept(self)
        node.condition.accept(self)
    
    def visit_break_statement(self, node: OpenCLBreakStatement) -> Any:
        pass
    
    def visit_continue_statement(self, node: OpenCLContinueStatement) -> Any:
        pass
    
    def visit_return_statement(self, node: OpenCLReturnStatement) -> Any:
        if node.value:
            node.value.accept(self)
    
    def visit_barrier(self, node: OpenCLBarrier) -> Any:
        pass
    
    def visit_variable_declaration(self, node: OpenCLVariableDeclaration) -> Any:
        node.type.accept(self)
        if node.initializer:
            node.initializer.accept(self)
    
    def visit_parameter(self, node: OpenCLParameter) -> Any:
        node.type.accept(self)
    
    def visit_function_declaration(self, node: OpenCLFunctionDeclaration) -> Any:
        node.return_type.accept(self)
        for param in node.parameters:
            param.accept(self)
        if node.body:
            node.body.accept(self)
    
    def visit_kernel_declaration(self, node: OpenCLKernelDeclaration) -> Any:
        node.return_type.accept(self)
        for param in node.parameters:
            param.accept(self)
        node.body.accept(self)
    
    def visit_struct_declaration(self, node: OpenCLStructDeclaration) -> Any:
        for field in node.fields:
            field.accept(self)
    
    def visit_typedef_declaration(self, node: OpenCLTypedefDeclaration) -> Any:
        node.type.accept(self)
    
    def visit_enum_declaration(self, node: OpenCLEnumDeclaration) -> Any:
        for name, value in node.values:
            if value:
                value.accept(self)
    
    def visit_preprocessor_directive(self, node: OpenCLPreprocessorDirective) -> Any:
        pass
    
    def visit_attribute(self, node: OpenCLAttribute) -> Any:
        pass


# Built-in Function Categories
OPENCL_BUILTIN_FUNCTIONS = {
    "work_item": [
        "get_work_dim", "get_global_size", "get_global_id", "get_local_size",
        "get_local_id", "get_num_groups", "get_group_id", "get_global_offset"
    ],
    "math": [
        "cos", "sin", "tan", "acos", "asin", "atan", "atan2", "cosh", "sinh", "tanh",
        "exp", "exp2", "exp10", "expm1", "log", "log2", "log10", "log1p", "logb",
        "sqrt", "rsqrt", "cbrt", "pow", "pown", "powr", "ceil", "floor", "trunc",
        "round", "rint", "fabs", "fmin", "fmax", "fmod", "remainder", "remquo",
        "copysign", "nan", "nextafter", "fdim", "fma", "frexp", "ldexp", "modf",
        "ilogb", "scalb", "hypot", "erf", "erfc", "gamma", "lgamma"
    ],
    "geometric": [
        "cross", "dot", "distance", "length", "normalize", "fast_distance",
        "fast_length", "fast_normalize"
    ],
    "relational": [
        "isequal", "isnotequal", "isgreater", "isgreaterequal", "isless",
        "islessequal", "islessgreater", "isfinite", "isinf", "isnan", "isnormal",
        "isordered", "isunordered", "signbit", "any", "all", "bitselect", "select"
    ],
    "vector": [
        "vload2", "vload3", "vload4", "vload8", "vload16", "vloada_half2",
        "vloada_half3", "vloada_half4", "vloada_half8", "vloada_half16",
        "vstore2", "vstore3", "vstore4", "vstore8", "vstore16", "vstorea_half2",
        "vstorea_half3", "vstorea_half4", "vstorea_half8", "vstorea_half16",
        "shuffle", "shuffle2"
    ],
    "synchronization": [
        "barrier", "mem_fence", "read_mem_fence", "write_mem_fence"
    ],
    "atomic": [
        "atomic_add", "atomic_sub", "atomic_xchg", "atomic_inc", "atomic_dec",
        "atomic_cmpxchg", "atomic_min", "atomic_max", "atomic_and", "atomic_or",
        "atomic_xor"
    ],
    "image": [
        "read_imagef", "read_imagei", "read_imageui", "write_imagef", "write_imagei",
        "write_imageui", "get_image_width", "get_image_height", "get_image_depth",
        "get_image_channel_data_type", "get_image_channel_order", "get_image_dim"
    ]
}

# OpenCL Built-in Types
OPENCL_BUILTIN_TYPES = {
    "scalar": [
        "bool", "char", "uchar", "short", "ushort", "int", "uint", "long", "ulong",
        "float", "double", "half", "size_t", "ptrdiff_t", "intptr_t", "uintptr_t",
        "void"
    ],
    "vector": [
        "char2", "char3", "char4", "char8", "char16",
        "uchar2", "uchar3", "uchar4", "uchar8", "uchar16",
        "short2", "short3", "short4", "short8", "short16",
        "ushort2", "ushort3", "ushort4", "ushort8", "ushort16",
        "int2", "int3", "int4", "int8", "int16",
        "uint2", "uint3", "uint4", "uint8", "uint16",
        "long2", "long3", "long4", "long8", "long16",
        "ulong2", "ulong3", "ulong4", "ulong8", "ulong16",
        "float2", "float3", "float4", "float8", "float16",
        "double2", "double3", "double4", "double8", "double16",
        "half2", "half3", "half4", "half8", "half16"
    ],
    "image": [
        "image1d_t", "image1d_buffer_t", "image1d_array_t",
        "image2d_t", "image2d_array_t", "image3d_t",
        "sampler_t"
    ],
    "other": [
        "event_t", "cl_mem_fence_flags"
    ]
} 