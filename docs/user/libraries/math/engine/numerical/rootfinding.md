# Root Finding Methods

The Root Finding Methods module (`math/engine/numerical/rootfinding`) provides comprehensive algorithms for solving nonlinear equations and systems of equations. This module implements robust, efficient methods for finding roots (zeros) of functions, including bracketing methods, open methods, polynomial root finding, and nonlinear system solving.

## Quick Start

```runa
Import "math/engine/numerical/rootfinding" as RootFind
Import "math/core/functions" as MathFunctions

Note: Define a simple nonlinear function
Process called "simple_function" that takes x as Real returns Real:
    Return x * x * x - 2.0 * x - 5.0

Note: Bisection method (guaranteed convergence)
Let bisection_result be RootFind.bisection_method(
    simple_function,
    lower_bound: 2.0,
    upper_bound: 3.0,
    tolerance: 1e-10,
    max_iterations: 100
)

Let bisection_root be RootFind.get_root(bisection_result)
Let bisection_iterations be RootFind.get_iterations(bisection_result)

Display "Bisection root: " joined with bisection_root
Display "Converged in: " joined with bisection_iterations joined with " iterations"

Note: Newton-Raphson method (quadratic convergence)
Process called "simple_function_derivative" that takes x as Real returns Real:
    Return 3.0 * x * x - 2.0

Let newton_result be RootFind.newton_raphson_method(
    simple_function,
    simple_function_derivative,
    initial_guess: 2.5,
    tolerance: 1e-12,
    max_iterations: 50
)

Let newton_root be RootFind.get_root(newton_result)
Let newton_iterations be RootFind.get_iterations(newton_result)

Display "Newton-Raphson root: " joined with newton_root
Display "Converged in: " joined with newton_iterations joined with " iterations"

Note: Automatic differentiation for Newton method
Let auto_newton_result be RootFind.newton_raphson_auto_diff(
    simple_function,
    initial_guess: 2.5,
    tolerance: 1e-12
)

Display "Newton with auto-diff root: " joined with RootFind.get_root(auto_newton_result)

Note: Brent's method (combines robustness and speed)
Let brent_result be RootFind.brent_method(
    simple_function,
    lower_bound: 2.0,
    upper_bound: 3.0,
    tolerance: 1e-14
)

Display "Brent's method root: " joined with RootFind.get_root(brent_result)
Display "Function evaluations: " joined with RootFind.get_function_evaluations(brent_result)

Note: Verify all methods found the same root
Let verification be simple_function(bisection_root)
Display "Function value at root: f(" joined with bisection_root joined with ") = " joined with verification
```

## Bracketing Methods

### Bisection Method

```runa
Note: Bisection method - guaranteed convergence for continuous functions
Process called "transcendental_function" that takes x as Real returns Real:
    Return MathFunctions.exp(x) - 3.0 * x

Note: Find initial bracket
Let bracket_search_result be RootFind.find_bracket(
    transcendental_function,
    initial_point: 1.0,
    search_radius: 5.0,
    max_attempts: 100
)

If RootFind.bracket_found(bracket_search_result):
    Let bracket_lower be RootFind.get_bracket_lower(bracket_search_result)
    Let bracket_upper be RootFind.get_bracket_upper(bracket_search_result)
    
    Display "Bracket found: [" joined with bracket_lower joined with ", " joined with bracket_upper joined with "]"
    
    Let detailed_bisection be RootFind.bisection_method_detailed(
        transcendental_function,
        bracket_lower,
        bracket_upper,
        tolerance: 1e-15,
        max_iterations: 100,
        store_iterations: True
    )
    
    Let iteration_history be RootFind.get_iteration_history(detailed_bisection)
    Let convergence_rate be RootFind.estimate_convergence_rate(iteration_history)
    
    Display "Theoretical convergence rate: linear (0.5 per iteration)"
    Display "Observed convergence rate: " joined with convergence_rate
    
    Note: Plot convergence behavior
    For i from 0 to 9:
        Let iteration_data be RootFind.get_iteration_data(iteration_history, i)
        Let interval_width be RootFind.get_interval_width(iteration_data)
        Display "Iteration " joined with i joined with ": interval width = " joined with interval_width

Otherwise:
    Display "No bracket found - function may not have roots in search region"
```

### False Position (Regula Falsi) Method

