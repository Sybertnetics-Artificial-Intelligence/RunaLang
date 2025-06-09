"""
File operations for Runa programming language.

This module provides functions for working with files and the filesystem.
"""

import os
import sys
import json
from typing import Dict, List, Any, Optional
from ...vm.vm import VirtualMachine, VMValue, VMValueType


def register_file_functions(vm: VirtualMachine) -> None:
    """
    Register file operation functions with the VM.
    
    Args:
        vm: The virtual machine to register the functions with
    """
    vm.native_functions["file_read"] = _file_read
    vm.native_functions["file_write"] = _file_write
    vm.native_functions["file_append"] = _file_append
    vm.native_functions["file_exists"] = _file_exists
    vm.native_functions["file_delete"] = _file_delete
    vm.native_functions["file_copy"] = _file_copy
    vm.native_functions["file_move"] = _file_move
    vm.native_functions["file_size"] = _file_size
    vm.native_functions["list_dir"] = _list_dir
    vm.native_functions["make_dir"] = _make_dir
    vm.native_functions["remove_dir"] = _remove_dir
    vm.native_functions["get_cwd"] = _get_cwd
    vm.native_functions["change_dir"] = _change_dir
    vm.native_functions["path_join"] = _path_join
    vm.native_functions["path_split"] = _path_split
    vm.native_functions["path_basename"] = _path_basename
    vm.native_functions["path_dirname"] = _path_dirname
    vm.native_functions["path_extension"] = _path_extension
    vm.native_functions["path_absolute"] = _path_absolute
    vm.native_functions["json_parse"] = _json_parse
    vm.native_functions["json_stringify"] = _json_stringify


def _file_read(vm: VirtualMachine, filepath: VMValue) -> VMValue:
    """
    Read a file and return its contents as a string.
    
    Args:
        vm: The virtual machine
        filepath: The path to the file
        
    Returns:
        A string VM value with the file contents
    """
    if filepath.type != VMValueType.STRING:
        return VMValue(VMValueType.NULL, None)
    
    try:
        with open(filepath.value, 'r', encoding='utf-8') as f:
            content = f.read()
        return VMValue(VMValueType.STRING, content)
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        return VMValue(VMValueType.NULL, None)


def _file_write(vm: VirtualMachine, filepath: VMValue, content: VMValue) -> VMValue:
    """
    Write content to a file, overwriting any existing content.
    
    Args:
        vm: The virtual machine
        filepath: The path to the file
        content: The content to write
        
    Returns:
        A boolean VM value indicating success
    """
    if filepath.type != VMValueType.STRING:
        return VMValue(VMValueType.BOOLEAN, False)
    
    try:
        with open(filepath.value, 'w', encoding='utf-8') as f:
            f.write(str(content.value))
        return VMValue(VMValueType.BOOLEAN, True)
    except Exception as e:
        print(f"Error writing to file: {e}", file=sys.stderr)
        return VMValue(VMValueType.BOOLEAN, False)


def _file_append(vm: VirtualMachine, filepath: VMValue, content: VMValue) -> VMValue:
    """
    Append content to a file.
    
    Args:
        vm: The virtual machine
        filepath: The path to the file
        content: The content to append
        
    Returns:
        A boolean VM value indicating success
    """
    if filepath.type != VMValueType.STRING:
        return VMValue(VMValueType.BOOLEAN, False)
    
    try:
        with open(filepath.value, 'a', encoding='utf-8') as f:
            f.write(str(content.value))
        return VMValue(VMValueType.BOOLEAN, True)
    except Exception as e:
        print(f"Error appending to file: {e}", file=sys.stderr)
        return VMValue(VMValueType.BOOLEAN, False)


def _file_exists(vm: VirtualMachine, filepath: VMValue) -> VMValue:
    """
    Check if a file exists.
    
    Args:
        vm: The virtual machine
        filepath: The path to check
        
    Returns:
        A boolean VM value indicating if the file exists
    """
    if filepath.type != VMValueType.STRING:
        return VMValue(VMValueType.BOOLEAN, False)
    
    return VMValue(VMValueType.BOOLEAN, os.path.exists(filepath.value))


def _file_delete(vm: VirtualMachine, filepath: VMValue) -> VMValue:
    """
    Delete a file.
    
    Args:
        vm: The virtual machine
        filepath: The path to the file to delete
        
    Returns:
        A boolean VM value indicating success
    """
    if filepath.type != VMValueType.STRING:
        return VMValue(VMValueType.BOOLEAN, False)
    
    try:
        if os.path.exists(filepath.value):
            os.remove(filepath.value)
            return VMValue(VMValueType.BOOLEAN, True)
        return VMValue(VMValueType.BOOLEAN, False)
    except Exception as e:
        print(f"Error deleting file: {e}", file=sys.stderr)
        return VMValue(VMValueType.BOOLEAN, False)


