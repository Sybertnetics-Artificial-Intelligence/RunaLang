#!/usr/bin/env python3
"""
LISP Code Generator

Generates clean, properly formatted LISP code from AST.
Handles S-expressions, proper indentation, and LISP conventions.
"""

from typing import List, Optional, Any, Union
from io import StringIO

from ...shared.base_toolchain import BaseGenerator
from .lisp_ast import (
    LispNode, LispExpression, LispForm, LispAtom, LispSymbol, LispList,
    LispCons, LispQuote, LispDefun, LispLambda, LispLet, LispSetq, LispIf,
    LispCond, LispProgn, LispWhen, LispUnless, LispCar, LispCdr, LispConsFunc,
    LispEq, LispEqual, LispAtomFunc, LispListp, LispLoop, LispReturn,
    LispDefmacro, LispMacroCall, LispApplication, LispProgram,
    LispNodeType
)


class LispCodeGenerator(BaseGenerator):
    """LISP code generator."""
    
    def __init__(self, indent_size: int = 2):
        super().__init__()
        self.indent_size = indent_size
        self.indent_level = 0
        self.output = StringIO()
        
        # Configuration
        self.format_config = {
            'max_line_length': 80,
            'align_parameters': True,
            'compact_simple_forms': True,
            'space_after_special_forms': True
        }
    
    def generate(self, node: LispNode) -> str:
        """Generate LISP code from AST node."""
        self.output = StringIO()
        self.indent_level = 0
        
        self._generate_node(node)
        return self.output.getvalue()
    
    def _generate_node(self, node: LispNode):
        """Generate code for any LISP node."""
        if isinstance(node, LispProgram):
            self._generate_program(node)
        elif isinstance(node, LispAtom):
            self._generate_atom(node)
        elif isinstance(node, LispSymbol):
            self._generate_symbol(node)
        elif isinstance(node, LispList):
            self._generate_list(node)
        elif isinstance(node, LispCons):
            self._generate_cons(node)
        elif isinstance(node, LispQuote):
            self._generate_quote(node)
        elif isinstance(node, LispDefun):
            self._generate_defun(node)
        elif isinstance(node, LispLambda):
            self._generate_lambda(node)
        elif isinstance(node, LispLet):
            self._generate_let(node)
        elif isinstance(node, LispSetq):
            self._generate_setq(node)
        elif isinstance(node, LispIf):
            self._generate_if(node)
        elif isinstance(node, LispCond):
            self._generate_cond(node)
        elif isinstance(node, LispProgn):
            self._generate_progn(node)
        elif isinstance(node, LispWhen):
            self._generate_when(node)
        elif isinstance(node, LispUnless):
            self._generate_unless(node)
        elif isinstance(node, LispApplication):
            self._generate_application(node)
        elif isinstance(node, (LispCar, LispCdr, LispConsFunc, LispEq, LispEqual,
                               LispAtomFunc, LispListp)):
            self._generate_builtin_function(node)
        elif isinstance(node, LispLoop):
            self._generate_loop(node)
        elif isinstance(node, LispReturn):
            self._generate_return(node)
        elif isinstance(node, LispDefmacro):
            self._generate_defmacro(node)
        elif isinstance(node, LispMacroCall):
            self._generate_macro_call(node)
        else:
            raise ValueError(f"Unknown LISP node type: {type(node)}")
    
    def _generate_program(self, node: LispProgram):
        """Generate LISP program."""
        for i, form in enumerate(node.forms):
            if i > 0:
                self.output.write("\n\n")
            self._generate_node(form)
    
    def _generate_atom(self, node: LispAtom):
        """Generate LISP atom."""
        if node.atom_type == "nil":
            self.output.write("nil")
        elif node.atom_type == "t":
            self.output.write("t")
        elif node.atom_type == "number":
            if isinstance(node.value, float):
                self.output.write(f"{node.value:.6f}".rstrip('0').rstrip('.'))
            else:
                self.output.write(str(node.value))
        elif node.atom_type == "string":
            escaped = node.value.replace('"', '\\"')
            self.output.write(f'"{escaped}"')
        else:
            self.output.write(str(node.value))
    
    def _generate_symbol(self, node: LispSymbol):
        """Generate LISP symbol."""
        self.output.write(node.name)
    
    def _generate_list(self, node: LispList):
        """Generate LISP list."""
        if not node.elements:
            self.output.write("()")
            return
        
        # Check if it's a simple list that can be on one line
        if self._is_simple_list(node):
            self.output.write("(")
            for i, elem in enumerate(node.elements):
                if i > 0:
                    self.output.write(" ")
                self._generate_node(elem)
            self.output.write(")")
        else:
            # Multi-line list
            self.output.write("(")
            self.indent_level += 1
            
            for i, elem in enumerate(node.elements):
                if i > 0:
                    self.output.write("\n")
                    self._write_indent()
                self._generate_node(elem)
            
            self.indent_level -= 1
            self.output.write(")")
    
    def _generate_cons(self, node: LispCons):
        """Generate LISP cons (dotted pair)."""
        self.output.write("(")
        self._generate_node(node.car)
        self.output.write(" . ")
        self._generate_node(node.cdr)
        self.output.write(")")
    
    def _generate_quote(self, node: LispQuote):
        """Generate LISP quote."""
        self.output.write("'")
        self._generate_node(node.expression)
    
    def _generate_defun(self, node: LispDefun):
        """Generate LISP defun."""
        self.output.write("(defun ")
        self._generate_node(node.name)
        self.output.write(" ")
        
        # Parameters
        self._generate_parameter_list(node.parameters)
        
        # Doc string
        if node.doc_string:
            self.output.write("\n")
            self._write_indent(1)
            escaped = node.doc_string.replace('"', '\\"')
            self.output.write(f'"{escaped}"')
        
        # Body
        if node.body:
            for expr in node.body:
                self.output.write("\n")
                self._write_indent(1)
                self._generate_node(expr)
        
        self.output.write(")")
    
    def _generate_lambda(self, node: LispLambda):
        """Generate LISP lambda."""
        self.output.write("(lambda ")
        
        # Parameters
        self._generate_parameter_list(node.parameters)
        
        # Body
        if node.body:
            for expr in node.body:
                self.output.write("\n")
                self._write_indent(1)
                self._generate_node(expr)
        
        self.output.write(")")
    
    def _generate_let(self, node: LispLet):
        """Generate LISP let."""
        self.output.write("(let (")
        
        # Bindings
        if node.bindings:
            for i, (symbol, value) in enumerate(node.bindings):
                if i > 0:
                    self.output.write("\n")
                    self._write_indent(2)
                self.output.write("(")
                self._generate_node(symbol)
                self.output.write(" ")
                self._generate_node(value)
                self.output.write(")")
        
        self.output.write(")")
        
        # Body
        if node.body:
            for expr in node.body:
                self.output.write("\n")
                self._write_indent(1)
                self._generate_node(expr)
        
        self.output.write(")")
    
    def _generate_setq(self, node: LispSetq):
        """Generate LISP setq."""
        self.output.write("(setq ")
        self._generate_node(node.symbol)
        self.output.write(" ")
        self._generate_node(node.value)
        self.output.write(")")
    
    def _generate_if(self, node: LispIf):
        """Generate LISP if."""
        self.output.write("(if ")
        self._generate_node(node.test)
        
        # Then clause
        if self._is_simple_expression(node.then_expr):
            self.output.write(" ")
            self._generate_node(node.then_expr)
        else:
            self.output.write("\n")
            self._write_indent(1)
            self._generate_node(node.then_expr)
        
        # Else clause
        if node.else_expr:
            if self._is_simple_expression(node.else_expr):
                self.output.write(" ")
                self._generate_node(node.else_expr)
            else:
                self.output.write("\n")
                self._write_indent(1)
                self._generate_node(node.else_expr)
        
        self.output.write(")")
    
    def _generate_cond(self, node: LispCond):
        """Generate LISP cond."""
        self.output.write("(cond")
        
        for test, expr in node.clauses:
            self.output.write("\n")
            self._write_indent(1)
            self.output.write("(")
            self._generate_node(test)
            self.output.write(" ")
            self._generate_node(expr)
            self.output.write(")")
        
        self.output.write(")")
    
    def _generate_progn(self, node: LispProgn):
        """Generate LISP progn."""
        self.output.write("(progn")
        
        for expr in node.expressions:
            self.output.write("\n")
            self._write_indent(1)
            self._generate_node(expr)
        
        self.output.write(")")
    
    def _generate_when(self, node: LispWhen):
        """Generate LISP when."""
        self.output.write("(when ")
        self._generate_node(node.test)
        
        for expr in node.body:
            self.output.write("\n")
            self._write_indent(1)
            self._generate_node(expr)
        
        self.output.write(")")
    
    def _generate_unless(self, node: LispUnless):
        """Generate LISP unless."""
        self.output.write("(unless ")
        self._generate_node(node.test)
        
        for expr in node.body:
            self.output.write("\n")
            self._write_indent(1)
            self._generate_node(expr)
        
        self.output.write(")")
    
    def _generate_application(self, node: LispApplication):
        """Generate LISP function application."""
        self.output.write("(")
        self._generate_node(node.function)
        
        if node.arguments:
            # Check if it fits on one line
            if self._is_simple_application(node):
                for arg in node.arguments:
                    self.output.write(" ")
                    self._generate_node(arg)
            else:
                # Multi-line
                for arg in node.arguments:
                    self.output.write("\n")
                    self._write_indent(1)
                    self._generate_node(arg)
        
        self.output.write(")")
    
    def _generate_builtin_function(self, node: LispExpression):
        """Generate LISP built-in function call."""
        if isinstance(node, LispCar):
            self.output.write("(car ")
            self._generate_node(node.expression)
            self.output.write(")")
        elif isinstance(node, LispCdr):
            self.output.write("(cdr ")
            self._generate_node(node.expression)
            self.output.write(")")
        elif isinstance(node, LispConsFunc):
            self.output.write("(cons ")
            self._generate_node(node.car)
            self.output.write(" ")
            self._generate_node(node.cdr)
            self.output.write(")")
        elif isinstance(node, LispEq):
            self.output.write("(eq ")
            self._generate_node(node.left)
            self.output.write(" ")
            self._generate_node(node.right)
            self.output.write(")")
        elif isinstance(node, LispEqual):
            self.output.write("(equal ")
            self._generate_node(node.left)
            self.output.write(" ")
            self._generate_node(node.right)
            self.output.write(")")
        elif isinstance(node, LispAtomFunc):
            self.output.write("(atom ")
            self._generate_node(node.expression)
            self.output.write(")")
        elif isinstance(node, LispListp):
            self.output.write("(listp ")
            self._generate_node(node.expression)
            self.output.write(")")
    
    def _generate_loop(self, node: LispLoop):
        """Generate LISP loop."""
        self.output.write("(loop")
        
        for expr in node.body:
            self.output.write("\n")
            self._write_indent(1)
            self._generate_node(expr)
        
        self.output.write(")")
    
    def _generate_return(self, node: LispReturn):
        """Generate LISP return."""
        self.output.write("(return")
        if node.value:
            self.output.write(" ")
            self._generate_node(node.value)
        self.output.write(")")
    
    def _generate_defmacro(self, node: LispDefmacro):
        """Generate LISP defmacro."""
        self.output.write("(defmacro ")
        self._generate_node(node.name)
        self.output.write(" ")
        
        # Parameters
        self._generate_parameter_list(node.parameters)
        
        # Body
        if node.body:
            for expr in node.body:
                self.output.write("\n")
                self._write_indent(1)
                self._generate_node(expr)
        
        self.output.write(")")
    
    def _generate_macro_call(self, node: LispMacroCall):
        """Generate LISP macro call."""
        self.output.write("(")
        self._generate_node(node.name)
        
        if node.arguments:
            for arg in node.arguments:
                self.output.write(" ")
                self._generate_node(arg)
        
        self.output.write(")")
    
    def _generate_parameter_list(self, parameters: List[LispSymbol]):
        """Generate parameter list."""
        self.output.write("(")
        for i, param in enumerate(parameters):
            if i > 0:
                self.output.write(" ")
            self._generate_node(param)
        self.output.write(")")
    
    def _write_indent(self, extra_levels: int = 0):
        """Write indentation."""
        total_levels = self.indent_level + extra_levels
        self.output.write(" " * (total_levels * self.indent_size))
    
    def _is_simple_list(self, node: LispList) -> bool:
        """Check if list is simple enough for one line."""
        if len(node.elements) == 0:
            return True
        if len(node.elements) > 5:
            return False
        
        # Check if all elements are atoms or simple symbols
        for elem in node.elements:
            if not isinstance(elem, (LispAtom, LispSymbol)):
                return False
        
        return True
    
    def _is_simple_expression(self, node: LispExpression) -> bool:
        """Check if expression is simple enough for one line."""
        if isinstance(node, (LispAtom, LispSymbol)):
            return True
        elif isinstance(node, LispList):
            return self._is_simple_list(node)
        elif isinstance(node, LispApplication):
            return self._is_simple_application(node)
        else:
            return False
    
    def _is_simple_application(self, node: LispApplication) -> bool:
        """Check if function application is simple enough for one line."""
        if len(node.arguments) > 3:
            return False
        
        # Check function
        if not isinstance(node.function, (LispSymbol, LispAtom)):
            return False
        
        # Check arguments
        for arg in node.arguments:
            if not isinstance(arg, (LispAtom, LispSymbol)):
                return False
        
        return True


