#!/usr/bin/env python3
"""
Shell Generator - Clean Shell Script Code Generation

Provides comprehensive shell script code generation with multiple formatting styles:
- POSIX sh compatible output
- Bash-specific features and syntax
- Zsh extended functionality
- Fish shell modern syntax
- Compact format for minimal space usage
- Readable format with proper indentation and comments

Features:
- Proper command and pipeline formatting
- Quote handling and escaping
- Variable expansion and substitution
- Function definition formatting
- Control structure indentation
- Comment preservation and generation
- Redirection and operator handling
- Cross-shell compatibility options
"""

from typing import List, Dict, Optional, Any, Union, TextIO
from dataclasses import dataclass
from enum import Enum
import io
import re
import shlex

from .shell_ast import *


class ShellDialect(Enum):
    """Shell dialect types"""
    POSIX = "sh"              # POSIX sh compatible
    BASH = "bash"             # Bash-specific features
    ZSH = "zsh"               # Zsh extended features
    FISH = "fish"             # Fish shell modern syntax
    DASH = "dash"             # Debian Almquist shell


class ShellFormatStyle(Enum):
    """Shell code formatting styles"""
    STANDARD = "standard"          # Clean, readable shell
    COMPACT = "compact"            # Minimal spacing
    READABLE = "readable"          # Enhanced readability with comments
    STRICT = "strict"              # Strict POSIX compliance
    MODERN = "modern"              # Modern shell features


@dataclass
class ShellGeneratorConfig:
    """Configuration for Shell code generation"""
    dialect: ShellDialect = ShellDialect.BASH
    style: ShellFormatStyle = ShellFormatStyle.STANDARD
    indent_size: int = 2
    max_line_length: int = 120
    use_long_options: bool = True
    quote_variables: bool = True
    add_error_handling: bool = True
    add_type_comments: bool = False
    preserve_comments: bool = True
    
    # Formatting options
    align_assignments: bool = True
    separate_functions: bool = True
    add_function_headers: bool = False
    sort_functions: bool = False
    
    # Safety options
    strict_mode: bool = False  # set -euo pipefail
    readonly_variables: bool = False
    check_commands: bool = False
    
    # Compatibility options
    posix_compliant: bool = False
    avoid_bashisms: bool = False
    use_local_variables: bool = True


