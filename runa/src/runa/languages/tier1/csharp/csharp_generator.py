#!/usr/bin/env python3
"""
C# Code Generator

Generates clean, modern C# code from C# AST with support for multiple
formatting styles and all C# language features from C# 1.0 through C# 12.0.
"""

from typing import List, Dict, Any, Optional, Union, Set
from dataclasses import dataclass, field
from enum import Enum, auto
import textwrap
import re

from .csharp_ast import *


class CSharpCodeStyle(Enum):
    """C# code formatting styles."""
    MICROSOFT = auto()      # Microsoft C# coding conventions
    GOOGLE = auto()         # Google C# style guide
    JETBRAINS = auto()      # JetBrains/ReSharper style
    UNITY = auto()          # Unity C# coding standards
    CLEAN_CODE = auto()     # Clean Code principles
    COMPACT = auto()        # Compact style for generated code


@dataclass
class CSharpFormattingOptions:
    """C# code formatting options."""
    # Indentation
    indent_size: int = 4
    use_tabs: bool = False
    
    # Braces
    brace_style: str = "microsoft"  # microsoft, java, stroustrup, gnu
    space_before_open_brace: bool = True
    new_line_before_open_brace: bool = True
    new_line_before_else: bool = True
    new_line_before_catch: bool = True
    new_line_before_finally: bool = True
    
    # Spacing
    space_after_keywords: bool = True
    space_around_operators: bool = True
    space_after_commas: bool = True
    space_after_semicolons: bool = True
    space_within_parentheses: bool = False
    space_within_brackets: bool = False
    space_within_braces: bool = False
    
    # Line breaks
    max_line_length: int = 120
    wrap_long_lines: bool = True
    blank_lines_around_namespaces: int = 1
    blank_lines_around_classes: int = 1
    blank_lines_around_methods: int = 1
    blank_lines_around_properties: int = 0
    
    # Naming conventions
    prefer_var_keyword: bool = True
    prefer_expression_bodies: bool = True
    prefer_pattern_matching: bool = True
    prefer_null_conditional: bool = True
    prefer_string_interpolation: bool = True
    
    # Modern C# features
    use_file_scoped_namespaces: bool = True  # C# 10.0
    use_global_using: bool = True  # C# 10.0
    use_top_level_programs: bool = False  # C# 9.0
    use_target_typed_new: bool = True  # C# 9.0
    use_records: bool = True  # C# 9.0
    use_init_only_properties: bool = True  # C# 9.0
    use_nullable_reference_types: bool = True  # C# 8.0
    use_switch_expressions: bool = True  # C# 8.0
    use_pattern_matching: bool = True  # C# 7.0+
    use_tuple_deconstruction: bool = True  # C# 7.0
    use_expression_bodied_members: bool = True  # C# 6.0+
    use_string_interpolation: bool = True  # C# 6.0
    use_null_conditional_operators: bool = True  # C# 6.0
    use_auto_properties: bool = True  # C# 3.0
    use_var_declarations: bool = True  # C# 3.0
    use_lambda_expressions: bool = True  # C# 3.0
    use_linq: bool = True  # C# 3.0
    use_generics: bool = True  # C# 2.0
    use_nullable_types: bool = True  # C# 2.0
    use_anonymous_methods: bool = True  # C# 2.0
    use_iterators: bool = True  # C# 2.0
    use_partial_classes: bool = True  # C# 2.0


class CSharpFormatter:
    """C# code formatter with multiple style presets."""
    
    @staticmethod
    def get_style_options(style: CSharpCodeStyle) -> CSharpFormattingOptions:
        """Get formatting options for a specific style."""
        if style == CSharpCodeStyle.MICROSOFT:
            return CSharpFormattingOptions(
                indent_size=4,
                use_tabs=False,
                brace_style="microsoft",
                new_line_before_open_brace=True,
                max_line_length=120,
                prefer_var_keyword=True,
                use_file_scoped_namespaces=True,
                use_nullable_reference_types=True
            )
        elif style == CSharpCodeStyle.GOOGLE:
            return CSharpFormattingOptions(
                indent_size=2,
                use_tabs=False,
                brace_style="java",
                new_line_before_open_brace=False,
                max_line_length=100,
                prefer_var_keyword=False,
                use_file_scoped_namespaces=False,
                use_nullable_reference_types=True
            )
        elif style == CSharpCodeStyle.JETBRAINS:
            return CSharpFormattingOptions(
                indent_size=4,
                use_tabs=False,
                brace_style="microsoft",
                new_line_before_open_brace=True,
                max_line_length=120,
                prefer_var_keyword=True,
                prefer_expression_bodies=True,
                use_file_scoped_namespaces=True,
                use_nullable_reference_types=True
            )
        elif style == CSharpCodeStyle.UNITY:
            return CSharpFormattingOptions(
                indent_size=4,
                use_tabs=False,
                brace_style="microsoft",
                new_line_before_open_brace=True,
                max_line_length=120,
                prefer_var_keyword=False,
                use_file_scoped_namespaces=False,
                use_nullable_reference_types=False
            )
        elif style == CSharpCodeStyle.CLEAN_CODE:
            return CSharpFormattingOptions(
                indent_size=4,
                use_tabs=False,
                brace_style="microsoft",
                new_line_before_open_brace=True,
                max_line_length=80,
                prefer_var_keyword=True,
                prefer_expression_bodies=True,
                use_file_scoped_namespaces=True,
                use_nullable_reference_types=True,
                blank_lines_around_methods=2
            )
        elif style == CSharpCodeStyle.COMPACT:
            return CSharpFormattingOptions(
                indent_size=2,
                use_tabs=False,
                brace_style="java",
                new_line_before_open_brace=False,
                max_line_length=150,
                prefer_var_keyword=True,
                blank_lines_around_namespaces=0,
                blank_lines_around_classes=0,
                blank_lines_around_methods=0,
                use_file_scoped_namespaces=True,
                use_nullable_reference_types=True
            )
        else:
            return CSharpFormattingOptions()


