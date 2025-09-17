# Core Numerical Methods

The Core Numerical Methods module (`math/engine/numerical/core`) provides the fundamental infrastructure for numerical computing in Runa. This module implements essential algorithms for floating-point arithmetic, error analysis, precision control, convergence detection, and numerical stability analysis that underpin all other numerical computing operations.

## Quick Start

```runa
Import "math/engine/numerical/core" as Numerical
Import "math/core/constants" as Constants

Note: Basic numerical precision and error analysis
Let value_a be 1.0 / 3.0
Let value_b be 0.33333333333333333
Let absolute_error be Numerical.absolute_error(value_a, value_b)
Let relative_error be Numerical.relative_error(value_a, value_b)

Display "Absolute error: " joined with absolute_error
Display "Relative error: " joined with relative_error

Note: Machine precision and numerical limits
Let machine_epsilon be Numerical.get_machine_epsilon("float64")
Let max_float be Numerical.get_max_representable("float64")
Let min_float be Numerical.get_min_representable("float64")

Display "Machine epsilon (double): " joined with machine_epsilon
Display "Maximum representable float: " joined with max_float

Note: Convergence testing
Let sequence_values be [1.0, 0.5, 0.25, 0.125, 0.0625]
Let convergence_test be Numerical.test_convergence(
    sequence_values,
    tolerance: 1e-6,
    convergence_type: "absolute"
)

Let has_converged be Numerical.is_converged(convergence_test)
Let convergence_rate be Numerical.estimate_convergence_rate(sequence_values)

Display "Sequence has converged: " joined with has_converged
Display "Estimated convergence rate: " joined with convergence_rate

Note: Condition number analysis
Let test_matrix be [
    [1.0, 0.99],
    [0.99, 0.98]
]

Let condition_number be Numerical.condition_number_matrix(test_matrix, "2-norm")
Let is_well_conditioned be Numerical.is_well_conditioned(condition_number, threshold: 1e12)

Display "Matrix condition number: " joined with condition_number
Display "Matrix is well-conditioned: " joined with is_well_conditioned

Note: High-precision arithmetic
Let high_precision_pi be Numerical.compute_high_precision_constant("pi", precision_digits: 50)
Display "High-precision π: " joined with high_precision_pi
```

## Floating-Point Arithmetic and Precision

### IEEE 754 Arithmetic Analysis

```runa
Note: Understand floating-point representation
Let test_value be 0.1
Let binary_representation be Numerical.to_binary_representation(test_value)
Let exact_decimal be Numerical.get_exact_decimal_representation(test_value)

Display "Binary representation of 0.1: " joined with binary_representation
Display "Exact decimal value: " joined with exact_decimal

Note: Floating-point arithmetic properties
Let a be 1e20
Let b be 1.0
Let c be -1e20

Let associative_test_1 be (a + b) + c
Let associative_test_2 be a + (b + c)
let associativity_holds be Numerical.nearly_equal(associative_test_1, associative_test_2, 1e-10)

Display "Associative property holds: " joined with associativity_holds
Display "Result 1: " joined with associative_test_1
Display "Result 2: " joined with associative_test_2

Note: Catastrophic cancellation detection
Let large_number be 1.0000001
Let nearly_equal_number be 1.0000000
Let subtraction_result be large_number - nearly_equal_number

Let cancellation_factor be Numerical.detect_cancellation(
    large_number, 
    nearly_equal_number, 
    subtraction_result
)

If Numerical.is_catastrophic_cancellation(cancellation_factor):
    Display "Warning: Catastrophic cancellation detected"
    Let stable_result be Numerical.stable_subtraction(large_number, nearly_equal_number)
    Display "Stable alternative: " joined with stable_result
```

### Multiple Precision Arithmetic

