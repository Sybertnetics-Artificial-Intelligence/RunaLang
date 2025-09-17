# Gamma Function Family

The **gamma** module provides comprehensive implementations of the gamma function and related special functions, including beta functions, incomplete gamma functions, digamma, polygamma, and factorial operations. These functions are fundamental to mathematical analysis, probability theory, and many areas of applied mathematics.

## Overview

The gamma function is one of the most important special functions in mathematics, serving as a continuous extension of the factorial function. This module provides high-precision implementations with multiple computational methods optimized for different parameter ranges and applications.

## Key Features

- **Complete Gamma Function Family**: Gamma, log-gamma, incomplete gamma functions
- **Beta Function Operations**: Complete and incomplete beta functions with optimizations
- **Factorial Extensions**: Generalized factorials and Pochhammer symbols
- **Digamma and Polygamma**: Logarithmic derivatives of gamma function
- **Multiple Algorithms**: Series expansions, asymptotic formulas, and special methods
- **High Precision**: Arbitrary precision arithmetic with error estimation

## Mathematical Foundation

### Gamma Function Definition

The gamma function extends the factorial to real and complex numbers:

```
Γ(z) = ∫₀^∞ t^(z-1) e^(-t) dt    (Re z > 0)
```

**Key Properties:**
- **Functional Equation**: Γ(z+1) = z Γ(z)  
- **Factorial Extension**: Γ(n) = (n-1)! for positive integers n
- **Reflection Formula**: Γ(z) Γ(1-z) = π / sin(πz)
- **Duplication Formula**: Γ(z) Γ(z+1/2) = √π 2^(1-2z) Γ(2z)

### Beta Function
```  
B(a,b) = ∫₀¹ t^(a-1) (1-t)^(b-1) dt = Γ(a)Γ(b)/Γ(a+b)
```

### Incomplete Gamma Functions
- **Lower**: γ(s,x) = ∫₀ˣ t^(s-1) e^(-t) dt
- **Upper**: Γ(s,x) = ∫ₓ^∞ t^(s-1) e^(-t) dt

## Data Types

### Configuration Structure

```runa
Type called "GammaConfig":
    precision as Float                    Note: Computational precision
    max_iterations as Integer             Note: Maximum iterations
    convergence_threshold as Float        Note: Convergence tolerance  
    series_method as String              Note: "lanczos", "stirling", "series"
    asymptotic_threshold as Float        Note: Switch point for asymptotics
    lanczos_coefficients as List[Float]  Note: Precomputed Lanczos coefficients
    stirling_corrections as List[Float]  Note: Stirling's correction terms
```

### Result Structure

```runa
Type called "GammaResult":
    value as Float                       Note: Function value
    error_estimate as Float              Note: Estimated error
    iterations_used as Integer           Note: Iterations for convergence
    method_used as String               Note: Algorithm used
    convergence_status as String        Note: "converged" or error status
    derivative_values as List[Float]    Note: Derivatives if computed
```

### Beta Function Configuration

```runa
Type called "BetaConfig":
    precision as Float                   Note: Computational precision
    integration_method as String        Note: "continued_fraction", "series"
    max_subdivisions as Integer         Note: Integration subdivisions
    continued_fraction_depth as Integer Note: CF truncation depth
    symmetry_optimization as Boolean   Note: Use B(a,b) = B(b,a) optimization
```

### Factorial Configuration

```runa
Type called "FactorialConfig":
    cache_size as Integer                Note: Factorial cache size
    stirling_approximation_threshold as Integer Note: Use Stirling for n > threshold  
    extended_precision as Boolean        Note: Use extended precision
    overflow_handling as String         Note: "error", "infinity", "log"
```

## Gamma Function Operations

### Basic Gamma Function

