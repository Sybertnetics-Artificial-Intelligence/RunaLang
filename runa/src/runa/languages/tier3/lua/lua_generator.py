#!/usr/bin/env python3
"""
Lua Generator - Clean Lua Code Generation

Provides comprehensive Lua code generation with multiple formatting styles:
- Standard Lua format with proper indentation and spacing
- Compact format for minimal space usage
- Love2D format for game development
- OpenResty format for web development
- Development format with extensive comments
- LuaRocks format for module distribution

Features:
- Proper function and table formatting
- Operator precedence handling
- String literal formatting with multiple quote styles
- Comment preservation and generation
- Control flow structure formatting
- Module and require statement generation
"""

from typing import List, Dict, Optional, Any, Union, TextIO
from dataclasses import dataclass
from enum import Enum
import io

from .lua_ast import *


class LuaFormatStyle(Enum):
    """Lua code formatting styles"""
    STANDARD = "standard"          # Clean, readable Lua
    COMPACT = "compact"            # Minimal spacing
    LOVE2D = "love2d"             # Love2D game framework style
    OPENRESTY = "openresty"       # OpenResty/Nginx Lua style
    DEVELOPMENT = "development"    # With extensive comments
    LUAROCKS = "luarocks"         # LuaRocks module style


@dataclass
class LuaGeneratorConfig:
    """Configuration for Lua code generation"""
    style: LuaFormatStyle = LuaFormatStyle.STANDARD
    indent_size: int = 2
    max_line_length: int = 120
    preserve_comments: bool = True
    add_semicolons: bool = False
    quote_style: str = '"'  # or "'"
    
    # Table formatting
    table_multiline_threshold: int = 3
    align_table_values: bool = True
    trailing_comma: bool = False
    
    # Function formatting
    space_before_function_params: bool = False
    space_in_function_params: bool = True
    
    # Development options
    add_type_comments: bool = False
    add_documentation: bool = False
    verbose_formatting: bool = False
    
    # Style-specific options
    love2d_conventions: bool = False
    openresty_conventions: bool = False
    luarocks_conventions: bool = False


