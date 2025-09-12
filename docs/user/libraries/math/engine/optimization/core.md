# Core Optimization Methods

The Core Optimization module (`math/engine/optimization/core`) provides fundamental optimization algorithms and infrastructure that serve as the foundation for more specialized optimization methods. This module implements classical optimization techniques with robust numerical implementations.

## Overview

This module provides essential optimization building blocks including line search methods, trust region algorithms, and fundamental optimization procedures that are used throughout the optimization engine.

## Key Algorithms

### Line Search Methods

Line search algorithms find the optimal step size along a given search direction, forming the backbone of many optimization algorithms.

#### Armijo Line Search
```runa
Import "math/engine/optimization/core" as Core

Process called "objective_function" that takes x as List[String] returns Float:
    Let x1 be MathCore.parse_float(x[0])
    Let x2 be MathCore.parse_float(x[1])
    Return x1 * x1 + 2.0 * x2 * x2

Process called "gradient_function" that takes x as List[String] returns List[String]:
    Let x1 be MathCore.parse_float(x[0])
    Let x2 be MathCore.parse_float(x[1])
    Return [MathCore.float_to_string(2.0 * x1), MathCore.float_to_string(4.0 * x2)]

Let current_point be ["2.0", "1.0"]
Let search_direction be ["-1.0", "-0.5"]

Let armijo_result be Core.armijo_line_search(
    objective_function,
    gradient_function,
    current_point,
    search_direction,
    c1: 1e-4,
    max_step: 1.0,
    backtrack_factor: 0.5
)

Let step_size be Core.get_step_size(armijo_result)
Let sufficient_decrease be Core.armijo_satisfied(armijo_result)

Display "Armijo step size: " joined with step_size
Display "Sufficient decrease: " joined with sufficient_decrease
```

#### Wolfe Line Search
```runa
Note: More sophisticated line search with curvature condition
Let wolfe_result be Core.wolfe_line_search(
    objective_function,
    gradient_function,
    current_point,
    search_direction,
    c1: 1e-4,
    c2: 0.9,
    max_iterations: 50
)

Let wolfe_step be Core.get_wolfe_step(wolfe_result)
Let strong_wolfe be Core.strong_wolfe_satisfied(wolfe_result)

Display "Wolfe step size: " joined with wolfe_step
Display "Strong Wolfe conditions: " joined with strong_wolfe
```

#### Golden Section Search
```runa
Note: Univariate optimization without derivatives
Process called "univariate_function" that takes x as Float returns Float:
    Return x * x - 4.0 * x + 3.0

Let golden_result be Core.golden_section_search(
    univariate_function,
    lower_bound: 0.0,
    upper_bound: 4.0,
    tolerance: 1e-8
)

Let optimal_point be Core.get_golden_optimum(golden_result)
Let optimal_value be Core.get_golden_value(golden_result)
Let iterations_count be Core.get_golden_iterations(golden_result)

Display "Golden section optimum: x* = " joined with optimal_point
Display "Optimal value: f(x*) = " joined with optimal_value
Display "Iterations: " joined with iterations_count
```

### Trust Region Methods

Trust region methods maintain a region around the current point where a quadratic model is trusted to approximate the objective function.

#### Basic Trust Region Algorithm
```runa
Let trust_region_config be Core.create_trust_region_config([
    ("initial_radius", 1.0),
    ("max_radius", 10.0),
    ("eta1", 0.25),  Note: Shrink threshold
    ("eta2", 0.75),  Note: Expand threshold
    ("gamma1", 0.25), Note: Shrink factor
    ("gamma2", 2.0),  Note: Expand factor
    ("tolerance", 1e-8)
])

Let trust_result be Core.trust_region_optimize(
    objective_function,
    gradient_function,
    current_point,
    trust_region_config
)

Let tr_solution be Core.get_trust_region_solution(trust_result)
Let tr_radius_history be Core.get_radius_history(trust_result)
Let tr_iterations be Core.get_trust_region_iterations(trust_result)

Display "Trust region solution: " joined with vector_to_string(tr_solution)
Display "Final trust region radius: " joined with tr_radius_history[-1]
Display "Converged in " joined with tr_iterations joined with " iterations"
```

