#!/usr/bin/env python3
"""
Starlark Abstract Syntax Tree (AST) Implementation

This module provides a comprehensive AST for the Starlark language, which is a Python-like
configuration language used primarily in Bazel build systems. Starlark is designed to be
deterministic and hermetic with restricted Python syntax.

Key Starlark features:
- Python-like syntax with restrictions for determinism
- Immutable data structures after construction
- No side effects or arbitrary code execution
- Limited standard library for configuration tasks
- Support for functions, rules, macros, aspects, and providers
- No classes, limited imports, no arbitrary file I/O

The AST follows the visitor pattern for easy traversal and transformation.
"""

from typing import Any, List, Optional, Union, Dict, Set
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum


class StarlarkNodeType(Enum):
    """Enumeration of all Starlark AST node types."""
    
    # Base types
    MODULE = "module"
    STATEMENT = "statement"
    EXPRESSION = "expression"
    
    # Literals
    INT_LITERAL = "int_literal"
    FLOAT_LITERAL = "float_literal"
    STRING_LITERAL = "string_literal"
    BOOL_LITERAL = "bool_literal"
    NONE_LITERAL = "none_literal"
    
    # Collections
    LIST = "list"
    TUPLE = "tuple"
    DICT = "dict"
    SET = "set"
    
    # Identifiers and access
    IDENTIFIER = "identifier"
    ATTRIBUTE = "attribute"
    INDEX = "index"
    SLICE = "slice"
    
    # Operators
    BINARY_OP = "binary_op"
    UNARY_OP = "unary_op"
    COMPARISON = "comparison"
    BOOLEAN_OP = "boolean_op"
    
    # Control flow
    IF = "if"
    FOR = "for"
    WHILE = "while"
    BREAK = "break"
    CONTINUE = "continue"
    PASS = "pass"
    
    # Functions and calls
    FUNCTION_DEF = "function_def"
    LAMBDA = "lambda"
    CALL = "call"
    RETURN = "return"
    
    # Assignments
    ASSIGN = "assign"
    AUG_ASSIGN = "aug_assign"
    
    # Starlark-specific constructs
    RULE = "rule"
    ASPECT = "aspect"
    PROVIDER = "provider"
    LOAD = "load"
    
    # Comprehensions
    LIST_COMP = "list_comp"
    DICT_COMP = "dict_comp"
    
    # Special constructs
    CONDITIONAL_EXPR = "conditional_expr"
    STARRED = "starred"
    KEYWORD = "keyword"


class StarlarkOperator(Enum):
    """Starlark operators."""
    
    # Arithmetic
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"
    FLOOR_DIV = "//"
    MOD = "%"
    POW = "**"
    
    # Bitwise
    BIT_OR = "|"
    BIT_XOR = "^"
    BIT_AND = "&"
    LEFT_SHIFT = "<<"
    RIGHT_SHIFT = ">>"
    INVERT = "~"
    
    # Comparison
    EQ = "=="
    NE = "!="
    LT = "<"
    LE = "<="
    GT = ">"
    GE = ">="
    IN = "in"
    NOT_IN = "not in"
    IS = "is"
    IS_NOT = "is not"
    
    # Logical
    AND = "and"
    OR = "or"
    NOT = "not"
    
    # Unary
    UADD = "+u"
    USUB = "-u"


@dataclass
class StarlarkNode(ABC):
    """Base class for all Starlark AST nodes."""
    
    node_type: StarlarkNodeType
    line: int = 0
    column: int = 0
    
    @abstractmethod
    def accept(self, visitor: 'StarlarkVisitor') -> Any:
        """Accept a visitor for traversal."""
        pass
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(type={self.node_type.value})"


