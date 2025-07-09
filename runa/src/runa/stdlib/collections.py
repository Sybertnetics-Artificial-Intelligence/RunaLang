"""
Runa Standard Library - Collections Module

Provides collection manipulation functions for Runa programs.
"""

def length_of_collection(collection):
    """Get the length of a collection."""
    return len(collection)

def is_empty_collection(collection):
    """Check if a collection is empty."""
    return len(collection) == 0

def add_item_to_list(lst, item):
    """Add an item to the end of a list."""
    lst.append(item)
    return lst

def insert_item_at_index(lst, index, item):
    """Insert an item at a specific index in a list."""
    lst.insert(index, item)
    return lst

def remove_item_from_list(lst, item):
    """Remove the first occurrence of an item from a list."""
    if item in lst:
        lst.remove(item)
    return lst

def remove_item_at_index(lst, index):
    """Remove an item at a specific index from a list."""
    if 0 <= index < len(lst):
        return lst.pop(index)
    return None

def get_item_at_index(collection, index):
    """Get an item at a specific index from a collection."""
    if 0 <= index < len(collection):
        return collection[index]
    return None

def set_item_at_index(lst, index, item):
    """Set an item at a specific index in a list."""
    if 0 <= index < len(lst):
        lst[index] = item
    return lst

def contains_item(collection, item):
    """Check if a collection contains an item."""
    return item in collection

def find_index_of_item(collection, item):
    """Find the index of the first occurrence of an item."""
    try:
        return collection.index(item)
    except ValueError:
        return -1

def count_item_occurrences(collection, item):
    """Count how many times an item appears in a collection."""
    return collection.count(item)

def reverse_list(lst):
    """Reverse a list in place."""
    lst.reverse()
    return lst

def sort_list(lst, reverse=False):
    """Sort a list in place."""
    lst.sort(reverse=reverse)
    return lst

def filter_list(lst, predicate):
    """Filter a list based on a predicate function."""
    return [item for item in lst if predicate(item)]

def map_list(lst, function):
    """Apply a function to each item in a list."""
    return [function(item) for item in lst]

def reduce_list(lst, function, initial=None):
    """Reduce a list to a single value using a function."""
    from functools import reduce
    if initial is None:
        return reduce(function, lst)
    return reduce(function, lst, initial)

def slice_list(lst, start, end=None, step=1):
    """Extract a slice from a list."""
    if end is None:
        return lst[start::step]
    return lst[start:end:step]

def concatenate_lists(*lists):
    """Concatenate multiple lists into one."""
    result = []
    for lst in lists:
        result.extend(lst)
    return result

def zip_lists(*lists):
    """Zip multiple lists together."""
    return list(zip(*lists))

def flatten_list(nested_list):
    """Flatten a nested list structure."""
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten_list(item))
        else:
            result.append(item)
    return result

def unique_items(collection):
    """Get unique items from a collection."""
    return list(set(collection))

def intersection_of_lists(*lists):
    """Find the intersection of multiple lists."""
    if not lists:
        return []
    result = set(lists[0])
    for lst in lists[1:]:
        result = result.intersection(set(lst))
    return list(result)

def union_of_lists(*lists):
    """Find the union of multiple lists."""
    result = set()
    for lst in lists:
        result = result.union(set(lst))
    return list(result)

def difference_of_lists(list1, list2):
    """Find items in list1 that are not in list2."""
    return list(set(list1) - set(list2))

def create_dictionary():
    """Create an empty dictionary."""
    return {}

def add_key_value_to_dictionary(dictionary, key, value):
    """Add a key-value pair to a dictionary."""
    dictionary[key] = value
    return dictionary

def get_value_from_dictionary(dictionary, key, default=None):
    """Get a value from a dictionary by key."""
    return dictionary.get(key, default)

def remove_key_from_dictionary(dictionary, key):
    """Remove a key from a dictionary."""
    if key in dictionary:
        del dictionary[key]
    return dictionary

def get_dictionary_keys(dictionary):
    """Get all keys from a dictionary."""
    return list(dictionary.keys())

def get_dictionary_values(dictionary):
    """Get all values from a dictionary."""
    return list(dictionary.values())

def get_dictionary_items(dictionary):
    """Get all key-value pairs from a dictionary."""
    return list(dictionary.items())

def merge_dictionaries(*dictionaries):
    """Merge multiple dictionaries into one."""
    result = {}
    for dictionary in dictionaries:
        result.update(dictionary)
    return result

# Runa-style function names for natural language calling
get_length_of = length_of_collection
check_if_empty = is_empty_collection
add_to_list = add_item_to_list
insert_into_list = insert_item_at_index
remove_from_list = remove_item_from_list
get_from_collection = get_item_at_index
check_if_contains = contains_item
find_position_of = find_index_of_item
count_occurrences_of = count_item_occurrences
reverse_collection = reverse_list
sort_collection = sort_list
filter_collection = filter_list
apply_to_each = map_list
combine_collection = reduce_list
get_slice_of = slice_list
join_collections = concatenate_lists
combine_lists = zip_lists
make_flat = flatten_list
get_unique_items = unique_items
find_common_items = intersection_of_lists
combine_all_items = union_of_lists
find_different_items = difference_of_lists
create_empty_dictionary = create_dictionary
add_to_dictionary = add_key_value_to_dictionary
get_from_dictionary = get_value_from_dictionary
remove_from_dictionary = remove_key_from_dictionary
get_all_keys = get_dictionary_keys
get_all_values = get_dictionary_values
combine_dictionaries = merge_dictionaries