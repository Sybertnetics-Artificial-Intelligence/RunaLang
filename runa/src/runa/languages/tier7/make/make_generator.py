#!/usr/bin/env python3
"""
Make Generator - Clean code generation for Make (GNU Make/POSIX Make)

Features:
- Clean Makefile generation with proper formatting
- Multiple style options (GNU Make, POSIX, modern)
- Proper indentation and whitespace handling
- Comment preservation and formatting
- Variable and rule organization
- Dependency ordering and optimization
- Cross-platform compatibility
"""

from typing import List, Dict, Any, Optional, TextIO
from dataclasses import dataclass
from io import StringIO
import re

from .make_ast import *

@dataclass
class MakeCodeStyle:
    """Make code style configuration"""
    # Indentation
    use_tabs: bool = True              # Use tabs vs spaces for commands
    indent_size: int = 4               # Spaces for continuation lines
    
    # Line formatting
    max_line_length: int = 80          # Maximum line length
    break_long_lines: bool = True      # Break long dependency lists
    align_assignments: bool = False    # Align variable assignments
    
    # Spacing
    space_around_equals: bool = True   # CC = gcc vs CC=gcc
    space_after_colon: bool = True     # target: deps vs target:deps
    blank_lines_between_rules: int = 1 # Blank lines between rules
    
    # Organization
    sort_variables: bool = False       # Sort variable definitions
    group_by_type: bool = True         # Group variables, rules, etc.
    include_comments: bool = True      # Include generated comments
    
    # Compatibility
    target_make: str = "gnu"           # gnu, posix, bsd
    escape_special_chars: bool = True  # Escape special characters
    
    # Modern features
    use_automatic_vars: bool = True    # Use $@, $<, etc.
    use_pattern_rules: bool = True     # Use pattern rules over suffix rules
    use_phony_targets: bool = True     # Add .PHONY declarations

