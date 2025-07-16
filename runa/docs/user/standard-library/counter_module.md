# Runa Standard Library: Counter Module

## Overview

The `collections/counter` module provides a comprehensive frequency counter (multiset) for tracking the number of occurrences of elements, with natural language operations for incrementing, decrementing, querying counts, and advanced statistical analysis. The module includes both standard counters and weighted counters for sophisticated data analysis.

## Features

- **Core Operations**: Increment, decrement, get/set counts
- **Weighted Counting**: Support for non-integer weights and normalization
- **Statistical Analysis**: Mean, median, variance, entropy, Gini coefficient
- **Similarity Metrics**: Cosine similarity, Jaccard similarity, distance calculations
- **Advanced Filtering**: Percentile-based, entropy-based, and custom filtering
- **Mathematical Operations**: Addition, subtraction, multiplication, division of counters
- **Transformation**: Key/value mapping, grouping, normalization
- **Memory Optimization**: Compaction, pruning, merging similar keys

## Types

### Counter[T]
Standard frequency counter with integer counts.

### WeightedCounter[T]
Advanced counter supporting floating-point weights and normalization.

## Core API

### Creation
- `Process called "create_counter" that returns Counter[Any]`
- `Process called "create_weighted_counter" that returns WeightedCounter[Any]`
- `Process called "from_list" that takes items as List[Any] returns Counter[Any]`
- `Process called "from_dict" that takes counts_dict as Dictionary[Any, Integer] returns Counter[Any]`

### Basic Operations
- `Process called "increment" that takes counter as Counter[Any] and key as Any returns Counter[Any]`
- `Process called "increment_by" that takes counter as Counter[Any] and key as Any and amount as Integer returns Counter[Any]`
- `Process called "increment_weighted" that takes counter as WeightedCounter[Any] and key as Any and weight as Number returns WeightedCounter[Any]`
- `Process called "decrement" that takes counter as Counter[Any] and key as Any returns Counter[Any]`
- `Process called "decrement_by" that takes counter as Counter[Any] and key as Any and amount as Integer returns Counter[Any]`
- `Process called "get_count" that takes counter as Counter[Any] and key as Any returns Integer`
- `Process called "get_weight" that takes counter as WeightedCounter[Any] and key as Any returns Number`
- `Process called "set_count" that takes counter as Counter[Any] and key as Any and count as Integer returns Counter[Any]`
- `Process called "set_weight" that takes counter as WeightedCounter[Any] and key as Any and weight as Number returns WeightedCounter[Any]`

### Query Operations
- `Process called "most_common" that takes counter as Counter[Any] and n as Integer returns List[Any]`
- `Process called "most_common_with_counts" that takes counter as Counter[Any] and n as Integer returns List[Tuple[Any, Integer]]`
- `Process called "least_common" that takes counter as Counter[Any] and n as Integer returns List[Any]`
- `Process called "total_count" that takes counter as Counter[Any] returns Integer`
- `Process called "total_weight" that takes counter as WeightedCounter[Any] returns Number`
- `Process called "unique_elements" that takes counter as Counter[Any] returns Integer`
- `Process called "is_empty" that takes counter as Counter[Any] returns Boolean`
- `Process called "has_element" that takes counter as Counter[Any] and key as Any returns Boolean`

## Advanced Statistical Operations

### Information Theory
- `Process called "entropy" that takes counter as Counter[Any] returns Number`
- `Process called "normalized_entropy" that takes counter as Counter[Any] returns Number`

### Distribution Analysis
- `Process called "mean_count" that takes counter as Counter[Any] returns Number`
- `Process called "median_count" that takes counter as Counter[Any] returns Number`
- `Process called "mode_count" that takes counter as Counter[Any] returns Integer`
- `Process called "count_variance" that takes counter as Counter[Any] returns Number`
- `Process called "count_std_dev" that takes counter as Counter[Any] returns Number`
- `Process called "gini_coefficient" that takes counter as Counter[Any] returns Number`
- `Process called "diversity_index" that takes counter as Counter[Any] returns Number`

## Normalization and Scaling

- `Process called "normalize" that takes counter as Counter[Any] returns WeightedCounter[Any]`
- `Process called "scale_by" that takes counter as Counter[Any] and factor as Number returns Counter[Any]`
- `Process called "log_scale" that takes counter as Counter[Any] returns Counter[Any]`

## Similarity and Distance Metrics

- `Process called "cosine_similarity" that takes counter1 as Counter[Any] and counter2 as Counter[Any] returns Number`
- `Process called "jaccard_similarity" that takes counter1 as Counter[Any] and counter2 as Counter[Any] returns Number`
- `Process called "euclidean_distance" that takes counter1 as Counter[Any] and counter2 as Counter[Any] returns Number`
- `Process called "manhattan_distance" that takes counter1 as Counter[Any] and counter2 as Counter[Any] returns Number`

## Mathematical Operations

