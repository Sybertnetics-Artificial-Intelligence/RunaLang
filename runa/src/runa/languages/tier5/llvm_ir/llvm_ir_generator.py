"""LLVM IR Code Generator - Generates LLVM IR source code from AST."""

from typing import Any, Dict, List, Optional, TextIO
from dataclasses import dataclass
import io

from .llvm_ir_ast import *


@dataclass
class LLVMIRCodeStyle:
    """Configuration for LLVM IR code generation style."""
    indent_size: int = 2
    use_tabs: bool = False
    align_instructions: bool = True
    comment_column: int = 50
    max_line_length: int = 120
    include_debug_info: bool = False


class LLVMIRCodeGenerator:
    """Generates LLVM IR source code from AST."""
    
    def __init__(self, style: Optional[LLVMIRCodeStyle] = None):
        self.style = style or LLVMIRCodeStyle()
        self.output = io.StringIO()
        self.indent_level = 0
    
    def generate(self, node: LLVMIRNode) -> str:
        """Generate LLVM IR code from AST."""
        self.output = io.StringIO()
        self.indent_level = 0
        
        try:
            self._generate_node(node)
            return self.output.getvalue()
        except Exception as e:
            return f"; Error generating LLVM IR: {str(e)}\n"
    
    def _generate_node(self, node: LLVMIRNode) -> None:
        """Generate code for specific node types."""
        if isinstance(node, ModuleNode):
            self._generate_module(node)
        elif isinstance(node, FunctionNode):
            self._generate_function(node)
        elif isinstance(node, BasicBlockNode):
            self._generate_basic_block(node)
        elif isinstance(node, InstructionNode):
            self._generate_instruction(node)
        elif isinstance(node, GlobalVariableNode):
            self._generate_global(node)
    
    def _generate_module(self, node: ModuleNode) -> None:
        """Generate module."""
        # Target information
        if node.target_triple:
            self._write(f'target triple = "{node.target_triple}"\n')
        if node.data_layout:
            self._write(f'target datalayout = "{node.data_layout}"\n')
        
        if node.target_triple or node.data_layout:
            self._write('\n')
        
        # Global variables
        for global_var in node.globals:
            self._generate_node(global_var)
            self._write('\n')
        
        if node.globals:
            self._write('\n')
        
        # Functions
        for i, function in enumerate(node.functions):
            if i > 0:
                self._write('\n')
            self._generate_node(function)
    
    def _generate_function(self, node: FunctionNode) -> None:
        """Generate function."""
        # Function header
        if node.is_declaration():
            self._write("declare ")
        else:
            self._write("define ")
        
        # Linkage
        if node.linkage != "external":
            self._write(f"{node.linkage} ")
        
        # Return type
        self._write(f"{node.function_type.return_type.name} ")
        
        # Function name
        self._write(f"@{node.name}(")
        
        # Parameters
        param_strs = []
        for i, param_type in enumerate(node.function_type.param_types):
            if i < len(node.arguments):
                arg = node.arguments[i]
                param_str = f"{param_type.name}"
                if arg.name:
                    param_str += f" %{arg.name}"
                param_strs.append(param_str)
            else:
                param_strs.append(param_type.name)
        
        if node.function_type.is_vararg:
            param_strs.append("...")
        
        self._write(", ".join(param_strs))
        self._write(")")
        
        # Function attributes
        if node.function_attributes:
            self._write(" " + " ".join(node.function_attributes))
        
        if node.is_declaration():
            self._write("\n")
            return
        
        # Function body
        self._write(" {\n")
        self.indent_level += 1
        
        for block in node.basic_blocks:
            self._generate_node(block)
        
        self.indent_level -= 1
        self._write("}\n")
    
    def _generate_basic_block(self, node: BasicBlockNode) -> None:
        """Generate basic block."""
        # Block label (except for entry block)
        if not node.is_entry_block():
            self._write(f"{node.name or 'unnamed'}:\n")
        
        # Instructions
        for instruction in node.instructions:
            self._generate_node(instruction)
    
    def _generate_instruction(self, node: InstructionNode) -> None:
        """Generate instruction."""
        self._write_indent()
        
        # Result assignment
        if node.name and not isinstance(node.value_type, VoidTypeNode):
            self._write(f"%{node.name} = ")
        
        # Instruction specific generation
        if isinstance(node, AddNode):
            self._generate_add(node)
        elif isinstance(node, SubNode):
            self._generate_sub(node)
        elif isinstance(node, MulNode):
            self._generate_mul(node)
        elif isinstance(node, AllocaNode):
            self._generate_alloca(node)
        elif isinstance(node, LoadNode):
            self._generate_load(node)
        elif isinstance(node, StoreNode):
            self._generate_store(node)
        elif isinstance(node, CallNode):
            self._generate_call(node)
        elif isinstance(node, ReturnNode):
            self._generate_return(node)
        elif isinstance(node, BranchNode):
            self._generate_branch(node)
        elif isinstance(node, ICmpNode):
            self._generate_icmp(node)
        elif isinstance(node, PhiNode):
            self._generate_phi(node)
        else:
            self._generate_generic_instruction(node)
        
        self._write("\n")
    
    def _generate_add(self, node: AddNode) -> None:
        """Generate add instruction."""
        flags = []
        if node.nsw:
            flags.append("nsw")
        if node.nuw:
            flags.append("nuw")
        
        flag_str = " " + " ".join(flags) if flags else ""
        self._write(f"add{flag_str} {node.left.value_type.name} {self._format_value(node.left)}, {self._format_value(node.right)}")
    
    def _generate_sub(self, node: SubNode) -> None:
        """Generate sub instruction."""
        flags = []
        if node.nsw:
            flags.append("nsw")
        if node.nuw:
            flags.append("nuw")
        
        flag_str = " " + " ".join(flags) if flags else ""
        self._write(f"sub{flag_str} {node.left.value_type.name} {self._format_value(node.left)}, {self._format_value(node.right)}")
    
    def _generate_mul(self, node: MulNode) -> None:
        """Generate mul instruction."""
        flags = []
        if node.nsw:
            flags.append("nsw")
        if node.nuw:
            flags.append("nuw")
        
        flag_str = " " + " ".join(flags) if flags else ""
        self._write(f"mul{flag_str} {node.left.value_type.name} {self._format_value(node.left)}, {self._format_value(node.right)}")
    
    def _generate_alloca(self, node: AllocaNode) -> None:
        """Generate alloca instruction."""
        self._write(f"alloca {node.allocated_type.name}")
        
        if node.array_size:
            self._write(f", {node.array_size.value_type.name} {self._format_value(node.array_size)}")
        
        if node.alignment:
            self._write(f", align {node.alignment}")
    
    def _generate_load(self, node: LoadNode) -> None:
        """Generate load instruction."""
        self._write(f"load {node.value_type.name}, ")
        self._write(f"{node.pointer.value_type.name} {self._format_value(node.pointer)}")
        
        if node.volatile:
            self._write(", volatile")
        
        if node.alignment:
            self._write(f", align {node.alignment}")
    
    def _generate_store(self, node: StoreNode) -> None:
        """Generate store instruction."""
        self._write("store ")
        
        if node.volatile:
            self._write("volatile ")
        
        self._write(f"{node.stored_value.value_type.name} {self._format_value(node.stored_value)}, ")
        self._write(f"{node.pointer.value_type.name} {self._format_value(node.pointer)}")
        
        if node.alignment:
            self._write(f", align {node.alignment}")
    
    def _generate_call(self, node: CallNode) -> None:
        """Generate call instruction."""
        if node.tail_call:
            self._write("tail ")
        
        self._write("call ")
        
        if node.calling_convention:
            self._write(f"{node.calling_convention} ")
        
        # Return type
        if isinstance(node.function.value_type, FunctionTypeNode):
            ret_type = node.function.value_type.return_type
        else:
            ret_type = node.value_type
        
        self._write(f"{ret_type.name} ")
        
        # Function
        self._write(f"{self._format_value(node.function)}(")
        
        # Arguments
        arg_strs = []
        for arg in node.arguments:
            arg_strs.append(f"{arg.value_type.name} {self._format_value(arg)}")
        
        self._write(", ".join(arg_strs))
        self._write(")")
    
    def _generate_return(self, node: ReturnNode) -> None:
        """Generate return instruction."""
        if node.return_value:
            self._write(f"ret {node.return_value.value_type.name} {self._format_value(node.return_value)}")
        else:
            self._write("ret void")
    
    def _generate_branch(self, node: BranchNode) -> None:
        """Generate branch instruction."""
        if node.condition:
            # Conditional branch
            self._write(f"br {node.condition.value_type.name} {self._format_value(node.condition)}, ")
            self._write(f"label %{node.true_block.name if node.true_block else 'unknown'}, ")
            self._write(f"label %{node.false_block.name if node.false_block else 'unknown'}")
        else:
            # Unconditional branch
            self._write(f"br label %{node.true_block.name if node.true_block else 'unknown'}")
    
    def _generate_icmp(self, node: ICmpNode) -> None:
        """Generate icmp instruction."""
        self._write(f"icmp {node.predicate} {node.left.value_type.name} {self._format_value(node.left)}, {self._format_value(node.right)}")
    
    def _generate_phi(self, node: PhiNode) -> None:
        """Generate phi instruction."""
        self._write(f"phi {node.value_type.name} ")
        
        phi_pairs = []
        for value, block in node.incoming:
            phi_pairs.append(f"[ {self._format_value(value)}, %{block.name} ]")
        
        self._write(", ".join(phi_pairs))
    
    def _generate_generic_instruction(self, node: InstructionNode) -> None:
        """Generate generic instruction."""
        self._write(node.opcode)
        
        if node.operands:
            operand_strs = []
            for operand in node.operands:
                operand_strs.append(f"{operand.value_type.name} {self._format_value(operand)}")
            self._write(" " + ", ".join(operand_strs))
    
    def _generate_global(self, node: GlobalVariableNode) -> None:
        """Generate global variable."""
        self._write(f"@{node.name} = ")
        
        # Linkage
        if node.linkage != "external":
            self._write(f"{node.linkage} ")
        
        # Visibility
        if node.visibility != "default":
            self._write(f"{node.visibility} ")
        
        # Thread local
        if node.thread_local:
            self._write("thread_local ")
        
        # Unnamed addr
        if node.unnamed_addr:
            self._write("unnamed_addr ")
        
        # Global or constant
        if node.constant:
            self._write("constant ")
        else:
            self._write("global ")
        
        # Type
        self._write(f"{node.global_type.name}")
        
        # Initializer
        if node.initializer:
            self._write(f" {self._format_value(node.initializer)}")
        
        # Alignment
        if node.alignment:
            self._write(f", align {node.alignment}")
        
        # Section
        if node.section:
            self._write(f', section "{node.section}"')
        
        self._write("\n")
    
    def _format_value(self, value: ValueNode) -> str:
        """Format value for output."""
        if isinstance(value, IntegerConstantNode):
            return str(value.value)
        elif isinstance(value, FloatConstantNode):
            return str(value.value)
        elif isinstance(value, BoolConstantNode):
            return "true" if value.value else "false"
        elif isinstance(value, NullConstantNode):
            return "null"
        elif isinstance(value, UndefConstantNode):
            return "undef"
        elif isinstance(value, PoisonConstantNode):
            return "poison"
        elif isinstance(value, GlobalVariableNode):
            return f"@{value.name}"
        elif value.name:
            return f"%{value.name}"
        else:
            return f"%{id(value)}"
    
    def _write(self, text: str) -> None:
        """Write text to output."""
        self.output.write(text)
    
    def _write_indent(self) -> None:
        """Write indentation."""
        if self.style.use_tabs:
            self._write('\t' * self.indent_level)
        else:
            self._write(' ' * (self.indent_level * self.style.indent_size))


