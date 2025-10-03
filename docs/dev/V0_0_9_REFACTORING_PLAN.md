# v0.0.9 Refactoring Plan: Transition to Modular Architecture

## Overview

This document outlines the comprehensive refactoring plan for v0.0.9+ to transform the monolithic v0.0.8 compiler structure into a well-organized, modular architecture based on the `_legacy/src` reference implementation.

**Goals:**
- Split large monolithic files into logical modules
- Establish clear compiler phase boundaries
- Create maintainable, testable architecture
- Support gradual migration from v0.0.9.0 → v0.1.0
- Maintain 3-stage bootstrap capability throughout

---

## Current State: v0.0.8 Structure

```
runa/bootstrap/v0.0.8/
├── src/
│   ├── main.runa          (245 lines)
│   ├── lexer.runa         (1,576 lines) - MONOLITHIC
│   ├── parser.runa        (4,350 lines) - TOO LARGE
│   ├── codegen.runa       (3,490 lines) - MONOLITHIC
│   ├── containers.runa    (1,241 lines)
│   ├── hashtable.runa     (667 lines)
│   └── string_utils.runa  (917 lines)
├── runtime/
│   └── runtime.c          (C runtime)
└── build/
    └── runac              (final compiler)
```

**Total:** 12,486 lines in 7 files

**Issues:**
- `parser.runa` (4,350 lines) - handles parsing, AST construction, all node types
- `codegen.runa` (3,490 lines) - x86-64 code generation, all instruction types
- `lexer.runa` (1,576 lines) - tokenization with no modularity
- No semantic analysis phase
- No IR layers
- Direct AST → x86-64 assembly (no abstraction)
- C runtime dependency

---

## Target State: _legacy/src Architecture

