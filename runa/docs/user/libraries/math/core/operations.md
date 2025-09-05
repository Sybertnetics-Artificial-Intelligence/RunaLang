Note: Math Core Operations Module

## Overview

The `math/core/operations` module provides fundamental mathematical operations with high precision arithmetic support. It includes basic arithmetic, power/root operations, logarithms, factorials, complex numbers, and numerically stable algorithms for reliable scientific computing.

## Key Features

- **Arbitrary Precision**: All operations support user-specified precision
- **Comprehensive Error Handling**: Domain, overflow, and underflow protection
- **Complex Numbers**: Full complex arithmetic support
- **Numerical Stability**: Kahan summation and compensated arithmetic
- **Modular Arithmetic**: GCD, LCM, and modular exponentiation
- **Performance Optimization**: Algorithm selection and parallel processing

## Data Types

### ArithmeticResult
Represents the result of an arithmetic operation:
```runa
Type called "ArithmeticResult":
    result_value as String          Note: Computed result
    operation_type as String        Note: Type of operation
    input_parameters as List[String] # Input operands
    precision_used as Integer       Note: Precision level
    computation_method as String    Note: Algorithm used
    error_estimate as Float         Note: Numerical error estimate
    overflow_occurred as Boolean    Note: Overflow detection
    underflow_occurred as Boolean   Note: Underflow detection
```

### ComplexNumber
Represents a complex number with both rectangular and polar forms:
```runa
Type called "ComplexNumber":
    real_part as String            Note: Real component
    imaginary_part as String       Note: Imaginary component
    magnitude as String            Note: |z| = √(a² + b²)
    argument as String             Note: arg(z) = atan2(b, a)
    polar_form as Dictionary[String, String] # Polar representation
    precision as Integer           Note: Precision level
```

### FactorialResult
Contains factorial computation information:
```runa
Type called "FactorialResult":
    input_value as Integer         Note: Input n
    factorial_value as String      Note: n! result
    computation_method as String   Note: Algorithm used
    approximation_used as Boolean  Note: Whether approximated
    stirling_approximation as String # Stirling's approximation
```

## Basic Arithmetic Operations

### Addition
```runa
Note: High-precision addition
Let a be "123456789.987654321"
Let b be "987654321.123456789"
Let precision be 50

Let sum_result be Operations.add(a, b, precision)
Display "Sum: " joined with sum_result.result_value
Display "Method: " joined with sum_result.computation_method
```

### Subtraction
```runa
Note: Precise subtraction
Let minuend be "1000.0"
Let subtrahend be "0.0000000001"
Let precision be 20

Let difference be Operations.subtract(minuend, subtrahend, precision)
Display "Difference: " joined with difference.result_value
Display "Precision used: " joined with String(difference.precision_used)
```

### Multiplication
```runa
Note: Large number multiplication
Let multiplicand be "123456789123456789"
Let multiplier be "987654321987654321"
Let precision be 100

Let product be Operations.multiply(multiplicand, multiplier, precision)
Display "Product: " joined with product.result_value
If product.overflow_occurred:
    Display "Warning: Overflow detected"
```

### Division
```runa
Note: Safe division with error handling
Let dividend be "22"
Let divisor be "7"
Let precision be 50

Try:
    Let quotient be Operations.divide(dividend, divisor, precision)
    Display "22/7 = " joined with quotient.result_value
    Display "Error estimate: " joined with String(quotient.error_estimate)
Catch Errors.MathematicalError as error:
    Display "Division error: " joined with error.message
```

### Modulo Operations
```runa
Note: Modular arithmetic
Let dividend be "17"
Let divisor be "5"

Let mod_result be Operations.modulo(dividend, divisor)
Display "17 mod 5 = " joined with mod_result.remainder
Display "Quotient: " joined with mod_result.quotient
```

## Power and Root Operations

