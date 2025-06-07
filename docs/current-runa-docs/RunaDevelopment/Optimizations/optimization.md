# Runa Optimization Guide

This guide explains the optimization capabilities in Runa, how they work, and how to use them effectively.

## Optimization Levels

Runa supports multiple optimization levels that can be specified when compiling or running code:

- **Level 0** (`--optimize 0`): No optimizations are applied. This is useful for debugging as the generated code will directly correspond to your source code.
- **Level 1** (`--optimize 1`): Basic optimizations are applied, including constant folding and dead code elimination.
- **Level 2** (`--optimize 2`): Aggressive optimizations are applied, including all basic optimizations plus loop optimization and multiple optimization passes.

You can specify the optimization level using the `--optimize` flag in the CLI:

```bash
runa compile --optimize 2 my_program.runa
runa run --optimize 1 my_program.runa
```

## Optimization Techniques

### Constant Folding

Constant folding is an optimization that evaluates constant expressions at compile time rather than runtime.

#### Example

**Before optimization:**
```
Let result = 10 * 20 + 5
```

**After optimization:**
```
Let result = 205
```

This optimization applies to:
- Arithmetic operations (+, -, *, /, %)
- Logical operations (and, or, not)
- Comparison operations (==, !=, <, >, <=, >=)
- String concatenation

### Dead Code Elimination

Dead code elimination removes code that has no effect on the program's output.

#### Example

**Before optimization:**
```
Let x = 10
If true Then
    Display "This will always execute"
Else
    Display "This will never execute"
End If
```

**After optimization:**
```
Let x = 10
Display "This will always execute"
```

This optimization removes:
- Unreachable code after return statements
- Unused variable declarations
- Conditional branches that will never execute
- Empty blocks

### Loop Optimization

Loop optimization improves the performance of loops by:

1. **Loop Invariant Code Motion**: Moving code that doesn't change inside the loop to outside the loop
2. **Loop Unrolling**: Expanding small loops to reduce overhead
3. **Loop Fusion**: Combining adjacent loops with same boundaries

#### Example

**Before optimization:**
```
Let sum = 0
Let i = 0
While i < 10 Do
    Let x = 20 * 5  # This calculation never changes
    sum = sum + x
    i = i + 1
End While
```

**After optimization:**
```
Let sum = 0
Let i = 0
Let x = 20 * 5  # Moved outside the loop
While i < 10 Do
    sum = sum + x
    i = i + 1
End While
```

## Benchmark Results

Runa includes benchmarking tools that demonstrate the impact of optimizations. The `optimization_benchmark.py` script in the `benchmarks` directory can be used to compare the performance of different optimization levels.

Typical results show:
- Level 1 optimizations provide 10-30% performance improvements over unoptimized code
- Level 2 optimizations can achieve 20-50% improvements on loop-heavy code

## Best Practices

1. **Development vs. Production**:
   - Use `--optimize 0` during development for easier debugging
   - Use `--optimize 2` for production deployments

2. **When to Avoid High Optimization Levels**:
   - If you need precise debugging information
   - If your code relies on specific evaluation order that might be altered by optimizations

3. **Program Structure for Better Optimization**:
   - Extract complex calculations from loops when possible
   - Use constants instead of repeated calculations
   - Break large functions into smaller ones to improve inlining opportunities

## Implementation Details

The optimization process in Runa works on the Abstract Syntax Tree (AST) representation of your program:

1. The AST is generated from your source code by the parser
2. Optimizers traverse and transform the AST based on the optimization level
3. The optimized AST is then used for code generation

The main optimizers are implemented in the `runa.optimization` module:
- `ConstantFolder`: Evaluates constant expressions
- `DeadCodeEliminator`: Removes unused or unreachable code
- `LoopOptimizer`: Optimizes loop structures

## Creating Custom Optimizations

Advanced users can create custom optimizations by extending the `Visitor` class from `runa.ast.visitors` and implementing the appropriate visit methods. See the [Contributing Guide](contributing.md) for more details.

## Performance Profiling

To identify which optimizations would be most beneficial for your code, you can use Runa's built-in profiler:

```bash
runa profile my_program.runa
```

This will generate a performance report that can help you identify bottlenecks and potential optimization opportunities. 