```runa
Note: False position method - linear interpolation between endpoints
Let false_position_result be RootFind.false_position_method(
    transcendental_function,
    lower_bound: bracket_lower,
    upper_bound: bracket_upper,
    tolerance: 1e-12,
    max_iterations: 100
)

Let false_position_root be RootFind.get_root(false_position_result)
Let false_position_iterations be RootFind.get_iterations(false_position_result)

Display "False position root: " joined with false_position_root
Display "False position iterations: " joined with false_position_iterations

Note: Modified false position (Illinois method)
Let illinois_result be RootFind.illinois_method(
    transcendental_function,
    lower_bound: bracket_lower,
    upper_bound: bracket_upper,
    tolerance: 1e-12
)

Display "Illinois method root: " joined with RootFind.get_root(illinois_result)
Display "Illinois method iterations: " joined with RootFind.get_iterations(illinois_result)

Note: Compare bisection vs false position
Let method_comparison be RootFind.compare_bracketing_methods(
    function: transcendental_function,
    bracket: [bracket_lower, bracket_upper],
    methods: ["bisection", "false_position", "illinois"],
    tolerance: 1e-10
)

For method in ["bisection", "false_position", "illinois"]:
    Let method_stats be RootFind.get_method_stats(method_comparison, method)
    Display method joined with " - iterations: " joined with RootFind.get_method_iterations(method_stats)
        joined with ", accuracy: " joined with RootFind.get_method_accuracy(method_stats)
```

## Open Methods

### Newton-Raphson and Variations

```runa
Note: Newton-Raphson method for various function types
Process called "polynomial_function" that takes x as Real returns Real:
    Return x * x * x * x - 3.0 * x * x + 2.0

Process called "polynomial_derivative" that takes x as Real returns Real:
    Return 4.0 * x * x * x - 6.0 * x

Note: Standard Newton-Raphson
Let newton_standard be RootFind.newton_raphson_method(
    polynomial_function,
    polynomial_derivative,
    initial_guess: 1.5,
    tolerance: 1e-14
)

Display "Standard Newton root: " joined with RootFind.get_root(newton_standard)

Note: Newton-Raphson with line search (for difficult functions)
Let newton_line_search be RootFind.newton_raphson_line_search(
    polynomial_function,
    polynomial_derivative,
    initial_guess: 1.5,
    tolerance: 1e-12,
    line_search_method: "armijo"
)

Let line_search_stats be RootFind.get_line_search_stats(newton_line_search)
Display "Line search steps per iteration: " joined with 
    RootFind.get_average_line_search_steps(line_search_stats)

Note: Modified Newton method for multiple roots
Process called "multiple_root_function" that takes x as Real returns Real:
    Return (x - 1.0) * (x - 1.0) * (x - 2.0)  Note: Double root at x=1

Process called "multiple_root_derivative" that takes x as Real returns Real:
    Return 2.0 * (x - 1.0) * (x - 2.0) + (x - 1.0) * (x - 1.0)

Let modified_newton be RootFind.modified_newton_multiple_roots(
    multiple_root_function,
    multiple_root_derivative,
    initial_guess: 0.5,
    multiplicity: 2,
    tolerance: 1e-10
)

Display "Modified Newton (multiple root): " joined with RootFind.get_root(modified_newton)

Note: Newton method with numerical derivatives
Let newton_numerical_deriv be RootFind.newton_raphson_numerical_derivative(
    polynomial_function,
    initial_guess: 1.5,
    derivative_step_size: 1e-8,
    tolerance: 1e-10
)

Display "Newton with numerical derivative: " joined with RootFind.get_root(newton_numerical_deriv)
```

### Secant and Quasi-Newton Methods

```runa
Note: Secant method - approximates derivative using two points
Let secant_result be RootFind.secant_method(
    polynomial_function,
    initial_point_1: 1.0,
    initial_point_2: 2.0,
    tolerance: 1e-12,
    max_iterations: 100
)

Display "Secant method root: " joined with RootFind.get_root(secant_result)
Display "Secant method iterations: " joined with RootFind.get_iterations(secant_result)

Note: Method of False Position (secant variant)
Let false_position_open be RootFind.false_position_open_method(
    polynomial_function,
    initial_point_1: 1.0,
    initial_point_2: 2.0,
    tolerance: 1e-12
)

Note: Steffensen's method (quadratic convergence without derivatives)
Let steffensen_result be RootFind.steffensen_method(
    polynomial_function,
    initial_guess: 1.5,
    tolerance: 1e-14
)

Display "Steffensen method root: " joined with RootFind.get_root(steffensen_result)
Display "Steffensen convergence order: " joined with 
    RootFind.estimate_convergence_order(RootFind.get_iteration_history(steffensen_result))

Note: Muller's method (handles complex roots)
Let muller_result be RootFind.muller_method(
    polynomial_function,
    initial_point_1: 0.0,
    initial_point_2: 1.0,  
    initial_point_3: 2.0,
    tolerance: 1e-12,
    complex_arithmetic: True
)

Let muller_roots be RootFind.get_all_roots_found(muller_result)
Display "Muller method found " joined with RootFind.count_roots(muller_roots) joined with " roots"
```

