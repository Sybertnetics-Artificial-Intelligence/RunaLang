#!/usr/bin/env python3
"""
Rholang Abstract Syntax Tree (AST) Implementation

This module provides a comprehensive AST for the Rholang language, which is a
process-oriented programming language for the RChain blockchain platform.

Rholang is based on the rho-calculus and supports:
- Process-oriented programming with concurrent execution
- Channel-based communication and synchronization
- Pattern matching and destructuring
- Smart contract development for RChain blockchain
- Message passing and process coordination
- Namespaces and contract deployment
- Formal verification capabilities

The AST follows the visitor pattern for easy traversal and transformation.
"""

from typing import Any, List, Optional, Union, Dict, Set
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum


class RholangNodeType(Enum):
    """Enumeration of all Rholang AST node types."""
    
    # Base types
    MODULE = "module"
    PROCESS = "process"
    EXPRESSION = "expression"
    PATTERN = "pattern"
    
    # Literals
    INT_LITERAL = "int_literal"
    STRING_LITERAL = "string_literal"
    BOOL_LITERAL = "bool_literal"
    BYTES_LITERAL = "bytes_literal"
    URI_LITERAL = "uri_literal"
    
    # Names and channels
    NAME = "name"
    UNFORGEABLE_NAME = "unforgeable_name"
    QUOTE = "quote"
    
    # Collections
    LIST = "list"
    TUPLE = "tuple"
    SET = "set"
    MAP = "map"
    
    # Process constructs
    PAR = "par"  # Parallel composition
    NEW = "new"  # Name restriction
    SEND = "send"
    RECEIVE = "receive"
    CONTRACT = "contract"
    MATCH = "match"
    BUNDLE = "bundle"
    
    # Control flow
    IF = "if"
    FOR = "for"
    
    # Operations
    BINARY_OP = "binary_op"
    UNARY_OP = "unary_op"
    METHOD_CALL = "method_call"
    
    # Pattern matching
    VAR_PATTERN = "var_pattern"
    WILDCARD_PATTERN = "wildcard_pattern"
    LIST_PATTERN = "list_pattern"
    TUPLE_PATTERN = "tuple_pattern"
    
    # Special constructs
    NIL = "nil"
    COPY = "copy"
    PEEK = "peek"


class RholangOperator(Enum):
    """Rholang operators."""
    
    # Arithmetic
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"
    MOD = "%"
    POW = "**"
    
    # Comparison
    EQ = "=="
    NE = "!="
    LT = "<"
    LE = "<="
    GT = ">"
    GE = ">="
    
    # Logical
    AND = "and"
    OR = "or"
    NOT = "not"
    
    # Bitwise
    BIT_AND = "&"
    BIT_OR = "|"
    BIT_XOR = "^"
    BIT_NOT = "~"
    LEFT_SHIFT = "<<"
    RIGHT_SHIFT = ">>"
    
    # String operations
    CONCAT = "++"
    
    # Set operations
    UNION = "union"
    DIFF = "diff"
    INTERSECT = "intersect"
    
    # Unary
    UADD = "+u"
    USUB = "-u"


@dataclass
class RholangNode(ABC):
    """Base class for all Rholang AST nodes."""
    
    node_type: RholangNodeType
    line: int = 0
    column: int = 0
    
    @abstractmethod
    def accept(self, visitor: 'RholangVisitor') -> Any:
        """Accept a visitor for traversal."""
        pass
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(type={self.node_type.value})"


