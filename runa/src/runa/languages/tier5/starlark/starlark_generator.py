#!/usr/bin/env python3
"""
Starlark Code Generator Implementation

This module provides comprehensive code generation for the Starlark language,
converting Starlark AST nodes into clean, properly formatted Starlark source code.

Key features:
- Clean, readable code generation with proper formatting
- Configurable code style options (indentation, line breaks, etc.)
- Support for all Starlark constructs including Bazel-specific features
- Proper handling of string escaping and numeric formatting
- Deterministic output for build system compatibility
- Comments and docstring preservation
- Optimization for generated code readability

The generator follows Starlark and Bazel style conventions for consistency.
"""

from typing import List, Optional, Union, Dict, Any
from dataclasses import dataclass, field
from enum import Enum
import re

from .starlark_ast import *


class StarlarkQuoteStyle(Enum):
    """String quote style options."""
    SINGLE = "single"  # Use single quotes
    DOUBLE = "double"  # Use double quotes
    AUTO = "auto"      # Choose based on content


class StarlarkIndentStyle(Enum):
    """Indentation style options."""
    SPACES_2 = "spaces_2"
    SPACES_4 = "spaces_4"
    TABS = "tabs"


@dataclass
class StarlarkCodeStyle:
    """Configuration for Starlark code generation style."""
    
    # Indentation
    indent_style: StarlarkIndentStyle = StarlarkIndentStyle.SPACES_4
    indent_size: int = 4
    
    # String formatting
    quote_style: StarlarkQuoteStyle = StarlarkQuoteStyle.DOUBLE
    prefer_triple_quotes: bool = True
    
    # Line formatting
    max_line_length: int = 88  # Following Black's default
    break_long_lines: bool = True
    
    # Spacing
    space_around_operators: bool = True
    space_after_comma: bool = True
    space_in_brackets: bool = False
    space_in_function_calls: bool = False
    
    # Blank lines
    blank_lines_around_functions: int = 2
    blank_lines_around_classes: int = 2
    blank_lines_in_functions: int = 1
    
    # Comments
    preserve_comments: bool = True
    comment_prefix: str = "# "
    
    # Bazel-specific
    sort_load_statements: bool = True
    group_similar_rules: bool = True
    
    def get_indent(self) -> str:
        """Get the indentation string."""
        if self.indent_style == StarlarkIndentStyle.TABS:
            return "\t"
        elif self.indent_style == StarlarkIndentStyle.SPACES_2:
            return "  "
        else:  # SPACES_4
            return "    "


