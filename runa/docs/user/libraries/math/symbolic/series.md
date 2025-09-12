# Symbolic Series Analysis

The Symbolic Series module (`math/symbolic/series`) provides comprehensive symbolic series operations and analysis systems. This module enables power series manipulation, Taylor and Laurent expansions, Fourier series analysis, asymptotic expansions, and advanced series convergence testing.

## Overview

The Symbolic Series module offers powerful series analysis capabilities including:

- **Power Series**: Construction, manipulation, and arithmetic operations
- **Taylor Series**: Expansions around arbitrary points with error analysis
- **Laurent Series**: Series with negative powers for functions with poles
- **Fourier Series**: Periodic function decomposition and synthesis
- **Asymptotic Series**: Asymptotic expansions and behavior analysis
- **Series Arithmetic**: Addition, multiplication, composition, and inversion
- **Convergence Analysis**: Radius of convergence and convergence testing
- **Generating Functions**: Combinatorial and analytical applications

## Core Data Structures

### Power Series Representation

```runa
Type called "PowerSeries":
    coefficients as Dictionary[String, String]    # Power -> coefficient mapping
    variable as String                           # Series variable
    expansion_point as String                   # Center of expansion
    series_order as Integer                     # Highest order computed
    radius_of_convergence as String           # Convergence radius
    series_type as String                      # taylor, laurent, power, etc.
    truncation_error as String                # Error bound estimate
```

### Fourier Series Representation

```runa
Type called "FourierSeries":
    cosine_coefficients as Dictionary[String, String]  # a_n coefficients
    sine_coefficients as Dictionary[String, String]    # b_n coefficients  
    dc_component as String                             # a_0/2 term
    period as String                                   # Function period
    fundamental_frequency as String                    # ω = 2π/T
    convergence_type as String                        # pointwise, uniform, L²
    gibbs_phenomenon as Boolean                       # Has Gibbs phenomenon
```

## Power Series Operations

### Basic Power Series Construction

```runa
Import "math/symbolic/series" as Series

Note: Create power series manually
Let power_series be Series.create_power_series(Dictionary with:
    "0": "1"      Note: Constant term
    "1": "1"      Note: Linear term  
    "2": "1/2"    Note: Quadratic term
    "3": "1/6"    Note: Cubic term
    "4": "1/24"   Note: Fourth-order term
), "x", "0", 10)

Display "Power series: " joined with Series.power_series_to_string(power_series)

Note: Recognize series as exponential function
Let recognition = Series.identify_series(power_series)
If recognition.identified:
    Display "Recognized as: " joined with recognition.function_name
    Display "Exact form: " joined with recognition.exact_expression

Note: Create geometric series
Let geometric = Series.create_geometric_series("1", "x", 20)
Display "Geometric series: " joined with Series.power_series_to_string(geometric)
Display "Sum (|x| < 1): " joined with geometric.closed_form
```

### Power Series Arithmetic

```runa
Note: Addition of power series
Let series1 be Series.create_exponential_series("x", 10)
Let series2 = Series.create_sine_series("x", 10)

Let sum_series = Series.add_power_series(series1, series2)
Display "e^x + sin(x) = " joined with Series.power_series_to_string(sum_series)

Note: Multiplication of power series
Let product_series = Series.multiply_power_series(series1, series2)
Display "e^x × sin(x) = " joined with Series.power_series_to_string(product_series)

Note: Division of power series
Let cosine_series = Series.create_cosine_series("x", 10)
Let quotient_series = Series.divide_power_series(series2, cosine_series)
Display "sin(x)/cos(x) = tan(x) = " joined with Series.power_series_to_string(quotient_series)

Note: Series composition
Let inner_series = Series.create_power_series(Dictionary with:
    "0": "0", "1": "2", "2": "0", "3": "0"
), "x", "0", 10)  Note: 2x
Let composed = Series.compose_power_series(series1, inner_series)
Display "e^(2x) = " joined with Series.power_series_to_string(composed)
```

### Series Inversion

