"""
LIGO Code Generator

Generates idiomatic LIGO code from AST nodes, supporting both JsLIGO and CameLIGO syntaxes.
"""

from typing import List, Optional, Union, Dict, Any
from io import StringIO
from .ligo_ast import *


class LIGOGenerator:
    """Generates LIGO code from AST nodes."""
    
    def __init__(self, syntax_style: LIGOSyntax = LIGOSyntax.JSLIGO, indent_size: int = 2):
        self.syntax_style = syntax_style
        self.indent_size = indent_size
        self.indent_level = 0
        self.output = StringIO()
        
    def generate(self, node: LIGONode) -> str:
        """Generate LIGO code for any AST node."""
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
            self._write("  " * self.indent_level + text + "\n")
        else:
            self._write("\n")
    
    def _indent(self):
        """Increase indentation level."""
        self.indent_level += 1
    
    def _dedent(self):
        """Decrease indentation level."""
        self.indent_level = max(0, self.indent_level - 1)
    
    def _visit(self, node: Optional[LIGONode]):
        """Visit a node and generate code for it."""
        if node is None:
            return
            
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self.visit_generic)
        visitor(node)
    
    def visit_generic(self, node: LIGONode):
        """Generic visitor for unknown nodes."""
        self._write(str(node))
    
    # Program and declarations
    def visit_LIGOProgram(self, node: LIGOProgram):
        """Generate code for LIGO program."""
        # Add syntax pragma for JsLIGO
        if self.syntax_style == LIGOSyntax.JSLIGO:
            self._write_line("#import \"@ligo/fa/lib/fa2/asset/extendable_fa2.jsligo\" \"FA2\"")
            self._write_line()
        
        for i, decl in enumerate(node.declarations):
            if i > 0:
                self._write_line()
            self._visit(decl)
    
    def visit_LIGOFunctionDecl(self, node: LIGOFunctionDecl):
        """Generate code for function declaration."""
        if self.syntax_style == LIGOSyntax.JSLIGO:
            self._generate_jsligo_function(node)
        else:
            self._generate_cameligo_function(node)
    
    def _generate_jsligo_function(self, node: LIGOFunctionDecl):
        """Generate JsLIGO function."""
        # Function signature
        visibility = "export " if node.visibility == LIGOVisibility.PUBLIC else ""
        
        self._write(f"{visibility}const {node.name} = (")
        
        # Parameters
        for i, param in enumerate(node.parameters):
            if i > 0:
                self._write(", ")
            self._write(param.name)
            if param.type_annotation:
                self._write(": ")
                self._visit(param.type_annotation)
        
        self._write(")")
        
        # Return type
        if node.return_type:
            self._write(": ")
            self._visit(node.return_type)
        
        self._write(" => {")
        self._write_line()
        
        # Function body
        self._indent()
        for stmt in node.body:
            self._visit(stmt)
            self._write_line()
        self._dedent()
        
        self._write_line("};")
    
    def _generate_cameligo_function(self, node: LIGOFunctionDecl):
        """Generate CameLIGO function."""
        self._write(f"let {node.name} (")
        
        # Parameters
        for i, param in enumerate(node.parameters):
            if i > 0:
                self._write(", ")
            self._write(param.name)
            if param.type_annotation:
                self._write(" : ")
                self._visit(param.type_annotation)
        
        self._write(")")
        
        # Return type
        if node.return_type:
            self._write(" : ")
            self._visit(node.return_type)
        
        self._write(" =")
        self._write_line()
        
        # Function body
        self._indent()
        for stmt in node.body:
            self._visit(stmt)
            self._write_line()
        self._dedent()
    
    def visit_LIGOVariableDecl(self, node: LIGOVariableDecl):
        """Generate code for variable declaration."""
        if self.syntax_style == LIGOSyntax.JSLIGO:
            self._generate_jsligo_variable(node)
        else:
            self._generate_cameligo_variable(node)
    
    def _generate_jsligo_variable(self, node: LIGOVariableDecl):
        """Generate JsLIGO variable declaration."""
        keyword = "const" if node.is_const else "let"
        self._write(f"{keyword} {node.name}")
        
        if node.type_annotation:
            self._write(": ")
            self._visit(node.type_annotation)
        
        if node.value:
            self._write(" = ")
            self._visit(node.value)
        
        self._write(";")
    
    def _generate_cameligo_variable(self, node: LIGOVariableDecl):
        """Generate CameLIGO variable declaration."""
        self._write(f"let {node.name}")
        
        if node.type_annotation:
            self._write(" : ")
            self._visit(node.type_annotation)
        
        if node.value:
            self._write(" = ")
            self._visit(node.value)
        
        self._write(" in")
    
    def visit_LIGOTypeDecl(self, node: LIGOTypeDecl):
        """Generate code for type declaration."""
        if self.syntax_style == LIGOSyntax.JSLIGO:
            self._write(f"type {node.name} = ")
        else:
            self._write(f"type {node.name} = ")
        
        self._visit(node.type_def)
        
        if self.syntax_style == LIGOSyntax.JSLIGO:
            self._write(";")
    
    def visit_LIGOContractDecl(self, node: LIGOContractDecl):
        """Generate code for contract declaration."""
        if self.syntax_style == LIGOSyntax.JSLIGO:
            self._generate_jsligo_contract(node)
        else:
            self._generate_cameligo_contract(node)
    
    def _generate_jsligo_contract(self, node: LIGOContractDecl):
        """Generate JsLIGO contract."""
        # Storage type
        if node.storage_type:
            self._write_line(f"type storage = ")
            self._visit(node.storage_type)
            self._write_line(";")
            self._write_line()
        
        # Parameter type (for entrypoints)
        if node.entrypoints:
            self._write_line("type parameter =")
            self._indent()
            for i, entry in enumerate(node.entrypoints):
                if i > 0:
                    self._write_line(" | ")
                else:
                    self._write_line("  ")
                
                self._write(f'["{ entry.name }", ')
                if entry.param_type:
                    self._visit(entry.param_type)
                else:
                    self._write("unit")
                self._write("]")
            self._dedent()
            self._write_line(";")
            self._write_line()
        
        # Main function
        self._write_line("const main = ([parameter, storage]: [parameter, storage]): [list<operation>, storage] => {")
        self._indent()
        
        if node.entrypoints:
            self._write_line("return match(parameter) {")
            self._indent()
            
            for entry in node.entrypoints:
                self._write_line(f'when({entry.name}(p)): {entry.name}(p, storage),')
            
            self._dedent()
            self._write_line("};")
        else:
            self._write_line("return [list([]) as list<operation>, storage];")
        
        self._dedent()
        self._write_line("};")
    
    def _generate_cameligo_contract(self, node: LIGOContractDecl):
        """Generate CameLIGO contract."""
        # Storage type
        if node.storage_type:
            self._write_line("type storage = ")
            self._visit(node.storage_type)
            self._write_line()
        
        # Parameter type
        if node.entrypoints:
            self._write_line("type action =")
            self._indent()
            for i, entry in enumerate(node.entrypoints):
                if i > 0:
                    self._write_line("| ")
                else:
                    self._write_line("  ")
                
                self._write(entry.name.capitalize())
                if entry.param_type:
                    self._write(" of ")
                    self._visit(entry.param_type)
            self._dedent()
            self._write_line()
        
        # Main function
        self._write_line("let main (action, storage : action * storage) : operation list * storage =")
        self._indent()
        
        if node.entrypoints:
            self._write_line("match action with")
            self._indent()
            
            for entry in node.entrypoints:
                self._write_line(f"{entry.name.capitalize()} p -> {entry.name} (p, storage)")
            
            self._dedent()
        else:
            self._write_line("([] : operation list), storage")
        
        self._dedent()
    
    # Types
    def visit_LIGOPrimitiveType(self, node: LIGOPrimitiveType):
        """Generate code for primitive type."""
        self._write(node.name)
    
    def visit_LIGORecordType(self, node: LIGORecordType):
        """Generate code for record type."""
        if self.syntax_style == LIGOSyntax.JSLIGO:
            self._write("{")
            for i, field in enumerate(node.fields):
                if i > 0:
                    self._write(", ")
                self._write(f"{field.name}: ")
                self._visit(field.type_annotation)
            self._write("}")
        else:
            self._write("{")
            for i, field in enumerate(node.fields):
                if i > 0:
                    self._write("; ")
                self._write(f"{field.name} : ")
                self._visit(field.type_annotation)
            self._write("}")
    
    def visit_LIGOVariantType(self, node: LIGOVariantType):
        """Generate code for variant type."""
        for i, variant in enumerate(node.variants):
            if i > 0:
                self._write(" | ")
            self._write(variant.name)
            if variant.type_annotation:
                if self.syntax_style == LIGOSyntax.JSLIGO:
                    self._write("(")
                    self._visit(variant.type_annotation)
                    self._write(")")
                else:
                    self._write(" of ")
                    self._visit(variant.type_annotation)
    
    def visit_LIGOListType(self, node: LIGOListType):
        """Generate code for list type."""
        if self.syntax_style == LIGOSyntax.JSLIGO:
            self._write("list<")
            self._visit(node.element_type)
            self._write(">")
        else:
            self._visit(node.element_type)
            self._write(" list")
    
    def visit_LIGOMapType(self, node: LIGOMapType):
        """Generate code for map type."""
        if self.syntax_style == LIGOSyntax.JSLIGO:
            self._write("map<")
            self._visit(node.key_type)
            self._write(", ")
            self._visit(node.value_type)
            self._write(">")
        else:
            self._write("(")
            self._visit(node.key_type)
            self._write(", ")
            self._visit(node.value_type)
            self._write(") map")
    
    def visit_LIGOOptionType(self, node: LIGOOptionType):
        """Generate code for option type."""
        if self.syntax_style == LIGOSyntax.JSLIGO:
            self._write("option<")
            self._visit(node.inner_type)
            self._write(">")
        else:
            self._visit(node.inner_type)
            self._write(" option")
    
    def visit_LIGOTupleType(self, node: LIGOTupleType):
        """Generate code for tuple type."""
        if self.syntax_style == LIGOSyntax.JSLIGO:
            self._write("[")
            for i, elem_type in enumerate(node.element_types):
                if i > 0:
                    self._write(", ")
                self._visit(elem_type)
            self._write("]")
        else:
            for i, elem_type in enumerate(node.element_types):
                if i > 0:
                    self._write(" * ")
                self._visit(elem_type)
    
    def visit_LIGOFunctionType(self, node: LIGOFunctionType):
        """Generate code for function type."""
        if self.syntax_style == LIGOSyntax.JSLIGO:
            self._write("(")
            for i, param_type in enumerate(node.param_types):
                if i > 0:
                    self._write(", ")
                self._visit(param_type)
            self._write(") => ")
            self._visit(node.return_type)
        else:
            for i, param_type in enumerate(node.param_types):
                if i > 0:
                    self._write(" -> ")
                self._visit(param_type)
            self._write(" -> ")
            self._visit(node.return_type)
    
    # Expressions
    def visit_LIGOLiteral(self, node: LIGOLiteral):
        """Generate code for literal."""
        if isinstance(node.value, str):
            self._write(f'"{node.value}"')
        elif isinstance(node.value, bool):
            self._write("true" if node.value else "false")
        elif node.value is None:
            self._write("unit" if self.syntax_style == LIGOSyntax.CAMELIGO else "()")
        else:
            self._write(str(node.value))
    
    def visit_LIGOIdentifier(self, node: LIGOIdentifier):
        """Generate code for identifier."""
        self._write(node.name)
    
    def visit_LIGOBinaryOp(self, node: LIGOBinaryOp):
        """Generate code for binary operation."""
        self._write("(")
        self._visit(node.left)
        self._write(f" {node.operator} ")
        self._visit(node.right)
        self._write(")")
    
    def visit_LIGOUnaryOp(self, node: LIGOUnaryOp):
        """Generate code for unary operation."""
        self._write(f"{node.operator} ")
        self._visit(node.operand)
    
    def visit_LIGOFunctionCall(self, node: LIGOFunctionCall):
        """Generate code for function call."""
        self._visit(node.function)
        self._write("(")
        for i, arg in enumerate(node.arguments):
            if i > 0:
                self._write(", ")
            self._visit(arg)
        self._write(")")
    
    def visit_LIGOConditional(self, node: LIGOConditional):
        """Generate code for conditional expression."""
        if self.syntax_style == LIGOSyntax.JSLIGO:
            self._write("(")
            self._visit(node.condition)
            self._write(" ? ")
            self._visit(node.then_expr)
            if node.else_expr:
                self._write(" : ")
                self._visit(node.else_expr)
            else:
                self._write(" : unit")
            self._write(")")
        else:
            self._write("if ")
            self._visit(node.condition)
            self._write(" then ")
            self._visit(node.then_expr)
            if node.else_expr:
                self._write(" else ")
                self._visit(node.else_expr)
    
    def visit_LIGOLambda(self, node: LIGOLambda):
        """Generate code for lambda expression."""
        if self.syntax_style == LIGOSyntax.JSLIGO:
            self._write("(")
            for i, param in enumerate(node.parameters):
                if i > 0:
                    self._write(", ")
                self._write(param.name)
                if param.type_annotation:
                    self._write(": ")
                    self._visit(param.type_annotation)
            self._write(") => ")
            self._visit(node.body)
        else:
            self._write("fun ")
            for i, param in enumerate(node.parameters):
                if i > 0:
                    self._write(" ")
                self._write(param.name)
                if param.type_annotation:
                    self._write(" : ")
                    self._visit(param.type_annotation)
            self._write(" -> ")
            self._visit(node.body)
    
    def visit_LIGORecordAccess(self, node: LIGORecordAccess):
        """Generate code for record field access."""
        self._visit(node.record)
        self._write(f".{node.field}")
    
    def visit_LIGOListAccess(self, node: LIGOListAccess):
        """Generate code for list element access."""
        self._visit(node.list_expr)
        self._write("[")
        self._visit(node.index)
        self._write("]")
    
    def visit_LIGOMapAccess(self, node: LIGOMapAccess):
        """Generate code for map value access."""
        if self.syntax_style == LIGOSyntax.JSLIGO:
            self._write("Map.find_opt(")
            self._visit(node.key)
            self._write(", ")
            self._visit(node.map_expr)
            self._write(")")
        else:
            self._write("Map.find_opt ")
            self._visit(node.key)
            self._write(" ")
            self._visit(node.map_expr)
    
    def visit_LIGORecordUpdate(self, node: LIGORecordUpdate):
        """Generate code for record update."""
        if self.syntax_style == LIGOSyntax.JSLIGO:
            self._write("{...")
            self._visit(node.record)
            self._write(", ")
            for i, (field, value) in enumerate(node.updates.items()):
                if i > 0:
                    self._write(", ")
                self._write(f"{field}: ")
                self._visit(value)
            self._write("}")
        else:
            self._write("{")
            self._visit(node.record)
            self._write(" with ")
            for i, (field, value) in enumerate(node.updates.items()):
                if i > 0:
                    self._write("; ")
                self._write(f"{field} = ")
                self._visit(value)
            self._write("}")
    
    def visit_LIGOListLiteral(self, node: LIGOListLiteral):
        """Generate code for list literal."""
        if self.syntax_style == LIGOSyntax.JSLIGO:
            self._write("list([")
            for i, elem in enumerate(node.elements):
                if i > 0:
                    self._write(", ")
                self._visit(elem)
            self._write("])")
        else:
            self._write("[")
            for i, elem in enumerate(node.elements):
                if i > 0:
                    self._write("; ")
                self._visit(elem)
            self._write("]")
    
    def visit_LIGOMapLiteral(self, node: LIGOMapLiteral):
        """Generate code for map literal."""
        if self.syntax_style == LIGOSyntax.JSLIGO:
            self._write("Map.literal(list([")
            for i, (key, value) in enumerate(node.entries):
                if i > 0:
                    self._write(", ")
                self._write("[")
                self._visit(key)
                self._write(", ")
                self._visit(value)
                self._write("]")
            self._write("]))")
        else:
            self._write("Map.literal [")
            for i, (key, value) in enumerate(node.entries):
                if i > 0:
                    self._write("; ")
                self._write("(")
                self._visit(key)
                self._write(", ")
                self._visit(value)
                self._write(")")
            self._write("]")
    
    def visit_LIGORecordLiteral(self, node: LIGORecordLiteral):
        """Generate code for record literal."""
        self._write("{")
        for i, (field, value) in enumerate(node.fields.items()):
            if i > 0:
                self._write(", " if self.syntax_style == LIGOSyntax.JSLIGO else "; ")
            self._write(f"{field}")
            self._write(": " if self.syntax_style == LIGOSyntax.JSLIGO else " = ")
            self._visit(value)
        self._write("}")
    
    # Patterns
    def visit_LIGOWildcardPattern(self, node: LIGOWildcardPattern):
        """Generate code for wildcard pattern."""
        self._write("_")
    
    def visit_LIGOVariablePattern(self, node: LIGOVariablePattern):
        """Generate code for variable pattern."""
        self._write(node.name)
    
    def visit_LIGOConstructorPattern(self, node: LIGOConstructorPattern):
        """Generate code for constructor pattern."""
        self._write(node.constructor)
        if node.args:
            if self.syntax_style == LIGOSyntax.JSLIGO:
                self._write("(")
                for i, arg in enumerate(node.args):
                    if i > 0:
                        self._write(", ")
                    self._visit(arg)
                self._write(")")
            else:
                for arg in node.args:
                    self._write(" ")
                    self._visit(arg)
    
    # Statements
    def visit_LIGOReturnStatement(self, node: LIGOReturnStatement):
        """Generate code for return statement."""
        if self.syntax_style == LIGOSyntax.JSLIGO:
            self._write("return ")
            if node.value:
                self._visit(node.value)
            self._write(";")
        else:
            if node.value:
                self._visit(node.value)
    
    def visit_LIGOMatchStatement(self, node: LIGOMatchStatement):
        """Generate code for match statement."""
        if self.syntax_style == LIGOSyntax.JSLIGO:
            self._write("match(")
            self._visit(node.expr)
            self._write(") {")
            self._write_line()
            
            self._indent()
            for case in node.cases:
                self._write("when(")
                self._visit(case.pattern)
                self._write("): ")
                self._visit(case.body)
                self._write_line(",")
            self._dedent()
            
            self._write("}")
        else:
            self._write("match ")
            self._visit(node.expr)
            self._write(" with")
            self._write_line()
            
            self._indent()
            for case in node.cases:
                self._write("| ")
                self._visit(case.pattern)
                self._write(" -> ")
                self._visit(case.body)
                self._write_line()
            self._dedent()


