# Runa Bootstrap Compiler v0.2 - Micro Runa

The second stage bootstrap compiler, written in Runa v0.1 syntax and compiled using the v0.1 compiler.

## Objective

Build a minimal but functional Runa compiler that can:
1. Parse basic Runa syntax with function parameters
2. Generate executable code (LLVM IR or direct assembly)
3. Support proper variable storage (using alloca)
4. Compile itself (self-hosting milestone)

## Build Instructions

```bash
# Compile individual components
./runac_v0.1 lexer.runa -o lexer.o
./runac_v0.1 parser.runa -o parser.o
./runac_v0.1 codegen.runa -o codegen.o
./runac_v0.1 main.runa -o main.o

# Link into executable
gcc -no-pie lexer.o parser.o codegen.o main.o -o runac_v0.2 -lm

# Test compilation
./runac_v0.2 test.runa -o test.o
gcc -no-pie test.o -o test_exe -lm
./test_exe
```

## Architecture Approach

Due to v0.1 limitations (no While loops, no function parameters), v0.2 uses:
- **Functional recursion** instead of While loops
- **Global state** for passing complex data between functions
- **Simple token buffer** with index-based traversal
- **Direct assembly generation** to avoid LLVM complexity

## Components

### 1. Lexer (`lexer.runa`)
- Tokenizes source into: Keywords, Identifiers, Numbers, Strings, Operators
- Uses recursion for character processing
- Stores tokens in global buffer

### 2. Parser (`parser.runa`)
- Builds simple AST from token stream
- Supports: Process definitions with parameters, Let/Set statements, If/Otherwise, Function calls
- Uses recursive descent parsing

### 3. Code Generator (`codegen.runa`)
- Generates x86-64 assembly directly
- Implements proper variable storage with stack allocation
- Supports function parameters via registers/stack

### 4. Main Driver (`main.runa`)
- Coordinates compilation pipeline
- Handles file I/O and command-line arguments

## Key Improvements Over v0.1

| Feature | v0.1 | v0.2 |
|---------|------|------|
| Function Parameters | ❌ None | ✅ Supported |
| Variable Storage | ❌ Values only | ✅ Stack allocation |
| While Loops | ❌ Broken | ✅ Fixed |
| Error Messages | ❌ Minimal | ✅ Line/column info |
| Self-Hosting | ❌ Cannot compile Runa | ✅ Can compile itself |

## Supported Syntax

```runa
Process called "factorial" that takes n as Integer returns Integer:
    If n is less than or equal to 1:
        Return 1
    Otherwise:
        Let result be factorial(n - 1)
        Return n * result
    End If
End Process

Process called "main" returns Integer:
    Let value be factorial(5)
    Print value
    Return 0
End Process
```

## Development Status

- [ ] Lexer implementation
- [ ] Parser implementation
- [ ] Code generator implementation
- [ ] Self-compilation test
- [ ] Basic standard library functions