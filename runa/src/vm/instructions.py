"""
Instruction set for the Runa Virtual Machine.

This module defines the complete instruction set used by the Runa VM,
including all opcodes and their operand formats.
"""

from enum import Enum, auto
from typing import List, Union, Optional, Any, Dict, Tuple
import struct
from dataclasses import dataclass


class OpCode(Enum):
    """
    Operation codes for the Runa Virtual Machine.
    
    The VM uses a stack-based architecture with these main instruction categories:
    - Stack manipulation: PUSH, POP, DUP, etc.
    - Arithmetic: ADD, SUB, MUL, DIV, etc.
    - Comparison: EQ, NE, LT, GT, etc.
    - Control flow: JMP, JZ, JNZ, CALL, RET, etc.
    - Memory: LOAD, STORE, etc.
    - Function: CALL, RET, etc.
    - Object: NEW, GETATTR, SETATTR, etc.
    """
    
    # Stack manipulation instructions
    NOP = auto()           # No operation
    PUSH = auto()          # Push constant onto stack
    POP = auto()           # Pop value from stack
    DUP = auto()           # Duplicate top of stack
    DUP_X1 = auto()        # Duplicate top of stack and insert below second value
    DUP_X2 = auto()        # Duplicate top of stack and insert below third value
    SWAP = auto()          # Swap top two values on stack
    ROT = auto()           # Rotate top three values on stack
    
    # Constant loading instructions
    PUSH_NULL = auto()     # Push null onto stack
    PUSH_TRUE = auto()     # Push true onto stack
    PUSH_FALSE = auto()    # Push false onto stack
    PUSH_INT = auto()      # Push integer constant onto stack
    PUSH_FLOAT = auto()    # Push float constant onto stack
    PUSH_STRING = auto()   # Push string constant onto stack
    
    # Arithmetic instructions
    ADD = auto()           # Add top two values on stack
    SUB = auto()           # Subtract top value from second value on stack
    MUL = auto()           # Multiply top two values on stack
    DIV = auto()           # Divide second value by top value on stack
    MOD = auto()           # Modulo second value by top value on stack
    NEG = auto()           # Negate top value on stack
    INC = auto()           # Increment top value on stack
    DEC = auto()           # Decrement top value on stack
    POW = auto()           # Raise second value to the power of top value
    
    # Bitwise instructions
    BIT_AND = auto()       # Bitwise AND top two values on stack
    BIT_OR = auto()        # Bitwise OR top two values on stack
    BIT_XOR = auto()       # Bitwise XOR top two values on stack
    BIT_NOT = auto()       # Bitwise NOT top value on stack
    SHL = auto()           # Shift left second value by top value on stack
    SHR = auto()           # Shift right second value by top value on stack
    
    # Logical instructions
    AND = auto()           # Logical AND top two values on stack
    OR = auto()            # Logical OR top two values on stack
    NOT = auto()           # Logical NOT top value on stack
    
    # Comparison instructions
    EQ = auto()            # Push true if top two values are equal
    NE = auto()            # Push true if top two values are not equal
    LT = auto()            # Push true if second value is less than top value
    LE = auto()            # Push true if second value is less than or equal to top value
    GT = auto()            # Push true if second value is greater than top value
    GE = auto()            # Push true if second value is greater than or equal to top value
    IS = auto()            # Push true if top two values are identical (same object)
    INSTANCE_OF = auto()   # Check if value is instance of type
    
    # Control flow instructions
    JMP = auto()           # Unconditional jump to offset
    JZ = auto()            # Jump to offset if top of stack is zero/false
    JNZ = auto()           # Jump to offset if top of stack is non-zero/true
    CALL = auto()          # Call function by name with arguments on stack
    CALL_METHOD = auto()   # Call method on object with arguments on stack
    RET = auto()           # Return from function with top of stack as return value
    THROW = auto()         # Throw exception with top of stack as exception object
    ENTER_TRY = auto()     # Enter try block with handler at offset
    EXIT_TRY = auto()      # Exit try block
    
    # Variable instructions
    LOAD_LOCAL = auto()    # Load local variable onto stack
    STORE_LOCAL = auto()   # Store top of stack to local variable
    LOAD_GLOBAL = auto()   # Load global variable onto stack
    STORE_GLOBAL = auto()  # Store top of stack to global variable
    LOAD_UPVALUE = auto()  # Load upvalue (captured variable) onto stack
    STORE_UPVALUE = auto() # Store top of stack to upvalue
    
    # Function instructions
    MAKE_FUNCTION = auto() # Create function object from code object
    MAKE_CLOSURE = auto()  # Create closure (function with upvalues)
    
    # Collection instructions
    BUILD_LIST = auto()    # Build list from values on stack
    BUILD_DICT = auto()    # Build dictionary from key/value pairs on stack
    GET_ITEM = auto()      # Get item from collection with index/key on stack
    SET_ITEM = auto()      # Set item in collection with index/key and value on stack
    APPEND = auto()        # Append top of stack to list
    
    # Object instructions
    NEW = auto()           # Create new object of type on stack
    GET_ATTR = auto()      # Get attribute from object
    SET_ATTR = auto()      # Set attribute on object
    
    # Module instructions
    IMPORT = auto()        # Import module
    EXPORT = auto()        # Export symbol from module
    MODULE_GET = auto()    # Get value from module
    MODULE_SET = auto()    # Set value in module
    MODULE_CALL = auto()   # Call function in module
    NAMESPACE_CREATE = auto()  # Create a new namespace
    NAMESPACE_GET = auto()     # Get value from namespace
    NAMESPACE_SET = auto()     # Set value in namespace
    MODULE_RESOLVE = auto()    # Resolve a module path
    
    # Iterator instructions
    ITER = auto()          # Create iterator from value on stack
    NEXT = auto()          # Get next value from iterator
    
    # Type instructions
    IS_TYPE = auto()       # Check if value is of specified type
    CAST = auto()          # Cast value to specified type
    
    # Memory management instructions
    GC_COLLECT = auto()    # Force garbage collection
    
    # Debug instructions
    BREAKPOINT = auto()    # Insert breakpoint for debugger
    LINE = auto()          # Set current line number for debug info
    
    # Meta instructions
    LOAD_CONST = auto()    # Load constant from constant pool
    MAKE_TYPE = auto()     # Create new type
    EXTEND_TYPE = auto()   # Extend existing type
    
    # Vector operations for AI
    VEC_ADD = auto()       # Add vectors
    VEC_SUB = auto()       # Subtract vectors
    VEC_MUL = auto()       # Multiply vectors
    VEC_DIV = auto()       # Divide vectors
    VEC_DOT = auto()       # Dot product of vectors
    
    # Tensor operations for ML
    TENSOR_ADD = auto()    # Add tensors
    TENSOR_SUB = auto()    # Subtract tensors
    TENSOR_MUL = auto()    # Multiply tensors
    TENSOR_DIV = auto()    # Divide tensors
    TENSOR_MATMUL = auto() # Matrix multiplication of tensors
    
    # Neural network operations
    NN_FORWARD = auto()    # Forward pass of neural network
    NN_BACKWARD = auto()   # Backward pass of neural network
    NN_UPDATE = auto()     # Update neural network weights
    
    # Knowledge graph operations
    KG_QUERY = auto()      # Execute a knowledge graph query
    KG_CREATE = auto()     # Create a node or relationship in the knowledge graph
    
    # Error handling
    TRY_BEGIN = auto()      # Begin try block, with offset to catch block
    TRY_END = auto()        # End try block, with offset to end of catch block
    CATCH_BEGIN = auto()    # Begin catch block
    CATCH_END = auto()      # End catch block
    
    # Closure support
    CREATE_CLOSURE = auto() # Create a closure
    CAPTURE_VAR = auto()    # Capture a variable in the closure
    LOAD_CAPTURED = auto()  # Load a captured variable
    STORE_CAPTURED = auto() # Store to a captured variable

    # Advanced control flow
    JUMP_IF_FALSE = auto()  # Jump if false (for short-circuit AND)
    JUMP_IF_TRUE = auto()   # Jump if true (for short-circuit OR)


