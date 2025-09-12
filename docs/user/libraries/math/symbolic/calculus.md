# Symbolic Calculus Operations

The Symbolic Calculus module (`math/symbolic/calculus`) provides comprehensive symbolic differentiation, integration, and advanced calculus operations. This module enables analytical calculus computations, series analysis, differential equation solving, and vector calculus operations.

## Overview

The Symbolic Calculus module offers powerful analytical mathematics capabilities including:

- **Symbolic Differentiation**: All standard differentiation rules and techniques
- **Symbolic Integration**: Integration methods and indefinite/definite integrals
- **Multivariable Calculus**: Partial derivatives, gradients, and vector operations
- **Series Analysis**: Taylor series, Laurent series, and asymptotic analysis
- **Differential Equations**: ODE and PDE symbolic solving
- **Vector Calculus**: Divergence, curl, line integrals, and surface integrals
- **Complex Analysis**: Residue calculus and contour integration

## Core Data Structures

### Derivative Representation

```runa
Type called "Derivative":
    expression as String                    # Function being differentiated
    variable as String                     # Variable of differentiation
    order as Integer                       # Order of derivative (1, 2, 3, ...)
    partial_variables as List[String]      # For partial derivatives
    derivative_rule as String             # Rule used (product, chain, etc.)
    chain_rule_applications as List[String] # Nested chain rule applications
```

### Integral Representation

```runa
Type called "Integral":
    integrand as String                    # Function being integrated
    variable as String                     # Variable of integration
    integration_bounds as Dictionary[String, String] # Lower and upper bounds
    integration_method as String          # Method used (substitution, parts, etc.)
    substitutions_used as List[String]    # Substitutions applied
    is_definite as Boolean               # Definite vs indefinite integral
    convergence_status as String         # Convergent, divergent, or conditional
```

## Symbolic Differentiation

### Basic Differentiation

```runa
Import "math/symbolic/calculus" as Calculus

Note: Basic derivative operations
Let f be "x^3 + 2*x^2 - 5*x + 1"
Let df_dx be Calculus.differentiate(f, "x")

Display "f(x) = " joined with f
Display "f'(x) = " joined with df_dx

Note: Higher-order derivatives
Let f_second be Calculus.differentiate_nth(f, "x", 2)
Let f_third be Calculus.differentiate_nth(f, "x", 3)

Display "f''(x) = " joined with f_second
Display "f'''(x) = " joined with f_third
```

### Advanced Differentiation Rules

```runa
Note: Product rule
Let u be "x^2"
Let v be "sin(x)"
Let product be u + "*" + v

Let product_derivative be Calculus.differentiate(product, "x")
Display "d/dx[x² · sin(x)] = " joined with product_derivative

Note: Quotient rule
Let numerator be "ln(x)"
Let denominator be "x^2 + 1"
Let quotient be numerator + "/" + "(" + denominator + ")"

Let quotient_derivative be Calculus.differentiate(quotient, "x")
Display "d/dx[ln(x)/(x² + 1)] = " joined with quotient_derivative

Note: Chain rule
Let composite be "sin(x^2 + 1)"
Let chain_derivative be Calculus.differentiate(composite, "x")

Display "d/dx[sin(x² + 1)] = " joined with chain_derivative

Note: Implicit differentiation
Let implicit_equation be "x^2 + y^2 = 25"
Let dy_dx be Calculus.implicit_differentiate(implicit_equation, "y", "x")

Display "For x² + y² = 25:"
Display "dy/dx = " joined with dy_dx
```

### Partial Derivatives

```runa
Note: Multivariable functions
Let f_xy be "x^3*y^2 + 2*x*y + sin(x*y)"

Note: First-order partial derivatives
Let df_dx be Calculus.partial_derivative(f_xy, "x")
Let df_dy be Calculus.partial_derivative(f_xy, "y")

Display "f(x,y) = " joined with f_xy
Display "∂f/∂x = " joined with df_dx
Display "∂f/∂y = " joined with df_dy

Note: Second-order partial derivatives
Let d2f_dx2 be Calculus.partial_derivative_nth(f_xy, "x", 2)
Let d2f_dy2 be Calculus.partial_derivative_nth(f_xy, "y", 2)
Let d2f_dxdy be Calculus.mixed_partial_derivative(f_xy, "x", "y")

Display "∂²f/∂x² = " joined with d2f_dx2
Display "∂²f/∂y² = " joined with d2f_dy2
Display "∂²f/∂x∂y = " joined with d2f_dxdy
```

