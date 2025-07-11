#!/usr/bin/env python3
"""
CUDA Converter - Bidirectional conversion between CUDA and Runa AST

Features:
- Complete CUDA → Runa AST conversion
- Full Runa AST → CUDA conversion  
- GPU kernel and device function mapping
- Memory management translation
- Thread indexing and execution model
- Parallel programming constructs
"""

from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass

# Import Runa core components
from runa.core.ast_nodes import *
from runa.core.semantic_analyzer import SemanticAnalyzer
from runa.core.types import *

# Import CUDA AST
from .cuda_ast import *

class CudaToRunaConverter:
    """Converts CUDA AST to Runa AST"""
    
    def __init__(self):
        self.semantic_analyzer = SemanticAnalyzer()
        self.variable_mappings: Dict[str, str] = {}
        self.function_mappings: Dict[str, str] = {}
        
    def convert(self, cuda_ast: CudaTranslationUnit) -> ModuleNode:
        """Convert CUDA AST to Runa AST"""
        module = ModuleNode(
            name="cuda_module",
            statements=[],
            imports=[],
            metadata={"original_language": "cuda", "parallel_computing": "gpu"}
        )
        
        # Convert includes to imports
        for include in cuda_ast.includes:
            import_stmt = self.convert_include_to_import(include)
            module.imports.append(import_stmt)
            
        # Convert declarations
        for decl in cuda_ast.declarations:
            runa_decl = self.convert_declaration(decl)
            if runa_decl:
                module.statements.append(runa_decl)
                
        return module
        
    def convert_declaration(self, decl: CudaDeclaration) -> Optional[DeclarationNode]:
        """Convert CUDA declaration to Runa declaration"""
        if isinstance(decl, KernelFunction):
            return self.convert_kernel_function(decl)
        elif isinstance(decl, DeviceFunction):
            return self.convert_device_function(decl)
        elif isinstance(decl, DeviceVariable):
            return self.convert_device_variable(decl)
        elif isinstance(decl, SharedMemoryDeclaration):
            return self.convert_shared_memory(decl)
        else:
            return None
            
    def convert_kernel_function(self, kernel: KernelFunction) -> FunctionDeclarationNode:
        """Convert CUDA kernel to Runa parallel function"""
        # Convert parameters
        params = [self.convert_parameter(p) for p in kernel.parameters]
        
        # Add GPU execution context parameter
        gpu_context = ParameterNode(
            name="gpu_context",
            type_annotation=self.create_gpu_context_type(),
            default_value=None
        )
        params.insert(0, gpu_context)
        
        # Convert body with GPU threading model
        body = self.convert_compound_statement(kernel.body)
        
        # Add GPU metadata
        func_decl = FunctionDeclarationNode(
            name=kernel.name,
            parameters=params,
            return_type=self.convert_cuda_type(kernel.return_type) if kernel.return_type else VoidTypeNode(),
            body=body,
            metadata={
                "cuda_kernel": True,
                "execution_space": "device",
                "parallel_execution": True
            }
        )
        
        return func_decl
        
    def convert_device_function(self, func: DeviceFunction) -> FunctionDeclarationNode:
        """Convert CUDA device function to Runa function"""
        params = [self.convert_parameter(p) for p in func.parameters]
        body = self.convert_compound_statement(func.body)
        
        return FunctionDeclarationNode(
            name=func.name,
            parameters=params,
            return_type=self.convert_cuda_type(func.return_type) if func.return_type else VoidTypeNode(),
            body=body,
            metadata={
                "cuda_device_function": True,
                "execution_space": "device"
            }
        )
        
    def convert_device_variable(self, var: DeviceVariable) -> VariableDeclarationNode:
        """Convert CUDA device variable to Runa variable"""
        initial_value = None
        if var.initial_value:
            initial_value = self.convert_expression(var.initial_value)
            
        return VariableDeclarationNode(
            name=var.name,
            type_annotation=self.convert_cuda_type(var.type),
            initial_value=initial_value,
            is_mutable=not var.is_constant,
            metadata={
                "cuda_memory_space": var.memory_space.value,
                "device_variable": True
            }
        )
        
    def convert_shared_memory(self, shared: SharedMemoryDeclaration) -> VariableDeclarationNode:
        """Convert shared memory to Runa shared variable"""
        return VariableDeclarationNode(
            name=shared.name,
            type_annotation=self.convert_cuda_type(shared.type),
            initial_value=None,
            is_mutable=True,
            metadata={
                "cuda_shared_memory": True,
                "memory_scope": "block"
            }
        )
        
    def convert_parameter(self, param: ParameterDeclaration) -> ParameterNode:
        """Convert CUDA parameter to Runa parameter"""
        return ParameterNode(
            name=param.name,
            type_annotation=self.convert_cuda_type(param.type),
            default_value=self.convert_expression(param.default_value) if param.default_value else None
        )
        
    def convert_cuda_type(self, cuda_type: CudaType) -> TypeNode:
        """Convert CUDA type to Runa type"""
        if isinstance(cuda_type, CudaBuiltinType):
            type_mapping = {
                'int': IntegerTypeNode(),
                'float': FloatTypeNode(),
                'double': FloatTypeNode(),
                'char': IntegerTypeNode(),
                'void': VoidTypeNode()
            }
            return type_mapping.get(cuda_type.type_name, AnyTypeNode())
        elif isinstance(cuda_type, CudaVectorType):
            # Convert vector types to arrays
            base_type = self.convert_cuda_type(CudaBuiltinType(cuda_type.base_type))
            return ArrayTypeNode(base_type, IntegerLiteralNode(cuda_type.dimension))
        elif isinstance(cuda_type, DevicePointerType):
            pointed_type = self.convert_cuda_type(cuda_type.pointed_type)
            return PointerTypeNode(pointed_type)
        else:
            return AnyTypeNode()
            
    def convert_compound_statement(self, stmt: CompoundStatement) -> BlockNode:
        """Convert compound statement to Runa block"""
        statements = []
        for cuda_stmt in stmt.statements:
            runa_stmt = self.convert_statement(cuda_stmt)
            if runa_stmt:
                statements.append(runa_stmt)
        return BlockNode(statements)
        
    def convert_statement(self, stmt: CudaStatement) -> Optional[StatementNode]:
        """Convert CUDA statement to Runa statement"""
        if isinstance(stmt, KernelLaunchStatement):
            return self.convert_kernel_launch_statement(stmt)
        elif isinstance(stmt, ExpressionStatement):
            expr = self.convert_expression(stmt.expression)
            return ExpressionStatementNode(expr)
        elif isinstance(stmt, IfStatement):
            return self.convert_if_statement(stmt)
        elif isinstance(stmt, ForStatement):
            return self.convert_for_statement(stmt)
        elif isinstance(stmt, ReturnStatement):
            value = self.convert_expression(stmt.value) if stmt.value else None
            return ReturnStatementNode(value)
        elif isinstance(stmt, CompoundStatement):
            return self.convert_compound_statement(stmt)
        else:
            return None
            
    def convert_kernel_launch_statement(self, stmt: KernelLaunchStatement) -> ExpressionStatementNode:
        """Convert kernel launch to Runa parallel execution"""
        launch = stmt.kernel_launch
        
        # Create parallel execution call
        kernel_ref = IdentifierNode(launch.kernel_name)
        config = self.convert_execution_config(launch.execution_config)
        args = [self.convert_expression(arg) for arg in launch.arguments]
        
        # Create GPU execution call
        gpu_call = FunctionCallNode(
            function=IdentifierNode("execute_on_gpu"),
            arguments=[kernel_ref, config] + args,
            metadata={"cuda_kernel_launch": True}
        )
        
        return ExpressionStatementNode(gpu_call)
        
    def convert_execution_config(self, config: ExecutionConfiguration) -> DictionaryLiteralNode:
        """Convert execution configuration to Runa dictionary"""
        fields = [
            DictionaryFieldNode(
                key=StringLiteralNode("grid_dim"),
                value=self.convert_expression(config.grid_dim)
            ),
            DictionaryFieldNode(
                key=StringLiteralNode("block_dim"),
                value=self.convert_expression(config.block_dim)
            )
        ]
        
        if config.shared_mem_size:
            fields.append(DictionaryFieldNode(
                key=StringLiteralNode("shared_memory"),
                value=self.convert_expression(config.shared_mem_size)
            ))
            
        return DictionaryLiteralNode(fields)
        
    def convert_expression(self, expr: CudaExpression) -> ExpressionNode:
        """Convert CUDA expression to Runa expression"""
        if isinstance(expr, ThreadIndex):
            return self.convert_thread_index(expr)
        elif isinstance(expr, Identifier):
            return IdentifierNode(expr.name)
        elif isinstance(expr, IntegerLiteral):
            return IntegerLiteralNode(expr.value)
        elif isinstance(expr, FloatLiteral):
            return FloatLiteralNode(expr.value)
        elif isinstance(expr, StringLiteral):
            return StringLiteralNode(expr.value)
        elif isinstance(expr, BinaryOperation):
            left = self.convert_expression(expr.left)
            right = self.convert_expression(expr.right)
            return BinaryOperationNode(left, expr.operator, right)
        elif isinstance(expr, FunctionCall):
            return self.convert_function_call(expr)
        elif isinstance(expr, ArrayAccess):
            array = self.convert_expression(expr.array)
            index = self.convert_expression(expr.index)
            return IndexAccessNode(array, index)
        else:
            return IdentifierNode("unknown")
            
    def convert_thread_index(self, thread_idx: ThreadIndex) -> FunctionCallNode:
        """Convert CUDA thread index to Runa GPU context call"""
        return FunctionCallNode(
            function=IdentifierNode("get_thread_index"),
            arguments=[
                StringLiteralNode(thread_idx.index_type),
                StringLiteralNode(thread_idx.dimension)
            ],
            metadata={"cuda_thread_index": True}
        )
        
    def convert_function_call(self, call: FunctionCall) -> FunctionCallNode:
        """Convert CUDA function call to Runa function call"""
        func = self.convert_expression(call.function)
        args = [self.convert_expression(arg) for arg in call.arguments]
        return FunctionCallNode(function=func, arguments=args)
        
    def convert_if_statement(self, if_stmt: IfStatement) -> IfStatementNode:
        """Convert CUDA if statement to Runa if statement"""
        condition = self.convert_expression(if_stmt.condition)
        then_stmt = self.convert_statement(if_stmt.then_statement)
        else_stmt = self.convert_statement(if_stmt.else_statement) if if_stmt.else_statement else None
        
        return IfStatementNode(condition, then_stmt, else_stmt)
        
    def convert_for_statement(self, for_stmt: ForStatement) -> ForStatementNode:
        """Convert CUDA for statement to Runa for statement"""
        init = self.convert_statement(for_stmt.init) if for_stmt.init else None
        condition = self.convert_expression(for_stmt.condition) if for_stmt.condition else None
        increment = self.convert_expression(for_stmt.increment) if for_stmt.increment else None
        body = self.convert_statement(for_stmt.body)
        
        return ForStatementNode(init, condition, increment, body)
        
    def convert_include_to_import(self, include: IncludeDirective) -> ImportStatementNode:
        """Convert CUDA include to Runa import"""
        module_name = include.header_name.replace('.h', '').replace('.cuh', '').replace('/', '.')
        return ImportStatementNode(module_name)
        
    def create_gpu_context_type(self) -> TypeNode:
        """Create GPU context type"""
        return CustomTypeNode("GPUContext")

