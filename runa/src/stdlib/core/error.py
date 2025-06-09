"""
Error handling module for Runa Standard Library.

This module provides error types, stack trace generation, and error handling functions
for the Runa programming language.
"""

from typing import Dict, List, Any, Optional
import traceback
import sys

from runa.src.vm.vm import VirtualMachine, VMValue, VMValueType


# Error type definitions
ERROR_TYPES = {
    "Error": {
        "description": "Base error type for all errors",
        "properties": ["message", "stack_trace"]
    },
    "TypeError": {
        "description": "Error thrown when a value is not of the expected type",
        "properties": ["message", "stack_trace", "expected_type", "actual_type"]
    },
    "ValueError": {
        "description": "Error thrown when a value is not valid",
        "properties": ["message", "stack_trace", "invalid_value"]
    },
    "ReferenceError": {
        "description": "Error thrown when an invalid reference is used",
        "properties": ["message", "stack_trace", "reference_name"]
    },
    "SyntaxError": {
        "description": "Error thrown when there is a syntax error in the code",
        "properties": ["message", "stack_trace", "source", "line", "column"]
    },
    "RangeError": {
        "description": "Error thrown when a value is outside the valid range",
        "properties": ["message", "stack_trace", "value", "min", "max"]
    },
    "IOError": {
        "description": "Error thrown when an I/O operation fails",
        "properties": ["message", "stack_trace", "operation", "path"]
    },
    "ImportError": {
        "description": "Error thrown when a module cannot be imported",
        "properties": ["message", "stack_trace", "module_name"]
    },
    "AssertionError": {
        "description": "Error thrown when an assertion fails",
        "properties": ["message", "stack_trace", "expression"]
    },
    "NotImplementedError": {
        "description": "Error thrown when a feature is not implemented",
        "properties": ["message", "stack_trace", "feature"]
    }
}


def _create_error(vm: VirtualMachine, error_type: str, message: VMValue, **kwargs) -> VMValue:
    """
    Create a new error object.
    
    Args:
        vm: The virtual machine
        error_type: The type of error to create
        message: The error message
        **kwargs: Additional error properties
        
    Returns:
        A VM value representing the error object
    """
    if message.type != VMValueType.STRING:
        message = VMValue(VMValueType.STRING, str(message))
    
    # Get stack trace from VM frames
    stack_trace = []
    for i, frame in enumerate(vm.frames):
        if i == 0:  # Skip the current frame
            continue
        
        module_name = frame.module.name or "<unnamed>"
        location = ""
        
        # Get source location if available
        if frame.module.source_map and frame.ip in frame.module.source_map:
            loc = frame.module.source_map[frame.ip]
            location = f"{loc.file}:{loc.line}:{loc.column}"
        
        # Get function name if available
        function_name = "<unknown>"
        for fname, (start, end) in frame.module.functions.items():
            if start <= frame.ip <= end:
                function_name = fname
                break
        
        stack_trace.append({
            "module": module_name,
            "function": function_name,
            "location": location
        })
    
    # Create error properties
    properties = {
        "message": message,
        "stack_trace": VMValue(VMValueType.LIST, [
            VMValue(VMValueType.OBJECT, {
                "module": VMValue(VMValueType.STRING, frame["module"]),
                "function": VMValue(VMValueType.STRING, frame["function"]),
                "location": VMValue(VMValueType.STRING, frame["location"])
            })
            for frame in stack_trace
        ])
    }
    
    # Add additional properties
    for key, value in kwargs.items():
        if key in ERROR_TYPES.get(error_type, {}).get("properties", []):
            properties[key] = value
    
    # Create the error object
    return VMValue(VMValueType.OBJECT, {
        "type": VMValue(VMValueType.STRING, error_type),
        "properties": properties
    })


def _error_to_string(vm: VirtualMachine, error: VMValue) -> VMValue:
    """
    Convert an error object to a string representation.
    
    Args:
        vm: The virtual machine
        error: The error object
        
    Returns:
        A string VM value with the error string representation
    """
    if error.type != VMValueType.OBJECT:
        return VMValue(VMValueType.STRING, str(error))
    
    error_type = error.value.get("type", VMValue(VMValueType.STRING, "Error"))
    if error_type.type != VMValueType.STRING:
        error_type = VMValue(VMValueType.STRING, "Error")
    
    props = error.value.get("properties", {})
    message = props.get("message", VMValue(VMValueType.STRING, "Unknown error"))
    if message.type != VMValueType.STRING:
        message = VMValue(VMValueType.STRING, str(message))
    
    stack_trace = props.get("stack_trace", VMValue(VMValueType.LIST, []))
    if stack_trace.type != VMValueType.LIST:
        stack_trace = VMValue(VMValueType.LIST, [])
    
    result = f"{error_type.value}: {message.value}\n"
    
    for i, frame in enumerate(stack_trace.value):
        if frame.type != VMValueType.OBJECT:
            continue
        
        frame_props = frame.value
        module = frame_props.get("module", VMValue(VMValueType.STRING, "<unknown>"))
        function = frame_props.get("function", VMValue(VMValueType.STRING, "<unknown>"))
        location = frame_props.get("location", VMValue(VMValueType.STRING, ""))
        
        result += f"  at {function.value} ({module.value}"
        if location.value:
            result += f" - {location.value}"
        result += ")\n"
    
    return VMValue(VMValueType.STRING, result)


