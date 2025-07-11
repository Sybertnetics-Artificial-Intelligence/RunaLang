#!/usr/bin/env python3
"""
Visual Basic Code Generator Implementation

Complete code generator for Visual Basic .NET with configurable styling,
proper formatting, and Microsoft coding conventions support.
"""

from typing import List, Dict, Optional, Any, Union, Set
import logging
from dataclasses import dataclass
from enum import Enum, auto

from .visual_basic_ast import *
from ....core.error_handler import ErrorHandler, ErrorType
from ....core.translation_context import TranslationContext

class VBCodeStyle(Enum):
    """Visual Basic code style options."""
    MICROSOFT = "Microsoft"  # Microsoft coding conventions
    COMPACT = "Compact"      # Compact style for space efficiency  
    VERBOSE = "Verbose"      # Verbose style with extra spacing

@dataclass
class VBGeneratorConfig:
    """Configuration for Visual Basic code generation."""
    style: VBCodeStyle = VBCodeStyle.MICROSOFT
    indent_size: int = 4
    use_tabs: bool = False
    max_line_length: int = 120
    newline_before_brace: bool = False
    space_before_parentheses: bool = False
    space_after_comma: bool = True
    preserve_comments: bool = True
    generate_documentation: bool = True
    use_explicit_types: bool = True
    prefer_properties: bool = True

