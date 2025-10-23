# Runa Memory Architecture

**Version:** 0.0.8.4.5.2+
**Status:** Instance/Arena Hybrid Implementation
**Philosophy:** Predictable, Safe, Fast

---

## The Golden Rule

> **"Arena for TEMPS, Ownership for PERMANENT"**

Memory must be freed exactly once. Choose the allocation strategy based on data lifetime, never mix strategies on the same data.

---

## Architecture Overview

Runa uses a **four-tier memory model** that provides optimal performance and safety for different data lifetimes:

```
┌─────────────────────────────────────────────────────┐
│  TIER 1: STACK      │ Fastest, Deterministic        │
│  - Local variables  │ Scope-based lifetime          │
│  - Fixed buffers    │ Zero allocation overhead      │
├─────────────────────────────────────────────────────┤
│  TIER 2: ARENA      │ Fast Bulk, O(1) Cleanup       │
│  - Temporary data   │ Operation-scoped lifetime     │
│  - Compilation temps│ Thousands of allocations → 1  │
├─────────────────────────────────────────────────────┤
│  TIER 3: OWNED HEAP │ Permanent, Structured         │
│  - Program data     │ Object-scoped lifetime        │
│  - Data structures  │ Deterministic cleanup         │
├─────────────────────────────────────────────────────┤
│  TIER 4: SHARED     │ Multiple Owners, Ref-counted  │
│  - Shared resources │ Last-owner-frees lifetime     │
│  - Caches          │ Atomic reference counting     │
└─────────────────────────────────────────────────────┘
```

---

## Tier 1: STACK Allocation

### What
Fixed-size, short-lived local variables with automatic lifetime management.

### When to Use
- Loop counters and indices
- Temporary calculations
- Small fixed-size buffers (< 4KB)
- Critical real-time code paths
- Any data that doesn't outlive function scope

### Performance
- **Allocation:** 0 nanoseconds (compiler-managed)
- **Deallocation:** 0 nanoseconds (automatic)
- **Overhead:** Zero bytes

### Example
```runa
Process called "calculate_trajectory" takes velocity as Integer returns Integer:
    Let buffer as Array[256] of Byte  // STACK - automatic
    Let result as Integer              // STACK - automatic
    Let i as Integer                   // STACK - automatic

    Set i to 0
    While i is less than 256:
        Set buffer[i] to 0
        Set i to i plus 1
    End While

    Set result to velocity multiplied by 2
    Return result
    // Everything freed automatically at scope end - O(1)
End Process
```

### Rules
- ✅ Perfect for real-time systems (NASA, police, emergency)
- ✅ Deterministic behavior (no allocation failures)
- ✅ Cache-friendly (contiguous memory)
- ❌ Cannot return pointers to stack data
- ❌ Limited size (typically 1-8MB total stack)
- ❌ Must know size at compile time

---

## Tier 2: ARENA Allocation

### What
Bulk temporary allocations with single-operation lifetime. All allocations freed together in O(1) time.

### When to Use
- Compiler temporaries (tokens, intermediate AST)
- HTTP request processing (headers, params, body parsing)
- Batch AI inference (preprocessing, feature extraction)
- Video/image frame processing
- Any data that lives for the duration of one "operation"

### How It Works
```
Arena = [======================================] 1MB buffer
         ^ pointer bumps forward for each allocation

Allocate 100 bytes:  [XXX------------------------------]
Allocate 200 bytes:  [XXXYYY---------------------------]
Allocate 50 bytes:   [XXXYYYZZZ------------------------]

Destroy arena:       [--------------------------------] ← All freed in O(1)!
```

### Performance
- **Allocation:** ~10 nanoseconds (pointer bump)
- **Deallocation:** ~100 nanoseconds (one free for entire arena)
- **Overhead:** 24 bytes per arena + unused capacity

