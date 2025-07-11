#!/usr/bin/env python3
"""
Julia Code Generator

Generates Julia source code from Julia AST nodes with proper formatting,
indentation, and Julia-specific syntax conventions.
"""

from typing import List, Optional, Any, Union, Dict
from .julia_ast import *


class JuliaGeneratorOptions:
    """Configuration options for Julia code generation."""
    
    def __init__(self):
        self.indent_size: int = 4
        self.use_spaces: bool = True
        self.max_line_length: int = 92  # Julia standard
        self.add_type_annotations: bool = True
        self.add_semicolons: bool = False  # Julia doesn't require semicolons
        self.preserve_comments: bool = True
        self.format_arrays: bool = True
        self.space_around_operators: bool = True
        self.align_struct_fields: bool = True


class JuliaGenerator:
    """Generates Julia source code from Julia AST."""
    
    def __init__(self, options: Optional[JuliaGeneratorOptions] = None):
        self.options = options or JuliaGeneratorOptions()
        self.indent_level = 0
        self.output_lines: List[str] = []
        self.current_line = ""
    
    def generate(self, node: JuliaNode) -> str:
        """Generate Julia code from AST node."""
        self.output_lines.clear()
        self.current_line = ""
        self.indent_level = 0
        
        self._visit_node(node)
        self._flush_current_line()
        
        return '\n'.join(self.output_lines)
    
    def _visit_node(self, node: JuliaNode) -> str:
        """Visit AST node and generate code."""
        if isinstance(node, JuliaProgram):
            return self._generate_program(node)
        elif isinstance(node, JuliaFile):
            return self._generate_file(node)
        elif isinstance(node, JuliaModuleDeclaration):
            return self._generate_module(node)
        elif isinstance(node, JuliaFunctionDeclaration):
            return self._generate_function(node)
        elif isinstance(node, JuliaStructDeclaration):
            return self._generate_struct(node)
        elif isinstance(node, JuliaImportDeclaration):
            return self._generate_import(node)
        elif isinstance(node, JuliaUsingDeclaration):
            return self._generate_using(node)
        elif isinstance(node, JuliaExportDeclaration):
            return self._generate_export(node)
        elif isinstance(node, JuliaConstDeclaration):
            return self._generate_const(node)
        elif isinstance(node, JuliaTypeAlias):
            return self._generate_type_alias(node)
        elif isinstance(node, JuliaAbstractTypeDeclaration):
            return self._generate_abstract_type(node)
        elif isinstance(node, JuliaMacroDeclaration):
            return self._generate_macro(node)
        
        # Expressions
        elif isinstance(node, JuliaIdentifier):
            return self._generate_identifier(node)
        elif isinstance(node, JuliaLiteralExpression):
            return self._generate_literal(node)
        elif isinstance(node, JuliaStringInterpolation):
            return self._generate_string_interpolation(node)
        elif isinstance(node, JuliaSymbolExpression):
            return self._generate_symbol(node)
        elif isinstance(node, JuliaArrayExpression):
            return self._generate_array(node)
        elif isinstance(node, JuliaTupleExpression):
            return self._generate_tuple(node)
        elif isinstance(node, JuliaDictExpression):
            return self._generate_dict(node)
        elif isinstance(node, JuliaRangeExpression):
            return self._generate_range(node)
        elif isinstance(node, JuliaComprehension):
            return self._generate_comprehension(node)
        elif isinstance(node, JuliaBinaryExpression):
            return self._generate_binary_expression(node)
        elif isinstance(node, JuliaUnaryExpression):
            return self._generate_unary_expression(node)
        elif isinstance(node, JuliaCallExpression):
            return self._generate_call(node)
        elif isinstance(node, JuliaIndexExpression):
            return self._generate_index(node)
        elif isinstance(node, JuliaDotExpression):
            return self._generate_dot_access(node)
        elif isinstance(node, JuliaBroadcastExpression):
            return self._generate_broadcast(node)
        elif isinstance(node, JuliaAssignmentExpression):
            return self._generate_assignment(node)
        elif isinstance(node, JuliaTernaryExpression):
            return self._generate_ternary(node)
        elif isinstance(node, JuliaMacroCall):
            return self._generate_macro_call(node)
        elif isinstance(node, JuliaQuoteExpression):
            return self._generate_quote(node)
        
        # Control flow
        elif isinstance(node, JuliaIfExpression):
            return self._generate_if(node)
        elif isinstance(node, JuliaForLoop):
            return self._generate_for(node)
        elif isinstance(node, JuliaWhileLoop):
            return self._generate_while(node)
        elif isinstance(node, JuliaReturnStatement):
            return self._generate_return(node)
        elif isinstance(node, JuliaBreakStatement):
            return "break"
        elif isinstance(node, JuliaContinueStatement):
            return "continue"
        elif isinstance(node, JuliaTryExpression):
            return self._generate_try(node)
        elif isinstance(node, JuliaLetExpression):
            return self._generate_let(node)
        elif isinstance(node, JuliaBeginBlock):
            return self._generate_begin(node)
        
        # Types
        elif isinstance(node, JuliaParametricType):
            return self._generate_parametric_type(node)
        elif isinstance(node, JuliaUnionType):
            return self._generate_union_type(node)
        
        return ""
    
    def _generate_program(self, program: JuliaProgram) -> str:
        """Generate complete Julia program."""
        for i, file in enumerate(program.files):
            if i > 0:
                self._add_line("")  # Separator between files
            self._visit_node(file)
        return ""
    
    def _generate_file(self, file: JuliaFile) -> str:
        """Generate Julia file."""
        # Module declaration
        if file.module_declaration:
            self._visit_node(file.module_declaration)
            return ""
        
        # Imports
        for imp in file.imports:
            self._visit_node(imp)
        
        if file.imports:
            self._add_line("")
        
        # Exports
        for export in file.exports:
            self._visit_node(export)
        
        if file.exports:
            self._add_line("")
        
        # Declarations
        for i, decl in enumerate(file.declarations):
            if i > 0:
                self._add_line("")
            self._visit_node(decl)
        
        return ""
    
    def _generate_module(self, module: JuliaModuleDeclaration) -> str:
        """Generate module declaration."""
        module_keyword = "baremodule" if module.is_baremodule else "module"
        self._add_line(f"{module_keyword} {module.name}")
        
        self._indent()
        for i, item in enumerate(module.body):
            if i > 0:
                self._add_line("")
            self._visit_node(item)
        self._dedent()
        
        self._add_line("end")
        return ""
    
    def _generate_function(self, func: JuliaFunctionDeclaration) -> str:
        """Generate function declaration."""
        if func.is_short_form and len(func.body) == 1:
            # Short form: f(x) = expr
            signature_str = self._generate_function_signature(func.signature) if func.signature else "()"
            body_expr = self._visit_node(func.body[0]) if func.body else ""
            self._add_line(f"function {func.name}{signature_str} = {body_expr}")
        else:
            # Long form function
            signature_str = self._generate_function_signature(func.signature) if func.signature else "()"
            
            # Return type annotation
            return_type_str = ""
            if func.return_type and self.options.add_type_annotations:
                return_type_str = f"::{self._visit_node(func.return_type)}"
            
            # Where clauses
            where_str = ""
            if func.where_clauses:
                where_parts = [self._visit_node(clause) for clause in func.where_clauses]
                where_str = f" where {', '.join(where_parts)}"
            
            self._add_line(f"function {func.name}{signature_str}{return_type_str}{where_str}")
            
            self._indent()
            for stmt in func.body:
                self._visit_node(stmt)
            self._dedent()
            
            self._add_line("end")
        
        return ""
    
    def _generate_function_signature(self, signature: Optional[JuliaFunctionSignature]) -> str:
        """Generate function signature."""
        if not signature:
            return "()"
        
        params = []
        
        # Regular parameters
        for param in signature.parameters:
            param_str = param.name
            if param.type and self.options.add_type_annotations:
                param_str += f"::{self._visit_node(param.type)}"
            if param.default_value:
                param_str += f"={self._visit_node(param.default_value)}"
            params.append(param_str)
        
        # Keyword parameters
        if signature.keyword_parameters:
            if params:
                params.append(";")
            
            for kw_param in signature.keyword_parameters:
                param_str = kw_param.name
                if kw_param.type and self.options.add_type_annotations:
                    param_str += f"::{self._visit_node(kw_param.type)}"
                if kw_param.default_value:
                    param_str += f"={self._visit_node(kw_param.default_value)}"
                params.append(param_str)
        
        # Varargs
        if signature.varargs:
            varargs_str = f"{signature.varargs.name}..."
            if signature.varargs.type and self.options.add_type_annotations:
                varargs_str = f"{signature.varargs.name}::{self._visit_node(signature.varargs.type)}..."
            params.append(varargs_str)
        
        return f"({', '.join(params)})"
    
    def _generate_struct(self, struct: JuliaStructDeclaration) -> str:
        """Generate struct declaration."""
        struct_keyword = "mutable struct" if struct.is_mutable else "struct"
        
        # Type parameters
        type_params_str = ""
        if struct.type_parameters:
            type_params = [param.name for param in struct.type_parameters]
            type_params_str = f"{{{', '.join(type_params)}}}"
        
        # Supertype
        supertype_str = ""
        if struct.supertype:
            supertype_str = f" <: {self._visit_node(struct.supertype)}"
        
        self._add_line(f"{struct_keyword} {struct.name}{type_params_str}{supertype_str}")
        
        self._indent()
        
        # Calculate max field name length for alignment
        max_name_length = 0
        if self.options.align_struct_fields and struct.fields:
            max_name_length = max(len(field.name) for field in struct.fields)
        
        for field in struct.fields:
            field_str = field.name
            
            if field.type and self.options.add_type_annotations:
                if self.options.align_struct_fields:
                    field_str = field_str.ljust(max_name_length)
                field_str += f"::{self._visit_node(field.type)}"
            
            if field.default_value:
                field_str += f" = {self._visit_node(field.default_value)}"
            
            self._add_line(field_str)
        
        self._dedent()
        self._add_line("end")
        return ""
    
    def _generate_import(self, imp: JuliaImportDeclaration) -> str:
        """Generate import declaration."""
        if imp.symbols:
            symbols_str = ", ".join(imp.symbols)
            import_str = f"import {imp.package}: {symbols_str}"
        else:
            import_str = f"import {imp.package}"
        
        if imp.alias:
            import_str += f" as {imp.alias}"
        
        self._add_line(import_str)
        return ""
    
    def _generate_using(self, using: JuliaUsingDeclaration) -> str:
        """Generate using declaration."""
        if using.symbols:
            symbols_str = ", ".join(using.symbols)
            using_str = f"using {using.package}: {symbols_str}"
        else:
            using_str = f"using {using.package}"
        
        self._add_line(using_str)
        return ""
    
    def _generate_export(self, export: JuliaExportDeclaration) -> str:
        """Generate export declaration."""
        symbols_str = ", ".join(export.symbols)
        self._add_line(f"export {symbols_str}")
        return ""
    
    def _generate_const(self, const: JuliaConstDeclaration) -> str:
        """Generate const declaration."""
        const_str = f"const {const.name}"
        
        if const.type and self.options.add_type_annotations:
            const_str += f"::{self._visit_node(const.type)}"
        
        if const.value:
            const_str += f" = {self._visit_node(const.value)}"
        
        self._add_line(const_str)
        return ""
    
    def _generate_type_alias(self, alias: JuliaTypeAlias) -> str:
        """Generate type alias."""
        alias_str = f"const {alias.name}"
        
        if alias.type_parameters:
            type_params = [param.name for param in alias.type_parameters]
            alias_str += f"{{{', '.join(type_params)}}}"
        
        if alias.target_type:
            alias_str += f" = {self._visit_node(alias.target_type)}"
        
        self._add_line(alias_str)
        return ""
    
    def _generate_abstract_type(self, abstract: JuliaAbstractTypeDeclaration) -> str:
        """Generate abstract type declaration."""
        abstract_str = f"abstract type {abstract.name}"
        
        if abstract.type_parameters:
            type_params = [param.name for param in abstract.type_parameters]
            abstract_str += f"{{{', '.join(type_params)}}}"
        
        if abstract.supertype:
            abstract_str += f" <: {self._visit_node(abstract.supertype)}"
        
        abstract_str += " end"
        self._add_line(abstract_str)
        return ""
    
    def _generate_macro(self, macro: JuliaMacroDeclaration) -> str:
        """Generate macro declaration."""
        params = [param.name for param in macro.parameters]
        params_str = f"({', '.join(params)})" if params else ""
        
        self._add_line(f"macro {macro.name}{params_str}")
        
        self._indent()
        for stmt in macro.body:
            self._visit_node(stmt)
        self._dedent()
        
        self._add_line("end")
        return ""
    
    def _generate_identifier(self, identifier: JuliaIdentifier) -> str:
        """Generate identifier."""
        return identifier.name
    
    def _generate_literal(self, literal: JuliaLiteralExpression) -> str:
        """Generate literal expression."""
        if literal.literal_type == "string":
            # Escape quotes in string
            escaped_value = str(literal.value).replace('"', '\\"')
            return f'"{escaped_value}"'
        elif literal.literal_type == "char":
            return f"'{literal.value}'"
        elif literal.literal_type == "boolean":
            return "true" if literal.value else "false"
        elif literal.literal_type == "nothing":
            return "nothing"
        else:
            return str(literal.value)
    
    def _generate_string_interpolation(self, interpolation: JuliaStringInterpolation) -> str:
        """Generate string interpolation."""
        result = '"'
        for part in interpolation.parts:
            if isinstance(part, str):
                result += part
            else:
                result += f"$({self._visit_node(part)})"
        result += '"'
        return result
    
    def _generate_symbol(self, symbol: JuliaSymbolExpression) -> str:
        """Generate symbol expression."""
        return f":{symbol.name}"
    
    def _generate_array(self, array: JuliaArrayExpression) -> str:
        """Generate array expression."""
        if not array.elements:
            return "[]"
        
        if len(array.elements) <= 3 or not self.options.format_arrays:
            # Single line
            elements = [self._visit_node(elem) for elem in array.elements]
            return f"[{', '.join(elements)}]"
        else:
            # Multi-line for longer arrays
            result = "[\n"
            self._indent()
            for i, elem in enumerate(array.elements):
                comma = "," if i < len(array.elements) - 1 else ""
                self._add_line(f"{self._get_indent()}{self._visit_node(elem)}{comma}")
            self._dedent()
            result += f"{self._get_indent()}]"
            return result
    
    def _generate_tuple(self, tuple_expr: JuliaTupleExpression) -> str:
        """Generate tuple expression."""
        if not tuple_expr.elements:
            return "()"
        
        elements = [self._visit_node(elem) for elem in tuple_expr.elements]
        
        if len(tuple_expr.elements) == 1:
            # Single element tuple needs trailing comma
            return f"({elements[0]},)"
        
        return f"({', '.join(elements)})"
    
    def _generate_dict(self, dict_expr: JuliaDictExpression) -> str:
        """Generate dictionary expression."""
        if not dict_expr.pairs:
            return "Dict()"
        
        pairs = []
        for key, value in dict_expr.pairs:
            key_str = self._visit_node(key)
            value_str = self._visit_node(value)
            pairs.append(f"{key_str} => {value_str}")
        
        if len(pairs) <= 2:
            return f"Dict({', '.join(pairs)})"
        else:
            # Multi-line for larger dictionaries
            result = "Dict(\n"
            self._indent()
            for i, pair in enumerate(pairs):
                comma = "," if i < len(pairs) - 1 else ""
                self._add_line(f"{self._get_indent()}{pair}{comma}")
            self._dedent()
            result += f"{self._get_indent()})"
            return result
    
    def _generate_range(self, range_expr: JuliaRangeExpression) -> str:
        """Generate range expression."""
        if range_expr.step:
            start = self._visit_node(range_expr.start) if range_expr.start else ""
            step = self._visit_node(range_expr.step)
            stop = self._visit_node(range_expr.stop) if range_expr.stop else ""
            return f"{start}:{step}:{stop}"
        else:
            start = self._visit_node(range_expr.start) if range_expr.start else ""
            stop = self._visit_node(range_expr.stop) if range_expr.stop else ""
            return f"{start}:{stop}"
    
    def _generate_comprehension(self, comp: JuliaComprehension) -> str:
        """Generate array comprehension."""
        expr_str = self._visit_node(comp.expression) if comp.expression else ""
        
        generators = []
        for gen in comp.generators:
            gen_str = f"{gen.variable} in {self._visit_node(gen.iterable)}"
            if gen.condition:
                gen_str += f" if {self._visit_node(gen.condition)}"
            generators.append(gen_str)
        
        generators_str = ", ".join(generators)
        return f"[{expr_str} for {generators_str}]"
    
    def _generate_binary_expression(self, binary: JuliaBinaryExpression) -> str:
        """Generate binary expression."""
        left = self._visit_node(binary.left) if binary.left else ""
        right = self._visit_node(binary.right) if binary.right else ""
        
        if self.options.space_around_operators:
            return f"{left} {binary.operator} {right}"
        else:
            return f"{left}{binary.operator}{right}"
    
    def _generate_unary_expression(self, unary: JuliaUnaryExpression) -> str:
        """Generate unary expression."""
        expr = self._visit_node(unary.expression) if unary.expression else ""
        
        if unary.is_postfix:
            return f"{expr}{unary.operator}"
        else:
            return f"{unary.operator}{expr}"
    
    def _generate_call(self, call: JuliaCallExpression) -> str:
        """Generate function call."""
        func = self._visit_node(call.function) if call.function else ""
        
        args = [self._visit_node(arg) for arg in call.arguments]
        
        # Add keyword arguments
        kw_args = []
        for name, expr in call.keyword_arguments.items():
            kw_args.append(f"{name}={self._visit_node(expr)}")
        
        if kw_args:
            if args:
                all_args = args + [";"] + kw_args
            else:
                all_args = [";"] + kw_args
        else:
            all_args = args
        
        args_str = ", ".join(all_args)
        return f"{func}({args_str})"
    
    def _generate_index(self, index: JuliaIndexExpression) -> str:
        """Generate array indexing."""
        obj = self._visit_node(index.object) if index.object else ""
        indices = [self._visit_node(idx) for idx in index.indices]
        indices_str = ", ".join(indices)
        return f"{obj}[{indices_str}]"
    
    def _generate_dot_access(self, dot: JuliaDotExpression) -> str:
        """Generate dot access."""
        obj = self._visit_node(dot.object) if dot.object else ""
        return f"{obj}.{dot.field}"
    
    def _generate_broadcast(self, broadcast: JuliaBroadcastExpression) -> str:
        """Generate broadcasting expression."""
        if broadcast.operator:
            # Broadcast operator like .+
            left = self._visit_node(broadcast.arguments[0]) if broadcast.arguments else ""
            right = self._visit_node(broadcast.arguments[1]) if len(broadcast.arguments) > 1 else ""
            return f"{left} {broadcast.operator} {right}"
        elif broadcast.function:
            # Broadcast function call like f.(x)
            func = self._visit_node(broadcast.function)
            args = [self._visit_node(arg) for arg in broadcast.arguments]
            args_str = ", ".join(args)
            return f"{func}.({args_str})"
        
        return ""
    
    def _generate_assignment(self, assignment: JuliaAssignmentExpression) -> str:
        """Generate assignment expression."""
        target = self._visit_node(assignment.target) if assignment.target else ""
        value = self._visit_node(assignment.value) if assignment.value else ""
        
        if self.options.space_around_operators:
            return f"{target} {assignment.operator} {value}"
        else:
            return f"{target}{assignment.operator}{value}"
    
    def _generate_ternary(self, ternary: JuliaTernaryExpression) -> str:
        """Generate ternary expression."""
        condition = self._visit_node(ternary.condition) if ternary.condition else ""
        true_expr = self._visit_node(ternary.true_expression) if ternary.true_expression else ""
        false_expr = self._visit_node(ternary.false_expression) if ternary.false_expression else ""
        
        return f"{condition} ? {true_expr} : {false_expr}"
    
    def _generate_macro_call(self, macro_call: JuliaMacroCall) -> str:
        """Generate macro call."""
        args = [self._visit_node(arg) for arg in macro_call.arguments]
        args_str = " ".join(args) if args else ""
        return f"@{macro_call.macro_name} {args_str}".strip()
    
    def _generate_quote(self, quote: JuliaQuoteExpression) -> str:
        """Generate quote expression."""
        if quote.is_short_form and len(quote.body) == 1:
            # Short form: :(expr)
            expr = self._visit_node(quote.body[0]) if quote.body else ""
            return f":({expr})"
        else:
            # Long form: quote ... end
            self._add_line("quote")
            self._indent()
            for stmt in quote.body:
                self._visit_node(stmt)
            self._dedent()
            self._add_line("end")
            return ""
    
    def _generate_if(self, if_expr: JuliaIfExpression) -> str:
        """Generate if expression."""
        condition = self._visit_node(if_expr.condition) if if_expr.condition else ""
        self._add_line(f"if {condition}")
        
        self._indent()
        for stmt in if_expr.then_body:
            self._visit_node(stmt)
        self._dedent()
        
        # Elseif clauses
        for elseif_clause in if_expr.elseif_clauses:
            condition = self._visit_node(elseif_clause.condition) if elseif_clause.condition else ""
            self._add_line(f"elseif {condition}")
            self._indent()
            for stmt in elseif_clause.body:
                self._visit_node(stmt)
            self._dedent()
        
        # Else clause
        if if_expr.else_body:
            self._add_line("else")
            self._indent()
            for stmt in if_expr.else_body:
                self._visit_node(stmt)
            self._dedent()
        
        self._add_line("end")
        return ""
    
    def _generate_for(self, for_loop: JuliaForLoop) -> str:
        """Generate for loop."""
        iterable = self._visit_node(for_loop.iterable) if for_loop.iterable else ""
        self._add_line(f"for {for_loop.variable} in {iterable}")
        
        self._indent()
        for stmt in for_loop.body:
            self._visit_node(stmt)
        self._dedent()
        
        self._add_line("end")
        return ""
    
    def _generate_while(self, while_loop: JuliaWhileLoop) -> str:
        """Generate while loop."""
        condition = self._visit_node(while_loop.condition) if while_loop.condition else ""
        self._add_line(f"while {condition}")
        
        self._indent()
        for stmt in while_loop.body:
            self._visit_node(stmt)
        self._dedent()
        
        self._add_line("end")
        return ""
    
    def _generate_return(self, return_stmt: JuliaReturnStatement) -> str:
        """Generate return statement."""
        if return_stmt.expression:
            expr = self._visit_node(return_stmt.expression)
            self._add_line(f"return {expr}")
        else:
            self._add_line("return")
        return ""
    
    def _generate_try(self, try_expr: JuliaTryExpression) -> str:
        """Generate try expression."""
        self._add_line("try")
        
        self._indent()
        for stmt in try_expr.try_body:
            self._visit_node(stmt)
        self._dedent()
        
        # Catch clauses
        for catch_clause in try_expr.catch_clauses:
            catch_str = "catch"
            if catch_clause.variable:
                catch_str += f" {catch_clause.variable}"
                if catch_clause.exception_type:
                    catch_str += f"::{self._visit_node(catch_clause.exception_type)}"
            
            self._add_line(catch_str)
            self._indent()
            for stmt in catch_clause.body:
                self._visit_node(stmt)
            self._dedent()
        
        # Finally clause
        if try_expr.finally_body:
            self._add_line("finally")
            self._indent()
            for stmt in try_expr.finally_body:
                self._visit_node(stmt)
            self._dedent()
        
        self._add_line("end")
        return ""
    
    def _generate_let(self, let_expr: JuliaLetExpression) -> str:
        """Generate let expression."""
        if let_expr.bindings:
            bindings = [self._visit_node(binding) for binding in let_expr.bindings]
            bindings_str = ", ".join(bindings)
            self._add_line(f"let {bindings_str}")
        else:
            self._add_line("let")
        
        self._indent()
        for stmt in let_expr.body:
            self._visit_node(stmt)
        self._dedent()
        
        self._add_line("end")
        return ""
    
    def _generate_begin(self, begin_block: JuliaBeginBlock) -> str:
        """Generate begin block."""
        self._add_line("begin")
        
        self._indent()
        for stmt in begin_block.body:
            self._visit_node(stmt)
        self._dedent()
        
        self._add_line("end")
        return ""
    
    def _generate_parametric_type(self, param_type: JuliaParametricType) -> str:
        """Generate parametric type."""
        if param_type.parameters:
            params = [self._visit_node(param) for param in param_type.parameters]
            params_str = f"{{{', '.join(params)}}}"
            return f"{param_type.base_type}{params_str}"
        else:
            return param_type.base_type
    
    def _generate_union_type(self, union_type: JuliaUnionType) -> str:
        """Generate union type."""
        types = [self._visit_node(t) for t in union_type.types]
        return f"Union{{{', '.join(types)}}}"
    
    # Helper methods
    def _indent(self):
        """Increase indentation level."""
        self.indent_level += 1
    
    def _dedent(self):
        """Decrease indentation level."""
        self.indent_level = max(0, self.indent_level - 1)
    
    def _get_indent(self) -> str:
        """Get current indentation string."""
        if self.options.use_spaces:
            return " " * (self.indent_level * self.options.indent_size)
        else:
            return "\t" * self.indent_level
    
    def _add_line(self, line: str = ""):
        """Add line to output."""
        if line:
            indented_line = self._get_indent() + line
        else:
            indented_line = line
        
        self.output_lines.append(indented_line)
    
    def _flush_current_line(self):
        """Flush current line if it has content."""
        if self.current_line.strip():
            self.output_lines.append(self.current_line)
            self.current_line = ""


def generate_julia_code(node: JuliaNode, options: Optional[JuliaGeneratorOptions] = None) -> str:
    """Generate Julia source code from AST node."""
    generator = JuliaGenerator(options)
    return generator.generate(node) 