class ShellCodeGenerator:
    """Generates clean shell script code from AST"""
    
    def __init__(self, config: Optional[ShellGeneratorConfig] = None):
        self.config = config or ShellGeneratorConfig()
        self.output = io.StringIO()
        self.indent_level = 0
        self.current_line_length = 0
        self.needs_newline = False
        self.in_function = False
        self.variables_declared = set()
        
        # Shell-specific syntax patterns
        self.shell_syntax = {
            ShellDialect.POSIX: {
                "function_syntax": "name() {",
                "local_var": "",
                "array_support": False,
                "test_command": "test",
                "process_substitution": False
            },
            ShellDialect.BASH: {
                "function_syntax": "function name() {",
                "local_var": "local",
                "array_support": True,
                "test_command": "[[",
                "process_substitution": True
            },
            ShellDialect.ZSH: {
                "function_syntax": "function name() {",
                "local_var": "local",
                "array_support": True,
                "test_command": "[[",
                "process_substitution": True
            },
            ShellDialect.FISH: {
                "function_syntax": "function name",
                "local_var": "set -l",
                "array_support": True,
                "test_command": "test",
                "process_substitution": False
            }
        }
        
        # Commands that should be quoted
        self.quote_requiring_commands = {
            "echo", "printf", "test", "[", "grep", "sed", "awk"
        }
    
    def generate(self, node: ShellNode) -> str:
        """Generate shell code from AST node"""
        self.output = io.StringIO()
        self.indent_level = 0
        self.current_line_length = 0
        self.needs_newline = False
        self.in_function = False
        self.variables_declared = set()
        
        if isinstance(node, ShellScript):
            self._generate_script(node)
        else:
            node.accept(self)
        
        return self.output.getvalue()
    
    def _generate_script(self, script: ShellScript) -> None:
        """Generate complete shell script"""
        # Add shebang
        if script.shebang:
            self._write_line(script.shebang)
        else:
            shebang = self._get_default_shebang()
            self._write_line(shebang)
        
        self._write_line("")
        
        # Add strict mode if configured
        if self.config.strict_mode:
            self._write_line("set -euo pipefail")
            self._write_line("")
        
        # Add script header comment if readable style
        if self.config.style == ShellFormatStyle.READABLE:
            self._write_line("# Generated shell script")
            self._write_line(f"# Dialect: {self.config.dialect.value}")
            self._write_line("")
        
        # Generate variable assignments first
        variable_assignments = script.get_variable_assignments()
        if variable_assignments:
            if self.config.style == ShellFormatStyle.READABLE:
                self._write_line("# Variables")
            
            for var_assign in variable_assignments:
                var_assign.accept(self)
            
            if variable_assignments:
                self._write_line("")
        
        # Generate functions
        if script.functions:
            if self.config.style == ShellFormatStyle.READABLE:
                self._write_line("# Functions")
                self._write_line("")
            
            functions = script.functions
            if self.config.sort_functions:
                functions = sorted(functions, key=lambda f: f.name)
            
            for i, func in enumerate(functions):
                if i > 0 and self.config.separate_functions:
                    self._write_line("")
                func.accept(self)
            
            if functions:
                self._write_line("")
        
        # Generate main script statements
        if script.statements:
            if self.config.style == ShellFormatStyle.READABLE and script.functions:
                self._write_line("# Main script")
                self._write_line("")
            
            for i, stmt in enumerate(script.statements):
                if i > 0 and isinstance(stmt, (ShellConditional, ShellLoop, ShellFunctionDefinition)):
                    self._write_line("")
                stmt.accept(self)
    
    def _get_default_shebang(self) -> str:
        """Get default shebang for dialect"""
        shebangs = {
            ShellDialect.POSIX: "#!/bin/sh",
            ShellDialect.BASH: "#!/bin/bash",
            ShellDialect.ZSH: "#!/bin/zsh",
            ShellDialect.FISH: "#!/usr/bin/fish",
            ShellDialect.DASH: "#!/bin/dash"
        }
        return shebangs.get(self.config.dialect, "#!/bin/bash")
    
    # Visitor methods
    def visit_shell_script(self, node: ShellScript) -> None:
        self._generate_script(node)
    
    def visit_shell_command(self, node: ShellCommand) -> None:
        """Generate shell command"""
        self._write_indent()
        
        # Add environment variables
        if node.environment:
            for key, value in node.environment.items():
                self._write(f'{key}="{self._escape_string(value)}" ')
        
        # Write command
        if self._needs_command_quoting(node.command):
            self._write(f'"{node.command}"')
        else:
            self._write(node.command)
        
        # Write arguments
        for arg in node.arguments:
            self._write(" ")
            self._write(self._format_argument(arg))
        
        # Write redirections
        for redir in node.redirections:
            self._write(" ")
            self._write(redir.get_redirection_string())
        
        # Background execution
        if node.background:
            self._write(" &")
        
        self._write_line()
    
    def visit_shell_pipeline(self, node: ShellPipeline) -> None:
        """Generate shell pipeline"""
        self._write_indent()
        
        if node.negated:
            self._write("! ")
        
        # Check if pipeline fits on one line
        pipeline_length = self._estimate_pipeline_length(node)
        
        if pipeline_length > self.config.max_line_length:
            self._write_multiline_pipeline(node)
        else:
            self._write_inline_pipeline(node)
        
        self._write_line()
    
    def visit_shell_compound_command(self, node: ShellCompoundCommand) -> None:
        """Generate shell compound command"""
        if node.is_subshell:
            self._write_indent()
            self._write("(")
            if self.config.style != ShellFormatStyle.COMPACT:
                self._write_line()
                self.indent_level += 1
            
            for stmt in node.body:
                stmt.accept(self)
            
            if self.config.style != ShellFormatStyle.COMPACT:
                self.indent_level -= 1
                self._write_indent()
            
            self._write(")")
        elif node.is_group:
            self._write_indent()
            self._write("{")
            if self.config.style != ShellFormatStyle.COMPACT:
                self._write_line()
                self.indent_level += 1
            
            for stmt in node.body:
                stmt.accept(self)
            
            if self.config.style != ShellFormatStyle.COMPACT:
                self.indent_level -= 1
                self._write_indent()
            
            self._write("}")
        
        self._write_line()
    
    def visit_shell_function_definition(self, node: ShellFunctionDefinition) -> None:
        """Generate shell function definition"""
        self.in_function = True
        
        if self.config.add_function_headers and self.config.style == ShellFormatStyle.READABLE:
            self._write_line(f"# Function: {node.name}")
            if node.parameters:
                self._write_line(f"# Parameters: {', '.join(node.parameters)}")
            self._write_line("")
        
        # Function declaration syntax
        syntax = self.shell_syntax[self.config.dialect]["function_syntax"]
        
        self._write_indent()
        if self.config.dialect == ShellDialect.FISH:
            self._write(f"function {node.name}")
        elif self.config.dialect == ShellDialect.POSIX:
            self._write(f"{node.name}() {{")
        else:
            if syntax.startswith("function"):
                self._write(f"function {node.name}() {{")
            else:
                self._write(f"{node.name}() {{")
        
        self._write_line()
        self.indent_level += 1
        
        # Add local variable declarations if supported
        if (self.config.use_local_variables and 
            self.config.dialect in (ShellDialect.BASH, ShellDialect.ZSH)):
            local_vars = list(node.local_variables.keys())
            if local_vars:
                for var in local_vars:
                    self._write_indent()
                    self._write(f'local {var}')
                    if node.local_variables[var]:
                        self._write(f'="{self._escape_string(node.local_variables[var])}"')
                    self._write_line()
                self._write_line()
        
        # Function body
        for stmt in node.body:
            stmt.accept(self)
        
        self.indent_level -= 1
        self._write_indent()
        
        if self.config.dialect == ShellDialect.FISH:
            self._write("end")
        else:
            self._write("}")
        
        self._write_line()
        self.in_function = False
    
    def visit_shell_variable_assignment(self, node: ShellVariableAssignment) -> None:
        """Generate shell variable assignment"""
        self._write_indent()
        
        # Add export/readonly/local prefix
        if node.export and not self.in_function:
            self._write("export ")
        elif node.readonly:
            self._write("readonly ")
        elif node.local and self.in_function:
            local_keyword = self.shell_syntax[self.config.dialect]["local_var"]
            if local_keyword:
                self._write(f"{local_keyword} ")
        
        # Variable name
        self._write(node.variable)
        
        # Assignment
        if node.array and self.shell_syntax[self.config.dialect]["array_support"]:
            # Array assignment
            self._write("=(")
            for i, value in enumerate(node.array_values):
                if i > 0:
                    self._write(" ")
                self._write(f'"{self._escape_string(value)}"')
            self._write(")")
        else:
            # Regular assignment
            self._write("=")
            if self.config.quote_variables or " " in node.value:
                self._write(f'"{self._escape_string(node.value)}"')
            else:
                self._write(node.value)
        
        self._write_line()
        self.variables_declared.add(node.variable)
    
    def visit_shell_conditional(self, node: ShellConditional) -> None:
        """Generate shell conditional statement"""
        if node.is_case_statement:
            self._generate_case_statement(node)
        else:
            self._generate_if_statement(node)
    
    def visit_shell_loop(self, node: ShellLoop) -> None:
        """Generate shell loop statement"""
        if node.is_for_loop:
            self._generate_for_loop(node)
        elif node.is_while_loop:
            self._generate_while_loop(node)
        elif node.is_until_loop:
            self._generate_until_loop(node)
    
    def visit_shell_redirection(self, node: ShellRedirection) -> None:
        """Generate shell redirection (usually handled by command)"""
        self._write(node.get_redirection_string())
    
    def visit_shell_expansion(self, node: ShellExpansion) -> None:
        """Generate shell expansion"""
        if isinstance(node, ShellParameterExpansion):
            self._write(node.get_expansion_string())
        elif isinstance(node, ShellCommandSubstitution):
            self._write(node.get_substitution_string())
        elif isinstance(node, ShellArithmeticExpansion):
            self._write(node.get_expansion_string())
    
    def visit_shell_comment(self, node: ShellComment) -> None:
        """Generate shell comment"""
        if self.config.preserve_comments:
            if node.inline:
                self._write("  # ")
                self._write(node.text)
            else:
                self._write_indent()
                self._write("# ")
                self._write(node.text)
                self._write_line()
    
    # Helper methods for complex structures
    def _generate_if_statement(self, node: ShellConditional) -> None:
        """Generate if statement"""
        self._write_indent()
        self._write("if ")
        self._write(self._format_condition(node.condition))
        self._write("; then")
        self._write_line()
        
        self.indent_level += 1
        for stmt in node.then_body:
            stmt.accept(self)
        self.indent_level -= 1
        
        # elif clauses
        for elif_condition, elif_body in node.elif_clauses:
            self._write_indent()
            self._write("elif ")
            self._write(self._format_condition(elif_condition))
            self._write("; then")
            self._write_line()
            
            self.indent_level += 1
            for stmt in elif_body:
                stmt.accept(self)
            self.indent_level -= 1
        
        # else clause
        if node.else_body:
            self._write_indent()
            self._write("else")
            self._write_line()
            
            self.indent_level += 1
            for stmt in node.else_body:
                stmt.accept(self)
            self.indent_level -= 1
        
        self._write_indent()
        self._write("fi")
        self._write_line()
    
    def _generate_case_statement(self, node: ShellConditional) -> None:
        """Generate case statement"""
        self._write_indent()
        self._write("case ")
        self._write(self._format_shell_value(node.condition))
        self._write(" in")
        self._write_line()
        
        self.indent_level += 1
        
        for pattern, body in node.case_patterns:
            self._write_indent()
            self._write(pattern)
            self._write(")")
            self._write_line()
            
            self.indent_level += 1
            for stmt in body:
                stmt.accept(self)
            
            # Add ;; separator
            self._write_indent()
            self._write(";;")
            self._write_line()
            self.indent_level -= 1
        
        self.indent_level -= 1
        self._write_indent()
        self._write("esac")
        self._write_line()
    
    def _generate_for_loop(self, node: ShellLoop) -> None:
        """Generate for loop"""
        self._write_indent()
        
        if self.config.dialect == ShellDialect.FISH:
            self._write(f"for {node.variable} in {self._format_shell_value(node.iterable or '')}")
        else:
            self._write(f"for {node.variable} in {self._format_shell_value(node.iterable or '$@')}")
        
        if self.config.dialect == ShellDialect.FISH:
            self._write_line()
        else:
            self._write("; do")
            self._write_line()
        
        self.indent_level += 1
        for stmt in node.body:
            stmt.accept(self)
        self.indent_level -= 1
        
        self._write_indent()
        if self.config.dialect == ShellDialect.FISH:
            self._write("end")
        else:
            self._write("done")
        self._write_line()
    
    def _generate_while_loop(self, node: ShellLoop) -> None:
        """Generate while loop"""
        self._write_indent()
        self._write("while ")
        self._write(self._format_condition(node.condition))
        
        if self.config.dialect == ShellDialect.FISH:
            self._write_line()
        else:
            self._write("; do")
            self._write_line()
        
        self.indent_level += 1
        for stmt in node.body:
            stmt.accept(self)
        self.indent_level -= 1
        
        self._write_indent()
        if self.config.dialect == ShellDialect.FISH:
            self._write("end")
        else:
            self._write("done")
        self._write_line()
    
    def _generate_until_loop(self, node: ShellLoop) -> None:
        """Generate until loop"""
        if self.config.dialect == ShellDialect.FISH:
            # Fish doesn't have until, convert to while with negation
            self._write_indent()
            self._write("while not ")
            self._write(self._format_condition(node.condition))
            self._write_line()
        else:
            self._write_indent()
            self._write("until ")
            self._write(self._format_condition(node.condition))
            self._write("; do")
            self._write_line()
        
        self.indent_level += 1
        for stmt in node.body:
            stmt.accept(self)
        self.indent_level -= 1
        
        self._write_indent()
        if self.config.dialect == ShellDialect.FISH:
            self._write("end")
        else:
            self._write("done")
        self._write_line()
    
    def _write_inline_pipeline(self, node: ShellPipeline) -> None:
        """Write pipeline on single line"""
        for i, cmd in enumerate(node.commands):
            if i > 0:
                self._write(" | ")
            
            # Write command inline
            if cmd.environment:
                for key, value in cmd.environment.items():
                    self._write(f'{key}="{self._escape_string(value)}" ')
            
            self._write(cmd.command)
            for arg in cmd.arguments:
                self._write(" ")
                self._write(self._format_argument(arg))
    
    def _write_multiline_pipeline(self, node: ShellPipeline) -> None:
        """Write pipeline across multiple lines"""
        for i, cmd in enumerate(node.commands):
            if i > 0:
                self._write(" \\")
                self._write_line()
                self._write_indent()
                self._write("  | ")
            
            # Write command
            if cmd.environment:
                for key, value in cmd.environment.items():
                    self._write(f'{key}="{self._escape_string(value)}" ')
            
            self._write(cmd.command)
            for arg in cmd.arguments:
                self._write(" ")
                self._write(self._format_argument(arg))
    
    def _format_condition(self, condition: str) -> str:
        """Format shell condition"""
        # Use appropriate test command for dialect
        test_cmd = self.shell_syntax[self.config.dialect]["test_command"]
        
        # Simple condition formatting
        if condition.startswith("[") or condition.startswith("test"):
            return condition
        
        # If it looks like a test expression, wrap it
        if any(op in condition for op in ["-eq", "-ne", "-lt", "-le", "-gt", "-ge", "-z", "-n", "-f", "-d"]):
            if test_cmd == "[[" and self.config.dialect in (ShellDialect.BASH, ShellDialect.ZSH):
                return f"[[ {condition} ]]"
            else:
                return f"[ {condition} ]"
        
        # Otherwise assume it's a command
        return condition
    
    def _format_argument(self, arg: str) -> str:
        """Format command argument with proper quoting"""
        # Check if argument needs quoting
        if (self._needs_quoting(arg) or 
            self.config.quote_variables or
            "$" in arg):
            return f'"{self._escape_string(arg)}"'
        else:
            return arg
    
    def _format_shell_value(self, value: str) -> str:
        """Format shell value"""
        if not value:
            return '""'
        
        # Handle variable expansions
        if value.startswith("$"):
            return value
        
        # Quote if necessary
        if self._needs_quoting(value):
            return f'"{self._escape_string(value)}"'
        
        return value
    
    def _needs_quoting(self, text: str) -> bool:
        """Check if text needs quoting"""
        # Characters that require quoting
        special_chars = {' ', '\t', '\n', '|', '&', ';', '(', ')', '<', '>', '`', '$', '\\', '"', "'", '?', '*', '[', ']', '{', '}'}
        return any(char in special_chars for char in text)
    
    def _needs_command_quoting(self, command: str) -> bool:
        """Check if command needs quoting"""
        return command in self.quote_requiring_commands or self._needs_quoting(command)
    
    def _escape_string(self, text: str) -> str:
        """Escape string for shell"""
        # Escape special characters
        return (text.replace('\\', '\\\\')
                    .replace('"', '\\"')
                    .replace('$', '\\$')
                    .replace('`', '\\`'))
    
    def _estimate_pipeline_length(self, pipeline: ShellPipeline) -> int:
        """Estimate length of pipeline if written inline"""
        length = 0
        
        for i, cmd in enumerate(pipeline.commands):
            if i > 0:
                length += 3  # " | "
            
            length += len(cmd.command)
            for arg in cmd.arguments:
                length += len(arg) + 1  # space + argument
        
        if pipeline.negated:
            length += 2  # "! "
        
        return length
    
    def _write(self, text: str) -> None:
        """Write text to output"""
        self.output.write(text)
        self.current_line_length += len(text)
    
    def _write_line(self, text: str = "") -> None:
        """Write line with newline"""
        if text:
            self._write(text)
        self.output.write('\n')
        self.current_line_length = 0
        self.needs_newline = False
    
    def _write_indent(self) -> None:
        """Write current indentation"""
        indent = ' ' * (self.indent_level * self.config.indent_size)
        self._write(indent)