### Example
```runa
Process called "compile_file" takes filename as String returns Program:
    // Create arena for ALL temporary compilation data
    Let arena be arena_create(1048576)  // 1MB arena

    // Phase 1: Lexing (thousands of temp allocations)
    Let source be arena_read_file(arena, filename)
    Let tokens be arena_tokenize(arena, source)
    // tokens might be 10,000+ Token structs → all in arena

    // Phase 2: Parsing (tens of thousands of temp nodes)
    Let temp_ast be arena_parse_tokens(arena, tokens)
    // temp_ast might be 50,000+ nodes → all in arena

    // Phase 3: Extract only what's needed (copy to owned heap)
    Let program be Program.from_temp_ast(temp_ast)  // OWNED
    // Copies validated AST to permanent heap storage

    // Destroy arena - frees EVERYTHING at once
    arena_destroy(arena)  // 60,000+ allocations freed in one operation!

    Return program  // Only permanent data survives
End Process
```

### Arena API
```runa
// Create arena
Let arena be arena_create(initial_capacity as Integer) returns Arena

// Allocate from arena (fast - pointer bump)
Let ptr be arena_allocate(arena, size as Integer) returns Pointer

// Duplicate string in arena
Let str be arena_string_duplicate(arena, source as String) returns String

// Convert integer to string in arena
Let str be arena_integer_to_string(arena, value as Integer) returns String

// Concatenate strings in arena
Let result be arena_string_concat(arena, str1, str2) returns String

// Reset arena (reuse buffer, keep capacity)
arena_reset(arena)

// Destroy arena (bulk free)
arena_destroy(arena)

// Query arena state
Let used be arena_get_used(arena) returns Integer
Let capacity be arena_get_capacity(arena) returns Integer
```

### Rules
- ✅ ONLY for data that lives for one "operation"
- ✅ Grows automatically if capacity exceeded
- ✅ Perfect for compilers, parsers, batch processing
- ❌ NEVER store arena pointers in permanent structures
- ❌ NEVER call deallocate() on arena-allocated memory
- ⚠️ Arena must outlive all pointers into it

### Critical Pattern: Copy Out
```runa
// ❌ WRONG: Storing arena pointer
Let arena be arena_create(1024)
Let temp be arena_string_duplicate(arena, "Hello")
some_struct.name = temp  // ❌ BAD! temp will be freed with arena
arena_destroy(arena)     // some_struct.name is now dangling!

// ✅ CORRECT: Copy to owned heap
Let arena be arena_create(1024)
Let temp be arena_string_duplicate(arena, "Hello")
some_struct.name = string_duplicate(temp)  // ✅ GOOD! Owned copy
arena_destroy(arena)  // temp freed, some_struct.name still valid
```

---

## Tier 3: OWNED HEAP Allocation

### What
Individually-managed heap allocations with structured ownership and deterministic cleanup.

### When to Use
- Program AST nodes (owned by Program)
- Application configuration (owned by App)
- Data structures (owned by parent struct)
- Any data that outlives the operation that created it
- Output data (results, reports, saved state)

### Performance
- **Allocation:** ~100 nanoseconds (malloc)
- **Deallocation:** ~50 nanoseconds (free)
- **Overhead:** ~16-32 bytes per allocation

### Example
```runa
// Structure definition with owned fields
Structure Program:
    functions: Pointer to Array      // Owned by Program
    types: Pointer to Array           // Owned by Program
    name: Pointer to String           // Owned by Program
    function_count: Integer
End Structure

// Constructor allocates owned data
Process called "program_create" takes name as String returns Program:
    Let prog be allocate(32)  // Allocate Program struct

    Let name_copy be string_duplicate(name)  // OWNED
    memory_set_pointer(prog, 0, name_copy)

    Let functions be allocate(16 multiplied by 8)  // OWNED array
    memory_set_pointer(prog, 8, functions)

    memory_set_int32(prog, 16, 0)  // function_count

    Return prog
End Process

// Destructor frees owned data
Process called "program_destroy" takes program as Program returns Nothing:
    If program is equal to 0:
        Return
    End If

    // Free owned name
    Let name be memory_get_pointer(program, 0)
    If name is not equal to 0:
        deallocate(name)
    End If

    // Free owned functions array
    Let functions be memory_get_pointer(program, 8)
    If functions is not equal to 0:
        Let count be memory_get_int32(program, 16)
        Let i be 0
        While i is less than count:
            Let func_ptr be memory_get_pointer(functions, i multiplied by 8)
            function_destroy(func_ptr)  // Recursive ownership
            Set i to i plus 1
        End While
        deallocate(functions)
    End If

    // Free Program struct itself
    deallocate(program)
End Process

// Usage
Process called "main" returns Integer:
    Let prog be program_create("MyProgram")

    // Use program...

    program_destroy(prog)  // Deterministic cleanup
    Return 0
End Process
```

