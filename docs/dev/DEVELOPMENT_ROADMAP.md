# Runa Development Roadmap
## From v0.0.8 to v1.0

**Current Status:** v0.0.8 (Self-Hosting Achieved ✅, First Self-Hosted Compiler)
**Previous:** v0.0.7.5 (Minimal Bootstrap in C - no longer used)
**Target:** v1.0 (Production-Ready Language)

---

## 📋 Milestone Overview

| Version | Focus Area | Status |
|---------|-----------|--------|
| **v0.0.7.5** | Self-hosting compiler (C bootstrap) | ✅ **COMPLETE** |
| **v0.0.8** | Core Language Complete (inline asm, imports, for loops, bitwise) | 🔄 **IN PROGRESS** |
| **v0.0.8.1** | Collections (Lists, Dictionaries, Sets) | 📋 Planned |
| **v0.0.8.2** | Match/Pattern Matching, Lambda Expressions | 📋 Planned |
| **v0.0.8.3** | String Interpolation, Ternary Operator | 📋 Planned |
| **v0.0.9** | Native Object Writer, Linker & Pure Runa Runtime | 📋 Planned |
| **v0.1.0** | Beta Release - Toolchain Independence | 🎯 Milestone |
| **v0.2.0** | Standard Library Expansion + Triple Syntax (--canon/--developer/--viewer) | 📋 Planned |
| **v0.3.0** | Error Handling & Debugging Tools (Try/Catch, Result types) | 📋 Planned |
| **v0.4.0** | Memory Management & Safety Features (Ownership, Lifetimes) | 📋 Planned |
| **v0.5.0** | Optimization Passes (Basic - Constant Folding, DCE, Inlining) | 📋 Planned |
| **v0.6.0** | Advanced Type System (Generics, Traits, Union/Optional types) | 📋 Planned |
| **v0.6.1** | Type Inference, Refinement Types | 📋 Planned |
| **v0.7.0** | Concurrency Primitives (Threads, Mutexes, Channels) | 📋 Planned |
| **v0.7.1** | Async/Await, Actors | 📋 Planned |
| **v0.8.0** | Advanced Optimization & Profiling (PGO, LTO, SIMD) | 📋 Planned |
| **v0.8.1** | AOTT Tier 0-1: Lightning Interpreter + Smart Bytecode | 📋 Planned |
| **v0.8.2** | AOTT Tier 2-3: Basic + Optimized Native Compilation | 📋 Planned |
| **v0.8.3** | AOTT Tier 4: Speculative Execution | 📋 Planned |
| **v0.9.0** | Package Management & Distribution | 📋 Planned |
| **v0.9.1** | IDE Tooling (LSP, Debugger, Profiler) | 📋 Planned |
| **v0.9.2** | AI Annotation System Implementation | 📋 Planned |
| **v1.0.0** | Production Release | 🎯 Goal |

---

# 🔹 v0.0.8: Core Language Complete

**Goal:** First fully self-hosted compiler with essential language features for real-world programming.

**Status:** Self-hosting achieved ✅. Now completing core language features.

**See also:** [V0_0_8_CRITICAL_FIXES.md](../bootstrap/v0.0.8/docs/V0_0_8_CRITICAL_FIXES.md)

## What Belongs in v0.0.8

### COMPILER Features (Lexer/Parser/Codegen):
- ✅ Basic types (Integer, String, Character)
- ✅ Variables (Let, Set)
- ✅ Arithmetic operators (+, -, *, /, %)
- ✅ Comparison operators (==, !=, <, >, <=, >=, "is not" variants)
- ✅ Logical operators (and, or, not)
- ✅ Bitwise operators (bit_and, bit_or, bit_xor, bit_shift_left, bit_shift_right)
- ✅ Control flow (If/Otherwise/End If, While/End While)
- ✅ Functions (Process called ... returns ...)
- ✅ Structs (Type with fields)
- ✅ Field access (dot notation)
- ✅ Array indexing (bracket notation)
- ✅ Comments (Note: single/multi-line)
- ✅ Break/Continue statements
- ✅ Negative numbers (negative keyword)
- ✅ Boolean literals (true/false)
- ✅ Parentheses for expression grouping
- ✅ Compound assignment (Set x gets increased by, Increase x by)
- ✅ **For loops** (`For var from start to end:` and `For var from start to end by step:`)
- ✅ **Import system** (Both `Import "file" as name` and `Import { items } from "file"` with optional aliasing)
- ✅ **Inline Assembly** (`Inline Assembly: ... End Assembly` with raw x86-64 instructions)

### RUNTIME Features (runtime/*.c → will become runtime/*.runa in v0.0.9):
- ✅ Memory allocation (malloc, free) - **Currently C, will be Runa in v0.0.9**
- ✅ String operations (length, concat, compare, char_at) - **Currently C, will be Runa in v0.0.9**
- ✅ File I/O (read_file, write_file) - **Currently C, will be Runa in v0.0.9**
- ✅ Basic I/O (Print/Display) - **Currently C, will be Runa in v0.0.9**
- ✅ Math functions (sin, cos, sqrt, pow, etc.) - **Currently C, will be Runa in v0.0.9**
- ❌ **List operations** (append, insert, remove, etc.) - **Will be Runa in v0.0.8.1**
- ❌ **Dictionary operations** (get, set, keys, values) - **Will be Runa in v0.0.8.1**
- ❌ **Advanced string ops** (split, join, trim, replace) - **Will be Runa in v0.0.8.1**

### EXTERNAL SYSTEMS (Not in compiler or runtime):
- Standard library modules (collections, datetime, network, JSON) - **v0.9.0**
- Package manager - **v0.9.0**
- Debugger/profiler - **v0.9.0**
- IDE tooling (LSP, syntax highlighting) - **v0.9.0**
- AOTT execution tiers - **v0.6.0-0.8.0**

## Critical Fixes (From V0_0_8_CRITICAL_FIXES.md):

### 1. ✅ **Fix Imports** - COMPLETE
Multi-file compilation with process_imports

### 2. ✅ **Negative Numbers** - COMPLETE
`negative` keyword and unary negation

### 3. ✅ **"is not" Comparisons** - COMPLETE
All variants (is not equal to, is not less than, etc.)

### 4. ✅ **Parentheses for Expression Grouping** - COMPLETE
`(2 plus 3) multiplied by 4`

### 5. ✅ **Note: Comments** - COMPLETE
Single-line, inline, and multi-line block comments

### 6. ✅ **Compound Assignment** - COMPLETE
`Set x gets increased by 5`, `Increase x by 5`

### 7. ✅ **Bitwise Operations** - COMPLETE
bit_and, bit_or, bit_xor, bit_shift_left, bit_shift_right

## New Features:

### 5. **Inline Assembly**
```runa
proc syscall_exit(code: int) -> int:
    Inline Assembly:
        mov $60, %rax
        movq -8(%rbp), %rdi
        syscall
    End Assembly
    ret 0
End proc
```

### 6. **Arrays**
```runa
Type called "IntArray":
    data as Pointer
    length as Integer
    capacity as Integer
End Type

Let numbers be IntArray with length 10
Set numbers at 0 to 42
Let x be numbers at 0
```

### 7. **Structs with Fields**
```runa
Type called "Point":
    x as Integer
    y as Integer
End Type

Let p be Point with x 10 and y 20
Display p.x
Display p.y
```

### 8. **For Loops**
```runa
For i from 0 to 10:
    Display i
End For
```

## Comprehensive Testing:

### Test all operators:
- Modulo (implemented, untested)
- Bitwise (AND, OR, XOR, shifts - implemented, untested)
- Logical (And, Or - minimal testing)

### Test edge cases:
- Division by zero
- Integer overflow
- Deep recursion
- Large numbers

## Success Criteria:
- ✅ Imports load and compile files
- ✅ Negative numbers work
- ✅ All "is not" comparisons work
- ✅ Inline assembly works
- ✅ Arrays with indexing
- ✅ Structs with field access
- ✅ For loops work
- ✅ All operators tested
- ✅ 50+ comprehensive tests passing
- ✅ Self-hosting still works

## Timeline: TBD

---

# 🔹 v0.0.8.1: Collections

**Goal:** Implement essential collection types - Lists, Dictionaries, Sets

## What Belongs Where:

### COMPILER (Parser/Codegen):
- ❌ List literals: `[1, 2, 3]` or `a list containing 1, 2, 3`
- ❌ Dictionary literals: `{"key": value}`
- ❌ Set literals: `set containing 1, 2, 3`
- ❌ List comprehensions: `[x multiplied by 2 for each x in numbers]`
- ❌ Slicing syntax: `list from index 1 to 5`

### RUNTIME (Implemented in Runa, compiled with runtime):
- ❌ List operations: `list_create`, `list_append`, `list_insert`, `list_remove`, `list_get`, `list_set`, `list_length`
- ❌ Dictionary operations: `dict_create`, `dict_set`, `dict_get`, `dict_has`, `dict_keys`, `dict_values`
- ❌ Set operations: `set_create`, `set_add`, `set_contains`, `set_remove`, `set_union`, `set_intersection`

## Success Criteria:
- ✅ List literals work
- ✅ Dictionary literals work
- ✅ Set literals work
- ✅ All collection operations implemented
- ✅ Collection types work with For Each loops
- ✅ Memory management (no leaks)
- ✅ Tests for all collection types

## Timeline: TBD

---

# 🔹 v0.0.8.2: Match/Pattern Matching & Lambda Expressions

**Goal:** Implement pattern matching and first-class functions

## What Belongs Where:

### COMPILER (Parser/Codegen):
- ❌ Match statement: `Match value: When pattern: ... End Match`
- ❌ Pattern matching with types: `When value of type Integer`
- ❌ Pattern matching with destructuring: `When [first, rest...]`
- ❌ Lambda expressions: `lambda x: x multiplied by 2`
- ❌ Function types: `Function[Integer, String, Boolean]`

### RUNTIME:
- ❌ Function closures (capture environment)
- ❌ Higher-order function utilities: `map`, `filter`, `reduce`

## Success Criteria:
- ✅ Match statements with multiple patterns
- ✅ Exhaustiveness checking (compiler warns on missing cases)
- ✅ Lambda expressions as values
- ✅ Closures capture variables correctly
- ✅ Higher-order functions work

## Timeline: TBD

---

# 🔹 v0.0.8.3: String Interpolation & Ternary Operator

