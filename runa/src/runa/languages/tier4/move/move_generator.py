#!/usr/bin/env python3
"""
Move Code Generator

Generates idiomatic Move source code from Move AST nodes, preserving Move's
resource-oriented programming semantics, abilities system, and safety-first
design principles. Supports multiple formatting styles and code conventions.

Features:
- Resource-oriented code generation
- Abilities system syntax
- Module and script organization
- Type system with generics and references
- Move-specific expressions and statements
- Formal verification syntax
- Configurable formatting and style options
"""

from typing import List, Optional, Dict, Any, Union, Set
from dataclasses import dataclass
from io import StringIO

from .move_ast import *


@dataclass
class MoveCodeStyle:
    """Move code formatting and style configuration."""
    indent_size: int = 4
    indent_char: str = " "
    max_line_length: int = 100
    brace_style: str = "same_line"  # "same_line" or "new_line"
    space_around_operators: bool = True
    space_after_comma: bool = True
    space_before_function_paren: bool = False
    newline_after_module_declaration: bool = True
    newline_before_function: bool = True
    newline_before_struct: bool = True
    group_imports: bool = True
    sort_imports: bool = True
    prefer_explicit_types: bool = True
    preserve_comments: bool = True
    
    # Move-specific style options
    abilities_on_same_line: bool = True
    acquires_on_same_line: bool = True
    type_params_multiline_threshold: int = 3
    function_params_multiline_threshold: int = 4


