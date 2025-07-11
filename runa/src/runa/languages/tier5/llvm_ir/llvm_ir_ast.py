"""
LLVM IR AST - Abstract Syntax Tree for LLVM Intermediate Representation.

This module provides comprehensive AST nodes for LLVM IR, supporting SSA form,
type system, instructions, metadata, and all major LLVM IR language constructs.
"""

from typing import Any, Dict, List, Optional, Union, Set, Tuple
from dataclasses import dataclass
from abc import ABC, abstractmethod
import re


@dataclass
class LLVMIRSourceLocation:
    """Source location information for LLVM IR nodes."""
    line: int
    column: int
    file: Optional[str] = None


class LLVMIRNode(ABC):
    """Base class for all LLVM IR AST nodes."""
    
    def __init__(self, location: Optional[LLVMIRSourceLocation] = None):
        self.location = location
        self.metadata: Dict[str, Any] = {}
        self.parent: Optional['LLVMIRNode'] = None
        self.children: List['LLVMIRNode'] = []
    
    @abstractmethod
    def accept(self, visitor: 'LLVMIRVisitor') -> Any:
        """Accept a visitor."""
        pass
    
    def add_child(self, child: 'LLVMIRNode') -> None:
        """Add a child node."""
        child.parent = self
        self.children.append(child)
    
    def get_type(self) -> str:
        """Get the node type name."""
        return self.__class__.__name__
    
    def __str__(self) -> str:
        return f"{self.get_type()}()"
    
    def __repr__(self) -> str:
        return self.__str__()


class LLVMIRVisitor(ABC):
    """Abstract visitor for LLVM IR AST traversal."""
    
    @abstractmethod
    def visit_module(self, node: 'ModuleNode') -> Any:
        pass
    
    @abstractmethod
    def visit_function(self, node: 'FunctionNode') -> Any:
        pass
    
    @abstractmethod
    def visit_basic_block(self, node: 'BasicBlockNode') -> Any:
        pass
    
    @abstractmethod
    def visit_instruction(self, node: 'InstructionNode') -> Any:
        pass
    
    @abstractmethod
    def visit_type(self, node: 'TypeNode') -> Any:
        pass
    
    @abstractmethod
    def visit_value(self, node: 'ValueNode') -> Any:
        pass


class LLVMIRTransformer(LLVMIRVisitor):
    """Transformer base class for LLVM IR AST modifications."""
    
    def transform(self, node: LLVMIRNode) -> LLVMIRNode:
        """Transform a node and return the result."""
        return node.accept(self)
    
    def visit_module(self, node: 'ModuleNode') -> 'ModuleNode':
        # Transform children
        new_functions = [self.transform(func) for func in node.functions]
        new_globals = [self.transform(glob) for glob in node.globals]
        
        node.functions = new_functions
        node.globals = new_globals
        return node
    
    def visit_function(self, node: 'FunctionNode') -> 'FunctionNode':
        # Transform basic blocks
        new_blocks = [self.transform(block) for block in node.basic_blocks]
        node.basic_blocks = new_blocks
        return node
    
    def visit_basic_block(self, node: 'BasicBlockNode') -> 'BasicBlockNode':
        # Transform instructions
        new_instructions = [self.transform(instr) for instr in node.instructions]
        node.instructions = new_instructions
        return node
    
    def visit_instruction(self, node: 'InstructionNode') -> 'InstructionNode':
        return node
    
    def visit_type(self, node: 'TypeNode') -> 'TypeNode':
        return node
    
    def visit_value(self, node: 'ValueNode') -> 'ValueNode':
        return node


# Type System Nodes

class TypeNode(LLVMIRNode):
    """Base class for LLVM IR types."""
    
    def __init__(self, name: str, size_bits: Optional[int] = None, location: Optional[LLVMIRSourceLocation] = None):
        super().__init__(location)
        self.name = name
        self.size_bits = size_bits
    
    def accept(self, visitor: LLVMIRVisitor) -> Any:
        return visitor.visit_type(self)
    
    def is_integer_type(self) -> bool:
        return isinstance(self, IntegerTypeNode)
    
    def is_float_type(self) -> bool:
        return isinstance(self, FloatTypeNode)
    
    def is_pointer_type(self) -> bool:
        return isinstance(self, PointerTypeNode)
    
    def is_array_type(self) -> bool:
        return isinstance(self, ArrayTypeNode)
    
    def is_struct_type(self) -> bool:
        return isinstance(self, StructTypeNode)
    
    def is_function_type(self) -> bool:
        return isinstance(self, FunctionTypeNode)
    
    def __str__(self) -> str:
        return self.name


