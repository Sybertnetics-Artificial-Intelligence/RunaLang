# Core Linear Algebra Operations

The Core Linear Algebra module (`math/engine/linalg/core`) provides the fundamental infrastructure for high-performance matrix and vector operations. This module serves as the foundation for all linear algebra computations in Runa, implementing optimized algorithms with BLAS/LAPACK integration for maximum performance.

## Quick Start

```runa
Import "math/engine/linalg/core" as LinAlg

Note: Create and manipulate matrices
Let matrix_a be LinAlg.create_matrix([
    [1.0, 2.0, 3.0],
    [4.0, 5.0, 6.0],
    [7.0, 8.0, 9.0]
])

Let matrix_b be LinAlg.create_matrix([
    [9.0, 8.0, 7.0],
    [6.0, 5.0, 4.0],
    [3.0, 2.0, 1.0]
])

Note: Basic matrix operations
Let matrix_sum be LinAlg.matrix_add(matrix_a, matrix_b)
Let matrix_product be LinAlg.matrix_multiply(matrix_a, matrix_b)
Let matrix_transpose be LinAlg.transpose(matrix_a)

Display "Matrix sum:" joined with LinAlg.matrix_to_string(matrix_sum)
Display "Matrix product:" joined with LinAlg.matrix_to_string(matrix_product)

Note: Vector operations
Let vector_x be LinAlg.create_vector([1.0, 2.0, 3.0])
Let vector_y be LinAlg.create_vector([4.0, 5.0, 6.0])

Let dot_product be LinAlg.dot_product(vector_x, vector_y)
Let vector_norm be LinAlg.vector_norm(vector_x, "euclidean")
Let normalized_vector be LinAlg.normalize(vector_x)

Display "Dot product: " joined with dot_product
Display "Vector norm: " joined with vector_norm
```

## Core Matrix Operations

### Matrix Creation and Manipulation

```runa
Note: Different matrix creation methods
Let zero_matrix be LinAlg.create_zero_matrix(3, 3)
Let identity_matrix be LinAlg.create_identity_matrix(4)
Let random_matrix be LinAlg.create_random_matrix(5, 5, "uniform", 0.0, 1.0)
Let diagonal_matrix be LinAlg.create_diagonal_matrix([1.0, 2.0, 3.0, 4.0])

Note: Matrix from data
Let data_matrix be LinAlg.create_matrix_from_data(csv_data, "row_major")
Let sparse_matrix be LinAlg.create_sparse_matrix(row_indices, col_indices, values)

Note: Matrix properties
Let rows be LinAlg.get_row_count(matrix_a)
Let cols be LinAlg.get_column_count(matrix_a)
Let is_square be LinAlg.is_square_matrix(matrix_a)
Let is_symmetric be LinAlg.is_symmetric(matrix_a)
Let rank be LinAlg.matrix_rank(matrix_a)

Display "Matrix dimensions: " joined with rows joined with "x" joined with cols
Display "Matrix rank: " joined with rank
```

### Advanced Matrix Operations

```runa
Note: Matrix arithmetic
Let scaled_matrix be LinAlg.matrix_scalar_multiply(matrix_a, 2.5)
Let matrix_difference be LinAlg.matrix_subtract(matrix_a, matrix_b)
Let element_wise_product be LinAlg.hadamard_product(matrix_a, matrix_b)

Note: Matrix transformations
Let matrix_inverse be LinAlg.matrix_inverse(matrix_a)
Let matrix_power be LinAlg.matrix_power(matrix_a, 3)
Let matrix_exponential be LinAlg.matrix_exponential(matrix_a)
Let matrix_logarithm be LinAlg.matrix_logarithm(matrix_a)

Note: Matrix norms and metrics
Let frobenius_norm be LinAlg.matrix_norm(matrix_a, "frobenius")
Let spectral_norm be LinAlg.matrix_norm(matrix_a, "spectral")
Let condition_number be LinAlg.condition_number(matrix_a)
Let determinant be LinAlg.determinant(matrix_a)
Let trace be LinAlg.trace(matrix_a)

Display "Determinant: " joined with determinant
Display "Condition number: " joined with condition_number
```

## Vector Operations

### Basic Vector Arithmetic

