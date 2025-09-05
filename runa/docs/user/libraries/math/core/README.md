Note: Math Core Module

The Math Core module (`math/core`) provides the fundamental mathematical operations and utilities that form the foundation of Runa's mathematical computing capabilities. This module offers high-precision arithmetic, comprehensive trigonometric functions, mathematical constants, comparison operations, and unit conversions.

## Module Overview

The Math Core module consists of five specialized submodules, each focusing on a specific area of mathematical computation:

| Submodule | Description | Key Features |
|-----------|-------------|--------------|
| **[Constants](constants.md)** | Mathematical constants with arbitrary precision | π, e, φ, physical constants, computational limits |
| **[Operations](operations.md)** | Fundamental arithmetic operations | Basic math, power/root, logarithms, factorials, complex numbers |
| **[Comparison](comparison.md)** | Mathematical comparison and ordering | Tolerance-based comparisons, sorting, ranking, statistical ordering |
| **[Trigonometry](trigonometry.md)** | Trigonometric and hyperbolic functions | Sin/cos/tan, inverse functions, angle conversions, complex trig |
| **[Conversion](conversion.md)** | Unit and format conversions | Angular units, number bases, coordinates, temperatures, scientific notation |

## Quick Start

### Basic Arithmetic
```runa
Import "math/core/operations" as Operations

Note: High-precision arithmetic
Let sum be Operations.add("123.456", "789.012", 50)
Let product be Operations.multiply("3.14159", "2.71828", 30)
Let sqrt_2 be Operations.square_root("2", 100)

Display "Sum: " joined with sum.result_value
Display "Product: " joined with product.result_value
Display "√2: " joined with sqrt_2.result_value
```

### Mathematical Constants
```runa
Import "math/core/constants" as Constants

Note: Get high-precision constants
Let pi be Constants.get_pi(50)
Let e be Constants.get_e(50)
Let golden_ratio be Constants.get_golden_ratio(50)

Display "π = " joined with pi
Display "e = " joined with e
Display "φ = " joined with golden_ratio
```

### Trigonometric Functions
```runa
Import "math/core/trigonometry" as Trig

Note: Trigonometric calculations
Let angle be "1.5708"  Note: π/2 radians
Let sine_result be Trig.sine(angle, "radians", 30)
Let cosine_result be Trig.cosine(angle, "radians", 30)

Display "sin(π/2 = " joined with sine_result.function_value)
Display "cos(π/2 = " joined with cosine_result.function_value)
```

### Comparisons and Sorting
```runa
Import "math/core/comparison" as Compare

Note: Tolerance-based comparison
Let tolerance_config be ToleranceConfiguration with:
    absolute_tolerance: "0.001"
    relative_tolerance: "0.01"
    comparison_method: "combined"

Let are_equal be Compare.equal_within_tolerance("3.14159", "3.14160", tolerance_config)
Display "Values are equal within tolerance: " joined with String(are_equal.result)

Note: Sort array of numbers
Let values be ["3.7", "1.2", "5.9", "2.1", "4.8"]
Let sorted_result be Compare.sort_ascending(values, Dictionary with: "stable": "true")

Display "Sorted values:"
For Each value in sorted_result.sorted_values:
    Display "  " joined with value
```

### Unit Conversions
```runa
Import "math/core/conversion" as Convert

Note: Convert between units
Let celsius be "25.0"
Let fahrenheit be Convert.celsius_to_fahrenheit(celsius, 10)
Let angle_deg be "180"
Let angle_rad be Convert.angle_to_radians(angle_deg, 30)

Display "25°C = " joined with fahrenheit.converted_value joined with "°F"
Display "180° = " joined with angle_rad.converted_value joined with " radians"
```

## Architecture and Design

### High-Precision Arithmetic
All mathematical operations in the Math Core module support arbitrary precision arithmetic:

- **BigDecimal Integration**: Uses the `math/engine/bigdecimal` module for precise calculations
- **Configurable Precision**: User-specified precision for all operations
- **Error Estimation**: Numerical error bounds for critical calculations
- **Stable Algorithms**: Numerically stable implementations (Kahan summation, etc.)

### Error Handling
Comprehensive error handling with diagnostic integration:

```runa
Try:
    Let result be Operations.divide("10", "0", 50)
Catch Errors.MathematicalError as error:
    Display "Error: " joined with error.message
    Display "Error code: " joined with error.diagnostic_info.error_code
    
    Let suggestion be SuggestionEngine.get_suggestion(error)
    Display "Suggestion: " joined with suggestion
```

### Performance Optimization
The module includes several performance optimization features:

- **Algorithm Selection**: Automatic selection of optimal algorithms based on input characteristics
- **Parallel Processing**: Multi-threaded operations for large datasets
- **Caching**: Intelligent caching of expensive computations
- **Vectorization**: Batch operations for arrays of values

## Advanced Features

### Complex Number Support
Full complex number arithmetic with both rectangular and polar representations:

```runa
Let z1 be ComplexNumber with:
    real_part: "3.0"
    imaginary_part: "4.0"
    precision: 50

Let z2 be ComplexNumber with:
    real_part: "1.0"
    imaginary_part: "-2.0"
    precision: 50

Let sum be Operations.complex_add(z1, z2)
Let product be Operations.complex_multiply(z1, z2)
```

### Statistical Operations
Statistical comparison and ordering operations:

```runa
Note: Statistical comparisons
Let sample_a be ["5.1", "4.9", "5.3", "4.8", "5.0"]
Let sample_b be ["6.2", "5.8", "6.1", "6.0", "5.9"]

Let stat_comparison be Compare.compare_distributions(sample_a, sample_b, "t-test")
Display "P-value: " joined with String(stat_comparison.p_value)

Note: Percentile calculations
Let dataset be ["1", "3", "5", "7", "9", "11", "13", "15", "17", "19"]
Let percentile_75 be Compare.percentile(dataset, 75.0, "linear")
Display "75th percentile: " joined with percentile_75
```

### Series Computations
Advanced series computations for mathematical constants:

```runa
Note: Compute π using different algorithms
Let machin_pi be Constants.compute_pi_series("machin", 100)
Let chudnovsky_pi be Constants.compute_pi_series("chudnovsky", 100)

Display "Machin formula: " joined with machin_pi["value"]
Display "Chudnovsky algorithm: " joined with chudnovsky_pi["value"]
Display "Convergence rate: " joined with chudnovsky_pi["convergence_rate"]
```

## Integration with Other Modules

### Engine Dependencies
The Math Core module integrates with several engine modules:

- **BigDecimal Engine**: High-precision arithmetic operations
- **Numerical Core**: Advanced numerical methods (Newton-Raphson, series expansions)
- **Root Finding**: Root finding algorithms for power and root operations

### Compiler Integration
- **Diagnostic Engine**: Error reporting and suggestions
- **Error Formatter**: Formatted error messages
- **Type Validation**: Input validation for mathematical operations

### System Integration
- **Memory Management**: Efficient handling of high-precision numbers
- **Performance Monitoring**: Benchmarking and optimization tools

## Common Use Cases

### Scientific Computing
```runa
Note: Calculate orbital period using Kepler's third law
Import "math/core/constants" as Constants
Import "math/core/operations" as Ops

Let G be Constants.get_gravitational_constant("SI")  Note: 6.674×10⁻¹¹ m³⋅kg⁻¹⋅s⁻²
Let M_earth be "5.972e24"  Note: kg
Let r_orbit be "4.22e7"    Note: meters (geostationary orbit)

Let GM be Ops.multiply(G.value, M_earth, 50)
Let r_cubed be Ops.power(r_orbit, "3", 50)
Let period_squared be Ops.divide(Ops.multiply("4", Constants.get_pi(20), 20).result_value joined with "^2", GM.result_value, 50)

Let period be Ops.square_root(period_squared.result_value, 30)
Display "Orbital period: " joined with period.result_value joined with " seconds"
```

### Engineering Calculations
```runa
Note: Signal processing: convert frequency to wavelength
Import "math/core/conversion" as Convert
Import "math/core/constants" as Constants

Let frequency be "2.4e9"  Note: 2.4 GHz (WiFi)
Let c be Constants.get_speed_of_light("SI")

Let wavelength be Ops.divide(c.value, frequency, 30)
Let wavelength_cm be Convert.convert_length_units(wavelength.result_value, "meters", 20)

Display "2.4 GHz wavelength: " joined with wavelength_cm["centimeters"] joined with " cm"
```

### Financial Mathematics
```runa
Note: Compound interest calculation
Let principal be "10000"    Note: $10,000
Let annual_rate be "0.05"   Note: 5%
Let time_years be "10"      Note: 10 years
Let compounds_per_year be "12"  Note: Monthly compounding

Note: A = P(1 + r/n)^(nt)
Let rate_per_compound be Ops.divide(annual_rate, compounds_per_year, 20)
Let exponent be Ops.multiply(compounds_per_year, time_years, 20)
Let base be Ops.add("1", rate_per_compound.result_value, 20)
Let compound_factor be Ops.power(base.result_value, exponent.result_value, 20)
Let final_amount be Ops.multiply(principal, compound_factor.result_value, 20)

Display "Final amount: $" joined with final_amount.result_value
```

## Performance Guidelines

### Precision vs. Performance
- **Low Precision (1-15 digits)**: Very fast, suitable for most calculations
- **Medium Precision (16-50 digits)**: Good balance for scientific computing
- **High Precision (51-200 digits)**: Slower but necessary for critical calculations
- **Ultra-High Precision (200+ digits)**: Use only when absolutely necessary

### Memory Optimization
```runa
Note: Efficient batch operations
Let large_dataset be generate_array(10000)

Note: Use vectorized operations instead of loops
Let results be Compare.vectorized_comparison(array_a, array_b, "less_than")

Note: Use parallel processing for heavy computations
Let parallel_options be Dictionary with:
    "thread_count": "4"
    "precision": "30"

Let parallel_sum be Ops.parallel_arithmetic("sum", large_dataset, parallel_options)
```