class RholangVisitor(ABC):
    """Abstract visitor for Rholang AST traversal."""
    
    @abstractmethod
    def visit_module(self, node: 'RholangModule') -> Any:
        pass
    
    @abstractmethod
    def visit_par(self, node: 'RholangPar') -> Any:
        pass
    
    @abstractmethod
    def visit_new(self, node: 'RholangNew') -> Any:
        pass
    
    @abstractmethod
    def visit_send(self, node: 'RholangSend') -> Any:
        pass
    
    @abstractmethod
    def visit_receive(self, node: 'RholangReceive') -> Any:
        pass
    
    @abstractmethod
    def visit_contract(self, node: 'RholangContract') -> Any:
        pass
    
    @abstractmethod
    def visit_match(self, node: 'RholangMatch') -> Any:
        pass
    
    @abstractmethod
    def visit_if(self, node: 'RholangIf') -> Any:
        pass
    
    @abstractmethod
    def visit_for(self, node: 'RholangFor') -> Any:
        pass
    
    @abstractmethod
    def visit_literal(self, node: 'RholangLiteral') -> Any:
        pass
    
    @abstractmethod
    def visit_name(self, node: 'RholangName') -> Any:
        pass
    
    @abstractmethod
    def visit_quote(self, node: 'RholangQuote') -> Any:
        pass
    
    @abstractmethod
    def visit_list(self, node: 'RholangList') -> Any:
        pass
    
    @abstractmethod
    def visit_tuple(self, node: 'RholangTuple') -> Any:
        pass
    
    @abstractmethod
    def visit_set(self, node: 'RholangSet') -> Any:
        pass
    
    @abstractmethod
    def visit_map(self, node: 'RholangMap') -> Any:
        pass
    
    @abstractmethod
    def visit_binary_op(self, node: 'RholangBinaryOp') -> Any:
        pass
    
    @abstractmethod
    def visit_unary_op(self, node: 'RholangUnaryOp') -> Any:
        pass
    
    @abstractmethod
    def visit_method_call(self, node: 'RholangMethodCall') -> Any:
        pass
    
    @abstractmethod
    def visit_pattern(self, node: 'RholangPattern') -> Any:
        pass


# Base classes

@dataclass
class RholangProcess(RholangNode):
    """Base class for all Rholang processes."""
    pass


@dataclass
class RholangExpression(RholangNode):
    """Base class for all Rholang expressions."""
    pass


@dataclass
class RholangPattern(RholangNode):
    """Base class for all Rholang patterns."""
    pass


# Expression nodes

@dataclass
class RholangLiteral(RholangExpression):
    """Literal value (int, string, bool, bytes, URI)."""
    
    value: Any
    literal_type: str  # "int", "string", "bool", "bytes", "uri"
    
    def __post_init__(self):
        type_map = {
            int: (RholangNodeType.INT_LITERAL, "int"),
            str: (RholangNodeType.STRING_LITERAL, "string"),
            bool: (RholangNodeType.BOOL_LITERAL, "bool"),
            bytes: (RholangNodeType.BYTES_LITERAL, "bytes")
        }
        
        if type(self.value) in type_map:
            self.node_type, self.literal_type = type_map[type(self.value)]
        elif isinstance(self.value, str) and self.value.startswith("rho:"):
            self.node_type = RholangNodeType.URI_LITERAL
            self.literal_type = "uri"
        else:
            self.node_type = RholangNodeType.STRING_LITERAL
            self.literal_type = "string"
    
    def accept(self, visitor: RholangVisitor) -> Any:
        return visitor.visit_literal(self)


@dataclass
class RholangName(RholangExpression):
    """Name reference (variable or channel name)."""
    
    name: str
    is_wildcard: bool = False
    node_type: RholangNodeType = field(default=RholangNodeType.NAME, init=False)
    
    def accept(self, visitor: RholangVisitor) -> Any:
        return visitor.visit_name(self)


@dataclass
class RholangUnforgeableName(RholangExpression):
    """Unforgeable name (private channel)."""
    
    name: Optional[str] = None  # Optional variable binding
    node_type: RholangNodeType = field(default=RholangNodeType.UNFORGEABLE_NAME, init=False)
    
    def accept(self, visitor: RholangVisitor) -> Any:
        return visitor.visit_name(self)


@dataclass
class RholangQuote(RholangExpression):
    """Quote process as name."""
    
    process: RholangProcess
    node_type: RholangNodeType = field(default=RholangNodeType.QUOTE, init=False)
    
    def accept(self, visitor: RholangVisitor) -> Any:
        return visitor.visit_quote(self)


