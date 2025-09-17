# AOTT - All-Of-The-Time Compilation System

AOTT is Runa's revolutionary tiered execution system that **replaces traditional JIT and AOT compilation** with a continuous optimization approach that spans from interpretation to maximum speculation.

## The AOTT Philosophy

**"All-Of-The-Time"** means optimization happens continuously throughout your program's lifetime:
- **Tier 0**: Immediate execution via interpretation
- **Tier 1**: Basic native compilation for warm code
- **Tier 2**: Advanced optimizations for hot code  
- **Tier 3-4**: Speculative execution for critical paths

## Architecture Overview

```
Bytecode Input → [T0 Lightning] → Profile Collection
                        ↓
              Warm Detection → [T1 Bytecode] → More Profiles
                        ↓
              Hot Detection → [T2 Native] → Advanced Profiles
                        ↓  
              Critical Detection → [T3 Optimized] → Speculation Data
                        ↓
              Maximum Performance → [T4 Speculative] → Guards & Deopt
                        ↓
              Guard Failure → [Deoptimization] → Back to T0/T1
```

## Directory Structure

- `core/` - Main orchestration and coordination (Runa)
- `tiers/` - Execution engines for each tier (Rust for performance)
- `analysis/` - Runtime analysis and optimization (Runa)  
- `compilation/` - Runtime compilation infrastructure (Rust/Runa)
- `memory/` - AOTT-specific memory management (Runa)
- `profiling/` - Profile collection and analysis (Runa)
- `deoptimization/` - Deopt and on-stack replacement (Rust)

## Execution Tiers

### Tier 0: Lightning Interpreter
- **Purpose**: Zero-cost startup, immediate execution
- **Implementation**: Ultra-fast interpreter with minimal overhead
- **Performance**: ~1x baseline (but zero startup cost)

### Tier 1: Bytecode Execution
- **Purpose**: Smart bytecode execution with optimizations
- **Implementation**: Optimized bytecode interpreter with profiling hooks
- **Performance**: ~2-3x improvement over lightning interpreter

### Tier 2: Native Execution  
- **Purpose**: Aggressive native compilation for warm code
- **Implementation**: LLVM-based native code generation
- **Performance**: ~10-20x improvement over bytecode

### Tier 3: Optimized Native
- **Purpose**: Heavily optimized native compilation for hot code
- **Implementation**: Advanced inlining, vectorization, loop optimization
- **Performance**: ~30-50x improvement over baseline

### Tier 4: Speculative Execution
- **Purpose**: Maximum performance through speculation for critical paths
- **Implementation**: Value/type speculation with deoptimization guards
- **Performance**: ~50-100x improvement (when speculation succeeds)

## Key Features

### Progressive Optimization
- Code starts at Tier 0 and promotes based on execution frequency
- No upfront compilation cost - optimization pays for itself
- Hotness thresholds adapt based on program behavior

### Advanced Analysis
- Call graph analysis for inlining decisions
- Escape analysis for stack allocation
- Type feedback for devirtualization
- Dataflow analysis for optimization opportunities

### Robust Deoptimization
- Speculation guards that trigger deoptimization on failure
- On-stack replacement for tier transitions
- State reconstruction to return to interpreter

### Multiple Backends
- LLVM for high-quality native code
- Direct x86-64/ARM64 for fast compilation
- WebAssembly for portability

## Performance Goals

AOTT aims to match or exceed:
- **HotSpot JVM**: Better startup, competitive steady-state
- **V8 JavaScript**: Superior tiered approach, better memory usage
- **PyPy**: More sophisticated speculation, cleaner deoptimization

## Integration Points

- **Receives from**: Compiler (bytecode + metadata), RunaTime (execution requests)
- **Provides to**: RunaTime (execution results), Self (tier promotion decisions)
- **Coordinates with**: GC (safe points), Debugger (breakpoints)

## Development Status

🚧 **Under Construction** - Fresh implementation replacing the old VM entirely.

**Current Priority**: Tier 0 interpreter to replace existing `vm.rs`

See `../../docs/plans/RUNA_AOTT_ARCHITECTURE_PLAN.md` for detailed implementation plan.