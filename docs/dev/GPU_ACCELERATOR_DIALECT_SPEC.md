# Runa GPU/Accelerator Dialect (MIR/LIR) Specification
## Portable GPU/Accelerator IR for CUDA, Metal, OpenCL, DSP, FPGA

## Version History
| Version | Date | Changes |
|---|---|---|
| 1.0 | 2025-10-17 | Initial specification: MIR.GPU dialect, LIR.GPU ops, reflection schema, backend mappings (CUDA, Metal, OpenCL, DSP, FPGA), rationale and rollout plan |

**Version:** 1.0  
**Status:** Production design (implementation-ready)  
**Classification:** Proprietary  
**Last Updated:** 2025-10-17  
**Authors:** Sybertnetics SCO Architecture Team  
**Model Type:** Compiler IR Design - GPU/Accelerator Dialect  
**Architecture:** HIR → MIR (with GPU dialect) → LIR (with GPU sub-dialect) → Target Backends (CUDA PTX, Metal MSL, OpenCL C, DSP ISA/LLVM, FPGA HDL/DSL)

---

## 0. Executive Summary
- We define a target-independent GPU/accelerator dialect across MIR and LIR to support CUDA, Metal, OpenCL, DSP, and FPGA from one pipeline.
- SPIR-V is not used internally. We emit target formats directly from LIR.GPU.
- The design is production-ready: types, ops, memory spaces, atomics, barriers, builtins, resources, reflection, and deterministic lowering contracts are specified.

---

## 1. Why start now
- Types: vector/matrix/fixed-width/atomic types must exist in MIR/LIR for GPU codegen.
- Memory model: distinct storage spaces (private, workgroup/shared, global, constant) require MIR metadata and LIR storage classes.
- Abstraction boundaries: isolating GPU semantics in MIR/LIR avoids polluting HIR and enables multi-backend portability.
- Target-independent optimizations: generic parallelism (workgroup tiling, vectorization, barrier placement) can be expressed early.

---

## 2. Dialect Overview
- HIR: language semantics, annotations (e.g., @kernel, @compute, @vertex, @fragment).
- MIR + MIR.GPU dialect: portable parallel semantics (execution model, resources, builtins, barriers) and reflection metadata.
- LIR + LIR.GPU sub-dialect: target-concrete ops with explicit widths, layouts, storage classes, and 1:1 mapping to backends.

---

## 3. Types (MIR/LIR)
- Scalars: i8/i16/i32/i64, u8/u16/u32/u64, f16/f32/f64, bool.
- Vectors: vecN<T>, N ∈ {2,3,4,8,16} (target may lower to native widths or scalarize).
- Matrices: matCxR<f16/f32/f64> (row-major canonical; layout lowered per target).
- Pointers: ptr<space, T> where space ∈ {private, workgroup, global, constant}.
- Atomics: atomic<T> where T ∈ {i32/u32/i64/u64}; ordering ∈ {relaxed, acquire, release, acq_rel, seq_cst}.
- Images/Samplers/Buffers (opaque): image2d, image3d, sampler, storage_buffer, uniform_buffer, acceleration_structure (opaque handles; lowered by backend).

---

## 4. Memory Model & Storage Classes
- Spaces: private (per-thread), workgroup (shared), global (device), constant (read-only), push_constants (Metal: argument buffers; CUDA: kernel params; OpenCL: __constant).
- Addressing:
  - MIR: attach `storage(space)` to variables; resources carry binding metadata.
  - LIR: make storage class explicit in every var/op.
- Synchronization scopes: thread, subgroup/warp, workgroup, device; memory scopes map to target intrinsics.

---

## 5. Execution Model & Builtins
- Kernel entry kinds: compute, vertex, fragment, mesh/task (future), raygen/miss/closesthit (future).
- Builtins (MIR): global_id.xyz, local_id.xyz, workgroup_id.xyz, num_workgroups.xyz, subgroup_id, subgroup_size, subgroup_local_id, vertex_index, instance_index, frag_coord.
- Lowering contract (LIR): each builtin maps to a concrete target intrinsic/variable (e.g., PTX `%ctaid/%ntid/%tid`, Metal `thread_position_in_grid`, OpenCL `get_global_id`).

---

