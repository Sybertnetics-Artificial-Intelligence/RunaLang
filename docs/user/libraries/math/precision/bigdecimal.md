# Math Precision BigDecimal Module

## Overview

The `math/precision/bigdecimal` module provides arbitrary precision decimal arithmetic that eliminates floating-point representation errors. It implements IEEE 754-2008 decimal arithmetic standards with configurable precision and rounding modes, making it essential for financial calculations, scientific computing, and applications requiring exact decimal representation.

## Key Features

- **Arbitrary Precision**: Decimal numbers with user-specified precision up to memory limits
- **Exact Decimal Arithmetic**: No floating-point representation errors (0.1 + 0.2 = 0.3)
- **Financial Grade**: Currency-aware operations with proper rounding
- **IEEE 754 Compliance**: Standard rounding modes and decimal arithmetic
- **Scientific Notation**: Normalized representations and exponent handling
- **Configurable Rounding**: Multiple rounding modes for different applications
- **Scale Management**: Precise control over decimal places
- **Performance Optimized**: Efficient algorithms for large-scale computations

## Data Types

### BigDecimal
Represents an arbitrary precision decimal number:
```runa
Type called "BigDecimal":
    unscaled_value as BigInteger    Note: Integer mantissa
    scale as Integer                Note: Number of decimal places
    precision as Integer            Note: Total significant digits
```

### RoundingMode
Specifies how to handle rounding in operations:
```runa
Type RoundingMode is:
    | HALF_UP          Note: Round towards "nearest neighbor" unless equidistant, then up
    | HALF_DOWN        Note: Round towards "nearest neighbor" unless equidistant, then down
    | HALF_EVEN        Note: Round to nearest even digit (banker's rounding)
    | UP               Note: Round away from zero
    | DOWN             Note: Round towards zero (truncation)
    | CEILING          Note: Round towards positive infinity
    | FLOOR            Note: Round towards negative infinity
    | UNNECESSARY      Note: Assert that rounding is not necessary
```

### MathContext
Configuration for arithmetic operations:
```runa
Type called "MathContext":
    precision as Integer           Note: Number of significant digits
    rounding_mode as RoundingMode  Note: How to handle rounding
    enable_traps as Boolean        Note: Whether to trap exceptional conditions
```

## Basic Operations

### Creating BigDecimal Values
```runa
Import "math/precision/bigdecimal" as BigDecimal

Note: Create from string (recommended for exact values)
Let price be BigDecimal.create_from_string("19.99")
Let tax_rate be BigDecimal.create_from_string("0.0825")

Note: Create from integer
Let quantity be BigDecimal.create_from_integer(5)

Note: Create with specific scale
Let precise_value be BigDecimal.create_from_string_with_scale("3.14159", 5)

Note: Create from components
Let custom be BigDecimal.create_from_unscaled(314159, 5)  Note: 3.14159
```

### Arithmetic Operations
```runa
Note: Basic arithmetic with precision control
Let a be BigDecimal.create_from_string("123.456")
Let b be BigDecimal.create_from_string("78.9")

Let sum be BigDecimal.add(a, b, 3)              Note: 202.356
Let difference be BigDecimal.subtract(a, b, 3)  Note: 44.556
Let product be BigDecimal.multiply(a, b, 3)     Note: 9740.758
Let quotient be BigDecimal.divide(a, b, 3)      Note: 1.564

Display "Sum: " joined with BigDecimal.to_string(sum)
Display "Product: " joined with BigDecimal.to_string(product)
```

### Precision and Scale Management
```runa
Note: Control precision and scale
Let value be BigDecimal.create_from_string("123.456789")

Note: Set specific scale with rounding
Let scaled_value be BigDecimal.set_scale(value, 2, RoundingMode.HALF_UP)
Display "Scaled to 2 places: " joined with BigDecimal.to_string(scaled_value)

Note: Set precision
Let precise_value be BigDecimal.set_precision(value, 5, RoundingMode.HALF_EVEN)
Display "5 significant digits: " joined with BigDecimal.to_string(precise_value)

Note: Strip trailing zeros
Let clean_value be BigDecimal.strip_trailing_zeros(BigDecimal.create_from_string("12.300"))
Display "Cleaned: " joined with BigDecimal.to_string(clean_value)  Note: "12.3"
```

## Advanced Operations

