"""
Built-in functions for the Runa Core module.

This module defines essential built-in functions that are available in every
Runa program without requiring explicit imports.
"""

from typing import Dict, Callable, Any, List, Optional, Union, Set, Tuple
from ...vm.vm import VirtualMachine, VMValue, VMValueType


def register_core_builtins(vm: VirtualMachine) -> None:
    """
    Register all core built-in functions with the VM.
    
    Args:
        vm: The virtual machine to register the functions with
    """
    # Basic type operations
    vm.native_functions["type"] = _type
    vm.native_functions["is_type"] = _is_type
    vm.native_functions["cast"] = _cast
    
    # Conversion functions
    vm.native_functions["to_string"] = _to_string
    vm.native_functions["to_int"] = _to_int
    vm.native_functions["to_float"] = _to_float
    vm.native_functions["to_bool"] = _to_bool
    vm.native_functions["to_list"] = _to_list
    vm.native_functions["to_dict"] = _to_dict
    
    # Collection operations
    vm.native_functions["len"] = _len
    vm.native_functions["range"] = _range
    vm.native_functions["enumerate"] = _enumerate
    vm.native_functions["zip"] = _zip
    
    # String operations
    vm.native_functions["format"] = _format
    vm.native_functions["join"] = _join
    vm.native_functions["split"] = _split
    
    # Object operations
    vm.native_functions["has_attr"] = _has_attr
    vm.native_functions["get_attr"] = _get_attr
    vm.native_functions["set_attr"] = _set_attr
    
    # System operations
    vm.native_functions["print"] = _print
    vm.native_functions["input"] = _input
    vm.native_functions["gc_collect"] = _gc_collect
    vm.native_functions["exit"] = _exit


def _type(vm: VirtualMachine, value: VMValue) -> VMValue:
    """
    Get the type of a value.
    
    Args:
        vm: The virtual machine
        value: The value to get the type of
        
    Returns:
        A string VM value with the type name
    """
    type_name = value.type.name.lower()
    return VMValue(VMValueType.STRING, type_name)


def _is_type(vm: VirtualMachine, value: VMValue, type_name: VMValue) -> VMValue:
    """
    Check if a value is of a specific type.
    
    Args:
        vm: The virtual machine
        value: The value to check
        type_name: The type name to check against
        
    Returns:
        A boolean VM value
    """
    if type_name.type != VMValueType.STRING:
        return VMValue(VMValueType.BOOLEAN, False)
    
    target_type_name = type_name.value.upper()
    try:
        target_type = VMValueType[target_type_name]
        return VMValue(VMValueType.BOOLEAN, value.type == target_type)
    except KeyError:
        return VMValue(VMValueType.BOOLEAN, False)


def _cast(vm: VirtualMachine, value: VMValue, type_name: VMValue) -> VMValue:
    """
    Cast a value to a specific type.
    
    Args:
        vm: The virtual machine
        value: The value to cast
        type_name: The type name to cast to
        
    Returns:
        The cast value or null if the cast failed
    """
    if type_name.type != VMValueType.STRING:
        return VMValue(VMValueType.NULL, None)
    
    target_type_name = type_name.value.upper()
    try:
        target_type = VMValueType[target_type_name]
    except KeyError:
        return VMValue(VMValueType.NULL, None)
    
    # Perform the cast based on target type
    if target_type == VMValueType.STRING:
        return _to_string(vm, value)
    elif target_type == VMValueType.INTEGER:
        return _to_int(vm, value)
    elif target_type == VMValueType.FLOAT:
        return _to_float(vm, value)
    elif target_type == VMValueType.BOOLEAN:
        return _to_bool(vm, value)
    elif target_type == VMValueType.LIST:
        return _to_list(vm, value)
    elif target_type == VMValueType.DICT:
        return _to_dict(vm, value)
    
    # Default case - can't cast
    return VMValue(VMValueType.NULL, None)


def _to_string(vm: VirtualMachine, value: VMValue) -> VMValue:
    """
    Convert a value to a string.
    
    Args:
        vm: The virtual machine
        value: The value to convert
        
    Returns:
        A string VM value
    """
    return VMValue(VMValueType.STRING, str(value.value))