class LuaCodeGenerator:
    """Generates clean Lua code from AST"""
    
    def __init__(self, config: Optional[LuaGeneratorConfig] = None):
        self.config = config or LuaGeneratorConfig()
        self.output = io.StringIO()
        self.indent_level = 0
        self.current_line_length = 0
        self.needs_newline = False
        
        # Adjust config based on style
        self._adjust_config_for_style()
        
        # Operator precedence for proper parenthesization
        self.operator_precedence = {
            LuaBinaryOperator.OR: 1,
            LuaBinaryOperator.AND: 2,
            LuaBinaryOperator.EQ: 3, LuaBinaryOperator.NE: 3,
            LuaBinaryOperator.LT: 3, LuaBinaryOperator.LE: 3,
            LuaBinaryOperator.GT: 3, LuaBinaryOperator.GE: 3,
            LuaBinaryOperator.CONCAT: 4,
            LuaBinaryOperator.ADD: 5, LuaBinaryOperator.SUB: 5,
            LuaBinaryOperator.MUL: 6, LuaBinaryOperator.DIV: 6,
            LuaBinaryOperator.IDIV: 6, LuaBinaryOperator.MOD: 6,
            LuaBinaryOperator.POW: 8,
        }
        
        # Right-associative operators
        self.right_associative = {LuaBinaryOperator.POW, LuaBinaryOperator.CONCAT}
    
    def _adjust_config_for_style(self) -> None:
        """Adjust configuration based on selected style"""
        if self.config.style == LuaFormatStyle.COMPACT:
            self.config.indent_size = 1
            self.config.preserve_comments = False
            self.config.space_in_function_params = False
            self.config.table_multiline_threshold = 10
        elif self.config.style == LuaFormatStyle.LOVE2D:
            self.config.love2d_conventions = True
            self.config.add_documentation = True
        elif self.config.style == LuaFormatStyle.OPENRESTY:
            self.config.openresty_conventions = True
            self.config.indent_size = 4
        elif self.config.style == LuaFormatStyle.DEVELOPMENT:
            self.config.add_type_comments = True
            self.config.add_documentation = True
            self.config.verbose_formatting = True
        elif self.config.style == LuaFormatStyle.LUAROCKS:
            self.config.luarocks_conventions = True
            self.config.add_documentation = True
    
    def generate(self, node: LuaNode) -> str:
        """Generate Lua code from AST node"""
        self.output = io.StringIO()
        self.indent_level = 0
        self.current_line_length = 0
        self.needs_newline = False
        
        if isinstance(node, LuaModule):
            self._generate_module(node)
        else:
            node.accept(self)
        
        return self.output.getvalue().rstrip() + "\n"
    
    def _generate_module(self, module: LuaModule) -> None:
        """Generate complete Lua module"""
        if self.config.style == LuaFormatStyle.DEVELOPMENT:
            self._write_line("-- Generated Lua Module")
            if module.filename:
                self._write_line(f"-- File: {module.filename}")
            self._write_line("")
        
        # Generate module header for LuaRocks style
        if self.config.luarocks_conventions and module.name:
            self._write_line(f"-- Module: {module.name}")
            self._write_line(f"local {module.name} = {{}}")
            self._write_line("")
        
        # Generate require statements
        if module.imports:
            for import_stmt in module.imports:
                import_stmt.accept(self)
            self._write_line("")
        
        # Generate module body
        module.body.accept(self)
        
        # Generate module footer for LuaRocks style
        if self.config.luarocks_conventions and module.name:
            self._write_line("")
            self._write_line(f"return {module.name}")
    
    # Visitor methods
    def visit_module(self, node: LuaModule) -> None:
        self._generate_module(node)
    
    def visit_block(self, node: LuaBlock) -> None:
        """Generate block of statements"""
        for i, stmt in enumerate(node.statements):
            if i > 0 and self._needs_spacing_between_statements(node.statements[i-1], stmt):
                self._write_line("")
            stmt.accept(self)
    
    def visit_literal(self, node: LuaLiteral) -> None:
        """Generate literal value"""
        if node.literal_type == LuaLiteralType.NIL:
            self._write("nil")
        elif node.literal_type == LuaLiteralType.BOOLEAN:
            self._write("true" if node.value else "false")
        else:
            self._write(str(node.value))
    
    def visit_identifier(self, node: LuaIdentifier) -> None:
        """Generate identifier"""
        self._write(node.name)
    
    def visit_binary_operation(self, node: LuaBinaryOperation) -> None:
        """Generate binary operation"""
        left_needs_parens = self._needs_parentheses(node.left, node.operator, True)
        right_needs_parens = self._needs_parentheses(node.right, node.operator, False)
        
        if left_needs_parens:
            self._write("(")
        node.left.accept(self)
        if left_needs_parens:
            self._write(")")
        
        # Add spaces around operator
        if self.config.style != LuaFormatStyle.COMPACT:
            self._write(f" {node.operator.value} ")
        else:
            self._write(node.operator.value)
        
        if right_needs_parens:
            self._write("(")
        node.right.accept(self)
        if right_needs_parens:
            self._write(")")
    
    def visit_unary_operation(self, node: LuaUnaryOperation) -> None:
        """Generate unary operation"""
        self._write(node.operator.value)
        
        # Add space for word operators
        if node.operator == LuaUnaryOperator.NOT:
            self._write(" ")
        
        needs_parens = isinstance(node.operand, (LuaBinaryOperation, LuaUnaryOperation))
        if needs_parens:
            self._write("(")
        node.operand.accept(self)
        if needs_parens:
            self._write(")")
    
    def visit_table_constructor(self, node: LuaTableConstructor) -> None:
        """Generate table constructor"""
        if not node.fields:
            self._write("{}")
            return
        
        # Determine if table should be multiline
        should_be_multiline = (
            len(node.fields) >= self.config.table_multiline_threshold or
            any(self._field_is_complex(field) for field in node.fields)
        )
        
        if should_be_multiline:
            self._generate_multiline_table(node)
        else:
            self._generate_inline_table(node)
    
    def _generate_multiline_table(self, node: LuaTableConstructor) -> None:
        """Generate multiline table"""
        self._write("{")
        self._write_line("")
        self._indent()
        
        for i, field in enumerate(node.fields):
            self._write_indent()
            field.accept(self)
            
            if i < len(node.fields) - 1 or self.config.trailing_comma:
                self._write(",")
            
            self._write_line("")
        
        self._dedent()
        self._write_indent()
        self._write("}")
    
    def _generate_inline_table(self, node: LuaTableConstructor) -> None:
        """Generate inline table"""
        self._write("{")
        
        for i, field in enumerate(node.fields):
            if i > 0:
                self._write(", " if self.config.style != LuaFormatStyle.COMPACT else ",")
            field.accept(self)
        
        self._write("}")
    
    def visit_table_field(self, node: LuaTableField) -> None:
        """Generate table field"""
        if node.key is None:
            # Array-style field
            node.value.accept(self)
        elif isinstance(node.key, LuaStringLiteral) and self._is_valid_identifier(node.key.value):
            # Named field with identifier key
            self._write(node.key.value)
            self._write(" = " if self.config.style != LuaFormatStyle.COMPACT else "=")
            node.value.accept(self)
        else:
            # Computed key
            self._write("[")
            node.key.accept(self)
            self._write("]")
            self._write(" = " if self.config.style != LuaFormatStyle.COMPACT else "=")
            node.value.accept(self)
    
    def visit_table_access(self, node: LuaTableAccess) -> None:
        """Generate table access"""
        node.table.accept(self)
        
        if node.is_dot_notation and isinstance(node.key, LuaStringLiteral):
            self._write(".")
            self._write(node.key.value)
        else:
            self._write("[")
            node.key.accept(self)
            self._write("]")
    
    def visit_function_call(self, node: LuaFunctionCall) -> None:
        """Generate function call"""
        node.function.accept(self)
        
        if self.config.space_before_function_params:
            self._write(" ")
        
        self._write("(")
        
        for i, arg in enumerate(node.arguments):
            if i > 0:
                self._write(", " if self.config.space_in_function_params else ",")
            arg.accept(self)
        
        self._write(")")
    
    def visit_function_definition(self, node: LuaFunctionDefinition) -> None:
        """Generate function definition"""
        self._write("function")
        
        if self.config.space_before_function_params:
            self._write(" ")
        
        self._write("(")
        
        for i, param in enumerate(node.parameters):
            if i > 0:
                self._write(", " if self.config.space_in_function_params else ",")
            self._write(param)
        
        if node.is_vararg:
            if node.parameters:
                self._write(", " if self.config.space_in_function_params else ",")
            self._write("...")
        
        self._write(")")
        self._write_line("")
        
        self._indent()
        node.body.accept(self)
        self._dedent()
        
        self._write_indent()
        self._write("end")
    
    def visit_vararg_expression(self, node: LuaVarargExpression) -> None:
        """Generate vararg expression"""
        self._write("...")
    
    def visit_assignment(self, node: LuaAssignment) -> None:
        """Generate assignment statement"""
        self._write_indent()
        
        if node.is_local:
            self._write("local ")
        
        for i, target in enumerate(node.targets):
            if i > 0:
                self._write(", ")
            target.accept(self)
        
        if node.values:
            self._write(" = " if self.config.style != LuaFormatStyle.COMPACT else "=")
            
            for i, value in enumerate(node.values):
                if i > 0:
                    self._write(", ")
                value.accept(self)
        
        if self.config.add_semicolons:
            self._write(";")
        
        self._write_line("")
    
    def visit_local_declaration(self, node: LuaLocalDeclaration) -> None:
        """Generate local declaration"""
        self._write_indent()
        self._write("local ")
        
        for i, name in enumerate(node.names):
            if i > 0:
                self._write(", ")
            self._write(name)
        
        if node.values:
            self._write(" = " if self.config.style != LuaFormatStyle.COMPACT else "=")
            
            for i, value in enumerate(node.values):
                if i > 0:
                    self._write(", ")
                value.accept(self)
        
        if self.config.add_semicolons:
            self._write(";")
        
        self._write_line("")
    
    def visit_function_declaration(self, node: LuaFunctionDeclaration) -> None:
        """Generate function declaration"""
        self._write_indent()
        
        if node.is_local:
            self._write("local ")
        
        self._write("function ")
        
        # Generate function name with table path
        if node.table_path:
            self._write(".".join(node.table_path))
            self._write("." if not node.is_method else ":")
        
        self._write(node.name)
        
        if self.config.space_before_function_params:
            self._write(" ")
        
        self._write("(")
        
        for i, param in enumerate(node.parameters):
            if i > 0:
                self._write(", " if self.config.space_in_function_params else ",")
            self._write(param)
        
        if node.is_vararg:
            if node.parameters:
                self._write(", " if self.config.space_in_function_params else ",")
            self._write("...")
        
        self._write(")")
        self._write_line("")
        
        self._indent()
        node.body.accept(self)
        self._dedent()
        
        self._write_indent()
        self._write("end")
        self._write_line("")
    
    def visit_if_statement(self, node: LuaIfStatement) -> None:
        """Generate if statement"""
        self._write_indent()
        self._write("if ")
        node.condition.accept(self)
        self._write(" then")
        self._write_line("")
        
        self._indent()
        node.then_block.accept(self)
        self._dedent()
        
        # Generate elseif clauses
        for elseif_clause in node.elseif_clauses:
            self._write_indent()
            self._write("elseif ")
            elseif_clause.condition.accept(self)
            self._write(" then")
            self._write_line("")
            
            self._indent()
            elseif_clause.block.accept(self)
            self._dedent()
        
        # Generate else clause
        if node.else_block:
            self._write_indent()
            self._write("else")
            self._write_line("")
            
            self._indent()
            node.else_block.accept(self)
            self._dedent()
        
        self._write_indent()
        self._write("end")
        self._write_line("")
    
    def visit_elseif_clause(self, node: LuaElseIfClause) -> None:
        """Generate elseif clause (handled by if statement)"""
        pass
    
    def visit_while_statement(self, node: LuaWhileStatement) -> None:
        """Generate while statement"""
        self._write_indent()
        self._write("while ")
        node.condition.accept(self)
        self._write(" do")
        self._write_line("")
        
        self._indent()
        node.body.accept(self)
        self._dedent()
        
        self._write_indent()
        self._write("end")
        self._write_line("")
    
    def visit_repeat_statement(self, node: LuaRepeatStatement) -> None:
        """Generate repeat-until statement"""
        self._write_indent()
        self._write("repeat")
        self._write_line("")
        
        self._indent()
        node.body.accept(self)
        self._dedent()
        
        self._write_indent()
        self._write("until ")
        node.condition.accept(self)
        self._write_line("")
    
    def visit_for_statement(self, node: LuaForStatement) -> None:
        """Generate numeric for statement"""
        self._write_indent()
        self._write(f"for {node.variable} = ")
        node.start.accept(self)
        self._write(", ")
        node.end.accept(self)
        
        if node.step:
            self._write(", ")
            node.step.accept(self)
        
        self._write(" do")
        self._write_line("")
        
        self._indent()
        node.body.accept(self)
        self._dedent()
        
        self._write_indent()
        self._write("end")
        self._write_line("")
    
    def visit_for_in_statement(self, node: LuaForInStatement) -> None:
        """Generate generic for-in statement"""
        self._write_indent()
        self._write("for ")
        
        for i, var in enumerate(node.variables):
            if i > 0:
                self._write(", ")
            self._write(var)
        
        self._write(" in ")
        
        for i, iterator in enumerate(node.iterators):
            if i > 0:
                self._write(", ")
            iterator.accept(self)
        
        self._write(" do")
        self._write_line("")
        
        self._indent()
        node.body.accept(self)
        self._dedent()
        
        self._write_indent()
        self._write("end")
        self._write_line("")
    
    def visit_break_statement(self, node: LuaBreakStatement) -> None:
        """Generate break statement"""
        self._write_indent()
        self._write("break")
        if self.config.add_semicolons:
            self._write(";")
        self._write_line("")
    
    def visit_continue_statement(self, node: LuaContinueStatement) -> None:
        """Generate continue statement (Lua 5.2+)"""
        self._write_indent()
        self._write("continue")
        if self.config.add_semicolons:
            self._write(";")
        self._write_line("")
    
    def visit_return_statement(self, node: LuaReturnStatement) -> None:
        """Generate return statement"""
        self._write_indent()
        self._write("return")
        
        if node.values:
            self._write(" ")
            for i, value in enumerate(node.values):
                if i > 0:
                    self._write(", ")
                value.accept(self)
        
        if self.config.add_semicolons:
            self._write(";")
        self._write_line("")
    
    def visit_goto_statement(self, node: LuaGotoStatement) -> None:
        """Generate goto statement"""
        self._write_indent()
        self._write(f"goto {node.label}")
        if self.config.add_semicolons:
            self._write(";")
        self._write_line("")
    
    def visit_label_statement(self, node: LuaLabelStatement) -> None:
        """Generate label statement"""
        self._write_indent()
        self._write(f"::{node.name}::")
        self._write_line("")
    
    def visit_expression_statement(self, node: LuaExpressionStatement) -> None:
        """Generate expression statement"""
        self._write_indent()
        node.expression.accept(self)
        if self.config.add_semicolons:
            self._write(";")
        self._write_line("")
    
    def visit_comment(self, node: LuaComment) -> None:
        """Generate comment"""
        if not self.config.preserve_comments:
            return
        
        if node.is_multiline:
            self._write_indent()
            self._write("--[[")
            self._write(node.text)
            self._write("]]")
            self._write_line("")
        else:
            self._write_indent()
            self._write("-- ")
            self._write(node.text)
            self._write_line("")
    
    def visit_require_statement(self, node: LuaRequireStatement) -> None:
        """Generate require statement"""
        self._write_indent()
        
        if node.is_local:
            self._write("local ")
            if node.alias:
                self._write(f"{node.alias} = ")
            else:
                # Extract module name from path
                module_name = node.module_name.split(".")[-1]
                self._write(f"{module_name} = ")
        
        self._write(f'require("{node.module_name}")')
        
        if self.config.add_semicolons:
            self._write(";")
        self._write_line("")
    
    def visit_do_statement(self, node: LuaDoStatement) -> None:
        """Generate do-end statement"""
        self._write_indent()
        self._write("do")
        self._write_line("")
        
        self._indent()
        node.body.accept(self)
        self._dedent()
        
        self._write_indent()
        self._write("end")
        self._write_line("")
    
    def visit_string_literal(self, node: LuaStringLiteral) -> None:
        """Generate string literal"""
        if node.is_multiline:
            self._write(f"[[{node.value}]]")
        else:
            quote = node.quote_style or self.config.quote_style
            escaped_value = self._escape_string(node.value, quote)
            self._write(f"{quote}{escaped_value}{quote}")
    
    def visit_number_literal(self, node: LuaNumberLiteral) -> None:
        """Generate number literal"""
        if node.raw_text and not node.is_hex:
            self._write(node.raw_text)
        elif node.is_hex:
            self._write(hex(int(node.value)))
        else:
            self._write(str(node.value))
    
    # Helper methods
    def _needs_parentheses(self, expr: LuaExpression, parent_op: LuaBinaryOperator, is_left: bool) -> bool:
        """Check if expression needs parentheses"""
        if not isinstance(expr, LuaBinaryOperation):
            return False
        
        expr_precedence = self.operator_precedence.get(expr.operator, 0)
        parent_precedence = self.operator_precedence.get(parent_op, 0)
        
        if expr_precedence < parent_precedence:
            return True
        
        if expr_precedence == parent_precedence:
            # Right-associative operators need parens on left
            if not is_left and parent_op in self.right_associative:
                return True
            # Left-associative operators need parens on right
            if is_left and parent_op not in self.right_associative:
                return True
        
        return False
    
    def _field_is_complex(self, field: LuaTableField) -> bool:
        """Check if table field is complex enough to warrant multiline"""
        return (isinstance(field.value, (LuaTableConstructor, LuaFunctionDefinition)) or
                (field.key and isinstance(field.key, (LuaFunctionCall, LuaBinaryOperation))))
    
    def _is_valid_identifier(self, name: str) -> bool:
        """Check if string is a valid Lua identifier"""
        if not name or not (name[0].isalpha() or name[0] == '_'):
            return False
        return all(c.isalnum() or c == '_' for c in name)
    
    def _needs_spacing_between_statements(self, prev: LuaStatement, current: LuaStatement) -> bool:
        """Check if spacing is needed between statements"""
        if self.config.style == LuaFormatStyle.COMPACT:
            return False
        
        # Add spacing around function declarations
        if isinstance(current, LuaFunctionDeclaration) or isinstance(prev, LuaFunctionDeclaration):
            return True
        
        # Add spacing around control structures
        control_structures = (LuaIfStatement, LuaWhileStatement, LuaForStatement, LuaForInStatement, LuaRepeatStatement)
        if isinstance(current, control_structures) or isinstance(prev, control_structures):
            return True
        
        return False
    
    def _escape_string(self, text: str, quote: str) -> str:
        """Escape string content for given quote style"""
        text = text.replace("\\", "\\\\")
        text = text.replace("\n", "\\n")
        text = text.replace("\t", "\\t")
        text = text.replace("\r", "\\r")
        
        if quote == '"':
            text = text.replace('"', '\\"')
        elif quote == "'":
            text = text.replace("'", "\\'")
        
        return text
    
    def _write(self, text: str) -> None:
        """Write text to output"""
        self.output.write(text)
        self.current_line_length += len(text)
    
    def _write_line(self, text: str = "") -> None:
        """Write line to output"""
        if text:
            self.output.write(text)
        self.output.write("\n")
        self.current_line_length = 0
    
    def _write_indent(self) -> None:
        """Write current indentation"""
        indent = " " * (self.indent_level * self.config.indent_size)
        self.output.write(indent)
        self.current_line_length += len(indent)
    
    def _indent(self) -> None:
        """Increase indentation level"""
        self.indent_level += 1
    
    def _dedent(self) -> None:
        """Decrease indentation level"""
        if self.indent_level > 0:
            self.indent_level -= 1


