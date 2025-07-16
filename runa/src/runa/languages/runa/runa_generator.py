"""
Runa Code Generator

Generates natural language Runa source code from Runa AST.
This is the "pretty printer" for the Runa language itself.
"""

from typing import List, Dict, Any, Optional
from ...core.base_components import BaseLanguageGenerator, GenerationError, LanguageInfo, LanguageTier
from ...core.runa_ast import *


# Define Runa language info
RUNA_LANGUAGE_INFO = LanguageInfo(
    name="runa",
    tier=LanguageTier.TIER1,
    file_extensions=[".runa"],
    mime_types=["text/x-runa"],
    description="Natural Language Programming Language",
    version="0.3.0",
    is_compiled=True,
    is_interpreted=True,
    has_static_typing=True,
    has_dynamic_typing=True,
    comment_patterns=[r"Note:\s*(.*)"],
    string_patterns=[r'"([^"\\\\]|\\\\.)*"', r"'([^'\\\\]|\\\\.)*'"],
    number_patterns=[r"\d+\.?\d*"],
    identifier_patterns=[r"[a-zA-Z_][a-zA-Z0-9_\s]*"]
)


class RunaGenerator(BaseLanguageGenerator):
    """Code generator for the Runa natural language programming language."""
    
    def __init__(self):
        super().__init__(RUNA_LANGUAGE_INFO)
        
        # Runa-specific formatting preferences
        self.indent_size = 4
        self.use_tabs = False
        self.prefer_natural_language = True
        self.max_line_length = 100
        
        # Natural language keywords mapping
        self.operator_keywords = {
            "EQUALS": "is equal to",
            "NOT_EQUALS": "is not equal to", 
            "GREATER_THAN": "is greater than",
            "LESS_THAN": "is less than",
            "GREATER_EQUAL": "is greater than or equal to",
            "LESS_EQUAL": "is less than or equal to",
            "AND": "and",
            "OR": "or",
            "NOT": "not",
            "PLUS": "plus",
            "MINUS": "minus",
            "MULTIPLY": "times",
            "DIVIDE": "divided by",
            "MODULO": "modulo",
            "POWER": "to the power of"
        }
    
    def generate(self, runa_ast: ASTNode) -> str:
        """Generate Runa source code from Runa AST."""
        try:
            code_lines = []
            self._generate_node(runa_ast, code_lines, 0)
            
            source_code = self.line_ending.join(code_lines)
            return self.format_code(source_code)
            
        except Exception as e:
            raise GenerationError(f"Failed to generate Runa code: {e}", runa_ast)
    
    def _generate_node(self, node: ASTNode, code_lines: List[str], indent_level: int):
        """Generate code for a single AST node."""
        node_type = type(node).__name__
        
        # Dispatch to specific generation methods
        method_name = f"_generate_{node_type.lower()}"
        if hasattr(self, method_name):
            getattr(self, method_name)(node, code_lines, indent_level)
        else:
            # Fallback for unimplemented node types
            code_lines.append(f"{self.get_indent(indent_level)}Note: Unimplemented node type {node_type}")
    
    # === PROGRAM AND STRUCTURE ===
    
    def _generate_program(self, node: Program, code_lines: List[str], indent_level: int):
        """Generate a complete Runa program."""
        for i, statement in enumerate(node.statements):
            if i > 0:
                code_lines.append("")  # Add blank line between statements
            self._generate_node(statement, code_lines, indent_level)
    
    # === DECLARATIONS ===
    
    def _generate_letstatement(self, node: LetStatement, code_lines: List[str], indent_level: int):
        """Generate a let statement: Let user name be "John"."""
        indent = self.get_indent(indent_level)
        
        # Start with "Let"
        line_parts = ["Let", node.identifier, "be"]
        
        # Add type annotation if present
        if node.type_annotation:
            type_str = self._type_to_string(node.type_annotation)
            line_parts.insert(-1, f"as {type_str}")
        
        # Add value
        value_str = self._expression_to_string(node.value)
        line_parts.append(value_str)
        
        code_lines.append(f"{indent}{' '.join(line_parts)}")
    
    def _generate_definestatement(self, node: DefineStatement, code_lines: List[str], indent_level: int):
        """Generate a define statement: Define constant PI as 3.14159."""
        indent = self.get_indent(indent_level)
        
        line_parts = ["Define"]
        if node.is_constant:
            line_parts.append("constant")
        
        line_parts.extend([node.identifier, "as"])
        
        # Add type annotation if present
        if node.type_annotation:
            type_str = self._type_to_string(node.type_annotation)
            line_parts.insert(-1, f"of type {type_str}")
        
        # Add value
        value_str = self._expression_to_string(node.value)
        line_parts.append(value_str)
        
        code_lines.append(f"{indent}{' '.join(line_parts)}")
    
    def _generate_setstatement(self, node: SetStatement, code_lines: List[str], indent_level: int):
        """Generate a set statement: Set user age to 25."""
        indent = self.get_indent(indent_level)
        target_str = self._expression_to_string(node.target)
        value_str = self._expression_to_string(node.value)
        
        code_lines.append(f"{indent}Set {target_str} to {value_str}")
    
    def _generate_processdefinition(self, node: ProcessDefinition, code_lines: List[str], indent_level: int):
        """Generate a process definition."""
        indent = self.get_indent(indent_level)
        
        # Process header
        header_parts = ["Process called", f'"{node.name}"']
        
        if node.parameters:
            param_strs = []
            for param in node.parameters:
                param_str = param.name
                if param.type_annotation:
                    param_str += f" as {self._type_to_string(param.type_annotation)}"
                param_strs.append(param_str)
            
            if len(param_strs) == 1:
                header_parts.extend(["that takes", param_strs[0]])
            else:
                header_parts.extend(["that takes", ", ".join(param_strs[:-1]), "and", param_strs[-1]])
        
        if node.return_type:
            return_type_str = self._type_to_string(node.return_type)
            header_parts.extend(["and returns", return_type_str])
        
        header_parts.append(":")
        code_lines.append(f"{indent}{' '.join(header_parts)}")
        
        # Process body
        for statement in node.body:
            self._generate_node(statement, code_lines, indent_level + 1)
    
    # === CONTROL FLOW ===
    
    def _generate_ifstatement(self, node: IfStatement, code_lines: List[str], indent_level: int):
        """Generate if statement with natural language."""
        indent = self.get_indent(indent_level)
        
        # Main if clause
        condition_str = self._expression_to_string(node.condition)
        code_lines.append(f"{indent}If {condition_str}:")
        
        for statement in node.then_block:
            self._generate_node(statement, code_lines, indent_level + 1)
        
        # Elif clauses
        for elif_condition, elif_block in node.elif_clauses:
            elif_condition_str = self._expression_to_string(elif_condition)
            code_lines.append(f"{indent}Otherwise if {elif_condition_str}:")
            for statement in elif_block:
                self._generate_node(statement, code_lines, indent_level + 1)
        
        # Else clause
        if node.else_block:
            code_lines.append(f"{indent}Otherwise:")
            for statement in node.else_block:
                self._generate_node(statement, code_lines, indent_level + 1)
    
    def _generate_whileloop(self, node: WhileLoop, code_lines: List[str], indent_level: int):
        """Generate while loop."""
        indent = self.get_indent(indent_level)
        condition_str = self._expression_to_string(node.condition)
        
        code_lines.append(f"{indent}While {condition_str}:")
        for statement in node.block:
            self._generate_node(statement, code_lines, indent_level + 1)
    
    def _generate_foreachloop(self, node: ForEachLoop, code_lines: List[str], indent_level: int):
        """Generate for-each loop."""
        indent = self.get_indent(indent_level)
        iterable_str = self._expression_to_string(node.iterable)
        
        code_lines.append(f"{indent}For each {node.variable} in {iterable_str}:")
        for statement in node.block:
            self._generate_node(statement, code_lines, indent_level + 1)
    
    def _generate_forrangeloop(self, node: ForRangeLoop, code_lines: List[str], indent_level: int):
        """Generate for-range loop."""
        indent = self.get_indent(indent_level)
        start_str = self._expression_to_string(node.start)
        end_str = self._expression_to_string(node.end)
        
        range_part = f"For {node.variable} from {start_str} to {end_str}"
        
        if node.step:
            step_str = self._expression_to_string(node.step)
            range_part += f" by {step_str}"
        
        code_lines.append(f"{indent}{range_part}:")
        for statement in node.block:
            self._generate_node(statement, code_lines, indent_level + 1)
    
    # === PATTERN MATCHING ===
    
    def _generate_matchstatement(self, node: MatchStatement, code_lines: List[str], indent_level: int):
        """Generate match statement."""
        indent = self.get_indent(indent_level)
        value_str = self._expression_to_string(node.value)
        
        code_lines.append(f"{indent}Match {value_str}:")
        
        for case in node.cases:
            self._generate_matchcase(case, code_lines, indent_level + 1)
    
    def _generate_matchcase(self, case: MatchCase, code_lines: List[str], indent_level: int):
        """Generate a match case."""
        indent = self.get_indent(indent_level)
        pattern_str = self._pattern_to_string(case.pattern)
        
        case_line = f"Case {pattern_str}"
        
        if case.guard:
            guard_str = self._expression_to_string(case.guard)
            case_line += f" when {guard_str}"
        
        case_line += ":"
        code_lines.append(f"{indent}{case_line}")
        
        for statement in case.block:
            self._generate_node(statement, code_lines, indent_level + 1)
    
    # === EXPRESSIONS ===
    
    def _generate_displaystatement(self, node: DisplayStatement, code_lines: List[str], indent_level: int):
        """Generate display statement."""
        indent = self.get_indent(indent_level)
        value_str = self._expression_to_string(node.value)
        
        if node.prefix:
            prefix_str = self._expression_to_string(node.prefix)
            code_lines.append(f"{indent}Display {prefix_str} followed by {value_str}")
        else:
            code_lines.append(f"{indent}Display {value_str}")
    
    def _generate_returnstatement(self, node: ReturnStatement, code_lines: List[str], indent_level: int):
        """Generate return statement."""
        indent = self.get_indent(indent_level)
        
        if node.value:
            value_str = self._expression_to_string(node.value)
            code_lines.append(f"{indent}Return {value_str}")
        else:
            code_lines.append(f"{indent}Return")
    
    def _generate_expressionstatement(self, node: ExpressionStatement, code_lines: List[str], indent_level: int):
        """Generate expression statement."""
        indent = self.get_indent(indent_level)
        expr_str = self._expression_to_string(node.expression)
        code_lines.append(f"{indent}{expr_str}")
    
    # === HELPER METHODS ===
    
    def _expression_to_string(self, expr: Expression) -> str:
        """Convert an expression to string."""
        if isinstance(expr, Identifier):
            return expr.name
        elif isinstance(expr, IntegerLiteral):
            return str(expr.value)
        elif isinstance(expr, FloatLiteral):
            return str(expr.value)
        elif isinstance(expr, StringLiteral):
            return f'"{expr.value}"'
        elif isinstance(expr, BooleanLiteral):
            return "true" if expr.value else "false"
        elif isinstance(expr, ListLiteral):
            elements = [self._expression_to_string(elem) for elem in expr.elements]
            return f"[{', '.join(elements)}]"
        elif isinstance(expr, BinaryExpression):
            left = self._expression_to_string(expr.left)
            right = self._expression_to_string(expr.right)
            op = self.operator_keywords.get(expr.operator.name, str(expr.operator.name))
            return f"{left} {op} {right}"
        elif isinstance(expr, FunctionCall):
            args = []
            for param_name, arg_value in expr.arguments:
                arg_str = self._expression_to_string(arg_value)
                if param_name:
                    args.append(f"{param_name} as {arg_str}")
                else:
                    args.append(arg_str)
            
            if len(args) == 0:
                return f"{expr.function_name}"
            elif len(args) == 1:
                return f"{expr.function_name} with {args[0]}"
            else:
                return f"{expr.function_name} with {', '.join(args[:-1])} and {args[-1]}"
        else:
            return f"<{type(expr).__name__}>"
    
    def _pattern_to_string(self, pattern: Pattern) -> str:
        """Convert a pattern to string."""
        if isinstance(pattern, LiteralPattern):
            return self._expression_to_string(pattern.value)
        elif isinstance(pattern, IdentifierPattern):
            return pattern.name
        elif isinstance(pattern, WildcardPattern):
            return "_"
        elif isinstance(pattern, ListPattern):
            elements = [self._pattern_to_string(elem) for elem in pattern.elements]
            pattern_str = f"[{', '.join(elements)}"
            if pattern.rest:
                pattern_str += f", ...{pattern.rest}"
            pattern_str += "]"
            return pattern_str
        else:
            return f"<{type(pattern).__name__}>"
    
    def _type_to_string(self, type_expr: TypeExpression) -> str:
        """Convert a type expression to string."""
        if isinstance(type_expr, BasicType):
            return type_expr.name
        elif isinstance(type_expr, GenericType):
            args = [self._type_to_string(arg) for arg in type_expr.type_args]
            return f"{type_expr.base_type}[{', '.join(args)}]"
        elif isinstance(type_expr, UnionType):
            types = [self._type_to_string(t) for t in type_expr.types]
            return ' OR '.join(types)
        elif isinstance(type_expr, IntersectionType):
            types = [self._type_to_string(t) for t in type_expr.types]
            return ' AND '.join(types)
        elif isinstance(type_expr, OptionalType):
            inner = self._type_to_string(type_expr.inner_type)
            return f"Optional[{inner}]"
        elif isinstance(type_expr, FunctionType):
            params = [self._type_to_string(p) for p in type_expr.param_types]
            return_type = self._type_to_string(type_expr.return_type)
            return f"Function[{', '.join(params)} -> {return_type}]"
        else:
            return f"<{type(type_expr).__name__}>"