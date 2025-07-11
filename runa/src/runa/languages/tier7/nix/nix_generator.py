#!/usr/bin/env python3
"""
Nix Generator - Clean code generation for Nix Expression Language

Features:
- Clean Nix expression generation with proper formatting
- Multiple style options (modern, traditional, compact)
- Proper indentation and whitespace handling
- Function and attribute set formatting
- String interpolation and multi-line strings
- Comment preservation and formatting
- Expression parenthesization
- Package and derivation formatting
"""

from typing import List, Dict, Any, Optional, TextIO
from dataclasses import dataclass
from io import StringIO
import re

from .nix_ast import *

@dataclass
class NixCodeStyle:
    """Nix code style configuration"""
    # Indentation
    indent_size: int = 2               # Spaces for indentation
    use_spaces: bool = True            # Use spaces vs tabs
    
    # Line formatting
    max_line_length: int = 100         # Maximum line length
    break_long_expressions: bool = True # Break long expressions
    
    # Spacing
    space_around_operators: bool = True # x + y vs x+y
    space_after_comma: bool = True     # [a, b] vs [a,b]
    space_after_colon: bool = True     # a: b vs a:b
    space_around_equals: bool = True   # a = b vs a=b
    
    # Attribute sets
    align_attributes: bool = False     # Align attribute assignments
    trailing_comma: bool = False       # Add trailing comma in sets/lists
    break_long_attribute_sets: bool = True
    
    # Functions
    break_long_function_params: bool = True
    space_before_function_body: bool = True
    
    # Strings
    prefer_single_quotes: bool = False # Use single quotes when possible
    break_long_strings: bool = True    # Break long string literals
    
    # Comments
    preserve_comments: bool = True     # Preserve comments
    comment_spacing: int = 2           # Spaces before comments
    
    # Organization
    sort_imports: bool = False         # Sort import statements
    group_similar_attributes: bool = False

