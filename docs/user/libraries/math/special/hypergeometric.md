# Hypergeometric Functions and Series

The **hypergeometric** module provides comprehensive implementations of generalized hypergeometric functions, confluent hypergeometric functions, Kummer functions, Whittaker functions, and Appell functions. These functions are fundamental solutions to differential equations and appear throughout mathematical physics and special function theory.

## Overview

Hypergeometric functions generalize many elementary and special functions as solutions to linear differential equations. This module implements the complete family of hypergeometric functions with multiple computational methods, analytical continuation, and connection formulas.

## Key Features

- **Gauss Hypergeometric Functions**: ₂F₁(a,b;c;z) with all transformations
- **Confluent Functions**: ₁F₁ and U functions with asymptotic expansions  
- **Generalized Functions**: ₚFₑ functions for arbitrary parameters
- **Connection Formulas**: Analytical continuation across branch cuts
- **Series Acceleration**: Convergence improvement techniques
- **Integral Representations**: Alternative computational methods

## Mathematical Foundation

### Gauss Hypergeometric Function
```
₂F₁(a,b;c;z) = Σ_{n=0}^∞ (a)ₙ(b)ₙ zⁿ / ((c)ₙ n!)
```
where (a)ₙ = a(a+1)...(a+n-1) is the Pochhammer symbol.

### Confluent Hypergeometric Functions
```
₁F₁(a;c;z) = Σ_{n=0}^∞ (a)ₙ zⁿ / ((c)ₙ n!)    (Kummer's function)
U(a,c,z) = π/sin(πc) [₁F₁(a;c;z)/Γ(c-a+1) - z^(1-c)₁F₁(a-c+1;2-c;z)/Γ(a)]
```

## Data Types

### Configuration Structure
```runa
Type called "HypergeometricConfig":
    precision as Float                   Note: Computational precision
    max_iterations as Integer            Note: Maximum iteration count
    convergence_threshold as Float       Note: Series convergence tolerance
    series_method as String             Note: "direct", "transformed", "asymptotic"
    transformation_threshold as Float   Note: Apply transformations when |z| > threshold
    integral_method as String          Note: "gauss_quadrature", "adaptive"
    continuation_method as String       Note: Analytical continuation approach
```

### Result Structure
```runa
Type called "HypergeometricResult":
    value as Float                      Note: Function value
    error_estimate as Float             Note: Computation error estimate
    iterations_used as Integer          Note: Iterations for convergence
    method_used as String              Note: Algorithm employed
    convergence_status as String       Note: Convergence information
    series_coefficients as List[Float] Note: Series expansion coefficients
```

## Gauss Hypergeometric Functions

### Basic ₂F₁ Functions

```runa
Import "math/special/hypergeometric" as Hypergeometric

Process called "compute_gauss_hypergeometric":
    Let config be Hypergeometric.HypergeometricConfig[
        precision: 15.0,
        max_iterations: 100,
        convergence_threshold: 1e-14,
        series_method: "direct",
        transformation_threshold: 0.8,
        integral_method: "gauss_quadrature",
        continuation_method: "monodromy"
    ]
    
    Note: Compute ₂F₁ for various parameter sets
    Let test_cases be [
        (1.0, 2.0, 3.0, 0.5),     Note: ₂F₁(1,2;3;0.5)
        (0.5, 0.5, 1.5, 0.25),    Note: ₂F₁(1/2,1/2;3/2;1/4)  
        (2.0, 3.0, 4.0, -0.3),    Note: ₂F₁(2,3;4;-0.3)
        (1.5, -0.5, 2.5, 0.9)     Note: ₂F₁(3/2,-1/2;5/2;0.9)
    ]
    
    For Each case in test_cases:
        Let a be case.0
        Let b be case.1  
        Let c be case.2
        Let z be case.3
        
        Let result be Hypergeometric.compute_hypergeometric_2f1[a, b, c, z, config]
        
        Print("₂F₁(" + a.to_string[] + "," + b.to_string[] + ";" + 
              c.to_string[] + ";" + z.to_string[] + ") = " + result.value.to_string[])
        Print("  Method: " + result.method_used + ", Error: " + result.error_estimate.to_string[])
    
    Note: Special values and identities
    Note: ₂F₁(a,b;c;0) = 1
    Let identity_at_zero be Hypergeometric.compute_hypergeometric_2f1[1.5, 2.5, 3.0, 0.0, config]
    Print("₂F₁(3/2,5/2;3;0) = " + identity_at_zero.value.to_string[] + " (should be 1)")
    
    Note: ₂F₁(1,1;2;z) = -ln(1-z)/z for |z| < 1
    Let special_case be Hypergeometric.compute_hypergeometric_2f1[1.0, 1.0, 2.0, 0.3, config]
    Let expected_value be -MathOps.natural_log[1.0 - 0.3] / 0.3
    Print("₂F₁(1,1;2;0.3) = " + special_case.value.to_string[])
    Print("Expected -ln(0.7)/0.3 = " + expected_value.to_string[])
    
    Return config
```