```runa
Import "math/special/gamma" as Gamma

Process called "compute_basic_gamma_values":
    Let config be Gamma.GammaConfig[
        precision: 15.0,
        max_iterations: 100,
        convergence_threshold: 1e-14,
        series_method: "lanczos",
        asymptotic_threshold: 10.0,
        lanczos_coefficients: [],
        stirling_corrections: []
    ]
    
    Note: Compute some important gamma values
    Let gamma_half be Gamma.compute_gamma[0.5, config]
    Print("Γ(1/2) = " + gamma_half.value.to_string[] + " (√π ≈ 1.7724538509...)")
    Print("Method used: " + gamma_half.method_used)
    Print("Error estimate: " + gamma_half.error_estimate.to_string[])
    
    Let gamma_1 be Gamma.compute_gamma[1.0, config]
    Print("Γ(1) = " + gamma_1.value.to_string[] + " (should be exactly 1)")
    
    Let gamma_2 be Gamma.compute_gamma[2.0, config]
    Print("Γ(2) = " + gamma_2.value.to_string[] + " (should be exactly 1)")
    
    Let gamma_3 be Gamma.compute_gamma[3.0, config]
    Print("Γ(3) = " + gamma_3.value.to_string[] + " (should be exactly 2)")
    
    Note: Test negative arguments using reflection formula
    Let gamma_neg_half be Gamma.compute_gamma[-0.5, config]
    Print("Γ(-1/2) = " + gamma_neg_half.value.to_string[] + " (-2√π ≈ -3.5449077018...)")
    
    Return config
```

### Log-Gamma Function

```runa
Process called "demonstrate_log_gamma":
    Let config be create_gamma_config[]
    
    Note: Log-gamma is more stable for large arguments
    Let large_arg be 100.0
    Let log_gamma_100 be Gamma.compute_log_gamma[large_arg, config]
    Print("log Γ(100) = " + log_gamma_100.value.to_string[])
    Print("This avoids overflow that would occur with Γ(100)")
    
    Note: Verify using relationship: log Γ(n) = log((n-1)!) = Σ log(k) for k=1 to n-1
    Let direct_sum be 0.0
    For k from 1 to 99:
        Let direct_sum be direct_sum + MathOps.natural_log[k.to_string[]]
    
    Print("Direct sum of logarithms: " + direct_sum.to_string[])
    Print("Difference: " + MathOps.absolute[log_gamma_100.value - direct_sum].to_string[])
    
    Note: Complex log-gamma for complex arguments  
    Let complex_result be Gamma.compute_log_gamma_complex[2.5, 1.5, config]
    Print("log Γ(2.5 + 1.5i) = " + complex_result["real_part"].to_string[] + 
          " + " + complex_result["imaginary_part"].to_string[] + "i")
    
    Return log_gamma_100
```

## Beta Function Operations

### Complete Beta Function

```runa
Process called "demonstrate_beta_function":
    Let beta_config be Gamma.BetaConfig[
        precision: 15.0,
        integration_method: "continued_fraction",
        max_subdivisions: 100,
        continued_fraction_depth: 50,
        symmetry_optimization: true
    ]
    
    Note: Basic beta function computations
    Let beta_2_3 be Gamma.compute_beta[2.0, 3.0, beta_config]
    Print("B(2,3) = " + beta_2_3.to_string[] + " (should be 1/12 ≈ 0.08333...)")
    
    Note: Verify using gamma function relationship: B(a,b) = Γ(a)Γ(b)/Γ(a+b)
    Let gamma_config be create_gamma_config[]
    Let gamma_2 be Gamma.compute_gamma[2.0, gamma_config].value
    Let gamma_3 be Gamma.compute_gamma[3.0, gamma_config].value  
    Let gamma_5 be Gamma.compute_gamma[5.0, gamma_config].value
    Let beta_via_gamma be (gamma_2 * gamma_3) / gamma_5
    
    Print("B(2,3) via gamma: " + beta_via_gamma.to_string[])
    Print("Direct beta: " + beta_2_3.to_string[])
    Print("Difference: " + MathOps.absolute[beta_2_3 - beta_via_gamma].to_string[])
    
    Note: Beta function with non-integer arguments
    Let beta_half_half be Gamma.compute_beta[0.5, 0.5, beta_config]
    Print("B(1/2, 1/2) = " + beta_half_half.to_string[] + " (should be π)")
    
    Return beta_config
```

