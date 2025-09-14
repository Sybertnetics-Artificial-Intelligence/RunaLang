# Runa Collection Syntax Reference

## Overview

Runa supports two syntax modes for collection literals: **Canonical** (natural language) and **Technical** (compact symbols). Both modes are equivalent and compile to identical bytecode. The compiler's type inference engine automatically determines collection types from their contents.

## List Types

### Canonical Syntax
```runa
Note: Basic list creation
Let my_list be a list of Integers, containing 1, 2, and 3

Note: Type inference from contents
Let numbers be a list containing 1, 2, 3, 4, 5
Note: Compiler infers: List[Integer]

Let names be a list containing "Alice", "Bob", "Charlie"
Note: Compiler infers: List[String]

Let mixed be a list containing 1, "hello", 3.14
Note: Compiler infers: List[Any] - requires explicit handling
```

### Technical Syntax
```runa
Note: Compact list creation
my_list = [1, 2, 3]
Note: Compiler infers: List[Integer]

numbers = [1, 2, 3, 4, 5]
names = ["Alice", "Bob", "Charlie"]
mixed = [1, "hello", 3.14]  Note: List[Any]
```

### Type-Safe Multi-Type Lists

#### The Any Type (Discouraged)
```runa
Note: Canonical - explicit Any type
Let mixed_list as List[Any] be a list containing 1, "hello", 3.14

Note: Technical
mixed_list: List[Any] = [1, "hello", 3.14]
```

#### Union Types (Recommended)
```runa
Note: Define union type first
Type StringIntFloat is String OR Integer OR Float

Note: Canonical - type-safe mixed list
Let mixed_list as List[StringIntFloat] be a list containing 1, "hello", 3.14

Note: Technical
mixed_list: List[StringIntFloat] = [1, "hello", 3.14]
```

## Dictionary Types

### Canonical Syntax
```runa
Note: Basic dictionary creation
Let user be a dictionary containing:
    "name" as "Alice",
    "age" as 30,
    "is_active" as true
End Dictionary

Note: Type inference
Let scores be a dictionary containing:
    "Alice" as 95,
    "Bob" as 87,
    "Charlie" as 92
End Dictionary
Note: Compiler infers: Dictionary[String, Integer]
```

### Technical Syntax
```runa
Note: Compact dictionary creation
user = {
    "name": "Alice",
    "age": 30,
    "is_active": true
}

scores = {
    "Alice": 95,
    "Bob": 87,
    "Charlie": 92
}
Note: Compiler infers: Dictionary[String, Integer]
```

## Array Types (Fixed-Size)

### Canonical Syntax
```runa
Note: Fixed-size array
Let my_vector be an Array of 3 Floats

Note: Array with initialization
Let coordinates be an Array of 3 Floats containing 1.0, 2.0, 3.0
Note: Compiler infers: Array[Float, 3]
```

### Technical Syntax
```runa
Note: Fixed-size array
my_vector: Array[Float, 3]

Note: Array with initialization
coordinates: Array[Float, 3] = [1.0, 2.0, 3.0]
```

## Collection Access

### Canonical Syntax
```runa
Note: List/Array access
Let first_item be my_list at index 0
Let last_item be my_list at index (length of my_list minus 1)

Note: Dictionary access
Let user_name be user at key "name"
Let user_age be user["age"]  Note: Both forms supported

Note: Length operations
Let size be length of my_list
Let count be number of items in scores
```

### Technical Syntax
```runa
Note: List/Array access
first_item = my_list[0]
last_item = my_list[my_list.length() - 1]

Note: Dictionary access
user_name = user["name"]
user_age = user.get("age")  Note: Safe access method

Note: Length operations
size = my_list.length()
count = scores.size()
```

## Type Inference Rules

### Single-Type Collections
The compiler analyzes all elements and infers the most specific common type:

```runa
Note: All integers -> List[Integer]
Let nums = [1, 2, 3]

Note: All strings -> List[String]
Let words = ["hello", "world"]

Note: Mixed numeric -> List[Float] (integers promoted)
Let values = [1, 2.5, 3]
```

### Multi-Type Collections
When elements have incompatible types, the compiler infers the most general type:

```runa
Note: Incompatible types -> List[Any]
Let mixed = [1, "hello", true]

Note: Compatible types -> Union type (when explicitly defined)
Type NumberOrString is Integer OR String
Let compatible as List[NumberOrString] = [1, "hello", 42]
```

## Advanced Collection Patterns

### List Comprehensions

#### Canonical Syntax
```runa
Note: List comprehension
Let squares be a list containing (x multiplied by x) for each x in numbers where x is greater than 0

Note: Nested comprehension
Let matrix be a list containing
    (a list containing y for each y from 1 to 3)
    for each x from 1 to 3
```

#### Technical Syntax
```runa
Note: List comprehension
squares = [x * x for x in numbers if x > 0]

Note: Nested comprehension
matrix = [[y for y in range(1, 4)] for x in range(1, 4)]
```

### Dictionary Comprehensions

#### Canonical Syntax
```runa
Note: Dictionary comprehension
Let word_lengths be a dictionary containing
    word as (length of word)
    for each word in words
    where (length of word) is greater than 3
```

