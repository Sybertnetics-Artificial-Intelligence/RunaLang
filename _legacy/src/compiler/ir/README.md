# Runa Compiler: Intermediate Representation (IR) System

## Overview

The Runa IR system is a **multi-level intermediate representation** designed for a **multi-target language** that can generate code for high-level languages (Python, JavaScript) and low-level systems (WebAssembly, LLVM). This tiered approach allows for optimal code generation and optimization at each level of abstraction.

## Architecture Philosophy

### Multi-Level IR Design

The IR system consists of three distinct levels, each serving a specific purpose:

1. **High-Level IR (HIR)** - Close to AST, preserves Runa semantics
2. **Mid-Level IR (MIR)** - Control Flow Graph, optimization-friendly
3. **Low-Level IR (LIR)** - Machine-like, virtual registers, explicit memory operations

### Key Benefits

- **Gradual Lowering**: Each level progressively removes abstractions
- **Target Flexibility**: HIR for Python/JS, LIR for Wasm/LLVM
- **Optimization Opportunities**: Different optimizations at each level
- **Maintainability**: Clear separation of concerns

## Directory Structure

```
src/runa/compiler/ir/
├── ir.runa                 # Main IR module entry point
├── ir_context.runa         # Central compilation context
├── hir/                    # High-Level IR
│   ├── hir.runa           # HIR node definitions
│   └── builder.runa       # AST to HIR translator
├── mir/                    # Mid-Level IR
│   ├── mir.runa           # MIR structures (CFG, BasicBlocks)
│   ├── builder.runa       # HIR to MIR lowering
│   └── verifier.runa      # MIR validation and SSA checking
├── lir/                    # Low-Level IR
│   ├── lir.runa           # LIR structures (VirtualRegisters)
│   └── builder.runa       # MIR to LIR lowering
├── types/                  # Unified type system
│   ├── types.runa         # Canonical type representation
│   └── layout.runa        # Cross-platform memory layout
└── optimizations/          # Optimization passes and analysis
    ├── hir_passes/
    ├── mir_passes/
    ├── lir_passes/
    ├── analysis/           # Data flow, control flow, dependency analysis
    └── benchmarking/       # Performance benchmarking framework
```

## Design Refinements

### Type-Safe APIs

The IR system uses idiomatic Runa `Result` types instead of generic dictionaries:

```runa
Type HIRBuildResult is Success with module as HIRModule | Failure with diagnostics as List[IRDiagnostic]

Process called "translate_ast_to_hir" that takes ast as ASTNode and context as IRContext returns HIRBuildResult:
    Let result be build_hir_from_ast with ast as ast and context as context
    
    If result.success:
        Return Success with module as result.hir_module
    Otherwise:
        Return Failure with diagnostics as result.diagnostics
```

### Explicit Compilation Pipeline

The compiler driver makes the pipeline explicit and composable:

```runa
Process called "compile_source" that takes source as String and context as IRContext returns CompilationResult:
    Note: Stage 1: Lexical Analysis
    Let lexer be create_lexer with source as source
    Let tokenization_result be tokenize with lexer as lexer
    
    Note: Stage 2: Parsing
    Let parser be create_parser with tokens as tokenization_result.tokens
    Let parsing_result be parse_program with parser as parser
    
    Note: Stage 3: HIR Translation
    Let hir_result be translate_ast_to_hir with ast as parsing_result.ast and context as context
    
    Note: Continue through MIR, LIR, Optimization, Validation...
```

### Object-Oriented Context Management

The IRContext uses proper object-oriented design:

```runa
Type SymbolTable is Dictionary with:
    symbols as Dictionary[String, Symbol]
    current_scope as Integer
    metadata as Dictionary[String, Any]

Process called "add_symbol" that takes self as SymbolTable and symbol as Symbol:
    Set self.symbols at key symbol.name to symbol

Process called "lookup_symbol" that takes self as SymbolTable and name as String returns Optional[Symbol]:
    If name is in self.symbols:
        Return self.symbols at key name
    Otherwise:
        Return None
```

## Optimization Framework

### Analysis Framework

The IR system includes comprehensive analysis capabilities:

#### Data Flow Analysis
- **Reaching Definitions**: Tracks variable definitions that reach each program point
- **Live Variables**: Identifies variables that are live at each program point
- **Available Expressions**: Finds expressions that are available for reuse
- **Very Busy Expressions**: Identifies expressions that are computed on all paths

