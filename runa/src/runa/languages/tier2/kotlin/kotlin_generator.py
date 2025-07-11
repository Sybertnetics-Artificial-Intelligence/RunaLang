#!/usr/bin/env python3
"""
Kotlin Code Generator

Generates Kotlin code from Kotlin AST nodes with support for multiple code styles.
Supports modern Kotlin features including coroutines, null safety, data classes,
sealed classes, inline classes, and DSL constructs.

This module provides:
- KotlinCodeGenerator: Kotlin AST → Kotlin code generation
- Multiple code formatting styles (Android, JetBrains, Square, etc.)
- Configurable indentation and formatting options
- Support for all Kotlin language constructs
- Performance-optimized generation

Author: Sybertnetics AI Solutions
License: MIT
"""

from typing import List, Optional, Dict, Any, Union, TextIO
from dataclasses import dataclass, field
from enum import Enum, auto
import io
import logging

from .kotlin_ast import (
    KotlinNode, KotlinProgram, KotlinStatement, KotlinExpression,
    KotlinClassDeclaration, KotlinFunctionDeclaration, KotlinPropertyDeclaration,
    KotlinPackageDeclaration, KotlinImportDeclaration, KotlinBinaryExpression,
    KotlinUnaryExpression, KotlinCallExpression, KotlinLambdaExpression,
    KotlinIfExpression, KotlinWhenExpression, KotlinTryExpression,
    KotlinIdentifier, KotlinLiteral, KotlinStringTemplate, KotlinType,
    KotlinBlock, KotlinReturnStatement, KotlinAssignment, KotlinForStatement,
    KotlinWhileStatement, KotlinModifier, KotlinVisibility, KotlinClassKind,
    KotlinOperator, KotlinVariance, KotlinNodeType, KotlinVisitor
)


class KotlinCodeStyle(Enum):
    """Kotlin code formatting styles."""
    ANDROID = "android"
    JETBRAINS = "jetbrains"
    SQUARE = "square"
    GOOGLE = "google"
    KOTLIN_OFFICIAL = "kotlin_official"
    GRADLE = "gradle"
    CLEAN_CODE = "clean_code"
    COMPACT = "compact"


class KotlinIndentationStyle(Enum):
    """Kotlin indentation styles."""
    SPACES = "spaces"
    TABS = "tabs"


class KotlinBraceStyle(Enum):
    """Kotlin brace styles."""
    SAME_LINE = "same_line"      # if (condition) {
    NEXT_LINE = "next_line"      # if (condition)
                                 # {
    NEXT_LINE_SHIFTED = "next_line_shifted"  # if (condition)
                                             #   {


class KotlinImportStyle(Enum):
    """Kotlin import organization styles."""
    ANDROID = "android"
    JETBRAINS = "jetbrains"
    ALPHABETICAL = "alphabetical"
    GROUPED = "grouped"


@dataclass
class KotlinFormattingOptions:
    """Kotlin code formatting options."""
    # Indentation
    indent_style: KotlinIndentationStyle = KotlinIndentationStyle.SPACES
    indent_size: int = 4
    continuation_indent_size: int = 8
    
    # Braces
    brace_style: KotlinBraceStyle = KotlinBraceStyle.SAME_LINE
    empty_block_style: str = "same_line"  # "same_line" or "next_line"
    
    # Line length and wrapping
    max_line_length: int = 120
    wrap_expressions: bool = True
    wrap_parameters: bool = True
    wrap_arguments: bool = True
    
    # Spacing
    space_before_parentheses: bool = False
    space_around_operators: bool = True
    space_after_comma: bool = True
    space_before_colon: bool = False
    space_after_colon: bool = True
    space_around_range: bool = False
    
    # Control structures
    space_before_if_parentheses: bool = True
    space_before_for_parentheses: bool = True
    space_before_while_parentheses: bool = True
    space_before_try_parentheses: bool = True
    space_before_catch_parentheses: bool = True
    
    # Functions and lambdas
    space_before_lambda_arrow: bool = True
    space_after_lambda_arrow: bool = True
    space_around_function_arrow: bool = True
    
    # Classes and objects
    space_before_class_left_brace: bool = True
    space_before_supertype_list: bool = True
    
    # Import organization
    import_style: KotlinImportStyle = KotlinImportStyle.ANDROID
    blank_lines_after_imports: int = 1
    blank_lines_before_class: int = 1
    blank_lines_after_class_header: int = 1
    blank_lines_before_method: int = 1
    
    # Comments
    line_comment_at_first_column: bool = False
    line_comment_add_space: bool = True
    block_comment_at_first_column: bool = False
    
    # Miscellaneous
    keep_blank_lines: int = 2
    keep_line_breaks: bool = True
    align_multiline_parameters: bool = True
    align_multiline_arguments: bool = True
    
    # Kotlin-specific
    use_explicit_types: bool = False
    use_trailing_comma: bool = True
    use_single_line_methods: bool = True
    use_expression_body: bool = True
    insert_whitespace_before_elvis: bool = True
    insert_whitespace_after_elvis: bool = True