### Fixed-Point Iteration

```runa
Note: Fixed-point iteration - solve x = g(x)
Process called "fixed_point_function" that takes x as Real returns Real:
    Note: Solve x^2 - 2x - 3 = 0 by rearranging to x = (x^2 - 3)/2
    Return (x * x - 3.0) / 2.0

Let fixed_point_result be RootFind.fixed_point_iteration(
    fixed_point_function,
    initial_guess: 3.5,
    tolerance: 1e-10,
    max_iterations: 1000
)

If RootFind.converged(fixed_point_result):
    Display "Fixed-point iteration root: " joined with RootFind.get_root(fixed_point_result)
Otherwise:
    Display "Fixed-point iteration did not converge - g'(x) may be > 1"

Note: Aitken acceleration for fixed-point iteration
Let aitken_accelerated be RootFind.fixed_point_aitken_acceleration(
    fixed_point_function,
    initial_guess: 3.5,
    tolerance: 1e-12
)

Display "Aitken accelerated result: " joined with RootFind.get_root(aitken_accelerated)
Display "Acceleration improvement: " joined with 
    (RootFind.get_iterations(fixed_point_result) / RootFind.get_iterations(aitken_accelerated)) joined with "x"

Note: Wegstein method for slowly converging fixed-point problems
Let wegstein_result be RootFind.wegstein_method(
    fixed_point_function,
    initial_guess: 3.5,
    tolerance: 1e-10,
    acceleration_parameter: 0.5
)

Display "Wegstein method root: " joined with RootFind.get_root(wegstein_result)
```

## Polynomial Root Finding

### Classical Polynomial Methods

```runa
Note: Polynomial root finding for various polynomial types
Let quadratic_coeffs be [1.0, -5.0, 6.0]  Note: x^2 - 5x + 6 = 0
Let cubic_coeffs be [1.0, -6.0, 11.0, -6.0]  Note: x^3 - 6x^2 + 11x - 6 = 0
Let quartic_coeffs be [1.0, -10.0, 35.0, -50.0, 24.0]

Note: Quadratic formula
Let quadratic_roots be RootFind.solve_quadratic(quadratic_coeffs)
Display "Quadratic roots: " joined with RootFind.format_roots(quadratic_roots)

Note: Cubic formula (Cardano's method)
Let cubic_roots be RootFind.solve_cubic(cubic_coeffs)
Display "Cubic roots: " joined with RootFind.format_roots(cubic_roots)

Note: Quartic formula (Ferrari's method)
Let quartic_roots be RootFind.solve_quartic(quartic_coeffs)
Display "Quartic roots: " joined with RootFind.format_roots(quartic_roots)

Note: General polynomial - Durand-Kerner method
Let high_degree_coeffs be [1.0, -15.0, 85.0, -225.0, 274.0, -120.0]  Note: degree 5

Let durand_kerner_roots be RootFind.durand_kerner_method(
    high_degree_coeffs,
    max_iterations: 1000,
    tolerance: 1e-12
)

Display "Durand-Kerner roots:"
For i from 0 to (RootFind.get_root_count(durand_kerner_roots) - 1):
    Let root be RootFind.get_root_at_index(durand_kerner_roots, i)
    Display "  Root " joined with (i + 1) joined with ": " joined with RootFind.format_complex_number(root)

Note: Bairstow's method for real coefficients
Let bairstow_roots be RootFind.bairstow_method(
    high_degree_coeffs,
    initial_p: 1.0,
    initial_q: 1.0,
    tolerance: 1e-10
)

Display "Bairstow method found " joined with RootFind.get_root_count(bairstow_roots) joined with " roots"
```

### Advanced Polynomial Techniques