- `Process called "add_counters" that takes counter1 as Counter[Any] and counter2 as Counter[Any] returns Counter[Any]`
- `Process called "subtract_counters" that takes counter1 as Counter[Any] and counter2 as Counter[Any] returns Counter[Any]`
- `Process called "intersection" that takes counter1 as Counter[Any] and counter2 as Counter[Any] returns Counter[Any]`
- `Process called "union" that takes counter1 as Counter[Any] and counter2 as Counter[Any] returns Counter[Any]`
- `Process called "multiply_counters" that takes counter1 as Counter[Any] and counter2 as Counter[Any] returns Counter[Any]`
- `Process called "divide_counters" that takes counter1 as Counter[Any] and counter2 as Counter[Any] returns Counter[Any]`

## Advanced Filtering and Selection

- `Process called "filter_by_count" that takes counter as Counter[Any] and min_count as Integer returns Counter[Any]`
- `Process called "filter_by_key" that takes counter as Counter[Any] and predicate as Process returns Counter[Any]`
- `Process called "top_k" that takes counter as Counter[Any] and k as Integer returns Counter[Any]`
- `Process called "bottom_k" that takes counter as Counter[Any] and k as Integer returns Counter[Any]`
- `Process called "filter_by_percentile" that takes counter as Counter[Any] and percentile as Number returns Counter[Any]`
- `Process called "filter_by_entropy" that takes counter as Counter[Any] and min_entropy as Number returns Counter[Any]`

## Transformation Operations

- `Process called "map_keys" that takes counter as Counter[Any] and transform as Process returns Counter[Any]`
- `Process called "map_values" that takes counter as Counter[Any] and transform as Process returns Counter[Any]`
- `Process called "group_by" that takes counter as Counter[Any] and group_func as Process returns Counter[Any]`

## Memory and Performance Optimizations

- `Process called "compact" that takes counter as Counter[Any] returns Counter[Any]`
- `Process called "prune_small_counts" that takes counter as Counter[Any] and threshold as Integer returns Counter[Any]`
- `Process called "merge_similar_keys" that takes counter as Counter[Any] and similarity_func as Process and threshold as Number returns Counter[Any]`

## Utility Operations

- `Process called "clear" that takes counter as Counter[Any] returns Counter[Any]`
- `Process called "copy" that takes counter as Counter[Any] returns Counter[Any]`
- `Process called "to_dict" that takes counter as Counter[Any] returns Dictionary[Any, Integer]`

## Usage Examples

### Basic Counter Operations
```runa
Let c be create_counter()
Call increment with counter as c and key as "apple"
Call increment with counter as c and key as "banana"
Call increment with counter as c and key as "apple"
Assert get_count with counter as c and key as "apple" is equal to 2
```

### Weighted Counter Operations
```runa
Let wc be create_weighted_counter()
Call increment_weighted with counter as wc and key as "A" and weight as 1.5
Call increment_weighted with counter as wc and key as "B" and weight as 2.3
Let normalized be normalize with counter as wc
```

### Statistical Analysis
```runa
Let c be from_list with items as list containing "a", "a", "b", "c", "a", "b"
Let entropy_val be entropy with counter as c
Let gini_val be gini_coefficient with counter as c
Let diversity be diversity_index with counter as c
```

### Similarity Calculations
```runa
Let c1 be from_list with items as list containing "a", "a", "b", "c"
Let c2 be from_list with items as list containing "a", "b", "b", "d"
Let similarity be cosine_similarity with counter1 as c1 and counter2 as c2
Let distance be euclidean_distance with counter1 as c1 and counter2 as c2
```

### Advanced Filtering
```runa
Let c be from_list with items as list containing 1, 1, 2, 3, 4, 5, 5, 5
Let top_3 be top_k with counter as c and k as 3
Let filtered be filter_by_percentile with counter as c and percentile as 75
```

### Mathematical Operations
```runa
Let c1 be from_list with items as list containing "a", "a", "b"
Let c2 be from_list with items as list containing "a", "b", "c"
Let sum_counter be add_counters with counter1 as c1 and counter2 as c2
Let intersection_counter be intersection with counter1 as c1 and counter2 as c2
```

## Examples

A complete, idiomatic example is available at:

    runa/examples/basic/counter_example.runa

## Testing

A comprehensive Runa-based test file for the counter module is located at:

    runa/tests/stdlib/test_counter.runa

This file exercises all counter operations using idiomatic Runa assertions and error handling. All standard library modules have corresponding Runa test files in this directory, ensuring production-ready quality and verifiability.

## Performance Characteristics

- **Time Complexity**: Most operations are O(n) where n is the number of unique elements
- **Space Complexity**: O(n) for storage of unique elements and their counts
- **Memory Efficiency**: Automatic compaction and pruning operations available
- **Thread Safety**: Operations are not thread-safe by default; use appropriate synchronization for concurrent access 