### Algorithm Selection
```runa
Note: Let the module choose optimal algorithms
Let characteristics be Dictionary with:
    "size_a": "1000"
    "precision": "100"

Let optimal_algo be Ops.select_optimal_algorithm("multiplication", characteristics)
Display "Optimal algorithm: " joined with optimal_algo
```

## Error Handling Best Practices

### Comprehensive Error Catching
```runa
Try:
    Let result be perform_complex_calculation()
Catch Errors.MathematicalError as math_error:
    Display "Mathematical error: " joined with math_error.message
    handle_domain_error(math_error)
Catch Errors.OverflowError as overflow_error:
    Display "Overflow detected: " joined with overflow_error.message
    handle_overflow(overflow_error)
Catch Errors.ComputationError as comp_error:
    Display "Computation failed: " joined with comp_error.message
    handle_computation_failure(comp_error)
```

### Input Validation
```runa
Note: Always validate inputs before computation
Let validation_rules be Dictionary with:
    "numeric": "true"
    "min_value": "-1e100"
    "max_value": "1e100"
    "allow_empty": "false"

Let validation_errors be Ops.validate_operands(operands, "multiplication")
If Length(validation_errors) > 0:
    Display "Validation errors:"
    For Each error in validation_errors:
        Display "  " joined with error
    Return
```

## Testing and Validation

### Unit Testing
```runa
Note: Test mathematical identities
Process called "test_trigonometric_identity":
    Let angle be "1.2345"
    Let precision be 50
    
    Let sin_val be Trig.sine(angle, "radians", precision)
    Let cos_val be Trig.cosine(angle, "radians", precision)
    
    Let sin_squared be Ops.multiply(sin_val.function_value, sin_val.function_value, precision)
    Let cos_squared be Ops.multiply(cos_val.function_value, cos_val.function_value, precision)
    Let identity be Ops.add(sin_squared.result_value, cos_squared.result_value, precision)
    
    Let expected be "1.0"
    Let difference be Ops.subtract(identity.result_value, expected, precision)
    Let tolerance be "1e-45"
    
    Assert Ops.absolute_value(difference.result_value).result_value < tolerance
```

### Benchmarking
```runa
Note: Performance testing
Let operation_types be ["addition", "multiplication", "sine", "square_root"]
Let test_data be create_benchmark_data()

Let benchmark_results be Ops.benchmark_operation_performance(operation_types, test_data)
For Each operation, time in benchmark_results:
    Display operation joined with ": " joined with String(time) joined with " ms average"
```

## Migration and Compatibility

### Version Compatibility
The Math Core module maintains backward compatibility while introducing new features:

- **Constants**: New constants added without breaking existing API
- **Operations**: Enhanced precision support with default fallbacks  
- **Functions**: New optional parameters with sensible defaults

### Legacy Support
```runa
Note: Legacy function calls still work
Let old_style_result be Ops.add("1", "2")  Note: Uses default precision
Let new_style_result be Ops.add("1", "2", 50)  Note: Explicit precision
```

## Contributing and Extensions

### Custom Mathematical Functions
```runa
Note: Extend the module with custom functions
Process called "custom_hyperbolic_function" that takes x as String, precision as Integer returns ArithmeticResult:
    Note: Custom implementation using existing operations
    Let exp_x be Ops.exponential(x, precision)
    Let exp_neg_x be Ops.exponential(Ops.multiply("-1", x, precision).result_value, precision)
    
    Let result be Ops.divide(
        Ops.subtract(exp_x.result_value, exp_neg_x.result_value, precision).result_value,
        "2",
        precision
    )
    
    Return result
```

### Performance Optimizations
```runa
Note: Contribute algorithm improvements
Process called "optimized_factorial" that takes n as Integer returns String:
    If n < 100:
        Return standard_factorial(n)
    Otherwise:
        Return stirling_approximation_with_correction(n)
```

## Related Documentation

- **[Math Engine](../engine/README.md)**: Low-level mathematical engines
- **[Math Statistics](../statistics/README.md)**: Statistical analysis functions
- **[Math Linear Algebra](../linalg/README.md)**: Matrix and vector operations
- **[Math Calculus](../calculus/README.md)**: Differentiation and integration
- **[Math Optimization](../optimization/README.md)**: Optimization algorithms

## Support and Community

For questions, bug reports, or feature requests:

1. **Documentation**: Check the detailed module documentation
2. **Examples**: Review the comprehensive examples in each submodule guide  
3. **Testing**: Run the built-in test suites for validation
4. **Performance**: Use the benchmarking tools to optimize your code

The Math Core module provides the essential mathematical foundation for all scientific, engineering, and analytical computing in Runa. Its high-precision arithmetic, comprehensive function set, and robust error handling make it suitable for both simple calculations and advanced mathematical research.