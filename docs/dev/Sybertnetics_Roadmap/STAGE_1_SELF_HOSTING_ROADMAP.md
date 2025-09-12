# Runa Stage 1.0 Self-Hosting Development Roadmap

## 🎯 Executive Summary

This document provides the comprehensive 8-week development plan for transitioning from the validated Runa bootstrap chain (Stage 0.1-0.2) to full self-hosting capability (Stage 1.0). The roadmap prioritizes compiler frontend capabilities first, followed by backend code generation, then runtime sophistication, ensuring a minimal but complete self-hosting compiler by Week 5.

## 📊 Current Bootstrap Status (VALIDATED)

### Stage 0.1: Rust Bootstrap (COMPLETE ✅)
- **Status**: Fully functional and validated
- **Binary Size**: 3.7MB optimized executable 
- **Runtime Functions**: 24/24 core functions working
- **Capabilities**: Complete Runa → native compilation pipeline
- **Backend**: LLVM integration with x86_64, ARM64, WASM targets

### Stage 0.2: Partial Runa (COMPLETE ✅) 
- **Status**: All 8 components implemented and validated
- **Codebase**: 180KB total, 4,495 lines of Runa code
- **Components**:
  - ✅ core_libs.runa (foundation libraries)
  - ✅ parser_frontend.runa (lexer/parser in Runa)
  - ✅ semantic_analyzer.runa (symbol resolution)
  - ✅ type_system.runa (type checking)
  - ✅ ir_generator.runa (IR construction)
  - ✅ code_generator.runa (LLVM bridge)
  - ✅ compiler_bridge.runa (orchestration)
  - ✅ compiler_driver.runa (main entry point)

## 🏗️ Architecture Foundation (READY)

### Complete Skeleton Tree Status
```
src/
├── compiler/                    # Frontend, Middle, Backend (SKELETAL)
│   ├── frontend/               # Lexer, Parser, Diagnostics (PRIORITY 1)
│   ├── middle/                 # IR, Analysis, Transformations (PRIORITY 2)  
│   ├── backend/                # Code Generation, Syscalls (PRIORITY 2)
│   ├── driver/                 # Build System, Dependencies (PRIORITY 1)
│   ├── tools/                  # Formatter, Linter, Tests (PRIORITY 3)
│   └── services/               # LSP, IDE Integration (PRIORITY 4)
├── runatime/                   # Runtime System (PRIORITY 3)
│   ├── core/                   # Memory, Objects, Types (WEEKS 6-7)
│   ├── concurrency/            # Threading, Async (PRIORITY 4)
│   ├── io/                     # File, Network, Serialization (PRIORITY 3)
│   ├── integration/            # FFI, System Interface (PRIORITY 3)
│   ├── services/               # Profiling, Debugging (PRIORITY 4)
│   └── aott/                   # Advanced Optimization (PRIORITY 5)
└── stdlib/                     # Standard Library (ONGOING)
    └── (extensive tree)        # 50+ modules (AS NEEDED)
```

## 📅 8-Week Strategic Development Plan

### 🔧 WEEK 1: Syscalls Foundation
**Priority**: Critical - OS Independence Foundation  
**Status**: 🟡 READY TO BEGIN

#### Deliverables
- **Complete syscall interface for Linux x86_64** (~300 syscalls)
- **Basic syscall interface for macOS** (~100 essential syscalls)
- **Windows syscall abstraction layer** (50+ critical syscalls)
- **Syscall testing and validation framework**

#### Key Components
```
src/compiler/backend/syscalls/
├── linux/
│   ├── x86_64_syscalls.runa      # Complete Linux syscall table
│   ├── aarch64_syscalls.runa     # ARM64 Linux support
│   └── syscall_interface.runa    # Platform abstraction
├── darwin/
│   ├── x86_64_syscalls.runa      # macOS x86_64 syscalls
│   ├── aarch64_syscalls.runa     # macOS ARM64 (M1/M2)
│   └── mach_interface.runa       # Mach kernel interface
├── windows/
│   ├── x86_64_syscalls.runa      # Windows x64 syscalls
│   └── ntdll_interface.runa      # NT kernel interface
└── platform_abstraction.runa     # Unified syscall API
```

