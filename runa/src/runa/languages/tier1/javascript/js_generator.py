#!/usr/bin/env python3
"""
JavaScript Code Generator

Generates JavaScript source code from JavaScript AST nodes.
Supports all modern JavaScript features and provides clean,
readable output with proper formatting.
"""

from typing import List, Dict, Any, Optional
from io import StringIO
import re

from .js_ast import *


class JSCodeGenerator:
    """JavaScript code generator with proper formatting."""
    
    def __init__(self, indent_size: int = 2, use_semicolons: bool = True):
        self.indent_size = indent_size
        self.use_semicolons = use_semicolons
        self.current_indent = 0
        self.output = StringIO()
        self.needs_semicolon = False
    
    def generate(self, node: JSNode) -> str:
        """Generate JavaScript code from AST node."""
        self.output = StringIO()
        self.current_indent = 0
        self.needs_semicolon = False
        
        self._visit_node(node)
        
        result = self.output.getvalue()
        self.output.close()
        return result
    
    def _visit_node(self, node: JSNode):
        """Visit a node and generate code."""
        if isinstance(node, JSProgram):
            self._visit_program(node)
        
        elif isinstance(node, JSLiteral):
            self._visit_literal(node)
        
        elif isinstance(node, JSIdentifier):
            self._visit_identifier(node)
        
        elif isinstance(node, JSBinaryExpression):
            self._visit_binary_expression(node)
        
        elif isinstance(node, JSUnaryExpression):
            self._visit_unary_expression(node)
        
        elif isinstance(node, JSUpdateExpression):
            self._visit_update_expression(node)
        
        elif isinstance(node, JSAssignmentExpression):
            self._visit_assignment_expression(node)
        
        elif isinstance(node, JSLogicalExpression):
            self._visit_logical_expression(node)
        
        elif isinstance(node, JSConditionalExpression):
            self._visit_conditional_expression(node)
        
        elif isinstance(node, JSCallExpression):
            self._visit_call_expression(node)
        
        elif isinstance(node, JSMemberExpression):
            self._visit_member_expression(node)
        
        elif isinstance(node, JSNewExpression):
            self._visit_new_expression(node)
        
        elif isinstance(node, JSArrayExpression):
            self._visit_array_expression(node)
        
        elif isinstance(node, JSObjectExpression):
            self._visit_object_expression(node)
        
        elif isinstance(node, JSProperty):
            self._visit_property(node)
        
        elif isinstance(node, JSFunctionExpression):
            self._visit_function_expression(node)
        
        elif isinstance(node, JSArrowFunctionExpression):
            self._visit_arrow_function_expression(node)
        
        elif isinstance(node, JSThisExpression):
            self._visit_this_expression(node)
        
        elif isinstance(node, JSSuper):
            self._visit_super(node)
        
        elif isinstance(node, JSSequenceExpression):
            self._visit_sequence_expression(node)
        
        elif isinstance(node, JSAwaitExpression):
            self._visit_await_expression(node)
        
        elif isinstance(node, JSYieldExpression):
            self._visit_yield_expression(node)
        
        elif isinstance(node, JSTemplateLiteral):
            self._visit_template_literal(node)
        
        # Statements
        elif isinstance(node, JSExpressionStatement):
            self._visit_expression_statement(node)
        
        elif isinstance(node, JSVariableDeclaration):
            self._visit_variable_declaration(node)
        
        elif isinstance(node, JSVariableDeclarator):
            self._visit_variable_declarator(node)
        
        elif isinstance(node, JSFunctionDeclaration):
            self._visit_function_declaration(node)
        
        elif isinstance(node, JSBlockStatement):
            self._visit_block_statement(node)
        
        elif isinstance(node, JSIfStatement):
            self._visit_if_statement(node)
        
        elif isinstance(node, JSWhileStatement):
            self._visit_while_statement(node)
        
        elif isinstance(node, JSForStatement):
            self._visit_for_statement(node)
        
        elif isinstance(node, JSReturnStatement):
            self._visit_return_statement(node)
        
        elif isinstance(node, JSBreakStatement):
            self._visit_break_statement(node)
        
        elif isinstance(node, JSContinueStatement):
            self._visit_continue_statement(node)
        
        elif isinstance(node, JSThrowStatement):
            self._visit_throw_statement(node)
        
        elif isinstance(node, JSTryStatement):
            self._visit_try_statement(node)
        
        elif isinstance(node, JSCatchClause):
            self._visit_catch_clause(node)
        
        elif isinstance(node, JSEmptyStatement):
            self._visit_empty_statement(node)
        
        elif isinstance(node, JSDebuggerStatement):
            self._visit_debugger_statement(node)
        
        else:
            raise NotImplementedError(f"Code generation not implemented for {type(node)}")
    
    def _write(self, text: str):
        """Write text to output."""
        self.output.write(text)
    
    def _write_line(self, text: str = ""):
        """Write a line with current indentation."""
        if text:
            self._write(self._get_indent() + text)
        self._write("\n")
    
    def _write_indent(self):
        """Write current indentation."""
        self._write(self._get_indent())
    
    def _get_indent(self) -> str:
        """Get current indentation string."""
        return " " * (self.current_indent * self.indent_size)
    
    def _increase_indent(self):
        """Increase indentation level."""
        self.current_indent += 1
    
    def _decrease_indent(self):
        """Decrease indentation level."""
        self.current_indent = max(0, self.current_indent - 1)
    
    def _write_semicolon(self):
        """Write semicolon if needed."""
        if self.use_semicolons:
            self._write(";")
    
    def _visit_program(self, node: JSProgram):
        """Visit program node."""
        for i, stmt in enumerate(node.body):
            if i > 0:
                self._write("\n")
            self._visit_node(stmt)
    
    def _visit_literal(self, node: JSLiteral):
        """Visit literal node."""
        if node.literal_type == JSLiteralType.NULL:
            self._write("null")
        elif node.literal_type == JSLiteralType.BOOLEAN:
            self._write("true" if node.value else "false")
        elif node.literal_type == JSLiteralType.NUMBER:
            self._write(str(node.value))
        elif node.literal_type == JSLiteralType.STRING:
            # Properly escape string
            escaped = self._escape_string(str(node.value))
            self._write(f'"{escaped}"')
        elif node.literal_type == JSLiteralType.REGEX:
            self._write(node.raw)
        elif node.literal_type == JSLiteralType.BIGINT:
            self._write(f"{node.value}n")
        else:
            self._write(node.raw)
    
    def _escape_string(self, s: str) -> str:
        """Escape string for JavaScript."""
        return (s.replace("\\", "\\\\")
                 .replace('"', '\\"')
                 .replace("\n", "\\n")
                 .replace("\r", "\\r")
                 .replace("\t", "\\t")
                 .replace("\b", "\\b")
                 .replace("\f", "\\f")
                 .replace("\v", "\\v")
                 .replace("\0", "\\0"))
    
    def _visit_identifier(self, node: JSIdentifier):
        """Visit identifier node."""
        self._write(node.name)
    
    def _visit_binary_expression(self, node: JSBinaryExpression):
        """Visit binary expression."""
        self._visit_node(node.left)
        self._write(f" {node.operator.value} ")
        self._visit_node(node.right)
    
    def _visit_unary_expression(self, node: JSUnaryExpression):
        """Visit unary expression."""
        if node.prefix:
            self._write(node.operator.value)
            if node.operator.value.isalpha():
                self._write(" ")
            self._visit_node(node.argument)
        else:
            self._visit_node(node.argument)
            self._write(node.operator.value)
    
    def _visit_update_expression(self, node: JSUpdateExpression):
        """Visit update expression."""
        if node.prefix:
            self._write(node.operator.value)
            self._visit_node(node.argument)
        else:
            self._visit_node(node.argument)
            self._write(node.operator.value)
    
    def _visit_assignment_expression(self, node: JSAssignmentExpression):
        """Visit assignment expression."""
        self._visit_node(node.left)
        self._write(f" {node.operator.value} ")
        self._visit_node(node.right)
    
    def _visit_logical_expression(self, node: JSLogicalExpression):
        """Visit logical expression."""
        self._visit_node(node.left)
        self._write(f" {node.operator.value} ")
        self._visit_node(node.right)
    
    def _visit_conditional_expression(self, node: JSConditionalExpression):
        """Visit conditional expression."""
        self._visit_node(node.test)
        self._write(" ? ")
        self._visit_node(node.consequent)
        self._write(" : ")
        self._visit_node(node.alternate)
    
    def _visit_call_expression(self, node: JSCallExpression):
        """Visit call expression."""
        self._visit_node(node.callee)
        if node.optional:
            self._write("?.")
        self._write("(")
        
        for i, arg in enumerate(node.arguments):
            if i > 0:
                self._write(", ")
            self._visit_node(arg)
        
        self._write(")")
    
    def _visit_member_expression(self, node: JSMemberExpression):
        """Visit member expression."""
        self._visit_node(node.object)
        
        if node.computed:
            if node.optional:
                self._write("?.")
            self._write("[")
            self._visit_node(node.property)
            self._write("]")
        else:
            if node.optional:
                self._write("?.")
            else:
                self._write(".")
            self._visit_node(node.property)
    
    def _visit_new_expression(self, node: JSNewExpression):
        """Visit new expression."""
        self._write("new ")
        self._visit_node(node.callee)
        
        if node.arguments:
            self._write("(")
            for i, arg in enumerate(node.arguments):
                if i > 0:
                    self._write(", ")
                self._visit_node(arg)
            self._write(")")
    
    def _visit_array_expression(self, node: JSArrayExpression):
        """Visit array expression."""
        self._write("[")
        
        for i, element in enumerate(node.elements):
            if i > 0:
                self._write(", ")
            
            if element is None:
                # Sparse array element
                pass
            else:
                self._visit_node(element)
        
        self._write("]")
    
    def _visit_object_expression(self, node: JSObjectExpression):
        """Visit object expression."""
        if not node.properties:
            self._write("{}")
            return
        
        self._write("{\n")
        self._increase_indent()
        
        for i, prop in enumerate(node.properties):
            if i > 0:
                self._write(",\n")
            
            self._write_indent()
            self._visit_node(prop)
        
        self._write("\n")
        self._decrease_indent()
        self._write_indent()
        self._write("}")
    
    def _visit_property(self, node: JSProperty):
        """Visit property node."""
        # Handle key
        if node.computed:
            self._write("[")
            self._visit_node(node.key)
            self._write("]")
        else:
            self._visit_node(node.key)
        
        if node.kind == JSPropertyKind.INIT:
            if not node.shorthand:
                self._write(": ")
                self._visit_node(node.value)
        elif node.kind == JSPropertyKind.GET:
            self._write("get ")
            self._visit_node(node.key)
            self._write("() ")
            self._visit_node(node.value)
        elif node.kind == JSPropertyKind.SET:
            self._write("set ")
            self._visit_node(node.key)
            self._write("(value) ")
            self._visit_node(node.value)
        elif node.kind == JSPropertyKind.METHOD:
            # Print method parameters from the function node
            if hasattr(node.value, 'params'):
                self._write("(")
                for i, param in enumerate(getattr(node.value, 'params', [])):
                    if i > 0:
                        self._write(", ")
                    self._visit_node(param)
                self._write(") ")
            else:
                self._write("() ")
            self._visit_node(node.value)
    
    def _visit_function_expression(self, node: JSFunctionExpression):
        """Visit function expression."""
        if node.async_:
            self._write("async ")
        
        self._write("function")
        
        if node.generator:
            self._write("*")
        
        if node.id:
            self._write(" ")
            self._visit_node(node.id)
        
        self._write("(")
        
        for i, param in enumerate(node.params):
            if i > 0:
                self._write(", ")
            self._visit_node(param)
        
        self._write(") ")
        self._visit_node(node.body)
    
    def _visit_arrow_function_expression(self, node: JSArrowFunctionExpression):
        """Visit arrow function expression."""
        if node.async_:
            self._write("async ")
        
        # Parameters
        if len(node.params) == 1 and isinstance(node.params[0], JSIdentifier):
            self._visit_node(node.params[0])
        else:
            self._write("(")
            for i, param in enumerate(node.params):
                if i > 0:
                    self._write(", ")
                self._visit_node(param)
            self._write(")")
        
        self._write(" => ")
        
        if node.expression:
            self._visit_node(node.body)
        else:
            self._visit_node(node.body)
    
    def _visit_this_expression(self, node: JSThisExpression):
        """Visit this expression."""
        self._write("this")
    
    def _visit_super(self, node: JSSuper):
        """Visit super node."""
        self._write("super")
    
    def _visit_sequence_expression(self, node: JSSequenceExpression):
        """Visit sequence expression."""
        for i, expr in enumerate(node.expressions):
            if i > 0:
                self._write(", ")
            self._visit_node(expr)
    
    def _visit_await_expression(self, node: JSAwaitExpression):
        """Visit await expression."""
        self._write("await ")
        self._visit_node(node.argument)
    
    def _visit_yield_expression(self, node: JSYieldExpression):
        """Visit yield expression."""
        self._write("yield")
        if node.delegate:
            self._write("*")
        if node.argument:
            self._write(" ")
            self._visit_node(node.argument)
    
    def _visit_template_literal(self, node: JSTemplateLiteral):
        """Visit template literal."""
        self._write("`")
        
        for i, quasi in enumerate(node.quasis):
            # Write string part
            if isinstance(quasi, JSLiteral):
                self._write(str(quasi.value))
            else:
                self._visit_node(quasi)
            
            # Write expression part
            if i < len(node.expressions):
                self._write("${")
                self._visit_node(node.expressions[i])
                self._write("}")
        
        self._write("`")
    
    def _visit_expression_statement(self, node: JSExpressionStatement):
        """Visit expression statement."""
        self._write_indent()
        self._visit_node(node.expression)
        self._write_semicolon()
        self._write("\n")
    
    def _visit_variable_declaration(self, node: JSVariableDeclaration):
        """Visit variable declaration."""
        self._write_indent()
        self._write(node.kind.value)
        self._write(" ")
        
        for i, declarator in enumerate(node.declarations):
            if i > 0:
                self._write(", ")
            self._visit_node(declarator)
        
        self._write_semicolon()
        self._write("\n")
    
    def _visit_variable_declarator(self, node: JSVariableDeclarator):
        """Visit variable declarator."""
        self._visit_node(node.id)
        
        if node.init:
            self._write(" = ")
            self._visit_node(node.init)
    
    def _visit_function_declaration(self, node: JSFunctionDeclaration):
        """Visit function declaration."""
        self._write_indent()
        
        if node.async_:
            self._write("async ")
        
        self._write("function")
        
        if node.generator:
            self._write("*")
        
        self._write(" ")
        self._visit_node(node.id)
        self._write("(")
        
        for i, param in enumerate(node.params):
            if i > 0:
                self._write(", ")
            self._visit_node(param)
        
        self._write(") ")
        self._visit_node(node.body)
        self._write("\n")
    
    def _visit_block_statement(self, node: JSBlockStatement):
        """Visit block statement."""
        self._write("{\n")
        self._increase_indent()
        
        for stmt in node.body:
            self._visit_node(stmt)
        
        self._decrease_indent()
        self._write_indent()
        self._write("}")
    
    def _visit_if_statement(self, node: JSIfStatement):
        """Visit if statement."""
        self._write_indent()
        self._write("if (")
        self._visit_node(node.test)
        self._write(") ")
        
        if isinstance(node.consequent, JSBlockStatement):
            self._visit_node(node.consequent)
        else:
            self._write("{\n")
            self._increase_indent()
            self._visit_node(node.consequent)
            self._decrease_indent()
            self._write_indent()
            self._write("}")
        
        if node.alternate:
            self._write(" else ")
            
            if isinstance(node.alternate, JSIfStatement):
                # else if
                self._write("if (")
                self._visit_node(node.alternate.test)
                self._write(") ")
                self._visit_node(node.alternate.consequent)
                
                if node.alternate.alternate:
                    self._write(" else ")
                    self._visit_node(node.alternate.alternate)
            else:
                if isinstance(node.alternate, JSBlockStatement):
                    self._visit_node(node.alternate)
                else:
                    self._write("{\n")
                    self._increase_indent()
                    self._visit_node(node.alternate)
                    self._decrease_indent()
                    self._write_indent()
                    self._write("}")
        
        self._write("\n")
    
    def _visit_while_statement(self, node: JSWhileStatement):
        """Visit while statement."""
        self._write_indent()
        self._write("while (")
        self._visit_node(node.test)
        self._write(") ")
        
        if isinstance(node.body, JSBlockStatement):
            self._visit_node(node.body)
        else:
            self._write("{\n")
            self._increase_indent()
            self._visit_node(node.body)
            self._decrease_indent()
            self._write_indent()
            self._write("}")
        
        self._write("\n")
    
    def _visit_for_statement(self, node: JSForStatement):
        """Visit for statement."""
        self._write_indent()
        self._write("for (")
        
        if node.init:
            if isinstance(node.init, JSVariableDeclaration):
                # Special handling for variable declaration in for loop
                self._write(node.init.kind.value)
                self._write(" ")
                
                for i, declarator in enumerate(node.init.declarations):
                    if i > 0:
                        self._write(", ")
                    self._visit_node(declarator)
            else:
                self._visit_node(node.init)
        
        self._write("; ")
        
        if node.test:
            self._visit_node(node.test)
        
        self._write("; ")
        
        if node.update:
            self._visit_node(node.update)
        
        self._write(") ")
        
        if isinstance(node.body, JSBlockStatement):
            self._visit_node(node.body)
        else:
            self._write("{\n")
            self._increase_indent()
            self._visit_node(node.body)
            self._decrease_indent()
            self._write_indent()
            self._write("}")
        
        self._write("\n")
    
    def _visit_return_statement(self, node: JSReturnStatement):
        """Visit return statement."""
        self._write_indent()
        self._write("return")
        
        if node.argument:
            self._write(" ")
            self._visit_node(node.argument)
        
        self._write_semicolon()
        self._write("\n")
    
    def _visit_break_statement(self, node: JSBreakStatement):
        """Visit break statement."""
        self._write_indent()
        self._write("break")
        
        if node.label:
            self._write(" ")
            self._visit_node(node.label)
        
        self._write_semicolon()
        self._write("\n")
    
    def _visit_continue_statement(self, node: JSContinueStatement):
        """Visit continue statement."""
        self._write_indent()
        self._write("continue")
        
        if node.label:
            self._write(" ")
            self._visit_node(node.label)
        
        self._write_semicolon()
        self._write("\n")
    
    def _visit_throw_statement(self, node: JSThrowStatement):
        """Visit throw statement."""
        self._write_indent()
        self._write("throw ")
        self._visit_node(node.argument)
        self._write_semicolon()
        self._write("\n")
    
    def _visit_try_statement(self, node: JSTryStatement):
        """Visit try statement."""
        self._write_indent()
        self._write("try ")
        self._visit_node(node.block)
        
        if node.handler:
            self._write(" ")
            self._visit_node(node.handler)
        
        if node.finalizer:
            self._write(" finally ")
            self._visit_node(node.finalizer)
        
        self._write("\n")
    
    def _visit_catch_clause(self, node: JSCatchClause):
        """Visit catch clause."""
        self._write("catch")
        
        if node.param:
            self._write(" (")
            self._visit_node(node.param)
            self._write(")")
        
        self._write(" ")
        self._visit_node(node.body)
    
    def _visit_empty_statement(self, node: JSEmptyStatement):
        """Visit empty statement."""
        self._write_indent()
        self._write_semicolon()
        self._write("\n")
    
    def _visit_debugger_statement(self, node: JSDebuggerStatement):
        """Visit debugger statement."""
        self._write_indent()
        self._write("debugger")
        self._write_semicolon()
        self._write("\n")


