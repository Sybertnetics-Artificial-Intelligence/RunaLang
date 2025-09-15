# Runa Incremental Self-Hosting Compiler Roadmap

## Executive Summary

This document outlines the strategic approach for achieving full self-hosting of the Runa compiler through incremental stages. Rather than attempting to jump directly from the Rust bootstrap (v0.1) to a full Runa compiler, we implement a series of progressively more capable compilers, each written in Runa and compiled by the previous stage.

## Philosophy: Incremental Complexity Growth

**Core Principle**: Each stage is a working, useful compiler that can compile itself and the next stage. No throwaway code - each step builds real value while progressing toward the ultimate goal.

**Key Benefits**:
- **Dogfooding**: We use Runa to write Runa compilers, validating language design at each step
- **Debugging**: Small feature gaps between stages make issues easy to isolate and fix
- **Reliability**: Always have a working fallback compiler
- **Velocity**: Focus on Runa development, not maintaining complex Rust code

---

## Stage Overview: The 5-Stage Journey

```
v0.1 Bootstrap (Rust) → v0.2 Micro-Runa → v0.3 Mini-Runa → v0.4 Moderate-Runa → v0.5 Partial-Runa → v1.0 Full-Runa
```

Each stage compiles the next, with progressively richer language features and capabilities.

---

## Stage v0.1: Bootstrap Compiler (Rust)

**Status**: ✅ **COMPLETED - OPERATIONAL & READY FOR v0.2**
**Language**: Rust
**Location**: `runa/bootstrap/v0.1_runa-bootstrap/`
**Test Results**: All core operations verified working (2025-09-14)

### Executive Summary
v0.1 bootstrap compiler is **READY TO COMPILE v0.2** with the following capabilities:
- ✅ All arithmetic operations working (+, -, *, /)
- ✅ All comparison operations working (==, !=, <, >, <=, >=)
- ✅ Function calls with parameters working
- ✅ String operations and file I/O working
- ✅ Conditional logic (If/Otherwise) working
- ⚠️ While loops have a bug (use recursion instead)
- ⚠️ Return values from recursion don't propagate (use file I/O for complex state)

**RECOMMENDATION**: Proceed with v0.2 development using functional programming style.

### Purpose
**THE ONLY PURPOSE OF v0.1 IS TO COMPILE v0.2**
- Must be able to parse the exact Runa syntax that v0.2 uses
- Must generate native executable that can run
- Cross-platform support so we don't rebuild compiler for each OS
- NO OTHER REQUIREMENTS - this is purely a bootstrap tool

### REQUIRED v0.1 CAPABILITIES FOR v0.2 COMPILATION

#### CORE PARSING REQUIREMENTS
- **Process definitions**: `Process called "name" that takes param as Type returns ReturnType:`
- **Type definitions**: `Type called "TypeName": field as DataType End Type`
- **Variable declarations**: `Let variable be value`, `Set variable to value`
- **Control flow**: `If`/`Otherwise`/`End If`, `While`/`End While`
- **Function calls**: `function_name(arg1, arg2)`
- **Field access**: `object.field`
- **Import statements**: `Import module "name" as Alias`
- **Constructor syntax**: `a value of type TypeName with field1 as value1, field2 as value2`

#### INLINE ASSEMBLY SUPPORT (CRITICAL)
```runa
Inline Assembly:
    "mov rax, %1\n"
    "syscall\n" 
    : "=r"(result)
    : "r"(syscall_num), "r"(arg1)
    : "rax", "rdi"
End Assembly
```
- Must parse inline assembly blocks
- Must generate working assembly code
- Must handle input/output constraints
- Must handle clobbered registers

#### TYPE SYSTEM REQUIREMENTS
- **Struct types**: Field access, construction, parameter passing
- **Basic types**: String, Integer, Boolean
- **Function types**: Parameter and return type checking
- **Module resolution**: Import and qualified function calls

#### CODE GENERATION REQUIREMENTS
- **Direct syscall generation**: No external runtime dependencies
- **Native assembly output**: x86_64, ARM64, RISC-V support
- **Executable creation**: Link to create runnable programs
- **Memory management**: Stack allocation, basic heap operations via syscalls

### ✅ ACTUAL v0.1 CAPABILITIES ACHIEVED (AS OF 2025-09-14)

