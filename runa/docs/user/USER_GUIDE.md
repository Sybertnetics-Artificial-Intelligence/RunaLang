# Runa Programming Language - User Guide

## Welcome to Runa! 🎉

Runa is a revolutionary natural language programming language that lets you write code in plain English while maintaining the power and precision of traditional programming languages.

## Table of Contents

- [Installation](#installation)
- [Your First Runa Program](#your-first-runa-program)
- [Basic Syntax](#basic-syntax)
- [Variables and Types](#variables-and-types)
- [Control Flow](#control-flow)
- [Functions](#functions)
- [Advanced Features](#advanced-features)
- [Examples](#examples)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Install Runa
```bash
# Clone the repository
git clone https://github.com/sybertnetics/runa
cd runa

# Install dependencies
pip install -e .

# Verify installation
python -m runa.cli --help
```

## Your First Runa Program

Create a file called `hello.runa`:

```runa
Display "Hello, World!"
```

Compile and run it:

```bash
# Compile to Python
python -m runa.cli compile hello.runa -t python

# Run the generated Python code
python hello.py
```

Output:
```
Hello, World!
```

## Basic Syntax

### Comments
Runa uses natural language, so comments are rarely needed, but you can use `Note:` for documentation:

```runa
Note: This is a comment explaining the code below
Display "This is actual code"
```

### Statements
Every statement in Runa reads like natural English:

```runa
Let x be 42
Set x to x plus 1
Display x
```

### Natural Language Keywords
Runa uses English words instead of symbols:
- `be` instead of `=`
- `is equal to` instead of `==`
- `is greater than` instead of `>`
- `and` / `or` instead of `&&` / `||`

## Variables and Types

### Variable Declaration

```runa
Let name be "Alice"
Let age be 25
Let is_student be true
Let grades be list containing 95, 87, 92
```

### Type Annotations

```runa
Let score (Integer) be 100
Let message (String) be "Hello"
Let numbers (List[Integer]) be list containing 1, 2, 3
```

### Advanced Types

```runa
// Union types
Let value (Integer or String) be 42

// Optional types  
Let optional_name (Optional[String]) be "John"

// Generic types
Let user_data (Dictionary[String, Integer]) be empty
```

## Control Flow

### If Statements

```runa
Let score be 85

If score is greater than 90:
    Display "Excellent!"
Otherwise if score is greater than 80:
    Display "Good job!"
Otherwise:
    Display "Keep trying!"
```

### Loops

```runa
// For-each loop
Let numbers be list containing 1, 2, 3, 4, 5
For each number in numbers:
    Display number

// While loop
Let count be 0
While count is less than 5:
    Display count
    Set count to count plus 1

// For-range loop
For i from 1 to 10:
    Display i

// Repeat loop
Repeat 3 times:
    Display "Hello"
```

### Pattern Matching

```runa
Let value be 42

Match value:
    Case 0:
        Display "Zero"
    Case x If x is greater than 0:
        Display "Positive number"
    Case _:
        Display "Negative number"
```

## Functions

### Function Definition

```runa
Process called "calculate area" that takes width as Integer and height as Integer returns Integer:
    Let area be width multiplied by height
    Return area
```

### Function Calls

```runa
Let result be Calculate Area with width as 10 and height as 5
Display result
```

### Async Functions

```runa
Async Process called "fetch data":
    Display "Fetching data..."
    Return "data"

Let future_data be Await Fetch Data
```

## Advanced Features

### Error Handling

```runa
Try:
    Let result be 10 divided by 0
    Display result
Catch as error:
    Display "An error occurred"
    Display error
Finally:
    Display "Cleanup complete"
```

### Modules

```runa
// Import modules
Import "math" as math_module
Import "utils" exposing calculate, format

// Export functions
Export calculate_area, format_currency
```

### Memory Management

```runa
// Ownership annotations
@owned Let buffer be list containing 1, 2, 3

// Explicit cleanup
Delete buffer
```

### Concurrency

```runa
// Atomic operations
Atomic:
    Set counter to counter plus 1

// Locking
Lock shared_resource:
    Display "Critical section"
```

## Examples

### Example 1: Simple Calculator

```runa
Process called "add" that takes a as Integer and b as Integer returns Integer:
    Return a plus b

Process called "multiply" that takes a as Integer and b as Integer returns Integer:
    Return a multiplied by b

Let x be 10
Let y be 5

Let sum be Add with a as x and b as y
Let product be Multiply with a as x and b as y

Display "Sum: " followed by sum
Display "Product: " followed by product
```

### Example 2: Data Processing

```runa
Let numbers be list containing 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
Let evens be empty list

For each number in numbers:
    If number modulo 2 is equal to 0:
        Add number to evens

Display "Even numbers:"
For each even in evens:
    Display even
```

### Example 3: User Input Validation

```runa
Process called "validate email" that takes email as String returns Boolean:
    If email contains "@" and email contains ".":
        Return true
    Otherwise:
        Return false

Let user_email be "user@example.com"
Let is_valid be Validate Email with email as user_email

If is_valid:
    Display "Valid email address"
Otherwise:
    Display "Invalid email address"
```

## Next Steps

- Read the [Language Reference](LANGUAGE_REFERENCE.md) for complete syntax details
- Explore [Example Projects](examples/) for more complex applications
- Check out the [Standard Library](stdlib/) documentation
- Join our community and contribute to Runa's development

## Getting Help

- Documentation: [docs/](docs/)
- Examples: [examples/](examples/)
- Issues: [GitHub Issues](https://github.com/sybertnetics/runa/issues)
- Community: [Discord Server](https://discord.gg/runa)

Happy coding with Runa! 🚀