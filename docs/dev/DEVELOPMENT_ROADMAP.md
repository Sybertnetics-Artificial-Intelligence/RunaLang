# Runa Development Roadmap
## From v0.0.8 to v1.0

**Current Status:** v0.0.8.2 (Struct Construction & Field Access Syntax)
**Previous:** v0.0.8.1 (Self-Hosting Achieved ✅, First Self-Hosted Compiler)
**Target:** v1.0 (Production-Ready Language)

---

## 🎯 Critical Path to v0.1.0 (Minimum Viable Stdlib)

Before starting standard library development in v0.1.0, these features are **ABSOLUTE REQUIREMENTS**:

1. ✅ **v0.0.8.1: Struct Construction & Field Access** - Can't write natural code without this
2. ✅ **v0.0.8.2: Collections & For Each Loops** - Stdlib needs lists, dicts, sets
3. ✅ **v0.0.8.3: Pattern Matching & ADT Construction** - Type system incomplete without it
4. ✅ **v0.0.8.4: Lambda & Type Inference** - Functional patterns + DX improvement
5. ⚠️ **v0.0.9: Error Handling (Result/Option types)** - Stdlib needs error handling
6. ⚠️ **v0.0.9: Generics** - Stdlib will be severely limited without generic collections

**Without features 1-4, stdlib code will look like C with English keywords.**
**Without features 5-6, stdlib will be non-idiomatic and error-prone.**

**Timeline Adjustment:** Error handling and generics moved to v0.0.9 to provide proper foundation for stdlib development in v0.1.0+.

---

## 📋 Milestone Overview

| Version | Focus Area | Status |
|---------|-----------|--------|
| **v0.0.7.5** | Self-hosting compiler (C bootstrap) | ✅ **COMPLETE** |
| **v0.0.8** | Core Language Complete (inline asm, imports, for loops, bitwise) | ✅ **COMPLETE**
| **v0.0.8.1** | Struct Construction & Field Access Syntax | ✅ **IN PROGRESS**
| **v0.0.8.2** | Collections (Lists, Dictionaries, Sets) + For Each Loops | 🔄 Planned |
| **v0.0.8.3** | Match/Pattern Matching + ADT/Variant Construction | 📋 Planned |
| **v0.0.8.4** | Lambda Expressions + Type Inference | 📋 Planned |
| **v0.0.8.5** | String Interpolation, Ternary Operator | 📋 Planned |
| **v0.0.8.6** | Advanced Types Phase 1: Range Constraints + Float/Float64 | 📋 Planned |
| **v0.0.8.7** | Advanced Types Phase 2: Wire Format Types (Integer16/32) + FFI Types | 📋 Planned |
| **v0.0.9** | Error Handling, Generics, Native Object Writer & Pure Runa Runtime | 📋 Planned |
| **v0.1.0** | Beta Release - Toolchain Independence + Stdlib Foundation | 🎯 Milestone |
| **v0.2.0** | Standard Library Expansion + Triple Syntax (--canon/--developer/--viewer) | 📋 Planned |
| **v0.3.0** | Debugging Tools & Dev Experience Improvements | 📋 Planned |
| **v0.4.0** | Memory Management & Safety Features (Ownership, Lifetimes) | 📋 Planned |
| **v0.5.0** | Optimization Passes (Basic - Constant Folding, DCE, Inlining) | 📋 Planned |
| **v0.6.0** | Advanced Type System Features (Traits, Union types, Refinement types) | 📋 Planned |
| **v0.6.1** | Type Inference, Refinement Types | 📋 Planned |
| **v0.7.0** | Concurrency Primitives (Threads, Mutexes, Channels) | 📋 Planned |
| **v0.7.1** | Async/Await, Actors | 📋 Planned |
| **v0.8.0** | Runa HIR (Human-Readable IR) + Advanced Optimization (PGO, LTO, SIMD) | 📋 Planned |
| **v0.8.1** | AOTT Tier 0-1: Lightning Interpreter + Smart Bytecode (uses HIR) | 📋 Planned |
| **v0.8.2** | AOTT Tier 2-3: Basic + Optimized Native Compilation (uses HIR) | 📋 Planned |
| **v0.8.3** | AOTT Tier 4: Speculative Execution (uses HIR) | 📋 Planned |
| **v0.9.0** | Cross-Compilation: Target Abstraction + Multi-Backend Foundation | 📋 Planned |
| **v0.9.1** | Cross-Compilation: Windows Support (x86-64 PE format) | 📋 Planned |
| **v0.9.2** | Cross-Compilation: macOS Support (x86-64 + ARM64 Mach-O format) | 📋 Planned |
| **v0.9.3** | Cross-Compilation: ARM64 Linux Support | 📋 Planned |
| **v0.9.4** | Cross-Compilation: WebAssembly Support (WASM + WASI) | 📋 Planned |
| **v0.9.5** | Package Management & Distribution | 📋 Planned |
| **v0.9.6** | IDE Tooling (LSP, Debugger, Profiler) | 📋 Planned |
| **v0.9.7** | AI Annotation System Implementation | 📋 Planned |
| **v1.0.0** | Production Release (All Platforms, All Features Complete) | 🎯 Goal |
| **v1.1** | Rosetta Stone Phase 1: C → Runa Translation | 📋 Planned |
| **v1.2** | Rosetta Stone Phase 2: Runa → Python Translation | 📋 Planned |
| **v1.3** | Rosetta Stone Phase 3: Bidirectional C ↔ Runa ↔ Python | 📋 Planned |

---

# 🔹 v0.0.8.2: Collections & For Each Loops

**Goal:** Implement essential collection types (Lists, Dictionaries, Sets) and natural iteration syntax.

**Priority:** HIGH - Required for stdlib and natural data structure usage.

## What Belongs Where:

### COMPILER (Parser/Codegen):
- ❌ **List literals (canonical)**: `Let numbers be list containing 1, 2, 3, 4, 5`
  - Parser: Recognize `list containing EXPR, EXPR, ...`
  - Codegen: Generate list_create() + list_append() for each element
- ❌ **Set literals (canonical)**: `Let unique be set containing 1, 2, 3`
  - Parser: Recognize `set containing EXPR, EXPR, ...`
  - Codegen: Generate set_create() + set_add() for each element
- ❌ **Dictionary literals (canonical)**:
  ```runa
  Let config be dictionary with:
      "width" as 800
      "height" as 600
  ```
  - Parser: Recognize `dictionary with: KEY as VALUE` (indented pairs)
  - Codegen: Generate dict_create() + dict_set() for each pair
- ❌ **For each loops**: `For each item in items: ... End For`
  - Parser: Recognize `For each IDENTIFIER in EXPRESSION:`
  - Codegen: Generate iterator pattern with list_length/list_get

### RUNTIME (Implemented in Runa, compiled with runtime):
- ❌ List operations: `list_create`, `list_append`, `list_insert`, `list_remove`, `list_get`, `list_set`, `list_length`
- ❌ Dictionary operations: `dict_create`, `dict_set`, `dict_get`, `dict_has`, `dict_keys`, `dict_values`
- ❌ Set operations: `set_create`, `set_add`, `set_contains`, `set_remove`, `set_union`, `set_intersection`

## Success Criteria:
- ✅ Canonical list syntax works: `list containing 1, 2, 3`
- ✅ Canonical set syntax works: `set containing 1, 2, 3`
- ✅ Canonical dictionary syntax works (indented key-value pairs)
- ✅ For each loops work with lists, sets, and dictionaries
- ✅ All collection operations implemented and tested
- ✅ Memory management (no leaks)
- ✅ Nested collections work: `list containing list containing 1, 2`
- ✅ Tests for all collection types

**Note:** Array literal syntax (`[1, 2, 3]`) is deferred to v0.2.0 as part of developer mode syntax.

## Timeline: TBD

---

# 🔹 v0.0.8.3: Match/Pattern Matching & ADT/Variant Construction

**Goal:** Implement pattern matching and algebraic data types (sum types/variants) - enables proper type-safe data modeling.

**Priority:** HIGH - ADTs are core to the type system and useless without pattern matching.

## What Belongs Where:

### COMPILER (Parser/Codegen):
- ❌ **Variant/ADT type definitions**:
  ```runa
  Type Shape is:
      | Circle with radius as Float
      | Rectangle with width as Float and height as Float
      | Triangle with base as Float and height as Float
  End Type
  ```
  - Parser: Recognize `Type NAME is: | Variant | Variant ...`
  - Type system: Store variant names and their fields
- ❌ **Variant construction**: `Let circle be Shape.Circle with radius as 5.0`
  - Parser: Recognize `TypeName.VariantName with field as value`
  - Codegen: Generate tagged union with discriminator + field storage
- ❌ **Match statement**: `Match value: When pattern: ... End Match`
  - Parser: Recognize `Match EXPR: When PATTERN: BLOCK ...`
  - Codegen: Generate switch/if-chain on discriminator
