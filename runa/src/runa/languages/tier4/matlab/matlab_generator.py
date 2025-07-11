#!/usr/bin/env python3
"""
Matlab Code Generator

Generates Matlab source code from Matlab AST with proper formatting,
indentation, and Matlab-specific syntax rules.
"""

from typing import List, Optional, Dict, Any, Union
from io import StringIO

from .matlab_ast import *


class MatlabCodeGenerator:
    """Generates Matlab code from AST."""
    
    def __init__(self, indent_size: int = 4):
        self.indent_size = indent_size
        self.indent_level = 0
        self.output = StringIO()
        
    def generate(self, node: MatlabNode) -> str:
        """Generate Matlab code from AST node."""
        self.output = StringIO()
        self.indent_level = 0
        
        if isinstance(node, MatlabScript):
            self.generate_script(node)
        elif isinstance(node, MatlabFunctionFile):
            self.generate_function_file(node)
        elif isinstance(node, MatlabClassFile):
            self.generate_class_file(node)
        elif isinstance(node, MatlabProgram):
            self.generate_program(node)
        else:
            self.visit_node(node)
        
        return self.output.getvalue()
    
    def write(self, text: str) -> None:
        """Write text to output."""
        self.output.write(text)
    
    def writeln(self, text: str = "") -> None:
        """Write line with proper indentation."""
        if text:
            self.write(' ' * (self.indent_level * self.indent_size) + text + '\n')
        else:
            self.write('\n')
    
    def indent(self) -> None:
        """Increase indentation level."""
        self.indent_level += 1
    
    def dedent(self) -> None:
        """Decrease indentation level."""
        self.indent_level = max(0, self.indent_level - 1)
    
    def generate_script(self, node: MatlabScript) -> None:
        """Generate Matlab script."""
        # Generate comments first
        for comment in node.comments:
            self.generate_comment(comment)
        
        # Generate statements
        for i, stmt in enumerate(node.statements):
            if i > 0:
                self.writeln()
            self.visit_node(stmt)
    
    def generate_function_file(self, node: MatlabFunctionFile) -> None:
        """Generate Matlab function file."""
        # Generate comments
        for comment in node.comments:
            self.generate_comment(comment)
        
        # Generate main function
        if node.main_function:
            self.visit_node(node.main_function)
        
        # Generate nested functions
        for nested_func in node.nested_functions:
            self.writeln()
            self.writeln()
            self.visit_node(nested_func)
    
    def generate_class_file(self, node: MatlabClassFile) -> None:
        """Generate Matlab class file."""
        # Generate comments
        for comment in node.comments:
            self.generate_comment(comment)
        
        # Generate class
        if node.class_declaration:
            self.visit_node(node.class_declaration)
    
    def generate_program(self, node: MatlabProgram) -> None:
        """Generate complete Matlab program."""
        for i, file_node in enumerate(node.files):
            if i > 0:
                self.writeln()
                self.writeln("% =" + "="*70)
                self.writeln()
            self.visit_node(file_node)
    
    def visit_node(self, node: MatlabNode) -> None:
        """Visit any Matlab AST node."""
        if isinstance(node, MatlabFunctionDeclaration):
            self.generate_function_declaration(node)
        elif isinstance(node, MatlabClassDeclaration):
            self.generate_class_declaration(node)
        elif isinstance(node, MatlabIfStatement):
            self.generate_if_statement(node)
        elif isinstance(node, MatlabForLoop):
            self.generate_for_loop(node)
        elif isinstance(node, MatlabWhileLoop):
            self.generate_while_loop(node)
        elif isinstance(node, MatlabTryCatchStatement):
            self.generate_try_catch(node)
        elif isinstance(node, MatlabSwitchStatement):
            self.generate_switch_statement(node)
        elif isinstance(node, MatlabAssignmentExpression):
            self.generate_assignment(node)
        elif isinstance(node, MatlabBreakStatement):
            self.writeln("break")
        elif isinstance(node, MatlabContinueStatement):
            self.writeln("continue")
        elif isinstance(node, MatlabReturnStatement):
            self.writeln("return")
        elif isinstance(node, MatlabGlobalDeclaration):
            self.generate_global_declaration(node)
        elif isinstance(node, MatlabPersistentDeclaration):
            self.generate_persistent_declaration(node)
        elif isinstance(node, MatlabComment):
            self.generate_comment(node)
        elif isinstance(node, MatlabExpression):
            self.generate_expression(node)
        else:
            # Fallback for unknown nodes
            pass
    
    def generate_function_declaration(self, node: MatlabFunctionDeclaration) -> None:
        """Generate function declaration."""
        # Function signature
        func_line = "function "
        
        # Output parameters
        if node.output_parameters:
            if len(node.output_parameters) == 1:
                func_line += node.output_parameters[0] + " = "
            else:
                func_line += "[" + ", ".join(node.output_parameters) + "] = "
        
        # Function name
        func_line += node.name
        
        # Input parameters
        if node.input_parameters:
            func_line += "(" + ", ".join(node.input_parameters) + ")"
        
        self.writeln(func_line)
        
        # Help comments
        for help_comment in node.help_comments:
            self.writeln(f"% {help_comment}")
        
        if node.help_comments:
            self.writeln()
        
        # Function body
        self.indent()
        for stmt in node.body:
            self.visit_node(stmt)
        self.dedent()
        
        self.writeln("end")
    
    def generate_class_declaration(self, node: MatlabClassDeclaration) -> None:
        """Generate class declaration."""
        # Class signature
        class_line = "classdef "
        
        # Class attributes
        if node.attributes:
            attr_list = []
            for key, value in node.attributes.items():
                if isinstance(value, bool):
                    attr_list.append(f"{key} = {str(value).lower()}")
                else:
                    attr_list.append(f"{key} = {value}")
            
            if attr_list:
                class_line += "(" + ", ".join(attr_list) + ") "
        
        class_line += node.name
        
        # Superclasses
        if node.superclasses:
            class_line += " < " + " & ".join(node.superclasses)
        
        self.writeln(class_line)
        
        self.indent()
        
        # Properties blocks
        for props_block in node.properties_blocks:
            self.generate_properties_block(props_block)
            self.writeln()
        
        # Methods blocks
        for methods_block in node.methods_blocks:
            self.generate_methods_block(methods_block)
            self.writeln()
        
        # Events blocks
        for events_block in node.events_blocks:
            self.generate_events_block(events_block)
            self.writeln()
        
        # Enumeration blocks
        for enum_block in node.enumeration_blocks:
            self.generate_enumeration_block(enum_block)
            self.writeln()
        
        self.dedent()
        self.writeln("end")
    
    def generate_properties_block(self, node: MatlabPropertiesBlock) -> None:
        """Generate properties block."""
        props_line = "properties"
        
        # Attributes
        if node.attributes:
            attr_list = []
            for key, value in node.attributes.items():
                if isinstance(value, bool):
                    attr_list.append(f"{key} = {str(value).lower()}")
                else:
                    attr_list.append(f"{key} = {value}")
            
            if attr_list:
                props_line += "(" + ", ".join(attr_list) + ")"
        
        self.writeln(props_line)
        
        self.indent()
        for prop in node.properties:
            self.generate_property_declaration(prop)
        self.dedent()
        
        self.writeln("end")
    
    def generate_property_declaration(self, node: MatlabPropertyDeclaration) -> None:
        """Generate property declaration."""
        prop_line = node.name
        
        if node.default_value:
            prop_line += " = " + self.expression_to_string(node.default_value)
        
        self.writeln(prop_line)
    
    def generate_methods_block(self, node: MatlabMethodsBlock) -> None:
        """Generate methods block."""
        methods_line = "methods"
        
        # Attributes
        if node.attributes:
            attr_list = []
            for key, value in node.attributes.items():
                if isinstance(value, bool):
                    attr_list.append(f"{key} = {str(value).lower()}")
                else:
                    attr_list.append(f"{key} = {value}")
            
            if attr_list:
                methods_line += "(" + ", ".join(attr_list) + ")"
        
        self.writeln(methods_line)
        
        self.indent()
        for i, method in enumerate(node.methods):
            if i > 0:
                self.writeln()
            self.generate_method_declaration(method)
        self.dedent()
        
        self.writeln("end")
    
    def generate_method_declaration(self, node: MatlabMethodDeclaration) -> None:
        """Generate method declaration."""
        # Method signature
        method_line = "function "
        
        # Output parameters
        if node.output_parameters:
            if len(node.output_parameters) == 1:
                method_line += node.output_parameters[0] + " = "
            else:
                method_line += "[" + ", ".join(node.output_parameters) + "] = "
        
        # Method name
        method_line += node.name
        
        # Input parameters
        if node.input_parameters:
            method_line += "(" + ", ".join(node.input_parameters) + ")"
        
        self.writeln(method_line)
        
        # Method body
        self.indent()
        for stmt in node.body:
            self.visit_node(stmt)
        self.dedent()
        
        self.writeln("end")
    
    def generate_events_block(self, node: MatlabEventsBlock) -> None:
        """Generate events block."""
        events_line = "events"
        
        # Attributes
        if node.attributes:
            attr_list = []
            for key, value in node.attributes.items():
                if isinstance(value, bool):
                    attr_list.append(f"{key} = {str(value).lower()}")
                else:
                    attr_list.append(f"{key} = {value}")
            
            if attr_list:
                events_line += "(" + ", ".join(attr_list) + ")"
        
        self.writeln(events_line)
        
        self.indent()
        for event in node.events:
            self.writeln(event)
        self.dedent()
        
        self.writeln("end")
    
    def generate_enumeration_block(self, node: MatlabEnumerationBlock) -> None:
        """Generate enumeration block."""
        self.writeln("enumeration")
        
        self.indent()
        for value in node.values:
            self.writeln(value)
        self.dedent()
        
        self.writeln("end")
    
    def generate_if_statement(self, node: MatlabIfStatement) -> None:
        """Generate if statement."""
        # If clause
        if_line = "if " + self.expression_to_string(node.condition)
        self.writeln(if_line)
        
        self.indent()
        for stmt in node.then_body:
            self.visit_node(stmt)
        self.dedent()
        
        # Elseif clauses
        for elseif in node.elseif_clauses:
            elseif_line = "elseif " + self.expression_to_string(elseif.condition)
            self.writeln(elseif_line)
            
            self.indent()
            for stmt in elseif.body:
                self.visit_node(stmt)
            self.dedent()
        
        # Else clause
        if node.else_body:
            self.writeln("else")
            
            self.indent()
            for stmt in node.else_body:
                self.visit_node(stmt)
            self.dedent()
        
        self.writeln("end")
    
    def generate_for_loop(self, node: MatlabForLoop) -> None:
        """Generate for loop."""
        for_line = f"for {node.variable} = {self.expression_to_string(node.iterable)}"
        self.writeln(for_line)
        
        self.indent()
        for stmt in node.body:
            self.visit_node(stmt)
        self.dedent()
        
        self.writeln("end")
    
    def generate_while_loop(self, node: MatlabWhileLoop) -> None:
        """Generate while loop."""
        while_line = "while " + self.expression_to_string(node.condition)
        self.writeln(while_line)
        
        self.indent()
        for stmt in node.body:
            self.visit_node(stmt)
        self.dedent()
        
        self.writeln("end")
    
    def generate_try_catch(self, node: MatlabTryCatchStatement) -> None:
        """Generate try-catch statement."""
        self.writeln("try")
        
        self.indent()
        for stmt in node.try_body:
            self.visit_node(stmt)
        self.dedent()
        
        catch_line = "catch"
        if node.exception_variable:
            catch_line += f" {node.exception_variable}"
        self.writeln(catch_line)
        
        self.indent()
        for stmt in node.catch_body:
            self.visit_node(stmt)
        self.dedent()
        
        self.writeln("end")
    
    def generate_switch_statement(self, node: MatlabSwitchStatement) -> None:
        """Generate switch statement."""
        switch_line = "switch " + self.expression_to_string(node.expression)
        self.writeln(switch_line)
        
        self.indent()
        
        # Case clauses
        for case in node.case_clauses:
            if len(case.values) == 1:
                case_line = "case " + self.expression_to_string(case.values[0])
            else:
                values_str = "{" + ", ".join(self.expression_to_string(v) for v in case.values) + "}"
                case_line = "case " + values_str
            
            self.writeln(case_line)
            
            self.indent()
            for stmt in case.body:
                self.visit_node(stmt)
            self.dedent()
        
        # Otherwise clause
        if node.otherwise_clause:
            self.writeln("otherwise")
            
            self.indent()
            for stmt in node.otherwise_clause.body:
                self.visit_node(stmt)
            self.dedent()
        
        self.dedent()
        self.writeln("end")
    
    def generate_assignment(self, node: MatlabAssignmentExpression) -> None:
        """Generate assignment expression."""
        # Left side
        if len(node.targets) == 1:
            left_side = self.expression_to_string(node.targets[0])
        else:
            targets_str = ", ".join(self.expression_to_string(t) for t in node.targets)
            left_side = f"[{targets_str}]"
        
        # Right side
        right_side = self.expression_to_string(node.value)
        
        assignment_line = f"{left_side} = {right_side}"
        self.writeln(assignment_line)
    
    def generate_global_declaration(self, node: MatlabGlobalDeclaration) -> None:
        """Generate global declaration."""
        global_line = "global " + " ".join(node.variables)
        self.writeln(global_line)
    
    def generate_persistent_declaration(self, node: MatlabPersistentDeclaration) -> None:
        """Generate persistent declaration."""
        persistent_line = "persistent " + " ".join(node.variables)
        self.writeln(persistent_line)
    
    def generate_comment(self, node: MatlabComment) -> None:
        """Generate comment."""
        if node.is_block_comment:
            self.writeln(f"%{{{node.text}%}}")
        else:
            self.writeln(f"% {node.text}")
    
    def generate_expression(self, node: MatlabExpression) -> None:
        """Generate expression statement."""
        expr_str = self.expression_to_string(node)
        self.writeln(expr_str)
    
    def expression_to_string(self, node: Optional[MatlabExpression]) -> str:
        """Convert expression to string."""
        if node is None:
            return ""
        
        if isinstance(node, MatlabIdentifier):
            return node.name
        
        elif isinstance(node, MatlabLiteralExpression):
            if node.literal_type == "logical":
                return "true" if node.value else "false"
            elif isinstance(node.value, str):
                return f"'{node.value}'"
            else:
                return str(node.value)
        
        elif isinstance(node, MatlabStringExpression):
            if node.is_char_array:
                return f"'{node.value}'"
            else:
                return f'"{node.value}"'
        
        elif isinstance(node, MatlabBinaryExpression):
            left = self.expression_to_string(node.left)
            right = self.expression_to_string(node.right)
            return f"({left} {node.operator} {right})"
        
        elif isinstance(node, MatlabUnaryExpression):
            expr = self.expression_to_string(node.expression)
            if node.is_postfix:
                return f"({expr}{node.operator})"
            else:
                return f"({node.operator}{expr})"
        
        elif isinstance(node, MatlabFunctionCall):
            func = self.expression_to_string(node.function)
            args = ", ".join(self.expression_to_string(arg) for arg in node.arguments)
            return f"{func}({args})"
        
        elif isinstance(node, MatlabMethodCall):
            obj = self.expression_to_string(node.object)
            args = ", ".join(self.expression_to_string(arg) for arg in node.arguments)
            return f"{obj}.{node.method_name}({args})"
        
        elif isinstance(node, MatlabFieldAccess):
            obj = self.expression_to_string(node.object)
            return f"{obj}.{node.field_name}"
        
        elif isinstance(node, MatlabMatrixExpression):
            if not node.rows:
                return "[]"
            
            rows_str = []
            for row in node.rows:
                row_str = ", ".join(self.expression_to_string(expr) for expr in row)
                rows_str.append(row_str)
            
            return "[" + "; ".join(rows_str) + "]"
        
        elif isinstance(node, MatlabCellArray):
            if not node.rows:
                return "{}"
            
            rows_str = []
            for row in node.rows:
                row_str = ", ".join(self.expression_to_string(expr) for expr in row)
                rows_str.append(row_str)
            
            return "{" + "; ".join(rows_str) + "}"
        
        elif isinstance(node, MatlabIndexingExpression):
            array = self.expression_to_string(node.array)
            indices = ", ".join(self.expression_to_string(idx) for idx in node.indices)
            
            if node.indexing_type == "paren":
                return f"{array}({indices})"
            elif node.indexing_type == "brace":
                return f"{array}{{{indices}}}"
            else:  # dot
                return f"{array}.{indices}"
        
        elif isinstance(node, MatlabSliceExpression):
            if node.is_colon:
                return ":"
            
            parts = []
            if node.start:
                parts.append(self.expression_to_string(node.start))
            if node.step:
                parts.append(self.expression_to_string(node.step))
            if node.stop:
                parts.append(self.expression_to_string(node.stop))
            
            return ":".join(parts)
        
        elif isinstance(node, MatlabAnonymousFunction):
            params = ", ".join(node.parameters)
            expr = self.expression_to_string(node.expression)
            return f"@({params}) {expr}"
        
        elif isinstance(node, MatlabFunctionHandle):
            return f"@{node.function_name}"
        
        else:
            return str(node)


def generate_matlab_code(node: MatlabNode, indent_size: int = 4) -> str:
    """Generate Matlab code from AST node."""
    generator = MatlabCodeGenerator(indent_size)
    return generator.generate(node) 