# Runa Standard Library: Math Module

## Overview

The `math/core` module provides comprehensive mathematical functions for Runa programs including arithmetic, trigonometry, logarithms, statistics, constants, and advanced mathematical operations. The module supports both natural language syntax and helper functions for advanced use cases.

## Features

- **Core Operations**: Basic arithmetic, comparison, and rounding functions
- **Trigonometric Functions**: Complete set of trig and hyperbolic functions
- **Logarithmic and Exponential**: Natural, base-10, base-2, and custom base logarithms
- **Special Functions**: Gamma, error functions, factorial, and combinatorial functions
- **Number Theory**: Prime testing, factorization, totient, and modular arithmetic
- **Combinatorics**: Binomial coefficients, multinomial, and Stirling numbers
- **Statistical Functions**: Mean, median, mode, variance, skewness, and kurtosis
- **Random Number Generation**: Uniform, normal, and exponential distributions
- **Vector Operations**: Dot product, cross product, normalization, and scaling
- **Complex Numbers**: Full complex arithmetic and functions
- **Polynomial and Interpolation**: Evaluation and various interpolation methods
- **Financial Mathematics**: Interest calculations, present/future value, annuities
- **Numerical Analysis**: Root finding, integration, and optimization
- **Series and Sequences**: Fibonacci, geometric, and arithmetic series
- **Cryptography Support**: Modular arithmetic and Chinese remainder theorem

## Mathematical Constants

- `pi` - Mathematical constant π (3.141592653589793)
- `e` - Natural logarithm base (2.718281828459045)
- `tau` - 2π (6.283185307179586)
- `phi` - Golden ratio (1.618033988749895)
- `gamma_euler` - Euler-Mascheroni constant (0.5772156649015329)
- `sqrt2` - Square root of 2 (1.4142135623730951)
- `sqrt3` - Square root of 3 (1.7320508075688772)
- `ln2` - Natural logarithm of 2 (0.6931471805599453)
- `ln10` - Natural logarithm of 10 (2.302585092994046)
- `infinity` - Positive infinity
- `negative_infinity` - Negative infinity
- `nan` - Not a Number

## Core API

### Basic Arithmetic
- `Process called "add" that takes a as Number and b as Number returns Number`
- `Process called "subtract" that takes a as Number and b as Number returns Number`
- `Process called "multiply" that takes a as Number and b as Number returns Number`
- `Process called "divide" that takes a as Number and b as Number returns Number`
- `Process called "modulo" that takes a as Number and b as Number returns Number`
- `Process called "floor_divide" that takes a as Number and b as Number returns Number`
- `Process called "power" that takes base as Number and exponent as Number returns Number`
- `Process called "sqrt" that takes x as Number returns Number`
- `Process called "cbrt" that takes x as Number returns Number`
- `Process called "nth_root" that takes x as Number and n as Number returns Number`

### Comparison and Selection
- `Process called "min" that takes a as Number and b as Number returns Number`
- `Process called "max" that takes a as Number and b as Number returns Number`
- `Process called "clamp" that takes value as Number and min_val as Number and max_val as Number returns Number`
- `Process called "sign" that takes x as Number returns Number`
- `Process called "copysign" that takes x as Number and y as Number returns Number`

### Absolute Value and Rounding
- `Process called "abs" that takes x as Number returns Number`
- `Process called "floor" that takes x as Number returns Number`
- `Process called "ceil" that takes x as Number returns Number`
- `Process called "round" that takes x as Number returns Number`
- `Process called "trunc" that takes x as Number returns Number`
- `Process called "round_to" that takes x as Number and decimals as Integer returns Number`

## Trigonometric Functions

### Basic Trigonometric (Radians)
- `Process called "sin" that takes angle as Number returns Number`
- `Process called "cos" that takes angle as Number returns Number`
- `Process called "tan" that takes angle as Number returns Number`
- `Process called "asin" that takes x as Number returns Number`
- `Process called "acos" that takes x as Number returns Number`
- `Process called "atan" that takes x as Number returns Number`
- `Process called "atan2" that takes y as Number and x as Number returns Number`
- `Process called "sinc" that takes x as Number returns Number`

### Hyperbolic Functions
- `Process called "sinh" that takes x as Number returns Number`
- `Process called "cosh" that takes x as Number returns Number`
- `Process called "tanh" that takes x as Number returns Number`
- `Process called "asinh" that takes x as Number returns Number`
- `Process called "acosh" that takes x as Number returns Number`
- `Process called "atanh" that takes x as Number returns Number`
- `Process called "sech" that takes x as Number returns Number`
- `Process called "csch" that takes x as Number returns Number`
- `Process called "coth" that takes x as Number returns Number`

## Logarithmic and Exponential Functions

