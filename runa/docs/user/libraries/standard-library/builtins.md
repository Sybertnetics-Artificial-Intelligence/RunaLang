# Runa Built-ins Module Guide

The Runa built-ins module provides essential functionality that forms the foundation of all Runa programs. This module includes exception handling, utility functions, global constants, and operator implementations that support Runa's natural language syntax.

## Overview

The built-ins module consists of four main components:

- **exceptions.runa**: Complete exception hierarchy and error handling
- **functions.runa**: Utility functions for common operations
- **globals.runa**: Global constants and system information
- **operators.runa**: Operator implementations and overloading support

All built-in functionality is automatically available in Runa programs without explicit import statements.

## Exception System (`exceptions.runa`)

### Exception Hierarchy

Runa provides a comprehensive exception system based on a natural language approach to error handling:

```runa
Note: Basic exception creation
Let error be create_exception with exception_type as "ValidationError" and message as "Invalid input provided"

Note: Specific exception types
Let type_error be create_type_error with expected as "String" and actual as "Integer" and variable as "username"
Let value_error be create_value_error with value as -5 and constraint as "Value must be positive"
Let index_error be create_index_error with index as 10 and size as 5 and collection_type as "List"
```

### Available Exception Types

1. **RunaException**: Base exception type
2. **TypeError**: Type mismatch errors
3. **ValueError**: Invalid value errors
4. **IndexError**: Collection index errors
5. **KeyError**: Dictionary key errors
6. **RuntimeError**: Runtime operation errors
7. **IOError**: Input/output errors
8. **NetworkError**: Network operation errors
9. **TimeoutError**: Operation timeout errors
10. **ValidationError**: Data validation errors

### Exception Chaining

```runa
Note: Chain exceptions to preserve error context
Let original_error be create_value_error with value as 0 and constraint as "Division by zero"
Let chained_error be create_runtime_error with operation as "calculate" and context as dictionary with "step" as "division"
Let final_exception be chain_exception with new_exception as chained_error and cause as original_error
```

### Error Recovery

```runa
Note: Get recovery suggestions for errors
Let suggestions be suggest_error_resolution with exception as type_error
For each suggestion in suggestions:
    Display "Suggestion: " with message suggestion
```

## Utility Functions (`functions.runa`)

### Mathematical Functions

```runa
Note: Basic mathematical operations
Let absolute_value be abs with value as -42                    Note: Returns 42
Let minimum be min with values as list containing 10, 5, 8     Note: Returns 5
Let maximum be max with values as list containing 10, 5, 8     Note: Returns 10
Let total be sum with values as list containing 1, 2, 3, 4     Note: Returns 10
Let power be pow with base as 2 and exponent as 3              Note: Returns 8
Let square_root be sqrt with value as 25                       Note: Returns 5.0

Note: Rounding functions
Let ceiling be ceil with value as 3.2                          Note: Returns 4
Let floored be floor with value as 3.8                         Note: Returns 3
Let rounded be round with value as 3.14159 and digits as 2     Note: Returns 3.14
```

### Type Conversion Functions

```runa
Note: Convert between different data types
Let string_value be to_string with value as 42                 Note: Returns "42"
Let integer_value be to_integer with value as "123"            Note: Returns 123
Let float_value be to_float with value as "3.14"              Note: Returns 3.14
Let boolean_value be to_boolean with value as "true"           Note: Returns true

Note: Handle different input types
Let int_from_float be to_integer with value as 45.7            Note: Returns 45
Let bool_from_int be to_boolean with value as 1                Note: Returns true
```

### String Manipulation

```runa
Note: String processing operations
Let text_length be length with collection as "Hello World"     Note: Returns 11
Let parts be split with text as "apple,banana,cherry" and delimiter as ","
Let combined be join with strings as parts and separator as "|"
Let cleaned be trim with text as "  hello world  "             Note: Returns "hello world"
Let upper_text be upper_case with text as "hello"              Note: Returns "HELLO"
Let lower_text be lower_case with text as "WORLD"              Note: Returns "world"
Let capitalized be capitalize with text as "hello world"       Note: Returns "Hello world"

Note: String searching and manipulation
Let replaced = replace with text as "Hello World" and old_substring as "World" and new_substring as "Runa"
Let padded_left be pad_left with text as "42" and width as 5 and fill_char as "0"  Note: Returns "00042"
```

### Collection Functions

```runa
Note: List manipulation
Let original_list be list containing 1, 2, 3
Let with_item be append with collection as original_list and item as 4
Let with_prefix be prepend with collection as original_list and item as 0
Let has_item be contains with collection as original_list and item as 2    Note: Returns true
Let item_position be index_of with collection as original_list and item as 2    Note: Returns 1

Note: List transformations
Let reversed_list be reverse with collection as original_list
Let sorted_list be sort with collection as list containing 3, 1, 4, 1, 5
Let unique_items be unique with collection as list containing 1, 2, 2, 3, 1

Note: Advanced operations
Let numbers be range with start as 1 and end as 10 and step as 2    Note: 1, 3, 5, 7, 9
Let indexed_items be enumerate with collection as list containing "a", "b", "c"
Let paired_items be zip with collections as list containing list containing 1, 2, 3, list containing "a", "b", "c"
```

