# Runa Compiler Intrinsics Specification

**Version:** 1.0
**Status:** Active Development
**Last Updated:** 2025-01-13

## Overview

Compiler intrinsics are special functions that the Runa compiler recognizes and replaces with platform-specific machine code during compilation. They enable pure Runa code to perform low-level operations without inline assembly.

## Design Philosophy

1. **Pure Runa Surface**: Primitives are written in pure Runa using intrinsics
2. **Platform Agnostic**: Same primitive code works on all platforms
3. **Backend Responsibility**: Compiler backend emits platform-specific code for each intrinsic
4. **Zero Overhead**: Intrinsics compile to optimal machine code (no function call overhead)

## Intrinsic Naming Convention

All intrinsics use the prefix `__intrinsic_` to distinguish them from regular functions:

```runa
__intrinsic_<category>_<operation>
```

Examples:
- `__intrinsic_memory_load_byte`
- `__intrinsic_syscall_invoke`
- `__intrinsic_atomic_add`

## Core Intrinsic Categories

### 1. Memory Operations

#### Load Operations
```runa
__intrinsic_memory_load_byte(ptr: Integer, offset: Integer) -> Integer
__intrinsic_memory_load_int32(ptr: Integer, offset: Integer) -> Integer
__intrinsic_memory_load_int64(ptr: Integer, offset: Integer) -> Integer
__intrinsic_memory_load_float64(ptr: Integer, offset: Integer) -> Float
```

**Backend Behavior:**
- x86_64: `MOV` instruction with appropriate size
- ARM64: `LDR` / `LDRB` instruction
- RISC-V: `LB` / `LW` / `LD` instruction

#### Store Operations
```runa
__intrinsic_memory_store_byte(ptr: Integer, offset: Integer, value: Integer) -> Void
__intrinsic_memory_store_int32(ptr: Integer, offset: Integer, value: Integer) -> Void
__intrinsic_memory_store_int64(ptr: Integer, offset: Integer, value: Integer) -> Void
__intrinsic_memory_store_float64(ptr: Integer, offset: Integer, value: Float) -> Void
```

**Backend Behavior:**
- x86_64: `MOV` instruction to memory
- ARM64: `STR` / `STRB` instruction
- RISC-V: `SB` / `SW` / `SD` instruction

#### Memory Operations
```runa
__intrinsic_memory_copy(dest: Integer, src: Integer, size: Integer) -> Void
__intrinsic_memory_set(dest: Integer, value: Integer, size: Integer) -> Void
__intrinsic_memory_compare(ptr1: Integer, ptr2: Integer, size: Integer) -> Integer
```

**Backend Behavior:**
- May inline for small sizes
- May call optimized library routine for large sizes
- Uses platform-specific SIMD if available

### 2. System Call Operations

```runa
__intrinsic_syscall_0(syscall_number: Integer) -> Integer
__intrinsic_syscall_1(syscall_number: Integer, arg1: Integer) -> Integer
__intrinsic_syscall_2(syscall_number: Integer, arg1: Integer, arg2: Integer) -> Integer
__intrinsic_syscall_3(syscall_number: Integer, arg1: Integer, arg2: Integer, arg3: Integer) -> Integer
__intrinsic_syscall_4(syscall_number: Integer, arg1: Integer, arg2: Integer, arg3: Integer, arg4: Integer) -> Integer
__intrinsic_syscall_5(syscall_number: Integer, arg1: Integer, arg2: Integer, arg3: Integer, arg4: Integer, arg5: Integer) -> Integer
__intrinsic_syscall_6(syscall_number: Integer, arg1: Integer, arg2: Integer, arg3: Integer, arg4: Integer, arg5: Integer, arg6: Integer) -> Integer
```

**Backend Behavior:**
- **Linux x86_64**: `syscall` instruction with arguments in RAX, RDI, RSI, RDX, R10, R8, R9
- **Linux ARM64**: `svc #0` instruction with arguments in X8, X0-X7
- **Windows x86_64**: Call Win32 API functions (not direct syscalls)
- **Darwin/macOS**: System call with different ABI

### 3. Atomic Operations

```runa
__intrinsic_atomic_load(ptr: Integer) -> Integer
__intrinsic_atomic_store(ptr: Integer, value: Integer) -> Void
__intrinsic_atomic_add(ptr: Integer, value: Integer) -> Integer
__intrinsic_atomic_sub(ptr: Integer, value: Integer) -> Integer
__intrinsic_atomic_exchange(ptr: Integer, value: Integer) -> Integer
__intrinsic_atomic_compare_exchange(ptr: Integer, expected: Integer, desired: Integer) -> Integer
```

**Backend Behavior:**
- x86_64: `LOCK` prefix + instruction (e.g., `LOCK ADD`)
- ARM64: `LDXR` / `STXR` load-exclusive/store-exclusive
- Uses platform-specific atomic instructions

### 4. Arithmetic Operations (Compiler Built-ins)

Most arithmetic is handled by the compiler naturally, but some operations need intrinsics:

```runa
__intrinsic_overflow_add(a: Integer, b: Integer) -> (Integer, Boolean)
__intrinsic_overflow_sub(a: Integer, b: Integer) -> (Integer, Boolean)
__intrinsic_overflow_mul(a: Integer, b: Integer) -> (Integer, Boolean)
__intrinsic_count_leading_zeros(value: Integer) -> Integer
__intrinsic_count_trailing_zeros(value: Integer) -> Integer
__intrinsic_popcount(value: Integer) -> Integer
```

