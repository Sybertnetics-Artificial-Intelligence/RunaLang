# Numerical Integration

The Numerical Integration module (`math/engine/numerical/integration`) provides comprehensive algorithms for numerical quadrature and cubature. This module implements Newton-Cotes formulas, Gaussian quadrature, adaptive integration methods, Monte Carlo techniques, and specialized algorithms for computing definite integrals, improper integrals, and multidimensional integrals essential for scientific computing and mathematical analysis.

## Quick Start

```runa
Import "math/engine/numerical/integration" as Integration
Import "math/core/functions" as MathFunctions
Import "math/core/constants" as Constants

Note: Define test functions for integration
Process called "simple_polynomial" that takes x as Real returns Real:
    Return x * x * x + 2.0 * x * x - x + 3.0

Process called "trigonometric_function" that takes x as Real returns Real:
    Return MathFunctions.sin(x) * MathFunctions.exp(-x)

Note: Trapezoidal rule (basic method)
Let trapezoidal_result be Integration.trapezoidal_rule(
    simple_polynomial,
    lower_bound: 0.0,
    upper_bound: 2.0,
    num_intervals: 100
)

Display "Trapezoidal rule result: " joined with trapezoidal_result

Note: Simpson's rule (higher accuracy)
Let simpson_result be Integration.simpson_rule(
    simple_polynomial,
    lower_bound: 0.0,
    upper_bound: 2.0,
    num_intervals: 100
)

Display "Simpson's rule result: " joined with simpson_result

Note: Exact integral for comparison: ∫₀² (x³ + 2x² - x + 3) dx
Let exact_integral be (2.0**4)/4.0 + 2.0*(2.0**3)/3.0 - (2.0**2)/2.0 + 3.0*2.0
    - (0.0**4/4.0 + 2.0*(0.0**3)/3.0 - (0.0**2)/2.0 + 3.0*0.0)
Display "Exact integral: " joined with exact_integral

Note: Gaussian quadrature (optimal points and weights)
Let gauss_legendre_result be Integration.gauss_legendre_quadrature(
    simple_polynomial,
    lower_bound: 0.0,
    upper_bound: 2.0,
    order: 5
)

Display "Gauss-Legendre (order 5): " joined with gauss_legendre_result

Note: Adaptive quadrature with error control
Let adaptive_result be Integration.adaptive_quadrature(
    trigonometric_function,
    lower_bound: 0.0,
    upper_bound: 4.0,
    tolerance: 1e-8,
    max_subdivisions: 1000
)

Let adaptive_value be Integration.get_integral_value(adaptive_result)
Let adaptive_error = Integration.get_error_estimate(adaptive_result)
Let subdivisions_used be Integration.get_subdivisions_used(adaptive_result)

Display "Adaptive quadrature: " joined with adaptive_value 
    joined with " ± " joined with adaptive_error
Display "Subdivisions used: " joined with subdivisions_used

Note: Monte Carlo integration for comparison
Let monte_carlo_result be Integration.monte_carlo_integration(
    trigonometric_function,
    lower_bound: 0.0,
    upper_bound: 4.0,
    num_samples: 100000
)

Let mc_value be Integration.get_monte_carlo_value(monte_carlo_result)
Let mc_error be Integration.get_monte_carlo_error(monte_carlo_result)

Display "Monte Carlo: " joined with mc_value joined with " ± " joined with mc_error
```

## Newton-Cotes Integration Formulas

### Basic Newton-Cotes Rules

```runa
Note: Compare different Newton-Cotes formulas
Process called "test_integrand" that takes x as Real returns Real:
    Return MathFunctions.exp(-x * x)  Note: Gaussian function

Let integration_bounds be [0.0, 1.0]
Let exact_gaussian_integral be 0.746824132812427  Note: Known value for reference

Note: Rectangle rule (lowest order)
Let rectangle_left be Integration.rectangle_rule_left(
    test_integrand,
    integration_bounds[0],
    integration_bounds[1],
    num_intervals: 1000
)

Let rectangle_right be Integration.rectangle_rule_right(
    test_integrand,
    integration_bounds[0],
    integration_bounds[1], 
    num_intervals: 1000
)

Let rectangle_midpoint be Integration.rectangle_rule_midpoint(
    test_integrand,
    integration_bounds[0],
    integration_bounds[1],
    num_intervals: 1000
)

Display "Rectangle rule comparisons (n=1000):"
Display "Left endpoint: " joined with rectangle_left 
    joined with " (error: " joined with Integration.abs(rectangle_left - exact_gaussian_integral) joined with ")"
Display "Right endpoint: " joined with rectangle_right
    joined with " (error: " joined with Integration.abs(rectangle_right - exact_gaussian_integral) joined with ")"
Display "Midpoint: " joined with rectangle_midpoint
    joined with " (error: " joined with Integration.abs(rectangle_midpoint - exact_gaussian_integral) joined with ")"

Note: Higher-order Newton-Cotes formulas
Let simpson_38_result be Integration.simpson_3_8_rule(
    test_integrand,
    integration_bounds[0],
    integration_bounds[1],
    num_intervals: 300  Note: Must be divisible by 3
)

Let boole_result be Integration.boole_rule(
    test_integrand,
    integration_bounds[0],
    integration_bounds[1],
    num_intervals: 400  Note: Must be divisible by 4
)

Display "Higher-order Newton-Cotes:"
Display "Simpson's 3/8 rule: " joined with simpson_38_result
    joined with " (error: " joined with Integration.abs(simpson_38_result - exact_gaussian_integral) joined with ")"
Display "Boole's rule: " joined with boole_result
    joined with " (error: " joined with Integration.abs(boole_result - exact_gaussian_integral) joined with ")"
```

