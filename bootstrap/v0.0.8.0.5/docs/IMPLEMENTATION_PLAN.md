# Runa v0.0.8 Implementation Plan

## Overview

v0.0.8 addresses two critical needs:
1. **Performance optimization** - Fix O(n²) compilation bottleneck discovered in v0.0.7.5
2. **Inline assembly** - Add native assembly support to eliminate external assembler dependency

## Current Status: v0.0.7.5 Performance Analysis

### Compilation Time Measurements

| Module | Functions | LOC | Compile Time | Status |
|--------|-----------|-----|--------------|--------|
| main.runa | 8 | 118 | 45ms | ✓ Acceptable |
| string_utils.runa | 1 | ~200 | ~100ms | ✓ Acceptable |
| hashtable.runa | 7 | ~150 | 632ms | ⚠ Slow |
| containers.runa | 0 | ~250 | 1.57s | ⚠ Slow |
| lexer.runa | 58 | ~800 | 1.17s | ⚠ Slow |
| **parser.runa** | 55 | ~1200 | **>10s** | ✗ **Unacceptable** |
| **codegen.runa** | 246 | ~2600 | **>10s** | ✗ **Unacceptable** |

### Performance Targets

- **Small files (<200 LOC):** <100ms
- **Medium files (200-500 LOC):** <500ms
- **Large files (500-1000 LOC):** <2s
- **Very large files (1000+ LOC):** <5s
- **Full self-compilation (7 modules):** <10s total

## Phase 1: Performance Profiling and Optimization

### Week 1: Identify Bottlenecks

**Objective:** Pinpoint exact O(n²) hotspots

**Tasks:**
1. Add timing instrumentation to parser.runa functions
2. Add timing instrumentation to codegen.runa functions
3. Compile parser.runa and codegen.runa with instrumentation
4. Identify top 5 slowest functions

**Expected findings:**
- Symbol table lookups (likely O(n) linear search repeated n times)
- Statement iteration (nested loops over statement arrays)
- String operations (repeated concatenation without buffering)
- Memory operations (repeated pointer dereferences)

**Success criteria:**
- Identified specific functions causing >80% of compile time
- Documented exact algorithmic complexity of each hotspot

### Week 2: Fix Critical Hotspots

**Priority 1: Symbol Table Optimization**

Current (suspected):
```runa
# O(n) lookup called n times = O(n²)
Process called "lookup_variable":
    Let i be 0
    While i is less than variable_count:
        If name matches variables[i]:
            Return variables[i]
        Let i be i plus 1
    Return 0
```

Fixed:
```runa
# Use hashtable for O(1) lookup
Process called "lookup_variable":
    Return hashtable_get(symbol_table, name)
```

**Priority 2: Statement Iteration**

Current (suspected):
```runa
# Nested loops over statements
For each function:
    For each statement in function:
        For each nested statement:
            Process statement  # O(n³) worst case
```

Fixed:
```runa
# Single-pass with stack-based traversal
Process statements with explicit stack
# O(n) with proper data structure
```

**Priority 3: String Buffering**

Current (suspected):
```runa
# Repeated string concatenation = O(n²)
Let result be ""
For each line:
    Let result be string_concat(result, line)
```

Fixed:
```runa
# String buffer with capacity doubling = O(n)
Let buffer be allocate_buffer(initial_capacity)
For each line:
    buffer_append(buffer, line)
Let result be buffer_to_string(buffer)
```

**Success criteria:**
- parser.runa compiles in <5s
- codegen.runa compiles in <5s
- Full self-compilation in <10s

### Week 3: Validate Performance

**Tasks:**
1. Run full benchmark suite
2. Measure self-compilation time (5 runs, average)
3. Profile with valgrind/cachegrind
4. Verify no memory leaks introduced
5. Ensure bootstrap still works (Stage 4 == Stage 5)

**Success criteria:**
- All performance targets met
- No regressions in correctness
- Bootstrap validation passes

## Phase 2: Inline Assembly Implementation

### Week 4: Design Inline Assembly Syntax

**Language syntax:**
```runa
Inline Assembly:
    mov $60, %rax
    xor %rdi, %rdi
    syscall
End Assembly
```

**Parser changes:**
- Add TOKEN_INLINE and TOKEN_ASSEMBLY keywords
- Add Statement type: STMT_INLINE_ASSEMBLY
- Store assembly lines as array of strings
- No validation of assembly syntax (pass-through)

**Codegen changes:**
- When emitting STMT_INLINE_ASSEMBLY:
  - Write each line directly to output file
  - No register allocation
  - No stack manipulation
  - User responsible for ABI compliance

**Design decisions:**
1. **No validation:** Pass assembly through verbatim
2. **No register tracking:** User manages registers
3. **No label mangling:** User creates unique labels
4. **Rationale:** Simplicity. Advanced users only.

### Week 5: Implement Parser Support

**Tasks:**
1. Add TOKEN_INLINE, TOKEN_ASSEMBLY to lexer
2. Add parse_inline_assembly() to parser
3. Add STMT_INLINE_ASSEMBLY to statement types
4. Store assembly lines as string array in AST
5. Write parser tests (tests/unit/test_inline_assembly.runa)

**Test cases:**
```runa
# Test 1: Simple syscall
Inline Assembly:
    mov $60, %rax
    syscall
End Assembly

# Test 2: Multi-line with labels
Inline Assembly:
.my_loop:
    dec %rcx
    jnz .my_loop
End Assembly

# Test 3: Mixed with regular code
Let x be 42
Inline Assembly:
    movq $99, %rax
End Assembly
print_integer(x)
```

