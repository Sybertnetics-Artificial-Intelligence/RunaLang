"""
Module system implementation for Runa Standard Library.

This module provides functions for module loading, importing, exporting,
and namespace management.
"""

import os
import sys
from typing import Dict, List, Any, Optional

from runa.src.vm.vm import VirtualMachine, VMValue, VMValueType
from runa.src.compiler import Compiler


# Registry of loaded modules
_loaded_modules = {}


def _compile_and_load_module(vm: VirtualMachine, source: VMValue, module_path: VMValue) -> VMValue:
    """
    Compile and load a module from source.
    
    Args:
        vm: The virtual machine
        source: The source code as a string
        module_path: The module path
        
    Returns:
        A VM value representing the loaded module
    """
    if source.type != VMValueType.STRING or module_path.type != VMValueType.STRING:
        return VMValue(VMValueType.NULL, None)
    
    try:
        # Compile the module
        compiler = Compiler()
        result = compiler.compile_string(source.value)
        
        if not result.success:
            print(f"Failed to compile module: {module_path.value}", file=sys.stderr)
            return VMValue(VMValueType.NULL, None)
        
        # Set the module name
        result.module.name = os.path.basename(module_path.value)
        
        # Load the module
        vm.load_module(result.module)
        
        # Create module object with exports
        module_obj = {
            "name": VMValue(VMValueType.STRING, result.module.name),
            "path": VMValue(VMValueType.STRING, module_path.value),
            "exports": VMValue(VMValueType.DICT, {})
        }
        
        # Store in loaded modules registry
        _loaded_modules[module_path.value] = module_obj
        
        return VMValue(VMValueType.OBJECT, module_obj)
    
    except Exception as e:
        print(f"Error loading module {module_path.value}: {str(e)}", file=sys.stderr)
        return VMValue(VMValueType.NULL, None)


def _get_current_module(vm: VirtualMachine) -> VMValue:
    """
    Get the current module object.
    
    Args:
        vm: The virtual machine
        
    Returns:
        A VM value representing the current module
    """
    if not vm.frames:
        return VMValue(VMValueType.NULL, None)
    
    current_frame = vm.frames[-1]
    module_name = current_frame.module.name or "<unnamed>"
    
    # Find the module in the registry
    for path, module in _loaded_modules.items():
        if module["name"].value == module_name:
            return VMValue(VMValueType.OBJECT, module)
    
    # If not found, create a new module object
    module_obj = {
        "name": VMValue(VMValueType.STRING, module_name),
        "path": VMValue(VMValueType.STRING, "<unknown>"),
        "exports": VMValue(VMValueType.DICT, {})
    }
    
    # Store in loaded modules registry with a generated key
    _loaded_modules[f"<dynamic>/{module_name}"] = module_obj
    
    return VMValue(VMValueType.OBJECT, module_obj)


def register_module_functions(vm: VirtualMachine) -> None:
    """
    Register module system functions with the VM.
    
    Args:
        vm: The virtual machine to register the functions with
    """
    vm.native_functions["compile_and_load_module"] = lambda source, path: _compile_and_load_module(vm, source, path)
    vm.native_functions["get_current_module"] = lambda: _get_current_module(vm) 