### Gradient and Directional Derivatives

```runa
Note: Gradient computation
Let scalar_field be "x^2 + y^2 + z^2"
Let gradient be Calculus.gradient(scalar_field, ["x", "y", "z"])

Display "∇f = " joined with Calculus.vector_to_string(gradient)

Note: Directional derivative
Let direction_vector be ["1", "1", "0"]  Note: direction (1, 1, 0)
Let directional_deriv be Calculus.directional_derivative(scalar_field, direction_vector, ["x", "y", "z"])

Display "Directional derivative in direction (1, 1, 0): " joined with directional_deriv

Note: Laplacian
Let laplacian be Calculus.laplacian(scalar_field, ["x", "y", "z"])
Display "∇²f = " joined with laplacian
```

## Symbolic Integration

### Basic Integration

```runa
Note: Indefinite integrals
Let integrand1 be "x^3 + 2*x - 1"
Let integral1 be Calculus.integrate(integrand1, "x")

Display "∫(" joined with integrand1 joined with ") dx = " joined with integral1

Note: Definite integrals
Let definite_result be Calculus.integrate_definite(integrand1, "x", "0", "2")
Display "∫₀² (" joined with integrand1 joined with ") dx = " joined with definite_result

Note: Improper integrals
Let improper_integrand be "1/(x^2 + 1)"
Let improper_result be Calculus.integrate_definite(improper_integrand, "x", "-∞", "∞")
Display "∫_{-∞}^{∞} 1/(x² + 1) dx = " joined with improper_result
```

### Integration Techniques

```runa
Note: Integration by substitution
Let substitution_integrand be "x*sqrt(1 + x^2)"
Let u_substitution be Calculus.integrate_by_substitution(
    substitution_integrand, 
    "x", 
    "u = 1 + x^2"
)

Display "∫ x√(1 + x²) dx = " joined with u_substitution.result
Display "Using substitution: " joined with u_substitution.substitution

Note: Integration by parts
Let parts_integrand be "x*exp(x)"
Let parts_result be Calculus.integrate_by_parts(
    parts_integrand,
    "x",
    Dictionary with:
        "u": "x"
        "dv": "exp(x)*dx"
)

Display "∫ x·eˣ dx = " joined with parts_result.result
Display "u = " joined with parts_result.u
Display "v = " joined with parts_result.v

Note: Partial fraction integration
Let rational_integrand be "1/((x-1)*(x+2))"
Let partial_fractions be Calculus.integrate_rational_function(rational_integrand, "x")

Display "∫ 1/((x-1)(x+2)) dx = " joined with partial_fractions.result
Display "Partial fractions used: " joined with partial_fractions.decomposition
```

### Special Integration Methods

```runa
Note: Trigonometric integrals
Let trig_integrand be "sin^3(x)*cos^2(x)"
Let trig_result be Calculus.integrate_trigonometric(trig_integrand, "x")

Display "∫ sin³(x)cos²(x) dx = " joined with trig_result

Note: Hyperbolic function integrals
Let hyperbolic_integrand be "sinh(x)*cosh(x)"
Let hyperbolic_result be Calculus.integrate(hyperbolic_integrand, "x")

Display "∫ sinh(x)cosh(x) dx = " joined with hyperbolic_result

Note: Logarithmic and exponential integrals
Let log_integrand be "ln(x)/x"
Let log_result be Calculus.integrate(log_integrand, "x")

Display "∫ ln(x)/x dx = " joined with log_result
```

### Multiple Integration

```runa
Note: Double integrals
Let double_integrand be "x*y^2"
Let double_integral be Calculus.integrate_multiple(
    double_integrand,
    [
        Dictionary with: "variable": "x", "lower": "0", "upper": "1",
        Dictionary with: "variable": "y", "lower": "0", "upper": "x"
    ]
)

Display "∬ xy² dA = " joined with double_integral

Note: Triple integrals with variable limits
Let triple_integrand be "x^2 + y^2 + z^2"
Let triple_integral be Calculus.integrate_multiple(
    triple_integrand,
    [
        Dictionary with: "variable": "x", "lower": "0", "upper": "1",
        Dictionary with: "variable": "y", "lower": "0", "upper": "sqrt(1-x^2)",
        Dictionary with: "variable": "z", "lower": "0", "upper": "sqrt(1-x^2-y^2)"
    ]
)

Display "∭ (x² + y² + z²) dV = " joined with triple_integral
```