```runa
Note: Work with different precision levels
Let single_precision_value be Numerical.create_float32(3.14159265358979)
Let double_precision_value be Numerical.create_float64(3.14159265358979)
Let quad_precision_value be Numerical.create_float128(3.14159265358979)

Display "Single precision: " joined with Numerical.to_string(single_precision_value, 8)
Display "Double precision: " joined with Numerical.to_string(double_precision_value, 16)
Display "Quad precision: " joined with Numerical.to_string(quad_precision_value, 32)

Note: Arbitrary precision arithmetic
Let arbitrary_precision_pi be Numerical.compute_arbitrary_precision([
    ("value", "pi"),
    ("precision_bits", 256),
    ("rounding_mode", "round_nearest")
])

Let pi_digits be Numerical.get_decimal_digits(arbitrary_precision_pi, digits: 75)
Display "π to 75 digits: " joined with pi_digits

Note: Precision conversion and rounding
Let high_precision_result be Numerical.multiply_arbitrary_precision(
    arbitrary_precision_pi,
    Numerical.create_arbitrary_precision("2.0", 256)
)

Let rounded_to_double be Numerical.round_to_precision(high_precision_result, "float64")
Let rounding_error be Numerical.compute_rounding_error(high_precision_result, rounded_to_double)

Display "Rounding error: " joined with rounding_error
```

### Interval Arithmetic

```runa
Note: Rigorous error bounds using interval arithmetic
Let interval_a be Numerical.create_interval(2.0, 3.0)
Let interval_b be Numerical.create_interval(1.5, 2.5)

Let interval_sum be Numerical.interval_add(interval_a, interval_b)
Let interval_product be Numerical.interval_multiply(interval_a, interval_b)
Let interval_quotient be Numerical.interval_divide(interval_a, interval_b)

Display "Interval sum: [" joined with Numerical.get_interval_lower(interval_sum) 
    joined with ", " joined with Numerical.get_interval_upper(interval_sum) joined with "]"

Note: Interval function evaluation
Process called "interval_function" that takes x_interval as Interval returns Interval:
    Let x_squared be Numerical.interval_power(x_interval, 2)
    Let two_x be Numerical.interval_multiply(Numerical.create_interval(2.0, 2.0), x_interval)
    Return Numerical.interval_subtract(x_squared, two_x)

Let input_interval be Numerical.create_interval(0.9, 1.1)
Let function_range be interval_function(input_interval)

Display "Function range over [0.9, 1.1]: [" 
    joined with Numerical.get_interval_lower(function_range)
    joined with ", " joined with Numerical.get_interval_upper(function_range) joined with "]"

Note: Validated computing with intervals
Let validated_computation be Numerical.validate_computation_with_intervals(
    computation_function: interval_function,
    input_bounds: input_interval,
    target_precision: 1e-10
)

Let is_computation_valid be Numerical.is_validated_result(validated_computation)
Let guaranteed_bounds be Numerical.get_guaranteed_bounds(validated_computation)

Display "Computation validation: " joined with is_computation_valid
```

## Error Analysis and Propagation

### Error Types and Measurement

```runa
Note: Different types of numerical errors
Let exact_value be Constants.get_e()  Note: Euler's number
Let approximation_1 be 2.718
Let approximation_2 be 2.7182818

Note: Absolute and relative errors
Let abs_error_1 be Numerical.absolute_error(exact_value, approximation_1)
Let abs_error_2 be Numerical.absolute_error(exact_value, approximation_2)
Let rel_error_1 be Numerical.relative_error(exact_value, approximation_1)
Let rel_error_2 be Numerical.relative_error(exact_value, approximation_2)

Display "Approximation 1 - Absolute error: " joined with abs_error_1
Display "Approximation 1 - Relative error: " joined with rel_error_1
Display "Approximation 2 - Absolute error: " joined with abs_error_2  
Display "Approximation 2 - Relative error: " joined with rel_error_2

Note: Significant digits analysis
Let significant_digits_1 be Numerical.count_significant_digits(exact_value, approximation_1)
Let significant_digits_2 be Numerical.count_significant_digits(exact_value, approximation_2)

Display "Significant digits in approximation 1: " joined with significant_digits_1
Display "Significant digits in approximation 2: " joined with significant_digits_2

Note: Error magnification in operations
Let small_error be 1e-10
Let value_with_error be 1.0 + small_error

Let magnified_error be Numerical.analyze_error_magnification([
    ("operation", "division"),
    ("numerator", value_with_error),
    ("denominator", small_error),
    ("input_error", small_error)
])

Let error_amplification_factor be Numerical.get_amplification_factor(magnified_error)
Display "Error amplification factor: " joined with error_amplification_factor
```

