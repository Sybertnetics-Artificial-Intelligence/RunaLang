# Runa Memory & Safety Master Plan
## Goal: Safer than Rust, Faster than C/JIT, Readable as Python

**Status:** Draft v1.0
**Created:** 2025-10-07
**Target:** v0.0.8.4 through v0.4.0

---

## 🎯 Vision

Runa will surpass all major languages in the safety/speed/ergonomics triangle:

1. **Safety > Rust** - Memory safety without borrow checker complexity
2. **Speed > C/Rust/JIT** - Zero-cost abstractions with compile-time optimization
3. **Experience > Python** - Natural syntax with automatic memory management

---

## 🚨 Critical Problem: Current State

**Lambda parser crash revealed fundamental issues:**
- No stack overflow protection
- Unsafe recursion in compiler itself
- Manual memory management without safety nets
- No bounds checking on arrays
- Null pointer vulnerabilities

**This must be fixed NOW or Runa cannot scale.**

---

## 📊 Feature Matrix

| Feature | Rust | C | Python/JIT | **Runa Target** |
|---------|------|---|------------|-----------------|
| Memory Safety | ✅ (borrow checker) | ❌ | ✅ (GC) | ✅ (compile-time) |
| Speed | ⚡⚡⚡ | ⚡⚡⚡⚡ | ⚡ | ⚡⚡⚡⚡⚡ |
| No GC Overhead | ✅ | ✅ | ❌ | ✅ |
| Zero-cost Abstractions | ✅ | ❌ | ❌ | ✅ |
| Developer Experience | ❌ (steep) | ❌ (unsafe) | ✅ | ✅ |
| Compile Time | ⚡⚡ (slow) | ⚡⚡⚡⚡ | N/A | ⚡⚡⚡⚡ |
| Stack Safety | ❌ | ❌ | ✅ (GC) | ✅ |
| Array Bounds Check | ✅ | ❌ | ✅ | ✅ (optimized away) |
| Null Safety | ✅ (Option) | ❌ | ⚡ (runtime) | ✅ (compile-time) |

---

## 🏗️ Implementation Roadmap

### Phase 1: Stack Safety (v0.0.8.4.1 - IMMEDIATE)
**Goal:** Fix lambda parser crash and prevent future stack issues

#### 1.1 Stack Overflow Protection
```runa
# Compiler automatically injects:
Process called "lambda_collect_free_vars" ...:
    # Auto-injected stack check
    inline assembly:
        cmpq %rsp, __stack_limit(%rip)
        jb __stack_overflow_panic
    :end inline

    # Original function body
    ...
End Process
```

**Implementation:**
- Add stack limit tracking to codegen context (offset 80)
- Inject stack probe at function entry for recursive functions
- Detect tail recursion and convert to loops (TCO)
- `--debug` mode: always check, `--release` mode: only if recursive depth unknown

**Tests:**
- `test_stack_overflow_detection.runa` - deep recursion triggers error, not crash
- `test_tail_call_optimization.runa` - factorial converts to loop
- `test_stack_probe_removed.runa` - non-recursive functions have no overhead

#### 1.2 Recursion Analysis
**Compile-time detection:**
```runa
# Compiler warns:
Process called "factorial" takes n as Integer returns Integer:
    If n is less than or equal to 1:
        Return 1
    End If
    Return n times factorial(n minus 1)  # ⚠️ Warning: Unbounded recursion detected
End Process

# Compiler suggests:
# Consider adding base case validation or using iteration
```

**Implementation:**
- Add call graph analysis pass
- Detect direct and indirect recursion
- Calculate max recursion depth if bounded
- Warn on unbounded recursion
- Auto-convert tail recursion to iteration

**Tests:**
- `test_recursion_warning.runa` - unbounded recursion warns
- `test_tail_recursion_converted.runa` - TCO happens
- `test_mutual_recursion_detected.runa` - indirect recursion caught

#### 1.3 Stack Size Calculation
**Know stack usage at compile time:**
```runa
# Compiler calculates:
Process called "parse_expression" takes parser as Integer returns Integer:
    Let local_array be Array of 100 Integers  # 800 bytes
    Let temp_string be String                   # 8 bytes (pointer)
    Let nested_call be parse_term(parser)       # + max(parse_term stack)
    ...
End Process
# Total stack: 808 + max_nested = Known at compile time
```

**Implementation:**
- Track local variable sizes
- Track max nested call stack usage
- Emit stack allocation instruction with exact size
- No wasted stack space

**Tests:**
- `test_stack_size_minimal.runa` - no over-allocation
- `test_large_local_array.runa` - correct space allocated

---

