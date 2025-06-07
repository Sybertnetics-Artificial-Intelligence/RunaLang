"""
Semantic Analyzer for Runa Programming Language.

This module implements comprehensive semantic analysis including:
- Symbol table management
- Type checking and inference
- Scope resolution
- Variable usage analysis
- Function signature validation
- Natural language construct validation
"""

from typing import List, Optional, Dict, Set, Any, Type as TypingType
from dataclasses import dataclass
from enum import Enum, auto

from .ast_nodes import *
from .symbol_table import (
    SymbolTable, Symbol, FunctionSymbol, SymbolType, 
    SymbolVisibility, ScopeType
)
from .errors import (
    SourcePosition, RunaSemanticError, ErrorReporter, 
    semantic_error, ErrorSeverity
)


class AnalysisPass(Enum):
    """Different analysis passes."""
    SYMBOL_COLLECTION = auto()
    TYPE_CHECKING = auto()
    USAGE_ANALYSIS = auto()
    FINAL_VALIDATION = auto()


@dataclass
class AnalysisResult:
    """Result of semantic analysis."""
    success: bool
    symbol_table: Optional[SymbolTable] = None
    errors: List[RunaSemanticError] = None
    warnings: List[RunaSemanticError] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []
        if self.warnings is None:
            self.warnings = []