@dataclass
class Instruction:
    """
    Represents a single instruction in the Runa bytecode.
    
    Attributes:
        opcode: The operation code
        operands: Optional operands for the instruction
        line: The source code line number (for debugging)
    """
    
    opcode: OpCode
    operands: List[Any] = None
    line: int = 0
    
    def __post_init__(self):
        """Initialize default values for None fields."""
        if self.operands is None:
            self.operands = []
    
    def __str__(self) -> str:
        """Return a string representation of the instruction."""
        if not self.operands:
            return f"{self.opcode.name}"
        return f"{self.opcode.name} {', '.join(str(op) for op in self.operands)}"
    
    def encode(self) -> bytes:
        """
        Encode the instruction as bytes.
        
        Returns:
            The encoded instruction
        """
        # Encode opcode as a single byte
        result = bytes([self.opcode.value])
        
        # Encode operands based on instruction format
        if self.opcode in [OpCode.PUSH_INT, OpCode.PUSH_FLOAT]:
            # Numeric constants are encoded as 8 bytes (double)
            value = self.operands[0]
            if self.opcode == OpCode.PUSH_INT:
                result += struct.pack(">q", value)  # 8-byte signed integer
            else:
                result += struct.pack(">d", value)  # 8-byte double
        
        elif self.opcode == OpCode.PUSH_STRING:
            # Strings are encoded as length + bytes
            value = self.operands[0].encode('utf-8')
            length = len(value)
            result += struct.pack(">I", length)  # 4-byte unsigned integer
            result += value
        
        elif self.opcode in [OpCode.JMP, OpCode.JZ, OpCode.JNZ, OpCode.ENTER_TRY]:
            # Jump offsets are encoded as 4-byte signed integers
            result += struct.pack(">i", self.operands[0])
        
        elif self.opcode in [OpCode.LOAD_LOCAL, OpCode.STORE_LOCAL,
                            OpCode.LOAD_GLOBAL, OpCode.STORE_GLOBAL,
                            OpCode.LOAD_UPVALUE, OpCode.STORE_UPVALUE]:
            # Variable indices are encoded as 4-byte unsigned integers
            result += struct.pack(">I", self.operands[0])
        
        elif self.opcode in [OpCode.BUILD_LIST, OpCode.BUILD_DICT]:
            # Collection sizes are encoded as 4-byte unsigned integers
            result += struct.pack(">I", self.operands[0])
        
        elif self.opcode == OpCode.LINE:
            # Line numbers are encoded as 4-byte unsigned integers
            result += struct.pack(">I", self.operands[0])
        
        # Debug information - line number
        result += struct.pack(">I", self.line)
        
        return result
    
    @classmethod
    def decode(cls, data: bytes, offset: int = 0) -> Tuple['Instruction', int]:
        """
        Decode an instruction from bytes.
        
        Args:
            data: The encoded data
            offset: The offset to start decoding from
            
        Returns:
            A tuple of (instruction, new_offset)
        """
        # Decode opcode
        opcode_value = data[offset]
        opcode = OpCode(opcode_value)
        offset += 1
        
        operands = []
        
        # Decode operands based on instruction format
        if opcode in [OpCode.PUSH_INT, OpCode.PUSH_FLOAT]:
            if opcode == OpCode.PUSH_INT:
                value = struct.unpack(">q", data[offset:offset+8])[0]
            else:
                value = struct.unpack(">d", data[offset:offset+8])[0]
            operands.append(value)
            offset += 8
        
        elif opcode == OpCode.PUSH_STRING:
            length = struct.unpack(">I", data[offset:offset+4])[0]
            offset += 4
            value = data[offset:offset+length].decode('utf-8')
            operands.append(value)
            offset += length
        
        elif opcode in [OpCode.JMP, OpCode.JZ, OpCode.JNZ, OpCode.ENTER_TRY]:
            value = struct.unpack(">i", data[offset:offset+4])[0]
            operands.append(value)
            offset += 4
        
        elif opcode in [OpCode.LOAD_LOCAL, OpCode.STORE_LOCAL,
                       OpCode.LOAD_GLOBAL, OpCode.STORE_GLOBAL,
                       OpCode.LOAD_UPVALUE, OpCode.STORE_UPVALUE]:
            value = struct.unpack(">I", data[offset:offset+4])[0]
            operands.append(value)
            offset += 4
        
        elif opcode in [OpCode.BUILD_LIST, OpCode.BUILD_DICT]:
            value = struct.unpack(">I", data[offset:offset+4])[0]
            operands.append(value)
            offset += 4
        
        elif opcode == OpCode.LINE:
            value = struct.unpack(">I", data[offset:offset+4])[0]
            operands.append(value)
            offset += 4
        
        # Decode debug information - line number
        line = struct.unpack(">I", data[offset:offset+4])[0]
        offset += 4
        
        return cls(opcode, operands, line), offset


