Note: Math Core Constants Module

## Overview

The `math/core/constants` module provides comprehensive access to mathematical constants with arbitrary precision support. It includes universal constants like π and e, physical constants, computational limits, and specialized mathematical values used across scientific computing.

## Key Features

- **Arbitrary Precision**: All constants can be computed to user-specified precision
- **Physical Constants**: CODATA-compliant fundamental physical constants
- **Computational Limits**: Machine-specific precision and overflow thresholds
- **Caching System**: Intelligent caching of computed high-precision constants
- **Validation**: Built-in verification of constant relationships and accuracy
- **Multiple Algorithms**: Optimal algorithm selection based on precision requirements

## Data Types

### MathematicalConstant
Represents a mathematical constant with metadata:
```runa
Type called "MathematicalConstant":
    name as String                    Note: Human-readable name
    symbol as String                  Note: Mathematical symbol
    value as String                   Note: High-precision value
    precision as Integer              Note: Number of decimal places
    is_rational as Boolean            Note: Whether constant is rational
    mathematical_definition as String Note: Formal definition
    computation_method as String      Note: Algorithm used
```

### PhysicalConstant
Represents a physical constant with units:
```runa
Type called "PhysicalConstant":
    constant_name as String          Note: Official name
    symbol as String                 Note: Standard symbol
    value as String                  Note: Numerical value
    units as String                  Note: Unit specification
    uncertainty as String            Note: Measurement uncertainty
    codata_year as String           Note: CODATA revision year
```

## Universal Mathematical Constants

### Pi (π)
```runa
Note: Get π to default precision
Let pi_value be Constants.get_pi(50)

Note: High precision π computation
Let high_precision_pi be Constants.get_pi(1000)
```

### Euler's Number (e)
```runa
Note: Get e with specified precision
Let e_value be Constants.get_e(50)

Note: Very high precision computation
Let precise_e be Constants.get_e(2000)
```

### Golden Ratio (φ)
```runa
Note: Get golden ratio
Let phi be Constants.get_golden_ratio(50)

Note: Verify φ² = φ + 1 property
Let phi_squared be Operations.multiply(phi, phi, 50)
Let phi_plus_one be Operations.add(phi, "1", 50)
```

### Euler-Mascheroni Constant (γ)
```runa
Note: Get Euler-Mascheroni constant
Let gamma be Constants.get_euler_gamma(50)
```

## Number Theory Constants

### Apéry's Constant (ζ(3))
```runa
Note: Get Apéry constant
Let apery be Constants.get_apery_constant(50)
```

### Catalan's Constant
```runa
Note: Get Catalan constant
Let catalan be Constants.get_catalan_constant(50)
```

### Glaisher-Kinkelin Constant
```runa
Note: Get Glaisher-Kinkelin constant
Let glaisher be Constants.get_glaisher_kinkelin(50)
```

## Physical Constants

### Speed of Light
```runa
Note: Get speed of light in different units
Let c_si be Constants.get_speed_of_light("SI")         Note: m/s
Let c_cgs be Constants.get_speed_of_light("CGS")       Note: cm/s
Let c_natural be Constants.get_speed_of_light("natural") Note: c = 1
```

### Planck Constant
```runa
Note: Get Planck constant
Let h_si be Constants.get_planck_constant("SI")        Note: J⋅s
Let h_cgs be Constants.get_planck_constant("CGS")      Note: erg⋅s
Let h_ev be Constants.get_planck_constant("eV")        Note: eV⋅s
```

### Gravitational Constant
```runa
Note: Get gravitational constant
Let G be Constants.get_gravitational_constant("SI")
Display "G = " joined with G.value joined with " ± " joined with G.uncertainty joined with " " joined with G.units
```

## Computational Constants

### Machine Epsilon
```runa
Note: Get machine epsilon for different types
Let float32_epsilon be Constants.get_machine_epsilon("float32")
Let float64_epsilon be Constants.get_machine_epsilon("float64")
Let decimal128_epsilon be Constants.get_machine_epsilon("decimal128")
```

### Safe Integer Limits
```runa
Note: Get maximum safe integers
Let int32_max be Constants.get_max_safe_integer("int32")
Let int64_max be Constants.get_max_safe_integer("int64")
Let js_safe_max be Constants.get_max_safe_integer("javascript_safe")
```

