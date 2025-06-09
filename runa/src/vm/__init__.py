"""
Runa Virtual Machine module.

This module provides the bytecode representation and virtual machine
for executing Runa programs.
"""

from .instructions import OpCode, Instruction
from .bytecode import BytecodeModule, BytecodeGenerator
from .vm import VirtualMachine, VMValue, VMFrame

__all__ = [
    'OpCode',
    'Instruction',
    'BytecodeModule',
    'BytecodeGenerator',
    'VirtualMachine',
    'VMValue',
    'VMFrame'
] 