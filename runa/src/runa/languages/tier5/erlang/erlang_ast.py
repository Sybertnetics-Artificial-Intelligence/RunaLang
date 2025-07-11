#!/usr/bin/env python3
"""
Erlang AST Node Definitions

Comprehensive Abstract Syntax Tree nodes for Erlang covering
actor model concurrency, pattern matching, functional programming,
and distributed systems features.
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod


class ErlangNodeType(Enum):
    """Erlang AST node types."""
    # Literals
    ATOM = auto()
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    BINARY = auto()
    BOOLEAN = auto()
    
    # Collections
    LIST = auto()
    TUPLE = auto()
    MAP = auto()
    RECORD = auto()
    
    # Variables and identifiers
    VARIABLE = auto()
    
    # Expressions
    MATCH = auto()
    BINARY_OP = auto()
    UNARY_OP = auto()
    FUNCTION_CALL = auto()
    
    # Pattern matching
    PATTERN = auto()
    CASE = auto()
    IF = auto()
    
    # Functions
    FUNCTION = auto()
    CLAUSE = auto()
    LAMBDA = auto()  # fun expressions
    
    # Modules and attributes
    MODULE = auto()
    ATTRIBUTE = auto()
    EXPORT = auto()
    IMPORT = auto()
    
    # Concurrency and processes
    SPAWN = auto()
    RECEIVE = auto()
    SEND = auto()
    
    # Control flow
    TRY = auto()
    CATCH = auto()
    THROW = auto()
    BEGIN = auto()
    
    # Comprehensions
    LIST_COMPREHENSION = auto()
    BINARY_COMPREHENSION = auto()
    
    # Guards
    GUARD = auto()
    GUARD_SEQUENCE = auto()
    
    # Records
    RECORD_DEFINITION = auto()
    RECORD_ACCESS = auto()
    RECORD_UPDATE = auto()
    
    # Macros
    MACRO_DEFINITION = auto()
    MACRO_CALL = auto()
    
    # Program
    PROGRAM = auto()


@dataclass
class ErlangNode(ABC):
    """Base class for all Erlang AST nodes."""
    type: ErlangNodeType = None
    location: Optional[tuple] = None
    
    @abstractmethod
    def accept(self, visitor):
        """Accept a visitor for the visitor pattern."""
        pass


@dataclass
class ErlangExpression(ErlangNode):
    """Base class for Erlang expressions."""
    pass


@dataclass
class ErlangStatement(ErlangNode):
    """Base class for Erlang statements."""
    pass


# Literals
@dataclass
class ErlangAtom(ErlangExpression):
    """Erlang atom literal."""
    value: str
    
    def __post_init__(self):
        self.type = ErlangNodeType.ATOM
    
    def accept(self, visitor):
        return visitor.visit_atom(self)


@dataclass
class ErlangInteger(ErlangExpression):
    """Erlang integer literal."""
    value: int
    
    def __post_init__(self):
        self.type = ErlangNodeType.INTEGER
    
    def accept(self, visitor):
        return visitor.visit_integer(self)


@dataclass
class ErlangFloat(ErlangExpression):
    """Erlang float literal."""
    value: float
    
    def __post_init__(self):
        self.type = ErlangNodeType.FLOAT
    
    def accept(self, visitor):
        return visitor.visit_float(self)


@dataclass
class ErlangString(ErlangExpression):
    """Erlang string literal."""
    value: str
    
    def __post_init__(self):
        self.type = ErlangNodeType.STRING
    
    def accept(self, visitor):
        return visitor.visit_string(self)


@dataclass
class ErlangBinary(ErlangExpression):
    """Erlang binary literal."""
    elements: List[ErlangExpression]
    
    def __post_init__(self):
        self.type = ErlangNodeType.BINARY
    
    def accept(self, visitor):
        return visitor.visit_binary(self)


@dataclass
class ErlangBoolean(ErlangExpression):
    """Erlang boolean literal."""
    value: bool
    
    def __post_init__(self):
        self.type = ErlangNodeType.BOOLEAN
    
    def accept(self, visitor):
        return visitor.visit_boolean(self)


# Collections
@dataclass
class ErlangList(ErlangExpression):
    """Erlang list."""
    elements: List[ErlangExpression]
    tail: Optional[ErlangExpression] = None  # For [H|T] syntax
    
    def __post_init__(self):
        self.type = ErlangNodeType.LIST
    
    def accept(self, visitor):
        return visitor.visit_list(self)


@dataclass
class ErlangTuple(ErlangExpression):
    """Erlang tuple."""
    elements: List[ErlangExpression]
    
    def __post_init__(self):
        self.type = ErlangNodeType.TUPLE
    
    def accept(self, visitor):
        return visitor.visit_tuple(self)


@dataclass
class ErlangMap(ErlangExpression):
    """Erlang map."""
    pairs: List[tuple]  # List of (key, value) pairs
    
    def __post_init__(self):
        self.type = ErlangNodeType.MAP
    
    def accept(self, visitor):
        return visitor.visit_map(self)


@dataclass
class ErlangRecord(ErlangExpression):
    """Erlang record."""
    name: str
    fields: Dict[str, ErlangExpression]
    
    def __post_init__(self):
        self.type = ErlangNodeType.RECORD
    
    def accept(self, visitor):
        return visitor.visit_record(self)


# Variables
@dataclass
class ErlangVariable(ErlangExpression):
    """Erlang variable."""
    name: str
    
    def __post_init__(self):
        self.type = ErlangNodeType.VARIABLE
    
    def accept(self, visitor):
        return visitor.visit_variable(self)


# Expressions
@dataclass
class ErlangMatch(ErlangExpression):
    """Erlang match expression (=)."""
    pattern: ErlangExpression
    expression: ErlangExpression
    
    def __post_init__(self):
        self.type = ErlangNodeType.MATCH
    
    def accept(self, visitor):
        return visitor.visit_match(self)


@dataclass
class ErlangBinaryOp(ErlangExpression):
    """Erlang binary operation."""
    left: ErlangExpression
    operator: str
    right: ErlangExpression
    
    def __post_init__(self):
        self.type = ErlangNodeType.BINARY_OP
    
    def accept(self, visitor):
        return visitor.visit_binary_op(self)


@dataclass
class ErlangUnaryOp(ErlangExpression):
    """Erlang unary operation."""
    operator: str
    operand: ErlangExpression
    
    def __post_init__(self):
        self.type = ErlangNodeType.UNARY_OP
    
    def accept(self, visitor):
        return visitor.visit_unary_op(self)


@dataclass
class ErlangFunctionCall(ErlangExpression):
    """Erlang function call."""
    module: Optional[ErlangExpression]  # For module:function() calls
    function: ErlangExpression
    arguments: List[ErlangExpression]
    
    def __post_init__(self):
        self.type = ErlangNodeType.FUNCTION_CALL
    
    def accept(self, visitor):
        return visitor.visit_function_call(self)


# Pattern matching
@dataclass
class ErlangPattern(ErlangExpression):
    """Erlang pattern."""
    pattern: ErlangExpression
    
    def __post_init__(self):
        self.type = ErlangNodeType.PATTERN
    
    def accept(self, visitor):
        return visitor.visit_pattern(self)


@dataclass
class ErlangCase(ErlangExpression):
    """Erlang case expression."""
    expression: ErlangExpression
    clauses: List['ErlangClause']
    
    def __post_init__(self):
        self.type = ErlangNodeType.CASE
    
    def accept(self, visitor):
        return visitor.visit_case(self)


@dataclass
class ErlangIf(ErlangExpression):
    """Erlang if expression."""
    clauses: List['ErlangClause']
    
    def __post_init__(self):
        self.type = ErlangNodeType.IF
    
    def accept(self, visitor):
        return visitor.visit_if(self)


# Functions
@dataclass
class ErlangFunction(ErlangStatement):
    """Erlang function definition."""
    name: str
    arity: int
    clauses: List['ErlangClause']
    
    def __post_init__(self):
        self.type = ErlangNodeType.FUNCTION
    
    def accept(self, visitor):
        return visitor.visit_function(self)


@dataclass
class ErlangClause(ErlangNode):
    """Erlang function clause."""
    patterns: List[ErlangExpression]
    guards: Optional[List['ErlangGuard']] = None
    body: List[ErlangExpression] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = ErlangNodeType.CLAUSE
    
    def accept(self, visitor):
        return visitor.visit_clause(self)


@dataclass
class ErlangLambda(ErlangExpression):
    """Erlang fun expression (lambda)."""
    clauses: List[ErlangClause]
    
    def __post_init__(self):
        self.type = ErlangNodeType.LAMBDA
    
    def accept(self, visitor):
        return visitor.visit_lambda(self)


# Module and attributes
@dataclass
class ErlangModule(ErlangNode):
    """Erlang module."""
    name: str
    attributes: List['ErlangAttribute'] = field(default_factory=list)
    functions: List[ErlangFunction] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = ErlangNodeType.MODULE
    
    def accept(self, visitor):
        return visitor.visit_module(self)


@dataclass
class ErlangAttribute(ErlangStatement):
    """Erlang module attribute."""
    name: str
    value: ErlangExpression
    
    def __post_init__(self):
        self.type = ErlangNodeType.ATTRIBUTE
    
    def accept(self, visitor):
        return visitor.visit_attribute(self)


@dataclass
class ErlangExport(ErlangAttribute):
    """Erlang export attribute."""
    functions: List[tuple]  # List of (function_name, arity) pairs
    
    def __post_init__(self):
        self.type = ErlangNodeType.EXPORT
    
    def accept(self, visitor):
        return visitor.visit_export(self)


@dataclass
class ErlangImport(ErlangAttribute):
    """Erlang import attribute."""
    module: str
    functions: List[tuple]  # List of (function_name, arity) pairs
    
    def __post_init__(self):
        self.type = ErlangNodeType.IMPORT
    
    def accept(self, visitor):
        return visitor.visit_import(self)


# Concurrency and processes
@dataclass
class ErlangSpawn(ErlangExpression):
    """Erlang spawn expression."""
    module: Optional[ErlangExpression]
    function: ErlangExpression
    arguments: List[ErlangExpression]
    
    def __post_init__(self):
        self.type = ErlangNodeType.SPAWN
    
    def accept(self, visitor):
        return visitor.visit_spawn(self)


@dataclass
class ErlangReceive(ErlangExpression):
    """Erlang receive expression."""
    clauses: List[ErlangClause]
    after_clause: Optional[tuple] = None  # (timeout, body)
    
    def __post_init__(self):
        self.type = ErlangNodeType.RECEIVE
    
    def accept(self, visitor):
        return visitor.visit_receive(self)


@dataclass
class ErlangSend(ErlangExpression):
    """Erlang send expression (!)."""
    destination: ErlangExpression
    message: ErlangExpression
    
    def __post_init__(self):
        self.type = ErlangNodeType.SEND
    
    def accept(self, visitor):
        return visitor.visit_send(self)


# Exception handling
@dataclass
class ErlangTry(ErlangExpression):
    """Erlang try expression."""
    body: List[ErlangExpression]
    catch_clauses: List[ErlangClause] = field(default_factory=list)
    after_body: List[ErlangExpression] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = ErlangNodeType.TRY
    
    def accept(self, visitor):
        return visitor.visit_try(self)


@dataclass
class ErlangCatch(ErlangExpression):
    """Erlang catch expression."""
    expression: ErlangExpression
    
    def __post_init__(self):
        self.type = ErlangNodeType.CATCH
    
    def accept(self, visitor):
        return visitor.visit_catch(self)


@dataclass
class ErlangThrow(ErlangExpression):
    """Erlang throw expression."""
    expression: ErlangExpression
    
    def __post_init__(self):
        self.type = ErlangNodeType.THROW
    
    def accept(self, visitor):
        return visitor.visit_throw(self)


@dataclass
class ErlangBegin(ErlangExpression):
    """Erlang begin...end block."""
    body: List[ErlangExpression]
    
    def __post_init__(self):
        self.type = ErlangNodeType.BEGIN
    
    def accept(self, visitor):
        return visitor.visit_begin(self)


# Comprehensions
@dataclass
class ErlangListComprehension(ErlangExpression):
    """Erlang list comprehension."""
    expression: ErlangExpression
    generators: List[tuple]  # List of (pattern, collection) pairs
    filters: List[ErlangExpression] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = ErlangNodeType.LIST_COMPREHENSION
    
    def accept(self, visitor):
        return visitor.visit_list_comprehension(self)


@dataclass
class ErlangBinaryComprehension(ErlangExpression):
    """Erlang binary comprehension."""
    expression: ErlangExpression
    generators: List[tuple]  # List of (pattern, collection) pairs
    filters: List[ErlangExpression] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = ErlangNodeType.BINARY_COMPREHENSION
    
    def accept(self, visitor):
        return visitor.visit_binary_comprehension(self)


# Guards
@dataclass
class ErlangGuard(ErlangExpression):
    """Erlang guard expression."""
    tests: List[ErlangExpression]
    
    def __post_init__(self):
        self.type = ErlangNodeType.GUARD
    
    def accept(self, visitor):
        return visitor.visit_guard(self)


@dataclass
class ErlangGuardSequence(ErlangExpression):
    """Erlang guard sequence (multiple guards with ;)."""
    guards: List[ErlangGuard]
    
    def __post_init__(self):
        self.type = ErlangNodeType.GUARD_SEQUENCE
    
    def accept(self, visitor):
        return visitor.visit_guard_sequence(self)


# Records
@dataclass
class ErlangRecordDefinition(ErlangStatement):
    """Erlang record definition."""
    name: str
    fields: List[tuple]  # List of (field_name, default_value) pairs
    
    def __post_init__(self):
        self.type = ErlangNodeType.RECORD_DEFINITION
    
    def accept(self, visitor):
        return visitor.visit_record_definition(self)


@dataclass
class ErlangRecordAccess(ErlangExpression):
    """Erlang record field access."""
    record: ErlangExpression
    record_name: str
    field: str
    
    def __post_init__(self):
        self.type = ErlangNodeType.RECORD_ACCESS
    
    def accept(self, visitor):
        return visitor.visit_record_access(self)


@dataclass
class ErlangRecordUpdate(ErlangExpression):
    """Erlang record update."""
    record: ErlangExpression
    record_name: str
    updates: Dict[str, ErlangExpression]
    
    def __post_init__(self):
        self.type = ErlangNodeType.RECORD_UPDATE
    
    def accept(self, visitor):
        return visitor.visit_record_update(self)


# Macros
@dataclass
class ErlangMacroDefinition(ErlangStatement):
    """Erlang macro definition."""
    name: str
    parameters: List[str]
    body: ErlangExpression
    
    def __post_init__(self):
        self.type = ErlangNodeType.MACRO_DEFINITION
    
    def accept(self, visitor):
        return visitor.visit_macro_definition(self)


@dataclass
class ErlangMacroCall(ErlangExpression):
    """Erlang macro call."""
    name: str
    arguments: List[ErlangExpression]
    
    def __post_init__(self):
        self.type = ErlangNodeType.MACRO_CALL
    
    def accept(self, visitor):
        return visitor.visit_macro_call(self)


# Program
@dataclass
class ErlangProgram(ErlangNode):
    """Erlang program/module."""
    module: ErlangModule
    
    def __post_init__(self):
        self.type = ErlangNodeType.PROGRAM
    
    def accept(self, visitor):
        return visitor.visit_program(self)


# Visitor pattern
class ErlangNodeVisitor(ABC):
    """Visitor interface for Erlang AST nodes."""
    
    @abstractmethod
    def visit_atom(self, node: ErlangAtom): pass
    
    @abstractmethod
    def visit_integer(self, node: ErlangInteger): pass
    
    @abstractmethod
    def visit_float(self, node: ErlangFloat): pass
    
    @abstractmethod
    def visit_string(self, node: ErlangString): pass
    
    @abstractmethod
    def visit_binary(self, node: ErlangBinary): pass
    
    @abstractmethod
    def visit_boolean(self, node: ErlangBoolean): pass
    
    @abstractmethod
    def visit_list(self, node: ErlangList): pass
    
    @abstractmethod
    def visit_tuple(self, node: ErlangTuple): pass
    
    @abstractmethod
    def visit_map(self, node: ErlangMap): pass
    
    @abstractmethod
    def visit_record(self, node: ErlangRecord): pass
    
    @abstractmethod
    def visit_variable(self, node: ErlangVariable): pass
    
    @abstractmethod
    def visit_match(self, node: ErlangMatch): pass
    
    @abstractmethod
    def visit_binary_op(self, node: ErlangBinaryOp): pass
    
    @abstractmethod
    def visit_unary_op(self, node: ErlangUnaryOp): pass
    
    @abstractmethod
    def visit_function_call(self, node: ErlangFunctionCall): pass
    
    @abstractmethod
    def visit_pattern(self, node: ErlangPattern): pass
    
    @abstractmethod
    def visit_case(self, node: ErlangCase): pass
    
    @abstractmethod
    def visit_if(self, node: ErlangIf): pass
    
    @abstractmethod
    def visit_function(self, node: ErlangFunction): pass
    
    @abstractmethod
    def visit_clause(self, node: ErlangClause): pass
    
    @abstractmethod
    def visit_lambda(self, node: ErlangLambda): pass
    
    @abstractmethod
    def visit_module(self, node: ErlangModule): pass
    
    @abstractmethod
    def visit_attribute(self, node: ErlangAttribute): pass
    
    @abstractmethod
    def visit_export(self, node: ErlangExport): pass
    
    @abstractmethod
    def visit_import(self, node: ErlangImport): pass
    
    @abstractmethod
    def visit_spawn(self, node: ErlangSpawn): pass
    
    @abstractmethod
    def visit_receive(self, node: ErlangReceive): pass
    
    @abstractmethod
    def visit_send(self, node: ErlangSend): pass
    
    @abstractmethod
    def visit_try(self, node: ErlangTry): pass
    
    @abstractmethod
    def visit_catch(self, node: ErlangCatch): pass
    
    @abstractmethod
    def visit_throw(self, node: ErlangThrow): pass
    
    @abstractmethod
    def visit_begin(self, node: ErlangBegin): pass
    
    @abstractmethod
    def visit_list_comprehension(self, node: ErlangListComprehension): pass
    
    @abstractmethod
    def visit_binary_comprehension(self, node: ErlangBinaryComprehension): pass
    
    @abstractmethod
    def visit_guard(self, node: ErlangGuard): pass
    
    @abstractmethod
    def visit_guard_sequence(self, node: ErlangGuardSequence): pass
    
    @abstractmethod
    def visit_record_definition(self, node: ErlangRecordDefinition): pass
    
    @abstractmethod
    def visit_record_access(self, node: ErlangRecordAccess): pass
    
    @abstractmethod
    def visit_record_update(self, node: ErlangRecordUpdate): pass
    
    @abstractmethod
    def visit_macro_definition(self, node: ErlangMacroDefinition): pass
    
    @abstractmethod
    def visit_macro_call(self, node: ErlangMacroCall): pass
    
    @abstractmethod
    def visit_program(self, node: ErlangProgram): pass


# Utility functions
def erlang_atom(value: str) -> ErlangAtom:
    """Create an Erlang atom."""
    return ErlangAtom(value)


def erlang_integer(value: int) -> ErlangInteger:
    """Create an Erlang integer."""
    return ErlangInteger(value)


def erlang_float(value: float) -> ErlangFloat:
    """Create an Erlang float."""
    return ErlangFloat(value)


def erlang_string(value: str) -> ErlangString:
    """Create an Erlang string."""
    return ErlangString(value)


def erlang_boolean(value: bool) -> ErlangBoolean:
    """Create an Erlang boolean."""
    return ErlangBoolean(value)


def erlang_variable(name: str) -> ErlangVariable:
    """Create an Erlang variable."""
    return ErlangVariable(name)


def erlang_list(*elements: ErlangExpression) -> ErlangList:
    """Create an Erlang list."""
    return ErlangList(list(elements))


def erlang_tuple(*elements: ErlangExpression) -> ErlangTuple:
    """Create an Erlang tuple."""
    return ErlangTuple(list(elements))


def erlang_map(**pairs) -> ErlangMap:
    """Create an Erlang map."""
    return ErlangMap(list(pairs.items()))


def erlang_function_call(function: ErlangExpression, *args: ErlangExpression, 
                        module: Optional[ErlangExpression] = None) -> ErlangFunctionCall:
    """Create an Erlang function call."""
    return ErlangFunctionCall(module, function, list(args))


def erlang_spawn(function: ErlangExpression, *args: ErlangExpression,
                module: Optional[ErlangExpression] = None) -> ErlangSpawn:
    """Create an Erlang spawn expression."""
    return ErlangSpawn(module, function, list(args))


def erlang_send(destination: ErlangExpression, message: ErlangExpression) -> ErlangSend:
    """Create an Erlang send expression."""
    return ErlangSend(destination, message) 