# Runa Standard Library: Dict Module

## Overview

The `collections/dict` module provides comprehensive dictionary operations for creating, manipulating, and querying key-value pairs. Idiomatic Runa code uses dictionary literals, comprehensions, and helper processes for advanced or programmatic use cases.

The module includes advanced features such as:
- Core dictionary operations (get, set, remove, update)
- Bulk operations and batch processing
- Searching and filtering operations
- Dictionary transformations and mapping
- Merging and combining operations
- Performance optimizations
- Thread-safe operations (when supported)

## Core Operations

### Creation and Basic Operations
- `Process called "from_pairs" that takes pairs as List[Tuple[Any, Any]] returns Dictionary[Any, Any]`
- `Process called "create_empty_dict" that returns Dictionary[Any, Any]`
- `Process called "get" that takes d as Dictionary[Any, Any] and key as Any returns Any`
- `Process called "get_safe" that takes d as Dictionary[Any, Any] and key as Any and default as Any returns Any`
- `Process called "get_or_create" that takes d as Dictionary[Any, Any] and key as Any and factory as Process returns Any`
- `Process called "set" that takes d as Dictionary[Any, Any] and key as Any and value as Any returns Dictionary[Any, Any]`
- `Process called "set_multiple" that takes d as Dictionary[Any, Any] and updates as Dictionary[Any, Any] returns Dictionary[Any, Any]`
- `Process called "remove" that takes d as Dictionary[Any, Any] and key as Any returns Dictionary[Any, Any]`
- `Process called "remove_safe" that takes d as Dictionary[Any, Any] and key as Any returns Dictionary[Any, Any]`
- `Process called "pop" that takes d as Dictionary[Any, Any] and key as Any returns (Dictionary[Any, Any], Any)`
- `Process called "pop_safe" that takes d as Dictionary[Any, Any] and key as Any and default as Any returns (Dictionary[Any, Any], Any)`
- `Process called "clear" that takes d as Dictionary[Any, Any] returns Dictionary[Any, Any]`
- `Process called "copy" that takes d as Dictionary[Any, Any] returns Dictionary[Any, Any]`
- `Process called "deep_copy" that takes d as Dictionary[Any, Any] returns Dictionary[Any, Any]`

### Query and Analysis
- `Process called "contains" that takes d as Dictionary[Any, Any] and key as Any returns Boolean`
- `Process called "size" that takes d as Dictionary[Any, Any] returns Integer`
- `Process called "is_empty" that takes d as Dictionary[Any, Any] returns Boolean`
- `Process called "keys" that takes d as Dictionary[Any, Any] returns List[Any]`
- `Process called "values" that takes d as Dictionary[Any, Any] returns List[Any]`
- `Process called "items" that takes d as Dictionary[Any, Any] returns List[Tuple[Any, Any]]`
- `Process called "has_key" that takes d as Dictionary[Any, Any] and key as Any returns Boolean`
- `Process called "has_value" that takes d as Dictionary[Any, Any] and value as Any returns Boolean`
- `Process called "find_key" that takes d as Dictionary[Any, Any] and value as Any returns Optional[Any]`
- `Process called "find_all_keys" that takes d as Dictionary[Any, Any] and value as Any returns List[Any]`

### Bulk Operations
- `Process called "update" that takes d as Dictionary[Any, Any] and other as Dictionary[Any, Any] returns Dictionary[Any, Any]`
- `Process called "update_multiple" that takes d as Dictionary[Any, Any] and others as List[Dictionary[Any, Any]] returns Dictionary[Any, Any]`
- `Process called "merge" that takes d1 as Dictionary[Any, Any] and d2 as Dictionary[Any, Any] returns Dictionary[Any, Any]`
- `Process called "merge_multiple" that takes dicts as List[Dictionary[Any, Any]] returns Dictionary[Any, Any]`
- `Process called "merge_with" that takes d1 as Dictionary[Any, Any] and d2 as Dictionary[Any, Any] and merge_func as Process returns Dictionary[Any, Any]`

### Filtering and Transformation
- `Process called "filter_keys" that takes d as Dictionary[Any, Any] and predicate as Process returns Dictionary[Any, Any]`
- `Process called "filter_values" that takes d as Dictionary[Any, Any] and predicate as Process returns Dictionary[Any, Any]`
- `Process called "filter_items" that takes d as Dictionary[Any, Any] and predicate as Process returns Dictionary[Any, Any]`
- `Process called "map_keys" that takes d as Dictionary[Any, Any] and transform as Process returns Dictionary[Any, Any]`
- `Process called "map_values" that takes d as Dictionary[Any, Any] and transform as Process returns Dictionary[Any, Any]`
- `Process called "map_items" that takes d as Dictionary[Any, Any] and transform as Process returns Dictionary[Any, Any]`
- `Process called "invert" that takes d as Dictionary[Any, Any] returns Dictionary[Any, Any]`
- `Process called "invert_safe" that takes d as Dictionary[Any, Any] returns Dictionary[Any, Any]`

