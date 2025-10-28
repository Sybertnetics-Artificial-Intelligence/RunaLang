# @ARC Codegen Implementation Guide

**Status**: NOT YET IMPLEMENTED (v0.0.8.5)
**Target**: Post-v0.0.8.5 (after Gungnir IR infrastructure complete)
**Priority**: HIGH (enables automatic memory management)

## Overview

This document describes how to implement automatic arc_retain() and arc_release() insertion in the Runa code generator based on the @ARC lifetime tracking data from `compiler/frontend/semantic/arc_lifetime_tracker.runa`.

## Current Status (v0.0.8.5)

### ✅ COMPLETE
- **Lexer**: TOKEN_AT (653) fully implemented for @ symbol recognition
- **Parser**: `parse_type_annotation()` in statement_parsers.runa handles `as @ARC Type` syntax
- **Type Annotations**: Complete infrastructure in `type_annotations.runa` for @ARC, @Owned, @Shared, @Arena, @Stack
- **Semantic Analysis**: `arc_lifetime_tracker.runa` provides complete lifetime tracking and insertion point marking

### ❌ NOT YET IMPLEMENTED
- **Codegen**: Automatic arc_retain/arc_release insertion (THIS DOCUMENT)
- **IR Infrastructure**: Requires Gungnir MIR/LIR for proper instrumentation

## Architecture

```
Source Code:
Let node as @ARC Node be create_node()
Use node
  ↓
Lexer: Recognizes "@", "ARC", "Node" as separate tokens
  ↓
Parser: Creates AST with TYPE_ANNOTATION node
  ↓
Semantic Analysis: arc_lifetime_tracker marks insertion points
  ↓
Codegen: Reads insertion points and inserts retain/release calls ← THIS IS MISSING
  ↓
Assembly Output:
  call create_node
  mov [node], rax
  call arc_retain    ; ← Inserted automatically
  ; ... use node ...
  call arc_release   ; ← Inserted automatically at last use
```

## Data Structures (from arc_lifetime_tracker.runa)

### ARCTracker Structure
```runa
Type called "ARCTracker":
    arc_variables as Integer      // HashTable of ARCVariable
    insertion_points as Integer   // List of InsertionPoint
    current_scope_depth as Integer
    error_count as Integer
    warning_count as Integer
End Type
```

### InsertionPoint Structure
```runa
Type called "InsertionPoint":
    ast_node as Integer           // WHERE to insert
    insertion_type as Integer     // WHAT to insert (1=retain, 2=release)
    variable_name as Integer      // WHICH variable
    line as Integer               // Source location
    column as Integer             // Source location
    is_conditional as Integer     // 1 if inside if/loop
End Type
```

### Insertion Type Constants
```runa
Constant INSERTION_RETAIN as Integer is 1
Constant INSERTION_RELEASE as Integer is 2
```

## Implementation Steps

### Step 1: Access Insertion Points in Codegen

In your codegen process (e.g., `codegen_elf_functions.runa` or equivalent):

```runa
Note: Get ARCTracker from semantic analyzer
Let arc_tracker be proc get_arc_tracker from SemanticAnalyzer with analyzer

If arc_tracker is not equal to 0:
    Note: Get insertion points List
    Let insertion_points be proc arc_get_insertion_points from ARCLifetimeTracker with arc_tracker

    Note: Get count of insertion points
    Let insertion_count be proc arc_get_insertion_point_count from ARCLifetimeTracker with arc_tracker

    Note: Iterate through insertion points and process each
    Let i be 0
    Loop while i is less than insertion_count:
        Let point be proc get from List with insertion_points, i

        Note: Process this insertion point
        proc codegen_process_insertion_point with point

        Set i to i plus 1
    End Loop
End If
```

### Step 2: Process Each Insertion Point

```runa
Process called "codegen_process_insertion_point" takes insertion_point as Integer returns Integer:
    Note: Extract insertion point data
    Let ast_node be proc memory_get_qword from Memory with insertion_point, 0
    Let insertion_type be proc memory_get_qword from Memory with insertion_point, 8
    Let variable_name be proc memory_get_qword from Memory with insertion_point, 16
    Let line be proc memory_get_qword from Memory with insertion_point, 24
    Let column be proc memory_get_qword from Memory with insertion_point, 32
    Let is_conditional be proc memory_get_qword from Memory with insertion_point, 40

    Note: Determine which call to insert
    If insertion_type is equal to 1:  // INSERTION_RETAIN
        proc codegen_insert_retain_call with ast_node, variable_name
    End If

    If insertion_type is equal to 2:  // INSERTION_RELEASE
        proc codegen_insert_release_call with ast_node, variable_name
    End If

    Return 1
End Process
```

