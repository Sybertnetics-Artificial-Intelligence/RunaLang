# Machine Module Architecture Plan
**The Privileged Foundation of Runa's Zero-Dependency Architecture**

## What Is The Machine Module?

### **Core Definition**
The machine module is a **privileged, compiler-aware standard library module** that contains **ALL inline assembly** in Runa's standard library. It provides safe, high-level APIs for direct hardware and OS control while hiding the dangerous complexity of raw assembly from end users.

### **Architectural Position**
```
Layer 1: Application Code (99.9% of developers)
        ↓ uses
Layer 2: Standard Library (File, Socket, Thread, etc.) 
        ↓ uses
Layer 3: Machine Module ← THE ONLY PLACE WITH INLINE ASSEMBLY
        ↓ compiles to
Layer 4: Raw Machine Instructions
```

### **Key Principles**
1. **Single Source of Assembly**: The machine module is the ONLY place in the entire stdlib allowed to contain inline assembly
2. **Compiler Intrinsics**: The compiler recognizes `Machine.*` calls and optimizes them to single instructions
3. **Core Team Maintained**: Maintained with the same rigor as the compiler itself
4. **Safe Abstractions**: Provides safe, high-level APIs that hide assembly complexity
5. **Zero Dependencies**: Enables Runa to have absolutely no external dependencies

## Why The Machine Module Is Critical

### **Problem Analysis**

#### **Current State Problems:**
1. **Scattered Inline Assembly**: Currently, inline assembly exists in multiple places (`memory_core.runa`, `syscall.runa`, etc.)
2. **Placeholder Functions**: `stdlib/sys/memory/safety/secure.runa` has 30+ placeholder functions that need low-level operations
3. **No Safety Layer**: Direct primitive usage throughout stdlib without validation or error handling
4. **Missing Compiler Optimization**: No unified point for compiler to optimize low-level operations

#### **The Solution:**
The machine module consolidates ALL inline assembly into a single, privileged location that:
- Provides safe APIs for dangerous operations
- Enables compiler intrinsic optimizations
- Maintains platform portability internally
- Allows stdlib to be built entirely in safe Runa

### **Technical Justification for Stdlib Location**

After analysis, `runa/src/stdlib/core/machine/` is the optimal location because:

1. **Library Semantics**: It IS a library that users import via `Import "core/machine/..." as Machine`
2. **Discoverability**: Users expect to find it in stdlib, not hidden in compiler internals
3. **Compiler Integration**: The compiler can still recognize and optimize `Machine.*` calls
4. **Privilege Marking**: The `core/` subdirectory clearly indicates it's privileged
5. **Consistency**: Matches patterns in other languages (Rust's `core::intrinsics`, Go's `unsafe`)

## Module Structure and Contents

### **Directory Layout**
```
runa/src/stdlib/core/machine/
├── syscall.runa       # Raw system call interface (the ONLY syscall assembly)
├── atomic.runa        # Atomic operations (lock prefix instructions)
├── memory.runa        # Memory operations (volatile, barriers, secure zeroing)
├── cpu.runa          # CPU feature detection and control (CPUID, RDTSC)
├── simd.runa         # SIMD/vector operations (SSE, AVX, NEON)
└── platform.runa     # Platform-specific constants and detection
```

### **Module Contents**

#### **syscall.runa - System Call Interface**
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
        unified entry point for ALL OS operations in Runa.
        No other module should contain syscall assembly.
    @End Security_Scope
    
    @Performance_Hints
        Compiles to a single syscall instruction with zero overhead.
        Platform-specific implementations selected at compile time.
    @End Performance_Hints
    
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

