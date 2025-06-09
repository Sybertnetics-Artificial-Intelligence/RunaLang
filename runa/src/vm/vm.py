"""
Virtual Machine for the Runa programming language.

This module provides the virtual machine that executes Runa bytecode.
It includes a stack-based interpreter with memory management and garbage collection.
"""

import sys
import time
from typing import List, Dict, Any, Optional, Union, Set, Tuple, Callable
from enum import Enum, auto
import gc
from dataclasses import dataclass
import os

from .instructions import OpCode, Instruction
from .bytecode import BytecodeModule
from .compiler import Compiler


class VMValueType(Enum):
    """Type of a value in the VM."""
    NULL = auto()
    BOOLEAN = auto()
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    LIST = auto()
    DICT = auto()
    FUNCTION = auto()
    OBJECT = auto()
    MODULE = auto()
    ITERATOR = auto()
    NATIVE_FUNCTION = auto()
    TYPE = auto()
    VECTOR = auto()
    TENSOR = auto()
    NEURAL_NETWORK = auto()
    CLOSURE = auto()


@dataclass
class VMValue:
    """
    Represents a value in the Runa VM.
    
    Attributes:
        type: The type of the value
        value: The actual value
    """
    
    type: VMValueType
    value: Any
    
    def __str__(self) -> str:
        """Return a string representation of the value."""
        if self.type == VMValueType.NULL:
            return "null"
        elif self.type == VMValueType.BOOLEAN:
            return "true" if self.value else "false"
        elif self.type in [VMValueType.INTEGER, VMValueType.FLOAT]:
            return str(self.value)
        elif self.type == VMValueType.STRING:
            return f'"{self.value}"'
        elif self.type == VMValueType.LIST:
            items = ", ".join(str(item) for item in self.value)
            return f"[{items}]"
        elif self.type == VMValueType.DICT:
            items = ", ".join(f"{key}: {value}" for key, value in self.value.items())
            return f"{{{items}}}"
        elif self.type == VMValueType.FUNCTION:
            return f"<function {self.value.get('name', 'anonymous')}>"
        elif self.type == VMValueType.OBJECT:
            return f"<object of type {self.value.get('type', 'unknown')}>"
        elif self.type == VMValueType.MODULE:
            return f"<module {self.value.get('name', 'unknown')}>"
        elif self.type == VMValueType.ITERATOR:
            return "<iterator>"
        elif self.type == VMValueType.NATIVE_FUNCTION:
            return "<native function>"
        elif self.type == VMValueType.TYPE:
            return f"<type {self.value.get('name', 'anonymous')}>"
        elif self.type == VMValueType.VECTOR:
            return f"<vector of size {len(self.value)}>"
        elif self.type == VMValueType.TENSOR:
            return f"<tensor of shape {self.value.shape}>"
        elif self.type == VMValueType.NEURAL_NETWORK:
            return "<neural network>"
        elif self.type == VMValueType.CLOSURE:
            return f"<closure for {self.value.name}>"
        return f"<unknown value of type {self.type}>"
    
    def __eq__(self, other) -> bool:
        """Compare two VM values for equality."""
        if not isinstance(other, VMValue):
            return False
        
        if self.type != other.type:
            return False
        
        return self.value == other.value
    
    def is_truthy(self) -> bool:
        """
        Determine if the value is truthy in Runa.
        
        Returns:
            True if the value is truthy, False otherwise
        """
        if self.type == VMValueType.NULL:
            return False
        
        if self.type == VMValueType.BOOLEAN:
            return self.value
        
        if self.type in [VMValueType.INTEGER, VMValueType.FLOAT]:
            return self.value != 0
        
        if self.type in [VMValueType.STRING, VMValueType.LIST, VMValueType.DICT]:
            return len(self.value) > 0
        
        # All other values are truthy
        return True


@dataclass
class VMClosure:
    """
    Represents a closure in the VM.
    
    Attributes:
        name: The name of the function
        module: The module containing the function
        captured_vars: The captured variables
    """
    
    name: str
    module: BytecodeModule
    captured_vars: List[VMValue]
    
    def __init__(self, name: str, module: BytecodeModule):
        """
        Initialize a new VMClosure.
        
        Args:
            name: The name of the function
            module: The module containing the function
        """
        self.name = name
        self.module = module
        self.captured_vars = []