class ShellFormatter:
    """Shell code formatter with various styles"""
    
    @staticmethod
    def format_shell(code: str, dialect: ShellDialect = ShellDialect.BASH,
                    style: ShellFormatStyle = ShellFormatStyle.STANDARD) -> str:
        """Format shell code with specified dialect and style"""
        from .shell_parser import parse_shell
        
        try:
            script = parse_shell(code)
            config = ShellGeneratorConfig(dialect=dialect, style=style)
            generator = ShellCodeGenerator(config)
            return generator.generate(script)
        except Exception as e:
            # If parsing fails, return original code
            return code
    
    @staticmethod
    def minify_shell(code: str) -> str:
        """Minify shell code for compact representation"""
        config = ShellGeneratorConfig(
            style=ShellFormatStyle.COMPACT,
            separate_functions=False,
            add_function_headers=False,
            preserve_comments=False
        )
        
        from .shell_parser import parse_shell
        
        try:
            script = parse_shell(code)
            generator = ShellCodeGenerator(config)
            return generator.generate(script)
        except Exception as e:
            return code
    
    @staticmethod
    def make_portable(code: str) -> str:
        """Make shell code POSIX portable"""
        config = ShellGeneratorConfig(
            dialect=ShellDialect.POSIX,
            style=ShellFormatStyle.STRICT,
            posix_compliant=True,
            avoid_bashisms=True,
            use_local_variables=False
        )
        
        from .shell_parser import parse_shell
        
        try:
            script = parse_shell(code)
            generator = ShellCodeGenerator(config)
            return generator.generate(script)
        except Exception as e:
            return code


def generate_shell(node: ShellNode, dialect: ShellDialect = ShellDialect.BASH,
                  style: ShellFormatStyle = ShellFormatStyle.STANDARD) -> str:
    """Generate shell code from AST node"""
    config = ShellGeneratorConfig(dialect=dialect, style=style)
    generator = ShellCodeGenerator(config)
    return generator.generate(node)


def format_shell_code(code: str, dialect: ShellDialect = ShellDialect.BASH,
                     style: ShellFormatStyle = ShellFormatStyle.STANDARD) -> str:
    """Format shell code string"""
    return ShellFormatter.format_shell(code, dialect, style) 