```runa
Note: Find multiplicative inverse of series
Let series_to_invert = Series.create_power_series(Dictionary with:
    "0": "1", "1": "x", "2": "x^2/2"
), "x", "0", 8)

Let inverse_series = Series.invert_power_series(series_to_invert)
Display "Inverse series: " joined with Series.power_series_to_string(inverse_series)

Note: Functional inverse (series reversion)
Let function_series = Series.create_power_series(Dictionary with:
    "0": "0", "1": "1", "2": "-1/6", "3": "1/120"
), "x", "0", 8)

Let reverted_series = Series.revert_power_series(function_series)
Display "Reverted series: " joined with Series.power_series_to_string(reverted_series)

Note: Lagrange inversion formula
Let lagrange_coefficients = Series.lagrange_inversion(function_series, 8)
Display "Lagrange inversion coefficients:"
For Each n, coefficient in lagrange_coefficients:
    Display "  [x^" joined with n joined with "]: " joined with coefficient
```

## Taylor Series Analysis

### Single-Variable Taylor Series

```runa
Note: Generate Taylor series for standard functions
Let exp_taylor = Series.taylor_series("exp(x)", "x", "0", 15)
Display "e^x = " joined with Series.power_series_to_string(exp_taylor)
Display "Radius of convergence: ∞"

Let log_taylor = Series.taylor_series("log(1+x)", "x", "0", 12)
Display "ln(1+x) = " joined with Series.power_series_to_string(log_taylor)
Display "Radius of convergence: " joined with log_taylor.radius_of_convergence

Note: Taylor series around arbitrary points
Let sin_taylor_pi4 = Series.taylor_series("sin(x)", "x", "π/4", 10)
Display "sin(x) around x = π/4:"
Display Series.power_series_to_string(sin_taylor_pi4)

Note: Error analysis
Let approximation_error = Series.taylor_error_bound(sin_taylor_pi4, "π/3", 6)
Display "Error bound for sin(π/3) using 6 terms: " joined with approximation_error.error_bound
Display "Actual error: " joined with approximation_error.actual_error
```

### Multivariable Taylor Series  

```runa
Note: Bivariate Taylor expansions
Let bivariate_function = "exp(x*y)"
Let bivariate_taylor = Series.multivariate_taylor_series(
    bivariate_function,
    ["x", "y"],
    ["0", "0"],
    6
)

Display "exp(xy) around (0,0):"
Display Series.multivariate_series_to_string(bivariate_taylor)

Note: Mixed partial derivatives in Taylor expansion  
Let mixed_partials = Series.extract_mixed_partials(bivariate_taylor)
Display "Mixed partial coefficients:"
For Each indices, coefficient in mixed_partials:
    Display "  ∂^" joined with indices.total_order joined with "f/∂x^" joined with indices.x_order joined with "∂y^" joined with indices.y_order joined with ": " joined with coefficient

Note: Convergence domain analysis
Let convergence_analysis = Series.analyze_multivariate_convergence(bivariate_taylor)
Display "Convergence region: " joined with convergence_analysis.domain_description
Display "Convergence type: " joined with convergence_analysis.convergence_type
```

### Maclaurin Series

```runa
Note: Maclaurin series (Taylor series at x=0)
Let standard_functions = ["sin(x)", "cos(x)", "tan(x)", "arcsin(x)", "arctan(x)"]

For Each func in standard_functions:
    Let maclaurin = Series.maclaurin_series(func, "x", 10)
    Display func joined with " = " joined with Series.power_series_to_string(maclaurin)
    
    Let convergence_info = Series.analyze_convergence(maclaurin)
    Display "  Radius: " joined with convergence_info.radius
    Display "  Convergence tests: " joined with StringOps.join(convergence_info.test_results, ", ")
```

## Laurent Series

### Laurent Series Construction