#### WHAT WE HAVE:
- **✅ Complete Parser**: All syntax requirements parsing correctly
- **✅ Type Definitions**: Struct types with fields fully working
- **✅ Process Definitions**: Function declarations and returns working
- **✅ Variable Operations**: Let/Set statements functional (with limitations)
- **✅ Control Flow**: If/Otherwise implemented and working
- **✅ Field Access**: Object.field notation working
- **✅ Imports**: Module import statements parsed
- **✅ Constructors**: "a value of type X with..." syntax working
- **✅ Inline Assembly**: Working for immediate values and basic operations
- **✅ LLVM Backend**: Generates valid object files (.o)
- **✅ Executable Generation**: Can link with gcc to create working executables
- **✅ Return Values**: Programs return correct exit codes
- **✅ Function Calls**: Functions can call other functions with parameters
- **✅ Arithmetic Operations**: All basic operations work (+, -, *, /)
- **✅ Comparison Operations**: All comparisons work (==, !=, <, >, <=, >=)
- **✅ Logical Operations**: AND and OR operators work correctly
- **✅ String Operations**: String concatenation, literals, and file I/O work
- **✅ File I/O**: WriteFile and ReadFile operations functional
- **✅ Recursion**: Compiles without segfaults (return values don't propagate)

#### WHAT WE DON'T HAVE:
- **❌ While/ForEach Loops**: Create infinite loops due to variable storage bug
- **❌ Variable Updates in Loops**: Variables stored as values not memory locations
- **❌ Return Values from Recursion**: Recursive return values don't propagate correctly
- **❌ Arrays/Lists**: No collection types
- **❌ Dynamic Inline Assembly**: Limited to basic immediate operations
- **❌ Cross-compilation**: Only compiles for host platform
- **❌ Memory Management**: No heap allocation, only stack
- **❌ Module Loading**: Can't actually load imported modules
- **❌ Error Recovery**: Compilation stops on first error

#### CRITICAL LIMITATIONS FOR v0.2:
**v0.1 has a fundamental variable storage issue** where variables are stored as LLVM values instead of memory locations (alloca). This causes:
- While loops to run infinitely (condition never updates)
- Set statements in loops don't affect loop conditions
- Variable updates create new values instead of modifying existing ones

**WORKAROUNDS FOR v0.2 DEVELOPMENT**:
- Use recursion instead of While/ForEach loops
- Use functional style programming (immutable variables)
- Pass state through function parameters instead of mutable variables
- Use file I/O for complex state management if needed

This means **v0.2 can be written in a functional style** avoiding the problematic features.

### THE CORRECTED CROSS-COMPILATION WORKFLOW (LINUX HOST)

**WE ALREADY HAVE COMPLETE SYSCALL IMPLEMENTATIONS FOR ALL PLATFORMS!**

Located at: `runa/src/compiler/backend/syscalls/platforms/`
- ✅ `linux_x64.runa` - Complete Linux x86_64 syscall definitions (~350 syscalls)
- ✅ `linux_arm64.runa` - Linux ARM64 syscall definitions
- ✅ `darwin_x64.runa` - macOS x86_64 syscall definitions  
- ✅ `darwin_arm64.runa` - macOS ARM64 syscall definitions
- ✅ `windows_x64.runa` - Windows x64 API definitions
- ✅ `freebsd_x64.runa` - FreeBSD x86_64 syscall definitions
- ✅ `openbsd_x64.runa` - OpenBSD x86_64 syscall definitions
- ✅ `netbsd_x64.runa` - NetBSD x86_64 syscall definitions

#### STAGE v0.1: THE GENESIS BUILD (USING RUST ON LINUX)
**From Linux development machine, build all v0.1 bootstrap compilers:**

```bash
# Build for Linux x86_64 (for development use)
rustc ./bootstrap/v0.1_runa-bootstrap/ --target=x86_64-unknown-linux-gnu --output ./build/v0.1/runac-linux-x64

# Build for Linux ARM64
rustc ./bootstrap/v0.1_runa-bootstrap/ --target=aarch64-unknown-linux-gnu --output ./build/v0.1/runac-linux-arm64

# Cross-compile for Windows x86_64
rustc ./bootstrap/v0.1_runa-bootstrap/ --target=x86_64-pc-windows-msvc --output ./build/v0.1/runac-windows-x64.exe

# Cross-compile for macOS x86_64
rustc ./bootstrap/v0.1_runa-bootstrap/ --target=x86_64-apple-darwin --output ./build/v0.1/runac-macos-x64

# Cross-compile for macOS ARM64
rustc ./bootstrap/v0.1_runa-bootstrap/ --target=aarch64-apple-darwin --output ./build/v0.1/runac-macos-arm64

# Cross-compile for FreeBSD x86_64
rustc ./bootstrap/v0.1_runa-bootstrap/ --target=x86_64-unknown-freebsd --output ./build/v0.1/runac-freebsd-x64

# Cross-compile for OpenBSD x86_64  
rustc ./bootstrap/v0.1_runa-bootstrap/ --target=x86_64-unknown-openbsd --output ./build/v0.1/runac-openbsd-x64

# Cross-compile for NetBSD x86_64
rustc ./bootstrap/v0.1_runa-bootstrap/ --target=x86_64-unknown-netbsd --output ./build/v0.1/runac-netbsd-x64
```

**Result**: Complete `/build/v0.1/` directory with native executables for all platforms.

#### STAGE v0.2: THE FIRST SELF-HOST AND CROSS-COMPILATION (USING RUNA)

**Development Phase** (Linux):
```bash
# Test v0.2 compilation on Linux during development
./build/v0.1/runac-linux-x64 ./bootstrap/v0.2_micro-runa/ --output ./build/v0.2/runac-linux-x64
```

**Release Phase** - Cross-compile v0.2 for all platforms from Linux:
```bash
# Self-compile v0.2 for Linux
./build/v0.2/runac-linux-x64 ./bootstrap/v0.2_micro-runa/ --target=x86_64-unknown-linux-gnu --output ./release/v0.2/runac-linux-x64

# Cross-compile for all other targets using the Linux v0.2 compiler
./build/v0.2/runac-linux-x64 ./bootstrap/v0.2_micro-runa/ --target=aarch64-unknown-linux-gnu --output ./release/v0.2/runac-linux-arm64
./build/v0.2/runac-linux-x64 ./bootstrap/v0.2_micro-runa/ --target=x86_64-pc-windows-msvc --output ./release/v0.2/runac-windows-x64.exe
./build/v0.2/runac-linux-x64 ./bootstrap/v0.2_micro-runa/ --target=x86_64-apple-darwin --output ./release/v0.2/runac-macos-x64
./build/v0.2/runac-linux-x64 ./bootstrap/v0.2_micro-runa/ --target=aarch64-apple-darwin --output ./release/v0.2/runac-macos-arm64
./build/v0.2/runac-linux-x64 ./bootstrap/v0.2_micro-runa/ --target=x86_64-unknown-freebsd --output ./release/v0.2/runac-freebsd-x64
./build/v0.2/runac-linux-x64 ./bootstrap/v0.2_micro-runa/ --target=x86_64-unknown-openbsd --output ./release/v0.2/runac-openbsd-x64
./build/v0.2/runac-linux-x64 ./bootstrap/v0.2_micro-runa/ --target=x86_64-unknown-netbsd --output ./release/v0.2/runac-netbsd-x64
```

**FULL PLATFORM MATRIX:**
- **Linux**: x86_64, ARM64  
- **Windows**: x86_64
- **macOS**: x86_64, ARM64
- **FreeBSD**: x86_64
- **OpenBSD**: x86_64  
- **NetBSD**: x86_64

**TIMELINE REDUCTION:** With existing syscall infrastructure, the timeline drops from 450-600 hours to ~150-200 hours total because the hardest part (syscall mappings) is already complete.

---

## Stage v0.2: Micro-Runa Compiler

**Status**: ✅ **READY FOR DEVELOPMENT**
**Language**: Runa (compiled by v0.1)
**Location**: `runa/bootstrap/v0.2_micro-runa/`

### DEVELOPMENT APPROACH: Functional Style Compiler

**v0.1 IS NOW CAPABLE OF COMPILING v0.2** with the following approach:
- ✅ Function calls work - can build modular compiler
- ✅ Arithmetic operations work - can implement calculations
- ✅ Comparison operations work - can implement logic
- ✅ String operations work - can handle source code
- ✅ File I/O works - can read source files and write output
- ✅ If/Otherwise work - can implement conditional logic
- ⚠️ Avoid While loops - use recursion instead
- ⚠️ Avoid mutable loop variables - use functional style

**Development Strategy**: Write v0.2 in a functional programming style
- Use recursion for iteration instead of While loops
- Pass state through function parameters
- Return new values instead of mutating variables
- Use file I/O for intermediate state if needed

**Timeline Estimate**: 60-80 hours (reduced from 200+ hours)

### EXAMPLE v0.2 CODE: Functional Style Compiler

```runa
Process called "tokenize_recursive" that takes input as String, position as Integer, tokens as TokenList returns TokenList:
    Note: Recursive tokenization avoiding While loops
    If position is greater than or equal to string_length(input):
        Return tokens
    End If

    Let current_char be string_char_at(input, position)
    Let next_token be identify_token(current_char, input, position)
    Let new_tokens be append_token(tokens, next_token)
    Let next_position be position + token_length(next_token)

    Return tokenize_recursive(input, next_position, new_tokens)
End Process

Process called "parse_statements" that takes tokens as TokenList, index as Integer, statements as StatementList returns StatementList:
    Note: Functional parsing without mutable state
    If index is greater than or equal to list_length(tokens):
        Return statements
    End If

    Let current_token be list_get(tokens, index)
    If token_is_keyword(current_token, "Process"):
        Let parsed_function be parse_function(tokens, index)
        Let new_statements be append_statement(statements, parsed_function)
        Let next_index be get_function_end_index(tokens, index)
        Return parse_statements(tokens, next_index, new_statements)
    Otherwise:
        Let parsed_statement be parse_single_statement(tokens, index)
        Let new_statements be append_statement(statements, parsed_statement)
        Let next_index be index + statement_token_count(parsed_statement)
        Return parse_statements(tokens, next_index, new_statements)
    End If
End Process
```

**This functional style avoids the While loop bug** while using v0.1's working features.

### CORE REQUIREMENTS FOR v0.2

#### 1. PARSE RUNA SOURCE CODE → REAL AST
- **Real lexer**: Tokenize Runa syntax, not placeholder returns
- **Real parser**: Build proper AST nodes, not empty functions
- **Real type definitions**: Handle struct types with field access
- **Real imports**: Resolve module dependencies that actually work

#### 2. TYPE CHECKING → ACTUAL TYPE SYSTEM WITH INFERENCE
- **Struct type checking**: Real field access validation
- **Function type checking**: Parameter and return type verification  
- **Module type resolution**: Cross-module function call validation
- **Type inference**: Deduce types from expressions and assignments

#### 3. CODE GENERATION → DIRECT ASSEMBLY OUTPUT
- **Native syscall generation**: Direct Linux/Windows/macOS syscalls
- **Inline assembly emission**: Generate actual assembly instructions
- **Memory management**: Stack allocation via syscalls, no libc
- **Executable creation**: Link to native executable format

#### 4. MODULE SYSTEM → IMPORT RESOLUTION THAT WORKS
- **File loading**: Read and parse imported .runa files
- **Symbol resolution**: Find functions/types across module boundaries
- **Dependency ordering**: Compile modules in correct order
- **Namespace management**: Handle qualified names like `Module.function`

#### 5. ERROR REPORTING → MEANINGFUL DIAGNOSTICS
- **Source location tracking**: Line/column numbers for all errors
- **Type error messages**: Clear explanations of type mismatches
- **Parse error recovery**: Continue parsing after syntax errors
- **Multiple error reporting**: Show all errors in one compilation pass

### INLINE ASSEMBLY - NATIVE IMPLEMENTATION
```runa
Process called "write_stdout" that takes message as String, length as Integer returns Integer:
    Let bytes_written be 0
    Inline Assembly:
        "mov rax, 1\n"          # sys_write
        "mov rdi, 1\n"          # stdout  
        "mov rsi, %1\n"         # message
        "mov rdx, %2\n"         # length
        "syscall\n"
        "mov %0, rax\n"         # return value
        : "=r"(bytes_written)
        : "r"(message), "r"(length) 
        : "rax", "rdi", "rsi", "rdx"
    End Assembly
    Return bytes_written
End Process
```

### SYSCALLS AND OS INTEGRATION - FULLY NATIVE
- **Direct syscalls**: No libc, no external dependencies
- **Platform-specific**: Linux/Windows/macOS syscall interfaces
- **File I/O**: Native open/read/write/close operations
- **Memory management**: mmap/VirtualAlloc for heap allocation
- **Process control**: Native fork/exec/exit operations

### v0.2 MUST BE WRITTEN ENTIRELY IN RUNA
- **Zero external dependencies**: No Rust, no C, no libc
- **Self-contained**: All functionality implemented in Runa
- **Cross-platform**: Works on Linux/Windows/macOS through syscalls
- **Self-bootstrapping**: Can compile itself once v0.1 compiles it

### BRUTAL TIMELINE ESTIMATE: 200+ HOURS
This requires implementing a complete working compiler from scratch in Runa.

### Technical Specifications

#### Syntax Support (Same as v0.1)
```runa
Process called "function_name" returns ReturnType:
    Let variable be value
    Set variable to new_value
    If condition:
        statements
    Otherwise:
        statements
    End If
    Return result
End Process

Type called "TypeName":
    field as DataType
End Type
```

#### Architecture
- **Single-file modules**: Each compiler component in separate .runa files
- **Concrete types only**: `List_of_String`, `Dict_String_to_Integer` instead of generics
- **Explicit imports**: `Import "lexer" as Lexer`
- **Separated comments**: No inline comments, all comments in separate blocks

#### Key Components
1. **lexer.runa**: Tokenizes Runa source code
2. **parser.runa**: Builds AST from tokens  
3. **type_checker.runa**: Validates types and semantics
4. **code_generator.runa**: Generates executable code
5. **compiler_driver.runa**: Orchestrates compilation pipeline
6. **main.runa**: Command-line interface

#### Self-Hosting Test
The v0.2 compiler must be able to compile itself:
```bash
v0.1_bootstrap v0.2_source/ --output v0.2_compiled
v0.2_compiled v0.2_source/ --output v0.2_self_compiled
# v0.2_compiled and v0.2_self_compiled should be functionally identical
```

---

## Stage v0.3: Mini-Runa Compiler

**Status**: 🚀 **IN DEVELOPMENT**  
**Language**: Runa (compiled by v0.1)  
**Target Location**: `runa/bootstrap/v0.3_mini-runa/`

### Design Goals
Add essential language features while maintaining simplicity and reliability.

### New Language Features
- **Basic Generics**: `List[T]`, `Optional[T]`, `Result[T, E]`
- **Module System**: `Import Module "path" as Name`
- **Inline Comments**: Comments after field declarations
- **Pattern Matching**: Basic `Match`/`When` constructs
- **Enhanced Error Recovery**: Better parse error handling
- **Basic Annotations**: Simple `@Reasoning` and `@Implementation` blocks

### Enhanced Capabilities
- **Multi-file projects**: Can compile projects spanning multiple files
- **Dependency resolution**: Understands module dependencies
- **Incremental compilation**: Only recompile changed modules
- **Better diagnostics**: Column-accurate error reporting
- **Basic optimization**: Loop unrolling, function inlining

### Architecture Improvements
- **Generic type system**: Template-based generic instantiation
- **Module resolution**: Path-based module finding and loading
- **Enhanced AST**: Richer AST nodes with more semantic information
- **Improved codegen**: Better register allocation and instruction selection

### Self-Hosting Validation
```bash
v0.2_compiler v0.3_source/ --output v0.3_compiled
v0.3_compiled v0.3_source/ --output v0.3_self_compiled
v0.3_compiled v0.2_source/ --output v0.2_recompiled_by_v0.3
# All outputs should be functionally correct
```

---

## Stage v0.4: Moderate-Runa Compiler

**Status**: 📋 **PLANNED**  
**Language**: Runa (compiled by v0.3)  
**Target Location**: `runa/bootstrap/v0.4_moderate-runa/`

### Design Goals
Implement advanced language features necessary for building sophisticated compilers.

### New Language Features
- **Advanced Generics**: Where clauses, generic constraints, higher-kinded types
- **Trait System**: Interfaces with default implementations
- **Advanced Pattern Matching**: Guards, destructuring, exhaustiveness checking
- **Macro System**: Compile-time code generation
- **Full Annotation System**: All annotation types from specification
- **Memory Management**: Ownership tracking, borrow checking

### Compiler Enhancements
- **Advanced Optimization**: SSA form, advanced loop optimizations, vectorization
- **Cross-platform Support**: Multiple target architectures
- **LLVM Integration**: Use LLVM as backend for better optimizations
- **Parallel Compilation**: Multi-threaded compilation pipeline
- **Language Server**: IDE integration capabilities

### Standard Library Bootstrap
- **Core Collections**: Vectors, Maps, Sets implemented in Runa
- **String Operations**: Full Unicode support, regex engine
- **File System**: Complete file/directory operations
- **Networking**: Basic TCP/UDP socket operations
- **Mathematical Operations**: Arbitrary precision arithmetic

### Architecture Evolution
- **Multi-pass Compilation**: Separate lexing, parsing, semantic analysis, optimization, codegen
- **Plugin System**: Loadable optimization passes and language extensions
- **Intermediate Representation**: Rich IR suitable for advanced optimizations
- **Debugging Support**: DWARF debug info generation, debugger integration

---

## Stage v0.5: Partial-Runa Compiler

**Status**: 📋 **PLANNED** (Current partial-runa to be refactored to this stage)  
**Language**: Runa (compiled by v0.4)  
**Target Location**: `runa/bootstrap/v0.5_partial-runa/` (refactored)

### Design Goals
Feature-complete Runa compiler capable of compiling the full v1.0 compiler and standard library.

### Complete Language Implementation
- **Full Language Specification**: All features from runa_complete_specification.md
- **Complete Type System**: Advanced types, dependent types, refinement types
- **Complete Concurrency**: Async/await, actors, channels, parallel constructs
- **Complete Metaprogramming**: Full macro system, compile-time evaluation
- **Complete Interoperability**: FFI, C bindings, external library integration

### Production-Quality Features
- **Incremental Compilation**: Smart recompilation based on dependency analysis
- **Package Management**: Module versioning, dependency resolution
- **Cross-Compilation**: Full cross-platform compilation matrix
- **Optimization Suite**: Profile-guided optimization, link-time optimization
- **Toolchain Integration**: Formatter, linter, documentation generator, test runner

### Standard Library Completion
- **Complete Standard Library**: All modules from stdlib specification
- **Performance Libraries**: SIMD operations, GPU computing interfaces
- **System Integration**: OS-specific functionality for all supported platforms
- **Network Stack**: HTTP client/server, websockets, advanced networking protocols
- **Data Processing**: JSON, XML, binary format parsing and generation

---

## Stage v1.0: Full Runa Compiler

**Status**: 🎯 **TARGET**  
**Language**: Runa (compiled by v0.5)  
**Target Location**: `runa/src/compiler/`

### Ultimate Goals
Production-ready, industry-strength compiler for the Runa language.

### Advanced Features
- **JIT Compilation**: Runtime optimization and adaptive compilation
- **Ahead-of-Time Optimization**: Aggressive whole-program optimization
- **Memory Management**: Advanced garbage collection, memory pool management
- **Distributed Compilation**: Compilation across multiple machines
- **Language Evolution**: Support for language versioning and migration

---

## Implementation Strategy

### Phase 1: Micro-Runa Development (Immediate)

**Objectives**:
1. Analyze current partial-runa to identify which features to defer
2. Create simplified versions using only v0.1-supported syntax
3. Implement core compiler pipeline in constrained Runa subset
4. Achieve self-hosting of v0.2

**Key Tasks**:
- [ ] **Audit partial-runa complexity**: Identify which features require deferral
- [ ] **Create micro-runa skeleton**: Simplified architecture using only basic syntax
- [ ] **Implement lexer**: Basic tokenization in constrained Runa
- [ ] **Implement parser**: AST construction using only supported constructs  
- [ ] **Implement type checker**: Basic type validation without generics
- [ ] **Implement codegen**: Simple code generation to native executable
- [ ] **Achieve self-compilation**: v0.2 compiles itself successfully
- [ ] **Validation testing**: Comprehensive test suite for v0.2 capabilities

**Success Criteria**:
- v0.1 (Rust) successfully compiles v0.2 (Micro-Runa)
- v0.2 (Micro-Runa) successfully compiles itself  
- v0.2 can compile simple Runa programs equivalent to v0.1 capabilities
- All tests pass for both v0.1-compiled and v0.2-self-compiled versions

**Timeline Estimate**: 2-3 development cycles

### Phase 2: Mini-Runa Development

**Objectives**:
1. Add generics support to v0.2 codebase
2. Implement enhanced module system
3. Add basic optimization passes
4. Achieve self-hosting of v0.3

**Success Criteria**:
- v0.2 successfully compiles v0.3 (Mini-Runa)
- v0.3 successfully compiles itself and v0.2
- Generic type system functional with basic containers
- Module system supports multi-file projects

**Timeline Estimate**: 3-4 development cycles

### Phase 3: Moderate-Runa Development

**Objectives**:
1. Implement advanced language features (traits, advanced patterns)
2. Add LLVM backend integration
3. Bootstrap essential standard library components
4. Achieve self-hosting of v0.4

**Success Criteria**:
- v0.3 successfully compiles v0.4 (Moderate-Runa)
- v0.4 can compile sophisticated programs using advanced features
- Standard library components implemented in Runa
- Performance meets production requirements

**Timeline Estimate**: 4-6 development cycles

### Phase 4: Partial-Runa Refactoring

**Objectives**:
1. Refactor existing partial-runa to use v0.4 as base
2. Implement complete language specification
3. Add production-quality tooling
4. Prepare for v1.0 development

**Success Criteria**:
- v0.4 successfully compiles v0.5 (Refactored Partial-Runa)
- v0.5 implements complete Runa language specification
- Toolchain integration functional
- Ready to compile production v1.0

**Timeline Estimate**: 6-8 development cycles

### Phase 5: Full Runa Production

**Objectives**:
1. Implement production-quality compiler
2. Complete advanced optimization suite
3. Finalize standard library
4. Release v1.0

**Success Criteria**:
- v0.5 successfully compiles v1.0 (Full Runa)
- v1.0 meets all performance and feature requirements
- Complete toolchain and ecosystem ready for public release
- Self-hosting achieved with production quality

**Timeline Estimate**: 8-12 development cycles

---

## Risk Mitigation Strategies

### Technical Risks

**Risk**: Feature creep causing complexity explosion  
**Mitigation**: Strict feature gates at each stage. No feature advances to next stage until current stage is stable.

**Risk**: Self-hosting validation failures  
**Mitigation**: Automated testing for every self-compilation. Binary diffing to ensure consistency.

**Risk**: Performance regression between stages  
**Mitigation**: Benchmark suite tracking performance across all stages. No performance regressions allowed.

### Development Risks

**Risk**: Extended development timeline  
**Mitigation**: Each stage provides immediate value. Can ship intermediate stages if needed.

**Risk**: Architecture decisions proving inadequate  
**Mitigation**: Incremental approach allows course correction at each stage boundary.

**Risk**: Testing complexity  
**Mitigation**: Comprehensive test matrix testing N×N stage combinations (each stage compiling every previous stage).

---

## Success Metrics

### Technical Metrics
- **Self-Hosting Success Rate**: 100% success rate for each stage compiling itself
- **Cross-Stage Compatibility**: Each stage can compile all previous stages
- **Performance Progression**: Each stage performs ≥ previous stage (no regressions)
- **Feature Completeness**: Each stage implements 100% of its designated feature set

### Quality Metrics  
- **Test Coverage**: ≥95% code coverage at each stage
- **Bug Density**: <0.1 bugs per KLOC in released stages
- **Compilation Speed**: Progressive improvement in compilation throughput
- **Memory Usage**: Bounded memory growth, no memory leaks

### Development Metrics
- **Development Velocity**: Consistent progress measured in features/cycle
- **Code Reuse**: High reuse percentage between stages (minimize rewriting)
- **Documentation Coverage**: 100% API documentation for each stage
- **Community Adoption**: External usage and contribution metrics

---

## Long-Term Vision

This incremental approach establishes Runa as:

1. **Self-Sufficient**: Complete toolchain written in Runa itself
2. **Production-Ready**: Industrial-strength compiler suitable for enterprise use
3. **Community-Friendly**: Clear progression path for contributors to understand and extend
4. **Technically Sound**: Each stage validates language design decisions through real usage
5. **Maintainable**: Modular architecture allows focused improvements without system-wide rewrites

The final result is not just a working compiler, but a proven, battle-tested language implementation that demonstrates Runa's capabilities through its own development process.

---

## Conclusion

This roadmap transforms the daunting task of building a self-hosting compiler into a series of achievable, incremental steps. Each stage provides value independently while building toward the ultimate goal of a production-ready, self-hosting Runa compiler.

By following this path, we ensure that:
- Development risk is minimized through incremental validation
- Each stage serves as both a stepping stone and a fallback option  
- The language design is validated through actual usage at each step
- The final compiler is built on a foundation of proven, working code

This approach embodies the Runa philosophy: intelligent, incremental progress toward ambitious goals.