# Runa Memory Automation Roadmap
**Version:** 1.0
**Status:** Planning Document
**Target:** v1.0 and beyond

---

## Overview

This document outlines the roadmap for automating Runa's memory management through language features, compiler improvements, and ARC (Automatic Reference Counting) implementation.

**Goal:** Transform Runa from manual memory management (current) to mostly-automatic memory management (future) while maintaining **100% real-time safety** and **deterministic behavior**.

---

## Current State (v0.0.8.5)

### What Works
- ✅ **Tier 1 (Stack)**: 100% automatic
- ✅ **Tier 2 (Arena)**: Infrastructure complete, manual arena lifecycle
- ✅ **Tier 3 (Owned)**: Manual allocate/deallocate
- ✅ **Tier 4 (Shared)**: Manual refcount_create/retain/release
- ❌ **Tier 5 (ARC)**: Not implemented

### Current Pain Points
```runa
Note: Manual memory management (v0.0.8.5)
Let program be allocate(32)  // Manual allocation
memory_set_pointer(program, 0, name_copy)  // Manual field setting
deallocate(program)  // Manual deallocation (easy to forget!)
```

**Problems:**
- Easy to forget `deallocate()` → memory leaks
- Easy to double-free → crashes
- Easy to use-after-free → undefined behavior
- Tedious refcount management

---

## Automation Roadmap

### Phase 1: Language Features (v0.9 - v1.0)
**Target:** 6-12 months
**Goal:** Add high-level language constructs that enable automation

#### 1.1 Constructors and Destructors

**Status:** Planned for v0.9

```runa
Note: Future - Constructors
Type called "Program":
    name as String
    functions as Array of Function

    Note: Constructor (automatic allocation)
    Process called "new" that takes program_name as String returns Program:
        Let prog be allocate(sizeof(Program))
        Set prog.name to string_duplicate(program_name)
        Set prog.functions to Array.new()
        Return prog
    End Process

    Note: Destructor (automatic deallocation)
    Process called "destroy" takes self as Program:
        deallocate(self.name)
        Array.destroy(self.functions)
        deallocate(self)
    End Process
End Type

Note: User code becomes simple
Let program be Program.new("MyProgram")
// ... use program ...
// Compiler automatically calls program.destroy() at scope end!
```

**Benefits:**
- ✅ Compiler automatically calls destructor
- ✅ No more forgotten deallocations
- ✅ RAII (Resource Acquisition Is Initialization) pattern
- ✅ Still deterministic (scope-based)

**Implementation:**
- Parser: Add constructor/destructor syntax
- Semantic analyzer: Track object lifetimes
- Codegen: Insert destructor calls at scope end

#### 1.2 Move Semantics (Ownership Transfer)

**Status:** Planned for v1.0

```runa
Note: Automatic ownership transfer
Process called "take_ownership" takes data as owned Program returns Nothing:
    // 'data' is moved, caller can no longer use it
    // Compiler tracks this!
End Process

Let prog be Program.new("Test")
take_ownership(prog)
// prog is now INVALID - compiler error if you try to use it!
```

**Benefits:**
- ✅ Compiler prevents use-after-move
- ✅ No runtime overhead
- ✅ Rust-style safety

#### 1.3 Borrow Checking

**Status:** Planned for v1.0

```runa
Note: Temporary references (no ownership transfer)
Process called "read_name" takes prog as borrowed Program returns String:
    Return prog.name  // Can read, cannot modify ownership
End Process

Let prog be Program.new("Test")
Let name be read_name(prog)  // prog still valid!
// Compiler ensures prog outlives the borrow
```

**Benefits:**
- ✅ Safe temporary access
- ✅ No ownership transfer overhead
- ✅ Compiler-verified safety

---

### Phase 2: ARC Implementation (v1.0 - v1.2)
**Target:** v1.0 (12-18 months)
**Goal:** Tier 5 (ARC) fully implemented

#### 2.1 Basic ARC Infrastructure

