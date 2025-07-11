#!/usr/bin/env python3
"""
OpenCL Code Generator - Clean OpenCL C Code Generation

Provides comprehensive code generation for OpenCL C including:
- Clean, readable code formatting
- Multiple style presets (standard, compact, kernel-focused, performance)
- Proper indentation and spacing
- Comment preservation and generation
- Kernel-specific formatting
- Memory qualifier formatting
- Vector operation formatting
- Built-in function formatting

Generates production-ready OpenCL C code with proper syntax and style.
"""

from typing import List, Dict, Optional, Any, TextIO
from dataclasses import dataclass
from enum import Enum
import io

from .opencl_ast import *


class OpenCLCodeStyle(Enum):
    """OpenCL code style presets"""
    STANDARD = "standard"        # Standard OpenCL C style
    COMPACT = "compact"          # Compact style for space efficiency
    KERNEL_FOCUSED = "kernel"    # Emphasizes kernel structure
    PERFORMANCE = "performance"  # Optimized for readability of performance code
    NVIDIA = "nvidia"           # NVIDIA CUDA-like style
    KHRONOS = "khronos"         # Khronos Group style guide


@dataclass
class OpenCLFormatConfig:
    """Configuration for OpenCL code formatting"""
    indent_size: int = 4
    use_tabs: bool = False
    max_line_length: int = 80
    brace_style: str = "k&r"  # "k&r", "allman", "gnu", "horstmann"
    space_after_keywords: bool = True
    space_around_operators: bool = True
    align_parameters: bool = False
    align_assignments: bool = False
    blank_lines_after_declarations: int = 1
    blank_lines_after_functions: int = 2
    comment_style: str = "line"  # "line", "block", "doxygen"
    kernel_annotation_style: str = "newline"  # "newline", "inline"
    vector_literal_multiline: bool = False
    memory_qualifier_spacing: bool = True
    
    @classmethod
    def from_style(cls, style: OpenCLCodeStyle) -> 'OpenCLFormatConfig':
        """Create configuration from style preset"""
        if style == OpenCLCodeStyle.STANDARD:
            return cls()
        elif style == OpenCLCodeStyle.COMPACT:
            return cls(
                indent_size=2,
                max_line_length=120,
                brace_style="k&r",
                blank_lines_after_declarations=0,
                blank_lines_after_functions=1,
                space_around_operators=False
            )
        elif style == OpenCLCodeStyle.KERNEL_FOCUSED:
            return cls(
                indent_size=4,
                max_line_length=100,
                brace_style="allman",
                align_parameters=True,
                blank_lines_after_functions=3,
                kernel_annotation_style="newline",
                comment_style="doxygen"
            )
        elif style == OpenCLCodeStyle.PERFORMANCE:
            return cls(
                indent_size=2,
                max_line_length=120,
                brace_style="k&r",
                align_assignments=True,
                vector_literal_multiline=True,
                memory_qualifier_spacing=True
            )
        elif style == OpenCLCodeStyle.NVIDIA:
            return cls(
                indent_size=4,
                max_line_length=100,
                brace_style="k&r",
                space_around_operators=True,
                kernel_annotation_style="inline"
            )
        elif style == OpenCLCodeStyle.KHRONOS:
            return cls(
                indent_size=4,
                max_line_length=80,
                brace_style="k&r",
                comment_style="doxygen",
                align_parameters=True
            )
        else:
            return cls()


