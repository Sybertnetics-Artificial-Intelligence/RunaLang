# Manual ARC (Automatic Reference Counting) - Production Guide

**Version**: v0.0.8.5
**Status**: Production-Ready
**Last Updated**: 2025-10-26

---

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [API Reference](#api-reference)
4. [Memory Management Fundamentals](#memory-management-fundamentals)
5. [Best Practices](#best-practices)
6. [Common Patterns](#common-patterns)
7. [Debugging and Leak Detection](#debugging-and-leak-detection)
8. [Performance Optimization](#performance-optimization)
9. [Migration to Automatic ARC](#migration-to-automatic-arc)
10. [Troubleshooting](#troubleshooting)

---

## Overview

### What is Manual ARC?

**Manual ARC (Automatic Reference Counting)** is Runa's production-ready memory management system that provides:

- **Memory Safety**: No manual `free()` calls - objects are deallocated automatically when refcount reaches 0
- **Shared Ownership**: Multiple references can safely own the same object
- **Cycle Prevention**: Weak references break reference cycles
- **Thread-Safety**: Atomic reference counting operations
- **Zero Overhead**: Direct delegation to Tier 4 (SHARED) infrastructure
- **Production-Ready**: Complete implementation with zero technical debt

### Manual vs Automatic ARC

| Feature | Manual ARC (v0.0.8.5) | Automatic ARC (Future) |
|---------|----------------------|------------------------|
| **Retain/Release** | Explicit `arc_retain()` and `arc_release()` | Compiler-inserted automatically |
| **Dependencies** | None - works now | Requires IR/Gungnir (MIR layer) |
| **Control** | Full developer control | Compiler-managed |
| **Migration** | N/A | Drop-in replacement for Manual ARC |
| **Performance** | Identical | Identical |
| **Use Case** | Production use today | Future convenience |

**Manual ARC provides 80% of ARC value** (memory safety, shared ownership) while being implementable immediately without IR dependencies.

### When to Use Manual ARC

**Use Manual ARC when:**
- You need shared ownership (multiple references to same object)
- Object lifetime is complex and cannot be determined statically
- You are building data structures with multiple owners (graphs, caches, etc.)
- Thread-safe reference counting is required

**Use Other Memory Tiers when:**
- **STACK**: Object lifetime is lexically scoped (most local variables)
- **ARENA**: Bulk allocation/deallocation (parser AST, batch processing)
- **OWNED**: Single ownership with explicit transfer (unique pointers)

---

## Quick Start

### Basic Usage

```runa
Import "runtime/core/memory/arc_heap.runa" as ARC
Import "runtime/stdlib/arc/arc_utils.runa" as ARCUtils

Process called "quick_start_example" returns Integer:
    Note: Reset statistics for clean measurement
    proc arc_stats_reset from ARCUtils

    Note: Allocate ARC-managed object (refcount = 1)
    Let obj be proc arc_allocate from ARC with 64

    Note: Use the object
    proc memory_set_int64 with obj, 0, 42

    Note: Release the reference (refcount = 0, object freed)
    proc arc_release from ARC with obj

    Note: Check for leaks
    If proc arc_assert_no_leaks from ARCUtils is equal to 0:
        Note: FAILURE - Memory leak detected
        Return 1
    End If

    Return 0  Note: Success
End Process
```

### Multiple References

```runa
Note: Create object
Let obj1 be proc arc_allocate from ARC with 64
proc memory_set_int64 with obj1, 0, 100

Note: Create second reference (refcount = 2)
Let obj2 be proc arc_retain from ARC with obj1

Note: obj1 and obj2 point to the same object
Note: Modifying through obj2 affects obj1

Note: Release first reference (refcount = 1, object still alive)
proc arc_release from ARC with obj1

Note: Object still alive because obj2 holds reference
Let value be proc memory_get_int64 with obj2, 0
Note: value = 100

Note: Release second reference (refcount = 0, object freed)
proc arc_release from ARC with obj2
```

### Weak References (Cycle Prevention)

```runa
Note: Create two objects
Let node_a be proc arc_allocate from ARC with 16
Let node_b be proc arc_allocate from ARC with 16

Note: Strong reference A -> B (A owns B)
Let b_retained be proc arc_retain from ARC with node_b
proc memory_set_int64 with node_a, 0, b_retained

Note: Weak reference B -> A (B does NOT own A, prevents cycle)
Let weak_a be proc arc_weak_create from ARC with node_a
proc memory_set_int64 with node_b, 8, weak_a

Note: To use weak reference, promote to strong
Let strong_a be proc arc_weak_promote from ARC with weak_a
If strong_a is not equal to 0:
    Note: Success - A is still alive
    proc arc_release from ARC with strong_a
Otherwise:
    Note: A was deallocated - weak reference is dead
End If

Note: Cleanup
proc arc_weak_release from ARC with weak_a
proc arc_release from ARC with node_b
proc arc_release from ARC with node_a
```

---

## API Reference

### Core Functions

#### `arc_allocate`

```runa
Process called "arc_allocate" takes size as Integer returns Integer
```

**Description**: Allocate ARC-managed memory

**Parameters**:
- `size` - Size in bytes to allocate

**Returns**:
- Pointer to allocated memory (refcount = 1)
- Returns 0 on allocation failure

**Example**:
```runa
Let obj be proc arc_allocate from ARC with 128
If obj is equal to 0:
    Note: Allocation failed
    Return 1
End If
```

**Notes**:
- Allocated memory is NOT zeroed (use `arc_allocate_zeroed` if needed)
- Initial refcount is 1 (caller owns the reference)
- Must call `arc_release` when done to avoid leaks

---

#### `arc_allocate_zeroed`

```runa
Process called "arc_allocate_zeroed" takes size as Integer returns Integer
```

**Description**: Allocate ARC-managed memory and initialize to zero

**Parameters**:
- `size` - Size in bytes to allocate

**Returns**:
- Pointer to zero-initialized memory (refcount = 1)
- Returns 0 on allocation failure

**Example**:
```runa
Let obj be proc arc_allocate_zeroed from ARC with 128
Note: All 128 bytes are guaranteed to be 0
```

**Notes**:
- Slightly slower than `arc_allocate` due to zeroing
- Useful for security-sensitive data or when initialization is required

---

#### `arc_retain`

```runa
Process called "arc_retain" takes ptr as Integer returns Integer
```

**Description**: Increment reference count (create new reference)

**Parameters**:
- `ptr` - Pointer to ARC object

**Returns**:
- Same pointer (for convenience)
- Returns 0 if `ptr` is invalid

**Example**:
```runa
Let obj1 be proc arc_allocate from ARC with 64  Note: refcount = 1
Let obj2 be proc arc_retain from ARC with obj1  Note: refcount = 2
Note: obj1 and obj2 point to same object
```

**Notes**:
- Thread-safe (uses atomic operations)
- Every `arc_retain` must be paired with `arc_release`
- Retaining increases refcount by 1

---

#### `arc_release`

```runa
Process called "arc_release" takes ptr as Integer returns Integer
```

**Description**: Decrement reference count (destroy reference)

**Parameters**:
- `ptr` - Pointer to ARC object

**Returns**:
- 1 if object still alive (refcount > 0)
- 0 if object was deallocated (refcount reached 0)

**Example**:
```runa
Let result be proc arc_release from ARC with obj
If result is equal to 0:
    Note: Object was deallocated
Otherwise:
    Note: Object still alive (other references exist)
End If
```

**Notes**:
- Thread-safe (uses atomic operations)
- Automatically deallocates when refcount reaches 0
- Do NOT use pointer after release returns 0

---

#### `arc_get_refcount`

```runa
Process called "arc_get_refcount" takes ptr as Integer returns Integer
```

**Description**: Get current reference count

**Parameters**:
- `ptr` - Pointer to ARC object

**Returns**:
- Current reference count
- Returns 0 if `ptr` is invalid

**Example**:
```runa
Let count be proc arc_get_refcount from ARC with obj
Note: count shows number of active references
```

**Notes**:
- For debugging only - do not make control flow decisions based on refcount
- In multi-threaded code, refcount may change immediately after reading

---

#### `arc_is_unique`

```runa
Process called "arc_is_unique" takes ptr as Integer returns Integer
```

**Description**: Check if reference is unique (enables copy-on-write optimization)

**Parameters**:
- `ptr` - Pointer to ARC object

**Returns**:
- 1 if refcount == 1 (unique reference, safe to mutate)
- 0 if refcount > 1 (shared, must clone before mutation)

**Example**:
```runa
If proc arc_is_unique from ARC with buffer is equal to 1:
    Note: Unique reference - safe to mutate in-place
    proc memory_set_int64 with buffer, 0, new_value
Otherwise:
    Note: Shared reference - must clone before mutation
    Let size be proc arc_get_size from ARC with buffer
    Let buffer_copy be proc arc_clone from ARC with buffer, size
    proc memory_set_int64 with buffer_copy, 0, new_value
    proc arc_release from ARC with buffer
    Set buffer to buffer_copy
End If
```

**Notes**:
- Critical for copy-on-write optimization
- Prevents accidental mutation of shared data
- Thread-safe

---

### Weak References

#### `arc_weak_create`

```runa
Process called "arc_weak_create" takes strong_ptr as Integer returns Integer
```

**Description**: Create weak reference (does NOT increment refcount)

**Parameters**:
- `strong_ptr` - Pointer to ARC object

**Returns**:
- Weak reference pointer
- Returns 0 on failure

**Example**:
```runa
Let strong be proc arc_allocate from ARC with 64
Let weak be proc arc_weak_create from ARC with strong
Note: strong refcount is still 1 (weak does not increment)
```

**Notes**:
- Weak references do NOT prevent deallocation
- Use to break reference cycles
- Must promote to strong reference before use

---

#### `arc_weak_release`

```runa
Process called "arc_weak_release" takes weak_ptr as Integer returns Integer
```

**Description**: Release weak reference

**Parameters**:
- `weak_ptr` - Weak reference pointer

**Returns**:
- 1 on success
- 0 if `weak_ptr` is invalid

**Example**:
```runa
proc arc_weak_release from ARC with weak
```

**Notes**:
- Does NOT affect strong refcount
- Always release weak references when done

---

#### `arc_weak_promote`

```runa
Process called "arc_weak_promote" takes weak_ptr as Integer returns Integer
```

**Description**: Promote weak reference to strong (increment refcount)

**Parameters**:
- `weak_ptr` - Weak reference pointer

**Returns**:
- Strong reference pointer (refcount incremented)
- Returns 0 if object was already deallocated

**Example**:
```runa
Let weak be proc arc_weak_create from ARC with strong
proc arc_release from ARC with strong  Note: May deallocate

Let promoted be proc arc_weak_promote from ARC with weak
If promoted is equal to 0:
    Note: Object was deallocated - weak reference is dead
Otherwise:
    Note: Success - promoted to strong reference
    Note: MUST call arc_release(promoted) when done
    proc arc_release from ARC with promoted
End If
```

**Notes**:
- Thread-safe
- Caller MUST release promoted strong reference
- Promotion may fail if object was deallocated

---

#### `arc_weak_is_alive`

```runa
Process called "arc_weak_is_alive" takes weak_ptr as Integer returns Integer
```

**Description**: Check if weak reference is still alive

**Parameters**:
- `weak_ptr` - Weak reference pointer

**Returns**:
- 1 if object is still alive
- 0 if object was deallocated

**Example**:
```runa
If proc arc_weak_is_alive from ARC with weak is equal to 1:
    Note: Safe to promote
    Let strong be proc arc_weak_promote from ARC with weak
    proc arc_release from ARC with strong
End If
```

**Notes**:
- Non-intrusive check (does not modify refcount)
- In multi-threaded code, object may be deallocated immediately after check

---

### Utility Functions

#### `arc_clone`

```runa
Process called "arc_clone" takes ptr as Integer, size as Integer returns Integer
```

**Description**: Create deep copy of ARC object

**Parameters**:
- `ptr` - Pointer to object to clone
- `size` - Size of object in bytes

**Returns**:
- Pointer to cloned object (refcount = 1)
- Returns 0 on failure

**Example**:
```runa
Let size be proc arc_get_size from ARC with original
Let copy be proc arc_clone from ARC with original, size
Note: copy is independent - modifying copy does not affect original
```

**Notes**:
- Performs shallow copy (copies bytes, not deep object graphs)
- Cloned object has independent refcount
- Useful for copy-on-write when `arc_is_unique` returns 0

---

#### `arc_get_size`

```runa
Process called "arc_get_size" takes ptr as Integer returns Integer
```

**Description**: Get allocation size of ARC object

**Parameters**:
- `ptr` - Pointer to ARC object

**Returns**:
- Size in bytes
- Returns 0 if `ptr` is invalid

**Example**:
```runa
Let size be proc arc_get_size from ARC with obj
Note: size is the original allocation size from arc_allocate
```

---

#### `arc_validate`

```runa
Process called "arc_validate" takes ptr as Integer returns Integer
```

**Description**: Validate ARC object for debugging

**Parameters**:
- `ptr` - Pointer to validate

**Returns**:
- 1 if object is valid
- 0 if object is invalid or corrupted

**Example**:
```runa
If proc arc_validate from ARC with obj is equal to 0:
    Note: ERROR - Object is corrupted or invalid
    Return 1
End If
```

**Notes**:
- For debugging only
- Checks allocation type, refcount sanity, header integrity

---

### Statistics and Debugging (arc_utils.runa)

#### `arc_stats_reset`

```runa
Process called "arc_stats_reset" returns Integer
```

**Description**: Reset ARC statistics to zero

**Returns**: 1 (always succeeds)

**Example**:
```runa
proc arc_stats_reset from ARCUtils
Note: Clean slate for profiling session
```

---

#### `arc_tracked_allocate`

```runa
Process called "arc_tracked_allocate" takes size as Integer returns Integer
```

**Description**: Allocate with statistics tracking

**Returns**: Pointer to allocated object (same as `arc_allocate`)

**Example**:
```runa
Let obj be proc arc_tracked_allocate from ARCUtils with 128
Note: Increments arc_total_allocations and arc_current_live_objects
```

---

#### `arc_tracked_retain`

```runa
Process called "arc_tracked_retain" takes ptr as Integer returns Integer
```

**Description**: Retain with statistics tracking

**Returns**: Same pointer (same as `arc_retain`)

**Example**:
```runa
Let obj2 be proc arc_tracked_retain from ARCUtils with obj1
Note: Increments arc_total_retains
```

---

#### `arc_tracked_release`

```runa
Process called "arc_tracked_release" takes ptr as Integer returns Integer
```

**Description**: Release with statistics tracking

**Returns**: 1 if alive, 0 if deallocated (same as `arc_release`)

**Example**:
```runa
proc arc_tracked_release from ARCUtils with obj
Note: Increments arc_total_releases and arc_total_deallocations
```

---

#### `arc_detect_leaks`

```runa
Process called "arc_detect_leaks" returns Integer
```

**Description**: Detect memory leaks

**Returns**: Number of leaked objects (0 if no leaks)

**Example**:
```runa
Let leak_count be proc arc_detect_leaks from ARCUtils
If leak_count is greater than 0:
    Note: LEAK DETECTED - leak_count objects not released
End If
```

---

#### `arc_check_balance`

```runa
Process called "arc_check_balance" returns Integer
```

**Description**: Check if retain/release calls are balanced

**Returns**:
- 1 if balanced
- 0 if unbalanced (leak or over-release)

**Example**:
```runa
If proc arc_check_balance from ARCUtils is equal to 0:
    Note: UNBALANCED - missing releases or extra releases
End If
```

**Notes**:
- Balance equation: `allocations + retains == releases + live_objects`

---

#### `arc_assert_no_leaks`

```runa
Process called "arc_assert_no_leaks" returns Integer
```

**Description**: Assert that no memory leaks exist

**Returns**:
- 1 if no leaks
- 0 if leaks detected

**Example**:
```runa
If proc arc_assert_no_leaks from ARCUtils is equal to 0:
    Note: TEST FAILED - Memory leaks detected
    Return 1
End If
```

---

#### `arc_assert_balanced`

```runa
Process called "arc_assert_balanced" returns Integer
```

**Description**: Assert that retain/release calls are balanced

**Returns**:
- 1 if balanced
- 0 if unbalanced

**Example**:
```runa
If proc arc_assert_balanced from ARCUtils is equal to 0:
    Note: TEST FAILED - Unbalanced retain/release
    Return 1
End If
```

---

#### `arc_warn_potential_cycle`

```runa
Process called "arc_warn_potential_cycle" takes ptr1 as Integer, ptr2 as Integer returns Integer
```

**Description**: Warn about potential reference cycle

**Parameters**:
- `ptr1` - First object
- `ptr2` - Second object

**Returns**:
- 1 if potential cycle detected
- 0 if no concern

**Example**:
```runa
Note: Creating bidirectional link
Set node_a.next to node_b
Set node_b.prev to node_a
If proc arc_warn_potential_cycle from ARCUtils with node_a, node_b is equal to 1:
    Note: WARNING - Consider using weak reference for prev
End If
```

**Notes**:
- Heuristic: warns if both objects have refcount > 1
- Use weak references to break cycles

---

## Memory Management Fundamentals

### Reference Counting Basics

**Reference counting** tracks how many references (pointers) exist to an object:

```
Initial allocation:    refcount = 1 (caller owns it)
arc_retain():         refcount += 1 (new owner)
arc_release():        refcount -= 1 (owner relinquished)
When refcount = 0:    object is deallocated
```

**Example**:
```runa
Let obj be proc arc_allocate from ARC with 64  Note: refcount = 1
Let ref1 be proc arc_retain from ARC with obj  Note: refcount = 2
Let ref2 be proc arc_retain from ARC with obj  Note: refcount = 3
proc arc_release from ARC with obj              Note: refcount = 2
proc arc_release from ARC with ref1             Note: refcount = 1
proc arc_release from ARC with ref2             Note: refcount = 0, deallocated
```

### Strong vs Weak References

**Strong Reference** (default):
- Increments refcount
- Prevents deallocation while it exists
- Created with `arc_allocate` or `arc_retain`

**Weak Reference**:
- Does NOT increment refcount
- Does NOT prevent deallocation
- Created with `arc_weak_create`
- Must be promoted to strong before use

**When to use weak references**:
- Back-pointers in bidirectional structures (doubly-linked lists, parent-child trees)
- Cache entries that should not prevent eviction
- Observer patterns where observers should not keep observables alive

### Reference Cycles

A **reference cycle** occurs when objects reference each other, preventing deallocation:

```
CYCLE EXAMPLE (LEAK):
  A --strong--> B
  B --strong--> A

Both A and B have refcount >= 1 forever (LEAK!)
```

**Solution**: Use weak references to break cycles:

```
CYCLE-FREE:
  A --strong--> B  (A owns B)
  B --weak----> A  (B does NOT own A)

When A is released, B is deallocated too (no leak)
```

### Copy-on-Write Optimization

**Copy-on-Write (COW)** avoids unnecessary copies:

```runa
Process called "append_to_buffer" takes buffer as Integer, value as Integer returns Integer:
    If proc arc_is_unique from ARC with buffer is equal to 1:
        Note: Unique reference - safe to mutate in-place
        proc append_value with buffer, value
        Return buffer
    Otherwise:
        Note: Shared reference - must clone before mutation
        Let size be proc arc_get_size from ARC with buffer
        Let new_buffer be proc arc_clone from ARC with buffer, size
        proc append_value with new_buffer, value
        proc arc_release from ARC with buffer
        Return new_buffer
    End If
End Process
```

**Benefits**:
- Avoids copying when reference is unique
- Preserves immutability when reference is shared
- Critical for performance in functional-style code

---

## Best Practices

### 1. Always Pair Retain and Release

**RULE**: Every `arc_retain` must be paired with `arc_release`.

**WRONG**:
```runa
Let obj be proc arc_allocate from ARC with 64
Let ref be proc arc_retain from ARC with obj
proc arc_release from ARC with obj
Note: LEAK - ref is never released
```

**CORRECT**:
```runa
Let obj be proc arc_allocate from ARC with 64
Let ref be proc arc_retain from ARC with obj
proc arc_release from ARC with obj
proc arc_release from ARC with ref  Note: Balanced
```

### 2. Release in Reverse Order (Stack Discipline)

**RULE**: Release references in reverse order of acquisition when possible.

**CORRECT**:
```runa
Let obj be proc arc_allocate from ARC with 64
Let ref1 be proc arc_retain from ARC with obj
Let ref2 be proc arc_retain from ARC with obj

proc arc_release from ARC with ref2  Note: Last acquired, first released
proc arc_release from ARC with ref1
proc arc_release from ARC with obj
```

### 3. Use Weak References for Back-Pointers

**RULE**: In bidirectional structures, use weak references for "parent" or "previous" pointers.

**WRONG** (creates cycle):
```runa
Type called "Node":
    next as Integer      Note: Strong reference
    prev as Integer      Note: Strong reference (CYCLE!)
End Type
```

**CORRECT**:
```runa
Type called "Node":
    next as Integer      Note: Strong reference
    prev_weak as Integer Note: Weak reference (breaks cycle)
End Type
```

### 4. Always Check Weak Reference Promotion

**RULE**: Always check result of `arc_weak_promote` before using.

**WRONG**:
```runa
Let strong be proc arc_weak_promote from ARC with weak
proc memory_get_int64 with strong, 0  Note: May be NULL!
```

**CORRECT**:
```runa
Let strong be proc arc_weak_promote from ARC with weak
If strong is equal to 0:
    Note: Object was deallocated
    Return 0
End If
proc memory_get_int64 with strong, 0  Note: Safe
proc arc_release from ARC with strong
```

### 5. Do Not Use Pointers After Release

**RULE**: Never use a pointer after `arc_release` returns 0.

**WRONG**:
```runa
Let result be proc arc_release from ARC with obj
If result is equal to 0:
    Note: Object was deallocated
End If
proc memory_get_int64 with obj, 0  Note: USE-AFTER-FREE BUG!
```

**CORRECT**:
```runa
Let value be proc memory_get_int64 with obj, 0
Let result be proc arc_release from ARC with obj
If result is equal to 0:
    Note: Object was deallocated
End If
Note: Do not use obj after this point
```

### 6. Use Statistics for Testing

**RULE**: Always use `arc_assert_no_leaks` and `arc_assert_balanced` in tests.

**CORRECT**:
```runa
Process called "test_my_function" returns Integer:
    proc arc_stats_reset from ARCUtils

    Note: Test code here
    proc my_function

    Note: Verify no leaks
    If proc arc_assert_no_leaks from ARCUtils is equal to 0:
        Note: TEST FAILED - Memory leak
        Return 1
    End If

    Note: Verify balance
    If proc arc_assert_balanced from ARCUtils is equal to 0:
        Note: TEST FAILED - Unbalanced retain/release
        Return 1
    End If

    Return 0  Note: Test passed
End Process
```

### 7. Prefer arc_is_unique for Copy-on-Write

**RULE**: Check `arc_is_unique` before mutating shared data.

**CORRECT**:
```runa
Process called "modify_buffer" takes buffer as Integer returns Integer:
    If proc arc_is_unique from ARC with buffer is equal to 0:
        Note: Shared - must clone
        Let size be proc arc_get_size from ARC with buffer
        Let new_buffer be proc arc_clone from ARC with buffer, size
        proc arc_release from ARC with buffer
        Set buffer to new_buffer
    End If

    Note: Safe to mutate in-place now
    proc mutate_buffer with buffer
    Return buffer
End Process
```

### 8. Document Ownership in Comments

**RULE**: Document who owns references in complex structures.

**EXAMPLE**:
```runa
Type called "TreeNode":
    value as Integer
    left as Integer      Note: Strong reference - parent owns left child
    right as Integer     Note: Strong reference - parent owns right child
    parent_weak as Integer  Note: Weak reference - child does NOT own parent
End Type
```

---

## Common Patterns

### Pattern 1: Singly-Linked List

```runa
Type called "ListNode" with annotation @ARC:
    value as Integer
    next as Integer  Note: Strong reference to next node
End Type

Process called "create_list_node" takes value as Integer returns Integer:
    Let node be proc arc_allocate from ARC with 16
    proc memory_set_int64 with node, 0, value
    proc memory_set_int64 with node, 8, 0  Note: next = NULL
    Return node
End Process

Process called "append_node" takes head as Integer, new_node as Integer returns Integer:
    If head is equal to 0:
        Return new_node
    End If

    Let current be head
    Let next be proc memory_get_int64 with current, 8

    While next is not equal to 0:
        Set current to next
        Set next to proc memory_get_int64 with current, 8
    End While

    Note: Retain new_node (head now owns it)
    Let retained be proc arc_retain from ARC with new_node
    proc memory_set_int64 with current, 8, retained

    Return head
End Process

Process called "destroy_list" takes head as Integer returns Integer:
    Let current be head

    While current is not equal to 0:
        Let next be proc memory_get_int64 with current, 8
        proc arc_release from ARC with current
        Set current to next
    End While

    Return 1
End Process
```

### Pattern 2: Doubly-Linked List (Weak Back-Pointers)

See `examples/arc/02_linked_list_weak.runa` for complete example.

```runa
Type called "ListNode" with annotation @ARC:
    value as Integer
    next as Integer         Note: Strong reference
    prev_weak as Integer    Note: Weak reference (prevents cycle)
End Type

Process called "link_nodes" takes prev as Integer, next as Integer returns Integer:
    Note: Set prev.next = next (strong)
    Let next_retained be proc arc_retain from ARC with next
    proc memory_set_int64 with prev, 8, next_retained

    Note: Set next.prev_weak = weak(prev)
    Let weak_prev be proc arc_weak_create from ARC with prev
    proc memory_set_int64 with next, 16, weak_prev

    Return 1
End Process
```

### Pattern 3: Binary Tree

See `examples/arc/03_tree_structure.runa` for complete example.

```runa
Type called "TreeNode" with annotation @ARC:
    value as Integer
    left as Integer   Note: Strong reference
    right as Integer  Note: Strong reference
End Type

Process called "destroy_tree_recursive" takes node as Integer returns Integer:
    If node is equal to 0:
        Return 1
    End If

    Note: Post-order traversal (children before parent)
    Let left be proc memory_get_int64 with node, 8
    If left is not equal to 0:
        proc destroy_tree_recursive with left
        proc arc_release from ARC with left
    End If

    Let right be proc memory_get_int64 with node, 16
    If right is not equal to 0:
        proc destroy_tree_recursive with right
        proc arc_release from ARC with right
    End If

    Note: Destroy current node
    proc arc_release from ARC with node

    Return 1
End Process
```

### Pattern 4: Parent-Child with Weak Parent Pointer

```runa
Type called "Widget" with annotation @ARC:
    name as Integer
    children as Integer      Note: List of strong references
    parent_weak as Integer   Note: Weak reference to parent
End Type

Process called "add_child" takes parent as Integer, child as Integer returns Integer:
    Note: Parent owns child (strong)
    proc add_to_children_list with parent, child

    Note: Child does NOT own parent (weak)
    Let weak_parent be proc arc_weak_create from ARC with parent
    proc memory_set_int64 with child, 16, weak_parent

    Return 1
End Process
```

### Pattern 5: Observer Pattern (Weak Observers)

```runa
Type called "Observable" with annotation @ARC:
    value as Integer
    observers as Integer  Note: List of WEAK references
End Type

Process called "register_observer" takes observable as Integer, observer as Integer returns Integer:
    Note: Create weak reference (observer does NOT keep observable alive)
    Let weak_observer be proc arc_weak_create from ARC with observer
    proc add_to_observer_list with observable, weak_observer
    Return 1
End Process

Process called "notify_observers" takes observable as Integer returns Integer:
    Let observers be proc memory_get_int64 with observable, 8
    Let count be proc get_observer_count with observers

    Let i be 0
    While i is less than count:
        Let weak be proc get_observer_at with observers, i

        Note: Try to promote weak reference
        Let strong be proc arc_weak_promote from ARC with weak
        If strong is not equal to 0:
            Note: Observer still alive - notify it
            proc notify_observer with strong
            proc arc_release from ARC with strong
        Otherwise:
            Note: Observer was deallocated - remove from list
            proc remove_observer_at with observers, i
        End If

        Set i to i plus 1
    End While

    Return 1
End Process
```

### Pattern 6: Cache (Weak Values)

```runa
Type called "Cache" with annotation @ARC:
    entries as Integer  Note: Dictionary of weak references
End Type

Process called "cache_get" takes cache as Integer, key as Integer returns Integer:
    Let weak be proc dictionary_lookup with cache, key
    If weak is equal to 0:
        Return 0  Note: Cache miss
    End If

    Note: Try to promote weak reference
    Let strong be proc arc_weak_promote from ARC with weak
    If strong is equal to 0:
        Note: Value was deallocated - remove from cache
        proc dictionary_remove with cache, key
        Return 0  Note: Cache miss
    End If

    Note: Cache hit - return strong reference
    Note: Caller MUST call arc_release when done
    Return strong
End Process

Process called "cache_put" takes cache as Integer, key as Integer, value as Integer returns Integer:
    Note: Store weak reference (does not prevent eviction)
    Let weak be proc arc_weak_create from ARC with value
    proc dictionary_insert with cache, key, weak
    Return 1
End Process
```

---

## Debugging and Leak Detection

### Leak Detection Workflow

**Step 1: Reset Statistics**
```runa
proc arc_stats_reset from ARCUtils
```

**Step 2: Run Code**
```runa
proc my_function
```

**Step 3: Check for Leaks**
```runa
Let leak_count be proc arc_detect_leaks from ARCUtils
If leak_count is greater than 0:
    Note: LEAK DETECTED - leak_count objects not released

    Note: Get detailed statistics
    Let stats be proc arc_dump_stats from ARCUtils
    Let allocations be proc memory_get_int64 from Memory with stats, 0
    Let deallocations be proc memory_get_int64 from Memory with stats, 8
    Let retains be proc memory_get_int64 from Memory with stats, 16
    Let releases be proc memory_get_int64 from Memory with stats, 24

    Note: Debug output
    Note: Allocations: allocations
    Note: Deallocations: deallocations
    Note: Retains: retains
    Note: Releases: releases
    Note: Live Objects: leak_count

    proc deallocate from Layout with stats
End If
```

**Step 4: Check Balance**
```runa
If proc arc_check_balance from ARCUtils is equal to 0:
    Note: UNBALANCED - retains/releases do not match
End If
```

### Common Leak Scenarios

**Scenario 1: Forgot to Release**
```runa
Note: WRONG
Let obj be proc arc_allocate from ARC with 64
Note: LEAK - never released

Note: CORRECT
Let obj be proc arc_allocate from ARC with 64
proc arc_release from ARC with obj
```

**Scenario 2: Unbalanced Retain/Release**
```runa
Note: WRONG
Let obj be proc arc_allocate from ARC with 64
Let ref1 be proc arc_retain from ARC with obj
proc arc_release from ARC with obj
Note: LEAK - ref1 never released

Note: CORRECT
Let obj be proc arc_allocate from ARC with 64
Let ref1 be proc arc_retain from ARC with obj
proc arc_release from ARC with obj
proc arc_release from ARC with ref1
```

**Scenario 3: Reference Cycle**
```runa
Note: WRONG - Cycle causes leak
Let node_a be proc arc_allocate from ARC with 16
Let node_b be proc arc_allocate from ARC with 16
proc memory_set_int64 with node_a, 0, proc arc_retain from ARC with node_b
proc memory_set_int64 with node_b, 0, proc arc_retain from ARC with node_a
proc arc_release from ARC with node_a
proc arc_release from ARC with node_b
Note: Both still have refcount = 1 (LEAK!)

Note: CORRECT - Use weak reference
Let node_a be proc arc_allocate from ARC with 16
Let node_b be proc arc_allocate from ARC with 16
proc memory_set_int64 with node_a, 0, proc arc_retain from ARC with node_b
Let weak_a be proc arc_weak_create from ARC with node_a
proc memory_set_int64 with node_b, 0, weak_a
proc arc_release from ARC with node_a
proc arc_release from ARC with node_b
proc arc_weak_release from ARC with weak_a
Note: No leak
```

### Using Assertions in Tests

```runa
Process called "test_with_leak_detection" returns Integer:
    Note: Reset statistics
    proc arc_stats_reset from ARCUtils

    Note: Test code
    Let obj be proc arc_tracked_allocate from ARCUtils with 64
    proc my_function with obj
    proc arc_tracked_release from ARCUtils with obj

    Note: Assert no leaks
    If proc arc_assert_no_leaks from ARCUtils is equal to 0:
        Note: TEST FAILED - Memory leak detected
        Return 1
    End If

    Note: Assert balanced
    If proc arc_assert_balanced from ARCUtils is equal to 0:
        Note: TEST FAILED - Unbalanced retain/release
        Return 1
    End If

    Return 0  Note: Test passed
End Process
```

---

## Performance Optimization

### 1. Minimize Retain/Release Calls

**Avoid unnecessary retain/release pairs:**

**INEFFICIENT**:
```runa
Let obj be proc arc_allocate from ARC with 64
Let temp be proc arc_retain from ARC with obj
proc use_object with temp
proc arc_release from ARC with temp
proc arc_release from ARC with obj
```

**EFFICIENT**:
```runa
Let obj be proc arc_allocate from ARC with 64
proc use_object with obj  Note: No extra retain/release
proc arc_release from ARC with obj
```

### 2. Use arc_is_unique for Copy-on-Write

**Always check uniqueness before cloning:**

```runa
If proc arc_is_unique from ARC with buffer is equal to 0:
    Note: Only clone if shared
    Let size be proc arc_get_size from ARC with buffer
    Let new_buffer be proc arc_clone from ARC with buffer, size
    proc arc_release from ARC with buffer
    Set buffer to new_buffer
End If
```

### 3. Prefer STACK or ARENA for Short-Lived Objects

**ARC has overhead - use other tiers when appropriate:**

```runa
Note: INEFFICIENT for temporary objects
Let temp be proc arc_allocate from ARC with 64
proc use_temp with temp
proc arc_release from ARC with temp

Note: EFFICIENT - use STACK
Let temp be a value of type TemporaryData
proc use_temp with temp
Note: Automatically deallocated at scope exit
```

### 4. Batch Operations to Reduce Atomic Overhead

**Atomic operations are expensive - batch when possible:**

```runa
Note: INEFFICIENT - many atomic operations
For Each item in collection:
    Let obj be proc arc_allocate from ARC with 64
    proc process_item with item, obj
    proc arc_release from ARC with obj
End For

Note: EFFICIENT - allocate all upfront
Let objects be proc allocate_array with collection_size
For Each item in collection:
    Let obj be proc arc_allocate from ARC with 64
    proc set_array_element with objects, index, obj
End For
For Each item in collection:
    Let obj be proc get_array_element with objects, index
    proc process_item with item, obj
    proc arc_release from ARC with obj
End For
```

### 5. Use Weak References for Caches

**Weak references prevent cache from keeping objects alive:**

```runa
Note: Strong references prevent eviction (BAD for cache)
Type called "Cache":
    entries as Integer  Note: Dictionary of strong references (WRONG)
End Type

Note: Weak references allow eviction (GOOD for cache)
Type called "Cache":
    entries as Integer  Note: Dictionary of weak references (CORRECT)
End Type
```

---

## Migration to Automatic ARC

### When Automatic ARC Arrives

**Automatic ARC (Phase 2)** will be implemented when IR/Gungnir (MIR layer) is complete. This will enable:

- Compiler automatically inserts `arc_retain` and `arc_release` calls
- Zero manual memory management
- Drop-in replacement for Manual ARC
- Identical performance and behavior

### Migration Path

**Your Manual ARC code will continue to work unchanged:**

```runa
Note: Manual ARC code (works now and future)
Let obj be proc arc_allocate from ARC with 64
Let ref be proc arc_retain from ARC with obj
proc arc_release from ARC with obj
proc arc_release from ARC with ref
```

**Automatic ARC equivalent (future):**

```runa
Note: Automatic ARC code (future - compiler inserts retain/release)
Type called "MyType" with annotation @ARC:
    field as Integer
End Type

Let obj be a value of type MyType  Note: Compiler inserts arc_allocate
Let ref be obj                       Note: Compiler inserts arc_retain
Note: Compiler inserts arc_release at scope exit automatically
```

### Preparing for Automatic ARC

**To prepare for Automatic ARC migration:**

1. **Use @ARC annotation on types** (already supported):
   ```runa
   Type called "MyType" with annotation @ARC:
       field as Integer
   End Type
   ```

2. **Follow ownership discipline** (strong vs weak references)

3. **Use statistics to verify correctness** (`arc_assert_no_leaks`, `arc_assert_balanced`)

4. **Document ownership in comments** (helps compiler analysis)

### Opt-In vs Opt-Out

When Automatic ARC arrives, you will be able to:

**Option 1: Opt-In to Automatic ARC**
- Annotate types with `@ARC`
- Compiler manages retain/release automatically
- Recommended for new code

**Option 2: Continue Using Manual ARC**
- Keep explicit `arc_retain` and `arc_release` calls
- Maximum control
- Recommended for performance-critical code or FFI boundaries

---

## Troubleshooting

### Problem: Memory Leak Detected

**Symptoms**:
- `arc_detect_leaks` returns non-zero
- `arc_assert_no_leaks` returns 0

**Diagnosis**:
```runa
Let stats be proc arc_dump_stats from ARCUtils
Let allocations be proc memory_get_int64 from Memory with stats, 0
Let deallocations be proc memory_get_int64 from Memory with stats, 8
Let retains be proc memory_get_int64 from Memory with stats, 16
Let releases be proc memory_get_int64 from Memory with stats, 24
Let live_objects be proc memory_get_int64 from Memory with stats, 32

Note: Debug output
Note: Allocations: allocations
Note: Deallocations: deallocations
Note: Retains: retains
Note: Releases: releases
Note: Live Objects: live_objects
```

**Solutions**:
1. **Check for missing `arc_release` calls**
2. **Check for reference cycles** (use weak references)
3. **Verify weak references are released** (`arc_weak_release`)

### Problem: Use-After-Free

**Symptoms**:
- Segmentation fault
- Corrupted data
- `arc_validate` returns 0

**Diagnosis**:
```runa
If proc arc_validate from ARC with obj is equal to 0:
    Note: Object is corrupted or was deallocated
End If
```

**Solutions**:
1. **Do not use pointer after `arc_release` returns 0**
2. **Check weak reference promotion** (may return NULL)
3. **Verify object is not deallocated in another thread**

### Problem: Unbalanced Retain/Release

**Symptoms**:
- `arc_check_balance` returns 0
- `arc_assert_balanced` returns 0

**Diagnosis**:
```runa
Let total_refs_created be allocations plus retains
Let total_refs_destroyed be releases
Let expected_unreleased be live_objects

If total_refs_created is not equal to total_refs_destroyed plus expected_unreleased:
    Note: UNBALANCED
    Note: Too many releases (over-release) or too few releases (leak)
End If
```

**Solutions**:
1. **Verify every `arc_retain` has matching `arc_release`**
2. **Check for double-release bugs**
3. **Ensure promoted weak references are released**

### Problem: Reference Cycle

**Symptoms**:
- `arc_detect_leaks` shows leaks
- Circular data structure

**Diagnosis**:
```runa
If proc arc_warn_potential_cycle from ARCUtils with obj1, obj2 is equal to 1:
    Note: Potential cycle detected
End If
```

**Solutions**:
1. **Use weak references for back-pointers**
2. **Use weak references in one direction of bidirectional relationships**
3. **Break cycles manually before releasing last reference**

### Problem: Performance Degradation

**Symptoms**:
- Excessive time in ARC operations
- High atomic contention

**Diagnosis**:
```runa
Let stats be proc arc_dump_stats from ARCUtils
Let retains be proc memory_get_int64 from Memory with stats, 16
Let releases be proc memory_get_int64 from Memory with stats, 24

Note: High retain/release counts indicate overhead
```

**Solutions**:
1. **Minimize retain/release calls** (avoid unnecessary copies)
2. **Use STACK or ARENA for short-lived objects**
3. **Batch operations to reduce atomic overhead**
4. **Use `arc_is_unique` for copy-on-write optimization**

---

## Appendix: Complete Example

See `examples/arc/` directory for complete working examples:

- **`01_basic_arc.runa`** - Basic allocation, multiple references, copy-on-write, statistics
- **`02_linked_list_weak.runa`** - Doubly-linked list with weak references
- **`03_tree_structure.runa`** - Binary tree with recursive cleanup

---

## Summary

**Manual ARC provides production-ready memory management for Runa v0.0.8.5:**

✅ **Memory Safety** - No manual `free()`, automatic deallocation
✅ **Shared Ownership** - Multiple references safely share objects
✅ **Cycle Prevention** - Weak references break reference cycles
✅ **Thread-Safety** - Atomic reference counting
✅ **Zero Technical Debt** - Complete implementation, production-ready
✅ **Debugging Support** - Comprehensive leak detection and statistics
✅ **Migration Path** - Seamless upgrade to Automatic ARC in future

**Remember**:
- Always pair `arc_retain` with `arc_release`
- Use weak references for back-pointers and caches
- Check `arc_is_unique` before mutating shared data
- Use `arc_assert_no_leaks` and `arc_assert_balanced` in tests
- Follow ownership discipline (document who owns what)

**Manual ARC is ready for production use in Runa v0.0.8.5 and beyond.**

---

**End of Manual ARC Production Guide**
