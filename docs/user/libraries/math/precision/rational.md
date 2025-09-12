# Math Precision Rational Module

## Overview

The `math/precision/rational` module provides exact rational number arithmetic using integer numerator and denominator representation. It implements fraction operations, reduction to lowest terms, continued fraction expansions, and rational approximations, making it essential for exact computation without rounding errors, number theory applications, and mathematical software requiring precise fractional arithmetic.

## Key Features

- **Exact Representation**: No rounding errors in fraction arithmetic
- **Automatic Reduction**: Always maintains lowest terms using GCD algorithms
- **Continued Fractions**: Expansion and convergent calculations
- **Rational Approximation**: Best approximations with controlled error bounds
- **Mixed Numbers**: Support for whole number plus fraction representation
- **Egyptian Fractions**: Decomposition into unit fractions
- **Farey Sequences**: Generation and mediant operations
- **Musical Intervals**: Just intonation and frequency ratio calculations

## Data Types

### Rational
Represents an exact rational number:
```runa
Type called "Rational":
    numerator as BigInteger      Note: Fraction numerator
    denominator as BigInteger    Note: Fraction denominator (always positive)
```

### MixedNumber
Represents a mixed number (whole + fraction):
```runa
Type called "MixedNumber":
    whole_part as BigInteger     Note: Integer part
    fractional_part as Rational  Note: Proper fraction part (< 1)
    is_negative as Boolean       Note: Sign of the mixed number
```

### ContinuedFractionExpansion
Represents continued fraction form:
```runa
Type called "ContinuedFractionExpansion":
    coefficients as Array[BigInteger]  Note: Partial quotients [a0; a1, a2, ...]
    is_finite as Boolean               Note: Whether expansion terminates
    period_start as Integer            Note: Start of repeating period (if any)
    period_length as Integer           Note: Length of repeating period
```

### RationalApproximation
Result of rational approximation:
```runa
Type called "RationalApproximation":
    approximation as Rational    Note: Best rational approximation
    error as Rational           Note: Absolute error
    relative_error as Rational  Note: Relative error
    convergent_index as Integer Note: Which convergent this represents
```

## Basic Operations

### Creating Rational Numbers
```runa
Import "math/precision/rational" as Rational

Note: Create from integers
Let simple_fraction be Rational.create(3, 4)          Note: 3/4
Let improper_fraction be Rational.create(7, 3)        Note: 7/3
Let negative_fraction be Rational.create(-5, 8)       Note: -5/8

Note: Create from strings
Let decimal_as_fraction be Rational.create_from_decimal("0.125")  Note: 1/8
Let repeating_decimal be Rational.create_from_decimal("0.333...")  Note: 1/3

Note: Create from BigIntegers
Let large_numerator be BigInteger.create_from_string("123456789")
Let large_denominator be BigInteger.create_from_string("987654321")
Let large_fraction be Rational.create_from_bigintegers(large_numerator, large_denominator)

Display "Simple fraction: " joined with Rational.to_string(simple_fraction)
Display "From decimal: " joined with Rational.to_string(decimal_as_fraction)
Display "Large fraction: " joined with Rational.to_string(large_fraction)
```

### Arithmetic Operations
```runa
Note: Basic arithmetic with automatic reduction
Let a be Rational.create(1, 3)   Note: 1/3
Let b be Rational.create(1, 6)   Note: 1/6

Let sum be Rational.add(a, b)           Note: 1/3 + 1/6 = 1/2
Let difference be Rational.subtract(a, b)  Note: 1/3 - 1/6 = 1/6
Let product be Rational.multiply(a, b)      Note: 1/3 * 1/6 = 1/18
Let quotient be Rational.divide(a, b)       Note: (1/3) / (1/6) = 2

Display "Sum: " joined with Rational.to_string(sum)
Display "Difference: " joined with Rational.to_string(difference)
Display "Product: " joined with Rational.to_string(product)
Display "Quotient: " joined with Rational.to_string(quotient)
```