class JSMinifier:
    """JavaScript code minifier."""
    
    def __init__(self):
        self.output = StringIO()
    
    def minify(self, node: JSNode) -> str:
        """Generate minified JavaScript code."""
        generator = JSCodeGenerator(indent_size=0, use_semicolons=True)
        code = generator.generate(node)
        
        # Remove unnecessary whitespace
        code = re.sub(r'\s+', ' ', code)
        code = re.sub(r';\s*}', '}', code)
        code = re.sub(r'{\s*', '{', code)
        code = re.sub(r'\s*}', '}', code)
        code = re.sub(r'\s*;\s*', ';', code)
        code = re.sub(r'\s*,\s*', ',', code)
        code = re.sub(r'\s*\+\s*', '+', code)
        code = re.sub(r'\s*-\s*', '-', code)
        code = re.sub(r'\s*\*\s*', '*', code)
        code = re.sub(r'\s*/\s*', '/', code)
        code = re.sub(r'\s*=\s*', '=', code)
        code = re.sub(r'\s*<\s*', '<', code)
        code = re.sub(r'\s*>\s*', '>', code)
        code = re.sub(r'\s*!\s*', '!', code)
        code = re.sub(r'\s*\?\s*', '?', code)
        code = re.sub(r'\s*:\s*', ':', code)
        
        return code.strip()