class StarlarkVisitor(ABC):
    """Abstract visitor for Starlark AST traversal."""
    
    @abstractmethod
    def visit_module(self, node: 'StarlarkModule') -> Any:
        pass
    
    @abstractmethod
    def visit_literal(self, node: 'StarlarkLiteral') -> Any:
        pass
    
    @abstractmethod
    def visit_identifier(self, node: 'StarlarkIdentifier') -> Any:
        pass
    
    @abstractmethod
    def visit_binary_op(self, node: 'StarlarkBinaryOp') -> Any:
        pass
    
    @abstractmethod
    def visit_unary_op(self, node: 'StarlarkUnaryOp') -> Any:
        pass
    
    @abstractmethod
    def visit_call(self, node: 'StarlarkCall') -> Any:
        pass
    
    @abstractmethod
    def visit_function_def(self, node: 'StarlarkFunctionDef') -> Any:
        pass
    
    @abstractmethod
    def visit_assign(self, node: 'StarlarkAssign') -> Any:
        pass
    
    @abstractmethod
    def visit_if(self, node: 'StarlarkIf') -> Any:
        pass
    
    @abstractmethod
    def visit_for(self, node: 'StarlarkFor') -> Any:
        pass
    
    @abstractmethod
    def visit_list(self, node: 'StarlarkList') -> Any:
        pass
    
    @abstractmethod
    def visit_dict(self, node: 'StarlarkDict') -> Any:
        pass
    
    @abstractmethod
    def visit_rule(self, node: 'StarlarkRule') -> Any:
        pass
    
    @abstractmethod
    def visit_load(self, node: 'StarlarkLoad') -> Any:
        pass


# Expression nodes

@dataclass
class StarlarkExpression(StarlarkNode):
    """Base class for all Starlark expressions."""
    pass


@dataclass
class StarlarkLiteral(StarlarkExpression):
    """Literal value (int, float, string, bool, None)."""
    
    value: Any
    literal_type: str  # "int", "float", "string", "bool", "none"
    
    def __post_init__(self):
        type_map = {
            int: (StarlarkNodeType.INT_LITERAL, "int"),
            float: (StarlarkNodeType.FLOAT_LITERAL, "float"),
            str: (StarlarkNodeType.STRING_LITERAL, "string"),
            bool: (StarlarkNodeType.BOOL_LITERAL, "bool"),
            type(None): (StarlarkNodeType.NONE_LITERAL, "none")
        }
        
        if type(self.value) in type_map:
            self.node_type, self.literal_type = type_map[type(self.value)]
        else:
            raise ValueError(f"Unsupported literal type: {type(self.value)}")
    
    def accept(self, visitor: StarlarkVisitor) -> Any:
        return visitor.visit_literal(self)


@dataclass
class StarlarkIdentifier(StarlarkExpression):
    """Variable or function name."""
    
    name: str
    node_type: StarlarkNodeType = field(default=StarlarkNodeType.IDENTIFIER, init=False)
    
    def accept(self, visitor: StarlarkVisitor) -> Any:
        return visitor.visit_identifier(self)


@dataclass
class StarlarkBinaryOp(StarlarkExpression):
    """Binary operation (left op right)."""
    
    left: StarlarkExpression
    operator: StarlarkOperator
    right: StarlarkExpression
    node_type: StarlarkNodeType = field(default=StarlarkNodeType.BINARY_OP, init=False)
    
    def accept(self, visitor: StarlarkVisitor) -> Any:
        return visitor.visit_binary_op(self)


@dataclass
class StarlarkUnaryOp(StarlarkExpression):
    """Unary operation (op operand)."""
    
    operator: StarlarkOperator
    operand: StarlarkExpression
    node_type: StarlarkNodeType = field(default=StarlarkNodeType.UNARY_OP, init=False)
    
    def accept(self, visitor: StarlarkVisitor) -> Any:
        return visitor.visit_unary_op(self)


@dataclass
class StarlarkComparison(StarlarkExpression):
    """Comparison operation."""
    
    left: StarlarkExpression
    operators: List[StarlarkOperator]
    comparators: List[StarlarkExpression]
    node_type: StarlarkNodeType = field(default=StarlarkNodeType.COMPARISON, init=False)
    
    def accept(self, visitor: StarlarkVisitor) -> Any:
        return visitor.visit_comparison(self)


@dataclass
class StarlarkBoolOp(StarlarkExpression):
    """Boolean operation (and/or)."""
    
    operator: StarlarkOperator  # AND or OR
    values: List[StarlarkExpression]
    node_type: StarlarkNodeType = field(default=StarlarkNodeType.BOOLEAN_OP, init=False)
    
    def accept(self, visitor: StarlarkVisitor) -> Any:
        return visitor.visit_bool_op(self)