## Series Analysis

### Taylor Series

```runa
Note: Taylor series expansions
Let function be "exp(x)"
Let taylor_series be Calculus.taylor_series(function, "x", "0", 10)

Display "e^x = " joined with taylor_series.series_representation
Display "Expansion point: " joined with taylor_series.expansion_point
Display "Terms included: " joined with String(taylor_series.order)

Note: Multivariable Taylor series
Let multivar_function be "sin(x + y)"
Let multivar_taylor be Calculus.multivariate_taylor_series(
    multivar_function,
    ["x", "y"],
    ["0", "0"],
    3
)

Display "sin(x + y) ≈ " joined with multivar_taylor.series_representation
```

### Laurent Series

```runa
Note: Laurent series for functions with poles
Let function_with_pole be "1/(z^2*(z-1))"
Let laurent_series be Calculus.laurent_series(function_with_pole, "z", "0", -2, 5)

Display "1/(z²(z-1)) = " joined with laurent_series.series_representation
Display "Principal part: " joined with laurent_series.principal_part
Display "Regular part: " joined with laurent_series.regular_part

Note: Residue calculation
Let residue be Calculus.compute_residue(function_with_pole, "z", "0")
Display "Residue at z=0: " joined with residue
```

### Asymptotic Analysis

```runa
Note: Asymptotic expansions
Let function be "x*exp(-x)"
Let asymptotic_expansion be Calculus.asymptotic_expansion(function, "x", "∞", 5)

Display "x·e^(-x) ~ " joined with asymptotic_expansion.expansion joined with " as x → ∞"

Note: Big O and little o analysis
Let f be "x^2 + 3*x + 1"
Let g be "x^2"

Let big_o_relation be Calculus.big_o_analysis(f, g, "x", "∞")
Let little_o_relation be Calculus.little_o_analysis(f, g, "x", "∞")

Display "f(x) = O(g(x)): " joined with String(big_o_relation)
Display "f(x) = o(g(x)): " joined with String(little_o_relation)
```

## Differential Equations

### Ordinary Differential Equations

```runa
Note: First-order ODEs
Let ode1 be "dy/dx = 2*x*y"
Let ode1_solution be Calculus.solve_ode(ode1, "y", "x")

Display "ODE: " joined with ode1
Display "Solution: " joined with ode1_solution.general_solution

Note: Second-order linear ODEs
Let ode2 be "d²y/dx² - 3*dy/dx + 2*y = 0"
Let ode2_solution be Calculus.solve_linear_ode(ode2, "y", "x", 2)

Display "Second-order ODE: " joined with ode2
Display "General solution: " joined with ode2_solution.general_solution
Display "Characteristic equation: " joined with ode2_solution.characteristic_equation

Note: Initial value problems
Let ivp_solution be Calculus.solve_initial_value_problem(
    ode1,
    "y", "x",
    Dictionary with: "x0": "0", "y0": "1"
)

Display "IVP solution: " joined with ivp_solution.particular_solution
```

### Partial Differential Equations

```runa
Note: Heat equation
Let heat_equation be "∂u/∂t = α²*(∂²u/∂x²)"
Let heat_solution be Calculus.solve_pde(heat_equation, "u", ["x", "t"], Dictionary with:
    "type": "parabolic"
    "method": "separation_of_variables"
    "boundary_conditions": [
        "u(0, t) = 0",
        "u(L, t) = 0"
    ]
    "initial_conditions": ["u(x, 0) = f(x)"]
)

Display "Heat equation solution:"
Display heat_solution.general_solution

Note: Wave equation
Let wave_equation be "∂²u/∂t² = c²*(∂²u/∂x²)"
Let wave_solution be Calculus.solve_wave_equation(
    wave_equation,
    "u", ["x", "t"],
    Dictionary with:
        "wave_speed": "c"
        "boundary_conditions": ["u(0, t) = u(L, t) = 0"]
        "initial_conditions": [
            "u(x, 0) = f(x)",
            "∂u/∂t(x, 0) = g(x)"
        ]
)

Display "Wave equation solution:"
Display wave_solution.d_alembert_solution
```