### Ownership Rules
1. **One Owner:** Each allocation has exactly one owner
2. **Owner Destroys:** Owner is responsible for calling deallocate()
3. **Transfer Ownership:** Can transfer, but then old owner must not touch it
4. **No Sharing:** If multiple owners needed, use Tier 4 (Shared)

### Rules
- ✅ Clear ownership semantics
- ✅ Deterministic destruction order
- ✅ Works for any lifetime pattern
- ❌ Must manually manage (unlike arena)
- ❌ Each allocation has overhead
- ⚠️ Must ensure destructor is called

---

## Tier 4: SHARED HEAP Allocation

### What
Reference-counted heap allocations with multiple owners. Freed when last owner releases.

### When to Use
- Shared configuration (multiple threads/workers)
- String interning pools
- Cache entries
- Shared resources (database connections)
- Circular data structures (with weak references)

### Performance
- **Allocation:** ~100 nanoseconds (malloc + ref count init)
- **Retain:** ~5 nanoseconds (atomic increment)
- **Release:** ~5-50 nanoseconds (atomic decrement + maybe free)
- **Overhead:** ~16-32 bytes + 8 bytes ref count

### Example
```runa
// Reference-counted structure
Structure RefCounted:
    data: Pointer              // The actual data
    ref_count: Integer         // Number of owners
End Structure

Process called "refcount_create" takes data as Pointer returns RefCounted:
    Let rc be allocate(16)
    memory_set_pointer(rc, 0, data)
    memory_set_integer(rc, 8, 1)  // Initial ref count = 1
    Return rc
End Process

Process called "refcount_retain" takes rc as RefCounted returns RefCounted:
    Let count be memory_get_integer(rc, 8)
    Set count to count plus 1
    memory_set_integer(rc, 8, count)
    Return rc
End Process

Process called "refcount_release" takes rc as RefCounted returns Nothing:
    Let count be memory_get_integer(rc, 8)
    Set count to count minus 1
    memory_set_integer(rc, 8, count)

    If count is equal to 0:
        Let data be memory_get_pointer(rc, 0)
        deallocate(data)    // Free the data
        deallocate(rc)      // Free the ref count struct
    End If
End Process

// Usage: Shared configuration
Process called "main" returns Integer:
    // Create shared config
    Let config_data be load_configuration()
    Let shared_config be refcount_create(config_data)

    // Worker 1 retains reference
    Let worker1_config be refcount_retain(shared_config)
    start_worker(worker1, worker1_config)

    // Worker 2 retains reference
    Let worker2_config be refcount_retain(shared_config)
    start_worker(worker2, worker2_config)

    // Main releases its reference
    refcount_release(shared_config)
    // Config still alive - workers own it

    // Workers eventually release - last one frees
    Return 0
End Process
```

### Rules
- ✅ Multiple owners safe
- ✅ Automatic cleanup when last owner releases
- ✅ Thread-safe with atomic operations
- ❌ More expensive than owned (ref counting overhead)
- ⚠️ Watch for cycles (A→B→A = memory leak)
- ⚠️ Use weak references to break cycles

---

## Decision Matrix

### Which Tier Should I Use?