- ❌ **Pattern matching with variants**:
  ```runa
  Match shape:
      When Circle with radius as r:
          Return 3.14159 multiplied by r multiplied by r
      When Rectangle with width as w and height as h:
          Return w multiplied by h
  ```
  - Parser: Recognize `When VariantName with field as binding`
  - Codegen: Extract discriminator, extract fields from tagged union
- ❌ **Pattern matching with literals**: `When 0:`, `When "hello":`
- ❌ **Pattern matching with types**: `When value of type Integer:`
- ❌ **Wildcard pattern**: `When _:` (catch-all)
- ❌ **Exhaustiveness checking**: Compiler warns on missing variant cases

### TYPE SYSTEM (Enhanced):
- ❌ **Tagged union representation**: Discriminator (int) + max-sized field storage
- ❌ **Variant registry**: Store all variants for a type
- ❌ **Exhaustiveness analysis**: Verify all variants are handled

## Implementation Notes:

**Tagged union layout:**
```runa
# Type Shape is: Circle | Rectangle | Triangle
# Compiler generates:
struct Shape {
    int discriminator;  # 0=Circle, 1=Rectangle, 2=Triangle
    union {
        struct { float radius; } circle;
        struct { float width; float height; } rectangle;
        struct { float base; float height; } triangle;
    } data;
}
```

## Success Criteria:
- ✅ Variant type definitions parse correctly
- ✅ Variant construction works: `Shape.Circle with radius as 5.0`
- ✅ Match statements with multiple patterns work
- ✅ Pattern destructuring extracts fields correctly
- ✅ Exhaustiveness checking warns on missing cases
- ✅ Wildcard pattern `_` works as catch-all
- ✅ Nested patterns work: `When Some(x):`
- ✅ All tests pass including ADT tests

## Timeline: TBD

---

# 🔹 v0.0.8.4: Lambda Expressions & Type Inference

**Goal:** Implement first-class functions and basic type inference for improved developer experience.

**Priority:** MEDIUM-HIGH - Enables functional programming patterns and reduces verbosity.

## What Belongs Where:

### COMPILER (Parser/Codegen):
- ❌ **Lambda expressions**: `Let double be lambda x: x multiplied by 2`
  - Parser: Recognize `lambda PARAMS: EXPRESSION`
  - Codegen: Generate anonymous function with closure capture
- ❌ **Multi-parameter lambdas**: `Let add be lambda x, y: x plus y`
- ❌ **Lambda in function calls**: `Let doubled be Map over numbers using lambda x: x multiplied by 2`
- ❌ **Type inference for literals**: `Let x be 42` infers `Integer`, `Let name be "Alice"` infers `String`
- ❌ **Type inference for collections**: `Let numbers be list containing 1, 2, 3` infers `List of Integer`
- ❌ **Type inference for function returns**: Infer return type from function body
- ❌ **Type inference for lambda parameters**: Infer from usage context

### RUNTIME:
- ❌ **Function closures**: Capture environment (free variables)
- ❌ **Higher-order function utilities**: `map`, `filter`, `reduce`, `fold`
- ❌ **Closure memory management**: Allocate/deallocate closure environment

### TYPE SYSTEM (Enhanced):
- ❌ **Type inference engine**: Hindley-Milner-style inference (simplified)
- ❌ **Type unification**: Resolve type variables to concrete types
- ❌ **Type constraint solving**: Ensure consistent types across expressions

## Implementation Notes:

**Lambda closures capture environment:**
```runa
Let x be 10
Let add_x be lambda y: y plus x  # Captures 'x' from environment

# Compiler generates:
struct Closure {
    void* function_ptr;
    void* environment;  # Stores captured variables
}
```

**Type inference:**
```runa
# User writes:
Let x be 42

# Compiler infers:
Let x as Integer be 42
```

## Success Criteria:
- ✅ Lambda expressions parse and compile correctly
- ✅ Lambdas can be assigned to variables
- ✅ Lambdas can be passed to functions
- ✅ Closures capture free variables correctly
- ✅ Higher-order functions (map, filter, reduce) work
- ✅ Type inference works for literals, collections, and functions
- ✅ Type errors are reported when inference fails
- ✅ All tests pass including lambda and inference tests

## Timeline: TBD

---

# 🔹 v0.0.8.5: String Interpolation, Ternary Operator, Function Pointers & Character Type

**Goal:** Developer ergonomics improvements - syntactic sugar for common patterns, plus complete function pointers and character type support.

**Priority:** MEDIUM - Nice to have, but not critical for core functionality.

## What Belongs Where:

### COMPILER (Parser/Codegen):
- ❌ **String interpolation**: `Display f"Value is {x}"`
  - Parser: Recognize `f"text {expr} text"` format strings
  - Codegen: Generate string concatenation calls
- ❌ **Ternary operator**: `Let result be value If condition Otherwise other_value`
  - Parser: Recognize `EXPR If COND Otherwise EXPR`
  - Codegen: Generate conditional expression (inline if)
- ❌ **Range expressions**: `1 to 10`, `1 through 10`
  - Parser: Recognize range syntax
  - Codegen: Generate range iterator for For loops
- ⚠️ **Function pointers** (Complete implementation): `Let fn_ptr be $function_name`
  - Lexer: ✅ TOKEN_DOLLAR already implemented
  - Parser: ✅ EXPR_FUNCTION_POINTER already created
  - Codegen: ⚠️ Fix indirect call handling - currently incomplete
  - Support calling through function pointers: `fn_ptr(args)`
  - Support passing function pointers as arguments
- ⚠️ **Character type** (Complete implementation): `Let c be 'a'`
  - Lexer: ✅ TOKEN_CHARACTER_TYPE already exists
  - Lexer: ❌ Add character literal tokenization ('a', '\n', etc.)
  - Parser: ❌ Handle character literals in expressions
  - Codegen: ❌ Generate code for character operations
  - Runtime: ❌ Character-to-string conversion functions

### RUNTIME:
- ❌ **Format string support**: Convert expressions to strings for interpolation
- ❌ **String concatenation**: Efficient string building for interpolation
- ❌ **Character conversion**: `char_to_string()`, `string_to_char()`

## Success Criteria:
- ✅ String interpolation with expressions works
- ✅ Nested expressions in interpolation work: `f"Result: {x plus y}"`
- ✅ Ternary operator precedence is correct
- ✅ Range expressions work in For loops
- ✅ Function pointers fully working: creation with `$`, indirect calls, passing as parameters
- ✅ Character literals work: `'a'`, `'\n'`, `'\t'`, etc.
- ✅ Character type operations work
- ✅ All features tested

## Timeline: TBD

---

# 🔹 v0.0.9: Error Handling, Generics, Native Object Writer & Pure Runa Runtime

**Goals:**
1. **Error Handling & Generics** - Foundation for stdlib development
2. **Complete Toolchain Independence** - No `as`, no `ld`, no `gcc`. Zero C dependencies.
3. **Architectural Refactoring** - Transition from monolithic v0.0.8 to modular architecture

**📝 Note:** This version includes major architectural refactoring. See [V0_0_9_REFACTORING_PLAN.md](V0_0_9_REFACTORING_PLAN.md) for detailed breakdown of v0.0.9.0 → v0.0.9.1 → v0.0.9.2 → v0.0.9.3 phased implementation and module structure.

## Architecture Transition:

**Current State (v0.0.8):**
```
src/
├── main.runa (245 lines)
├── lexer.runa (1,576 lines) - MONOLITHIC
├── parser.runa (4,350 lines) - TOO LARGE
├── codegen.runa (3,490 lines) - MONOLITHIC
├── containers.runa (1,241 lines)
├── hashtable.runa (667 lines)
└── string_utils.runa (917 lines)
```

**Target State (v0.0.9.3):**
```
src/
├── frontend/
│   ├── lexer/ (lexer.runa, token.runa)
│   └── parser/ (parser.runa, ast.runa)
├── semantic/
│   ├── semantic_analyzer.runa
│   ├── type_checker.runa (with generics support)
│   └── symbol_table.runa
├── ir/
│   ├── hir/ (High-level IR)
│   └── mir/ (Mid-level IR)
├── backend/
│   └── x86_64/ (codegen.runa, instruction_selector.runa, object_writer.runa)
└── runtime/ (Pure Runa runtime - replaces runtime.c)
```

**Phased Implementation:**
- **v0.0.9.0**: Split lexer/parser, add Result/Option types, begin runtime.runa
- **v0.0.9.1**: Add semantic analysis phase, implement generics + type inference
- **v0.0.9.2**: Add IR layers (HIR/MIR), native ELF64 object writer, custom linker
- **v0.0.9.3**: Complete pure Runa runtime, eliminate runtime.c, zero external dependencies

## Features to Implement:

### 1. **Error Handling (Result & Option Types)**

**Motivation:** Stdlib needs proper error handling before v0.1.0. Moving from v0.3.0 to v0.0.9.

**Result Type:**
```runa
Note: Built-in Result type for operations that can fail
Type Result of T and E:
    Variant Success contains value as T
    Variant Failure contains error as E
End Type

Process called "divide" takes a as Integer, b as Integer returns Result of Integer and String:
    If b is equal to 0:
        Return a Failure with error as "Division by zero"
    End If
    Return a Success with value as a divided by b
End Process

Note: Usage
Let result be divide(10, 0)
Match result:
    When Success with value:
        display("Result: ")
        display_integer(value)
    When Failure with error:
        display("Error: ")
        display(error)
End Match
```