### Power Operations
```runa
Note: Rational exponentiation
Let base be Rational.create(3, 4)        Note: 3/4
Let positive_exp be Rational.power(base, 3)      Note: (3/4)³ = 27/64
Let negative_exp be Rational.power(base, -2)     Note: (3/4)⁻² = 16/9

Let root be Rational.nth_root(Rational.create(8, 27), 3)  Note: ∛(8/27) = 2/3

Display "Cubed: " joined with Rational.to_string(positive_exp)
Display "Negative power: " joined with Rational.to_string(negative_exp)
Display "Cube root: " joined with Rational.to_string(root)
```

## Advanced Operations

### GCD and LCM
```runa
Note: Greatest Common Divisor and Least Common Multiple
Let frac1 be Rational.create(12, 18)    Note: 12/18 = 2/3
Let frac2 be Rational.create(15, 20)    Note: 15/20 = 3/4

Let gcd_result be Rational.gcd(frac1, frac2)
Let lcm_result be Rational.lcm(frac1, frac2)

Display "GCD of 2/3 and 3/4: " joined with Rational.to_string(gcd_result)
Display "LCM of 2/3 and 3/4: " joined with Rational.to_string(lcm_result)
```

### Reduction and Simplification
```runa
Note: Fraction reduction operations
Let unreduced be Rational.create_unreduced(24, 36)  Note: Don't auto-reduce

Display "Unreduced: " joined with Rational.to_string_unreduced(unreduced)  Note: 24/36
Let reduced be Rational.reduce(unreduced)
Display "Reduced: " joined with Rational.to_string(reduced)  Note: 2/3

Note: Check if fraction is in lowest terms
Let is_reduced be Rational.is_in_lowest_terms(unreduced)
Display "Is in lowest terms: " joined with String(is_reduced)  Note: false
```

### Modular Operations
```runa
Note: Modular arithmetic with rationals
Let a be Rational.create(7, 3)
Let b be Rational.create(5, 2)
Let modulus be Rational.create(2, 1)

Let mod_sum be Rational.mod_add(a, b, modulus)
Let mod_product be Rational.mod_multiply(a, b, modulus)

Display "Modular sum: " joined with Rational.to_string(mod_sum)
Display "Modular product: " joined with Rational.to_string(mod_product)
```

## Continued Fractions

### Expansion and Convergents
```runa
Note: Generate continued fraction expansion
Let golden_ratio be Rational.create(1618, 1000)  Note: Approximation of φ

Let cf_expansion be Rational.to_continued_fraction(golden_ratio)
Display "Continued fraction: [" joined with String(cf_expansion.coefficients[0])
For i from 1 to cf_expansion.coefficients.length - 1:
    Display "; " joined with String(cf_expansion.coefficients[i])
Display "]"

Note: Calculate convergents
Let convergents be Rational.calculate_convergents(cf_expansion, 5)
For i from 0 to convergents.length - 1:
    Display "C" joined with String(i) joined with " = " joined with Rational.to_string(convergents[i])
```

### Periodic Continued Fractions
```runa
Note: Detect periodic patterns in continued fractions
Let sqrt_2_approx be Rational.create(14142135, 10000000)  Note: √2 approximation

Let cf_expansion be Rational.to_continued_fraction(sqrt_2_approx)
Let periodic_analysis be Rational.analyze_periodicity(cf_expansion)

If periodic_analysis.is_periodic:
    Display "Periodic continued fraction detected"
    Display "Period starts at: " joined with String(periodic_analysis.period_start)
    Display "Period length: " joined with String(periodic_analysis.period_length)
```

### Best Rational Approximations
```runa
Note: Find best rational approximations within error bounds
Let target_value be Rational.create_from_decimal("3.14159265")  Note: π approximation
Let max_denominator be 1000

Let approximations be Rational.best_approximations(target_value, max_denominator)

Display "Best rational approximations to π:"
For Each approx in approximations:
    Let error be Rational.abs(Rational.subtract(target_value, approx.approximation))
    Display "  " joined with Rational.to_string(approx.approximation) joined with " (error: " joined with Rational.to_decimal_string(error, 10) joined with ")"
```

## Mixed Numbers