#### **atomic.runa - Atomic Operations**
```runa
Process called "atomic_compare_and_swap" that takes 
    ptr as Pointer,
    expected as Integer,
    desired as Integer
returns Boolean:
    @Implementation
        Hardware atomic compare-and-swap using LOCK CMPXCHG.
        This is the foundation for all lock-free data structures.
    @End Implementation
    
    Let success as Boolean
    
    Inline Assembly volatile:
        "mov rax, %2"              Note: Load expected value
        "lock cmpxchg [%1], %3"    Note: Atomic CAS
        "sete %0"                  Note: Set success flag
        : "=r"(success)
        : "r"(ptr), "r"(expected), "r"(desired)
        : "rax", "memory", "flags"
    End Assembly
    
    Return success
End Process

Process called "atomic_add" that takes ptr as Pointer, value as Integer returns Integer:
    @Implementation
        Atomic fetch-and-add operation. Returns the old value.
        Compiles to a single LOCK XADD instruction.
    @End Implementation
    
    Let old_value as Integer
    
    Inline Assembly volatile:
        "lock xadd [%1], %2"
        "mov %0, %2"
        : "=r"(old_value)
        : "r"(ptr), "r"(value)
        : "memory"
    End Assembly
    
    Return old_value
End Process
```

#### **memory.runa - Memory Operations**
```runa
Process called "secure_zero_memory" that takes ptr as Pointer, size as Integer:
    @Security_Scope
        Securely zeros memory in a way that cannot be optimized out.
        Critical for cryptographic key material cleanup.
    @End Security_Scope
    
    Inline Assembly volatile:
        "mov rcx, %1"          Note: Size counter
        "mov rdi, %0"          Note: Destination pointer
        "xor al, al"           Note: Zero value
        "rep stosb"            Note: Fill with zeros
        "mfence"               Note: Memory barrier
        :
        : "r"(ptr), "r"(size)
        : "rcx", "rdi", "al", "memory"
    End Assembly
End Process

Process called "memory_fence":
    @Implementation
        Full memory barrier. Prevents CPU and compiler reordering.
    @End Implementation
    
    Inline Assembly volatile:
        "mfence"
        :
        :
        : "memory"
    End Assembly
End Process
```

#### **cpu.runa - CPU Control and Detection**
```runa
Process called "cpuid" that takes function as Integer returns CPUIDResult:
    @Implementation
        Execute CPUID instruction for CPU feature detection.
        Essential for runtime selection of optimized code paths.
    @End Implementation
    
    Let result be CPUIDResult
    
    Inline Assembly:
        "mov eax, %4"        Note: Function number
        "cpuid"              Note: Execute CPUID
        "mov %0, eax"        Note: Store EAX result
        "mov %1, ebx"        Note: Store EBX result  
        "mov %2, ecx"        Note: Store ECX result
        "mov %3, edx"        Note: Store EDX result
        : "=r"(result.eax), "=r"(result.ebx), "=r"(result.ecx), "=r"(result.edx)
        : "r"(function)
        : "eax", "ebx", "ecx", "edx"
    End Assembly
    
    Return result
End Process

Process called "rdtsc" returns Integer:
    @Implementation
        Read Time-Stamp Counter for high-precision timing.
        Returns CPU cycle count since boot.
    @End Implementation
    
    Let cycles as Integer
    
    Inline Assembly:
        "rdtsc"                    Note: Read timestamp counter
        "shl rdx, 32"              Note: Shift high 32 bits
        "or rax, rdx"              Note: Combine into 64-bit value
        "mov %0, rax"              Note: Store result
        : "=r"(cycles)
        :
        : "rax", "rdx"
    End Assembly
    
    Return cycles
End Process
```

## Migration Strategy

### **Phase 1: Consolidation (Week 1-2)**

**Objective**: Create the machine module and consolidate all inline assembly

1. **Create machine module structure** at `runa/src/stdlib/core/machine/`
2. **Move all inline assembly** from scattered locations:
   - From `compiler/frontend/primitives/assembly/syscall.runa` → `machine/syscall.runa`
   - From `compiler/frontend/primitives/core/memory_core.runa` → `machine/memory.runa`
   - From other scattered locations → appropriate machine module files
3. **Update existing primitives** to call machine module instead of using inline assembly

### **Phase 2: Stdlib Migration (Week 3-4)**

**Objective**: Update stdlib to use machine module exclusively