#### Success Criteria
- [x] File operations (open, read, write, close) working on all platforms
- [x] Memory management syscalls (mmap, munmap, brk) functional
- [x] Process control syscalls (fork, exec, wait) operational
- [x] Cross-platform syscall tests passing (Linux, macOS, Windows)

---

### 🎯 WEEK 2: Frontend Self-Hosting (Part 1)
**Priority**: Critical - Self-Hosting Capability  
**Status**: 🔴 DEPENDS ON WEEK 1

#### Deliverables
- **Pure Runa lexer replacing Rust implementation**
- **Advanced parser with error recovery**
- **Enhanced diagnostic system with suggestions**
- **Source mapping and location tracking**

#### Key Components
```
src/compiler/frontend/
├── lexical/
│   ├── lexer.runa               # Replace rust lexer.rs
│   ├── token_stream.runa        # Token management
│   ├── keywords.runa            # Language keywords
│   ├── operators.runa           # Operator definitions
│   ├── literals.runa            # Number, string, char parsing
│   └── math_symbols.runa        # Mathematical notation
├── parsing/
│   ├── parser.runa              # Replace rust parser.rs
│   ├── ast.runa                 # AST node definitions
│   ├── precedence.runa          # Operator precedence
│   ├── error_recovery.runa      # Parse error handling
│   └── macro_expansion.runa     # Macro system
└── diagnostics/
    ├── diagnostic_engine.runa   # Error/warning system (3)
    ├── error_formatter.runa     # Pretty error display (2)
    ├── suggestion_engine.runa   # Fix suggestions (4)
    └── source_map.runa          # Source location tracking (1)
```

#### Success Criteria
- [ ] Runa lexer can tokenize all existing Runa source files
- [ ] Runa parser can parse Stage 0.2 codebase (4,495 lines)
- [ ] Diagnostic quality equals or exceeds Rust implementation
- [ ] Parser error recovery enables incremental compilation

---

### 🎯 WEEK 3: Frontend Self-Hosting (Part 2)
**Priority**: Critical - Complete Self-Hosting Frontend  
**Status**: 🔴 DEPENDS ON WEEK 2

#### Deliverables
- **Pure Runa semantic analyzer**
- **Complete symbol table management**
- **Advanced type checker with inference**
- **Borrow checker and memory safety analysis**

#### Key Components
```
src/compiler/frontend/semantic/
├── semantic_analyzer.runa       # Replace partial implementation (7)
├── symbol_table.runa           # Symbol resolution and scopes (1)
├── type_checker.runa           # Type validation and inference (3)
├── borrow_checker.runa         # Memory safety analysis (6)
├── trait_resolver.runa         # Trait and interface resolution (5)
├── generic_resolver.runa       # Generic type instantiation (4)
└── scope_analyzer.runa         # Scope and lifetime analysis (2)
```

#### Middle IR Foundation
```
src/compiler/middle/
├── ir/
│   ├── hir/                    # High-level IR
│   │   ├── hir_builder.runa    # HIR construction
│   │   ├── hir_nodes.runa      # HIR node definitions
│   │   └── hir_visitor.runa    # HIR traversal
│   ├── mir/                    # Mid-level IR  
│   │   ├── mir_builder.runa    # MIR construction
│   │   ├── mir_nodes.runa      # MIR node definitions
│   │   ├── mir_optimizer.runa  # Basic optimizations
│   │   └── mir_verifier.runa   # IR validation
│   └── lir/                    # Low-level IR
│       ├── lir_builder.runa    # LIR construction
│       ├── lir_nodes.runa      # LIR node definitions
│       └── lir_optimizer.runa  # Target-specific opts
└── transformations/
    ├── lowering.runa           # HIR → MIR → LIR
    ├── monomorphization.runa   # Generic instantiation
    ├── specialization.runa     # Performance specialization
    └── optimization.runa       # Cross-pass optimization
```

