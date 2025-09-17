# Orthogonal Polynomials and Classical Polynomial Systems

The **orthogonal** module provides comprehensive implementations of classical orthogonal polynomials including Legendre, Chebyshev, Hermite, Laguerre, Jacobi, and Gegenbauer polynomials. These polynomials form the foundation for numerical integration, approximation theory, and mathematical physics applications.

## Overview

Orthogonal polynomials are sequences of polynomials that satisfy orthogonality relations with respect to specific weight functions over defined intervals. This module implements all major classical orthogonal polynomial families with high precision, efficient recurrence relations, and associated quadrature rules.

## Key Features

- **Complete Classical Families**: Legendre, Chebyshev, Hermite, Laguerre, Jacobi, Gegenbauer
- **Associated Functions**: Associated Legendre polynomials for spherical harmonics
- **Quadrature Rules**: Gauss quadrature with optimal nodes and weights
- **Zeros Computation**: High-precision computation of polynomial roots
- **Recurrence Relations**: Stable three-term recurrence implementations
- **Weight Functions**: Proper handling of orthogonality weight functions

## Mathematical Foundation

### Orthogonality Relation
```
∫_{a}^{b} P_m(x) P_n(x) w(x) dx = h_n δ_{mn}
```
where w(x) is the weight function, [a,b] is the interval, and h_n is the normalization constant.

### Three-Term Recurrence
All classical orthogonal polynomials satisfy:
```
P_{n+1}(x) = (A_n x + B_n) P_n(x) - C_n P_{n-1}(x)
```

## Data Types

### Configuration Structure
```runa
Type called "OrthogonalConfig":
    precision as Float                   Note: Computational precision
    max_degree as Integer               Note: Maximum polynomial degree
    convergence_threshold as Float     Note: Convergence tolerance
    normalization_type as String       Note: "monic", "orthonormal", "standard"
    weight_function as String          Note: Associated weight function
    interval_type as String            Note: "finite", "semi_infinite", "infinite"
    quadrature_points as Integer       Note: Number of quadrature nodes
```

### Result Structure  
```runa
Type called "PolynomialResult":
    value as Float                      Note: Polynomial value at point
    derivative_values as List[Float]   Note: Derivative values if computed
    error_estimate as Float            Note: Estimation error
    degree as Integer                  Note: Polynomial degree
    normalization as String            Note: Normalization used
    weight_value as Float              Note: Weight function value
```

### Quadrature Rule
```runa
Type called "QuadratureRule":
    nodes as List[Float]               Note: Quadrature nodes
    weights as List[Float]             Note: Corresponding weights
    degree_exactness as Integer        Note: Exact integration degree
    interval as Dictionary[String, Float] Note: Integration interval
    weight_function as String         Note: Associated weight function
```

## Legendre Polynomials

### Standard Legendre Polynomials

```runa
Import "math/special/orthogonal" as Orthogonal

Process called "compute_legendre_polynomials":
    Let config be Orthogonal.OrthogonalConfig[
        precision: 15.0,
        max_degree: 20,
        convergence_threshold: 1e-14,
        normalization_type: "standard",
        weight_function: "uniform",
        interval_type: "finite",
        quadrature_points: 10
    ]
    
    Let x be 0.7
    Print("Legendre polynomials P_n(" + x.to_string[] + "):")
    
    Note: Compute first few Legendre polynomials
    For n from 0 to 6:
        Let result be Orthogonal.compute_legendre_polynomial[n, x, config]
        Print("P_" + n.to_string[] + "(" + x.to_string[] + ") = " + result.value.to_string[])
    
    Note: Verify orthogonality relation ∫₋₁¹ P_m(x) P_n(x) dx = (2/(2n+1)) δ_{mn}
    Print("Orthogonality verification:")
    Let m be 2
    Let n be 3
    
    Let orthogonality_integral be Orthogonal.compute_orthogonality_integral[
        "legendre", m, n, config
    ]
    
    Print("∫₋₁¹ P_" + m.to_string[] + "(x) P_" + n.to_string[] + "(x) dx = " + 
          orthogonality_integral.inner_product.to_string[])
    Print("Should be 0 for m ≠ n: " + (MathOps.absolute[orthogonality_integral.inner_product] < 1e-12).to_string[])
    
    Note: Test same index (should be 2/(2n+1))
    Let self_integral be Orthogonal.compute_orthogonality_integral["legendre", n, n, config]
    Let expected_norm be 2.0 / (2.0 * n.to_float[] + 1.0)
    
    Print("∫₋₁¹ P_" + n.to_string[] + "²(x) dx = " + self_integral.inner_product.to_string[])
    Print("Expected 2/(2n+1) = " + expected_norm.to_string[])
    
    Return config
```

