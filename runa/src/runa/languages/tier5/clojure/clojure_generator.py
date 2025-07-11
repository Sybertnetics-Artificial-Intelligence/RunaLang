#!/usr/bin/env python3
"""
Clojure Code Generator

Generates clean, idiomatic Clojure code from Clojure AST nodes.
Handles proper S-expression formatting, indentation, and Clojure conventions.
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass
from io import StringIO

from .clojure_ast import *


@dataclass
class ClojureCodeStyle:
    """Clojure code style configuration."""
    indent_size: int = 2
    line_length: int = 80
    use_tabs: bool = False
    align_forms: bool = True
    compact_collections: bool = False
    
    @property
    def indent_string(self) -> str:
        """Get indentation string."""
        if self.use_tabs:
            return '\t'
        return ' ' * self.indent_size


class ClojureCodeGenerator:
    """Generates Clojure source code from AST."""
    
    def __init__(self, style: Optional[ClojureCodeStyle] = None):
        self.style = style or ClojureCodeStyle()
        self.output = StringIO()
        self.indent_level = 0
        self.current_line = ""
    
    def generate(self, node: ClojureNode) -> str:
        """Generate code for AST node."""
        self.output = StringIO()
        self.indent_level = 0
        self.current_line = ""
        
        self.visit(node)
        return self.output.getvalue().strip()
    
    def visit(self, node: ClojureNode) -> str:
        """Visit AST node and generate code."""
        method_name = f"visit_{node.__class__.__name__.lower()}"
        method = getattr(self, method_name, self.visit_generic)
        return method(node)
    
    def visit_generic(self, node: ClojureNode) -> str:
        """Generic visit method."""
        return f";; Unknown node: {type(node)}"
    
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
    
    def visit_clojuremodule(self, node: ClojureModule) -> str:
        """Generate module."""
        # Generate namespace if present
        if node.namespace:
            self.visit(node.namespace)
            self.write_line()
            self.write_line()
        
        # Generate forms
        for i, form in enumerate(node.forms):
            if i > 0:
                self.write_line()
            self.visit(form)
        
        return self.output.getvalue()
    
    def visit_clojurens(self, node: ClojureNs) -> str:
        """Generate namespace declaration."""
        self.write("(ns ")
        self.visit(node.name)
        
        # Add require/import/use clauses if present
        if node.requires or node.imports or node.uses:
            self.write_line()
            self.indent()
            
            for require in node.requires:
                self.write("(:require ")
                self.visit(require.namespace)
                if require.alias:
                    self.write(" :as ")
                    self.visit(require.alias)
                if require.refer:
                    self.write(" :refer [")
                    for i, ref in enumerate(require.refer):
                        if i > 0:
                            self.write(" ")
                        self.visit(ref)
                    self.write("]")
                self.write_line(")")
            
            self.dedent()
        
        self.write_line(")")
        return ""
    
    def visit_clojureliteral(self, node: ClojureLiteral) -> str:
        """Generate literal."""
        if node.literal_type == "nil":
            self.write("nil")
        elif node.literal_type == "boolean":
            self.write("true" if node.value else "false")
        elif node.literal_type == "number":
            self.write(str(node.value))
        elif node.literal_type == "string":
            escaped = node.value.replace('\\', '\\\\').replace('"', '\\"')
            self.write(f'"{escaped}"')
        elif node.literal_type == "char":
            self.write(f"\\{node.value}")
        elif node.literal_type == "keyword":
            if not node.value.startswith(':'):
                self.write(':')
            self.write(node.value.lstrip(':'))
        else:
            self.write(str(node.value))
        return ""
    
    def visit_clojuresymbol(self, node: ClojureSymbol) -> str:
        """Generate symbol."""
        if node.namespace:
            self.write(f"{node.namespace}/{node.name}")
        else:
            self.write(node.name)
        return ""
    
    def visit_clojurelist(self, node: ClojureList) -> str:
        """Generate list."""
        self.write("(")
        
        for i, elem in enumerate(node.elements):
            if i > 0:
                self.write(" ")
            self.visit(elem)
        
        self.write(")")
        return ""
    
    def visit_clojurevector(self, node: ClojureVector) -> str:
        """Generate vector."""
        self.write("[")
        
        for i, elem in enumerate(node.elements):
            if i > 0:
                self.write(" ")
            self.visit(elem)
        
        self.write("]")
        return ""
    
    def visit_clojuremap(self, node: ClojureMap) -> str:
        """Generate map."""
        self.write("{")
        
        for i, (key, value) in enumerate(node.pairs):
            if i > 0:
                self.write(" ")
            self.visit(key)
            self.write(" ")
            self.visit(value)
        
        self.write("}")
        return ""
    
    def visit_clojureset(self, node: ClojureSet) -> str:
        """Generate set."""
        self.write("#{")
        
        for i, elem in enumerate(node.elements):
            if i > 0:
                self.write(" ")
            self.visit(elem)
        
        self.write("}")
        return ""
    
    def visit_clojuredef(self, node: ClojureDef) -> str:
        """Generate def form."""
        self.write("(def ")
        self.visit(node.symbol)
        
        if node.doc_string:
            self.write(f' "{node.doc_string}"')
        
        self.write(" ")
        self.visit(node.value)
        self.write_line(")")
        return ""
    
    def visit_clojuredefn(self, node: ClojureDefn) -> str:
        """Generate defn form."""
        self.write("(defn ")
        self.visit(node.name)
        
        if node.doc_string:
            self.write_line()
            self.indent()
            self.write(f'"{node.doc_string}"')
            self.write_line()
            self.dedent()
        
        # Generate arities
        if len(node.arities) == 1:
            # Single arity
            arity = node.arities[0]
            self.write(" [")
            for i, param in enumerate(arity.params):
                if i > 0:
                    self.write(" ")
                self.visit(param)
            self.write("]")
            
            if len(arity.body) == 1:
                self.write(" ")
                self.visit(arity.body[0])
            else:
                self.write_line()
                self.indent()
                for expr in arity.body:
                    self.visit(expr)
                    self.write_line()
                self.dedent()
        else:
            # Multiple arities
            self.write_line()
            self.indent()
            for arity in node.arities:
                self.write("([")
                for i, param in enumerate(arity.params):
                    if i > 0:
                        self.write(" ")
                    self.visit(param)
                self.write("] ")
                
                if len(arity.body) == 1:
                    self.visit(arity.body[0])
                else:
                    self.write_line()
                    self.indent()
                    for expr in arity.body:
                        self.visit(expr)
                        self.write_line()
                    self.dedent()
                
                self.write_line(")")
            self.dedent()
        
        self.write_line(")")
        return ""
    
    def visit_clojurefn(self, node: ClojureFn) -> str:
        """Generate fn form."""
        self.write("(fn")
        
        if node.name:
            self.write(" ")
            self.visit(node.name)
        
        if node.arities:
            arity = node.arities[0]  # Simplified for single arity
            self.write(" [")
            for i, param in enumerate(arity.params):
                if i > 0:
                    self.write(" ")
                self.visit(param)
            self.write("]")
            
            for expr in arity.body:
                self.write(" ")
                self.visit(expr)
        
        self.write(")")
        return ""
    
    def visit_clojurelet(self, node: ClojureLet) -> str:
        """Generate let form."""
        self.write("(let [")
        
        for i, (symbol, value) in enumerate(node.bindings):
            if i > 0:
                self.write(" ")
            self.visit(symbol)
            self.write(" ")
            self.visit(value)
        
        self.write("]")
        
        if len(node.body) == 1:
            self.write(" ")
            self.visit(node.body[0])
        else:
            self.write_line()
            self.indent()
            for expr in node.body:
                self.visit(expr)
                self.write_line()
            self.dedent()
        
        self.write(")")
        return ""
    
    def visit_clojureif(self, node: ClojureIf) -> str:
        """Generate if form."""
        self.write("(if ")
        self.visit(node.test)
        self.write(" ")
        self.visit(node.then_expr)
        
        if node.else_expr:
            self.write(" ")
            self.visit(node.else_expr)
        
        self.write(")")
        return ""
    
    def visit_clojurecond(self, node: ClojureCond) -> str:
        """Generate cond form."""
        self.write("(cond")
        
        if node.clauses:
            self.write_line()
            self.indent()
            
            for test, expr in node.clauses:
                self.visit(test)
                self.write(" ")
                self.visit(expr)
                self.write_line()
            
            self.dedent()
        
        self.write(")")
        return ""
    
    def visit_clojuredo(self, node: ClojureDo) -> str:
        """Generate do form."""
        self.write("(do")
        
        for expr in node.expressions:
            self.write(" ")
            self.visit(expr)
        
        self.write(")")
        return ""
    
    def visit_clojureloop(self, node: ClojureLoop) -> str:
        """Generate loop form."""
        self.write("(loop [")
        
        for i, (symbol, value) in enumerate(node.bindings):
            if i > 0:
                self.write(" ")
            self.visit(symbol)
            self.write(" ")
            self.visit(value)
        
        self.write("]")
        
        if len(node.body) == 1:
            self.write(" ")
            self.visit(node.body[0])
        else:
            self.write_line()
            self.indent()
            for expr in node.body:
                self.visit(expr)
                self.write_line()
            self.dedent()
        
        self.write(")")
        return ""
    
    def visit_clojurerecur(self, node: ClojureRecur) -> str:
        """Generate recur form."""
        self.write("(recur")
        
        for arg in node.args:
            self.write(" ")
            self.visit(arg)
        
        self.write(")")
        return ""
    
    def visit_clojurequote(self, node: ClojureQuote) -> str:
        """Generate quote."""
        self.write("'")
        self.visit(node.expression)
        return ""
    
    def visit_clojuresyntaxquote(self, node: ClojureSyntaxQuote) -> str:
        """Generate syntax quote."""
        self.write("`")
        self.visit(node.expression)
        return ""
    
    def visit_clojureunquote(self, node: ClojureUnquote) -> str:
        """Generate unquote."""
        self.write("~")
        self.visit(node.expression)
        return ""
    
    def visit_clojureunquotesplicing(self, node: ClojureUnquoteSplicing) -> str:
        """Generate unquote splicing."""
        self.write("~@")
        self.visit(node.expression)
        return ""
    
    def visit_clojurederef(self, node: ClojureDeref) -> str:
        """Generate deref."""
        self.write("@")
        self.visit(node.expression)
        return ""
    
    def visit_clojurejavainterop(self, node: ClojureJavaInterop) -> str:
        """Generate Java interop."""
        self.write("(.")
        self.write(node.method)
        self.write(" ")
        self.visit(node.target)
        
        for arg in node.args:
            self.write(" ")
            self.visit(arg)
        
        self.write(")")
        return ""
    
    def visit_clojurenew(self, node: ClojureNew) -> str:
        """Generate new form."""
        self.write("(new ")
        self.visit(node.class_name)
        
        for arg in node.args:
            self.write(" ")
            self.visit(arg)
        
        self.write(")")
        return ""


def generate_clojure(node: ClojureNode, style: Optional[ClojureCodeStyle] = None) -> str:
    """Generate Clojure code from AST node."""
    generator = ClojureCodeGenerator(style)
    return generator.generate(node) 