class VoidTypeNode(TypeNode):
    """LLVM IR void type."""
    
    def __init__(self, location: Optional[LLVMIRSourceLocation] = None):
        super().__init__("void", 0, location)


class IntegerTypeNode(TypeNode):
    """LLVM IR integer type (i1, i8, i16, i32, i64, etc.)."""
    
    def __init__(self, bit_width: int, location: Optional[LLVMIRSourceLocation] = None):
        super().__init__(f"i{bit_width}", bit_width, location)
        self.bit_width = bit_width


class FloatTypeNode(TypeNode):
    """LLVM IR floating-point type (half, float, double, etc.)."""
    
    def __init__(self, precision: str, location: Optional[LLVMIRSourceLocation] = None):
        size_map = {"half": 16, "float": 32, "double": 64, "fp128": 128, "x86_fp80": 80}
        super().__init__(precision, size_map.get(precision, 32), location)
        self.precision = precision


class PointerTypeNode(TypeNode):
    """LLVM IR pointer type."""
    
    def __init__(self, pointee_type: TypeNode, address_space: int = 0, location: Optional[LLVMIRSourceLocation] = None):
        name = f"{pointee_type.name}*"
        if address_space != 0:
            name = f"{pointee_type.name} addrspace({address_space})*"
        super().__init__(name, None, location)
        self.pointee_type = pointee_type
        self.address_space = address_space


class ArrayTypeNode(TypeNode):
    """LLVM IR array type."""
    
    def __init__(self, element_type: TypeNode, size: int, location: Optional[LLVMIRSourceLocation] = None):
        name = f"[{size} x {element_type.name}]"
        super().__init__(name, None, location)
        self.element_type = element_type
        self.size = size


class VectorTypeNode(TypeNode):
    """LLVM IR vector type."""
    
    def __init__(self, element_type: TypeNode, size: int, scalable: bool = False, location: Optional[LLVMIRSourceLocation] = None):
        if scalable:
            name = f"<vscale x {size} x {element_type.name}>"
        else:
            name = f"<{size} x {element_type.name}>"
        super().__init__(name, None, location)
        self.element_type = element_type
        self.size = size
        self.scalable = scalable


class StructTypeNode(TypeNode):
    """LLVM IR struct type."""
    
    def __init__(self, fields: List[TypeNode], packed: bool = False, name: Optional[str] = None, location: Optional[LLVMIRSourceLocation] = None):
        if name:
            type_name = f"%{name}"
        else:
            field_names = ", ".join(field.name for field in fields)
            if packed:
                type_name = f"<{{{field_names}}}>"
            else:
                type_name = f"{{{field_names}}}"
        super().__init__(type_name, None, location)
        self.fields = fields
        self.packed = packed
        self.struct_name = name


class FunctionTypeNode(TypeNode):
    """LLVM IR function type."""
    
    def __init__(self, return_type: TypeNode, param_types: List[TypeNode], is_vararg: bool = False, location: Optional[LLVMIRSourceLocation] = None):
        param_names = ", ".join(param.name for param in param_types)
        if is_vararg:
            param_names += ", ..."
        name = f"{return_type.name} ({param_names})"
        super().__init__(name, None, location)
        self.return_type = return_type
        self.param_types = param_types
        self.is_vararg = is_vararg


class LabelTypeNode(TypeNode):
    """LLVM IR label type."""
    
    def __init__(self, location: Optional[LLVMIRSourceLocation] = None):
        super().__init__("label", None, location)


class MetadataTypeNode(TypeNode):
    """LLVM IR metadata type."""
    
    def __init__(self, location: Optional[LLVMIRSourceLocation] = None):
        super().__init__("metadata", None, location)


class TokenTypeNode(TypeNode):
    """LLVM IR token type."""
    
    def __init__(self, location: Optional[LLVMIRSourceLocation] = None):
        super().__init__("token", None, location)