### Conversion and Operations
```runa
Note: Mixed number operations
Let improper1 be Rational.create(22, 7)  Note: 22/7 = 3 1/7
Let improper2 be Rational.create(19, 5)  Note: 19/5 = 3 4/5

Let mixed1 be Rational.to_mixed_number(improper1)
Let mixed2 be Rational.to_mixed_number(improper2)

Display "Mixed 1: " joined with MixedNumber.to_string(mixed1)  Note: "3 1/7"
Display "Mixed 2: " joined with MixedNumber.to_string(mixed2)  Note: "3 4/5"

Note: Arithmetic with mixed numbers
Let mixed_sum be MixedNumber.add(mixed1, mixed2)
Let mixed_product be MixedNumber.multiply(mixed1, mixed2)

Display "Sum: " joined with MixedNumber.to_string(mixed_sum)
Display "Product: " joined with MixedNumber.to_string(mixed_product)
```

### Recipe Calculations
```runa
Note: Practical mixed number calculations for cooking
Process called "scale_recipe" that takes ingredients as Array[MixedNumber], scale_factor as Rational returns Array[MixedNumber]:
    Let scaled_ingredients be Array[MixedNumber]()
    
    For Each ingredient in ingredients:
        Let ingredient_rational be MixedNumber.to_rational(ingredient)
        Let scaled_rational be Rational.multiply(ingredient_rational, scale_factor)
        Let scaled_mixed be Rational.to_mixed_number(scaled_rational)
        scaled_ingredients.add(scaled_mixed)
    
    Return scaled_ingredients

Let recipe_amounts be Array[MixedNumber]()
recipe_amounts.add(MixedNumber.create(2, Rational.create(1, 2)))  Note: 2 1/2 cups
recipe_amounts.add(MixedNumber.create(1, Rational.create(3, 4)))  Note: 1 3/4 cups
recipe_amounts.add(MixedNumber.create(0, Rational.create(2, 3)))  Note: 2/3 cup

Let scale_factor be Rational.create(3, 2)  Note: 1.5x recipe
Let scaled_recipe be scale_recipe(recipe_amounts, scale_factor)

Display "Original recipe scaled by 1.5x:"
For i from 0 to scaled_recipe.length - 1:
    Display "  Ingredient " joined with String(i + 1) joined with ": " joined with MixedNumber.to_string(scaled_recipe[i])
```

## Egyptian Fractions

### Unit Fraction Decomposition
```runa
Note: Decompose rational into sum of unit fractions
Let fraction be Rational.create(7, 12)

Let egyptian_expansion be Rational.to_egyptian_fractions(fraction)

Display "7/12 as Egyptian fractions:"
For Each unit_fraction in egyptian_expansion:
    Display "  1/" joined with BigInteger.to_string(Rational.get_denominator(unit_fraction), 10)

Note: Verify the decomposition
Let sum be Rational.ZERO
For Each unit_fraction in egyptian_expansion:
    Set sum to Rational.add(sum, unit_fraction)

Let decomposition_correct be Rational.equals(sum, fraction)
Display "Decomposition verified: " joined with String(decomposition_correct)
```

### Greedy Algorithm
```runa
Note: Egyptian fraction using greedy algorithm
Process called "egyptian_greedy" that takes rational as Rational returns Array[Rational]:
    Let result be Array[Rational]()
    Let remaining be rational
    
    While not Rational.is_zero(remaining):
        Let ceiling_denom be Rational.ceiling_division(Rational.get_denominator(remaining), Rational.get_numerator(remaining))
        Let unit_fraction be Rational.create(BigInteger.ONE, ceiling_denom)
        
        result.add(unit_fraction)
        Set remaining to Rational.subtract(remaining, unit_fraction)
    
    Return result

Let test_fraction be Rational.create(5, 6)
Let greedy_expansion be egyptian_greedy(test_fraction)

Display "5/6 using greedy algorithm:"
For Each unit in greedy_expansion:
    Display "  " joined with Rational.to_string(unit)
```

## Farey Sequences

### Generation and Properties
```runa
Note: Generate Farey sequence of order n
Process called "generate_farey_sequence" that takes order as Integer returns Array[Rational]:
    Let farey_sequence be Array[Rational]()
    
    For denominator from 1 to order:
        For numerator from 0 to denominator:
            If BigInteger.gcd(BigInteger.create_from_integer(numerator), BigInteger.create_from_integer(denominator)) == 1:
                farey_sequence.add(Rational.create(numerator, denominator))
    
    Note: Sort the fractions
    Return Rational.sort_ascending(farey_sequence)

Let farey_5 be generate_farey_sequence(5)

Display "Farey sequence F₅:"
For Each fraction in farey_5:
    Display "  " joined with Rational.to_string(fraction)
```

