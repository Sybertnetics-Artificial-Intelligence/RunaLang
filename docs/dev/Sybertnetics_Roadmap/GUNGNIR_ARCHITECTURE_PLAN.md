# **Gungnir: The Runa Precision Compilation Pipeline**

**Vision:** To forge high-level, semantic-rich Runa code into the most performant and correct native machine code possible for any given CPU target, ensuring that Runa's expressiveness is matched by uncompromised execution speed.

**Status:** Planning Phase (Target: v0.8.0+)

---

## 🎯 The Vision: Forging Perfection

In the Runa ecosystem, our goal is not merely to compile code, but to **forge it**. We take the high-level, semantic-rich representation of the Runa language and, through a series of deliberate, transformative stages, shape it into the most performant and correct native machine code possible for a given CPU target. This forging process is **Gungnir**.

Named after Odin's mythical spear, which was so perfectly balanced that it never missed its mark, the Gungnir pipeline is our compiler's weapon of precision. It is a three-stage Intermediate Representation (IR) pipeline designed to systematically refine Runa code, applying the right optimizations at the right level of abstraction to achieve performance that meets or exceeds the best hand-tuned C++ or Rust code.

Gungnir is the answer to the question: "How do we translate the beautiful, high-level expressiveness of Runa into raw, uncompromised CPU performance?"

---

## 🚫 Why a Single IR is Not Enough

A simplistic compiler might try to convert a high-level Abstract Syntax Tree (AST) directly into machine code. This approach is fundamentally flawed and cannot produce high-performance executables.

1.  **High-Level IRs (like Runa HIR)** are excellent for semantic analysis and source-to-source translation but are terrible for optimization. They contain complex, structured control flow and named variables, making data-flow analysis nearly impossible.
2.  **Low-Level IRs (like LLVM IR)** are excellent for optimization but have already lost too much high-level information. They cannot be used for human-readable translation or high-level semantic analysis.

A multi-stage pipeline is the industry standard for all high-performance compilers (GCC, Clang/LLVM, Rustc) because it allows the compiler to apply the right kind of analysis at the right level of abstraction.

---

## ✨ The Three Forges of Gungnir: HIR, MIR, and LIR

The Gungnir pipeline consists of three distinct IRs, each serving as a "forge" with a specific purpose. This separation of concerns is the key to its power.

```
Runa Source Code
    ↓
Parser → AST (Abstract Syntax Tree)
    ↓
┌──────────────────────────────────────────────────┐
│ Forge 1: HIR (High-Level IR) - The Rosetta Stone │
│ • Human-readable, semantic-rich Runa code.       │
│ • Used for type checking, macro expansion, and   │
│   cross-language translation.                    │
└────────────────────┬─────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────┐
│ Forge 2: MIR (Mid-Level IR) - The Optimization   │
│           Core                                   │
│ • SSA-form, Control-Flow Graph (CFG).            │
│ • Platform-agnostic optimizations (DCE, LICM).   │
└────────────────────┬─────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────┐
│ Forge 3: LIR (Low-Level IR) - The Machine Bridge │
│ • Virtual registers, machine-like instructions.  │
│ • Register allocation, instruction selection.    │
└────────────────────┬─────────────────────────────┘
                     │
                     ▼
CPU Backend → Native Machine Code (x86-64, ARM64, etc.)
```

### **Forge 1: HIR (High-Level IR) - The Anvil of Semantics**

*   **Purpose:** To be the first, most faithful representation of the source code's *intent*. The HIR is, in fact, valid, type-checked Runa code. It is the universal hub for the "Rosetta Stone" project.
*   **Form:** A structured, tree-like representation that mirrors the source code. It uses named variables, structured control flow (`If`, `For`, `While`), and preserves all high-level type information.
*   **Key Operations:**
    *   **Type Checking & Semantic Analysis:** Verifying the correctness of the program.
    *   **Macro Expansion & Desugaring:** Translating high-level syntactic sugar into more fundamental language constructs.
    *   **Rosetta Stone Translation:** Serving as the entry and exit point for translating to and from other languages like Python and C.
    *   **Triple Syntax Generation:** Generating the `--canon`, `--viewer`, and `--developer` views of the code.

