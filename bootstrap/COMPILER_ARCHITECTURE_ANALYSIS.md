# Runa Compiler Architecture Analysis & Modernization Plan

**Date**: 2025-10-11
**Current Version**: v0.0.8.4.5
**Target**: World-class compiler architecture

---

## 1. CURRENT ARCHITECTURE PROBLEMS

### 1.1 Import System Issues
**Current State (v0.0.8.4.5):**
- ❌ **No recursive import processing** - doesn't handle transitive dependencies
- ❌ **No deduplication** - same file can be imported multiple times
- ❌ **No cycle detection** - circular imports cause infinite loops
- ❌ **Re-parses every import** - no caching of parsed modules
- ❌ **No dependency graph** - can't determine build order
- ❌ **Sequential processing** - can't parallelize independent imports

**Problems This Causes:**
```
sizeof.runa imports alignment_core.runa
alignment_core.runa imports pointer_primitive.runa

Result: pointer_primitive.runa never gets processed!
```

### 1.2 Global State Problems
**Current State:**
- ❌ **No global state mechanism** - can't track compiler-wide information
- ❌ **Attempting to use top-level `Let`** - doesn't work for mutable state
- ❌ **Pass-by-value semantics** - can't share state across function calls

**What We Need:**
- Compilation context that tracks:
  - Imported modules
  - Symbol table
  - Type information
  - Error accumulation
  - Configuration

### 1.3 Error Handling Issues
**Current State:**
- ❌ **Immediate termination on error** - stops at first error
- ❌ **No error recovery** - can't continue parsing after error
- ❌ **No error context** - hard to debug compound errors
- ❌ **Printf-style errors** - not machine-readable

**Production Compilers:**
- Collect all errors before stopping
- Provide rich diagnostics with source location
- Suggest fixes
- Machine-readable output (JSON, etc.)

### 1.4 Memory Management Issues
**Current State:**
- ❌ **Manual memory management** - easy to leak or double-free
- ❌ **No ownership tracking** - unclear who owns what
- ❌ **No RAII pattern** - manual cleanup everywhere
- ❌ **Pointer arithmetic** - `memory_get_pointer(ptr, offset)` is error-prone

**Problems:**
```runa
Let import_source be read_file_internal(import_filename)
Note: If we return early, who frees import_source?
Note: Cleanup code duplicated in every error path
```

### 1.5 Data Structure Issues
**Current State:**
- ❌ **Raw pointers everywhere** - `Integer` used as pointer type
- ❌ **Magic offset numbers** - `memory_get_int32(program, 40)` - what is 40?
- ❌ **No type safety** - everything is `Integer`
- ❌ **Manual array management** - no dynamic arrays

**Example of Poor Practice:**
```runa
Let import_count be memory_get_int32(program, 40)  Note: PROGRAM_IMPORT_COUNT
Let imports be memory_get_pointer(program, 32)      Note: PROGRAM_IMPORTS
```
What if offsets change? Everything breaks!

### 1.6 Control Flow Issues
**Current State:**
- ❌ **No `break` statement** - can't exit loops early
- ❌ **No `continue` statement** - forced to nest everything in `If` blocks
- ❌ **No early return guards** - error handling is deeply nested

**Example of Painful Code:**
```runa
If condition is equal to 0:
    Note: Everything must go inside here
    If another_condition is equal to 1:
        Note: Deeply nested
        If yet_another is equal to 1:
            Note: Even more nested!
        End If
    End If
End If
```

### 1.7 String Handling Issues
**Current State:**
- ❌ **Manual string concatenation** - creates many temporary strings
- ❌ **No string builder** - inefficient for multiple concatenations
- ❌ **Must manually deallocate** - easy to leak
- ❌ **No string interpolation** - can't do `"Error: {filename}"`

**Example:**
```runa
Let error_msg_temp be string_concat("[IMPORT ERROR] Failed to read: ", import_filename)
print_string(error_msg_temp)
deallocate(error_msg_temp)
```

---

## 2. WORLD-CLASS ARCHITECTURE DESIGN

### 2.1 Core Principle: Context-Oriented Architecture

**The Foundation:**
```
┌──────────────────────────────────────────────────────────┐
│             CompilerContext (Single Source of Truth)      │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  ┌─────────────────┐  ┌──────────────────┐              │
│  │  ModuleCache    │  │  SymbolTable     │              │
│  │                 │  │                  │              │
│  │  hash → AST     │  │  name → symbol   │              │
│  │  path → module  │  │  scope hierarchy │              │
│  └─────────────────┘  └──────────────────┘              │
│                                                           │
│  ┌─────────────────┐  ┌──────────────────┐              │
│  │  TypeCache      │  │  ErrorCollector  │              │
│  │                 │  │                  │              │
│  │  type checking  │  │  all errors      │              │
│  │  memoization    │  │  warnings        │              │
│  └─────────────────┘  └──────────────────┘              │
│                                                           │
│  ┌─────────────────┐  ┌──────────────────┐              │
│  │  DependencyDAG  │  │  Configuration   │              │
│  │                 │  │                  │              │
│  │  import graph   │  │  compiler flags  │              │
│  │  build order    │  │  paths, options  │              │
│  └─────────────────┘  └──────────────────┘              │
│                                                           │
└──────────────────────────────────────────────────────────┘
                    ↓
        Passed to ALL compiler phases:

        process_imports(context, program)
        resolve_symbols(context, program)
        type_check(context, program)
        generate_code(context, program)
```

