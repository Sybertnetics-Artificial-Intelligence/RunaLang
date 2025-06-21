"""
Runa Runtime System

Provides the execution environment, memory management, and built-in functions
for the Runa programming language. Supports AI-to-AI communication patterns
and universal translation capabilities.
"""

import sys
import time
import math
import random
import json
import asyncio
from typing import Any, Dict, List, Optional, Callable, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum
import threading
import weakref
from collections import defaultdict, deque
import gc

from .error_handler import RunaError, RunaRuntimeError, RunaTypeError
from .performance_monitor import PerformanceMonitor


class MemoryType(Enum):
    """Types of memory allocation in the runtime."""
    STACK = "stack"
    HEAP = "heap"
    CONSTANT = "constant"
    SHARED = "shared"
    AI_CONTEXT = "ai_context"


@dataclass
class MemoryBlock:
    """Represents a block of memory in the runtime."""
    address: int
    size: int
    memory_type: MemoryType
    data: Any
    reference_count: int = 0
    last_access: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RuntimeContext:
    """Runtime execution context for a Runa program."""
    program_id: str
    start_time: float
    memory_usage: int = 0
    instruction_count: int = 0
    call_stack_depth: int = 0
    max_call_stack_depth: int = 1000
    variables: Dict[str, Any] = field(default_factory=dict)
    functions: Dict[str, Callable] = field(default_factory=dict)
    modules: Dict[str, Any] = field(default_factory=dict)
    ai_context: Dict[str, Any] = field(default_factory=dict)
    performance_data: Dict[str, Any] = field(default_factory=dict)


