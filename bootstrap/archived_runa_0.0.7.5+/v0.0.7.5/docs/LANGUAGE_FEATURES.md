# Runa v0.0.7.5 Implemented Language Features

## Overview

This document details which language features from the complete Runa specification are implemented in v0.0.7.5. This version represents a bootstrap compiler with a minimal but complete feature set.

## Implementation Status

### Core Language (Fully Implemented)

#### Process Definitions
**Status:** Complete

```runa
Process called "name" takes param1 as Type1, param2 as Type2 returns ReturnType:
    # statements
End Process
```

**Features:**
- Named processes (functions)
- Multiple parameters with type annotations
- Return type specifications
- Return statements
- Process calls with arguments

#### Variables
**Status:** Complete

```runa
Let variable_name be expression
```

**Features:**
- Variable declarations
- Variable assignments
- Variable scoping (local to process)
- Type inference from initialization

#### Expressions
**Status:** Complete

**Arithmetic Operations:**
- `plus` (+)
- `minus` (-)
- `multiplied by` (*)
- `divided by` (/)
- `modulo by` (%)

**Comparison Operations:**
- `is equal to` (==)
- `is not equal to` (!=)
- `is less than` (<)
- `is greater than` (>)
- `is less than or equal to` (<=)
- `is greater than or equal to` (>=)

**Logical Operations:**
- `and` (&&)
- `or` (||)
- `not` (!)

**Other:**
- Parenthesized expressions
- Integer literals
- String literals
- Variable references
- Function calls
- Field access (dot notation)

#### Control Flow
**Status:** Complete

**Conditionals:**
```runa
If condition:
    # statements
Otherwise:
    # statements
End If
```

**Loops:**
```runa
While condition:
    # statements
End While
```

**Features:**
- Nested conditionals
- Nested loops
- Break statements (partial)
- Continue statements (partial)

#### Type System (Partial)
**Status:** Partial Implementation

**Implemented:**
```runa
Type CustomType is:
    field1 as Integer
    field2 as Integer
End Type
```

- Custom type definitions
- Struct-like types with fields
- Field access via dot notation
- Type size calculation

**Not Implemented:**
- Arrays (syntax exists but limited support)
- Enums/Unions (Match/When partially implemented)
- Type inference beyond basic cases
- Generic types
- Type aliases

#### Pattern Matching (Partial)
**Status:** Syntax parsed, limited codegen

```runa
Match expression:
    When variant_name with field1, field2:
        # statements
    Otherwise:
        # statements
End Match
```

**Status:** Parser recognizes syntax, codegen has basic structure but untested

### Builtin Functions (Complete)

#### String Operations
- `print_string(str: Integer) -> Integer` - Print to stdout
- `string_concat(str1: Integer, str2: Integer) -> Integer` - Concatenate
- `string_length(str: Integer) -> Integer` - Get length
- `string_equals(str1: Integer, str2: Integer) -> Integer` - Compare
- `string_substring(str: Integer, start: Integer, length: Integer) -> Integer` - Extract substring
- `string_char_at(str: Integer, index: Integer) -> Integer` - Get character
- `integer_to_string(n: Integer) -> Integer` - Convert to string
- `string_to_integer(str: Integer) -> Integer` - Parse integer

#### Integer Operations
- `print_integer(n: Integer) -> Integer` - Print to stdout

#### Memory Operations
- `allocate(size: Integer) -> Integer` - Allocate heap memory
- `deallocate(ptr: Integer) -> Integer` - Free memory
- `memory_get_integer(ptr: Integer, offset: Integer) -> Integer` - Read integer
- `memory_set_integer(ptr: Integer, offset: Integer, value: Integer) -> Integer` - Write integer
- `memory_get_pointer(ptr: Integer, offset: Integer) -> Integer` - Read pointer
- `memory_set_pointer(ptr: Integer, offset: Integer, value: Integer) -> Integer` - Write pointer
- `memory_get_byte(ptr: Integer, offset: Integer) -> Integer` - Read byte
- `memory_set_byte(ptr: Integer, offset: Integer, value: Integer) -> Integer` - Write byte
- `memory_get_int32(ptr: Integer, offset: Integer) -> Integer` - Read 32-bit int
- `memory_set_int32(ptr: Integer, offset: Integer, value: Integer) -> Integer` - Write 32-bit int
- `memory_copy(dest: Integer, src: Integer, size: Integer) -> Integer` - Copy memory
- `memory_reallocate(ptr: Integer, size: Integer) -> Integer` - Resize allocation

#### File Operations
- `file_write_fd(fd: Integer, str: Integer, mode: Integer) -> Integer` - Write to file descriptor
- `file_close_fd(fd: Integer) -> Integer` - Close file descriptor
- `runtime_read_file(filename: Integer) -> Integer` - Read entire file