### Forward and Backward Error Analysis

```runa
Note: Forward error analysis - how errors in input affect output
Process called "sensitive_function" that takes x as Real returns Real:
    Return 1.0 / (x - 1.0)

Let input_value be 1.0001
Let input_perturbation be 1e-6
Let perturbed_input be input_value + input_perturbation

Let exact_output be sensitive_function(input_value)
Let perturbed_output be sensitive_function(perturbed_input)

Let forward_error be Numerical.forward_error_analysis(
    function: sensitive_function,
    input_value: input_value,
    input_error: input_perturbation
)

Let condition_number be Numerical.get_condition_number(forward_error)
Display "Function condition number: " joined with condition_number

Note: Backward error analysis - find input that gives computed output exactly
Let computed_result be 10000.1  Note: Some computed result with rounding errors

Let backward_error_analysis be Numerical.backward_error_analysis(
    function: sensitive_function,
    input_value: input_value,
    computed_output: computed_result
)

Let backward_error be Numerical.get_backward_error(backward_error_analysis)
Let is_numerically_stable be Numerical.is_backward_stable(backward_error_analysis, tolerance: 1e-12)

Display "Backward error: " joined with backward_error
Display "Algorithm is backward stable: " joined with is_numerically_stable
```

### Error Propagation in Computations

```runa
Note: Track error propagation through a computation sequence
Let computation_chain be Numerical.create_computation_chain()

Let step_1_input be Numerical.create_value_with_error(1.5, 1e-8)
Numerical.add_computation_step(computation_chain, "square", step_1_input)

Let step_2_result be Numerical.get_chain_intermediate_result(computation_chain, 1)
Numerical.add_computation_step(computation_chain, "add_constant", step_2_result, 0.25)

Let step_3_result be Numerical.get_chain_intermediate_result(computation_chain, 2)
Numerical.add_computation_step(computation_chain, "sqrt", step_3_result)

Let final_result be Numerical.execute_computation_chain(computation_chain)
Let propagated_error be Numerical.get_propagated_error(final_result)

Display "Final result: " joined with Numerical.get_value(final_result)
Display "Propagated error: ± " joined with propagated_error

Note: Sensitivity analysis for multivariate functions
Process called "multivariate_function" that takes variables as Vector returns Real:
    Let x be Numerical.get_vector_element(variables, 0)
    Let y be Numerical.get_vector_element(variables, 1)
    Return x * x + y * y - 2.0 * x * y

Let input_vector be Numerical.create_vector([2.0, 3.0])
Let input_errors be Numerical.create_vector([1e-6, 1e-6])

Let sensitivity_analysis be Numerical.multivariate_sensitivity_analysis(
    function: multivariate_function,
    input_point: input_vector,
    input_uncertainties: input_errors
)

Let output_uncertainty be Numerical.get_output_uncertainty(sensitivity_analysis)
Let partial_sensitivities be Numerical.get_partial_sensitivities(sensitivity_analysis)

Display "Output uncertainty: ± " joined with output_uncertainty
Display "Sensitivities: " joined with Numerical.vector_to_string(partial_sensitivities)
```

## Convergence Analysis and Acceleration

### Convergence Detection