class LuaFormatter:
    """Utility class for Lua code formatting"""
    
    @staticmethod
    def format_lua(code: str, style: LuaFormatStyle = LuaFormatStyle.STANDARD) -> str:
        """Format Lua code string"""
        from .lua_parser import parse_lua
        
        ast = parse_lua(code)
        generator_config = LuaGeneratorConfig(style=style)
        generator = LuaCodeGenerator(generator_config)
        
        return generator.generate(ast)
    
    @staticmethod
    def minify_lua(code: str) -> str:
        """Minify Lua code by removing unnecessary whitespace"""
        config = LuaGeneratorConfig(
            style=LuaFormatStyle.COMPACT,
            preserve_comments=False
        )
        
        from .lua_parser import parse_lua
        ast = parse_lua(code)
        generator = LuaCodeGenerator(config)
        
        return generator.generate(ast)
    
    @staticmethod
    def love2d_format(code: str) -> str:
        """Format Lua code for Love2D game development"""
        config = LuaGeneratorConfig(
            style=LuaFormatStyle.LOVE2D,
            love2d_conventions=True
        )
        
        from .lua_parser import parse_lua
        ast = parse_lua(code)
        generator = LuaCodeGenerator(config)
        
        return generator.generate(ast)


def generate_lua(node: LuaNode, style: LuaFormatStyle = LuaFormatStyle.STANDARD) -> str:
    """Generate Lua code from AST node"""
    config = LuaGeneratorConfig(style=style)
    generator = LuaCodeGenerator(config)
    return generator.generate(node)


def format_lua_code(code: str, style: LuaFormatStyle = LuaFormatStyle.STANDARD) -> str:
    """Format Lua code string"""
    return LuaFormatter.format_lua(code, style) 