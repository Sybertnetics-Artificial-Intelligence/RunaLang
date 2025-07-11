#!/usr/bin/env python3
"""
HCL Generator - Clean HCL Code Generation

Provides comprehensive HCL code generation with multiple formatting styles:
- Standard HCL format with proper indentation
- Terraform format with resource-specific styling
- Compact format for minimal space usage
- JSON-compatible format for tool integration
- Development format with extensive comments

Features:
- Proper block and attribute formatting
- String interpolation with ${} syntax
- Comment preservation and generation
- Attribute alignment and spacing
- Expression formatting with precedence
- Terraform-specific constructs formatting
"""

from typing import List, Dict, Optional, Any, Union, TextIO
from dataclasses import dataclass
from enum import Enum
import io

from .hcl_ast import *


class HCLFormatStyle(Enum):
    """HCL code formatting styles"""
    STANDARD = "standard"          # Clean, readable HCL
    TERRAFORM = "terraform"        # Terraform-specific formatting
    COMPACT = "compact"            # Minimal spacing
    JSON_COMPATIBLE = "json"       # JSON-compatible output
    DEVELOPMENT = "development"    # With extensive comments


@dataclass
class HCLGeneratorConfig:
    """Configuration for HCL code generation"""
    style: HCLFormatStyle = HCLFormatStyle.STANDARD
    indent_size: int = 2
    max_line_length: int = 120
    align_attributes: bool = True
    preserve_comments: bool = True
    add_trailing_commas: bool = False
    sort_attributes: bool = False
    quote_style: str = '"'  # or "'"
    
    # Terraform-specific options
    terraform_version: str = "1.0"
    group_terraform_blocks: bool = True
    add_block_comments: bool = False
    
    # Development options
    add_type_hints: bool = False
    add_documentation: bool = False
    verbose_interpolation: bool = False


