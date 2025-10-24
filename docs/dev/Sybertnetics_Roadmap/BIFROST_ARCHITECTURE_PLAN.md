# **Bifröst: The Runa Universal Compute IR**

**Vision:** To create a single, unified, high-level Intermediate Representation (IR) that allows Runa code to be compiled and optimally executed on any specialized, massively parallel hardware, from GPUs and FPGAs to DSPs and future AI accelerators.

**Status:** Planning Phase (Target: v0.9.0+)

---

## 🎯 The Vision: A Bridge to Infinite Power

In the age of heterogeneous computing, the CPU is no longer the sole arbiter of performance. True computational power lies in a diverse ecosystem of specialized silicon. The greatest challenge facing modern software is the fragmentation of this ecosystem. Each hardware vendor has its own proprietary language (CUDA, Metal), its own tools, and its own internal IRs (PTX, AIR).

**Bifröst** is Runa's answer to this fragmentation.

Named after the mythical rainbow bridge connecting the mortal realm to the realm of the gods, Bifröst is a **next-generation, graph-based, formally verifiable IR** designed from first principles for the world of massively parallel computing. It is the single, unified bridge that allows high-level Runa code to be translated into the raw power of any specialized hardware.

Bifröst is not just a "SPIR-V alternative." It is a conceptual leap forward, designed to be a true "full-spectrum" compute IR, targeting everything from the most powerful NVIDIA GPUs to custom FPGAs and DSPs with a single, unified, and verifiable representation.

---

## 🚫 Why Existing IRs Are Not The Answer

Current solutions like LLVM IR and SPIR-V are powerful but were not designed for the full breadth of the heterogeneous world we now live in.

### LLVM IR's Limitations

1.  **CPU-Centric Design:** LLVM was born as a CPU compiler infrastructure. Its models for parallelism, memory, and execution are fundamentally based on CPU architecture. GPU support is an add-on, not a native concept.
2.  **Loss of Parallel Semantics:** LLVM IR represents a linear sequence of low-level instructions. It loses the high-level structure of a parallel computation (e.g., "apply this function to all 1 million elements"). This makes it incredibly difficult for a backend to reconstruct the original parallel intent and map it optimally to hardware.
3.  **Impoverished Type System:** It lacks first-class types for hardware concepts like `Vectors`, `Matrices`, `Textures`, or `FixedPoint` numbers, which are critical for graphics and DSPs.
4.  **Single, Flat Memory Model:** LLVM IR assumes a single, unified memory space. It has no native understanding of the complex memory hierarchies of GPUs (`global`, `shared`, `local` memory), which are the most critical factor for performance.

### SPIR-V's Limitations

1.  **Graphics-First Heritage:** SPIR-V is an excellent standard for graphics shaders and general-purpose GPU compute (GPGPU). However, its execution model is tightly coupled to the GPU model of workgroups and subgroups.
2.  **Limited Target Scope:** It is not designed to effectively represent the unique computational models of other accelerators, such as the reconfigurable dataflow pipelines of an **FPGA** or the fixed-function hardware of a **DSP**.
3.  **Not High-Level Enough:** While higher-level than machine code, it still loses significant semantic information, making high-level, cross-platform optimizations difficult.

---

## ✨ Why Bifröst is a Revolutionary Approach

Bifröst is designed from the ground up to overcome these limitations by adhering to a different set of core principles.

| Feature | LLVM IR | SPIR-V | Bifröst (Runa) |
| :--- | :--- | :--- | :--- |
| **Primary Target** | CPUs | GPUs | **All Accelerators** (GPU, FPGA, DSP, etc.) |
| **Representation** | Linear Instructions | Linear Instructions | **Computational Graph (DAG)** |
| **Abstraction Level** | Low (add, load, store) | Mid (GPU-centric ops) | **High** (`MatrixMultiply`, `Convolve2D`, `FFT`) |
| **Parallelism Model** | Implicit (libraries) | Explicit (GPU model) | **Explicit & Abstract** (`DataParallel`, `Pipeline`) |
| **Memory Model** | Flat Address Space | GPU Memory Spaces | **Explicit & Hierarchical** (`global`, `shared`, etc.) |
| **Verifiability** | Difficult | Limited | **Formally Verifiable** (by design) |

### Core Design Principles