### Mediant Operations
```runa
Note: Calculate mediant of two fractions
Let a be Rational.create(1, 3)  Note: 1/3
Let b be Rational.create(1, 2)  Note: 1/2

Let mediant be Rational.mediant(a, b)  Note: (1+1)/(3+2) = 2/5

Display "Mediant of 1/3 and 1/2: " joined with Rational.to_string(mediant)

Note: Properties of mediants
Let mediant_between be Rational.compare(a, mediant) < 0 and Rational.compare(mediant, b) < 0
Display "Mediant is between a and b: " joined with String(mediant_between)

Note: Ford circles and mediant trees
Let ford_neighbors be Rational.find_farey_neighbors(mediant, 10)
Display "Farey neighbors of mediant:"
For Each neighbor in ford_neighbors:
    Display "  " joined with Rational.to_string(neighbor)
```

## Musical Applications

### Just Intonation
```runa
Note: Musical intervals as rational numbers
Let unison be Rational.create(1, 1)        Note: 1:1
Let octave be Rational.create(2, 1)        Note: 2:1
Let perfect_fifth be Rational.create(3, 2) Note: 3:2
Let perfect_fourth be Rational.create(4, 3) Note: 4:3
Let major_third be Rational.create(5, 4)    Note: 5:4
Let minor_third be Rational.create(6, 5)    Note: 6:5

Note: Calculate frequency ratios
Let base_frequency be Rational.create(440, 1)  Note: A4 = 440 Hz

Let frequencies be Array[Rational]()
Let intervals be Array[Rational]()
intervals.add(unison)
intervals.add(major_third)
intervals.add(perfect_fifth)
intervals.add(octave)

For Each interval in intervals:
    Let frequency be Rational.multiply(base_frequency, interval)
    frequencies.add(frequency)

Display "Just intonation frequencies (Hz):"
Let note_names be Array[String]()
note_names.add("A4")
note_names.add("C#5")
note_names.add("E5")
note_names.add("A5")

For i from 0 to frequencies.length - 1:
    Display "  " joined with note_names[i] joined with ": " joined with Rational.to_decimal_string(frequencies[i], 2)
```

### Harmonic Series
```runa
Note: Generate harmonic series ratios
Process called "generate_harmonic_ratios" that takes fundamental as Integer, harmonic_count as Integer returns Array[Rational]:
    Let harmonics be Array[Rational]()
    
    For i from 1 to harmonic_count:
        harmonics.add(Rational.create(i, fundamental))
    
    Return harmonics

Let harmonic_ratios be generate_harmonic_ratios(1, 16)

Display "First 16 harmonic ratios:"
For i from 0 to harmonic_ratios.length - 1:
    Let ratio be harmonic_ratios[i]
    Display "  H" joined with String(i + 1) joined with ": " joined with Rational.to_string(ratio)
```

## Comparison and Ordering

### Rational Comparison
```runa
Note: Compare rationals with different denominators
Let a be Rational.create(2, 3)   Note: 2/3
Let b be Rational.create(5, 7)   Note: 5/7
Let c be Rational.create(3, 4)   Note: 3/4

Note: Various comparison operations
Let comparison_ab be Rational.compare(a, b)  Note: < 0 if a < b, 0 if equal, > 0 if a > b
Let is_equal be Rational.equals(a, b)
Let is_less_than be Rational.less_than(a, b)
Let is_greater_than be Rational.greater_than(a, c)

Display "2/3 compared to 5/7: " joined with String(comparison_ab)
Display "2/3 > 3/4: " joined with String(is_greater_than)

Note: Sort array of rationals
Let rational_array be Array[Rational]()
rational_array.add(c)  Note: 3/4
rational_array.add(a)  Note: 2/3  
rational_array.add(b)  Note: 5/7

Let sorted_rationals be Rational.sort_ascending(rational_array)

Display "Sorted rationals:"
For Each rational in sorted_rationals:
    Display "  " joined with Rational.to_string(rational) joined with " = " joined with Rational.to_decimal_string(rational, 4)
```

