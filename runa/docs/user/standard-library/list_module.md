# Runa Standard Library: List Module

## Overview

The `collections/list` module provides comprehensive list operations for creating, manipulating, and querying ordered sequences. Idiomatic Runa code uses list literals, comprehensions, and helper processes for advanced or programmatic use cases.

The module includes advanced features such as:
- Core list operations (append, remove, insert, pop)
- Bulk operations and batch processing
- Searching and filtering operations
- Sorting and ordering operations
- Slicing and indexing with bounds checking
- List transformations and mapping
- Performance optimizations
- Thread-safe operations (when supported)

## Core Operations

### Creation and Basic Operations
- `Process called "create_list" that takes elements as List[Any] returns List[Any]`
- `Process called "create_empty_list" that returns List[Any]`
- `Process called "append" that takes lst as List[Any] and value as Any returns List[Any]`
- `Process called "append_multiple" that takes lst as List[Any] and values as List[Any] returns List[Any]`
- `Process called "insert_at_index" that takes lst as List[Any] and index as Integer and value as Any returns List[Any]`
- `Process called "remove_at_index" that takes lst as List[Any] and index as Integer returns List[Any]`
- `Process called "remove_value" that takes lst as List[Any] and value as Any returns List[Any]`
- `Process called "remove_all" that takes lst as List[Any] and value as Any returns List[Any]`
- `Process called "pop" that takes lst as List[Any] returns (List[Any], Any)`
- `Process called "pop_at_index" that takes lst as List[Any] and index as Integer returns (List[Any], Any)`
- `Process called "clear" that takes lst as List[Any] returns List[Any]`
- `Process called "copy" that takes lst as List[Any] returns List[Any]`
- `Process called "deep_copy" that takes lst as List[Any] returns List[Any]`

### Query and Analysis
- `Process called "length" that takes lst as List[Any] returns Integer`
- `Process called "is_empty" that takes lst as List[Any] returns Boolean`
- `Process called "get" that takes lst as List[Any] and index as Integer returns Any`
- `Process called "get_safe" that takes lst as List[Any] and index as Integer and default as Any returns Any`
- `Process called "set" that takes lst as List[Any] and index as Integer and value as Any returns List[Any]`
- `Process called "contains" that takes lst as List[Any] and value as Any returns Boolean`
- `Process called "count" that takes lst as List[Any] and value as Any returns Integer`
- `Process called "index" that takes lst as List[Any] and value as Any returns Integer`
- `Process called "index_safe" that takes lst as List[Any] and value as Any returns Optional[Integer]`

### Slicing and Indexing
- `Process called "slice_list" that takes lst as List[Any] and start as Integer and end as Integer returns List[Any]`
- `Process called "slice_with_step" that takes lst as List[Any] and start as Integer and end as Integer and step as Integer returns List[Any]`
- `Process called "get_first" that takes lst as List[Any] returns Any`
- `Process called "get_last" that takes lst as List[Any] returns Any`
- `Process called "get_first_safe" that takes lst as List[Any] and default as Any returns Any`
- `Process called "get_last_safe" that takes lst as List[Any] and default as Any returns Any`

### Bulk Operations
- `Process called "extend" that takes lst as List[Any] and other as List[Any] returns List[Any]`
- `Process called "extend_multiple" that takes lst as List[Any] and others as List[List[Any]] returns List[Any]`
- `Process called "reverse" that takes lst as List[Any] returns List[Any]`
- `Process called "reverse_in_place" that takes lst as List[Any] returns List[Any]`

### Searching and Filtering
- `Process called "find" that takes lst as List[Any] and predicate as Process returns Optional[Integer]`
- `Process called "find_all" that takes lst as List[Any] and predicate as Process returns List[Integer]`
- `Process called "filter" that takes lst as List[Any] and predicate as Process returns List[Any]`
- `Process called "filter_not" that takes lst as List[Any] and predicate as Process returns List[Any]`
- `Process called "take" that takes lst as List[Any] and n as Integer returns List[Any]`
- `Process called "drop" that takes lst as List[Any] and n as Integer returns List[Any]`
- `Process called "take_while" that takes lst as List[Any] and predicate as Process returns List[Any]`
- `Process called "drop_while" that takes lst as List[Any] and predicate as Process returns List[Any]`

### Transformations
- `Process called "map" that takes lst as List[Any] and transform as Process returns List[Any]`
- `Process called "map_with_index" that takes lst as List[Any] and transform as Process returns List[Any]`
- `Process called "flat_map" that takes lst as List[Any] and transform as Process returns List[Any]`
- `Process called "zip" that takes lst1 as List[Any] and lst2 as List[Any] returns List[Tuple[Any, Any]]`
- `Process called "zip_longest" that takes lst1 as List[Any] and lst2 as List[Any] and fill_value as Any returns List[Tuple[Any, Any]]`