### Validation Functions

```runa
Note: Data validation utilities
Let is_empty_text be is_empty with collection as ""               Note: Returns true
Let is_number be is_numeric with value as "123.45"               Note: Returns true
Let is_letters be is_alphabetic with value as "hello"            Note: Returns true
Let is_mixed be is_alphanumeric with value as "hello123"         Note: Returns true
```

### String Formatting

```runa
Note: Template-based string formatting
Let template be "Hello {name}, you are {age} years old"
Let values be dictionary with "name" as "Alice", "age" as 25
Let formatted be format_string with template as template and values as values
Display formatted    Note: "Hello Alice, you are 25 years old"
```

## Global Constants (`globals.runa`)

### Mathematical Constants

```runa
Note: Access mathematical constants
Display "Pi: " with message PI                    Note: 3.141592653589793
Display "Euler's number: " with message E         Note: 2.718281828459045
Display "Tau: " with message TAU                  Note: 6.283185307179586
Display "Golden ratio: " with message GOLDEN_RATIO Note: 1.618033988749895
```

### System Information

```runa
Note: Access system and runtime information
Display "Runa version: " with message RUNA_VERSION           Note: "2.1.0"
Display "Platform: " with message PLATFORM_NAME             Note: Platform-specific
Display "CPU count: " with message CPU_COUNT                Note: Number of cores
Display "Debug mode: " with message DEBUG_MODE              Note: Current debug status

Note: Get comprehensive runtime statistics
Let stats be get_runtime_statistics
For each key and value in stats:
    Display key with message ": " with message value
```

### Environment Management

```runa
Note: Access environment variables
Let home_dir be get_environment_variable with name as "HOME"
Let path_var be get_environment_variable with name as "PATH"

Note: List available global variables
Let global_vars be list_global_variables
For each var_name in global_vars:
    Let var_value be get_global_variable with name as var_name
    Display var_name with message " = " with message var_value
```

## Operators (`operators.runa`)

### Arithmetic Operators

```runa
Note: Arithmetic operations with explicit functions
Let sum_result be add with left as 5 and right as 3           Note: Returns 8
Let diff_result be subtract with left as 10 and right as 4    Note: Returns 6
Let product be multiply with left as 6 and right as 7         Note: Returns 42
Let quotient be divide with left as 15 and right as 3         Note: Returns 5
Let remainder be modulo with left as 17 and right as 5        Note: Returns 2
Let power_result be power with base as 2 and exponent as 4    Note: Returns 16
```

### Comparison Operators

```runa
Note: Comparison operations
Let are_equal be equals with left as 5 and right as 5         Note: Returns true
Let not_equal be not_equals with left as 5 and right as 3     Note: Returns true
Let is_less be less_than with left as 3 and right as 7        Note: Returns true
Let is_greater be greater_than with left as 9 and right as 4  Note: Returns true
Let comparison be compare with left as 5 and right as 3       Note: Returns 1 (left > right)
```

### Collection Operators

```runa
Note: Collection operations
Let list1 be list containing 1, 2, 3
Let list2 be list containing 4, 5, 6
Let combined_lists be list_concatenate with left as list1 and right as list2

Let test_dict be dictionary with "a" as 1, "b" as 2
Let has_key be dictionary_contains_key with dict as test_dict and key as "a"
Let has_value be dictionary_contains_value with dict as test_dict and value as 2

Note: Set operations
Let set1 be set containing 1, 2, 3
Let set2 be set containing 2, 3, 4
Let union_result be set_union with left as set1 and right as set2
Let intersection_result be set_intersection with left as set1 and right as set2
```

### Operator Metadata

```runa
Note: Get information about operators
Let precedence be get_operator_precedence with operator as "+"
Let associativity be get_operator_associativity with operator as "**"
Let can_override be can_overload_operator with operator as "+"

Note: Natural language mapping
Let symbol be map_natural_language_operator with operator_phrase as "is greater than"
Display "Symbol: " with message symbol    Note: ">"
```

## Error Handling Best Practices

### Using Try-Catch Blocks

```runa
Note: Proper error handling
Try:
    Let result be to_integer with value as user_input
    Display "Converted: " with message result
Catch error:
    If error["error_code"] is equal to "TypeError":
        Display "Please provide a valid number"
    Otherwise:
        Display "Error: " with message error["message"]
        
        Note: Get suggestions for recovery
        Let suggestions be suggest_error_resolution with exception as error
        For each suggestion in suggestions:
            Display "Try: " with message suggestion
```