class HCLCodeGenerator:
    """Generates clean HCL code from AST"""
    
    def __init__(self, config: Optional[HCLGeneratorConfig] = None):
        self.config = config or HCLGeneratorConfig()
        self.output = io.StringIO()
        self.indent_level = 0
        self.current_line_length = 0
        self.needs_newline = False
        
        # Operator precedence for proper parenthesization
        self.operator_precedence = {
            '||': 1,
            '&&': 2,
            '==': 3, '!=': 3,
            '<': 4, '<=': 4, '>': 4, '>=': 4,
            '+': 5, '-': 5,
            '*': 6, '/': 6, '%': 6,
            '!': 7, 'unary-': 7,
        }
    
    def generate(self, node: HCLNode) -> str:
        """Generate HCL code from AST node"""
        self.output = io.StringIO()
        self.indent_level = 0
        self.current_line_length = 0
        self.needs_newline = False
        
        if isinstance(node, HCLConfiguration):
            self._generate_configuration(node)
        else:
            node.accept(self)
        
        return self.output.getvalue()
    
    def _generate_configuration(self, config: HCLConfiguration) -> None:
        """Generate complete HCL configuration"""
        if self.config.style == HCLFormatStyle.DEVELOPMENT:
            self._write_line("# Generated HCL Configuration")
            self._write_line(f"# Terraform Version: {self.config.terraform_version}")
            self._write_line("")
        
        # Group items by type for better organization
        if self.config.group_terraform_blocks:
            self._generate_grouped_configuration(config)
        else:
            self._generate_sequential_configuration(config)
    
    def _generate_grouped_configuration(self, config: HCLConfiguration) -> None:
        """Generate configuration with grouped blocks"""
        # Separate items by type
        terraform_blocks = []
        providers = []
        variables = []
        locals = []
        data_sources = []
        resources = []
        modules = []
        outputs = []
        other_blocks = []
        attributes = []
        comments = []
        
        for item in config.body:
            if isinstance(item, HCLBlock):
                if item.type == "terraform":
                    terraform_blocks.append(item)
                elif item.type == "provider":
                    providers.append(item)
                elif item.type == "variable":
                    variables.append(item)
                elif item.type == "locals":
                    locals.append(item)
                elif item.type == "data":
                    data_sources.append(item)
                elif item.type == "resource":
                    resources.append(item)
                elif item.type == "module":
                    modules.append(item)
                elif item.type == "output":
                    outputs.append(item)
                else:
                    other_blocks.append(item)
            elif isinstance(item, HCLAttribute):
                attributes.append(item)
            elif isinstance(item, HCLComment):
                comments.append(item)
        
        # Generate in logical order
        sections = [
            ("Terraform Configuration", terraform_blocks),
            ("Providers", providers),
            ("Variables", variables),
            ("Local Values", locals),
            ("Data Sources", data_sources),
            ("Resources", resources),
            ("Modules", modules),
            ("Outputs", outputs),
            ("Other Blocks", other_blocks),
            ("Attributes", attributes),
        ]
        
        first_section = True
        for section_name, items in sections:
            if items:
                if not first_section:
                    self._write_line("")
                
                if self.config.add_block_comments and len(items) > 1:
                    self._write_line(f"# {section_name}")
                    self._write_line("")
                
                for i, item in enumerate(items):
                    if i > 0:
                        self._write_line("")
                    item.accept(self)
                
                first_section = False
    
    def _generate_sequential_configuration(self, config: HCLConfiguration) -> None:
        """Generate configuration in original order"""
        for i, item in enumerate(config.body):
            if i > 0 and isinstance(item, (HCLBlock, HCLAttribute)):
                self._write_line("")
            item.accept(self)
    
    # Visitor methods
    def visit_configuration(self, node: HCLConfiguration) -> None:
        self._generate_configuration(node)
    
    def visit_block(self, node: HCLBlock) -> None:
        """Generate HCL block"""
        # Block header
        self._write_indent()
        self._write(node.type)
        
        # Block labels
        for label in node.labels:
            self._write(" ")
            if self._needs_quotes(label):
                self._write(f'{self.config.quote_style}{label}{self.config.quote_style}')
            else:
                self._write(label)
        
        self._write(" {")
        
        if self.config.style == HCLFormatStyle.COMPACT:
            # Compact style - same line if possible
            if self._estimate_block_size(node) < 50:
                self._generate_compact_block_body(node)
                self._write("}")
                self._write_line("")
                return
        
        self._write_line("")
        
        # Block body
        self.indent_level += 1
        
        if self.config.sort_attributes:
            # Sort attributes first, then blocks
            attrs = [item for item in node.body if isinstance(item, HCLAttribute)]
            blocks = [item for item in node.body if isinstance(item, HCLBlock)]
            attrs.sort(key=lambda x: x.name)
            items = attrs + blocks
        else:
            items = node.body
        
        for i, item in enumerate(items):
            if i > 0 and isinstance(item, HCLBlock):
                self._write_line("")
            item.accept(self)
        
        self.indent_level -= 1
        self._write_indent()
        self._write_line("}")
    
    def visit_attribute(self, node: HCLAttribute) -> None:
        """Generate HCL attribute"""
        self._write_indent()
        self._write(node.name)
        
        if self.config.align_attributes:
            # Add spacing for alignment (simplified)
            self._write(" = ")
        else:
            self._write(" = ")
        
        # Generate value
        if isinstance(node.value, (HCLString, HCLList, HCLMap, HCLObject)):
            # Complex values may need line breaks
            if self._estimate_expression_size(node.value) > 60:
                self._write_line("")
                self.indent_level += 1
                self._write_indent()
                node.value.accept(self)
                self.indent_level -= 1
            else:
                node.value.accept(self)
        else:
            node.value.accept(self)
        
        self._write_line("")
    
    def visit_literal(self, node: HCLLiteral) -> None:
        if node.type == HCLType.STRING:
            self._write_string_literal(str(node.value))
        elif node.type == HCLType.NUMBER:
            self._write(str(node.value))
        elif node.type == HCLType.BOOL:
            self._write("true" if node.value else "false")
        elif node.type == HCLType.NULL:
            self._write("null")
        else:
            self._write(str(node.value))
    
    def visit_string(self, node: HCLString) -> None:
        """Generate HCL string with interpolation"""
        if node.is_heredoc:
            self._generate_heredoc(node)
        else:
            self._generate_interpolated_string(node)
    
    def visit_number(self, node: HCLNumber) -> None:
        self._write(node.raw_text)
    
    def visit_bool(self, node: HCLBool) -> None:
        self._write("true" if node.value else "false")
    
    def visit_null(self, node: HCLNull) -> None:
        self._write("null")
    
    def visit_list(self, node: HCLList) -> None:
        """Generate HCL list"""
        if not node.elements:
            self._write("[]")
            return
        
        if self.config.style == HCLFormatStyle.COMPACT or len(node.elements) == 1:
            # Compact format
            self._write("[")
            for i, element in enumerate(node.elements):
                if i > 0:
                    self._write(", ")
                element.accept(self)
            if self.config.add_trailing_commas and len(node.elements) > 1:
                self._write(",")
            self._write("]")
        else:
            # Multi-line format
            self._write("[")
            self._write_line("")
            self.indent_level += 1
            
            for i, element in enumerate(node.elements):
                self._write_indent()
                element.accept(self)
                if i < len(node.elements) - 1 or self.config.add_trailing_commas:
                    self._write(",")
                self._write_line("")
            
            self.indent_level -= 1
            self._write_indent()
            self._write("]")
    
    def visit_map(self, node: HCLMap) -> None:
        """Generate HCL map"""
        if not node.pairs:
            self._write("{}")
            return
        
        self._write("{")
        
        if self.config.style == HCLFormatStyle.COMPACT and len(node.pairs) <= 2:
            # Compact format
            for i, (key, value) in enumerate(node.pairs):
                if i > 0:
                    self._write(", ")
                key.accept(self)
                self._write(": ")
                value.accept(self)
            self._write("}")
        else:
            # Multi-line format
            self._write_line("")
            self.indent_level += 1
            
            for i, (key, value) in enumerate(node.pairs):
                self._write_indent()
                key.accept(self)
                self._write(" : ")
                value.accept(self)
                if i < len(node.pairs) - 1 or self.config.add_trailing_commas:
                    self._write(",")
                self._write_line("")
            
            self.indent_level -= 1
            self._write_indent()
            self._write("}")
    
    def visit_object(self, node: HCLObject) -> None:
        """Generate HCL object"""
        if not node.fields:
            self._write("{}")
            return
        
        self._write("{")
        
        if self.config.style == HCLFormatStyle.COMPACT and len(node.fields) <= 2:
            # Compact format
            for i, (key, value) in enumerate(node.fields.items()):
                if i > 0:
                    self._write(", ")
                self._write(key)
                self._write(" = ")
                value.accept(self)
            self._write("}")
        else:
            # Multi-line format
            self._write_line("")
            self.indent_level += 1
            
            items = list(node.fields.items())
            if self.config.sort_attributes:
                items.sort(key=lambda x: x[0])
            
            for i, (key, value) in enumerate(items):
                self._write_indent()
                self._write(key)
                self._write(" = ")
                value.accept(self)
                if i < len(items) - 1 or self.config.add_trailing_commas:
                    self._write(",")
                self._write_line("")
            
            self.indent_level -= 1
            self._write_indent()
            self._write("}")
    
    def visit_identifier(self, node: HCLIdentifier) -> None:
        self._write(node.name)
    
    def visit_attribute_access(self, node: HCLAttributeAccess) -> None:
        node.object.accept(self)
        self._write(".")
        self._write(node.attribute)
    
    def visit_index_access(self, node: HCLIndexAccess) -> None:
        node.object.accept(self)
        self._write("[")
        node.index.accept(self)
        self._write("]")
    
    def visit_function_call(self, node: HCLFunctionCall) -> None:
        """Generate HCL function call"""
        self._write(node.name)
        self._write("(")
        
        if node.args:
            if self.config.style == HCLFormatStyle.COMPACT or len(node.args) <= 3:
                # Single line
                for i, arg in enumerate(node.args):
                    if i > 0:
                        self._write(", ")
                    arg.accept(self)
            else:
                # Multi-line for complex function calls
                self._write_line("")
                self.indent_level += 1
                
                for i, arg in enumerate(node.args):
                    self._write_indent()
                    arg.accept(self)
                    if i < len(node.args) - 1:
                        self._write(",")
                    self._write_line("")
                
                self.indent_level -= 1
                self._write_indent()
        
        self._write(")")
    
    def visit_binary_op(self, node: HCLBinaryOp) -> None:
        """Generate binary operation with proper precedence"""
        left_needs_parens = self._needs_parentheses(node.left, node.operator, True)
        right_needs_parens = self._needs_parentheses(node.right, node.operator, False)
        
        if left_needs_parens:
            self._write("(")
        node.left.accept(self)
        if left_needs_parens:
            self._write(")")
        
        # Add spacing around operator
        self._write(f" {node.operator} ")
        
        if right_needs_parens:
            self._write("(")
        node.right.accept(self)
        if right_needs_parens:
            self._write(")")
    
    def visit_unary_op(self, node: HCLUnaryOp) -> None:
        self._write(node.operator)
        
        # Add space for word operators
        if node.operator.isalpha():
            self._write(" ")
        
        needs_parens = isinstance(node.operand, (HCLBinaryOp, HCLConditional))
        if needs_parens:
            self._write("(")
        node.operand.accept(self)
        if needs_parens:
            self._write(")")
    
    def visit_conditional(self, node: HCLConditional) -> None:
        """Generate conditional expression"""
        # Check if we need to break lines
        estimated_size = (self._estimate_expression_size(node.condition) + 
                         self._estimate_expression_size(node.true_value) + 
                         self._estimate_expression_size(node.false_value))
        
        if estimated_size > 80 and self.config.style != HCLFormatStyle.COMPACT:
            # Multi-line conditional
            node.condition.accept(self)
            self._write_line(" ?")
            self.indent_level += 1
            self._write_indent()
            node.true_value.accept(self)
            self._write_line(" :")
            self._write_indent()
            node.false_value.accept(self)
            self.indent_level -= 1
        else:
            # Single line conditional
            node.condition.accept(self)
            self._write(" ? ")
            node.true_value.accept(self)
            self._write(" : ")
            node.false_value.accept(self)
    
    def visit_interpolation(self, node: HCLInterpolation) -> None:
        """Generate string interpolation"""
        self._write("${")
        node.expression.accept(self)
        self._write("}")
    
    def visit_for_expression(self, node: HCLForExpression) -> None:
        """Generate for expression"""
        if node.is_object:
            self._write("{")
        else:
            self._write("[")
        
        self._write("for ")
        
        if node.key_var:
            self._write(f"{node.key_var}, ")
        self._write(f"{node.value_var} in ")
        node.collection.accept(self)
        self._write(" : ")
        
        if node.key_expr:
            node.key_expr.accept(self)
            self._write(" => ")
        
        node.value_expr.accept(self)
        
        if node.condition:
            self._write(" if ")
            node.condition.accept(self)
        
        if node.is_object:
            self._write("}")
        else:
            self._write("]")
    
    def visit_splat_expression(self, node: HCLSplatExpression) -> None:
        node.source.accept(self)
        self._write("[*].")
        node.each.accept(self)
    
    def visit_comment(self, node: HCLComment) -> None:
        if not self.config.preserve_comments:
            return
        
        if node.is_line_comment:
            self._write_indent()
            self._write(f"// {node.text}")
            self._write_line("")
        else:
            self._write_indent()
            self._write(f"/* {node.text} */")
            self._write_line("")
    
    # Terraform-specific visitors
    def visit_variable(self, node: HCLVariable) -> None:
        self.visit_block(node)
    
    def visit_local(self, node: HCLLocal) -> None:
        self.visit_block(node)
    
    def visit_output(self, node: HCLOutput) -> None:
        self.visit_block(node)
    
    def visit_resource(self, node: HCLResource) -> None:
        if self.config.add_block_comments:
            self._write_indent()
            self._write_line(f"# {node.type}.{node.name}")
        self.visit_block(node)
    
    def visit_data_source(self, node: HCLDataSource) -> None:
        if self.config.add_block_comments:
            self._write_indent()
            self._write_line(f"# data.{node.type}.{node.name}")
        self.visit_block(node)
    
    def visit_provider(self, node: HCLProvider) -> None:
        self.visit_block(node)
    
    def visit_module(self, node: HCLModule) -> None:
        if self.config.add_block_comments:
            self._write_indent()
            self._write_line(f"# module.{node.name}")
        self.visit_block(node)
    
    def visit_validation(self, node: HCLValidation) -> None:
        self._write_indent()
        self._write_line("validation {")
        self.indent_level += 1
        
        self._write_indent()
        self._write("condition = ")
        node.condition.accept(self)
        self._write_line("")
        
        self._write_indent()
        self._write(f'error_message = "{node.error_message}"')
        self._write_line("")
        
        self.indent_level -= 1
        self._write_indent()
        self._write_line("}")
    
    def visit_lifecycle(self, node: HCLLifecycle) -> None:
        self._write_indent()
        self._write_line("lifecycle {")
        self.indent_level += 1
        
        if node.create_before_destroy:
            self._write_indent()
            self._write_line("create_before_destroy = true")
        
        if node.prevent_destroy:
            self._write_indent()
            self._write_line("prevent_destroy = true")
        
        if node.ignore_changes:
            self._write_indent()
            self._write("ignore_changes = [")
            for i, change in enumerate(node.ignore_changes):
                if i > 0:
                    self._write(", ")
                self._write(change)
            self._write_line("]")
        
        self.indent_level -= 1
        self._write_indent()
        self._write_line("}")
    
    # Helper methods
    def _generate_heredoc(self, node: HCLString) -> None:
        """Generate heredoc string"""
        if node.heredoc_identifier:
            self._write(f"<<{node.heredoc_identifier}")
            self._write_line("")
            
            # Write heredoc content
            for part in node.parts:
                if isinstance(part, str):
                    # Split into lines and write each
                    lines = part.split('\n')
                    for line in lines:
                        self._write_line(line)
                elif isinstance(part, HCLInterpolation):
                    part.accept(self)
            
            self._write_line(node.heredoc_identifier)
    
    def _generate_interpolated_string(self, node: HCLString) -> None:
        """Generate string with interpolation"""
        self._write(self.config.quote_style)
        
        for part in node.parts:
            if isinstance(part, str):
                # Escape quotes and special characters
                escaped = part.replace('\\', '\\\\')
                escaped = escaped.replace(self.config.quote_style, f'\\{self.config.quote_style}')
                self._write(escaped)
            elif isinstance(part, HCLInterpolation):
                part.accept(self)
        
        self._write(self.config.quote_style)
    
    def _generate_compact_block_body(self, node: HCLBlock) -> None:
        """Generate compact block body on same line"""
        for i, item in enumerate(node.body):
            if i > 0:
                self._write("; ")
            if isinstance(item, HCLAttribute):
                self._write(f"{item.name} = ")
                item.value.accept(self)
    
    def _write_string_literal(self, value: str) -> None:
        """Write a string literal with proper escaping"""
        self._write(self.config.quote_style)
        escaped = value.replace('\\', '\\\\')
        escaped = escaped.replace(self.config.quote_style, f'\\{self.config.quote_style}')
        self._write(escaped)
        self._write(self.config.quote_style)
    
    def _needs_quotes(self, value: str) -> bool:
        """Check if a string value needs quotes"""
        if not value:
            return True
        
        # Check if it's a valid identifier
        if not (value[0].isalpha() or value[0] == '_'):
            return True
        
        for char in value[1:]:
            if not (char.isalnum() or char in '_-'):
                return True
        
        return False
    
    def _needs_parentheses(self, expr: HCLExpression, parent_op: str, is_left: bool) -> bool:
        """Check if expression needs parentheses"""
        if not isinstance(expr, HCLBinaryOp):
            return False
        
        parent_prec = self.operator_precedence.get(parent_op, 0)
        expr_prec = self.operator_precedence.get(expr.operator, 0)
        
        if expr_prec < parent_prec:
            return True
        
        # Same precedence - check associativity
        if expr_prec == parent_prec and not is_left:
            return True
        
        return False
    
    def _estimate_expression_size(self, expr: HCLExpression) -> int:
        """Estimate the size of an expression when rendered"""
        if isinstance(expr, (HCLString, HCLIdentifier)):
            return 10
        elif isinstance(expr, HCLNumber):
            return 5
        elif isinstance(expr, (HCLBool, HCLNull)):
            return 5
        elif isinstance(expr, HCLList):
            return 5 + sum(self._estimate_expression_size(e) for e in expr.elements)
        elif isinstance(expr, (HCLMap, HCLObject)):
            return 20  # Simplified estimate
        elif isinstance(expr, HCLBinaryOp):
            return (self._estimate_expression_size(expr.left) + 
                   self._estimate_expression_size(expr.right) + 5)
        elif isinstance(expr, HCLFunctionCall):
            return 10 + sum(self._estimate_expression_size(arg) for arg in expr.args)
        else:
            return 10
    
    def _estimate_block_size(self, block: HCLBlock) -> int:
        """Estimate the size of a block when rendered"""
        size = len(block.type) + sum(len(label) for label in block.labels)
        size += sum(len(getattr(item, 'name', '')) + 10 for item in block.body)
        return size
    
    def _write(self, text: str) -> None:
        """Write text to output"""
        self.output.write(text)
        self.current_line_length += len(text)
    
    def _write_line(self, text: str = "") -> None:
        """Write line to output"""
        if text:
            self._write(text)
        self.output.write("\n")
        self.current_line_length = 0
        self.needs_newline = False
    
    def _write_indent(self) -> None:
        """Write current indentation"""
        indent = " " * (self.indent_level * self.config.indent_size)
        self._write(indent)