# Utility functions
def generate_llvm_ir_code(node: LLVMIRNode, style: Optional[LLVMIRCodeStyle] = None) -> str:
    """Generate LLVM IR code from AST node."""
    generator = LLVMIRCodeGenerator(style)
    return generator.generate(node)


def format_llvm_ir_code(code: str, style: Optional[LLVMIRCodeStyle] = None) -> str:
    """Format LLVM IR code."""
    # Basic formatting - could be more sophisticated
    lines = code.split('\n')
    formatted_lines = []
    indent_level = 0
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            formatted_lines.append('')
            continue
        
        # Decrease indent for closing braces
        if stripped == '}':
            indent_level = max(0, indent_level - 1)
        
        # Add indentation
        if style and style.use_tabs:
            indent = '\t' * indent_level
        else:
            indent_size = style.indent_size if style else 2
            indent = ' ' * (indent_level * indent_size)
        
        formatted_lines.append(indent + stripped)
        
        # Increase indent for opening braces
        if stripped.endswith('{'):
            indent_level += 1
    
    return '\n'.join(formatted_lines)


def optimize_llvm_ir_code(code: str) -> str:
    """Apply basic optimizations to LLVM IR code."""
    # Placeholder for optimization passes
    # Could implement:
    # - Dead code elimination
    # - Constant folding
    # - Instruction combining
    return code


def create_llvm_ir_generator(style: Optional[LLVMIRCodeStyle] = None) -> LLVMIRCodeGenerator:
    """Create LLVM IR code generator."""
    return LLVMIRCodeGenerator(style) 