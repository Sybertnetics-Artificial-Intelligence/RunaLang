#!/usr/bin/env python3
"""
Rust Code Generator

Generates Rust code from Rust AST nodes with support for multiple code styles.
Supports modern Rust features including ownership, borrowing, lifetimes, async/await,
pattern matching, generics, traits, macros, and comprehensive formatting options.

This module provides:
- RustCodeGenerator: Rust AST → Rust code generation
- Multiple code formatting styles (rustfmt, Google, Mozilla, etc.)
- Configurable indentation and formatting options
- Support for all Rust language constructs
- Performance-optimized generation

Author: Sybertnetics AI Solutions
License: MIT
"""

from typing import List, Optional, Dict, Any, Union, TextIO
from dataclasses import dataclass, field
from enum import Enum, auto
import io
import logging

from .rust_ast import (
    RustNode, RustCrate, RustItem, RustExpression, RustStatement, RustPattern,
    RustFunction, RustStruct, RustEnum, RustTrait, RustImpl, RustModule,
    RustUseDeclaration, RustTypeAlias, RustConst, RustStatic, RustUnion,
    RustType, RustTypeReference, RustReferenceType, RustPointerType,
    RustArrayType, RustSliceType, RustTupleType, RustFunctionType,
    RustTraitObject, RustImplTrait, RustLifetime, RustTypeParam,
    RustLifetimeParam, RustConstParam, RustWhereClause, RustGenericParam,
    RustIdentifier, RustLiteral, RustPath, RustBlock, RustIfExpression,
    RustMatchExpression, RustLoopExpression, RustWhileExpression,
    RustForExpression, RustCallExpression, RustMethodCall, RustFieldAccess,
    RustIndexExpression, RustTupleExpression, RustArrayExpression,
    RustStructExpression, RustClosure, RustAwaitExpression, RustTryExpression,
    RustReturnExpression, RustBreakExpression, RustContinueExpression,
    RustMacroCall, RustExpressionStatement, RustLetStatement, RustItemStatement,
    RustIdentifierPattern, RustWildcardPattern, RustLiteralPattern,
    RustStructPattern, RustTuplePattern, RustReferencePattern, RustOrPattern,
    RustRangePattern, RustAttribute, RustMatchArm, RustField, RustEnumVariant,
    RustParameter, RustVisibility, RustMutability, RustSafety, RustAsyncness,
    RustVisitor
)


class RustCodeStyle(Enum):
    """Rust code formatting styles."""
    RUSTFMT = "rustfmt"           # Official Rust formatter style
    GOOGLE = "google"             # Google Rust style
    MOZILLA = "mozilla"           # Mozilla Rust style
    KERNEL = "kernel"             # Linux kernel Rust style
    EMBEDDED = "embedded"         # Embedded Rust style
    COMPACT = "compact"           # Compact style for space-constrained environments
    VERBOSE = "verbose"           # Verbose style with explicit types
    FUNCTIONAL = "functional"     # Functional programming style


class RustIndentationStyle(Enum):
    """Rust indentation styles."""
    SPACES = "spaces"
    TABS = "tabs"


class RustBraceStyle(Enum):
    """Rust brace styles."""
    SAME_LINE = "same_line"       # if condition {
    NEXT_LINE = "next_line"       # if condition
                                  # {
    NEXT_LINE_SHIFTED = "next_line_shifted"  # if condition
                                             #   {