class HCLFormatter:
    """Utility class for HCL code formatting"""
    
    @staticmethod
    def format_hcl(code: str, style: HCLFormatStyle = HCLFormatStyle.STANDARD) -> str:
        """Format HCL code string"""
        from .hcl_parser import parse_hcl
        
        try:
            ast = parse_hcl(code)
            config = HCLGeneratorConfig(style=style)
            generator = HCLCodeGenerator(config)
            return generator.generate(ast)
        except Exception:
            # Return original code if parsing fails
            return code
    
    @staticmethod
    def minify_hcl(code: str) -> str:
        """Minify HCL code"""
        config = HCLGeneratorConfig(
            style=HCLFormatStyle.COMPACT,
            indent_size=0,
            align_attributes=False,
            preserve_comments=False
        )
        
        from .hcl_parser import parse_hcl
        
        try:
            ast = parse_hcl(code)
            generator = HCLCodeGenerator(config)
            return generator.generate(ast)
        except Exception:
            return code
    
    @staticmethod
    def terraform_format(code: str) -> str:
        """Format code using Terraform conventions"""
        config = HCLGeneratorConfig(
            style=HCLFormatStyle.TERRAFORM,
            group_terraform_blocks=True,
            sort_attributes=True,
            add_block_comments=True
        )
        
        from .hcl_parser import parse_hcl
        
        try:
            ast = parse_hcl(code)
            generator = HCLCodeGenerator(config)
            return generator.generate(ast)
        except Exception:
            return code


# Convenience functions
def generate_hcl(node: HCLNode, style: HCLFormatStyle = HCLFormatStyle.STANDARD) -> str:
    """Generate HCL code from AST node"""
    config = HCLGeneratorConfig(style=style)
    generator = HCLCodeGenerator(config)
    return generator.generate(node)


def format_hcl_code(code: str, style: HCLFormatStyle = HCLFormatStyle.STANDARD) -> str:
    """Parse and reformat HCL code"""
    return HCLFormatter.format_hcl(code, style) 