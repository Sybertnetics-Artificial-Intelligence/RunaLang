# Bessel Functions and Cylindrical Functions

The **bessel** module provides comprehensive implementations of Bessel functions of all kinds, modified Bessel functions, spherical Bessel functions, Airy functions, and Hankel functions. These functions are fundamental solutions to cylindrical wave equations and appear throughout physics and engineering.

## Overview

Bessel functions are solutions to Bessel's differential equation, which arises when solving the wave equation in cylindrical coordinates. This module implements all standard types of Bessel functions with high precision and multiple computational methods optimized for different parameter ranges.

## Key Features

- **Complete Bessel Function Family**: First and second kind, modified, spherical variants
- **Airy Functions**: Solutions to Airy's differential equation  
- **Hankel Functions**: Complex linear combinations of Bessel functions
- **Zeros Computation**: Accurate computation of Bessel function zeros
- **Multiple Algorithms**: Series, asymptotic, recurrence, and integral methods
- **High Precision**: Arbitrary precision arithmetic with error bounds

## Mathematical Foundation

### Bessel's Differential Equation
```
x² d²y/dx² + x dy/dx + (x² - ν²)y = 0
```

**Solutions:**
- **First Kind**: J_ν(x) - finite at x = 0
- **Second Kind**: Y_ν(x) - singular at x = 0  
- **Modified First Kind**: I_ν(x) for modified equation
- **Modified Second Kind**: K_ν(x) for modified equation

### Series Representations

**Bessel Function of First Kind:**
```
J_ν(x) = (x/2)^ν Σ_{k=0}^∞ (-1)^k (x²/4)^k / (k! Γ(ν+k+1))
```

**Modified Bessel Function:**
```
I_ν(x) = (x/2)^ν Σ_{k=0}^∞ (x²/4)^k / (k! Γ(ν+k+1))
```

### Asymptotic Expansions
For large |x|:
```
J_ν(x) ~ √(2/πx) cos(x - νπ/2 - π/4) + O(x^(-3/2))
Y_ν(x) ~ √(2/πx) sin(x - νπ/2 - π/4) + O(x^(-3/2))
```

## Data Types

### Configuration Structure

```runa
Type called "BesselConfig":
    precision as Float                   Note: Computational precision
    max_iterations as Integer            Note: Maximum iteration count
    convergence_threshold as Float       Note: Series convergence tolerance
    series_method as String             Note: "power_series", "recurrence"
    asymptotic_threshold as Float       Note: Switch to asymptotic methods
    recurrence_direction as String      Note: "forward", "backward", "miller"
    scaling_factor as Float             Note: Prevent overflow in recurrence
```

### Result Structure

```runa
Type called "BesselResult":
    value as Float                      Note: Function value
    error_estimate as Float             Note: Estimated computation error
    iterations_used as Integer          Note: Iterations for convergence
    method_used as String              Note: Algorithm used
    convergence_status as String       Note: Convergence information
    derivative_values as List[Float]   Note: Derivative values if computed
```

### Zeros Data Structure

```runa
Type called "BesselZeros":
    function_type as String             Note: "bessel_j", "bessel_y", etc.
    order as Float                      Note: Order ν of Bessel function
    zeros_list as List[Float]          Note: List of computed zeros
    accuracy as Float                  Note: Accuracy of zero computation
    computation_method as String       Note: Method used for zeros
```

### Asymptotic Expansion Structure

```runa
Type called "AsymptoticExpansion":
    leading_term as Float              Note: Principal asymptotic term
    correction_terms as List[Float]    Note: Higher-order corrections
    expansion_order as Integer         Note: Number of terms computed
    validity_range as Dictionary[String, Float]  Note: Range of validity
```

## Bessel Functions of the First Kind (J_ν)

### Basic Bessel J Functions

