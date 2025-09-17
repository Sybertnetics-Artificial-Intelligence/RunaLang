Note: Math Core Trigonometry Module

## Overview

The `math/core/trigonometry` module provides comprehensive trigonometric and hyperbolic functions with high precision support. It includes all standard trigonometric functions, their inverses, hyperbolic functions, angle unit conversions, and special angle calculations for scientific and engineering applications.

## Key Features

- **Complete Function Set**: All trigonometric, inverse, and hyperbolic functions
- **Multiple Angle Units**: Radians, degrees, gradians, and turns
- **High Precision**: Arbitrary precision calculations using series expansions
- **Special Angles**: Optimized calculations for common angles (π/6, π/4, π/3, etc.)
- **Complex Trigonometry**: Support for complex-valued trigonometric functions
- **Numerical Stability**: Careful handling of domain boundaries and singularities

## Data Types

### TrigonometricResult
Represents the result of a trigonometric calculation:
```runa
Type called "TrigonometricResult":
    function_value as String        Note: Computed function value
    function_name as String         Note: Function that was computed
    input_angle as String          Note: Original angle input
    angle_unit as String           Note: Unit of angle (radians/degrees)
    precision_used as Integer      Note: Precision level used
    quadrant as Integer            Note: Quadrant of angle (1-4)
    principal_value as Boolean     Note: Whether result is principal value
    computation_method as String   Note: Algorithm used
    error_occurred as Boolean      Note: Error flag
    domain_error as Boolean        Note: Domain error flag
    asymptote_error as Boolean     Note: Asymptote approach error
```

## Basic Trigonometric Functions

### Sine Function
```runa
Note: Sine calculation in different units
Let angle_rad be "1.5708"  Note: π/2 radians
Let angle_deg be "90"      Note: 90 degrees

Let sine_rad be Trigonometry.sine(angle_rad, "radians", 50)
Let sine_deg be Trigonometry.sine(angle_deg, "degrees", 50)

Display "sin(π/2 = " joined with sine_rad.function_value)   Note: Should be ~1
Display "sin(90° = " joined with sine_deg.function_value)   Note: Should be ~1
Display "Quadrant: " joined with String(sine_rad.quadrant)  Note: Should be 1
```

### Cosine Function
```runa
Note: Cosine with high precision
Let angle be "0.0"
Let precision be 100

Let cosine_result be Trigonometry.cosine(angle, "radians", precision)
Display "cos(0 = " joined with cosine_result.function_value)  Note: Should be exactly 1
Display "Method: " joined with cosine_result.computation_method
```

### Tangent Function
```runa
Note: Tangent function with asymptote handling
Let angle be "1.5707"  Note: Close to π/2
Let precision be 50

Try:
    Let tangent_result be Trigonometry.tangent(angle, "radians", precision)
    Display "tan(" joined with angle joined with " = " joined with tangent_result.function_value)
    If tangent_result.asymptote_error:
        Display "Warning: Near asymptote"
Catch Errors.MathematicalError as error:
    Display "Tangent error: " joined with error.message
```

### Cotangent, Secant, and Cosecant
```runa
Note: Reciprocal trigonometric functions
Let angle be "0.7854"  Note: π/4 radians
Let precision be 50

Let cotangent_result be Trigonometry.cotangent(angle, "radians", precision)
Let secant_result be Trigonometry.secant(angle, "radians", precision)
Let cosecant_result be Trigonometry.cosecant(angle, "radians", precision)

Display "cot(π/4 = " joined with cotangent_result.function_value)  Note: Should be 1
Display "sec(π/4 = " joined with secant_result.function_value)     Note: Should be √2
Display "csc(π/4 = " joined with cosecant_result.function_value)   Note: Should be √2
```

## Inverse Trigonometric Functions

### Arcsine
```runa
Note: Inverse sine function
Let value be "0.5"
Let precision be 50

Let arcsine_result be Trigonometry.arcsine(value, "radians", precision)
Display "arcsin(0.5 = " joined with arcsine_result.function_value)  Note: Should be π/6
Display "In degrees: " joined with arcsine_result.function_value joined with " rad = " joined with 
      Trigonometry.convert_angle(arcsine_result.function_value, "radians", "degrees", precision) joined with "°")
```

