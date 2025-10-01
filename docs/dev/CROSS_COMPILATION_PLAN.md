# Runa Cross-Compilation Plan

**Goal:** Enable Runa to compile programs for multiple platforms and architectures from a single host machine.

**Status:** Planning Phase (Target: v0.9.0 or v1.1.0)

---

## 🎯 Overview

Cross-compilation allows developers to:
- Compile Windows binaries on Linux
- Compile macOS binaries on Windows
- Compile ARM binaries on x86-64
- Compile WASM from any platform

**Philosophy:** Build it entirely in Runa - no external dependencies (no Rust, no LLVM required for basic cross-compilation).

---

## 📅 Phased Approach

### Current State (v0.0.7.5)
- ✅ Compiles Runa → x86-64 Linux ELF binaries
- ✅ Self-hosting
- ⚠️ Single platform only (Linux x86-64)

### Phase 1: Foundation (v0.0.8 - v0.8.0)
**Focus:** Perfect single-platform compilation

**Goals:**
- Stable Linux x86-64 compiler
- Full language features
- Comprehensive standard library
- Excellent performance

**Rationale:** Must master one platform before supporting multiple.

### Phase 2: Abstraction (v0.9.0)
**Focus:** Make codegen target-aware

**Goals:**
- Abstract architecture-specific code
- Separate platform-specific syscalls
- Design target selection API
- Prepare for multiple backends

### Phase 3: Multi-Platform (v1.1.0+)
**Focus:** Add additional platforms incrementally

**Priority Order:**
1. x86-64 Linux (v0.0.7.5 ✅)
2. x86-64 Windows (PE format)
3. x86-64 macOS (Mach-O format)
4. ARM64 Linux
5. ARM64 macOS (Apple Silicon)
6. WASM (browsers, WASI)

---

## 🏗️ Architecture Design

### Target Abstraction

```runa
# Target triple: <arch>-<os>-<abi>
# Examples: x86_64-linux-gnu, x86_64-windows-msvc, aarch64-darwin-macho

Type called "Target":
    arch as String        # "x86_64", "aarch64", "wasm32"
    os as String          # "linux", "windows", "darwin", "wasi"
    abi as String         # "gnu", "msvc", "darwin", "wasi"
    format as String      # "elf64", "pe", "macho", "wasm"
    endian as String      # "little", "big"
    pointer_size as Integer  # 4 (32-bit) or 8 (64-bit)
End Type

Process called "target_from_triple" takes triple as String returns Integer:
    # Parse "x86_64-linux-gnu" → Target struct
    # Returns pointer to Target
End Process
```

### Usage

```bash
# Compile for current platform (default):
runac program.runa -o program

# Cross-compile for Windows:
runac --target=x86_64-windows program.runa -o program.exe

# Cross-compile for macOS:
runac --target=x86_64-darwin program.runa -o program

# Cross-compile for ARM64 Linux:
runac --target=aarch64-linux program.runa -o program-arm

# Compile to WebAssembly:
runac --target=wasm32-wasi program.runa -o program.wasm

# List available targets:
runac --list-targets
```

---

## 🔧 Implementation Details

### 1. Multi-Backend Codegen

**Current (v0.0.7.5):**
```
src/codegen.runa  → Generates x86-64 assembly only
```

**Future (v0.9.0+):**
```
src/codegen/
├── codegen_common.runa      # Shared logic (AST traversal, etc.)
├── codegen_x86_64.runa      # x86-64 instruction generation
├── codegen_aarch64.runa     # ARM64 instruction generation
├── codegen_wasm.runa        # WASM bytecode generation
└── codegen_riscv.runa       # RISC-V (future)
```