### Mathematical Functions
```runa
Note: Advanced mathematical operations
Let x be BigDecimal.create_from_string("2.0")
Let precision be 20

Note: Power operations
Let squared be BigDecimal.power(x, 2, precision)
Let cube_root be BigDecimal.nth_root(BigDecimal.create_from_string("8"), 3, precision)

Note: Exponential and logarithmic functions
Let exp_x be BigDecimal.exponential(x, precision)
Let ln_x be BigDecimal.natural_log(x, precision)
Let log10_x be BigDecimal.log10(x, precision)

Display "2^2 = " joined with BigDecimal.to_string(squared)
Display "exp(2) = " joined with BigDecimal.to_string(exp_x)
Display "ln(2) = " joined with BigDecimal.to_string(ln_x)
```

### Trigonometric Functions
```runa
Note: Arbitrary precision trigonometry
Let angle be BigDecimal.create_from_string("1.5707963267948966")  Note: π/2
Let precision be 30

Let sine be BigDecimal.sin(angle, precision)
Let cosine be BigDecimal.cos(angle, precision)
Let tangent be BigDecimal.tan(angle, precision)

Display "sin(π/2) = " joined with BigDecimal.to_string(sine)
Display "cos(π/2) = " joined with BigDecimal.to_string(cosine)

Note: Inverse functions
Let arcsin be BigDecimal.asin(BigDecimal.create_from_string("0.5"), precision)
Display "arcsin(0.5) = " joined with BigDecimal.to_string(arcsin)
```

### Statistical Functions
```runa
Note: Statistical operations on BigDecimal arrays
Let values be Array[BigDecimal]()
values.add(BigDecimal.create_from_string("10.5"))
values.add(BigDecimal.create_from_string("12.3"))
values.add(BigDecimal.create_from_string("9.8"))
values.add(BigDecimal.create_from_string("11.2"))

Let mean be BigDecimal.arithmetic_mean(values, 10)
Let variance be BigDecimal.variance(values, 10)
Let std_dev be BigDecimal.standard_deviation(values, 10)

Display "Mean: " joined with BigDecimal.to_string(mean)
Display "Standard deviation: " joined with BigDecimal.to_string(std_dev)
```

## Financial Applications

### Currency Operations
```runa
Note: Financial calculations with proper rounding
Process called "calculate_compound_interest" that takes principal as BigDecimal, rate as BigDecimal, periods as Integer returns BigDecimal:
    Let one be BigDecimal.ONE
    Let rate_plus_one be BigDecimal.add(one, rate, 20)
    Let compound_factor be BigDecimal.power(rate_plus_one, periods, 20)
    Return BigDecimal.multiply(principal, compound_factor, 2)

Let initial_investment be BigDecimal.create_from_string("10000.00")
Let annual_rate be BigDecimal.create_from_string("0.05")
Let final_amount be calculate_compound_interest(initial_investment, annual_rate, 10)

Display "Final amount: $" joined with BigDecimal.to_string(final_amount)
```

### Tax Calculations
```runa
Note: Precise tax calculations
Let gross_amount be BigDecimal.create_from_string("100.00")
Let tax_rates be Array[BigDecimal]()
tax_rates.add(BigDecimal.create_from_string("0.08"))    Note: State tax
tax_rates.add(BigDecimal.create_from_string("0.015"))   Note: City tax

Let total_tax be BigDecimal.ZERO
For Each rate in tax_rates:
    Let tax_amount be BigDecimal.multiply(gross_amount, rate, 2)
    Set total_tax to BigDecimal.add(total_tax, tax_amount, 2)

Let final_amount be BigDecimal.add(gross_amount, total_tax, 2)
Display "Total with taxes: $" joined with BigDecimal.to_string(final_amount)
```

### Loan Calculations
```runa
Note: Mortgage payment calculation
Process called "calculate_monthly_payment" that takes loan_amount as BigDecimal, annual_rate as BigDecimal, years as Integer returns BigDecimal:
    Let monthly_rate be BigDecimal.divide(annual_rate, BigDecimal.create_from_string("12"), 10)
    Let num_payments be BigDecimal.create_from_integer(years * 12)
    
    Let rate_plus_one be BigDecimal.add(BigDecimal.ONE, monthly_rate, 10)
    Let rate_factor be BigDecimal.power(rate_plus_one, BigDecimal.to_integer(num_payments), 10)
    
    Let numerator be BigDecimal.multiply(loan_amount,
        BigDecimal.multiply(monthly_rate, rate_factor, 10), 10)
    Let denominator be BigDecimal.subtract(rate_factor, BigDecimal.ONE, 10)
    
    Return BigDecimal.divide(numerator, denominator, 2)

Let loan be BigDecimal.create_from_string("300000.00")
Let rate be BigDecimal.create_from_string("0.045")
Let monthly_payment be calculate_monthly_payment(loan, rate, 30)

Display "Monthly payment: $" joined with BigDecimal.to_string(monthly_payment)
```

