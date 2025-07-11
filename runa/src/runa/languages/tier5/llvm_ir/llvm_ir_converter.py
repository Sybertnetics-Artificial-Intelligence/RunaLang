"""LLVM IR Converter - Bidirectional conversion between LLVM IR and Runa Universal AST."""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass

from runa.core.ast import Node, NodeType
from runa.core.metadata import ASTMetadata
from .llvm_ir_ast import *


@dataclass
class LLVMIRConversionConfig:
    """Configuration for LLVM IR conversion."""
    target_triple: str = "x86_64-unknown-linux-gnu"
    data_layout: str = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
    preserve_debug_info: bool = True
    optimize_level: int = 0


class LLVMIRToRunaConverter:
    """Converts LLVM IR AST to Runa Universal AST."""
    
    def __init__(self, config: Optional[LLVMIRConversionConfig] = None):
        self.config = config or LLVMIRConversionConfig()
    
    def convert(self, llvm_node: LLVMIRNode) -> Node:
        """Convert LLVM IR node to Runa AST."""
        if isinstance(llvm_node, ModuleNode):
            return self._convert_module(llvm_node)
        elif isinstance(llvm_node, FunctionNode):
            return self._convert_function(llvm_node)
        elif isinstance(llvm_node, BasicBlockNode):
            return self._convert_basic_block(llvm_node)
        elif isinstance(llvm_node, InstructionNode):
            return self._convert_instruction(llvm_node)
        else:
            return Node(type=NodeType.IDENTIFIER, value=str(llvm_node))
    
    def _convert_module(self, node: ModuleNode) -> Node:
        """Convert module to program."""
        children = []
        for func in node.functions:
            children.append(self.convert(func))
        for glob in node.globals:
            children.append(self._convert_global(glob))
        
        return Node(
            type=NodeType.PROGRAM,
            children=children,
            metadata=ASTMetadata(
                source_language="llvm_ir",
                target_triple=node.target_triple,
                data_layout=node.data_layout
            )
        )
    
    def _convert_function(self, node: FunctionNode) -> Node:
        """Convert function."""
        params = [Node(type=NodeType.PARAMETER, value=arg.name) for arg in node.arguments]
        body_nodes = [self.convert(block) for block in node.basic_blocks]
        
        return Node(
            type=NodeType.FUNCTION_DEF,
            value=node.name,
            children=[
                Node(type=NodeType.PARAMETER_LIST, children=params),
                Node(type=NodeType.BLOCK, children=body_nodes)
            ],
            metadata=ASTMetadata(source_language="llvm_ir", linkage=node.linkage)
        )
    
    def _convert_basic_block(self, node: BasicBlockNode) -> Node:
        """Convert basic block to block."""
        instructions = [self.convert(instr) for instr in node.instructions]
        return Node(
            type=NodeType.BLOCK,
            value=node.name,
            children=instructions,
            metadata=ASTMetadata(source_language="llvm_ir", block_type="basic")
        )
    
    def _convert_instruction(self, node: InstructionNode) -> Node:
        """Convert instruction."""
        if isinstance(node, AddNode):
            return Node(type=NodeType.BINARY_OP, value="add", 
                       children=[self._convert_value(node.left), self._convert_value(node.right)])
        elif isinstance(node, LoadNode):
            return Node(type=NodeType.VARIABLE_REF, value=str(node.pointer))
        elif isinstance(node, StoreNode):
            return Node(type=NodeType.ASSIGNMENT, 
                       children=[self._convert_value(node.pointer), self._convert_value(node.stored_value)])
        elif isinstance(node, CallNode):
            args = [self._convert_value(arg) for arg in node.arguments]
            return Node(type=NodeType.FUNCTION_CALL, value=str(node.function), children=args)
        elif isinstance(node, ReturnNode):
            ret_val = self._convert_value(node.return_value) if node.return_value else None
            children = [ret_val] if ret_val else []
            return Node(type=NodeType.RETURN, children=children)
        else:
            return Node(type=NodeType.EXPRESSION, value=node.opcode)
    
    def _convert_value(self, value: ValueNode) -> Node:
        """Convert value."""
        if isinstance(value, IntegerConstantNode):
            return Node(type=NodeType.LITERAL, value=value.value)
        elif isinstance(value, FloatConstantNode):
            return Node(type=NodeType.LITERAL, value=value.value)
        elif isinstance(value, BoolConstantNode):
            return Node(type=NodeType.LITERAL, value=value.value)
        else:
            return Node(type=NodeType.IDENTIFIER, value=value.name or "unnamed")
    
    def _convert_global(self, node: GlobalVariableNode) -> Node:
        """Convert global variable."""
        init_val = self._convert_value(node.initializer) if node.initializer else None
        children = [init_val] if init_val else []
        
        return Node(
            type=NodeType.VARIABLE_DEF,
            value=node.name,
            children=children,
            metadata=ASTMetadata(source_language="llvm_ir", global_var=True, linkage=node.linkage)
        )