#### Control Flow Analysis
- **Dominance Analysis**: Computes dominance relationships between basic blocks
- **Loop Analysis**: Identifies and analyzes loops in the control flow graph
- **Critical Edge Analysis**: Finds critical edges that may need splitting

#### Dependency Tracking
- **Data Dependencies**: Tracks data dependencies between instructions
- **Control Dependencies**: Identifies control dependencies between blocks
- **Circular Dependency Detection**: Finds and reports circular dependencies

### Optimization Passes

#### HIR Level Optimizations
- **Function Inlining**: Inlines small functions to reduce call overhead
- **Loop Optimization**: Applies loop invariant code motion, unrolling, and strength reduction
- **Loop Vectorization**: Converts scalar operations to vector operations for SIMD optimization
- **Advanced Loop Optimizations**: Applies loop fusion, interchange, tiling, and distribution

#### MIR Level Optimizations
- **Constant Folding**: Evaluates constant expressions at compile time
- **Dead Code Elimination**: Removes unreachable and unused code
- **SSA Construction**: Converts to Static Single Assignment form

#### LIR Level Optimizations
- **Register Allocation**: Allocates virtual registers to physical registers

#### Advanced Optimization Frameworks
- **Profile-Guided Optimization**: Uses runtime profiles to guide optimization decisions
- **Interprocedural Analysis**: Analyzes and optimizes across function boundaries
- **Target-Specific Optimizations**: Platform-specific optimizations for x86, ARM, RISC-V

### Performance Benchmarking

The system includes a comprehensive benchmarking framework:

```runa
Process called "run_benchmark_suite" that takes benchmarker as PerformanceBenchmarker and suite_name as String returns Dictionary[String, Any]:
    Let suite be benchmarker.benchmark_suites at key suite_name
    Let results be list containing
    
    For each test in suite.benchmarks:
        Let result be run_single_benchmark with benchmarker as benchmarker and test as test
        Add result to results
    
    Return dictionary containing:
        "success" as true
        "results" as results
        "summary" as generate_benchmark_summary with results as results
```

## Optimization Levels

The system supports multiple optimization levels:

- **Level 0**: No optimizations (for debugging)
- **Level 1**: Basic optimizations (inlining, constant folding)
- **Level 2**: Standard optimizations (includes loop optimization, vectorization, advanced loop optimizations, register allocation)
- **Level 3**: Aggressive optimizations (includes profile-guided optimization, interprocedural analysis, target-specific optimizations)

## Usage Examples

### Basic IR Creation

```runa
Let context be create_ir_context with compilation_unit as "my_program" and source_file as "main.runa"
Let ir_module be create_ir_module_with_context with context as context

Note: Add content to the IR module
Let function be create_hir_function with name as "main" and parameters as list containing and body as list containing
Add function to ir_module.hir.declarations
```

### Running Optimizations

```runa
Let optimized_result be optimize_ir_module with ir_module as ir_module and context as context and optimization_level as 2

If optimized_result.success:
    Let optimized_module be optimized_result.optimized_module
    Let statistics be optimized_result.statistics
    Display "Optimizations applied: " plus statistics.total_optimizations
```

### Performance Benchmarking

```runa
Let benchmarker be create_performance_benchmarker with context as context
Let suite be create_standard_benchmarks with benchmarker as benchmarker
Let results be run_benchmark_suite with benchmarker as benchmarker and suite_name as "standard_optimization_benchmarks"

Display "Benchmark Results:"
Display "Total Time: " plus results.total_time_ms plus " ms"
Display "Total Memory: " plus results.total_memory_mb plus " MB"
```

## Testing

The IR system includes comprehensive test suites:

- **IR System Tests**: Test creation and basic operations of IR components
- **Optimization Tests**: Test all optimization passes and the pipeline
- **Analysis Tests**: Test data flow, control flow, and dependency analysis
- **Benchmark Tests**: Test performance benchmarking framework

Run tests with:

```runa
Let ir_results be test_ir_system
Let optimization_results be test_optimization_system

Display "IR System Tests: " plus ir_results.summary.success_rate plus "%"
Display "Optimization Tests: " plus optimization_results.summary.success_rate plus "%"
```

## Future Enhancements

- **Advanced Loop Optimizations**: Vectorization, loop fusion, loop interchange
- **Interprocedural Analysis**: Cross-function optimization opportunities
- **Profile-Guided Optimization**: Use runtime profiles to guide optimizations
- **Target-Specific Optimizations**: Platform-specific optimizations for different backends 