## Scientific Computing

### Series Calculations
```runa
Note: High-precision series expansion for e
Process called "calculate_e_series" that takes precision as Integer returns BigDecimal:
    Let e_sum be BigDecimal.ZERO
    Let factorial be BigDecimal.ONE
    Let term be BigDecimal.ONE
    Let n be 0
    
    While BigDecimal.compare_abs(term, BigDecimal.create_from_string("1e-" joined with String(precision))) > 0:
        Set e_sum to BigDecimal.add(e_sum, term, precision + 10)
        Set n to n + 1
        Set factorial to BigDecimal.multiply(factorial, BigDecimal.create_from_integer(n), precision + 10)
        Set term to BigDecimal.divide(BigDecimal.ONE, factorial, precision + 10)
    
    Return BigDecimal.set_precision(e_sum, precision, RoundingMode.HALF_EVEN)

Let e_precise be calculate_e_series(50)
Display "e (50 digits): " joined with BigDecimal.to_string(e_precise)
```

### Newton-Raphson Method
```runa
Note: Square root using Newton-Raphson iteration
Process called "sqrt_newton" that takes x as BigDecimal, precision as Integer returns BigDecimal:
    If BigDecimal.is_zero(x):
        Return BigDecimal.ZERO
    
    Let guess be BigDecimal.divide(x, BigDecimal.create_from_string("2"), precision + 5)
    Let tolerance be BigDecimal.create_from_string("1e-" joined with String(precision + 2))
    
    For i from 1 to 100:  Note: Maximum iterations
        Let x_over_guess be BigDecimal.divide(x, guess, precision + 5)
        Let new_guess be BigDecimal.divide(
            BigDecimal.add(guess, x_over_guess, precision + 5),
            BigDecimal.create_from_string("2"),
            precision + 5
        )
        
        Let difference be BigDecimal.abs(BigDecimal.subtract(new_guess, guess, precision + 5))
        If BigDecimal.compare(difference, tolerance) < 0:
            Return BigDecimal.set_precision(new_guess, precision, RoundingMode.HALF_EVEN)
        
        Set guess to new_guess
    
    Return BigDecimal.set_precision(guess, precision, RoundingMode.HALF_EVEN)

Let sqrt_2 be sqrt_newton(BigDecimal.create_from_string("2"), 100)
Display "√2 (100 digits): " joined with BigDecimal.to_string(sqrt_2)
```

## Comparison Operations

### Equality and Ordering
```runa
Note: Precision-aware comparisons
Let a be BigDecimal.create_from_string("3.14")
Let b be BigDecimal.create_from_string("3.140")
Let c be BigDecimal.create_from_string("3.141")

Note: Exact comparison
Let exact_equal be BigDecimal.equals(a, b)           Note: false (different scales)
Let value_equal be BigDecimal.compare(a, b) == 0     Note: true (same value)

Note: Tolerance-based comparison
Let tolerance be BigDecimal.create_from_string("0.001")
Let close_enough be BigDecimal.equals_within_tolerance(a, c, tolerance)

Display "Exact equality: " joined with String(exact_equal)
Display "Value equality: " joined with String(value_equal)
Display "Within tolerance: " joined with String(close_enough)
```

### Min/Max Operations
```runa
Note: Find extremes in BigDecimal collections
Let values be Array[BigDecimal]()
values.add(BigDecimal.create_from_string("12.34"))
values.add(BigDecimal.create_from_string("5.67"))
values.add(BigDecimal.create_from_string("89.01"))

Let minimum be BigDecimal.min(values)
Let maximum be BigDecimal.max(values)
Let range be BigDecimal.subtract(maximum, minimum, 10)

Display "Range: " joined with BigDecimal.to_string(range)
```

## Configuration and Context

### Math Context Usage
```runa
Note: Configure arithmetic context
Let financial_context be MathContext with:
    precision: 20
    rounding_mode: RoundingMode.HALF_EVEN
    enable_traps: false

Let scientific_context be MathContext with:
    precision: 50
    rounding_mode: RoundingMode.HALF_UP
    enable_traps: true

Note: Use context in operations
Let a be BigDecimal.create_from_string("10")
Let b be BigDecimal.create_from_string("3")

Let financial_result be BigDecimal.divide_with_context(a, b, financial_context)
Let scientific_result be BigDecimal.divide_with_context(a, b, scientific_context)

Display "Financial precision: " joined with BigDecimal.to_string(financial_result)
Display "Scientific precision: " joined with BigDecimal.to_string(scientific_result)
```