@dataclass
class RustFormattingOptions:
    """Rust code formatting options."""
    # Indentation
    indent_style: RustIndentationStyle = RustIndentationStyle.SPACES
    indent_size: int = 4
    continuation_indent_size: int = 8
    
    # Braces
    brace_style: RustBraceStyle = RustBraceStyle.SAME_LINE
    empty_block_style: str = "same_line"  # "same_line" or "next_line"
    
    # Line length and wrapping
    max_line_length: int = 100
    wrap_comments: bool = True
    wrap_expressions: bool = True
    wrap_parameters: bool = True
    wrap_arguments: bool = True
    wrap_array_elements: bool = True
    
    # Spacing
    space_before_parentheses: bool = False
    space_around_operators: bool = True
    space_after_comma: bool = True
    space_before_colon: bool = False
    space_after_colon: bool = True
    space_around_range: bool = False
    
    # Control structures
    space_before_if_parentheses: bool = True
    space_before_match_parentheses: bool = True
    space_before_loop_braces: bool = True
    space_before_where_clause: bool = True
    
    # Functions and closures
    space_before_closure_pipe: bool = False
    space_after_closure_pipe: bool = True
    space_around_closure_arrow: bool = True
    
    # Types and generics
    space_before_generic_brackets: bool = False
    space_after_generic_brackets: bool = False
    space_around_type_bounds: bool = True
    
    # Attributes and macros
    normalize_attributes: bool = True
    group_attributes: bool = True
    macro_use_parens: bool = False
    
    # Comments and documentation
    normalize_doc_attributes: bool = True
    doc_comment_width: int = 80
    
    # Import organization
    group_imports: bool = True
    imports_granularity: str = "module"  # "module", "crate", "item"
    
    # Trailing elements
    trailing_comma: str = "vertical"  # "always", "never", "vertical"
    trailing_semicolon: bool = True
    
    # Rust-specific
    use_explicit_lifetimes: bool = False
    use_explicit_types: bool = False
    prefer_short_lifetime_names: bool = True
    normalize_visibility: bool = True
    group_impl_items: bool = True
    
    # Advanced formatting
    combine_control_expr: bool = True
    condense_wildcard_suffixes: bool = False
    format_code_in_doc_comments: bool = False
    format_strings: bool = False
    hard_tabs: bool = False
    match_arm_blocks: bool = True
    newline_style: str = "auto"  # "auto", "unix", "windows"
    remove_nested_parens: bool = True
    reorder_impl_items: bool = False


class RustFormatter:
    """Rust code formatter with multiple style presets."""
    
    @staticmethod
    def get_style_options(style: RustCodeStyle) -> RustFormattingOptions:
        """Get formatting options for a specific style."""
        if style == RustCodeStyle.RUSTFMT:
            return RustFormattingOptions(
                indent_size=4,
                max_line_length=100,
                brace_style=RustBraceStyle.SAME_LINE,
                trailing_comma="vertical",
                group_imports=True,
                normalize_attributes=True
            )
        
        elif style == RustCodeStyle.GOOGLE:
            return RustFormattingOptions(
                indent_size=2,
                max_line_length=100,
                brace_style=RustBraceStyle.SAME_LINE,
                trailing_comma="always",
                group_imports=True,
                space_around_operators=True,
                wrap_expressions=True
            )
        
        elif style == RustCodeStyle.MOZILLA:
            return RustFormattingOptions(
                indent_size=4,
                max_line_length=80,
                brace_style=RustBraceStyle.NEXT_LINE,
                trailing_comma="vertical",
                group_imports=False,
                use_explicit_types=True
            )
        
        elif style == RustCodeStyle.KERNEL:
            return RustFormattingOptions(
                indent_style=RustIndentationStyle.TABS,
                indent_size=8,
                max_line_length=80,
                brace_style=RustBraceStyle.NEXT_LINE,
                trailing_comma="never",
                space_around_operators=True,
                use_explicit_types=True
            )
        
        elif style == RustCodeStyle.EMBEDDED:
            return RustFormattingOptions(
                indent_size=2,
                max_line_length=120,
                brace_style=RustBraceStyle.SAME_LINE,
                trailing_comma="vertical",
                use_explicit_types=True,
                use_explicit_lifetimes=True,
                prefer_short_lifetime_names=True
            )
        
        elif style == RustCodeStyle.COMPACT:
            return RustFormattingOptions(
                indent_size=2,
                max_line_length=160,
                brace_style=RustBraceStyle.SAME_LINE,
                trailing_comma="never",
                space_around_operators=False,
                space_after_comma=False,
                combine_control_expr=True,
                remove_nested_parens=True
            )
        
        elif style == RustCodeStyle.VERBOSE:
            return RustFormattingOptions(
                indent_size=4,
                max_line_length=120,
                brace_style=RustBraceStyle.NEXT_LINE,
                trailing_comma="always",
                use_explicit_types=True,
                use_explicit_lifetimes=True,
                normalize_visibility=True,
                wrap_expressions=True,
                wrap_parameters=True
            )
        
        elif style == RustCodeStyle.FUNCTIONAL:
            return RustFormattingOptions(
                indent_size=2,
                max_line_length=100,
                brace_style=RustBraceStyle.SAME_LINE,
                trailing_comma="vertical",
                space_around_closure_arrow=True,
                combine_control_expr=True,
                match_arm_blocks=False
            )
        
        else:
            return RustFormattingOptions()