**Goal:** Developer ergonomics improvements

## What Belongs Where:

### COMPILER (Parser/Codegen):
- ❌ String interpolation: `f"Value is {x}"`
- ❌ Ternary operator: `value If condition Otherwise other_value`
- ❌ Range expressions: `1 to 10`, `1 through 10`

### RUNTIME:
- ❌ Format string support functions

## Success Criteria:
- ✅ String interpolation with expressions
- ✅ Ternary operator precedence correct
- ✅ Range expressions work in For loops
- ✅ All features tested

## Timeline: TBD

---

# 🔹 v0.0.9: Native Object Writer, Linker & Pure Runa Runtime

**Goal:** Complete toolchain independence - no `as`, no `ld`, no `gcc`. Zero C dependencies.

## Features to Implement:

### 1. **ELF Object File Writer**
- Generate `.o` files directly (no `.s` intermediate)
- ELF64 format specification
- Symbol table generation
- Relocation entries
- Section headers (.text, .data, .rodata, .bss)

### 2. **Custom Linker**
- Link multiple `.o` files into executable
- Resolve symbols across modules
- Handle relocations
- Generate executable ELF binary
- Support for:
  - Static linking
  - Entry point specification
  - Section merging

### 3. **Pure Runa Runtime (Zero C)**
**Replaces `runtime/runtime.c` with `runtime/runtime.runa`**

Write runtime entirely in Runa using inline assembly for syscalls:

```runa
# runtime/runtime_io.runa
proc write_syscall(fd: int, buf: ptr, len: int) -> int:
    Inline Assembly:
        mov $1, %rax           # syscall: write
        movq -8(%rbp), %rdi    # fd
        movq -16(%rbp), %rsi   # buf
        movq -24(%rbp), %rdx   # len
        syscall
    End Assembly
    ret 0
End proc

proc exit_syscall(code: int) -> int:
    Inline Assembly:
        mov $60, %rax          # syscall: exit
        movq -8(%rbp), %rdi    # exit code
        syscall
    End Assembly
    ret 0
End proc
```

**Runtime modules to implement:**
- `runtime/runtime_io.runa` - read, write, open, close
- `runtime/runtime_memory.runa` - malloc, free, memcpy, memset
- `runtime/runtime_string.runa` - string operations
- `runtime/runtime_file.runa` - file operations
- `runtime/runtime_math.runa` - basic math (if needed)

**Compilation:**
```bash
# Compile runtime modules to .o files
runac runtime/runtime_io.runa -o runtime/runtime_io.o --emit=obj
runac runtime/runtime_memory.runa -o runtime/runtime_memory.o --emit=obj
runac runtime/runtime_string.runa -o runtime/runtime_string.o --emit=obj

# Link with user program
runac main.runa --link runtime/*.o -o program
```

### 4. **New Compilation Flags**
```bash
# Direct object file generation:
runac program.runa -o program.o --emit=obj

# Link multiple objects:
runac --link main.o utils.o runtime/*.o -o program

# Or do both in one step (auto-links runtime):
runac main.runa utils.runa -o program
```

### 5. **File Format Support**
- **Phase 1:** ELF64 (Linux x86-64)
- **Phase 2:** PE (Windows) - future
- **Phase 3:** Mach-O (macOS) - future

### 6. **Build Process Changes**
**Old (v0.0.7.5):**
```bash
gcc -c runtime/runtime.c -o runtime/runtime.o    # Needs GCC
as --64 program.s -o program.o                   # Needs as
ld program.o runtime/runtime.o -o program        # Needs ld
```

**New (v0.0.9):**
```bash
runac runtime/runtime.runa -o runtime.o --emit=obj    # Pure Runa
runac program.runa --link runtime.o -o program        # Pure Runa
# Zero external dependencies!
```

## Success Criteria:
- ✅ Generate valid ELF object files
- ✅ Link multiple objects successfully
- ✅ Executables run without external assembler/linker
- ✅ **Pure Runa runtime (zero C code)**
- ✅ **Zero dependency on GCC, as, or ld**
- ✅ Self-hosting with native object generation
- ✅ Bootstrap produces identical binaries

## Timeline: TBD

---

# 🎯 v0.1.0: Beta Release - True Toolchain Independence

**Goal:** First public beta - zero external dependencies. Pure Runa compiler that requires nothing but libc for syscalls.

**What "Toolchain Independence" Means:**
- ✅ No GCC (pure Runa runtime)
- ✅ No as (native object generation)
- ✅ No ld (custom linker)
- ✅ Single binary distribution
- ✅ Works out-of-the-box on any Linux x86-64 system

## Deliverables:

### 1. **Complete Toolchain**
- `runac` - compiler (Runa → native executable, all-in-one)
  - Integrated parser, codegen, object writer, linker
  - No external tools needed
- `runaobj` - object file inspector (debugging tool)
- `runadump` - disassembler / binary inspector

### 2. **Documentation**
- Complete language specification
- Standard library reference
- Compiler internals guide
- Migration guide from C/Rust/Python

### 3. **Packaging**
- Standalone binary distribution (Linux x86-64)
- Installation script
- Shell completion (bash, zsh)

### 4. **Testing Suite**
- 100+ test programs
- Regression test suite
- Performance benchmarks vs C/Rust/Python/Java
- Memory leak detection

### 5. **Announcement**
- Blog post: "Runa v0.1.0: A Self-Hosting, Toolchain-Independent Language"
- HackerNews/Reddit launch
- GitHub release with binaries

## Success Criteria:
- ✅ No external dependencies (except libc for syscalls)
- ✅ Passes all test suites
- ✅ Documentation complete
- ✅ Public release ready

## Timeline: TBD

---

# 🔹 v0.2.0: Standard Library Expansion + Triple Syntax

**Goal:** Expand standard library with essential utilities for real-world programming AND implement Triple Syntax Architecture (--canon, --developer, --viewer modes).

**Note:** Collections already implemented in v0.0.8.1. This version adds MORE stdlib modules.

## What Belongs Where:

### STANDARD LIBRARY MODULES (Separate from compiler/runtime):
These are Runa modules (.runa files) that users import

- ❌ **String Library Module** (`stdlib/strings.runa`)
  - String manipulation: `split`, `join`, `trim`, `replace`, `substring`, `starts_with`, `ends_with`
  - Pattern matching: Basic regex support
  - Unicode: UTF-8 encoding/decoding
  - String formatting utilities

- ❌ **File I/O Module** (`stdlib/files.runa`)
  - Buffered I/O (wrap syscalls)
  - Binary file support
  - Directory operations: `list_dir`, `create_dir`, `delete_dir`
  - Path manipulation: `join_path`, `dirname`, `basename`, `absolute_path`

- ❌ **Math Library Module** (`stdlib/math.runa`)
  - Advanced functions beyond runtime: `factorial`, `gcd`, `lcm`
  - Random number generation: `random_int`, `random_float`, `random_choice`
  - Statistical functions: `mean`, `median`, `stddev`

- ❌ **DateTime Module** (`stdlib/datetime.runa`)
  - Current time/date via syscalls
  - Parsing and formatting (ISO 8601, custom formats)
  - Duration calculations
  - Timers and stopwatches

### RUNTIME (Low-level functions remain in runtime/*.c):
- Already exists: syscalls, memory, basic string ops
- NO CHANGES NEEDED for v0.2.0

### TRIPLE SYNTAX ARCHITECTURE (COMPILER):
**See:** `runa/docs/dev/Sybertnetics_Roadmap/TRIPLE_SYNTAX_IMPLEMENTATION_SUMMARY.md`

- ❌ **Complete CLI→Lexer Mode Passing**
  - `runac --canon file.runa` → lexer receives CANON mode
  - `runac --developer file.runa` → lexer receives DEVELOPER mode
  - `runac --viewer file.runa` → compiler outputs viewer format (display only)

- ❌ **Developer Mode Syntax (`--developer`)**
  - Mathematical operators: `+`, `-`, `*`, `/`, `%`, `**`
  - Comparison operators: `==`, `!=`, `<`, `>`, `<=`, `>=`
  - Assignment: `=` instead of `be`
  - Function syntax: `proc name()` instead of `Process called "name"`
  - Bidirectional conversion with --canon mode

- ❌ **Viewer Mode Output (`--viewer`)**
  - Natural language sentence generation
  - Educational context and explanations
  - READ-ONLY display format (not compilable)
  - Generated from either --canon or --developer source

- ❌ **Mode Configuration System**
  - Project-level `.runaconfig` file
  - User-level preferences
  - Per-file mode hints

- ❌ **`runafmt` Formatter Tool**
  - Convert between modes: `runafmt --mode=developer input.runa`
  - Preserves semantics across conversions
  - Validates syntax in all three modes

## Success Criteria:

**Standard Library:**
- ✅ Standard library covers 80% of common use cases
- ✅ Documentation for all stdlib functions
- ✅ Example programs using stdlib
- ✅ Performance competitive with C stdlib
- ✅ Modules importable via `Import "stdlib/strings"`

**Triple Syntax:**
- ✅ All three modes (--canon, --developer, --viewer) fully functional
- ✅ Bidirectional conversion between canon and developer modes
- ✅ `runafmt` tool can convert any Runa code between modes
- ✅ Documentation showing all three syntax forms side-by-side
- ✅ Example programs demonstrating all modes

## Timeline: TBD

---

# 🔹 v0.3.0: Error Handling & Debugging Tools

**Goal:** Production-grade error reporting and debugging capabilities.

## What Belongs Where:

### COMPILER (Parser/Codegen):
- ❌ **Try/Catch/Finally** - Exception handling syntax
  ```runa
  Try:
      Let result be divide(10, 0)
  Catch error:
      Print "Error: " plus error
  Finally:
      Print "Cleanup"
  End Try
  ```
- ❌ **Throw Statement** - Exception throwing
  ```runa
  If x is less than 0:
      Throw "Value must be positive"
  End If
  ```
- ❌ **Result Types** - Canonical error handling
  ```runa
  Process called "divide" takes a as Integer, b as Integer returns Result of Integer, String:
      If b is equal to 0:
          Return Error("Division by zero")
      Otherwise:
          Return Success(a divided by b)
      End If
  End Process
  ```
- ❌ **Error Propagation** - `?` operator
  ```runa
  Let result be divide(10, 0)?  # Propagates error up
  ```
