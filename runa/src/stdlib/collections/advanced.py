"""
Advanced collection types and operations for Runa.

This module provides advanced data structures and collection operations.
"""

from typing import Dict, List, Any, Optional, Set, Tuple
import heapq
import itertools
from collections import deque, defaultdict, Counter

from ...vm.vm import VirtualMachine, VMValue, VMValueType


def register_collections_functions(vm: VirtualMachine) -> None:
    """
    Register collection functions with the VM.
    
    Args:
        vm: The virtual machine to register the functions with
    """
    # List operations
    vm.native_functions["list_append"] = _list_append
    vm.native_functions["list_insert"] = _list_insert
    vm.native_functions["list_remove"] = _list_remove
    vm.native_functions["list_pop"] = _list_pop
    vm.native_functions["list_index"] = _list_index
    vm.native_functions["list_count"] = _list_count
    vm.native_functions["list_sort"] = _list_sort
    vm.native_functions["list_reverse"] = _list_reverse
    vm.native_functions["list_slice"] = _list_slice
    
    # Dictionary operations
    vm.native_functions["dict_keys"] = _dict_keys
    vm.native_functions["dict_values"] = _dict_values
    vm.native_functions["dict_items"] = _dict_items
    vm.native_functions["dict_get"] = _dict_get
    vm.native_functions["dict_pop"] = _dict_pop
    vm.native_functions["dict_clear"] = _dict_clear
    vm.native_functions["dict_update"] = _dict_update
    
    # Set operations
    vm.native_functions["set_create"] = _set_create
    vm.native_functions["set_add"] = _set_add
    vm.native_functions["set_remove"] = _set_remove
    vm.native_functions["set_contains"] = _set_contains
    vm.native_functions["set_union"] = _set_union
    vm.native_functions["set_intersection"] = _set_intersection
    vm.native_functions["set_difference"] = _set_difference
    
    # Queue operations
    vm.native_functions["queue_create"] = _queue_create
    vm.native_functions["queue_push"] = _queue_push
    vm.native_functions["queue_pop"] = _queue_pop
    vm.native_functions["queue_peek"] = _queue_peek
    
    # Priority queue operations
    vm.native_functions["priority_queue_create"] = _priority_queue_create
    vm.native_functions["priority_queue_push"] = _priority_queue_push
    vm.native_functions["priority_queue_pop"] = _priority_queue_pop
    vm.native_functions["priority_queue_peek"] = _priority_queue_peek


# List operations

def _list_append(vm: VirtualMachine, lst: VMValue, item: VMValue) -> VMValue:
    """
    Append an item to a list.
    
    Args:
        vm: The virtual machine
        lst: The list to append to
        item: The item to append
        
    Returns:
        The modified list
    """
    if lst.type != VMValueType.LIST:
        return VMValue(VMValueType.LIST, [item])
    
    lst.value.append(item)
    return lst


def _list_insert(vm: VirtualMachine, lst: VMValue, index: VMValue, item: VMValue) -> VMValue:
    """
    Insert an item at a specific index in a list.
    
    Args:
        vm: The virtual machine
        lst: The list to insert into
        index: The index to insert at
        item: The item to insert
        
    Returns:
        The modified list
    """
    if lst.type != VMValueType.LIST or index.type != VMValueType.INTEGER:
        return VMValue(VMValueType.LIST, [item])
    
    try:
        lst.value.insert(index.value, item)
    except IndexError:
        # If index is out of range, append to the end
        lst.value.append(item)
    
    return lst


def _list_remove(vm: VirtualMachine, lst: VMValue, item: VMValue) -> VMValue:
    """
    Remove the first occurrence of an item from a list.
    
    Args:
        vm: The virtual machine
        lst: The list to remove from
        item: The item to remove
        
    Returns:
        A boolean indicating success
    """
    if lst.type != VMValueType.LIST:
        return VMValue(VMValueType.BOOLEAN, False)
    
    # Find the item by value comparison
    for i, val in enumerate(lst.value):
        if _values_equal(val, item):
            lst.value.pop(i)
            return VMValue(VMValueType.BOOLEAN, True)
    
    return VMValue(VMValueType.BOOLEAN, False)


