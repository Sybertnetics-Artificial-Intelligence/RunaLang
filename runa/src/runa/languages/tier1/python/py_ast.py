#!/usr/bin/env python3
"""
Python AST Node Definitions

Comprehensive Abstract Syntax Tree nodes for Python covering
all language features from Python 3.8+ including type hints,
async/await, pattern matching, and modern Python constructs.
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod


class PyNodeType(Enum):
    """Python AST node types."""
    # Literals
    LITERAL = auto()
    CONSTANT = auto()
    NAME = auto()
    
    # Expressions
    BINARY_OP = auto()
    UNARY_OP = auto()
    COMPARE = auto()
    CALL = auto()
    ATTRIBUTE = auto()
    SUBSCRIPT = auto()
    SLICE = auto()
    LIST = auto()
    TUPLE = auto()
    SET = auto()
    DICT = auto()
    LIST_COMP = auto()
    SET_COMP = auto()
    DICT_COMP = auto()
    GENERATOR_EXP = auto()
    LAMBDA = auto()
    CONDITIONAL = auto()
    STARRED = auto()
    YIELD = auto()
    YIELD_FROM = auto()
    AWAIT = auto()
    NAMED_EXPR = auto()  # Walrus operator :=
    
    # Statements
    EXPRESSION_STMT = auto()
    ASSIGN = auto()
    ANN_ASSIGN = auto()  # Annotated assignment
    AUG_ASSIGN = auto()  # Augmented assignment
    RAISE = auto()
    ASSERT = auto()
    DELETE = auto()
    PASS = auto()
    BREAK = auto()
    CONTINUE = auto()
    
    # Control flow
    IF = auto()
    WHILE = auto()
    FOR = auto()
    TRY = auto()
    WITH = auto()
    MATCH = auto()  # Pattern matching (3.10+)
    
    # Functions and classes
    FUNCTION_DEF = auto()
    ASYNC_FUNCTION_DEF = auto()
    CLASS_DEF = auto()
    RETURN = auto()
    GLOBAL = auto()
    NONLOCAL = auto()
    
    # Imports
    IMPORT = auto()
    IMPORT_FROM = auto()
    
    # Module
    MODULE = auto()
    
    # Exception handling
    EXCEPT_HANDLER = auto()
    
    # Comprehensions
    COMPREHENSION = auto()
    
    # Arguments
    ARGUMENTS = auto()
    ARG = auto()
    KEYWORD = auto()
    
    # Type annotations
    TYPE_IGNORE = auto()
    TYPE_COMMENT = auto()
    
    # Pattern matching (3.10+)
    MATCH_VALUE = auto()
    MATCH_SINGLETON = auto()
    MATCH_SEQUENCE = auto()
    MATCH_MAPPING = auto()
    MATCH_CLASS = auto()
    MATCH_STAR = auto()
    MATCH_AS = auto()
    MATCH_OR = auto()
    
    # Aliases
    ALIAS = auto()


class PyOperator(Enum):
    """Python operators."""
    # Arithmetic
    ADD = "+"
    SUB = "-"
    MULT = "*"
    DIV = "/"
    MOD = "%"
    POW = "**"
    LSHIFT = "<<"
    RSHIFT = ">>"
    BITOR = "|"
    BITXOR = "^"
    BITAND = "&"
    FLOORDIV = "//"
    MATMULT = "@"  # Matrix multiplication
    
    # Comparison
    EQ = "=="
    NOT_EQ = "!="
    LT = "<"
    LTE = "<="
    GT = ">"
    GTE = ">="
    IS = "is"
    IS_NOT = "is not"
    IN = "in"
    NOT_IN = "not in"
    
    # Unary
    INVERT = "~"
    NOT = "not"
    UADD = "+"
    USUB = "-"
    
    # Boolean
    AND = "and"
    OR = "or"


class PyContext(Enum):
    """Python expression context."""
    LOAD = auto()
    STORE = auto()
    DEL = auto()


@dataclass
class PyNode(ABC):
    """Base class for all Python AST nodes."""
    type: PyNodeType = None
    lineno: Optional[int] = None
    col_offset: Optional[int] = None
    end_lineno: Optional[int] = None
    end_col_offset: Optional[int] = None
    
    @abstractmethod
    def accept(self, visitor):
        """Accept a visitor for the visitor pattern."""
        pass


@dataclass
class PyExpression(PyNode):
    """Base class for Python expressions."""
    pass


@dataclass
class PyStatement(PyNode):
    """Base class for Python statements."""
    pass


@dataclass
class PyConstant(PyExpression):
    """Python constant node."""
    value: Any
    kind: Optional[str] = None
    
    def __post_init__(self):
        self.type = PyNodeType.CONSTANT
    
    def accept(self, visitor):
        return visitor.visit_constant(self)


@dataclass
class PyName(PyExpression):
    """Python name node."""
    id: str
    ctx: PyContext = PyContext.LOAD
    
    def __post_init__(self):
        self.type = PyNodeType.NAME
    
    def accept(self, visitor):
        return visitor.visit_name(self)


@dataclass
class PyBinOp(PyExpression):
    """Python binary operation node."""
    left: PyExpression
    op: PyOperator
    right: PyExpression
    
    def __post_init__(self):
        self.type = PyNodeType.BINARY_OP
    
    def accept(self, visitor):
        return visitor.visit_binop(self)


@dataclass
class PyUnaryOp(PyExpression):
    """Python unary operation node."""
    op: PyOperator
    operand: PyExpression
    
    def __post_init__(self):
        self.type = PyNodeType.UNARY_OP
    
    def accept(self, visitor):
        return visitor.visit_unaryop(self)


@dataclass
class PyCompare(PyExpression):
    """Python comparison node."""
    left: PyExpression
    ops: List[PyOperator]
    comparators: List[PyExpression]
    
    def __post_init__(self):
        self.type = PyNodeType.COMPARE
    
    def accept(self, visitor):
        return visitor.visit_compare(self)


@dataclass
class PyCall(PyExpression):
    """Python function call node."""
    func: PyExpression
    args: List[PyExpression]
    keywords: List['PyKeyword']
    
    def __post_init__(self):
        self.type = PyNodeType.CALL
    
    def accept(self, visitor):
        return visitor.visit_call(self)


@dataclass
class PyAttribute(PyExpression):
    """Python attribute access node."""
    value: PyExpression
    attr: str
    ctx: PyContext = PyContext.LOAD
    
    def __post_init__(self):
        self.type = PyNodeType.ATTRIBUTE
    
    def accept(self, visitor):
        return visitor.visit_attribute(self)


@dataclass
class PySubscript(PyExpression):
    """Python subscript node."""
    value: PyExpression
    slice: PyExpression
    ctx: PyContext = PyContext.LOAD
    
    def __post_init__(self):
        self.type = PyNodeType.SUBSCRIPT
    
    def accept(self, visitor):
        return visitor.visit_subscript(self)


@dataclass
class PySlice(PyExpression):
    """Python slice node."""
    lower: Optional[PyExpression] = None
    upper: Optional[PyExpression] = None
    step: Optional[PyExpression] = None
    
    def __post_init__(self):
        self.type = PyNodeType.SLICE
    
    def accept(self, visitor):
        return visitor.visit_slice(self)


@dataclass
class PyList(PyExpression):
    """Python list node."""
    elts: List[PyExpression]
    ctx: PyContext = PyContext.LOAD
    
    def __post_init__(self):
        self.type = PyNodeType.LIST
    
    def accept(self, visitor):
        return visitor.visit_list(self)


@dataclass
class PyTuple(PyExpression):
    """Python tuple node."""
    elts: List[PyExpression]
    ctx: PyContext = PyContext.LOAD
    
    def __post_init__(self):
        self.type = PyNodeType.TUPLE
    
    def accept(self, visitor):
        return visitor.visit_tuple(self)


@dataclass
class PySet(PyExpression):
    """Python set node."""
    elts: List[PyExpression]
    
    def __post_init__(self):
        self.type = PyNodeType.SET
    
    def accept(self, visitor):
        return visitor.visit_set(self)


@dataclass
class PyDict(PyExpression):
    """Python dictionary node."""
    keys: List[Optional[PyExpression]]
    values: List[PyExpression]
    
    def __post_init__(self):
        self.type = PyNodeType.DICT
    
    def accept(self, visitor):
        return visitor.visit_dict(self)


@dataclass
class PyListComp(PyExpression):
    """Python list comprehension node."""
    elt: PyExpression
    generators: List['PyComprehension']
    
    def __post_init__(self):
        self.type = PyNodeType.LIST_COMP
    
    def accept(self, visitor):
        return visitor.visit_listcomp(self)


@dataclass
class PySetComp(PyExpression):
    """Python set comprehension node."""
    elt: PyExpression
    generators: List['PyComprehension']
    
    def __post_init__(self):
        self.type = PyNodeType.SET_COMP
    
    def accept(self, visitor):
        return visitor.visit_setcomp(self)


@dataclass
class PyDictComp(PyExpression):
    """Python dictionary comprehension node."""
    key: PyExpression
    value: PyExpression
    generators: List['PyComprehension']
    
    def __post_init__(self):
        self.type = PyNodeType.DICT_COMP
    
    def accept(self, visitor):
        return visitor.visit_dictcomp(self)


@dataclass
class PyGeneratorExp(PyExpression):
    """Python generator expression node."""
    elt: PyExpression
    generators: List['PyComprehension']
    
    def __post_init__(self):
        self.type = PyNodeType.GENERATOR_EXP
    
    def accept(self, visitor):
        return visitor.visit_generatorexp(self)


@dataclass
class PyLambda(PyExpression):
    """Python lambda node."""
    args: 'PyArguments'
    body: PyExpression
    
    def __post_init__(self):
        self.type = PyNodeType.LAMBDA
    
    def accept(self, visitor):
        return visitor.visit_lambda(self)


@dataclass
class PyIfExp(PyExpression):
    """Python conditional expression node."""
    test: PyExpression
    body: PyExpression
    orelse: PyExpression
    
    def __post_init__(self):
        self.type = PyNodeType.CONDITIONAL
    
    def accept(self, visitor):
        return visitor.visit_ifexp(self)


@dataclass
class PyStarred(PyExpression):
    """Python starred expression node."""
    value: PyExpression
    ctx: PyContext = PyContext.LOAD
    
    def __post_init__(self):
        self.type = PyNodeType.STARRED
    
    def accept(self, visitor):
        return visitor.visit_starred(self)


@dataclass
class PyYield(PyExpression):
    """Python yield expression node."""
    value: Optional[PyExpression] = None
    
    def __post_init__(self):
        self.type = PyNodeType.YIELD
    
    def accept(self, visitor):
        return visitor.visit_yield(self)


@dataclass
class PyYieldFrom(PyExpression):
    """Python yield from expression node."""
    value: PyExpression
    
    def __post_init__(self):
        self.type = PyNodeType.YIELD_FROM
    
    def accept(self, visitor):
        return visitor.visit_yield_from(self)


@dataclass
class PyAwait(PyExpression):
    """Python await expression node."""
    value: PyExpression
    
    def __post_init__(self):
        self.type = PyNodeType.AWAIT
    
    def accept(self, visitor):
        return visitor.visit_await(self)


@dataclass
class PyNamedExpr(PyExpression):
    """Python named expression node (walrus operator)."""
    target: PyExpression
    value: PyExpression
    
    def __post_init__(self):
        self.type = PyNodeType.NAMED_EXPR
    
    def accept(self, visitor):
        return visitor.visit_namedexpr(self)


# Statement nodes
@dataclass
class PyExpressionStmt(PyStatement):
    """Python expression statement node."""
    value: PyExpression
    
    def __post_init__(self):
        self.type = PyNodeType.EXPRESSION_STMT
    
    def accept(self, visitor):
        return visitor.visit_expr_stmt(self)


@dataclass
class PyAssign(PyStatement):
    """Python assignment statement node."""
    targets: List[PyExpression]
    value: PyExpression
    type_comment: Optional[str] = None
    
    def __post_init__(self):
        self.type = PyNodeType.ASSIGN
    
    def accept(self, visitor):
        return visitor.visit_assign(self)


@dataclass
class PyAnnAssign(PyStatement):
    """Python annotated assignment statement node."""
    target: PyExpression
    annotation: PyExpression
    value: Optional[PyExpression] = None
    simple: bool = True
    
    def __post_init__(self):
        self.type = PyNodeType.ANN_ASSIGN
    
    def accept(self, visitor):
        return visitor.visit_ann_assign(self)


@dataclass
class PyAugAssign(PyStatement):
    """Python augmented assignment statement node."""
    target: PyExpression
    op: PyOperator
    value: PyExpression
    
    def __post_init__(self):
        self.type = PyNodeType.AUG_ASSIGN
    
    def accept(self, visitor):
        return visitor.visit_aug_assign(self)


@dataclass
class PyRaise(PyStatement):
    """Python raise statement node."""
    exc: Optional[PyExpression] = None
    cause: Optional[PyExpression] = None
    
    def __post_init__(self):
        self.type = PyNodeType.RAISE
    
    def accept(self, visitor):
        return visitor.visit_raise(self)


@dataclass
class PyAssert(PyStatement):
    """Python assert statement node."""
    test: PyExpression
    msg: Optional[PyExpression] = None
    
    def __post_init__(self):
        self.type = PyNodeType.ASSERT
    
    def accept(self, visitor):
        return visitor.visit_assert(self)


@dataclass
class PyDelete(PyStatement):
    """Python delete statement node."""
    targets: List[PyExpression]
    
    def __post_init__(self):
        self.type = PyNodeType.DELETE
    
    def accept(self, visitor):
        return visitor.visit_delete(self)


@dataclass
class PyPass(PyStatement):
    """Python pass statement node."""
    
    def __post_init__(self):
        self.type = PyNodeType.PASS
    
    def accept(self, visitor):
        return visitor.visit_pass(self)


@dataclass
class PyBreak(PyStatement):
    """Python break statement node."""
    
    def __post_init__(self):
        self.type = PyNodeType.BREAK
    
    def accept(self, visitor):
        return visitor.visit_break(self)


@dataclass
class PyContinue(PyStatement):
    """Python continue statement node."""
    
    def __post_init__(self):
        self.type = PyNodeType.CONTINUE
    
    def accept(self, visitor):
        return visitor.visit_continue(self)


@dataclass
class PyIf(PyStatement):
    """Python if statement node."""
    test: PyExpression
    body: List[PyStatement]
    orelse: List[PyStatement]
    
    def __post_init__(self):
        self.type = PyNodeType.IF
    
    def accept(self, visitor):
        return visitor.visit_if(self)


@dataclass
class PyWhile(PyStatement):
    """Python while statement node."""
    test: PyExpression
    body: List[PyStatement]
    orelse: List[PyStatement]
    
    def __post_init__(self):
        self.type = PyNodeType.WHILE
    
    def accept(self, visitor):
        return visitor.visit_while(self)


@dataclass
class PyFor(PyStatement):
    """Python for statement node."""
    target: PyExpression
    iter: PyExpression
    body: List[PyStatement]
    orelse: List[PyStatement]
    type_comment: Optional[str] = None
    
    def __post_init__(self):
        self.type = PyNodeType.FOR
    
    def accept(self, visitor):
        return visitor.visit_for(self)


@dataclass
class PyTry(PyStatement):
    """Python try statement node."""
    body: List[PyStatement]
    handlers: List['PyExceptHandler']
    orelse: List[PyStatement]
    finalbody: List[PyStatement]
    
    def __post_init__(self):
        self.type = PyNodeType.TRY
    
    def accept(self, visitor):
        return visitor.visit_try(self)


@dataclass
class PyWith(PyStatement):
    """Python with statement node."""
    items: List['PyWithItem']
    body: List[PyStatement]
    type_comment: Optional[str] = None
    
    def __post_init__(self):
        self.type = PyNodeType.WITH
    
    def accept(self, visitor):
        return visitor.visit_with(self)


@dataclass
class PyFunctionDef(PyStatement):
    """Python function definition node."""
    name: str
    args: 'PyArguments'
    body: List[PyStatement]
    decorator_list: List[PyExpression]
    returns: Optional[PyExpression] = None
    type_comment: Optional[str] = None
    
    def __post_init__(self):
        self.type = PyNodeType.FUNCTION_DEF
    
    def accept(self, visitor):
        return visitor.visit_functiondef(self)


@dataclass
class PyAsyncFunctionDef(PyStatement):
    """Python async function definition node."""
    name: str
    args: 'PyArguments'
    body: List[PyStatement]
    decorator_list: List[PyExpression]
    returns: Optional[PyExpression] = None
    type_comment: Optional[str] = None
    
    def __post_init__(self):
        self.type = PyNodeType.ASYNC_FUNCTION_DEF
    
    def accept(self, visitor):
        return visitor.visit_async_functiondef(self)


@dataclass
class PyClassDef(PyStatement):
    """Python class definition node."""
    name: str
    bases: List[PyExpression]
    keywords: List['PyKeyword']
    body: List[PyStatement]
    decorator_list: List[PyExpression]
    
    def __post_init__(self):
        self.type = PyNodeType.CLASS_DEF
    
    def accept(self, visitor):
        return visitor.visit_classdef(self)


@dataclass
class PyReturn(PyStatement):
    """Python return statement node."""
    value: Optional[PyExpression] = None
    
    def __post_init__(self):
        self.type = PyNodeType.RETURN
    
    def accept(self, visitor):
        return visitor.visit_return(self)


@dataclass
class PyGlobal(PyStatement):
    """Python global statement node."""
    names: List[str]
    
    def __post_init__(self):
        self.type = PyNodeType.GLOBAL
    
    def accept(self, visitor):
        return visitor.visit_global(self)


@dataclass
class PyNonlocal(PyStatement):
    """Python nonlocal statement node."""
    names: List[str]
    
    def __post_init__(self):
        self.type = PyNodeType.NONLOCAL
    
    def accept(self, visitor):
        return visitor.visit_nonlocal(self)


@dataclass
class PyImport(PyStatement):
    """Python import statement node."""
    names: List['PyAlias']
    
    def __post_init__(self):
        self.type = PyNodeType.IMPORT
    
    def accept(self, visitor):
        return visitor.visit_import(self)


@dataclass
class PyImportFrom(PyStatement):
    """Python import from statement node."""
    module: Optional[str]
    names: List['PyAlias']
    level: int = 0
    
    def __post_init__(self):
        self.type = PyNodeType.IMPORT_FROM
    
    def accept(self, visitor):
        return visitor.visit_import_from(self)


@dataclass
class PyModule(PyNode):
    """Python module node."""
    body: List[PyStatement]
    type_ignores: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = PyNodeType.MODULE
    
    def accept(self, visitor):
        return visitor.visit_module(self)


# Helper nodes
@dataclass
class PyExceptHandler(PyNode):
    """Python exception handler node."""
    type: Optional[PyExpression] = None
    name: Optional[str] = None
    body: List[PyStatement] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = PyNodeType.EXCEPT_HANDLER
    
    def accept(self, visitor):
        return visitor.visit_excepthandler(self)


@dataclass
class PyWithItem(PyNode):
    """Python with item node."""
    context_expr: PyExpression
    optional_vars: Optional[PyExpression] = None
    
    def accept(self, visitor):
        return visitor.visit_withitem(self)


@dataclass
class PyArguments(PyNode):
    """Python arguments node."""
    posonlyargs: List['PyArg'] = field(default_factory=list)
    args: List['PyArg'] = field(default_factory=list)
    vararg: Optional['PyArg'] = None
    kwonlyargs: List['PyArg'] = field(default_factory=list)
    kw_defaults: List[Optional[PyExpression]] = field(default_factory=list)
    kwarg: Optional['PyArg'] = None
    defaults: List[PyExpression] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = PyNodeType.ARGUMENTS
    
    def accept(self, visitor):
        return visitor.visit_arguments(self)


@dataclass
class PyArg(PyNode):
    """Python argument node."""
    arg: str
    annotation: Optional[PyExpression] = None
    type_comment: Optional[str] = None
    
    def __post_init__(self):
        self.type = PyNodeType.ARG
    
    def accept(self, visitor):
        return visitor.visit_arg(self)


@dataclass
class PyKeyword(PyNode):
    """Python keyword argument node."""
    arg: Optional[str]
    value: PyExpression
    
    def __post_init__(self):
        self.type = PyNodeType.KEYWORD
    
    def accept(self, visitor):
        return visitor.visit_keyword(self)


@dataclass
class PyAlias(PyNode):
    """Python alias node."""
    name: str
    asname: Optional[str] = None
    
    def __post_init__(self):
        self.type = PyNodeType.ALIAS
    
    def accept(self, visitor):
        return visitor.visit_alias(self)


@dataclass
class PyComprehension(PyNode):
    """Python comprehension node."""
    target: PyExpression
    iter: PyExpression
    ifs: List[PyExpression]
    is_async: bool = False
    
    def __post_init__(self):
        self.type = PyNodeType.COMPREHENSION
    
    def accept(self, visitor):
        return visitor.visit_comprehension(self)


class PyNodeVisitor(ABC):
    """Abstract base class for Python AST visitors."""
    
    @abstractmethod
    def visit_constant(self, node: PyConstant): pass
    
    @abstractmethod
    def visit_name(self, node: PyName): pass
    
    @abstractmethod
    def visit_binop(self, node: PyBinOp): pass
    
    @abstractmethod
    def visit_unaryop(self, node: PyUnaryOp): pass
    
    @abstractmethod
    def visit_compare(self, node: PyCompare): pass
    
    @abstractmethod
    def visit_call(self, node: PyCall): pass
    
    @abstractmethod
    def visit_attribute(self, node: PyAttribute): pass
    
    @abstractmethod
    def visit_subscript(self, node: PySubscript): pass
    
    @abstractmethod
    def visit_slice(self, node: PySlice): pass
    
    @abstractmethod
    def visit_list(self, node: PyList): pass
    
    @abstractmethod
    def visit_tuple(self, node: PyTuple): pass
    
    @abstractmethod
    def visit_set(self, node: PySet): pass
    
    @abstractmethod
    def visit_dict(self, node: PyDict): pass
    
    @abstractmethod
    def visit_listcomp(self, node: PyListComp): pass
    
    @abstractmethod
    def visit_setcomp(self, node: PySetComp): pass
    
    @abstractmethod
    def visit_dictcomp(self, node: PyDictComp): pass
    
    @abstractmethod
    def visit_generatorexp(self, node: PyGeneratorExp): pass
    
    @abstractmethod
    def visit_lambda(self, node: PyLambda): pass
    
    @abstractmethod
    def visit_ifexp(self, node: PyIfExp): pass
    
    @abstractmethod
    def visit_starred(self, node: PyStarred): pass
    
    @abstractmethod
    def visit_yield(self, node: PyYield): pass
    
    @abstractmethod
    def visit_yield_from(self, node: PyYieldFrom): pass
    
    @abstractmethod
    def visit_await(self, node: PyAwait): pass
    
    @abstractmethod
    def visit_namedexpr(self, node: PyNamedExpr): pass
    
    @abstractmethod
    def visit_expr_stmt(self, node: PyExpressionStmt): pass
    
    @abstractmethod
    def visit_assign(self, node: PyAssign): pass
    
    @abstractmethod
    def visit_ann_assign(self, node: PyAnnAssign): pass
    
    @abstractmethod
    def visit_aug_assign(self, node: PyAugAssign): pass
    
    @abstractmethod
    def visit_raise(self, node: PyRaise): pass
    
    @abstractmethod
    def visit_assert(self, node: PyAssert): pass
    
    @abstractmethod
    def visit_delete(self, node: PyDelete): pass
    
    @abstractmethod
    def visit_pass(self, node: PyPass): pass
    
    @abstractmethod
    def visit_break(self, node: PyBreak): pass
    
    @abstractmethod
    def visit_continue(self, node: PyContinue): pass
    
    @abstractmethod
    def visit_if(self, node: PyIf): pass
    
    @abstractmethod
    def visit_while(self, node: PyWhile): pass
    
    @abstractmethod
    def visit_for(self, node: PyFor): pass
    
    @abstractmethod
    def visit_try(self, node: PyTry): pass
    
    @abstractmethod
    def visit_with(self, node: PyWith): pass
    
    @abstractmethod
    def visit_functiondef(self, node: PyFunctionDef): pass
    
    @abstractmethod
    def visit_async_functiondef(self, node: PyAsyncFunctionDef): pass
    
    @abstractmethod
    def visit_classdef(self, node: PyClassDef): pass
    
    @abstractmethod
    def visit_return(self, node: PyReturn): pass
    
    @abstractmethod
    def visit_global(self, node: PyGlobal): pass
    
    @abstractmethod
    def visit_nonlocal(self, node: PyNonlocal): pass
    
    @abstractmethod
    def visit_import(self, node: PyImport): pass
    
    @abstractmethod
    def visit_import_from(self, node: PyImportFrom): pass
    
    @abstractmethod
    def visit_module(self, node: PyModule): pass
    
    @abstractmethod
    def visit_excepthandler(self, node: PyExceptHandler): pass
    
    @abstractmethod
    def visit_withitem(self, node: PyWithItem): pass
    
    @abstractmethod
    def visit_arguments(self, node: PyArguments): pass
    
    @abstractmethod
    def visit_arg(self, node: PyArg): pass
    
    @abstractmethod
    def visit_keyword(self, node: PyKeyword): pass
    
    @abstractmethod
    def visit_alias(self, node: PyAlias): pass
    
    @abstractmethod
    def visit_comprehension(self, node: PyComprehension): pass