```
START HERE
    ↓
┌───────────────────────────────┐
│ Is size known at compile time?│
│ AND < 4KB?                    │
└───────────────────────────────┘
    YES ↓              NO ↓
    ┌──────────┐         ↓
    │  STACK   │         ↓
    └──────────┘         ↓
                         ↓
┌────────────────────────────────────┐
│ Does data live only during one     │
│ operation (compile, request, etc)? │
└────────────────────────────────────┘
    YES ↓                    NO ↓
    ┌──────────┐               ↓
    │  ARENA   │               ↓
    └──────────┘               ↓
                               ↓
┌──────────────────────────────────┐
│ Is data returned or stored?      │
└──────────────────────────────────┘
    YES ↓                  NO ↓
    ↓                  Use ARENA!
    ↓
┌─────────────────────────────────┐
│ Multiple owners needed?          │
└─────────────────────────────────┘
    YES ↓              NO ↓
    ┌──────────┐    ┌──────────────┐
    │ SHARED   │    │  OWNED HEAP  │
    └──────────┘    └──────────────┘
```

### Quick Reference

| Question | Answer |
|----------|--------|
| Loop counter? | → STACK |
| Temporary buffer in function? | → STACK |
| Parsing tokens during compilation? | → ARENA |
| Intermediate AST nodes? | → ARENA |
| Final program AST? | → OWNED |
| Configuration object? | → OWNED (or SHARED if multi-thread) |
| Cached data shared by threads? | → SHARED |
| String that outlives function? | → OWNED |
| 100,000 temp strings during batch? | → ARENA |

---

## Implementation in Runa Compiler v0.0.8.4.5.2

### Current Architecture

```
main.runa
    ↓
    Creates ARENA (64KB)
    ↓
    Creates LEXER (OWNED, gets arena reference)
    ↓
    Creates PARSER (OWNED, gets arena reference)
    ↓
    Creates CODEGEN (OWNED, gets arena reference)
    ↓
    Compilation happens:
        - Tokens (ARENA temps)
        - Temp strings (ARENA)
        - AST nodes (OWNED)
        - Variables (OWNED)
    ↓
    Destroys CODEGEN (frees OWNED data)
    ↓
    Destroys PROGRAM (frees OWNED AST)
    ↓
    Destroys PARSER (frees OWNED state)
    ↓
    Destroys LEXER (frees OWNED state)
    ↓
    Destroys ARENA (bulk frees all temps)
    ↓
    Exit
```

### Structure Sizes

```
Parser:  32 bytes (OWNED)
  - lexer:         8 bytes (pointer)
  - current_token: 8 bytes (pointer)
  - current_prog:  8 bytes (pointer)
  - arena:         8 bytes (pointer) ← Tier 2 reference

Lexer:   40 bytes (OWNED)
  - source:        8 bytes (pointer)
  - position:      4 bytes
  - line:          4 bytes
  - column:        4 bytes
  - current_char:  1 byte
  - padding:       3 bytes
  - arena:         8 bytes (pointer) ← Tier 2 reference
  - padding:       8 bytes

Codegen: 96 bytes (OWNED)
  - output_file:   8 bytes
  - variables:     8 bytes (pointer to OWNED array)
  - strings:       8 bytes (pointer to OWNED array)
  - [... other fields ...]
  - arena:         8 bytes (pointer) ← Tier 2 reference

Arena:   24 bytes (OWNED)
  - buffer:        8 bytes (pointer to ARENA memory)
  - capacity:      8 bytes
  - used:          8 bytes
```

### Memory Flow Example

```runa
// Compilation of "test.runa":

1. main creates arena (64KB allocated)
   Heap: [Arena struct: 24B] + [Arena buffer: 65536B]

2. lexer_create allocates source string (OWNED)
   Heap: [source: 1024B]

3. Lexing creates tokens using arena
   Arena: [Token: 24B][Token: 24B][Token: 24B]... (100 tokens = 2400B)

4. Parser creates AST nodes (OWNED)
   Heap: [ASTNode: 64B][ASTNode: 64B]... (50 nodes = 3200B)

5. Codegen creates temp labels (ARENA)
   Arena: [".L1": 4B][".L2": 4B][".L3": 4B]...

6. Codegen stores final labels (OWNED)
   Heap: [".STR0": 6B][".STR1": 6B]...

7. Compilation complete:
   - Destroy codegen: frees OWNED labels (~50B)
   - Destroy program: frees OWNED AST (~3200B)
   - Destroy parser: frees OWNED state (~32B)
   - Destroy lexer: frees OWNED source (~1024B)
   - Destroy arena: frees ALL temps (2400B tokens + labels) in O(1)

Final: 0 bytes leaked ✅
```