## 6. MIR.GPU Dialect (Portable Ops & Metadata)
### 6.1 Annotations (Attributes)
- `@kernel(stage=compute|vertex|fragment, workgroup_size=(x,y,z), local_size_hint=(x,y,z)?)`
- `@resource(set, binding, space=uniform|storage|sampler|image, name, layout=std140|std430|metal)`
- `@push_constants(size, align)`
- `@io(location, interpolation=?, builtin=?)`

### 6.2 MIR Ops (selected)
- Control: structured loops, if/else, switch (no unstructured gotos).
- Memory:
  - `gpu.alloc(space, type, count?) → ptr`
  - `gpu.load(ptr, ordering?) → val`
  - `gpu.store(ptr, val, ordering?)`
  - `gpu.atomic(op, ptr<atomic<T>>, val, ordering, scope) → T`
- Barriers & fences:
  - `gpu.barrier(exec_scope=workgroup|subgroup|device, mem_scope, semantics)`
  - `gpu.memory_fence(mem_scope, semantics)`
- Builtins:
  - `gpu.global_id(axis)→u32`, `gpu.local_id(axis)`, `gpu.workgroup_id(axis)`, `gpu.num_workgroups(axis)`
  - `gpu.subgroup_id()`, `gpu.subgroup_size()`, `gpu.subgroup_local_id()`
- Resources:
  - `gpu.resource_load(resource, index/coords, ...)`
  - `gpu.resource_store(resource, index/coords, val, ...)`
- Images/Samplers (optional in MIR; can be modeled as resources + intrinsics):
  - `gpu.sample(image, sampler, coords, lod|grad?)`

### 6.3 Reflection Metadata (MIR)
- Entry points: stage, workgroup_size, required features.
- IO: inputs/outputs with locations and types.
- Resources: descriptor sets/bindings (or argument buffer indices), space, type, size, stride, layout.
- Push constants / kernel parameters layout.

---

## 7. LIR.GPU Sub-Dialect (Concrete Ops)
- All ops are SSA with explicit types, widths, storage, and layout. Each op has a lowering note per backend.

### 7.1 Core ops
- `lir.var(storage, type, align, size?) → ptr` (allocated lifetime-scope)
- `lir.load(ptr, volatility=?, ordering=?, scope=?) → T`
- `lir.store(ptr, val, volatility=?, ordering=?, scope=?)`
- `lir.atomic_add/sub/and/or/xor/min/max(ptr<atomic<T>>, val, ordering, scope) → T`
- `lir.barrier(exec_scope, mem_scope, semantics)`
- `lir.mem_fence(mem_scope, semantics)`

### 7.2 Builtins (LIR intrinsics)
- `lir.id_global_x/y/z() → u32`, `lir.id_local_x/y/z() → u32`, `lir.id_group_x/y/z() → u32`
- `lir.num_groups_x/y/z() → u32`, `lir.subgroup_size() → u32`, `lir.subgroup_local_id() → u32`

### 7.3 Resources & IO
- `lir.bind_uniform(set, binding) → handle`, `lir.bind_storage(set, binding) → handle`
- `lir.buffer_load(handle, byte_offset, T) → T`, `lir.buffer_store(handle, byte_offset, T)`
- `lir.image_sample(handle_img, handle_samp, coords, options) → vecN<f32>`
- `lir.image_load/store(handle_img, coords, T)`
- IO registers: `lir.read_input(location, T)`, `lir.write_output(location, T)`

### 7.4 Control & Math
- Structured control mirrored from MIR; lowered to target branching.
- Math ops map to target instruction sets or lib calls where needed.

---

## 8. Reflection Artifact (JSON)
Generated alongside device code for runtime binding.
```json
{
  "module": "runa_kernel_pack",
  "entries": [
    {
      "name": "my_kernel",
      "stage": "compute",
      "workgroup_size": [8,8,1],
      "resources": [
        {"set":0, "binding":0, "space":"storage", "type":"buffer", "size":4096, "stride":16, "name":"data"}
      ],
      "push_constants": {"size": 32, "align": 16},
      "inputs": [],
      "outputs": []
    }
  ]
}
```
- Deterministic ordering; stable schema versioned in docs.

---

## 9. Backend Mappings (Deterministic Contracts)