```runa
Import "math/special/bessel" as Bessel

Process called "compute_basic_bessel_j":
    Let config be Bessel.BesselConfig[
        precision: 15.0,
        max_iterations: 100,
        convergence_threshold: 1e-14,
        series_method: "power_series",
        asymptotic_threshold: 10.0,
        recurrence_direction: "forward",
        scaling_factor: 1.0
    ]
    
    Note: Integer order Bessel functions
    Let j0_1 be Bessel.compute_bessel_j[0.0, 1.0, config]
    Print("J₀(1) = " + j0_1.value.to_string[] + " ≈ 0.7651976865...")
    Print("Method: " + j0_1.method_used + ", Error: " + j0_1.error_estimate.to_string[])
    
    Let j1_1 be Bessel.compute_bessel_j[1.0, 1.0, config]
    Print("J₁(1) = " + j1_1.value.to_string[] + " ≈ 0.4400505857...")
    
    Let j2_1 be Bessel.compute_bessel_j[2.0, 1.0, config]
    Print("J₂(1) = " + j2_1.value.to_string[] + " ≈ 0.1149034849...")
    
    Note: Non-integer order Bessel functions
    Let j_half_2 be Bessel.compute_bessel_j[0.5, 2.0, config]
    Print("J_{1/2}(2) = " + j_half_2.value.to_string[])
    
    Note: Verify recurrence relation: J_{ν-1}(x) + J_{ν+1}(x) = (2ν/x)J_ν(x)
    Let nu be 1.0
    Let x be 2.0
    Let j0_2 be Bessel.compute_bessel_j[0.0, x, config].value
    Let j1_2 be Bessel.compute_bessel_j[1.0, x, config].value
    Let j2_2 be Bessel.compute_bessel_j[2.0, x, config].value
    
    Let left_side be j0_2 + j2_2
    Let right_side be (2.0 * nu / x) * j1_2
    
    Print("Recurrence check: J₀(2) + J₂(2) = " + left_side.to_string[])
    Print("                  (2×1/2)J₁(2) = " + right_side.to_string[])
    Print("Difference: " + MathOps.absolute[left_side - right_side].to_string[])
    
    Return config
```

### Derivatives and Special Values

```runa
Process called "compute_bessel_derivatives":
    Let config be create_bessel_config[]
    
    Note: Derivatives using recurrence relations
    Let x be 3.0
    For nu from 0.0 to 3.0 by 0.5:
        Let derivative be Bessel.compute_bessel_j_derivative[nu, x, config]
        Print("J'_{" + nu.to_string[] + "}(" + x.to_string[] + ") = " + derivative.to_string[])
    
    Note: Special case: J'₀(x) = -J₁(x)
    let j0_prime be Bessel.compute_bessel_j_derivative[0.0, x, config]
    let j1_value be Bessel.compute_bessel_j[1.0, x, config].value
    
    Print("J'₀(3) = " + j0_prime.to_string[])
    Print("-J₁(3) = " + (-j1_value).to_string[])
    Print("Difference: " + MathOps.absolute[j0_prime + j1_value].to_string[])
    
    Note: Connection to spherical Bessel functions
    Note: j_n(x) = √(π/2x) J_{n+1/2}(x)
    Let n be 1
    Let spherical_j1 be Bessel.compute_spherical_bessel_j[n, x, config]
    Let cylindrical_equivalent be MathOps.square_root[MathOps.pi / (2.0 * x)] * 
                                 Bessel.compute_bessel_j[n.to_float[] + 0.5, x, config].value
    
    Print("j₁(3) = " + spherical_j1.value.to_string[])
    Print("√(π/6) J_{3/2}(3) = " + cylindrical_equivalent.to_string[])
    
    Return derivative
```

## Bessel Functions of the Second Kind (Y_ν)

### Neumann Functions

```runa
Process called "compute_bessel_y_functions":
    Let config be create_bessel_config[]
    
    Note: Bessel functions of second kind (Neumann functions)
    Let x be 2.0
    
    Let y0_2 be Bessel.compute_bessel_y[0.0, x, config]
    Print("Y₀(2) = " + y0_2.value.to_string[] + " ≈ 0.5103756726...")
    Print("Method: " + y0_2.method_used)
    
    Let y1_2 be Bessel.compute_bessel_y[1.0, x, config]
    Print("Y₁(2) = " + y1_2.value.to_string[] + " ≈ -0.1070324315...")
    
    Note: Non-integer order
    Let y_half_2 be Bessel.compute_bessel_y[0.5, x, config]
    Print("Y_{1/2}(2) = " + y_half_2.value.to_string[])
    
    Note: Verify Wronskian: J_ν(x)Y'_ν(x) - J'_ν(x)Y_ν(x) = 2/(πx)
    Let nu be 1.0
    Let j_nu be Bessel.compute_bessel_j[nu, x, config].value
    Let y_nu be Bessel.compute_bessel_y[nu, x, config].value
    Let j_prime_nu be Bessel.compute_bessel_j_derivative[nu, x, config]
    Let y_prime_nu be Bessel.compute_bessel_y_derivative[nu, x, config]
    
    Let wronskian be j_nu * y_prime_nu - j_prime_nu * y_nu
    Let expected_wronskian be 2.0 / (MathOps.pi * x)
    
    Print("Wronskian = " + wronskian.to_string[])
    Print("Expected = 2/(πx) = " + expected_wronskian.to_string[])
    Print("Difference: " + MathOps.absolute[wronskian - expected_wronskian].to_string[])
    
    Return y0_2
```