@dataclass
class RholangList(RholangExpression):
    """List literal [a, b, c]."""
    
    elements: List[RholangExpression]
    node_type: RholangNodeType = field(default=RholangNodeType.LIST, init=False)
    
    def accept(self, visitor: RholangVisitor) -> Any:
        return visitor.visit_list(self)


@dataclass
class RholangTuple(RholangExpression):
    """Tuple literal (a, b, c)."""
    
    elements: List[RholangExpression]
    node_type: RholangNodeType = field(default=RholangNodeType.TUPLE, init=False)
    
    def accept(self, visitor: RholangVisitor) -> Any:
        return visitor.visit_tuple(self)


@dataclass
class RholangSet(RholangExpression):
    """Set literal Set(a, b, c)."""
    
    elements: List[RholangExpression]
    node_type: RholangNodeType = field(default=RholangNodeType.SET, init=False)
    
    def accept(self, visitor: RholangVisitor) -> Any:
        return visitor.visit_set(self)


@dataclass
class RholangMap(RholangExpression):
    """Map literal {key: value, ...}."""
    
    pairs: List['RholangMapPair']
    node_type: RholangNodeType = field(default=RholangNodeType.MAP, init=False)
    
    def accept(self, visitor: RholangVisitor) -> Any:
        return visitor.visit_map(self)


@dataclass
class RholangMapPair(RholangNode):
    """Key-value pair in a map."""
    
    key: RholangExpression
    value: RholangExpression
    node_type: RholangNodeType = field(default=RholangNodeType.MAP, init=False)
    
    def accept(self, visitor: RholangVisitor) -> Any:
        return visitor.visit_map(self)


@dataclass
class RholangBinaryOp(RholangExpression):
    """Binary operation (left op right)."""
    
    left: RholangExpression
    operator: RholangOperator
    right: RholangExpression
    node_type: RholangNodeType = field(default=RholangNodeType.BINARY_OP, init=False)
    
    def accept(self, visitor: RholangVisitor) -> Any:
        return visitor.visit_binary_op(self)


@dataclass
class RholangUnaryOp(RholangExpression):
    """Unary operation (op operand)."""
    
    operator: RholangOperator
    operand: RholangExpression
    node_type: RholangNodeType = field(default=RholangNodeType.UNARY_OP, init=False)
    
    def accept(self, visitor: RholangVisitor) -> Any:
        return visitor.visit_unary_op(self)


@dataclass
class RholangMethodCall(RholangExpression):
    """Method call on an expression."""
    
    target: RholangExpression
    method: str
    arguments: List[RholangExpression]
    node_type: RholangNodeType = field(default=RholangNodeType.METHOD_CALL, init=False)
    
    def accept(self, visitor: RholangVisitor) -> Any:
        return visitor.visit_method_call(self)


# Process nodes

@dataclass
class RholangNil(RholangProcess):
    """Nil process (terminated process)."""
    
    node_type: RholangNodeType = field(default=RholangNodeType.NIL, init=False)
    
    def accept(self, visitor: RholangVisitor) -> Any:
        return visitor.visit_nil(self)


@dataclass
class RholangPar(RholangProcess):
    """Parallel composition of processes."""
    
    processes: List[RholangProcess]
    node_type: RholangNodeType = field(default=RholangNodeType.PAR, init=False)
    
    def accept(self, visitor: RholangVisitor) -> Any:
        return visitor.visit_par(self)


@dataclass
class RholangNew(RholangProcess):
    """Name restriction (new names)."""
    
    names: List[str]
    process: RholangProcess
    uri_patterns: List[str] = field(default_factory=list)
    node_type: RholangNodeType = field(default=RholangNodeType.NEW, init=False)
    
    def accept(self, visitor: RholangVisitor) -> Any:
        return visitor.visit_new(self)


