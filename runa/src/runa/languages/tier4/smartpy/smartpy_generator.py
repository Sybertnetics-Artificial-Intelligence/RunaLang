"""
SmartPy Code Generator

Generates idiomatic SmartPy code from AST nodes.
"""

from typing import List, Optional, Union, Dict, Any
from io import StringIO
from .smartpy_ast import *


class SmartPyGenerator:
    """Generates SmartPy code from AST nodes."""
    
    def __init__(self, indent_size: int = 4):
        self.indent_size = indent_size
        self.indent_level = 0
        self.output = StringIO()
        
    def generate(self, node: SmartPyNode) -> str:
        """Generate SmartPy code for any AST node."""
        self.output = StringIO()
        self.indent_level = 0
        self._visit(node)
        return self.output.getvalue()
    
    def _write(self, text: str = ""):
        """Write text to output."""
        self.output.write(text)
    
    def _write_line(self, text: str = ""):
        """Write a line with current indentation."""
        if text:
            self._write(" " * (self.indent_level * self.indent_size) + text + "\n")
        else:
            self._write("\n")
    
    def _indent(self):
        """Increase indentation level."""
        self.indent_level += 1
    
    def _dedent(self):
        """Decrease indentation level."""
        self.indent_level = max(0, self.indent_level - 1)
    
    def _visit(self, node: Optional[SmartPyNode]):
        """Visit a node and generate code for it."""
        if node is None:
            return
            
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self.visit_generic)
        visitor(node)
    
    def visit_generic(self, node: SmartPyNode):
        """Generic visitor for unknown nodes."""
        self._write(str(node))
    
    # Module and program
    def visit_SmartPyModule(self, node: SmartPyModule):
        """Generate code for SmartPy module."""
        # Imports
        for import_node in node.imports:
            self._visit(import_node)
            self._write_line()
        
        if node.imports:
            self._write_line()
        
        # Declarations
        for i, decl in enumerate(node.declarations):
            if i > 0:
                self._write_line()
                self._write_line()
            self._visit(decl)
    
    def visit_SmartPyImport(self, node: SmartPyImport):
        """Generate import statement."""
        if node.names:
            self._write(f"from {node.module} import {', '.join(node.names)}")
        else:
            self._write(f"import {node.module}")
            if node.alias:
                self._write(f" as {node.alias}")
    
    # Contract definition
    def visit_SmartPyContractDef(self, node: SmartPyContractDef):
        """Generate smart contract class."""
        self._write(f"class {node.name}")
        
        if node.base_classes:
            self._write(f"({', '.join(node.base_classes)})")
        
        self._write(":")
        self._write_line()
        self._indent()
        
        # Init method
        if node.init_method:
            self._visit(node.init_method)
            self._write_line()
            self._write_line()
        
        # Entry points
        for entry_point in node.entry_points:
            self._visit(entry_point)
            self._write_line()
            self._write_line()
        
        # Regular methods
        for method in node.methods:
            self._visit(method)
            self._write_line()
            self._write_line()
        
        self._dedent()
    
    def visit_SmartPyMethodDef(self, node: SmartPyMethodDef):
        """Generate method definition."""
        # Decorators
        for decorator in node.decorators:
            self._write_line(decorator)
        
        # Method signature
        self._write(f"def {node.name}(")
        if node.parameters:
            self._write(", ".join(node.parameters))
        self._write("):")
        self._write_line()
        
        # Method body
        self._indent()
        if node.body:
            for stmt in node.body:
                self._visit(stmt)
                self._write_line()
        else:
            self._write_line("pass")
        self._dedent()
    
    def visit_SmartPyFunctionDef(self, node: SmartPyFunctionDef):
        """Generate function definition."""
        # Decorators
        for decorator in node.decorators:
            self._write_line(decorator)
        
        # Function signature
        self._write(f"def {node.name}(")
        if node.parameters:
            self._write(", ".join(node.parameters))
        self._write("):")
        self._write_line()
        
        # Function body
        self._indent()
        if node.body:
            for stmt in node.body:
                self._visit(stmt)
                self._write_line()
        else:
            self._write_line("pass")
        self._dedent()
    
    # Expressions
    def visit_SmartPyLiteral(self, node: SmartPyLiteral):
        """Generate literal."""
        if isinstance(node.value, str):
            self._write(f'"{node.value}"')
        elif isinstance(node.value, bool):
            self._write("True" if node.value else "False")
        elif node.value is None:
            self._write("None")
        else:
            self._write(str(node.value))
    
    def visit_SmartPyIdentifier(self, node: SmartPyIdentifier):
        """Generate identifier."""
        self._write(node.name)
    
    def visit_SmartPyBinaryOp(self, node: SmartPyBinaryOp):
        """Generate binary operation."""
        self._visit(node.left)
        self._write(f" {node.operator} ")
        self._visit(node.right)
    
    def visit_SmartPyUnaryOp(self, node: SmartPyUnaryOp):
        """Generate unary operation."""
        self._write(f"{node.operator} ")
        self._visit(node.operand)
    
    def visit_SmartPyFunctionCall(self, node: SmartPyFunctionCall):
        """Generate function call."""
        self._visit(node.function)
        self._write("(")
        
        # Arguments
        args = []
        for arg in node.args:
            arg_str = StringIO()
            temp_output = self.output
            self.output = arg_str
            self._visit(arg)
            self.output = temp_output
            args.append(arg_str.getvalue())
        
        # Keyword arguments
        for key, value in node.keywords.items():
            value_str = StringIO()
            temp_output = self.output
            self.output = value_str
            self._visit(value)
            self.output = temp_output
            args.append(f"{key}={value_str.getvalue()}")
        
        self._write(", ".join(args))
        self._write(")")
    
    def visit_SmartPyAttributeAccess(self, node: SmartPyAttributeAccess):
        """Generate attribute access."""
        self._visit(node.object)
        self._write(f".{node.attribute}")
    
    def visit_SmartPyIndexAccess(self, node: SmartPyIndexAccess):
        """Generate index access."""
        self._visit(node.object)
        self._write("[")
        self._visit(node.index)
        self._write("]")
    
    def visit_SmartPyListLiteral(self, node: SmartPyListLiteral):
        """Generate list literal."""
        self._write("[")
        for i, elem in enumerate(node.elements):
            if i > 0:
                self._write(", ")
            self._visit(elem)
        self._write("]")
    
    def visit_SmartPyMapLiteral(self, node: SmartPyMapLiteral):
        """Generate map literal."""
        self._write("{")
        for i, (key, value) in enumerate(node.pairs):
            if i > 0:
                self._write(", ")
            self._visit(key)
            self._write(": ")
            self._visit(value)
        self._write("}")
    
    # SmartPy built-ins
    def visit_SmartPySender(self, node: SmartPySender):
        """Generate sp.sender."""
        self._write("sp.sender")
    
    def visit_SmartPyAmount(self, node: SmartPyAmount):
        """Generate sp.amount."""
        self._write("sp.amount")
    
    def visit_SmartPyBalance(self, node: SmartPyBalance):
        """Generate sp.balance.""" 
        self._write("sp.balance")
    
    def visit_SmartPyNow(self, node: SmartPyNow):
        """Generate sp.now."""
        self._write("sp.now")
    
    # Statements
    def visit_SmartPyAssignment(self, node: SmartPyAssignment):
        """Generate assignment statement."""
        self._visit(node.target)
        self._write(" = ")
        self._visit(node.value)
    
    def visit_SmartPyAugmentedAssignment(self, node: SmartPyAugmentedAssignment):
        """Generate augmented assignment."""
        self._visit(node.target)
        self._write(f" {node.operator} ")
        self._visit(node.value)
    
    def visit_SmartPyExpressionStatement(self, node: SmartPyExpressionStatement):
        """Generate expression statement."""
        self._visit(node.expression)
    
    def visit_SmartPyIf(self, node: SmartPyIf):
        """Generate if statement."""
        self._write("if ")
        self._visit(node.test)
        self._write(":")
        self._write_line()
        
        self._indent()
        for stmt in node.body:
            self._visit(stmt)
            self._write_line()
        self._dedent()
        
        if node.orelse:
            self._write_line("else:")
            self._indent()
            for stmt in node.orelse:
                self._visit(stmt)
                self._write_line()
            self._dedent()
    
    def visit_SmartPyFor(self, node: SmartPyFor):
        """Generate for loop."""
        self._write(f"for {node.target} in ")
        self._visit(node.iter)
        self._write(":")
        self._write_line()
        
        self._indent()
        for stmt in node.body:
            self._visit(stmt)
            self._write_line()
        self._dedent()
    
    def visit_SmartPyWhile(self, node: SmartPyWhile):
        """Generate while loop."""
        self._write("while ")
        self._visit(node.test)
        self._write(":")
        self._write_line()
        
        self._indent()
        for stmt in node.body:
            self._visit(stmt)
            self._write_line()
        self._dedent()
    
    def visit_SmartPyReturn(self, node: SmartPyReturn):
        """Generate return statement."""
        self._write("return")
        if node.value:
            self._write(" ")
            self._visit(node.value)
    
    # SmartPy specific statements
    def visit_SmartPyVerify(self, node: SmartPyVerify):
        """Generate sp.verify statement."""
        self._write("sp.verify(")
        self._visit(node.condition)
        if node.message:
            self._write(", ")
            self._visit(node.message)
        self._write(")")
    
    def visit_SmartPyFailwith(self, node: SmartPyFailwith):
        """Generate sp.failwith statement."""
        self._write("sp.failwith(")
        self._visit(node.value)
        self._write(")")
    
    def visit_SmartPyStorageInit(self, node: SmartPyStorageInit):
        """Generate storage initialization."""
        self._write("self.init(")
        
        field_strs = []
        for field_name, field_value in node.fields.items():
            value_str = StringIO()
            temp_output = self.output
            self.output = value_str
            self._visit(field_value)
            self.output = temp_output
            field_strs.append(f"{field_name}={value_str.getvalue()}")
        
        self._write(", ".join(field_strs))
        self._write(")")
    
    # Tests
    def visit_SmartPyTestDef(self, node: SmartPyTestDef):
        """Generate test function."""
        self._write_line("@sp.add_test(name=\"" + node.name + "\")")
        self._write_line("def test():")
        
        self._indent()
        for stmt in node.body:
            self._visit(stmt)
            self._write_line()
        self._dedent()


def generate_smartpy_code(ast_node: SmartPyNode, indent_size: int = 4) -> str:
    """Generate SmartPy code from an AST node."""
    generator = SmartPyGenerator(indent_size)
    return generator.generate(ast_node) 