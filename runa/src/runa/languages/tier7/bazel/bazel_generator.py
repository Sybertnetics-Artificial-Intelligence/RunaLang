#!/usr/bin/env python3
"""
Bazel Code Generator

Clean code generation for Bazel build files including:
- BUILD files with proper formatting
- WORKSPACE files with dependency organization
- .bzl files with custom rule definitions
- Starlark syntax with consistent style
- Label formatting and validation
- Attribute organization and comments
"""

from typing import List, Dict, Any, Optional, Union, TextIO
from dataclasses import dataclass
from io import StringIO

from .bazel_ast import *


@dataclass
class BazelCodeStyle:
    """Configuration for Bazel code formatting."""
    indent_size: int = 4
    indent_char: str = " "
    max_line_length: int = 120
    sort_attributes: bool = True
    use_trailing_commas: bool = True
    separate_targets: bool = True
    attribute_alignment: bool = True
    comment_style: str = "# "
    string_quote: str = '"'
    
    # BUILD file specific
    sort_load_statements: bool = True
    group_similar_targets: bool = True
    
    # Label formatting
    use_short_labels: bool = True
    explicit_package_labels: bool = False


class BazelFormatter:
    """Handles indentation and formatting for Bazel code."""
    
    def __init__(self, style: BazelCodeStyle):
        self.style = style
        self.current_indent = 0
        self.output = StringIO()
        
    def indent(self) -> None:
        """Increase indentation level."""
        self.current_indent += 1
    
    def dedent(self) -> None:
        """Decrease indentation level."""
        self.current_indent = max(0, self.current_indent - 1)
    
    def write_line(self, line: str = "") -> None:
        """Write a line with proper indentation."""
        if line.strip():
            indent_str = self.style.indent_char * (self.current_indent * self.style.indent_size)
            self.output.write(f"{indent_str}{line}\n")
        else:
            self.output.write("\n")
    
    def write_lines(self, lines: List[str]) -> None:
        """Write multiple lines."""
        for line in lines:
            self.write_line(line)
    
    def write_comment(self, comment: str) -> None:
        """Write a comment line."""
        if comment.strip():
            clean_comment = comment.strip().lstrip('#').strip()
            self.write_line(f"{self.style.comment_style}{clean_comment}")
    
    def write_block_comment(self, comment: str) -> None:
        """Write a multi-line comment block."""
        lines = comment.strip().split('\n')
        for line in lines:
            self.write_comment(line)
    
    def get_output(self) -> str:
        """Get the formatted output."""
        return self.output.getvalue()
    
    def reset(self) -> None:
        """Reset the formatter state."""
        self.current_indent = 0
        self.output = StringIO()


