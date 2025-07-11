#!/usr/bin/env python3
"""
C++ Code Generator

Generates clean, modern C++ source code from C++ AST nodes.
Supports C++11 through C++23 features with configurable formatting
and coding style options.
"""

from typing import List, Dict, Any, Optional
from io import StringIO
from dataclasses import dataclass

from .cpp_ast import *


@dataclass
class CppCodeStyle:
    """C++ code style configuration."""
    indent_size: int = 4
    use_spaces: bool = True
    brace_style: str = "allman"  # allman, k&r, stroustrup, gnu
    max_line_length: int = 100
    include_comments: bool = True
    namespace_indent: bool = False
    access_specifier_indent: int = 2
    template_space_before_angle: bool = False
    pointer_alignment: str = "left"  # left, right, middle
    include_header_guards: bool = True
    sort_includes: bool = True
    modern_cpp_features: bool = True  # Use C++11+ features


class CppCodeGenerator:
    """C++ code generator."""
    
    def __init__(self, style: Optional[CppCodeStyle] = None):
        self.style = style or CppCodeStyle()
        self.output = StringIO()
        self.current_indent = 0
        self.in_class = False
        self.in_namespace = False
        self.generated_includes = set()
        self.forward_declarations = set()
    
    def generate(self, node: CppNode) -> str:
        """Generate C++ code from AST node."""
        self.output = StringIO()
        self.current_indent = 0
        self.generated_includes.clear()
        self.forward_declarations.clear()
        
        self._visit_node(node)
        
        result = self.output.getvalue()
        self.output.close()
        return result
    
    def _visit_node(self, node: CppNode):
        """Visit a node and generate code."""
        if isinstance(node, CppTranslationUnit):
            self._visit_translation_unit(node)
        elif isinstance(node, CppIntegerLiteral):
            self._visit_integer_literal(node)
        elif isinstance(node, CppFloatingLiteral):
            self._visit_floating_literal(node)
        elif isinstance(node, CppStringLiteral):
            self._visit_string_literal(node)
        elif isinstance(node, CppCharacterLiteral):
            self._visit_character_literal(node)
        elif isinstance(node, CppBooleanLiteral):
            self._visit_boolean_literal(node)
        elif isinstance(node, CppNullptrLiteral):
            self._visit_nullptr_literal(node)
        elif isinstance(node, CppIdentifier):
            self._visit_identifier(node)
        elif isinstance(node, CppQualifiedName):
            self._visit_qualified_name(node)
        elif isinstance(node, CppBinaryOp):
            self._visit_binary_op(node)
        elif isinstance(node, CppUnaryOp):
            self._visit_unary_op(node)
        elif isinstance(node, CppConditionalOp):
            self._visit_conditional_op(node)
        elif isinstance(node, CppAssignment):
            self._visit_assignment(node)
        elif isinstance(node, CppCall):
            self._visit_call(node)
        elif isinstance(node, CppMemberAccess):
            self._visit_member_access(node)
        elif isinstance(node, CppArraySubscript):
            self._visit_array_subscript(node)
        elif isinstance(node, CppCast):
            self._visit_cast(node)
        elif isinstance(node, CppSizeofExpr):
            self._visit_sizeof(node)
        elif isinstance(node, CppNewExpr):
            self._visit_new_expr(node)
        elif isinstance(node, CppDeleteExpr):
            self._visit_delete_expr(node)
        elif isinstance(node, CppLambda):
            self._visit_lambda(node)
        elif isinstance(node, CppInitializerList):
            self._visit_initializer_list(node)
        elif isinstance(node, CppExpressionStmt):
            self._visit_expression_stmt(node)
        elif isinstance(node, CppCompoundStmt):
            self._visit_compound_stmt(node)
        elif isinstance(node, CppIfStmt):
            self._visit_if_stmt(node)
        elif isinstance(node, CppWhileStmt):
            self._visit_while_stmt(node)
        elif isinstance(node, CppForStmt):
            self._visit_for_stmt(node)
        elif isinstance(node, CppRangeForStmt):
            self._visit_range_for_stmt(node)
        elif isinstance(node, CppReturnStmt):
            self._visit_return_stmt(node)
        elif isinstance(node, CppBreakStmt):
            self._visit_break_stmt(node)
        elif isinstance(node, CppContinueStmt):
            self._visit_continue_stmt(node)
        elif isinstance(node, CppVariableDecl):
            self._visit_variable_decl(node)
        elif isinstance(node, CppFunctionDecl):
            self._visit_function_decl(node)
        elif isinstance(node, CppClassDecl):
            self._visit_class_decl(node)
        elif isinstance(node, CppNamespaceDecl):
            self._visit_namespace_decl(node)
        elif isinstance(node, CppTemplateDecl):
            self._visit_template_decl(node)
        elif isinstance(node, CppBuiltinType):
            self._visit_builtin_type(node)
        elif isinstance(node, CppPointerType):
            self._visit_pointer_type(node)
        elif isinstance(node, CppReferenceType):
            self._visit_reference_type(node)
        elif isinstance(node, CppArrayType):
            self._visit_array_type(node)
        elif isinstance(node, CppAutoType):
            self._visit_auto_type(node)
        elif isinstance(node, CppDecltypeType):
            self._visit_decltype_type(node)
        else:
            self._write("/* unknown node */")
    
    def _visit_translation_unit(self, node: CppTranslationUnit):
        """Visit translation unit."""
        # Generate standard includes if needed
        if self.style.modern_cpp_features:
            common_includes = [
                "#include <iostream>",
                "#include <string>",
                "#include <vector>",
                "#include <memory>",
                "#include <algorithm>",
                "#include <functional>"
            ]
            
            for include in common_includes:
                if include not in self.generated_includes:
                    self._write_line(include)
                    self.generated_includes.add(include)
            
            if self.generated_includes:
                self._write_line()
        
        # Generate declarations
        for i, decl in enumerate(node.declarations):
            if i > 0:
                self._write_line()
            self._visit_node(decl)
    
    def _visit_integer_literal(self, node: CppIntegerLiteral):
        """Visit integer literal."""
        value_str = str(node.value)
        if node.suffix:
            value_str += node.suffix
        self._write(value_str)
    
    def _visit_floating_literal(self, node: CppFloatingLiteral):
        """Visit floating literal."""
        value_str = str(node.value)
        if node.suffix:
            value_str += node.suffix
        self._write(value_str)
    
    def _visit_string_literal(self, node: CppStringLiteral):
        """Visit string literal."""
        value = node.value
        if node.prefix:
            value = node.prefix + value
        self._write(value)
    
    def _visit_character_literal(self, node: CppCharacterLiteral):
        """Visit character literal."""
        value = node.value
        if node.prefix:
            value = node.prefix + value
        self._write(value)
    
    def _visit_boolean_literal(self, node: CppBooleanLiteral):
        """Visit boolean literal."""
        self._write("true" if node.value else "false")
    
    def _visit_nullptr_literal(self, node: CppNullptrLiteral):
        """Visit nullptr literal."""
        self._write("nullptr")
    
    def _visit_identifier(self, node: CppIdentifier):
        """Visit identifier."""
        self._write(node.name)
    
    def _visit_qualified_name(self, node: CppQualifiedName):
        """Visit qualified name."""
        if node.scope:
            self._visit_node(node.scope)
            self._write("::")
        self._write(node.name)
    
    def _visit_binary_op(self, node: CppBinaryOp):
        """Visit binary operation."""
        needs_parens = self._needs_parentheses(node)
        
        if needs_parens:
            self._write("(")
        
        self._visit_node(node.left)
        self._write(f" {node.operator.value} ")
        self._visit_node(node.right)
        
        if needs_parens:
            self._write(")")
    
    def _visit_unary_op(self, node: CppUnaryOp):
        """Visit unary operation."""
        if node.is_postfix:
            self._visit_node(node.operand)
            self._write(node.operator.value.replace("post", ""))
        else:
            if node.operator in [CppOperator.PRE_INC, CppOperator.PRE_DEC]:
                self._write(node.operator.value.replace("pre", ""))
            else:
                self._write(node.operator.value)
            
            if node.operator == CppOperator.LOGICAL_NOT:
                self._write(" ")
            
            self._visit_node(node.operand)
    
    def _visit_conditional_op(self, node: CppConditionalOp):
        """Visit conditional operation."""
        self._visit_node(node.condition)
        self._write(" ? ")
        self._visit_node(node.true_expr)
        self._write(" : ")
        self._visit_node(node.false_expr)
    
    def _visit_assignment(self, node: CppAssignment):
        """Visit assignment."""
        self._visit_node(node.left)
        self._write(f" {node.operator.value} ")
        self._visit_node(node.right)
    
    def _visit_call(self, node: CppCall):
        """Visit function call."""
        self._visit_node(node.function)
        self._write("(")
        
        for i, arg in enumerate(node.arguments):
            if i > 0:
                self._write(", ")
            self._visit_node(arg)
        
        self._write(")")
    
    def _visit_member_access(self, node: CppMemberAccess):
        """Visit member access."""
        self._visit_node(node.object)
        self._write("->" if node.is_arrow else ".")
        self._write(node.member)
    
    def _visit_array_subscript(self, node: CppArraySubscript):
        """Visit array subscript."""
        self._visit_node(node.array)
        self._write("[")
        self._visit_node(node.index)
        self._write("]")
    
    def _visit_cast(self, node: CppCast):
        """Visit cast expression."""
        if node.cast_kind == "static":
            self._write("static_cast<")
            self._visit_node(node.target_type)
            self._write(">(")
            self._visit_node(node.operand)
            self._write(")")
        elif node.cast_kind == "dynamic":
            self._write("dynamic_cast<")
            self._visit_node(node.target_type)
            self._write(">(")
            self._visit_node(node.operand)
            self._write(")")
        elif node.cast_kind == "const":
            self._write("const_cast<")
            self._visit_node(node.target_type)
            self._write(">(")
            self._visit_node(node.operand)
            self._write(")")
        elif node.cast_kind == "reinterpret":
            self._write("reinterpret_cast<")
            self._visit_node(node.target_type)
            self._write(">(")
            self._visit_node(node.operand)
            self._write(")")
        else:
            # C-style cast
            self._write("(")
            self._visit_node(node.target_type)
            self._write(")")
            self._visit_node(node.operand)
    
    def _visit_sizeof(self, node: CppSizeofExpr):
        """Visit sizeof expression."""
        self._write("sizeof(")
        self._visit_node(node.operand)
        self._write(")")
    
    def _visit_new_expr(self, node: CppNewExpr):
        """Visit new expression."""
        self._write("new ")
        
        if node.is_array:
            self._visit_node(node.target_type)
            self._write("[")
            if node.array_size:
                self._visit_node(node.array_size)
            self._write("]")
        else:
            self._visit_node(node.target_type)
            
            if node.initializer:
                self._write("(")
                self._visit_node(node.initializer)
                self._write(")")
    
    def _visit_delete_expr(self, node: CppDeleteExpr):
        """Visit delete expression."""
        self._write("delete")
        if node.is_array:
            self._write("[]")
        self._write(" ")
        self._visit_node(node.operand)
    
    def _visit_lambda(self, node: CppLambda):
        """Visit lambda expression."""
        self._write("[")
        
        # Captures
        for i, capture in enumerate(node.captures):
            if i > 0:
                self._write(", ")
            self._visit_lambda_capture(capture)
        
        self._write("]")
        
        # Parameters
        if node.parameters and node.parameters.parameters:
            self._write("(")
            self._visit_parameter_list(node.parameters)
            self._write(")")
        
        # Mutable
        if node.is_mutable:
            self._write(" mutable")
        
        # Return type
        if node.return_type:
            self._write(" -> ")
            self._visit_node(node.return_type)
        
        # Body
        self._write(" ")
        self._visit_node(node.body)
    
    def _visit_lambda_capture(self, node: CppLambdaCapture):
        """Visit lambda capture."""
        if node.is_by_reference:
            self._write("&")
        
        if node.is_this:
            self._write("this")
        elif node.name:
            self._write(node.name)
            if node.init_expr:
                self._write(" = ")
                self._visit_node(node.init_expr)
    
    def _visit_initializer_list(self, node: CppInitializerList):
        """Visit initializer list."""
        self._write("{")
        
        for i, element in enumerate(node.elements):
            if i > 0:
                self._write(", ")
            self._visit_node(element)
        
        self._write("}")
    
    def _visit_expression_stmt(self, node: CppExpressionStmt):
        """Visit expression statement."""
        self._write_indent()
        if node.expression:
            self._visit_node(node.expression)
        self._write(";\n")
    
    def _visit_compound_stmt(self, node: CppCompoundStmt):
        """Visit compound statement."""
        if self.style.brace_style == "k&r":
            self._write(" {")
        else:
            self._write_line()
            self._write_indent()
            self._write("{")
        
        self._write_line()
        self._indent()
        
        for stmt in node.statements:
            self._visit_node(stmt)
        
        self._dedent()
        self._write_indent()
        self._write("}")
    
    def _visit_if_stmt(self, node: CppIfStmt):
        """Visit if statement."""
        self._write_indent()
        self._write("if (")
        self._visit_node(node.condition)
        self._write(")")
        
        if isinstance(node.then_stmt, CppCompoundStmt):
            self._visit_compound_stmt(node.then_stmt)
        else:
            self._write_line()
            self._indent()
            self._visit_node(node.then_stmt)
            self._dedent()
        
        if node.else_stmt:
            if self.style.brace_style == "k&r":
                self._write(" else")
            else:
                self._write_line()
                self._write_indent()
                self._write("else")
            
            if isinstance(node.else_stmt, CppIfStmt):
                self._write(" ")
                # Remove indent for else if
                current = self.current_indent
                self.current_indent = 0
                self._visit_node(node.else_stmt)
                self.current_indent = current
            elif isinstance(node.else_stmt, CppCompoundStmt):
                self._visit_compound_stmt(node.else_stmt)
            else:
                self._write_line()
                self._indent()
                self._visit_node(node.else_stmt)
                self._dedent()
        
        self._write_line()
    
    def _visit_while_stmt(self, node: CppWhileStmt):
        """Visit while statement."""
        self._write_indent()
        self._write("while (")
        self._visit_node(node.condition)
        self._write(")")
        
        if isinstance(node.body, CppCompoundStmt):
            self._visit_compound_stmt(node.body)
        else:
            self._write_line()
            self._indent()
            self._visit_node(node.body)
            self._dedent()
        
        self._write_line()
    
    def _visit_for_stmt(self, node: CppForStmt):
        """Visit for statement."""
        self._write_indent()
        self._write("for (")
        
        if node.init:
            # Remove trailing semicolon and newline from init
            init_output = StringIO()
            old_output = self.output
            self.output = init_output
            old_indent = self.current_indent
            self.current_indent = 0
            
            self._visit_node(node.init)
            
            self.current_indent = old_indent
            self.output = old_output
            
            init_str = init_output.getvalue().strip().rstrip(';').rstrip('\n')
            self._write(init_str)
        
        self._write("; ")
        
        if node.condition:
            self._visit_node(node.condition)
        
        self._write("; ")
        
        if node.increment:
            self._visit_node(node.increment)
        
        self._write(")")
        
        if isinstance(node.body, CppCompoundStmt):
            self._visit_compound_stmt(node.body)
        else:
            self._write_line()
            self._indent()
            self._visit_node(node.body)
            self._dedent()
        
        self._write_line()
    
    def _visit_range_for_stmt(self, node: CppRangeForStmt):
        """Visit range-based for statement."""
        self._write_indent()
        self._write("for (")
        self._visit_node(node.variable)
        self._write(" : ")
        self._visit_node(node.range)
        self._write(")")
        
        if isinstance(node.body, CppCompoundStmt):
            self._visit_compound_stmt(node.body)
        else:
            self._write_line()
            self._indent()
            self._visit_node(node.body)
            self._dedent()
        
        self._write_line()
    
    def _visit_return_stmt(self, node: CppReturnStmt):
        """Visit return statement."""
        self._write_indent()
        self._write("return")
        
        if node.value:
            self._write(" ")
            self._visit_node(node.value)
        
        self._write(";\n")
    
    def _visit_break_stmt(self, node: CppBreakStmt):
        """Visit break statement."""
        self._write_indent()
        self._write("break;\n")
    
    def _visit_continue_stmt(self, node: CppContinueStmt):
        """Visit continue statement."""
        self._write_indent()
        self._write("continue;\n")
    
    def _visit_variable_decl(self, node: CppVariableDecl):
        """Visit variable declaration."""
        self._write_indent()
        
        # Storage class
        if node.storage_class:
            self._write(f"{node.storage_class.value} ")
        
        # Constexpr/consteval/constinit
        if node.is_constexpr:
            self._write("constexpr ")
        elif node.is_consteval:
            self._write("consteval ")
        elif node.is_constinit:
            self._write("constinit ")
        
        # Type
        self._visit_node(node.var_type)
        self._write(" ")
        
        # Name
        self._write(node.name)
        
        # Initializer
        if node.initializer:
            self._write(" = ")
            self._visit_node(node.initializer)
        
        self._write(";\n")
    
    def _visit_function_decl(self, node: CppFunctionDecl):
        """Visit function declaration."""
        self._write_indent()
        
        # Storage class and specifiers
        if node.storage_class:
            self._write(f"{node.storage_class.value} ")
        
        if node.is_inline:
            self._write("inline ")
        
        if node.is_virtual:
            self._write("virtual ")
        
        if node.is_constexpr:
            self._write("constexpr ")
        elif node.is_consteval:
            self._write("consteval ")
        
        if node.is_explicit:
            self._write("explicit ")
        
        # Return type (unless constructor/destructor)
        if not (node.name.startswith("~") or node.return_type.type == CppNodeType.BUILTIN_TYPE and node.return_type.name == "void"):
            self._visit_node(node.return_type)
            self._write(" ")
        
        # Function name
        self._write(node.name)
        
        # Parameters
        self._write("(")
        self._visit_parameter_list(node.parameters)
        self._write(")")
        
        # Trailing return type (C++11)
        if node.trailing_return_type:
            self._write(" -> ")
            self._visit_node(node.trailing_return_type)
        
        # Override/final
        if node.is_override:
            self._write(" override")
        
        if node.is_final:
            self._write(" final")
        
        # Pure virtual
        if node.is_pure_virtual:
            self._write(" = 0")
        
        # Body or semicolon
        if node.body:
            if isinstance(node.body, CppCompoundStmt):
                self._visit_compound_stmt(node.body)
            else:
                self._write_line()
                self._indent()
                self._visit_node(node.body)
                self._dedent()
        else:
            self._write(";")
        
        self._write_line()
    
    def _visit_parameter_list(self, node: CppParameterList):
        """Visit parameter list."""
        for i, param in enumerate(node.parameters):
            if i > 0:
                self._write(", ")
            self._visit_parameter(param)
        
        if node.is_variadic:
            if node.parameters:
                self._write(", ")
            self._write("...")
    
    def _visit_parameter(self, node: CppParameter):
        """Visit parameter."""
        self._visit_node(node.param_type)
        
        if node.name:
            self._write(" ")
            self._write(node.name)
        
        if node.default_value:
            self._write(" = ")
            self._visit_node(node.default_value)
    
    def _visit_class_decl(self, node: CppClassDecl):
        """Visit class declaration."""
        self._write_indent()
        
        if node.is_struct:
            self._write("struct")
        elif node.is_union:
            self._write("union")
        else:
            self._write("class")
        
        self._write(f" {node.name}")
        
        # Base classes
        if node.base_classes:
            self._write(" : ")
            for i, base in enumerate(node.base_classes):
                if i > 0:
                    self._write(", ")
                self._visit_base_specifier(base)
        
        if self.style.brace_style == "k&r":
            self._write(" {")
        else:
            self._write_line()
            self._write_indent()
            self._write("{")
        
        self._write_line()
        
        old_in_class = self.in_class
        self.in_class = True
        
        current_access = CppAccessSpecifier.PRIVATE if not node.is_struct else CppAccessSpecifier.PUBLIC
        
        for member in node.members:
            # Add access specifiers as needed
            if hasattr(member, 'access_specifier'):
                if member.access_specifier != current_access:
                    current_access = member.access_specifier
                    self._write_access_specifier(current_access)
            
            self._visit_node(member)
        
        self.in_class = old_in_class
        
        self._write_indent()
        self._write("};\n")
    
    def _visit_base_specifier(self, node: CppBaseSpecifier):
        """Visit base class specifier."""
        if node.access != CppAccessSpecifier.PUBLIC:
            self._write(f"{node.access.value} ")
        
        if node.is_virtual:
            self._write("virtual ")
        
        self._visit_node(node.base_type)
    
    def _visit_namespace_decl(self, node: CppNamespaceDecl):
        """Visit namespace declaration."""
        self._write_indent()
        self._write("namespace")
        
        if node.name:
            self._write(f" {node.name}")
        
        if self.style.brace_style == "k&r":
            self._write(" {")
        else:
            self._write_line()
            self._write_indent()
            self._write("{")
        
        self._write_line()
        
        old_in_namespace = self.in_namespace
        self.in_namespace = True
        
        if not self.style.namespace_indent:
            # Don't indent namespace contents
            for decl in node.declarations:
                self._visit_node(decl)
        else:
            self._indent()
            for decl in node.declarations:
                self._visit_node(decl)
            self._dedent()
        
        self.in_namespace = old_in_namespace
        
        self._write_indent()
        self._write("}")
        
        if node.name:
            self._write(f"  // namespace {node.name}")
        
        self._write_line()
    
    def _visit_template_decl(self, node: CppTemplateDecl):
        """Visit template declaration."""
        self._write_indent()
        self._write("template")
        
        if self.style.template_space_before_angle:
            self._write(" ")
        
        self._write("<")
        self._visit_template_parameter_list(node.template_params)
        self._write(">")
        
        self._write_line()
        self._visit_node(node.declaration)
    
    def _visit_template_parameter_list(self, node: CppTemplateParameterList):
        """Visit template parameter list."""
        for i, param in enumerate(node.parameters):
            if i > 0:
                self._write(", ")
            self._visit_template_parameter(param)
    
    def _visit_template_parameter(self, node: CppTemplateParameter):
        """Visit template parameter with comprehensive handling."""
        try:
            if hasattr(node, 'kind'):
                if node.kind == "type":
                    # Type parameter: typename T
                    self._write("typename")
                    
                    # Handle C++20 concepts/constraints
                    if hasattr(node, 'constraints') and node.constraints:
                        self._write(" ")
                        self._visit_constraint_list(node.constraints)
                    
                    if hasattr(node, 'name') and node.name:
                        self._write(f" {node.name}")
                    
                    # Handle default type
                    if hasattr(node, 'default_value') and node.default_value:
                        self._write(" = ")
                        self._visit_node(node.default_value)
                
                elif node.kind == "non_type":
                    # Non-type parameter: int N
                    if hasattr(node, 'type') and node.type:
                        self._visit_node(node.type)
                    else:
                        self._write("auto")
                    
                    if hasattr(node, 'name') and node.name:
                        self._write(f" {node.name}")
                    
                    # Handle default value
                    if hasattr(node, 'default_value') and node.default_value:
                        self._write(" = ")
                        self._visit_node(node.default_value)
                
                elif node.kind == "template":
                    # Template template parameter: template<typename> class Container
                    self._write("template")
                    
                    # Handle template parameters of the template parameter
                    if hasattr(node, 'template_params') and node.template_params:
                        self._write("<")
                        self._visit_template_parameter_list(node.template_params)
                        self._write(">")
                    
                    self._write(" class")
                    
                    if hasattr(node, 'name') and node.name:
                        self._write(f" {node.name}")
                    
                    # Handle default template
                    if hasattr(node, 'default_value') and node.default_value:
                        self._write(" = ")
                        self._visit_node(node.default_value)
                
                elif node.kind == "concept":
                    # C++20 concept parameter: Concept T
                    if hasattr(node, 'concept_name') and node.concept_name:
                        self._write(node.concept_name)
                    else:
                        self._write("Concept")
                    
                    if hasattr(node, 'name') and node.name:
                        self._write(f" {node.name}")
                    
                    # Handle concept arguments
                    if hasattr(node, 'concept_args') and node.concept_args:
                        self._write("<")
                        for i, arg in enumerate(node.concept_args):
                            if i > 0:
                                self._write(", ")
                            self._visit_node(arg)
                        self._write(">")
                
                elif node.kind == "parameter_pack":
                    # Variadic template parameter: typename... Args
                    self._write("typename...")
                    
                    if hasattr(node, 'name') and node.name:
                        self._write(f" {node.name}")
                    
                    # Handle constraints for parameter packs
                    if hasattr(node, 'constraints') and node.constraints:
                        self._write(" ")
                        self._visit_constraint_list(node.constraints)
                
                elif node.kind == "non_type_pack":
                    # Non-type parameter pack: int... Values
                    if hasattr(node, 'type') and node.type:
                        self._visit_node(node.type)
                    else:
                        self._write("auto")
                    
                    self._write("...")
                    
                    if hasattr(node, 'name') and node.name:
                        self._write(f" {node.name}")
                
                else:
                    # Unknown parameter kind - fallback
                    self._write("auto")
                    if hasattr(node, 'name') and node.name:
                        self._write(f" {node.name}")
            else:
                # Fallback for nodes without kind attribute
                self._write("auto")
                if hasattr(node, 'name') and node.name:
                    self._write(f" {node.name}")
                    
        except Exception as e:
            self._log_error(f"Error visiting template parameter: {e}")
            # Fallback to basic output
            self._write("auto")
            if hasattr(node, 'name') and node.name:
                self._write(f" {node.name}")
    
    def _visit_constraint_list(self, constraints):
        """Visit C++20 concept constraints."""
        try:
            if not constraints:
                return
            
            # Handle single constraint
            if len(constraints) == 1:
                self._visit_constraint(constraints[0])
                return
            
            # Handle multiple constraints with logical operators
            for i, constraint in enumerate(constraints):
                if i > 0:
                    # Add logical operator between constraints
                    if hasattr(constraint, 'logical_op'):
                        if constraint.logical_op == "and":
                            self._write(" && ")
                        elif constraint.logical_op == "or":
                            self._write(" || ")
                        else:
                            self._write(" && ")
                    else:
                        self._write(" && ")
                
                self._visit_constraint(constraint)
                
        except Exception as e:
            self._log_error(f"Error visiting constraint list: {e}")
    
    def _visit_constraint(self, constraint):
        """Visit individual C++20 concept constraint."""
        try:
            if hasattr(constraint, 'kind'):
                if constraint.kind == "concept":
                    # Concept constraint: Concept<T>
                    if hasattr(constraint, 'concept_name'):
                        self._write(constraint.concept_name)
                    
                    if hasattr(constraint, 'arguments') and constraint.arguments:
                        self._write("<")
                        for i, arg in enumerate(constraint.arguments):
                            if i > 0:
                                self._write(", ")
                            self._visit_node(arg)
                        self._write(">")
                
                elif constraint.kind == "type":
                    # Type constraint: std::is_integral_v<T>
                    if hasattr(constraint, 'type'):
                        self._visit_node(constraint.type)
                
                elif constraint.kind == "expression":
                    # Expression constraint: requires { T::value }
                    self._write("requires { ")
                    if hasattr(constraint, 'expression'):
                        self._visit_node(constraint.expression)
                    self._write(" }")
                
                elif constraint.kind == "compound":
                    # Compound constraint: requires { typename T::type; }
                    self._write("requires { ")
                    if hasattr(constraint, 'requirements'):
                        for req in constraint.requirements:
                            self._visit_requirement(req)
                            self._write("; ")
                    self._write("}")
                
                else:
                    # Unknown constraint type
                    self._write("auto")
            else:
                # Fallback
                self._write("auto")
                
        except Exception as e:
            self._log_error(f"Error visiting constraint: {e}")
            self._write("auto")
    
    def _visit_requirement(self, requirement):
        """Visit C++20 requirement within a requires clause."""
        try:
            if hasattr(requirement, 'kind'):
                if requirement.kind == "type":
                    # Type requirement: typename T::type
                    self._write("typename ")
                    if hasattr(requirement, 'type'):
                        self._visit_node(requirement.type)
                
                elif requirement.kind == "simple":
                    # Simple requirement: T::value
                    if hasattr(requirement, 'expression'):
                        self._visit_node(requirement.expression)
                
                elif requirement.kind == "compound":
                    # Compound requirement: { T::value } -> std::convertible_to<int>
                    self._write("{ ")
                    if hasattr(requirement, 'expression'):
                        self._visit_node(requirement.expression)
                    self._write(" }")
                    
                    if hasattr(requirement, 'return_type'):
                        self._write(" -> ")
                        self._visit_node(requirement.return_type)
                
                elif requirement.kind == "nested":
                    # Nested requirement: requires T::value
                    self._write("requires ")
                    if hasattr(requirement, 'constraint'):
                        self._visit_constraint(requirement.constraint)
                
                else:
                    # Unknown requirement type
                    self._write("auto")
            else:
                # Fallback
                self._write("auto")
                
        except Exception as e:
            self._log_error(f"Error visiting requirement: {e}")
            self._write("auto")
    
    def _visit_builtin_type(self, node: CppBuiltinType):
        """Visit builtin type."""
        # Add const qualifier if present
        if CppTypeQualifier.CONST in node.qualifiers:
            self._write("const ")
        
        self._write(node.name)
        
        # Add volatile qualifier if present
        if CppTypeQualifier.VOLATILE in node.qualifiers:
            self._write(" volatile")
    
    def _visit_pointer_type(self, node: CppPointerType):
        """Visit pointer type."""
        self._visit_node(node.pointee_type)
        
        if self.style.pointer_alignment == "left":
            self._write("*")
        elif self.style.pointer_alignment == "right":
            self._write(" *")
        else:  # middle
            self._write(" * ")
    
    def _visit_reference_type(self, node: CppReferenceType):
        """Visit reference type."""
        self._visit_node(node.referenced_type)
        
        if node.is_rvalue_reference:
            self._write("&&")
        else:
            self._write("&")
    
    def _visit_array_type(self, node: CppArrayType):
        """Visit array type."""
        self._visit_node(node.element_type)
        self._write("[")
        
        if node.size:
            self._visit_node(node.size)
        
        self._write("]")
    
    def _visit_auto_type(self, node: CppAutoType):
        """Visit auto type."""
        self._write("auto")
    
    def _visit_decltype_type(self, node: CppDecltypeType):
        """Visit decltype type."""
        self._write("decltype(")
        self._visit_node(node.expression)
        self._write(")")
    
    def _write_access_specifier(self, access: CppAccessSpecifier):
        """Write access specifier."""
        indent = self.current_indent - self.style.access_specifier_indent
        if indent < 0:
            indent = 0
        
        spaces = self._get_indent_string(indent)
        self._write(f"{spaces}{access.value}:\n")
    
    def _needs_parentheses(self, node: CppBinaryOp) -> bool:
        """Check if binary operation needs parentheses based on operator precedence."""
        try:
            # C++ operator precedence table (higher number = higher precedence)
            precedence = {
                # Assignment operators (lowest precedence)
                CppOperator.ASSIGN: 1,
                CppOperator.ADD_ASSIGN: 1, CppOperator.SUB_ASSIGN: 1,
                CppOperator.MUL_ASSIGN: 1, CppOperator.DIV_ASSIGN: 1, CppOperator.MOD_ASSIGN: 1,
                CppOperator.LEFT_SHIFT_ASSIGN: 1, CppOperator.RIGHT_SHIFT_ASSIGN: 1,
                CppOperator.BIT_AND_ASSIGN: 1, CppOperator.BIT_OR_ASSIGN: 1, CppOperator.BIT_XOR_ASSIGN: 1,
                
                # Conditional operator
                CppOperator.CONDITIONAL: 2,
                
                # Logical OR
                CppOperator.LOGICAL_OR: 3,
                
                # Logical AND
                CppOperator.LOGICAL_AND: 4,
                
                # Bitwise OR
                CppOperator.BIT_OR: 5,
                
                # Bitwise XOR
                CppOperator.BIT_XOR: 6,
                
                # Bitwise AND
                CppOperator.BIT_AND: 7,
                
                # Equality operators
                CppOperator.EQ: 8, CppOperator.NE: 8,
                
                # Relational operators
                CppOperator.LT: 9, CppOperator.LE: 9, CppOperator.GT: 9, CppOperator.GE: 9,
                CppOperator.SPACESHIP: 9,  # C++20 three-way comparison
                
                # Shift operators
                CppOperator.LEFT_SHIFT: 10, CppOperator.RIGHT_SHIFT: 10,
                
                # Additive operators
                CppOperator.ADD: 11, CppOperator.SUB: 11,
                
                # Multiplicative operators
                CppOperator.MUL: 12, CppOperator.DIV: 12, CppOperator.MOD: 12,
                
                # Pointer-to-member operators
                CppOperator.POINTER_TO_MEMBER: 13,
                
                # Unary operators (highest precedence)
                CppOperator.UNARY_PLUS: 14, CppOperator.UNARY_MINUS: 14,
                CppOperator.LOGICAL_NOT: 14, CppOperator.BIT_NOT: 14,
                CppOperator.DEREF: 14, CppOperator.ADDR_OF: 14,
                CppOperator.SIZEOF: 14, CppOperator.ALIGNOF: 14,
                CppOperator.CAST: 14, CppOperator.NEW: 14, CppOperator.DELETE: 14,
            }
            
            # Get current operator precedence
            current_prec = precedence.get(node.operator, 0)
            
            # Check left operand
            if isinstance(node.left, CppBinaryOp):
                left_prec = precedence.get(node.left.operator, 0)
                # Left associativity: if left precedence is lower, we need parentheses
                if left_prec < current_prec:
                    return True
                # Same precedence: check associativity rules
                elif left_prec == current_prec:
                    # Most operators are left-associative, except assignment and conditional
                    if node.operator in [CppOperator.ASSIGN, CppOperator.ADD_ASSIGN, 
                                       CppOperator.SUB_ASSIGN, CppOperator.MUL_ASSIGN,
                                       CppOperator.DIV_ASSIGN, CppOperator.MOD_ASSIGN,
                                       CppOperator.LEFT_SHIFT_ASSIGN, CppOperator.RIGHT_SHIFT_ASSIGN,
                                       CppOperator.BIT_AND_ASSIGN, CppOperator.BIT_OR_ASSIGN,
                                       CppOperator.BIT_XOR_ASSIGN, CppOperator.CONDITIONAL]:
                        # Right-associative operators
                        return False
                    else:
                        # Left-associative operators
                        return True
            
            # Check right operand
            if isinstance(node.right, CppBinaryOp):
                right_prec = precedence.get(node.right.operator, 0)
                # Right associativity: if right precedence is lower or equal, we need parentheses
                if right_prec < current_prec:
                    return True
                # Same precedence: check associativity rules
                elif right_prec == current_prec:
                    # Assignment and conditional are right-associative
                    if node.operator in [CppOperator.ASSIGN, CppOperator.ADD_ASSIGN, 
                                       CppOperator.SUB_ASSIGN, CppOperator.MUL_ASSIGN,
                                       CppOperator.DIV_ASSIGN, CppOperator.MOD_ASSIGN,
                                       CppOperator.LEFT_SHIFT_ASSIGN, CppOperator.RIGHT_SHIFT_ASSIGN,
                                       CppOperator.BIT_AND_ASSIGN, CppOperator.BIT_OR_ASSIGN,
                                       CppOperator.BIT_XOR_ASSIGN, CppOperator.CONDITIONAL]:
                        # Right-associative operators
                        return True
                    else:
                        # Left-associative operators
                        return False
            
            # Special cases for mixed-type operations
            if self._is_mixed_type_operation(node):
                return True
            
            return False
            
        except Exception as e:
            # Conservative approach: add parentheses if there's any uncertainty
            self._log_warning(f"Error in precedence check: {e}")
            return True
    
    def _is_mixed_type_operation(self, node: CppBinaryOp) -> bool:
        """Check if operation involves mixed types that might need explicit parentheses."""
        try:
            # Check for mixed arithmetic types
            if node.operator in [CppOperator.ADD, CppOperator.SUB, CppOperator.MUL, CppOperator.DIV]:
                left_type = self._get_expression_type(node.left)
                right_type = self._get_expression_type(node.right)
                
                # Mixed integer/floating point operations
                if (left_type in ['int', 'long', 'short', 'char'] and 
                    right_type in ['float', 'double', 'long double']):
                    return True
                if (right_type in ['int', 'long', 'short', 'char'] and 
                    left_type in ['float', 'double', 'long double']):
                    return True
                
                # Mixed signed/unsigned operations
                if (left_type in ['int', 'long', 'short', 'char'] and 
                    right_type in ['unsigned int', 'unsigned long', 'unsigned short', 'unsigned char']):
                    return True
                if (right_type in ['int', 'long', 'short', 'char'] and 
                    left_type in ['unsigned int', 'unsigned long', 'unsigned short', 'unsigned char']):
                    return True
            
            # Check for pointer arithmetic
            if node.operator in [CppOperator.ADD, CppOperator.SUB]:
                left_type = self._get_expression_type(node.left)
                right_type = self._get_expression_type(node.right)
                
                if 'pointer' in left_type or 'pointer' in right_type:
                    return True
            
            return False
            
        except Exception:
            return False
    
    def _get_expression_type(self, expr) -> str:
        """Get the type of an expression (simplified)."""
        try:
            if hasattr(expr, 'type'):
                return str(expr.type)
            elif hasattr(expr, 'kind'):
                if expr.kind == "integer_literal":
                    return "int"
                elif expr.kind == "floating_literal":
                    return "double"
                elif expr.kind == "string_literal":
                    return "const char*"
                elif expr.kind == "boolean_literal":
                    return "bool"
                elif expr.kind == "identifier":
                    # Try to infer type from context
                    return "auto"
            return "auto"
        except Exception:
            return "auto"
    
    def _write(self, text: str):
        """Write text to output."""
        self.output.write(text)
    
    def _write_line(self, text: str = ""):
        """Write line to output."""
        if text:
            self._write(text)
        self._write("\n")
    
    def _write_indent(self):
        """Write current indentation."""
        self._write(self._get_indent_string())
    
    def _get_indent_string(self, level: Optional[int] = None) -> str:
        """Get indentation string."""
        if level is None:
            level = self.current_indent
        
        if self.style.use_spaces:
            return " " * (level * self.style.indent_size)
        else:
            return "\t" * level
    
    def _indent(self):
        """Increase indentation level."""
        self.current_indent += 1
    
    def _dedent(self):
        """Decrease indentation level."""
        self.current_indent = max(0, self.current_indent - 1)


