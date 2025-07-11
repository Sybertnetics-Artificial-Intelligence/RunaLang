"""
Scilla Code Generator

This module generates idiomatic Scilla smart contract code from AST nodes.
Produces clean, readable, and gas-efficient Scilla code following best practices
for the Zilliqa blockchain.

Features:
- Smart contract structure generation
- Functional programming patterns
- Type-safe code generation  
- Gas optimization awareness
- Proper indentation and formatting
"""

from typing import List, Optional, Dict, Any
from io import StringIO

from .scilla_ast import *


class ScillaCodeGenerator:
    """Generates Scilla source code from AST"""
    
    def __init__(self, indent_size: int = 2):
        self.indent_size = indent_size
        self.indent_level = 0
        self.output = StringIO()
        
    def generate(self, node: ScillaProgram) -> str:
        """Generate Scilla code from program AST"""
        self.output = StringIO()
        self.indent_level = 0
        
        self._generate_program(node)
        return self.output.getvalue()
    
    def _write(self, text: str = ""):
        """Write text to output"""
        self.output.write(text)
    
    def _writeln(self, text: str = ""):
        """Write line with current indentation"""
        if text:
            indent = " " * (self.indent_level * self.indent_size)
            self.output.write(f"{indent}{text}\n")
        else:
            self.output.write("\n")
    
    def _indent(self):
        """Increase indentation level"""
        self.indent_level += 1
    
    def _dedent(self):
        """Decrease indentation level"""
        self.indent_level = max(0, self.indent_level - 1)
    
    def _generate_program(self, node: ScillaProgram):
        """Generate complete Scilla program"""
        # Scilla version
        self._writeln(f"scilla_version {node.scilla_version}")
        self._writeln()
        
        # Imports
        for imp in node.contract.imports:
            self._generate_import(imp)
        
        if node.contract.imports:
            self._writeln()
        
        # Library
        if node.contract.library:
            self._generate_library(node.contract.library)
            self._writeln()
        
        # Contract
        self._generate_contract(node.contract)
    
    def _generate_import(self, node: ScillaImport):
        """Generate import statement"""
        if node.items:
            items = ", ".join(node.items)
            self._writeln(f"import {node.module} as {items}")
        else:
            self._writeln(f"import {node.module}")
    
    def _generate_library(self, node: ScillaLibrary):
        """Generate library declaration"""
        self._writeln(f"library {node.name}")
        self._writeln()
        
        # Library imports
        for imp in node.imports:
            self._generate_import(imp)
        
        if node.imports:
            self._writeln()
        
        # Type declarations
        for type_decl in node.type_declarations:
            self._generate_adt_declaration(type_decl)
            self._writeln()
        
        # Function declarations  
        for func_decl in node.function_declarations:
            self._generate_library_function(func_decl)
            self._writeln()
    
    def _generate_adt_declaration(self, node: ScillaADTDeclaration):
        """Generate algebraic data type declaration"""
        type_params = ""
        if node.type_params:
            params = " ".join(f"'{tp.name}" for tp in node.type_params)
            type_params = f" {params}"
        
        self._writeln(f"type {node.name}{type_params} =")
        
        for i, constructor in enumerate(node.constructors):
            if i > 0:
                self._write(" | ")
            else:
                self._write("  ")
            
            self._write(constructor.name)
            if constructor.arg_types:
                self._write(" of ")
                type_strs = [self._type_to_string(t) for t in constructor.arg_types]
                self._write(" * ".join(type_strs))
            
            if i == len(node.constructors) - 1:
                self._write("\n")
            else:
                self._write("\n")
    
    def _generate_library_function(self, node: ScillaLibraryFunction):
        """Generate library function"""
        # Type parameters
        type_params = ""
        if node.type_params:
            params = " ".join(f"'{tp.name}" for tp in node.type_params)
            type_params = f" {params}"
        
        # Parameters
        param_strs = []
        for param in node.params:
            param_str = f"{param.name} : {self._type_to_string(param.type)}"
            param_strs.append(param_str)
        
        params = " -> ".join(param_strs)
        if params:
            params += " -> "
        
        return_type = self._type_to_string(node.return_type)
        
        self._writeln(f"let {node.name}{type_params} : {params}{return_type} =")
        self._indent()
        self._generate_expression(node.body)
        self._writeln()
        self._dedent()
    
    def _generate_contract(self, node: ScillaContract):
        """Generate contract declaration"""
        # Contract header
        self._write(f"contract {node.name}")
        
        # Immutable parameters
        if node.immutable_params:
            self._write("(")
            param_strs = []
            for param in node.immutable_params:
                param_str = f"{param.name} : {self._type_to_string(param.type)}"
                param_strs.append(param_str)
            self._write(", ".join(param_strs))
            self._write(")")
        else:
            self._write("()")
        
        self._writeln()
        self._writeln()
        
        # Fields
        for field in node.fields:
            self._generate_field(field)
        
        if node.fields:
            self._writeln()
        
        # Transitions and procedures
        for transition in node.transitions:
            self._generate_transition(transition)
            self._writeln()
        
        for procedure in node.procedures:
            self._generate_procedure(procedure)
            self._writeln()
    
    def _generate_field(self, node: ScillaFieldDeclaration):
        """Generate contract field"""
        field_type = self._type_to_string(node.type)
        
        if node.init_value:
            self._write(f"field {node.name} : {field_type} = ")
            self._generate_expression(node.init_value)
            self._writeln()
        else:
            self._writeln(f"field {node.name} : {field_type}")
    
    def _generate_transition(self, node: ScillaTransition):
        """Generate contract transition"""
        # Transition header
        self._write(f"transition {node.name}")
        
        # Parameters
        if node.params:
            self._write("(")
            param_strs = []
            for param in node.params:
                param_str = f"{param.name} : {self._type_to_string(param.type)}"
                param_strs.append(param_str)
            self._write(", ".join(param_strs))
            self._write(")")
        else:
            self._write("()")
        
        self._writeln()
        self._indent()
        
        # Statements
        for stmt in node.statements:
            self._generate_statement(stmt)
        
        self._dedent()
        self._writeln("end")
    
    def _generate_procedure(self, node: ScillaProcedure):
        """Generate contract procedure"""
        # Procedure header
        self._write(f"procedure {node.name}")
        
        # Parameters
        if node.params:
            self._write("(")
            param_strs = []
            for param in node.params:
                param_str = f"{param.name} : {self._type_to_string(param.type)}"
                param_strs.append(param_str)
            self._write(", ".join(param_strs))
            self._write(")")
        else:
            self._write("()")
        
        self._writeln()
        self._indent()
        
        # Statements
        for stmt in node.statements:
            self._generate_statement(stmt)
        
        self._dedent()
        self._writeln("end")
    
    def _generate_statement(self, node: ScillaStatement):
        """Generate statement"""
        if isinstance(node, ScillaLoad):
            self._writeln(f"{node.var} <- {node.field};")
        
        elif isinstance(node, ScillaStore):
            self._write(f"{node.field} := ")
            self._generate_expression(node.value)
            self._writeln(";")
        
        elif isinstance(node, ScillaBind):
            self._write(f"{node.var} = ")
            self._generate_expression(node.value)
            self._writeln(";")
        
        elif isinstance(node, ScillaMapUpdate):
            self._write(f"{node.map_name}[")
            self._generate_expression(node.key)
            self._write("] := ")
            self._generate_expression(node.value)
            self._writeln(";")
        
        elif isinstance(node, ScillaMapDelete):
            self._write(f"delete {node.map_name}[")
            self._generate_expression(node.key)
            self._writeln("];")
        
        elif isinstance(node, ScillaSend):
            self._write("send ")
            self._generate_expression(node.messages)
            self._writeln(";")
        
        elif isinstance(node, ScillaEvent):
            self._write("event ")
            self._generate_expression(node.event)
            self._writeln(";")
        
        elif isinstance(node, ScillaThrow):
            self._write("throw ")
            self._generate_expression(node.exception)
            self._writeln(";")
        
        elif isinstance(node, ScillaAccept):
            self._writeln("accept;")
        
        elif isinstance(node, ScillaMatchStmt):
            self._generate_match_statement(node)
    
    def _generate_match_statement(self, node: ScillaMatchStmt):
        """Generate match statement"""
        self._write("match ")
        self._generate_expression(node.expr)
        self._writeln(" with")
        
        for pattern, statements in node.branches:
            self._write("| ")
            self._generate_pattern(pattern)
            self._writeln(" =>")
            self._indent()
            for stmt in statements:
                self._generate_statement(stmt)
            self._dedent()
        
        self._writeln("end;")
    
    def _generate_expression(self, node: ScillaExpression):
        """Generate expression"""
        if isinstance(node, ScillaIdentifier):
            self._write(node.name)
        
        elif isinstance(node, ScillaLiteral):
            self._generate_literal(node.literal)
        
        elif isinstance(node, ScillaApplication):
            self._generate_expression(node.function)
            for arg in node.args:
                self._write(" ")
                self._generate_expression(arg)
        
        elif isinstance(node, ScillaBuiltinCall):
            self._write(node.builtin)
            if node.type_args:
                self._write(" {")
                type_strs = [self._type_to_string(t) for t in node.type_args]
                self._write(" ".join(type_strs))
                self._write("}")
            for arg in node.args:
                self._write(" ")
                self._generate_expression(arg)
        
        elif isinstance(node, ScillaLet):
            self._generate_let_expression(node)
        
        elif isinstance(node, ScillaMatch):
            self._generate_match_expression(node)
        
        elif isinstance(node, ScillaConstructor):
            self._write("{")
            self._write(node.name)
            for arg in node.args:
                self._write(" ")
                self._generate_expression(arg)
            self._write("}")
        
        elif isinstance(node, ScillaMapAccess):
            self._generate_expression(node.map_expr)
            self._write("[")
            self._generate_expression(node.key)
            self._write("]")
        
        elif isinstance(node, ScillaFieldAccess):
            self._write(node.field)
        
        elif isinstance(node, ScillaMessageConstruction):
            self._generate_message_construction(node)
        
        elif isinstance(node, ScillaEventConstruction):
            self._generate_event_construction(node)
        
        elif isinstance(node, ScillaLambda):
            self._generate_lambda(node)
        
        elif isinstance(node, ScillaTFun):
            self._generate_type_abstraction(node)
        
        elif isinstance(node, ScillaTApp):
            self._generate_expression(node.expr)
            self._write(" @")
            type_strs = [self._type_to_string(t) for t in node.type_args]
            self._write(" @".join(type_strs))
    
    def _generate_literal(self, node):
        """Generate literal values"""
        if isinstance(node, ScillaIntLiteral):
            self._write(node.value)
        
        elif isinstance(node, ScillaStringLiteral):
            self._write(f'"{node.value}"')
        
        elif isinstance(node, ScillaBoolLiteral):
            self._write("True" if node.value else "False")
        
        elif isinstance(node, ScillaByStrLiteral):
            self._write(node.value)
        
        elif isinstance(node, ScillaAddressLiteral):
            self._write(node.value)
    
    def _generate_let_expression(self, node: ScillaLet):
        """Generate let expression"""
        self._writeln("let")
        self._indent()
        
        for pattern, expr in node.bindings:
            self._generate_pattern(pattern)
            self._write(" = ")
            self._generate_expression(expr)
            self._writeln()
        
        self._dedent()
        self._write("in ")
        self._generate_expression(node.body)
    
    def _generate_match_expression(self, node: ScillaMatch):
        """Generate match expression"""
        self._write("match ")
        self._generate_expression(node.expr)
        self._writeln(" with")
        
        for pattern, expr in node.branches:
            self._write("| ")
            self._generate_pattern(pattern)
            self._write(" => ")
            self._generate_expression(expr)
            self._writeln()
        
        self._write("end")
    
    def _generate_pattern(self, node: ScillaPattern):
        """Generate pattern"""
        if isinstance(node, ScillaWildcardPattern):
            self._write("_")
        
        elif isinstance(node, ScillaVariablePattern):
            self._write(node.name)
        
        elif isinstance(node, ScillaConstructorPattern):
            self._write(node.constructor)
            for arg in node.args:
                self._write(" ")
                self._generate_pattern(arg)
        
        elif isinstance(node, ScillaLiteralPattern):
            self._generate_literal(node.literal)
    
    def _generate_message_construction(self, node: ScillaMessageConstruction):
        """Generate message construction"""
        self._write("{")
        
        field_strs = []
        for name, expr in node.fields.items():
            field_str = f"{name} : "
            # Create a temporary output for the expression
            temp_output = StringIO()
            old_output = self.output
            self.output = temp_output
            self._generate_expression(expr)
            expr_str = temp_output.getvalue()
            self.output = old_output
            field_str += expr_str
            field_strs.append(field_str)
        
        self._write("; ".join(field_strs))
        self._write("}")
    
    def _generate_event_construction(self, node: ScillaEventConstruction):
        """Generate event construction"""
        self._write("{")
        self._write(f"_eventname : \"{node.name}\"")
        
        for name, expr in node.params.items():
            self._write(f"; {name} : ")
            self._generate_expression(expr)
        
        self._write("}")
    
    def _generate_lambda(self, node: ScillaLambda):
        """Generate lambda expression"""
        self._write("fun (")
        
        param_strs = []
        for name, param_type in node.params:
            param_str = f"{name} : {self._type_to_string(param_type)}"
            param_strs.append(param_str)
        
        self._write(", ".join(param_strs))
        self._write(") => ")
        self._generate_expression(node.body)
    
    def _generate_type_abstraction(self, node: ScillaTFun):
        """Generate type abstraction"""
        self._write("tfun ")
        for type_var in node.type_vars:
            self._write(f"'{type_var} ")
        self._write("=> ")
        self._generate_expression(node.body)
    
    def _type_to_string(self, scilla_type: ScillaType) -> str:
        """Convert Scilla type to string"""
        if isinstance(scilla_type, ScillaPrimitive):
            return scilla_type.type.value
        
        elif isinstance(scilla_type, ScillaMapType):
            key_str = self._type_to_string(scilla_type.key_type)
            val_str = self._type_to_string(scilla_type.value_type)
            return f"Map {key_str} {val_str}"
        
        elif isinstance(scilla_type, ScillaListType):
            elem_str = self._type_to_string(scilla_type.element_type)
            return f"List {elem_str}"
        
        elif isinstance(scilla_type, ScillaOptionType):
            elem_str = self._type_to_string(scilla_type.element_type)
            return f"Option {elem_str}"
        
        elif isinstance(scilla_type, ScillaPairType):
            first_str = self._type_to_string(scilla_type.first_type)
            second_str = self._type_to_string(scilla_type.second_type)
            return f"Pair {first_str} {second_str}"
        
        elif isinstance(scilla_type, ScillaCustomType):
            if scilla_type.type_args:
                args_str = " ".join(self._type_to_string(t) for t in scilla_type.type_args)
                return f"{scilla_type.name} {args_str}"
            return scilla_type.name
        
        elif isinstance(scilla_type, ScillaFunctionType):
            args_str = " -> ".join(self._type_to_string(t) for t in scilla_type.arg_types)
            ret_str = self._type_to_string(scilla_type.return_type)
            return f"({args_str}) -> {ret_str}"
        
        else:
            return str(scilla_type)


def generate_scilla_code(ast: ScillaProgram, indent_size: int = 2) -> str:
    """Generate Scilla code from AST"""
    generator = ScillaCodeGenerator(indent_size)
    return generator.generate(ast)


def format_scilla_code(code: str) -> str:
    """Format Scilla code for readability"""
    lines = code.split('\n')
    formatted_lines = []
    
    for line in lines:
        # Remove trailing whitespace
        line = line.rstrip()
        
        # Add line if not empty or if it's a meaningful empty line
        if line or (formatted_lines and formatted_lines[-1]):
            formatted_lines.append(line)
    
    # Remove trailing empty lines
    while formatted_lines and not formatted_lines[-1]:
        formatted_lines.pop()
    
    return '\n'.join(formatted_lines) + '\n' 