def _file_copy(vm: VirtualMachine, source: VMValue, dest: VMValue) -> VMValue:
    """
    Copy a file from source to destination.
    
    Args:
        vm: The virtual machine
        source: The source file path
        dest: The destination file path
        
    Returns:
        A boolean VM value indicating success
    """
    if source.type != VMValueType.STRING or dest.type != VMValueType.STRING:
        return VMValue(VMValueType.BOOLEAN, False)
    
    try:
        import shutil
        shutil.copy2(source.value, dest.value)
        return VMValue(VMValueType.BOOLEAN, True)
    except Exception as e:
        print(f"Error copying file: {e}", file=sys.stderr)
        return VMValue(VMValueType.BOOLEAN, False)


def _file_move(vm: VirtualMachine, source: VMValue, dest: VMValue) -> VMValue:
    """
    Move a file from source to destination.
    
    Args:
        vm: The virtual machine
        source: The source file path
        dest: The destination file path
        
    Returns:
        A boolean VM value indicating success
    """
    if source.type != VMValueType.STRING or dest.type != VMValueType.STRING:
        return VMValue(VMValueType.BOOLEAN, False)
    
    try:
        import shutil
        shutil.move(source.value, dest.value)
        return VMValue(VMValueType.BOOLEAN, True)
    except Exception as e:
        print(f"Error moving file: {e}", file=sys.stderr)
        return VMValue(VMValueType.BOOLEAN, False)


def _file_size(vm: VirtualMachine, filepath: VMValue) -> VMValue:
    """
    Get the size of a file in bytes.
    
    Args:
        vm: The virtual machine
        filepath: The path to the file
        
    Returns:
        An integer VM value with the file size
    """
    if filepath.type != VMValueType.STRING:
        return VMValue(VMValueType.INTEGER, -1)
    
    try:
        if os.path.exists(filepath.value) and os.path.isfile(filepath.value):
            size = os.path.getsize(filepath.value)
            return VMValue(VMValueType.INTEGER, size)
        return VMValue(VMValueType.INTEGER, -1)
    except Exception as e:
        print(f"Error getting file size: {e}", file=sys.stderr)
        return VMValue(VMValueType.INTEGER, -1)


def _list_dir(vm: VirtualMachine, directory: VMValue) -> VMValue:
    """
    List the contents of a directory.
    
    Args:
        vm: The virtual machine
        directory: The directory path
        
    Returns:
        A list VM value with the directory contents
    """
    if directory.type != VMValueType.STRING:
        return VMValue(VMValueType.LIST, [])
    
    try:
        if os.path.exists(directory.value) and os.path.isdir(directory.value):
            contents = os.listdir(directory.value)
            return VMValue(VMValueType.LIST, [
                VMValue(VMValueType.STRING, item) for item in contents
            ])
        return VMValue(VMValueType.LIST, [])
    except Exception as e:
        print(f"Error listing directory: {e}", file=sys.stderr)
        return VMValue(VMValueType.LIST, [])


def _make_dir(vm: VirtualMachine, directory: VMValue, recursive: VMValue = None) -> VMValue:
    """
    Create a directory.
    
    Args:
        vm: The virtual machine
        directory: The directory path to create
        recursive: Whether to create parent directories
        
    Returns:
        A boolean VM value indicating success
    """
    if directory.type != VMValueType.STRING:
        return VMValue(VMValueType.BOOLEAN, False)
    
    is_recursive = recursive and recursive.type == VMValueType.BOOLEAN and recursive.value
    
    try:
        if is_recursive:
            os.makedirs(directory.value, exist_ok=True)
        else:
            os.mkdir(directory.value)
        return VMValue(VMValueType.BOOLEAN, True)
    except Exception as e:
        print(f"Error creating directory: {e}", file=sys.stderr)
        return VMValue(VMValueType.BOOLEAN, False)


