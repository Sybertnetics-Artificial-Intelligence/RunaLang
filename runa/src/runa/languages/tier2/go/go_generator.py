#!/usr/bin/env python3
"""
Go Code Generator

Generates clean, idiomatic Go source code from Go AST nodes.
Supports all Go language features including:
- Packages and imports
- Type system (structs, interfaces, channels, maps, slices)
- Functions and methods with multiple return values
- Goroutines and channel operations
- Control flow (if, for, switch, select, defer)
- Error handling patterns
- Proper Go formatting and style conventions
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass
from io import StringIO

from .go_ast import *


@dataclass
class GoGeneratorOptions:
    """Options for Go code generation."""
    indent_size: int = 4
    use_tabs: bool = True
    max_line_length: int = 120
    format_imports: bool = True
    add_comments: bool = True
    gofmt_style: bool = True
    
    # Go-specific options
    package_comment: bool = True
    function_comments: bool = True
    type_comments: bool = True
    error_handling_style: str = "explicit"  # "explicit" or "panic"


class GoCodeGenerator:
    """Go code generator for producing clean Go source code."""
    
    def __init__(self, options: GoGeneratorOptions = None):
        self.options = options or GoGeneratorOptions()
        self.output = StringIO()
        self.indent_level = 0
        self.current_line_empty = True
        
    def generate(self, node: GoNode) -> str:
        """Generate Go code from AST node."""
        self.output = StringIO()
        self.indent_level = 0
        self.current_line_empty = True
        
        self.visit(node)
        
        result = self.output.getvalue()
        self.output.close()
        
        return result
    
    def visit(self, node: GoNode):
        """Visit AST node and generate code."""
        if node is None:
            return
        
        method_name = f"visit_{node.__class__.__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        visitor(node)
    
    def generic_visit(self, node: GoNode):
        """Generic visitor for unknown nodes."""
        self.write(f"/* Unknown node: {node.__class__.__name__} */")
    
    def write(self, text: str):
        """Write text to output."""
        if text == "":
            return
        
        if self.current_line_empty and text.strip():
            self.write_indent()
        
        self.output.write(text)
        self.current_line_empty = False
    
    def writeln(self, text: str = ""):
        """Write line to output."""
        if text:
            self.write(text)
        self.output.write("\n")
        self.current_line_empty = True
    
    def write_indent(self):
        """Write current indentation."""
        if self.options.use_tabs:
            self.output.write("\t" * self.indent_level)
        else:
            self.output.write(" " * (self.indent_level * self.options.indent_size))
    
    def indent(self):
        """Increase indentation level."""
        self.indent_level += 1
    
    def dedent(self):
        """Decrease indentation level."""
        self.indent_level = max(0, self.indent_level - 1)
    
    def write_block(self, statements: List[GoStatement], add_braces: bool = True):
        """Write block of statements."""
        if add_braces:
            self.writeln(" {")
            self.indent()
        
        for i, stmt in enumerate(statements):
            if i > 0 and self._needs_blank_line_before(stmt):
                self.writeln()
            self.visit(stmt)
            if not isinstance(stmt, (GoBlockStatement, GoIfStatement, GoForStatement, GoSwitchStatement)):
                self.writeln()
        
        if add_braces:
            self.dedent()
            self.write("}")
    
    def _needs_blank_line_before(self, stmt: GoStatement) -> bool:
        """Check if statement needs blank line before it."""
        return isinstance(stmt, (GoFunctionDeclaration, GoTypeDeclaration, GoVarDeclaration, GoConstDeclaration))
    
    # Node visitors
    
    def visit_GoProgram(self, node: GoProgram):
        """Generate code for Go program."""
        for i, file_node in enumerate(node.files):
            if i > 0:
                self.writeln()
                self.writeln("// ========== Next File ==========")
                self.writeln()
            self.visit(file_node)
    
    def visit_GoFile(self, node: GoFile):
        """Generate code for Go file."""
        # Package declaration
        if node.package:
            if self.options.package_comment:
                self.writeln("// Package declaration")
            self.visit(node.package)
            self.writeln()
        
        # Import declarations
        if node.imports:
            if len(node.imports) == 1 and len(node.imports[0].specs) == 1:
                # Single import
                self.visit(node.imports[0])
                self.writeln()
            else:
                # Multiple imports - group them
                self.writeln("import (")
                self.indent()
                for import_decl in node.imports:
                    for spec in import_decl.specs:
                        self.visit(spec)
                        self.writeln()
                self.dedent()
                self.writeln(")")
            self.writeln()
        
        # Top-level declarations
        for i, decl in enumerate(node.declarations):
            if i > 0:
                self.writeln()
            self.visit(decl)
            self.writeln()
    
    def visit_GoPackageDeclaration(self, node: GoPackageDeclaration):
        """Generate package declaration."""
        self.write(f"package {node.name}")
    
    def visit_GoImportDeclaration(self, node: GoImportDeclaration):
        """Generate import declaration."""
        if len(node.specs) == 1:
            self.write("import ")
            self.visit(node.specs[0])
        else:
            self.writeln("import (")
            self.indent()
            for spec in node.specs:
                self.visit(spec)
                self.writeln()
            self.dedent()
            self.write(")")
    
    def visit_GoImportSpec(self, node: GoImportSpec):
        """Generate import specification."""
        if node.name:
            if node.name == ".":
                self.write(". ")
            else:
                self.write(f"{node.name} ")
        self.write(f'"{node.path}"')
    
    # Type visitors
    
    def visit_GoBasicType(self, node: GoBasicType):
        """Generate basic type."""
        self.write(node.name)
    
    def visit_GoArrayType(self, node: GoArrayType):
        """Generate array type."""
        self.write("[")
        if node.length:
            self.visit(node.length)
        self.write("]")
        if node.element_type:
            self.visit(node.element_type)
    
    def visit_GoSliceType(self, node: GoSliceType):
        """Generate slice type."""
        self.write("[]")
        if node.element_type:
            self.visit(node.element_type)
    
    def visit_GoStructType(self, node: GoStructType):
        """Generate struct type."""
        self.write("struct")
        if not node.fields:
            self.write("{}")
            return
        
        self.writeln(" {")
        self.indent()
        
        for field in node.fields:
            self.visit(field)
            self.writeln()
        
        self.dedent()
        self.write("}")
    
    def visit_GoPointerType(self, node: GoPointerType):
        """Generate pointer type."""
        self.write("*")
        if node.base_type:
            self.visit(node.base_type)
    
    def visit_GoFunctionType(self, node: GoFunctionType):
        """Generate function type."""
        self.write("func(")
        
        # Parameters
        for i, param in enumerate(node.params):
            if i > 0:
                self.write(", ")
            self.visit(param)
        
        self.write(")")
        
        # Return type
        if node.results:
            if len(node.results) == 1 and not node.results[0].names:
                # Single unnamed return type
                self.write(" ")
                self.visit(node.results[0].type)
            else:
                # Multiple or named return types
                self.write(" (")
                for i, result in enumerate(node.results):
                    if i > 0:
                        self.write(", ")
                    self.visit(result)
                self.write(")")
    
    def visit_GoInterfaceType(self, node: GoInterfaceType):
        """Generate interface type."""
        self.write("interface")
        if not node.methods:
            self.write("{}")
            return
        
        self.writeln(" {")
        self.indent()
        
        for method in node.methods:
            self.visit(method)
            self.writeln()
        
        self.dedent()
        self.write("}")
    
    def visit_GoMapType(self, node: GoMapType):
        """Generate map type."""
        self.write("map[")
        if node.key_type:
            self.visit(node.key_type)
        self.write("]")
        if node.value_type:
            self.visit(node.value_type)
    
    def visit_GoChannelType(self, node: GoChannelType):
        """Generate channel type."""
        if node.direction == GoChannelDirection.RECEIVE:
            self.write("<-chan ")
        elif node.direction == GoChannelDirection.SEND:
            self.write("chan<- ")
        else:
            self.write("chan ")
        
        if node.value_type:
            self.visit(node.value_type)
    
    def visit_GoField(self, node: GoField):
        """Generate struct field or function parameter."""
        # Field names
        if node.names:
            for i, name in enumerate(node.names):
                if i > 0:
                    self.write(", ")
                self.write(name)
            self.write(" ")
        
        # Field type
        if node.type:
            self.visit(node.type)
        
        # Struct tag
        if node.tag:
            self.write(f" `{node.tag}`")
    
    def visit_GoMethodSpec(self, node: GoMethodSpec):
        """Generate interface method specification."""
        self.write(node.name)
        if node.type:
            # Extract function signature without 'func' keyword
            if isinstance(node.type, GoFunctionType):
                self.write("(")
                for i, param in enumerate(node.type.params):
                    if i > 0:
                        self.write(", ")
                    self.visit(param)
                self.write(")")
                
                if node.type.results:
                    if len(node.type.results) == 1 and not node.type.results[0].names:
                        self.write(" ")
                        self.visit(node.type.results[0].type)
                    else:
                        self.write(" (")
                        for i, result in enumerate(node.type.results):
                            if i > 0:
                                self.write(", ")
                            self.visit(result)
                        self.write(")")
    
    # Expression visitors
    
    def visit_GoIdentifier(self, node: GoIdentifier):
        """Generate identifier."""
        self.write(node.name)
    
    def visit_GoBasicLiteral(self, node: GoBasicLiteral):
        """Generate basic literal."""
        self.write(node.value)
    
    def visit_GoCompositeLiteral(self, node: GoCompositeLiteral):
        """Generate composite literal."""
        if node.type:
            self.visit(node.type)
        
        self.write("{")
        for i, element in enumerate(node.elements):
            if i > 0:
                self.write(", ")
            self.visit(element)
        self.write("}")
    
    def visit_GoFunctionLiteral(self, node: GoFunctionLiteral):
        """Generate function literal (closure)."""
        if node.type:
            self.visit(node.type)
        
        if node.body:
            self.write(" ")
            self.visit(node.body)
    
    def visit_GoUnaryExpression(self, node: GoUnaryExpression):
        """Generate unary expression."""
        self.write(node.operator.value)
        if node.operand:
            self.visit(node.operand)
    
    def visit_GoBinaryExpression(self, node: GoBinaryExpression):
        """Generate binary expression."""
        if node.left:
            self.visit(node.left)
        
        self.write(f" {node.operator.value} ")
        
        if node.right:
            self.visit(node.right)
    
    def visit_GoCallExpression(self, node: GoCallExpression):
        """Generate function call."""
        if node.function:
            self.visit(node.function)
        
        self.write("(")
        for i, arg in enumerate(node.args):
            if i > 0:
                self.write(", ")
            self.visit(arg)
        
        if node.ellipsis:
            self.write("...")
        
        self.write(")")
    
    def visit_GoIndexExpression(self, node: GoIndexExpression):
        """Generate index expression."""
        if node.expr:
            self.visit(node.expr)
        
        self.write("[")
        if node.index:
            self.visit(node.index)
        self.write("]")
    
    def visit_GoSliceExpression(self, node: GoSliceExpression):
        """Generate slice expression."""
        if node.expr:
            self.visit(node.expr)
        
        self.write("[")
        
        if node.low:
            self.visit(node.low)
        self.write(":")
        
        if node.high:
            self.visit(node.high)
        
        if node.slice3 and node.max:
            self.write(":")
            self.visit(node.max)
        
        self.write("]")
    
    def visit_GoSelectorExpression(self, node: GoSelectorExpression):
        """Generate selector expression."""
        if node.expr:
            self.visit(node.expr)
        self.write(f".{node.selector}")
    
    def visit_GoTypeAssertionExpression(self, node: GoTypeAssertionExpression):
        """Generate type assertion."""
        if node.expr:
            self.visit(node.expr)
        
        self.write(".(")
        if node.type:
            self.visit(node.type)
        else:
            self.write("type")  # For type switches
        self.write(")")
    
    def visit_GoParenExpression(self, node: GoParenExpression):
        """Generate parenthesized expression."""
        self.write("(")
        if node.expr:
            self.visit(node.expr)
        self.write(")")
    
    # Statement visitors
    
    def visit_GoExpressionStatement(self, node: GoExpressionStatement):
        """Generate expression statement."""
        if node.expr:
            self.visit(node.expr)
    
    def visit_GoAssignmentStatement(self, node: GoAssignmentStatement):
        """Generate assignment statement."""
        # Left side
        for i, expr in enumerate(node.left):
            if i > 0:
                self.write(", ")
            self.visit(expr)
        
        self.write(f" {node.operator.value} ")
        
        # Right side
        for i, expr in enumerate(node.right):
            if i > 0:
                self.write(", ")
            self.visit(expr)
    
    def visit_GoShortVarDeclaration(self, node: GoShortVarDeclaration):
        """Generate short variable declaration."""
        # Left side
        for i, expr in enumerate(node.left):
            if i > 0:
                self.write(", ")
            self.visit(expr)
        
        self.write(" := ")
        
        # Right side
        for i, expr in enumerate(node.right):
            if i > 0:
                self.write(", ")
            self.visit(expr)
    
    def visit_GoIncDecStatement(self, node: GoIncDecStatement):
        """Generate increment/decrement statement."""
        if node.expr:
            self.visit(node.expr)
        self.write(node.operator.value)
    
    def visit_GoBlockStatement(self, node: GoBlockStatement):
        """Generate block statement."""
        self.writeln("{")
        self.indent()
        
        for stmt in node.statements:
            self.visit(stmt)
            if not isinstance(stmt, (GoBlockStatement, GoIfStatement, GoForStatement, GoSwitchStatement)):
                self.writeln()
        
        self.dedent()
        self.write("}")
    
    def visit_GoIfStatement(self, node: GoIfStatement):
        """Generate if statement."""
        self.write("if ")
        
        # Init statement
        if node.init:
            self.visit(node.init)
            self.write("; ")
        
        # Condition
        if node.condition:
            self.visit(node.condition)
        
        # Body
        if node.body:
            self.write(" ")
            self.visit(node.body)
        
        # Else clause
        if node.else_stmt:
            self.write(" else ")
            if isinstance(node.else_stmt, GoIfStatement):
                self.visit(node.else_stmt)
            else:
                self.visit(node.else_stmt)
    
    def visit_GoForStatement(self, node: GoForStatement):
        """Generate for statement."""
        self.write("for ")
        
        # Init statement
        if node.init:
            self.visit(node.init)
        
        if node.condition or node.post:
            self.write("; ")
            
            # Condition
            if node.condition:
                self.visit(node.condition)
            
            if node.post:
                self.write("; ")
                self.visit(node.post)
        
        # Body
        if node.body:
            self.write(" ")
            self.visit(node.body)
    
    def visit_GoRangeStatement(self, node: GoRangeStatement):
        """Generate range statement."""
        self.write("for ")
        
        # Key and value
        if node.key:
            self.visit(node.key)
            if node.value:
                self.write(", ")
                self.visit(node.value)
        
        self.write(f" {node.assign_token} range ")
        
        # Expression
        if node.expr:
            self.visit(node.expr)
        
        # Body
        if node.body:
            self.write(" ")
            self.visit(node.body)
    
    def visit_GoSwitchStatement(self, node: GoSwitchStatement):
        """Generate switch statement."""
        self.write("switch ")
        
        # Init statement
        if node.init:
            self.visit(node.init)
            self.write("; ")
        
        # Tag
        if node.tag:
            self.visit(node.tag)
        
        self.writeln(" {")
        
        # Cases
        for case in node.body:
            self.visit(case)
        
        self.write("}")
    
    def visit_GoTypeSwitchStatement(self, node: GoTypeSwitchStatement):
        """Generate type switch statement."""
        self.write("switch ")
        
        # Init statement
        if node.init:
            self.visit(node.init)
            self.write("; ")
        
        # Assignment
        if node.assign:
            self.visit(node.assign)
        
        self.writeln(" {")
        
        # Cases
        for case in node.body:
            self.visit(case)
        
        self.write("}")
    
    def visit_GoSelectStatement(self, node: GoSelectStatement):
        """Generate select statement."""
        self.writeln("select {")
        
        for comm in node.body:
            self.visit(comm)
        
        self.write("}")
    
    def visit_GoCaseClause(self, node: GoCaseClause):
        """Generate case clause."""
        if node.values:
            self.write("case ")
            for i, value in enumerate(node.values):
                if i > 0:
                    self.write(", ")
                self.visit(value)
        else:
            self.write("default")
        
        self.writeln(":")
        
        # Case body
        if node.body:
            self.indent()
            for stmt in node.body:
                self.visit(stmt)
                if not isinstance(stmt, (GoBlockStatement, GoIfStatement, GoForStatement)):
                    self.writeln()
            self.dedent()
    
    def visit_GoCommClause(self, node: GoCommClause):
        """Generate communication clause for select."""
        if node.comm:
            self.write("case ")
            self.visit(node.comm)
        else:
            self.write("default")
        
        self.writeln(":")
        
        # Comm body
        if node.body:
            self.indent()
            for stmt in node.body:
                self.visit(stmt)
                if not isinstance(stmt, (GoBlockStatement, GoIfStatement, GoForStatement)):
                    self.writeln()
            self.dedent()
    
    def visit_GoDeferStatement(self, node: GoDeferStatement):
        """Generate defer statement."""
        self.write("defer ")
        if node.call:
            self.visit(node.call)
    
    def visit_GoGoStatement(self, node: GoGoStatement):
        """Generate go statement (goroutine)."""
        self.write("go ")
        if node.call:
            self.visit(node.call)
    
    def visit_GoReturnStatement(self, node: GoReturnStatement):
        """Generate return statement."""
        self.write("return")
        if node.results:
            self.write(" ")
            for i, result in enumerate(node.results):
                if i > 0:
                    self.write(", ")
                self.visit(result)
    
    def visit_GoBreakStatement(self, node: GoBreakStatement):
        """Generate break statement."""
        self.write("break")
        if node.label:
            self.write(f" {node.label}")
    
    def visit_GoContinueStatement(self, node: GoContinueStatement):
        """Generate continue statement."""
        self.write("continue")
        if node.label:
            self.write(f" {node.label}")
    
    def visit_GoGotoStatement(self, node: GoGotoStatement):
        """Generate goto statement."""
        self.write(f"goto {node.label}")
    
    def visit_GoFallthroughStatement(self, node: GoFallthroughStatement):
        """Generate fallthrough statement."""
        self.write("fallthrough")
    
    def visit_GoLabeledStatement(self, node: GoLabeledStatement):
        """Generate labeled statement."""
        self.write(f"{node.label}:")
        if node.stmt:
            self.writeln()
            self.visit(node.stmt)
    
    def visit_GoSendStatement(self, node: GoSendStatement):
        """Generate send statement."""
        if node.channel:
            self.visit(node.channel)
        self.write(" <- ")
        if node.value:
            self.visit(node.value)
    
    # Declaration visitors
    
    def visit_GoConstDeclaration(self, node: GoConstDeclaration):
        """Generate const declaration."""
        if len(node.specs) == 1:
            self.write("const ")
            self.visit(node.specs[0])
        else:
            self.writeln("const (")
            self.indent()
            for spec in node.specs:
                self.visit(spec)
                self.writeln()
            self.dedent()
            self.write(")")
    
    def visit_GoVarDeclaration(self, node: GoVarDeclaration):
        """Generate var declaration."""
        if len(node.specs) == 1:
            self.write("var ")
            self.visit(node.specs[0])
        else:
            self.writeln("var (")
            self.indent()
            for spec in node.specs:
                self.visit(spec)
                self.writeln()
            self.dedent()
            self.write(")")
    
    def visit_GoValueSpec(self, node: GoValueSpec):
        """Generate value specification."""
        # Names
        for i, name in enumerate(node.names):
            if i > 0:
                self.write(", ")
            self.write(name)
        
        # Type
        if node.type:
            self.write(" ")
            self.visit(node.type)
        
        # Values
        if node.values:
            self.write(" = ")
            for i, value in enumerate(node.values):
                if i > 0:
                    self.write(", ")
                self.visit(value)
    
    def visit_GoTypeDeclaration(self, node: GoTypeDeclaration):
        """Generate type declaration."""
        if len(node.specs) == 1:
            self.write("type ")
            self.visit(node.specs[0])
        else:
            self.writeln("type (")
            self.indent()
            for spec in node.specs:
                self.visit(spec)
                self.writeln()
            self.dedent()
            self.write(")")
    
    def visit_GoTypeSpec(self, node: GoTypeSpec):
        """Generate type specification."""
        self.write(f"{node.name} ")
        if node.type:
            self.visit(node.type)
    
    def visit_GoFunctionDeclaration(self, node: GoFunctionDeclaration):
        """Generate function declaration."""
        if self.options.function_comments and node.comment:
            self.writeln(f"// {node.comment}")
        
        self.write(f"func {node.name}")
        
        if node.type:
            # Parameters
            self.write("(")
            if node.type.params:
                for i, param in enumerate(node.type.params):
                    if i > 0:
                        self.write(", ")
                    self.visit(param)
            self.write(")")
            
            # Return type
            if node.type.results:
                if len(node.type.results) == 1 and not node.type.results[0].names:
                    self.write(" ")
                    self.visit(node.type.results[0].type)
                else:
                    self.write(" (")
                    for i, result in enumerate(node.type.results):
                        if i > 0:
                            self.write(", ")
                        self.visit(result)
                    self.write(")")
        
        # Body
        if node.body:
            self.write(" ")
            self.visit(node.body)
    
    def visit_GoMethodDeclaration(self, node: GoMethodDeclaration):
        """Generate method declaration."""
        if self.options.function_comments and node.comment:
            self.writeln(f"// {node.comment}")
        
        self.write("func ")
        
        # Receiver
        if node.receiver:
            self.write("(")
            self.visit(node.receiver)
            self.write(") ")
        
        self.write(node.name)
        
        if node.type:
            # Parameters
            self.write("(")
            if node.type.params:
                for i, param in enumerate(node.type.params):
                    if i > 0:
                        self.write(", ")
                    self.visit(param)
            self.write(")")
            
            # Return type
            if node.type.results:
                if len(node.type.results) == 1 and not node.type.results[0].names:
                    self.write(" ")
                    self.visit(node.type.results[0].type)
                else:
                    self.write(" (")
                    for i, result in enumerate(node.type.results):
                        if i > 0:
                            self.write(", ")
                        self.visit(result)
                    self.write(")")
        
        # Body
        if node.body:
            self.write(" ")
            self.visit(node.body)


# Convenience functions
def generate_go_code(node: GoNode, options: GoGeneratorOptions = None) -> str:
    """Generate Go code from AST node."""
    generator = GoCodeGenerator(options)
    return generator.generate(node)


def format_go_code(code: str) -> str:
    """Format Go code using basic formatting rules."""
    # This is a simplified formatter
    # In production, you'd want to use gofmt or a more sophisticated formatter
    lines = code.split('\n')
    formatted_lines = []
    indent_level = 0
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            formatted_lines.append('')
            continue
        
        # Adjust indentation
        if stripped.endswith('{'):
            formatted_lines.append('\t' * indent_level + stripped)
            indent_level += 1
        elif stripped.startswith('}'):
            indent_level = max(0, indent_level - 1)
            formatted_lines.append('\t' * indent_level + stripped)
        else:
            formatted_lines.append('\t' * indent_level + stripped)
    
    return '\n'.join(formatted_lines)


# Example usage
if __name__ == "__main__":
    # Create a simple Go program AST
    package_decl = GoPackageDeclaration(name="main")
    
    import_spec = GoImportSpec(path="fmt")
    import_decl = GoImportDeclaration(specs=[import_spec])
    
    # main function
    main_body = GoBlockStatement(statements=[
        GoExpressionStatement(expr=GoCallExpression(
            function=GoSelectorExpression(
                expr=GoIdentifier(name="fmt"),
                selector="Println"
            ),
            args=[GoBasicLiteral(kind=GoBasicLiteralKind.STRING, value='"Hello, World!"')]
        ))
    ])
    
    main_func = GoFunctionDeclaration(
        name="main",
        type=GoFunctionType(params=[], results=[]),
        body=main_body
    )
    
    file_node = GoFile(
        package=package_decl,
        imports=[import_decl],
        declarations=[main_func]
    )
    
    program = GoProgram(files=[file_node])
    
    # Generate code
    generator = GoCodeGenerator()
    code = generator.generate(program)
    print(code) 