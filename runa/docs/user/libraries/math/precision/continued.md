# Math Precision Continued Fractions Module

## Overview

The `math/precision/continued` module provides comprehensive continued fraction operations including convergent calculations, best rational approximations, periodic expansions, and numerical analysis applications. It implements classical algorithms for continued fraction arithmetic, quadratic irrational recognition, and approximation theory using convergent properties.

## Key Features

- **General Continued Fractions**: Both simple and general continued fraction representations
- **Convergent Calculations**: Precise computation of convergents with error bounds
- **Periodic Detection**: Recognition and analysis of periodic continued fractions
- **Best Approximations**: Optimal rational approximations using convergent properties
- **Quadratic Irrationals**: Special handling for square root expansions
- **Arithmetic Operations**: Addition and multiplication of continued fractions
- **Diophantine Applications**: Solutions to Diophantine equations and approximation problems
- **Calendar Algorithms**: Applications in astronomical and calendar calculations

## Data Types

### ContinuedFraction
Represents a continued fraction expansion:
```runa
Type called "ContinuedFraction":
    coefficients as Array[BigInteger]    Note: Partial quotients [a0; a1, a2, ...]
    is_finite as Boolean                 Note: Whether expansion terminates
    is_periodic as Boolean               Note: Whether expansion is periodic
    period_start as Integer              Note: Index where period begins
    period_length as Integer             Note: Length of repeating sequence
```

### Convergent
Represents a rational convergent of a continued fraction:
```runa
Type called "Convergent":
    numerator as BigInteger              Note: Convergent numerator
    denominator as BigInteger            Note: Convergent denominator
    index as Integer                     Note: Convergent index (n)
    error_bound as Rational              Note: Upper bound on approximation error
```

### PeriodicAnalysis
Analysis result for periodic continued fractions:
```runa
Type called "PeriodicAnalysis":
    is_purely_periodic as Boolean        Note: Starts repeating immediately
    period_coefficients as Array[BigInteger]  Note: The repeating sequence
    pre_period as Array[BigInteger]      Note: Non-repeating part before period
    minimal_period as Integer            Note: Length of shortest period
```

### ApproximationResult
Result of best approximation calculations:
```runa
Type called "ApproximationResult":
    best_approximation as Rational       Note: Best rational approximation
    convergent_index as Integer          Note: Which convergent provides this
    error as BigDecimal                  Note: Absolute approximation error
    quality_measure as BigDecimal        Note: Quality of approximation
```

## Basic Operations

### Creating Continued Fractions
```runa
Import "math/precision/continued" as Continued
Import "math/precision/rational" as Rational
Import "math/precision/bigdecimal" as BigDecimal

Note: Create from rational number
Let rational_value be Rational.create(355, 113)  Note: Good π approximation
Let cf_from_rational be Continued.create_from_rational(rational_value)

Display "355/113 as continued fraction:"
Display Continued.to_string(cf_from_rational)

Note: Create from decimal approximation
Let pi_decimal be BigDecimal.create_from_string("3.14159265358979323846")
Let cf_from_decimal be Continued.create_from_decimal(pi_decimal, 20)

Display "π as continued fraction (20 terms):"
Display Continued.to_string(cf_from_decimal)

Note: Create from coefficients directly
Let golden_ratio_coeffs be Array[BigInteger]()
golden_ratio_coeffs.add(BigInteger.create_from_integer(1))
For i from 1 to 10:
    golden_ratio_coeffs.add(BigInteger.ONE)

Let golden_ratio_cf be Continued.create_from_coefficients(golden_ratio_coeffs)
Display "Golden ratio: " joined with Continued.to_string(golden_ratio_cf)
```

### Computing Convergents
```runa
Note: Calculate convergents using recurrence relations
Let cf be Continued.create_from_coefficients(golden_ratio_coeffs)
Let convergents be Continued.calculate_convergents(cf, 8)

Display "Golden ratio convergents:"
For i from 0 to convergents.length - 1:
    Let conv be convergents[i]
    Let decimal_value be BigDecimal.divide(
        BigDecimal.create_from_biginteger(conv.numerator, 20),
        BigDecimal.create_from_biginteger(conv.denominator, 20),
        20
    )
    Display "C" joined with String(i) joined with " = " joined with 
            BigInteger.to_string(conv.numerator, 10) joined with "/" joined with 
            BigInteger.to_string(conv.denominator, 10) joined with 
            " ≈ " joined with BigDecimal.to_string(decimal_value)
```