### Associated Legendre Polynomials

```runa
Process called "compute_associated_legendre":
    Let config be create_orthogonal_config[]
    
    Note: Associated Legendre polynomials P_n^m(x) for spherical harmonics
    Let x be 0.5
    
    Print("Associated Legendre polynomials P_n^m(" + x.to_string[] + "):")
    
    Note: Compute for various (n,m) pairs
    Let test_cases be [(2,0), (2,1), (2,2), (3,0), (3,1), (3,2), (3,3)]
    
    For Each case in test_cases:
        Let n be case.0
        Let m be case.1
        
        Let result be Orthogonal.compute_associated_legendre[n, m, x, config]
        Print("P_" + n.to_string[] + "^" + m.to_string[] + "(" + x.to_string[] + ") = " + result.to_string[])
    
    Note: Verify relation to spherical harmonics
    Note: Y_l^m(θ,φ) = √[(2l+1)(l-m)!/(4π(l+m)!)] P_l^m(cos θ) e^(imφ)
    Let l be 2
    Let m be 1
    Let theta be MathOps.pi / 3.0  Note: 60 degrees
    
    Let cos_theta be MathOps.cos[theta]
    Let assoc_leg be Orthogonal.compute_associated_legendre[l, m, cos_theta, config]
    
    Note: Normalization factor for spherical harmonics
    Let factorial_lm_minus be factorial_function[l - m]
    Let factorial_lm_plus be factorial_function[l + m]
    Let norm_factor be MathOps.square_root[(2.0 * l.to_float[] + 1.0) * factorial_lm_minus / (4.0 * MathOps.pi * factorial_lm_plus)]
    
    Print("Spherical harmonic normalization:")
    Print("P_" + l.to_string[] + "^" + m.to_string[] + "(cos " + (theta * 180.0 / MathOps.pi).to_string[] + "°) = " + assoc_leg.to_string[])
    Print("Normalization factor: " + norm_factor.to_string[])
    
    Return result

Process called "factorial_function" that takes n as Integer returns Float:
    If n <= 0:
        Return 1.0
    Let result be 1.0
    For i from 1 to n:
        Set result to result * i.to_float[]
    Return result
```

## Chebyshev Polynomials  

### First and Second Kind

```runa
Process called "compute_chebyshev_polynomials":
    Let config be create_orthogonal_config[]
    
    Let x be 0.6
    Print("Chebyshev polynomials at x = " + x.to_string[] + ":")
    
    Note: First kind T_n(x) with weight (1-x²)^(-1/2) on [-1,1]  
    Print("First kind T_n(x):")
    For n from 0 to 5:
        Let result be Orthogonal.compute_chebyshev_first[n, x, config]
        Print("T_" + n.to_string[] + "(" + x.to_string[] + ") = " + result.value.to_string[])
    
    Note: Second kind U_n(x) with weight (1-x²)^(1/2) on [-1,1]
    Print("Second kind U_n(x):")
    For n from 0 to 5:
        Let result be Orthogonal.compute_chebyshev_second[n, x, config]
        Print("U_" + n.to_string[] + "(" + x.to_string[] + ") = " + result.value.to_string[])
    
    Note: Verify T_n(cos θ) = cos(nθ) identity
    Let theta be MathOps.pi / 4.0  Note: 45 degrees
    Let cos_theta be MathOps.cos[theta]
    Let n be 3
    
    Let chebyshev_val be Orthogonal.compute_chebyshev_first[n, cos_theta, config].value
    Let trigonometric_val be MathOps.cos[n.to_float[] * theta]
    
    Print("Trigonometric identity verification:")
    Print("T_" + n.to_string[] + "(cos 45°) = " + chebyshev_val.to_string[])
    Print("cos(3 × 45°) = " + trigonometric_val.to_string[])
    Print("Difference: " + MathOps.absolute[chebyshev_val - trigonometric_val].to_string[])
    
    Return result
```

## Hermite Polynomials

### Physicist's and Probabilist's Forms

