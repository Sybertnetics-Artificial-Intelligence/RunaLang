# Calculus Symbols

The Calculus Symbols module provides comprehensive support for mathematical notation used in calculus and mathematical analysis. This module covers integral and derivative symbols, limit notation, vector calculus operators, and advanced analysis symbols.

## Quick Start

```runa
Import "math/symbols/calculus_symbols" as Calculus

Note: Access basic calculus symbols
Let integral_symbol be Calculus.get_integral_symbol("definite")
Let derivative_symbol be Calculus.get_derivative_symbol("partial")
Let limit_symbol be Calculus.get_limit_symbol("standard")

Display "Basic calculus: " joined with derivative_symbol joined with " " joined with integral_symbol

Note: Create calculus expressions
Let integral_expression be Calculus.create_integral_expression(
    "0", "∞", "e^(-x²)", "x"
)
Let derivative_expression be Calculus.create_derivative_expression(
    "f", "x", 2  Note: Second derivative
)

Display "Integral: " joined with integral_expression
Display "Derivative: " joined with derivative_expression

Note: Validate calculus notation
Let expression be "∫₀^∞ e^(-x²) dx = √π/2"
Let validation_result be Calculus.validate_calculus_expression(expression)
If Calculus.is_valid_calculus(validation_result):
    Display "Valid calculus expression"
```

## Integral Symbols and Notation

### Single Variable Integrals

```runa
Import "math/symbols/calculus_symbols" as Calc

Note: Different types of integral symbols
Let indefinite_integral be Calc.get_indefinite_integral()      Note: ∫
Let definite_integral be Calc.get_definite_integral()          Note: ∫ with limits
Let improper_integral be Calc.get_improper_integral()          Note: ∫ with infinite limits
Let riemann_integral be Calc.get_riemann_integral()            Note: Standard ∫

Display "Indefinite: " joined with indefinite_integral joined with " f(x) dx"
Display "Definite: " joined with definite_integral joined with "ₐᵇ f(x) dx"
Display "Improper: " joined with improper_integral joined with "₋∞^∞ f(x) dx"

Note: Create formatted integral expressions
Let basic_integral be Calc.format_integral("sin(x)", "x", "0", "π")
Let substitution_integral be Calc.format_integral("u² du", "u", "0", "1")
Let parametric_integral be Calc.format_parametric_integral("f(t)", "t", "a", "b")

Display "Basic: " joined with basic_integral
Display "Substitution: " joined with substitution_integral
Display "Parametric: " joined with parametric_integral
```

### Multiple Integrals

```runa
Note: Multi-dimensional integration symbols
Let double_integral be Calc.get_double_integral()              Note: ∬
Let triple_integral be Calc.get_triple_integral()              Note: ∭
Let quadruple_integral be Calc.get_quadruple_integral()        Note: ⨌

Display "Double integral: " joined with double_integral joined with " f(x,y) dx dy"
Display "Triple integral: " joined with triple_integral joined with " f(x,y,z) dx dy dz"

Note: Region-specific multiple integrals
Let region_double = Calc.format_region_integral(
    "f(x,y)", ["x", "y"], "D"
)
Let volume_triple = Calc.format_volume_integral(
    "ρ(x,y,z)", ["x", "y", "z"], "V"
)

Display "Over region D: " joined with region_double
Display "Over volume V: " joined with volume_triple

Note: Coordinate system integrals
Let polar_integral be Calc.format_polar_integral("r²", "r", "θ", "0", "2π", "0", "R")
Let cylindrical_integral be Calc.format_cylindrical_integral("z", "r", "θ", "z")
Let spherical_integral be Calc.format_spherical_integral("ρ²", "ρ", "θ", "φ")

Display "Polar: " joined with polar_integral
Display "Cylindrical: " joined with cylindrical_integral
Display "Spherical: " joined with spherical_integral
```

### Line and Surface Integrals

