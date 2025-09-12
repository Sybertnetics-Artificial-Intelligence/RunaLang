# Machine Module Architecture Plan

## Executive Summary

The `machine` module provides Runa's foundational interface to hardware and operating system primitives. It serves as the privileged, compiler-aware bridge between Runa's high-level abstractions and raw machine capabilities, eliminating all C library dependencies through direct inline assembly and syscalls.

## Current State

Runa already has:
- **Zero C library dependencies** - We use direct runtime calls internally
- **Inline assembly support** - Located in `/runa/src/compiler/frontend/primitives/assembly/inline_asm.runa`
- **Existing stdlib structure**:
  - `sys/os` - OS abstractions
  - `sys/concurrent` - Concurrency primitives
  - `sys/io` - I/O operations
  - `sys/memory` - Memory management
  - `net` - Networking

## Proposed Architecture

### Location
`runa/src/stdlib/core/machine/` - A privileged core module with compiler intrinsic support

### Module Structure
```
runa/src/stdlib/core/
└── machine/
    ├── syscall.runa      # Raw syscall interface
    ├── atomic.runa       # Atomic operations
    ├── memory.runa       # Memory operations (volatile, secure zeroing)
    ├── cpu.runa          # CPU feature detection and control
    └── simd.runa         # SIMD/vector operations
```

### Integration Points

The machine module will serve as the foundation for existing stdlib modules:
- `sys/os` → Built on `machine/syscall.runa`
- `sys/concurrent` → Built on `machine/atomic.runa`
- `sys/io` → Built on `machine/syscall.runa`
- `sys/memory` → Built on `machine/memory.runa`
- `net` → Built on `machine/syscall.runa`

## Three-Layer Architecture

### Layer 1: Application (99.9% of developers)
- Write safe, high-level Runa code
- Use stdlib abstractions (`sys/os`, `net`, etc.)
- Never touch assembly or syscalls directly

### Layer 2: Machine Module (Core team)
- Wraps dangerous inline assembly in safe APIs
- Provides compiler intrinsics for optimization
- Maintained with same rigor as compiler

### Layer 3: Compiler/Runtime (Systems programmers)
- Implements inline assembly primitives
- Handles bootstrapping and initialization
- Direct hardware interface

## Implementation Phases

### Phase 1: Foundation (Immediate Priority)

#### 1.1 Syscall Interface
**File:** `machine/syscall.runa`
```runa
Process called "raw_syscall" that takes 
    number as Integer,
    arg1 as Integer,
    arg2 as Integer,
    arg3 as Integer,
    arg4 as Integer,
    arg5 as Integer,
    arg6 as Integer
returns Integer:
    @Security_Scope
        Direct operating system interface. This is the single
        unified entry point for all OS operations.
    @End Security_Scope
    
    Let result as Integer
    
    Inline Assembly volatile:
        "mov rax, %1"    Note: Syscall number
        "mov rdi, %2"    Note: First argument
        "mov rsi, %3"    Note: Second argument
        "mov rdx, %4"    Note: Third argument
        "mov r10, %5"    Note: Fourth argument
        "mov r8, %6"     Note: Fifth argument
        "mov r9, %7"     Note: Sixth argument
        "syscall"        Note: Invoke kernel
        "mov %0, rax"    Note: Return value
        : "=r"(result)
        : "r"(number), "r"(arg1), "r"(arg2), "r"(arg3), "r"(arg4), "r"(arg5), "r"(arg6)
        : "rax", "rdi", "rsi", "rdx", "r10", "r8", "r9", "rcx", "r11", "memory"
    End Assembly
    
    Return result
End Process
```

#### 1.2 Atomic Operations
**File:** `machine/atomic.runa`
- `atomic_load` - Atomic read
- `atomic_store` - Atomic write
- `atomic_add` - Atomic addition
- `atomic_compare_and_swap` - CAS operation
- `atomic_exchange` - Atomic swap

