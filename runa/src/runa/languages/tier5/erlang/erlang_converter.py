#!/usr/bin/env python3
"""
Erlang Converter

Bidirectional converter between Erlang AST and Runa universal AST.
Handles actor model concurrency, pattern matching, and functional programming.
"""

from typing import List, Optional, Dict, Any
from ...shared.base_toolchain import BaseConverter
from ....core.ast_nodes import *
from .erlang_ast import *


class ErlangToRunaConverter(BaseConverter):
    """Convert Erlang AST to Runa AST."""
    
    def convert(self, erlang_node: ErlangNode) -> Node:
        """Convert Erlang node to Runa node."""
        if isinstance(erlang_node, ErlangProgram):
            return self._convert_program(erlang_node)
        elif isinstance(erlang_node, ErlangModule):
            return self._convert_module(erlang_node)
        elif isinstance(erlang_node, ErlangFunction):
            return self._convert_function(erlang_node)
        elif isinstance(erlang_node, ErlangAtom):
            return Literal(erlang_node.value, "atom")
        elif isinstance(erlang_node, ErlangInteger):
            return Literal(erlang_node.value, "integer")
        elif isinstance(erlang_node, ErlangFloat):
            return Literal(erlang_node.value, "float")
        elif isinstance(erlang_node, ErlangString):
            return Literal(erlang_node.value, "string")
        elif isinstance(erlang_node, ErlangBoolean):
            return Literal(erlang_node.value, "boolean")
        elif isinstance(erlang_node, ErlangVariable):
            return Identifier(erlang_node.name)
        elif isinstance(erlang_node, ErlangList):
            return self._convert_list(erlang_node)
        elif isinstance(erlang_node, ErlangTuple):
            return self._convert_tuple(erlang_node)
        elif isinstance(erlang_node, ErlangBinaryOp):
            return self._convert_binary_op(erlang_node)
        elif isinstance(erlang_node, ErlangFunctionCall):
            return self._convert_function_call(erlang_node)
        elif isinstance(erlang_node, ErlangMatch):
            return Assignment(self.convert(erlang_node.pattern), self.convert(erlang_node.expression))
        elif isinstance(erlang_node, ErlangCase):
            return self._convert_case(erlang_node)
        elif isinstance(erlang_node, ErlangSpawn):
            return self._convert_spawn(erlang_node)
        elif isinstance(erlang_node, ErlangReceive):
            return self._convert_receive(erlang_node)
        elif isinstance(erlang_node, ErlangSend):
            return self._convert_send(erlang_node)
        else:
            return Identifier("unknown_erlang_construct")
    
    def _convert_program(self, node: ErlangProgram) -> Block:
        return Block([self.convert(node.module)])
    
    def _convert_module(self, node: ErlangModule) -> Block:
        statements = []
        for attr in node.attributes:
            statements.append(self.convert(attr))
        for func in node.functions:
            statements.append(self.convert(func))
        return Block(statements)
    
    def _convert_function(self, node: ErlangFunction) -> FunctionDeclaration:
        # Convert first clause for simplicity
        clause = node.clauses[0] if node.clauses else ErlangClause([], None, [])
        parameters = [Parameter(f"arg{i}", None) for i in range(node.arity)]
        body_stmts = [self.convert(expr) for expr in clause.body]
        return FunctionDeclaration(node.name, parameters, None, Block(body_stmts), [])
    
    def _convert_list(self, node: ErlangList) -> ListLiteral:
        elements = [self.convert(elem) for elem in node.elements]
        return ListLiteral(elements)
    
    def _convert_tuple(self, node: ErlangTuple) -> ListLiteral:
        elements = [self.convert(elem) for elem in node.elements]
        return ListLiteral(elements)  # Represent as list in Runa
    
    def _convert_binary_op(self, node: ErlangBinaryOp) -> BinaryOp:
        left = self.convert(node.left)
        right = self.convert(node.right)
        return BinaryOp(left, node.operator, right)
    
    def _convert_function_call(self, node: ErlangFunctionCall) -> FunctionCall:
        function = self.convert(node.function)
        args = [self.convert(arg) for arg in node.arguments]
        return FunctionCall(function, args)
    
    def _convert_case(self, node: ErlangCase) -> IfStatement:
        # Convert case to if-else chain for simplicity
        condition = self.convert(node.expression)
        # For simplicity, convert first clause
        if node.clauses:
            clause = node.clauses[0]
            body = Block([self.convert(expr) for expr in clause.body])
            return IfStatement(condition, body, None)
        return IfStatement(condition, Block([]), None)
    
    def _convert_spawn(self, node: ErlangSpawn) -> FunctionCall:
        function = self.convert(node.function)
        args = [self.convert(arg) for arg in node.arguments]
        return FunctionCall(Identifier("spawn"), [function] + args)
    
    def _convert_receive(self, node: ErlangReceive) -> FunctionCall:
        return FunctionCall(Identifier("receive"), [])
    
    def _convert_send(self, node: ErlangSend) -> FunctionCall:
        dest = self.convert(node.destination)
        msg = self.convert(node.message)
        return FunctionCall(Identifier("send"), [dest, msg])


