# Runa Compiler Optimizations: In-depth Guide

This document provides a detailed explanation of the optimization system in the Runa compiler, including its architecture, individual optimizations, and how to extend it with new optimizations.

## Table of Contents
- [Optimization Architecture](#optimization-architecture)
- [Optimization Levels](#optimization-levels)
- [Optimization Implementations](#optimization-implementations)
  - [Constant Folding](#constant-folding)
  - [Dead Code Elimination](#dead-code-elimination)
  - [Loop Optimization](#loop-optimization)
- [Error Handling](#error-handling)
- [Testing Optimizations](#testing-optimizations)
- [Cross-Platform Compatibility](#cross-platform-compatibility)
- [Adding New Optimizations](#adding-new-optimizations)
- [Benchmarking and Performance](#benchmarking-and-performance)

## Optimization Architecture

The Runa optimization system is designed as a pipeline of AST transformations. Each optimization is implemented as a visitor pattern that traverses the AST and applies transformations to eligible nodes.

The main components are:

1. **Optimization Module (`src/runa/optimization/`)**: The central module that coordinates all optimizations.
2. **Individual Optimizations**: Each optimization is implemented as a separate class in its own file.
3. **Error Handling System**: A robust error handling system that gracefully handles errors during optimization.
4. **Integration with Transpiler**: The optimization pipeline is integrated with the Runa transpiler.

The optimization process follows these steps:

1. Parse Runa source code into an AST
2. Apply semantic analysis to ensure the code is valid
3. Apply optimizations to the AST based on the selected optimization level
4. Generate target code from the optimized AST

## Optimization Levels

Runa provides three optimization levels:

- **Level 0 (None)**: No optimizations are applied. This is useful for debugging or when you want to ensure the code is transpiled exactly as written.
- **Level 1 (Basic)**: Basic optimizations are applied, including constant folding and dead code elimination. These optimizations are generally safe and don't significantly change the structure of the code.
- **Level 2 (Aggressive)**: All basic optimizations plus more aggressive optimizations like loop optimization. These optimizations can significantly restructure the code for better performance.

You can set the optimization level when compiling or running Runa code using the `--optimize` flag:

```bash
runa compile --optimize 2 myfile.runa
runa run --optimize 1 myfile.runa
```

Or when using the API:

```python
from runa.transpiler import Transpiler

transpiler = Transpiler(optimization_level=2)
```

## Optimization Implementations

### Constant Folding

**Location**: `src/runa/optimization/constant_folding.py`

Constant folding evaluates constant expressions at compile time rather than at runtime. This reduces the number of operations performed at runtime and can lead to more efficient code.

#### Features:

- Evaluates arithmetic operations on number literals (`+`, `-`, `*`, `/`, `%`)
- Evaluates string concatenation (`+`)
- Evaluates boolean operations (`and`, `or`, `not`)
- Evaluates comparison operations (`==`, `!=`, `<`, `<=`, `>`, `>=`)
- Handles edge cases like division by zero safely
- Implements short-circuit evaluation for boolean operations
- Handles mixed-type operations (e.g., string + number)

#### Example:

```runa
// Before optimization
let x = 3 * 4 + 2;

// After optimization
let x = 14;
```

#### Edge Cases:

The constant folder handles several edge cases gracefully:

- Division by zero is detected and not folded
- Modulo by zero is detected and not folded
- Circular references are detected with a maximum iteration limit
- Errors during folding are caught and logged as warnings

### Dead Code Elimination

**Location**: `src/runa/optimization/dead_code.py`

Dead code elimination removes code that will never be executed or has no effect on the program. This reduces code size and can improve performance.

#### Features:

- Removes unreachable code after return statements
- Eliminates unused variable declarations
- Removes branches with constant conditions (if/else with constant condition)
- Eliminates redundant assignments (variables assigned but never used)

#### Example:

```runa
// Before optimization
function example(): int {
    let x = 5;
    let y = 10;  // Unused
    return x;
    let z = 15;  // Unreachable
}

// After optimization
function example(): int {
    let x = 5;
    return x;
}
```

### Loop Optimization

**Location**: `src/runa/optimization/loop_optimization.py`

Loop optimization improves the performance of loops by applying various transformations that reduce the overhead of loops or move invariant code outside loops.

#### Features:

- **Loop Invariant Code Motion (LICM)**: Moves expressions that don't change during loop execution outside the loop
- **Loop Fusion**: Combines adjacent loops with the same iteration structure to reduce loop overhead
- **Loop Metadata Annotation**: Adds metadata to loops that could benefit from unrolling

#### Example:

```runa
// Before optimization (Loop Invariant Code Motion)
for (let i = 0; i < n; i = i + 1) {
    let invariant = 5 * 10;
    result = result + invariant;
}

// After optimization
let invariant = 5 * 10;
for (let i = 0; i < n; i = i + 1) {
    result = result + invariant;
}
```

```runa
// Before optimization (Loop Fusion)
for (let i = 0; i < n; i = i + 1) {
    a[i] = a[i] * 2;
}
for (let i = 0; i < n; i = i + 1) {
    b[i] = b[i] + 1;
}

// After optimization
for (let i = 0; i < n; i = i + 1) {
    a[i] = a[i] * 2;
    b[i] = b[i] + 1;
}
```

## Error Handling

**Location**: `src/runa/optimization/errors.py`

The optimization system includes a robust error handling system that gracefully handles errors during optimization. This ensures that even if an optimization fails, the compilation process can continue with a meaningful error message.

### Components:

- **OptimizationError**: Base class for all optimization-related errors
- **ConstantFoldingError**: Error specific to constant folding
- **DeadCodeEliminationError**: Error specific to dead code elimination
- **LoopOptimizationError**: Error specific to loop optimization
- **OptimizationWarning**: Warning generated during optimization
- **OptimizationLogger**: Logger for optimization activities, warnings, and errors
- **optimization_try_catch** decorator: Wraps optimization functions to catch and handle errors

### Usage:

```python
from runa.optimization.errors import OptimizationWarning, optimization_try_catch

@optimization_try_catch
def some_optimization_function(ast):
    # Optimization logic...
    
    if risky_condition:
        warning = OptimizationWarning(
            "Risky operation detected",
            "my_optimization",
            node.position
        )
        warnings.append(warning)
```

## Testing Optimizations

The Runa project includes several testing approaches for optimizations:

### Unit Tests

**Location**: `tests/optimization/`

Unit tests for individual optimizations verify that each optimization works correctly in isolation.

### Integration Tests

**Location**: `tests/integration/test_optimization_integration.py`

Integration tests verify that all optimizations work together correctly on real-world code examples.

### Cross-Platform Tests

**Location**: `tools/cross_platform_tester.py`

Cross-platform tests ensure that optimizations produce the same results across different platforms (e.g., Windows, Linux, macOS).

### Running Tests:

```bash
# Run all tests
python -m unittest discover

# Run specific test
python -m unittest tests.optimization.test_constant_folding
```

## Cross-Platform Compatibility

The Runa optimization system is designed to be cross-platform compatible. The `tools/cross_platform_tester.py` tool helps verify that optimizations produce the same results across different platforms.

### Usage:

```bash
# Run tests on current platform
python tools/cross_platform_tester.py test examples/*.runa --output-dir results

# Compare results from different platforms
python tools/cross_platform_tester.py compare results/results_Windows.json results/results_Linux.json
```

## Adding New Optimizations

To add a new optimization to the Runa compiler, follow these steps:

1. Create a new file in `src/runa/optimization/` for your optimization
2. Implement your optimization as a visitor that extends the `Visitor` class
3. Add an `optimize` method that applies your optimization to an AST
4. Update the `__init__.py` file to import and expose your optimization
5. Add the optimization to the appropriate optimization level in `optimize_ast`
6. Write unit tests for your optimization
7. Update the documentation to describe your optimization

### Example:

```python
from runa.ast.visitors import Visitor
from .errors import OptimizationError, OptimizationWarning, optimization_try_catch

class MyNewOptimization(Visitor):
    def __init__(self):
        super().__init__()
        self.optimizations_applied = 0
        self.warnings = []
    
    @optimization_try_catch
    def optimize(self, ast):
        # Apply optimization to AST
        result = self.visit(ast)
        return result
    
    # Visitor methods for each node type...
```

Then update `__init__.py`:

```python
from .my_new_optimization import MyNewOptimization

# In optimize_ast function:
if level >= OPTIMIZATION_LEVEL_BASIC:
    # Add your optimization at the appropriate level
    my_optimizer = MyNewOptimization()
    ast = my_optimizer.optimize(ast)
    logger.optimization_counts["my_new_optimization"] = my_optimizer.optimizations_applied
```

## Benchmarking and Performance

The Runa project includes tools for benchmarking optimization performance:

### Optimization Benchmark

**Location**: `benchmarks/optimization_benchmark.py`

This tool benchmarks the performance of Runa optimizations on various code samples. It measures compile time, runtime, and overall execution time with different optimization levels.

### Optimization Visualization Tool

**Location**: `tools/optimize_code.py`

This tool demonstrates the effect of optimizations on Runa code by showing the differences between optimized and unoptimized code.

### Usage:

```bash
# Run optimization benchmark
python -m benchmarks.optimization_benchmark

# Visualize optimization effects
python tools/optimize_code.py examples/optimization_demo.runa --level 2
```

## Conclusion

The Runa optimization system provides a powerful framework for improving the performance of Runa programs. By using the appropriate optimization level and understanding the available optimizations, you can significantly enhance the efficiency of your Runa code while maintaining correctness. 