### Arccosine
```runa
Note: Inverse cosine function
Let value be "0.7071"  Note: Approximately √2/2
Let precision be 50

Let arccosine_result be Trigonometry.arccosine(value, "radians", precision)
Display "arccos(√2/2 ≈ " joined with arccosine_result.function_value)  Note: Should be π/4
Display "Principal value: " joined with String(arccosine_result.principal_value)
```

### Arctangent
```runa
Note: Single-argument arctangent
Let value be "1.0"
Let precision be 50

Let arctangent_result be Trigonometry.arctangent(value, "radians", precision)
Display "arctan(1 = " joined with arctangent_result.function_value)  Note: Should be π/4
```

### Two-Argument Arctangent (atan2)
```runa
Note: Two-argument arctangent for full quadrant resolution
Let y be "1.0"
Let x be "-1.0"
Let precision be 50

Let atan2_result be Trigonometry.arctangent2(y, x, "radians", precision)
Display "atan2(1, -1 = " joined with atan2_result.function_value)  Note: Should be 3π/4
Display "Quadrant: " joined with String(atan2_result.quadrant)      Note: Should be 2
```

## Hyperbolic Functions

### Hyperbolic Sine
```runa
Note: Hyperbolic sine function
Let x be "2.0"
Let precision be 50

Let sinh_result be Trigonometry.hyperbolic_sine(x, precision)
Display "sinh(2 = " joined with sinh_result.function_value)
Display "Method: " joined with sinh_result.computation_method
```

### Hyperbolic Cosine
```runa
Note: Hyperbolic cosine function
Let x be "1.5"
Let precision be 50

Let cosh_result be Trigonometry.hyperbolic_cosine(x, precision)
Display "cosh(1.5 = " joined with cosh_result.function_value)
```

### Hyperbolic Tangent
```runa
Note: Hyperbolic tangent function
Let x be "3.0"
Let precision be 50

Let tanh_result be Trigonometry.hyperbolic_tangent(x, precision)
Display "tanh(3 = " joined with tanh_result.function_value)  Note: Should approach 1
```

### Reciprocal Hyperbolic Functions
```runa
Note: Hyperbolic cotangent, secant, and cosecant
Let x be "2.0"
Let precision be 50

Let coth_result be Trigonometry.hyperbolic_cotangent(x, precision)
Let sech_result be Trigonometry.hyperbolic_secant(x, precision)
Let csch_result be Trigonometry.hyperbolic_cosecant(x, precision)

Display "coth(2 = " joined with coth_result.function_value)
Display "sech(2 = " joined with sech_result.function_value)
Display "csch(2 = " joined with csch_result.function_value)
```

## Inverse Hyperbolic Functions

### Inverse Hyperbolic Sine
```runa
Note: Area hyperbolic sine
Let x be "2.0"
Let precision be 50

Let asinh_result be Trigonometry.inverse_hyperbolic_sine(x, precision)
Display "asinh(2 = " joined with asinh_result.function_value)
```

### Inverse Hyperbolic Cosine
```runa
Note: Area hyperbolic cosine (x ≥ 1)
Let x be "2.0"
Let precision be 50

Try:
    Let acosh_result be Trigonometry.inverse_hyperbolic_cosine(x, precision)
    Display "acosh(2 = " joined with acosh_result.function_value)
Catch Errors.MathematicalError as error:
    Display "Domain error: " joined with error.message
```

### Inverse Hyperbolic Tangent
```runa
Note: Area hyperbolic tangent (|x| < 1)
Let x be "0.5"
Let precision be 50

Try:
    Let atanh_result be Trigonometry.inverse_hyperbolic_tangent(x, precision)
    Display "atanh(0.5 = " joined with atanh_result.function_value)
Catch Errors.MathematicalError as error:
    Display "Domain error: " joined with error.message
```

## Angle Unit Conversions

