# Compiler-Based Ownership and Borrow Tracking Implementation Plan

**Version**: 1.0
**Target**: Runa Compiler v0.1.0+
**Status**: Planning Phase
**Dependencies**: Semantic Analyzer, Type System

---

## Executive Summary

This document outlines the implementation plan for compile-time ownership and borrow tracking in the Runa compiler. While runtime validation primitives (allocation registry, `BorrowedRef`, `validate_borrow_lifetime()`) provide safety nets for debugging and dynamic scenarios, the compiler must enforce ownership rules statically to prevent bugs before code execution.

**Key Distinction:**
- **Runtime Primitives** (✅ Implemented in v0.0.8.5): Catch bugs at runtime, useful for debugging and FFI
- **Compiler Tracking** (❌ Not Yet Implemented): Prevent bugs at compile-time, guarantees safety

---

## Motivation

### Why Compile-Time Tracking?

From the Runa Language Specification (Section 6: Semantic Analysis):

```runa
Note: Ownership transfer validation
Process called "transfer_ownership" that takes data as List[String]):
    processor.take_ownership(data)  Note: data ownership transferred
    Display length of data  Note: Error: data no longer owned
```

The `Note: Error: data no longer owned` indicates **compile-time rejection** - the code never runs.

### Runtime vs Compile-Time

| Feature | Runtime Primitives | Compiler Tracking |
|---------|-------------------|------------------|
| **When** | During execution | During compilation |
| **Purpose** | Safety net, debugging | Prevent bugs entirely |
| **Coverage** | Best-effort detection | Exhaustive analysis |
| **Use Cases** | FFI, dynamic code, debugging | All safe Runa code |
| **Performance** | Runtime overhead | Zero runtime cost |

---

## Design Goals

1. **Memory Safety**: Prevent use-after-free, double-free, and dangling pointers
2. **Zero Runtime Cost**: All checks performed at compile-time
3. **Clear Error Messages**: Help developers understand ownership violations
4. **Gradual Adoption**: Allow opt-out for FFI and unsafe code blocks
5. **Rust-Inspired**: Learn from proven borrow checker design
6. **Runa-Adapted**: Fit Runa's natural language syntax and type system

---

## Core Concepts

### 1. Ownership Rules

**Rule 1: Single Owner**
- Each value has exactly one owner at a time
- When owner goes out of scope, value is deallocated

**Rule 2: Transfer of Ownership**
- Assignment and function calls transfer ownership (move semantics)
- Original variable becomes invalid after transfer

**Rule 3: Borrowing**
- References allow temporary access without ownership
- Borrows must not outlive the owner

**Rule 4: Mutability Exclusion**
- Either multiple immutable borrows OR one mutable borrow
- Never both simultaneously

### 2. Reference Types

```runa
Type RefType:
    Case Owned          Note: Exclusive ownership, can move
    Case SharedImmutable Note: Multiple readers allowed
    Case SharedMutable   Note: Exclusive write access (requires synchronization)
    Case Borrowed(lifetime) Note: Temporary access, tied to owner lifetime
    Case Moved          Note: Ownership transferred, use is error
```

### 3. Lifetime Tracking

```runa
Note: Lifetime parameters (similar to Rust)
Process called "get_first_element"[L1, L2]
    that takes data as List[String] with lifetime L1
    returns Reference[String] with lifetime L2
    where L2 is less than or equal to L1:

    Note: Return type lifetime L2 must not outlive parameter lifetime L1
    If length of data is greater than 0:
        Return reference to data[0]  Note: Valid: L2 <= L1
    Otherwise:
        Return reference to ""  Note: Error: string literal lifetime < L1
```

---

## Implementation Phases

### Phase 1: Ownership Tracking (4-6 weeks)

**Goal**: Track ownership state for all variables

**Components:**
1. **Symbol Table Extension**
   - Add `ownership_state` field to variable entries
   - Track: `Owned`, `Moved`, `Borrowed`, `Shared`

2. **Move Semantics**
   - Detect ownership transfers in assignments
   - Mark moved variables as invalid
   - Generate errors on use-after-move

3. **Scope Analysis**
   - Track variable lifetimes through scopes
   - Insert automatic deallocation at scope exit
   - Validate ownership at scope boundaries

**Example Error Messages:**
```
Error: Use of moved value
  --> example.runa:5:12
   |
 3 |     Let data be create_list()
   |         ---- value created here
 4 |     process_data(data)
   |                  ---- value moved here
 5 |     Display data
   |             ^^^^ value used after move
   |
   = note: consider cloning the value if you need to use it after transfer
```

### Phase 2: Borrow Checking (6-8 weeks)

**Goal**: Enforce borrow rules and prevent aliasing violations

**Components:**
1. **Borrow Tracking**
   - Track active borrows for each variable
   - Distinguish mutable vs immutable borrows
   - Validate borrow exclusivity rules

