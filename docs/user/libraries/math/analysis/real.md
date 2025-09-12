Note: Real Analysis Module

## Overview

The `math/analysis/real` module provides comprehensive real analysis functionality, including sequences and series analysis, limits and continuity, differentiation and integration theory, function spaces, and metric space operations. This module forms the foundation for advanced mathematical analysis in Runa.

## Key Features

- **Sequences and Series**: Convergence tests, limit computation, and series analysis
- **Continuity Theory**: Epsilon-delta definitions and uniform convergence
- **Integration Theory**: Riemann and Lebesgue integration methods
- **Function Spaces**: Analysis of function properties and approximations
- **Metric Spaces**: Completeness, compactness, and connectedness
- **Real Function Analysis**: Comprehensive function property analysis

## Data Types

### Sequence
Represents a mathematical sequence with convergence properties:
```runa
Type called "Sequence":
    terms as List[String]              Note: Sequence terms
    indexing_function as Dictionary[String, String]  Note: Index mapping
    limit as String                    Note: Sequence limit
    is_convergent as Boolean           Note: Convergence status
    is_bounded as Boolean              Note: Boundedness property
    is_monotonic as Boolean            Note: Monotonic property
    convergence_rate as String         Note: Rate of convergence
    cauchy_property as Boolean         Note: Cauchy criterion
```

### Series
Represents a mathematical series with convergence analysis:
```runa
Type called "Series":
    terms as List[String]              Note: Series terms
    partial_sums as List[String]       Note: Partial sum sequence
    sum as String                      Note: Series sum
    is_convergent as Boolean           Note: Convergence status
    convergence_test as String         Note: Test method used
    radius_of_convergence as String    Note: Power series radius
    is_absolutely_convergent as Boolean Note: Absolute convergence
    is_conditionally_convergent as Boolean Note: Conditional convergence
```

### RealFunction
Represents a real-valued function with analytical properties:
```runa
Type called "RealFunction":
    domain as Dictionary[String, String]           Note: Function domain
    codomain as Dictionary[String, String]         Note: Function codomain
    expression as String                          Note: Function expression
    is_continuous as Boolean                      Note: Continuity property
    is_differentiable as Boolean                  Note: Differentiability
    is_integrable as Boolean                      Note: Integrability
    continuity_points as List[String]             Note: Continuous points
    discontinuity_points as List[String]          Note: Discontinuous points
    critical_points as List[String]               Note: Critical points
```

### MetricSpace
Represents a metric space with topological properties:
```runa
Type called "MetricSpace":
    points as List[String]                        Note: Space points
    metric as Dictionary[String, Dictionary[String, String]] Note: Distance function
    is_complete as Boolean                        Note: Completeness property
    is_compact as Boolean                         Note: Compactness property
    is_connected as Boolean                       Note: Connectedness property
    diameter as String                            Note: Space diameter
    dense_subsets as List[List[String]]           Note: Dense subsets
```

## Sequence and Series Operations

### Testing Sequence Convergence
```runa
Import "math/analysis/real" as RealAnalysis

Note: Create a sequence
Let sequence_terms be ["1", "0.5", "0.333", "0.25", "0.2"]
Let harmonic_sequence be Sequence with:
    terms: sequence_terms
    indexing_function: Dictionary with: "formula": "1/n"
    is_convergent: false
    is_bounded: true
    is_monotonic: true
    cauchy_property: false

Note: Test convergence
Let is_convergent be RealAnalysis.test_sequence_convergence(harmonic_sequence)
Display "Harmonic sequence convergent: " joined with String(is_convergent)

Note: Compute sequence limit
If is_convergent:
    Let limit_value be RealAnalysis.compute_sequence_limit(harmonic_sequence, "epsilon_delta")
    Display "Limit: " joined with limit_value.limit_value
    Display "Convergence rate: " joined with limit_value.convergence_rate
```