@dataclass
class VMFrame:
    """
    Represents a frame on the call stack.
    
    Attributes:
        module: The bytecode module being executed
        ip: The instruction pointer
        stack: The operand stack
        locals: The local variables
        globals: The global variables
        upvalues: The upvalues (captured variables)
        try_handlers: The try handler stack
        closure: The closure for this frame (if any)
    """
    
    module: BytecodeModule
    ip: int = 0
    stack: List[VMValue] = None
    locals: List[VMValue] = None
    globals: Dict[str, VMValue] = None
    upvalues: List[List[VMValue]] = None
    try_handlers: List[Tuple[int, int, int]] = None  # [(try_start, catch_start, catch_end), ...]
    closure: Optional[VMClosure] = None
    
    def __post_init__(self):
        """Initialize default values for None fields."""
        if self.stack is None:
            self.stack = []
        if self.locals is None:
            self.locals = []
        if self.globals is None:
            self.globals = {}
        if self.upvalues is None:
            self.upvalues = []
        if self.try_handlers is None:
            self.try_handlers = []


class VirtualMachine:
    """
    Virtual Machine for executing Runa bytecode.
    
    The VM uses a stack-based architecture with a call stack, operand stack,
    and memory management with garbage collection.
    
    Attributes:
        frames: The call stack of execution frames
        modules: The loaded modules
        native_functions: The registered native functions
        debug_mode: Whether debug mode is enabled
        current_error: The current error being handled
        error_thrown: Whether an error has been thrown
    """
    
    def __init__(self, debug_mode: bool = False):
        """
        Initialize a new virtual machine.
        
        Args:
            debug_mode: Whether to enable debug mode
        """
        # VM state
        self.frames = []
        self.global_vars = {}
        self.modules = {}
        self.module_cache = {}
        self.module_search_paths = [".", "./modules", "./lib"]
        self.namespaces = {}
        self.native_functions = {}
        self.error_thrown = False
        self.current_error = None
        self.debug_mode = debug_mode
        
        # Performance metrics
        self.instruction_count = 0
        self.call_count = 0
        self.start_time = time.time()
        
        # Register native functions
        self._register_native_functions()
        
        # Load standard library
        self._load_stdlib()
    
    def _register_native_functions(self) -> None:
        """Register built-in native functions."""
        self.native_functions["print"] = self._native_print
        self.native_functions["input"] = self._native_input
        self.native_functions["len"] = self._native_len
        self.native_functions["type"] = self._native_type
        self.native_functions["range"] = self._native_range
        self.native_functions["gc_collect"] = self._native_gc_collect
    
    def _load_stdlib(self) -> None:
        """Load the standard library modules."""
        try:
            # Import standard library modules
            from runa.src.stdlib.core.builtins import register_core_builtins
            from runa.src.stdlib.core.error import register_error_functions
            from runa.src.stdlib.core.module import register_module_functions
            from runa.src.stdlib.io.file import register_file_functions
            from runa.src.stdlib.io.stream import register_stream_functions
            from runa.src.stdlib.collections.advanced import register_collection_functions
            from runa.src.stdlib.math.functions import register_math_functions
            
            # Register standard library functions
            register_core_builtins(self)
            register_error_functions(self)
            register_module_functions(self)
            register_file_functions(self)
            register_stream_functions(self)
            register_collection_functions(self)
            register_math_functions(self)
            
        except ImportError as e:
            print(f"Warning: Failed to load standard library: {e}", file=sys.stderr)
    
    def _native_print(self, *args) -> VMValue:
        """
        Native print function.
        
        Args:
            *args: The arguments to print
            
        Returns:
            A null VM value
        """
        print(*[str(arg) for arg in args])
        return VMValue(VMValueType.NULL, None)
    
    def _native_input(self, prompt: Optional[VMValue] = None) -> VMValue:
        """
        Native input function.
        
        Args:
            prompt: The prompt to display
            
        Returns:
            A string VM value with the user input
        """
        if prompt and prompt.type == VMValueType.STRING:
            user_input = input(prompt.value)
        else:
            user_input = input()
        return VMValue(VMValueType.STRING, user_input)
    
    def _native_len(self, value: VMValue) -> VMValue:
        """
        Native len function.
        
        Args:
            value: The value to get the length of
            
        Returns:
            An integer VM value with the length
        """
        if value.type in [VMValueType.STRING, VMValueType.LIST, VMValueType.DICT]:
            return VMValue(VMValueType.INTEGER, len(value.value))
        
        # Error: value has no length
        raise ValueError(f"Cannot get length of {value}")
    
    def _native_type(self, value: VMValue) -> VMValue:
        """
        Native type function.
        
        Args:
            value: The value to get the type of
            
        Returns:
            A string VM value with the type name
        """
        type_names = {
            VMValueType.NULL: "Null",
            VMValueType.BOOLEAN: "Boolean",
            VMValueType.INTEGER: "Integer",
            VMValueType.FLOAT: "Float",
            VMValueType.STRING: "String",
            VMValueType.LIST: "List",
            VMValueType.DICT: "Dictionary",
            VMValueType.FUNCTION: "Function",
            VMValueType.OBJECT: "Object",
            VMValueType.MODULE: "Module",
            VMValueType.ITERATOR: "Iterator",
            VMValueType.NATIVE_FUNCTION: "NativeFunction",
            VMValueType.TYPE: "Type",
            VMValueType.VECTOR: "Vector",
            VMValueType.TENSOR: "Tensor",
            VMValueType.NEURAL_NETWORK: "NeuralNetwork",
        }
        return VMValue(VMValueType.STRING, type_names[value.type])
    
    def _native_range(self, *args) -> VMValue:
        """
        Native range function.
        
        Args:
            *args: The arguments to range (start, stop, step)
            
        Returns:
            A list VM value with the range
        """
        if len(args) == 1:
            # range(stop)
            stop = args[0].value
            start, step = 0, 1
        elif len(args) == 2:
            # range(start, stop)
            start, stop = args[0].value, args[1].value
            step = 1
        elif len(args) == 3:
            # range(start, stop, step)
            start, stop, step = args[0].value, args[1].value, args[2].value
        else:
            raise ValueError("range() takes 1-3 arguments")
        
        range_list = list(range(start, stop, step))
        return VMValue(VMValueType.LIST, [VMValue(VMValueType.INTEGER, i) for i in range_list])
    
    def _native_gc_collect(self) -> VMValue:
        """
        Native gc_collect function.
        
        Returns:
            An integer VM value with the number of objects collected
        """
        count = gc.collect()
        return VMValue(VMValueType.INTEGER, count)
    
    def load_module(self, module: BytecodeModule) -> None:
        """
        Load a bytecode module into the VM.
        
        Args:
            module: The module to load
        """
        self.modules[module.name] = module
    
    def execute_module(self, module_name: str) -> VMValue:
        """
        Execute a loaded module.
        
        Args:
            module_name: The name of the module to execute
            
        Returns:
            The result of executing the module
        """
        if module_name not in self.modules:
            raise ValueError(f"Module {module_name} not loaded")
        
        module = self.modules[module_name]
        
        # Create a new frame for the module
        frame = VMFrame(
            module=module,
            globals={name: VMValue(VMValueType.NULL, None) for name in module.global_names}
        )
        
        # Push the frame onto the call stack
        self.frames.append(frame)
        
        # Execute the module
        self.start_time = time.time()
        result = self._execute()
        self.end_time = time.time()
        
        return result
    
    def _execute(self) -> VMValue:
        """
        Execute the current frame until it returns.
        
        Returns:
            The result of execution
        """
        # Get the current frame
        frame = self.frames[-1]
        
        # Execute instructions until return
        while True:
            # Check if we've reached the end of the instructions
            if frame.ip >= len(frame.module.instructions):
                # Implicit return null
                if not frame.stack:
                    frame.stack.append(VMValue(VMValueType.NULL, None))
                
                # Return the top of the stack
                result = frame.stack.pop()
                
                # Pop the frame
                self.frames.pop()
                
                return result
            
            # Get the current instruction
            instruction = frame.module.instructions[frame.ip]
            
            # Increment the instruction pointer
            frame.ip += 1
            
            # Increment the instruction count
            self.instruction_count += 1
            
            # Execute the instruction
            result = self._execute_instruction(instruction, frame)
            
            # If the instruction returned a value, return it
            if result is not None:
                return result
    
    def _execute_instruction(self, instruction: Instruction, frame: VMFrame) -> Optional[VMValue]:
        """
        Execute a single instruction.
        
        Args:
            instruction: The instruction to execute
            frame: The current frame
            
        Returns:
            The result of the instruction, or None if no result
        """
        # Update metrics
        self.instruction_count += 1
        
        # Check for error propagation
        if self.error_thrown:
            # Look for a try handler in the current frame
            for try_start, catch_start, catch_end in reversed(frame.try_handlers):
                # If we're in a try block, jump to the catch handler
                if try_start <= frame.ip <= catch_start:
                    frame.ip = catch_start
                    return None
                
                # If we're in a catch block for this error, continue execution
                if catch_start <= frame.ip <= catch_end:
                    # Reset error state
                    self.error_thrown = False
                    self.current_error = None
                    return None
            
            # If we're not in a try block, propagate the error to the caller
            if len(self.frames) > 1:
                # Pop the current frame
                self.frames.pop()
                
                # Continue error propagation in the caller frame
                return None
            
            # If we're in the top-level frame, print the error and terminate
            error_str = str(self.current_error)
            print(f"Unhandled error: {error_str}", file=sys.stderr)
            
            # Reset error state
            self.error_thrown = False
            self.current_error = None
            
            # Terminate execution
            return VMValue(VMValueType.NULL, None)
        
        # Normal instruction execution
        op = instruction.opcode
        
        # Control flow instructions
        if op == OpCode.JUMP:
            frame.ip = instruction.operand
            return None
        elif op == OpCode.JUMP_IF_FALSE:
            value = frame.stack.pop()
            if not value.is_truthy():
                frame.ip = instruction.operand
            return None
        elif op == OpCode.JUMP_IF_TRUE:
            value = frame.stack.pop()
            if value.is_truthy():
                frame.ip = instruction.operand
            return None
        
        # Try-catch instructions
        elif op == OpCode.TRY_BEGIN:
            # try_start, catch_start, catch_end
            frame.try_handlers.append((frame.ip, instruction.operand, 0))  # catch_end will be set by TRY_END
            return None
        elif op == OpCode.TRY_END:
            # Set the catch_end for the current try handler
            if frame.try_handlers:
                try_start, catch_start, _ = frame.try_handlers[-1]
                frame.try_handlers[-1] = (try_start, catch_start, instruction.operand)
            return None
        elif op == OpCode.CATCH_BEGIN:
            # This is handled by the error propagation logic above
            return None
        elif op == OpCode.CATCH_END:
            # End of catch block, just continue execution
            return None
        
        # Debug output
        if self.debug_mode:
            print(f"Executing: {instruction}")
            print(f"Stack: {frame.stack}")
        
        # Execute the instruction based on opcode
        if op == OpCode.NOP:
            # No operation
            pass
        
        elif op == OpCode.PUSH_NULL:
            # Push null onto stack
            frame.stack.append(VMValue(VMValueType.NULL, None))
        
        elif op == OpCode.PUSH_TRUE:
            # Push true onto stack
            frame.stack.append(VMValue(VMValueType.BOOLEAN, True))
        
        elif op == OpCode.PUSH_FALSE:
            # Push false onto stack
            frame.stack.append(VMValue(VMValueType.BOOLEAN, False))
        
        elif op == OpCode.PUSH_INT:
            # Push integer onto stack
            frame.stack.append(VMValue(VMValueType.INTEGER, instruction.operands[0]))
        
        elif op == OpCode.PUSH_FLOAT:
            # Push float onto stack
            frame.stack.append(VMValue(VMValueType.FLOAT, instruction.operands[0]))
        
        elif op == OpCode.PUSH_STRING:
            # Push string onto stack
            frame.stack.append(VMValue(VMValueType.STRING, instruction.operands[0]))
        
        elif op == OpCode.POP:
            # Pop value from stack
            frame.stack.pop()
        
        elif op == OpCode.DUP:
            # Duplicate top of stack
            frame.stack.append(frame.stack[-1])
        
        elif op == OpCode.SWAP:
            # Swap top two values on stack
            frame.stack[-1], frame.stack[-2] = frame.stack[-2], frame.stack[-1]
        
        elif op == OpCode.ADD:
            # Add top two values on stack
            right = frame.stack.pop()
            left = frame.stack.pop()
            
            if left.type == VMValueType.INTEGER and right.type == VMValueType.INTEGER:
                # Integer addition
                frame.stack.append(VMValue(VMValueType.INTEGER, left.value + right.value))
            
            elif left.type in [VMValueType.INTEGER, VMValueType.FLOAT] and right.type in [VMValueType.INTEGER, VMValueType.FLOAT]:
                # Float addition
                frame.stack.append(VMValue(VMValueType.FLOAT, float(left.value) + float(right.value)))
            
            elif left.type == VMValueType.STRING and right.type == VMValueType.STRING:
                # String concatenation
                frame.stack.append(VMValue(VMValueType.STRING, left.value + right.value))
            
            elif left.type == VMValueType.LIST and right.type == VMValueType.LIST:
                # List concatenation
                frame.stack.append(VMValue(VMValueType.LIST, left.value + right.value))
            
            elif left.type == VMValueType.VECTOR and right.type == VMValueType.VECTOR:
                # Vector addition
                if len(left.value) != len(right.value):
                    raise ValueError("Cannot add vectors of different lengths")
                
                result = [VMValue(VMValueType.FLOAT, left.value[i].value + right.value[i].value) 
                         for i in range(len(left.value))]
                frame.stack.append(VMValue(VMValueType.VECTOR, result))
            
            else:
                raise ValueError(f"Cannot add {left} and {right}")
        
        elif op == OpCode.SUB:
            # Subtract top value from second value on stack
            right = frame.stack.pop()
            left = frame.stack.pop()
            
            if left.type == VMValueType.INTEGER and right.type == VMValueType.INTEGER:
                # Integer subtraction
                frame.stack.append(VMValue(VMValueType.INTEGER, left.value - right.value))
            
            elif left.type in [VMValueType.INTEGER, VMValueType.FLOAT] and right.type in [VMValueType.INTEGER, VMValueType.FLOAT]:
                # Float subtraction
                frame.stack.append(VMValue(VMValueType.FLOAT, float(left.value) - float(right.value)))
            
            elif left.type == VMValueType.VECTOR and right.type == VMValueType.VECTOR:
                # Vector subtraction
                if len(left.value) != len(right.value):
                    raise ValueError("Cannot subtract vectors of different lengths")
                
                result = [VMValue(VMValueType.FLOAT, left.value[i].value - right.value[i].value) 
                         for i in range(len(left.value))]
                frame.stack.append(VMValue(VMValueType.VECTOR, result))
            
            else:
                raise ValueError(f"Cannot subtract {right} from {left}")
        
        elif op == OpCode.RET:
            # Return from function with top of stack as return value
            result = frame.stack.pop() if frame.stack else VMValue(VMValueType.NULL, None)
            
            # Pop the frame
            self.frames.pop()
            
            # Push the result onto the caller's stack
            if self.frames:
                self.frames[-1].stack.append(result)
            
            return result
        
        # Closure instructions
        elif op == OpCode.CREATE_CLOSURE:
            func_name = instruction.operands[0]
            num_captured = instruction.operands[1]
            
            # Create a new closure
            closure = VMClosure(func_name, frame.module)
            
            # Push the closure onto the stack
            frame.stack.append(VMValue(VMValueType.CLOSURE, closure))
            
            return None
        
        elif op == OpCode.CAPTURE_VAR:
            var_idx = instruction.operands[0]
            
            # Get the value from the local variable
            value = frame.locals[var_idx]
            
            # Get the closure from the stack
            closure_val = frame.stack[-1]
            if closure_val.type != VMValueType.CLOSURE:
                self._throw_error("TypeError", "Expected closure")
                return None
            
            # Add the captured variable to the closure
            closure_val.value.captured_vars.append(value)
            
            return None
        
        elif op == OpCode.LOAD_CAPTURED:
            var_idx = instruction.operands[0]
            
            # Get the closure from the current frame
            if frame.closure is None:
                self._throw_error("RuntimeError", "No closure available")
                return None
            
            # Get the captured variable
            if var_idx >= len(frame.closure.captured_vars):
                self._throw_error("IndexError", f"Captured variable index out of range: {var_idx}")
                return None
            
            # Push the captured variable onto the stack
            frame.stack.append(frame.closure.captured_vars[var_idx])
            
            return None
        
        elif op == OpCode.STORE_CAPTURED:
            var_idx = instruction.operands[0]
            
            # Get the closure from the current frame
            if frame.closure is None:
                self._throw_error("RuntimeError", "No closure available")
                return None
            
            # Get the value to store
            value = frame.stack.pop()
            
            # Store the value in the captured variable
            if var_idx >= len(frame.closure.captured_vars):
                self._throw_error("IndexError", f"Captured variable index out of range: {var_idx}")
                return None
            
            frame.closure.captured_vars[var_idx] = value
            
            return None
        
        # Call instructions
        elif op == OpCode.CALL:
            func_name = instruction.operands[0]
            arg_count = instruction.operands[1]
            
            return self._call_function(func_name, arg_count, frame)
        
        # Module system instructions
        elif op == OpCode.IMPORT:
            # Get the module name
            module_name = frame.stack.pop()
            
            # Load the module
            module = self._load_module_by_name(module_name.value)
            
            # Push the module onto the stack
            frame.stack.append(module)
        
        elif op == OpCode.EXPORT:
            # Get the symbol name and value
            value = frame.stack.pop()
            name = frame.stack.pop()
            
            # Add to current module's exports
            current_module = frame.module
            current_module.exports[name.value] = value
            
            # Register the export
            current_module.add_export(name.value)
        
        elif op == OpCode.MODULE_GET:
            # Get the module and property name
            prop_name = frame.stack.pop()
            module = frame.stack.pop()
            
            # Ensure module is a module or namespace
            if module.type not in [VMValueType.MODULE, VMValueType.OBJECT]:
                self._throw_error("TypeError", f"Cannot get property {prop_name.value} of non-module")
                return None
            
            # Get the property
            if module.type == VMValueType.MODULE:
                if prop_name.value in module.value.exports:
                    value = module.value.exports[prop_name.value]
                else:
                    self._throw_error("ReferenceError", f"Module {module.value.name} has no export '{prop_name.value}'")
                    return None
            else:  # Object (namespace)
                if "exports" in module.value and prop_name.value in module.value["exports"].value:
                    value = module.value["exports"].value[prop_name.value]
                elif prop_name.value in module.value:
                    value = module.value[prop_name.value]
                else:
                    self._throw_error("ReferenceError", f"Object has no property '{prop_name.value}'")
                    return None
            
            # Push the value onto the stack
            frame.stack.append(value)
        
        elif op == OpCode.MODULE_SET:
            # Get the module, property name, and value
            value = frame.stack.pop()
            prop_name = frame.stack.pop()
            module = frame.stack.pop()
            
            # Ensure module is a module or namespace
            if module.type not in [VMValueType.MODULE, VMValueType.OBJECT]:
                self._throw_error("TypeError", f"Cannot set property {prop_name.value} of non-module")
                return None
            
            # Set the property
            if module.type == VMValueType.MODULE:
                module.value.exports[prop_name.value] = value
            else:  # Object (namespace)
                if "exports" in module.value:
                    module.value["exports"].value[prop_name.value] = value
                else:
                    module.value[prop_name.value] = value
            
            # Push the value onto the stack
            frame.stack.append(value)
        
        elif op == OpCode.NAMESPACE_CREATE:
            # Get the namespace name
            name = frame.stack.pop()
            
            # Create a new namespace
            namespace = {
                "name": name,
                "exports": VMValue(VMValueType.DICT, {})
            }
            
            # Register the namespace
            namespace_id = f"namespace:{name.value}"
            self.namespaces[namespace_id] = namespace
            
            # Push the namespace onto the stack
            frame.stack.append(VMValue(VMValueType.OBJECT, namespace))
        
        elif op == OpCode.MODULE_RESOLVE:
            # Get the module path
            path = frame.stack.pop()
            
            # Resolve the module path
            resolved_path = self._resolve_module_path(path.value)
            
            # Push the resolved path onto the stack
            frame.stack.append(VMValue(VMValueType.STRING, resolved_path))
        
        return None
    
    def _call_function(self, func_name: str, arg_count: int, frame: VMFrame) -> Optional[VMValue]:
        """
        Call a function.
        
        Args:
            func_name: The name of the function to call
            arg_count: The number of arguments
            frame: The current frame
            
        Returns:
            The result of the function call, or None to continue execution
        """
        # Check for native function
        if func_name in self.native_functions:
            # Pop arguments from the stack
            args = []
            for _ in range(arg_count):
                args.insert(0, frame.stack.pop())
            
            # Call the native function
            try:
                result = self.native_functions[func_name](self, *args)
                
                # Push the result onto the stack
                frame.stack.append(result)
                
                return None
            except Exception as e:
                self._throw_error("NativeFunctionError", str(e))
                return None
        
        # Check for bytecode function in the current module
        if func_name in frame.module.function_offsets:
            # Get the function offset
            func_offset = frame.module.function_offsets[func_name]
            
            # Pop arguments from the stack
            args = []
            for _ in range(arg_count):
                args.insert(0, frame.stack.pop())
            
            # Create a new frame for the function call
            new_frame = VMFrame(
                module=frame.module,
                locals=args,
                ip=func_offset
            )
            
            # Push the new frame
            self.frames.append(new_frame)
            
            # Continue execution in the new frame
            return None
        
        # Check for bytecode function in imported modules
        for module_name, module in self.modules.items():
            if func_name in module.function_offsets:
                # Get the function offset
                func_offset = module.function_offsets[func_name]
                
                # Pop arguments from the stack
                args = []
                for _ in range(arg_count):
                    args.insert(0, frame.stack.pop())
                
                # Create a new frame for the function call
                new_frame = VMFrame(
                    module=module,
                    locals=args,
                    ip=func_offset
                )
                
                # Push the new frame
                self.frames.append(new_frame)
                
                # Continue execution in the new frame
                return None
        
        # Function not found
        self._throw_error("UndefinedFunctionError", f"Function '{func_name}' is not defined")
        return None

    def _call_closure(self, closure: VMClosure, arg_count: int, frame: VMFrame) -> Optional[VMValue]:
        """
        Call a closure.
        
        Args:
            closure: The closure to call
            arg_count: The number of arguments
            frame: The current frame
            
        Returns:
            The result of the closure call, or None to continue execution
        """
        # Get the function offset
        if closure.name not in closure.module.function_offsets:
            self._throw_error("UndefinedFunctionError", f"Function '{closure.name}' is not defined")
            return None
        
        func_offset = closure.module.function_offsets[closure.name]
        
        # Pop arguments from the stack
        args = []
        for _ in range(arg_count):
            args.insert(0, frame.stack.pop())
        
        # Check if this is a tail call (call just before return)
        is_tail_call = (
            frame.ip < len(frame.module.instructions) and
            frame.module.instructions[frame.ip].opcode == OpCode.RET
        )
        
        if is_tail_call and len(self.frames) > 1:
            # Tail call optimization: reuse the current frame
            # Set the instruction pointer to the function offset
            frame.ip = func_offset
            
            # Replace the locals with the arguments
            frame.locals = args
            
            # Set the closure
            frame.closure = closure
            
            # Continue execution in the current frame
            return None
        else:
            # Create a new frame for the function call
            new_frame = VMFrame(
                module=closure.module,
                locals=args,
                ip=func_offset,
                closure=closure
            )
            
            # Push the new frame
            self.frames.append(new_frame)
            
            # Continue execution in the new frame
            return None
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """
        Get performance metrics for the last execution.
        
        Returns:
            A dictionary of performance metrics
        """
        elapsed_time = self.end_time - self.start_time
        instructions_per_second = self.instruction_count / elapsed_time if elapsed_time > 0 else 0
        
        return {
            "instruction_count": self.instruction_count,
            "elapsed_time": elapsed_time,
            "instructions_per_second": instructions_per_second,
        }
    
    def reset_metrics(self) -> None:
        """Reset performance metrics."""
        self.instruction_count = 0
        self.call_count = 0
        self.start_time = 0
        self.end_time = 0
    
    def _load_module_by_name(self, module_name: str) -> VMValue:
        """
        Load a module by name.
        
        Args:
            module_name: The name of the module to load
            
        Returns:
            A VM value representing the loaded module
        """
        # Check if module is already loaded
        if module_name in self.module_cache:
            return self.module_cache[module_name]
        
        # Try to resolve the module path
        module_path = self._resolve_module_path(module_name)
        
        if not module_path:
            self._throw_error("ImportError", f"Module '{module_name}' not found")
            return VMValue(VMValueType.NULL, None)
        
        # Try to load the module
        try:
            # Check if it's a native module
            if module_name.startswith("runa."):
                return self._load_native_module(module_name)
            
            # Load from file
            with open(module_path, "r") as f:
                source = f.read()
            
            # Compile the module
            compiler = Compiler()
            result = compiler.compile_string(source, filename=module_path)
            
            if not result.success:
                self._throw_error("ImportError", f"Failed to compile module: {module_name}")
                return VMValue(VMValueType.NULL, None)
            
            # Set the module name
            result.module.name = module_name
            
            # Load the module
            self.load_module(result.module)
            
            # Execute the module to initialize it
            self.execute_module(module_name)
            
            # Get the module object
            module_obj = VMValue(VMValueType.MODULE, result.module)
            
            # Cache the module
            self.module_cache[module_name] = module_obj
            
            return module_obj
        
        except Exception as e:
            self._throw_error("ImportError", f"Error loading module '{module_name}': {str(e)}")
            return VMValue(VMValueType.NULL, None)
    
    def _resolve_module_path(self, module_name: str) -> str:
        """
        Resolve a module name to a file path.
        
        Args:
            module_name: The name of the module to resolve
            
        Returns:
            The resolved file path, or empty string if not found
        """
        # Check if it's a native module
        if module_name.startswith("runa."):
            return module_name
        
        # Replace dots with path separators
        relative_path = module_name.replace(".", os.sep)
        
        # Try each search path
        for search_path in self.module_search_paths:
            # Try with .runa extension
            full_path = os.path.join(search_path, relative_path + ".runa")
            if os.path.isfile(full_path):
                return full_path
            
            # Try with .py extension
            full_path = os.path.join(search_path, relative_path + ".py")
            if os.path.isfile(full_path):
                return full_path
            
            # Try as a directory with __init__.runa
            full_path = os.path.join(search_path, relative_path, "__init__.runa")
            if os.path.isfile(full_path):
                return full_path
            
            # Try as a directory with __init__.py
            full_path = os.path.join(search_path, relative_path, "__init__.py")
            if os.path.isfile(full_path):
                return full_path
        
        # Module not found
        return ""
    
    def _load_native_module(self, module_name: str) -> VMValue:
        """
        Load a native module.
        
        Args:
            module_name: The name of the native module to load
            
        Returns:
            A VM value representing the loaded module
        """
        # Check if the module is already loaded
        if module_name in self.module_cache:
            return self.module_cache[module_name]
        
        # Get the module components
        module_parts = module_name.split(".")
        
        # Special handling for standard library modules
        if module_parts[0] == "runa" and len(module_parts) > 1:
            # Create the module object
            module_obj = {
                "name": VMValue(VMValueType.STRING, module_name),
                "exports": VMValue(VMValueType.DICT, {})
            }
            
            # Add module exports based on the module name
            if module_parts[1] == "core":
                # Core module exports
                module_obj["exports"].value.update({
                    "print": VMValue(VMValueType.NATIVE_FUNCTION, self._native_print),
                    "input": VMValue(VMValueType.NATIVE_FUNCTION, self._native_input),
                    "len": VMValue(VMValueType.NATIVE_FUNCTION, self._native_len),
                    "type": VMValue(VMValueType.NATIVE_FUNCTION, self._native_type),
                })
                
                # Add module system functions if it's the module module
                if len(module_parts) > 2 and module_parts[2] == "module":
                    module_obj["exports"].value.update({
                        "load_module": VMValue(VMValueType.NATIVE_FUNCTION, lambda path: self._load_module_by_name(path.value)),
                        "resolve_path": VMValue(VMValueType.NATIVE_FUNCTION, lambda path: VMValue(VMValueType.STRING, self._resolve_module_path(path.value))),
                        "create_namespace": VMValue(VMValueType.NATIVE_FUNCTION, self._native_create_namespace),
                    })
            
            # Create the module value
            module_value = VMValue(VMValueType.OBJECT, module_obj)
            
            # Cache the module
            self.module_cache[module_name] = module_value
            
            return module_value
        
        # Unknown native module
        self._throw_error("ImportError", f"Unknown native module: {module_name}")
        return VMValue(VMValueType.NULL, None)
    
    def _native_create_namespace(self, name: VMValue) -> VMValue:
        """
        Create a new namespace.
        
        Args:
            name: The name of the namespace
            
        Returns:
            A VM value representing the namespace
        """
        if name.type != VMValueType.STRING:
            self._throw_error("TypeError", "Namespace name must be a string")
            return VMValue(VMValueType.NULL, None)
        
        # Create a new namespace
        namespace = {
            "name": name,
            "exports": VMValue(VMValueType.DICT, {})
        }
        
        # Register the namespace
        namespace_id = f"namespace:{name.value}"
        self.namespaces[namespace_id] = namespace
        
        # Return the namespace
        return VMValue(VMValueType.OBJECT, namespace) 