# Define instruction formats for documentation and validation
INSTRUCTION_FORMATS = {
    # No operands
    OpCode.NOP: [],
    OpCode.POP: [],
    OpCode.DUP: [],
    OpCode.SWAP: [],
    OpCode.ROT: [],
    OpCode.ADD: [],
    OpCode.SUB: [],
    OpCode.MUL: [],
    OpCode.DIV: [],
    OpCode.MOD: [],
    OpCode.NEG: [],
    OpCode.INC: [],
    OpCode.DEC: [],
    OpCode.BIT_AND: [],
    OpCode.BIT_OR: [],
    OpCode.BIT_XOR: [],
    OpCode.BIT_NOT: [],
    OpCode.SHL: [],
    OpCode.SHR: [],
    OpCode.AND: [],
    OpCode.OR: [],
    OpCode.NOT: [],
    OpCode.EQ: [],
    OpCode.NE: [],
    OpCode.LT: [],
    OpCode.LE: [],
    OpCode.GT: [],
    OpCode.GE: [],
    OpCode.IS: [],
    OpCode.RET: [],
    OpCode.EXIT_TRY: [],
    OpCode.PUSH_NULL: [],
    OpCode.PUSH_TRUE: [],
    OpCode.PUSH_FALSE: [],
    OpCode.GC_COLLECT: [],
    OpCode.BREAKPOINT: [],
    OpCode.ITER: [],
    OpCode.NEXT: [],
    OpCode.GET_ITEM: [],
    OpCode.SET_ITEM: [],
    OpCode.APPEND: [],
    
    # One integer operand
    OpCode.PUSH_INT: ["int"],
    OpCode.PUSH_FLOAT: ["float"],
    OpCode.PUSH_STRING: ["string"],
    OpCode.JMP: ["offset"],
    OpCode.JZ: ["offset"],
    OpCode.JNZ: ["offset"],
    OpCode.ENTER_TRY: ["offset"],
    OpCode.LOAD_LOCAL: ["index"],
    OpCode.STORE_LOCAL: ["index"],
    OpCode.LOAD_GLOBAL: ["index"],
    OpCode.STORE_GLOBAL: ["index"],
    OpCode.LOAD_UPVALUE: ["index"],
    OpCode.STORE_UPVALUE: ["index"],
    OpCode.BUILD_LIST: ["count"],
    OpCode.BUILD_DICT: ["count"],
    OpCode.LINE: ["line"],
    OpCode.LOAD_CONST: ["index"],
    
    # String operand
    OpCode.CALL: ["name"],
    OpCode.CALL_METHOD: ["name"],
    OpCode.GET_ATTR: ["name"],
    OpCode.SET_ATTR: ["name"],
    OpCode.IMPORT: ["module"],
    OpCode.EXPORT: ["name"],
    OpCode.IS_TYPE: ["type"],
    OpCode.CAST: ["type"],
    
    # Multiple operands
    OpCode.MAKE_FUNCTION: ["name", "parameter_count"],
    OpCode.MAKE_CLOSURE: ["name", "parameter_count", "upvalue_count"],
    OpCode.NEW: ["type"],
} 