```runa
Note: Vector creation and basic operations
Let unit_vector_x be LinAlg.create_unit_vector(3, 0)  Note: [1, 0, 0]
Let random_vector be LinAlg.create_random_vector(5, "normal", 0.0, 1.0)

Let vector_sum be LinAlg.vector_add(vector_x, vector_y)
Let vector_difference be LinAlg.vector_subtract(vector_x, vector_y)
Let scaled_vector be LinAlg.vector_scalar_multiply(vector_x, 3.0)

Note: Vector products
Let dot_result be LinAlg.dot_product(vector_x, vector_y)
Let cross_product be LinAlg.cross_product(vector_x, vector_y)  Note: 3D vectors only
Let outer_product be LinAlg.outer_product(vector_x, vector_y)

Display "Cross product: " joined with LinAlg.vector_to_string(cross_product)
```

### Vector Norms and Metrics

```runa
Note: Different vector norms
Let l1_norm be LinAlg.vector_norm(vector_x, "l1")
Let l2_norm be LinAlg.vector_norm(vector_x, "l2")
Let linf_norm be LinAlg.vector_norm(vector_x, "infinity")
Let p_norm be LinAlg.vector_norm(vector_x, "p", 2.5)

Note: Vector distances and angles
Let euclidean_distance be LinAlg.vector_distance(vector_x, vector_y, "euclidean")
Let manhattan_distance be LinAlg.vector_distance(vector_x, vector_y, "manhattan")
Let cosine_similarity be LinAlg.cosine_similarity(vector_x, vector_y)
Let angle_between be LinAlg.angle_between_vectors(vector_x, vector_y)

Display "Angle between vectors: " joined with angle_between joined with " radians"
```

## Memory Management and Performance

### Efficient Memory Operations

```runa
Note: Memory-efficient operations
LinAlg.set_memory_pool_size(1024 * 1024 * 512)  Note: 512MB pool
LinAlg.enable_memory_mapping(True)

Note: In-place operations for large matrices
LinAlg.matrix_add_inplace(matrix_a, matrix_b)  Note: matrix_a += matrix_b
LinAlg.matrix_multiply_inplace(matrix_a, matrix_b)  Note: matrix_a *= matrix_b
LinAlg.transpose_inplace(matrix_a)

Note: Memory usage monitoring
Let memory_usage be LinAlg.get_memory_usage()
Display "Current memory usage: " joined with memory_usage joined with " bytes"
```

### Performance Optimization

```runa
Note: Configure performance settings
LinAlg.set_thread_count(8)
LinAlg.set_block_size(256)  Note: Optimize for L2 cache
LinAlg.enable_vectorization(True)
LinAlg.set_numerical_precision("double")

Note: BLAS/LAPACK configuration
LinAlg.set_blas_library("openblas")
LinAlg.optimize_for_cpu_architecture("avx2")
LinAlg.enable_gpu_acceleration(True, "cuda")

Note: Performance profiling
Let start_time be LinAlg.get_current_time()
Let result be LinAlg.matrix_multiply(large_matrix_1, large_matrix_2)
Let end_time be LinAlg.get_current_time()
Let execution_time be LinAlg.time_difference(start_time, end_time)

Display "Matrix multiplication time: " joined with execution_time joined with "ms"
```

## Advanced Matrix Types

### Specialized Matrix Formats

```runa
Note: Different matrix storage formats
Let symmetric_matrix be LinAlg.create_symmetric_matrix(symmetric_data)
Let triangular_matrix be LinAlg.create_triangular_matrix(triangular_data, "upper")
Let banded_matrix be LinAlg.create_banded_matrix(diagonal_data, lower_bands, upper_bands)

Note: Complex matrices
Let complex_matrix be LinAlg.create_complex_matrix(real_part, imaginary_part)
Let conjugate_matrix be LinAlg.conjugate_transpose(complex_matrix)
Let hermitian_matrix be LinAlg.create_hermitian_matrix(hermitian_data)

Note: Matrix conversions
Let dense_from_sparse be LinAlg.sparse_to_dense(sparse_matrix)
Let sparse_from_dense be LinAlg.dense_to_sparse(dense_matrix, tolerance)
Let compressed_matrix be LinAlg.compress_matrix(matrix_a, "lz4")
```

### Matrix Views and Slicing