### Error Analysis
```runa
Note: Analyze convergent approximation quality
Process called "analyze_convergent_error" that takes target as BigDecimal, convergent as Convergent, precision as Integer returns ErrorAnalysis:
    Let target_rational be Rational.create_from_bigdecimal(target)
    Let convergent_rational be Rational.create_from_bigintegers(convergent.numerator, convergent.denominator)
    
    Let absolute_error be Rational.abs(Rational.subtract(target_rational, convergent_rational))
    Let relative_error be Rational.divide(absolute_error, target_rational)
    
    Note: Theoretical error bound: |x - pn/qn| < 1/(qn * qn+1)
    Let theoretical_bound be Rational.create(BigInteger.ONE,
        BigInteger.multiply(convergent.denominator, convergent.denominator))
    
    Return ErrorAnalysis with:
        absolute_error: absolute_error
        relative_error: relative_error
        theoretical_bound: theoretical_bound
        meets_bound: Rational.compare(absolute_error, theoretical_bound) < 0

Let pi_value be BigDecimal.create_from_string("3.14159265358979323846264338327950288")
Let pi_cf be Continued.create_from_decimal(pi_value, 15)
Let pi_convergents be Continued.calculate_convergents(pi_cf, 10)

Display "π convergent error analysis:"
For Each conv in pi_convergents:
    Let error_analysis be analyze_convergent_error(pi_value, conv, 50)
    Display "C" joined with String(conv.index) joined with " error: " joined with 
            Rational.to_decimal_string(error_analysis.absolute_error, 10) joined with
            " (bound satisfied: " joined with String(error_analysis.meets_bound) joined with ")"
```

## Periodic Continued Fractions

### Square Root Expansions
```runa
Note: Generate periodic continued fraction for square roots
Process called "sqrt_continued_fraction" that takes n as Integer returns ContinuedFraction:
    Note: Algorithm for √n where n is not a perfect square
    Let n_big be BigInteger.create_from_integer(n)
    Let a0 be BigInteger.sqrt(n_big)  Note: Integer part of √n
    
    If BigInteger.equals(BigInteger.multiply(a0, a0), n_big):
        Note: Perfect square, return [a0; ] (finite)
        Let coeffs be Array[BigInteger]()
        coeffs.add(a0)
        Return Continued.create_from_coefficients(coeffs)
    
    Note: Generate periodic expansion
    Let coefficients be Array[BigInteger]()
    coefficients.add(a0)
    
    Let m be BigInteger.ZERO
    Let d be BigInteger.ONE
    Let a be a0
    
    Let seen_states be Dictionary[String, Integer]()
    Let period_start be -1
    
    While true:
        Set m to BigInteger.subtract(BigInteger.multiply(a, d), m)
        Set d to BigInteger.divide(BigInteger.subtract(n_big, BigInteger.multiply(m, m)), d)
        Set a to BigInteger.divide(BigInteger.add(a0, m), d)
        
        coefficients.add(a)
        
        Let state be String(BigInteger.to_string(m, 10)) joined with "," joined with String(BigInteger.to_string(d, 10))
        
        If seen_states.contains_key(state):
            Set period_start to seen_states.get(state)
            Break
        
        seen_states.set(state, coefficients.length - 1)
    
    Return Continued.create_periodic(coefficients, period_start, coefficients.length - period_start)

Let sqrt_2_cf be sqrt_continued_fraction(2)
Display "√2 continued fraction: " joined with Continued.to_string(sqrt_2_cf)

Let sqrt_13_cf be sqrt_continued_fraction(13)
Display "√13 continued fraction: " joined with Continued.to_string(sqrt_13_cf)
```

