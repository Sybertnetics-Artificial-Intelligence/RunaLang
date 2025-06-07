"""
AST Visualization Tools for Runa Programming Language.

This module provides comprehensive tools for visualizing Abstract Syntax Trees
including text output, graphical representation, and debugging utilities.

Features:
- Tree structure visualization
- Graphical AST rendering
- Node statistics and analysis
- Export to various formats
- Interactive AST exploration
"""

from typing import List, Dict, Optional, Any, Set, TextIO
from dataclasses import dataclass
from io import StringIO
import json

from .ast_nodes import *
from .symbol_table import SymbolTable


@dataclass
class NodeInfo:
    """Information about an AST node for visualization."""
    node_type: str
    value: str
    position: str
    children: List['NodeInfo']
    attributes: Dict[str, Any]


class ASTTextVisualizer(ASTVisitor):
    """
    Text-based AST visualizer.
    
    Generates human-readable tree structure representations
    of the AST with proper indentation and node details.
    """
    
    def __init__(self, show_positions: bool = True, show_types: bool = True, max_depth: Optional[int] = None):
        """
        Initialize the text visualizer.
        
        Args:
            show_positions: Whether to show source positions
            show_types: Whether to show node types
            max_depth: Maximum depth to visualize (None for unlimited)
        """
        self.show_positions = show_positions
        self.show_types = show_types
        self.max_depth = max_depth
        self.output = StringIO()
        self.current_depth = 0
        self.indent_size = 2
    
    def visualize(self, node: ASTNode) -> str:
        """
        Visualize an AST node and return the text representation.
        
        Args:
            node: Root AST node to visualize
            
        Returns:
            String representation of the AST
        """
        self.output = StringIO()
        self.current_depth = 0
        node.accept(self)
        return self.output.getvalue()
    
    def _write_line(self, text: str) -> None:
        """Write a line with proper indentation."""
        indent = " " * (self.current_depth * self.indent_size)
        self.output.write(f"{indent}{text}\n")
    
    def _format_node_header(self, node: ASTNode, extra_info: str = "") -> str:
        """Format the header for a node."""
        parts = []
        
        if self.show_types:
            parts.append(f"[{node.__class__.__name__}]")
        
        if extra_info:
            parts.append(extra_info)
        
        if self.show_positions:
            parts.append(f"@{node.position}")
        
        return " ".join(parts)
    
    def _visit_children(self, children: List[ASTNode]) -> None:
        """Visit a list of child nodes."""
        if self.max_depth is not None and self.current_depth >= self.max_depth:
            self._write_line("... (max depth reached)")
            return
        
        self.current_depth += 1
        for child in children:
            if child is not None:
                child.accept(self)
        self.current_depth -= 1
    
    # ========== VISITOR METHODS ==========
    
    def visit_program(self, node: Program) -> Any:
        """Visit program node."""
        self._write_line(self._format_node_header(node, f"({len(node.statements)} statements)"))
        self._visit_children(node.statements)
        return None
    
    def visit_block(self, node: Block) -> Any:
        """Visit block node."""
        self._write_line(self._format_node_header(node, f"({len(node.statements)} statements)"))
        self._visit_children(node.statements)
        return None
    
    def visit_declaration(self, node: Declaration) -> Any:
        """Visit declaration node."""
        kind = "const" if node.is_constant else "var"
        type_info = f" : {node.type_annotation.type_name}" if node.type_annotation else ""
        self._write_line(self._format_node_header(node, f"{kind} {node.identifier}{type_info}"))
        
        if node.type_annotation:
            self.current_depth += 1
            self._write_line("Type:")
            node.type_annotation.accept(self)
            self.current_depth -= 1
        
        self.current_depth += 1
        self._write_line("Initializer:")
        node.initializer.accept(self)
        self.current_depth -= 1
        
        return None
    
    def visit_assignment(self, node: Assignment) -> Any:
        """Visit assignment node."""
        self._write_line(self._format_node_header(node, f"{node.identifier} ="))
        
        self.current_depth += 1
        self._write_line("Value:")
        node.value.accept(self)
        self.current_depth -= 1
        
        return None
    
    def visit_expression_statement(self, node: ExpressionStatement) -> Any:
        """Visit expression statement node."""
        self._write_line(self._format_node_header(node, "expression statement"))
        
        self.current_depth += 1
        node.expression.accept(self)
        self.current_depth -= 1
        
        return None
    
    def visit_display_statement(self, node: DisplayStatement) -> Any:
        """Visit display statement node."""
        self._write_line(self._format_node_header(node, "display"))
        
        self.current_depth += 1
        self._write_line("Expression:")
        node.expression.accept(self)
        
        if node.message:
            self._write_line("Message:")
            node.message.accept(self)
        self.current_depth -= 1
        
        return None
    
    def visit_literal(self, node: Literal) -> Any:
        """Visit literal node."""
        value_repr = repr(node.value) if node.value is not None else "null"
        self._write_line(self._format_node_header(node, f"{node.literal_type}: {value_repr}"))
        return None
    
    def visit_identifier(self, node: Identifier) -> Any:
        """Visit identifier node."""
        self._write_line(self._format_node_header(node, f"'{node.name}'"))
        return None
    
    def visit_binary_expression(self, node: BinaryExpression) -> Any:
        """Visit binary expression node."""
        self._write_line(self._format_node_header(node, f"'{node.operator.value}'"))
        
        self.current_depth += 1
        self._write_line("Left:")
        node.left.accept(self)
        self._write_line("Right:")
        node.right.accept(self)
        self.current_depth -= 1
        
        return None
    
    def visit_unary_expression(self, node: UnaryExpression) -> Any:
        """Visit unary expression node."""
        self._write_line(self._format_node_header(node, f"'{node.operator.value}'"))
        
        self.current_depth += 1
        self._write_line("Operand:")
        node.operand.accept(self)
        self.current_depth -= 1
        
        return None
    
    def visit_function_call(self, node: FunctionCall) -> Any:
        """Visit function call node."""
        arg_count = len(node.arguments) + len(node.positional_args)
        self._write_line(self._format_node_header(node, f"call '{node.function_name}' ({arg_count} args)"))
        
        if node.arguments or node.positional_args:
            self.current_depth += 1
            self._write_line("Arguments:")
            
            self.current_depth += 1
            for name, arg in node.arguments:
                self._write_line(f"{name}:")
                self.current_depth += 1
                arg.accept(self)
                self.current_depth -= 1
            
            for i, arg in enumerate(node.positional_args):
                self._write_line(f"pos[{i}]:")
                self.current_depth += 1
                arg.accept(self)
                self.current_depth -= 1
            
            self.current_depth -= 2
        
        return None
    
    def visit_list_expression(self, node: ListExpression) -> Any:
        """Visit list expression node."""
        self._write_line(self._format_node_header(node, f"list ({len(node.elements)} elements)"))
        
        if node.elements:
            self.current_depth += 1
            self._write_line("Elements:")
            self._visit_children(node.elements)
            self.current_depth -= 1
        
        return None
    
    def visit_type_annotation(self, node: TypeAnnotation) -> Any:
        """Visit type annotation node."""
        type_info = node.type_name
        if node.generic_args:
            arg_types = [arg.type_name for arg in node.generic_args]
            type_info += f"<{', '.join(arg_types)}>"
        
        self._write_line(self._format_node_header(node, f"type: {type_info}"))
        return None
    
    def visit_comment(self, node: Comment) -> Any:
        """Visit comment node."""
        text_preview = node.text[:50] + "..." if len(node.text) > 50 else node.text
        self._write_line(self._format_node_header(node, f"comment: {repr(text_preview)}"))
        return None
    
    # Default implementations for other node types
    def visit_return_statement(self, node: ReturnStatement) -> Any:
        self._write_line(self._format_node_header(node, "return"))
        if node.value:
            self.current_depth += 1
            node.value.accept(self)
            self.current_depth -= 1
        return None
    
    def visit_break_statement(self, node: BreakStatement) -> Any:
        self._write_line(self._format_node_header(node, "break"))
        return None
    
    def visit_continue_statement(self, node: ContinueStatement) -> Any:
        self._write_line(self._format_node_header(node, "continue"))
        return None
    
    def visit_input_statement(self, node: InputStatement) -> Any:
        self._write_line(self._format_node_header(node, "input"))
        self.current_depth += 1
        node.prompt.accept(self)
        self.current_depth -= 1
        return None
    
    def visit_import_statement(self, node: ImportStatement) -> Any:
        items = ", ".join(node.import_items) if node.import_items else "all"
        self._write_line(self._format_node_header(node, f"import {items} from '{node.module_name}'"))
        return None
    
    def visit_if_statement(self, node: IfStatement) -> Any:
        self._write_line(self._format_node_header(node, "if"))
        self.current_depth += 1
        self._write_line("Condition:")
        node.condition.accept(self)
        self._write_line("Then:")
        node.then_block.accept(self)
        if node.else_block:
            self._write_line("Else:")
            node.else_block.accept(self)
        self.current_depth -= 1
        return None
    
    def visit_while_loop(self, node: WhileLoop) -> Any:
        self._write_line(self._format_node_header(node, "while"))
        self.current_depth += 1
        self._write_line("Condition:")
        node.condition.accept(self)
        self._write_line("Body:")
        node.body.accept(self)
        self.current_depth -= 1
        return None
    
    def visit_for_loop(self, node: ForLoop) -> Any:
        self._write_line(self._format_node_header(node, f"for {node.variable} in"))
        self.current_depth += 1
        self._write_line("Iterable:")
        node.iterable.accept(self)
        self._write_line("Body:")
        node.body.accept(self)
        self.current_depth -= 1
        return None
    
    def visit_try_catch_statement(self, node: TryCatchStatement) -> Any:
        self._write_line(self._format_node_header(node, f"try-catch ({node.catch_variable})"))
        self.current_depth += 1
        self._write_line("Try:")
        node.try_block.accept(self)
        self._write_line("Catch:")
        node.catch_block.accept(self)
        self.current_depth -= 1
        return None
    
    def visit_parameter(self, node: Parameter) -> Any:
        type_info = f" : {node.type_annotation.type_name}" if node.type_annotation else ""
        self._write_line(self._format_node_header(node, f"param {node.name}{type_info}"))
        return None
    
    def visit_process_definition(self, node: ProcessDefinition) -> Any:
        return_info = f" -> {node.return_type.type_name}" if node.return_type else ""
        self._write_line(self._format_node_header(node, f"function '{node.name}'({len(node.parameters)} params){return_info}"))
        
        if node.parameters:
            self.current_depth += 1
            self._write_line("Parameters:")
            self._visit_children(node.parameters)
            self.current_depth -= 1
        
        self.current_depth += 1
        self._write_line("Body:")
        node.body.accept(self)
        self.current_depth -= 1
        return None
    
    def visit_member_access(self, node: MemberAccess) -> Any:
        self._write_line(self._format_node_header(node, f"member access .{node.member}"))
        self.current_depth += 1
        self._write_line("Object:")
        node.object.accept(self)
        self.current_depth -= 1
        return None
    
    def visit_index_access(self, node: IndexAccess) -> Any:
        self._write_line(self._format_node_header(node, "index access []"))
        self.current_depth += 1
        self._write_line("Object:")
        node.object.accept(self)
        self._write_line("Index:")
        node.index.accept(self)
        self.current_depth -= 1
        return None
    
    def visit_key_value_pair(self, node: KeyValuePair) -> Any:
        self._write_line(self._format_node_header(node, "key-value pair"))
        self.current_depth += 1
        self._write_line("Key:")
        node.key.accept(self)
        self._write_line("Value:")
        node.value.accept(self)
        self.current_depth -= 1
        return None
    
    def visit_dictionary_expression(self, node: DictionaryExpression) -> Any:
        self._write_line(self._format_node_header(node, f"dictionary ({len(node.pairs)} pairs)"))
        if node.pairs:
            self.current_depth += 1
            self._write_line("Pairs:")
            self._visit_children(node.pairs)
            self.current_depth -= 1
        return None
    
    def visit_model_definition(self, node: ModelDefinition) -> Any:
        self._write_line(self._format_node_header(node, f"model '{node.name}' ({len(node.layers)} layers)"))
        return None
    
    def visit_layer_definition(self, node: LayerDefinition) -> Any:
        self._write_line(self._format_node_header(node, f"layer '{node.layer_type}'"))
        return None
    
    def visit_training_config(self, node: TrainingConfig) -> Any:
        self._write_line(self._format_node_header(node, f"training config for '{node.model_name}'"))
        return None
    
    def visit_knowledge_query(self, node: KnowledgeQuery) -> Any:
        self._write_line(self._format_node_header(node, f"knowledge query '{node.query_type}'"))
        return None
    
    def visit_union_type(self, node: UnionType) -> Any:
        types = " | ".join(t.type_name for t in node.types)
        self._write_line(self._format_node_header(node, f"union type: {types}"))
        return None
    
    def visit_generic_type(self, node: GenericType) -> Any:
        params = ", ".join(p.type_name for p in node.type_params)
        self._write_line(self._format_node_header(node, f"generic type: {node.base_type}<{params}>"))
        return None
    
    def visit_eof_node(self, node: EOFNode) -> Any:
        self._write_line(self._format_node_header(node, "EOF"))
        return None


