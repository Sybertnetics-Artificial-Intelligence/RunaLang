"""
Assembly Converter - Bidirectional conversion between Assembly and Runa Universal AST.

This module provides comprehensive converters for translating between Assembly language
constructs and Runa's Universal AST, supporting multiple architectures and instruction sets.
"""

from typing import Any, Dict, List, Optional, Union, Tuple
from dataclasses import dataclass
import re

from runa.core.ast import Node, NodeType
from runa.core.metadata import ASTMetadata
from .assembly_ast import *


@dataclass
class AssemblyConversionConfig:
    """Configuration for Assembly conversion operations."""
    target_architecture: str = "x64"  # x86, x64, arm, arm64, riscv, mips, powerpc
    instruction_format: str = "intel"  # intel, at&t
    preserve_comments: bool = True
    preserve_labels: bool = True
    preserve_directives: bool = True
    optimize_instructions: bool = False
    include_metadata: bool = True
    validate_registers: bool = True
    validate_instructions: bool = True


class AssemblyToRunaConverter:
    """Converts Assembly AST to Runa Universal AST."""
    
    def __init__(self, config: Optional[AssemblyConversionConfig] = None):
        self.config = config or AssemblyConversionConfig()
        self.metadata_stack: List[Dict[str, Any]] = []
        self.label_table: Dict[str, str] = {}
        self.register_mapping: Dict[str, str] = {}
        self.instruction_mapping: Dict[str, str] = {}
        self._setup_mappings()
    
    def _setup_mappings(self) -> None:
        """Setup architecture-specific mappings."""
        # Register mappings (Assembly -> Runa semantic names)
        if self.config.target_architecture in ["x86", "x64"]:
            self.register_mapping = {
                "rax": "accumulator_64",
                "eax": "accumulator_32", 
                "ax": "accumulator_16",
                "al": "accumulator_8",
                "rbx": "base_64",
                "rcx": "counter_64",
                "rdx": "data_64",
                "rsp": "stack_pointer",
                "rbp": "base_pointer",
                "rsi": "source_index",
                "rdi": "destination_index",
                "rip": "instruction_pointer",
                "r8": "general_register_8",
                "r9": "general_register_9",
                "r10": "general_register_10",
                "r11": "general_register_11",
                "r12": "general_register_12",
                "r13": "general_register_13",
                "r14": "general_register_14",
                "r15": "general_register_15",
                "xmm0": "float_register_0",
                "xmm1": "float_register_1",
                "xmm2": "float_register_2",
                "xmm3": "float_register_3",
            }
        elif self.config.target_architecture in ["arm", "arm64"]:
            self.register_mapping = {
                "x0": "argument_0", "x1": "argument_1", "x2": "argument_2", "x3": "argument_3",
                "x4": "argument_4", "x5": "argument_5", "x6": "argument_6", "x7": "argument_7",
                "x8": "indirect_result", "x9": "general_9", "x10": "general_10",
                "x11": "general_11", "x12": "general_12", "x13": "general_13",
                "x14": "general_14", "x15": "general_15", "x16": "intra_procedure_call",
                "x17": "intra_procedure_call_2", "x18": "platform_register",
                "x19": "callee_saved_19", "x20": "callee_saved_20",
                "x21": "callee_saved_21", "x22": "callee_saved_22",
                "x29": "frame_pointer", "x30": "link_register", "sp": "stack_pointer",
                "v0": "vector_0", "v1": "vector_1", "v2": "vector_2", "v3": "vector_3",
            }
        
        # Instruction mappings (Assembly -> Runa operation types)
        self.instruction_mapping = {
            # Data movement
            "mov": "assign", "movq": "assign", "movl": "assign",
            "lea": "load_effective_address", "push": "stack_push", "pop": "stack_pop",
            "xchg": "exchange", "cmpxchg": "compare_exchange",
            
            # Arithmetic
            "add": "add", "sub": "subtract", "mul": "multiply", "div": "divide",
            "inc": "increment", "dec": "decrement", "neg": "negate",
            "adc": "add_with_carry", "sbb": "subtract_with_borrow",
            "imul": "signed_multiply", "idiv": "signed_divide",
            
            # Logical
            "and": "bitwise_and", "or": "bitwise_or", "xor": "bitwise_xor",
            "not": "bitwise_not", "shl": "shift_left", "shr": "shift_right",
            "sal": "arithmetic_shift_left", "sar": "arithmetic_shift_right",
            "rol": "rotate_left", "ror": "rotate_right",
            
            # Comparison
            "cmp": "compare", "test": "test_bits",
            
            # Control flow
            "jmp": "unconditional_jump", "je": "jump_if_equal", "jne": "jump_if_not_equal",
            "jz": "jump_if_zero", "jnz": "jump_if_not_zero",
            "jl": "jump_if_less", "jle": "jump_if_less_equal",
            "jg": "jump_if_greater", "jge": "jump_if_greater_equal",
            "ja": "jump_if_above", "jb": "jump_if_below",
            "call": "function_call", "ret": "return", "leave": "function_epilogue",
            
            # System
            "int": "interrupt", "syscall": "system_call", "sysenter": "system_enter",
            "nop": "no_operation", "hlt": "halt",
            
            # Floating point
            "fadd": "float_add", "fsub": "float_subtract",
            "fmul": "float_multiply", "fdiv": "float_divide",
            "fld": "float_load", "fst": "float_store",
            "fcom": "float_compare", "fcomi": "float_compare_integer",
            
            # String operations
            "movs": "move_string", "cmps": "compare_string",
            "scas": "scan_string", "lods": "load_string", "stos": "store_string",
            
            # Bit manipulation
            "bt": "bit_test", "bts": "bit_test_set", "btr": "bit_test_reset",
            "btc": "bit_test_complement", "bsf": "bit_scan_forward",
            "bsr": "bit_scan_reverse", "popcnt": "population_count",
        }
    
    def convert(self, assembly_node: AssemblyNode) -> Node:
        """Convert Assembly AST node to Runa Universal AST."""
        try:
            return self._convert_node(assembly_node)
        except Exception as e:
            # Return error node with metadata
            return Node(
                type=NodeType.ERROR,
                metadata=ASTMetadata(
                    error_message=f"Assembly conversion error: {str(e)}",
                    source_language="assembly",
                    original_node=str(assembly_node)
                )
            )
    
    def _convert_node(self, node: AssemblyNode) -> Node:
        """Convert specific Assembly node types."""
        if isinstance(node, ProgramNode):
            return self._convert_program(node)
        elif isinstance(node, InstructionNode):
            return self._convert_instruction(node)
        elif isinstance(node, LabelNode):
            return self._convert_label(node)
        elif isinstance(node, DirectiveNode):
            return self._convert_directive(node)
        elif isinstance(node, SectionNode):
            return self._convert_section(node)
        elif isinstance(node, RegisterNode):
            return self._convert_register(node)
        elif isinstance(node, MemoryNode):
            return self._convert_memory(node)
        elif isinstance(node, ImmediateNode):
            return self._convert_immediate(node)
        elif isinstance(node, LabelRefNode):
            return self._convert_label_ref(node)
        elif isinstance(node, CommentNode):
            return self._convert_comment(node)
        elif isinstance(node, MacroNode):
            return self._convert_macro(node)
        elif isinstance(node, ConditionalNode):
            return self._convert_conditional(node)
        elif isinstance(node, DataDefinitionNode):
            return self._convert_data_definition(node)
        elif isinstance(node, ExpressionNode):
            return self._convert_expression(node)
        else:
            # Generic node conversion
            return Node(
                type=NodeType.IDENTIFIER,
                value=str(node),
                metadata=ASTMetadata(
                    source_language="assembly",
                    node_type="unknown",
                    original_node=str(node)
                )
            )
    
    def _convert_program(self, node: ProgramNode) -> Node:
        """Convert program node."""
        children = []
        for item in node.items:
            converted = self._convert_node(item)
            if converted:
                children.append(converted)
        
        return Node(
            type=NodeType.PROGRAM,
            children=children,
            metadata=ASTMetadata(
                source_language="assembly",
                architecture=self.config.target_architecture,
                instruction_format=self.config.instruction_format,
                node_type="program"
            )
        )
    
    def _convert_instruction(self, node: InstructionNode) -> Node:
        """Convert instruction node."""
        # Map assembly instruction to Runa operation
        operation = self.instruction_mapping.get(node.mnemonic.lower(), "assembly_operation")
        
        # Convert operands
        operands = []
        for operand in node.operands:
            converted_operand = self._convert_node(operand)
            if converted_operand:
                operands.append(converted_operand)
        
        # Determine if this is an assignment-like operation
        if operation in ["assign", "load_effective_address"] and len(operands) >= 2:
            return Node(
                type=NodeType.ASSIGNMENT,
                children=[operands[0], operands[1]],  # destination, source
                metadata=ASTMetadata(
                    source_language="assembly",
                    operation=operation,
                    instruction=node.mnemonic,
                    node_type="assignment"
                )
            )
        elif operation in ["add", "subtract", "multiply", "divide"]:
            return Node(
                type=NodeType.BINARY_OP,
                value=operation,
                children=operands,
                metadata=ASTMetadata(
                    source_language="assembly",
                    operation=operation,
                    instruction=node.mnemonic,
                    node_type="binary_operation"
                )
            )
        elif operation.startswith("jump"):
            return Node(
                type=NodeType.CONDITIONAL if "if" in operation else NodeType.GOTO,
                children=operands,
                metadata=ASTMetadata(
                    source_language="assembly",
                    operation=operation,
                    instruction=node.mnemonic,
                    node_type="control_flow"
                )
            )
        elif operation == "function_call":
            return Node(
                type=NodeType.FUNCTION_CALL,
                children=operands,
                metadata=ASTMetadata(
                    source_language="assembly",
                    operation=operation,
                    instruction=node.mnemonic,
                    node_type="function_call"
                )
            )
        elif operation == "return":
            return Node(
                type=NodeType.RETURN,
                children=operands,
                metadata=ASTMetadata(
                    source_language="assembly",
                    operation=operation,
                    instruction=node.mnemonic,
                    node_type="return"
                )
            )
        else:
            # Generic operation
            return Node(
                type=NodeType.EXPRESSION,
                value=operation,
                children=operands,
                metadata=ASTMetadata(
                    source_language="assembly",
                    operation=operation,
                    instruction=node.mnemonic,
                    node_type="operation"
                )
            )
    
    def _convert_label(self, node: LabelNode) -> Node:
        """Convert label node."""
        self.label_table[node.name] = node.name
        return Node(
            type=NodeType.LABEL,
            value=node.name,
            metadata=ASTMetadata(
                source_language="assembly",
                node_type="label"
            )
        )
    
    def _convert_directive(self, node: DirectiveNode) -> Node:
        """Convert directive node."""
        return Node(
            type=NodeType.PRAGMA,
            value=node.name,
            children=[self._convert_node(arg) for arg in node.args] if node.args else [],
            metadata=ASTMetadata(
                source_language="assembly",
                directive_type=node.name,
                node_type="directive"
            )
        )
    
    def _convert_section(self, node: SectionNode) -> Node:
        """Convert section node."""
        children = []
        for item in node.contents:
            converted = self._convert_node(item)
            if converted:
                children.append(converted)
        
        return Node(
            type=NodeType.MODULE,
            value=node.name,
            children=children,
            metadata=ASTMetadata(
                source_language="assembly",
                section_type=node.section_type,
                node_type="section"
            )
        )
    
    def _convert_register(self, node: RegisterNode) -> Node:
        """Convert register node."""
        # Map register to semantic name
        semantic_name = self.register_mapping.get(node.name.lower(), node.name)
        
        return Node(
            type=NodeType.IDENTIFIER,
            value=semantic_name,
            metadata=ASTMetadata(
                source_language="assembly",
                register_name=node.name,
                register_size=node.size,
                node_type="register"
            )
        )
    
    def _convert_memory(self, node: MemoryNode) -> Node:
        """Convert memory reference node."""
        # Convert memory addressing to array access or pointer dereference
        base_expr = None
        if node.base:
            base_expr = self._convert_node(node.base)
        
        # Build address expression
        address_parts = []
        if base_expr:
            address_parts.append(base_expr)
        
        if node.index:
            index_expr = self._convert_node(node.index)
            if node.scale and node.scale > 1:
                scale_expr = Node(type=NodeType.LITERAL, value=node.scale)
                scaled_index = Node(
                    type=NodeType.BINARY_OP,
                    value="multiply",
                    children=[index_expr, scale_expr]
                )
                address_parts.append(scaled_index)
            else:
                address_parts.append(index_expr)
        
        if node.displacement:
            disp_expr = Node(type=NodeType.LITERAL, value=node.displacement)
            address_parts.append(disp_expr)
        
        # Combine address parts
        if len(address_parts) == 1:
            address_expr = address_parts[0]
        elif len(address_parts) > 1:
            address_expr = address_parts[0]
            for part in address_parts[1:]:
                address_expr = Node(
                    type=NodeType.BINARY_OP,
                    value="add",
                    children=[address_expr, part]
                )
        else:
            address_expr = Node(type=NodeType.LITERAL, value=0)
        
        return Node(
            type=NodeType.ARRAY_ACCESS,
            children=[address_expr],
            metadata=ASTMetadata(
                source_language="assembly",
                memory_size=node.size,
                addressing_mode="memory_reference",
                node_type="memory_access"
            )
        )
    
    def _convert_immediate(self, node: ImmediateNode) -> Node:
        """Convert immediate value node."""
        return Node(
            type=NodeType.LITERAL,
            value=node.value,
            metadata=ASTMetadata(
                source_language="assembly",
                immediate_type=type(node.value).__name__,
                node_type="immediate"
            )
        )
    
    def _convert_label_ref(self, node: LabelRefNode) -> Node:
        """Convert label reference node."""
        return Node(
            type=NodeType.IDENTIFIER,
            value=node.label,
            metadata=ASTMetadata(
                source_language="assembly",
                reference_type="label",
                node_type="label_reference"
            )
        )
    
    def _convert_comment(self, node: CommentNode) -> Node:
        """Convert comment node."""
        if not self.config.preserve_comments:
            return None
        
        return Node(
            type=NodeType.COMMENT,
            value=node.text,
            metadata=ASTMetadata(
                source_language="assembly",
                node_type="comment"
            )
        )
    
    def _convert_macro(self, node: MacroNode) -> Node:
        """Convert macro node."""
        # Convert parameters
        params = []
        for param in node.parameters:
            params.append(Node(type=NodeType.IDENTIFIER, value=param))
        
        # Convert body
        body_nodes = []
        for stmt in node.body:
            converted = self._convert_node(stmt)
            if converted:
                body_nodes.append(converted)
        
        return Node(
            type=NodeType.FUNCTION_DEF,
            value=node.name,
            children=[
                Node(type=NodeType.PARAMETER_LIST, children=params),
                Node(type=NodeType.BLOCK, children=body_nodes)
            ],
            metadata=ASTMetadata(
                source_language="assembly",
                definition_type="macro",
                node_type="macro_definition"
            )
        )
    
    def _convert_conditional(self, node: ConditionalNode) -> Node:
        """Convert conditional assembly node."""
        condition = self._convert_node(node.condition)
        
        then_nodes = []
        for stmt in node.then_block:
            converted = self._convert_node(stmt)
            if converted:
                then_nodes.append(converted)
        
        else_nodes = []
        if node.else_block:
            for stmt in node.else_block:
                converted = self._convert_node(stmt)
                if converted:
                    else_nodes.append(converted)
        
        children = [
            condition,
            Node(type=NodeType.BLOCK, children=then_nodes)
        ]
        
        if else_nodes:
            children.append(Node(type=NodeType.BLOCK, children=else_nodes))
        
        return Node(
            type=NodeType.IF,
            children=children,
            metadata=ASTMetadata(
                source_language="assembly",
                node_type="conditional_assembly"
            )
        )
    
    def _convert_data_definition(self, node: DataDefinitionNode) -> Node:
        """Convert data definition node."""
        # Convert values
        value_nodes = []
        for value in node.values:
            if isinstance(value, str):
                value_nodes.append(Node(type=NodeType.LITERAL, value=value))
            elif isinstance(value, (int, float)):
                value_nodes.append(Node(type=NodeType.LITERAL, value=value))
            else:
                converted = self._convert_node(value)
                if converted:
                    value_nodes.append(converted)
        
        return Node(
            type=NodeType.VARIABLE_DEF,
            value=node.label if hasattr(node, 'label') else "data",
            children=value_nodes,
            metadata=ASTMetadata(
                source_language="assembly",
                data_type=node.data_type,
                node_type="data_definition"
            )
        )
    
    def _convert_expression(self, node: ExpressionNode) -> Node:
        """Convert expression node."""
        if node.operator:
            # Binary expression
            left = self._convert_node(node.left)
            right = self._convert_node(node.right)
            
            return Node(
                type=NodeType.BINARY_OP,
                value=node.operator,
                children=[left, right],
                metadata=ASTMetadata(
                    source_language="assembly",
                    node_type="expression"
                )
            )
        else:
            # Single operand
            return self._convert_node(node.left)


