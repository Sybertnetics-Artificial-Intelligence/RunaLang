#!/usr/bin/env python3
"""
Pact Code Generator

Generates idiomatic LISP-like Pact smart contract code from AST.
Supports S-expressions, capabilities, formal verification, and Kadena-specific constructs.
"""

from typing import List, Optional, Dict, Any
from io import StringIO
from .pact_ast import *


class PactCodeStyle:
    """Configuration for Pact code style."""
    
    def __init__(self):
        self.indent_size = 2
        self.use_spaces = True
        self.max_line_length = 80
        self.format_style = "lisp"  # lisp, compact


class PactFormatter:
    """Formats Pact code according to style guidelines."""
    
    def __init__(self, style: PactCodeStyle):
        self.style = style
        self.indent_level = 0
        self.output = StringIO()
        self.line_start = True
    
    def write(self, text: str) -> None:
        """Write text to output."""
        if self.line_start and text.strip():
            self.output.write(" " * (self.indent_level * self.style.indent_size))
            self.line_start = False
        self.output.write(text)
    
    def write_line(self, text: str = "") -> None:
        """Write line with newline."""
        if text:
            self.write(text)
        self.output.write("\n")
        self.line_start = True
    
    def indent(self) -> None:
        """Increase indentation level."""
        self.indent_level += 1
    
    def dedent(self) -> None:
        """Decrease indentation level."""
        if self.indent_level > 0:
            self.indent_level -= 1
    
    def get_output(self) -> str:
        """Get formatted output."""
        return self.output.getvalue()