@dataclass
class RholangSend(RholangProcess):
    """Send data on a channel."""
    
    channel: RholangExpression
    data: List[RholangExpression]
    persistent: bool = False
    peek: bool = False
    node_type: RholangNodeType = field(default=RholangNodeType.SEND, init=False)
    
    def accept(self, visitor: RholangVisitor) -> Any:
        return visitor.visit_send(self)


@dataclass
class RholangReceive(RholangProcess):
    """Receive data from channels."""
    
    receives: List['RholangReceivePattern']
    continuation: RholangProcess
    persistent: bool = False
    peek: bool = False
    node_type: RholangNodeType = field(default=RholangNodeType.RECEIVE, init=False)
    
    def accept(self, visitor: RholangVisitor) -> Any:
        return visitor.visit_receive(self)


@dataclass
class RholangReceivePattern(RholangNode):
    """Pattern for receiving from a channel."""
    
    channel: RholangExpression
    patterns: List[RholangPattern]
    condition: Optional[RholangExpression] = None
    node_type: RholangNodeType = field(default=RholangNodeType.RECEIVE, init=False)
    
    def accept(self, visitor: RholangVisitor) -> Any:
        return visitor.visit_receive(self)


@dataclass
class RholangContract(RholangProcess):
    """Contract definition."""
    
    name: RholangExpression
    parameters: List[RholangPattern]
    body: RholangProcess
    node_type: RholangNodeType = field(default=RholangNodeType.CONTRACT, init=False)
    
    def accept(self, visitor: RholangVisitor) -> Any:
        return visitor.visit_contract(self)


@dataclass
class RholangMatch(RholangProcess):
    """Pattern matching."""
    
    target: RholangExpression
    cases: List['RholangMatchCase']
    node_type: RholangNodeType = field(default=RholangNodeType.MATCH, init=False)
    
    def accept(self, visitor: RholangVisitor) -> Any:
        return visitor.visit_match(self)


@dataclass
class RholangMatchCase(RholangNode):
    """Case in a match expression."""
    
    pattern: RholangPattern
    condition: Optional[RholangExpression]
    body: RholangProcess
    node_type: RholangNodeType = field(default=RholangNodeType.MATCH, init=False)
    
    def accept(self, visitor: RholangVisitor) -> Any:
        return visitor.visit_match(self)


@dataclass
class RholangIf(RholangProcess):
    """Conditional process."""
    
    condition: RholangExpression
    then_process: RholangProcess
    else_process: Optional[RholangProcess] = None
    node_type: RholangNodeType = field(default=RholangNodeType.IF, init=False)
    
    def accept(self, visitor: RholangVisitor) -> Any:
        return visitor.visit_if(self)


@dataclass
class RholangFor(RholangProcess):
    """For comprehension over collections."""
    
    variables: List[RholangPattern]
    generators: List[RholangExpression]
    body: RholangProcess
    node_type: RholangNodeType = field(default=RholangNodeType.FOR, init=False)
    
    def accept(self, visitor: RholangVisitor) -> Any:
        return visitor.visit_for(self)


@dataclass
class RholangBundle(RholangProcess):
    """Bundle construct for capability control."""
    
    bundle_type: str  # "read", "write", "readWrite"
    process: RholangProcess
    node_type: RholangNodeType = field(default=RholangNodeType.BUNDLE, init=False)
    
    def accept(self, visitor: RholangVisitor) -> Any:
        return visitor.visit_bundle(self)


# Pattern nodes

@dataclass
class RholangVarPattern(RholangPattern):
    """Variable pattern for binding."""
    
    name: str
    node_type: RholangNodeType = field(default=RholangNodeType.VAR_PATTERN, init=False)
    
    def accept(self, visitor: RholangVisitor) -> Any:
        return visitor.visit_pattern(self)


@dataclass
class RholangWildcardPattern(RholangPattern):
    """Wildcard pattern (_)."""
    
    node_type: RholangNodeType = field(default=RholangNodeType.WILDCARD_PATTERN, init=False)
    
    def accept(self, visitor: RholangVisitor) -> Any:
        return visitor.visit_pattern(self)