- `Process called "log" that takes x as Number returns Number`
- `Process called "log10" that takes x as Number returns Number`
- `Process called "log2" that takes x as Number returns Number`
- `Process called "log_base" that takes x as Number and base as Number returns Number`
- `Process called "log1p" that takes x as Number returns Number`
- `Process called "exp" that takes x as Number returns Number`
- `Process called "exp2" that takes x as Number returns Number`
- `Process called "expm1" that takes x as Number returns Number`
- `Process called "pow" that takes base as Number and exponent as Number returns Number`

## Special Mathematical Functions

- `Process called "gamma" that takes x as Number returns Number`
- `Process called "lgamma" that takes x as Number returns Number`
- `Process called "erf" that takes x as Number returns Number`
- `Process called "erfc" that takes x as Number returns Number`
- `Process called "factorial" that takes n as Integer returns Integer`
- `Process called "double_factorial" that takes n as Integer returns Integer`
- `Process called "gcd" that takes a as Integer and b as Integer returns Integer`
- `Process called "lcm" that takes a as Integer and b as Integer returns Integer`
- `Process called "extended_gcd" that takes a as Integer and b as Integer returns (Integer, Integer, Integer)`

## Number Theory Functions

- `Process called "is_prime" that takes n as Integer returns Boolean`
- `Process called "next_prime" that takes n as Integer returns Integer`
- `Process called "prime_factors" that takes n as Integer returns List[Integer]`
- `Process called "totient" that takes n as Integer returns Integer`
- `Process called "mobius" that takes n as Integer returns Integer`

## Combinatorics Functions

- `Process called "binomial" that takes n as Integer and k as Integer returns Integer`
- `Process called "multinomial" that takes n as Integer and k_list as List[Integer] returns Integer`
- `Process called "stirling_first" that takes n as Integer and k as Integer returns Integer`
- `Process called "stirling_second" that takes n as Integer and k as Integer returns Integer`

## Number Classification and Testing

- `Process called "is_finite" that takes x as Number returns Boolean`
- `Process called "is_infinite" that takes x as Number returns Boolean`
- `Process called "is_nan" that takes x as Number returns Boolean`
- `Process called "is_integer" that takes x as Number returns Boolean`
- `Process called "is_positive" that takes x as Number returns Boolean`
- `Process called "is_negative" that takes x as Number returns Boolean`
- `Process called "is_zero" that takes x as Number returns Boolean`
- `Process called "is_close" that takes a as Number and b as Number and rel_tol as Number returns Boolean`

## Angle Conversion Functions

- `Process called "degrees_to_radians" that takes degrees as Number returns Number`
- `Process called "radians_to_degrees" that takes radians as Number returns Number`
- `Process called "normalize_angle" that takes angle as Number returns Number`

## Advanced Statistical Functions

- `Process called "mean" that takes values as List[Number] returns Number`
- `Process called "median" that takes values as List[Number] returns Number`
- `Process called "mode" that takes values as List[Number] returns Number`
- `Process called "variance" that takes values as List[Number] returns Number`
- `Process called "std_dev" that takes values as List[Number] returns Number`
- `Process called "skewness" that takes values as List[Number] returns Number`
- `Process called "kurtosis" that takes values as List[Number] returns Number`

## Random Number Generation

- `Process called "random" that returns Number`
- `Process called "random_range" that takes min_val as Number and max_val as Number returns Number`
- `Process called "random_int" that takes min_val as Integer and max_val as Integer returns Integer`
- `Process called "random_normal" that takes mean as Number and std_dev as Number returns Number`
- `Process called "random_exponential" that takes lambda_val as Number returns Number`

## Vector and Matrix Operations

- `Process called "dot_product" that takes a as List[Number] and b as List[Number] returns Number`
- `Process called "vector_norm" that takes v as List[Number] returns Number`
- `Process called "vector_add" that takes a as List[Number] and b as List[Number] returns List[Number]`
- `Process called "vector_scale" that takes v as List[Number] and scalar as Number returns List[Number]`
- `Process called "vector_cross" that takes a as List[Number] and b as List[Number] returns List[Number]`

## Complex Number Support

### Complex Class
- `real as Number` - Real part
- `imag as Number` - Imaginary part
- `Process called "conjugate" that takes self returns Complex`
- `Process called "magnitude" that takes self returns Number`
- `Process called "phase" that takes self returns Number`

### Complex Operations
- `Process called "complex" that takes real as Number and imag as Number returns Complex`
- `Process called "complex_add" that takes a as Complex and b as Complex returns Complex`
- `Process called "complex_multiply" that takes a as Complex and b as Complex returns Complex`
- `Process called "complex_divide" that takes a as Complex and b as Complex returns Complex`
- `Process called "complex_power" that takes a as Complex and n as Number returns Complex`

## Polynomial and Interpolation Functions

- `Process called "evaluate_polynomial" that takes coefficients as List[Number] and x as Number returns Number`
- `Process called "linear_interpolate" that takes x as Number and x1 as Number and y1 as Number and x2 as Number and y2 as Number returns Number`
- `Process called "cubic_interpolate" that takes x as Number and x0 as Number and y0 as Number and x1 as Number and y1 as Number and x2 as Number and y2 as Number and x3 as Number and y3 as Number returns Number`

