#!/usr/bin/env python3
"""
Haskell Code Generator

Generates clean, idiomatic Haskell code from Haskell AST nodes.
Handles proper formatting, indentation, and Haskell syntax conventions.
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass
from io import StringIO

from .haskell_ast import *


@dataclass
class HaskellCodeStyle:
    """Haskell code style configuration."""
    indent_size: int = 2
    line_length: int = 80
    use_tabs: bool = False
    space_after_comma: bool = True
    space_around_operators: bool = True
    align_guards: bool = True
    compact_lists: bool = False
    
    @property
    def indent_string(self) -> str:
        """Get indentation string."""
        if self.use_tabs:
            return '\t'
        return ' ' * self.indent_size


class HaskellCodeGenerator:
    """Generates Haskell source code from AST."""
    
    def __init__(self, style: Optional[HaskellCodeStyle] = None):
        self.style = style or HaskellCodeStyle()
        self.output = StringIO()
        self.indent_level = 0
        self.current_line = ""
    
    def generate(self, node: HsNode) -> str:
        """Generate code for AST node."""
        self.output = StringIO()
        self.indent_level = 0
        self.current_line = ""
        
        self.visit(node)
        return self.output.getvalue().strip()
    
    def visit(self, node: HsNode) -> str:
        """Visit AST node and generate code."""
        method_name = f"visit_{node.__class__.__name__.lower()}"
        method = getattr(self, method_name, self.visit_generic)
        return method(node)
    
    def visit_generic(self, node: HsNode) -> str:
        """Generic visit method."""
        return f"-- Unknown node: {type(node)}"
    
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
    
    def visit_hsmodule(self, node: HsModule) -> str:
        """Generate module."""
        if node.name:
            self.write(f"module {node.name}")
            if node.exports:
                self.write(" (")
                for i, export in enumerate(node.exports):
                    if i > 0:
                        self.write(", ")
                    self.write(export.name)
                self.write(")")
            self.write_line(" where")
            self.write_line()
        
        # Imports
        for imp in node.imports:
            self.visit_hsimport(imp)
            self.write_line()
        
        if node.imports:
            self.write_line()
        
        # Declarations
        for i, decl in enumerate(node.declarations):
            if i > 0:
                self.write_line()
            self.visit(decl)
        
        return self.output.getvalue()
    
    def visit_hsimport(self, node: HsImport) -> str:
        """Generate import."""
        self.write("import")
        if node.qualified:
            self.write(" qualified")
        self.write(f" {node.module_name}")
        if node.alias:
            self.write(f" as {node.alias}")
        if node.import_list:
            self.write(" (")
            for i, item in enumerate(node.import_list):
                if i > 0:
                    self.write(", ")
                self.write(item)
            self.write(")")
        if node.hiding:
            self.write(" hiding")
        self.write_line()
        return ""
    
    def visit_hsfunctiondeclaration(self, node: HsFunctionDeclaration) -> str:
        """Generate function declaration."""
        for i, clause in enumerate(node.clauses):
            if i > 0:
                self.write_line()
            
            self.write(node.name)
            
            # Patterns
            for pattern in clause.patterns:
                self.write(" ")
                self.visit_pattern(pattern)
            
            # Guards or direct definition
            if len(clause.guards) == 1 and isinstance(clause.guards[0].condition, HsLiteral):
                # Simple definition
                self.write(" = ")
                self.visit(clause.guards[0].expression)
            else:
                # Guarded definition
                self.write_line()
                self.indent()
                for guard in clause.guards:
                    self.write("| ")
                    self.visit(guard.condition)
                    self.write(" = ")
                    self.visit(guard.expression)
                    self.write_line()
                self.dedent()
            
            if not clause.guards or len(clause.guards) == 1:
                self.write_line()
        
        return ""
    
    def visit_hstypesignature(self, node: HsTypeSignature) -> str:
        """Generate type signature."""
        self.write(", ".join(node.names))
        self.write(" :: ")
        self.visit_type(node.type_expr)
        self.write_line()
        return ""
    
    def visit_hsdatadeclaration(self, node: HsDataDeclaration) -> str:
        """Generate data declaration."""
        self.write("data ")
        self.write(node.name)
        
        # Type parameters
        for param in node.parameters:
            self.write(f" {param}")
        
        if node.constructors:
            self.write_line(" =")
            self.indent()
            
            for i, constructor in enumerate(node.constructors):
                if i > 0:
                    self.write_line("| ", end="")
                else:
                    self.write("  ")
                
                self.visit_dataconstructor(constructor)
                if i < len(node.constructors) - 1:
                    self.write_line()
            
            self.dedent()
        
        # Deriving clause
        if node.deriving:
            self.write_line()
            self.write("  deriving (")
            for i, derived in enumerate(node.deriving):
                if i > 0:
                    self.write(", ")
                self.write(derived)
            self.write(")")
        
        self.write_line()
        return ""
    
    def visit_dataconstructor(self, constructor: HsDataConstructor) -> str:
        """Generate data constructor."""
        self.write(constructor.name)
        
        if constructor.field_names:
            # Record syntax
            self.write(" {")
            for i, (field_name, field_type) in enumerate(zip(constructor.field_names, constructor.fields)):
                if i > 0:
                    self.write(", ")
                self.write(f" {field_name} :: ")
                self.visit_type(field_type)
            self.write(" }")
        else:
            # Regular constructor
            for field_type in constructor.fields:
                self.write(" ")
                self.visit_type(field_type)
        
        return ""
    
    def visit_hstypedeclaration(self, node: HsTypeDeclaration) -> str:
        """Generate type declaration."""
        self.write("type ")
        self.write(node.name)
        
        for param in node.parameters:
            self.write(f" {param}")
        
        self.write(" = ")
        self.visit_type(node.body)
        self.write_line()
        return ""
    
    def visit_hsclassdeclaration(self, node: HsClassDeclaration) -> str:
        """Generate class declaration."""
        self.write("class ")
        
        if node.constraints:
            self.write("(")
            for i, constraint in enumerate(node.constraints):
                if i > 0:
                    self.write(", ")
                self.visit_constraint(constraint)
            self.write(") => ")
        
        self.write(f"{node.name} {node.parameter}")
        self.write_line(" where")
        
        if node.methods:
            self.indent()
            for method in node.methods:
                self.visit_methodsignature(method)
            self.dedent()
        
        return ""
    
    def visit_hsinstancedeclaration(self, node: HsInstanceDeclaration) -> str:
        """Generate instance declaration."""
        self.write("instance ")
        
        if node.constraints:
            self.write("(")
            for i, constraint in enumerate(node.constraints):
                if i > 0:
                    self.write(", ")
                self.visit_constraint(constraint)
            self.write(") => ")
        
        self.write(f"{node.class_name} ")
        self.visit_type(node.instance_type)
        self.write_line(" where")
        
        if node.methods:
            self.indent()
            for method in node.methods:
                self.visit_binding(method)
            self.dedent()
        
        return ""
    
    def visit_hsliteral(self, node: HsLiteral) -> str:
        """Generate literal."""
        if node.literal_type == "string":
            self.write(f'"{node.value}"')
        elif node.literal_type == "char":
            self.write(f"'{node.value}'")
        elif node.literal_type == "boolean":
            self.write("True" if node.value else "False")
        else:
            self.write(str(node.value))
        return ""
    
    def visit_hsvariable(self, node: HsVariable) -> str:
        """Generate variable."""
        if node.qualified:
            self.write(f"{node.qualified}.{node.name}")
        else:
            self.write(node.name)
        return ""
    
    def visit_hsconstructor(self, node: HsConstructor) -> str:
        """Generate constructor."""
        if node.qualified:
            self.write(f"{node.qualified}.{node.name}")
        else:
            self.write(node.name)
        return ""
    
    def visit_hsapplication(self, node: HsApplication) -> str:
        """Generate function application."""
        self.visit(node.function)
        for arg in node.arguments:
            self.write(" ")
            if self.needs_parens(arg):
                self.write("(")
                self.visit(arg)
                self.write(")")
            else:
                self.visit(arg)
        return ""
    
    def visit_hslambda(self, node: HsLambda) -> str:
        """Generate lambda expression."""
        self.write("\\")
        for i, param in enumerate(node.parameters):
            if i > 0:
                self.write(" ")
            self.visit_pattern(param)
        self.write(" -> ")
        self.visit(node.body)
        return ""
    
    def visit_hsif(self, node: HsIf) -> str:
        """Generate if expression."""
        self.write("if ")
        self.visit(node.condition)
        self.write(" then ")
        self.visit(node.then_expr)
        self.write(" else ")
        self.visit(node.else_expr)
        return ""
    
    def visit_hscase(self, node: HsCase) -> str:
        """Generate case expression."""
        self.write("case ")
        self.visit(node.expression)
        self.write_line(" of")
        
        self.indent()
        for alt in node.alternatives:
            self.visit_alternative(alt)
        self.dedent()
        return ""
    
    def visit_alternative(self, alt: HsAlternative) -> str:
        """Generate case alternative."""
        self.visit_pattern(alt.pattern)
        
        if len(alt.guards) == 1 and isinstance(alt.guards[0].condition, HsLiteral):
            self.write(" -> ")
            self.visit(alt.guards[0].expression)
        else:
            self.write_line()
            self.indent()
            for guard in alt.guards:
                self.write("| ")
                self.visit(guard.condition)
                self.write(" -> ")
                self.visit(guard.expression)
                self.write_line()
            self.dedent()
        
        self.write_line()
        return ""
    
    def visit_hslist(self, node: HsList) -> str:
        """Generate list expression."""
        self.write("[")
        for i, elem in enumerate(node.elements):
            if i > 0:
                self.write(", ")
            self.visit(elem)
        self.write("]")
        return ""
    
    def visit_hstuple(self, node: HsTuple) -> str:
        """Generate tuple expression."""
        self.write("(")
        for i, elem in enumerate(node.elements):
            if i > 0:
                self.write(", ")
            self.visit(elem)
        self.write(")")
        return ""
    
    def visit_pattern(self, pattern: HsPattern) -> str:
        """Generate pattern."""
        if isinstance(pattern, HsWildcardPattern):
            self.write("_")
        elif isinstance(pattern, HsVariablePattern):
            self.write(pattern.name)
        elif isinstance(pattern, HsConstructorPattern):
            self.write(pattern.constructor)
            for p in pattern.patterns:
                self.write(" ")
                if self.pattern_needs_parens(p):
                    self.write("(")
                    self.visit_pattern(p)
                    self.write(")")
                else:
                    self.visit_pattern(p)
        elif isinstance(pattern, HsLiteralPattern):
            self.visit(pattern.literal)
        elif isinstance(pattern, HsListPattern):
            self.write("[")
            for i, p in enumerate(pattern.patterns):
                if i > 0:
                    self.write(", ")
                self.visit_pattern(p)
            self.write("]")
        elif isinstance(pattern, HsTuplePattern):
            self.write("(")
            for i, p in enumerate(pattern.patterns):
                if i > 0:
                    self.write(", ")
                self.visit_pattern(p)
            self.write(")")
        elif isinstance(pattern, HsAsPattern):
            self.write(f"{pattern.variable}@")
            self.visit_pattern(pattern.pattern)
        return ""
    
    def visit_type(self, type_expr: HsType) -> str:
        """Generate type expression."""
        if isinstance(type_expr, HsTypeVariable):
            self.write(type_expr.name)
        elif isinstance(type_expr, HsTypeConstructor):
            self.write(type_expr.name)
        elif isinstance(type_expr, HsFunctionType):
            if self.type_needs_parens(type_expr.from_type):
                self.write("(")
                self.visit_type(type_expr.from_type)
                self.write(")")
            else:
                self.visit_type(type_expr.from_type)
            self.write(" -> ")
            self.visit_type(type_expr.to_type)
        elif isinstance(type_expr, HsListType):
            self.write("[")
            self.visit_type(type_expr.element_type)
            self.write("]")
        elif isinstance(type_expr, HsTupleType):
            self.write("(")
            for i, t in enumerate(type_expr.types):
                if i > 0:
                    self.write(", ")
                self.visit_type(t)
            self.write(")")
        elif isinstance(type_expr, HsTypeApplication):
            self.visit_type(type_expr.constructor)
            for arg in type_expr.arguments:
                self.write(" ")
                if self.type_needs_parens(arg):
                    self.write("(")
                    self.visit_type(arg)
                    self.write(")")
                else:
                    self.visit_type(arg)
        elif isinstance(type_expr, HsForallType):
            self.write("forall ")
            self.write(" ".join(type_expr.variables))
            self.write(". ")
            if type_expr.constraints:
                self.write("(")
                for i, constraint in enumerate(type_expr.constraints):
                    if i > 0:
                        self.write(", ")
                    self.visit_constraint(constraint)
                self.write(") => ")
            self.visit_type(type_expr.body_type)
        return ""
    
    def visit_constraint(self, constraint: HsConstraint) -> str:
        """Generate type constraint."""
        self.write(f"{constraint.class_name} ")
        self.visit_type(constraint.type_expr)
        return ""
    
    def visit_methodsignature(self, method: HsMethodSignature) -> str:
        """Generate method signature."""
        self.write(f"{method.name} :: ")
        self.visit_type(method.type_expr)
        self.write_line()
        return ""
    
    def visit_binding(self, binding: HsBinding) -> str:
        """Generate binding."""
        self.visit_pattern(binding.pattern)
        self.write(" = ")
        self.visit(binding.expression)
        self.write_line()
        return ""
    
    def needs_parens(self, expr: HsExpression) -> bool:
        """Check if expression needs parentheses."""
        return isinstance(expr, (HsApplication, HsLambda, HsIf, HsCase))
    
    def pattern_needs_parens(self, pattern: HsPattern) -> bool:
        """Check if pattern needs parentheses."""
        return isinstance(pattern, (HsConstructorPattern, HsAsPattern))
    
    def type_needs_parens(self, type_expr: HsType) -> bool:
        """Check if type needs parentheses."""
        return isinstance(type_expr, (HsFunctionType, HsTypeApplication))


def generate_haskell(node: HsNode, style: Optional[HaskellCodeStyle] = None) -> str:
    """Generate Haskell code from AST node."""
    generator = HaskellCodeGenerator(style)
    return generator.generate(node)


# Export all components
__all__ = [
    "HaskellCodeStyle",
    "HaskellCodeGenerator",
    "generate_haskell"
] 