- ❌ **Assert Statement** - Runtime assertions
  ```runa
  Assert x is greater than 0, "x must be positive"
  ```
- ❌ **Panic System** - Unrecoverable errors
  ```runa
  Panic("Critical failure: memory corruption")
  ```

### RUNTIME (Implemented in Runa):
- ❌ **Stack trace generation** - Capture call stack on error
- ❌ **Exception type system** - Built-in exception types
- ❌ **Debug info structures** - Line numbers, file names in errors

### COMPILER IMPROVEMENTS:
- ❌ **Better error messages**
  - Colored output (red for errors, yellow for warnings)
  - Source code snippets showing error location
  - Helpful suggestions (e.g., "Did you mean 'multiplied by'?")
  - Error codes with documentation links
- ❌ **DWARF debug information** - For GDB compatibility
- ❌ **Source maps** - Map compiled assembly back to source

### EXTERNAL TOOLS (Separate binaries):
- ❌ **`runadbg`** - Interactive debugger
  - Breakpoints
  - Step through code
  - Variable inspection
  - GDB-compatible interface
- ❌ **Stack trace formatter** - Pretty-print crash dumps

## Success Criteria:
- ✅ Try/Catch/Finally works correctly
- ✅ Result types prevent unchecked errors
- ✅ Error propagation (`?`) reduces boilerplate
- ✅ Stack traces show accurate file/line info
- ✅ Compiler errors are helpful and actionable
- ✅ GDB can debug Runa programs
- ✅ Panic shows full stack trace before exit

## Timeline: TBD

---

# 🔹 v0.4.0: Memory Management & Safety Features

**Goal:** Prevent memory bugs through ownership and lifetime tracking.

## What Belongs Where:

### COMPILER (Type System/Semantic Analysis):
- ❌ **Ownership System** - Track ownership of values
  ```runa
  Process called "takes_ownership" takes data as String (owned):
      # data is moved here, caller can't use it anymore
      Print data
  End Process

  Process called "borrows_data" takes data as String (borrowed):
      # data is borrowed, caller still owns it
      Print data
  End Process
  ```
- ❌ **Lifetime Annotations** - Explicit lifetimes
  ```runa
  Process called "get_reference" with lifetime 'a takes data as String (borrowed 'a) returns String (borrowed 'a):
      Return data
  End Process
  ```
- ❌ **Borrow Checker** - Compile-time validation
  - Use-after-free detection
  - Double-free detection
  - Dangling pointer detection
  - Mutable aliasing prevention
- ❌ **Move Semantics** - Explicit ownership transfer
- ❌ **Drop/Destructor System** - Automatic cleanup

### RUNTIME (Implemented in Runa):
- ❌ **Reference Counting (Optional)** - Rc<T> type
  ```runa
  Type called "RcString":
      data as String
      ref_count as Integer
  End Type
  ```
- ❌ **Arena Allocators** - Bulk deallocation
  ```runa
  Let arena be arena_create(1024)  # 1KB arena
  Let data be arena_allocate(arena, 256)
  # ... use data ...
  arena_destroy(arena)  # Frees all at once
  ```
- ❌ **Leak Detection** - Runtime tracking (debug mode)

### COMPILER (Code Generation):
- ❌ **Automatic drop insertion** - Insert cleanup calls
- ❌ **Move optimization** - Elide unnecessary copies

## Success Criteria:
- ✅ Ownership prevents use-after-free at compile time
- ✅ Borrow checker catches dangling references
- ✅ No memory leaks in standard library
- ✅ Performance impact < 5% vs manual management
- ✅ Clear error messages for ownership violations
- ✅ Rc<T> works for shared ownership cases
- ✅ Arena allocators provide zero-cost bulk deallocation

## Timeline: TBD

---

# 🔹 v0.5.0: Optimization Passes (Basic)

**Goal:** Close performance gap with C through basic compiler optimizations.

## What Belongs Where:

### COMPILER (Optimization Passes - NEW):
All optimizations happen between parsing and codegen

- ❌ **Constant Folding** (EXPAND EXISTING)
  - Already have: arithmetic operators
  - Add: logical operators, comparisons, bitwise ops
  ```runa
  # Before:
  Let x be 2 plus 3 multiplied by 4
  # After optimization:
  Let x be 14
  ```

- ❌ **Constant Propagation**
  ```runa
  # Before:
  Let x be 5
  Let y be x plus 3
  # After optimization:
  Let y be 8
  ```

- ❌ **Dead Code Elimination**
  ```runa
  # Before:
  If 1 is equal to 2:
      Print "Never happens"
  End If
  # After optimization:
  # (entire block removed)
  ```

- ❌ **Common Subexpression Elimination**
  ```runa
  # Before:
  Let a be x plus y
  Let b be x plus y  # Computed again
  # After optimization:
  Let a be x plus y
  Let b be a  # Reuse
  ```

- ❌ **Function Inlining** - Inline small functions
  ```runa
  # Before:
  Process called "add" takes a as Integer, b as Integer returns Integer:
      Return a plus b
  End Process
  Let result be add(5, 3)

  # After optimization:
  Let result be 5 plus 3
  ```

- ❌ **Loop Optimizations**
  - Loop unrolling (small, fixed-iteration loops)
  - Loop-invariant code motion (move constant calculations outside loop)
  - Strength reduction (multiply → shift when possible)
  ```runa
  # Before:
  For i from 0 to 4:
      Print i
  End For

  # After unrolling:
  Print 0
  Print 1
  Print 2
  Print 3
  ```

- ❌ **Register Allocation** - Better use of CPU registers
  - Graph coloring algorithm
  - Reduce stack usage
  - Fewer memory loads/stores

- ❌ **Peephole Optimization** - Local instruction improvements
  ```asm
  # Before:
  movq $0, %rax
  addq $5, %rax
  # After:
  movq $5, %rax
  ```

### COMPILER FLAGS:
- ❌ `-O0` - No optimization (fast compile, debug builds)
- ❌ `-O1` - Basic optimizations (default)
- ❌ `-O2` - Aggressive optimizations
- ❌ `-O3` - Maximum optimization (may increase binary size)

## Success Criteria:
- ✅ Fibonacci benchmark within 1.5x of C (-O2)
- ✅ Primes benchmark within 1.5x of C (-O2)
- ✅ Compilation time increase < 20% at -O2
- ✅ All tests still pass with optimizations enabled
- ✅ Debug builds (-O0) compile fast for development

## Timeline: TBD

---

# 🔹 v0.6.0: Advanced Type System (Generics, Traits, Union/Optional types)

**Goal:** Richer type system for safety, expressiveness, and code reuse.

## What Belongs Where:

### COMPILER (Parser/Type System/Semantic Analysis):

#### 1. **Generics/Templates**
```runa
Type called "List" with type parameter T:
    items as Pointer
    count as Integer
    capacity as Integer
End Type

Process called "list_append" with type parameter T takes list as List of T, item as T:
    # Implementation
End Process

# Usage:
Let numbers be List of Integer
list_append(numbers, 42)

Let names be List of String
list_append(names, "Alice")
```

#### 2. **Sum Types (Enums/ADTs)**
```runa
Type called "Result" with type parameter T, E:
    Either:
        Success with value as T
        Or
        Error with error as E
    End Either
End Type

Type called "Option" with type parameter T:
    Either:
        Some with value as T
        Or
        None
    End Either
End Type

Type called "Color":
    Either:
        Red
        Or
        Green
        Or
        Blue
        Or
        RGB with r as Integer, g as Integer, b as Integer
    End Either
End Type
```

#### 3. **Pattern Matching Enhancement** (Extend v0.0.8.2)
```runa
Match result:
    When Success with value:
        Print "Got: " plus integer_to_string(value)
    When Error with error:
        Print "Error: " plus error
End Match

Match color:
    When Red:
        Print "Red"
    When RGB with r, g, b:
        Print "RGB(" plus integer_to_string(r) plus ", " plus integer_to_string(g) plus ", " plus integer_to_string(b) plus ")"
End Match
```

#### 4. **Union Types**
```runa
Type called "IntOrString":
    Union:
        Integer
        Or
        String
    End Union
End Type

Let value be IntOrString
Set value to 42
# Later:
Set value to "hello"
```

#### 5. **Optional Types** (Syntactic sugar for Option<T>)
```runa
Type called "Person":
    name as String
    age as Optional of Integer  # May or may not have age
End Type

Let person be Person with name "Alice" and age Some(30)
Let anonymous be Person with name "Bob" and age None
```

#### 6. **Trait System (Protocols/Interfaces)**
```runa
Trait called "Comparable":
    Process called "compare" takes self as This, other as This returns Integer
End Trait

Type called "Point" conforms to Comparable:
    x as Integer
    y as Integer

    Process called "compare" takes self as Point, other as Point returns Integer:
        If self.x is equal to other.x:
            Return self.y minus other.y
        Otherwise:
            Return self.x minus other.x
        End If
    End Process
End Type

# Generic with trait constraint:
Process called "max" with type parameter T where T conforms to Comparable takes a as T, b as T returns T:
    If a.compare(b) is greater than 0:
        Return a
    Otherwise:
        Return b
    End If
End Process
```

### COMPILER (Codegen):
- ❌ **Monomorphization** - Generate specialized code for each generic instantiation
- ❌ **Tag-based sum types** - Efficient enum representation
- ❌ **Vtable generation** - For trait objects (dynamic dispatch)

### COMPILER (Type Checker):
- ❌ **Generic constraint checking** - Verify trait bounds
- ❌ **Exhaustiveness checking** - Ensure all match cases covered
- ❌ **Type unification** - Resolve generic type parameters

## Success Criteria:
- ✅ Generics work across types and functions
- ✅ Sum types compile efficiently (tagged unions)
- ✅ Pattern matching is exhaustive (compiler checks all cases)
- ✅ Traits enable polymorphism without runtime cost
- ✅ Type system prevents common bugs (null pointers, type confusion)
- ✅ Generic code is as fast as hand-written specialized code
- ✅ Union types safely handle multiple type cases

## Timeline: TBD

---

# 🔹 v0.6.1: Type Inference & Refinement Types

**Goal:** Reduce verbosity while maintaining type safety.

## What Belongs Where:

### COMPILER (Type Inference Engine):
- ❌ **Local type inference** - Infer variable types from assignments
  ```runa
  # Before (explicit):
  Let x as Integer be 5
  Let y as String be "hello"

  # After (inferred):
  Let x be 5           # Inferred: Integer
  Let y be "hello"     # Inferred: String
  ```

- ❌ **Function return type inference**
  ```runa
  # Before:
  Process called "add" takes a as Integer, b as Integer returns Integer:
      Return a plus b
  End Process

  # After:
  Process called "add" takes a as Integer, b as Integer:
      Return a plus b  # Return type inferred as Integer
  End Process
  ```

- ❌ **Generic type inference**
  ```runa
  # No need to specify type parameters explicitly:
  Let numbers be List containing 1, 2, 3  # Inferred: List of Integer
  ```

### COMPILER (Refinement Types):
- ❌ **Refinement type definitions**
  ```runa
  Type called "PositiveInteger" is Integer where value is greater than 0
  Type called "NonEmptyString" is String where string_length(value) is greater than 0
  Type called "EvenInteger" is Integer where value modulo by 2 is equal to 0
  ```

- ❌ **Compile-time verification** - Check refinement constraints when possible
  ```runa
  Let x as PositiveInteger be 5   # OK
  Let y as PositiveInteger be -3  # Compile error: -3 doesn't satisfy constraint
  ```

- ❌ **Runtime verification** - Insert checks when compile-time verification impossible
  ```runa
  Process called "make_positive" takes input as Integer returns PositiveInteger:
      If input is less than or equal to 0:
          Panic("Input must be positive")
      End If
      Return input  # Runtime check inserted automatically
  End Process
  ```

## Success Criteria:
- ✅ Type inference reduces boilerplate by 40%+
- ✅ Inference never surprises (predictable rules)
- ✅ Refinement types catch domain errors at compile time
- ✅ Runtime checks are minimal and optimized
- ✅ Error messages show inferred types clearly

## Timeline: TBD

---

# 🔹 v0.7.0: Concurrency Primitives

**Goal:** Safe multi-threaded programming support.

## What Belongs Where:

### COMPILER (Parser/Type System):
- ❌ **Async/Await syntax**
  ```runa
  Async Process called "fetch_data" returns String:
      Let data be Await http_get("https://api.example.com")
      Return data
  End Process
  ```

### RUNTIME (Implemented in Runa with inline asm for syscalls):
- ❌ **Thread creation** - `thread_spawn`, `thread_join`
  ```runa
  Process called "worker" takes id as Integer returns Integer:
      Print "Worker " plus integer_to_string(id)
      Return 0
  End Process

  Let thread1 be thread_spawn(worker, 1)
  Let thread2 be thread_spawn(worker, 2)
  thread_join(thread1)
  thread_join(thread2)
  ```

- ❌ **Mutex/Lock primitives** - `mutex_create`, `mutex_lock`, `mutex_unlock`
  ```runa
  Type called "Mutex" with type parameter T:
      data as T
      lock as Pointer
  End Type

  Process called "with_lock" takes mutex as Mutex of Integer:
      mutex_lock(mutex)
      # Critical section
      mutex_unlock(mutex)
  End Process
  ```

- ❌ **Channels** - Message passing between threads
  ```runa
  Let channel be channel_create(Integer)
  thread_spawn(sender, channel)
  Let value be channel_receive(channel)
  channel_send(channel, 42)
  ```

- ❌ **Atomic operations** - Lock-free primitives
  ```runa
  Let counter be atomic_create(0)
  atomic_increment(counter)
  Let value be atomic_load(counter)
  atomic_compare_and_swap(counter, 5, 10)
  ```

- ❌ **Thread-local storage**
  ```runa
  Thread Local Let thread_id be 0
  ```

### COMPILER (Semantic Analysis):
- ❌ **Thread safety analysis** - Detect data races
  - Warn on unsynchronized shared mutable state
  - Enforce mutex usage for shared data
  - `Send` and `Sync` traits (like Rust)

- ❌ **Deadlock detection** - Static analysis for common patterns
  - Warn on potential circular waits
  - Suggest lock ordering

## Success Criteria:
- ✅ Multi-threaded programs work correctly
- ✅ No data races in safe code (borrow checker prevents)
- ✅ Performance scales with core count
- ✅ Async/await reduces callback hell
- ✅ Channels provide safe inter-thread communication
- ✅ Compiler catches common concurrency bugs
- ✅ Documentation includes concurrency guide

## Timeline: TBD

---

# 🔹 v0.7.1: Async/Await & Actor Model

**Goal:** Advanced concurrency patterns for scalable systems.

## What Belongs Where:

### COMPILER (Parser):
- ❌ **Actor syntax**
  ```runa
  Actor called "Counter":
      State:
          count as Integer
      End State

      Message Handler called "increment":
          Set count to count plus 1
      End Handler

      Message Handler called "get" returns Integer:
          Return count
      End Handler
  End Actor

  # Usage:
  Let counter be spawn_actor(Counter with count 0)
  send(counter, increment)
  Let value be Await send(counter, get)
  ```

### RUNTIME (Async Runtime):
- ❌ **Event loop** - Single-threaded async executor
- ❌ **Future/Promise system** - Async primitives
- ❌ **Async I/O** - Non-blocking file/network operations
  ```runa
  Async Process called "read_file_async" takes path as String returns String:
      Let handle be Await open_async(path)
      Let contents be Await read_async(handle)
      Await close_async(handle)
      Return contents
  End Process
  ```

- ❌ **Actor runtime** - Lightweight actor scheduling
  - Mailbox for messages
  - Automatic supervision (restart on failure)
  - Location transparency (actors on different machines)

### STANDARD LIBRARY:
- ❌ **async-stdlib** - Async versions of I/O operations
  - `async_read_file`, `async_write_file`
  - `async_http_get`, `async_http_post`
  - `async_tcp_connect`, `async_tcp_listen`

## Success Criteria:
- ✅ Async/await prevents callback hell
- ✅ Event loop handles thousands of concurrent tasks
- ✅ Actor model provides supervision and fault tolerance
- ✅ Async I/O scales better than thread-per-connection
- ✅ Documentation includes async programming guide
- ✅ Benchmarks show performance comparable to Tokio/async-std

## Timeline: TBD

---

# 🔹 v0.8.0: Advanced Optimization & Profiling

**Goal:** Match or exceed C performance through advanced optimizations.

## What Belongs Where:

### COMPILER (Advanced Optimization Passes):
- ❌ **Profile-Guided Optimization (PGO)**
  ```bash
  # Step 1: Build with instrumentation
  runac --profile-gen program.runa -o program_instrumented

  # Step 2: Run on representative workload
  ./program_instrumented < workload.txt
  # Generates program.profdata

  # Step 3: Build with profile data
  runac --profile-use=program.profdata program.runa -o program_optimized
  ```
  - Inline hot functions
  - Optimize branch prediction
  - Reorder code for better cache locality

- ❌ **Link-Time Optimization (LTO)**
  - Optimize across compilation units
  - Inline across modules
  - Global dead code elimination
  - Whole-program analysis

- ❌ **SIMD Auto-Vectorization**
  ```runa
  # Compiler automatically uses AVX/SSE:
  For i from 0 to 1000:
      Set array at i to array at i multiplied by 2
  End For
  # → Vectorized to process 8 elements at once (AVX2)
  ```

- ❌ **Loop Optimizations (Advanced)**
  - Loop fusion (combine adjacent loops)
  - Loop interchange (reorder nested loops for cache)
  - Loop blocking/tiling (improve cache reuse)
  - Software pipelining

- ❌ **Escape Analysis** - Stack allocate when possible
  ```runa
  Process called "use_list":
      Let list be List of Integer  # Doesn't escape
      # → Allocated on stack instead of heap
  End Process
  ```

- ❌ **Branch Prediction Hints**
  ```runa
  If Likely x is greater than 0:  # Hint: likely true
      # Hot path
  End If
  ```

- ❌ **Instruction Selection** - Use best CPU instructions
  - Multiply by power-of-2 → shift
  - Small constants → lea instruction
  - Conditional moves instead of branches

### EXTERNAL TOOL (runaprof - NEW):
- ❌ **Sampling Profiler**
  ```bash
  runac --profile program.runa -o program
  ./program
  runaprof program.profile
  ```
  - Shows function call counts
  - Time spent per function
  - Hot spots visualization
  - Flame graphs

- ❌ **Memory Profiler**
  - Heap allocation tracking
  - Memory leak detection
  - Peak memory usage
  - Allocation hotspots

- ❌ **Cache Profiler**
  - Cache miss rates
  - Identify cache-unfriendly code
  - Suggest optimizations

## Success Criteria:
- ✅ Performance matches or beats C on benchmarks (-O3)
- ✅ PGO provides 10-30% speedup on real workloads
- ✅ SIMD vectorization works automatically for simple loops
- ✅ Profiler identifies bottlenecks accurately
- ✅ LTO reduces binary size and improves performance
- ✅ Compilation time still reasonable (< 2x slower than C at -O3)

## Timeline: TBD

---

# 🔹 v0.8.1: AOTT Tier 0-1 (Lightning Interpreter + Smart Bytecode)

**Goal:** Implement first two tiers of AOTT execution architecture.

**What is AOTT?** All-Of-The-Time execution architecture with 5 tiers:
- Tier 0: Lightning Interpreter (fast startup, profiling hooks)
- Tier 1: Smart Bytecode Execution (inline caching, basic optimizations)
- Tier 2: Basic Native Execution (LLVM-based, code caching)
- Tier 3: Optimized Native Execution (aggressive optimizations)
- Tier 4: Speculative Execution (validated speculation with deoptimization)

## What Belongs Where:

### COMPILER (NEW - Bytecode Backend):
- ❌ **Bytecode Generator** - Alternative to assembly codegen
  ```runa
  # Source:
  Let x be 5 plus 3

  # Bytecode:
  LOAD_CONST 5
  LOAD_CONST 3
  ADD
  STORE_LOCAL 0
  ```

- ❌ **Bytecode Format Specification**
  ```
  Runa Bytecode Format (.rbc):

  Header (16 bytes):
    Magic Number: 0x52554E41 ("RUNA")
    Version: 2 bytes (major.minor)
    Flags: 2 bytes (optimization level, debug info)
    Constant Pool Size: 4 bytes
    Code Section Size: 4 bytes

  Constant Pool:
    Entry Count: 4 bytes
    Entries: Variable length
      Type Tag: 1 byte (0x01=Integer, 0x02=Float, 0x03=String, 0x04=Function)
      Data: Variable length based on type

  Code Section:
    Instruction Count: 4 bytes
    Instructions: Variable length
      Opcode: 1 byte
      Operands: 0-3 bytes depending on instruction
  ```