class BazelCodeGenerator:
    """Generates clean Bazel code from AST."""
    
    def __init__(self, style: Optional[BazelCodeStyle] = None):
        self.style = style or BazelCodeStyle()
        self.formatter = BazelFormatter(self.style)
        
    def generate(self, node: BazelNode) -> str:
        """Generate Bazel code from AST node."""
        self.formatter.reset()
        
        if isinstance(node, BuildFile):
            self._generate_build_file(node)
        elif isinstance(node, WorkspaceFile):
            self._generate_workspace_file(node)
        elif isinstance(node, BzlFile):
            self._generate_bzl_file(node)
        elif isinstance(node, TargetDefinition):
            self._generate_target_definition(node)
        elif isinstance(node, RuleDefinition):
            self._generate_rule_definition(node)
        elif isinstance(node, LoadStatement):
            self._generate_load_statement(node)
        elif isinstance(node, FunctionDef):
            self._generate_function_def(node)
        elif isinstance(node, Assignment):
            self._generate_assignment(node)
        elif isinstance(node, IfStatement):
            self._generate_if_statement(node)
        elif isinstance(node, ForLoop):
            self._generate_for_loop(node)
        else:
            self._generate_expression(node)
        
        return self.formatter.get_output()
    
    def _generate_build_file(self, node: BuildFile) -> None:
        """Generate BUILD file content."""
        # File header comment
        self.formatter.write_comment(f"BUILD file for package: {node.package_name}")
        self.formatter.write_line()
        
        # Add package() declaration if needed
        if node.visibility or node.licenses:
            self._generate_package_declaration(node)
            self.formatter.write_line()
        
        # Separate load statements from other statements
        load_statements = [stmt for stmt in node.statements if isinstance(stmt, LoadStatement)]
        other_statements = [stmt for stmt in node.statements if not isinstance(stmt, LoadStatement)]
        
        # Generate load statements first
        if load_statements:
            if self.style.sort_load_statements:
                load_statements.sort(key=lambda x: x.file_path)
            
            for stmt in load_statements:
                self._generate_statement(stmt)
            
            if other_statements:
                self.formatter.write_line()
        
        # Generate other statements
        if self.style.group_similar_targets:
            grouped_statements = self._group_statements(other_statements)
            for group in grouped_statements:
                for stmt in group:
                    self._generate_statement(stmt)
                    if self.style.separate_targets and isinstance(stmt, TargetDefinition):
                        self.formatter.write_line()
                if group != grouped_statements[-1]:
                    self.formatter.write_line()
        else:
            for stmt in other_statements:
                self._generate_statement(stmt)
                if self.style.separate_targets and isinstance(stmt, TargetDefinition):
                    self.formatter.write_line()
    
    def _generate_workspace_file(self, node: WorkspaceFile) -> None:
        """Generate WORKSPACE file content."""
        # File header comment
        self.formatter.write_comment(f"WORKSPACE file for: {node.workspace_name}")
        self.formatter.write_line()
        
        # Workspace declaration
        self.formatter.write_line(f'workspace(name = "{node.workspace_name}")')
        
        if node.statements:
            self.formatter.write_line()
            
            # Group workspace rules by type
            workspace_rules = []
            other_statements = []
            
            for stmt in node.statements:
                if isinstance(stmt, WorkspaceRule):
                    workspace_rules.append(stmt)
                else:
                    other_statements.append(stmt)
            
            # Generate workspace rules first
            if workspace_rules:
                rule_groups = self._group_workspace_rules(workspace_rules)
                for rule_type, rules in rule_groups.items():
                    if rules:
                        self.formatter.write_comment(f"{rule_type.replace('_', ' ').title()} Dependencies")
                        for rule in rules:
                            self._generate_statement(rule)
                        self.formatter.write_line()
            
            # Generate other statements
            for stmt in other_statements:
                self._generate_statement(stmt)
    
    def _generate_bzl_file(self, node: BzlFile) -> None:
        """Generate .bzl file content."""
        # File header comment
        self.formatter.write_comment(f"Bazel extension file: {node.file_name}")
        if node.load_statements:
            self.formatter.write_comment("Custom rules and macros")
        self.formatter.write_line()
        
        # Generate statements
        for stmt in node.statements:
            self._generate_statement(stmt)
            if isinstance(stmt, (FunctionDef, RuleDefinition)):
                self.formatter.write_line()
    
    def _generate_package_declaration(self, node: BuildFile) -> None:
        """Generate package() declaration."""
        attributes = []
        
        if node.visibility:
            visibility_list = self._format_string_list(node.visibility)
            attributes.append(f"default_visibility = {visibility_list}")
        
        if node.licenses:
            licenses_list = self._format_string_list(node.licenses)
            attributes.append(f"licenses = {licenses_list}")
        
        if attributes:
            if len(attributes) == 1 and len(attributes[0]) < 60:
                self.formatter.write_line(f"package({attributes[0]})")
            else:
                self.formatter.write_line("package(")
                self.formatter.indent()
                for attr in attributes:
                    self.formatter.write_line(f"{attr},")
                self.formatter.dedent()
                self.formatter.write_line(")")
    
    def _generate_statement(self, stmt: BazelStatement) -> None:
        """Generate code for a statement."""
        if isinstance(stmt, LoadStatement):
            self._generate_load_statement(stmt)
        elif isinstance(stmt, TargetDefinition):
            self._generate_target_definition(stmt)
        elif isinstance(stmt, RuleDefinition):
            self._generate_rule_definition(stmt)
        elif isinstance(stmt, FunctionDef):
            self._generate_function_def(stmt)
        elif isinstance(stmt, Assignment):
            self._generate_assignment(stmt)
        elif isinstance(stmt, IfStatement):
            self._generate_if_statement(stmt)
        elif isinstance(stmt, ForLoop):
            self._generate_for_loop(stmt)
        elif isinstance(stmt, WorkspaceRule):
            self._generate_workspace_rule(stmt)
    
    def _generate_load_statement(self, node: LoadStatement) -> None:
        """Generate load statement."""
        file_path = self._quote_string(node.file_path)
        
        if not node.symbols:
            self.formatter.write_line(f"load({file_path})")
            return
        
        if len(node.symbols) == 1 and len(file_path) + len(node.symbols[0]) < 80:
            # Single line format
            symbol = self._quote_string(node.symbols[0])
            self.formatter.write_line(f"load({file_path}, {symbol})")
        else:
            # Multi-line format
            self.formatter.write_line(f"load(")
            self.formatter.indent()
            self.formatter.write_line(f"{file_path},")
            
            for i, symbol in enumerate(node.symbols):
                quoted_symbol = self._quote_string(symbol)
                comma = "," if i < len(node.symbols) - 1 or self.style.use_trailing_commas else ""
                self.formatter.write_line(f"{quoted_symbol}{comma}")
            
            self.formatter.dedent()
            self.formatter.write_line(")")
    
    def _generate_target_definition(self, node: TargetDefinition) -> None:
        """Generate target definition."""
        # Prepare attributes
        all_attributes = dict(node.attributes)
        all_attributes["name"] = Literal(node.target_name, "string")
        
        if node.visibility:
            visibility_list = ListExpr([Literal(v, "string") for v in node.visibility])
            all_attributes["visibility"] = visibility_list
        
        if node.tags:
            tags_list = ListExpr([Literal(t, "string") for t in node.tags])
            all_attributes["tags"] = tags_list
        
        # Sort attributes if enabled
        if self.style.sort_attributes:
            # Put 'name' first, then sort others
            sorted_attrs = {"name": all_attributes["name"]}
            for key in sorted(k for k in all_attributes.keys() if k != "name"):
                sorted_attrs[key] = all_attributes[key]
            all_attributes = sorted_attrs
        
        # Generate target call
        if len(all_attributes) == 1 and len(node.target_name) < 40:
            # Single line format
            name_value = self._quote_string(node.target_name)
            self.formatter.write_line(f'{node.rule_name}(name = {name_value})')
        else:
            # Multi-line format
            self.formatter.write_line(f"{node.rule_name}(")
            self.formatter.indent()
            
            max_key_length = max(len(key) for key in all_attributes.keys()) if self.style.attribute_alignment else 0
            
            for i, (key, value) in enumerate(all_attributes.items()):
                formatted_value = self._generate_expression_string(value)
                
                if self.style.attribute_alignment and max_key_length > 0:
                    padding = " " * (max_key_length - len(key))
                    formatted_line = f"{key}{padding} = {formatted_value}"
                else:
                    formatted_line = f"{key} = {formatted_value}"
                
                comma = "," if i < len(all_attributes) - 1 or self.style.use_trailing_commas else ""
                self.formatter.write_line(f"{formatted_line}{comma}")
            
            self.formatter.dedent()
            self.formatter.write_line(")")
    
    def _generate_rule_definition(self, node: RuleDefinition) -> None:
        """Generate rule definition."""
        self.formatter.write_line(f"{node.name} = rule(")
        self.formatter.indent()
        
        # Implementation
        impl_value = self._quote_string(node.implementation)
        self.formatter.write_line(f"implementation = {impl_value},")
        
        # Attributes
        if node.attributes:
            self.formatter.write_line("attrs = {")
            self.formatter.indent()
            
            for attr_name, attr_def in node.attributes.items():
                attr_config = self._generate_attribute_definition(attr_def)
                self.formatter.write_line(f'"{attr_name}": {attr_config},')
            
            self.formatter.dedent()
            self.formatter.write_line("},")
        
        # Other properties
        if node.executable:
            self.formatter.write_line("executable = True,")
        if node.test:
            self.formatter.write_line("test = True,")
        
        self.formatter.dedent()
        self.formatter.write_line(")")
    
    def _generate_function_def(self, node: FunctionDef) -> None:
        """Generate function definition."""
        # Function signature
        params = []
        for param in node.parameters:
            if param in node.defaults:
                default_value = self._generate_expression_string(node.defaults[param])
                params.append(f"{param} = {default_value}")
            else:
                params.append(param)
        
        params_str = ", ".join(params)
        self.formatter.write_line(f"def {node.name}({params_str}):")
        
        # Function body
        self.formatter.indent()
        if node.body:
            for stmt in node.body:
                self._generate_statement(stmt)
        else:
            self.formatter.write_line("pass")
        self.formatter.dedent()
    
    def _generate_assignment(self, node: Assignment) -> None:
        """Generate assignment statement."""
        value_str = self._generate_expression_string(node.value)
        self.formatter.write_line(f"{node.target} {node.operator} {value_str}")
    
    def _generate_if_statement(self, node: IfStatement) -> None:
        """Generate if statement."""
        condition_str = self._generate_expression_string(node.condition)
        self.formatter.write_line(f"if {condition_str}:")
        
        # Then block
        self.formatter.indent()
        if node.then_body:
            for stmt in node.then_body:
                self._generate_statement(stmt)
        else:
            self.formatter.write_line("pass")
        self.formatter.dedent()
        
        # Else block
        if node.else_body:
            self.formatter.write_line("else:")
            self.formatter.indent()
            for stmt in node.else_body:
                self._generate_statement(stmt)
            self.formatter.dedent()
    
    def _generate_for_loop(self, node: ForLoop) -> None:
        """Generate for loop."""
        iterable_str = self._generate_expression_string(node.iterable)
        self.formatter.write_line(f"for {node.variable} in {iterable_str}:")
        
        self.formatter.indent()
        if node.body:
            for stmt in node.body:
                self._generate_statement(stmt)
        else:
            self.formatter.write_line("pass")
        self.formatter.dedent()
    
    def _generate_workspace_rule(self, node: WorkspaceRule) -> None:
        """Generate workspace rule."""
        attributes = dict(node.attributes)
        
        if len(attributes) <= 1:
            # Single line format
            if attributes:
                attr_strs = []
                for key, value in attributes.items():
                    value_str = self._generate_expression_string(value)
                    attr_strs.append(f"{key} = {value_str}")
                attrs_str = ", ".join(attr_strs)
                self.formatter.write_line(f"{node.rule_name}({attrs_str})")
            else:
                self.formatter.write_line(f"{node.rule_name}()")
        else:
            # Multi-line format
            self.formatter.write_line(f"{node.rule_name}(")
            self.formatter.indent()
            
            for i, (key, value) in enumerate(attributes.items()):
                value_str = self._generate_expression_string(value)
                comma = "," if i < len(attributes) - 1 or self.style.use_trailing_commas else ""
                self.formatter.write_line(f"{key} = {value_str}{comma}")
            
            self.formatter.dedent()
            self.formatter.write_line(")")
    
    def _generate_expression(self, node: BazelExpression) -> None:
        """Generate expression code."""
        expr_str = self._generate_expression_string(node)
        self.formatter.write_line(expr_str)
    
    def _generate_expression_string(self, node: BazelExpression) -> str:
        """Generate expression as string."""
        if isinstance(node, Literal):
            return self._format_literal(node)
        elif isinstance(node, Identifier):
            return node.name
        elif isinstance(node, Label):
            return self._format_label(node)
        elif isinstance(node, ListExpr):
            return self._format_list(node)
        elif isinstance(node, DictExpr):
            return self._format_dict(node)
        elif isinstance(node, CallExpr):
            return self._format_call(node)
        elif isinstance(node, Attribute):
            obj_str = self._generate_expression_string(node.object)
            return f"{obj_str}.{node.attribute}"
        else:
            return str(node)
    
    def _format_literal(self, node: Literal) -> str:
        """Format literal value."""
        if node.literal_type == "string":
            return self._quote_string(node.value)
        elif node.literal_type == "boolean":
            return "True" if node.value else "False"
        elif node.literal_type == "none":
            return "None"
        else:
            return str(node.value)
    
    def _format_label(self, node: Label) -> str:
        """Format Bazel label."""
        return self._quote_string(str(node))
    
    def _format_list(self, node: ListExpr) -> str:
        """Format list expression."""
        if not node.elements:
            return "[]"
        
        if len(node.elements) == 1:
            element_str = self._generate_expression_string(node.elements[0])
            if len(element_str) < 60:
                return f"[{element_str}]"
        
        # Multi-line format
        lines = ["["]
        for i, element in enumerate(node.elements):
            element_str = self._generate_expression_string(element)
            comma = "," if i < len(node.elements) - 1 or self.style.use_trailing_commas else ""
            lines.append(f"    {element_str}{comma}")
        lines.append("]")
        
        return "\n".join(lines)
    
    def _format_dict(self, node: DictExpr) -> str:
        """Format dictionary expression."""
        if not node.pairs:
            return "{}"
        
        if len(node.pairs) == 1:
            key_str = self._generate_expression_string(node.pairs[0][0])
            value_str = self._generate_expression_string(node.pairs[0][1])
            if len(key_str) + len(value_str) < 50:
                return f"{{{key_str}: {value_str}}}"
        
        # Multi-line format
        lines = ["{"]
        for i, (key, value) in enumerate(node.pairs):
            key_str = self._generate_expression_string(key)
            value_str = self._generate_expression_string(value)
            comma = "," if i < len(node.pairs) - 1 or self.style.use_trailing_commas else ""
            lines.append(f"    {key_str}: {value_str}{comma}")
        lines.append("}")
        
        return "\n".join(lines)
    
    def _format_call(self, node: CallExpr) -> str:
        """Format function call."""
        function_str = self._generate_expression_string(node.function)
        
        all_args = []
        
        # Positional arguments
        for arg in node.args:
            arg_str = self._generate_expression_string(arg)
            all_args.append(arg_str)
        
        # Keyword arguments
        for name, value in node.kwargs.items():
            value_str = self._generate_expression_string(value)
            all_args.append(f"{name} = {value_str}")
        
        if not all_args:
            return f"{function_str}()"
        
        args_str = ", ".join(all_args)
        if len(function_str) + len(args_str) < 80:
            return f"{function_str}({args_str})"
        
        # Multi-line format
        lines = [f"{function_str}("]
        for i, arg in enumerate(all_args):
            comma = "," if i < len(all_args) - 1 or self.style.use_trailing_commas else ""
            lines.append(f"    {arg}{comma}")
        lines.append(")")
        
        return "\n".join(lines)
    
    def _format_string_list(self, strings: List[str]) -> str:
        """Format a list of strings."""
        if len(strings) == 1 and len(strings[0]) < 50:
            return f'["{strings[0]}"]'
        
        quoted_strings = [self._quote_string(s) for s in strings]
        return f"[{', '.join(quoted_strings)}]"
    
    def _quote_string(self, value: str) -> str:
        """Quote a string value."""
        # Escape quotes in the string
        escaped = value.replace('\\', '\\\\').replace(self.style.string_quote, f'\\{self.style.string_quote}')
        return f"{self.style.string_quote}{escaped}{self.style.string_quote}"
    
    def _generate_attribute_definition(self, attr_def: AttributeDefinition) -> str:
        """Generate attribute definition for rule."""
        attr_type = f"attr.{attr_def.attr_type}()"
        
        # Add configurations
        configs = []
        if attr_def.mandatory:
            configs.append("mandatory = True")
        if attr_def.default is not None:
            if isinstance(attr_def.default, str):
                default_str = self._quote_string(attr_def.default)
            else:
                default_str = str(attr_def.default)
            configs.append(f"default = {default_str}")
        if attr_def.doc:
            doc_str = self._quote_string(attr_def.doc)
            configs.append(f"doc = {doc_str}")
        
        if configs:
            configs_str = ", ".join(configs)
            return f"attr.{attr_def.attr_type}({configs_str})"
        
        return attr_type
    
    def _group_statements(self, statements: List[BazelStatement]) -> List[List[BazelStatement]]:
        """Group statements by type for better organization."""
        groups = []
        current_group = []
        current_type = None
        
        for stmt in statements:
            stmt_type = type(stmt)
            if stmt_type != current_type:
                if current_group:
                    groups.append(current_group)
                current_group = [stmt]
                current_type = stmt_type
            else:
                current_group.append(stmt)
        
        if current_group:
            groups.append(current_group)
        
        return groups
    
    def _group_workspace_rules(self, rules: List[WorkspaceRule]) -> Dict[str, List[WorkspaceRule]]:
        """Group workspace rules by type."""
        groups = {
            "local_repository": [],
            "git_repository": [], 
            "http_archive": [],
            "other": []
        }
        
        for rule in rules:
            rule_type = type(rule).__name__.lower()
            if rule_type in groups:
                groups[rule_type].append(rule)
            else:
                groups["other"].append(rule)
        
        return groups


# Public API functions
def generate_bazel(node: BazelNode, style: Optional[BazelCodeStyle] = None) -> str:
    """Generate Bazel code from AST node."""
    generator = BazelCodeGenerator(style)
    return generator.generate(node)


# Export classes and functions
__all__ = [
    'BazelCodeGenerator',
    'BazelCodeStyle', 
    'BazelFormatter',
    'generate_bazel'
] 