def _remove_dir(vm: VirtualMachine, directory: VMValue, recursive: VMValue = None) -> VMValue:
    """
    Remove a directory.
    
    Args:
        vm: The virtual machine
        directory: The directory path to remove
        recursive: Whether to recursively remove subdirectories and files
        
    Returns:
        A boolean VM value indicating success
    """
    if directory.type != VMValueType.STRING:
        return VMValue(VMValueType.BOOLEAN, False)
    
    is_recursive = recursive and recursive.type == VMValueType.BOOLEAN and recursive.value
    
    try:
        if is_recursive:
            import shutil
            shutil.rmtree(directory.value)
        else:
            os.rmdir(directory.value)
        return VMValue(VMValueType.BOOLEAN, True)
    except Exception as e:
        print(f"Error removing directory: {e}", file=sys.stderr)
        return VMValue(VMValueType.BOOLEAN, False)


def _get_cwd(vm: VirtualMachine) -> VMValue:
    """
    Get the current working directory.
    
    Args:
        vm: The virtual machine
        
    Returns:
        A string VM value with the current working directory
    """
    try:
        return VMValue(VMValueType.STRING, os.getcwd())
    except Exception as e:
        print(f"Error getting current directory: {e}", file=sys.stderr)
        return VMValue(VMValueType.NULL, None)


def _change_dir(vm: VirtualMachine, directory: VMValue) -> VMValue:
    """
    Change the current working directory.
    
    Args:
        vm: The virtual machine
        directory: The directory to change to
        
    Returns:
        A boolean VM value indicating success
    """
    if directory.type != VMValueType.STRING:
        return VMValue(VMValueType.BOOLEAN, False)
    
    try:
        os.chdir(directory.value)
        return VMValue(VMValueType.BOOLEAN, True)
    except Exception as e:
        print(f"Error changing directory: {e}", file=sys.stderr)
        return VMValue(VMValueType.BOOLEAN, False)


def _path_join(vm: VirtualMachine, *paths) -> VMValue:
    """
    Join path components.
    
    Args:
        vm: The virtual machine
        *paths: The path components to join
        
    Returns:
        A string VM value with the joined path
    """
    try:
        path_strings = []
        for path in paths:
            if path.type != VMValueType.STRING:
                path_strings.append(str(path.value))
            else:
                path_strings.append(path.value)
        
        joined_path = os.path.join(*path_strings)
        return VMValue(VMValueType.STRING, joined_path)
    except Exception as e:
        print(f"Error joining paths: {e}", file=sys.stderr)
        return VMValue(VMValueType.NULL, None)


def _path_split(vm: VirtualMachine, path: VMValue) -> VMValue:
    """
    Split a path into directory and filename.
    
    Args:
        vm: The virtual machine
        path: The path to split
        
    Returns:
        A list VM value with [dirname, basename]
    """
    if path.type != VMValueType.STRING:
        return VMValue(VMValueType.LIST, [
            VMValue(VMValueType.STRING, ""),
            VMValue(VMValueType.STRING, "")
        ])
    
    try:
        dirname, basename = os.path.split(path.value)
        return VMValue(VMValueType.LIST, [
            VMValue(VMValueType.STRING, dirname),
            VMValue(VMValueType.STRING, basename)
        ])
    except Exception as e:
        print(f"Error splitting path: {e}", file=sys.stderr)
        return VMValue(VMValueType.LIST, [
            VMValue(VMValueType.STRING, ""),
            VMValue(VMValueType.STRING, "")
        ])


def _path_basename(vm: VirtualMachine, path: VMValue) -> VMValue:
    """
    Get the basename of a path.
    
    Args:
        vm: The virtual machine
        path: The path
        
    Returns:
        A string VM value with the basename
    """
    if path.type != VMValueType.STRING:
        return VMValue(VMValueType.STRING, "")
    
    try:
        basename = os.path.basename(path.value)
        return VMValue(VMValueType.STRING, basename)
    except Exception as e:
        print(f"Error getting basename: {e}", file=sys.stderr)
        return VMValue(VMValueType.STRING, "")


def _path_dirname(vm: VirtualMachine, path: VMValue) -> VMValue:
    """
    Get the directory name of a path.
    
    Args:
        vm: The virtual machine
        path: The path
        
    Returns:
        A string VM value with the directory name
    """
    if path.type != VMValueType.STRING:
        return VMValue(VMValueType.STRING, "")
    
    try:
        dirname = os.path.dirname(path.value)
        return VMValue(VMValueType.STRING, dirname)
    except Exception as e:
        print(f"Error getting dirname: {e}", file=sys.stderr)
        return VMValue(VMValueType.STRING, "")