@dataclass
class StarlarkAttribute(StarlarkExpression):
    """Attribute access (object.attr)."""
    
    value: StarlarkExpression
    attr: str
    node_type: StarlarkNodeType = field(default=StarlarkNodeType.ATTRIBUTE, init=False)
    
    def accept(self, visitor: StarlarkVisitor) -> Any:
        return visitor.visit_attribute(self)


@dataclass
class StarlarkIndex(StarlarkExpression):
    """Index access (object[index])."""
    
    value: StarlarkExpression
    index: StarlarkExpression
    node_type: StarlarkNodeType = field(default=StarlarkNodeType.INDEX, init=False)
    
    def accept(self, visitor: StarlarkVisitor) -> Any:
        return visitor.visit_index(self)


@dataclass
class StarlarkSlice(StarlarkExpression):
    """Slice access (object[start:end:step])."""
    
    value: StarlarkExpression
    start: Optional[StarlarkExpression]
    end: Optional[StarlarkExpression]
    step: Optional[StarlarkExpression]
    node_type: StarlarkNodeType = field(default=StarlarkNodeType.SLICE, init=False)
    
    def accept(self, visitor: StarlarkVisitor) -> Any:
        return visitor.visit_slice(self)


@dataclass
class StarlarkList(StarlarkExpression):
    """List literal [a, b, c]."""
    
    elements: List[StarlarkExpression]
    node_type: StarlarkNodeType = field(default=StarlarkNodeType.LIST, init=False)
    
    def accept(self, visitor: StarlarkVisitor) -> Any:
        return visitor.visit_list(self)


@dataclass
class StarlarkTuple(StarlarkExpression):
    """Tuple literal (a, b, c)."""
    
    elements: List[StarlarkExpression]
    node_type: StarlarkNodeType = field(default=StarlarkNodeType.TUPLE, init=False)
    
    def accept(self, visitor: StarlarkVisitor) -> Any:
        return visitor.visit_tuple(self)


@dataclass
class StarlarkDict(StarlarkExpression):
    """Dictionary literal {key: value, ...}."""
    
    keys: List[StarlarkExpression]
    values: List[StarlarkExpression]
    node_type: StarlarkNodeType = field(default=StarlarkNodeType.DICT, init=False)
    
    def accept(self, visitor: StarlarkVisitor) -> Any:
        return visitor.visit_dict(self)


@dataclass
class StarlarkCall(StarlarkExpression):
    """Function call func(args, kwargs)."""
    
    func: StarlarkExpression
    args: List[StarlarkExpression]
    keywords: List['StarlarkKeyword']
    node_type: StarlarkNodeType = field(default=StarlarkNodeType.CALL, init=False)
    
    def accept(self, visitor: StarlarkVisitor) -> Any:
        return visitor.visit_call(self)


@dataclass
class StarlarkKeyword(StarlarkNode):
    """Keyword argument in function call."""
    
    arg: str  # keyword name
    value: StarlarkExpression
    node_type: StarlarkNodeType = field(default=StarlarkNodeType.KEYWORD, init=False)
    
    def accept(self, visitor: StarlarkVisitor) -> Any:
        return visitor.visit_keyword(self)


@dataclass
class StarlarkLambda(StarlarkExpression):
    """Lambda function lambda args: body."""
    
    args: List[str]
    body: StarlarkExpression
    node_type: StarlarkNodeType = field(default=StarlarkNodeType.LAMBDA, init=False)
    
    def accept(self, visitor: StarlarkVisitor) -> Any:
        return visitor.visit_lambda(self)


@dataclass
class StarlarkConditionalExpr(StarlarkExpression):
    """Conditional expression (test if condition else orelse)."""
    
    test: StarlarkExpression
    body: StarlarkExpression
    orelse: StarlarkExpression
    node_type: StarlarkNodeType = field(default=StarlarkNodeType.CONDITIONAL_EXPR, init=False)
    
    def accept(self, visitor: StarlarkVisitor) -> Any:
        return visitor.visit_conditional_expr(self)