- ❌ **Instruction Set Architecture (32 core opcodes)**
  ```
  Core Instructions:
    0x00: NOP           - No operation
    0x01: LOAD_CONST    - Load constant from pool
    0x02: LOAD_LOCAL    - Load local variable
    0x03: STORE_LOCAL   - Store to local variable
    0x04: LOAD_GLOBAL   - Load global variable
    0x05: STORE_GLOBAL  - Store to global variable
    0x06: LOAD_FIELD    - Load struct field
    0x07: STORE_FIELD   - Store struct field
    0x08: LOAD_INDEX    - Array indexing
    0x09: STORE_INDEX   - Array assignment

  Arithmetic:
    0x10: ADD           - Addition
    0x11: SUB           - Subtraction
    0x12: MUL           - Multiplication
    0x13: DIV           - Division
    0x14: MOD           - Modulo

  Comparison:
    0x20: EQ            - Equal
    0x21: NE            - Not equal
    0x22: LT            - Less than
    0x23: LE            - Less or equal
    0x24: GT            - Greater than
    0x25: GE            - Greater or equal

  Control Flow:
    0x30: JUMP          - Unconditional jump
    0x31: JUMP_IF_TRUE  - Conditional jump
    0x32: JUMP_IF_FALSE - Conditional jump
    0x33: CALL          - Function call
    0x34: RETURN        - Return from function

  Memory:
    0x40: ALLOC         - Allocate memory
    0x41: FREE          - Free memory
  ```

### NEW BINARY: `runai` (Runa Interpreter)
**Tier 0: Lightning Interpreter**
- ❌ **Fast startup** - No compilation delay
- ❌ **Direct bytecode interpretation** - Simple switch-based VM
  ```c
  while (true) {
      opcode = bytecode[pc++];
      switch (opcode) {
          case OP_ADD:
              b = stack[--sp];
              a = stack[--sp];
              stack[sp++] = a + b;
              break;
          // ... other opcodes
      }
  }
  ```
- ❌ **Profiling hooks** - Track hot functions
  ```c
  function_call_counts[function_id]++;
  if (function_call_counts[function_id] > TIER1_THRESHOLD) {
      tier1_compile(function_id);  // Upgrade to Tier 1
  }
  ```
- ❌ **Debugging support** - Breakpoints, variable inspection

**Tier 1: Smart Bytecode Execution**
- ❌ **Inline Caching** - Cache method lookup results
  ```c
  // First call:
  field_offset = lookup_field(obj_type, "name");  // Slow
  cache[pc] = field_offset;                        // Cache it

  // Subsequent calls:
  field_offset = cache[pc];  // Fast
  ```
- ❌ **Quickening** - Replace generic opcodes with specialized ones
  ```
  # First execution:
  LOAD_GLOBAL "x"  → Looks up "x" in global table

  # After first execution (quickened):
  LOAD_GLOBAL_CACHED 0x12345678  → Direct memory load
  ```
- ❌ **Type Feedback** - Track observed types for later optimization
  ```c
  // Track types seen at each operation:
  if (type_at[pc] == UNKNOWN) {
      type_at[pc] = typeof(operand);
  } else if (type_at[pc] != typeof(operand)) {
      type_at[pc] = POLYMORPHIC;  // Multiple types seen
  }
  ```
- ❌ **Hot function detection** - Identify functions to JIT compile
  ```c
  if (function_call_counts[function_id] > TIER2_THRESHOLD) {
      tier2_compile(function_id);  // Upgrade to native code
  }
  ```

### COMPILER FLAGS:
- ❌ `--emit=bytecode` - Generate .rbc instead of assembly
- ❌ `--interpret` - Run in interpreter mode (Tier 0/1)

## Success Criteria:
- ✅ Interpreter has < 10ms startup time
- ✅ Tier 0 performance: 10-50x slower than native
- ✅ Tier 1 performance: 5-20x slower than native (better than Tier 0)
- ✅ Hot functions automatically upgrade from Tier 0 → Tier 1
- ✅ Inline caching improves performance on polymorphic code
- ✅ Bytecode format is stable and documented
- ✅ Interpreter supports all language features

## Timeline: TBD

---

# 🔹 v0.8.2: AOTT Tier 2-3 (Basic + Optimized Native Compilation)

**Goal:** JIT compilation from bytecode to native code with optimizations.

## What Belongs Where:

### NEW BINARY: `runajit` (Runa JIT Compiler)
**Tier 2: Basic Native Execution**
- ❌ **JIT Compilation** - Compile hot functions to native code
  - Use LLVM as backend
  - Cache compiled code for reuse
  - Fallback to interpreter for cold code

- ❌ **Code Cache** - Store compiled native code
  ```
  ~/.runa/code_cache/
    └── 1a2b3c4d.so  # Compiled function (shared object)
  ```

- ❌ **Type Specialization** - Generate specialized code based on observed types
  ```
  # Generic bytecode:
  ADD  # Works for any types

  # Specialized native code (when types are known):
  addq %rbx, %rax  # Fast integer addition
  ```

- ❌ **Deoptimization Support** - Fallback to interpreter when assumptions violated
  ```c
  // Assume x is always Integer:
  if (typeof(x) != INTEGER) {
      deoptimize();  // Return to interpreter
  }
  int result = x + y;  // Fast path
  ```

**Tier 3: Optimized Native Execution**
- ❌ **Aggressive Inlining** - Inline across function boundaries
- ❌ **Dead Code Elimination** - Remove unreachable code
- ❌ **Register Allocation** - Optimal use of CPU registers
- ❌ **Loop Optimizations** - Unrolling, invariant code motion
- ❌ **Branch Prediction** - Reorder code based on profiling data

### RUNTIME SYSTEM:
- ❌ **On-Stack Replacement (OSR)** - Switch from interpreted to JIT mid-function
  ```c
  // Function starts in interpreter (Tier 0/1)
  // After many iterations, hot loop detected:
  // → JIT compile the loop
  // → Jump to compiled code without returning
  ```

- ❌ **Tiering Policy** - Decide when to upgrade execution tier
  ```c
  if (function_calls < 100) {
      // Tier 0: Interpreter
  } else if (function_calls < 1000) {
      // Tier 1: Smart bytecode
  } else if (function_calls < 10000) {
      // Tier 2: Basic native
  } else {
      // Tier 3: Optimized native
  }
  ```

- ❌ **Compilation Threads** - JIT compile in background
  - Don't block execution while compiling
  - Run compiler in separate thread
  - Switch to compiled code when ready

### COMPILER:
- ❌ **LLVM Integration** - Use LLVM for code generation
  - Generate LLVM IR from bytecode
  - Apply LLVM optimization passes
  - Emit native code

## Success Criteria:
- ✅ Tier 2 performance: 2-5x slower than native (comparable to LuaJIT)
- ✅ Tier 3 performance: 0.5-2x slower than native (comparable to V8)
- ✅ Hot functions automatically upgrade: Tier 1 → Tier 2 → Tier 3
- ✅ Code cache reduces recompilation overhead
- ✅ Deoptimization works correctly (no crashes)
- ✅ OSR allows long-running functions to be optimized mid-execution
- ✅ Compilation happens in background without blocking

## Timeline: TBD

---

# 🔹 v0.8.3: AOTT Tier 4 (Speculative Execution)

**Goal:** Aggressive speculative optimizations with fallback mechanisms.

## What Belongs Where:

### JIT COMPILER (Speculative Optimizations):
**Tier 4: Speculative Execution**
- ❌ **Speculative Inlining** - Inline polymorphic calls
  ```c
  // Assume obj.method always resolves to specific_method (based on profiling):
  if (obj->vtable != expected_vtable) {
      deoptimize();  // Wrong assumption, fallback
  }
  specific_method(obj);  // Fast path (no virtual dispatch)
  ```

- ❌ **Type Speculation** - Assume types based on profiling
  ```c
  // Assume x is always Integer (95% of calls):
  if (typeof(x) != INTEGER) {
      deoptimize();
  }
  int result = x + 5;  // Fast integer path
  ```

- ❌ **Escape Analysis & Scalar Replacement**
  ```runa
  Process called "use_point":
      Let p be Point with x 10 and y 20
      Print p.x plus p.y
  End Process

  # Optimized (p doesn't escape):
  Process called "use_point":
      Let x be 10
      Let y be 20
      Print x plus y  # No heap allocation!
  End Process
  ```

- ❌ **Loop-Invariant Code Motion (Aggressive)**
  ```runa
  For i from 0 to 1000:
      Let factor be expensive_calculation()
      Set array at i to array at i multiplied by factor
  End For

  # Speculate that expensive_calculation() is pure:
  Let factor be expensive_calculation()  # Moved outside loop
  For i from 0 to 1000:
      Set array at i to array at i multiplied by factor
  End For
  ```

- ❌ **Branch Elimination** - Remove branches based on profiling
  ```c
  // Profile shows x > 0 99% of the time:
  // → Generate code that assumes x > 0, with guard
  if (x <= 0) {
      deoptimize();  // Rare case
  }
  // Fast path continues...
  ```

- ❌ **Deoptimization Infrastructure**
  - Capture interpreter state (locals, stack, PC)
  - Reconstruct state when speculation fails
  - Continue in interpreter or lower tier

### RUNTIME:
- ❌ **Speculation Tracking** - Record speculation successes/failures
  ```c
  if (speculation_failed[function_id]++ > THRESHOLD) {
      // This speculation keeps failing, stop using it
      disable_speculation(function_id);
      recompile_without_speculation(function_id);
  }
  ```

- ❌ **Adaptive Optimization** - Adjust strategy based on behavior
  - If speculation fails often, back off
  - If speculation succeeds, be more aggressive

### PROFILER INTEGRATION:
- ❌ **Profile-Directed Speculation** - Use profiling data
  ```bash
  # Run with profiling:
  runajit --profile program.runa
  # Generates profile.data

  # Use profile for speculation:
  runajit --profile-use=profile.data program.runa
  # → Tier 4 uses profile data for better speculation
  ```