class PactCodeGenerator:
    """Generates Pact smart contract code from AST."""
    
    def __init__(self, style: PactCodeStyle = None):
        self.style = style or PactCodeStyle()
        self.formatter = PactFormatter(self.style)
    
    def generate_program(self, program: PactProgram) -> str:
        """Generate complete Pact program."""
        self.formatter = PactFormatter(self.style)
        
        for module in program.modules:
            self.generate_module(module)
            self.formatter.write_line()
        
        return self.formatter.get_output()
    
    def generate_module(self, module: PactModule) -> None:
        """Generate Pact module."""
        self.formatter.write_line(f"(module {module.name}")
        self.formatter.indent()
        
        # Generate governance if present
        if module.governance:
            self.formatter.write("  ")
            self.generate_expression(module.governance)
            self.formatter.write_line()
        
        # Generate declarations
        for decl in module.declarations:
            self.formatter.write_line()
            self.generate_declaration(decl)
        
        self.formatter.dedent()
        self.formatter.write_line(")")
    
    def generate_declaration(self, decl: PactDeclaration) -> None:
        """Generate declaration."""
        if isinstance(decl, PactDefun):
            self.generate_defun(decl)
        elif isinstance(decl, PactDefcap):
            self.generate_defcap(decl)
        elif isinstance(decl, PactDefconst):
            self.generate_defconst(decl)
        elif isinstance(decl, PactDefschema):
            self.generate_defschema(decl)
        elif isinstance(decl, PactDeftable):
            self.generate_deftable(decl)
    
    def generate_defun(self, defun: PactDefun) -> None:
        """Generate function definition."""
        self.formatter.write(f"(defun {defun.name} (")
        
        # Parameters
        for i, param in enumerate(defun.parameters):
            if i > 0:
                self.formatter.write(" ")
            self.formatter.write(param.name)
            if param.pact_type:
                self.formatter.write(f":{param.pact_type.name}")
        
        self.formatter.write(")")
        
        # Return type
        if defun.return_type:
            self.formatter.write(f":{defun.return_type.name}")
        
        # Documentation
        if defun.documentation:
            self.formatter.write_line()
            self.formatter.write(f'  "{defun.documentation}"')
        
        # Body
        if defun.body:
            self.formatter.write_line()
            self.formatter.write("  ")
            self.generate_expression(defun.body)
        
        self.formatter.write(")")
    
    def generate_defcap(self, defcap: PactDefcap) -> None:
        """Generate capability definition."""
        self.formatter.write(f"(defcap {defcap.name} (")
        
        # Parameters
        for i, param in enumerate(defcap.parameters):
            if i > 0:
                self.formatter.write(" ")
            self.formatter.write(param.name)
            if param.pact_type:
                self.formatter.write(f":{param.pact_type.name}")
        
        self.formatter.write(")")
        
        # Documentation
        if defcap.documentation:
            self.formatter.write_line()
            self.formatter.write(f'  "{defcap.documentation}"')
        
        # Body
        if defcap.body:
            self.formatter.write_line()
            self.formatter.write("  ")
            self.generate_expression(defcap.body)
        
        self.formatter.write(")")
    
    def generate_defconst(self, defconst: PactDefconst) -> None:
        """Generate constant definition."""
        self.formatter.write(f"(defconst {defconst.name}")
        
        if defconst.pact_type:
            self.formatter.write(f":{defconst.pact_type.name}")
        
        self.formatter.write(" ")
        self.generate_expression(defconst.value)
        self.formatter.write(")")
    
    def generate_defschema(self, defschema: PactDefschema) -> None:
        """Generate schema definition."""
        self.formatter.write(f"(defschema {defschema.name}")
        
        for field in defschema.fields:
            self.formatter.write_line()
            self.formatter.write(f"  {field.name}:{field.field_type.name}")
        
        self.formatter.write(")")
    
    def generate_deftable(self, deftable: PactDeftable) -> None:
        """Generate table definition."""
        self.formatter.write(f"(deftable {deftable.name}:{deftable.schema})")
    
    def generate_expression(self, expr: PactExpression) -> None:
        """Generate expression."""
        if isinstance(expr, PactLiteral):
            self.generate_literal(expr)
        elif isinstance(expr, PactVariable):
            self.generate_variable(expr)
        elif isinstance(expr, PactFunctionCall):
            self.generate_function_call(expr)
        elif isinstance(expr, PactIf):
            self.generate_if(expr)
        elif isinstance(expr, PactLet):
            self.generate_let(expr)
        elif isinstance(expr, PactObject):
            self.generate_object(expr)
        elif isinstance(expr, PactList):
            self.generate_list(expr)
        else:
            self.formatter.write("()")  # Default fallback
    
    def generate_literal(self, literal: PactLiteral) -> None:
        """Generate literal value."""
        if literal.literal_type == "string":
            escaped = literal.value.replace("\\", "\\\\").replace('"', '\\"')
            self.formatter.write(f'"{escaped}"')
        elif literal.literal_type == "bool":
            self.formatter.write("true" if literal.value else "false")
        else:
            self.formatter.write(str(literal.value))
    
    def generate_variable(self, var: PactVariable) -> None:
        """Generate variable reference."""
        self.formatter.write(var.name)
    
    def generate_function_call(self, call: PactFunctionCall) -> None:
        """Generate function call."""
        self.formatter.write(f"({call.function}")
        
        for arg in call.arguments:
            self.formatter.write(" ")
            self.generate_expression(arg)
        
        self.formatter.write(")")
    
    def generate_if(self, if_expr: PactIf) -> None:
        """Generate if expression."""
        self.formatter.write("(if ")
        self.generate_expression(if_expr.condition)
        self.formatter.write(" ")
        self.generate_expression(if_expr.then_expr)
        
        if if_expr.else_expr:
            self.formatter.write(" ")
            self.generate_expression(if_expr.else_expr)
        
        self.formatter.write(")")
    
    def generate_let(self, let_expr: PactLet) -> None:
        """Generate let expression."""
        self.formatter.write("(let (")
        
        for i, binding in enumerate(let_expr.bindings):
            if i > 0:
                self.formatter.write(" ")
            self.formatter.write(f"({binding.variable} ")
            self.generate_expression(binding.value)
            self.formatter.write(")")
        
        self.formatter.write(") ")
        self.generate_expression(let_expr.body)
        self.formatter.write(")")
    
    def generate_object(self, obj: PactObject) -> None:
        """Generate object literal."""
        self.formatter.write("{")
        
        first = True
        for key, value in obj.fields.items():
            if not first:
                self.formatter.write(", ")
            first = False
            
            self.formatter.write(f'"{key}": ')
            self.generate_expression(value)
        
        self.formatter.write("}")
    
    def generate_list(self, lst: PactList) -> None:
        """Generate list expression."""
        self.formatter.write("(")
        
        for i, element in enumerate(lst.elements):
            if i > 0:
                self.formatter.write(" ")
            self.generate_expression(element)
        
        self.formatter.write(")")


def generate_pact(ast: PactProgram, style: PactCodeStyle = None) -> str:
    """Generate Pact code from AST."""
    generator = PactCodeGenerator(style)
    return generator.generate_program(ast) 