### Global Configuration
```runa
Note: Set global defaults
BigDecimal.set_global_precision(28)
BigDecimal.set_global_rounding_mode(RoundingMode.HALF_EVEN)
BigDecimal.set_global_scale_mode(ScaleMode.AUTO_ADJUST)

Note: Operations now use global settings
Let result be BigDecimal.divide(BigDecimal.create_from_string("1"), BigDecimal.create_from_string("3"))
Display "Global context result: " joined with BigDecimal.to_string(result)
```

## Conversion Operations

### Type Conversions
```runa
Note: Convert between different numeric types
Let big_decimal be BigDecimal.create_from_string("123.456789")

Note: To basic types
Let as_float be BigDecimal.to_float(big_decimal)
Let as_double be BigDecimal.to_double(big_decimal)
Let as_integer be BigDecimal.to_integer(big_decimal)  Note: Truncates

Note: To other precision types
Let as_big_integer be BigDecimal.to_biginteger(big_decimal)
Let as_rational be BigDecimal.to_rational(big_decimal)

Note: To string formats
Let string_repr be BigDecimal.to_string(big_decimal)
Let scientific_notation be BigDecimal.to_scientific_string(big_decimal)
Let plain_string be BigDecimal.to_plain_string(big_decimal)

Display "Scientific: " joined with scientific_notation
Display "Plain: " joined with plain_string
```

### Format Conversions
```runa
Note: Specialized formatting
Let currency be BigDecimal.create_from_string("1234.56")

Note: Currency formatting
Let usd_format be BigDecimal.to_currency_string(currency, "USD", 2)
Let eur_format be BigDecimal.to_currency_string(currency, "EUR", 2)

Note: Percentage formatting  
Let percentage be BigDecimal.create_from_string("0.1567")
Let percent_format be BigDecimal.to_percentage_string(percentage, 2)

Display "USD: " joined with usd_format      Note: "$1,234.56"
Display "Percentage: " joined with percent_format  Note: "15.67%"
```

## Performance Optimization

### Batch Operations
```runa
Note: Efficient batch calculations
Let values be Array[BigDecimal]()
For i from 1 to 1000:
    values.add(BigDecimal.create_from_string(String(i) joined with ".50"))

Note: Vectorized operations
Let batch_sum be BigDecimal.batch_sum(values, 10)
Let batch_product be BigDecimal.batch_product(values.slice(0, 10), 10)
Let batch_average be BigDecimal.batch_average(values, 10)

Display "Batch sum: " joined with BigDecimal.to_string(batch_sum)
Display "Batch average: " joined with BigDecimal.to_string(batch_average)
```

### Memory Management
```runa
Note: Optimize memory usage for large computations
Let memory_config be BigDecimalMemoryConfig with:
    initial_capacity: 1000
    growth_factor: 1.5
    enable_pooling: true
    auto_cleanup: true

BigDecimal.configure_memory(memory_config)

Note: Monitor memory usage
Let memory_usage be BigDecimal.get_memory_statistics()
Display "Memory used: " joined with String(memory_usage.bytes_allocated)
Display "Objects pooled: " joined with String(memory_usage.pooled_objects)
```

## Error Handling

### Exception Types
The BigDecimal module defines several specific exception types:

- **DivisionByZero**: Division by zero attempted
- **InvalidPrecision**: Invalid precision specification
- **RoundingNecessary**: Rounding required but mode is UNNECESSARY
- **Overflow**: Result exceeds representable range
- **Underflow**: Result too small to represent accurately

### Error Handling Examples
```runa
Try:
    Let result be BigDecimal.divide(
        BigDecimal.create_from_string("1"),
        BigDecimal.create_from_string("0"),
        10
    )
Catch Errors.DivisionByZero as error:
    Display "Cannot divide by zero: " joined with error.message
    Let suggestion be SuggestionEngine.get_suggestion(error)
    Display "Suggestion: " joined with suggestion

Try:
    Let rounded be BigDecimal.divide_with_rounding(
        BigDecimal.create_from_string("10"),
        BigDecimal.create_from_string("3"),
        2,
        RoundingMode.UNNECESSARY
    )
Catch Errors.RoundingNecessary as error:
    Display "Rounding required: " joined with error.message
    Note: Use a different rounding mode
    Let fixed be BigDecimal.divide_with_rounding(
        BigDecimal.create_from_string("10"),
        BigDecimal.create_from_string("3"),
        2,
        RoundingMode.HALF_UP
    )
```

