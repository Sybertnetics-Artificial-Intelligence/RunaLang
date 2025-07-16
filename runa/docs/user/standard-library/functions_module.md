# Runa Standard Library: Built-in Helper Processes Module

## Overview

The `builtins/functions` module provides programmatic helper processes for exponentiation, absolute value, and string formatting. These helpers supplement Runa's natural language syntax and are intended for use in programmatic and AI-generated code.

## API

- `Process called "pow" that takes base as Number and exponent as Number returns Number`
  - Returns `base` raised to the power of `exponent`.
- `Process called "abs" that takes x as Number returns Number`
  - Returns the absolute value of `x`.
- `Process called "format_string" that takes template as String and values as Dictionary[String, Any] returns String`
  - Returns the template string with `{key}` placeholders replaced by values from the dictionary.

## Usage Example

```runa
Let result be pow with base as 2 and exponent as 8
Assert result is equal to 256

Let formatted be format_string with template as "User {name} is {age} years old" and values as dictionary with:
    "name" as "Alice"
    "age" as 30
Assert formatted is equal to "User Alice is 30 years old"
```

## Testing

A comprehensive Runa-based test file for the built-in helper processes module is located at:

    runa/tests/stdlib/test_builtins.runa

This file exercises all helper processes using idiomatic Runa assertions and error handling. All standard library modules have corresponding Runa test files in this directory, ensuring production-ready quality and verifiability. 