### Exponentiation
```runa
Note: Integer powers
Let base be "2.5"
Let exponent be "10"
Let precision be 30

Let power_result be Operations.power(base, exponent, precision)
Display "2.5^10 = " joined with power_result.result_value
Display "Method: " joined with power_result.computation_method

Note: Floating-point exponents
Let float_exp be "2.5"
Let float_power be Operations.power("4", float_exp, precision)
Display "4^2.5 = " joined with float_power.result_value
```

### Square Root
```runa
Note: High-precision square root
Let radicand be "2"
Let precision be 100

Let sqrt_result be Operations.square_root(radicand, precision)
Display "√2 = " joined with sqrt_result.result_value
Display "Method: " joined with sqrt_result.computation_method
Display "Error estimate: " joined with String(sqrt_result.error_estimate)
```

### Cube Root
```runa
Note: Cube root calculation
Let radicand be "27"
Let precision be 50

Let cbrt_result be Operations.cube_root(radicand, precision)
Display "∛27 = " joined with cbrt_result.result_value

Note: Negative cube root
Let negative_cbrt be Operations.cube_root("-8", precision)
Display "∛(-8 = " joined with negative_cbrt.result_value)
```

### Nth Root
```runa
Note: General nth root
Let radicand be "32"
Let root_index be 5
Let precision be 30

Let nth_root_result be Operations.nth_root(radicand, root_index, precision)
Display "32^(1/5 = " joined with nth_root_result.result_value)

Note: Negative root index (reciprocal)
Let reciprocal_root be Operations.nth_root("16", -2, precision)
Display "16^(-1/2 = " joined with reciprocal_root.result_value)
```

### Exponential Function
```runa
Note: e^x calculation
Let exponent be "2.5"
Let precision be 50

Let exp_result be Operations.exponential(exponent, precision)
Display "e^2.5 = " joined with exp_result.result_value
Display "Method: " joined with exp_result.computation_method
```

## Logarithmic Operations

### Natural Logarithm
```runa
Note: ln(x) calculation
Let argument be "10"
Let precision be 50

Try:
    Let ln_result be Operations.natural_logarithm(argument, precision)
    Display "ln(10 = " joined with ln_result.result_value)
    Display "Error estimate: " joined with String(ln_result.error_estimate)
Catch Errors.MathematicalError as error:
    Display "Logarithm error: " joined with error.message
```

### Common Logarithm
```runa
Note: log₁₀(x) calculation
Let argument be "100"
Let precision be 30

Let log10_result be Operations.common_logarithm(argument, precision)
Display "log₁₀(100 = " joined with log10_result.result_value)  Note: Should be "2"
```

### Binary Logarithm
```runa
Note: log₂(x) calculation
Let argument be "1024"
Let precision be 30

Let log2_result be Operations.binary_logarithm(argument, precision)
Display "log₂(1024 = " joined with log2_result.result_value)  Note: Should be "10"
```

### Arbitrary Base Logarithm
```runa
Note: log_b(x) calculation
Let argument be "125"
Let base be "5"
Let precision be 30

Let log_result be Operations.logarithm_arbitrary_base(argument, base, precision)
Display "log₅(125 = " joined with log_result.result_value)  Note: Should be "3"
```

### Change of Base
```runa
Note: Convert logarithm from one base to another
Let argument be "100"
Let from_base be "10"
Let to_base be "2"
Let precision be 50

Let converted_log be Operations.logarithm_change_of_base(argument, from_base, to_base, precision)
Display "log₂(100 = " joined with converted_log.result_value)
```

## Factorial and Combinatorial Operations

### Factorial
```runa
Note: Standard factorial
Let n be 10
Let factorial_result be Operations.factorial(n)
Display "10! = " joined with factorial_result.factorial_value
Display "Method: " joined with factorial_result.computation_method

Note: Large factorial with Stirling's approximation
Let large_n be 200
Let large_factorial be Operations.factorial(large_n)
If large_factorial.approximation_used:
    Display "200! ≈ " joined with large_factorial.factorial_value joined with " (Stirling")
    Display "Stirling approximation: " joined with large_factorial.stirling_approximation
```

