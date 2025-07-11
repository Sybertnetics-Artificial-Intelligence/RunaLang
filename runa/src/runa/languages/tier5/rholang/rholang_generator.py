#!/usr/bin/env python3
"""
Rholang Code Generator Implementation

This module provides comprehensive code generation for the Rholang language,
converting Rholang AST nodes into clean, properly formatted Rholang source code.

Key features:
- Clean, readable code generation for all Rholang constructs
- Support for process-oriented programming patterns
- Channel communication and synchronization formatting
- Pattern matching and destructuring syntax
- Smart contract generation for RChain blockchain
- Configurable code style options (indentation, spacing, etc.)
- Proper handling of process composition and parallel execution
- Formal verification friendly output
- Comments and documentation preservation
- Optimized for RChain deployment

The generator follows Rholang and RChain conventions for consistency.
"""

from typing import List, Optional, Union, Dict, Any, Set
from dataclasses import dataclass, field
from enum import Enum
import re

from .rholang_ast import *


class RholangQuoteStyle(Enum):
    """String quote style options."""
    DOUBLE = "double"  # Use double quotes (Rholang standard)
    SINGLE = "single"  # Use single quotes


class RholangIndentStyle(Enum):
    """Indentation style options."""
    SPACES_2 = "spaces_2"
    SPACES_4 = "spaces_4"  # Rholang standard


@dataclass
class RholangCodeStyle:
    """Configuration for Rholang code generation style."""
    
    # Indentation
    indent_style: RholangIndentStyle = RholangIndentStyle.SPACES_2
    indent_size: int = 2
    
    # String formatting
    quote_style: RholangQuoteStyle = RholangQuoteStyle.DOUBLE
    
    # Line formatting
    max_line_length: int = 100  # RChain community standard
    break_long_lines: bool = True
    
    # Spacing
    space_around_operators: bool = True
    space_after_comma: bool = True
    space_in_brackets: bool = False
    space_around_sends: bool = True  # x!(data) vs x! (data)
    
    # Process formatting
    align_parallel_processes: bool = True
    indent_nested_processes: bool = True
    separate_process_blocks: bool = True
    
    # Pattern formatting
    align_pattern_guards: bool = True
    indent_pattern_bodies: bool = True
    
    # Contract formatting
    align_contract_parameters: bool = True
    separate_contract_sections: bool = True
    
    # Comments
    preserve_comments: bool = True
    comment_prefix: str = "// "
    block_comment_style: str = "/* ... */"
    
    # Blockchain-specific
    format_deployment_annotations: bool = True
    align_channel_operations: bool = True
    
    def get_indent(self) -> str:
        """Get the indentation string."""
        if self.indent_style == RholangIndentStyle.SPACES_2:
            return "  "
        else:  # SPACES_4
            return "    "