```runa
Note: Path and surface integration
Let line_integral be Calc.get_line_integral_symbol()           Note: ∮ or ∫_C
Let closed_line_integral be Calc.get_closed_line_integral()    Note: ∮
Let surface_integral be Calc.get_surface_integral_symbol()     Note: ∬_S
Let closed_surface_integral be Calc.get_closed_surface_integral()  Note: ∯

Display "Line integral: " joined with line_integral joined with "_C F·dr"
Display "Closed line: " joined with closed_line_integral joined with "_C F·dr"
Display "Surface integral: " joined with surface_integral joined with "_S F·dS"
Display "Closed surface: " joined with closed_surface_integral joined with "_S F·dS"

Note: Vector field integrals
Let work_integral be Calc.format_work_integral("F", "C")
Let flux_integral be Calc.format_flux_integral("F", "S")
Let circulation_integral be Calc.format_circulation_integral("F", "C")

Display "Work: " joined with work_integral
Display "Flux: " joined with flux_integral
Display "Circulation: " joined with circulation_integral
```

## Derivative Symbols and Notation

### Ordinary Derivatives

```runa
Note: Standard derivative notation
Let leibniz_notation be Calc.get_leibniz_derivative("f", "x")      Note: df/dx
Let prime_notation be Calc.get_prime_derivative("f", 1)            Note: f'
Let dot_notation be Calc.get_dot_derivative("x", 1)                Note: ẋ for time derivatives

Display "Leibniz: " joined with leibniz_notation
Display "Prime: " joined with prime_notation joined with "(x)"
Display "Dot: " joined with dot_notation joined with " (time derivative)"

Note: Higher-order derivatives
Let second_derivative be Calc.get_nth_derivative("f", "x", 2)      Note: d²f/dx²
Let third_derivative be Calc.get_nth_derivative("f", "x", 3)       Note: d³f/dx³
Let nth_derivative be Calc.get_nth_derivative("f", "x", "n")       Note: dⁿf/dxⁿ

Display "Second: " joined with second_derivative
Display "Third: " joined with third_derivative
Display "Nth: " joined with nth_derivative
```

### Partial Derivatives

```runa
Note: Partial derivative symbols
Let partial_symbol be Calc.get_partial_symbol()                   Note: ∂
Let first_partial be Calc.get_partial_derivative("f", "x")        Note: ∂f/∂x
Let mixed_partial be Calc.get_mixed_partial("f", ["x", "y"])      Note: ∂²f/∂x∂y

Display "Partial symbol: " joined with partial_symbol
Display "First partial: " joined with first_partial
Display "Mixed partial: " joined with mixed_partial

Note: Higher-order partial derivatives
Let second_partial_x be Calc.get_partial_derivative("f", "x", 2)  Note: ∂²f/∂x²
Let second_partial_y be Calc.get_partial_derivative("f", "y", 2)  Note: ∂²f/∂y²
Let laplacian_2d be Calc.format_laplacian_2d("f")                Note: ∂²f/∂x² + ∂²f/∂y²

Display "Second partial x: " joined with second_partial_x
Display "Second partial y: " joined with second_partial_y
Display "2D Laplacian: " joined with laplacian_2d
```

### Vector Derivatives

```runa
Note: Vector calculus derivative operators
Let gradient_symbol be Calc.get_gradient_symbol()                 Note: ∇
Let divergence_operator be Calc.get_divergence_operator()         Note: ∇·
Let curl_operator be Calc.get_curl_operator()                     Note: ∇×
Let laplacian_operator be Calc.get_laplacian_operator()           Note: ∇² or Δ

Display "Gradient: " joined with gradient_symbol joined with "f"
Display "Divergence: " joined with divergence_operator joined with "F"
Display "Curl: " joined with curl_operator joined with "F"
Display "Laplacian: " joined with laplacian_operator joined with "f"

Note: Vector field operations
Let gradient_field be Calc.format_gradient("f", ["x", "y", "z"])
Let divergence_calc be Calc.format_divergence("F", ["x", "y", "z"])
Let curl_calc be Calc.format_curl("F", ["x", "y", "z"])

Display "Gradient: " joined with gradient_field
Display "Divergence: " joined with divergence_calc
Display "Curl: " joined with curl_calc
```

