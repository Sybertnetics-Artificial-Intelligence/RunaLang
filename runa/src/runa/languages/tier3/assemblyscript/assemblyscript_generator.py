#!/usr/bin/env python3
"""
AssemblyScript Code Generator

Generates AssemblyScript text from AssemblyScript AST nodes with support for multiple formatting styles.

Author: Sybertnetics AI Solutions
License: MIT
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass
from enum import Enum, auto
import logging

from .assemblyscript_ast import *


class AssemblyScriptCodeStyle(Enum):
    """AssemblyScript code formatting styles."""
    STANDARD = "standard"
    COMPACT = "compact"
    PRETTY = "pretty"
    MINIFIED = "minified"


@dataclass
class AssemblyScriptFormattingOptions:
    """AssemblyScript code formatting options."""
    indent_size: int = 2
    use_tabs: bool = False
    max_line_length: int = 120
    
    # AssemblyScript-specific
    semicolons: str = "always"  # "always", "never", "auto"
    trailing_comma: bool = False
    space_before_function_paren: bool = False
    brace_style: str = "1tbs"  # "1tbs", "allman", "stroustrup"
    quote_style: str = "double"  # "double", "single"
    line_break: str = '\n'
    
    # Type annotations
    explicit_return_types: bool = True
    explicit_parameter_types: bool = True
    
    # Export/Import formatting
    organize_imports: bool = True
    group_imports: bool = True


class AssemblyScriptFormatter:
    """AssemblyScript code formatter with style presets."""
    
    @staticmethod
    def get_style_options(style: AssemblyScriptCodeStyle) -> AssemblyScriptFormattingOptions:
        """Get formatting options for a specific style."""
        if style == AssemblyScriptCodeStyle.STANDARD:
            return AssemblyScriptFormattingOptions(
                indent_size=2,
                semicolons="always",
                explicit_return_types=True
            )
        elif style == AssemblyScriptCodeStyle.COMPACT:
            return AssemblyScriptFormattingOptions(
                indent_size=1,
                max_line_length=200,
                trailing_comma=False,
                space_before_function_paren=False
            )
        elif style == AssemblyScriptCodeStyle.PRETTY:
            return AssemblyScriptFormattingOptions(
                indent_size=4,
                trailing_comma=True,
                space_before_function_paren=True,
                organize_imports=True,
                explicit_return_types=True
            )
        elif style == AssemblyScriptCodeStyle.MINIFIED:
            return AssemblyScriptFormattingOptions(
                indent_size=0,
                line_break="",
                semicolons="never",
                trailing_comma=False,
                space_before_function_paren=False
            )
        else:
            return AssemblyScriptFormattingOptions()


class AssemblyScriptCodeGenerator(AsVisitorExtended):
    """AssemblyScript code generator that produces formatted code from AST."""
    
    def __init__(self, style: AssemblyScriptCodeStyle = AssemblyScriptCodeStyle.STANDARD):
        self.style = style
        self.options = AssemblyScriptFormatter.get_style_options(style)
        self.logger = logging.getLogger(__name__)
        
        # Output state
        self.output = []
        self.indent_level = 0
        self.current_line_length = 0
        self.needs_indent = True
    
    def generate(self, node: AsNode) -> str:
        """Generate AssemblyScript text from an AST node."""
        self.output = []
        self.indent_level = 0
        self.current_line_length = 0
        self.needs_indent = True
        
        try:
            node.accept(self)
            result = "".join(self.output)
            return self._post_process(result)
        except Exception as e:
            self.logger.error(f"AssemblyScript code generation failed: {e}")
            raise RuntimeError(f"Failed to generate AssemblyScript code: {e}")
    
    def _post_process(self, code: str) -> str:
        """Post-process generated code."""
        if self.style == AssemblyScriptCodeStyle.MINIFIED:
            # Remove unnecessary whitespace for minified style
            lines = code.split('\n')
            processed_lines = []
            for line in lines:
                line = line.strip()
                if line:
                    processed_lines.append(line)
            return ' '.join(processed_lines)
        else:
            # Standard post-processing
            lines = code.split('\n')
            processed_lines = []
            
            for line in lines:
                # Remove trailing whitespace
                line = line.rstrip()
                processed_lines.append(line)
            
            # Remove trailing empty lines
            while processed_lines and not processed_lines[-1]:
                processed_lines.pop()
            
            return '\n'.join(processed_lines)
    
    def _write(self, text: str):
        """Write text to output."""
        if self.needs_indent and text.strip() and self.options.line_break:
            self._write_indent()
            self.needs_indent = False
        
        self.output.append(text)
        self.current_line_length += len(text)
    
    def _write_line(self, text: str = ""):
        """Write a line of text."""
        if text:
            self._write(text)
        if self.options.line_break:
            self.output.append(self.options.line_break)
            self.current_line_length = 0
            self.needs_indent = True
    
    def _write_indent(self):
        """Write current indentation."""
        if self.indent_level > 0:
            if self.options.use_tabs:
                indent = '\t' * self.indent_level
            else:
                indent = ' ' * (self.indent_level * self.options.indent_size)
            
            self.output.append(indent)
            self.current_line_length += len(indent)
    
    def _increase_indent(self):
        """Increase indentation level."""
        self.indent_level += 1
    
    def _decrease_indent(self):
        """Decrease indentation level."""
        self.indent_level = max(0, self.indent_level - 1)
    
    def _write_semicolon(self):
        """Write semicolon if required by style."""
        if self.options.semicolons == "always":
            self._write(";")
    
    def _quote_string(self, text: str) -> str:
        """Quote string according to style."""
        if self.options.quote_style == "single":
            return f"'{text}'"
        else:
            return f'"{text}"'
    
    def _write_brace_start(self):
        """Write opening brace according to brace style."""
        if self.options.brace_style == "allman":
            self._write_line()
            self._write("{")
        else:  # 1tbs, stroustrup
            self._write(" {")
    
    # Visitor methods
    def visit_as_program(self, node: AsProgram):
        """Visit AssemblyScript program."""
        # Write imports first
        if node.imports:
            for import_stmt in node.imports:
                import_stmt.accept(self)
                self._write_line()
            
            # Add blank line after imports
            if node.statements:
                self._write_line()
        
        # Write statements
        for i, stmt in enumerate(node.statements):
            stmt.accept(self)
            
            # Add blank line between top-level declarations
            if i < len(node.statements) - 1 and self.options.line_break:
                self._write_line()
        
        # Write exports at the end
        if node.exports:
            if node.statements:
                self._write_line()
            
            for export_stmt in node.exports:
                export_stmt.accept(self)
                self._write_line()
    
    def visit_as_function(self, node: AsFunction):
        """Visit AssemblyScript function."""
        # Write decorators
        for decorator in node.decorators:
            self._write(f"@{decorator}")
            self._write_line()
        
        # Write export if needed
        if node.is_export:
            self._write("export ")
        
        # Write function keyword
        self._write("function ")
        
        # Write function name
        self._write(node.name)
        
        # Write generic parameters
        if node.generic_params:
            self._write("<")
            for i, param in enumerate(node.generic_params):
                if i > 0:
                    self._write(", ")
                self._write(param)
            self._write(">")
        
        # Write parameters
        paren_space = " " if self.options.space_before_function_paren else ""
        self._write(f"{paren_space}(")
        
        for i, param in enumerate(node.parameters):
            if i > 0:
                self._write(", ")
            
            self._write(param.name)
            if self.options.explicit_parameter_types and param.param_type:
                self._write(": ")
                param.param_type.accept(self)
            
            if param.default_value:
                self._write(" = ")
                param.default_value.accept(self)
        
        self._write(")")
        
        # Write return type
        if self.options.explicit_return_types and node.return_type:
            self._write(": ")
            node.return_type.accept(self)
        
        # Write function body
        self._write_brace_start()
        self._write_line()
        
        self._increase_indent()
        for stmt in node.body:
            stmt.accept(self)
            self._write_line()
        self._decrease_indent()
        
        self._write("}")
        self._write_line()
    
    def visit_as_class(self, node: AsClass):
        """Visit AssemblyScript class."""
        # Write decorators
        for decorator in node.decorators:
            self._write(f"@{decorator}")
            self._write_line()
        
        # Write export and modifiers
        if node.is_export:
            self._write("export ")
        
        if node.is_abstract:
            self._write("abstract ")
        
        self._write("class ")
        self._write(node.name)
        
        # Write generic parameters
        if node.generic_params:
            self._write("<")
            for i, param in enumerate(node.generic_params):
                if i > 0:
                    self._write(", ")
                self._write(param)
            self._write(">")
        
        # Write inheritance
        if node.super_class:
            self._write(f" extends {node.super_class}")
        
        if node.implements:
            self._write(" implements ")
            for i, interface in enumerate(node.implements):
                if i > 0:
                    self._write(", ")
                self._write(interface)
        
        # Write class body
        self._write_brace_start()
        self._write_line()
        
        self._increase_indent()
        for i, member in enumerate(node.members):
            self._write_class_member(member)
            
            # Add blank line between members
            if i < len(node.members) - 1:
                self._write_line()
        
        self._decrease_indent()
        self._write("}")
        self._write_line()
    
    def _write_class_member(self, member: AsClassMember):
        """Write class member."""
        # Write access modifier
        if member.access_modifier != "public":
            self._write(f"{member.access_modifier} ")
        
        # Write modifiers
        if member.is_static:
            self._write("static ")
        
        if member.is_readonly:
            self._write("readonly ")
        
        if member.is_abstract:
            self._write("abstract ")
        
        # Write member based on type
        if member.member_type == "field":
            self._write(member.name)
            if member.field_type:
                self._write(": ")
                member.field_type.accept(self)
            
            if member.initial_value:
                self._write(" = ")
                member.initial_value.accept(self)
            
            self._write_semicolon()
            self._write_line()
        
        elif member.member_type == "method" and member.method:
            self.visit_as_function(member.method)
        
        elif member.member_type == "constructor":
            self._write("constructor(")
            # Write constructor parameters (simplified)
            self._write(")")
            self._write_brace_start()
            self._write_line()
            self._write("}")
            self._write_line()
    
    def visit_as_interface(self, node: AsInterface):
        """Visit AssemblyScript interface."""
        if node.is_export:
            self._write("export ")
        
        self._write("interface ")
        self._write(node.name)
        
        # Write generic parameters
        if node.generic_params:
            self._write("<")
            for i, param in enumerate(node.generic_params):
                if i > 0:
                    self._write(", ")
                self._write(param)
            self._write(">")
        
        # Write extends clause
        if node.extends:
            self._write(" extends ")
            for i, ext in enumerate(node.extends):
                if i > 0:
                    self._write(", ")
                self._write(ext)
        
        # Write interface body
        self._write_brace_start()
        self._write_line()
        
        self._increase_indent()
        for member in node.members:
            self._write_interface_member(member)
        self._decrease_indent()
        
        self._write("}")
        self._write_line()
    
    def _write_interface_member(self, member: AsInterfaceMember):
        """Write interface member."""
        self._write(member.name)
        
        if member.member_type == "method":
            self._write("(")
            for i, param in enumerate(member.method_params):
                if i > 0:
                    self._write(", ")
                self._write(param.name)
                if param.param_type:
                    self._write(": ")
                    param.param_type.accept(self)
            self._write(")")
            
            if member.return_type:
                self._write(": ")
                member.return_type.accept(self)
        
        elif member.member_type == "property" and member.signature_type:
            self._write(": ")
            member.signature_type.accept(self)
        
        self._write_semicolon()
        self._write_line()
    
    def visit_as_variable_declaration(self, node: AsVariableDeclaration):
        """Visit AssemblyScript variable declaration."""
        if node.is_export:
            self._write("export ")
        
        if node.is_const:
            self._write("const ")
        else:
            self._write("let ")
        
        self._write(node.name)
        
        if node.var_type:
            self._write(": ")
            node.var_type.accept(self)
        
        if node.initial_value:
            self._write(" = ")
            node.initial_value.accept(self)
        
        self._write_semicolon()
    
    def visit_as_expression(self, node: AsExpression):
        """Visit AssemblyScript expression (base implementation)."""
        if isinstance(node, AsLiteral):
            self._visit_literal(node)
        elif isinstance(node, AsIdentifier):
            self._write(node.name)
        elif isinstance(node, AsBinaryExpression):
            self._visit_binary_expression(node)
        elif isinstance(node, AsUnaryExpression):
            self._visit_unary_expression(node)
        elif isinstance(node, AsCallExpression):
            self._visit_call_expression(node)
        elif isinstance(node, AsMemberExpression):
            self._visit_member_expression(node)
        elif isinstance(node, AsArrayExpression):
            self._visit_array_expression(node)
        elif isinstance(node, AsObjectExpression):
            self._visit_object_expression(node)
        else:
            self._write("unknown")
    
    def _visit_literal(self, node: AsLiteral):
        """Visit literal expression."""
        if node.literal_type == "string":
            self._write(self._quote_string(str(node.value)))
        elif node.literal_type == "boolean":
            self._write("true" if node.value else "false")
        elif node.literal_type == "null":
            self._write("null")
        else:
            self._write(str(node.value))
    
    def _visit_binary_expression(self, node: AsBinaryExpression):
        """Visit binary expression."""
        node.left.accept(self)
        self._write(f" {node.operator} ")
        node.right.accept(self)
    
    def _visit_unary_expression(self, node: AsUnaryExpression):
        """Visit unary expression."""
        if node.is_prefix:
            self._write(node.operator)
            node.operand.accept(self)
        else:
            node.operand.accept(self)
            self._write(node.operator)
    
    def _visit_call_expression(self, node: AsCallExpression):
        """Visit call expression."""
        node.function.accept(self)
        
        # Write type arguments
        if node.type_arguments:
            self._write("<")
            for i, type_arg in enumerate(node.type_arguments):
                if i > 0:
                    self._write(", ")
                type_arg.accept(self)
            self._write(">")
        
        self._write("(")
        for i, arg in enumerate(node.arguments):
            if i > 0:
                self._write(", ")
            arg.accept(self)
        self._write(")")
    
    def _visit_member_expression(self, node: AsMemberExpression):
        """Visit member expression."""
        node.object.accept(self)
        
        if node.computed:
            self._write("[")
            node.property.accept(self)
            self._write("]")
        else:
            self._write(".")
            node.property.accept(self)
    
    def _visit_array_expression(self, node: AsArrayExpression):
        """Visit array expression."""
        self._write("[")
        for i, element in enumerate(node.elements):
            if i > 0:
                self._write(", ")
            if element:
                element.accept(self)
        
        if self.options.trailing_comma and node.elements:
            self._write(",")
        
        self._write("]")
    
    def _visit_object_expression(self, node: AsObjectExpression):
        """Visit object expression."""
        self._write("{")
        
        if node.properties:
            if self.options.line_break:
                self._write_line()
                self._increase_indent()
            
            for i, prop in enumerate(node.properties):
                if i > 0:
                    self._write(",")
                    if self.options.line_break:
                        self._write_line()
                
                # Write property key
                if prop.computed:
                    self._write("[")
                    prop.key.accept(self)
                    self._write("]")
                else:
                    prop.key.accept(self)
                
                self._write(": ")
                prop.value.accept(self)
            
            if self.options.trailing_comma:
                self._write(",")
            
            if self.options.line_break:
                self._write_line()
                self._decrease_indent()
        
        self._write("}")
    
    def visit_as_statement(self, node: AsStatement):
        """Visit AssemblyScript statement (base implementation)."""
        if isinstance(node, AsBlock):
            self._visit_block(node)
        elif isinstance(node, AsIfStatement):
            self._visit_if_statement(node)
        elif isinstance(node, AsWhileStatement):
            self._visit_while_statement(node)
        elif isinstance(node, AsForStatement):
            self._visit_for_statement(node)
        elif isinstance(node, AsReturnStatement):
            self._visit_return_statement(node)
        elif isinstance(node, AsExpressionStatement):
            node.expression.accept(self)
            self._write_semicolon()
        elif isinstance(node, AsVariableDeclaration):
            self.visit_as_variable_declaration(node)
    
    def _visit_block(self, node: AsBlock):
        """Visit block statement."""
        self._write_brace_start()
        self._write_line()
        
        self._increase_indent()
        for stmt in node.statements:
            stmt.accept(self)
            self._write_line()
        self._decrease_indent()
        
        self._write("}")
    
    def _visit_if_statement(self, node: AsIfStatement):
        """Visit if statement."""
        self._write("if (")
        node.condition.accept(self)
        self._write(")")
        
        if isinstance(node.then_statement, AsBlock):
            node.then_statement.accept(self)
        else:
            self._write_brace_start()
            self._write_line()
            self._increase_indent()
            node.then_statement.accept(self)
            self._write_line()
            self._decrease_indent()
            self._write("}")
        
        if node.else_statement:
            self._write(" else")
            
            if isinstance(node.else_statement, AsIfStatement):
                self._write(" ")
                node.else_statement.accept(self)
            elif isinstance(node.else_statement, AsBlock):
                node.else_statement.accept(self)
            else:
                self._write_brace_start()
                self._write_line()
                self._increase_indent()
                node.else_statement.accept(self)
                self._write_line()
                self._decrease_indent()
                self._write("}")
    
    def _visit_while_statement(self, node: AsWhileStatement):
        """Visit while statement."""
        self._write("while (")
        node.condition.accept(self)
        self._write(")")
        
        if isinstance(node.body, AsBlock):
            node.body.accept(self)
        else:
            self._write_brace_start()
            self._write_line()
            self._increase_indent()
            node.body.accept(self)
            self._write_line()
            self._decrease_indent()
            self._write("}")
    
    def _visit_for_statement(self, node: AsForStatement):
        """Visit for statement."""
        self._write("for (")
        
        if node.init:
            node.init.accept(self)
        self._write("; ")
        
        if node.condition:
            node.condition.accept(self)
        self._write("; ")
        
        if node.update:
            node.update.accept(self)
        
        self._write(")")
        
        if isinstance(node.body, AsBlock):
            node.body.accept(self)
        else:
            self._write_brace_start()
            self._write_line()
            self._increase_indent()
            node.body.accept(self)
            self._write_line()
            self._decrease_indent()
            self._write("}")
    
    def _visit_return_statement(self, node: AsReturnStatement):
        """Visit return statement."""
        self._write("return")
        if node.value:
            self._write(" ")
            node.value.accept(self)
        self._write_semicolon()
    
    def visit_as_type(self, node: AsType):
        """Visit AssemblyScript type."""
        self._write(node.name)
        
        if node.generic_args:
            self._write("<")
            for i, arg in enumerate(node.generic_args):
                if i > 0:
                    self._write(", ")
                arg.accept(self)
            self._write(">")
        
        if node.is_array:
            self._write("[]")
        
        if node.is_nullable:
            self._write(" | null")
    
    def visit_as_import(self, node: AsImport):
        """Visit AssemblyScript import."""
        self._write("import ")
        
        if node.specifiers:
            if len(node.specifiers) == 1 and not node.specifiers[0].local:
                # Default import
                self._write(node.specifiers[0].imported)
            else:
                # Named imports
                self._write("{ ")
                for i, spec in enumerate(node.specifiers):
                    if i > 0:
                        self._write(", ")
                    
                    self._write(spec.imported)
                    if spec.local and spec.local != spec.imported:
                        self._write(f" as {spec.local}")
                
                self._write(" }")
        
        self._write(f' from "{node.source}"')
        self._write_semicolon()
    
    def visit_as_export(self, node: AsExport):
        """Visit AssemblyScript export."""
        self._write("export ")
        
        if node.export_type == "default":
            self._write("default ")
        
        if node.declaration:
            node.declaration.accept(self)
        elif node.specifiers:
            self._write("{ ")
            for i, spec in enumerate(node.specifiers):
                if i > 0:
                    self._write(", ")
                
                self._write(spec.local)
                if spec.exported and spec.exported != spec.local:
                    self._write(f" as {spec.exported}")
            
            self._write(" }")
            
            if node.source:
                self._write(f' from "{node.source}"')
            
            self._write_semicolon()


# Convenience functions
def generate_assemblyscript_code(ast: Union[AsProgram, AsFunction, AsClass], 
                                style: AssemblyScriptCodeStyle = AssemblyScriptCodeStyle.STANDARD) -> str:
    """Generate AssemblyScript code from AST with specified style."""
    generator = AssemblyScriptCodeGenerator(style)
    return generator.generate(ast)


def format_assemblyscript_code(code: str, 
                              style: AssemblyScriptCodeStyle = AssemblyScriptCodeStyle.STANDARD) -> str:
    """Format existing AssemblyScript code with specified style."""
    try:
        # Parse and regenerate
        from .assemblyscript_parser import parse_assemblyscript
        ast = parse_assemblyscript(code)
        return generate_assemblyscript_code(ast, style)
    except Exception as e:
        # If parsing fails, return original
        logging.getLogger(__name__).warning(f"Failed to format AssemblyScript: {e}")
        return code


def assemblyscript_to_compact_style(code: str) -> str:
    """Convert AssemblyScript to compact style."""
    return format_assemblyscript_code(code, AssemblyScriptCodeStyle.COMPACT)


def assemblyscript_to_pretty_style(code: str) -> str:
    """Convert AssemblyScript to pretty style."""
    return format_assemblyscript_code(code, AssemblyScriptCodeStyle.PRETTY)


def assemblyscript_to_minified_style(code: str) -> str:
    """Convert AssemblyScript to minified style."""
    return format_assemblyscript_code(code, AssemblyScriptCodeStyle.MINIFIED)


def validate_assemblyscript_format(code: str) -> bool:
    """Validate AssemblyScript format."""
    try:
        from .assemblyscript_parser import parse_assemblyscript
        parse_assemblyscript(code)
        return True
    except:
        return False


def create_assemblyscript_function(name: str, 
                                  return_type: str = "void",
                                  params: List[Tuple[str, str]] = None,
                                  body: str = "// TODO: implement") -> str:
    """Create AssemblyScript function template."""
    param_list = []
    if params:
        for param_name, param_type in params:
            param_list.append(f"{param_name}: {param_type}")
    
    params_str = ", ".join(param_list)
    
    template = f"""function {name}({params_str}): {return_type} {{
    {body}
}}"""
    
    return template


def create_assemblyscript_class(name: str,
                               extends: str = None,
                               fields: List[Tuple[str, str]] = None,
                               methods: List[str] = None) -> str:
    """Create AssemblyScript class template."""
    class_parts = [f"class {name}"]
    
    if extends:
        class_parts.append(f" extends {extends}")
    
    class_parts.append(" {\n")
    
    # Add fields
    if fields:
        for field_name, field_type in fields:
            class_parts.append(f"    {field_name}: {field_type};\n")
        class_parts.append("\n")
    
    # Add constructor
    class_parts.append("    constructor() {\n")
    class_parts.append("        // TODO: initialize\n")
    class_parts.append("    }\n")
    
    # Add methods
    if methods:
        class_parts.append("\n")
        for method in methods:
            class_parts.append(f"    {method}\n")
    
    class_parts.append("}")
    
    return "".join(class_parts)


def create_assemblyscript_module_template(name: str) -> str:
    """Create AssemblyScript module template."""
    template = f"""// {name} Module
// AssemblyScript WebAssembly module

export function add(a: i32, b: i32): i32 {{
    return a + b;
}}

export function multiply(a: f64, b: f64): f64 {{
    return a * b;
}}

export class {name} {{
    private value: i32;
    
    constructor(initialValue: i32 = 0) {{
        this.value = initialValue;
    }}
    
    getValue(): i32 {{
        return this.value;
    }}
    
    setValue(newValue: i32): void {{
        this.value = newValue;
    }}
}}

export const VERSION: string = "1.0.0";
"""
    
    return template