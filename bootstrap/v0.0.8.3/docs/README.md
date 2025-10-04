# Runa Programming Language

**Version:** v0.0.8.2
**Status:** Bootstrap Phase - Self-Hosting Achieved ✅
**Target:** Linux x86-64

---

## What is Runa?

Runa is a **human-readable programming language** that compiles to native machine code. Unlike most programming languages that use symbols and abbreviations, Runa uses natural English phrases to make code readable to both programmers and non-programmers.

### Key Features

- ✅ **Natural Language Syntax** - Code reads like English
- ✅ **Self-Hosting** - Compiler written in Runa, compiled by Runa
- ✅ **Native Code Generation** - Direct x86-64 assembly output
- ✅ **Zero Dependencies** - Single binary, no runtime needed
- ✅ **Fast Execution** - Comparable to C performance (~1-2x slower)
- ✅ **Collections Support** - Lists with natural syntax
- ✅ **Inline Assembly** - Direct access to x86-64 instructions
- ✅ **Struct Types** - Custom data structures
- ✅ **For-Each Loops** - Iterate over collections naturally

### Example Code

```runa
Process called "factorial" takes n as Integer returns Integer:
    If n is less than or equal to 1:
        Return 1
    End If
    Return n times factorial(n minus 1)
End Process

Process called "main" returns Integer:
    Let result be factorial(10)
    Display("Factorial of 10 is: ")
    Display(integer_to_string(result))
    Return 0
End Process
```

---

## Why Runa?

### 1. **Readability First**
Traditional code:
```c
int factorial(int n) {
    return (n <= 1) ? 1 : n * factorial(n - 1);
}
```

Runa code:
```runa
Process called "factorial" takes n as Integer returns Integer:
    If n is less than or equal to 1:
        Return 1
    End If
    Return n times factorial(n minus 1)
End Process
```

### 2. **Performance Without Complexity**
- Compiles directly to x86-64 assembly
- No garbage collection overhead
- Manual memory control when needed
- Inline assembly for critical sections

### 3. **Progressive Complexity**
- Start with simple, readable code
- Add performance optimizations as needed
- Use inline assembly for hot paths
- Full control over memory layout

---

## How Runa Works

### Compilation Pipeline

```
Source Code (.runa)
    ↓
Lexer (tokenization)
    ↓
Parser (AST construction)
    ↓
Code Generator (x86-64 assembly)
    ↓
Assembler (machine code)
    ↓
Linker (executable binary)
```

### Architecture

**Compiler Components:**
- **Lexer** (`lexer.runa`) - Tokenizes source code, handles multi-word keywords
- **Parser** (`parser.runa`) - Builds Abstract Syntax Tree (AST)
- **Code Generator** (`codegen.runa`) - Generates x86-64 assembly
- **Runtime** (`runtime.c`) - Minimal C runtime for syscalls (being replaced)

**Collection Runtime:**
- **Lists** (`runtime_list.runa`) - Dynamic arrays with resize support
- **Dictionaries** - *Coming in v0.0.8.2* (planned)
- **Sets** - *Coming in v0.0.8.2* (planned)

---

## Current Capabilities (v0.0.8.2)

### Language Features

✅ **Data Types:**
- Integer (64-bit signed)
- String (pointers to null-terminated strings)
- Pointer (raw memory addresses)
- Struct (custom types with fields)
- Boolean (True/False literals)

✅ **Control Flow:**
- If/Otherwise If/Otherwise
- For loops (counting and for-each)
- While loops
- Break/Continue
- Match statements (pattern matching)

✅ **Functions:**
- Process definitions with parameters
- Return values
- Recursion
- Inline assembly blocks

✅ **Collections:**
- List literals: `Let nums be a list containing 1, 2, 3`
- For-each: `For each item in items: ... End For`
- Runtime functions: create, append, get, set, insert, remove

✅ **Operators:**
- Arithmetic: `plus`, `minus`, `times`, `divided by`, `modulo`
- Comparison: `is equal to`, `is not equal to`, `is less than`, etc.
- Logical: `and`, `or`, `not`
- Bitwise: `bitwise and`, `bitwise or`, `bitwise xor`, `shift left`, `shift right`