class RunaToCudaConverter:
    """Converts Runa AST to CUDA AST"""
    
    def __init__(self):
        self.variable_mappings: Dict[str, str] = {}
        
    def convert(self, runa_ast: ModuleNode) -> CudaTranslationUnit:
        """Convert Runa AST to CUDA AST"""
        declarations = []
        includes = []
        
        # Add standard CUDA includes
        includes.append(IncludeDirective("cuda_runtime.h", True))
        includes.append(IncludeDirective("device_launch_parameters.h", True))
        
        # Convert statements to declarations
        for stmt in runa_ast.statements:
            cuda_decl = self.convert_statement_to_declaration(stmt)
            if cuda_decl:
                declarations.append(cuda_decl)
                
        return CudaTranslationUnit(declarations=declarations, includes=includes)
        
    def convert_statement_to_declaration(self, stmt: StatementNode) -> Optional[CudaDeclaration]:
        """Convert Runa statement to CUDA declaration"""
        if isinstance(stmt, FunctionDeclarationNode):
            return self.convert_function_declaration(stmt)
        elif isinstance(stmt, VariableDeclarationNode):
            return self.convert_variable_declaration(stmt)
        else:
            return None
            
    def convert_function_declaration(self, func: FunctionDeclarationNode) -> CudaDeclaration:
        """Convert Runa function to CUDA function"""
        metadata = func.metadata or {}
        
        if metadata.get("cuda_kernel", False):
            return self.convert_to_kernel_function(func)
        else:
            return self.convert_to_device_function(func)
            
    def convert_to_kernel_function(self, func: FunctionDeclarationNode) -> KernelFunction:
        """Convert to CUDA kernel function"""
        # Remove GPU context parameter
        params = []
        for param in func.parameters:
            if param.name != "gpu_context":
                cuda_param = ParameterDeclaration(
                    name=param.name,
                    type=self.convert_runa_type(param.type_annotation)
                )
                params.append(cuda_param)
                
        body = self.convert_block_to_compound(func.body)
        
        return KernelFunction(
            name=func.name,
            parameters=params,
            body=body,
            return_type=self.convert_runa_type(func.return_type)
        )
        
    def convert_to_device_function(self, func: FunctionDeclarationNode) -> DeviceFunction:
        """Convert to CUDA device function"""
        params = []
        for param in func.parameters:
            cuda_param = ParameterDeclaration(
                name=param.name,
                type=self.convert_runa_type(param.type_annotation)
            )
            params.append(cuda_param)
            
        body = self.convert_block_to_compound(func.body)
        
        return DeviceFunction(
            name=func.name,
            parameters=params,
            body=body,
            return_type=self.convert_runa_type(func.return_type)
        )
        
    def convert_variable_declaration(self, var: VariableDeclarationNode) -> DeviceVariable:
        """Convert Runa variable to CUDA device variable"""
        metadata = var.metadata or {}
        
        memory_space = CudaMemorySpace.GLOBAL
        if metadata.get("cuda_shared_memory", False):
            memory_space = CudaMemorySpace.SHARED
        elif "cuda_memory_space" in metadata:
            memory_space = CudaMemorySpace(metadata["cuda_memory_space"])
            
        initial_value = None
        if var.initial_value:
            initial_value = self.convert_expression(var.initial_value)
            
        return DeviceVariable(
            name=var.name,
            type=self.convert_runa_type(var.type_annotation),
            memory_space=memory_space,
            initial_value=initial_value,
            is_constant=not var.is_mutable
        )
        
    def convert_runa_type(self, runa_type: TypeNode) -> CudaType:
        """Convert Runa type to CUDA type"""
        if isinstance(runa_type, IntegerTypeNode):
            return CudaBuiltinType("int")
        elif isinstance(runa_type, FloatTypeNode):
            return CudaBuiltinType("float")
        elif isinstance(runa_type, VoidTypeNode):
            return CudaBuiltinType("void")
        elif isinstance(runa_type, ArrayTypeNode):
            # Convert to CUDA vector type if small array
            if isinstance(runa_type.size, IntegerLiteralNode) and runa_type.size.value <= 4:
                base_type = self.convert_runa_type(runa_type.element_type)
                if isinstance(base_type, CudaBuiltinType):
                    return CudaVectorType(base_type.type_name, runa_type.size.value)
            return DevicePointerType(self.convert_runa_type(runa_type.element_type))
        else:
            return CudaBuiltinType("int")  # Default
            
    def convert_block_to_compound(self, block: BlockNode) -> CompoundStatement:
        """Convert Runa block to CUDA compound statement"""
        statements = []
        for stmt in block.statements:
            cuda_stmt = self.convert_statement(stmt)
            if cuda_stmt:
                statements.append(cuda_stmt)
        return CompoundStatement(statements)
        
    def convert_statement(self, stmt: StatementNode) -> Optional[CudaStatement]:
        """Convert Runa statement to CUDA statement"""
        if isinstance(stmt, ExpressionStatementNode):
            expr = self.convert_expression(stmt.expression)
            return ExpressionStatement(expr)
        elif isinstance(stmt, ReturnStatementNode):
            value = self.convert_expression(stmt.value) if stmt.value else None
            return ReturnStatement(value)
        elif isinstance(stmt, IfStatementNode):
            condition = self.convert_expression(stmt.condition)
            then_stmt = self.convert_statement(stmt.then_statement)
            else_stmt = self.convert_statement(stmt.else_statement) if stmt.else_statement else None
            return IfStatement(condition, then_stmt, else_stmt)
        else:
            return None
            
    def convert_expression(self, expr: ExpressionNode) -> CudaExpression:
        """Convert Runa expression to CUDA expression"""
        if isinstance(expr, IdentifierNode):
            return Identifier(expr.name)
        elif isinstance(expr, IntegerLiteralNode):
            return IntegerLiteral(expr.value)
        elif isinstance(expr, FloatLiteralNode):
            return FloatLiteral(expr.value)
        elif isinstance(expr, StringLiteralNode):
            return StringLiteral(expr.value)
        elif isinstance(expr, BinaryOperationNode):
            left = self.convert_expression(expr.left)
            right = self.convert_expression(expr.right)
            return BinaryOperation(left, expr.operator, right)
        elif isinstance(expr, FunctionCallNode):
            return self.convert_function_call(expr)
        else:
            return Identifier("unknown")
            
    def convert_function_call(self, call: FunctionCallNode) -> CudaExpression:
        """Convert Runa function call to CUDA expression"""
        if isinstance(call.function, IdentifierNode):
            func_name = call.function.name
            
            # Handle special GPU functions
            if func_name == "get_thread_index":
                if len(call.arguments) >= 2:
                    index_type = call.arguments[0].value if isinstance(call.arguments[0], StringLiteralNode) else "threadIdx"
                    dimension = call.arguments[1].value if isinstance(call.arguments[1], StringLiteralNode) else "x"
                    return ThreadIndex(index_type, dimension)
                    
        func = self.convert_expression(call.function)
        args = [self.convert_expression(arg) for arg in call.arguments]
        return FunctionCall(func, args)

# Main conversion functions

def cuda_to_runa(cuda_ast: CudaTranslationUnit) -> ModuleNode:
    """Convert CUDA AST to Runa AST"""
    converter = CudaToRunaConverter()
    return converter.convert(cuda_ast)

def runa_to_cuda(runa_ast: ModuleNode) -> CudaTranslationUnit:
    """Convert Runa AST to CUDA AST"""
    converter = RunaToCudaConverter()
    return converter.convert(runa_ast)

# Export main components
__all__ = [
    'CudaToRunaConverter', 'RunaToCudaConverter',
    'cuda_to_runa', 'runa_to_cuda'
] 