class JSFormatter:
    """JavaScript code formatter with various style options."""
    
    def __init__(self, style: str = "standard"):
        self.style = style
        
        if style == "standard":
            self.indent_size = 2
            self.use_semicolons = True
            self.space_before_function_paren = False
            self.space_in_object_braces = True
        elif style == "airbnb":
            self.indent_size = 2
            self.use_semicolons = True
            self.space_before_function_paren = False
            self.space_in_object_braces = True
        elif style == "google":
            self.indent_size = 2
            self.use_semicolons = True
            self.space_before_function_paren = False
            self.space_in_object_braces = False
        elif style == "prettier":
            self.indent_size = 2
            self.use_semicolons = True
            self.space_before_function_paren = False
            self.space_in_object_braces = True
        else:
            # Default
            self.indent_size = 2
            self.use_semicolons = True
            self.space_before_function_paren = False
            self.space_in_object_braces = True
    
    def format(self, node: JSNode) -> str:
        """Format JavaScript code with specified style."""
        generator = JSCodeGenerator(
            indent_size=self.indent_size,
            use_semicolons=self.use_semicolons
        )
        return generator.generate(node)


def generate_javascript(ast: JSNode, minify: bool = False, style: str = "standard") -> str:
    """Generate JavaScript code from AST."""
    if minify:
        minifier = JSMinifier()
        return minifier.minify(ast)
    else:
        formatter = JSFormatter(style)
        return formatter.format(ast)


def format_javascript(code: str, style: str = "standard") -> str:
    """Format JavaScript code using the internal parser and formatter."""
    from .js_parser import parse_javascript
    try:
        ast = parse_javascript(code)
        formatter = JSFormatter(style)
        return formatter.format(ast)
    except Exception as e:
        # If parsing fails, return the code as-is
        return code