### **Forge 2: MIR (Mid-Level IR) - The Crucible of Optimization**

*   **Purpose:** To be the primary engine for powerful, platform-agnostic optimizations. This is where the code is melted down and purified.
*   **Form:** A **Control-Flow Graph (CFG)** of basic blocks, with all instructions in **Static Single Assignment (SSA)** form. In SSA, every variable is assigned exactly once, which makes data-flow analysis dramatically simpler and more powerful.
*   **Key Operations:**
    *   **Classic Optimizations:** This is where the bulk of traditional compiler optimizations happen.
        *   Dead Code Elimination (DCE)
        *   Constant Propagation
        *   Common Subexpression Elimination (CSE)
        *   Loop-Invariant Code Motion (LICM)
    *   **Advanced Analysis:** Liveness analysis, alias analysis, and dominance calculations are performed here.
    *   **AOTT Integration:** The MIR is the source for the AOTT engine's bytecode generation (Tiers 0-1).

### **Forge 3: LIR (Low-Level IR) - The Final Sharpening**

*   **Purpose:** To bridge the gap between the platform-agnostic MIR and the specific details of a target CPU architecture.
*   **Form:** A sequence of machine-like instructions that use an infinite set of **virtual registers**. It is no longer in SSA form.
*   **Key Operations:**
    *   **Register Allocation:** The most critical step. A **graph-coloring register allocator** maps the infinite virtual registers to the finite set of physical CPU registers (e.g., the 16 general-purpose registers on x86-64). This process includes intelligent "spilling" of variables to the stack when register pressure is high.
    *   **Instruction Selection:** Choosing the optimal machine instructions for a given LIR operation (e.g., using `lea` instead of `add` and `mov` on x86-64).
    *   **Peephole Optimization:** Performing small, local transformations on the final instruction stream to clean up inefficiencies.

---

## 🏗️ Architecture Overview

The Gungnir pipeline is a core part of the Runa compiler, transforming the AST into executable code.

### Architectural Components (`runa/compiler/middle/`)

```
runa/compiler/middle/
├── gungnir/
│   ├── hir/
│   │   ├── hir.runa          // HIR type definitions.
│   │   └── builder.runa      // AST -> HIR lowering.
│   ├── mir/
│   │   ├── mir.runa          // MIR type definitions (SSA, CFG).
│   │   ├── builder.runa      // HIR -> MIR lowering.
│   │   └── optimizations/    // Folder for all MIR optimization passes.
│   └── lir/
│       ├── lir.runa          // LIR type definitions (virtual registers).
│       ├── builder.runa      // MIR -> LIR lowering.
│       └── reg_alloc.runa    // Graph-coloring register allocator.
│
├── analysis/
│   ├── type_checker.runa     // Operates on HIR.
│   ├── liveness.runa         // Operates on LIR.
│   └── dominance.runa        // Operates on MIR.
│
└── backends/
    ├── x86_64/
    │   └── codegen.runa      // LIR -> x86-64 Assembly.
    └── arm64/
        └── codegen.runa      // LIR -> ARM64 Assembly.
```

### The Flow of Transformation

1.  **`AST -> HIR` (`hir/builder.runa`):** The parser's AST is converted into a semantic-rich HIR. Type checking is performed at this stage. This is where the Rosetta Stone and Triple Syntax systems operate.

2.  **`HIR -> MIR` (`mir/builder.runa`):** The structured HIR is lowered into a CFG in SSA form. This involves:
    *   Converting `If`/`For`/`While` into basic blocks and branches.
    *   Calculating dominance frontiers to place `phi` nodes.
    *   Renaming all variables into SSA form (e.g., `x` becomes `%x.0`, `%x.1`, etc.).

3.  **`MIR Optimizations` (`mir/optimizations/`):** A series of passes are run over the MIR to improve the code. This includes constant propagation, dead code elimination, and loop optimizations.

4.  **`MIR -> LIR` (`lir/builder.runa`):** The optimized MIR is translated into a machine-like LIR.
    *   SSA form is destroyed. `phi` nodes are converted into `move` instructions in predecessor blocks.
    *   SSA temporaries are converted into an infinite set of virtual registers.

