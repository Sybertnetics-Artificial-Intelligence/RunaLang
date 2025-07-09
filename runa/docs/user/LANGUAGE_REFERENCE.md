# Runa Language Reference

## Table of Contents

- [Lexical Structure](#lexical-structure)
- [Types and Type System](#types-and-type-system)
- [Variables and Constants](#variables-and-constants)
- [Expressions](#expressions)
- [Statements](#statements)
- [Functions and Processes](#functions-and-processes)
- [Control Flow](#control-flow)
- [Pattern Matching](#pattern-matching)
- [Error Handling](#error-handling)
- [Modules and Imports](#modules-and-imports)
- [Concurrency](#concurrency)
- [Memory Management](#memory-management)
- [Built-in Functions](#built-in-functions)

## Lexical Structure

### Keywords

Runa uses natural English keywords:

**Variable Declaration:**
- `Let` - declares a mutable variable
- `Define` - declares a variable/constant
- `Set` - assigns to an existing variable
- `constant` - marks a definition as constant

**Control Flow:**
- `If`, `Otherwise` - conditional statements
- `Unless`, `When` - alternative conditionals
- `For`, `While`, `Do`, `Repeat` - loops
- `Match`, `Case`, `Default` - pattern matching
- `Break`, `Continue` - loop control
- `Return` - function return

**Types:**
- `Integer`, `Float`, `String`, `Boolean`
- `List`, `Dictionary`, `Array`, `Tuple`
- `Optional`, `Function`
- `Any`, `Void`, `Never`

**Operators:**
- `is equal to`, `is not equal to`
- `is greater than`, `is less than`
- `is greater than or equal to`, `is less than or equal to`
- `plus`, `minus`, `multiplied by`, `divided by`
- `modulo`, `to the power of`
- `and`, `or`, `not`

**Others:**
- `Process`, `called`, `that`, `takes`, `returns`
- `Try`, `Catch`, `Finally`, `Throw`
- `Import`, `Export`, `Module`, `exposing`
- `Async`, `Await`, `Send`, `Atomic`, `Lock`
- `Delete`, `owned`, `borrowed`, `shared`, `lifetime`

### Identifiers

Identifiers can be:
- Single words: `name`, `age`, `total`
- Multi-word with spaces: `user name`, `total price`, `shopping cart`
- Snake_case: `user_name`, `total_price`

### Literals

**Integer Literals:**
```runa
42
-17
0
1000
```

**Float Literals:**
```runa
3.14
-2.5
0.0
1.23e10
```

**String Literals:**
```runa
"Hello, World!"
'Single quotes also work'
"Strings with \"escaped quotes\""
```

**Boolean Literals:**
```runa
true
false
True    // Also accepted
False   // Also accepted
```

**List Literals:**
```runa
list containing 1, 2, 3
list containing "a", "b", "c"
empty list
```

## Types and Type System

### Basic Types

```runa
Let count (Integer) be 42
Let price (Float) be 19.99
Let name (String) be "Alice"
Let is_active (Boolean) be true
```

### Generic Types

```runa
Let numbers (List[Integer]) be list containing 1, 2, 3
Let scores (Array[Float]) be empty
Let mapping (Dictionary[String, Integer]) be empty
Let pair (Tuple[String, Integer]) be ("Alice", 25)
```

### Union Types

```runa
Let value (Integer or String) be 42
Let result (String or Boolean or Integer) be "success"
```

### Optional Types

```runa
Let maybe_name (Optional[String]) be "John"
Let maybe_age (Optional Integer) be 25
```

### Intersection Types

```runa
// For interfaces/traits (future feature)
Let validator (Serializable and Validatable) be some_object
```

### Function Types

```runa
Let callback (Function[Integer, String]) be some_function
Let processor (Function[List[Integer], Boolean]) be another_function
```

## Variables and Constants

### Variable Declaration

```runa
// Mutable variables
Let x be 42
Let name be "Alice"
Let items be list containing 1, 2, 3

// With type annotations
Let age (Integer) be 25
Let message (String) be "Hello"
```

### Constant Declaration

```runa
Define constant PI as 3.14159
Define constant MAX_SIZE as 1000
```

### Assignment

```runa
Let x be 10
Set x to 20
Set x to x plus 5
```

### Memory Annotations

```runa
@owned Let buffer be list containing 1, 2, 3
@borrowed Let reference be some_value
@shared Let shared_data be some_resource
@lifetime(a) Let scoped_value be some_data
```

## Expressions

### Arithmetic Expressions

```runa
Let result be 10 plus 5
Let difference be a minus b
Let product be x multiplied by y
Let quotient be total divided by count
Let remainder be x modulo y
Let power be base to the power of exponent
```

### Comparison Expressions

```runa
If x is equal to y
If a is not equal to b
If score is greater than 90
If age is less than 18
If value is greater than or equal to threshold
If count is less than or equal to limit
```

### Logical Expressions

```runa
If x is greater than 0 and y is less than 10
If name is equal to "admin" or role is equal to "manager"
If not is_valid
```

### Function Calls

```runa
Let result be Calculate Total with items as cart
Let greeting be Format Message with name as "Alice" and greeting as "Hello"
```

### Member Access

```runa
Let user_name be user.name
Let first_item be items[0]
Let length be text.length
```

## Statements

### Expression Statements

```runa
Display "Hello"
Calculate Total with items as cart
```

### Block Statements

Blocks are defined by indentation:

```runa
If condition:
    Display "First line"
    Display "Second line"
    Let x be 42
```

## Functions and Processes

### Function Definition

```runa
Process called "greet" that takes name as String returns String:
    Return "Hello, " followed by name

Process called "add" that takes a as Integer and b as Integer returns Integer:
    Return a plus b
```

### Parameters

```runa
// Single parameter
Process called "square" that takes x as Integer returns Integer:
    Return x multiplied by x

// Multiple parameters
Process called "calculate area" that takes width as Float and height as Float returns Float:
    Return width multiplied by height

// No parameters
Process called "get current time" returns String:
    Return "12:00 PM"
```

### Async Functions

```runa
Async Process called "fetch data" returns String:
    Display "Fetching..."
    Return "data"

// Using async functions
Let result be Await Fetch Data
```

## Control Flow

### If Statements

```runa
If condition:
    Display "True branch"

If x is greater than 0:
    Display "Positive"
Otherwise if x is equal to 0:
    Display "Zero"
Otherwise:
    Display "Negative"
```

### Unless Statements

```runa
Unless is_valid:
    Display "Invalid input"
```

### When Statements

```runa
When user_logged_in:
    Display "Welcome back!"
```

### For Loops

```runa
// For-each
For each item in items:
    Display item

// For-range
For i from 1 to 10:
    Display i

For i from 0 to 100 step 2:
    Display i
```

### While Loops

```runa
While count is less than 10:
    Display count
    Set count to count plus 1
```

### Do-While Loops

```runa
Do:
    Display "At least once"
    Set x to x plus 1
While x is less than 5
```

### Repeat Loops

```runa
Repeat 5 times:
    Display "Hello"
```

## Pattern Matching

### Basic Pattern Matching

```runa
Match value:
    Case 0:
        Display "Zero"
    Case 1:
        Display "One"
    Case _:
        Display "Other"
```

### Pattern with Guards

```runa
Match number:
    Case x If x is greater than 0:
        Display "Positive"
    Case x If x is less than 0:
        Display "Negative"
    Case _:
        Display "Zero"
```

### List Patterns

```runa
Match items:
    Case []:
        Display "Empty list"
    Case [x]:
        Display "Single item"
    Case [first, rest...]:
        Display "First: " followed by first
```

## Error Handling

### Try-Catch-Finally

```runa
Try:
    Let result be risky_operation()
    Display result
Catch RuntimeError as error:
    Display "Runtime error: " followed by error
Catch as general_error:
    Display "Unknown error: " followed by general_error
Finally:
    Display "Cleanup"
```

### Throwing Exceptions

```runa
If invalid_input:
    Throw "Invalid input provided"
```

## Modules and Imports

### Importing Modules

```runa
// Import entire module with alias
Import "math" as math_module

// Import specific functions
Import "utils" exposing calculate, format, validate

// Import from standard library
Import "stdlib/string" exposing split, join, trim
```

### Exporting Symbols

```runa
// Export specific functions
Export calculate_total, format_currency

// Export all symbols
Export all
```

### Module Declaration

```runa
Module "utilities" with:
    Process called "helper" returns String:
        Return "help"
    
    Export helper
```

## Concurrency

### Async/Await

```runa
Async Process called "fetch user" that takes id as Integer returns String:
    Let data be Await fetch_from_api(id)
    Return data

Let user = Await Fetch User with id as 123
```

### Send/Receive (Actor Model)

```runa
Send message to actor
```

### Atomic Operations

```runa
Atomic:
    Set counter to counter plus 1
    Set total to total plus amount
```

### Locking

```runa
Lock shared_resource:
    Display "In critical section"
    Modify shared_resource
```

## Memory Management

### Ownership Annotations

```runa
@owned Let buffer be create_buffer()
@borrowed Let view be buffer
@shared Let reference be shared_data
```

### Lifetime Annotations

```runa
@lifetime(a) Let scoped_reference be some_value
```

### Explicit Cleanup

```runa
Delete large_buffer
```

## Built-in Functions

### Display Functions

```runa
Display "Hello"
Display "Value: " followed by x
Display message with "Prefix: "
```

### Type Conversion

```runa
Let str_num be "42"
Let number be str_num as Integer
Let text be number as String
```

### Collection Operations

```runa
Let length be Length of items
Let is_empty be Is Empty items
Add item to collection
Remove item from collection
```

### String Operations

```runa
Let upper_text be Uppercase text
Let lower_text be Lowercase text
Let trimmed be Trim whitespace from text
```

### Math Operations

```runa
Let absolute = Absolute value of -5
Let rounded = Round 3.7
Let maximum = Maximum of a and b
Let minimum = Minimum of a and b
```

## Grammar Summary

```ebnf
program = statement*

statement = 
    | let_statement
    | define_statement  
    | set_statement
    | if_statement
    | loop_statement
    | match_statement
    | try_statement
    | import_statement
    | export_statement
    | function_definition
    | expression_statement

expression =
    | literal
    | identifier
    | binary_expression
    | function_call
    | member_access

type_expression =
    | basic_type
    | generic_type
    | union_type
    | optional_type
    | function_type
```

## Operator Precedence

From highest to lowest precedence:

1. Member access (`.`, `[]`)
2. Function calls
3. Unary operators (`not`, `-`)
4. Power (`to the power of`)
5. Multiplication/Division (`multiplied by`, `divided by`, `modulo`)
6. Addition/Subtraction (`plus`, `minus`)
7. Comparison (`is greater than`, `is equal to`, etc.)
8. Logical AND (`and`)
9. Logical OR (`or`)

## Reserved Words

All keywords listed in the [Keywords](#keywords) section are reserved and cannot be used as identifiers.

## Style Guide

### Naming Conventions

- Variables: `user_name`, `total_price`
- Functions: `"calculate total"`, `"format currency"`
- Constants: `MAX_SIZE`, `PI`
- Types: `Integer`, `String`, `UserAccount`

### Indentation

Use 4 spaces for indentation (no tabs).

### Line Length

Keep lines under 100 characters when possible.

### Comments

Use `Note:` for explanatory comments:

```runa
Note: This calculates the compound interest
Let interest be principal multiplied by rate
```