1. **Update `sys/memory/safety/secure.runa`**:
   - Replace 30+ placeholder functions with machine module calls
   - Example:
   ```runa
   Import "core/machine/memory" as Machine
   
   Process called "create_secure_buffer" that takes size as Integer, lock_memory as Boolean returns SecureBuffer:
       Let buffer be SecureBuffer
       Set buffer.data_ptr to allocate_memory(size)
       Machine.secure_zero_memory(buffer.data_ptr, size)
       
       If lock_memory:
           Let result be Machine.raw_syscall(SYS_MLOCK, buffer.data_ptr, size, 0, 0, 0, 0)
           If result is less than 0:
               Return error_buffer()
           End If
       End If
       
       Return buffer
   End Process
   ```

2. **Update all syscall usage** throughout stdlib to use `Machine.raw_syscall`
3. **Update all atomic operations** to use `Machine.atomic_*`
4. **Remove all other inline assembly** from stdlib

### **Phase 3: Compiler Integration (Month 2)**

**Objective**: Add compiler intrinsic recognition for optimization

1. **Add intrinsic recognition** in compiler:
   ```runa
   Process called "optimize_call" that takes call as FunctionCall returns Instruction:
       If call.module equals "core/machine/atomic" and call.function equals "atomic_add":
           Return generate_lock_xadd_instruction(call.arguments)
       Otherwise if call.module equals "core/machine/memory" and call.function equals "memory_fence":
           Return generate_mfence_instruction()
       Otherwise:
           Return standard_function_call(call)
       End If
   End Process
   ```

2. **Add platform-specific optimizations** for different architectures
3. **Validate performance** matches or exceeds current implementation

## Compiler Awareness and Optimization

### **Intrinsic Recognition**
The compiler will recognize specific machine module patterns and optimize them:

| Machine Module Call | Compiles To |
|-------------------|-------------|
| `Machine.atomic_add(ptr, val)` | Single `lock xadd` instruction |
| `Machine.atomic_compare_and_swap(ptr, exp, des)` | Single `lock cmpxchg` instruction |
| `Machine.memory_fence()` | Single `mfence` instruction |
| `Machine.raw_syscall(...)` | Direct `syscall` instruction |
| `Machine.rdtsc()` | `rdtsc` instruction pair |

### **Platform-Specific Compilation**
The compiler selects platform-specific implementations at compile time:
- x86_64: Intel/AMD specific instructions
- ARM64: ARM specific instructions (SVC instead of SYSCALL)
- RISC-V: RISC-V specific instructions
- WASM: Appropriate WASI calls

## Security and Safety Considerations

### **Privilege Levels**
1. **Machine Module**: Contains ALL inline assembly, maintained by core team only
2. **Standard Library**: Uses machine module, contains NO inline assembly
3. **User Applications**: Use stdlib, never directly access machine module

### **Safety Guarantees**
- **No Direct Assembly Access**: Users cannot write inline assembly
- **Validated Operations**: Machine module validates inputs where possible
- **Platform Abstraction**: Platform differences hidden from users
- **Compiler Verification**: Compiler ensures machine module usage is safe

### **Security Properties**
- **Secure Zeroing**: `secure_zero_memory` cannot be optimized out
- **Atomic Guarantees**: All atomic operations are truly atomic
- **Memory Barriers**: Proper ordering guarantees for concurrent code
- **Syscall Safety**: Centralized syscall interface for auditing

## Success Metrics

1. **✅ Zero External Dependencies**: No C library or external runtime needed
2. **✅ Single Assembly Location**: ALL inline assembly in machine module only
3. **✅ Placeholder Elimination**: All 30+ placeholders in secure.runa implemented
4. **✅ Performance Parity**: Machine module calls compile to single instructions
5. **✅ Platform Coverage**: x86_64, ARM64, RISC-V, WASM support
6. **✅ Compiler Integration**: Intrinsic optimization for all critical operations

## Implementation Timeline