class MakeFormatter:
    """Formatter for Make code with style options"""
    
    def __init__(self, style: MakeCodeStyle = None):
        self.style = style or MakeCodeStyle()
        
    def format_identifier(self, name: str) -> str:
        """Format identifier according to style"""
        if self.style.escape_special_chars:
            # Escape special Make characters
            name = name.replace('$', '$$')
            name = name.replace('#', r'\#')
        return name
        
    def format_variable_assignment(self, var: MakeVariable) -> str:
        """Format variable assignment"""
        name = self.format_identifier(var.name)
        op = var.assignment_type
        value = self.format_expression(var.value)
        
        if self.style.space_around_equals:
            return f"{name} {op} {value}"
        else:
            return f"{name}{op}{value}"
            
    def format_expression(self, expr: MakeExpression) -> str:
        """Format Make expression"""
        if isinstance(expr, TextLiteral):
            return expr.value
        elif isinstance(expr, VariableReference):
            return expr.name
        elif isinstance(expr, AutomaticVariable):
            symbol = expr.symbol
            modifier = expr.modifier or ""
            return f"${symbol}{modifier}"
        elif isinstance(expr, MakeFunction):
            return self.format_function(expr)
        elif isinstance(expr, ConcatenatedText):
            parts = [self.format_expression(part) for part in expr.parts]
            return ''.join(parts)
        else:
            return str(expr)
            
    def format_function(self, func: MakeFunction) -> str:
        """Format function call"""
        args = [self.format_expression(arg) for arg in func.arguments]
        arg_str = ','.join(args)
        return f"$({func.name} {arg_str})"
        
    def format_rule_header(self, rule: MakeRule) -> str:
        """Format rule header (targets: dependencies)"""
        targets = ' '.join(rule.targets)
        colon = "::" if rule.is_double_colon else ":"
        
        # Format dependencies
        deps = []
        deps.extend(rule.dependencies)
        
        # Add order-only dependencies
        if rule.order_only_deps:
            deps.append("|")
            deps.extend(rule.order_only_deps)
            
        if self.style.space_after_colon:
            if deps:
                return f"{targets}{colon} {' '.join(deps)}"
            else:
                return f"{targets}{colon}"
        else:
            if deps:
                return f"{targets}{colon}{' '.join(deps)}"
            else:
                return f"{targets}{colon}"
                
    def format_command(self, cmd: MakeCommand) -> str:
        """Format command line"""
        line = cmd.command_line
        
        # Add command prefixes
        prefixes = ""
        if cmd.is_silent:
            prefixes += "@"
        if cmd.ignore_errors:
            prefixes += "-"
        if cmd.always_execute:
            prefixes += "+"
            
        # Use tab for indentation
        indent = "\t" if self.style.use_tabs else " " * self.style.indent_size
        
        return f"{indent}{prefixes}{line}"
        
    def format_comment(self, comment: MakeComment) -> str:
        """Format comment"""
        return f"# {comment.text}"
        
    def format_conditional(self, cond: MakeConditional) -> List[str]:
        """Format conditional block"""
        lines = []
        
        # Format condition
        condition_text = self.format_expression(cond.condition)
        lines.append(f"{cond.condition_type} {condition_text}")
        
        # Format then block
        for stmt in cond.then_statements:
            stmt_lines = self.format_statement(stmt)
            lines.extend(stmt_lines)
            
        # Format else block
        if cond.else_statements:
            lines.append("else")
            for stmt in cond.else_statements:
                stmt_lines = self.format_statement(stmt)
                lines.extend(stmt_lines)
                
        lines.append("endif")
        return lines
        
    def format_statement(self, stmt: MakeStatement) -> List[str]:
        """Format any Make statement"""
        if isinstance(stmt, MakeVariable):
            return [self.format_variable_assignment(stmt)]
        elif isinstance(stmt, MakeRule):
            return self.format_rule(stmt)
        elif isinstance(stmt, MakeComment):
            return [self.format_comment(stmt)]
        elif isinstance(stmt, MakeConditional):
            return self.format_conditional(stmt)
        elif isinstance(stmt, MakeInclude):
            return self.format_include(stmt)
        elif isinstance(stmt, VPathDirective):
            return self.format_vpath(stmt)
        elif isinstance(stmt, ExportDirective):
            return self.format_export(stmt)
        elif isinstance(stmt, SpecialTarget):
            return self.format_special_target(stmt)
        elif isinstance(stmt, UserDefinedFunction):
            return self.format_user_function(stmt)
        else:
            return [f"# Unknown statement: {type(stmt).__name__}"]
            
    def format_rule(self, rule: MakeRule) -> List[str]:
        """Format complete rule"""
        lines = []
        
        # Rule header
        header = self.format_rule_header(rule)
        
        # Break long lines if needed
        if self.style.break_long_lines and len(header) > self.style.max_line_length:
            header = self.break_long_line(header)
            
        lines.append(header)
        
        # Commands
        for cmd in rule.commands:
            lines.append(self.format_command(cmd))
            
        return lines
        
    def format_include(self, include: MakeInclude) -> List[str]:
        """Format include directive"""
        directive = "-include" if include.is_optional else "include"
        filenames = ' '.join(include.filenames)
        return [f"{directive} {filenames}"]
        
    def format_vpath(self, vpath: VPathDirective) -> List[str]:
        """Format VPATH directive"""
        if vpath.pattern:
            # vpath pattern directories
            dirs = ' '.join(vpath.directories)
            return [f"vpath {vpath.pattern} {dirs}"]
        else:
            # VPATH = directories
            dirs = ' '.join(vpath.directories)
            return [f"VPATH = {dirs}"]
            
    def format_export(self, export: ExportDirective) -> List[str]:
        """Format export directive"""
        directive = "unexport" if export.is_unexport else "export"
        if export.variables:
            vars_str = ' '.join(export.variables)
            return [f"{directive} {vars_str}"]
        else:
            return [directive]
            
    def format_special_target(self, target: SpecialTarget) -> List[str]:
        """Format special target"""
        if target.dependencies:
            deps = ' '.join(target.dependencies)
            return [f"{target.name}: {deps}"]
        else:
            return [f"{target.name}:"]
            
    def format_user_function(self, func: UserDefinedFunction) -> List[str]:
        """Format user-defined function"""
        lines = []
        lines.append(f"define {func.name}")
        
        for stmt in func.body:
            stmt_lines = self.format_statement(stmt)
            lines.extend(stmt_lines)
            
        lines.append("endef")
        return lines
        
    def break_long_line(self, line: str) -> str:
        """Break long line using backslash continuation"""
        if len(line) <= self.style.max_line_length:
            return line
            
        # Find good break points (after spaces)
        parts = []
        current = ""
        
        for char in line:
            current += char
            if char == ' ' and len(current) > self.style.max_line_length // 2:
                parts.append(current.rstrip())
                current = ""
                
        if current:
            parts.append(current)
            
        if len(parts) > 1:
            continuation = f" \\\n{' ' * self.style.indent_size}"
            return continuation.join(parts)
        else:
            return line