class NixFormatter:
    """Formatter for Nix code with style options"""
    
    def __init__(self, style: NixCodeStyle = None):
        self.style = style or NixCodeStyle()
        self.current_indent = 0
        
    def indent(self) -> str:
        """Get current indentation string"""
        if self.style.use_spaces:
            return " " * (self.current_indent * self.style.indent_size)
        else:
            return "\t" * self.current_indent
            
    def increase_indent(self) -> None:
        """Increase indentation level"""
        self.current_indent += 1
        
    def decrease_indent(self) -> None:
        """Decrease indentation level"""
        self.current_indent = max(0, self.current_indent - 1)
        
    def format_expression(self, expr: NixExpression) -> str:
        """Format any Nix expression"""
        if isinstance(expr, StringLiteral):
            return self.format_string_literal(expr)
        elif isinstance(expr, IntegerLiteral):
            return str(expr.value)
        elif isinstance(expr, FloatLiteral):
            return str(expr.value)
        elif isinstance(expr, BooleanLiteral):
            return "true" if expr.value else "false"
        elif isinstance(expr, NullLiteral):
            return "null"
        elif isinstance(expr, PathLiteral):
            return expr.value
        elif isinstance(expr, Identifier):
            return expr.name
        elif isinstance(expr, AttributeSet):
            return self.format_attribute_set(expr)
        elif isinstance(expr, AttributeAccess):
            return self.format_attribute_access(expr)
        elif isinstance(expr, ListExpression):
            return self.format_list_expression(expr)
        elif isinstance(expr, FunctionExpression):
            return self.format_function_expression(expr)
        elif isinstance(expr, FunctionApplication):
            return self.format_function_application(expr)
        elif isinstance(expr, LetExpression):
            return self.format_let_expression(expr)
        elif isinstance(expr, ConditionalExpression):
            return self.format_conditional_expression(expr)
        elif isinstance(expr, BinaryOperation):
            return self.format_binary_operation(expr)
        elif isinstance(expr, UnaryOperation):
            return self.format_unary_operation(expr)
        elif isinstance(expr, WithExpression):
            return self.format_with_expression(expr)
        elif isinstance(expr, AssertExpression):
            return self.format_assert_expression(expr)
        elif isinstance(expr, ImportExpression):
            return self.format_import_expression(expr)
        elif isinstance(expr, DerivationExpression):
            return self.format_derivation_expression(expr)
        elif isinstance(expr, BuiltinFunction):
            return expr.name
        elif isinstance(expr, StringInterpolation):
            return self.format_string_interpolation(expr)
        elif isinstance(expr, PackageExpression):
            return self.format_package_expression(expr)
        elif isinstance(expr, OverrideExpression):
            return self.format_override_expression(expr)
        elif isinstance(expr, CallPackageExpression):
            return self.format_call_package_expression(expr)
        else:
            return f"/* Unknown expression: {type(expr).__name__} */"
            
    def format_string_literal(self, string_lit: StringLiteral) -> str:
        """Format string literal"""
        value = string_lit.value
        quote = string_lit.quote_style
        
        # Choose quote style
        if not quote:
            if self.style.prefer_single_quotes and "'" not in value:
                quote = "'"
            else:
                quote = '"'
                
        # Handle multiline strings
        if '\n' in value and quote != "''":
            # Use multiline string syntax
            lines = value.split('\n')
            if len(lines) > 1:
                result = "''\n"
                self.increase_indent()
                for line in lines:
                    result += self.indent() + line + "\n"
                self.decrease_indent()
                result += self.indent() + "''"
                return result
                
        # Escape quotes in string
        if quote == '"':
            value = value.replace('"', r'\"')
        elif quote == "'":
            value = value.replace("'", r"\'")
            
        return f"{quote}{value}{quote}"
        
    def format_attribute_set(self, attr_set: AttributeSet) -> str:
        """Format attribute set"""
        if not attr_set.attributes:
            return "{ }"
            
        # Check if we should format on multiple lines
        single_line = self.should_format_single_line_set(attr_set)
        
        result = ""
        if attr_set.is_recursive:
            result += "rec "
            
        if single_line:
            result += "{ "
            bindings = []
            for binding in attr_set.attributes:
                bindings.append(self.format_attribute_binding(binding))
            result += "; ".join(bindings)
            if self.style.trailing_comma and bindings:
                result += ";"
            result += " }"
        else:
            result += "{\n"
            self.increase_indent()
            
            for i, binding in enumerate(attr_set.attributes):
                binding_str = self.format_attribute_binding(binding)
                result += self.indent() + binding_str
                
                # Add semicolon
                if i < len(attr_set.attributes) - 1 or self.style.trailing_comma:
                    result += ";"
                    
                result += "\n"
                
            self.decrease_indent()
            result += self.indent() + "}"
            
        return result
        
    def format_attribute_binding(self, binding: AttributeBinding) -> str:
        """Format attribute binding"""
        if binding.is_inherit:
            result = "inherit"
            if binding.inherit_source:
                source = self.format_expression(binding.inherit_source)
                result += f" ({source})"
            result += " " + " ".join(binding.path)
            return result
        else:
            # Regular binding
            path = ".".join(f'"{part}"' if " " in part else part for part in binding.path)
            value = self.format_expression(binding.value)
            
            if self.style.space_around_equals:
                return f"{path} = {value}"
            else:
                return f"{path}={value}"
                
    def format_attribute_access(self, access: AttributeAccess) -> str:
        """Format attribute access"""
        expr = self.format_expression(access.expression)
        
        # Parenthesize if necessary
        if self.needs_parentheses(access.expression):
            expr = f"({expr})"
            
        if isinstance(access.attribute, str):
            attr = access.attribute
            # Quote if necessary
            if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_-]*$', attr):
                attr = f'"{attr}"'
            result = f"{expr}.{attr}"
        else:
            # Dynamic attribute access
            attr_expr = self.format_expression(access.attribute)
            result = f"{expr}.{{{attr_expr}}}"
            
        # Handle default value
        if access.has_default and access.default_value:
            default = self.format_expression(access.default_value)
            result += f" or {default}"
            
        return result
        
    def format_list_expression(self, list_expr: ListExpression) -> str:
        """Format list expression"""
        if not list_expr.elements:
            return "[ ]"
            
        # Check if we should format on single line
        single_line = self.should_format_single_line_list(list_expr)
        
        if single_line:
            elements = []
            for elem in list_expr.elements:
                elements.append(self.format_expression(elem))
            separator = ", " if self.style.space_after_comma else ","
            return f"[ {separator.join(elements)} ]"
        else:
            result = "[\n"
            self.increase_indent()
            
            for elem in list_expr.elements:
                elem_str = self.format_expression(elem)
                result += self.indent() + elem_str + "\n"
                
            self.decrease_indent()
            result += self.indent() + "]"
            return result
            
    def format_function_expression(self, func_expr: FunctionExpression) -> str:
        """Format function expression"""
        if isinstance(func_expr.parameter, str):
            # Simple function: arg: body
            param = func_expr.parameter
        else:
            # Complex parameters: { a, b ? default }: body
            param = self.format_function_parameters(func_expr.parameter)
            
        body = self.format_expression(func_expr.body)
        
        # Add parentheses if body is complex
        if self.needs_parentheses(func_expr.body):
            body = f"({body})"
            
        if self.style.space_after_colon:
            return f"{param}: {body}"
        else:
            return f"{param}:{body}"
            
    def format_function_parameters(self, params: FunctionParameters) -> str:
        """Format function parameters"""
        if not params.parameters and not params.has_ellipsis:
            result = "{ }"
        else:
            parts = []
            
            for name, default in params.parameters.items():
                if default:
                    default_str = self.format_expression(default)
                    parts.append(f"{name} ? {default_str}")
                else:
                    parts.append(name)
                    
            if params.has_ellipsis:
                parts.append("...")
                
            if len(parts) == 1 and not self.style.break_long_function_params:
                result = f"{{ {parts[0]} }}"
            else:
                separator = ", " if self.style.space_after_comma else ","
                result = f"{{ {separator.join(parts)} }}"
                
        # Handle @ pattern
        if params.at_pattern:
            result += f" @ {params.at_pattern}"
            
        return result
        
    def format_function_application(self, app: FunctionApplication) -> str:
        """Format function application"""
        func = self.format_expression(app.function)
        arg = self.format_expression(app.argument)
        
        # Parenthesize if necessary
        if self.needs_parentheses(app.function):
            func = f"({func})"
        if self.needs_parentheses(app.argument):
            arg = f"({arg})"
            
        return f"{func} {arg}"
        
    def format_let_expression(self, let_expr: LetExpression) -> str:
        """Format let expression"""
        result = "let\n"
        self.increase_indent()
        
        for binding in let_expr.bindings:
            binding_str = self.format_attribute_binding(binding)
            result += self.indent() + binding_str + ";\n"
            
        self.decrease_indent()
        result += self.indent() + "in\n"
        
        body = self.format_expression(let_expr.body)
        if self.is_multiline_expression(let_expr.body):
            self.increase_indent()
            result += self.indent() + body
            self.decrease_indent()
        else:
            result += self.indent() + body
            
        return result
        
    def format_conditional_expression(self, cond_expr: ConditionalExpression) -> str:
        """Format conditional expression"""
        condition = self.format_expression(cond_expr.condition)
        then_expr = self.format_expression(cond_expr.then_expr)
        else_expr = self.format_expression(cond_expr.else_expr)
        
        # Check if we should format on multiple lines
        total_length = len(condition) + len(then_expr) + len(else_expr) + 20
        
        if total_length > self.style.max_line_length or self.is_multiline_expression(cond_expr.then_expr):
            result = f"if {condition}\n"
            self.increase_indent()
            result += f"{self.indent()}then {then_expr}\n"
            result += f"{self.indent()}else {else_expr}"
            self.decrease_indent()
            return result
        else:
            return f"if {condition} then {then_expr} else {else_expr}"
            
    def format_binary_operation(self, bin_op: BinaryOperation) -> str:
        """Format binary operation"""
        left = self.format_expression(bin_op.left)
        right = self.format_expression(bin_op.right)
        op = bin_op.operator
        
        # Parenthesize operands if necessary
        if self.needs_parentheses_in_binary_op(bin_op.left, op, True):
            left = f"({left})"
        if self.needs_parentheses_in_binary_op(bin_op.right, op, False):
            right = f"({right})"
            
        if self.style.space_around_operators:
            return f"{left} {op} {right}"
        else:
            return f"{left}{op}{right}"
            
    def format_unary_operation(self, unary_op: UnaryOperation) -> str:
        """Format unary operation"""
        operand = self.format_expression(unary_op.operand)
        op = unary_op.operator
        
        if self.needs_parentheses(unary_op.operand):
            operand = f"({operand})"
            
        return f"{op}{operand}"
        
    def format_with_expression(self, with_expr: WithExpression) -> str:
        """Format with expression"""
        namespace = self.format_expression(with_expr.namespace)
        body = self.format_expression(with_expr.body)
        
        return f"with {namespace}; {body}"
        
    def format_assert_expression(self, assert_expr: AssertExpression) -> str:
        """Format assert expression"""
        condition = self.format_expression(assert_expr.condition)
        body = self.format_expression(assert_expr.body)
        
        return f"assert {condition}; {body}"
        
    def format_import_expression(self, import_expr: ImportExpression) -> str:
        """Format import expression"""
        path = self.format_expression(import_expr.path)
        return f"import {path}"
        
    def format_derivation_expression(self, deriv_expr: DerivationExpression) -> str:
        """Format derivation expression"""
        # Derivations are special attribute sets
        attr_set = AttributeSet(attributes=deriv_expr.attributes)
        return f"derivation {self.format_attribute_set(attr_set)}"
        
    def format_string_interpolation(self, interp: StringInterpolation) -> str:
        """Format string interpolation"""
        expr = self.format_expression(interp.expression)
        return f"${{{expr}}}"
        
    def format_package_expression(self, pkg_expr: PackageExpression) -> str:
        """Format package expression"""
        deriv = self.format_derivation_expression(pkg_expr.derivation)
        
        if pkg_expr.meta:
            meta = self.format_expression(pkg_expr.meta)
            return f"{deriv} // {{ meta = {meta}; }}"
        else:
            return deriv
            
    def format_override_expression(self, override_expr: OverrideExpression) -> str:
        """Format override expression"""
        package = self.format_expression(override_expr.package)
        overrides = self.format_expression(override_expr.overrides)
        
        return f"{package}.override {overrides}"
        
    def format_call_package_expression(self, call_pkg_expr: CallPackageExpression) -> str:
        """Format callPackage expression"""
        package_path = self.format_expression(call_pkg_expr.package_path)
        
        if call_pkg_expr.arguments:
            args = self.format_expression(call_pkg_expr.arguments)
            return f"callPackage {package_path} {args}"
        else:
            return f"callPackage {package_path} {{}}"
            
    def format_comment(self, comment: Comment) -> str:
        """Format comment"""
        if comment.is_block:
            lines = comment.text.split('\n')
            if len(lines) == 1:
                return f"/* {comment.text} */"
            else:
                result = "/*\n"
                for line in lines:
                    result += f" * {line}\n"
                result += " */"
                return result
        else:
            return f"# {comment.text}"
            
    # Helper methods
    
    def should_format_single_line_set(self, attr_set: AttributeSet) -> bool:
        """Check if attribute set should be formatted on single line"""
        if len(attr_set.attributes) > 3:
            return False
            
        total_length = 4  # "{ }"
        for binding in attr_set.attributes:
            # Estimate length
            path_len = sum(len(p) for p in binding.path)
            total_length += path_len + 10  # rough estimate
            
        return total_length <= self.style.max_line_length // 2
        
    def should_format_single_line_list(self, list_expr: ListExpression) -> bool:
        """Check if list should be formatted on single line"""
        if len(list_expr.elements) > 5:
            return False
            
        total_length = 4  # "[ ]"
        for elem in list_expr.elements:
            # Estimate length
            total_length += 10  # rough estimate
            
        return total_length <= self.style.max_line_length // 2
        
    def needs_parentheses(self, expr: NixExpression) -> bool:
        """Check if expression needs parentheses in current context"""
        return isinstance(expr, (BinaryOperation, ConditionalExpression, 
                               LetExpression, WithExpression, AssertExpression))
                               
    def needs_parentheses_in_binary_op(self, expr: NixExpression, parent_op: str, is_left: bool) -> bool:
        """Check if expression needs parentheses in binary operation"""
        if not isinstance(expr, BinaryOperation):
            return False
            
        # Define operator precedence
        precedence = {
            '||': 1,
            '&&': 2,
            '==': 3, '!=': 3,
            '<': 4, '<=': 4, '>': 4, '>=': 4,
            '++': 5, '//': 5,
            '+': 6, '-': 6,
            '*': 7, '/': 7
        }
        
        parent_prec = precedence.get(parent_op, 0)
        expr_prec = precedence.get(expr.operator, 0)
        
        if expr_prec < parent_prec:
            return True
        if expr_prec == parent_prec and not is_left:
            return True
            
        return False
        
    def is_multiline_expression(self, expr: NixExpression) -> bool:
        """Check if expression is naturally multiline"""
        return isinstance(expr, (AttributeSet, LetExpression, ListExpression))