### 9.1 CUDA (PTX)
- Builtins: `id_global` → `%ctaid * %ntid + %tid`; local/group variables map to `.shared` (workgroup) and `.local` (private).
- Memory spaces: private→`.local`, workgroup→`.shared`, global→`.global`, constant→`.const`.
- Barriers: `bar.sync` (workgroup), memory fences via `membar.*`.
- Atomics: `atom.global.add.*`, `atom.shared.add.*` with ordering mapped to CUDA semantics (promote when necessary).
- Output: `.ptx` text; optional `ptxas` integration left to toolchain.

### 9.2 Metal (MSL)
- Builtins: `thread_position_in_grid`, `thread_position_in_threadgroup`, `threadgroup_position_in_grid`.
- Memory spaces: private→`thread`, workgroup→`threadgroup`, global→`device`, constant→`constant`.
- Barriers: `threadgroup_barrier(mem_flags)`.
- Resources: argument buffers / buffer indices map from (set,binding) deterministically.
- Output: `.metal` text; platform: macOS, iOS, tvOS, watchOS (select dialect by target flag).

### 9.3 OpenCL (OpenCL C)
- Builtins: `get_global_id`, `get_local_id`, `get_group_id`.
- Memory spaces: `__private`, `__local`, `__global`, `__constant`.
- Barriers: `barrier(flags)`.
- Output: OpenCL C kernel source; optional SPIR-V is out-of-scope by design.

### 9.4 DSP
- Define target profiles with:
  - Vector width, lane count, alignment requirements.
  - Available atomics/barriers (often limited or absent).
  - Memory bank layout (SRAM/DRAM) and DMA hooks.
- Lowering: scalarize or vectorize ops; schedule barriers to device constraints; provide intrinsics for saturation and fixed-point when required.
- Output: DSP ISA or LLVM IR for vendor toolchains.

### 9.5 FPGA
- Profiles:
  - Pipelining annotations (II), unroll factors, on-chip memory placement (BRAM/URAM), stream interfaces.
  - Static allocation of `workgroup` memory to BRAM blocks; `global` via AXI.
- Lowering: convert kernels to dataflow + loops with explicit pragmas (e.g., `#pragma HLS pipeline`, `unroll`).
- Output: vendor HDL/DSL (e.g., HLS C/C++, MLIR-affine/HLS dialect), driven by our LIR semantics and reflection.

---

## 10. Validation & CI
- Unit tests: MIR→LIR lowering; LIR verifier (storage classes, widths, alignment, barrier placement checks).
- Backend tests: generate target code; run vendor validators/tools where possible (PTX lint, Metal compile check, OpenCL build, DSP/FPGA synthesis dry-run modes).
- Golden tests: end-to-end kernels with known outputs; compare across targets where semantics align.

---

## 11. Implementation Plan (Phased)
- Phase A (now):
  - Implement MIR.GPU attributes/ops and reflection collector.
  - Implement LIR.GPU ops with verifier.
  - Add JSON reflection emitter.
- Phase B:
  - Implement CUDA PTX emitter; run conformance tests on NVIDIA.
  - Implement Metal MSL emitter for macOS/iOS/tvOS/watchOS.
  - Implement OpenCL C emitter for CPU/GPU.
- Phase C:
  - Implement DSP backend for selected device family (specify profiles).
  - Implement FPGA HLS backend (C++/pragmas or MLIR-based) with resource/pipeline controls.

---

## 12. Non-Goals (for clarity)
- No internal SPIR-V; Vulkan is not a first-class backend in this design.
- No dependency on Khronos specs for internal IR semantics.

---

## 13. Appendix: Op Tables (abbrev)
- Atomics: add, sub, and, or, xor, min, max (signed/unsigned), exchange, compare_exchange.
- Semantics flags: acquire, release, acq_rel, seq_cst; scopes: thread, subgroup, workgroup, device.
- Image ops: sample, fetch, read, write; backends may lower to lib/intrinsics or reject when unsupported.

---

## 14. Target Capability Profiles & Feature Detection

### 14.1 Backend Capability Tiers
All backends are classified into capability tiers that determine which LIR.GPU features are supported:

#### Tier 1: Full GPU (CUDA, Metal, OpenCL)
- **Execution Model**: Full SIMT/SIMD threading with subgroups/warps
- **Memory Spaces**: All (private, workgroup, global, constant)
- **Atomics**: Full hardware support with all orderings
- **Barriers**: Hardware execution and memory barriers
- **Images/Samplers**: Native texture unit support
- **Vectors**: Native vector types (vec2/3/4/8/16)
- **Matrices**: Native or efficiently lowered matrix ops
- **Subgroup Ops**: Shuffle, broadcast, vote, ballot

#### Tier 2: Limited Parallel (DSP)
- **Execution Model**: SIMD vectors, limited or no threading
- **Memory Spaces**: Private, global (workgroup emulated via scratchpad)
- **Atomics**: Software emulation via critical sections (performance penalty)
- **Barriers**: Software semaphore emulation (limited scalability)
- **Images/Samplers**: Software-emulated interpolation only
- **Vectors**: Native SIMD vectors (width varies: 2/4/8/16 depending on ISA)
- **Matrices**: Scalarized or manually vectorized
- **Subgroup Ops**: Not supported (subgroup_size=1)

#### Tier 3: Dataflow (FPGA)
- **Execution Model**: Spatial pipeline, no threading concept
- **Memory Spaces**: Private (registers/BRAM), global (AXI/DDR)
- **Atomics**: Synthesized arbitration logic (expensive, discouraged)
- **Barriers**: Converted to pipeline flush or stream synchronization
- **Images/Samplers**: Not supported (reject or software emulation)
- **Vectors**: Synthesized as parallel datapaths
- **Matrices**: Synthesized as systolic arrays (manual pragma required)
- **Subgroup Ops**: Not applicable

### 14.2 Feature Detection & Graceful Degradation

#### LIR Feature Query Op
```
lir.target_supports(feature_name: string) → bool
```
- Features: `atomics`, `barriers`, `subgroups`, `images`, `matrices`, `vectors.width.N`
- Compile-time constant; enables conditional lowering paths
- Example usage:
```
if lir.target_supports("atomics"):
    result = lir.atomic_add(ptr, val, ordering, scope)
else:
    # Fallback: critical section emulation
    lir.begin_critical_section()
    tmp = lir.load(ptr)
    tmp = tmp + val
    lir.store(ptr, tmp)
    lir.end_critical_section()
```

#### Backend Behavior for Unsupported Features
- **Default**: Emit compile-time error with clear message
- **Opt-in Fallback** (via compiler flag `--allow-gpu-fallback`):
  - Atomics → Critical sections (DSP only)
  - Barriers → NOP with warning (DSP, FPGA)
  - Images → Reject (cannot emulate efficiently)
  - Subgroup ops → Scalarize to single-thread (DSP, FPGA)
  - Matrices → Scalarize to loops (DSP, FPGA)

---

## 15. DSP Backend: Detailed Design & Workarounds

### 15.1 Target DSP Families (Priority Order)
1. **Texas Instruments C66x DSP** (TI KeyStone, 8-core VLIW)
   - SIMD: 128-bit (4×f32 or 8×i16)
   - Memory: L1D (32KB), L2 (512KB shared), DDR via EDMA
   - No hardware atomics, no barriers
   - Output: C66x intrinsics or LLVM IR → TI compiler

2. **Qualcomm Hexagon DSP** (Snapdragon SoCs)
   - SIMD: HVX vectors (64/128 bytes)
   - Memory: L2 TCM, DDR
   - Limited atomics (mutex registers), no barriers
   - Output: Hexagon intrinsics or LLVM IR → Hexagon compiler

3. **ARM Helium (M-profile Vector Extension)**
   - SIMD: MVE 128-bit vectors
   - Memory: SRAM, Flash
   - No atomics, no barriers
   - Output: ARM intrinsics or LLVM IR → ARM compiler

### 15.2 DSP-Specific Lowering Strategies

#### Memory Spaces
- **private** → Local registers or stack
- **workgroup** → Scratchpad SRAM (L1D on C66x, TCM on Hexagon)
  - Size limited (32-64KB typical)
  - Statically allocated at kernel launch
- **global** → External DDR/DRAM
  - Access via DMA for efficiency (manual management)
- **constant** → Read-only data in L2 cache or flash

