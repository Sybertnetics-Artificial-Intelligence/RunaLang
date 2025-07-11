#!/usr/bin/env python3
"""
LISP AST Node Definitions

Comprehensive Abstract Syntax Tree nodes for LISP covering
classical S-expressions, functional programming constructs,
and traditional LISP language features.
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod


class LispNodeType(Enum):
    """LISP AST node types."""
    # Atoms
    ATOM = auto()
    SYMBOL = auto()
    NUMBER = auto()
    STRING = auto()
    NIL = auto()
    T = auto()  # True in LISP
    
    # Lists and structures
    LIST = auto()
    CONS = auto()
    QUOTE = auto()
    
    # Special forms
    DEFUN = auto()
    LAMBDA = auto()
    LET = auto()
    SETQ = auto()
    IF = auto()
    COND = auto()
    PROGN = auto()
    WHEN = auto()
    UNLESS = auto()
    
    # Built-in functions
    CAR = auto()
    CDR = auto()
    CONS_FUNC = auto()
    EQ = auto()
    EQUAL = auto()
    ATOM_FUNC = auto()
    LISTP = auto()
    
    # Control flow
    LOOP = auto()
    RETURN = auto()
    GO = auto()
    TAGBODY = auto()
    
    # Macros
    DEFMACRO = auto()
    MACRO_CALL = auto()
    
    # Module/Package
    PROGRAM = auto()


class LispSpecialForm(Enum):
    """LISP special forms."""
    DEFUN = "defun"
    LAMBDA = "lambda"
    LET = "let"
    SETQ = "setq"
    IF = "if"
    COND = "cond"
    PROGN = "progn"
    QUOTE = "quote"
    WHEN = "when"
    UNLESS = "unless"
    DEFMACRO = "defmacro"


@dataclass
class LispNode(ABC):
    """Base class for all LISP AST nodes."""
    type: LispNodeType = None
    location: Optional[tuple] = None
    
    @abstractmethod
    def accept(self, visitor):
        """Accept a visitor for the visitor pattern."""
        pass


@dataclass
class LispExpression(LispNode):
    """Base class for LISP expressions."""
    pass


@dataclass
class LispForm(LispNode):
    """Base class for LISP forms."""
    pass


# Atoms
@dataclass
class LispAtom(LispExpression):
    """LISP atom (non-list value)."""
    value: Any
    atom_type: str  # "symbol", "number", "string", "nil", "t"
    
    def __post_init__(self):
        if self.atom_type == "nil":
            self.type = LispNodeType.NIL
        elif self.atom_type == "t":
            self.type = LispNodeType.T
        elif self.atom_type == "symbol":
            self.type = LispNodeType.SYMBOL
        elif self.atom_type == "number":
            self.type = LispNodeType.NUMBER
        elif self.atom_type == "string":
            self.type = LispNodeType.STRING
        else:
            self.type = LispNodeType.ATOM
    
    def accept(self, visitor):
        return visitor.visit_atom(self)


@dataclass
class LispSymbol(LispExpression):
    """LISP symbol."""
    name: str
    
    def __post_init__(self):
        self.type = LispNodeType.SYMBOL
    
    def accept(self, visitor):
        return visitor.visit_symbol(self)


# Lists and structures
@dataclass
class LispList(LispExpression):
    """LISP list."""
    elements: List[LispExpression]
    
    def __post_init__(self):
        self.type = LispNodeType.LIST
    
    def accept(self, visitor):
        return visitor.visit_list(self)


@dataclass
class LispCons(LispExpression):
    """LISP cons cell."""
    car: LispExpression
    cdr: LispExpression
    
    def __post_init__(self):
        self.type = LispNodeType.CONS
    
    def accept(self, visitor):
        return visitor.visit_cons(self)


@dataclass
class LispQuote(LispExpression):
    """LISP quote form."""
    expression: LispExpression
    
    def __post_init__(self):
        self.type = LispNodeType.QUOTE
    
    def accept(self, visitor):
        return visitor.visit_quote(self)


# Special forms
@dataclass
class LispDefun(LispForm):
    """LISP function definition."""
    name: LispSymbol
    parameters: List[LispSymbol]
    body: List[LispExpression]
    doc_string: Optional[str] = None
    
    def __post_init__(self):
        self.type = LispNodeType.DEFUN
    
    def accept(self, visitor):
        return visitor.visit_defun(self)


@dataclass
class LispLambda(LispExpression):
    """LISP lambda expression."""
    parameters: List[LispSymbol]
    body: List[LispExpression]
    
    def __post_init__(self):
        self.type = LispNodeType.LAMBDA
    
    def accept(self, visitor):
        return visitor.visit_lambda(self)


@dataclass
class LispLet(LispExpression):
    """LISP let binding."""
    bindings: List[tuple]  # List of (symbol, value) pairs
    body: List[LispExpression]
    
    def __post_init__(self):
        self.type = LispNodeType.LET
    
    def accept(self, visitor):
        return visitor.visit_let(self)


@dataclass
class LispSetq(LispExpression):
    """LISP setq assignment."""
    symbol: LispSymbol
    value: LispExpression
    
    def __post_init__(self):
        self.type = LispNodeType.SETQ
    
    def accept(self, visitor):
        return visitor.visit_setq(self)


@dataclass
class LispIf(LispExpression):
    """LISP if conditional."""
    test: LispExpression
    then_expr: LispExpression
    else_expr: Optional[LispExpression] = None
    
    def __post_init__(self):
        self.type = LispNodeType.IF
    
    def accept(self, visitor):
        return visitor.visit_if(self)


@dataclass
class LispCond(LispExpression):
    """LISP cond conditional."""
    clauses: List[tuple]  # List of (test, expr) pairs
    
    def __post_init__(self):
        self.type = LispNodeType.COND
    
    def accept(self, visitor):
        return visitor.visit_cond(self)


@dataclass
class LispProgn(LispExpression):
    """LISP progn sequence."""
    expressions: List[LispExpression]
    
    def __post_init__(self):
        self.type = LispNodeType.PROGN
    
    def accept(self, visitor):
        return visitor.visit_progn(self)


@dataclass
class LispWhen(LispExpression):
    """LISP when conditional."""
    test: LispExpression
    body: List[LispExpression]
    
    def __post_init__(self):
        self.type = LispNodeType.WHEN
    
    def accept(self, visitor):
        return visitor.visit_when(self)


@dataclass
class LispUnless(LispExpression):
    """LISP unless conditional."""
    test: LispExpression
    body: List[LispExpression]
    
    def __post_init__(self):
        self.type = LispNodeType.UNLESS
    
    def accept(self, visitor):
        return visitor.visit_unless(self)


# Built-in functions
@dataclass
class LispCar(LispExpression):
    """LISP car function call."""
    expression: LispExpression
    
    def __post_init__(self):
        self.type = LispNodeType.CAR
    
    def accept(self, visitor):
        return visitor.visit_car(self)


@dataclass
class LispCdr(LispExpression):
    """LISP cdr function call."""
    expression: LispExpression
    
    def __post_init__(self):
        self.type = LispNodeType.CDR
    
    def accept(self, visitor):
        return visitor.visit_cdr(self)


@dataclass
class LispConsFunc(LispExpression):
    """LISP cons function call."""
    car: LispExpression
    cdr: LispExpression
    
    def __post_init__(self):
        self.type = LispNodeType.CONS_FUNC
    
    def accept(self, visitor):
        return visitor.visit_cons_func(self)


@dataclass
class LispEq(LispExpression):
    """LISP eq comparison."""
    left: LispExpression
    right: LispExpression
    
    def __post_init__(self):
        self.type = LispNodeType.EQ
    
    def accept(self, visitor):
        return visitor.visit_eq(self)


@dataclass
class LispEqual(LispExpression):
    """LISP equal comparison."""
    left: LispExpression
    right: LispExpression
    
    def __post_init__(self):
        self.type = LispNodeType.EQUAL
    
    def accept(self, visitor):
        return visitor.visit_equal(self)


@dataclass
class LispAtomFunc(LispExpression):
    """LISP atom predicate."""
    expression: LispExpression
    
    def __post_init__(self):
        self.type = LispNodeType.ATOM_FUNC
    
    def accept(self, visitor):
        return visitor.visit_atom_func(self)


@dataclass
class LispListp(LispExpression):
    """LISP listp predicate."""
    expression: LispExpression
    
    def __post_init__(self):
        self.type = LispNodeType.LISTP
    
    def accept(self, visitor):
        return visitor.visit_listp(self)


# Control flow
@dataclass
class LispLoop(LispExpression):
    """LISP loop construct."""
    body: List[LispExpression]
    
    def __post_init__(self):
        self.type = LispNodeType.LOOP
    
    def accept(self, visitor):
        return visitor.visit_loop(self)


@dataclass
class LispReturn(LispExpression):
    """LISP return statement."""
    value: Optional[LispExpression] = None
    
    def __post_init__(self):
        self.type = LispNodeType.RETURN
    
    def accept(self, visitor):
        return visitor.visit_return(self)


# Macros
@dataclass
class LispDefmacro(LispForm):
    """LISP macro definition."""
    name: LispSymbol
    parameters: List[LispSymbol]
    body: List[LispExpression]
    
    def __post_init__(self):
        self.type = LispNodeType.DEFMACRO
    
    def accept(self, visitor):
        return visitor.visit_defmacro(self)


@dataclass
class LispMacroCall(LispExpression):
    """LISP macro call."""
    name: LispSymbol
    arguments: List[LispExpression]
    
    def __post_init__(self):
        self.type = LispNodeType.MACRO_CALL
    
    def accept(self, visitor):
        return visitor.visit_macro_call(self)


# Function application
@dataclass
class LispApplication(LispExpression):
    """LISP function application."""
    function: LispExpression
    arguments: List[LispExpression]
    
    def accept(self, visitor):
        return visitor.visit_application(self)


# Program/Module
@dataclass
class LispProgram(LispNode):
    """LISP program/module."""
    forms: List[LispForm] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = LispNodeType.PROGRAM
    
    def accept(self, visitor):
        return visitor.visit_program(self)


# Visitor pattern
class LispNodeVisitor(ABC):
    """Visitor interface for LISP AST nodes."""
    
    @abstractmethod
    def visit_atom(self, node: LispAtom): pass
    
    @abstractmethod
    def visit_symbol(self, node: LispSymbol): pass
    
    @abstractmethod
    def visit_list(self, node: LispList): pass
    
    @abstractmethod
    def visit_cons(self, node: LispCons): pass
    
    @abstractmethod
    def visit_quote(self, node: LispQuote): pass
    
    @abstractmethod
    def visit_defun(self, node: LispDefun): pass
    
    @abstractmethod
    def visit_lambda(self, node: LispLambda): pass
    
    @abstractmethod
    def visit_let(self, node: LispLet): pass
    
    @abstractmethod
    def visit_setq(self, node: LispSetq): pass
    
    @abstractmethod
    def visit_if(self, node: LispIf): pass
    
    @abstractmethod
    def visit_cond(self, node: LispCond): pass
    
    @abstractmethod
    def visit_progn(self, node: LispProgn): pass
    
    @abstractmethod
    def visit_car(self, node: LispCar): pass
    
    @abstractmethod
    def visit_cdr(self, node: LispCdr): pass
    
    @abstractmethod
    def visit_application(self, node: LispApplication): pass
    
    @abstractmethod
    def visit_program(self, node: LispProgram): pass


# Utility functions
def lisp_nil() -> LispAtom:
    """Create nil atom."""
    return LispAtom(None, "nil")

def lisp_t() -> LispAtom:
    """Create t atom."""
    return LispAtom(True, "t")

def lisp_number(value: Union[int, float]) -> LispAtom:
    """Create number atom."""
    return LispAtom(value, "number")

def lisp_string(value: str) -> LispAtom:
    """Create string atom."""
    return LispAtom(value, "string")

def lisp_symbol(name: str) -> LispSymbol:
    """Create symbol."""
    return LispSymbol(name)

def lisp_list(*elements: LispExpression) -> LispList:
    """Create list."""
    return LispList(list(elements))

def lisp_cons(car: LispExpression, cdr: LispExpression) -> LispCons:
    """Create cons cell."""
    return LispCons(car, cdr)

def lisp_quote(expr: LispExpression) -> LispQuote:
    """Create quote."""
    return LispQuote(expr)

def lisp_application(func: LispExpression, *args: LispExpression) -> LispApplication:
    """Create function application."""
    return LispApplication(func, list(args)) 