### Sorting and Ordering
- `Process called "sort" that takes lst as List[Any] returns List[Any]`
- `Process called "sort_in_place" that takes lst as List[Any] returns List[Any]`
- `Process called "sort_with_comparator" that takes lst as List[Any] and comparator as Process returns List[Any]`
- `Process called "sort_in_place_with_comparator" that takes lst as List[Any] and comparator as Process returns List[Any]`
- `Process called "sort_reverse" that takes lst as List[Any] returns List[Any]`
- `Process called "sort_in_place_reverse" that takes lst as List[Any] returns List[Any]`

### Utility Operations
- `Process called "unique" that takes lst as List[Any] returns List[Any]`
- `Process called "unique_by" that takes lst as List[Any] and key_func as Process returns List[Any]`
- `Process called "flatten" that takes lst as List[List[Any]] returns List[Any]`
- `Process called "flatten_deep" that takes lst as List[Any] returns List[Any]`
- `Process called "chunk" that takes lst as List[Any] and size as Integer returns List[List[Any]]`
- `Process called "partition" that takes lst as List[Any] and predicate as Process returns (List[Any], List[Any])`
- `Process called "group_by" that takes lst as List[Any] and key_func as Process returns Dictionary[Any, List[Any]]`
- `Process called "all" that takes lst as List[Any] and predicate as Process returns Boolean`
- `Process called "any" that takes lst as List[Any] and predicate as Process returns Boolean`
- `Process called "none" that takes lst as List[Any] and predicate as Process returns Boolean`
- `Process called "sum" that takes lst as List[Number] returns Number`
- `Process called "product" that takes lst as List[Number] returns Number`
- `Process called "average" that takes lst as List[Number] returns Number`
- `Process called "min_list" that takes lst as List[Number] returns Number`
- `Process called "max_list" that takes lst as List[Number] returns Number`

## Usage Examples

### Basic List Operations
```runa
Let numbers be list containing 1, 2, 3, 4, 5

Note: Append and insert operations
Let numbers be append with lst as numbers and value as 6
Let numbers be insert_at_index with lst as numbers and index as 0 and value as 0

Note: Remove operations
Let numbers be remove_value with lst as numbers and value as 3
Let (numbers, last) be pop with lst as numbers

Note: Query operations
Assert length of numbers is equal to 5
Assert numbers contains 2
Assert get with lst as numbers and index as 1 is equal to 1
```

### Advanced Operations
```runa
Let data be list containing 1, 2, 3, 4, 5, 6, 7, 8, 9, 10

Note: Filtering and mapping
Let evens be filter with lst as data and predicate as lambda x: remainder of x divided by 2 is equal to 0
Let squares be map with lst as evens and transform as lambda x: x multiplied by x

Note: Slicing and chunking
Let first_half be slice_list with lst as data and start as 0 and end as 5
Let chunks be chunk with lst as data and size as 3

Note: Sorting and grouping
Let sorted_data be sort with lst as data
Let grouped be group_by with lst as data and key_func as lambda x: remainder of x divided by 3
```

### Functional Programming Patterns
```runa
Let users be list containing:
    dictionary with "name" as "Alice" and "age" as 30
    dictionary with "name" as "Bob" and "age" as 25
    dictionary with "name" as "Charlie" and "age" as 35

Note: Complex transformations
Let names be map with lst as users and transform as lambda user: user["name"]
Let adults be filter with lst as users and predicate as lambda user: user["age"] is greater than or equal to 30
Let age_sum be sum with lst as map with lst as users and transform as lambda user: user["age"]
```

## Performance Considerations

- **Immutable Operations**: Most operations return new lists, preserving immutability
- **In-Place Operations**: Use `sort_in_place`, `reverse_in_place` for better performance when mutation is acceptable
- **Bulk Operations**: Use `extend`, `append_multiple` for adding multiple elements efficiently
- **Safe Operations**: Use `get_safe`, `index_safe` to avoid exceptions in production code

## Testing

A comprehensive Runa-based test file for the list module is located at:

    runa/tests/stdlib/test_list.runa

This file exercises all list operations using idiomatic Runa assertions and error handling. All standard library modules have corresponding Runa test files in this directory, ensuring production-ready quality and verifiability.

The test suite covers:
- Basic list operations and edge cases
- Error handling for invalid operations
- Performance characteristics of bulk operations
- Functional programming patterns and transformations
- Integration with other collection types 