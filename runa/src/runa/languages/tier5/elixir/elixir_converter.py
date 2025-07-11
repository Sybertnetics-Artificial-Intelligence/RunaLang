#!/usr/bin/env python3
"""
Elixir AST Converter Module

This module provides bidirectional conversion between Elixir AST and Runa Universal AST,
supporting all major language constructs including:
- Actor model with processes and message passing
- Pattern matching and guards
- Functional programming constructs
- Pipe operators and function composition
- Modules, functions, and protocols
- Macros and metaprogramming
"""

from typing import Any, Dict, List, Optional, Union
from ...core.base_components import BaseConverter, Node, NodeType
from .elixir_ast import *

class ElixirToRunaConverter(BaseConverter):
    """Converts Elixir AST to Runa Universal AST."""
    
    def __init__(self):
        super().__init__()
        self.source_language = "elixir"
        self.target_language = "runa"
    
    def convert_node(self, node: ElixirNode) -> Node:
        """Convert an Elixir AST node to a Runa node."""
        method_name = f"convert_{node.node_type.value}"
        method = getattr(self, method_name, None)
        
        if method:
            return method(node)
        else:
            # Fallback for unsupported nodes
            return Node(
                node_type=NodeType.UNKNOWN,
                value=str(node.node_type.value),
                children=[],
                metadata={
                    "original_type": node.node_type.value,
                    "source_language": "elixir"
                }
            )
    
    def convert_atom(self, node: ElixirAtom) -> Node:
        """Convert atom to Runa constant."""
        return Node(
            node_type=NodeType.LITERAL,
            value=node.value,
            metadata={
                "literal_type": "atom",
                "elixir_type": "atom"
            }
        )
    
    def convert_integer(self, node: ElixirInteger) -> Node:
        """Convert integer to Runa number."""
        return Node(
            node_type=NodeType.LITERAL,
            value=node.value,
            metadata={"literal_type": "integer"}
        )
    
    def convert_float(self, node: ElixirFloat) -> Node:
        """Convert float to Runa number."""
        return Node(
            node_type=NodeType.LITERAL,
            value=node.value,
            metadata={"literal_type": "float"}
        )
    
    def convert_string(self, node: ElixirString) -> Node:
        """Convert string to Runa string."""
        return Node(
            node_type=NodeType.LITERAL,
            value=node.value,
            metadata={
                "literal_type": "string",
                "interpolated": node.interpolated
            }
        )
    
    def convert_boolean(self, node: ElixirBoolean) -> Node:
        """Convert boolean to Runa boolean."""
        return Node(
            node_type=NodeType.LITERAL,
            value=node.value,
            metadata={"literal_type": "boolean"}
        )
    
    def convert_nil(self, node: ElixirNil) -> Node:
        """Convert nil to Runa null."""
        return Node(
            node_type=NodeType.LITERAL,
            value=None,
            metadata={"literal_type": "nil"}
        )
    
    def convert_variable(self, node: ElixirVariable) -> Node:
        """Convert variable to Runa identifier."""
        return Node(
            node_type=NodeType.IDENTIFIER,
            value=node.name
        )
    
    def convert_list(self, node: ElixirList) -> Node:
        """Convert list to Runa list."""
        elements = [self.convert_node(elem) for elem in node.elements]
        
        result = Node(
            node_type=NodeType.LIST,
            children=elements,
            metadata={"collection_type": "list"}
        )
        
        if node.tail:
            result.metadata["has_tail"] = True
            result.children.append(self.convert_node(node.tail))
        
        return result
    
    def convert_tuple(self, node: ElixirTuple) -> Node:
        """Convert tuple to Runa tuple."""
        elements = [self.convert_node(elem) for elem in node.elements]
        return Node(
            node_type=NodeType.TUPLE,
            children=elements,
            metadata={"collection_type": "tuple"}
        )
    
    def convert_map(self, node: ElixirMap) -> Node:
        """Convert map to Runa dictionary."""
        pairs = []
        for key, value in node.pairs:
            key_node = self.convert_node(key)
            value_node = self.convert_node(value)
            pair = Node(
                node_type=NodeType.KEY_VALUE_PAIR,
                children=[key_node, value_node]
            )
            pairs.append(pair)
        
        return Node(
            node_type=NodeType.DICTIONARY,
            children=pairs,
            metadata={"collection_type": "map"}
        )
    
    def convert_pipe(self, node: ElixirPipe) -> Node:
        """Convert pipe operator to Runa function composition."""
        left = self.convert_node(node.left)
        right = self.convert_node(node.right)
        
        return Node(
            node_type=NodeType.FUNCTION_CALL,
            children=[right, left],
            metadata={
                "operator": "pipe",
                "elixir_construct": "pipe_operator"
            }
        )
    
    def convert_match(self, node: ElixirMatch) -> Node:
        """Convert match expression to Runa assignment."""
        left = self.convert_node(node.left)
        right = self.convert_node(node.right)
        
        return Node(
            node_type=NodeType.ASSIGNMENT,
            children=[left, right],
            metadata={"assignment_type": "pattern_match"}
        )
    
    def convert_binary_op(self, node: ElixirBinaryOp) -> Node:
        """Convert binary operation to Runa binary operation."""
        left = self.convert_node(node.left)
        right = self.convert_node(node.right)
        
        return Node(
            node_type=NodeType.BINARY_OP,
            value=node.operator,
            children=[left, right]
        )
    
    def convert_function_call(self, node: ElixirFunctionCall) -> Node:
        """Convert function call to Runa function call."""
        args = [self.convert_node(arg) for arg in node.args]
        function_node = Node(node_type=NodeType.IDENTIFIER, value=node.function)
        
        return Node(
            node_type=NodeType.FUNCTION_CALL,
            children=[function_node] + args
        )
    
    def convert_remote_call(self, node: ElixirRemoteCall) -> Node:
        """Convert remote call to Runa method call."""
        module = self.convert_node(node.module)
        args = [self.convert_node(arg) for arg in node.args]
        
        return Node(
            node_type=NodeType.METHOD_CALL,
            value=node.function,
            children=[module] + args,
            metadata={"call_type": "remote"}
        )
    
    def convert_case(self, node: ElixirCase) -> Node:
        """Convert case expression to Runa match expression."""
        expr = self.convert_node(node.expr)
        clauses = [self.convert_node(clause) for clause in node.clauses]
        
        return Node(
            node_type=NodeType.MATCH,
            children=[expr] + clauses,
            metadata={"construct": "case"}
        )
    
    def convert_if(self, node: ElixirIf) -> Node:
        """Convert if expression to Runa conditional."""
        condition = self.convert_node(node.condition)
        then_branch = self.convert_node(node.then_branch)
        
        children = [condition, then_branch]
        if node.else_branch:
            else_branch = self.convert_node(node.else_branch)
            children.append(else_branch)
        
        return Node(
            node_type=NodeType.CONDITIONAL,
            children=children
        )
    
    def convert_spawn(self, node: ElixirSpawn) -> Node:
        """Convert spawn to Runa process creation."""
        function = self.convert_node(node.function)
        args = [self.convert_node(arg) for arg in node.args]
        
        return Node(
            node_type=NodeType.FUNCTION_CALL,
            value="spawn_process",
            children=[function] + args,
            metadata={
                "construct": "process_spawn",
                "concurrency_model": "actor"
            }
        )
    
    def convert_send(self, node: ElixirSend) -> Node:
        """Convert send to Runa message send."""
        destination = self.convert_node(node.destination)
        message = self.convert_node(node.message)
        
        return Node(
            node_type=NodeType.FUNCTION_CALL,
            value="send_message",
            children=[destination, message],
            metadata={
                "construct": "message_send",
                "concurrency_model": "actor"
            }
        )
    
    def convert_receive(self, node: ElixirReceive) -> Node:
        """Convert receive to Runa message receive."""
        clauses = [self.convert_node(clause) for clause in node.clauses]
        
        result = Node(
            node_type=NodeType.FUNCTION_CALL,
            value="receive_message",
            children=clauses,
            metadata={
                "construct": "message_receive",
                "concurrency_model": "actor"
            }
        )
        
        if node.after_clause:
            timeout, body = node.after_clause
            timeout_node = self.convert_node(timeout)
            body_node = self.convert_node(body)
            result.metadata["has_timeout"] = True
            result.children.extend([timeout_node, body_node])
        
        return result
    
    def convert_function(self, node: ElixirFunction) -> Node:
        """Convert function to Runa function definition."""
        clauses = [self.convert_node(clause) for clause in node.clauses]
        
        return Node(
            node_type=NodeType.FUNCTION_DEFINITION,
            value=node.name,
            children=clauses,
            metadata={
                "arity": node.arity,
                "private": node.private
            }
        )
    
    def convert_module(self, node: ElixirModule) -> Node:
        """Convert module to Runa module."""
        body = [self.convert_node(stmt) for stmt in node.body]
        attributes = [self.convert_node(attr) for attr in node.attributes]
        
        return Node(
            node_type=NodeType.MODULE,
            value=node.name,
            children=attributes + body,
            metadata={"language": "elixir"}
        )
    
    def convert_program(self, node: ElixirProgram) -> Node:
        """Convert program to Runa program."""
        statements = [self.convert_node(stmt) for stmt in node.statements]
        
        return Node(
            node_type=NodeType.PROGRAM,
            children=statements,
            metadata={"source_language": "elixir"}
        )

