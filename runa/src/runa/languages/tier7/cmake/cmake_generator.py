#!/usr/bin/env python3
"""
CMake Code Generator

Clean code generation for CMake build files including:
- CMakeLists.txt with proper formatting
- Modern CMake target-based syntax
- Cross-platform build configurations
- Variable and property management
"""

from typing import List, Dict, Any, Optional, Union, TextIO
from dataclasses import dataclass
from io import StringIO

from .cmake_ast import *


@dataclass
class CMakeCodeStyle:
    """Configuration for CMake code formatting."""
    indent_size: int = 2
    indent_char: str = " "
    max_line_length: int = 120
    command_case: str = "lower"  # lower, upper, title
    variable_case: str = "upper"  # upper, lower
    sort_properties: bool = True
    use_modern_syntax: bool = True
    separate_commands: bool = True


class CMakeFormatter:
    """Handles indentation and formatting for CMake code."""
    
    def __init__(self, style: CMakeCodeStyle):
        self.style = style
        self.current_indent = 0
        self.output = StringIO()
        
    def indent(self) -> None:
        """Increase indentation level."""
        self.current_indent += 1
    
    def dedent(self) -> None:
        """Decrease indentation level."""
        self.current_indent = max(0, self.current_indent - 1)
    
    def write_line(self, line: str = "") -> None:
        """Write a line with proper indentation."""
        if line.strip():
            indent_str = self.style.indent_char * (self.current_indent * self.style.indent_size)
            self.output.write(f"{indent_str}{line}\n")
        else:
            self.output.write("\n")
    
    def get_output(self) -> str:
        """Get the formatted output."""
        return self.output.getvalue()
    
    def reset(self) -> None:
        """Reset the formatter state."""
        self.current_indent = 0
        self.output = StringIO()