def generate_ligo_code(ast_node: LIGONode, syntax_style: LIGOSyntax = LIGOSyntax.JSLIGO, 
                      indent_size: int = 2) -> str:
    """Generate LIGO code from an AST node."""
    generator = LIGOGenerator(syntax_style, indent_size)
    return generator.generate(ast_node)


def format_ligo_code(code: str, syntax_style: LIGOSyntax = LIGOSyntax.JSLIGO) -> str:
    """Format LIGO code with proper indentation and spacing."""
    lines = code.split('\n')
    formatted_lines = []
    indent_level = 0
    
    for line in lines:
        stripped = line.strip()
        
        if not stripped:
            formatted_lines.append('')
            continue
        
        # Decrease indent for closing braces
        if stripped.startswith('}') or stripped.startswith('end'):
            indent_level = max(0, indent_level - 1)
        
        # Add indented line
        formatted_lines.append('  ' * indent_level + stripped)
        
        # Increase indent for opening braces  
        if stripped.endswith('{') or stripped.endswith('begin'):
            indent_level += 1
        elif syntax_style == LIGOSyntax.CAMELIGO:
            if (stripped.startswith('match ') or 
                stripped.startswith('if ') or
                stripped.startswith('let ') and ' = ' in stripped):
                indent_level += 1
    
    return '\n'.join(formatted_lines) 