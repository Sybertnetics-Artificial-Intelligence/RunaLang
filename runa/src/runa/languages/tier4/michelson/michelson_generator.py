"""
Michelson Code Generator for producing idiomatic stack-based smart contract code.

This module generates properly formatted Michelson code from AST nodes,
optimizing for readability and gas efficiency.
"""

from typing import List, Dict, Any, Optional, Union
from .michelson_ast import *


class MichelsonGeneratorError(Exception):
    """Exception raised during Michelson code generation."""
    pass


class MichelsonGenerator:
    """Generates Michelson source code from AST."""
    
    def __init__(self, indent_size: int = 2, optimize: bool = True):
        self.indent_size = indent_size
        self.optimize = optimize
        self.current_indent = 0
        self.output_lines = []
    
    def indent(self) -> str:
        """Get current indentation string."""
        return " " * (self.current_indent * self.indent_size)
    
    def emit_line(self, line: str = ""):
        """Emit a line with current indentation."""
        if line.strip():
            self.output_lines.append(self.indent() + line.strip())
        else:
            self.output_lines.append("")
    
    def emit_inline(self, text: str):
        """Emit text without newline."""
        if not self.output_lines:
            self.output_lines.append("")
        
        if self.output_lines[-1]:
            self.output_lines[-1] += " " + text.strip()
        else:
            self.output_lines[-1] = self.indent() + text.strip()
    
    def push_indent(self):
        """Increase indentation level."""
        self.current_indent += 1
    
    def pop_indent(self):
        """Decrease indentation level."""
        self.current_indent = max(0, self.current_indent - 1)
    
    def generate_type(self, type_node: MichelsonType_Node) -> str:
        """Generate Michelson type representation."""
        if not type_node.args:
            return type_node.type_name.value
        
        # Compound types with arguments
        if type_node.type_name in [MichelsonType.PAIR, MichelsonType.OR]:
            args_str = " ".join(self.generate_type(arg) for arg in type_node.args)
            return f"({type_node.type_name.value} {args_str})"
        
        elif type_node.type_name in [MichelsonType.OPTION, MichelsonType.LIST, MichelsonType.SET]:
            inner_type = self.generate_type(type_node.args[0])
            return f"({type_node.type_name.value} {inner_type})"
        
        elif type_node.type_name in [MichelsonType.MAP, MichelsonType.BIG_MAP]:
            if len(type_node.args) >= 2:
                key_type = self.generate_type(type_node.args[0])
                value_type = self.generate_type(type_node.args[1])
                return f"({type_node.type_name.value} {key_type} {value_type})"
        
        elif type_node.type_name == MichelsonType.LAMBDA:
            if len(type_node.args) >= 2:
                param_type = self.generate_type(type_node.args[0])
                return_type = self.generate_type(type_node.args[1])
                return f"(lambda {param_type} {return_type})"
        
        elif type_node.type_name == MichelsonType.CONTRACT:
            if type_node.args:
                param_type = self.generate_type(type_node.args[0])
                return f"(contract {param_type})"
        
        # Default fallback
        return type_node.type_name.value
    
    def generate_literal(self, literal: MichelsonLiteral) -> str:
        """Generate literal value representation."""
        if isinstance(literal.value, str):
            # String literals need quotes
            if literal.type_hint == MichelsonType.STRING:
                return f'"{literal.value}"'
            elif literal.type_hint == MichelsonType.BYTES:
                return literal.value  # Bytes are already in 0x format
            else:
                return f'"{literal.value}"'
        
        elif isinstance(literal.value, int):
            return str(literal.value)
        
        elif isinstance(literal.value, bool):
            return "True" if literal.value else "False"
        
        else:
            return str(literal.value)
    
    def generate_instruction_args(self, instruction: MichelsonInstruction_Node) -> str:
        """Generate instruction arguments."""
        if not instruction.args:
            return ""
        
        arg_strs = []
        for arg in instruction.args:
            if isinstance(arg, MichelsonType_Node):
                arg_strs.append(self.generate_type(arg))
            elif isinstance(arg, MichelsonLiteral):
                arg_strs.append(self.generate_literal(arg))
            elif isinstance(arg, MichelsonInstruction_Node):
                arg_strs.append(self.generate_instruction(arg))
            elif isinstance(arg, MichelsonSequence):
                arg_strs.append(self.generate_sequence_inline(arg))
            else:
                arg_strs.append(str(arg))
        
        return " ".join(arg_strs)
    
    def generate_instruction(self, instruction: MichelsonInstruction_Node) -> str:
        """Generate a single instruction."""
        args_str = self.generate_instruction_args(instruction)
        
        if args_str:
            return f"{instruction.instruction.value} {args_str}"
        else:
            return instruction.instruction.value
    
    def generate_sequence_inline(self, sequence: MichelsonSequence) -> str:
        """Generate a sequence of instructions inline (in braces)."""
        if not sequence.instructions:
            return "{}"
        
        if len(sequence.instructions) == 1:
            # Single instruction can be inline
            inner = self.generate_instruction(sequence.instructions[0])
            return f"{{ {inner} }}"
        
        # Multiple instructions - use multi-line format
        lines = ["{"]
        for instr in sequence.instructions:
            lines.append(f"  {self.generate_instruction(instr)} ;")
        
        # Remove semicolon from last instruction
        if lines[-1].endswith(" ;"):
            lines[-1] = lines[-1][:-2]
        
        lines.append("}")
        return "\n".join(lines)
    
    def generate_sequence(self, sequence: MichelsonSequence):
        """Generate a sequence of instructions with proper formatting."""
        if not sequence.instructions:
            self.emit_line("{}")
            return
        
        self.emit_line("{")
        self.push_indent()
        
        for i, instruction in enumerate(sequence.instructions):
            instr_str = self.generate_instruction(instruction)
            
            # Add semicolon to all but the last instruction
            if i < len(sequence.instructions) - 1:
                instr_str += " ;"
            
            self.emit_line(instr_str)
        
        self.pop_indent()
        self.emit_line("}")
    
    def generate_pair(self, pair: MichelsonPair) -> str:
        """Generate a pair value."""
        left_str = self.generate_node_value(pair.left)
        right_str = self.generate_node_value(pair.right)
        return f"(Pair {left_str} {right_str})"
    
    def generate_left(self, left: MichelsonLeft) -> str:
        """Generate a Left variant."""
        value_str = self.generate_node_value(left.value)
        return f"(Left {value_str})"
    
    def generate_right(self, right: MichelsonRight) -> str:
        """Generate a Right variant."""
        value_str = self.generate_node_value(right.value)
        return f"(Right {value_str})"
    
    def generate_some(self, some: MichelsonSome) -> str:
        """Generate a Some option."""
        value_str = self.generate_node_value(some.value)
        return f"(Some {value_str})"
    
    def generate_none(self, none: MichelsonNone) -> str:
        """Generate a None option."""
        type_str = self.generate_type(none.type_annotation)
        return f"(None {type_str})"
    
    def generate_list(self, list_node: MichelsonList) -> str:
        """Generate a list value."""
        if not list_node.elements:
            return "{}"
        
        element_strs = []
        for element in list_node.elements:
            element_strs.append(self.generate_node_value(element))
        
        return "{ " + " ; ".join(element_strs) + " }"
    
    def generate_set(self, set_node: MichelsonSet) -> str:
        """Generate a set value."""
        if not set_node.elements:
            return "{}"
        
        element_strs = []
        for element in set_node.elements:
            element_strs.append(self.generate_node_value(element))
        
        return "{ " + " ; ".join(element_strs) + " }"
    
    def generate_map(self, map_node: MichelsonMap) -> str:
        """Generate a map value."""
        if not map_node.entries:
            return "{}"
        
        entry_strs = []
        for entry in map_node.entries:
            if isinstance(entry, MichelsonPair):
                key_str = self.generate_node_value(entry.left)
                value_str = self.generate_node_value(entry.right)
                entry_strs.append(f"Elt {key_str} {value_str}")
        
        return "{ " + " ; ".join(entry_strs) + " }"
    
    def generate_lambda(self, lambda_node: MichelsonLambda) -> str:
        """Generate a lambda function."""
        param_type = self.generate_type(lambda_node.param_type)
        return_type = self.generate_type(lambda_node.return_type)
        body = self.generate_sequence_inline(lambda_node.body)
        
        return f"(lambda {param_type} {return_type} {body})"
    
    def generate_node_value(self, node: MichelsonNode) -> str:
        """Generate value representation for any node."""
        if isinstance(node, MichelsonLiteral):
            return self.generate_literal(node)
        elif isinstance(node, MichelsonPair):
            return self.generate_pair(node)
        elif isinstance(node, MichelsonLeft):
            return self.generate_left(node)
        elif isinstance(node, MichelsonRight):
            return self.generate_right(node)
        elif isinstance(node, MichelsonSome):
            return self.generate_some(node)
        elif isinstance(node, MichelsonNone):
            return self.generate_none(node)
        elif isinstance(node, MichelsonList):
            return self.generate_list(node)
        elif isinstance(node, MichelsonSet):
            return self.generate_set(node)
        elif isinstance(node, MichelsonMap):
            return self.generate_map(node)
        elif isinstance(node, MichelsonLambda):
            return self.generate_lambda(node)
        else:
            return str(node)
    
    def generate_contract(self, contract: MichelsonContract):
        """Generate a complete Michelson contract."""
        # Parameter section
        param_type_str = self.generate_type(contract.parameter_type)
        self.emit_line(f"parameter {param_type_str} ;")
        self.emit_line()
        
        # Storage section
        storage_type_str = self.generate_type(contract.storage_type)
        self.emit_line(f"storage {storage_type_str} ;")
        self.emit_line()
        
        # Code section
        self.emit_line("code")
        self.generate_sequence(contract.code)
    
    def optimize_instructions(self, instructions: List[MichelsonInstruction_Node]) -> List[MichelsonInstruction_Node]:
        """Apply basic optimizations to instruction sequence."""
        if not self.optimize or not instructions:
            return instructions
        
        optimized = []
        i = 0
        
        while i < len(instructions):
            current = instructions[i]
            
            # Optimization: DUP followed by DROP = no-op
            if (i + 1 < len(instructions) and
                current.instruction == MichelsonInstruction.DUP and
                instructions[i + 1].instruction == MichelsonInstruction.DROP):
                # Skip both instructions
                i += 2
                continue
            
            # Optimization: PUSH followed by DROP = no-op
            if (i + 1 < len(instructions) and
                current.instruction == MichelsonInstruction.PUSH and
                instructions[i + 1].instruction == MichelsonInstruction.DROP):
                # Skip both instructions
                i += 2
                continue
            
            # Optimization: Multiple DROP instructions can be combined
            if current.instruction == MichelsonInstruction.DROP:
                drop_count = 1
                j = i + 1
                while (j < len(instructions) and 
                       instructions[j].instruction == MichelsonInstruction.DROP):
                    drop_count += 1
                    j += 1
                
                # Add optimized DROP instructions
                for _ in range(drop_count):
                    optimized.append(current)
                i = j
                continue
            
            # No optimization applied, keep instruction
            optimized.append(current)
            i += 1
        
        return optimized
    
    def generate(self, node: MichelsonASTNode) -> str:
        """Generate Michelson code from AST node."""
        self.output_lines = []
        self.current_indent = 0
        
        try:
            if isinstance(node, MichelsonContract):
                self.generate_contract(node)
            elif isinstance(node, MichelsonSequence):
                # Optimize if enabled
                if self.optimize:
                    node.instructions = self.optimize_instructions(node.instructions)
                self.generate_sequence(node)
            elif isinstance(node, MichelsonInstruction_Node):
                instruction_str = self.generate_instruction(node)
                self.emit_line(instruction_str)
            elif isinstance(node, MichelsonType_Node):
                type_str = self.generate_type(node)
                self.emit_line(type_str)
            elif isinstance(node, MichelsonLiteral):
                literal_str = self.generate_literal(node)
                self.emit_line(literal_str)
            else:
                raise MichelsonGeneratorError(f"Cannot generate code for node type: {type(node)}")
            
            return "\n".join(self.output_lines)
        
        except Exception as e:
            raise MichelsonGeneratorError(f"Code generation failed: {str(e)}")
    
    def generate_with_annotations(self, node: MichelsonASTNode, 
                                 add_comments: bool = True) -> str:
        """Generate Michelson code with annotations and comments."""
        code = self.generate(node)
        
        if add_comments and isinstance(node, MichelsonContract):
            # Add header comment
            header = [
                "# Michelson Smart Contract",
                "# Generated by Runa Michelson Toolchain",
                "# ",
                ""
            ]
            
            code_lines = code.split('\n')
            return '\n'.join(header + code_lines)
        
        return code