class MakeCodeGenerator:
    """Main code generator for Make"""
    
    def __init__(self, style: MakeCodeStyle = None):
        self.style = style or MakeCodeStyle()
        self.formatter = MakeFormatter(self.style)
        
    def generate(self, ast: MakeFile) -> str:
        """Generate Make code from AST"""
        output = StringIO()
        self.generate_to_stream(ast, output)
        return output.getvalue()
        
    def generate_to_stream(self, ast: MakeFile, stream: TextIO) -> None:
        """Generate Make code to stream"""
        # Add file header comment
        if self.style.include_comments:
            self.write_file_header(stream)
            
        # Organize statements by type if requested
        if self.style.group_by_type:
            self.generate_organized(ast, stream)
        else:
            self.generate_sequential(ast, stream)
            
    def generate_organized(self, ast: MakeFile, stream: TextIO) -> None:
        """Generate organized Makefile with grouped sections"""
        # Separate statements by type
        variables = []
        includes = []
        special_targets = []
        rules = []
        conditionals = []
        functions = []
        others = []
        
        for stmt in ast.statements:
            if isinstance(stmt, MakeVariable):
                variables.append(stmt)
            elif isinstance(stmt, MakeInclude):
                includes.append(stmt)
            elif isinstance(stmt, SpecialTarget):
                special_targets.append(stmt)
            elif isinstance(stmt, MakeRule):
                rules.append(stmt)
            elif isinstance(stmt, MakeConditional):
                conditionals.append(stmt)
            elif isinstance(stmt, UserDefinedFunction):
                functions.append(stmt)
            else:
                others.append(stmt)
                
        # Generate sections
        self.generate_section(stream, "Includes", includes)
        self.generate_section(stream, "Variables", variables)
        self.generate_section(stream, "Special Targets", special_targets)
        self.generate_section(stream, "Functions", functions)
        self.generate_section(stream, "Conditionals", conditionals)
        self.generate_section(stream, "Rules", rules)
        self.generate_section(stream, "Other", others)
        
    def generate_sequential(self, ast: MakeFile, stream: TextIO) -> None:
        """Generate Makefile in original order"""
        for i, stmt in enumerate(ast.statements):
            if i > 0:
                # Add blank lines between rules
                if (isinstance(stmt, MakeRule) and 
                    isinstance(ast.statements[i-1], MakeRule)):
                    for _ in range(self.style.blank_lines_between_rules):
                        stream.write("\n")
                        
            lines = self.formatter.format_statement(stmt)
            for line in lines:
                stream.write(line + "\n")
                
    def generate_section(self, stream: TextIO, title: str, statements: List[MakeStatement]) -> None:
        """Generate a section with title"""
        if not statements:
            return
            
        if self.style.include_comments:
            stream.write(f"# {title}\n")
            stream.write("#" + "=" * (len(title) + 1) + "\n\n")
            
        # Sort variables if requested
        if title == "Variables" and self.style.sort_variables:
            statements = sorted(statements, key=lambda v: v.name if hasattr(v, 'name') else '')
            
        for stmt in statements:
            lines = self.formatter.format_statement(stmt)
            for line in lines:
                stream.write(line + "\n")
                
        stream.write("\n")
        
    def write_file_header(self, stream: TextIO) -> None:
        """Write file header comment"""
        header = [
            "# Makefile",
            "# Generated by Runa Universal Translation System",
            "#",
            "# This file was automatically generated from Runa source code.",
            "# Manual modifications may be lost on regeneration.",
            ""
        ]
        
        for line in header:
            stream.write(line + "\n")
            
    def add_phony_targets(self, ast: MakeFile) -> MakeFile:
        """Add .PHONY declarations for phony targets"""
        if not self.style.use_phony_targets:
            return ast
            
        phony_targets = []
        
        # Find phony targets
        for stmt in ast.statements:
            if isinstance(stmt, MakeRule) and stmt.is_phony:
                phony_targets.extend(stmt.targets)
                
        # Add .PHONY declaration
        if phony_targets:
            phony_stmt = SpecialTarget(
                name=".PHONY",
                dependencies=phony_targets
            )
            
            # Insert after variables but before rules
            insert_pos = 0
            for i, stmt in enumerate(ast.statements):
                if isinstance(stmt, MakeRule):
                    insert_pos = i
                    break
            else:
                insert_pos = len(ast.statements)
                
            ast.statements.insert(insert_pos, phony_stmt)
            
        return ast
        
    def optimize_dependencies(self, ast: MakeFile) -> MakeFile:
        """Optimize dependency ordering"""
        # This could implement dependency sorting, duplicate removal, etc.
        # For now, just return as-is
        return ast