### Incomplete Beta Function

```runa
Process called "demonstrate_incomplete_beta":
    Let beta_config be create_beta_config[]
    
    Note: Incomplete beta function I_x(a,b) = B_x(a,b) / B(a,b)
    Let x be 0.3
    Let a be 2.0  
    Let b be 5.0
    
    Let incomplete_beta be Gamma.compute_incomplete_beta[x, a, b, beta_config]
    Print("I_0.3(2,5) = " + incomplete_beta.to_string[])
    
    Note: This is related to cumulative distribution function of Beta distribution
    Print("This gives the CDF of Beta(2,5) distribution at x = 0.3")
    
    Note: Verify boundary conditions
    Let incomplete_beta_0 be Gamma.compute_incomplete_beta[0.0, a, b, beta_config]
    Let incomplete_beta_1 be Gamma.compute_incomplete_beta[1.0, a, b, beta_config]
    
    Print("I_0(2,5) = " + incomplete_beta_0.to_string[] + " (should be 0)")
    Print("I_1(2,5) = " + incomplete_beta_1.to_string[] + " (should be 1)")
    
    Note: Regularized incomplete beta function
    Let regularized_beta be Gamma.compute_regularized_incomplete_beta[x, a, b, beta_config]
    Print("B_0.3(2,5) = " + regularized_beta.to_string[])
    
    Return incomplete_beta
```

## Incomplete Gamma Functions

### Lower and Upper Incomplete Gamma

```runa
Process called "demonstrate_incomplete_gamma":
    Let config be create_gamma_config[]
    
    Let s be 2.5
    Let x be 3.0
    
    Note: Lower incomplete gamma γ(s,x)
    Let lower_gamma be Gamma.compute_lower_incomplete_gamma[s, x, config]
    Print("γ(2.5, 3) = " + lower_gamma.value.to_string[])
    Print("Method: " + lower_gamma.method_used)
    
    Note: Upper incomplete gamma Γ(s,x)  
    Let upper_gamma be Gamma.compute_upper_incomplete_gamma[s, x, config]
    Print("Γ(2.5, 3) = " + upper_gamma.value.to_string[])
    
    Note: Verify completeness: γ(s,x) + Γ(s,x) = Γ(s)
    Let complete_gamma be Gamma.compute_gamma[s, config].value
    Let sum_incomplete be lower_gamma.value + upper_gamma.value
    
    Print("γ(2.5, 3) + Γ(2.5, 3) = " + sum_incomplete.to_string[])
    Print("Γ(2.5) = " + complete_gamma.to_string[])
    Print("Difference: " + MathOps.absolute[complete_gamma - sum_incomplete].to_string[])
    
    Note: Regularized incomplete gamma functions
    Let reg_lower be Gamma.compute_regularized_lower_gamma[s, x, config]
    Let reg_upper be Gamma.compute_regularized_upper_gamma[s, x, config]
    
    Print("P(2.5, 3) = γ(2.5, 3)/Γ(2.5) = " + reg_lower.to_string[])
    Print("Q(2.5, 3) = Γ(2.5, 3)/Γ(2.5) = " + reg_upper.to_string[])
    Print("P + Q = " + (reg_lower + reg_upper).to_string[] + " (should be 1)")
    
    Return lower_gamma
```

## Factorial and Pochhammer Symbol

### Generalized Factorial Operations