**Option Type:**
```runa
Note: Built-in Option type for optional values
Type Option of T:
    Variant Some contains value as T
    Variant None
End Type

Process called "find_user" takes id as Integer returns Option of String:
    If id is equal to 1:
        Return Some with value as "Alice"
    End If
    Return None
End Process
```

**Implementation Requirements:**
- Built-in `Result` and `Option` types in compiler
- Pattern matching support (already in v0.0.8.3)
- Type inference for generic types
- Helper methods: `is_success()`, `is_failure()`, `unwrap()`, `unwrap_or(default)`

### 2. **Generics (Parametric Polymorphism)**

**Motivation:** Stdlib needs generic collections. Moving from v0.6.0 to v0.0.9.

**Generic Types:**
```runa
Note: Generic List type
Type List of T:
    Field items as Integer  Note: Pointer to T array
    Field length as Integer
    Field capacity as Integer
End Type

Process called "list_create" of type T returns List of T:
    Let list be allocate(24)  Note: sizeof(List)
    memory_set_pointer(list, 0, 0)  Note: items = NULL
    memory_set_integer(list, 8, 0)   Note: length = 0
    memory_set_integer(list, 16, 0)  Note: capacity = 0
    Return list
End Process

Process called "list_append" of type T takes list as List of T, item as T returns Integer:
    Note: Implementation...
    Return 0
End Process
```

**Generic Functions:**
```runa
Process called "swap" of type T takes a as T, b as T returns Integer:
    Let temp be a
    Set a to b
    Set b to temp
    Return 0
End Process

Note: Usage with type inference
Let x be 5
Let y be 10
swap(x, y)  Note: Compiler infers T = Integer
```

**Implementation Requirements:**
- Generic type parameters: `Type Foo of T:` and `Process foo of type T:`
- Type inference for generic instantiation
- Monomorphization (generate separate code for each concrete type)
- Generic constraints (later): `Process foo of type T where T has Comparable:`

### 3. **ELF Object File Writer**
- Generate `.o` files directly (no `.s` intermediate)
- ELF64 format specification
- Symbol table generation
- Relocation entries
- Section headers (.text, .data, .rodata, .bss)

### 4. **Custom Linker**
- Link multiple `.o` files into executable
- Resolve symbols across modules
- Handle relocations
- Generate executable ELF binary
- Support for:
  - Static linking
  - Entry point specification
  - Section merging

### 5. **Pure Runa Runtime (Zero C)**
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

### 6. **New Compilation Flags**
```bash
# Direct object file generation:
runac program.runa -o program.o --emit=obj

# Link multiple objects:
runac --link main.o utils.o runtime/*.o -o program

# Or do both in one step (auto-links runtime):
runac main.runa utils.runa -o program
```

### 7. **File Format Support**
- **Phase 1:** ELF64 (Linux x86-64)
- **Phase 2:** PE (Windows) - future
- **Phase 3:** Mach-O (macOS) - future

### 8. **Build Process Changes**
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

**Error Handling & Generics:**
- ✅ Result<T,E> and Option<T> types work correctly
- ✅ Generic types and functions compile and instantiate properly
- ✅ Type inference works for generic parameters
- ✅ Pattern matching works with Result/Option
- ✅ Standard library can be written using these features

**Toolchain Independence:**
- ✅ Generate valid ELF object files
- ✅ Link multiple objects successfully
- ✅ Executables run without external assembler/linker
- ✅ **Pure Runa runtime (zero C code)**
- ✅ **Zero dependency on GCC, as, or ld**
- ✅ Self-hosting with native object generation
- ✅ Bootstrap produces identical binaries

## Timeline: TBD

---

# 🎯 v0.1.0: Beta Release - Toolchain Independence + Stdlib Foundation

**Goals:**
1. **Toolchain Independence** - Zero external dependencies (no GCC/as/ld)
2. **Stdlib Foundation** - Basic standard library using error handling & generics from v0.0.9

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

### 2. **Standard Library Foundation**
- `stdlib/result.runa` - Result<T,E> helper functions
- `stdlib/option.runa` - Option<T> helper functions
- `stdlib/list.runa` - Generic List<T> collection
- `stdlib/dict.runa` - Generic Dict<K,V> collection
- `stdlib/string.runa` - String utilities
- `stdlib/io.runa` - File I/O with error handling
- `stdlib/math.runa` - Mathematical functions

### 3. **Documentation**
- Complete language specification
- Standard library reference
- Compiler internals guide
- Migration guide from C/Rust/Python

### 4. **Packaging**
- Standalone binary distribution (Linux x86-64)
- Installation script
- Shell completion (bash, zsh)

### 5. **Testing Suite**
- 100+ test programs
- Regression test suite
- Performance benchmarks vs C/Rust/Python/Java
- Memory leak detection
- Stdlib unit tests

### 6. **Announcement**
- Blog post: "Runa v0.1.0: A Self-Hosting, Toolchain-Independent Language"
- HackerNews/Reddit launch
- GitHub release with binaries

## Success Criteria:
- ✅ No external dependencies (except libc for syscalls)
- ✅ Basic stdlib modules working with error handling & generics
- ✅ Passes all test suites (compiler + stdlib)
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

  **Field Access:**
  - Dot notation: `p.x` instead of `the x of p`
  - Dot assignment: `p.x = 15` instead of `Set the x of p to 15`

  **Collection Literals:**
  - Array literals: `[1, 2, 3]` instead of `list containing 1, 2, 3`
  - Dict literals: `{"key": value}` instead of `dictionary with: "key" as value`
  - Set literals: `{1, 2, 3}` instead of `set containing 1, 2, 3`

  **Type Syntax:**
  - Generic types: `List[Integer]` instead of `List of Integer`
  - Function types: `Function[Integer, Integer]` instead of function pointer syntax

  **Operators:**
  - Mathematical: `+`, `-`, `*`, `/`, `%`, `**` instead of `plus`, `minus`, etc.
  - Comparison: `==`, `!=`, `<`, `>`, `<=`, `>=` instead of `is equal to`, etc.
  - Logical: `&&`, `||`, `!` instead of `and`, `or`, `not`
  - Assignment: `=` instead of `be`

  **Control Flow:**
  - If syntax: `if (condition) { ... } else { ... }` instead of `If condition: ... Otherwise: ... End If`
  - For loops: `for item in items { ... }` instead of `For each item in items: ... End For`
  - While loops: `while (condition) { ... }` instead of `While condition: ... End While`

  **Functions:**
  - Function syntax: `proc name()` instead of `Process called "name"`
  - Return syntax: `return value` instead of `Return value`

  **Comments:**
  - Line comments: `//` instead of `Note:`
  - Block comments: `/* ... */` instead of multi-line `Note:`

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
- ✅ Bidirectional conversion between canon and developer modes preserves semantics
- ✅ All developer mode features work (deferred from v0.0.8.x):
  - ✅ Dot notation for field access (`p.x` from v0.0.8.1)
  - ✅ Array literals (`[1, 2, 3]` from v0.0.8.2)
  - ✅ Dict/Set literals (`{...}` from v0.0.8.2)
  - ✅ Generic type syntax (`List[Integer]` from v0.0.8.4)
  - ✅ Mathematical operators (`+`, `-`, `*`, `/`)
  - ✅ Comparison operators (`==`, `!=`, `<`, `>`, `<=`, `>=`)
  - ✅ Logical operators (`&&`, `||`, `!`)
  - ✅ C-style control flow (`if`, `for`, `while` with braces)
  - ✅ Short function syntax (`proc`, `return`)
  - ✅ Developer comments (`//` and `/* */`)
- ✅ `runafmt` tool can convert any Runa code between modes
- ✅ Documentation showing all three syntax forms side-by-side
- ✅ Example programs demonstrating all modes
- ✅ Comprehensive test suite covering all syntax variations

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

**CURRENT STATUS (v0.0.7.6): MEMORY UNSAFE**
- ❌ No reference counting
- ❌ No garbage collection
- ❌ No automatic lifetime tracking
- ❌ No borrow checker
- ❌ No ownership system
- ❌ Manual malloc/free (same memory bugs as C)

**See:** `UNIVERSAL_LANGUAGE_GAP_ANALYSIS.md` for detailed analysis

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
- ❌ **Automatic Reference Counting (ARC)** - Primary memory management strategy
  ```runa
  # Automatic - user doesn't see this:
  # Object header includes reference count
  # Compiler inserts increment/decrement automatically
  # Object freed when count reaches zero
  ```

- ❌ **Garbage Collection (GC)** - For handling cyclic references
  ```runa
  # Mark-and-sweep GC for cycles that ARC can't handle
  # Triggered automatically when memory pressure increases
  # Optional, can be disabled with compiler flag
  ```

- ❌ **Reference Counted Types (Rc<T>)** - Manual shared ownership
  ```runa
  Type called "RcString":
      data as String
      ref_count as Integer
  End Type
  ```