### Set-like Operations
- `Process called "intersection" that takes d1 as Dictionary[Any, Any] and d2 as Dictionary[Any, Any] returns Dictionary[Any, Any]`
- `Process called "union" that takes d1 as Dictionary[Any, Any] and d2 as Dictionary[Any, Any] returns Dictionary[Any, Any]`
- `Process called "difference" that takes d1 as Dictionary[Any, Any] and d2 as Dictionary[Any, Any] returns Dictionary[Any, Any]`
- `Process called "symmetric_difference" that takes d1 as Dictionary[Any, Any] and d2 as Dictionary[Any, Any] returns Dictionary[Any, Any]`

### Utility Operations
- `Process called "from_keys" that takes keys as List[Any] and default_value as Any returns Dictionary[Any, Any]`
- `Process called "from_keys_with_factory" that takes keys as List[Any] and factory as Process returns Dictionary[Any, Any]`
- `Process called "group_by" that takes items as List[Any] and key_func as Process returns Dictionary[Any, List[Any]]`
- `Process called "count_by" that takes items as List[Any] and key_func as Process returns Dictionary[Any, Integer]`
- `Process called "any" that takes d as Dictionary[Any, Any] and predicate as Process returns Boolean`
- `Process called "all" that takes d as Dictionary[Any, Any] and predicate as Process returns Boolean`
- `Process called "none" that takes d as Dictionary[Any, Any] and predicate as Process returns Boolean`
- `Process called "find" that takes d as Dictionary[Any, Any] and predicate as Process returns Optional[Tuple[Any, Any]]`
- `Process called "find_all" that takes d as Dictionary[Any, Any] and predicate as Process returns List[Tuple[Any, Any]]`
- `Process called "min_key" that takes d as Dictionary[Any, Any] returns Optional[Any]`
- `Process called "max_key" that takes d as Dictionary[Any, Any] returns Optional[Any]`
- `Process called "min_value" that takes d as Dictionary[Any, Any] returns Optional[Any]`
- `Process called "max_value" that takes d as Dictionary[Any, Any] returns Optional[Any]`
- `Process called "sum_values" that takes d as Dictionary[Any, Number] returns Number`
- `Process called "average_values" that takes d as Dictionary[Any, Number] returns Number`

## Usage Examples

### Basic Dictionary Operations
```runa
Let config be dictionary with:
    "host" as "localhost"
    "port" as 8080
    "debug" as true

Note: Safe access and modification
Let host be get_safe with d as config and key as "host" and default as "127.0.0.1"
Let (config, port) be pop with d as config and key as "port"
Let config be set with d as config and key as "timeout" and value as 30

Note: Bulk operations
Let updates be dictionary with:
    "max_connections" as 100
    "retry_count" as 3
Let config be update with d as config and other as updates
```

### Advanced Operations
```runa
Let users be list containing:
    dictionary with "id" as 1 and "name" as "Alice" and "age" as 30
    dictionary with "id" as 2 and "name" as "Bob" and "age" as 25
    dictionary with "id" as 3 and "name" as "Charlie" and "age" as 35

Note: Grouping and counting
Let by_age be group_by with items as users and key_func as lambda user: user["age"]
Let name_counts be count_by with items as users and key_func as lambda user: user["name"]

Note: Filtering and transformation
Let adults be filter_values with d as by_age and predicate as lambda users: length of users is greater than 0
Let age_names be map_values with d as by_age and transform as lambda users: map with lst as users and transform as lambda user: user["name"]
```

### Dictionary Merging and Combining
```runa
Let defaults be dictionary with:
    "theme" as "light"
    "language" as "en"
    "notifications" as true

Let user_prefs be dictionary with:
    "theme" as "dark"
    "timezone" as "UTC"

Note: Merging with custom logic
Let merged be merge_with with d1 as defaults and d2 as user_prefs and merge_func as lambda key, v1, v2: v2

Note: Set-like operations
Let common_keys be intersection with d1 as defaults and d2 as user_prefs
Let all_keys be union with d1 as defaults and d2 as user_prefs
```

### Functional Programming Patterns
```runa
Let data be dictionary with:
    "a" as 1
    "b" as 2
    "c" as 3
    "d" as 4

Note: Complex transformations
Let doubled be map_values with d as data and transform as lambda x: x multiplied by 2
Let even_values be filter_values with d as data and predicate as lambda x: remainder of x divided by 2 is equal to 0
Let key_value_pairs be items with d as data
Let sum_values be sum_values with d as data
```

## Performance Considerations

- **Immutable Operations**: Most operations return new dictionaries, preserving immutability
- **Safe Operations**: Use `get_safe`, `pop_safe`, `remove_safe` to avoid exceptions in production code
- **Bulk Operations**: Use `update`, `set_multiple` for efficient batch modifications
- **Factory Functions**: Use `get_or_create`, `from_keys_with_factory` for lazy initialization

## Testing

A comprehensive Runa-based test file for the dict module is located at:

    runa/tests/stdlib/test_dict.runa

This file exercises all dictionary operations using idiomatic Runa assertions and error handling. All standard library modules have corresponding Runa test files in this directory, ensuring production-ready quality and verifiability.

The test suite covers:
- Basic dictionary operations and edge cases
- Error handling for missing keys and invalid operations
- Performance characteristics of bulk operations
- Functional programming patterns and transformations
- Integration with other collection types 