### Convert Between Units
```runa
Note: Convert angles between different units
Let angle_rad be "1.5708"  Note: π/2 radians
Let precision be 50

Let degrees be Trigonometry.convert_angle(angle_rad, "radians", "degrees", precision)
Let gradians be Trigonometry.convert_angle(angle_rad, "radians", "gradians", precision)
Let turns be Trigonometry.convert_angle(angle_rad, "radians", "turns", precision)

Display angle_rad joined with " radians = " joined with degrees joined with " degrees"
Display angle_rad joined with " radians = " joined with gradians joined with " gradians"
Display angle_rad joined with " radians = " joined with turns joined with " turns"
```

### Angle Normalization
```runa
Note: Normalize angles to principal ranges
Let large_angle be "7.5"  Note: Greater than 2π
Let negative_angle be "-2.5"

Let normalized_positive be Trigonometry.normalize_angle(large_angle, "radians", 50)
Let normalized_negative be Trigonometry.normalize_angle(negative_angle, "radians", 50)

Display "7.5 rad normalized: " joined with normalized_positive
Display "-2.5 rad normalized: " joined with normalized_negative
```

## Special Angle Calculations

### Common Angles
```runa
Note: Exact values for special angles
Let special_angles be ["30", "45", "60", "90"]  Note: degrees
Let precision be 50

For Each angle in special_angles:
    Let sine_val be Trigonometry.sine(angle, "degrees", precision)
    Let cosine_val be Trigonometry.cosine(angle, "degrees", precision)
    Let tangent_val be Trigonometry.tangent(angle, "degrees", precision)
    
    Display angle joined with "°:"
    Display "  sin = " joined with sine_val.function_value
    Display "  cos = " joined with cosine_val.function_value
    Display "  tan = " joined with tangent_val.function_value
```

### π-Based Angles
```runa
Note: Calculations with π fractions
Let pi_fractions be ["π/6", "π/4", "π/3", "π/2"]
Let precision be 50

For Each fraction in pi_fractions:
    Let angle_value be Trigonometry.evaluate_pi_fraction(fraction, precision)
    Let sine_result be Trigonometry.sine(angle_value, "radians", precision)
    Display "sin(" joined with fraction joined with " = " joined with sine_result.function_value)
```

## Complex Trigonometry

### Complex Sine and Cosine
```runa
Note: Complex trigonometric functions
Let complex_angle be ComplexNumber with:
    real_part: "1.0"
    imaginary_part: "0.5"
    precision: 50

Let complex_sine be Trigonometry.complex_sine(complex_angle)
Let complex_cosine be Trigonometry.complex_cosine(complex_angle)

Display "sin(1 joined with 0.5i = " joined with complex_sine.real_part joined with " joined with " joined with complex_sine.imaginary_part joined with "i")
Display "cos(1 joined with 0.5i = " joined with complex_cosine.real_part joined with " joined with " joined with complex_cosine.imaginary_part joined with "i")
```

### Euler's Formula
```runa
Note: e^(ix) = cos(x) joined with i*sin(x)
Let x be "2.0"
Let precision be 50

Let euler_result be Trigonometry.euler_formula(x, precision)
Display "e^(2i = " joined with euler_result.real_part joined with " joined with " joined with euler_result.imaginary_part joined with "i")

Note: Verify with separate calculations
Let cos_x be Trigonometry.cosine(x, "radians", precision)
Let sin_x be Trigonometry.sine(x, "radians", precision)
Display "cos(2 = " joined with cos_x.function_value)
Display "sin(2 = " joined with sin_x.function_value)
```

## Trigonometric Identities

### Pythagorean Identity
```runa
Note: Verify sin²(x) joined with cos²(x) = 1
Let angle be "1.2345"
Let precision be 50

Let sine_val be Trigonometry.sine(angle, "radians", precision)
Let cosine_val be Trigonometry.cosine(angle, "radians", precision)

Let sine_squared be Operations.multiply(sine_val.function_value, sine_val.function_value, precision)
Let cosine_squared be Operations.multiply(cosine_val.function_value, cosine_val.function_value, precision)
Let identity_check be Operations.add(sine_squared.result_value, cosine_squared.result_value, precision)

Display "sin²(" joined with angle joined with " joined with cos²(" joined with angle joined with ") = " joined with identity_check.result_value)
```