### Periodic Analysis
```runa
Note: Analyze periodic structure of continued fractions
Process called "analyze_periodicity" that takes cf as ContinuedFraction returns PeriodicAnalysis:
    If not cf.is_periodic:
        Return PeriodicAnalysis with:
            is_purely_periodic: false
            minimal_period: 0
    
    Let period_coeffs be Array[BigInteger]()
    For i from cf.period_start to cf.period_start + cf.period_length - 1:
        period_coeffs.add(cf.coefficients[i])
    
    Let pre_period be Array[BigInteger]()
    For i from 0 to cf.period_start - 1:
        pre_period.add(cf.coefficients[i])
    
    Return PeriodicAnalysis with:
        is_purely_periodic: cf.period_start == 1  Note: Purely periodic if period starts after a0
        period_coefficients: period_coeffs
        pre_period: pre_period
        minimal_period: cf.period_length

Let sqrt_5_cf be sqrt_continued_fraction(5)
Let periodic_analysis be analyze_periodicity(sqrt_5_cf)

Display "√5 periodic analysis:"
Display "Is purely periodic: " joined with String(periodic_analysis.is_purely_periodic)
Display "Period length: " joined with String(periodic_analysis.minimal_period)
Display "Period coefficients: " joined with BigInteger.array_to_string(periodic_analysis.period_coefficients)
```

### Quadratic Irrational Recognition
```runa
Note: Determine if a continued fraction represents a quadratic irrational
Process called "is_quadratic_irrational" that takes cf as ContinuedFraction returns QuadraticForm:
    If not cf.is_periodic:
        Return QuadraticForm.NONE  Note: Not quadratic irrational
    
    Note: Every quadratic irrational has a periodic continued fraction
    Note: Use theory to reconstruct the quadratic equation
    
    Let convergents be Continued.calculate_convergents(cf, cf.period_start + 2 * cf.period_length)
    
    Note: Find quadratic equation ax² + bx + c = 0 satisfied by the value
    Note: This involves solving a system using three convergents
    
    Let n1 be convergents[cf.period_start].numerator
    Let d1 be convergents[cf.period_start].denominator
    Let n2 be convergents[cf.period_start + cf.period_length].numerator  
    Let d2 be convergents[cf.period_start + cf.period_length].denominator
    
    Note: The quadratic form can be reconstructed from the periodic structure
    Return QuadraticForm.analyze_from_period(cf.period_coefficients)

Process called "reconstruct_quadratic_equation" that takes cf as ContinuedFraction returns QuadraticEquation:
    Let quad_form be is_quadratic_irrational(cf)
    
    If quad_form != QuadraticForm.NONE:
        Return QuadraticEquation with:
            a: quad_form.coefficient_a
            b: quad_form.coefficient_b  
            c: quad_form.coefficient_c
    
    Return QuadraticEquation.NONE
```

## Best Rational Approximations

### Convergent-Based Approximations
```runa
Note: Find best rational approximations using convergent theory
Process called "best_approximations_bounded_denominator" that takes target as BigDecimal, max_denominator as Integer returns Array[ApproximationResult]:
    Let cf be Continued.create_from_decimal(target, 100)
    Let convergents be Continued.calculate_convergents(cf, 50)
    
    Let best_approximations be Array[ApproximationResult]()
    
    For Each conv in convergents:
        If BigInteger.compare(conv.denominator, BigInteger.create_from_integer(max_denominator)) <= 0:
            Let target_rational be Rational.create_from_bigdecimal(target)
            Let conv_rational be Rational.create_from_bigintegers(conv.numerator, conv.denominator)
            Let error be Rational.abs(Rational.subtract(target_rational, conv_rational))
            
            Let quality be BigDecimal.divide(
                BigDecimal.ONE,
                BigDecimal.multiply(
                    BigDecimal.create_from_biginteger(conv.denominator, 20),
                    Rational.to_bigdecimal(error, 20),
                    20
                ),
                20
            )
            
            best_approximations.add(ApproximationResult with:
                best_approximation: conv_rational
                convergent_index: conv.index
                error: Rational.to_bigdecimal(error, 20)
                quality_measure: quality
            )
    
    Note: Sort by quality (higher is better)
    Return ApproximationResult.sort_by_quality(best_approximations)

Let e_value be BigDecimal.create_from_string("2.71828182845904523536028747135266249")
Let e_approximations be best_approximations_bounded_denominator(e_value, 1000)

Display "Best rational approximations to e (denominator ≤ 1000):"
For i from 0 to Integer.min(5, e_approximations.length - 1):  Note: Show top 5
    Let approx be e_approximations[i]
    Display "  " joined with Rational.to_string(approx.best_approximation) joined with 
            " (error: " joined with BigDecimal.to_scientific_string(approx.error, 3) joined with 
            ", quality: " joined with BigDecimal.to_string(approx.quality_measure) joined with ")"
```

