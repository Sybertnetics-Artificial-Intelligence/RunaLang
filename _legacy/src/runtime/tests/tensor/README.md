# Tensor Runtime Test Suite

This directory contains comprehensive tests for Runa's Tensor Runtime System, validating all components from basic tensor operations to advanced automatic differentiation and GPU acceleration.

## Test Structure

### Integration Tests (`test_tensor_runtime_integration.runa`)

End-to-end tests that validate the entire tensor runtime system working together:

- **Basic Tensor Operations**: Creation, initialization, and basic arithmetic
- **Automatic Differentiation**: Gradient computation and backpropagation
- **Graph Optimization**: Computational graph fusion and optimization
- **Device Management**: Memory allocation, device placement, and cross-device transfers
- **Neural Network Operations**: Activation functions, convolution, and matrix operations
- **Performance Benchmarking**: Throughput and latency measurements

### Unit Tests (`test_tensor_operations.runa`)

Isolated tests for individual tensor operations with edge cases:

- **Tensor Creation & Initialization**: Different shapes, data types, and initialization patterns
- **Arithmetic Operations**: Add, subtract, multiply, divide with edge cases (division by zero)
- **Mathematical Operations**: Exponential, logarithm, trigonometric, square root, power
- **Reduction Operations**: Sum, mean, max, min along different axes
- **Matrix Operations**: Matrix multiplication, transpose, dot product
- **Activation Functions**: ReLU, Sigmoid, Tanh, GELU, Softmax

## Running Tests

### Run All Tests
```bash
# From the runa/src/runtime/tests/tensor directory
runa run run_tensor_tests.runa
```

### Run Unit Tests Only
```bash
runa run test_tensor_operations.runa
```

## Test Coverage

The test suite provides comprehensive coverage of:

### Core Functionality
- ✅ Tensor creation and memory management
- ✅ Basic arithmetic operations (+, -, *, /)
- ✅ Mathematical functions (exp, log, sin, cos, sqrt, pow)
- ✅ Reduction operations (sum, mean, max, min)
- ✅ Matrix operations (matmul, transpose, dot)

### Advanced Features
- ✅ Automatic differentiation and gradient computation
- ✅ Computational graph optimization and fusion
- ✅ Device placement and memory management
- ✅ Cross-device tensor transfers
- ✅ Neural network activation functions

### Performance & Reliability
- ✅ Memory leak detection
- ✅ Performance benchmarking
- ✅ Error handling and edge cases
- ✅ Numerical stability validation

## Test Results

Each test produces detailed results including:

- **Pass/Fail Status**: Clear indication of test outcome
- **Execution Time**: Performance metrics for each test
- **Memory Usage**: Memory consumption tracking
- **Error Messages**: Detailed failure descriptions
- **Performance Metrics**: Throughput, latency, and efficiency measurements

## Expected Output

When all tests pass, you should see:

```
=== Tensor Runtime Test Report ===

✓ basic_operations: PASSED (0.123s, 45 MB)
✓ autograd: PASSED (0.089s, 67 MB)
✓ graph_optimization: PASSED (0.234s, 123 MB)
✓ device_management: PASSED (0.156s, 89 MB)
✓ neural_network_operations: PASSED (0.078s, 34 MB)

Tests: 5/5 passed

🎉 All tensor runtime tests passed!

=== Performance Metrics ===
matrix_multiplication_benchmark: 1234.56 ops/sec, 0.810ms latency, 2.45 MB/op

✅ Tensor Runtime System: ALL TESTS PASSED
The tensor runtime is ready for production use!
```

## Dependencies

The tests depend on the following tensor runtime components:

- `tensor_runtime.runa` - Core tensor infrastructure
- `autograd_engine.runa` - Automatic differentiation
- `graph_optimizer.runa` - Computational graph optimization
- `device_manager.runa` - Device and memory management
- `tensor_compiler_integration.runa` - GPU compiler integration
- `tensor_ops.runa` - Tensor operations library

## Host Implementation Notes

The tests use FFI boundaries for performance-critical operations that are implemented in the host runtime (Rust). Key external functions include:

- `get_current_time()` - High-resolution timing
- `get_memory_usage()` - Memory consumption tracking

These functions must be implemented in the Rust host runtime for tests to execute correctly.

## Extending the Tests

To add new tests:

1. **Unit Tests**: Add new test functions to `test_tensor_operations.runa`
2. **Integration Tests**: Add new test scenarios to `test_tensor_runtime_integration.runa`
3. **Performance Tests**: Add new benchmarks to the performance benchmark section

Follow the existing pattern of:
- Try/catch error handling
- Detailed validation with tolerance checks
- Clear error messages
- Performance timing