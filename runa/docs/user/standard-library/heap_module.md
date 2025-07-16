# Runa Standard Library: Heap Module

## Overview

The `collections/heap` module provides comprehensive heap/priority queue functionality with natural language operations for pushing, popping, peeking, and heapifying elements. Supports both min-heap and max-heap with custom comparators, bulk operations, and advanced heap algorithms.

## Features

- **Core Operations**: Push, pop, peek with priority support
- **Heap Types**: Min-heap, max-heap, and custom comparator heaps
- **Bulk Operations**: Heapify, merge heaps, extend with values
- **K-Element Operations**: Extract k-largest/smallest elements
- **Advanced Operations**: Replace, pushpop, update priority, remove at index
- **Validation**: Heap integrity checking and debugging
- **Performance Optimizations**: Efficient heap maintenance algorithms
- **Thread Safety**: Operations are not thread-safe by default

## Types

### Heap[T]
Priority queue with configurable comparator and heap type.

### HeapNode[T]
Node structure for priority-based heaps with timestamp support.

## Core API

### Creation
- `Process called "create_heap" that returns Heap[Any]`
- `Process called "create_max_heap" that returns Heap[Any]`
- `Process called "create_heap_with_comparator" that takes comparator as Process returns Heap[Any]`

### Basic Operations
- `Process called "push" that takes heap as Heap[Any] and value as Any returns Heap[Any]`
- `Process called "push_with_priority" that takes heap as Heap[Any] and value as Any and priority as Number returns Heap[Any]`
- `Process called "pop" that takes heap as Heap[Any] returns (Heap[Any], Any)`
- `Process called "pop_with_priority" that takes heap as Heap[Any] returns (Heap[Any], Any, Number)`
- `Process called "peek" that takes heap as Heap[Any] returns Any`
- `Process called "peek_with_priority" that takes heap as Heap[Any] returns (Any, Number)`

### Query Operations
- `Process called "heap_length" that takes heap as Heap[Any] returns Integer`
- `Process called "heap_is_empty" that takes heap as Heap[Any] returns Boolean`
- `Process called "get_heap_type" that takes heap as Heap[Any] returns String`
- `Process called "get_comparator" that takes heap as Heap[Any] returns Process`

## Heap Maintenance Operations

- `Process called "heapify_up" that takes heap as Heap[Any] and index as Integer returns Heap[Any]`
- `Process called "heapify_up_with_comparator" that takes heap as Heap[Any] and index as Integer returns Heap[Any]`
- `Process called "heapify_down" that takes heap as Heap[Any] and index as Integer returns Heap[Any]`
- `Process called "heapify_down_with_comparator" that takes heap as Heap[Any] and index as Integer returns Heap[Any]`

## Bulk Operations

- `Process called "heapify" that takes items as List[Any] returns Heap[Any]`
- `Process called "heapify_max" that takes items as List[Any] returns Heap[Any]`
- `Process called "heapify_with_comparator" that takes items as List[Any] and comparator as Process returns Heap[Any]`
- `Process called "merge_heaps" that takes heap1 as Heap[Any] and heap2 as Heap[Any] returns Heap[Any]`
- `Process called "extend" that takes heap as Heap[Any] and values as List[Any] returns Heap[Any]`

## K-Element Operations

- `Process called "k_largest" that takes heap as Heap[Any] and k as Integer returns List[Any]`
- `Process called "k_smallest" that takes heap as Heap[Any] and k as Integer returns List[Any]`
- `Process called "nlargest" that takes items as List[Any] and n as Integer returns List[Any]`
- `Process called "nsmallest" that takes items as List[Any] and n as Integer returns List[Any]`

## Heap Validation and Debugging

- `Process called "is_valid_heap" that takes heap as Heap[Any] returns Boolean`
- `Process called "heap_to_list" that takes heap as Heap[Any] returns List[Any]`
- `Process called "heap_to_sorted_list" that takes heap as Heap[Any] returns List[Any]`
- `Process called "copy_heap" that takes heap as Heap[Any] returns Heap[Any]`

## Advanced Operations

- `Process called "replace" that takes heap as Heap[Any] and value as Any returns (Heap[Any], Any)`
- `Process called "pushpop" that takes heap as Heap[Any] and value as Any returns (Heap[Any], Any)`
- `Process called "update_priority" that takes heap as Heap[Any] and index as Integer and new_priority as Number returns Heap[Any]`
- `Process called "remove_at_index" that takes heap as Heap[Any] and index as Integer returns Heap[Any]`