def _list_pop(vm: VirtualMachine, lst: VMValue, index: VMValue = None) -> VMValue:
    """
    Remove and return an item at a specific index from a list.
    
    Args:
        vm: The virtual machine
        lst: The list to pop from
        index: The index to pop (default: last item)
        
    Returns:
        The popped item or null if the list is empty
    """
    if lst.type != VMValueType.LIST:
        return VMValue(VMValueType.NULL, None)
    
    if not lst.value:
        return VMValue(VMValueType.NULL, None)
    
    idx = -1  # Default to last item
    if index and index.type == VMValueType.INTEGER:
        idx = index.value
    
    try:
        return lst.value.pop(idx)
    except IndexError:
        return VMValue(VMValueType.NULL, None)


def _list_index(vm: VirtualMachine, lst: VMValue, item: VMValue) -> VMValue:
    """
    Find the index of the first occurrence of an item in a list.
    
    Args:
        vm: The virtual machine
        lst: The list to search
        item: The item to find
        
    Returns:
        The index of the item or -1 if not found
    """
    if lst.type != VMValueType.LIST:
        return VMValue(VMValueType.INTEGER, -1)
    
    for i, val in enumerate(lst.value):
        if _values_equal(val, item):
            return VMValue(VMValueType.INTEGER, i)
    
    return VMValue(VMValueType.INTEGER, -1)


def _list_count(vm: VirtualMachine, lst: VMValue, item: VMValue) -> VMValue:
    """
    Count the number of occurrences of an item in a list.
    
    Args:
        vm: The virtual machine
        lst: The list to search
        item: The item to count
        
    Returns:
        The count of the item
    """
    if lst.type != VMValueType.LIST:
        return VMValue(VMValueType.INTEGER, 0)
    
    count = 0
    for val in lst.value:
        if _values_equal(val, item):
            count += 1
    
    return VMValue(VMValueType.INTEGER, count)


def _list_sort(vm: VirtualMachine, lst: VMValue, reverse: VMValue = None) -> VMValue:
    """
    Sort a list in-place.
    
    Args:
        vm: The virtual machine
        lst: The list to sort
        reverse: Whether to sort in reverse order
        
    Returns:
        The sorted list
    """
    if lst.type != VMValueType.LIST:
        return VMValue(VMValueType.LIST, [])
    
    is_reverse = reverse and reverse.type == VMValueType.BOOLEAN and reverse.value
    
    try:
        lst.value.sort(key=_vm_value_sort_key, reverse=is_reverse)
    except Exception:
        # If sorting fails (e.g. different types), do nothing
        pass
    
    return lst


def _list_reverse(vm: VirtualMachine, lst: VMValue) -> VMValue:
    """
    Reverse a list in-place.
    
    Args:
        vm: The virtual machine
        lst: The list to reverse
        
    Returns:
        The reversed list
    """
    if lst.type != VMValueType.LIST:
        return VMValue(VMValueType.LIST, [])
    
    lst.value.reverse()
    return lst


def _list_slice(vm: VirtualMachine, lst: VMValue, start: VMValue, end: VMValue = None, step: VMValue = None) -> VMValue:
    """
    Get a slice of a list.
    
    Args:
        vm: The virtual machine
        lst: The list to slice
        start: The start index
        end: The end index (exclusive)
        step: The step size
        
    Returns:
        A new list with the slice
    """
    if lst.type != VMValueType.LIST or start.type != VMValueType.INTEGER:
        return VMValue(VMValueType.LIST, [])
    
    start_idx = start.value
    end_idx = None
    step_size = 1
    
    if end and end.type == VMValueType.INTEGER:
        end_idx = end.value
    
    if step and step.type == VMValueType.INTEGER:
        step_size = step.value
        if step_size == 0:
            step_size = 1  # Prevent zero step
    
    try:
        sliced = lst.value[start_idx:end_idx:step_size]
        return VMValue(VMValueType.LIST, sliced.copy())
    except Exception:
        return VMValue(VMValueType.LIST, [])


