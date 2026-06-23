# Runa Language Guide (v0.0.8.3)

This guide documents the Runa programming language syntax and features as implemented in v0.0.8.3. All examples are taken from actual working test files.

## Table of Contents
1. [Program Structure](#program-structure)
2. [Comments](#comments)
3. [Variables](#variables)
4. [Data Types](#data-types)
5. [Operators](#operators)
6. [Control Flow](#control-flow)
7. [Functions](#functions)
8. [Structs](#structs)
9. [Collections](#collections)
   - [Lists](#lists)
   - [Sets](#sets)
   - [Dictionaries](#dictionaries)
10. [Algebraic Data Types (ADTs)](#algebraic-data-types-adts)
   - [Variant Types](#variant-types)
   - [Pattern Matching](#pattern-matching)
11. [Inline Assembly](#inline-assembly)
12. [Imports](#imports)

---

## Program Structure

Every Runa program starts with a `main` function (called a "Process"):

```runa
Process called "main" returns Integer:
    Display "Hello, World!"
    Return 0
End Process
```

## Comments

Runa uses `Note:` for single-line comments and `Note: ... :End Note` for multi-line comments:

```runa
Note: This is a single-line comment
Let x be 10

Note:
This is a multi-line comment
that spans multiple lines
:End Note

Let y be 20
```

**IMPORTANT:** The `#` character is ONLY allowed inside inline assembly blocks. It is NOT a general comment syntax.

## Variables

### Declaration and Assignment

Variables are declared with `Let` and assigned with `Set`:

```runa
Let x be 10        Note: Declare and initialize
Set x to 20        Note: Assign new value
```

### Type Inference

Runa uses type inference - you don't specify types when declaring variables:

```runa
Let count be 0          Note: Integer inferred
Let flag be true        Note: Boolean inferred
```

### Compound Assignment

```runa
Let x be 10
Set x to x plus 5       Note: x = 15
Set x to x minus 3      Note: x = 12
Set x to x multiplied by 2   Note: x = 24
```

## Data Types

### Integers

```runa
Let positive be 42
Let negative be minus 10    Note: Negative numbers use 'minus' prefix
Let zero be 0
```

### Booleans

```runa
Let is_true be true
Let is_false be false
```

### Structs

See [Structs](#structs) section below.

### Collections

See [Collections](#collections) section below for Lists, Sets, and Dictionaries.

---

## Operators

### Arithmetic Operators

```runa
Let sum be a plus b
Let diff be a minus b
Let prod be a multiplied by b
Let quot be a divided by b
Let remainder be a modulo by c
```

### Comparison Operators

```runa
If x is equal to y:
If x is not equal to y:
If x is less than y:
If x is greater than y:
If x is less than or equal to y:
If x is greater than or equal to y:
If x is not less than y:
If x is not greater than y:
```

### Logical Operators

```runa
If x is equal to 5 and y is greater than 3:
    Display "Both conditions true"
End If

If x is equal to 5 or y is equal to 10:
    Display "At least one condition true"
End If
```

### Bitwise Operators

```runa
Let result be a bitwise and b
Let result be a bitwise or b
Let result be a bitwise xor b
Let result be a left shifted by 2
Let result be a right shifted by 2
```

---

## Control Flow

### If Statements

```runa
If x is equal to 10:
    Display "x is 10"
Otherwise:
    Display "x is not 10"
End If
```

### Otherwise If (Else If)

```runa
If value is equal to 1:
    Set result to 100
Otherwise If value is equal to 2:
    Set result to 200
Otherwise If value is equal to 3:
    Set result to 300
Otherwise:
    Set result to 999
End If
```

### While Loops

```runa
Let counter be 0
Let sum be 0
While counter is less than 5:
    Set sum to sum plus counter
    Set counter to counter plus 1
End While
```

### For Loops

```runa
Note: Basic For loop
Let sum be 0
For i from 1 to 5:
    Set sum to sum plus i
End For

Note: For loop with step
Let sum be 0
For j from 0 to 10 by 2:
    Set sum to sum plus j
End For
```

### For-Each Loops

```runa
Note: Iterate over a list
Let numbers be a list containing 1, 2, 3, 4, 5
For each num in numbers:
    Display integer_to_string(num)
End For
```

### Break and Continue

```runa
Let i be 0
While i is less than 10:
    Set i to i plus 1
    If i is equal to 5:
        Continue    Note: Skip to next iteration
    End If
    If i is equal to 8:
        Break      Note: Exit loop
    End If
    Display integer_to_string(i)
End While
```

---

## Functions

### Function Definition

Functions are called "Processes" in Runa:

```runa
Process called "add" takes x as Integer, y as Integer returns Integer:
    Let result be x plus y
    Return result
End Process
```

### Calling Functions

```runa
Let sum be add(5, 3)
Display integer_to_string(sum)
```

### Multiple Parameters

```runa
Process called "calculate" takes a as Integer, b as Integer, c as Integer returns Integer:
    Let temp be a plus b
    Let result be temp multiplied by c
    Return result
End Process
```

---

## Structs

### Defining a Struct

```runa
Type called "Point":
    x as Integer
    y as Integer
End Type
```

### Creating Struct Instances

```runa
Let p be a Point with x 10 and y 20
```

### Accessing Struct Fields

```runa
Note: Read field
Let px be the x of p

Note: Write field
Set the x of p to 100
```

### Nested Structs

```runa
Type called "Rectangle":
    top_left as Point
    bottom_right as Point
End Type

Let rect be a Rectangle with top_left p1 and bottom_right p2
Let x_coord be the x of the top_left of rect
Set the y of the bottom_right of rect to 50
```

---

## Collections

Runa provides three built-in collection types: **Lists**, **Sets**, and **Dictionaries**. All collection keywords (`list`, `set`, `dictionary`) are **context-aware** - they only act as keywords when followed by `containing` or `with:`, allowing you to use them as variable names elsewhere in your code.

### Lists

Lists are ordered, mutable sequences that can contain duplicate values.

#### List Literal Syntax

```runa
Note: Two equivalent syntaxes for list literals

Note: Syntax 1: "list containing"
Let numbers be list containing 10, 20, 30

Note: Syntax 2: "a list containing" (more natural English)
Let values be a list containing 1, 2, 3, 4, 5

Note: Lists with expressions
Let x be 5
Let y be 10
Let computed be a list containing x, y, x plus y

Note: Empty list (use runtime function)
Let empty be list_create()

Note: "list" can be used as a variable name
Let list be 42  Note: This works! "list" is context-aware
```

#### List Runtime Operations

```runa
Note: Create empty list
Let my_list be list_create()

Note: Append elements
list_append(my_list, 10)
list_append(my_list, 20)
list_append(my_list, 30)

Note: Get element by index (0-based)
Let first be list_get(my_list, 0)  Note: Returns 10

Note: Set element at index
list_set(my_list, 1, 100)  Note: Changes 20 to 100

Note: Insert element at index
list_insert(my_list, 1, 15)  Note: Insert 15 at position 1

Note: Remove element at index (returns removed value)
Let removed be list_remove(my_list, 0)

Note: Get list length
Let len be list_length(my_list)

Note: Clear all elements
list_clear(my_list)

Note: Destroy list and free memory
list_destroy(my_list)
```

#### Iterating Over Lists

```runa
Note: For-each loop over list
Let numbers be a list containing 1, 2, 3, 4, 5
Let sum be 0

For each num in numbers:
    Set sum to sum plus num
End For

Note: Nested for-each loops
Let list1 be a list containing 10, 20
Let list2 be a list containing 1, 2, 3

For each x in list1:
    For each y in list2:
        Display(integer_to_string(x plus y))
    End For
End For
```

---

### Sets

Sets are unordered collections of unique values. Duplicate values are automatically removed.

#### Set Literal Syntax

```runa
Note: Two equivalent syntaxes for set literals

Note: Syntax 1: "set containing"
Let unique be set containing 1, 2, 3, 4, 5

Note: Syntax 2: "a set containing" (more natural English)
Let numbers be a set containing 10, 20, 30

Note: Sets automatically deduplicate
Let deduped be set containing 1, 2, 2, 3, 3, 3
Note: deduped contains only {1, 2, 3}

Note: "set" can be used as a variable name
Let set be 100  Note: This works! "set" is context-aware
```

#### Set Runtime Operations

```runa
Note: Create empty set
Let my_set be set_create()

Note: Add elements (duplicates ignored)
set_add(my_set, 10)
set_add(my_set, 20)
set_add(my_set, 10)  Note: Ignored, already in set

Note: Check if set contains element
Let has_ten be set_contains(my_set, 10)  Note: Returns 1 (true)
Let has_fifty be set_contains(my_set, 50)  Note: Returns 0 (false)

Note: Remove element (returns 1 if removed, 0 if not found)
Let removed be set_remove(my_set, 10)

Note: Get set size
Let size be set_size(my_set)

Note: Set union (combine two sets)
Let set1 be set containing 1, 2, 3
Let set2 be set containing 3, 4, 5
Let union_set be set_union(set1, set2)  Note: {1, 2, 3, 4, 5}

Note: Set intersection (common elements)
Let intersection be set_intersection(set1, set2)  Note: {3}
```

#### Iterating Over Sets

```runa
Note: Sets can be iterated with for-each loops
Let my_set be set containing 100, 200, 300

For each value in my_set:
    Display integer_to_string(value)
End For
```

---

### Dictionaries

Dictionaries are key-value mappings (also called hash maps or associative arrays).

#### Dictionary Literal Syntax

```runa
Note: Dictionary syntax: "dictionary with: key as value and key as value ..."

Note: Simple dictionary
Let ages be dictionary with: 1 as 25 and 2 as 30 and 3 as 35

Note: Dictionary with expressions
Let x be 10
Let y be 20
Let mapping be dictionary with: x as y and 100 as x plus y

Note: "dictionary" can be used as a variable name
Let dictionary be 777  Note: This works! "dictionary" is context-aware
```

#### Dictionary Runtime Operations

```runa
Note: Create empty dictionary
Let my_dict be dict_create()

Note: Set key-value pairs
dict_set(my_dict, 1, 100)
dict_set(my_dict, 2, 200)
dict_set(my_dict, 3, 300)

Note: Get value by key (returns value, or 0 if key not found)
Let value be dict_get(my_dict, 1)  Note: Returns 100

Note: Check if dictionary has key
Let has_key be dict_has(my_dict, 1)  Note: Returns 1 (true)
Let missing be dict_has(my_dict, 99)  Note: Returns 0 (false)

Note: Remove key-value pair (returns 1 if removed, 0 if not found)
Let removed be dict_remove(my_dict, 2)

Note: Get dictionary size (number of key-value pairs)
Let size be dict_size(my_dict)

Note: Get all keys as a list
Let keys be dict_keys(my_dict)

Note: Get all values as a list
Let values be dict_values(my_dict)
```

#### Iterating Over Dictionaries

```runa
Note: Iterate over dictionary keys
Let ages be dictionary with: 1 as 25 and 2 as 30 and 3 as 35
Let keys be dict_keys(ages)

For each key in keys:
    Let value be dict_get(ages, key)
    Display(integer_to_string(key))
    Display integer_to_string(value)
End For

Note: Iterate over dictionary values
Let values be dict_values(ages)
For each val in values:
    Display(integer_to_string(val))
End For
```

---

### Context-Aware Collection Keywords

The keywords `list`, `set`, and `dictionary` are **context-aware** - they only act as keywords in specific contexts:

```runa
Note: As keywords (followed by "containing" or "with:")
Let my_list be list containing 1, 2, 3
Let my_set be set containing 1, 2, 3
Let my_dict be dictionary with: 1 as 100

Note: As variable names (anywhere else)
Let list be 42
Let set be 100
Let dictionary be 200
Set list to list plus set  Note: Works perfectly!

Note: Real example from compiler source code
Let list be list_create()  Note: "list" is a variable, not a keyword
list_append(list, value)
```

This design allows natural English-like syntax for collection literals while maintaining full backward compatibility with existing code that uses these words as identifiers.

---

## Inline Assembly

Runa supports inline x86-64 assembly for low-level operations:

```runa
Let x be 5

Inline Assembly:
    movq -8(%rbp), %rbx
    addq $37, %rbx
    movq %rbx, -8(%rbp)
End Assembly

Note: x is now 42
```

**IMPORTANT:** Hash (`#`) comments are ONLY allowed inside `Inline Assembly` blocks, nowhere else!

**Example with comments:**

```runa
Inline Assembly:
    # Save value to register (hash comments work here!)
    movq -8(%rbp), %rbx

    # Add 37 to it
    addq $37, %rbx

    # Store result back
    movq %rbx, -8(%rbp)
End Assembly
```

---

## Imports

### Importing Other Files

```runa
Import "tests/unit/test_imports_helper.runa" as Helper

Process called "main" returns Integer:
    Let result be add(10, 5)
    Display(integer_to_string(result))
    Return 0
End Process
```

### Multi-File Projects

You can split your code across multiple files and import them:

```runa
Note: In math_utils.runa
Process called "add" takes a as Integer, b as Integer returns Integer:
    Return a plus b
End Process

Note: In main.runa
Import "math_utils.runa" as MathUtils

Process called "main" returns Integer:
    Let result be add(10, 20)
    Display(integer_to_string(result))
    Return 0
End Process
```

---

## Built-in Functions

### Display
```runa
Display "Hello"
Display integer_to_string(42)
```

### String Conversion
```runa
Let str be integer_to_string(42)
```

### Collection Functions
See [Collections](#collections) section for complete list, set, and dictionary operations.

---

## Language Features Summary

✅ **Implemented in v0.0.8.3:**
- Variables with type inference
- Integers and booleans
- Arithmetic, comparison, logical, and bitwise operators
- Control flow (If/Otherwise If/Otherwise, While, For, For-Each)
- Functions (Processes) with multiple parameters
- Structs with nested field access
- **Collections:**
  - **Lists** with literals (`list containing`) and runtime operations
  - **Sets** with literals (`set containing`) and runtime operations
  - **Dictionaries** with literals (`dictionary with:`) and runtime operations
- For-each loops over collections
- Context-aware collection keywords (`list`, `set`, `dictionary`)
- **Algebraic Data Types (ADTs):**
  - **Variant types** with multiple constructors
  - **Pattern matching** with `Match`/`When` statements
  - **Field extraction** from variant patterns
  - **Wildcard patterns** (`_`) for catch-all cases
  - **Literal patterns** for matching specific integer values
  - **Type patterns** (`of Type`) for runtime type discrimination
  - **Exhaustiveness checking** with warnings for incomplete matches
  - **Recursive ADTs** (lists, trees, etc.)
- Inline assembly with hash (`#`) comments
- Multi-file imports
- Break/Continue statements
- Negative numbers
- Compound assignments

❌ **Not Yet Implemented:**
- String type (planned)
- Floating-point numbers
- Generic types
- Error handling
- Advanced pattern matching (literals, guards)

---

## Example Programs

### Hello World
```runa
Process called "main" returns Integer:
    Display "Hello, World!"
    Return 0
End Process
```

### Fibonacci Sequence
```runa
Process called "fibonacci" takes n as Integer returns Integer:
    If n is less than or equal to 1:
        Return n
    End If
    Let a be fibonacci(n minus 1)
    Let b be fibonacci(n minus 2)
    Return a plus b
End Process

Process called "main" returns Integer:
    Let result be fibonacci(10)
    Display integer_to_string(result)
    Return 0
End Process
```

### Working with Lists
```runa
Process called "main" returns Integer:
    Note: Create a list and calculate sum
    Let numbers be a list containing 1, 2, 3, 4, 5
    Let sum be 0

    For each num in numbers:
        Set sum to sum plus num
    End For

    Display "Sum is:"
    Display integer_to_string(sum)  Note: Prints 15
    Return 0
End Process
```

### Working with Sets
```runa
Process called "main" returns Integer:
    Note: Sets automatically deduplicate
    Let unique_nums be set containing 1, 2, 2, 3, 3, 3, 4, 5

    Let size be set_size(unique_nums)
    Display "Set size:"
    Display integer_to_string(size)  Note: Prints 5, not 8

    Note: Set operations
    Let set1 be set containing 1, 2, 3
    Let set2 be set containing 3, 4, 5

    Let union be set_union(set1, set2)
    Display "Union size:"
    Display integer_to_string(set_size(union))  Note: Prints 5

    Let intersection be set_intersection(set1, set2)
    Display "Intersection size:"
    Display integer_to_string(set_size(intersection))  Note: Prints 1

    Return 0
End Process
```

### Working with Dictionaries
```runa
Process called "main" returns Integer:
    Note: Create a dictionary mapping IDs to scores
    Let scores be dictionary with: 1 as 95 and 2 as 87 and 3 as 92

    Note: Get values
    Let score1 be dict_get(scores, 1)
    Display "Score for ID 1:"
    Display integer_to_string(score1)  Note: Prints 95

    Note: Add new entry
    dict_set(scores, 4, 88)

    Note: Iterate over all entries
    Let keys be dict_keys(scores)
    For each key in keys:
        Let value be dict_get(scores, key)
        Display(integer_to_string(key))
        Display integer_to_string(value)
    End For

    Return 0
End Process
```

### Nested Collections
```runa
Process called "main" returns Integer:
    Note: Lists of lists (nested collections)
    Let list1 be list containing 1, 2, 3
    Let list2 be list containing 4, 5, 6
    Let matrix be list_create()
    list_append(matrix, list1)
    list_append(matrix, list2)

    Note: Access nested elements
    Let row0 be list_get(matrix, 0)
    Let element be list_get(row0, 1)
    Display integer_to_string(element)  Note: Prints 2

    Note: Dictionary with list values
    Let data be dict_create()
    dict_set(data, 100, list1)
    dict_set(data, 200, list2)

    Let retrieved be dict_get(data, 100)
    Let first be list_get(retrieved, 0)
    Display integer_to_string(first)  Note: Prints 1

    Return 0
End Process
```

### Working with Structs
```runa
Type called "Point":
    x as Integer
    y as Integer
End Type

Process called "distance" takes p1 as Point, p2 as Point returns Integer:
    Let dx be the x of p2 minus the x of p1
    Let dy be the y of p2 minus the y of p1
    Let result be dx multiplied by dx plus dy multiplied by dy
    Return result
End Process

Process called "main" returns Integer:
    Let p1 be a Point with x 0 and y 0
    Let p2 be a Point with x 3 and y 4
    Let dist_squared be distance(p1, p2)
    Display integer_to_string(dist_squared)
    Return 0
End Process
```

## 10. Algebraic Data Types (ADTs)

### Variant Types

ADTs (also known as sum types or tagged unions) allow you to define types that can be one of several variants. Each variant can have its own set of fields.

**Basic Syntax:**
```runa
Type TypeName is:
    | Variant1
    | Variant2 with field1 as Integer
    | Variant3 with field1 as Integer and field2 as Integer
End Type
```

**Example - Option Type:**
```runa
Type Option is:
    | Some with value as Integer
    | None
End Type
```

**Example - Shape Type:**
```runa
Type Shape is:
    | Circle with radius as Integer
    | Rectangle with width as Integer and height as Integer
    | Triangle with base as Integer and height as Integer
End Type
```

**Constructing Variants:**

Variants without fields:
```runa
Let x be a None with
```

Variants with a single field:
```runa
Let x be a Some with value as 42
Let circle be a Circle with radius as 5
```

Variants with multiple fields:
```runa
Let rect be a Rectangle with width as 10 and height as 20
Let tri be a Triangle with base as 8 and height as 6
```

### Pattern Matching

Use `Match` statements to discriminate between variants and extract their fields.

**Basic Syntax:**
```runa
Match value:
    When Variant1:
        Note: Handle variant without fields
    When Variant2 with field1 as x:
        Note: Extract and use field
    When Variant3 with field1 as a and field2 as b:
        Note: Extract multiple fields
    When _:
        Note: Wildcard catches all other cases
End Match
```

**Example - Option Type:**
```runa
Process called "get_or_default" takes opt as Integer, default as Integer returns Integer:
    Let result be 0

    Match opt:
        When Some with value as v:
            Set result to v
        When None:
            Set result to default
    End Match

    Return result
End Process

Process called "main" returns Integer:
    Let x be a Some with value as 42
    Let value be get_or_default(x, 0)
    Display integer_to_string(value)  Note: Prints 42

    Let y be a None with
    Let default_value be get_or_default(y, 100)
    Display integer_to_string(default_value)  Note: Prints 100

    Return 0
End Process
```

**Example - Shape Area Calculation:**
```runa
Process called "area" takes shape as Integer returns Integer:
    Let result be 0

    Match shape:
        When Circle with radius as r:
            Set result to r multiplied by r multiplied by 3
        When Rectangle with width as w and height as h:
            Set result to w multiplied by h
        When Triangle with base as b and height as h:
            Set result to b multiplied by h divided by 2
    End Match

    Return result
End Process

Process called "main" returns Integer:
    Let circle be a Circle with radius as 5
    Let circle_area be area(circle)
    Display integer_to_string(circle_area)  Note: Prints 75

    Let rect be a Rectangle with width as 10 and height as 20
    Let rect_area be area(rect)
    Display integer_to_string(rect_area)  Note: Prints 200

    Return 0
End Process
```

**Wildcard Patterns:**

The wildcard pattern `_` matches any variant and is useful for default cases:

```runa
Process called "is_some" takes opt as Integer returns Integer:
    Let result be 0

    Match opt:
        When Some with value as v:
            Set result to 1
        When _:
            Set result to 0
    End Match

    Return result
End Process
```

**Literal Patterns:**

Match statements support matching on literal values (integers):

```runa
Process called "classify_number" takes num as Integer returns Integer:
    Let result be 0

    Match num:
        When 0:
            Display "Zero"
            Set result to 0
        When 1:
            Display "One"
            Set result to 1
        When _:
            Display "Other"
            Set result to minus 1
    End Match

    Return result
End Process
```

**Type Patterns:**

Match on the type of a value to distinguish between integers and heap-allocated objects:

```runa
Process called "describe_value" takes value as Integer returns Integer:
    Match value:
        When x of Type Integer:
            Display "It's an integer"
        When _:
            Display "It's a heap object"
    End Match

    Return 0
End Process
```

**Note:** Type patterns use a pointer threshold (4096) to distinguish primitives from heap objects. Values below the threshold are treated as integers, values above are treated as pointers to heap-allocated data.

**Exhaustiveness Checking:**

The compiler warns when match statements don't cover all variants:

```runa
Type Option is:
    | Some with value as Integer
    | None
End Type

Process called "main" returns Integer:
    Let x be a Some with value as 42

    Note: Warning: Match on type 'Option' is not exhaustive. Missing variants: - None
    Match x:
        When Some with value as v:
            Display integer_to_string(v)
    End Match

    Return 0
End Process
```

To make a match exhaustive, either:
1. Add cases for all missing variants
2. Use a wildcard pattern `_` as the last case

```runa
Note: Exhaustive match with wildcard
Match x:
    When Some with value as v:
        Display integer_to_string(v)
    When _:
        Display "None or unknown"
End Match
```

**Recursive ADTs:**

ADTs can reference themselves, enabling recursive data structures:

```runa
Type List is:
    | Cons with head as Integer and tail as Integer
    | Nil
End Type

Process called "sum_list" takes list as Integer returns Integer:
    Let result be 0

    Match list:
        When Cons with head as h and tail as t:
            Let tail_sum be sum_list(t)
            Set result to h plus tail_sum
        When Nil:
            Set result to 0
        When _:
            Set result to 0
    End Match

    Return result
End Process

Process called "main" returns Integer:
    Note: Build list [1, 2, 3]
    Let nil be a Nil with
    Let list3 be a Cons with head as 3 and tail as nil
    Let list2 be a Cons with head as 2 and tail as list3
    Let list1 be a Cons with head as 1 and tail as list2

    Let total be sum_list(list1)
    Display integer_to_string(total)  Note: Prints 6

    Return 0
End Process
```

**Binary Tree Example:**
```runa
Type BinaryTree is:
    | Leaf with value as Integer
    | Node with value as Integer and left as Integer and right as Integer
End Type

Process called "tree_sum" takes tree as Integer returns Integer:
    Let result be 0

    Match tree:
        When Leaf with value as v:
            Set result to v
        When Node with value as v and left as l and right as r:
            Let left_sum be tree_sum(l)
            Let right_sum be tree_sum(r)
            Set result to v plus left_sum plus right_sum
        When _:
            Set result to 0
    End Match

    Return result
End Process

Process called "main" returns Integer:
    Note: Build tree with root=1, left=Node(5, Leaf(10), Leaf(20)), right=Leaf(30)
    Let leaf1 be a Leaf with value as 10
    Let leaf2 be a Leaf with value as 20
    Let leaf3 be a Leaf with value as 30
    Let node1 be a Node with value as 5 and left as leaf1 and right as leaf2
    Let root be a Node with value as 1 and left as node1 and right as leaf3

    Let total be tree_sum(root)
    Display integer_to_string(total)  Note: Prints 66 (1+5+10+20+30)

    Return 0
End Process
```

**Expression Evaluator Example:**
```runa
Type Expression is:
    | Number with value as Integer
    | Add with left as Integer and right as Integer
    | Multiply with left as Integer and right as Integer
End Type

Process called "eval_expr" takes expr as Integer returns Integer:
    Let result be 0

    Match expr:
        When Number with value as v:
            Set result to v
        When Add with left as l and right as r:
            Let left_val be eval_expr(l)
            Let right_val be eval_expr(r)
            Set result to left_val plus right_val
        When Multiply with left as l and right as r:
            Let left_val be eval_expr(l)
            Let right_val be eval_expr(r)
            Set result to left_val multiplied by right_val
        When _:
            Set result to 0
    End Match

    Return result
End Process

Process called "main" returns Integer:
    Note: Evaluate (2 + 3) * 4 = 20
    Let num2 be a Number with value as 2
    Let num3 be a Number with value as 3
    Let num4 be a Number with value as 4

    Let add2_3 be a Add with left as num2 and right as num3
    Let result_expr be a Multiply with left as add2_3 and right as num4

    Let result be eval_expr(result_expr)
    Display integer_to_string(result)  Note: Prints 20

    Return 0
End Process
```

## 11. Inline Assembly

---

This guide covers all implemented features in v0.0.8.3. For compiler usage instructions, see [GETTING_STARTED.md](GETTING_STARTED.md).