```
_legacy/src/
├── compiler/
│   ├── main.runa
│   ├── driver.runa                    # Compiler driver orchestration
│   │
│   ├── lexer/                         # FRONTEND: Tokenization
│   │   ├── lexer.runa                 # Main lexer implementation
│   │   ├── token.runa                 # Token types and utilities
│   │   ├── diagnostics.runa           # Error reporting
│   │   └── internal/
│   │       ├── definitions.runa       # Keyword/operator definitions
│   │       └── utilities.runa         # Helper functions
│   │
│   ├── parser/                        # FRONTEND: AST Construction
│   │   ├── parser.runa                # Main parser
│   │   └── ast.runa                   # AST node definitions
│   │
│   ├── semantic/                      # SEMANTIC ANALYSIS
│   │   ├── semantic_analyzer.runa     # Main analyzer orchestration
│   │   ├── type_checker.runa          # Type checking
│   │   ├── type_inference.runa        # Type inference
│   │   ├── type_enforcement.runa      # Type enforcement engine
│   │   ├── symbol_table.runa          # Symbol management
│   │   ├── symbol_visitor.runa        # Symbol resolution
│   │   ├── validation.runa            # Semantic validation
│   │   ├── dependency_analyzer.runa   # Dependency analysis
│   │   ├── memory_analyzer.runa       # Memory safety analysis
│   │   ├── diagnostics.runa           # Error reporting
│   │   ├── visitor.runa               # AST visitor pattern
│   │   └── lsp_integration.runa       # LSP support
│   │
│   ├── ir/                            # INTERMEDIATE REPRESENTATION
│   │   ├── ir.runa                    # IR common definitions
│   │   ├── ir_context.runa            # IR compilation context
│   │   │
│   │   ├── hir/                       # High-level IR (close to source)
│   │   │   ├── hir.runa               # HIR node definitions
│   │   │   └── builder.runa           # HIR construction
│   │   │
│   │   ├── mir/                       # Mid-level IR (platform-independent)
│   │   │   ├── mir.runa               # MIR node definitions
│   │   │   ├── builder.runa           # MIR construction
│   │   │   └── verifier.runa          # MIR validation
│   │   │
│   │   ├── lir/                       # Low-level IR (close to machine)
│   │   │   ├── lir.runa               # LIR node definitions
│   │   │   ├── builder.runa           # LIR construction
│   │   │   └── bytecode_generator.runa
│   │   │
│   │   ├── types/                     # IR type system
│   │   │   ├── types.runa             # Type definitions
│   │   │   └── layout.runa            # Memory layout
│   │   │
│   │   └── optimizations/             # Optimization passes
│   │       ├── pass_interface.runa    # Optimization pass interface
│   │       ├── optimization_pipeline.runa
│   │       │
│   │       ├── analysis/              # Analysis passes
│   │       │   ├── control_flow_analysis.runa
│   │       │   ├── data_flow_analysis.runa
│   │       │   └── dependency_tracking.runa
│   │       │
│   │       ├── hir_passes/            # HIR optimizations
│   │       │   ├── inlining.runa
│   │       │   ├── loop_optimization.runa
│   │       │   ├── loop_vectorization.runa
│   │       │   └── advanced_loop_optimizations.runa
│   │       │
│   │       ├── mir_passes/            # MIR optimizations
│   │       │   ├── constant_folding.runa
│   │       │   ├── dead_code_elimination.runa
│   │       │   └── ssa.runa
│   │       │
│   │       ├── lir_passes/            # LIR optimizations
│   │       │   └── register_allocation.runa
│   │       │
│   │       ├── interprocedural/       # Whole-program analysis
│   │       │   └── interprocedural_analysis.runa
│   │       │
│   │       ├── profile_guided/        # PGO
│   │       │   └── profile_guided_optimization.runa
│   │       │
│   │       ├── target_specific/       # Architecture-specific
│   │       │   └── target_specific_optimizations.runa
│   │       │
│   │       └── benchmarking/
│   │           └── performance_benchmark.runa
│   │
│   ├── backends/                      # CODE GENERATION
│   │   ├── x86_64/                    # (v0.0.9 - to be created)
│   │   │   ├── codegen.runa
│   │   │   ├── instruction_selector.runa
│   │   │   └── object_writer.runa     # Native ELF64 writer
│   │   │
│   │   ├── gpu/                       # (v0.3.0+)
│   │   │   ├── gpu_backend.runa
│   │   │   ├── cuda_backend.runa
│   │   │   ├── metal_backend.runa
│   │   │   ├── opencl_backend.runa
│   │   │   ├── gpu_memory.runa
│   │   │   ├── kernel_optimizer.runa
│   │   │   └── parallelization_analyzer.runa
│   │   │
│   │   └── wasm/                      # (v0.3.0+)
│   │       ├── wasm_generator.runa
│   │       ├── wasm_optimizer.runa
│   │       ├── wasm_runtime.runa
│   │       ├── wasi_interface.runa
│   │       └── shared_interfaces.runa
│   │
│   └── lsp/                           # Language Server Protocol (v0.2.0+)
│       ├── main.runa
│       ├── lsp_server.runa
│       ├── lsp_handlers.runa
│       └── lsp_types.runa
│
└── runtime/                           # RUNTIME LIBRARY
    ├── src/
    │   ├── runtime.runa               # Pure Runa runtime (v0.0.9 goal)
    │   │
    │   ├── aott/                      # Adaptive Optimization (v0.4.0+)
    │   │   ├── analysis/
    │   │   ├── compilation/
    │   │   ├── execution/
    │   │   ├── hot_swapping/
    │   │   └── optimization/
    │   │
    │   ├── async/                     # Async runtime (v0.5.0+)
    │   │
    │   ├── ffi/                       # FFI support (v0.1.0+)
    │   │
    │   ├── os/                        # OS abstractions (v0.0.9+)
    │   │   └── system/
    │   │
    │   └── tensor/                    # Tensor operations (v0.7.0+)
    │
    └── runtime.c                      # C runtime (deprecated in v0.0.9)
```

---

## Migration Strategy: Integrated with DEVELOPMENT_ROADMAP.md

**Philosophy:** Refactor the compiler structure while implementing the planned v0.0.9 features from DEVELOPMENT_ROADMAP.md. Each sub-version adds both structural improvements AND new language features.

---

### Phase 1: v0.0.9.0 - Foundation Split + Error Handling (Bootstrap with v0.0.8)

**Goals:**
1. **Refactoring:** Break apart the largest monolithic files
2. **Features:** Implement Result<T,E> and Option<T> types (from roadmap)

**Structural Changes:**

```
runa/bootstrap/v0.0.9/
├── src/
│   ├── main.runa                      # Compiler entry point
│   │
│   ├── frontend/                      # NEW: Frontend modules
│   │   ├── lexer/
│   │   │   ├── lexer.runa             # Split from v0.0.8 lexer.runa
│   │   │   └── token.runa             # Token definitions extracted
│   │   │
│   │   └── parser/
│   │       ├── parser.runa            # Core parser (from v0.0.8)
│   │       └── ast.runa               # AST node definitions (extracted)
│   │
│   ├── backend/                       # NEW: Backend modules
│   │   └── x86_64/
│   │       └── codegen.runa           # From v0.0.8 codegen.runa
│   │
│   ├── utils/                         # Utilities
│   │   ├── containers.runa
│   │   ├── hashtable.runa
│   │   └── string_utils.runa
│   │
│   └── runtime/                       # NEW: Pure Runa runtime begins
│       └── runtime_io.runa            # Initial I/O syscalls in Runa
│
└── runtime/
    └── runtime.c                      # C runtime (still used for most functions)
```

