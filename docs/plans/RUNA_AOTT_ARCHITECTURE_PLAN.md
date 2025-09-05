# RUNA AOTT (All-of-The-Time) Architecture Plan

## Executive Summary

This document provides a comprehensive plan for Runa's AOTT (All-of-The-Time) execution system, detailing how it replaces existing components, enhances performance, and provides a tiered execution strategy that rivals or exceeds modern language runtimes like HotSpot JVM, V8, and .NET CLR.

## Current Runa Architecture Analysis

### Existing Execution Flow
```
Runa Source Code
    ↓
Lexer (runa/src/compiler/lexer/) → Tokens
    ↓
Parser (runa/src/compiler/parser/) → AST
    ↓
Semantic Analysis (runa/src/compiler/semantic/) → Validated AST
    ↓
HIR Builder (runa/src/compiler/ir/hir/) → High-level IR
    ↓
MIR Builder (runa/src/compiler/ir/mir/) → Mid-level IR
    ↓
LIR Builder (runa/src/compiler/ir/lir/) → Low-level IR
    ↓
Bytecode Generator (runa/src/compiler/ir/lir/bytecode_generator.runa) → Bytecode
    ↓
VM Execution (runa/_legacy/src/runtime/vm.rs) → Direct Interpretation [LEGACY - BEING REPLACED]
```

### Components Being Replaced by AOTT

#### 1. **Primary Replacement: VM Interpreter (`runa/_legacy/src/runtime/vm.rs`)**
- **Current State**: Basic bytecode interpreter
- **AOTT Replacement**: Tiered execution system with 5 optimization tiers
- **Performance Impact**: 10-100x execution speed improvement

#### 2. **Enhanced Integration: Bytecode Generator**
- **Current**: Simple bytecode emission
- **AOTT Enhancement**: Profile-guided bytecode generation with speculation points
- **New Capabilities**: Deoptimization metadata, guard insertion, tier transition points

#### 3. **Runtime Memory Management Integration**
- **Current**: Basic garbage collection (`runa/_legacy/src/runtime/gc.rs`) [LEGACY]
- **AOTT Integration**: Enhanced GC (`runa/src/runatime/core/memory/garbage_collector.runa`)
- **AOTT Enhancement**: Escape analysis-driven allocation, speculative object pooling
- **Memory Performance**: 2-5x allocation speed improvement

## AOTT Architecture Deep Dive

### Tier 0: Lightning Interpreter
**Location**: `/runatime/src/aott/execution/lightning/`

**Purpose**: Ultra-fast startup, minimal overhead execution
- Direct bytecode interpretation with computed goto dispatch
- Zero-cost profiling and promotion detection
- Hardware-accelerated instruction dispatch
- Serves as entry point and deoptimization target

**Key Components** (Actual Implementation):
```rust
pub struct LightningInterpreter {
    /// Lightning-fast instruction dispatcher
    dispatcher: InstructionDispatcher,
    /// Minimal stack machine for execution
    stack_machine: MinimalStackMachine,
    /// Zero-cost profiling hooks
    profiler: ZeroCostProfiler,
    /// Promotion detection system
    promotion_detector: PromotionDetector,
}
```

**Replaces**: Current `vm.rs` basic interpreter

### Tier 1: Smart Bytecode Execution
**Location**: `/runatime/src/aott/execution/bytecode/`

**Purpose**: Enhanced bytecode execution with smart optimizations
- Optimized dispatch system with inline caching
- Basic profiling hooks and tier promotion detection
- Enhanced stack machine with overflow protection
- Smart bytecode optimization pipeline

**Key Components** (Actual Implementation):
```rust
pub struct BytecodeExecutor {
    /// Smart execution engine
    execution_engine: BytecodeExecutionEngine,
    /// Optimized dispatch system
    dispatch_system: OptimizedDispatchSystem,
    /// Profiling integration
    profiler: BytecodeProfiler,
    /// Optimization pipeline
    optimizer: BytecodeOptimizer,
}
```