- ❌ **Arena Allocators** - Bulk deallocation for performance
  ```runa
  Let arena be arena_create(1024)  # 1KB arena
  Let data be arena_allocate(arena, 256)
  # ... use data ...
  arena_destroy(arena)  # Frees all at once
  ```

- ❌ **Leak Detection** - Runtime tracking (debug mode)
  - Track all allocations
  - Report leaked objects on program exit
  - Source location for leak origin

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

# 🔹 v0.8.0: Runa HIR (Human-Readable IR) + Advanced Optimization & Profiling

**Goal:** Implement Runa's Human-Readable Intermediate Representation (HIR) as the universal translation layer, enabling cross-compilation, AOTT, and advanced optimizations.

**Philosophy:** Build our own IR (Runa HIR) - NOT LLVM IR - that is human-readable, preserves high-level semantics, and can be written/edited by humans.

## What Belongs Where:

### COMPILER (Runa HIR Implementation):

- ❌ **HIR Design & Specification**
  - **Human-readable intermediate representation** - Valid Runa code (can be written/edited by humans)
  - **Preserves high-level semantics** - NOT low-level SSA like LLVM IR
  - **Triple syntax support** (--canon, --viewer, --developer)
  - **Language-agnostic abstractions** - Universal semantic representation
  - **Metadata system** - Preserve language-specific features

  **Why Runa HIR vs LLVM IR:**
  | Feature | LLVM IR | Runa HIR |
  |---------|---------|----------|
  | Human Readable | ❌ SSA, registers, basic blocks | ✅ Valid Runa code |
  | Bidirectional | ❌ One-way only | ✅ Two-way with semantics |
  | Preserves Semantics | ❌ Low-level only | ✅ High-level concepts |
  | Multiple Syntax | ❌ Single form | ✅ Triple syntax |
  | Writeable | ❌ Too complex | ✅ Yes (--canon, --developer) |

  **HIR Node Types:**
  ```runa
  Type called "HIRNode":
      node_id as String
      node_type as HIRNodeType
      source_location as SourceLocation
      type_signature as TypeInfo
      metadata as Dictionary
  End Type

  Type called "HIRNodeType" is one of:
      | ProgramRoot
      | ModuleDefinition
      | FunctionDefinition
      | TypeDefinition
      | VariableDeclaration
      | Expression
      | Statement
      | ControlFlow
      | Pattern
  End Type
  ```

- ❌ **AST → HIR Lowering**
  ```
  Runa Source → Parse → AST → Lower to HIR → Optimize → Codegen
  ```
  - Convert AST to HIR representation
  - Preserve type information
  - Maintain semantic meaning
  - Keep variable names and structure
  - Attach metadata for language features

  **Example Lowering:**
  ```runa
  # Source (Canonical):
  Process called "factorial" takes n as Integer returns Integer:
      If n is less than or equal to 1:
          Return 1
      End If
      Return n times factorial(n minus 1)
  End Process

  # HIR (same as source - HIR is valid Runa):
  Process called "factorial" takes n as Integer returns Integer:
      If n is less than or equal to 1:
          Return 1
      End If
      Return n times factorial(n minus 1)
  End Process
  ```

- ❌ **HIR → Multiple Backends**
  - HIR → x86-64 assembly (Linux/Windows/macOS)
  - HIR → AArch64 assembly (ARM64)
  - HIR → WASM bytecode
  - Foundation for cross-compilation (v0.9.0+)

  **Backend Interface:**
  ```runa
  Process called "codegen_generate" takes program as Integer, target as Integer returns Integer:
      Let arch be memory_get_pointer(target, 0)  # target->arch

      If string_equals(arch, "x86_64") is equal to 1:
          Return codegen_x86_64_generate(program, target)
      Otherwise If string_equals(arch, "aarch64") is equal to 1:
          Return codegen_aarch64_generate(program, target)
      Otherwise If string_equals(arch, "wasm32") is equal to 1:
          Return codegen_wasm_generate(program, target)
      End If
  End Process
  ```

- ❌ **HIR Optimization Passes**
  - Constant folding on HIR
  - Dead code elimination on HIR
  - Inlining at HIR level
  - Common subexpression elimination

- ❌ **Triple Syntax Generators**
  Generate three different syntax views from HIR:

  **--canon (Canonical - Structured):**
  ```runa
  Process called "factorial" takes n as Integer returns Integer:
      If n is less than or equal to 1:
          Return 1
      End If
      Return n times factorial(n minus 1)
  End Process
  ```

  **--viewer (Natural Language - Read-only):**
  ```
  Define a process called "factorial" that takes an integer n and returns an integer.
  If n is less than or equal to 1, return 1.
  Otherwise, return n multiplied by the factorial of n minus 1.
  ```

  **--developer (Concise - Writeable):**
  ```runa
  proc factorial(n: int) -> int:
      if n <= 1:
          ret 1
      End if
      ret n * factorial(n - 1)
  End proc
  ```

### COMPILER (Advanced Optimization):

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

# 🔹 v0.9.0: Cross-Compilation: Target Abstraction + Multi-Backend Foundation

**Goal:** Abstract compiler to support multiple target platforms, laying the foundation for Windows, macOS, ARM64, and WASM support.

**Philosophy:** Build it entirely in Runa using Runa HIR - no external dependencies, no LLVM IR (we build our own IR).

## Cross-Compilation Overview:

Cross-compilation allows developers to:
- Compile Windows binaries on Linux
- Compile macOS binaries on Windows
- Compile ARM binaries on x86-64
- Compile WASM from any platform

**Implementation Order (v0.9.0-v0.9.4):**
1. x86-64 Linux (v0.0.7.5 ✅ COMPLETE)
2. x86-64 Windows PE format (v0.9.1)
3. x86-64 + ARM64 macOS Mach-O format (v0.9.2)
4. ARM64 Linux (v0.9.3)
5. WASM + WASI (v0.9.4)

## What Belongs Where:

### COMPILER (Target Abstraction):
- ❌ **Target Triple System**
  ```runa
  # Target format: <arch>-<os>-<abi>
  # Examples: x86_64-linux-gnu, x86_64-windows-msvc, aarch64-darwin-macho

  Type called "Target":
      arch as String        # "x86_64", "aarch64", "wasm32"
      os as String          # "linux", "windows", "darwin", "wasi"
      abi as String         # "gnu", "msvc", "darwin", "wasi"
      format as String      # "elf64", "pe", "macho", "wasm"
      endian as String      # "little", "big"
      pointer_size as Integer  # 4 (32-bit) or 8 (64-bit)
  End Type

  Process called "target_from_triple" takes triple as String returns Integer:
      # Parse "x86_64-linux-gnu" → Target struct
      # Returns pointer to Target
  End Process
  ```

- ❌ **Compiler Flag: `--target`**
  ```bash
  # Compile for current platform (default):
  runac program.runa -o program

  # Cross-compile for Windows:
  runac --target=x86_64-windows program.runa -o program.exe

  # Cross-compile for macOS:
  runac --target=x86_64-darwin program.runa -o program

  # Cross-compile for ARM64 Linux:
  runac --target=aarch64-linux program.runa -o program-arm

  # Compile to WebAssembly:
  runac --target=wasm32-wasi program.runa -o program.wasm

  # List available targets:
  runac --list-targets
  ```

- ❌ **Refactor Codegen for Multi-Backend**
  ```
  Current (v0.0.7.5):
  src/codegen.runa  → Generates x86-64 assembly only

  Future (v0.9.0+):
  src/codegen/
  ├── codegen_common.runa      # Shared logic (HIR traversal, etc.)
  ├── codegen_x86_64.runa      # x86-64 instruction generation
  ├── codegen_aarch64.runa     # ARM64 instruction generation
  ├── codegen_wasm.runa        # WASM bytecode generation
  ├── target.runa              # Target abstraction
  └── backend_interface.runa   # Backend API
  ```

  **Backend Selection:**
  ```runa
  Process called "codegen_generate" takes program as Integer, target as Integer returns Integer:
      Let arch be memory_get_pointer(target, 0)  # target->arch

      If string_equals(arch, "x86_64") is equal to 1:
          Return codegen_x86_64_generate(program, target)
      Otherwise If string_equals(arch, "aarch64") is equal to 1:
          Return codegen_aarch64_generate(program, target)
      Otherwise If string_equals(arch, "wasm32") is equal to 1:
          Return codegen_wasm_generate(program, target)
      Otherwise:
          Print "Unsupported architecture: "
          Print arch
          exit_with_code(1)
      End If
  End Process
  ```

- ❌ **Host Target Detection**
  - Auto-detect current platform (x86_64-linux, x86_64-windows, etc.)
  - Use as default if `--target` not specified