class RholangCodeGenerator:
    """Generates Rholang source code from AST nodes."""
    
    def __init__(self, style: Optional[RholangCodeStyle] = None):
        self.style = style or RholangCodeStyle()
        self.indent_level = 0
        self.output_lines: List[str] = []
        self.current_line = ""
        self.last_was_blank = False
        self.in_parallel_context = False
        self.channel_names: Set[str] = set()
    
    def generate(self, node: RholangNode) -> str:
        """Generate Rholang code from an AST node."""
        self.indent_level = 0
        self.output_lines = []
        self.current_line = ""
        self.last_was_blank = False
        self.in_parallel_context = False
        self.channel_names.clear()
        
        self._generate_node(node)
        self._flush_line()
        
        # Join lines and clean up extra blank lines
        code = '\n'.join(self.output_lines)
        code = re.sub(r'\n\n\n+', '\n\n', code)  # Max 2 consecutive newlines
        
        return code.strip() + '\n' if code.strip() else ''
    
    def _generate_node(self, node: RholangNode) -> None:
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
    
    def _format_string(self, value: str) -> str:
        """Format a string literal with proper escaping and quotes."""
        quote = '"' if self.style.quote_style == RholangQuoteStyle.DOUBLE else "'"
        
        # Escape the string
        escaped = self._escape_string(value, quote)
        return f"{quote}{escaped}{quote}"
    
    def _escape_string(self, value: str, quote: str) -> str:
        """Escape string content for the given quote style."""
        escaped = value.replace('\\', '\\\\')
        escaped = escaped.replace('\n', '\\n')
        escaped = escaped.replace('\t', '\\t')
        escaped = escaped.replace('\r', '\\r')
        
        if quote == '"':
            escaped = escaped.replace('"', '\\"')
        elif quote == "'":
            escaped = escaped.replace("'", "\\'")
        
        return escaped
    
    def _format_operator(self, op: RholangOperator) -> str:
        """Format an operator with appropriate spacing."""
        op_str = op.value
        if self.style.space_around_operators and op in [
            RholangOperator.ADD, RholangOperator.SUB, RholangOperator.MUL,
            RholangOperator.DIV, RholangOperator.EQ, RholangOperator.NE,
            RholangOperator.LT, RholangOperator.LE, RholangOperator.GT,
            RholangOperator.GE, RholangOperator.AND, RholangOperator.OR
        ]:
            return f" {op_str} "
        return op_str
    
    def _join_with_comma(self, items: List[str], trailing_comma: bool = False) -> str:
        """Join items with comma and optional spacing."""
        if not items:
            return ""
        
        separator = ", " if self.style.space_after_comma else ","
        joined = separator.join(items)
        
        if trailing_comma and len(items) > 1:
            joined += separator.rstrip()
        
        return joined
    
    # Visitor methods
    
    def visit_module(self, node: RholangModule) -> None:
        """Generate module code."""
        # Generate imports first
        if node.imports:
            for import_stmt in node.imports:
                self._write_indent()
                self._writeln(f"import {import_stmt}")
            self._blank_line()
        
        # Generate main body processes
        for i, process in enumerate(node.body):
            if i > 0 and self.style.separate_process_blocks:
                self._blank_line()
            
            self._write_indent()
            self._generate_node(process)
            
            # Add separator for top-level processes
            if i < len(node.body) - 1:
                self._writeln(" |")
    
    def visit_literal(self, node: RholangLiteral) -> None:
        """Generate literal code."""
        if node.literal_type == "string":
            self._write(self._format_string(str(node.value)))
        elif node.literal_type == "int":
            self._write(str(node.value))
        elif node.literal_type == "bool":
            self._write("true" if node.value else "false")
        elif node.literal_type == "bytes":
            # Format as hex string
            if isinstance(node.value, bytes):
                hex_str = node.value.hex()
                self._write(f'"{hex_str}".hexToBytes()')
            else:
                self._write(str(node.value))
        elif node.literal_type == "uri":
            self._write(f"`{node.value}`")
        else:
            self._write(str(node.value))
    
    def visit_name(self, node: RholangName) -> None:
        """Generate name code."""
        if node.is_wildcard:
            self._write("_")
        else:
            self._write(node.name)
            self.channel_names.add(node.name)
    
    def visit_quote(self, node: RholangQuote) -> None:
        """Generate quote code."""
        self._write("@{")
        self._generate_node(node.process)
        self._write("}")
    
    def visit_list(self, node: RholangList) -> None:
        """Generate list code."""
        self._write("[")
        if self.style.space_in_brackets and node.elements:
            self._write(" ")
        
        element_strs = []
        for element in node.elements:
            element_code = ""
            old_current = self.current_line
            self.current_line = ""
            self._generate_node(element)
            element_code = self.current_line
            self.current_line = old_current
            element_strs.append(element_code)
        
        self._write(self._join_with_comma(element_strs))
        
        if self.style.space_in_brackets and node.elements:
            self._write(" ")
        self._write("]")
    
    def visit_tuple(self, node: RholangTuple) -> None:
        """Generate tuple code."""
        self._write("(")
        element_strs = []
        for element in node.elements:
            element_code = ""
            old_current = self.current_line
            self.current_line = ""
            self._generate_node(element)
            element_code = self.current_line
            self.current_line = old_current
            element_strs.append(element_code)
        
        self._write(self._join_with_comma(element_strs))
        self._write(")")
    
    def visit_set(self, node: RholangSet) -> None:
        """Generate set code."""
        self._write("Set(")
        element_strs = []
        for element in node.elements:
            element_code = ""
            old_current = self.current_line
            self.current_line = ""
            self._generate_node(element)
            element_code = self.current_line
            self.current_line = old_current
            element_strs.append(element_code)
        
        self._write(self._join_with_comma(element_strs))
        self._write(")")
    
    def visit_map(self, node: RholangMap) -> None:
        """Generate map code."""
        self._write("{")
        
        if node.pairs:
            if len(node.pairs) > 3:  # Multi-line for many pairs
                self._writeln()
                self._indent()
                
                for i, pair in enumerate(node.pairs):
                    self._write_indent()
                    self._generate_node(pair.key)
                    self._write(": ")
                    self._generate_node(pair.value)
                    
                    if i < len(node.pairs) - 1:
                        self._writeln(",")
                    else:
                        self._writeln()
                
                self._dedent()
                self._write_indent()
            else:  # Single line for few pairs
                pair_strs = []
                for pair in node.pairs:
                    key_code = ""
                    old_current = self.current_line
                    self.current_line = ""
                    self._generate_node(pair.key)
                    key_code = self.current_line
                    self.current_line = ""
                    self._generate_node(pair.value)
                    value_code = self.current_line
                    self.current_line = old_current
                    pair_strs.append(f"{key_code}: {value_code}")
                
                self._write(self._join_with_comma(pair_strs))
        
        self._write("}")
    
    def visit_binary_op(self, node: RholangBinaryOp) -> None:
        """Generate binary operation code."""
        self._generate_node(node.left)
        self._write(self._format_operator(node.operator))
        self._generate_node(node.right)
    
    def visit_unary_op(self, node: RholangUnaryOp) -> None:
        """Generate unary operation code."""
        op_str = node.operator.value
        if op_str.endswith('u'):  # Unary operators
            op_str = op_str[:-1]
        
        self._write(op_str)
        self._generate_node(node.operand)
    
    def visit_method_call(self, node: RholangMethodCall) -> None:
        """Generate method call code."""
        self._generate_node(node.target)
        self._write(f".{node.method}(")
        
        arg_strs = []
        for arg in node.arguments:
            arg_code = ""
            old_current = self.current_line
            self.current_line = ""
            self._generate_node(arg)
            arg_code = self.current_line
            self.current_line = old_current
            arg_strs.append(arg_code)
        
        self._write(self._join_with_comma(arg_strs))
        self._write(")")
    
    def visit_nil(self, node: RholangNil) -> None:
        """Generate Nil process code."""
        self._write("Nil")
    
    def visit_par(self, node: RholangPar) -> None:
        """Generate parallel composition code."""
        if not node.processes:
            self.visit_nil(RholangNil())
            return
        
        old_parallel = self.in_parallel_context
        self.in_parallel_context = True
        
        for i, process in enumerate(node.processes):
            if i > 0:
                if self.style.align_parallel_processes:
                    self._writeln(" |")
                    self._write_indent()
                else:
                    self._write(" | ")
            
            self._generate_node(process)
        
        self.in_parallel_context = old_parallel
    
    def visit_new(self, node: RholangNew) -> None:
        """Generate new name restriction code."""
        self._write("new ")
        self._write(", ".join(node.names))
        
        if node.uri_patterns:
            self._write(" in {")
            self._writeln()
            self._indent()
            self._write_indent()
            self._write("uriPatterns: [")
            pattern_strs = [f'"{pattern}"' for pattern in node.uri_patterns]
            self._write(self._join_with_comma(pattern_strs))
            self._writeln("]")
            self._dedent()
            self._write_indent()
            self._write("}")
        
        self._write(" in {")
        self._writeln()
        self._indent()
        self._write_indent()
        self._generate_node(node.process)
        self._writeln()
        self._dedent()
        self._write_indent()
        self._write("}")
    
    def visit_send(self, node: RholangSend) -> None:
        """Generate send operation code."""
        self._generate_node(node.channel)
        
        if node.persistent:
            self._write("!!")
        elif node.peek:
            self._write("!?")
        else:
            self._write("!")
        
        if self.style.space_around_sends:
            self._write(" ")
        
        self._write("(")
        
        data_strs = []
        for data in node.data:
            data_code = ""
            old_current = self.current_line
            self.current_line = ""
            self._generate_node(data)
            data_code = self.current_line
            self.current_line = old_current
            data_strs.append(data_code)
        
        self._write(self._join_with_comma(data_strs))
        self._write(")")
    
    def visit_receive(self, node: RholangReceive) -> None:
        """Generate receive operation code."""
        self._write("for (")
        
        # Generate receive patterns
        pattern_strs = []
        for recv_pattern in node.receives:
            pattern_code = ""
            old_current = self.current_line
            self.current_line = ""
            
            # Generate patterns for this channel
            pat_strs = []
            for pattern in recv_pattern.patterns:
                pat_code = ""
                old_pat = self.current_line
                self.current_line = ""
                self._generate_node(pattern)
                pat_code = self.current_line
                self.current_line = old_pat
                pat_strs.append(pat_code)
            
            # Generate channel and patterns
            channel_code = ""
            old_chan = self.current_line
            self.current_line = ""
            self._generate_node(recv_pattern.channel)
            channel_code = self.current_line
            self.current_line = old_chan
            
            pattern_code = f"{self._join_with_comma(pat_strs)} <- {channel_code}"
            
            # Add condition if present
            if recv_pattern.condition:
                cond_code = ""
                old_cond = self.current_line
                self.current_line = ""
                self._generate_node(recv_pattern.condition)
                cond_code = self.current_line
                self.current_line = old_cond
                pattern_code += f" if {cond_code}"
            
            self.current_line = old_current
            pattern_strs.append(pattern_code)
        
        self._write("; ".join(pattern_strs))
        self._write(") {")
        self._writeln()
        self._indent()
        self._write_indent()
        self._generate_node(node.continuation)
        self._writeln()
        self._dedent()
        self._write_indent()
        self._write("}")
    
    def visit_contract(self, node: RholangContract) -> None:
        """Generate contract definition code."""
        self._write("contract ")
        self._generate_node(node.name)
        self._write("(")
        
        # Generate parameters
        param_strs = []
        for param in node.parameters:
            param_code = ""
            old_current = self.current_line
            self.current_line = ""
            self._generate_node(param)
            param_code = self.current_line
            self.current_line = old_current
            param_strs.append(param_code)
        
        if self.style.align_contract_parameters and len(param_strs) > 3:
            self._writeln()
            self._indent()
            for i, param in enumerate(param_strs):
                self._write_indent()
                self._write(param)
                if i < len(param_strs) - 1:
                    self._writeln(",")
                else:
                    self._writeln()
            self._dedent()
            self._write_indent()
        else:
            self._write(self._join_with_comma(param_strs))
        
        self._write(") = {")
        self._writeln()
        self._indent()
        self._write_indent()
        self._generate_node(node.body)
        self._writeln()
        self._dedent()
        self._write_indent()
        self._write("}")
    
    def visit_match(self, node: RholangMatch) -> None:
        """Generate match expression code."""
        self._write("match ")
        self._generate_node(node.target)
        self._write(" {")
        self._writeln()
        self._indent()
        
        for case in node.cases:
            self._write_indent()
            self._generate_node(case.pattern)
            
            if case.condition:
                self._write(" if ")
                self._generate_node(case.condition)
            
            self._write(" => {")
            self._writeln()
            self._indent()
            self._write_indent()
            self._generate_node(case.body)
            self._writeln()
            self._dedent()
            self._write_indent()
            self._writeln("}")
        
        self._dedent()
        self._write_indent()
        self._write("}")
    
    def visit_if(self, node: RholangIf) -> None:
        """Generate if statement code."""
        self._write("if (")
        self._generate_node(node.condition)
        self._write(") {")
        self._writeln()
        self._indent()
        self._write_indent()
        self._generate_node(node.then_process)
        self._writeln()
        self._dedent()
        self._write_indent()
        self._write("}")
        
        if node.else_process:
            self._write(" else {")
            self._writeln()
            self._indent()
            self._write_indent()
            self._generate_node(node.else_process)
            self._writeln()
            self._dedent()
            self._write_indent()
            self._write("}")
    
    def visit_for(self, node: RholangFor) -> None:
        """Generate for comprehension code."""
        self._write("for (")
        
        # Generate variable patterns and generators
        gen_strs = []
        for i, (var, gen) in enumerate(zip(node.variables, node.generators)):
            var_code = ""
            old_current = self.current_line
            self.current_line = ""
            self._generate_node(var)
            var_code = self.current_line
            self.current_line = ""
            self._generate_node(gen)
            gen_code = self.current_line
            self.current_line = old_current
            gen_strs.append(f"{var_code} <- {gen_code}")
        
        self._write("; ".join(gen_strs))
        self._write(") {")
        self._writeln()
        self._indent()
        self._write_indent()
        self._generate_node(node.body)
        self._writeln()
        self._dedent()
        self._write_indent()
        self._write("}")
    
    def visit_bundle(self, node: RholangBundle) -> None:
        """Generate bundle construct code."""
        self._write(f"bundle{{{node.bundle_type}}} {{")
        self._writeln()
        self._indent()
        self._write_indent()
        self._generate_node(node.process)
        self._writeln()
        self._dedent()
        self._write_indent()
        self._write("}")
    
    def visit_pattern(self, node: RholangPattern) -> None:
        """Generate pattern code."""
        if isinstance(node, RholangVarPattern):
            self._write(node.name)
        elif isinstance(node, RholangWildcardPattern):
            self._write("_")
        elif isinstance(node, RholangListPattern):
            self._write("[")
            pattern_strs = []
            for pattern in node.patterns:
                pat_code = ""
                old_current = self.current_line
                self.current_line = ""
                self._generate_node(pattern)
                pat_code = self.current_line
                self.current_line = old_current
                pattern_strs.append(pat_code)
            
            self._write(self._join_with_comma(pattern_strs))
            
            if node.remainder:
                if pattern_strs:
                    self._write(", ")
                self._write("...")
                self._generate_node(node.remainder)
            
            self._write("]")
        elif isinstance(node, RholangTuplePattern):
            self._write("(")
            pattern_strs = []
            for pattern in node.patterns:
                pat_code = ""
                old_current = self.current_line
                self.current_line = ""
                self._generate_node(pattern)
                pat_code = self.current_line
                self.current_line = old_current
                pattern_strs.append(pat_code)
            
            self._write(self._join_with_comma(pattern_strs))
            self._write(")")


def generate_rholang(node: RholangNode, style: Optional[RholangCodeStyle] = None) -> str:
    """
    Generate Rholang source code from an AST node.
    
    Args:
        node: The Rholang AST node to generate code for
        style: Optional code style configuration
        
    Returns:
        Generated Rholang source code as string
    """
    generator = RholangCodeGenerator(style)
    return generator.generate(node) 