## Vector Calculus

### Vector Field Operations

```runa
Note: Define vector fields
Let vector_field_F be [
    "y*z",      Note: F₁ component
    "x*z",      Note: F₂ component
    "x*y"       Note: F₃ component
]

Note: Divergence
Let div_F be Calculus.divergence(vector_field_F, ["x", "y", "z"])
Display "div F = " joined with div_F

Note: Curl
Let curl_F be Calculus.curl(vector_field_F, ["x", "y", "z"])
Display "curl F = " joined with Calculus.vector_to_string(curl_F)

Note: Check if field is conservative
Let is_conservative be Calculus.is_conservative(vector_field_F, ["x", "y", "z"])
Display "Is conservative: " joined with String(is_conservative)

If is_conservative:
    Let potential be Calculus.find_potential_function(vector_field_F, ["x", "y", "z"])
    Display "Potential function: " joined with potential
```

### Line and Surface Integrals

```runa
Note: Line integrals
Let curve be Dictionary with:
    "parametric": ["t", "t^2", "t^3"]
    "parameter": "t"
    "domain": ["0", "1"]

Let line_integral_scalar be Calculus.line_integral_scalar_field("x^2 + y^2 + z^2", curve)
Display "∫_C (x² + y² + z²) ds = " joined with line_integral_scalar

Let line_integral_vector be Calculus.line_integral_vector_field(vector_field_F, curve)
Display "∫_C F · dr = " joined with line_integral_vector

Note: Surface integrals
Let surface be Dictionary with:
    "parametric": ["u*cos(v)", "u*sin(v)", "u^2"]
    "parameters": ["u", "v"]
    "domain": [["0", "1"], ["0", "2*π"]]

Let surface_integral be Calculus.surface_integral(vector_field_F, surface)
Display "∬_S F · dS = " joined with surface_integral
```

### Fundamental Theorems

```runa
Note: Green's theorem verification
Let region be Dictionary with:
    "boundary": ["t", "sin(t)"]  Note: Simple example
    "parameter_range": ["0", "2*π"]

Let greens_lhs be Calculus.line_integral_vector_field(["x*y", "-x^2"], region.boundary)
Let greens_rhs be Calculus.double_integral(
    Calculus.partial_derivative("-x^2", "x") + " - " + Calculus.partial_derivative("x*y", "y"),
    region
)

Display "Green's theorem verification:"
Display "∮_C (xy dx - x² dy) = " joined with greens_lhs
Display "∬_R (∂Q/∂x - ∂P/∂y) dA = " joined with greens_rhs

Note: Stokes' theorem
Let surface_with_boundary be Dictionary with:
    "surface": surface
    "boundary_curve": curve

Let stokes_lhs be Calculus.line_integral_vector_field(vector_field_F, surface_with_boundary.boundary_curve)
Let stokes_rhs be Calculus.surface_integral(
    Calculus.curl(vector_field_F, ["x", "y", "z"]),
    surface_with_boundary.surface
)

Display "Stokes' theorem verification:"
Display "∮_C F · dr = " joined with stokes_lhs
Display "∬_S (curl F) · dS = " joined with stokes_rhs
```

## Complex Analysis

### Complex Functions

```runa
Note: Complex differentiation
Let complex_function be "z^2 + i*z + 1"
Let complex_derivative be Calculus.complex_differentiate(complex_function, "z")

Display "f(z) = " joined with complex_function
Display "f'(z) = " joined with complex_derivative

Note: Cauchy-Riemann equations
Let u be "x^2 - y^2"  Note: Real part
Let v be "2*x*y"      Note: Imaginary part

Let cr_satisfied be Calculus.check_cauchy_riemann(u, v, "x", "y")
Display "Cauchy-Riemann equations satisfied: " joined with String(cr_satisfied)

If cr_satisfied:
    Let analytic_function be u + " + i*(" + v + ")"
    Display "Analytic function: f(z) = " joined with analytic_function
```

### Contour Integration