class OpenCLCodeGenerator:
    """Generates clean OpenCL C code from AST"""
    
    def __init__(self, config: Optional[OpenCLFormatConfig] = None):
        self.config = config or OpenCLFormatConfig()
        self.output = io.StringIO()
        self.indent_level = 0
        self.at_line_start = True
        self.suppress_newlines = False
        
        # Track state for formatting decisions
        self.in_kernel = False
        self.in_function_params = False
        self.last_was_declaration = False
    
    def generate(self, program: OpenCLProgram) -> str:
        """Generate OpenCL code from program AST"""
        self.output = io.StringIO()
        self.indent_level = 0
        self.at_line_start = True
        
        # Generate preprocessor directives first
        for directive in program.preprocessor_directives:
            self._generate_preprocessor_directive(directive)
            self._newline()
        
        if program.preprocessor_directives:
            self._newline()
        
        # Generate declarations
        for i, decl in enumerate(program.declarations):
            if i > 0:
                self._blank_lines(self.config.blank_lines_after_declarations)
            
            self._generate_declaration(decl)
            
            # Add extra spacing after functions
            if isinstance(decl, (OpenCLFunctionDeclaration, OpenCLKernelDeclaration)):
                self._blank_lines(self.config.blank_lines_after_functions)
        
        return self.output.getvalue()
    
    def _generate_preprocessor_directive(self, directive: OpenCLPreprocessorDirective) -> None:
        """Generate preprocessor directive"""
        self._write(directive.content)
    
    def _generate_declaration(self, decl: OpenCLDeclaration) -> None:
        """Generate declaration"""
        if isinstance(decl, OpenCLKernelDeclaration):
            self._generate_kernel_declaration(decl)
        elif isinstance(decl, OpenCLFunctionDeclaration):
            self._generate_function_declaration(decl)
        elif isinstance(decl, OpenCLVariableDeclaration):
            self._generate_variable_declaration(decl)
            self._write(";")
        elif isinstance(decl, OpenCLStructDeclaration):
            self._generate_struct_declaration(decl)
        elif isinstance(decl, OpenCLTypedefDeclaration):
            self._generate_typedef_declaration(decl)
        elif isinstance(decl, OpenCLEnumDeclaration):
            self._generate_enum_declaration(decl)
    
    def _generate_kernel_declaration(self, kernel: OpenCLKernelDeclaration) -> None:
        """Generate kernel declaration"""
        self.in_kernel = True
        
        # Add kernel documentation comment if available
        if self.config.comment_style == "doxygen":
            self._write("/**")
            self._newline()
            self._write(f" * @brief OpenCL kernel: {kernel.name}")
            self._newline()
            for i, param in enumerate(kernel.parameters):
                self._write(f" * @param {param.name} {self._get_param_description(param)}")
                self._newline()
            self._write(" */")
            self._newline()
        
        # Kernel qualifier
        if self.config.kernel_annotation_style == "newline":
            self._write("__kernel")
            self._newline()
        else:
            self._write("__kernel ")
        
        # Return type
        self._generate_type(kernel.return_type)
        if self.config.kernel_annotation_style == "newline":
            pass  # No space needed
        else:
            self._write(" ")
        
        # Function name
        self._write(kernel.name)
        
        # Parameters
        self._write("(")
        self._generate_parameter_list(kernel.parameters)
        self._write(")")
        
        # Body
        if kernel.body:
            if self.config.brace_style == "allman":
                self._newline()
                self._write("{")
            else:
                if self.config.space_after_keywords:
                    self._write(" {")
                else:
                    self._write("{")
            
            self._newline()
            self._indent()
            self._generate_statement(kernel.body)
            self._dedent()
            self._write("}")
        
        self.in_kernel = False
    
    def _generate_function_declaration(self, func: OpenCLFunctionDeclaration) -> None:
        """Generate function declaration"""
        # Function qualifiers
        for qualifier in func.qualifiers:
            self._write(qualifier.value)
            self._write(" ")
        
        # Return type
        self._generate_type(func.return_type)
        self._write(" ")
        
        # Function name
        self._write(func.name)
        
        # Parameters
        self._write("(")
        self._generate_parameter_list(func.parameters)
        self._write(")")
        
        # Body or semicolon
        if func.body:
            if self.config.brace_style == "allman":
                self._newline()
                self._write("{")
            else:
                if self.config.space_after_keywords:
                    self._write(" {")
                else:
                    self._write("{")
            
            self._newline()
            self._indent()
            self._generate_statement(func.body)
            self._dedent()
            self._write("}")
        else:
            self._write(";")
    
    def _generate_parameter_list(self, parameters: List[OpenCLParameter]) -> None:
        """Generate function parameter list"""
        if not parameters:
            return
        
        self.in_function_params = True
        
        if self.config.align_parameters and len(parameters) > 1:
            # Multi-line parameter formatting
            for i, param in enumerate(parameters):
                if i > 0:
                    self._write(",")
                    self._newline()
                    self._write("    ")  # Align with opening parenthesis
                self._generate_parameter(param)
        else:
            # Single-line or simple formatting
            for i, param in enumerate(parameters):
                if i > 0:
                    self._write(", ")
                self._generate_parameter(param)
        
        self.in_function_params = False
    
    def _generate_parameter(self, param: OpenCLParameter) -> None:
        """Generate function parameter"""
        # Address space qualifier
        if param.address_space and self.config.memory_qualifier_spacing:
            self._write(param.address_space.value)
            self._write(" ")
        elif param.address_space:
            self._write(param.address_space.value)
        
        # Access qualifier
        if param.access_qualifier:
            if param.address_space and self.config.memory_qualifier_spacing:
                pass  # Space already added
            elif param.access_qualifier:
                self._write(" ")
            self._write(param.access_qualifier.value)
            self._write(" ")
        
        # Const qualifier
        if param.is_const:
            self._write("const ")
        
        # Type
        self._generate_type(param.type)
        self._write(" ")
        
        # Name
        self._write(param.name)
    
    def _generate_variable_declaration(self, var: OpenCLVariableDeclaration) -> None:
        """Generate variable declaration"""
        # Address space qualifier
        if var.address_space:
            self._write(var.address_space.value)
            self._write(" ")
        
        # Const qualifier
        if var.is_const:
            self._write("const ")
        
        # Type
        self._generate_type(var.type)
        self._write(" ")
        
        # Name
        self._write(var.name)
        
        # Initializer
        if var.initializer:
            if self.config.space_around_operators:
                self._write(" = ")
            else:
                self._write("=")
            self._generate_expression(var.initializer)
    
    def _generate_struct_declaration(self, struct: OpenCLStructDeclaration) -> None:
        """Generate struct declaration"""
        self._write("struct ")
        self._write(struct.name)
        
        if self.config.brace_style == "allman":
            self._newline()
            self._write("{")
        else:
            self._write(" {")
        
        self._newline()
        self._indent()
        
        for field in struct.fields:
            self._generate_variable_declaration(field)
            self._write(";")
            self._newline()
        
        self._dedent()
        self._write("}")
        
        if struct.is_packed:
            self._write(" __attribute__((packed))")
        
        self._write(";")
    
    def _generate_typedef_declaration(self, typedef: OpenCLTypedefDeclaration) -> None:
        """Generate typedef declaration"""
        self._write("typedef ")
        self._generate_type(typedef.type)
        self._write(" ")
        self._write(typedef.name)
        self._write(";")
    
    def _generate_enum_declaration(self, enum: OpenCLEnumDeclaration) -> None:
        """Generate enum declaration"""
        self._write("enum")
        if enum.name:
            self._write(" ")
            self._write(enum.name)
        
        if self.config.brace_style == "allman":
            self._newline()
            self._write("{")
        else:
            self._write(" {")
        
        self._newline()
        self._indent()
        
        for i, (name, value) in enumerate(enum.values):
            if i > 0:
                self._write(",")
                self._newline()
            
            self._write(name)
            if value:
                if self.config.space_around_operators:
                    self._write(" = ")
                else:
                    self._write("=")
                self._generate_expression(value)
        
        self._newline()
        self._dedent()
        self._write("};")
    
    def _generate_type(self, type_node: OpenCLType) -> None:
        """Generate type"""
        if isinstance(type_node, OpenCLBuiltinType):
            if type_node.vector_size:
                self._write(f"{type_node.name}{type_node.vector_size}")
            else:
                self._write(type_node.name)
        
        elif isinstance(type_node, OpenCLPointerType):
            self._generate_type(type_node.base_type)
            self._write("*")
            if type_node.address_space:
                self._write(" ")
                self._write(type_node.address_space.value)
        
        elif isinstance(type_node, OpenCLArrayType):
            self._generate_type(type_node.element_type)
            self._write("[")
            if type_node.size:
                self._generate_expression(type_node.size)
            self._write("]")
        
        elif isinstance(type_node, OpenCLImageType):
            self._write(f"image{type_node.dimension}_t")
    
    def _generate_statement(self, stmt: OpenCLStatement) -> None:
        """Generate statement"""
        if isinstance(stmt, OpenCLBlock):
            self._generate_block(stmt)
        elif isinstance(stmt, OpenCLExpressionStatement):
            self._generate_expression(stmt.expression)
            self._write(";")
            self._newline()
        elif isinstance(stmt, OpenCLIfStatement):
            self._generate_if_statement(stmt)
        elif isinstance(stmt, OpenCLWhileLoop):
            self._generate_while_statement(stmt)
        elif isinstance(stmt, OpenCLForLoop):
            self._generate_for_statement(stmt)
        elif isinstance(stmt, OpenCLDoWhileLoop):
            self._generate_do_while_statement(stmt)
        elif isinstance(stmt, OpenCLReturnStatement):
            self._generate_return_statement(stmt)
        elif isinstance(stmt, OpenCLBreakStatement):
            self._write("break;")
            self._newline()
        elif isinstance(stmt, OpenCLContinueStatement):
            self._write("continue;")
            self._newline()
        elif isinstance(stmt, OpenCLBarrier):
            self._generate_barrier(stmt)
    
    def _generate_block(self, block: OpenCLBlock) -> None:
        """Generate block statement"""
        for stmt in block.statements:
            self._generate_statement(stmt)
    
    def _generate_if_statement(self, if_stmt: OpenCLIfStatement) -> None:
        """Generate if statement"""
        self._write("if")
        if self.config.space_after_keywords:
            self._write(" (")
        else:
            self._write("(")
        
        self._generate_expression(if_stmt.condition)
        self._write(")")
        
        # Then statement
        if isinstance(if_stmt.then_stmt, OpenCLBlock):
            if self.config.brace_style == "allman":
                self._newline()
                self._write("{")
            else:
                if self.config.space_after_keywords:
                    self._write(" {")
                else:
                    self._write("{")
            
            self._newline()
            self._indent()
            self._generate_statement(if_stmt.then_stmt)
            self._dedent()
            self._write("}")
        else:
            self._newline()
            self._indent()
            self._generate_statement(if_stmt.then_stmt)
            self._dedent()
        
        # Else statement
        if if_stmt.else_stmt:
            self._write(" else")
            
            if isinstance(if_stmt.else_stmt, OpenCLBlock):
                if self.config.brace_style == "allman":
                    self._newline()
                    self._write("{")
                else:
                    if self.config.space_after_keywords:
                        self._write(" {")
                    else:
                        self._write("{")
                
                self._newline()
                self._indent()
                self._generate_statement(if_stmt.else_stmt)
                self._dedent()
                self._write("}")
            else:
                self._newline()
                self._indent()
                self._generate_statement(if_stmt.else_stmt)
                self._dedent()
        
        self._newline()
    
    def _generate_while_statement(self, while_stmt: OpenCLWhileLoop) -> None:
        """Generate while statement"""
        self._write("while")
        if self.config.space_after_keywords:
            self._write(" (")
        else:
            self._write("(")
        
        self._generate_expression(while_stmt.condition)
        self._write(")")
        
        if isinstance(while_stmt.body, OpenCLBlock):
            if self.config.brace_style == "allman":
                self._newline()
                self._write("{")
            else:
                if self.config.space_after_keywords:
                    self._write(" {")
                else:
                    self._write("{")
            
            self._newline()
            self._indent()
            self._generate_statement(while_stmt.body)
            self._dedent()
            self._write("}")
        else:
            self._newline()
            self._indent()
            self._generate_statement(while_stmt.body)
            self._dedent()
        
        self._newline()
    
    def _generate_for_statement(self, for_stmt: OpenCLForLoop) -> None:
        """Generate for statement"""
        self._write("for")
        if self.config.space_after_keywords:
            self._write(" (")
        else:
            self._write("(")
        
        # Init
        if for_stmt.init:
            if isinstance(for_stmt.init, OpenCLVariableDeclaration):
                self._generate_variable_declaration(for_stmt.init)
            else:
                self._generate_statement(for_stmt.init)
        self._write("; ")
        
        # Condition
        if for_stmt.condition:
            self._generate_expression(for_stmt.condition)
        self._write("; ")
        
        # Update
        if for_stmt.update:
            self._generate_expression(for_stmt.update)
        
        self._write(")")
        
        if isinstance(for_stmt.body, OpenCLBlock):
            if self.config.brace_style == "allman":
                self._newline()
                self._write("{")
            else:
                if self.config.space_after_keywords:
                    self._write(" {")
                else:
                    self._write("{")
            
            self._newline()
            self._indent()
            self._generate_statement(for_stmt.body)
            self._dedent()
            self._write("}")
        else:
            self._newline()
            self._indent()
            self._generate_statement(for_stmt.body)
            self._dedent()
        
        self._newline()
    
    def _generate_do_while_statement(self, do_while: OpenCLDoWhileLoop) -> None:
        """Generate do-while statement"""
        self._write("do")
        
        if isinstance(do_while.body, OpenCLBlock):
            if self.config.brace_style == "allman":
                self._newline()
                self._write("{")
            else:
                if self.config.space_after_keywords:
                    self._write(" {")
                else:
                    self._write("{")
            
            self._newline()
            self._indent()
            self._generate_statement(do_while.body)
            self._dedent()
            self._write("}")
        else:
            self._newline()
            self._indent()
            self._generate_statement(do_while.body)
            self._dedent()
        
        self._write(" while")
        if self.config.space_after_keywords:
            self._write(" (")
        else:
            self._write("(")
        
        self._generate_expression(do_while.condition)
        self._write(");")
        self._newline()
    
    def _generate_return_statement(self, return_stmt: OpenCLReturnStatement) -> None:
        """Generate return statement"""
        self._write("return")
        if return_stmt.value:
            self._write(" ")
            self._generate_expression(return_stmt.value)
        self._write(";")
        self._newline()
    
    def _generate_barrier(self, barrier: OpenCLBarrier) -> None:
        """Generate barrier statement"""
        self._write(f"barrier({barrier.memory_fence});")
        self._newline()
    
    def _generate_expression(self, expr: OpenCLExpression) -> None:
        """Generate expression"""
        if isinstance(expr, OpenCLIdentifier):
            self._write(expr.name)
        
        elif isinstance(expr, OpenCLLiteral):
            self._generate_literal(expr)
        
        elif isinstance(expr, OpenCLVectorLiteral):
            self._generate_vector_literal(expr)
        
        elif isinstance(expr, OpenCLBinaryOp):
            self._generate_binary_op(expr)
        
        elif isinstance(expr, OpenCLUnaryOp):
            self._generate_unary_op(expr)
        
        elif isinstance(expr, OpenCLArrayAccess):
            self._generate_expression(expr.array)
            self._write("[")
            self._generate_expression(expr.index)
            self._write("]")
        
        elif isinstance(expr, OpenCLFieldAccess):
            self._generate_expression(expr.object)
            self._write(".")
            self._write(expr.field)
        
        elif isinstance(expr, OpenCLFunctionCall):
            self._generate_function_call(expr)
        
        elif isinstance(expr, OpenCLBuiltinCall):
            self._generate_builtin_call(expr)
        
        elif isinstance(expr, OpenCLCast):
            self._generate_cast(expr)
        
        elif isinstance(expr, OpenCLConditional):
            self._generate_conditional(expr)
    
    def _generate_literal(self, literal: OpenCLLiteral) -> None:
        """Generate literal value"""
        if isinstance(literal.value, str):
            self._write(f'"{literal.value}"')
        elif isinstance(literal.value, bool):
            self._write("true" if literal.value else "false")
        elif isinstance(literal.value, float):
            if literal.type_hint == "half":
                self._write(f"{literal.value}h")
            elif literal.type_hint == "double":
                self._write(f"{literal.value}")
            else:
                self._write(f"{literal.value}f")
        else:
            self._write(str(literal.value))
    
    def _generate_vector_literal(self, vector: OpenCLVectorLiteral) -> None:
        """Generate vector literal"""
        self._write("(")
        self._write(vector.type_name)
        self._write(")(")
        
        if self.config.vector_literal_multiline and len(vector.components) > 2:
            for i, component in enumerate(vector.components):
                if i > 0:
                    self._write(",")
                    self._newline()
                    self._write("    ")
                self._generate_expression(component)
        else:
            for i, component in enumerate(vector.components):
                if i > 0:
                    self._write(", ")
                self._generate_expression(component)
        
        self._write(")")
    
    def _generate_binary_op(self, binary: OpenCLBinaryOp) -> None:
        """Generate binary operation"""
        need_parens = self._needs_parentheses(binary)
        
        if need_parens:
            self._write("(")
        
        self._generate_expression(binary.left)
        
        if self.config.space_around_operators:
            self._write(f" {binary.operator} ")
        else:
            self._write(binary.operator)
        
        self._generate_expression(binary.right)
        
        if need_parens:
            self._write(")")
    
    def _generate_unary_op(self, unary: OpenCLUnaryOp) -> None:
        """Generate unary operation"""
        if unary.operator in ["++", "--"] and self._is_postfix_operator(unary):
            self._generate_expression(unary.operand)
            self._write(unary.operator)
        else:
            self._write(unary.operator)
            self._generate_expression(unary.operand)
    
    def _generate_function_call(self, call: OpenCLFunctionCall) -> None:
        """Generate function call"""
        self._write(call.name)
        self._write("(")
        
        for i, arg in enumerate(call.args):
            if i > 0:
                self._write(", ")
            self._generate_expression(arg)
        
        self._write(")")
    
    def _generate_builtin_call(self, call: OpenCLBuiltinCall) -> None:
        """Generate built-in function call"""
        self._write(call.name)
        self._write("(")
        
        for i, arg in enumerate(call.args):
            if i > 0:
                self._write(", ")
            self._generate_expression(arg)
        
        self._write(")")
    
    def _generate_cast(self, cast: OpenCLCast) -> None:
        """Generate type cast"""
        self._write("(")
        self._generate_type(cast.target_type)
        self._write(")")
        self._generate_expression(cast.expression)
    
    def _generate_conditional(self, cond: OpenCLConditional) -> None:
        """Generate conditional expression"""
        self._generate_expression(cond.condition)
        self._write(" ? ")
        self._generate_expression(cond.true_expr)
        self._write(" : ")
        self._generate_expression(cond.false_expr)
    
    def _get_param_description(self, param: OpenCLParameter) -> str:
        """Get parameter description for documentation"""
        desc_parts = []
        
        if param.address_space:
            desc_parts.append(f"({param.address_space.value})")
        
        if param.access_qualifier:
            desc_parts.append(f"({param.access_qualifier.value})")
        
        return " ".join(desc_parts) if desc_parts else "parameter"
    
    def _needs_parentheses(self, expr: OpenCLBinaryOp) -> bool:
        """Check if binary expression needs parentheses"""
        # Simplified precedence check
        return False  # Could implement full precedence rules
    
    def _is_postfix_operator(self, unary: OpenCLUnaryOp) -> bool:
        """Check if unary operator is postfix"""
        return False  # Would need context analysis
    
    # Output utilities
    def _write(self, text: str) -> None:
        """Write text to output"""
        if self.at_line_start and text.strip():
            self._write_indent()
            self.at_line_start = False
        self.output.write(text)
    
    def _write_indent(self) -> None:
        """Write current indentation"""
        if self.config.use_tabs:
            self.output.write("\t" * self.indent_level)
        else:
            self.output.write(" " * (self.indent_level * self.config.indent_size))
    
    def _newline(self) -> None:
        """Write newline and mark at line start"""
        if not self.suppress_newlines:
            self.output.write("\n")
            self.at_line_start = True
    
    def _blank_lines(self, count: int) -> None:
        """Write blank lines"""
        for _ in range(count):
            self._newline()
    
    def _indent(self) -> None:
        """Increase indentation level"""
        self.indent_level += 1
    
    def _dedent(self) -> None:
        """Decrease indentation level"""
        self.indent_level = max(0, self.indent_level - 1)