```runa
Process called "demonstrate_factorial_operations":
    Let factorial_config be Gamma.FactorialConfig[
        cache_size: 100,
        stirling_approximation_threshold: 20,
        extended_precision: true,
        overflow_handling: "log"
    ]
    
    Note: Standard factorial computations
    For n from 0 to 10:
        Let factorial_result be Gamma.compute_factorial[n, factorial_config]
        Print(n.to_string[] + "! = " + factorial_result.factorial_value.to_string[])
    
    Note: Large factorials using Stirling's approximation
    Let large_n be 50
    Let large_factorial be Gamma.compute_factorial[large_n, factorial_config]
    Print(large_n.to_string[] + "! ≈ " + large_factorial.factorial_value.to_string[])
    Print("Method: " + large_factorial.method_used)
    
    Note: Double factorial n!! = n(n-2)(n-4)...
    Let double_factorial_9 be Gamma.compute_double_factorial[9]
    Print("9!! = " + double_factorial_9.to_string[] + " = 9×7×5×3×1 = 945")
    
    Let double_factorial_10 be Gamma.compute_double_factorial[10] 
    Print("10!! = " + double_factorial_10.to_string[] + " = 10×8×6×4×2 = 3840")
    
    Return factorial_config
```

### Pochhammer Symbol (Rising Factorial)

```runa
Process called "demonstrate_pochhammer_symbol":
    Let config be create_gamma_config[]
    
    Note: Pochhammer symbol (a)_n = a(a+1)(a+2)...(a+n-1) = Γ(a+n)/Γ(a)
    Let a be 2.5
    Let n be 4
    
    Let pochhammer be Gamma.compute_pochhammer_symbol[a, n, config]
    Print("(2.5)_4 = " + pochhammer.to_string[])
    
    Note: Verify by direct computation
    Let direct_product be a * (a+1.0) * (a+2.0) * (a+3.0)
    Print("Direct: 2.5 × 3.5 × 4.5 × 5.5 = " + direct_product.to_string[])
    
    Note: Verify using gamma function relationship
    Let gamma_a_plus_n be Gamma.compute_gamma[a + n.to_float[], config].value
    Let gamma_a be Gamma.compute_gamma[a, config].value
    Let pochhammer_via_gamma be gamma_a_plus_n / gamma_a
    
    Print("Via gamma: Γ(6.5)/Γ(2.5) = " + pochhammer_via_gamma.to_string[])
    Print("Difference: " + MathOps.absolute[pochhammer - pochhammer_via_gamma].to_string[])
    
    Note: Binomial coefficient using Pochhammer symbols
    Let binomial_10_4 be Gamma.compute_binomial_coefficient[10, 4, config]
    Print("C(10,4) = " + binomial_10_4.to_string[] + " (should be 210)")
    
    Return pochhammer
```

## Digamma and Polygamma Functions

### Digamma Function (ψ Function)

```runa
Process called "demonstrate_digamma_function":
    Let config be create_gamma_config[]
    
    Note: Digamma function ψ(z) = d/dz log Γ(z) = Γ'(z)/Γ(z)
    
    Note: Special values
    Let psi_1 be Gamma.compute_digamma[1.0, config]
    Print("ψ(1) = " + psi_1.to_string[] + " (should be -γ ≈ -0.57721566...)")
    
    Let psi_half be Gamma.compute_digamma[0.5, config]
    Print("ψ(1/2) = " + psi_half.to_string[] + " (should be -γ - 2ln(2) ≈ -1.9635100...)")
    
    Let psi_2 be Gamma.compute_digamma[2.0, config]
    Print("ψ(2) = " + psi_2.to_string[] + " (should be 1 - γ ≈ 0.4227843...)")
    
    Note: Recurrence relation: ψ(z+1) = ψ(z) + 1/z
    Let psi_2_5 be Gamma.compute_digamma[2.5, config]
    Let psi_1_5 be Gamma.compute_digamma[1.5, config]
    Let recurrence_check be psi_1_5 + 1.0/1.5
    
    Print("ψ(2.5) = " + psi_2_5.to_string[])
    Print("ψ(1.5) + 1/1.5 = " + recurrence_check.to_string[])
    Print("Recurrence check difference: " + MathOps.absolute[psi_2_5 - recurrence_check].to_string[])
    
    Return psi_1
```

### Polygamma Functions  