### Series Convergence Analysis
```runa
Note: Analyze geometric series
Let geometric_terms be ["1", "0.5", "0.25", "0.125", "0.0625"]
Let geometric_series be Series with:
    terms: geometric_terms
    is_convergent: true
    convergence_test: "ratio"
    radius_of_convergence: "1.0"
    is_absolutely_convergent: true

Let convergence_result be RealAnalysis.analyze_series_convergence(geometric_series)
Display "Series converges: " joined with String(convergence_result.is_convergent)
Display "Sum: " joined with convergence_result.series_sum
Display "Test used: " joined with convergence_result.convergence_test_applied

Note: Power series analysis
Let power_series_coeffs be ["1", "1", "0.5", "0.167", "0.042"]
Let power_series be Series with:
    terms: power_series_coeffs
    convergence_test: "root_test"
    
Let radius_result be RealAnalysis.compute_radius_of_convergence(power_series)
Display "Radius of convergence: " joined with radius_result.radius
Display "Convergence interval: [" joined with radius_result.interval_start joined with ", " joined with radius_result.interval_end joined with "]"
```

### Alternating Series Test
```runa
Note: Test alternating harmonic series
Let alternating_terms be ["1", "-0.5", "0.333", "-0.25", "0.2", "-0.167"]
Let alternating_series be Series with:
    terms: alternating_terms
    is_convergent: false
    
Let alternating_result be RealAnalysis.alternating_series_test(alternating_series)
Display "Alternating series converges: " joined with String(alternating_result.converges)
Display "Error bound: " joined with alternating_result.error_bound
Display "Conditional convergence: " joined with String(alternating_result.is_conditional)
```

## Function Analysis

### Continuity Testing
```runa
Note: Test function continuity
Let rational_function be RealFunction with:
    domain: Dictionary with: "start": "-10", "end": "10", "exclude": ["0"]
    expression: "1/x"
    is_continuous: false
    discontinuity_points: ["0"]

Let continuity_result be RealAnalysis.test_function_continuity(rational_function, "0.001")
Display "Function continuous: " joined with String(continuity_result.is_continuous)
Display "Discontinuities: " joined with String(Length(continuity_result.discontinuity_points))

For Each point in continuity_result.discontinuity_points:
    Let discontinuity_type be RealAnalysis.classify_discontinuity(rational_function, point)
    Display "Point " joined with point joined with ": " joined with discontinuity_type.classification
```

### Differentiability Analysis
```runa
Note: Analyze function differentiability
Let polynomial_function be RealFunction with:
    domain: Dictionary with: "start": "-5", "end": "5"
    expression: "x^3 - 2*x^2 + x - 1"
    is_differentiable: true

Let derivative_result be RealAnalysis.compute_derivative(polynomial_function, "symbolic")
Display "Derivative: " joined with derivative_result.derivative_expression
Display "Critical points: " joined with String(Length(derivative_result.critical_points))

For Each critical_point in derivative_result.critical_points:
    Let nature be RealAnalysis.classify_critical_point(polynomial_function, critical_point)
    Display "Critical point " joined with critical_point joined with ": " joined with nature.classification
```

### Function Limits
```runa
Note: Compute function limits
Let limit_function be RealFunction with:
    domain: Dictionary with: "start": "0", "end": "2", "exclude": ["1"]
    expression: "(x^2 - 1)/(x - 1)"

Note: Limit as x approaches 1
Let limit_result be RealAnalysis.compute_function_limit(limit_function, "1", "both_sides")
Display "lim(x→1) (x²-1)/(x-1) = " joined with limit_result.limit_value
Display "Left limit: " joined with limit_result.left_limit
Display "Right limit: " joined with limit_result.right_limit
Display "Limit exists: " joined with String(limit_result.limit_exists)

Note: Infinite limits
Let asymptotic_result be RealAnalysis.analyze_asymptotic_behavior(limit_function)
Display "Vertical asymptotes: " joined with String(Length(asymptotic_result.vertical_asymptotes))
Display "Horizontal asymptotes: " joined with String(Length(asymptotic_result.horizontal_asymptotes))
```

## Integration Theory