2. **Lifetime Inference**
   - Infer lifetimes for local references
   - Propagate lifetime constraints through function calls
   - Validate lifetime relationships

3. **Alias Analysis**
   - Detect potential aliasing violations
   - Prevent simultaneous mutable and immutable access
   - Track reference chains

**Example Validation:**
```runa
Process called "example":
    Let mutable data be create_list()

    Let ref1 be reference to data      Note: Immutable borrow
    Let ref2 be reference to data      Note: OK - multiple immutable borrows

    Let mutable_ref be mutable reference to data
    Note: ERROR - cannot borrow as mutable while immutable borrows exist
```

### Phase 3: Lifetime Parameters (8-10 weeks)

**Goal**: Support explicit lifetime annotations for complex scenarios

**Components:**
1. **Lifetime Syntax**
   - Parse lifetime parameters in function signatures
   - Support lifetime bounds and constraints
   - Allow explicit lifetime annotations

2. **Lifetime Checking**
   - Validate lifetime parameter usage
   - Check lifetime bounds at call sites
   - Ensure returned references don't outlive inputs

3. **Lifetime Elision**
   - Infer simple lifetime relationships
   - Apply elision rules for common patterns
   - Reduce annotation burden

**Example:**
```runa
Note: Explicit lifetime parameters
Process called "select_longer"[L1, L2, L3]
    that takes s1 as String with lifetime L1,
               s2 as String with lifetime L2
    returns String with lifetime L3
    where L3 is less than or equal to L1,
          L3 is less than or equal to L2:

    If length of s1 is greater than length of s2:
        Return s1  Note: Valid - L3 <= L1
    Otherwise:
        Return s2  Note: Valid - L3 <= L2
```

### Phase 4: Advanced Features (6-8 weeks)

**Goal**: Handle complex ownership patterns

**Components:**
1. **Interior Mutability**
   - Support for reference-counted mutable containers
   - Cell/RefCell equivalents for controlled mutation
   - Runtime borrow checking for dynamic scenarios

2. **Partial Moves**
   - Allow moving individual fields from structs
   - Track field-level ownership
   - Support for destructuring with moves

3. **Copy Types**
   - Identify types safe to copy (primitives, small values)
   - Implicit copying for Copy types
   - Explicit cloning for non-Copy types

4. **Drop/Destructor Integration**
   - Call destructors when ownership ends
   - Validate destructor safety
   - Support for custom cleanup logic

### Phase 5: FFI and Unsafe Code (4-6 weeks)

**Goal**: Integrate with foreign code safely

**Components:**
1. **Unsafe Blocks**
   - Opt-out of ownership checking
   - Clear boundary between safe and unsafe
   - Documentation requirements for unsafe

2. **FFI Ownership Annotations**
   - `owned`, `borrowed`, `shared` annotations for C functions
   - Automatic conversion at FFI boundaries
   - Validation of ownership contracts

3. **Raw Pointer Support**
   - Raw pointers bypass ownership system
   - Only allowed in unsafe blocks
   - Tools for safe conversion to/from references

**Example:**
```runa
External Process called "c_take_ownership"
    takes data as String[owned]    Note: C takes ownership, will free
    returns Integer

External Process called "c_borrow_string"
    takes data as String[borrowed] Note: C borrows, Runa retains ownership
    returns Integer

Process called "ffi_example":
    Let data be "hello"

    Let result1 be c_borrow_string(data)  Note: OK - borrowed
    Display data                          Note: OK - still owned

    Let result2 be c_take_ownership(data) Note: OK - ownership transferred
    Display data                          Note: ERROR - data no longer owned
```

### Phase 6: Integration and Testing (4-6 weeks)

**Goal**: Integrate with compiler pipeline and validate

**Components:**
1. **Error Recovery**
   - Graceful handling of ownership errors
   - Continue analysis after errors
   - Suggest fixes for common violations

2. **Test Suite**
   - Comprehensive ownership violation tests
   - Edge cases and complex scenarios
   - Regression testing

3. **Documentation**
   - User guide for ownership system
   - Migration guide from untracked code
   - Best practices and patterns

---

## Technical Architecture

### Compiler Pipeline Integration

```
┌─────────────────┐
│  Lexer/Parser   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Type Checker  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌──────────────────┐
│ Ownership       │────▶│ Borrow Checker   │
│ Analyzer        │     │                  │
└────────┬────────┘     └──────────────────┘
         │
         ▼
┌─────────────────┐
│   Code Gen      │
└─────────────────┘
```

### Data Structures