```runa
Note: Matrix slicing and views
Let submatrix be LinAlg.get_submatrix(matrix_a, 1, 3, 0, 2)  Note: rows 1-2, cols 0-1
Let matrix_row be LinAlg.get_row(matrix_a, 1)
Let matrix_column be LinAlg.get_column(matrix_a, 2)
Let diagonal_elements be LinAlg.get_diagonal(matrix_a)

Note: Matrix blocks and partitioning
Let block_11 be LinAlg.get_block(matrix_a, 0, 2, 0, 2)
Let block_12 be LinAlg.get_block(matrix_a, 0, 2, 2, 4)
Let partitioned_matrix be LinAlg.partition_matrix(matrix_a, [2, 2], [2, 2])

Note: Modify matrix views
LinAlg.set_submatrix(matrix_a, submatrix, 1, 3, 0, 2)
LinAlg.set_row(matrix_a, new_row_data, 1)
LinAlg.set_column(matrix_a, new_col_data, 2)
```

## Numerical Stability and Error Handling

### Condition Analysis

```runa
Import "core/error_handling" as ErrorHandling

Note: Numerical stability checks
Let condition_num be LinAlg.condition_number(matrix_a)
Let is_well_conditioned be LinAlg.is_well_conditioned(matrix_a, 1e10)
Let numerical_rank be LinAlg.numerical_rank(matrix_a, 1e-12)

If condition_num > 1e12:
    Display "Warning: Matrix is ill-conditioned (condition number: " joined with condition_num joined with ")"
    Let regularized be LinAlg.add_regularization(matrix_a, 1e-8)
    Display "Applied regularization to improve conditioning"
```

### Error Recovery

```runa
Note: Safe operations with error handling
Let safe_inverse be LinAlg.safe_matrix_inverse(potentially_singular)

If ErrorHandling.is_error(safe_inverse):
    Let error_type be ErrorHandling.get_error_type(safe_inverse)
    
    If ErrorHandling.is_singular_matrix(error_type):
        Display "Matrix is singular - computing pseudoinverse"
        Let pseudo_inv be LinAlg.pseudoinverse(potentially_singular)
    
    Otherwise If ErrorHandling.is_numerical_instability(error_type):
        Display "Numerical instability detected - using iterative refinement"
        Let refined_inverse be LinAlg.iteratively_refined_inverse(potentially_singular)
    
    Otherwise:
        Display "Linear algebra error: " joined with ErrorHandling.get_error_message(safe_inverse)
```

## Integration with Other Modules

### Mathematical Functions Integration

```runa
Import "math/core/functions" as MathFunctions
Import "math/core/constants" as Constants

Note: Trigonometric matrix functions
Let rotation_2d be LinAlg.create_rotation_matrix_2d(Constants.get_pi() / 4)
Let rotation_3d_x be LinAlg.create_rotation_matrix_3d("x", Constants.get_pi() / 6)
Let rotation_3d_y be LinAlg.create_rotation_matrix_3d("y", Constants.get_pi() / 3)

Note: Matrix functions using mathematical operations
Let sin_matrix be LinAlg.apply_elementwise(matrix_a, MathFunctions.sin)
Let exp_matrix be LinAlg.matrix_exponential(matrix_a)
Let log_matrix be LinAlg.matrix_logarithm(matrix_a)

Display "Rotation matrix (2D):" joined with LinAlg.matrix_to_string(rotation_2d)
```

### Statistics Integration

```runa
Import "stats/descriptive" as Stats

Note: Statistical operations on matrices
Let data_matrix be LinAlg.create_matrix_from_csv("data.csv")
Let column_means be LinAlg.compute_column_means(data_matrix)
Let covariance_matrix be LinAlg.compute_covariance_matrix(data_matrix)
Let correlation_matrix be LinAlg.compute_correlation_matrix(data_matrix)

Note: Principal Component Analysis preparation
Let centered_data be LinAlg.center_columns(data_matrix)
Let standardized_data be LinAlg.standardize_columns(data_matrix)

Display "Data matrix mean: " joined with LinAlg.vector_to_string(column_means)
```

## Performance Benchmarking

### Algorithm Performance Testing