class CMakeCodeGenerator:
    """Generates clean CMake code from AST."""
    
    def __init__(self, style: Optional[CMakeCodeStyle] = None):
        self.style = style or CMakeCodeStyle()
        self.formatter = CMakeFormatter(self.style)
        
    def generate(self, node: CMakeNode) -> str:
        """Generate CMake code from AST node."""
        self.formatter.reset()
        
        if isinstance(node, CMakeFile):
            self._generate_cmake_file(node)
        elif isinstance(node, CommandInvocation):
            self._generate_command_invocation(node)
        elif isinstance(node, ProjectCommand):
            self._generate_project_command(node)
        elif isinstance(node, AddExecutable):
            self._generate_add_executable(node)
        elif isinstance(node, AddLibrary):
            self._generate_add_library(node)
        elif isinstance(node, SetCommand):
            self._generate_set_command(node)
        else:
            self._generate_expression(node)
        
        return self.formatter.get_output()
    
    def _generate_cmake_file(self, node: CMakeFile) -> None:
        """Generate CMakeLists.txt file content."""
        # CMake minimum required version
        if node.cmake_minimum_required:
            self.formatter.write_line(f"cmake_minimum_required(VERSION {node.cmake_minimum_required})")
            self.formatter.write_line()
        
        # Generate statements
        for i, stmt in enumerate(node.statements):
            self._generate_statement(stmt)
            if self.style.separate_commands and i < len(node.statements) - 1:
                self.formatter.write_line()
    
    def _generate_statement(self, stmt: CMakeStatement) -> None:
        """Generate code for a statement."""
        if isinstance(stmt, CommandInvocation):
            self._generate_command_invocation(stmt)
        elif isinstance(stmt, ProjectCommand):
            self._generate_project_command(stmt)
        elif isinstance(stmt, AddExecutable):
            self._generate_add_executable(stmt)
        elif isinstance(stmt, AddLibrary):
            self._generate_add_library(stmt)
        elif isinstance(stmt, SetCommand):
            self._generate_set_command(stmt)
        elif isinstance(stmt, TargetLinkLibraries):
            self._generate_target_link_libraries(stmt)
        elif isinstance(stmt, FindPackage):
            self._generate_find_package(stmt)
    
    def _generate_command_invocation(self, node: CommandInvocation) -> None:
        """Generate generic command invocation."""
        command_name = self._format_command_name(node.command_name)
        
        if not node.arguments:
            self.formatter.write_line(f"{command_name}()")
            return
        
        # Single line if short
        args_str = " ".join(self._generate_expression_string(arg) for arg in node.arguments)
        if len(command_name) + len(args_str) < self.style.max_line_length:
            self.formatter.write_line(f"{command_name}({args_str})")
        else:
            # Multi-line
            self.formatter.write_line(f"{command_name}(")
            self.formatter.indent()
            for arg in node.arguments:
                arg_str = self._generate_expression_string(arg)
                self.formatter.write_line(arg_str)
            self.formatter.dedent()
            self.formatter.write_line(")")
    
    def _generate_project_command(self, node: ProjectCommand) -> None:
        """Generate project command."""
        parts = [node.name]
        
        if node.version:
            parts.extend(["VERSION", node.version])
        
        if node.languages:
            parts.extend(["LANGUAGES"] + node.languages)
        
        if node.description:
            parts.extend(["DESCRIPTION", f'"{node.description}"'])
        
        command = self._format_command_name("project")
        args_str = " ".join(parts)
        
        if len(command) + len(args_str) < self.style.max_line_length:
            self.formatter.write_line(f"{command}({args_str})")
        else:
            self.formatter.write_line(f"{command}(")
            self.formatter.indent()
            for part in parts:
                self.formatter.write_line(part)
            self.formatter.dedent()
            self.formatter.write_line(")")
    
    def _generate_add_executable(self, node: AddExecutable) -> None:
        """Generate add_executable command."""
        command = self._format_command_name("add_executable")
        parts = [node.name]
        
        if node.is_win32:
            parts.append("WIN32")
        if node.is_macosx_bundle:
            parts.append("MACOSX_BUNDLE")
        if node.exclude_from_all:
            parts.append("EXCLUDE_FROM_ALL")
        
        parts.extend(node.sources)
        
        args_str = " ".join(parts)
        if len(command) + len(args_str) < self.style.max_line_length:
            self.formatter.write_line(f"{command}({args_str})")
        else:
            self.formatter.write_line(f"{command}(")
            self.formatter.indent()
            for part in parts:
                self.formatter.write_line(part)
            self.formatter.dedent()
            self.formatter.write_line(")")
    
    def _generate_add_library(self, node: AddLibrary) -> None:
        """Generate add_library command."""
        command = self._format_command_name("add_library")
        parts = [node.name]
        
        if node.library_type != "STATIC":
            parts.append(node.library_type)
        
        if node.exclude_from_all:
            parts.append("EXCLUDE_FROM_ALL")
        
        parts.extend(node.sources)
        
        args_str = " ".join(parts)
        if len(command) + len(args_str) < self.style.max_line_length:
            self.formatter.write_line(f"{command}({args_str})")
        else:
            self.formatter.write_line(f"{command}(")
            self.formatter.indent()
            for part in parts:
                self.formatter.write_line(part)
            self.formatter.dedent()
            self.formatter.write_line(")")
    
    def _generate_set_command(self, node: SetCommand) -> None:
        """Generate set command."""
        command = self._format_command_name("set")
        
        if isinstance(node.value, list):
            value_str = " ".join(f'"{v}"' if " " in v else v for v in node.value)
        else:
            value_str = f'"{node.value}"' if " " in str(node.value) else str(node.value)
        
        parts = [node.variable, value_str]
        
        if node.cache:
            parts.append("CACHE")
            if node.cache_type:
                parts.append(node.cache_type)
            if node.cache_docstring:
                parts.append(f'"{node.cache_docstring}"')
            if node.force:
                parts.append("FORCE")
        
        if node.parent_scope:
            parts.append("PARENT_SCOPE")
        
        args_str = " ".join(parts)
        if len(command) + len(args_str) < self.style.max_line_length:
            self.formatter.write_line(f"{command}({args_str})")
        else:
            self.formatter.write_line(f"{command}(")
            self.formatter.indent()
            for part in parts:
                self.formatter.write_line(part)
            self.formatter.dedent()
            self.formatter.write_line(")")
    
    def _generate_target_link_libraries(self, node: TargetLinkLibraries) -> None:
        """Generate target_link_libraries command."""
        command = self._format_command_name("target_link_libraries")
        parts = [node.target]
        
        if self.style.use_modern_syntax and node.scope != "PUBLIC":
            parts.append(node.scope)
        
        parts.extend(node.libraries)
        
        args_str = " ".join(parts)
        if len(command) + len(args_str) < self.style.max_line_length:
            self.formatter.write_line(f"{command}({args_str})")
        else:
            self.formatter.write_line(f"{command}(")
            self.formatter.indent()
            for part in parts:
                self.formatter.write_line(part)
            self.formatter.dedent()
            self.formatter.write_line(")")
    
    def _generate_find_package(self, node: FindPackage) -> None:
        """Generate find_package command."""
        command = self._format_command_name("find_package")
        parts = [node.package_name]
        
        if node.version:
            parts.append(node.version)
            if node.exact:
                parts.append("EXACT")
        
        if node.quiet:
            parts.append("QUIET")
        
        if node.required:
            parts.append("REQUIRED")
        
        if node.components:
            parts.extend(["COMPONENTS"] + node.components)
        
        if node.optional_components:
            parts.extend(["OPTIONAL_COMPONENTS"] + node.optional_components)
        
        args_str = " ".join(parts)
        if len(command) + len(args_str) < self.style.max_line_length:
            self.formatter.write_line(f"{command}({args_str})")
        else:
            self.formatter.write_line(f"{command}(")
            self.formatter.indent()
            for part in parts:
                self.formatter.write_line(part)
            self.formatter.dedent()
            self.formatter.write_line(")")
    
    def _generate_expression(self, node: CMakeExpression) -> None:
        """Generate expression code."""
        expr_str = self._generate_expression_string(node)
        self.formatter.write_line(expr_str)
    
    def _generate_expression_string(self, node: CMakeExpression) -> str:
        """Generate expression as string."""
        if isinstance(node, StringLiteral):
            return f'"{node.value}"' if " " in node.value else node.value
        elif isinstance(node, VariableRef):
            return f"${{{node.variable}}}"
        elif isinstance(node, GeneratorExpr):
            return node.expression
        elif isinstance(node, QuotedArgument):
            return f'"{node.content}"'
        elif isinstance(node, BracketArgument):
            level_str = "=" * node.level
            return f"[{level_str}[{node.content}]{level_str}]"
        else:
            return str(node)
    
    def _format_command_name(self, command: str) -> str:
        """Format command name according to style."""
        if self.style.command_case == "lower":
            return command.lower()
        elif self.style.command_case == "upper":
            return command.upper()
        elif self.style.command_case == "title":
            return command.title()
        else:
            return command


# Public API functions
def generate_cmake(node: CMakeNode, style: Optional[CMakeCodeStyle] = None) -> str:
    """Generate CMake code from AST node."""
    generator = CMakeCodeGenerator(style)
    return generator.generate(node)


# Export classes and functions
__all__ = [
    'CMakeCodeGenerator',
    'CMakeCodeStyle',
    'CMakeFormatter',
    'generate_cmake'
] 