#!/usr/bin/env python3
"""
Vyper Code Generator

Production-ready Vyper code generator that creates clean, properly formatted Vyper source code
with correct Python-like indentation, syntax, and Vyper coding conventions.
"""

from typing import List, Optional, Any, Union, Dict
from dataclasses import dataclass

from .vyper_ast import *


class VyperCodeStyle:
    """Vyper code style configuration."""
    def __init__(self):
        self.indent_size = 4
        self.use_spaces = True
        self.max_line_length = 88
        self.blank_lines_around_functions = 2
        self.blank_lines_around_classes = 2


class VyperFormatter:
    """Vyper code formatter utilities."""
    
    @staticmethod
    def format_decorator(decorator_name: str) -> str:
        """Format decorator with @ prefix."""
        return f"@{decorator_name}"
    
    @staticmethod
    def format_type_annotation(type_name: str) -> str:
        """Format type annotation for Vyper."""
        return type_name
    
    @staticmethod
    def format_function_signature(name: str, params: str, return_type: Optional[str] = None) -> str:
        """Format function signature."""
        if return_type and return_type != "void":
            return f"def {name}({params}) -> {return_type}:"
        else:
            return f"def {name}({params}):"


class VyperCodeGenerator:
    """Generate Vyper source code from Vyper AST."""
    
    def __init__(self, style: VyperCodeStyle = None):
        self.style = style or VyperCodeStyle()
        self.current_indent = 0
        self.output_lines: List[str] = []
    
    def generate(self, vyper_node: VyperNode) -> str:
        """Generate Vyper source code from AST node."""
        self.output_lines = []
        self.current_indent = 0
        
        if isinstance(vyper_node, VyperModule):
            self.generate_module(vyper_node)
        else:
            self.generate_node(vyper_node)
        
        return '\n'.join(self.output_lines)
    
    def generate_module(self, vyper_module: VyperModule):
        """Generate Vyper module."""
        # Generate imports
        for import_stmt in vyper_module.imports:
            self.generate_import_statement(import_stmt)
        
        # Generate from imports
        for from_import in vyper_module.from_imports:
            self.generate_from_import(from_import)
        
        if vyper_module.imports or vyper_module.from_imports:
            self.add_line("")
        
        # Generate interfaces
        for interface in vyper_module.interfaces:
            self.generate_interface_definition(interface)
            self.add_line("")
        
        # Generate implements statements
        for implements in vyper_module.implements:
            self.generate_implements_statement(implements)
        
        if vyper_module.implements:
            self.add_line("")
        
        # Generate structs
        for struct in vyper_module.structs:
            self.generate_struct_definition(struct)
            self.add_line("")
        
        # Generate enums
        for enum in vyper_module.enums:
            self.generate_enum_definition(enum)
            self.add_line("")
        
        # Generate constants
        for constant in vyper_module.constants:
            self.generate_constant_declaration(constant)
        
        if vyper_module.constants:
            self.add_line("")
        
        # Generate immutables
        for immutable in vyper_module.immutables:
            self.generate_immutable_declaration(immutable)
        
        if vyper_module.immutables:
            self.add_line("")
        
        # Generate state variables
        for state_var in vyper_module.state_variables:
            self.generate_state_variable(state_var)
        
        if vyper_module.state_variables:
            self.add_line("")
        
        # Generate events
        for event in vyper_module.events:
            self.generate_event_definition(event)
            self.add_line("")
        
        # Generate functions
        for i, function in enumerate(vyper_module.functions):
            if i > 0:
                for _ in range(self.style.blank_lines_around_functions):
                    self.add_line("")
            self.generate_function_definition(function)
    
    def generate_import_statement(self, import_stmt: VyperImportStatement):
        """Generate import statement."""
        if import_stmt.alias:
            self.add_line(f"import {import_stmt.module} as {import_stmt.alias}")
        else:
            self.add_line(f"import {import_stmt.module}")
    
    def generate_from_import(self, from_import: VyperFromImport):
        """Generate from import statement."""
        names_with_aliases = []
        for i, name in enumerate(from_import.names):
            if i < len(from_import.aliases) and from_import.aliases[i]:
                names_with_aliases.append(f"{name} as {from_import.aliases[i]}")
            else:
                names_with_aliases.append(name)
        
        names_str = ", ".join(names_with_aliases)
        self.add_line(f"from {from_import.module} import {names_str}")
    
    def generate_interface_definition(self, interface: VyperInterfaceDefinition):
        """Generate interface definition."""
        self.add_line(f"interface {interface.name}:")
        self.current_indent += 1
        
        if not interface.functions and not interface.events:
            self.add_line("pass")
        else:
            # Generate functions
            for function in interface.functions:
                self.generate_function_signature_only(function)
            
            # Generate events
            for event in interface.events:
                self.generate_event_definition(event)
        
        self.current_indent -= 1
    
    def generate_implements_statement(self, implements: VyperImplementsStatement):
        """Generate implements statement."""
        self.add_line(f"implements: {implements.interface_name}")
    
    def generate_struct_definition(self, struct: VyperStructDefinition):
        """Generate struct definition."""
        self.add_line(f"struct {struct.name}:")
        self.current_indent += 1
        
        if not struct.fields:
            self.add_line("pass")
        else:
            for field in struct.fields:
                field_type = self.generate_type_name(field.type_annotation)
                self.add_line(f"{field.name}: {field_type}")
        
        self.current_indent -= 1
    
    def generate_enum_definition(self, enum: VyperEnumDefinition):
        """Generate enum definition."""
        self.add_line(f"enum {enum.name}:")
        self.current_indent += 1
        
        if not enum.values:
            self.add_line("pass")
        else:
            for value in enum.values:
                self.add_line(value)
        
        self.current_indent -= 1
    
    def generate_constant_declaration(self, constant: VyperConstantDeclaration):
        """Generate constant declaration."""
        type_str = self.generate_type_name(constant.type_annotation)
        value_str = self.generate_node(constant.value)
        self.add_line(f"{constant.name}: constant({type_str}) = {value_str}")
    
    def generate_immutable_declaration(self, immutable: VyperImmutableDeclaration):
        """Generate immutable declaration."""
        type_str = self.generate_type_name(immutable.type_annotation)
        self.add_line(f"{immutable.name}: immutable({type_str})")
    
    def generate_state_variable(self, state_var: VyperStateVariable):
        """Generate state variable declaration."""
        type_str = self.generate_type_name(state_var.type_annotation)
        
        if state_var.is_public:
            var_line = f"{state_var.name}: public({type_str})"
        else:
            var_line = f"{state_var.name}: {type_str}"
        
        if state_var.initial_value:
            value_str = self.generate_node(state_var.initial_value)
            var_line += f" = {value_str}"
        
        self.add_line(var_line)
    
    def generate_event_definition(self, event: VyperEventDefinition):
        """Generate event definition."""
        self.add_line(f"event {event.name}:")
        self.current_indent += 1
        
        if not event.parameters:
            self.add_line("pass")
        else:
            for param in event.parameters:
                param_type = self.generate_type_name(param.type_annotation)
                # Check for indexed modifier (Vyper uses indexed for event params)
                param_line = f"{param.name}: {param_type}"
                self.add_line(param_line)
        
        self.current_indent -= 1
    
    def generate_function_definition(self, function: VyperFunctionDefinition):
        """Generate function definition."""
        # Generate decorators
        for decorator in function.decorators:
            decorator_line = VyperFormatter.format_decorator(decorator.name)
            self.add_line(decorator_line)
        
        # Generate function signature
        params = ""
        if function.parameters:
            params = self.generate_parameter_list(function.parameters)
        
        return_type = None
        if function.return_type:
            return_type = self.generate_type_name(function.return_type)
        
        func_signature = VyperFormatter.format_function_signature(
            function.name, params, return_type
        )
        self.add_line(func_signature)
        
        # Generate function body
        self.current_indent += 1
        
        if not function.body:
            self.add_line("pass")
        else:
            for stmt in function.body:
                self.generate_statement(stmt)
        
        self.current_indent -= 1
    
    def generate_function_signature_only(self, function: VyperFunctionDefinition):
        """Generate function signature without body (for interfaces)."""
        # Generate decorators
        for decorator in function.decorators:
            decorator_line = VyperFormatter.format_decorator(decorator.name)
            self.add_line(decorator_line)
        
        # Generate function signature
        params = ""
        if function.parameters:
            params = self.generate_parameter_list(function.parameters)
        
        return_type = None
        if function.return_type:
            return_type = self.generate_type_name(function.return_type)
        
        func_signature = VyperFormatter.format_function_signature(
            function.name, params, return_type
        )
        self.add_line(func_signature)
        self.current_indent += 1
        self.add_line("...")
        self.current_indent -= 1
    
    def generate_parameter_list(self, param_list: VyperParameterList) -> str:
        """Generate parameter list."""
        params = []
        
        for param in param_list.parameters:
            param_type = self.generate_type_name(param.type_annotation)
            param_str = f"{param.name}: {param_type}"
            
            if param.default_value:
                default_str = self.generate_node(param.default_value)
                param_str += f" = {default_str}"
            
            params.append(param_str)
        
        return ", ".join(params)
    
    def generate_statement(self, stmt: VyperStatement):
        """Generate statement."""
        if isinstance(stmt, VyperExpressionStatement):
            expr_str = self.generate_node(stmt.expression)
            self.add_line(expr_str)
        
        elif isinstance(stmt, VyperAssignmentStatement):
            target_str = self.generate_node(stmt.target)
            value_str = self.generate_node(stmt.value)
            self.add_line(f"{target_str} = {value_str}")
        
        elif isinstance(stmt, VyperAugmentedAssignment):
            target_str = self.generate_node(stmt.target)
            value_str = self.generate_node(stmt.value)
            op_str = stmt.operator.value
            self.add_line(f"{target_str} {op_str} {value_str}")
        
        elif isinstance(stmt, VyperIfStatement):
            self.generate_if_statement(stmt)
        
        elif isinstance(stmt, VyperForLoop):
            self.generate_for_loop(stmt)
        
        elif isinstance(stmt, VyperReturnStatement):
            if stmt.value:
                value_str = self.generate_node(stmt.value)
                self.add_line(f"return {value_str}")
            else:
                self.add_line("return")
        
        elif isinstance(stmt, VyperAssertStatement):
            test_str = self.generate_node(stmt.test)
            if stmt.msg:
                msg_str = self.generate_node(stmt.msg)
                self.add_line(f"assert {test_str}, {msg_str}")
            else:
                self.add_line(f"assert {test_str}")
        
        elif isinstance(stmt, VyperRaiseStatement):
            if stmt.exc:
                exc_str = self.generate_node(stmt.exc)
                self.add_line(f"raise {exc_str}")
            else:
                self.add_line("raise")
        
        elif isinstance(stmt, VyperLogStatement):
            event_call_str = self.generate_node(stmt.event_call)
            self.add_line(f"log {event_call_str}")
        
        elif isinstance(stmt, VyperBreakStatement):
            self.add_line("break")
        
        elif isinstance(stmt, VyperContinueStatement):
            self.add_line("continue")
        
        elif isinstance(stmt, VyperPassStatement):
            self.add_line("pass")
        
        else:
            # Fallback
            self.add_line(f"# Unknown statement: {type(stmt).__name__}")
    
    def generate_if_statement(self, if_stmt: VyperIfStatement):
        """Generate if statement."""
        condition_str = self.generate_node(if_stmt.condition)
        self.add_line(f"if {condition_str}:")
        
        self.current_indent += 1
        if not if_stmt.body:
            self.add_line("pass")
        else:
            for stmt in if_stmt.body:
                self.generate_statement(stmt)
        self.current_indent -= 1
        
        if if_stmt.orelse:
            self.add_line("else:")
            self.current_indent += 1
            for stmt in if_stmt.orelse:
                self.generate_statement(stmt)
            self.current_indent -= 1
    
    def generate_for_loop(self, for_loop: VyperForLoop):
        """Generate for loop."""
        target_str = self.generate_node(for_loop.target)
        iter_str = self.generate_node(for_loop.iter)
        self.add_line(f"for {target_str} in {iter_str}:")
        
        self.current_indent += 1
        if not for_loop.body:
            self.add_line("pass")
        else:
            for stmt in for_loop.body:
                self.generate_statement(stmt)
        self.current_indent -= 1
    
    def generate_node(self, node: VyperNode) -> str:
        """Generate code for any Vyper AST node."""
        if isinstance(node, VyperIdentifier):
            return node.name
        
        elif isinstance(node, VyperLiteral):
            return self.generate_literal(node)
        
        elif isinstance(node, VyperBinaryExpression):
            return self.generate_binary_expression(node)
        
        elif isinstance(node, VyperUnaryExpression):
            return self.generate_unary_expression(node)
        
        elif isinstance(node, VyperFunctionCall):
            return self.generate_function_call(node)
        
        elif isinstance(node, VyperAttributeAccess):
            return self.generate_attribute_access(node)
        
        elif isinstance(node, VyperSubscriptAccess):
            return self.generate_subscript_access(node)
        
        elif isinstance(node, VyperListExpression):
            return self.generate_list_expression(node)
        
        elif isinstance(node, VyperDictExpression):
            return self.generate_dict_expression(node)
        
        elif isinstance(node, VyperTupleExpression):
            return self.generate_tuple_expression(node)
        
        else:
            return f"# Unknown node: {type(node).__name__}"
    
    def generate_literal(self, literal: VyperLiteral) -> str:
        """Generate literal value."""
        if literal.type_name == "string":
            # Escape quotes and return as string literal
            escaped_value = str(literal.value).replace('"', '\\"')
            return f'"{escaped_value}"'
        elif literal.type_name == "bool":
            return "True" if literal.value else "False"
        elif literal.type_name == "number":
            return str(literal.value)
        else:
            return str(literal.value)
    
    def generate_binary_expression(self, bin_expr: VyperBinaryExpression) -> str:
        """Generate binary expression."""
        left_str = self.generate_node(bin_expr.left)
        right_str = self.generate_node(bin_expr.right)
        op_str = bin_expr.operator.value
        
        # Handle operator precedence with parentheses if needed
        return f"({left_str} {op_str} {right_str})"
    
    def generate_unary_expression(self, unary_expr: VyperUnaryExpression) -> str:
        """Generate unary expression."""
        operand_str = self.generate_node(unary_expr.operand)
        op_str = unary_expr.operator.value
        
        if unary_expr.operator in [VyperOperator.NOT]:
            return f"{op_str} {operand_str}"
        else:
            return f"{op_str}{operand_str}"
    
    def generate_function_call(self, func_call: VyperFunctionCall) -> str:
        """Generate function call."""
        func_str = self.generate_node(func_call.func)
        
        args = []
        
        # Positional arguments
        for arg in func_call.args:
            args.append(self.generate_node(arg))
        
        # Keyword arguments
        for keyword in func_call.keywords:
            value_str = self.generate_node(keyword.value)
            args.append(f"{keyword.arg}={value_str}")
        
        args_str = ", ".join(args)
        return f"{func_str}({args_str})"
    
    def generate_attribute_access(self, attr_access: VyperAttributeAccess) -> str:
        """Generate attribute access."""
        value_str = self.generate_node(attr_access.value)
        return f"{value_str}.{attr_access.attr}"
    
    def generate_subscript_access(self, subscript: VyperSubscriptAccess) -> str:
        """Generate subscript access."""
        value_str = self.generate_node(subscript.value)
        
        if subscript.slice.upper is None and subscript.slice.step is None:
            # Simple index
            index_str = self.generate_node(subscript.slice.lower)
            return f"{value_str}[{index_str}]"
        else:
            # Slice
            slice_parts = []
            if subscript.slice.lower:
                slice_parts.append(self.generate_node(subscript.slice.lower))
            else:
                slice_parts.append("")
            
            if subscript.slice.upper:
                slice_parts.append(self.generate_node(subscript.slice.upper))
            else:
                slice_parts.append("")
            
            if subscript.slice.step:
                slice_parts.append(self.generate_node(subscript.slice.step))
            
            slice_str = ":".join(slice_parts)
            return f"{value_str}[{slice_str}]"
    
    def generate_list_expression(self, list_expr: VyperListExpression) -> str:
        """Generate list expression."""
        elements = [self.generate_node(elem) for elem in list_expr.elements]
        return f"[{', '.join(elements)}]"
    
    def generate_dict_expression(self, dict_expr: VyperDictExpression) -> str:
        """Generate dictionary expression."""
        pairs = []
        for key, value in zip(dict_expr.keys, dict_expr.values):
            key_str = self.generate_node(key)
            value_str = self.generate_node(value)
            pairs.append(f"{key_str}: {value_str}")
        
        return f"{{{', '.join(pairs)}}}"
    
    def generate_tuple_expression(self, tuple_expr: VyperTupleExpression) -> str:
        """Generate tuple expression."""
        elements = [self.generate_node(elem) for elem in tuple_expr.elements]
        if len(elements) == 1:
            return f"({elements[0]},)"  # Single element tuple needs comma
        else:
            return f"({', '.join(elements)})"
    
    def generate_type_name(self, type_name: VyperTypeName) -> str:
        """Generate type name."""
        if isinstance(type_name, VyperPrimitiveTypeName):
            return type_name.name.value
        
        elif isinstance(type_name, VyperArrayType):
            element_type = self.generate_type_name(type_name.element_type)
            if type_name.size:
                size_str = self.generate_node(type_name.size)
                return f"{element_type}[{size_str}]"
            else:
                return f"{element_type}[]"
        
        elif isinstance(type_name, VyperDynArrayType):
            element_type = self.generate_type_name(type_name.element_type)
            max_size_str = self.generate_node(type_name.max_size)
            return f"DynArray[{element_type}, {max_size_str}]"
        
        elif isinstance(type_name, VyperHashMapType):
            key_type = self.generate_type_name(type_name.key_type)
            value_type = self.generate_type_name(type_name.value_type)
            return f"HashMap[{key_type}, {value_type}]"
        
        elif isinstance(type_name, VyperStructType):
            return type_name.name
        
        elif isinstance(type_name, VyperInterfaceType):
            return type_name.name
        
        else:
            return str(type_name)
    
    def add_line(self, line: str):
        """Add a line to output with proper indentation."""
        if line.strip():  # Don't indent empty lines
            indented_line = " " * (self.current_indent * self.style.indent_size) + line
            self.output_lines.append(indented_line)
        else:
            self.output_lines.append("")


# Convenience functions for external use
def generate_vyper_code(vyper_ast: VyperNode, style: VyperCodeStyle = None) -> str:
    """Generate Vyper source code from AST."""
    generator = VyperCodeGenerator(style)
    return generator.generate(vyper_ast)


def generate_vyper(vyper_ast: VyperNode) -> str:
    """Generate Vyper source code (convenience function)."""
    return generate_vyper_code(vyper_ast) 