#### Dogleg Method
```runa
Note: Efficient trust region subproblem solver
Process called "hessian_function" that takes x as List[String] returns List[List[String]]:
    Note: Constant Hessian for quadratic function
    Return [
        ["2.0", "0.0"],
        ["0.0", "4.0"]
    ]

Let dogleg_result be Core.dogleg_trust_region(
    objective_function,
    gradient_function,
    hessian_function,
    current_point,
    trust_radius: 1.0
)

Let dogleg_step be Core.get_dogleg_step(dogleg_result)
Let cauchy_step be Core.get_cauchy_point(dogleg_result)
Let newton_step be Core.get_newton_step(dogleg_result)

Display "Dogleg step: " joined with vector_to_string(dogleg_step)
Display "Cauchy point: " joined with vector_to_string(cauchy_step)
Display "Newton step: " joined with vector_to_string(newton_step)
```

### Quasi-Newton Methods

Quasi-Newton methods approximate the Hessian matrix using gradient information from previous iterations.

#### BFGS Algorithm
```runa
Let bfgs_config be Core.create_bfgs_config([
    ("tolerance", 1e-8),
    ("max_iterations", 1000),
    ("line_search", "wolfe"),
    ("initial_hessian", "identity")
])

Let bfgs_result be Core.bfgs_optimize(
    objective_function,
    gradient_function,
    current_point,
    bfgs_config
)

Let bfgs_solution be Core.get_bfgs_solution(bfgs_result)
Let bfgs_hessian_approx be Core.get_final_hessian_approximation(bfgs_result)
Let bfgs_iterations be Core.get_bfgs_iterations(bfgs_result)

Display "BFGS solution: " joined with vector_to_string(bfgs_solution)
Display "Converged in " joined with bfgs_iterations joined with " iterations"

Note: Analyze Hessian approximation quality
Let exact_hessian be compute_exact_hessian(objective_function, bfgs_solution)
Let hessian_error be Core.matrix_frobenius_norm_difference(bfgs_hessian_approx, exact_hessian)
Display "Hessian approximation error: " joined with hessian_error
```

#### L-BFGS Algorithm
```runa
Note: Limited memory BFGS for large-scale problems
Let lbfgs_config be Core.create_lbfgs_config([
    ("memory_size", 10),
    ("tolerance", 1e-8),
    ("max_iterations", 1000),
    ("line_search", "strong_wolfe")
])

Let lbfgs_result be Core.lbfgs_optimize(
    objective_function,
    gradient_function,
    current_point,
    lbfgs_config
)

Let lbfgs_solution be Core.get_lbfgs_solution(lbfgs_result)
Let memory_usage be Core.get_lbfgs_memory_usage(lbfgs_result)
Let lbfgs_iterations be Core.get_lbfgs_iterations(lbfgs_result)

Display "L-BFGS solution: " joined with vector_to_string(lbfgs_solution)
Display "Memory usage: " joined with memory_usage joined with " vectors stored"
Display "Converged in " joined with lbfgs_iterations joined with " iterations"
```

#### DFP Algorithm
```runa
Note: Davidon-Fletcher-Powell method (dual to BFGS)
Let dfp_result be Core.dfp_optimize(
    objective_function,
    gradient_function,
    current_point,
    tolerance: 1e-8,
    max_iterations: 1000
)

Let dfp_solution be Core.get_dfp_solution(dfp_result)
Let dfp_hessian_inverse be Core.get_dfp_hessian_inverse_approximation(dfp_result)

Display "DFP solution: " joined with vector_to_string(dfp_solution)

Note: Compare with BFGS performance
Let convergence_comparison be Core.compare_quasi_newton_methods([bfgs_result, lbfgs_result, dfp_result])
Display "Fastest convergence: " joined with Core.get_fastest_method(convergence_comparison)
```

### Newton's Method

Newton's method uses second-order information for quadratic convergence.