### Double Factorial
```runa
Note: Double factorial n!! = n × (n-2) × (n-4) × ...
Let n be 8
Let double_fact be Operations.double_factorial(n)
Display "8!! = " joined with double_fact.factorial_value  Note: 8 × 6 × 4 × 2 = 384
```

### Subfactorial (Derangements)
```runa
Note: Subfactorial !n (number of derangements)
Let n be 5
Let subfact be Operations.subfactorial(n)
Display "!5 = " joined with subfact.factorial_value  Note: Number of derangements of 5 items
```

### Factorial Approximations
```runa
Note: Compare different approximation methods
Let n be 50

Let stirling_approx be Operations.factorial_approximation(n, "stirling")
Let ramanujan_approx be Operations.factorial_approximation(n, "ramanujan")

Display "Stirling approximation: " joined with stirling_approx.factorial_value
Display "Ramanujan approximation: " joined with ramanujan_approx.factorial_value
```

### Binomial Coefficient
```runa
Note: C(n,k) = n! / (k!(n-k)!)
Let n be 10
Let k be 3

Let binomial be Operations.binomial_coefficient(n, k)
Display "C(10,3 = " joined with binomial.result_value)  Note: 120
Display "Method: " joined with binomial.computation_method
```

## Absolute Value and Sign Operations

### Absolute Value
```runa
Note: Absolute value calculation
Let positive_val be "42.5"
Let negative_val be "-17.3"

Let abs_pos be Operations.absolute_value(positive_val)
Let abs_neg be Operations.absolute_value(negative_val)

Display "|42.5| = " joined with abs_pos.result_value   Note: "42.5"
Display "|-17.3| = " joined with abs_neg.result_value  Note: "17.3"
```

### Sign Functions
```runa
Note: Sign detection
Let values be ["5.7", "-3.2", "0.0"]

For Each value in values:
    Let sign_int be Operations.sign(value)        Note: Returns -1, 0, or 1
    Let sign_float be Operations.signum(value)    Note: Returns "-1.0", "0.0", or "1.0"
    Display "sign(" joined with value joined with " = " joined with String(sign_int) joined with ", signum = ") joined with sign_float)
```

### Copy Sign
```runa
Note: Copy sign from one number to another
Let magnitude be "42.5"
Let sign_source be "-10.0"

Let result be Operations.copy_sign(magnitude, sign_source)
Display "copy_sign(42.5, -10.0 = " joined with result)  Note: "-42.5"
```

## Modular Arithmetic

### Greatest Common Divisor
```runa
Note: GCD using Euclidean algorithm
Let a be "48"
Let b be "18"

Let gcd_result be Operations.greatest_common_divisor(a, b)
Display "gcd(48, 18 = " joined with gcd_result)  Note: "6"
```

### Least Common Multiple
```runa
Note: LCM calculation
Let a be "12"
Let b be "15"

Let lcm_result be Operations.least_common_multiple(a, b)
Display "lcm(12, 15 = " joined with lcm_result)  Note: "60"
```

### Extended Euclidean Algorithm
```runa
Note: Find Bézout coefficients: ax joined with by = gcd(a,b)
Let a be "30"
Let b be "18"

Let extended_result be Operations.extended_euclidean_algorithm(a, b)
Display "gcd(30, 18 = " joined with extended_result["gcd"])
Display "30 × " joined with extended_result["x"] joined with " joined with 18 × " joined with extended_result["y"] joined with " = " joined with extended_result["gcd"]
```

### Modular Inverse
```runa
Note: Find multiplicative inverse modulo m
Let a be "7"
Let modulus be "26"

Try:
    Let inverse be Operations.modular_inverse(a, modulus)
    Display "7⁻¹ (mod 26 = " joined with inverse)
Catch Errors.InvalidOperation as error:
    Display "No modular inverse exists: " joined with error.message
```

### Modular Exponentiation
```runa
Note: Efficient computation of (base^exponent) mod modulus
Let base be "3"
Let exponent be "100"
Let modulus be "7"

Let mod_exp_result be Operations.modular_exponentiation(base, exponent, modulus)
Display "3^100 (mod 7 = " joined with mod_exp_result)
```