## Modified Bessel Functions

### Modified Bessel Functions of First Kind (I_ν)

```runa
Process called "compute_modified_bessel_i":
    Let config be create_bessel_config[]
    
    Note: Modified Bessel functions I_ν(x) - exponentially growing
    Let x be 1.5
    
    Let i0_x be Bessel.compute_modified_bessel_i[0.0, x, config]
    Print("I₀(1.5) = " + i0_x.value.to_string[] + " ≈ 1.6467232021...")
    
    Let i1_x be Bessel.compute_modified_bessel_i[1.0, x, config]  
    Print("I₁(1.5) = " + i1_x.value.to_string[] + " ≈ 0.9816664306...")
    
    Note: Verify modified recurrence: I_{ν-1}(x) - I_{ν+1}(x) = (2ν/x)I_ν(x)
    Let nu be 1.0
    let i0_x_val be i0_x.value
    let i1_x_val be i1_x.value
    let i2_x be Bessel.compute_modified_bessel_i[2.0, x, config].value
    
    let left_side be i0_x_val - i2_x
    let right_side be (2.0 * nu / x) * i1_x_val
    
    Print("Modified recurrence check:")
    Print("I₀(1.5) - I₂(1.5) = " + left_side.to_string[])
    Print("(2×1/1.5)I₁(1.5) = " + right_side.to_string[])
    Print("Difference: " + MathOps.absolute[left_side - right_side].to_string[])
    
    Note: Exponential scaling for large arguments
    Let large_x be 10.0
    Let i0_large be Bessel.compute_modified_bessel_i[0.0, large_x, config]
    Let scaled_i0 be Bessel.compute_scaled_modified_bessel_i[0.0, large_x, config]
    
    Print("I₀(10) = " + i0_large.value.to_string[] + " (large value)")
    Print("e^(-10) I₀(10) = " + scaled_i0.value.to_string[] + " (scaled)")
    
    Return i0_x
```

### Modified Bessel Functions of Second Kind (K_ν)

```runa
Process called "compute_modified_bessel_k":
    Let config be create_bessel_config[]
    
    Note: Modified Bessel functions K_ν(x) - exponentially decaying
    Let x be 2.0
    
    Let k0_x be Bessel.compute_modified_bessel_k[0.0, x, config]
    Print("K₀(2) = " + k0_x.value.to_string[] + " ≈ 0.1138938727...")
    
    Let k1_x be Bessel.compute_modified_bessel_k[1.0, x, config]
    Print("K₁(2) = " + k1_x.value.to_string[] + " ≈ 0.1398658818...")
    
    Note: Verify K_{-ν}(x) = K_ν(x) symmetry
    Let k_neg_half be Bessel.compute_modified_bessel_k[-0.5, x, config]
    Let k_pos_half be Bessel.compute_modified_bessel_k[0.5, x, config]
    
    Print("K_{-1/2}(2) = " + k_neg_half.value.to_string[])
    Print("K_{1/2}(2) = " + k_pos_half.value.to_string[])
    Print("Symmetry check difference: " + MathOps.absolute[k_neg_half.value - k_pos_half.value].to_string[])
    
    Note: Connection to exponential integral
    Note: K₀(x) = -ln(x/2)I₀(x) - γI₀(x) + higher order terms for small x
    Let small_x be 0.1
    Let k0_small be Bessel.compute_modified_bessel_k[0.0, small_x, config]
    Print("K₀(0.1) = " + k0_small.value.to_string[] + " (should be large for small x)")
    
    Return k0_x
```

## Spherical Bessel Functions

### Spherical Functions j_n and y_n

