# Runa Standard Library: Set Module

## Overview

The `collections/set` module provides comprehensive set operations for creating, manipulating, and querying unordered collections of unique elements. Idiomatic Runa code uses set literals, comprehensions, and helper processes for advanced or programmatic use cases.

The module includes advanced features such as:
- Core set operations (add, remove, contains, clear)
- Bulk operations and batch processing
- Set theory operations (union, intersection, difference)
- Searching and filtering operations
- Set transformations and mapping
- Performance optimizations
- Thread-safe operations (when supported)

## Core Operations

### Creation and Basic Operations
- `Process called "from_list" that takes elements as List[Any] returns Set[Any]`
- `Process called "create_empty_set" that returns Set[Any]`
- `Process called "add" that takes s as Set[Any] and value as Any returns Set[Any]`
- `Process called "add_multiple" that takes s as Set[Any] and values as List[Any] returns Set[Any]`
- `Process called "remove" that takes s as Set[Any] and value as Any returns Set[Any]`
- `Process called "remove_safe" that takes s as Set[Any] and value as Any returns Set[Any]`
- `Process called "discard" that takes s as Set[Any] and value as Any returns Set[Any]`
- `Process called "pop" that takes s as Set[Any] returns (Set[Any], Any)`
- `Process called "clear" that takes s as Set[Any] returns Set[Any]`
- `Process called "copy" that takes s as Set[Any] returns Set[Any]`
- `Process called "deep_copy" that takes s as Set[Any] returns Set[Any]`

### Query and Analysis
- `Process called "contains" that takes s as Set[Any] and value as Any returns Boolean`
- `Process called "size" that takes s as Set[Any] returns Integer`
- `Process called "is_empty" that takes s as Set[Any] returns Boolean`
- `Process called "elements" that takes s as Set[Any] returns List[Any]`
- `Process called "has_element" that takes s as Set[Any] and value as Any returns Boolean`
- `Process called "is_subset" that takes s1 as Set[Any] and s2 as Set[Any] returns Boolean`
- `Process called "is_superset" that takes s1 as Set[Any] and s2 as Set[Any] returns Boolean`
- `Process called "is_proper_subset" that takes s1 as Set[Any] and s2 as Set[Any] returns Boolean`
- `Process called "is_proper_superset" that takes s1 as Set[Any] and s2 as Set[Any] returns Boolean`
- `Process called "is_disjoint" that takes s1 as Set[Any] and s2 as Set[Any] returns Boolean`

### Set Theory Operations
- `Process called "union" that takes s1 as Set[Any] and s2 as Set[Any] returns Set[Any]`
- `Process called "union_multiple" that takes sets as List[Set[Any]] returns Set[Any]`
- `Process called "intersection" that takes s1 as Set[Any] and s2 as Set[Any] returns Set[Any]`
- `Process called "intersection_multiple" that takes sets as List[Set[Any]] returns Set[Any]`
- `Process called "difference" that takes s1 as Set[Any] and s2 as Set[Any] returns Set[Any]`
- `Process called "difference_multiple" that takes sets as List[Set[Any]] returns Set[Any]`
- `Process called "symmetric_difference" that takes s1 as Set[Any] and s2 as Set[Any] returns Set[Any]`
- `Process called "complement" that takes s as Set[Any] and universe as Set[Any] returns Set[Any]`

### Bulk Operations
- `Process called "update" that takes s as Set[Any] and other as Set[Any] returns Set[Any]`
- `Process called "update_multiple" that takes s as Set[Any] and others as List[Set[Any]] returns Set[Any]`
- `Process called "intersection_update" that takes s as Set[Any] and other as Set[Any] returns Set[Any]`
- `Process called "intersection_update_multiple" that takes s as Set[Any] and others as List[Set[Any]] returns Set[Any]`
- `Process called "difference_update" that takes s as Set[Any] and other as Set[Any] returns Set[Any]`
- `Process called "difference_update_multiple" that takes s as Set[Any] and others as List[Set[Any]] returns Set[Any]`
- `Process called "symmetric_difference_update" that takes s as Set[Any] and other as Set[Any] returns Set[Any]`

### Filtering and Transformation
- `Process called "filter" that takes s as Set[Any] and predicate as Process returns Set[Any]`
- `Process called "filter_not" that takes s as Set[Any] and predicate as Process returns Set[Any]`
- `Process called "map" that takes s as Set[Any] and transform as Process returns Set[Any]`
- `Process called "flat_map" that takes s as Set[Any] and transform as Process returns Set[Any]`
- `Process called "partition" that takes s as Set[Any] and predicate as Process returns (Set[Any], Set[Any])`