class CSharpCodeGenerator:
    """C# code generator with comprehensive modern C# support."""
    
    def __init__(self, style: CSharpCodeStyle = CSharpCodeStyle.MICROSOFT):
        self.style = style
        self.options = CSharpFormatter.get_style_options(style)
        self.indent_level = 0
        self.output = []
        self.imports = set()
        self.namespace_name = ""
        self.current_class = None
        self.in_expression = False
        self.generated_helpers = set()
        
    def generate(self, node: CSharpNode) -> str:
        """Generate C# code from AST node."""
        self.output = []
        self.indent_level = 0
        self.imports = set()
        self.namespace_name = ""
        self.current_class = None
        self.in_expression = False
        self.generated_helpers = set()
        
        self._generate_node(node)
        
        # Build final output
        result = []
        
        # Add standard imports if needed
        if self.imports:
            sorted_imports = sorted(self.imports)
            if self.options.use_global_using:
                result.extend(f"global using {imp};" for imp in sorted_imports)
            else:
                result.extend(f"using {imp};" for imp in sorted_imports)
            result.append("")
        
        # Add generated code
        result.extend(self.output)
        
        return "\n".join(result)
    
    def _generate_node(self, node: CSharpNode) -> None:
        """Generate code for a specific node type."""
        if isinstance(node, CSharpCompilationUnit):
            self._generate_compilation_unit(node)
        elif isinstance(node, CSharpNamespaceDeclaration):
            self._generate_namespace_declaration(node)
        elif isinstance(node, CSharpUsingDirective):
            self._generate_using_directive(node)
        elif isinstance(node, CSharpClassDeclaration):
            self._generate_class_declaration(node)
        elif isinstance(node, CSharpStructDeclaration):
            self._generate_struct_declaration(node)
        elif isinstance(node, CSharpInterfaceDeclaration):
            self._generate_interface_declaration(node)
        elif isinstance(node, CSharpEnumDeclaration):
            self._generate_enum_declaration(node)
        elif isinstance(node, CSharpRecordDeclaration):
            self._generate_record_declaration(node)
        elif isinstance(node, CSharpMethodDeclaration):
            self._generate_method_declaration(node)
        elif isinstance(node, CSharpPropertyDeclaration):
            self._generate_property_declaration(node)
        elif isinstance(node, CSharpFieldDeclaration):
            self._generate_field_declaration(node)
        elif isinstance(node, CSharpConstructorDeclaration):
            self._generate_constructor_declaration(node)
        elif isinstance(node, CSharpDestructorDeclaration):
            self._generate_destructor_declaration(node)
        elif isinstance(node, CSharpIndexerDeclaration):
            self._generate_indexer_declaration(node)
        elif isinstance(node, CSharpOperatorDeclaration):
            self._generate_operator_declaration(node)
        elif isinstance(node, CSharpEventDeclaration):
            self._generate_event_declaration(node)
        elif isinstance(node, CSharpDelegateDeclaration):
            self._generate_delegate_declaration(node)
        elif isinstance(node, CSharpStatement):
            self._generate_statement(node)
        elif isinstance(node, CSharpExpression):
            self._generate_expression(node)
        elif isinstance(node, CSharpType):
            self._generate_type(node)
        elif isinstance(node, list):
            for item in node:
                self._generate_node(item)
    
    def _generate_compilation_unit(self, node: CSharpCompilationUnit) -> None:
        """Generate compilation unit."""
        # Handle using directives
        for using_directive in node.using_directives:
            self._generate_using_directive(using_directive)
        
        if node.using_directives:
            self._add_blank_lines(1)
        
        # Handle global attributes
        for attr in node.global_attributes:
            self._generate_attribute(attr)
        
        # Handle members
        for i, member in enumerate(node.members):
            if i > 0:
                self._add_blank_lines(self.options.blank_lines_around_namespaces)
            self._generate_node(member)
    
    def _generate_namespace_declaration(self, node: CSharpNamespaceDeclaration) -> None:
        """Generate namespace declaration."""
        self.namespace_name = node.name
        
        if self.options.use_file_scoped_namespaces and len(node.members) > 0:
            # File-scoped namespace (C# 10.0)
            self._write_line(f"namespace {node.name};")
            self._add_blank_lines(1)
            
            for i, member in enumerate(node.members):
                if i > 0:
                    self._add_blank_lines(self.options.blank_lines_around_classes)
                self._generate_node(member)
        else:
            # Traditional namespace
            self._write_line(f"namespace {node.name}")
            self._write_line("{")
            self._indent()
            
            for i, member in enumerate(node.members):
                if i > 0:
                    self._add_blank_lines(self.options.blank_lines_around_classes)
                self._generate_node(member)
            
            self._dedent()
            self._write_line("}")
    
    def _generate_using_directive(self, node: CSharpUsingDirective) -> None:
        """Generate using directive."""
        if node.is_global:
            prefix = "global using"
        else:
            prefix = "using"
        
        if node.alias:
            self._write_line(f"{prefix} {node.alias} = {node.name};")
        elif node.is_static:
            self._write_line(f"{prefix} static {node.name};")
        else:
            self._write_line(f"{prefix} {node.name};")
    
    def _generate_class_declaration(self, node: CSharpClassDeclaration) -> None:
        """Generate class declaration."""
        self.current_class = node.name
        
        # Generate attributes
        for attr in node.attributes:
            self._generate_attribute(attr)
        
        # Generate class signature
        parts = []
        
        # Access modifiers
        if node.modifiers:
            parts.extend(node.modifiers)
        
        # Class keyword
        if node.is_partial:
            parts.append("partial")
        parts.append("class")
        parts.append(node.name)
        
        # Generic parameters
        if node.type_parameters:
            type_params = ", ".join(tp.name for tp in node.type_parameters)
            parts.append(f"<{type_params}>")
        
        # Base types
        if node.base_types:
            base_list = ", ".join(self._type_to_string(bt) for bt in node.base_types)
            parts.append(f": {base_list}")
        
        self._write_line(" ".join(parts))
        
        # Type constraints
        for tp in node.type_parameters or []:
            if tp.constraints:
                constraint_list = ", ".join(self._type_to_string(c) for c in tp.constraints)
                self._write_line(f"    where {tp.name} : {constraint_list}")
        
        # Class body
        self._write_line("{")
        self._indent()
        
        # Generate members
        for i, member in enumerate(node.members):
            if i > 0:
                self._add_blank_lines(self.options.blank_lines_around_methods)
            self._generate_node(member)
        
        self._dedent()
        self._write_line("}")
        
        self.current_class = None
    
    def _generate_struct_declaration(self, node: CSharpStructDeclaration) -> None:
        """Generate struct declaration."""
        # Generate attributes
        for attr in node.attributes:
            self._generate_attribute(attr)
        
        # Generate struct signature
        parts = []
        
        # Access modifiers
        if node.modifiers:
            parts.extend(node.modifiers)
        
        # Struct keyword
        if node.is_partial:
            parts.append("partial")
        if node.is_readonly:
            parts.append("readonly")
        if node.is_ref:
            parts.append("ref")
        parts.append("struct")
        parts.append(node.name)
        
        # Generic parameters
        if node.type_parameters:
            type_params = ", ".join(tp.name for tp in node.type_parameters)
            parts.append(f"<{type_params}>")
        
        # Interfaces
        if node.interfaces:
            interface_list = ", ".join(self._type_to_string(i) for i in node.interfaces)
            parts.append(f": {interface_list}")
        
        self._write_line(" ".join(parts))
        
        # Type constraints
        for tp in node.type_parameters or []:
            if tp.constraints:
                constraint_list = ", ".join(self._type_to_string(c) for c in tp.constraints)
                self._write_line(f"    where {tp.name} : {constraint_list}")
        
        # Struct body
        self._write_line("{")
        self._indent()
        
        # Generate members
        for i, member in enumerate(node.members):
            if i > 0:
                self._add_blank_lines(self.options.blank_lines_around_methods)
            self._generate_node(member)
        
        self._dedent()
        self._write_line("}")
    
    def _generate_interface_declaration(self, node: CSharpInterfaceDeclaration) -> None:
        """Generate interface declaration."""
        # Generate attributes
        for attr in node.attributes:
            self._generate_attribute(attr)
        
        # Generate interface signature
        parts = []
        
        # Access modifiers
        if node.modifiers:
            parts.extend(node.modifiers)
        
        # Interface keyword
        if node.is_partial:
            parts.append("partial")
        parts.append("interface")
        parts.append(node.name)
        
        # Generic parameters
        if node.type_parameters:
            type_params = ", ".join(tp.name for tp in node.type_parameters)
            parts.append(f"<{type_params}>")
        
        # Base interfaces
        if node.base_interfaces:
            base_list = ", ".join(self._type_to_string(bi) for bi in node.base_interfaces)
            parts.append(f": {base_list}")
        
        self._write_line(" ".join(parts))
        
        # Type constraints
        for tp in node.type_parameters or []:
            if tp.constraints:
                constraint_list = ", ".join(self._type_to_string(c) for c in tp.constraints)
                self._write_line(f"    where {tp.name} : {constraint_list}")
        
        # Interface body
        self._write_line("{")
        self._indent()
        
        # Generate members
        for i, member in enumerate(node.members):
            if i > 0:
                self._add_blank_lines(self.options.blank_lines_around_methods)
            self._generate_node(member)
        
        self._dedent()
        self._write_line("}")
    
    def _generate_enum_declaration(self, node: CSharpEnumDeclaration) -> None:
        """Generate enum declaration."""
        # Generate attributes
        for attr in node.attributes:
            self._generate_attribute(attr)
        
        # Generate enum signature
        parts = []
        
        # Access modifiers
        if node.modifiers:
            parts.extend(node.modifiers)
        
        parts.append("enum")
        parts.append(node.name)
        
        # Underlying type
        if node.underlying_type:
            parts.append(f": {self._type_to_string(node.underlying_type)}")
        
        self._write_line(" ".join(parts))
        
        # Enum body
        self._write_line("{")
        self._indent()
        
        # Generate enum members
        for i, member in enumerate(node.members):
            line = member.name
            if member.value:
                line += f" = {self._expression_to_string(member.value)}"
            
            if i < len(node.members) - 1:
                line += ","
            
            self._write_line(line)
        
        self._dedent()
        self._write_line("}")
    
    def _generate_record_declaration(self, node: CSharpRecordDeclaration) -> None:
        """Generate record declaration (C# 9.0)."""
        # Generate attributes
        for attr in node.attributes:
            self._generate_attribute(attr)
        
        # Generate record signature
        parts = []
        
        # Access modifiers
        if node.modifiers:
            parts.extend(node.modifiers)
        
        parts.append("record")
        if node.is_class:
            parts.append("class")
        elif node.is_struct:
            parts.append("struct")
        
        parts.append(node.name)
        
        # Generic parameters
        if node.type_parameters:
            type_params = ", ".join(tp.name for tp in node.type_parameters)
            parts.append(f"<{type_params}>")
        
        # Primary constructor parameters
        if node.parameters:
            param_list = ", ".join(self._parameter_to_string(p) for p in node.parameters)
            parts.append(f"({param_list})")
        
        # Base types
        if node.base_types:
            base_list = ", ".join(self._type_to_string(bt) for bt in node.base_types)
            parts.append(f": {base_list}")
        
        self._write_line(" ".join(parts))
        
        # Type constraints
        for tp in node.type_parameters or []:
            if tp.constraints:
                constraint_list = ", ".join(self._type_to_string(c) for c in tp.constraints)
                self._write_line(f"    where {tp.name} : {constraint_list}")
        
        # Record body (if has members)
        if node.members:
            self._write_line("{")
            self._indent()
            
            for i, member in enumerate(node.members):
                if i > 0:
                    self._add_blank_lines(self.options.blank_lines_around_methods)
                self._generate_node(member)
            
            self._dedent()
            self._write_line("}")
        else:
            self._write_line(";")
    
    def _generate_method_declaration(self, node: CSharpMethodDeclaration) -> None:
        """Generate method declaration."""
        # Generate attributes
        for attr in node.attributes:
            self._generate_attribute(attr)
        
        # Generate method signature
        parts = []
        
        # Access modifiers
        if node.modifiers:
            parts.extend(node.modifiers)
        
        # Return type
        if node.return_type:
            parts.append(self._type_to_string(node.return_type))
        else:
            parts.append("void")
        
        # Method name
        parts.append(node.name)
        
        # Generic parameters
        if node.type_parameters:
            type_params = ", ".join(tp.name for tp in node.type_parameters)
            parts.append(f"<{type_params}>")
        
        # Parameters
        param_list = ", ".join(self._parameter_to_string(p) for p in node.parameters)
        parts.append(f"({param_list})")
        
        # Type constraints
        constraints = []
        for tp in node.type_parameters or []:
            if tp.constraints:
                constraint_list = ", ".join(self._type_to_string(c) for c in tp.constraints)
                constraints.append(f"where {tp.name} : {constraint_list}")
        
        signature = " ".join(parts)
        if constraints:
            signature += "\n    " + "\n    ".join(constraints)
        
        # Method body
        if node.body:
            self._write_line(signature)
            self._generate_node(node.body)
        elif node.expression_body:
            if self.options.prefer_expression_bodies:
                self._write_line(f"{signature} => {self._expression_to_string(node.expression_body)};")
            else:
                self._write_line(signature)
                self._write_line("{")
                self._indent()
                self._write_line(f"return {self._expression_to_string(node.expression_body)};")
                self._dedent()
                self._write_line("}")
        else:
            # Interface method or abstract method
            self._write_line(f"{signature};")
    
    def _generate_property_declaration(self, node: CSharpPropertyDeclaration) -> None:
        """Generate property declaration."""
        # Generate attributes
        for attr in node.attributes:
            self._generate_attribute(attr)
        
        # Generate property signature
        parts = []
        
        # Access modifiers
        if node.modifiers:
            parts.extend(node.modifiers)
        
        # Property type
        parts.append(self._type_to_string(node.type))
        
        # Property name
        parts.append(node.name)
        
        signature = " ".join(parts)
        
        # Property body
        if node.expression_body:
            if self.options.prefer_expression_bodies:
                self._write_line(f"{signature} => {self._expression_to_string(node.expression_body)};")
            else:
                self._write_line(f"{signature}")
                self._write_line("{")
                self._indent()
                self._write_line(f"get => {self._expression_to_string(node.expression_body)};")
                self._dedent()
                self._write_line("}")
        elif node.initializer:
            if self.options.use_init_only_properties and not node.getter and not node.setter:
                # Init-only property (C# 9.0)
                self._write_line(f"{signature} {{ get; init; }} = {self._expression_to_string(node.initializer)};")
            elif self.options.use_auto_properties and not node.getter and not node.setter:
                # Auto-implemented property
                self._write_line(f"{signature} {{ get; set; }} = {self._expression_to_string(node.initializer)};")
            else:
                self._write_line(f"{signature}")
                self._write_line("{")
                self._indent()
                
                if node.getter:
                    self._generate_node(node.getter)
                else:
                    self._write_line("get;")
                
                if node.setter:
                    self._generate_node(node.setter)
                else:
                    self._write_line("set;")
                
                self._dedent()
                self._write_line("}")
        else:
            if self.options.use_auto_properties and not node.getter and not node.setter:
                # Auto-implemented property
                self._write_line(f"{signature} {{ get; set; }}")
            else:
                self._write_line(f"{signature}")
                self._write_line("{")
                self._indent()
                
                if node.getter:
                    self._generate_node(node.getter)
                else:
                    self._write_line("get;")
                
                if node.setter:
                    self._generate_node(node.setter)
                else:
                    self._write_line("set;")
                
                self._dedent()
                self._write_line("}")
    
    def _generate_field_declaration(self, node: CSharpFieldDeclaration) -> None:
        """Generate field declaration."""
        # Generate attributes
        for attr in node.attributes:
            self._generate_attribute(attr)
        
        # Generate field signature
        parts = []
        
        # Access modifiers
        if node.modifiers:
            parts.extend(node.modifiers)
        
        # Field type
        parts.append(self._type_to_string(node.type))
        
        # Field name
        parts.append(node.name)
        
        # Initializer
        if node.initializer:
            parts.append(f"= {self._expression_to_string(node.initializer)}")
        
        self._write_line(" ".join(parts) + ";")
    
    def _generate_constructor_declaration(self, node: CSharpConstructorDeclaration) -> None:
        """Generate constructor declaration."""
        # Generate attributes
        for attr in node.attributes:
            self._generate_attribute(attr)
        
        # Generate constructor signature
        parts = []
        
        # Access modifiers
        if node.modifiers:
            parts.extend(node.modifiers)
        
        # Constructor name
        parts.append(node.name)
        
        # Parameters
        param_list = ", ".join(self._parameter_to_string(p) for p in node.parameters)
        parts.append(f"({param_list})")
        
        # Base/this constructor call
        if node.base_constructor_arguments is not None:
            arg_list = ", ".join(self._expression_to_string(arg) for arg in node.base_constructor_arguments)
            parts.append(f": base({arg_list})")
        elif node.this_constructor_arguments is not None:
            arg_list = ", ".join(self._expression_to_string(arg) for arg in node.this_constructor_arguments)
            parts.append(f": this({arg_list})")
        
        self._write_line(" ".join(parts))
        
        # Constructor body
        if node.body:
            self._generate_node(node.body)
        else:
            self._write_line("{")
            self._write_line("}")
    
    def _generate_destructor_declaration(self, node: CSharpDestructorDeclaration) -> None:
        """Generate destructor declaration."""
        # Generate attributes
        for attr in node.attributes:
            self._generate_attribute(attr)
        
        # Generate destructor signature
        parts = []
        
        # Access modifiers
        if node.modifiers:
            parts.extend(node.modifiers)
        
        # Destructor name
        parts.append(f"~{node.name}()")
        
        self._write_line(" ".join(parts))
        
        # Destructor body
        if node.body:
            self._generate_node(node.body)
        else:
            self._write_line("{")
            self._write_line("}")
    
    def _generate_statement(self, node: CSharpStatement) -> None:
        """Generate statement."""
        if isinstance(node, CSharpExpressionStatement):
            self._generate_expression_statement(node)
        elif isinstance(node, CSharpBlock):
            self._generate_block_statement(node)
        elif isinstance(node, CSharpIfStatement):
            self._generate_if_statement(node)
        elif isinstance(node, CSharpWhileStatement):
            self._generate_while_statement(node)
        elif isinstance(node, CSharpForStatement):
            self._generate_for_statement(node)
        elif isinstance(node, CSharpForEachStatement):
            self._generate_foreach_statement(node)
        elif isinstance(node, CSharpDoStatement):
            self._generate_do_statement(node)
        elif isinstance(node, CSharpSwitchStatement):
            self._generate_switch_statement(node)
        elif isinstance(node, CSharpBreakStatement):
            self._generate_break_statement(node)
        elif isinstance(node, CSharpContinueStatement):
            self._generate_continue_statement(node)
        elif isinstance(node, CSharpReturnStatement):
            self._generate_return_statement(node)
        elif isinstance(node, CSharpThrowStatement):
            self._generate_throw_statement(node)
        elif isinstance(node, CSharpTryStatement):
            self._generate_try_statement(node)
        elif isinstance(node, CSharpLockStatement):
            self._generate_lock_statement(node)
        elif isinstance(node, CSharpUsingStatement):
            self._generate_using_statement(node)
        elif isinstance(node, CSharpYieldStatement):
            self._generate_yield_statement(node)
        elif isinstance(node, CSharpLocalDeclarationStatement):
            self._generate_local_declaration_statement(node)
        elif isinstance(node, CSharpEmptyStatement):
            self._generate_empty_statement(node)
        elif isinstance(node, CSharpLabeledStatement):
            self._generate_labeled_statement(node)
        elif isinstance(node, CSharpGotoStatement):
            self._generate_goto_statement(node)
        elif isinstance(node, CSharpCheckedStatement):
            self._generate_checked_statement(node)
        elif isinstance(node, CSharpUncheckedStatement):
            self._generate_unchecked_statement(node)
        elif isinstance(node, CSharpUnsafeStatement):
            self._generate_unsafe_statement(node)
        elif isinstance(node, CSharpFixedStatement):
            self._generate_fixed_statement(node)
    
    def _generate_expression_statement(self, node: CSharpExpressionStatement) -> None:
        """Generate expression statement."""
        self._write_line(f"{self._expression_to_string(node.expression)};")
    
    def _generate_block_statement(self, node: CSharpBlock) -> None:
        """Generate block statement."""
        self._write_line("{")
        self._indent()
        
        for stmt in node.statements:
            self._generate_node(stmt)
        
        self._dedent()
        self._write_line("}")
    
    def _generate_if_statement(self, node: CSharpIfStatement) -> None:
        """Generate if statement."""
        condition = self._expression_to_string(node.condition)
        
        if self.options.space_before_open_brace:
            self._write_line(f"if ({condition})")
        else:
            self._write_line(f"if ({condition})")
        
        self._generate_node(node.then_statement)
        
        if node.else_statement:
            if self.options.new_line_before_else:
                self._write_line("else")
            else:
                self._write("else ")
            self._generate_node(node.else_statement)
    
    def _generate_while_statement(self, node: CSharpWhileStatement) -> None:
        """Generate while statement."""
        condition = self._expression_to_string(node.condition)
        self._write_line(f"while ({condition})")
        self._generate_node(node.body)
    
    def _generate_for_statement(self, node: CSharpForStatement) -> None:
        """Generate for statement."""
        parts = []
        
        # Initializers
        if node.initializers:
            init_parts = []
            for init in node.initializers:
                if isinstance(init, CSharpVariableDeclaration):
                    var_type = self._type_to_string(init.type) if init.type else "var"
                    init_parts.append(f"{var_type} {init.name} = {self._expression_to_string(init.initializer)}")
                else:
                    init_parts.append(self._expression_to_string(init))
            parts.append(", ".join(init_parts))
        else:
            parts.append("")
        
        # Condition
        if node.condition:
            parts.append(self._expression_to_string(node.condition))
        else:
            parts.append("")
        
        # Incrementors
        if node.incrementors:
            inc_parts = [self._expression_to_string(inc) for inc in node.incrementors]
            parts.append(", ".join(inc_parts))
        else:
            parts.append("")
        
        self._write_line(f"for ({'; '.join(parts)})")
        self._generate_node(node.body)
    
    def _generate_foreach_statement(self, node: CSharpForEachStatement) -> None:
        """Generate foreach statement."""
        var_type = self._type_to_string(node.type) if node.type else "var"
        collection = self._expression_to_string(node.collection)
        
        self._write_line(f"foreach ({var_type} {node.variable} in {collection})")
        self._generate_node(node.body)
    
    def _generate_do_statement(self, node: CSharpDoStatement) -> None:
        """Generate do-while statement."""
        self._write_line("do")
        self._generate_node(node.body)
        condition = self._expression_to_string(node.condition)
        self._write_line(f"while ({condition});")
    
    def _generate_switch_statement(self, node: CSharpSwitchStatement) -> None:
        """Generate switch statement."""
        expression = self._expression_to_string(node.expression)
        
        self._write_line(f"switch ({expression})")
        self._write_line("{")
        self._indent()
        
        for case in node.cases:
            if case.labels:
                for label in case.labels:
                    if label.value:
                        self._write_line(f"case {self._expression_to_string(label.value)}:")
                    else:
                        self._write_line("default:")
            
            self._indent()
            for stmt in case.statements:
                self._generate_node(stmt)
            self._dedent()
        
        self._dedent()
        self._write_line("}")
    
    def _generate_break_statement(self, node: CSharpBreakStatement) -> None:
        """Generate break statement."""
        self._write_line("break;")
    
    def _generate_continue_statement(self, node: CSharpContinueStatement) -> None:
        """Generate continue statement."""
        self._write_line("continue;")
    
    def _generate_return_statement(self, node: CSharpReturnStatement) -> None:
        """Generate return statement."""
        if node.expression:
            self._write_line(f"return {self._expression_to_string(node.expression)};")
        else:
            self._write_line("return;")
    
    def _generate_throw_statement(self, node: CSharpThrowStatement) -> None:
        """Generate throw statement."""
        if node.expression:
            self._write_line(f"throw {self._expression_to_string(node.expression)};")
        else:
            self._write_line("throw;")
    
    def _generate_try_statement(self, node: CSharpTryStatement) -> None:
        """Generate try statement."""
        self._write_line("try")
        self._generate_node(node.try_block)
        
        for catch_clause in node.catch_clauses:
            if catch_clause.type:
                catch_type = self._type_to_string(catch_clause.type)
                if catch_clause.identifier:
                    self._write_line(f"catch ({catch_type} {catch_clause.identifier})")
                else:
                    self._write_line(f"catch ({catch_type})")
            else:
                self._write_line("catch")
            
            if catch_clause.filter:
                self._write_line(f"when ({self._expression_to_string(catch_clause.filter)})")
            
            self._generate_node(catch_clause.block)
        
        if node.finally_block:
            self._write_line("finally")
            self._generate_node(node.finally_block)
    
    def _generate_lock_statement(self, node: CSharpLockStatement) -> None:
        """Generate lock statement."""
        expression = self._expression_to_string(node.expression)
        self._write_line(f"lock ({expression})")
        self._generate_node(node.body)
    
    def _generate_using_statement(self, node: CSharpUsingStatement) -> None:
        """Generate using statement."""
        if node.declaration:
            var_type = self._type_to_string(node.declaration.type) if node.declaration.type else "var"
            self._write_line(f"using ({var_type} {node.declaration.name} = {self._expression_to_string(node.declaration.initializer)})")
        else:
            self._write_line(f"using ({self._expression_to_string(node.expression)})")
        
        self._generate_node(node.body)
    
    def _generate_yield_statement(self, node: CSharpYieldStatement) -> None:
        """Generate yield statement."""
        if node.expression:
            self._write_line(f"yield return {self._expression_to_string(node.expression)};")
        else:
            self._write_line("yield break;")
    
    def _generate_local_declaration_statement(self, node: CSharpLocalDeclarationStatement) -> None:
        """Generate local declaration statement."""
        var_type = self._type_to_string(node.type) if node.type else "var"
        
        if node.initializer:
            self._write_line(f"{var_type} {node.name} = {self._expression_to_string(node.initializer)};")
        else:
            self._write_line(f"{var_type} {node.name};")
    
    def _generate_empty_statement(self, node: CSharpEmptyStatement) -> None:
        """Generate empty statement."""
        self._write_line(";")
    
    def _generate_labeled_statement(self, node: CSharpLabeledStatement) -> None:
        """Generate labeled statement."""
        self._write_line(f"{node.label}:")
        self._generate_node(node.statement)
    
    def _generate_goto_statement(self, node: CSharpGotoStatement) -> None:
        """Generate goto statement."""
        if node.label:
            self._write_line(f"goto {node.label};")
        elif node.case_expression:
            self._write_line(f"goto case {self._expression_to_string(node.case_expression)};")
        else:
            self._write_line("goto default;")
    
    def _generate_checked_statement(self, node: CSharpCheckedStatement) -> None:
        """Generate checked statement."""
        self._write_line("checked")
        self._generate_node(node.body)
    
    def _generate_unchecked_statement(self, node: CSharpUncheckedStatement) -> None:
        """Generate unchecked statement."""
        self._write_line("unchecked")
        self._generate_node(node.body)
    
    def _generate_unsafe_statement(self, node: CSharpUnsafeStatement) -> None:
        """Generate unsafe statement."""
        self._write_line("unsafe")
        self._generate_node(node.body)
    
    def _generate_fixed_statement(self, node: CSharpFixedStatement) -> None:
        """Generate fixed statement."""
        declarations = []
        for decl in node.declarations:
            var_type = self._type_to_string(decl.type) if decl.type else "var"
            declarations.append(f"{var_type} {decl.name} = {self._expression_to_string(decl.initializer)}")
        
        self._write_line(f"fixed ({', '.join(declarations)})")
        self._generate_node(node.body)
    
    def _generate_expression(self, node: CSharpExpression) -> str:
        """Generate expression."""
        return self._expression_to_string(node)
    
    def _expression_to_string(self, node: CSharpExpression) -> str:
        """Convert expression to string."""
        if isinstance(node, CSharpLiteral):
            return self._literal_to_string(node)
        elif isinstance(node, CSharpIdentifier):
            return node.name
        elif isinstance(node, CSharpBinaryExpression):
            return self._binary_expression_to_string(node)
        elif isinstance(node, CSharpUnaryExpression):
            return self._unary_expression_to_string(node)
        elif isinstance(node, CSharpConditionalExpression):
            return self._conditional_expression_to_string(node)
        elif isinstance(node, CSharpAssignmentExpression):
            return self._assignment_expression_to_string(node)
        elif isinstance(node, CSharpInvocationExpression):
            return self._invocation_expression_to_string(node)
        elif isinstance(node, CSharpMemberAccessExpression):
            return self._member_access_expression_to_string(node)
        elif isinstance(node, CSharpElementAccessExpression):
            return self._element_access_expression_to_string(node)
        elif isinstance(node, CSharpCastExpression):
            return self._cast_expression_to_string(node)
        elif isinstance(node, CSharpIsExpression):
            return self._is_expression_to_string(node)
        elif isinstance(node, CSharpAsExpression):
            return self._as_expression_to_string(node)
        elif isinstance(node, CSharpThisExpression):
            return "this"
        elif isinstance(node, CSharpBaseExpression):
            return "base"
        elif isinstance(node, CSharpTypeOfExpression):
            return f"typeof({self._type_to_string(node.type)})"
        elif isinstance(node, CSharpSizeOfExpression):
            return f"sizeof({self._type_to_string(node.type)})"
        elif isinstance(node, CSharpNameOfExpression):
            return f"nameof({self._expression_to_string(node.expression)})"
        elif isinstance(node, CSharpDefaultExpression):
            if node.type:
                return f"default({self._type_to_string(node.type)})"
            else:
                return "default"
        elif isinstance(node, CSharpObjectCreationExpression):
            return self._object_creation_expression_to_string(node)
        elif isinstance(node, CSharpArrayCreationExpression):
            return self._array_creation_expression_to_string(node)
        elif isinstance(node, CSharpAnonymousObjectCreationExpression):
            return self._anonymous_object_creation_expression_to_string(node)
        elif isinstance(node, CSharpLambdaExpression):
            return self._lambda_expression_to_string(node)
        elif isinstance(node, CSharpAnonymousMethodExpression):
            return self._anonymous_method_expression_to_string(node)
        elif isinstance(node, CSharpAwaitExpression):
            return f"await {self._expression_to_string(node.expression)}"
        elif isinstance(node, CSharpTupleExpression):
            return self._tuple_expression_to_string(node)
        elif isinstance(node, CSharpThrowExpression):
            return f"throw {self._expression_to_string(node.expression)}"
        elif isinstance(node, CSharpSwitchExpression):
            return self._switch_expression_to_string(node)
        elif isinstance(node, CSharpWithExpression):
            return self._with_expression_to_string(node)
        elif isinstance(node, CSharpInterpolatedStringExpression):
            return self._interpolated_string_expression_to_string(node)
        else:
            return str(node)
    
    def _literal_to_string(self, node: CSharpLiteral) -> str:
        """Convert literal to string."""
        if isinstance(node, CSharpStringLiteral):
            if node.is_verbatim:
                return f'@"{node.value}"'
            elif node.is_raw:
                return f'"""{node.value}"""'
            else:
                return f'"{node.value}"'
        elif isinstance(node, CSharpCharacterLiteral):
            return f"'{node.value}'"
        elif isinstance(node, CSharpBooleanLiteral):
            return "true" if node.value else "false"
        elif isinstance(node, CSharpNullLiteral):
            return "null"
        else:
            return str(node.value)
    
    def _binary_expression_to_string(self, node: CSharpBinaryExpression) -> str:
        """Convert binary expression to string."""
        left = self._expression_to_string(node.left)
        right = self._expression_to_string(node.right)
        
        if self.options.space_around_operators:
            return f"{left} {node.operator} {right}"
        else:
            return f"{left}{node.operator}{right}"
    
    def _unary_expression_to_string(self, node: CSharpUnaryExpression) -> str:
        """Convert unary expression to string."""
        operand = self._expression_to_string(node.operand)
        
        if node.is_prefix:
            return f"{node.operator}{operand}"
        else:
            return f"{operand}{node.operator}"
    
    def _conditional_expression_to_string(self, node: CSharpConditionalExpression) -> str:
        """Convert conditional expression to string."""
        condition = self._expression_to_string(node.condition)
        when_true = self._expression_to_string(node.when_true)
        when_false = self._expression_to_string(node.when_false)
        
        return f"{condition} ? {when_true} : {when_false}"
    
    def _assignment_expression_to_string(self, node: CSharpAssignmentExpression) -> str:
        """Convert assignment expression to string."""
        left = self._expression_to_string(node.left)
        right = self._expression_to_string(node.right)
        
        if self.options.space_around_operators:
            return f"{left} {node.operator} {right}"
        else:
            return f"{left}{node.operator}{right}"
    
    def _invocation_expression_to_string(self, node: CSharpInvocationExpression) -> str:
        """Convert invocation expression to string."""
        expression = self._expression_to_string(node.expression)
        
        args = []
        for arg in node.arguments:
            arg_str = self._expression_to_string(arg.expression)
            if arg.name:
                arg_str = f"{arg.name}: {arg_str}"
            if arg.ref_kind:
                arg_str = f"{arg.ref_kind} {arg_str}"
            args.append(arg_str)
        
        if self.options.space_within_parentheses:
            return f"{expression}( {', '.join(args)} )"
        else:
            return f"{expression}({', '.join(args)})"
    
    def _member_access_expression_to_string(self, node: CSharpMemberAccessExpression) -> str:
        """Convert member access expression to string."""
        expression = self._expression_to_string(node.expression)
        
        if node.is_conditional:
            return f"{expression}?{node.operator}{node.name}"
        else:
            return f"{expression}{node.operator}{node.name}"
    
    def _element_access_expression_to_string(self, node: CSharpElementAccessExpression) -> str:
        """Convert element access expression to string."""
        expression = self._expression_to_string(node.expression)
        
        args = [self._expression_to_string(arg) for arg in node.arguments]
        
        if node.is_conditional:
            if self.options.space_within_brackets:
                return f"{expression}?[ {', '.join(args)} ]"
            else:
                return f"{expression}?[{', '.join(args)}]"
        else:
            if self.options.space_within_brackets:
                return f"{expression}[ {', '.join(args)} ]"
            else:
                return f"{expression}[{', '.join(args)}]"
    
    def _cast_expression_to_string(self, node: CSharpCastExpression) -> str:
        """Convert cast expression to string."""
        type_str = self._type_to_string(node.type)
        expression = self._expression_to_string(node.expression)
        
        return f"({type_str}){expression}"
    
    def _is_expression_to_string(self, node: CSharpIsExpression) -> str:
        """Convert is expression to string."""
        expression = self._expression_to_string(node.expression)
        
        if node.pattern:
            pattern = self._pattern_to_string(node.pattern)
            return f"{expression} is {pattern}"
        else:
            type_str = self._type_to_string(node.type)
            return f"{expression} is {type_str}"
    
    def _as_expression_to_string(self, node: CSharpAsExpression) -> str:
        """Convert as expression to string."""
        expression = self._expression_to_string(node.expression)
        type_str = self._type_to_string(node.type)
        
        return f"{expression} as {type_str}"
    
    def _object_creation_expression_to_string(self, node: CSharpObjectCreationExpression) -> str:
        """Convert object creation expression to string."""
        if node.type:
            type_str = self._type_to_string(node.type)
        else:
            type_str = ""
        
        result = f"new {type_str}" if type_str else "new"
        
        if node.arguments:
            args = [self._expression_to_string(arg) for arg in node.arguments]
            result += f"({', '.join(args)})"
        
        if node.initializer:
            init_parts = []
            for init in node.initializer:
                if init.name:
                    init_parts.append(f"{init.name} = {self._expression_to_string(init.expression)}")
                else:
                    init_parts.append(self._expression_to_string(init.expression))
            
            result += f" {{ {', '.join(init_parts)} }}"
        
        return result
    
    def _array_creation_expression_to_string(self, node: CSharpArrayCreationExpression) -> str:
        """Convert array creation expression to string."""
        if node.type:
            type_str = self._type_to_string(node.type)
            result = f"new {type_str}"
        else:
            result = "new"
        
        if node.size_expressions:
            sizes = [self._expression_to_string(size) for size in node.size_expressions]
            result += f"[{', '.join(sizes)}]"
        else:
            result += "[]"
        
        if node.initializer:
            init_parts = [self._expression_to_string(init) for init in node.initializer]
            result += f" {{ {', '.join(init_parts)} }}"
        
        return result
    
    def _anonymous_object_creation_expression_to_string(self, node: CSharpAnonymousObjectCreationExpression) -> str:
        """Convert anonymous object creation expression to string."""
        init_parts = []
        for init in node.initializers:
            if init.name:
                init_parts.append(f"{init.name} = {self._expression_to_string(init.expression)}")
            else:
                init_parts.append(self._expression_to_string(init.expression))
        
        return f"new {{ {', '.join(init_parts)} }}"
    
    def _lambda_expression_to_string(self, node: CSharpLambdaExpression) -> str:
        """Convert lambda expression to string."""
        if len(node.parameters) == 1 and not node.parameters[0].type:
            params = node.parameters[0].name
        else:
            param_parts = []
            for param in node.parameters:
                if param.type:
                    param_parts.append(f"{self._type_to_string(param.type)} {param.name}")
                else:
                    param_parts.append(param.name)
            params = f"({', '.join(param_parts)})"
        
        if node.body:
            body = "{ " + self._statements_to_string(node.body) + " }"
        else:
            body = self._expression_to_string(node.expression)
        
        return f"{params} => {body}"
    
    def _anonymous_method_expression_to_string(self, node: CSharpAnonymousMethodExpression) -> str:
        """Convert anonymous method expression to string."""
        if node.parameters:
            param_parts = []
            for param in node.parameters:
                param_parts.append(f"{self._type_to_string(param.type)} {param.name}")
            params = f"({', '.join(param_parts)})"
        else:
            params = ""
        
        body = "{ " + self._statements_to_string(node.body) + " }"
        
        return f"delegate{params} {body}"
    
    def _tuple_expression_to_string(self, node: CSharpTupleExpression) -> str:
        """Convert tuple expression to string."""
        elements = []
        for element in node.elements:
            if element.name:
                elements.append(f"{element.name}: {self._expression_to_string(element.expression)}")
            else:
                elements.append(self._expression_to_string(element.expression))
        
        return f"({', '.join(elements)})"
    
    def _switch_expression_to_string(self, node: CSharpSwitchExpression) -> str:
        """Convert switch expression to string (C# 8.0)."""
        expression = self._expression_to_string(node.expression)
        
        arms = []
        for arm in node.arms:
            pattern = self._pattern_to_string(arm.pattern)
            result = self._expression_to_string(arm.expression)
            
            if arm.when_clause:
                when_condition = self._expression_to_string(arm.when_clause)
                arms.append(f"{pattern} when {when_condition} => {result}")
            else:
                arms.append(f"{pattern} => {result}")
        
        return f"{expression} switch {{ {', '.join(arms)} }}"
    
    def _with_expression_to_string(self, node: CSharpWithExpression) -> str:
        """Convert with expression to string (C# 9.0)."""
        expression = self._expression_to_string(node.expression)
        
        init_parts = []
        for init in node.initializers:
            init_parts.append(f"{init.name} = {self._expression_to_string(init.expression)}")
        
        return f"{expression} with {{ {', '.join(init_parts)} }}"
    
    def _interpolated_string_expression_to_string(self, node: CSharpInterpolatedStringExpression) -> str:
        """Convert interpolated string expression to string."""
        parts = []
        for part in node.parts:
            if isinstance(part, str):
                parts.append(part)
            else:
                expr = self._expression_to_string(part.expression)
                if part.alignment:
                    expr += f",{part.alignment}"
                if part.format:
                    expr += f":{part.format}"
                parts.append(f"{{{expr}}}")
        
        return f'$"{"".join(parts)}"'
    
    def _pattern_to_string(self, pattern: CSharpPattern) -> str:
        """Convert pattern to string."""
        if isinstance(pattern, CSharpConstantPattern):
            return self._expression_to_string(pattern.value)
        elif isinstance(pattern, CSharpTypePattern):
            return self._type_to_string(pattern.type)
        elif isinstance(pattern, CSharpVarPattern):
            return f"var {pattern.name}"
        elif isinstance(pattern, CSharpDeclarationPattern):
            type_str = self._type_to_string(pattern.type)
            return f"{type_str} {pattern.name}"
        elif isinstance(pattern, CSharpDiscardPattern):
            return "_"
        elif isinstance(pattern, CSharpTuplePattern):
            elements = [self._pattern_to_string(elem) for elem in pattern.elements]
            return f"({', '.join(elements)})"
        elif isinstance(pattern, CSharpPropertyPattern):
            props = []
            for prop in pattern.properties:
                props.append(f"{prop.name}: {self._pattern_to_string(prop.pattern)}")
            return f"{{ {', '.join(props)} }}"
        elif isinstance(pattern, CSharpRelationalPattern):
            return f"{pattern.operator} {self._expression_to_string(pattern.value)}"
        elif isinstance(pattern, CSharpLogicalPattern):
            left = self._pattern_to_string(pattern.left)
            right = self._pattern_to_string(pattern.right)
            return f"{left} {pattern.operator} {right}"
        else:
            return str(pattern)
    
    def _type_to_string(self, type_node: CSharpType) -> str:
        """Convert type to string."""
        if isinstance(type_node, CSharpPredefinedType):
            return type_node.name
        elif isinstance(type_node, CSharpIdentifierType):
            return type_node.name
        elif isinstance(type_node, CSharpQualifiedType):
            return f"{self._type_to_string(type_node.left)}.{type_node.right}"
        elif isinstance(type_node, CSharpGenericType):
            base_type = self._type_to_string(type_node.base_type)
            type_args = [self._type_to_string(arg) for arg in type_node.type_arguments]
            return f"{base_type}<{', '.join(type_args)}>"
        elif isinstance(type_node, CSharpArrayType):
            element_type = self._type_to_string(type_node.element_type)
            rank = "," * (type_node.rank - 1) if type_node.rank > 1 else ""
            return f"{element_type}[{rank}]"
        elif isinstance(type_node, CSharpPointerType):
            pointee_type = self._type_to_string(type_node.pointee_type)
            return f"{pointee_type}*"
        elif isinstance(type_node, CSharpNullableType):
            underlying_type = self._type_to_string(type_node.underlying_type)
            return f"{underlying_type}?"
        elif isinstance(type_node, CSharpTupleType):
            elements = []
            for element in type_node.elements:
                element_str = self._type_to_string(element.type)
                if element.name:
                    element_str = f"{element_str} {element.name}"
                elements.append(element_str)
            return f"({', '.join(elements)})"
        else:
            return str(type_node)
    
    def _parameter_to_string(self, param: CSharpParameter) -> str:
        """Convert parameter to string."""
        parts = []
        
        if param.attributes:
            attr_parts = []
            for attr in param.attributes:
                attr_parts.append(f"[{attr.name}]")
            parts.append(" ".join(attr_parts))
        
        if param.modifiers:
            parts.extend(param.modifiers)
        
        if param.type:
            parts.append(self._type_to_string(param.type))
        
        parts.append(param.name)
        
        if param.default_value:
            parts.append(f"= {self._expression_to_string(param.default_value)}")
        
        return " ".join(parts)
    
    def _attribute_to_string(self, attr: CSharpAttribute) -> str:
        """Convert attribute to string."""
        result = attr.name
        
        if attr.arguments:
            args = [self._expression_to_string(arg) for arg in attr.arguments]
            result += f"({', '.join(args)})"
        
        return result
    
    def _generate_attribute(self, attr: CSharpAttribute) -> None:
        """Generate attribute."""
        attr_str = self._attribute_to_string(attr)
        
        if attr.target:
            self._write_line(f"[{attr.target}: {attr_str}]")
        else:
            self._write_line(f"[{attr_str}]")
    
    def _statements_to_string(self, statements: List[CSharpStatement]) -> str:
        """Convert statements to string."""
        # This is a simplified version for inline use
        parts = []
        for stmt in statements:
            if isinstance(stmt, CSharpExpressionStatement):
                parts.append(f"{self._expression_to_string(stmt.expression)};")
            elif isinstance(stmt, CSharpReturnStatement):
                if stmt.expression:
                    parts.append(f"return {self._expression_to_string(stmt.expression)};")
                else:
                    parts.append("return;")
            else:
                parts.append("/* complex statement */")
        
        return " ".join(parts)
    
    def _write_line(self, text: str = "") -> None:
        """Write a line with proper indentation."""
        if text:
            indent = self._get_indent()
            self.output.append(f"{indent}{text}")
        else:
            self.output.append("")
    
    def _write(self, text: str) -> None:
        """Write text without newline."""
        if self.output:
            self.output[-1] += text
        else:
            self.output.append(text)
    
    def _get_indent(self) -> str:
        """Get current indentation string."""
        if self.options.use_tabs:
            return "\t" * self.indent_level
        else:
            return " " * (self.indent_level * self.options.indent_size)
    
    def _indent(self) -> None:
        """Increase indentation level."""
        self.indent_level += 1
    
    def _dedent(self) -> None:
        """Decrease indentation level."""
        self.indent_level = max(0, self.indent_level - 1)
    
    def _add_blank_lines(self, count: int) -> None:
        """Add blank lines."""
        for _ in range(count):
            self._write_line()


def generate_csharp(node: CSharpNode, style: CSharpCodeStyle = CSharpCodeStyle.MICROSOFT) -> str:
    """
    Generate C# code from C# AST.
    
    Args:
        node: C# AST node
        style: Code formatting style
    
    Returns:
        Generated C# code
    """
    generator = CSharpCodeGenerator(style)
    return generator.generate(node)


def generate_csharp_with_options(node: CSharpNode, options: CSharpFormattingOptions) -> str:
    """
    Generate C# code with custom formatting options.
    
    Args:
        node: C# AST node
        options: Custom formatting options
    
    Returns:
        Generated C# code
    """
    generator = CSharpCodeGenerator()
    generator.options = options
    return generator.generate(node)