#!/usr/bin/env python3
"""
Clojure AST Node Definitions

Comprehensive Abstract Syntax Tree nodes for Clojure covering
functional programming with S-expressions, immutable data structures,
macros, and dynamic features.
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod


class ClojureNodeType(Enum):
    """Clojure AST node types."""
    # Literals
    LITERAL = auto()
    NIL = auto()
    BOOLEAN = auto()
    NUMBER = auto()
    STRING = auto()
    CHARACTER = auto()
    KEYWORD = auto()
    
    # Identifiers and symbols
    SYMBOL = auto()
    QUALIFIED_SYMBOL = auto()
    
    # Collections
    LIST = auto()
    VECTOR = auto()
    MAP = auto()
    SET = auto()
    
    # Special forms
    DEF = auto()
    DEFN = auto()
    DEFMACRO = auto()
    FN = auto()
    LET = auto()
    IF = auto()
    WHEN = auto()
    COND = auto()
    CASE = auto()
    DO = auto()
    LOOP = auto()
    RECUR = auto()
    TRY = auto()
    CATCH = auto()
    FINALLY = auto()
    THROW = auto()
    
    # Namespace forms
    NS = auto()
    IN_NS = auto()
    REQUIRE = auto()
    USE = auto()
    IMPORT = auto()
    
    # Metadata and reader macros
    METADATA = auto()
    QUOTE = auto()
    SYNTAX_QUOTE = auto()
    UNQUOTE = auto()
    UNQUOTE_SPLICING = auto()
    DEREF = auto()
    
    # Interop
    JAVA_INTEROP = auto()
    NEW = auto()
    DOT = auto()
    
    # Threading macros
    THREAD_FIRST = auto()
    THREAD_LAST = auto()


class ClojureSpecialForm(Enum):
    """Clojure special forms."""
    DEF = "def"
    IF = "if"
    DO = "do"
    LET = "let"
    QUOTE = "quote"
    VAR = "var"
    FN = "fn"
    LOOP = "loop"
    RECUR = "recur"
    THROW = "throw"
    TRY = "try"
    CATCH = "catch"
    FINALLY = "finally"
    NEW = "new"
    DOT = "."
    SET_BANG = "set!"


@dataclass
class ClojureNode(ABC):
    """Base class for all Clojure AST nodes."""
    type: ClojureNodeType = None
    metadata: Optional[Dict[str, Any]] = None
    location: Optional[tuple] = None
    
    @abstractmethod
    def accept(self, visitor):
        """Accept a visitor for the visitor pattern."""
        pass


@dataclass
class ClojureExpression(ClojureNode):
    """Base class for Clojure expressions."""
    pass


@dataclass
class ClojureForm(ClojureNode):
    """Base class for Clojure forms."""
    pass


# Literals
@dataclass
class ClojureLiteral(ClojureExpression):
    """Clojure literal value."""
    value: Any
    literal_type: str  # "nil", "boolean", "number", "string", "char", "keyword"
    
    def __post_init__(self):
        if self.literal_type == "nil":
            self.type = ClojureNodeType.NIL
        elif self.literal_type == "boolean":
            self.type = ClojureNodeType.BOOLEAN
        elif self.literal_type == "number":
            self.type = ClojureNodeType.NUMBER
        elif self.literal_type == "string":
            self.type = ClojureNodeType.STRING
        elif self.literal_type == "char":
            self.type = ClojureNodeType.CHARACTER
        elif self.literal_type == "keyword":
            self.type = ClojureNodeType.KEYWORD
        else:
            self.type = ClojureNodeType.LITERAL
    
    def accept(self, visitor):
        return visitor.visit_literal(self)


@dataclass
class ClojureSymbol(ClojureExpression):
    """Clojure symbol."""
    name: str
    namespace: Optional[str] = None
    
    def __post_init__(self):
        if self.namespace:
            self.type = ClojureNodeType.QUALIFIED_SYMBOL
        else:
            self.type = ClojureNodeType.SYMBOL
    
    @property
    def qualified_name(self) -> str:
        if self.namespace:
            return f"{self.namespace}/{self.name}"
        return self.name
    
    def accept(self, visitor):
        return visitor.visit_symbol(self)


# Collections
@dataclass
class ClojureList(ClojureExpression):
    """Clojure list."""
    elements: List[ClojureExpression]
    
    def __post_init__(self):
        self.type = ClojureNodeType.LIST
    
    def accept(self, visitor):
        return visitor.visit_list(self)


@dataclass
class ClojureVector(ClojureExpression):
    """Clojure vector."""
    elements: List[ClojureExpression]
    
    def __post_init__(self):
        self.type = ClojureNodeType.VECTOR
    
    def accept(self, visitor):
        return visitor.visit_vector(self)


@dataclass
class ClojureMap(ClojureExpression):
    """Clojure map."""
    pairs: List[tuple]  # List of (key, value) tuples
    
    def __post_init__(self):
        self.type = ClojureNodeType.MAP
    
    def accept(self, visitor):
        return visitor.visit_map(self)


@dataclass
class ClojureSet(ClojureExpression):
    """Clojure set."""
    elements: List[ClojureExpression]
    
    def __post_init__(self):
        self.type = ClojureNodeType.SET
    
    def accept(self, visitor):
        return visitor.visit_set(self)


# Special forms
@dataclass
class ClojureDef(ClojureForm):
    """Clojure def form."""
    symbol: ClojureSymbol
    value: ClojureExpression
    doc_string: Optional[str] = None
    
    def __post_init__(self):
        self.type = ClojureNodeType.DEF
    
    def accept(self, visitor):
        return visitor.visit_def(self)


@dataclass
class ClojureFn(ClojureExpression):
    """Clojure function."""
    name: Optional[ClojureSymbol] = None
    arities: List['ClojureFnArity'] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = ClojureNodeType.FN
    
    def accept(self, visitor):
        return visitor.visit_fn(self)


@dataclass
class ClojureFnArity:
    """Function arity definition."""
    params: List[ClojureSymbol]
    body: List[ClojureExpression]
    variadic: bool = False


@dataclass
class ClojureDefn(ClojureForm):
    """Clojure defn form."""
    name: ClojureSymbol
    doc_string: Optional[str] = None
    arities: List[ClojureFnArity] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = ClojureNodeType.DEFN
    
    def accept(self, visitor):
        return visitor.visit_defn(self)


@dataclass
class ClojureLet(ClojureExpression):
    """Clojure let form."""
    bindings: List[tuple]  # List of (symbol, value) pairs
    body: List[ClojureExpression]
    
    def __post_init__(self):
        self.type = ClojureNodeType.LET
    
    def accept(self, visitor):
        return visitor.visit_let(self)


@dataclass
class ClojureIf(ClojureExpression):
    """Clojure if form."""
    test: ClojureExpression
    then_expr: ClojureExpression
    else_expr: Optional[ClojureExpression] = None
    
    def __post_init__(self):
        self.type = ClojureNodeType.IF
    
    def accept(self, visitor):
        return visitor.visit_if(self)


@dataclass
class ClojureCond(ClojureExpression):
    """Clojure cond form."""
    clauses: List[tuple]  # List of (test, expr) pairs
    
    def __post_init__(self):
        self.type = ClojureNodeType.COND
    
    def accept(self, visitor):
        return visitor.visit_cond(self)


@dataclass
class ClojureDo(ClojureExpression):
    """Clojure do form."""
    expressions: List[ClojureExpression]
    
    def __post_init__(self):
        self.type = ClojureNodeType.DO
    
    def accept(self, visitor):
        return visitor.visit_do(self)


@dataclass
class ClojureLoop(ClojureExpression):
    """Clojure loop form."""
    bindings: List[tuple]  # List of (symbol, value) pairs
    body: List[ClojureExpression]
    
    def __post_init__(self):
        self.type = ClojureNodeType.LOOP
    
    def accept(self, visitor):
        return visitor.visit_loop(self)


@dataclass
class ClojureRecur(ClojureExpression):
    """Clojure recur form."""
    args: List[ClojureExpression]
    
    def __post_init__(self):
        self.type = ClojureNodeType.RECUR
    
    def accept(self, visitor):
        return visitor.visit_recur(self)


# Namespace forms
@dataclass
class ClojureNs(ClojureForm):
    """Clojure namespace declaration."""
    name: ClojureSymbol
    requires: List['ClojureRequire'] = field(default_factory=list)
    imports: List['ClojureImport'] = field(default_factory=list)
    uses: List['ClojureUse'] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = ClojureNodeType.NS
    
    def accept(self, visitor):
        return visitor.visit_ns(self)


@dataclass
class ClojureRequire:
    """Clojure require specification."""
    namespace: ClojureSymbol
    alias: Optional[ClojureSymbol] = None
    refer: Optional[List[ClojureSymbol]] = None


@dataclass
class ClojureImport:
    """Clojure import specification."""
    java_class: str
    alias: Optional[str] = None


@dataclass
class ClojureUse:
    """Clojure use specification."""
    namespace: ClojureSymbol
    only: Optional[List[ClojureSymbol]] = None


# Metadata and reader macros
@dataclass
class ClojureQuote(ClojureExpression):
    """Clojure quote form."""
    expression: ClojureExpression
    
    def __post_init__(self):
        self.type = ClojureNodeType.QUOTE
    
    def accept(self, visitor):
        return visitor.visit_quote(self)


@dataclass
class ClojureSyntaxQuote(ClojureExpression):
    """Clojure syntax quote (backtick)."""
    expression: ClojureExpression
    
    def __post_init__(self):
        self.type = ClojureNodeType.SYNTAX_QUOTE
    
    def accept(self, visitor):
        return visitor.visit_syntax_quote(self)


@dataclass
class ClojureUnquote(ClojureExpression):
    """Clojure unquote form."""
    expression: ClojureExpression
    
    def __post_init__(self):
        self.type = ClojureNodeType.UNQUOTE
    
    def accept(self, visitor):
        return visitor.visit_unquote(self)


@dataclass
class ClojureUnquoteSplicing(ClojureExpression):
    """Clojure unquote-splicing form."""
    expression: ClojureExpression
    
    def __post_init__(self):
        self.type = ClojureNodeType.UNQUOTE_SPLICING
    
    def accept(self, visitor):
        return visitor.visit_unquote_splicing(self)


@dataclass
class ClojureDeref(ClojureExpression):
    """Clojure deref form (@)."""
    expression: ClojureExpression
    
    def __post_init__(self):
        self.type = ClojureNodeType.DEREF
    
    def accept(self, visitor):
        return visitor.visit_deref(self)


# Java interop
@dataclass
class ClojureJavaInterop(ClojureExpression):
    """Clojure Java interop form."""
    target: ClojureExpression
    method: str
    args: List[ClojureExpression] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = ClojureNodeType.JAVA_INTEROP
    
    def accept(self, visitor):
        return visitor.visit_java_interop(self)


@dataclass
class ClojureNew(ClojureExpression):
    """Clojure new form."""
    class_name: ClojureSymbol
    args: List[ClojureExpression] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = ClojureNodeType.NEW
    
    def accept(self, visitor):
        return visitor.visit_new(self)


# Threading macros
@dataclass
class ClojureThreadFirst(ClojureExpression):
    """Clojure thread-first macro (->)."""
    initial: ClojureExpression
    forms: List[ClojureExpression]
    
    def __post_init__(self):
        self.type = ClojureNodeType.THREAD_FIRST
    
    def accept(self, visitor):
        return visitor.visit_thread_first(self)


@dataclass
class ClojureThreadLast(ClojureExpression):
    """Clojure thread-last macro (->>)."""
    initial: ClojureExpression
    forms: List[ClojureExpression]
    
    def __post_init__(self):
        self.type = ClojureNodeType.THREAD_LAST
    
    def accept(self, visitor):
        return visitor.visit_thread_last(self)


# Module-level node
@dataclass
class ClojureModule(ClojureNode):
    """Clojure module/file."""
    namespace: Optional[ClojureNs] = None
    forms: List[ClojureForm] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_module(self)


# Visitor pattern
class ClojureNodeVisitor(ABC):
    """Visitor interface for Clojure AST nodes."""
    
    @abstractmethod
    def visit_literal(self, node: ClojureLiteral): pass
    
    @abstractmethod
    def visit_symbol(self, node: ClojureSymbol): pass
    
    @abstractmethod
    def visit_list(self, node: ClojureList): pass
    
    @abstractmethod
    def visit_vector(self, node: ClojureVector): pass
    
    @abstractmethod
    def visit_map(self, node: ClojureMap): pass
    
    @abstractmethod
    def visit_set(self, node: ClojureSet): pass
    
    @abstractmethod
    def visit_def(self, node: ClojureDef): pass
    
    @abstractmethod
    def visit_fn(self, node: ClojureFn): pass
    
    @abstractmethod
    def visit_defn(self, node: ClojureDefn): pass
    
    @abstractmethod
    def visit_let(self, node: ClojureLet): pass
    
    @abstractmethod
    def visit_if(self, node: ClojureIf): pass
    
    @abstractmethod
    def visit_cond(self, node: ClojureCond): pass
    
    @abstractmethod
    def visit_do(self, node: ClojureDo): pass
    
    @abstractmethod
    def visit_loop(self, node: ClojureLoop): pass
    
    @abstractmethod
    def visit_recur(self, node: ClojureRecur): pass
    
    @abstractmethod
    def visit_ns(self, node: ClojureNs): pass
    
    @abstractmethod
    def visit_quote(self, node: ClojureQuote): pass
    
    @abstractmethod
    def visit_module(self, node: ClojureModule): pass


# Utility functions
def clj_nil() -> ClojureLiteral:
    """Create nil literal."""
    return ClojureLiteral(None, "nil")

def clj_bool(value: bool) -> ClojureLiteral:
    """Create boolean literal."""
    return ClojureLiteral(value, "boolean")

def clj_num(value: Union[int, float]) -> ClojureLiteral:
    """Create number literal."""
    return ClojureLiteral(value, "number")

def clj_str(value: str) -> ClojureLiteral:
    """Create string literal."""
    return ClojureLiteral(value, "string")

def clj_keyword(name: str) -> ClojureLiteral:
    """Create keyword literal."""
    return ClojureLiteral(name, "keyword")

def clj_symbol(name: str, namespace: Optional[str] = None) -> ClojureSymbol:
    """Create symbol."""
    return ClojureSymbol(name, namespace)

def clj_list(*elements: ClojureExpression) -> ClojureList:
    """Create list."""
    return ClojureList(list(elements))

def clj_vector(*elements: ClojureExpression) -> ClojureVector:
    """Create vector."""
    return ClojureVector(list(elements))

def clj_map(**pairs) -> ClojureMap:
    """Create map from keyword arguments."""
    map_pairs = []
    for k, v in pairs.items():
        key = clj_keyword(k) if isinstance(k, str) else k
        map_pairs.append((key, v))
    return ClojureMap(map_pairs) 