### Composite and Adaptive Newton-Cotes

```runa
Note: Convergence analysis of composite rules
Let interval_counts be [10, 20, 40, 80, 160, 320]
Let trapezoidal_errors be []
Let simpson_errors be []

Display "Convergence analysis:"
Display "n | Trapezoidal Error | Simpson Error"

For n in interval_counts:
    Let trap_result be Integration.trapezoidal_rule(test_integrand, 0.0, 1.0, n)
    Let simp_result be Integration.simpson_rule(test_integrand, 0.0, 1.0, n)
    
    Let trap_error be Integration.abs(trap_result - exact_gaussian_integral)
    Let simp_error be Integration.abs(simp_result - exact_gaussian_integral)
    
    Integration.append_to_list(trapezoidal_errors, trap_error)
    Integration.append_to_list(simpson_errors, simp_error)
    
    Display n joined with " | " joined with trap_error joined with " | " joined with simp_error

Note: Estimate convergence rates
Let trap_convergence_rate be Integration.estimate_convergence_rate(trapezoidal_errors, interval_counts)
Let simp_convergence_rate be Integration.estimate_convergence_rate(simpson_errors, interval_counts)

Display "Estimated convergence rates:"
Display "Trapezoidal: O(h^" joined with trap_convergence_rate joined with ")"
Display "Simpson: O(h^" joined with simp_convergence_rate joined with ")"

Note: Adaptive Simpson's method
Let adaptive_simpson be Integration.adaptive_simpson(
    test_integrand,
    lower_bound: 0.0,
    upper_bound: 1.0,
    tolerance: 1e-10,
    max_recursion_depth: 15
)

Let adaptive_simpson_value be Integration.get_adaptive_value(adaptive_simpson)
Let adaptive_simpson_evals be Integration.get_function_evaluations(adaptive_simpson)
Let recursion_depth_used be Integration.get_max_depth_reached(adaptive_simpson)

Display "Adaptive Simpson results:"
Display "Value: " joined with adaptive_simpson_value
Display "Function evaluations: " joined with adaptive_simpson_evals
Display "Maximum recursion depth: " joined with recursion_depth_used
```

## Gaussian Quadrature Methods

### Classical Gaussian Quadrature

```runa
Note: Compare different Gaussian quadrature orders
Let gaussian_orders be [2, 4, 6, 8, 10, 12]

Display "Gaussian quadrature accuracy comparison:"
Display "Order | Result | Error"

For order in gaussian_orders:
    Let gauss_result be Integration.gauss_legendre_quadrature(
        test_integrand,
        lower_bound: 0.0,
        upper_bound: 1.0,
        order: order
    )
    
    Let gauss_error be Integration.abs(gauss_result - exact_gaussian_integral)
    Display order joined with " | " joined with gauss_result joined with " | " joined with gauss_error

Note: Gauss-Chebyshev quadrature for oscillatory integrands
Process called "oscillatory_integrand" that takes x as Real returns Real:
    Return MathFunctions.cos(10.0 * x) / MathFunctions.sqrt(1.0 - x * x)

Let gauss_chebyshev_result be Integration.gauss_chebyshev_quadrature(
    oscillatory_integrand,
    order: 20
)

Display "Gauss-Chebyshev for oscillatory function: " joined with gauss_chebyshev_result

Note: Gauss-Laguerre for semi-infinite integrals
Process called "exponential_decay_integrand" that takes x as Real returns Real:
    Return x * x  Note: Will be multiplied by e^(-x) by the method

Let gauss_laguerre_result be Integration.gauss_laguerre_quadrature(
    exponential_decay_integrand,
    order: 15
)

Display "Gauss-Laguerre for ∫₀^∞ x²e^(-x) dx: " joined with gauss_laguerre_result
Display "Exact value: 2.0"

Note: Gauss-Hermite for infinite integrals
Process called "polynomial_with_gaussian_weight" that takes x as Real returns Real:
    Return x * x  Note: Will be multiplied by e^(-x²) by the method

Let gauss_hermite_result be Integration.gauss_hermite_quadrature(
    polynomial_with_gaussian_weight,
    order: 10
)

Display "Gauss-Hermite for ∫₋∞^∞ x²e^(-x²) dx: " joined with gauss_hermite_result
Display "Exact value: " joined with (MathFunctions.sqrt(Constants.get_pi()) / 2.0)
```