class MoveCodeGenerator:
    """Generates Move source code from Move AST."""
    
    def __init__(self, style: Optional[MoveCodeStyle] = None):
        self.style = style or MoveCodeStyle()
        self.output = StringIO()
        self.indent_level = 0
        self.at_line_start = True
        
    def generate(self, node: MoveNode) -> str:
        """Generate Move code from AST node."""
        self.output = StringIO()
        self.indent_level = 0
        self.at_line_start = True
        
        node.accept(self)
        
        return self.output.getvalue()
    
    def write(self, text: str):
        """Write text to output."""
        if self.at_line_start and text.strip():
            self.output.write(self.style.indent_char * (self.indent_level * self.style.indent_size))
            self.at_line_start = False
        self.output.write(text)
    
    def writeln(self, text: str = ""):
        """Write text followed by newline."""
        if text:
            self.write(text)
        self.output.write("\n")
        self.at_line_start = True
    
    def indent(self):
        """Increase indentation level."""
        self.indent_level += 1
    
    def dedent(self):
        """Decrease indentation level."""
        self.indent_level = max(0, self.indent_level - 1)
    
    def write_separated(self, items: List[str], separator: str = ", "):
        """Write items separated by separator."""
        for i, item in enumerate(items):
            if i > 0:
                self.write(separator)
            self.write(item)
    
    def visit_program(self, node: MoveProgram):
        """Generate Move program."""
        # Generate modules
        for i, module in enumerate(node.modules):
            if i > 0:
                self.writeln()
                self.writeln()
            module.accept(self)
        
        # Generate scripts
        for script in node.scripts:
            self.writeln()
            self.writeln()
            script.accept(self)
        
        # Generate specifications
        for spec in node.specifications:
            self.writeln()
            self.writeln()
            spec.accept(self)
    
    def visit_module(self, node: MoveModule):
        """Generate Move module."""
        self.write(f"module {node.address}::{node.name}")
        
        if self.style.brace_style == "same_line":
            self.write(" {")
        else:
            self.writeln()
            self.write("{")
        
        if self.style.newline_after_module_declaration:
            self.writeln()
        
        self.indent()
        
        # Generate use declarations
        if node.use_declarations:
            if self.style.group_imports:
                use_decls = sorted(node.use_declarations, key=lambda u: u.module_name) if self.style.sort_imports else node.use_declarations
            else:
                use_decls = node.use_declarations
            
            for use_decl in use_decls:
                use_decl.accept(self)
                self.writeln()
            
            if node.friend_declarations or node.constants or node.structs or node.functions:
                self.writeln()
        
        # Generate friend declarations
        if node.friend_declarations:
            for friend_decl in node.friend_declarations:
                friend_decl.accept(self)
                self.writeln()
            self.writeln()
        
        # Generate constants
        if node.constants:
            for const in node.constants:
                const.accept(self)
                self.writeln()
            self.writeln()
        
        # Generate structs
        for i, struct in enumerate(node.structs):
            if i > 0 and self.style.newline_before_struct:
                self.writeln()
            struct.accept(self)
            if i < len(node.structs) - 1 or node.functions:
                self.writeln()
        
        # Generate functions
        for i, func in enumerate(node.functions):
            if i > 0 and self.style.newline_before_function:
                self.writeln()
            func.accept(self)
            if i < len(node.functions) - 1:
                self.writeln()
        
        self.dedent()
        self.writeln("}")
    
    def visit_struct_declaration(self, node: MoveStructDeclaration):
        """Generate Move struct declaration."""
        if node.is_native:
            self.write("native ")
        
        self.write("struct ")
        self.write(node.name)
        
        # Type parameters
        if node.type_parameters:
            self.write("<")
            type_params = []
            for tp in node.type_parameters:
                param_str = tp.name
                if tp.constraints:
                    param_str += ": " + " + ".join(constraint.value for constraint in tp.constraints)
                type_params.append(param_str)
            
            if len(type_params) > self.style.type_params_multiline_threshold:
                self.writeln()
                self.indent()
                for i, param in enumerate(type_params):
                    self.write(param)
                    if i < len(type_params) - 1:
                        self.write(",")
                        self.writeln()
                self.dedent()
                self.writeln()
                self.write(">")
            else:
                self.write_separated(type_params)
                self.write(">")
        
        # Abilities
        if node.abilities:
            if self.style.abilities_on_same_line:
                self.write(" has ")
            else:
                self.writeln()
                self.indent()
                self.write("has ")
            
            abilities = [ability.value for ability in node.abilities]
            self.write_separated(abilities, " + ")
            
            if not self.style.abilities_on_same_line:
                self.dedent()
        
        if node.fields:
            self.write(" {")
            self.writeln()
            self.indent()
            
            for i, field in enumerate(node.fields):
                field.accept(self)
                if i < len(node.fields) - 1:
                    self.write(",")
                self.writeln()
            
            self.dedent()
            self.write("}")
        else:
            self.write(" {}")
    
    def visit_function_declaration(self, node: MoveFunctionDeclaration):
        """Generate Move function declaration."""
        # Visibility
        if node.visibility != MoveVisibility.PRIVATE:
            if node.visibility == MoveVisibility.PUBLIC:
                self.write("public ")
            elif node.visibility == MoveVisibility.PUBLIC_FRIEND:
                self.write("public(friend) ")
            elif node.visibility == MoveVisibility.PUBLIC_SCRIPT:
                self.write("public(script) ")
            elif node.visibility == MoveVisibility.PUBLIC_ENTRY:
                self.write("public(entry) ")
        
        if node.is_entry and node.visibility == MoveVisibility.PUBLIC:
            self.write("entry ")
        
        if node.is_native:
            self.write("native ")
        
        self.write("fun ")
        self.write(node.name)
        
        # Type parameters
        if node.type_parameters:
            self.write("<")
            type_params = []
            for tp in node.type_parameters:
                param_str = tp.name
                if tp.constraints:
                    param_str += ": " + " + ".join(constraint.value for constraint in tp.constraints)
                type_params.append(param_str)
            self.write_separated(type_params)
            self.write(">")
        
        # Parameters
        if self.style.space_before_function_paren:
            self.write(" ")
        self.write("(")
        
        if node.parameters:
            if len(node.parameters) > self.style.function_params_multiline_threshold:
                self.writeln()
                self.indent()
                for i, param in enumerate(node.parameters):
                    param.accept(self)
                    if i < len(node.parameters) - 1:
                        self.write(",")
                        self.writeln()
                self.dedent()
                self.writeln()
            else:
                for i, param in enumerate(node.parameters):
                    param.accept(self)
                    if i < len(node.parameters) - 1:
                        self.write(", " if self.style.space_after_comma else ",")
        
        self.write(")")
        
        # Return type
        if node.return_type:
            self.write(": ")
            node.return_type.accept(self)
        
        # Acquires clause
        if node.acquires:
            if self.style.acquires_on_same_line:
                self.write(" acquires ")
            else:
                self.writeln()
                self.indent()
                self.write("acquires ")
            
            for i, acq in enumerate(node.acquires):
                acq.accept(self)
                if i < len(node.acquires) - 1:
                    self.write(", " if self.style.space_after_comma else ",")
            
            if not self.style.acquires_on_same_line:
                self.dedent()
        
        # Function body
        if node.body:
            self.write(" ")
            node.body.accept(self)
        else:
            self.write(";")
    
    def visit_parameter(self, node: MoveParameter):
        """Generate function parameter."""
        self.write(node.name)
        self.write(": ")
        node.parameter_type.accept(self)
    
    def visit_field(self, node: MoveField):
        """Generate struct field."""
        self.write(node.name)
        self.write(": ")
        node.field_type.accept(self)
    
    def visit_use_declaration(self, node: MoveUseDeclaration):
        """Generate use declaration."""
        self.write("use ")
        
        if node.module_address:
            self.write(f"{node.module_address}::")
        
        self.write(node.module_name)
        
        if node.imported_items:
            self.write("::{")
            self.write_separated(node.imported_items)
            self.write("}")
        elif node.import_name:
            self.write(f" as {node.import_name}")
        
        self.write(";")
    
    def visit_friend_declaration(self, node: MoveFriendDeclaration):
        """Generate friend declaration."""
        self.write(f"friend {node.module_address}::{node.module_name};")
    
    def visit_constant_declaration(self, node: MoveConstantDeclaration):
        """Generate constant declaration."""
        self.write("const ")
        self.write(node.name)
        self.write(": ")
        node.constant_type.accept(self)
        self.write(" = ")
        node.value.accept(self)
        self.write(";")
    
    def visit_primitive(self, node: MovePrimitive):
        """Generate primitive type."""
        self.write(node.type_name.value)
    
    def visit_struct_type(self, node: MoveStructType):
        """Generate struct type."""
        if node.module_name:
            self.write(f"{node.module_name}::")
        self.write(node.struct_name)
        
        if node.type_arguments:
            self.write("<")
            for i, arg in enumerate(node.type_arguments):
                arg.accept(self)
                if i < len(node.type_arguments) - 1:
                    self.write(", " if self.style.space_after_comma else ",")
            self.write(">")
    
    def visit_vector_type(self, node: MoveVectorType):
        """Generate vector type."""
        self.write("vector<")
        node.element_type.accept(self)
        self.write(">")
    
    def visit_reference_type(self, node: MoveReferenceType):
        """Generate reference type."""
        if node.is_mutable:
            self.write("&mut ")
        else:
            self.write("&")
        node.referenced_type.accept(self)
    
    def visit_literal(self, node: MoveLiteral):
        """Generate literal."""
        if node.literal_type == MovePrimitiveType.BOOL:
            self.write("true" if node.value else "false")
        elif node.literal_type == MovePrimitiveType.ADDRESS:
            self.write(f"@{node.value}")
        elif isinstance(node.value, str):
            self.write(f'"{node.value}"')
        else:
            self.write(str(node.value))
    
    def visit_identifier(self, node: MoveIdentifier):
        """Generate identifier."""
        self.write(node.name)
    
    def visit_binary_op(self, node: MoveBinaryOp):
        """Generate binary operation."""
        node.left.accept(self)
        
        if self.style.space_around_operators:
            self.write(f" {node.operator.value} ")
        else:
            self.write(node.operator.value)
        
        node.right.accept(self)
    
    def visit_function_call(self, node: MoveFunctionCall):
        """Generate function call."""
        if node.module_name:
            self.write(f"{node.module_name}::")
        self.write(node.function_name)
        
        # Type arguments
        if node.type_arguments:
            self.write("<")
            for i, arg in enumerate(node.type_arguments):
                arg.accept(self)
                if i < len(node.type_arguments) - 1:
                    self.write(", " if self.style.space_after_comma else ",")
            self.write(">")
        
        self.write("(")
        for i, arg in enumerate(node.arguments):
            arg.accept(self)
            if i < len(node.arguments) - 1:
                self.write(", " if self.style.space_after_comma else ",")
        self.write(")")
    
    def visit_borrow(self, node: MoveBorrow):
        """Generate borrow expression."""
        if node.is_mutable:
            self.write("&mut ")
        else:
            self.write("&")
        node.expression.accept(self)
    
    def visit_move(self, node: MoveMove):
        """Generate move expression."""
        self.write("move ")
        node.expression.accept(self)
    
    def visit_copy(self, node: MoveCopy):
        """Generate copy expression."""
        self.write("copy ")
        node.expression.accept(self)
    
    def visit_block(self, node: MoveBlock):
        """Generate block."""
        self.write("{")
        
        if node.statements or node.return_expression:
            self.writeln()
            self.indent()
            
            for stmt in node.statements:
                stmt.accept(self)
                self.writeln()
            
            if node.return_expression:
                node.return_expression.accept(self)
                self.writeln()
            
            self.dedent()
        
        self.write("}")
    
    def visit_variable_declaration(self, node: MoveVariableDeclaration):
        """Generate variable declaration."""
        self.write("let ")
        node.pattern.accept(self)
        
        if node.type_annotation:
            self.write(": ")
            node.type_annotation.accept(self)
        
        if node.initializer:
            self.write(" = ")
            node.initializer.accept(self)
        
        self.write(";")
    
    def visit_identifier_pattern(self, node: MoveIdentifierPattern):
        """Generate identifier pattern."""
        if node.is_mutable:
            self.write("mut ")
        self.write(node.name)
    
    def visit_assignment(self, node: MoveAssignment):
        """Generate assignment."""
        node.target.accept(self)
        self.write(" = ")
        node.value.accept(self)
        self.write(";")
    
    def visit_return(self, node: MoveReturn):
        """Generate return statement."""
        self.write("return")
        if node.value:
            self.write(" ")
            node.value.accept(self)
        self.write(";")
    
    def visit_abort(self, node: MoveAbort):
        """Generate abort statement."""
        self.write("abort ")
        node.code.accept(self)
        self.write(";")


def generate_move_code(ast: MoveNode, style: Optional[MoveCodeStyle] = None) -> str:
    """Generate Move source code from AST."""
    generator = MoveCodeGenerator(style)
    return generator.generate(ast)


def format_move_code(source: str, style: Optional[MoveCodeStyle] = None) -> str:
    """Format Move source code according to style guide."""
    # This would parse and regenerate the code with proper formatting
    # For now, return the source as-is
    return source


class MoveFormatter:
    """Move code formatter for consistent styling."""
    
    def __init__(self, style: Optional[MoveCodeStyle] = None):
        self.style = style or MoveCodeStyle()
    
    def format(self, source: str) -> str:
        """Format Move source code."""
        # Implementation would involve parsing and regenerating
        return format_move_code(source, self.style) 