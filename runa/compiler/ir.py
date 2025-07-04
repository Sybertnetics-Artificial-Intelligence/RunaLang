"""
Runa Intermediate Representation (IR)

This module defines the IR used for code generation. The IR is designed to:
1. Bridge between high-level Runa AST and target language code
2. Preserve natural language semantics while enabling efficient translation
3. Support multiple target languages (starting with Python)
4. Use SSA-like form with typed operands and three-address instructions
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Union, Dict, Any, Set
from enum import Enum, auto
import uuid

# === TYPE SYSTEM ===

@dataclass(frozen=True)
class IRType:
    """Type information for IR operands."""
    name: str
    is_generic: bool = False
    type_args: List['IRType'] = field(default_factory=list)
    
    def __str__(self):
        if self.is_generic and self.type_args:
            args = ", ".join(str(arg) for arg in self.type_args)
            return f"{self.name}[{args}]"
        return self.name

class IRTypes:
    """Standard IR types matching Runa's type system."""
    INTEGER = IRType("Integer")
    FLOAT = IRType("Float") 
    STRING = IRType("String")
    BOOLEAN = IRType("Boolean")
    ANY = IRType("Any")
    VOID = IRType("Void")
    
    @staticmethod
    def list_of(element_type: IRType) -> IRType:
        return IRType("List", is_generic=True, type_args=[element_type])
    
    @staticmethod
    def dict_of(key_type: IRType, value_type: IRType) -> IRType:
        return IRType("Dictionary", is_generic=True, type_args=[key_type, value_type])

# === OPERANDS ===

class IROperand:
    """Base class for all IR operands."""
    def __init__(self, ir_type: IRType):
        self.ir_type = ir_type

class IRVariable(IROperand):
    """Named variable operand with SSA-like unique identifiers."""
    def __init__(self, name: str, ir_type: IRType):
        super().__init__(ir_type)
        self.name = name
        self.id = str(uuid.uuid4())[:8]  # Unique ID for SSA
    
    def __str__(self):
        return f"%{self.name}_{self.id}"
    
    def __eq__(self, other):
        return isinstance(other, IRVariable) and self.id == other.id
    
    def __hash__(self):
        return hash(self.id)

class IRTemporary(IROperand):
    """Temporary variable for intermediate computations."""
    _temp_counter = 0
    
    def __init__(self, ir_type: IRType, prefix: str = "tmp"):
        super().__init__(ir_type)
        IRTemporary._temp_counter += 1
        self.name = f"{prefix}_{IRTemporary._temp_counter}"
        self.id = str(uuid.uuid4())[:8]
    
    def __str__(self):
        return f"%{self.name}_{self.id}"
    
    def __eq__(self, other):
        return isinstance(other, IRTemporary) and self.id == other.id
    
    def __hash__(self):
        return hash(self.id)

class IRConstant(IROperand):
    """Constant value operand."""
    def __init__(self, value: Any, ir_type: IRType):
        super().__init__(ir_type)
        self.value = value
    
    def __str__(self):
        if self.ir_type == IRTypes.STRING:
            return f'"{self.value}"'
        elif self.ir_type == IRTypes.BOOLEAN:
            return str(self.value).lower()
        return str(self.value)
    
    def __eq__(self, other):
        return isinstance(other, IRConstant) and self.value == other.value and self.ir_type == other.ir_type
    
    def __hash__(self):
        return hash((self.value, self.ir_type.name))

# === INSTRUCTIONS ===

