# Runa Code Examples

This document provides examples of Runa code to demonstrate various language features and optimizations.

## Basic Examples

### Hello World
```
Display "Hello, World!"
```

### Variables and Arithmetic
```
Let a be 10
Let b be 20
Let sum be a plus b
Display sum  # Output: 30
```

## Control Flow Examples

### If Statement
```
Let age be 18

If age greater than or equal to 18:
    Display "You are an adult"
Otherwise:
    Display "You are a minor"
```

### For Each Loop
```
Let numbers be [1, 2, 3, 4, 5]
Let sum be 0

For each num in numbers:
    Set sum to sum plus num

Display sum  # Output: 15
```

### While Loop
```
Let counter be 1
Let sum be 0

While counter less than or equal to 5:
    Set sum to sum plus counter
    Set counter to counter plus 1

Display sum  # Output: 15
```

## Function Examples

### Basic Function
```
Process called "greet" that takes name:
    Display "Hello" with name as name
    
greet with "Alice"  # Output: Hello Alice
```

### Factorial Function (Recursive)
```
Process called "factorial" that takes n:
    If n less than or equal to 1:
        Return 1
    Otherwise:
        Return n multiplied by factorial with n minus 1

Let result be factorial with 5
Display result  # Output: 120
```

### Factorial Function (Iterative with While Loop)
```
Process called "factorial" that takes n:
    Let result be 1
    Let i be 1
    
    While i less than or equal to n:
        Set result to result multiplied by i
        Set i to i plus 1
        
    Return result

Let result be factorial with 5
Display result  # Output: 120
```

## Data Structure Examples

### List Operations
```
Let numbers be [1, 2, 3, 4, 5]
Let first be numbers at 0
Let last be numbers at 4

Display first  # Output: 1
Display last   # Output: 5
```

### Dictionary Operations
```
Let person be [
    "name": "Alice",
    "age": 25,
    "city": "New York"
]

Display person at "name"  # Output: Alice
```

## Optimization Examples

### Constant Folding
```
# Without optimization:
Let result be 10 plus 20 multiplied by 3
Display result  # Computed at runtime

# With optimization (level 1 or higher):
# The expression is evaluated at compile time as 10 + (20 * 3) = 70
Let result be 70
Display result
```

### Dead Code Elimination
```
# Without optimization:
Let flag be True

If flag:
    Display "This will be shown"
Otherwise:
    # This branch will never execute
    Display "This will never be shown"

# With optimization (level 1 or higher):
# The if-statement is removed and only the true branch remains
Display "This will be shown"
```

### Loop Optimization - Loop Unrolling
```
# Without optimization:
Let items be [1, 2, 3]
Let sum be 0

For each item in items:
    Set sum to sum plus item

Display sum  # Output: 6

# With optimization (level 2):
# The loop is unrolled into sequential operations
Let items be [1, 2, 3]
Let sum be 0

Set sum to sum plus 1
Set sum to sum plus 2
Set sum to sum plus 3

Display sum  # Output: 6
```

### Loop Optimization - Loop Invariant Code Motion
```
# Without optimization:
Let x be 10
Let y be 20
Let result be 0
Let i be 0

While i less than 100:
    # x * y doesn't change within the loop
    Set result to result plus x multiplied by y
    Set i to i plus 1

# With optimization (level 2):
# The invariant expression is moved outside the loop
Let x be 10
Let y be 20
Let result be 0
Let i be 0
Let temp be x multiplied by y  # Computed once

While i less than 100:
    Set result to result plus temp
    Set i to i plus 1
```

## Running the Examples

You can run these examples with different optimization levels to see the performance differences:

```bash
# Run without optimizations
runa run example.runa --optimize 0

# Run with basic optimizations
runa run example.runa --optimize 1

# Run with aggressive optimizations
runa run example.runa --optimize 2
```

## Benchmarking Examples

You can also run benchmarks to see the performance impact of optimizations:

```bash
# Run loop optimization benchmarks
runa benchmark loop

# Run general optimization benchmarks
runa benchmark optimization
```

For more detailed examples, see the `examples/` directory in the Runa repository. 