class SemanticAnalyzer(ASTVisitor):
    """
    Comprehensive semantic analyzer for Runa programs.
    
    Performs multi-pass analysis:
    1. Symbol collection and definition
    2. Type checking and inference
    3. Usage analysis and validation
    4. Final validation and optimization hints
    """
    
    def __init__(self, error_reporter: Optional[ErrorReporter] = None):
        """Initialize the semantic analyzer."""
        self.symbol_table = SymbolTable()
        self.error_reporter = error_reporter or ErrorReporter()
        self.errors: List[RunaSemanticError] = []
        self.warnings: List[RunaSemanticError] = []
        
        # Analysis state
        self.current_pass = AnalysisPass.SYMBOL_COLLECTION
        self.in_function = False
        self.current_function: Optional[FunctionSymbol] = None
        self.return_found = False
        
        # Variable usage tracking
        self.declared_vars: Set[str] = set()
        self.used_vars: Set[str] = set()
        self.assigned_vars: Set[str] = set()
        
        # Loop depth tracking for break/continue validation
        self.loop_depth = 0
    
    def analyze(self, program: Program) -> AnalysisResult:
        """
        Perform complete semantic analysis on a program.
        
        Returns:
            AnalysisResult with symbol table and any errors/warnings.
        """
        try:
            # Pass 1: Symbol collection
            self.current_pass = AnalysisPass.SYMBOL_COLLECTION
            self.visit_program(program)
            
            # Pass 2: Type checking
            self.current_pass = AnalysisPass.TYPE_CHECKING
            self.visit_program(program)
            
            # Pass 3: Usage analysis
            self.current_pass = AnalysisPass.USAGE_ANALYSIS
            self.visit_program(program)
            
            # Pass 4: Final validation
            self.current_pass = AnalysisPass.FINAL_VALIDATION
            self._final_validation()
            
            success = len(self.errors) == 0
            
            return AnalysisResult(
                success=success,
                symbol_table=self.symbol_table,
                errors=self.errors,
                warnings=self.warnings
            )
            
        except Exception as e:
            error = semantic_error(
                f"Unexpected error during semantic analysis: {str(e)}",
                SourcePosition(1, 1)
            )
            self.errors.append(error)
            
            return AnalysisResult(
                success=False,
                symbol_table=self.symbol_table,
                errors=self.errors,
                warnings=self.warnings
            )
    
    def error(self, message: str, position: SourcePosition, note: str = "") -> None:
        """Report a semantic error."""
        error = semantic_error(message, position, note)
        self.errors.append(error)
        self.error_reporter.add_error(error)
    
    def warning(self, message: str, position: SourcePosition, note: str = "") -> None:
        """Report a semantic warning."""
        warning = semantic_error(message, position, note, ErrorSeverity.WARNING)
        self.warnings.append(warning)
        self.error_reporter.add_error(warning)
    
    # ========== VISITOR METHODS ==========
    
    def visit_program(self, node: Program) -> Any:
        """Visit the program root node."""
        for statement in node.statements:
            statement.accept(self)
        return None
    
    def visit_block(self, node: Block) -> Any:
        """Visit a block of statements."""
        self.symbol_table.create_block_scope()
        
        try:
            for statement in node.statements:
                statement.accept(self)
        finally:
            self.symbol_table.exit_scope()
        
        return None
    
    def visit_declaration(self, node: Declaration) -> Any:
        """Visit a variable declaration."""
        if self.current_pass == AnalysisPass.SYMBOL_COLLECTION:
            self._collect_declaration(node)
        elif self.current_pass == AnalysisPass.TYPE_CHECKING:
            self._check_declaration_types(node)
        elif self.current_pass == AnalysisPass.USAGE_ANALYSIS:
            self._analyze_declaration_usage(node)
        
        return None
    
    def visit_assignment(self, node: Assignment) -> Any:
        """Visit an assignment statement."""
        if self.current_pass == AnalysisPass.SYMBOL_COLLECTION:
            # Check if variable is declared
            if not self.symbol_table.is_defined_anywhere(node.identifier):
                self.error(
                    f"Assignment to undeclared variable '{node.identifier}'",
                    node.position,
                    "Variables must be declared with 'let' or 'define' before assignment"
                )
        
        elif self.current_pass == AnalysisPass.TYPE_CHECKING:
            self._check_assignment_types(node)
        
        elif self.current_pass == AnalysisPass.USAGE_ANALYSIS:
            self.assigned_vars.add(node.identifier)
        
        # Visit the value expression
        node.value.accept(self)
        return None
    
    def visit_expression_statement(self, node: ExpressionStatement) -> Any:
        """Visit an expression statement."""
        node.expression.accept(self)
        return None
    
    def visit_return_statement(self, node: ReturnStatement) -> Any:
        """Visit a return statement."""
        if not self.in_function:
            self.error(
                "Return statement outside function",
                node.position,
                "Return statements can only be used inside function definitions"
            )
        
        if node.value:
            node.value.accept(self)
        
        self.return_found = True
        return None
    
    def visit_break_statement(self, node: BreakStatement) -> Any:
        """Visit a break statement."""
        if self.loop_depth == 0:
            self.error(
                "Break statement outside loop",
                node.position,
                "Break statements can only be used inside loops (while, for)"
            )
        return None
    
    def visit_continue_statement(self, node: ContinueStatement) -> Any:
        """Visit a continue statement."""
        if self.loop_depth == 0:
            self.error(
                "Continue statement outside loop",
                node.position,
                "Continue statements can only be used inside loops (while, for)"
            )
        return None
    
    def visit_display_statement(self, node: DisplayStatement) -> Any:
        """Visit a display statement."""
        node.expression.accept(self)
        if node.message:
            node.message.accept(self)
        return None
    
    def visit_input_statement(self, node: InputStatement) -> Any:
        """Visit an input statement."""
        node.prompt.accept(self)
        return None
    
    def visit_import_statement(self, node: ImportStatement) -> Any:
        """Visit an import statement."""
        # Basic module resolution - for now just validate that it's a valid identifier
        if not node.module_name.replace('_', '').replace('.', '').isalnum():
            self.error(
                f"Invalid module name '{node.module_name}'",
                node.position,
                "Module names should contain only letters, numbers, underscores, and dots"
            )
        
        # Create symbol for imported module (simplified)
        if self.current_pass == AnalysisPass.SYMBOL_COLLECTION:
            module_symbol = Symbol(
                name=node.alias or node.module_name.split('.')[-1],
                symbol_type=SymbolType.MODULE,
                data_type=None,
                position=node.position,
                is_mutable=False,
                is_initialized=True
            )
            
            try:
                self.symbol_table.define(module_symbol)
            except Exception as e:
                self.error(str(e), node.position)
        
        return None
    
    def visit_if_statement(self, node: IfStatement) -> Any:
        """Visit an if statement."""
        node.condition.accept(self)
        node.then_block.accept(self)
        
        for condition, block in node.elif_clauses:
            condition.accept(self)
            block.accept(self)
        
        if node.else_block:
            node.else_block.accept(self)
        
        return None
    
    def visit_while_loop(self, node: WhileLoop) -> Any:
        """Visit a while loop."""
        node.condition.accept(self)
        
        # Enter loop context
        self.loop_depth += 1
        try:
            node.body.accept(self)
        finally:
            self.loop_depth -= 1
            
        return None
    
    def visit_for_loop(self, node: ForLoop) -> Any:
        """Visit a for loop."""
        # Create loop variable in new scope
        self.symbol_table.create_block_scope()
        
        try:
            # Define loop variable
            if self.current_pass == AnalysisPass.SYMBOL_COLLECTION:
                loop_var = Symbol(
                    name=node.variable,
                    symbol_type=SymbolType.VARIABLE,
                    data_type=None,  # Type will be inferred from iterable
                    position=node.position,
                    is_mutable=True,
                    is_initialized=True
                )
                self.symbol_table.define(loop_var)
            
            node.iterable.accept(self)
            
            # Enter loop context
            self.loop_depth += 1
            try:
                node.body.accept(self)
            finally:
                self.loop_depth -= 1
            
        finally:
            self.symbol_table.exit_scope()
        
        return None
    
    def visit_try_catch_statement(self, node: TryCatchStatement) -> Any:
        """Visit a try-catch statement."""
        node.try_block.accept(self)
        
        # Create scope for catch block with error variable
        self.symbol_table.create_block_scope()
        
        try:
            if self.current_pass == AnalysisPass.SYMBOL_COLLECTION:
                error_var = Symbol(
                    name=node.catch_variable,
                    symbol_type=SymbolType.VARIABLE,
                    data_type=None,  # Error type
                    position=node.position,
                    is_mutable=False,
                    is_initialized=True
                )
                self.symbol_table.define(error_var)
            
            node.catch_block.accept(self)
            
        finally:
            self.symbol_table.exit_scope()
        
        return None
    
    def visit_parameter(self, node: Parameter) -> Any:
        """Visit a function parameter."""
        return None
    
    def visit_process_definition(self, node: ProcessDefinition) -> Any:
        """Visit a function definition."""
        if self.current_pass == AnalysisPass.SYMBOL_COLLECTION:
            self._collect_function(node)
        elif self.current_pass == AnalysisPass.TYPE_CHECKING:
            self._check_function_types(node)
        
        return None
    
    def visit_literal(self, node: Literal) -> Any:
        """Visit a literal expression."""
        return None
    
    def visit_identifier(self, node: Identifier) -> Any:
        """Visit an identifier expression."""
        if self.current_pass == AnalysisPass.SYMBOL_COLLECTION:
            # Check if identifier is defined
            if not self.symbol_table.is_defined_anywhere(node.name):
                self.error(
                    f"Undefined identifier '{node.name}'",
                    node.position,
                    "Variables must be declared before use"
                )
        
        elif self.current_pass == AnalysisPass.USAGE_ANALYSIS:
            self.used_vars.add(node.name)
        
        return None
    
    def visit_binary_expression(self, node: BinaryExpression) -> Any:
        """Visit a binary expression."""
        node.left.accept(self)
        node.right.accept(self)
        
        if self.current_pass == AnalysisPass.TYPE_CHECKING:
            self._check_binary_operation(node)
        
        return None
    
    def visit_unary_expression(self, node: UnaryExpression) -> Any:
        """Visit a unary expression."""
        node.operand.accept(self)
        return None
    
    def visit_function_call(self, node: FunctionCall) -> Any:
        """Visit a function call."""
        if self.current_pass == AnalysisPass.SYMBOL_COLLECTION:
            # Check if function is defined
            symbol = self.symbol_table.lookup(node.function_name)
            if symbol is None:
                self.error(
                    f"Undefined function '{node.function_name}'",
                    node.position,
                    "Functions must be defined before use"
                )
            elif symbol.symbol_type != SymbolType.FUNCTION:
                self.error(
                    f"'{node.function_name}' is not a function",
                    node.position,
                    f"'{node.function_name}' is a {symbol.symbol_type.name.lower()}"
                )
        
        # Visit arguments
        for name, arg in node.arguments:
            arg.accept(self)
        
        for arg in node.positional_args:
            arg.accept(self)
        
        return None
    
    def visit_member_access(self, node: MemberAccess) -> Any:
        """Visit a member access expression."""
        node.object.accept(self)
        return None
    
    def visit_index_access(self, node: IndexAccess) -> Any:
        """Visit an index access expression."""
        node.object.accept(self)
        node.index.accept(self)
        return None
    
    def visit_list_expression(self, node: ListExpression) -> Any:
        """Visit a list expression."""
        for element in node.elements:
            element.accept(self)
        return None
    
    def visit_key_value_pair(self, node: KeyValuePair) -> Any:
        """Visit a key-value pair."""
        node.key.accept(self)
        node.value.accept(self)
        return None
    
    def visit_dictionary_expression(self, node: DictionaryExpression) -> Any:
        """Visit a dictionary expression."""
        for pair in node.pairs:
            pair.accept(self)
        return None
    
    def visit_model_definition(self, node: ModelDefinition) -> Any:
        """Visit a model definition."""
        # Validate model configuration
        for param in node.parameters:
            param.accept(self)
        
        if node.architecture:
            node.architecture.accept(self)
        
        # Create model symbol
        if self.current_pass == AnalysisPass.SYMBOL_COLLECTION:
            model_symbol = Symbol(
                name=node.name,
                symbol_type=SymbolType.CLASS,  # Models are class-like entities
                data_type=None,
                position=node.position,
                is_mutable=False,
                is_initialized=True
            )
            
            try:
                self.symbol_table.define(model_symbol)
            except Exception as e:
                self.error(str(e), node.position)
        
        return None
    
    def visit_layer_definition(self, node: LayerDefinition) -> Any:
        """Visit a layer definition."""
        # Validate layer parameters
        if node.config:
            node.config.accept(self)
        
        # Basic validation of layer type
        if node.layer_type not in ['dense', 'conv2d', 'lstm', 'attention', 'dropout', 'batch_norm']:
            self.warning(
                f"Unknown layer type '{node.layer_type}'",
                node.position,
                "Consider using standard layer types like 'dense', 'conv2d', 'lstm', etc."
            )
        
        return None
    
    def visit_training_config(self, node: TrainingConfig) -> Any:
        """Visit a training configuration."""
        # Validate training parameters
        for param in node.parameters:
            param.accept(self)
        
        # Basic validation of common parameters
        if hasattr(node, 'learning_rate'):
            if isinstance(node.learning_rate, (int, float)) and node.learning_rate <= 0:
                self.warning(
                    "Learning rate should be positive",
                    node.position,
                    "Typical learning rates are between 0.001 and 0.1"
                )
        
        return None
    
    def visit_knowledge_query(self, node: KnowledgeQuery) -> Any:
        """Visit a knowledge query."""
        for param in node.parameters:
            param.accept(self)
        return None
    
    def visit_type_annotation(self, node: TypeAnnotation) -> Any:
        """Visit a type annotation."""
        return None
    
    def visit_union_type(self, node: UnionType) -> Any:
        """Visit a union type."""
        for type_ann in node.types:
            type_ann.accept(self)
        return None
    
    def visit_generic_type(self, node: GenericType) -> Any:
        """Visit a generic type."""
        for type_param in node.type_params:
            type_param.accept(self)
        return None
    
    def visit_comment(self, node: Comment) -> Any:
        """Visit a comment."""
        return None
    
    def visit_eof_node(self, node: EOFNode) -> Any:
        """Visit EOF node."""
        return None
    
    # ========== HELPER METHODS ==========
    
    def _collect_declaration(self, node: Declaration) -> None:
        """Collect a variable declaration in symbol table."""
        # Check for redefinition in current scope
        if self.symbol_table.is_defined(node.identifier):
            existing = self.symbol_table.lookup_local(node.identifier)
            self.error(
                f"Redefinition of '{node.identifier}'",
                node.position,
                f"Previously defined at {existing.position}"
            )
            return
        
        # Create symbol
        symbol = Symbol(
            name=node.identifier,
            symbol_type=SymbolType.CONSTANT if node.is_constant else SymbolType.VARIABLE,
            data_type=node.type_annotation,
            position=node.position,
            is_mutable=not node.is_constant,
            is_initialized=True
        )
        
        try:
            self.symbol_table.define(symbol)
            self.declared_vars.add(node.identifier)
        except Exception as e:
            self.error(str(e), node.position)
        
        # Visit initializer
        node.initializer.accept(self)
    
    def _check_declaration_types(self, node: Declaration) -> None:
        """Check types in variable declaration."""
        # Visit initializer to check its type
        node.initializer.accept(self)
        
        # Basic type checking if type annotation is present
        if node.type_annotation:
            # For now, just validate that type annotation is valid
            if hasattr(node.type_annotation, 'name'):
                type_name = node.type_annotation.name
                if type_name not in ['string', 'number', 'boolean', 'list', 'dict', 'auto']:
                    self.warning(
                        f"Unknown type '{type_name}'",
                        node.position,
                        "Consider using standard types: string, number, boolean, list, dict, or auto"
                    )
        
        # Check for potential type mismatches (basic validation)
        if hasattr(node.initializer, 'value'):
            init_value = node.initializer.value
            if node.type_annotation and hasattr(node.type_annotation, 'name'):
                expected_type = node.type_annotation.name
                actual_type = self._infer_literal_type(init_value)
                
                if actual_type and expected_type != 'auto' and actual_type != expected_type:
                    self.warning(
                        f"Type mismatch: expected {expected_type}, got {actual_type}",
                        node.position,
                        "Consider using 'auto' for automatic type inference"
                    )
    
    def _analyze_declaration_usage(self, node: Declaration) -> None:
        """Analyze variable declaration usage."""
        node.initializer.accept(self)
    
    def _check_assignment_types(self, node: Assignment) -> None:
        """Check types in assignment."""
        symbol = self.symbol_table.lookup(node.identifier)
        if symbol and not symbol.is_mutable:
            self.error(
                f"Cannot assign to constant '{node.identifier}'",
                node.position,
                "Constants defined with 'define' cannot be modified"
            )
    
    def _collect_function(self, node: ProcessDefinition) -> None:
        """Collect function definition in symbol table."""
        # Check for redefinition
        if self.symbol_table.is_defined(node.name):
            existing = self.symbol_table.lookup_local(node.name)
            self.error(
                f"Redefinition of function '{node.name}'",
                node.position,
                f"Previously defined at {existing.position}"
            )
            return
        
        # Create parameter symbols
        param_symbols = []
        for param in node.parameters:
            param_symbol = Symbol(
                name=param.name,
                symbol_type=SymbolType.PARAMETER,
                data_type=param.type_annotation,
                position=param.position,
                is_mutable=True,
                is_initialized=True
            )
            param_symbols.append(param_symbol)
        
        # Create function symbol
        func_symbol = FunctionSymbol(
            name=node.name,
            symbol_type=SymbolType.FUNCTION,
            data_type=None,
            position=node.position,
            is_mutable=False,
            parameters=param_symbols,
            return_type=node.return_type
        )
        
        try:
            self.symbol_table.define(func_symbol)
        except Exception as e:
            self.error(str(e), node.position)
    
    def _check_function_types(self, node: ProcessDefinition) -> None:
        """Check types in function definition."""
        # Enter function scope
        old_in_function = self.in_function
        old_function = self.current_function
        old_return_found = self.return_found
        
        self.in_function = True
        self.current_function = self.symbol_table.lookup(node.name)
        self.return_found = False
        
        # Create function scope with parameters
        param_symbols = []
        for param in node.parameters:
            param_symbol = Symbol(
                name=param.name,
                symbol_type=SymbolType.PARAMETER,
                data_type=param.type_annotation,
                position=param.position,
                is_mutable=True,
                is_initialized=True
            )
            param_symbols.append(param_symbol)
        
        self.symbol_table.create_function_scope(node.name, param_symbols)
        
        try:
            # Visit function body
            node.body.accept(self)
            
            # Check return statement requirement
            if node.return_type and not self.return_found:
                self.warning(
                    f"Function '{node.name}' declares return type but has no return statement",
                    node.position,
                    "Consider adding a return statement or removing the return type"
                )
        
        finally:
            self.symbol_table.exit_scope()
            self.in_function = old_in_function
            self.current_function = old_function
            self.return_found = old_return_found
    
    def _check_binary_operation(self, node: BinaryExpression) -> None:
        """Check if binary operation is valid."""
        # Basic validation of binary operations
        operator = node.operator
        
        # Check for division by zero literals
        if operator == BinaryOperator.DIVIDE and hasattr(node.right, 'value'):
            if node.right.value == 0:
                self.warning(
                    "Division by zero",
                    node.position,
                    "This will cause a runtime error"
                )
        
        # Check for comparison with different types (basic cases)
        if operator in [BinaryOperator.EQUALS, BinaryOperator.NOT_EQUALS,
                       BinaryOperator.LESS_THAN, BinaryOperator.GREATER_THAN,
                       BinaryOperator.LESS_EQUALS, BinaryOperator.GREATER_EQUALS]:
            
            left_type = self._infer_expression_type(node.left)
            right_type = self._infer_expression_type(node.right)
            
            if (left_type and right_type and 
                left_type != right_type and 
                left_type != 'auto' and right_type != 'auto'):
                self.warning(
                    f"Comparing different types: {left_type} and {right_type}",
                    node.position,
                    "This may not behave as expected"
                )
    
    def _final_validation(self) -> None:
        """Perform final validation checks."""
        # Check for unused variables
        unused_vars = self.declared_vars - self.used_vars
        for var_name in unused_vars:
            symbol = self.symbol_table.lookup(var_name)
            if symbol:
                self.warning(
                    f"Variable '{var_name}' is declared but never used",
                    symbol.position,
                    "Consider removing unused variables"
                )
        
        # Check for variables that are used but never assigned (after initial declaration)
        never_assigned = self.used_vars - self.assigned_vars - self.declared_vars
        for var_name in never_assigned:
            symbol = self.symbol_table.lookup(var_name)
            if symbol and symbol.symbol_type == SymbolType.VARIABLE:
                self.warning(
                    f"Variable '{var_name}' is used but never modified",
                    symbol.position,
                    "Consider using 'define' for constants"
                )
    
    def _infer_literal_type(self, value) -> Optional[str]:
        """Infer the type of a literal value."""
        if isinstance(value, str):
            return 'string'
        elif isinstance(value, (int, float)):
            return 'number'
        elif isinstance(value, bool):
            return 'boolean'
        elif isinstance(value, list):
            return 'list'
        elif isinstance(value, dict):
            return 'dict'
        return None
    
    def _infer_expression_type(self, expr) -> Optional[str]:
        """Infer the type of an expression (basic implementation)."""
        if hasattr(expr, 'value'):
            return self._infer_literal_type(expr.value)
        elif hasattr(expr, 'name'):
            # Look up variable type
            symbol = self.symbol_table.lookup(expr.name)
            if symbol and symbol.data_type and hasattr(symbol.data_type, 'name'):
                return symbol.data_type.name
        return None


# Export main classes
__all__ = [
    'SemanticAnalyzer',
    'AnalysisResult',
    'AnalysisPass',
] 