```runa
Note: Aberth-Ehrlich method (simultaneous iteration)
Let aberth_roots be RootFind.aberth_ehrlich_method(
    high_degree_coeffs,
    initial_approximations: "automatic",
    tolerance: 1e-14,
    max_iterations: 200
)

Let aberth_convergence be RootFind.analyze_convergence(aberth_roots)
Display "Aberth method convergence rate: " joined with 
    RootFind.get_average_convergence_rate(aberth_convergence)

Note: Jenkins-Traub method (three-stage algorithm)
Let jenkins_traub_roots be RootFind.jenkins_traub_method(
    high_degree_coeffs,
    tolerance: 1e-12
)

Display "Jenkins-Traub method accuracy: " joined with 
    RootFind.verify_polynomial_roots(high_degree_coeffs, jenkins_traub_roots)

Note: Laguerre's method (global convergence)
Let laguerre_root be RootFind.laguerre_method(
    high_degree_coeffs,
    initial_guess: RootFind.create_complex_number(1.0, 1.0),
    tolerance: 1e-12
)

Display "Laguerre method single root: " joined with RootFind.format_complex_number(laguerre_root)

Note: Polynomial deflation for finding all roots
Let polynomial_deflation_result be RootFind.polynomial_deflation_all_roots(
    high_degree_coeffs,
    root_finding_method: "laguerre",
    deflation_method: "synthetic_division",
    tolerance: 1e-10
)

Let all_deflated_roots be RootFind.get_all_deflated_roots(polynomial_deflation_result)
Let deflation_accuracy be RootFind.check_deflation_accuracy(polynomial_deflation_result)

Display "Deflation method found " joined with RootFind.get_root_count(all_deflated_roots) joined with " roots"
Display "Deflation accuracy maintained: " joined with deflation_accuracy
```

### Polynomial Root Properties and Analysis

```runa
Note: Analyze polynomial root properties
Let root_analyzer be RootFind.create_polynomial_root_analyzer(high_degree_coeffs)

Let root_bounds be RootFind.compute_root_bounds(root_analyzer, method: "cauchy")
Let root_count_estimates be RootFind.estimate_root_counts(root_analyzer)

Display "Root bounds (Cauchy): " joined with RootFind.format_bounds(root_bounds)
Display "Positive real roots (Descartes): " joined with 
    RootFind.get_positive_real_root_count(root_count_estimates)
Display "Negative real roots: " joined with 
    RootFind.get_negative_real_root_count(root_count_estimates)

Note: Root sensitivity analysis
Let sensitivity_analysis be RootFind.polynomial_sensitivity_analysis(
    high_degree_coeffs,
    coefficient_perturbations: [1e-10, 1e-8, 1e-6],
    num_perturbations: 100
)

Let most_sensitive_root be RootFind.get_most_sensitive_root(sensitivity_analysis)
Let condition_numbers be RootFind.get_root_condition_numbers(sensitivity_analysis)

Display "Most sensitive root index: " joined with most_sensitive_root
Display "Average root condition number: " joined with 
    RootFind.get_average_condition_number(condition_numbers)
```

## Nonlinear System Solving

### Newton Methods for Systems

```runa
Import "math/engine/linalg/core" as LinAlg

Note: Newton-Raphson for systems of nonlinear equations
Process called "nonlinear_system" that takes variables as Vector returns Vector:
    Let x be LinAlg.get_element(variables, 0)
    Let y be LinAlg.get_element(variables, 1)
    
    Let f1 be x * x + y * y - 1.0     Note: Circle equation
    Let f2 be x - y * y               Note: Parabola equation
    
    Return LinAlg.create_vector([f1, f2])

Process called "system_jacobian" that takes variables as Vector returns Matrix:
    Let x be LinAlg.get_element(variables, 0)
    Let y be LinAlg.get_element(variables, 1)
    
    Note: Jacobian matrix [∂f1/∂x ∂f1/∂y; ∂f2/∂x ∂f2/∂y]
    Return LinAlg.create_matrix([
        [2.0 * x, 2.0 * y],
        [1.0, -2.0 * y]
    ])

Let system_newton_result be RootFind.newton_raphson_system(
    nonlinear_system,
    system_jacobian,
    initial_guess: LinAlg.create_vector([0.5, 0.5]),
    tolerance: 1e-12,
    max_iterations: 100
)

Let system_solution be RootFind.get_system_solution(system_newton_result)
Display "System solution: x = " joined with LinAlg.get_element(system_solution, 0)
    joined with ", y = " joined with LinAlg.get_element(system_solution, 1)

Note: Verify solution
Let verification_residual be nonlinear_system(system_solution)
Let residual_norm be LinAlg.vector_norm(verification_residual, "euclidean")
Display "Residual norm: " joined with residual_norm

Note: Newton method with finite difference Jacobian
Let newton_fd_result be RootFind.newton_raphson_system_finite_diff(
    nonlinear_system,
    initial_guess: LinAlg.create_vector([0.7, 0.3]),
    tolerance: 1e-10,
    finite_diff_step: 1e-8
)

Display "Newton FD solution: " joined with 
    LinAlg.vector_to_string(RootFind.get_system_solution(newton_fd_result))
```

### Quasi-Newton Methods for Systems