**Split Tasks:**

1. **lexer.runa (1,576 lines) → 2 files:**
   - `frontend/lexer/lexer.runa` (≈1,200 lines) - lexer logic
   - `frontend/lexer/token.runa` (≈376 lines) - token types, utilities

2. **parser.runa (4,350 lines) → 2 files:**
   - `frontend/parser/parser.runa` (≈2,800 lines) - parsing logic
   - `frontend/parser/ast.runa` (≈1,550 lines) - AST node definitions, helpers

3. **codegen.runa (3,490 lines) → 1 file (no change yet):**
   - `backend/x86_64/codegen.runa` (3,490 lines) - moved to new location

4. **Create initial pure Runa runtime:**
   - `src/runtime/runtime_io.runa` - syscalls (write, read, open, close, exit)

**Feature Tasks (from roadmap):**

5. **Error Handling Types:**
   - Built-in `Result of T and E` type (parser + codegen)
   - Built-in `Option of T` type (parser + codegen)
   - Pattern matching support for Result/Option (already in v0.0.8.3)
   - Helper methods: `is_success()`, `is_failure()`, `unwrap()`, `unwrap_or()`

**Bootstrap:** Use v0.0.8/build/runac to compile v0.0.9.0

**Timeline:** 2-3 weeks

---

### Phase 2: v0.0.9.1 - Semantic Analysis + Generics (Bootstrap with v0.0.9.0)

**Goals:**
1. **Refactoring:** Add semantic analysis phase between parser and codegen
2. **Features:** Implement generics/parametric polymorphism (from roadmap)

**Structural Additions:**

```
├── src/
│   ├── semantic/                      # NEW: Semantic analysis
│   │   ├── semantic_analyzer.runa     # Main analyzer
│   │   ├── type_checker.runa          # Type checking + generic instantiation
│   │   ├── symbol_table.runa          # Symbol management
│   │   ├── validation.runa            # Semantic validation
│   │   └── type_inference.runa        # Type inference for generics
│   │
│   └── runtime/
│       ├── runtime_io.runa            # (from v0.0.9.0)
│       └── runtime_memory.runa        # NEW: malloc, free syscalls in Runa
```

**Refactoring Changes:**
- Parser produces raw AST
- Semantic analyzer validates and annotates AST
- Semantic analyzer performs generic type instantiation (monomorphization)
- Codegen receives validated, annotated AST with concrete types

**Feature Tasks (from roadmap):**

1. **Generic Types:**
   - `Type Foo of T:` syntax (parser)
   - `Process foo of type T:` syntax (parser)
   - Type parameter tracking (semantic analyzer)
   - Monomorphization (generate separate code for each concrete type)

2. **Type Inference:**
   - Infer generic type parameters from usage
   - Example: `swap(5, 10)` infers `T = Integer`

3. **Generic Collections Foundation:**
   - `List of T`, `Dict of K and V`, `Set of T` (ready for stdlib)

**Bootstrap:** Use v0.0.9.0/build/runac to compile v0.0.9.1

**Timeline:** 3-4 weeks

---

### Phase 3: v0.0.9.2 - IR Foundation + Native Object Writer (Bootstrap with v0.0.9.1)

**Goals:**
1. **Refactoring:** Introduce IR layers (HIR, MIR)
2. **Features:** Native ELF64 object file writer + custom linker (from roadmap)

**Structural Additions:**

```
├── src/
│   ├── ir/                            # NEW: IR layers
│   │   ├── ir.runa                    # Common IR definitions
│   │   ├── hir/
│   │   │   ├── hir.runa               # HIR nodes
│   │   │   └── builder.runa           # HIR construction from AST
│   │   │
│   │   └── mir/
│   │       ├── mir.runa               # MIR nodes (basic, no SSA yet)
│   │       └── builder.runa           # MIR construction from HIR
│   │
│   ├── backend/
│   │   └── x86_64/
│   │       ├── codegen.runa           # Refactored for MIR input
│   │       ├── instruction_selector.runa  # NEW: MIR → x86-64 instructions
│   │       ├── object_writer.runa     # NEW: Native ELF64 writer
│   │       └── linker.runa            # NEW: Custom linker
│   │
│   └── runtime/
│       ├── runtime_io.runa            # (from v0.0.9.0)
│       ├── runtime_memory.runa        # (from v0.0.9.1)
│       └── runtime_string.runa        # NEW: string ops in Runa
```

