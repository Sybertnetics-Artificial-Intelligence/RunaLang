#!/usr/bin/env python3
"""
Lua AST - Abstract Syntax Tree for Lua Programming Language

Provides comprehensive AST node definitions for Lua including:
- Variables, functions, and scoping constructs
- Tables, metatables, and table operations
- Control flow structures (if, while, for, repeat)
- Expressions and operators with proper precedence
- String literals and patterns
- Comments and documentation
- Module system and require statements
- Coroutines and advanced Lua features
- Multiple return values and varargs

Supports Lua 5.1, 5.2, 5.3, and 5.4 syntax and semantics.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any, Union
from enum import Enum
from dataclasses import dataclass


class LuaNode(ABC):
    """Base class for all Lua AST nodes"""
    
    def __init__(self, location: Optional[Dict[str, Any]] = None):
        self.location = location or {}
        self.parent: Optional['LuaNode'] = None
        self.children: List['LuaNode'] = []
    
    @abstractmethod
    def accept(self, visitor: 'LuaVisitor') -> Any:
        """Accept visitor pattern implementation"""
        pass
    
    def add_child(self, child: 'LuaNode') -> None:
        """Add child node"""
        if child:
            child.parent = self
            self.children.append(child)


class LuaExpression(LuaNode):
    """Base class for Lua expressions"""
    pass


class LuaStatement(LuaNode):
    """Base class for Lua statements"""
    pass


class LuaBinaryOperator(Enum):
    """Lua binary operators"""
    # Arithmetic
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"
    IDIV = "//"  # Lua 5.3+
    MOD = "%"
    POW = "^"
    
    # Relational
    EQ = "=="
    NE = "~="
    LT = "<"
    LE = "<="
    GT = ">"
    GE = ">="
    
    # Logical
    AND = "and"
    OR = "or"
    
    # String
    CONCAT = ".."


class LuaUnaryOperator(Enum):
    """Lua unary operators"""
    NOT = "not"
    NEG = "-"
    LEN = "#"
    BNOT = "~"  # Lua 5.3+ bitwise not


class LuaLiteralType(Enum):
    """Lua literal types"""
    NIL = "nil"
    BOOLEAN = "boolean"
    NUMBER = "number"
    STRING = "string"
    TABLE = "table"
    FUNCTION = "function"
    USERDATA = "userdata"
    THREAD = "thread"


# Expressions
@dataclass
class LuaLiteral(LuaExpression):
    """Lua literal value"""
    value: Any
    literal_type: LuaLiteralType
    raw_text: str
    
    def accept(self, visitor: 'LuaVisitor') -> Any:
        return visitor.visit_literal(self)


@dataclass
class LuaIdentifier(LuaExpression):
    """Lua identifier"""
    name: str
    
    def accept(self, visitor: 'LuaVisitor') -> Any:
        return visitor.visit_identifier(self)


@dataclass
class LuaBinaryOperation(LuaExpression):
    """Lua binary operation"""
    left: LuaExpression
    operator: LuaBinaryOperator
    right: LuaExpression
    
    def accept(self, visitor: 'LuaVisitor') -> Any:
        return visitor.visit_binary_operation(self)


@dataclass
class LuaUnaryOperation(LuaExpression):
    """Lua unary operation"""
    operator: LuaUnaryOperator
    operand: LuaExpression
    
    def accept(self, visitor: 'LuaVisitor') -> Any:
        return visitor.visit_unary_operation(self)


@dataclass
class LuaTableConstructor(LuaExpression):
    """Lua table constructor"""
    fields: List['LuaTableField']
    
    def accept(self, visitor: 'LuaVisitor') -> Any:
        return visitor.visit_table_constructor(self)


@dataclass
class LuaTableField(LuaNode):
    """Lua table field"""
    key: Optional[LuaExpression]  # None for array-style entries
    value: LuaExpression
    is_method: bool = False  # For key:value syntax
    
    def accept(self, visitor: 'LuaVisitor') -> Any:
        return visitor.visit_table_field(self)


@dataclass
class LuaTableAccess(LuaExpression):
    """Lua table access (table[key] or table.key)"""
    table: LuaExpression
    key: LuaExpression
    is_dot_notation: bool = False  # table.key vs table[key]
    
    def accept(self, visitor: 'LuaVisitor') -> Any:
        return visitor.visit_table_access(self)


@dataclass
class LuaFunctionCall(LuaExpression):
    """Lua function call"""
    function: LuaExpression
    arguments: List[LuaExpression]
    is_method_call: bool = False  # obj:method() vs obj.method()
    
    def accept(self, visitor: 'LuaVisitor') -> Any:
        return visitor.visit_function_call(self)


@dataclass
class LuaFunctionDefinition(LuaExpression):
    """Lua function definition"""
    parameters: List[str]
    body: 'LuaBlock'
    is_vararg: bool = False  # function(...) 
    name: Optional[str] = None  # For named functions
    is_local: bool = False
    is_method: bool = False  # function obj:method()
    
    def accept(self, visitor: 'LuaVisitor') -> Any:
        return visitor.visit_function_definition(self)


@dataclass
class LuaVarargExpression(LuaExpression):
    """Lua vararg expression (...)"""
    
    def accept(self, visitor: 'LuaVisitor') -> Any:
        return visitor.visit_vararg_expression(self)


# Statements
@dataclass
class LuaAssignment(LuaStatement):
    """Lua assignment statement"""
    targets: List[LuaExpression]  # Can assign to multiple variables
    values: List[LuaExpression]   # Can assign multiple values
    is_local: bool = False
    
    def accept(self, visitor: 'LuaVisitor') -> Any:
        return visitor.visit_assignment(self)


@dataclass
class LuaLocalDeclaration(LuaStatement):
    """Lua local variable declaration"""
    names: List[str]
    values: List[LuaExpression]
    
    def accept(self, visitor: 'LuaVisitor') -> Any:
        return visitor.visit_local_declaration(self)


@dataclass
class LuaFunctionDeclaration(LuaStatement):
    """Lua function declaration statement"""
    name: str
    parameters: List[str]
    body: 'LuaBlock'
    is_local: bool = False
    is_method: bool = False
    is_vararg: bool = False
    table_path: List[str] = None  # For function table.subtable.name()
    
    def __post_init__(self):
        if self.table_path is None:
            self.table_path = []
    
    def accept(self, visitor: 'LuaVisitor') -> Any:
        return visitor.visit_function_declaration(self)


@dataclass
class LuaIfStatement(LuaStatement):
    """Lua if statement"""
    condition: LuaExpression
    then_block: 'LuaBlock'
    elseif_clauses: List['LuaElseIfClause']
    else_block: Optional['LuaBlock'] = None
    
    def accept(self, visitor: 'LuaVisitor') -> Any:
        return visitor.visit_if_statement(self)


@dataclass
class LuaElseIfClause(LuaNode):
    """Lua elseif clause"""
    condition: LuaExpression
    block: 'LuaBlock'
    
    def accept(self, visitor: 'LuaVisitor') -> Any:
        return visitor.visit_elseif_clause(self)


@dataclass
class LuaWhileStatement(LuaStatement):
    """Lua while loop"""
    condition: LuaExpression
    body: 'LuaBlock'
    
    def accept(self, visitor: 'LuaVisitor') -> Any:
        return visitor.visit_while_statement(self)


@dataclass
class LuaRepeatStatement(LuaStatement):
    """Lua repeat-until loop"""
    body: 'LuaBlock'
    condition: LuaExpression
    
    def accept(self, visitor: 'LuaVisitor') -> Any:
        return visitor.visit_repeat_statement(self)


@dataclass
class LuaForStatement(LuaStatement):
    """Lua numeric for loop"""
    variable: str
    start: LuaExpression
    end: LuaExpression
    step: Optional[LuaExpression]
    body: 'LuaBlock'
    
    def accept(self, visitor: 'LuaVisitor') -> Any:
        return visitor.visit_for_statement(self)


@dataclass
class LuaForInStatement(LuaStatement):
    """Lua generic for-in loop"""
    variables: List[str]
    iterators: List[LuaExpression]
    body: 'LuaBlock'
    
    def accept(self, visitor: 'LuaVisitor') -> Any:
        return visitor.visit_for_in_statement(self)


@dataclass
class LuaBreakStatement(LuaStatement):
    """Lua break statement"""
    
    def accept(self, visitor: 'LuaVisitor') -> Any:
        return visitor.visit_break_statement(self)


@dataclass
class LuaContinueStatement(LuaStatement):
    """Lua continue statement (Lua 5.2+)"""
    
    def accept(self, visitor: 'LuaVisitor') -> Any:
        return visitor.visit_continue_statement(self)


@dataclass
class LuaReturnStatement(LuaStatement):
    """Lua return statement"""
    values: List[LuaExpression]
    
    def accept(self, visitor: 'LuaVisitor') -> Any:
        return visitor.visit_return_statement(self)


@dataclass
class LuaGotoStatement(LuaStatement):
    """Lua goto statement (Lua 5.2+)"""
    label: str
    
    def accept(self, visitor: 'LuaVisitor') -> Any:
        return visitor.visit_goto_statement(self)


@dataclass
class LuaLabelStatement(LuaStatement):
    """Lua label statement (Lua 5.2+)"""
    name: str
    
    def accept(self, visitor: 'LuaVisitor') -> Any:
        return visitor.visit_label_statement(self)


@dataclass
class LuaExpressionStatement(LuaStatement):
    """Lua expression as statement (function calls)"""
    expression: LuaExpression
    
    def accept(self, visitor: 'LuaVisitor') -> Any:
        return visitor.visit_expression_statement(self)


@dataclass
class LuaBlock(LuaNode):
    """Lua block (sequence of statements)"""
    statements: List[LuaStatement]
    
    def accept(self, visitor: 'LuaVisitor') -> Any:
        return visitor.visit_block(self)


@dataclass
class LuaComment(LuaNode):
    """Lua comment"""
    text: str
    is_multiline: bool = False
    is_documentation: bool = False
    
    def accept(self, visitor: 'LuaVisitor') -> Any:
        return visitor.visit_comment(self)


@dataclass
class LuaModule(LuaNode):
    """Lua module/chunk (complete Lua file)"""
    body: LuaBlock
    name: Optional[str] = None
    filename: Optional[str] = None
    imports: List['LuaRequireStatement'] = None
    exports: Dict[str, LuaExpression] = None
    
    def __post_init__(self):
        if self.imports is None:
            self.imports = []
        if self.exports is None:
            self.exports = {}
    
    def accept(self, visitor: 'LuaVisitor') -> Any:
        return visitor.visit_module(self)


@dataclass
class LuaRequireStatement(LuaStatement):
    """Lua require/import statement"""
    module_name: str
    alias: Optional[str] = None
    is_local: bool = True
    
    def accept(self, visitor: 'LuaVisitor') -> Any:
        return visitor.visit_require_statement(self)


# Advanced Lua Features
@dataclass
class LuaMetatableOperation(LuaExpression):
    """Lua metatable operation (getmetatable/setmetatable)"""
    operation: str  # "get" or "set"
    table: LuaExpression
    metatable: Optional[LuaExpression] = None  # For setmetatable
    
    def accept(self, visitor: 'LuaVisitor') -> Any:
        return visitor.visit_metatable_operation(self)


@dataclass
class LuaCoroutineExpression(LuaExpression):
    """Lua coroutine expression"""
    operation: str  # "create", "resume", "yield", "status", "wrap"
    function: Optional[LuaExpression] = None
    arguments: List[LuaExpression] = None
    
    def __post_init__(self):
        if self.arguments is None:
            self.arguments = []
    
    def accept(self, visitor: 'LuaVisitor') -> Any:
        return visitor.visit_coroutine_expression(self)


@dataclass
class LuaStringInterpolation(LuaExpression):
    """Lua string interpolation (custom extension)"""
    template: str
    expressions: List[LuaExpression]
    
    def accept(self, visitor: 'LuaVisitor') -> Any:
        return visitor.visit_string_interpolation(self)


@dataclass
class LuaDoStatement(LuaStatement):
    """Lua do-end block"""
    body: LuaBlock
    
    def accept(self, visitor: 'LuaVisitor') -> Any:
        return visitor.visit_do_statement(self)


# String and pattern matching
@dataclass
class LuaStringLiteral(LuaExpression):
    """Lua string literal with format information"""
    value: str
    quote_style: str = '"'  # '"', "'", or "[[]]"
    is_multiline: bool = False
    
    def accept(self, visitor: 'LuaVisitor') -> Any:
        return visitor.visit_string_literal(self)


@dataclass
class LuaNumberLiteral(LuaExpression):
    """Lua number literal"""
    value: Union[int, float]
    is_integer: bool
    is_hex: bool = False
    raw_text: str = ""
    
    def accept(self, visitor: 'LuaVisitor') -> Any:
        return visitor.visit_number_literal(self)


# Visitor Pattern
class LuaVisitor(ABC):
    """Visitor interface for Lua AST"""
    
    @abstractmethod
    def visit_module(self, node: LuaModule) -> Any:
        pass
    
    @abstractmethod
    def visit_block(self, node: LuaBlock) -> Any:
        pass
    
    @abstractmethod
    def visit_literal(self, node: LuaLiteral) -> Any:
        pass
    
    @abstractmethod
    def visit_identifier(self, node: LuaIdentifier) -> Any:
        pass
    
    @abstractmethod
    def visit_binary_operation(self, node: LuaBinaryOperation) -> Any:
        pass
    
    @abstractmethod
    def visit_unary_operation(self, node: LuaUnaryOperation) -> Any:
        pass
    
    @abstractmethod
    def visit_table_constructor(self, node: LuaTableConstructor) -> Any:
        pass
    
    @abstractmethod
    def visit_table_field(self, node: LuaTableField) -> Any:
        pass
    
    @abstractmethod
    def visit_table_access(self, node: LuaTableAccess) -> Any:
        pass
    
    @abstractmethod
    def visit_function_call(self, node: LuaFunctionCall) -> Any:
        pass
    
    @abstractmethod
    def visit_function_definition(self, node: LuaFunctionDefinition) -> Any:
        pass
    
    @abstractmethod
    def visit_vararg_expression(self, node: LuaVarargExpression) -> Any:
        pass
    
    @abstractmethod
    def visit_assignment(self, node: LuaAssignment) -> Any:
        pass
    
    @abstractmethod
    def visit_local_declaration(self, node: LuaLocalDeclaration) -> Any:
        pass
    
    @abstractmethod
    def visit_function_declaration(self, node: LuaFunctionDeclaration) -> Any:
        pass
    
    @abstractmethod
    def visit_if_statement(self, node: LuaIfStatement) -> Any:
        pass
    
    @abstractmethod
    def visit_elseif_clause(self, node: LuaElseIfClause) -> Any:
        pass
    
    @abstractmethod
    def visit_while_statement(self, node: LuaWhileStatement) -> Any:
        pass
    
    @abstractmethod
    def visit_repeat_statement(self, node: LuaRepeatStatement) -> Any:
        pass
    
    @abstractmethod
    def visit_for_statement(self, node: LuaForStatement) -> Any:
        pass
    
    @abstractmethod
    def visit_for_in_statement(self, node: LuaForInStatement) -> Any:
        pass
    
    @abstractmethod
    def visit_break_statement(self, node: LuaBreakStatement) -> Any:
        pass
    
    @abstractmethod
    def visit_continue_statement(self, node: LuaContinueStatement) -> Any:
        pass
    
    @abstractmethod
    def visit_return_statement(self, node: LuaReturnStatement) -> Any:
        pass
    
    @abstractmethod
    def visit_goto_statement(self, node: LuaGotoStatement) -> Any:
        pass
    
    @abstractmethod
    def visit_label_statement(self, node: LuaLabelStatement) -> Any:
        pass
    
    @abstractmethod
    def visit_expression_statement(self, node: LuaExpressionStatement) -> Any:
        pass
    
    @abstractmethod
    def visit_comment(self, node: LuaComment) -> Any:
        pass
    
    @abstractmethod
    def visit_require_statement(self, node: LuaRequireStatement) -> Any:
        pass
    
    @abstractmethod
    def visit_metatable_operation(self, node: LuaMetatableOperation) -> Any:
        pass
    
    @abstractmethod
    def visit_coroutine_expression(self, node: LuaCoroutineExpression) -> Any:
        pass
    
    @abstractmethod
    def visit_string_interpolation(self, node: LuaStringInterpolation) -> Any:
        pass
    
    @abstractmethod
    def visit_do_statement(self, node: LuaDoStatement) -> Any:
        pass
    
    @abstractmethod
    def visit_string_literal(self, node: LuaStringLiteral) -> Any:
        pass
    
    @abstractmethod
    def visit_number_literal(self, node: LuaNumberLiteral) -> Any:
        pass


class LuaBaseVisitor(LuaVisitor):
    """Base visitor with default implementations"""
    
    def visit_module(self, node: LuaModule) -> Any:
        return node.body.accept(self)
    
    def visit_block(self, node: LuaBlock) -> Any:
        results = []
        for stmt in node.statements:
            results.append(stmt.accept(self))
        return results
    
    def visit_literal(self, node: LuaLiteral) -> Any:
        return node.value
    
    def visit_identifier(self, node: LuaIdentifier) -> Any:
        return node.name
    
    def visit_binary_operation(self, node: LuaBinaryOperation) -> Any:
        left = node.left.accept(self)
        right = node.right.accept(self)
        return (left, node.operator, right)
    
    def visit_unary_operation(self, node: LuaUnaryOperation) -> Any:
        operand = node.operand.accept(self)
        return (node.operator, operand)
    
    def visit_table_constructor(self, node: LuaTableConstructor) -> Any:
        return [field.accept(self) for field in node.fields]
    
    def visit_table_field(self, node: LuaTableField) -> Any:
        key = node.key.accept(self) if node.key else None
        value = node.value.accept(self)
        return (key, value)
    
    def visit_table_access(self, node: LuaTableAccess) -> Any:
        table = node.table.accept(self)
        key = node.key.accept(self)
        return (table, key)
    
    def visit_function_call(self, node: LuaFunctionCall) -> Any:
        function = node.function.accept(self)
        arguments = [arg.accept(self) for arg in node.arguments]
        return (function, arguments)
    
    def visit_function_definition(self, node: LuaFunctionDefinition) -> Any:
        body = node.body.accept(self)
        return (node.parameters, body)
    
    def visit_vararg_expression(self, node: LuaVarargExpression) -> Any:
        return "..."
    
    def visit_assignment(self, node: LuaAssignment) -> Any:
        targets = [target.accept(self) for target in node.targets]
        values = [value.accept(self) for value in node.values]
        return (targets, values)
    
    def visit_local_declaration(self, node: LuaLocalDeclaration) -> Any:
        values = [value.accept(self) for value in node.values]
        return (node.names, values)
    
    def visit_function_declaration(self, node: LuaFunctionDeclaration) -> Any:
        body = node.body.accept(self)
        return (node.name, node.parameters, body)
    
    def visit_if_statement(self, node: LuaIfStatement) -> Any:
        condition = node.condition.accept(self)
        then_block = node.then_block.accept(self)
        elseifs = [clause.accept(self) for clause in node.elseif_clauses]
        else_block = node.else_block.accept(self) if node.else_block else None
        return (condition, then_block, elseifs, else_block)
    
    def visit_elseif_clause(self, node: LuaElseIfClause) -> Any:
        condition = node.condition.accept(self)
        block = node.block.accept(self)
        return (condition, block)
    
    def visit_while_statement(self, node: LuaWhileStatement) -> Any:
        condition = node.condition.accept(self)
        body = node.body.accept(self)
        return (condition, body)
    
    def visit_repeat_statement(self, node: LuaRepeatStatement) -> Any:
        body = node.body.accept(self)
        condition = node.condition.accept(self)
        return (body, condition)
    
    def visit_for_statement(self, node: LuaForStatement) -> Any:
        start = node.start.accept(self)
        end = node.end.accept(self)
        step = node.step.accept(self) if node.step else None
        body = node.body.accept(self)
        return (node.variable, start, end, step, body)
    
    def visit_for_in_statement(self, node: LuaForInStatement) -> Any:
        iterators = [iter.accept(self) for iter in node.iterators]
        body = node.body.accept(self)
        return (node.variables, iterators, body)
    
    def visit_break_statement(self, node: LuaBreakStatement) -> Any:
        return "break"
    
    def visit_continue_statement(self, node: LuaContinueStatement) -> Any:
        return "continue"
    
    def visit_return_statement(self, node: LuaReturnStatement) -> Any:
        values = [value.accept(self) for value in node.values]
        return values
    
    def visit_goto_statement(self, node: LuaGotoStatement) -> Any:
        return node.label
    
    def visit_label_statement(self, node: LuaLabelStatement) -> Any:
        return node.name
    
    def visit_expression_statement(self, node: LuaExpressionStatement) -> Any:
        return node.expression.accept(self)
    
    def visit_comment(self, node: LuaComment) -> Any:
        return node.text
    
    def visit_require_statement(self, node: LuaRequireStatement) -> Any:
        return (node.module_name, node.alias)
    
    def visit_metatable_operation(self, node: LuaMetatableOperation) -> Any:
        table = node.table.accept(self)
        metatable = node.metatable.accept(self) if node.metatable else None
        return (node.operation, table, metatable)
    
    def visit_coroutine_expression(self, node: LuaCoroutineExpression) -> Any:
        function = node.function.accept(self) if node.function else None
        arguments = [arg.accept(self) for arg in node.arguments]
        return (node.operation, function, arguments)
    
    def visit_string_interpolation(self, node: LuaStringInterpolation) -> Any:
        expressions = [expr.accept(self) for expr in node.expressions]
        return (node.template, expressions)
    
    def visit_do_statement(self, node: LuaDoStatement) -> Any:
        return node.body.accept(self)
    
    def visit_string_literal(self, node: LuaStringLiteral) -> Any:
        return node.value
    
    def visit_number_literal(self, node: LuaNumberLiteral) -> Any:
        return node.value


# Helper functions for creating common AST nodes
def create_lua_identifier(name: str) -> LuaIdentifier:
    """Create a Lua identifier node"""
    return LuaIdentifier(name=name)


def create_lua_number(value: Union[int, float], raw_text: str = "") -> LuaNumberLiteral:
    """Create a Lua number literal node"""
    return LuaNumberLiteral(
        value=value,
        is_integer=isinstance(value, int),
        raw_text=raw_text or str(value)
    )


def create_lua_string(value: str, quote_style: str = '"') -> LuaStringLiteral:
    """Create a Lua string literal node"""
    return LuaStringLiteral(
        value=value,
        quote_style=quote_style,
        is_multiline=quote_style.startswith('[[')
    )


def create_lua_table(fields: List[LuaTableField]) -> LuaTableConstructor:
    """Create a Lua table constructor node"""
    return LuaTableConstructor(fields=fields)


def create_lua_function(parameters: List[str], body: LuaBlock, 
                       is_vararg: bool = False) -> LuaFunctionDefinition:
    """Create a Lua function definition node"""
    return LuaFunctionDefinition(
        parameters=parameters,
        body=body,
        is_vararg=is_vararg
    )


def create_lua_block(statements: List[LuaStatement]) -> LuaBlock:
    """Create a Lua block node"""
    return LuaBlock(statements=statements)


def create_lua_module(body: LuaBlock, name: Optional[str] = None) -> LuaModule:
    """Create a Lua module node"""
    return LuaModule(body=body, name=name) 