```runa
Note: Test different types of convergence
Let fibonacci_ratios be [
    1.0, 2.0, 1.5, 1.666667, 1.6, 1.625, 1.615385, 1.619048,
    1.617647, 1.618182, 1.617978, 1.618056, 1.618026, 1.618037
]

Let absolute_convergence be Numerical.test_absolute_convergence(
    fibonacci_ratios,
    tolerance: 1e-6
)

Let relative_convergence be Numerical.test_relative_convergence(
    fibonacci_ratios,
    tolerance: 1e-6
)

Let monotonic_convergence be Numerical.test_monotonic_convergence(fibonacci_ratios)

Display "Absolute convergence: " joined with Numerical.is_converged(absolute_convergence)
Display "Relative convergence: " joined with Numerical.is_converged(relative_convergence)
Display "Monotonic convergence: " joined with monotonic_convergence

Note: Estimate convergence rate and order
Let convergence_order be Numerical.estimate_convergence_order(fibonacci_ratios)
Let convergence_constant be Numerical.estimate_convergence_constant(fibonacci_ratios)

Display "Convergence order: " joined with convergence_order
Display "Convergence constant: " joined with convergence_constant

Note: Stagnation detection
Let stagnating_sequence be [1.0, 0.5, 0.25, 0.125, 0.1249999, 0.1249999, 0.1249999]

Let stagnation_analysis be Numerical.detect_stagnation(
    stagnating_sequence,
    stagnation_threshold: 1e-6,
    consecutive_steps: 3
)

Let has_stagnated be Numerical.is_stagnating(stagnation_analysis)
Let stagnation_point be Numerical.get_stagnation_point(stagnation_analysis)

Display "Sequence has stagnated: " joined with has_stagnated
Display "Stagnation detected at step: " joined with stagnation_point
```

### Convergence Acceleration Techniques

```runa
Note: Aitken's Δ² process for linear convergence acceleration
Let slowly_converging_sequence be [
    1.0, 0.9, 0.81, 0.729, 0.6561, 0.59049, 0.531441, 0.4782969
]

Let aitken_accelerated be Numerical.aitken_acceleration(slowly_converging_sequence)
Let acceleration_improvement be Numerical.compare_convergence_rates(
    slowly_converging_sequence,
    aitken_accelerated
)

Display "Original sequence last value: " joined with 
    Numerical.get_last_element(slowly_converging_sequence)
Display "Aitken accelerated value: " joined with 
    Numerical.get_last_element(aitken_accelerated)
Display "Acceleration improvement factor: " joined with acceleration_improvement

Note: Richardson extrapolation
Let richardson_sequence be [1.5708, 1.5707963, 1.57079632679]  Note: π/2 approximations
Let richardson_extrapolated be Numerical.richardson_extrapolation(
    richardson_sequence,
    extrapolation_order: 2
)

Display "Richardson extrapolated value: " joined with richardson_extrapolated

Note: Shanks transformation for oscillating sequences
Let oscillating_sequence be [1.0, -0.5, 0.25, -0.125, 0.0625, -0.03125]
Let shanks_transformed be Numerical.shanks_transformation(oscillating_sequence)

Display "Shanks transformation result: " joined with 
    Numerical.get_last_element(shanks_transformed)

Note: Epsilon algorithm (generalization of Aitken)
Let epsilon_acceleration be Numerical.epsilon_algorithm(
    slowly_converging_sequence,
    max_order: 4
)

Let epsilon_table be Numerical.get_epsilon_table(epsilon_acceleration)
Let best_approximation be Numerical.get_best_approximation(epsilon_acceleration)

Display "Best epsilon algorithm approximation: " joined with best_approximation
```

## Numerical Stability and Conditioning

### Condition Number Analysis

```runa
Note: Analyze conditioning of different mathematical operations
Let well_conditioned_matrix be [
    [2.0, 1.0],
    [1.0, 2.0]
]

Let ill_conditioned_matrix be [
    [1.0, 1.0],
    [1.0, 1.000001]
]

Let condition_1 be Numerical.condition_number_matrix(well_conditioned_matrix, "2-norm")
Let condition_2 be Numerical.condition_number_matrix(ill_conditioned_matrix, "2-norm")

Display "Well-conditioned matrix κ: " joined with condition_1
Display "Ill-conditioned matrix κ: " joined with condition_2

Note: Condition number for different norms
Let condition_1_norm be Numerical.condition_number_matrix(ill_conditioned_matrix, "1-norm")
Let condition_inf_norm be Numerical.condition_number_matrix(ill_conditioned_matrix, "infinity-norm")
Let condition_frobenius be Numerical.condition_number_matrix(ill_conditioned_matrix, "frobenius")

Display "Condition number (1-norm): " joined with condition_1_norm
Display "Condition number (∞-norm): " joined with condition_inf_norm
Display "Condition number (Frobenius): " joined with condition_frobenius

Note: Function condition number analysis
Process called "condition_test_function" that takes x as Real returns Real:
    Return Numerical.log(x)

Let function_condition be Numerical.function_condition_number(
    condition_test_function,
    evaluation_point: 1.001,
    perturbation_size: 1e-8
)

Display "Function condition number: " joined with function_condition

Note: Eigenvalue condition analysis
Let eigenvalue_matrix be [
    [4.0, -1.0, 1.0],
    [-1.0, 4.0, -1.0], 
    [1.0, -1.0, 4.0]
]

Let eigenvalue_conditioning be Numerical.eigenvalue_condition_analysis(eigenvalue_matrix)
Let worst_conditioned_eigenvalue be Numerical.get_worst_conditioned_eigenvalue(eigenvalue_conditioning)

Display "Worst eigenvalue condition number: " joined with worst_conditioned_eigenvalue
```