## Success Criteria:
- ✅ Tier 4 performance: 0.8-1.2x of native C (comparable to V8 Turbofan)
- ✅ Speculative optimizations improve performance by 20-50% over Tier 3
- ✅ Deoptimization is rare (< 1% of execution)
- ✅ When deoptimization happens, it's fast (< 1ms)
- ✅ Adaptive optimization prevents repeated speculation failures
- ✅ Benchmarks show competitive performance with V8, PyPy, LuaJIT

## Timeline: TBD

---

# 🔹 v0.9.0: Package Management & Distribution

**Goal:** Complete package ecosystem for code sharing and distribution.

## What Belongs Where:

### NEW TOOL: `rpack` (Runa Package Manager)
- ❌ **Package Manifest** - `runa.toml`
  ```toml
  [package]
  name = "myproject"
  version = "0.1.0"
  authors = ["Your Name <you@example.com>"]
  license = "MIT"
  description = "A cool Runa project"

  [dependencies]
  stdlib = "0.2.0"
  http = "^1.0"
  json = "2.1"

  [dev-dependencies]
  test-framework = "0.3"
  ```

- ❌ **Commands**
  ```bash
  # Create new project:
  rpack new myproject
  rpack init  # In existing directory

  # Dependency management:
  rpack add stdlib@0.2.0
  rpack remove stdlib
  rpack update  # Update all dependencies

  # Build & run:
  rpack build
  rpack run
  rpack test
  rpack bench

  # Publishing:
  rpack login
  rpack publish

  # Search & info:
  rpack search json
  rpack info http
  ```

- ❌ **Dependency Resolution**
  - Semantic versioning (SemVer)
  - Lockfile (`runa.lock`) for reproducible builds
  - Conflict resolution
  - Transitive dependency handling

- ❌ **Package Registry** - Central repository (like crates.io, npm)
  - Web interface: `packages.runa-lang.org`
  - API for package manager
  - User authentication
  - Package upload/download
  - Version management
  - Documentation hosting

### PROJECT STRUCTURE:
```
myproject/
├── runa.toml           # Package manifest
├── runa.lock           # Lockfile (auto-generated)
├── src/
│   ├── main.runa       # Entry point
│   ├── lib.runa        # Library code
│   └── utils.runa      # Internal modules
├── tests/
│   ├── test_main.runa
│   └── test_utils.runa
├── benches/
│   └── bench_performance.runa
├── examples/
│   └── example_usage.runa
├── docs/
│   └── README.md
└── target/             # Build output (auto-generated)
    ├── debug/
    └── release/
```

### COMPILER INTEGRATION:
- ❌ **Module Resolution** - Find packages in `runa_modules/`
  ```runa
  Import "http"  # Looks in runa_modules/http/
  Import "json"  # Looks in runa_modules/json/
  ```

- ❌ **Version Selection** - Use versions from `runa.lock`

## Success Criteria:
- ✅ Package manager resolves dependencies correctly
- ✅ Semantic versioning prevents breaking changes
- ✅ Lockfile ensures reproducible builds
- ✅ Central repository is operational
- ✅ 50+ packages available at launch
- ✅ Web interface for browsing packages
- ✅ Documentation is auto-generated and hosted

## Timeline: TBD

---

# 🔹 v0.9.1: IDE Tooling (LSP, Debugger, Profiler)

**Goal:** Professional developer tools for productivity.

## What Belongs Where:

### NEW TOOL: `runa-language-server` (LSP Implementation)
Language Server Protocol for IDE integration

- ❌ **Features**:
  - Syntax highlighting
  - Autocomplete (context-aware suggestions)
  - Go to definition (Ctrl+Click)
  - Find all references
  - Rename symbol (refactoring)
  - Hover documentation
  - Inline errors/warnings
  - Code actions (quick fixes)
  - Format document

- ❌ **IDE Integration**:
  - VS Code extension
  - IntelliJ plugin
  - Vim/Neovim plugin
  - Emacs mode
  - Sublime Text package

### NEW TOOL: `runadbg` (Interactive Debugger)
- ❌ **Debugger Features**:
  - Breakpoints (line-based, conditional)
  - Step through code (step in, step over, step out)
  - Variable inspection (locals, globals)
  - Call stack visualization
  - Watch expressions
  - REPL (evaluate expressions in debug context)
  - GDB compatibility (can use GDB with Runa programs)

- ❌ **Debug Information**:
  - DWARF debug info generation (in compiler)
  - Source maps (bytecode → source)
  - Symbol tables

### NEW TOOL: `runaprof` (Profiler - Enhanced from v0.8.0)
- ❌ **Profiling Modes**:
  - CPU profiling (sampling, instrumentation)
  - Memory profiling (allocations, leaks)
  - Time profiling (function timings)

- ❌ **Visualization**:
  - Flame graphs
  - Call graphs
  - Timeline view
  - Hot spots report

- ❌ **Integration**:
  - VS Code profiler view
  - HTML reports
  - Terminal UI

### NEW TOOL: `runafmt` (Code Formatter)
- ❌ **Formatting Rules**:
  - Consistent indentation (4 spaces)
  - Line wrapping (80 characters)
  - Consistent keyword spacing
  - Configurable via `.runafmt.toml`

- ❌ **IDE Integration**:
  - Format on save
  - Format selection
  - Format entire project

### NEW TOOL: `runalint` (Linter)
- ❌ **Lint Rules**:
  - Unused variables/imports
  - Dead code
  - Style violations
  - Complexity metrics
  - Potential bugs (null checks, etc.)

- ❌ **Configuration**:
  - `.runalint.toml` for custom rules
  - Disable specific rules per-line or per-file

## Success Criteria:
- ✅ LSP provides smooth IDE experience (autocomplete < 100ms)
- ✅ Debugger works in VS Code, terminal
- ✅ Profiler identifies bottlenecks accurately
- ✅ Formatter produces consistent, readable code
- ✅ Linter catches common mistakes
- ✅ Tools are documented with examples
- ✅ VS Code extension has 1000+ installs

## Timeline: TBD

---

# 🔹 v0.9.2: AI Annotation System Implementation

**Goal:** Implement AI-first annotation system from specification.

## What Belongs Where:

### COMPILER (Parser):
Recognize and parse AI annotations

- ❌ **@Reasoning** blocks
  ```runa
  @Reasoning:
      This algorithm uses binary search for O(log n) performance.
      Alternative approaches considered:
      - Linear search: O(n) - too slow for large datasets
      - Hash table: O(1) average - not applicable for sorted data
  End Reasoning
  ```

- ❌ **@Implementation** blocks
  ```runa
  @Implementation:
      Uses divide-and-conquer approach:
      1. Find middle element
      2. Compare with target
      3. Recursively search left or right half
  End Implementation
  ```

- ❌ **@Uncertainty** annotations
  ```runa
  @Uncertainty:
      ?[binary_search, linear_search] with confidence 0.8
      Prefer binary_search if list_size > 100
  End Uncertainty
  ```

- ❌ **@KnowledgeReference** blocks
  ```runa
  @KnowledgeReference:
      algorithm: "Binary Search"
      source: "CLRS Introduction to Algorithms, Section 2.3"
      url: "https://en.wikipedia.org/wiki/Binary_search_algorithm"
  End KnowledgeReference
  ```

- ❌ **@TestCases** blocks
  ```runa
  @TestCases:
      Input: [1, 2, 3, 4, 5], target = 3
      Expected: 2 (index of 3)

      Input: [1, 2, 3, 4, 5], target = 6
      Expected: -1 (not found)
  End TestCases
  ```

- ❌ **@Task** blocks
  ```runa
  @Task:
      description: "Implement binary search"
      priority: high
      estimated_time: "2 hours"
      dependencies: ["sort_array", "test_framework"]
  End Task
  ```

- ❌ **@Requirements** blocks
  ```runa
  @Requirements:
      performance: "O(log n) time complexity"
      memory: "O(1) space complexity"
      input: "Sorted array of integers"
      output: "Index of target, or -1 if not found"
  End Requirements
  ```

- ❌ **@Verify** blocks
  ```runa
  @Verify:
      assertion: "array is sorted"
      assertion: "target is within array bounds"
      postcondition: "result is valid index or -1"
  End Verify
  ```

- ❌ **@Resource_Constraints** blocks
  ```runa
  @Resource_Constraints:
      max_memory: "1GB"
      max_cpu_time: "100ms"
      max_network_bandwidth: "10MB/s"
  End Resource_Constraints
  ```

- ❌ **@Security_Scope** blocks
  ```runa
  @Security_Scope:
      access_level: "public"
      sensitive_data: false
      audit_required: false
  End Security_Scope
  ```

- ❌ **@Execution_Model** blocks
  ```runa
  @Execution_Model:
      parallel: true
      async: false
      thread_safe: true
  End Execution_Model
  ```

### COMPILER (Semantic Analysis):
- ❌ **Annotation validation** - Check annotation syntax
- ❌ **Annotation extraction** - Store in AST metadata
- ❌ **Annotation queries** - API for tools to access annotations

### NEW TOOLS:
- ❌ **`runa-annotations`** - Extract and query annotations
  ```bash
  runa-annotations list myproject/  # List all annotations
  runa-annotations extract @Reasoning myproject/  # Extract reasoning blocks
  runa-annotations verify myproject/  # Check annotation consistency
  ```

- ❌ **`runa-ai-assist`** - AI-powered code assistance
  ```bash
  runa-ai-assist suggest function_name  # Suggest implementation based on annotations
  runa-ai-assist verify function_name   # Verify implementation matches requirements
  runa-ai-assist test function_name     # Generate tests from @TestCases annotations
  ```

### DOCUMENTATION GENERATOR:
- ❌ **`runa-doc`** - Generate documentation from annotations
  ```bash
  runa-doc generate myproject/  # Generate HTML docs
  # Includes:
  # - Function signatures
  # - @Reasoning explanations
  # - @Implementation details
  # - @TestCases examples
  # - @Requirements specifications
  ```

## Success Criteria:
- ✅ All annotation types parse correctly
- ✅ Annotations stored in AST without affecting compilation
- ✅ Tools can extract and query annotations
- ✅ Documentation generator produces readable output
- ✅ AI assistance tools provide useful suggestions
- ✅ Annotations improve code understandability by 40%+

## Timeline: TBD

---

# 🎯 v1.0.0: Production Release

**Goal:** Stable, documented, production-ready language.