```runa
Note: Broyden's method (quasi-Newton for systems)
Let broyden_result be RootFind.broyden_method(
    nonlinear_system,
    initial_guess: LinAlg.create_vector([0.6, 0.4]),
    initial_jacobian_approximation: LinAlg.create_identity_matrix(2),
    tolerance: 1e-10
)

Display "Broyden method solution: " joined with 
    LinAlg.vector_to_string(RootFind.get_system_solution(broyden_result))

Let broyden_jacobian_updates be RootFind.get_jacobian_update_count(broyden_result)
Display "Jacobian updates in Broyden: " joined with broyden_jacobian_updates

Note: BFGS method for nonlinear systems
Let bfgs_result be RootFind.bfgs_nonlinear_system(
    nonlinear_system,
    initial_guess: LinAlg.create_vector([0.4, 0.6]),
    tolerance: 1e-12
)

Display "BFGS solution: " joined with 
    LinAlg.vector_to_string(RootFind.get_system_solution(bfgs_result))

Note: Compare system solving methods
Let system_method_comparison be RootFind.compare_system_methods(
    system_function: nonlinear_system,
    jacobian_function: system_jacobian,
    initial_guess: LinAlg.create_vector([0.5, 0.5]),
    methods: ["newton_raphson", "broyden", "bfgs"],
    tolerance: 1e-10
)

For method in ["newton_raphson", "broyden", "bfgs"]:
    Let method_performance be RootFind.get_system_method_performance(system_method_comparison, method)
    Display method joined with " - iterations: " joined with 
        RootFind.get_system_iterations(method_performance) joined with 
        ", function evaluations: " joined with 
        RootFind.get_system_function_evaluations(method_performance)
```

### Advanced System Solving Techniques

```runa
Note: Trust region methods for robust convergence
Let trust_region_result be RootFind.trust_region_dogleg_method(
    nonlinear_system,
    system_jacobian,
    initial_guess: LinAlg.create_vector([0.8, 0.2]),
    initial_trust_radius: 1.0,
    tolerance: 1e-12
)

Let trust_region_path be RootFind.get_optimization_path(trust_region_result)
Let final_trust_radius be RootFind.get_final_trust_radius(trust_region_result)

Display "Trust region final radius: " joined with final_trust_radius
Display "Trust region iterations: " joined with LinAlg.vector_length(trust_region_path)

Note: Continuation (homotopy) methods
Process called "homotopy_function" that takes variables as Vector, parameter as Real returns Vector:
    Let x be LinAlg.get_element(variables, 0)
    Let y be LinAlg.get_element(variables, 1)
    Let t be parameter
    
    Note: H(x,y,t) = (1-t)*F_simple(x,y) + t*F_target(x,y)
    Let simple_f1 be x - 1.0
    Let simple_f2 be y - 1.0
    
    Let target_f1 be x * x + y * y - 1.0
    Let target_f2 be x - y * y
    
    Let f1 be (1.0 - t) * simple_f1 + t * target_f1
    Let f2 be (1.0 - t) * simple_f2 + t * target_f2
    
    Return LinAlg.create_vector([f1, f2])

Let continuation_result be RootFind.continuation_method(
    homotopy_function,
    initial_solution: LinAlg.create_vector([1.0, 1.0]),
    parameter_start: 0.0,
    parameter_end: 1.0,
    step_size: 0.1,
    tolerance: 1e-8
)

Let continuation_path be RootFind.get_continuation_path(continuation_result)
Let final_solution be RootFind.get_final_continuation_solution(continuation_result)

Display "Continuation method final solution: " joined with 
    LinAlg.vector_to_string(final_solution)

Note: Multiple root finding for systems
Let multiple_system_roots be RootFind.find_multiple_system_roots(
    nonlinear_system,
    search_region: [[-2.0, 2.0], [-2.0, 2.0]],
    num_initial_guesses: 25,
    clustering_tolerance: 1e-6
)

Let unique_roots be RootFind.get_unique_system_roots(multiple_system_roots)
Display "Found " joined with RootFind.count_unique_roots(unique_roots) joined with " unique system roots"

For i from 0 to (RootFind.count_unique_roots(unique_roots) - 1):
    Let root_i be RootFind.get_unique_root(unique_roots, i)
    Display "Root " joined with (i + 1) joined with ": " joined with LinAlg.vector_to_string(root_i)
```

## Specialized Root Finding Applications

### Optimization-Based Root Finding