def _to_int(vm: VirtualMachine, value: VMValue) -> VMValue:
    """
    Convert a value to an integer.
    
    Args:
        vm: The virtual machine
        value: The value to convert
        
    Returns:
        An integer VM value or null if the conversion failed
    """
    try:
        if value.type == VMValueType.STRING:
            return VMValue(VMValueType.INTEGER, int(value.value))
        elif value.type == VMValueType.FLOAT:
            return VMValue(VMValueType.INTEGER, int(value.value))
        elif value.type == VMValueType.BOOLEAN:
            return VMValue(VMValueType.INTEGER, 1 if value.value else 0)
        elif value.type == VMValueType.INTEGER:
            return value
        else:
            return VMValue(VMValueType.NULL, None)
    except ValueError:
        return VMValue(VMValueType.NULL, None)


def _to_float(vm: VirtualMachine, value: VMValue) -> VMValue:
    """
    Convert a value to a float.
    
    Args:
        vm: The virtual machine
        value: The value to convert
        
    Returns:
        A float VM value or null if the conversion failed
    """
    try:
        if value.type == VMValueType.STRING:
            return VMValue(VMValueType.FLOAT, float(value.value))
        elif value.type == VMValueType.INTEGER:
            return VMValue(VMValueType.FLOAT, float(value.value))
        elif value.type == VMValueType.BOOLEAN:
            return VMValue(VMValueType.FLOAT, 1.0 if value.value else 0.0)
        elif value.type == VMValueType.FLOAT:
            return value
        else:
            return VMValue(VMValueType.NULL, None)
    except ValueError:
        return VMValue(VMValueType.NULL, None)


def _to_bool(vm: VirtualMachine, value: VMValue) -> VMValue:
    """
    Convert a value to a boolean.
    
    Args:
        vm: The virtual machine
        value: The value to convert
        
    Returns:
        A boolean VM value
    """
    if value.type == VMValueType.NULL:
        return VMValue(VMValueType.BOOLEAN, False)
    elif value.type == VMValueType.BOOLEAN:
        return value
    elif value.type == VMValueType.INTEGER:
        return VMValue(VMValueType.BOOLEAN, bool(value.value))
    elif value.type == VMValueType.FLOAT:
        return VMValue(VMValueType.BOOLEAN, bool(value.value))
    elif value.type == VMValueType.STRING:
        return VMValue(VMValueType.BOOLEAN, bool(value.value))
    elif value.type == VMValueType.LIST:
        return VMValue(VMValueType.BOOLEAN, bool(value.value))
    elif value.type == VMValueType.DICT:
        return VMValue(VMValueType.BOOLEAN, bool(value.value))
    else:
        return VMValue(VMValueType.BOOLEAN, True)


def _to_list(vm: VirtualMachine, value: VMValue) -> VMValue:
    """
    Convert a value to a list.
    
    Args:
        vm: The virtual machine
        value: The value to convert
        
    Returns:
        A list VM value or null if the conversion failed
    """
    if value.type == VMValueType.LIST:
        return value
    elif value.type == VMValueType.STRING:
        # Convert string to list of characters
        return VMValue(VMValueType.LIST, [
            VMValue(VMValueType.STRING, c) for c in value.value
        ])
    elif value.type == VMValueType.DICT:
        # Convert dictionary to list of keys
        return VMValue(VMValueType.LIST, [
            k for k, _ in value.value.items()
        ])
    elif value.type == VMValueType.NULL:
        return VMValue(VMValueType.LIST, [])
    else:
        # Single item list
        return VMValue(VMValueType.LIST, [value])


def _to_dict(vm: VirtualMachine, value: VMValue) -> VMValue:
    """
    Convert a value to a dictionary.
    
    Args:
        vm: The virtual machine
        value: The value to convert
        
    Returns:
        A dictionary VM value or null if the conversion failed
    """
    if value.type == VMValueType.DICT:
        return value
    elif value.type == VMValueType.LIST:
        # Convert list to dict with indices as keys
        result = {}
        for i, item in enumerate(value.value):
            result[VMValue(VMValueType.INTEGER, i)] = item
        return VMValue(VMValueType.DICT, result)
    elif value.type == VMValueType.NULL:
        return VMValue(VMValueType.DICT, {})
    else:
        return VMValue(VMValueType.NULL, None)