**Refactoring Changes:**
- AST → HIR → MIR → x86-64 codegen
- Native object file generation (no more `as` dependency)
- Native linking (no more `ld` dependency)

**Feature Tasks (from roadmap):**

1. **ELF64 Object Writer:**
   - Generate `.o` files directly (no `.s` intermediate)
   - ELF64 format headers, section headers
   - Symbol table generation
   - Relocation entries
   - Sections: .text, .data, .rodata, .bss

2. **Custom Linker:**
   - Link multiple `.o` files into executable
   - Resolve symbols across modules
   - Handle relocations
   - Generate executable ELF binary
   - Support static linking, entry point specification

3. **New Compilation Flags:**
   - `runac program.runa -o program.o --emit=obj`
   - `runac --link main.o utils.o -o program`
   - `runac main.runa utils.runa -o program` (all-in-one)

**Bootstrap:** Use v0.0.9.1/build/runac to compile v0.0.9.2

**Timeline:** 4-6 weeks

---

### Phase 4: v0.0.9.3 - Pure Runa Runtime (Bootstrap with v0.0.9.2)

**Goals:**
1. **Feature:** Complete pure Runa runtime, eliminate `runtime.c` (from roadmap)
2. **Refactoring:** Finalize v0.0.9 architecture

**Structural Changes:**

```
├── src/
│   └── runtime/
│       ├── runtime_io.runa            # Complete I/O syscalls
│       ├── runtime_memory.runa        # Complete memory syscalls
│       ├── runtime_string.runa        # Complete string operations
│       └── runtime_file.runa          # File operations
│
└── runtime/
    └── runtime.c                      # DELETED - no longer needed!
```

**Feature Tasks (from roadmap):**

1. **Complete Runtime in Pure Runa:**
   - All syscalls implemented using inline assembly
   - Memory allocation (`mmap`, `munmap` syscalls)
   - String operations (using memory ops)
   - File operations (open, read, write, close syscalls)
   - Math operations (if needed)

2. **Compilation Process:**
   ```bash
   # Compile runtime modules to .o files
   runac src/runtime/runtime_io.runa -o runtime/runtime_io.o --emit=obj
   runac src/runtime/runtime_memory.runa -o runtime/runtime_memory.o --emit=obj
   runac src/runtime/runtime_string.runa -o runtime/runtime_string.o --emit=obj
   runac src/runtime/runtime_file.runa -o runtime/runtime_file.o --emit=obj

   # Link with user program
   runac main.runa --link runtime/*.o -o program
   ```

3. **Zero External Dependencies:**
   - ✅ No GCC (pure Runa runtime)
   - ✅ No as (native object generation from v0.0.9.2)
   - ✅ No ld (custom linker from v0.0.9.2)
   - ✅ Single binary distribution

**Bootstrap:** Use v0.0.9.2/build/runac to compile v0.0.9.3

**Timeline:** 2-3 weeks

---

### Phase 5: v0.1.0 - Complete Architecture + Stdlib Foundation (Bootstrap with v0.0.9.3)

**Goals:**
1. **Refactoring:** Full modular architecture with optimization pipeline
2. **Features:** Stdlib foundation using Result/Option/Generics from v0.0.9

**Complete Structure:**
- Full semantic analysis (dependency analysis, memory safety)
- IR optimization pipeline (constant folding, DCE, inlining)
- Stdlib foundation (collections, I/O, string operations)
- Toolchain utilities (runaobj, runadump)

**Bootstrap:** Use v0.0.9.3/build/runac to compile v0.1.0

**Timeline:** 4-6 weeks

---

## Detailed Module Breakdown

### Frontend: Lexer Module

**Files:**
- `frontend/lexer/lexer.runa` - Main lexer implementation
- `frontend/lexer/token.runa` - Token type definitions, utilities

**Responsibilities:**
- Tokenization of Runa source code
- Multi-word construct recognition
- Token stream generation
- Lexical error reporting

**Migration from v0.0.8:**
- Extract token type constants → `token.runa`
- Keep lexer state and logic → `lexer.runa`