### Statistical Operations
```runa
Note: Statistical analysis of rational numbers
Let rational_data be Array[Rational]()
rational_data.add(Rational.create(1, 2))
rational_data.add(Rational.create(2, 3))
rational_data.add(Rational.create(3, 4))
rational_data.add(Rational.create(4, 5))
rational_data.add(Rational.create(5, 6))

Let mean be Rational.arithmetic_mean(rational_data)
Let median be Rational.median(rational_data)
Let range be Rational.range(rational_data)

Display "Mean: " joined with Rational.to_string(mean)
Display "Median: " joined with Rational.to_string(median)
Display "Range: " joined with Rational.to_string(range)
```

## Conversion Operations

### Decimal Conversion
```runa
Note: Convert to various decimal representations
Let fraction be Rational.create(22, 7)  Note: 22/7 ≈ π

Let decimal_5_places be Rational.to_decimal_string(fraction, 5)
Let scientific_notation be Rational.to_scientific_string(fraction, 3)
Let percentage be Rational.to_percentage_string(fraction, 2)

Display "22/7 as decimal: " joined with decimal_5_places
Display "Scientific: " joined with scientific_notation
Display "Percentage: " joined with percentage

Note: Detect repeating decimals
Let repeating_result be Rational.to_repeating_decimal(Rational.create(1, 3))
Display "1/3 repeating: " joined with repeating_result.non_repeating_part joined with repeating_result.repeating_part joined with "..."
```

### Other Type Conversions
```runa
Note: Convert to other precision types
Let rational_value be Rational.create(355, 113)  Note: Good π approximation

Let as_bigdecimal be Rational.to_bigdecimal(rational_value, 20)
Let as_float be Rational.to_float(rational_value)
Let as_double be Rational.to_double(rational_value)

Display "As BigDecimal: " joined with BigDecimal.to_string(as_bigdecimal)
Display "As float: " joined with String(as_float)
Display "As double: " joined with String(as_double)
```

## Error Handling

### Exception Types
The Rational module defines several specific exception types:

- **InvalidDenominator**: Zero denominator provided
- **InvalidOperation**: Operation not supported for given inputs
- **ConversionError**: Error converting between types
- **OverflowError**: Result exceeds representable range

### Error Handling Examples
```runa
Try:
    Let invalid_rational be Rational.create(5, 0)  Note: Zero denominator
Catch Errors.InvalidDenominator as error:
    Display "Invalid denominator: " joined with error.message
    Display "Denominator cannot be zero in rational numbers"

Try:
    Let non_rational_root be Rational.nth_root(Rational.create(2, 1), 2)  Note: √2 is irrational
Catch Errors.InvalidOperation as error:
    Display "Cannot represent irrational result as rational: " joined with error.message
    Display "Consider using BigDecimal approximation instead"
```

## Performance Optimization

### Efficient Arithmetic
```runa
Note: Optimize rational arithmetic for performance
Process called "optimize_rational_chain" that takes operations as Array[RationalOperation] returns Rational:
    Note: Combine operations to minimize intermediate reductions
    Let combined_numerator be BigInteger.ONE
    Let combined_denominator be BigInteger.ONE
    
    For Each operation in operations:
        If operation.type == "multiply":
            Set combined_numerator to BigInteger.multiply(combined_numerator, operation.operand.numerator)
            Set combined_denominator to BigInteger.multiply(combined_denominator, operation.operand.denominator)
        Otherwise If operation.type == "divide":
            Set combined_numerator to BigInteger.multiply(combined_numerator, operation.operand.denominator)
            Set combined_denominator to BigInteger.multiply(combined_denominator, operation.operand.numerator)
    
    Note: Only reduce once at the end
    Return Rational.create_from_bigintegers(combined_numerator, combined_denominator)
```

### Memory Management
```runa
Note: Manage memory for large rational computations
Let memory_config be RationalMemoryConfig with:
    reduce_immediately: false    Note: Delay reduction until needed
    cache_gcds: true            Note: Cache GCD calculations
    pool_denominators: true     Note: Reuse common denominators
    
Rational.configure_memory(memory_config)

Note: Monitor rational memory usage
Let memory_stats be Rational.get_memory_statistics()
Display "Rational objects: " joined with String(memory_stats.active_rationals)
Display "Cached GCDs: " joined with String(memory_stats.cached_gcds)
```