## Complex Number Operations

### Complex Number Creation
```runa
Note: Create complex numbers
Let z1 be ComplexNumber with:
    real_part: "3.0"
    imaginary_part: "4.0"
    precision: 50

Let z2 be ComplexNumber with:
    real_part: "1.0"
    imaginary_part: "-2.0"
    precision: 50
```

### Complex Arithmetic
```runa
Note: Complex addition
Let sum_complex be Operations.complex_add(z1, z2)
Display "(3+4i joined with (1-2i) = " joined with sum_complex.real_part joined with " joined with " joined with sum_complex.imaginary_part joined with "i")

Note: Complex multiplication
Let product_complex be Operations.complex_multiply(z1, z2)
Display "(3+4i × (1-2i) = " joined with product_complex.real_part joined with " joined with " joined with product_complex.imaginary_part joined with "i")

Note: Complex division
Let quotient_complex be Operations.complex_divide(z1, z2)
Display "(3+4i ÷ (1-2i) = " joined with quotient_complex.real_part joined with " joined with " joined with quotient_complex.imaginary_part joined with "i")
```

### Complex Properties
```runa
Note: Complex conjugate
Let conjugate be Operations.complex_conjugate(z1)
Display "Conjugate of (3+4i = " joined with conjugate.real_part joined with " joined with " joined with conjugate.imaginary_part joined with "i")

Note: Magnitude (absolute value)
Let magnitude be Operations.complex_magnitude(z1)
Display "|3+4i| = " joined with magnitude  Note: Should be "5.0"
```

## Numerically Stable Operations

### Stable Summation
```runa
Note: Kahan summation for numerical stability
Let values be ["1e20", "1.0", "-1e20", "1.0"]
Let precision be 50

Let stable_sum_result be Operations.stable_sum(values, precision)
Display "Stable sum: " joined with stable_sum_result.result_value
Display "Method: " joined with stable_sum_result.computation_method
Display "Error estimate: " joined with String(stable_sum_result.error_estimate)
```

### Stable Product
```runa
Note: Logarithmic multiplication for stability
Let values be ["1e100", "1e100", "1e-100", "1e-100"]
Let precision be 50

Let stable_product_result be Operations.stable_product(values, precision)
Display "Stable product: " joined with stable_product_result.result_value
Display "Method: " joined with stable_product_result.computation_method
```

### Compensated Arithmetic
```runa
Note: Error-compensated operations
Let operands be ["1e20", "1.0", "2.0"]
Let precision be 50

Let compensated_result be Operations.compensated_arithmetic("addition", operands, precision)
Display "Compensated sum: " joined with compensated_result.result_value
Display "Error compensation applied: " joined with compensated_result.computation_method
```

## Advanced Operations

### Operation Sequence Optimization
```runa
Note: Optimize mathematical operation sequences
Let operations be [
    Dictionary with: "operation": "multiply", "operand_a": "x", "operand_b": "0",
    Dictionary with: "operation": "add", "operand_a": "y", "operand_b": "0",
    Dictionary with: "operation": "multiply", "operand_a": "z", "operand_b": "1"
]

Let optimized_ops be Operations.optimize_operation_sequence(operations)
Display "Optimized " joined with String(Length(operations) joined with " operations to ") joined with String(Length(optimized_ops)))
```

### Algorithm Selection
```runa
Note: Select optimal algorithm based on operand characteristics
Let operand_chars be Dictionary with:
    "size_a": "1000"
    "size_b": "1000"

Let optimal_mult_algo be Operations.select_optimal_algorithm("multiplication", operand_chars)
Display "Optimal multiplication algorithm: " joined with optimal_mult_algo

Note: For square root
Let sqrt_chars be Dictionary with: "precision": "500"
Let optimal_sqrt_algo be Operations.select_optimal_algorithm("square_root", sqrt_chars)
Display "Optimal sqrt algorithm: " joined with optimal_sqrt_algo
```