## Utility Operations

- `Process called "clear" that takes heap as Heap[Any] returns Heap[Any]`

## Usage Examples

### Basic Heap Operations
```runa
Let h be create_heap()
Let h be push with heap as h and value as 5
Let h be push with heap as h and value as 3
Let h be push with heap as h and value as 7
Let (h, min_val) be pop with heap as h
Assert min_val is equal to 3
```

### Max Heap Operations
```runa
Let h be create_max_heap()
Let h be push with heap as h and value as 5
Let h be push with heap as h and value as 3
Let h be push with heap as h and value as 7
Let (h, max_val) be pop with heap as h
Assert max_val is equal to 7
```

### Priority-Based Heap
```runa
Let h be create_heap()
Let h be push_with_priority with heap as h and value as "task1" and priority as 3
Let h be push_with_priority with heap as h and value as "task2" and priority as 1
Let h be push_with_priority with heap as h and value as "task3" and priority as 2
Let (h, value, priority) be pop_with_priority with heap as h
Assert value is equal to "task2"
Assert priority is equal to 1
```

### Custom Comparator
```runa
Let comparator be lambda a and b: length of a is less than length of b
Let h be create_heap_with_comparator with comparator as comparator
Let h be push with heap as h and value as "longer"
Let h be push with heap as h and value as "short"
Let h be push with heap as h and value as "medium"
Let (h, shortest) be pop with heap as h
Assert shortest is equal to "short"
```

### Bulk Operations
```runa
Let items be list containing 5, 3, 7, 1, 9, 2
Let h be heapify with items as items
Let (h, min_val) be pop with heap as h
Assert min_val is equal to 1

Let h1 be heapify with items as list containing 1, 3, 5
Let h2 be heapify with items as list containing 2, 4, 6
Let merged be merge_heaps with heap1 as h1 and heap2 as h2
Assert heap_length with heap as merged is equal to 6
```

### K-Element Operations
```runa
Let items be list containing 5, 3, 7, 1, 9, 2, 8, 4, 6
Let largest_3 be nlargest with items as items and n as 3
Assert largest_3[0] is equal to 9
Assert largest_3[1] is equal to 8
Assert largest_3[2] is equal to 7

Let smallest_3 be nsmallest with items as items and n as 3
Assert smallest_3[0] is equal to 1
Assert smallest_3[1] is equal to 2
Assert smallest_3[2] is equal to 3
```

### Advanced Operations
```runa
Let h be heapify with items as list containing 1, 3, 5, 7, 9
Let (h, old_val) be replace with heap as h and value as 2
Assert old_val is equal to 1

Let h be heapify with items as list containing 1, 3, 5
Let (h, result) be pushpop with heap as h and value as 0
Assert result is equal to 0

Let h be heapify with items as list containing 1, 3, 5, 7, 9
Let h be update_priority with heap as h and index as 2 and new_priority as 0
Let (h, value) be pop with heap as h
Assert value is equal to 5
```

### Heap Validation
```runa
Let h be heapify with items as list containing 1, 3, 5, 7, 9
Assert is_valid_heap with heap as h is equal to true

Let sorted_list be heap_to_sorted_list with heap as h
Assert sorted_list[0] is equal to 1
Assert sorted_list[1] is equal to 3
Assert sorted_list[2] is equal to 5
```

## Examples

A complete, idiomatic example is available at:

    runa/examples/basic/heap_example.runa

## Testing

A comprehensive Runa-based test file for the heap module is located at:

    runa/tests/stdlib/test_heap.runa

This file exercises all heap operations using idiomatic Runa assertions and error handling. All standard library modules have corresponding Runa test files in this directory, ensuring production-ready quality and verifiability.

## Performance Characteristics

- **Time Complexity**:
  - Push/Pop: O(log n)
  - Peek: O(1)
  - Heapify: O(n)
  - Merge: O(n + m)
  - K-largest/smallest: O(k log n)
- **Space Complexity**: O(n) for storage
- **Memory Efficiency**: In-place heapification and efficient memory usage
- **Thread Safety**: Operations are not thread-safe by default; use appropriate synchronization for concurrent access

## Use Cases

- **Priority Queues**: Task scheduling, event processing
- **Top-K Queries**: Finding largest/smallest elements
- **Sorting**: Heap sort implementation
- **Graph Algorithms**: Dijkstra's, Prim's algorithms
- **Data Stream Processing**: Maintaining running statistics
- **Resource Management**: CPU scheduling, memory allocation 