**Milestone:** v1.0

**Components:**
1. **Refcount Metadata:**
   - Add refcount field to ARC-allocated objects
   - Atomic increment/decrement operations
   - Thread-safe refcount management

2. **Compiler Analysis:**
   - Track ARC-annotated types
   - Insert retain calls on assignment
   - Insert release calls at scope end
   - Optimize redundant retain/release pairs

3. **Syntax:**
```runa
Note: ARC annotation on types
Type called "Config" with annotation @ARC:
    database_url as String
    api_key as String
End Type

Note: ARC annotation on variables
Let config as @ARC be Config.new()
Let copy be config  // Compiler inserts: refcount_retain(config)
// Scope end: Compiler inserts: refcount_release(config), refcount_release(copy)
```

**Implementation Steps:**
1. Add `@ARC` annotation to parser
2. Modify type system to track ARC types
3. Add refcount metadata to heap allocations
4. Implement retain/release insertion pass
5. Add optimization pass to eliminate redundant retain/release

#### 2.2 Weak References

**Milestone:** v1.1

```runa
Type called "Node" with annotation @ARC:
    value as Integer
    next as Node          // Strong reference
    prev as weak Node     // Weak reference (no refcount increment)
End Type
```

**Implementation:**
- Add `weak` keyword
- Track weak vs strong references in type system
- Weak references don't increment refcount
- Weak references become null when object is freed

#### 2.3 ARC Optimizations

**Milestone:** v1.2

**Optimizations:**
1. **Redundant Retain/Release Elimination:**
```runa
Let x as @ARC be MyClass.new()
Let y be x  // Retain
Set y to x  // Redundant retain (same value!)
// Compiler optimizes: only one retain
```

2. **Scope Lifetime Extension:**
```runa
Process called "foo":
    Let x as @ARC be MyClass.new()
    // No intermediate retain/release if x never escapes
    Return x  // Only retain/release at return
End Process
```

3. **Static Analysis:**
   - Detect non-escaping ARC objects → convert to Owned
   - Detect single-owner ARC objects → convert to Owned
   - Warn on potential cycles

---

### Phase 3: Advanced Automation (v1.5+)
**Target:** v1.5+ (18-24 months)

#### 3.1 Automatic Tier Selection

**Goal:** Compiler chooses optimal tier automatically

```runa
Note: Future - Compiler auto-selects tier
Let temp be "Hello"  // Compiler: Stack (fits, short-lived)
Let data be parse_file("big.txt")  // Compiler: Arena (temp, bulk)
Let config be Config.load()  // Compiler: Owned (permanent, single owner)
Let shared be load_shared_resource()  // Compiler: ARC (multiple owners detected)
```

**Implementation:**
- Escape analysis: Does value escape function?
- Lifetime analysis: How long does value live?
- Sharing analysis: Multiple owners?

#### 3.2 Arena Scope Blocks

```runa
Note: Automatic arena management
With Arena of size 1048576:
    Let tokens be tokenize(source)  // Automatic arena allocation
    Let ast be parse(tokens)  // Automatic arena allocation

    Let program be extract_program(ast)  // Owned (escapes arena)
End Arena  // Automatic arena destruction

// program survives, tokens/ast freed
```

#### 3.3 Lifetime Annotations (Rust-style)

```runa
Note: Explicit lifetime constraints
Process called "get_first"
    takes list as List with lifetime 'a
    returns String with lifetime 'a:

    Return list.get(0)  // Compiler ensures returned ref lives as long as list
End Process
```

---

## Implementation Timeline

```
v0.9 (6 months):
  - Constructors/destructors
  - Basic scope-based destruction
  - Move semantics (basic)

v1.0 (12 months):
  - ARC infrastructure (Tier 5)
  - Basic retain/release insertion
  - Weak references
  - Borrow checking (basic)

v1.1 (15 months):
  - ARC optimizations
  - Cycle detection warnings
  - Improved escape analysis

v1.2 (18 months):
  - Advanced ARC optimizations
  - Static single-owner detection
  - Better compiler diagnostics

v1.5 (24 months):
  - Automatic tier selection
  - Arena scope blocks
  - Lifetime annotations
  - Full Rust-level safety
```