✅ **Advanced Features:**
- Struct field access with natural syntax
- Import system for multi-file projects
- Inline assembly for low-level operations
- Context-sensitive keywords (can use `list`, `set` as variable names)

---

## Project Structure

```
v0.0.8.2/
├── README.md                    # This file
├── GETTING_STARTED.md          # Compilation and usage guide
├── LANGUAGE_GUIDE.md           # Language reference
│
├── src/                        # Compiler source code (written in Runa)
│   ├── main.runa               # Entry point
│   ├── lexer.runa              # Tokenization
│   ├── parser.runa             # AST construction
│   ├── codegen.runa            # x86-64 code generation
│   ├── containers.runa         # Dynamic arrays/lists
│   ├── hashtable.runa          # Hash tables
│   ├── string_utils.runa       # String operations
│   └── runtime_list.runa       # List runtime library
│
├── runtime/
│   └── runtime.c               # C runtime (syscalls, memory)
│
├── build/
│   └── runac                   # Compiled Runa compiler (executable)
│
├── tests/unit/                 # Unit tests
└── benchmarks/                 # Performance benchmarks
    ├── runa/                   # Runa implementations
    ├── c/                      # C comparison
    ├── python/                 # Python comparison
    ├── java/                   # Java comparison
    └── run_benchmarks.sh       # Benchmark runner
```

---

## Performance

### Benchmark Results (vs C, Python, Java)

| Benchmark | Runa vs C | Runa vs Python | Runa vs Java |
|-----------|-----------|----------------|--------------|
| Factorial | **0.97x** (faster!) | 0.24x faster | 2.35x slower |
| Primes | **1.00x** (equal!) | 0.46x faster | 2.21x slower |
| Fibonacci | 1.56x slower | **4.48x faster** | 2.66x slower |
| Quicksort | 2.53x slower | **11.70x faster** | 3.39x slower |
| **Average** | **~1.3x slower** | **~5x faster** | **~2.5x slower** |

**Key Takeaways:**
- ✅ Nearly matches C performance (no optimizer!)
- ✅ Consistently faster than Python (2-12x)
- ✅ Competitive with Java (within 2-4x)

---

## Roadmap

### Completed (v0.0.8.2)
- ✅ Self-hosting compiler
- ✅ Struct construction and field access
- ✅ List literals and for-each loops
- ✅ Pattern matching
- ✅ Inline assembly
- ✅ Multi-file imports

### In Progress (v0.0.8.2)
- 🔄 Dictionary literals and runtime
- 🔄 Set literals and runtime

### Coming Soon
- **v0.0.8.3** - Match/Pattern matching enhancements, ADTs
- **v0.0.8.4** - Lambda expressions, type inference
- **v0.0.9** - Error handling (Result/Option), generics, native object writer
- **v0.1.0** - Beta release, standard library foundation
- **v1.0.0** - Production release

---

## Philosophy

**Runa's Core Principles:**

1. **Human Readability** - Code should be understandable by non-programmers
2. **Performance** - Native compilation, no runtime overhead
3. **Simplicity** - Minimal concepts, maximum power
4. **Progressive Disclosure** - Start simple, add complexity as needed
5. **Self-Hosting** - Compiler written in the language it compiles

---

## Community & Support

- **GitHub Issues:** Report bugs and request features
- **Documentation:** See `GETTING_STARTED.md` and `LANGUAGE_GUIDE.md`
- **Examples:** Check `tests/unit/` for usage examples
- **Benchmarks:** See `benchmarks/` for performance comparisons

---

## License

*(Add license information here)*

---

## Quick Start

```bash
# Compile a Runa program
./build/runac program.runa /tmp/program.s

# Assemble and link
as /tmp/program.s -o /tmp/program.o
gcc /tmp/program.o runtime/runtime.c -o program -lm

# Run
./program
```

See [GETTING_STARTED.md](GETTING_STARTED.md) for detailed instructions.
