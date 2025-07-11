#!/usr/bin/env python3
"""
Assembly Abstract Syntax Tree (AST) Module

This module defines the complete AST structure for Assembly language,
supporting multiple architectures and all major language constructs including:
- Multiple instruction sets (x86, x64, ARM, RISC-V)
- Registers and memory addressing modes
- Labels, symbols, and directives
- Immediate values and expressions
- Sections and program structure
- Macros and conditional assembly
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass

# Architecture enumeration
class AssemblyArchitecture(Enum):
    X86 = "x86"
    X64 = "x64"
    ARM = "arm"
    ARM64 = "arm64"
    RISC_V = "risc_v"
    MIPS = "mips"
    PowerPC = "powerpc"

# Node type enumeration
class AssemblyNodeType(Enum):
    # Instructions
    INSTRUCTION = "instruction"
    MOVE = "move"
    ARITHMETIC = "arithmetic"
    LOGICAL = "logical"
    JUMP = "jump"
    CALL = "call"
    RETURN = "return"
    PUSH = "push"
    POP = "pop"
    COMPARE = "compare"
    TEST = "test"
    
    # Operands
    REGISTER = "register"
    IMMEDIATE = "immediate"
    MEMORY = "memory"
    LABEL_REF = "label_ref"
    
    # Memory addressing
    DIRECT_ADDRESS = "direct_address"
    INDIRECT_ADDRESS = "indirect_address"
    INDEXED_ADDRESS = "indexed_address"
    BASE_DISPLACEMENT = "base_displacement"
    
    # Program structure
    LABEL = "label"
    DIRECTIVE = "directive"
    SECTION = "section"
    SYMBOL = "symbol"
    
    # Data types
    BYTE_DATA = "byte_data"
    WORD_DATA = "word_data"
    DWORD_DATA = "dword_data"
    QWORD_DATA = "qword_data"
    STRING_DATA = "string_data"
    
    # Expressions
    EXPRESSION = "expression"
    BINARY_EXPR = "binary_expr"
    UNARY_EXPR = "unary_expr"
    
    # Macros and conditionals
    MACRO = "macro"
    MACRO_CALL = "macro_call"
    CONDITIONAL = "conditional"
    
    # Comments
    COMMENT = "comment"
    
    # Program
    PROGRAM = "program"

# Instruction types
class InstructionType(Enum):
    # Data movement
    MOV = "mov"
    LEA = "lea"
    XCHG = "xchg"
    
    # Arithmetic
    ADD = "add"
    SUB = "sub"
    MUL = "mul"
    DIV = "div"
    INC = "inc"
    DEC = "dec"
    NEG = "neg"
    
    # Logical
    AND = "and"
    OR = "or"
    XOR = "xor"
    NOT = "not"
    SHL = "shl"
    SHR = "shr"
    ROL = "rol"
    ROR = "ror"
    
    # Control flow
    JMP = "jmp"
    JZ = "jz"
    JNZ = "jnz"
    JE = "je"
    JNE = "jne"
    JL = "jl"
    JG = "jg"
    JLE = "jle"
    JGE = "jge"
    JC = "jc"
    JNC = "jnc"
    
    # Function calls
    CALL = "call"
    RET = "ret"
    ENTER = "enter"
    LEAVE = "leave"
    
    # Stack operations
    PUSH = "push"
    POP = "pop"
    PUSHF = "pushf"
    POPF = "popf"
    
    # Comparison and testing
    CMP = "cmp"
    TEST = "test"
    
    # String operations
    MOVS = "movs"
    CMPS = "cmps"
    SCAS = "scas"
    LODS = "lods"
    STOS = "stos"
    
    # System calls
    INT = "int"
    SYSCALL = "syscall"
    
    # Floating point
    FLD = "fld"
    FST = "fst"
    FADD = "fadd"
    FSUB = "fsub"
    FMUL = "fmul"
    FDIV = "fdiv"
    
    # No operation
    NOP = "nop"

# Register types for different architectures
class X86Register(Enum):
    # 32-bit general purpose
    EAX = "eax"
    EBX = "ebx"
    ECX = "ecx"
    EDX = "edx"
    ESI = "esi"
    EDI = "edi"
    ESP = "esp"
    EBP = "ebp"
    
    # 16-bit general purpose
    AX = "ax"
    BX = "bx"
    CX = "cx"
    DX = "dx"
    SI = "si"
    DI = "di"
    SP = "sp"
    BP = "bp"
    
    # 8-bit general purpose
    AL = "al"
    AH = "ah"
    BL = "bl"
    BH = "bh"
    CL = "cl"
    CH = "ch"
    DL = "dl"
    DH = "dh"
    
    # Segment registers
    CS = "cs"
    DS = "ds"
    ES = "es"
    FS = "fs"
    GS = "gs"
    SS = "ss"

class X64Register(Enum):
    # 64-bit general purpose
    RAX = "rax"
    RBX = "rbx"
    RCX = "rcx"
    RDX = "rdx"
    RSI = "rsi"
    RDI = "rdi"
    RSP = "rsp"
    RBP = "rbp"
    R8 = "r8"
    R9 = "r9"
    R10 = "r10"
    R11 = "r11"
    R12 = "r12"
    R13 = "r13"
    R14 = "r14"
    R15 = "r15"
    
    # 32-bit views
    EAX = "eax"
    EBX = "ebx"
    ECX = "ecx"
    EDX = "edx"

class ARMRegister(Enum):
    # General purpose registers
    R0 = "r0"
    R1 = "r1"
    R2 = "r2"
    R3 = "r3"
    R4 = "r4"
    R5 = "r5"
    R6 = "r6"
    R7 = "r7"
    R8 = "r8"
    R9 = "r9"
    R10 = "r10"
    R11 = "r11"
    R12 = "r12"
    
    # Special registers
    SP = "sp"  # Stack pointer (R13)
    LR = "lr"  # Link register (R14)
    PC = "pc"  # Program counter (R15)
    
    # Status register
    CPSR = "cpsr"

# Data size enumeration
class DataSize(Enum):
    BYTE = 1
    WORD = 2
    DWORD = 4
    QWORD = 8
    TBYTE = 10
    OWORD = 16

@dataclass
class AssemblyNode(ABC):
    """Base class for all Assembly AST nodes."""
    node_type: AssemblyNodeType
    line_number: Optional[int] = None
    column_number: Optional[int] = None
    
    @abstractmethod
    def accept(self, visitor: 'AssemblyNodeVisitor') -> Any:
        """Accept a visitor for the visitor pattern."""
        pass

@dataclass
class AssemblyOperand(AssemblyNode):
    """Base class for Assembly operands."""
    pass

@dataclass
class AssemblyInstruction(AssemblyNode):
    """Base class for Assembly instructions."""
    pass

# Operands

@dataclass
class AssemblyRegister(AssemblyOperand):
    """Assembly register operand."""
    name: str
    size: DataSize
    architecture: AssemblyArchitecture
    
    def __post_init__(self):
        self.node_type = AssemblyNodeType.REGISTER
    
    def accept(self, visitor: 'AssemblyNodeVisitor') -> Any:
        return visitor.visit_register(self)

@dataclass
class AssemblyImmediate(AssemblyOperand):
    """Assembly immediate value operand."""
    value: Union[int, str]
    size: Optional[DataSize] = None
    
    def __post_init__(self):
        self.node_type = AssemblyNodeType.IMMEDIATE
    
    def accept(self, visitor: 'AssemblyNodeVisitor') -> Any:
        return visitor.visit_immediate(self)

@dataclass
class AssemblyMemory(AssemblyOperand):
    """Assembly memory operand."""
    base: Optional[AssemblyRegister] = None
    index: Optional[AssemblyRegister] = None
    scale: Optional[int] = None
    displacement: Optional[Union[int, str]] = None
    size: Optional[DataSize] = None
    
    def __post_init__(self):
        self.node_type = AssemblyNodeType.MEMORY
    
    def accept(self, visitor: 'AssemblyNodeVisitor') -> Any:
        return visitor.visit_memory(self)

@dataclass
class AssemblyLabelRef(AssemblyOperand):
    """Assembly label reference."""
    name: str
    
    def __post_init__(self):
        self.node_type = AssemblyNodeType.LABEL_REF
    
    def accept(self, visitor: 'AssemblyNodeVisitor') -> Any:
        return visitor.visit_label_ref(self)

# Instructions

@dataclass
class AssemblyGenericInstruction(AssemblyInstruction):
    """Generic assembly instruction."""
    mnemonic: str
    operands: List[AssemblyOperand]
    instruction_type: Optional[InstructionType] = None
    
    def __post_init__(self):
        self.node_type = AssemblyNodeType.INSTRUCTION
    
    def accept(self, visitor: 'AssemblyNodeVisitor') -> Any:
        return visitor.visit_instruction(self)

@dataclass
class AssemblyMoveInstruction(AssemblyInstruction):
    """Assembly move instruction (MOV, LEA, etc.)."""
    destination: AssemblyOperand
    source: AssemblyOperand
    move_type: InstructionType = InstructionType.MOV
    
    def __post_init__(self):
        self.node_type = AssemblyNodeType.MOVE
    
    def accept(self, visitor: 'AssemblyNodeVisitor') -> Any:
        return visitor.visit_move(self)

@dataclass
class AssemblyArithmeticInstruction(AssemblyInstruction):
    """Assembly arithmetic instruction."""
    operation: InstructionType
    destination: AssemblyOperand
    source: Optional[AssemblyOperand] = None
    
    def __post_init__(self):
        self.node_type = AssemblyNodeType.ARITHMETIC
    
    def accept(self, visitor: 'AssemblyNodeVisitor') -> Any:
        return visitor.visit_arithmetic(self)

@dataclass
class AssemblyLogicalInstruction(AssemblyInstruction):
    """Assembly logical instruction."""
    operation: InstructionType
    destination: AssemblyOperand
    source: Optional[AssemblyOperand] = None
    
    def __post_init__(self):
        self.node_type = AssemblyNodeType.LOGICAL
    
    def accept(self, visitor: 'AssemblyNodeVisitor') -> Any:
        return visitor.visit_logical(self)

@dataclass
class AssemblyJumpInstruction(AssemblyInstruction):
    """Assembly jump instruction."""
    jump_type: InstructionType
    target: AssemblyOperand
    condition: Optional[str] = None
    
    def __post_init__(self):
        self.node_type = AssemblyNodeType.JUMP
    
    def accept(self, visitor: 'AssemblyNodeVisitor') -> Any:
        return visitor.visit_jump(self)

@dataclass
class AssemblyCallInstruction(AssemblyInstruction):
    """Assembly call instruction."""
    target: AssemblyOperand
    calling_convention: Optional[str] = None
    
    def __post_init__(self):
        self.node_type = AssemblyNodeType.CALL
    
    def accept(self, visitor: 'AssemblyNodeVisitor') -> Any:
        return visitor.visit_call(self)

@dataclass
class AssemblyReturnInstruction(AssemblyInstruction):
    """Assembly return instruction."""
    value: Optional[AssemblyOperand] = None
    
    def __post_init__(self):
        self.node_type = AssemblyNodeType.RETURN
    
    def accept(self, visitor: 'AssemblyNodeVisitor') -> Any:
        return visitor.visit_return(self)

@dataclass
class AssemblyStackInstruction(AssemblyInstruction):
    """Assembly stack instruction (PUSH/POP)."""
    operation: InstructionType  # PUSH or POP
    operand: AssemblyOperand
    
    def __post_init__(self):
        self.node_type = AssemblyNodeType.PUSH if self.operation == InstructionType.PUSH else AssemblyNodeType.POP
    
    def accept(self, visitor: 'AssemblyNodeVisitor') -> Any:
        return visitor.visit_stack(self)

@dataclass
class AssemblyCompareInstruction(AssemblyInstruction):
    """Assembly compare instruction."""
    left: AssemblyOperand
    right: AssemblyOperand
    compare_type: InstructionType = InstructionType.CMP
    
    def __post_init__(self):
        self.node_type = AssemblyNodeType.COMPARE
    
    def accept(self, visitor: 'AssemblyNodeVisitor') -> Any:
        return visitor.visit_compare(self)

# Program structure

@dataclass
class AssemblyLabel(AssemblyNode):
    """Assembly label."""
    name: str
    global_label: bool = False
    
    def __post_init__(self):
        self.node_type = AssemblyNodeType.LABEL
    
    def accept(self, visitor: 'AssemblyNodeVisitor') -> Any:
        return visitor.visit_label(self)

@dataclass
class AssemblyDirective(AssemblyNode):
    """Assembly directive."""
    name: str
    arguments: List[str]
    
    def __post_init__(self):
        self.node_type = AssemblyNodeType.DIRECTIVE
    
    def accept(self, visitor: 'AssemblyNodeVisitor') -> Any:
        return visitor.visit_directive(self)

@dataclass
class AssemblySection(AssemblyNode):
    """Assembly section."""
    name: str
    attributes: List[str]
    content: List[AssemblyNode]
    
    def __post_init__(self):
        self.node_type = AssemblyNodeType.SECTION
    
    def accept(self, visitor: 'AssemblyNodeVisitor') -> Any:
        return visitor.visit_section(self)

@dataclass
class AssemblySymbol(AssemblyNode):
    """Assembly symbol definition."""
    name: str
    value: Union[int, str, AssemblyOperand]
    symbol_type: str = "local"  # local, global, extern
    
    def __post_init__(self):
        self.node_type = AssemblyNodeType.SYMBOL
    
    def accept(self, visitor: 'AssemblyNodeVisitor') -> Any:
        return visitor.visit_symbol(self)

# Data definitions

@dataclass
class AssemblyDataDefinition(AssemblyNode):
    """Assembly data definition."""
    size: DataSize
    values: List[Union[int, str, AssemblyOperand]]
    
    def __post_init__(self):
        if self.size == DataSize.BYTE:
            self.node_type = AssemblyNodeType.BYTE_DATA
        elif self.size == DataSize.WORD:
            self.node_type = AssemblyNodeType.WORD_DATA
        elif self.size == DataSize.DWORD:
            self.node_type = AssemblyNodeType.DWORD_DATA
        elif self.size == DataSize.QWORD:
            self.node_type = AssemblyNodeType.QWORD_DATA
        else:
            self.node_type = AssemblyNodeType.BYTE_DATA
    
    def accept(self, visitor: 'AssemblyNodeVisitor') -> Any:
        return visitor.visit_data_definition(self)

@dataclass
class AssemblyStringData(AssemblyNode):
    """Assembly string data."""
    value: str
    null_terminated: bool = True
    
    def __post_init__(self):
        self.node_type = AssemblyNodeType.STRING_DATA
    
    def accept(self, visitor: 'AssemblyNodeVisitor') -> Any:
        return visitor.visit_string_data(self)

# Expressions

@dataclass
class AssemblyExpression(AssemblyNode):
    """Assembly expression."""
    pass

@dataclass
class AssemblyBinaryExpression(AssemblyExpression):
    """Assembly binary expression."""
    left: AssemblyOperand
    operator: str
    right: AssemblyOperand
    
    def __post_init__(self):
        self.node_type = AssemblyNodeType.BINARY_EXPR
    
    def accept(self, visitor: 'AssemblyNodeVisitor') -> Any:
        return visitor.visit_binary_expression(self)

@dataclass
class AssemblyUnaryExpression(AssemblyExpression):
    """Assembly unary expression."""
    operator: str
    operand: AssemblyOperand
    
    def __post_init__(self):
        self.node_type = AssemblyNodeType.UNARY_EXPR
    
    def accept(self, visitor: 'AssemblyNodeVisitor') -> Any:
        return visitor.visit_unary_expression(self)

# Macros and conditionals

@dataclass
class AssemblyMacro(AssemblyNode):
    """Assembly macro definition."""
    name: str
    parameters: List[str]
    body: List[AssemblyNode]
    
    def __post_init__(self):
        self.node_type = AssemblyNodeType.MACRO
    
    def accept(self, visitor: 'AssemblyNodeVisitor') -> Any:
        return visitor.visit_macro(self)

@dataclass
class AssemblyMacroCall(AssemblyNode):
    """Assembly macro call."""
    name: str
    arguments: List[AssemblyOperand]
    
    def __post_init__(self):
        self.node_type = AssemblyNodeType.MACRO_CALL
    
    def accept(self, visitor: 'AssemblyNodeVisitor') -> Any:
        return visitor.visit_macro_call(self)

@dataclass
class AssemblyConditional(AssemblyNode):
    """Assembly conditional compilation."""
    condition: str
    then_body: List[AssemblyNode]
    else_body: Optional[List[AssemblyNode]] = None
    
    def __post_init__(self):
        self.node_type = AssemblyNodeType.CONDITIONAL
    
    def accept(self, visitor: 'AssemblyNodeVisitor') -> Any:
        return visitor.visit_conditional(self)

# Comments

@dataclass
class AssemblyComment(AssemblyNode):
    """Assembly comment."""
    text: str
    inline: bool = False
    
    def __post_init__(self):
        self.node_type = AssemblyNodeType.COMMENT
    
    def accept(self, visitor: 'AssemblyNodeVisitor') -> Any:
        return visitor.visit_comment(self)

# Program

@dataclass
class AssemblyProgram(AssemblyNode):
    """Assembly program (complete source file)."""
    architecture: AssemblyArchitecture
    sections: List[AssemblySection]
    global_statements: List[AssemblyNode]
    
    def __post_init__(self):
        self.node_type = AssemblyNodeType.PROGRAM
    
    def accept(self, visitor: 'AssemblyNodeVisitor') -> Any:
        return visitor.visit_program(self)

# Visitor pattern

class AssemblyNodeVisitor(ABC):
    """Abstract visitor for Assembly AST nodes."""
    
    @abstractmethod
    def visit_register(self, node: AssemblyRegister) -> Any: pass
    
    @abstractmethod
    def visit_immediate(self, node: AssemblyImmediate) -> Any: pass
    
    @abstractmethod
    def visit_memory(self, node: AssemblyMemory) -> Any: pass
    
    @abstractmethod
    def visit_label_ref(self, node: AssemblyLabelRef) -> Any: pass
    
    @abstractmethod
    def visit_instruction(self, node: AssemblyGenericInstruction) -> Any: pass
    
    @abstractmethod
    def visit_move(self, node: AssemblyMoveInstruction) -> Any: pass
    
    @abstractmethod
    def visit_arithmetic(self, node: AssemblyArithmeticInstruction) -> Any: pass
    
    @abstractmethod
    def visit_logical(self, node: AssemblyLogicalInstruction) -> Any: pass
    
    @abstractmethod
    def visit_jump(self, node: AssemblyJumpInstruction) -> Any: pass
    
    @abstractmethod
    def visit_call(self, node: AssemblyCallInstruction) -> Any: pass
    
    @abstractmethod
    def visit_return(self, node: AssemblyReturnInstruction) -> Any: pass
    
    @abstractmethod
    def visit_stack(self, node: AssemblyStackInstruction) -> Any: pass
    
    @abstractmethod
    def visit_compare(self, node: AssemblyCompareInstruction) -> Any: pass
    
    @abstractmethod
    def visit_label(self, node: AssemblyLabel) -> Any: pass
    
    @abstractmethod
    def visit_directive(self, node: AssemblyDirective) -> Any: pass
    
    @abstractmethod
    def visit_section(self, node: AssemblySection) -> Any: pass
    
    @abstractmethod
    def visit_symbol(self, node: AssemblySymbol) -> Any: pass
    
    @abstractmethod
    def visit_data_definition(self, node: AssemblyDataDefinition) -> Any: pass
    
    @abstractmethod
    def visit_string_data(self, node: AssemblyStringData) -> Any: pass
    
    @abstractmethod
    def visit_binary_expression(self, node: AssemblyBinaryExpression) -> Any: pass
    
    @abstractmethod
    def visit_unary_expression(self, node: AssemblyUnaryExpression) -> Any: pass
    
    @abstractmethod
    def visit_macro(self, node: AssemblyMacro) -> Any: pass
    
    @abstractmethod
    def visit_macro_call(self, node: AssemblyMacroCall) -> Any: pass
    
    @abstractmethod
    def visit_conditional(self, node: AssemblyConditional) -> Any: pass
    
    @abstractmethod
    def visit_comment(self, node: AssemblyComment) -> Any: pass
    
    @abstractmethod
    def visit_program(self, node: AssemblyProgram) -> Any: pass

# Helper utility functions

def asm_register(name: str, size: DataSize, arch: AssemblyArchitecture) -> AssemblyRegister:
    """Create an assembly register."""
    return AssemblyRegister(node_type=AssemblyNodeType.REGISTER, name=name, size=size, architecture=arch)

def asm_immediate(value: Union[int, str], size: Optional[DataSize] = None) -> AssemblyImmediate:
    """Create an assembly immediate value."""
    return AssemblyImmediate(node_type=AssemblyNodeType.IMMEDIATE, value=value, size=size)

def asm_memory(base: Optional[AssemblyRegister] = None, 
               index: Optional[AssemblyRegister] = None,
               scale: Optional[int] = None,
               displacement: Optional[Union[int, str]] = None,
               size: Optional[DataSize] = None) -> AssemblyMemory:
    """Create an assembly memory operand."""
    return AssemblyMemory(
        node_type=AssemblyNodeType.MEMORY,
        base=base, index=index, scale=scale, 
        displacement=displacement, size=size
    )

def asm_label_ref(name: str) -> AssemblyLabelRef:
    """Create an assembly label reference."""
    return AssemblyLabelRef(node_type=AssemblyNodeType.LABEL_REF, name=name)

def asm_mov(dest: AssemblyOperand, src: AssemblyOperand) -> AssemblyMoveInstruction:
    """Create a MOV instruction."""
    return AssemblyMoveInstruction(
        node_type=AssemblyNodeType.MOVE,
        destination=dest, source=src
    )

def asm_add(dest: AssemblyOperand, src: AssemblyOperand) -> AssemblyArithmeticInstruction:
    """Create an ADD instruction."""
    return AssemblyArithmeticInstruction(
        node_type=AssemblyNodeType.ARITHMETIC,
        operation=InstructionType.ADD,
        destination=dest, source=src
    )

def asm_jmp(target: AssemblyOperand) -> AssemblyJumpInstruction:
    """Create a JMP instruction."""
    return AssemblyJumpInstruction(
        node_type=AssemblyNodeType.JUMP,
        jump_type=InstructionType.JMP,
        target=target
    )

def asm_call(target: AssemblyOperand) -> AssemblyCallInstruction:
    """Create a CALL instruction."""
    return AssemblyCallInstruction(
        node_type=AssemblyNodeType.CALL,
        target=target
    )

def asm_label(name: str, global_label: bool = False) -> AssemblyLabel:
    """Create an assembly label."""
    return AssemblyLabel(
        node_type=AssemblyNodeType.LABEL,
        name=name, global_label=global_label
    ) 