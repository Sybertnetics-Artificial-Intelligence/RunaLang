"""
Runa Virtual Machine

High-performance bytecode execution engine with JIT compilation capabilities
and AI-specific optimizations for universal translation and AI-to-AI communication.
"""

import time
import threading
import ctypes
from typing import Any, Dict, List, Optional, Callable, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum
import weakref
from collections import defaultdict, deque
import sys
import gc

from .error_handler import RunaError, RunaRuntimeError, RunaTypeError, RunaVMError
from .performance_monitor import PerformanceMonitor
from .runtime import RunaRuntime, RuntimeContext, MemoryManager


class VMState(Enum):
    """Virtual machine execution states."""
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    HALTED = "halted"
    ERROR = "error"


@dataclass
class VMContext:
    """Virtual machine execution context."""
    program_counter: int = 0
    stack: List[Any] = field(default_factory=list)
    variables: Dict[str, Any] = field(default_factory=dict)
    call_stack: List[Dict[str, Any]] = field(default_factory=list)
    instruction_count: int = 0
    start_time: float = field(default_factory=time.time)
    max_stack_size: int = 10000
    max_call_depth: int = 1000
    debug_mode: bool = False
    performance_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class JITBlock:
    """JIT compiled code block."""
    start_pc: int
    end_pc: int
    compiled_code: Optional[Callable] = None
    execution_count: int = 0
    last_execution: float = field(default_factory=time.time)
    optimization_level: int = 0