```runa
Note: Contour integrals using residue theorem
Let complex_integrand be "1/(z^3 - 1)"
Let contour be Dictionary with:
    "type": "circle"
    "center": "0"
    "radius": "2"

Note: Find singularities
Let singularities be Calculus.find_singularities(complex_integrand, "z")
Display "Singularities: " joined with StringOps.join(singularities, ", ")

Note: Compute residues
Let residues be []
For Each singularity in singularities:
    If Calculus.is_inside_contour(singularity, contour):
        Let residue be Calculus.compute_residue(complex_integrand, "z", singularity)
        Let residues be ListOps.append(residues, residue)

Note: Apply residue theorem
Let contour_integral be Calculus.contour_integral_by_residues(residues)
Display "∮_C 1/(z³ - 1) dz = " joined with contour_integral
```

## Limits and Continuity

### Limit Computation

```runa
Note: Standard limits
Let limit1 be Calculus.limit("sin(x)/x", "x", "0")
Display "lim_{x→0} sin(x)/x = " joined with limit1

Note: L'Hôpital's rule
Let indeterminate_form be "x*ln(x)"
Let lhopital_limit be Calculus.limit_lhopital(indeterminate_form, "x", "0")
Display "lim_{x→0⁺} x ln(x) = " joined with lhopital_limit

Note: Multivariable limits
Let multivar_limit be Calculus.limit_multivariate("(x^2*y)/(x^2 + y^2)", ["x", "y"], ["0", "0"])
If multivar_limit.exists:
    Display "lim_{(x,y)→(0,0)} x²y/(x² + y²) = " joined with multivar_limit.value
Otherwise:
    Display "Limit does not exist"
    Display "Approach paths give different limits: " joined with StringOps.join(multivar_limit.counterexamples, ", ")
```

### Continuity Analysis

```runa
Note: Test function continuity
Note: The following quoted expression uses conventional mathematical "if/then/else" notation as data, not Runa control flow keywords.
Let function be "if x ≠ 0 then sin(x)/x else 1"
Let continuity_at_zero be Calculus.test_continuity(function, "x", "0")

Display "Function is continuous at x=0: " joined with String(continuity_at_zero.is_continuous)

If not continuity_at_zero.is_continuous:
    Display "Type of discontinuity: " joined with continuity_at_zero.discontinuity_type
    Display "Left limit: " joined with continuity_at_zero.left_limit
    Display "Right limit: " joined with continuity_at_zero.right_limit
    Display "Function value: " joined with continuity_at_zero.function_value
```

## Optimization and Critical Points

### Critical Point Analysis

```runa
Note: Find critical points
Let function be "x^3 - 3*x^2 + 2"
Let critical_points be Calculus.find_critical_points(function, "x")

Display "Critical points:"
For Each point in critical_points:
    Display "  x = " joined with point.value
    Display "  Type: " joined with point.classification  Note: local max, min, or inflection

Note: Second derivative test
For Each point in critical_points:
    Let second_deriv be Calculus.second_derivative_test(function, "x", point.value)
    Display "At x = " joined with point.value joined with ": " joined with second_deriv.conclusion
```

### Multivariable Optimization

```runa
Note: Find critical points of multivariable functions
Let multivar_function be "x^2 + y^2 - 2*x - 4*y + 5"
Let gradient_vector be Calculus.gradient(multivar_function, ["x", "y"])

Let critical_points_2d be Calculus.solve_system([
    gradient_vector[0] + " = 0",
    gradient_vector[1] + " = 0"
], ["x", "y"])

Display "Critical point: (" joined with critical_points_2d.x joined with ", " joined with critical_points_2d.y joined with ")"

Note: Hessian matrix analysis
Let hessian be Calculus.hessian_matrix(multivar_function, ["x", "y"])
Let at_critical_point be Calculus.evaluate_hessian(hessian, critical_points_2d)
let classification be Calculus.classify_critical_point_2d(at_critical_point)

Display "Classification: " joined with classification  Note: local min/max or saddle point
```

## Fourier Analysis

### Fourier Series

```runa
Note: Compute Fourier series
Note: The following quoted expression uses conventional mathematical "if/then/else" notation as data, not Runa control flow keywords.
Let periodic_function be "if -π < x < 0 then -1 else 1"  Note: Square wave
Let fourier_series be Calculus.fourier_series(periodic_function, "x", "π")

Display "Fourier series coefficients:"
Display "a₀ = " joined with fourier_series.a0
For Each n, coefficient in fourier_series.cosine_coefficients:
    Display "a" joined with String(n) joined with " = " joined with coefficient
For Each n, coefficient in fourier_series.sine_coefficients:
    Display "b" joined with String(n) joined with " = " joined with coefficient

Let fourier_approximation be Calculus.fourier_series_partial_sum(fourier_series, 10)
Display "10-term approximation: " joined with fourier_approximation
```