### Numerical Stability Assessment

```runa
Note: Algorithm stability analysis
Let stability_test_data be [1e10, 1.0, -1e10]

Let naive_sum be Numerical.naive_summation(stability_test_data)
Let kahan_sum be Numerical.kahan_summation(stability_test_data)
Let compensated_sum be Numerical.compensated_summation(stability_test_data)

Display "Naive summation: " joined with naive_sum
Display "Kahan summation: " joined with kahan_sum
Display "Compensated summation: " joined with compensated_sum

Note: Stability of matrix operations
Let near_singular_matrix be [
    [1.0, 2.0, 3.0],
    [4.0, 5.0, 6.0],
    [7.0, 8.0, 9.00001]
]

Let stability_analysis be Numerical.matrix_operation_stability(
    near_singular_matrix,
    operations: ["inversion", "determinant", "eigenvalues"]
)

Let inversion_stability be Numerical.get_operation_stability(stability_analysis, "inversion")
Let determinant_stability be Numerical.get_operation_stability(stability_analysis, "determinant")

Display "Matrix inversion stability: " joined with inversion_stability
Display "Determinant computation stability: " joined with determinant_stability

Note: Perturbation analysis
Let perturbation_study be Numerical.perform_perturbation_analysis(
    matrix: near_singular_matrix,
    perturbation_magnitude: 1e-12,
    num_perturbations: 100,
    operation: "eigenvalue_computation"
)

Let max_eigenvalue_change be Numerical.get_max_perturbation_effect(perturbation_study)
Let average_sensitivity be Numerical.get_average_sensitivity(perturbation_study)

Display "Maximum eigenvalue change: " joined with max_eigenvalue_change
Display "Average sensitivity: " joined with average_sensitivity
```

### Regularization and Stabilization

```runa
Note: Regularization techniques for ill-conditioned problems
Let ill_conditioned_system be [
    [1.0, 1.0],
    [1.0, 1.0000001]
]

Let rhs_vector be [2.0, 2.0000001]

Note: Tikhonov regularization
Let tikhonov_regularized be Numerical.tikhonov_regularization(
    ill_conditioned_system,
    rhs_vector,
    regularization_parameter: 1e-6
)

Let regularized_solution be Numerical.solve_regularized_system(tikhonov_regularized)

Note: Truncated SVD regularization
Let svd_regularized be Numerical.svd_regularization(
    ill_conditioned_system,
    rhs_vector,
    truncation_tolerance: 1e-10
)

Let svd_solution be Numerical.solve_regularized_system(svd_regularized)

Display "Tikhonov solution: [" joined with Numerical.get_vector_element(regularized_solution, 0)
    joined with ", " joined with Numerical.get_vector_element(regularized_solution, 1) joined with "]"
Display "SVD solution: [" joined with Numerical.get_vector_element(svd_solution, 0)
    joined with ", " joined with Numerical.get_vector_element(svd_solution, 1) joined with "]"

Note: Iterative refinement for stability
Let initial_solution be Numerical.solve_system_basic(ill_conditioned_system, rhs_vector)
Let refined_solution be Numerical.iterative_refinement(
    ill_conditioned_system,
    rhs_vector,
    initial_solution,
    max_refinements: 5,
    tolerance: 1e-12
)

Let refinement_improvement be Numerical.compute_residual_improvement(
    ill_conditioned_system,
    rhs_vector,
    initial_solution,
    refined_solution
)

Display "Residual improvement factor: " joined with refinement_improvement
```