---

## Automation Levels by Version

### v0.0.8.5 (Current)
```
Tier 1: Stack      - 100% automatic ✅
Tier 2: Arena      - Manual lifecycle (create/destroy)
Tier 3: Owned      - Fully manual (allocate/deallocate)
Tier 4: Shared     - Fully manual (retain/release)
Tier 5: ARC        - Not implemented ❌
```

### v0.9
```
Tier 1: Stack      - 100% automatic ✅
Tier 2: Arena      - Manual lifecycle (create/destroy)
Tier 3: Owned      - Automatic destruction ✅ (destructors)
Tier 4: Shared     - Manual (retain/release)
Tier 5: ARC        - Not implemented ❌
```

### v1.0
```
Tier 1: Stack      - 100% automatic ✅
Tier 2: Arena      - Manual lifecycle (create/destroy)
Tier 3: Owned      - Automatic destruction ✅ (destructors)
Tier 4: Shared     - Manual (retain/release)
Tier 5: ARC        - 99% automatic ✅ (compiler inserts retain/release)
```

### v1.5+
```
Tier 1: Stack      - 100% automatic ✅
Tier 2: Arena      - 95% automatic ✅ (scope blocks)
Tier 3: Owned      - 100% automatic ✅ (with borrow checking)
Tier 4: Shared     - Manual (expert control)
Tier 5: ARC        - 99% automatic ✅
+ Compiler auto-selects tier ✅
```

---

## Success Metrics

### Developer Experience
- **v0.9:** 70% less manual memory management (destructors)
- **v1.0:** 90% less manual memory management (ARC)
- **v1.5:** 95% less manual memory management (auto tier selection)

### Safety
- **v0.9:** No use-after-free (scope-based destruction)
- **v1.0:** No use-after-free, no double-free (ARC + borrow checking)
- **v1.5:** Memory safety guaranteed by compiler (Rust-level)

### Performance
- **All versions:** Zero GC pauses (real-time safe)
- **All versions:** Deterministic behavior
- **v1.0+:** ARC overhead < 5% vs manual (optimizations)

---

## Risk Mitigation

### Risk: ARC Performance Overhead
**Mitigation:**
- Optimize redundant retain/release away
- Allow fallback to manual Tier 4 for critical paths
- Profile-guided optimization

### Risk: Complexity
**Mitigation:**
- Phased rollout (v0.9 → v1.0 → v1.5)
- Clear documentation and examples
- Gradual migration path

### Risk: Breaking Changes
**Mitigation:**
- Maintain backward compatibility
- New features are opt-in (annotations)
- Deprecation warnings, not errors

---

## Decision Points

### When to Implement ARC?
**Decision:** v1.0
**Rationale:**
- Need destructors first (v0.9) as foundation
- ARC builds on destructor infrastructure
- Allows testing with real codebases before ARC

### Full GC Later?
**Decision:** No, never
**Rationale:**
- Breaks real-time guarantee
- ARC handles 99% of convenience use cases
- Tier 1-5 cover all needs without GC

---

## Summary

**Current (v0.0.8.5):**
- Mostly manual memory management
- Arena helps with bulk temps
- Tedious but functional

**v0.9 (Destructors):**
- Automatic cleanup for Tier 3 (Owned)
- 70% automation

**v1.0 (ARC):**
- Tier 5 available for convenience
- 90% automation
- Still 100% real-time safe

**v1.5+ (Full Automation):**
- Compiler chooses optimal tier
- 95%+ automation
- Rust-level safety

**Result:**
- Fast (real-time safe, deterministic)
- Safe (compiler-verified)
- Easy (mostly automatic)

---

**Runa: Fast, Safe, Easy - Pick All Three**

*Roadmap subject to change based on community feedback and real-world usage.*