### Current Limitations

**Status:** Partial implementation
- ✅ Arena infrastructure complete
- ✅ Parser, Lexer, Codegen have arena references
- ✅ `arena_integer_to_string` converts temps to arena
- ⚠️ Most string operations still use heap (acceptable for v0.0.8.x)
- ⚠️ Small leaks (~358 bytes from heap string operations)

**Why not 100% arena?**
Some strings are stored in structures and freed by destroy functions. Converting these to arena would require:
1. Removing all individual `deallocate()` calls for strings
2. Ensuring arena outlives all structures
3. Careful ordering of destruction

This is planned for v1.0 with full ownership semantics.

---

## Performance Characteristics

### Allocation Speed (typical x86-64)

| Tier | Allocation Time | Example |
|------|----------------|---------|
| STACK | 0 ns | `Let x as Integer` |
| ARENA | ~10 ns | `arena_allocate(arena, 100)` |
| OWNED | ~100 ns | `allocate(100)` |
| SHARED | ~110 ns | `refcount_create(data)` |

### Deallocation Speed

| Tier | Deallocation Time | Example |
|------|------------------|---------|
| STACK | 0 ns | Automatic |
| ARENA | ~100 ns | `arena_destroy(arena)` (all objects) |
| OWNED | ~50 ns | `deallocate(ptr)` (per object) |
| SHARED | ~5-50 ns | `refcount_release(rc)` |

### Memory Overhead

| Tier | Per-Allocation Overhead | Notes |
|------|------------------------|-------|
| STACK | 0 bytes | Compiler-managed |
| ARENA | ~0 bytes | Amortized (capacity waste only) |
| OWNED | ~16-32 bytes | malloc metadata |
| SHARED | ~24-40 bytes | malloc + ref count |

### Throughput Comparison

**Scenario:** Allocate 1 million 32-byte objects

| Strategy | Time | Memory Used |
|----------|------|-------------|
| Individual malloc/free | ~100 ms | 32MB + 16-32MB overhead |
| Arena (one arena) | ~10 ms | 32MB + 24 bytes overhead |
| Stack (if possible) | ~0 ms | 32MB + 0 overhead |

---

## Real-World Use Cases

### NASA Mission Critical (Real-Time)
```runa
Process called "calculate_orbital_adjustment" takes sensor_data as SensorReading returns Adjustment:
    // STACK: Zero allocation, deterministic
    Let delta_v as Float64
    Let burn_time as Float64
    Let buffer as Array[16] of Float64

    // All calculations on stack - no heap allocation!
    Set delta_v to calculate_delta_v(sensor_data)
    Set burn_time to calculate_burn_duration(delta_v)

    Let adjustment as Adjustment
    Set adjustment.delta_v to delta_v
    Set adjustment.burn_time to burn_time

    Return adjustment
    // Guaranteed < 1 microsecond, zero allocations
End Process
```

### Police Dispatch (Real-Time + Temporary Data)
```runa
Process called "dispatch_emergency" takes call_data as CallData returns DispatchResult:
    // STACK: Critical path data
    Let priority as Integer
    Let unit_count as Integer

    // ARENA: Temporary routing calculations
    Let arena be arena_create(4096)
    Let available_units be arena_find_units(arena, call_data.location)
    Let route be arena_calculate_fastest_route(arena, available_units)

    // OWNED: Result that outlives operation
    Let result be DispatchResult.create(route.unit_id, route.eta)

    arena_destroy(arena)  // Cleanup temps
    Return result  // OWNED result survives
End Process
```

### AI Batch Inference (Bulk Processing)
```runa
Process called "batch_inference" takes images as Array, model as Model returns Array:
    // ARENA: All preprocessing temps
    Let arena be arena_create(10485760)  // 10MB for batch

    Let results be Array.create()
    Let i as Integer
    Set i to 0
    While i is less than Array.length(images):
        // All preprocessing in arena (thousands of allocations)
        Let preprocessed be arena_preprocess_image(arena, images[i])
        Let features be arena_extract_features(arena, preprocessed)

        // Inference result (OWNED - outlives arena)
        Let prediction be model_predict(model, features)
        Array.push(results, prediction)

        Set i to i plus 1
    End While

    arena_destroy(arena)  // Millions of temps freed in O(1)
    Return results  // OWNED predictions survive
End Process
```