class RunaToElixirConverter(BaseConverter):
    """Converts Runa Universal AST to Elixir AST."""
    
    def __init__(self):
        super().__init__()
        self.source_language = "runa"
        self.target_language = "elixir"
    
    def convert_node(self, node: Node) -> ElixirNode:
        """Convert a Runa node to an Elixir AST node."""
        if node.node_type == NodeType.LITERAL:
            return self.convert_literal(node)
        elif node.node_type == NodeType.IDENTIFIER:
            return self.convert_identifier(node)
        elif node.node_type == NodeType.LIST:
            return self.convert_list(node)
        elif node.node_type == NodeType.TUPLE:
            return self.convert_tuple(node)
        elif node.node_type == NodeType.DICTIONARY:
            return self.convert_dictionary(node)
        elif node.node_type == NodeType.BINARY_OP:
            return self.convert_binary_op(node)
        elif node.node_type == NodeType.FUNCTION_CALL:
            return self.convert_function_call(node)
        elif node.node_type == NodeType.ASSIGNMENT:
            return self.convert_assignment(node)
        elif node.node_type == NodeType.CONDITIONAL:
            return self.convert_conditional(node)
        elif node.node_type == NodeType.FUNCTION_DEFINITION:
            return self.convert_function_definition(node)
        elif node.node_type == NodeType.MODULE:
            return self.convert_module(node)
        elif node.node_type == NodeType.PROGRAM:
            return self.convert_program(node)
        else:
            # Fallback for unsupported nodes
            return ElixirAtom(value=f"unsupported_{node.node_type.value}")
    
    def convert_literal(self, node: Node) -> ElixirExpression:
        """Convert literal to appropriate Elixir literal."""
        metadata = node.metadata or {}
        literal_type = metadata.get("literal_type", "unknown")
        
        if literal_type == "atom":
            return ElixirAtom(value=str(node.value))
        elif literal_type in ["integer", "int"]:
            return ElixirInteger(value=int(node.value))
        elif literal_type in ["float", "double"]:
            return ElixirFloat(value=float(node.value))
        elif literal_type == "string":
            interpolated = metadata.get("interpolated", False)
            return ElixirString(value=str(node.value), interpolated=interpolated)
        elif literal_type == "boolean":
            return ElixirBoolean(value=bool(node.value))
        elif literal_type == "nil" or node.value is None:
            return ElixirNil()
        else:
            # Default to string representation
            return ElixirString(value=str(node.value))
    
    def convert_identifier(self, node: Node) -> ElixirVariable:
        """Convert identifier to Elixir variable."""
        return ElixirVariable(name=str(node.value))
    
    def convert_list(self, node: Node) -> ElixirList:
        """Convert list to Elixir list."""
        elements = []
        tail = None
        
        for i, child in enumerate(node.children):
            if i == len(node.children) - 1 and node.metadata and node.metadata.get("has_tail"):
                tail = self.convert_node(child)
            else:
                elements.append(self.convert_node(child))
        
        return ElixirList(elements=elements, tail=tail)
    
    def convert_tuple(self, node: Node) -> ElixirTuple:
        """Convert tuple to Elixir tuple."""
        elements = [self.convert_node(child) for child in node.children]
        return ElixirTuple(elements=elements)
    
    def convert_dictionary(self, node: Node) -> ElixirMap:
        """Convert dictionary to Elixir map."""
        pairs = []
        for child in node.children:
            if child.node_type == NodeType.KEY_VALUE_PAIR and len(child.children) == 2:
                key = self.convert_node(child.children[0])
                value = self.convert_node(child.children[1])
                pairs.append((key, value))
        
        return ElixirMap(pairs=pairs)
    
    def convert_binary_op(self, node: Node) -> ElixirBinaryOp:
        """Convert binary operation to Elixir binary operation."""
        if len(node.children) >= 2:
            left = self.convert_node(node.children[0])
            right = self.convert_node(node.children[1])
            return ElixirBinaryOp(left=left, operator=str(node.value), right=right)
        else:
            # Fallback
            return ElixirAtom(value="invalid_binary_op")
    
    def convert_function_call(self, node: Node) -> ElixirExpression:
        """Convert function call to appropriate Elixir construct."""
        metadata = node.metadata or {}
        
        # Check for special constructs
        if metadata.get("construct") == "process_spawn":
            if len(node.children) >= 1:
                function = self.convert_node(node.children[0])
                args = [self.convert_node(child) for child in node.children[1:]]
                return ElixirSpawn(function=function, args=args)
        
        elif metadata.get("construct") == "message_send":
            if len(node.children) >= 2:
                destination = self.convert_node(node.children[0])
                message = self.convert_node(node.children[1])
                return ElixirSend(destination=destination, message=message)
        
        elif metadata.get("construct") == "message_receive":
            clauses = [self.convert_node(child) for child in node.children]
            return ElixirReceive(clauses=clauses)
        
        elif metadata.get("operator") == "pipe":
            if len(node.children) >= 2:
                right = self.convert_node(node.children[0])  # Function in pipe
                left = self.convert_node(node.children[1])   # Value being piped
                return ElixirPipe(left=left, right=right)
        
        # Regular function call
        if len(node.children) >= 1:
            function_name = str(node.value) if node.value else str(node.children[0].value)
            args = [self.convert_node(child) for child in node.children[1:]]
            return ElixirFunctionCall(function=function_name, args=args)
        else:
            return ElixirFunctionCall(function=str(node.value or "unknown"), args=[])
    
    def convert_assignment(self, node: Node) -> ElixirMatch:
        """Convert assignment to Elixir match expression."""
        if len(node.children) >= 2:
            left = self.convert_node(node.children[0])
            right = self.convert_node(node.children[1])
            return ElixirMatch(left=left, right=right)
        else:
            # Fallback
            return ElixirAtom(value="invalid_assignment")
    
    def convert_conditional(self, node: Node) -> ElixirIf:
        """Convert conditional to Elixir if expression."""
        if len(node.children) >= 2:
            condition = self.convert_node(node.children[0])
            then_branch = self.convert_node(node.children[1])
            else_branch = None
            
            if len(node.children) >= 3:
                else_branch = self.convert_node(node.children[2])
            
            return ElixirIf(condition=condition, then_branch=then_branch, else_branch=else_branch)
        else:
            # Fallback
            return ElixirAtom(value="invalid_conditional")
    
    def convert_function_definition(self, node: Node) -> ElixirFunction:
        """Convert function definition to Elixir function."""
        name = str(node.value or "unknown")
        metadata = node.metadata or {}
        arity = metadata.get("arity", len(node.children))
        private = metadata.get("private", False)
        
        # Convert clauses
        clauses = []
        for child in node.children:
            # For now, create a simple clause
            clause = ElixirClause(pattern=None, guard=None, body=self.convert_node(child))
            clauses.append(clause)
        
        return ElixirFunction(name=name, arity=arity, clauses=clauses, private=private)
    
    def convert_module(self, node: Node) -> ElixirModule:
        """Convert module to Elixir module."""
        name = str(node.value or "UnknownModule")
        body = [self.convert_node(child) for child in node.children]
        
        return ElixirModule(name=name, body=body)
    
    def convert_program(self, node: Node) -> ElixirProgram:
        """Convert program to Elixir program."""
        statements = [self.convert_node(child) for child in node.children]
        return ElixirProgram(statements=statements)

# Convenience functions

def elixir_to_runa(elixir_ast: ElixirNode) -> Node:
    """Convert Elixir AST to Runa Universal AST."""
    converter = ElixirToRunaConverter()
    return converter.convert_node(elixir_ast)

def runa_to_elixir(runa_ast: Node) -> ElixirNode:
    """Convert Runa Universal AST to Elixir AST."""
    converter = RunaToElixirConverter()
    return converter.convert_node(runa_ast) 