```runa
Process called "compute_hermite_polynomials":
    Let config be create_orthogonal_config[]
    
    Let x be 1.2
    Print("Hermite polynomials at x = " + x.to_string[] + ":")
    
    Note: Physicist's Hermite polynomials H_n(x) with weight e^(-x²) on (-∞,∞)
    Print("Physicist's form H_n(x):")
    For n from 0 to 4:
        Let result be Orthogonal.compute_hermite_physicist[n, x, config]
        Print("H_" + n.to_string[] + "(" + x.to_string[] + ") = " + result.value.to_string[])
    
    Note: Probabilist's Hermite polynomials He_n(x) with weight e^(-x²/2)  
    Print("Probabilist's form He_n(x):")
    For n from 0 to 4:
        Let result be Orthogonal.compute_hermite_probabilist[n, x, config]
        Print("He_" + n.to_string[] + "(" + x.to_string[] + ") = " + result.value.to_string[])
    
    Note: Connection: He_n(x) = 2^(-n/2) H_n(x/√2)
    Let n be 3
    Let he_direct be Orthogonal.compute_hermite_probabilist[n, x, config].value
    Let h_scaled be Orthogonal.compute_hermite_physicist[n, x / MathOps.square_root[2.0], config].value
    Let he_from_h be MathOps.power[2.0, -n.to_float[]/2.0] * h_scaled
    
    Print("Connection formula verification:")
    Print("He_" + n.to_string[] + "(" + x.to_string[] + ") = " + he_direct.to_string[])
    Print("2^(-3/2) H_3(x/√2) = " + he_from_h.to_string[])
    Print("Difference: " + MathOps.absolute[he_direct - he_from_h].to_string[])
    
    Return result
```

## Laguerre Polynomials

### Standard and Generalized Forms

```runa  
Process called "compute_laguerre_polynomials":
    Let config be create_orthogonal_config[]
    
    Let x be 2.0
    Print("Laguerre polynomials at x = " + x.to_string[] + ":")
    
    Note: Standard Laguerre L_n(x) with weight e^(-x) on [0,∞)
    Print("Standard Laguerre L_n(x):")
    For n from 0 to 4:
        Let result be Orthogonal.compute_laguerre_standard[n, x, config]
        Print("L_" + n.to_string[] + "(" + x.to_string[] + ") = " + result.value.to_string[])
    
    Note: Associated/Generalized Laguerre L_n^(α)(x) with weight x^α e^(-x)
    Let alpha be 0.5
    Print("Associated Laguerre L_n^(1/2)(x):")
    For n from 0 to 4:
        Let result be Orthogonal.compute_laguerre_associated[n, alpha, x, config]
        Print("L_" + n.to_string[] + "^(" + alpha.to_string[] + ")(" + x.to_string[] + ") = " + result.value.to_string[])
    
    Note: Connection to quantum harmonic oscillator
    Note: ψ_n(x) ∝ e^(-x²/2) H_n(x) or in momentum space involves Laguerre polynomials
    Print("Application to quantum harmonic oscillator:")
    Print("Radial hydrogen wavefunctions use associated Laguerre polynomials")
    Print("L_n^(2l+1)(2Zr/na₀) appears in R_{n,l}(r)")
    
    Return result
```

## Jacobi Polynomials

### General Two-Parameter Family

```runa
Process called "compute_jacobi_polynomials":
    Let config be create_orthogonal_config[]
    
    Note: Jacobi polynomials P_n^(α,β)(x) with weight (1-x)^α(1+x)^β on [-1,1]
    Let alpha be 0.5
    Let beta be 1.5  
    Let x be 0.3
    
    Print("Jacobi polynomials P_n^(" + alpha.to_string[] + "," + beta.to_string[] + ")(" + x.to_string[] + "):")
    
    For n from 0 to 4:
        Let result be Orthogonal.compute_jacobi_polynomial[n, alpha, beta, x, config]
        Print("P_" + n.to_string[] + "^(" + alpha.to_string[] + "," + beta.to_string[] + ")(" + x.to_string[] + ") = " + result.value.to_string[])
    
    Note: Special cases
    Note: P_n^(0,0)(x) = P_n(x) (Legendre)
    Let legendre_via_jacobi be Orthogonal.compute_jacobi_polynomial[3, 0.0, 0.0, x, config].value
    Let legendre_direct be Orthogonal.compute_legendre_polynomial[3, x, config].value
    
    Print("Special case verification:")
    Print("P_3^(0,0)(" + x.to_string[] + ") = " + legendre_via_jacobi.to_string[])
    Print("P_3(" + x.to_string[] + ") = " + legendre_direct.to_string[])
    Print("Difference: " + MathOps.absolute[legendre_via_jacobi - legendre_direct].to_string[])
    
    Note: P_n^(-1/2,-1/2)(x) = (2/π) T_n(x) (Chebyshev first kind)
    Let chebyshev_via_jacobi be Orthogonal.compute_jacobi_polynomial[2, -0.5, -0.5, x, config].value
    Let chebyshev_direct be Orthogonal.compute_chebyshev_first[2, x, config].value
    Let expected_factor be 2.0 / MathOps.pi
    
    Print("P_2^(-1/2,-1/2)(" + x.to_string[] + ") = " + chebyshev_via_jacobi.to_string[])
    Print("(2/π) T_2(" + x.to_string[] + ") = " + (expected_factor * chebyshev_direct).to_string[])
    
    Return result
```