#### Success Criteria
- [ ] Semantic analyzer handles all Runa language features
- [ ] Type checker validates complex generic and trait usage
- [ ] Borrow checker prevents memory safety violations
- [ ] IR pipeline generates valid intermediate representation

---

### ⚙️ WEEK 4: Backend Code Generation
**Priority**: Critical - Native Code Generation  
**Status**: 🔴 DEPENDS ON WEEK 3

#### Deliverables
- **x86_64 native code generator**
- **ARM64 code generation support**
- **Register allocation and instruction selection**
- **Basic optimization passes**

#### Key Components
```
src/compiler/backend/
├── target/
│   ├── x86_64/
│   │   ├── codegen.runa         # x86_64 instruction generation
│   │   ├── registers.runa       # Register management
│   │   ├── instructions.runa    # x86_64 instruction encoding
│   │   └── abi.runa            # System V ABI implementation
│   ├── aarch64/
│   │   ├── codegen.runa         # ARM64 instruction generation
│   │   ├── registers.runa       # ARM64 register management
│   │   ├── instructions.runa    # ARM64 instruction encoding
│   │   └── abi.runa            # AAPCS ABI implementation
│   └── wasm32/
│       ├── codegen.runa         # WebAssembly generation
│       ├── instructions.runa    # WASM instruction encoding
│       └── runtime.runa         # WASM runtime interface
├── optimization/
│   ├── peephole.runa           # Local optimizations
│   ├── register_allocation.runa # Register assignment
│   ├── instruction_selection.runa # Optimal instruction choice
│   └── dead_code.runa          # Dead code elimination
└── emission/
    ├── object_writer.runa       # ELF/Mach-O/PE generation
    ├── relocations.runa         # Relocation handling
    └── symbol_table.runa        # Symbol table generation
```

#### Success Criteria
- [ ] Generate working x86_64 native code for basic programs
- [ ] ARM64 code generation produces functional binaries
- [ ] Register allocation generates efficient code
- [ ] Object files link successfully with system linker

---

### 🔗 WEEK 5: Linking and Executable Generation
**Priority**: Critical - Complete Compilation Pipeline  
**Status**: 🔴 DEPENDS ON WEEK 4

#### Deliverables
- **Native linker implementation**
- **Executable generation (ELF, Mach-O, PE)**
- **Dynamic library support**
- **Complete compilation driver**

#### Key Components
```
src/compiler/backend/assembler/
├── instruction_encoding/
│   ├── x86_64/
│   │   ├── encoder.runa         # x86_64 instruction encoding
│   │   ├── registers.runa       # Register mappings
│   │   └── opcodes.runa         # Opcode tables
│   └── arm64/
│       ├── encoder.runa         # ARM64 instruction encoding
│       ├── registers.runa       # Register mappings
│       └── opcodes.runa         # Opcode tables
├── assembly_parser.runa         # Parse inline Assembly syntax
├── placeholder_resolver.runa    # Resolve %[var] placeholders
└── label_manager.runa           # Handle labels and jumps

src/compiler/backend/linking/
├── assembler/
│   ├── assembler.runa           # Main assembler interface
│   └── object_generator.runa    # Generate object files
├── linkers/
│   ├── elf_linker.runa         # Linux ELF linking
│   ├── macho_linker.runa       # macOS Mach-O linking
│   └── pe_linker.runa          # Windows PE linking
├── formats/
│   ├── elf/
│   │   ├── elf_writer.runa     # ELF file format
│   │   ├── sections.runa       # ELF sections
│   │   └── relocations.runa    # ELF relocations
│   ├── macho/
│   │   ├── macho_writer.runa   # Mach-O file format
│   │   ├── segments.runa       # Mach-O segments  
│   │   └── relocations.runa    # Mach-O relocations
│   └── pe/
│       ├── pe_writer.runa      # PE file format
│       ├── sections.runa       # PE sections
│       └── relocations.runa    # PE relocations
└── driver/
    ├── compilation_pipeline.runa # Full compilation orchestration
    ├── dependency_resolver.runa  # Module dependency resolution
    └── build_cache.runa          # Incremental compilation
```