---

### Frontend: Parser Module

**Files:**
- `frontend/parser/parser.runa` - Main parser implementation
- `frontend/parser/ast.runa` - AST node definitions

**Responsibilities:**
- Syntax analysis
- AST construction
- Parser error recovery
- Natural language construct parsing

**Migration from v0.0.8:**
- Extract all AST node structure definitions → `ast.runa`
- Extract AST helper functions → `ast.runa`
- Keep parsing logic → `parser.runa`

**AST Node Types to Extract:**
- Program, Function, Type, Statement, Expression
- All node type constants
- Node creation/manipulation functions

---

### Semantic Analysis Module (NEW in v0.0.9.1)

**Files:**
- `semantic/semantic_analyzer.runa` - Orchestration
- `semantic/type_checker.runa` - Type checking
- `semantic/symbol_table.runa` - Symbol management
- `semantic/validation.runa` - Semantic rules

**Responsibilities:**
- Type checking and inference
- Symbol resolution
- Semantic rule enforcement
- Error and warning generation

**New Capabilities:**
- Detect undefined variables
- Type mismatch detection
- Scope validation
- Function signature validation

---

### IR Module (NEW in v0.0.9.2)

**Structure:**
- HIR (High-level IR) - Close to source, preserves structure
- MIR (Mid-level IR) - Platform-independent, SSA form
- LIR (Low-level IR) - Close to machine, virtual registers

**Files:**
- `ir/ir.runa` - Common IR definitions
- `ir/hir/hir.runa`, `ir/hir/builder.runa`
- `ir/mir/mir.runa`, `ir/mir/builder.runa`

**Transformation Pipeline:**
```
AST → HIR → MIR → LIR → x86-64 Assembly → ELF64 Object
```

**Benefits:**
- Platform abstraction
- Optimization opportunities
- Multiple backend support (future)

---

### Backend: x86_64 Module

**v0.0.9.0 Files:**
- `backend/x86_64/codegen.runa` - Assembly generation

**v0.0.9.2 Files:**
- `backend/x86_64/codegen.runa` - Refactored for IR input
- `backend/x86_64/instruction_selector.runa` - MIR → x86-64 instructions
- `backend/x86_64/object_writer.runa` - Native ELF64 object file writer

**Responsibilities:**
- x86-64 instruction selection
- Register allocation
- Assembly generation
- Native object file generation (v0.0.9.2+)

**Migration from v0.0.8:**
- Keep codegen.runa mostly intact in v0.0.9.0
- Refactor in v0.0.9.2 to consume IR instead of AST

---

### Runtime Module

**v0.0.9.0:**
- Begin `src/runtime/runtime.runa` - Runa implementation of runtime functions
- Still link with `runtime/runtime.c` for functionality

**v0.0.9.2:**
- Complete `runtime.runa` implementation
- Eliminate `runtime.c` dependency

**Functions to Migrate:**
- Memory allocation (`memory_allocate`, `memory_free`)
- String operations (`string_concatenate`, `string_length`)
- I/O operations (`print_string`, `print_integer`, `file_read`, `file_write`)
- List operations (`list_create`, `list_append`, `list_get`)
- System operations (`sys_exit`, `sys_argc`, `sys_argv`)

---

## File Size Targets

### v0.0.9.0 Target Sizes

**Frontend:**
- `frontend/lexer/lexer.runa`: ≈1,200 lines (from 1,576)
- `frontend/lexer/token.runa`: ≈376 lines (extracted)
- `frontend/parser/parser.runa`: ≈2,800 lines (from 4,350)
- `frontend/parser/ast.runa`: ≈1,550 lines (extracted)

**Backend:**
- `backend/x86_64/codegen.runa`: ≈3,490 lines (unchanged, moved)

**Utils:**
- `utils/containers.runa`: 1,241 lines
- `utils/hashtable.runa`: 667 lines
- `utils/string_utils.runa`: 917 lines

**Total:** ≈12,241 lines in 8 files (vs 12,486 in 7 files)

**Improvement:** Better organization, similar total size

---

### v0.0.9.1 Target Sizes

**New Semantic Module:**
- `semantic/semantic_analyzer.runa`: ≈400 lines
- `semantic/type_checker.runa`: ≈600 lines
- `semantic/symbol_table.runa`: ≈500 lines
- `semantic/validation.runa`: ≈300 lines

**Total Addition:** ≈1,800 lines
**Overall Total:** ≈14,041 lines in 12 files