# Value Nodes

class ValueNode(LLVMIRNode):
    """Base class for LLVM IR values."""
    
    def __init__(self, value_type: TypeNode, name: Optional[str] = None, location: Optional[LLVMIRSourceLocation] = None):
        super().__init__(location)
        self.value_type = value_type
        self.name = name
        self.uses: List['UseNode'] = []
        self.is_constant = False
    
    def accept(self, visitor: LLVMIRVisitor) -> Any:
        return visitor.visit_value(self)
    
    def add_use(self, use: 'UseNode') -> None:
        """Add a use of this value."""
        self.uses.append(use)
    
    def get_name(self) -> str:
        """Get the value name."""
        return self.name if self.name else f"<unnamed_{id(self)}>"
    
    def __str__(self) -> str:
        return f"{self.value_type.name} {self.get_name()}"


class ConstantNode(ValueNode):
    """Base class for LLVM IR constants."""
    
    def __init__(self, value_type: TypeNode, value: Any, location: Optional[LLVMIRSourceLocation] = None):
        super().__init__(value_type, None, location)
        self.value = value
        self.is_constant = True


class IntegerConstantNode(ConstantNode):
    """LLVM IR integer constant."""
    
    def __init__(self, value: int, bit_width: int, location: Optional[LLVMIRSourceLocation] = None):
        super().__init__(IntegerTypeNode(bit_width), value, location)
    
    def __str__(self) -> str:
        return f"{self.value_type.name} {self.value}"


class FloatConstantNode(ConstantNode):
    """LLVM IR floating-point constant."""
    
    def __init__(self, value: float, precision: str, location: Optional[LLVMIRSourceLocation] = None):
        super().__init__(FloatTypeNode(precision), value, location)
    
    def __str__(self) -> str:
        return f"{self.value_type.name} {self.value}"


class BoolConstantNode(ConstantNode):
    """LLVM IR boolean constant (i1)."""
    
    def __init__(self, value: bool, location: Optional[LLVMIRSourceLocation] = None):
        super().__init__(IntegerTypeNode(1), value, location)
    
    def __str__(self) -> str:
        return f"i1 {str(self.value).lower()}"


class NullConstantNode(ConstantNode):
    """LLVM IR null constant."""
    
    def __init__(self, pointer_type: PointerTypeNode, location: Optional[LLVMIRSourceLocation] = None):
        super().__init__(pointer_type, None, location)
    
    def __str__(self) -> str:
        return f"{self.value_type.name} null"


class UndefConstantNode(ConstantNode):
    """LLVM IR undef constant."""
    
    def __init__(self, value_type: TypeNode, location: Optional[LLVMIRSourceLocation] = None):
        super().__init__(value_type, "undef", location)
    
    def __str__(self) -> str:
        return f"{self.value_type.name} undef"


class PoisonConstantNode(ConstantNode):
    """LLVM IR poison constant."""
    
    def __init__(self, value_type: TypeNode, location: Optional[LLVMIRSourceLocation] = None):
        super().__init__(value_type, "poison", location)
    
    def __str__(self) -> str:
        return f"{self.value_type.name} poison"


class GlobalVariableNode(ValueNode):
    """LLVM IR global variable."""
    
    def __init__(self, name: str, value_type: TypeNode, initializer: Optional[ConstantNode] = None,
                 linkage: str = "external", visibility: str = "default", thread_local: bool = False,
                 unnamed_addr: bool = False, constant: bool = False, location: Optional[LLVMIRSourceLocation] = None):
        super().__init__(PointerTypeNode(value_type), name, location)
        self.global_type = value_type
        self.initializer = initializer
        self.linkage = linkage
        self.visibility = visibility
        self.thread_local = thread_local
        self.unnamed_addr = unnamed_addr
        self.constant = constant
        self.alignment: Optional[int] = None
        self.section: Optional[str] = None
        self.comdat: Optional[str] = None
    
    def __str__(self) -> str:
        result = f"@{self.name} = "
        if self.linkage != "external":
            result += f"{self.linkage} "
        if self.visibility != "default":
            result += f"{self.visibility} "
        if self.thread_local:
            result += "thread_local "
        if self.unnamed_addr:
            result += "unnamed_addr "
        if self.constant:
            result += "constant "
        else:
            result += "global "
        result += f"{self.global_type.name}"
        if self.initializer:
            result += f" {self.initializer}"
        return result


