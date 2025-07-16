# Runa Standard Library: String Module

## Overview

The `string` module provides comprehensive string formatting, manipulation, validation, and analysis utilities for Runa programs. All functions are designed to be idiomatic, robust, and production-ready, matching the breadth and depth of modern language standard libraries.

## String Constants

The module provides standard string constants for common character sets:

```runa
# Character sets
ascii_letters    # "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
ascii_lowercase  # "abcdefghijklmnopqrstuvwxyz"
ascii_uppercase  # "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
digits          # "0123456789"
hexdigits       # "0123456789abcdefABCDEF"
octdigits       # "01234567"
punctuation     # "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
whitespace      # " \t\n\r\x0b\x0c"
```

## Basic String Operations

### Case Manipulation
- `upper(s: String) -> String` - Convert to uppercase
- `lower(s: String) -> String` - Convert to lowercase
- `title(s: String) -> String` - Convert to title case
- `capitalize(s: String) -> String` - Capitalize first letter
- `swapcase(s: String) -> String` - Swap case of all characters

### Trimming and Whitespace
- `trim(s: String) -> String` - Remove leading and trailing whitespace
- `trim_left(s: String) -> String` - Remove leading whitespace
- `trim_right(s: String) -> String` - Remove trailing whitespace

### Concatenation and Replacement
- `concat(a: String, b: String) -> String` - Concatenate two strings
- `replace(s: String, old: String, new: String) -> String` - Replace first occurrence
- `replace_all(s: String, old: String, new: String) -> String` - Replace all occurrences

### Splitting and Joining
- `split(s: String, sep: String) -> List[String]` - Split by separator
- `split_lines(s: String) -> List[String]` - Split by newlines
- `split_whitespace(s: String) -> List[String]` - Split by whitespace
- `join(items: List[String], sep: String) -> String` - Join with separator

## String Validation and Testing

### Content Validation
- `is_empty(s: String) -> Boolean` - Check if string is empty
- `is_blank(s: String) -> Boolean` - Check if string is blank (whitespace only)
- `starts_with(s: String, prefix: String) -> Boolean` - Check if starts with prefix
- `ends_with(s: String, suffix: String) -> Boolean` - Check if ends with suffix
- `contains(s: String, substr: String) -> Boolean` - Check if contains substring

### Character Type Validation
- `is_alpha(s: String) -> Boolean` - Check if contains only alphabetic characters
- `is_digit(s: String) -> Boolean` - Check if contains only digits
- `is_alphanumeric(s: String) -> Boolean` - Check if contains only alphanumeric characters
- `is_whitespace(s: String) -> Boolean` - Check if contains only whitespace

## String Formatting

### Template Formatting
- `format_string(template: String, values: Dictionary[String, Any]) -> String` - Format with {key} placeholders

### Padding and Justification
- `pad_left(s: String, width: Integer, char: String = " ") -> String` - Pad to width on left
- `pad_right(s: String, width: Integer, char: String = " ") -> String` - Pad to width on right
- `center(s: String, width: Integer, char: String = " ") -> String` - Center in width
- `justify_left(s: String, width: Integer) -> String` - Left justify
- `justify_right(s: String, width: Integer) -> String` - Right justify
- `justify_center(s: String, width: Integer) -> String` - Center justify

## String Analysis

### Search and Count
- `count(s: String, substr: String) -> Integer` - Count occurrences
- `find(s: String, substr: String) -> Integer` - Find first occurrence
- `find_last(s: String, substr: String) -> Integer` - Find last occurrence
- `index_of(s: String, substr: String) -> Integer` - Get index of first occurrence
- `last_index_of(s: String, substr: String) -> Integer` - Get index of last occurrence

## String Transformation

### Basic Transformations
- `reverse(s: String) -> String` - Reverse string
- `repeat(s: String, count: Integer) -> String` - Repeat string
- `substring(s: String, start: Integer, end: Integer) -> String` - Extract substring
- `remove(s: String, substr: String) -> String` - Remove first occurrence
- `remove_all(s: String, substr: String) -> String` - Remove all occurrences