### 2.2 Module Cache System

**Design:**
```runa
Structure ModuleCache:
    modules: HashMap<String, Module>
    loading: HashSet<String>  Note: Detect circular imports

Structure Module:
    path: String
    content_hash: String
    ast: Program
    exports: SymbolTable
    imports: Array<String>
    state: ModuleState  Note: Loading, Loaded, Error
```

**Benefits:**
- ✅ Content-based deduplication
- ✅ Cycle detection
- ✅ Lazy loading
- ✅ Parallel compilation ready

### 2.3 Dependency Graph

**Design:**
```runa
Structure DependencyGraph:
    nodes: HashMap<String, Node>
    edges: Array<Edge>

Structure Node:
    module_path: String
    dependencies: Array<String>
    dependents: Array<String>

Process called "topological_sort" takes graph returns Array<String>:
    Note: Returns compilation order
```

**Benefits:**
- ✅ Detects cycles
- ✅ Optimal build order
- ✅ Parallel compilation
- ✅ Incremental builds

### 2.4 Error Collection System

**Design:**
```runa
Structure ErrorCollector:
    errors: Array<CompileError>
    warnings: Array<CompileWarning>
    max_errors: Integer

Structure CompileError:
    message: String
    file: String
    line: Integer
    column: Integer
    severity: ErrorSeverity
    suggestion: String
```

**Benefits:**
- ✅ Collect all errors before stopping
- ✅ Rich diagnostics
- ✅ IDE integration friendly
- ✅ Actionable suggestions

### 2.5 Type System with Caching

**Design:**
```runa
Structure TypeCache:
    types: HashMap<String, Type>
    constraints: Array<Constraint>

Note: Memoized type checking
Process called "get_type" takes context, expr returns Type:
    If expr in context.type_cache:
        Return cached_type
    End If
    Let computed_type be compute_type(context, expr)
    cache_type(context, expr, computed_type)
    Return computed_type
End Process
```

---

## 3. TIERED IMPLEMENTATION PLAN

### Phase 1: Foundation (v0.0.8.4.5.1)
**Goal: Basic Context Structure**

**Add:**
1. `CompilerContext` structure
2. Pass context through compilation pipeline
3. Basic module cache (array-based)

**Changes:**
- `main()` creates context
- `process_imports(context, program)` - takes context
- `codegen_generate(context, codegen, program)` - takes context

**Testing:**
- Compile simple programs
- Verify context is passed correctly

---

### Phase 2: Import Deduplication (v0.0.8.4.5.2)
**Goal: Fix duplicate imports**

**Add:**
1. Module cache in context
2. Check cache before importing
3. Mark modules as loaded

**Changes:**
- Import cache stored in context
- `is_module_loaded(context, path)` function
- `mark_module_loaded(context, path, ast)` function

**Testing:**
- `sizeof.runa` with nested imports
- Verify no duplicate processing

---

### Phase 3: Recursive Imports (v0.0.8.4.5.3)
**Goal: Handle transitive dependencies**

**Add:**
1. Recursive import processing
2. Cycle detection (simple)

**Changes:**
- `process_imports` recursively processes nested imports
- Check for cycles using "loading" set

**Testing:**
- Deep import chains (A→B→C)
- Detect circular imports (A→B→A)

---

### Phase 4: Dependency Graph (v0.0.8.4.5.4)
**Goal: Build proper dependency tracking**

**Add:**
1. Dependency graph structure
2. Topological sort
3. Build order computation

**Changes:**
- Build graph of all imports
- Process in correct order
- Better error messages for cycles

**Testing:**
- Complex import graphs
- Diamond dependencies (A→B,C; B,C→D)

---

### Phase 5: Error Collection (v0.0.8.4.5.5)
**Goal: Better error handling**

**Add:**
1. Error collector in context
2. Continue on error
3. Report all errors at end

**Changes:**
- Don't return immediately on error
- Add error to collector
- Check error count at end

**Testing:**
- File with multiple errors
- Verify all errors reported

---

### Phase 6: Memory Management Patterns (v0.0.8.4.5.6)
**Goal: Safer memory handling**

**Add:**
1. Resource ownership pattern
2. Scope-based cleanup
3. Error path cleanup helpers

**Changes:**
- Clear ownership rules
- `defer`-like cleanup (if possible)
- Automated cleanup on error

**Testing:**
- Verify no leaks with valgrind
- Test error paths

---

### Phase 7: Control Flow Improvements (v0.0.8.4.5.7)
**Goal: Add break/continue**

**Add:**
1. `break` statement
2. `continue` statement
3. Guard clauses support

**Changes:**
- Lexer: add BREAK, CONTINUE tokens
- Parser: parse break/continue
- Codegen: generate jump instructions

**Testing:**
- Loop with break
- Loop with continue
- Nested loops

