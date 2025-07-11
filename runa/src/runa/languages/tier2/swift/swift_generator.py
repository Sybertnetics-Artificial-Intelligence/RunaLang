#!/usr/bin/env python3
"""
Swift Code Generator

Generates Swift code from Swift AST nodes with support for multiple code styles.

Author: Sybertnetics AI Solutions
License: MIT
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass
from enum import Enum, auto
import logging

from .swift_ast import *


class SwiftCodeStyle(Enum):
    """Swift code formatting styles."""
    APPLE = "apple"
    GOOGLE = "google"
    RAYWENDERLICH = "raywenderlich"
    SWIFTLINT = "swiftlint"
    COMPACT = "compact"


@dataclass
class SwiftFormattingOptions:
    """Swift code formatting options."""
    indent_size: int = 4
    max_line_length: int = 120
    use_tabs: bool = False
    space_before_brace: bool = True
    space_after_comma: bool = True
    space_around_operators: bool = True
    trailing_comma: bool = False
    
    # Swift-specific
    force_unwrapping_spacing: bool = False
    optional_chaining_spacing: bool = False
    prefer_explicit_types: bool = False
    prefer_shorthand_operators: bool = True


class SwiftFormatter:
    """Swift code formatter with style presets."""
    
    @staticmethod
    def get_style_options(style: SwiftCodeStyle) -> SwiftFormattingOptions:
        """Get formatting options for a specific style."""
        if style == SwiftCodeStyle.APPLE:
            return SwiftFormattingOptions(
                indent_size=4,
                max_line_length=120,
                space_before_brace=True,
                trailing_comma=False
            )
        elif style == SwiftCodeStyle.GOOGLE:
            return SwiftFormattingOptions(
                indent_size=2,
                max_line_length=100,
                space_before_brace=True,
                trailing_comma=True
            )
        elif style == SwiftCodeStyle.RAYWENDERLICH:
            return SwiftFormattingOptions(
                indent_size=2,
                max_line_length=120,
                space_before_brace=True,
                trailing_comma=False
            )
        elif style == SwiftCodeStyle.SWIFTLINT:
            return SwiftFormattingOptions(
                indent_size=4,
                max_line_length=120,
                space_before_brace=True,
                trailing_comma=True
            )
        elif style == SwiftCodeStyle.COMPACT:
            return SwiftFormattingOptions(
                indent_size=2,
                max_line_length=160,
                space_before_brace=False,
                trailing_comma=False
            )
        else:
            return SwiftFormattingOptions()


class SwiftCodeGenerator(SwiftVisitor):
    """Swift code generator that produces formatted Swift source code from AST."""
    
    def __init__(self, style: SwiftCodeStyle = SwiftCodeStyle.APPLE):
        self.style = style
        self.options = SwiftFormatter.get_style_options(style)
        self.logger = logging.getLogger(__name__)
        
        # Output state
        self.output = []
        self.indent_level = 0
        self.current_line_length = 0
        self.needs_indent = True
    
    def generate(self, node: SwiftNode) -> str:
        """Generate Swift code from an AST node."""
        self.output = []
        self.indent_level = 0
        self.current_line_length = 0
        self.needs_indent = True
        
        try:
            node.accept(self)
            result = "".join(self.output)
            return self._post_process(result)
        except Exception as e:
            self.logger.error(f"Swift code generation failed: {e}")
            raise RuntimeError(f"Failed to generate Swift code: {e}")
    
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
    def visit_swift_source_file(self, node: SwiftSourceFile):
        """Visit source file."""
        # Write imports
        for import_decl in node.imports:
            import_decl.accept(self)
            self._write_line()
        
        if node.imports:
            self._write_line()
        
        # Write declarations
        for i, decl in enumerate(node.declarations):
            if i > 0:
                self._write_line()
                self._write_line()
            
            decl.accept(self)
            self._write_line()
    
    def visit_swift_import_declaration(self, node: SwiftImportDeclaration):
        """Visit import declaration."""
        self._write('import ')
        self._write(node.module_name)
    
    def visit_swift_class_declaration(self, node: SwiftClassDeclaration):
        """Visit class declaration."""
        # Write access level
        if node.access_level != SwiftAccessLevel.INTERNAL:
            self._write(node.access_level.value)
            self._write_space()
        
        # Write modifiers
        if node.is_final:
            self._write('final ')
        
        self._write('class ')
        self._write(node.name)
        
        # Write inheritance
        if node.superclass or node.protocols:
            self._write(': ')
            
            inheritance_list = []
            if node.superclass:
                inheritance_list.append(node.superclass.name if hasattr(node.superclass, 'name') else str(node.superclass))
            
            for protocol in node.protocols:
                inheritance_list.append(protocol.name if hasattr(protocol, 'name') else str(protocol))
            
            self._write(', '.join(inheritance_list))
        
        # Write body
        self._write_brace_open()
        
        for i, member in enumerate(node.members):
            if i > 0:
                self._write_line()
            
            member.accept(self)
            self._write_line()
        
        self._write_brace_close()
    
    def visit_swift_struct_declaration(self, node: SwiftStructDeclaration):
        """Visit struct declaration."""
        # Write access level
        if node.access_level != SwiftAccessLevel.INTERNAL:
            self._write(node.access_level.value)
            self._write_space()
        
        self._write('struct ')
        self._write(node.name)
        
        # Write protocols
        if node.protocols:
            self._write(': ')
            protocol_names = []
            for protocol in node.protocols:
                protocol_names.append(protocol.name if hasattr(protocol, 'name') else str(protocol))
            self._write(', '.join(protocol_names))
        
        # Write body
        self._write_brace_open()
        
        for i, member in enumerate(node.members):
            if i > 0:
                self._write_line()
            
            member.accept(self)
            self._write_line()
        
        self._write_brace_close()
    
    def visit_swift_enum_declaration(self, node: SwiftEnumDeclaration):
        """Visit enum declaration."""
        # Write access level
        if node.access_level != SwiftAccessLevel.INTERNAL:
            self._write(node.access_level.value)
            self._write_space()
        
        self._write('enum ')
        self._write(node.name)
        
        # Write raw type and protocols
        inheritance_list = []
        if node.raw_type:
            inheritance_list.append(node.raw_type.name if hasattr(node.raw_type, 'name') else str(node.raw_type))
        
        for protocol in node.protocols:
            inheritance_list.append(protocol.name if hasattr(protocol, 'name') else str(protocol))
        
        if inheritance_list:
            self._write(': ')
            self._write(', '.join(inheritance_list))
        
        # Write body
        self._write_brace_open()
        
        # Write cases
        for case in node.cases:
            self._write('case ')
            self._write(case.name)
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
    
    def visit_swift_function_declaration(self, node: SwiftFunctionDeclaration):
        """Visit function declaration."""
        # Write access level
        if node.access_level != SwiftAccessLevel.INTERNAL:
            self._write(node.access_level.value)
            self._write_space()
        
        # Write modifiers
        if node.is_static:
            self._write('static ')
        if node.is_mutating:
            self._write('mutating ')
        
        self._write('func ')
        self._write(node.name)
        
        # Write parameters
        self._write('(')
        
        for i, param in enumerate(node.parameters):
            if i > 0:
                self._write(', ')
            
            if param.external_name:
                self._write(param.external_name)
                self._write(' ')
            
            self._write(param.internal_name)
            
            if param.type_annotation:
                self._write(': ')
                self._write_type(param.type_annotation)
            
            if param.default_value:
                self._write(' = ')
                param.default_value.accept(self)
        
        self._write(')')
        
        # Write return type
        if node.return_type:
            self._write(' -> ')
            self._write_type(node.return_type)
        
        # Write body
        if node.body:
            self._write_brace_open()
            node.body.accept(self)
            self._write_brace_close()
    
    def visit_swift_variable_declaration(self, node: SwiftVariableDeclaration):
        """Visit variable declaration."""
        # Write access level
        if node.access_level != SwiftAccessLevel.INTERNAL:
            self._write(node.access_level.value)
            self._write_space()
        
        self._write(node.mutability.value)
        self._write(' ')
        self._write(node.name)
        
        if node.type_annotation:
            self._write(': ')
            self._write_type(node.type_annotation)
        
        if node.initializer:
            self._write(' = ')
            node.initializer.accept(self)
    
    def visit_swift_actor_declaration(self, node: SwiftActorDeclaration):
        """Visit actor declaration."""
        # Write access level
        if node.access_level != SwiftAccessLevel.INTERNAL:
            self._write(node.access_level.value)
            self._write_space()
        
        self._write('actor ')
        self._write(node.name)
        
        # Write protocols
        if node.protocols:
            self._write(': ')
            protocol_names = []
            for protocol in node.protocols:
                protocol_names.append(protocol.name if hasattr(protocol, 'name') else str(protocol))
            self._write(', '.join(protocol_names))
        
        # Write body
        self._write_brace_open()
        
        for i, member in enumerate(node.members):
            if i > 0:
                self._write_line()
            
            member.accept(self)
            self._write_line()
        
        self._write_brace_close()
    
    def visit_swift_code_block(self, node: SwiftCodeBlock):
        """Visit code block."""
        for stmt in node.statements:
            stmt.accept(self)
            self._write_line()
    
    def visit_swift_identifier_expression(self, node: SwiftIdentifierExpression):
        """Visit identifier expression."""
        self._write(node.name)
    
    def visit_swift_literal_expression(self, node: SwiftLiteralExpression):
        """Visit literal expression."""
        if node.literal_type == "string":
            self._write(f'"{node.value}"')
        elif node.literal_type == "bool":
            self._write(str(node.value).lower())
        elif node.literal_type == "nil":
            self._write('nil')
        else:
            self._write(str(node.value))
    
    def visit_swift_protocol_declaration(self, node: SwiftProtocolDeclaration):
        """Visit protocol declaration."""
        # Write access level
        if node.access_level != SwiftAccessLevel.INTERNAL:
            self._write(node.access_level.value)
            self._write_space()
        
        self._write('protocol ')
        self._write(node.name)
        
        # Write inherited protocols
        if node.protocols:
            self._write(': ')
            protocol_names = []
            for protocol in node.protocols:
                protocol_names.append(protocol.name if hasattr(protocol, 'name') else str(protocol))
            self._write(', '.join(protocol_names))
        
        # Write body
        self._write_brace_open()
        
        for i, member in enumerate(node.members):
            if i > 0:
                self._write_line()
            
            member.accept(self)
            self._write_line()
        
        self._write_brace_close()
    
    def visit_swift_extension_declaration(self, node: SwiftExtensionDeclaration):
        """Visit extension declaration."""
        # Write access level
        if node.access_level != SwiftAccessLevel.INTERNAL:
            self._write(node.access_level.value)
            self._write_space()
        
        self._write('extension ')
        
        if node.extended_type:
            self._write_type(node.extended_type)
        
        # Write protocols
        if node.protocols:
            self._write(': ')
            protocol_names = []
            for protocol in node.protocols:
                protocol_names.append(protocol.name if hasattr(protocol, 'name') else str(protocol))
            self._write(', '.join(protocol_names))
        
        # Write body
        self._write_brace_open()
        
        for i, member in enumerate(node.members):
            if i > 0:
                self._write_line()
            
            member.accept(self)
            self._write_line()
        
        self._write_brace_close()
    
    def _write_type(self, type_node: SwiftType):
        """Write type."""
        if isinstance(type_node, SwiftTypeIdentifier):
            self._write(type_node.name)
        elif isinstance(type_node, SwiftOptionalType):
            if type_node.wrapped_type:
                self._write_type(type_node.wrapped_type)
            self._write('?')
        elif isinstance(type_node, SwiftArrayType):
            self._write('[')
            if type_node.element_type:
                self._write_type(type_node.element_type)
            self._write(']')
        elif isinstance(type_node, SwiftDictionaryType):
            self._write('[')
            if type_node.key_type:
                self._write_type(type_node.key_type)
            self._write(': ')
            if type_node.value_type:
                self._write_type(type_node.value_type)
            self._write(']')
        else:
            self._write('Any')


# Convenience functions
def generate_swift_code(ast: SwiftSourceFile, 
                       style: SwiftCodeStyle = SwiftCodeStyle.APPLE) -> str:
    """Generate Swift code from AST with specified style."""
    generator = SwiftCodeGenerator(style)
    return generator.generate(ast)


def format_swift_code(code: str, 
                     style: SwiftCodeStyle = SwiftCodeStyle.APPLE) -> str:
    """Format existing Swift code with specified style."""
    # This would require parsing and re-generating
    # For now, return the original code
    return code