## Financial Mathematics

- `Process called "compound_interest" that takes principal as Number and rate as Number and time as Number and periods as Integer returns Number`
- `Process called "simple_interest" that takes principal as Number and rate as Number and time as Number returns Number`
- `Process called "present_value" that takes future_value as Number and rate as Number and time as Number returns Number`
- `Process called "future_value" that takes present_value as Number and rate as Number and time as Number returns Number`
- `Process called "annuity_payment" that takes principal as Number and rate as Number and periods as Integer returns Number`

## Numerical Analysis

- `Process called "newton_raphson" that takes f as Process and df as Process and x0 as Number and tolerance as Number returns Number`
- `Process called "bisection" that takes f as Process and a as Number and b as Number and tolerance as Number returns Number`
- `Process called "trapezoidal_integration" that takes f as Process and a as Number and b as Number and n as Integer returns Number`
- `Process called "simpson_integration" that takes f as Process and a as Number and b as Number and n as Integer returns Number`

## Series and Sequences

- `Process called "fibonacci" that takes n as Integer returns Integer`
- `Process called "fibonacci_sequence" that takes n as Integer returns List[Integer]`
- `Process called "geometric_series" that takes a as Number and r as Number and n as Integer returns Number`
- `Process called "arithmetic_series" that takes a as Number and d as Number and n as Integer returns Number`

## Cryptography Support

- `Process called "modular_power" that takes base as Integer and exponent as Integer and modulus as Integer returns Integer`
- `Process called "modular_inverse" that takes a as Integer and m as Integer returns Integer`
- `Process called "chinese_remainder" that takes remainders as List[Integer] and moduli as List[Integer] returns Integer`

## Usage Examples

### Basic Arithmetic
```runa
Let result be add with a as 5 and b as 3
Let product be multiply with a as 4 and b as 7
Let power_val be power with base as 2 and exponent as 8
```

### Trigonometric Functions
```runa
Let angle be degrees_to_radians with degrees as 45
Let sin_val be sin with angle as angle
Let cos_val be cos with angle as angle
```

### Statistical Functions
```runa
Let values be list containing 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
Let mean_val be mean with values as values
Let std_val be std_dev with values as values
Let skew_val be skewness with values as values
```

### Complex Numbers
```runa
Let z1 be complex with real as 3 and imag as 4
Let z2 be complex with real as 1 and imag as 2
Let sum be complex_add with a as z1 and b as z2
Let magnitude be the magnitude of z1
```

### Number Theory
```runa
Let is_prime_val be is_prime with n as 17
Let factors be prime_factors with n as 84
Let totient_val be totient with n as 12
```

### Combinatorics
```runa
Let binomial_val be binomial with n as 10 and k as 3
Let stirling_val be stirling_second with n as 5 and k as 3
```

### Financial Calculations
```runa
Let future_val be compound_interest with principal as 1000 and rate as 0.05 and time as 10 and periods as 12
Let pv be present_value with future_value as 2000 and rate as 0.06 and time as 5
```

### Numerical Analysis
```runa
Let f be lambda x: x multiplied by x minus 4
Let df be lambda x: 2 multiplied by x
Let root be newton_raphson with f as f and df as df and x0 as 2 and tolerance as 1e-6
```

### Random Numbers
```runa
Let uniform_val be random_range with min_val as 0 and max_val as 100
Let normal_val be random_normal with mean as 0 and std_dev as 1
```

### Vector Operations
```runa
Let v1 be list containing 1, 2, 3
Let v2 be list containing 4, 5, 6
Let dot_prod be dot_product with a as v1 and b as v2
Let norm be vector_norm with v as v1
```

### Cryptography
```runa
Let mod_pow be modular_power with base as 7 and exponent as 13 and modulus as 11
Let inv be modular_inverse with a as 3 and m as 11
```

## Examples

A complete, idiomatic example is available at:

    runa/examples/basic/math_example.runa

## Testing

A comprehensive Runa-based test file for the math module is located at:

    runa/tests/stdlib/test_math.runa

This file exercises all math operations using idiomatic Runa assertions and error handling. All standard library modules have corresponding Runa test files in this directory, ensuring production-ready quality and verifiability.

## Performance Characteristics

- **Time Complexity**: Most operations are O(1) for basic arithmetic
- **Space Complexity**: O(1) for most operations, O(n) for series and sequences
- **Precision**: Double-precision floating-point arithmetic
- **Thread Safety**: Operations are thread-safe for immutable operations

## Use Cases

- **Scientific Computing**: Numerical analysis, statistics, and modeling
- **Financial Applications**: Interest calculations, present value analysis
- **Cryptography**: Modular arithmetic and number theory
- **Data Analysis**: Statistical functions and random number generation
- **Graphics and Animation**: Trigonometric and vector operations
- **Signal Processing**: Complex numbers and Fourier analysis
- **Machine Learning**: Mathematical foundations and optimization 