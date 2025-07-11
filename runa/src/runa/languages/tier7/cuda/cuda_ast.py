#!/usr/bin/env python3
"""
CUDA AST - Abstract Syntax Tree for CUDA C++ Language

Comprehensive AST representation supporting:
- CUDA kernel functions (__global__, __device__, __host__)
- GPU memory management (device, shared, constant, texture)
- Execution configuration and thread indexing
- CUDA runtime API calls and synchronization
- Device properties and capabilities
- Streams, events, and asynchronous execution
- NVCC compiler directives and optimization
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from enum import Enum

# Base AST Node Classes

class CudaMemorySpace(Enum):
    """CUDA memory space qualifiers"""
    GLOBAL = "__global__"
    DEVICE = "__device__"
    CONSTANT = "__constant__"
    SHARED = "__shared__"
    TEXTURE = "__texture__"
    SURFACE = "__surface__"

class CudaExecutionSpace(Enum):
    """CUDA execution space qualifiers"""
    GLOBAL = "__global__"      # Kernel function
    DEVICE = "__device__"      # Device function
    HOST = "__host__"          # Host function
    HOST_DEVICE = "__host__ __device__"  # Both

class CudaArchitecture(Enum):
    """CUDA compute architectures"""
    FERMI = "sm_20"
    KEPLER = "sm_30"
    KEPLER_K80 = "sm_37"
    MAXWELL = "sm_50"
    MAXWELL_TITAN = "sm_52"
    PASCAL = "sm_60"
    PASCAL_P100 = "sm_60"
    VOLTA = "sm_70"
    TURING = "sm_75"
    AMPERE = "sm_80"
    AMPERE_A100 = "sm_80"
    ADA_LOVELACE = "sm_89"
    HOPPER = "sm_90"

@dataclass
class CudaNode(ABC):
    """Base class for all CUDA AST nodes"""
    line_number: int = 0
    column_number: int = 0
    source_file: Optional[str] = None
    
    @abstractmethod
    def accept(self, visitor: 'CudaVisitor') -> Any:
        """Accept visitor for traversal"""
        pass

@dataclass 
class CudaExpression(CudaNode):
    """Base class for CUDA expressions"""
    pass

@dataclass
class CudaStatement(CudaNode):
    """Base class for CUDA statements"""
    pass

@dataclass
class CudaDeclaration(CudaNode):
    """Base class for CUDA declarations"""
    pass

@dataclass
class CudaType(CudaNode):
    """Base class for CUDA types"""
    pass

# Core AST Node Types

@dataclass
class CudaTranslationUnit(CudaNode):
    """Root node representing a complete CUDA source file"""
    declarations: List[CudaDeclaration] = field(default_factory=list)
    includes: List['IncludeDirective'] = field(default_factory=list)
    cuda_runtime_version: Optional[str] = None
    target_architectures: List[CudaArchitecture] = field(default_factory=list)
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_cuda_translation_unit(self)

# CUDA-specific Declarations

@dataclass
class KernelFunction(CudaDeclaration):
    """CUDA kernel function declaration"""
    name: str
    parameters: List['ParameterDeclaration'] = field(default_factory=list)
    body: 'CompoundStatement'
    execution_space: CudaExecutionSpace = CudaExecutionSpace.GLOBAL
    return_type: CudaType = None
    attributes: List['CudaAttribute'] = field(default_factory=list)
    template_parameters: List['TemplateParameter'] = field(default_factory=list)
    launch_bounds: Optional['LaunchBounds'] = None
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_kernel_function(self)

@dataclass
class DeviceFunction(CudaDeclaration):
    """CUDA device function declaration"""
    name: str
    parameters: List['ParameterDeclaration'] = field(default_factory=list)
    body: 'CompoundStatement'
    execution_space: CudaExecutionSpace = CudaExecutionSpace.DEVICE
    return_type: CudaType = None
    attributes: List['CudaAttribute'] = field(default_factory=list)
    is_inline: bool = False
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_device_function(self)

@dataclass
class DeviceVariable(CudaDeclaration):
    """CUDA device variable declaration"""
    name: str
    type: CudaType
    memory_space: CudaMemorySpace
    initial_value: Optional[CudaExpression] = None
    is_constant: bool = False
    is_extern: bool = False
    array_size: Optional[CudaExpression] = None
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_device_variable(self)

@dataclass
class SharedMemoryDeclaration(CudaDeclaration):
    """Shared memory variable declaration"""
    name: str
    type: CudaType
    size: Optional[CudaExpression] = None  # For dynamic shared memory
    is_extern: bool = False
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_shared_memory_declaration(self)

@dataclass
class TextureDeclaration(CudaDeclaration):
    """Texture memory declaration"""
    name: str
    type: CudaType
    dimensions: int = 1  # 1D, 2D, or 3D
    is_layered: bool = False
    is_normalized: bool = False
    address_mode: str = "clamp"
    filter_mode: str = "point"
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_texture_declaration(self)

# CUDA Expressions

@dataclass
class KernelLaunch(CudaExpression):
    """CUDA kernel launch expression"""
    kernel_name: str
    execution_config: 'ExecutionConfiguration'
    arguments: List[CudaExpression] = field(default_factory=list)
    stream: Optional[CudaExpression] = None
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_kernel_launch(self)

@dataclass
class ExecutionConfiguration(CudaExpression):
    """CUDA execution configuration <<<...>>>"""
    grid_dim: CudaExpression
    block_dim: CudaExpression
    shared_mem_size: Optional[CudaExpression] = None
    stream: Optional[CudaExpression] = None
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_execution_configuration(self)

@dataclass
class ThreadIndex(CudaExpression):
    """CUDA thread indexing (threadIdx, blockIdx, etc.)"""
    index_type: str  # threadIdx, blockIdx, blockDim, gridDim
    dimension: str   # x, y, z
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_thread_index(self)

@dataclass
class CudaBuiltinCall(CudaExpression):
    """CUDA built-in function call"""
    function_name: str
    arguments: List[CudaExpression] = field(default_factory=list)
    return_type: Optional[CudaType] = None
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_cuda_builtin_call(self)

@dataclass
class MemoryTransfer(CudaExpression):
    """CUDA memory transfer (cudaMemcpy, etc.)"""
    destination: CudaExpression
    source: CudaExpression
    size: CudaExpression
    direction: str  # H2D, D2H, D2D, H2H
    is_async: bool = False
    stream: Optional[CudaExpression] = None
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_memory_transfer(self)

@dataclass
class MemoryAllocation(CudaExpression):
    """CUDA memory allocation (cudaMalloc, etc.)"""
    pointer: CudaExpression
    size: CudaExpression
    memory_type: str = "device"  # device, host, managed, pinned
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_memory_allocation(self)

@dataclass
class SynchronizationCall(CudaExpression):
    """CUDA synchronization call"""
    sync_type: str  # __syncthreads, cudaDeviceSynchronize, etc.
    arguments: List[CudaExpression] = field(default_factory=list)
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_synchronization_call(self)

@dataclass
class AtomicOperation(CudaExpression):
    """CUDA atomic operation"""
    operation: str  # atomicAdd, atomicCAS, etc.
    address: CudaExpression
    operands: List[CudaExpression] = field(default_factory=list)
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_atomic_operation(self)

@dataclass
class WarpShuffle(CudaExpression):
    """CUDA warp shuffle operation"""
    operation: str  # __shfl, __shfl_up, __shfl_down, etc.
    variable: CudaExpression
    lane_id: CudaExpression
    width: Optional[CudaExpression] = None
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_warp_shuffle(self)

@dataclass
class TextureAccess(CudaExpression):
    """Texture memory access"""
    texture_name: str
    coordinates: List[CudaExpression]
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_texture_access(self)

# CUDA Statements

@dataclass
class KernelLaunchStatement(CudaStatement):
    """CUDA kernel launch as statement"""
    kernel_launch: KernelLaunch
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_kernel_launch_statement(self)

@dataclass
class MemoryTransferStatement(CudaStatement):
    """Memory transfer as statement"""
    transfer: MemoryTransfer
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_memory_transfer_statement(self)

@dataclass
class SynchronizationStatement(CudaStatement):
    """Synchronization as statement"""
    sync_call: SynchronizationCall
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_synchronization_statement(self)

@dataclass
class ErrorCheckStatement(CudaStatement):
    """CUDA error checking statement"""
    cuda_call: CudaExpression
    error_handling: Optional[CudaStatement] = None
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_error_check_statement(self)

# CUDA Types

@dataclass
class CudaVectorType(CudaType):
    """CUDA vector types (float3, int4, etc.)"""
    base_type: str  # float, int, char, etc.
    dimension: int  # 1, 2, 3, 4
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_cuda_vector_type(self)

@dataclass
class CudaBuiltinType(CudaType):
    """CUDA built-in types"""
    type_name: str  # dim3, cudaEvent_t, cudaStream_t, etc.
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_cuda_builtin_type(self)

@dataclass
class DevicePointerType(CudaType):
    """Device pointer type"""
    pointed_type: CudaType
    memory_space: CudaMemorySpace = CudaMemorySpace.GLOBAL
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_device_pointer_type(self)

# CUDA Attributes and Annotations

@dataclass
class CudaAttribute(CudaNode):
    """CUDA attribute or annotation"""
    name: str
    arguments: List[CudaExpression] = field(default_factory=list)
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_cuda_attribute(self)

@dataclass
class LaunchBounds(CudaAttribute):
    """__launch_bounds__ attribute"""
    max_threads_per_block: int
    min_blocks_per_multiprocessor: Optional[int] = None
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_launch_bounds(self)

@dataclass
class DeviceAttribute(CudaAttribute):
    """__device__ attribute"""
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_device_attribute(self)

@dataclass
class HostAttribute(CudaAttribute):
    """__host__ attribute"""
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_host_attribute(self)

@dataclass
class GlobalAttribute(CudaAttribute):
    """__global__ attribute"""
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_global_attribute(self)

# CUDA Directives

@dataclass
class IncludeDirective(CudaNode):
    """Include directive"""
    header_name: str
    is_system: bool = False  # <> vs ""
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_include_directive(self)

@dataclass
class PragmaDirective(CudaNode):
    """Pragma directive"""
    directive: str
    arguments: List[str] = field(default_factory=list)
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_pragma_directive(self)

# Standard C++ Constructs (extended for CUDA)

@dataclass
class ParameterDeclaration(CudaDeclaration):
    """Function parameter declaration"""
    name: str
    type: CudaType
    default_value: Optional[CudaExpression] = None
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_parameter_declaration(self)

@dataclass
class CompoundStatement(CudaStatement):
    """Compound statement { ... }"""
    statements: List[CudaStatement] = field(default_factory=list)
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_compound_statement(self)

@dataclass
class IfStatement(CudaStatement):
    """If statement"""
    condition: CudaExpression
    then_statement: CudaStatement
    else_statement: Optional[CudaStatement] = None
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_if_statement(self)

@dataclass
class ForStatement(CudaStatement):
    """For loop statement"""
    init: Optional[CudaStatement] = None
    condition: Optional[CudaExpression] = None
    increment: Optional[CudaExpression] = None
    body: CudaStatement
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_for_statement(self)

@dataclass
class WhileStatement(CudaStatement):
    """While loop statement"""
    condition: CudaExpression
    body: CudaStatement
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_while_statement(self)

@dataclass
class ReturnStatement(CudaStatement):
    """Return statement"""
    value: Optional[CudaExpression] = None
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_return_statement(self)

@dataclass
class ExpressionStatement(CudaStatement):
    """Expression statement"""
    expression: CudaExpression
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_expression_statement(self)

# Basic Expressions

@dataclass
class Identifier(CudaExpression):
    """Identifier expression"""
    name: str
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_identifier(self)

@dataclass
class IntegerLiteral(CudaExpression):
    """Integer literal"""
    value: int
    suffix: Optional[str] = None  # U, L, UL, etc.
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_integer_literal(self)

@dataclass
class FloatLiteral(CudaExpression):
    """Float literal"""
    value: float
    suffix: Optional[str] = None  # f, F, l, L
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_float_literal(self)

@dataclass
class StringLiteral(CudaExpression):
    """String literal"""
    value: str
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_string_literal(self)

@dataclass
class BinaryOperation(CudaExpression):
    """Binary operation"""
    left: CudaExpression
    operator: str
    right: CudaExpression
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_binary_operation(self)

@dataclass
class UnaryOperation(CudaExpression):
    """Unary operation"""
    operator: str
    operand: CudaExpression
    is_postfix: bool = False
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_unary_operation(self)

@dataclass
class FunctionCall(CudaExpression):
    """Function call expression"""
    function: CudaExpression
    arguments: List[CudaExpression] = field(default_factory=list)
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_function_call(self)

@dataclass
class ArrayAccess(CudaExpression):
    """Array access expression"""
    array: CudaExpression
    index: CudaExpression
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_array_access(self)

@dataclass
class MemberAccess(CudaExpression):
    """Member access expression"""
    object: CudaExpression
    member: str
    is_pointer_access: bool = False  # -> vs .
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_member_access(self)

# Template Support

@dataclass
class TemplateParameter(CudaNode):
    """Template parameter"""
    name: str
    type: Optional[CudaType] = None
    default_value: Optional[CudaExpression] = None
    is_typename: bool = True
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_template_parameter(self)

# Comments

@dataclass
class Comment(CudaNode):
    """Comment in CUDA code"""
    text: str
    is_block: bool = False  # /* */ vs //
    
    def accept(self, visitor: 'CudaVisitor') -> Any:
        return visitor.visit_comment(self)

# Visitor Pattern

class CudaVisitor(ABC):
    """Abstract visitor for CUDA AST traversal"""
    
    @abstractmethod
    def visit_cuda_translation_unit(self, node: CudaTranslationUnit) -> Any:
        pass
    
    @abstractmethod
    def visit_kernel_function(self, node: KernelFunction) -> Any:
        pass
    
    @abstractmethod
    def visit_device_function(self, node: DeviceFunction) -> Any:
        pass
    
    @abstractmethod
    def visit_device_variable(self, node: DeviceVariable) -> Any:
        pass
    
    @abstractmethod
    def visit_shared_memory_declaration(self, node: SharedMemoryDeclaration) -> Any:
        pass
    
    @abstractmethod
    def visit_texture_declaration(self, node: TextureDeclaration) -> Any:
        pass
    
    @abstractmethod
    def visit_kernel_launch(self, node: KernelLaunch) -> Any:
        pass
    
    @abstractmethod
    def visit_execution_configuration(self, node: ExecutionConfiguration) -> Any:
        pass
    
    @abstractmethod
    def visit_thread_index(self, node: ThreadIndex) -> Any:
        pass
    
    @abstractmethod
    def visit_cuda_builtin_call(self, node: CudaBuiltinCall) -> Any:
        pass
    
    @abstractmethod
    def visit_memory_transfer(self, node: MemoryTransfer) -> Any:
        pass
    
    @abstractmethod
    def visit_memory_allocation(self, node: MemoryAllocation) -> Any:
        pass
    
    @abstractmethod
    def visit_synchronization_call(self, node: SynchronizationCall) -> Any:
        pass
    
    @abstractmethod
    def visit_atomic_operation(self, node: AtomicOperation) -> Any:
        pass
    
    @abstractmethod
    def visit_warp_shuffle(self, node: WarpShuffle) -> Any:
        pass
    
    @abstractmethod
    def visit_texture_access(self, node: TextureAccess) -> Any:
        pass
    
    @abstractmethod
    def visit_kernel_launch_statement(self, node: KernelLaunchStatement) -> Any:
        pass
    
    @abstractmethod
    def visit_memory_transfer_statement(self, node: MemoryTransferStatement) -> Any:
        pass
    
    @abstractmethod
    def visit_synchronization_statement(self, node: SynchronizationStatement) -> Any:
        pass
    
    @abstractmethod
    def visit_error_check_statement(self, node: ErrorCheckStatement) -> Any:
        pass
    
    @abstractmethod
    def visit_cuda_vector_type(self, node: CudaVectorType) -> Any:
        pass
    
    @abstractmethod
    def visit_cuda_builtin_type(self, node: CudaBuiltinType) -> Any:
        pass
    
    @abstractmethod
    def visit_device_pointer_type(self, node: DevicePointerType) -> Any:
        pass
    
    @abstractmethod
    def visit_cuda_attribute(self, node: CudaAttribute) -> Any:
        pass
    
    @abstractmethod
    def visit_launch_bounds(self, node: LaunchBounds) -> Any:
        pass
    
    @abstractmethod
    def visit_device_attribute(self, node: DeviceAttribute) -> Any:
        pass
    
    @abstractmethod
    def visit_host_attribute(self, node: HostAttribute) -> Any:
        pass
    
    @abstractmethod
    def visit_global_attribute(self, node: GlobalAttribute) -> Any:
        pass
    
    @abstractmethod
    def visit_include_directive(self, node: IncludeDirective) -> Any:
        pass
    
    @abstractmethod
    def visit_pragma_directive(self, node: PragmaDirective) -> Any:
        pass
    
    @abstractmethod
    def visit_parameter_declaration(self, node: ParameterDeclaration) -> Any:
        pass
    
    @abstractmethod
    def visit_compound_statement(self, node: CompoundStatement) -> Any:
        pass
    
    @abstractmethod
    def visit_if_statement(self, node: IfStatement) -> Any:
        pass
    
    @abstractmethod
    def visit_for_statement(self, node: ForStatement) -> Any:
        pass
    
    @abstractmethod
    def visit_while_statement(self, node: WhileStatement) -> Any:
        pass
    
    @abstractmethod
    def visit_return_statement(self, node: ReturnStatement) -> Any:
        pass
    
    @abstractmethod
    def visit_expression_statement(self, node: ExpressionStatement) -> Any:
        pass
    
    @abstractmethod
    def visit_identifier(self, node: Identifier) -> Any:
        pass
    
    @abstractmethod
    def visit_integer_literal(self, node: IntegerLiteral) -> Any:
        pass
    
    @abstractmethod
    def visit_float_literal(self, node: FloatLiteral) -> Any:
        pass
    
    @abstractmethod
    def visit_string_literal(self, node: StringLiteral) -> Any:
        pass
    
    @abstractmethod
    def visit_binary_operation(self, node: BinaryOperation) -> Any:
        pass
    
    @abstractmethod
    def visit_unary_operation(self, node: UnaryOperation) -> Any:
        pass
    
    @abstractmethod
    def visit_function_call(self, node: FunctionCall) -> Any:
        pass
    
    @abstractmethod
    def visit_array_access(self, node: ArrayAccess) -> Any:
        pass
    
    @abstractmethod
    def visit_member_access(self, node: MemberAccess) -> Any:
        pass
    
    @abstractmethod
    def visit_template_parameter(self, node: TemplateParameter) -> Any:
        pass
    
    @abstractmethod
    def visit_comment(self, node: Comment) -> Any:
        pass

# Utility Functions

def create_kernel_function(name: str, params: List[ParameterDeclaration], body: CompoundStatement) -> KernelFunction:
    """Create kernel function"""
    return KernelFunction(
        name=name,
        parameters=params,
        body=body,
        execution_space=CudaExecutionSpace.GLOBAL
    )

def create_device_function(name: str, params: List[ParameterDeclaration], body: CompoundStatement) -> DeviceFunction:
    """Create device function"""
    return DeviceFunction(
        name=name,
        parameters=params,
        body=body,
        execution_space=CudaExecutionSpace.DEVICE
    )

def create_kernel_launch(kernel: str, grid: CudaExpression, block: CudaExpression, *args) -> KernelLaunch:
    """Create kernel launch"""
    config = ExecutionConfiguration(grid_dim=grid, block_dim=block)
    return KernelLaunch(
        kernel_name=kernel,
        execution_config=config,
        arguments=list(args)
    )

def create_thread_id(dim: str = "x") -> BinaryOperation:
    """Create global thread ID calculation"""
    block_id = ThreadIndex("blockIdx", dim)
    block_dim = ThreadIndex("blockDim", dim)
    thread_id = ThreadIndex("threadIdx", dim)
    
    return BinaryOperation(
        left=BinaryOperation(left=block_id, operator="*", right=block_dim),
        operator="+",
        right=thread_id
    )

def create_memory_copy(dst: CudaExpression, src: CudaExpression, size: CudaExpression, kind: str) -> MemoryTransfer:
    """Create memory copy operation"""
    return MemoryTransfer(
        destination=dst,
        source=src,
        size=size,
        direction=kind
    )

# CUDA Built-in Functions Reference
CUDA_BUILTIN_FUNCTIONS = {
    # Thread and block functions
    '__syncthreads', '__syncwarp', '__threadfence', '__threadfence_block', '__threadfence_system',
    
    # Math functions
    '__float2int_rn', '__int2float_rn', '__float2half_rn', '__half2float',
    '__powf', '__expf', '__logf', '__sinf', '__cosf', '__tanf',
    '__rsqrtf', '__sqrtf', '__fabsf', '__fmaxf', '__fminf',
    
    # Atomic functions
    'atomicAdd', 'atomicSub', 'atomicMin', 'atomicMax', 'atomicAnd', 'atomicOr', 'atomicXor',
    'atomicCAS', 'atomicExch', 'atomicInc', 'atomicDec',
    
    # Warp functions
    '__shfl', '__shfl_up', '__shfl_down', '__shfl_xor',
    '__ballot', '__any', '__all', '__popc', '__clz',
    
    # Texture functions
    'tex1D', 'tex2D', 'tex3D', 'tex1Dfetch', 'tex2Dgather',
    
    # Surface functions
    'surf1Dread', 'surf2Dread', 'surf3Dread', 'surf1Dwrite', 'surf2Dwrite', 'surf3Dwrite'
}

# Export main classes
__all__ = [
    # Enums
    'CudaMemorySpace', 'CudaExecutionSpace', 'CudaArchitecture',
    
    # Base classes
    'CudaNode', 'CudaExpression', 'CudaStatement', 'CudaDeclaration', 'CudaType', 'CudaVisitor',
    
    # Core nodes
    'CudaTranslationUnit',
    
    # Declarations
    'KernelFunction', 'DeviceFunction', 'DeviceVariable', 'SharedMemoryDeclaration', 
    'TextureDeclaration', 'ParameterDeclaration',
    
    # Expressions
    'KernelLaunch', 'ExecutionConfiguration', 'ThreadIndex', 'CudaBuiltinCall',
    'MemoryTransfer', 'MemoryAllocation', 'SynchronizationCall', 'AtomicOperation',
    'WarpShuffle', 'TextureAccess',
    
    # Statements
    'KernelLaunchStatement', 'MemoryTransferStatement', 'SynchronizationStatement',
    'ErrorCheckStatement', 'CompoundStatement', 'IfStatement', 'ForStatement',
    'WhileStatement', 'ReturnStatement', 'ExpressionStatement',
    
    # Types
    'CudaVectorType', 'CudaBuiltinType', 'DevicePointerType',
    
    # Attributes
    'CudaAttribute', 'LaunchBounds', 'DeviceAttribute', 'HostAttribute', 'GlobalAttribute',
    
    # Directives
    'IncludeDirective', 'PragmaDirective',
    
    # Basic expressions
    'Identifier', 'IntegerLiteral', 'FloatLiteral', 'StringLiteral',
    'BinaryOperation', 'UnaryOperation', 'FunctionCall', 'ArrayAccess', 'MemberAccess',
    
    # Template
    'TemplateParameter',
    
    # Comments
    'Comment',
    
    # Utilities
    'create_kernel_function', 'create_device_function', 'create_kernel_launch',
    'create_thread_id', 'create_memory_copy',
    'CUDA_BUILTIN_FUNCTIONS'
] 