---

### v0.0.9.2 Target Sizes

**New IR Module:**
- `ir/ir.runa`: ≈200 lines
- `ir/hir/hir.runa`: ≈400 lines
- `ir/hir/builder.runa`: ≈600 lines
- `ir/mir/mir.runa`: ≈500 lines
- `ir/mir/builder.runa`: ≈700 lines

**Backend Expansion:**
- `backend/x86_64/codegen.runa`: ≈2,000 lines (refactored down)
- `backend/x86_64/instruction_selector.runa`: ≈1,200 lines (extracted)
- `backend/x86_64/object_writer.runa`: ≈1,500 lines (new)

**Runtime:**
- `runtime/runtime.runa`: ≈2,000 lines (complete implementation)

**Total Addition:** ≈3,900 lines
**Overall Total:** ≈17,941 lines in 21 files

---

### v0.1.0 Target Sizes

**Expanded Semantic:**
- Add `type_inference.runa`, `dependency_analyzer.runa`, `memory_analyzer.runa`
- ≈1,200 lines additional

**Expanded IR:**
- Add optimization passes (constant folding, DCE, inlining)
- ≈2,000 lines additional

**Stdlib Foundation:**
- Basic collections, I/O, strings
- ≈3,000 lines additional

**Overall Total:** ≈24,141 lines in ≈35 files

---

## Import Management

### v0.0.9.0 Import Examples

**frontend/lexer/lexer.runa:**
```runa
Import "token.runa"
Import "../../utils/string_utils.runa"
```

**frontend/parser/parser.runa:**
```runa
Import "ast.runa"
Import "../lexer/lexer.runa"
Import "../lexer/token.runa"
```

**backend/x86_64/codegen.runa:**
```runa
Import "../../frontend/parser/ast.runa"
Import "../../utils/string_utils.runa"
Import "../../utils/containers.runa"
```

---

### v0.0.9.1 Import Examples

**semantic/semantic_analyzer.runa:**
```runa
Import "../frontend/parser/ast.runa"
Import "type_checker.runa"
Import "symbol_table.runa"
Import "validation.runa"
```

**backend/x86_64/codegen.runa:**
```runa
Import "../../frontend/parser/ast.runa"
Import "../../semantic/semantic_analyzer.runa"  # NEW: for annotated AST
Import "../../utils/string_utils.runa"
```

---

### v0.0.9.2 Import Examples

**ir/mir/builder.runa:**
```runa
Import "../ir.runa"
Import "mir.runa"
Import "../hir/hir.runa"
Import "../../semantic/semantic_analyzer.runa"
```

**backend/x86_64/instruction_selector.runa:**
```runa
Import "../../ir/mir/mir.runa"
Import "../../ir/lir/lir.runa"
Import "codegen.runa"
```

**backend/x86_64/object_writer.runa:**
```runa
Import "../../utils/containers.runa"
Import "../../utils/hashtable.runa"
```

---

## Bootstrap Strategy

### 3-Stage Bootstrap Process (Maintained Throughout)

**Stage 1:** Compile new version with previous version's compiler
**Stage 2:** Compile new version with Stage 1 compiler
**Stage 3:** Compile new version with Stage 2 compiler (verify stability)

### Example: v0.0.9.0 Bootstrap

```bash
# Stage 1: Use v0.0.8/build/runac to compile v0.0.9.0 sources
cd runa/bootstrap/v0.0.9
mkdir -p stage1

# Compile all v0.0.9.0 source files with v0.0.8/build/runac
../v0.0.8/build/runac src/main.runa /tmp/main.s
as --64 /tmp/main.s -o stage1/main.o

../v0.0.8/build/runac src/frontend/lexer/lexer.runa /tmp/lexer.s
as --64 /tmp/lexer.s -o stage1/lexer.o

# ... (compile all modules)

gcc stage1/*.o runtime/runtime.o -lm -o stage1/runac

# Stage 2: Use stage1/runac to compile v0.0.9.0 sources again
mkdir -p stage2
./stage1/runac src/main.runa /tmp/main.s
as --64 /tmp/main.s -o stage2/main.o
# ... (repeat for all modules)
gcc stage2/*.o runtime/runtime.o -lm -o stage2/runac

# Stage 3: Use stage2/runac to compile v0.0.9.0 sources again
mkdir -p stage3
./stage2/runac src/main.runa /tmp/main.s
as --64 /tmp/main.s -o stage3/main.o
# ... (repeat for all modules)
gcc stage3/*.o runtime/runtime.o -lm -o stage3/runac

# Verify: stage2/runac and stage3/runac should be identical
diff stage2/runac stage3/runac
```