@dataclass
class StarlarkListComp(StarlarkExpression):
    """List comprehension [expr for target in iter if condition]."""
    
    element: StarlarkExpression
    target: str
    iter: StarlarkExpression
    ifs: List[StarlarkExpression]
    node_type: StarlarkNodeType = field(default=StarlarkNodeType.LIST_COMP, init=False)
    
    def accept(self, visitor: StarlarkVisitor) -> Any:
        return visitor.visit_list_comp(self)


@dataclass
class StarlarkDictComp(StarlarkExpression):
    """Dictionary comprehension {key: value for target in iter if condition}."""
    
    key: StarlarkExpression
    value: StarlarkExpression
    target: str
    iter: StarlarkExpression
    ifs: List[StarlarkExpression]
    node_type: StarlarkNodeType = field(default=StarlarkNodeType.DICT_COMP, init=False)
    
    def accept(self, visitor: StarlarkVisitor) -> Any:
        return visitor.visit_dict_comp(self)


# Statement nodes

@dataclass
class StarlarkStatement(StarlarkNode):
    """Base class for all Starlark statements."""
    pass


@dataclass
class StarlarkAssign(StarlarkStatement):
    """Assignment statement."""
    
    targets: List[StarlarkExpression]
    value: StarlarkExpression
    node_type: StarlarkNodeType = field(default=StarlarkNodeType.ASSIGN, init=False)
    
    def accept(self, visitor: StarlarkVisitor) -> Any:
        return visitor.visit_assign(self)


@dataclass
class StarlarkAugAssign(StarlarkStatement):
    """Augmented assignment (+=, -=, etc.)."""
    
    target: StarlarkExpression
    operator: StarlarkOperator
    value: StarlarkExpression
    node_type: StarlarkNodeType = field(default=StarlarkNodeType.AUG_ASSIGN, init=False)
    
    def accept(self, visitor: StarlarkVisitor) -> Any:
        return visitor.visit_aug_assign(self)


@dataclass
class StarlarkFunctionDef(StarlarkStatement):
    """Function definition."""
    
    name: str
    args: List[str]
    defaults: List[StarlarkExpression]
    body: List[StarlarkStatement]
    node_type: StarlarkNodeType = field(default=StarlarkNodeType.FUNCTION_DEF, init=False)
    
    def accept(self, visitor: StarlarkVisitor) -> Any:
        return visitor.visit_function_def(self)


@dataclass
class StarlarkReturn(StarlarkStatement):
    """Return statement."""
    
    value: Optional[StarlarkExpression]
    node_type: StarlarkNodeType = field(default=StarlarkNodeType.RETURN, init=False)
    
    def accept(self, visitor: StarlarkVisitor) -> Any:
        return visitor.visit_return(self)


@dataclass
class StarlarkIf(StarlarkStatement):
    """If statement."""
    
    test: StarlarkExpression
    body: List[StarlarkStatement]
    orelse: List[StarlarkStatement]
    node_type: StarlarkNodeType = field(default=StarlarkNodeType.IF, init=False)
    
    def accept(self, visitor: StarlarkVisitor) -> Any:
        return visitor.visit_if(self)


@dataclass
class StarlarkFor(StarlarkStatement):
    """For loop."""
    
    target: str
    iter: StarlarkExpression
    body: List[StarlarkStatement]
    node_type: StarlarkNodeType = field(default=StarlarkNodeType.FOR, init=False)
    
    def accept(self, visitor: StarlarkVisitor) -> Any:
        return visitor.visit_for(self)


@dataclass
class StarlarkBreak(StarlarkStatement):
    """Break statement."""
    
    node_type: StarlarkNodeType = field(default=StarlarkNodeType.BREAK, init=False)
    
    def accept(self, visitor: StarlarkVisitor) -> Any:
        return visitor.visit_break(self)


@dataclass
class StarlarkContinue(StarlarkStatement):
    """Continue statement."""
    
    node_type: StarlarkNodeType = field(default=StarlarkNodeType.CONTINUE, init=False)
    
    def accept(self, visitor: StarlarkVisitor) -> Any:
        return visitor.visit_continue(self)