## String Encoding and Escaping

### HTML and Special Characters
- `escape_html(s: String) -> String` - Escape HTML entities
- `unescape_html(s: String) -> String` - Unescape HTML entities
- `escape_regex(s: String) -> String` - Escape regex special characters
- `quote(s: String) -> String` - Add double quotes
- `unquote(s: String) -> String` - Remove surrounding quotes

## Classes

### StringTemplate

Template-based string substitution with support for both regular and safe substitution:

```runa
Let template be StringTemplate with template as "Hello $name, you are $age years old"
Let values be dictionary with:
    "name" as "Alice"
    "age" as 30
Let result be substitute with self as template and values as values
# Result: "Hello Alice, you are 30 years old"

Let safe_result be safe_substitute with self as template and values as dictionary with "name" as "Bob"
# Result: "Hello Bob, you are $age years old" (missing values left unchanged)
```

### StringBuilder

Efficient string concatenation for building large strings:

```runa
Let builder be StringBuilder with parts as list containing
Let result be builder.append with s as "Hello"
Let result be result.append_line with s as "World"
Let final_string be the build of result
```

### Advanced String Processing

```runa
Let text be "Hello, World! This is a test string."
Let words be string.split_whitespace with s as text
Let word_count be the length of words
Let longest_word be string.max with a as words[0] and b as words[1]

Let builder be StringBuilder with parts as list containing
For each word in words:
    Let processed be string.capitalize with s as word
    Let result be builder.append with s as processed
    Let result be result.append with s as " "
Let final_text be the build of result
```

## Usage Examples

### Basic Operations
```runa
Let greeting be "Hello, World!"
Let upper_greeting be upper with s as greeting
Let lower_greeting be lower with s as greeting
Let trimmed be trim with s as "  hello world  "
```

### String Validation
```runa
Let email be "user@example.com"
Assert contains with s as email and substr as "@" is equal to true
Assert ends_with with s as email and suffix as ".com" is equal to true
Assert is_alphanumeric with s as "hello123" is equal to true
```

### String Formatting
```runa
Let template be "User {name} has {count} messages"
Let values be dictionary with:
    "name" as "Alice"
    "count" as 42
Let formatted be format_string with template as template and values as values
# Result: "User Alice has 42 messages"
```

### String Analysis
```runa
Let text be "hello world hello"
Let count be count with s as text and substr as "hello"
# Result: 2
Let position be find with s as text and substr as "world"
# Result: 6
```

### String Transformation
```runa
Let s be "hello"
Let reversed be reverse with s as s
# Result: "olleh"
Let repeated be repeat with s as s and count as 3
# Result: "hellohellohello"
```

## Testing

A comprehensive Runa-based test file for the string module is located at:

    runa/tests/stdlib/test_string_format.runa

This file exercises all string operations including:
- Basic string operations (concat, upper, lower, title, capitalize, swapcase)
- Trimming and whitespace handling
- Replacement and splitting operations
- String validation and testing
- Formatting and padding
- String analysis and search
- String transformation
- Encoding and escaping
- StringTemplate and StringBuilder classes
- Edge cases and error handling

All tests use idiomatic Runa assertions and error handling, ensuring production-ready quality and verifiability.

## Performance Considerations

- **StringBuilder** should be used for building large strings through multiple concatenations
- **Template formatting** is more efficient than manual string replacement for complex formatting
- **Character validation** functions are optimized for common use cases
- **Search and analysis** functions use efficient algorithms for large strings

## Error Handling

The string module handles edge cases gracefully:
- Empty strings return appropriate default values
- Invalid parameters raise clear error messages
- Unicode text is handled correctly
- Whitespace-only text is processed appropriately
- Out-of-bounds indices are handled safely 