def generate_michelson(ast_node: MichelsonASTNode, 
                      indent_size: int = 2, 
                      optimize: bool = True,
                      add_comments: bool = True) -> str:
    """Generate Michelson source code from AST."""
    generator = MichelsonGenerator(indent_size=indent_size, optimize=optimize)
    
    if add_comments:
        return generator.generate_with_annotations(ast_node, add_comments=True)
    else:
        return generator.generate(ast_node)


def generate_michelson_compact(ast_node: MichelsonASTNode) -> str:
    """Generate compact Michelson code without extra formatting."""
    generator = MichelsonGenerator(indent_size=0, optimize=True)
    
    # Override emit_line to not add indentation
    original_emit = generator.emit_line
    def compact_emit(line=""):
        if line.strip():
            generator.output_lines.append(line.strip())
        else:
            generator.output_lines.append("")
    
    generator.emit_line = compact_emit
    return generator.generate(ast_node)


def generate_michelson_storage(value: Union[MichelsonNode, Any], 
                             storage_type: MichelsonType_Node) -> str:
    """Generate Michelson storage initialization value."""
    generator = MichelsonGenerator()
    
    if isinstance(value, MichelsonNode):
        return generator.generate_node_value(value)
    else:
        # Convert Python value to Michelson literal
        literal = MichelsonLiteral(value)
        return generator.generate_literal(literal)


def format_michelson_code(code: str, indent_size: int = 2) -> str:
    """Format existing Michelson code with consistent indentation."""
    lines = code.split('\n')
    formatted_lines = []
    indent_level = 0
    
    for line in lines:
        stripped = line.strip()
        
        if not stripped or stripped.startswith('#'):
            formatted_lines.append(stripped)
            continue
        
        # Decrease indent for closing braces
        if stripped == '}':
            indent_level = max(0, indent_level - 1)
        
        # Add indentation
        formatted_line = ' ' * (indent_level * indent_size) + stripped
        formatted_lines.append(formatted_line)
        
        # Increase indent for opening braces
        if stripped == '{':
            indent_level += 1
    
    return '\n'.join(formatted_lines) 