### Riemann Integration
```runa
Note: Compute Riemann integral
Let integrable_function be RealFunction with:
    domain: Dictionary with: "start": "0", "end": "1"
    expression: "x^2"
    is_integrable: true

Let riemann_result be RealAnalysis.riemann_integrate(integrable_function, "0", "1", "trapezoid")
Display "∫₀¹ x² dx = " joined with riemann_result.integral_value
Display "Method: " joined with riemann_result.integration_method
Display "Error estimate: " joined with riemann_result.error_estimate
Display "Number of partitions: " joined with String(riemann_result.partition_count)

Note: Test Riemann integrability
Let discontinuous_function be RealFunction with:
    domain: Dictionary with: "start": "0", "end": "1"
    expression: "floor(2*x)"  Note: Step function
    discontinuity_points: ["0.5"]

Let integrability_test be RealAnalysis.test_riemann_integrability(discontinuous_function)
Display "Riemann integrable: " joined with String(integrability_test.is_integrable)
Display "Measure of discontinuities: " joined with integrability_test.discontinuity_measure
```

### Lebesgue Integration
```runa
Note: Lebesgue integration for more general functions
Let lebesgue_function be RealFunction with:
    domain: Dictionary with: "start": "0", "end": "1"
    expression: "x^(1/3)"  Note: Not differentiable at 0
    is_integrable: true

Let lebesgue_result be RealAnalysis.lebesgue_integrate(lebesgue_function, "0", "1")
Display "Lebesgue integral: " joined with lebesgue_result.integral_value
Display "Measurable: " joined with String(lebesgue_result.is_measurable)
Display "Absolutely integrable: " joined with String(lebesgue_result.is_absolutely_integrable)

Note: Compare Riemann and Lebesgue integrals
Let comparison be RealAnalysis.compare_integration_methods(lebesgue_function, "0", "1")
Display "Riemann integral: " joined with comparison.riemann_value
Display "Lebesgue integral: " joined with comparison.lebesgue_value
Display "Difference: " joined with comparison.difference
```

### Improper Integrals
```runa
Note: Handle improper integrals
Let improper_function be RealFunction with:
    domain: Dictionary with: "start": "1", "end": "infinity"
    expression: "1/(x^2)"

Let improper_result be RealAnalysis.improper_integral(improper_function, "1", "infinity")
Display "∫₁^∞ 1/x² dx = " joined with improper_result.integral_value
Display "Convergent: " joined with String(improper_result.converges)
Display "Convergence test: " joined with improper_result.convergence_test

Note: Integral with singularity
Let singular_function be RealFunction with:
    domain: Dictionary with: "start": "0", "end": "1"
    expression: "1/sqrt(x)"

Let singular_result be RealAnalysis.improper_integral(singular_function, "0", "1")
Display "∫₀¹ 1/√x dx = " joined with singular_result.integral_value
Display "Principal value: " joined with singular_result.principal_value
```

## Metric Space Operations

### Creating and Analyzing Metric Spaces
```runa
Note: Create Euclidean metric space
Let euclidean_points be ["(0,0)", "(1,1)", "(2,0)", "(1,2)"]
Let euclidean_metric be Dictionary[String, Dictionary[String, String]]()

Note: Define Euclidean distance
Set euclidean_metric["(0,0)"]["(1,1)"] to "1.414"
Set euclidean_metric["(0,0)"]["(2,0)"] to "2.000"
Set euclidean_metric["(1,1)"]["(2,0)"] to "1.414"

Let euclidean_space be MetricSpace with:
    points: euclidean_points
    metric: euclidean_metric
    is_complete: true
    is_compact: false
    is_connected: true

Let completeness_test be RealAnalysis.test_metric_space_completeness(euclidean_space)
Display "Space complete: " joined with String(completeness_test.is_complete)
Display "Cauchy sequences converge: " joined with String(completeness_test.cauchy_convergence)
```