#### Classical Newton Method
```runa
Let newton_config be Core.create_newton_config([
    ("tolerance", 1e-10),
    ("max_iterations", 100),
    ("line_search", "armijo"),
    ("hessian_modification", "cholesky")
])

Let newton_result be Core.newton_optimize(
    objective_function,
    gradient_function,
    hessian_function,
    current_point,
    newton_config
)

Let newton_solution be Core.get_newton_solution(newton_result)
Let newton_iterations be Core.get_newton_iterations(newton_result)
Let quadratic_convergence be Core.verify_quadratic_convergence(newton_result)

Display "Newton solution: " joined with vector_to_string(newton_solution)
Display "Quadratic convergence: " joined with quadratic_convergence
```

#### Modified Newton Method
```runa
Note: Handle negative curvature and indefinite Hessians
Let modified_newton_result be Core.modified_newton_optimize(
    objective_function,
    gradient_function,
    hessian_function,
    current_point,
    modification_strategy: "eigenvalue_modification",
    min_eigenvalue: 1e-6
)

Let modified_solution be Core.get_modified_newton_solution(modified_newton_result)
Let hessian_modifications be Core.get_hessian_modification_count(modified_newton_result)

Display "Modified Newton solution: " joined with vector_to_string(modified_solution)
Display "Hessian modifications applied: " joined with hessian_modifications
```

### Conjugate Gradient Methods

Conjugate gradient methods are particularly effective for quadratic functions and large-scale optimization.

#### Fletcher-Reeves Method
```runa
Let fr_config be Core.create_conjugate_gradient_config([
    ("beta_formula", "fletcher_reeves"),
    ("tolerance", 1e-8),
    ("max_iterations", 1000),
    ("restart_frequency", 50)
])

Let fr_result be Core.conjugate_gradient_optimize(
    objective_function,
    gradient_function,
    current_point,
    fr_config
)

Let fr_solution be Core.get_conjugate_gradient_solution(fr_result)
Let fr_iterations be Core.get_conjugate_gradient_iterations(fr_result)
Let restart_count be Core.get_restart_count(fr_result)

Display "Fletcher-Reeves solution: " joined with vector_to_string(fr_solution)
Display "Iterations: " joined with fr_iterations joined with " (restarts: " joined with restart_count joined with ")"
```

#### Polak-Ribière Method
```runa
Let pr_config be Core.create_conjugate_gradient_config([
    ("beta_formula", "polak_ribiere"),
    ("tolerance", 1e-8),
    ("max_iterations", 1000),
    ("restart_frequency", 50)
])

Let pr_result be Core.conjugate_gradient_optimize(
    objective_function,
    gradient_function,
    current_point,
    pr_config
)

Note: Compare different beta formulas
Let beta_comparison be Core.compare_cg_beta_formulas([fr_result, pr_result])
Display "Best beta formula for this problem: " joined with Core.get_best_beta_formula(beta_comparison)
```

## Advanced Features

### Automatic Differentiation Integration

```runa
Import "math/engine/autodiff/forward" as AutoDiff

Note: Use automatic differentiation for gradient computation
Process called "complex_objective" that takes x as List[String] returns Float:
    Let vars be AutoDiff.create_variables(x)
    Let x1 be AutoDiff.get_variable(vars, 0)
    Let x2 be AutoDiff.get_variable(vars, 1)
    
    Let term1 be AutoDiff.multiply(x1, x1)
    Let term2 be AutoDiff.multiply(AutoDiff.sin(x2), AutoDiff.cos(x1))
    Let result be AutoDiff.add(term1, term2)
    
    Return AutoDiff.get_value(result)

Let autodiff_gradient be Core.create_autodiff_gradient(complex_objective)

Let autodiff_result be Core.bfgs_optimize(
    complex_objective,
    autodiff_gradient,
    current_point,
    bfgs_config
)

Let autodiff_solution be Core.get_bfgs_solution(autodiff_result)
Display "Automatic differentiation solution: " joined with vector_to_string(autodiff_solution)
```

### Numerical Differentiation

