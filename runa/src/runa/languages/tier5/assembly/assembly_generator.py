"""
Assembly Code Generator - Generates Assembly source code from Assembly AST.

This module provides comprehensive code generation for Assembly language,
supporting multiple architectures and instruction formats with proper formatting.
"""

from typing import Any, Dict, List, Optional, TextIO, Union
from dataclasses import dataclass
import io

from .assembly_ast import *


@dataclass
class AssemblyCodeStyle:
    """Configuration for Assembly code generation style."""
    instruction_format: str = "intel"  # intel, at&t
    indent_size: int = 4
    use_tabs: bool = False
    mnemonic_case: str = "lower"  # lower, upper
    register_case: str = "lower"  # lower, upper
    comment_style: str = "semicolon"  # semicolon, hash, slash
    label_colon: bool = True
    operand_spacing: str = ", "  # ", " or ","
    align_comments: bool = True
    comment_column: int = 40
    include_line_numbers: bool = False
    max_line_length: int = 120
    preserve_blank_lines: bool = True
    section_spacing: int = 2
    instruction_spacing: int = 1


class AssemblyCodeGenerator:
    """Generates Assembly source code from Assembly AST."""
    
    def __init__(self, style: Optional[AssemblyCodeStyle] = None):
        self.style = style or AssemblyCodeStyle()
        self.output = io.StringIO()
        self.current_line = 0
        self.current_column = 0
        self.indent_level = 0
        self.in_section = False
        self.label_table: Dict[str, int] = {}
        self.comment_buffer: List[str] = []
    
    def generate(self, node: AssemblyNode) -> str:
        """Generate Assembly code from AST node."""
        self.output = io.StringIO()
        self.current_line = 0
        self.current_column = 0
        self.indent_level = 0
        self.in_section = False
        self.label_table.clear()
        self.comment_buffer.clear()
        
        try:
            self._generate_node(node)
            return self.output.getvalue()
        except Exception as e:
            # Return error as comment
            return f"; Error generating Assembly code: {str(e)}\n"
    
    def generate_to_file(self, node: AssemblyNode, filename: str) -> None:
        """Generate Assembly code and write to file."""
        code = self.generate(node)
        with open(filename, 'w') as f:
            f.write(code)
    
    def _generate_node(self, node: AssemblyNode) -> None:
        """Generate code for specific node types."""
        if isinstance(node, ProgramNode):
            self._generate_program(node)
        elif isinstance(node, InstructionNode):
            self._generate_instruction(node)
        elif isinstance(node, LabelNode):
            self._generate_label(node)
        elif isinstance(node, DirectiveNode):
            self._generate_directive(node)
        elif isinstance(node, SectionNode):
            self._generate_section(node)
        elif isinstance(node, CommentNode):
            self._generate_comment(node)
        elif isinstance(node, MacroNode):
            self._generate_macro(node)
        elif isinstance(node, ConditionalNode):
            self._generate_conditional(node)
        elif isinstance(node, DataDefinitionNode):
            self._generate_data_definition(node)
        elif isinstance(node, list):
            for item in node:
                self._generate_node(item)
        else:
            self._write_comment(f"Unsupported node type: {type(node).__name__}")
    
    def _generate_program(self, node: ProgramNode) -> None:
        """Generate complete program."""
        # Add header comment if configured
        if hasattr(self.style, 'include_header') and self.style.include_header:
            self._write_comment("Generated Assembly Code")
            self._write_comment(f"Format: {self.style.instruction_format}")
            self._write_newline()
        
        for item in node.items:
            self._generate_node(item)
            
            # Add spacing between major sections
            if isinstance(item, (SectionNode, MacroNode)):
                for _ in range(self.style.section_spacing):
                    self._write_newline()
            elif isinstance(item, LabelNode):
                for _ in range(self.style.instruction_spacing):
                    self._write_newline()
    
    def _generate_instruction(self, node: InstructionNode) -> None:
        """Generate instruction."""
        # Flush any pending comments
        self._flush_comment_buffer()
        
        # Format mnemonic
        mnemonic = node.mnemonic
        if self.style.mnemonic_case == "upper":
            mnemonic = mnemonic.upper()
        elif self.style.mnemonic_case == "lower":
            mnemonic = mnemonic.lower()
        
        # Write indent
        self._write_indent()
        
        # Write mnemonic
        self._write(mnemonic)
        
        # Write operands if present
        if node.operands:
            self._write(" ")
            
            operand_strings = []
            for operand in node.operands:
                operand_str = self._format_operand(operand)
                operand_strings.append(operand_str)
            
            self._write(self.style.operand_spacing.join(operand_strings))
        
        # Add instruction comment if present
        if hasattr(node, 'comment') and node.comment:
            self._write_aligned_comment(node.comment)
        
        self._write_newline()
    
    def _generate_label(self, node: LabelNode) -> None:
        """Generate label."""
        # Labels typically don't have indentation
        label_str = node.name
        if self.style.label_colon:
            label_str += ":"
        
        self._write(label_str)
        self._write_newline()
        
        # Store label position
        self.label_table[node.name] = self.current_line
    
    def _generate_directive(self, node: DirectiveNode) -> None:
        """Generate assembler directive."""
        self._write_indent()
        
        # Format directive (usually starts with . or %)
        if self.style.instruction_format == "intel":
            directive = f".{node.name}"
        else:  # AT&T
            directive = f".{node.name}"
        
        self._write(directive)
        
        # Write arguments
        if node.args:
            self._write(" ")
            arg_strings = []
            for arg in node.args:
                if isinstance(arg, str):
                    arg_strings.append(arg)
                elif isinstance(arg, AssemblyNode):
                    arg_strings.append(self._format_operand(arg))
                else:
                    arg_strings.append(str(arg))
            
            self._write(self.style.operand_spacing.join(arg_strings))
        
        self._write_newline()
    
    def _generate_section(self, node: SectionNode) -> None:
        """Generate section."""
        # Section directive
        if self.style.instruction_format == "intel":
            section_directive = f".section {node.name}"
        else:  # AT&T
            section_directive = f".section {node.name}"
        
        self._write(section_directive)
        
        if node.section_type:
            self._write(f", \"{node.section_type}\"")
        
        self._write_newline()
        self._write_newline()
        
        # Mark that we're in a section for indentation
        old_in_section = self.in_section
        self.in_section = True
        
        # Generate section contents
        for item in node.contents:
            self._generate_node(item)
        
        self.in_section = old_in_section
        self._write_newline()
    
    def _generate_comment(self, node: CommentNode) -> None:
        """Generate comment."""
        comment_prefix = self._get_comment_prefix()
        
        # Handle multi-line comments
        lines = node.text.split('\n')
        for line in lines:
            self._write_indent()
            self._write(f"{comment_prefix} {line.strip()}")
            self._write_newline()
    
    def _generate_macro(self, node: MacroNode) -> None:
        """Generate macro definition."""
        # Macro directive
        self._write(f".macro {node.name}")
        
        # Parameters
        if node.parameters:
            self._write(" ")
            self._write(", ".join(node.parameters))
        
        self._write_newline()
        
        # Increase indent for macro body
        self.indent_level += 1
        
        # Generate macro body
        for stmt in node.body:
            self._generate_node(stmt)
        
        # Decrease indent
        self.indent_level -= 1
        
        # End macro
        self._write(".endm")
        self._write_newline()
    
    def _generate_conditional(self, node: ConditionalNode) -> None:
        """Generate conditional assembly."""
        # Conditional directive
        self._write(f".if ")
        condition_str = self._format_operand(node.condition)
        self._write(condition_str)
        self._write_newline()
        
        # Increase indent
        self.indent_level += 1
        
        # Generate then block
        for stmt in node.then_block:
            self._generate_node(stmt)
        
        # Else block if present
        if node.else_block:
            self.indent_level -= 1
            self._write(".else")
            self._write_newline()
            self.indent_level += 1
            
            for stmt in node.else_block:
                self._generate_node(stmt)
        
        # End conditional
        self.indent_level -= 1
        self._write(".endif")
        self._write_newline()
    
    def _generate_data_definition(self, node: DataDefinitionNode) -> None:
        """Generate data definition."""
        self._write_indent()
        
        # Data directive based on type
        directive_map = {
            "db": ".byte",
            "dw": ".word", 
            "dd": ".long",
            "dq": ".quad",
            "ascii": ".ascii",
            "asciz": ".asciz"
        }
        
        directive = directive_map.get(node.data_type, f".{node.data_type}")
        self._write(directive)
        self._write(" ")
        
        # Format values
        value_strings = []
        for value in node.values:
            if isinstance(value, str):
                # String literal
                value_strings.append(f'"{value}"')
            elif isinstance(value, (int, float)):
                value_strings.append(str(value))
            elif isinstance(value, AssemblyNode):
                value_strings.append(self._format_operand(value))
            else:
                value_strings.append(str(value))
        
        self._write(self.style.operand_spacing.join(value_strings))
        self._write_newline()
    
    def _format_operand(self, operand: AssemblyNode) -> str:
        """Format operand for output."""
        if isinstance(operand, RegisterNode):
            return self._format_register(operand)
        elif isinstance(operand, ImmediateNode):
            return self._format_immediate(operand)
        elif isinstance(operand, MemoryNode):
            return self._format_memory(operand)
        elif isinstance(operand, LabelRefNode):
            return self._format_label_ref(operand)
        elif isinstance(operand, ExpressionNode):
            return self._format_expression(operand)
        else:
            return str(operand)
    
    def _format_register(self, node: RegisterNode) -> str:
        """Format register operand."""
        reg_name = node.name
        
        if self.style.register_case == "upper":
            reg_name = reg_name.upper()
        elif self.style.register_case == "lower":
            reg_name = reg_name.lower()
        
        if self.style.instruction_format == "at&t":
            return f"%{reg_name}"
        else:  # Intel
            return reg_name
    
    def _format_immediate(self, node: ImmediateNode) -> str:
        """Format immediate operand."""
        value_str = str(node.value)
        
        if self.style.instruction_format == "at&t":
            return f"${value_str}"
        else:  # Intel
            return value_str
    
    def _format_memory(self, node: MemoryNode) -> str:
        """Format memory operand."""
        if self.style.instruction_format == "intel":
            return self._format_memory_intel(node)
        else:  # AT&T
            return self._format_memory_att(node)
    
    def _format_memory_intel(self, node: MemoryNode) -> str:
        """Format memory operand in Intel syntax."""
        parts = []
        
        # Size prefix
        if node.size:
            size_map = {8: "byte", 16: "word", 32: "dword", 64: "qword"}
            size_prefix = size_map.get(node.size, "")
            if size_prefix:
                parts.append(f"{size_prefix} ptr")
        
        # Build address expression
        address_parts = []
        
        if node.base:
            address_parts.append(self._format_operand(node.base))
        
        if node.index:
            index_str = self._format_operand(node.index)
            if node.scale and node.scale > 1:
                index_str += f"*{node.scale}"
            address_parts.append(index_str)
        
        if node.displacement:
            if node.displacement > 0 and address_parts:
                address_parts.append(f"+{node.displacement}")
            else:
                address_parts.append(str(node.displacement))
        
        if address_parts:
            address_expr = "".join(address_parts)
        else:
            address_expr = "0"
        
        parts.append(f"[{address_expr}]")
        return " ".join(parts)
    
    def _format_memory_att(self, node: MemoryNode) -> str:
        """Format memory operand in AT&T syntax."""
        # AT&T: displacement(base,index,scale)
        displacement = node.displacement or 0
        base_str = ""
        if node.base:
            base_str = self._format_operand(node.base)
        
        index_str = ""
        if node.index:
            index_str = self._format_operand(node.index)
        
        scale = node.scale or 1
        
        if base_str and index_str:
            return f"{displacement}({base_str},{index_str},{scale})"
        elif base_str:
            return f"{displacement}({base_str})"
        elif index_str:
            return f"{displacement}(,{index_str},{scale})"
        else:
            return str(displacement)
    
    def _format_label_ref(self, node: LabelRefNode) -> str:
        """Format label reference."""
        return node.label
    
    def _format_expression(self, node: ExpressionNode) -> str:
        """Format expression operand."""
        if node.operator:
            left_str = self._format_operand(node.left)
            right_str = self._format_operand(node.right)
            return f"({left_str} {node.operator} {right_str})"
        else:
            return self._format_operand(node.left)
    
    def _write(self, text: str) -> None:
        """Write text to output."""
        self.output.write(text)
        self.current_column += len(text)
    
    def _write_newline(self) -> None:
        """Write newline to output."""
        self.output.write('\n')
        self.current_line += 1
        self.current_column = 0
    
    def _write_indent(self) -> None:
        """Write appropriate indentation."""
        if self.in_section:
            indent = self.indent_level + 1
        else:
            indent = self.indent_level
        
        if self.style.use_tabs:
            self._write('\t' * indent)
        else:
            self._write(' ' * (indent * self.style.indent_size))
    
    def _write_comment(self, text: str) -> None:
        """Write comment with proper formatting."""
        comment_prefix = self._get_comment_prefix()
        self._write(f"{comment_prefix} {text}")
        self._write_newline()
    
    def _write_aligned_comment(self, text: str) -> None:
        """Write comment aligned to comment column."""
        if self.style.align_comments:
            # Pad to comment column
            while self.current_column < self.style.comment_column:
                self._write(' ')
        else:
            self._write(' ')
        
        comment_prefix = self._get_comment_prefix()
        self._write(f"{comment_prefix} {text}")
    
    def _get_comment_prefix(self) -> str:
        """Get comment prefix based on style."""
        if self.style.comment_style == "semicolon":
            return ";"
        elif self.style.comment_style == "hash":
            return "#"
        elif self.style.comment_style == "slash":
            return "//"
        else:
            return ";"
    
    def _flush_comment_buffer(self) -> None:
        """Flush any buffered comments."""
        for comment in self.comment_buffer:
            self._write_comment(comment)
        self.comment_buffer.clear()