### Adaptive Gaussian Quadrature

```runa
Note: Gauss-Kronrod adaptive integration
Process called "challenging_integrand" that takes x as Real returns Real:
    If x == 0.5:
        Return 1.0  Note: Handle potential singularity
    Otherwise:
        Return MathFunctions.abs(x - 0.5)**(-0.3)

Let gauss_kronrod_result be Integration.gauss_kronrod_adaptive(
    challenging_integrand,
    lower_bound: 0.0,
    upper_bound: 1.0,
    tolerance: 1e-6,
    max_subdivisions: 100
)

Let gk_value be Integration.get_gk_integral_value(gauss_kronrod_result)
Let gk_error_estimate be Integration.get_gk_error_estimate(gauss_kronrod_result)
Let gk_subdivisions be Integration.get_gk_subdivisions_used(gauss_kronrod_result)

Display "Gauss-Kronrod adaptive results:"
Display "Integral value: " joined with gk_value
Display "Error estimate: " joined with gk_error_estimate
Display "Subdivisions used: " joined with gk_subdivisions

Note: Doubly adaptive quadrature
Let doubly_adaptive_result be Integration.doubly_adaptive_quadrature(
    challenging_integrand,
    lower_bound: 0.0,
    upper_bound: 1.0,
    absolute_tolerance: 1e-8,
    relative_tolerance: 1e-6,
    initial_subdivisions: 4
)

Let da_performance_metrics be Integration.get_performance_metrics(doubly_adaptive_result)
Display "Doubly adaptive performance:"
Display Integration.format_performance_metrics(da_performance_metrics)
```

## Multidimensional Integration

### Double and Triple Integrals

```runa
Note: Double integral using nested 1D quadrature
Process called "double_integral_function" that takes x as Real, y as Real returns Real:
    Return x * x + y * y

Let double_integral_nested = Integration.double_integral_nested(
    double_integral_function,
    x_bounds: [0.0, 1.0],
    y_bounds: [0.0, 2.0],
    x_method: "simpson",
    y_method: "simpson",
    x_intervals: 50,
    y_intervals: 50
)

Let exact_double_integral be (1.0/3.0) * 2.0 + (1.0) * (8.0/3.0)  Note: ∫∫(x²+y²)dydx
Display "Double integral (nested): " joined with double_integral_nested
Display "Exact double integral: " joined with exact_double_integral

Note: Monte Carlo double integration
Let mc_double_integral be Integration.monte_carlo_2d(
    double_integral_function,
    x_bounds: [0.0, 1.0],
    y_bounds: [0.0, 2.0],
    num_samples: 1000000
)

Display "Monte Carlo double integral: " joined with Integration.get_mc_2d_value(mc_double_integral)
    joined with " ± " joined with Integration.get_mc_2d_error(mc_double_integral)

Note: Triple integral
Process called "triple_integral_function" that takes x as Real, y as Real, z as Real returns Real:
    Return x * y * z

Let triple_integral_result be Integration.triple_integral_nested(
    triple_integral_function,
    x_bounds: [0.0, 1.0],
    y_bounds: [0.0, 1.0], 
    z_bounds: [0.0, 1.0],
    method: "gauss_legendre",
    order: 4
)

Display "Triple integral result: " joined with triple_integral_result
Display "Exact triple integral: 0.125"
```

### Cubature Methods