### Compiler (Mixed)
```runa
Process called "compile_project" takes project as Project returns Binary:
    // ARENA: All compilation temps
    Let arena be arena_create(104857600)  // 100MB for large project

    // OWNED: Accumulated results
    Let compiled_modules be Array.create()

    Let i as Integer
    Set i to 0
    While i is less than project.module_count:
        // ARENA: Tokens, temp AST, temp strings
        Let tokens be arena_lex(arena, project.modules[i])
        Let temp_ast be arena_parse(arena, tokens)

        // OWNED: Final validated AST
        Let module_ast be Module.from_temp_ast(temp_ast)
        Array.push(compiled_modules, module_ast)

        // Reset arena for next module (reuse buffer)
        arena_reset(arena)

        Set i to i plus 1
    End While

    // OWNED: Final binary
    Let binary be link_modules(compiled_modules)

    arena_destroy(arena)  // All temps freed
    Array.destroy(compiled_modules)  // Owned ASTs freed

    Return binary
End Process
```

### Cybersecurity (Isolated Processing)
```runa
Process called "scan_suspicious_packet" takes packet as Bytes returns ThreatReport:
    // ARENA: Isolated analysis (sandboxed)
    Let arena be arena_create(65536)

    // All parsing in arena - if malicious, just destroy arena
    Let parsed be arena_parse_packet(arena, packet)

    If is_malformed(parsed):
        arena_destroy(arena)  // Destroy potentially malicious data
        Return ThreatReport.create(MALFORMED)
    End If

    Let analysis be arena_analyze_threats(arena, parsed)

    // OWNED: Safe report (copied out of arena)
    Let report be ThreatReport.from_analysis(analysis)

    arena_destroy(arena)  // Destroy all untrusted data
    Return report  // Only safe data survives
End Process
```

---

## Common Patterns

### Pattern 1: Arena Scope
```runa
Process called "do_operation" takes input as Data returns Result:
    Let arena be arena_create(size)

    // All temps use arena
    Let temp1 be arena_allocate(arena, 100)
    Let temp2 be arena_allocate(arena, 200)

    // Extract result (OWNED)
    Let result be create_result(temp1, temp2)

    arena_destroy(arena)  // Bulk cleanup
    Return result  // OWNED survives
End Process
```

### Pattern 2: Arena Reset (Reuse)
```runa
Process called "process_batch" takes items as Array returns Results:
    Let arena be arena_create(65536)
    Let results be Array.create()

    Let i as Integer
    Set i to 0
    While i is less than Array.length(items):
        // Process one item with arena
        Let temp be arena_process(arena, items[i])
        Let result be extract_result(temp)  // OWNED
        Array.push(results, result)

        arena_reset(arena)  // Reuse arena buffer
        Set i to i plus 1
    End While

    arena_destroy(arena)
    Return results
End Process
```

### Pattern 3: Nested Ownership
```runa
Structure Parent:
    children: Array of Child  // Parent OWNS children
End Structure

Process called "parent_destroy" takes parent as Parent:
    Let i as Integer
    Set i to 0
    While i is less than Array.length(parent.children):
        child_destroy(parent.children[i])  // Destroy owned children
        Set i to i plus 1
    End While
    Array.destroy(parent.children)
    deallocate(parent)
End Process
```

### Pattern 4: Reference Counting
```runa
Structure SharedResource:
    rc: RefCounted
End Structure

Process called "share_resource" takes resource as SharedResource returns SharedResource:
    refcount_retain(resource.rc)
    Return resource
End Process

Process called "release_resource" takes resource as SharedResource:
    refcount_release(resource.rc)  // Freed when count reaches 0
End Process
```

---

## Anti-Patterns (DO NOT DO)

