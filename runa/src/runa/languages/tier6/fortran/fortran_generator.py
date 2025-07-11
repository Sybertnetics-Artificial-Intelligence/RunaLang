"""
Fortran Code Generator for Runa Universal Translation Platform
Generates clean, scientific computing optimized Fortran code

This generator produces high-quality Fortran code with:
- Support for both fixed-form (FORTRAN 77) and free-form (Fortran 90+) output
- Scientific computing best practices
- Proper array handling and mathematical operations
- Module system and interface generation
- Memory management (allocatable, pointer)
- Parallel constructs (coarrays, do concurrent)
"""

from typing import List, Optional, Dict, Any, Union
import logging
from dataclasses import dataclass

from .fortran_ast import *
from ...core.generator_base import BaseGenerator, GenerationError

logger = logging.getLogger(__name__)

@dataclass
class FortranGenerationContext:
    """Context for Fortran code generation"""
    indent_level: int = 0
    in_module: bool = False
    current_module: Optional[str] = None
    output_form: str = "free"  # free, fixed
    scientific_mode: bool = True
    precision_style: str = "explicit"  # explicit, implicit
    column_limit: int = 132  # 72 for fixed-form
    
class FortranGenerator(BaseGenerator):
    """Generates Fortran code from Fortran AST"""
    
    def __init__(self, output_form: str = "free"):
        super().__init__()
        self.context = FortranGenerationContext(output_form=output_form)
        
        # Set formatting based on form
        if output_form == "fixed":
            self.context.column_limit = 72
            self.indent_size = 6  # Start from column 7
        else:
            self.context.column_limit = 132
            self.indent_size = 2
            
    def generate(self, node: FortranNode) -> str:
        """Generate Fortran code from AST node"""
        try:
            method_name = f"_generate_{node.node_type.value}"
            if hasattr(self, method_name):
                return getattr(self, method_name)(node)
            else:
                logger.warning(f"No generator for node type: {node.node_type}")
                return f"! TODO: Generate {node.node_type.value}"
        except Exception as e:
            logger.error(f"Error generating Fortran code: {e}")
            raise GenerationError(f"Failed to generate code for {node.node_type}: {e}")
    
    def _get_indent(self) -> str:
        """Get current indentation string"""
        if self.context.output_form == "fixed":
            return " " * 6  # Fixed form starts at column 7
        else:
            return " " * (self.context.indent_level * self.indent_size)
    
    def _indent(self):
        """Increase indentation level"""
        self.context.indent_level += 1
    
    def _dedent(self):
        """Decrease indentation level"""
        self.context.indent_level = max(0, self.context.indent_level - 1)
    
    # Program structure generators
    
    def _generate_program(self, node: FortranProgram) -> str:
        """Generate Fortran program"""
        lines = []
        
        # Program statement
        lines.append(f"program {node.name}")
        self._indent()
        
        # Implicit none for good practice
        if self.context.scientific_mode:
            lines.append(self._get_indent() + "implicit none")
            lines.append("")
        
        # Variable declarations
        for var_decl in node.variables:
            lines.append(self._get_indent() + self.generate(var_decl))
        
        if node.variables:
            lines.append("")
        
        # Program statements
        for stmt in node.statements:
            stmt_code = self.generate(stmt)
            if stmt_code.strip():
                lines.append(self._get_indent() + stmt_code)
        
        # Contains section
        if node.contains_section:
            lines.append("")
            lines.append(self._get_indent() + "contains")
            lines.append("")
            
            for proc in node.contains_section:
                proc_code = self.generate(proc)
                lines.append(proc_code)
                lines.append("")
        
        self._dedent()
        lines.append(f"end program {node.name}")
        
        return "\n".join(lines)
    
    def _generate_module(self, node: FortranModule) -> str:
        """Generate Fortran module"""
        lines = []
        
        # Module statement
        lines.append(f"module {node.name}")
        self._indent()
        
        self.context.in_module = True
        self.context.current_module = node.name
        
        # Implicit none
        if self.context.scientific_mode:
            lines.append(self._get_indent() + "implicit none")
            lines.append("")
        
        # Use statements
        for use_stmt in node.use_statements:
            lines.append(self._get_indent() + self.generate(use_stmt))
        
        if node.use_statements:
            lines.append("")
        
        # Public/private declarations
        lines.append(self._get_indent() + "private")
        lines.append("")
        
        # Declarations
        for decl in node.declarations:
            lines.append(self._get_indent() + self.generate(decl))
        
        # Interfaces
        for interface in node.interfaces:
            lines.append("")
            lines.append(self._get_indent() + self.generate(interface))
        
        # Contains section
        if node.contains_section:
            lines.append("")
            lines.append(self._get_indent() + "contains")
            lines.append("")
            
            for proc in node.contains_section:
                proc_code = self.generate(proc)
                # Indent the procedure
                proc_lines = proc_code.split('\n')
                for proc_line in proc_lines:
                    if proc_line.strip():
                        lines.append(self._get_indent() + proc_line)
                    else:
                        lines.append("")
                lines.append("")
        
        self._dedent()
        lines.append(f"end module {node.name}")
        
        self.context.in_module = False
        
        return "\n".join(lines)
    
    def _generate_subroutine(self, node: FortranSubroutine) -> str:
        """Generate Fortran subroutine"""
        lines = []
        
        # Subroutine signature
        sub_line = f"subroutine {node.name}"
        
        if node.parameters:
            param_names = [param.name for param in node.parameters]
            sub_line += f"({', '.join(param_names)})"
        
        lines.append(sub_line)
        self._indent()
        
        # Implicit none
        if self.context.scientific_mode:
            lines.append(self._get_indent() + "implicit none")
            lines.append("")
        
        # Parameter declarations
        for param in node.parameters:
            if param.type_spec:
                param_line = self._get_indent()
                
                # Add intent if specified
                if param.intent:
                    param_line += f"{self.generate(param.type_spec)}, intent({param.intent}) :: {param.name}"
                else:
                    param_line += f"{self.generate(param.type_spec)} :: {param.name}"
                
                lines.append(param_line)
        
        # Variable declarations
        for var_decl in node.variables:
            lines.append(self._get_indent() + self.generate(var_decl))
        
        if node.parameters or node.variables:
            lines.append("")
        
        # Subroutine body
        for stmt in node.statements:
            stmt_code = self.generate(stmt)
            if stmt_code.strip():
                lines.append(self._get_indent() + stmt_code)
        
        # Contains section
        if node.contains_section:
            lines.append("")
            lines.append(self._get_indent() + "contains")
            lines.append("")
            
            for proc in node.contains_section:
                proc_code = self.generate(proc)
                lines.append(proc_code)
                lines.append("")
        
        self._dedent()
        lines.append(f"end subroutine {node.name}")
        
        return "\n".join(lines)
    
    def _generate_function(self, node: FortranFunction) -> str:
        """Generate Fortran function"""
        lines = []
        
        # Function signature
        func_line = ""
        
        # Add return type if specified
        if node.return_type:
            func_line += f"{self.generate(node.return_type)} "
        
        func_line += f"function {node.name}"
        
        if node.parameters:
            param_names = [param.name for param in node.parameters]
            func_line += f"({', '.join(param_names)})"
        
        # Add result clause if specified
        if node.result_variable:
            func_line += f" result({node.result_variable})"
        
        lines.append(func_line)
        self._indent()
        
        # Implicit none
        if self.context.scientific_mode:
            lines.append(self._get_indent() + "implicit none")
            lines.append("")
        
        # Parameter declarations
        for param in node.parameters:
            if param.type_spec:
                param_line = self._get_indent()
                
                # Add intent if specified
                if param.intent:
                    param_line += f"{self.generate(param.type_spec)}, intent({param.intent}) :: {param.name}"
                else:
                    param_line += f"{self.generate(param.type_spec)} :: {param.name}"
                
                lines.append(param_line)
        
        # Variable declarations
        for var_decl in node.variables:
            lines.append(self._get_indent() + self.generate(var_decl))
        
        if node.parameters or node.variables:
            lines.append("")
        
        # Function body
        for stmt in node.statements:
            stmt_code = self.generate(stmt)
            if stmt_code.strip():
                lines.append(self._get_indent() + stmt_code)
        
        self._dedent()
        lines.append(f"end function {node.name}")
        
        return "\n".join(lines)
    
    def _generate_interface(self, node: FortranInterface) -> str:
        """Generate Fortran interface"""
        lines = []
        
        if node.name:
            lines.append(f"interface {node.name}")
        else:
            lines.append("interface")
        
        self._indent()
        
        for proc in node.procedures:
            proc_code = self.generate(proc)
            lines.append(self._get_indent() + proc_code)
        
        self._dedent()
        lines.append("end interface")
        
        return "\n".join(lines)
    
    # Declaration generators
    
    def _generate_variable_declaration(self, node: FortranVariableDeclaration) -> str:
        """Generate variable declaration"""
        type_line = self.generate(node.type_spec)
        
        # Add attributes
        if node.attributes:
            attr_str = ", ".join(node.attributes)
            type_line += f", {attr_str}"
        
        # Add double colon for modern style
        type_line += " :: "
        
        # Add variable names
        var_names = ", ".join(node.names)
        type_line += var_names
        
        # Add initialization if present
        if node.initialization:
            init_value = self.generate(node.initialization)
            type_line += f" = {init_value}"
        
        return type_line
    
    def _generate_intrinsic_type(self, node: FortranTypeSpec) -> str:
        """Generate intrinsic type specification"""
        type_str = node.type_name
        
        if node.kind:
            if isinstance(node.kind, int):
                type_str += f"(kind={node.kind})"
            else:
                type_str += f"(kind={node.kind})"
        elif node.length:
            type_str += f"(len={node.length})"
        
        return type_str
    
    def _generate_use_statement(self, node: FortranUseStatement) -> str:
        """Generate use statement"""
        use_line = f"use {node.module_name}"
        
        if node.only_list:
            only_items = ", ".join(node.only_list)
            use_line += f", only: {only_items}"
        
        return use_line
    
    # Control structure generators
    
    def _generate_if_construct(self, node: FortranIfConstruct) -> str:
        """Generate if construct"""
        lines = []
        
        # If statement
        condition = self.generate(node.condition)
        if_line = f"if ({condition}) then"
        
        if node.construct_name:
            if_line = f"{node.construct_name}: {if_line}"
        
        lines.append(if_line)
        
        # Then block
        self._indent()
        for stmt in node.then_block:
            stmt_code = self.generate(stmt)
            if stmt_code.strip():
                lines.append(self._get_indent() + stmt_code)
        self._dedent()
        
        # Elsif blocks
        for elsif in node.elsif_blocks:
            elsif_condition = self.generate(elsif.condition)
            lines.append(f"else if ({elsif_condition}) then")
            
            self._indent()
            for stmt in elsif.statements:
                stmt_code = self.generate(stmt)
                if stmt_code.strip():
                    lines.append(self._get_indent() + stmt_code)
            self._dedent()
        
        # Else block
        if node.else_block:
            lines.append("else")
            
            self._indent()
            for stmt in node.else_block:
                stmt_code = self.generate(stmt)
                if stmt_code.strip():
                    lines.append(self._get_indent() + stmt_code)
            self._dedent()
        
        # End if
        end_line = "end if"
        if node.construct_name:
            end_line += f" {node.construct_name}"
        
        lines.append(end_line)
        
        return "\n".join(lines)
    
    def _generate_do_construct(self, node: FortranDoConstruct) -> str:
        """Generate do construct"""
        lines = []
        
        # Do statement
        do_line = "do"
        
        if node.construct_name:
            do_line = f"{node.construct_name}: {do_line}"
        
        # Add loop variable and bounds
        if node.variable and node.start and node.end:
            do_line += f" {node.variable} = {self.generate(node.start)}, {self.generate(node.end)}"
            
            if node.step:
                do_line += f", {self.generate(node.step)}"
        
        lines.append(do_line)
        
        # Do body
        self._indent()
        for stmt in node.body:
            stmt_code = self.generate(stmt)
            if stmt_code.strip():
                lines.append(self._get_indent() + stmt_code)
        self._dedent()
        
        # End do
        end_line = "end do"
        if node.construct_name:
            end_line += f" {node.construct_name}"
        
        lines.append(end_line)
        
        return "\n".join(lines)
    
    def _generate_do_concurrent(self, node: FortranDoConcurrent) -> str:
        """Generate do concurrent construct"""
        lines = []
        
        # Do concurrent statement
        do_line = "do concurrent"
        
        if node.construct_name:
            do_line = f"{node.construct_name}: {do_line}"
        
        # Add concurrent headers
        if node.concurrent_headers:
            header_strs = []
            for header in node.concurrent_headers:
                header_str = f"{header.variable} = {self.generate(header.start)}:{self.generate(header.end)}"
                if header.step:
                    header_str += f":{self.generate(header.step)}"
                header_strs.append(header_str)
            
            do_line += f" ({', '.join(header_strs)})"
        
        # Add mask if present
        if node.mask:
            do_line += f", {self.generate(node.mask)}"
        
        lines.append(do_line)
        
        # Do body
        self._indent()
        for stmt in node.body:
            stmt_code = self.generate(stmt)
            if stmt_code.strip():
                lines.append(self._get_indent() + stmt_code)
        self._dedent()
        
        # End do
        end_line = "end do"
        if node.construct_name:
            end_line += f" {node.construct_name}"
        
        lines.append(end_line)
        
        return "\n".join(lines)
    
    # Expression generators
    
    def _generate_assignment(self, node: FortranAssignment) -> str:
        """Generate assignment statement"""
        lhs = self.generate(node.lhs)
        rhs = self.generate(node.rhs)
        
        if node.is_pointer_assignment:
            return f"{lhs} => {rhs}"
        else:
            return f"{lhs} = {rhs}"
    
    def _generate_binary_operation(self, node: FortranBinaryOperation) -> str:
        """Generate binary operation"""
        left = self.generate(node.left)
        right = self.generate(node.right)
        
        # Add parentheses for clarity in scientific expressions
        if node.operator in ["**", "*", "/"]:
            return f"{left} {node.operator} {right}"
        else:
            return f"({left} {node.operator} {right})"
    
    def _generate_unary_operation(self, node: FortranUnaryOperation) -> str:
        """Generate unary operation"""
        operand = self.generate(node.operand)
        
        if node.operator == ".not.":
            return f".not. {operand}"
        else:
            return f"{node.operator}{operand}"
    
    def _generate_function_call(self, node: FortranFunctionCall) -> str:
        """Generate function call"""
        args = [self.generate(arg) for arg in node.arguments]
        
        if args:
            return f"{node.name}({', '.join(args)})"
        else:
            return f"{node.name}()"
    
    def _generate_array_reference(self, node: FortranArrayReference) -> str:
        """Generate array reference"""
        array = self.generate(node.array)
        indices = [self.generate(idx) for idx in node.indices]
        
        return f"{array}({', '.join(indices)})"
    
    def _generate_array_section(self, node: FortranArraySection) -> str:
        """Generate array section"""
        array = self.generate(node.array)
        
        section_strs = []
        for triplet in node.section_subscripts:
            section_str = ""
            if triplet.start:
                section_str += self.generate(triplet.start)
            section_str += ":"
            if triplet.end:
                section_str += self.generate(triplet.end)
            if triplet.stride:
                section_str += f":{self.generate(triplet.stride)}"
            
            section_strs.append(section_str)
        
        return f"{array}({', '.join(section_strs)})"
    
    # I/O statement generators
    
    def _generate_read_statement(self, node: FortranReadStatement) -> str:
        """Generate read statement"""
        read_str = "read"
        
        # Add unit and format if present
        specifiers = []
        if node.unit:
            specifiers.append(f"unit={self.generate(node.unit)}")
        if node.format:
            specifiers.append(f"fmt={self.generate(node.format)}")
        
        if specifiers:
            read_str += f"({', '.join(specifiers)})"
        
        # Add variables
        if node.variables:
            var_list = [self.generate(var) for var in node.variables]
            read_str += f" {', '.join(var_list)}"
        
        return read_str
    
    def _generate_write_statement(self, node: FortranWriteStatement) -> str:
        """Generate write statement"""
        write_str = "write"
        
        # Add unit and format if present
        specifiers = []
        if node.unit:
            specifiers.append(f"unit={self.generate(node.unit)}")
        if node.format:
            specifiers.append(f"fmt={self.generate(node.format)}")
        
        if specifiers:
            write_str += f"({', '.join(specifiers)})"
        
        # Add expressions
        if node.expressions:
            expr_list = [self.generate(expr) for expr in node.expressions]
            write_str += f" {', '.join(expr_list)}"
        
        return write_str
    
    def _generate_print_statement(self, node: FortranPrintStatement) -> str:
        """Generate print statement"""
        print_str = "print"
        
        if node.format:
            print_str += f" {self.generate(node.format)}"
        else:
            print_str += " *"
        
        if node.expressions:
            expr_list = [self.generate(expr) for expr in node.expressions]
            print_str += f", {', '.join(expr_list)}"
        
        return print_str
    
    # Literal generators
    
    def _generate_integer_literal(self, node: FortranIntegerLiteral) -> str:
        """Generate integer literal"""
        if node.kind:
            return f"{node.value}_{node.kind}"
        else:
            return str(node.value)
    
    def _generate_real_literal(self, node: FortranRealLiteral) -> str:
        """Generate real literal"""
        # Format for scientific notation if appropriate
        if abs(node.value) >= 1e6 or (abs(node.value) < 1e-3 and node.value != 0):
            value_str = f"{node.value:.6e}"
        else:
            value_str = str(node.value)
            if '.' not in value_str:
                value_str += '.0'
        
        if node.kind:
            return f"{value_str}_{node.kind}"
        else:
            return value_str
    
    def _generate_complex_literal(self, node: FortranComplexLiteral) -> str:
        """Generate complex literal"""
        real_part = self._format_numeric_part(node.real_part)
        imag_part = self._format_numeric_part(node.imag_part)
        
        complex_str = f"({real_part}, {imag_part})"
        
        if node.kind:
            complex_str += f"_{node.kind}"
        
        return complex_str
    
    def _generate_logical_literal(self, node: FortranLogicalLiteral) -> str:
        """Generate logical literal"""
        value_str = ".true." if node.value else ".false."
        
        if node.kind:
            return f"{value_str}_{node.kind}"
        else:
            return value_str
    
    def _generate_character_literal(self, node: FortranCharacterLiteral) -> str:
        """Generate character literal"""
        # Escape single quotes
        escaped_value = node.value.replace("'", "''")
        
        if node.kind:
            return f"{node.kind}_'{escaped_value}'"
        else:
            return f"'{escaped_value}'"
    
    def _generate_identifier(self, node: FortranIdentifier) -> str:
        """Generate identifier"""
        return node.name
    
    # Utility methods
    
    def _format_numeric_part(self, value: Union[int, float]) -> str:
        """Format numeric part for complex literals"""
        if isinstance(value, int):
            return str(value)
        else:
            return f"{value:.6g}"
    
    def set_output_form(self, form: str):
        """Set output form (free or fixed)"""
        self.context.output_form = form
        
        if form == "fixed":
            self.context.column_limit = 72
            self.indent_size = 6
        else:
            self.context.column_limit = 132
            self.indent_size = 2
    
    def enable_scientific_mode(self):
        """Enable scientific computing optimizations"""
        self.context.scientific_mode = True 