### Phase 2: Memory Safety (v0.0.8.4.2 - v0.0.8.5)
**Goal:** Prevent use-after-free, double-free, leaks

#### 2.1 Use-After-Free Detection
```runa
Process called "main" returns Integer:
    Let ptr be allocate(100)
    deallocate(ptr)
    memory_set_integer(ptr, 0, 42)  # ❌ Compile error: ptr used after deallocation
    Return 0
End Process
```

**Implementation:**
- Track allocation/deallocation in dataflow analysis
- Mark variables as "moved" after deallocation
- Error on use of moved variables
- Clear, readable error messages

**Tests:**
- `test_use_after_free_detected.runa` - compile error
- `test_double_free_detected.runa` - compile error
- `test_valid_pointer_usage.runa` - compiles

#### 2.2 Null Pointer Elimination
```runa
# OLD (unsafe):
Let ptr be 0  # Null pointer
If ptr is not equal to 0:
    memory_get_integer(ptr, 0)  # Runtime check needed
End If

# NEW (safe):
Let maybe_value be None of Integer
Match maybe_value:
    Case Some(value):
        # value is guaranteed non-null here
    Case None:
        # Handle missing value
End Match
```

**Implementation:**
- Deprecate raw null pointers (0)
- Enforce Option/Result types for potentially missing values
- Compiler guarantees no null dereferences
- Option is zero-cost (single pointer with null = None)

**Tests:**
- `test_null_pointer_forbidden.runa` - compile error
- `test_option_type_safety.runa` - compiles and correct
- `test_option_zero_cost.runa` - assembly has no overhead

#### 2.3 Array Bounds Checking
```runa
Process called "main" returns Integer:
    Let arr be Array of 10 Integers
    Let value be arr at 15  # ❌ Compile error if provable, runtime check otherwise
    Return 0
End Process
```

**Implementation:**
- Constant indices: check at compile time
- Variable indices: inject bounds check in debug mode
- Release mode: remove checks if provably safe (dataflow analysis)
- Track array lengths in type system

**Tests:**
- `test_constant_bounds_compile_error.runa` - index 15 of array[10] errors
- `test_variable_bounds_runtime_check.runa` - debug mode checks
- `test_bounds_check_optimized_away.runa` - release mode no check if safe

---

### Phase 3: Automatic Memory Management (v0.0.8.6 - v0.0.9)
**Goal:** No manual allocate/deallocate, all automatic at compile time

#### 3.1 Ownership Tracking
```runa
Process called "takes_ownership" takes data as Integer returns Integer:
    # 'data' is consumed here
    deallocate(data)
    Return 0
End Process

Process called "main" returns Integer:
    Let ptr be allocate(100)
    takes_ownership(ptr)
    # ptr is moved, compiler prevents further use
    # memory_set_integer(ptr, 0, 42)  # ❌ Compile error: ptr moved
    Return 0
End Process
```

**Implementation:**
- Track variable ownership in dataflow analysis
- Mark variables as "moved" when passed to consuming functions
- Prevent use of moved variables
- Automatic deallocation at end of scope

**Tests:**
- `test_ownership_move.runa` - move prevents reuse
- `test_ownership_borrow.runa` - borrowed variables still usable
- `test_auto_deallocate.runa` - memory freed at scope end

#### 3.2 Escape Analysis
```runa
Process called "main" returns Integer:
    # Compiler detects this doesn't escape - stack allocates
    Let local_array be Array of 100 Integers
    Let sum be 0
    For i from 0 to 99:
        Set sum to sum plus (local_array at i)
    End For
    Return sum
    # Compiler: No heap allocation, no deallocation needed
End Process
```

**Implementation:**
- Analyze if allocations escape function scope
- Stack-allocate non-escaping allocations
- Heap-allocate escaping allocations
- Zero overhead for local allocations

**Tests:**
- `test_escape_analysis_stack.runa` - local array on stack
- `test_escape_analysis_heap.runa` - returned pointer on heap
- `test_escape_closure_capture.runa` - captured variables on heap

#### 3.3 Compile-Time Reference Counting
```runa
Process called "main" returns Integer:
    Let data be allocate(1000)
    Let ptr1 be data  # refcount = 2 (compile-time)
    Let ptr2 be data  # refcount = 3

    # Compiler knows exact refcount at each point
    # Automatically inserts deallocation when refcount hits 0

    Return 0
    # Compiler: deallocate(data) inserted here
End Process
```

