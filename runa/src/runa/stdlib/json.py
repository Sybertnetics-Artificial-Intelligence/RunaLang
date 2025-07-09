"""
Runa Standard Library - JSON Module

Provides JSON parsing and serialization for Runa programs.
"""

import json as py_json

def parse_json_string(json_string):
    """Parse a JSON string into a Python object."""
    try:
        return py_json.loads(json_string)
    except py_json.JSONDecodeError as e:
        raise Exception(f"Error parsing JSON: {e}")

def convert_to_json_string(obj, indent=None):
    """Convert a Python object to a JSON string."""
    try:
        return py_json.dumps(obj, indent=indent, ensure_ascii=False)
    except TypeError as e:
        raise Exception(f"Error converting to JSON: {e}")

def read_json_file(file_path):
    """Read and parse a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return py_json.load(file)
    except FileNotFoundError:
        raise Exception(f"JSON file not found: {file_path}")
    except py_json.JSONDecodeError as e:
        raise Exception(f"Error parsing JSON file: {e}")
    except Exception as e:
        raise Exception(f"Error reading JSON file: {e}")

def write_json_file(file_path, obj, indent=2):
    """Write a Python object to a JSON file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            py_json.dump(obj, file, indent=indent, ensure_ascii=False)
        return True
    except Exception as e:
        raise Exception(f"Error writing JSON file: {e}")

def pretty_print_json(obj, indent=2):
    """Pretty print a JSON object."""
    try:
        return py_json.dumps(obj, indent=indent, ensure_ascii=False, sort_keys=True)
    except TypeError as e:
        raise Exception(f"Error formatting JSON: {e}")

def minify_json(obj):
    """Minify a JSON object (remove whitespace)."""
    try:
        return py_json.dumps(obj, separators=(',', ':'), ensure_ascii=False)
    except TypeError as e:
        raise Exception(f"Error minifying JSON: {e}")

def validate_json_string(json_string):
    """Validate if a string is valid JSON."""
    try:
        py_json.loads(json_string)
        return True
    except py_json.JSONDecodeError:
        return False

def get_json_value(json_obj, key, default=None):
    """Get a value from a JSON object by key."""
    if isinstance(json_obj, dict):
        return json_obj.get(key, default)
    return default

def set_json_value(json_obj, key, value):
    """Set a value in a JSON object."""
    if isinstance(json_obj, dict):
        json_obj[key] = value
    return json_obj

def has_json_key(json_obj, key):
    """Check if a JSON object has a specific key."""
    if isinstance(json_obj, dict):
        return key in json_obj
    return False

def get_json_keys(json_obj):
    """Get all keys from a JSON object."""
    if isinstance(json_obj, dict):
        return list(json_obj.keys())
    return []

def get_json_values(json_obj):
    """Get all values from a JSON object."""
    if isinstance(json_obj, dict):
        return list(json_obj.values())
    return []

def merge_json_objects(*json_objects):
    """Merge multiple JSON objects into one."""
    result = {}
    for obj in json_objects:
        if isinstance(obj, dict):
            result.update(obj)
    return result

def filter_json_object(json_obj, keys_to_keep):
    """Filter a JSON object to keep only specified keys."""
    if isinstance(json_obj, dict):
        return {key: json_obj[key] for key in keys_to_keep if key in json_obj}
    return {}

def remove_json_keys(json_obj, keys_to_remove):
    """Remove specified keys from a JSON object."""
    if isinstance(json_obj, dict):
        return {key: value for key, value in json_obj.items() if key not in keys_to_remove}
    return json_obj

def flatten_json_object(json_obj, separator='.'):
    """Flatten a nested JSON object."""
    def _flatten(obj, parent_key=''):
        items = []
        if isinstance(obj, dict):
            for key, value in obj.items():
                new_key = f"{parent_key}{separator}{key}" if parent_key else key
                if isinstance(value, dict):
                    items.extend(_flatten(value, new_key).items())
                elif isinstance(value, list):
                    for i, item in enumerate(value):
                        list_key = f"{new_key}[{i}]"
                        if isinstance(item, dict):
                            items.extend(_flatten(item, list_key).items())
                        else:
                            items.append((list_key, item))
                else:
                    items.append((new_key, value))
        return dict(items)
    
    return _flatten(json_obj)

def unflatten_json_object(flattened_obj, separator='.'):
    """Unflatten a flattened JSON object."""
    result = {}
    for key, value in flattened_obj.items():
        parts = key.split(separator)
        current = result
        
        for part in parts[:-1]:
            if '[' in part and ']' in part:
                # Handle array indices
                array_key = part.split('[')[0]
                index = int(part.split('[')[1].split(']')[0])
                if array_key not in current:
                    current[array_key] = []
                while len(current[array_key]) <= index:
                    current[array_key].append({})
                current = current[array_key][index]
            else:
                if part not in current:
                    current[part] = {}
                current = current[part]
        
        # Set the final value
        final_key = parts[-1]
        if '[' in final_key and ']' in final_key:
            array_key = final_key.split('[')[0]
            index = int(final_key.split('[')[1].split(']')[0])
            if array_key not in current:
                current[array_key] = []
            while len(current[array_key]) <= index:
                current[array_key].append(None)
            current[array_key][index] = value
        else:
            current[final_key] = value
    
    return result

def deep_copy_json(json_obj):
    """Create a deep copy of a JSON object."""
    return py_json.loads(py_json.dumps(json_obj))

def compare_json_objects(obj1, obj2):
    """Compare two JSON objects for equality."""
    return py_json.dumps(obj1, sort_keys=True) == py_json.dumps(obj2, sort_keys=True)

def json_object_size(json_obj):
    """Get the size of a JSON object in bytes."""
    return len(py_json.dumps(json_obj, ensure_ascii=False).encode('utf-8'))

# Runa-style function names for natural language calling
convert_json_to_object = parse_json_string
convert_object_to_json = convert_to_json_string
load_json_from_file = read_json_file
save_json_to_file = write_json_file
format_json_nicely = pretty_print_json
compress_json = minify_json
check_if_valid_json = validate_json_string
get_value_from_json = get_json_value
set_value_in_json = set_json_value
check_if_json_has_key = has_json_key
get_all_json_keys = get_json_keys
get_all_json_values = get_json_values
combine_json_objects = merge_json_objects
keep_only_json_keys = filter_json_object
remove_json_properties = remove_json_keys
make_json_flat = flatten_json_object
make_json_nested = unflatten_json_object
copy_json_object = deep_copy_json
check_if_json_equal = compare_json_objects
get_json_size = json_object_size