```runa
Import "math/engine/linalg/core" as LinAlg

Note: Adaptive cubature for multidimensional integration
Process called "multidimensional_function" that takes variables as Vector returns Real:
    Let x be LinAlg.get_element(variables, 0)
    Let y be LinAlg.get_element(variables, 1)
    Let z be LinAlg.get_element(variables, 2)
    Return MathFunctions.exp(-(x*x + y*y + z*z))

Let integration_region be [
    [-2.0, 2.0],  Note: x bounds
    [-2.0, 2.0],  Note: y bounds  
    [-2.0, 2.0]   Note: z bounds
]

Let adaptive_cubature_result be Integration.adaptive_cubature(
    multidimensional_function,
    integration_region,
    tolerance: 1e-6,
    max_evaluations: 100000
)

Let cubature_value be Integration.get_cubature_value(adaptive_cubature_result)
Let cubature_error be Integration.get_cubature_error(adaptive_cubature_result)
Let function_evaluations be Integration.get_cubature_evaluations(adaptive_cubature_result)

Display "Adaptive cubature (3D Gaussian):"
Display "Value: " joined with cubature_value joined with " ± " joined with cubature_error
Display "Function evaluations: " joined with function_evaluations
Display "Theoretical value: " joined with (Constants.get_pi() ** 1.5)

Note: Quasi-Monte Carlo integration
Let qmc_result be Integration.quasi_monte_carlo_integration(
    multidimensional_function,
    integration_region,
    sequence_type: "sobol",
    num_points: 65536  Note: Power of 2 for Sobol sequences
)

Let qmc_value be Integration.get_qmc_value(qmc_result)
Let qmc_error_estimate be Integration.get_qmc_error_estimate(qmc_result)

Display "Quasi-Monte Carlo (Sobol):"
Display "Value: " joined with qmc_value joined with " ± " joined with qmc_error_estimate

Note: Sparse grid integration
Let sparse_grid_result be Integration.sparse_grid_integration(
    multidimensional_function,
    dimension: 3,
    level: 4,
    grid_type: "clenshaw_curtis"
)

Let sg_value be Integration.get_sparse_grid_value(sparse_grid_result)
Let sg_points_used be Integration.get_sparse_grid_points(sparse_grid_result)

Display "Sparse grid integration:"
Display "Value: " joined with sg_value
Display "Grid points used: " joined with sg_points_used
```

## Improper Integrals

### Semi-Infinite and Infinite Integrals

```runa
Note: Semi-infinite integral using transformation
Process called "semi_infinite_integrand" that takes x as Real returns Real:
    Return MathFunctions.exp(-x) * x * x

Note: Direct semi-infinite integration
Let semi_inf_direct be Integration.semi_infinite_integral(
    semi_infinite_integrand,
    lower_bound: 0.0,
    method: "gauss_laguerre",
    order: 15
)

Display "Semi-infinite integral ∫₀^∞ x²e^(-x) dx: " joined with semi_inf_direct
Display "Exact value: 2.0"

Note: Transformation method for semi-infinite integrals
Let semi_inf_transformation be Integration.semi_infinite_transformation(
    semi_infinite_integrand,
    lower_bound: 0.0,
    transformation: "exponential",
    finite_upper_bound: 10.0,  Note: Truncation point
    method: "gauss_legendre",
    order: 20
)

Display "Semi-infinite (transformation): " joined with semi_inf_transformation

Note: Infinite integral
Process called "infinite_integrand" that takes x as Real returns Real:
    Return MathFunctions.exp(-x * x)

Let infinite_integral_result be Integration.infinite_integral(
    infinite_integrand,
    method: "gauss_hermite",
    order: 20
)

Display "Infinite integral ∫₋∞^∞ e^(-x²) dx: " joined with infinite_integral_result
Display "Exact value: " joined with MathFunctions.sqrt(Constants.get_pi())

Note: Doubly infinite integral using transformation
Process called "doubly_infinite_integrand" that takes x as Real returns Real:
    Return 1.0 / (1.0 + x * x * x * x)

Let doubly_infinite_result be Integration.doubly_infinite_integral(
    doubly_infinite_integrand,
    transformation_method: "rational",
    integration_method: "adaptive_gauss_kronrod",
    tolerance: 1e-10
)

Display "Doubly infinite integral ∫₋∞^∞ 1/(1+x⁴) dx: " joined with doubly_infinite_result
Display "Exact value: " joined with (Constants.get_pi() / MathFunctions.sqrt(2.0))
```

### Singular Integrals