**Integration**: Processes bytecode with profiling and optimization before tier promotion

### Tier 2: Basic Native Execution
**Location**: `/runatime/src/aott/execution/native/`

**Purpose**: LLVM-based native code generation and execution
- Basic native compilation using LLVM backend
- Code caching for compiled functions
- Profile collection for higher-tier optimization
- Native execution monitoring

**Key Components** (Actual Implementation):
```rust
pub struct NativeExecutor {
    /// LLVM compiler interface
    llvm_compiler: LLVMCompilerInterface,
    /// Code cache manager
    code_cache: NativeCodeCache,
    /// Execution monitor
    execution_monitor: NativeExecutionMonitor,
    /// Execution statistics
    execution_stats: NativeExecutionStatistics,
}
```

**Integration**: Compiles hot functions to native code with basic optimizations

### Tier 3: Optimized Native Execution
**Location**: `/runatime/src/aott/execution/optimized/`

**Purpose**: Heavily optimized native execution with advanced analysis
- Advanced compilation pipeline with aggressive optimizations
- Vectorization, inlining, and interprocedural optimizations
- Advanced register allocation and memory management
- Performance monitoring and optimization feedback

**Key Components** (Actual Implementation):
```rust
pub struct OptimizedNativeExecutor {
    /// Advanced compilation pipeline
    compilation_pipeline: AdvancedCompilationPipeline,
    /// Optimization engine
    optimization_engine: OptimizationEngine,
    /// Performance monitoring
    performance_monitor: PerformanceMonitor,
    /// Execution statistics
    execution_stats: OptimizedExecutionStatistics,
}
```

**Integration**: Applies maximum optimizations to performance-critical code

### Tier 4: Speculative Execution
**Location**: `/runatime/src/aott/execution/speculative/`

**Purpose**: Maximum performance through aggressive speculation
- Value speculation and type prediction
- Polymorphic inline caching and guard validation
- Loop specialization and speculative optimizations
- Runtime assumption validation with deoptimization

**Key Components** (Actual Implementation):
```rust
pub struct SpeculativeExecutor {
    /// Speculation coordinator
    speculation_coordinator: SpeculationCoordinator,
    /// Execution engine
    execution_engine: SpeculativeExecutionEngine,
    /// Guard validation system
    guard_validator: GuardValidationSystem,
    /// Performance monitor
    performance_monitor: SpeculativePerformanceMonitor,
}
```

**Integration**: Maximum performance through validated runtime speculation

## Detailed Component Integration Plan

### Phase 1: Execution Engine Implementation

#### 1.1 Lightning Interpreter (`lightning/`)
- ✅ Hardware-accelerated instruction dispatch
- ✅ Zero-cost profiling integration
- ✅ Complete stack machine implementation
- ✅ Promotion detection system
- ✅ All instruction handlers implemented

**Key Achievements**:
- Ultra-fast startup (minimal overhead)
- Computed goto dispatch for maximum performance
- Thread-safe execution support
- Comprehensive instruction set coverage
- Integration with AOTT tier promotion system

#### 1.2 Smart Bytecode Execution (`bytecode/`)
**Current Implementation Status**:
- Enhanced dispatch system with inline caching
- Basic profiling hooks implementation
- T1 optimizer for bytecode-level optimizations
- Profile collection infrastructure

**Integration Strategy**:
```runa
Process called "execute_smart_bytecode" that takes bytecode as BytecodeProgram returns ExecutionResult:
    Let executor be BytecodeExecutor::new()
    Let optimizer be T1Optimizer::new()

    Note: Apply basic bytecode optimizations
    Let optimized_bytecode be optimizer.optimize(bytecode)

    For instruction in optimized_bytecode.instructions:
        Let result be executor.execute_instruction(instruction)
        executor.profiler.record_execution(instruction, result)

        Note: Check for tier promotion to T2 Native
        If executor.should_promote_to_native(instruction.function_id):
            Return TierPromotionRequest { target_tier: Tier2, function_id: instruction.function_id }

    Return ExecutionResult::Success
```