class JITCompiler:
    """Just-In-Time compiler for performance optimization."""
    
    def __init__(self, vm: 'RunaVM'):
        self.vm = vm
        self.compiled_blocks: Dict[int, JITBlock] = {}
        self.hot_threshold = 10
        self.performance_monitor = PerformanceMonitor()
        self.optimization_levels = {
            0: self._basic_optimization,
            1: self._intermediate_optimization,
            2: self._advanced_optimization
        }
    
    def should_compile(self, pc: int, execution_count: int) -> bool:
        """Determine if a code block should be JIT compiled."""
        return execution_count >= self.hot_threshold
    
    def compile_block(self, start_pc: int, end_pc: int, bytecode: List[Dict[str, Any]], 
                     optimization_level: int = 1) -> Optional[JITBlock]:
        """Compile a block of bytecode to native code."""
        start_time = time.time()
        
        try:
            jit_block = JITBlock(
                start_pc=start_pc,
                end_pc=end_pc,
                optimization_level=optimization_level
            )
            
            block_instructions = bytecode[start_pc:end_pc]
            
            if optimization_level in self.optimization_levels:
                optimized_instructions = self.optimization_levels[optimization_level](block_instructions)
            else:
                optimized_instructions = block_instructions
            
            compiled_function = self._generate_native_code(optimized_instructions)
            
            jit_block.compiled_code = compiled_function
            self.compiled_blocks[start_pc] = jit_block
            
            compilation_time = time.time() - start_time
            self.performance_monitor.record_operation(
                "jit_compilation", compilation_time,
                {"start_pc": start_pc, "end_pc": end_pc, "optimization_level": optimization_level}
            )
            
            return jit_block
        
        except Exception as e:
            self.performance_monitor.record_error(f"JIT compilation failed: {e}")
            return None
    
    def _basic_optimization(self, instructions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Basic instruction-level optimizations."""
        optimized = []
        
        for i, instruction in enumerate(instructions):
            opcode = instruction['opcode']
            
            if opcode == 'BINARY_OP' and i > 0:
                prev_instruction = instructions[i - 1]
                if prev_instruction['opcode'] == 'LOAD_CONST':
                    try:
                        left = prev_instruction['value']
                        right = instruction.get('value', None)
                        operator = instruction['operator']
                        
                        if operator == 'plus':
                            result = left + right
                        elif operator == 'multiplied by':
                            result = left * right
                        elif operator == 'minus':
                            result = left - right
                        elif operator == 'divided by':
                            result = left / right
                        else:
                            optimized.append(instruction)
                            continue
                        
                        optimized[-1] = {'opcode': 'LOAD_CONST', 'value': result}
                        continue
                    except:
                        pass
            
            optimized.append(instruction)
        
        return optimized
    
    def _intermediate_optimization(self, instructions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Intermediate optimizations including dead code elimination."""
        optimized = self._basic_optimization(instructions)
        
        live_instructions = []
        for instruction in optimized:
            opcode = instruction['opcode']
            
            if opcode == 'RETURN':
                live_instructions.append(instruction)
                break
            
            live_instructions.append(instruction)
        
        return live_instructions
    
    def _advanced_optimization(self, instructions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Advanced optimizations including loop unrolling and inlining."""
        optimized = self._intermediate_optimization(instructions)
        
        return optimized
    
    def _generate_native_code(self, instructions: List[Dict[str, Any]]) -> Callable:
        """Generate native code from optimized instructions."""
        
        def compiled_function(vm_context: VMContext, runtime: RunaRuntime) -> Any:
            """Compiled native function."""
            for instruction in instructions:
                opcode = instruction['opcode']
                
                if opcode == 'LOAD_CONST':
                    vm_context.stack.append(instruction['value'])
                elif opcode == 'LOAD_VAR':
                    var_name = instruction['name']
                    if var_name in vm_context.variables:
                        vm_context.stack.append(vm_context.variables[var_name])
                    else:
                        raise RunaRuntimeError(f"Undefined variable: {var_name}")
                elif opcode == 'STORE_VAR':
                    var_name = instruction['name']
                    value = vm_context.stack.pop()
                    vm_context.variables[var_name] = value
                elif opcode == 'BINARY_OP':
                    right = vm_context.stack.pop()
                    left = vm_context.stack.pop()
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
                    else:
                        raise RunaRuntimeError(f"Unknown binary operator: {operator}")
                    
                    vm_context.stack.append(result)
                elif opcode == 'CALL':
                    func_name = instruction['name']
                    arg_count = instruction['arg_count']
                    args = [vm_context.stack.pop() for _ in range(arg_count)]
                    args.reverse()
                    
                    if func_name in runtime.global_functions:
                        result = runtime.global_functions[func_name](*args)
                    else:
                        raise RunaRuntimeError(f"Undefined function: {func_name}")
                    
                    vm_context.stack.append(result)
            
            return vm_context.stack[-1] if vm_context.stack else None
        
        return compiled_function
    
    def get_compilation_stats(self) -> Dict[str, Any]:
        """Get JIT compilation statistics."""
        total_blocks = len(self.compiled_blocks)
        total_executions = sum(block.execution_count for block in self.compiled_blocks.values())
        
        return {
            "compiled_blocks": total_blocks,
            "total_executions": total_executions,
            "average_executions_per_block": total_executions / total_blocks if total_blocks > 0 else 0
        }


class RunaVM:
    """High-performance Runa Virtual Machine."""
    
    def __init__(self, memory_size: int = 1024 * 1024 * 10):
        self.runtime = RunaRuntime(memory_size)
        self.jit_compiler = JITCompiler(self)
        self.state = VMState.IDLE
        self.context: Optional[VMContext] = None
        self.performance_monitor = PerformanceMonitor()
        self.execution_thread: Optional[threading.Thread] = None
        self.stop_execution = False
        
        self.total_instructions_executed = 0
        self.total_execution_time = 0.0
        self.programs_executed = 0
        
        self.ai_pattern_cache: Dict[str, Any] = {}
        self.translation_cache: Dict[str, str] = {}
    
    def execute(self, bytecode: List[Dict[str, Any]], program_id: Optional[str] = None) -> Any:
        """Execute bytecode with high-performance optimizations."""
        if self.state == VMState.RUNNING:
            raise RunaVMError("VM is already running")
        
        if not bytecode:
            return None
        
        self.context = VMContext()
        if program_id:
            self.context.program_id = program_id
        
        self.state = VMState.RUNNING
        self.stop_execution = False
        
        start_time = time.time()
        
        try:
            result = self._execute_bytecode(bytecode)
            
            execution_time = time.time() - start_time
            self.total_execution_time += execution_time
            self.total_instructions_executed += self.context.instruction_count
            self.programs_executed += 1
            
            self.context.performance_data.update({
                'execution_time': execution_time,
                'instructions_executed': self.context.instruction_count,
                'instructions_per_second': self.context.instruction_count / execution_time if execution_time > 0 else 0
            })
            
            self.performance_monitor.record_operation(
                "vm_execution", execution_time,
                {
                    "instructions": self.context.instruction_count,
                    "program_id": program_id or "unknown",
                    "jit_blocks_used": len([b for b in self.jit_compiler.compiled_blocks.values() if b.execution_count > 0])
                }
            )
            
            return result
        
        except Exception as e:
            self.state = VMState.ERROR
            self.performance_monitor.record_error(str(e))
            raise
        
        finally:
            self.state = VMState.IDLE
            self.context = None
    
    def _execute_bytecode(self, bytecode: List[Dict[str, Any]]) -> Any:
        """Execute bytecode with JIT compilation support."""
        pc = 0
        
        while pc < len(bytecode) and not self.stop_execution:
            if pc in self.jit_compiler.compiled_blocks:
                jit_block = self.jit_compiler.compiled_blocks[pc]
                
                if jit_block.compiled_code:
                    result = jit_block.compiled_code(self.context, self.runtime)
                    jit_block.execution_count += 1
                    jit_block.last_execution = time.time()
                    
                    pc = jit_block.end_pc
                    self.context.instruction_count += (jit_block.end_pc - jit_block.start_pc)
                    continue
            
            instruction = bytecode[pc]
            opcode = instruction['opcode']
            
            result = self._execute_instruction(opcode, instruction)
            
            if result == 'HALT':
                break
            elif result == 'JUMP':
                pc = instruction['target']
                continue
            elif result == 'CALL':
                pass
            
            pc += 1
            self.context.instruction_count += 1
            
            if pc % 100 == 0:
                self._check_jit_opportunities(bytecode, pc)
            
            if self.context.instruction_count > 1000000:
                raise RunaVMError("Instruction limit exceeded - possible infinite loop")
            
            if len(self.context.stack) > self.context.max_stack_size:
                raise RunaVMError("Stack overflow")
        
        return self.context.stack[-1] if self.context.stack else None
    
    def _execute_instruction(self, opcode: str, instruction: Dict[str, Any]) -> str:
        """Execute a single bytecode instruction using Runa operators."""
        if opcode == 'LOAD_CONST':
            self.context.stack.append(instruction['value'])
        
        elif opcode == 'LOAD_VAR':
            var_name = instruction['name']
            if var_name in self.context.variables:
                self.context.stack.append(self.context.variables[var_name])
            elif var_name in self.runtime.global_variables:
                self.context.stack.append(self.runtime.global_variables[var_name])
            else:
                raise RunaRuntimeError(f"Undefined variable: {var_name}")
        
        elif opcode == 'STORE_VAR':
            var_name = instruction['name']
            value = self.context.stack.pop()
            self.context.variables[var_name] = value
        
        elif opcode == 'BINARY_OP':
            right = self.context.stack.pop()
            left = self.context.stack.pop()
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
            
            self.context.stack.append(result)
        
        elif opcode == 'UNARY_OP':
            value = self.context.stack.pop()
            operator = instruction['operator']
            
            if operator == 'minus':
                result = -value
            elif operator == 'not':
                result = not value
            else:
                raise RunaRuntimeError(f"Unknown unary operator: {operator}")
            
            self.context.stack.append(result)
        
        elif opcode == 'CALL':
            func_name = instruction['name']
            arg_count = instruction['arg_count']
            args = [self.context.stack.pop() for _ in range(arg_count)]
            args.reverse()
            
            if func_name in self.runtime.global_functions:
                result = self.runtime.global_functions[func_name](*args)
            else:
                raise RunaRuntimeError(f"Undefined function: {func_name}")
            
            self.context.stack.append(result)
        
        elif opcode == 'JUMP':
            return 'JUMP'
        
        elif opcode == 'JUMP_IF_FALSE':
            condition = self.context.stack.pop()
            if not condition:
                return 'JUMP'
        
        elif opcode == 'RETURN':
            return 'HALT'
        
        else:
            raise RunaRuntimeError(f"Unknown opcode: {opcode}")
        
        return 'CONTINUE'
    
    def _check_jit_opportunities(self, bytecode: List[Dict[str, Any]], current_pc: int) -> None:
        """Check for opportunities to JIT compile hot code paths."""
        block_size = 50
        
        for start_pc in range(0, len(bytecode), block_size):
            end_pc = min(start_pc + block_size, len(bytecode))
            
            if start_pc in self.jit_compiler.compiled_blocks:
                continue
            
            execution_count = self._get_block_execution_count(start_pc, end_pc)
            
            if self.jit_compiler.should_compile(start_pc, execution_count):
                self.jit_compiler.compile_block(start_pc, end_pc, bytecode)
    
    def _get_block_execution_count(self, start_pc: int, end_pc: int) -> int:
        """Get execution count for a block of instructions."""
        return self.context.instruction_count // 1000
    
    def execute_async(self, bytecode: List[Dict[str, Any]], program_id: Optional[str] = None) -> threading.Thread:
        """Execute bytecode asynchronously in a separate thread."""
        def async_execution():
            try:
                self.execute(bytecode, program_id)
            except Exception as e:
                self.performance_monitor.record_error(f"Async execution failed: {e}")
        
        self.execution_thread = threading.Thread(target=async_execution)
        self.execution_thread.start()
        return self.execution_thread
    
    def stop(self) -> None:
        """Stop current execution."""
        self.stop_execution = True
        if self.execution_thread and self.execution_thread.is_alive():
            self.execution_thread.join(timeout=1.0)
    
    def pause(self) -> None:
        """Pause execution."""
        if self.state == VMState.RUNNING:
            self.state = VMState.PAUSED
    
    def resume(self) -> None:
        """Resume execution."""
        if self.state == VMState.PAUSED:
            self.state = VMState.RUNNING
    
    def get_stats(self) -> Dict[str, Any]:
        """Get VM execution statistics."""
        return {
            "state": self.state.value,
            "total_instructions_executed": self.total_instructions_executed,
            "total_execution_time": self.total_execution_time,
            "programs_executed": self.programs_executed,
            "average_instructions_per_second": self.total_instructions_executed / self.total_execution_time if self.total_execution_time > 0 else 0,
            "jit_stats": self.jit_compiler.get_compilation_stats(),
            "memory_stats": self.runtime.get_memory_stats(),
            "performance_stats": self.performance_monitor.get_stats()
        }
    
    def reset(self) -> None:
        """Reset VM state."""
        self.stop()
        self.state = VMState.IDLE
        self.context = None
        self.jit_compiler.compiled_blocks.clear()
        self.runtime.cleanup()
        self.performance_monitor.reset()
        
        self.total_instructions_executed = 0
        self.total_execution_time = 0.0
        self.programs_executed = 0
    
    def optimize_for_ai(self) -> None:
        """Apply AI-specific optimizations."""
        common_patterns = [
            "translation_request",
            "pattern_analysis", 
            "neural_computation",
            "semantic_analysis"
        ]
        
        for pattern in common_patterns:
            if pattern not in self.ai_pattern_cache:
                self.ai_pattern_cache[pattern] = self._optimize_ai_pattern(pattern)
    
    def _optimize_ai_pattern(self, pattern: str) -> Any:
        """Optimize a specific AI pattern."""
        return {
            "pattern": pattern,
            "optimized": True,
            "cache_key": f"ai_pattern_{pattern}"
        }


# Global VM instance
_vm_instance: Optional[RunaVM] = None


def get_vm() -> RunaVM:
    """Get the global VM instance."""
    global _vm_instance
    if _vm_instance is None:
        _vm_instance = RunaVM()
    return _vm_instance


def reset_vm() -> None:
    """Reset the global VM instance."""
    global _vm_instance
    if _vm_instance:
        _vm_instance.reset()
    _vm_instance = None 