## Best Practices

### 1. Choose Appropriate Representation
```runa
Note: Guidelines for when to use rationals vs decimals
Process called "recommend_number_type" that takes use_case as String returns String:
    If use_case == "exact_fractions":
        Return "rational"           Note: Exact arithmetic needed
    Otherwise If use_case == "financial":
        Return "bigdecimal"         Note: Fixed decimal places
    Otherwise If use_case == "scientific":
        Return "bigdecimal"         Note: Controlled precision
    Otherwise If use_case == "music_theory":
        Return "rational"           Note: Exact frequency ratios
    Otherwise:
        Return "consider_requirements"
```

### 2. Performance Optimization
```runa
Note: Optimize rational operations
Process called "optimize_rational_computation" that takes computation_type as String returns OptimizationHints:
    Let hints be OptimizationHints()
    
    If computation_type == "many_multiplications":
        hints.add("delay_reduction_until_end")
        hints.add("combine_operations")
    Otherwise If computation_type == "continued_fractions":
        hints.add("cache_partial_quotients")
        hints.add("use_lazy_evaluation")
    Otherwise If computation_type == "farey_sequences":
        hints.add("precompute_gcd_table")
        hints.add("use_mediant_tree")
    
    Return hints
```

### 3. Precision Management
```runa
Note: Control precision in rational approximations
Process called "set_approximation_precision" that takes target_error as Rational, max_denominator as Integer returns ApproximationConfig:
    Return ApproximationConfig with:
        max_denominator: max_denominator
        target_error: target_error
        prefer_simple_fractions: true
        use_continued_fractions: true
```

## Integration Examples

### With Statistics Module
```runa
Import "math/precision/rational" as Rational
Import "math/statistics/descriptive" as Stats

Note: Exact statistical calculations
Let rational_dataset be Array[Rational]()
rational_dataset.add(Rational.create(1, 2))
rational_dataset.add(Rational.create(2, 3))
rational_dataset.add(Rational.create(3, 4))
rational_dataset.add(Rational.create(4, 5))

Let exact_mean be Stats.arithmetic_mean_rational(rational_dataset)
Let exact_variance be Stats.variance_rational(rational_dataset)

Display "Exact mean: " joined with Rational.to_string(exact_mean)
Display "Exact variance: " joined with Rational.to_string(exact_variance)
```

### With BigInteger Module
```runa
Import "math/precision/rational" as Rational
Import "math/precision/biginteger" as BigInteger

Note: Rational numbers with very large components
Let large_factorial be BigInteger.factorial(100)
Let factorial_ratio be Rational.create_from_bigintegers(large_factorial, BigInteger.factorial(99))

Display "100!/99! = " joined with Rational.to_string(factorial_ratio)
Display "Which equals: " joined with String(BigInteger.to_integer(Rational.get_numerator(factorial_ratio)))
```

## Testing and Validation

### Mathematical Identities
```runa
Note: Test fundamental rational arithmetic identities
Process called "test_rational_identities" returns Boolean:
    Let all_tests_pass be true
    
    Note: Test a + b = b + a (commutativity)
    Let a be Rational.create(2, 3)
    Let b be Rational.create(5, 7)
    
    Let sum_ab be Rational.add(a, b)
    Let sum_ba be Rational.add(b, a)
    
    If not Rational.equals(sum_ab, sum_ba):
        Display "Commutativity test failed"
        Set all_tests_pass to false
    
    Note: Test (a * b) * c = a * (b * c) (associativity)
    Let c be Rational.create(3, 11)
    Let product1 be Rational.multiply(Rational.multiply(a, b), c)
    Let product2 be Rational.multiply(a, Rational.multiply(b, c))
    
    If not Rational.equals(product1, product2):
        Display "Associativity test failed"
        Set all_tests_pass to false
    
    Return all_tests_pass

Let identity_tests_pass be test_rational_identities()
Display "Mathematical identity tests: " joined with String(identity_tests_pass)
```

The Rational module provides the foundation for exact fractional arithmetic in Runa, enabling applications that require mathematical precision, musical interval calculations, and number theory computations without the approximation errors inherent in floating-point representations.