```runa
Import "math/engine/numerical/optimization" as Optimization

Note: Convert root finding to optimization problem
Process called "root_finding_objective" that takes x as Real returns Real:
    Let function_value be simple_function(x)
    Return function_value * function_value  Note: Minimize |f(x)|^2

Let optimization_root be Optimization.minimize_scalar(
    root_finding_objective,
    bounds: [2.0, 3.0],
    method: "golden_section",
    tolerance: 1e-12
)

Let opt_based_root be Optimization.get_minimizer(optimization_root)
Let opt_objective_value be Optimization.get_minimum_value(optimization_root)

Display "Optimization-based root: " joined with opt_based_root
Display "Objective value (should be ~0): " joined with opt_objective_value

Note: Multi-objective root finding (find multiple roots simultaneously)
Let multi_objective_result be RootFind.multi_objective_root_finding(
    simple_function,
    search_intervals: [[0.0, 1.0], [2.0, 3.0], [3.0, 4.0]],
    optimization_method: "particle_swarm",
    tolerance: 1e-10
)

Let all_found_roots be RootFind.get_all_found_roots(multi_objective_result)
Display "Multi-objective found " joined with RootFind.count_roots(all_found_roots) joined with " roots"
```

### Stochastic Root Finding

```runa
Note: Stochastic methods for difficult root finding problems
Let stochastic_root_finder be RootFind.create_stochastic_root_finder([
    ("method", "simulated_annealing"),
    ("initial_temperature", 100.0),
    ("cooling_rate", 0.95),
    ("max_iterations", 10000)
])

Process called "difficult_function" that takes x as Real returns Real:
    Note: Function with many local minima
    Return MathFunctions.sin(10.0 * x) * MathFunctions.exp(-x * x) + 0.5 * x - 0.3

Let stochastic_result be RootFind.stochastic_root_search(
    stochastic_root_finder,
    difficult_function,
    search_domain: [-2.0, 2.0],
    target_tolerance: 1e-8
)

Let stochastic_roots be RootFind.get_stochastic_roots(stochastic_result)
Display "Stochastic method found " joined with RootFind.count_roots(stochastic_roots) joined with " roots"

Note: Genetic algorithm for root finding
Let genetic_root_finder be RootFind.create_genetic_algorithm_root_finder([
    ("population_size", 100),
    ("mutation_rate", 0.1),
    ("crossover_rate", 0.8),
    ("max_generations", 500)
])

Let genetic_result be RootFind.genetic_algorithm_root_search(
    genetic_root_finder,
    difficult_function,
    search_bounds: [-2.0, 2.0]
)

Display "Genetic algorithm root: " joined with RootFind.get_best_root(genetic_result)
```

### Interval Root Finding

```runa
Import "math/engine/numerical/core" as Numerical

Note: Interval Newton method for guaranteed root bounds
Process called "interval_function" that takes x_interval as Interval returns Interval:
    Let x_squared be Numerical.interval_power(x_interval, 2)
    Let two_x be Numerical.interval_multiply(Numerical.create_interval(2.0, 2.0), x_interval)
    Let five_interval be Numerical.create_interval(5.0, 5.0)
    Return Numerical.interval_subtract(Numerical.interval_subtract(x_squared, two_x), five_interval)

Let interval_newton_result be RootFind.interval_newton_method(
    interval_function,
    initial_interval: Numerical.create_interval(2.0, 3.0),
    tolerance: 1e-10,
    max_iterations: 100
)

Let guaranteed_root_bounds be RootFind.get_guaranteed_bounds(interval_newton_result)
Display "Guaranteed root bounds: [" joined with Numerical.get_interval_lower(guaranteed_root_bounds)
    joined with ", " joined with Numerical.get_interval_upper(guaranteed_root_bounds) joined with "]"

Note: Interval bisection with rigorous error bounds
Let interval_bisection_result be RootFind.interval_bisection_method(
    interval_function,
    initial_interval: Numerical.create_interval(2.0, 3.0),
    target_width: 1e-12
)

Let certified_bounds be RootFind.get_certified_root_bounds(interval_bisection_result)
Let bounds_width be Numerical.interval_width(certified_bounds)

Display "Certified root bounds width: " joined with bounds_width
Display "Root is guaranteed to be in: [" 
    joined with Numerical.get_interval_lower(certified_bounds)
    joined with ", " joined with Numerical.get_interval_upper(certified_bounds) joined with "]"
```

## Performance Analysis and Optimization

### Convergence Rate Analysis

```runa
Note: Analyze and compare convergence rates of different methods
Let convergence_analyzer be RootFind.create_convergence_analyzer()

Let test_functions be [
    ("polynomial", simple_function),
    ("transcendental", transcendental_function),
    ("oscillatory", difficult_function)
]

Let methods_to_test be [
    "bisection",
    "newton_raphson", 
    "secant",
    "brent"
]

Let convergence_study = RootFind.comprehensive_convergence_study(
    convergence_analyzer,
    test_functions: test_functions,
    methods: methods_to_test,
    tolerance_levels: [1e-6, 1e-10, 1e-14]
)

For function_name in ["polynomial", "transcendental", "oscillatory"]:
    Display "Function: " joined with function_name
    
    For method in methods_to_test:
        Let method_performance be RootFind.get_method_performance(convergence_study, function_name, method)
        
        If RootFind.method_converged(method_performance):
            Let avg_iterations be RootFind.get_average_iterations(method_performance)
            Let convergence_order be RootFind.get_observed_convergence_order(method_performance)
            
            Display "  " joined with method joined with ": " 
                joined with avg_iterations joined with " iterations, order " 
                joined with convergence_order
        Otherwise:
            Display "  " joined with method joined with ": failed to converge"
```