class ASTJSONExporter(ASTVisitor):
    """
    Export AST to JSON format for external tools and analysis.
    """
    
    def __init__(self, include_positions: bool = True):
        """Initialize the JSON exporter."""
        self.include_positions = include_positions
    
    def export(self, node: ASTNode) -> str:
        """Export AST node to JSON string."""
        data = node.accept(self)
        return json.dumps(data, indent=2)
    
    def _create_node_dict(self, node: ASTNode, extra_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a dictionary representation of a node."""
        result = {
            "node_type": node.__class__.__name__,
            "type_enum": node.node_type.name if hasattr(node, 'node_type') else None
        }
        
        if self.include_positions:
            result["position"] = {
                "line": node.position.line,
                "column": node.position.column,
                "filename": node.position.filename
            }
        
        if extra_data:
            result.update(extra_data)
        
        return result
    
    def visit_program(self, node: Program) -> Dict[str, Any]:
        return self._create_node_dict(node, {
            "statements": [stmt.accept(self) for stmt in node.statements]
        })
    
    def visit_literal(self, node: Literal) -> Dict[str, Any]:
        return self._create_node_dict(node, {
            "value": node.value,
            "literal_type": node.literal_type
        })
    
    def visit_identifier(self, node: Identifier) -> Dict[str, Any]:
        return self._create_node_dict(node, {
            "name": node.name
        })
    
    def visit_binary_expression(self, node: BinaryExpression) -> Dict[str, Any]:
        return self._create_node_dict(node, {
            "operator": node.operator.value,
            "left": node.left.accept(self),
            "right": node.right.accept(self)
        })
    
    # Add other visitor methods as needed...
    
    def visit_declaration(self, node: Declaration) -> Dict[str, Any]:
        return self._create_node_dict(node, {
            "identifier": node.identifier,
            "is_constant": node.is_constant,
            "type_annotation": node.type_annotation.accept(self) if node.type_annotation else None,
            "initializer": node.initializer.accept(self)
        })
    
    # Default implementation for all other nodes
    def visit_block(self, node: Block) -> Dict[str, Any]:
        return self._create_node_dict(node, {"statements": [s.accept(self) for s in node.statements]})
    
    def visit_assignment(self, node: Assignment) -> Dict[str, Any]:
        return self._create_node_dict(node, {"identifier": node.identifier, "value": node.value.accept(self)})
    
    def visit_expression_statement(self, node: ExpressionStatement) -> Dict[str, Any]:
        return self._create_node_dict(node, {"expression": node.expression.accept(self)})
    
    def visit_return_statement(self, node: ReturnStatement) -> Dict[str, Any]:
        return self._create_node_dict(node, {"value": node.value.accept(self) if node.value else None})
    
    def visit_break_statement(self, node: BreakStatement) -> Dict[str, Any]:
        return self._create_node_dict(node)
    
    def visit_continue_statement(self, node: ContinueStatement) -> Dict[str, Any]:
        return self._create_node_dict(node)
    
    def visit_display_statement(self, node: DisplayStatement) -> Dict[str, Any]:
        return self._create_node_dict(node, {
            "expression": node.expression.accept(self),
            "message": node.message.accept(self) if node.message else None
        })
    
    def visit_input_statement(self, node: InputStatement) -> Dict[str, Any]:
        return self._create_node_dict(node, {"prompt": node.prompt.accept(self)})
    
    def visit_import_statement(self, node: ImportStatement) -> Dict[str, Any]:
        return self._create_node_dict(node, {
            "module_name": node.module_name,
            "import_items": node.import_items,
            "alias": node.alias
        })
    
    def visit_if_statement(self, node: IfStatement) -> Dict[str, Any]:
        return self._create_node_dict(node, {
            "condition": node.condition.accept(self),
            "then_block": node.then_block.accept(self),
            "elif_clauses": [(cond.accept(self), block.accept(self)) for cond, block in node.elif_clauses],
            "else_block": node.else_block.accept(self) if node.else_block else None
        })
    
    def visit_while_loop(self, node: WhileLoop) -> Dict[str, Any]:
        return self._create_node_dict(node, {
            "condition": node.condition.accept(self),
            "body": node.body.accept(self)
        })
    
    def visit_for_loop(self, node: ForLoop) -> Dict[str, Any]:
        return self._create_node_dict(node, {
            "variable": node.variable,
            "iterable": node.iterable.accept(self),
            "body": node.body.accept(self)
        })
    
    def visit_try_catch_statement(self, node: TryCatchStatement) -> Dict[str, Any]:
        return self._create_node_dict(node, {
            "try_block": node.try_block.accept(self),
            "catch_variable": node.catch_variable,
            "catch_block": node.catch_block.accept(self)
        })
    
    def visit_parameter(self, node: Parameter) -> Dict[str, Any]:
        return self._create_node_dict(node, {
            "name": node.name,
            "type_annotation": node.type_annotation.accept(self) if node.type_annotation else None,
            "default_value": node.default_value.accept(self) if node.default_value else None
        })
    
    def visit_process_definition(self, node: ProcessDefinition) -> Dict[str, Any]:
        return self._create_node_dict(node, {
            "name": node.name,
            "parameters": [p.accept(self) for p in node.parameters],
            "return_type": node.return_type.accept(self) if node.return_type else None,
            "body": node.body.accept(self)
        })
    
    def visit_unary_expression(self, node: UnaryExpression) -> Dict[str, Any]:
        return self._create_node_dict(node, {
            "operator": node.operator.value,
            "operand": node.operand.accept(self)
        })
    
    def visit_function_call(self, node: FunctionCall) -> Dict[str, Any]:
        return self._create_node_dict(node, {
            "function_name": node.function_name,
            "arguments": [(name, arg.accept(self)) for name, arg in node.arguments],
            "positional_args": [arg.accept(self) for arg in node.positional_args]
        })
    
    def visit_member_access(self, node: MemberAccess) -> Dict[str, Any]:
        return self._create_node_dict(node, {
            "object": node.object.accept(self),
            "member": node.member
        })
    
    def visit_index_access(self, node: IndexAccess) -> Dict[str, Any]:
        return self._create_node_dict(node, {
            "object": node.object.accept(self),
            "index": node.index.accept(self)
        })
    
    def visit_list_expression(self, node: ListExpression) -> Dict[str, Any]:
        return self._create_node_dict(node, {
            "elements": [elem.accept(self) for elem in node.elements]
        })
    
    def visit_key_value_pair(self, node: KeyValuePair) -> Dict[str, Any]:
        return self._create_node_dict(node, {
            "key": node.key.accept(self),
            "value": node.value.accept(self)
        })
    
    def visit_dictionary_expression(self, node: DictionaryExpression) -> Dict[str, Any]:
        return self._create_node_dict(node, {
            "pairs": [pair.accept(self) for pair in node.pairs]
        })
    
    def visit_model_definition(self, node: ModelDefinition) -> Dict[str, Any]:
        return self._create_node_dict(node, {
            "name": node.name,
            "layers": [layer.accept(self) for layer in node.layers],
            "configuration": node.configuration
        })
    
    def visit_layer_definition(self, node: LayerDefinition) -> Dict[str, Any]:
        return self._create_node_dict(node, {
            "layer_type": node.layer_type,
            "properties": {k: v.accept(self) for k, v in node.properties.items()}
        })
    
    def visit_training_config(self, node: TrainingConfig) -> Dict[str, Any]:
        return self._create_node_dict(node, {
            "model_name": node.model_name,
            "config_options": {k: v.accept(self) for k, v in node.config_options.items()}
        })
    
    def visit_knowledge_query(self, node: KnowledgeQuery) -> Dict[str, Any]:
        return self._create_node_dict(node, {
            "query_type": node.query_type,
            "query_string": node.query_string,
            "parameters": [param.accept(self) for param in node.parameters]
        })
    
    def visit_type_annotation(self, node: TypeAnnotation) -> Dict[str, Any]:
        return self._create_node_dict(node, {
            "type_name": node.type_name,
            "generic_args": [arg.accept(self) for arg in node.generic_args] if node.generic_args else None
        })
    
    def visit_union_type(self, node: UnionType) -> Dict[str, Any]:
        return self._create_node_dict(node, {
            "types": [t.accept(self) for t in node.types]
        })
    
    def visit_generic_type(self, node: GenericType) -> Dict[str, Any]:
        return self._create_node_dict(node, {
            "base_type": node.base_type,
            "type_params": [param.accept(self) for param in node.type_params]
        })
    
    def visit_comment(self, node: Comment) -> Dict[str, Any]:
        return self._create_node_dict(node, {"text": node.text})
    
    def visit_eof_node(self, node: EOFNode) -> Dict[str, Any]:
        return self._create_node_dict(node)


class ASTStatistics:
    """
    Collect and analyze statistics about an AST.
    """
    
    def __init__(self):
        """Initialize statistics collector."""
        self.node_counts: Dict[str, int] = {}
        self.max_depth = 0
        self.total_nodes = 0
        self.statement_count = 0
        self.expression_count = 0
        self.function_count = 0
        self.variable_count = 0
    
    def analyze(self, node: ASTNode) -> Dict[str, Any]:
        """
        Analyze an AST and return statistics.
        
        Args:
            node: Root AST node to analyze
            
        Returns:
            Dictionary containing various statistics
        """
        self.node_counts.clear()
        self.max_depth = 0
        self.total_nodes = 0
        self.statement_count = 0
        self.expression_count = 0
        self.function_count = 0
        self.variable_count = 0
        
        self._analyze_node(node, 0)
        
        return {
            "total_nodes": self.total_nodes,
            "max_depth": self.max_depth,
            "node_type_counts": dict(sorted(self.node_counts.items())),
            "statement_count": self.statement_count,
            "expression_count": self.expression_count,
            "function_count": self.function_count,
            "variable_count": self.variable_count,
            "complexity_score": self._calculate_complexity()
        }
    
    def _analyze_node(self, node: ASTNode, depth: int) -> None:
        """Recursively analyze a node."""
        if node is None:
            return
        
        # Update statistics
        node_type = node.__class__.__name__
        self.node_counts[node_type] = self.node_counts.get(node_type, 0) + 1
        self.total_nodes += 1
        self.max_depth = max(self.max_depth, depth)
        
        # Count specific types
        if isinstance(node, Statement):
            self.statement_count += 1
        if isinstance(node, Expression):
            self.expression_count += 1
        if isinstance(node, ProcessDefinition):
            self.function_count += 1
        if isinstance(node, Declaration):
            self.variable_count += 1
        
        # Recursively analyze children
        if isinstance(node, Program):
            for stmt in node.statements:
                self._analyze_node(stmt, depth + 1)
        elif isinstance(node, Block):
            for stmt in node.statements:
                self._analyze_node(stmt, depth + 1)
        elif isinstance(node, Declaration):
            self._analyze_node(node.initializer, depth + 1)
            if node.type_annotation:
                self._analyze_node(node.type_annotation, depth + 1)
        elif isinstance(node, Assignment):
            self._analyze_node(node.value, depth + 1)
        elif isinstance(node, BinaryExpression):
            self._analyze_node(node.left, depth + 1)
            self._analyze_node(node.right, depth + 1)
        elif isinstance(node, UnaryExpression):
            self._analyze_node(node.operand, depth + 1)
        elif isinstance(node, FunctionCall):
            for _, arg in node.arguments:
                self._analyze_node(arg, depth + 1)
            for arg in node.positional_args:
                self._analyze_node(arg, depth + 1)
        elif isinstance(node, ListExpression):
            for elem in node.elements:
                self._analyze_node(elem, depth + 1)
        # Add more node types as needed
    
    def _calculate_complexity(self) -> float:
        """Calculate a complexity score for the AST."""
        # Simple complexity metric based on various factors
        complexity = 0.0
        
        # Base complexity from total nodes
        complexity += self.total_nodes * 0.1
        
        # Additional complexity from control structures
        complexity += self.node_counts.get("IfStatement", 0) * 2
        complexity += self.node_counts.get("WhileLoop", 0) * 3
        complexity += self.node_counts.get("ForLoop", 0) * 3
        complexity += self.node_counts.get("TryCatchStatement", 0) * 2
        
        # Function complexity
        complexity += self.function_count * 5
        
        # Depth penalty
        complexity += (self.max_depth - 1) * 1.5
        
        return complexity


# Export main classes
__all__ = [
    'ASTTextVisualizer',
    'ASTJSONExporter', 
    'ASTStatistics',
    'NodeInfo',
] 