**Ownership Graph:**
```runa
Type OwnershipGraph:
    Contains variables as Map[VariableId, OwnershipState]
    Contains borrows as List[BorrowEdge]
    Contains lifetimes as Map[LifetimeId, LifetimeInfo]

Type OwnershipState:
    Case Owned
    Case Moved(location as SourceLocation)
    Case Borrowed(count as Integer, mutable as Boolean)
    Case Invalid

Type BorrowEdge:
    Contains borrower as VariableId
    Contains owner as VariableId
    Contains lifetime as LifetimeId
    Contains is_mutable as Boolean
```

**Lifetime Constraints:**
```runa
Type LifetimeConstraint:
    Case Outlives(longer as LifetimeId, shorter as LifetimeId)
    Case Equal(l1 as LifetimeId, l2 as LifetimeId)
    Case StaticLifetime(l as LifetimeId)
```

---

## Relationship to Runtime Primitives

### Runtime Primitives (v0.0.8.5 - Already Implemented)

Located in `memory/layout.runa` and `memory/references.runa`:

1. **Allocation Registry**
   - Global hash table tracking all allocations
   - Generation counters for use-after-realloc detection
   - Liveness tracking for use-after-free detection

2. **BorrowedRef Structure**
   - 32-byte structure wrapping borrowed pointers
   - Contains: data_ptr, owner_alloc_id, owner_generation, offset

3. **Runtime Validation Functions**
   - `validate_borrow_lifetime()` - Full 7-step validation
   - `borrowed_is_valid()` - Check if allocation is still valid
   - `get_reference_type()` - Query allocation type from registry

### Division of Responsibility

| Scenario | Compiler Tracking | Runtime Primitives |
|----------|------------------|-------------------|
| **Safe Runa Code** | Prevents all violations | Not needed (zero overhead) |
| **Unsafe Blocks** | Warnings only | Catches violations at runtime |
| **FFI Boundaries** | Validates contracts | Validates actual pointers |
| **Debug Builds** | Full analysis | Additional runtime checks |
| **Release Builds** | Full analysis | Minimal/optional checks |
| **Dynamic Code** | Cannot analyze | Essential safety net |

### Integration Points

1. **Debug Mode**: Compiler inserts runtime validation calls even for safe code
2. **Unsafe Blocks**: Compiler suggests runtime validation functions
3. **FFI**: Automatic conversion between compiler tracking and runtime structures
4. **Testing**: Runtime primitives validate compiler analysis correctness

---

## Success Criteria

### Phase 1 Complete When:
- [ ] All ownership transfers are tracked
- [ ] Use-after-move errors are detected
- [ ] 90% of simple ownership bugs caught

### Phase 2 Complete When:
- [ ] Borrow exclusivity rules enforced
- [ ] Aliasing violations detected
- [ ] 95% of borrow-related bugs caught

### Phase 3 Complete When:
- [ ] Lifetime parameters fully supported
- [ ] Complex borrowing patterns work
- [ ] Error messages are clear and actionable

### Full System Complete When:
- [ ] All test cases pass
- [ ] Performance overhead < 5% compile time
- [ ] Zero false positives in test suite
- [ ] Documentation complete
- [ ] Migration guide available

---

## Open Questions

1. **Granularity**: Field-level vs struct-level ownership tracking?
2. **Performance**: Trade-offs between precision and compile-time overhead?
3. **Opt-Out**: Per-function, per-module, or per-file unsafe annotations?
4. **Diagnostics**: How to explain complex lifetime errors clearly?
5. **Backwards Compatibility**: Migration path for existing code?

---

## References

1. **Runa Language Specification**: `docs/user/language-specification/runa_language_specification.md`
2. **Rust Borrow Checker**: [The Rust Reference - Borrow Checking](https://doc.rust-lang.org/reference/borrow-checking.html)
3. **Runtime Primitives**: `runa/bootstrap/v0.0.8.5/compiler/frontend/primitives/memory/`
4. **Allocation Registry Design**: `docs/dev/allocation_registry_and_borrow_validation_plan.md`

---

## Timeline Summary

| Phase | Duration | Key Deliverable |
|-------|----------|----------------|
| 1. Ownership Tracking | 4-6 weeks | Move semantics working |
| 2. Borrow Checking | 6-8 weeks | Aliasing prevention |
| 3. Lifetime Parameters | 8-10 weeks | Complex borrows supported |
| 4. Advanced Features | 6-8 weeks | Interior mutability, Copy types |
| 5. FFI/Unsafe | 4-6 weeks | Safe foreign function calls |
| 6. Integration | 4-6 weeks | Production-ready system |
| **Total** | **32-44 weeks** | **Complete ownership system** |

---

## Conclusion

Compile-time ownership and borrow tracking will make Runa a memory-safe language with zero runtime overhead for safe code. The runtime primitives implemented in v0.0.8.5 provide the foundation for debugging and dynamic scenarios, while the compiler will prevent bugs before they can occur.

This is a substantial undertaking (8-11 months), but the result will be a language that combines the safety of Rust with Runa's natural language syntax and AI-first design philosophy.