### Step 3: Insert arc_retain() Calls

```runa
Process called "codegen_insert_retain_call" takes ast_node as Integer, variable_name as Integer returns Integer:
    Note:
    Insert arc_retain() call after AST node.

    Assembly pattern (x86-64):
        ; node is in rax after allocation/assignment
        mov rdi, rax           ; First argument: pointer to retain
        call arc_retain        ; Increment refcount
        ; rax still contains node pointer

    Algorithm:
    1. Get variable location (register or stack)
    2. Load variable pointer into rdi (first argument register)
    3. Call arc_retain
    4. Result (same pointer) in rax
    :End Note

    Note: Get variable location from symbol table
    Let var_location be proc lookup_variable_location with variable_name

    Note: Generate assembly to load pointer into rdi
    If variable is in rax:
        Note: Already in rax, just move to rdi
        proc emit_asm with "mov rdi, rax"
    Otherwise:
        Note: Load from stack/memory into rdi
        proc emit_asm with "mov rdi, [variable_location]"
    End If

    Note: Call arc_retain
    proc emit_asm with "call arc_retain"

    Return 1
End Process
```

### Step 4: Insert arc_release() Calls

```runa
Process called "codegen_insert_release_call" takes ast_node as Integer, variable_name as Integer returns Integer:
    Note:
    Insert arc_release() call at AST node (last use or scope exit).

    Assembly pattern (x86-64):
        mov rdi, [node]        ; Load pointer to release
        call arc_release       ; Decrement refcount (may free)
        ; Do NOT use node after this point

    Algorithm:
    1. Get variable location (register or stack)
    2. Load variable pointer into rdi
    3. Call arc_release
    4. Mark variable as invalid (debugging)
    :End Note

    Note: Get variable location from symbol table
    Let var_location be proc lookup_variable_location with variable_name

    Note: Generate assembly to load pointer into rdi
    proc emit_asm with "mov rdi, [variable_location]"

    Note: Call arc_release
    proc emit_asm with "call arc_release"

    Note: Optional: Zero out variable location for safety (prevents use-after-free)
    proc emit_asm with "mov qword [variable_location], 0"

    Return 1
End Process
```

## Insertion Point Placement Rules

### Retain Insertion Points

arc_tracker marks RETAIN insertion points at:

1. **Variable Declaration with Initialization**
   ```runa
   Let node as @ARC Node be create_node()
   ; Retain after create_node() returns
   ```

2. **Assignment from Another @ARC Variable**
   ```runa
   Set node2 to node1
   ; Retain node1 before assignment (creates new reference)
   ```

3. **Passing @ARC Variable to Function**
   ```runa
   proc use_node with node
   ; Retain before function call (function gets new reference)
   ```

4. **Storing @ARC Variable in Structure/Collection**
   ```runa
   Set list.items[0] to node
   ; Retain before storing (collection holds new reference)
   ```

### Release Insertion Points

arc_tracker marks RELEASE insertion points at:

1. **Variable Last Use**
   ```runa
   Let node as @ARC Node be create_node()
   proc process with node
   proc something_else        ; ← Release 'node' here (last use was previous line)
   ```

2. **Scope Exit**
   ```runa
   If condition:
       Let node as @ARC Node be create_node()
       proc use_node with node
   End If  ; ← Release 'node' here (scope exit)
   ```

3. **Before Reassignment**
   ```runa
   Let node as @ARC Node be create_node()
   Set node to another_node()  ; ← Release old 'node' before reassignment
   ```

4. **Function Return (if not returning the value)**
   ```runa
   Process called "foo" returns Integer:
       Let node as @ARC Node be create_node()
       proc use_node with node
       Return 42              ; ← Release 'node' before return
   End Process
   ```

## Edge Cases and Special Handling

### Conditional Blocks

If `insertion_point.is_conditional == 1`, the insertion is inside an if/loop:

```runa
If condition:
    Let node as @ARC Node be create_node()
    ; Retain after create
    proc use_node with node
    ; Release before End If
End If
```

**Codegen must ensure**:
- Retain only executes if condition is true
- Release only executes if the corresponding retain executed
- Track whether variable was initialized in this path

### Early Returns

```runa
Process called "foo" returns Integer:
    Let node as @ARC Node be create_node()

    If error:
        Return 0  ; ← Must release 'node' BEFORE return
    End If

    proc use_node with node
    Return 1      ; ← Must release 'node' BEFORE return
End Process
```

**Codegen must**:
- Insert release before EVERY return statement
- Track which @ARC variables are live at each return

### Returning @ARC Values

```runa
Process called "create_thing" returns @ARC Node:
    Let node as @ARC Node be create_node()
    Return node  ; ← Do NOT release - transfer ownership to caller
End Process
```