### Fourier Transform

```runa
Note: Symbolic Fourier transforms
Let time_function be "exp(-a*t^2)"  Note: Gaussian function
Let fourier_transform be Calculus.fourier_transform(time_function, "t", "ω")

Display "F{e^(-at²)} = " joined with fourier_transform

Note: Convolution theorem
Let f be "exp(-t)"
Let g be "sin(t)"
Let convolution be Calculus.convolution(f, g, "t")
Let transform_of_convolution be Calculus.fourier_transform(convolution, "t", "ω")

Let F_f be Calculus.fourier_transform(f, "t", "ω") 
Let F_g be Calculus.fourier_transform(g, "t", "ω")
let product_of_transforms be "(" + F_f + ")*(" + F_g + ")"

Display "Convolution theorem verification:"
Display "F{f * g} = " joined with transform_of_convolution
Display "F{f} × F{g} = " joined with product_of_transforms
```

## Error Handling and Validation

### Mathematical Error Management

```runa
Try:
    Let problematic_integral be Calculus.integrate("1/x", "x", "-1", "1")  Note: Integrand has singularity
    
Catch Errors.ConvergenceError as conv_error:
    Display "Integration convergence error: " joined with conv_error.message
    Display "Singularity location: " joined with conv_error.singularity_point
    
    Note: Suggest principal value computation
    Let principal_value be Calculus.principal_value_integral("1/x", "x", "-1", "1")
    Display "Principal value: " joined with principal_value

Catch Errors.CalculusError as calc_error:
    Display "Calculus operation error: " joined with calc_error.message
    Display "Failed operation: " joined with calc_error.operation
    Display "Function: " joined with calc_error.function
```

### Domain Validation

```runa
Note: Check function domains before operations
Let function_to_check be "ln(x - 1)"
Let domain_analysis be Calculus.analyze_domain(function_to_check, "x")

Display "Function: " joined with function_to_check
Display "Domain: " joined with domain_analysis.domain
Display "Singularities: " joined with StringOps.join(domain_analysis.singularities, ", ")
Display "Branch cuts: " joined with StringOps.join(domain_analysis.branch_cuts, ", ")

Note: Validate integration bounds
Let bounds_check be Calculus.validate_integration_bounds("1/sqrt(1-x^2)", "x", "-2", "2")
If not bounds_check.valid:
    Display "Invalid integration bounds:"
    Display "Issues: " joined with StringOps.join(bounds_check.issues, ", ")
    Display "Suggested bounds: " joined with bounds_check.suggested_bounds
```

## Performance Optimization

### Caching and Memoization

```runa
Note: Enable caching for expensive symbolic operations
Let cache_config be Dictionary with:
    "cache_derivatives": "true"
    "cache_integrals": "true"
    "cache_series": "true"
    "max_cache_size": "1000"

Calculus.configure_caching(cache_config)

Note: Expensive computation that benefits from caching
Let expensive_computation be Calculus.integrate("exp(-x^2)*sin(x)", "x")
let cached_result be Calculus.integrate("exp(-x^2)*sin(x)", "x")  Note: Should use cache

Let cache_stats be Calculus.get_cache_statistics()
Display "Cache hits: " joined with String(cache_stats.hits)
```

## Related Documentation

- **[Symbolic Core](core.md)**: Expression representation and manipulation
- **[Symbolic Algebra](algebra.md)**: Algebraic operations and polynomial manipulation
- **[Symbolic Functions](functions.md)**: Special functions and mathematical identities
- **[Symbolic Series](series.md)**: Series analysis and expansions
- **[Numerical Integration](../engine/numerical/integration.md)**: Numerical integration methods
- **[Differential Equations](../engine/numerical/ode.md)**: Numerical ODE solving
- **[Real Analysis](../analysis/real.md)**: Real analysis operations
- **[Complex Analysis](../analysis/complex.md)**: Complex analysis functions

The Symbolic Calculus module provides comprehensive analytical mathematics capabilities, from basic differentiation and integration to advanced vector calculus, differential equations, and complex analysis. Its symbolic approach enables exact mathematical computations and analytical insights that complement numerical methods.