def _path_extension(vm: VirtualMachine, path: VMValue) -> VMValue:
    """
    Get the file extension of a path.
    
    Args:
        vm: The virtual machine
        path: The path
        
    Returns:
        A string VM value with the extension
    """
    if path.type != VMValueType.STRING:
        return VMValue(VMValueType.STRING, "")
    
    try:
        _, ext = os.path.splitext(path.value)
        return VMValue(VMValueType.STRING, ext)
    except Exception as e:
        print(f"Error getting extension: {e}", file=sys.stderr)
        return VMValue(VMValueType.STRING, "")


def _path_absolute(vm: VirtualMachine, path: VMValue) -> VMValue:
    """
    Get the absolute path.
    
    Args:
        vm: The virtual machine
        path: The path
        
    Returns:
        A string VM value with the absolute path
    """
    if path.type != VMValueType.STRING:
        return VMValue(VMValueType.STRING, "")
    
    try:
        abs_path = os.path.abspath(path.value)
        return VMValue(VMValueType.STRING, abs_path)
    except Exception as e:
        print(f"Error getting absolute path: {e}", file=sys.stderr)
        return VMValue(VMValueType.STRING, "")


def _json_parse(vm: VirtualMachine, json_str: VMValue) -> VMValue:
    """
    Parse a JSON string into a Runa value.
    
    Args:
        vm: The virtual machine
        json_str: The JSON string to parse
        
    Returns:
        A VM value representing the parsed JSON
    """
    if json_str.type != VMValueType.STRING:
        return VMValue(VMValueType.NULL, None)
    
    try:
        data = json.loads(json_str.value)
        return _convert_json_to_vm_value(data)
    except Exception as e:
        print(f"Error parsing JSON: {e}", file=sys.stderr)
        return VMValue(VMValueType.NULL, None)


def _json_stringify(vm: VirtualMachine, value: VMValue, pretty: VMValue = None) -> VMValue:
    """
    Convert a Runa value to a JSON string.
    
    Args:
        vm: The virtual machine
        value: The value to convert
        pretty: Whether to pretty-print the JSON
        
    Returns:
        A string VM value with the JSON
    """
    try:
        data = _convert_vm_value_to_json(value)
        
        is_pretty = pretty and pretty.type == VMValueType.BOOLEAN and pretty.value
        if is_pretty:
            json_str = json.dumps(data, indent=2)
        else:
            json_str = json.dumps(data)
            
        return VMValue(VMValueType.STRING, json_str)
    except Exception as e:
        print(f"Error stringifying to JSON: {e}", file=sys.stderr)
        return VMValue(VMValueType.NULL, None)


def _convert_json_to_vm_value(data: Any) -> VMValue:
    """
    Convert a Python value from JSON to a VM value.
    
    Args:
        data: The Python value to convert
        
    Returns:
        A VM value
    """
    if data is None:
        return VMValue(VMValueType.NULL, None)
    elif isinstance(data, bool):
        return VMValue(VMValueType.BOOLEAN, data)
    elif isinstance(data, int):
        return VMValue(VMValueType.INTEGER, data)
    elif isinstance(data, float):
        return VMValue(VMValueType.FLOAT, data)
    elif isinstance(data, str):
        return VMValue(VMValueType.STRING, data)
    elif isinstance(data, list):
        return VMValue(VMValueType.LIST, [
            _convert_json_to_vm_value(item) for item in data
        ])
    elif isinstance(data, dict):
        result = {}
        for key, value in data.items():
            result[VMValue(VMValueType.STRING, key)] = _convert_json_to_vm_value(value)
        return VMValue(VMValueType.DICT, result)
    else:
        # Unsupported type
        return VMValue(VMValueType.NULL, None)


def _convert_vm_value_to_json(value: VMValue) -> Any:
    """
    Convert a VM value to a Python value for JSON.
    
    Args:
        value: The VM value to convert
        
    Returns:
        A Python value suitable for JSON serialization
    """
    if value.type == VMValueType.NULL:
        return None
    elif value.type == VMValueType.BOOLEAN:
        return bool(value.value)
    elif value.type == VMValueType.INTEGER:
        return int(value.value)
    elif value.type == VMValueType.FLOAT:
        return float(value.value)
    elif value.type == VMValueType.STRING:
        return str(value.value)
    elif value.type == VMValueType.LIST:
        return [_convert_vm_value_to_json(item) for item in value.value]
    elif value.type == VMValueType.DICT:
        result = {}
        for key, val in value.value.items():
            # JSON only allows string keys
            str_key = str(key.value)
            result[str_key] = _convert_vm_value_to_json(val)
        return result
    else:
        # Unsupported type
        return None 