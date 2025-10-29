# **Gungnir: Precision CPU Compilation Pipeline**

**Version:** 1.0
**Status:** Planning Phase (Target: v0.8.0+)
**Classification:** Internal Technical Specification (Confidential)
**Last Updated:** 2025-01-23

---

## **Table of Contents**

1. [Overview](#overview)
2. [Vision: Forging Perfection](#vision-forging-perfection)
3. [Why a Single IR Is Not Enough](#why-a-single-ir-is-not-enough)
4. [The Three Forges: HIR, MIR, and LIR](#the-three-forges-hir-mir-and-lir)
5. [Architecture Overview](#architecture-overview)
6. [The Flow of Transformation](#the-flow-of-transformation)
7. [Implementation Roadmap](#implementation-roadmap)
8. [Success Criteria](#success-criteria)
9. [Related Documentation](#related-documentation)

---

## **Overview**

**Gungnir** is Runa's precision CPU compilation pipeline, designed to forge high-level, semantic-rich Runa code into the most performant and correct native machine code possible for any given CPU target. Named after Odin's mythical spear—which was so perfectly balanced that it never missed its mark—Gungnir represents the compiler's weapon of precision.

**Key Characteristics:**
- **Three-Stage IR Pipeline:** HIR → MIR → LIR
- **Platform-Agnostic Optimization:** Powerful transformations at the MIR level
- **Industry-Standard Architecture:** SSA form, CFG, graph-coloring register allocation
- **Performance Target:** Match or exceed hand-tuned C++/Rust code

**Design Philosophy:**
Gungnir is the answer to the question: "How do we translate the beautiful, high-level expressiveness of Runa into raw, uncompromised CPU performance?"

**Strategic Position:**
- **CPU Target:** Gungnir handles all CPU architectures (x86-64, ARM64, RISC-V)
- **Complementary to Bifröst:** While Bifröst targets accelerators, Gungnir targets CPUs
- **Foundation for Self-Hosting:** Gungnir compiles the Runa compiler itself

---

## **Vision: Forging Perfection**

In the Runa ecosystem, our goal is not merely to compile code, but to **forge it**. We take the high-level, semantic-rich representation of the Runa language and, through a series of deliberate, transformative stages, shape it into the most performant and correct native machine code possible for a given CPU target.

**The Forging Metaphor:**

Each stage of Gungnir acts as a "forge," applying specific transformations at the right level of abstraction:

1. **HIR (High-Level IR) - The Anvil of Semantics:** Preserves the programmer's intent, enables source-to-source translation
2. **MIR (Mid-Level IR) - The Crucible of Optimization:** Melts down code into SSA form, applies powerful transformations
3. **LIR (Low-Level IR) - The Final Sharpening:** Bridges to hardware, allocates registers, selects optimal instructions

**Performance Promise:**
Gungnir-compiled Runa code will achieve performance that meets or exceeds the best hand-tuned C++ or Rust code on equivalent algorithms.

---

## **Why a Single IR Is Not Enough**

A simplistic compiler might try to convert a high-level Abstract Syntax Tree (AST) directly into machine code. This approach is fundamentally flawed and cannot produce high-performance executables.

### **The Two-Extreme Problem**

| Aspect | High-Level IR (e.g., HIR) | Low-Level IR (e.g., LLVM IR) | Multi-Stage Solution |
|--------|---------------------------|------------------------------|----------------------|
| **Human Readability** | ✅ Excellent | ❌ Poor | ✅ HIR for translation |
| **Semantic Preservation** | ✅ High | ❌ Lost | ✅ HIR preserves intent |
| **Optimization Power** | ❌ Very Limited | ✅ Excellent | ✅ MIR optimizes |
| **Hardware Mapping** | ❌ Impossible | ✅ Good | ✅ LIR bridges to CPU |
| **Cross-Language Translation** | ✅ Natural | ❌ Infeasible | ✅ HIR enables Rosetta |

### **Why High-Level IRs Fail at Optimization**

**Example: Simple loop in HIR**
```runa
For i from 0 to 99:
    Set array at index i to (i times 2) plus 1
End For
```

**Problems for optimization:**
- Control flow is complex (loop structure)
- Variables are named, not numbered
- Data dependencies unclear
- Cannot easily apply SSA-based optimizations

### **Why Low-Level IRs Fail at Translation**

**Example: Same loop in LLVM IR**
```llvm
%i = phi i32 [ 0, %entry ], [ %i.next, %loop ]
%i.times.2 = mul i32 %i, 2
%result = add i32 %i.times.2, 1
%ptr = getelementptr [100 x i32], [100 x i32]* %array, i32 0, i32 %i
store i32 %result, i32* %ptr
%i.next = add i32 %i, 1
%cond = icmp slt i32 %i.next, 100
br i1 %cond, label %loop, label %exit
```

**Problems for translation:**
- Lost semantic information (what is this loop doing?)
- Cannot reconstruct "For i from 0 to 99"
- Impossible to translate back to idiomatic Python or C

### **Industry Standard: Multi-Stage Pipelines**

**All high-performance compilers use multi-stage IRs:**
- **GCC:** GIMPLE (high) → RTL (low)
- **Clang/LLVM:** Clang AST → LLVM IR
- **Rustc:** HIR → MIR → LLVM IR
- **Runa/Gungnir:** HIR → MIR → LIR

**Why:** Each stage serves a specific purpose at the right level of abstraction.

---

## **The Three Forges: HIR, MIR, and LIR**

### **Pipeline Visualization**

```
Runa Source Code
    ↓
Parser → AST (Abstract Syntax Tree)
    ↓
┌──────────────────────────────────────────────────┐
│ Forge 1: HIR (High-Level IR) - The Rosetta Stone │
│ • Human-readable, semantic-rich Runa code        │
│ • Used for type checking, macro expansion, and   │
│   cross-language translation                     │
└────────────────────┬─────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────┐
│ Forge 2: MIR (Mid-Level IR) - The Optimization   │
│           Core                                   │
│ • SSA-form, Control-Flow Graph (CFG)             │
│ • Platform-agnostic optimizations (DCE, LICM)    │
└────────────────────┬─────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────┐
│ Forge 3: LIR (Low-Level IR) - The Machine Bridge │
│ • Virtual registers, machine-like instructions   │
│ • Register allocation, instruction selection     │
└────────────────────┬─────────────────────────────┘
                     │
                     ▼
CPU Backend → Native Machine Code (x86-64, ARM64, RISC-V, etc.)
```

---

### **Forge 1: HIR (High-Level IR) - The Anvil of Semantics**

**Purpose:** First, most faithful representation of source code intent. Valid, type-checked Runa code.

**Form:** Structured, tree-like representation mirroring source code:
- Named variables (not SSA temporaries)
- Structured control flow (`If`, `For`, `While`)
- Preserves all high-level type information
- Valid Runa syntax (can be pretty-printed)

**Key Operations:**

| Operation | Description |
|-----------|-------------|
| **Type Checking** | Verify correctness of the program |
| **Semantic Analysis** | Ensure valid language constructs |
| **Macro Expansion** | Translate syntactic sugar to fundamental constructs |
| **Desugaring** | Convert high-level features to simpler forms |
| **Rosetta Stone** | Entry/exit point for cross-language translation |
| **Triple Syntax** | Generate `--canon`, `--viewer`, `--developer` views |

**Example HIR:**
```runa
Process called "factorial" that takes n as Integer returns Integer:
    If n is equal to 0:
        Return 1
    Otherwise:
        Return n times (factorial of (n minus 1))
    End If
End Process
```

**Characteristics:**
- ✅ Human-readable
- ✅ Preserves programmer intent
- ✅ Type-safe
- ❌ Not optimizable (complex control flow)

---

### **Forge 2: MIR (Mid-Level IR) - The Crucible of Optimization**

**Purpose:** Primary engine for powerful, platform-agnostic optimizations. Code is "melted down and purified."

**Form:** Control-Flow Graph (CFG) of basic blocks in Static Single Assignment (SSA) form:
- **Basic Blocks:** Sequences of instructions with single entry/exit
- **SSA Form:** Every variable assigned exactly once
- **CFG Edges:** Represent control flow between blocks
- **Phi Nodes:** Merge values from different control flow paths

**Key Operations:**

| Optimization Pass | Description | Impact |
|-------------------|-------------|--------|
| **Dead Code Elimination (DCE)** | Remove unused computations | Code size, performance |
| **Constant Propagation** | Replace variables with constant values | Simplification |
| **Common Subexpression Elimination (CSE)** | Avoid redundant computations | Performance |
| **Loop-Invariant Code Motion (LICM)** | Hoist computations out of loops | Performance |
| **Inlining** | Replace function calls with function body | Performance |
| **Strength Reduction** | Replace expensive ops with cheaper ones | Performance |

**Example MIR (SSA Form):**
```
factorial:
    entry:
        %0 = param(n)
        %1 = const(0)
        %2 = eq %0, %1
        br %2, block_then, block_else

    block_then:
        %3 = const(1)
        return %3

    block_else:
        %4 = const(1)
        %5 = sub %0, %4
        %6 = call factorial(%5)
        %7 = mul %0, %6
        return %7
```

**Characteristics:**
- ✅ Excellent for optimization (SSA enables powerful analysis)
- ✅ Platform-agnostic (no hardware details)
- ✅ Clear data dependencies
- ❌ Not human-readable
- ❌ Cannot be directly executed

**SSA Benefits:**
- **Simplified Data-Flow Analysis:** Each variable has exactly one definition
- **Efficient Use-Def Chains:** Easy to find where values are used
- **Powerful Optimizations:** DCE, CSE, LICM all leverage SSA properties

---

### **Forge 3: LIR (Low-Level IR) - The Final Sharpening**

**Purpose:** Bridge the gap between platform-agnostic MIR and specific CPU architecture details.

**Form:** Sequence of machine-like instructions using **infinite virtual registers**:
- No longer in SSA form (phi nodes eliminated)
- Instructions resemble target CPU instructions
- Virtual registers (unlimited number)
- Explicit stack operations

**Key Operations:**

| Operation | Description | Complexity |
|-----------|-------------|------------|
| **SSA Destruction** | Convert phi nodes to move instructions | Medium |
| **Register Allocation** | Map virtual → physical registers | **High** (NP-hard) |
| **Instruction Selection** | Choose optimal CPU instructions | Medium |
| **Peephole Optimization** | Local instruction improvements | Low |

**Example LIR (Virtual Registers):**
```
factorial:
    entry:
        v0 = load_param(n)
        v1 = load_const(0)
        v2 = cmp_eq v0, v1
        branch_if v2, block_then, block_else

    block_then:
        v3 = load_const(1)
        return v3

    block_else:
        v4 = load_const(1)
        v5 = sub v0, v4
        v6 = call factorial(v5)
        v7 = mul v0, v6
        return v7
```

**Register Allocation (Graph Coloring):**

1. **Liveness Analysis:** Determine when each virtual register is "live" (in use)
2. **Interference Graph:** Build graph where nodes = virtual registers, edges = cannot share physical register
3. **Graph Coloring:** Assign colors (physical registers) such that no adjacent nodes share a color
4. **Spilling:** If insufficient colors, spill some registers to stack

**Result (x86-64 with physical registers):**
```asm
factorial:
    entry:
        mov rdi, [rsp+8]    ; n in rdi
        xor rsi, rsi        ; 0 in rsi
        cmp rdi, rsi
        je .then
        jmp .else

    .then:
        mov rax, 1
        ret

    .else:
        mov rcx, rdi
        dec rdi
        call factorial
        imul rax, rcx
        ret
```

---

## **Architecture Overview**

### **Module Structure**

```
runa/compiler/middle/
├── gungnir/
│   ├── hir/
│   │   ├── hir.runa          // HIR type definitions
│   │   ├── builder.runa      // AST → HIR lowering
│   │   ├── type_checker.runa // Type checking on HIR
│   │   └── pretty_print.runa // HIR → Runa source (Triple Syntax)
│   │
│   ├── mir/
│   │   ├── mir.runa          // MIR type definitions (SSA, CFG)
│   │   ├── builder.runa      // HIR → MIR lowering (SSA construction)
│   │   ├── optimizations/    // MIR optimization passes
│   │   │   ├── dce.runa      // Dead Code Elimination
│   │   │   ├── const_prop.runa // Constant Propagation
│   │   │   ├── cse.runa      // Common Subexpression Elimination
│   │   │   ├── licm.runa     // Loop-Invariant Code Motion
│   │   │   ├── inlining.runa // Function inlining
│   │   │   └── strength_reduction.runa
│   │   └── analysis/
│   │       ├── dominance.runa // Dominance analysis
│   │       └── alias.runa     // Alias analysis
│   │
│   └── lir/
│       ├── lir.runa          // LIR type definitions (virtual registers)
│       ├── builder.runa      // MIR → LIR lowering (SSA destruction)
│       ├── reg_alloc.runa    // Graph-coloring register allocator
│       └── instruction_selection.runa // Optimal instruction selection
│
└── backends/
    ├── x86_64/
    │   ├── codegen.runa      // LIR → x86-64 Assembly
    │   └── abi.runa          // x86-64 calling convention
    ├── arm64/
    │   ├── codegen.runa      // LIR → ARM64 Assembly
    │   └── abi.runa          // ARM64 calling convention
    └── riscv/
        ├── codegen.runa      // LIR → RISC-V Assembly
        └── abi.runa          // RISC-V calling convention
```

---

## **The Flow of Transformation**

### **Step-by-Step Compilation Process**

#### **Step 1: AST → HIR (`hir/builder.runa`)**

**Input:** Parser's Abstract Syntax Tree
**Output:** Type-checked HIR

**Process:**
1. Convert AST nodes to HIR nodes
2. Resolve names and symbols
3. Perform type checking
4. Expand macros and desugar syntax
5. Generate Triple Syntax views (`--canon`, `--viewer`, `--developer`)

**Why This Matters:**
- HIR is the foundation for Rosetta Stone (cross-language translation)
- Type errors caught early (better error messages)
- Semantic correctness guaranteed before optimization

---

#### **Step 2: HIR → MIR (`mir/builder.runa`)**

**Input:** Type-checked HIR
**Output:** SSA-form MIR (CFG)

**Process:**
1. **CFG Construction:** Convert structured control flow (`If`, `For`) into basic blocks and branches
2. **SSA Construction:**
   - Calculate dominance frontiers
   - Place phi nodes at merge points
   - Rename all variables into SSA temporaries (`x` → `%x.0`, `%x.1`, ...)
3. **Verification:** Ensure SSA form is valid

**Example Transformation:**

**HIR:**
```runa
Let x be 0
For i from 0 to 9:
    Set x to x plus 1
End For
Return x
```

**MIR (SSA):**
```
entry:
    %x.0 = const(0)
    %i.0 = const(0)
    br loop_header

loop_header:
    %x.1 = phi(%x.0, %x.2)
    %i.1 = phi(%i.0, %i.2)
    %cond = lt %i.1, const(10)
    br %cond, loop_body, exit

loop_body:
    %x.2 = add %x.1, const(1)
    %i.2 = add %i.1, const(1)
    br loop_header

exit:
    return %x.1
```

---

#### **Step 3: MIR Optimizations (`mir/optimizations/`)**

**Input:** SSA-form MIR
**Output:** Optimized SSA-form MIR

**Example: Constant Propagation + Dead Code Elimination**

**Before:**
```
%a = const(5)
%b = const(3)
%c = add %a, %b
%d = mul %c, const(2)
%e = add %a, const(10)  // %e never used
return %d
```

**After Constant Propagation:**
```
%a = const(5)
%b = const(3)
%c = const(8)          // 5 + 3 = 8
%d = const(16)         // 8 * 2 = 16
%e = const(15)         // Dead code
return const(16)
```

**After Dead Code Elimination:**
```
return const(16)
```

---

#### **Step 4: MIR → LIR (`lir/builder.runa`)**

**Input:** Optimized MIR
**Output:** LIR with virtual registers

**Process:**
1. **SSA Destruction:**
   - Eliminate phi nodes
   - Insert move instructions in predecessor blocks
2. **Virtual Register Allocation:**
   - Convert SSA temporaries to virtual registers
   - Virtual registers are unlimited (v0, v1, v2, ...)
3. **Lowering:**
   - Convert high-level MIR operations to machine-like LIR instructions

**Example:**

**MIR:**
```
loop_header:
    %x.1 = phi(%x.0, %x.2)
    ...
```

**LIR (SSA destroyed):**
```
entry_to_loop:
    v_x = v_x_0    // Copy from entry
    br loop_header

loop_body_to_loop:
    v_x = v_x_2    // Copy from loop body
    br loop_header

loop_header:
    // Use v_x directly (no phi)
    ...
```

---

#### **Step 5: Register Allocation (`lir/reg_alloc.runa`)**

**Input:** LIR with unlimited virtual registers
**Output:** LIR with physical registers

**Algorithm: Graph Coloring**

1. **Build Interference Graph:**
   - Nodes = virtual registers
   - Edge between `v1` and `v2` if their live ranges overlap (cannot share physical register)

2. **Color the Graph:**
   - Assign colors (physical registers: rax, rbx, rcx, ...)
   - Constraint: No adjacent nodes can have the same color
   - If graph cannot be colored with available registers → **spill**

3. **Spilling:**
   - Choose virtual registers to spill to stack
   - Insert `load` and `store` instructions around their uses
   - Repeat until graph can be colored

**Example:**

**Virtual Registers:**
```
v0 = load_param(n)
v1 = load_const(5)
v2 = add v0, v1
v3 = mul v2, v2
return v3
```

**Physical Registers (x86-64):**
```
mov rdi, [rsp+8]   ; n in rdi (v0 → rdi)
mov rsi, 5          ; 5 in rsi (v1 → rsi)
add rdi, rsi        ; rdi = rdi + rsi (v2 → rdi)
imul rdi, rdi       ; rdi = rdi * rdi (v3 → rdi)
mov rax, rdi        ; return value in rax
ret
```

---

#### **Step 6: LIR → Assembly (`backends/*/codegen.runa`)**

**Input:** LIR with physical registers
**Output:** Target assembly code

**Process:**
1. **Instruction Selection:** Map LIR instructions to target CPU instructions
2. **Function Prologue/Epilogue:** Set up/tear down stack frame
3. **Calling Convention:** Follow ABI (x86-64 System V, ARM64 AAPCS, etc.)
4. **Peephole Optimization:** Local instruction improvements

**Example:**

**LIR:**
```
function_entry:
    rdi = load_param(n)
    rsi = load_const(5)
    rdi = add rdi, rsi
    return rdi
```

**x86-64 Assembly:**
```asm
function:
    push rbp
    mov rbp, rsp
    ; rdi already contains first parameter
    add rdi, 5
    mov rax, rdi
    pop rbp
    ret
```

---

## **Implementation Roadmap**

### **Phase 1: HIR Integration (Target: v0.8.0)**

**Timeline:** 2-3 months

**Goal:** Re-integrate HIR from legacy codebase. Pipeline becomes `AST → HIR → Assembly`.

**Deliverables:**
- ✅ `runa/compiler/middle/gungnir/hir/` module complete
- ✅ HIR type definitions and builder implemented
- ✅ Type checker operates on HIR
- ✅ Triple Syntax system functional (`--canon`, `--viewer`, `--developer`)
- ✅ HIR pretty-printer generates valid Runa source

**Success Criteria:**
- Compiler uses HIR as primary representation after parsing
- All existing language features correctly represented in HIR
- Compiler outputs valid Runa code in all three syntax modes
- Foundation for Rosetta Stone laid

**Team:** 2 developers

---

### **Phase 2: MIR Integration & Core Optimizations (Target: v0.8.1)**

**Timeline:** 4-5 months

**Goal:** Implement `HIR → MIR` lowering and core optimization passes. Pipeline becomes `AST → HIR → MIR → Assembly`.

**Deliverables:**
- ✅ `runa/compiler/middle/gungnir/mir/` module complete
- ✅ SSA construction algorithm implemented and verified
- ✅ CFG builder (structured control flow → basic blocks)
- ✅ Core optimization passes:
  - Dead Code Elimination (DCE)
  - Constant Propagation
  - Common Subexpression Elimination (CSE)
  - Loop-Invariant Code Motion (LICM)

**Success Criteria:**
- Compiler successfully lowers HIR to valid SSA-form MIR
- Optimization passes measurably improve code quality
- Performance on benchmarks improves by **10-20%** over unoptimized version
- SSA form is correct (passes verification)

**Team:** 3 developers (1 SSA construction, 2 optimizations)

---

### **Phase 3: LIR Integration & Register Allocation (Target: v0.8.2)**

**Timeline:** 4-5 months

**Goal:** Implement `MIR → LIR → Assembly` pipeline, including graph-coloring register allocator.

**Deliverables:**
- ✅ `runa/compiler/middle/gungnir/lir/` module complete
- ✅ SSA destruction (phi elimination)
- ✅ Virtual register generation
- ✅ Graph-coloring register allocator for x86-64
- ✅ Liveness analysis
- ✅ Spilling algorithm

**Success Criteria:**
- Compiler has modern three-stage IR pipeline
- Register allocator makes efficient use of physical registers
- Spilling algorithm minimizes stack usage
- Full pipeline is self-hosting (compiles itself)
- Passes all regression tests

**Team:** 3 developers (1 LIR lowering, 2 register allocation)

---

### **Phase 4: Advanced Optimizations (Target: v0.8.3)**

**Timeline:** 4-6 months

**Goal:** Implement advanced, whole-program optimizations.

**Deliverables:**
- ✅ Profile-Guided Optimization (PGO) infrastructure
- ✅ Link-Time Optimization (LTO) framework
- ✅ SIMD auto-vectorization (simple loops)
- ✅ Advanced inlining heuristics
- ✅ Alias analysis improvements

**Success Criteria:**
- PGO provides **10-30% speedup** on real-world benchmarks
- LTO enables cross-module optimizations
- Runa performance on standard benchmarks competitive with C++/Rust
- SIMD vectorization provides measurable speedup on applicable loops

**Team:** 4 developers (2 PGO/LTO, 2 vectorization)

---

## **Success Criteria**

### **Phase 1 Success Metrics**
- [ ] HIR correctly represents 100% of Runa language features
- [ ] Triple Syntax system generates valid Runa code in all modes
- [ ] Type checker catches all type errors (zero false negatives)
- [ ] HIR serves as foundation for Rosetta Stone translation

### **Phase 2 Success Metrics**
- [ ] SSA construction is correct (passes formal verification tests)
- [ ] Optimization passes provide measurable improvements:
  - Code size reduction: **10-20%**
  - Execution time improvement: **10-20%**
- [ ] MIR optimization suite is modular and extensible

### **Phase 3 Success Metrics**
- [ ] Register allocator achieves **>90%** physical register utilization
- [ ] Spilling overhead is minimal (< **5%** performance impact)
- [ ] Full pipeline is self-hosting (compiles Runa compiler)
- [ ] Zero register allocation bugs in production use

### **Phase 4 Success Metrics**
- [ ] PGO improves performance by **10-30%** on profiled benchmarks
- [ ] LTO enables whole-program optimization (verified by benchmarks)
- [ ] Runa matches or exceeds C++/Rust performance on standard benchmarks:
  - Fibonacci: within **5%** of Rust
  - Matrix multiplication: within **10%** of C++
  - Sorting algorithms: within **5%** of Rust
- [ ] SIMD auto-vectorization provides **2-4x** speedup on vectorizable loops

### **Overall Success Criteria**

**Technical Excellence:**
- Gungnir becomes the foundation for all CPU compilation in Runa
- Performance is competitive with industry-leading compilers
- Three-stage IR pipeline is maintainable and extensible

**Developer Impact:**
- Runa developers see performance parity with C++/Rust
- Compiler is fast enough for interactive development
- Self-hosting compiler is production-ready

**Ecosystem Value:**
- Gungnir enables Rosetta Stone cross-language translation
- Triple Syntax system improves code accessibility
- Foundation for future compiler innovations (AOTT, etc.)

---

## **Related Documentation**

- [BIFROST_ARCHITECTURE_PLAN.md](BIFROST_ARCHITECTURE_PLAN.md) - Accelerator compilation pipeline (complementary to Gungnir)
- [COMPLETE_MODEL_ARCHITECTURE.md](COMPLETE_MODEL_ARCHITECTURE.md) - Overall SyberCraft SCO architecture
- [Runa Development Roadmap](../../runa/docs/dev/DEVELOPMENT_ROADMAP.md) - Overall language development timeline
- Rosetta Stone Architecture - Details on HIR-based cross-language translation

---

**END OF DOCUMENT**