## Limit Symbols and Notation

### Standard Limits

```runa
Note: Limit notation
Let limit_symbol be Calc.get_limit_symbol()                      Note: lim
Let limit_at_point be Calc.format_limit("f(x)", "x", "a")        Note: lim(x→a) f(x)
Let limit_at_infinity be Calc.format_limit("f(x)", "x", "∞")     Note: lim(x→∞) f(x)

Display "Limit at point: " joined with limit_at_point
Display "Limit at infinity: " joined with limit_at_infinity

Note: One-sided limits
Let left_limit be Calc.format_left_limit("f(x)", "x", "a")       Note: lim(x→a⁻) f(x)
Let right_limit be Calc.format_right_limit("f(x)", "x", "a")     Note: lim(x→a⁺) f(x)

Display "Left limit: " joined with left_limit
Display "Right limit: " joined with right_limit
```

### Multi-Variable Limits

```runa
Note: Limits in multiple variables
Let multivariable_limit be Calc.format_multivariable_limit(
    "f(x,y)", ["x", "y"], ["a", "b"]
)
Let path_limit be Calc.format_path_limit("f(x,y)", "path", "(a,b)")

Display "Multivariable: " joined with multivariable_limit
Display "Along path: " joined with path_limit

Note: Supremum and infimum
Let supremum_symbol be Calc.get_supremum_symbol()                Note: sup
Let infimum_symbol be Calc.get_infimum_symbol()                  Note: inf
Let limsup_symbol be Calc.get_limsup_symbol()                    Note: lim sup
Let liminf_symbol be Calc.get_liminf_symbol()                    Note: lim inf

Display "Supremum: " joined with supremum_symbol joined with " f(x)"
Display "Limit superior: " joined with limsup_symbol joined with " aₙ"
```

### Sequence and Series Limits

```runa
Note: Limits for sequences and series
Let sequence_limit be Calc.format_sequence_limit("aₙ", "n", "∞")
Let series_limit be Calc.format_series_limit("aₙ", "n", "1", "∞")

Display "Sequence limit: " joined with sequence_limit
Display "Series limit: " joined with series_limit

Note: Convergence notation
Let convergence_symbol be Calc.get_convergence_symbol()          Note: →
Let absolute_convergence be Calc.format_absolute_convergence("∑aₙ")
Let conditional_convergence be Calc.format_conditional_convergence("∑aₙ")

Display "Convergence: aₙ " joined with convergence_symbol joined with " L"
Display "Absolute convergence: " joined with absolute_convergence
```

## Summation and Product Notation

### Summation Symbols

```runa
Note: Summation notation
Let sigma_symbol be Calc.get_summation_symbol()                  Note: ∑
Let finite_sum be Calc.format_finite_sum("aᵢ", "i", "1", "n")   Note: ∑ᵢ₌₁ⁿ aᵢ
Let infinite_sum be Calc.format_infinite_sum("aᵢ", "i", "1")    Note: ∑ᵢ₌₁^∞ aᵢ

Display "Finite sum: " joined with finite_sum
Display "Infinite sum: " joined with infinite_sum

Note: Multiple summations
Let double_sum be Calc.format_double_sum("aᵢⱼ", "i", "j", "1", "n", "1", "m")
Let nested_sum be Calc.format_nested_sum("f(i,j,k)", ["i", "j", "k"], 
    ["1", "1", "1"], ["n", "m", "p"])

Display "Double sum: " joined with double_sum
Display "Nested sum: " joined with nested_sum
```

### Product Notation