class NixCodeGenerator:
    """Main code generator for Nix"""
    
    def __init__(self, style: NixCodeStyle = None):
        self.style = style or NixCodeStyle()
        self.formatter = NixFormatter(self.style)
        
    def generate(self, ast: NixFile) -> str:
        """Generate Nix code from AST"""
        output = StringIO()
        self.generate_to_stream(ast, output)
        return output.getvalue()
        
    def generate_to_stream(self, ast: NixFile, stream: TextIO) -> None:
        """Generate Nix code to stream"""
        # Generate main expression
        expr_str = self.formatter.format_expression(ast.expression)
        stream.write(expr_str)
        
        # Ensure file ends with newline
        if not expr_str.endswith('\n'):
            stream.write('\n')
            
    def format_for_file(self, ast: NixFile) -> str:
        """Format for writing to file with proper structure"""
        result = self.generate(ast)
        
        # Add file header comment if requested
        if self.style.preserve_comments:
            header = "# Generated by Runa Universal Translation System\n\n"
            result = header + result
            
        return result

# Convenience functions

def generate_nix(ast: NixFile, style: NixCodeStyle = None) -> str:
    """Generate Nix code from AST"""
    generator = NixCodeGenerator(style)
    return generator.generate(ast)

def generate_nix_to_file(ast: NixFile, filename: str, style: NixCodeStyle = None) -> None:
    """Generate Nix code to file"""
    generator = NixCodeGenerator(style)
    code = generator.format_for_file(ast)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(code)