#### Success Criteria
- [ ] Complete "Hello World" compilation without external linker
- [ ] Generate working executables on Linux, macOS, Windows
- [ ] Dynamic library creation and loading functional
- [ ] Bootstrap compiler can compile itself (Stage 1.0 achieved!)

---

### 🧠 WEEK 6: Runtime Core (Part 1)
**Priority**: High - Memory Management  
**Status**: 🟡 ENHANCEMENT PHASE

#### Deliverables
- **Advanced garbage collector**
- **Memory pool allocation**
- **Heap management system**
- **Stack overflow protection**

#### Key Components
```
src/runatime/core/memory/
├── allocator.runa              # Memory allocation strategies
├── garbage_collector.runa      # GC implementation
├── heap_manager.runa           # Heap organization
├── pool_allocator.runa         # Pool-based allocation
├── stack_manager.runa          # Stack management
└── memory_profiler.runa        # Memory usage tracking
```

#### Success Criteria
- [ ] Memory allocator handles all allocation patterns efficiently
- [ ] Garbage collector prevents memory leaks in long-running programs
- [ ] Memory profiler provides accurate usage statistics
- [ ] Stack overflow detection prevents crashes

---

### 🏗️ WEEK 7: Runtime Core (Part 2)
**Priority**: High - Object Model and Type System  
**Status**: 🟡 ENHANCEMENT PHASE

#### Deliverables
- **Complete object model implementation**
- **Dynamic type system support**
- **Reflection capabilities**
- **Generic instantiation runtime**

#### Key Components
```
src/runatime/core/
├── object_model/
│   ├── object_layout.runa       # Object memory layout
│   ├── vtable_manager.runa      # Virtual method tables
│   ├── reference_counting.runa  # Reference counting system
│   ├── weak_references.runa     # Weak reference implementation
│   └── finalizers.runa          # Object finalization
└── type_system/
    ├── type_info.runa           # Runtime type information
    ├── reflection.runa          # Reflection API
    ├── dynamic_dispatch.runa    # Dynamic method dispatch
    ├── generic_instantiation.runa # Generic type creation
    └── type_checker.runa        # Runtime type validation
```

#### Success Criteria
- [ ] Object creation and method dispatch working correctly
- [ ] Reflection provides complete type introspection
- [ ] Generic types instantiate properly at runtime
- [ ] Reference counting prevents memory leaks

---

### 🚀 WEEK 8: Runtime Integration and Testing
**Priority**: High - System Integration  
**Status**: 🟡 VALIDATION PHASE

#### Deliverables
- **Complete integration testing suite**
- **Performance benchmarking framework**
- **Stress testing and validation**
- **Documentation and examples**

#### Key Components
```
src/runatime/
├── integration/
│   ├── system_interface/
│   │   ├── platform_specific.runa    # Platform-specific code
│   │   ├── environment_manager.runa  # Environment variables
│   │   ├── process_manager.runa      # Process management
│   │   ├── signal_handler.runa       # Signal handling
│   │   └── system_info.runa          # System information
│   └── ffi/
│       ├── ffi_bridge.runa          # Foreign function interface
│       ├── c_interface.runa         # C library integration
│       ├── callback_manager.runa    # Callback management
│       ├── type_marshaling.runa     # Type conversion
│       └── native_library_loader.runa # Dynamic library loading
└── tools/
    ├── performance_tester.runa      # Performance testing
    ├── memory_analyzer.runa         # Memory analysis
    ├── runtime_profiler.runa        # Runtime profiling
    └── diagnostic_tools.runa        # Debugging tools
```