### Angle Sum Formulas
```runa
Note: sin(A joined with B) = sin(A)cos(B) joined with cos(A)sin(B)
Let angle_a be "0.5"
Let angle_b be "0.8"
Let precision be 50

Let sum_angle be Operations.add(angle_a, angle_b, precision)
Let sin_sum_direct be Trigonometry.sine(sum_angle.result_value, "radians", precision)

Let sin_a be Trigonometry.sine(angle_a, "radians", precision)
Let cos_a be Trigonometry.cosine(angle_a, "radians", precision)
Let sin_b be Trigonometry.sine(angle_b, "radians", precision)
Let cos_b be Trigonometry.cosine(angle_b, "radians", precision)

Let term1 be Operations.multiply(sin_a.function_value, cos_b.function_value, precision)
Let term2 be Operations.multiply(cos_a.function_value, sin_b.function_value, precision)
Let sin_sum_formula be Operations.add(term1.result_value, term2.result_value, precision)

Display "sin(" joined with angle_a joined with " joined with " joined with angle_b joined with " direct = " joined with sin_sum_direct.function_value)
Display "sin(" joined with angle_a joined with " joined with " joined with angle_b joined with " formula = " joined with sin_sum_formula.result_value)
```

### Double Angle Formulas
```runa
Note: cos(2x) = cos²(x) - sin²(x) = 2cos²(x) - 1 = 1 - 2sin²(x)
Let angle be "0.6"
Let precision be 50

Let double_angle be Operations.multiply("2", angle, precision)
Let cos_2x_direct be Trigonometry.cosine(double_angle.result_value, "radians", precision)

Let cos_x be Trigonometry.cosine(angle, "radians", precision)
Let sin_x be Trigonometry.sine(angle, "radians", precision)

Note: First formula: cos²(x) - sin²(x)
Let cos_squared be Operations.multiply(cos_x.function_value, cos_x.function_value, precision)
Let sin_squared be Operations.multiply(sin_x.function_value, sin_x.function_value, precision)
Let cos_2x_formula1 be Operations.subtract(cos_squared.result_value, sin_squared.result_value, precision)

Display "cos(2×" joined with angle joined with " direct = " joined with cos_2x_direct.function_value)
Display "cos(2×" joined with angle joined with " formula = " joined with cos_2x_formula1.result_value)
```

## Spherical Trigonometry

### Spherical Triangle
```runa
Note: Law of cosines for spherical triangles
Note: cos(c) = cos(a)cos(b) joined with sin(a)sin(b)cos(C)
Let side_a be "1.2"  Note: radians
Let side_b be "0.8"
Let angle_c be "1.5"
Let precision be 50

Let spherical_result be Trigonometry.spherical_law_of_cosines(side_a, side_b, angle_c, precision)
Display "Spherical law of cosines result: " joined with spherical_result.function_value
```

### Great Circle Distance
```runa
Note: Distance between two points on a sphere
Let lat1 be "40.7128"  Note: New York latitude (degrees)
Let lon1 be "-74.0060" # New York longitude
Let lat2 be "51.5074"  Note: London latitude
Let lon2 be "-0.1278"  Note: London longitude
Let radius be "6371"   Note: Earth radius in km

Let great_circle_dist be Trigonometry.great_circle_distance(lat1, lon1, lat2, lon2, radius, 50)
Display "Distance from NYC to London: " joined with great_circle_dist joined with " km"
```

## Periodic Function Properties

### Period Detection
```runa
Note: Determine fundamental period of trigonometric expressions
Let amplitude be "2.5"
Let frequency be "3.0"
Let phase be "0.5"

Let period be Trigonometry.calculate_period(frequency, "sine")
Display "Period of " joined with amplitude joined with "sin(" joined with frequency joined with "x joined with " joined with phase joined with " = " joined with period)
```

### Phase Analysis
```runa
Note: Analyze phase relationships between trigonometric functions
Let func1_params be Dictionary with: "amplitude": "1", "frequency": "2", "phase": "0"
Let func2_params be Dictionary with: "amplitude": "1", "frequency": "2", "phase": "1.5708"

Let phase_diff be Trigonometry.phase_difference(func1_params, func2_params)
Display "Phase difference: " joined with phase_diff joined with " radians"
```