@dataclass
class RholangListPattern(RholangPattern):
    """List pattern for destructuring."""
    
    patterns: List[RholangPattern]
    remainder: Optional[RholangPattern] = None
    node_type: RholangNodeType = field(default=RholangNodeType.LIST_PATTERN, init=False)
    
    def accept(self, visitor: RholangVisitor) -> Any:
        return visitor.visit_pattern(self)


@dataclass
class RholangTuplePattern(RholangPattern):
    """Tuple pattern for destructuring."""
    
    patterns: List[RholangPattern]
    node_type: RholangNodeType = field(default=RholangNodeType.TUPLE_PATTERN, init=False)
    
    def accept(self, visitor: RholangVisitor) -> Any:
        return visitor.visit_pattern(self)


# Module and top-level

@dataclass
class RholangModule(RholangNode):
    """Top-level module containing processes."""
    
    body: List[RholangProcess]
    imports: List[str] = field(default_factory=list)
    node_type: RholangNodeType = field(default=RholangNodeType.MODULE, init=False)
    
    def accept(self, visitor: RholangVisitor) -> Any:
        return visitor.visit_module(self)


# Helper functions for creating AST nodes

def rho_int(value: int) -> RholangLiteral:
    """Create an integer literal."""
    return RholangLiteral(value=value, literal_type="int")


def rho_string(value: str) -> RholangLiteral:
    """Create a string literal."""
    return RholangLiteral(value=value, literal_type="string")


def rho_bool(value: bool) -> RholangLiteral:
    """Create a boolean literal."""
    return RholangLiteral(value=value, literal_type="bool")


def rho_bytes(value: bytes) -> RholangLiteral:
    """Create a bytes literal."""
    return RholangLiteral(value=value, literal_type="bytes")


def rho_uri(value: str) -> RholangLiteral:
    """Create a URI literal."""
    return RholangLiteral(value=value, literal_type="uri")


def rho_name(name: str, is_wildcard: bool = False) -> RholangName:
    """Create a name reference."""
    return RholangName(name=name, is_wildcard=is_wildcard)


def rho_unforgeable(name: Optional[str] = None) -> RholangUnforgeableName:
    """Create an unforgeable name."""
    return RholangUnforgeableName(name=name)


def rho_quote(process: RholangProcess) -> RholangQuote:
    """Create a quoted process."""
    return RholangQuote(process=process)


def rho_list(elements: List[RholangExpression]) -> RholangList:
    """Create a list literal."""
    return RholangList(elements=elements)


def rho_tuple(elements: List[RholangExpression]) -> RholangTuple:
    """Create a tuple literal."""
    return RholangTuple(elements=elements)


def rho_set(elements: List[RholangExpression]) -> RholangSet:
    """Create a set literal."""
    return RholangSet(elements=elements)


def rho_map(pairs: List[RholangMapPair]) -> RholangMap:
    """Create a map literal."""
    return RholangMap(pairs=pairs)


def rho_map_pair(key: RholangExpression, value: RholangExpression) -> RholangMapPair:
    """Create a map key-value pair."""
    return RholangMapPair(key=key, value=value)


def rho_nil() -> RholangNil:
    """Create a nil process."""
    return RholangNil()


def rho_par(processes: List[RholangProcess]) -> RholangPar:
    """Create parallel composition."""
    return RholangPar(processes=processes)


def rho_new(names: List[str], process: RholangProcess, 
           uri_patterns: Optional[List[str]] = None) -> RholangNew:
    """Create name restriction."""
    return RholangNew(names=names, process=process, uri_patterns=uri_patterns or [])


def rho_send(channel: RholangExpression, data: List[RholangExpression],
            persistent: bool = False, peek: bool = False) -> RholangSend:
    """Create a send process."""
    return RholangSend(channel=channel, data=data, persistent=persistent, peek=peek)


def rho_receive(receives: List[RholangReceivePattern], continuation: RholangProcess,
               persistent: bool = False, peek: bool = False) -> RholangReceive:
    """Create a receive process."""
    return RholangReceive(receives=receives, continuation=continuation, 
                         persistent=persistent, peek=peek)


