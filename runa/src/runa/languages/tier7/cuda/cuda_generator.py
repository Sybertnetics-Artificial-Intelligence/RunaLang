#!/usr/bin/env python3
"""
CUDA Generator - Clean code generation for CUDA C++

Features:
- Clean CUDA C++ code generation with proper formatting
- Kernel launch syntax and execution configuration
- GPU memory management and thread indexing
- NVCC-compatible output with optimization hints
"""

from typing import List, Dict, Any, Optional, TextIO
from dataclasses import dataclass
from io import StringIO
from .cuda_ast import *

@dataclass
class CudaCodeStyle:
    """CUDA code style configuration"""
    indent_size: int = 4
    use_spaces: bool = True
    max_line_length: int = 100
    space_around_operators: bool = True
    kernel_launch_newline: bool = True
    include_optimization_hints: bool = True

class CudaFormatter:
    """Formatter for CUDA code"""
    
    def __init__(self, style: CudaCodeStyle = None):
        self.style = style or CudaCodeStyle()
        self.current_indent = 0
        
    def indent(self) -> str:
        if self.style.use_spaces:
            return " " * (self.current_indent * self.style.indent_size)
        return "\t" * self.current_indent
        
    def increase_indent(self):
        self.current_indent += 1
        
    def decrease_indent(self):
        self.current_indent = max(0, self.current_indent - 1)
        
    def format_translation_unit(self, unit: CudaTranslationUnit) -> str:
        result = ""
        
        # Format includes
        for include in unit.includes:
            result += self.format_include(include) + "\n"
        if unit.includes:
            result += "\n"
            
        # Format declarations
        for i, decl in enumerate(unit.declarations):
            if i > 0:
                result += "\n"
            result += self.format_declaration(decl) + "\n"
            
        return result
        
    def format_include(self, include: IncludeDirective) -> str:
        if include.is_system:
            return f"#include <{include.header_name}>"
        return f'#include "{include.header_name}"'
        
    def format_declaration(self, decl: CudaDeclaration) -> str:
        if isinstance(decl, KernelFunction):
            return self.format_kernel_function(decl)
        elif isinstance(decl, DeviceFunction):
            return self.format_device_function(decl)
        elif isinstance(decl, DeviceVariable):
            return self.format_device_variable(decl)
        elif isinstance(decl, SharedMemoryDeclaration):
            return self.format_shared_memory(decl)
        return ""
        
    def format_kernel_function(self, kernel: KernelFunction) -> str:
        result = "__global__ "
        result += self.format_function_signature(kernel.name, kernel.parameters, kernel.return_type)
        result += " " + self.format_compound_statement(kernel.body)
        return result
        
    def format_device_function(self, func: DeviceFunction) -> str:
        result = f"__{func.execution_space.value.split('__')[1]}__ "
        result += self.format_function_signature(func.name, func.parameters, func.return_type)
        result += " " + self.format_compound_statement(func.body)
        return result
        
    def format_device_variable(self, var: DeviceVariable) -> str:
        result = f"__{var.memory_space.value.split('__')[1]}__ "
        result += self.format_type(var.type) + " " + var.name
        if var.initial_value:
            result += " = " + self.format_expression(var.initial_value)
        return result + ";"
        
    def format_shared_memory(self, shared: SharedMemoryDeclaration) -> str:
        result = "__shared__ " + self.format_type(shared.type) + " " + shared.name
        if shared.size:
            result += "[" + self.format_expression(shared.size) + "]"
        return result + ";"
        
    def format_function_signature(self, name: str, params: List[ParameterDeclaration], return_type: CudaType) -> str:
        result = ""
        if return_type:
            result += self.format_type(return_type) + " "
        result += name + "("
        
        param_strs = []
        for param in params:
            param_str = self.format_type(param.type) + " " + param.name
            param_strs.append(param_str)
            
        result += ", ".join(param_strs) + ")"
        return result
        
    def format_type(self, cuda_type: CudaType) -> str:
        if isinstance(cuda_type, CudaBuiltinType):
            return cuda_type.type_name
        elif isinstance(cuda_type, CudaVectorType):
            return f"{cuda_type.base_type}{cuda_type.dimension}"
        elif isinstance(cuda_type, DevicePointerType):
            return self.format_type(cuda_type.pointed_type) + "*"
        return "void"
        
    def format_compound_statement(self, stmt: CompoundStatement) -> str:
        result = "{\n"
        self.increase_indent()
        
        for s in stmt.statements:
            formatted = self.format_statement(s)
            if formatted:
                result += self.indent() + formatted + "\n"
                
        self.decrease_indent()
        result += self.indent() + "}"
        return result
        
    def format_statement(self, stmt: CudaStatement) -> str:
        if isinstance(stmt, ExpressionStatement):
            return self.format_expression(stmt.expression) + ";"
        elif isinstance(stmt, ReturnStatement):
            if stmt.value:
                return "return " + self.format_expression(stmt.value) + ";"
            return "return;"
        elif isinstance(stmt, IfStatement):
            return self.format_if_statement(stmt)
        elif isinstance(stmt, ForStatement):
            return self.format_for_statement(stmt)
        elif isinstance(stmt, KernelLaunchStatement):
            return self.format_kernel_launch_statement(stmt)
        elif isinstance(stmt, CompoundStatement):
            return self.format_compound_statement(stmt)
        return ""
        
    def format_if_statement(self, if_stmt: IfStatement) -> str:
        result = "if (" + self.format_expression(if_stmt.condition) + ") "
        result += self.format_statement(if_stmt.then_statement)
        if if_stmt.else_statement:
            result += " else " + self.format_statement(if_stmt.else_statement)
        return result
        
    def format_for_statement(self, for_stmt: ForStatement) -> str:
        result = "for ("
        if for_stmt.init:
            result += self.format_statement(for_stmt.init).rstrip(';')
        result += "; "
        if for_stmt.condition:
            result += self.format_expression(for_stmt.condition)
        result += "; "
        if for_stmt.increment:
            result += self.format_expression(for_stmt.increment)
        result += ") " + self.format_statement(for_stmt.body)
        return result
        
    def format_kernel_launch_statement(self, stmt: KernelLaunchStatement) -> str:
        launch = stmt.kernel_launch
        result = launch.kernel_name
        result += self.format_execution_configuration(launch.execution_config)
        result += "("
        args = [self.format_expression(arg) for arg in launch.arguments]
        result += ", ".join(args) + ");"
        return result
        
    def format_execution_configuration(self, config: ExecutionConfiguration) -> str:
        result = "<<<"
        result += self.format_expression(config.grid_dim)
        result += ", " + self.format_expression(config.block_dim)
        if config.shared_mem_size:
            result += ", " + self.format_expression(config.shared_mem_size)
        if config.stream:
            result += ", " + self.format_expression(config.stream)
        result += ">>>"
        return result
        
    def format_expression(self, expr: CudaExpression) -> str:
        if isinstance(expr, Identifier):
            return expr.name
        elif isinstance(expr, IntegerLiteral):
            return str(expr.value)
        elif isinstance(expr, FloatLiteral):
            return str(expr.value) + "f"
        elif isinstance(expr, StringLiteral):
            return f'"{expr.value}"'
        elif isinstance(expr, ThreadIndex):
            return f"{expr.index_type}.{expr.dimension}"
        elif isinstance(expr, BinaryOperation):
            left = self.format_expression(expr.left)
            right = self.format_expression(expr.right)
            op = f" {expr.operator} " if self.style.space_around_operators else expr.operator
            return f"{left}{op}{right}"
        elif isinstance(expr, FunctionCall):
            func = self.format_expression(expr.function)
            args = [self.format_expression(arg) for arg in expr.arguments]
            return f"{func}({', '.join(args)})"
        elif isinstance(expr, ArrayAccess):
            array = self.format_expression(expr.array)
            index = self.format_expression(expr.index)
            return f"{array}[{index}]"
        elif isinstance(expr, MemberAccess):
            obj = self.format_expression(expr.object)
            op = "->" if expr.is_pointer_access else "."
            return f"{obj}{op}{expr.member}"
        return ""

class CudaCodeGenerator:
    """Main code generator for CUDA"""
    
    def __init__(self, style: CudaCodeStyle = None):
        self.style = style or CudaCodeStyle()
        self.formatter = CudaFormatter(self.style)
        
    def generate(self, ast: CudaTranslationUnit) -> str:
        """Generate CUDA code from AST"""
        return self.formatter.format_translation_unit(ast)
        
    def generate_to_file(self, ast: CudaTranslationUnit, filename: str) -> None:
        """Generate CUDA code to file"""
        code = self.generate(ast)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(code)

def generate_cuda(ast: CudaTranslationUnit, style: CudaCodeStyle = None) -> str:
    """Generate CUDA code from AST"""
    generator = CudaCodeGenerator(style)
    return generator.generate(ast)

__all__ = ['CudaCodeStyle', 'CudaFormatter', 'CudaCodeGenerator', 'generate_cuda'] 