#### System Operations
- `get_command_line_arg(index: Integer) -> Integer` - Get argv[index]

### Features NOT Implemented in v0.0.7.5

#### Advanced Type System
- **Arrays:** Syntax exists but codegen incomplete
- **Generics:** Not implemented
- **Type aliases:** Not implemented
- **Type inference:** Limited to basic cases
- **Union types:** Partial parser support only

#### Advanced Control Flow
- **For loops:** Not implemented
- **Do-while loops:** Not implemented
- **Switch statements:** Not implemented (Match exists but limited)
- **Labeled breaks/continues:** Not implemented

#### Module System
- **Import statements:** Not implemented
- **Export declarations:** Not implemented
- **Module namespacing:** Not implemented
- **Package management:** Not implemented

#### Object-Oriented Features
- **Classes:** Not planned for bootstrap
- **Inheritance:** Not planned for bootstrap
- **Interfaces:** Not planned for bootstrap
- **Methods:** Not planned for bootstrap

#### Functional Features
- **Lambda expressions:** Not implemented
- **Closures:** Not implemented
- **Higher-order functions:** Can pass function pointers manually
- **Pattern matching (full):** Partial implementation only

#### Advanced Features
- **Macros:** Not implemented
- **Compile-time evaluation:** Not implemented
- **Inline assembly:** Not implemented (coming in v0.0.8)
- **Foreign function interface:** Manual only
- **Concurrency primitives:** Not implemented
- **Exceptions:** Not implemented

#### Standard Library
- **Collections:** Not implemented (must build manually)
- **I/O library:** Basic file operations only
- **Math library:** Basic arithmetic only
- **Networking:** Not implemented
- **JSON/XML parsing:** Not implemented
- **Regular expressions:** Not implemented

### Specification Compliance

| Feature Category | Implementation Status |
|-----------------|----------------------|
| Basic syntax | 100% |
| Process definitions | 100% |
| Variables | 100% |
| Expressions | 100% |
| Control flow (if/while) | 100% |
| Type declarations | 80% |
| Pattern matching | 30% |
| Arrays | 20% |
| Module system | 0% |
| Standard library | 10% |
| **Overall** | **~60%** |

## Language Differences from Specification

### Syntax Variations

The v0.0.7.5 implementation uses slightly different syntax than some specification documents:

**Type Declarations:**
```runa
# v0.0.7.5 syntax (implemented)
Type Name is:
    field as Integer
End Type

# Some specs show (not implemented)
type Name {
    field: Integer
}
```

**Array Syntax:**
```runa
# Specified in docs but not fully implemented
Type Array is: array[10] of Integer
```

### Calling Conventions

v0.0.7.5 uses System V AMD64 ABI for x86-64 Linux. Other platforms and ABIs are not supported.

### String Representation

Strings are null-terminated C-style strings (pointers to char arrays). There is no separate string type or string object.

## Compiler Behavior

### Type Checking

Limited type checking is performed:
- Integer vs pointer distinction
- Basic type size calculations
- No comprehensive type safety

### Error Handling

The compiler reports syntax errors but may not catch all semantic errors:
- Use of undeclared variables may not be caught
- Type mismatches may generate invalid assembly
- Stack overflow is not detected

### Optimization

No optimization is performed. Generated code is:
- Unoptimized
- Verbose
- Naive register allocation
- No inlining
- No constant folding

## Future Versions

### v0.0.8 (Planned)
- Inline assembly support
- Better error messages

### v0.0.9 (Planned)
- Native object file generation
- Custom linker
- Removes dependency on GNU toolchain

### v0.1.0+ (Future)
- Complete array support
- Full pattern matching
- Module system
- Standard library
- Multiple platforms

## Testing Coverage

The following test programs are included and verified working:

- `test_minimal.runa` - Minimal main function
- `test_let.runa` - Variable declarations
- `test_if.runa` - Conditional statements
- `test_args.runa` - Command line argument handling
- `test_strings.runa` - String operations
- `test_file.runa` - File I/O
- `test_compiler.runa` - Self-compilation test

All tests pass with the v0.0.7.5 compiler.

## Compatibility Notes

### Backward Compatibility

v0.0.7.5 is compatible with v0.0.7.3 source code (the C bootstrap). All v0.0.7.3 features are preserved.

### Forward Compatibility

Code written for v0.0.7.5 will be compatible with future versions, but new features will be added that are not available in v0.0.7.5.

## Conclusion

Runa v0.0.7.5 implements a minimal but complete subset of the Runa language specification. It is sufficient for writing the compiler itself and other systems programming tasks, but lacks many convenience features planned for future versions.

The focus of v0.0.7.5 is **correctness and self-hosting capability**, not feature completeness. Future versions will expand the feature set while maintaining compatibility with this bootstrap foundation.