1.  **Graph-Based Representation:** Bifröst represents computations as a Directed Acyclic Graph (DAG). Nodes are high-level operations (`MatrixMultiply`, `Convolve2D`), and edges represent the flow of data. This structure is ideal for high-level optimization and mapping to parallel architectures.

2.  **Explicit & Abstract Parallelism:** Bifröst has first-class concepts for different modes of parallelism (`DataParallel`, `TaskGraph`, `Pipeline`), which can be mapped efficiently to any target hardware.

3.  **Hardware-Aware Type System:** It includes a rich type system with native support for `Vector`, `Matrix`, `Texture`, and `FixedPoint` numbers, essential for targeting diverse hardware.

4.  **Explicit Memory Hierarchy:** Bifröst understands the complex memory hierarchies of modern accelerators. It has native concepts for `global`, `shared`, `local`, and `constant` memory, enabling precise control over data placement.

5.  **Formal Verifiability:** The high-level, graph-based nature of Bifröst allows for static analysis to prove critical properties like memory safety, data-race freedom, and resource bounds *before* the code ever touches the hardware.

---

## 🏗️ Architecture Overview

The Bifröst pipeline runs in parallel to the Gungnir (CPU) pipeline, branching off from the Mid-Level IR (MIR).

```
┌──────────────────────────────────────────────────┐
│  Runa Source Code (or translated from C, Python...)│
└────────────────────┬─────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────┐
│  AST → HIR → MIR (Platform-Agnostic Optimizations) │
└────────────────────┬─────────────────────────────┘
                     │
     ┌───────────────┴───────────────┐
     │ (CPU & General Purpose Path)  │ (Heterogeneous / Accelerator Path)
     ▼                               ▼
┌────────────────────┐   ┌────────────────────────┐
│  Gungnir (LIR)     │   │  Bifröst (Universal    │
│  • For CPU targets │   │     Compute IR)        │
└────────┬───────────┘   └──────────┬─────────────┘
         │                         │
         ▼                         ▼
┌────────────────────┐   ┌────────────────────────┐
│ CPU Backends       │   │ Accelerator Backends   │
│ • x86-64 Assembly  │   │ • CUDA (for NVIDIA)    │
│ • ARM64 Assembly   │   │ • Metal (for Apple)    │
│ • RISC-V Assembly  │   │ • Verilog/VHDL (FPGAs) │
└────────────────────┘   └────────────────────────┘
```

### Architectural Components (`runa/compiler/middle/bifrost/`)

```
runa/compiler/middle/bifrost/
├── graph/
│   ├── node.runa          // Defines the core `BifrostNode` (operations) and `BifrostType`.
│   ├── edge.runa          // Defines data flow edges and dependencies.
│   └── graph.runa         // The main `BifrostGraph` data structure.
│
├── builder.runa           // Translates Runa MIR into a Bifröst compute graph.
│
├── analysis/
│   ├── parallelism.runa   // Detects and classifies parallelism patterns in the graph.
│   ├── memory_access.runa // Analyzes memory access patterns for optimization.
│   └── verifier.runa        // Formally verifies the graph for safety and correctness.
│
├── optimizations/
│   ├── kernel_fusion.runa // Merges multiple small kernels into one to reduce overhead.
│   ├── layout_opt.runa    // Optimizes data layout in memory for better access patterns.
│   └── op_reordering.runa // Reorders operations to improve instruction-level parallelism.
│
└── backends/
    ├── cuda/
    │   └── cuda_gen.runa    // Generates PTX or CUDA C++ from a Bifröst graph.
    ├── metal/
    │   └── metal_gen.runa   // Generates Metal Shading Language (MSL).
    ├── opencl/
    │   └── opencl_gen.runa  // Generates OpenCL C.
    └── fpga/
        └── hdl_gen.runa     // Generates synthesizable Verilog or VHDL.
```

---

## 🚀 The Developer Experience: Seamless Acceleration

A Runa developer does not need to be a CUDA or Metal expert. They simply write idiomatic, high-level Runa code, and the compiler handles the rest.