### Mediants and Farey Neighbors
```runa
Note: Use mediant properties to find intermediate approximations
Process called "find_farey_neighbors" that takes target_cf as ContinuedFraction, max_denom as Integer returns Array[Rational]:
    Let convergents be Continued.calculate_convergents(target_cf, 20)
    Let neighbors be Array[Rational]()
    
    For i from 1 to convergents.length - 1:
        Let prev_conv be convergents[i - 1]  
        Let curr_conv be convergents[i]
        
        If BigInteger.compare(curr_conv.denominator, BigInteger.create_from_integer(max_denom)) <= 0:
            Note: Find mediants between consecutive convergents
            Let mediant_num be BigInteger.add(prev_conv.numerator, curr_conv.numerator)
            Let mediant_denom be BigInteger.add(prev_conv.denominator, curr_conv.denominator)
            
            If BigInteger.compare(mediant_denom, BigInteger.create_from_integer(max_denom)) <= 0:
                neighbors.add(Rational.create_from_bigintegers(mediant_num, mediant_denom))
    
    Return neighbors

Let pi_cf be Continued.create_from_decimal(
    BigDecimal.create_from_string("3.14159265358979323846"), 30
)
Let pi_neighbors be find_farey_neighbors(pi_cf, 100)

Display "Farey neighbors of π (denominator ≤ 100):"
For Each neighbor in pi_neighbors:
    Let error_from_pi be Rational.abs(Rational.subtract(
        neighbor,
        Rational.create(314159265358979323846, BigInteger.power(BigInteger.create_from_integer(10), BigInteger.create_from_integer(20)))
    ))
    Display "  " joined with Rational.to_string(neighbor) joined with 
            " ≈ " joined with Rational.to_decimal_string(neighbor, 8)
```

## Continued Fraction Arithmetic

### Addition of Continued Fractions
```runa
Note: Add two continued fractions (complex operation)
Process called "add_continued_fractions" that takes cf1 as ContinuedFraction, cf2 as ContinuedFraction returns ContinuedFraction:
    Note: Convert to high-precision decimals, add, then convert back
    Note: Direct CF addition is algorithmically complex
    
    Let precision be 100
    Let decimal1 be Continued.to_bigdecimal(cf1, precision)
    Let decimal2 be Continued.to_bigdecimal(cf2, precision)
    
    Let sum_decimal be BigDecimal.add(decimal1, decimal2, precision)
    
    Return Continued.create_from_decimal(sum_decimal, 50)

Note: Test with golden ratio identities
Let phi_cf be Continued.create_from_coefficients(Array[BigInteger]([BigInteger.ONE] * 10))  Note: [1; 1, 1, 1, ...]
Let one_cf be Continued.create_from_coefficients(Array[BigInteger]([BigInteger.ONE]))       Note: [1]

Let phi_plus_one be add_continued_fractions(phi_cf, one_cf)

Display "φ + 1 continued fraction:"
Display Continued.to_string(phi_plus_one)

Note: Verify φ + 1 = φ² (golden ratio property)
Let phi_decimal be Continued.to_bigdecimal(phi_cf, 50)
let phi_squared_decimal be BigDecimal.multiply(phi_decimal, phi_decimal, 50)
let phi_plus_one_decimal be Continued.to_bigdecimal(phi_plus_one, 50)

let difference be BigDecimal.abs(BigDecimal.subtract(phi_squared_decimal, phi_plus_one_decimal, 50))
Display "Verification |φ² - (φ + 1)|: " joined with BigDecimal.to_scientific_string(difference, 5)
```