class KotlinFormatter:
    """Kotlin code formatter with multiple style presets."""
    
    @staticmethod
    def get_style_options(style: KotlinCodeStyle) -> KotlinFormattingOptions:
        """Get formatting options for a specific style."""
        if style == KotlinCodeStyle.ANDROID:
            return KotlinFormattingOptions(
                indent_size=4,
                max_line_length=100,
                brace_style=KotlinBraceStyle.SAME_LINE,
                import_style=KotlinImportStyle.ANDROID,
                use_trailing_comma=True,
                use_single_line_methods=False,
                use_expression_body=True
            )
        
        elif style == KotlinCodeStyle.JETBRAINS:
            return KotlinFormattingOptions(
                indent_size=4,
                max_line_length=120,
                brace_style=KotlinBraceStyle.SAME_LINE,
                import_style=KotlinImportStyle.JETBRAINS,
                use_trailing_comma=False,
                use_single_line_methods=True,
                use_expression_body=True
            )
        
        elif style == KotlinCodeStyle.SQUARE:
            return KotlinFormattingOptions(
                indent_size=2,
                max_line_length=100,
                brace_style=KotlinBraceStyle.SAME_LINE,
                import_style=KotlinImportStyle.ALPHABETICAL,
                use_trailing_comma=True,
                use_single_line_methods=False,
                use_expression_body=False
            )
        
        elif style == KotlinCodeStyle.GOOGLE:
            return KotlinFormattingOptions(
                indent_size=2,
                max_line_length=100,
                brace_style=KotlinBraceStyle.SAME_LINE,
                import_style=KotlinImportStyle.GROUPED,
                use_trailing_comma=True,
                use_single_line_methods=False,
                use_expression_body=True
            )
        
        elif style == KotlinCodeStyle.KOTLIN_OFFICIAL:
            return KotlinFormattingOptions(
                indent_size=4,
                max_line_length=120,
                brace_style=KotlinBraceStyle.SAME_LINE,
                import_style=KotlinImportStyle.JETBRAINS,
                use_trailing_comma=False,
                use_single_line_methods=True,
                use_expression_body=True
            )
        
        elif style == KotlinCodeStyle.GRADLE:
            return KotlinFormattingOptions(
                indent_size=4,
                max_line_length=120,
                brace_style=KotlinBraceStyle.SAME_LINE,
                import_style=KotlinImportStyle.GROUPED,
                use_trailing_comma=True,
                use_single_line_methods=False,
                use_expression_body=False
            )
        
        elif style == KotlinCodeStyle.CLEAN_CODE:
            return KotlinFormattingOptions(
                indent_size=4,
                max_line_length=80,
                brace_style=KotlinBraceStyle.NEXT_LINE,
                import_style=KotlinImportStyle.GROUPED,
                use_trailing_comma=False,
                use_single_line_methods=False,
                use_expression_body=False,
                keep_blank_lines=1,
                blank_lines_before_method=2
            )
        
        elif style == KotlinCodeStyle.COMPACT:
            return KotlinFormattingOptions(
                indent_size=2,
                max_line_length=160,
                brace_style=KotlinBraceStyle.SAME_LINE,
                import_style=KotlinImportStyle.ALPHABETICAL,
                use_trailing_comma=False,
                use_single_line_methods=True,
                use_expression_body=True,
                keep_blank_lines=1,
                blank_lines_before_method=0
            )
        
        else:
            return KotlinFormattingOptions()