```runa
Note: Product symbols
Let pi_symbol be Calc.get_product_symbol()                      Note: ∏
Let finite_product be Calc.format_finite_product("aᵢ", "i", "1", "n")  Note: ∏ᵢ₌₁ⁿ aᵢ
Let infinite_product be Calc.format_infinite_product("aᵢ", "i", "1")   Note: ∏ᵢ₌₁^∞ aᵢ

Display "Finite product: " joined with finite_product
Display "Infinite product: " joined with infinite_product

Note: Specialized products
Let factorial_product be Calc.format_factorial_as_product("n")
Let falling_factorial be Calc.format_falling_factorial("x", "n")
Let rising_factorial be Calc.format_rising_factorial("x", "n")

Display "Factorial: " joined with factorial_product
Display "Falling factorial: " joined with falling_factorial
Display "Rising factorial: " joined with rising_factorial
```

## Advanced Analysis Symbols

### Measure Theory

```runa
Note: Measure-theoretic integration
Let measure_integral be Calc.get_measure_integral_symbol()       Note: ∫ with measure
Let lebesgue_integral be Calc.format_lebesgue_integral("f", "μ", "X")
Let riemann_stieltjes be Calc.format_riemann_stieltjes_integral("f", "g", "a", "b")

Display "Lebesgue integral: " joined with lebesgue_integral
Display "Riemann-Stieltjes: " joined with riemann_stieltjes

Note: Almost everywhere notation
Let almost_everywhere be Calc.get_almost_everywhere_symbol()     Note: a.e.
Let almost_surely be Calc.get_almost_surely_symbol()             Note: a.s.
Let essential_supremum be Calc.get_essential_supremum_symbol()   Note: ess sup

Display "Almost everywhere: f = g " joined with almost_everywhere
Display "Essential supremum: " joined with essential_supremum joined with " f"
```

### Complex Analysis

```runa
Note: Complex analysis symbols
Let complex_integral be Calc.get_complex_line_integral()
Let residue_symbol be Calc.get_residue_symbol()                  Note: Res
Let principal_value be Calc.get_principal_value_symbol()         Note: P.V.

Display "Complex integral: " joined with complex_integral joined with "_C f(z) dz"
Display "Residue: " joined with residue_symbol joined with "(f, z₀)"
Display "Principal value: " joined with principal_value joined with " ∫ f(x) dx"

Note: Complex derivative notation
Let complex_derivative be Calc.format_complex_derivative("f", "z")
Let holomorphic_derivative be Calc.format_holomorphic_derivative("f", "z")
Let wirtinger_derivatives be Calc.format_wirtinger_derivatives("f", "z")

Display "Complex derivative: " joined with complex_derivative
Display "Holomorphic: " joined with holomorphic_derivative
```

### Functional Analysis

```runa
Note: Functional analysis notation
Let weak_convergence be Calc.get_weak_convergence_symbol()       Note: ⇀
Let strong_convergence be Calc.get_strong_convergence_symbol()   Note: →
Let weak_star_convergence be Calc.get_weak_star_convergence()    Note: *⇀

Display "Weak convergence: fₙ " joined with weak_convergence joined with " f"
Display "Strong convergence: fₙ " joined with strong_convergence joined with " f"
Display "Weak-* convergence: fₙ " joined with weak_star_convergence joined with " f"

Note: Operator notation
Let adjoint_operator be Calc.format_adjoint_operator("T")        Note: T*
Let composition_operator be Calc.format_operator_composition("T", "S")  Note: T∘S
Let tensor_product be Calc.format_tensor_product("A", "B")       Note: A⊗B

Display "Adjoint: " joined with adjoint_operator
Display "Composition: " joined with composition_operator
Display "Tensor product: " joined with tensor_product
```

## Differential Equations

### Ordinary Differential Equations

```runa
Note: ODE notation
Let ode_first_order be Calc.format_first_order_ode("y", "x")     Note: dy/dx = f(x,y)
Let ode_second_order be Calc.format_second_order_ode("y", "x")   Note: d²y/dx² = f(x,y,y')
Let ode_nth_order be Calc.format_nth_order_ode("y", "x", "n")    Note: dⁿy/dxⁿ = f(...)

Display "First order ODE: " joined with ode_first_order
Display "Second order ODE: " joined with ode_second_order
Display "nth order ODE: " joined with ode_nth_order

Note: Initial value problems
Let ivp_notation be Calc.format_initial_value_problem(
    "y", "x", "f(x,y)", "x₀", "y₀"
)
Display "Initial value problem: " joined with ivp_notation
```