# Dictionary operations

def _dict_keys(vm: VirtualMachine, dct: VMValue) -> VMValue:
    """
    Get the keys of a dictionary.
    
    Args:
        vm: The virtual machine
        dct: The dictionary
        
    Returns:
        A list of the keys
    """
    if dct.type != VMValueType.DICT:
        return VMValue(VMValueType.LIST, [])
    
    return VMValue(VMValueType.LIST, list(dct.value.keys()))


def _dict_values(vm: VirtualMachine, dct: VMValue) -> VMValue:
    """
    Get the values of a dictionary.
    
    Args:
        vm: The virtual machine
        dct: The dictionary
        
    Returns:
        A list of the values
    """
    if dct.type != VMValueType.DICT:
        return VMValue(VMValueType.LIST, [])
    
    return VMValue(VMValueType.LIST, list(dct.value.values()))


def _dict_items(vm: VirtualMachine, dct: VMValue) -> VMValue:
    """
    Get the items (key-value pairs) of a dictionary.
    
    Args:
        vm: The virtual machine
        dct: The dictionary
        
    Returns:
        A list of lists, where each inner list is [key, value]
    """
    if dct.type != VMValueType.DICT:
        return VMValue(VMValueType.LIST, [])
    
    items = []
    for key, value in dct.value.items():
        items.append(VMValue(VMValueType.LIST, [key, value]))
    
    return VMValue(VMValueType.LIST, items)


def _dict_get(vm: VirtualMachine, dct: VMValue, key: VMValue, default: VMValue = None) -> VMValue:
    """
    Get a value from a dictionary with a default if the key doesn't exist.
    
    Args:
        vm: The virtual machine
        dct: The dictionary
        key: The key to look up
        default: The default value if key doesn't exist
        
    Returns:
        The value or default
    """
    if dct.type != VMValueType.DICT:
        return default or VMValue(VMValueType.NULL, None)
    
    for k, v in dct.value.items():
        if _values_equal(k, key):
            return v
    
    return default or VMValue(VMValueType.NULL, None)


def _dict_pop(vm: VirtualMachine, dct: VMValue, key: VMValue, default: VMValue = None) -> VMValue:
    """
    Remove a key from a dictionary and return its value.
    
    Args:
        vm: The virtual machine
        dct: The dictionary
        key: The key to remove
        default: The default value if key doesn't exist
        
    Returns:
        The value or default
    """
    if dct.type != VMValueType.DICT:
        return default or VMValue(VMValueType.NULL, None)
    
    for k in list(dct.value.keys()):
        if _values_equal(k, key):
            value = dct.value[k]
            del dct.value[k]
            return value
    
    return default or VMValue(VMValueType.NULL, None)


def _dict_clear(vm: VirtualMachine, dct: VMValue) -> VMValue:
    """
    Remove all items from a dictionary.
    
    Args:
        vm: The virtual machine
        dct: The dictionary
        
    Returns:
        The empty dictionary
    """
    if dct.type != VMValueType.DICT:
        return VMValue(VMValueType.DICT, {})
    
    dct.value.clear()
    return dct


def _dict_update(vm: VirtualMachine, dct: VMValue, other: VMValue) -> VMValue:
    """
    Update a dictionary with items from another dictionary.
    
    Args:
        vm: The virtual machine
        dct: The dictionary to update
        other: The dictionary to update from
        
    Returns:
        The updated dictionary
    """
    if dct.type != VMValueType.DICT:
        dct = VMValue(VMValueType.DICT, {})
    
    if other.type != VMValueType.DICT:
        return dct
    
    for key, value in other.value.items():
        dct.value[key] = value
    
    return dct