## Geometric Constants

### Unit Circle Properties
```runa
Note: Circle circumference (2π)
Let circumference be Constants.get_unit_circle_circumference(50)

Note: Unit sphere surface area (4π)
Let sphere_area be Constants.get_unit_sphere_surface_area(50)

Note: Unit sphere volume (4π/3)
Let sphere_volume be Constants.get_unit_sphere_volume(50)
```

## Logarithmic Constants

### Natural Logarithms
```runa
Note: ln(2) and ln(10)
Let ln2 be Constants.get_natural_log_2(50)
Let ln10 be Constants.get_natural_log_10(50)

Note: log₁₀(e) and log₂(e)
Let log10_e be Constants.get_log10_e(50)
Let log2_e be Constants.get_log2_e(50)
```

## Advanced Constant Operations

### Arbitrary Precision Computation
```runa
Note: Compute π using different algorithms
Let pi_machin be Constants.compute_constant_arbitrary_precision("pi", 1000, "machin")
Let pi_chudnovsky be Constants.compute_constant_arbitrary_precision("pi", 1000, "chudnovsky")

Display "Machin formula: " joined with pi_machin["value"]
Display "Method: " joined with pi_machin["method"]
Display "Computation time: " joined with pi_machin["computation_time"] joined with "s"
```

### Algorithm Optimization
```runa
Note: Get optimal algorithm for precision requirement
Let optimal_algo be Constants.optimize_constant_algorithm("pi", 10000)
Display "Optimal algorithm for 10,000 digits: " joined with optimal_algo

Note: Estimate computation time
Let estimated_time be Constants.estimate_computation_time("pi", 10000, optimal_algo)
Display "Estimated time: " joined with String(estimated_time) joined with " seconds"
```

### Constant Validation
```runa
Note: Validate computed constant against known value
Let computed_pi be Constants.get_pi(100)
Let reference_pi be "3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679"
Let is_valid be Constants.validate_constant_precision(computed_pi, reference_pi, 1e-95)

If is_valid:
    Display "Computed π passes validation"
Otherwise:
    Display "Computed π failed validation"
```

## Series Computations

### Pi Series
```runa
Note: Compute π using various series
Let leibniz_pi be Constants.compute_pi_series("leibniz", 50)
Let machin_pi be Constants.compute_pi_series("machin", 50)
Let chudnovsky_pi be Constants.compute_pi_series("chudnovsky", 50)

Display "Leibniz series convergence: " joined with leibniz_pi["convergence_rate"]
Display "Terms used: " joined with leibniz_pi["terms_used"]
```

### E Series
```runa
Note: Compute e using different methods
Let taylor_e be Constants.compute_e_series("taylor", 50)
Let continued_fraction_e be Constants.compute_e_series("continued_fraction", 50)

Display "Taylor series: " joined with taylor_e["value"]
Display "Continued fraction: " joined with continued_fraction_e["value"]
```

### Zeta Function
```runa
Note: Compute Riemann zeta function values
Let zeta_2 be Constants.compute_zeta_function("2", 50)  Note: π²/6
Let zeta_3 be Constants.compute_zeta_function("3", 50)  Note: Apéry constant
Let zeta_4 be Constants.compute_zeta_function("4", 50)  Note: π⁴/90
```

## Constant Relationships

### Verify Mathematical Identities
```runa
Note: Verify Euler's identity: e^(iπ) joined with 1 = 0
Let relationships be Constants.verify_constant_relationships(["euler_identity"], 50)
For Each verification in relationships:
    Display verification["relationship"] joined with " verified: " joined with verification["verified"]
    If verification["verified"] != "True":
        Display "Error: " joined with verification["error"]
```

### Derive Constants from Others
```runa
Note: Derive π from ζ(2) = π²/6
Let pi_from_zeta be Constants.derive_constant_from_others("pi", ["zeta_2"], 50)
Display "π derived from ζ(2: " joined with pi_from_zeta)

Note: Derive golden ratio from √5
Let phi_from_sqrt5 be Constants.derive_constant_from_others("golden_ratio", ["sqrt_5"], 50)
```