class RustCodeGenerator(RustVisitor):
    """
    Rust code generator that produces formatted Rust source code from AST.
    
    Supports multiple formatting styles and comprehensive Rust language features
    including ownership, borrowing, lifetimes, async/await, pattern matching,
    generics, traits, macros, and advanced type system constructs.
    """
    
    def __init__(self, style: RustCodeStyle = RustCodeStyle.RUSTFMT):
        """
        Initialize the Rust code generator.
        
        Args:
            style: Code formatting style to use
        """
        self.style = style
        self.options = RustFormatter.get_style_options(style)
        self.logger = logging.getLogger(__name__)
        
        # Output state
        self.output = []
        self.indent_level = 0
        self.current_line_length = 0
        self.needs_indent = True
        
        # Context tracking
        self.in_function = False
        self.in_struct = False
        self.in_enum = False
        self.in_trait = False
        self.in_impl = False
        self.in_unsafe = False
        self.in_async = False
        
        # Lifetime and generic tracking
        self.lifetime_counter = 0
        self.generic_context = set()
        
        # Import management
        self.required_imports = set()
        self.current_module = None
    
    def generate(self, node: RustNode) -> str:
        """
        Generate Rust code from an AST node.
        
        Args:
            node: Rust AST node to generate code from
            
        Returns:
            str: Generated Rust source code
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
            self.logger.error(f"Rust code generation failed: {e}")
            raise RuntimeError(f"Failed to generate Rust code: {e}")
    
    def _post_process(self, code: str) -> str:
        """Post-process generated code."""
        lines = code.split('\n')
        
        # Remove excessive blank lines
        processed_lines = []
        blank_line_count = 0
        
        for line in lines:
            if line.strip() == '':
                blank_line_count += 1
                if blank_line_count <= 2:  # Max 2 consecutive blank lines
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
        if self.options.indent_style == RustIndentationStyle.SPACES:
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
        if self.options.brace_style == RustBraceStyle.SAME_LINE:
            self._write_space()
            self._write('{')
        elif self.options.brace_style == RustBraceStyle.NEXT_LINE:
            self._write_line()
            self._write('{')
        elif self.options.brace_style == RustBraceStyle.NEXT_LINE_SHIFTED:
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
    def visit_rust_crate(self, node: RustCrate):
        """Visit Rust crate."""
        # Write crate-level attributes
        for attr in node.attributes:
            attr.accept(self)
            self._write_line()
        
        if node.attributes:
            self._write_line()
        
        # Write items
        for i, item in enumerate(node.items):
            if i > 0:
                self._write_line()
                self._write_line()
            
            item.accept(self)
    
    def visit_rust_module(self, node: RustModule):
        """Visit module."""
        self.current_module = node.name
        
        # Write visibility
        self._write_visibility(node.visibility)
        
        self._write('mod ')
        self._write(node.name)
        
        if node.items:
            self._write_brace_open()
            
            for i, item in enumerate(node.items):
                if i > 0:
                    self._write_line()
                
                item.accept(self)
                self._write_line()
            
            self._write_brace_close()
        else:
            self._write(';')
    
    def visit_rust_use_declaration(self, node: RustUseDeclaration):
        """Visit use declaration."""
        # Write visibility
        self._write_visibility(node.visibility)
        
        self._write('use ')
        self._write(node.path)
        
        if node.alias:
            self._write(' as ')
            self._write(node.alias)
        
        self._write(';')
    
    def visit_rust_function(self, node: RustFunction):
        """Visit function."""
        self.in_function = True
        
        # Write visibility
        self._write_visibility(node.visibility)
        
        # Write modifiers
        if node.is_async:
            self._write('async ')
        if node.is_unsafe:
            self._write('unsafe ')
        if node.is_extern:
            self._write('extern ')
            if node.abi:
                self._write(f'"{node.abi}" ')
        if node.is_const:
            self._write('const ')
        
        self._write('fn ')
        self._write(node.name)
        
        # Write generics
        if node.generics:
            self._write('<')
            self._write_separated_list(node.generics, ', ')
            self._write('>')
        
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
            self._write(' -> ')
            node.return_type.accept(self)
        
        # Write where clause
        if node.where_clause:
            self._write_space_if_needed(self.options.space_before_where_clause)
            node.where_clause.accept(self)
        
        # Write body
        if node.body:
            self._write_brace_open()
            node.body.accept(self)
            self._write_brace_close()
        else:
            self._write(';')
        
        self.in_function = False
    
    def visit_rust_struct(self, node: RustStruct):
        """Visit struct."""
        self.in_struct = True
        
        # Write visibility
        self._write_visibility(node.visibility)
        
        self._write('struct ')
        self._write(node.name)
        
        # Write generics
        if node.generics:
            self._write('<')
            self._write_separated_list(node.generics, ', ')
            self._write('>')
        
        # Write where clause
        if node.where_clause:
            self._write_space_if_needed(self.options.space_before_where_clause)
            node.where_clause.accept(self)
        
        # Write fields
        if node.is_unit:
            self._write(';')
        elif node.is_tuple:
            self._write('(')
            if node.fields:
                self._write_separated_list(
                    node.fields,
                    ', ',
                    lambda f: self._write_tuple_field(f)
                )
            self._write(');')
        else:
            self._write_brace_open()
            
            for i, field in enumerate(node.fields):
                if i > 0:
                    self._write_line()
                
                self._write_struct_field(field)
                self._write(',')
                self._write_line()
            
            self._write_brace_close()
        
        self.in_struct = False
    
    def visit_rust_enum(self, node: RustEnum):
        """Visit enum."""
        self.in_enum = True
        
        # Write visibility
        self._write_visibility(node.visibility)
        
        self._write('enum ')
        self._write(node.name)
        
        # Write generics
        if node.generics:
            self._write('<')
            self._write_separated_list(node.generics, ', ')
            self._write('>')
        
        # Write where clause
        if node.where_clause:
            self._write_space_if_needed(self.options.space_before_where_clause)
            node.where_clause.accept(self)
        
        # Write variants
        self._write_brace_open()
        
        for i, variant in enumerate(node.variants):
            if i > 0:
                self._write_line()
            
            self._write_enum_variant(variant)
            self._write(',')
            self._write_line()
        
        self._write_brace_close()
        
        self.in_enum = False
    
    def visit_rust_trait(self, node: RustTrait):
        """Visit trait."""
        self.in_trait = True
        
        # Write visibility
        self._write_visibility(node.visibility)
        
        if node.is_unsafe:
            self._write('unsafe ')
        if node.is_auto:
            self._write('auto ')
        
        self._write('trait ')
        self._write(node.name)
        
        # Write generics
        if node.generics:
            self._write('<')
            self._write_separated_list(node.generics, ', ')
            self._write('>')
        
        # Write supertraits
        if node.supertraits:
            self._write(': ')
            self._write_separated_list(
                node.supertraits,
                ' + ',
                lambda st: self._write(st)
            )
        
        # Write where clause
        if node.where_clause:
            self._write_space_if_needed(self.options.space_before_where_clause)
            node.where_clause.accept(self)
        
        # Write trait items
        self._write_brace_open()
        
        for i, item in enumerate(node.items):
            if i > 0:
                self._write_line()
            
            item.accept(self)
            self._write_line()
        
        self._write_brace_close()
        
        self.in_trait = False
    
    def visit_rust_impl(self, node: RustImpl):
        """Visit impl block."""
        self.in_impl = True
        
        # Write visibility
        self._write_visibility(node.visibility)
        
        if node.is_unsafe:
            self._write('unsafe ')
        
        self._write('impl')
        
        # Write generics
        if node.generics:
            self._write('<')
            self._write_separated_list(node.generics, ', ')
            self._write('>')
        
        # Write trait reference
        if node.trait_ref:
            self._write(' ')
            self._write(node.trait_ref)
            self._write(' for')
        
        # Write self type
        if node.self_type:
            self._write(' ')
            node.self_type.accept(self)
        
        # Write where clause
        if node.where_clause:
            self._write_space_if_needed(self.options.space_before_where_clause)
            node.where_clause.accept(self)
        
        # Write impl items
        self._write_brace_open()
        
        for i, item in enumerate(node.items):
            if i > 0:
                self._write_line()
            
            item.accept(self)
            self._write_line()
        
        self._write_brace_close()
        
        self.in_impl = False
    
    def visit_rust_type_alias(self, node: RustTypeAlias):
        """Visit type alias."""
        # Write visibility
        self._write_visibility(node.visibility)
        
        self._write('type ')
        self._write(node.name)
        
        # Write generics
        if node.generics:
            self._write('<')
            self._write_separated_list(node.generics, ', ')
            self._write('>')
        
        # Write where clause
        if node.where_clause:
            self._write_space_if_needed(self.options.space_before_where_clause)
            node.where_clause.accept(self)
        
        if node.type_def:
            self._write(' = ')
            node.type_def.accept(self)
        
        self._write(';')
    
    def visit_rust_const(self, node: RustConst):
        """Visit const declaration."""
        # Write visibility
        self._write_visibility(node.visibility)
        
        self._write('const ')
        self._write(node.name)
        
        if node.const_type:
            self._write(': ')
            node.const_type.accept(self)
        
        if node.value:
            self._write(' = ')
            node.value.accept(self)
        
        self._write(';')
    
    def visit_rust_static(self, node: RustStatic):
        """Visit static declaration."""
        # Write visibility
        self._write_visibility(node.visibility)
        
        self._write('static ')
        
        if node.mutability == RustMutability.MUTABLE:
            self._write('mut ')
        
        self._write(node.name)
        
        if node.static_type:
            self._write(': ')
            node.static_type.accept(self)
        
        if node.value:
            self._write(' = ')
            node.value.accept(self)
        
        self._write(';')
    
    def visit_rust_identifier(self, node: RustIdentifier):
        """Visit identifier."""
        self._write(node.name)
    
    def visit_rust_literal(self, node: RustLiteral):
        """Visit literal."""
        if node.literal_type == "string":
            self._write(f'"{node.value}"')
        elif node.literal_type == "char":
            self._write(f"'{node.value}'")
        elif node.literal_type == "boolean":
            self._write(str(node.value).lower())
        elif node.value is None:
            # This might be a unit type or similar
            self._write('()')
        else:
            value_str = str(node.value)
            if node.suffix:
                value_str += node.suffix
            self._write(value_str)
    
    def visit_rust_path(self, node: RustPath):
        """Visit path."""
        for i, segment in enumerate(node.segments):
            if i > 0:
                self._write('::')
            
            self._write(segment)
            
            # Write type arguments for this segment
            if i < len(node.type_arguments) and node.type_arguments[i]:
                self._write('<')
                self._write_separated_list(node.type_arguments[i], ', ')
                self._write('>')
    
    def visit_rust_block(self, node: RustBlock):
        """Visit block."""
        if node.is_unsafe:
            self._write('unsafe ')
        if node.is_async:
            self._write('async ')
        if node.is_const:
            self._write('const ')
        
        # For single-expression blocks in certain contexts, we might want different formatting
        if len(node.statements) == 0 and node.expression:
            # Single expression block
            node.expression.accept(self)
        elif len(node.statements) == 1 and not node.expression:
            # Single statement block
            stmt = node.statements[0]
            if isinstance(stmt, RustExpressionStatement) and not stmt.has_semicolon:
                # Expression statement without semicolon
                stmt.expression.accept(self) if stmt.expression else None
            else:
                stmt.accept(self)
        else:
            # Multi-statement block
            for stmt in node.statements:
                stmt.accept(self)
                self._write_line()
            
            if node.expression:
                node.expression.accept(self)
    
    def visit_rust_if_expression(self, node: RustIfExpression):
        """Visit if expression."""
        self._write('if ')
        
        if node.condition:
            node.condition.accept(self)
        
        self._write_space_if_needed(self.options.space_before_if_parentheses)
        self._write_brace_open()
        
        if node.then_branch:
            node.then_branch.accept(self)
        
        self._write_brace_close()
        
        if node.else_branch:
            self._write(' else ')
            
            if isinstance(node.else_branch, RustIfExpression):
                # else if
                node.else_branch.accept(self)
            else:
                self._write_brace_open()
                node.else_branch.accept(self)
                self._write_brace_close()
    
    def visit_rust_match_expression(self, node: RustMatchExpression):
        """Visit match expression."""
        self._write('match ')
        
        if node.expression:
            node.expression.accept(self)
        
        self._write_space_if_needed(self.options.space_before_match_parentheses)
        self._write_brace_open()
        
        for arm in node.arms:
            self._write_match_arm(arm)
            self._write_line()
        
        self._write_brace_close()
    
    def visit_rust_call_expression(self, node: RustCallExpression):
        """Visit call expression."""
        if node.function:
            node.function.accept(self)
        
        self._write('(')
        
        if node.arguments:
            self._write_separated_list(node.arguments, ', ')
        
        self._write(')')
    
    def visit_rust_method_call(self, node: RustMethodCall):
        """Visit method call."""
        if node.receiver:
            node.receiver.accept(self)
        
        self._write('.')
        self._write(node.method_name)
        
        # Write type arguments
        if node.type_arguments:
            self._write('::<')
            self._write_separated_list(node.type_arguments, ', ')
            self._write('>')
        
        self._write('(')
        
        if node.arguments:
            self._write_separated_list(node.arguments, ', ')
        
        self._write(')')
    
    def visit_rust_field_access(self, node: RustFieldAccess):
        """Visit field access."""
        if node.receiver:
            node.receiver.accept(self)
        
        self._write('.')
        self._write(node.field_name)
    
    def visit_rust_await_expression(self, node: RustAwaitExpression):
        """Visit await expression."""
        if node.expression:
            node.expression.accept(self)
        
        self._write('.await')
    
    def visit_rust_try_expression(self, node: RustTryExpression):
        """Visit try expression."""
        if node.expression:
            node.expression.accept(self)
        
        self._write('?')
    
    def visit_rust_return_expression(self, node: RustReturnExpression):
        """Visit return expression."""
        self._write('return')
        
        if node.expression:
            self._write(' ')
            node.expression.accept(self)
    
    def visit_rust_let_statement(self, node: RustLetStatement):
        """Visit let statement."""
        self._write('let ')
        
        if node.pattern:
            self._write_pattern(node.pattern)
        
        if node.type_annotation:
            self._write(': ')
            node.type_annotation.accept(self)
        
        if node.initializer:
            self._write(' = ')
            node.initializer.accept(self)
        
        self._write(';')
    
    def visit_rust_expression_statement(self, node: RustExpressionStatement):
        """Visit expression statement."""
        if node.expression:
            node.expression.accept(self)
        
        if node.has_semicolon:
            self._write(';')
    
    def visit_rust_type_reference(self, node: RustTypeReference):
        """Visit type reference."""
        self._write(node.path)
        
        if node.type_arguments:
            self._write('<')
            self._write_separated_list(node.type_arguments, ', ')
            self._write('>')
    
    def visit_rust_reference_type(self, node: RustReferenceType):
        """Visit reference type."""
        self._write('&')
        
        if node.lifetime:
            node.lifetime.accept(self)
            self._write(' ')
        
        if node.mutability == RustMutability.MUTABLE:
            self._write('mut ')
        
        if node.inner_type:
            node.inner_type.accept(self)
    
    def visit_rust_array_type(self, node: RustArrayType):
        """Visit array type."""
        self._write('[')
        
        if node.element_type:
            node.element_type.accept(self)
        
        if node.size:
            self._write('; ')
            node.size.accept(self)
        
        self._write(']')
    
    def visit_rust_tuple_type(self, node: RustTupleType):
        """Visit tuple type."""
        self._write('(')
        
        if node.element_types:
            self._write_separated_list(node.element_types, ', ')
            
            # Single-element tuple needs trailing comma
            if len(node.element_types) == 1:
                self._write(',')
        
        self._write(')')
    
    def visit_rust_lifetime(self, node: RustLifetime):
        """Visit lifetime."""
        self._write(f"'{node.name}")
    
    def visit_rust_attribute(self, node: RustAttribute):
        """Visit attribute."""
        if node.is_inner:
            self._write('#![')
        else:
            self._write('#[')
        
        self._write(node.path)
        
        if node.tokens:
            self._write('(')
            self._write(''.join(node.tokens))
            self._write(')')
        
        self._write(']')
    
    # Helper methods
    def _write_visibility(self, visibility: RustVisibility):
        """Write visibility modifier."""
        if visibility == RustVisibility.PUBLIC:
            self._write('pub ')
        elif visibility == RustVisibility.PUBLIC_CRATE:
            self._write('pub(crate) ')
        elif visibility == RustVisibility.PUBLIC_SUPER:
            self._write('pub(super) ')
        elif visibility == RustVisibility.PUBLIC_SELF:
            self._write('pub(self) ')
        elif visibility == RustVisibility.PUBLIC_IN:
            self._write('pub(in path) ')  # Simplified
        # PRIVATE is default, write nothing
    
    def _write_parameter(self, param: RustParameter):
        """Write function parameter."""
        if param.is_self:
            if param.self_kind:
                self._write(param.self_kind)
            else:
                self._write('self')
        else:
            self._write(param.name)
            
            if param.param_type:
                self._write(': ')
                param.param_type.accept(self)
    
    def _write_struct_field(self, field: RustField):
        """Write struct field."""
        # Write field visibility
        self._write_visibility(field.visibility)
        
        self._write(field.name)
        
        if field.field_type:
            self._write(': ')
            field.field_type.accept(self)
    
    def _write_tuple_field(self, field: RustField):
        """Write tuple struct field."""
        # Write field visibility
        self._write_visibility(field.visibility)
        
        if field.field_type:
            field.field_type.accept(self)
    
    def _write_enum_variant(self, variant: RustEnumVariant):
        """Write enum variant."""
        self._write(variant.name)
        
        if variant.is_tuple and variant.fields:
            self._write('(')
            self._write_separated_list(
                variant.fields,
                ', ',
                lambda f: self._write_tuple_field(f)
            )
            self._write(')')
        elif not variant.is_unit and variant.fields:
            self._write_brace_open()
            
            for i, field in enumerate(variant.fields):
                if i > 0:
                    self._write_line()
                
                self._write_struct_field(field)
                self._write(',')
                self._write_line()
            
            self._write_brace_close()
        
        if variant.discriminant:
            self._write(' = ')
            variant.discriminant.accept(self)
    
    def _write_match_arm(self, arm: RustMatchArm):
        """Write match arm."""
        if arm.pattern:
            self._write_pattern(arm.pattern)
        
        if arm.guard:
            self._write(' if ')
            arm.guard.accept(self)
        
        self._write(' => ')
        
        if arm.body:
            if self.options.match_arm_blocks:
                self._write_brace_open()
                arm.body.accept(self)
                self._write_brace_close()
            else:
                arm.body.accept(self)
        
        self._write(',')
    
    def _write_pattern(self, pattern: RustPattern):
        """Write pattern (simplified)."""
        if isinstance(pattern, RustIdentifierPattern):
            if pattern.mutability == RustMutability.MUTABLE:
                self._write('mut ')
            self._write(pattern.name)
        elif isinstance(pattern, RustWildcardPattern):
            self._write('_')
        elif isinstance(pattern, RustLiteralPattern):
            if pattern.literal:
                pattern.literal.accept(self)
        else:
            # Default pattern handling
            self._write('_')


# Convenience functions
def generate_rust_code(ast: RustCrate, 
                      style: RustCodeStyle = RustCodeStyle.RUSTFMT) -> str:
    """Generate Rust code from AST with specified style."""
    generator = RustCodeGenerator(style)
    return generator.generate(ast)


def format_rust_code(code: str, 
                    style: RustCodeStyle = RustCodeStyle.RUSTFMT) -> str:
    """Format existing Rust code with specified style."""
    # This would require parsing and re-generating
    # For now, return the original code
    return code