class AssemblyFormatter:
    """Formats existing Assembly code according to style rules."""
    
    def __init__(self, style: Optional[AssemblyCodeStyle] = None):
        self.style = style or AssemblyCodeStyle()
    
    def format_code(self, code: str) -> str:
        """Format Assembly code string."""
        lines = code.split('\n')
        formatted_lines = []
        
        for line in lines:
            formatted_line = self._format_line(line)
            formatted_lines.append(formatted_line)
        
        return '\n'.join(formatted_lines)
    
    def _format_line(self, line: str) -> str:
        """Format a single line of Assembly code."""
        line = line.strip()
        
        if not line:
            return line
        
        # Comment line
        if line.startswith(';') or line.startswith('#') or line.startswith('//'):
            return self._format_comment_line(line)
        
        # Label line
        if line.endswith(':') and not line.startswith('.'):
            return self._format_label_line(line)
        
        # Directive line
        if line.startswith('.') or line.startswith('%'):
            return self._format_directive_line(line)
        
        # Instruction line
        return self._format_instruction_line(line)
    
    def _format_comment_line(self, line: str) -> str:
        """Format comment line."""
        # Extract comment text
        for prefix in [';', '#', '//']:
            if line.startswith(prefix):
                text = line[len(prefix):].strip()
                return f"{self._get_comment_prefix()} {text}"
        return line
    
    def _format_label_line(self, line: str) -> str:
        """Format label line."""
        label = line.rstrip(':').strip()
        if self.style.label_colon:
            return f"{label}:"
        else:
            return label
    
    def _format_directive_line(self, line: str) -> str:
        """Format directive line."""
        # Add proper indentation
        indent = ' ' * self.style.indent_size if not self.style.use_tabs else '\t'
        return f"{indent}{line}"
    
    def _format_instruction_line(self, line: str) -> str:
        """Format instruction line."""
        parts = line.split()
        if not parts:
            return line
        
        # Extract mnemonic
        mnemonic = parts[0]
        if self.style.mnemonic_case == "upper":
            mnemonic = mnemonic.upper()
        elif self.style.mnemonic_case == "lower":
            mnemonic = mnemonic.lower()
        
        # Format operands
        operands = []
        if len(parts) > 1:
            operand_text = ' '.join(parts[1:])
            # Simple operand splitting (could be more sophisticated)
            operands = [op.strip() for op in operand_text.split(',')]
        
        # Build formatted instruction
        indent = ' ' * self.style.indent_size if not self.style.use_tabs else '\t'
        formatted = f"{indent}{mnemonic}"
        
        if operands:
            formatted += f" {self.style.operand_spacing.join(operands)}"
        
        return formatted
    
    def _get_comment_prefix(self) -> str:
        """Get comment prefix based on style."""
        if self.style.comment_style == "semicolon":
            return ";"
        elif self.style.comment_style == "hash":
            return "#"
        elif self.style.comment_style == "slash":
            return "//"
        else:
            return ";"