#### Atomics (Software Emulation)
```c
// LIR: lir.atomic_add(ptr, val, relaxed, workgroup)
// Lowered to (TI C66x):
_disable_interrupts();  // Critical section
tmp = *ptr;
*ptr = tmp + val;
_enable_interrupts();
return tmp;
```
- **Performance**: 10-100× slower than hardware atomics
- **Recommendation**: Avoid atomics on DSP; use reduction patterns instead

#### Barriers (Software Emulation via Semaphores)
```c
// LIR: lir.barrier(workgroup, workgroup, acq_rel)
// Lowered to (multi-core DSP):
__sync_synchronize();  // Memory fence
atomic_increment(&barrier_counter);
while (atomic_load(&barrier_counter) < NUM_CORES);
atomic_decrement(&barrier_counter);
```
- **Limitation**: Only works for small core counts (≤8)
- **Recommendation**: Structure code to avoid barriers; use message-passing instead

#### Subgroup Operations
- `subgroup_size()` → Returns `1`
- `subgroup_id()` → Returns `0`
- All subgroup collective ops (shuffle, broadcast, vote) → Reject with error

#### Vectorization Strategy
- Detect vector operations in LIR
- Map to DSP SIMD intrinsics where available:
  - TI C66x: `_dotp2`, `_add4`, `_mpy2`
  - Hexagon HVX: `Q6_V_vadd_VV`, `Q6_V_vmpy_VV`
  - ARM Helium: `vaddq_f32`, `vmulq_f32`
- Scalarize if no matching intrinsic

#### DMA Integration (Critical for Performance)
```
# Annotation in HIR/MIR:
@dsp_dma(source=global_buffer, dest=workgroup_scratch, size=1024, blocking=false)

# Lowered to (TI C66x EDMA):
EDMA3_DRV_setSrcParams(channel, &global_buffer, ...);
EDMA3_DRV_setDestParams(channel, &scratch, ...);
EDMA3_DRV_enableTransfer(channel, EDMA3_DRV_TRIG_MODE_MANUAL);
```

### 15.3 DSP Backend Output Formats
1. **LLVM IR** (preferred):
   - Emit LLVM IR with target-specific intrinsics
   - Leverage vendor's LLVM-based compiler (TI, Hexagon)
   - Enables target-specific optimizations

2. **C with Intrinsics** (fallback):
   - Generate C code with vendor intrinsics
   - Portable across DSP toolchains
   - Less optimized than LLVM IR

3. **Native Assembly** (future):
   - Direct emission of DSP ISA (VLIW packets)
   - Maximum control but high maintenance cost

---

## 16. FPGA Backend: Detailed Design & HLS Integration

### 16.1 Target FPGA Toolchains (Priority Order)
1. **Xilinx Vitis HLS** (AMD FPGAs: Versal, UltraScale+)
   - Input: C/C++ with pragmas
   - Output: RTL (Verilog/VHDL) or XO object files
   - Supports: Pipeline, unroll, array_partition, dataflow pragmas

2. **Intel oneAPI** (Intel FPGAs: Agilex, Stratix)
   - Input: SYCL/C++ with attributes
   - Output: RTL or AOCX bitstreams
   - Supports: [[intel::fpga_pipeline]], [[intel::fpga_memory]]

3. **Open-Source (Future)**: CIRCT (MLIR-based HLS)
   - Input: MLIR dialects (affine, scf, hls)
   - Output: RTL via CIRCT lowering passes
   - Enables vendor-neutral HLS

### 16.2 FPGA Execution Model Transformation

#### From Thread Model to Dataflow Model
**LIR.GPU Thread Semantics:**
```
@kernel(compute, workgroup_size=(64,1,1))
kernel void process(global float* in, global float* out) {
    uint gid = lir.id_global_x();
    float val = lir.buffer_load(in, gid);
    val = val * 2.0;
    lir.buffer_store(out, gid, val);
}
```

**Lowered to Xilinx HLS C++:**
```cpp
void process(hls::stream<float>& in, hls::stream<float>& out, int count) {
#pragma HLS INTERFACE axis port=in
#pragma HLS INTERFACE axis port=out
#pragma HLS PIPELINE II=1
    for (int i = 0; i < count; i++) {
#pragma HLS LOOP_TRIPCOUNT min=64 max=4096
        float val = in.read();
        val = val * 2.0f;
        out.write(val);
    }
}
```

