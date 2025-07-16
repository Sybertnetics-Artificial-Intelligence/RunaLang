# Runa Standard Library: Deque Module

## Overview

The `collections/deque` module provides a comprehensive double-ended queue with natural language operations for adding, removing, and inspecting elements from both ends. Advanced features include rotation, bulk operations, slicing, searching, sorting, and performance optimizations.

## Features

- **Core Operations**: Add/remove from both ends with bounds checking
- **Rotation and Shifting**: Rotate elements left/right, shift elements
- **Bulk Operations**: Extend from front/back, batch processing
- **Slicing and Indexing**: Get/set at specific indices with bounds checking
- **Searching and Filtering**: Find elements, count occurrences, filter by predicate
- **Sorting and Ordering**: Sort with custom keys, check if sorted
- **Statistical Operations**: Min/max, sum, average calculations
- **Memory Optimization**: Compaction, deduplication, shuffling
- **Bounded Deques**: Optional maximum length with automatic truncation

## Types

### Deque[T]
Double-ended queue with optional maximum length constraint.

## Core API

### Creation
- `Process called "create_deque" that returns Deque[Any]`
- `Process called "create_deque_with_maxlen" that takes maxlen as Integer returns Deque[Any]`
- `Process called "from_list" that takes items as List[Any] returns Deque[Any]`
- `Process called "from_list_with_maxlen" that takes items as List[Any] and maxlen as Integer returns Deque[Any]`

### Basic Operations
- `Process called "add_to_front" that takes deque as Deque[Any] and value as Any returns Deque[Any]`
- `Process called "add_to_back" that takes deque as Deque[Any] and value as Any returns Deque[Any]`
- `Process called "remove_from_front" that takes deque as Deque[Any] returns (Deque[Any], Any)`
- `Process called "remove_from_back" that takes deque as Deque[Any] returns (Deque[Any], Any)`
- `Process called "peek_front" that takes deque as Deque[Any] returns Any`
- `Process called "peek_back" that takes deque as Deque[Any] returns Any`

### Query Operations
- `Process called "deque_length" that takes deque as Deque[Any] returns Integer`
- `Process called "deque_is_empty" that takes deque as Deque[Any] returns Boolean`
- `Process called "deque_is_full" that takes deque as Deque[Any] returns Boolean`
- `Process called "get_maxlen" that takes deque as Deque[Any] returns Optional[Integer]`
- `Process called "set_maxlen" that takes deque as Deque[Any] and maxlen as Integer returns Deque[Any]`

## Rotation and Shifting Operations

- `Process called "rotate" that takes deque as Deque[Any] and n as Integer returns Deque[Any]`
- `Process called "rotate_left" that takes deque as Deque[Any] and n as Integer returns Deque[Any]`
- `Process called "rotate_right" that takes deque as Deque[Any] and n as Integer returns Deque[Any]`
- `Process called "shift_left" that takes deque as Deque[Any] and n as Integer returns Deque[Any]`
- `Process called "shift_right" that takes deque as Deque[Any] and n as Integer returns Deque[Any]`

## Bulk Operations

- `Process called "extend_front" that takes deque as Deque[Any] and values as List[Any] returns Deque[Any]`
- `Process called "extend_back" that takes deque as Deque[Any] and values as List[Any] returns Deque[Any]`
- `Process called "clear" that takes deque as Deque[Any] returns Deque[Any]`
- `Process called "copy" that takes deque as Deque[Any] returns Deque[Any]`

## Slicing and Indexing

- `Process called "get_at_index" that takes deque as Deque[Any] and index as Integer returns Any`
- `Process called "set_at_index" that takes deque as Deque[Any] and index as Integer and value as Any returns Deque[Any]`
- `Process called "slice_deque" that takes deque as Deque[Any] and start as Integer and end as Integer returns Deque[Any]`
- `Process called "reverse" that takes deque as Deque[Any] returns Deque[Any]`

## Searching and Filtering

- `Process called "index_of" that takes deque as Deque[Any] and value as Any returns Integer`
- `Process called "index_of_from" that takes deque as Deque[Any] and value as Any and start as Integer returns Integer`
- `Process called "count" that takes deque as Deque[Any] and value as Any returns Integer`
- `Process called "contains" that takes deque as Deque[Any] and value as Any returns Boolean`
- `Process called "filter" that takes deque as Deque[Any] and predicate as Process returns Deque[Any]`
- `Process called "map" that takes deque as Deque[Any] and transform as Process returns Deque[Any]`

## Sorting and Ordering