---

### Phase 8: String Builder (v0.0.8.4.5.8)
**Goal: Efficient string operations**

**Add:**
1. StringBuilder structure
2. Append operations
3. Finalize to string

**Changes:**
- Replace manual concatenation
- Use StringBuilder for error messages
- Reduce allocations

**Testing:**
- Build large strings efficiently
- Measure performance improvement

---

### Phase 9: Integration & Polish (v0.0.8.4.6)
**Goal: Bring it all together**

**Final System:**
- Complete context-based architecture
- Full import system with caching
- Error collection and reporting
- Better memory management
- Modern control flow
- Efficient string handling

**Testing:**
- Full compiler test suite
- Primitive system (all 46 files)
- Performance benchmarks
- Memory leak tests

---

## 4. WORLD-CLASS FEATURES FOR FUTURE

### v0.0.8.5+: Query System (Rust-style)
```runa
Process called "query_module_exports" takes context, path returns SymbolTable:
    Note: Memoized query
    If cached(context, "exports", path):
        Return get_cached(context, "exports", path)
    End If

    Let module be load_module(context, path)
    Let exports be compute_exports(context, module)
    cache_result(context, "exports", path, exports)
    Return exports
End Process
```

### v0.0.8.6+: Incremental Compilation
- Track file timestamps/hashes
- Only recompile changed modules
- Save compiled artifacts
- Load from cache when possible

### v0.0.8.7+: Parallel Compilation
- Build dependency graph
- Identify independent modules
- Compile in parallel
- Thread pool for worker threads

### v0.0.8.8+: Semantic Analysis Phase
- Separate parsing from semantic analysis
- Multi-pass compilation
- Better type checking
- Optimization passes

---

## 5. COMPARISON TO PRODUCTION COMPILERS

### Current Runa (v0.0.8.4.5)
```
Parse → Process Imports (flat) → Generate Code
```

### After Modernization (v0.0.8.4.6)
```
Parse → Build Dep Graph → Process Imports (recursive, cached) →
Semantic Analysis → Type Check → Generate Code
```

### Rust (rustc)
```
Parse → Expand Macros → Name Resolution → Type Check →
Borrow Check → MIR → Optimization → LLVM IR → Machine Code
```

### Our Competitive Advantages After v0.0.8.4.6:
1. ✅ Context-based architecture (same as Rust, GCC)
2. ✅ Module caching (same as Python, Java)
3. ✅ Dependency graph (same as Go, Rust)
4. ✅ Error collection (same as modern compilers)
5. ✅ Clear data ownership (preparing for borrow checking)

**We would be competitive with:**
- Early Rust (before MIR)
- Go compiler (similar simplicity + power)
- Zig (explicit, clear architecture)

**We would SURPASS:**
- C (no preprocessor mess)
- C++ (cleaner import system than headers)
- Python (static typing + performance)

---

## 6. SUCCESS CRITERIA

### v0.0.8.4.6 Must:
1. ✅ Handle nested imports correctly (sizeof → alignment_core → pointer_primitive)
2. ✅ Deduplicate imports automatically
3. ✅ Detect circular imports with clear error
4. ✅ Collect multiple errors before stopping
5. ✅ No global variables (all in context)
6. ✅ Pass all existing tests
7. ✅ Compile all 46 primitive files
8. ✅ No memory leaks (valgrind clean)
9. ✅ 10% faster than v0.0.8.4.5 (due to caching)
10. ✅ Clear architecture for future extensions

---

## 7. FILES TO MODIFY

### v0.0.8.4.5.1 (Context Foundation):
- `src/main.runa` - Create CompilerContext, pass to functions
- `src/parser.runa` - Accept context parameter
- `src/codegen.runa` - Accept context parameter

### v0.0.8.4.5.2 (Import Deduplication):
- `src/main.runa` - Add module cache to context
- `src/containers.runa` - May need HashMap/Set if not available

### v0.0.8.4.5.3 (Recursive Imports):
- `src/main.runa` - Recursive process_imports

### v0.0.8.4.5.4 (Dependency Graph):
- `src/main.runa` - Build and use dep graph
- New: `src/depgraph.runa` (maybe)

### v0.0.8.4.5.5 (Error Collection):
- `src/main.runa` - Use error collector
- `src/lexer.runa` - Report errors to collector
- `src/parser.runa` - Report errors to collector

### v0.0.8.4.5.6 (Memory):
- All files - Review ownership

### v0.0.8.4.5.7 (Control Flow):
- `src/lexer.runa` - Add BREAK/CONTINUE tokens
- `src/parser.runa` - Parse break/continue
- `src/codegen.runa` - Generate jumps

### v0.0.8.4.5.8 (StringBuilder):
- New: `src/string_builder.runa` (or in string_utils)
- All files - Use StringBuilder

---

## NEXT STEPS

1. ✅ Review this plan
2. Start with v0.0.8.4.5.1 (Context Foundation)
3. Implement each phase incrementally
4. Test thoroughly at each step
5. Reach v0.0.8.4.6 with world-class architecture

**This plan gives us a compiler architecture that rivals Rust, Go, and Zig!**
