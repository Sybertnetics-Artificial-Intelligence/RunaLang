# Runa Programming Language - User Guide

## Welcome to Runa! 🎉

Runa is a revolutionary natural language programming language that lets you write code in plain English while maintaining the power and precision of traditional programming languages.

## Table of Contents

- [Installation](#installation)
- [Language Support](#language-support)
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
Note: Clone the repository
git clone https://github.com/sybertnetics/runa
cd runa

Note: Install dependencies
pip install -e .

Note: Verify installation
python -m runa.cli --help
```

## Language Support

Runa's Universal Translation Platform supports over 50+ programming languages organized into 7 tiers based on usage patterns and development priority. 

### Quick Overview
- **Tier 1-2**: Production-ready with comprehensive support (JavaScript, Python, Rust, Go, etc.)
- **Tier 3-4**: Good support for specialized domains (HTML, CSS, Solidity, GraphQL, etc.)  
- **Tier 5-7**: Functional support for niche and legacy languages (LISP, COBOL, Nix, etc.)

For complete language support details, supported features, and quality expectations, see [Language Tier System](LANGUAGE_TIERS.md).

### Translation Examples
```bash
Note: Translate Runa to any supported language
python -m runa.cli translate app.runa --target javascript
python -m runa.cli translate app.runa --target rust
python -m runa.cli translate app.runa --target solidity

Note: Round-trip verification
python -m runa.cli verify app.runa --target python --verify-round-trip
```

## Your First Runa Program

Create a file called `hello.runa`:

```runa
Display "Hello, World!"
```

Compile and run it:

```bash
Note: Compile to Python
python -m runa.cli compile hello.runa -t python

Note: Run the generated Python code
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
- `equals` instead of `==`
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
Note: Union types
Let value (Integer or String) be 42

Note: Optional types  
Let optional_name (Optional[String]) be "John"

Note: Generic types
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
Note: For-each loop
Let numbers be list containing 1, 2, 3, 4, 5
For each number in numbers:
    Display number

Note: While loop
Let count be 0
While count is less than 5:
    Display count
    Set count to count plus 1

Note: For-range loop
For i from 1 to 10:
    Display i

Note: Repeat loop
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
Note: Import modules
Import "math" as math_module
Import "utils" exposing calculate, format

Note: Export functions
Export calculate_area, format_currency
```

### Memory Management

```runa
Note: Ownership annotations
@owned Let buffer be list containing 1, 2, 3

Note: Explicit cleanup
Delete buffer
```

### Concurrency

```runa
Note: Atomic operations
Atomic:
    Set counter to counter plus 1

Note: Locking
Lock shared_resource:
    Display "Critical section"
```

## Working with Collections

### Creating Sets
- Static:
  ```runa
  Let s be set containing 1, 2, 3
  ```
- Dynamic:
  ```runa
  Let s be set containing x for each x in values
  ```
- Programmatic:
  ```runa
  Let s be from_list with elements as values
  ```

### Creating Dictionaries
- Static:
  ```runa
  Let d be dictionary with:
      "a" as 1
      "b" as 2
  ```
- Dynamic:
  ```runa
  Let d be dictionary with:
      k as v for each (k, v) in pairs
  ```
- Programmatic:
  ```runa
  Let d be from_pairs with pairs as key_value_pairs
  ```

### Creating Lists
- Static:
  ```runa
  Let l be list containing 1, 2, 3
  ```
- Dynamic:
  ```runa
  Let l be list containing f(x) for each x in data if x is greater than 0
  ```
- Programmatic:
  ```runa
  Let l be create_list with elements as data
  ```