#### Technical Syntax
```runa
Note: Dictionary comprehension
word_lengths = {word: len(word) for word in words if len(word) > 3}
```

## Collection Methods and Operations

### Common Operations

#### Canonical Syntax
```runa
Note: List operations
Add item to end of my_list
Insert item at index 0 in my_list
Remove item from my_list
Let item be first item in my_list
Let item be last item in my_list

Note: Dictionary operations
Set user at key "email" to "alice@example.com"
Remove key "temp" from user
Let keys be all keys in user
Let values be all values in user
```

#### Technical Syntax
```runa
Note: List operations
my_list.append(item)
my_list.insert(0, item)
my_list.remove(item)
item = my_list.first()
item = my_list.last()

Note: Dictionary operations
user["email"] = "alice@example.com"
user.remove("temp")
keys = user.keys()
values = user.values()
```

## Type Annotations

### Explicit Type Annotations

#### Canonical Syntax
```runa
Note: Explicit list type
Let scores as List[Integer] be a list containing 95, 87, 92

Note: Explicit dictionary type
Let user_data as Dictionary[String, Any] be a dictionary containing:
    "name" as "Alice",
    "age" as 30
End Dictionary

Note: Complex nested type
Let matrix as List[List[Float]] be a list containing:
    a list containing 1.0, 2.0, 3.0,
    a list containing 4.0, 5.0, 6.0
End List
```

#### Technical Syntax
```runa
Note: Explicit list type
scores: List[Integer] = [95, 87, 92]

Note: Explicit dictionary type
user_data: Dictionary[String, Any] = {
    "name": "Alice",
    "age": 30
}

Note: Complex nested type
matrix: List[List[Float]] = [
    [1.0, 2.0, 3.0],
    [4.0, 5.0, 6.0]
]
```

## Performance Considerations

### Memory Layout
- **Lists**: Dynamic arrays with amortized O(1) append
- **Arrays**: Fixed-size, stack-allocated when size is compile-time constant
- **Dictionaries**: Hash tables with O(1) average access time

### Type Inference Performance
- Type inference is performed at compile time - no runtime overhead
- The compiler caches inference results for repeated patterns
- Complex union types may increase compilation time but have no runtime cost

### Collection Selection Guidelines

```runa
Note: Use Arrays for fixed-size numeric data
Let vertex as Array[Float, 3] = [x, y, z]

Note: Use Lists for dynamic collections
Let items be a list containing initial_items
Add new_item to end of items

Note: Use Dictionaries for key-value mappings
Let cache be a dictionary containing:
    key as computed_value
End Dictionary
```

## Error Handling

### Type Errors
```runa
Note: This will cause a compile-time error:
Let numbers as List[Integer] = [1, "two", 3]
Note: Error: Cannot assign String "two" to List[Integer]

Note: This requires explicit handling:
Let mixed as List[Any] = [1, "two", 3]
Note: Runtime type checking required when accessing elements
```

### Runtime Errors
```runa
Note: Index out of bounds
Let item be my_list at index 999  Note: Runtime error if index >= length

Note: Safe access patterns
If index is less than (length of my_list):
    Let item be my_list at index index
Otherwise:
    Display "Index out of bounds"
End If
```

## Best Practices

### 1. Prefer Type Inference
```runa
Note: Good - let the compiler infer
Let numbers = [1, 2, 3, 4, 5]

Note: Unnecessary - type is obvious
Let numbers as List[Integer] = [1, 2, 3, 4, 5]
```

### 2. Use Union Types for Mixed Data
```runa
Note: Good - explicit and type-safe
Type JsonValue is String OR Integer OR Float OR Boolean OR None
Let json_array as List[JsonValue] = [1, "hello", 3.14, true, None]

Note: Avoid - requires runtime type checking everywhere
Let json_array as List[Any] = [1, "hello", 3.14, true, None]
```

### 3. Choose Appropriate Collection Types
```runa
Note: Good - fixed-size data
Let rgb_color as Array[Float, 3] = [1.0, 0.5, 0.2]

Note: Good - dynamic data
Let user_scores be a list containing initial_scores
Add new_score to end of user_scores

Note: Good - key-value relationships
Let user_preferences be a dictionary containing:
    "theme" as "dark",
    "language" as "en"
End Dictionary
```

## Syntax Conversion Table

| Operation | Canonical | Technical |
|-----------|-----------|-----------|
| List literal | `a list containing 1, 2, 3` | `[1, 2, 3]` |
| Dict literal | `a dictionary containing: "key" as value End Dictionary` | `{"key": value}` |
| Array type | `Array of 3 Floats` | `Array[Float, 3]` |
| Index access | `list at index 0` | `list[0]` |
| Length | `length of list` | `list.length()` |
| Dict access | `dict at key "name"` | `dict["name"]` |
| Dict keys | `all keys in dict` | `dict.keys()` |
| List append | `Add item to end of list` | `list.append(item)` |
| List insert | `Insert item at index 0 in list` | `list.insert(0, item)` |

Both syntax forms are fully interchangeable and compile to identical bytecode. Choose the form that best fits your project's coding standards and developer preferences.