**Architecture:**
```runa
Process called "codegen_generate" takes program as Integer, target as Integer returns Integer:
    Let arch be memory_get_pointer(target, 0)  # target->arch

    If string_equals(arch, "x86_64") is equal to 1:
        Return codegen_x86_64_generate(program, target)
    Otherwise If string_equals(arch, "aarch64") is equal to 1:
        Return codegen_aarch64_generate(program, target)
    Otherwise If string_equals(arch, "wasm32") is equal to 1:
        Return codegen_wasm_generate(program, target)
    Otherwise:
        Print "Unsupported architecture: "
        Print arch
        exit_with_code(1)
    End If
End Process
```

---

### 2. Multi-Format Object Writer

**Current (v0.0.9 Plan):**
```
src/object_writer.runa  → Writes ELF64 only
```

**Future (v1.1.0+):**
```
src/formats/
├── elf64.runa           # ELF 64-bit format (Linux, BSD)
├── pe.runa              # PE format (Windows)
├── macho.runa           # Mach-O format (macOS, iOS)
├── wasm.runa            # WebAssembly module format
└── format_common.runa   # Shared utilities
```

**Format Selection:**
```runa
Process called "write_object_file" takes code as Integer, target as Integer, filename as String returns Integer:
    Let format be memory_get_pointer(target, 24)  # target->format

    If string_equals(format, "elf64") is equal to 1:
        Return write_elf64(code, target, filename)
    Otherwise If string_equals(format, "pe") is equal to 1:
        Return write_pe(code, target, filename)
    Otherwise If string_equals(format, "macho") is equal to 1:
        Return write_macho(code, target, filename)
    Otherwise If string_equals(format, "wasm") is equal to 1:
        Return write_wasm(code, target, filename)
    End If
End Process
```

---

### 3. Cross-Platform Standard Library

**Challenge:** System calls differ across platforms.

**Solution:** Platform abstraction layer.

```runa
# Public API (platform-independent):
Process called "file_open" takes path as String, mode as Integer returns Integer:
    Let target be get_current_target()
    Let os be memory_get_pointer(target, 8)  # target->os

    If string_equals(os, "linux") is equal to 1:
        Return file_open_linux(path, mode)
    Otherwise If string_equals(os, "windows") is equal to 1:
        Return file_open_windows(path, mode)
    Otherwise If string_equals(os, "darwin") is equal to 1:
        Return file_open_darwin(path, mode)
    Otherwise If string_equals(os, "wasi") is equal to 1:
        Return file_open_wasi(path, mode)
    End If
End Process

# Platform-specific implementations:
Process called "file_open_linux" takes path as String, mode as Integer returns Integer:
    # Linux syscall: open (2)
    Inline Assembly:
        mov $2, %rax           # syscall: open
        movq -8(%rbp), %rdi    # path
        movq -16(%rbp), %rsi   # mode
        syscall
    End Assembly
    Return 0
End Process

Process called "file_open_windows" takes path as String, mode as Integer returns Integer:
    # Windows API: CreateFileA
    # Call Win32 API (requires different calling convention)
End Process

Process called "file_open_darwin" takes path as String, mode as Integer returns Integer:
    # macOS syscall: open (2) - similar to Linux
End Process

Process called "file_open_wasi" takes path as String, mode as Integer returns Integer:
    # WASI: fd_open
End Process
```

**Standard Library Structure:**
```
stdlib/
├── io/
│   ├── io_common.runa       # Public API
│   ├── io_linux.runa        # Linux syscalls
│   ├── io_windows.runa      # Windows API
│   ├── io_darwin.runa       # macOS syscalls
│   └── io_wasi.runa         # WASI functions
├── fs/
│   ├── fs_common.runa
│   ├── fs_linux.runa
│   ├── fs_windows.runa
│   └── fs_darwin.runa
└── net/
    ├── net_common.runa
    ├── net_posix.runa       # Linux/macOS/BSD
    └── net_windows.runa     # Winsock
```

---

## 📋 Platform-Specific Details

### 1. x86-64 Windows (PE Format)

