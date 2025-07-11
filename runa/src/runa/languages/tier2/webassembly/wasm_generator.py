#!/usr/bin/env python3
"""
WebAssembly Code Generator

Generates WebAssembly text format (WAT) from WebAssembly AST nodes with support 
for multiple formatting styles.

Author: Sybertnetics AI Solutions
License: MIT
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass
from enum import Enum, auto
import logging

from .wasm_ast import *


class WasmCodeStyle(Enum):
    """WebAssembly code formatting styles."""
    STANDARD = "standard"
    COMPACT = "compact"
    EXPANDED = "expanded"
    MINIMAL = "minimal"


@dataclass
class WasmFormattingOptions:
    """WebAssembly code formatting options."""
    indent_size: int = 2
    use_tabs: bool = False
    max_line_length: int = 120
    
    # WebAssembly-specific
    align_instructions: bool = True
    group_instructions: bool = True
    inline_simple_expressions: bool = True
    use_abbreviated_forms: bool = True
    include_comments: bool = True
    separate_sections: bool = True
    explicit_indices: bool = False


class WasmFormatter:
    """WebAssembly code formatter with style presets."""
    
    @staticmethod
    def get_style_options(style: WasmCodeStyle) -> WasmFormattingOptions:
        """Get formatting options for a specific style."""
        if style == WasmCodeStyle.STANDARD:
            return WasmFormattingOptions(
                indent_size=2,
                max_line_length=120,
                align_instructions=True,
                group_instructions=True,
                include_comments=True,
                separate_sections=True
            )
        elif style == WasmCodeStyle.COMPACT:
            return WasmFormattingOptions(
                indent_size=1,
                max_line_length=160,
                align_instructions=False,
                group_instructions=False,
                inline_simple_expressions=True,
                use_abbreviated_forms=True,
                include_comments=False,
                separate_sections=False
            )
        elif style == WasmCodeStyle.EXPANDED:
            return WasmFormattingOptions(
                indent_size=4,
                max_line_length=100,
                align_instructions=True,
                group_instructions=True,
                inline_simple_expressions=False,
                use_abbreviated_forms=False,
                include_comments=True,
                separate_sections=True,
                explicit_indices=True
            )
        elif style == WasmCodeStyle.MINIMAL:
            return WasmFormattingOptions(
                indent_size=0,
                max_line_length=200,
                align_instructions=False,
                group_instructions=False,
                inline_simple_expressions=True,
                use_abbreviated_forms=True,
                include_comments=False,
                separate_sections=False
            )
        else:
            return WasmFormattingOptions()


class WasmCodeGenerator(WasmVisitorExtended):
    """WebAssembly code generator that produces formatted WAT from AST."""
    
    def __init__(self, style: WasmCodeStyle = WasmCodeStyle.STANDARD):
        self.style = style
        self.options = WasmFormatter.get_style_options(style)
        self.logger = logging.getLogger(__name__)
        
        # Output state
        self.output = []
        self.indent_level = 0
        self.current_line_length = 0
        self.needs_indent = True
        
        # Context state
        self.function_names = {}
        self.type_names = {}
        self.global_names = {}
        self.current_function_locals = []
    
    def generate(self, node: WasmNode) -> str:
        """Generate WebAssembly text format from an AST node."""
        self.output = []
        self.indent_level = 0
        self.current_line_length = 0
        self.needs_indent = True
        
        try:
            node.accept(self)
            result = "".join(self.output)
            return self._post_process(result)
        except Exception as e:
            self.logger.error(f"WebAssembly code generation failed: {e}")
            raise RuntimeError(f"Failed to generate WebAssembly code: {e}")
    
    def _post_process(self, code: str) -> str:
        """Post-process generated code."""
        lines = code.split('\n')
        processed_lines = []
        
        for line in lines:
            # Remove extra whitespace
            line = line.rstrip()
            if line or not processed_lines or processed_lines[-1]:
                processed_lines.append(line)
        
        result = '\n'.join(processed_lines)
        
        if result and not result.endswith('\n'):
            result += '\n'
        
        return result
    
    def _write(self, text: str):
        """Write text to output."""
        if self.needs_indent and text.strip():
            self._write_indent()
            self.needs_indent = False
        
        self.output.append(text)
        self.current_line_length += len(text)
    
    def _write_line(self, text: str = ""):
        """Write a line of text."""
        if text:
            self._write(text)
        self.output.append('\n')
        self.current_line_length = 0
        self.needs_indent = True
    
    def _write_indent(self):
        """Write current indentation."""
        if self.options.use_tabs:
            indent = '\t' * self.indent_level
        else:
            indent = ' ' * (self.indent_level * self.options.indent_size)
        
        self.output.append(indent)
        self.current_line_length += len(indent)
    
    def _increase_indent(self):
        """Increase indentation level."""
        self.indent_level += 1
    
    def _decrease_indent(self):
        """Decrease indentation level."""
        self.indent_level = max(0, self.indent_level - 1)
    
    def _write_space(self):
        """Write a space if needed."""
        if self.output and not self.output[-1].endswith(' '):
            self._write(' ')
    
    def _write_s_expr_open(self, name: str):
        """Write opening S-expression."""
        self._write(f'({name}')
    
    def _write_s_expr_close(self):
        """Write closing S-expression."""
        self._write(')')
    
    def _write_comment(self, text: str):
        """Write comment."""
        if self.options.include_comments:
            self._write(f';; {text}')
            self._write_line()
    
    def _write_separated_list(self, items: List[Any], separator: str = " ", generate_func=None):
        """Write a separated list."""
        if not items:
            return
        
        if generate_func is None:
            generate_func = lambda item: item.accept(self)
        
        for i, item in enumerate(items):
            if i > 0:
                self._write(separator)
            generate_func(item)
    
    # Visitor methods
    def visit_wasm_module(self, node: WasmModule):
        """Visit WebAssembly module."""
        self._write_s_expr_open('module')
        self._write_line()
        self._increase_indent()
        
        if self.options.separate_sections:
            sections = [
                ("types", node.types),
                ("imports", node.imports),
                ("functions", node.functions),
                ("tables", node.tables),
                ("memories", node.memories),
                ("globals", node.globals),
                ("exports", node.exports),
                ("elements", node.elements),
                ("data", node.data)
            ]
            
            for section_name, items in sections:
                if items:
                    if self.options.include_comments:
                        self._write_comment(f"{section_name.title()} section")
                    
                    for item in items:
                        item.accept(self)
                        self._write_line()
                    
                    if self.options.separate_sections:
                        self._write_line()
        else:
            # Write all items in order
            all_items = (node.types + node.imports + node.functions + 
                        node.tables + node.memories + node.globals + 
                        node.exports + node.elements + node.data)
            
            for item in all_items:
                item.accept(self)
                self._write_line()
        
        # Handle start function
        if node.start is not None:
            self._write_s_expr_open('start')
            self._write_space()
            self._write(str(node.start))
            self._write_s_expr_close()
            self._write_line()
        
        self._decrease_indent()
        self._write_s_expr_close()
    
    def visit_wasm_type(self, node: WasmType):
        """Visit WebAssembly type."""
        self._write_s_expr_open('type')
        self._write_space()
        self._write_s_expr_open('func')
        
        # Parameters
        if node.parameters:
            for param_type in node.parameters:
                self._write_space()
                self._write_s_expr_open('param')
                self._write_space()
                self._write(param_type.value)
                self._write_s_expr_close()
        
        # Results
        if node.results:
            for result_type in node.results:
                self._write_space()
                self._write_s_expr_open('result')
                self._write_space()
                self._write(result_type.value)
                self._write_s_expr_close()
        
        self._write_s_expr_close()
        self._write_s_expr_close()
    
    def visit_wasm_import(self, node: WasmImport):
        """Visit WebAssembly import."""
        self._write_s_expr_open('import')
        self._write_space()
        self._write(f'"{node.module}"')
        self._write_space()
        self._write(f'"{node.name}"')
        self._write_space()
        
        self._write_s_expr_open(node.kind)
        if node.type_index is not None:
            self._write_space()
            self._write(str(node.type_index))
        # TODO: Handle other type info
        self._write_s_expr_close()
        
        self._write_s_expr_close()
    
    def visit_wasm_export(self, node: WasmExport):
        """Visit WebAssembly export."""
        self._write_s_expr_open('export')
        self._write_space()
        self._write(f'"{node.name}"')
        self._write_space()
        
        self._write_s_expr_open(node.kind)
        self._write_space()
        self._write(str(node.index))
        self._write_s_expr_close()
        
        self._write_s_expr_close()
    
    def visit_wasm_function(self, node: WasmFunction):
        """Visit WebAssembly function."""
        self._write_s_expr_open('func')
        
        if node.name:
            self._write_space()
            self._write(f'${node.name}')
        
        # Type reference
        if self.options.explicit_indices:
            self._write_space()
            self._write_s_expr_open('type')
            self._write_space()
            self._write(str(node.type_index))
            self._write_s_expr_close()
        
        # Locals
        if node.locals:
            for local_type in node.locals:
                self._write_space()
                self._write_s_expr_open('local')
                self._write_space()
                self._write(local_type.value)
                self._write_s_expr_close()
        
        # Body
        if node.body:
            if self.options.group_instructions:
                self._write_line()
                self._increase_indent()
                
                for instruction in node.body:
                    instruction.accept(self)
                    self._write_line()
                
                self._decrease_indent()
            else:
                for instruction in node.body:
                    self._write_space()
                    instruction.accept(self)
        
        self._write_s_expr_close()
    
    def visit_wasm_table(self, node: WasmTable):
        """Visit WebAssembly table."""
        self._write_s_expr_open('table')
        self._write_space()
        
        # Limits
        node.limits.accept(self)
        
        self._write_space()
        self._write(node.element_type.value)
        
        self._write_s_expr_close()
    
    def visit_wasm_memory(self, node: WasmMemory):
        """Visit WebAssembly memory."""
        self._write_s_expr_open('memory')
        self._write_space()
        
        # Limits
        node.limits.accept(self)
        
        self._write_s_expr_close()
    
    def visit_wasm_global(self, node: WasmGlobal):
        """Visit WebAssembly global."""
        self._write_s_expr_open('global')
        self._write_space()
        
        # Mutability and type
        if node.mutability == WasmMutability.VAR:
            self._write_s_expr_open('mut')
            self._write_space()
            self._write(node.value_type.value)
            self._write_s_expr_close()
        else:
            self._write(node.value_type.value)
        
        # Initialization
        if node.init:
            for instruction in node.init:
                self._write_space()
                instruction.accept(self)
        
        self._write_s_expr_close()
    
    def visit_wasm_data(self, node: WasmData):
        """Visit WebAssembly data."""
        self._write_s_expr_open('data')
        self._write_space()
        
        # Memory index
        self._write(str(node.memory_index))
        
        # Offset
        if node.offset:
            for instruction in node.offset:
                self._write_space()
                instruction.accept(self)
        
        # Data
        if node.data:
            self._write_space()
            # Convert bytes to string representation
            data_str = node.data.decode('utf-8', errors='replace')
            self._write(f'"{data_str}"')
        
        self._write_s_expr_close()
    
    def visit_wasm_element(self, node: WasmElement):
        """Visit WebAssembly element."""
        self._write_s_expr_open('elem')
        self._write_space()
        
        # Table index
        self._write(str(node.table_index))
        
        # Offset
        if node.offset:
            for instruction in node.offset:
                self._write_space()
                instruction.accept(self)
        
        # Init
        if node.init:
            for func_index in node.init:
                self._write_space()
                self._write(str(func_index))
        
        self._write_s_expr_close()
    
    def visit_wasm_instruction(self, node: WasmInstruction):
        """Visit WebAssembly instruction."""
        if self.options.inline_simple_expressions and not node.args:
            self._write(node.opcode.value)
        else:
            self._write_s_expr_open(node.opcode.value)
            
            for arg in node.args:
                self._write_space()
                if isinstance(arg, (int, float)):
                    self._write(str(arg))
                else:
                    self._write(str(arg))
            
            self._write_s_expr_close()
    
    def visit_wasm_limits(self, node: WasmLimits):
        """Visit WebAssembly limits."""
        self._write(str(node.min))
        if node.max is not None:
            self._write_space()
            self._write(str(node.max))
    
    def visit_wasm_custom_section(self, node: WasmCustomSection):
        """Visit WebAssembly custom section."""
        self._write_s_expr_open('custom')
        self._write_space()
        self._write(f'"{node.name}"')
        self._write_space()
        # Data representation simplified
        self._write(f'"{node.data.hex()}"')
        self._write_s_expr_close()
    
    def visit_wasm_block(self, node: WasmBlock):
        """Visit WebAssembly block."""
        self._write_s_expr_open('block')
        
        if node.label:
            self._write_space()
            self._write(f'${node.label}')
        
        if node.result_type:
            self._write_space()
            self._write_s_expr_open('result')
            self._write_space()
            self._write(node.result_type.value)
            self._write_s_expr_close()
        
        if node.instructions:
            self._write_line()
            self._increase_indent()
            
            for instruction in node.instructions:
                instruction.accept(self)
                self._write_line()
            
            self._decrease_indent()
        
        self._write_s_expr_close()
    
    def visit_wasm_loop(self, node: WasmLoop):
        """Visit WebAssembly loop."""
        self._write_s_expr_open('loop')
        
        if node.label:
            self._write_space()
            self._write(f'${node.label}')
        
        if node.result_type:
            self._write_space()
            self._write_s_expr_open('result')
            self._write_space()
            self._write(node.result_type.value)
            self._write_s_expr_close()
        
        if node.instructions:
            self._write_line()
            self._increase_indent()
            
            for instruction in node.instructions:
                instruction.accept(self)
                self._write_line()
            
            self._decrease_indent()
        
        self._write_s_expr_close()
    
    def visit_wasm_if(self, node: WasmIf):
        """Visit WebAssembly if."""
        self._write_s_expr_open('if')
        
        if node.label:
            self._write_space()
            self._write(f'${node.label}')
        
        if node.result_type:
            self._write_space()
            self._write_s_expr_open('result')
            self._write_space()
            self._write(node.result_type.value)
            self._write_s_expr_close()
        
        # Then block
        if node.then_instructions:
            self._write_line()
            self._increase_indent()
            self._write_s_expr_open('then')
            self._write_line()
            self._increase_indent()
            
            for instruction in node.then_instructions:
                instruction.accept(self)
                self._write_line()
            
            self._decrease_indent()
            self._write_s_expr_close()
            self._write_line()
            self._decrease_indent()
        
        # Else block
        if node.else_instructions:
            self._increase_indent()
            self._write_s_expr_open('else')
            self._write_line()
            self._increase_indent()
            
            for instruction in node.else_instructions:
                instruction.accept(self)
                self._write_line()
            
            self._decrease_indent()
            self._write_s_expr_close()
            self._write_line()
            self._decrease_indent()
        
        self._write_s_expr_close()


# Convenience functions
def generate_wasm_code(ast: WasmModule, 
                      style: WasmCodeStyle = WasmCodeStyle.STANDARD) -> str:
    """Generate WebAssembly text format from AST with specified style."""
    generator = WasmCodeGenerator(style)
    return generator.generate(ast)


def format_wasm_code(code: str, 
                    style: WasmCodeStyle = WasmCodeStyle.STANDARD) -> str:
    """Format existing WebAssembly code with specified style."""
    # This would require parsing and re-generating
    # For now, return the original code
    return code