## Advanced Numerical Algorithms

### Adaptive Precision Control

```runa
Note: Automatic precision adjustment based on problem characteristics
Let adaptive_precision_controller be Numerical.create_adaptive_precision_controller([
    ("initial_precision", "float64"),
    ("max_precision", "float128"), 
    ("precision_increase_factor", 2),
    ("stability_threshold", 1e-12)
])

Process called "precision_sensitive_computation" that takes x as Real returns Real:
    Return (x - 1.0) / (x * x - 1.0)

Let adaptive_result be Numerical.compute_with_adaptive_precision(
    adaptive_precision_controller,
    precision_sensitive_computation,
    input_value: 1.0000001,
    target_accuracy: 1e-15
)

Let final_precision_used be Numerical.get_final_precision(adaptive_result)
Let achieved_accuracy be Numerical.get_achieved_accuracy(adaptive_result)

Display "Final precision used: " joined with final_precision_used
Display "Achieved accuracy: " joined with achieved_accuracy

Note: Mixed precision algorithms
Let mixed_precision_config be Numerical.create_mixed_precision_configuration([
    ("working_precision", "float32"),
    ("accumulation_precision", "float64"),
    ("final_precision", "float64"),
    ("intermediate_checks", True)
])

Let mixed_precision_result be Numerical.compute_with_mixed_precision(
    mixed_precision_config,
    computation_function: precision_sensitive_computation,
    input_data: [0.9999999, 1.0000001, 1.0000002]
)

Let performance_improvement be Numerical.get_performance_improvement(mixed_precision_result)
Let accuracy_maintained be Numerical.verify_accuracy_maintained(mixed_precision_result)

Display "Performance improvement: " joined with performance_improvement joined with "x"
Display "Accuracy maintained: " joined with accuracy_maintained
```

### Verified Computing

```runa
Note: Rigorous numerical computation with guaranteed bounds
Let verification_config be Numerical.create_verification_configuration([
    ("use_interval_arithmetic", True),
    ("error_bound_computation", "rigorous"),
    ("rounding_mode_control", True)
])

Process called "function_to_verify" that takes x as Real returns Real:
    Return x * x * x - 2.0 * x - 1.0

Let verified_computation be Numerical.compute_with_verification(
    verification_config,
    function_to_verify,
    input_range: Numerical.create_interval(1.0, 2.0),
    subdivision_depth: 10
)

Let guaranteed_range be Numerical.get_guaranteed_output_range(verified_computation)
Let verification_certificate be Numerical.get_verification_certificate(verified_computation)

Display "Guaranteed output range: [" joined with Numerical.get_interval_lower(guaranteed_range)
    joined with ", " joined with Numerical.get_interval_upper(guaranteed_range) joined with "]"
Display "Verification certificate valid: " joined with 
    Numerical.is_certificate_valid(verification_certificate)

Note: Certified root bounds
Let certified_root_bounds be Numerical.compute_certified_root_bounds(
    function_to_verify,
    search_interval: Numerical.create_interval(1.0, 2.0),
    isolation_tolerance: 1e-10
)

Let root_intervals be Numerical.get_root_isolation_intervals(certified_root_bounds)
Let num_certified_roots be Numerical.get_number_of_roots(certified_root_bounds)

Display "Number of certified roots: " joined with num_certified_roots
For i from 0 to (num_certified_roots - 1):
    Let root_interval be Numerical.get_root_interval(root_intervals, i)
    Display "Root " joined with (i + 1) joined with " in: [" 
        joined with Numerical.get_interval_lower(root_interval)
        joined with ", " joined with Numerical.get_interval_upper(root_interval) joined with "]"
```

## Performance Optimization and Monitoring

### Computational Complexity Analysis