# Set operations

def _set_create(vm: VirtualMachine, items: VMValue = None) -> VMValue:
    """
    Create a set (implemented as a dictionary with None values).
    
    Args:
        vm: The virtual machine
        items: Optional list of items to add to the set
        
    Returns:
        A dictionary VM value representing the set
    """
    result = {}
    
    if items and items.type == VMValueType.LIST:
        for item in items.value:
            # Skip unhashable types
            if item.type in [VMValueType.LIST, VMValueType.DICT]:
                continue
            result[item] = VMValue(VMValueType.NULL, None)
    
    return VMValue(VMValueType.DICT, result)


def _set_add(vm: VirtualMachine, set_dict: VMValue, item: VMValue) -> VMValue:
    """
    Add an item to a set.
    
    Args:
        vm: The virtual machine
        set_dict: The set (as a dictionary)
        item: The item to add
        
    Returns:
        The modified set
    """
    if set_dict.type != VMValueType.DICT:
        set_dict = VMValue(VMValueType.DICT, {})
    
    # Skip unhashable types
    if item.type not in [VMValueType.LIST, VMValueType.DICT]:
        set_dict.value[item] = VMValue(VMValueType.NULL, None)
    
    return set_dict


def _set_remove(vm: VirtualMachine, set_dict: VMValue, item: VMValue) -> VMValue:
    """
    Remove an item from a set.
    
    Args:
        vm: The virtual machine
        set_dict: The set (as a dictionary)
        item: The item to remove
        
    Returns:
        A boolean indicating success
    """
    if set_dict.type != VMValueType.DICT:
        return VMValue(VMValueType.BOOLEAN, False)
    
    for key in list(set_dict.value.keys()):
        if _values_equal(key, item):
            del set_dict.value[key]
            return VMValue(VMValueType.BOOLEAN, True)
    
    return VMValue(VMValueType.BOOLEAN, False)


def _set_contains(vm: VirtualMachine, set_dict: VMValue, item: VMValue) -> VMValue:
    """
    Check if a set contains an item.
    
    Args:
        vm: The virtual machine
        set_dict: The set (as a dictionary)
        item: The item to check
        
    Returns:
        A boolean indicating containment
    """
    if set_dict.type != VMValueType.DICT:
        return VMValue(VMValueType.BOOLEAN, False)
    
    for key in set_dict.value.keys():
        if _values_equal(key, item):
            return VMValue(VMValueType.BOOLEAN, True)
    
    return VMValue(VMValueType.BOOLEAN, False)


def _set_union(vm: VirtualMachine, set1: VMValue, set2: VMValue) -> VMValue:
    """
    Get the union of two sets.
    
    Args:
        vm: The virtual machine
        set1: The first set
        set2: The second set
        
    Returns:
        A new set with the union
    """
    if set1.type != VMValueType.DICT:
        set1 = VMValue(VMValueType.DICT, {})
    
    if set2.type != VMValueType.DICT:
        return set1
    
    result = {}
    
    # Add all items from set1
    for key in set1.value.keys():
        result[key] = VMValue(VMValueType.NULL, None)
    
    # Add all items from set2
    for key in set2.value.keys():
        result[key] = VMValue(VMValueType.NULL, None)
    
    return VMValue(VMValueType.DICT, result)


def _set_intersection(vm: VirtualMachine, set1: VMValue, set2: VMValue) -> VMValue:
    """
    Get the intersection of two sets.
    
    Args:
        vm: The virtual machine
        set1: The first set
        set2: The second set
        
    Returns:
        A new set with the intersection
    """
    if set1.type != VMValueType.DICT or set2.type != VMValueType.DICT:
        return VMValue(VMValueType.DICT, {})
    
    result = {}
    
    # Add items that are in both sets
    for key1 in set1.value.keys():
        for key2 in set2.value.keys():
            if _values_equal(key1, key2):
                result[key1] = VMValue(VMValueType.NULL, None)
                break
    
    return VMValue(VMValueType.DICT, result)