@dataclass
class StarlarkPass(StarlarkStatement):
    """Pass statement."""
    
    node_type: StarlarkNodeType = field(default=StarlarkNodeType.PASS, init=False)
    
    def accept(self, visitor: StarlarkVisitor) -> Any:
        return visitor.visit_pass(self)


# Starlark-specific constructs

@dataclass
class StarlarkLoad(StarlarkStatement):
    """Load statement for importing symbols."""
    
    module: str
    symbols: List[str]
    aliases: Dict[str, str] = field(default_factory=dict)
    node_type: StarlarkNodeType = field(default=StarlarkNodeType.LOAD, init=False)
    
    def accept(self, visitor: StarlarkVisitor) -> Any:
        return visitor.visit_load(self)


@dataclass
class StarlarkRule(StarlarkStatement):
    """Rule definition (Bazel build rule)."""
    
    name: str
    implementation: StarlarkExpression
    attrs: Dict[str, StarlarkExpression]
    doc: Optional[str] = None
    node_type: StarlarkNodeType = field(default=StarlarkNodeType.RULE, init=False)
    
    def accept(self, visitor: StarlarkVisitor) -> Any:
        return visitor.visit_rule(self)


@dataclass
class StarlarkAspect(StarlarkStatement):
    """Aspect definition (Bazel aspect)."""
    
    name: str
    implementation: StarlarkExpression
    attr_aspects: List[str]
    attrs: Dict[str, StarlarkExpression]
    node_type: StarlarkNodeType = field(default=StarlarkNodeType.ASPECT, init=False)
    
    def accept(self, visitor: StarlarkVisitor) -> Any:
        return visitor.visit_aspect(self)


@dataclass
class StarlarkProvider(StarlarkStatement):
    """Provider definition (Bazel provider)."""
    
    name: str
    fields: List[str]
    doc: Optional[str] = None
    node_type: StarlarkNodeType = field(default=StarlarkNodeType.PROVIDER, init=False)
    
    def accept(self, visitor: StarlarkVisitor) -> Any:
        return visitor.visit_provider(self)


# Module and top-level

@dataclass
class StarlarkModule(StarlarkNode):
    """Top-level module containing all statements."""
    
    body: List[StarlarkStatement]
    docstring: Optional[str] = None
    node_type: StarlarkNodeType = field(default=StarlarkNodeType.MODULE, init=False)
    
    def accept(self, visitor: StarlarkVisitor) -> Any:
        return visitor.visit_module(self)


# Helper functions for creating AST nodes

def starlark_int(value: int) -> StarlarkLiteral:
    """Create an integer literal."""
    return StarlarkLiteral(value=value, literal_type="int")


def starlark_float(value: float) -> StarlarkLiteral:
    """Create a float literal."""
    return StarlarkLiteral(value=value, literal_type="float")


def starlark_string(value: str) -> StarlarkLiteral:
    """Create a string literal."""
    return StarlarkLiteral(value=value, literal_type="string")


def starlark_bool(value: bool) -> StarlarkLiteral:
    """Create a boolean literal."""
    return StarlarkLiteral(value=value, literal_type="bool")


def starlark_none() -> StarlarkLiteral:
    """Create a None literal."""
    return StarlarkLiteral(value=None, literal_type="none")


def starlark_var(name: str) -> StarlarkIdentifier:
    """Create a variable reference."""
    return StarlarkIdentifier(name=name)


def starlark_call(func: StarlarkExpression, args: List[StarlarkExpression], 
                  keywords: Optional[List[StarlarkKeyword]] = None) -> StarlarkCall:
    """Create a function call."""
    return StarlarkCall(func=func, args=args, keywords=keywords or [])


def starlark_list(elements: List[StarlarkExpression]) -> StarlarkList:
    """Create a list literal."""
    return StarlarkList(elements=elements)


def starlark_dict(keys: List[StarlarkExpression], 
                  values: List[StarlarkExpression]) -> StarlarkDict:
    """Create a dictionary literal."""
    return StarlarkDict(keys=keys, values=values)


def starlark_assign(targets: List[StarlarkExpression], 
                    value: StarlarkExpression) -> StarlarkAssign:
    """Create an assignment statement."""
    return StarlarkAssign(targets=targets, value=value)