### Partial Differential Equations

```runa
Note: PDE notation
Let heat_equation be Calc.format_heat_equation("u", "t", "x")
Let wave_equation be Calc.format_wave_equation("u", "t", "x")
Let laplace_equation be Calc.format_laplace_equation("u", ["x", "y"])
Let poisson_equation be Calc.format_poisson_equation("u", ["x", "y"], "f")

Display "Heat equation: " joined with heat_equation
Display "Wave equation: " joined with wave_equation
Display "Laplace equation: " joined with laplace_equation
Display "Poisson equation: " joined with poisson_equation

Note: Boundary conditions
Let dirichlet_bc be Calc.format_dirichlet_boundary("u", "∂Ω", "g")
Let neumann_bc be Calc.format_neumann_boundary("u", "∂Ω", "h")
Let robin_bc be Calc.format_robin_boundary("u", "∂Ω", "α", "β", "γ")

Display "Dirichlet BC: " joined with dirichlet_bc
Display "Neumann BC: " joined with neumann_bc
Display "Robin BC: " joined with robin_bc
```

## Variational Calculus

### Functional Derivatives

```runa
Note: Variational calculus symbols
Let functional_derivative be Calc.get_functional_derivative_symbol()  Note: δ
Let variation_symbol be Calc.get_variation_symbol()                   Note: δ
Let euler_lagrange be Calc.format_euler_lagrange_equation("L", "y", "x")

Display "Functional derivative: " joined with functional_derivative joined with "F/δy"
Display "Variation: " joined with variation_symbol joined with "y"
Display "Euler-Lagrange: " joined with euler_lagrange

Note: Action integrals
Let action_integral be Calc.format_action_integral("L", "q", "t₁", "t₂")
Let lagrangian_notation be Calc.format_lagrangian("L", ["q", "q̇", "t"])
Let hamiltonian_notation be Calc.format_hamiltonian("H", ["p", "q", "t"])

Display "Action: " joined with action_integral
Display "Lagrangian: " joined with lagrangian_notation
Display "Hamiltonian: " joined with hamiltonian_notation
```

## Symbol Formatting and Display

### Expression Formatting

```runa
Note: Format complex calculus expressions
Let complex_integral = Calc.format_complex_expression([
    "∫∫∫_V", "∇·F", "dV = ∮∮_S", "F·n̂", "dS"
])
Let stokes_theorem be Calc.format_stokes_theorem("F", "S", "C")
Let greens_theorem be Calc.format_greens_theorem("P", "Q", "D", "C")

Display "Divergence theorem: " joined with complex_integral
Display "Stokes' theorem: " joined with stokes_theorem
Display "Green's theorem: " joined with greens_theorem

Note: Multi-line expression formatting
Let multiline_calculation be Calc.format_multiline_calculation([
    "∫₀^∞ e^(-x²) dx",
    "= ½∫₋∞^∞ e^(-x²) dx", 
    "= ½√π",
    "= √π/2"
])
Display "Multi-step calculation:"
Display multiline_calculation
```

### Accessibility and Alternative Formats

```runa
Note: Generate accessible descriptions
Let integral_expression be "∫₀^∞ x²e^(-x) dx = 2!"
Let screen_reader_text be Calc.generate_accessibility_text(integral_expression)
Let speech_text be Calc.generate_speech_text(integral_expression)

Display "Screen reader: " joined with screen_reader_text
Display "Speech: " joined with speech_text

Note: Multiple output formats
Let latex_output be Calc.convert_to_latex(integral_expression)
Let mathml_output be Calc.convert_to_mathml(integral_expression)
Let ascii_math be Calc.convert_to_ascii_math(integral_expression)

Display "LaTeX: " joined with latex_output
Display "MathML: " joined with mathml_output
Display "ASCII Math: " joined with ascii_math
```