| Phase | Duration | Deliverables |
|-------|----------|-------------|
| Phase 1: Consolidation | Week 1-2 | Machine module created, all assembly consolidated |
| Phase 2: Stdlib Migration | Week 3-4 | Stdlib updated to use machine module exclusively |
| Phase 3: Compiler Integration | Month 2 | Intrinsic optimizations implemented |
| Phase 4: Platform Expansion | Month 3 | ARM64, RISC-V support added |
| Phase 5: Advanced Features | Month 4 | SIMD operations, hardware crypto |

## Conclusion

The machine module is the **architectural keystone** that enables Runa to be a true systems programming language with zero external dependencies. By consolidating ALL inline assembly into a single, privileged, compiler-aware module maintained by the core team, we achieve:

1. **Maximum Safety**: Users never touch assembly
2. **Maximum Performance**: Compiler intrinsics ensure zero overhead
3. **Maximum Portability**: Platform differences hidden in machine module
4. **Maximum Security**: All dangerous operations in one auditable location

This design fulfills Runa's vision: **"The power of the low level, with the safety and simplicity of the high level."**

The machine module is where **Runa meets the metal, safely, efficiently, and elegantly.**

It is a **privileged, compiler-aware, core library** that is maintained by our team with the same rigor as the compiler itself.

Let's lay out the full, complete plan.

---

### **The `machine` Module: A Strategic Blueprint**

**Core Mission:** To provide a safe, stable, and high-level Runa API for direct, low-level machine and operating system control, abstracting away the danger and complexity of raw inline assembly from the end-user.

**Location:** `runa/stdlib/core/machine/`
*   It is part of the `stdlib` because it is a library that users will import and use.
*   It is in a `core` subdirectory to signify that it is a foundational, privileged part of the platform, not a normal library.

**Relationship to the Compiler:**
The `machine` module is special. The Runa compiler will be **aware of its existence** and will have special logic for optimizing its functions. When the compiler sees a call to `Machine.atomic_add`, it won't treat it like a normal function call. It will know that this specific call should be replaced with a single, hyper-optimized `lock add` assembly instruction. This is a technique called **"compiler intrinsics,"** and it's how you get the absolute best performance.

---

### **Roadmap for Implementation**

This is a multi-phase plan to build out this critical module.

#### **Phase 1: The Foundational Primitives (The "Kernel Bridge")**

**Objective:** To build the core, unsafe primitives that are the only parts of the standard library allowed to use inline assembly. This phase is about creating the fundamental bridge to the hardware.

*   **1.1. Create the Syscall Interface:**
    *   **File:** `runa/stdlib/core/machine/syscall.runa`
    *   **Content:** The `raw_syscall` process we designed previously. This will be the single, unified entry point for all operating system calls. It will be heavily documented as "unsafe and for internal use only."
*   **1.2. Create the Atomic Operations Interface:**
    *   **File:** `runa/stdlib/core/machine/atomic.runa`
    *   **Content:** A suite of processes for atomic operations (`atomic_add`, `atomic_compare_and_swap`, etc.). Each of these will be implemented using a small, specific, and volatile `Inline Assembly` block.
*   **1.3. Create the Memory Operations Interface:**
    *   **File:** `runa/stdlib/core/machine/memory.runa`
    *   **Content:** The `securely_zero_memory` process, as well as other primitives like `memory_copy_non_temporal` (a special, highly optimized memory copy for video or network buffers), and `cpu_cache_flush`.

#### **Phase 2: The Safe, High-Level OS Abstraction**

**Objective:** To build a beautiful, safe, and cross-platform Runa API on top of the dangerous primitives from Phase 1. This is the API that 99% of our other standard library modules will use.

*   **2.1. Build the File System API:**
    *   **File:** `runa/stdlib/os/file.runa`
    *   **Action:** Rewrite our existing file I/O library to use the `Machine.raw_syscall` primitive instead of relying on the FFI to a C library. This makes our file I/O **completely native to Runa.**
