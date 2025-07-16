"""
Runa Intermediate Representation (IR) - Control Flow Graph (CFG)

This module defines the data structures for a Control Flow Graph, which is a common
intermediate representation used in compilers to represent the flow of logic in a
program.

The CFG is a directed graph where:
- Nodes are `BasicBlock` objects, representing straight-line code sequences.
- Edges represent jumps (conditional or unconditional) between basic blocks.

This IR is language-agnostic and serves as the common ground for semantic
comparison between different language ASTs.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Union, Any

# ---------------------------------------------------------------------------
#  Operands
# ---------------------------------------------------------------------------

@dataclass
class Var:
    """Represents a variable or temporary in the IR."""
    name: str

@dataclass
class Constant:
    """Represents a literal constant value."""
    value: Any

Operand = Union[Var, Constant]

# ---------------------------------------------------------------------------
#  IR Instructions (Three-Address Code style)
# ---------------------------------------------------------------------------

@dataclass
class IRInstruction:
    """Base class for all IR instructions."""
    pass

@dataclass
class Assign(IRInstruction):
    """Assignment: `target = source`"""
    target: Var
    source: Operand

@dataclass
class BinaryOperation(IRInstruction):
    """Binary Operation: `target = left_op <op> right_op`"""
    target: Var
    op: str  # e.g., '+', '-', '==', '>'
    left: Operand
    right: Operand

@dataclass
class UnaryOperation(IRInstruction):
    """Unary Operation: `target = <op> operand`"""
    target: Var
    op: str # e.g., '-', 'not'
    operand: Operand

@dataclass
class FunctionCall(IRInstruction):
    """Function Call: `target = call function_name(arg1, arg2, ...)`"""
    target: Optional[Var]  # None if the return value is ignored
    function_name: str
    args: List[Operand]

@dataclass
class ConditionalJump(IRInstruction):
    """If `condition` is true, jump to `true_target`, else `false_target`."""
    condition: Operand
    true_target: 'BasicBlock'
    false_target: 'BasicBlock'

@dataclass
class UnconditionalJump(IRInstruction):
    """Jump to `target`."""
    target: 'BasicBlock'

@dataclass
class Return(IRInstruction):
    """Return a value from a function."""
    value: Optional[Operand]

# ---------------------------------------------------------------------------
#  CFG Components
# ---------------------------------------------------------------------------

@dataclass
class BasicBlock:
    """A sequence of instructions that are executed sequentially."""
    id: int
    instructions: List[IRInstruction] = field(default_factory=list)
    predecessors: List['BasicBlock'] = field(default_factory=list)
    successors: List['BasicBlock'] = field(default_factory=list)

    def __post_init__(self):
        # The last instruction in a basic block MUST be a "terminator"
        # (e.g., a jump or a return). This is enforced by the CFG builder.
        pass

@dataclass
class ControlFlowGraph:
    """A complete Control Flow Graph for a function or module."""
    entry_block: BasicBlock
    exit_block: BasicBlock
    blocks: List[BasicBlock] = field(default_factory=list)

    def __str__(self):
        lines = []
        for block in self.blocks:
            lines.append(f"Block {block.id}:")
            for inst in block.instructions:
                lines.append(f"  {inst}")
            lines.append(f"  Successors: {[b.id for b in block.successors]}")
        return "\n".join(lines) 