class RunaToAssemblyConverter:
    """Converts Runa Universal AST to Assembly AST."""
    
    def __init__(self, config: Optional[AssemblyConversionConfig] = None):
        self.config = config or AssemblyConversionConfig()
        self.register_allocator = RegisterAllocator(self.config.target_architecture)
        self.label_generator = LabelGenerator()
        self.instruction_selector = InstructionSelector(self.config.target_architecture)
    
    def convert(self, runa_node: Node) -> AssemblyNode:
        """Convert Runa Universal AST to Assembly AST."""
        try:
            return self._convert_node(runa_node)
        except Exception as e:
            # Return comment with error info
            return CommentNode(f"Conversion error: {str(e)}")
    
    def _convert_node(self, node: Node) -> AssemblyNode:
        """Convert specific Runa node types."""
        if node.type == NodeType.PROGRAM:
            return self._convert_program(node)
        elif node.type == NodeType.ASSIGNMENT:
            return self._convert_assignment(node)
        elif node.type == NodeType.BINARY_OP:
            return self._convert_binary_op(node)
        elif node.type == NodeType.FUNCTION_CALL:
            return self._convert_function_call(node)
        elif node.type == NodeType.RETURN:
            return self._convert_return(node)
        elif node.type == NodeType.IF:
            return self._convert_if(node)
        elif node.type == NodeType.WHILE:
            return self._convert_while(node)
        elif node.type == NodeType.FOR:
            return self._convert_for(node)
        elif node.type == NodeType.LITERAL:
            return self._convert_literal(node)
        elif node.type == NodeType.IDENTIFIER:
            return self._convert_identifier(node)
        elif node.type == NodeType.COMMENT:
            return self._convert_comment(node)
        else:
            # Default: return as comment
            return CommentNode(f"Unsupported node type: {node.type}")
    
    def _convert_program(self, node: Node) -> ProgramNode:
        """Convert program node."""
        items = []
        
        # Add standard prologue
        if self.config.target_architecture == "x64":
            items.extend([
                SectionNode("text", "code", []),
                DirectiveNode("global", ["_start"])
            ])
        
        # Convert children
        for child in node.children:
            converted = self._convert_node(child)
            if converted:
                if isinstance(converted, list):
                    items.extend(converted)
                else:
                    items.append(converted)
        
        return ProgramNode(items)
    
    def _convert_assignment(self, node: Node) -> Union[InstructionNode, List[InstructionNode]]:
        """Convert assignment to mov instruction."""
        if len(node.children) >= 2:
            dest = self._convert_to_operand(node.children[0])
            src = self._convert_to_operand(node.children[1])
            
            return InstructionNode("mov", [dest, src])
        
        return CommentNode("Invalid assignment")
    
    def _convert_binary_op(self, node: Node) -> Union[InstructionNode, List[InstructionNode]]:
        """Convert binary operation."""
        if len(node.children) >= 2:
            left = self._convert_to_operand(node.children[0])
            right = self._convert_to_operand(node.children[1])
            
            # Map operation to instruction
            op_map = {
                "add": "add",
                "subtract": "sub", 
                "multiply": "imul",
                "divide": "idiv",
                "bitwise_and": "and",
                "bitwise_or": "or",
                "bitwise_xor": "xor"
            }
            
            instruction = op_map.get(node.value, "nop")
            return InstructionNode(instruction, [left, right])
        
        return CommentNode(f"Invalid binary operation: {node.value}")
    
    def _convert_function_call(self, node: Node) -> List[InstructionNode]:
        """Convert function call."""
        instructions = []
        
        # Setup arguments (simplified)
        if node.children:
            for i, arg in enumerate(node.children):
                arg_operand = self._convert_to_operand(arg)
                if i < 4:  # First 4 args in registers (x64 calling convention)
                    reg_names = ["rdi", "rsi", "rdx", "rcx"]
                    instructions.append(
                        InstructionNode("mov", [
                            RegisterNode(reg_names[i]),
                            arg_operand
                        ])
                    )
                else:
                    # Push to stack
                    instructions.append(InstructionNode("push", [arg_operand]))
        
        # Make the call
        if hasattr(node, 'value') and node.value:
            instructions.append(InstructionNode("call", [LabelRefNode(node.value)]))
        else:
            instructions.append(InstructionNode("call", [RegisterNode("rax")]))
        
        return instructions
    
    def _convert_return(self, node: Node) -> List[InstructionNode]:
        """Convert return statement."""
        instructions = []
        
        # Load return value if provided
        if node.children:
            return_val = self._convert_to_operand(node.children[0])
            instructions.append(InstructionNode("mov", [RegisterNode("rax"), return_val]))
        
        instructions.append(InstructionNode("ret", []))
        return instructions
    
    def _convert_if(self, node: Node) -> List[AssemblyNode]:
        """Convert if statement."""
        instructions = []
        
        if len(node.children) >= 2:
            condition = node.children[0]
            then_block = node.children[1]
            else_block = node.children[2] if len(node.children) > 2 else None
            
            # Generate labels
            end_label = self.label_generator.generate("if_end")
            else_label = self.label_generator.generate("if_else") if else_block else end_label
            
            # Convert condition (simplified)
            cond_instructions = self._convert_condition(condition, else_label)
            instructions.extend(cond_instructions)
            
            # Then block
            for stmt in then_block.children:
                converted = self._convert_node(stmt)
                if isinstance(converted, list):
                    instructions.extend(converted)
                else:
                    instructions.append(converted)
            
            # Jump to end if there's an else block
            if else_block:
                instructions.append(InstructionNode("jmp", [LabelRefNode(end_label)]))
                instructions.append(LabelNode(else_label))
                
                # Else block
                for stmt in else_block.children:
                    converted = self._convert_node(stmt)
                    if isinstance(converted, list):
                        instructions.extend(converted)
                    else:
                        instructions.append(converted)
            
            instructions.append(LabelNode(end_label))
        
        return instructions
    
    def _convert_while(self, node: Node) -> List[AssemblyNode]:
        """Convert while loop."""
        instructions = []
        
        if len(node.children) >= 2:
            condition = node.children[0]
            body = node.children[1]
            
            # Generate labels
            start_label = self.label_generator.generate("while_start")
            end_label = self.label_generator.generate("while_end")
            
            instructions.append(LabelNode(start_label))
            
            # Convert condition
            cond_instructions = self._convert_condition(condition, end_label)
            instructions.extend(cond_instructions)
            
            # Body
            for stmt in body.children:
                converted = self._convert_node(stmt)
                if isinstance(converted, list):
                    instructions.extend(converted)
                else:
                    instructions.append(converted)
            
            # Jump back to start
            instructions.append(InstructionNode("jmp", [LabelRefNode(start_label)]))
            instructions.append(LabelNode(end_label))
        
        return instructions
    
    def _convert_for(self, node: Node) -> List[AssemblyNode]:
        """Convert for loop (simplified)."""
        # Convert to while loop equivalent
        if len(node.children) >= 3:
            init = node.children[0]
            condition = node.children[1] 
            update = node.children[2]
            body = node.children[3] if len(node.children) > 3 else Node(type=NodeType.BLOCK, children=[])
            
            instructions = []
            
            # Initialization
            init_converted = self._convert_node(init)
            if isinstance(init_converted, list):
                instructions.extend(init_converted)
            else:
                instructions.append(init_converted)
            
            # Create while loop
            while_node = Node(
                type=NodeType.WHILE,
                children=[
                    condition,
                    Node(type=NodeType.BLOCK, children=body.children + [update])
                ]
            )
            
            while_converted = self._convert_while(while_node)
            instructions.extend(while_converted)
            
            return instructions
        
        return [CommentNode("Invalid for loop")]
    
    def _convert_literal(self, node: Node) -> ImmediateNode:
        """Convert literal to immediate operand."""
        return ImmediateNode(node.value)
    
    def _convert_identifier(self, node: Node) -> RegisterNode:
        """Convert identifier to register (simplified)."""
        # Map semantic names back to registers
        reg_mapping = {
            "accumulator_64": "rax",
            "accumulator_32": "eax",
            "base_64": "rbx",
            "counter_64": "rcx",
            "data_64": "rdx",
            "stack_pointer": "rsp",
            "base_pointer": "rbp",
        }
        
        reg_name = reg_mapping.get(node.value, "rax")  # Default to rax
        return RegisterNode(reg_name)
    
    def _convert_comment(self, node: Node) -> CommentNode:
        """Convert comment node."""
        return CommentNode(node.value)
    
    def _convert_to_operand(self, node: Node) -> AssemblyNode:
        """Convert Runa node to Assembly operand."""
        if node.type == NodeType.LITERAL:
            return ImmediateNode(node.value)
        elif node.type == NodeType.IDENTIFIER:
            return self._convert_identifier(node)
        elif node.type == NodeType.ARRAY_ACCESS:
            # Convert to memory reference
            if node.children:
                base = self._convert_to_operand(node.children[0])
                return MemoryNode(base=base)
            return RegisterNode("rax")
        else:
            return RegisterNode("rax")  # Default
    
    def _convert_condition(self, condition: Node, false_label: str) -> List[InstructionNode]:
        """Convert condition to comparison and conditional jump."""
        instructions = []
        
        if condition.type == NodeType.BINARY_OP:
            left = self._convert_to_operand(condition.children[0])
            right = self._convert_to_operand(condition.children[1])
            
            instructions.append(InstructionNode("cmp", [left, right]))
            
            # Map condition to jump instruction
            jump_map = {
                "equals": "jne",  # Jump if NOT equal (to skip then block)
                "not_equals": "je",
                "less_than": "jge",
                "less_than_or_equal": "jg",
                "greater_than": "jle",
                "greater_than_or_equal": "jl"
            }
            
            jump_instr = jump_map.get(condition.value, "jne")
            instructions.append(InstructionNode(jump_instr, [LabelRefNode(false_label)]))
        else:
            # Simple condition - test if zero
            operand = self._convert_to_operand(condition)
            instructions.append(InstructionNode("test", [operand, operand]))
            instructions.append(InstructionNode("jz", [LabelRefNode(false_label)]))
        
        return instructions