#### 1.3 Basic Native Execution (`native/`)
**Current Implementation Status**:
- LLVM compiler interface implementation
- Code cache management system
- Profile collection for optimization feedback
- Native execution monitoring

**Implementation Strategy**:
```runa
Process called "execute_native" that takes bytecode as BytecodeFunction, profile as ProfileData returns NativeResult:
    Let native_executor be NativeExecutor::new()
    Let llvm_compiler be LLVMCompilerInterface::new()

    Note: Check code cache first
    If native_executor.code_cache.has_compiled(bytecode.function_id):
        Let cached_code be native_executor.code_cache.get(bytecode.function_id)
        Return native_executor.execute_cached(cached_code)

    Note: Compile to native code
    Let llvm_ir be llvm_compiler.bytecode_to_llvm_ir(bytecode)
    Let native_code be llvm_compiler.compile_to_native(llvm_ir)

    Note: Cache compiled code
    native_executor.code_cache.store(bytecode.function_id, native_code)

    Note: Execute with profiling
    Let result be native_executor.execute(native_code)
    native_executor.execution_monitor.record_execution(bytecode.function_id, result)

    Return result
```

#### 1.4 Optimized Native Execution (`optimized/`)
**Current Implementation Status**:
- Advanced compilation pipeline framework
- Vectorization engine implementation
- Inlining engine with cost-benefit analysis
- Register allocation system
- Loop optimization infrastructure

**Implementation Strategy**:
```runa
Process called "execute_optimized_native" that takes bytecode as BytecodeFunction returns OptimizedResult:
    Let optimized_executor be OptimizedNativeExecutor::new()
    Let compilation_pipeline be AdvancedCompilationPipeline::new()

    Note: Apply comprehensive optimizations
    Let analysis_results be compilation_pipeline.analyze(bytecode)
    Let optimized_ir be compilation_pipeline.optimize(bytecode, analysis_results)

    Note: Vectorize and inline where beneficial
    Let vectorized_ir be optimized_executor.vectorization_engine.vectorize(optimized_ir)
    Let inlined_ir be optimized_executor.inlining_engine.inline(vectorized_ir)

    Note: Generate optimized native code
    Let optimized_code be compilation_pipeline.compile_to_native(inlined_ir)

    Note: Execute with advanced monitoring
    Let result be optimized_executor.execute(optimized_code)
    optimized_executor.performance_monitor.record_metrics(bytecode.function_id, result)

    Return result
```

#### 1.5 Speculative Execution (`speculative/`)
**Current Implementation Status**:
- Speculation coordinator framework
- Guard validation system implementation
- Value speculation engine
- Type speculation and PIC management
- Loop specialization infrastructure

**Implementation Strategy**:
```runa
Process called "execute_speculative" that takes bytecode as BytecodeFunction returns SpeculativeResult:
    Let speculative_executor be SpeculativeExecutor::new()
    Let speculation_coordinator be SpeculationCoordinator::new()

    Note: Generate speculative assumptions
    Let assumptions be speculation_coordinator.analyze_and_speculate(bytecode)

    Note: Execute with speculation
    Let result be speculative_executor.execute_with_speculation(bytecode, assumptions)

    Note: Validate assumptions and deoptimize if needed
    If speculative_executor.guard_validator.validate_assumptions(assumptions) == false:
        Note: Deoptimize to lower tier
        Return DeoptimizationRequest { target_tier: Tier3, reason: "Speculation failed" }

    Return result
```

### Phase 2: Integration with Existing Compiler Pipeline

#### 2.1 LIR to AOTT Bridge
**Enhancement Location**: `/compiler/ir/lir/bytecode_generator.runa`