class ArgumentNode(ValueNode):
    """LLVM IR function argument."""
    
    def __init__(self, value_type: TypeNode, name: Optional[str] = None, location: Optional[LLVMIRSourceLocation] = None):
        super().__init__(value_type, name, location)
        self.attributes: List[str] = []
    
    def __str__(self) -> str:
        result = f"{self.value_type.name}"
        if self.attributes:
            result = " ".join(self.attributes) + " " + result
        if self.name:
            result += f" %{self.name}"
        return result


# Instruction Nodes

class InstructionNode(ValueNode):
    """Base class for LLVM IR instructions."""
    
    def __init__(self, opcode: str, value_type: TypeNode, operands: List[ValueNode], name: Optional[str] = None, location: Optional[LLVMIRSourceLocation] = None):
        super().__init__(value_type, name, location)
        self.opcode = opcode
        self.operands = operands
        self.attributes: Dict[str, Any] = {}
        self.debug_info: Optional[Dict[str, Any]] = None
        self.fast_math_flags: Set[str] = set()
    
    def accept(self, visitor: LLVMIRVisitor) -> Any:
        return visitor.visit_instruction(self)
    
    def get_operand(self, index: int) -> ValueNode:
        """Get operand by index."""
        return self.operands[index]
    
    def set_operand(self, index: int, value: ValueNode) -> None:
        """Set operand by index."""
        self.operands[index] = value
    
    def add_attribute(self, name: str, value: Any = True) -> None:
        """Add instruction attribute."""
        self.attributes[name] = value
    
    def has_side_effects(self) -> bool:
        """Check if instruction has side effects."""
        side_effect_opcodes = {
            "store", "call", "invoke", "fence", "atomicrmw", "cmpxchg",
            "load",  # can have side effects with volatile
        }
        return self.opcode in side_effect_opcodes
    
    def is_terminator(self) -> bool:
        """Check if instruction is a terminator."""
        terminator_opcodes = {
            "ret", "br", "switch", "indirectbr", "invoke", "resume",
            "catchswitch", "catchret", "cleanupret", "unreachable"
        }
        return self.opcode in terminator_opcodes
    
    def __str__(self) -> str:
        result = ""
        if self.name and not isinstance(self.value_type, VoidTypeNode):
            result += f"%{self.name} = "
        
        result += self.opcode
        
        # Add operands
        if self.operands:
            operand_strs = []
            for operand in self.operands:
                operand_strs.append(str(operand))
            result += " " + ", ".join(operand_strs)
        
        return result


# Arithmetic Instructions

class BinaryOpNode(InstructionNode):
    """LLVM IR binary operation instruction."""
    
    def __init__(self, opcode: str, left: ValueNode, right: ValueNode, name: Optional[str] = None, location: Optional[LLVMIRSourceLocation] = None):
        super().__init__(opcode, left.value_type, [left, right], name, location)
        self.left = left
        self.right = right


class AddNode(BinaryOpNode):
    """LLVM IR add instruction."""
    
    def __init__(self, left: ValueNode, right: ValueNode, nsw: bool = False, nuw: bool = False, name: Optional[str] = None, location: Optional[LLVMIRSourceLocation] = None):
        super().__init__("add", left, right, name, location)
        self.nsw = nsw
        self.nuw = nuw


class SubNode(BinaryOpNode):
    """LLVM IR sub instruction."""
    
    def __init__(self, left: ValueNode, right: ValueNode, nsw: bool = False, nuw: bool = False, name: Optional[str] = None, location: Optional[LLVMIRSourceLocation] = None):
        super().__init__("sub", left, right, name, location)
        self.nsw = nsw
        self.nuw = nuw


class MulNode(BinaryOpNode):
    """LLVM IR mul instruction."""
    
    def __init__(self, left: ValueNode, right: ValueNode, nsw: bool = False, nuw: bool = False, name: Optional[str] = None, location: Optional[LLVMIRSourceLocation] = None):
        super().__init__("mul", left, right, name, location)
        self.nsw = nsw
        self.nuw = nuw


