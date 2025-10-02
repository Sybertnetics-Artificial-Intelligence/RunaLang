# Runa v0.0.7.5 Compiler Usage Guide

## Overview

The Runa v0.0.7.5 compiler (`runac`) is a self-hosting compiler that translates Runa source code into x86-64 assembly language. This guide covers installation, usage, and practical examples.

## Installation

### Prerequisites

- Linux x86-64 system
- GNU Assembler (`as`)
- GCC compiler and linker
- Standard C library development files

### Building from Source

1. Navigate to the bootstrap directory:
```bash
cd runa/bootstrap/v0.0.7.5
```

2. Build the compiler using the Makefile:
```bash
make build
```

This will create the compiler executable at `build/runac`.

### Verifying Installation

Test the compiler with a simple program:
```bash
echo 'Process called "main" takes argc as Integer, argv as Integer returns Integer:
    Return 0
End Process' > test.runa

./build/runac test.runa test.s
```

If successful, you'll see:
```
Successfully compiled 'test.runa' to 'test.s'
```

## Basic Usage

### Command Line Interface

```bash
runac <input.runa> <output.s>
```

**Parameters:**
- `<input.runa>`: Path to Runa source file
- `<output.s>`: Path for generated assembly output

**Example:**
```bash
./build/runac my_program.runa my_program.s
```

### Assembling and Linking

After compilation, assemble and link the output:

```bash
# Assemble to object file
as --64 my_program.s -o my_program.o

# Link with runtime
gcc my_program.o -lm -ldl -lpthread -Wl,--export-dynamic -o my_program

# Run
./my_program
```

## Complete Workflow Example

### Step 1: Write Runa Code

Create `hello.runa`:
```runa
Process called "main" takes argc as Integer, argv as Integer returns Integer:
    print_string("Hello, World!")
    Return 0
End Process
```

### Step 2: Compile

```bash
./build/runac hello.runa hello.s
```

### Step 3: Assemble

```bash
as --64 hello.s -o hello.o
```

### Step 4: Link

```bash
gcc hello.o -lm -ldl -lpthread -Wl,--export-dynamic -o hello
```

### Step 5: Execute

```bash
./hello
# Output: Hello, World!
```

## Supported Language Features

### Process Definitions

```runa
Process called "function_name" takes param1 as Integer, param2 as Integer returns Integer:
    # Function body
    Return value
End Process
```

### Variables

```runa
Let variable_name be expression
```

### Control Flow

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

### Expressions

**Arithmetic:**
- `plus`, `minus`, `multiplied by`, `divided by`, `modulo`

**Comparison:**
- `is equal to`, `is not equal to`
- `is less than`, `is greater than`
- `is less than or equal to`, `is greater than or equal to`

**Logical:**
- `and`, `or`, `not`

### Type System

**Built-in Types:**
- `Integer` - 64-bit signed integer
- `String` - null-terminated string pointer

**Type Declarations:**
```runa
Type Point is:
    x as Integer
    y as Integer
End Type
```

### Builtin Functions

**String Operations:**
- `print_string(str)` - Print string to stdout
- `string_concat(str1, str2)` - Concatenate strings
- `string_length(str)` - Get string length
- `string_equals(str1, str2)` - Compare strings
- `integer_to_string(n)` - Convert integer to string

**Integer Operations:**
- `print_integer(n)` - Print integer to stdout

**Memory Management:**
- `allocate(size)` - Allocate memory
- `deallocate(ptr)` - Free memory
- `memory_get_integer(ptr, offset)` - Read integer from memory
- `memory_set_integer(ptr, offset, value)` - Write integer to memory
- `memory_get_pointer(ptr, offset)` - Read pointer from memory
- `memory_set_pointer(ptr, offset, value)` - Write pointer to memory

**File Operations:**
- `file_write_fd(fd, str, mode)` - Write string to file descriptor
- `file_close_fd(fd)` - Close file descriptor

**System:**
- `get_command_line_arg(index)` - Get command line argument

## Compiler Output

### Assembly Format

The compiler generates GNU AS syntax x86-64 assembly with the following structure:

```assembly
.section .rodata
.STR0:    .string "string literals"

.text
.globl function_name
function_name:
    pushq %rbp
    movq %rsp, %rbp
    # function body
    popq %rbp
    ret
```