```runa
Note: Analyze algorithm complexity and scaling behavior
Let complexity_analyzer be Numerical.create_complexity_analyzer()

Let test_sizes be [100, 200, 400, 800, 1600]
Let execution_times be []

For size in test_sizes:
    Let test_matrix be Numerical.create_random_matrix(size, size)
    
    Let start_time be Numerical.get_high_precision_time()
    Let matrix_inverse be Numerical.matrix_inverse(test_matrix)
    Let end_time be Numerical.get_high_precision_time()
    
    Let execution_time be end_time - start_time
    Numerical.append_to_vector(execution_times, execution_time)

Let complexity_analysis be Numerical.analyze_complexity_scaling(
    complexity_analyzer,
    input_sizes: test_sizes,
    execution_times: execution_times
)

Let estimated_complexity be Numerical.get_complexity_estimate(complexity_analysis)
Let scaling_coefficient be Numerical.get_scaling_coefficient(complexity_analysis)

Display "Estimated complexity: O(n^" joined with estimated_complexity joined with ")"
Display "Scaling coefficient: " joined with scaling_coefficient

Note: Memory usage analysis
Let memory_profiler be Numerical.create_memory_profiler()
Numerical.start_memory_profiling(memory_profiler)

Let large_computation_result be Numerical.compute_large_matrix_product(
    size: 2000,
    precision: "float64"
)

Numerical.stop_memory_profiling(memory_profiler)

Let memory_report be Numerical.get_memory_report(memory_profiler)
Let peak_memory be Numerical.get_peak_memory_usage(memory_report)
Let memory_efficiency be Numerical.get_memory_efficiency(memory_report)

Display "Peak memory usage: " joined with peak_memory joined with " MB"
Display "Memory efficiency: " joined with memory_efficiency joined with "%"
```

### Algorithm Performance Tuning

```runa
Note: Optimize numerical algorithms for specific hardware
Let performance_tuner be Numerical.create_performance_tuner()

Let cpu_characteristics be Numerical.analyze_cpu_characteristics([
    "cache_sizes",
    "simd_capabilities", 
    "floating_point_units",
    "memory_bandwidth"
])

Let optimized_parameters be Numerical.optimize_algorithm_parameters(
    performance_tuner,
    algorithm: "matrix_multiplication",
    problem_size: 1000,
    hardware_info: cpu_characteristics,
    optimization_target: "throughput"
)

Let block_size be Numerical.get_optimal_block_size(optimized_parameters)
Let thread_count be Numerical.get_optimal_thread_count(optimized_parameters)
Let vectorization_strategy be Numerical.get_vectorization_strategy(optimized_parameters)

Display "Optimal block size: " joined with block_size
Display "Optimal thread count: " joined with thread_count
Display "Vectorization strategy: " joined with vectorization_strategy

Note: Performance benchmarking and validation
Let benchmark_suite be Numerical.create_benchmark_suite([
    "basic_arithmetic",
    "matrix_operations",
    "transcendental_functions", 
    "special_functions"
])

Let benchmark_results be Numerical.run_benchmark_suite(
    benchmark_suite,
    optimization_level: "aggressive",
    precision_levels: ["float32", "float64", "float128"]
)

Let performance_summary be Numerical.generate_performance_summary(benchmark_results)
Display "Performance summary:"
Display Numerical.format_performance_table(performance_summary)
```

## Integration Examples

### With Mathematical Functions

```runa
Import "math/core/functions" as MathFunctions

Note: High-precision computation of special function values
Let high_precision_bessel be Numerical.compute_special_function_high_precision(
    function_name: "bessel_j0",
    argument: 10.0,
    target_precision: 50
)

Let standard_bessel be MathFunctions.bessel_j0(10.0)
Let precision_difference be Numerical.count_matching_digits(high_precision_bessel, standard_bessel)

Display "High-precision J₀(10): " joined with high_precision_bessel
Display "Standard precision J₀(10): " joined with standard_bessel  
Display "Matching digits: " joined with precision_difference

Note: Error analysis in special function evaluation
Let error_analysis be Numerical.analyze_special_function_error(
    function_name: "gamma_function",
    argument_range: Numerical.create_interval(0.1, 10.0),
    evaluation_points: 1000
)

Let max_relative_error be Numerical.get_max_relative_error(error_analysis)
Let average_accuracy be Numerical.get_average_accuracy(error_analysis)

Display "Maximum relative error in Γ(x): " joined with max_relative_error
Display "Average accuracy (significant digits): " joined with average_accuracy
```