# Style presets

def modern_nix_style() -> NixCodeStyle:
    """Modern Nix style preset"""
    return NixCodeStyle(
        indent_size=2,
        max_line_length=100,
        space_around_operators=True,
        space_after_comma=True,
        trailing_comma=True,
        break_long_attribute_sets=True,
        break_long_function_params=True,
        preserve_comments=True
    )

def traditional_nix_style() -> NixCodeStyle:
    """Traditional Nix style preset"""
    return NixCodeStyle(
        indent_size=2,
        max_line_length=80,
        space_around_operators=True,
        space_after_comma=True,
        trailing_comma=False,
        break_long_attribute_sets=False,
        break_long_function_params=False,
        preserve_comments=True
    )

def compact_nix_style() -> NixCodeStyle:
    """Compact Nix style preset"""
    return NixCodeStyle(
        indent_size=1,
        max_line_length=120,
        space_around_operators=False,
        space_after_comma=False,
        trailing_comma=False,
        break_long_attribute_sets=False,
        break_long_function_params=False,
        preserve_comments=False,
        align_attributes=False
    )

def nixpkgs_style() -> NixCodeStyle:
    """Nixpkgs style preset matching repository conventions"""
    return NixCodeStyle(
        indent_size=2,
        max_line_length=79,
        space_around_operators=True,
        space_after_comma=True,
        trailing_comma=False,
        break_long_attribute_sets=True,
        break_long_function_params=True,
        preserve_comments=True,
        sort_imports=True,
        group_similar_attributes=True
    )

# Export main components
__all__ = [
    'NixCodeStyle', 'NixFormatter', 'NixCodeGenerator',
    'generate_nix', 'generate_nix_to_file',
    'modern_nix_style', 'traditional_nix_style', 'compact_nix_style', 'nixpkgs_style'
] 