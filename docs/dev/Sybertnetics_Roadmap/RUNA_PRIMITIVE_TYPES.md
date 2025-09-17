# Runa Primitive Types Documentation

## Overview
This document defines the primitive (built-in) types available in Runa that exist at the language level and do not depend on the standard library. These are the only types available to the compiler itself.

## Core Primitive Types

### 1. **Integer**
- 64-bit signed integer (-9,223,372,036,854,775,808 to 9,223,372,036,854,775,807)
- Default numeric type
- Literals: `42`, `-17`, `0`
- Operations: `plus`, `minus`, `times`, `divided by`, `modulo`
- Comparisons: `equal to`, `not equal to`, `greater than`, `less than`, `greater than or equal to`, `less than or equal to`

### 2. **Float**
- 64-bit floating point (IEEE 754 double precision)
- Literals: `3.14`, `-0.5`, `1.0e10`
- Operations: Same as Integer plus transcendental functions via external calls
- Note: Float literals must contain a decimal point or exponential notation

### 3. **Boolean**
- Binary truth value
- Literals: `true`, `false`
- Operations: `and`, `or`, `not`
- Used in conditionals and control flow

### 4. **String**
- UTF-8 encoded text
- Immutable sequence of characters
- Literals: `"Hello"`, `"Line 1\nLine 2"`
- Operations: Concatenation via `+` operator
- Built-in: `.length()`, `.starts_with()`, `.contains()`, `.split()`

### 5. **Character**
- Single Unicode code point
- Literals: `'a'`, `'β'`, `'\n'`
- Can be converted to/from Integer (Unicode value)

### 6. **Nothing**
- Unit type representing absence of value
- Only value: `nothing`
- Used as return type for procedures with no return value
- Cannot be stored in variables

### 7. **Any**
- Top type that can hold any value
- Used for generic/dynamic typing scenarios
- Requires runtime type checking for operations
- Cast required to use as specific type: `value as Integer`

## Primitive Type Syntax

### Variable Declaration
```runa
Let x be 42                    Note: Integer
Let pi be 3.14159              Note: Float  
Let flag be true               Note: Boolean
Let name be "Alice"            Note: String
Let initial be 'A'             Note: Character
```

### Type Annotations
```runa
Let count as Integer be 0
Let rate as Float be 0.05
Let active as Boolean be false
Let label as String be "default"
Let marker as Character be 'X'
```

### Function Signatures
```runa
Process called "calculate" that takes x as Integer, y as Integer returns Integer:
    Return x plus y
End Process

Process called "print" that takes message as String returns Nothing:
    Note: Prints to console
End Process
```

## Composite Types (NOT Primitives)

These types are defined in the standard library and are NOT available to the compiler:

- `List[T]` - Dynamic array (stdlib/collections)
- `Dictionary[K,V]` - Hash map (stdlib/collections)  
- `Optional[T]` - Maybe type (stdlib/types)
- `Result[T,E]` - Error handling (stdlib/types)
- `Set[T]` - Unique collection (stdlib/collections)
- `Tuple[...]` - Fixed-size heterogeneous collection (stdlib/types)

## Compiler-Internal Structures

For the compiler's own use, we define minimal internal structures that don't depend on stdlib. These are defined in `compiler/backend/syscalls/compiler_internals.runa`.

## Type Conversion

### Implicit Conversions
- None (Runa requires explicit conversions for type safety)

### Explicit Conversions
```runa
Let i as Integer be 65
Let c as Character be i as Character    Note: Results in 'A'

Let s as String be "123"
Let n as Integer be parse_integer(s)     Note: Requires parsing function
```

## Memory Representation

### Size in Bytes
- Integer: 8 bytes
- Float: 8 bytes  
- Boolean: 1 byte (may be padded for alignment)
- Character: 4 bytes (UTF-32 internally)
- String: Variable (pointer + length + capacity)
- Nothing: 0 bytes (compile-time only)
- Any: Variable (tagged union)

## Notes for Compiler Development

1. **The compiler can ONLY use these primitive types** - no stdlib dependencies
2. **Arrays must be handled specially** - use pointer + size internally
3. **Error handling** - use Integer error codes, not Optional/Result
4. **Collections** - implement minimal versions in compiler_internals if needed
5. **String operations** - many are compiler built-ins, not library functions

## Built-in Operations

### Integer Operations
- Arithmetic: `plus`, `minus`, `times`, `divided by`, `modulo`
- Bitwise: `shifted left by`, `shifted right by`, `bitwise and`, `bitwise or`, `bitwise xor`, `bitwise not`
- Comparison: `equal to`, `not equal to`, `greater than`, `less than`, `greater than or equal to`, `less than or equal to`

### String Operations (Compiler Built-ins)
- `string1 + string2` - Concatenation
- `string.length()` - Get length
- `string.char_at(index)` - Get character at index
- `string.substring(start, end)` - Extract substring
- `string.index_of(substring)` - Find substring position

### Type Checking
- `value is Integer` - Runtime type check
- `value as Integer` - Runtime type cast (may panic)

## Important Constraints

1. **No null/nil** - Runa has no null value. Use explicit error handling.
2. **No implicit numeric conversions** - Integer and Float are distinct
3. **Strings are immutable** - All string operations return new strings
4. **No pointer arithmetic** - Memory addresses are opaque
5. **No undefined behavior** - All operations have defined semantics