```runa
Process called "compute_spherical_bessel":
    Let config be create_bessel_config[]
    
    Note: Spherical Bessel functions j_n(x) and y_n(x)
    Let x be 5.0
    
    Note: First few orders
    For n from 0 to 4:
        Let j_n be Bessel.compute_spherical_bessel_j[n, x, config]
        Let y_n be Bessel.compute_spherical_bessel_y[n, x, config]
        
        Print("j_" + n.to_string[] + "(" + x.to_string[] + ") = " + j_n.value.to_string[])
        Print("y_" + n.to_string[] + "(" + x.to_string[] + ") = " + y_n.value.to_string[])
    
    Note: Verify connection to elementary functions for low orders
    Note: j₀(x) = sin(x)/x, y₀(x) = -cos(x)/x
    Let j0_direct be MathOps.sin[x] / x
    Let y0_direct be -MathOps.cos[x] / x
    
    let j0_computed be Bessel.compute_spherical_bessel_j[0, x, config].value
    let y0_computed be Bessel.compute_spherical_bessel_y[0, x, config].value
    
    Print("j₀(5) direct: sin(5)/5 = " + j0_direct.to_string[])
    Print("j₀(5) computed = " + j0_computed.to_string[])
    Print("Difference: " + MathOps.absolute[j0_direct - j0_computed].to_string[])
    
    Print("y₀(5) direct: -cos(5)/5 = " + y0_direct.to_string[])
    Print("y₀(5) computed = " + y0_computed.to_string[])
    Print("Difference: " + MathOps.absolute[y0_direct - y0_computed].to_string[])
    
    Note: j₁(x) = (sin(x) - x cos(x))/x², y₁(x) = -(cos(x) + x sin(x))/x²
    Let sin_x be MathOps.sin[x]
    Let cos_x be MathOps.cos[x]
    Let j1_direct be (sin_x - x * cos_x) / (x * x)
    Let y1_direct be -(cos_x + x * sin_x) / (x * x)
    
    Let j1_computed be Bessel.compute_spherical_bessel_j[1, x, config].value
    Let y1_computed be Bessel.compute_spherical_bessel_y[1, x, config].value
    
    Print("j₁(5) verification difference: " + MathOps.absolute[j1_direct - j1_computed].to_string[])
    Print("y₁(5) verification difference: " + MathOps.absolute[y1_direct - y1_computed].to_string[])
    
    Return j0_computed
```

## Airy Functions

### Airy Ai and Bi Functions

```runa
Process called "compute_airy_functions":
    Let config be create_bessel_config[]
    
    Note: Airy functions Ai(x) and Bi(x) - solutions to Airy equation y'' - xy = 0
    
    Note: Evaluate at various points
    For Each x in [-2.0, -1.0, 0.0, 1.0, 2.0]:
        Let ai_x be Bessel.compute_airy_ai[x, config]
        Let bi_x be Bessel.compute_airy_bi[x, config]
        
        Print("Ai(" + x.to_string[] + ") = " + ai_x.value.to_string[])
        Print("Bi(" + x.to_string[] + ") = " + bi_x.value.to_string[])
    
    Note: Special values
    Note: Ai(0) = 1/(3^(2/3) Γ(2/3)) ≈ 0.355028053887817
    Let ai_0 be Bessel.compute_airy_ai[0.0, config]
    Print("Ai(0) = " + ai_0.value.to_string[] + " ≈ 0.355028053887817")
    
    Note: Derivatives
    Let x_eval be 1.0
    Let ai_prime be Bessel.compute_airy_ai_derivative[x_eval, config]
    Let bi_prime be Bessel.compute_airy_bi_derivative[x_eval, config]
    
    Print("Ai'(1) = " + ai_prime.to_string[])
    Print("Bi'(1) = " + bi_prime.to_string[])
    
    Note: Wronskian: Ai(x)Bi'(x) - Ai'(x)Bi(x) = 1/π
    Let ai_val be Bessel.compute_airy_ai[x_eval, config].value
    Let bi_val be Bessel.compute_airy_bi[x_eval, config].value
    
    let wronskian be ai_val * bi_prime - ai_prime * bi_val
    let expected be 1.0 / MathOps.pi
    
    Print("Airy Wronskian = " + wronskian.to_string[])
    Print("Expected = 1/π = " + expected.to_string[])
    Print("Difference: " + MathOps.absolute[wronskian - expected].to_string[])
    
    Return ai_0
```

## Hankel Functions and Complex Analysis

### Hankel Functions H^(1) and H^(2)