def _len(vm: VirtualMachine, value: VMValue) -> VMValue:
    """
    Get the length of a value.
    
    Args:
        vm: The virtual machine
        value: The value to get the length of
        
    Returns:
        An integer VM value with the length
    """
    if value.type == VMValueType.STRING:
        return VMValue(VMValueType.INTEGER, len(value.value))
    elif value.type == VMValueType.LIST:
        return VMValue(VMValueType.INTEGER, len(value.value))
    elif value.type == VMValueType.DICT:
        return VMValue(VMValueType.INTEGER, len(value.value))
    else:
        return VMValue(VMValueType.INTEGER, 0)


def _range(vm: VirtualMachine, *args) -> VMValue:
    """
    Create a range of integers.
    
    Args:
        vm: The virtual machine
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
    return VMValue(VMValueType.LIST, [
        VMValue(VMValueType.INTEGER, i) for i in range_list
    ])


def _enumerate(vm: VirtualMachine, iterable: VMValue) -> VMValue:
    """
    Enumerate the items in an iterable.
    
    Args:
        vm: The virtual machine
        iterable: The iterable to enumerate
        
    Returns:
        A list of (index, value) tuples
    """
    result = []
    
    if iterable.type == VMValueType.LIST:
        for i, item in enumerate(iterable.value):
            pair = [VMValue(VMValueType.INTEGER, i), item]
            result.append(VMValue(VMValueType.LIST, pair))
    elif iterable.type == VMValueType.STRING:
        for i, char in enumerate(iterable.value):
            pair = [
                VMValue(VMValueType.INTEGER, i),
                VMValue(VMValueType.STRING, char)
            ]
            result.append(VMValue(VMValueType.LIST, pair))
    elif iterable.type == VMValueType.DICT:
        for i, (key, value) in enumerate(iterable.value.items()):
            pair = [VMValue(VMValueType.INTEGER, i), key]
            result.append(VMValue(VMValueType.LIST, pair))
    
    return VMValue(VMValueType.LIST, result)


def _zip(vm: VirtualMachine, *iterables) -> VMValue:
    """
    Zip multiple iterables together.
    
    Args:
        vm: The virtual machine
        *iterables: The iterables to zip
        
    Returns:
        A list of tuples containing elements from each iterable
    """
    result = []
    
    # Convert all iterables to lists
    lists = []
    for it in iterables:
        if it.type == VMValueType.LIST:
            lists.append(it.value)
        elif it.type == VMValueType.STRING:
            lists.append([VMValue(VMValueType.STRING, c) for c in it.value])
        else:
            lists.append([])
    
    # Find the minimum length
    min_len = min(len(lst) for lst in lists) if lists else 0
    
    # Create the zipped result
    for i in range(min_len):
        tuple_items = [lst[i] for lst in lists]
        result.append(VMValue(VMValueType.LIST, tuple_items))
    
    return VMValue(VMValueType.LIST, result)


def _format(vm: VirtualMachine, template: VMValue, *args, **kwargs) -> VMValue:
    """
    Format a string template with values.
    
    Args:
        vm: The virtual machine
        template: The string template
        *args: Positional arguments for formatting
        **kwargs: Keyword arguments for formatting
        
    Returns:
        A formatted string
    """
    if template.type != VMValueType.STRING:
        return VMValue(VMValueType.STRING, "")
    
    # Convert args to Python values
    py_args = [arg.value for arg in args]
    
    # Extract kwargs from the last argument if it's a dictionary
    py_kwargs = {}
    if args and args[-1].type == VMValueType.DICT:
        kwargs_dict = args[-1].value
        py_kwargs = {
            k.value: v.value 
            for k, v in kwargs_dict.items() 
            if k.type == VMValueType.STRING
        }
        py_args = py_args[:-1]
    
    try:
        result = template.value.format(*py_args, **py_kwargs)
        return VMValue(VMValueType.STRING, result)
    except Exception as e:
        return VMValue(VMValueType.STRING, str(e))


def _join(vm: VirtualMachine, separator: VMValue, iterable: VMValue) -> VMValue:
    """
    Join an iterable with a separator.
    
    Args:
        vm: The virtual machine
        separator: The separator string
        iterable: The iterable to join
        
    Returns:
        A joined string
    """
    if separator.type != VMValueType.STRING:
        sep = ""
    else:
        sep = separator.value
    
    strings = []
    if iterable.type == VMValueType.LIST:
        for item in iterable.value:
            strings.append(str(item.value))
    elif iterable.type == VMValueType.STRING:
        return iterable  # No need to join a string
    elif iterable.type == VMValueType.DICT:
        for key in iterable.value:
            strings.append(str(key.value))
    
    return VMValue(VMValueType.STRING, sep.join(strings))


def _split(vm: VirtualMachine, string: VMValue, separator: VMValue) -> VMValue:
    """
    Split a string by a separator.
    
    Args:
        vm: The virtual machine
        string: The string to split
        separator: The separator string
        
    Returns:
        A list of substrings
    """
    if string.type != VMValueType.STRING:
        return VMValue(VMValueType.LIST, [])
    
    if separator.type != VMValueType.STRING:
        sep = " "
    else:
        sep = separator.value
    
    parts = string.value.split(sep)
    return VMValue(VMValueType.LIST, [
        VMValue(VMValueType.STRING, part) for part in parts
    ])


def _has_attr(vm: VirtualMachine, obj: VMValue, attr_name: VMValue) -> VMValue:
    """
    Check if an object has an attribute.
    
    Args:
        vm: The virtual machine
        obj: The object to check
        attr_name: The attribute name
        
    Returns:
        A boolean VM value
    """
    if obj.type != VMValueType.OBJECT or attr_name.type != VMValueType.STRING:
        return VMValue(VMValueType.BOOLEAN, False)
    
    return VMValue(VMValueType.BOOLEAN, attr_name.value in obj.value)


def _get_attr(vm: VirtualMachine, obj: VMValue, attr_name: VMValue) -> VMValue:
    """
    Get an attribute from an object.
    
    Args:
        vm: The virtual machine
        obj: The object to get the attribute from
        attr_name: The attribute name
        
    Returns:
        The attribute value or null if not found
    """
    if obj.type != VMValueType.OBJECT or attr_name.type != VMValueType.STRING:
        return VMValue(VMValueType.NULL, None)
    
    if attr_name.value not in obj.value:
        return VMValue(VMValueType.NULL, None)
    
    return obj.value[attr_name.value]


def _set_attr(vm: VirtualMachine, obj: VMValue, attr_name: VMValue, value: VMValue) -> VMValue:
    """
    Set an attribute on an object.
    
    Args:
        vm: The virtual machine
        obj: The object to set the attribute on
        attr_name: The attribute name
        value: The value to set
        
    Returns:
        The value that was set
    """
    if obj.type != VMValueType.OBJECT or attr_name.type != VMValueType.STRING:
        return VMValue(VMValueType.NULL, None)
    
    obj.value[attr_name.value] = value
    return value


def _print(vm: VirtualMachine, *args) -> VMValue:
    """
    Print values to the console.
    
    Args:
        vm: The virtual machine
        *args: The values to print
        
    Returns:
        A null VM value
    """
    print(*[str(arg.value) for arg in args])
    return VMValue(VMValueType.NULL, None)


def _input(vm: VirtualMachine, prompt: VMValue = None) -> VMValue:
    """
    Get input from the console.
    
    Args:
        vm: The virtual machine
        prompt: Optional prompt to display
        
    Returns:
        A string VM value with the input
    """
    if prompt and prompt.type == VMValueType.STRING:
        result = input(prompt.value)
    else:
        result = input()
    
    return VMValue(VMValueType.STRING, result)


def _gc_collect(vm: VirtualMachine) -> VMValue:
    """
    Force garbage collection.
    
    Args:
        vm: The virtual machine
        
    Returns:
        An integer VM value with the number of objects collected
    """
    import gc
    count = gc.collect()
    return VMValue(VMValueType.INTEGER, count)


def _exit(vm: VirtualMachine, code: VMValue = None) -> VMValue:
    """
    Exit the program.
    
    Args:
        vm: The virtual machine
        code: Optional exit code
        
    Returns:
        Never returns - exits the program
    """
    if code and code.type == VMValueType.INTEGER:
        exit_code = code.value
    else:
        exit_code = 0
    
    import sys
    sys.exit(exit_code) 