# Convenience functions

def generate_make(ast: MakeFile, style: MakeCodeStyle = None) -> str:
    """Generate Make code from AST"""
    generator = MakeCodeGenerator(style)
    return generator.generate(ast)

def generate_make_to_file(ast: MakeFile, filename: str, style: MakeCodeStyle = None) -> None:
    """Generate Make code to file"""
    generator = MakeCodeGenerator(style)
    with open(filename, 'w', encoding='utf-8') as f:
        generator.generate_to_stream(ast, f)

# Style presets

def gnu_make_style() -> MakeCodeStyle:
    """GNU Make style preset"""
    return MakeCodeStyle(
        use_tabs=True,
        max_line_length=80,
        space_around_equals=True,
        space_after_colon=True,
        target_make="gnu",
        use_automatic_vars=True,
        use_pattern_rules=True,
        use_phony_targets=True
    )

def posix_make_style() -> MakeCodeStyle:
    """POSIX Make style preset"""
    return MakeCodeStyle(
        use_tabs=True,
        max_line_length=72,
        space_around_equals=False,
        space_after_colon=True,
        target_make="posix",
        use_automatic_vars=True,
        use_pattern_rules=False,  # POSIX prefers suffix rules
        use_phony_targets=False
    )

def modern_make_style() -> MakeCodeStyle:
    """Modern Make style preset with clean formatting"""
    return MakeCodeStyle(
        use_tabs=True,
        max_line_length=100,
        space_around_equals=True,
        space_after_colon=True,
        blank_lines_between_rules=1,
        sort_variables=True,
        group_by_type=True,
        include_comments=True,
        target_make="gnu",
        use_automatic_vars=True,
        use_pattern_rules=True,
        use_phony_targets=True
    )

def compact_make_style() -> MakeCodeStyle:
    """Compact Make style for minimal files"""
    return MakeCodeStyle(
        use_tabs=True,
        max_line_length=120,
        space_around_equals=False,
        space_after_colon=False,
        blank_lines_between_rules=0,
        sort_variables=False,
        group_by_type=False,
        include_comments=False,
        break_long_lines=False
    )

# Export main components
__all__ = [
    'MakeCodeStyle', 'MakeFormatter', 'MakeCodeGenerator',
    'generate_make', 'generate_make_to_file',
    'gnu_make_style', 'posix_make_style', 'modern_make_style', 'compact_make_style'
] 