class DivNode(BinaryOpNode):
    """Base for LLVM IR division instructions."""
    pass


class UDivNode(DivNode):
    """LLVM IR udiv instruction."""
    
    def __init__(self, left: ValueNode, right: ValueNode, exact: bool = False, name: Optional[str] = None, location: Optional[LLVMIRSourceLocation] = None):
        super().__init__("udiv", left, right, name, location)
        self.exact = exact


class SDivNode(DivNode):
    """LLVM IR sdiv instruction."""
    
    def __init__(self, left: ValueNode, right: ValueNode, exact: bool = False, name: Optional[str] = None, location: Optional[LLVMIRSourceLocation] = None):
        super().__init__("sdiv", left, right, name, location)
        self.exact = exact


class FDivNode(DivNode):
    """LLVM IR fdiv instruction."""
    
    def __init__(self, left: ValueNode, right: ValueNode, name: Optional[str] = None, location: Optional[LLVMIRSourceLocation] = None):
        super().__init__("fdiv", left, right, name, location)


# Memory Instructions

class AllocaNode(InstructionNode):
    """LLVM IR alloca instruction."""
    
    def __init__(self, allocated_type: TypeNode, array_size: Optional[ValueNode] = None, alignment: Optional[int] = None, name: Optional[str] = None, location: Optional[LLVMIRSourceLocation] = None):
        operands = [array_size] if array_size else []
        super().__init__("alloca", PointerTypeNode(allocated_type), operands, name, location)
        self.allocated_type = allocated_type
        self.array_size = array_size
        self.alignment = alignment


class LoadNode(InstructionNode):
    """LLVM IR load instruction."""
    
    def __init__(self, pointer: ValueNode, volatile: bool = False, alignment: Optional[int] = None, name: Optional[str] = None, location: Optional[LLVMIRSourceLocation] = None):
        # Get pointee type
        if isinstance(pointer.value_type, PointerTypeNode):
            loaded_type = pointer.value_type.pointee_type
        else:
            loaded_type = pointer.value_type  # Fallback
        
        super().__init__("load", loaded_type, [pointer], name, location)
        self.pointer = pointer
        self.volatile = volatile
        self.alignment = alignment


class StoreNode(InstructionNode):
    """LLVM IR store instruction."""
    
    def __init__(self, value: ValueNode, pointer: ValueNode, volatile: bool = False, alignment: Optional[int] = None, location: Optional[LLVMIRSourceLocation] = None):
        super().__init__("store", VoidTypeNode(), [value, pointer], None, location)
        self.stored_value = value
        self.pointer = pointer
        self.volatile = volatile
        self.alignment = alignment


class GetElementPtrNode(InstructionNode):
    """LLVM IR getelementptr instruction."""
    
    def __init__(self, base_type: TypeNode, pointer: ValueNode, indices: List[ValueNode], inbounds: bool = False, name: Optional[str] = None, location: Optional[LLVMIRSourceLocation] = None):
        super().__init__("getelementptr", PointerTypeNode(base_type), [pointer] + indices, name, location)
        self.base_type = base_type
        self.pointer = pointer
        self.indices = indices
        self.inbounds = inbounds


# Control Flow Instructions

class BranchNode(InstructionNode):
    """LLVM IR branch instruction."""
    
    def __init__(self, condition: Optional[ValueNode] = None, true_block: Optional['BasicBlockNode'] = None, false_block: Optional['BasicBlockNode'] = None, location: Optional[LLVMIRSourceLocation] = None):
        if condition:
            # Conditional branch
            operands = [condition]
            self.condition = condition
            self.true_block = true_block
            self.false_block = false_block
        else:
            # Unconditional branch
            operands = []
            self.condition = None
            self.true_block = true_block
            self.false_block = None
        
        super().__init__("br", VoidTypeNode(), operands, None, location)


class ReturnNode(InstructionNode):
    """LLVM IR return instruction."""
    
    def __init__(self, return_value: Optional[ValueNode] = None, location: Optional[LLVMIRSourceLocation] = None):
        operands = [return_value] if return_value else []
        super().__init__("ret", VoidTypeNode(), operands, None, location)
        self.return_value = return_value