5.  **`Register Allocation` (`lir/reg_alloc.runa`):**
    *   Liveness analysis is performed on the LIR to determine the live range of each virtual register.
    *   An interference graph is built.
    *   The graph is "colored" using a fixed number of colors (physical registers).
    *   Virtual registers that cannot be colored are "spilled" to the stack, and `load`/`store` instructions are inserted.

6.  **`LIR -> Assembly` (`backends/*/codegen.runa`):** The final, register-allocated LIR is trivially translated into the target assembly language. This stage also handles function prologues/epilogues and calling conventions.

---

## 📋 Implementation Roadmap

The implementation of the Gungnir pipeline is a core part of the Runa v1.0 roadmap, replacing the direct AST-to-assembly compiler.

### Phase 1: HIR Integration (Target: v0.8.0)

*   **Goal:** Re-integrate the HIR from the `_legacy` codebase. The compiler pipeline becomes `AST -> HIR -> Assembly`.
*   **Deliverables:**
    *   `runa/compiler/middle/gungnir/hir/` module is complete.
    *   The Triple Syntax system (`--canon`, `--viewer`, `--developer`) becomes operational.
    *   The foundation for the Rosetta Stone is laid.
*   **Success Criteria:**
    *   ✅ The compiler uses HIR as its primary representation after parsing.
    *   ✅ All existing language features are correctly represented in HIR.
    *   ✅ The compiler can output valid Runa code in all three syntax modes from the HIR.

### Phase 2: MIR Integration & Core Optimizations (Target: v0.8.1)

*   **Goal:** Implement the `HIR -> MIR` lowering step and the core optimization passes. The pipeline becomes `AST -> HIR -> MIR -> Assembly`.
*   **Deliverables:**
    *   `runa/compiler/middle/gungnir/mir/` module is complete.
    *   SSA construction algorithm is implemented and verified.
    *   Core optimization passes (DCE, Constant Propagation, CSE) are functional.
*   **Success Criteria:**
    *   ✅ The compiler can successfully lower HIR to valid SSA-form MIR.
    *   ✅ Optimization passes measurably improve code quality (e.g., smaller code size, fewer instructions).
    *   ✅ Performance on benchmarks improves by at least 10-20% over the unoptimized version.

### Phase 3: LIR Integration & Register Allocation (Target: v0.8.2)

*   **Goal:** Implement the full `MIR -> LIR -> Assembly` pipeline, including the graph-coloring register allocator.
*   **Deliverables:**
    *   `runa/compiler/middle/gungnir/lir/` module is complete.
    *   A graph-coloring register allocator is implemented for the x86-64 backend.
*   **Success Criteria:**
    *   ✅ The compiler now has a modern, three-stage IR, enabling more sophisticated code generation.
    *   ✅ The register allocator makes more efficient use of physical registers than the previous naive approach.
    *   ✅ The full pipeline is self-hosting and passes all regression tests.

### Phase 4: Advanced Optimizations (Target: v0.8.3)

*   **Goal:** With the full pipeline in place, implement advanced, whole-program optimizations.
*   **Deliverables:**
    *   Profile-Guided Optimization (PGO) infrastructure.
    *   Link-Time Optimization (LTO) framework.
    *   Initial implementation of SIMD Auto-Vectorization for simple loops.
*   **Success Criteria:**
    *   ✅ PGO provides a 10-30% speedup on real-world application benchmarks.
    *   ✅ LTO enables cross-module inlining and dead code elimination.
    *   ✅ Runa's performance on standard benchmarks is now in direct competition with C++ and Rust.

---

## 🎯 Conclusion

The Gungnir pipeline is not just a compiler architecture; it is a statement of intent. It declares that Runa will not compromise on performance. By adopting this industry-standard, three-stage approach, we ensure that the Runa language has the architectural foundation to be not only the most expressive and safest systems language, but also one of the fastest. Gungnir is the forge that will craft Runa's legacy of performance and precision.

---

## 🔗 Related Documents

- Rosetta Stone Architecture - Details on the HIR.
- Bifröst Architecture - The parallel pipeline for heterogeneous compute.
- Development Roadmap - Overall project timeline.

---