def rho_receive_pattern(channel: RholangExpression, patterns: List[RholangPattern],
                       condition: Optional[RholangExpression] = None) -> RholangReceivePattern:
    """Create a receive pattern."""
    return RholangReceivePattern(channel=channel, patterns=patterns, condition=condition)


def rho_contract(name: RholangExpression, parameters: List[RholangPattern],
                body: RholangProcess) -> RholangContract:
    """Create a contract definition."""
    return RholangContract(name=name, parameters=parameters, body=body)


def rho_match(target: RholangExpression, cases: List[RholangMatchCase]) -> RholangMatch:
    """Create a match expression."""
    return RholangMatch(target=target, cases=cases)


def rho_match_case(pattern: RholangPattern, body: RholangProcess,
                  condition: Optional[RholangExpression] = None) -> RholangMatchCase:
    """Create a match case."""
    return RholangMatchCase(pattern=pattern, condition=condition, body=body)


def rho_if(condition: RholangExpression, then_process: RholangProcess,
          else_process: Optional[RholangProcess] = None) -> RholangIf:
    """Create an if process."""
    return RholangIf(condition=condition, then_process=then_process, else_process=else_process)


def rho_for(variables: List[RholangPattern], generators: List[RholangExpression],
           body: RholangProcess) -> RholangFor:
    """Create a for comprehension."""
    return RholangFor(variables=variables, generators=generators, body=body)


def rho_var_pattern(name: str) -> RholangVarPattern:
    """Create a variable pattern."""
    return RholangVarPattern(name=name)


def rho_wildcard_pattern() -> RholangWildcardPattern:
    """Create a wildcard pattern."""
    return RholangWildcardPattern()


def rho_list_pattern(patterns: List[RholangPattern], 
                    remainder: Optional[RholangPattern] = None) -> RholangListPattern:
    """Create a list pattern."""
    return RholangListPattern(patterns=patterns, remainder=remainder)


def rho_tuple_pattern(patterns: List[RholangPattern]) -> RholangTuplePattern:
    """Create a tuple pattern."""
    return RholangTuplePattern(patterns=patterns)


# Validation functions

