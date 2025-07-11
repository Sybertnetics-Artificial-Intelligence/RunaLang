"""
Perl Code Generator for Runa Universal Translation Platform
Generates idiomatic Perl code from Perl AST

This generator produces high-quality Perl code with:
- Idiomatic Perl style and best practices
- Proper text processing constructs
- Advanced regex features
- Context-aware code generation
- CPAN module integration
- Object-oriented and procedural styles
"""

from typing import List, Optional, Dict, Any, Union
import logging
from dataclasses import dataclass

from .perl_ast import *
from ...core.generator_base import BaseGenerator, GenerationError

logger = logging.getLogger(__name__)

@dataclass
class PerlGenerationContext:
    """Context for Perl code generation"""
    indent_level: int = 0
    in_package: bool = False
    current_package: Optional[str] = None
    use_strict: bool = True
    use_warnings: bool = True
    text_processing_style: str = "modern"  # modern, classic, golf
    regex_style: str = "readable"  # readable, compact, extended
    variable_style: str = "descriptive"  # descriptive, short, perl_style
    
class PerlGenerator(BaseGenerator):
    """Generates Perl code from Perl AST"""
    
    def __init__(self):
        super().__init__()
        self.context = PerlGenerationContext()
        
        # Perl formatting preferences
        self.indent_size = 4
        self.max_line_length = 120
        self.use_modern_features = True
        
    def generate(self, node: PerlNode) -> str:
        """Generate Perl code from AST node"""
        try:
            method_name = f"_generate_{node.node_type.value}"
            if hasattr(self, method_name):
                return getattr(self, method_name)(node)
            else:
                logger.warning(f"No generator for node type: {node.node_type}")
                return f"# TODO: Generate {node.node_type.value}"
        except Exception as e:
            logger.error(f"Error generating Perl code: {e}")
            raise GenerationError(f"Failed to generate code for {node.node_type}: {e}")
    
    def _get_indent(self) -> str:
        """Get current indentation string"""
        return " " * (self.context.indent_level * self.indent_size)
    
    def _indent(self):
        """Increase indentation level"""
        self.context.indent_level += 1
    
    def _dedent(self):
        """Decrease indentation level"""
        self.context.indent_level = max(0, self.context.indent_level - 1)
    
    # Program structure generators
    
    def _generate_program(self, node: PerlProgram) -> str:
        """Generate complete Perl program"""
        lines = []
        
        # Add shebang if present
        if node.shebang:
            lines.append(node.shebang)
            lines.append("")
        
        # Add use statements
        if node.use_statements:
            for use_stmt in node.use_statements:
                lines.append(self.generate(use_stmt))
            lines.append("")
        
        # Add packages
        if node.packages:
            for package in node.packages:
                lines.append(self.generate(package))
                lines.append("")
        
        # Add main statements
        for stmt in node.statements:
            stmt_code = self.generate(stmt)
            if stmt_code.strip():
                lines.append(stmt_code)
        
        # Add final 1; for modules
        if node.packages:
            lines.append("1;")
        
        return "\n".join(lines)
    
    def _generate_package(self, node: PerlPackage) -> str:
        """Generate package declaration"""
        lines = []
        
        # Package declaration
        package_line = f"package {node.name}"
        if node.version:
            package_line += f" {node.version}"
        lines.append(package_line + ";")
        lines.append("")
        
        self.context.in_package = True
        self.context.current_package = node.name
        
        # Package statements
        for stmt in node.statements:
            lines.append(self.generate(stmt))
        
        self.context.in_package = False
        
        return "\n".join(lines)
    
    def _generate_use_statement(self, node: PerlUseStatement) -> str:
        """Generate use statement"""
        use_line = f"use {node.module_name}"
        
        if node.version:
            use_line += f" {node.version}"
        
        if node.import_list:
            imports = ", ".join(node.import_list)
            use_line += f" qw({imports})"
        elif node.arguments:
            args = ", ".join(self.generate(arg) for arg in node.arguments)
            use_line += f" ({args})"
        
        return use_line + ";"
    
    def _generate_require_statement(self, node: PerlRequireStatement) -> str:
        """Generate require statement"""
        if isinstance(node.module_name, str):
            return f"require {node.module_name};"
        else:
            module_expr = self.generate(node.module_name)
            return f"require {module_expr};"
    
    # Variable generators
    
    def _generate_scalar_variable(self, node: PerlScalarVariable) -> str:
        """Generate scalar variable"""
        name = f"${node.name}"
        if node.package and node.package != "main":
            name = f"${node.package}::{node.name}"
        return name
    
    def _generate_array_variable(self, node: PerlArrayVariable) -> str:
        """Generate array variable"""
        name = f"@{node.name}"
        if node.package and node.package != "main":
            name = f"@{node.package}::{node.name}"
        return name
    
    def _generate_hash_variable(self, node: PerlHashVariable) -> str:
        """Generate hash variable"""
        name = f"%{node.name}"
        if node.package and node.package != "main":
            name = f"%{node.package}::{node.name}"
        return name
    
    def _generate_typeglob(self, node: PerlTypeglob) -> str:
        """Generate typeglob"""
        name = f"*{node.name}"
        if node.package and node.package != "main":
            name = f"*{node.package}::{node.name}"
        return name
    
    def _generate_reference(self, node: PerlReference) -> str:
        """Generate reference"""
        expr = self.generate(node.expression)
        return f"\\{expr}"
    
    def _generate_dereference(self, node: PerlDereference) -> str:
        """Generate dereference"""
        ref = self.generate(node.reference)
        
        if node.dereference_type == "scalar":
            return f"${{{{ref}}}}"
        elif node.dereference_type == "array":
            return f"@{{{ref}}}"
        elif node.dereference_type == "hash":
            return f"%{{{ref}}}"
        elif node.dereference_type == "code":
            return f"&{{{ref}}}"
        elif node.dereference_type == "glob":
            return f"*{{{ref}}}"
        else:
            return f"${{{ref}}}"
    
    # Subroutine generators
    
    def _generate_subroutine_declaration(self, node: PerlSubroutineDeclaration) -> str:
        """Generate subroutine declaration"""
        lines = []
        
        # Subroutine signature
        sub_line = f"sub {node.name}"
        
        if node.prototype:
            sub_line += f"({node.prototype})"
        
        if node.attributes:
            attrs = " ".join(f":{attr}" for attr in node.attributes)
            sub_line += f" {attrs}"
        
        lines.append(sub_line + " {")
        
        self._indent()
        
        # Parameter extraction (if parameters are defined)
        if node.parameters:
            param_line = self._get_indent() + "my ("
            param_vars = [f"${param}" for param in node.parameters]
            param_line += ", ".join(param_vars) + ") = @_;"
            lines.append(param_line)
            lines.append("")
        
        # Subroutine body
        for stmt in node.body:
            stmt_code = self.generate(stmt)
            if stmt_code.strip():
                lines.append(self._get_indent() + stmt_code)
        
        self._dedent()
        lines.append("}")
        
        return "\n".join(lines)
    
    def _generate_subroutine_call(self, node: PerlSubroutineCall) -> str:
        """Generate subroutine call"""
        name = node.name
        if node.package:
            name = f"{node.package}::{name}"
        
        if node.ampersand_prefix:
            name = f"&{name}"
        
        if node.arguments:
            args = ", ".join(self.generate(arg) for arg in node.arguments)
            return f"{name}({args})"
        else:
            return name
    
    def _generate_anonymous_subroutine(self, node: PerlAnonymousSubroutine) -> str:
        """Generate anonymous subroutine"""
        lines = ["sub {"]
        
        self._indent()
        
        # Parameter extraction
        if node.parameters:
            param_line = self._get_indent() + "my ("
            param_vars = [f"${param}" for param in node.parameters]
            param_line += ", ".join(param_vars) + ") = @_;"
            lines.append(param_line)
            lines.append("")
        
        # Body
        for stmt in node.body:
            stmt_code = self.generate(stmt)
            if stmt_code.strip():
                lines.append(self._get_indent() + stmt_code)
        
        self._dedent()
        lines.append("}")
        
        return "\n".join(lines)
    
    # Control structure generators
    
    def _generate_if_statement(self, node: PerlIfStatement) -> str:
        """Generate if statement"""
        lines = []
        
        # If clause
        condition = self.generate(node.condition)
        lines.append(f"if ({condition}) {{")
        
        self._indent()
        for stmt in node.then_block:
            stmt_code = self.generate(stmt)
            if stmt_code.strip():
                lines.append(self._get_indent() + stmt_code)
        self._dedent()
        
        # Elsif clauses
        for elsif in node.elsif_blocks:
            elsif_condition = self.generate(elsif.condition)
            lines.append(f"}} elsif ({elsif_condition}) {{")
            
            self._indent()
            for stmt in elsif.statements:
                stmt_code = self.generate(stmt)
                if stmt_code.strip():
                    lines.append(self._get_indent() + stmt_code)
            self._dedent()
        
        # Else clause
        if node.else_block:
            lines.append("} else {")
            
            self._indent()
            for stmt in node.else_block:
                stmt_code = self.generate(stmt)
                if stmt_code.strip():
                    lines.append(self._get_indent() + stmt_code)
            self._dedent()
        
        lines.append("}")
        return "\n".join(lines)
    
    def _generate_unless_statement(self, node: PerlUnlessStatement) -> str:
        """Generate unless statement"""
        lines = []
        
        condition = self.generate(node.condition)
        lines.append(f"unless ({condition}) {{")
        
        self._indent()
        for stmt in node.then_block:
            stmt_code = self.generate(stmt)
            if stmt_code.strip():
                lines.append(self._get_indent() + stmt_code)
        self._dedent()
        
        if node.else_block:
            lines.append("} else {")
            
            self._indent()
            for stmt in node.else_block:
                stmt_code = self.generate(stmt)
                if stmt_code.strip():
                    lines.append(self._get_indent() + stmt_code)
            self._dedent()
        
        lines.append("}")
        return "\n".join(lines)
    
    def _generate_while_loop(self, node: PerlWhileLoop) -> str:
        """Generate while loop"""
        lines = []
        
        condition = self.generate(node.condition)
        lines.append(f"while ({condition}) {{")
        
        self._indent()
        for stmt in node.body:
            stmt_code = self.generate(stmt)
            if stmt_code.strip():
                lines.append(self._get_indent() + stmt_code)
        self._dedent()
        
        lines.append("}")
        return "\n".join(lines)
    
    def _generate_until_loop(self, node: PerlUntilLoop) -> str:
        """Generate until loop"""
        lines = []
        
        condition = self.generate(node.condition)
        lines.append(f"until ({condition}) {{")
        
        self._indent()
        for stmt in node.body:
            stmt_code = self.generate(stmt)
            if stmt_code.strip():
                lines.append(self._get_indent() + stmt_code)
        self._dedent()
        
        lines.append("}")
        return "\n".join(lines)
    
    def _generate_for_loop(self, node: PerlForLoop) -> str:
        """Generate C-style for loop"""
        init = self.generate(node.initialization) if node.initialization else ""
        condition = self.generate(node.condition) if node.condition else ""
        increment = self.generate(node.increment) if node.increment else ""
        
        lines = [f"for ({init}; {condition}; {increment}) {{"]
        
        self._indent()
        for stmt in node.body:
            stmt_code = self.generate(stmt)
            if stmt_code.strip():
                lines.append(self._get_indent() + stmt_code)
        self._dedent()
        
        lines.append("}")
        return "\n".join(lines)
    
    def _generate_foreach_loop(self, node: PerlForeachLoop) -> str:
        """Generate foreach loop"""
        lines = []
        
        iterable = self.generate(node.iterable)
        
        if node.variable:
            var = self.generate(node.variable)
            lines.append(f"foreach {var} ({iterable}) {{")
        else:
            lines.append(f"foreach ({iterable}) {{")
        
        self._indent()
        for stmt in node.body:
            stmt_code = self.generate(stmt)
            if stmt_code.strip():
                lines.append(self._get_indent() + stmt_code)
        self._dedent()
        
        lines.append("}")
        return "\n".join(lines)
    
    def _generate_given_when(self, node: PerlGivenWhen) -> str:
        """Generate given/when switch statement"""
        lines = []
        
        expr = self.generate(node.expression)
        lines.append(f"given ({expr}) {{")
        
        self._indent()
        
        for when_block in node.when_blocks:
            when_condition = self.generate(when_block.condition)
            lines.append(self._get_indent() + f"when ({when_condition}) {{")
            
            self._indent()
            for stmt in when_block.statements:
                stmt_code = self.generate(stmt)
                if stmt_code.strip():
                    lines.append(self._get_indent() + stmt_code)
            self._dedent()
            
            lines.append(self._get_indent() + "}")
        
        if node.default_block:
            lines.append(self._get_indent() + "default {")
            
            self._indent()
            for stmt in node.default_block:
                stmt_code = self.generate(stmt)
                if stmt_code.strip():
                    lines.append(self._get_indent() + stmt_code)
            self._dedent()
            
            lines.append(self._get_indent() + "}")
        
        self._dedent()
        lines.append("}")
        
        return "\n".join(lines)
    
    # Expression generators
    
    def _generate_assignment(self, node: PerlAssignment) -> str:
        """Generate assignment expression"""
        left = self.generate(node.left)
        right = self.generate(node.right)
        return f"{left} {node.operator} {right};"
    
    def _generate_binary_operation(self, node: PerlBinaryOperation) -> str:
        """Generate binary operation"""
        left = self.generate(node.left)
        right = self.generate(node.right)
        return f"{left} {node.operator} {right}"
    
    def _generate_unary_operation(self, node: PerlUnaryOperation) -> str:
        """Generate unary operation"""
        operand = self.generate(node.operand)
        
        if node.prefix:
            return f"{node.operator}{operand}"
        else:
            return f"{operand}{node.operator}"
    
    def _generate_ternary_operation(self, node: PerlTernaryOperation) -> str:
        """Generate ternary conditional operation"""
        condition = self.generate(node.condition)
        true_expr = self.generate(node.true_expression)
        false_expr = self.generate(node.false_expression)
        
        return f"{condition} ? {true_expr} : {false_expr}"
    
    # Regex and string generators
    
    def _generate_regex_match(self, node: PerlRegexMatch) -> str:
        """Generate regex match operation"""
        string = self.generate(node.string)
        pattern = self.generate(node.pattern)
        return f"{string} {node.operator} {pattern}"
    
    def _generate_regex_substitution(self, node: PerlRegexSubstitution) -> str:
        """Generate regex substitution"""
        string = self.generate(node.string)
        return f"{string} =~ s/{node.pattern}/{node.replacement}/{node.flags}"
    
    def _generate_regex_transliteration(self, node: PerlRegexTransliteration) -> str:
        """Generate transliteration operation"""
        string = self.generate(node.string)
        return f"{string} =~ tr/{node.search_list}/{node.replacement_list}/{node.flags}"
    
    def _generate_string_literal(self, node: PerlStringLiteral) -> str:
        """Generate string literal"""
        value = node.value.replace("\\", "\\\\").replace("\"", "\\\"")
        
        if node.quote_type == "single":
            value = value.replace("'", "\\'")
            return f"'{value}'"
        elif node.quote_type == "double":
            return f'"{value}"'
        elif node.quote_type == "qq":
            return f"qq({value})"
        elif node.quote_type == "q":
            return f"q({value})"
        else:
            return f'"{value}"'
    
    def _generate_regex_literal(self, node: PerlRegexLiteral) -> str:
        """Generate regex literal"""
        if node.flags:
            return f"/{node.pattern}/{node.flags}"
        else:
            return f"/{node.pattern}/"
    
    def _generate_here_document(self, node: PerlHereDocument) -> str:
        """Generate here document"""
        if node.interpolate:
            return f"<<{node.delimiter}\n{node.content}\n{node.delimiter}"
        else:
            return f"<<'{node.delimiter}'\n{node.content}\n{node.delimiter}"
    
    def _generate_interpolated_string(self, node: PerlInterpolatedString) -> str:
        """Generate interpolated string"""
        parts = []
        for part in node.parts:
            if isinstance(part, str):
                parts.append(part)
            else:
                parts.append(self.generate(part))
        
        return f'"{{"".join(parts)}}"'
    
    def _generate_quoted_word_list(self, node: PerlQuotedWordList) -> str:
        """Generate quoted word list"""
        words = " ".join(node.words)
        return f"qw({words})"
    
    # Data structure generators
    
    def _generate_array_literal(self, node: PerlArrayLiteral) -> str:
        """Generate array literal"""
        if not node.elements:
            return "()"
        
        elements = [self.generate(elem) for elem in node.elements]
        
        # Short array on one line
        if len(elements) <= 3:
            return f"({', '.join(elements)})"
        
        # Multi-line array
        lines = ["("]
        self._indent()
        for elem in elements:
            lines.append(self._get_indent() + elem + ",")
        self._dedent()
        lines.append(")")
        
        return "\n".join(lines)
    
    def _generate_hash_literal(self, node: PerlHashLiteral) -> str:
        """Generate hash literal"""
        if not node.pairs:
            return "()"
        
        pairs = []
        for pair in node.pairs:
            key = self.generate(pair.key)
            value = self.generate(pair.value)
            
            # Use fat comma for bareword keys
            if isinstance(pair.key, PerlBareword):
                pairs.append(f"{key} => {value}")
            else:
                pairs.append(f"{key} => {value}")
        
        # Short hash on one line
        if len(pairs) <= 2:
            return f"({', '.join(pairs)})"
        
        # Multi-line hash
        lines = ["("]
        self._indent()
        for pair in pairs:
            lines.append(self._get_indent() + pair + ",")
        self._dedent()
        lines.append(")")
        
        return "\n".join(lines)
    
    def _generate_array_slice(self, node: PerlArraySlice) -> str:
        """Generate array slice"""
        array = self.generate(node.array)
        indices = [self.generate(idx) for idx in node.indices]
        
        if len(indices) == 1:
            return f"{array}[{indices[0]}]"
        else:
            return f"{array}[{', '.join(indices)}]"
    
    def _generate_hash_slice(self, node: PerlHashSlice) -> str:
        """Generate hash slice"""
        hash_ref = self.generate(node.hash)
        keys = [self.generate(key) for key in node.keys]
        
        if len(keys) == 1:
            return f"{hash_ref}{{{keys[0]}}}"
        else:
            return f"@{hash_ref}{{{', '.join(keys)}}}"
    
    # I/O and special generators
    
    def _generate_print_statement(self, node: PerlPrintStatement) -> str:
        """Generate print statement"""
        if node.filehandle:
            fh = self.generate(node.filehandle)
            if node.arguments:
                args = ", ".join(self.generate(arg) for arg in node.arguments)
                return f"print {fh} {args};"
            else:
                return f"print {fh};"
        else:
            if node.arguments:
                args = ", ".join(self.generate(arg) for arg in node.arguments)
                return f"print {args};"
            else:
                return "print;"
    
    def _generate_open_statement(self, node: PerlOpenStatement) -> str:
        """Generate open statement"""
        fh = self.generate(node.filehandle)
        filename = self.generate(node.filename)
        return f"open({fh}, '{node.mode}', {filename});"
    
    def _generate_readline(self, node: PerlReadline) -> str:
        """Generate readline operation"""
        if node.filehandle:
            fh = self.generate(node.filehandle)
            return f"<{fh}>"
        else:
            return "<>"
    
    def _generate_filehandle(self, node: PerlFilehandle) -> str:
        """Generate filehandle"""
        return node.name
    
    # Object-oriented generators
    
    def _generate_bless_expression(self, node: PerlBlessExpression) -> str:
        """Generate bless expression"""
        ref = self.generate(node.reference)
        
        if node.class_name:
            class_name = self.generate(node.class_name)
            return f"bless {ref}, {class_name}"
        else:
            return f"bless {ref}"
    
    def _generate_method_call(self, node: PerlMethodCall) -> str:
        """Generate method call"""
        obj = self.generate(node.object)
        
        if node.arguments:
            args = ", ".join(self.generate(arg) for arg in node.arguments)
            return f"{obj}->{node.method}({args})"
        else:
            return f"{obj}->{node.method}"
    
    # Special construct generators
    
    def _generate_eval_expression(self, node: PerlEvalExpression) -> str:
        """Generate eval expression"""
        if node.is_string_eval:
            if isinstance(node.expression, str):
                return f'eval "{node.expression}"'
            else:
                expr = self.generate(node.expression)
                return f"eval {expr}"
        else:
            expr = self.generate(node.expression)
            return f"eval {{ {expr} }}"
    
    def _generate_special_variable(self, node: PerlSpecialVariable) -> str:
        """Generate special variable"""
        return node.name
    
    def _generate_magic_variable(self, node: PerlMagicVariable) -> str:
        """Generate magic variable"""
        return node.name
    
    def _generate_format_statement(self, node: PerlFormatStatement) -> str:
        """Generate format statement"""
        lines = [f"format {node.name} ="]
        lines.extend(node.format_lines)
        lines.append(".")
        return "\n".join(lines)
    
    # Literal generators
    
    def _generate_numeric_literal(self, node: PerlNumericLiteral) -> str:
        """Generate numeric literal"""
        if node.base == 16:
            return f"0x{format(int(node.value), 'x')}"
        elif node.base == 8:
            return f"0{format(int(node.value), 'o')}"
        elif node.base == 2:
            return f"0b{format(int(node.value), 'b')}"
        else:
            return str(node.value)
    
    def _generate_identifier(self, node: PerlIdentifier) -> str:
        """Generate identifier"""
        return node.name
    
    def _generate_bareword(self, node: PerlBareword) -> str:
        """Generate bareword"""
        return node.name
    
    # Utility methods
    
    def set_style(self, style: str):
        """Set code generation style (modern, classic, golf)"""
        self.context.text_processing_style = style
    
    def set_regex_style(self, style: str):
        """Set regex generation style (readable, compact, extended)"""
        self.context.regex_style = style
    
    def enable_modern_features(self):
        """Enable modern Perl features"""
        self.use_modern_features = True 