class OpenCLFormatter:
    """High-level OpenCL code formatter"""
    
    def __init__(self, style: OpenCLCodeStyle = OpenCLCodeStyle.STANDARD):
        self.style = style
        self.config = OpenCLFormatConfig.from_style(style)
    
    def format_program(self, program: OpenCLProgram) -> str:
        """Format complete OpenCL program"""
        generator = OpenCLCodeGenerator(self.config)
        return generator.generate(program)
    
    def format_code(self, code: str) -> str:
        """Format OpenCL code string (requires parsing)"""
        # This would require the parser to be imported
        # from .opencl_parser import parse_opencl
        # program = parse_opencl(code)
        # return self.format_program(program)
        return code  # Placeholder
    
    def set_style(self, style: OpenCLCodeStyle) -> None:
        """Change formatting style"""
        self.style = style
        self.config = OpenCLFormatConfig.from_style(style)
    
    def customize_config(self, **kwargs) -> None:
        """Customize formatting configuration"""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)


# Convenience functions
def generate_opencl(program: OpenCLProgram, 
                   style: OpenCLCodeStyle = OpenCLCodeStyle.STANDARD) -> str:
    """Generate OpenCL code with specified style"""
    formatter = OpenCLFormatter(style)
    return formatter.format_program(program)


def format_opencl_code(code: str, 
                      style: OpenCLCodeStyle = OpenCLCodeStyle.STANDARD) -> str:
    """Format existing OpenCL code"""
    formatter = OpenCLFormatter(style)
    return formatter.format_code(code) 