```runa
Note: Finite difference approximations when analytical gradients unavailable
Let finite_diff_config be Core.create_finite_difference_config([
    ("method", "central"),
    ("step_size", 1e-8),
    ("adaptive_step", True)
])

Let finite_diff_gradient be Core.create_finite_difference_gradient(
    objective_function,
    finite_diff_config
)

Let finite_diff_hessian be Core.create_finite_difference_hessian(
    objective_function,
    finite_diff_config
)

Note: Compare accuracy of different finite difference methods
Let forward_diff be Core.create_finite_difference_gradient(objective_function, [("method", "forward")])
Let central_diff be Core.create_finite_difference_gradient(objective_function, [("method", "central")])

Let gradient_accuracy_test be Core.compare_gradient_approximations(
    [forward_diff, central_diff, autodiff_gradient],
    test_point: current_point
)

Display "Most accurate gradient method: " joined with Core.get_most_accurate_method(gradient_accuracy_test)
```

### Optimization Diagnostics

```runa
Note: Comprehensive optimization monitoring and analysis
Let diagnostic_monitor be Core.create_diagnostic_monitor([
    ("track_objective", True),
    ("track_gradient_norm", True),
    ("track_step_size", True),
    ("track_condition_number", True),
    ("save_iterates", True)
])

Let monitored_result be Core.optimize_with_diagnostics(
    objective_function,
    gradient_function,
    current_point,
    method: "bfgs",
    monitor: diagnostic_monitor
)

Let diagnostic_data be Core.get_diagnostic_data(monitored_result)

Note: Analyze convergence behavior
Let objective_history be Core.get_objective_history(diagnostic_data)
Let gradient_norm_history be Core.get_gradient_norm_history(diagnostic_data)
Let step_size_history be Core.get_step_size_history(diagnostic_data)

Let convergence_rate be Core.estimate_convergence_rate(objective_history)
Let conditioning_issues be Core.detect_conditioning_problems(diagnostic_data)

Display "Estimated convergence rate: " joined with convergence_rate
If Core.has_conditioning_issues(conditioning_issues):
    Display "Warning: Conditioning problems detected"
    Let condition_numbers be Core.get_condition_number_history(diagnostic_data)
    Display "Max condition number: " joined with Core.max_condition_number(condition_numbers)
```

### Multi-Start Optimization

```runa
Note: Global optimization through multiple random starts
Let multistart_config be Core.create_multistart_config([
    ("num_starts", 20),
    ("start_distribution", "uniform"),
    ("bounds", [[-10.0, 10.0], [-10.0, 10.0]]),
    ("local_method", "lbfgs"),
    ("tolerance", 1e-8)
])

Let multistart_result be Core.multistart_optimize(
    objective_function,
    gradient_function,
    multistart_config
)

Let all_local_minima be Core.get_all_local_minima(multistart_result)
Let global_minimum be Core.get_global_minimum(multistart_result)
Let success_rate be Core.get_convergence_success_rate(multistart_result)

Display "Found " joined with Core.count_unique_minima(all_local_minima) joined with " unique local minima"
Display "Global minimum: " joined with vector_to_string(global_minimum)
Display "Success rate: " joined with (success_rate * 100.0) joined with "%"

Note: Analyze basin of attraction
Let basin_analysis be Core.analyze_basins_of_attraction(multistart_result)
Let largest_basin be Core.get_largest_basin(basin_analysis)
Display "Largest basin of attraction: " joined with Core.describe_basin(largest_basin)
```

## Performance Optimization

### Parallel Line Search
```runa
Note: Parallel evaluation of multiple step sizes
Let parallel_line_search_config be Core.create_parallel_line_search_config([
    ("num_threads", 4),
    ("candidate_steps", [0.1, 0.5, 1.0, 2.0, 5.0]),
    ("evaluation_strategy", "simultaneous")
])

Let parallel_search_result be Core.parallel_line_search(
    objective_function,
    gradient_function,
    current_point,
    search_direction,
    parallel_line_search_config
)

Let best_parallel_step be Core.get_best_parallel_step(parallel_search_result)
Let evaluation_speedup be Core.get_parallel_speedup(parallel_search_result)

Display "Best parallel step size: " joined with best_parallel_step
Display "Parallel speedup: " joined with evaluation_speedup joined with "x"
```