### Multiplication and Division
```runa
Note: Multiply continued fractions
Process called "multiply_continued_fractions" that takes cf1 as ContinuedFraction, cf2 as ContinuedFraction returns ContinuedFraction:
    Let precision be 100
    Let decimal1 be Continued.to_bigdecimal(cf1, precision)
    Let decimal2 be Continued.to_bigdecimal(cf2, precision)
    
    Let product_decimal be BigDecimal.multiply(decimal1, decimal2, precision)
    
    Return Continued.create_from_decimal(product_decimal, 50)

Note: Test multiplication with √2 × √2 = 2
Let sqrt_2_cf be sqrt_continued_fraction(2)
Let sqrt_2_squared be multiply_continued_fractions(sqrt_2_cf, sqrt_2_cf)

Display "√2 × √2 continued fraction:"
Display Continued.to_string(sqrt_2_squared)

Note: Should be very close to [2]
Let expected_2 be Continued.create_from_coefficients(Array[BigInteger]([BigInteger.create_from_integer(2)]))
Let difference_cf be Continued.subtract_continued_fractions(sqrt_2_squared, expected_2)
let difference_decimal be Continued.to_bigdecimal(difference_cf, 30)

Display "Error from 2: " joined with BigDecimal.to_scientific_string(BigDecimal.abs(difference_decimal), 5)
```

## Applications

### Calendar Calculations  
```runa
Note: Solar year length approximation using continued fractions
Let tropical_year_days be BigDecimal.create_from_string("365.24219904")  Note: Mean tropical year
Let year_cf be Continued.create_from_decimal(tropical_year_days, 20)

Display "Tropical year in days as continued fraction:"
Display Continued.to_string(year_cf)

Let year_convergents be Continued.calculate_convergents(year_cf, 10)

Display "Calendar approximations:"
For Each conv in year_convergents:
    Let days_per_year be Rational.create_from_bigintegers(conv.numerator, conv.denominator)
    Let years_in_cycle be BigInteger.to_integer(conv.denominator)
    Let days_in_cycle be BigInteger.to_integer(conv.numerator)
    Let leap_days be days_in_cycle - (years_in_cycle * 365)
    
    If years_in_cycle <= 10000:  Note: Only show practical calendar cycles
        Display "  " joined with String(years_in_cycle) joined with " years = " joined with 
                String(days_in_cycle) joined with " days (+" joined with String(leap_days) joined with " leap days)"
        Display "    Error per year: " joined with 
                Rational.to_decimal_string(
                    Rational.abs(Rational.subtract(days_per_year, 
                        Rational.create_from_decimal("365.24219904"))), 10
                ) joined with " days"
```

### Musical Temperament
```runa
Note: Equal temperament vs just intonation using continued fractions
Let semitone_ratio be BigDecimal.power(BigDecimal.create_from_string("2"), 
                                      BigDecimal.create_from_rational(Rational.create(1, 12)), 50)  Note: 12th root of 2

Let semitone_cf be Continued.create_from_decimal(semitone_ratio, 30)

Display "12-TET semitone ratio continued fraction:"
Display Continued.to_string(semitone_cf)

Note: Compare with just intonation ratios
Let just_ratios be Array[Rational]()
just_ratios.add(Rational.create(16, 15))  Note: Minor second
just_ratios.add(Rational.create(9, 8))    Note: Major second  
just_ratios.add(Rational.create(6, 5))    Note: Minor third
just_ratios.add(Rational.create(5, 4))    Note: Major third

Display "Just intonation vs 12-TET comparison:"
For i from 0 to just_ratios.length - 1:
    Let just_ratio be just_ratios[i]
    Let tet_ratio be BigDecimal.power(semitone_ratio, BigDecimal.create_from_integer(i + 1), 30)
    
    Let difference be Rational.abs(Rational.subtract(just_ratio, Rational.create_from_bigdecimal(tet_ratio)))
    Let cents_diff be BigDecimal.multiply(
        BigDecimal.natural_log(Rational.to_bigdecimal(Rational.divide(just_ratio, Rational.create_from_bigdecimal(tet_ratio)), 30), 30),
        BigDecimal.create_from_string("1731.23404907"),  Note: 1200 / ln(2) for cents conversion
        10
    )
    
    Display "  Interval " joined with String(i + 1) joined with ": " joined with 
            BigDecimal.to_string(cents_diff) joined with " cents difference"
```

