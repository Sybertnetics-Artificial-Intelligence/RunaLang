"""
Tests for the Runa Virtual Machine.

This module contains tests for the bytecode representation, virtual machine execution,
and bytecode generation from AST.
"""

import unittest
import sys
import os

# Add the project root to the path so we can import the modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.vm.instructions import OpCode, Instruction
from src.vm.bytecode import BytecodeModule
from src.vm.vm import VirtualMachine, VMValue, VMValueType


class TestInstructions(unittest.TestCase):
    """Tests for the bytecode instructions."""
    
    def test_instruction_creation(self):
        """Test creating instructions."""
        # Create a simple instruction
        instr = Instruction(OpCode.NOP)
        self.assertEqual(instr.opcode, OpCode.NOP)
        self.assertEqual(instr.operands, [])
        self.assertEqual(instr.line, 0)
        
        # Create an instruction with operands
        instr = Instruction(OpCode.PUSH_INT, [42], 10)
        self.assertEqual(instr.opcode, OpCode.PUSH_INT)
        self.assertEqual(instr.operands, [42])
        self.assertEqual(instr.line, 10)
    
    def test_instruction_string_representation(self):
        """Test string representation of instructions."""
        instr = Instruction(OpCode.NOP)
        self.assertEqual(str(instr), "NOP")
        
        instr = Instruction(OpCode.PUSH_INT, [42])
        self.assertEqual(str(instr), "PUSH_INT 42")
    
    def test_instruction_encoding_decoding(self):
        """Test encoding and decoding instructions."""
        # Test NOP instruction
        instr = Instruction(OpCode.NOP, line=10)
        encoded = instr.encode()
        decoded, _ = Instruction.decode(encoded)
        self.assertEqual(decoded.opcode, instr.opcode)
        self.assertEqual(decoded.operands, instr.operands)
        self.assertEqual(decoded.line, instr.line)
        
        # Test PUSH_INT instruction
        instr = Instruction(OpCode.PUSH_INT, [42], 10)
        encoded = instr.encode()
        decoded, _ = Instruction.decode(encoded)
        self.assertEqual(decoded.opcode, instr.opcode)
        self.assertEqual(decoded.operands, instr.operands)
        self.assertEqual(decoded.line, instr.line)
        
        # Test PUSH_STRING instruction
        instr = Instruction(OpCode.PUSH_STRING, ["hello"], 10)
        encoded = instr.encode()
        decoded, _ = Instruction.decode(encoded)
        self.assertEqual(decoded.opcode, instr.opcode)
        self.assertEqual(decoded.operands, instr.operands)
        self.assertEqual(decoded.line, instr.line)


class TestBytecodeModule(unittest.TestCase):
    """Tests for the bytecode module."""
    
    def test_module_creation(self):
        """Test creating a bytecode module."""
        module = BytecodeModule("test_module")
        self.assertEqual(module.name, "test_module")
        self.assertEqual(module.instructions, [])
        self.assertEqual(module.constants, [])
        self.assertEqual(module.string_pool, [])
        self.assertEqual(module.global_names, [])
        self.assertEqual(module.import_names, [])
        self.assertEqual(module.export_names, [])
        self.assertEqual(module.source_map, {})
    
    def test_add_instruction(self):
        """Test adding instructions to a module."""
        module = BytecodeModule("test_module")
        
        # Add a NOP instruction
        offset = module.add_instruction(Instruction(OpCode.NOP))
        self.assertEqual(offset, 0)
        self.assertEqual(len(module.instructions), 1)
        self.assertEqual(module.instructions[0].opcode, OpCode.NOP)
        
        # Add a PUSH_INT instruction
        offset = module.add_instruction(Instruction(OpCode.PUSH_INT, [42]))
        self.assertEqual(offset, 1)
        self.assertEqual(len(module.instructions), 2)
        self.assertEqual(module.instructions[1].opcode, OpCode.PUSH_INT)
        self.assertEqual(module.instructions[1].operands, [42])
    
    def test_add_constant(self):
        """Test adding constants to a module."""
        module = BytecodeModule("test_module")
        
        # Add an integer constant
        index = module.add_constant(42)
        self.assertEqual(index, 0)
        self.assertEqual(module.constants, [42])
        
        # Add a string constant
        index = module.add_constant("hello")
        self.assertEqual(index, 1)
        self.assertEqual(module.constants, [42, "hello"])
        
        # Add a duplicate constant
        index = module.add_constant(42)
        self.assertEqual(index, 0)  # Should return the existing index
        self.assertEqual(module.constants, [42, "hello"])
    
    def test_module_encoding_decoding(self):
        """Test encoding and decoding a bytecode module."""
        module = BytecodeModule("test_module")
        module.filename = "test.runa"
        
        # Add some instructions
        module.add_instruction(Instruction(OpCode.PUSH_INT, [42], 10))
        module.add_instruction(Instruction(OpCode.PUSH_STRING, ["hello"], 11))
        module.add_instruction(Instruction(OpCode.ADD, line=12))
        module.add_instruction(Instruction(OpCode.RET, line=13))
        
        # Add some constants
        module.add_constant(42)
        module.add_constant("hello")
        
        # Add some globals
        module.add_global("x")
        module.add_global("y")
        
        # Add some imports and exports
        module.add_import("math")
        module.add_export("main")
        
        # Add a function
        module.add_function("main", 0, 4)
        
        # Encode the module
        encoded = module.encode()
        
        # Decode the module
        decoded = BytecodeModule.decode(encoded)
        
        # Check that the decoded module matches the original
        self.assertEqual(decoded.name, module.name)
        self.assertEqual(decoded.filename, module.filename)
        self.assertEqual(len(decoded.instructions), len(module.instructions))
        self.assertEqual(decoded.constants, module.constants)
        self.assertEqual(decoded.global_names, module.global_names)
        self.assertEqual(decoded.import_names, module.import_names)
        self.assertEqual(decoded.export_names, module.export_names)
        self.assertEqual(decoded.functions, module.functions)


