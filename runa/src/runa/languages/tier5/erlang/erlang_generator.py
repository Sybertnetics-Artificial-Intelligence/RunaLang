#!/usr/bin/env python3
"""
Erlang Code Generator

Generates clean Erlang code from AST.
"""

from typing import List, Optional
from io import StringIO
from ...shared.base_toolchain import BaseGenerator
from .erlang_ast import *


class ErlangCodeGenerator(BaseGenerator):
    """Erlang code generator."""
    
    def __init__(self, indent_size: int = 4):
        super().__init__()
        self.indent_size = indent_size
        self.indent_level = 0
        self.output = StringIO()
    
    def generate(self, node: ErlangNode) -> str:
        """Generate Erlang code from AST."""
        self.output = StringIO()
        self.indent_level = 0
        self._generate_node(node)
        return self.output.getvalue()
    
    def _generate_node(self, node: ErlangNode):
        """Generate code for any Erlang node."""
        if isinstance(node, ErlangProgram):
            self._generate_program(node)
        elif isinstance(node, ErlangModule):
            self._generate_module(node)
        elif isinstance(node, ErlangFunction):
            self._generate_function(node)
        elif isinstance(node, ErlangAtom):
            self.output.write(node.value)
        elif isinstance(node, ErlangInteger):
            self.output.write(str(node.value))
        elif isinstance(node, ErlangFloat):
            self.output.write(str(node.value))
        elif isinstance(node, ErlangString):
            self.output.write(f'"{node.value}"')
        elif isinstance(node, ErlangBoolean):
            self.output.write("true" if node.value else "false")
        elif isinstance(node, ErlangVariable):
            self.output.write(node.name)
        elif isinstance(node, ErlangList):
            self._generate_list(node)
        elif isinstance(node, ErlangTuple):
            self._generate_tuple(node)
        elif isinstance(node, ErlangBinaryOp):
            self._generate_binary_op(node)
        elif isinstance(node, ErlangFunctionCall):
            self._generate_function_call(node)
        elif isinstance(node, ErlangMatch):
            self._generate_match(node)
        elif isinstance(node, ErlangExport):
            self._generate_export(node)
        else:
            self.output.write("unknown")
    
    def _generate_program(self, node: ErlangProgram):
        """Generate Erlang program."""
        self._generate_node(node.module)
    
    def _generate_module(self, node: ErlangModule):
        """Generate module."""
        self.output.write(f"-module({node.name}).\n\n")
        
        for attr in node.attributes:
            self._generate_node(attr)
            self.output.write("\n")
        
        self.output.write("\n")
        
        for func in node.functions:
            self._generate_node(func)
            self.output.write("\n\n")
    
    def _generate_function(self, node: ErlangFunction):
        """Generate function."""
        for i, clause in enumerate(node.clauses):
            if i > 0:
                self.output.write(";\n")
            
            self.output.write(f"{node.name}(")
            for j, pattern in enumerate(clause.patterns):
                if j > 0:
                    self.output.write(", ")
                self._generate_node(pattern)
            self.output.write(")")
            
            if clause.guards:
                self.output.write(" when ")
                # Generate guards
            
            self.output.write(" ->\n")
            self.indent_level += 1
            
            for k, expr in enumerate(clause.body):
                if k > 0:
                    self.output.write(",\n")
                self._write_indent()
                self._generate_node(expr)
            
            self.indent_level -= 1
        
        self.output.write(".")
    
    def _generate_export(self, node: ErlangExport):
        """Generate export."""
        self.output.write("-export([")
        for i, (name, arity) in enumerate(node.functions):
            if i > 0:
                self.output.write(", ")
            self.output.write(f"{name}/{arity}")
        self.output.write("]).")
    
    def _generate_list(self, node: ErlangList):
        """Generate list."""
        self.output.write("[")
        for i, elem in enumerate(node.elements):
            if i > 0:
                self.output.write(", ")
            self._generate_node(elem)
        
        if node.tail:
            self.output.write(" | ")
            self._generate_node(node.tail)
        
        self.output.write("]")
    
    def _generate_tuple(self, node: ErlangTuple):
        """Generate tuple."""
        self.output.write("{")
        for i, elem in enumerate(node.elements):
            if i > 0:
                self.output.write(", ")
            self._generate_node(elem)
        self.output.write("}")
    
    def _generate_binary_op(self, node: ErlangBinaryOp):
        """Generate binary operation."""
        self._generate_node(node.left)
        self.output.write(f" {node.operator} ")
        self._generate_node(node.right)
    
    def _generate_function_call(self, node: ErlangFunctionCall):
        """Generate function call."""
        if node.module:
            self._generate_node(node.module)
            self.output.write(":")
        
        self._generate_node(node.function)
        self.output.write("(")
        
        for i, arg in enumerate(node.arguments):
            if i > 0:
                self.output.write(", ")
            self._generate_node(arg)
        
        self.output.write(")")
    
    def _generate_match(self, node: ErlangMatch):
        """Generate match expression."""
        self._generate_node(node.pattern)
        self.output.write(" = ")
        self._generate_node(node.expression)
    
    def _write_indent(self):
        """Write indentation."""
        self.output.write(" " * (self.indent_level * self.indent_size))


def generate_erlang_code(node: ErlangNode, indent_size: int = 4) -> str:
    """Generate Erlang code from AST."""
    generator = ErlangCodeGenerator(indent_size)
    return generator.generate(node) 