```runa
Process called "demonstrate_polygamma_functions":
    Let config be create_gamma_config[]
    
    Note: Polygamma functions ψ^(n)(z) = d^(n+1)/dz^(n+1) log Γ(z)
    
    Let z be 2.0
    
    Note: First polygamma (trigamma) ψ^(1)(z)
    Let trigamma be Gamma.compute_polygamma[1, z, config]
    Print("ψ'(2) = " + trigamma.value.to_string[] + " (trigamma function)")
    
    Note: Second polygamma ψ^(2)(z)  
    Let second_polygamma be Gamma.compute_polygamma[2, z, config]
    Print("ψ''(2) = " + second_polygamma.value.to_string[])
    
    Note: Higher order polygamma functions
    For order from 3 to 6:
        Let nth_polygamma be Gamma.compute_polygamma[order, z, config]
        Print("ψ^(" + order.to_string[] + ")(2) = " + nth_polygamma.value.to_string[])
    
    Note: Special values for trigamma function
    Let trigamma_1 be Gamma.compute_polygamma[1, 1.0, config]
    Print("ψ'(1) = " + trigamma_1.value.to_string[] + " (should be π²/6 ≈ 1.6449340...)")
    
    Let trigamma_half be Gamma.compute_polygamma[1, 0.5, config]
    Print("ψ'(1/2) = " + trigamma_half.value.to_string[] + " (should be π²/2 ≈ 4.9348022...)")
    
    Return trigamma
```

## Advanced Applications

### Probability Distributions

```runa
Process called "demonstrate_gamma_in_probability":
    Let config be create_gamma_config[]
    
    Note: Gamma distribution probability density function
    Process called "gamma_pdf" that takes x as Float, shape as Float, rate as Float returns Float:
        Note: f(x; α, β) = (β^α / Γ(α)) x^(α-1) e^(-βx)
        If x <= 0.0:
            Return 0.0
        
        Let gamma_alpha be Gamma.compute_gamma[shape, config].value
        Let coefficient be MathOps.power[rate, shape] / gamma_alpha
        Let density be coefficient * MathOps.power[x, shape - 1.0] * MathOps.exp[-rate * x]
        
        Return density
    
    Let shape_param be 2.0
    Let rate_param be 1.5
    
    Note: Evaluate PDF at various points
    For Each x in [0.5, 1.0, 1.5, 2.0, 3.0]:
        Let pdf_value be gamma_pdf[x, shape_param, rate_param]
        Print("Gamma PDF(" + x.to_string[] + "; α=2, β=1.5) = " + pdf_value.to_string[])
    
    Note: Beta distribution using beta function
    Process called "beta_pdf" that takes x as Float, alpha as Float, beta as Float returns Float:
        Note: f(x; α, β) = x^(α-1) (1-x)^(β-1) / B(α, β)
        If x <= 0.0 or x >= 1.0:
            Return 0.0
        
        Let beta_config be create_beta_config[]
        Let beta_func be Gamma.compute_beta[alpha, beta, beta_config]
        Let density be MathOps.power[x, alpha - 1.0] * MathOps.power[1.0 - x, beta - 1.0] / beta_func
        
        Return density
    
    Let alpha_param be 2.0
    Let beta_param be 3.0
    
    For Each x in [0.1, 0.3, 0.5, 0.7, 0.9]:
        Let pdf_value be beta_pdf[x, alpha_param, beta_param]
        Print("Beta PDF(" + x.to_string[] + "; α=2, β=3) = " + pdf_value.to_string[])
    
    Return "Probability distributions demonstrated"
```

### Statistical Moments