**Current Enhancement Needed**:
```runa
Process called "generate_aott_bytecode" that takes lir as LIRProgram returns AOTTBytecode:
    Let bytecode_gen be BytecodeGenerator::new()
    
    Note: Add AOTT-specific metadata
    bytecode_gen.enable_profiling_hooks(true)
    bytecode_gen.enable_speculation_points(true)
    bytecode_gen.enable_deoptimization_metadata(true)
    
    Let bytecode be bytecode_gen.generate(lir)
    
    Note: Insert tier promotion checks
    bytecode = insert_tier_promotion_checks(bytecode)
    
    Return bytecode
```

#### 2.2 Runtime Interface Integration
**Legacy Location**: `runa/_legacy/src/runtime/ffi/runtime_interface.rs`
**Current AOTT Interface**: `runa/src/runatime/services/aott_interface/`

**New System Calls for AOTT**:
- `_rt_aott_execute` - Entry point for AOTT execution
- `_rt_tier_promote` - Manual tier promotion trigger  
- `_rt_deoptimize` - Force deoptimization for debugging
- `_rt_profile_query` - Query execution profiles
- `_rt_speculation_budget` - Manage speculation resources

### Phase 3: Performance Analysis Integration

#### 3.1 Analysis System Enhancement
**Location**: `runa/src/runatime/aott/analysis/`

**Integration Points**:
- **Escape Analysis** → Guide Tier 1+ allocation strategies
- **Dataflow Analysis** → Inform speculation decisions
- **Profile Analysis** → Drive tier promotion decisions
- **Error Handling** → Provide fallback analysis for failed optimizations

#### 3.2 Optimization Pipeline Integration
**Location**: `runa/src/runatime/aott/compilation/optimization_passes/`

**Tier-Specific Optimization Strategies**:
- **T0 Lightning**: No optimization (ultra-fast interpretation only)
- **T1 Smart Bytecode**: Basic optimizations (constant folding, DCE, inline caching)
- **T2 Basic Native**: LLVM basic optimizations (constant folding, DCE, basic inlining)
- **T3 Optimized Native**: Advanced optimizations (vectorization, aggressive inlining, loop specialization)
- **T4 Speculative**: Maximum speculation (value/type speculation, PIC, guard validation)

## Implementation Roadmap

### Milestone 1: Core Execution Engines (COMPLETED ✅)
- ✅ **T0 Lightning Interpreter**: Complete bytecode execution with hardware acceleration
- ✅ **Tier promotion infrastructure**: Promotion detection and request system
- ✅ **Basic profiling**: Zero-cost profiling hooks throughout execution
- ✅ **Instruction dispatch**: Computed goto and optimized dispatch systems

**Success Criteria**: ✅ **ACHIEVED** - Lightning Interpreter executes faster than current VM

### Milestone 2: Enhanced Bytecode Execution (Current Focus)
- 🔄 **T1 Smart Bytecode**: Enhance with inline caching and basic optimizations
- 🔄 **Tier promotion logic**: Complete promotion detection and transition system
- 🔄 **Profile collection**: Comprehensive execution profiling across all tiers
- 🔄 **Integration testing**: End-to-end tier promotion testing

**Success Criteria**: Smart bytecode execution with automatic tier promotion

### Milestone 3: Native Code Generation (Next Phase)
- ⏳ **T2 Basic Native**: LLVM-based compilation with code caching
- ⏳ **T3 Optimized Native**: Advanced optimizations and vectorization
- ⏳ **Performance benchmarking**: Compare tier performance improvements
- ⏳ **Memory management**: Integration with escape analysis

**Success Criteria**: Native execution shows 5-10x performance improvement over T0