#### Success Criteria
- [ ] All integration tests pass on target platforms
- [ ] Performance benchmarks show competitive results
- [ ] Memory usage stays within acceptable bounds
- [ ] Stage 1.0 compiler is stable and production-ready

---

## 📊 Development Tracking

### Weekly Milestones Checklist

#### Week 1: Syscalls Foundation ⏳
- [ ] Linux x86_64 syscalls implemented
- [ ] macOS syscall abstraction working
- [ ] Windows syscall layer functional
- [ ] Cross-platform syscall tests passing
- [ ] **BLOCKER RESOLUTION**: Any syscall implementation issues must be resolved before Week 2

#### Week 2: Frontend Self-Hosting (Part 1) ⏳
- [ ] Pure Runa lexer operational
- [ ] Parser handles all language constructs
- [ ] Diagnostic system provides quality error messages
- [ ] **DEPENDENCY**: Requires Week 1 completion for file I/O syscalls

#### Week 3: Frontend Self-Hosting (Part 2) ⏳
- [ ] Semantic analyzer validates all language features
- [ ] Type system handles generics and traits
- [ ] Borrow checker enforces memory safety
- [ ] IR pipeline generates valid intermediate code
- [ ] **MILESTONE**: Frontend completely self-hosted

#### Week 4: Backend Code Generation ⏳
- [ ] x86_64 code generation functional
- [ ] ARM64 support operational
- [ ] Register allocation efficient
- [ ] Basic optimizations working
- [ ] **DEPENDENCY**: Requires Week 3 IR pipeline

#### Week 5: Linking and Executable Generation ⏳

**Overview**: Implement native assembler and linker in pure Runa to achieve true self-hosting without external toolchain dependencies.

##### Day 1-2: Assembler Implementation
- [ ] **Instruction Encoding Engine**
  - [ ] x86_64 instruction encoder (MOV, ADD, SUB, JMP, CALL, RET, etc.)
  - [ ] ARM64 instruction encoder (basic instruction set)
  - [ ] Register allocation mapping to machine encoding
  - [ ] Addressing mode encoding (immediate, register, memory)
  
- [ ] **Assembly Parser** (for inline Assembly statements)
  - [ ] Parse AT&T and Intel syntax
  - [ ] Variable placeholder resolution (%[var] → register/memory)
  - [ ] Label and jump target resolution
  - [ ] Macro expansion support

##### Day 3-4: Object File Generation
- [ ] **Object File Formats**
  - [ ] ELF object writer (Linux/BSD)
  - [ ] Mach-O object writer (macOS)  
  - [ ] COFF/PE object writer (Windows)
  
- [ ] **Section Management**
  - [ ] .text (code) section generation
  - [ ] .data (initialized data) section
  - [ ] .bss (uninitialized data) section
  - [ ] .rodata (read-only data) section
  - [ ] Symbol table generation
  - [ ] Relocation table creation

##### Day 5-6: Native Linker
- [ ] **Symbol Resolution**
  - [ ] Multi-object file symbol merging
  - [ ] Undefined symbol detection
  - [ ] Weak symbol handling
  - [ ] Symbol visibility (global/local/hidden)

- [ ] **Relocation Processing**
  - [ ] Absolute address relocation
  - [ ] PC-relative relocation
  - [ ] GOT/PLT relocation (for dynamic linking)
  - [ ] Section base adjustments

##### Day 7: Executable Generation
- [ ] **Executable Formats**
  - [ ] ELF executable generation (Linux/BSD)
  - [ ] Mach-O executable generation (macOS)
  - [ ] PE executable generation (Windows)
  
- [ ] **Program Headers**
  - [ ] Entry point specification
  - [ ] Segment loading instructions
  - [ ] Dynamic linker path (if needed)
  - [ ] Stack/heap initial configuration

