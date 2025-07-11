#!/usr/bin/env python3
"""
GraphQL Code Generator

Generates clean, properly formatted GraphQL source code from GraphQL AST nodes.
Supports all GraphQL language features including:
- Operations: query, mutation, subscription
- Type definitions: object, interface, union, enum, input, scalar
- Selections: fields, fragments, inline fragments
- Arguments, variables, directives
- Values and literals
- Schema definitions
- Proper GraphQL formatting and style conventions
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass
from io import StringIO

from .graphql_ast import *


@dataclass
class GraphQLGeneratorOptions:
    """Options for GraphQL code generation."""
    indent_size: int = 2
    use_tabs: bool = False
    max_line_length: int = 120
    format_multiline: bool = True
    add_comments: bool = True
    
    # GraphQL-specific options
    operation_comments: bool = True
    type_comments: bool = True
    field_comments: bool = True
    sort_fields: bool = False
    compact_arguments: bool = False


class GraphQLCodeGenerator:
    """GraphQL code generator for producing clean GraphQL source code."""
    
    def __init__(self, options: GraphQLGeneratorOptions = None):
        self.options = options or GraphQLGeneratorOptions()
        self.output = StringIO()
        self.indent_level = 0
        self.current_line_empty = True
        
    def generate(self, node: GraphQLNode) -> str:
        """Generate GraphQL code from AST node."""
        self.output = StringIO()
        self.indent_level = 0
        self.current_line_empty = True
        
        self.visit(node)
        
        result = self.output.getvalue()
        self.output.close()
        
        return result
    
    def visit(self, node: GraphQLNode):
        """Visit AST node and generate code."""
        if node is None:
            return
        
        method_name = f"visit_{node.__class__.__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        visitor(node)
    
    def generic_visit(self, node: GraphQLNode):
        """Generic visitor for unknown nodes."""
        self.write(f"# Unknown node: {node.__class__.__name__}")
    
    def write(self, text: str):
        """Write text to output."""
        if text == "":
            return
        
        if self.current_line_empty and text.strip():
            self.write_indent()
        
        self.output.write(text)
        self.current_line_empty = False
    
    def writeln(self, text: str = ""):
        """Write line to output."""
        if text:
            self.write(text)
        self.output.write("\n")
        self.current_line_empty = True
    
    def write_indent(self):
        """Write current indentation."""
        if self.options.use_tabs:
            self.output.write("\t" * self.indent_level)
        else:
            self.output.write(" " * (self.indent_level * self.options.indent_size))
    
    def indent(self):
        """Increase indentation level."""
        self.indent_level += 1
    
    def dedent(self):
        """Decrease indentation level."""
        self.indent_level = max(0, self.indent_level - 1)
    
    def write_block(self, content_fn):
        """Write a block with braces and proper indentation."""
        self.writeln(" {")
        self.indent()
        content_fn()
        self.dedent()
        self.write("}")
    
    # Node visitors
    
    def visit_GraphQLDocument(self, node: GraphQLDocument):
        """Generate code for GraphQL document."""
        for i, definition in enumerate(node.definitions):
            if i > 0:
                self.writeln()
                self.writeln()
            self.visit(definition)
    
    def visit_GraphQLOperationDefinition(self, node: GraphQLOperationDefinition):
        """Generate operation definition."""
        if self.options.operation_comments:
            op_type_name = node.operation_type.name.lower()
            self.writeln(f"# {op_type_name.title()} operation")
        
        # Operation type
        self.write(node.operation_type.name.lower())
        
        # Operation name
        if node.name:
            self.write(f" {node.name}")
        
        # Variable definitions
        if node.variable_definitions:
            self.write("(")
            for i, var_def in enumerate(node.variable_definitions):
                if i > 0:
                    self.write(", ")
                self.visit(var_def)
            self.write(")")
        
        # Directives
        if node.directives:
            self.write(" ")
            self.write_directives(node.directives)
        
        # Selection set
        if node.selection_set:
            self.visit(node.selection_set)
    
    def visit_GraphQLFragmentDefinition(self, node: GraphQLFragmentDefinition):
        """Generate fragment definition."""
        if self.options.operation_comments:
            self.writeln(f"# Fragment for {node.type_condition}")
        
        self.write(f"fragment {node.name} on {node.type_condition}")
        
        if node.directives:
            self.write(" ")
            self.write_directives(node.directives)
        
        if node.selection_set:
            self.visit(node.selection_set)
    
    def visit_GraphQLSelectionSet(self, node: GraphQLSelectionSet):
        """Generate selection set."""
        def write_selections():
            for i, selection in enumerate(node.selections):
                if i > 0:
                    self.writeln()
                self.visit(selection)
        
        self.write_block(write_selections)
    
    def visit_GraphQLField(self, node: GraphQLField):
        """Generate field selection."""
        # Alias
        if node.alias:
            self.write(f"{node.alias}: ")
        
        # Field name
        self.write(node.name)
        
        # Arguments
        if node.arguments:
            self.write("(")
            if self.options.compact_arguments or len(node.arguments) <= 2:
                for i, arg in enumerate(node.arguments):
                    if i > 0:
                        self.write(", ")
                    self.visit(arg)
            else:
                self.writeln()
                self.indent()
                for i, arg in enumerate(node.arguments):
                    if i > 0:
                        self.writeln()
                    self.visit(arg)
                self.dedent()
                self.writeln()
            self.write(")")
        
        # Directives
        if node.directives:
            self.write(" ")
            self.write_directives(node.directives)
        
        # Nested selection set
        if node.selection_set:
            self.write(" ")
            self.visit(node.selection_set)
    
    def visit_GraphQLFragmentSpread(self, node: GraphQLFragmentSpread):
        """Generate fragment spread."""
        self.write(f"...{node.name}")
        
        if node.directives:
            self.write(" ")
            self.write_directives(node.directives)
    
    def visit_GraphQLInlineFragment(self, node: GraphQLInlineFragment):
        """Generate inline fragment."""
        self.write("...")
        
        if node.type_condition:
            self.write(f" on {node.type_condition}")
        
        if node.directives:
            self.write(" ")
            self.write_directives(node.directives)
        
        if node.selection_set:
            self.write(" ")
            self.visit(node.selection_set)
    
    def visit_GraphQLArgument(self, node: GraphQLArgument):
        """Generate argument."""
        self.write(f"{node.name}: ")
        self.visit(node.value)
    
    def visit_GraphQLVariableDefinition(self, node: GraphQLVariableDefinition):
        """Generate variable definition."""
        self.visit(node.variable)
        self.write(f": {node.type}")
        
        if node.default_value is not None:
            self.write(" = ")
            self.visit(node.default_value)
    
    def visit_GraphQLVariable(self, node: GraphQLVariable):
        """Generate variable reference."""
        self.write(f"${node.name}")
    
    # Value nodes
    
    def visit_GraphQLIntValue(self, node: GraphQLIntValue):
        """Generate integer value."""
        self.write(str(node.value))
    
    def visit_GraphQLFloatValue(self, node: GraphQLFloatValue):
        """Generate float value."""
        self.write(str(node.value))
    
    def visit_GraphQLStringValue(self, node: GraphQLStringValue):
        """Generate string value."""
        # Escape quotes and special characters
        escaped = node.value.replace('"', '\\"').replace('\n', '\\n').replace('\t', '\\t')
        self.write(f'"{escaped}"')
    
    def visit_GraphQLBooleanValue(self, node: GraphQLBooleanValue):
        """Generate boolean value."""
        self.write("true" if node.value else "false")
    
    def visit_GraphQLNullValue(self, node: GraphQLNullValue):
        """Generate null value."""
        self.write("null")
    
    def visit_GraphQLEnumValue(self, node: GraphQLEnumValue):
        """Generate enum value."""
        self.write(node.value)
    
    def visit_GraphQLListValue(self, node: GraphQLListValue):
        """Generate list value."""
        self.write("[")
        for i, value in enumerate(node.values):
            if i > 0:
                self.write(", ")
            self.visit(value)
        self.write("]")
    
    def visit_GraphQLObjectValue(self, node: GraphQLObjectValue):
        """Generate object value."""
        if not node.fields:
            self.write("{}")
            return
        
        self.write("{ ")
        for i, field in enumerate(node.fields):
            if i > 0:
                self.write(", ")
            self.visit(field)
        self.write(" }")
    
    def visit_GraphQLObjectField(self, node: GraphQLObjectField):
        """Generate object field."""
        self.write(f"{node.name}: ")
        self.visit(node.value)
    
    # Directive
    
    def visit_GraphQLDirective(self, node: GraphQLDirective):
        """Generate directive."""
        self.write(f"@{node.name}")
        
        if node.arguments:
            self.write("(")
            for i, arg in enumerate(node.arguments):
                if i > 0:
                    self.write(", ")
                self.visit(arg)
            self.write(")")
    
    def write_directives(self, directives: List[GraphQLDirective]):
        """Write multiple directives."""
        for i, directive in enumerate(directives):
            if i > 0:
                self.write(" ")
            self.visit(directive)
    
    # Type system definitions
    
    def visit_GraphQLObjectTypeDefinition(self, node: GraphQLObjectTypeDefinition):
        """Generate object type definition."""
        if self.options.type_comments:
            self.writeln(f"# Object type: {node.name}")
        
        self.write(f"type {node.name}")
        
        # Implements interfaces
        if node.interfaces:
            self.write(" implements ")
            for i, interface in enumerate(node.interfaces):
                if i > 0:
                    self.write(" & ")
                self.write(interface)
        
        # Directives
        if node.directives:
            self.write(" ")
            self.write_directives(node.directives)
        
        # Fields
        if node.fields:
            def write_fields():
                for i, field in enumerate(node.fields):
                    if i > 0:
                        self.writeln()
                    self.visit(field)
            
            self.write_block(write_fields)
        else:
            self.write(" {}")
    
    def visit_GraphQLFieldDefinition(self, node: GraphQLFieldDefinition):
        """Generate field definition."""
        if self.options.field_comments and hasattr(node, 'description'):
            self.writeln(f"# {node.description}")
        
        self.write(node.name)
        
        # Arguments
        if node.arguments:
            self.write("(")
            for i, arg in enumerate(node.arguments):
                if i > 0:
                    self.write(", ")
                self.visit(arg)
            self.write(")")
        
        self.write(f": {node.type}")
        
        # Directives
        if node.directives:
            self.write(" ")
            self.write_directives(node.directives)
    
    def visit_GraphQLInputValueDefinition(self, node: GraphQLInputValueDefinition):
        """Generate input value definition."""
        self.write(f"{node.name}: {node.type}")
        
        if node.default_value is not None:
            self.write(" = ")
            self.visit(node.default_value)
        
        if node.directives:
            self.write(" ")
            self.write_directives(node.directives)
    
    def visit_GraphQLInterfaceTypeDefinition(self, node: GraphQLInterfaceTypeDefinition):
        """Generate interface type definition."""
        if self.options.type_comments:
            self.writeln(f"# Interface type: {node.name}")
        
        self.write(f"interface {node.name}")
        
        if node.directives:
            self.write(" ")
            self.write_directives(node.directives)
        
        if node.fields:
            def write_fields():
                for i, field in enumerate(node.fields):
                    if i > 0:
                        self.writeln()
                    self.visit(field)
            
            self.write_block(write_fields)
        else:
            self.write(" {}")
    
    def visit_GraphQLUnionTypeDefinition(self, node: GraphQLUnionTypeDefinition):
        """Generate union type definition."""
        if self.options.type_comments:
            self.writeln(f"# Union type: {node.name}")
        
        self.write(f"union {node.name}")
        
        if node.directives:
            self.write(" ")
            self.write_directives(node.directives)
        
        if node.types:
            self.write(" = ")
            for i, type_name in enumerate(node.types):
                if i > 0:
                    self.write(" | ")
                self.write(type_name)
    
    def visit_GraphQLEnumTypeDefinition(self, node: GraphQLEnumTypeDefinition):
        """Generate enum type definition."""
        if self.options.type_comments:
            self.writeln(f"# Enum type: {node.name}")
        
        self.write(f"enum {node.name}")
        
        if node.directives:
            self.write(" ")
            self.write_directives(node.directives)
        
        if node.values:
            def write_values():
                for i, value in enumerate(node.values):
                    if i > 0:
                        self.writeln()
                    self.write(value)
            
            self.write_block(write_values)
        else:
            self.write(" {}")
    
    def visit_GraphQLInputObjectTypeDefinition(self, node: GraphQLInputObjectTypeDefinition):
        """Generate input object type definition."""
        if self.options.type_comments:
            self.writeln(f"# Input type: {node.name}")
        
        self.write(f"input {node.name}")
        
        if node.directives:
            self.write(" ")
            self.write_directives(node.directives)
        
        if node.fields:
            def write_fields():
                for i, field in enumerate(node.fields):
                    if i > 0:
                        self.writeln()
                    self.visit(field)
            
            self.write_block(write_fields)
        else:
            self.write(" {}")
    
    def visit_GraphQLScalarTypeDefinition(self, node: GraphQLScalarTypeDefinition):
        """Generate scalar type definition."""
        if self.options.type_comments:
            self.writeln(f"# Scalar type: {node.name}")
        
        self.write(f"scalar {node.name}")
        
        if node.directives:
            self.write(" ")
            self.write_directives(node.directives)
    
    def visit_GraphQLName(self, node: GraphQLName):
        """Generate name."""
        self.write(node.value)


# Public API functions
def generate_graphql_code(node: GraphQLNode, options: GraphQLGeneratorOptions = None) -> str:
    """Generate GraphQL code from AST node."""
    generator = GraphQLCodeGenerator(options)
    return generator.generate(node)

def format_graphql_code(code: str) -> str:
    """Format GraphQL code (basic formatting)."""
    # Basic formatting - could be enhanced with more sophisticated formatting
    lines = code.split('\n')
    formatted_lines = []
    indent_level = 0
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            formatted_lines.append('')
            continue
        
        # Adjust indent for closing braces
        if stripped.startswith('}'):
            indent_level = max(0, indent_level - 1)
        
        # Add line with proper indentation
        formatted_lines.append('  ' * indent_level + stripped)
        
        # Adjust indent for opening braces
        if stripped.endswith('{'):
            indent_level += 1
    
    return '\n'.join(formatted_lines) 