class CallNode(InstructionNode):
    """LLVM IR call instruction."""
    
    def __init__(self, function: ValueNode, arguments: List[ValueNode], calling_convention: Optional[str] = None, name: Optional[str] = None, location: Optional[LLVMIRSourceLocation] = None):
        # Determine return type
        if isinstance(function.value_type, FunctionTypeNode):
            return_type = function.value_type.return_type
        else:
            return_type = VoidTypeNode()  # Fallback
        
        super().__init__("call", return_type, [function] + arguments, name, location)
        self.function = function
        self.arguments = arguments
        self.calling_convention = calling_convention
        self.tail_call = False
        self.no_tail_call = False


class ICmpNode(InstructionNode):
    """LLVM IR icmp instruction."""
    
    def __init__(self, predicate: str, left: ValueNode, right: ValueNode, name: Optional[str] = None, location: Optional[LLVMIRSourceLocation] = None):
        super().__init__("icmp", IntegerTypeNode(1), [left, right], name, location)
        self.predicate = predicate
        self.left = left
        self.right = right


class FCmpNode(InstructionNode):
    """LLVM IR fcmp instruction."""
    
    def __init__(self, predicate: str, left: ValueNode, right: ValueNode, name: Optional[str] = None, location: Optional[LLVMIRSourceLocation] = None):
        super().__init__("fcmp", IntegerTypeNode(1), [left, right], name, location)
        self.predicate = predicate
        self.left = left
        self.right = right


class SelectNode(InstructionNode):
    """LLVM IR select instruction."""
    
    def __init__(self, condition: ValueNode, true_value: ValueNode, false_value: ValueNode, name: Optional[str] = None, location: Optional[LLVMIRSourceLocation] = None):
        super().__init__("select", true_value.value_type, [condition, true_value, false_value], name, location)
        self.condition = condition
        self.true_value = true_value
        self.false_value = false_value


# Cast Instructions

class CastNode(InstructionNode):
    """Base class for LLVM IR cast instructions."""
    
    def __init__(self, opcode: str, value: ValueNode, target_type: TypeNode, name: Optional[str] = None, location: Optional[LLVMIRSourceLocation] = None):
        super().__init__(opcode, target_type, [value], name, location)
        self.cast_value = value
        self.target_type = target_type


class TruncNode(CastNode):
    """LLVM IR trunc instruction."""
    
    def __init__(self, value: ValueNode, target_type: TypeNode, name: Optional[str] = None, location: Optional[LLVMIRSourceLocation] = None):
        super().__init__("trunc", value, target_type, name, location)


class ZExtNode(CastNode):
    """LLVM IR zext instruction."""
    
    def __init__(self, value: ValueNode, target_type: TypeNode, name: Optional[str] = None, location: Optional[LLVMIRSourceLocation] = None):
        super().__init__("zext", value, target_type, name, location)


class SExtNode(CastNode):
    """LLVM IR sext instruction."""
    
    def __init__(self, value: ValueNode, target_type: TypeNode, name: Optional[str] = None, location: Optional[LLVMIRSourceLocation] = None):
        super().__init__("sext", value, target_type, name, location)


class BitCastNode(CastNode):
    """LLVM IR bitcast instruction."""
    
    def __init__(self, value: ValueNode, target_type: TypeNode, name: Optional[str] = None, location: Optional[LLVMIRSourceLocation] = None):
        super().__init__("bitcast", value, target_type, name, location)


# PHI Node

class PhiNode(InstructionNode):
    """LLVM IR phi instruction."""
    
    def __init__(self, value_type: TypeNode, incoming: List[Tuple[ValueNode, 'BasicBlockNode']], name: Optional[str] = None, location: Optional[LLVMIRSourceLocation] = None):
        operands = [value for value, block in incoming]
        super().__init__("phi", value_type, operands, name, location)
        self.incoming = incoming
    
    def add_incoming(self, value: ValueNode, block: 'BasicBlockNode') -> None:
        """Add an incoming value and block."""
        self.incoming.append((value, block))
        self.operands.append(value)


# Basic Block and Function Nodes