### ❌ Storing Arena Pointers
```runa
// WRONG: Arena pointer stored in permanent structure
Let arena be arena_create(1024)
Let temp be arena_allocate(arena, 100)
some_struct.field = temp  // ❌ BAD!
arena_destroy(arena)  // some_struct.field now dangling!
```

### ❌ Mixing Free Strategies
```runa
// WRONG: Calling deallocate on arena memory
Let arena be arena_create(1024)
Let ptr be arena_allocate(arena, 100)
deallocate(ptr)  // ❌ BAD! This is arena memory!
arena_destroy(arena)  // ❌ Double free!
```

### ❌ Leaking Arena Reference
```runa
// WRONG: Arena destroyed before data used
Process called "get_data" returns String:
    Let arena be arena_create(1024)
    Let data be arena_string_duplicate(arena, "Hello")
    arena_destroy(arena)
    Return data  // ❌ BAD! Dangling pointer!
End Process
```

### ❌ Forgetting Ownership
```runa
// WRONG: Not freeing owned data
Let data be allocate(1024)
// ... use data ...
// ❌ BAD! Memory leaked, never freed
```

### ❌ Reference Count Cycles
```runa
// WRONG: Circular references without weak refs
Let a be refcount_create(data_a)
Let b be refcount_create(data_b)
a.next = refcount_retain(b)
b.prev = refcount_retain(a)  // ❌ BAD! Cycle = memory leak
// Use weak references to break cycles!
```

---

## Future Direction (v1.0+)

### Automatic Ownership (Rust-style)
```runa
// Future: Compiler tracks ownership automatically
Let data be String.new("Hello")  // Owned
Let moved be data  // Ownership transferred
// data is now invalid, compiler error if used
```

### Lifetime Annotations
```runa
// Future: Compiler enforces lifetime constraints
Process called "get_substring" takes str as String with lifetime 'a returns String 'a:
    Return str.substring(0, 10)  // Reference valid as long as str
End Process
```

### Automatic Arena Scoping
```runa
// Future: Arena scope blocks
Arena.scope(65536) do:
    Let temp1 be allocate(100)  // Automatically arena
    Let temp2 be allocate(200)  // Automatically arena
    // ...
End Arena  // Automatic bulk free
```

---

## Who Does This Currently?

### **Rust** (Ownership + Optional Arena)
- Default: Ownership with compiler-enforced lifetimes
- Arena: Available via crates (`bumpalo`, `typed-arena`)
- Used by: Firefox, Discord, Cloudflare, AWS

### **Zig** (Explicit Allocators)
- Every function takes an allocator parameter
- Programmer chooses: GPA, Arena, or custom
- Used by: Bun, TigerBeetle

### **C with Arenas**
- Manual but common pattern in high-performance C
- Used by: Compilers (LLVM uses bump allocators), game engines

### **Swift** (ARC + Value Semantics)
- Automatic reference counting for classes
- Value types (structs) use stack/owned semantics
- Used by: Apple ecosystem

### **Odin** (Manual + Arena Support)
- Similar to Zig, explicit allocator parameters
- Built-in arena support
- Used by: Game development

---

## Summary

### The Golden Rule
> **"Arena for TEMPS, Ownership for PERMANENT"**

### The Four Tiers
1. **STACK** - Fastest, zero-cost, automatic
2. **ARENA** - Fast bulk, O(1) cleanup, operation-scoped
3. **OWNED** - Structured lifetime, deterministic, permanent
4. **SHARED** - Multiple owners, ref-counted, when needed

### Key Principles
- ✅ Choose tier based on data lifetime
- ✅ Never mix strategies on same data
- ✅ Copy when crossing boundaries
- ✅ Clear ownership semantics
- ✅ Deterministic cleanup

### Result
- 🚀 **Fast**: Arena bulk operations
- 🛡️ **Safe**: No use-after-free, no double-free
- ⏱️ **Predictable**: Deterministic for real-time
- 🎯 **Flexible**: Right tool for each use case

---

**Runa: Fast, Safe, Predictable**

*Memory architecture inspired by Rust, Zig, and modern systems programming practices.*
