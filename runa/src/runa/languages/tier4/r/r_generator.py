#!/usr/bin/env python3
"""
R Code Generator

Production-ready R code generator that creates clean, properly formatted R source code
with correct indentation, syntax, and R coding conventions.
"""

from typing import List, Optional, Any, Union, Dict
from dataclasses import dataclass

from .r_ast import *


class RCodeGenerator:
    """Generate R source code from R AST."""
    
    def __init__(self, indent_size: int = 2):
        self.indent_size = indent_size
        self.current_indent = 0
        self.output_lines: List[str] = []
    
    def generate(self, r_node: RNode) -> str:
        """Generate R source code from AST node."""
        self.output_lines = []
        self.current_indent = 0
        
        if isinstance(r_node, RProgram):
            self.generate_program(r_node)
        elif isinstance(r_node, RScript):
            self.generate_script(r_node)
        else:
            self.generate_node(r_node)
        
        return '\n'.join(self.output_lines)
    
    def generate_program(self, r_program: RProgram):
        """Generate R program."""
        for i, stmt in enumerate(r_program.statements):
            if i > 0:
                self.add_line("")  # Blank line between statements
            self.generate_node(stmt)
    
    def generate_script(self, r_script: RScript):
        """Generate R script."""
        # Add shebang if specified
        if r_script.shebang:
            self.add_line(r_script.shebang)
            self.add_line("")
        
        for i, stmt in enumerate(r_script.statements):
            if i > 0:
                self.add_line("")
            self.generate_node(stmt)
    
    def generate_node(self, r_node: RNode) -> str:
        """Generate code for any R node."""
        if isinstance(r_node, RFunctionDefinition):
            return self.generate_function_definition(r_node)
        elif isinstance(r_node, RFunctionCall):
            return self.generate_function_call(r_node)
        elif isinstance(r_node, RIdentifier):
            return self.generate_identifier(r_node)
        elif isinstance(r_node, RAssignment):
            return self.generate_assignment(r_node)
        elif isinstance(r_node, RBinaryExpression):
            return self.generate_binary_expression(r_node)
        elif isinstance(r_node, RUnaryExpression):
            return self.generate_unary_expression(r_node)
        elif isinstance(r_node, RNumericLiteral):
            return self.generate_numeric_literal(r_node)
        elif isinstance(r_node, RStringLiteral):
            return self.generate_string_literal(r_node)
        elif isinstance(r_node, RLogicalLiteral):
            return self.generate_logical_literal(r_node)
        elif isinstance(r_node, RNullLiteral):
            return self.generate_null_literal(r_node)
        elif isinstance(r_node, RNALiteral):
            return self.generate_na_literal(r_node)
        elif isinstance(r_node, RVector):
            return self.generate_vector(r_node)
        elif isinstance(r_node, RList):
            return self.generate_list(r_node)
        elif isinstance(r_node, RDataFrame):
            return self.generate_data_frame(r_node)
        elif isinstance(r_node, RMatrix):
            return self.generate_matrix(r_node)
        elif isinstance(r_node, RFactor):
            return self.generate_factor(r_node)
        elif isinstance(r_node, RIfStatement):
            return self.generate_if_statement(r_node)
        elif isinstance(r_node, RForLoop):
            return self.generate_for_loop(r_node)
        elif isinstance(r_node, RWhileLoop):
            return self.generate_while_loop(r_node)
        elif isinstance(r_node, RRepeatLoop):
            return self.generate_repeat_loop(r_node)
        elif isinstance(r_node, RReturnStatement):
            return self.generate_return_statement(r_node)
        elif isinstance(r_node, RBreakStatement):
            return self.generate_break_statement(r_node)
        elif isinstance(r_node, RNextStatement):
            return self.generate_next_statement(r_node)
        elif isinstance(r_node, RIndexExpression):
            return self.generate_index_expression(r_node)
        elif isinstance(r_node, RDollarAccess):
            return self.generate_dollar_access(r_node)
        elif isinstance(r_node, RAtAccess):
            return self.generate_at_access(r_node)
        elif isinstance(r_node, RNamespaceAccess):
            return self.generate_namespace_access(r_node)
        elif isinstance(r_node, RFormula):
            return self.generate_formula(r_node)
        elif isinstance(r_node, RTildeExpression):
            return self.generate_tilde_expression(r_node)
        elif isinstance(r_node, RPackageLoad):
            return self.generate_package_load(r_node)
        elif isinstance(r_node, RComment):
            return self.generate_comment(r_node)
        else:
            return f"# Unknown node type: {type(r_node).__name__}"
    
    def generate_function_definition(self, r_func: RFunctionDefinition) -> str:
        """Generate R function definition."""
        # Generate parameter list
        params = []
        for param in r_func.parameters:
            if param.is_ellipsis:
                params.append("...")
            else:
                param_str = param.name
                if param.default_value:
                    default_code = self.generate_node(param.default_value)
                    param_str += f" = {default_code}"
                params.append(param_str)
        
        param_list = ", ".join(params)
        
        # Function header
        func_header = f"function({param_list})"
        
        # Function body
        if len(r_func.body) == 1 and not isinstance(r_func.body[0], (RIfStatement, RForLoop, RWhileLoop)):
            # Single expression body
            body_code = self.generate_node(r_func.body[0])
            result = f"{func_header} {body_code}"
        else:
            # Block body
            result = f"{func_header} {{"
            self.add_line(result)
            
            self.current_indent += 1
            for stmt in r_func.body:
                stmt_code = self.generate_node(stmt)
                self.add_line(stmt_code)
            self.current_indent -= 1
            
            self.add_line("}")
            return ""  # Already added to output
        
        return result
    
    def generate_function_call(self, r_call: RFunctionCall) -> str:
        """Generate R function call."""
        function_code = self.generate_node(r_call.function)
        
        # Generate arguments
        args = []
        for arg in r_call.arguments:
            if arg.name:
                # Named argument
                arg_code = f"{arg.name} = {self.generate_node(arg.value)}"
            else:
                # Positional argument
                arg_code = self.generate_node(arg.value)
            args.append(arg_code)
        
        arg_list = ", ".join(args)
        return f"{function_code}({arg_list})"
    
    def generate_identifier(self, r_id: RIdentifier) -> str:
        """Generate R identifier."""
        # Handle special identifiers that need quoting
        if ' ' in r_id.name or any(c in r_id.name for c in '.-+*/^%<>=!&|()[]{}'):
            return f"`{r_id.name}`"
        return r_id.name
    
    def generate_assignment(self, r_assign: RAssignment) -> str:
        """Generate R assignment."""
        target_code = self.generate_node(r_assign.target)
        value_code = self.generate_node(r_assign.value)
        
        # Map operator to R syntax
        operator_map = {
            ROperator.ASSIGN: "<-",
            ROperator.ASSIGN_RIGHT: "->",
            ROperator.ASSIGN_EQUAL: "=",
            ROperator.SUPER_ASSIGN: "<<-",
            ROperator.SUPER_ASSIGN_RIGHT: "->>"
        }
        
        op_str = operator_map.get(r_assign.operator, "<-")
        
        if r_assign.operator == ROperator.ASSIGN_RIGHT:
            result = f"{value_code} {op_str} {target_code}"
        else:
            result = f"{target_code} {op_str} {value_code}"
        
        self.add_line(result)
        return ""
    
    def generate_binary_expression(self, r_expr: RBinaryExpression) -> str:
        """Generate R binary expression."""
        left_code = self.generate_node(r_expr.left)
        right_code = self.generate_node(r_expr.right)
        
        # Map operators to R syntax
        operator_map = {
            ROperator.PLUS: "+",
            ROperator.MINUS: "-",
            ROperator.MULTIPLY: "*",
            ROperator.DIVIDE: "/",
            ROperator.INTEGER_DIVIDE: "%/%",
            ROperator.MODULO: "%%",
            ROperator.POWER: "^",
            ROperator.POWER_ALT: "**",
            ROperator.EQUAL: "==",
            ROperator.NOT_EQUAL: "!=",
            ROperator.LESS_THAN: "<",
            ROperator.LESS_EQUAL: "<=",
            ROperator.GREATER_THAN: ">",
            ROperator.GREATER_EQUAL: ">=",
            ROperator.AND: "&",
            ROperator.OR: "|",
            ROperator.AND_SHORT: "&&",
            ROperator.OR_SHORT: "||",
            ROperator.IN: "%in%",
            ROperator.MATCH: "%*%",
            ROperator.OUTER: "%o%",
            ROperator.KRONECKER: "%x%"
        }
        
        op_str = operator_map.get(r_expr.operator, "+")
        
        # Add parentheses for complex expressions
        needs_parens = isinstance(r_expr.left, RBinaryExpression) or isinstance(r_expr.right, RBinaryExpression)
        
        if needs_parens:
            return f"({left_code}) {op_str} ({right_code})"
        else:
            return f"{left_code} {op_str} {right_code}"
    
    def generate_unary_expression(self, r_expr: RUnaryExpression) -> str:
        """Generate R unary expression."""
        expr_code = self.generate_node(r_expr.expression)
        
        operator_map = {
            ROperator.MINUS: "-",
            ROperator.PLUS: "+",
            ROperator.NOT: "!"
        }
        
        op_str = operator_map.get(r_expr.operator, "-")
        return f"{op_str}{expr_code}"
    
    def generate_numeric_literal(self, r_num: RNumericLiteral) -> str:
        """Generate R numeric literal."""
        if r_num.is_integer:
            return f"{r_num.value}L"
        else:
            return str(r_num.value)
    
    def generate_string_literal(self, r_str: RStringLiteral) -> str:
        """Generate R string literal."""
        # Escape quotes and special characters
        escaped = r_str.value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    
    def generate_logical_literal(self, r_bool: RLogicalLiteral) -> str:
        """Generate R logical literal."""
        return "TRUE" if r_bool.value else "FALSE"
    
    def generate_null_literal(self, r_null: RNullLiteral) -> str:
        """Generate R NULL literal."""
        return "NULL"
    
    def generate_na_literal(self, r_na: RNALiteral) -> str:
        """Generate R NA literal."""
        return r_na.na_type
    
    def generate_vector(self, r_vec: RVector) -> str:
        """Generate R vector creation."""
        elements = [self.generate_node(elem) for elem in r_vec.elements]
        element_list = ", ".join(elements)
        return f"c({element_list})"
    
    def generate_list(self, r_list: RList) -> str:
        """Generate R list creation."""
        elements = []
        for elem in r_list.elements:
            if elem.name:
                elem_code = f"{elem.name} = {self.generate_node(elem.value)}"
            else:
                elem_code = self.generate_node(elem.value)
            elements.append(elem_code)
        
        element_list = ", ".join(elements)
        return f"list({element_list})"
    
    def generate_data_frame(self, r_df: RDataFrame) -> str:
        """Generate R data.frame creation."""
        columns = []
        for col in r_df.columns:
            col_code = f"{col.name} = {self.generate_node(col.values)}"
            columns.append(col_code)
        
        column_list = ", ".join(columns)
        return f"data.frame({column_list})"
    
    def generate_matrix(self, r_matrix: RMatrix) -> str:
        """Generate R matrix creation."""
        data_code = self.generate_node(r_matrix.data)
        
        args = [data_code]
        
        if r_matrix.nrow:
            args.append(f"nrow = {self.generate_node(r_matrix.nrow)}")
        
        if r_matrix.ncol:
            args.append(f"ncol = {self.generate_node(r_matrix.ncol)}")
        
        if r_matrix.byrow is not None:
            args.append(f"byrow = {'TRUE' if r_matrix.byrow else 'FALSE'}")
        
        arg_list = ", ".join(args)
        return f"matrix({arg_list})"
    
    def generate_factor(self, r_factor: RFactor) -> str:
        """Generate R factor creation."""
        data_code = self.generate_node(r_factor.data)
        
        args = [data_code]
        
        if r_factor.levels:
            levels_code = self.generate_node(r_factor.levels)
            args.append(f"levels = {levels_code}")
        
        if r_factor.labels:
            labels_code = self.generate_node(r_factor.labels)
            args.append(f"labels = {labels_code}")
        
        if r_factor.ordered is not None:
            args.append(f"ordered = {'TRUE' if r_factor.ordered else 'FALSE'}")
        
        arg_list = ", ".join(args)
        return f"factor({arg_list})"
    
    def generate_if_statement(self, r_if: RIfStatement) -> str:
        """Generate R if statement."""
        condition_code = self.generate_node(r_if.condition)
        
        # Start if statement
        if_line = f"if ({condition_code}) {{"
        self.add_line(if_line)
        
        # Then clause
        self.current_indent += 1
        then_code = self.generate_node(r_if.then_expr)
        if then_code:  # If not already added to output
            self.add_line(then_code)
        self.current_indent -= 1
        
        # Else clause
        if r_if.else_expr:
            self.add_line("} else {")
            self.current_indent += 1
            else_code = self.generate_node(r_if.else_expr)
            if else_code:
                self.add_line(else_code)
            self.current_indent -= 1
        
        self.add_line("}")
        return ""
    
    def generate_for_loop(self, r_for: RForLoop) -> str:
        """Generate R for loop."""
        variable = r_for.variable
        iterable_code = self.generate_node(r_for.iterable)
        
        # Start for loop
        for_line = f"for ({variable} in {iterable_code}) {{"
        self.add_line(for_line)
        
        # Loop body
        self.current_indent += 1
        body_code = self.generate_node(r_for.body)
        if body_code:
            self.add_line(body_code)
        self.current_indent -= 1
        
        self.add_line("}")
        return ""
    
    def generate_while_loop(self, r_while: RWhileLoop) -> str:
        """Generate R while loop."""
        condition_code = self.generate_node(r_while.condition)
        
        # Start while loop
        while_line = f"while ({condition_code}) {{"
        self.add_line(while_line)
        
        # Loop body
        self.current_indent += 1
        body_code = self.generate_node(r_while.body)
        if body_code:
            self.add_line(body_code)
        self.current_indent -= 1
        
        self.add_line("}")
        return ""
    
    def generate_repeat_loop(self, r_repeat: RRepeatLoop) -> str:
        """Generate R repeat loop."""
        self.add_line("repeat {")
        
        # Loop body
        self.current_indent += 1
        body_code = self.generate_node(r_repeat.body)
        if body_code:
            self.add_line(body_code)
        self.current_indent -= 1
        
        self.add_line("}")
        return ""
    
    def generate_return_statement(self, r_return: RReturnStatement) -> str:
        """Generate R return statement."""
        if r_return.value:
            value_code = self.generate_node(r_return.value)
            result = f"return({value_code})"
        else:
            result = "return()"
        
        self.add_line(result)
        return ""
    
    def generate_break_statement(self, r_break: RBreakStatement) -> str:
        """Generate R break statement."""
        self.add_line("break")
        return ""
    
    def generate_next_statement(self, r_next: RNextStatement) -> str:
        """Generate R next statement."""
        self.add_line("next")
        return ""
    
    def generate_index_expression(self, r_index: RIndexExpression) -> str:
        """Generate R indexing expression."""
        object_code = self.generate_node(r_index.object)
        
        # Generate indices
        indices = [self.generate_node(idx) for idx in r_index.indices]
        index_list = ", ".join(indices)
        
        if r_index.is_double_bracket:
            return f"{object_code}[[{index_list}]]"
        else:
            return f"{object_code}[{index_list}]"
    
    def generate_dollar_access(self, r_dollar: RDollarAccess) -> str:
        """Generate R dollar access."""
        object_code = self.generate_node(r_dollar.object)
        return f"{object_code}${r_dollar.element}"
    
    def generate_at_access(self, r_at: RAtAccess) -> str:
        """Generate R at access."""
        object_code = self.generate_node(r_at.object)
        return f"{object_code}@{r_at.slot}"
    
    def generate_namespace_access(self, r_ns: RNamespaceAccess) -> str:
        """Generate R namespace access."""
        if r_ns.is_internal:
            return f"{r_ns.package}:::{r_ns.function}"
        else:
            return f"{r_ns.package}::{r_ns.function}"
    
    def generate_formula(self, r_formula: RFormula) -> str:
        """Generate R formula."""
        if r_formula.left:
            left_code = self.generate_node(r_formula.left)
            right_code = self.generate_node(r_formula.right)
            return f"{left_code} ~ {right_code}"
        else:
            right_code = self.generate_node(r_formula.right)
            return f"~ {right_code}"
    
    def generate_tilde_expression(self, r_tilde: RTildeExpression) -> str:
        """Generate R tilde expression."""
        expr_code = self.generate_node(r_tilde.expression)
        return f"~ {expr_code}"
    
    def generate_package_load(self, r_pkg: RPackageLoad) -> str:
        """Generate R package load statement."""
        if r_pkg.is_require:
            result = f"require({r_pkg.package_name})"
        else:
            result = f"library({r_pkg.package_name})"
        
        self.add_line(result)
        return ""
    
    def generate_comment(self, r_comment: RComment) -> str:
        """Generate R comment."""
        self.add_line(f"# {r_comment.text}")
        return ""
    
    def add_line(self, line: str):
        """Add a line with proper indentation."""
        if line.strip():  # Don't indent empty lines
            indented_line = " " * (self.current_indent * self.indent_size) + line
            self.output_lines.append(indented_line)
        else:
            self.output_lines.append("")


def generate_r_code(r_ast: RNode, indent_size: int = 2) -> str:
    """Generate R source code from AST."""
    generator = RCodeGenerator(indent_size=indent_size)
    return generator.generate(r_ast) 