class AssemblyOptimizer:
    """Performs basic Assembly code optimizations."""
    
    def __init__(self):
        self.peephole_patterns = [
            # mov rax, rbx; mov rbx, rax -> xchg rax, rbx
            (["mov {r1}, {r2}", "mov {r2}, {r1}"], ["xchg {r1}, {r2}"]),
            
            # add rax, 0 -> nop (remove)
            (["add {r}, 0"], []),
            
            # sub rax, 0 -> nop (remove)  
            (["sub {r}, 0"], []),
            
            # mov rax, rax -> nop (remove)
            (["mov {r}, {r}"], []),
            
            # push rax; pop rax -> nop (remove both)
            (["push {r}", "pop {r}"], []),
        ]
    
    def optimize(self, node: AssemblyNode) -> AssemblyNode:
        """Apply optimizations to Assembly AST."""
        if isinstance(node, ProgramNode):
            return self._optimize_program(node)
        elif isinstance(node, list):
            return [self.optimize(item) for item in node if item is not None]
        else:
            return node
    
    def _optimize_program(self, node: ProgramNode) -> ProgramNode:
        """Optimize program node."""
        optimized_items = []
        i = 0
        
        while i < len(node.items):
            item = node.items[i]
            
            if isinstance(item, InstructionNode):
                # Try peephole optimizations
                consumed, replacement = self._try_peephole_optimization(node.items, i)
                if consumed > 0:
                    # Pattern matched, add replacement instructions
                    optimized_items.extend(replacement)
                    i += consumed
                else:
                    # No optimization, keep original
                    optimized_items.append(item)
                    i += 1
            else:
                optimized_items.append(item)
                i += 1
        
        return ProgramNode(optimized_items)
    
    def _try_peephole_optimization(self, items: List[AssemblyNode], start: int) -> Tuple[int, List[InstructionNode]]:
        """Try to apply peephole optimization starting at given index."""
        for pattern, replacement in self.peephole_patterns:
            match, consumed = self._match_pattern(items, start, pattern)
            if match:
                # Apply replacement with matched variables
                new_instructions = []
                for repl_template in replacement:
                    new_instr = self._apply_template(repl_template, match)
                    new_instructions.append(new_instr)
                return consumed, new_instructions
        
        return 0, []
    
    def _match_pattern(self, items: List[AssemblyNode], start: int, pattern: List[str]) -> Tuple[Optional[Dict[str, str]], int]:
        """Try to match instruction pattern."""
        if start + len(pattern) > len(items):
            return None, 0
        
        variables = {}
        
        for i, template in enumerate(pattern):
            item = items[start + i]
            if not isinstance(item, InstructionNode):
                return None, 0
            
            if not self._match_instruction(item, template, variables):
                return None, 0
        
        return variables, len(pattern)
    
    def _match_instruction(self, instr: InstructionNode, template: str, variables: Dict[str, str]) -> bool:
        """Try to match single instruction against template."""
        # Simple template matching (could be more sophisticated)
        template_parts = template.split()
        if len(template_parts) == 0:
            return False
        
        # Check mnemonic
        if template_parts[0] != instr.mnemonic:
            return False
        
        # Check operands
        if len(template_parts) > 1:
            operand_template = ' '.join(template_parts[1:])
            operand_actual = ', '.join(str(op) for op in instr.operands)
            
            return self._match_operands(operand_actual, operand_template, variables)
        
        return True
    
    def _match_operands(self, actual: str, template: str, variables: Dict[str, str]) -> bool:
        """Match operands with variable substitution."""
        # Simple variable matching
        import re
        
        # Replace variables in template with regex patterns
        pattern = template
        variable_pattern = r'\{(\w+)\}'
        
        def replace_var(match):
            var_name = match.group(1)
            return f'(?P<{var_name}>\\w+)'
        
        pattern = re.sub(variable_pattern, replace_var, pattern)
        
        match = re.match(pattern, actual)
        if match:
            # Store matched variables
            variables.update(match.groupdict())
            return True
        
        return False
    
    def _apply_template(self, template: str, variables: Dict[str, str]) -> InstructionNode:
        """Apply variable substitutions to instruction template."""
        # Replace variables in template
        result = template
        for var_name, var_value in variables.items():
            result = result.replace(f'{{{var_name}}}', var_value)
        
        # Parse result back to instruction
        parts = result.split()
        mnemonic = parts[0]
        
        operands = []
        if len(parts) > 1:
            operand_text = ' '.join(parts[1:])
            # Simple operand parsing
            operand_strs = [op.strip() for op in operand_text.split(',')]
            for op_str in operand_strs:
                # Create appropriate operand node (simplified)
                if op_str.isdigit():
                    operands.append(ImmediateNode(int(op_str)))
                else:
                    operands.append(RegisterNode(op_str))
        
        return InstructionNode(mnemonic, operands) 