```runa
Note: Integrals with endpoint singularities
Process called "endpoint_singular_integrand" that takes x as Real returns Real:
    If x <= 0.0:
        Return 0.0  Note: Handle boundary
    Otherwise:
        Return MathFunctions.log(x) / MathFunctions.sqrt(x)

Let singular_endpoint_result be Integration.singular_endpoint_integral(
    endpoint_singular_integrand,
    lower_bound: 0.0,
    upper_bound: 1.0,
    singularity_location: "lower",
    singularity_strength: 0.5,  Note: x^(-0.5) behavior
    method: "gauss_jacobi",
    alpha: -0.5,
    beta: 0.0,
    order: 15
)

Display "Endpoint singular integral: " joined with singular_endpoint_result

Note: Interior singularity
Process called "interior_singular_integrand" that takes x as Real returns Real:
    Let singularity_point be 0.3
    If Integration.abs(x - singularity_point) < 1e-15:
        Return 0.0  Note: Handle exact singularity
    Otherwise:
        Return 1.0 / MathFunctions.sqrt(Integration.abs(x - singularity_point))

Let interior_singular_result be Integration.interior_singularity_integral(
    interior_singular_integrand,
    lower_bound: 0.0,
    upper_bound: 1.0,
    singularity_point: 0.3,
    subtraction_method: True,  Note: Use singularity subtraction
    tolerance: 1e-8
)

Display "Interior singular integral: " joined with interior_singular_result

Note: Cauchy principal value integral
Process called "cauchy_principal_integrand" that takes x as Real returns Real:
    Return 1.0 / x

Let cauchy_principal_result be Integration.cauchy_principal_value(
    cauchy_principal_integrand,
    lower_bound: -1.0,
    upper_bound: 1.0,
    singularity_point: 0.0,
    method: "symmetric_exclusion",
    exclusion_radius: 1e-8
)

Display "Cauchy principal value ∫₋₁¹ 1/x dx: " joined with cauchy_principal_result
Display "Expected result: 0.0 (by symmetry)"
```

## Monte Carlo Integration

### Basic Monte Carlo Methods

```runa
Note: Standard Monte Carlo integration
Process called "monte_carlo_test_function" that takes x as Real returns Real:
    Return 4.0 / (1.0 + x * x)  Note: Computes π when integrated from 0 to 1

Let sample_sizes be [1000, 10000, 100000, 1000000]

Display "Monte Carlo convergence analysis for π estimation:"
Display "Samples | Estimate | Error | Error/√n"

For n in sample_sizes:
    Let mc_pi_result be Integration.monte_carlo_integration(
        monte_carlo_test_function,
        lower_bound: 0.0,
        upper_bound: 1.0,
        num_samples: n
    )
    
    Let pi_estimate be Integration.get_monte_carlo_value(mc_pi_result)
    Let pi_error be Integration.abs(pi_estimate - Constants.get_pi())
    Let normalized_error be pi_error * MathFunctions.sqrt(n)
    
    Display n joined with " | " joined with pi_estimate joined with " | " 
        joined with pi_error joined with " | " joined with normalized_error

Note: Importance sampling Monte Carlo
Process called "importance_sampling_integrand" that takes x as Real returns Real:
    Return MathFunctions.exp(-x * x / 2.0)  Note: Gaussian-like function

Process called "importance_sampling_pdf" that takes x as Real returns Real:
    Return MathFunctions.exp(-x)  Note: Exponential sampling distribution

Let importance_sampling_result be Integration.importance_sampling_monte_carlo(
    importance_sampling_integrand,
    importance_sampling_pdf,
    lower_bound: 0.0,
    upper_bound: 5.0,
    num_samples: 100000
)

Display "Importance sampling Monte Carlo: " joined with 
    Integration.get_importance_sampling_value(importance_sampling_result)

Note: Stratified sampling
Let stratified_mc_result be Integration.stratified_monte_carlo(
    monte_carlo_test_function,
    lower_bound: 0.0,
    upper_bound: 1.0,
    num_strata: 10,
    samples_per_stratum: 1000
)

Let stratified_variance_reduction be Integration.compute_variance_reduction_factor(
    standard_mc_result: Integration.monte_carlo_integration(monte_carlo_test_function, 0.0, 1.0, 10000),
    stratified_result: stratified_mc_result
)

Display "Stratified sampling variance reduction: " joined with stratified_variance_reduction joined with "x"
```

### Advanced Monte Carlo Techniques