```runa
Note: Performance comparison of different algorithms
Let large_matrix be LinAlg.create_random_matrix(1000, 1000, "normal", 0.0, 1.0)

Note: Test different multiplication algorithms
Let start_blas be LinAlg.get_timestamp()
Let result_blas be LinAlg.matrix_multiply_blas(large_matrix, large_matrix)
Let time_blas be LinAlg.get_timestamp() - start_blas

Let start_naive be LinAlg.get_timestamp()
Let result_naive be LinAlg.matrix_multiply_naive(large_matrix, large_matrix)
Let time_naive be LinAlg.get_timestamp() - start_naive

Display "BLAS multiplication: " joined with time_blas joined with "ms"
Display "Naive multiplication: " joined with time_naive joined with "ms"
Display "Speedup: " joined with (time_naive / time_blas) joined with "x"
```

## Best Practices

### Algorithm Selection

1. **Use BLAS/LAPACK**: Always prefer BLAS/LAPACK optimized routines for standard operations
2. **Memory Layout**: Store matrices in column-major format for optimal BLAS performance
3. **Block Operations**: Use blocked algorithms for cache efficiency with large matrices
4. **Vectorization**: Enable SIMD instructions for element-wise operations

### Performance Optimization

```runa
Note: Optimal performance configuration
LinAlg.configure_for_performance([
    ("thread_count", "auto"),
    ("block_size", "cache_optimal"),
    ("vectorization", True),
    ("gpu_threshold", 10000),
    ("memory_pool", "adaptive")
])

Note: Memory access pattern optimization
Let optimized_layout be LinAlg.optimize_memory_layout(matrix_data, "column_major")
Let cache_friendly be LinAlg.apply_cache_blocking(large_operation, 256)
```

### Error Prevention

```runa
Note: Defensive programming practices
If LinAlg.matrix_dimensions_compatible(matrix_a, matrix_b, "multiply"):
    Let product be LinAlg.matrix_multiply(matrix_a, matrix_b)
Otherwise:
    Display "Matrix dimensions incompatible for multiplication"
    Return LinAlg.create_error_matrix("dimension_mismatch")

Note: Numerical stability checks
Let stability_report be LinAlg.analyze_numerical_stability(computation_sequence)
If LinAlg.is_numerically_stable(stability_report):
    Let result be LinAlg.execute_computation_sequence(computation_sequence)
Otherwise:
    Let improved_sequence be LinAlg.improve_numerical_stability(computation_sequence)
    Let result be LinAlg.execute_computation_sequence(improved_sequence)
```

## Advanced Examples

### Large-Scale Linear Algebra

```runa
Note: Handle matrices too large for memory
Let large_matrix_file be "very_large_matrix.dat"
Let memory_mapped_matrix be LinAlg.create_memory_mapped_matrix(large_matrix_file)

Note: Out-of-core operations
Let out_of_core_result be LinAlg.out_of_core_multiply(
    memory_mapped_matrix, 
    another_large_matrix,
    chunk_size: 1000,
    temp_directory: "/tmp/linalgtemp"
)

Note: Distributed computation
LinAlg.configure_distributed_computing([
    "node1.cluster.local",
    "node2.cluster.local", 
    "node3.cluster.local"
])

Let distributed_result be LinAlg.distributed_matrix_multiply(
    huge_matrix_1,
    huge_matrix_2,
    distribution_strategy: "block_cyclic"
)
```

### Custom Precision Arithmetic

```runa
Note: Different precision levels
Let quad_precision_matrix be LinAlg.create_matrix_quad_precision(high_precision_data)
Let arbitrary_precision_matrix be LinAlg.create_matrix_arbitrary_precision(data, 128)

Note: Mixed precision computations
Let mixed_result be LinAlg.mixed_precision_multiply(
    single_precision_matrix,
    double_precision_matrix,
    output_precision: "double"
)

Note: Interval arithmetic for error bounds
Let interval_matrix be LinAlg.create_interval_matrix(lower_bounds, upper_bounds)
Let interval_result be LinAlg.interval_matrix_multiply(interval_matrix, interval_matrix)
Let error_bounds be LinAlg.get_result_bounds(interval_result)

Display "Result bounds: [" joined with error_bounds.lower joined with ", " joined with error_bounds.upper joined with "]"
```

The Core Linear Algebra module provides the essential building blocks for all linear algebra computations in Runa, emphasizing performance, numerical stability, and comprehensive functionality for scientific and engineering applications.