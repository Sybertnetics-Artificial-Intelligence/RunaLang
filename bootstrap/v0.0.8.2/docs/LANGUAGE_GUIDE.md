# Runa Language Guide (v0.0.8.2)

This guide documents the Runa programming language syntax and features as implemented in v0.0.8.2. All examples are taken from actual working test files.

## Table of Contents
1. [Program Structure](#program-structure)
2. [Comments](#comments)
3. [Variables](#variables)
4. [Data Types](#data-types)
5. [Operators](#operators)
6. [Control Flow](#control-flow)
7. [Functions](#functions)
8. [Structs](#structs)
9. [Lists](#lists)
10. [Inline Assembly](#inline-assembly)
11. [Imports](#imports)

---

## Program Structure

Every Runa program starts with a `main` function (called a "Process"):

```runa
Process called "main" returns Integer:
    Display("Hello, World!")
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

### Lists

See [Lists](#lists) section below.

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
    Display("Both conditions true")
End If

If x is equal to 5 or y is equal to 10:
    Display("At least one condition true")
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
    Display("x is 10")
Otherwise:
    Display("x is not 10")
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
    Display(integer_to_string(num))
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
    Display(integer_to_string(i))
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
Display(integer_to_string(sum))
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

## Lists

### List Literals

```runa
Note: Create list with values
Let numbers be a list containing 10, 20, 30

Note: Create list with expressions
Let x be 5
Let y be 10
Let computed be a list containing x, y, x plus y
```

### List Operations

```runa
Note: Create empty list
Let list be list_create()

Note: Append elements
list_append(list, 10)
list_append(list, 20)

Note: Get element
Let val be list_get(list, 0)

Note: Set element
list_set(list, 0, 100)

Note: Insert element
list_insert(list, 1, 15)

Note: Remove element
Let removed be list_remove(list, 1)

Note: Get length
Let len be list_length(list)

Note: Clear list
list_clear(list)

Note: Destroy list
list_destroy(list)
```

### Iterating Over Lists

```runa
Let fruits be a list containing 100, 200, 300
For each item in fruits:
    Display(integer_to_string(item))
End For
```

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
Display("Hello")
Display(integer_to_string(42))
```

### String Conversion
```runa
Let str be integer_to_string(42)
```

### List Functions
See [Lists](#lists) section for complete list operations.

---

## Language Features Summary

✅ **Implemented in v0.0.8.2:**
- Variables with type inference
- Integers and booleans
- Arithmetic, comparison, logical, and bitwise operators
- Control flow (If/Otherwise If/Otherwise, While, For, For-Each)
- Functions (Processes) with multiple parameters
- Structs with nested field access
- Lists with runtime operations
- List literals and for-each loops
- Inline assembly
- Multi-file imports
- Break/Continue statements
- Negative numbers
- Compound assignments

❌ **Not Yet Implemented:**
- Sets
- Dictionaries
- String type (planned)
- Floating-point numbers
- Generic types
- Error handling

---

## Example Programs

### Hello World
```runa
Process called "main" returns Integer:
    Display("Hello, World!")
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
    Display(integer_to_string(result))
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

    Display("Sum is:")
    Display(integer_to_string(sum))
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
    Display(integer_to_string(dist_squared))
    Return 0
End Process
```

---

This guide covers all implemented features in v0.0.8.2. For compiler usage instructions, see [GETTING_STARTED.md](GETTING_STARTED.md).