*   **2.2. Build the Networking API:**
    *   **File:** `runa/stdlib/net/socket.runa`
    *   **Action:** Rewrite our core socket library to use `Machine.raw_syscall` for creating sockets, binding ports, and sending/receiving data.
*   **2.3. Build the Concurrency Primitives:**
    *   **File:** `runa/stdlib/concurrent/mutex.runa`
    *   **Action:** Implement our Mutex and other synchronization primitives using the safe, atomic operations from `runa/stdlib/core/machine/atomic.runa`.

#### **Phase 3: The "Future-Proof" Hardware Abstraction**

**Objective:** To create the framework for giving Runa developers access to the latest, bleeding-edge CPU features without them ever needing to touch assembly.

*   **3.1. Build the CPU Feature Detection API:**
    *   **File:** `runa/stdlib/core/machine/cpu.runa`
    *   **Content:** A process called `cpu_supports_feature` that uses the `CPUID` assembly instruction to detect which features (e.g., AVX512, AES-NI) are available on the current machine.
*   **3.2. Implement the First Hardware-Accelerated Library:**
    *   **File:** `runa/stdlib/crypto/aes.runa`
    *   **Action:** Implement the AES encryption algorithm. It will have a check:
        ```runa
        If Machine.cpu_supports_feature with feature as "AES-NI":
            // Call an internal, privileged process that uses the
            // ENCRYPT_AES_256 inline assembly instruction.
        Otherwise:
            // Use a standard, safe, but slower Runa implementation of AES.
        ```
*   **3.3. Document the "Hardware Acceleration Request" Process:**
    *   Create a process for the community to request that our core team add support for new CPU instructions to the `machine` module in future Runa releases.

---

### **The Full List of Features for the `machine` Module**

This is the comprehensive list of functions that the `runa/stdlib/core/machine/` module should contain to cover all the essential needs of high-performance and systems-level developers.

#### **`syscall.runa`**
*   `raw_syscall`: The core, unsafe syscall dispatcher.

#### **`atomic.runa` (Safe Wrappers)**
*   `atomic_load`: Atomically reads a value from memory.
*   `atomic_store`: Atomically writes a value to memory.
*   `atomic_add` / `atomic_subtract`: Atomically adds/subtracts a value.
*   `atomic_and` / `atomic_or` / `atomic_xor`: Atomic bitwise operations.
*   `atomic_exchange`: Atomically swaps a value in memory.
*   `atomic_compare_and_swap`: The most critical atomic primitive. Atomically compares a value in memory and, if it matches an expected value, swaps it with a new one.

#### **`memory.runa` (Safe Wrappers)**
*   `securely_zero_memory`: The non-optimizable memory wipe function we designed.
*   `volatile_read` / `volatile_write`: Reads/writes from memory in a way the compiler is forbidden from re-ordering. Essential for device drivers.
*   `cpu_cache_flush`: A process to manually flush a specific line from the CPU's cache.
*   `prefetch_memory`: A hint to the CPU to start loading a piece of memory into its cache before it's actually needed.

#### **`cpu.runa` (Safe Wrappers)**
*   `cpu_supports_feature`: The CPUID-based feature detection.
*   `get_cpu_cycle_count`: A process that uses the `rdtsc` instruction to get the high-precision CPU timestamp counter. Essential for ultra-fine-grained performance benchmarking.
*   `cpu_pause`: A hint to the CPU (the `PAUSE` instruction) that is critical for implementing high-performance spin-locks without consuming massive amounts of power.

#### **`simd.runa` (The Advanced Vector API)**
*   This would be the most complex part of the module. It would provide a high-level API for SIMD (Single Instruction, Multiple Data) operations. A developer would not write assembly; they would write:
    ```runa
    Let vector_a be a value of type SIMD_Vector_Float32x8 with data as ...
    Let vector_b be a value of type SIMD_Vector_Float32x8 with data as ...
    
    Let vector_sum be Machine.simd_add with a as vector_a and b as vector_b
    ```
    Under the hood, the compiler would translate `Machine.simd_add` into a single `VADDPS` (Vector Add Packed Single-Precision) assembly instruction.