class TestVirtualMachine(unittest.TestCase):
    """Tests for the virtual machine."""
    
    def test_vm_creation(self):
        """Test creating a virtual machine."""
        vm = VirtualMachine()
        self.assertEqual(vm.frames, [])
        self.assertEqual(vm.modules, {})
        self.assertFalse(vm.debug_mode)
    
    def test_arithmetic_instructions(self):
        """Test arithmetic instructions."""
        # Create a simple module with arithmetic instructions
        module = BytecodeModule("test_module")
        
        # Push two integers (3 and 4) and add them
        module.add_instruction(Instruction(OpCode.PUSH_INT, [3]))
        module.add_instruction(Instruction(OpCode.PUSH_INT, [4]))
        module.add_instruction(Instruction(OpCode.ADD))
        module.add_instruction(Instruction(OpCode.RET))
        
        # Execute the module
        vm = VirtualMachine()
        vm.load_module(module)
        result = vm.execute_module("test_module")
        
        # Check the result
        self.assertEqual(result.type, VMValueType.INTEGER)
        self.assertEqual(result.value, 7)
    
    def test_string_operations(self):
        """Test string operations."""
        # Create a simple module with string operations
        module = BytecodeModule("test_module")
        
        # Push two strings and concatenate them
        module.add_instruction(Instruction(OpCode.PUSH_STRING, ["Hello, "]))
        module.add_instruction(Instruction(OpCode.PUSH_STRING, ["World!"]))
        module.add_instruction(Instruction(OpCode.ADD))
        module.add_instruction(Instruction(OpCode.RET))
        
        # Execute the module
        vm = VirtualMachine()
        vm.load_module(module)
        result = vm.execute_module("test_module")
        
        # Check the result
        self.assertEqual(result.type, VMValueType.STRING)
        self.assertEqual(result.value, "Hello, World!")
    
    def test_performance_metrics(self):
        """Test performance metrics."""
        # Create a simple module with a loop
        module = BytecodeModule("test_module")
        
        # Push initial counter (0)
        module.add_instruction(Instruction(OpCode.PUSH_INT, [0]))
        
        # Push limit (1000)
        module.add_instruction(Instruction(OpCode.PUSH_INT, [1000]))
        
        # Start of loop:
        # Duplicate counter (stack: counter, limit)
        module.add_instruction(Instruction(OpCode.DUP_X1))
        
        # Increment counter (stack: counter+1, limit, counter)
        module.add_instruction(Instruction(OpCode.PUSH_INT, [1]))
        module.add_instruction(Instruction(OpCode.ADD))
        
        # Swap to get comparison order right (stack: limit, counter+1)
        module.add_instruction(Instruction(OpCode.SWAP))
        
        # Duplicate for comparison (stack: limit, counter+1, limit)
        module.add_instruction(Instruction(OpCode.DUP))
        
        # Swap again (stack: limit, limit, counter+1)
        module.add_instruction(Instruction(OpCode.SWAP))
        
        # Compare if counter+1 < limit (stack: limit, counter+1, bool)
        module.add_instruction(Instruction(OpCode.LT))
        
        # Jump to end if counter+1 >= limit (stack: limit, counter+1)
        jump_offset = module.add_instruction(Instruction(OpCode.JZ, [0]))  # placeholder offset
        
        # Jump back to start of loop (stack: limit, counter+1)
        module.add_instruction(Instruction(OpCode.JMP, [-8]))  # -8 is the relative offset
        
        # End of loop:
        # Update the jump offset now that we know where the end is
        module.instructions[jump_offset].operands[0] = 1  # jump 1 instruction forward
        
        # Return counter (stack: limit, counter+1)
        module.add_instruction(Instruction(OpCode.SWAP))
        module.add_instruction(Instruction(OpCode.POP))
        module.add_instruction(Instruction(OpCode.RET))
        
        # Execute the module
        vm = VirtualMachine()
        vm.load_module(module)
        result = vm.execute_module("test_module")
        
        # Check the result
        self.assertEqual(result.type, VMValueType.INTEGER)
        self.assertEqual(result.value, 1000)
        
        # Check the performance metrics
        metrics = vm.get_performance_metrics()
        self.assertIn("instruction_count", metrics)
        self.assertIn("elapsed_time", metrics)
        self.assertIn("instructions_per_second", metrics)
        self.assertGreater(metrics["instruction_count"], 0)
        self.assertGreater(metrics["elapsed_time"], 0)
        self.assertGreater(metrics["instructions_per_second"], 0)


if __name__ == "__main__":
    unittest.main() 