### Makefile Support

**v0.0.9.0 Makefile:**
```makefile
PREV_COMPILER = ../v0.0.8/build/runac
RUNTIME = runtime/runtime.o

SOURCES = \
	src/main.runa \
	src/frontend/lexer/lexer.runa \
	src/frontend/lexer/token.runa \
	src/frontend/parser/parser.runa \
	src/frontend/parser/ast.runa \
	src/backend/x86_64/codegen.runa \
	src/utils/containers.runa \
	src/utils/hashtable.runa \
	src/utils/string_utils.runa

all: stage1 stage2 stage3 build

stage1:
	mkdir -p stage1
	# Compile with v0.0.8 compiler
	$(PREV_COMPILER) src/main.runa /tmp/main.s && as --64 /tmp/main.s -o stage1/main.o
	# ... (all sources)
	gcc stage1/*.o $(RUNTIME) -lm -o stage1/runac

stage2:
	mkdir -p stage2
	# Compile with stage1
	./stage1/runac src/main.runa /tmp/main.s && as --64 /tmp/main.s -o stage2/main.o
	# ... (all sources)
	gcc stage2/*.o $(RUNTIME) -lm -o stage2/runac

stage3:
	mkdir -p stage3
	# Compile with stage2
	./stage2/runac src/main.runa /tmp/main.s && as --64 /tmp/main.s -o stage3/main.o
	# ... (all sources)
	gcc stage3/*.o $(RUNTIME) -lm -o stage3/runac

build:
	mkdir -p build
	cp stage3/runac build/runac

test:
	python3 run_tests.py

clean:
	rm -rf stage1 stage2 stage3 build /tmp/*.s /tmp/*.o
```

---

## Testing Strategy

### Unit Tests per Module

**v0.0.9.0:**
- `tests/unit/test_lexer.runa` - Lexer tests
- `tests/unit/test_parser.runa` - Parser tests
- `tests/unit/test_codegen.runa` - Codegen tests

**v0.0.9.1:**
- `tests/unit/test_semantic_analyzer.runa` - Semantic analysis
- `tests/unit/test_type_checker.runa` - Type checking

**v0.0.9.2:**
- `tests/unit/test_hir.runa` - HIR construction
- `tests/unit/test_mir.runa` - MIR construction
- `tests/unit/test_object_writer.runa` - Object file generation

### Integration Tests

- `tests/integration/test_full_compilation.runa` - End-to-end compilation
- `tests/integration/test_bootstrap.runa` - Bootstrap verification

### Regression Tests

- Maintain all v0.0.8 tests
- All existing tests must pass with new architecture

---

## Risk Mitigation

### Challenges

1. **Module Interdependencies**
   - **Risk:** Circular dependencies between modules
   - **Mitigation:** Clear layering (frontend → semantic → ir → backend)

2. **Import Path Management**
   - **Risk:** Complex relative imports break easily
   - **Mitigation:** Document import conventions, use consistent patterns

3. **Bootstrap Complexity**
   - **Risk:** More files = longer bootstrap time
   - **Mitigation:** Parallelize compilation where possible, optimize Makefile

4. **Runtime Migration**
   - **Risk:** Pure Runa runtime may have bugs vs. C runtime
   - **Mitigation:** Gradual migration, extensive testing, keep C runtime until v0.0.9.2

5. **Maintaining Compatibility**
   - **Risk:** Breaking changes during refactoring
   - **Mitigation:** Keep all v0.0.8 tests passing throughout

### Rollback Plan

- Each phase (v0.0.9.0, v0.0.9.1, v0.0.9.2) is a stable checkpoint
- If v0.0.9.1 fails, can revert to v0.0.9.0
- Git tags for each phase

---

## Success Criteria

### v0.0.9.0 Success Criteria
**Refactoring:**
- ✅ All v0.0.8 tests pass
- ✅ 3-stage bootstrap succeeds
- ✅ lexer.runa split into 2 files (lexer + token)
- ✅ parser.runa split into 2 files (parser + ast)
- ✅ codegen.runa moved to backend/x86_64/
- ✅ Initial runtime_io.runa created with basic syscalls

**Features (from roadmap):**
- ✅ Result<T,E> type implemented and functional
- ✅ Option<T> type implemented and functional
- ✅ Pattern matching works with Result/Option
- ✅ Helper methods work (is_success, unwrap, etc.)