```runa
Note: Laurent series for functions with poles
Let function_with_pole = "1/((z-1)*(z-2))"
Let laurent_series = Series.laurent_series(function_with_pole, "z", "1", -2, 8)

Display "Laurent series around z = 1:"
Display "Principal part: " joined with Series.principal_part_to_string(laurent_series)
Display "Regular part: " joined with Series.regular_part_to_string(laurent_series)

Note: Residue calculation
Let residue = Series.extract_residue(laurent_series)
Display "Residue at z = 1: " joined with residue

Note: Classification of singularities
Let singularity_analysis = Series.classify_singularity(function_with_pole, "z", "1")
Display "Singularity type: " joined with singularity_analysis.type
Display "Order: " joined with String(singularity_analysis.order)
```

### Laurent Series Arithmetic

```runa
Note: Operations with Laurent series
Let laurent1 = Series.laurent_series("1/z", "z", "0", -1, 5)
Let laurent2 = Series.laurent_series("1/(z-1)", "z", "0", 0, 5)

Let laurent_sum = Series.add_laurent_series(laurent1, laurent2)
Display "1/z + 1/(z-1) = " joined with Series.laurent_series_to_string(laurent_sum)

Let laurent_product = Series.multiply_laurent_series(laurent1, laurent2)
Display "1/z × 1/(z-1) = " joined with Series.laurent_series_to_string(laurent_product)

Note: Analytic continuation
Let analytic_continuation = Series.analytic_continuation(laurent1, "0", "2")
Display "Continuation from z=0 to z=2: " joined with Series.laurent_series_to_string(analytic_continuation)
```

## Fourier Series

### Fourier Series Construction

```runa
Note: Fourier series for periodic functions
Note: The following quoted expression uses conventional mathematical "if/then/else" notation as data, not Runa control flow keywords.
Let square_wave = "if -π < x < 0 then -1 else 1"  Note: Square wave on [-π, π]
Let fourier_square = Series.fourier_series(square_wave, "x", "π")

Display "Square wave Fourier series:"
Display "a₀ = " joined with fourier_square.dc_component
Display "Sine coefficients (first 5):"
For Each n, bn in fourier_square.sine_coefficients:
    If n <= 5:
        Display "  b" joined with String(n) joined with " = " joined with bn

Note: Sawtooth wave
Let sawtooth = "x"  Note: Sawtooth on [-π, π]
Let fourier_sawtooth = Series.fourier_series(sawtooth, "x", "π")

Display "Sawtooth wave Fourier series:"
Display "Sine coefficients:"
For Each n, bn in fourier_sawtooth.sine_coefficients:
    If n <= 5:
        Display "  b" joined with String(n) joined with " = " joined with bn
```

### Fourier Series Analysis

```runa
Note: Convergence properties
Let convergence_analysis = Series.analyze_fourier_convergence(fourier_square)
Display "Fourier series convergence:"
Display "Pointwise convergence: " joined with String(convergence_analysis.pointwise)
Display "Uniform convergence: " joined with String(convergence_analysis.uniform)
Display "L² convergence: " joined with String(convergence_analysis.l2_convergence)

Note: Gibbs phenomenon detection
If convergence_analysis.has_gibbs_phenomenon:
    Display "Gibbs phenomenon present at discontinuities"
    Display "Overshoot percentage: " joined with String(convergence_analysis.gibbs_overshoot) joined with "%"

Note: Partial sum approximation
Let partial_sums = Series.fourier_partial_sums(fourier_square, [1, 3, 5, 10, 20])
For Each n, approximation in partial_sums:
    Let error_analysis = Series.fourier_approximation_error(square_wave, approximation, "x")
    Display "n = " joined with String(n) joined with ", L² error = " joined with error_analysis.l2_error
```

### Complex Fourier Series

```runa
Note: Complex exponential form
Let complex_fourier = Series.complex_fourier_series(square_wave, "x", "π")

Display "Complex Fourier series:"
Display "Fundamental frequency: " joined with complex_fourier.fundamental_frequency
For Each n, cn in complex_fourier.complex_coefficients:
    If n >= -3 and n <= 3:
        Display "  c" joined with String(n) joined with " = " joined with cn

Note: Relationship between forms
Let verification = Series.verify_fourier_forms(fourier_square, complex_fourier)
Display "Complex and trigonometric forms match: " joined with String(verification.forms_match)
```

## Generating Functions

### Ordinary Generating Functions