**Codegen must**:
- Skip release if variable is being returned
- arc_tracker marks `is_return_value == 1` in ARCVariable

### Loop Variables

```runa
Loop 10 times:
    Let node as @ARC Node be create_node()
    proc use_node with node
End Loop  ; ← Release after EACH iteration
```

**Codegen must**:
- Release at end of each iteration
- Not accumulate unreleased references

## Integration with Existing Codegen

### Current Codegen Flow (v0.0.8.5)

```
1. Parse AST
2. Semantic analysis
3. Type checking
4. Symbol resolution
5. Codegen: Generate assembly
   - Process declarations
   - Process expressions
   - Process statements
6. Link and output
```

### Updated Codegen Flow (Post-v0.0.8.5)

```
1. Parse AST
2. Semantic analysis
   - Run arc_lifetime_tracker
   - Mark insertion points in AST
3. Type checking
4. Symbol resolution
5. Codegen: Generate assembly
   - Process declarations
   - Process expressions
   - Process statements
   - **NEW**: Process insertion points
     - Insert arc_retain calls
     - Insert arc_release calls
6. Link and output
```

## Testing Strategy

### Unit Tests

1. **Single Variable**
   ```runa
   Let node as @ARC Node be create_node()
   proc use_node with node
   ; Expected: 1 retain, 1 release
   ```

2. **Multiple Variables**
   ```runa
   Let node1 as @ARC Node be create_node()
   Let node2 as @ARC Node be create_node()
   proc use_both with node1, node2
   ; Expected: 2 retains, 2 releases
   ```

3. **Nested Scopes**
   ```runa
   Let outer as @ARC Node be create_node()
   If condition:
       Let inner as @ARC Node be create_node()
   End If
   ; Expected: outer: 1 retain, 1 release
   ;          inner: 1 retain, 1 release (in if block)
   ```

4. **Early Return**
   ```runa
   Process called "test" returns Integer:
       Let node as @ARC Node be create_node()
       If error:
           Return 0  ; Must release before return
       End If
       Return 1      ; Must release before return
   End Process
   ```

### Integration Tests

1. Compile test programs with @ARC variables
2. Run with memory leak detector (valgrind)
3. Verify refcount balance (retain count == release count)
4. Verify no memory leaks
5. Verify no use-after-free errors

## Performance Considerations

### Retain/Release Overhead

- arc_retain: Atomic increment (~10-20 cycles)
- arc_release: Atomic decrement + conditional free (~50-100 cycles if freed)

**Optimization opportunities**:
- Eliminate retain/release pairs when variable doesn't escape scope
- Escape analysis can remove unnecessary operations
- Inline simple retain/release calls

### Example Optimization

**Before optimization**:
```runa
Let node as @ARC Node be create_node()
proc local_use_only with node  ; Function doesn't store reference
; node never escapes, could use stack allocation
```

**After escape analysis**:
```runa
; Compiler detects node doesn't escape
; Downgrade from @ARC to @Owned (no retain/release needed)
; Or use stack allocation if size known
```

## Dependencies

### Required for Full Implementation

1. **IR Infrastructure (Gungnir)**:
   - MIR (Mid-level IR) for high-level transformations
   - LIR (Low-level IR) for insertion point instrumentation
   - IR builder and optimizer

2. **Escape Analysis Pass**:
   - Detect which @ARC variables escape their scope
   - Optimize away unnecessary retain/release pairs

3. **Backend Integration**:
   - arc_retain/arc_release function calls
   - Calling convention support (System V AMD64 ABI)
   - Register allocation aware of retain/release

## Completion Criteria

@ARC codegen implementation is complete when:

- ✅ arc_tracker insertion points are read in codegen
- ✅ arc_retain() calls inserted at RETAIN insertion points
- ✅ arc_release() calls inserted at RELEASE insertion points
- ✅ Edge cases handled (conditionals, early returns, loops, return values)
- ✅ All unit tests pass
- ✅ Integration tests show zero memory leaks
- ✅ Performance benchmarks show acceptable overhead
- ✅ Escape analysis optimization implemented

## References

- `compiler/frontend/semantic/arc_lifetime_tracker.runa` - Lifetime tracking implementation
- `compiler/frontend/parsing/type_annotations.runa` - Type annotation parsing
- `runtime/core/memory/arc_heap.runa` - Runtime arc_retain/arc_release implementation
- `docs/dev/MEMORY_ARCHITECTURE.md` - Memory tier specifications

## Contact

For questions about @ARC codegen implementation, consult:
- MEMORY_ARCHITECTURE.md for memory tier specifications
- arc_lifetime_tracker.runa for insertion point data structures
- Gungnir IR documentation (when available)