### Transformations and Continuation

```runa
Process called "demonstrate_hypergeometric_transformations":
    Let config be create_hypergeometric_config[]
    
    Note: Pfaff transformations for analytical continuation
    Let a be 1.5
    Let b be 2.5
    Let c be 3.0
    Let z be 1.2  Note: Outside unit circle
    
    Print("Hypergeometric transformations for |z| > 1:")
    Print("Original: ₂F₁(" + a.to_string[] + "," + b.to_string[] + ";" + c.to_string[] + ";" + z.to_string[] + ")")
    
    Note: Apply transformation z → z/(z-1)
    Let z_transformed be z / (z - 1.0)
    Let a_new be a
    Let b_new be c - b  
    Let c_new be c
    
    Print("Transformed: z' = " + z_transformed.to_string[] + ", b' = c - b = " + b_new.to_string[])
    
    Let result_original be Hypergeometric.compute_hypergeometric_2f1[a, b, c, z, config]
    Let result_transformed be Hypergeometric.compute_hypergeometric_2f1[a_new, b_new, c_new, z_transformed, config]
    
    Note: Apply transformation factor (1-z)^(-a)
    Let transformation_factor be MathOps.power[1.0 - z, -a]
    Let final_result be transformation_factor * result_transformed.value
    
    Print("Direct computation: " + result_original.value.to_string[])
    Print("Via transformation: " + final_result.to_string[])
    Print("Method used: " + result_original.method_used)
    
    Return result_original
```

## Confluent Hypergeometric Functions

### Kummer Functions ₁F₁

```runa
Process called "compute_confluent_hypergeometric":
    Let config be create_hypergeometric_config[]
    
    Note: Confluent hypergeometric function ₁F₁(a;c;z)
    Let test_cases be [
        (1.0, 2.0, 1.0),      Note: ₁F₁(1;2;1)
        (0.5, 1.5, 2.0),      Note: ₁F₁(1/2;3/2;2)
        (2.0, 3.0, -1.0),     Note: ₁F₁(2;3;-1)
        (-1.0, 0.5, 0.5)      Note: ₁F₁(-1;1/2;1/2)
    ]
    
    Print("Confluent hypergeometric functions ₁F₁(a;c;z):")
    For Each case in test_cases:
        Let a be case.0
        Let c be case.1
        Let z be case.2
        
        Let result be Hypergeometric.compute_confluent_hypergeometric_1f1[a, c, z, config]
        
        Print("₁F₁(" + a.to_string[] + ";" + c.to_string[] + ";" + z.to_string[] + ") = " + result.value.to_string[])
        Print("  Convergence: " + result.convergence_status)
    
    Note: Connection to elementary functions
    Note: ₁F₁(1;2;2z) = sinh(z)/z
    Let a be 1.0
    Let c be 2.0
    Let z be 1.0
    Let hyp_result be Hypergeometric.compute_confluent_hypergeometric_1f1[a, c, 2.0*z, config].value
    Let sinh_z_over_z be MathOps.sinh[z] / z
    
    Print("Connection to elementary functions:")
    Print("₁F₁(1;2;2) = " + hyp_result.to_string[])
    Print("sinh(1)/1 = " + sinh_z_over_z.to_string[])
    Print("Difference: " + MathOps.absolute[hyp_result - sinh_z_over_z].to_string[])
    
    Return result
```

### Whittaker Functions

```runa
Process called "compute_whittaker_functions":
    Let config be create_hypergeometric_config[]
    
    Note: Whittaker functions M_{κ,μ}(z) and W_{κ,μ}(z)
    Let kappa be 1.5
    Let mu be 0.5
    Let z be 2.0
    
    Let whittaker_m be Hypergeometric.compute_whittaker_m[kappa, mu, z, config]
    Let whittaker_w be Hypergeometric.compute_whittaker_w[kappa, mu, z, config]
    
    Print("Whittaker functions:")
    Print("M_{" + kappa.to_string[] + "," + mu.to_string[] + "}(" + z.to_string[] + ") = " + whittaker_m.value.to_string[])
    Print("W_{" + kappa.to_string[] + "," + mu.to_string[] + "}(" + z.to_string[] + ") = " + whittaker_w.value.to_string[])
    
    Note: Connection to confluent hypergeometric
    Note: M_{κ,μ}(z) = e^(-z/2) z^(μ+1/2) ₁F₁(μ-κ+1/2; 2μ+1; z)
    Let a_equiv be mu - kappa + 0.5
    Let c_equiv be 2.0 * mu + 1.0
    
    Let hyp_equiv be Hypergeometric.compute_confluent_hypergeometric_1f1[a_equiv, c_equiv, z, config].value
    Let factor be MathOps.exp[-z/2.0] * MathOps.power[z, mu + 0.5]
    Let m_via_hyp be factor * hyp_equiv
    
    Print("Via ₁F₁: M = e^(-z/2) z^(μ+1/2) ₁F₁(μ-κ+1/2; 2μ+1; z)")
    Print("Direct M: " + whittaker_m.value.to_string[])
    Print("Via ₁F₁: " + m_via_hyp.to_string[])
    
    Return whittaker_m
```