**Backend Behavior:**
- x86_64: Use CPU flags (OF) for overflow detection, `LZCNT`, `TZCNT`, `POPCNT`
- ARM64: Use `CLZ`, `CTZ` instructions
- Fallback to software implementation if CPU doesn't support

### 5. CPU Feature Detection

```runa
__intrinsic_cpu_has_feature(feature_id: Integer) -> Boolean
__intrinsic_cpu_get_cycle_count() -> Integer
__intrinsic_cpu_pause() -> Void
```

**Backend Behavior:**
- Runtime CPU feature detection (CPUID on x86_64)
- Performance counter access
- Spin-wait hint (PAUSE on x86_64, YIELD on ARM64)

### 6. Floating Point Operations

```runa
__intrinsic_float_sqrt(value: Float) -> Float
__intrinsic_float_abs(value: Float) -> Float
__intrinsic_float_min(a: Float, b: Float) -> Float
__intrinsic_float_max(a: Float, b: Float) -> Float
__intrinsic_float_round(value: Float) -> Float
__intrinsic_float_floor(value: Float) -> Float
__intrinsic_float_ceil(value: Float) -> Float
```

**Backend Behavior:**
- x86_64: SSE/AVX instructions (`SQRTSD`, `ROUNDSD`, etc.)
- ARM64: NEON instructions
- Fallback to software implementation if needed

## Implementation in Primitives

### Before (with inline assembly):
```runa
Process called "memory_get_byte" takes ptr as Integer, offset as Integer returns Integer:
    Let result be 0
    Inline Assembly:
        movq -8(%rbp), %rax      # ptr
        movq -16(%rbp), %rcx     # offset
        movb (%rax,%rcx,1), %al  # load byte
        movzbq %al, %rax         # zero-extend
        movq %rax, -24(%rbp)     # result
    End Assembly
    Return result
End Process
```

### After (pure Runa with intrinsic):
```runa
Process called "memory_get_byte" takes ptr as Integer, offset as Integer returns Integer:
    Return __intrinsic_memory_load_byte(ptr, offset)
End Process
```

## Backend Codegen Requirements

When the compiler encounters an intrinsic call, the backend must:

1. **Recognize the intrinsic name** (starts with `__intrinsic_`)
2. **Emit platform-specific code** inline (no actual function call)
3. **Optimize aggressively** (intrinsics are performance-critical)
4. **Handle all target platforms** (x86_64, ARM64, MIPS, RISC-V, etc.)

### Example Backend Implementation (Pseudo-code):

```
if function_name == "__intrinsic_memory_load_byte":
    if target_platform == "x86_64":
        emit("movq", arg1_reg, "%rax")        # ptr to RAX
        emit("movq", arg2_reg, "%rcx")        # offset to RCX
        emit("movb", "(%rax,%rcx,1)", "%al")  # load byte
        emit("movzbq", "%al", result_reg)     # zero-extend to result
    elif target_platform == "arm64":
        emit("ldrb", result_reg, "[" + arg1_reg + ", " + arg2_reg + "]")
    elif target_platform == "riscv":
        emit("add", "t0", arg1_reg, arg2_reg)  # ptr + offset
        emit("lb", result_reg, "0(t0)")        # load byte
```

## Intrinsic Detection by Compiler

The compiler frontend should:

1. **Parse normally** - Intrinsics look like regular function calls
2. **Mark as intrinsic** in the AST/IR
3. **Skip normal function call codegen** - Pass to intrinsic handler
4. **Backend emits inline code** - No call overhead

## Error Handling

If an intrinsic is not implemented for a target platform:

1. **Compile-time error**: "Intrinsic __intrinsic_X not available for target platform Y"
2. **Provide fallback**: Some intrinsics may have software fallback implementations
3. **Document limitations**: Clearly document which intrinsics work on which platforms

## Benefits of This Approach

1. **✅ Portable**: Primitives written once, work everywhere
2. **✅ Self-hosting**: Compiler can compile itself on any platform
3. **✅ Performance**: Zero overhead - intrinsics compile to optimal code
4. **✅ Maintainable**: No 21 versions of every primitive
5. **✅ Type-safe**: Intrinsics have proper type signatures
6. **✅ Debuggable**: Pure Runa is easier to debug than inline assembly

## Migration Path

### Phase 1: Define Intrinsics
- Create this specification document ✅
- Define all needed intrinsics ✅

### Phase 2: Create Intrinsics Module
- Create `primitives/core/intrinsics.runa` with intrinsic declarations
- Document each intrinsic's behavior

### Phase 3: Refactor Primitives
- Rewrite memory_core.runa to use intrinsics
- Rewrite syscall.runa to use intrinsics
- Rewrite other primitives as needed

### Phase 4: Backend Implementation
- Implement intrinsic codegen in compiler backend
- Support all target platforms
- Test and validate on each platform

### Phase 5: Remove Inline Assembly
- Remove all inline assembly from primitives
- Keep platform-specific files for platform metadata only

## Future Extensions

Possible additional intrinsic categories:

- SIMD operations (`__intrinsic_simd_add_i32x4`)
- Cryptographic operations (`__intrinsic_crypto_aes_encrypt`)
- GPU operations (`__intrinsic_gpu_parallel_for`)
- Network operations (`__intrinsic_net_checksum`)

---

**This specification enables Runa to be truly platform-agnostic while maintaining maximum performance.**