**Key Transformations:**
1. **Iteration Space** → Loop bounds (workgroup_size × num_workgroups)
2. **Global Memory** → AXI master ports or streams
3. **Workgroup Memory** → BRAM arrays with partition pragmas
4. **Barriers** → Dataflow synchronization or loop pipelining boundaries

#### Memory Space Mapping
- **private** → Registers (automatically allocated)
- **workgroup** → On-chip BRAM/URAM
  - Pragma: `#pragma HLS BIND_STORAGE variable=shared type=ram_t2p impl=bram`
  - Partitioning for parallel access: `#pragma HLS ARRAY_PARTITION variable=shared cyclic factor=8`
- **global** → External DDR via AXI
  - Burst access patterns: `#pragma HLS INTERFACE m_axi port=data bundle=gmem0 depth=1024`
- **constant** → ROM (LUTRAM or BRAM)

#### Atomics (Synthesized Arbitration)
```cpp
// LIR: lir.atomic_add(ptr, val, ordering, scope)
// Lowered to HLS with mutex:
#pragma HLS INTERFACE ap_hs port=mutex
void atomic_add(volatile int* ptr, int val) {
    // Hardware mutex or single-cycle read-modify-write
    #pragma HLS PROTOCOL fixed
    #pragma HLS LATENCY min=1 max=1
    *ptr = *ptr + val;  // Synthesized as RMW FSM
}
```
- **Cost**: ~50-200 LUTs + 1-5 BRAMs per atomic variable
- **Recommendation**: Minimize atomics; use reduction trees instead

#### Barriers → Pipeline Flush
```cpp
// LIR: lir.barrier(workgroup, workgroup, acq_rel)
// Lowered to HLS:
#pragma HLS PIPELINE OFF  // Disable pipeline at barrier point
// Insert explicit sync or dataflow handshake
```
- FPGAs don't have "threads" to synchronize
- Barriers indicate pipeline flush points or dataflow stage boundaries

### 16.3 FPGA-Specific Annotations

#### Pipeline Control
```
@fpga_pipeline(II=1, enable=true, style=flp)
lir.loop(i, 0, N) {
    // Loop body pipelined with initiation interval = 1
}
```
→ Lowers to: `#pragma HLS PIPELINE II=1 style=flp`

#### Loop Unrolling
```
@fpga_unroll(factor=4)
lir.loop(i, 0, N) { ... }
```
→ Lowers to: `#pragma HLS UNROLL factor=4`

#### Array Partitioning
```
@fpga_partition(mode=cyclic, factor=8, dim=1)
lir.var(workgroup, float[1024], align=4) → scratch
```
→ Lowers to: `#pragma HLS ARRAY_PARTITION variable=scratch cyclic factor=8 dim=1`

#### Dataflow Regions
```
@fpga_dataflow
{
    stage1(in, tmp);  // Concurrent execution
    stage2(tmp, out);
}
```
→ Lowers to: `#pragma HLS DATAFLOW`

### 16.4 FPGA Backend Output Formats
1. **Vitis HLS C/C++** (Xilinx):
   - C++14 with HLS pragmas
   - Template metaprogramming for parameterization
   - Output: `.cpp` files + TCL build script

2. **Intel oneAPI SYCL** (Intel):
   - SYCL kernels with FPGA attributes
   - Output: `.cpp` files + CMake configuration

3. **CIRCT MLIR** (Future):
   - MLIR HLS dialect
   - Output: `.mlir` files → CIRCT → RTL

---

## 17. Implementation Recommendations

### 17.1 Build Order: IR First, Backends Later
**DO NOT BUILD BACKENDS NOW.** Follow this sequence:

#### Phase A: IR Foundations (Do This First)
1. **Implement MIR.GPU Dialect**:
   - Define MIR.GPU ops in `compiler/mir/ops/gpu/`
   - Implement attributes (`@kernel`, `@resource`, etc.)
   - Build reflection metadata collector
   - **Estimate**: 2-3 weeks

2. **Implement LIR.GPU Sub-Dialect**:
   - Define LIR.GPU ops in `compiler/lir/ops/gpu/`
   - Implement type system (vectors, matrices, atomics, pointers with spaces)
   - Build LIR verifier (storage class checks, alignment, etc.)
   - **Estimate**: 2-3 weeks