class IRInstructionType(Enum):
    """Types of IR instructions."""
    # Arithmetic
    ADD = auto()
    SUBTRACT = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    POWER = auto()
    
    # Comparison
    EQUALS = auto()
    NOT_EQUALS = auto()
    GREATER_THAN = auto()
    LESS_THAN = auto()
    GREATER_EQUAL = auto()
    LESS_EQUAL = auto()
    
    # Logical
    AND = auto()
    OR = auto()
    NOT = auto()
    
    # Assignment
    ASSIGN = auto()
    COPY = auto()
    
    # Memory operations
    LOAD = auto()
    STORE = auto()
    MEMBER_ACCESS = auto()
    INDEX_ACCESS = auto()
    
    # Function operations
    CALL = auto()
    RETURN = auto()
    
    # Control flow
    JUMP = auto()
    BRANCH = auto()
    LABEL = auto()
    
    # Built-ins
    DISPLAY = auto()
    LIST_CREATE = auto()
    DICT_CREATE = auto()
    
    # Special
    PHI = auto()  # For SSA form
    NOP = auto()

@dataclass
class IRInstruction:
    """Base class for IR instructions."""
    instruction_type: IRInstructionType
    result: Optional[IROperand] = None
    operands: List[IROperand] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __str__(self):
        parts = []
        if self.result:
            parts.append(f"{self.result} = ")
        
        parts.append(self.instruction_type.name.lower())
        
        if self.operands:
            operand_strs = [str(op) for op in self.operands]
            parts.append(" " + ", ".join(operand_strs))
        
        return "".join(parts)

# Specialized instruction classes for complex operations

class IRCallInstruction(IRInstruction):
    """Function call instruction with named arguments."""
    
    def __init__(self, result: Optional[IROperand], function_name: str, 
                 arguments: List[tuple[str, IROperand]]):
        super().__init__(IRInstructionType.CALL, result)
        self.function_name = function_name
        self.arguments = arguments
    
    def __str__(self):
        result_part = f"{self.result} = " if self.result else ""
        args_part = ", ".join(f"{name}={op}" for name, op in self.arguments)
        return f"{result_part}call {self.function_name}({args_part})"

class IRBranchInstruction(IRInstruction):
    """Conditional branch instruction."""
    
    def __init__(self, condition: IROperand, true_label: str, false_label: str):
        super().__init__(IRInstructionType.BRANCH)
        self.condition = condition
        self.true_label = true_label
        self.false_label = false_label
    
    def __str__(self):
        return f"branch {self.condition}, {self.true_label}, {self.false_label}"

class IRLabelInstruction(IRInstruction):
    """Label instruction for control flow targets."""
    
    def __init__(self, label: str):
        super().__init__(IRInstructionType.LABEL)
        self.label = label
    
    def __str__(self):
        return f"{self.label}:"

class IRDisplayInstruction(IRInstruction):
    """Display instruction preserving Runa's natural language semantics."""
    
    def __init__(self, value: IROperand, prefix: Optional[IROperand] = None):
        super().__init__(IRInstructionType.DISPLAY)
        self.value = value
        self.prefix = prefix
    
    def __str__(self):
        if self.prefix:
            return f"display {self.value} with prefix {self.prefix}"
        return f"display {self.value}"

# === BASIC BLOCKS ===

@dataclass
class IRBasicBlock:
    """Basic block containing a sequence of instructions."""
    label: str
    instructions: List[IRInstruction] = field(default_factory=list)
    predecessors: Set[str] = field(default_factory=set)
    successors: Set[str] = field(default_factory=set)
    
    def add_instruction(self, instruction: IRInstruction):
        """Add an instruction to this basic block."""
        self.instructions.append(instruction)
    
    def add_predecessor(self, predecessor: str):
        """Add a predecessor block."""
        self.predecessors.add(predecessor)
    
    def add_successor(self, successor: str):
        """Add a successor block."""
        self.successors.add(successor)
    
    def __str__(self):
        lines = [f"{self.label}:"]
        for instruction in self.instructions:
            lines.append(f"    {instruction}")
        return "\n".join(lines)

# === FUNCTIONS AND MODULES ===