- `Process called "sort" that takes deque as Deque[Any] returns Deque[Any]`
- `Process called "sort_with_key" that takes deque as Deque[Any] and key_func as Process returns Deque[Any]`
- `Process called "sort_reverse" that takes deque as Deque[Any] returns Deque[Any]`
- `Process called "is_sorted" that takes deque as Deque[Any] returns Boolean`
- `Process called "is_sorted_reverse" that takes deque as Deque[Any] returns Boolean`

## Statistical Operations

- `Process called "min_element" that takes deque as Deque[Any] returns Any`
- `Process called "max_element" that takes deque as Deque[Any] returns Any`
- `Process called "sum_elements" that takes deque as Deque[Any] returns Number`
- `Process called "average" that takes deque as Deque[Any] returns Number`

## Memory and Performance Optimizations

- `Process called "compact" that takes deque as Deque[Any] returns Deque[Any]`
- `Process called "deduplicate" that takes deque as Deque[Any] returns Deque[Any]`
- `Process called "shuffle" that takes deque as Deque[Any] returns Deque[Any]`

## Utility Operations

- `Process called "to_list" that takes deque as Deque[Any] returns List[Any]`

## Usage Examples

### Basic Deque Operations
```runa
Let d be create_deque()
Let d be add_to_front with deque as d and value as "first"
Let d be add_to_back with deque as d and value as "last"
Let (d, front_value) be remove_from_front with deque as d
Let (d, back_value) be remove_from_back with deque as d
```

### Bounded Deque Operations
```runa
Let d be create_deque_with_maxlen with maxlen as 3
Let d be add_to_back with deque as d and value as "a"
Let d be add_to_back with deque as d and value as "b"
Let d be add_to_back with deque as d and value as "c"
Let d be add_to_back with deque as d and value as "d"  Note: "a" is automatically removed
```

### Rotation Operations
```runa
Let d be from_list with items as list containing 1, 2, 3, 4, 5
Let d be rotate with deque as d and n as 2  Note: Rotate right by 2
Let d be rotate_left with deque as d and n as 1  Note: Rotate left by 1
```

### Bulk Operations
```runa
Let d be create_deque()
Let d be extend_front with deque as d and values as list containing "a", "b", "c"
Let d be extend_back with deque as d and values as list containing "x", "y", "z"
```

### Slicing and Indexing
```runa
Let d be from_list with items as list containing 1, 2, 3, 4, 5
Let value be get_at_index with deque as d and index as 2
Let d be set_at_index with deque as d and index as 1 and value as 99
Let sliced be slice_deque with deque as d and start as 1 and end as 4
```

### Searching and Filtering
```runa
Let d be from_list with items as list containing "apple", "banana", "apple", "cherry"
Let index be index_of with deque as d and value as "banana"
Let count be count with deque as d and value as "apple"
Let filtered be filter with deque as d and predicate as lambda x: length of x is greater than 5
```

### Sorting Operations
```runa
Let d be from_list with items as list containing 3, 1, 4, 1, 5
Let d be sort with deque as d
Let is_sorted_val be is_sorted with deque as d
Let d be sort_reverse with deque as d
```

### Statistical Operations
```runa
Let d be from_list with items as list containing 1, 2, 3, 4, 5
Let min_val be min_element with deque as d
Let max_val be max_element with deque as d
Let sum_val be sum_elements with deque as d
Let avg_val be average with deque as d
```

### Memory Optimizations
```runa
Let d be from_list with items as list containing 1, None, 2, None, 3
Let compacted be compact with deque as d  Note: Removes None values
Let d be from_list with items as list containing 1, 2, 1, 3, 2
Let unique be deduplicate with deque as d  Note: Removes duplicates
Let shuffled be shuffle with deque as d  Note: Randomizes order
```

## Examples

A complete, idiomatic example is available at:

    runa/examples/basic/deque_example.runa

## Testing

A comprehensive Runa-based test file for the deque module is located at:

    runa/tests/stdlib/test_deque.runa

This file exercises all deque operations using idiomatic Runa assertions and error handling. All standard library modules have corresponding Runa test files in this directory, ensuring production-ready quality and verifiability.

## Performance Characteristics

- **Time Complexity**: 
  - Front/back operations: O(1) amortized
  - Index access: O(1)
  - Rotation: O(n)
  - Sorting: O(n log n)
- **Space Complexity**: O(n) for storage
- **Memory Efficiency**: Automatic truncation for bounded deques
- **Thread Safety**: Operations are not thread-safe by default; use appropriate synchronization for concurrent access

## Use Cases

- **Sliding Window**: Use bounded deques for maintaining fixed-size windows
- **Undo/Redo**: Use for command history with automatic truncation
- **Queue Management**: Efficient FIFO/LIFO operations
- **Data Processing**: Rotation and bulk operations for data transformation
- **Caching**: Bounded deques for LRU-like behavior 