#### 1.3 Memory Operations
**File:** `machine/memory.runa`
- `securely_zero_memory` - Non-optimizable memory wipe
- `volatile_read`/`volatile_write` - Compiler-fence operations
- `memory_fence` - Memory barrier
- `cache_flush` - CPU cache control

### Phase 2: Stdlib Migration

#### 2.1 Update sys/os
- Rewrite file operations to use `Machine.raw_syscall`
- Remove any remaining external dependencies

#### 2.2 Update sys/concurrent
- Rewrite mutexes/locks using `Machine.atomic_*`
- Implement lock-free data structures

#### 2.3 Update net
- Rewrite socket operations using `Machine.raw_syscall`
- Direct kernel networking interface

### Phase 3: Advanced Features

#### 3.1 CPU Feature Detection
**File:** `machine/cpu.runa`
```runa
Process called "cpu_supports_feature" that takes feature as String returns Boolean:
    @Implementation
        Uses CPUID instruction to detect CPU capabilities
    @End Implementation
    
    Match feature:
        When "AVX512":
            Return check_avx512_support()
        When "AES-NI":
            Return check_aesni_support()
        When "AVX2":
            Return check_avx2_support()
        Otherwise:
            Return False
    End Match
End Process
```

#### 3.2 SIMD Operations
**File:** `machine/simd.runa`
- High-level vector operations
- Compiler intrinsics for auto-vectorization
- Platform-specific optimizations

### Phase 4: Hardware Acceleration

#### 4.1 Crypto Acceleration
- AES-NI support for encryption
- SHA extensions for hashing
- Random number generation (RDRAND)

#### 4.2 Machine Learning Acceleration
- AVX512 for neural networks
- Tensor operations
- GPU interface foundations

## Compiler Integration

### Intrinsic Recognition
The compiler will recognize `Machine.*` calls and optimize them:

```runa
Process called "optimize_machine_call" that takes call as FunctionCall returns Instruction:
    If call.name starts with "Machine.atomic_":
        Return generate_atomic_instruction(call)
    Else if call.name starts with "Machine.simd_":
        Return generate_simd_instruction(call)
    Otherwise:
        Return standard_call(call)
End Process
```

### Performance Guarantees
- `Machine.atomic_*` → Single atomic instruction
- `Machine.simd_*` → Single SIMD instruction
- `Machine.raw_syscall` → Direct syscall, no wrapper

## Security Considerations

### Privilege Levels
1. **Machine module** - Trusted, audited, minimal assembly
2. **Stdlib modules** - Built on machine, no direct assembly
3. **User code** - Cannot access machine module directly (future restriction)

### Volatile Operations
All security-critical operations marked `volatile` to prevent optimization:
- Memory zeroing
- Cryptographic operations
- Timing-sensitive code

## Benefits

### For Runa
- **True self-sufficiency** - Zero external dependencies
- **Maximum performance** - Direct hardware access
- **Future-proof** - New CPU features easily added
- **Security** - Proper volatile operations

### For Developers
- **Safe abstractions** - Never touch assembly
- **High performance** - Compiler intrinsics
- **Clear semantics** - Natural language APIs
- **Hardware features** - Automatic CPU detection

## Success Metrics

1. **Zero C dependencies** - Maintain current state
2. **Performance parity** - Match or exceed C/Rust
3. **API simplicity** - Natural language clarity
4. **Security audit** - Pass security review
5. **Platform coverage** - x86_64, ARM64, RISC-V

## Timeline

- **Week 1-2**: Implement Phase 1 (Foundation)
- **Week 3-4**: Begin Phase 2 (Stdlib Migration)
- **Month 2**: Complete Phase 2, begin Phase 3
- **Month 3**: Complete Phase 3, begin Phase 4
- **Month 4**: Complete Phase 4, optimization

## Conclusion

The machine module represents Runa's commitment to being a true systems language while maintaining its AI-first, natural language philosophy. By providing safe, high-level abstractions over raw hardware capabilities, we enable both maximum performance and maximum safety - the ultimate fulfillment of Runa's vision.