class StarlarkCodeGenerator:
    """Generates Starlark source code from AST nodes."""
    
    def __init__(self, style: Optional[StarlarkCodeStyle] = None):
        self.style = style or StarlarkCodeStyle()
        self.indent_level = 0
        self.output_lines: List[str] = []
        self.current_line = ""
        self.last_was_blank = False
    
    def generate(self, node: StarlarkNode) -> str:
        """Generate Starlark code from an AST node."""
        self.indent_level = 0
        self.output_lines = []
        self.current_line = ""
        self.last_was_blank = False
        
        self._generate_node(node)
        self._flush_line()
        
        # Join lines and clean up extra blank lines
        code = '\n'.join(self.output_lines)
        code = re.sub(r'\n\n\n+', '\n\n', code)  # Max 2 consecutive newlines
        
        return code.strip() + '\n' if code.strip() else ''
    
    def _generate_node(self, node: StarlarkNode) -> None:
        """Generate code for a specific node type."""
        node.accept(self)
    
    def _write(self, text: str) -> None:
        """Write text to current line."""
        self.current_line += text
    
    def _writeln(self, text: str = "") -> None:
        """Write text and start a new line."""
        self.current_line += text
        self._flush_line()
    
    def _flush_line(self) -> None:
        """Flush current line to output."""
        line = self.current_line.rstrip()
        self.output_lines.append(line)
        self.current_line = ""
        self.last_was_blank = not line
    
    def _indent(self) -> None:
        """Increase indentation level."""
        self.indent_level += 1
    
    def _dedent(self) -> None:
        """Decrease indentation level."""
        self.indent_level = max(0, self.indent_level - 1)
    
    def _write_indent(self) -> None:
        """Write current indentation."""
        if self.current_line == "":
            self._write(self.style.get_indent() * self.indent_level)
    
    def _blank_line(self) -> None:
        """Add a blank line if not already at one."""
        if not self.last_was_blank:
            self._writeln()
    
    def _blank_lines(self, count: int) -> None:
        """Add specified number of blank lines."""
        for _ in range(count):
            if not self.last_was_blank:
                self._writeln()
    
    def _format_string(self, value: str) -> str:
        """Format a string literal with proper escaping and quotes."""
        # Choose quote style
        if self.style.quote_style == StarlarkQuoteStyle.AUTO:
            # Use double quotes if string contains single quotes, otherwise single
            quote = '"' if "'" in value and '"' not in value else "'"
        elif self.style.quote_style == StarlarkQuoteStyle.SINGLE:
            quote = "'"
        else:
            quote = '"'
        
        # Handle multiline strings
        if '\n' in value and self.style.prefer_triple_quotes:
            quote = '"""' if quote == '"' else "'''"
            return f"{quote}{value}{quote}"
        
        # Escape the string
        escaped = self._escape_string(value, quote)
        return f"{quote}{escaped}{quote}"
    
    def _escape_string(self, value: str, quote: str) -> str:
        """Escape string content for the given quote style."""
        # Basic escaping
        escaped = value.replace('\\', '\\\\')
        escaped = escaped.replace('\n', '\\n')
        escaped = escaped.replace('\t', '\\t')
        escaped = escaped.replace('\r', '\\r')
        
        # Quote-specific escaping
        if quote == '"':
            escaped = escaped.replace('"', '\\"')
        elif quote == "'":
            escaped = escaped.replace("'", "\\'")
        
        return escaped
    
    def _format_number(self, value: Union[int, float]) -> str:
        """Format a numeric literal."""
        if isinstance(value, float):
            if value.is_integer():
                return f"{int(value)}.0"
            else:
                return str(value)
        else:
            return str(value)
    
    def _join_with_comma(self, items: List[str], trailing_comma: bool = False) -> str:
        """Join items with commas and proper spacing."""
        if not items:
            return ""
        
        separator = ", " if self.style.space_after_comma else ","
        result = separator.join(items)
        
        if trailing_comma and len(items) > 0:
            result += ","
        
        return result
    
    # Visitor methods
    
    def visit_module(self, node: StarlarkModule) -> None:
        """Generate code for a module."""
        first = True
        
        # Module docstring
        if node.docstring:
            self._write_indent()
            self._writeln(self._format_string(node.docstring))
            self._blank_line()
            first = False
        
        # Separate load statements from other statements
        load_statements = []
        other_statements = []
        
        for stmt in node.body:
            if isinstance(stmt, StarlarkLoad):
                load_statements.append(stmt)
            else:
                other_statements.append(stmt)
        
        # Generate load statements first
        if load_statements:
            if not first:
                self._blank_line()
            
            if self.style.sort_load_statements:
                load_statements.sort(key=lambda x: x.module)
            
            for i, stmt in enumerate(load_statements):
                if i > 0:
                    self._writeln()
                self._generate_node(stmt)
            
            if other_statements:
                self._blank_lines(2)
        
        # Generate other statements
        prev_was_function = False
        prev_was_rule = False
        
        for i, stmt in enumerate(other_statements):
            is_function = isinstance(stmt, StarlarkFunctionDef)
            is_rule = isinstance(stmt, (StarlarkRule, StarlarkAspect, StarlarkProvider))
            
            # Add spacing between different types of constructs
            if i > 0:
                if (is_function and not prev_was_function) or (prev_was_function and not is_function):
                    self._blank_lines(self.style.blank_lines_around_functions)
                elif (is_rule and not prev_was_rule) or (prev_was_rule and not is_rule):
                    self._blank_lines(2)
                elif is_function or prev_was_function:
                    self._blank_lines(self.style.blank_lines_around_functions)
                else:
                    self._blank_line()
            
            self._generate_node(stmt)
            
            prev_was_function = is_function
            prev_was_rule = is_rule
    
    def visit_literal(self, node: StarlarkLiteral) -> None:
        """Generate code for a literal."""
        if node.literal_type == "string":
            self._write(self._format_string(node.value))
        elif node.literal_type in ["int", "float"]:
            self._write(self._format_number(node.value))
        elif node.literal_type == "bool":
            self._write("True" if node.value else "False")
        elif node.literal_type == "none":
            self._write("None")
        else:
            self._write(str(node.value))
    
    def visit_identifier(self, node: StarlarkIdentifier) -> None:
        """Generate code for an identifier."""
        self._write(node.name)
    
    def visit_binary_op(self, node: StarlarkBinaryOp) -> None:
        """Generate code for a binary operation."""
        self._generate_node(node.left)
        
        if self.style.space_around_operators:
            self._write(f" {node.operator.value} ")
        else:
            self._write(node.operator.value)
        
        self._generate_node(node.right)
    
    def visit_unary_op(self, node: StarlarkUnaryOp) -> None:
        """Generate code for a unary operation."""
        self._write(node.operator.value)
        
        if node.operator in [StarlarkOperator.NOT]:
            self._write(" ")
        
        self._generate_node(node.operand)
    
    def visit_comparison(self, node: StarlarkComparison) -> None:
        """Generate code for a comparison."""
        self._generate_node(node.left)
        
        for op, comp in zip(node.operators, node.comparators):
            if self.style.space_around_operators:
                self._write(f" {op.value} ")
            else:
                self._write(op.value)
            self._generate_node(comp)
    
    def visit_bool_op(self, node: StarlarkBoolOp) -> None:
        """Generate code for a boolean operation."""
        operator = f" {node.operator.value} "
        
        for i, value in enumerate(node.values):
            if i > 0:
                self._write(operator)
            self._generate_node(value)
    
    def visit_attribute(self, node: StarlarkAttribute) -> None:
        """Generate code for attribute access."""
        self._generate_node(node.value)
        self._write(f".{node.attr}")
    
    def visit_index(self, node: StarlarkIndex) -> None:
        """Generate code for index access."""
        self._generate_node(node.value)
        self._write("[")
        if self.style.space_in_brackets:
            self._write(" ")
        self._generate_node(node.index)
        if self.style.space_in_brackets:
            self._write(" ")
        self._write("]")
    
    def visit_slice(self, node: StarlarkSlice) -> None:
        """Generate code for slice access."""
        self._generate_node(node.value)
        self._write("[")
        if self.style.space_in_brackets:
            self._write(" ")
        
        if node.start:
            self._generate_node(node.start)
        self._write(":")
        
        if node.end:
            self._generate_node(node.end)
        
        if node.step:
            self._write(":")
            self._generate_node(node.step)
        
        if self.style.space_in_brackets:
            self._write(" ")
        self._write("]")
    
    def visit_list(self, node: StarlarkList) -> None:
        """Generate code for a list literal."""
        self._write("[")
        
        if self.style.space_in_brackets and node.elements:
            self._write(" ")
        
        if node.elements:
            if len(node.elements) == 1:
                self._generate_node(node.elements[0])
            else:
                for i, elem in enumerate(node.elements):
                    if i > 0:
                        self._write(", " if self.style.space_after_comma else ",")
                    self._generate_node(elem)
        
        if self.style.space_in_brackets and node.elements:
            self._write(" ")
        
        self._write("]")
    
    def visit_tuple(self, node: StarlarkTuple) -> None:
        """Generate code for a tuple literal."""
        self._write("(")
        
        if self.style.space_in_brackets and node.elements:
            self._write(" ")
        
        if node.elements:
            for i, elem in enumerate(node.elements):
                if i > 0:
                    self._write(", " if self.style.space_after_comma else ",")
                self._generate_node(elem)
            
            # Add trailing comma for single-element tuples
            if len(node.elements) == 1:
                self._write(",")
        
        if self.style.space_in_brackets and node.elements:
            self._write(" ")
        
        self._write(")")
    
    def visit_dict(self, node: StarlarkDict) -> None:
        """Generate code for a dictionary literal."""
        self._write("{")
        
        if node.keys:
            if len(node.keys) <= 2:
                # Inline short dictionaries
                if self.style.space_in_brackets:
                    self._write(" ")
                
                for i, (key, value) in enumerate(zip(node.keys, node.values)):
                    if i > 0:
                        self._write(", " if self.style.space_after_comma else ",")
                    
                    self._generate_node(key)
                    self._write(": " if self.style.space_around_operators else ":")
                    self._generate_node(value)
                
                if self.style.space_in_brackets:
                    self._write(" ")
            else:
                # Multi-line format for longer dictionaries
                self._writeln()
                self._indent()
                
                for i, (key, value) in enumerate(zip(node.keys, node.values)):
                    self._write_indent()
                    self._generate_node(key)
                    self._write(": " if self.style.space_around_operators else ":")
                    self._generate_node(value)
                    self._writeln(",")
                
                self._dedent()
                self._write_indent()
        
        self._write("}")
    
    def visit_call(self, node: StarlarkCall) -> None:
        """Generate code for a function call."""
        self._generate_node(node.func)
        self._write("(")
        
        if self.style.space_in_function_calls and (node.args or node.keywords):
            self._write(" ")
        
        # Positional arguments
        for i, arg in enumerate(node.args):
            if i > 0:
                self._write(", " if self.style.space_after_comma else ",")
            self._generate_node(arg)
        
        # Keyword arguments
        if node.keywords:
            if node.args:
                self._write(", " if self.style.space_after_comma else ",")
            
            for i, kw in enumerate(node.keywords):
                if i > 0:
                    self._write(", " if self.style.space_after_comma else ",")
                self._generate_node(kw)
        
        if self.style.space_in_function_calls and (node.args or node.keywords):
            self._write(" ")
        
        self._write(")")
    
    def visit_keyword(self, node: StarlarkKeyword) -> None:
        """Generate code for a keyword argument."""
        self._write(f"{node.arg} = ")
        self._generate_node(node.value)
    
    def visit_lambda(self, node: StarlarkLambda) -> None:
        """Generate code for a lambda expression."""
        self._write("lambda")
        
        if node.args:
            self._write(" ")
            for i, arg in enumerate(node.args):
                if i > 0:
                    self._write(", ")
                self._write(arg)
        
        self._write(": ")
        self._generate_node(node.body)
    
    def visit_conditional_expr(self, node: StarlarkConditionalExpr) -> None:
        """Generate code for a conditional expression."""
        self._generate_node(node.body)
        self._write(" if ")
        self._generate_node(node.test)
        self._write(" else ")
        self._generate_node(node.orelse)
    
    def visit_list_comp(self, node: StarlarkListComp) -> None:
        """Generate code for a list comprehension."""
        self._write("[")
        self._generate_node(node.element)
        self._write(f" for {node.target} in ")
        self._generate_node(node.iter)
        
        for if_clause in node.ifs:
            self._write(" if ")
            self._generate_node(if_clause)
        
        self._write("]")
    
    def visit_dict_comp(self, node: StarlarkDictComp) -> None:
        """Generate code for a dictionary comprehension."""
        self._write("{")
        self._generate_node(node.key)
        self._write(": ")
        self._generate_node(node.value)
        self._write(f" for {node.target} in ")
        self._generate_node(node.iter)
        
        for if_clause in node.ifs:
            self._write(" if ")
            self._generate_node(if_clause)
        
        self._write("}")
    
    def visit_assign(self, node: StarlarkAssign) -> None:
        """Generate code for an assignment statement."""
        self._write_indent()
        
        for i, target in enumerate(node.targets):
            if i > 0:
                self._write(" = ")
            self._generate_node(target)
        
        self._write(" = ")
        self._generate_node(node.value)
        self._writeln()
    
    def visit_aug_assign(self, node: StarlarkAugAssign) -> None:
        """Generate code for an augmented assignment."""
        self._write_indent()
        self._generate_node(node.target)
        self._write(f" {node.operator.value}= ")
        self._generate_node(node.value)
        self._writeln()
    
    def visit_function_def(self, node: StarlarkFunctionDef) -> None:
        """Generate code for a function definition."""
        self._write_indent()
        self._write(f"def {node.name}(")
        
        # Parameters
        for i, arg in enumerate(node.args):
            if i > 0:
                self._write(", ")
            
            self._write(arg)
            
            # Default values
            default_index = i - (len(node.args) - len(node.defaults))
            if default_index >= 0:
                self._write(" = ")
                self._generate_node(node.defaults[default_index])
        
        self._writeln("):")
        
        # Function body
        self._indent()
        
        if not node.body:
            self._write_indent()
            self._writeln("pass")
        else:
            for stmt in node.body:
                self._generate_node(stmt)
        
        self._dedent()
    
    def visit_return(self, node: StarlarkReturn) -> None:
        """Generate code for a return statement."""
        self._write_indent()
        self._write("return")
        
        if node.value:
            self._write(" ")
            self._generate_node(node.value)
        
        self._writeln()
    
    def visit_if(self, node: StarlarkIf) -> None:
        """Generate code for an if statement."""
        self._write_indent()
        self._write("if ")
        self._generate_node(node.test)
        self._writeln(":")
        
        # Then body
        self._indent()
        
        if not node.body:
            self._write_indent()
            self._writeln("pass")
        else:
            for stmt in node.body:
                self._generate_node(stmt)
        
        self._dedent()
        
        # Else body
        if node.orelse:
            # Check if else body is a single if statement (elif)
            if len(node.orelse) == 1 and isinstance(node.orelse[0], StarlarkIf):
                self._write_indent()
                self._write("el")
                self._generate_node(node.orelse[0])
            else:
                self._write_indent()
                self._writeln("else:")
                self._indent()
                
                for stmt in node.orelse:
                    self._generate_node(stmt)
                
                self._dedent()
    
    def visit_for(self, node: StarlarkFor) -> None:
        """Generate code for a for loop."""
        self._write_indent()
        self._write(f"for {node.target} in ")
        self._generate_node(node.iter)
        self._writeln(":")
        
        # Loop body
        self._indent()
        
        if not node.body:
            self._write_indent()
            self._writeln("pass")
        else:
            for stmt in node.body:
                self._generate_node(stmt)
        
        self._dedent()
    
    def visit_break(self, node: StarlarkBreak) -> None:
        """Generate code for a break statement."""
        self._write_indent()
        self._writeln("break")
    
    def visit_continue(self, node: StarlarkContinue) -> None:
        """Generate code for a continue statement."""
        self._write_indent()
        self._writeln("continue")
    
    def visit_pass(self, node: StarlarkPass) -> None:
        """Generate code for a pass statement."""
        self._write_indent()
        self._writeln("pass")
    
    def visit_load(self, node: StarlarkLoad) -> None:
        """Generate code for a load statement."""
        self._write_indent()
        self._write("load(")
        self._write(self._format_string(node.module))
        
        if node.symbols:
            self._write(", ")
            
            for i, symbol in enumerate(node.symbols):
                if i > 0:
                    self._write(", ")
                
                if symbol in node.aliases:
                    self._write(f"{self._format_string(symbol)} = {self._format_string(node.aliases[symbol])}")
                else:
                    self._write(self._format_string(symbol))
        
        self._writeln(")")
    
    def visit_rule(self, node: StarlarkRule) -> None:
        """Generate code for a rule definition."""
        self._write_indent()
        self._write(f"{node.name} = rule(")
        self._writeln()
        self._indent()
        
        # Implementation
        self._write_indent()
        self._write("implementation = ")
        self._generate_node(node.implementation)
        self._writeln(",")
        
        # Attributes
        if node.attrs:
            self._write_indent()
            self._writeln("attrs = {")
            self._indent()
            
            for name, value in node.attrs.items():
                self._write_indent()
                self._write(f"{self._format_string(name)}: ")
                self._generate_node(value)
                self._writeln(",")
            
            self._dedent()
            self._write_indent()
            self._writeln("},")
        
        # Documentation
        if node.doc:
            self._write_indent()
            self._write("doc = ")
            self._write(self._format_string(node.doc))
            self._writeln(",")
        
        self._dedent()
        self._write_indent()
        self._writeln(")")
    
    def visit_aspect(self, node: StarlarkAspect) -> None:
        """Generate code for an aspect definition."""
        self._write_indent()
        self._write(f"{node.name} = aspect(")
        self._writeln()
        self._indent()
        
        # Implementation
        self._write_indent()
        self._write("implementation = ")
        self._generate_node(node.implementation)
        self._writeln(",")
        
        # Attr aspects
        if node.attr_aspects:
            self._write_indent()
            self._write("attr_aspects = [")
            for i, attr in enumerate(node.attr_aspects):
                if i > 0:
                    self._write(", ")
                self._write(self._format_string(attr))
            self._writeln("],")
        
        # Attributes
        if node.attrs:
            self._write_indent()
            self._writeln("attrs = {")
            self._indent()
            
            for name, value in node.attrs.items():
                self._write_indent()
                self._write(f"{self._format_string(name)}: ")
                self._generate_node(value)
                self._writeln(",")
            
            self._dedent()
            self._write_indent()
            self._writeln("},")
        
        self._dedent()
        self._write_indent()
        self._writeln(")")
    
    def visit_provider(self, node: StarlarkProvider) -> None:
        """Generate code for a provider definition."""
        self._write_indent()
        self._write(f"{node.name} = provider(")
        
        if node.fields:
            self._writeln()
            self._indent()
            self._write_indent()
            self._write("fields = [")
            
            for i, field in enumerate(node.fields):
                if i > 0:
                    self._write(", ")
                self._write(self._format_string(field))
            
            self._writeln("],")
            
            if node.doc:
                self._write_indent()
                self._write("doc = ")
                self._write(self._format_string(node.doc))
                self._writeln(",")
            
            self._dedent()
            self._write_indent()
        elif node.doc:
            self._write("doc = ")
            self._write(self._format_string(node.doc))
        
        self._writeln(")")


def generate_starlark(node: StarlarkNode, style: Optional[StarlarkCodeStyle] = None) -> str:
    """Generate Starlark source code from an AST node."""
    generator = StarlarkCodeGenerator(style)
    return generator.generate(node)


__all__ = [
    "StarlarkQuoteStyle",
    "StarlarkIndentStyle", 
    "StarlarkCodeStyle",
    "StarlarkCodeGenerator",
    "generate_starlark"
] 