def generate_cpp(node: CppNode, style: Optional[CppCodeStyle] = None) -> str:
    """Generate C++ code from AST node."""
    generator = CppCodeGenerator(style)
    return generator.generate(node)


class CppFormatter:
    """C++ code formatter with different style presets."""
    
    @staticmethod
    def google_style() -> CppCodeStyle:
        """Google C++ style guide."""
        return CppCodeStyle(
            indent_size=2,
            use_spaces=True,
            brace_style="k&r",
            max_line_length=80,
            namespace_indent=False,
            pointer_alignment="left",
            template_space_before_angle=False
        )
    
    @staticmethod
    def llvm_style() -> CppCodeStyle:
        """LLVM coding standards."""
        return CppCodeStyle(
            indent_size=2,
            use_spaces=True,
            brace_style="allman",
            max_line_length=80,
            namespace_indent=False,
            pointer_alignment="right",
            template_space_before_angle=True
        )
    
    @staticmethod
    def mozilla_style() -> CppCodeStyle:
        """Mozilla coding style."""
        return CppCodeStyle(
            indent_size=2,
            use_spaces=True,
            brace_style="allman",
            max_line_length=80,
            namespace_indent=True,
            pointer_alignment="left",
            template_space_before_angle=False
        )
    
    @staticmethod
    def webkit_style() -> CppCodeStyle:
        """WebKit coding style."""
        return CppCodeStyle(
            indent_size=4,
            use_spaces=True,
            brace_style="stroustrup",
            max_line_length=120,
            namespace_indent=False,
            pointer_alignment="left",
            template_space_before_angle=False
        )
    
    @staticmethod
    def microsoft_style() -> CppCodeStyle:
        """Microsoft Visual Studio style."""
        return CppCodeStyle(
            indent_size=4,
            use_spaces=True,
            brace_style="allman",
            max_line_length=120,
            namespace_indent=True,
            pointer_alignment="left",
            template_space_before_angle=True
        )