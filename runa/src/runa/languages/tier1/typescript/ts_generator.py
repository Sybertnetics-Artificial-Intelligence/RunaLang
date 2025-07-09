#!/usr/bin/env python3
"""
TypeScript Code Generator

Generates TypeScript source code from TypeScript AST nodes.
Supports all TypeScript features including type annotations, generics,
interfaces, and modern language constructs.
"""

from typing import List, Dict, Any, Optional
from io import StringIO
import re

from .ts_ast import *


class TSCodeGenerator:
    """TypeScript code generator with proper formatting."""
    
    def __init__(self, indent_size: int = 2, use_semicolons: bool = True, use_trailing_comma: bool = True):
        self.indent_size = indent_size
        self.use_semicolons = use_semicolons
        self.use_trailing_comma = use_trailing_comma
        self.current_indent = 0
        self.output = StringIO()
        self.needs_semicolon = False
    
    def generate(self, node: TSNode) -> str:
        """Generate TypeScript code from AST node."""
        self.output = StringIO()
        self.current_indent = 0
        self.needs_semicolon = False
        
        self._visit_node(node)
        
        result = self.output.getvalue()
        self.output.close()
        return result
    
    def _visit_node(self, node: TSNode):
        """Visit a node and generate code."""
        if isinstance(node, TSProgram):
            self._visit_program(node)
        
        elif isinstance(node, TSLiteral):
            self._visit_literal(node)
        
        elif isinstance(node, TSIdentifier):
            self._visit_identifier(node)
        
        elif isinstance(node, TSTypeAnnotation):
            self._visit_type_annotation(node)
        
        elif isinstance(node, TSTypeReference):
            self._visit_type_reference(node)
        
        elif isinstance(node, TSUnionType):
            self._visit_union_type(node)
        
        elif isinstance(node, TSIntersectionType):
            self._visit_intersection_type(node)
        
        elif isinstance(node, TSTupleType):
            self._visit_tuple_type(node)
        
        elif isinstance(node, TSArrayType):
            self._visit_array_type(node)
        
        elif isinstance(node, TSFunctionType):
            self._visit_function_type(node)
        
        elif isinstance(node, TSTypeLiteral):
            self._visit_type_literal(node)
        
        elif isinstance(node, TSTypeParameter):
            self._visit_type_parameter(node)
        
        elif isinstance(node, TSTypeAssertion):
            self._visit_type_assertion(node)
        
        elif isinstance(node, TSParameter):
            self._visit_parameter(node)
        
        elif isinstance(node, TSVariableDeclaration):
            self._visit_variable_declaration(node)
        
        elif isinstance(node, TSVariableDeclarator):
            self._visit_variable_declarator(node)
        
        elif isinstance(node, TSFunctionDeclaration):
            self._visit_function_declaration(node)
        
        elif isinstance(node, TSInterfaceDeclaration):
            self._visit_interface_declaration(node)
        
        elif isinstance(node, TSTypeAliasDeclaration):
            self._visit_type_alias_declaration(node)
        
        elif isinstance(node, TSEnumDeclaration):
            self._visit_enum_declaration(node)
        
        elif isinstance(node, TSEnumMember):
            self._visit_enum_member(node)
        
        elif isinstance(node, TSClassDeclaration):
            self._visit_class_declaration(node)
        
        elif isinstance(node, TSNamespaceDeclaration):
            self._visit_namespace_declaration(node)
        
        elif isinstance(node, TSMethodSignature):
            self._visit_method_signature(node)
        
        elif isinstance(node, TSPropertySignature):
            self._visit_property_signature(node)
        
        elif isinstance(node, TSBlockStatement):
            self._visit_block_statement(node)
        
        else:
            self._write(f"/* Unknown node type: {type(node)} */")
    
    def _visit_program(self, node: TSProgram):
        """Visit program node."""
        for i, stmt in enumerate(node.body):
            if i > 0:
                self._write_line()
            self._visit_node(stmt)
    
    def _visit_literal(self, node: TSLiteral):
        """Visit literal node."""
        if node.literal_type == TSLiteralType.NULL:
            self._write("null")
        elif node.literal_type == TSLiteralType.UNDEFINED:
            self._write("undefined")
        elif node.literal_type == TSLiteralType.BOOLEAN:
            self._write("true" if node.value else "false")
        elif node.literal_type == TSLiteralType.NUMBER:
            self._write(str(node.value))
        elif node.literal_type == TSLiteralType.STRING:
            self._write(f'"{node.value}"')
        elif node.literal_type == TSLiteralType.BIGINT:
            self._write(f"{node.value}n")
        elif node.literal_type == TSLiteralType.TEMPLATE:
            self._write(f"`{node.value}`")
        else:
            self._write(node.raw)
    
    def _visit_identifier(self, node: TSIdentifier):
        """Visit identifier node."""
        self._write(node.name)
    
    def _visit_type_annotation(self, node: TSTypeAnnotation):
        """Visit type annotation node."""
        self._write(": ")
        self._visit_node(node.type_annotation)
    
    def _visit_type_reference(self, node: TSTypeReference):
        """Visit type reference node."""
        self._visit_node(node.type_name)
        
        if node.type_arguments:
            self._write("<")
            for i, arg in enumerate(node.type_arguments):
                if i > 0:
                    self._write(", ")
                self._visit_node(arg)
            self._write(">")
    
    def _visit_union_type(self, node: TSUnionType):
        """Visit union type node."""
        for i, type_node in enumerate(node.types):
            if i > 0:
                self._write(" | ")
            self._visit_node(type_node)
    
    def _visit_intersection_type(self, node: TSIntersectionType):
        """Visit intersection type node."""
        for i, type_node in enumerate(node.types):
            if i > 0:
                self._write(" & ")
            self._visit_node(type_node)
    
    def _visit_tuple_type(self, node: TSTupleType):
        """Visit tuple type node."""
        self._write("[")
        for i, element_type in enumerate(node.element_types):
            if i > 0:
                self._write(", ")
            self._visit_node(element_type)
        self._write("]")
    
    def _visit_array_type(self, node: TSArrayType):
        """Visit array type node."""
        self._visit_node(node.element_type)
        self._write("[]")
    
    def _visit_function_type(self, node: TSFunctionType):
        """Visit function type node."""
        if node.type_parameters:
            self._write("<")
            for i, param in enumerate(node.type_parameters):
                if i > 0:
                    self._write(", ")
                self._visit_node(param)
            self._write(">")
        
        self._write("(")
        for i, param in enumerate(node.parameters):
            if i > 0:
                self._write(", ")
            self._visit_node(param)
        self._write(") => ")
        self._visit_node(node.return_type)
    
    def _visit_type_literal(self, node: TSTypeLiteral):
        """Visit type literal node."""
        self._write("{")
        if node.members:
            self._write_line()
            self._indent()
            for i, member in enumerate(node.members):
                if i > 0:
                    self._write_line()
                self._write_indent()
                self._visit_node(member)
                if self.use_semicolons:
                    self._write(";")
            self._dedent()
            self._write_line()
            self._write_indent()
        self._write("}")
    
    def _visit_type_parameter(self, node: TSTypeParameter):
        """Visit type parameter node."""
        self._visit_node(node.name)
        
        if node.constraint:
            self._write(" extends ")
            self._visit_node(node.constraint)
        
        if node.default_type:
            self._write(" = ")
            self._visit_node(node.default_type)
    
    def _visit_type_assertion(self, node: TSTypeAssertion):
        """Visit type assertion node."""
        self._visit_node(node.expression)
        self._write(" as ")
        self._visit_node(node.type_annotation)
    
    def _visit_parameter(self, node: TSParameter):
        """Visit parameter node."""
        # Access modifiers
        if node.access_modifier:
            self._write(f"{node.access_modifier.value} ")
        
        if node.readonly:
            self._write("readonly ")
        
        if node.rest:
            self._write("...")
        
        self._visit_node(node.name)
        
        if node.optional:
            self._write("?")
        
        if node.type_annotation:
            self._visit_node(node.type_annotation)
        
        if node.default_value:
            self._write(" = ")
            self._visit_node(node.default_value)
    
    def _visit_variable_declaration(self, node: TSVariableDeclaration):
        """Visit variable declaration node."""
        self._write(f"{node.kind.value} ")
        
        for i, declarator in enumerate(node.declarations):
            if i > 0:
                self._write(", ")
            self._visit_node(declarator)
        
        if self.use_semicolons:
            self._write(";")
    
    def _visit_variable_declarator(self, node: TSVariableDeclarator):
        """Visit variable declarator node."""
        self._visit_node(node.id)
        
        if node.type_annotation:
            self._visit_node(node.type_annotation)
        
        if node.init:
            self._write(" = ")
            self._visit_node(node.init)
    
    def _visit_function_declaration(self, node: TSFunctionDeclaration):
        """Visit function declaration node."""
        if node.async_:
            self._write("async ")
        
        self._write("function")
        
        if node.generator:
            self._write("*")
        
        self._write(" ")
        self._visit_node(node.name)
        
        if node.type_parameters:
            self._write("<")
            for i, param in enumerate(node.type_parameters):
                if i > 0:
                    self._write(", ")
                self._visit_node(param)
            self._write(">")
        
        self._write("(")
        for i, param in enumerate(node.parameters):
            if i > 0:
                self._write(", ")
            self._visit_node(param)
        self._write(")")
        
        if node.return_type:
            self._visit_node(node.return_type)
        
        self._write(" ")
        self._visit_node(node.body)
    
    def _visit_interface_declaration(self, node: TSInterfaceDeclaration):
        """Visit interface declaration node."""
        self._write("interface ")
        self._visit_node(node.name)
        
        if node.type_parameters:
            self._write("<")
            for i, param in enumerate(node.type_parameters):
                if i > 0:
                    self._write(", ")
                self._visit_node(param)
            self._write(">")
        
        if node.extends_clause:
            self._write(" extends ")
            for i, extend_type in enumerate(node.extends_clause):
                if i > 0:
                    self._write(", ")
                self._visit_node(extend_type)
        
        self._write(" {")
        if node.body:
            self._write_line()
            self._indent()
            for i, member in enumerate(node.body):
                if i > 0:
                    self._write_line()
                self._write_indent()
                self._visit_node(member)
                if self.use_semicolons:
                    self._write(";")
            self._dedent()
            self._write_line()
            self._write_indent()
        self._write("}")
    
    def _visit_type_alias_declaration(self, node: TSTypeAliasDeclaration):
        """Visit type alias declaration node."""
        self._write("type ")
        self._visit_node(node.name)
        
        if node.type_parameters:
            self._write("<")
            for i, param in enumerate(node.type_parameters):
                if i > 0:
                    self._write(", ")
                self._visit_node(param)
            self._write(">")
        
        self._write(" = ")
        self._visit_node(node.type_annotation)
        
        if self.use_semicolons:
            self._write(";")
    
    def _visit_enum_declaration(self, node: TSEnumDeclaration):
        """Visit enum declaration node."""
        if node.const:
            self._write("const ")
        
        self._write("enum ")
        self._visit_node(node.name)
        self._write(" {")
        
        if node.members:
            self._write_line()
            self._indent()
            for i, member in enumerate(node.members):
                if i > 0:
                    self._write(",")
                    self._write_line()
                self._write_indent()
                self._visit_node(member)
            
            if self.use_trailing_comma:
                self._write(",")
            
            self._dedent()
            self._write_line()
            self._write_indent()
        
        self._write("}")
    
    def _visit_enum_member(self, node: TSEnumMember):
        """Visit enum member node."""
        self._visit_node(node.name)
        
        if node.initializer:
            self._write(" = ")
            self._visit_node(node.initializer)
    
    def _visit_class_declaration(self, node: TSClassDeclaration):
        """Visit class declaration node."""
        if node.abstract:
            self._write("abstract ")
        
        self._write("class ")
        self._visit_node(node.name)
        
        if node.type_parameters:
            self._write("<")
            for i, param in enumerate(node.type_parameters):
                if i > 0:
                    self._write(", ")
                self._visit_node(param)
            self._write(">")
        
        if node.super_class:
            self._write(" extends ")
            self._visit_node(node.super_class)
        
        if node.implements_clause:
            self._write(" implements ")
            for i, interface_type in enumerate(node.implements_clause):
                if i > 0:
                    self._write(", ")
                self._visit_node(interface_type)
        
        self._write(" {")
        
        if node.body:
            self._write_line()
            self._indent()
            for i, member in enumerate(node.body):
                if i > 0:
                    self._write_line()
                self._write_indent()
                self._visit_node(member)
            self._dedent()
            self._write_line()
            self._write_indent()
        
        self._write("}")
    
    def _visit_namespace_declaration(self, node: TSNamespaceDeclaration):
        """Visit namespace declaration node."""
        self._write("namespace ")
        self._visit_node(node.name)
        self._write(" {")
        
        if node.body:
            self._write_line()
            self._indent()
            for i, stmt in enumerate(node.body):
                if i > 0:
                    self._write_line()
                self._write_indent()
                self._visit_node(stmt)
            self._dedent()
            self._write_line()
            self._write_indent()
        
        self._write("}")
    
    def _visit_method_signature(self, node: TSMethodSignature):
        """Visit method signature node."""
        self._visit_node(node.name)
        
        if node.optional:
            self._write("?")
        
        if node.type_parameters:
            self._write("<")
            for i, param in enumerate(node.type_parameters):
                if i > 0:
                    self._write(", ")
                self._visit_node(param)
            self._write(">")
        
        self._write("(")
        for i, param in enumerate(node.parameters):
            if i > 0:
                self._write(", ")
            self._visit_node(param)
        self._write(")")
        
        if node.return_type:
            self._visit_node(node.return_type)
    
    def _visit_property_signature(self, node: TSPropertySignature):
        """Visit property signature node."""
        if node.readonly:
            self._write("readonly ")
        
        self._visit_node(node.name)
        
        if node.optional:
            self._write("?")
        
        if node.type_annotation:
            self._visit_node(node.type_annotation)
    
    def _visit_block_statement(self, node: TSBlockStatement):
        """Visit block statement node."""
        self._write("{")
        
        if node.body:
            self._write_line()
            self._indent()
            for i, stmt in enumerate(node.body):
                if i > 0:
                    self._write_line()
                self._write_indent()
                self._visit_node(stmt)
            self._dedent()
            self._write_line()
            self._write_indent()
        
        self._write("}")
    
    # Helper methods
    def _write(self, text: str):
        """Write text to output."""
        self.output.write(text)
    
    def _write_line(self):
        """Write a new line."""
        self.output.write('\n')
    
    def _write_indent(self):
        """Write current indentation."""
        self.output.write(' ' * (self.current_indent * self.indent_size))
    
    def _indent(self):
        """Increase indentation level."""
        self.current_indent += 1
    
    def _dedent(self):
        """Decrease indentation level."""
        self.current_indent = max(0, self.current_indent - 1)