- ❌ **Multi-Format Object Writer Foundation**
  ```
  Current (v0.0.9 Plan):
  src/object_writer.runa  → Writes ELF64 only

  Future (v0.9.1+):
  src/formats/
  ├── elf64.runa           # ELF 64-bit format (Linux, BSD)
  ├── pe.runa              # PE format (Windows) - v0.9.1
  ├── macho.runa           # Mach-O format (macOS, iOS) - v0.9.2
  ├── wasm.runa            # WebAssembly module format - v0.9.4
  └── format_common.runa   # Shared utilities
  ```

  **Format Selection:**
  ```runa
  Process called "write_object_file" takes code as Integer, target as Integer, filename as String returns Integer:
      Let format be memory_get_pointer(target, 24)  # target->format

      If string_equals(format, "elf64") is equal to 1:
          Return write_elf64(code, target, filename)
      Otherwise If string_equals(format, "pe") is equal to 1:
          Return write_pe(code, target, filename)
      Otherwise If string_equals(format, "macho") is equal to 1:
          Return write_macho(code, target, filename)
      Otherwise If string_equals(format, "wasm") is equal to 1:
          Return write_wasm(code, target, filename)
      End If
  End Process
  ```

### STANDARD LIBRARY (Cross-Platform Abstraction):

**Challenge:** System calls differ across platforms.

**Solution:** Platform abstraction layer.

```runa
# Public API (platform-independent):
Process called "file_open" takes path as String, mode as Integer returns Integer:
    Let target be get_current_target()
    Let os be memory_get_pointer(target, 8)  # target->os

    If string_equals(os, "linux") is equal to 1:
        Return file_open_linux(path, mode)
    Otherwise If string_equals(os, "windows") is equal to 1:
        Return file_open_windows(path, mode)
    Otherwise If string_equals(os, "darwin") is equal to 1:
        Return file_open_darwin(path, mode)
    Otherwise If string_equals(os, "wasi") is equal to 1:
        Return file_open_wasi(path, mode)
    End If
End Process
```

**Standard Library Structure:**
```
stdlib/
├── io/
│   ├── io_common.runa       # Public API
│   ├── io_linux.runa        # Linux syscalls
│   ├── io_windows.runa      # Windows API
│   ├── io_darwin.runa       # macOS syscalls
│   └── io_wasi.runa         # WASI functions
├── fs/
│   ├── fs_common.runa
│   ├── fs_linux.runa
│   ├── fs_windows.runa
│   └── fs_darwin.runa
└── net/
    ├── net_common.runa
    ├── net_posix.runa       # Linux/macOS/BSD
    └── net_windows.runa     # Winsock
```

## Format Complexity Comparison:

| Format | Platform | Difficulty | Lines of Code (est.) | Target Version |
|--------|----------|------------|---------------------|----------------|
| **ELF64** | Linux | ⭐⭐⭐ Medium | ~1000 LOC | v0.0.9 ✅ |
| **PE** | Windows | ⭐⭐⭐⭐ Hard | ~2000 LOC | v0.9.1 |
| **Mach-O** | macOS | ⭐⭐⭐⭐ Hard | ~2000 LOC | v0.9.2 |
| **WASM** | Web | ⭐⭐ Easy | ~500 LOC | v0.9.4 |

**Why ELF is easiest:**
- Well-documented specification
- Simpler structure (sections, symbols, relocations)
- No code signing requirements
- Open-source tooling for reference

**Why PE/Mach-O are harder:**
- Complex import/export tables
- Code signing (macOS)
- Platform-specific quirks
- Less documentation

## Success Criteria:
- ✅ Can specify `--target` flag (even if only x86-64 Linux works)
- ✅ Codegen is target-aware (accepts Target parameter)
- ✅ Architecture cleanly separated (ready for new backends)
- ✅ HIR → Backend interface well-defined
- ✅ Foundation ready for v0.9.1+ (Windows, macOS, ARM64, WASM)

## Timeline: 3-4 weeks

---

# 🔹 v0.9.1: Cross-Compilation: Windows Support (x86-64)

**Goal:** Enable cross-compilation to Windows PE format with Microsoft x64 calling convention.

## Platform Details:

**File Format:** PE (Portable Executable)
**Calling Convention:** Microsoft x64 (different from System V!)
**System API:** Win32 API (no direct syscalls)

## What Belongs Where:

### COMPILER:
- ❌ **PE Object Writer** (src/formats/pe.runa)
  - Portable Executable format for Windows
  - Import/export tables
  - DLL linking
  - Resource sections

- ❌ **Microsoft x64 Calling Convention** (codegen_x86_64.runa)

  **Key Differences from Linux (System V):**
  - Arguments passed in: **RCX, RDX, R8, R9** (not RDI, RSI, RDX, RCX)
  - **Shadow space:** 32 bytes reserved on stack (even if not used)
  - Different system calls (via kernel32.dll, not syscall instruction)
  - No direct syscalls - must use DLLs

  **Example Windows Function Call:**
  ```runa
  # Windows x64 function call:
  Process called "windows_print" takes message as String:
      Inline Assembly:
          # Windows x64 ABI:
          # RCX = first argument
          # RDX = second argument
          # R8 = third argument
          # R9 = fourth argument
          # Stack must have 32-byte shadow space

          sub $32, %rsp           # Allocate shadow space
          movq -8(%rbp), %rcx     # Load message into RCX (first arg)
          call WriteConsoleA      # Windows API function
          add $32, %rsp           # Clean up shadow space
      End Assembly
  End Process
  ```

- ❌ **Windows Codegen Backend**
  - Use Win32 API (no direct syscalls)
  - DLL imports (kernel32.dll, user32.dll, etc.)
  - Exception handling (SEH - Structured Exception Handling)

### STANDARD LIBRARY:
- ❌ **Windows Stdlib Port** (stdlib/platform/windows/)

  **Platform-specific implementations:**
  ```runa
  Process called "file_open_windows" takes path as String, mode as Integer returns Integer:
      # Windows API: CreateFileA
      # Call Win32 API (requires different calling convention)
      # Returns: File handle or INVALID_HANDLE_VALUE (-1)
  End Process

  Process called "file_read_windows" takes fd as Integer, buffer as String, length as Integer returns Integer:
      # Windows API: ReadFile
  End Process

  Process called "file_write_windows" takes fd as Integer, buffer as String, length as Integer returns Integer:
      # Windows API: WriteFile
  End Process
  ```

  **Full Windows stdlib:**
  - file_open_windows (CreateFileA)
  - file_read_windows (ReadFile)
  - file_write_windows (WriteFile)
  - file_close_windows (CloseHandle)
  - network_windows (Winsock API - WSAStartup, socket, connect, send, recv)
  - process_windows (CreateProcess)
  - thread_windows (CreateThread)
  - memory_windows (VirtualAlloc, VirtualFree)

### TESTING:
- ❌ Test on Windows (native or Wine)
- ❌ Add Windows to CI/CD pipeline
- ❌ Cross-compilation tests (compile on Linux, run on Windows)

## Success Criteria:
- ✅ `runac --target=x86_64-windows program.runa -o program.exe` works
- ✅ Generated .exe runs correctly on Windows
- ✅ Standard library functions work on Windows
- ✅ Can cross-compile from Linux to Windows
- ✅ Microsoft x64 calling convention implemented correctly
- ✅ Win32 API calls work (file I/O, networking, processes)

## Timeline: 4-6 weeks

---

# 🔹 v0.9.2: Cross-Compilation: macOS Support (x86-64 + ARM64)

**Goal:** Enable cross-compilation to macOS Mach-O format for Intel and Apple Silicon.

## Platform Details:

**File Format:** Mach-O (Mach Object)
**Calling Convention:** System V (same as Linux for x86-64), AAPCS64 (ARM64)
**System API:** BSD syscalls (similar to Linux)
**Challenge:** Code signing required on Apple Silicon

## What Belongs Where:

### COMPILER:
- ❌ **Mach-O Object Writer** (src/formats/macho.runa)
  - Mach-O format for macOS/iOS
  - Load commands
  - Section layout (__TEXT, __DATA, __LINKEDIT)
  - Dynamic linking (dyld)
  - Universal binaries (fat binaries - both x86-64 and ARM64 in one file)

- ❌ **macOS Syscall Differences**
  - **Syscall numbers:** 0x2000000 offset (macOS-specific)
  - BSD-style syscalls (similar to Linux)
  - Different syscall numbers (write = 0x2000004, not 1)
  - Different dynamic linker
  - Different section names

  **Example macOS Syscall:**
  ```runa
  # macOS syscall (write):
  Process called "macos_write" takes fd as Integer, buffer as String, length as Integer returns Integer:
      Inline Assembly:
          mov $0x2000004, %rax    # macOS syscall: write (0x2000000 + 4)
          movq -8(%rbp), %rdi     # fd
          movq -16(%rbp), %rsi    # buffer
          movq -24(%rbp), %rdx    # length
          syscall
      End Assembly
      Return 0
  End Process
  ```