### Parallel Arithmetic
```runa
Note: Parallel processing for large operations
Let large_operand_list be generate_large_list(10000)
Let parallel_options be Dictionary with:
    "thread_count": "4"
    "precision": "50"

Let parallel_sum be Operations.parallel_arithmetic("sum", large_operand_list, parallel_options)
Display "Parallel sum result: " joined with parallel_sum.result_value
Display "Computation method: " joined with parallel_sum.computation_method
```

## Input Validation and Error Handling

### Operand Validation
```runa
Note: Validate operands before computation
Let operands be ["3.14", "2.71", "invalid"]
Try:
    Let validated_operands be Operations.validate_operands(operands, "multiplication")
    Display "All operands valid"
Catch Errors.MathematicalError as error:
    Display "Validation failed: " joined with error.message
```

### Precision Verification
```runa
Note: Verify result meets precision requirements
Let result be "3.141592653589793"
Let expected_precision be 15

Let precision_ok be Operations.verify_result_precision(result, expected_precision)
If precision_ok:
    Display "Result meets precision requirement"
Otherwise:
    Display "Insufficient precision in result"
```

## Utility Operations

### Result Formatting
```runa
Note: Format arithmetic results
Let calculation_result be Operations.multiply("123.456", "789.012", 10)
Let format_options be Dictionary with:
    "format_type": "scientific"
    "precision_digits": "6"
    "show_metadata": "true"

Let formatted be Operations.format_arithmetic_result(calculation_result, format_options)
Display formatted
```

### Base Conversion
```runa
Note: Convert between number bases
Let decimal_number be "255"
Let binary be Operations.convert_number_base(decimal_number, 10, 2)
Let hexadecimal be Operations.convert_number_base(decimal_number, 10, 16)

Display "255₁₀ = " joined with binary joined with "₂ = " joined with hexadecimal joined with "₁₆"
```

### Performance Benchmarking
```runa
Note: Benchmark operation performance
Let operation_types be ["addition", "multiplication", "division", "square_root"]
Let test_data be Dictionary with:
    "addition": ["123.456", "789.012"]
    "multiplication": ["123.456", "789.012"]
    "division": ["123.456", "789.012"]
    "square_root": ["123.456"]

Let benchmark_results be Operations.benchmark_operation_performance(operation_types, test_data)
For Each operation, avg_time in benchmark_results:
    Display operation joined with ": " joined with String(avg_time * 1000 joined with " ms average"))
```

## Error Handling

The operations module provides comprehensive error handling:

```runa
Note: Division by zero
Try:
    Let division_result be Operations.divide("10", "0", 50)
Catch Errors.MathematicalError as error:
    Display "Math error: " joined with error.message
    Let diagnostic be error.diagnostic_info
    Display "Error code: " joined with diagnostic.error_code
    Let suggestion be SuggestionEngine.get_suggestion(error)
    Display "Suggestion: " joined with suggestion

Note: Domain errors for logarithms
Try:
    Let log_negative be Operations.natural_logarithm("-5", 50)
Catch Errors.MathematicalError as error:
    Display "Domain error: " joined with error.message

Note: Overflow detection
Try:
    Let huge_power be Operations.power("10", "1000", 50)
Catch Errors.OverflowError as error:
    Display "Overflow detected: " joined with error.message
```

## Performance Considerations

- **Precision Trade-offs**: Higher precision increases computation time exponentially
- **Algorithm Selection**: Use `select_optimal_algorithm()` for performance-critical operations
- **Parallel Processing**: Leverage parallel operations for large datasets
- **Numerical Stability**: Use stable algorithms for sensitive calculations

## Best Practices

1. **Choose Appropriate Precision**: Balance accuracy needs with performance requirements
2. **Handle All Errors**: Mathematical operations can fail in various ways
3. **Use Stable Algorithms**: Employ Kahan summation and compensated arithmetic for critical calculations
4. **Validate Inputs**: Always validate operands before computation
5. **Monitor Performance**: Benchmark operations with representative data
6. **Consider Complex Numbers**: Use complex arithmetic when dealing with negative roots or advanced mathematics