## Validation and Error Checking

### Expression Validation

```runa
Import "core/error_handling" as ErrorHandling

Note: Validate calculus expressions
Let expressions_to_check be [
    "∫₀^∞ e^(-x²) dx",           Note: Valid
    "∂²f/∂x²",                   Note: Valid
    "lim(x→0) sin(x)/x",         Note: Valid
    "∫₀ e^(-x²) dx",             Note: Missing upper limit
    "∂f/∂",                      Note: Missing variable
    "lim sin(x)/x"               Note: Missing approach
]

For Each expression in expressions_to_check:
    Let validation_result be Calc.validate_calculus_notation(expression)
    
    If ErrorHandling.is_valid(validation_result):
        Display expression joined with " ✓"
    Otherwise:
        Display expression joined with " ✗"
        Let errors be ErrorHandling.get_validation_errors(validation_result)
        For Each error in errors:
            Display "  Error: " joined with ErrorHandling.error_message(error)
            Display "  Fix: " joined with Calc.suggest_correction(error)
```

### Dimensional Analysis

```runa
Note: Check dimensional consistency
Let physics_expressions be [
    "∫ F dx = Work",             Note: Force × distance = energy
    "d²x/dt² = acceleration",    Note: length/time² = acceleration
    "∫ ρ dV = mass"              Note: density × volume = mass
]

For Each expr in physics_expressions:
    Let dimensional_check be Calc.check_dimensional_consistency(expr)
    If Calc.is_dimensionally_consistent(dimensional_check):
        Display expr joined with " - dimensions consistent"
    Otherwise:
        Let dimension_error be Calc.get_dimensional_error(dimensional_check)
        Display expr joined with " - " joined with dimension_error
```

## Integration Examples

### With Mathematical Computing

```runa
Import "math/core/operations" as Operations

Note: Integrate with numerical computation
Let integral_symbol be Calc.get_definite_integral()
Let numerical_value be Operations.numerical_integration("e^(-x²)", 0, 1)
Let symbolic_expression be Calc.combine_symbol_and_value(
    integral_symbol joined with "₀¹ e^(-x²) dx", 
    numerical_value
)

Display "Combined: " joined with symbolic_expression
```

### With Formatting Systems

```runa
Import "math/symbols/formatting" as Format

Note: Advanced mathematical formatting
Let complex_calculus = "∮_C (z² + 1)/(z - i) dz = 2πi·Res(f, i)"
Let formatted_result be Format.format_with_calculus_rules(
    complex_calculus,
    Calc.get_calculus_formatting_rules()
)

Display "Formatted calculus: " joined with formatted_result
```

## Performance Optimization

### Symbol Caching

```runa
Note: Optimize symbol lookup and rendering
Calc.enable_symbol_caching(True)
Calc.preload_common_calculus_symbols()

Let benchmark_result be Calc.benchmark_symbol_performance(1000)
Let average_time be Calc.get_average_symbol_time(benchmark_result)

Display "Average symbol lookup: " joined with average_time joined with "μs"
```

## Best Practices

### Mathematical Notation Standards
- Use standard calculus notation conventions consistently
- Prefer widely recognized symbols over alternative forms
- Consider context when choosing between notation variants
- Validate mathematical expressions for correctness

### Formatting Guidelines
- Use appropriate spacing around operators and symbols
- Maintain consistent subscript and superscript formatting
- Consider accessibility requirements for complex expressions
- Test symbol rendering across different display contexts

### Integration Recommendations
- Combine symbolic and numerical approaches when appropriate
- Validate dimensional consistency in physical applications
- Use proper mathematical typography for professional documents
- Consider internationalization for global mathematical communication

This module provides comprehensive support for calculus notation, enabling precise mathematical expression in computational analysis and educational applications.