def _format_stack_trace(vm: VirtualMachine, error: VMValue) -> VMValue:
    """
    Format the stack trace of an error object.
    
    Args:
        vm: The virtual machine
        error: The error object
        
    Returns:
        A string VM value with the formatted stack trace
    """
    if error.type != VMValueType.OBJECT:
        return VMValue(VMValueType.STRING, "")
    
    props = error.value.get("properties", {})
    stack_trace = props.get("stack_trace", VMValue(VMValueType.LIST, []))
    if stack_trace.type != VMValueType.LIST:
        return VMValue(VMValueType.STRING, "")
    
    result = "Stack trace:\n"
    
    for i, frame in enumerate(stack_trace.value):
        if frame.type != VMValueType.OBJECT:
            continue
        
        frame_props = frame.value
        module = frame_props.get("module", VMValue(VMValueType.STRING, "<unknown>"))
        function = frame_props.get("function", VMValue(VMValueType.STRING, "<unknown>"))
        location = frame_props.get("location", VMValue(VMValueType.STRING, ""))
        
        result += f"  {i}: {function.value} ({module.value}"
        if location.value:
            result += f" - {location.value}"
        result += ")\n"
    
    return VMValue(VMValueType.STRING, result)


def _throw(vm: VirtualMachine, error: VMValue) -> VMValue:
    """
    Throw an error.
    
    Args:
        vm: The virtual machine
        error: The error to throw
        
    Returns:
        A null VM value (never returned since an error is thrown)
    """
    # Store the error in a special VM register for the try-catch system
    vm.current_error = error
    
    # If there are no try handlers, print the error and exit
    if not vm.frames or not vm.frames[-1].try_handlers:
        error_str = _error_to_string(vm, error).value
        print(f"Unhandled error: {error_str}", file=sys.stderr)
        return VMValue(VMValueType.NULL, None)
    
    # Signal that an error has been thrown
    vm.error_thrown = True
    
    # This return value is never used since the VM will jump to the catch block
    return VMValue(VMValueType.NULL, None)


def _assert(vm: VirtualMachine, condition: VMValue, message: Optional[VMValue] = None) -> VMValue:
    """
    Assert that a condition is true, throw an AssertionError if it's not.
    
    Args:
        vm: The virtual machine
        condition: The condition to check
        message: Optional error message
        
    Returns:
        A boolean VM value indicating the result of the assertion
    """
    if not condition.is_truthy():
        if message is None or message.type != VMValueType.STRING:
            message = VMValue(VMValueType.STRING, "Assertion failed")
        
        error = _create_error(vm, "AssertionError", message, 
                              expression=VMValue(VMValueType.STRING, str(condition)))
        _throw(vm, error)
        return VMValue(VMValueType.BOOLEAN, False)
    
    return VMValue(VMValueType.BOOLEAN, True)


def register_error_functions(vm: VirtualMachine) -> None:
    """
    Register error handling functions with the VM.
    
    Args:
        vm: The virtual machine to register the functions with
    """
    # Register error creation functions
    vm.native_functions["create_error"] = lambda *args: _create_error(vm, "Error", *args)
    vm.native_functions["create_type_error"] = lambda *args: _create_error(vm, "TypeError", *args)
    vm.native_functions["create_value_error"] = lambda *args: _create_error(vm, "ValueError", *args)
    vm.native_functions["create_reference_error"] = lambda *args: _create_error(vm, "ReferenceError", *args)
    vm.native_functions["create_syntax_error"] = lambda *args: _create_error(vm, "SyntaxError", *args)
    vm.native_functions["create_range_error"] = lambda *args: _create_error(vm, "RangeError", *args)
    vm.native_functions["create_io_error"] = lambda *args: _create_error(vm, "IOError", *args)
    vm.native_functions["create_import_error"] = lambda *args: _create_error(vm, "ImportError", *args)
    vm.native_functions["create_assertion_error"] = lambda *args: _create_error(vm, "AssertionError", *args)
    vm.native_functions["create_not_implemented_error"] = lambda *args: _create_error(vm, "NotImplementedError", *args)
    
    # Register error utility functions
    vm.native_functions["error_to_string"] = lambda error: _error_to_string(vm, error)
    vm.native_functions["format_stack_trace"] = lambda error: _format_stack_trace(vm, error)
    vm.native_functions["throw"] = lambda error: _throw(vm, error)
    vm.native_functions["assert"] = lambda *args: _assert(vm, *args) 