### Algorithm Selection and Adaptation

```runa
Note: Intelligent algorithm selection based on problem characteristics
Let algorithm_selector be RootFind.create_algorithm_selector([
    ("function_smoothness_analysis", True),
    ("derivative_availability_check", True), 
    ("bracket_existence_test", True),
    ("convergence_requirement_analysis", True)
])

Process called "algorithm_test_function" that takes x as Real returns Real:
    Return MathFunctions.tan(x) - x  Note: Many roots, some difficult

Let function_analysis be RootFind.analyze_function_characteristics(
    algorithm_selector,
    algorithm_test_function,
    analysis_interval: [0.0, 10.0]
)

Let recommended_method be RootFind.get_recommended_method(function_analysis)
Let backup_methods be RootFind.get_backup_methods(function_analysis)

Display "Recommended method: " joined with recommended_method
Display "Backup methods: " joined with RootFind.format_method_list(backup_methods)

Note: Adaptive root finding with automatic method switching
Let adaptive_result be RootFind.adaptive_root_finding(
    algorithm_test_function,
    search_region: [3.0, 3.5],  Note: Region with a root
    convergence_criteria: [
        ("tolerance", 1e-12),
        ("max_iterations", 100),
        ("max_function_evaluations", 200)
    ],
    method_switching_enabled: True
)

Let methods_used be RootFind.get_methods_used(adaptive_result)
Let method_switch_points be RootFind.get_method_switch_points(adaptive_result)

Display "Adaptive result: " joined with RootFind.get_root(adaptive_result)
Display "Methods used: " joined with RootFind.format_method_sequence(methods_used)
Display "Method switches at iterations: " joined with 
    RootFind.format_switch_points(method_switch_points)
```

## Error Analysis and Robustness

### Root Finding Error Analysis

```runa
Note: Comprehensive error analysis for root finding
Let error_analyzer be RootFind.create_error_analyzer([
    ("forward_error", True),
    ("backward_error", True),
    ("condition_number", True),
    ("sensitivity_analysis", True)
])

Let root_error_analysis be RootFind.analyze_root_finding_errors(
    error_analyzer,
    function: simple_function,
    derivative: simple_function_derivative,
    computed_root: newton_root,
    method: "newton_raphson"
)

Let forward_error be RootFind.get_forward_error(root_error_analysis)
Let backward_error be RootFind.get_backward_error(root_error_analysis)
Let condition_number be RootFind.get_root_condition_number(root_error_analysis)

Display "Forward error: " joined with forward_error
Display "Backward error: " joined with backward_error  
Display "Root condition number: " joined with condition_number

Note: Sensitivity to function perturbations
Let sensitivity_study be RootFind.function_perturbation_sensitivity(
    simple_function,
    newton_root,
    perturbation_levels: [1e-10, 1e-8, 1e-6],
    num_perturbations: 50
)

Let max_root_change be RootFind.get_max_root_change(sensitivity_study)
Let average_sensitivity be RootFind.get_average_sensitivity(sensitivity_study)

Display "Maximum root change: " joined with max_root_change
Display "Average sensitivity: " joined with average_sensitivity
```

### Robust Root Finding Strategies

```runa
Import "core/error_handling" as ErrorHandling

Note: Failsafe root finding with multiple fallback methods
Let robust_root_finder be RootFind.create_robust_root_finder([
    ("primary_method", "brent"),
    ("fallback_methods", ["bisection", "newton_raphson", "secant"]),
    ("convergence_criteria", [
        ("absolute_tolerance", 1e-12),
        ("relative_tolerance", 1e-10),
        ("max_iterations", 1000)
    ]),
    ("robustness_checks", [
        ("overflow_detection", True),
        ("nan_detection", True),
        ("convergence_stagnation", True)
    ])
])

Let robust_result be RootFind.robust_root_search(
    robust_root_finder,
    simple_function,
    initial_info: [("bracket", [2.0, 3.0]), ("initial_guess", 2.5)]
)

If ErrorHandling.is_success(robust_result):
    Let final_root be ErrorHandling.get_result(robust_result)
    Let method_used be RootFind.get_successful_method(robust_result)
    Let robustness_report be RootFind.get_robustness_report(robust_result)
    
    Display "Robust root finding successful: " joined with final_root
    Display "Method used: " joined with method_used
    Display "Robustness issues encountered: " joined with 
        RootFind.count_robustness_issues(robustness_report)
Otherwise:
    Let failure_analysis be ErrorHandling.get_failure_analysis(robust_result)
    Display "All methods failed. Analysis: " joined with 
        RootFind.format_failure_analysis(failure_analysis)
```

