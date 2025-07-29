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
└── optimizations/          # Optimization passes (future)
    ├── hir_passes/
    ├── mir_passes/
    └── lir_passes/
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

### Functional Optimization Passes

Optimization passes follow a functional design pattern:

```runa
Type OptimizationPassResult[T] is Success with module as T and statistics as Dictionary[String, Any] | Failure with diagnostics as List[IRDiagnostic]

Process called "chain_passes" that takes passes as List[Pass[T]] and module as T and context as IRContext returns OptimizationPassResult[T]:
    Let current_module be module
    
    For each pass in passes:
        Let result be run_pass with pass as pass and module as current_module and context as context
        Match result:
            When Success with module as new_module and statistics as statistics:
                Set current_module to new_module
            When Failure with diagnostics as diagnostics:
                Return Failure with diagnostics as diagnostics
    
    Return Success with module as current_module and statistics as total_statistics
```

## IR Levels in Detail

### High-Level IR (HIR)

**Purpose**: Preserves Runa semantics with explicit scopes and resolved names.

**Key Features**:
- **Explicit Scopes**: Unlike AST, HIR has explicit scope nodes
- **Resolved Names**: All identifiers point to canonical declarations
- **Type Annotations**: Every expression has inferred types
- **Semantic Analysis**: Performs type checking and name resolution

**Example HIR**:
```runa
HIRProcessDeclaration with:
    name as "add"
    parameters as [HIRParameter with name as "a", type as Integer]
    return_type as Integer
    body as [HIRReturnStatement with value as HIRBinaryOperation with left as "a", operator as "plus", right as "b"]
```

### Mid-Level IR (MIR)

**Purpose**: Control Flow Graph representation for optimization.

**Key Features**:
- **Basic Blocks**: Linear sequences of instructions
- **Control Flow Graph**: Explicit predecessor/successor relationships
- **SSA Form**: Static Single Assignment for optimization
- **Type Safety**: Maintains type information throughout

**Example MIR**:
```runa
MIRFunction with:
    name as "add"
    basic_blocks as [
        MIRBasicBlock with:
            name as "entry"
            instructions as [
                MIRBinaryOp with destination as "%0", left as "a", operator as "plus", right as "b"
            ]
            terminator as MIRReturnTerminator with value as "%0"
    ]
```

### Low-Level IR (LIR)

**Purpose**: Machine-like representation with virtual registers.

**Key Features**:
- **Virtual Registers**: Explicit register allocation
- **Memory Operations**: Explicit load/store instructions
- **Immediate Values**: Direct constant handling
- **Platform Independence**: Machine-like but target-agnostic

**Example LIR**:
```runa
LIRFunction with:
    name as "add"
    basic_blocks as [
        LIRBasicBlock with:
            name as "entry"
            instructions as [
                LIRBinaryOp with destination as VirtualRegister with name as "%0", left as VirtualRegister with name as "%a", operator as "plus", right as VirtualRegister with name as "%b"
            ]
            terminator as LIRReturnTerminator with value as VirtualRegister with name as "%0"
    ]
```

## Type System

### Unified Type Representation

The IR uses a **canonical type system** that's consistent across all levels:

```runa
Type IRType is:
    | IRPrimitiveType with name as String and size as Integer and alignment as Integer
    | IRPointerType with pointee as IRType and is_mutable as Boolean
    | IRArrayType with element_type as IRType and length as Optional[Integer]
    | IRStructType with name as String and fields as List[IRField] and size as Integer and alignment as Integer
    | IRUnionType with name as String and variants as List[IRVariant] and size as Integer and alignment as Integer
    | IRFunctionType with parameters as List[IRType] and return_type as IRType and is_variadic as Boolean
    | IRGenericType with name as String and type_parameters as List[String] and constraints as List[IRTypeConstraint]
    | IRTypeParameter with name as String and constraint as Optional[IRType]
    | IRInferredType with placeholder as String
    | IRUnknownType
```