class RunaToErlangConverter(BaseConverter):
    """Convert Runa AST to Erlang AST."""
    
    def convert(self, runa_node: Node) -> ErlangNode:
        """Convert Runa node to Erlang node."""
        if isinstance(runa_node, Block):
            return self._convert_block(runa_node)
        elif isinstance(runa_node, Literal):
            return self._convert_literal(runa_node)
        elif isinstance(runa_node, Identifier):
            return ErlangVariable(runa_node.name)
        elif isinstance(runa_node, BinaryOp):
            return self._convert_binary_op(runa_node)
        elif isinstance(runa_node, FunctionCall):
            return self._convert_function_call(runa_node)
        elif isinstance(runa_node, FunctionDeclaration):
            return self._convert_function_declaration(runa_node)
        elif isinstance(runa_node, Assignment):
            return ErlangMatch(self.convert(runa_node.target), self.convert(runa_node.value))
        elif isinstance(runa_node, ListLiteral):
            return self._convert_list_literal(runa_node)
        else:
            return ErlangAtom("unknown_runa_construct")
    
    def _convert_block(self, node: Block) -> ErlangModule:
        functions = []
        attributes = []
        
        for stmt in node.statements:
            converted = self.convert(stmt)
            if isinstance(converted, ErlangFunction):
                functions.append(converted)
            elif isinstance(converted, ErlangAttribute):
                attributes.append(converted)
        
        return ErlangModule("generated_module", attributes, functions)
    
    def _convert_literal(self, node: Literal) -> ErlangExpression:
        if node.literal_type == "integer":
            return ErlangInteger(node.value)
        elif node.literal_type == "float":
            return ErlangFloat(node.value)
        elif node.literal_type == "string":
            return ErlangString(node.value)
        elif node.literal_type == "boolean":
            return ErlangBoolean(node.value)
        else:
            return ErlangAtom(str(node.value))
    
    def _convert_binary_op(self, node: BinaryOp) -> ErlangBinaryOp:
        left = self.convert(node.left)
        right = self.convert(node.right)
        return ErlangBinaryOp(left, node.operator, right)
    
    def _convert_function_call(self, node: FunctionCall) -> ErlangFunctionCall:
        function = self.convert(node.function)
        args = [self.convert(arg) for arg in node.arguments]
        return ErlangFunctionCall(None, function, args)
    
    def _convert_function_declaration(self, node: FunctionDeclaration) -> ErlangFunction:
        patterns = [ErlangVariable(param.name) for param in node.parameters]
        body = [self.convert(stmt) for stmt in node.body.statements] if isinstance(node.body, Block) else [self.convert(node.body)]
        clause = ErlangClause(patterns, None, body)
        return ErlangFunction(node.name, len(node.parameters), [clause])
    
    def _convert_list_literal(self, node: ListLiteral) -> ErlangList:
        elements = [self.convert(elem) for elem in node.elements]
        return ErlangList(elements)


# Convenience functions
def erlang_to_runa(erlang_ast: ErlangNode) -> Node:
    """Convert Erlang AST to Runa AST."""
    converter = ErlangToRunaConverter()
    return converter.convert(erlang_ast)


def runa_to_erlang(runa_ast: Node) -> ErlangNode:
    """Convert Runa AST to Erlang AST."""
    converter = RunaToErlangConverter()
    return converter.convert(runa_ast) 