```runa
Note: Control variates Monte Carlo
Process called "control_variate_integrand" that takes x as Real returns Real:
    Return MathFunctions.exp(-x)

Process called "control_variate_function" that takes x as Real returns Real:
    Return 1.0 - x  Note: Linear control variate

Let control_variate_result be Integration.control_variate_monte_carlo(
    control_variate_integrand,
    control_variate_function,
    exact_control_integral: 0.5,  Note: ∫₀¹ (1-x) dx = 0.5
    lower_bound: 0.0,
    upper_bound: 1.0,
    num_samples: 50000
)

Let cv_variance_reduction be Integration.get_control_variate_variance_reduction(control_variate_result)
Display "Control variate variance reduction: " joined with cv_variance_reduction joined with "x"

Note: Antithetic variates
Let antithetic_variates_result be Integration.antithetic_variates_monte_carlo(
    monte_carlo_test_function,
    lower_bound: 0.0,
    upper_bound: 1.0,
    num_sample_pairs: 25000
)

Let av_variance_reduction be Integration.get_antithetic_variance_reduction(antithetic_variates_result)
Display "Antithetic variates variance reduction: " joined with av_variance_reduction joined with "x"

Note: Latin hypercube sampling for higher dimensions
Let latin_hypercube_result be Integration.latin_hypercube_monte_carlo(
    multidimensional_function,
    dimension: 3,
    bounds: [[-1.0, 1.0], [-1.0, 1.0], [-1.0, 1.0]],
    num_samples: 10000
)

Display "Latin hypercube sampling (3D): " joined with 
    Integration.get_latin_hypercube_value(latin_hypercube_result)
```

## Oscillatory Integration

### Filon and Levin Methods

```runa
Note: Highly oscillatory integrands
Process called "oscillatory_integrand" that takes x as Real returns Real:
    Return MathFunctions.sin(100.0 * x) * MathFunctions.exp(-x)

Let oscillation_frequency be 100.0

Note: Standard quadrature (will struggle)
Let standard_quad_oscillatory be Integration.gauss_legendre_quadrature(
    oscillatory_integrand,
    lower_bound: 0.0,
    upper_bound: 2.0,
    order: 50  Note: High order needed
)

Display "Standard quadrature (oscillatory): " joined with standard_quad_oscillatory

Note: Filon's method for sin(wx)f(x) integrals
Process called "filon_amplitude_function" that takes x as Real returns Real:
    Return MathFunctions.exp(-x)

Let filon_result be Integration.filon_sine_integration(
    filon_amplitude_function,
    frequency: oscillation_frequency,
    lower_bound: 0.0,
    upper_bound: 2.0,
    num_intervals: 100
)

Display "Filon method: " joined with filon_result

Note: Levin's method for more general oscillatory integrals
Let levin_result be Integration.levin_collocation_method(
    oscillatory_integrand,
    lower_bound: 0.0,
    upper_bound: 2.0,
    oscillation_frequency: oscillation_frequency,
    collocation_points: 10
)

Display "Levin collocation method: " joined with levin_result

Note: Asymptotic method for high-frequency oscillations
Let asymptotic_result be Integration.asymptotic_oscillatory_integration(
    filon_amplitude_function,
    frequency: oscillation_frequency,
    lower_bound: 0.0,
    upper_bound: 2.0,
    asymptotic_order: 3
)

Display "Asymptotic method: " joined with asymptotic_result

Note: Exact value for comparison (when available)
Let exact_oscillatory be oscillation_frequency / (1.0 + oscillation_frequency * oscillation_frequency) *
    (1.0 - MathFunctions.exp(-2.0) * MathFunctions.cos(200.0))
Display "Exact oscillatory integral: " joined with exact_oscillatory
```

## Performance Analysis and Optimization

### Convergence and Efficiency Analysis

```runa
Note: Comprehensive performance comparison
Let performance_test_functions be [
    ("smooth_polynomial", simple_polynomial),
    ("oscillatory", oscillatory_integrand),
    ("singular", endpoint_singular_integrand),
    ("gaussian", test_integrand)
]

Let integration_methods be [
    ("trapezoidal", "trapezoidal_rule"),
    ("simpson", "simpson_rule"),
    ("gauss_legendre_5", "gauss_legendre_quadrature"),
    ("adaptive_simpson", "adaptive_simpson"),
    ("gauss_kronrod", "gauss_kronrod_adaptive")
]

Let performance_results be Integration.comprehensive_performance_analysis(
    test_functions: performance_test_functions,
    methods: integration_methods,
    tolerance_levels: [1e-4, 1e-6, 1e-8, 1e-10],
    efficiency_metrics: ["function_evaluations", "execution_time", "memory_usage"]
)

Display "Performance analysis summary:"
For function_name in ["smooth_polynomial", "oscillatory", "singular", "gaussian"]:
    Display "Function: " joined with function_name
    
    For method_name in ["trapezoidal", "simpson", "gauss_legendre_5", "adaptive_simpson", "gauss_kronrod"]:
        Let method_performance be Integration.get_method_performance(performance_results, function_name, method_name)
        
        If Integration.method_succeeded(method_performance):
            Let avg_evaluations be Integration.get_average_function_evaluations(method_performance)
            Let avg_time be Integration.get_average_execution_time(method_performance)
            
            Display "  " joined with method_name joined with ": " joined with avg_evaluations 
                joined with " evals, " joined with avg_time joined with " ms"
        Otherwise:
            Display "  " joined with method_name joined with ": failed"

Note: Error vs. computational cost analysis
Let efficiency_frontier_analysis be Integration.compute_efficiency_frontier(
    test_function: test_integrand,
    bounds: [0.0, 1.0],
    methods: integration_methods,
    cost_tolerance_pairs: [(10, 1e-2), (50, 1e-4), (200, 1e-6), (1000, 1e-8), (5000, 1e-10)]
)

Let pareto_optimal_methods be Integration.get_pareto_optimal_methods(efficiency_frontier_analysis)
Display "Pareto-optimal methods: " joined with Integration.format_method_list(pareto_optimal_methods)
```