- [ ] **Additional Work**
  - [ ] Native linker generates working executables
  - [ ] Multi-platform support (Linux, macOS, Windows)
  - [ ] Dynamic library support functional

**Success Criteria**:
- [ ] Can assemble inline Assembly to machine code
- [ ] Generates valid object files linkable by system linker (interim)
- [ ] Native linker produces working executables
- [ ] Runa compiler can compile and link itself
- [ ] **CRITICAL MILESTONE**: Self-hosting achieved! 🎉

#### Week 6: Runtime Core (Part 1) ⏳
- [ ] Memory allocator operational
- [ ] Garbage collector functional
- [ ] Memory profiling working
- [ ] **ENHANCEMENT PHASE**: Core runtime capabilities

#### Week 7: Runtime Core (Part 2) ⏳
- [ ] Object model complete
- [ ] Reflection system working
- [ ] Generic runtime instantiation functional
- [ ] **ENHANCEMENT PHASE**: Advanced runtime features

#### Week 8: Integration and Testing ⏳
- [ ] Integration tests passing
- [ ] Performance benchmarks satisfactory
- [ ] System stability validated
- [ ] **FINAL MILESTONE**: Stage 1.0 production ready! 🚀

---

## 🎯 Success Metrics

### Technical Milestones
1. **Week 5**: Runa compiler can compile itself (bootstrap independence)
2. **Week 8**: Performance competitive with existing languages
3. **Ongoing**: Memory safety without runtime overhead
4. **Ongoing**: Zero external dependencies except OS syscalls

### Performance Targets
- **Compilation Speed**: 10,000+ lines/second
- **Binary Size**: <10MB self-hosting compiler
- **Memory Usage**: <100MB peak during self-compilation
- **Startup Time**: <100ms compiler startup

### Quality Assurance
- **Test Coverage**: >95% code coverage
- **Platform Support**: Linux, macOS, Windows validated
- **Architecture Support**: x86_64, ARM64 functional
- **Language Features**: 100% Runa specification implemented

---

## 🚨 Risk Management

### Critical Path Dependencies
1. **Syscalls (Week 1)** → All subsequent work depends on OS interface
2. **Frontend (Weeks 2-3)** → Backend cannot function without IR pipeline
3. **Code Generation (Week 4)** → Linking requires generated object code
4. **Linking (Week 5)** → Self-hosting milestone depends on executable generation

### Contingency Plans
- **Syscall Issues**: Fall back to Rust FFI for Week 1 if assembly problematic
- **Parser Complexity**: Prioritize core syntax, defer advanced features
- **Code Generation Bugs**: Focus on x86_64 first, ARM64/WASM as stretch goals
- **Performance Issues**: Optimize in Stage 1.1, focus on correctness in 1.0

### Resource Allocation
- **Weeks 1-5**: 100% focus on critical path to self-hosting
- **Weeks 6-8**: Runtime enhancements and optimization
- **Ongoing**: Standard library development as needed for compiler functionality

---

## 📋 Implementation Notes

### Architecture Decisions
- **Syscall Assembly**: Week 1 foundation enables complete OS independence
- **Three-Tier IR**: HIR→MIR→LIR provides optimization opportunities
- **Native Linking**: Eliminates external toolchain dependencies
- **Memory Safety**: Compile-time + runtime checks ensure security

### Development Priorities
1. **Self-Hosting** (Weeks 1-5): Minimal viable self-hosting compiler
2. **Runtime Sophistication** (Weeks 6-7): Advanced memory and object management
3. **Integration Testing** (Week 8): Validation and performance tuning
4. **AOTT System** (Future): Advanced optimization and tiered compilation

This roadmap ensures Runa achieves complete self-hosting by Week 5 while building a robust foundation for advanced runtime capabilities. The strategic prioritization of compiler frontend + syscalls creates a minimal but complete development environment, enabling all subsequent enhancements to be developed in pure Runa.