### Compactness Analysis
```runa
Note: Test compactness properties
Let bounded_space be MetricSpace with:
    points: ["(0,0)", "(0,1)", "(1,0)", "(1,1)"]
    is_compact: true
    diameter: "1.414"

Let compactness_result be RealAnalysis.analyze_compactness(bounded_space)
Display "Compact: " joined with String(compactness_result.is_compact)
Display "Sequentially compact: " joined with String(compactness_result.is_sequentially_compact)
Display "Totally bounded: " joined with String(compactness_result.is_totally_bounded)

Note: Find epsilon-net
Let epsilon be "0.5"
Let epsilon_net be RealAnalysis.construct_epsilon_net(bounded_space, epsilon)
Display "ε-net size: " joined with String(Length(epsilon_net.covering_points))
```

### Connectedness Properties
```runa
Note: Analyze space connectedness
Let disconnected_space be MetricSpace with:
    points: ["(-1,0)", "(0,0)", "(2,0)", "(3,0)"]
    is_connected: false

Let connectedness_result be RealAnalysis.test_connectedness(disconnected_space)
Display "Connected: " joined with String(connectedness_result.is_connected)
Display "Path connected: " joined with String(connectedness_result.is_path_connected)
Display "Number of components: " joined with String(connectedness_result.component_count)

For Each component in connectedness_result.connected_components:
    Display "Component: " joined with String(component.points)
```

## Uniform Convergence

### Function Sequence Convergence
```runa
Note: Analyze uniform convergence of function sequences
Let function_sequence be List[RealFunction]
Let f1 be RealFunction with: expression: "x/1"
Let f2 be RealFunction with: expression: "x/2"
Let f3 be RealFunction with: expression: "x/3"
Let f4 be RealFunction with: expression: "x/4"

Add f1 to function_sequence
Add f2 to function_sequence
Add f3 to function_sequence
Add f4 to function_sequence

Let limit_function be RealFunction with: expression: "0"

Let uniform_convergence be UniformConvergence with:
    function_sequence: function_sequence
    limit_function: limit_function
    is_uniform: true
    pointwise_convergent: true

Let convergence_analysis be RealAnalysis.test_uniform_convergence(uniform_convergence, "[0,1]")
Display "Uniform convergence: " joined with String(convergence_analysis.is_uniform)
Display "Pointwise convergence: " joined with String(convergence_analysis.is_pointwise)
Display "Rate of convergence: " joined with convergence_analysis.convergence_rate

Note: Weierstrass M-test
Let M_test_result be RealAnalysis.weierstrass_m_test(function_sequence, "[0,1]")
Display "M-test passes: " joined with String(M_test_result.test_passes)
Display "Uniform bound: " joined with M_test_result.uniform_bound
```

### Approximation Theory
```runa
Note: Polynomial approximation (Weierstrass approximation theorem)
Let target_function be RealFunction with:
    domain: Dictionary with: "start": "0", "end": "1"
    expression: "exp(x)"

Let polynomial_degree be 5
Let weierstrass_approx be RealAnalysis.weierstrass_approximation(target_function, polynomial_degree)
Display "Approximating polynomial: " joined with weierstrass_approx.polynomial_expression
Display "Maximum error: " joined with weierstrass_approx.maximum_error
Display "L² error: " joined with weierstrass_approx.l2_error

Note: Bernstein polynomial approximation
Let bernstein_approx be RealAnalysis.bernstein_approximation(target_function, polynomial_degree)
Display "Bernstein polynomial: " joined with bernstein_approx.polynomial_expression
Display "Uniform convergence: " joined with String(bernstein_approx.uniform_convergence)
```

## Advanced Real Analysis

### Function Spaces
```runa
Note: Analyze function spaces L^p
Let function_list be [
    RealFunction with: expression: "x^2",
    RealFunction with: expression: "sin(x)",
    RealFunction with: expression: "1/(1+x^2)"
]

Let p_norm be "2"  Note: L² space
Let lp_space_result be RealAnalysis.analyze_lp_space(function_list, p_norm, "[0,1]")
Display "L" joined with p_norm joined with " space dimension: " joined with String(lp_space_result.dimension)
Display "Separable: " joined with String(lp_space_result.is_separable)
Display "Complete: " joined with String(lp_space_result.is_complete)

For Each func in function_list:
    Let norm_value be RealAnalysis.compute_lp_norm(func, p_norm, "[0,1]")
    Display "||" joined with func.expression joined with "||_" joined with p_norm joined with " = " joined with norm_value.norm_value
```