class TSMinifier:
    """TypeScript code minifier."""
    
    def __init__(self):
        self.generator = TSCodeGenerator(indent_size=0, use_semicolons=True)
    
    def minify(self, node: TSNode) -> str:
        """Minify TypeScript code."""
        code = self.generator.generate(node)
        
        # Remove unnecessary whitespace
        code = re.sub(r'\s+', ' ', code)
        code = re.sub(r'\s*{\s*', '{', code)
        code = re.sub(r'\s*}\s*', '}', code)
        code = re.sub(r'\s*;\s*', ';', code)
        code = re.sub(r'\s*,\s*', ',', code)
        code = re.sub(r'\s*:\s*', ':', code)
        
        return code.strip()


class TSFormatter:
    """TypeScript code formatter with different styles."""
    
    def __init__(self, style: str = "standard"):
        self.style = style
        self._configure_style()
    
    def _configure_style(self):
        """Configure formatting style."""
        if self.style == "standard":
            self.generator = TSCodeGenerator(indent_size=2, use_semicolons=True)
        elif self.style == "compact":
            self.generator = TSCodeGenerator(indent_size=2, use_semicolons=False)
        elif self.style == "expanded":
            self.generator = TSCodeGenerator(indent_size=4, use_semicolons=True)
        else:
            self.generator = TSCodeGenerator()
    
    def format(self, node: TSNode) -> str:
        """Format TypeScript code."""
        return self.generator.generate(node)


def generate_typescript(node: TSNode, **options) -> str:
    """Generate TypeScript code from AST node."""
    if options.get("minify", False):
        minifier = TSMinifier()
        return minifier.minify(node)
    
    style = options.get("style", "standard")
    formatter = TSFormatter(style)
    return formatter.format(node)