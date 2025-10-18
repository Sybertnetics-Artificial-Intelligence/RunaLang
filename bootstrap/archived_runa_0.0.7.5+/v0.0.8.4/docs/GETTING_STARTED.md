# Getting Started with Runa

**Version:** v0.0.8.2

This guide explains how to compile and run Runa programs using the Runa compiler.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Compiling Your First Program](#compiling-your-first-program)
3. [The Compilation Process](#the-compilation-process)
4. [Command Line Usage](#command-line-usage)
5. [Multi-File Projects](#multi-file-projects)
6. [Troubleshooting](#troubleshooting)
7. [Advanced Usage](#advanced-usage)

---

## Prerequisites

### Required Tools

- **Linux x86-64** (or WSL on Windows)
- **Runa Compiler** - `build/runac` (included in this distribution)
- **GNU Assembler** - `as` (usually pre-installed)
- **GCC** - For linking (usually pre-installed)

### Verify Installation

```bash
# Check if compiler exists
ls build/runac

# Check assembler
which as

# Check GCC
which gcc
```

---

## Compiling Your First Program

### Step 1: Write a Runa Program

Create `hello.runa`:

```runa
Process called "main" returns Integer:
    Display "Hello, Runa!"
    Return 0
End Process
```

### Step 2: Compile to Assembly

```bash
./build/runac hello.runa /tmp/hello.s
```

This generates x86-64 assembly at `/tmp/hello.s`.

### Step 3: Assemble to Object File

```bash
as /tmp/hello.s -o /tmp/hello.o
```

This creates the machine code object file.

### Step 4: Link with Runtime

```bash
gcc /tmp/hello.o runtime/runtime.c -o hello -lm
```

This creates the final executable `hello`.

### Step 5: Run

```bash
./hello
```

Output:
```
Hello, Runa!
```

---

## The Compilation Process

### What Happens During Compilation?

```
Source Code (hello.runa)
    ↓ [Runa Compiler - Lexer]
Tokens (list of keywords, identifiers, operators)
    ↓ [Runa Compiler - Parser]
Abstract Syntax Tree (AST)
    ↓ [Runa Compiler - Code Generator]
x86-64 Assembly (/tmp/hello.s)
    ↓ [GNU Assembler - as]
Object File (/tmp/hello.o)
    ↓ [GCC Linker]
Executable Binary (hello)
```

### Why Multiple Steps?

1. **Runa Compiler** (`runac`) - Translates Runa → Assembly
2. **Assembler** (`as`) - Translates Assembly → Machine Code
3. **Linker** (`gcc`) - Combines your code with runtime library

*Note: Future versions will combine these steps into a single command.*

---

## Command Line Usage

### Basic Syntax

```bash
./build/runac <input.runa> <output.s>
```

### Arguments

- **First argument** - Input Runa source file (`.runa`)
- **Second argument** - Output assembly file (`.s`)

### Examples

```bash
# Compile program.runa to program.s
./build/runac program.runa program.s

# Use /tmp for temporary files
./build/runac myapp.runa /tmp/myapp.s

# Compile and run in one go
./build/runac test.runa /tmp/test.s && \
  as /tmp/test.s -o /tmp/test.o && \
  gcc /tmp/test.o runtime/runtime.c -o test -lm && \
  ./test
```

### Helper Script (Optional)

Create `runac.sh` for convenience:

```bash
#!/bin/bash
# Usage: ./runac.sh program.runa [output_name]

INPUT=$1
OUTPUT=${2:-program}

# Compile
./build/runac "$INPUT" /tmp/output.s || exit 1

# Assemble
as /tmp/output.s -o /tmp/output.o || exit 1

# Link
gcc /tmp/output.o runtime/runtime.c -o "$OUTPUT" -lm || exit 1

echo "Compiled successfully: $OUTPUT"
```

Usage:
```bash
chmod +x runac.sh
./runac.sh hello.runa hello
./hello
```

---

## Multi-File Projects

### Using Imports

Runa supports multi-file projects using the `Import` statement.

**File: math_utils.runa**
```runa
Process called "square" takes x as Integer returns Integer:
    Return x times x
End Process

Process called "cube" takes x as Integer returns Integer:
    Return x times x times x
End Process
```

**File: main.runa**
```runa
Import "math_utils.runa"

Process called "main" returns Integer:
    Let result be square(5)
    Display "5 squared is: "
    Display integer_to_string(result)
    Return 0
End Process
```

### Compiling Multi-File Projects

**Method 1: Compile each file separately**

```bash
# Compile math_utils.runa
./build/runac math_utils.runa /tmp/math_utils.s
as /tmp/math_utils.s -o /tmp/math_utils.o

# Compile main.runa
./build/runac main.runa /tmp/main.s
as /tmp/main.s -o /tmp/main.o

# Link together
gcc /tmp/main.o /tmp/math_utils.o runtime/runtime.c -o program -lm
./program
```

**Method 2: Import handles it** (current implementation)

```bash
# The Import statement tells the compiler to include the file
./build/runac main.runa /tmp/main.s
as /tmp/main.s -o /tmp/main.o
gcc /tmp/main.o runtime/runtime.c -o program -lm
./program
```

---

## Troubleshooting

### Error: "Command not found: ./build/runac"

**Problem:** Compiler not found or not executable.

**Solution:**
```bash
# Check if file exists
ls -la build/runac

# Make executable (if needed)
chmod +x build/runac

# If missing, rebuild the compiler
make clean && make
```

### Error: "cannot execute binary file"

**Problem:** Running Linux binary on Windows (need WSL).

**Solution:**
```bash
# Use WSL on Windows
wsl ./build/runac program.runa /tmp/program.s
wsl as /tmp/program.s -o /tmp/program.o
wsl gcc /tmp/program.o runtime/runtime.c -o program -lm
wsl ./program
```

### Error: "Undefined reference to 'xxx'"

**Problem:** Missing runtime link or function not defined.

**Solution:**
```bash
# Make sure to link runtime.c
gcc output.o runtime/runtime.c -o program -lm
#                ^^^^^^^^^^^^^^         ^^^
#                Runtime library      Math library

# Check function names match exactly (case-sensitive)
```

### Error: "Segmentation fault"

**Problem:** Memory access error or stack corruption.

**Solutions:**
1. Check array bounds
2. Verify pointer dereferences
3. Check struct field offsets
4. Run with `gdb` for debugging:
   ```bash
   gdb ./program
   (gdb) run
   (gdb) backtrace
   ```

### Compilation Errors

**Syntax errors:**
- Check spelling of keywords (`Process`, `End Process`, etc.)
- Verify indentation (Runa is indentation-sensitive)
- Ensure `End` statements match opening statements

**Type errors:**
- Verify function signatures match declarations
- Check that return types are correct
- Ensure parameters are passed in correct order

---

## Advanced Usage

### Inline Assembly

For performance-critical code, use inline assembly:

```runa
Process called "fast_add" takes a as Integer, b as Integer returns Integer:
    Inline Assembly:
        movq -8(%rbp), %rax    # Load a into RAX
        movq -16(%rbp), %rbx   # Load b into RBX
        addq %rbx, %rax        # RAX = RAX + RBX
    End Assembly
    Return 0  # Return value already in RAX
End Process
```

### Using Collections

**Lists:**
```runa
Process called "main" returns Integer:
    # Create list literal
    Let numbers be a list containing 10, 20, 30, 40, 50

    # Iterate with for-each
    For each num in numbers:
        Display integer_to_string(num)
    End For

    # Use runtime functions
    Let list be list_create()
    list_append(list, 100)
    list_append(list, 200)
    Let value be list_get(list, 0)  # Gets 100

    Return 0
End Process
```

### Debugging Tips

1. **Add Debug Output:**
   ```runa
   Display "Debug: x = "
   Display integer_to_string(x)
   ```

2. **Check Assembly Output:**
   ```bash
   # View generated assembly
   cat /tmp/program.s | less
   ```

3. **Use GDB:**
   ```bash
   # Compile with debug info
   gcc -g output.o runtime/runtime.c -o program -lm

   # Debug
   gdb ./program
   (gdb) break main
   (gdb) run
   (gdb) step
   ```

4. **Memory Debugging:**
   ```bash
   # Check for memory leaks
   valgrind ./program
   ```

---

## Performance Tips

### 1. Minimize Function Calls

```runa
# Slower (function call overhead)
Let result be square(x) plus square(y)

# Faster (inline calculation)
Let result be x times x plus y times y
```

### 2. Use Inline Assembly for Hot Paths

For performance-critical loops, consider inline assembly.

### 3. Reuse Allocations

```runa
# Slower (allocates each time)
For each i in range(1000):
    Let list be list_create()
    # ...
End For

# Faster (allocate once)
Let list be list_create()
For each i in range(1000):
    list_clear(list)
    # ...
End For
```

### 4. Profile Your Code

```bash
# Run benchmarks
cd benchmarks
./run_benchmarks.sh

# Time specific code
time ./program
```

---

## Next Steps

- Read [LANGUAGE_GUIDE.md](LANGUAGE_GUIDE.md) for complete language reference
- Explore examples in `tests/unit/`
- Run benchmarks in `benchmarks/`
- Check the roadmap in `README.md`

---

## Quick Reference

### Complete Workflow

```bash
# 1. Write code
nano program.runa

# 2. Compile
./build/runac program.runa /tmp/program.s

# 3. Assemble
as /tmp/program.s -o /tmp/program.o

# 4. Link
gcc /tmp/program.o runtime/runtime.c -o program -lm

# 5. Run
./program
```

### One-Liner

```bash
./build/runac prog.runa /tmp/p.s && as /tmp/p.s -o /tmp/p.o && gcc /tmp/p.o runtime/runtime.c -o prog -lm && ./prog
```