def starlark_function(name: str, args: List[str], body: List[StarlarkStatement],
                      defaults: Optional[List[StarlarkExpression]] = None) -> StarlarkFunctionDef:
    """Create a function definition."""
    return StarlarkFunctionDef(name=name, args=args, defaults=defaults or [], body=body)


def starlark_if(test: StarlarkExpression, body: List[StarlarkStatement],
                orelse: Optional[List[StarlarkStatement]] = None) -> StarlarkIf:
    """Create an if statement."""
    return StarlarkIf(test=test, body=body, orelse=orelse or [])


def starlark_for(target: str, iter: StarlarkExpression, 
                 body: List[StarlarkStatement]) -> StarlarkFor:
    """Create a for loop."""
    return StarlarkFor(target=target, iter=iter, body=body)


def starlark_load(module: str, symbols: List[str], 
                  aliases: Optional[Dict[str, str]] = None) -> StarlarkLoad:
    """Create a load statement."""
    return StarlarkLoad(module=module, symbols=symbols, aliases=aliases or {})


def starlark_rule(name: str, implementation: StarlarkExpression,
                  attrs: Dict[str, StarlarkExpression], doc: Optional[str] = None) -> StarlarkRule:
    """Create a rule definition."""
    return StarlarkRule(name=name, implementation=implementation, attrs=attrs, doc=doc)


# Validation functions

def validate_starlark_ast(node: StarlarkNode) -> List[str]:
    """Validate a Starlark AST and return any errors."""
    errors = []
    
    class ValidationVisitor(StarlarkVisitor):
        def visit_module(self, node: StarlarkModule) -> None:
            for stmt in node.body:
                stmt.accept(self)
        
        def visit_literal(self, node: StarlarkLiteral) -> None:
            pass
        
        def visit_identifier(self, node: StarlarkIdentifier) -> None:
            if not node.name.isidentifier():
                errors.append(f"Invalid identifier: {node.name}")
        
        def visit_binary_op(self, node: StarlarkBinaryOp) -> None:
            node.left.accept(self)
            node.right.accept(self)
        
        def visit_unary_op(self, node: StarlarkUnaryOp) -> None:
            node.operand.accept(self)
        
        def visit_call(self, node: StarlarkCall) -> None:
            node.func.accept(self)
            for arg in node.args:
                arg.accept(self)
            for kw in node.keywords:
                kw.accept(self)
        
        def visit_function_def(self, node: StarlarkFunctionDef) -> None:
            if not node.name.isidentifier():
                errors.append(f"Invalid function name: {node.name}")
            for stmt in node.body:
                stmt.accept(self)
        
        def visit_assign(self, node: StarlarkAssign) -> None:
            for target in node.targets:
                target.accept(self)
            node.value.accept(self)
        
        def visit_if(self, node: StarlarkIf) -> None:
            node.test.accept(self)
            for stmt in node.body:
                stmt.accept(self)
            for stmt in node.orelse:
                stmt.accept(self)
        
        def visit_for(self, node: StarlarkFor) -> None:
            if not node.target.isidentifier():
                errors.append(f"Invalid for loop target: {node.target}")
            node.iter.accept(self)
            for stmt in node.body:
                stmt.accept(self)
        
        def visit_list(self, node: StarlarkList) -> None:
            for elem in node.elements:
                elem.accept(self)
        
        def visit_dict(self, node: StarlarkDict) -> None:
            if len(node.keys) != len(node.values):
                errors.append("Dictionary keys and values count mismatch")
            for key in node.keys:
                key.accept(self)
            for value in node.values:
                value.accept(self)
        
        def visit_rule(self, node: StarlarkRule) -> None:
            if not node.name.isidentifier():
                errors.append(f"Invalid rule name: {node.name}")
            node.implementation.accept(self)
            for value in node.attrs.values():
                value.accept(self)
        
        def visit_load(self, node: StarlarkLoad) -> None:
            if not node.module:
                errors.append("Load statement must specify a module")
            for symbol in node.symbols:
                if not symbol.isidentifier():
                    errors.append(f"Invalid symbol in load: {symbol}")
        
        # Additional visitor methods for completeness
        def visit_comparison(self, node: StarlarkComparison) -> None:
            node.left.accept(self)
            for comp in node.comparators:
                comp.accept(self)
        
        def visit_bool_op(self, node: StarlarkBoolOp) -> None:
            for value in node.values:
                value.accept(self)
        
        def visit_attribute(self, node: StarlarkAttribute) -> None:
            node.value.accept(self)
        
        def visit_index(self, node: StarlarkIndex) -> None:
            node.value.accept(self)
            node.index.accept(self)
        
        def visit_slice(self, node: StarlarkSlice) -> None:
            node.value.accept(self)
            if node.start:
                node.start.accept(self)
            if node.end:
                node.end.accept(self)
            if node.step:
                node.step.accept(self)
        
        def visit_tuple(self, node: StarlarkTuple) -> None:
            for elem in node.elements:
                elem.accept(self)
        
        def visit_keyword(self, node: StarlarkKeyword) -> None:
            node.value.accept(self)
        
        def visit_lambda(self, node: StarlarkLambda) -> None:
            node.body.accept(self)
        
        def visit_conditional_expr(self, node: StarlarkConditionalExpr) -> None:
            node.test.accept(self)
            node.body.accept(self)
            node.orelse.accept(self)
        
        def visit_list_comp(self, node: StarlarkListComp) -> None:
            node.element.accept(self)
            node.iter.accept(self)
            for if_clause in node.ifs:
                if_clause.accept(self)
        
        def visit_dict_comp(self, node: StarlarkDictComp) -> None:
            node.key.accept(self)
            node.value.accept(self)
            node.iter.accept(self)
            for if_clause in node.ifs:
                if_clause.accept(self)
        
        def visit_aug_assign(self, node: StarlarkAugAssign) -> None:
            node.target.accept(self)
            node.value.accept(self)
        
        def visit_return(self, node: StarlarkReturn) -> None:
            if node.value:
                node.value.accept(self)
        
        def visit_break(self, node: StarlarkBreak) -> None:
            pass
        
        def visit_continue(self, node: StarlarkContinue) -> None:
            pass
        
        def visit_pass(self, node: StarlarkPass) -> None:
            pass
        
        def visit_aspect(self, node: StarlarkAspect) -> None:
            node.implementation.accept(self)
            for value in node.attrs.values():
                value.accept(self)
        
        def visit_provider(self, node: StarlarkProvider) -> None:
            if not node.name.isidentifier():
                errors.append(f"Invalid provider name: {node.name}")
    
    visitor = ValidationVisitor()
    node.accept(visitor)
    return errors