def validate_rholang_ast(node: RholangNode) -> List[str]:
    """Validate a Rholang AST and return any errors."""
    errors = []
    
    class ValidationVisitor(RholangVisitor):
        def visit_module(self, node: RholangModule) -> None:
            for process in node.body:
                process.accept(self)
        
        def visit_par(self, node: RholangPar) -> None:
            if len(node.processes) < 2:
                errors.append("Parallel composition must have at least 2 processes")
            for process in node.processes:
                process.accept(self)
        
        def visit_new(self, node: RholangNew) -> None:
            if not node.names:
                errors.append("New construct must declare at least one name")
            for name in node.names:
                if not name.isidentifier():
                    errors.append(f"Invalid name in new construct: {name}")
            node.process.accept(self)
        
        def visit_send(self, node: RholangSend) -> None:
            node.channel.accept(self)
            for data in node.data:
                data.accept(self)
        
        def visit_receive(self, node: RholangReceive) -> None:
            if not node.receives:
                errors.append("Receive must have at least one receive pattern")
            for receive in node.receives:
                receive.accept(self)
            node.continuation.accept(self)
        
        def visit_contract(self, node: RholangContract) -> None:
            node.name.accept(self)
            for param in node.parameters:
                param.accept(self)
            node.body.accept(self)
        
        def visit_match(self, node: RholangMatch) -> None:
            if not node.cases:
                errors.append("Match must have at least one case")
            node.target.accept(self)
            for case in node.cases:
                case.accept(self)
        
        def visit_if(self, node: RholangIf) -> None:
            node.condition.accept(self)
            node.then_process.accept(self)
            if node.else_process:
                node.else_process.accept(self)
        
        def visit_for(self, node: RholangFor) -> None:
            if len(node.variables) != len(node.generators):
                errors.append("For comprehension must have equal number of variables and generators")
            for var in node.variables:
                var.accept(self)
            for gen in node.generators:
                gen.accept(self)
            node.body.accept(self)
        
        def visit_literal(self, node: RholangLiteral) -> None:
            if node.literal_type == "uri" and not node.value.startswith("rho:"):
                errors.append(f"Invalid URI literal: {node.value}")
        
        def visit_name(self, node: RholangName) -> None:
            if not node.is_wildcard and not node.name.isidentifier():
                errors.append(f"Invalid name: {node.name}")
        
        def visit_quote(self, node: RholangQuote) -> None:
            node.process.accept(self)
        
        def visit_list(self, node: RholangList) -> None:
            for elem in node.elements:
                elem.accept(self)
        
        def visit_tuple(self, node: RholangTuple) -> None:
            for elem in node.elements:
                elem.accept(self)
        
        def visit_set(self, node: RholangSet) -> None:
            for elem in node.elements:
                elem.accept(self)
        
        def visit_map(self, node: RholangMap) -> None:
            for pair in node.pairs:
                pair.key.accept(self)
                pair.value.accept(self)
        
        def visit_binary_op(self, node: RholangBinaryOp) -> None:
            node.left.accept(self)
            node.right.accept(self)
        
        def visit_unary_op(self, node: RholangUnaryOp) -> None:
            node.operand.accept(self)
        
        def visit_method_call(self, node: RholangMethodCall) -> None:
            node.target.accept(self)
            for arg in node.arguments:
                arg.accept(self)
        
        def visit_pattern(self, node: RholangPattern) -> None:
            if isinstance(node, RholangVarPattern):
                if not node.name.isidentifier():
                    errors.append(f"Invalid variable pattern: {node.name}")
            elif isinstance(node, RholangListPattern):
                for pattern in node.patterns:
                    pattern.accept(self)
                if node.remainder:
                    node.remainder.accept(self)
            elif isinstance(node, RholangTuplePattern):
                for pattern in node.patterns:
                    pattern.accept(self)
        
        def visit_nil(self, node: RholangNil) -> None:
            pass
        
        def visit_bundle(self, node: RholangBundle) -> None:
            if node.bundle_type not in ["read", "write", "readWrite"]:
                errors.append(f"Invalid bundle type: {node.bundle_type}")
            node.process.accept(self)
    
    visitor = ValidationVisitor()
    node.accept(visitor)
    return errors


__all__ = [
    # Base classes
    "RholangNode", "RholangProcess", "RholangExpression", "RholangPattern", "RholangVisitor",
    
    # Enums
    "RholangNodeType", "RholangOperator",
    
    # Expression nodes
    "RholangLiteral", "RholangName", "RholangUnforgeableName", "RholangQuote",
    "RholangList", "RholangTuple", "RholangSet", "RholangMap", "RholangMapPair",
    "RholangBinaryOp", "RholangUnaryOp", "RholangMethodCall",
    
    # Process nodes
    "RholangNil", "RholangPar", "RholangNew", "RholangSend", "RholangReceive",
    "RholangReceivePattern", "RholangContract", "RholangMatch", "RholangMatchCase",
    "RholangIf", "RholangFor", "RholangBundle",
    
    # Pattern nodes
    "RholangVarPattern", "RholangWildcardPattern", "RholangListPattern", "RholangTuplePattern",
    
    # Module
    "RholangModule",
    
    # Helper functions
    "rho_int", "rho_string", "rho_bool", "rho_bytes", "rho_uri",
    "rho_name", "rho_unforgeable", "rho_quote", "rho_list", "rho_tuple", "rho_set", "rho_map",
    "rho_map_pair", "rho_nil", "rho_par", "rho_new", "rho_send", "rho_receive",
    "rho_receive_pattern", "rho_contract", "rho_match", "rho_match_case", "rho_if", "rho_for",
    "rho_var_pattern", "rho_wildcard_pattern", "rho_list_pattern", "rho_tuple_pattern",
    
    # Validation
    "validate_rholang_ast"
] 