**File Format:** PE (Portable Executable)
**Calling Convention:** Microsoft x64 (different from System V!)
**System API:** Win32 API (no direct syscalls)

**Key Differences from Linux:**
- Arguments passed in: RCX, RDX, R8, R9 (not RDI, RSI, RDX, RCX)
- Shadow space: 32 bytes reserved on stack
- Different system calls (via kernel32.dll, not syscall instruction)
- No direct syscalls - must use DLLs

**Example:**
```runa
# Windows x64 function call:
Process called "windows_print" takes message as String:
    Inline Assembly:
        # Windows x64 ABI:
        # RCX = first argument
        # RDX = second argument
        # R8 = third argument
        # R9 = fourth argument
        # Stack must have 32-byte shadow space

        sub $32, %rsp           # Allocate shadow space
        movq -8(%rbp), %rcx     # Load message into RCX (first arg)
        call WriteConsoleA      # Windows API function
        add $32, %rsp           # Clean up shadow space
    End Assembly
End Process
```

**Implementation Priority:** v1.1.0

---

### 2. x86-64 macOS (Mach-O Format)

**File Format:** Mach-O (Mach Object)
**Calling Convention:** System V (same as Linux)
**System API:** BSD syscalls (similar to Linux)
**Challenge:** Code signing required on Apple Silicon

**Key Differences from Linux:**
- Different syscall numbers
- Requires code signature (on ARM64)
- Different dynamic linker
- Different section names

**Example:**
```runa
# macOS syscall (write):
Process called "macos_write" takes fd as Integer, buffer as String, length as Integer returns Integer:
    Inline Assembly:
        mov $0x2000004, %rax    # macOS syscall: write (0x2000000 + 4)
        movq -8(%rbp), %rdi     # fd
        movq -16(%rbp), %rsi    # buffer
        movq -24(%rbp), %rdx    # length
        syscall
    End Assembly
    Return 0
End Process
```

**Implementation Priority:** v1.1.0

---

### 3. ARM64 Linux (ELF Format)

**Architecture:** AArch64
**File Format:** ELF64 (same as x86-64)
**Calling Convention:** AAPCS64
**System API:** Linux syscalls (same numbers as x86-64)

**Key Differences from x86-64:**
- Different instruction set (ARM vs x86)
- Different registers (X0-X30 vs RAX-R15)
- Different syscall instruction (SVC vs SYSCALL)

**Example:**
```runa
# ARM64 syscall (exit):
Process called "arm64_exit" takes code as Integer:
    Inline Assembly:
        mov x8, #93        // syscall: exit
        ldr x0, [fp, #-8]  // load exit code
        svc #0             // invoke syscall
    End Assembly
End Process
```

**Implementation Priority:** v1.2.0

---

### 4. WebAssembly (WASM Format)

**Architecture:** Stack-based VM
**File Format:** WASM binary module
**System API:** WASI (WebAssembly System Interface)

**Key Differences:**
- Not native code - bytecode for VM
- No registers - stack-based
- Sandbox environment
- Limited system access

**Example:**
```runa
# WASM doesn't use assembly - generates bytecode directly
Process called "wasm_add" takes a as Integer, b as Integer returns Integer:
    # Codegen emits WASM instructions:
    # local.get 0    (load a)
    # local.get 1    (load b)
    # i32.add        (add)
    Return a plus b
End Process
```

**Implementation Priority:** v1.3.0

---

## 🛠️ Development Plan

### v0.9.0: Target Abstraction

**Tasks:**
1. Create `Target` type and parser
2. Refactor codegen to accept target parameter
3. Separate x86-64-specific code from generic code
4. Add `--target` flag to compiler
5. Implement target detection (host platform)

**Success Criteria:**
- Can specify target (even if only x86-64 Linux works)
- Architecture clearly separated
- Foundation for adding new targets

---

### v1.1.0: Windows Support