This comprehensive `machine` module, built by our core team using the raw `Inline Assembly` feature, is the perfect architectural solution. It fully delivers on the promise of Runa: **the power of the low level, with the safety and simplicity of the high level.**

example:

Let's walk through a complete, concrete example.

We will use one of the most important and common use cases: creating a **thread-safe counter**. This is a fundamental building block in any concurrent program, and it is a perfect showcase for why the `machine` module is so powerful.

---

### **The Problem: The "Race Condition"**

Imagine you are building a web server and you want to count the total number of requests. The simplest code would be:

```runa
Let total_requests be 0

// This process is called by many different threads at the same time
Process called "handle_new_request":
    // This line is DANGEROUS!
    Set total_requests to total_requests plus 1
```

This code is **dangerously broken** in a multi-threaded environment. Two threads might read the value of `total_requests` (let's say it's 100) at the same time. Both will calculate `100 + 1`. Both will then write `101` back. You just received two requests, but your counter only went up by one. This is called a **race condition.**

### **The Solution: Using the `machine` Module for Atomic Operations**

The `machine` module provides the safe, high-level tool to solve this problem without the developer ever needing to think about assembly.

Here is the corrected, perfectly thread-safe Runa code.

```runa
// First, we import the machine module to get access to its capabilities
Import "stdlib/core/machine" as Machine

// We declare our counter. It is a standard Integer.
Let total_requests be 0

// This process is now completely thread-safe
Process called "handle_new_request":
    // This is the key line.
    // We are not using a simple 'plus'. We are calling the special,
    // atomic_add process from the machine module.
    Machine.atomic_add with target as total_requests and value as 1
```

---

### **What is Actually Happening Under the Hood? (The Compiler's View)**

This is the magic. The developer wrote a single, beautiful, and clear line of Runa. But because the Runa compiler is **aware of the `machine` module**, it knows this is not a normal function call. It will perform a series of sophisticated steps to generate the most efficient and correct low-level code.

**1. The Developer Writes the High-Level Code:**
```runa
Machine.atomic_add with target as total_requests and value as 1
```

**2. The Compiler Sees the "Intrinsic" Call:**
The compiler recognizes `Machine.atomic_add` as a special **compiler intrinsic**. It knows that it shouldn't generate a normal function call. Instead, it should look up the internal implementation for this specific process.

**3. The Compiler "Opens Up" the `machine` Module:**
The compiler effectively looks at the source code you and your team wrote for `stdlib/core/machine/atomic.runa`:

```runa
// Inside stdlib/core/machine/atomic.runa
Process called "atomic_add" that takes target as Integer and value as Integer:
    Inline Assembly volatile:
        // This is the secret sauce. The 'lock' prefix is a special
        // CPU command that ensures this 'add' operation is atomic.
        // It guarantees that no other thread can interrupt it.
        "lock add [ %0 ], %1\n"   Note: Atomically add the value to the memory location.
        :
        : "r"(target), "r"(value)
        : "memory", "cc"
    End Assembly
```

**4. The Compiler Generates the Final Machine Code:**
Instead of generating a complex function call, the compiler takes the assembly code from the intrinsic and **pastes it directly** into the machine code for the `handle_new_request` process.

The final, compiled machine code for that single line of Runa will be the equivalent of:

```assembly
; ... some setup code ...
lock add [address_of_total_requests], 1
; ... some cleanup code ...
```

---

### **The Result: The Best of Both Worlds**

*   **The Developer's Experience:** The developer wrote a single, clear line of code that reads like English. They never saw the word `lock` or `add` or `[ %0 ]`. They simply asked the `machine` to perform a safe, atomic addition.
*   **The Machine's Execution:** The final program is running a **single, hyper-optimized, and fundamentally thread-safe CPU instruction.** There is zero overhead. It is the most performant and correct way to solve this problem.

This is the power of the `machine` module. It gives every Runa developer the **performance and power of an expert systems programmer** while maintaining the **safety and simplicity of a high-level language.**