### Diophantine Equations
```runa
Note: Solve Pell equation x² - ny² = 1 using continued fractions
Process called "solve_pell_equation" that takes n as Integer returns PellSolution:
    If Integer.is_perfect_square(n):
        Return PellSolution.NO_SOLUTION  Note: No solution for perfect squares
    
    Let sqrt_n_cf be sqrt_continued_fraction(n)
    Let period_length be sqrt_n_cf.period_length
    
    Note: Solution comes from convergents
    Let convergent_index be period_length - 1
    If period_length % 2 == 0:
        Set convergent_index to 2 * period_length - 1
    
    Let convergents be Continued.calculate_convergents(sqrt_n_cf, convergent_index + 1)
    Let solution_conv be convergents[convergent_index]
    
    Let x be solution_conv.numerator
    Let y be solution_conv.denominator
    
    Note: Verify x² - ny² = 1
    Let x_squared be BigInteger.multiply(x, x)
    Let ny_squared be BigInteger.multiply(BigInteger.create_from_integer(n), BigInteger.multiply(y, y))
    Let pell_value be BigInteger.subtract(x_squared, ny_squared)
    
    Return PellSolution with:
        x: x
        y: y
        verified: BigInteger.equals(pell_value, BigInteger.ONE)

Let pell_solutions be Array[PellSolution]()
Let test_values be Array[Integer]([2, 3, 5, 6, 7, 8, 10])

Display "Pell equation solutions (x² - ny² = 1):"
For Each n in test_values:
    Let solution be solve_pell_equation(n)
    If solution.verified:
        Display "n=" joined with String(n) joined with ": x=" joined with 
                BigInteger.to_string(solution.x, 10) joined with ", y=" joined with 
                BigInteger.to_string(solution.y, 10)
```

## Performance Optimization

### Efficient Convergent Calculation
```runa
Note: Optimized convergent calculation using matrix multiplication
Process called "fast_convergents" that takes cf as ContinuedFraction, count as Integer returns Array[Convergent]:
    Note: Use matrix formulation: [pn; qn] = [an 1; 1 0] * [pn-1; qn-1]
    
    Let convergents be Array[Convergent]()
    
    Note: Initialize with p-1 = 1, p0 = a0, q-1 = 0, q0 = 1
    Let p_prev2 be BigInteger.ONE
    Let p_prev1 be cf.coefficients[0]
    Let q_prev2 be BigInteger.ZERO
    Let q_prev1 be BigInteger.ONE
    
    convergents.add(Convergent with:
        numerator: p_prev1
        denominator: q_prev1
        index: 0
        error_bound: Rational.create(BigInteger.ONE, q_prev1)
    )
    
    For i from 1 to Integer.min(count - 1, cf.coefficients.length - 1):
        Let an be cf.coefficients[i]
        
        Let p_current be BigInteger.add(BigInteger.multiply(an, p_prev1), p_prev2)
        Let q_current be BigInteger.add(BigInteger.multiply(an, q_prev1), q_prev2)
        
        convergents.add(Convergent with:
            numerator: p_current
            denominator: q_current
            index: i
            error_bound: Rational.create(BigInteger.ONE, BigInteger.multiply(q_current, q_prev1))
        )
        
        Set p_prev2 to p_prev1
        Set p_prev1 to p_current
        Set q_prev2 to q_prev1
        Set q_prev1 to q_current
    
    Return convergents
```

### Memory-Efficient Operations
```runa
Note: Memory-efficient continued fraction operations
Let memory_config be ContinuedFractionMemoryConfig with:
    lazy_convergent_calculation: true
    coefficient_pooling: true
    precision_on_demand: true
    cache_periodic_patterns: true

Continued.configure_memory(memory_config)

Note: Streaming convergent calculation for very long expansions
Process called "stream_convergents" that takes cf_generator as CoefficientGenerator, max_convergents as Integer returns ConvergentStream:
    Let stream be ConvergentStream()
    
    Let p_prev2 be BigInteger.ONE
    Let p_prev1 be BigInteger.ZERO
    Let q_prev2 be BigInteger.ZERO  
    Let q_prev1 be BigInteger.ONE
    
    Let convergent_count be 0
    While convergent_count < max_convergents and cf_generator.has_next():
        Let an be cf_generator.next()
        
        If convergent_count == 0:
            Set p_prev1 to an
        Otherwise:
            Let p_current be BigInteger.add(BigInteger.multiply(an, p_prev1), p_prev2)
            Let q_current be BigInteger.add(BigInteger.multiply(an, q_prev1), q_prev2)
            
            stream.add_convergent(Convergent with:
                numerator: p_current
                denominator: q_current
                index: convergent_count
            )
            
            Set p_prev2 to p_prev1
            Set p_prev1 to p_current
            Set q_prev2 to q_prev1
            Set q_prev1 to q_current
        
        Set convergent_count to convergent_count + 1
    
    Return stream
```

