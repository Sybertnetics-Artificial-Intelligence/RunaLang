# Machine Code Architecture Plan

**Version:** 1.0
**Status:** Implementation Phase
**Last Updated:** 2025-01-23
**Classification:** Internal Technical Specification

---

## Overview

This document outlines the correct architecture for `backend/machine_code/` to support the intrinsic-based primitive system. The hybrid model maximizes code reuse while cleanly isolating platform-specific differences.

## Design Philosophy

**Architecture-First Grouping:**
- Group by CPU architecture (x86_64, ARM64, RISC-V, etc.)
- Share common instruction generation logic
- Isolate OS-specific differences in subdirectories

**Benefits:**
- **Maximum Code Reuse**: Instruction encoding is architecture-specific, not OS-specific
- **Clean Separation**: OS differences (syscalls) isolated in dedicated files
- **Maintainable**: Avoid duplicating complex backend logic across 18+ platforms
- **Scalable**: Easy to add new platforms for existing architectures

## Target Architecture

### Current Structure (Incorrect)
```
backend/machine_code/
├── aarch64/           # Generic ARM64
├── arm32/             # Generic ARM32
├── mips/              # Generic MIPS
├── powerpc/           # Generic PowerPC
├── riscv/             # Generic RISC-V
├── wasm/              # WebAssembly
├── x86/               # Generic x86
└── x86_64/            # Generic x86_64
```

### Target Structure (Correct)
```
backend/machine_code/
├── x86_64/
│   ├── instructions.runa      # Common x86_64 instructions (ADD, MOV, etc.)
│   ├── register_allocator.runa # Register allocation logic for x86_64
│   ├── calling_convention.runa # x86_64 calling conventions
│   └── syscalls/
│       ├── linux.runa         # Linux syscalls for x86_64
│       ├── windows.runa       # Windows syscalls for x86_64
│       └── darwin.runa        # macOS syscalls for x86_64
├── arm64/
│   ├── instructions.runa      # Common ARM64 instructions (LDR, STR, etc.)
│   ├── register_allocator.runa # Register allocation logic for ARM64
│   ├── calling_convention.runa # ARM64 calling conventions
│   └── syscalls/
│       ├── linux.runa         # Linux syscalls for ARM64
│       ├── darwin.runa        # macOS syscalls for ARM64
│       └── windows.runa       # Windows syscalls for ARM64
├── arm32/
│   ├── instructions.runa      # Common ARM32 instructions
│   ├── register_allocator.runa # Register allocation logic for ARM32
│   └── syscalls/
│       └── linux.runa         # Linux syscalls for ARM32
├── riscv64/
│   ├── instructions.runa      # Common RISC-V 64-bit instructions
│   ├── register_allocator.runa # Register allocation logic for RISC-V 64
│   └── syscalls/
│       ├── linux.runa         # Linux syscalls for RISC-V 64
│       └── freebsd.runa       # FreeBSD syscalls for RISC-V 64
├── riscv32/
│   ├── instructions.runa      # Common RISC-V 32-bit instructions
│   ├── register_allocator.runa # Register allocation logic for RISC-V 32
│   └── syscalls/
│       └── linux.runa         # Linux syscalls for RISC-V 32
├── mips64/
│   ├── instructions.runa      # Common MIPS 64-bit instructions
│   ├── register_allocator.runa # Register allocation logic for MIPS 64
│   └── syscalls/
│       ├── linux.runa        # Linux syscalls for MIPS 64
│       └── freebsd.runa       # FreeBSD syscalls for MIPS 64
├── mips32/
│   ├── instructions.runa      # Common MIPS 32-bit instructions
│   ├── register_allocator.runa # Register allocation logic for MIPS 32
│   └── syscalls/
│       ├── linux.runa         # Linux syscalls for MIPS 32
│       └── freebsd.runa       # FreeBSD syscalls for MIPS 32
├── powerpc/
│   ├── instructions.runa      # Common PowerPC instructions
│   ├── register_allocator.runa # Register allocation logic for PowerPC
│   └── syscalls/
│       ├── linux.runa         # Linux syscalls for PowerPC
│       └── aix.runa           # AIX syscalls for PowerPC
└── wasm/
    ├── instructions.runa      # WebAssembly instruction encoding
    ├── wasm_encoder.runa      # WASM bytecode generation
    ├── wasm_optimizer.runa    # WASM optimization passes
    └── wasi/
        └── wasi_interface.runa # WASI syscall interface
```