### Milestone 4: Speculative Execution (Future Phase)
- ⏳ **T4 Speculative**: Value/type speculation with guard validation
- ⏳ **Deoptimization system**: Seamless fallback between tiers
- ⏳ **Advanced profiling**: ML-driven optimization decisions
- ⏳ **Error recovery**: Robust speculation failure handling

**Success Criteria**: Maximum performance through validated speculation

### Milestone 5: Production Readiness (Final Phase)
- ⏳ **Integration testing**: Full compiler-to-execution pipeline
- ⏳ **Performance monitoring**: Real-time tier performance tracking
- ⏳ **Documentation**: Complete AOTT system documentation
- ⏳ **Beta deployment**: Production-ready with monitoring

**Success Criteria**: Complete AOTT system ready for production deployment

## Performance Expectations

### Benchmark Targets
- **T0 Lightning Startup**: 2-3x faster than current VM
- **T1 Smart Bytecode**: 3-5x faster than current VM
- **T2 Basic Native**: 5-10x faster than current VM
- **T3 Optimized Native**: 10-25x faster than current VM
- **T4 Speculative**: 25-50x faster than current VM (maximum performance)
- **Memory Usage**: 20-30% reduction through escape analysis
- **Tier Promotion Time**: <10ms for T0→T1, <50ms for T1→T2, <200ms for T2→T3

### Tier Performance Progression
- **T0 Lightning**: Ultra-fast startup, minimal overhead interpretation
- **T1 Smart Bytecode**: Enhanced dispatch with inline caching and basic opts
- **T2 Basic Native**: LLVM compilation with code caching
- **T3 Optimized Native**: Advanced optimizations, vectorization, inlining
- **T4 Speculative**: Maximum performance through validated speculation

### Comparison with Industry Standards
- **vs HotSpot JVM**: Superior startup (T0), competitive steady-state (T3-T4)
- **vs V8**: Better tier progression, similar optimization approach
- **vs .NET CLR**: Superior speculative capabilities (T4), comparable native performance (T2-T3)

## Risk Analysis and Mitigation

### Technical Risks
1. **LLVM Integration Complexity**
   - Mitigation: Start with simple IR generation, gradually add features
   - Fallback: Implement custom code generator if LLVM proves problematic

2. **Speculation Overhead**
   - Mitigation: Conservative speculation budgets, aggressive deoptimization
   - Monitoring: Detailed speculation success/failure metrics

3. **Memory Management Integration**
   - Mitigation: Gradual integration with existing GC system
   - Testing: Extensive memory leak and performance testing

### Timeline Risks
1. **Scope Creep**
   - Mitigation: Focus on core execution first, defer advanced features
   - Process: Weekly milestone reviews with go/no-go decisions

2. **Integration Complexity**
   - Mitigation: Extensive integration testing at each milestone
   - Fallback: Maintain current VM as backup execution path

## Future Evolution Path

### Phase 4: Self-Hosting Migration (Post-Beta)
Once AOTT is stable and performant, migrate from Rust to Runa:

1. **Runtime Components**: Rewrite execution engines in Runa
2. **Compiler Integration**: Self-host the AOTT system
3. **Bootstrap Elimination**: Remove Rust dependencies entirely

### Phase 5: Advanced Features
- **GPU Acceleration**: Integrate with existing GPU backend
- **Distributed Execution**: Multi-node speculation and optimization
- **AI-Guided Optimization**: Machine learning for optimization decisions

## Conclusion

The AOTT system represents a fundamental upgrade to Runa's execution capabilities, replacing simple interpretation with a sophisticated tiered execution strategy. By implementing this system, Runa will achieve performance competitive with industry-leading language runtimes while maintaining the simplicity and AI-friendliness that defines the language.

The immediate focus should be on completing the execution engine implementations to unblock beta deployment for intern testing. The long-term vision of self-hosting and advanced features can be pursued once the core system proves its value in production use.

---

**Next Action**: Begin implementing the execution engine placeholders, starting with the bytecode execution system as the foundation for all higher optimization tiers.