## Integration Examples

### With Optimization Methods

```runa
Import "math/engine/numerical/optimization" as Optimization

Note: Root finding in optimization contexts
Process called "optimization_gradient" that takes x as Real returns Real:
    Return 2.0 * x * x * x - 6.0 * x * x + 6.0 * x - 2.0  Note: Derivative of some objective

Let critical_points be RootFind.find_critical_points(
    optimization_gradient,
    search_interval: [-2.0, 4.0],
    method: "multiple_shooting"
)

Display "Found " joined with RootFind.count_critical_points(critical_points) joined with " critical points:"
For i from 0 to (RootFind.count_critical_points(critical_points) - 1):
    Let critical_point be RootFind.get_critical_point(critical_points, i)
    Display "  x = " joined with critical_point
```

### With Differential Equations

```runa
Import "math/engine/numerical/ode" as ODE

Note: Root finding in shooting methods for boundary value problems
Process called "ode_system" that takes t as Real, y as Vector returns Vector:
    Let y1 be LinAlg.get_element(y, 0)
    Let y2 be LinAlg.get_element(y, 1)
    Return LinAlg.create_vector([y2, -y1])  Note: Simple harmonic oscillator

Process called "shooting_residual" that takes initial_slope as Real returns Real:
    Let initial_condition be LinAlg.create_vector([0.0, initial_slope])
    Let ode_solution be ODE.runge_kutta_solve(
        ode_system,
        t_start: 0.0,
        t_end: 3.14159,  Note: π
        y_initial: initial_condition,
        step_size: 0.01
    )
    
    Let final_value be ODE.get_final_value(ode_solution)
    Return LinAlg.get_element(final_value, 0)  Note: Should be 0 for boundary condition

Let shooting_method_result be RootFind.secant_method(
    shooting_residual,
    initial_point_1: 0.5,
    initial_point_2: 1.5,
    tolerance: 1e-10
)

Let correct_initial_slope be RootFind.get_root(shooting_method_result)
Display "Shooting method initial slope: " joined with correct_initial_slope
```

## Best Practices

### Method Selection Guidelines

```runa
Note: Guidelines for choosing appropriate root-finding methods
Let method_selection_guide be RootFind.create_method_selection_guide([
    ("function_properties", [
        ("smoothness", "check_derivatives"),
        ("monotonicity", "analyze_behavior"),
        ("multiplicity", "detect_multiple_roots")
    ]),
    ("computational_constraints", [
        ("function_evaluations", "minimize_calls"),
        ("derivative_availability", "check_analytical"),
        ("precision_requirements", "set_tolerances")
    ]),
    ("robustness_requirements", [
        ("convergence_guarantee", "use_bracketing"),
        ("global_search", "multiple_initial_guesses"),
        ("error_handling", "implement_fallbacks")
    ])
])

Let selection_recommendation be RootFind.recommend_method(
    method_selection_guide,
    function_characteristics: [
        ("smooth", True),
        ("derivative_available", False),
        ("bracket_known", True),
        ("high_precision_needed", True)
    ]
)

Display "Method selection recommendation:"
Display RootFind.format_recommendation(selection_recommendation)
```

### Performance Optimization

```runa
Note: Optimize root-finding performance
Let performance_optimizer be RootFind.create_performance_optimizer([
    ("function_evaluation_caching", True),
    ("derivative_approximation_reuse", True),
    ("convergence_acceleration", True),
    ("parallel_processing", True)
])

Let optimized_root_finder be RootFind.create_optimized_root_finder(
    performance_optimizer,
    base_method: "newton_raphson",
    target_function: simple_function
)

Let performance_comparison be RootFind.compare_performance(
    standard_method: "newton_raphson",
    optimized_method: optimized_root_finder,
    test_problems: standard_test_functions,
    metrics: ["execution_time", "function_evaluations", "memory_usage"]
)

Let performance_improvement be RootFind.get_performance_improvement(performance_comparison)
Display "Performance improvement: " joined with performance_improvement joined with "x speedup"
```

The Root Finding Methods module provides robust, efficient algorithms for solving nonlinear equations across all domains of scientific and engineering computation, with comprehensive error analysis, adaptive method selection, and performance optimization capabilities.