## Implementation Strategy

### Phase 1: Restructure Existing Directories
1. **Rename** `aarch64/` → `arm64/`
2. **Split** `riscv/` → `riscv32/` + `riscv64/`
3. **Split** `mips/` → `mips32/` + `mips64/`
4. **Keep** `x86_64/`, `arm32/`, `powerpc/`, `wasm/`

### Phase 2: Add Syscall Subdirectories
1. **Create** `syscalls/` subdirectory in each architecture
2. **Implement** platform-specific syscall files
3. **Migrate** syscall logic from `backend/syscalls/platforms/`

### Phase 3: Implement Intrinsic Support
1. **Add** intrinsic handling to each architecture
2. **Implement** `__intrinsic_syscall_*` functions
3. **Test** intrinsic-based primitive compilation

## Architecture-Specific Details

### x86_64
**Common Instructions:**
- Arithmetic: `ADD`, `SUB`, `MUL`, `DIV`
- Memory: `MOV`, `LEA`, `PUSH`, `POP`
- Control: `JMP`, `CALL`, `RET`, `CMP`
- SIMD: `SSE`, `AVX` instructions

**Platform-Specific Syscalls:**
- **Linux**: `syscall` instruction with System V ABI
- **Windows**: Win32 API calls (not direct syscalls)
- **macOS**: BSD syscalls with different ABI

### ARM64
**Common Instructions:**
- Arithmetic: `ADD`, `SUB`, `MUL`, `DIV`
- Memory: `LDR`, `STR`, `LDP`, `STP`
- Control: `B`, `BL`, `RET`, `CMP`
- SIMD: `NEON` instructions

**Platform-Specific Syscalls:**
- **Linux**: `svc #0` instruction with AAPCS ABI
- **macOS**: BSD syscalls with AAPCS ABI
- **Windows**: ARM64 Win32 API calls

### RISC-V
**Common Instructions:**
- Arithmetic: `ADD`, `SUB`, `MUL`, `DIV`
- Memory: `LW`, `SW`, `LB`, `SB`
- Control: `JAL`, `JALR`, `BEQ`, `BNE`
- Vector: `V` extension instructions

**Platform-Specific Syscalls:**
- **Linux**: `ecall` instruction with System V ABI
- **FreeBSD**: BSD syscalls with System V ABI

### WebAssembly
**Special Considerations:**
- **Virtual Machine**: Not physical CPU
- **WASI Interface**: WebAssembly System Interface
- **Sandboxed**: No direct OS access
- **Bytecode**: WASM bytecode, not assembly

## Migration Benefits

### Code Reuse
- **Instruction Encoding**: Write once per architecture
- **Register Allocation**: Share across all platforms
- **Optimization**: Architecture-specific, not platform-specific

### Maintainability
- **Single Source**: One file per instruction type
- **Clear Separation**: OS differences isolated
- **Easy Testing**: Test architecture logic independently

### Scalability
- **New Platforms**: Add syscall file only
- **New Architectures**: Add complete architecture directory
- **Cross-Platform**: Same instruction logic everywhere

## Implementation Timeline

### Week 1-2: Restructure
- Rename and split existing directories
- Create syscall subdirectories
- Update build system

### Week 3-4: Syscall Migration
- Move syscall logic from `backend/syscalls/platforms/`
- Implement platform-specific syscall files
- Test syscall functionality

### Week 5-6: Intrinsic Implementation
- Add intrinsic handling to each architecture
- Implement `__intrinsic_syscall_*` functions
- Test intrinsic-based compilation

### Week 7-8: Testing & Validation
- Comprehensive testing on all platforms
- Performance validation
- Documentation updates

## Success Criteria

### Technical
- [ ] All architectures support intrinsic syscalls
- [ ] Platform-specific syscalls work correctly
- [ ] No code duplication between platforms
- [ ] Build system supports new structure

### Performance
- [ ] Intrinsic syscalls have zero overhead
- [ ] Instruction generation is optimal
- [ ] Register allocation is efficient

### Maintainability
- [ ] Clear separation of concerns
- [ ] Easy to add new platforms
- [ ] Comprehensive documentation

## Related Documentation

- [INTRINSICS_SPECIFICATION.md](../compiler/frontend/primitives/INTRINSICS_SPECIFICATION.md)
- [Platform Primitives](../compiler/frontend/primitives/platform/)
- [Backend Syscalls](../compiler/backend/syscalls/)

---

**END OF DOCUMENT**
