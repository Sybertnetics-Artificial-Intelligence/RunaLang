#!/usr/bin/env python3
"""
PHP Code Generator

Generates PHP code from PHP AST nodes with support for multiple code styles.

Author: Sybertnetics AI Solutions
License: MIT
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass
from enum import Enum, auto
import logging

from .php_ast import *


class PhpCodeStyle(Enum):
    """PHP code formatting styles."""
    PSR12 = "psr12"
    SYMFONY = "symfony"
    LARAVEL = "laravel"
    WORDPRESS = "wordpress"
    DRUPAL = "drupal"
    COMPACT = "compact"


@dataclass
class PhpFormattingOptions:
    """PHP code formatting options."""
    indent_size: int = 4
    max_line_length: int = 120
    use_tabs: bool = False
    space_before_brace: bool = True
    space_after_comma: bool = True
    space_around_operators: bool = True
    trailing_comma: bool = False
    
    # PHP-specific
    php_tag_style: str = "<?php"  # <?php or <?
    declare_strict_types: bool = True
    one_class_per_file: bool = True
    namespace_declaration_newlines: int = 2
    use_statement_grouping: bool = True
    method_chaining_indent: int = 4


class PhpFormatter:
    """PHP code formatter with style presets."""
    
    @staticmethod
    def get_style_options(style: PhpCodeStyle) -> PhpFormattingOptions:
        """Get formatting options for a specific style."""
        if style == PhpCodeStyle.PSR12:
            return PhpFormattingOptions(
                indent_size=4,
                max_line_length=120,
                space_before_brace=False,
                trailing_comma=True,
                declare_strict_types=True
            )
        elif style == PhpCodeStyle.SYMFONY:
            return PhpFormattingOptions(
                indent_size=4,
                max_line_length=120,
                space_before_brace=False,
                trailing_comma=True,
                declare_strict_types=True,
                use_statement_grouping=True
            )
        elif style == PhpCodeStyle.LARAVEL:
            return PhpFormattingOptions(
                indent_size=4,
                max_line_length=120,
                space_before_brace=False,
                trailing_comma=True,
                declare_strict_types=false
            )
        elif style == PhpCodeStyle.WORDPRESS:
            return PhpFormattingOptions(
                indent_size=4,
                max_line_length=100,
                space_before_brace=True,
                trailing_comma=False,
                declare_strict_types=False
            )
        elif style == PhpCodeStyle.DRUPAL:
            return PhpFormattingOptions(
                indent_size=2,
                max_line_length=80,
                space_before_brace=True,
                trailing_comma=False,
                declare_strict_types=False
            )
        elif style == PhpCodeStyle.COMPACT:
            return PhpFormattingOptions(
                indent_size=2,
                max_line_length=160,
                space_before_brace=False,
                trailing_comma=False
            )
        else:
            return PhpFormattingOptions()


class PhpCodeGenerator(PhpVisitor):
    """PHP code generator that produces formatted PHP source code from AST."""
    
    def __init__(self, style: PhpCodeStyle = PhpCodeStyle.PSR12):
        self.style = style
        self.options = PhpFormatter.get_style_options(style)
        self.logger = logging.getLogger(__name__)
        
        # Output state
        self.output = []
        self.indent_level = 0
        self.current_line_length = 0
        self.needs_indent = True
    
    def generate(self, node: PhpNode) -> str:
        """Generate PHP code from an AST node."""
        self.output = []
        self.indent_level = 0
        self.current_line_length = 0
        self.needs_indent = True
        
        try:
            node.accept(self)
            result = "".join(self.output)
            return self._post_process(result)
        except Exception as e:
            self.logger.error(f"PHP code generation failed: {e}")
            raise RuntimeError(f"Failed to generate PHP code: {e}")
    
    def _post_process(self, code: str) -> str:
        """Post-process generated code."""
        lines = code.split('\n')
        processed_lines = []
        
        for line in lines:
            processed_lines.append(line)
        
        result = '\n'.join(processed_lines)
        
        if result and not result.endswith('\n'):
            result += '\n'
        
        return result
    
    def _write(self, text: str):
        """Write text to output."""
        if self.needs_indent and text.strip():
            self._write_indent()
            self.needs_indent = False
        
        self.output.append(text)
        self.current_line_length += len(text)
    
    def _write_line(self, text: str = ""):
        """Write a line of text."""
        if text:
            self._write(text)
        self.output.append('\n')
        self.current_line_length = 0
        self.needs_indent = True
    
    def _write_indent(self):
        """Write current indentation."""
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
    
    def _write_space(self):
        """Write a space if needed."""
        if self.output and not self.output[-1].endswith(' '):
            self._write(' ')
    
    def _write_brace_open(self):
        """Write opening brace."""
        if self.options.space_before_brace:
            self._write_space()
        self._write('{')
        self._write_line()
        self._increase_indent()
    
    def _write_brace_close(self):
        """Write closing brace."""
        self._decrease_indent()
        self._write('}')
    
    def _write_separated_list(self, items: List[Any], separator: str = ", ", generate_func=None):
        """Write a separated list."""
        if not items:
            return
        
        if generate_func is None:
            generate_func = lambda item: item.accept(self)
        
        for i, item in enumerate(items):
            if i > 0:
                self._write(separator)
            generate_func(item)
    
    # Visitor methods
    def visit_php_source_file(self, node: PhpSourceFile):
        """Visit source file."""
        # Write PHP opening tag
        self._write_line(self.options.php_tag_style)
        
        # Write declare statement for strict types
        if self.options.declare_strict_types:
            self._write_line("declare(strict_types=1);")
            self._write_line()
        
        # Write namespace declarations
        namespace_written = False
        for decl in node.declarations:
            if isinstance(decl, PhpNamespaceDeclaration):
                if namespace_written:
                    self._write_line()
                decl.accept(self)
                namespace_written = True
        
        if namespace_written:
            for _ in range(self.options.namespace_declaration_newlines):
                self._write_line()
        
        # Write use declarations
        use_declarations = [decl for decl in node.declarations if isinstance(decl, PhpUseDeclaration)]
        if use_declarations:
            for decl in use_declarations:
                decl.accept(self)
                self._write_line()
            self._write_line()
        
        # Write other declarations
        for decl in node.declarations:
            if not isinstance(decl, (PhpNamespaceDeclaration, PhpUseDeclaration)):
                decl.accept(self)
                self._write_line()
                self._write_line()
        
        # Write statements
        for stmt in node.statements:
            stmt.accept(self)
            self._write_line()
    
    def visit_php_namespace_declaration(self, node: PhpNamespaceDeclaration):
        """Visit namespace declaration."""
        self._write('namespace ')
        self._write(node.name)
        
        if node.statements:
            self._write_brace_open()
            for stmt in node.statements:
                stmt.accept(self)
                self._write_line()
            self._write_brace_close()
        else:
            self._write(';')
    
    def visit_php_use_declaration(self, node: PhpUseDeclaration):
        """Visit use declaration."""
        self._write('use ')
        self._write(node.name)
        
        if node.alias:
            self._write(' as ')
            self._write(node.alias)
        
        self._write(';')
    
    def visit_php_class_declaration(self, node: PhpClassDeclaration):
        """Visit class declaration."""
        # Write modifiers
        if node.is_abstract:
            self._write('abstract ')
        if node.is_final:
            self._write('final ')
        if node.is_readonly:
            self._write('readonly ')
        
        self._write('class ')
        self._write(node.name)
        
        # Write inheritance
        if node.extends:
            self._write(' extends ')
            self._write(node.extends)
        
        if node.implements:
            self._write(' implements ')
            self._write_separated_list(node.implements, ', ', lambda x: self._write(x))
        
        # Write body
        self._write_brace_open()
        
        for i, member in enumerate(node.members):
            if i > 0:
                self._write_line()
            
            member.accept(self)
            self._write_line()
        
        self._write_brace_close()
    
    def visit_php_interface_declaration(self, node: PhpInterfaceDeclaration):
        """Visit interface declaration."""
        self._write('interface ')
        self._write(node.name)
        
        if node.extends:
            self._write(' extends ')
            self._write_separated_list(node.extends, ', ', lambda x: self._write(x))
        
        # Write body
        self._write_brace_open()
        
        for i, member in enumerate(node.members):
            if i > 0:
                self._write_line()
            
            member.accept(self)
            self._write_line()
        
        self._write_brace_close()
    
    def visit_php_trait_declaration(self, node: PhpTraitDeclaration):
        """Visit trait declaration."""
        self._write('trait ')
        self._write(node.name)
        
        # Write body
        self._write_brace_open()
        
        for i, member in enumerate(node.members):
            if i > 0:
                self._write_line()
            
            member.accept(self)
            self._write_line()
        
        self._write_brace_close()
    
    def visit_php_enum_declaration(self, node: PhpEnumDeclaration):
        """Visit enum declaration."""
        self._write('enum ')
        self._write(node.name)
        
        if node.backed_type:
            self._write(': ')
            node.backed_type.accept(self)
        
        if node.implements:
            self._write(' implements ')
            self._write_separated_list(node.implements, ', ', lambda x: self._write(x))
        
        # Write body
        self._write_brace_open()
        
        # Write cases
        for case in node.cases:
            self._write('case ')
            self._write(case.name)
            if case.value:
                self._write(' = ')
                case.value.accept(self)
            self._write(';')
            self._write_line()
        
        # Write members
        if node.cases and node.members:
            self._write_line()
        
        for i, member in enumerate(node.members):
            if i > 0:
                self._write_line()
            
            member.accept(self)
            self._write_line()
        
        self._write_brace_close()
    
    def visit_php_function_declaration(self, node: PhpFunctionDeclaration):
        """Visit function declaration."""
        self._write('function ')
        self._write(node.name)
        
        # Write parameters
        self._write('(')
        self._write_separated_list(node.parameters)
        self._write(')')
        
        # Write return type
        if node.return_type:
            self._write(': ')
            node.return_type.accept(self)
        
        # Write body
        if node.body:
            self._write_brace_open()
            node.body.accept(self)
            self._write_brace_close()
    
    def visit_php_method_declaration(self, node: PhpMethodDeclaration):
        """Visit method declaration."""
        # Write visibility and modifiers
        if node.visibility:
            self._write(node.visibility.value)
            self._write_space()
        
        if node.is_static:
            self._write('static ')
        if node.is_abstract:
            self._write('abstract ')
        if node.is_final:
            self._write('final ')
        
        self._write('function ')
        self._write(node.name)
        
        # Write parameters
        self._write('(')
        self._write_separated_list(node.parameters)
        self._write(')')
        
        # Write return type
        if node.return_type:
            self._write(': ')
            node.return_type.accept(self)
        
        # Write body
        if node.body and not node.is_abstract:
            self._write_brace_open()
            node.body.accept(self)
            self._write_brace_close()
        else:
            self._write(';')
    
    def visit_php_property_declaration(self, node: PhpPropertyDeclaration):
        """Visit property declaration."""
        # Write visibility and modifiers
        if node.visibility:
            self._write(node.visibility.value)
            self._write_space()
        
        if node.is_static:
            self._write('static ')
        if node.is_readonly:
            self._write('readonly ')
        
        # Write type hint
        if node.type_hint:
            node.type_hint.accept(self)
            self._write_space()
        
        self._write(f'${node.name}')
        
        # Write default value
        if node.default_value:
            self._write(' = ')
            node.default_value.accept(self)
        
        self._write(';')
    
    def visit_php_variable(self, node: PhpVariable):
        """Visit variable."""
        self._write(node.name)
    
    def visit_php_literal(self, node: PhpLiteral):
        """Visit literal."""
        if node.literal_type == "string":
            # Use double quotes for strings
            escaped_value = str(node.value).replace('\\', '\\\\').replace('"', '\\"')
            self._write(f'"{escaped_value}"')
        elif node.literal_type == "bool":
            self._write('true' if node.value else 'false')
        elif node.literal_type == "null":
            self._write('null')
        else:
            self._write(str(node.value))
    
    def visit_php_identifier(self, node: PhpIdentifier):
        """Visit identifier."""
        self._write(node.name)
    
    def visit_php_block(self, node: PhpBlock):
        """Visit block."""
        for stmt in node.statements:
            stmt.accept(self)
            self._write_line()
    
    def visit_php_expression_statement(self, node: PhpExpressionStatement):
        """Visit expression statement."""
        if node.expression:
            node.expression.accept(self)
        self._write(';')
    
    def visit_php_echo_statement(self, node: PhpEchoStatement):
        """Visit echo statement."""
        self._write('echo ')
        self._write_separated_list(node.expressions)
        self._write(';')
    
    def visit_php_return_statement(self, node: PhpReturnStatement):
        """Visit return statement."""
        self._write('return')
        if node.expression:
            self._write_space()
            node.expression.accept(self)
        self._write(';')
    
    def visit_php_type_declaration(self, node: PhpTypeDeclaration):
        """Visit type declaration."""
        self._write(node.name)
    
    def visit_php_nullable_type(self, node: PhpNullableType):
        """Visit nullable type."""
        self._write('?')
        if node.inner_type:
            node.inner_type.accept(self)
    
    def visit_php_union_type(self, node: PhpUnionType):
        """Visit union type."""
        self._write_separated_list(node.types, '|')
    
    def visit_php_parameter(self, node: PhpParameter):
        """Visit parameter."""
        if node.type_hint:
            node.type_hint.accept(self)
            self._write_space()
        
        if node.is_reference:
            self._write('&')
        
        if node.is_variadic:
            self._write('...')
        
        self._write(node.name)
        
        if node.default_value:
            self._write(' = ')
            node.default_value.accept(self)


# Convenience functions
def generate_php_code(ast: PhpSourceFile, 
                     style: PhpCodeStyle = PhpCodeStyle.PSR12) -> str:
    """Generate PHP code from AST with specified style."""
    generator = PhpCodeGenerator(style)
    return generator.generate(ast)


def format_php_code(code: str, 
                   style: PhpCodeStyle = PhpCodeStyle.PSR12) -> str:
    """Format existing PHP code with specified style."""
    # This would require parsing and re-generating
    # For now, return the original code
    return code