## Generalized Hypergeometric Functions

### ₚFₑ Functions

```runa
Process called "compute_generalized_hypergeometric":
    Let config be create_hypergeometric_config[]
    
    Note: Generalized hypergeometric function ₚFₑ
    Let a_params be [1.0, 2.0, 0.5]  Note: Numerator parameters
    Let b_params be [3.0, 1.5]       Note: Denominator parameters  
    Let z be 0.3
    
    Print("Generalized hypergeometric function ₃F₂:")
    Print("Parameters a = [1, 2, 1/2], b = [3, 3/2], z = 0.3")
    
    Let result be Hypergeometric.compute_generalized_hypergeometric[a_params, b_params, z, config]
    
    Print("₃F₂(1,2,1/2; 3,3/2; 0.3) = " + result.value.to_string[])
    Print("Series coefficients (first 5):")
    For i from 0 to MathOps.minimum[4, result.series_coefficients.length - 1]:
        Print("  c_" + i.to_string[] + " = " + result.series_coefficients[i].to_string[])
    
    Note: Convergence analysis
    Print("Convergence properties:")
    Print("  p = " + a_params.length.to_string[] + " (numerator parameters)")
    Print("  q = " + b_params.length.to_string[] + " (denominator parameters)")
    If a_params.length <= b_params.length:
        Print("  Series converges for |z| < ∞ (p ≤ q)")
    Otherwise If a_params.length == b_params.length + 1:
        Print("  Series converges for |z| < 1 (p = q + 1)")
    Otherwise:
        Print("  Series has finite convergence radius (p > q + 1)")
    
    Return result
```

## Applications in Physics and Mathematics

### Quantum Mechanics Applications

```runa
Process called "hypergeometric_quantum_applications":
    Let config be create_hypergeometric_config[]
    
    Note: Hydrogen atom wavefunctions involve hypergeometric functions
    Note: Radial part: R_{n,l}(r) ∝ r^l e^(-Zr/na₀) ₁F₁(-n+l+1; 2l+2; 2Zr/na₀)
    
    Let n be 3      Note: Principal quantum number
    Let l be 1      Note: Orbital angular momentum
    Let Z be 1.0    Note: Nuclear charge
    let a0 be 1.0   Note: Bohr radius (normalized)
    Let r be 2.0    Note: Radial coordinate
    
    Print("Hydrogen atom radial wavefunction:")
    Print("n = " + n.to_string[] + ", l = " + l.to_string[])
    
    Note: Hypergeometric parameters
    Let a_hyp be -n.to_float[] + l.to_float[] + 1.0  Note: Should be negative integer for polynomial
    Let c_hyp be 2.0 * l.to_float[] + 2.0
    Let z_hyp be 2.0 * Z * r / (n.to_float[] * a0)
    
    Print("Hypergeometric arguments:")
    Print("₁F₁(" + a_hyp.to_string[] + "; " + c_hyp.to_string[] + "; " + z_hyp.to_string[] + ")")
    
    Let hyp_result be Hypergeometric.compute_confluent_hypergeometric_1f1[a_hyp, c_hyp, z_hyp, config]
    
    Note: The function should terminate as a polynomial since a < 0 is integer
    Print("Hypergeometric part: " + hyp_result.value.to_string[])
    Print("Polynomial termination: " + (a_hyp < 0.0 and MathOps.absolute[a_hyp - MathOps.round[a_hyp]] < 1e-10).to_string[])
    
    Note: Full radial function normalization and prefactors would be applied here
    Let exponential_part be MathOps.exp[-Z * r / (n.to_float[] * a0)]
    Let power_part be MathOps.power[r, l.to_float[]]
    
    Print("Exponential factor: e^(-Zr/na₀) = " + exponential_part.to_string[])
    Print("Power factor: r^l = " + power_part.to_string[])
    
    Return hyp_result
```

### Statistical Mechanics