```runa
Note: A simple vector addition in Runa.

Process called "vector_add" that takes a as List of Float, b as List of Float returns List of Float:
    Let result be a new List of Float with capacity as length of a

    Note: The compiler identifies this loop as a massively data-parallel operation.
    Note: It will be automatically offloaded to the GPU via the Bifröst pipeline.
    For i from 0 to (length of a) minus 1:
        Set result at index i to (a at index i) plus (b at index i)
    End For

    Return result
End Process
```

For expert users, Runa provides explicit directives for fine-grained control.

```runa
@Execution_Model:
    target: "gpu"
    backend: "cuda"  // Request a specific backend, or "auto"
    block_size: 256  // Provide a hint for the CUDA block size
@End_Execution_Model
Process called "matrix_multiply" that takes A as Matrix, B as Matrix returns Matrix:
    // ... implementation ...
End Process
```

---

## 📋 Implementation Roadmap

The development of Bifröst is a major post-v0.8 initiative, planned to be executed in parallel with the AOTT and Cross-Compilation efforts.

### Phase 1: Graph Foundation (Target: v0.9.0)

*   **Goal:** Implement the core Bifröst graph data structures and the `MIR -> Bifröst` builder.
*   **Deliverables:**
    *   `runa/compiler/middle/bifrost/graph/` module is complete and unit-tested.
    *   `runa/compiler/middle/bifrost/builder.runa` is implemented.
*   **Success Criteria:**
    *   ✅ The compiler can successfully translate Runa MIR into a valid, in-memory Bifröst graph.
    *   ✅ The graph structure correctly represents data dependencies and high-level operations.
    *   ✅ No code generation is implemented in this phase.

### Phase 2: First Backend - CUDA (Target: v0.9.1)

*   **Goal:** Implement the first end-to-end backend for NVIDIA GPUs.
*   **Deliverables:**
    *   `runa/compiler/middle/bifrost/backends/cuda/cuda_gen.runa` is implemented.
    *   The compiler can take a Bifröst graph and generate working CUDA C++ or PTX.
*   **Success Criteria:**
    *   ✅ Simple, data-parallel Runa loops can be successfully compiled and executed on NVIDIA GPUs.
    *   ✅ Performance is at least 5x faster than the equivalent single-threaded CPU version for suitable workloads.
    *   ✅ End-to-end integration tests pass.

### Phase 3: Optimization & Analysis (Target: v0.9.2)

*   **Goal:** Implement the core optimization passes and the formal verifier.
*   **Deliverables:**
    *   `runa/compiler/middle/bifrost/optimizations/` library is built out.
    *   `runa/compiler/middle/bifrost/analysis/verifier.runa` is implemented.
*   **Success Criteria:**
    *   ✅ Kernel fusion provides a measurable performance increase (e.g., >30%) on relevant benchmarks.
    *   ✅ Memory layout optimizations improve memory-bound kernel performance.
    *   ✅ The verifier can statically prove memory safety and data-race freedom for simple kernels.

### Phase 4: Additional Backends - Metal & OpenCL (Target: v0.9.3)

*   **Goal:** Add support for Apple and AMD/Intel GPUs, proving the portability of the Bifröst design.
*   **Deliverables:**
    *   `metal_gen.runa` and `opencl_gen.runa` modules are implemented.
*   **Success Criteria:**
    *   ✅ The exact same Runa source code can be compiled to run on NVIDIA, Apple, and AMD GPUs.
    *   ✅ Performance on each platform is within 80% of hand-written, platform-specific code (e.g., MSL for Metal).

### Phase 5: The Final Frontier - FPGAs (Target: v1.0+)

*   **Goal:** Target reconfigurable hardware, the ultimate test of Bifröst's flexibility.
*   **Deliverables:**
    *   `runa/compiler/middle/bifrost/backends/fpga/hdl_gen.runa` is implemented.
*   **Success Criteria:**
    *   ✅ The compiler can generate synthesizable Verilog or VHDL from a Bifröst graph representing a dataflow pipeline.
    *   ✅ Simple Runa algorithms can be compiled and run on a target FPGA development board.

---

## 🎯 Conclusion

Bifröst is the architectural key that unlocks Runa's "full-spectrum" promise. It elevates the compiler from a CPU-centric tool to a true universal translator for computation. By providing a single, high-level, verifiable representation for all forms of parallel hardware, Bifröst eliminates the fragmentation and complexity that plague modern high-performance computing, making the power of accelerators accessible to all Runa developers.