### v0.0.9.1 Success Criteria
**Refactoring:**
- ✅ Semantic analysis module functional
- ✅ Type checking detects basic errors
- ✅ Symbol table resolves symbols correctly
- ✅ All v0.0.9.0 tests pass
- ✅ 3-stage bootstrap succeeds

**Features (from roadmap):**
- ✅ Generic types work (`Type Foo of T:`)
- ✅ Generic functions work (`Process foo of type T:`)
- ✅ Type inference infers generic parameters
- ✅ Monomorphization generates separate code per type
- ✅ Generic collections foundation ready for stdlib

### v0.0.9.2 Success Criteria
**Refactoring:**
- ✅ HIR layer functional
- ✅ MIR layer functional
- ✅ AST → HIR → MIR → x86-64 pipeline works
- ✅ All previous tests pass
- ✅ 3-stage bootstrap succeeds

**Features (from roadmap):**
- ✅ Native ELF64 object file generation works (no `as` dependency)
- ✅ Custom linker works (no `ld` dependency)
- ✅ New compilation flags work (--emit=obj, --link)
- ✅ Can compile and link Runa programs without external tools

### v0.0.9.3 Success Criteria
**Refactoring:**
- ✅ v0.0.9 architecture complete and stable
- ✅ All previous tests pass
- ✅ 3-stage bootstrap succeeds

**Features (from roadmap):**
- ✅ Pure Runa runtime complete (runtime.c deleted)
- ✅ All syscalls implemented in Runa with inline asm
- ✅ Zero external dependencies (no GCC/as/ld)
- ✅ Self-hosting with pure Runa runtime
- ✅ Bootstrap produces identical binaries

### v0.1.0 Success Criteria
**Refactoring:**
- ✅ Full semantic analysis (dependency analysis, memory safety)
- ✅ IR optimization pipeline (constant folding, DCE, inlining)
- ✅ Complete modular architecture

**Features (from roadmap):**
- ✅ Stdlib foundation (collections, I/O, strings)
- ✅ Toolchain utilities (runaobj, runadump)
- ✅ Beta-quality compiler
- ✅ All tests pass
- ✅ 3-stage bootstrap succeeds

---

## Timeline Estimate

**v0.0.9.0:** 2-3 weeks
- File splitting and reorganization (lexer, parser)
- Import path updates
- Bootstrap testing
- **Result<T,E> and Option<T> implementation**
- Initial runtime_io.runa with syscalls

**v0.0.9.1:** 3-4 weeks
- Semantic analyzer implementation
- Type checker implementation
- Symbol table implementation
- **Generics implementation (parser + semantic + monomorphization)**
- **Type inference for generics**
- runtime_memory.runa

**v0.0.9.2:** 4-6 weeks
- HIR implementation
- MIR implementation
- **ELF64 object writer (most complex)**
- **Custom linker**
- **New compilation flags (--emit=obj, --link)**
- runtime_string.runa

**v0.0.9.3:** 2-3 weeks
- **Complete pure Runa runtime (all syscalls)**
- **Eliminate runtime.c**
- **Zero external dependencies**
- runtime_file.runa

**v0.1.0:** 4-6 weeks
- Complete semantic analysis features
- IR optimization passes (constant folding, DCE, inlining)
- **Stdlib foundation (using Result/Option/Generics)**
- **Toolchain utilities (runaobj, runadump)**

**Total:** 15-22 weeks (≈4-5.5 months)

**Alignment with DEVELOPMENT_ROADMAP.md:**
- Roadmap shows v0.0.9: 6 weeks
- This plan: v0.0.9.0-v0.0.9.3 = 11-16 weeks
- **Difference:** We're adding architectural refactoring alongside feature work
- **Trade-off:** Takes longer, but results in maintainable, modular codebase

---

## Next Steps

1. **Review this plan** - Ensure alignment with goals
2. **Create v0.0.9.0 directory structure** - Set up initial layout
3. **Begin lexer split** - Start with smallest module (lexer → lexer + token)
4. **Update imports** - Fix import paths
5. **Test bootstrap** - Verify v0.0.8 can compile split sources
6. **Iterate** - Continue splitting parser, moving codegen

---

## References

- **_legacy/src/compiler** - Reference architecture for modular compiler
- **_legacy/src/runtime** - Reference architecture for runtime
- **v0.0.8 source** - Current monolithic implementation
- **DEVELOPMENT_ROADMAP.md** - Overall project roadmap