```runa
Process called "hypergeometric_statistical_applications":
    Let config be create_hypergeometric_config[]
    
    Note: Hypergeometric functions appear in partition functions and correlation functions
    Note: Example: Ising model solutions involve elliptic integrals and hypergeometric functions
    
    Let temperature be 2.0  Note: Reduced temperature T/T_c
    Let field be 0.1        Note: External magnetic field
    
    Print("Statistical mechanics application:")
    Print("Temperature parameter: " + temperature.to_string[])
    Print("External field: " + field.to_string[])
    
    Note: Simplified example - actual Ising model solutions are more complex
    Let partition_params be compute_partition_function_parameters[temperature, field]
    
    Note: Many body correlation functions
    Let a_corr be 0.5
    Let b_corr be 1.5  
    Let c_corr be 2.0
    Let z_corr be field / temperature
    
    Let correlation_hyp be Hypergeometric.compute_hypergeometric_2f1[a_corr, b_corr, c_corr, z_corr, config]
    
    Print("Correlation function hypergeometric part:")
    Print("₂F₁(" + a_corr.to_string[] + "," + b_corr.to_string[] + ";" + c_corr.to_string[] + ";" + z_corr.to_string[] + ") = " + correlation_hyp.value.to_string[])
    
    Return correlation_hyp

Process called "compute_partition_function_parameters" that takes T as Float, H as Float returns Dictionary[String, Float]:
    Note: Compute parameters for partition function expansion
    Let params be Dictionary[String, Float]
    Set params["coupling"] to 1.0 / T
    Set params["field_coupling"] to H / T
    Return params
```

## Error Handling and Numerical Stability

```runa
Process called "demonstrate_hypergeometric_robustness":
    Let config be create_hypergeometric_config[]
    
    Try:
        Note: Test problematic cases
        Note: Pole in denominator parameter
        Let singular_case be Hypergeometric.compute_hypergeometric_2f1[1.0, 2.0, 0.0, 0.5, config]
        
    Catch error as Errors.InvalidParameters:
        Print("Singular denominator correctly handled: " + error.message)
    
    Try:
        Note: Test convergence at boundary |z| = 1
        Let boundary_case be Hypergeometric.compute_hypergeometric_2f1[1.0, 2.0, 3.0, 1.0, config]
        Print("At convergence boundary:")
        Print("₂F₁(1,2;3;1) = " + boundary_case.value.to_string[])
        Print("Method: " + boundary_case.method_used)
        
    Catch error as Errors.ConvergenceFailure:
        Print("Convergence issue at boundary: " + error.message)
    
    Note: Validate against known special cases
    Let validation_passed be validate_hypergeometric_identities[config]
    Print("Identity validation: " + validation_passed.to_string[])
    
    Return "Robustness testing completed"

Process called "validate_hypergeometric_identities" that takes config as Hypergeometric.HypergeometricConfig returns Boolean:
    Let tolerance be 1e-12
    
    Note: Test ₂F₁(a,b;c;z) = (1-z)^(-a) ₂F₁(a,c-b;c;z/(z-1)) for |z| > 1
    Let a be 0.5
    Let b be 1.5  
    Let c be 2.5
    Let z be 0.3
    
    Let direct be Hypergeometric.compute_hypergeometric_2f1[a, b, c, z, config].value
    Let identity_rhs be MathOps.power[1.0 - z, -a] * 
                       Hypergeometric.compute_hypergeometric_2f1[a, c - b, c, z/(z - 1.0), config].value
    
    Return MathOps.absolute[direct - identity_rhs] < tolerance
```

## Best Practices

### Algorithm Selection
1. **Small |z|**: Direct power series expansion
2. **Large |z|**: Apply appropriate transformations  
3. **Near poles**: Use regularized functions
4. **High precision**: Increase series terms and use extended arithmetic

### Performance Optimization  
1. **Parameter preprocessing**: Check for polynomial cases
2. **Series acceleration**: Apply convergence acceleration techniques
3. **Transformation selection**: Choose optimal transformation for convergence
4. **Caching**: Store computed series coefficients

## Integration with Other Modules

- **Special Functions**: Connections to gamma, beta, and other special functions
- **Differential Equations**: Solutions to linear ODEs with regular singular points
- **Mathematical Physics**: Quantum mechanics, statistical mechanics applications
- **Numerical Methods**: Series acceleration and analytical continuation techniques

## See Also

- [Special Functions Overview](README.md) - Module introduction and examples
- [Gamma Functions Guide](gamma.md) - Pochhammer symbols and related functions
- [Bessel Functions Guide](bessel.md) - Related cylindrical functions
- [Mathematical References](https://mathworld.wolfram.com/HypergeometricFunction.html)
- [Physics Applications](https://en.wikipedia.org/wiki/Hypergeometric_function#Physics)