## Best Practices

### 1. Input Validation
```runa
Process called "validate_decimal_input" that takes input as String returns ValidationResult:
    Let validation be ValidationResult()
    
    If not is_valid_decimal_string(input):
        validation.add_error("Invalid decimal format")
    
    If get_decimal_places(input) > MAX_SUPPORTED_SCALE:
        validation.add_error("Scale exceeds system limits")
    
    Return validation
```

### 2. Precision Planning
```runa
Note: Plan precision requirements upfront
Process called "calculate_required_precision" that takes operation as String, operands as Array[BigDecimal] returns Integer:
    Let base_precision be get_maximum_precision(operands)
    
    If operation == "division":
        Return base_precision + 10  Note: Extra precision for division
    Otherwise If operation == "exponential":
        Return base_precision + 20  Note: More precision for transcendental functions
    Otherwise:
        Return base_precision + 5   Note: Standard buffer
```

### 3. Rounding Strategy
```runa
Note: Choose appropriate rounding modes
Process called "select_rounding_mode" that takes context as String returns RoundingMode:
    If context == "financial":
        Return RoundingMode.HALF_EVEN  Note: Banker's rounding
    Otherwise If context == "statistical":
        Return RoundingMode.HALF_UP    Note: Standard rounding
    Otherwise If context == "conservative":
        Return RoundingMode.UP         Note: Always round up
    Otherwise:
        Return RoundingMode.HALF_EVEN  Note: Default
```

### 4. Performance Monitoring
```runa
Note: Monitor computation performance
Process called "benchmark_decimal_operation" that takes operation as Process, iterations as Integer returns PerformanceMeasurement:
    Let start_time be System.current_time_nanos()
    Let memory_before be System.memory_usage()
    
    For i from 1 to iterations:
        operation()
    
    Let end_time be System.current_time_nanos()
    Let memory_after be System.memory_usage()
    
    Return PerformanceMeasurement with:
        execution_time: end_time - start_time
        memory_delta: memory_after - memory_before
        iterations: iterations
```

## Integration Examples

### With Statistics Module
```runa
Import "math/precision/bigdecimal" as BigDecimal
Import "math/statistics/descriptive" as Stats

Note: High-precision statistical analysis
Let dataset be Array[BigDecimal]()
For i from 1 to 1000:
    Let random_value be generate_random_decimal(20)  Note: 20 decimal places
    dataset.add(random_value)

Let precise_mean be Stats.arithmetic_mean_bigdecimal(dataset, 30)
Let precise_variance be Stats.variance_bigdecimal(dataset, 30)

Display "High-precision mean: " joined with BigDecimal.to_string(precise_mean)
Display "High-precision variance: " joined with BigDecimal.to_string(precise_variance)
```

### With Core Math
```runa
Import "math/precision/bigdecimal" as BigDecimal
Import "math/core/constants" as Constants

Note: Combine with high-precision constants
Let pi_50_digits be Constants.get_pi(50)
Let radius be BigDecimal.create_from_string("5.25")

Let area be BigDecimal.multiply(
    BigDecimal.multiply(pi_50_digits, radius, 50),
    radius,
    50
)

Display "Circle area (50 digits): " joined with BigDecimal.to_string(area)
```

## Migration Guide

### From Floating-Point
```runa
Note: Convert existing floating-point code
Note: Before (floating-point with errors)
Let price_old be 19.99
Let tax_rate_old be 0.0825
Let total_old be price_old * (1.0 + tax_rate_old)

Note: After (exact decimal arithmetic)
Let price_new be BigDecimal.create_from_string("19.99")
Let tax_rate_new be BigDecimal.create_from_string("0.0825")
Let tax_factor be BigDecimal.add(BigDecimal.ONE, tax_rate_new, 10)
Let total_new be BigDecimal.multiply(price_new, tax_factor, 2)

Display "Floating-point result: " joined with String(total_old)
Display "BigDecimal result: " joined with BigDecimal.to_string(total_new)
```

The BigDecimal module provides the foundation for exact decimal arithmetic in Runa, eliminating floating-point errors and providing the precision control essential for financial, scientific, and mathematical applications.