## Error Handling

### Exception Types
The Continued module defines several specific exception types:

- **InvalidExpansion**: Invalid continued fraction coefficients
- **ConvergenceError**: Convergent calculation failed
- **PeriodicityError**: Error in periodic pattern detection
- **ApproximationError**: Approximation quality insufficient

### Error Handling Examples
```runa
Try:
    Let invalid_coeffs be Array[BigInteger]()
    invalid_coeffs.add(BigInteger.create_from_integer(-1))  Note: Negative coefficient invalid
    Let invalid_cf be Continued.create_from_coefficients(invalid_coeffs)
Catch Errors.InvalidExpansion as error:
    Display "Invalid expansion: " joined with error.message
    Display "All coefficients except the first must be positive"

Try:
    Let very_large_cf be Continued.create_from_decimal(
        BigDecimal.create_from_string("1e10000"), 1000000
    )
Catch Errors.ConvergenceError as error:
    Display "Convergence error: " joined with error.message
    Display "Consider reducing precision requirements or expansion length"
```

## Testing and Validation

### Mathematical Identity Verification
```runa
Note: Test fundamental continued fraction identities
Process called "test_continued_fraction_identities" returns Boolean:
    Let all_tests_pass be true
    
    Note: Test that [a0; a1, a2, ...] conversion is correct
    Let test_rational be Rational.create(1415926535, 1000000000)  Note: π approximation
    Let cf be Continued.create_from_rational(test_rational)
    Let reconstructed be Continued.to_rational(cf)
    
    If not Rational.equals(test_rational, reconstructed):
        Display "Rational conversion test failed"
        Set all_tests_pass to false
    
    Note: Test convergent properties
    Let golden_cf be Continued.create_from_coefficients(Array[BigInteger]([BigInteger.ONE] * 20))
    Let convergents be Continued.calculate_convergents(golden_cf, 10)
    
    Note: Test that pn*qn-1 - pn-1*qn = (-1)^(n-1)
    For i from 1 to convergents.length - 1:
        Let pn be convergents[i].numerator
        Let qn be convergents[i].denominator  
        Let pn_1 be convergents[i - 1].numerator
        Let qn_1 be convergents[i - 1].denominator
        
        Let determinant be BigInteger.subtract(
            BigInteger.multiply(pn, qn_1),
            BigInteger.multiply(pn_1, qn)
        )
        
        Let expected be BigInteger.create_from_integer((-1) ^ (i - 1))
        
        If not BigInteger.equals(determinant, expected):
            Display "Convergent determinant test failed at index " joined with String(i)
            Set all_tests_pass to false
    
    Return all_tests_pass

Let identity_tests_pass be test_continued_fraction_identities()
Display "Continued fraction identity tests: " joined with String(identity_tests_pass)
```