### Fourier Analysis Preparation
```runa
Note: Orthogonal function systems
Let orthogonal_basis be [
    RealFunction with: expression: "1",
    RealFunction with: expression: "cos(π*x)",
    RealFunction with: expression: "sin(π*x)",
    RealFunction with: expression: "cos(2*π*x)",
    RealFunction with: expression: "sin(2*π*x)"
]

Let orthogonality_test be RealAnalysis.test_orthogonality(orthogonal_basis, "[-1,1]")
Display "Orthogonal system: " joined with String(orthogonality_test.is_orthogonal)
Display "Orthonormal: " joined with String(orthogonality_test.is_orthonormal)

Note: Function expansion in orthogonal basis
Let target_function be RealFunction with: expression: "x^2"
Let expansion_result be RealAnalysis.orthogonal_expansion(target_function, orthogonal_basis, "[-1,1]")
Display "Expansion coefficients:"
For Each coeff, index in expansion_result.coefficients:
    Display "  a_" joined with String(index) joined with " = " joined with coeff
Display "Approximation error: " joined with expansion_result.approximation_error
```

## Error Handling

### Domain and Convergence Errors
```runa
Note: Handle various analysis errors
Try:
    Note: Invalid domain for limit
    Let invalid_function be RealFunction with:
        domain: Dictionary with: "start": "1", "end": "0"  Note: Invalid interval
        expression: "x^2"
    
    Let limit_result be RealAnalysis.compute_function_limit(invalid_function, "0.5", "both_sides")
Catch Errors.DomainError as error:
    Display "Domain error: " joined with error.message
    Display "Valid domain required for limit computation"

Try:
    Note: Non-convergent series
    Let divergent_series be Series with:
        terms: ["1", "2", "3", "4", "5"]
        is_convergent: false
    
    Let sum_result be RealAnalysis.compute_series_sum(divergent_series)
Catch Errors.ConvergenceError as error:
    Display "Convergence error: " joined with error.message
    Display "Series must converge to compute sum"
```

### Integration Errors
```runa
Try:
    Note: Non-integrable function
    Let non_integrable be RealFunction with:
        expression: "1/x"
        domain: Dictionary with: "start": "-1", "end": "1", "exclude": ["0"]
    
    Let integral_result be RealAnalysis.riemann_integrate(non_integrable, "-1", "1", "simpson")
Catch Errors.IntegrationError as error:
    Display "Integration error: " joined with error.message
    Display "Function not Riemann integrable on given interval"
    
    Note: Try Lebesgue integration instead
    Try:
        Let lebesgue_result be RealAnalysis.lebesgue_integrate(non_integrable, "-1", "1")
        Display "Lebesgue integral exists: " joined with lebesgue_result.integral_value
    Catch Errors.IntegrationError as lebesgue_error:
        Display "Neither Riemann nor Lebesgue integrable: " joined with lebesgue_error.message
```

## Performance Considerations

- **Series Convergence**: Use appropriate convergence tests based on series characteristics
- **Function Analysis**: Cache derivative and integral computations for repeated use
- **Metric Space Operations**: Use spatial indexing for large point sets
- **Integration Methods**: Choose method based on function smoothness and accuracy requirements

## Best Practices

1. **Validate Domains**: Always verify function domains before analysis
2. **Choose Appropriate Tests**: Use the most efficient convergence test for each series type
3. **Handle Discontinuities**: Properly classify and handle function discontinuities
4. **Error Estimation**: Always check error bounds in numerical computations
5. **Convergence Criteria**: Use appropriate epsilon values for limit computations
6. **Integration Method Selection**: Match integration method to function properties

## Related Documentation

- **[Math Core Operations](../core/operations.md)**: Basic mathematical operations
- **[Math Engine Numerical](../engine/numerical/README.md)**: Numerical computation methods
- **[Math Analysis Complex](complex.md)**: Complex analysis functions
- **[Math Analysis Functional](functional.md)**: Functional analysis and operators