## Final Polish:

### 1. **Stability**
- ❌ Zero known critical bugs
- ❌ 1000+ test programs pass
- ❌ Fuzz testing (10 million+ inputs, no crashes)
- ❌ Memory safety verified (Valgrind clean)
- ❌ Security audit completed
- ❌ Stress testing (long-running programs, high concurrency)

### 2. **Documentation (Complete)**
- ❌ **Language Reference** - Complete specification
  - All syntax forms documented
  - All operators explained
  - Type system guide
  - Memory model
  - Concurrency model

- ❌ **Tutorial Series**
  - Beginner: "Learn Runa in Y Minutes"
  - Intermediate: "Building Real Applications"
  - Advanced: "System Programming in Runa"

- ❌ **Standard Library Documentation**
  - Every function documented
  - Examples for common use cases
  - API reference (searchable)

- ❌ **Cookbook** - Common patterns
  - File I/O patterns
  - Concurrency patterns
  - Error handling patterns
  - Performance optimization patterns

- ❌ **Compiler Architecture Guide**
  - Lexer design
  - Parser implementation
  - Type system
  - Code generation
  - AOTT architecture

- ❌ **Contributing Guide**
  - How to build from source
  - Code style guidelines
  - Testing requirements
  - Pull request process

### 3. **Tooling (Complete)**
- ❌ **VS Code Extension**
  - Syntax highlighting
  - Autocomplete
  - Debugging
  - Profiling integration
  - Error squiggles
  - Refactoring support

- ❌ **Language Server Protocol (LSP)** - For all editors

- ❌ **Package Repository** - `packages.runa-lang.org`
  - 100+ packages available
  - Documentation hosting
  - Search and discovery
  - Version management

- ❌ **CI/CD Templates**
  - GitHub Actions
  - GitLab CI
  - Jenkins
  - Travis CI

### 4. **Performance**
- ❌ **Benchmarks**
  - Competitive with C/Rust on CPU-bound tasks
  - Performance reports published
  - Comparison with other languages (Go, Python, Node.js)

- ❌ **Optimization Levels**
  - `-O0` - No optimization (fast compile, debug builds)
  - `-O1` - Basic optimizations (default)
  - `-O2` - Aggressive optimizations (recommended for production)
  - `-O3` - Maximum optimization (may increase binary size)
  - `-Os` - Optimize for size

- ❌ **Binary Size**
  - Size optimization mode
  - Strip debug info
  - Link-time optimization

### 5. **Ecosystem**
- ❌ **Packages in Repository**
  - 100+ packages at v1.0 launch
  - Core categories covered:
    - Web frameworks (HTTP, REST, GraphQL)
    - Database drivers (PostgreSQL, MySQL, SQLite)
    - Serialization (JSON, XML, YAML, MessagePack)
    - Networking (TCP, UDP, HTTP/2)
    - Cryptography (hashing, encryption)
    - Testing frameworks
    - Logging libraries
    - CLI tools

- ❌ **Community**
  - Discord server (1000+ members)
  - Forum/discussion board
  - Regular releases (6-week cycle)
  - Core team identified
  - Governance model established

- ❌ **Adoption**
  - 10+ companies using in production
  - Case studies published
  - Testimonials collected

### 6. **Dual Syntax System (Complete)**
- ❌ **Canon Mode** - Natural language (default)
  ```runa
  Let x be 5 plus 3 multiplied by 2
  ```

- ❌ **Developer Mode** - Symbols (opt-in)
  ```runa
  Let x be 5 + 3 * 2
  ```

- ❌ **Viewer Mode** - Full natural language (for non-programmers)
  ```
  Let the variable x be calculated as: five plus three, then multiplied by two
  ```

- ❌ **Seamless Conversion**
  ```bash
  runafmt --mode=canon input.runa
  runafmt --mode=dev input.runa
  runafmt --mode=viewer input.runa
  ```

### 7. **AOTT Architecture (Complete)**
- ✅ **Tier 0** - Lightning Interpreter (v0.8.1)
- ✅ **Tier 1** - Smart Bytecode (v0.8.1)
- ✅ **Tier 2** - Basic Native (v0.8.2)
- ✅ **Tier 3** - Optimized Native (v0.8.2)
- ✅ **Tier 4** - Speculative Execution (v0.8.3)
- ❌ **Adaptive Tiering** - Automatic tier selection based on workload
- ❌ **Tier Visualization** - Show which tier each function is running in

### 8. **Release Artifacts**
- ❌ **Binary Distributions**
  - Linux x86-64 (static binary)
  - Linux ARM64
  - macOS x86-64
  - macOS ARM64 (Apple Silicon)
  - Windows x86-64

- ❌ **Source Distribution**
  - Tarball with full source
  - Git tag: v1.0.0

- ❌ **Docker Images**
  ```bash
  docker pull runa-lang/runa:1.0.0
  docker pull runa-lang/runa:latest
  ```

- ❌ **Package Manager Support**
  - apt (Debian/Ubuntu): `apt install runa`
  - homebrew (macOS): `brew install runa`
  - winget (Windows): `winget install runa`
  - Arch User Repository (AUR): `yay -S runa`

### 9. **Launch Plan**
- ❌ **Announcement Blog Post**
  - "Introducing Runa v1.0: AI-First Programming Language"
  - Technical highlights
  - Getting started guide
  - Roadmap for future versions

- ❌ **Social Media Campaign**
  - HackerNews launch
  - Reddit (/r/programming, /r/ProgrammingLanguages)
  - Twitter/X announcement
  - YouTube demo video

- ❌ **Press Kit**
  - Logo assets
  - Screenshots
  - Example code
  - Key features list
  - Contact information

### 10. **Post-Launch Support**
- ❌ **Bug Bounty Program** - Reward security researchers
- ❌ **Long-Term Support (LTS)** - v1.0.x receives patches for 2 years
- ❌ **Deprecation Policy** - 2-version deprecation cycle
- ❌ **Security Updates** - Critical patches within 24 hours

## Success Criteria:
- ✅ Passes all stability requirements (zero critical bugs)
- ✅ Documentation is comprehensive and clear
- ✅ Community is active and growing (1000+ Discord members)
- ✅ 10+ companies using in production
- ✅ Performance competitive with established languages
- ✅ 100+ packages available in repository
- ✅ Positive reception on HackerNews/Reddit (top 3 posts)
- ✅ Weekly active users: 1000+ developers

## Timeline:
**Target Date:** TBD (approximately 118 weeks from v0.0.8 start)

---

# 📊 Complete Timeline Summary (Updated)

| Phase | Duration | Cumulative Time | Focus |
|-------|----------|-----------------|-------|
| **v0.0.8** | 4 weeks | 4 weeks | Core language features, bitwise ops, inline asm |
| **v0.0.8.1** | 3 weeks | 7 weeks | Collections (Lists, Dicts, Sets) |
| **v0.0.8.2** | 3 weeks | 10 weeks | Match/Pattern matching, Lambdas |
| **v0.0.8.3** | 2 weeks | 12 weeks | String interpolation, Ternary |
| **v0.0.9** | 6 weeks | 18 weeks | Native object writer, linker, Pure Runa runtime |
| **v0.1.0** | 2 weeks | 20 weeks | Beta release polish, packaging |
| **v0.2.0** | 6 weeks | 26 weeks | Standard library modules |
| **v0.3.0** | 6 weeks | 32 weeks | Error handling (Try/Catch, Result) |
| **v0.4.0** | 6 weeks | 38 weeks | Memory safety (Ownership, Lifetimes) |
| **v0.5.0** | 6 weeks | 44 weeks | Basic optimizations (Constant folding, DCE, Inlining) |
| **v0.6.0** | 8 weeks | 52 weeks | Advanced type system (Generics, Traits, ADTs) |
| **v0.6.1** | 4 weeks | 56 weeks | Type inference, Refinement types |
| **v0.7.0** | 6 weeks | 62 weeks | Concurrency (Threads, Mutexes, Channels) |
| **v0.7.1** | 4 weeks | 66 weeks | Async/Await, Actors |
| **v0.8.0** | 8 weeks | 74 weeks | Advanced optimization (PGO, LTO, SIMD) |
| **v0.8.1** | 6 weeks | 80 weeks | AOTT Tier 0-1 (Interpreter, Bytecode) |
| **v0.8.2** | 8 weeks | 88 weeks | AOTT Tier 2-3 (JIT, Optimized native) |
| **v0.8.3** | 6 weeks | 94 weeks | AOTT Tier 4 (Speculative execution) |
| **v0.9.0** | 6 weeks | 100 weeks | Package manager, registry |
| **v0.9.1** | 8 weeks | 108 weeks | IDE tooling (LSP, Debugger, Profiler) |
| **v0.9.2** | 4 weeks | 112 weeks | AI Annotation system |
| **v1.0.0** | 12 weeks | **124 weeks** | Production polish, launch |

**Total Development Time:** ~124 weeks (2.4 years)

---

# 🎯 Feature Distribution Summary

## By Component:

### COMPILER (Lexer/Parser/Codegen/Type System):
- v0.0.8: Core language, inline asm, for loops
- v0.0.8.1: Collection literals
- v0.0.8.2: Match/lambdas
- v0.0.8.3: String interpolation, ternary
- v0.3.0: Try/Catch, Result types, error propagation
- v0.4.0: Ownership system, borrow checker
- v0.5.0: Optimization passes
- v0.6.0: Generics, traits, sum types, union types
- v0.6.1: Type inference, refinement types
- v0.7.0: Async/await syntax
- v0.8.0: PGO, LTO, SIMD
- v0.8.1-0.8.3: Bytecode generation
- v0.9.2: AI annotations parsing

### RUNTIME (Implemented in Runa):
- v0.0.8: Existing C runtime continues
- v0.0.8.1: Collection operations
- v0.0.8.2: Closures, higher-order functions
- v0.0.9: **Pure Runa runtime** (replaces C)
- v0.3.0: Exception handling, stack traces
- v0.4.0: Rc<T>, arena allocators
- v0.7.0: Threads, mutexes, channels, atomics
- v0.7.1: Async runtime, actors
- v0.8.1-0.8.3: Interpreter, JIT runtime

### STANDARD LIBRARY (Separate .runa modules):
- v0.2.0: Strings, Files, Math, DateTime modules
- v0.7.1: Async I/O library