**Tasks:**
1. Implement PE object writer
2. Implement x86-64 Windows codegen (Microsoft ABI)
3. Port standard library to Windows (Win32 API)
4. Test on Windows
5. Add Windows to CI/CD

**Success Criteria:**
- Cross-compile Windows binaries from Linux
- Windows binaries run correctly
- Standard library works on Windows

---

### v1.2.0: macOS Support

**Tasks:**
1. Implement Mach-O object writer
2. Handle macOS syscall differences
3. Port standard library to macOS
4. Test on macOS (x86-64 and ARM64)
5. Handle code signing requirements

**Success Criteria:**
- Cross-compile macOS binaries from Linux
- macOS binaries run correctly
- Apple Silicon support

---

### v1.3.0: ARM64 & WASM

**Tasks:**
1. Implement ARM64 codegen
2. Implement WASM bytecode generator
3. Test on Raspberry Pi / ARM servers
4. Test WASM in browser and Node.js

**Success Criteria:**
- Cross-compile ARM64 binaries
- Cross-compile WASM modules
- Both targets work correctly

---

## 🚫 What We're NOT Doing

### NOT Using Rust

**Why people use Rust for cross-compilation:**
- `cargo build --target=<triple>` just works
- LLVM handles all backends
- Pre-built toolchains available

**Why we're NOT using Rust:**
- ✅ We want Runa to be self-sufficient
- ✅ No external dependencies
- ✅ Full control over codegen
- ✅ Smaller binary size
- ✅ Educational value

**Trade-off:**
- ⚠️ More work (we write each backend)
- ⚠️ Less optimization (no LLVM... yet)

---

### NOT Building LLVM (Initially)

**LLVM is NOT the same as AOTT** - they solve different problems:

#### LLVM:
- **What it is:** Compiler infrastructure library
- **What it does:** IR → optimized native code for many targets
- **Benefits:** World-class optimization, many backends (x86, ARM, WASM, etc.)
- **Trade-offs:** Large dependency (100+ MB), slower compilation

#### AOTT (All-Of-The-Time):
- **What it is:** Runtime execution strategy
- **What it does:** Continuous optimization during program execution
- **Benefits:** Adapts to actual runtime behavior, no warmup penalty
- **Trade-offs:** More complex runtime

**They're complementary, not alternatives!**

---

## 🤔 LLVM vs Custom Backend: The Decision

### Option A: Custom Backends (v1.1-v1.3)

**Pros:**
- ✅ Zero dependencies
- ✅ Fast compilation
- ✅ Small binary (~500KB)
- ✅ Full control
- ✅ Simple architecture

**Cons:**
- ⚠️ Write each backend manually
- ⚠️ Less optimization than LLVM
- ⚠️ More maintenance burden

**Good for:** Getting to multi-platform quickly, educational purposes

---

### Option B: LLVM Backend (v1.4+)

**Architecture:**
```
Runa source → Parse → AST → LLVM IR → LLVM Optimization → Native code (any target)
```

**Pros:**
- ✅ All targets "for free" (x86, ARM, WASM, RISC-V, etc.)
- ✅ World-class optimization
- ✅ Well-tested backends
- ✅ JIT support (for AOTT T2-T4)

**Cons:**
- ⚠️ Large dependency (LLVM is 100+ MB)
- ⚠️ Slower compilation
- ⚠️ More complex build process

**Good for:** Maximum performance, wide platform support

---

### Recommended Hybrid Approach

**v1.0-v1.3:** Custom backends
- Master x86-64 Linux
- Add Windows, macOS, ARM64 manually
- Fast compilation, zero dependencies

**v1.4+:** Add LLVM as OPTIONAL backend
```bash
# Use custom backend (fast compile, good performance):
runac program.runa -o program

# Use LLVM backend (slow compile, best performance):
runac --backend=llvm program.runa -o program

# Use LLVM for specific target:
runac --backend=llvm --target=riscv64-linux program.runa -o program
```