## Rational Approximations

### Find Rational Approximations
```runa
Note: Find rational approximations to π
Let pi_approximations be Constants.find_rational_approximations(Constants.get_pi(50), 10000)
For Each approx in pi_approximations:
    Let numerator be approx["numerator"]
    Let denominator be approx["denominator"]
    Let error be approx["error"]
    Display numerator joined with "/" joined with denominator joined with " (error: " joined with error joined with "")
```

## Caching System

### Cache Management
```runa
Note: Cache computed constant
Let cached_pi be Constants.get_pi(1000)
Let storage_options be Dictionary with:
    "cache_directory": "/tmp/runa_constants"
    "compression": "true"

Let cache_success be Constants.cache_computed_constant(
    cached_pi, 
    storage_options
)

Note: Load cached constant
Try:
    Let loaded_constant be Constants.load_cached_constant("pi", 1000)
    Display "Loaded from cache: " joined with loaded_constant.value
Catch Errors.NotFound:
    Display "Constant not found in cache"
```

### Precision Management
```runa
Note: Manage different precision levels
Let precision_requirements be Dictionary with:
    "pi": 500
    "e": 300
    "golden_ratio": 100

Let precision_status be Constants.manage_constant_precision_levels(precision_requirements)
For Each constant, status in precision_status:
    Display constant joined with ": " joined with status
```

## Benchmarking

### Performance Comparison
```runa
Note: Compare constant computation methods
Let methods be ["pi_machin", "pi_chudnovsky", "e_taylor", "golden_ratio_algebraic"]
Let precision_levels be [50, 100, 200, 500]

Let benchmark_results be Constants.benchmark_constant_computation(methods, precision_levels)
For Each method, results in benchmark_results:
    Display "Method: " joined with method
    Display "Average time: " joined with String(results["average_computation_time"]) joined with "s"
    Display "Success rate: " joined with String(results["success_rate"]) joined with "%"
```

### Precision Comparison
```runa
Note: Compare precision of different values
Let computed_values be [
    Constants.get_pi(50),
    Constants.get_e(50),
    Constants.get_golden_ratio(50)
]

Let precision_comparison be Constants.compare_constant_precisions(computed_values, 50)
Display "Overall precision score: " joined with String(precision_comparison["overall_precision"])
```

## Statistical Constants

### Normal Distribution
```runa
Note: Get normalization constant for normal distribution
Let normal_norm be Constants.get_normal_distribution_normalization(50)
Display "1/√(2π = " joined with normal_norm)

Note: Stirling's approximation constant
Let stirling_const be Constants.get_stirling_approximation_constant(50)
Display "√(2π = " joined with stirling_const)
```

### Chi-squared Distribution
```runa
Note: Get normalization constant for chi-squared distribution
Let chi_norm be Constants.get_chi_squared_normalization(5, 50)  Note: 5 degrees of freedom
Display "Chi-squared normalization: " joined with chi_norm
```

## Error Handling

The constants module provides comprehensive error handling:

- **Precision Errors**: Invalid precision specifications
- **Computation Errors**: Failed series convergence
- **Domain Errors**: Invalid parameter ranges
- **Cache Errors**: Storage and retrieval failures

```runa
Try:
    Let invalid_precision be Constants.get_pi(-10)
Catch Errors.InvalidOperation as error:
    Display "Error: " joined with error.message
    Let suggestion be SuggestionEngine.get_suggestion(error)
    Display "Suggestion: " joined with suggestion
```

## Performance Considerations

- **Algorithm Selection**: Use `optimize_constant_algorithm()` for best performance
- **Caching**: Cache frequently used high-precision constants
- **Precision Planning**: Request only necessary precision to minimize computation time
- **Batch Operations**: Group related constant computations together

## Best Practices

1. **Choose Appropriate Precision**: Higher precision increases computation time exponentially
2. **Use Caching**: Cache expensive high-precision computations
3. **Validate Results**: Verify critical constants against known references
4. **Handle Errors**: Always wrap constant computations in error handling
5. **Monitor Performance**: Use benchmarking for performance-critical applications
6. **Algorithm Awareness**: Understand convergence properties of different algorithms