### EXTERNAL TOOLS (Separate binaries):
- v0.0.9: Object inspector (`runaobj`), Disassembler (`runadump`)
- v0.1.0: Packager
- v0.3.0: Debugger (`runadbg`)
- v0.8.0: Profiler (`runaprof`)
- v0.8.1: Interpreter (`runai`)
- v0.8.2: JIT compiler (`runajit`)
- v0.9.0: Package manager (`rpack`)
- v0.9.1: Language server (`runa-language-server`), Formatter (`runafmt`), Linter (`runalint`)
- v0.9.2: Annotation tools (`runa-annotations`, `runa-ai-assist`), Doc generator (`runa-doc`)

---

End of Development Roadmap

**Goal:** Production-grade error reporting and debugging tools.

## Features to Implement:

### 1. **Result Types (Canonical Error Handling)**
```runa
Process called "divide" takes a as Integer, b as Integer returns Result of Integer, String:
    If b is equal to 0:
        Return Error("Division by zero")
    Otherwise:
        Return Success(a divided by b)
    End If
End Process
```

### 2. **Error Propagation**
```runa
Process called "calculate" returns Result of Integer, String:
    Let result be divide(10, 0)?  # ? propagates errors
    Return Success(result)
End Process
```

### 3. **Panic System**
```runa
Process called "must_work" takes value as Integer:
    If value is less than 0:
        Panic("Value must be non-negative")
    End If
End Process
```

### 4. **Stack Traces**
- Generate stack traces on panic
- Line numbers and function names
- Source code context

### 5. **Debugger Support**
- DWARF debug information
- GDB compatibility
- Breakpoint support
- Variable inspection

### 6. **Compiler Error Improvements**
- Colored error messages
- Source code snippets
- Helpful suggestions
- Error codes with documentation links

## Success Criteria:
- ✅ Errors are explicit and handled safely
- ✅ Stack traces are accurate and helpful
- ✅ GDB can debug Runa programs
- ✅ Compiler errors guide users to fixes

## Timeline: TBD

---

# 🔹 v0.6.0: Memory Management & Safety

**Goal:** Balance performance with safety - prevent memory bugs.

## Features to Implement:

### 1. **Ownership System (Inspired by Rust)**
```runa
Process called "takes_ownership" takes data as String (owned):
    # data is moved here, caller can't use it anymore
    Print data
End Process

Process called "borrows_data" takes data as String (borrowed):
    # data is borrowed, caller still owns it
    Print data
End Process
```

### 2. **Lifetime Annotations**
```runa
Process called "get_reference" with lifetime 'a takes data as String (borrowed 'a) returns String (borrowed 'a):
    Return data
End Process
```

### 3. **Reference Counting (Optional)**
```runa
Type called "RcString":
    data as String
    ref_count as Integer
End Type
```

### 4. **Arena Allocators**
```runa
Let arena be arena_create(1024)  # 1KB arena
Let data be arena_allocate(arena, 256)
# ... use data ...
arena_destroy(arena)  # Frees all allocations at once
```

### 5. **Compile-Time Memory Safety Checks**
- Use-after-free detection
- Double-free detection
- Memory leak warnings

## Success Criteria:
- ✅ No memory leaks in standard library
- ✅ Ownership prevents common bugs
- ✅ Performance impact < 5% vs manual management
- ✅ Clear error messages for ownership violations

## Timeline: TBD

---

# 🔹 v0.7.0: Optimization Passes (Level 1)

**Goal:** Close performance gap with C - basic optimizations.

## Features to Implement:

### 1. **Constant Folding**
```runa
# Before:
Let x be 2 plus 3 multiplied by 4

# After optimization:
Let x be 14
```

### 2. **Dead Code Elimination**
```runa
# Before:
If 1 is equal to 2:
    Print "Never happens"
End If

# After optimization:
# (entire block removed)
```

### 3. **Common Subexpression Elimination**
```runa
# Before:
Let a be x plus y
Let b be x plus y  # Computed again

# After optimization:
Let a be x plus y
Let b be a  # Reuse previous computation
```

### 4. **Function Inlining**
```runa
# Before:
Process called "add" takes a as Integer, b as Integer returns Integer:
    Return a plus b
End Process

Let result be add(5, 3)

# After optimization:
Let result be 5 plus 3  # Function call eliminated
```

### 5. **Loop Optimizations**
- Loop unrolling (small, fixed-iteration loops)
- Loop-invariant code motion
- Strength reduction (multiply → shift when possible)

### 6. **Register Allocation**
- Use more CPU registers, less stack
- Reduce memory access overhead

## Success Criteria:
- ✅ Fibonacci benchmark within 1.5x of C
- ✅ Primes benchmark within 1.5x of C
- ✅ Compilation time increase < 20%
- ✅ All tests still pass

## Timeline: TBD

---

# 🔹 v0.8.0: Concurrency Primitives

**Goal:** Multi-threaded programming support.

## Features to Implement:

### 1. **Thread Creation**
```runa
Process called "worker" takes id as Integer returns Integer:
    Print "Worker " plus integer_to_string(id)
    Return 0
End Process

Process called "main" returns Integer:
    Let thread1 be thread_spawn(worker, 1)
    Let thread2 be thread_spawn(worker, 2)

    thread_join(thread1)
    thread_join(thread2)

    Return 0
End Process
```

### 2. **Mutexes & Locks**
```runa
Type called "Mutex" with type parameter T:
    data as T
    lock as Pointer
End Type

Process called "with_lock" takes mutex as Mutex of Integer:
    mutex_lock(mutex)
    # Critical section
    mutex_unlock(mutex)
End Process
```

### 3. **Channels (Message Passing)**
```runa
Let channel be channel_create(Integer)
thread_spawn(sender, channel)
Let value be channel_receive(channel)
```

### 4. **Atomic Operations**
```runa
Let counter be atomic_create(0)
atomic_increment(counter)
Let value be atomic_load(counter)
```

### 5. **Thread Safety Analysis**
- Compiler warns on potential data races
- Enforces mutex usage
- Detects deadlocks (static analysis)

## Success Criteria:
- ✅ Multi-threaded programs work correctly
- ✅ No data races in safe code
- ✅ Performance scales with core count
- ✅ Documentation includes concurrency guide

## Timeline: TBD

---

# 🔹 v0.9.0: Advanced Optimization & Profiling

**Goal:** Match or exceed C performance, developer tooling.

## Features to Implement:

### 1. **Profile-Guided Optimization (PGO)**
```bash
# Step 1: Build with instrumentation
runac --profile-gen program.runa -o program_instrumented

# Step 2: Run on representative data
./program_instrumented < workload.txt

# Step 3: Build with profile data
runac --profile-use=profile.data program.runa -o program_optimized
```

### 2. **Link-Time Optimization (LTO)**
- Optimize across compilation units
- Inline across files
- Global dead code elimination

### 3. **SIMD Auto-Vectorization**
```runa
# Compiler automatically uses AVX/SSE for loops:
For i from 0 to 1000:
    Set array[i] to array[i] multiplied by 2
End For
# → Vectorized to process 8 elements at once
```

### 4. **Profiler Tool (`runaprof`)**
```bash
runac --profile program.runa -o program
./program
runaprof program.profile
# Shows:
# - Function call counts
# - Time spent per function
# - Memory allocations
# - Cache misses
```

### 5. **Advanced Codegen**
- Instruction selection optimization
- Peephole optimization
- Branch prediction hints
- Cache-friendly code layout

## Success Criteria:
- ✅ Performance matches or beats C on benchmarks
- ✅ PGO provides 10-30% speedup
- ✅ Profiler identifies bottlenecks accurately
- ✅ Compilation time still reasonable (<2x slower than C)

## Timeline: TBD

---

# 🎯 v1.0.0: Production Release

**Goal:** Stable, documented, production-ready language.

## Final Polish:

### 1. **Stability**
- Zero known critical bugs
- 1000+ test programs pass
- Fuzz testing (10 million+ inputs)
- Memory safety verified

### 2. **Documentation**
- Complete language reference
- Tutorial series (beginner to advanced)
- Standard library documentation
- Cookbook (common patterns)
- Compiler architecture guide
- Contributing guide

### 3. **Tooling**
- VS Code extension (syntax highlighting, autocomplete, debugging)
- Language server protocol (LSP) implementation
- Package repository (rpack.io)
- CI/CD templates

### 4. **Performance**
- Benchmarks show competitiveness with C/Rust
- Optimization levels: `-O0`, `-O1`, `-O2`, `-O3`
- Binary size optimization mode

### 5. **Ecosystem**
- 50+ packages in repository
- Active community (Discord, forum)
- Regular releases (6-week cycle)

### 6. **Dual Syntax System**
- Canonical (readable) mode
- Developer (concise) mode
- Viewer (AI/tooling) mode
- Seamless conversion

### 7. **AOTT Architecture** (Optional)
- 5-tier execution system
- Lightning interpreter (T0)
- Smart bytecode (T1)
- Basic native compilation (T2)
- Optimized native (T3)
- Speculative execution (T4)

## Success Criteria:
- ✅ Passes all stability requirements
- ✅ Documentation is comprehensive
- ✅ Community is active and growing
- ✅ Used in production by early adopters
- ✅ Performance competitive with established languages

## Timeline: TBD

---

# 📊 Complete Timeline Summary

| Phase | Duration | Total Time |
|-------|----------|------------|
| **v0.0.8** Inline Assembly | 2-3 weeks | 3 weeks |
| **v0.0.9** Native Object/Linker | 4-6 weeks | 9 weeks |
| **v0.1.0** Beta Release | 2-3 weeks | 12 weeks |
| **v0.2.0** Standard Library | 6-8 weeks | 20 weeks |
| **v0.3.0** Type System | 8-10 weeks | 30 weeks |
| **v0.4.0** Modules & Packages | 10-12 weeks | 42 weeks |
| **v0.5.0** Error Handling | 6-8 weeks | 50 weeks |
| **v0.6.0** Memory Safety | 10-12 weeks | 62 weeks |
| **v0.7.0** Optimization L1 | 8-10 weeks | 72 weeks |
| **v0.8.0** Concurrency | 10-12 weeks | 84 weeks |
| **v0.9.0** Advanced Optimization | 12-14 weeks | 98 weeks |
| **v1.0.0** Production Polish | 16-20 weeks | **118 weeks** |


---

# 🎯 Priority Adjustments