3. **Implement MIR→LIR Lowering Pass**:
   - Lower portable MIR.GPU ops to concrete LIR.GPU ops
   - Apply target-independent optimizations (dead code, constant folding)
   - **Estimate**: 1-2 weeks

4. **Implement JSON Reflection Emitter**:
   - Generate reflection artifacts from LIR.GPU metadata
   - **Estimate**: 1 week

**Total Phase A**: 6-9 weeks

#### Phase B: Backend Implementation (Do This After Phase A)
1. **CUDA PTX Backend** (highest priority):
   - LIR.GPU → PTX text emission
   - Validate with NVIDIA `ptxas` compiler
   - **Estimate**: 3-4 weeks

2. **Metal MSL Backend**:
   - LIR.GPU → MSL source emission
   - Test on macOS/iOS
   - **Estimate**: 3-4 weeks

3. **OpenCL C Backend**:
   - LIR.GPU → OpenCL C source emission
   - **Estimate**: 2-3 weeks

#### Phase C: Advanced Backends (Do This Last)
1. **DSP Backend** (TI C66x or Hexagon):
   - LIR.GPU → LLVM IR with DSP intrinsics
   - Implement software emulation for atomics/barriers
   - **Estimate**: 4-6 weeks

2. **FPGA Backend** (Xilinx Vitis HLS):
   - LIR.GPU → HLS C++ with pragmas
   - Implement dataflow transformations
   - **Estimate**: 6-8 weeks

### 17.2 Why IR First?
1. **Stable Foundation**: Backends depend on stable IR contracts; changing IR after backends are built is costly
2. **Parallel Development**: Multiple backends can be built concurrently once IR is stable
3. **Testing Infrastructure**: IR-level tests are faster and more comprehensive than end-to-end backend tests
4. **Design Validation**: Building IR forces you to resolve semantic ambiguities early

---

## 18. Potential Issues & Mitigations

### Issue 1: Barrier Semantics Across Targets
**Problem**: Barrier semantics differ significantly between targets.

**Mitigation**:
- Document exact lowering for each target in spec
- DSP: Emit software semaphore with performance warning
- FPGA: Convert to pipeline flush or reject if inside tight loop
- Add `--strict-barriers` flag to error on unsupported targets

### Issue 2: Subgroup Size Variability
**Problem**: Subgroup sizes vary (CUDA=32, Metal=32/64, OpenCL=variable, DSP=1).

**Mitigation**:
- `subgroup_size()` is runtime query for OpenCL/Metal
- Compile-time constant for CUDA/DSP/FPGA
- Compiler can specialize code paths if size is known

### Issue 3: Atomics on DSP/FPGA
**Problem**: No hardware atomics on most DSPs; expensive synthesis on FPGA.

**Mitigation**:
- Emit error by default
- `--allow-atomic-fallback` flag enables software emulation (DSP) or synthesis (FPGA)
- Provide alternative: reduction tree pattern in standard library

### Issue 4: Image/Sampler on DSP/FPGA
**Problem**: No texture units.

**Mitigation**:
- Reject image/sampler ops with clear error message
- Provide manual interpolation library functions as alternative
- Document in user guide: "Images not supported on DSP/FPGA"

### Issue 5: Matrix Operations
**Problem**: Only CUDA/Metal have native matrix support.

**Mitigation**:
- OpenCL: Scalarize to loops (acceptable performance loss)
- DSP: Vectorize with SIMD intrinsics
- FPGA: Synthesize systolic array with pragma annotations
- Add `lir.target_supports("matrices.native")` query

---

## 19. Updated Version History
| Version | Date | Changes |
|---|---|---|
| 1.0 | 2025-10-17 | Initial specification |
| 1.1 | 2025-10-18 | Added sections 14-19: Target capability profiles, feature detection, detailed DSP/FPGA designs, implementation recommendations, issue mitigations |

**Last Updated:** 2025-10-18

---

## 20. Key Takeaway
Designing the MIR/LIR GPU dialect now prevents costly retrofits, enables immediate CUDA/Metal/OpenCL, and establishes the abstractions needed to extend into DSP/FPGA with predictable, deterministic lowering contracts.

**Build the IR layers first (Phase A), then implement backends (Phase B/C).** This approach ensures a stable foundation and enables parallel backend development.
