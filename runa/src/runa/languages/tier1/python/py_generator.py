#!/usr/bin/env python3
"""
Python Code Generator

Generates Python source code from Python AST nodes.
Uses the built-in ast module's unparse functionality when available,
with fallback to custom generation.
"""

import ast
import sys
from typing import List, Dict, Any, Optional
from io import StringIO

from .py_ast import *


class PyCodeGenerator:
    """Python code generator."""
    
    def __init__(self, indent_size: int = 4, use_type_hints: bool = True):
        self.indent_size = indent_size
        self.use_type_hints = use_type_hints
        self.current_indent = 0
        self.output = StringIO()
    
    def generate(self, node: PyNode) -> str:
        """Generate Python code from AST node."""
        self.output = StringIO()
        self.current_indent = 0
        
        self._visit_node(node)
        
        result = self.output.getvalue()
        self.output.close()
        return result
    
    def _visit_node(self, node: PyNode):
        """Visit a node and generate code."""
        if isinstance(node, PyModule):
            self._visit_module(node)
        elif isinstance(node, PyConstant):
            self._visit_constant(node)
        elif isinstance(node, PyName):
            self._visit_name(node)
        elif isinstance(node, PyBinOp):
            self._visit_binop(node)
        elif isinstance(node, PyUnaryOp):
            self._visit_unaryop(node)
        elif isinstance(node, PyCompare):
            self._visit_compare(node)
        elif isinstance(node, PyCall):
            self._visit_call(node)
        elif isinstance(node, PyAttribute):
            self._visit_attribute(node)
        elif isinstance(node, PySubscript):
            self._visit_subscript(node)
        elif isinstance(node, PyList):
            self._visit_list(node)
        elif isinstance(node, PyTuple):
            self._visit_tuple(node)
        elif isinstance(node, PyDict):
            self._visit_dict(node)
        elif isinstance(node, PySet):
            self._visit_set(node)
        elif isinstance(node, PyLambda):
            self._visit_lambda(node)
        elif isinstance(node, PyIfExp):
            self._visit_ifexp(node)
        elif isinstance(node, PyStarred):
            self._visit_starred(node)
        elif isinstance(node, PyYield):
            self._visit_yield(node)
        elif isinstance(node, PyYieldFrom):
            self._visit_yield_from(node)
        elif isinstance(node, PyAwait):
            self._visit_await(node)
        elif isinstance(node, PyExpressionStmt):
            self._visit_expr_stmt(node)
        elif isinstance(node, PyAssign):
            self._visit_assign(node)
        elif isinstance(node, PyAnnAssign):
            self._visit_ann_assign(node)
        elif isinstance(node, PyAugAssign):
            self._visit_aug_assign(node)
        elif isinstance(node, PyRaise):
            self._visit_raise(node)
        elif isinstance(node, PyAssert):
            self._visit_assert(node)
        elif isinstance(node, PyDelete):
            self._visit_delete(node)
        elif isinstance(node, PyPass):
            self._visit_pass(node)
        elif isinstance(node, PyBreak):
            self._visit_break(node)
        elif isinstance(node, PyContinue):
            self._visit_continue(node)
        elif isinstance(node, PyIf):
            self._visit_if(node)
        elif isinstance(node, PyWhile):
            self._visit_while(node)
        elif isinstance(node, PyFor):
            self._visit_for(node)
        elif isinstance(node, PyTry):
            self._visit_try(node)
        elif isinstance(node, PyWith):
            self._visit_with(node)
        elif isinstance(node, PyFunctionDef):
            self._visit_functiondef(node)
        elif isinstance(node, PyAsyncFunctionDef):
            self._visit_async_functiondef(node)
        elif isinstance(node, PyClassDef):
            self._visit_classdef(node)
        elif isinstance(node, PyReturn):
            self._visit_return(node)
        elif isinstance(node, PyGlobal):
            self._visit_global(node)
        elif isinstance(node, PyNonlocal):
            self._visit_nonlocal(node)
        elif isinstance(node, PyImport):
            self._visit_import(node)
        elif isinstance(node, PyImportFrom):
            self._visit_import_from(node)
        elif isinstance(node, PyExceptHandler):
            self._visit_excepthandler(node)
        elif isinstance(node, PyWithItem):
            self._visit_withitem(node)
        elif isinstance(node, PyArguments):
            self._visit_arguments(node)
        elif isinstance(node, PyArg):
            self._visit_arg(node)
        elif isinstance(node, PyKeyword):
            self._visit_keyword(node)
        elif isinstance(node, PyAlias):
            self._visit_alias(node)
        elif isinstance(node, PyComprehension):
            self._visit_comprehension(node)
        else:
            self._write(f"# Unknown node: {type(node)}")
    
    def _visit_module(self, node: PyModule):
        """Visit module node."""
        for i, stmt in enumerate(node.body):
            if i > 0:
                self._write_line()
            self._visit_node(stmt)
    
    def _visit_constant(self, node: PyConstant):
        """Visit constant node."""
        if node.value is None:
            self._write("None")
        elif isinstance(node.value, bool):
            self._write("True" if node.value else "False")
        elif isinstance(node.value, str):
            self._write(repr(node.value))
        else:
            self._write(str(node.value))
    
    def _visit_name(self, node: PyName):
        """Visit name node."""
        self._write(node.id)
    
    def _visit_binop(self, node: PyBinOp):
        """Visit binary operation node."""
        self._visit_node(node.left)
        self._write(f" {node.op.value} ")
        self._visit_node(node.right)
    
    def _visit_unaryop(self, node: PyUnaryOp):
        """Visit unary operation node."""
        self._write(node.op.value)
        if node.op == PyOperator.NOT:
            self._write(" ")
        self._visit_node(node.operand)
    
    def _visit_compare(self, node: PyCompare):
        """Visit compare node."""
        self._visit_node(node.left)
        for op, comparator in zip(node.ops, node.comparators):
            self._write(f" {op.value} ")
            self._visit_node(comparator)
    
    def _visit_call(self, node: PyCall):
        """Visit call node."""
        self._visit_node(node.func)
        self._write("(")
        
        for i, arg in enumerate(node.args):
            if i > 0:
                self._write(", ")
            self._visit_node(arg)
        
        if node.args and node.keywords:
            self._write(", ")
        
        for i, keyword in enumerate(node.keywords):
            if i > 0:
                self._write(", ")
            self._visit_node(keyword)
        
        self._write(")")
    
    def _visit_attribute(self, node: PyAttribute):
        """Visit attribute node."""
        self._visit_node(node.value)
        self._write(f".{node.attr}")
    
    def _visit_subscript(self, node: PySubscript):
        """Visit subscript node."""
        self._visit_node(node.value)
        self._write("[")
        self._visit_node(node.slice)
        self._write("]")
    
    def _visit_list(self, node: PyList):
        """Visit list node."""
        self._write("[")
        for i, elt in enumerate(node.elts):
            if i > 0:
                self._write(", ")
            self._visit_node(elt)
        self._write("]")
    
    def _visit_tuple(self, node: PyTuple):
        """Visit tuple node."""
        self._write("(")
        for i, elt in enumerate(node.elts):
            if i > 0:
                self._write(", ")
            self._visit_node(elt)
        if len(node.elts) == 1:
            self._write(",")
        self._write(")")
    
    def _visit_dict(self, node: PyDict):
        """Visit dict node."""
        self._write("{")
        for i, (key, value) in enumerate(zip(node.keys, node.values)):
            if i > 0:
                self._write(", ")
            if key is None:
                self._write("**")
                self._visit_node(value)
            else:
                self._visit_node(key)
                self._write(": ")
                self._visit_node(value)
        self._write("}")
    
    def _visit_set(self, node: PySet):
        """Visit set node."""
        if not node.elts:
            self._write("set()")
        else:
            self._write("{")
            for i, elt in enumerate(node.elts):
                if i > 0:
                    self._write(", ")
                self._visit_node(elt)
            self._write("}")
    
    def _visit_lambda(self, node: PyLambda):
        """Visit lambda node."""
        self._write("lambda ")
        self._visit_node(node.args)
        self._write(": ")
        self._visit_node(node.body)
    
    def _visit_ifexp(self, node: PyIfExp):
        """Visit if expression node."""
        self._visit_node(node.body)
        self._write(" if ")
        self._visit_node(node.test)
        self._write(" else ")
        self._visit_node(node.orelse)
    
    def _visit_starred(self, node: PyStarred):
        """Visit starred node."""
        self._write("*")
        self._visit_node(node.value)
    
    def _visit_yield(self, node: PyYield):
        """Visit yield node."""
        self._write("yield")
        if node.value:
            self._write(" ")
            self._visit_node(node.value)
    
    def _visit_yield_from(self, node: PyYieldFrom):
        """Visit yield from node."""
        self._write("yield from ")
        self._visit_node(node.value)
    
    def _visit_await(self, node: PyAwait):
        """Visit await node."""
        self._write("await ")
        self._visit_node(node.value)
    
    def _visit_expr_stmt(self, node: PyExpressionStmt):
        """Visit expression statement node."""
        self._write_indent()
        self._visit_node(node.value)
        self._write_line()
    
    def _visit_assign(self, node: PyAssign):
        """Visit assign node."""
        self._write_indent()
        for i, target in enumerate(node.targets):
            if i > 0:
                self._write(" = ")
            self._visit_node(target)
        self._write(" = ")
        self._visit_node(node.value)
        self._write_line()
    
    def _visit_ann_assign(self, node: PyAnnAssign):
        """Visit annotated assign node."""
        self._write_indent()
        self._visit_node(node.target)
        self._write(": ")
        self._visit_node(node.annotation)
        if node.value:
            self._write(" = ")
            self._visit_node(node.value)
        self._write_line()
    
    def _visit_aug_assign(self, node: PyAugAssign):
        """Visit augmented assign node."""
        self._write_indent()
        self._visit_node(node.target)
        self._write(f" {node.op.value}= ")
        self._visit_node(node.value)
        self._write_line()
    
    def _visit_raise(self, node: PyRaise):
        """Visit raise node."""
        self._write_indent()
        self._write("raise")
        if node.exc:
            self._write(" ")
            self._visit_node(node.exc)
        if node.cause:
            self._write(" from ")
            self._visit_node(node.cause)
        self._write_line()
    
    def _visit_assert(self, node: PyAssert):
        """Visit assert node."""
        self._write_indent()
        self._write("assert ")
        self._visit_node(node.test)
        if node.msg:
            self._write(", ")
            self._visit_node(node.msg)
        self._write_line()
    
    def _visit_delete(self, node: PyDelete):
        """Visit delete node."""
        self._write_indent()
        self._write("del ")
        for i, target in enumerate(node.targets):
            if i > 0:
                self._write(", ")
            self._visit_node(target)
        self._write_line()
    
    def _visit_pass(self, node: PyPass):
        """Visit pass node."""
        self._write_indent()
        self._write("pass")
        self._write_line()
    
    def _visit_break(self, node: PyBreak):
        """Visit break node."""
        self._write_indent()
        self._write("break")
        self._write_line()
    
    def _visit_continue(self, node: PyContinue):
        """Visit continue node."""
        self._write_indent()
        self._write("continue")
        self._write_line()
    
    def _visit_if(self, node: PyIf):
        """Visit if node."""
        self._write_indent()
        self._write("if ")
        self._visit_node(node.test)
        self._write(":")
        self._write_line()
        
        self._indent()
        for stmt in node.body:
            self._visit_node(stmt)
        self._dedent()
        
        if node.orelse:
            self._write_indent()
            if len(node.orelse) == 1 and isinstance(node.orelse[0], PyIf):
                self._write("elif ")
                self._visit_node(node.orelse[0].test)
                self._write(":")
                self._write_line()
                
                self._indent()
                for stmt in node.orelse[0].body:
                    self._visit_node(stmt)
                self._dedent()
                
                if node.orelse[0].orelse:
                    self._write_indent()
                    self._write("else:")
                    self._write_line()
                    
                    self._indent()
                    for stmt in node.orelse[0].orelse:
                        self._visit_node(stmt)
                    self._dedent()
            else:
                self._write("else:")
                self._write_line()
                
                self._indent()
                for stmt in node.orelse:
                    self._visit_node(stmt)
                self._dedent()
    
    def _visit_while(self, node: PyWhile):
        """Visit while node."""
        self._write_indent()
        self._write("while ")
        self._visit_node(node.test)
        self._write(":")
        self._write_line()
        
        self._indent()
        for stmt in node.body:
            self._visit_node(stmt)
        self._dedent()
        
        if node.orelse:
            self._write_indent()
            self._write("else:")
            self._write_line()
            
            self._indent()
            for stmt in node.orelse:
                self._visit_node(stmt)
            self._dedent()
    
    def _visit_for(self, node: PyFor):
        """Visit for node."""
        self._write_indent()
        self._write("for ")
        self._visit_node(node.target)
        self._write(" in ")
        self._visit_node(node.iter)
        self._write(":")
        self._write_line()
        
        self._indent()
        for stmt in node.body:
            self._visit_node(stmt)
        self._dedent()
        
        if node.orelse:
            self._write_indent()
            self._write("else:")
            self._write_line()
            
            self._indent()
            for stmt in node.orelse:
                self._visit_node(stmt)
            self._dedent()
    
    def _visit_try(self, node: PyTry):
        """Visit try node."""
        self._write_indent()
        self._write("try:")
        self._write_line()
        
        self._indent()
        for stmt in node.body:
            self._visit_node(stmt)
        self._dedent()
        
        for handler in node.handlers:
            self._visit_node(handler)
        
        if node.orelse:
            self._write_indent()
            self._write("else:")
            self._write_line()
            
            self._indent()
            for stmt in node.orelse:
                self._visit_node(stmt)
            self._dedent()
        
        if node.finalbody:
            self._write_indent()
            self._write("finally:")
            self._write_line()
            
            self._indent()
            for stmt in node.finalbody:
                self._visit_node(stmt)
            self._dedent()
    
    def _visit_with(self, node: PyWith):
        """Visit with node."""
        self._write_indent()
        self._write("with ")
        
        for i, item in enumerate(node.items):
            if i > 0:
                self._write(", ")
            self._visit_node(item)
        
        self._write(":")
        self._write_line()
        
        self._indent()
        for stmt in node.body:
            self._visit_node(stmt)
        self._dedent()
    
    def _visit_functiondef(self, node: PyFunctionDef):
        """Visit function definition node."""
        self._write_indent()
        self._write("def ")
        self._write(node.name)
        self._write("(")
        self._visit_node(node.args)
        self._write(")")
        
        if node.returns and self.use_type_hints:
            self._write(" -> ")
            self._visit_node(node.returns)
        
        self._write(":")
        self._write_line()
        
        self._indent()
        for stmt in node.body:
            self._visit_node(stmt)
        self._dedent()
    
    def _visit_async_functiondef(self, node: PyAsyncFunctionDef):
        """Visit async function definition node."""
        self._write_indent()
        self._write("async def ")
        self._write(node.name)
        self._write("(")
        self._visit_node(node.args)
        self._write(")")
        
        if node.returns and self.use_type_hints:
            self._write(" -> ")
            self._visit_node(node.returns)
        
        self._write(":")
        self._write_line()
        
        self._indent()
        for stmt in node.body:
            self._visit_node(stmt)
        self._dedent()
    
    def _visit_classdef(self, node: PyClassDef):
        """Visit class definition node."""
        self._write_indent()
        self._write("class ")
        self._write(node.name)
        
        if node.bases or node.keywords:
            self._write("(")
            
            for i, base in enumerate(node.bases):
                if i > 0:
                    self._write(", ")
                self._visit_node(base)
            
            if node.bases and node.keywords:
                self._write(", ")
            
            for i, keyword in enumerate(node.keywords):
                if i > 0:
                    self._write(", ")
                self._visit_node(keyword)
            
            self._write(")")
        
        self._write(":")
        self._write_line()
        
        self._indent()
        for stmt in node.body:
            self._visit_node(stmt)
        self._dedent()
    
    def _visit_return(self, node: PyReturn):
        """Visit return node."""
        self._write_indent()
        self._write("return")
        if node.value:
            self._write(" ")
            self._visit_node(node.value)
        self._write_line()
    
    def _visit_global(self, node: PyGlobal):
        """Visit global node."""
        self._write_indent()
        self._write("global ")
        self._write(", ".join(node.names))
        self._write_line()
    
    def _visit_nonlocal(self, node: PyNonlocal):
        """Visit nonlocal node."""
        self._write_indent()
        self._write("nonlocal ")
        self._write(", ".join(node.names))
        self._write_line()
    
    def _visit_import(self, node: PyImport):
        """Visit import node."""
        self._write_indent()
        self._write("import ")
        for i, alias in enumerate(node.names):
            if i > 0:
                self._write(", ")
            self._visit_node(alias)
        self._write_line()
    
    def _visit_import_from(self, node: PyImportFrom):
        """Visit import from node."""
        self._write_indent()
        self._write("from ")
        
        if node.level > 0:
            self._write("." * node.level)
        
        if node.module:
            self._write(node.module)
        
        self._write(" import ")
        
        for i, alias in enumerate(node.names):
            if i > 0:
                self._write(", ")
            self._visit_node(alias)
        
        self._write_line()
    
    def _visit_excepthandler(self, node: PyExceptHandler):
        """Visit exception handler node."""
        self._write_indent()
        self._write("except")
        
        if node.type:
            self._write(" ")
            self._visit_node(node.type)
        
        if node.name:
            self._write(f" as {node.name}")
        
        self._write(":")
        self._write_line()
        
        self._indent()
        for stmt in node.body:
            self._visit_node(stmt)
        self._dedent()
    
    def _visit_withitem(self, node: PyWithItem):
        """Visit with item node."""
        self._visit_node(node.context_expr)
        if node.optional_vars:
            self._write(" as ")
            self._visit_node(node.optional_vars)
    
    def _visit_arguments(self, node: PyArguments):
        """Visit arguments node."""
        all_args = []
        
        # Positional-only arguments
        for arg in node.posonlyargs:
            all_args.append(arg)
        
        if node.posonlyargs:
            all_args.append("/")
        
        # Regular arguments
        for i, arg in enumerate(node.args):
            if i < len(node.defaults):
                default_index = len(node.args) - len(node.defaults) + i
                if default_index >= 0:
                    all_args.append((arg, node.defaults[default_index]))
                else:
                    all_args.append(arg)
            else:
                all_args.append(arg)
        
        # Vararg
        if node.vararg:
            all_args.append(f"*{node.vararg}")
        
        # Keyword-only arguments
        for i, arg in enumerate(node.kwonlyargs):
            if i < len(node.kw_defaults) and node.kw_defaults[i]:
                all_args.append((arg, node.kw_defaults[i]))
            else:
                all_args.append(arg)
        
        # Kwarg
        if node.kwarg:
            all_args.append(f"**{node.kwarg}")
        
        for i, arg in enumerate(all_args):
            if i > 0:
                self._write(", ")
            
            if isinstance(arg, str):
                self._write(arg)
            elif isinstance(arg, tuple):
                self._visit_node(arg[0])
                self._write("=")
                self._visit_node(arg[1])
            else:
                self._visit_node(arg)
    
    def _visit_arg(self, node: PyArg):
        """Visit argument node."""
        self._write(node.arg)
        if node.annotation and self.use_type_hints:
            self._write(": ")
            self._visit_node(node.annotation)
    
    def _visit_keyword(self, node: PyKeyword):
        """Visit keyword node."""
        if node.arg:
            self._write(f"{node.arg}=")
        else:
            self._write("**")
        self._visit_node(node.value)
    
    def _visit_alias(self, node: PyAlias):
        """Visit alias node."""
        self._write(node.name)
        if node.asname:
            self._write(f" as {node.asname}")
    
    def _visit_comprehension(self, node: PyComprehension):
        """Visit comprehension node."""
        if node.is_async:
            self._write("async ")
        self._write("for ")
        self._visit_node(node.target)
        self._write(" in ")
        self._visit_node(node.iter)
        
        for if_clause in node.ifs:
            self._write(" if ")
            self._visit_node(if_clause)
    
    # Helper methods
    def _write(self, text: str):
        """Write text to output."""
        self.output.write(text)
    
    def _write_line(self):
        """Write a new line."""
        self.output.write('\n')
    
    def _write_indent(self):
        """Write current indentation."""
        self.output.write(' ' * (self.current_indent * self.indent_size))
    
    def _indent(self):
        """Increase indentation level."""
        self.current_indent += 1
    
    def _dedent(self):
        """Decrease indentation level."""
        self.current_indent = max(0, self.current_indent - 1)


def generate_python(node: PyNode, **options) -> str:
    """Generate Python code from AST node."""
    indent_size = options.get("indent_size", 4)
    use_type_hints = options.get("use_type_hints", True)
    
    generator = PyCodeGenerator(indent_size=indent_size, use_type_hints=use_type_hints)
    return generator.generate(node)