### Vectorized Operations
```runa
Note: SIMD-optimized vector operations for large problems
Core.enable_vectorization(True)
Core.set_vector_instruction_set("AVX2")

Let large_dimension_problem be create_large_scale_problem(dimension: 10000)
Let vectorized_result be Core.lbfgs_optimize_vectorized(
    large_dimension_problem.objective,
    large_dimension_problem.gradient,
    large_dimension_problem.initial_point,
    lbfgs_config
)

Let vectorized_performance be Core.get_vectorization_performance(vectorized_result)
Display "Vectorization speedup: " joined with Core.get_simd_speedup(vectorized_performance) joined with "x"
```

## Error Handling and Robustness

### Numerical Stability
```runa
Note: Handle numerical issues gracefully
Let robust_config be Core.create_robust_optimization_config([
    ("check_conditioning", True),
    ("max_condition_number", 1e12),
    ("regularization_parameter", 1e-10),
    ("step_size_safeguards", True),
    ("gradient_verification", True)
])

Let robust_result be Core.robust_optimize(
    objective_function,
    gradient_function,
    current_point,
    method: "modified_newton",
    robust_config
)

If Core.optimization_successful(robust_result):
    Let robust_solution be Core.get_robust_solution(robust_result)
    Display "Robust optimization successful: " joined with vector_to_string(robust_solution)
Otherwise:
    Let error_diagnosis be Core.diagnose_optimization_failure(robust_result)
    Display "Optimization failed: " joined with Core.get_error_description(error_diagnosis)
    
    Let recovery_suggestions be Core.get_recovery_suggestions(error_diagnosis)
    For suggestion in recovery_suggestions:
        Display "Suggestion: " joined with suggestion
```

### Convergence Verification
```runa
Note: Verify optimality conditions
Let optimality_checker be Core.create_optimality_checker([
    ("gradient_tolerance", 1e-6),
    ("second_order_check", True),
    ("constraint_tolerance", 1e-8)
])

Let solution_verification be Core.verify_solution_optimality(
    optimality_checker,
    objective_function,
    gradient_function,
    hessian_function,
    robust_solution
)

If Core.is_optimal_solution(solution_verification):
    Let optimality_measures be Core.get_optimality_measures(solution_verification)
    Display "Solution verified optimal"
    Display "Gradient norm: " joined with Core.get_gradient_norm(optimality_measures)
    Display "Smallest Hessian eigenvalue: " joined with Core.get_min_hessian_eigenvalue(optimality_measures)
Otherwise:
    Let optimality_violations be Core.get_optimality_violations(solution_verification)
    Display "Optimality conditions violated:"
    For violation in optimality_violations:
        Display "  - " joined with Core.describe_violation(violation)
```

## Best Practices

### Algorithm Selection Guidelines

1. **For Small to Medium Problems (n < 1000)**:
   - Use Newton's method when Hessian is available and positive definite
   - Use BFGS for general nonlinear optimization
   - Use conjugate gradient for quadratic or near-quadratic functions

2. **For Large Problems (n > 1000)**:
   - Use L-BFGS for general nonlinear optimization
   - Use nonlinear conjugate gradient for memory-constrained environments
   - Consider coordinate descent for separable problems

3. **For Ill-Conditioned Problems**:
   - Use trust region methods instead of line search methods
   - Apply preconditioning when possible
   - Consider regularization techniques

### Performance Tips

- **Gradient Computation**: Use automatic differentiation when possible, central differences for numerical gradients
- **Line Search**: Strong Wolfe conditions provide better theoretical guarantees than Armijo alone  
- **Memory Management**: Use L-BFGS for problems where storing the full Hessian is impractical
- **Convergence Monitoring**: Monitor both absolute and relative changes in objective and gradient

This module provides the essential building blocks for optimization algorithms, with robust implementations suitable for production use in scientific and engineering applications.