### With Linear Algebra Operations

```runa
Import "math/engine/linalg/core" as LinAlg

Note: Numerical stability in linear algebra computations
Let test_matrix be LinAlg.create_hilbert_matrix(10)  Note: Notoriously ill-conditioned

Let stability_report be Numerical.analyze_linear_algebra_stability(
    matrix: test_matrix,
    operations: ["inversion", "eigenvalue_decomposition", "svd"],
    precision_levels: ["float32", "float64", "float128"]
)

Let inversion_accuracy be Numerical.get_operation_accuracy(stability_report, "inversion")
Let eigenvalue_accuracy be Numerical.get_operation_accuracy(stability_report, "eigenvalue_decomposition")

Display "Matrix inversion accuracy:"
For precision in ["float32", "float64", "float128"]:
    Let accuracy be Numerical.get_precision_accuracy(inversion_accuracy, precision)
    Display "  " joined with precision joined with ": " joined with accuracy joined with " digits"

Note: Iterative refinement integration
Let linear_system_matrix be LinAlg.create_random_matrix(500, 500)
Let linear_system_rhs be LinAlg.create_random_vector(500)

Let refined_solution be Numerical.solve_with_iterative_refinement(
    matrix: linear_system_matrix,
    rhs: linear_system_rhs,
    initial_precision: "float32",
    refinement_precision: "float64",
    max_refinements: 5
)

Let final_residual_norm be Numerical.compute_residual_norm(
    linear_system_matrix,
    linear_system_rhs,
    refined_solution
)

Display "Final residual norm: " joined with final_residual_norm
```

## Best Practices

### Numerical Algorithm Design

```runa
Note: Guidelines for robust numerical algorithm implementation
Let algorithm_design_checker be Numerical.create_algorithm_design_checker()

Note: Check for common numerical pitfalls
Let algorithm_analysis be Numerical.analyze_algorithm_design(
    algorithm_design_checker,
    algorithm_description: "custom_root_finding_method",
    implementation_details: algorithm_implementation_details
)

Let potential_issues be Numerical.get_potential_numerical_issues(algorithm_analysis)
Let stability_warnings be Numerical.get_stability_warnings(algorithm_analysis)

Display "Potential numerical issues found: " joined with 
    Numerical.count_issues(potential_issues)

For issue in potential_issues:
    Display "  - " joined with Numerical.describe_issue(issue)

Note: Validation and testing framework
Let numerical_test_suite be Numerical.create_numerical_test_suite([
    ("accuracy_tests", True),
    ("stability_tests", True),
    ("performance_tests", True),
    ("edge_case_tests", True)
])

Let test_results be Numerical.run_numerical_tests(
    numerical_test_suite,
    algorithm_under_test: "custom_algorithm",
    test_data_sets: standard_test_problems
)

Let test_passed be Numerical.all_tests_passed(test_results)
Let test_summary be Numerical.generate_test_summary(test_results)

Display "All tests passed: " joined with test_passed
Display "Test summary: " joined with test_summary
```

### Error Control and Monitoring

```runa
Note: Comprehensive error control framework
Let error_control_system be Numerical.create_error_control_system([
    ("error_estimation", "adaptive"),
    ("tolerance_management", "automatic"),
    ("precision_adjustment", "dynamic"),
    ("convergence_monitoring", "comprehensive")
])

Let controlled_computation be Numerical.compute_with_error_control(
    error_control_system,
    computation_function: complex_numerical_computation,
    input_data: problem_data,
    accuracy_requirements: user_accuracy_requirements
)

Let error_control_report be Numerical.get_error_control_report(controlled_computation)
Let accuracy_achieved be Numerical.verify_accuracy_requirements(
    controlled_computation,
    user_accuracy_requirements
)

Display "Accuracy requirements met: " joined with accuracy_achieved
Display "Error control summary:"
Display Numerical.format_error_control_report(error_control_report)
```

The Core Numerical Methods module provides the essential infrastructure for reliable, accurate, and efficient numerical computing, ensuring that all numerical algorithms in Runa maintain high standards of precision, stability, and performance across diverse computational domains.