class BasicBlockNode(LLVMIRNode):
    """LLVM IR basic block."""
    
    def __init__(self, name: Optional[str] = None, instructions: Optional[List[InstructionNode]] = None, location: Optional[LLVMIRSourceLocation] = None):
        super().__init__(location)
        self.name = name
        self.instructions = instructions or []
        self.predecessors: List['BasicBlockNode'] = []
        self.successors: List['BasicBlockNode'] = []
        self.parent_function: Optional['FunctionNode'] = None
    
    def accept(self, visitor: LLVMIRVisitor) -> Any:
        return visitor.visit_basic_block(self)
    
    def add_instruction(self, instruction: InstructionNode) -> None:
        """Add an instruction to the basic block."""
        self.instructions.append(instruction)
        instruction.parent = self
    
    def get_terminator(self) -> Optional[InstructionNode]:
        """Get the terminator instruction."""
        if self.instructions and self.instructions[-1].is_terminator():
            return self.instructions[-1]
        return None
    
    def is_entry_block(self) -> bool:
        """Check if this is the entry block of a function."""
        return (self.parent_function and 
                self.parent_function.basic_blocks and 
                self.parent_function.basic_blocks[0] == self)
    
    def __str__(self) -> str:
        name = self.name or f"bb_{id(self)}"
        return f"{name}:"


class FunctionNode(LLVMIRNode):
    """LLVM IR function definition."""
    
    def __init__(self, name: str, function_type: FunctionTypeNode, linkage: str = "external", 
                 visibility: str = "default", calling_convention: Optional[str] = None,
                 basic_blocks: Optional[List[BasicBlockNode]] = None, location: Optional[LLVMIRSourceLocation] = None):
        super().__init__(location)
        self.name = name
        self.function_type = function_type
        self.linkage = linkage
        self.visibility = visibility
        self.calling_convention = calling_convention
        self.basic_blocks = basic_blocks or []
        self.arguments: List[ArgumentNode] = []
        self.attributes: List[str] = []
        self.return_attributes: List[str] = []
        self.function_attributes: List[str] = []
        self.personality: Optional[ValueNode] = None
        self.gc: Optional[str] = None
        self.section: Optional[str] = None
        self.comdat: Optional[str] = None
        self.alignment: Optional[int] = None
        
        # Set up arguments
        for i, param_type in enumerate(function_type.param_types):
            arg = ArgumentNode(param_type, f"arg{i}")
            self.arguments.append(arg)
        
        # Set parent references
        for block in self.basic_blocks:
            block.parent_function = self
    
    def accept(self, visitor: LLVMIRVisitor) -> Any:
        return visitor.visit_function(self)
    
    def add_basic_block(self, block: BasicBlockNode) -> None:
        """Add a basic block to the function."""
        self.basic_blocks.append(block)
        block.parent_function = self
    
    def get_entry_block(self) -> Optional[BasicBlockNode]:
        """Get the entry basic block."""
        return self.basic_blocks[0] if self.basic_blocks else None
    
    def is_declaration(self) -> bool:
        """Check if this is a function declaration (no body)."""
        return len(self.basic_blocks) == 0
    
    def __str__(self) -> str:
        result = f"define {self.linkage} {self.function_type.return_type.name} @{self.name}("
        
        # Add parameters
        param_strs = []
        for arg in self.arguments:
            param_strs.append(str(arg))
        result += ", ".join(param_strs)
        
        result += ")"
        
        if self.is_declaration():
            return result
        else:
            return result + " {"


class ModuleNode(LLVMIRNode):
    """LLVM IR module (top-level container)."""
    
    def __init__(self, name: str = "", target_triple: Optional[str] = None, 
                 data_layout: Optional[str] = None, location: Optional[LLVMIRSourceLocation] = None):
        super().__init__(location)
        self.name = name
        self.target_triple = target_triple
        self.data_layout = data_layout
        self.functions: List[FunctionNode] = []
        self.globals: List[GlobalVariableNode] = []
        self.aliases: List['AliasNode'] = []
        self.metadata: Dict[str, Any] = {}
        self.named_metadata: Dict[str, List[Any]] = {}
        self.comdat_definitions: Dict[str, str] = {}
        self.attribute_groups: Dict[int, List[str]] = {}
    
    def accept(self, visitor: LLVMIRVisitor) -> Any:
        return visitor.visit_module(self)
    
    def add_function(self, function: FunctionNode) -> None:
        """Add a function to the module."""
        self.functions.append(function)
        function.parent = self
    
    def add_global(self, global_var: GlobalVariableNode) -> None:
        """Add a global variable to the module."""
        self.globals.append(global_var)
        global_var.parent = self
    
    def get_function(self, name: str) -> Optional[FunctionNode]:
        """Get a function by name."""
        for func in self.functions:
            if func.name == name:
                return func
        return None
    
    def get_global(self, name: str) -> Optional[GlobalVariableNode]:
        """Get a global variable by name."""
        for glob in self.globals:
            if glob.name == name:
                return glob
        return None