```runa
Note: Create generating functions for sequences
Let fibonacci_sequence = ["1", "1", "2", "3", "5", "8", "13", "21", "34", "55"]
Let fibonacci_gf = Series.ordinary_generating_function(fibonacci_sequence, "x")

Display "Fibonacci generating function:"
Display Series.power_series_to_string(fibonacci_gf)

Note: Closed form of Fibonacci generating function
Let fibonacci_closed_form = Series.find_closed_form_ogf(fibonacci_gf)
Display "Closed form: " joined with fibonacci_closed_form.expression
Display "Derivation method: " joined with fibonacci_closed_form.method

Note: Extract coefficients
Let extracted_coefficients = Series.extract_coefficient_sequence(fibonacci_closed_form, 20)
Display "Extracted Fibonacci numbers (first 10):"
For Each i, coeff in extracted_coefficients:
    If i < 10:
        Display "  F(" joined with String(i) joined with ") = " joined with coeff
```

### Exponential Generating Functions

```runa
Note: Exponential generating functions
Let factorial_sequence = ["1", "1", "2", "6", "24", "120", "720"]  Note: n!
Let factorial_egf = Series.exponential_generating_function(factorial_sequence, "x")

Display "Factorial EGF: " joined with Series.power_series_to_string(factorial_egf)

Let factorial_recognition = Series.identify_egf(factorial_egf)
Display "Recognized as: " joined with factorial_recognition.function_name

Note: Bell numbers generating function
Let bell_egf = Series.create_bell_numbers_egf("x", 15)
Display "Bell numbers EGF: " joined with Series.power_series_to_string(bell_egf)

Let bell_numbers = Series.extract_egf_coefficients(bell_egf, 10)
Display "Bell numbers (first 10):"
For Each n, bell_n in bell_numbers:
    Display "  B(" joined with String(n) joined with ") = " joined with bell_n
```

### Combinatorial Applications

```runa
Note: Partition generating functions
Let partition_gf = Series.partition_generating_function("x", 50)
Display "Partition generating function (50 terms):"
Display Series.power_series_to_string(partition_gf)

Let partition_numbers = Series.extract_partition_numbers(partition_gf, 20)
Display "Partition numbers p(n):"
For Each n, p_n in partition_numbers:
    If n <= 10:
        Display "  p(" joined with String(n) joined with ") = " joined with p_n

Note: Catalan numbers
Let catalan_gf = Series.catalan_generating_function("x", 15)
Let catalan_closed_form = Series.catalan_closed_form_derivation()

Display "Catalan generating function:"
Display "Series form: " joined with Series.power_series_to_string(catalan_gf)
Display "Closed form: " joined with catalan_closed_form.expression
Display "Square root relation: " joined with catalan_closed_form.sqrt_relation
```

## Asymptotic Series

### Asymptotic Expansions

```runa
Note: Asymptotic series for large arguments
Let stirling_function = "log(Γ(z))"
Let stirling_asymptotic = Series.asymptotic_series(stirling_function, "z", "∞", 8)

Display "Stirling's asymptotic formula:"
Display Series.asymptotic_series_to_string(stirling_asymptotic)

Note: Error bounds for asymptotic series
Let error_bounds = Series.asymptotic_error_analysis(stirling_asymptotic, "100")
Display "Error bounds for z = 100:"
For Each n, error in error_bounds:
    Display "  " joined with String(n) joined with " terms: error ≤ " joined with error

Note: Optimal truncation
Let optimal_truncation = Series.find_optimal_truncation(stirling_asymptotic, "50")
Display "Optimal number of terms for z = 50: " joined with String(optimal_truncation.optimal_terms)
Display "Estimated error: " joined with optimal_truncation.error_estimate
```

### Asymptotic Methods