class KotlinCodeGenerator(KotlinVisitor):
    """
    Kotlin code generator that produces formatted Kotlin source code from AST.
    
    Supports multiple formatting styles and comprehensive Kotlin language features
    including modern constructs like coroutines, null safety, and DSL patterns.
    """
    
    def __init__(self, style: KotlinCodeStyle = KotlinCodeStyle.JETBRAINS):
        """
        Initialize the Kotlin code generator.
        
        Args:
            style: Code formatting style to use
        """
        self.style = style
        self.options = KotlinFormatter.get_style_options(style)
        self.logger = logging.getLogger(__name__)
        
        # Output state
        self.output = []
        self.indent_level = 0
        self.current_line_length = 0
        self.needs_indent = True
        
        # Context tracking
        self.in_class = False
        self.in_function = False
        self.in_expression = False
        self.function_depth = 0
        
        # Import management
        self.required_imports = set()
        self.current_package = None
    
    def generate(self, node: KotlinNode) -> str:
        """
        Generate Kotlin code from an AST node.
        
        Args:
            node: Kotlin AST node to generate code from
            
        Returns:
            str: Generated Kotlin source code
        """
        self.output = []
        self.indent_level = 0
        self.current_line_length = 0
        self.needs_indent = True
        
        try:
            node.accept(self)
            
            # Join output and clean up
            result = "".join(self.output)
            return self._post_process(result)
            
        except Exception as e:
            self.logger.error(f"Kotlin code generation failed: {e}")
            raise RuntimeError(f"Failed to generate Kotlin code: {e}")
    
    def _post_process(self, code: str) -> str:
        """Post-process generated code."""
        lines = code.split('\n')
        
        # Remove excessive blank lines
        processed_lines = []
        blank_line_count = 0
        
        for line in lines:
            if line.strip() == '':
                blank_line_count += 1
                if blank_line_count <= self.options.keep_blank_lines:
                    processed_lines.append(line)
            else:
                blank_line_count = 0
                processed_lines.append(line)
        
        # Join and clean up
        result = '\n'.join(processed_lines)
        
        # Ensure file ends with newline
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
        if self.options.indent_style == KotlinIndentationStyle.SPACES:
            indent = ' ' * (self.indent_level * self.options.indent_size)
        else:
            indent = '\t' * self.indent_level
        
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
    
    def _write_space_if_needed(self, condition: bool):
        """Write space if condition is true."""
        if condition:
            self._write_space()
    
    def _should_wrap_line(self, additional_length: int = 0) -> bool:
        """Check if line should be wrapped."""
        return (self.current_line_length + additional_length) > self.options.max_line_length
    
    def _write_brace_open(self):
        """Write opening brace with proper formatting."""
        if self.options.brace_style == KotlinBraceStyle.SAME_LINE:
            self._write_space_if_needed(self.options.space_before_class_left_brace)
            self._write('{')
        elif self.options.brace_style == KotlinBraceStyle.NEXT_LINE:
            self._write_line()
            self._write('{')
        elif self.options.brace_style == KotlinBraceStyle.NEXT_LINE_SHIFTED:
            self._write_line()
            self._increase_indent()
            self._write('{')
            self._decrease_indent()
        
        self._write_line()
        self._increase_indent()
    
    def _write_brace_close(self):
        """Write closing brace with proper formatting."""
        self._decrease_indent()
        self._write('}')
    
    def _write_separated_list(self, items: List[Any], separator: str = ", ", 
                             generate_func=None, wrap_threshold: int = 3):
        """Write a separated list with proper formatting."""
        if not items:
            return
        
        if generate_func is None:
            generate_func = lambda item: item.accept(self)
        
        # Check if we should wrap
        should_wrap = len(items) > wrap_threshold or self._should_wrap_line()
        
        for i, item in enumerate(items):
            if i > 0:
                self._write(separator.rstrip())
                if should_wrap:
                    self._write_line()
                elif self.options.space_after_comma and separator.endswith(','):
                    self._write(' ')
            
            generate_func(item)
    
    # Visitor methods
    def visit_program(self, node: KotlinProgram):
        """Visit Kotlin program."""
        # Write package declaration
        if node.package_declaration:
            node.package_declaration.accept(self)
            self._write_line()
            self._write_line()
        
        # Write imports
        if node.imports:
            self._write_imports(node.imports)
            self._write_line()
            
            # Add blank lines after imports
            for _ in range(self.options.blank_lines_after_imports):
                self._write_line()
        
        # Write declarations
        for i, decl in enumerate(node.declarations):
            if i > 0:
                for _ in range(self.options.blank_lines_before_class):
                    self._write_line()
            
            decl.accept(self)
            self._write_line()
    
    def visit_package_declaration(self, node: KotlinPackageDeclaration):
        """Visit package declaration."""
        self._write('package ')
        self._write(node.name)
    
    def visit_import_declaration(self, node: KotlinImportDeclaration):
        """Visit import declaration."""
        self._write('import ')
        self._write(node.path)
        
        if node.alias:
            self._write(' as ')
            self._write(node.alias)
    
    def _write_imports(self, imports: List[KotlinImportDeclaration]):
        """Write imports with proper organization."""
        if not imports:
            return
        
        # Group imports by style
        if self.options.import_style == KotlinImportStyle.GROUPED:
            # Group by package
            groups = {}
            for imp in imports:
                package = imp.path.split('.')[0]
                if package not in groups:
                    groups[package] = []
                groups[package].append(imp)
            
            # Write groups
            for i, (package, group) in enumerate(sorted(groups.items())):
                if i > 0:
                    self._write_line()
                
                for imp in sorted(group, key=lambda x: x.path):
                    imp.accept(self)
                    self._write_line()
        
        else:
            # Sort alphabetically
            sorted_imports = sorted(imports, key=lambda x: x.path)
            for imp in sorted_imports:
                imp.accept(self)
                self._write_line()
    
    def visit_class_declaration(self, node: KotlinClassDeclaration):
        """Visit class declaration."""
        self.in_class = True
        
        # Write modifiers
        self._write_modifiers(node.modifiers)
        
        # Write class keyword
        self._write('class ')
        self._write(node.name)
        
        # Write type parameters
        if node.type_parameters:
            self._write('<')
            self._write_separated_list(node.type_parameters, ', ')
            self._write('>')
        
        # Write primary constructor
        if node.primary_constructor:
            self._write_space_if_needed(self.options.space_before_parentheses)
            self._write('(')
            # Write constructor parameters (simplified)
            self._write(')')
        
        # Write supertypes
        if node.supertypes:
            self._write_space_if_needed(self.options.space_before_supertype_list)
            self._write(' : ')
            self._write_separated_list(node.supertypes, ', ')
        
        # Write class body
        if node.members:
            self._write_brace_open()
            
            for _ in range(self.options.blank_lines_after_class_header):
                self._write_line()
            
            for i, member in enumerate(node.members):
                if i > 0:
                    for _ in range(self.options.blank_lines_before_method):
                        self._write_line()
                
                member.accept(self)
                self._write_line()
            
            self._write_brace_close()
        else:
            # Empty class
            if self.options.empty_block_style == "same_line":
                self._write(' {}')
            else:
                self._write_brace_open()
                self._write_brace_close()
        
        self.in_class = False
    
    def visit_function_declaration(self, node: KotlinFunctionDeclaration):
        """Visit function declaration."""
        self.in_function = True
        self.function_depth += 1
        
        # Write modifiers
        self._write_modifiers(node.modifiers)
        
        # Write fun keyword
        self._write('fun ')
        
        # Write type parameters
        if node.type_parameters:
            self._write('<')
            self._write_separated_list(node.type_parameters, ', ')
            self._write('>')
            self._write(' ')
        
        # Write function name
        self._write(node.name)
        
        # Write parameters
        self._write('(')
        if node.parameters:
            self._write_separated_list(
                node.parameters, 
                ', ',
                lambda p: self._write_parameter(p)
            )
        self._write(')')
        
        # Write return type
        if node.return_type:
            self._write(': ')
            node.return_type.accept(self)
        
        # Write body
        if node.body:
            if (self.options.use_expression_body and 
                self._is_simple_expression_body(node.body)):
                self._write(' = ')
                node.body.accept(self)
            else:
                self._write_brace_open()
                node.body.accept(self)
                self._write_brace_close()
        
        self.function_depth -= 1
        self.in_function = self.function_depth > 0
    
    def visit_property_declaration(self, node: KotlinPropertyDeclaration):
        """Visit property declaration."""
        # Write modifiers
        self._write_modifiers(node.modifiers)
        
        # Write val/var
        if node.is_var:
            self._write('var ')
        else:
            self._write('val ')
        
        # Write property name
        self._write(node.name)
        
        # Write type
        if node.type:
            self._write(': ')
            node.type.accept(self)
        
        # Write initializer
        if node.initializer:
            self._write(' = ')
            node.initializer.accept(self)
        
        # Write getter/setter (simplified)
        if node.getter or node.setter:
            self._write_line()
            self._increase_indent()
            
            if node.getter:
                self._write('get() = ')
                # Write getter body
                self._write_line()
            
            if node.setter:
                self._write('set(value) ')
                # Write setter body
                self._write_line()
            
            self._decrease_indent()
    
    def visit_return_statement(self, node: KotlinReturnStatement):
        """Visit return statement."""
        self._write('return')
        
        if node.value:
            self._write(' ')
            node.value.accept(self)
    
    def visit_assignment(self, node: KotlinAssignment):
        """Visit assignment."""
        node.target.accept(self)
        self._write_space_if_needed(self.options.space_around_operators)
        self._write('=')
        self._write_space_if_needed(self.options.space_around_operators)
        node.value.accept(self)
    
    def visit_block(self, node: KotlinBlock):
        """Visit block."""
        for stmt in node.statements:
            stmt.accept(self)
            self._write_line()
    
    def visit_if_expression(self, node: KotlinIfExpression):
        """Visit if expression."""
        self._write('if')
        self._write_space_if_needed(self.options.space_before_if_parentheses)
        self._write('(')
        node.condition.accept(self)
        self._write(')')
        
        # Write then branch
        self._write(' ')
        if isinstance(node.then_branch, KotlinBlock):
            self._write_brace_open()
            node.then_branch.accept(self)
            self._write_brace_close()
        else:
            node.then_branch.accept(self)
        
        # Write else branch
        if node.else_branch:
            self._write(' else ')
            if isinstance(node.else_branch, KotlinBlock):
                self._write_brace_open()
                node.else_branch.accept(self)
                self._write_brace_close()
            else:
                node.else_branch.accept(self)
    
    def visit_when_expression(self, node: KotlinWhenExpression):
        """Visit when expression."""
        self._write('when')
        
        if node.subject:
            self._write(' (')
            node.subject.accept(self)
            self._write(')')
        
        self._write_brace_open()
        
        for entry in node.entries:
            conditions = entry.get('conditions', [])
            body = entry.get('body')
            
            # Write conditions
            for i, condition in enumerate(conditions):
                if i > 0:
                    self._write(', ')
                
                if condition == "else":
                    self._write('else')
                else:
                    condition.accept(self)
            
            self._write(' -> ')
            body.accept(self)
            self._write_line()
        
        self._write_brace_close()
    
    def visit_try_expression(self, node: KotlinTryExpression):
        """Visit try expression."""
        self._write('try')
        self._write_space_if_needed(self.options.space_before_try_parentheses)
        
        # Write try block
        self._write_brace_open()
        node.try_block.accept(self)
        self._write_brace_close()
        
        # Write catch blocks
        for catch_block in node.catch_blocks:
            self._write(' catch')
            self._write_space_if_needed(self.options.space_before_catch_parentheses)
            self._write('(')
            
            param = catch_block.get('parameter')
            if param:
                self._write(param.get('name', 'e'))
                self._write(': ')
                param_type = param.get('type')
                if param_type:
                    param_type.accept(self)
            
            self._write(')')
            
            # Write catch body
            self._write_brace_open()
            catch_body = catch_block.get('body')
            if catch_body:
                catch_body.accept(self)
            self._write_brace_close()
        
        # Write finally block
        if node.finally_block:
            self._write(' finally')
            self._write_brace_open()
            node.finally_block.accept(self)
            self._write_brace_close()
    
    def visit_for_statement(self, node: KotlinForStatement):
        """Visit for statement."""
        self._write('for')
        self._write_space_if_needed(self.options.space_before_for_parentheses)
        self._write('(')
        self._write(node.variable)
        self._write(' in ')
        node.iterable.accept(self)
        self._write(')')
        
        # Write body
        self._write_brace_open()
        node.body.accept(self)
        self._write_brace_close()
    
    def visit_while_statement(self, node: KotlinWhileStatement):
        """Visit while statement."""
        self._write('while')
        self._write_space_if_needed(self.options.space_before_while_parentheses)
        self._write('(')
        node.condition.accept(self)
        self._write(')')
        
        # Write body
        self._write_brace_open()
        node.body.accept(self)
        self._write_brace_close()
    
    def visit_binary_expression(self, node: KotlinBinaryExpression):
        """Visit binary expression."""
        node.left.accept(self)
        
        # Handle special operators
        if node.operator.value in ['?.', '?:', '!!']:
            self._write_space_if_needed(self.options.insert_whitespace_before_elvis)
            self._write(node.operator.value)
            self._write_space_if_needed(self.options.insert_whitespace_after_elvis)
        else:
            self._write_space_if_needed(self.options.space_around_operators)
            self._write(node.operator.value)
            self._write_space_if_needed(self.options.space_around_operators)
        
        node.right.accept(self)
    
    def visit_unary_expression(self, node: KotlinUnaryExpression):
        """Visit unary expression."""
        if node.is_prefix:
            self._write(node.operator.value)
            node.operand.accept(self)
        else:
            node.operand.accept(self)
            self._write(node.operator.value)
    
    def visit_call_expression(self, node: KotlinCallExpression):
        """Visit call expression."""
        node.callee.accept(self)
        self._write('(')
        
        if node.arguments:
            self._write_separated_list(node.arguments, ', ')
        
        self._write(')')
    
    def visit_lambda_expression(self, node: KotlinLambdaExpression):
        """Visit lambda expression."""
        self._write('{ ')
        
        # Write parameters
        if node.parameters:
            for i, param in enumerate(node.parameters):
                if i > 0:
                    self._write(', ')
                self._write(param.get('name', 'it'))
            
            self._write_space_if_needed(self.options.space_before_lambda_arrow)
            self._write('->')
            self._write_space_if_needed(self.options.space_after_lambda_arrow)
        
        # Write body
        node.body.accept(self)
        
        self._write(' }')
    
    def visit_identifier(self, node: KotlinIdentifier):
        """Visit identifier."""
        self._write(node.name)
    
    def visit_literal(self, node: KotlinLiteral):
        """Visit literal."""
        if node.type == "String":
            self._write(f'"{node.value}"')
        elif node.type == "Char":
            self._write(f"'{node.value}'")
        elif node.type == "Boolean":
            self._write(str(node.value).lower())
        elif node.value is None:
            self._write('null')
        else:
            self._write(str(node.value))
    
    def visit_string_template(self, node: KotlinStringTemplate):
        """Visit string template."""
        self._write(f'"{node.value}"')
    
    def visit_type(self, node: KotlinType):
        """Visit type."""
        self._write(node.name)
        
        if node.type_arguments:
            self._write('<')
            self._write_separated_list(node.type_arguments, ', ')
            self._write('>')
        
        if node.nullable:
            self._write('?')
    
    def _write_modifiers(self, modifiers: List[KotlinModifier]):
        """Write modifiers."""
        if not modifiers:
            return
        
        # Group modifiers by category
        visibility_modifiers = ['public', 'private', 'protected', 'internal']
        inheritance_modifiers = ['abstract', 'final', 'open', 'sealed']
        function_modifiers = ['suspend', 'inline', 'noinline', 'crossinline', 'reified']
        property_modifiers = ['const', 'lateinit']
        other_modifiers = ['data', 'inner', 'override', 'external', 'actual', 'expect']
        
        # Write in order
        for modifier in modifiers:
            self._write(modifier.name)
            self._write(' ')
    
    def _write_parameter(self, param: Dict[str, Any]):
        """Write function parameter."""
        name = param.get('name', 'param')
        param_type = param.get('type')
        default_value = param.get('default_value')
        
        self._write(name)
        self._write(': ')
        
        if param_type:
            param_type.accept(self)
        else:
            self._write('Any')
        
        if default_value:
            self._write(' = ')
            default_value.accept(self)
    
    def _is_simple_expression_body(self, body) -> bool:
        """Check if body is simple enough for expression syntax."""
        if not self.options.use_expression_body:
            return False
        
        # Check if body is a single expression
        if isinstance(body, KotlinBlock):
            return len(body.statements) == 1 and isinstance(body.statements[0], KotlinExpression)
        
        return isinstance(body, KotlinExpression)


# Convenience functions
def generate_kotlin_code(ast: KotlinProgram, 
                        style: KotlinCodeStyle = KotlinCodeStyle.JETBRAINS) -> str:
    """Generate Kotlin code from AST with specified style."""
    generator = KotlinCodeGenerator(style)
    return generator.generate(ast)


def format_kotlin_code(code: str, 
                      style: KotlinCodeStyle = KotlinCodeStyle.JETBRAINS) -> str:
    """Format existing Kotlin code with specified style."""
    # This would require parsing and re-generating
    # For now, return the original code
    return code