@dataclass
class IRFunction:
    """Function representation in IR."""
    name: str
    parameters: List[IRVariable]
    return_type: IRType
    entry_block: str
    basic_blocks: List[IRBasicBlock] = field(default_factory=list)
    blocks: Dict[str, IRBasicBlock] = field(default_factory=dict)  # For backward compatibility
    local_variables: Dict[str, IRVariable] = field(default_factory=dict)
    
    def add_block(self, block: IRBasicBlock):
        """Add a basic block to this function."""
        self.blocks[block.label] = block
        if block not in self.basic_blocks:
            self.basic_blocks.append(block)
    
    def get_block(self, label: str) -> IRBasicBlock:
        """Get a basic block by label."""
        return self.blocks[label]
    
    def add_variable(self, name: str, variable: IRVariable):
        """Add a local variable."""
        self.local_variables[name] = variable
    
    def __str__(self):
        lines = [f"function {self.name}:"]
        for block in self.blocks.values():
            lines.append(str(block))
            lines.append("")  # Empty line between blocks
        return "\n".join(lines)

@dataclass
class IRModule:
    """Top-level IR module representing a complete program."""
    name: str
    functions: List[IRFunction] = field(default_factory=list)  # For new approach
    function_dict: Dict[str, IRFunction] = field(default_factory=dict)  # For backward compatibility
    global_variables: Dict[str, IRVariable] = field(default_factory=dict)
    string_constants: List[str] = field(default_factory=list)
    main_function: Optional[str] = None
    
    def add_function(self, function: IRFunction):
        """Add a function to this module."""
        self.function_dict[function.name] = function
        if function not in self.functions:
            self.functions.append(function)
        if function.name == "main":
            self.main_function = function.name
    
    def get_function(self, name: str) -> Optional[IRFunction]:
        """Get a function by name."""
        return self.function_dict.get(name)
    
    def add_global_variable(self, name: str, variable: IRVariable):
        """Add a global variable."""
        self.global_variables[name] = variable
    
    def __str__(self):
        lines = [f"module {self.name}:"]
        lines.append("")
        
        # Global variables
        if self.global_variables:
            lines.append("globals:")
            for name, var in self.global_variables.items():
                lines.append(f"    {var} : {var.ir_type}")
            lines.append("")
        
        # Functions
        for function in self.functions:
            lines.append(str(function))
            lines.append("")
        
        return "\n".join(lines)

# === HELPER FUNCTIONS ===

def create_ir_operand(value: Any, ir_type: Optional[IRType] = None) -> IROperand:
    """Create appropriate IR operand from a Python value."""
    if ir_type is None:
        # Infer type from value
        if isinstance(value, int):
            ir_type = IRTypes.INTEGER
        elif isinstance(value, float):
            ir_type = IRTypes.FLOAT
        elif isinstance(value, str):
            ir_type = IRTypes.STRING
        elif isinstance(value, bool):
            ir_type = IRTypes.BOOLEAN
        elif isinstance(value, list):
            ir_type = IRTypes.list_of(IRTypes.ANY)
        else:
            ir_type = IRTypes.ANY
    
    return IRConstant(value, ir_type)

def create_binary_instruction(op_type: IRInstructionType, left: IROperand, 
                            right: IROperand, result_type: IRType) -> IRInstruction:
    """Create a binary operation instruction."""
    result = IRTemporary(result_type)
    return IRInstruction(op_type, result, [left, right])

def create_assignment_instruction(target: IROperand, source: IROperand) -> IRInstruction:
    """Create an assignment instruction."""
    return IRInstruction(IRInstructionType.ASSIGN, target, [source])

def create_label_instruction(label: str) -> IRLabelInstruction:
    """Create a label instruction."""
    return IRLabelInstruction(label)

def create_jump_instruction(target_label: str) -> IRInstruction:
    """Create an unconditional jump instruction."""
    return IRInstruction(IRInstructionType.JUMP, metadata={"target": target_label})

def create_return_instruction(value: Optional[IROperand] = None) -> IRInstruction:
    """Create a return instruction."""
    operands = [value] if value else []
    return IRInstruction(IRInstructionType.RETURN, operands=operands) 