```runa
Note: Watson's lemma applications
Let laplace_integral = "∫₀^∞ exp(-t*z) * t^(α-1) * (1 + a*t) dt"
Let watson_expansion = Series.apply_watson_lemma(laplace_integral, "z", "∞", 6)

Display "Watson's lemma expansion:"
Display Series.asymptotic_series_to_string(watson_expansion)

Note: Saddle point method
Let complex_integral = "∫_{-∞}^{∞} exp(n*f(z)) dz"
Let saddle_point_expansion = Series.saddle_point_expansion(complex_integral, "n", "∞", 4)

Display "Saddle point expansion:"
Display Series.asymptotic_series_to_string(saddle_point_expansion)
Display "Critical points: " joined with StringOps.join(saddle_point_expansion.critical_points, ", ")
```

## Series Convergence

### Convergence Tests

```runa
Note: Apply various convergence tests
Let test_series = Series.create_power_series(Dictionary with:
    "n": "1/n^2"  Note: Coefficients are 1/n²
), "x", "0", 50)

Let ratio_test = Series.ratio_test(test_series)
Display "Ratio test:"
Display "  Limit: " joined with ratio_test.limit_value
Display "  Conclusion: " joined with ratio_test.conclusion
Display "  Radius: " joined with ratio_test.radius_of_convergence

Let root_test = Series.root_test(test_series)
Display "Root test:"
Display "  Limit superior: " joined with root_test.limsup
Display "  Radius: " joined with root_test.radius_of_convergence

Note: Cauchy-Hadamard theorem application
Let cauchy_hadamard = Series.apply_cauchy_hadamard(test_series)
Display "Cauchy-Hadamard radius: " joined with cauchy_hadamard.radius
Display "Method used: " joined with cauchy_hadamard.method
```

### Convergence on the Circle

```runa
Note: Boundary convergence analysis
Let boundary_analysis = Series.analyze_boundary_convergence(test_series)

Display "Convergence on |x| = R:"
For Each point, convergence in boundary_analysis.boundary_points:
    Display "  x = " joined with point joined with ": " joined with convergence.type
    If convergence.conditional:
        Display "    (conditionally convergent)"
    
Note: Abel's theorem applications
Let abel_sum = Series.apply_abel_theorem(test_series, "1")
Display "Abel sum at x = 1: " joined with abel_sum.limit_value
Display "Convergence type: " joined with abel_sum.convergence_type
```

## Padé Approximants

### Rational Approximation

```runa
Note: Construct Padé approximants
Let original_series = Series.taylor_series("exp(x)", "x", "0", 20)
Let pade_33 = Series.pade_approximant(original_series, 3, 3)

Display "Padé [3/3] approximant to e^x:"
Display "Numerator: " joined with pade_33.numerator
Display "Denominator: " joined with pade_33.denominator

Note: Accuracy comparison
Let accuracy_analysis = Series.compare_approximations(
    "exp(x)",
    [original_series, pade_33],
    ["Taylor 6-terms", "Padé [3/3]"],
    "x = 2"
)

Display "Approximation accuracy at x = 2:"
For Each method, error in accuracy_analysis:
    Display "  " joined with method joined with ": error = " joined with error
```

### Continued Fractions

```runa
Note: Convert series to continued fractions
Let continued_fraction = Series.series_to_continued_fraction(original_series)
Display "Continued fraction form:"
Display Series.continued_fraction_to_string(continued_fraction)

Note: Convergents of continued fractions
Let convergents = Series.continued_fraction_convergents(continued_fraction, 8)
Display "Continued fraction convergents:"
For Each n, convergent in convergents:
    Display "  C" joined with String(n) joined with " = " joined with convergent.numerator joined with "/" joined with convergent.denominator
```

## Special Series

### Hypergeometric Series

```runa
Note: Hypergeometric series analysis
Let hypergeometric = Series.hypergeometric_series("a", "b", "c", "x", 20)
Display "₂F₁(a,b;c;x) = " joined with Series.power_series_to_string(hypergeometric)

Note: Transformation formulas
Let transformed = Series.apply_hypergeometric_transformation(hypergeometric, "euler")
Display "Euler transformation: " joined with Series.power_series_to_string(transformed)

Let continued_hypergeometric = Series.hypergeometric_continued_fraction("a", "b", "c", "x")
Display "Continued fraction form: " joined with Series.continued_fraction_to_string(continued_hypergeometric)
```