## Gauss Quadrature Rules

### High-Precision Integration

```runa
Process called "demonstrate_gauss_quadrature":
    Let config be create_orthogonal_config[]
    
    Note: Generate Gauss-Legendre quadrature rule
    Let n_points be 5
    Let legendre_quadrature be Orthogonal.compute_gauss_legendre_quadrature[n_points, config]
    
    Print("Gauss-Legendre quadrature with " + n_points.to_string[] + " points:")
    Print("Nodes and weights:")
    For i from 0 to n_points - 1:
        Print("  x_" + i.to_string[] + " = " + legendre_quadrature.nodes[i].to_string[])
        Print("  w_" + i.to_string[] + " = " + legendre_quadrature.weights[i].to_string[])
    
    Print("Exact for polynomials up to degree: " + legendre_quadrature.degree_exactness.to_string[])
    
    Note: Test integration accuracy
    Process called "test_function" that takes x as Float returns Float:
        Return x * x * x + 2.0 * x * x - x + 3.0  Note: Cubic polynomial
    
    Note: Exact integral of x³ + 2x² - x + 3 from -1 to 1
    Let exact_integral be (1.0/4.0 + 2.0/3.0 + 3.0) - (-1.0/4.0 + 2.0/3.0 + 1.0 + 3.0)
    Let exact_result be 2.0/3.0 * 2.0 + 6.0  Note: Simplifies to 22/3
    Set exact_result to 22.0/3.0
    
    Note: Numerical integration using quadrature
    Let numerical_result be 0.0
    For i from 0 to n_points - 1:
        Let x_i be legendre_quadrature.nodes[i]
        Let w_i be legendre_quadrature.weights[i]
        Let f_xi be test_function[x_i]
        Set numerical_result to numerical_result + w_i * f_xi
    
    Print("Integration test:")
    Print("∫₋₁¹ (x³ + 2x² - x + 3) dx")
    Print("Exact result: " + exact_result.to_string[])
    Print("Quadrature result: " + numerical_result.to_string[])
    Print("Error: " + MathOps.absolute[exact_result - numerical_result].to_string[])
    
    Note: Test Gauss-Hermite quadrature for infinite interval
    Let hermite_quadrature be Orthogonal.compute_gauss_hermite_quadrature[n_points, config]
    
    Print("Gauss-Hermite quadrature nodes (first 3):")
    For i from 0 to MathOps.minimum[2, n_points - 1]:
        Print("  x_" + i.to_string[] + " = " + hermite_quadrature.nodes[i].to_string[])
        Print("  w_" + i.to_string[] + " = " + hermite_quadrature.weights[i].to_string[])
    
    Return legendre_quadrature
```

## Applications in Mathematical Physics

### Spherical Harmonics