def _set_difference(vm: VirtualMachine, set1: VMValue, set2: VMValue) -> VMValue:
    """
    Get the difference of two sets (items in set1 that are not in set2).
    
    Args:
        vm: The virtual machine
        set1: The first set
        set2: The second set
        
    Returns:
        A new set with the difference
    """
    if set1.type != VMValueType.DICT:
        return VMValue(VMValueType.DICT, {})
    
    if set2.type != VMValueType.DICT:
        return set1
    
    result = {}
    
    # Add items from set1 that are not in set2
    for key1 in set1.value.keys():
        in_set2 = False
        for key2 in set2.value.keys():
            if _values_equal(key1, key2):
                in_set2 = True
                break
        
        if not in_set2:
            result[key1] = VMValue(VMValueType.NULL, None)
    
    return VMValue(VMValueType.DICT, result)


# Queue operations

# Store queues by handle
_queues: Dict[int, deque] = {}
_next_queue_handle = 1

def _queue_create(vm: VirtualMachine, items: VMValue = None) -> VMValue:
    """
    Create a queue.
    
    Args:
        vm: The virtual machine
        items: Optional list of items to add to the queue
        
    Returns:
        An integer VM value with the queue handle
    """
    global _queues, _next_queue_handle
    
    queue = deque()
    
    if items and items.type == VMValueType.LIST:
        for item in items.value:
            queue.append(item)
    
    handle = _next_queue_handle
    _next_queue_handle += 1
    _queues[handle] = queue
    
    return VMValue(VMValueType.INTEGER, handle)


def _queue_push(vm: VirtualMachine, handle: VMValue, item: VMValue) -> VMValue:
    """
    Push an item onto the end of a queue.
    
    Args:
        vm: The virtual machine
        handle: The queue handle
        item: The item to push
        
    Returns:
        A boolean indicating success
    """
    global _queues
    
    if handle.type != VMValueType.INTEGER or handle.value not in _queues:
        return VMValue(VMValueType.BOOLEAN, False)
    
    _queues[handle.value].append(item)
    return VMValue(VMValueType.BOOLEAN, True)


def _queue_pop(vm: VirtualMachine, handle: VMValue) -> VMValue:
    """
    Pop an item from the front of a queue.
    
    Args:
        vm: The virtual machine
        handle: The queue handle
        
    Returns:
        The popped item or null if the queue is empty
    """
    global _queues
    
    if handle.type != VMValueType.INTEGER or handle.value not in _queues:
        return VMValue(VMValueType.NULL, None)
    
    queue = _queues[handle.value]
    
    if not queue:
        return VMValue(VMValueType.NULL, None)
    
    return queue.popleft()


def _queue_peek(vm: VirtualMachine, handle: VMValue) -> VMValue:
    """
    Peek at the front item of a queue without removing it.
    
    Args:
        vm: The virtual machine
        handle: The queue handle
        
    Returns:
        The front item or null if the queue is empty
    """
    global _queues
    
    if handle.type != VMValueType.INTEGER or handle.value not in _queues:
        return VMValue(VMValueType.NULL, None)
    
    queue = _queues[handle.value]
    
    if not queue:
        return VMValue(VMValueType.NULL, None)
    
    return queue[0]


# Priority queue operations

# Store priority queues by handle
_priority_queues: Dict[int, List[Tuple[Any, VMValue]]] = {}
_next_pq_handle = 1

def _priority_queue_create(vm: VirtualMachine) -> VMValue:
    """
    Create a priority queue.
    
    Args:
        vm: The virtual machine
        
    Returns:
        An integer VM value with the priority queue handle
    """
    global _priority_queues, _next_pq_handle
    
    pq = []
    
    handle = _next_pq_handle
    _next_pq_handle += 1
    _priority_queues[handle] = pq
    
    return VMValue(VMValueType.INTEGER, handle)


