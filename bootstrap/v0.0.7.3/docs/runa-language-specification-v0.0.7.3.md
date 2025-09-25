# Runa Language Specification v0.0.7.3

## Overview

This document comprehensively describes the Runa programming language as implemented in the v0.0.7.3 bootstrap compiler. This specification covers every feature, syntax element, and capability available for transpiling the compiler from C to Runa.

## Table of Contents

1. [Basic Syntax](#basic-syntax)
2. [Data Types](#data-types)
3. [Variables](#variables)
4. [Functions (Processes)](#functions-processes)
5. [Control Flow](#control-flow)
6. [Expressions and Operations](#expressions-and-operations)
7. [Type Definitions](#type-definitions)
8. [String Operations](#string-operations)
9. [List Operations](#list-operations)
10. [File I/O](#file-io)
11. [Mathematical Functions](#mathematical-functions)
12. [System Functions](#system-functions)
13. [Inline Assembly](#inline-assembly)
14. [Function Pointers](#function-pointers)
15. [Arrays](#arrays)
16. [Algebraic Data Types (ADTs)](#algebraic-data-types-adts)
17. [Import System](#import-system)
18. [Comments](#comments)
19. [Complete Token Reference](#complete-token-reference)
20. [Grammar Rules](#grammar-rules)

---

## Basic Syntax

### Program Structure
Every Runa program consists of:
- Import statements (optional)
- Type definitions (optional)
- Global variable declarations (optional)
- Function definitions (processes)

### Function Definition Syntax
```runa
Process called "function_name" takes param1 as Type1, param2 as Type2 returns ReturnType:
    # Function body
End Process
```

### Minimal Program Example
```runa
Process called "main" takes argc as Integer, argv as Integer returns Integer:
    Return 42
End Process
```

---

## Data Types

### Built-in Types
- **Integer**: 64-bit signed integer
- **String**: UTF-8 string
- **Character**: Single character

### Type Declaration Examples
```runa
Let x be 42                    # Integer
Let str be "Hello World"       # String literal
Let ch be 'A'                  # Character (single quotes)
```

---

## Variables

### Variable Declaration
```runa
Let variable_name be expression
```

### Variable Assignment
```runa
Set variable_name to expression
```

### Field Assignment
```runa
Set struct_var.field_name to expression
```

### Examples
```runa
Let x be 10
Let y be 20
Set x to x plus y
```

---

## Functions (Processes)

### Function Definition
```runa
Process called "function_name" takes param1 as Type1, param2 as Type2 returns ReturnType:
    # Function body
    Return expression
End Process
```

### Function Call
```runa
function_name(arg1, arg2)
```

### Examples
```runa
Process called "add" takes a as Integer, b as Integer returns Integer:
    Return a plus b
End Process

Process called "main" takes argc as Integer, argv as Integer returns Integer:
    Let result be add(10, 20)
    Return result
End Process
```

---

## Control Flow

### If Statement
```runa
If condition:
    # statements
Otherwise:
    # statements
End If
```

### Multi-condition If (Otherwise If)
```runa
If condition1:
    # statements
Otherwise If condition2:
    # statements
Otherwise:
    # statements
End If
```

### While Loop
```runa
While condition:
    # statements
End While
```

### Break and Continue
```runa
While condition:
    If some_condition:
        Break
    End If
    If other_condition:
        Continue
    End If
    # more statements
End While
```

### Examples
```runa
Process called "factorial" takes n as Integer returns Integer:
    Let result be 1
    Let i be 1
    While i is less than n plus 1:
        Set result to result multiplied by i
        Set i to i plus 1
    End While
    Return result
End Process
```

---

## Expressions and Operations

### Arithmetic Operations
- `plus` - Addition
- `minus` - Subtraction
- `multiplied by` - Multiplication
- `divided by` - Division
- `modulo by` - Modulo

### Comparison Operations
- `is equal to` - Equality
- `is not equal to` - Inequality
- `is less than` - Less than
- `is greater than` - Greater than
- `is less than or equal to` - Less than or equal
- `is greater than or equal to` - Greater than or equal

### Logical Operations
- `and` - Logical AND
- `or` - Logical OR
- `not` - Logical NOT

### Bitwise Operations
- `bit_and` - Bitwise AND
- `bit_or` - Bitwise OR
- `bit_xor` - Bitwise XOR
- `bit_shift_left by` - Left shift
- `bit_shift_right by` - Right shift

### Examples
```runa
Let a be 10
Let b be 20
Let sum be a plus b
Let is_greater be a is greater than b
Let bitwise_result be a bit_and b
```

---

## Type Definitions

### Struct Types
```runa
Type called "TypeName":
    field1 as Type1,
    field2 as Type2,
    field3 as Type3
End Type
```

### Example
```runa
Type called "Point":
    x as Integer,
    y as Integer
End Type

Process called "main" takes argc as Integer, argv as Integer returns Integer:
    Let p be Point
    Set p.x to 10
    Set p.y to 20
    Let sum be p.x plus p.y
    Return sum
End Process
```

---

## String Operations

### String Functions
- `string_length(str)` - Get string length
- `string_char_at(str, index)` - Get character at index
- `string_substring(str, start, length)` - Extract substring
- `string_equals(str1, str2)` - Compare strings for equality
- `string_concat(str1, str2)` - Concatenate strings
- `string_compare(str1, str2)` - Compare strings lexicographically
- `string_to_integer(str)` - Convert string to integer
- `integer_to_string(num)` - Convert integer to string
- `string_find(haystack, needle)` - Find substring position
- `string_replace(str, old, new)` - Replace substring
- `string_trim(str)` - Remove leading/trailing whitespace
- `string_split(str, delimiter)` - Split string by delimiter

### Character Functions
- `ascii_value_of(char)` - Get ASCII value
- `is_digit(char)` - Check if character is digit
- `is_alpha(char)` - Check if character is alphabetic
- `is_whitespace(char)` - Check if character is whitespace

### Examples
```runa
Let str1 be "Hello"
Let str2 be " World"
Let result be string_concat(str1, str2)
Let length be string_length(result)
Let substring be string_substring(result, 0, 5)
```

---

## List Operations

### Basic List Functions
- `list_create()` - Create new list
- `list_append(list, item)` - Append item to list
- `list_get(list, index)` - Get item at index
- `list_get_integer(list, index)` - Get integer item at index
- `list_length(list)` - Get list length
- `list_destroy(list)` - Destroy list

### Enhanced List Functions
- `list_set(list, index, value)` - Set value at index
- `list_insert(list, index, value)` - Insert value at index
- `list_remove(list, index)` - Remove item at index
- `list_clear(list)` - Clear all items
- `list_find(list, value)` - Find value in list
- `list_sort(list)` - Sort list
- `list_reverse(list)` - Reverse list
- `list_copy(list)` - Copy list
- `list_merge(list1, list2)` - Merge two lists

### Examples
```runa
Let my_list be list_create()
list_append(my_list, "Hello")
list_append(my_list, "World")
Let count be list_length(my_list)
Let item be list_get(my_list, 0)
```

---

## File I/O

### Basic File Operations
- `read_file(filename)` - Read entire file as string
- `write_file(filename, content)` - Write string to file

### Enhanced File Operations
- `file_open(filename, mode)` - Open file with mode
- `file_close(handle)` - Close file handle
- `file_read_line(handle)` - Read line from file
- `file_write_line(handle, content)` - Write line to file
- `file_exists(filename)` - Check if file exists
- `file_delete(filename)` - Delete file
- `file_size(filename)` - Get file size
- `file_seek(handle, position)` - Seek to position
- `file_tell(handle)` - Get current position
- `file_eof(handle)` - Check end of file

### Examples
```runa
Let content be read_file("input.txt")
Let result be write_file("output.txt", "Hello World")

Let handle be file_open("data.txt", "r")
Let line be file_read_line(handle)
file_close(handle)
```

---

## Mathematical Functions

### Math Operations
- `sin(x)` - Sine function
- `cos(x)` - Cosine function
- `tan(x)` - Tangent function
- `sqrt(x)` - Square root
- `pow(base, exponent)` - Power function
- `abs(x)` - Absolute value
- `floor(x)` - Floor function
- `ceil(x)` - Ceiling function
- `min(a, b)` - Minimum value
- `max(a, b)` - Maximum value
- `random()` - Random number
- `log(x)` - Natural logarithm
- `exp(x)` - Exponential function

### Examples
```runa
Let angle be 3.14159
Let sine_val be sin(angle)
Let power_val be pow(2, 8)
Let random_val be random()
```

---

## System Functions

### System Operations
- `get_command_line_args()` - Get command line arguments
- `exit_with_code(code)` - Exit with status code
- `panic(message)` - Panic with error message
- `assert(condition)` - Assert condition
- `allocate(size)` - Allocate memory
- `deallocate(ptr)` - Deallocate memory

### Examples
```runa
Let args be get_command_line_args()
assert(args is not equal to 0)
exit_with_code(0)
```

---

## Inline Assembly

### Syntax
```runa
Inline Assembly:
    "assembly instruction 1"    Note: Optional comment
    "assembly instruction 2"    Note: Another comment
    : "output_constraints"
    : "input_constraints"
    : "clobber_list"
End Assembly
```

### Example
```runa
Let result be 0
Inline Assembly:
    "movq $42, %rax"     Note: Load immediate value 42 into rax
    "movq %rax, %0"      Note: Store result to output variable
    : "=r"(result)
    :
    : "rax"
End Assembly
```

---

## Function Pointers

### Function Pointer Type Declaration
```runa
Type FunctionPtr is Pointer of Process that takes Integer, Integer returns Integer
```

### Function Pointer Usage
```runa
Let func_ptr be add    # Point to function 'add'
Let result be func_ptr(10, 20)  # Call through pointer
```

### Example
```runa
Process called "add" takes a as Integer, b as Integer returns Integer:
    Return a plus b
End Process

Process called "multiply" takes a as Integer, b as Integer returns Integer:
    Return a multiplied by b
End Process

Process called "main" takes argc as Integer, argv as Integer returns Integer:
    Let operation be add
    Let result be operation(5, 3)
    Return result
End Process
```

---

## Arrays

### Array Type Declaration
```runa
Type IntArray is Array of Integer with length 10
```

### Array Usage
```runa
Let arr be IntArray
Set arr[0] to 42
Let value be arr[0]
```

### Example
```runa
Type called "Matrix":
    data as Array of Integer with length 100
End Type

Process called "main" takes argc as Integer, argv as Integer returns Integer:
    Let matrix be Matrix
    Set matrix.data[0] to 42
    Return matrix.data[0]
End Process
```

---

## Algebraic Data Types (ADTs)

### ADT Definition
```runa
Type TypeName is
    | Variant1 with field1 as Type1 and field2 as Type2
    | Variant2 with field1 as Type1
    | Variant3
```

### Pattern Matching
```runa
Match expression:
    When Variant1 with field1 as var1 and field2 as var2:
        # statements
    End When
    When Variant2 with field1 as var1:
        # statements
    End When
    When Variant3:
        # statements
    End When
End Match
```

### Complete Example
```runa
Type Shape is
    | Circle with radius as Integer
    | Rectangle with width as Integer and height as Integer

Process called "test_shapes" returns Integer:
    Let shape1 be Circle with radius as 5

    Match shape1:
        When Circle with radius as r:
            Print r
        End When
        When Rectangle with width as w and height as h:
            Print w
            Print h
        End When
    End Match

    Let shape2 be Rectangle with width as 10 and height as 20

    Match shape2:
        When Circle with radius as r:
            Print r
        End When
        When Rectangle with width as w and height as h:
            Print w
            Print h
        End When
    End Match

    Return 0
End Process
```

---

## Import System

### Import Syntax
```runa
Import "filename" as ModuleName
```

### Example
```runa
Import "utils" as Utils
Import "math_helpers" as Math

Process called "main" takes argc as Integer, argv as Integer returns Integer:
    # Use imported functions
    Return 0
End Process
```

---

## Comments

### Single Line Comments
```runa
# This is a comment
Let x be 42  # Comment at end of line
```

Comments start with `#` and continue to end of line.

---

## Complete Token Reference

### Keywords
- `Process` - Function definition
- `called` - Function name introducer
- `takes` - Parameter list introducer
- `as` - Type specifier
- `returns` - Return type specifier
- `End` - Block terminator
- `Let` - Variable declaration
- `be` - Assignment operator for Let
- `Set` - Variable assignment
- `to` - Assignment operator for Set
- `Return` - Return statement
- `If` - Conditional statement
- `Otherwise` - Else clause
- `Otherwise If` - Else if clause
- `While` - Loop statement
- `Break` - Break statement
- `Continue` - Continue statement
- `Print` - Print statement
- `Type` - Type definition
- `Import` - Import statement
- `Match` - Pattern matching
- `When` - Pattern matching case
- `with` - ADT field specifier
- `and` - Multiple field separator
- `Inline` - Inline assembly
- `Assembly` - Assembly block
- `Note` - Assembly comment
- `Pointer` - Function pointer type
- `of` - Type specifier for pointers
- `that` - Function signature introducer
- `Array` - Array type
- `length` - Array length specifier

### Built-in Types
- `Integer` - 64-bit signed integer
- `String` - UTF-8 string
- `Character` - Single character

### Operators
- `plus` - Addition
- `minus` - Subtraction
- `multiplied` - Multiplication (use with `by`)
- `divided` - Division (use with `by`)
- `modulo` - Modulo (use with `by`)
- `by` - Operator modifier
- `is` - Comparison introducer
- `equal` - Equality comparison
- `not` - Negation
- `less` - Less than comparison
- `greater` - Greater than comparison
- `than` - Comparison modifier
- `and` - Logical AND
- `or` - Logical OR

### Bitwise Operators
- `bit_and` - Bitwise AND
- `bit_or` - Bitwise OR
- `bit_xor` - Bitwise XOR
- `bit_shift_left` - Left shift
- `bit_shift_right` - Right shift

### Punctuation
- `:` - Colon (block introducer)
- `.` - Dot (field access)
- `,` - Comma (separator)
- `(` - Left parenthesis
- `)` - Right parenthesis
- `[` - Left bracket (array indexing)
- `]` - Right bracket
- `|` - Pipe (ADT variant separator)
- `"` - String literal delimiter

---

## Grammar Rules

### Program Structure
```
Program ::= (Import | TypeDefinition | GlobalVariable | Function)*

Import ::= "Import" StringLiteral "as" Identifier

GlobalVariable ::= "Let" Identifier "be" Expression

TypeDefinition ::= StructType | VariantType | FunctionPtrType | ArrayType

StructType ::= "Type" "called" StringLiteral ":" (TypeField ",")* TypeField "End" "Type"

VariantType ::= "Type" Identifier "is" ("|" Variant)+

ArrayType ::= "Type" Identifier "is" "Array" "of" TypeName "with" "length" Integer

Function ::= "Process" "called" StringLiteral "takes" ParameterList "returns" TypeName ":" StatementList "End" "Process"
```

### Statements
```
Statement ::= LetStatement | SetStatement | ReturnStatement | IfStatement |
              WhileStatement | PrintStatement | BreakStatement | ContinueStatement |
              MatchStatement | InlineAssembly | ExpressionStatement

LetStatement ::= "Let" Identifier "be" Expression

SetStatement ::= "Set" LValue "to" Expression

ReturnStatement ::= "Return" Expression

IfStatement ::= "If" Expression ":" StatementList
                ("Otherwise" "If" Expression ":" StatementList)*
                ("Otherwise" ":" StatementList)?
                "End" "If"

WhileStatement ::= "While" Expression ":" StatementList "End" "While"

MatchStatement ::= "Match" Expression ":" (MatchCase)* "End" "Match"

MatchCase ::= "When" Identifier ("with" FieldPattern ("and" FieldPattern)*)? ":"
              StatementList "End" "When"
```

### Expressions
```
Expression ::= ComparisonExpr

ComparisonExpr ::= ArithmeticExpr (ComparisonOp ArithmeticExpr)?

ComparisonOp ::= "is" "equal" "to" | "is" "not" "equal" "to" |
                 "is" "less" "than" | "is" "greater" "than" |
                 "is" "less" "than" "or" "equal" "to" |
                 "is" "greater" "than" "or" "equal" "to"

ArithmeticExpr ::= Term (("plus" | "minus") Term)*

Term ::= Factor (("multiplied" "by" | "divided" "by" | "modulo" "by") Factor)*

Factor ::= Integer | StringLiteral | Identifier | FunctionCall | FieldAccess |
           ArrayIndex | VariantConstructor | "(" Expression ")"

FunctionCall ::= Identifier "(" (Expression ",")* Expression? ")"

FieldAccess ::= Expression "." Identifier

ArrayIndex ::= Expression "[" Expression "]"

VariantConstructor ::= Identifier "with" FieldAssignment ("and" FieldAssignment)*

FieldAssignment ::= Identifier "as" Expression
```

This specification covers every feature available in the Runa v0.0.7.3 bootstrap compiler and provides the complete syntax and semantics needed for transpiling the C implementation to Runa.

---

## Usage Notes for Transpilation

When transpiling the v0.0.7.3 C compiler to Runa:

1. **Memory Management**: Use `allocate()` and `deallocate()` for dynamic memory
2. **Error Handling**: Use `panic()` and `assert()` for error conditions
3. **String Handling**: Leverage the comprehensive string manipulation functions
4. **Data Structures**: Use ADTs for complex data modeling and structs for simple records
5. **File Operations**: Use enhanced file I/O for compiler input/output handling
6. **Function Pointers**: Use for callback mechanisms and function tables
7. **Inline Assembly**: Use sparingly for performance-critical sections
8. **Arrays**: Use for fixed-size data collections like token arrays

The language provides all necessary features to implement a complete compiler while maintaining readability and safety through its high-level syntax.