```runa
Process called "compute_statistical_moments":
    Let config be create_gamma_config[]
    
    Note: Moments of gamma distribution: E[X^k] = Γ(α+k)/(β^k Γ(α))
    Let alpha be 3.0  Note: Shape parameter
    Let beta be 2.0   Note: Rate parameter
    
    Note: Raw moments
    For k from 1 to 4:
        Let gamma_alpha_plus_k be Gamma.compute_gamma[alpha + k.to_float[], config].value
        Let gamma_alpha be Gamma.compute_gamma[alpha, config].value
        Let moment_k be gamma_alpha_plus_k / (MathOps.power[beta, k.to_float[]] * gamma_alpha)
        Print("E[X^" + k.to_string[] + "] = " + moment_k.to_string[])
    
    Note: Central moments can be computed using binomial expansion and raw moments
    Let mean be alpha / beta
    Let variance be alpha / (beta * beta)
    
    Print("Mean (μ) = α/β = " + mean.to_string[])  
    Print("Variance (σ²) = α/β² = " + variance.to_string[])
    Print("Standard deviation (σ) = " + MathOps.square_root[variance].to_string[])
    
    Note: Coefficient of variation
    let cv be MathOps.square_root[variance] / mean
    Print("Coefficient of variation = σ/μ = " + cv.to_string[])
    
    Return mean
```

## Error Handling and Validation

### Domain and Convergence Validation

```runa
Process called "demonstrate_error_handling":
    Let config be create_gamma_config[]
    
    Try:
        Note: Test gamma function at poles (negative integers)
        Let gamma_at_pole be Gamma.compute_gamma[-2.0, config]
        Print("This should not be reached - gamma has pole at -2")
    Catch error as Errors.InvalidDomain:
        Print("Correctly caught domain error: " + error.message)
    
    Try:
        Note: Test with very high precision requirements
        Let high_precision_config be config
        Set high_precision_config.precision to 100.0
        Set high_precision_config.convergence_threshold to 1e-99
        
        Let result be Gamma.compute_gamma[1.1, high_precision_config]
        Print("High precision Γ(1.1): " + result.value.to_string[])
        Print("Convergence status: " + result.convergence_status)
        
    Catch error as Errors.ConvergenceFailure:
        Print("Convergence failed: " + error.message)
        Print("Consider increasing max_iterations or adjusting method")
    
    Try:
        Note: Test beta function with problematic parameters
        Let beta_config be create_beta_config[]
        Let problematic_beta be Gamma.compute_incomplete_beta[0.999999, 0.01, 0.01, beta_config]
        Print("Incomplete beta near boundary: " + problematic_beta.to_string[])
        
    Catch error as Errors.NumericalInstability:
        Print("Numerical instability detected: " + error.message)
        Print("Consider using different method or parameter transformation")
    
    Return "Error handling demonstrated"
```

## Best Practices

### Algorithm Selection Guidelines

1. **Gamma Function**:
   - Use Lanczos approximation for general purposes
   - Use asymptotic expansion for |z| > 10
   - Use reflection formula for Re(z) < 0.5

2. **Incomplete Functions**:
   - Use series expansion for small arguments
   - Use continued fractions for moderate arguments  
   - Use asymptotic expansions for large arguments

3. **High Precision**:
   - Increase coefficient precision accordingly
   - Use extended precision arithmetic for critical applications
   - Validate results using different methods

### Performance Optimization

1. **Caching**: Cache frequently used gamma values and coefficients
2. **Method Selection**: Choose algorithms based on argument ranges
3. **Precision Scaling**: Use minimum required precision for efficiency
4. **Precomputation**: Precompute Lanczos and Stirling coefficients

## Integration with Other Modules

- **Statistics**: Probability density functions and moment computations
- **Analysis**: Complex function theory and analytic continuation
- **Numerical Methods**: Integration and series acceleration techniques
- **Combinatorics**: Binomial coefficients and hypergeometric functions

## See Also

- [Beta Function Properties](https://mathworld.wolfram.com/BetaFunction.html)
- [Special Functions Module Overview](README.md) - Module introduction and examples
- [Hypergeometric Functions Guide](hypergeometric.md) - Related special functions
- [Statistics Documentation](../statistics/README.md) - Probability distributions
- [Complex Analysis Documentation](../analysis/README.md) - Complex gamma functions