- ❌ **Apple Silicon (ARM64) Support**
  - **AArch64 codegen** (src/codegen/codegen_aarch64.runa)
  - Apple's ARM64 calling convention (AAPCS64)
  - Code signing requirements (ad-hoc signing for development)

  **ARM64 Architecture Details:**
  - Different instruction set (ARM vs x86)
  - Different registers (X0-X30 vs RAX-R15)
  - Different syscall instruction (SVC vs SYSCALL)

  **Example ARM64 Syscall:**
  ```runa
  # ARM64 syscall (exit):
  Process called "arm64_exit" takes code as Integer:
      Inline Assembly:
          mov x8, #1             // syscall number: exit
          ldr x0, [fp, #-8]      // load exit code
          svc #0                 // invoke syscall
      End Assembly
  End Process
  ```

  **ARM64 Calling Convention (AAPCS64):**
  - Arguments in: X0, X1, X2, X3, X4, X5, X6, X7
  - Return value in: X0
  - Callee-saved: X19-X29
  - Stack pointer: SP (X31)
  - Frame pointer: FP (X29)
  - Link register: LR (X30)

### STANDARD LIBRARY:
- ❌ **macOS Stdlib Port** (stdlib/platform/darwin/)

  **Platform-specific implementations:**
  ```runa
  Process called "file_open_darwin" takes path as String, mode as Integer returns Integer:
      # macOS syscall: open (2) - similar to Linux but different syscall number
      # Syscall number: 0x2000000 + 5 = 0x2000005
  End Process

  Process called "network_darwin" takes ...:
      # BSD sockets (same as Linux, just different syscall numbers)
  End Process

  Process called "process_darwin" takes ...:
      # BSD fork/exec
  End Process
  ```

  **Full macOS stdlib:**
  - file_open_darwin (BSD open syscall: 0x2000005)
  - file_read_darwin (BSD read syscall: 0x2000003)
  - file_write_darwin (BSD write syscall: 0x2000004)
  - network_darwin (BSD sockets)
  - process_darwin (BSD fork/exec)
  - thread_darwin (pthread)
  - memory_darwin (mmap, munmap)

### TESTING:
- ❌ Test on macOS Intel (x86-64)
- ❌ Test on macOS Apple Silicon (ARM64)
- ❌ Test universal binaries (fat binaries with both architectures)
- ❌ Add macOS to CI/CD pipeline
- ❌ Handle code signing (ad-hoc for development, proper signing for distribution)

## Success Criteria:
- ✅ `runac --target=x86_64-darwin program.runa -o program` works
- ✅ `runac --target=aarch64-darwin program.runa -o program` works
- ✅ Generated binaries run on Intel Macs
- ✅ Generated binaries run on Apple Silicon
- ✅ Standard library works on macOS
- ✅ Can create universal binaries (both x86-64 and ARM64)
- ✅ Code signing works (ad-hoc for development)

## Timeline: 4-6 weeks

---

# 🔹 v0.9.3: Cross-Compilation: ARM64 Linux Support

**Goal:** Enable cross-compilation to ARM64 Linux for servers, Raspberry Pi, and mobile devices.

## Platform Details:

**Architecture:** AArch64 (ARM64)
**File Format:** ELF64 (same as x86-64 Linux)
**Calling Convention:** AAPCS64 (ARM Architecture Procedure Call Standard)
**System API:** Linux syscalls (same numbers as x86-64)

## What Belongs Where:

### COMPILER:
- ❌ **ARM64 Linux Backend**
  - Use existing codegen_aarch64.runa (from v0.9.2)
  - ELF64 format (same as x86-64 Linux)
  - AAPCS64 calling convention

- ❌ **ARM64-Specific Codegen**

  **Register Allocation:**
  - General purpose: X0-X30 (64-bit), W0-W30 (32-bit lower halves)
  - Special registers:
    - SP (Stack Pointer) = X31
    - FP (Frame Pointer) = X29
    - LR (Link Register) = X30
    - PC (Program Counter) - not directly accessible

  **Syscall Mechanism:**
  - Instruction: **SVC #0** (not SYSCALL like x86-64)
  - Syscall number in: X8
  - Arguments in: X0, X1, X2, X3, X4, X5
  - Return value in: X0

  **Example ARM64 Linux Syscall (write):**
  ```runa
  Process called "arm64_linux_write" takes fd as Integer, buffer as String, length as Integer returns Integer:
      Inline Assembly:
          mov x8, #64            // syscall number: write (same as x86-64)
          ldr x0, [fp, #-8]      // fd
          ldr x1, [fp, #-16]     // buffer
          ldr x2, [fp, #-24]     // length
          svc #0                 // invoke syscall (different from x86-64 SYSCALL)
      End Assembly
      Return 0
  End Process
  ```

  **ARM64 Instructions:**
  - Load/store: LDR (load register), STR (store register)
  - Arithmetic: ADD, SUB, MUL, SDIV (signed divide)
  - Logical: AND, ORR (OR), EOR (XOR)
  - Branch: B (branch), BL (branch and link), BR (branch register), BLR (branch link register)
  - Compare: CMP, TST
  - Conditional: B.EQ, B.NE, B.LT, B.GT, etc.

### STANDARD LIBRARY:
- ❌ **ARM64 Linux Stdlib**
  - **Same syscall numbers** as x86-64 Linux (write=1, read=0, open=2, etc.)
  - **Same APIs** (reuse Linux stdlib logic)
  - **Different implementation** (ARM64 assembly instead of x86-64)

  **Key Advantage:** Most code can be shared with x86-64 Linux, just different codegen.

  ```runa
  # Platform abstraction (same for both architectures):
  Process called "file_open_linux" takes path as String, mode as Integer returns Integer:
      Let arch be get_current_arch()

      If string_equals(arch, "x86_64") is equal to 1:
          # Use x86-64 syscall instruction
      Otherwise If string_equals(arch, "aarch64") is equal to 1:
          # Use ARM64 SVC instruction
      End If
  End Process
  ```

### TESTING:
- ❌ Test on Raspberry Pi 4 (ARM64)
- ❌ Test on ARM64 servers (AWS Graviton, Oracle Cloud, etc.)
- ❌ Add ARM64 to CI/CD pipeline (use QEMU for emulation)
- ❌ Cross-compilation tests (compile on x86-64, run on ARM64)

## Success Criteria:
- ✅ `runac --target=aarch64-linux program.runa -o program` works
- ✅ Generated binaries run on ARM64 Linux
- ✅ Standard library works on ARM64 Linux
- ✅ Can cross-compile from x86-64 to ARM64
- ✅ Performance comparable to x86-64 (accounting for CPU differences)

## Timeline: 3-4 weeks

---

# 🔹 v0.9.4: Cross-Compilation: WebAssembly Support

**Goal:** Enable compilation to WebAssembly for browsers, Node.js, and edge computing.

## Platform Details:

**Architecture:** Stack-based VM (not register-based)
**File Format:** WASM binary module (.wasm)
**System API:** WASI (WebAssembly System Interface)
**Challenge:** Sandboxed environment, limited system access

## What Belongs Where:

### COMPILER:
- ❌ **WASM Bytecode Generator** (src/codegen/codegen_wasm.runa)
  - HIR → WASM bytecode
  - Stack-based VM instructions (not registers like x86/ARM)
  - Module format (.wasm binary)
  - Text format (.wat) for debugging

  **Key Differences from Native Code:**
  - **No registers** - stack-based (push/pop operations)
  - **No direct memory access** - sandboxed linear memory
  - **No syscalls** - must use WASI functions
  - **Bytecode, not assembly** - virtual machine instructions

- ❌ **WASM Instructions**

  **Arithmetic:**
  - i32.add, i32.sub, i32.mul, i32.div_s (signed), i32.div_u (unsigned)
  - i64.add, i64.sub, i64.mul, i64.div_s, i64.div_u
  - f32.add, f32.sub, f32.mul, f32.div
  - f64.add, f64.sub, f64.mul, f64.div

  **Control Flow:**
  - if...else...end
  - loop...end
  - block...end
  - br (branch), br_if (conditional branch)
  - return

  **Memory:**
  - i32.load, i64.load (load from linear memory)
  - i32.store, i64.store (store to linear memory)
  - memory.size, memory.grow

  **Functions:**
  - call (direct function call)
  - call_indirect (indirect call through table)

  **Example WASM Code Generation:**
  ```runa
  # Runa source:
  Let x be 5 plus 3

  # Generated WASM (text format):
  i32.const 5    ;; push 5 onto stack
  i32.const 3    ;; push 3 onto stack
  i32.add        ;; pop two values, add, push result
  local.set 0    ;; store in local variable 0 (x)

  # Note: WASM doesn't use assembly - generates bytecode directly
  # No registers like RAX, X0 - everything on stack
  ```

- ❌ **WASI Support** (WebAssembly System Interface)

  **WASI provides:**
  - File I/O: fd_read, fd_write, fd_close, path_open
  - Environment variables: environ_get, environ_sizes_get
  - Command-line args: args_get, args_sizes_get
  - Random numbers: random_get
  - Clock: clock_time_get
  - Process exit: proc_exit

  **Example WASI Usage:**
  ```runa
  Process called "wasm_write" takes fd as Integer, buffer as String, length as Integer returns Integer:
      # Call WASI fd_write function (not syscall!)
      # WASI functions are imported from host environment
  End Process
  ```

