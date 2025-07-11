#!/usr/bin/env python3
"""
OCaml Code Generator

Generates clean, idiomatic OCaml code from OCaml AST nodes.
Handles proper formatting, indentation, and OCaml syntax conventions.
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass
from io import StringIO

from .ocaml_ast import *


@dataclass
class OcamlCodeStyle:
    """OCaml code style configuration."""
    indent_size: int = 2
    line_length: int = 80
    use_tabs: bool = False
    space_after_comma: bool = True
    space_around_operators: bool = True
    compact_lists: bool = False
    match_indent: int = 2
    
    @property
    def indent_string(self) -> str:
        """Get indentation string."""
        if self.use_tabs:
            return '\t'
        return ' ' * self.indent_size


class OcamlCodeGenerator:
    """Generates OCaml source code from AST."""
    
    def __init__(self, style: Optional[OcamlCodeStyle] = None):
        self.style = style or OcamlCodeStyle()
        self.output = StringIO()
        self.indent_level = 0
        self.current_line = ""
    
    def generate(self, node: OcamlNode) -> str:
        """Generate code for AST node."""
        self.output = StringIO()
        self.indent_level = 0
        self.current_line = ""
        
        self.visit(node)
        return self.output.getvalue().strip()
    
    def visit(self, node: OcamlNode) -> str:
        """Visit AST node and generate code."""
        method_name = f"visit_{node.__class__.__name__.lower()}"
        method = getattr(self, method_name, self.visit_generic)
        return method(node)
    
    def visit_generic(self, node: OcamlNode) -> str:
        """Generic visit method."""
        return f"(* Unknown node: {type(node)} *)"
    
    def write(self, text: str):
        """Write text to output."""
        self.current_line += text
    
    def write_line(self, text: str = ""):
        """Write line with current indentation."""
        if text:
            self.current_line += text
        if self.current_line.strip():
            self.output.write(self.style.indent_string * self.indent_level + self.current_line.rstrip())
        self.output.write('\n')
        self.current_line = ""
    
    def indent(self):
        """Increase indentation."""
        self.indent_level += 1
    
    def dedent(self):
        """Decrease indentation."""
        self.indent_level = max(0, self.indent_level - 1)
    
    def visit_ocamlmodule(self, node: OcamlModule) -> str:
        """Generate module."""
        for i, decl in enumerate(node.declarations):
            if i > 0:
                self.write_line()
            self.visit(decl)
        
        return self.output.getvalue()
    
    def visit_ocamlvaluedeclaration(self, node: OcamlValueDeclaration) -> str:
        """Generate value declaration."""
        if node.recursive:
            self.write("let rec ")
        else:
            self.write("let ")
        
        self.visit_pattern(node.pattern)
        self.write(" = ")
        self.visit(node.expression)
        self.write_line()
        return ""
    
    def visit_ocamltypedeclaration(self, node: OcamlTypeDeclaration) -> str:
        """Generate type declaration."""
        self.write("type ")
        
        # Type parameters
        if node.parameters:
            if len(node.parameters) == 1:
                self.write(f"'{node.parameters[0]} ")
            else:
                self.write("(")
                for i, param in enumerate(node.parameters):
                    if i > 0:
                        self.write(", ")
                    self.write(f"'{param}")
                self.write(") ")
        
        self.write(node.name)
        
        # Type definition
        if node.definition:
            self.write(" = ")
            self.visit_type(node.definition)
        elif node.variants:
            self.write(" =")
            self.write_line()
            self.indent()
            for i, variant in enumerate(node.variants):
                if i > 0:
                    self.write_line("| ", end="")
                else:
                    self.write("  ")
                self.visit_variant(variant)
                if i < len(node.variants) - 1:
                    self.write_line()
            self.dedent()
        elif node.fields:
            self.write(" = {")
            self.write_line()
            self.indent()
            for i, field in enumerate(node.fields):
                self.visit_record_field(field)
                if i < len(node.fields) - 1:
                    self.write(";")
                self.write_line()
            self.dedent()
            self.write("}")
        
        self.write_line()
        return ""
    
    def visit_variant(self, variant: OcamlVariant) -> str:
        """Generate variant constructor."""
        self.write(variant.name)
        if variant.parameters:
            self.write(" of ")
            for i, param_type in enumerate(variant.parameters):
                if i > 0:
                    self.write(" * ")
                self.visit_type(param_type)
        return ""
    
    def visit_record_field(self, field: OcamlRecordField) -> str:
        """Generate record field."""
        if field.mutable:
            self.write("mutable ")
        self.write(f"{field.name} : ")
        self.visit_type(field.type_expr)
        return ""
    
    def visit_ocamlliteral(self, node: OcamlLiteral) -> str:
        """Generate literal."""
        if node.literal_type == "string":
            self.write(f'"{node.value}"')
        elif node.literal_type == "char":
            self.write(f"'{node.value}'")
        elif node.literal_type == "bool":
            self.write("true" if node.value else "false")
        else:
            self.write(str(node.value))
        return ""
    
    def visit_ocamlidentifier(self, node: OcamlIdentifier) -> str:
        """Generate identifier."""
        if node.module_path:
            self.write(".".join(node.module_path) + ".")
        self.write(node.name)
        return ""
    
    def visit_ocamlconstructor(self, node: OcamlConstructor) -> str:
        """Generate constructor."""
        if node.module_path:
            self.write(".".join(node.module_path) + ".")
        self.write(node.name)
        return ""
    
    def visit_ocamlapplication(self, node: OcamlApplication) -> str:
        """Generate application."""
        need_parens = self.needs_parens(node.function)
        if need_parens:
            self.write("(")
        self.visit(node.function)
        if need_parens:
            self.write(")")
        
        for arg in node.arguments:
            self.write(" ")
            need_parens = self.needs_parens(arg)
            if need_parens:
                self.write("(")
            self.visit(arg)
            if need_parens:
                self.write(")")
        return ""
    
    def visit_ocamlfunction(self, node: OcamlFunction) -> str:
        """Generate function."""
        self.write("fun ")
        for i, param in enumerate(node.parameters):
            if i > 0:
                self.write(" ")
            self.visit_pattern(param)
        self.write(" -> ")
        self.visit(node.body)
        return ""
    
    def visit_ocamllet(self, node: OcamlLet) -> str:
        """Generate let expression."""
        if node.recursive:
            self.write("let rec ")
        else:
            self.write("let ")
        
        self.visit_pattern(node.pattern)
        self.write(" = ")
        self.visit(node.value)
        self.write(" in")
        self.write_line()
        self.visit(node.body)
        return ""
    
    def visit_ocamlif(self, node: OcamlIf) -> str:
        """Generate if expression."""
        self.write("if ")
        self.visit(node.condition)
        self.write(" then ")
        self.visit(node.then_expr)
        if node.else_expr:
            self.write(" else ")
            self.visit(node.else_expr)
        return ""
    
    def visit_ocamlmatch(self, node: OcamlMatch) -> str:
        """Generate match expression."""
        self.write("match ")
        self.visit(node.expression)
        self.write(" with")
        self.write_line()
        
        self.indent()
        for i, case in enumerate(node.cases):
            if i > 0:
                self.write_line()
            self.write("| ")
            self.visit_pattern(case.pattern)
            if case.guard:
                self.write(" when ")
                self.visit(case.guard)
            self.write(" -> ")
            self.visit(case.expression)
        self.dedent()
        return ""
    
    def visit_ocamltuple(self, node: OcamlTuple) -> str:
        """Generate tuple."""
        self.write("(")
        for i, elem in enumerate(node.elements):
            if i > 0:
                self.write(", ")
            self.visit(elem)
        self.write(")")
        return ""
    
    def visit_ocamllist(self, node: OcamlList) -> str:
        """Generate list."""
        self.write("[")
        for i, elem in enumerate(node.elements):
            if i > 0:
                self.write("; ")
            self.visit(elem)
        self.write("]")
        return ""
    
    def visit_ocamlrecord(self, node: OcamlRecord) -> str:
        """Generate record."""
        self.write("{")
        if node.base:
            self.visit(node.base)
            self.write(" with ")
        
        for i, field_binding in enumerate(node.fields):
            if i > 0:
                self.write("; ")
            self.write(f"{field_binding.field} = ")
            self.visit(field_binding.expression)
        self.write("}")
        return ""
    
    def visit_ocamlfieldaccess(self, node: OcamlFieldAccess) -> str:
        """Generate field access."""
        need_parens = self.needs_parens(node.expression)
        if need_parens:
            self.write("(")
        self.visit(node.expression)
        if need_parens:
            self.write(")")
        self.write(f".{node.field}")
        return ""
    
    def visit_pattern(self, pattern: OcamlPattern) -> str:
        """Visit pattern node."""
        method_name = f"visit_{pattern.__class__.__name__.lower()}"
        method = getattr(self, method_name, self.visit_generic)
        return method(pattern)
    
    def visit_ocamlwildcardpattern(self, node: OcamlWildcardPattern) -> str:
        """Generate wildcard pattern."""
        self.write("_")
        return ""
    
    def visit_ocamlvariablepattern(self, node: OcamlVariablePattern) -> str:
        """Generate variable pattern."""
        self.write(node.name)
        return ""
    
    def visit_ocamlconstructorpattern(self, node: OcamlConstructorPattern) -> str:
        """Generate constructor pattern."""
        if node.module_path:
            self.write(".".join(node.module_path) + ".")
        self.write(node.constructor)
        
        if node.patterns:
            self.write(" (")
            for i, pattern in enumerate(node.patterns):
                if i > 0:
                    self.write(", ")
                self.visit_pattern(pattern)
            self.write(")")
        return ""
    
    def visit_ocamltuplepattern(self, node: OcamlTuplePattern) -> str:
        """Generate tuple pattern."""
        self.write("(")
        for i, pattern in enumerate(node.patterns):
            if i > 0:
                self.write(", ")
            self.visit_pattern(pattern)
        self.write(")")
        return ""
    
    def visit_type(self, type_expr: OcamlType) -> str:
        """Visit type node."""
        method_name = f"visit_{type_expr.__class__.__name__.lower()}"
        method = getattr(self, method_name, self.visit_generic)
        return method(type_expr)
    
    def visit_ocamltypevariable(self, node: OcamlTypeVariable) -> str:
        """Generate type variable."""
        self.write(f"'{node.name}")
        return ""
    
    def visit_ocamltypeconstructor(self, node: OcamlTypeConstructor) -> str:
        """Generate type constructor."""
        if node.arguments:
            if len(node.arguments) == 1:
                self.visit_type(node.arguments[0])
                self.write(" ")
            else:
                self.write("(")
                for i, arg in enumerate(node.arguments):
                    if i > 0:
                        self.write(", ")
                    self.visit_type(arg)
                self.write(") ")
        
        if node.module_path:
            self.write(".".join(node.module_path) + ".")
        self.write(node.name)
        return ""
    
    def visit_ocamlfunctiontype(self, node: OcamlFunctionType) -> str:
        """Generate function type."""
        need_parens = self.type_needs_parens(node.parameter_type)
        if need_parens:
            self.write("(")
        self.visit_type(node.parameter_type)
        if need_parens:
            self.write(")")
        
        self.write(" -> ")
        self.visit_type(node.return_type)
        return ""
    
    def visit_ocamltupletype(self, node: OcamlTupleType) -> str:
        """Generate tuple type."""
        for i, type_expr in enumerate(node.types):
            if i > 0:
                self.write(" * ")
            need_parens = self.type_needs_parens(type_expr)
            if need_parens:
                self.write("(")
            self.visit_type(type_expr)
            if need_parens:
                self.write(")")
        return ""
    
    def needs_parens(self, expr: OcamlExpression) -> bool:
        """Check if expression needs parentheses."""
        return isinstance(expr, (OcamlApplication, OcamlLet, OcamlIf, OcamlMatch, OcamlFunction))
    
    def type_needs_parens(self, type_expr: OcamlType) -> bool:
        """Check if type expression needs parentheses."""
        return isinstance(type_expr, OcamlFunctionType)


def generate_ocaml(node: OcamlNode, style: Optional[OcamlCodeStyle] = None) -> str:
    """Generate OCaml code from AST node."""
    generator = OcamlCodeGenerator(style)
    return generator.generate(node) 