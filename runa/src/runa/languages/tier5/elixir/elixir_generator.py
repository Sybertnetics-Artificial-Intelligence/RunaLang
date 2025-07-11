#!/usr/bin/env python3
"""
Elixir Code Generator Module

This module provides comprehensive code generation for the Elixir programming language,
supporting all major language constructs including:
- Clean, idiomatic Elixir syntax
- Proper indentation and formatting
- Actor model with processes and message passing
- Pattern matching and guards
- Functional programming constructs
- Pipe operators and function composition
- Modules, functions, and protocols
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from ...core.base_components import BaseGenerator
from .elixir_ast import *

@dataclass
class ElixirCodeStyle:
    """Configuration for Elixir code formatting."""
    indent_size: int = 2
    max_line_length: int = 100
    use_spaces: bool = True
    trailing_comma: bool = True
    pipe_indent: int = 2
    function_clause_spacing: bool = True
    module_doc_style: str = "moduledoc"  # or "doc"

class ElixirCodeGenerator(BaseGenerator):
    """Generates clean, idiomatic Elixir code from AST."""
    
    def __init__(self, style: Optional[ElixirCodeStyle] = None):
        super().__init__()
        self.style = style or ElixirCodeStyle()
        self.indent_level = 0
        self.output = []
    
    def get_indent(self, extra_levels: int = 0) -> str:
        """Get indentation string for current level."""
        total_levels = self.indent_level + extra_levels
        if self.style.use_spaces:
            return " " * (total_levels * self.style.indent_size)
        else:
            return "\t" * total_levels
    
    def increase_indent(self):
        """Increase indentation level."""
        self.indent_level += 1
    
    def decrease_indent(self):
        """Decrease indentation level."""
        self.indent_level = max(0, self.indent_level - 1)
    
    def emit(self, code: str, indent: bool = True, newline: bool = True):
        """Emit code with optional indentation and newline."""
        if indent:
            code = self.get_indent() + code
        if newline:
            code += "\n"
        self.output.append(code)
    
    def emit_line(self, code: str = "", indent: bool = True):
        """Emit a line of code."""
        self.emit(code, indent=indent, newline=True)
    
    def generate_node(self, node: ElixirNode) -> str:
        """Generate code for any Elixir AST node."""
        method_name = f"generate_{node.node_type.value}"
        method = getattr(self, method_name, None)
        
        if method:
            return method(node)
        else:
            return f"# Unsupported node: {node.node_type.value}"
    
    def generate_atom(self, node: ElixirAtom) -> str:
        """Generate atom literal."""
        if node.value.isidentifier() and not any(c in node.value for c in "?!"):
            return f":{node.value}"
        else:
            # Quoted atom
            return f':{node.value!r}'
    
    def generate_integer(self, node: ElixirInteger) -> str:
        """Generate integer literal."""
        return str(node.value)
    
    def generate_float(self, node: ElixirFloat) -> str:
        """Generate float literal."""
        return str(node.value)
    
    def generate_string(self, node: ElixirString) -> str:
        """Generate string literal."""
        if node.interpolated:
            # String interpolation
            return f'"{node.value}"'
        else:
            return repr(node.value)
    
    def generate_boolean(self, node: ElixirBoolean) -> str:
        """Generate boolean literal."""
        return "true" if node.value else "false"
    
    def generate_nil(self, node: ElixirNil) -> str:
        """Generate nil literal."""
        return "nil"
    
    def generate_variable(self, node: ElixirVariable) -> str:
        """Generate variable."""
        return node.name
    
    def generate_pin(self, node: ElixirPin) -> str:
        """Generate pin operator."""
        return f"^{self.generate_node(node.variable)}"
    
    def generate_list(self, node: ElixirList) -> str:
        """Generate list literal."""
        if not node.elements and not node.tail:
            return "[]"
        
        elements = [self.generate_node(elem) for elem in node.elements]
        
        if node.tail:
            tail_code = self.generate_node(node.tail)
            elements_str = ", ".join(elements)
            return f"[{elements_str} | {tail_code}]"
        else:
            if len(elements) == 1:
                return f"[{elements[0]}]"
            elif len(elements) <= 3:
                return f"[{', '.join(elements)}]"
            else:
                # Multi-line for longer lists
                inner = ",\n".join(f"{self.get_indent(1)}{elem}" for elem in elements)
                return f"[\n{inner}\n{self.get_indent()}]"
    
    def generate_tuple(self, node: ElixirTuple) -> str:
        """Generate tuple literal."""
        elements = [self.generate_node(elem) for elem in node.elements]
        
        if len(elements) == 0:
            return "{}"
        elif len(elements) <= 3:
            return f"{{{', '.join(elements)}}}"
        else:
            # Multi-line for longer tuples
            inner = ",\n".join(f"{self.get_indent(1)}{elem}" for elem in elements)
            return f"{{\n{inner}\n{self.get_indent()}}}"
    
    def generate_map(self, node: ElixirMap) -> str:
        """Generate map literal."""
        if not node.pairs:
            return "%{}"
        
        pairs = []
        for key, value in node.pairs:
            key_code = self.generate_node(key)
            value_code = self.generate_node(value)
            
            # Use shorthand for atom keys
            if isinstance(key, ElixirAtom) and key.value.isidentifier():
                pairs.append(f"{key.value}: {value_code}")
            else:
                pairs.append(f"{key_code} => {value_code}")
        
        if len(pairs) <= 2 and all(len(pair) < 20 for pair in pairs):
            return f"%{{{', '.join(pairs)}}}"
        else:
            # Multi-line for complex maps
            inner = ",\n".join(f"{self.get_indent(1)}{pair}" for pair in pairs)
            return f"%{{\n{inner}\n{self.get_indent()}}}"
    
    def generate_keyword_list(self, node: ElixirKeywordList) -> str:
        """Generate keyword list."""
        pairs = []
        for atom, value in node.pairs:
            value_code = self.generate_node(value)
            pairs.append(f"{atom.value}: {value_code}")
        
        return f"[{', '.join(pairs)}]"
    
    def generate_pipe(self, node: ElixirPipe) -> str:
        """Generate pipe operator."""
        left = self.generate_node(node.left)
        right = self.generate_node(node.right)
        
        # Check if we need to break the line
        full_line = f"{left} |> {right}"
        if len(full_line) <= self.style.max_line_length:
            return full_line
        else:
            # Multi-line pipe
            return f"{left}\n{self.get_indent()}|> {right}"
    
    def generate_match(self, node: ElixirMatch) -> str:
        """Generate match expression."""
        left = self.generate_node(node.left)
        right = self.generate_node(node.right)
        return f"{left} = {right}"
    
    def generate_binary_op(self, node: ElixirBinaryOp) -> str:
        """Generate binary operation."""
        left = self.generate_node(node.left)
        right = self.generate_node(node.right)
        
        # Add spaces around operators
        operators_with_spaces = ["+", "-", "*", "/", "==", "!=", "<", ">", "<=", ">=", "and", "or", "&&", "||"]
        if node.operator in operators_with_spaces:
            return f"{left} {node.operator} {right}"
        else:
            return f"{left}{node.operator}{right}"
    
    def generate_unary_op(self, node: ElixirUnaryOp) -> str:
        """Generate unary operation."""
        operand = self.generate_node(node.operand)
        return f"{node.operator}{operand}"
    
    def generate_function_call(self, node: ElixirFunctionCall) -> str:
        """Generate function call."""
        args = [self.generate_node(arg) for arg in node.args]
        
        if not args:
            return f"{node.function}()"
        elif len(args) == 1:
            return f"{node.function}({args[0]})"
        elif len(args) <= 3 and all(len(arg) < 15 for arg in args):
            return f"{node.function}({', '.join(args)})"
        else:
            # Multi-line for many arguments
            args_str = ",\n".join(f"{self.get_indent(1)}{arg}" for arg in args)
            return f"{node.function}(\n{args_str}\n{self.get_indent()})"
    
    def generate_remote_call(self, node: ElixirRemoteCall) -> str:
        """Generate remote call (Module.function)."""
        module = self.generate_node(node.module)
        args = [self.generate_node(arg) for arg in node.args]
        
        if not args:
            return f"{module}.{node.function}()"
        elif len(args) <= 3:
            return f"{module}.{node.function}({', '.join(args)})"
        else:
            # Multi-line for many arguments
            args_str = ",\n".join(f"{self.get_indent(1)}{arg}" for arg in args)
            return f"{module}.{node.function}(\n{args_str}\n{self.get_indent()})"
    
    def generate_case(self, node: ElixirCase) -> str:
        """Generate case expression."""
        expr = self.generate_node(node.expr)
        result = [f"case {expr} do"]
        
        self.increase_indent()
        for clause in node.clauses:
            clause_code = self.generate_clause(clause)
            result.append(f"{self.get_indent()}{clause_code}")
        self.decrease_indent()
        
        result.append(f"{self.get_indent()}end")
        return "\n".join(result)
    
    def generate_cond(self, node: ElixirCond) -> str:
        """Generate cond expression."""
        result = ["cond do"]
        
        self.increase_indent()
        for clause in node.clauses:
            clause_code = self.generate_clause(clause)
            result.append(f"{self.get_indent()}{clause_code}")
        self.decrease_indent()
        
        result.append(f"{self.get_indent()}end")
        return "\n".join(result)
    
    def generate_if(self, node: ElixirIf) -> str:
        """Generate if expression."""
        condition = self.generate_node(node.condition)
        then_branch = self.generate_node(node.then_branch)
        
        if node.else_branch:
            else_branch = self.generate_node(node.else_branch)
            return f"if {condition} do\n{self.get_indent(1)}{then_branch}\n{self.get_indent()}else\n{self.get_indent(1)}{else_branch}\n{self.get_indent()}end"
        else:
            return f"if {condition} do\n{self.get_indent(1)}{then_branch}\n{self.get_indent()}end"
    
    def generate_unless(self, node: ElixirUnless) -> str:
        """Generate unless expression."""
        condition = self.generate_node(node.condition)
        then_branch = self.generate_node(node.then_branch)
        
        if node.else_branch:
            else_branch = self.generate_node(node.else_branch)
            return f"unless {condition} do\n{self.get_indent(1)}{then_branch}\n{self.get_indent()}else\n{self.get_indent(1)}{else_branch}\n{self.get_indent()}end"
        else:
            return f"unless {condition} do\n{self.get_indent(1)}{then_branch}\n{self.get_indent()}end"
    
    def generate_with(self, node: ElixirWith) -> str:
        """Generate with expression."""
        clauses = [self.generate_clause(clause) for clause in node.clauses]
        body = self.generate_node(node.do_block)
        
        result = [f"with {', '.join(clauses)} do"]
        
        self.increase_indent()
        result.append(f"{self.get_indent()}{body}")
        self.decrease_indent()
        
        if node.else_block:
            else_body = self.generate_node(node.else_block)
            result.append(f"{self.get_indent()}else")
            self.increase_indent()
            result.append(f"{self.get_indent()}{else_body}")
            self.decrease_indent()
        
        result.append(f"{self.get_indent()}end")
        return "\n".join(result)
    
    def generate_clause(self, node: ElixirClause) -> str:
        """Generate function clause or case clause."""
        parts = []
        
        if node.pattern:
            parts.append(self.generate_node(node.pattern))
        
        if node.guard:
            guard_code = self.generate_node(node.guard)
            parts.append(f"when {guard_code}")
        
        body = self.generate_node(node.body)
        pattern_part = " ".join(parts) if parts else ""
        
        if pattern_part:
            return f"{pattern_part} -> {body}"
        else:
            return f"-> {body}"
    
    def generate_function(self, node: ElixirFunction) -> str:
        """Generate function definition."""
        result = []
        
        for i, clause in enumerate(node.clauses):
            if i == 0:
                # First clause uses def/defp
                func_keyword = "defp" if node.private else "def"
                clause_code = self.generate_clause(clause)
                result.append(f"{func_keyword} {node.name}{clause_code}")
            else:
                # Additional clauses
                clause_code = self.generate_clause(clause)
                result.append(f"def {node.name}{clause_code}")
            
            if self.style.function_clause_spacing and i < len(node.clauses) - 1:
                result.append("")
        
        return "\n".join(result)
    
    def generate_anonymous_function(self, node: ElixirAnonymousFunction) -> str:
        """Generate anonymous function."""
        if len(node.clauses) == 1:
            clause = node.clauses[0]
            clause_code = self.generate_clause(clause)
            return f"fn {clause_code} end"
        else:
            result = ["fn"]
            self.increase_indent()
            for clause in node.clauses:
                clause_code = self.generate_clause(clause)
                result.append(f"{self.get_indent()}{clause_code}")
            self.decrease_indent()
            result.append(f"{self.get_indent()}end")
            return "\n".join(result)
    
    def generate_spawn(self, node: ElixirSpawn) -> str:
        """Generate spawn expression."""
        function = self.generate_node(node.function)
        if node.args:
            args = [self.generate_node(arg) for arg in node.args]
            return f"spawn({function}, [{', '.join(args)}])"
        else:
            return f"spawn({function})"
    
    def generate_send(self, node: ElixirSend) -> str:
        """Generate send expression."""
        destination = self.generate_node(node.destination)
        message = self.generate_node(node.message)
        return f"send({destination}, {message})"
    
    def generate_receive(self, node: ElixirReceive) -> str:
        """Generate receive expression."""
        result = ["receive do"]
        
        self.increase_indent()
        for clause in node.clauses:
            clause_code = self.generate_clause(clause)
            result.append(f"{self.get_indent()}{clause_code}")
        self.decrease_indent()
        
        if node.after_clause:
            timeout, body = node.after_clause
            timeout_code = self.generate_node(timeout)
            body_code = self.generate_node(body)
            result.append(f"{self.get_indent()}after")
            self.increase_indent()
            result.append(f"{self.get_indent()}{timeout_code} -> {body_code}")
            self.decrease_indent()
        
        result.append(f"{self.get_indent()}end")
        return "\n".join(result)
    
    def generate_for_comprehension(self, node: ElixirForComprehension) -> str:
        """Generate for comprehension."""
        generators = []
        for pattern, enumerable in node.generators:
            pattern_code = self.generate_node(pattern)
            enum_code = self.generate_node(enumerable)
            generators.append(f"{pattern_code} <- {enum_code}")
        
        parts = ["for"] + generators
        
        if node.filters:
            filter_codes = [self.generate_node(f) for f in node.filters]
            parts.extend(filter_codes)
        
        if node.into:
            into_code = self.generate_node(node.into)
            parts.append(f"into: {into_code}")
        
        if node.body:
            body_code = self.generate_node(node.body)
            return f"{', '.join(parts)}, do: {body_code}"
        else:
            return f"{', '.join(parts)}"
    
    def generate_module(self, node: ElixirModule) -> str:
        """Generate module definition."""
        result = [f"defmodule {node.name} do"]
        
        self.increase_indent()
        
        # Generate attributes first
        for attr in node.attributes:
            attr_code = self.generate_node(attr)
            result.append(f"{self.get_indent()}{attr_code}")
        
        if node.attributes and node.body:
            result.append("")  # Blank line between attributes and body
        
        # Generate body
        for i, stmt in enumerate(node.body):
            stmt_code = self.generate_node(stmt)
            result.append(f"{self.get_indent()}{stmt_code}")
            
            # Add spacing between functions
            if i < len(node.body) - 1 and isinstance(stmt, (ElixirFunction, ElixirDef, ElixirDefp)):
                result.append("")
        
        self.decrease_indent()
        result.append(f"{self.get_indent()}end")
        
        return "\n".join(result)
    
    def generate_defmodule(self, node: ElixirDefmodule) -> str:
        """Generate defmodule statement."""
        return self.generate_module(node.module)
    
    def generate_def(self, node: ElixirDef) -> str:
        """Generate def statement."""
        return self.generate_function(node.function)
    
    def generate_defp(self, node: ElixirDefp) -> str:
        """Generate defp statement."""
        return self.generate_function(node.function)
    
    def generate_module_attribute(self, node: ElixirModuleAttribute) -> str:
        """Generate module attribute."""
        if node.value:
            value_code = self.generate_node(node.value)
            return f"@{node.name} {value_code}"
        else:
            return f"@{node.name}"
    
    def generate_alias(self, node: ElixirAlias) -> str:
        """Generate alias statement."""
        module = self.generate_node(node.module)
        if node.alias:
            return f"alias {module}, as: {node.alias}"
        else:
            return f"alias {module}"
    
    def generate_import(self, node: ElixirImport) -> str:
        """Generate import statement."""
        module = self.generate_node(node.module)
        parts = [f"import {module}"]
        
        if node.only:
            only_list = [f"{name}/{arity}" for name, arity in node.only]
            parts.append(f"only: [{', '.join(only_list)}]")
        
        if node.except_:
            except_list = [f"{name}/{arity}" for name, arity in node.except_]
            parts.append(f"except: [{', '.join(except_list)}]")
        
        return ", ".join(parts)
    
    def generate_program(self, node: ElixirProgram) -> str:
        """Generate complete program."""
        result = []
        
        for i, stmt in enumerate(node.statements):
            stmt_code = self.generate_node(stmt)
            result.append(stmt_code)
            
            # Add spacing between top-level statements
            if i < len(node.statements) - 1:
                result.append("")
        
        return "\n".join(result)

def generate_elixir_code(node: ElixirNode, style: Optional[ElixirCodeStyle] = None) -> str:
    """Generate Elixir code from an AST node."""
    generator = ElixirCodeGenerator(style)
    return generator.generate_node(node) 