def generate_lisp_code(node: LispNode, indent_size: int = 2) -> str:
    """Generate LISP code from AST node."""
    generator = LispCodeGenerator(indent_size)
    return generator.generate(node)


class LispFormatter:
    """LISP code formatter with various formatting options."""
    
    def __init__(self, config: Optional[dict] = None):
        self.config = config or {}
        self.default_config = {
            'indent_size': 2,
            'max_line_length': 80,
            'align_parameters': True,
            'compact_simple_forms': True,
            'space_after_special_forms': True,
            'preserve_comments': True
        }
        
        # Merge configs
        for key, value in self.default_config.items():
            if key not in self.config:
                self.config[key] = value
    
    def format(self, code: str) -> str:
        """Format LISP code."""
        # This is a simplified formatter
        # In a real implementation, you'd parse and reformat
        return self._apply_basic_formatting(code)
    
    def _apply_basic_formatting(self, code: str) -> str:
        """Apply basic formatting rules."""
        lines = code.split('\n')
        formatted_lines = []
        indent_level = 0
        
        for line in lines:
            stripped = line.strip()
            if not stripped:
                formatted_lines.append('')
                continue
            
            # Count parentheses for indentation
            open_parens = stripped.count('(')
            close_parens = stripped.count(')')
            
            # Adjust indent level for closing parens at start
            if stripped.startswith(')'):
                indent_level = max(0, indent_level - close_parens + open_parens)
            
            # Format line with proper indentation
            indent = ' ' * (indent_level * self.config['indent_size'])
            formatted_lines.append(indent + stripped)
            
            # Adjust indent level for next line
            if not stripped.startswith(')'):
                indent_level += open_parens - close_parens
            
            indent_level = max(0, indent_level)
        
        return '\n'.join(formatted_lines)


def format_lisp_code(code: str, config: Optional[dict] = None) -> str:
    """Format LISP code with given configuration."""
    formatter = LispFormatter(config)
    return formatter.format(code) 