### STANDARD LIBRARY:
- ❌ **WASM Stdlib Port** (stdlib/platform/wasi/)

  **Platform-specific implementations:**
  ```runa
  Process called "file_open_wasi" takes path as String, mode as Integer returns Integer:
      # WASI: path_open
      # Different from syscalls - sandbox-safe API
  End Process

  Process called "file_read_wasi" takes fd as Integer, buffer as String, length as Integer returns Integer:
      # WASI: fd_read
  End Process

  Process called "file_write_wasi" takes fd as Integer, buffer as String, length as Integer returns Integer:
      # WASI: fd_write
  End Process
  ```

  **Full WASI stdlib:**
  - file_open_wasi (path_open)
  - file_read_wasi (fd_read)
  - file_write_wasi (fd_write)
  - file_close_wasi (fd_close)
  - Sandboxed environment (no raw syscalls, no direct memory access)
  - Limited to WASI capabilities (no networking in WASI preview1)

### TESTING:
- ❌ Test in browsers (Chrome, Firefox, Safari)
- ❌ Test in Node.js (with WASI support: `node --experimental-wasi-unstable-preview1`)
- ❌ Test in Deno, Wasmer, Wasmtime
- ❌ Test in edge runtimes (Cloudflare Workers, Fastly Compute@Edge)
- ❌ Add WASM to CI/CD pipeline

## Success Criteria:
- ✅ `runac --target=wasm32-wasi program.runa -o program.wasm` works
- ✅ Generated .wasm runs in browsers
- ✅ Generated .wasm runs in Node.js with WASI
- ✅ Generated .wasm runs in Deno, Wasmer, Wasmtime
- ✅ Standard library works in WASM environment (sandboxed)
- ✅ Can output .wat (text format) for debugging

## Timeline: 4-5 weeks

---

# 🔹 v0.9.5: Package Management & Distribution

**Goal:** Complete package ecosystem for code sharing and distribution (moved from v0.9.0).

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

# 🔹 v0.9.6: IDE Tooling (LSP, Debugger, Profiler)

**Goal:** Professional developer tools for productivity (moved from v0.9.1).

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

# 🔹 v0.9.7: AI Annotation System Implementation

**Goal:** Implement AI-first annotation system from specification (moved from v0.9.2).

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

**Goal:** Stable, documented, production-ready language with full cross-platform support.

## Platform Support (ALL COMPLETE):
- ✅ x86-64 Linux (ELF64)
- ✅ x86-64 Windows (PE)
- ✅ x86-64 macOS (Mach-O)
- ✅ ARM64 Linux (ELF64)
- ✅ ARM64 macOS / Apple Silicon (Mach-O)
- ✅ WebAssembly (WASM + WASI)

## Feature Completeness (ALL COMPLETE):
- ✅ Advanced Type System (Range constraints, Float, Wire formats, FFI types)
- ✅ Error Handling & Generics
- ✅ Native Object Writer & Pure Runa Runtime
- ✅ Standard Library (comprehensive, cross-platform)
- ✅ Triple Syntax (--canon, --developer, --viewer)
- ✅ Memory Management & Safety (Ownership, Lifetimes)
- ✅ Optimization Passes (Constant folding, DCE, Inlining, PGO, LTO)
- ✅ Runa HIR (Human-Readable IR) for cross-compilation
- ✅ Concurrency (Threads, Mutexes, Channels, Async/Await, Actors)
- ✅ AOTT (All-Of-The-Time optimization, Tier 0-4)
- ✅ Package Management (`rpack`)
- ✅ IDE Tooling (LSP, Debugger, Profiler)
- ✅ AI Annotation System

## Final Polish:

### 1. **Stability**
- ❌ Zero known critical bugs
- ❌ 1000+ test programs pass (all platforms)
- ❌ Fuzz testing (10 million+ inputs, no crashes)
- ❌ Memory safety verified (Valgrind clean)
- ❌ Security audit completed
- ❌ Stress testing (long-running programs, high concurrency)
- ❌ Cross-platform testing (Linux, Windows, macOS, ARM64, WASM)

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

# 🔹 v1.1: Rosetta Stone Phase 1 - C Frontend (C → Runa Translation)

**Goal:** Implement C → Runa HIR translator, enabling translation from C to Runa.

**Foundation:** Builds on Runa HIR from v0.8.0 (already human-readable, triple syntax ready).

## What Belongs Where:

### COMPILER (Language Frontend):
- ❌ **C Parser** (src/rosetta/frontends/c/c_parser.runa)
  - Parse C syntax (functions, structs, pointers, control flow)
  - Build C AST (Abstract Syntax Tree)
  - Support subset of C initially

- ❌ **C Semantic Analyzer** (src/rosetta/frontends/c/c_semantic.runa)
  - Extract C semantics (types, scopes, lifetime)
  - Resolve declarations and references
  - Type checking

- ❌ **C → HIR Translator** (src/rosetta/frontends/c/c_to_hir.runa)
  - Map C AST to Runa HIR
  - Preserve C semantics in HIR metadata
  - Map C types to Runa types

  **Example Translation:**
  ```c
  // C input:
  int factorial(int n) {
      if (n <= 1) return 1;
      return n * factorial(n - 1);
  }

  // Runa HIR output (--canon):
  Process called "factorial" takes n as Integer returns Integer:
      If n is less than or equal to 1:
          Return 1
      End If
      Return n times factorial(n minus 1)
  End Process
  ```

- ❌ **Compiler Flag: `--from`**
  ```bash
  # Translate C to Runa canonical
  runac --from=c legacy.c --to=canon -o legacy.runa

  # Translate C to Runa viewer mode (natural language docs)
  runac --from=c legacy.c --to=viewer -o legacy_docs.txt

  # Translate C to Runa developer mode
  runac --from=c legacy.c --to=developer -o legacy.dev.runa
  ```

### Supported C Features (Initial):
- ✅ Functions and function calls
- ✅ Basic types (int, float, char, void)
- ✅ Pointers and arrays
- ✅ Structs (map to Runa types)
- ✅ Control flow (if, while, for)
- ✅ Operators (arithmetic, logical, bitwise)
- ✅ Standard library calls (printf → Display, malloc → memory management)

### NOT Supported (v1.1):
- ❌ Preprocessor macros (future)
- ❌ Unions (future)
- ❌ Complex pointer arithmetic (future)
- ❌ Inline assembly (future)

## Success Criteria:
- ✅ Can translate simple C programs to Runa
- ✅ Generated Runa code compiles and runs correctly
- ✅ Preserves C semantics (pointers, memory management)
- ✅ Output is idiomatic Runa
- ✅ Can translate 80% of typical C programs

## Timeline: 6-8 weeks

---

# 🔹 v1.2: Rosetta Stone Phase 2 - Python Backend (Runa → Python Translation)

**Goal:** Implement Runa HIR → Python translator, enabling translation from Runa to Python.

**Foundation:** Uses Runa HIR from v0.8.0 as source.

## What Belongs Where:

### COMPILER (Language Backend):
- ❌ **HIR → Python Generator** (src/rosetta/backends/python/hir_to_python.runa)
  - Generate idiomatic Python code from Runa HIR
  - Add type hints (Python 3.9+)
  - Use Pythonic patterns (list comprehensions, etc.)

- ❌ **Python Type Mapper** (src/rosetta/backends/python/python_types.runa)
  - Map Runa types to Python type hints
  - Integer → int, String → str, List → list[T]

- ❌ **Python Idioms** (src/rosetta/backends/python/python_idioms.runa)
  - Generate idiomatic Python (not literal translations)
  - Use list comprehensions where appropriate
  - Use Python naming conventions (snake_case)

  **Example Translation:**
  ```runa
  # Runa HIR input (--canon):
  Process called "factorial" takes n as Integer returns Integer:
      If n is less than or equal to 1:
          Return 1
      End If
      Return n times factorial(n minus 1)
  End Process

  # Python output:
  def factorial(n: int) -> int:
      """Calculate factorial of n."""
      if n <= 1:
          return 1
      return n * factorial(n - 1)
  ```

- ❌ **Compiler Flag: `--to=python`**
  ```bash
  # Translate Runa to Python
  runac --from=canon program.runa --to=python -o program.py

  # Translate C → Runa → Python (full pipeline)
  runac --from=c legacy.c --to=python -o modernized.py
  ```

## Success Criteria:
- ✅ Generates working Python code from Runa HIR
- ✅ Python code is idiomatic (uses list comprehensions, etc.)
- ✅ Includes type hints
- ✅ Handles Runa types → Python types correctly
- ✅ C → Runa → Python pipeline works end-to-end

## Timeline: 4-6 weeks

---

# 🔹 v1.3: Rosetta Stone Phase 3 - Bidirectional Translation & Additional Languages

**Goal:** Complete bidirectional C ↔ Runa ↔ Python translation, add Python frontend, begin work on additional languages.

## What Belongs Where:

### COMPILER (Additional Frontends):
- ❌ **Python Parser** (src/rosetta/frontends/python/)
  - Parse Python syntax
  - Build Python AST
  - Handle dynamic typing

