#!/usr/bin/env python3
"""
Scala Code Generator

Generates Scala code from Scala AST nodes with support for multiple code styles.

Author: Sybertnetics AI Solutions
License: MIT
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass
from enum import Enum, auto
import logging

from .scala_ast import *


class ScalaCodeStyle(Enum):
    """Scala code formatting styles."""
    STANDARD = "standard"
    TWITTER = "twitter"
    AKKA = "akka"
    DATABRICKS = "databricks"
    SCALAFMT = "scalafmt"
    COMPACT = "compact"


@dataclass
class ScalaFormattingOptions:
    """Scala code formatting options."""
    indent_size: int = 2
    max_line_length: int = 120
    use_tabs: bool = False
    space_before_brace: bool = True
    space_after_comma: bool = True
    space_around_operators: bool = True
    trailing_comma: bool = True
    
    # Scala-specific
    align_parameters: bool = True
    align_arrows: bool = True
    new_line_before_curly_lambda: bool = False
    spaces_in_imports: bool = True
    rewrite_traits: bool = True
    prefer_curry_def: bool = False
    spaces_around_at_in_pattern: bool = False
    blank_line_before_docstring: bool = False
    docstring_style: str = "SpaceAsterisk"  # Asterisk, SpaceAsterisk, AsteriskSpace
    rewrite_tokens: bool = True


class ScalaFormatter:
    """Scala code formatter with style presets."""
    
    @staticmethod
    def get_style_options(style: ScalaCodeStyle) -> ScalaFormattingOptions:
        """Get formatting options for a specific style."""
        if style == ScalaCodeStyle.STANDARD:
            return ScalaFormattingOptions(
                indent_size=2,
                max_line_length=120,
                space_before_brace=True,
                trailing_comma=True
            )
        elif style == ScalaCodeStyle.TWITTER:
            return ScalaFormattingOptions(
                indent_size=2,
                max_line_length=100,
                space_before_brace=True,
                trailing_comma=True,
                align_parameters=True,
                align_arrows=True
            )
        elif style == ScalaCodeStyle.AKKA:
            return ScalaFormattingOptions(
                indent_size=2,
                max_line_length=120,
                space_before_brace=True,
                trailing_comma=True,
                rewrite_traits=True,
                prefer_curry_def=True
            )
        elif style == ScalaCodeStyle.DATABRICKS:
            return ScalaFormattingOptions(
                indent_size=2,
                max_line_length=100,
                space_before_brace=True,
                trailing_comma=True,
                rewrite_tokens=True
            )
        elif style == ScalaCodeStyle.SCALAFMT:
            return ScalaFormattingOptions(
                indent_size=2,
                max_line_length=80,
                space_before_brace=True,
                trailing_comma=True,
                align_parameters=True,
                align_arrows=True,
                new_line_before_curly_lambda=True
            )
        elif style == ScalaCodeStyle.COMPACT:
            return ScalaFormattingOptions(
                indent_size=2,
                max_line_length=160,
                space_before_brace=False,
                trailing_comma=False
            )
        else:
            return ScalaFormattingOptions()


class ScalaCodeGenerator(ScalaVisitor):
    """Scala code generator that produces formatted Scala source code from AST."""
    
    def __init__(self, style: ScalaCodeStyle = ScalaCodeStyle.STANDARD):
        self.style = style
        self.options = ScalaFormatter.get_style_options(style)
        self.logger = logging.getLogger(__name__)
        
        # Output state
        self.output = []
        self.indent_level = 0
        self.current_line_length = 0
        self.needs_indent = True
    
    def generate(self, node: ScalaNode) -> str:
        """Generate Scala code from an AST node."""
        self.output = []
        self.indent_level = 0
        self.current_line_length = 0
        self.needs_indent = True
        
        try:
            node.accept(self)
            result = "".join(self.output)
            return self._post_process(result)
        except Exception as e:
            self.logger.error(f"Scala code generation failed: {e}")
            raise RuntimeError(f"Failed to generate Scala code: {e}")
    
    def _post_process(self, code: str) -> str:
        """Post-process generated code."""
        lines = code.split('\n')
        processed_lines = []
        
        for line in lines:
            processed_lines.append(line)
        
        result = '\n'.join(processed_lines)
        
        if result and not result.endswith('\n'):
            result += '\n'
        
        return result
    
    def _write(self, text: str):
        """Write text to output."""
        if self.needs_indent and text.strip():
            self._write_indent()
            self.needs_indent = False
        
        self.output.append(text)
        self.current_line_length += len(text)
    
    def _write_line(self, text: str = ""):
        """Write a line of text."""
        if text:
            self._write(text)
        self.output.append('\n')
        self.current_line_length = 0
        self.needs_indent = True
    
    def _write_indent(self):
        """Write current indentation."""
        if self.options.use_tabs:
            indent = '\t' * self.indent_level
        else:
            indent = ' ' * (self.indent_level * self.options.indent_size)
        
        self.output.append(indent)
        self.current_line_length += len(indent)
    
    def _increase_indent(self):
        """Increase indentation level."""
        self.indent_level += 1
    
    def _decrease_indent(self):
        """Decrease indentation level."""
        self.indent_level = max(0, self.indent_level - 1)
    
    def _write_space(self):
        """Write a space if needed."""
        if self.output and not self.output[-1].endswith(' '):
            self._write(' ')
    
    def _write_brace_open(self):
        """Write opening brace."""
        if self.options.space_before_brace:
            self._write_space()
        self._write('{')
        self._write_line()
        self._increase_indent()
    
    def _write_brace_close(self):
        """Write closing brace."""
        self._decrease_indent()
        self._write('}')
    
    def _write_separated_list(self, items: List[Any], separator: str = ", ", generate_func=None):
        """Write a separated list."""
        if not items:
            return
        
        if generate_func is None:
            generate_func = lambda item: item.accept(self)
        
        for i, item in enumerate(items):
            if i > 0:
                self._write(separator)
            generate_func(item)
    
    # Visitor methods
    def visit_scala_source_file(self, node: ScalaSourceFile):
        """Visit source file."""
        # Write package declaration
        if node.package_declaration:
            node.package_declaration.accept(self)
            self._write_line()
            self._write_line()
        
        # Write imports
        if node.imports:
            for import_decl in node.imports:
                import_decl.accept(self)
                self._write_line()
            self._write_line()
        
        # Write declarations
        for i, decl in enumerate(node.declarations):
            if i > 0:
                self._write_line()
            
            decl.accept(self)
            self._write_line()
    
    def visit_scala_package_declaration(self, node: ScalaPackageDeclaration):
        """Visit package declaration."""
        self._write('package ')
        self._write(node.name)
    
    def visit_scala_import_declaration(self, node: ScalaImportDeclaration):
        """Visit import declaration."""
        self._write('import ')
        self._write(node.path)
        
        if node.selectors:
            self._write('.{')
            self._write_separated_list(node.selectors, ', ', lambda x: self._write(x))
            self._write('}')
    
    def visit_scala_class_declaration(self, node: ScalaClassDeclaration):
        """Visit class declaration."""
        # Write modifiers
        if node.is_abstract:
            self._write('abstract ')
        if node.is_final:
            self._write('final ')
        if node.is_sealed:
            self._write('sealed ')
        if node.is_case:
            self._write('case ')
        
        self._write('class ')
        self._write(node.name)
        
        # Write type parameters
        if node.type_parameters:
            self._write('[')
            self._write_separated_list(node.type_parameters)
            self._write(']')
        
        # Write constructor parameters
        if node.constructor_parameters:
            self._write('(')
            self._write_separated_list(node.constructor_parameters)
            self._write(')')
        
        # Write extends clause
        if node.extends_clause:
            self._write(' extends ')
            node.extends_clause.accept(self)
        
        # Write with clauses
        for with_clause in node.with_clauses:
            self._write(' with ')
            with_clause.accept(self)
        
        # Write body
        if node.members:
            self._write_brace_open()
            
            for i, member in enumerate(node.members):
                if i > 0:
                    self._write_line()
                
                member.accept(self)
                self._write_line()
            
            self._write_brace_close()
    
    def visit_scala_trait_declaration(self, node: ScalaTraitDeclaration):
        """Visit trait declaration."""
        if node.is_sealed:
            self._write('sealed ')
        
        self._write('trait ')
        self._write(node.name)
        
        # Write type parameters
        if node.type_parameters:
            self._write('[')
            self._write_separated_list(node.type_parameters)
            self._write(']')
        
        # Write extends clause
        if node.extends_clause:
            self._write(' extends ')
            node.extends_clause.accept(self)
        
        # Write with clauses
        for with_clause in node.with_clauses:
            self._write(' with ')
            with_clause.accept(self)
        
        # Write body
        if node.members:
            self._write_brace_open()
            
            for i, member in enumerate(node.members):
                if i > 0:
                    self._write_line()
                
                member.accept(self)
                self._write_line()
            
            self._write_brace_close()
    
    def visit_scala_object_declaration(self, node: ScalaObjectDeclaration):
        """Visit object declaration."""
        if node.is_case:
            self._write('case ')
        
        self._write('object ')
        self._write(node.name)
        
        # Write extends clause
        if node.extends_clause:
            self._write(' extends ')
            node.extends_clause.accept(self)
        
        # Write with clauses
        for with_clause in node.with_clauses:
            self._write(' with ')
            with_clause.accept(self)
        
        # Write body
        if node.members:
            self._write_brace_open()
            
            for i, member in enumerate(node.members):
                if i > 0:
                    self._write_line()
                
                member.accept(self)
                self._write_line()
            
            self._write_brace_close()
    
    def visit_scala_enum_declaration(self, node: ScalaEnumDeclaration):
        """Visit enum declaration."""
        self._write('enum ')
        self._write(node.name)
        
        # Write type parameters
        if node.type_parameters:
            self._write('[')
            self._write_separated_list(node.type_parameters)
            self._write(']')
        
        # Write body
        self._write_brace_open()
        
        # Write cases
        for case in node.cases:
            self._write('case ')
            self._write(case.name)
            
            if case.parameters:
                self._write('(')
                self._write_separated_list(case.parameters)
                self._write(')')
            
            if case.extends_clauses:
                self._write(' extends ')
                self._write_separated_list(case.extends_clauses, ' with ')
            
            self._write_line()
        
        # Write members
        if node.cases and node.members:
            self._write_line()
        
        for i, member in enumerate(node.members):
            if i > 0:
                self._write_line()
            
            member.accept(self)
            self._write_line()
        
        self._write_brace_close()
    
    def visit_scala_function_declaration(self, node: ScalaFunctionDeclaration):
        """Visit function declaration."""
        if node.is_abstract:
            self._write('abstract ')
        if node.is_override:
            self._write('override ')
        if node.is_implicit:
            self._write('implicit ')
        if node.is_inline:
            self._write('inline ')
        
        self._write('def ')
        self._write(node.name)
        
        # Write type parameters
        if node.type_parameters:
            self._write('[')
            self._write_separated_list(node.type_parameters)
            self._write(']')
        
        # Write parameter lists
        for param_list in node.parameter_lists:
            self._write('(')
            self._write_separated_list(param_list)
            self._write(')')
        
        # Write return type
        if node.return_type:
            self._write(': ')
            node.return_type.accept(self)
        
        # Write body
        if node.body and not node.is_abstract:
            self._write(' = ')
            node.body.accept(self)
    
    def visit_scala_value_declaration(self, node: ScalaValueDeclaration):
        """Visit value declaration."""
        if node.is_lazy:
            self._write('lazy ')
        if node.is_implicit:
            self._write('implicit ')
        if node.is_override:
            self._write('override ')
        
        self._write('val ')
        self._write(node.name)
        
        if node.type_annotation:
            self._write(': ')
            node.type_annotation.accept(self)
        
        if node.value:
            self._write(' = ')
            node.value.accept(self)
    
    def visit_scala_variable_declaration(self, node: ScalaVariableDeclaration):
        """Visit variable declaration."""
        if node.is_override:
            self._write('override ')
        
        self._write('var ')
        self._write(node.name)
        
        if node.type_annotation:
            self._write(': ')
            node.type_annotation.accept(self)
        
        if node.value:
            self._write(' = ')
            node.value.accept(self)
    
    def visit_scala_type_alias_declaration(self, node: ScalaTypeAliasDeclaration):
        """Visit type alias declaration."""
        self._write('type ')
        self._write(node.name)
        
        if node.type_parameters:
            self._write('[')
            self._write_separated_list(node.type_parameters)
            self._write(']')
        
        if node.alias_type:
            self._write(' = ')
            node.alias_type.accept(self)
    
    def visit_scala_identifier(self, node: ScalaIdentifier):
        """Visit identifier."""
        self._write(node.name)
    
    def visit_scala_literal(self, node: ScalaLiteral):
        """Visit literal."""
        if node.literal_type == "string":
            self._write(f'"{node.value}"')
        elif node.literal_type == "char":
            self._write(f"'{node.value}'")
        elif node.literal_type == "bool":
            self._write(str(node.value).lower())
        elif node.literal_type == "null":
            self._write('null')
        elif node.literal_type == "unit":
            self._write('()')
        elif node.literal_type == "symbol":
            self._write(str(node.value))
        else:
            self._write(str(node.value))
    
    def visit_scala_block_expression(self, node: ScalaBlockExpression):
        """Visit block expression."""
        self._write_brace_open()
        
        for stmt in node.statements:
            stmt.accept(self)
            self._write_line()
        
        if node.result_expression:
            node.result_expression.accept(self)
            self._write_line()
        
        self._write_brace_close()
    
    def visit_scala_if_expression(self, node: ScalaIfExpression):
        """Visit if expression."""
        self._write('if (')
        if node.condition:
            node.condition.accept(self)
        self._write(') ')
        
        if node.then_expression:
            node.then_expression.accept(self)
        
        if node.else_expression:
            self._write(' else ')
            node.else_expression.accept(self)
    
    def visit_scala_match_expression(self, node: ScalaMatchExpression):
        """Visit match expression."""
        if node.scrutinee:
            node.scrutinee.accept(self)
        
        self._write(' match ')
        self._write_brace_open()
        
        for case in node.cases:
            self._write('case ')
            if case.pattern:
                case.pattern.accept(self)
            
            if case.guard:
                self._write(' if ')
                case.guard.accept(self)
            
            self._write(' => ')
            
            if case.body:
                case.body.accept(self)
            
            self._write_line()
        
        self._write_brace_close()
    
    def visit_scala_for_expression(self, node: ScalaForExpression):
        """Visit for expression."""
        self._write('for {')
        self._write_line()
        self._increase_indent()
        
        for generator in node.generators:
            if generator.pattern:
                generator.pattern.accept(self)
            self._write(' <- ')
            if generator.expression:
                generator.expression.accept(self)
            
            for guard in generator.guards:
                self._write(' if ')
                guard.accept(self)
            
            self._write_line()
        
        self._decrease_indent()
        self._write('} ')
        
        if node.is_yield:
            self._write('yield ')
        
        if node.yield_expression:
            node.yield_expression.accept(self)
    
    def visit_scala_while_expression(self, node: ScalaWhileExpression):
        """Visit while expression."""
        self._write('while (')
        if node.condition:
            node.condition.accept(self)
        self._write(') ')
        
        if node.body:
            node.body.accept(self)
    
    def visit_scala_function_call_expression(self, node: ScalaFunctionCallExpression):
        """Visit function call expression."""
        if node.function:
            node.function.accept(self)
        
        # Write type arguments
        if node.type_arguments:
            self._write('[')
            self._write_separated_list(node.type_arguments)
            self._write(']')
        
        # Write argument lists
        for arg_list in node.arguments:
            self._write('(')
            self._write_separated_list(arg_list)
            self._write(')')
    
    def visit_scala_method_call_expression(self, node: ScalaMethodCallExpression):
        """Visit method call expression."""
        if node.receiver:
            node.receiver.accept(self)
        
        self._write('.')
        self._write(node.method_name)
        
        # Write type arguments
        if node.type_arguments:
            self._write('[')
            self._write_separated_list(node.type_arguments)
            self._write(']')
        
        # Write argument lists
        for arg_list in node.arguments:
            self._write('(')
            self._write_separated_list(arg_list)
            self._write(')')
    
    def visit_scala_lambda_expression(self, node: ScalaLambdaExpression):
        """Visit lambda expression."""
        if node.parameters:
            if len(node.parameters) == 1:
                node.parameters[0].accept(self)
            else:
                self._write('(')
                self._write_separated_list(node.parameters)
                self._write(')')
        
        self._write(' => ')
        
        if node.body:
            node.body.accept(self)
    
    def visit_scala_binary_expression(self, node: ScalaBinaryExpression):
        """Visit binary expression."""
        if node.left:
            node.left.accept(self)
        
        if self.options.space_around_operators:
            self._write(' ')
        
        self._write(node.operator)
        
        if self.options.space_around_operators:
            self._write(' ')
        
        if node.right:
            node.right.accept(self)
    
    def visit_scala_unary_expression(self, node: ScalaUnaryExpression):
        """Visit unary expression."""
        if node.is_prefix:
            self._write(node.operator)
            if node.operand:
                node.operand.accept(self)
        else:
            if node.operand:
                node.operand.accept(self)
            self._write(node.operator)
    
    def visit_scala_assignment_expression(self, node: ScalaAssignmentExpression):
        """Visit assignment expression."""
        if node.target:
            node.target.accept(self)
        
        self._write(' = ')
        
        if node.value:
            node.value.accept(self)
    
    def visit_scala_new_expression(self, node: ScalaNewExpression):
        """Visit new expression."""
        self._write('new ')
        
        if node.class_type:
            node.class_type.accept(self)
        
        for arg_list in node.arguments:
            self._write('(')
            self._write_separated_list(arg_list)
            self._write(')')
    
    def visit_scala_tuple_expression(self, node: ScalaTupleExpression):
        """Visit tuple expression."""
        self._write('(')
        self._write_separated_list(node.elements)
        self._write(')')
    
    def visit_scala_list_expression(self, node: ScalaListExpression):
        """Visit list expression."""
        self._write('List(')
        self._write_separated_list(node.elements)
        self._write(')')
    
    def visit_scala_type_identifier(self, node: ScalaTypeIdentifier):
        """Visit type identifier."""
        self._write(node.name)
        
        if node.type_arguments:
            self._write('[')
            self._write_separated_list(node.type_arguments)
            self._write(']')
    
    def visit_scala_function_type(self, node: ScalaFunctionType):
        """Visit function type."""
        if len(node.parameter_types) == 1:
            node.parameter_types[0].accept(self)
        else:
            self._write('(')
            self._write_separated_list(node.parameter_types)
            self._write(')')
        
        self._write(' => ')
        
        if node.return_type:
            node.return_type.accept(self)
    
    def visit_scala_tuple_type(self, node: ScalaTupleType):
        """Visit tuple type."""
        self._write('(')
        self._write_separated_list(node.element_types)
        self._write(')')
    
    def visit_scala_type_parameter(self, node: ScalaTypeParameter):
        """Visit type parameter."""
        if node.variance:
            self._write(node.variance)
        
        self._write(node.name)
        
        if node.upper_bound:
            self._write(' <: ')
            node.upper_bound.accept(self)
        
        if node.lower_bound:
            self._write(' >: ')
            node.lower_bound.accept(self)
        
        for context_bound in node.context_bounds:
            self._write(' : ')
            context_bound.accept(self)
        
        for view_bound in node.view_bounds:
            self._write(' <% ')
            view_bound.accept(self)
    
    def visit_scala_parameter(self, node: ScalaParameter):
        """Visit parameter."""
        if node.is_implicit:
            self._write('implicit ')
        
        self._write(node.name)
        
        if node.parameter_type:
            self._write(': ')
            
            if node.is_by_name:
                self._write('=> ')
            
            node.parameter_type.accept(self)
            
            if node.is_varargs:
                self._write('*')
        
        if node.default_value:
            self._write(' = ')
            node.default_value.accept(self)
    
    def visit_scala_argument(self, node: ScalaArgument):
        """Visit argument."""
        if node.name:
            self._write(node.name)
            self._write(' = ')
        
        if node.value:
            node.value.accept(self)
    
    def visit_scala_wildcard_pattern(self, node: ScalaWildcardPattern):
        """Visit wildcard pattern."""
        self._write('_')
    
    def visit_scala_identifier_pattern(self, node: ScalaIdentifierPattern):
        """Visit identifier pattern."""
        self._write(node.name)
    
    def visit_scala_literal_pattern(self, node: ScalaLiteralPattern):
        """Visit literal pattern."""
        if node.literal:
            node.literal.accept(self)
    
    def visit_scala_constructor_pattern(self, node: ScalaConstructorPattern):
        """Visit constructor pattern."""
        if node.constructor:
            node.constructor.accept(self)
        
        if node.patterns:
            self._write('(')
            self._write_separated_list(node.patterns)
            self._write(')')
    
    def visit_scala_tuple_pattern(self, node: ScalaTuplePattern):
        """Visit tuple pattern."""
        self._write('(')
        self._write_separated_list(node.patterns)
        self._write(')')
    
    def visit_scala_typed_pattern(self, node: ScalaTypedPattern):
        """Visit typed pattern."""
        if node.pattern:
            node.pattern.accept(self)
        
        self._write(': ')
        
        if node.pattern_type:
            node.pattern_type.accept(self)


# Convenience functions
def generate_scala_code(ast: ScalaSourceFile, 
                       style: ScalaCodeStyle = ScalaCodeStyle.STANDARD) -> str:
    """Generate Scala code from AST with specified style."""
    generator = ScalaCodeGenerator(style)
    return generator.generate(ast)


def format_scala_code(code: str, 
                     style: ScalaCodeStyle = ScalaCodeStyle.STANDARD) -> str:
    """Format existing Scala code with specified style."""
    # This would require parsing and re-generating
    # For now, return the original code
    return code