**Success criteria:**
- Parser accepts inline assembly syntax
- AST correctly stores assembly lines
- No crashes or memory leaks
- All parser tests pass

### Week 6: Implement Codegen Support

**Tasks:**
1. Add codegen_generate_inline_assembly() function
2. Emit assembly lines directly to output file
3. No register allocation or stack adjustment
4. Write codegen tests

**Implementation:**
```runa
Process called "codegen_generate_inline_assembly" takes codegen as Integer, stmt as Integer:
    Let line_count be memory_get_int32(stmt, 16)
    Let lines be memory_get_pointer(stmt, 24)

    Let i be 0
    While i is less than line_count:
        Let line_offset be i multiplied by 8
        Let line be memory_get_pointer(lines, line_offset)
        emit_line(codegen, line)
        Let i be i plus 1
    End While
End Process
```

**Success criteria:**
- Inline assembly appears verbatim in output .s file
- Assembler successfully assembles output
- Generated binary executes correctly
- All codegen tests pass

### Week 7: End-to-End Testing

**Test programs:**

**Test 1: Hello world with syscall**
```runa
Process called "main" takes argc as Integer, argv as Integer returns Integer:
    Inline Assembly:
        # write syscall
        movq $1, %rax          # sys_write
        movq $1, %rdi          # stdout
        leaq .hello_msg(%rip), %rsi
        movq $13, %rdx         # length
        syscall

    .hello_msg:
        .ascii "Hello, World!"
    End Assembly
    Return 0
End Process
```

**Test 2: Custom exit code**
```runa
Process called "main" takes argc as Integer, argv as Integer returns Integer:
    Let exit_code be 42
    Inline Assembly:
        movq exit_code(%rip), %rdi
        movq $60, %rax
        syscall
    End Assembly
    Return 0
End Process
```

**Test 3: Inline assembly in function**
```runa
Process called "fast_multiply" takes a as Integer, b as Integer returns Integer:
    Inline Assembly:
        movq a(%rip), %rax
        imulq b(%rip), %rax
    End Assembly
    Return 0  # Rax already has result
End Process
```

**Success criteria:**
- All test programs compile
- All test programs execute with correct output
- No assembler errors
- No linker errors

### Week 8: Documentation and Polish

**Documentation:**
1. Update language specification with inline assembly syntax
2. Add inline assembly examples to user guide
3. Document ABI requirements for inline assembly
4. Add safety warnings (no validation, user responsibility)

**Polish:**
1. Clean up any debug output
2. Ensure consistent error messages
3. Add helpful error for common mistakes
4. Update ACHIEVEMENT.md

**Success criteria:**
- Complete documentation
- All examples work
- Clean codebase

## Phase 3: Integration and Verification

### Week 9: Full Bootstrap Test

**Tasks:**
1. Compile v0.0.8 with v0.0.7.5
2. Compile v0.0.8 with itself (self-compile)
3. Verify Stage 2 == Stage 3 outputs
4. Run full test suite
5. Run benchmark suite
6. Measure performance improvements

**Performance comparison:**

| Metric | v0.0.7.5 | v0.0.8 Target | Improvement |
|--------|----------|---------------|-------------|
| parser.runa | >10s | <5s | >50% |
| codegen.runa | >10s | <5s | >50% |
| Full self-compile | >1min | <10s | >80% |
| Fibonacci benchmark | 43ms | <50ms | Maintained |

**Success criteria:**
- Bootstrap passes
- All tests pass
- Performance targets met
- No regressions

### Week 10: Release Preparation

**Tasks:**
1. Copy v0.0.8 to release branch
2. Tag release v0.0.8.0
3. Build release binary
4. Generate release notes
5. Update main README

**Release checklist:**
- [ ] Bootstrap verified (Stage 2 == Stage 3)
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Benchmark results documented
- [ ] Performance targets met
- [ ] Inline assembly working
- [ ] Documentation complete
- [ ] No known critical bugs

## Success Criteria

### Must Have (Required)
1. Self-compilation in <10 seconds
2. parser.runa compiles in <5 seconds
3. codegen.runa compiles in <5 seconds
4. Inline assembly syntax fully functional
5. Bootstrap verification passes
6. All existing tests still pass
7. No memory leaks (valgrind clean)

### Should Have (High Priority)
1. Inline assembly examples and tests
2. Performance profiling documentation
3. Updated language specification
4. Benchmark improvements documented

### Nice to Have (Optional)
1. Comparison with other minimal compilers
2. Optimization documentation for users
3. Performance tips for large files

## Risk Mitigation

### Risk 1: Performance fixes break correctness
**Mitigation:** Continuous bootstrap testing after each optimization

### Risk 2: Inline assembly too complex
**Mitigation:** Start with minimal pass-through, add features later if needed

### Risk 3: Can't achieve 10s target
**Mitigation:** Set minimum acceptable target (30s), document as known issue

### Risk 4: Scope creep
**Mitigation:** Strict adherence to this plan, no new features

## Timeline Summary

- **Weeks 1-3:** Performance optimization (3 weeks)
- **Weeks 4-8:** Inline assembly (5 weeks)
- **Weeks 9-10:** Integration and release (2 weeks)
- **Total:** 10 weeks

## Notes

- v0.0.7.5 remains untouched as verified milestone
- All work happens in v0.0.8 branch
- Can be compressed if performance fixes are straightforward
- Can extend if inline assembly needs more iteration
- No feature additions beyond performance and inline assembly