### Parallel and High-Performance Integration

```runa
Note: Parallel Monte Carlo integration
Let parallel_monte_carlo_result be Integration.parallel_monte_carlo(
    multidimensional_function,
    integration_region: [[-1.0, 1.0], [-1.0, 1.0], [-1.0, 1.0]],
    total_samples: 10000000,
    num_threads: 8
)

Let parallel_mc_value be Integration.get_parallel_mc_value(parallel_monte_carlo_result)
Let parallel_speedup be Integration.get_parallel_speedup(parallel_monte_carlo_result)

Display "Parallel Monte Carlo (8 threads):"
Display "Value: " joined with parallel_mc_value
Display "Speedup: " joined with parallel_speedup joined with "x"

Note: GPU-accelerated integration (if available)
If Integration.gpu_available():
    Integration.set_device("gpu")
    
    Let gpu_monte_carlo_result be Integration.gpu_monte_carlo(
        multidimensional_function,
        integration_region: [[-1.0, 1.0], [-1.0, 1.0], [-1.0, 1.0]],
        num_samples: 100000000,
        block_size: 256
    )
    
    Let gpu_speedup be Integration.get_gpu_speedup(gpu_monte_carlo_result)
    Display "GPU Monte Carlo speedup: " joined with gpu_speedup joined with "x"
    
    Integration.set_device("cpu")

Note: Vectorized integration for multiple integrands
Let multiple_integrands be [
    simple_polynomial,
    trigonometric_function,
    test_integrand
]

Let vectorized_integration_result be Integration.vectorized_quadrature(
    multiple_integrands,
    bounds: [0.0, 1.0],
    method: "gauss_legendre",
    order: 10
)

Display "Vectorized integration results:"
For i from 0 to (Integration.count_integrands(multiple_integrands) - 1):
    Let result_i be Integration.get_vectorized_result(vectorized_integration_result, i)
    Display "Integrand " joined with i joined with ": " joined with result_i
```

## Integration with Other Modules

### With Differential Equations

```runa
Import "math/engine/numerical/ode" as ODE

Note: Integrate solutions of differential equations
Process called "ode_integrand_system" that takes t as Real, y as Vector returns Vector:
    Let y1 be LinAlg.get_element(y, 0)
    Return LinAlg.create_vector([-y1])  Note: dy/dt = -y, solution is e^(-t)

Let ode_solution be ODE.runge_kutta_solve(
    ode_integrand_system,
    t_start: 0.0,
    t_end: 2.0,
    y_initial: LinAlg.create_vector([1.0]),
    step_size: 0.01
)

Process called "solution_integrand" that takes t as Real returns Real:
    Let solution_at_t be ODE.interpolate_solution(ode_solution, t)
    Return LinAlg.get_element(solution_at_t, 0)

Let integrated_ode_solution be Integration.adaptive_quadrature(
    solution_integrand,
    lower_bound: 0.0,
    upper_bound: 2.0,
    tolerance: 1e-8
)

Display "Integral of ODE solution: " joined with Integration.get_integral_value(integrated_ode_solution)
Display "Exact integral of e^(-t) from 0 to 2: " joined with (1.0 - MathFunctions.exp(-2.0))
```

### With Optimization Problems