```runa
Process called "compute_hankel_functions":
    Let config be create_bessel_config[]
    
    Note: Hankel functions H^(1)_ν(x) = J_ν(x) + i Y_ν(x)
    Note: Hankel functions H^(2)_ν(x) = J_ν(x) - i Y_ν(x)
    
    Let nu be 0.0
    Let x be 3.0
    
    Let hankel1 be Bessel.compute_hankel_function_first[nu, x, config]
    Let hankel2 be Bessel.compute_hankel_function_second[nu, x, config]
    
    Print("H^(1)₀(3) = " + hankel1.real_part.to_string[] + " + " + 
          hankel1.imaginary_part.to_string[] + "i")
    Print("H^(2)₀(3) = " + hankel2.real_part.to_string[] + " + " + 
          hankel2.imaginary_part.to_string[] + "i")
    
    Note: Verify relationships with J and Y
    Let j0_3 be Bessel.compute_bessel_j[nu, x, config].value
    Let y0_3 be Bessel.compute_bessel_y[nu, x, config].value
    
    Print("J₀(3) = " + j0_3.to_string[])
    Print("Y₀(3) = " + y0_3.to_string[])
    Print("H^(1) real part verification: " + MathOps.absolute[hankel1.real_part - j0_3].to_string[])
    Print("H^(1) imag part verification: " + MathOps.absolute[hankel1.imaginary_part - y0_3].to_string[])
    
    Note: Asymptotic behavior for large |x|
    Note: H^(1)_ν(x) ~ √(2/πx) e^(i(x - νπ/2 - π/4))
    Let large_x be 20.0
    Let hankel1_large be Bessel.compute_hankel_function_first[nu, large_x, config]
    
    Let asymptotic_magnitude be MathOps.square_root[2.0 / (MathOps.pi * large_x)]
    let phase be large_x - nu * MathOps.pi / 2.0 - MathOps.pi / 4.0
    let asymptotic_real be asymptotic_magnitude * MathOps.cos[phase]
    let asymptotic_imag be asymptotic_magnitude * MathOps.sin[phase]
    
    Print("H^(1)₀(20) computed: " + hankel1_large.real_part.to_string[] + " + " + 
          hankel1_large.imaginary_part.to_string[] + "i")
    Print("H^(1)₀(20) asymptotic: " + asymptotic_real.to_string[] + " + " + 
          asymptotic_imag.to_string[] + "i")
    
    Return hankel1
```

## Zeros of Bessel Functions

### Computing Bessel Function Zeros

```runa
Process called "compute_bessel_zeros":
    Let config be create_bessel_config[]
    
    Note: Zeros of J₀(x)
    Let j0_zeros be Bessel.compute_bessel_j_zeros[0.0, 10, config]
    Print("First 10 zeros of J₀(x):")
    For i from 0 to j0_zeros.zeros_list.length - 1:
        Print("  α₀," + (i+1).to_string[] + " = " + j0_zeros.zeros_list[i].to_string[])
    
    Note: Verify these are actually zeros
    Print("Verification (values should be ≈ 0):")
    For i from 0 to 4:  Note: Check first 5 zeros
        Let zero_value be j0_zeros.zeros_list[i]
        Let function_at_zero be Bessel.compute_bessel_j[0.0, zero_value, config]
        Print("  J₀(" + zero_value.to_string[] + ") = " + function_at_zero.value.to_string[])
    
    Note: Zeros of J₁(x)
    Let j1_zeros be Bessel.compute_bessel_j_zeros[1.0, 5, config]
    Print("First 5 zeros of J₁(x):")
    For i from 0 to j1_zeros.zeros_list.length - 1:
        Print("  α₁," + (i+1).to_string[] + " = " + j1_zeros.zeros_list[i].to_string[])
    
    Note: Zeros of Y₀(x)
    Let y0_zeros be Bessel.compute_bessel_y_zeros[0.0, 5, config]
    Print("First 5 zeros of Y₀(x):")
    For i from 0 to y0_zeros.zeros_list.length - 1:
        Print("  β₀," + (i+1).to_string[] + " = " + y0_zeros.zeros_list[i].to_string[])
    
    Note: Asymptotic approximation for large zeros
    Note: For large k: α₀,k ≈ (k - 1/4)π
    Let k be 10
    Let asymptotic_zero be (k.to_float[] - 0.25) * MathOps.pi
    Let actual_zero be j0_zeros.zeros_list[k-1]
    Print("α₀," + k.to_string[] + " asymptotic: " + asymptotic_zero.to_string[])
    Print("α₀," + k.to_string[] + " computed: " + actual_zero.to_string[])
    Print("Relative error: " + MathOps.absolute[(actual_zero - asymptotic_zero) / actual_zero].to_string[])
    
    Return j0_zeros
```