**Best of both worlds:**
- Default: Fast custom backend
- Optional: LLVM for maximum performance/platforms

---

## 🔄 AOTT + LLVM Integration (Future)

**AOTT is a runtime strategy, LLVM is a compiler infrastructure - they work together!**

### AOTT Tier Implementation with LLVM:

```
Tier 0 (Lightning): Interpreter
    ↓ (hot code detected)
Tier 1 (Smart Bytecode): Enhanced interpreter
    ↓ (hotter code detected)
Tier 2 (Basic Native): LLVM -O0 compilation
    ↓ (hottest code detected)
Tier 3 (Optimized Native): LLVM -O2 compilation
    ↓ (ultra-hot code detected)
Tier 4 (Speculative): LLVM -O3 + PGO + speculative inlining
```

**How LLVM helps AOTT:**
- **T2-T4:** Use LLVM JIT to compile hot code at runtime
- **Optimization:** LLVM provides optimization passes for T3-T4
- **Flexibility:** Deoptimize back to T0 if speculation fails

**Architecture:**
```runa
Process called "aott_tier2_compile" takes function as Integer returns Integer:
    # Convert Runa IR to LLVM IR
    Let llvm_ir be generate_llvm_ir(function)

    # JIT compile with LLVM
    Let native_code be llvm_jit_compile(llvm_ir, "-O0")

    # Return function pointer to compiled code
    Return native_code
End Process
```

**This is a v2.0+ feature** - far future, but LLVM enables it.

---

## 📊 Format Complexity Comparison

| Format | Platform | Difficulty | Lines of Code (est.) | Priority |
|--------|----------|------------|---------------------|----------|
| **ELF64** | Linux | ⭐⭐⭐ Medium | ~1000 LOC | v0.0.9 ✅ |
| **PE** | Windows | ⭐⭐⭐⭐ Hard | ~2000 LOC | v1.1.0 |
| **Mach-O** | macOS | ⭐⭐⭐⭐ Hard | ~2000 LOC | v1.2.0 |
| **WASM** | Web | ⭐⭐ Easy | ~500 LOC | v1.3.0 |

**Why ELF is easiest:**
- Well-documented specification
- Simpler structure (sections, symbols, relocations)
- No code signing requirements
- Open-source tooling for reference

**Why PE/Mach-O are harder:**
- Complex import/export tables
- Code signing (macOS)
- Platform-specific quirks
- Less documentation

---

## 🎯 Summary

### Short Answer:
**When:** v0.9.0 (abstraction), v1.1.0+ (actual cross-compilation)
**How:** Pure Runa - no Rust needed
**LLVM:** Optional in v1.4+ for extra performance/platforms

### Strategy:
1. **v0.0.8-v0.8.0:** Perfect Linux x86-64
2. **v0.9.0:** Abstract codegen for multiple targets
3. **v1.1.0:** Add Windows (PE format)
4. **v1.2.0:** Add macOS (Mach-O format)
5. **v1.3.0:** Add ARM64 + WASM
6. **v1.4.0+:** Optionally add LLVM backend

### AOTT vs LLVM:
- **AOTT:** Runtime optimization strategy (5-tier execution)
- **LLVM:** Compiler infrastructure (IR + optimization + backends)
- **Together:** LLVM can power AOTT tiers 2-4 (optional, future)

### Philosophy:
Build a **self-sufficient compiler** first, add **LLVM as optional backend** later for users who want maximum performance or exotic platforms.

---

## 🔗 Related Documents

- [Development Roadmap](./DEVELOPMENT_ROADMAP.md)
- [AOTT Architecture Plan](../../archived/docs/plans/RUNA_AOTT_ARCHITECTURE_PLAN.md)
- [v0.0.9 Milestone](./milestones/V0.0.9_NATIVE_OBJECT_LINKER.md)

---

**Status:** Planning Document
**Target Implementation:** v0.9.0 (abstraction), v1.1.0+ (platforms)