# Additional Nodes

class AliasNode(LLVMIRNode):
    """LLVM IR alias definition."""
    
    def __init__(self, name: str, aliasee: ValueNode, linkage: str = "external", 
                 visibility: str = "default", location: Optional[LLVMIRSourceLocation] = None):
        super().__init__(location)
        self.name = name
        self.aliasee = aliasee
        self.linkage = linkage
        self.visibility = visibility
    
    def accept(self, visitor: LLVMIRVisitor) -> Any:
        return visitor.visit_value(self)


class UseNode:
    """Represents a use of a value."""
    
    def __init__(self, user: InstructionNode, used: ValueNode, operand_index: int):
        self.user = user
        self.used = used
        self.operand_index = operand_index


# Utility Functions

def validate_llvm_ir_ast(node: LLVMIRNode) -> List[str]:
    """Validate LLVM IR AST for correctness."""
    issues = []
    
    if isinstance(node, ModuleNode):
        # Validate module
        for func in node.functions:
            func_issues = validate_llvm_ir_ast(func)
            issues.extend(func_issues)
    
    elif isinstance(node, FunctionNode):
        # Validate function
        if not node.basic_blocks and not node.is_declaration():
            issues.append(f"Function {node.name} has no basic blocks")
        
        for block in node.basic_blocks:
            block_issues = validate_llvm_ir_ast(block)
            issues.extend(block_issues)
    
    elif isinstance(node, BasicBlockNode):
        # Validate basic block
        if not node.instructions:
            issues.append("Basic block has no instructions")
        
        terminator = node.get_terminator()
        if not terminator:
            issues.append("Basic block has no terminator")
    
    return issues


def optimize_llvm_ir_ast(node: LLVMIRNode) -> LLVMIRNode:
    """Apply basic optimizations to LLVM IR AST."""
    # This would implement basic optimizations like:
    # - Dead code elimination
    # - Constant folding
    # - Instruction combining
    # For now, return the node unchanged
    return node


def get_node_info(node: LLVMIRNode) -> Dict[str, Any]:
    """Get information about an LLVM IR AST node."""
    info = {
        "type": node.get_type(),
        "location": node.location,
        "children_count": len(node.children),
        "metadata": node.metadata
    }
    
    if isinstance(node, ValueNode):
        info["value_type"] = str(node.value_type)
        info["name"] = node.name
        info["is_constant"] = node.is_constant
    
    if isinstance(node, InstructionNode):
        info["opcode"] = node.opcode
        info["operand_count"] = len(node.operands)
        info["has_side_effects"] = node.has_side_effects()
        info["is_terminator"] = node.is_terminator()
    
    return info


def create_llvm_ir_node(node_type: str, **kwargs) -> LLVMIRNode:
    """Factory function to create LLVM IR AST nodes."""
    node_classes = {
        "module": ModuleNode,
        "function": FunctionNode,
        "basic_block": BasicBlockNode,
        "add": AddNode,
        "sub": SubNode,
        "mul": MulNode,
        "alloca": AllocaNode,
        "load": LoadNode,
        "store": StoreNode,
        "call": CallNode,
        "ret": ReturnNode,
        "br": BranchNode,
        "icmp": ICmpNode,
        "fcmp": FCmpNode,
        "phi": PhiNode,
        # Add more as needed
    }
    
    if node_type not in node_classes:
        raise ValueError(f"Unknown node type: {node_type}")
    
    return node_classes[node_type](**kwargs) 