**Implementation:**
- Track reference counts at compile time where possible
- Insert deallocation when count reaches zero
- Fall back to runtime refcounting only for unpredictable cases
- Most cases are compile-time (faster than Rust's borrow checker)

**Tests:**
- `test_static_refcount.runa` - compile-time refcounting
- `test_dynamic_refcount.runa` - runtime refcounting when needed
- `test_zero_cost_rc.runa` - no overhead vs manual management

---

### Phase 4: Performance Features (v0.0.9 - v0.1.0)
**Goal:** Faster than C/Rust through aggressive optimization

#### 4.1 Arena Allocators
```runa
# Built-in arena allocator
Process called "parse_file" takes filename as String returns AST:
    Let arena be Arena create()

    # All allocations from arena (bulk malloc)
    Let tokens be arena allocate_array(Token, 1000)
    Let nodes be arena allocate_array(Node, 500)

    # Single bulk deallocation
    arena destroy()  # Frees everything at once
    Return ast
End Process
```

**Implementation:**
- Add Arena type to stdlib
- Bulk malloc/free (faster than per-object)
- Linear allocation (fast)
- Bulk deallocation (faster than individual frees)

**Tests:**
- `test_arena_allocator.runa` - bulk alloc/free
- `benchmark_arena_vs_malloc.runa` - 10x+ faster

#### 4.2 Inline Everything
```runa
# Small functions automatically inlined
Process called "square" takes x as Integer returns Integer:
    Return x times x
End Process

# Compiler inlines all calls:
Let result be square(5)  # → Let result be 5 times 5
```

**Implementation:**
- Inline functions < 50 instructions by default
- Cross-module inlining with LTO
- Profile-guided inlining (hot paths)
- No function call overhead for small functions

**Tests:**
- `test_inline_small_function.runa` - no call instruction in asm
- `test_inline_hot_path.runa` - loop body inlined
- `benchmark_inline_vs_call.runa` - measure speedup

#### 4.3 SIMD Auto-Vectorization
```runa
# Compiler auto-vectorizes:
Process called "sum_array" takes arr as Array of Integer, size as Integer returns Integer:
    Let sum be 0
    For i from 0 to size minus 1:
        Set sum to sum plus (arr at i)
    End For
    Return sum
End Process

# Generates:
# movdqa (%rdi), %xmm0     # Load 4 integers at once
# paddd %xmm0, %xmm1       # Add 4 integers in parallel
# (loop unrolled + vectorized)
```

**Implementation:**
- Detect vectorizable loops
- Emit SIMD instructions (SSE/AVX)
- Auto-unroll loops for better vectorization
- Fallback to scalar if not vectorizable

**Tests:**
- `test_simd_sum.runa` - uses SSE instructions
- `test_simd_multiply.runa` - vectorized element-wise ops
- `benchmark_simd_speedup.runa` - 4x+ faster than scalar

---

### Phase 5: Zero-Cost Abstractions (v0.1.0 - v0.2.0)
**Goal:** All safety checks compile away in release mode

#### 5.1 Zero-Sized Types (ZSTs)
```runa
# Marker type with no runtime cost:
Type PhantomData of T:
    # Empty - takes zero bytes
End Type

# Iterator with zero-cost state machine:
Type RangeIterator:
    Field current as Integer
    Field end as Integer
    Field phantom as PhantomData of Integer  # Zero bytes
End Type
```

**Implementation:**
- Detect types with size = 0
- Eliminate all loads/stores for ZST values
- Remove ZST fields from struct layouts
- Keep only enum tags, discard ZST variant data
- Zero call overhead for functions taking/returning Unit type

**Tests:**
- `test_zst_size_zero.runa` - sizeof(Unit) == 0
- `test_zst_no_codegen.runa` - no instructions for ZST ops
- `test_phantom_type_safety.runa` - type safety without cost
- `benchmark_zst_iterator.runa` - same speed as manual loop

#### 5.2 Bounds Check Elimination
```runa
Process called "sum_array" takes arr as Array of Integer, size as Integer returns Integer:
    Let sum be 0
    For i from 0 to size minus 1:
        Set sum to sum plus (arr at i)  # Compiler proves i < size, removes check
    End For
    Return sum
End Process
```

**Implementation:**
- Dataflow analysis proves index validity
- Remove redundant bounds checks
- Keep checks in debug mode
- Zero overhead in release mode

**Tests:**
- `test_bounds_check_removed.runa` - release asm has no check
- `test_bounds_check_kept.runa` - debug asm has check
- `benchmark_zero_cost_arrays.runa` - same speed as C

#### 5.3 Option Unwrap Elimination
```runa
Process called "main" returns Integer:
    Let maybe be Some(42)

    Match maybe:
        Case Some(x):
            Return x  # Compiler knows x is valid, no null check
        Case None:
            Return 0
    End Match
End Process

# Generated assembly has NO null check - compiler proved it
```

**Implementation:**
- Track Option state through dataflow
- Eliminate checks when proven Some
- Zero overhead vs raw pointers
- But with safety guarantees

**Tests:**
- `test_option_unwrap_eliminated.runa` - no null check in asm
- `benchmark_option_vs_null.runa` - identical performance

---

## 🧪 Testing Strategy

### Safety Tests (Must Fail to Compile)
- `test_use_after_free.runa` - compile error
- `test_double_free.runa` - compile error
- `test_null_dereference.runa` - compile error
- `test_out_of_bounds.runa` - compile error (constant index)
- `test_moved_variable_use.runa` - compile error

### Performance Tests (Must Match or Beat C)
- `benchmark_array_sum.runa` - same speed as C (vectorized)
- `benchmark_string_copy.runa` - same speed as memcpy
- `benchmark_arena_allocator.runa` - 10x faster than malloc/free
- `benchmark_inline_functions.runa` - zero call overhead
- `benchmark_bounds_check_removed.runa` - identical to unchecked C

### Compiler Tests (Validate Optimizations)
- `test_tco_applied.runa` - tail recursion becomes loop
- `test_escape_analysis.runa` - stack vs heap allocation correct
- `test_inline_applied.runa` - small functions have no call
- `test_simd_generated.runa` - SSE/AVX instructions present
- `test_bounds_check_eliminated.runa` - no check in release asm

---

## 📈 Version Integration

### v0.0.8.4.1 (IMMEDIATE - Week 1)
**Stack Safety Foundation**
- Stack overflow protection (probes)
- Tail call optimization
- Recursion depth analysis
- Fix lambda parser crash

### v0.0.8.4.2 (Week 2)
**Basic Memory Safety**
- Use-after-free detection
- Null pointer elimination (enforce Option)
- Array bounds checking (always in debug)

### v0.0.8.5 (Week 3-4)
**Automatic Memory - Phase 1**
- Ownership tracking
- Move semantics
- Compile-time memory analysis

### v0.0.8.6 (Month 2)
**Performance Features**
- Arena allocators
- Basic inlining
- Escape analysis

### v0.0.9 (Month 3-4)
**Advanced Memory Management**
- Compile-time reference counting
- Advanced escape analysis
- Cross-module optimization

### v0.1.0 (Month 5-6)
**Zero-Cost Abstractions**
- Bounds check elimination
- SIMD auto-vectorization
- Full optimization pipeline

### v0.2.4 (Month 9-12)
**Optional GC (Fallback Only)**
- Mark-sweep collector
- Generational GC
- Only for truly dynamic cases

### v0.4.0 (Year 2)
**Rust-Level Safety**
- Full ownership system
- Lifetime inference
- Complete memory safety guarantees

---

## 🎯 Success Metrics

**Safety (Better than Rust):**
- ✅ Zero use-after-free bugs (compile-time prevention)
- ✅ Zero null pointer dereferences (Option enforced)
- ✅ Zero buffer overflows (bounds checking)
- ✅ Clear error messages (no lifetime annotations needed)
- ✅ Compile-time guarantees (no runtime overhead)

**Speed (Faster than C/Rust/JIT):**
- ✅ Array operations: Same speed as C (vectorized)
- ✅ Memory allocation: 10x faster (arena allocators)
- ✅ Function calls: Zero overhead (inlining)
- ✅ Abstractions: Zero cost (optimized away)
- ✅ No GC pauses (compile-time management)

**Experience (Better than Python):**
- ✅ Natural syntax (already have)
- ✅ Type inference (don't write types everywhere)
- ✅ Clear errors ("Variable x freed here, used here" not "lifetime error")
- ✅ Fast compilation (< 1 second for most programs)
- ✅ No manual memory management (automatic)

---

## 🚀 Next Steps

1. **Immediate:** Implement Phase 1 (Stack Safety) to fix lambda crash
2. **Week 1:** Complete stack overflow protection and TCO
3. **Week 2:** Add use-after-free detection and Option enforcement
4. **Month 1:** Full automatic memory management foundation
5. **Month 2-3:** Performance features (arena, inline, SIMD)
6. **Month 4-6:** Zero-cost abstractions and optimization

---

## 📝 Notes

**Philosophy:**
- **Compile-time > Runtime** - Do everything possible at compilation
- **Zero-cost** - Abstractions must have no runtime overhead
- **Clarity** - Error messages must be understandable by non-experts
- **Progressive** - Start simple, add complexity only when needed

**Design Principles:**
1. Safety by default (must explicitly opt into unsafe)
2. Performance by default (optimizations on by default)
3. Clarity in errors (explain what's wrong and how to fix)
4. Incremental adoption (can mix manual and automatic memory management)

---

**End of Memory & Safety Master Plan v1.0**