class RegisterAllocator:
    """Simple register allocator for Assembly generation."""
    
    def __init__(self, architecture: str):
        self.architecture = architecture
        self.available_registers = self._get_available_registers()
        self.allocated_registers: Dict[str, str] = {}
    
    def _get_available_registers(self) -> List[str]:
        """Get available registers for the target architecture."""
        if self.architecture in ["x86", "x64"]:
            return ["rax", "rbx", "rcx", "rdx", "r8", "r9", "r10", "r11"]
        elif self.architecture in ["arm", "arm64"]:
            return [f"x{i}" for i in range(0, 16)]
        else:
            return ["r0", "r1", "r2", "r3", "r4", "r5", "r6", "r7"]
    
    def allocate(self, variable: str) -> str:
        """Allocate a register for a variable."""
        if variable in self.allocated_registers:
            return self.allocated_registers[variable]
        
        if self.available_registers:
            reg = self.available_registers.pop(0)
            self.allocated_registers[variable] = reg
            return reg
        
        # Spill to memory if no registers available
        return "memory_spill"


class LabelGenerator:
    """Generate unique labels for Assembly code."""
    
    def __init__(self):
        self.counters: Dict[str, int] = {}
    
    def generate(self, prefix: str) -> str:
        """Generate a unique label with the given prefix."""
        count = self.counters.get(prefix, 0)
        self.counters[prefix] = count + 1
        return f"{prefix}_{count}"


class InstructionSelector:
    """Select appropriate instructions for the target architecture."""
    
    def __init__(self, architecture: str):
        self.architecture = architecture
    
    def select_move_instruction(self, size: int) -> str:
        """Select move instruction based on operand size."""
        if self.architecture in ["x86", "x64"]:
            size_map = {8: "movb", 16: "movw", 32: "movl", 64: "movq"}
            return size_map.get(size, "mov")
        return "mov"
    
    def select_arithmetic_instruction(self, operation: str, size: int) -> str:
        """Select arithmetic instruction."""
        base_map = {
            "add": "add",
            "subtract": "sub",
            "multiply": "imul",
            "divide": "idiv"
        }
        return base_map.get(operation, "nop") 