def _priority_queue_push(vm: VirtualMachine, handle: VMValue, item: VMValue, priority: VMValue) -> VMValue:
    """
    Push an item onto a priority queue with the given priority.
    
    Args:
        vm: The virtual machine
        handle: The priority queue handle
        item: The item to push
        priority: The priority (lower values have higher priority)
        
    Returns:
        A boolean indicating success
    """
    global _priority_queues
    
    if (handle.type != VMValueType.INTEGER or 
        handle.value not in _priority_queues or
        priority.type not in [VMValueType.INTEGER, VMValueType.FLOAT]):
        return VMValue(VMValueType.BOOLEAN, False)
    
    pq = _priority_queues[handle.value]
    
    # Use the priority value for sorting
    heapq.heappush(pq, (priority.value, item))
    
    return VMValue(VMValueType.BOOLEAN, True)


def _priority_queue_pop(vm: VirtualMachine, handle: VMValue) -> VMValue:
    """
    Pop the highest-priority item from a priority queue.
    
    Args:
        vm: The virtual machine
        handle: The priority queue handle
        
    Returns:
        The popped item or null if the queue is empty
    """
    global _priority_queues
    
    if handle.type != VMValueType.INTEGER or handle.value not in _priority_queues:
        return VMValue(VMValueType.NULL, None)
    
    pq = _priority_queues[handle.value]
    
    if not pq:
        return VMValue(VMValueType.NULL, None)
    
    _, item = heapq.heappop(pq)
    return item


def _priority_queue_peek(vm: VirtualMachine, handle: VMValue) -> VMValue:
    """
    Peek at the highest-priority item of a priority queue without removing it.
    
    Args:
        vm: The virtual machine
        handle: The priority queue handle
        
    Returns:
        The highest-priority item or null if the queue is empty
    """
    global _priority_queues
    
    if handle.type != VMValueType.INTEGER or handle.value not in _priority_queues:
        return VMValue(VMValueType.NULL, None)
    
    pq = _priority_queues[handle.value]
    
    if not pq:
        return VMValue(VMValueType.NULL, None)
    
    _, item = pq[0]
    return item


# Helper functions

def _values_equal(a: VMValue, b: VMValue) -> bool:
    """
    Compare two VM values for equality.
    
    Args:
        a: The first value
        b: The second value
        
    Returns:
        Whether the values are equal
    """
    if a.type != b.type:
        return False
    
    if a.type == VMValueType.LIST:
        if len(a.value) != len(b.value):
            return False
        
        for i in range(len(a.value)):
            if not _values_equal(a.value[i], b.value[i]):
                return False
        
        return True
    
    elif a.type == VMValueType.DICT:
        if len(a.value) != len(b.value):
            return False
        
        for key_a, value_a in a.value.items():
            found = False
            for key_b, value_b in b.value.items():
                if _values_equal(key_a, key_b) and _values_equal(value_a, value_b):
                    found = True
                    break
            
            if not found:
                return False
        
        return True
    
    else:
        # For simple types, compare the value directly
        return a.value == b.value


def _vm_value_sort_key(value: VMValue) -> Any:
    """
    Get a sort key for a VM value.
    
    Args:
        value: The VM value
        
    Returns:
        A sort key for the value
    """
    if value.type == VMValueType.NULL:
        return (0, None)
    elif value.type == VMValueType.BOOLEAN:
        return (1, value.value)
    elif value.type == VMValueType.INTEGER:
        return (2, value.value)
    elif value.type == VMValueType.FLOAT:
        return (3, value.value)
    elif value.type == VMValueType.STRING:
        return (4, value.value)
    else:
        # Lists, dicts, and other complex types are sorted by their string representation
        return (5, str(value.value)) 