class VBCodeGenerator:
    """Visual Basic code generator."""
    
    def __init__(self, config: VBGeneratorConfig = None, error_handler: ErrorHandler = None):
        self.config = config or VBGeneratorConfig()
        self.error_handler = error_handler or ErrorHandler()
        self.logger = logging.getLogger(__name__)
        self._output: List[str] = []
        self._current_indent = 0
        self._at_line_start = True
        
    def generate(self, node: VBNode) -> str:
        """Generate Visual Basic code from AST node."""
        self._output = []
        self._current_indent = 0
        self._at_line_start = True
        
        try:
            node.accept(self)
            return '\n'.join(self._output)
        except Exception as e:
            self.error_handler.add_error(
                ErrorType.GENERATION_ERROR,
                f"Failed to generate VB code: {e}",
                0, 0
            )
            return f"' Generation error: {e}"
    
    # Visitor methods for VB AST nodes
    def visit_vb_source_unit(self, node: VBSourceUnit):
        """Generate source unit."""
        # Option statements
        for option in node.option_statements:
            option.accept(self)
            self._write_line()
        
        if node.option_statements:
            self._write_line()
        
        # Imports statements
        for imports in node.imports_statements:
            imports.accept(self)
        
        if node.imports_statements:
            self._write_line()
        
        # Global attributes
        for attr in node.global_attributes:
            attr.accept(self)
        
        if node.global_attributes:
            self._write_line()
        
        # Namespaces
        for i, namespace in enumerate(node.namespace_declarations):
            if i > 0:
                self._write_line()
            namespace.accept(self)
        
        # Type declarations
        for i, type_decl in enumerate(node.type_declarations):
            if i > 0 or node.namespace_declarations:
                self._write_line()
            type_decl.accept(self)
    
    def visit_vb_option_statement(self, node: VBOptionStatement):
        """Generate Option statement."""
        self._write(f"Option {node.option_type} {node.value}")
    
    def visit_vb_imports_statement(self, node: VBImportsStatement):
        """Generate Imports statement."""
        if node.alias:
            self._write(f"Imports {node.alias} = {node.namespace}")
        else:
            self._write(f"Imports {node.namespace}")
    
    def visit_vb_namespace(self, node: VBNamespace):
        """Generate Namespace declaration."""
        self._write(f"Namespace {node.name}")
        self._write_line()
        self._indent()
        
        # Type declarations
        for i, type_decl in enumerate(node.type_declarations):
            if i > 0:
                self._write_line()
            type_decl.accept(self)
        
        # Nested namespaces
        for namespace in node.nested_namespaces:
            self._write_line()
            namespace.accept(self)
        
        self._dedent()
        self._write("End Namespace")
    
    def visit_vb_class_declaration(self, node: VBClassDeclaration):
        """Generate Class declaration."""
        # Attributes
        for attr in node.attributes:
            attr.accept(self)
            self._write_line()
        
        # Access modifier and modifiers
        line = self._get_access_modifier_text(node.access_modifier)
        
        if node.is_partial:
            line += " Partial"
        if node.is_mustinherit:
            line += " MustInherit"
        if node.is_notinheritable:
            line += " NotInheritable"
        
        line += f" Class {node.name}"
        
        # Type parameters
        if node.type_parameters:
            params = ", ".join(tp.name for tp in node.type_parameters)
            line += f"(Of {params})"
        
        self._write(line)
        self._write_line()
        
        # Inheritance
        if node.inherits_from:
            self._indent()
            self._write(f"Inherits {node.inherits_from}")
            self._write_line()
            self._dedent()
        
        # Implements
        if node.implements:
            self._indent()
            implements_text = ", ".join(node.implements)
            self._write(f"Implements {implements_text}")
            self._write_line()
            self._dedent()
        
        if node.inherits_from or node.implements:
            self._write_line()
        
        self._indent()
        
        # Members
        for i, member in enumerate(node.members):
            if i > 0:
                self._write_line()
            member.accept(self)
        
        self._dedent()
        self._write("End Class")
    
    def visit_vb_module_declaration(self, node: VBModuleDeclaration):
        """Generate Module declaration."""
        # Attributes
        for attr in node.attributes:
            attr.accept(self)
            self._write_line()
        
        # Access modifier
        line = self._get_access_modifier_text(node.access_modifier)
        line += f" Module {node.name}"
        
        self._write(line)
        self._write_line()
        self._indent()
        
        # Members
        for i, member in enumerate(node.members):
            if i > 0:
                self._write_line()
            member.accept(self)
        
        self._dedent()
        self._write("End Module")
    
    def visit_vb_interface_declaration(self, node: VBInterfaceDeclaration):
        """Generate Interface declaration."""
        # Attributes
        for attr in node.attributes:
            attr.accept(self)
            self._write_line()
        
        # Access modifier
        line = self._get_access_modifier_text(node.access_modifier)
        line += f" Interface {node.name}"
        
        # Type parameters
        if node.type_parameters:
            params = ", ".join(tp.name for tp in node.type_parameters)
            line += f"(Of {params})"
        
        self._write(line)
        self._write_line()
        
        # Inheritance
        if node.inherits_from:
            self._indent()
            inherits_text = ", ".join(node.inherits_from)
            self._write(f"Inherits {inherits_text}")
            self._write_line()
            self._dedent()
            self._write_line()
        
        self._indent()
        
        # Members
        for i, member in enumerate(node.members):
            if i > 0:
                self._write_line()
            member.accept(self)
        
        self._dedent()
        self._write("End Interface")
    
    def visit_vb_structure_declaration(self, node: VBStructureDeclaration):
        """Generate Structure declaration."""
        # Access modifier
        line = self._get_access_modifier_text(node.access_modifier)
        line += f" Structure {node.name}"
        
        # Type parameters
        if node.type_parameters:
            params = ", ".join(tp.name for tp in node.type_parameters)
            line += f"(Of {params})"
        
        self._write(line)
        self._write_line()
        
        # Implements
        if node.implements:
            self._indent()
            implements_text = ", ".join(node.implements)
            self._write(f"Implements {implements_text}")
            self._write_line()
            self._dedent()
            self._write_line()
        
        self._indent()
        
        # Members
        for i, member in enumerate(node.members):
            if i > 0:
                self._write_line()
            member.accept(self)
        
        self._dedent()
        self._write("End Structure")
    
    def visit_vb_enum_declaration(self, node: VBEnumDeclaration):
        """Generate Enum declaration."""
        # Access modifier
        line = self._get_access_modifier_text(node.access_modifier)
        line += f" Enum {node.name}"
        
        # Underlying type
        if node.underlying_type:
            line += f" As {self._get_type_text(node.underlying_type)}"
        
        self._write(line)
        self._write_line()
        self._indent()
        
        # Members
        for i, member in enumerate(node.members):
            if i > 0:
                self._write_line()
            member.accept(self)
        
        self._dedent()
        self._write("End Enum")
    
    def visit_vb_enum_member(self, node: VBEnumMember):
        """Generate Enum member."""
        line = node.name
        if node.value:
            line += " = "
            node.value.accept(self)
            line += self._output.pop()  # Get the last generated text
        self._write(line)
    
    def visit_vb_method_declaration(self, node: VBMethodDeclaration):
        """Generate Method declaration."""
        # Attributes
        for attr in node.attributes:
            attr.accept(self)
            self._write_line()
        
        # Access modifier and member modifiers
        line = self._get_access_modifier_text(node.access_modifier)
        
        for modifier in node.member_modifiers:
            line += f" {modifier.value}"
        
        # Sub or Function
        if node.is_function:
            line += " Function"
        else:
            line += " Sub"
        
        line += f" {node.name}"
        
        # Type parameters
        if node.type_parameters:
            params = ", ".join(tp.name for tp in node.type_parameters)
            line += f"(Of {params})"
        
        # Parameters
        line += "("
        if node.parameters:
            param_texts = []
            for param in node.parameters:
                param_texts.append(self._get_parameter_text(param))
            line += ", ".join(param_texts)
        line += ")"
        
        # Return type
        if node.return_type and node.is_function:
            line += f" As {self._get_type_text(node.return_type)}"
        
        # Handles clause
        if node.handles_clause:
            line += f" Handles {', '.join(node.handles_clause)}"
        
        # Implements clause
        if node.implements_clause:
            line += f" Implements {', '.join(node.implements_clause)}"
        
        self._write(line)
        self._write_line()
        
        # Body
        if node.body:
            self._indent()
            for stmt in node.body:
                stmt.accept(self)
                self._write_line()
            self._dedent()
        
        # End Sub/Function
        if node.is_function:
            self._write("End Function")
        else:
            self._write("End Sub")
    
    def visit_vb_property_declaration(self, node: VBPropertyDeclaration):
        """Generate Property declaration."""
        # Attributes
        for attr in node.attributes:
            attr.accept(self)
            self._write_line()
        
        # Access modifier and member modifiers
        line = self._get_access_modifier_text(node.access_modifier)
        
        for modifier in node.member_modifiers:
            line += f" {modifier.value}"
        
        line += f" Property {node.name}"
        
        # Parameters (for indexed properties)
        if node.parameters:
            line += "("
            param_texts = []
            for param in node.parameters:
                param_texts.append(self._get_parameter_text(param))
            line += ", ".join(param_texts)
            line += ")"
        
        # Type
        if node.property_type:
            line += f" As {self._get_type_text(node.property_type)}"
        
        # Auto-implemented property with initial value
        if node.auto_implemented:
            if node.initial_value:
                line += " = "
                node.initial_value.accept(self)
                line += self._output.pop()  # Get the last generated text
            self._write(line)
        else:
            self._write(line)
            self._write_line()
            self._indent()
            
            # Getter
            if node.getter:
                node.getter.accept(self)
                self._write_line()
            
            # Setter
            if node.setter:
                node.setter.accept(self)
                self._write_line()
            
            self._dedent()
            self._write("End Property")
    
    def visit_vb_accessor_declaration(self, node: VBAccessorDeclaration):
        """Generate Property accessor."""
        if node.is_getter:
            line = "Get"
        else:
            line = "Set"
        
        if node.access_modifier:
            line = f"{self._get_access_modifier_text(node.access_modifier)} {line}"
        
        self._write(line)
        self._write_line()
        
        if node.body:
            self._indent()
            for stmt in node.body:
                stmt.accept(self)
                self._write_line()
            self._dedent()
        
        if node.is_getter:
            self._write("End Get")
        else:
            self._write("End Set")
    
    def visit_vb_field_declaration(self, node: VBFieldDeclaration):
        """Generate Field declaration."""
        # Attributes
        for attr in node.attributes:
            attr.accept(self)
            self._write_line()
        
        # Access modifier and member modifiers
        line = self._get_access_modifier_text(node.access_modifier)
        
        for modifier in node.member_modifiers:
            line += f" {modifier.value}"
        
        if node.is_constant:
            line += " Const"
        else:
            line += " Dim"
        
        line += f" {node.name}"
        
        # Type
        if node.field_type:
            line += f" As {self._get_type_text(node.field_type)}"
        
        # Initial value
        if node.initial_value:
            line += " = "
            node.initial_value.accept(self)
            line += self._output.pop()  # Get the last generated text
        
        self._write(line)
    
    def visit_vb_binary_expression(self, node: VBBinaryExpression):
        """Generate Binary expression."""
        node.left.accept(self)
        left_text = self._output.pop()
        
        node.right.accept(self)
        right_text = self._output.pop()
        
        operator_text = self._get_operator_text(node.operator)
        
        if self.config.space_after_comma:
            result = f"{left_text} {operator_text} {right_text}"
        else:
            result = f"{left_text}{operator_text}{right_text}"
        
        self._output.append(result)
    
    def visit_vb_literal_expression(self, node: VBLiteralExpression):
        """Generate Literal expression."""
        if node.literal_type == "String":
            self._output.append(f'"{node.value}"')
        elif node.literal_type == "Boolean":
            self._output.append("True" if node.value else "False")
        elif node.literal_type == "Nothing":
            self._output.append("Nothing")
        else:
            self._output.append(str(node.value))
    
    def visit_vb_identifier_expression(self, node: VBIdentifierExpression):
        """Generate Identifier expression."""
        self._output.append(node.name)
    
    def visit_vb_member_access_expression(self, node: VBMemberAccessExpression):
        """Generate Member access expression."""
        node.expression.accept(self)
        expr_text = self._output.pop()
        self._output.append(f"{expr_text}.{node.member_name}")
    
    def visit_vb_invocation_expression(self, node: VBInvocationExpression):
        """Generate Method invocation expression."""
        node.expression.accept(self)
        expr_text = self._output.pop()
        
        args = []
        for arg in node.arguments:
            arg.accept(self)
            args.append(self._output.pop())
        
        args_text = ", ".join(args)
        self._output.append(f"{expr_text}({args_text})")
    
    def visit_vb_argument(self, node: VBArgument):
        """Generate Method argument."""
        result = ""
        
        if node.name:
            result += f"{node.name}:="
        
        node.expression.accept(self)
        result += self._output.pop()
        
        self._output.append(result)
    
    def visit_vb_attribute(self, node: VBAttribute):
        """Generate Attribute."""
        line = f"<{node.name}"
        
        if node.arguments:
            args = []
            for arg in node.arguments:
                arg.accept(self)
                args.append(self._output.pop())
            line += f"({', '.join(args)})"
        
        line += ">"
        self._write(line)
    
    def visit_vb_comment(self, node: VBComment):
        """Generate Comment."""
        self._write(f"' {node.text}")
    
    # Helper methods
    def _get_access_modifier_text(self, modifier: VBAccessModifier) -> str:
        """Get access modifier text."""
        return modifier.value
    
    def _get_operator_text(self, operator: VBOperator) -> str:
        """Get operator text."""
        return operator.value
    
    def _get_type_text(self, vb_type: VBType) -> str:
        """Get type text."""
        if isinstance(vb_type, VBNamedType):
            result = vb_type.name
            if vb_type.type_arguments:
                args = [self._get_type_text(arg) for arg in vb_type.type_arguments]
                result += f"(Of {', '.join(args)})"
            if vb_type.is_nullable:
                result += "?"
            return result
        elif isinstance(vb_type, VBArrayType):
            element_text = self._get_type_text(vb_type.element_type)
            if vb_type.rank == 1:
                return f"{element_text}()"
            else:
                commas = "," * (vb_type.rank - 1)
                return f"{element_text}({commas})"
        else:
            return "Object"
    
    def _get_parameter_text(self, param: VBParameter) -> str:
        """Get parameter text."""
        result = ""
        
        if param.is_optional:
            result += "Optional "
        
        if param.is_byref:
            result += "ByRef "
        else:
            result += "ByVal "
        
        if param.is_paramarray:
            result += "ParamArray "
        
        result += param.name
        
        if param.parameter_type:
            result += f" As {self._get_type_text(param.parameter_type)}"
        
        if param.default_value:
            param.default_value.accept(self)
            result += f" = {self._output.pop()}"
        
        return result
    
    def _write(self, text: str):
        """Write text to output."""
        if self._at_line_start and text.strip():
            self._output.append(" " * (self._current_indent * self.config.indent_size) + text)
            self._at_line_start = False
        elif text.strip():
            if self._output:
                self._output[-1] += text
            else:
                self._output.append(text)
    
    def _write_line(self, text: str = ""):
        """Write line to output."""
        if text:
            self._write(text)
        if not self._at_line_start:
            self._output.append("")
        self._at_line_start = True
    
    def _indent(self):
        """Increase indentation."""
        self._current_indent += 1
    
    def _dedent(self):
        """Decrease indentation."""
        self._current_indent = max(0, self._current_indent - 1)

def generate_visual_basic(node: VBNode, config: VBGeneratorConfig = None) -> str:
    """Generate Visual Basic code from AST node."""
    generator = VBCodeGenerator(config)
    return generator.generate(node)

def format_visual_basic_code(code: str, config: VBGeneratorConfig = None) -> str:
    """Format Visual Basic code."""
    # This would typically involve parsing and regenerating
    # For now, just return the code as-is
    return code 