## Applications in Physics and Engineering

### Vibrating Membrane (Drum Head)

```runa
Process called "drum_vibration_modes":
    Let config be create_bessel_config[]
    
    Note: Normal modes of circular membrane fixed at boundary
    Note: Solution: u(r,θ,t) = J_m(α_{m,n} r/a) [A cos(mθ) + B sin(mθ)] cos(ω_{m,n} t)
    Note: Boundary condition: J_m(α_{m,n}) = 0
    
    Let drum_radius be 1.0  Note: Normalized radius
    
    Note: Fundamental mode (0,1): m=0, first zero of J₀
    Let j0_zeros be Bessel.compute_bessel_j_zeros[0.0, 3, config]
    Let alpha_01 be j0_zeros.zeros_list[0]
    
    Print("Drum vibration analysis:")
    Print("Fundamental mode (0,1): α₀,₁ = " + alpha_01.to_string[])
    
    Note: Evaluate mode shape at various radii
    Print("Mode shape J₀(α₀,₁ r/a) for fundamental mode:")
    For Each r in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
        Let scaled_arg be alpha_01 * r / drum_radius
        If r == 1.0:  Note: At boundary, should be zero
            Print("  r = " + r.to_string[] + ": J₀(" + scaled_arg.to_string[] + ") = 0 (boundary condition)")
        Otherwise:
            Let mode_amplitude be Bessel.compute_bessel_j[0.0, scaled_arg, config].value
            Print("  r = " + r.to_string[] + ": J₀(" + scaled_arg.to_string[] + ") = " + mode_amplitude.to_string[])
    
    Note: Higher modes
    Let alpha_02 be j0_zeros.zeros_list[1]  Note: (0,2) mode
    Let j1_zeros be Bessel.compute_bessel_j_zeros[1.0, 2, config]
    Let alpha_11 be j1_zeros.zeros_list[0]  Note: (1,1) mode
    
    Print("Higher modes:")
    Print("  (0,2) mode: α₀,₂ = " + alpha_02.to_string[])
    Print("  (1,1) mode: α₁,₁ = " + alpha_11.to_string[])
    
    Note: Frequency ratios (proportional to α_{m,n})
    Print("Frequency ratios relative to fundamental:")
    Print("  f₀,₂/f₀,₁ = " + (alpha_02/alpha_01).to_string[])
    Print("  f₁,₁/f₀,₁ = " + (alpha_11/alpha_01).to_string[])
    
    Return alpha_01
```

### Heat Conduction in Cylinder

```runa
Process called "cylindrical_heat_conduction":
    Let config be create_bessel_config[]
    
    Note: Heat equation in cylinder with insulated boundary
    Note: ∂u/∂t = α ∇²u with ∂u/∂r|_{r=a} = 0
    Note: Solution: u(r,t) = Σ A_n J₀(β_n r/a) exp(-α β_n² t/a²)
    Note: β_n are zeros of J₁ (derivative boundary condition)
    
    Let j1_zeros be Bessel.compute_bessel_j_zeros[1.0, 5, config]
    
    Print("Heat conduction in cylinder with insulated boundary:")
    Print("Eigenvalues β_n (zeros of J₁):")
    For i from 0 to 4:
        Print("  β_" + (i+1).to_string[] + " = " + j1_zeros.zeros_list[i].to_string[])
    
    Note: Time evolution for first few modes
    Let thermal_diffusivity be 1.0
    Let cylinder_radius be 1.0
    Let time be 0.1
    
    Print("Decay factors exp(-α β_n² t/a²) at t = 0.1:")
    For i from 0 to 4:
        Let beta_n be j1_zeros.zeros_list[i]
        Let decay_factor be MathOps.exp[
            -thermal_diffusivity * beta_n * beta_n * time / (cylinder_radius * cylinder_radius)
        ]
        Print("  Mode " + (i+1).to_string[] + ": " + decay_factor.to_string[])
    
    Note: Spatial distribution of first mode
    Let beta_1 be j1_zeros.zeros_list[0]
    Print("First mode spatial distribution J₀(β₁ r/a):")
    For Each r in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
        Let arg be beta_1 * r / cylinder_radius
        Let amplitude be Bessel.compute_bessel_j[0.0, arg, config].value
        Print("  r = " + r.to_string[] + ": " + amplitude.to_string[])
    
    Return j1_zeros
```

