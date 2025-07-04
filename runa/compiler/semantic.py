"""
Runa Semantic Analyzer (Phase 1.3)

Performs semantic analysis on the AST produced by the parser:
1. Builds symbol tables with lexical scoping
2. Infers and validates types for expressions and statements
3. Reports semantic errors (duplicate declarations, undefined identifiers, type mismatches)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Union

from .ast_nodes import (
    ASTNode,
    Program,
    Statement,
    Expression,
    LetStatement,
    DefineStatement,
    SetStatement,
    Identifier,
    IntegerLiteral,
    FloatLiteral,
    StringLiteral,
    BooleanLiteral,
    ListLiteral,
    BasicType,
    GenericType,
    TypeExpression,
    BinaryExpression,
    BinaryOperator,
    FunctionCall,
    UnionType as UT,
)

# ---------------------------------------------------------------------------
#  Semantic Error
# ---------------------------------------------------------------------------

class SemanticError(Exception):
    """Raised when a semantic error is encountered during analysis."""

    def __init__(self, message: str, node: Optional[ASTNode] = None):
        self.message = message
        self.node = node
        super().__init__(message)

# ---------------------------------------------------------------------------
#  Symbol & Scope
# ---------------------------------------------------------------------------

@dataclass
class Symbol:
    """Represents a declared symbol in a scope."""

    name: str
    type: TypeExpression
    mutable: bool = True  # False for constants

class Scope:
    """Lexical scope containing symbols and reference to parent scope."""

    def __init__(self, parent: Optional[Scope] = None):
        self.parent: Optional[Scope] = parent
        self.symbols: Dict[str, Symbol] = {}

    # -------------------- Symbol Management --------------------
    def declare(self, symbol: Symbol):
        if symbol.name in self.symbols:
            raise SemanticError(f"Duplicate declaration of '{symbol.name}'")
        self.symbols[symbol.name] = symbol

    def lookup(self, name: str) -> Optional[Symbol]:
        scope: Optional[Scope] = self
        while scope is not None:
            if name in scope.symbols:
                return scope.symbols[name]
            scope = scope.parent
        return None

# ---------------------------------------------------------------------------
#  Semantic Analyzer Visitor
# ---------------------------------------------------------------------------

class SemanticAnalyzer:
    """Walks the AST, builds symbol tables, and validates types."""

    def __init__(self):
        self.global_scope = Scope()
        self.current_scope = self.global_scope
        self.errors: List[SemanticError] = []

    # -------------------- Entry Point --------------------
    def analyze(self, program: Program):
        try:
            program.accept(self)
        except SemanticError as e:
            self.errors.append(e)
        return self.errors

    # -------------------- Scope Helpers --------------------
    def push_scope(self):
        self.current_scope = Scope(self.current_scope)

    def pop_scope(self):
        if self.current_scope.parent is not None:
            self.current_scope = self.current_scope.parent

    # -------------------- Visitor Dispatch --------------------
    def visit_program(self, node: Program):
        for stmt in node.statements:
            stmt.accept(self)

    # -------------------- Statement Visitors --------------------
    def visit_let_statement(self, node: LetStatement):
        # Evaluate expression type
        value_type = self.infer_type(node.value)
        # If annotation provided, validate compatibility
        if node.type_annotation is not None:
            annotated_type = node.type_annotation
            if not self.is_assignable(value_type, annotated_type):
                self.errors.append(SemanticError(
                    f"Type mismatch in let statement: cannot assign {value_type} to {annotated_type}",
                    node,
                ))
            final_type = annotated_type
        else:
            final_type = value_type
        # Declare symbol
        symbol = Symbol(name=node.identifier, type=final_type, mutable=True)
        try:
            self.current_scope.declare(symbol)
        except SemanticError as e:
            self.errors.append(e)

    def visit_define_statement(self, node: DefineStatement):
        value_type = self.infer_type(node.value)
        if node.type_annotation is not None:
            annotated_type = node.type_annotation
            if not self.is_assignable(value_type, annotated_type):
                self.errors.append(SemanticError(
                    f"Type mismatch in define statement: cannot assign {value_type} to {annotated_type}",
                    node,
                ))
            final_type = annotated_type
        else:
            final_type = value_type
        symbol = Symbol(name=node.identifier, type=final_type, mutable=not node.is_constant)
        try:
            self.current_scope.declare(symbol)
        except SemanticError as e:
            self.errors.append(e)

    def visit_set_statement(self, node: SetStatement):
        # Only simple identifier targets for now
        if isinstance(node.target, Identifier):
            symbol = self.current_scope.lookup(node.target.name)
            if symbol is None:
                self.errors.append(SemanticError(f"Undefined variable '{node.target.name}'", node))
                return
            if not symbol.mutable:
                self.errors.append(SemanticError(f"Cannot assign to constant '{symbol.name}'", node))
            value_type = self.infer_type(node.value)
            if not self.is_assignable(value_type, symbol.type):
                self.errors.append(SemanticError(
                    f"Type mismatch: cannot assign {value_type} to {symbol.type} for '{symbol.name}'",
                    node,
                ))
        else:
            # More complex assignable targets can be handled later
            pass

    def visit_if_statement(self, node):
        # Ensure condition is boolean-compatible
        cond_type = self.infer_type(node.condition)
        if not self.is_assignable(cond_type, BasicType("Boolean")):
            self.errors.append(SemanticError("If condition must be Boolean-compatible", node))
        # New scope for then block
        self.push_scope()
        for stmt in node.then_block:
            stmt.accept(self)
        self.pop_scope()
        # Elif clauses
        for cond, block in node.elif_clauses:
            cond_type = self.infer_type(cond)
            if not self.is_assignable(cond_type, BasicType("Boolean")):
                self.errors.append(SemanticError("Else-if condition must be Boolean-compatible", node))
            self.push_scope()
            for stmt in block:
                stmt.accept(self)
            self.pop_scope()
        # Else block
        if node.else_block:
            self.push_scope()
            for stmt in node.else_block:
                stmt.accept(self)
            self.pop_scope()

    def visit_while_loop(self, node):
        """Validate while loop semantics."""
        # Ensure condition is boolean-compatible
        cond_type = self.infer_type(node.condition)
        if not self.is_assignable(cond_type, BasicType("Boolean")):
            self.errors.append(SemanticError("While condition must be Boolean-compatible", node))
        
        # New scope for loop body
        self.push_scope()
        for stmt in node.block:
            stmt.accept(self)
        self.pop_scope()

    def visit_for_loop(self, node):
        """Validate for loop semantics."""
        # Check that iterable expression is valid
        iterable_type = self.infer_type(node.iterable)
        
        # For now, assume any iterable is valid (List, etc.)
        # In a more complete implementation, we'd check if it's actually iterable
        
        # New scope for loop body with loop variable
        self.push_scope()
        
        # Declare loop variable (assume Any type for elements)
        loop_var_symbol = Symbol(name=node.variable, type=BasicType("Any"), mutable=True)
        try:
            self.current_scope.declare(loop_var_symbol)
        except SemanticError as e:
            self.errors.append(e)
        
        # Process loop body
        for stmt in node.block:
            stmt.accept(self)
        
        self.pop_scope()

    def visit_for_each_loop(self, node):
        """Validate for-each loop."""
        # Ensure iterable expression is valid (Any type acceptable)
        self.infer_type(node.iterable)
        self.push_scope()
        loop_var_symbol = Symbol(name=node.variable, type=BasicType("Any"), mutable=True)
        try:
            self.current_scope.declare(loop_var_symbol)
        except SemanticError as e:
            self.errors.append(e)
        for stmt in node.block:
            stmt.accept(self)
        self.pop_scope()

    def visit_display_statement(self, node):
        # Validate that the value is a valid expression (no type requirement)
        self.infer_type(node.value)
        if node.prefix:
            self.infer_type(node.prefix)

    def visit_return_statement(self, node):
        # We aren't inside function bodies yet; just validate expression
        if node.value:
            self.infer_type(node.value)

    def visit_expression_statement(self, node):
        self.infer_type(node.expression)

    # Placeholder visitors for unimplemented constructs
    def generic_visit(self, node):
        # No-op for nodes not yet semantically analyzed
        pass

    # -------------------- Expression Visitors --------------------
    def visit_identifier(self, node: Identifier):
        symbol = self.current_scope.lookup(node.name)
        if symbol is None:
            self.errors.append(SemanticError(f"Undefined variable '{node.name}'", node))
        return symbol.type

    def visit_integer_literal(self, node: IntegerLiteral):
        return BasicType("Integer")

    def visit_float_literal(self, node: FloatLiteral):
        return BasicType("Float")

    def visit_string_literal(self, node: StringLiteral):
        return BasicType("String")

    def visit_boolean_literal(self, node: BooleanLiteral):
        return BasicType("Boolean")

    def visit_list_literal(self, node: ListLiteral):
        elem_type_objs = [self.infer_type(el) for el in node.elements]
        # If all element types are identical BasicType, keep that; else promote to Any
        if elem_type_objs and all(isinstance(t, BasicType) for t in elem_type_objs):
            names = {t.name for t in elem_type_objs}
            if len(names) == 1:
                element_type = BasicType(next(iter(names)))
            else:
                element_type = BasicType("Any")
        else:
            element_type = BasicType("Any")
        return GenericType("List", [element_type])

    def visit_binary_expression(self, node: BinaryExpression):
        left_type = self.infer_type(node.left)
        right_type = self.infer_type(node.right)
        # Simplified numeric/boolean handling
        if node.operator in {
            BinaryOperator.PLUS,
            BinaryOperator.MINUS,
            BinaryOperator.MULTIPLY,
            BinaryOperator.DIVIDE,
            BinaryOperator.MODULO,
            BinaryOperator.POWER,
        }:
            # Arithmetic: require numeric operands
            if left_type.name not in {"Integer", "Float"} or right_type.name not in {"Integer", "Float"}:
                self.errors.append(SemanticError("Arithmetic operators require numeric operands", node))
            # Result type: Float if either operand is Float else Integer
            if left_type.name == "Float" or right_type.name == "Float":
                return BasicType("Float")
            return BasicType("Integer")
        elif node.operator in {
            BinaryOperator.EQUALS,
            BinaryOperator.NOT_EQUALS,
            BinaryOperator.GREATER_THAN,
            BinaryOperator.LESS_THAN,
            BinaryOperator.GREATER_EQUAL,
            BinaryOperator.LESS_EQUAL,
        }:
            # Comparison: result is Boolean
            return BasicType("Boolean")
        elif node.operator in {BinaryOperator.AND, BinaryOperator.OR}:
            # Logical operators require boolean operands
            if left_type.name != "Boolean" or right_type.name != "Boolean":
                self.errors.append(SemanticError("Logical operators require Boolean operands", node))
            return BasicType("Boolean")
        else:
            return BasicType("Any")

    def visit_function_call(self, node: FunctionCall):
        # For now, assume function returns Any
        for _, arg_value in node.arguments:
            self.infer_type(arg_value)
        return BasicType("Any")

    def visit_process_definition(self, node):
        """Validate a process/function definition."""
        # Add function symbol to current scope
        func_symbol = Symbol(name=node.name, type=BasicType("Function"), mutable=False)
        try:
            self.current_scope.declare(func_symbol)
        except SemanticError as e:
            self.errors.append(e)
        # New scope for parameters and body
        self.push_scope()
        for param in node.parameters:
            param_symbol = Symbol(name=param.name, type=BasicType("Any"), mutable=False)
            try:
                self.current_scope.declare(param_symbol)
            except SemanticError as e:
                self.errors.append(e)
        # Visit body statements
        for stmt in node.body:
            stmt.accept(self)
        self.pop_scope()

    # -------------------- Utility Methods --------------------
    def infer_type(self, expr: Expression) -> TypeExpression:
        """Infer the type of an expression via the expression's accept method."""
        try:
            return expr.accept(self)
        except AttributeError:
            # If expression type not handled yet, return Any
            return BasicType("Any")

    def is_assignable(self, source: TypeExpression, target: TypeExpression) -> bool:
        """Check if a value of source type can be assigned to target type (simplified)."""
        # Any matches everything
        if isinstance(target, BasicType) and target.name == "Any":
            return True
        if isinstance(source, BasicType) and source.name == "Any":
            return True

        # BasicType to BasicType equality
        if isinstance(target, BasicType) and isinstance(source, BasicType):
            return source.name == target.name

        # GenericType compatibility (covariant on type args)
        if isinstance(target, GenericType) and isinstance(source, GenericType):
            if target.base_type != source.base_type or len(target.type_args) != len(source.type_args):
                return False
            return all(self.is_assignable(s, t) for s, t in zip(source.type_args, target.type_args))

        # UnionType: source must be compatible with any member, or every member of source compatible with target
        if isinstance(target, UT):
            return any(self.is_assignable(source, t) for t in target.types)
        if isinstance(source, UT):
            return all(self.is_assignable(s, target) for s in source.types)

        return False

# ---------------------------------------------------------------------------
#  Public API Helper
# ---------------------------------------------------------------------------

def analyze_semantics(program: Program) -> List[SemanticError]:
    analyzer = SemanticAnalyzer()
    return analyzer.analyze(program) 