## Numerical Methods

### Series Expansion Control
```runa
Note: Control Taylor series expansion parameters
Let angle be "10.0"  Note: Large angle requiring many terms
Let series_config be Dictionary with:
    "max_terms": "100"
    "convergence_tolerance": "1e-50"
    "acceleration_method": "euler"

Let sine_result be Trigonometry.sine_series_expansion(angle, "radians", series_config, 50)
Display "sin(10 with series expansion: " joined with sine_result.function_value)
Display "Terms used: " joined with String(sine_result.terms_used)
Display "Convergence achieved: " joined with String(sine_result.convergence_achieved)
```

### Argument Reduction
```runa
Note: Efficient argument reduction for large angles
Let very_large_angle be "1000000.0"
Let precision be 30

Let reduced_angle be Trigonometry.reduce_argument(very_large_angle, "radians", precision)
Display "Original angle: " joined with very_large_angle
Display "Reduced angle: " joined with reduced_angle["reduced_angle"]
Display "Reduction factor: " joined with reduced_angle["reduction_factor"]

Let sine_large be Trigonometry.sine(very_large_angle, "radians", precision)
Display "sin(1000000 = " joined with sine_large.function_value)
```

## Performance Optimization

### Lookup Tables
```runa
Note: Use precomputed lookup tables for common angles
Let lookup_config be Dictionary with:
    "resolution": "0.001"  Note: radians
    "range_min": "0"
    "range_max": "6.283185307179586"  Note: 2π
    "interpolation": "linear"

Let lookup_table be Trigonometry.create_lookup_table("sine", lookup_config, 50)
Let fast_sine be Trigonometry.lookup_sine("1.5", lookup_table)
Display "Fast sine lookup: " joined with fast_sine
```

### Vectorized Operations
```runa
Note: Compute trigonometric functions for arrays
Let angles be ["0", "0.5", "1.0", "1.5", "2.0", "2.5", "3.0"]
Let precision be 30

Let sine_values be Trigonometry.vectorized_sine(angles, "radians", precision)
Display "Vectorized sine calculation:"
For i from 0 to Length(angles) - 1:
    Display "  sin(" joined with angles[i] joined with " = " joined with sine_values[i])
```

## Error Handling

The trigonometry module provides comprehensive error handling:

```runa
Note: Domain errors for inverse functions
Try:
    Let invalid_arcsin be Trigonometry.arcsine("2.0", "radians", 50)
Catch Errors.MathematicalError as error:
    Display "Domain error: " joined with error.message
    If error.diagnostic_info.error_code equals "TRIG_DOMAIN_ERROR":
        Display "Suggestion: Arcsine domain is [-1, 1]"

Note: Asymptote errors
Try:
    Let pi_half be Constants.get_pi(50)
    Let half_pi be Operations.divide(pi_half, "2", 50)
    Let tangent_asymptote be Trigonometry.tangent(half_pi.result_value, "radians", 50)
Catch Errors.MathematicalError as error:
    Display "Asymptote error: " joined with error.message

Note: Convergence failures
Try:
    Let problematic_series be Trigonometry.sine("1000", "radians", 200)
    If problematic_series.series_convergence_failed:
        Display "Warning: Series convergence may be poor"
Catch Errors.ComputationError as error:
    Display "Computation error: " joined with error.message
```

## Performance Considerations

- **Argument Reduction**: Large angles are automatically reduced to improve accuracy
- **Series Convergence**: Higher precision may require more terms in series expansions
- **Special Angles**: Use exact values when possible for common angles
- **Lookup Tables**: Consider precomputed tables for repeated calculations

## Best Practices

1. **Choose Appropriate Units**: Use radians for mathematical calculations, degrees for user interfaces
2. **Handle Domain Errors**: Always check domains for inverse functions
3. **Use Proper Precision**: Balance accuracy requirements with computational cost
4. **Normalize Angles**: Normalize large angles to avoid numerical issues
5. **Verify Identities**: Use trigonometric identities to verify critical calculations
6. **Consider Complex Numbers**: Use complex trigonometry for advanced applications