class MemoryManager:
    """Manages memory allocation and garbage collection."""
    
    def __init__(self, initial_size: int = 1024 * 1024):
        self.total_memory = initial_size
        self.used_memory = 0
        self.memory_blocks: Dict[int, MemoryBlock] = {}
        self.free_blocks: List[Tuple[int, int]] = [(0, initial_size)]
        self.next_address = 0
        self.gc_threshold = 0.8
        self.performance_monitor = PerformanceMonitor()
        
    def allocate(self, size: int, memory_type: MemoryType = MemoryType.HEAP) -> int:
        """Allocate memory block of specified size."""
        start_time = time.time()
        
        if self.used_memory / self.total_memory > self.gc_threshold:
            self.garbage_collect()
        
        best_fit = None
        best_fit_size = float('inf')
        
        for i, (addr, block_size) in enumerate(self.free_blocks):
            if block_size >= size and block_size < best_fit_size:
                best_fit = (i, addr, block_size)
                best_fit_size = block_size
        
        if best_fit is None:
            self._expand_memory(size)
            return self.allocate(size, memory_type)
        
        i, addr, block_size = best_fit
        
        del self.free_blocks[i]
        
        memory_block = MemoryBlock(
            address=addr,
            size=size,
            memory_type=memory_type,
            data=bytearray(size)
        )
        
        self.memory_blocks[addr] = memory_block
        self.used_memory += size
        
        remaining = block_size - size
        if remaining > 0:
            self._add_free_block(addr + size, remaining)
        
        self.performance_monitor.record_operation(
            "memory_allocation", time.time() - start_time, {"size": size, "type": memory_type.value}
        )
        
        return addr
    
    def deallocate(self, address: int) -> bool:
        """Deallocate memory block at specified address."""
        if address not in self.memory_blocks:
            return False
        
        block = self.memory_blocks[address]
        self.used_memory -= block.size
        del self.memory_blocks[address]
        
        self._add_free_block(address, block.size)
        
        return True
    
    def read(self, address: int, size: int) -> bytes:
        """Read data from memory address."""
        if address not in self.memory_blocks:
            raise RunaRuntimeError(f"Invalid memory address: {address}")
        
        block = self.memory_blocks[address]
        if address + size > block.address + block.size:
            raise RunaRuntimeError(f"Memory read out of bounds: {address}+{size}")
        
        block.last_access = time.time()
        return bytes(block.data[:size])
    
    def write(self, address: int, data: bytes) -> None:
        """Write data to memory address."""
        if address not in self.memory_blocks:
            raise RunaRuntimeError(f"Invalid memory address: {address}")
        
        block = self.memory_blocks[address]
        if address + len(data) > block.address + block.size:
            raise RunaRuntimeError(f"Memory write out of bounds: {address}+{len(data)}")
        
        block.data[:len(data)] = data
        block.last_access = time.time()
    
    def _expand_memory(self, required_size: int) -> None:
        """Expand total memory capacity."""
        expansion = max(required_size, self.total_memory // 2)
        self.total_memory += expansion
        
        self._add_free_block(self.total_memory - expansion, expansion)
    
    def _add_free_block(self, address: int, size: int) -> None:
        """Add a free memory block, merging adjacent blocks."""
        insert_pos = 0
        for i, (addr, block_size) in enumerate(self.free_blocks):
            if addr < address:
                insert_pos = i + 1
            else:
                break
        
        if insert_pos > 0:
            prev_addr, prev_size = self.free_blocks[insert_pos - 1]
            if prev_addr + prev_size == address:
                self.free_blocks[insert_pos - 1] = (prev_addr, prev_size + size)
                return
        
        if insert_pos < len(self.free_blocks):
            next_addr, next_size = self.free_blocks[insert_pos]
            if address + size == next_addr:
                self.free_blocks[insert_pos] = (address, size + next_size)
                return
        
        self.free_blocks.insert(insert_pos, (address, size))
    
    def garbage_collect(self) -> int:
        """Perform garbage collection and return freed bytes."""
        start_time = time.time()
        freed_bytes = 0
        
        marked = set()
        
        for block in self.memory_blocks.values():
            if block.reference_count > 0:
                marked.add(block.address)
        
        addresses_to_remove = []
        for address, block in self.memory_blocks.items():
            if address not in marked:
                addresses_to_remove.append(address)
                freed_bytes += block.size
        
        for address in addresses_to_remove:
            self.deallocate(address)
        
        self.performance_monitor.record_operation(
            "garbage_collection", time.time() - start_time, {"freed_bytes": freed_bytes}
        )
        
        return freed_bytes
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory usage statistics."""
        return {
            "total_memory": self.total_memory,
            "used_memory": self.used_memory,
            "free_memory": self.total_memory - self.used_memory,
            "utilization": self.used_memory / self.total_memory,
            "block_count": len(self.memory_blocks),
            "free_block_count": len(self.free_blocks)
        }


class BuiltinFunctions:
    """Built-in functions for the Runa runtime."""
    
    def __init__(self, runtime: 'RunaRuntime'):
        self.runtime = runtime
    
    def display(self, *args, **kwargs) -> None:
        """Display values to output using Runa syntax."""
        sep = kwargs.get('sep', ' ')
        end = kwargs.get('end', '\n')
        output = sep.join(str(arg) for arg in args) + end
        self.runtime.output_buffer.append(output)
    
    def input_with_prompt(self, prompt: str = "") -> str:
        """Get input from user using Runa syntax."""
        if prompt:
            self.runtime.output_buffer.append(prompt)
        return self.runtime.get_input()
    
    def length_of(self, obj: Any) -> int:
        """Get length of object using Runa syntax."""
        if hasattr(obj, '__len__'):
            return len(obj)
        raise RunaTypeError(f"Object of type {type(obj).__name__} has no length")
    
    def type_of(self, obj: Any) -> str:
        """Get type name of object using Runa syntax."""
        return type(obj).__name__
    
    def range_function(self, start: int, stop: Optional[int] = None, step: int = 1) -> List[int]:
        """Generate range of numbers using Runa syntax."""
        if stop is None:
            start, stop = 0, start
        return list(range(start, stop, step))
    
    def absolute_value(self, x: Union[int, float]) -> Union[int, float]:
        """Get absolute value using Runa syntax."""
        return abs(x)
    
    def minimum_value(self, *args) -> Any:
        """Get minimum value using Runa syntax."""
        return min(args)
    
    def maximum_value(self, *args) -> Any:
        """Get maximum value using Runa syntax."""
        return max(args)
    
    def sum_of_all(self, iterable: List[Union[int, float]]) -> Union[int, float]:
        """Sum all values in iterable using Runa syntax."""
        return sum(iterable)
    
    def round_number(self, x: float, ndigits: int = 0) -> float:
        """Round number to specified decimal places using Runa syntax."""
        return round(x, ndigits)
    
    def power_of(self, x: Union[int, float], y: Union[int, float]) -> Union[int, float]:
        """Raise x to the power of y using Runa syntax."""
        return pow(x, y)
    
    def square_root(self, x: float) -> float:
        """Get square root using Runa syntax."""
        return math.sqrt(x)
    
    def sine(self, x: float) -> float:
        """Get sine of angle in radians using Runa syntax."""
        return math.sin(x)
    
    def cosine(self, x: float) -> float:
        """Get cosine of angle in radians using Runa syntax."""
        return math.cos(x)
    
    def tangent(self, x: float) -> float:
        """Get tangent of angle in radians using Runa syntax."""
        return math.tan(x)
    
    def random_number(self) -> float:
        """Get random float between 0 and 1 using Runa syntax."""
        return random.random()
    
    def random_integer(self, a: int, b: int) -> int:
        """Get random integer between a and b inclusive using Runa syntax."""
        return random.randint(a, b)
    
    def choose_random(self, seq: List[Any]) -> Any:
        """Choose random element from sequence using Runa syntax."""
        return random.choice(seq)
    
    def shuffle_sequence(self, seq: List[Any]) -> None:
        """Shuffle sequence in place using Runa syntax."""
        random.shuffle(seq)
    
    def current_time(self) -> float:
        """Get current time in seconds since epoch using Runa syntax."""
        return time.time()
    
    def sleep_for(self, seconds: float) -> None:
        """Sleep for specified seconds using Runa syntax."""
        time.sleep(seconds)
    
    def json_to_string(self, obj: Any) -> str:
        """Convert object to JSON string using Runa syntax."""
        return json.dumps(obj)
    
    def json_from_string(self, s: str) -> Any:
        """Parse JSON string to object using Runa syntax."""
        return json.loads(s)
    
    def ai_think(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """AI thinking function using Runa syntax."""
        return f"AI thinking about: {prompt}"
    
    def ai_learn(self, data: Any, pattern: str) -> bool:
        """AI learning function using Runa syntax."""
        return True
    
    def ai_communicate(self, message: str, target: str) -> str:
        """AI communication function using Runa syntax."""
        return f"Message sent to {target}: {message}"
    
    def ai_translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """AI translation function using Runa syntax."""
        return f"Translated '{text}' from {source_lang} to {target_lang}"
    
    def ai_analyze(self, data: Any, analysis_type: str) -> Dict[str, Any]:
        """AI analysis function using Runa syntax."""
        return {
            "type": analysis_type,
            "data": data,
            "analysis": "AI analysis result"
        }


class RunaRuntime:
    """Main runtime system for executing Runa programs."""
    
    def __init__(self, memory_size: int = 1024 * 1024 * 10):
        self.memory_manager = MemoryManager(memory_size)
        self.builtins = BuiltinFunctions(self)
        self.contexts: Dict[str, RuntimeContext] = {}
        self.current_context: Optional[RuntimeContext] = None
        self.output_buffer: List[str] = []
        self.input_buffer: List[str] = []
        self.performance_monitor = PerformanceMonitor()
        self.global_variables: Dict[str, Any] = {}
        self.global_functions: Dict[str, Callable] = {}
        
        self._init_builtins()
    
    def _init_builtins(self) -> None:
        """Initialize built-in functions in global scope."""
        builtin_methods = [
            'display', 'input_with_prompt', 'length_of', 'type_of', 'range_function',
            'absolute_value', 'minimum_value', 'maximum_value', 'sum_of_all',
            'round_number', 'power_of', 'square_root', 'sine', 'cosine', 'tangent',
            'random_number', 'random_integer', 'choose_random', 'shuffle_sequence',
            'current_time', 'sleep_for', 'json_to_string', 'json_from_string',
            'ai_think', 'ai_learn', 'ai_communicate', 'ai_translate', 'ai_analyze'
        ]
        
        for method_name in builtin_methods:
            method = getattr(self.builtins, method_name)
            self.global_functions[method_name] = method
    
    def create_context(self, program_id: str) -> RuntimeContext:
        """Create a new runtime context for program execution."""
        context = RuntimeContext(
            program_id=program_id,
            start_time=time.time()
        )
        self.contexts[program_id] = context
        return context
    
    def set_context(self, context: RuntimeContext) -> None:
        """Set the current execution context."""
        self.current_context = context
    
    def get_context(self) -> Optional[RuntimeContext]:
        """Get the current execution context."""
        return self.current_context
    
    def execute_bytecode(self, bytecode: List[Dict[str, Any]], context: Optional[RuntimeContext] = None) -> Any:
        """Execute bytecode instructions."""
        if context is None:
            context = self.create_context(f"program_{int(time.time())}")
        
        self.set_context(context)
        start_time = time.time()
        
        stack: List[Any] = []
        variables: Dict[str, Any] = {}
        pc = 0
        
        try:
            while pc < len(bytecode):
                instruction = bytecode[pc]
                opcode = instruction['opcode']
                
                result = self._execute_instruction(opcode, instruction, stack, variables)
                
                if result == 'HALT':
                    break
                elif result == 'JUMP':
                    pc = instruction['target']
                    continue
                elif result == 'CALL':
                    pass
                
                pc += 1
                context.instruction_count += 1
                
                if context.instruction_count > 1000000:
                    raise RunaRuntimeError("Instruction limit exceeded - possible infinite loop")
        
        except Exception as e:
            self.performance_monitor.record_error(str(e))
            raise
        
        finally:
            execution_time = time.time() - start_time
            context.performance_data['execution_time'] = execution_time
            context.performance_data['instructions_executed'] = context.instruction_count
            
            self.performance_monitor.record_operation(
                "program_execution", execution_time,
                {"instructions": context.instruction_count, "program_id": context.program_id}
            )
        
        return stack[-1] if stack else None
    
    def _execute_instruction(self, opcode: str, instruction: Dict[str, Any], 
                           stack: List[Any], variables: Dict[str, Any]) -> str:
        """Execute a single bytecode instruction using Runa operators."""
        if opcode == 'LOAD_CONST':
            stack.append(instruction['value'])
        
        elif opcode == 'LOAD_VAR':
            var_name = instruction['name']
            if var_name in variables:
                stack.append(variables[var_name])
            elif var_name in self.global_variables:
                stack.append(self.global_variables[var_name])
            else:
                raise RunaRuntimeError(f"Undefined variable: {var_name}")
        
        elif opcode == 'STORE_VAR':
            var_name = instruction['name']
            value = stack.pop()
            variables[var_name] = value
        
        elif opcode == 'BINARY_OP':
            right = stack.pop()
            left = stack.pop()
            operator = instruction['operator']
            
            if operator == 'plus':
                result = left + right
            elif operator == 'minus':
                result = left - right
            elif operator == 'multiplied by':
                result = left * right
            elif operator == 'divided by':
                if right == 0:
                    raise RunaRuntimeError("Division by zero")
                result = left / right
            elif operator == 'modulo':
                result = left % right
            elif operator == 'power of':
                result = left ** right
            elif operator == 'is equal to':
                result = left == right
            elif operator == 'is not equal to':
                result = left != right
            elif operator == 'is greater than':
                result = left > right
            elif operator == 'is less than':
                result = left < right
            elif operator == 'is greater than or equal to':
                result = left >= right
            elif operator == 'is less than or equal to':
                result = left <= right
            elif operator == 'and':
                result = left and right
            elif operator == 'or':
                result = left or right
            elif operator == 'contains':
                result = right in left
            elif operator == 'followed by':
                result = str(left) + str(right)
            else:
                raise RunaRuntimeError(f"Unknown binary operator: {operator}")
            
            stack.append(result)
        
        elif opcode == 'UNARY_OP':
            value = stack.pop()
            operator = instruction['operator']
            
            if operator == 'minus':
                result = -value
            elif operator == 'not':
                result = not value
            else:
                raise RunaRuntimeError(f"Unknown unary operator: {operator}")
            
            stack.append(result)
        
        elif opcode == 'CALL':
            func_name = instruction['name']
            arg_count = instruction['arg_count']
            args = [stack.pop() for _ in range(arg_count)]
            args.reverse()
            
            if func_name in self.global_functions:
                result = self.global_functions[func_name](*args)
            else:
                raise RunaRuntimeError(f"Undefined function: {func_name}")
            
            stack.append(result)
        
        elif opcode == 'JUMP':
            return 'JUMP'
        
        elif opcode == 'JUMP_IF_FALSE':
            condition = stack.pop()
            if not condition:
                return 'JUMP'
        
        elif opcode == 'RETURN':
            return 'HALT'
        
        else:
            raise RunaRuntimeError(f"Unknown opcode: {opcode}")
        
        return 'CONTINUE'
    
    def get_output(self) -> str:
        """Get all output from the runtime."""
        output = ''.join(self.output_buffer)
        self.output_buffer.clear()
        return output
    
    def add_input(self, input_data: str) -> None:
        """Add input data to the runtime."""
        self.input_buffer.append(input_data)
    
    def get_input(self) -> str:
        """Get input data from the runtime."""
        if self.input_buffer:
            return self.input_buffer.pop(0)
        return ""
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory usage statistics."""
        return self.memory_manager.get_memory_stats()
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics."""
        return self.performance_monitor.get_stats()
    
    def cleanup(self) -> None:
        """Clean up runtime resources."""
        self.memory_manager.garbage_collect()
        self.contexts.clear()
        self.output_buffer.clear()
        self.input_buffer.clear()


# Global runtime instance
_runtime_instance: Optional[RunaRuntime] = None


def get_runtime() -> RunaRuntime:
    """Get the global runtime instance."""
    global _runtime_instance
    if _runtime_instance is None:
        _runtime_instance = RunaRuntime()
    return _runtime_instance


def reset_runtime() -> None:
    """Reset the global runtime instance."""
    global _runtime_instance
    if _runtime_instance:
        _runtime_instance.cleanup()
    _runtime_instance = None 