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
    IntersectionType,
    OptionalType,
    FunctionType,
    # Pattern matching
    MatchStatement,
    MatchCase,
    Pattern,
    LiteralPattern,
    IdentifierPattern,
    WildcardPattern,
    ListPattern,
    # Error handling
    TryStatement,
    CatchClause,
    ThrowStatement,
    # Module system
    ImportStatement,
    ExportStatement,
    ModuleDeclaration,
    # Async/await and concurrency
    AwaitExpression,
    AsyncProcessDefinition,
    SendStatement,
    AtomicBlock,
    LockStatement,
    # Memory management
    DeleteStatement,
    AnnotatedVariableDeclaration,
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
        self.warnings: List[Dict] = []

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

    def visit_for_range_loop(self, node):
        """Validate for-range loop semantics."""
        # Push new scope for loop variable
        self.push_scope()
        
        # Validate start and end expressions
        start_type = self.infer_type(node.start)
        end_type = self.infer_type(node.end)
        
        # Start and end should be integers
        if start_type and start_type.name != "Integer":
            self.errors.append(SemanticError("For-range start value must be an integer", node.start))
        if end_type and end_type.name != "Integer":
            self.errors.append(SemanticError("For-range end value must be an integer", node.end))
        
        # Validate step if present
        if node.step:
            step_type = self.infer_type(node.step)
            if step_type and step_type.name != "Integer":
                self.errors.append(SemanticError("For-range step value must be an integer", node.step))
        
        # Declare loop variable in new scope
        loop_var_symbol = Symbol(node.variable, BasicType("Integer"))
        self.current_scope.declare(loop_var_symbol)
        
        # Validate loop body
        for stmt in node.block:
            stmt.accept(self)
        
        self.pop_scope()
    
    def visit_do_while_loop(self, node):
        """Validate do-while loop semantics."""
        # Push new scope for loop body
        self.push_scope()
        
        # Validate loop body
        for stmt in node.block:
            stmt.accept(self)
        
        # Validate condition
        condition_type = self.infer_type(node.condition)
        if condition_type and condition_type.name != "Boolean":
            self.errors.append(SemanticError("Do-while condition must be boolean", node.condition))
        
        self.pop_scope()
    
    def visit_repeat_loop(self, node):
        """Validate repeat loop semantics."""
        # Push new scope for loop body
        self.push_scope()
        
        # Validate count expression
        count_type = self.infer_type(node.count)
        if count_type and count_type.name != "Integer":
            self.errors.append(SemanticError("Repeat count must be an integer", node.count))
        
        # Validate loop body
        for stmt in node.block:
            stmt.accept(self)
        
        self.pop_scope()
    
    def visit_match_statement(self, node):
        """Validate match statement semantics."""
        # Validate the expression being matched
        match_type = self.infer_type(node.value)
        
        # Validate each case
        for case in node.cases:
            # Push new scope for pattern variables
            self.push_scope()
            
            # Validate pattern against match type
            self.validate_pattern(case.pattern, match_type)
            
            # Validate guard if present
            if case.guard:
                guard_type = self.infer_type(case.guard)
                if guard_type and guard_type.name != "Boolean":
                    self.errors.append(SemanticError("Match guard must be boolean", case.guard))
            
            # Validate case body
            for stmt in case.block:
                stmt.accept(self)
            
            self.pop_scope()
        
        # TODO: Add exhaustiveness checking
    
    def validate_pattern(self, pattern, expected_type):
        """Validate a pattern against the expected type."""
        if isinstance(pattern, LiteralPattern):
            # Validate literal pattern
            literal_type = self.infer_type(pattern.value)
            if expected_type and literal_type and literal_type.name != expected_type.name:
                self.errors.append(SemanticError(
                    f"Pattern literal type {literal_type.name} doesn't match {expected_type.name}",
                    pattern.value
                ))
        
        elif isinstance(pattern, IdentifierPattern):
            # Declare pattern variable in current scope
            symbol = Symbol(pattern.name, expected_type or BasicType("Any"))
            try:
                self.current_scope.declare(symbol)
            except SemanticError as e:
                self.errors.append(e)
        
        elif isinstance(pattern, WildcardPattern):
            # Wildcard always matches
            pass
        
        elif isinstance(pattern, ListPattern):
            # Validate list pattern
            if expected_type and expected_type.name != "List":
                self.errors.append(SemanticError(
                    f"List pattern cannot match type {expected_type.name}",
                    pattern
                ))
            
            # For now, assume list element type is Any
            element_type = BasicType("Any")
            
            # Validate element patterns
            for element_pattern in pattern.elements:
                self.validate_pattern(element_pattern, element_type)
            
            # Validate rest pattern if present
            if pattern.rest:
                rest_symbol = Symbol(pattern.rest, BasicType("List"))
                try:
                    self.current_scope.declare(rest_symbol)
                except SemanticError as e:
                    self.errors.append(e)
    
    def visit_literal_pattern(self, node):
        """Validate literal pattern."""
        return self.infer_type(node.value)
    
    def visit_identifier_pattern(self, node):
        """Identifier patterns are handled in validate_pattern."""
        pass
    
    def visit_wildcard_pattern(self, node):
        """Wildcard patterns always match."""
        pass
    
    def visit_list_pattern(self, node):
        """List patterns are handled in validate_pattern."""
        pass
    
    def visit_try_statement(self, node):
        """Validate try statement semantics."""
        # Push new scope for try block
        self.push_scope()
        
        # Validate try block
        for stmt in node.try_block:
            stmt.accept(self)
        
        self.pop_scope()
        
        # Validate catch clauses
        for catch_clause in node.catch_clauses:
            # Push new scope for catch block
            self.push_scope()
            
            # Declare exception variable if present
            if catch_clause.exception_name:
                exception_type = catch_clause.exception_type or BasicType("Exception")
                symbol = Symbol(catch_clause.exception_name, exception_type)
                try:
                    self.current_scope.declare(symbol)
                except SemanticError as e:
                    self.errors.append(e)
            
            # Validate catch block
            for stmt in catch_clause.block:
                stmt.accept(self)
            
            self.pop_scope()
        
        # Validate finally block if present
        if node.finally_block:
            self.push_scope()
            
            for stmt in node.finally_block:
                stmt.accept(self)
            
            self.pop_scope()
    
    def visit_throw_statement(self, node):
        """Validate throw statement semantics."""
        # Validate the exception expression
        exception_type = self.infer_type(node.exception)
        
        # For now, accept any type as throwable
        # In a more strict type system, we might require specific exception types
    
    def visit_import_statement(self, node):
        """Validate import statement semantics."""
        # For now, just validate that the module path is a valid string
        # In a complete implementation, we would:
        # 1. Check if the module exists
        # 2. Validate imported names exist in the module
        # 3. Add imported symbols to current scope
        
        if node.alias:
            # Create symbol for the module alias
            module_symbol = Symbol(node.alias, BasicType("Module"))
            try:
                self.current_scope.declare(module_symbol)
            except SemanticError as e:
                self.errors.append(e)
        
        if node.imported_names:
            # Create symbols for imported names
            for name in node.imported_names:
                symbol = Symbol(name, BasicType("Any"))  # Unknown type for now
                try:
                    self.current_scope.declare(symbol)
                except SemanticError as e:
                    self.errors.append(e)
    
    def visit_export_statement(self, node):
        """Validate export statement semantics."""
        # Validate that exported names exist in current scope
        if node.exported_names:
            for name in node.exported_names:
                symbol = self.current_scope.lookup(name)
                if symbol is None:
                    self.errors.append(SemanticError(f"Cannot export undefined symbol '{name}'", node))
    
    def visit_module_declaration(self, node):
        """Validate module declaration semantics."""
        # Create new scope for module
        self.push_scope()
        
        # Process module body
        for stmt in node.body:
            stmt.accept(self)
        
        self.pop_scope()
    
    def visit_await_expression(self, node):
        """Validate await expression semantics."""
        # Validate the awaited expression
        awaited_type = self.infer_type(node.expression)
        
        # For now, assume any type can be awaited
        # In a complete implementation, we would check for Future/Promise types
        return awaited_type
    
    def visit_async_process_definition(self, node):
        """Validate async process definition semantics."""
        # Similar to regular process but async
        func_symbol = Symbol(name=node.name, type=BasicType("AsyncFunction"), mutable=False)
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
    
    def visit_send_statement(self, node):
        """Validate send statement semantics."""
        # Validate message and target expressions
        self.infer_type(node.message)
        self.infer_type(node.target)
        
        # For now, assume any message can be sent to any target
        # In a complete implementation, we would validate actor types
    
    def visit_atomic_block(self, node):
        """Validate atomic block semantics."""
        # Create new scope for atomic block
        self.push_scope()
        
        # Process atomic block body
        for stmt in node.body:
            stmt.accept(self)
        
        self.pop_scope()
    
    def visit_lock_statement(self, node):
        """Validate lock statement semantics."""
        # Validate resource expression
        self.infer_type(node.resource)
        
        # Create new scope for lock body
        self.push_scope()
        
        # Process lock body
        for stmt in node.body:
            stmt.accept(self)
        
        self.pop_scope()
    
    def visit_delete_statement(self, node):
        """Validate delete statement semantics."""
        # Validate target expression
        target_type = self.infer_type(node.target)
        
        # For now, assume any expression can be deleted
        # In a complete implementation, we would check for ownership
    
    def visit_annotated_variable_declaration(self, node):
        """Validate annotated variable declaration semantics."""
        # Validate memory annotations (basic check for now)
        for annotation in node.memory_annotations:
            # For now, just accept all annotations
            # In a complete implementation, we would validate:
            # - Ownership compatibility
            # - Lifetime validity
            # - Borrowing rules
            pass
        
        # Validate the base declaration
        node.base_declaration.accept(self)

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
        """Check if a value of source type can be assigned to target type with comprehensive validation."""
        # Null checks
        if source is None or target is None:
            return False
            
        # Any matches everything
        if isinstance(target, BasicType) and target.name == "Any":
            return True
        if isinstance(source, BasicType) and source.name == "Any":
            return True

        # BasicType to BasicType with numeric coercion
        if isinstance(target, BasicType) and isinstance(source, BasicType):
            if source.name == target.name:
                return True
            # Allow integer to float coercion
            if source.name == "Integer" and target.name == "Float":
                return True
            # Allow boolean to string coercion for display
            if source.name == "Boolean" and target.name == "String":
                return True
            return False

        # GenericType compatibility with proper variance
        if isinstance(target, GenericType) and isinstance(source, GenericType):
            if target.base_type != source.base_type or len(target.type_args) != len(source.type_args):
                return False
            
            # Special handling for List types (covariant in element type)
            if target.base_type == "List":
                return all(self.is_assignable(s, t) for s, t in zip(source.type_args, target.type_args))
            
            # Dictionary types (contravariant in key, covariant in value)
            if target.base_type == "Dictionary" and len(target.type_args) == 2:
                key_compatible = self.is_assignable(target.type_args[0], source.type_args[0])  # contravariant
                value_compatible = self.is_assignable(source.type_args[1], target.type_args[1])  # covariant
                return key_compatible and value_compatible
                
            return all(self.is_assignable(s, t) for s, t in zip(source.type_args, target.type_args))

        # UnionType: source must be compatible with any member
        if isinstance(target, UT):
            return any(self.is_assignable(source, t) for t in target.types)
        if isinstance(source, UT):
            return all(self.is_assignable(s, target) for s in source.types)

        # IntersectionType: source must be compatible with all members
        if isinstance(target, IntersectionType):
            return all(self.is_assignable(source, t) for t in target.types)
        if isinstance(source, IntersectionType):
            return any(self.is_assignable(s, target) for s in source.types)
        
        # OptionalType: source must be compatible with inner type or None
        if isinstance(target, OptionalType):
            return (self.is_assignable(source, target.inner_type) or 
                   isinstance(source, BasicType) and source.name == "None")
        if isinstance(source, OptionalType):
            return self.is_assignable(source.inner_type, target)
        
        # FunctionType compatibility with proper variance
        if isinstance(target, FunctionType) and isinstance(source, FunctionType):
            if len(target.param_types) != len(source.param_types):
                return False
            # Contravariant on parameters, covariant on return type
            params_compatible = all(self.is_assignable(t, s) for s, t in zip(source.param_types, target.param_types))
            return_compatible = self.is_assignable(source.return_type, target.return_type)
            return params_compatible and return_compatible

        return False
    
    def validate_type_expression(self, type_expr: TypeExpression) -> List[str]:
        """Validate a type expression and return list of validation errors."""
        errors = []
        
        if isinstance(type_expr, BasicType):
            valid_basic_types = {"Integer", "Float", "String", "Boolean", "Any", "Void", "None"}
            if type_expr.name not in valid_basic_types:
                errors.append(f"Unknown basic type: {type_expr.name}")
        
        elif isinstance(type_expr, GenericType):
            # Validate base type
            valid_generic_bases = {"List", "Dictionary", "Optional", "Function"}
            if type_expr.base_type not in valid_generic_bases:
                errors.append(f"Unknown generic type: {type_expr.base_type}")
            
            # Validate type arguments
            if type_expr.base_type == "List" and len(type_expr.type_args) != 1:
                errors.append("List type must have exactly one type argument")
            elif type_expr.base_type == "Dictionary" and len(type_expr.type_args) != 2:
                errors.append("Dictionary type must have exactly two type arguments")
            elif type_expr.base_type == "Optional" and len(type_expr.type_args) != 1:
                errors.append("Optional type must have exactly one type argument")
            
            # Recursively validate type arguments
            for arg in type_expr.type_args:
                errors.extend(self.validate_type_expression(arg))
        
        elif isinstance(type_expr, UT):
            if len(type_expr.types) < 2:
                errors.append("Union type must have at least two component types")
            
            # Check for redundant types
            type_names = set()
            for component in type_expr.types:
                type_str = str(component)
                if type_str in type_names:
                    errors.append(f"Redundant type in union: {type_str}")
                type_names.add(type_str)
                
                # Recursively validate component types
                errors.extend(self.validate_type_expression(component))
        
        elif isinstance(type_expr, IntersectionType):
            if len(type_expr.types) < 2:
                errors.append("Intersection type must have at least two component types")
            
            # Recursively validate component types
            for component in type_expr.types:
                errors.extend(self.validate_type_expression(component))
        
        elif isinstance(type_expr, OptionalType):
            # Recursively validate inner type
            errors.extend(self.validate_type_expression(type_expr.inner_type))
        
        elif isinstance(type_expr, FunctionType):
            # Validate parameter types
            for param_type in type_expr.param_types:
                errors.extend(self.validate_type_expression(param_type))
            
            # Validate return type
            errors.extend(self.validate_type_expression(type_expr.return_type))
        
        return errors
    
    def check_type_compatibility(self, expr_type: TypeExpression, expected_type: TypeExpression, context: str = "") -> None:
        """Check type compatibility and add error if incompatible."""
        if not self.is_assignable(expr_type, expected_type):
            context_str = f" in {context}" if context else ""
            self.errors.append(SemanticError(
                f"Type mismatch{context_str}: expected {expected_type}, got {expr_type}"
            ))
    
    def resolve_numeric_type(self, left_type: TypeExpression, right_type: TypeExpression) -> TypeExpression:
        """Resolve the result type of numeric operations."""
        if not isinstance(left_type, BasicType) or not isinstance(right_type, BasicType):
            return BasicType("Any")
        
        # If either operand is float, result is float
        if left_type.name == "Float" or right_type.name == "Float":
            return BasicType("Float")
        
        # If both are integers, result is integer
        if left_type.name == "Integer" and right_type.name == "Integer":
            return BasicType("Integer")
        
        # Otherwise, fallback to Any
        return BasicType("Any")
    
    # Add visitor methods for advanced type expressions
    def visit_basic_type(self, node):
        """Visit basic type node."""
        return node
    
    def visit_generic_type(self, node):
        """Visit generic type node."""
        # Validate type arguments
        for type_arg in node.type_args:
            type_arg.accept(self)
        return node
    
    def visit_union_type(self, node):
        """Visit union type node."""
        # Validate all component types
        for component_type in node.types:
            component_type.accept(self)
        return node
    
    def visit_intersection_type(self, node):
        """Visit intersection type node."""
        # Validate all component types
        for component_type in node.types:
            component_type.accept(self)
        return node
    
    def visit_optional_type(self, node):
        """Visit optional type node."""
        # Validate inner type
        node.inner_type.accept(self)
        return node
    
    def visit_function_type(self, node):
        """Visit function type node."""
        # Validate parameter and return types
        for param_type in node.param_types:
            param_type.accept(self)
        node.return_type.accept(self)
        return node
    
    def reset(self):
        """Reset analyzer state for new analysis."""
        self.global_scope = Scope()
        self.current_scope = self.global_scope
        self.errors.clear()
        self.warnings.clear()
    
    def get_warnings(self) -> List[Dict]:
        """Get accumulated warnings."""
        return self.warnings.copy()
    
    def add_warning(self, message: str, line: int = 0, column: int = 0, length: int = 10):
        """Add a warning to the warnings list."""
        self.warnings.append({
            'message': message,
            'line': line,
            'column': column,
            'length': length
        })

# ---------------------------------------------------------------------------
#  Public API Helper
# ---------------------------------------------------------------------------

def analyze_semantics(program: Program) -> List[SemanticError]:
    analyzer = SemanticAnalyzer()
    return analyzer.analyze(program) 