```runa
Process called "spherical_harmonics_application":
    Let config be create_orthogonal_config[]
    
    Note: Spherical harmonics Y_l^m(θ,φ) = N_l^m P_l^|m|(cos θ) e^(imφ)
    Let l be 2  Note: Angular momentum quantum number
    Let m be 1  Note: Magnetic quantum number
    Let theta be MathOps.pi / 3.0  Note: Polar angle (60°)
    Let phi be MathOps.pi / 4.0    Note: Azimuthal angle (45°)
    
    Print("Spherical harmonics Y_" + l.to_string[] + "^" + m.to_string[] + "(θ,φ):")
    Print("θ = " + (theta * 180.0 / MathOps.pi).to_string[] + "°, φ = " + (phi * 180.0 / MathOps.pi).to_string[] + "°")
    
    Note: Compute associated Legendre polynomial part
    Let cos_theta be MathOps.cos[theta]
    Let assoc_legendre be Orthogonal.compute_associated_legendre[l, MathOps.absolute[m], cos_theta, config]
    
    Note: Normalization constant N_l^m = √[(2l+1)(l-|m|)!/(4π(l+|m|)!)]
    Let l_minus_m_factorial be factorial_function[l - MathOps.absolute[m]]
    Let l_plus_m_factorial be factorial_function[l + MathOps.absolute[m]]
    Let normalization be MathOps.square_root[
        (2.0 * l.to_float[] + 1.0) * l_minus_m_factorial / (4.0 * MathOps.pi * l_plus_m_factorial)
    ]
    
    Note: Complex exponential part
    Let complex_real be MathOps.cos[m.to_float[] * phi]
    Let complex_imag be MathOps.sin[m.to_float[] * phi]
    
    Print("Components:")
    Print("P_" + l.to_string[] + "^" + MathOps.absolute[m].to_string[] + "(cos θ) = " + assoc_legendre.to_string[])
    Print("Normalization N_" + l.to_string[] + "^" + m.to_string[] + " = " + normalization.to_string[])
    Print("e^(imφ) = " + complex_real.to_string[] + " + " + complex_imag.to_string[] + "i")
    
    Let ylm_real be normalization * assoc_legendre * complex_real
    Let ylm_imag be normalization * assoc_legendre * complex_imag
    
    Print("Y_" + l.to_string[] + "^" + m.to_string[] + "(θ,φ) = " + ylm_real.to_string[] + " + " + ylm_imag.to_string[] + "i")
    
    Return normalization
```

### Quantum Harmonic Oscillator

```runa
Process called "quantum_oscillator_wavefunctions":
    Let config be create_orthogonal_config[]
    
    Note: Quantum harmonic oscillator wavefunctions ψ_n(x) = N_n e^(-x²/2) H_n(x)
    Let n be 3  Note: Quantum number
    Let x be 1.0  Note: Position
    
    Print("Quantum harmonic oscillator wavefunction ψ_" + n.to_string[] + "(x):")
    
    Note: Hermite polynomial part
    Let hermite_val be Orthogonal.compute_hermite_physicist[n, x, config].value
    
    Note: Gaussian envelope
    Let gaussian be MathOps.exp[-x * x / 2.0]
    
    Note: Normalization N_n = (mω/πℏ)^(1/4) / √(2^n n!)
    Let factorial_n be factorial_function[n]
    Let power_2_n be MathOps.power[2.0, n.to_float[]]
    Let normalization be 1.0 / MathOps.square_root[power_2_n * factorial_n * MathOps.square_root[MathOps.pi]]
    
    Let wavefunction be normalization * gaussian * hermite_val
    
    Print("Components at x = " + x.to_string[] + ":")
    Print("H_" + n.to_string[] + "(" + x.to_string[] + ") = " + hermite_val.to_string[])
    Print("e^(-x²/2) = " + gaussian.to_string[])
    Print("N_" + n.to_string[] + " = " + normalization.to_string[])
    Print("ψ_" + n.to_string[] + "(" + x.to_string[] + ") = " + wavefunction.to_string[])
    
    Note: Verify normalization by integration (conceptual)
    Print("Wavefunction normalization requires:")
    Print("∫_{-∞}^{∞} |ψ_n(x)|² dx = 1")
    Print("This uses Hermite orthogonality with Gaussian weight")
    
    Return wavefunction
```

## Best Practices

### Computational Guidelines
1. **Recurrence Relations**: Use three-term recurrence for stability
2. **Domain Validation**: Check arguments are within valid intervals
3. **Normalization**: Choose appropriate normalization for application
4. **High Degrees**: Use asymptotic approximations for large n

### Performance Optimization
1. **Caching**: Store computed polynomial values for repeated use
2. **Vectorization**: Compute multiple polynomial values simultaneously  
3. **Precision Scaling**: Match precision to accuracy requirements
4. **Method Selection**: Choose optimal algorithm based on degree and domain

## Integration with Other Modules

- **Numerical Integration**: Gauss quadrature rules for high-precision integration
- **Special Functions**: Connections to hypergeometric and other special functions
- **Linear Algebra**: Matrix representations and eigenvalue problems
- **Physics Applications**: Quantum mechanics, classical mechanics, electromagnetic theory

## See Also

- [Special Functions Overview](README.md) - Module introduction and examples  
- [Hypergeometric Functions Guide](hypergeometric.md) - Connections to hypergeometric theory
- [Numerical Integration Documentation](../engine/numerical/README.md) - Quadrature methods
- [Physics Applications](https://mathworld.wolfram.com/OrthogonalPolynomial.html)
- [Approximation Theory](https://en.wikipedia.org/wiki/Orthogonal_polynomials)