__all__ = [
    # Base classes
    "StarlarkNode", "StarlarkExpression", "StarlarkStatement", "StarlarkVisitor",
    
    # Enums
    "StarlarkNodeType", "StarlarkOperator",
    
    # Expression nodes
    "StarlarkLiteral", "StarlarkIdentifier", "StarlarkBinaryOp", "StarlarkUnaryOp",
    "StarlarkComparison", "StarlarkBoolOp", "StarlarkAttribute", "StarlarkIndex",
    "StarlarkSlice", "StarlarkList", "StarlarkTuple", "StarlarkDict", "StarlarkCall",
    "StarlarkKeyword", "StarlarkLambda", "StarlarkConditionalExpr", "StarlarkListComp",
    "StarlarkDictComp",
    
    # Statement nodes
    "StarlarkAssign", "StarlarkAugAssign", "StarlarkFunctionDef", "StarlarkReturn",
    "StarlarkIf", "StarlarkFor", "StarlarkBreak", "StarlarkContinue", "StarlarkPass",
    
    # Starlark-specific
    "StarlarkLoad", "StarlarkRule", "StarlarkAspect", "StarlarkProvider",
    
    # Module
    "StarlarkModule",
    
    # Helper functions
    "starlark_int", "starlark_float", "starlark_string", "starlark_bool", "starlark_none",
    "starlark_var", "starlark_call", "starlark_list", "starlark_dict", "starlark_assign",
    "starlark_function", "starlark_if", "starlark_for", "starlark_load", "starlark_rule",
    
    # Validation
    "validate_starlark_ast"
] 