### Custom Error Messages

```runa
Note: Create descriptive error messages
Process called "validate_age" that takes age as Integer returns Boolean:
    If age is less than 0:
        Throw create_value_error with value as age and constraint as "Age must be non-negative"
    If age is greater than 150:
        Throw create_value_error with value as age and constraint as "Age must be realistic (0-150)"
    Return true
```

## Performance Considerations

### Efficient Collection Operations

```runa
Note: Use appropriate data structures
Let large_dataset be list containing    Note: For large datasets
For i from 1 to 10000:
    Add i to large_dataset

Note: Use unique for deduplication (more efficient than manual checking)
Let unique_values be unique with collection as large_dataset

Note: Use contains for membership testing
If contains with collection as unique_values and item as 5000:
    Display "Found target value"
```

### Memory Management

```runa
Note: Be mindful of memory usage with large strings
Let large_text be ""
Let parts be list containing
For i from 1 to 1000:
    Add "Part " with message i to parts

Note: More efficient than repeated concatenation
Let combined_text be join with strings as parts and separator as " "
```

## Integration Examples

### Data Processing Pipeline

```runa
Note: Complete data processing example
Process called "process_user_data" that takes raw_data as List[String] returns Dictionary[String, Any]:
    Let results be dictionary with:
        "valid_entries" as list containing,
        "errors" as list containing,
        "statistics" as dictionary containing,
        "total_processed" as 0
    
    For each entry in raw_data:
        Try:
            Let cleaned be trim with text as entry
            If not (is_empty with collection as cleaned):
                Let parts be split with text as cleaned and delimiter as ","
                If length of parts is equal to 3:
                    Let name be trim with text as parts[0]
                    Let age be to_integer with value as parts[1]
                    Let email be trim with text as parts[2]
                    
                    Note: Validate data
                    If is_alphabetic with value as name and age is greater than 0 and contains with collection as email and item as "@":
                        Let user_record be dictionary with:
                            "name" as capitalize with text as name,
                            "age" as age,
                            "email" as lower_case with text as email
                        Add user_record to results["valid_entries"]
                    Otherwise:
                        Add "Invalid data format: " with message entry to results["errors"]
                Otherwise:
                    Add "Incorrect field count: " with message entry to results["errors"]
        Catch error:
            Add "Processing error for '" with message entry with message "': " with message error["message"] to results["errors"]
        
        Set results["total_processed"] to results["total_processed"] plus 1
    
    Set results["statistics"] to dictionary with:
        "valid_count" as length of results["valid_entries"],
        "error_count" as length of results["errors"],
        "success_rate" as (length of results["valid_entries"] divided by results["total_processed"]) times 100
    
    Return results

Note: Usage
Let sample_data be list containing "Alice, 25, alice@email.com", "Bob, thirty, bob@email", "Charlie, 35, charlie@email.com"
Let processed be process_user_data with raw_data as sample_data
Display "Processing complete: " with message processed["statistics"]["success_rate"] with message "% success rate"
```

## Testing Your Code

The built-ins module includes comprehensive test coverage. Run the test suite to verify functionality:

```bash
cd runa/
python -m pytest tests/unit/stdlib/test_builtins.runa -v
```

Key test categories:
- Exception creation and chaining
- Mathematical function accuracy
- Type conversion edge cases
- String manipulation correctness
- Collection operation performance
- Global variable accessibility
- Operator precedence and associativity

## Advanced Usage

### Custom Exception Types

```runa
Note: Extend the exception system for domain-specific errors
Process called "create_business_logic_error" that takes operation as String and context as Dictionary[String, Any] returns RunaException:
    Let base_error be create_runtime_error with operation as operation and context as context
    Set base_error["error_code"] to "BusinessLogicError"
    Set base_error["message"] to "Business rule violation in " with message operation
    Return base_error
```

### Operator Overloading

```runa
Note: Register custom operator implementations
Let success be register_operator_overload with type_name as "Money" and operator as "+" and implementation as "add_money"
If success:
    Display "Custom addition operator registered for Money type"
```

### Performance Monitoring

```runa
Note: Monitor system resources during processing
Process called "monitor_performance" that takes operation_name as String returns Dictionary[String, Any]:
    Let start_stats be get_runtime_statistics
    Let start_time be start_stats["current_timestamp"]
    
    Note: Perform operation here
    
    Let end_stats be get_runtime_statistics
    Let end_time be end_stats["current_timestamp"]
    
    Return dictionary with:
        "operation" as operation_name,
        "duration_ms" as end_time minus start_time,
        "memory_usage" as end_stats["memory_size_bytes"]
```

The Runa built-ins module provides a solid foundation for all Runa applications, combining natural language syntax with robust functionality. Use these tools to build reliable, maintainable programs that handle errors gracefully and process data efficiently.