### q-Series

```runa
Note: Basic q-series
Let q_pochhammer = Series.q_pochhammer_symbol("a", "q", "n")
Display "(a;q)_n = " joined with Series.q_series_to_string(q_pochhammer)

Let basic_hypergeometric = Series.basic_hypergeometric_series(["a₁", "a₂"], ["b₁"], "q", "z", 15)
Display "₂φ₁(a₁,a₂;b₁;q,z) = " joined with Series.q_series_to_string(basic_hypergeometric)

Note: q-series identities
Let ramanujan_identity = Series.verify_q_series_identity("ramanujan_1", "q")
Display "Ramanujan q-series identity verified: " joined with String(ramanujan_identity.verified)
```

## Error Analysis and Truncation

### Truncation Error Bounds

```runa
Note: Compute truncation error bounds
Let series = Series.taylor_series("sin(x)", "x", "0", 10)
Let error_bound = Series.taylor_truncation_error(series, "π/4", 6)

Display "sin(π/4) approximation error (6 terms):"
Display "Error bound: " joined with error_bound.theoretical_bound
Display "Actual error: " joined with error_bound.actual_error
Display "Error ratio: " joined with error_bound.efficiency

Note: Adaptive truncation
Let adaptive_approximation = Series.adaptive_series_evaluation(
    "exp(x)",
    "5",
    Dictionary with:
        "tolerance": "1e-12"
        "max_terms": "50"
)

Display "Adaptive evaluation of exp(5):"
Display "Terms needed: " joined with String(adaptive_approximation.terms_used)
Display "Final error: " joined with adaptive_approximation.estimated_error
Display "Result: " joined with adaptive_approximation.value
```

## Performance Optimization

### Efficient Series Computation

```runa
Note: Optimize series computations
Let optimization_config = Dictionary with:
    "use_horner_method": "true"
    "cache_coefficients": "true"
    "parallel_evaluation": "true"
    "precision_arithmetic": "100"

Series.configure_performance(optimization_config)

Note: Benchmark different methods
Let benchmark_results = Series.benchmark_series_methods(
    "exp(x)",
    ["direct", "horner", "cached", "parallel"],
    "x = 10",
    1000  Note: 1000 evaluations
)

Display "Performance benchmarks (1000 evaluations):"
For Each method, time in benchmark_results:
    Display "  " joined with method joined with ": " joined with String(time) joined with " ms"
```

## Error Handling

### Series Computation Errors

```runa
Try:
    Let divergent_series = Series.create_power_series(Dictionary with:
        "n": "n!"  Note: Factorial coefficients
    ), "x", "0", 20)
    
    Let invalid_evaluation = Series.evaluate_power_series(divergent_series, "2")
    
Catch Errors.SeriesConvergenceError as conv_error:
    Display "Series convergence error: " joined with conv_error.message
    Display "Radius of convergence: " joined with conv_error.convergence_radius
    Display "Evaluation point: " joined with conv_error.evaluation_point
    
    Note: Suggest alternative approaches
    Display "Suggested alternatives:"
    For Each alternative in conv_error.suggested_methods:
        Display "  " joined with alternative

Catch Errors.NumericalInstabilityError as instability:
    Display "Numerical instability in series computation"
    Display "Problematic terms: " joined with StringOps.join(instability.problematic_terms, ", ")
```

## Related Documentation

- **[Symbolic Core](core.md)**: Expression representation for series coefficients
- **[Symbolic Calculus](calculus.md)**: Taylor series via differentiation
- **[Symbolic Functions](functions.md)**: Special functions and their series representations
- **[Complex Analysis](../analysis/complex.md)**: Laurent series and residue theory
- **[Real Analysis](../analysis/real.md)**: Convergence theory and uniform convergence
- **[Fourier Analysis](../engine/fourier/README.md)**: FFT and discrete Fourier analysis

The Symbolic Series module provides comprehensive series analysis capabilities, from basic power series arithmetic to advanced asymptotic analysis and generating functions. Its symbolic approach enables exact series manipulations while providing numerical evaluation with error control for practical applications.