- ❌ **Python → HIR Translator** (src/rosetta/frontends/python/python_to_hir.runa)
  - Map Python AST to Runa HIR
  - Preserve dynamic typing semantics in metadata
  - Handle Python-specific features (duck typing, generators, etc.)

  **Example: Preserving Dynamic Typing**
  ```python
  # Python input:
  def process(data):
      if isinstance(data, int):
          return data * 2
      elif isinstance(data, str):
          return data.upper()
      return None

  # Runa HIR (preserves dynamic semantics):
  Type called "DynamicValue":
      type_tag as String
      value as Pointer
  End Type

  Process called "process" takes data as DynamicValue returns DynamicValue:
      If data.type_tag is equal to "Integer":
          Let value be cast_to_integer(data.value)
          Return DynamicValue with type_tag "Integer" and value times 2
      Otherwise If data.type_tag is equal to "String":
          Return DynamicValue with type_tag "String" and string_to_upper(value)
      Otherwise:
          Return DynamicValue with type_tag "None"
      End If
  End Process
  ```

### COMPILER (Additional Backends):
- ❌ **HIR → C Generator** (src/rosetta/backends/c/hir_to_c.runa)
  - Generate C code from Runa HIR
  - Handle memory management (malloc/free)
  - Add ownership comments

  **Example Translation:**
  ```runa
  # Runa HIR input:
  Process called "factorial" takes n as Integer returns Integer:
      If n is less than or equal to 1:
          Return 1
      End If
      Return n times factorial(n minus 1)
  End Process

  # C output:
  /* Generated from Runa */
  int factorial(int n) {
      if (n <= 1) {
          return 1;
      }
      return n * factorial(n - 1);
  }
  ```

### Cross-Language Workflows:

**1. Modernize Legacy C to Python:**
```bash
# C → Runa HIR → Python
runac --from=c old_system.c --to=python -o new_system.py
```

**2. Port Python to C for Performance:**
```bash
# Python → Runa HIR → C
runac --from=python script.py --to=c -o optimized.c
```

**3. Understand Legacy Code:**
```bash
# C → Natural language documentation
runac --from=c complex_system.c --to=viewer -o documentation.txt
```

**4. Cross-Language Refactoring:**
```bash
# Write once in Runa, generate for multiple languages
runac algorithm.runa --to=python -o algorithm.py
runac algorithm.runa --to=c -o algorithm.c
runac algorithm.runa --to=rust -o algorithm.rs  # future
```

### Future Languages (v1.4+):
**Priority Order:**
1. **Rust** (v1.4) - Modern systems language, ownership model
2. **JavaScript** (v1.5) - Web development, dynamic typing
3. **Java** (v1.6) - Enterprise, OOP patterns
4. **Go** (v1.7) - Cloud native, concurrency

## Why Runa as Rosetta Stone Works:

| Feature | LLVM IR | Runa HIR |
|---------|---------|----------|
| **Human Readable** | ❌ SSA, registers, basic blocks | ✅ Valid Runa code |
| **Bidirectional** | ❌ One-way only | ✅ Two-way with semantics |
| **Preserves Semantics** | ❌ Low-level only | ✅ High-level concepts |
| **Multiple Views** | ❌ Single IR form | ✅ Triple syntax |
| **Natural Language** | ❌ Not possible | ✅ --viewer mode |
| **Writeable** | ❌ Too complex | ✅ --canon, --developer |

**LLVM can't be a Rosetta Stone because:**
- Unreadable (SSA, basic blocks, registers)
- One-way translation only (source → LLVM → native)
- Loses high-level semantics
- Not human-writeable

**Runa HIR is perfect because:**
- Human-readable (valid Runa code)
- Bidirectional (language ↔ HIR ↔ language)
- Preserves high-level semantics
- Triple syntax (--canon, --viewer, --developer)

## Success Criteria:
- ✅ C → Runa → Python pipeline works
- ✅ Python → Runa → C pipeline works
- ✅ Round-trip translation preserves behavior
- ✅ 100+ test programs successfully translated
- ✅ Real-world code examples working

## Timeline: 6-8 weeks

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
| **v0.9.0** | 4 weeks | 100 weeks | Cross-compilation: Target abstraction |
| **v0.9.1** | 6 weeks | 106 weeks | Cross-compilation: Windows support |
| **v0.9.2** | 6 weeks | 112 weeks | Cross-compilation: macOS support (x86-64 + ARM64) |
| **v0.9.3** | 4 weeks | 116 weeks | Cross-compilation: ARM64 Linux |
| **v0.9.4** | 5 weeks | 121 weeks | Cross-compilation: WebAssembly |
| **v0.9.5** | 6 weeks | 127 weeks | Package manager & distribution |
| **v0.9.6** | 8 weeks | 135 weeks | IDE tooling (LSP, Debugger, Profiler) |
| **v0.9.7** | 4 weeks | 139 weeks | AI Annotation system |
| **v1.0.0** | 12 weeks | **151 weeks** | Production polish, launch |
| **v1.1** | 8 weeks | 159 weeks | Rosetta Stone: C → Runa translation |
| **v1.2** | 6 weeks | 165 weeks | Rosetta Stone: Runa → Python translation |
| **v1.3** | 8 weeks | **173 weeks** | Rosetta Stone: Bidirectional C ↔ Runa ↔ Python |

**Total Development Time to v1.0:** ~151 weeks (2.9 years)
**Total Development Time to v1.3 (Rosetta Stone):** ~173 weeks (3.3 years)

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

# 🎯 Priority Adjustments & Feature Dependencies

## Language Completeness Analysis

**Current Status (v0.0.7.6):** ~30% of language specification implemented

### Core Features Present ✅
- Variables, functions, control flow
- Basic types, structs, arrays
- Imports, inline assembly
- Bitwise operators, compound assignment
- Comments, string literals

### Critical Missing Features ❌ (Blocks Natural Code)
1. **Struct construction & field access** (`Let p be a value of type Point with x as 10`, `the x of p`)
2. **Collection literals** (`list containing 1, 2, 3`, `dictionary with "key" as value`)
3. **For each loops** (`For each item in items`)
4. **Pattern matching** (`Match value: When pattern: ...`)
5. **ADT/Variant construction** (`Shape.Circle with radius as 5.0`)
6. **Lambda expressions** (`lambda x: x multiplied by 2`)
7. **Type inference** (`Let x be 42` auto-infers Integer)

### High Priority Features ⚠️ (Needed for Stdlib)
8. **Error handling** (`Try/Catch/Finally`)
9. **Generics** (`Process[T]`, `List[T]`)
10. **Result types** (`Result[T, E]`)

### Lower Priority Features 📋 (Nice to Have)
- String interpolation, ternary operator
- Async/await, concurrency
- Advanced control structures
- Operator overloading
- Property accessors

## Recommended Timeline Adjustment

**Original plan had Error Handling in v0.3.0 and Generics in v0.6.0.**
**Problem:** Can't write idiomatic stdlib without these features.

**Proposed adjustment:**
- **v0.0.8.1-8.5**: Implement features #1-7 (critical missing features)
- **v0.0.9**: Native toolchain (as planned)
- **v0.1.0-0.2.0**: Basic stdlib WITHOUT generics/error handling (functional but limited)
- **v0.3.0**: Error Handling (Try/Catch, Result types) - MOVED UP IN PRIORITY
- **v0.4.0**: Memory Management (as planned)
- **v0.5.0**: Optimization (as planned)
- **v0.6.0**: Generics + Advanced Types - CRITICAL FOR STDLIB MATURITY
- **v0.6.1**: Type Inference improvements (as planned)
- **v0.7.0+**: Concurrency, advanced features

**Key insight:** Stdlib development will happen in two phases:
1. **v0.1.0-0.2.0**: Basic stdlib with manual types (before generics)
2. **v0.6.0+**: Mature stdlib with generic collections (after generics)

## Feature Dependency Graph

```
v0.0.8 (Base Language)
    ↓
v0.0.8.1 (Struct Syntax) ← CRITICAL - Everything depends on this
    ↓
v0.0.8.2 (Collections + For Each) ← HIGH - Stdlib needs collections
    ↓
v0.0.8.3 (Pattern Matching + ADTs) ← HIGH - Type system completeness
    ↓
v0.0.8.4 (Lambdas + Inference) ← MEDIUM - Functional patterns
    ↓
v0.1.0 (Basic Stdlib) ← Can start here, but limited without generics
    ↓
v0.3.0 (Error Handling) ← Stdlib needs this for production use
    ↓
v0.6.0 (Generics) ← Stdlib becomes mature here
    ↓
v1.0.0 (Production Release)
```

## Summary

**To reach v0.1.0 (Minimum Viable Stdlib):**
- Must complete: v0.0.8.1, v0.0.8.2, v0.0.8.3, v0.0.8.4
- Should complete: v0.0.8.5 (nice to have)
- Can defer: Error handling and generics (will retrofit stdlib later)

**To reach v1.0.0 (Production Ready):**
- Must complete: Everything through v0.6.0 (generics)
- Stdlib will need significant refactoring when generics arrive


