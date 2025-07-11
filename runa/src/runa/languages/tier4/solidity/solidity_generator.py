#!/usr/bin/env python3
"""
Solidity Code Generator

Production-ready Solidity code generator that creates clean, properly formatted Solidity source code
with correct indentation, syntax, and Solidity coding conventions.
"""

from typing import List, Optional, Any, Union, Dict
from dataclasses import dataclass

from .solidity_ast import *


class SolidityCodeGenerator:
    """Generate Solidity source code from Solidity AST."""
    
    def __init__(self, indent_size: int = 4):
        self.indent_size = indent_size
        self.current_indent = 0
        self.output_lines: List[str] = []
    
    def generate(self, sol_node: SolidityNode) -> str:
        """Generate Solidity source code from AST node."""
        self.output_lines = []
        self.current_indent = 0
        
        if isinstance(sol_node, SoliditySourceUnit):
            self.generate_source_unit(sol_node)
        else:
            self.generate_node(sol_node)
        
        return '\n'.join(self.output_lines)
    
    def generate_source_unit(self, sol_unit: SoliditySourceUnit):
        """Generate Solidity source unit."""
        # Generate pragma directives
        for pragma in sol_unit.pragma_directives:
            self.generate_pragma_directive(pragma)
        
        if sol_unit.pragma_directives:
            self.add_line("")
        
        # Generate import directives
        for import_dir in sol_unit.import_directives:
            self.generate_import_directive(import_dir)
        
        if sol_unit.import_directives:
            self.add_line("")
        
        # Generate contracts
        for i, contract in enumerate(sol_unit.contracts):
            if i > 0:
                self.add_line("")
            self.generate_contract_definition(contract)
        
        # Generate interfaces
        for interface in sol_unit.interfaces:
            self.add_line("")
            self.generate_interface_definition(interface)
        
        # Generate libraries
        for library in sol_unit.libraries:
            self.add_line("")
            self.generate_library_definition(library)
    
    def generate_pragma_directive(self, pragma: SolidityPragmaDirective):
        """Generate pragma directive."""
        self.add_line(f"pragma {pragma.name} {pragma.value};")
    
    def generate_import_directive(self, import_dir: SolidityImportDirective):
        """Generate import directive."""
        if import_dir.alias:
            self.add_line(f'import "{import_dir.path}" as {import_dir.alias};')
        else:
            self.add_line(f'import "{import_dir.path}";')
    
    def generate_contract_definition(self, contract: SolidityContractDefinition):
        """Generate contract definition."""
        # Contract header
        contract_line = f"contract {contract.name}"
        
        # Add inheritance
        if contract.inheritance:
            inherited = [inh.base_name for inh in contract.inheritance]
            contract_line += f" is {', '.join(inherited)}"
        
        contract_line += " {"
        self.add_line(contract_line)
        self.current_indent += 1
        
        # State variables
        if contract.state_variables:
            for state_var in contract.state_variables:
                self.generate_state_variable(state_var)
            self.add_line("")
        
        # Events
        if contract.events:
            for event in contract.events:
                self.generate_event_definition(event)
            self.add_line("")
        
        # Errors
        if contract.errors:
            for error in contract.errors:
                self.generate_error_definition(error)
            self.add_line("")
        
        # Modifiers
        if contract.modifiers:
            for modifier in contract.modifiers:
                self.generate_modifier_definition(modifier)
                self.add_line("")
        
        # Constructor
        if contract.constructor:
            self.generate_constructor_definition(contract.constructor)
            self.add_line("")
        
        # Functions
        for i, function in enumerate(contract.functions):
            if i > 0:
                self.add_line("")
            self.generate_function_definition(function)
        
        self.current_indent -= 1
        self.add_line("}")
    
    def generate_interface_definition(self, interface: SolidityInterfaceDefinition):
        """Generate interface definition."""
        self.add_line(f"interface {interface.name} {{")
        self.current_indent += 1
        
        # Functions (interface functions have no body)
        for function in interface.functions:
            self.generate_function_signature(function)
        
        self.current_indent -= 1
        self.add_line("}")
    
    def generate_library_definition(self, library: SolidityLibraryDefinition):
        """Generate library definition."""
        self.add_line(f"library {library.name} {{")
        self.current_indent += 1
        
        # Library functions
        for function in library.functions:
            self.generate_function_definition(function)
            self.add_line("")
        
        self.current_indent -= 1
        self.add_line("}")
    
    def generate_state_variable(self, state_var: SolidityStateVariable):
        """Generate state variable declaration."""
        var_line = ""
        
        # Type
        type_str = self.generate_type_name(state_var.type_name)
        var_line += type_str
        
        # Visibility
        if state_var.visibility:
            var_line += f" {state_var.visibility.value}"
        
        # Modifiers
        if state_var.is_constant:
            var_line += " constant"
        
        if state_var.is_immutable:
            var_line += " immutable"
        
        # Name
        var_line += f" {state_var.name}"
        
        # Initial value
        if state_var.initial_value:
            value_code = self.generate_node(state_var.initial_value)
            var_line += f" = {value_code}"
        
        var_line += ";"
        self.add_line(var_line)
    
    def generate_function_definition(self, function: SolidityFunctionDefinition):
        """Generate function definition."""
        func_line = "function "
        
        # Function name (constructor/fallback/receive are special)
        if function.name in ["constructor", "fallback", "receive"]:
            func_line = function.name + " "
        else:
            func_line += function.name
        
        # Parameters
        if function.parameters:
            params = self.generate_parameter_list(function.parameters)
            func_line += f"({params})"
        else:
            func_line += "()"
        
        # Visibility
        if function.visibility:
            func_line += f" {function.visibility.value}"
        
        # Mutability
        if function.mutability and function.mutability != SolidityMutability.NONPAYABLE:
            func_line += f" {function.mutability.value}"
        
        # Virtual/Override
        if function.is_virtual:
            func_line += " virtual"
        
        if function.is_override:
            func_line += " override"
        
        # Modifiers
        for modifier in function.modifiers:
            modifier_code = self.generate_modifier_invocation(modifier)
            func_line += f" {modifier_code}"
        
        # Return parameters
        if function.return_parameters and function.return_parameters.parameters:
            returns = self.generate_parameter_list(function.return_parameters)
            func_line += f" returns ({returns})"
        
        # Function body
        if function.body:
            func_line += " {"
            self.add_line(func_line)
            
            self.current_indent += 1
            self.generate_block(function.body)
            self.current_indent -= 1
            
            self.add_line("}")
        else:
            # Interface function or abstract function
            func_line += ";"
            self.add_line(func_line)
    
    def generate_function_signature(self, function: SolidityFunctionDefinition):
        """Generate function signature (for interfaces)."""
        func_line = f"function {function.name}"
        
        # Parameters
        if function.parameters:
            params = self.generate_parameter_list(function.parameters)
            func_line += f"({params})"
        else:
            func_line += "()"
        
        # Visibility
        if function.visibility:
            func_line += f" {function.visibility.value}"
        
        # Mutability
        if function.mutability and function.mutability != SolidityMutability.NONPAYABLE:
            func_line += f" {function.mutability.value}"
        
        # Return parameters
        if function.return_parameters and function.return_parameters.parameters:
            returns = self.generate_parameter_list(function.return_parameters)
            func_line += f" returns ({returns})"
        
        func_line += ";"
        self.add_line(func_line)
    
    def generate_constructor_definition(self, constructor: SolidityConstructorDefinition):
        """Generate constructor definition."""
        func_line = "constructor"
        
        # Parameters
        if constructor.parameters:
            params = self.generate_parameter_list(constructor.parameters)
            func_line += f"({params})"
        else:
            func_line += "()"
        
        # Visibility
        if constructor.visibility:
            func_line += f" {constructor.visibility.value}"
        
        # Payable
        if constructor.is_payable:
            func_line += " payable"
        
        # Modifiers
        for modifier in constructor.modifiers:
            modifier_code = self.generate_modifier_invocation(modifier)
            func_line += f" {modifier_code}"
        
        # Body
        if constructor.body:
            func_line += " {"
            self.add_line(func_line)
            
            self.current_indent += 1
            self.generate_block(constructor.body)
            self.current_indent -= 1
            
            self.add_line("}")
        else:
            func_line += ";"
            self.add_line(func_line)
    
    def generate_event_definition(self, event: SolidityEventDefinition):
        """Generate event definition."""
        event_line = f"event {event.name}"
        
        if event.parameters:
            params = self.generate_parameter_list(event.parameters, include_indexed=True)
            event_line += f"({params})"
        else:
            event_line += "()"
        
        event_line += ";"
        self.add_line(event_line)
    
    def generate_error_definition(self, error: SolidityErrorDefinition):
        """Generate error definition."""
        error_line = f"error {error.name}"
        
        if error.parameters:
            params = self.generate_parameter_list(error.parameters)
            error_line += f"({params})"
        else:
            error_line += "()"
        
        error_line += ";"
        self.add_line(error_line)
    
    def generate_modifier_definition(self, modifier: SolidityModifierDefinition):
        """Generate modifier definition."""
        mod_line = f"modifier {modifier.name}"
        
        if modifier.parameters:
            params = self.generate_parameter_list(modifier.parameters)
            mod_line += f"({params})"
        else:
            mod_line += "()"
        
        if modifier.body:
            mod_line += " {"
            self.add_line(mod_line)
            
            self.current_indent += 1
            self.generate_block(modifier.body)
            self.current_indent -= 1
            
            self.add_line("}")
        else:
            mod_line += ";"
            self.add_line(mod_line)
    
    def generate_parameter_list(self, param_list: SolidityParameterList, include_indexed: bool = False) -> str:
        """Generate parameter list."""
        params = []
        for param in param_list.parameters:
            param_str = self.generate_type_name(param.type_name)
            
            if include_indexed and param.is_indexed:
                param_str += " indexed"
            
            if param.name:
                param_str += f" {param.name}"
            
            params.append(param_str)
        
        return ", ".join(params)
    
    def generate_modifier_invocation(self, modifier: SolidityModifierInvocation) -> str:
        """Generate modifier invocation."""
        mod_str = modifier.name
        
        if modifier.arguments:
            args = [self.generate_node(arg) for arg in modifier.arguments]
            mod_str += f"({', '.join(args)})"
        
        return mod_str
    
    def generate_block(self, block: SolidityBlock):
        """Generate block statements."""
        for stmt in block.statements:
            self.generate_node(stmt)
    
    def generate_node(self, node: SolidityNode) -> str:
        """Generate code for any Solidity node."""
        if isinstance(node, SolidityVariableDeclaration):
            return self.generate_variable_declaration(node)
        elif isinstance(node, SolidityFunctionCall):
            return self.generate_function_call(node)
        elif isinstance(node, SolidityIdentifier):
            return self.generate_identifier(node)
        elif isinstance(node, SolidityLiteral):
            return self.generate_literal(node)
        elif isinstance(node, SolidityBinaryExpression):
            return self.generate_binary_expression(node)
        elif isinstance(node, SolidityUnaryExpression):
            return self.generate_unary_expression(node)
        elif isinstance(node, SolidityAssignment):
            return self.generate_assignment(node)
        elif isinstance(node, SolidityIfStatement):
            return self.generate_if_statement(node)
        elif isinstance(node, SolidityForLoop):
            return self.generate_for_loop(node)
        elif isinstance(node, SolidityWhileLoop):
            return self.generate_while_loop(node)
        elif isinstance(node, SolidityReturnStatement):
            return self.generate_return_statement(node)
        elif isinstance(node, SolidityBreakStatement):
            return self.generate_break_statement(node)
        elif isinstance(node, SolidiyContinueStatement):
            return self.generate_continue_statement(node)
        elif isinstance(node, SolidityEmitStatement):
            return self.generate_emit_statement(node)
        elif isinstance(node, SolidityRevertStatement):
            return self.generate_revert_statement(node)
        elif isinstance(node, SolidityRequireStatement):
            return self.generate_require_statement(node)
        elif isinstance(node, SolidityAssertStatement):
            return self.generate_assert_statement(node)
        elif isinstance(node, SolidityMemberAccess):
            return self.generate_member_access(node)
        elif isinstance(node, SolidityIndexAccess):
            return self.generate_index_access(node)
        elif isinstance(node, SolidityComment):
            return self.generate_comment(node)
        else:
            return f"/* Unknown node type: {type(node).__name__} */"
    
    def generate_variable_declaration(self, var_decl: SolidityVariableDeclaration) -> str:
        """Generate variable declaration."""
        var_line = self.generate_type_name(var_decl.type_name)
        
        if var_decl.storage_location:
            var_line += f" {var_decl.storage_location.value}"
        
        var_line += f" {var_decl.name}"
        
        if var_decl.initial_value:
            value_code = self.generate_node(var_decl.initial_value)
            var_line += f" = {value_code}"
        
        var_line += ";"
        self.add_line(var_line)
        return ""
    
    def generate_function_call(self, func_call: SolidityFunctionCall) -> str:
        """Generate function call."""
        function_code = self.generate_node(func_call.expression)
        
        # Handle named arguments
        args = []
        for i, arg in enumerate(func_call.arguments):
            arg_code = self.generate_node(arg)
            
            # Check if this is a named argument
            if i < len(func_call.names) and func_call.names[i]:
                args.append(f"{func_call.names[i]}: {arg_code}")
            else:
                args.append(arg_code)
        
        arg_list = ", ".join(args)
        return f"{function_code}({arg_list})"
    
    def generate_identifier(self, identifier: SolidityIdentifier) -> str:
        """Generate identifier."""
        return identifier.name
    
    def generate_literal(self, literal: SolidityLiteral) -> str:
        """Generate literal value."""
        if literal.type_name in ["string", "bytes"]:
            # String literal
            escaped = str(literal.value).replace("\\", "\\\\").replace('"', '\\"')
            return f'"{escaped}"'
        elif literal.type_name == "bool":
            return "true" if literal.value else "false"
        elif literal.type_name == "address":
            return f"0x{literal.value}"
        else:
            return str(literal.value)
    
    def generate_binary_expression(self, bin_expr: SolidityBinaryExpression) -> str:
        """Generate binary expression."""
        left_code = self.generate_node(bin_expr.left)
        right_code = self.generate_node(bin_expr.right)
        
        operator_map = {
            SolidityOperator.PLUS: "+",
            SolidityOperator.MINUS: "-",
            SolidityOperator.MULTIPLY: "*",
            SolidityOperator.DIVIDE: "/",
            SolidityOperator.MODULO: "%",
            SolidityOperator.EXPONENT: "**",
            SolidityOperator.EQUAL: "==",
            SolidityOperator.NOT_EQUAL: "!=",
            SolidityOperator.LESS_THAN: "<",
            SolidityOperator.LESS_EQUAL: "<=",
            SolidityOperator.GREATER_THAN: ">",
            SolidityOperator.GREATER_EQUAL: ">=",
            SolidityOperator.AND: "&&",
            SolidityOperator.OR: "||",
            SolidityOperator.ASSIGN: "="
        }
        
        op_str = operator_map.get(bin_expr.operator, "+")
        return f"{left_code} {op_str} {right_code}"
    
    def generate_unary_expression(self, unary_expr: SolidityUnaryExpression) -> str:
        """Generate unary expression."""
        expr_code = self.generate_node(unary_expr.expression)
        
        operator_map = {
            SolidityOperator.MINUS: "-",
            SolidityOperator.NOT: "!",
            SolidityOperator.BITWISE_NOT: "~"
        }
        
        op_str = operator_map.get(unary_expr.operator, "-")
        
        if unary_expr.is_prefix:
            return f"{op_str}{expr_code}"
        else:
            return f"{expr_code}{op_str}"
    
    def generate_assignment(self, assignment: SolidityAssignment) -> str:
        """Generate assignment statement."""
        left_code = self.generate_node(assignment.left)
        right_code = self.generate_node(assignment.right)
        
        result = f"{left_code} = {right_code};"
        self.add_line(result)
        return ""
    
    def generate_if_statement(self, if_stmt: SolidityIfStatement) -> str:
        """Generate if statement."""
        condition_code = self.generate_node(if_stmt.condition)
        
        self.add_line(f"if ({condition_code}) {{")
        self.current_indent += 1
        
        if isinstance(if_stmt.then_statement, SolidityBlock):
            self.generate_block(if_stmt.then_statement)
        else:
            self.generate_node(if_stmt.then_statement)
        
        self.current_indent -= 1
        
        if if_stmt.else_statement:
            self.add_line("} else {")
            self.current_indent += 1
            
            if isinstance(if_stmt.else_statement, SolidityBlock):
                self.generate_block(if_stmt.else_statement)
            else:
                self.generate_node(if_stmt.else_statement)
            
            self.current_indent -= 1
        
        self.add_line("}")
        return ""
    
    def generate_for_loop(self, for_loop: SolidityForLoop) -> str:
        """Generate for loop."""
        init_code = ""
        if for_loop.init_statement:
            init_code = self.generate_node(for_loop.init_statement).rstrip(';')
        
        condition_code = ""
        if for_loop.condition:
            condition_code = self.generate_node(for_loop.condition)
        
        update_code = ""
        if for_loop.update_expression:
            update_code = self.generate_node(for_loop.update_expression)
        
        self.add_line(f"for ({init_code}; {condition_code}; {update_code}) {{")
        
        self.current_indent += 1
        if isinstance(for_loop.body, SolidityBlock):
            self.generate_block(for_loop.body)
        else:
            self.generate_node(for_loop.body)
        self.current_indent -= 1
        
        self.add_line("}")
        return ""
    
    def generate_while_loop(self, while_loop: SolidityWhileLoop) -> str:
        """Generate while loop."""
        condition_code = self.generate_node(while_loop.condition)
        
        self.add_line(f"while ({condition_code}) {{")
        
        self.current_indent += 1
        if isinstance(while_loop.body, SolidityBlock):
            self.generate_block(while_loop.body)
        else:
            self.generate_node(while_loop.body)
        self.current_indent -= 1
        
        self.add_line("}")
        return ""
    
    def generate_return_statement(self, ret_stmt: SolidityReturnStatement) -> str:
        """Generate return statement."""
        if ret_stmt.expression:
            expr_code = self.generate_node(ret_stmt.expression)
            result = f"return {expr_code};"
        else:
            result = "return;"
        
        self.add_line(result)
        return ""
    
    def generate_break_statement(self, break_stmt: SolidityBreakStatement) -> str:
        """Generate break statement."""
        self.add_line("break;")
        return ""
    
    def generate_continue_statement(self, cont_stmt: SolidiyContinueStatement) -> str:
        """Generate continue statement."""
        self.add_line("continue;")
        return ""
    
    def generate_emit_statement(self, emit_stmt: SolidityEmitStatement) -> str:
        """Generate emit statement."""
        event_call = self.generate_node(emit_stmt.event_call)
        result = f"emit {event_call};"
        self.add_line(result)
        return ""
    
    def generate_revert_statement(self, revert_stmt: SolidityRevertStatement) -> str:
        """Generate revert statement."""
        if revert_stmt.error_call:
            error_call = self.generate_node(revert_stmt.error_call)
            result = f"revert {error_call};"
        else:
            result = "revert();"
        
        self.add_line(result)
        return ""
    
    def generate_require_statement(self, req_stmt: SolidityRequireStatement) -> str:
        """Generate require statement."""
        condition_code = self.generate_node(req_stmt.condition)
        
        if req_stmt.message:
            message_code = self.generate_node(req_stmt.message)
            result = f"require({condition_code}, {message_code});"
        else:
            result = f"require({condition_code});"
        
        self.add_line(result)
        return ""
    
    def generate_assert_statement(self, assert_stmt: SolidityAssertStatement) -> str:
        """Generate assert statement."""
        condition_code = self.generate_node(assert_stmt.condition)
        result = f"assert({condition_code});"
        self.add_line(result)
        return ""
    
    def generate_member_access(self, member_access: SolidityMemberAccess) -> str:
        """Generate member access."""
        expression_code = self.generate_node(member_access.expression)
        return f"{expression_code}.{member_access.member_name}"
    
    def generate_index_access(self, index_access: SolidityIndexAccess) -> str:
        """Generate index access."""
        base_code = self.generate_node(index_access.base_expression)
        index_code = self.generate_node(index_access.index_expression)
        return f"{base_code}[{index_code}]"
    
    def generate_comment(self, comment: SolidityComment) -> str:
        """Generate comment."""
        self.add_line(f"// {comment.text}")
        return ""
    
    def generate_type_name(self, type_name: SolidityType) -> str:
        """Generate type name."""
        if isinstance(type_name, SolidityElementaryType):
            return type_name.name
        elif isinstance(type_name, SolidityArrayType):
            base_type = self.generate_type_name(type_name.base_type)
            if type_name.length:
                length_code = self.generate_node(type_name.length)
                return f"{base_type}[{length_code}]"
            else:
                return f"{base_type}[]"
        elif isinstance(type_name, SolidityMappingType):
            key_type = self.generate_type_name(type_name.key_type)
            value_type = self.generate_type_name(type_name.value_type)
            return f"mapping({key_type} => {value_type})"
        elif isinstance(type_name, SolidityUserDefinedType):
            return type_name.name
        elif isinstance(type_name, SolidityFunctionType):
            # Function type: function (uint256) external returns (bool)
            params = ""
            if type_name.parameter_types:
                param_types = [self.generate_type_name(pt) for pt in type_name.parameter_types]
                params = ", ".join(param_types)
            
            returns = ""
            if type_name.return_types:
                return_types = [self.generate_type_name(rt) for rt in type_name.return_types]
                returns = f" returns ({', '.join(return_types)})"
            
            visibility = ""
            if type_name.visibility:
                visibility = f" {type_name.visibility.value}"
            
            mutability = ""
            if type_name.mutability and type_name.mutability != SolidityMutability.NONPAYABLE:
                mutability = f" {type_name.mutability.value}"
            
            return f"function ({params}){visibility}{mutability}{returns}"
        else:
            return "unknown"
    
    def add_line(self, line: str):
        """Add a line with proper indentation."""
        if line.strip():  # Don't indent empty lines
            indented_line = " " * (self.current_indent * self.indent_size) + line
            self.output_lines.append(indented_line)
        else:
            self.output_lines.append("")


def generate_solidity_code(sol_ast: SolidityNode, indent_size: int = 4) -> str:
    """Generate Solidity source code from AST."""
    generator = SolidityCodeGenerator(indent_size=indent_size)
    return generator.generate(sol_ast) 