### Cross-Platform Layout

The layout system calculates memory sizes and alignments for different platforms:

```runa
Process called "calculate_layout" that takes type_system as TypeSystem and ir_type as IRType and strategy as LayoutStrategy returns LayoutInfo:
    Note: Calculate memory layout for a type
    Match ir_type:
        When IRPrimitiveType with name as name and size as size and alignment as alignment:
            Return LayoutInfo with size as size and alignment as alignment
        When IRStructType with name as name and fields as fields and size as size and alignment as alignment:
            Return calculate_struct_layout with type_system as type_system and fields as fields and strategy as strategy
        Otherwise:
            Return default_layout
```

## Usage Examples

### Creating an IR Module

```runa
Let context be create_ir_context with compilation_unit as "main" and source_file as "main.runa"
Let ir_module be create_ir_module
```

### AST to HIR Translation

```runa
Let ast_node be parse_runa_code with code as "Let x be 42"
Let hir_result be build_hir_from_ast with ast as ast_node and context as context
If hir_result.success:
    Let hir_module be hir_result.hir_module
```

### HIR to MIR Lowering

```runa
Let mir_result be build_mir_from_hir with hir_module as hir_module and context as context
If mir_result.success:
    Let mir_module be mir_result.mir_module
```

### MIR to LIR Lowering

```runa
Let lir_result be build_lir_from_mir with mir_module as mir_module and context as context
If lir_result.success:
    Let lir_module be lir_result.lir_module
```

### IR Validation

```runa
Let mir_validation be validate_mir with mir_module as mir_module
If mir_validation.valid:
    Display "MIR is valid"
Otherwise:
    Display "MIR validation errors: " plus mir_validation.errors
```

## Optimization Framework

### Implemented Optimization Passes

**HIR Optimizations**:
- ✅ **Function Inlining** (`hir_passes/inlining.runa`) - Inlines small functions to reduce call overhead
- 🔄 Constant propagation (planned)
- 🔄 Dead code elimination (planned)

**MIR Optimizations**:
- ✅ **Constant Folding** (`mir_passes/constant_folding.runa`) - Evaluates constant expressions at compile time
- ✅ **Dead Code Elimination** (`mir_passes/dead_code_elimination.runa`) - Removes unreachable code and unused variables
- ✅ **SSA Construction** (`mir_passes/ssa.runa`) - Converts MIR to Static Single Assignment form
- 🔄 Loop optimizations (planned)
- 🔄 Register allocation preparation (planned)

**LIR Optimizations**:
- ✅ **Register Allocation** (`lir_passes/register_allocation.runa`) - Maps virtual registers to physical registers
- 🔄 Instruction scheduling (planned)
- 🔄 Peephole optimizations (planned)

### Optimization Pipeline

The optimization pipeline (`optimizations/optimization_pipeline.runa`) orchestrates all passes:

```runa
Process called "optimize_ir_module" that takes ir_module as IRModule and context as IRContext and optimization_level as Integer returns Dictionary[String, Any]:
    Note: Apply optimizations to an IR module
    
    Let type_system be create_type_system
    Let pipeline be create_optimization_pipeline with context as context and type_system as type_system
    Set pipeline.optimization_level to optimization_level
    
    Let optimized_module be copy_ir_module with module as ir_module
    Let total_optimizations be 0
    
    Note: Configure optimization level
    Let enabled_passes be get_enabled_passes_for_level with level as optimization_level
    Set pipeline.enabled_passes to enabled_passes
    
    Note: Apply HIR optimizations
    If "hir_inlining" is in enabled_passes:
        Let hir_result be optimize_hir_with_inlining with hir_module as optimized_module.hir and context as context
        If hir_result.success:
            Set optimized_module.hir to hir_result.optimized_module
            Set pipeline.pass_statistics at key "hir_inlining" to hir_result.statistics
            Set total_optimizations to total_optimizations plus 1
    
    Note: Apply MIR optimizations
    If "mir_constant_folding" is in enabled_passes:
        Let mir_result be optimize_mir_with_constant_folding with mir_module as optimized_module.mir and context as context
        If mir_result.success:
            Set optimized_module.mir to mir_result.optimized_module
            Set pipeline.pass_statistics at key "mir_constant_folding" to mir_result.statistics
            Set total_optimizations to total_optimizations plus 1
    
    Note: Apply LIR optimizations
    If "lir_register_allocation" is in enabled_passes:
        Let lir_result be allocate_registers with lir_module as optimized_module.lir and context as context
        If lir_result.success:
            Set optimized_module.lir to lir_result.optimized_module
            Set pipeline.pass_statistics at key "lir_register_allocation" to lir_result.statistics
            Set total_optimizations to total_optimizations plus 1
    
    Return dictionary containing:
        "success" as true
        "optimized_module" as optimized_module
        "statistics" as dictionary containing:
            "total_optimizations" as total_optimizations
            "pass_statistics" as pipeline.pass_statistics
            "optimization_level" as optimization_level
```

### Optimization Levels

- **Level 0**: No optimizations
- **Level 1**: Basic optimizations (inlining, constant folding)
- **Level 2**: Standard optimizations (includes dead code elimination, register allocation)
- **Level 3**: Aggressive optimizations (includes SSA construction, advanced passes)

### Usage Examples

```runa
Let context be create_ir_context with compilation_unit as "main" and source_file as "main.runa"
Let ir_module be create_ir_module

Note: Apply optimizations
Let optimization_result be optimize_ir_module with ir_module as ir_module and context as context and optimization_level as 2
If optimization_result.success:
    Let optimized_module be optimization_result.optimized_module
    Let statistics be optimization_result.statistics
    Display "Applied " plus statistics.total_optimizations plus " optimizations"
```

## Testing

### Running IR Tests

```runa
Let test_results be test_ir_system
Let summary be test_results at key "summary"
Display "IR Tests: " plus summary.passed_tests plus "/" plus summary.total_tests plus " passed"
```

### Test Coverage

The IR system includes comprehensive tests for:
- Module creation and initialization
- Type system functionality
- HIR/MIR/LIR creation and manipulation
- IR transformations between levels
- Validation and error handling

## Performance Considerations

### Memory Efficiency

- **Shared Type System**: Types are shared across all IR levels
- **Lazy Evaluation**: IR nodes are created only when needed
- **Context Reuse**: IR context is reused across transformations

### Optimization Opportunities

- **Early Optimization**: HIR-level optimizations reduce work for later stages
- **Target-Specific**: Different optimization strategies for different targets
- **Incremental**: Optimizations can be applied incrementally

## Future Enhancements

### Planned Features

1. **Advanced Optimizations**:
   - Loop vectorization
   - Function specialization
   - Inter-procedural optimizations

2. **Target-Specific IRs**:
   - Python-specific HIR extensions
   - WebAssembly-specific LIR extensions
   - LLVM IR compatibility

3. **Debugging Support**:
   - Source mapping between IR levels
   - Debug information preservation
   - IR visualization tools

4. **Parallel Processing**:
   - Concurrent IR transformations
   - Parallel optimization passes
   - Multi-threaded code generation

## Contributing

When contributing to the IR system:

1. **Maintain Level Separation**: Keep HIR, MIR, and LIR concerns separate
2. **Preserve Type Safety**: Ensure type information flows correctly
3. **Add Tests**: Include tests for new functionality
4. **Update Documentation**: Keep this README current
5. **Follow Patterns**: Use existing patterns for consistency

## Conclusion

The Runa IR system provides a robust foundation for multi-target compilation with clear separation of concerns, comprehensive type safety, and extensive optimization opportunities. Its tiered architecture enables efficient code generation for diverse target platforms while maintaining the high-level semantics of the Runa language. 