#!/usr/bin/env python3
"""
Elixir Abstract Syntax Tree (AST) Module

This module defines the complete AST structure for the Elixir programming language,
supporting all major language constructs including:
- Pattern matching and guards
- Pipe operator and function composition
- Actor model with processes and message passing
- Modules, functions, and protocols
- Macros and metaprogramming
- GenServer and OTP patterns
- Exception handling and supervisors
- Comprehensions and streams
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass

# Node type enumeration
class ElixirNodeType(Enum):
    # Literals
    ATOM = "atom"
    INTEGER = "integer"
    FLOAT = "float"
    STRING = "string"
    BINARY = "binary"
    BOOLEAN = "boolean"
    NIL = "nil"
    
    # Collections
    LIST = "list"
    TUPLE = "tuple"
    MAP = "map"
    KEYWORD_LIST = "keyword_list"
    
    # Variables and patterns
    VARIABLE = "variable"
    PATTERN = "pattern"
    PIN = "pin"
    
    # Expressions
    MATCH = "match"
    PIPE = "pipe"
    BINARY_OP = "binary_op"
    UNARY_OP = "unary_op"
    FUNCTION_CALL = "function_call"
    REMOTE_CALL = "remote_call"
    CASE = "case"
    COND = "cond"
    IF = "if"
    UNLESS = "unless"
    WITH = "with"
    
    # Functions and modules
    FUNCTION = "function"
    FUNCTION_CLAUSE = "function_clause"
    ANONYMOUS_FUNCTION = "anonymous_function"
    MODULE = "module"
    
    # Definitions and declarations
    DEF = "def"
    DEFP = "defp"
    DEFMACRO = "defmacro"
    DEFMACROP = "defmacrop"
    DEFMODULE = "defmodule"
    DEFPROTOCOL = "defprotocol"
    DEFIMPL = "defimpl"
    DEFSTRUCT = "defstruct"
    DEFEXCEPTION = "defexception"
    
    # Control flow
    DO_BLOCK = "do_block"
    TRY = "try"
    CATCH = "catch"
    RESCUE = "rescue"
    AFTER = "after"
    THROW = "throw"
    RAISE = "raise"
    
    # Processes and concurrency
    SPAWN = "spawn"
    SEND = "send"
    RECEIVE = "receive"
    PROCESS = "process"
    
    # Comprehensions
    FOR_COMPREHENSION = "for_comprehension"
    
    # Guards and when
    GUARD = "guard"
    WHEN = "when"
    
    # Aliases and imports
    ALIAS = "alias"
    IMPORT = "import"
    REQUIRE = "require"
    USE = "use"
    
    # Attributes
    MODULE_ATTRIBUTE = "module_attribute"
    
    # Macros
    QUOTE = "quote"
    UNQUOTE = "unquote"
    UNQUOTE_SPLICING = "unquote_splicing"
    
    # Program
    PROGRAM = "program"

@dataclass
class ElixirNode(ABC):
    """Base class for all Elixir AST nodes."""
    node_type: ElixirNodeType
    line_number: Optional[int] = None
    column_number: Optional[int] = None
    
    @abstractmethod
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        """Accept a visitor for the visitor pattern."""
        pass

@dataclass
class ElixirExpression(ElixirNode):
    """Base class for Elixir expressions."""
    pass

@dataclass
class ElixirStatement(ElixirNode):
    """Base class for Elixir statements."""
    pass

# Literals

@dataclass
class ElixirAtom(ElixirExpression):
    """Elixir atom literal (:atom)."""
    value: str
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.ATOM
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_atom(self)

@dataclass
class ElixirInteger(ElixirExpression):
    """Elixir integer literal."""
    value: int
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.INTEGER
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_integer(self)

@dataclass
class ElixirFloat(ElixirExpression):
    """Elixir float literal."""
    value: float
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.FLOAT
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_float(self)

@dataclass
class ElixirString(ElixirExpression):
    """Elixir string literal."""
    value: str
    interpolated: bool = False
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.STRING
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_string(self)

@dataclass
class ElixirBinary(ElixirExpression):
    """Elixir binary literal."""
    value: bytes
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.BINARY
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_binary(self)

@dataclass
class ElixirBoolean(ElixirExpression):
    """Elixir boolean literal."""
    value: bool
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.BOOLEAN
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_boolean(self)

@dataclass
class ElixirNil(ElixirExpression):
    """Elixir nil literal."""
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.NIL
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_nil(self)

# Collections

@dataclass
class ElixirList(ElixirExpression):
    """Elixir list [1, 2, 3]."""
    elements: List[ElixirExpression]
    tail: Optional[ElixirExpression] = None  # For [head | tail] syntax
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.LIST
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_list(self)

@dataclass
class ElixirTuple(ElixirExpression):
    """Elixir tuple {1, 2, 3}."""
    elements: List[ElixirExpression]
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.TUPLE
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_tuple(self)

@dataclass
class ElixirMap(ElixirExpression):
    """Elixir map %{key: value}."""
    pairs: List[tuple[ElixirExpression, ElixirExpression]]
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.MAP
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_map(self)

@dataclass
class ElixirKeywordList(ElixirExpression):
    """Elixir keyword list [key: value]."""
    pairs: List[tuple[ElixirAtom, ElixirExpression]]
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.KEYWORD_LIST
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_keyword_list(self)

# Variables and patterns

@dataclass
class ElixirVariable(ElixirExpression):
    """Elixir variable."""
    name: str
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.VARIABLE
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_variable(self)

@dataclass
class ElixirPattern(ElixirExpression):
    """Elixir pattern for pattern matching."""
    pattern: ElixirExpression
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.PATTERN
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_pattern(self)

@dataclass
class ElixirPin(ElixirExpression):
    """Elixir pin operator ^variable."""
    variable: ElixirVariable
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.PIN
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_pin(self)

# Expressions

@dataclass
class ElixirMatch(ElixirExpression):
    """Elixir match expression pattern = expression."""
    left: ElixirExpression
    right: ElixirExpression
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.MATCH
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_match(self)

@dataclass
class ElixirPipe(ElixirExpression):
    """Elixir pipe operator |>."""
    left: ElixirExpression
    right: ElixirExpression
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.PIPE
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_pipe(self)

@dataclass
class ElixirBinaryOp(ElixirExpression):
    """Elixir binary operation."""
    left: ElixirExpression
    operator: str
    right: ElixirExpression
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.BINARY_OP
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_binary_op(self)

@dataclass
class ElixirUnaryOp(ElixirExpression):
    """Elixir unary operation."""
    operator: str
    operand: ElixirExpression
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.UNARY_OP
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_unary_op(self)

@dataclass
class ElixirFunctionCall(ElixirExpression):
    """Elixir function call function(args)."""
    function: str
    args: List[ElixirExpression]
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.FUNCTION_CALL
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_function_call(self)

@dataclass
class ElixirRemoteCall(ElixirExpression):
    """Elixir remote call Module.function(args)."""
    module: ElixirExpression
    function: str
    args: List[ElixirExpression]
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.REMOTE_CALL
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_remote_call(self)

@dataclass
class ElixirCase(ElixirExpression):
    """Elixir case expression."""
    expr: ElixirExpression
    clauses: List['ElixirClause']
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.CASE
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_case(self)

@dataclass
class ElixirCond(ElixirExpression):
    """Elixir cond expression."""
    clauses: List['ElixirClause']
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.COND
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_cond(self)

@dataclass
class ElixirIf(ElixirExpression):
    """Elixir if expression."""
    condition: ElixirExpression
    then_branch: ElixirExpression
    else_branch: Optional[ElixirExpression] = None
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.IF
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_if(self)

@dataclass
class ElixirUnless(ElixirExpression):
    """Elixir unless expression."""
    condition: ElixirExpression
    then_branch: ElixirExpression
    else_branch: Optional[ElixirExpression] = None
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.UNLESS
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_unless(self)

@dataclass
class ElixirWith(ElixirExpression):
    """Elixir with expression."""
    clauses: List['ElixirClause']
    do_block: ElixirExpression
    else_block: Optional[ElixirExpression] = None
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.WITH
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_with(self)

# Function and module constructs

@dataclass
class ElixirClause(ElixirNode):
    """Elixir function clause or case clause."""
    pattern: Optional[ElixirExpression]
    guard: Optional['ElixirGuard']
    body: ElixirExpression
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.FUNCTION_CLAUSE
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_clause(self)

@dataclass
class ElixirFunction(ElixirStatement):
    """Elixir function definition."""
    name: str
    arity: int
    clauses: List[ElixirClause]
    private: bool = False
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.FUNCTION
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_function(self)

@dataclass
class ElixirAnonymousFunction(ElixirExpression):
    """Elixir anonymous function fn -> end."""
    clauses: List[ElixirClause]
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.ANONYMOUS_FUNCTION
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_anonymous_function(self)

@dataclass
class ElixirModule(ElixirStatement):
    """Elixir module definition."""
    name: str
    body: List[ElixirStatement]
    attributes: List['ElixirModuleAttribute'] = None
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.MODULE
        if self.attributes is None:
            self.attributes = []
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_module(self)

# Definitions

@dataclass
class ElixirDef(ElixirStatement):
    """Elixir def definition."""
    function: ElixirFunction
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.DEF
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_def(self)

@dataclass
class ElixirDefp(ElixirStatement):
    """Elixir defp (private function) definition."""
    function: ElixirFunction
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.DEFP
        self.function.private = True
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_defp(self)

@dataclass
class ElixirDefmacro(ElixirStatement):
    """Elixir defmacro definition."""
    function: ElixirFunction
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.DEFMACRO
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_defmacro(self)

@dataclass
class ElixirDefmodule(ElixirStatement):
    """Elixir defmodule definition."""
    module: ElixirModule
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.DEFMODULE
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_defmodule(self)

@dataclass
class ElixirDefstruct(ElixirStatement):
    """Elixir defstruct definition."""
    fields: List[Union[ElixirAtom, tuple[ElixirAtom, ElixirExpression]]]
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.DEFSTRUCT
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_defstruct(self)

# Control flow

@dataclass
class ElixirDoBlock(ElixirExpression):
    """Elixir do block."""
    body: List[ElixirExpression]
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.DO_BLOCK
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_do_block(self)

@dataclass
class ElixirTry(ElixirExpression):
    """Elixir try expression."""
    body: ElixirExpression
    rescue_clauses: List[ElixirClause] = None
    catch_clauses: List[ElixirClause] = None
    else_clauses: List[ElixirClause] = None
    after_block: Optional[ElixirExpression] = None
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.TRY
        if self.rescue_clauses is None:
            self.rescue_clauses = []
        if self.catch_clauses is None:
            self.catch_clauses = []
        if self.else_clauses is None:
            self.else_clauses = []
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_try(self)

@dataclass
class ElixirRaise(ElixirExpression):
    """Elixir raise expression."""
    exception: Optional[ElixirExpression] = None
    message: Optional[ElixirExpression] = None
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.RAISE
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_raise(self)

@dataclass
class ElixirThrow(ElixirExpression):
    """Elixir throw expression."""
    value: ElixirExpression
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.THROW
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_throw(self)

# Processes and concurrency

@dataclass
class ElixirSpawn(ElixirExpression):
    """Elixir spawn expression."""
    function: ElixirExpression
    args: List[ElixirExpression] = None
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.SPAWN
        if self.args is None:
            self.args = []
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_spawn(self)

@dataclass
class ElixirSend(ElixirExpression):
    """Elixir send expression pid <- message."""
    destination: ElixirExpression
    message: ElixirExpression
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.SEND
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_send(self)

@dataclass
class ElixirReceive(ElixirExpression):
    """Elixir receive expression."""
    clauses: List[ElixirClause]
    after_clause: Optional[tuple[ElixirExpression, ElixirExpression]] = None
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.RECEIVE
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_receive(self)

# Comprehensions

@dataclass
class ElixirForComprehension(ElixirExpression):
    """Elixir for comprehension."""
    generators: List[tuple[ElixirExpression, ElixirExpression]]
    filters: List[ElixirExpression] = None
    body: ElixirExpression = None
    into: Optional[ElixirExpression] = None
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.FOR_COMPREHENSION
        if self.filters is None:
            self.filters = []
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_for_comprehension(self)

# Guards

@dataclass
class ElixirGuard(ElixirExpression):
    """Elixir guard expression."""
    conditions: List[ElixirExpression]
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.GUARD
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_guard(self)

@dataclass
class ElixirWhen(ElixirExpression):
    """Elixir when clause."""
    expression: ElixirExpression
    guard: ElixirGuard
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.WHEN
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_when(self)

# Aliases and imports

@dataclass
class ElixirAlias(ElixirStatement):
    """Elixir alias statement."""
    module: ElixirExpression
    alias: Optional[str] = None
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.ALIAS
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_alias(self)

@dataclass
class ElixirImport(ElixirStatement):
    """Elixir import statement."""
    module: ElixirExpression
    only: Optional[List[tuple[str, int]]] = None
    except_: Optional[List[tuple[str, int]]] = None
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.IMPORT
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_import(self)

@dataclass
class ElixirRequire(ElixirStatement):
    """Elixir require statement."""
    module: ElixirExpression
    alias: Optional[str] = None
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.REQUIRE
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_require(self)

@dataclass
class ElixirUse(ElixirStatement):
    """Elixir use statement."""
    module: ElixirExpression
    options: List[ElixirExpression] = None
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.USE
        if self.options is None:
            self.options = []
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_use(self)

# Attributes

@dataclass
class ElixirModuleAttribute(ElixirStatement):
    """Elixir module attribute @attr value."""
    name: str
    value: Optional[ElixirExpression] = None
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.MODULE_ATTRIBUTE
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_module_attribute(self)

# Macros

@dataclass
class ElixirQuote(ElixirExpression):
    """Elixir quote expression."""
    expression: ElixirExpression
    options: List[ElixirExpression] = None
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.QUOTE
        if self.options is None:
            self.options = []
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_quote(self)

@dataclass
class ElixirUnquote(ElixirExpression):
    """Elixir unquote expression."""
    expression: ElixirExpression
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.UNQUOTE
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_unquote(self)

@dataclass
class ElixirUnquoteSplicing(ElixirExpression):
    """Elixir unquote_splicing expression."""
    expression: ElixirExpression
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.UNQUOTE_SPLICING
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_unquote_splicing(self)

# Program

@dataclass
class ElixirProgram(ElixirNode):
    """Elixir program (top-level module)."""
    statements: List[ElixirStatement]
    
    def __post_init__(self):
        self.node_type = ElixirNodeType.PROGRAM
    
    def accept(self, visitor: 'ElixirNodeVisitor') -> Any:
        return visitor.visit_program(self)

# Visitor pattern

class ElixirNodeVisitor(ABC):
    """Abstract visitor for Elixir AST nodes."""
    
    @abstractmethod
    def visit_atom(self, node: ElixirAtom) -> Any: pass
    
    @abstractmethod
    def visit_integer(self, node: ElixirInteger) -> Any: pass
    
    @abstractmethod
    def visit_float(self, node: ElixirFloat) -> Any: pass
    
    @abstractmethod
    def visit_string(self, node: ElixirString) -> Any: pass
    
    @abstractmethod
    def visit_binary(self, node: ElixirBinary) -> Any: pass
    
    @abstractmethod
    def visit_boolean(self, node: ElixirBoolean) -> Any: pass
    
    @abstractmethod
    def visit_nil(self, node: ElixirNil) -> Any: pass
    
    @abstractmethod
    def visit_list(self, node: ElixirList) -> Any: pass
    
    @abstractmethod
    def visit_tuple(self, node: ElixirTuple) -> Any: pass
    
    @abstractmethod
    def visit_map(self, node: ElixirMap) -> Any: pass
    
    @abstractmethod
    def visit_keyword_list(self, node: ElixirKeywordList) -> Any: pass
    
    @abstractmethod
    def visit_variable(self, node: ElixirVariable) -> Any: pass
    
    @abstractmethod
    def visit_pattern(self, node: ElixirPattern) -> Any: pass
    
    @abstractmethod
    def visit_pin(self, node: ElixirPin) -> Any: pass
    
    @abstractmethod
    def visit_match(self, node: ElixirMatch) -> Any: pass
    
    @abstractmethod
    def visit_pipe(self, node: ElixirPipe) -> Any: pass
    
    @abstractmethod
    def visit_binary_op(self, node: ElixirBinaryOp) -> Any: pass
    
    @abstractmethod
    def visit_unary_op(self, node: ElixirUnaryOp) -> Any: pass
    
    @abstractmethod
    def visit_function_call(self, node: ElixirFunctionCall) -> Any: pass
    
    @abstractmethod
    def visit_remote_call(self, node: ElixirRemoteCall) -> Any: pass
    
    @abstractmethod
    def visit_case(self, node: ElixirCase) -> Any: pass
    
    @abstractmethod
    def visit_cond(self, node: ElixirCond) -> Any: pass
    
    @abstractmethod
    def visit_if(self, node: ElixirIf) -> Any: pass
    
    @abstractmethod
    def visit_unless(self, node: ElixirUnless) -> Any: pass
    
    @abstractmethod
    def visit_with(self, node: ElixirWith) -> Any: pass
    
    @abstractmethod
    def visit_clause(self, node: ElixirClause) -> Any: pass
    
    @abstractmethod
    def visit_function(self, node: ElixirFunction) -> Any: pass
    
    @abstractmethod
    def visit_anonymous_function(self, node: ElixirAnonymousFunction) -> Any: pass
    
    @abstractmethod
    def visit_module(self, node: ElixirModule) -> Any: pass
    
    @abstractmethod
    def visit_def(self, node: ElixirDef) -> Any: pass
    
    @abstractmethod
    def visit_defp(self, node: ElixirDefp) -> Any: pass
    
    @abstractmethod
    def visit_defmacro(self, node: ElixirDefmacro) -> Any: pass
    
    @abstractmethod
    def visit_defmodule(self, node: ElixirDefmodule) -> Any: pass
    
    @abstractmethod
    def visit_defstruct(self, node: ElixirDefstruct) -> Any: pass
    
    @abstractmethod
    def visit_do_block(self, node: ElixirDoBlock) -> Any: pass
    
    @abstractmethod
    def visit_try(self, node: ElixirTry) -> Any: pass
    
    @abstractmethod
    def visit_raise(self, node: ElixirRaise) -> Any: pass
    
    @abstractmethod
    def visit_throw(self, node: ElixirThrow) -> Any: pass
    
    @abstractmethod
    def visit_spawn(self, node: ElixirSpawn) -> Any: pass
    
    @abstractmethod
    def visit_send(self, node: ElixirSend) -> Any: pass
    
    @abstractmethod
    def visit_receive(self, node: ElixirReceive) -> Any: pass
    
    @abstractmethod
    def visit_for_comprehension(self, node: ElixirForComprehension) -> Any: pass
    
    @abstractmethod
    def visit_guard(self, node: ElixirGuard) -> Any: pass
    
    @abstractmethod
    def visit_when(self, node: ElixirWhen) -> Any: pass
    
    @abstractmethod
    def visit_alias(self, node: ElixirAlias) -> Any: pass
    
    @abstractmethod
    def visit_import(self, node: ElixirImport) -> Any: pass
    
    @abstractmethod
    def visit_require(self, node: ElixirRequire) -> Any: pass
    
    @abstractmethod
    def visit_use(self, node: ElixirUse) -> Any: pass
    
    @abstractmethod
    def visit_module_attribute(self, node: ElixirModuleAttribute) -> Any: pass
    
    @abstractmethod
    def visit_quote(self, node: ElixirQuote) -> Any: pass
    
    @abstractmethod
    def visit_unquote(self, node: ElixirUnquote) -> Any: pass
    
    @abstractmethod
    def visit_unquote_splicing(self, node: ElixirUnquoteSplicing) -> Any: pass
    
    @abstractmethod
    def visit_program(self, node: ElixirProgram) -> Any: pass

# Helper utility functions

def elixir_atom(value: str) -> ElixirAtom:
    """Create an Elixir atom."""
    return ElixirAtom(node_type=ElixirNodeType.ATOM, value=value)

def elixir_integer(value: int) -> ElixirInteger:
    """Create an Elixir integer."""
    return ElixirInteger(node_type=ElixirNodeType.INTEGER, value=value)

def elixir_float(value: float) -> ElixirFloat:
    """Create an Elixir float."""
    return ElixirFloat(node_type=ElixirNodeType.FLOAT, value=value)

def elixir_string(value: str, interpolated: bool = False) -> ElixirString:
    """Create an Elixir string."""
    return ElixirString(node_type=ElixirNodeType.STRING, value=value, interpolated=interpolated)

def elixir_boolean(value: bool) -> ElixirBoolean:
    """Create an Elixir boolean."""
    return ElixirBoolean(node_type=ElixirNodeType.BOOLEAN, value=value)

def elixir_nil() -> ElixirNil:
    """Create an Elixir nil."""
    return ElixirNil(node_type=ElixirNodeType.NIL)

def elixir_variable(name: str) -> ElixirVariable:
    """Create an Elixir variable."""
    return ElixirVariable(node_type=ElixirNodeType.VARIABLE, name=name)

def elixir_list(*elements: ElixirExpression, tail: Optional[ElixirExpression] = None) -> ElixirList:
    """Create an Elixir list."""
    return ElixirList(node_type=ElixirNodeType.LIST, elements=list(elements), tail=tail)

def elixir_tuple(*elements: ElixirExpression) -> ElixirTuple:
    """Create an Elixir tuple."""
    return ElixirTuple(node_type=ElixirNodeType.TUPLE, elements=list(elements))

def elixir_map(**pairs) -> ElixirMap:
    """Create an Elixir map."""
    map_pairs = []
    for key, value in pairs.items():
        if isinstance(key, str):
            key_expr = elixir_atom(key)
        else:
            key_expr = key
        map_pairs.append((key_expr, value))
    return ElixirMap(node_type=ElixirNodeType.MAP, pairs=map_pairs)

def elixir_function_call(function: str, *args: ElixirExpression) -> ElixirFunctionCall:
    """Create an Elixir function call."""
    return ElixirFunctionCall(node_type=ElixirNodeType.FUNCTION_CALL, function=function, args=list(args))

def elixir_remote_call(module: ElixirExpression, function: str, *args: ElixirExpression) -> ElixirRemoteCall:
    """Create an Elixir remote call."""
    return ElixirRemoteCall(node_type=ElixirNodeType.REMOTE_CALL, module=module, function=function, args=list(args))

def elixir_pipe(left: ElixirExpression, right: ElixirExpression) -> ElixirPipe:
    """Create an Elixir pipe operation."""
    return ElixirPipe(node_type=ElixirNodeType.PIPE, left=left, right=right)

def elixir_spawn(function: ElixirExpression, *args: ElixirExpression) -> ElixirSpawn:
    """Create an Elixir spawn expression."""
    return ElixirSpawn(node_type=ElixirNodeType.SPAWN, function=function, args=list(args))

def elixir_send(destination: ElixirExpression, message: ElixirExpression) -> ElixirSend:
    """Create an Elixir send expression."""
    return ElixirSend(node_type=ElixirNodeType.SEND, destination=destination, message=message) 