### Approximation Quality Testing
```runa
Note: Test approximation quality bounds
Process called "test_approximation_quality" that takes target as BigDecimal, max_denom as Integer returns QualityReport:
    Let cf be Continued.create_from_decimal(target, 100)
    Let approximations be best_approximations_bounded_denominator(target, max_denom)
    
    Let quality_report be QualityReport()
    
    For Each approx in approximations:
        Let theoretical_bound be BigDecimal.divide(
            BigDecimal.ONE,
            BigDecimal.multiply(
                BigDecimal.create_from_string("2"),
                BigDecimal.power(BigDecimal.create_from_biginteger(Rational.get_denominator(approx.best_approximation), 20), BigDecimal.create_from_string("2"), 20),
                20
            ),
            20
        )
        
        Let meets_bound be BigDecimal.compare(approx.error, theoretical_bound) < 0
        
        quality_report.add_result(ApproximationQuality with:
            approximation: approx.best_approximation
            actual_error: approx.error
            theoretical_bound: theoretical_bound
            bound_satisfied: meets_bound
        )
    
    Return quality_report

Let sqrt_2_decimal be BigDecimal.create_from_string("1.41421356237309504880168872420969807856967187537694")
Let quality_report be test_approximation_quality(sqrt_2_decimal, 1000)

Display "√2 approximation quality report:"
For Each result in quality_report.results:
    Display "  " joined with Rational.to_string(result.approximation) joined with 
            ": bound satisfied = " joined with String(result.bound_satisfied)
```

## Best Practices

### 1. Precision Management
```runa
Note: Guidelines for precision in continued fraction operations
Process called "recommend_precision" that takes operation_type as String, input_precision as Integer returns Integer:
    If operation_type == "rational_conversion":
        Return input_precision  Note: Exact operation
    Otherwise If operation_type == "decimal_expansion":
        Return input_precision + 20  Note: Extra precision for convergence
    Otherwise If operation_type == "arithmetic_operations":
        Return input_precision + 50  Note: Significant extra precision needed
    Otherwise:
        Return input_precision + 10  Note: Conservative buffer
```

### 2. Performance Optimization
```runa
Note: Choose efficient algorithms based on requirements
Process called "select_algorithm" that takes cf_length as Integer, convergent_count as Integer returns String:
    If convergent_count <= 10:
        Return "direct_recurrence"      Note: Simple recurrence relations
    Otherwise If cf_length > 1000000:
        Return "streaming_computation"   Note: Memory-efficient for long expansions
    Otherwise If convergent_count > 1000:
        Return "matrix_multiplication"   Note: Faster for many convergents
    Otherwise:
        Return "optimized_recurrence"    Note: Balanced approach
```

### 3. Memory Management
```runa
Note: Manage memory for large continued fraction computations
Process called "configure_for_large_computation" that takes expansion_length as Integer returns MemoryConfig:
    Return MemoryConfig with:
        lazy_evaluation: expansion_length > 10000
        coefficient_caching: expansion_length < 100000
        streaming_mode: expansion_length > 1000000
        precision_scaling: true
```

## Integration Examples

### With Rational Module
```runa
Import "math/precision/continued" as Continued
Import "math/precision/rational" as Rational

Note: Convert between continued fractions and rationals
Let fraction be Rational.create(1414213562, 1000000000)  Note: √2 approximation
Let cf_expansion be Continued.create_from_rational(fraction)
Let convergents be Continued.calculate_convergents(cf_expansion, 5)

Display "Rational to continued fraction to convergents:"
Display "Original: " joined with Rational.to_string(fraction)
Display "CF: " joined with Continued.to_string(cf_expansion)

For Each conv in convergents:
    Let conv_rational be Rational.create_from_bigintegers(conv.numerator, conv.denominator)
    Display "C" joined with String(conv.index) joined with ": " joined with Rational.to_string(conv_rational)
```

### With BigDecimal Module
```runa
Import "math/precision/continued" as Continued
Import "math/precision/bigdecimal" as BigDecimal

Note: High-precision continued fraction calculations
Let pi_high_precision be BigDecimal.create_from_string("3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679")

Let pi_cf be Continued.create_from_decimal(pi_high_precision, 50)
Let pi_convergents be Continued.calculate_convergents(pi_cf, 15)

Display "High-precision π convergents:"
For Each conv in pi_convergents.slice(10, 15):  Note: Show convergents 10-15
    Let conv_decimal be BigDecimal.divide(
        BigDecimal.create_from_biginteger(conv.numerator, 100),
        BigDecimal.create_from_biginteger(conv.denominator, 100),
        100
    )
    Display "C" joined with String(conv.index) joined with " = " joined with BigDecimal.to_string(conv_decimal)
```

The Continued Fractions module provides sophisticated tools for working with continued fraction representations, enabling applications in number theory, approximation theory, calendar calculations, musical temperament, and solving Diophantine equations with high precision and mathematical rigor.