### Register Usage

The compiler follows System V AMD64 ABI conventions:
- `%rax` - Return value
- `%rdi, %rsi, %rdx, %rcx, %r8, %r9` - First 6 function arguments
- `%rbp` - Frame pointer
- `%rsp` - Stack pointer

## Error Messages

### Compilation Errors

The compiler provides detailed error messages with line numbers:

```
[PARSER ERROR] Expected identifier after Let at line 5
[PARSER ERROR] Expected 'End Process' at line 10
```

### Common Issues

**File Not Found:**
```
[MAIN ERROR] Could not open input file 'missing.runa'
```

**Syntax Errors:**
- Missing `End Process`, `End If`, `End While`
- Invalid operators or expressions
- Mismatched parentheses

## Advanced Usage

### Multi-Module Programs

The v0.0.7.5 compiler operates on single files. For multi-module programs, compile each module separately and link:

```bash
./build/runac module1.runa module1.s
./build/runac module2.runa module2.s

as --64 module1.s -o module1.o
as --64 module2.s -o module2.o

gcc module1.o module2.o -lm -ldl -lpthread -Wl,--export-dynamic -o program
```

### Debugging Generated Assembly

View the generated assembly:
```bash
less output.s
```

Check specific sections:
```bash
# View string literals
grep ".STR" output.s

# View function definitions
grep ".globl" output.s
```

## Limitations

### Current Limitations

1. **Single Source File:** Each compilation operates on one file
2. **No Optimization:** Generated code is unoptimized
3. **Limited Type System:** Only integers and pointers
4. **No Floating Point:** Integer arithmetic only
5. **No Inline Assembly:** Cannot embed assembly (coming in v0.0.8)
6. **External Toolchain:** Requires GNU assembler and linker

### Platform Requirements

- **OS:** Linux only
- **Architecture:** x86-64 only
- **ABI:** System V AMD64

## Performance Considerations

### Compilation Speed

The compiler processes approximately 1000 lines per second on modern hardware.

### Output Size

Generated assembly is verbose (unoptimized). Typical expansion:
- 1 line of Runa → 5-10 lines of assembly

### Runtime Performance

Generated code performs comparably to interpreted languages but slower than optimized C code.

## Troubleshooting

### Compiler Crashes

If the compiler crashes:
1. Check input file for syntax errors
2. Verify file is valid UTF-8
3. Ensure file ends with newline
4. Report issue with minimal reproduction case

### Linker Errors

**Undefined reference to `main`:**
- Ensure your Runa file has a `main` process

**Undefined reference to builtin functions:**
- These are resolved at link time from the C runtime
- Ensure you link with `-ldl -lpthread`

### Empty Output Files

If the compiler produces empty `.s` files:
- Check for parser errors in output
- Verify input file has valid syntax
- Ensure `main` process exists

## Examples

### Hello World

```runa
Process called "main" takes argc as Integer, argv as Integer returns Integer:
    print_string("Hello, World!")
    Return 0
End Process
```

### Factorial Function

```runa
Process called "factorial" takes n as Integer returns Integer:
    If n is less than or equal to 1:
        Return 1
    End If
    Let n_minus_1 be n minus 1
    Let factorial_result be factorial(n_minus_1)
    Let result be n multiplied by factorial_result
    Return result
End Process

Process called "main" takes argc as Integer, argv as Integer returns Integer:
    Let result be factorial(5)
    print_integer(result)
    Return 0
End Process
```

### String Manipulation

```runa
Process called "main" takes argc as Integer, argv as Integer returns Integer:
    Let greeting be "Hello"
    Let name be "Runa"
    Let message be string_concat(greeting, " ")
    Let final_message be string_concat(message, name)
    print_string(final_message)
    Return 0
End Process
```

## Next Steps

- Read the complete language specification in `runa/docs/user/language-specification/`
- Explore example programs in `runa/bootstrap/v0.0.7.5/tests/`
- Learn about compiler internals in `runa/docs/dev/`

## Version Information

**Compiler Version:** v0.0.7.5
**Release Date:** September 30, 2025
**Status:** Self-hosting, production-ready
**Language Level:** Bootstrap subset

For the complete feature set planned for future versions, see the roadmap in the main README.