class RunaToLLVMIRConverter:
    """Converts Runa Universal AST to LLVM IR AST."""
    
    def __init__(self, config: Optional[LLVMIRConversionConfig] = None):
        self.config = config or LLVMIRConversionConfig()
        self.module = ModuleNode("runa_module", self.config.target_triple, self.config.data_layout)
        self.current_function: Optional[FunctionNode] = None
        self.current_block: Optional[BasicBlockNode] = None
        self.value_counter = 0
    
    def convert(self, runa_node: Node) -> LLVMIRNode:
        """Convert Runa AST to LLVM IR."""
        if runa_node.type == NodeType.PROGRAM:
            return self._convert_program(runa_node)
        elif runa_node.type == NodeType.FUNCTION_DEF:
            return self._convert_function_def(runa_node)
        elif runa_node.type == NodeType.BLOCK:
            return self._convert_block(runa_node)
        elif runa_node.type == NodeType.ASSIGNMENT:
            return self._convert_assignment(runa_node)
        elif runa_node.type == NodeType.BINARY_OP:
            return self._convert_binary_op(runa_node)
        elif runa_node.type == NodeType.FUNCTION_CALL:
            return self._convert_function_call(runa_node)
        elif runa_node.type == NodeType.RETURN:
            return self._convert_return(runa_node)
        elif runa_node.type == NodeType.LITERAL:
            return self._convert_literal(runa_node)
        else:
            return self._create_comment(f"Unsupported node: {runa_node.type}")
    
    def _convert_program(self, node: Node) -> ModuleNode:
        """Convert program to module."""
        for child in node.children:
            converted = self.convert(child)
            if isinstance(converted, FunctionNode):
                self.module.add_function(converted)
            elif isinstance(converted, GlobalVariableNode):
                self.module.add_global(converted)
        return self.module
    
    def _convert_function_def(self, node: Node) -> FunctionNode:
        """Convert function definition."""
        name = node.value or "unnamed_func"
        
        # Create simple function type (void -> void for now)
        func_type = FunctionTypeNode(VoidTypeNode(), [])
        function = FunctionNode(name, func_type)
        
        # Create entry block
        entry_block = BasicBlockNode("entry")
        function.add_basic_block(entry_block)
        
        self.current_function = function
        self.current_block = entry_block
        
        # Convert function body
        if len(node.children) > 1:  # Has body
            body = node.children[1]
            for stmt in body.children:
                instr = self.convert(stmt)
                if isinstance(instr, InstructionNode):
                    entry_block.add_instruction(instr)
        
        # Add return if missing
        if not entry_block.get_terminator():
            entry_block.add_instruction(ReturnNode())
        
        return function
    
    def _convert_block(self, node: Node) -> BasicBlockNode:
        """Convert block."""
        block = BasicBlockNode(node.value or f"block_{self.value_counter}")
        self.value_counter += 1
        
        old_block = self.current_block
        self.current_block = block
        
        for child in node.children:
            instr = self.convert(child)
            if isinstance(instr, InstructionNode):
                block.add_instruction(instr)
        
        self.current_block = old_block
        return block
    
    def _convert_assignment(self, node: Node) -> InstructionNode:
        """Convert assignment to store."""
        if len(node.children) >= 2:
            target = self.convert(node.children[0])
            value = self.convert(node.children[1])
            
            # Create alloca for target if needed
            if isinstance(target, ArgumentNode):
                alloca = AllocaNode(IntegerTypeNode(32), name=target.name)
                return StoreNode(value, alloca)
        
        return self._create_nop()
    
    def _convert_binary_op(self, node: Node) -> InstructionNode:
        """Convert binary operation."""
        if len(node.children) >= 2:
            left = self.convert(node.children[0])
            right = self.convert(node.children[1])
            
            if node.value == "add":
                return AddNode(left, right, name=f"add_{self.value_counter}")
            elif node.value == "subtract":
                return SubNode(left, right, name=f"sub_{self.value_counter}")
            elif node.value == "multiply":
                return MulNode(left, right, name=f"mul_{self.value_counter}")
        
        return self._create_nop()
    
    def _convert_function_call(self, node: Node) -> CallNode:
        """Convert function call."""
        func_name = node.value or "unknown_func"
        
        # Create function reference
        func_type = FunctionTypeNode(VoidTypeNode(), [])
        func_ref = GlobalVariableNode(func_name, func_type)
        
        # Convert arguments
        args = [self.convert(child) for child in node.children]
        
        return CallNode(func_ref, args, name=f"call_{self.value_counter}")
    
    def _convert_return(self, node: Node) -> ReturnNode:
        """Convert return statement."""
        if node.children:
            return_value = self.convert(node.children[0])
            return ReturnNode(return_value)
        else:
            return ReturnNode()
    
    def _convert_literal(self, node: Node) -> ConstantNode:
        """Convert literal value."""
        if isinstance(node.value, int):
            return IntegerConstantNode(node.value, 32)
        elif isinstance(node.value, float):
            return FloatConstantNode(node.value, "float")
        elif isinstance(node.value, bool):
            return BoolConstantNode(node.value)
        else:
            return IntegerConstantNode(0, 32)
    
    def _create_nop(self) -> InstructionNode:
        """Create no-op instruction."""
        return InstructionNode("nop", VoidTypeNode(), [])
    
    def _create_comment(self, text: str) -> InstructionNode:
        """Create comment instruction."""
        return InstructionNode("comment", VoidTypeNode(), [], name=text)


# Utility functions
def convert_llvm_ir_to_runa(llvm_node: LLVMIRNode, config: Optional[LLVMIRConversionConfig] = None) -> Node:
    """Convert LLVM IR AST to Runa AST."""
    converter = LLVMIRToRunaConverter(config)
    return converter.convert(llvm_node)


def convert_runa_to_llvm_ir(runa_node: Node, config: Optional[LLVMIRConversionConfig] = None) -> LLVMIRNode:
    """Convert Runa AST to LLVM IR AST."""
    converter = RunaToLLVMIRConverter(config)
    return converter.convert(runa_node)


def create_llvm_ir_converter(config: Optional[LLVMIRConversionConfig] = None) -> LLVMIRToRunaConverter:
    """Create LLVM IR converter."""
    return LLVMIRToRunaConverter(config) 