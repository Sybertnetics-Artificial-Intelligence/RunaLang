#!/usr/bin/env python3
"""
Python Parser

Python parser that leverages the built-in AST module to parse Python code
and converts it to our custom Python AST format.
"""

import ast
import sys
from typing import List, Optional, Dict, Any, Union

from .py_ast import *


class PythonASTConverter:
    """Converts Python's built-in AST to our custom AST format."""
    
    def __init__(self):
        self.node_map = {}
    
    def convert(self, node: ast.AST) -> PyNode:
        """Convert built-in AST node to our format."""
        if isinstance(node, ast.Module):
            return self._convert_module(node)
        elif isinstance(node, ast.Constant):
            return self._convert_constant(node)
        elif isinstance(node, ast.Name):
            return self._convert_name(node)
        elif isinstance(node, ast.BinOp):
            return self._convert_binop(node)
        elif isinstance(node, ast.UnaryOp):
            return self._convert_unaryop(node)
        elif isinstance(node, ast.Compare):
            return self._convert_compare(node)
        elif isinstance(node, ast.Call):
            return self._convert_call(node)
        elif isinstance(node, ast.Attribute):
            return self._convert_attribute(node)
        elif isinstance(node, ast.Subscript):
            return self._convert_subscript(node)
        elif isinstance(node, ast.List):
            return self._convert_list(node)
        elif isinstance(node, ast.Tuple):
            return self._convert_tuple(node)
        elif isinstance(node, ast.Set):
            return self._convert_set(node)
        elif isinstance(node, ast.Dict):
            return self._convert_dict(node)
        elif isinstance(node, ast.ListComp):
            return self._convert_listcomp(node)
        elif isinstance(node, ast.SetComp):
            return self._convert_setcomp(node)
        elif isinstance(node, ast.DictComp):
            return self._convert_dictcomp(node)
        elif isinstance(node, ast.GeneratorExp):
            return self._convert_generatorexp(node)
        elif isinstance(node, ast.Lambda):
            return self._convert_lambda(node)
        elif isinstance(node, ast.IfExp):
            return self._convert_ifexp(node)
        elif isinstance(node, ast.Starred):
            return self._convert_starred(node)
        elif isinstance(node, ast.Yield):
            return self._convert_yield(node)
        elif isinstance(node, ast.YieldFrom):
            return self._convert_yield_from(node)
        elif isinstance(node, ast.Await):
            return self._convert_await(node)
        elif isinstance(node, ast.Expr):
            return self._convert_expr_stmt(node)
        elif isinstance(node, ast.Assign):
            return self._convert_assign(node)
        elif isinstance(node, ast.AnnAssign):
            return self._convert_ann_assign(node)
        elif isinstance(node, ast.AugAssign):
            return self._convert_aug_assign(node)
        elif isinstance(node, ast.Raise):
            return self._convert_raise(node)
        elif isinstance(node, ast.Assert):
            return self._convert_assert(node)
        elif isinstance(node, ast.Delete):
            return self._convert_delete(node)
        elif isinstance(node, ast.Pass):
            return self._convert_pass(node)
        elif isinstance(node, ast.Break):
            return self._convert_break(node)
        elif isinstance(node, ast.Continue):
            return self._convert_continue(node)
        elif isinstance(node, ast.If):
            return self._convert_if(node)
        elif isinstance(node, ast.While):
            return self._convert_while(node)
        elif isinstance(node, ast.For):
            return self._convert_for(node)
        elif isinstance(node, ast.Try):
            return self._convert_try(node)
        elif isinstance(node, ast.With):
            return self._convert_with(node)
        elif isinstance(node, ast.FunctionDef):
            return self._convert_functiondef(node)
        elif isinstance(node, ast.AsyncFunctionDef):
            return self._convert_async_functiondef(node)
        elif isinstance(node, ast.ClassDef):
            return self._convert_classdef(node)
        elif isinstance(node, ast.Return):
            return self._convert_return(node)
        elif isinstance(node, ast.Global):
            return self._convert_global(node)
        elif isinstance(node, ast.Nonlocal):
            return self._convert_nonlocal(node)
        elif isinstance(node, ast.Import):
            return self._convert_import(node)
        elif isinstance(node, ast.ImportFrom):
            return self._convert_import_from(node)
        elif isinstance(node, ast.ExceptHandler):
            return self._convert_excepthandler(node)
        elif isinstance(node, ast.arguments):
            return self._convert_arguments(node)
        elif isinstance(node, ast.arg):
            return self._convert_arg(node)
        elif isinstance(node, ast.keyword):
            return self._convert_keyword(node)
        elif isinstance(node, ast.alias):
            return self._convert_alias(node)
        elif isinstance(node, ast.comprehension):
            return self._convert_comprehension(node)
        else:
            # Fallback for unknown nodes
            return PyConstant(f"Unknown node: {type(node).__name__}")
    
    def _convert_module(self, node: ast.Module) -> PyModule:
        """Convert module node."""
        body = [self.convert(stmt) for stmt in node.body]
        return PyModule(body)
    
    def _convert_constant(self, node: ast.Constant) -> PyConstant:
        """Convert constant node."""
        return PyConstant(node.value)
    
    def _convert_name(self, node: ast.Name) -> PyName:
        """Convert name node."""
        ctx = PyContext.LOAD
        if isinstance(node.ctx, ast.Store):
            ctx = PyContext.STORE
        elif isinstance(node.ctx, ast.Del):
            ctx = PyContext.DEL
        
        return PyName(node.id, ctx)
    
    def _convert_binop(self, node: ast.BinOp) -> PyBinOp:
        """Convert binary operation node."""
        left = self.convert(node.left)
        right = self.convert(node.right)
        op = self._convert_operator(node.op)
        
        return PyBinOp(left, op, right)
    
    def _convert_unaryop(self, node: ast.UnaryOp) -> PyUnaryOp:
        """Convert unary operation node."""
        operand = self.convert(node.operand)
        op = self._convert_operator(node.op)
        
        return PyUnaryOp(op, operand)
    
    def _convert_compare(self, node: ast.Compare) -> PyCompare:
        """Convert compare node."""
        left = self.convert(node.left)
        ops = [self._convert_operator(op) for op in node.ops]
        comparators = [self.convert(comp) for comp in node.comparators]
        
        return PyCompare(left, ops, comparators)
    
    def _convert_call(self, node: ast.Call) -> PyCall:
        """Convert call node."""
        func = self.convert(node.func)
        args = [self.convert(arg) for arg in node.args]
        keywords = [self.convert(kw) for kw in node.keywords]
        
        return PyCall(func, args, keywords)
    
    def _convert_attribute(self, node: ast.Attribute) -> PyAttribute:
        """Convert attribute node."""
        value = self.convert(node.value)
        ctx = PyContext.LOAD
        if isinstance(node.ctx, ast.Store):
            ctx = PyContext.STORE
        elif isinstance(node.ctx, ast.Del):
            ctx = PyContext.DEL
        
        return PyAttribute(value, node.attr, ctx)
    
    def _convert_subscript(self, node: ast.Subscript) -> PySubscript:
        """Convert subscript node."""
        value = self.convert(node.value)
        slice_node = self.convert(node.slice)
        ctx = PyContext.LOAD
        if isinstance(node.ctx, ast.Store):
            ctx = PyContext.STORE
        elif isinstance(node.ctx, ast.Del):
            ctx = PyContext.DEL
        
        return PySubscript(value, slice_node, ctx)
    
    def _convert_list(self, node: ast.List) -> PyList:
        """Convert list node."""
        elts = [self.convert(elt) for elt in node.elts]
        ctx = PyContext.LOAD
        if isinstance(node.ctx, ast.Store):
            ctx = PyContext.STORE
        elif isinstance(node.ctx, ast.Del):
            ctx = PyContext.DEL
        
        return PyList(elts, ctx)
    
    def _convert_tuple(self, node: ast.Tuple) -> PyTuple:
        """Convert tuple node."""
        elts = [self.convert(elt) for elt in node.elts]
        ctx = PyContext.LOAD
        if isinstance(node.ctx, ast.Store):
            ctx = PyContext.STORE
        elif isinstance(node.ctx, ast.Del):
            ctx = PyContext.DEL
        
        return PyTuple(elts, ctx)
    
    def _convert_set(self, node: ast.Set) -> PySet:
        """Convert set node."""
        elts = [self.convert(elt) for elt in node.elts]
        return PySet(elts)
    
    def _convert_dict(self, node: ast.Dict) -> PyDict:
        """Convert dict node."""
        keys = [self.convert(key) if key else None for key in node.keys]
        values = [self.convert(value) for value in node.values]
        return PyDict(keys, values)
    
    def _convert_listcomp(self, node: ast.ListComp) -> PyListComp:
        """Convert list comprehension node."""
        elt = self.convert(node.elt)
        generators = [self.convert(gen) for gen in node.generators]
        return PyListComp(elt, generators)
    
    def _convert_setcomp(self, node: ast.SetComp) -> PySetComp:
        """Convert set comprehension node."""
        elt = self.convert(node.elt)
        generators = [self.convert(gen) for gen in node.generators]
        return PySetComp(elt, generators)
    
    def _convert_dictcomp(self, node: ast.DictComp) -> PyDictComp:
        """Convert dict comprehension node."""
        key = self.convert(node.key)
        value = self.convert(node.value)
        generators = [self.convert(gen) for gen in node.generators]
        return PyDictComp(key, value, generators)
    
    def _convert_generatorexp(self, node: ast.GeneratorExp) -> PyGeneratorExp:
        """Convert generator expression node."""
        elt = self.convert(node.elt)
        generators = [self.convert(gen) for gen in node.generators]
        return PyGeneratorExp(elt, generators)
    
    def _convert_lambda(self, node: ast.Lambda) -> PyLambda:
        """Convert lambda node."""
        args = self.convert(node.args)
        body = self.convert(node.body)
        return PyLambda(args, body)
    
    def _convert_ifexp(self, node: ast.IfExp) -> PyIfExp:
        """Convert if expression node."""
        test = self.convert(node.test)
        body = self.convert(node.body)
        orelse = self.convert(node.orelse)
        return PyIfExp(test, body, orelse)
    
    def _convert_starred(self, node: ast.Starred) -> PyStarred:
        """Convert starred node."""
        value = self.convert(node.value)
        ctx = PyContext.LOAD
        if isinstance(node.ctx, ast.Store):
            ctx = PyContext.STORE
        elif isinstance(node.ctx, ast.Del):
            ctx = PyContext.DEL
        
        return PyStarred(value, ctx)
    
    def _convert_yield(self, node: ast.Yield) -> PyYield:
        """Convert yield node."""
        value = self.convert(node.value) if node.value else None
        return PyYield(value)
    
    def _convert_yield_from(self, node: ast.YieldFrom) -> PyYieldFrom:
        """Convert yield from node."""
        value = self.convert(node.value)
        return PyYieldFrom(value)
    
    def _convert_await(self, node: ast.Await) -> PyAwait:
        """Convert await node."""
        value = self.convert(node.value)
        return PyAwait(value)
    
    def _convert_expr_stmt(self, node: ast.Expr) -> PyExpressionStmt:
        """Convert expression statement node."""
        value = self.convert(node.value)
        return PyExpressionStmt(value)
    
    def _convert_assign(self, node: ast.Assign) -> PyAssign:
        """Convert assign node."""
        targets = [self.convert(target) for target in node.targets]
        value = self.convert(node.value)
        return PyAssign(targets, value)
    
    def _convert_ann_assign(self, node: ast.AnnAssign) -> PyAnnAssign:
        """Convert annotated assign node."""
        target = self.convert(node.target)
        annotation = self.convert(node.annotation)
        value = self.convert(node.value) if node.value else None
        return PyAnnAssign(target, annotation, value)
    
    def _convert_aug_assign(self, node: ast.AugAssign) -> PyAugAssign:
        """Convert augmented assign node."""
        target = self.convert(node.target)
        op = self._convert_operator(node.op)
        value = self.convert(node.value)
        return PyAugAssign(target, op, value)
    
    def _convert_raise(self, node: ast.Raise) -> PyRaise:
        """Convert raise node."""
        exc = self.convert(node.exc) if node.exc else None
        cause = self.convert(node.cause) if node.cause else None
        return PyRaise(exc, cause)
    
    def _convert_assert(self, node: ast.Assert) -> PyAssert:
        """Convert assert node."""
        test = self.convert(node.test)
        msg = self.convert(node.msg) if node.msg else None
        return PyAssert(test, msg)
    
    def _convert_delete(self, node: ast.Delete) -> PyDelete:
        """Convert delete node."""
        targets = [self.convert(target) for target in node.targets]
        return PyDelete(targets)
    
    def _convert_pass(self, node: ast.Pass) -> PyPass:
        """Convert pass node."""
        return PyPass()
    
    def _convert_break(self, node: ast.Break) -> PyBreak:
        """Convert break node."""
        return PyBreak()
    
    def _convert_continue(self, node: ast.Continue) -> PyContinue:
        """Convert continue node."""
        return PyContinue()
    
    def _convert_if(self, node: ast.If) -> PyIf:
        """Convert if node."""
        test = self.convert(node.test)
        body = [self.convert(stmt) for stmt in node.body]
        orelse = [self.convert(stmt) for stmt in node.orelse]
        return PyIf(test, body, orelse)
    
    def _convert_while(self, node: ast.While) -> PyWhile:
        """Convert while node."""
        test = self.convert(node.test)
        body = [self.convert(stmt) for stmt in node.body]
        orelse = [self.convert(stmt) for stmt in node.orelse]
        return PyWhile(test, body, orelse)
    
    def _convert_for(self, node: ast.For) -> PyFor:
        """Convert for node."""
        target = self.convert(node.target)
        iter_node = self.convert(node.iter)
        body = [self.convert(stmt) for stmt in node.body]
        orelse = [self.convert(stmt) for stmt in node.orelse]
        return PyFor(target, iter_node, body, orelse)
    
    def _convert_try(self, node: ast.Try) -> PyTry:
        """Convert try node."""
        body = [self.convert(stmt) for stmt in node.body]
        handlers = [self.convert(handler) for handler in node.handlers]
        orelse = [self.convert(stmt) for stmt in node.orelse]
        finalbody = [self.convert(stmt) for stmt in node.finalbody]
        return PyTry(body, handlers, orelse, finalbody)
    
    def _convert_with(self, node: ast.With) -> PyWith:
        """Convert with node."""
        items = [PyWithItem(self.convert(item.context_expr), 
                           self.convert(item.optional_vars) if item.optional_vars else None)
                for item in node.items]
        body = [self.convert(stmt) for stmt in node.body]
        return PyWith(items, body)
    
    def _convert_functiondef(self, node: ast.FunctionDef) -> PyFunctionDef:
        """Convert function definition node."""
        args = self.convert(node.args)
        body = [self.convert(stmt) for stmt in node.body]
        decorator_list = [self.convert(dec) for dec in node.decorator_list]
        returns = self.convert(node.returns) if node.returns else None
        return PyFunctionDef(node.name, args, body, decorator_list, returns)
    
    def _convert_async_functiondef(self, node: ast.AsyncFunctionDef) -> PyAsyncFunctionDef:
        """Convert async function definition node."""
        args = self.convert(node.args)
        body = [self.convert(stmt) for stmt in node.body]
        decorator_list = [self.convert(dec) for dec in node.decorator_list]
        returns = self.convert(node.returns) if node.returns else None
        return PyAsyncFunctionDef(node.name, args, body, decorator_list, returns)
    
    def _convert_classdef(self, node: ast.ClassDef) -> PyClassDef:
        """Convert class definition node."""
        bases = [self.convert(base) for base in node.bases]
        keywords = [self.convert(kw) for kw in node.keywords]
        body = [self.convert(stmt) for stmt in node.body]
        decorator_list = [self.convert(dec) for dec in node.decorator_list]
        return PyClassDef(node.name, bases, keywords, body, decorator_list)
    
    def _convert_return(self, node: ast.Return) -> PyReturn:
        """Convert return node."""
        value = self.convert(node.value) if node.value else None
        return PyReturn(value)
    
    def _convert_global(self, node: ast.Global) -> PyGlobal:
        """Convert global node."""
        return PyGlobal(node.names)
    
    def _convert_nonlocal(self, node: ast.Nonlocal) -> PyNonlocal:
        """Convert nonlocal node."""
        return PyNonlocal(node.names)
    
    def _convert_import(self, node: ast.Import) -> PyImport:
        """Convert import node."""
        names = [self.convert(alias) for alias in node.names]
        return PyImport(names)
    
    def _convert_import_from(self, node: ast.ImportFrom) -> PyImportFrom:
        """Convert import from node."""
        names = [self.convert(alias) for alias in node.names]
        return PyImportFrom(node.module, names, node.level)
    
    def _convert_excepthandler(self, node: ast.ExceptHandler) -> PyExceptHandler:
        """Convert exception handler node."""
        type_node = self.convert(node.type) if node.type else None
        body = [self.convert(stmt) for stmt in node.body]
        return PyExceptHandler(type_node, node.name, body)
    
    def _convert_arguments(self, node: ast.arguments) -> PyArguments:
        """Convert arguments node."""
        args = [self.convert(arg) for arg in node.args]
        defaults = [self.convert(default) for default in node.defaults]
        kwonlyargs = [self.convert(arg) for arg in node.kwonlyargs]
        kw_defaults = [self.convert(default) if default else None for default in node.kw_defaults]
        vararg = self.convert(node.vararg) if node.vararg else None
        kwarg = self.convert(node.kwarg) if node.kwarg else None
        
        # Handle positional-only arguments (Python 3.8+)
        posonlyargs = []
        if hasattr(node, 'posonlyargs'):
            posonlyargs = [self.convert(arg) for arg in node.posonlyargs]
        
        return PyArguments(posonlyargs, args, vararg, kwonlyargs, kw_defaults, kwarg, defaults)
    
    def _convert_arg(self, node: ast.arg) -> PyArg:
        """Convert argument node."""
        annotation = self.convert(node.annotation) if node.annotation else None
        return PyArg(node.arg, annotation)
    
    def _convert_keyword(self, node: ast.keyword) -> PyKeyword:
        """Convert keyword node."""
        value = self.convert(node.value)
        return PyKeyword(node.arg, value)
    
    def _convert_alias(self, node: ast.alias) -> PyAlias:
        """Convert alias node."""
        return PyAlias(node.name, node.asname)
    
    def _convert_comprehension(self, node: ast.comprehension) -> PyComprehension:
        """Convert comprehension node."""
        target = self.convert(node.target)
        iter_node = self.convert(node.iter)
        ifs = [self.convert(if_clause) for if_clause in node.ifs]
        is_async = getattr(node, 'is_async', False)
        return PyComprehension(target, iter_node, ifs, is_async)
    
    def _convert_operator(self, op: ast.operator) -> PyOperator:
        """Convert operator node."""
        op_map = {
            ast.Add: PyOperator.ADD,
            ast.Sub: PyOperator.SUB,
            ast.Mult: PyOperator.MULT,
            ast.Div: PyOperator.DIV,
            ast.Mod: PyOperator.MOD,
            ast.Pow: PyOperator.POW,
            ast.LShift: PyOperator.LSHIFT,
            ast.RShift: PyOperator.RSHIFT,
            ast.BitOr: PyOperator.BITOR,
            ast.BitXor: PyOperator.BITXOR,
            ast.BitAnd: PyOperator.BITAND,
            ast.FloorDiv: PyOperator.FLOORDIV,
            ast.Eq: PyOperator.EQ,
            ast.NotEq: PyOperator.NOT_EQ,
            ast.Lt: PyOperator.LT,
            ast.LtE: PyOperator.LTE,
            ast.Gt: PyOperator.GT,
            ast.GtE: PyOperator.GTE,
            ast.Is: PyOperator.IS,
            ast.IsNot: PyOperator.IS_NOT,
            ast.In: PyOperator.IN,
            ast.NotIn: PyOperator.NOT_IN,
            ast.Invert: PyOperator.INVERT,
            ast.Not: PyOperator.NOT,
            ast.UAdd: PyOperator.UADD,
            ast.USub: PyOperator.USUB,
            ast.And: PyOperator.AND,
            ast.Or: PyOperator.OR,
        }
        
        # Handle matrix multiplication (Python 3.5+)
        if hasattr(ast, 'MatMult') and isinstance(op, ast.MatMult):
            return PyOperator.MATMULT
        
        return op_map.get(type(op), PyOperator.ADD)


def parse_python(source: str) -> PyModule:
    """Parse Python source code into our custom AST."""
    try:
        # Parse using built-in ast module
        builtin_ast = ast.parse(source)
        
        # Convert to our AST format
        converter = PythonASTConverter()
        return converter.convert(builtin_ast)
        
    except SyntaxError as e:
        raise SyntaxError(f"Python syntax error: {e}")
    except Exception as e:
        raise Exception(f"Failed to parse Python code: {e}")