```runa
Import "math/engine/numerical/optimization" as Optimization

Note: Integration in optimization constraints
Process called "optimization_objective_with_integral" that takes parameters as Vector returns Real:
    Let a be LinAlg.get_element(parameters, 0)
    Let b be LinAlg.get_element(parameters, 1)
    
    Process called "parametric_integrand" that takes x as Real returns Real:
        Return a * x * x + b * x
    
    Let integral_constraint be Integration.gauss_legendre_quadrature(
        parametric_integrand,
        lower_bound: 0.0,
        upper_bound: 1.0,
        order: 5
    )
    
    Note: Minimize (a-1)² + (b-2)² subject to integral constraint = 1
    Return (a - 1.0) * (a - 1.0) + (b - 2.0) * (b - 2.0) + 
           100.0 * (integral_constraint - 1.0) * (integral_constraint - 1.0)  Note: Penalty method

Let constrained_optimization_result be Optimization.minimize(
    optimization_objective_with_integral,
    initial_guess: LinAlg.create_vector([0.5, 1.5]),
    method: "nelder_mead",
    tolerance: 1e-8
)

Let optimal_parameters be Optimization.get_optimal_point(constrained_optimization_result)
Display "Optimal parameters: " joined with LinAlg.vector_to_string(optimal_parameters)

Note: Verify constraint satisfaction
Process called "verify_constraint" that takes x as Real returns Real:
    Let a_opt be LinAlg.get_element(optimal_parameters, 0)
    Let b_opt be LinAlg.get_element(optimal_parameters, 1)
    Return a_opt * x * x + b_opt * x

Let constraint_verification be Integration.gauss_legendre_quadrature(
    verify_constraint,
    lower_bound: 0.0,
    upper_bound: 1.0,
    order: 5
)

Display "Constraint verification (should be 1.0): " joined with constraint_verification
```

## Best Practices and Method Selection

### Integration Method Selection Guide

```runa
Note: Automatic method selection based on integrand properties
Let method_selector be Integration.create_method_selector([
    ("integrand_properties", [
        ("smoothness", ["smooth", "piecewise_smooth", "discontinuous"]),
        ("oscillation", ["none", "low_frequency", "high_frequency"]),
        ("singularities", ["none", "endpoint", "interior", "multiple"]),
        ("dimension", [1, 2, 3, "high_dimensional"])
    ]),
    ("computational_constraints", [
        ("accuracy_requirement", ["low", "medium", "high", "very_high"]),
        ("function_evaluation_cost", ["cheap", "moderate", "expensive"]),
        ("time_constraint", ["none", "moderate", "strict"]),
        ("memory_constraint", ["abundant", "moderate", "limited"])
    ])
])

Let method_recommendation be Integration.recommend_integration_method(
    method_selector,
    integrand_characteristics: [
        ("smoothness", "smooth"),
        ("oscillation", "none"),
        ("singularities", "none"),
        ("dimension", 1),
        ("accuracy_requirement", "high"),
        ("function_evaluation_cost", "moderate"),
        ("time_constraint", "moderate"),
        ("memory_constraint", "abundant")
    ]
)

Display "Integration method recommendation:"
Display Integration.format_method_recommendation(method_recommendation)

Let alternative_methods be Integration.get_alternative_methods(method_recommendation)
Display "Alternative methods: " joined with Integration.format_method_list(alternative_methods)
```

### Error Control and Validation

```runa
Note: Comprehensive error control framework
Let error_controller be Integration.create_error_controller([
    ("error_estimation", "adaptive"),
    ("tolerance_management", "automatic"),
    ("method_validation", "cross_verification"),
    ("result_verification", "enabled")
])

Let controlled_integration be Integration.integrate_with_error_control(
    error_controller,
    integrand: test_integrand,
    bounds: [0.0, 1.0],
    target_accuracy: 1e-10
)

Let error_control_report be Integration.get_error_control_report(controlled_integration)
Let accuracy_achieved be Integration.verify_accuracy_achieved(controlled_integration)

Display "Error control results:"
Display "Accuracy achieved: " joined with accuracy_achieved
Display "Methods tried: " joined with Integration.get_methods_attempted(error_control_report)
Display "Final method selected: " joined with Integration.get_final_method(error_control_report)
Display "Estimated final error: " joined with Integration.get_final_error_estimate(error_control_report)

Note: Cross-verification with multiple methods
Let cross_verification_result be Integration.cross_verify_integration(
    test_integrand,
    bounds: [0.0, 1.0],
    methods: ["adaptive_simpson", "gauss_kronrod", "monte_carlo"],
    consensus_tolerance: 1e-8
)

Let verification_consensus be Integration.get_verification_consensus(cross_verification_result)
Let consensus_achieved be Integration.consensus_achieved(cross_verification_result)

Display "Cross-verification results:"
Display "Consensus achieved: " joined with consensus_achieved
Display "Consensus value: " joined with verification_consensus
Display "Method agreement: " joined with Integration.get_method_agreement_statistics(cross_verification_result)
```

The Numerical Integration module provides comprehensive, efficient, and robust algorithms for computing integrals across all domains of scientific computing, with advanced error control, adaptive methods, and specialized techniques for challenging integration problems.