### Utility Operations
- `Process called "from_keys" that takes keys as List[Any] returns Set[Any]`
- `Process called "from_values" that takes values as List[Any] returns Set[Any]`
- `Process called "group_by" that takes items as List[Any] and key_func as Process returns Dictionary[Any, Set[Any]]`
- `Process called "count_by" that takes items as List[Any] and key_func as Process returns Dictionary[Any, Integer]`
- `Process called "any" that takes s as Set[Any] and predicate as Process returns Boolean`
- `Process called "all" that takes s as Set[Any] and predicate as Process returns Boolean`
- `Process called "none" that takes s as Set[Any] and predicate as Process returns Boolean`
- `Process called "find" that takes s as Set[Any] and predicate as Process returns Optional[Any]`
- `Process called "find_all" that takes s as Set[Any] and predicate as Process returns Set[Any]`
- `Process called "min_element" that takes s as Set[Number] returns Optional[Number]`
- `Process called "max_element" that takes s as Set[Number] returns Optional[Number]`
- `Process called "sum_elements" that takes s as Set[Number] returns Number`
- `Process called "average_elements" that takes s as Set[Number] returns Number`
- `Process called "product_elements" that takes s as Set[Number] returns Number`
- `Process called "powerset" that takes s as Set[Any] returns Set[Set[Any]]`
- `Process called "cartesian_product" that takes s1 as Set[Any] and s2 as Set[Any] returns Set[Tuple[Any, Any]]`
- `Process called "cartesian_product_multiple" that takes sets as List[Set[Any]] returns Set[List[Any]]`

## Usage Examples

### Basic Set Operations
```runa
Let numbers be set containing 1, 2, 3, 4, 5

Note: Add and remove operations
Let numbers be add with s as numbers and value as 6
Let numbers be remove_safe with s as numbers and value as 3
Let (numbers, popped) be pop with s as numbers

Note: Query operations
Assert size of numbers is equal to 4
Assert numbers contains 2
Assert not numbers contains 3
```

### Set Theory Operations
```runa
Let set_a be set containing 1, 2, 3, 4, 5
Let set_b be set containing 4, 5, 6, 7, 8

Note: Basic set operations
Let union_set be union with s1 as set_a and s2 as set_b
Let intersection_set be intersection with s1 as set_a and s2 as set_b
Let difference_set be difference with s1 as set_a and s2 as set_b
Let symmetric_diff be symmetric_difference with s1 as set_a and s2 as set_b

Note: Set relationships
Assert is_subset with s1 as intersection_set and s2 as set_a
Assert is_disjoint with s1 as difference_set and s2 as set_b
```

### Advanced Operations
```runa
Let users be list containing:
    dictionary with "id" as 1 and "roles" as list containing "admin", "user"
    dictionary with "id" as 2 and "roles" as list containing "user", "moderator"
    dictionary with "id" as 3 and "roles" as list containing "admin", "moderator"

Note: Set operations on complex data
Let all_roles be set containing
For each user in users:
    Let user_roles be from_list with elements as user["roles"]
    Set all_roles to union with s1 as all_roles and s2 as user_roles

Let admin_users be set containing
For each user in users:
    If user["roles"] contains "admin":
        Add user["id"] to admin_users
```

### Functional Programming Patterns
```runa
Let data be set containing 1, 2, 3, 4, 5, 6, 7, 8, 9, 10

Note: Filtering and mapping
Let evens be filter with s as data and predicate as lambda x: remainder of x divided by 2 is equal to 0
Let squares be map with s as evens and transform as lambda x: x multiplied by x

Note: Partitioning and grouping
Let (small, large) be partition with s as data and predicate as lambda x: x is less than 5
Let grouped be group_by with items as elements of data and key_func as lambda x: remainder of x divided by 3
```

### Mathematical Set Operations
```runa
Let universe be set containing 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
Let subset_a be set containing 2, 4, 6, 8, 10
Let subset_b be set containing 1, 3, 5, 7, 9

Note: Complement operations
Let complement_a be complement with s as subset_a and universe as universe
Assert complement_a is equal to subset_b

Note: Powerset generation
Let powerset_a be powerset with s as set containing 1, 2, 3
Assert size of powerset_a is equal to 8

Note: Cartesian products
Let product be cartesian_product with s1 as set containing "a", "b" and s2 as set containing 1, 2
Assert size of product is equal to 4
```

## Performance Considerations

- **Immutable Operations**: Most operations return new sets, preserving immutability
- **Safe Operations**: Use `remove_safe`, `discard` to avoid exceptions in production code
- **Bulk Operations**: Use `update`, `add_multiple` for efficient batch modifications
- **Set Theory**: Use specialized operations like `union`, `intersection` for better performance than manual iteration

## Testing

A comprehensive Runa-based test file for the set module is located at:

    runa/tests/stdlib/test_set.runa

This file exercises all set operations using idiomatic Runa assertions and error handling. All standard library modules have corresponding Runa test files in this directory, ensuring production-ready quality and verifiability.

The test suite covers:
- Basic set operations and edge cases
- Error handling for invalid operations
- Performance characteristics of bulk operations
- Functional programming patterns and transformations
- Integration with other collection types 