## Error Handling and Numerical Stability

### Robustness and Validation

```runa
Process called "demonstrate_bessel_error_handling":
    Let config be create_bessel_config[]
    
    Try:
        Note: Test with extreme parameters
        Let large_order be 100.0
        Let small_arg be 0.001
        
        Let result be Bessel.compute_bessel_j[large_order, small_arg, config]
        Print("J_100(0.001) = " + result.value.to_string[])
        Print("Method used: " + result.method_used)
        Print("Convergence: " + result.convergence_status)
        
        If result.convergence_status != "converged":
            Print("Warning: Potential accuracy issues")
    
    Catch error as Errors.ConvergenceFailure:
        Print("Convergence failed: " + error.message)
        Print("Consider increasing precision or max_iterations")
    
    Try:
        Note: Test overflow protection
        Let moderate_order be 5.0
        Let large_arg be 50.0
        
        Note: Use scaled functions to avoid overflow
        Let scaled_result be Bessel.compute_scaled_modified_bessel_i[moderate_order, large_arg, config]
        Print("e^(-50) I₅(50) = " + scaled_result.value.to_string[])
        
    Catch error as Errors.NumericalOverflow:
        Print("Overflow detected: " + error.message)
        Print("Using scaled functions recommended")
    
    Try:
        Note: Test argument validation
        Let negative_arg be -1.0
        Let bessel_result be Bessel.compute_modified_bessel_k[0.0, negative_arg, config]
        
    Catch error as Errors.InvalidDomain:
        Print("Domain error correctly caught: " + error.message)
        Print("Modified Bessel K functions require x > 0")
    
    Note: Validate using known relationships
    Let validation_passed be validate_bessel_identities[config]
    If validation_passed:
        Print("All Bessel function identities validated successfully")
    Otherwise:
        Print("Warning: Some validation checks failed")
    
    Return "Error handling demonstrated"

Process called "validate_bessel_identities" that takes config as Bessel.BesselConfig returns Boolean:
    Note: Test various mathematical identities
    Let tolerance be 1e-12
    let all_passed be true
    
    Note: Test J_{-n}(x) = (-1)^n J_n(x) for integer n
    Let x be 2.5
    Let n be 3
    Let j_neg_n be Bessel.compute_bessel_j[-n.to_float[], x, config].value
    Let j_pos_n be Bessel.compute_bessel_j[n.to_float[], x, config].value
    Let expected be MathOps.power[-1.0, n.to_float[]] * j_pos_n
    
    If MathOps.absolute[j_neg_n - expected] > tolerance:
        Let all_passed be false
    
    Note: Test addition formula (simplified case)
    Note: More comprehensive tests would be added here
    
    Return all_passed
```

## Best Practices

### Algorithm Selection Guidelines

1. **Small Arguments**: Use power series expansions
2. **Large Arguments**: Use asymptotic expansions  
3. **Intermediate Arguments**: Use recurrence relations or continued fractions
4. **High Order**: Use Miller's algorithm for backward recurrence
5. **Modified Functions**: Use scaled versions to prevent overflow

### Performance Optimization

1. **Precompute Zeros**: Cache frequently used Bessel function zeros
2. **Recurrence Relations**: Use three-term recurrence for efficiency
3. **Asymptotic Switching**: Automatic method selection based on arguments
4. **Precision Scaling**: Match precision to accuracy requirements

## Integration with Other Modules

- **Physics Simulations**: Wave equations and vibration analysis
- **Signal Processing**: Filter design and Fourier transforms  
- **Probability Theory**: Statistical distributions involving Bessel functions
- **Numerical Methods**: Integration and root finding for zeros computation

## See Also

- [Special Functions Overview](README.md) - Module introduction and examples
- [Gamma Functions Guide](gamma.md) - Related special functions
- [Orthogonal Polynomials Guide](orthogonal.md) - Spherical harmonics applications
- [Mathematical Physics Applications](https://mathworld.wolfram.com/BesselFunction.html)
- [Numerical Methods Documentation](../engine/numerical/README.md) - Underlying algorithms