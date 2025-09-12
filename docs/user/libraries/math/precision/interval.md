# Math Precision Interval Module

## Overview

The `math/precision/interval` module provides interval arithmetic operations for representing and computing with uncertain or imprecise values. It implements mathematical interval analysis techniques including uncertainty propagation, constraint satisfaction, global optimization, and verification methods, making it essential for robust numerical computation where rounding errors, measurement uncertainties, and parameter variations must be rigorously tracked and bounded.

## Key Features

- **Guaranteed Containment**: All operations preserve the containment property
- **Uncertainty Propagation**: Track error bounds through complex calculations  
- **Constraint Satisfaction**: Interval constraint propagation techniques
- **Global Optimization**: Branch-and-bound methods with guaranteed bounds
- **Verification Methods**: Computer-assisted proofs and validation
- **Inclusion Functions**: Optimal interval extensions of real functions
- **Robust Computing**: Handle measurement errors and parameter variations
- **Scientific Applications**: Validated numerical integration and ODE solving

## Data Types

### Interval
Represents a closed interval [lower, upper]:
```runa
Type called "Interval":
    lower as BigDecimal             Note: Lower bound (infimum)
    upper as BigDecimal             Note: Upper bound (supremum) 
    is_empty as Boolean             Note: Whether interval is empty
    precision as Integer            Note: Precision of bounds
```

### IntervalVector
Represents a vector of intervals for multidimensional problems:
```runa
Type called "IntervalVector":
    components as Array[Interval]   Note: Interval components
    dimension as Integer            Note: Number of dimensions
    is_degenerate as Boolean        Note: Whether any component is empty
```

### ConstraintResult
Result of constraint propagation:
```runa
Type called "ConstraintResult":
    intervals as IntervalVector     Note: Constrained intervals
    is_consistent as Boolean        Note: Whether constraints are satisfiable
    reduction_ratio as BigDecimal   Note: How much intervals were reduced
    iterations as Integer           Note: Number of propagation iterations
```

### OptimizationResult  
Result of interval-based global optimization:
```runa
Type called "OptimizationResult":
    global_minimum as Interval      Note: Bounds on global minimum value
    minimizer_box as IntervalVector Note: Box containing global minimizers
    upper_bound as BigDecimal       Note: Best known upper bound
    lower_bound as BigDecimal       Note: Guaranteed lower bound
    certified as Boolean            Note: Whether result is mathematically certified
```

## Basic Operations

### Creating Intervals
```runa
Import "math/precision/interval" as Interval

Note: Create intervals in various ways
Let point_interval be Interval.create_point("3.14159")
Let range_interval be Interval.create_range("2.5", "7.8")
Let center_radius be Interval.create_from_center_radius("5.0", "0.2")  Note: [4.8, 5.2]
Let percentage_error be Interval.create_from_relative_error("100.0", "0.05")  Note: 5% error

Note: Create from measurements with uncertainty
Let measurement be Interval.create_from_measurement("9.81", "0.02")  Note: g ± 0.02

Display "Point interval: " joined with Interval.to_string(point_interval)
Display "Range interval: " joined with Interval.to_string(range_interval)
Display "Center±radius: " joined with Interval.to_string(center_radius)
Display "Measurement: " joined with Interval.to_string(measurement)
```

### Arithmetic Operations
```runa
Note: Interval arithmetic preserves containment
Let a be Interval.create_range("2.0", "3.0")    Note: [2, 3]
Let b be Interval.create_range("1.5", "2.5")    Note: [1.5, 2.5]

Let sum be Interval.add(a, b)                    Note: [3.5, 5.5]
Let difference be Interval.subtract(a, b)        Note: [-0.5, 1.5]
Let product be Interval.multiply(a, b)           Note: [3.0, 7.5]
Let quotient be Interval.divide(a, b)            Note: [0.8, 2.0]

Display "Sum: " joined with Interval.to_string(sum)
Display "Difference: " joined with Interval.to_string(difference)
Display "Product: " joined with Interval.to_string(product)
Display "Quotient: " joined with Interval.to_string(quotient)

Note: Handle division by zero
Let zero_interval be Interval.create_range("-1.0", "1.0")  Note: Contains zero
Try:
    Let division_by_zero be Interval.divide(a, zero_interval)
Catch Errors.IntervalDivisionByZero as error:
    Display "Division by interval containing zero: " joined with error.message
    Let extended_result be Interval.extended_divide(a, zero_interval)
    Display "Extended division result: " joined with Interval.to_string(extended_result)
```

### Power and Root Operations
```runa
Note: Power operations with interval exponents
Let base be Interval.create_range("2.0", "3.0")
Let exponent be Interval.create_range("1.5", "2.5")

Let power_result be Interval.power(base, exponent)
Display "Power [2,3]^[1.5,2.5]: " joined with Interval.to_string(power_result)

Note: Root operations
Let radicand be Interval.create_range("4.0", "16.0")
Let square_root be Interval.sqrt(radicand)
Let cube_root be Interval.nth_root(radicand, 3)

Display "Square root of [4,16]: " joined with Interval.to_string(square_root)
Display "Cube root of [4,16]: " joined with Interval.to_string(cube_root)

Note: Handle negative numbers in roots
Let negative_interval be Interval.create_range("-8.0", "8.0")
Let complex_root be Interval.nth_root_real(negative_interval, 3)  Note: Only real cube root
Display "Real cube root of [-8,8]: " joined with Interval.to_string(complex_root)
```

## Advanced Mathematical Functions

### Trigonometric Functions
```runa
Note: Trigonometric functions with interval arguments
Let angle_interval be Interval.create_range("0.0", "1.5708")  Note: [0, π/2]

Let sine_result be Interval.sin(angle_interval)
Let cosine_result be Interval.cos(angle_interval)
Let tangent_result be Interval.tan(angle_interval)

Display "sin([0, π/2]): " joined with Interval.to_string(sine_result)
Display "cos([0, π/2]): " joined with Interval.to_string(cosine_result)
Display "tan([0, π/2]): " joined with Interval.to_string(tangent_result)

Note: Handle multiple periods
Let large_angle be Interval.create_range("0.0", "10.0")  Note: Multiple periods
Let sine_multi_period be Interval.sin(large_angle)
Display "sin([0, 10]) spans multiple periods: " joined with Interval.to_string(sine_multi_period)

Note: Inverse trigonometric functions
Let sin_values be Interval.create_range("-0.5", "0.5")
Let arcsin_result be Interval.asin(sin_values)
Display "arcsin([-0.5, 0.5]): " joined with Interval.to_string(arcsin_result)
```

### Exponential and Logarithmic Functions
```runa
Note: Exponential functions preserve monotonicity
Let exp_input be Interval.create_range("-1.0", "2.0")
Let exp_result be Interval.exp(exp_input)
Let exp10_result be Interval.exp10(exp_input)

Display "exp([-1, 2]): " joined with Interval.to_string(exp_result)
Display "10^[-1, 2]: " joined with Interval.to_string(exp10_result)

Note: Logarithmic functions (domain must be positive)
Let log_input be Interval.create_range("0.1", "10.0")
Let ln_result be Interval.log(log_input)
Let log10_result be Interval.log10(log_input)

Display "ln([0.1, 10]): " joined with Interval.to_string(ln_result)
Display "log10([0.1, 10]): " joined with Interval.to_string(log10_result)

Note: Handle domain violations
Let invalid_log_input be Interval.create_range("-1.0", "1.0")  Note: Contains non-positive values
Try:
    Let invalid_log be Interval.log(invalid_log_input)
Catch Errors.IntervalDomainError as error:
    Display "Domain error for logarithm: " joined with error.message
    Let restricted_log be Interval.log_restricted(invalid_log_input)  Note: Restricts to positive part
    Display "Restricted log result: " joined with Interval.to_string(restricted_log)
```

### Hyperbolic Functions
```runa
Note: Hyperbolic functions and their inverses
Let hyperbolic_input be Interval.create_range("-2.0", "2.0")

Let sinh_result be Interval.sinh(hyperbolic_input)
Let cosh_result be Interval.cosh(hyperbolic_input)
Let tanh_result be Interval.tanh(hyperbolic_input)

Display "sinh([-2, 2]): " joined with Interval.to_string(sinh_result)
Display "cosh([-2, 2]): " joined with Interval.to_string(cosh_result)  Note: Always ≥ 1
Display "tanh([-2, 2]): " joined with Interval.to_string(tanh_result)  Note: Bounded by [-1, 1]

Note: Inverse hyperbolic functions
Let asinh_result be Interval.asinh(hyperbolic_input)
Let acosh_input be Interval.create_range("1.0", "3.0")  Note: Domain ≥ 1
Let acosh_result be Interval.acosh(acosh_input)

Display "asinh([-2, 2]): " joined with Interval.to_string(asinh_result)
Display "acosh([1, 3]): " joined with Interval.to_string(acosh_result)
```

## Uncertainty Propagation

### Error Analysis in Calculations
```runa
Note: Propagate measurement uncertainties through calculations
Process called "calculate_volume_with_uncertainty" that takes length as Interval, width as Interval, height as Interval returns VolumeResult:
    Let volume be Interval.multiply(
        Interval.multiply(length, width),
        height
    )
    
    Let relative_uncertainty be Interval.divide(
        Interval.subtract(Interval.upper_bound(volume), Interval.lower_bound(volume)),
        Interval.midpoint(volume)
    )
    
    Return VolumeResult with:
        volume: volume
        absolute_uncertainty: Interval.width(volume)
        relative_uncertainty: relative_uncertainty
        confidence: "guaranteed"

Note: Measurements with uncertainties
Let length_measurement be Interval.create_from_measurement("10.5", "0.1")  Note: 10.5 ± 0.1 cm
Let width_measurement be Interval.create_from_measurement("8.2", "0.05")   Note: 8.2 ± 0.05 cm  
Let height_measurement be Interval.create_from_measurement("5.7", "0.08")  Note: 5.7 ± 0.08 cm

Let volume_result be calculate_volume_with_uncertainty(length_measurement, width_measurement, height_measurement)

Display "Volume calculation with uncertainty:"
Display "  Volume: " joined with Interval.to_string(volume_result.volume) joined with " cm³"
Display "  Absolute uncertainty: ±" joined with BigDecimal.to_string(volume_result.absolute_uncertainty)
Display "  Relative uncertainty: " joined with BigDecimal.to_string(volume_result.relative_uncertainty) joined with "%"
```

### Complex Expression Evaluation
```runa
Note: Evaluate complex expressions with interval arithmetic
Process called "evaluate_quadratic_formula" that takes a as Interval, b as Interval, c as Interval returns QuadraticSolution:
    Note: Solve ax² + bx + c = 0 using quadratic formula
    
    Let discriminant be Interval.subtract(
        Interval.multiply(b, b),
        Interval.multiply(
            Interval.multiply(Interval.create_point("4"), a),
            c
        )
    )
    
    If Interval.upper_bound(discriminant) < BigDecimal.ZERO:
        Return QuadraticSolution with:
            has_real_solutions: false
            discriminant_interval: discriminant
    
    Let sqrt_discriminant be Interval.sqrt(discriminant)
    Let two_a be Interval.multiply(Interval.create_point("2"), a)
    
    Let solution1 be Interval.divide(
        Interval.add(Interval.negate(b), sqrt_discriminant),
        two_a
    )
    
    Let solution2 be Interval.divide(
        Interval.subtract(Interval.negate(b), sqrt_discriminant),
        two_a
    )
    
    Return QuadraticSolution with:
        has_real_solutions: true
        solution1: solution1
        solution2: solution2
        discriminant_interval: discriminant

Let a_coeff be Interval.create_from_measurement("1.0", "0.01")    Note: Slightly uncertain
Let b_coeff be Interval.create_from_measurement("-5.0", "0.05")
Let c_coeff be Interval.create_from_measurement("6.0", "0.02")

Let quadratic_solution be evaluate_quadratic_formula(a_coeff, b_coeff, c_coeff)

If quadratic_solution.has_real_solutions:
    Display "Quadratic solutions with uncertainty:"
    Display "  x₁ ∈ " joined with Interval.to_string(quadratic_solution.solution1)
    Display "  x₂ ∈ " joined with Interval.to_string(quadratic_solution.solution2)
    Display "  Discriminant ∈ " joined with Interval.to_string(quadratic_solution.discriminant_interval)
```

### Taylor Series with Remainder Bounds
```runa
Note: Taylor series expansion with rigorous error bounds
Process called "taylor_exp_with_bounds" that takes x_interval as Interval, terms as Integer returns TaylorResult:
    Note: Compute e^x using Taylor series with remainder bounds
    
    Let sum be Interval.create_point("1.0")  Note: Start with first term
    Let factorial be BigDecimal.ONE
    
    For n from 1 to terms - 1:
        Set factorial to BigDecimal.multiply(factorial, BigDecimal.create_from_integer(n), 50)
        Let term be Interval.divide(
            Interval.power(x_interval, n),
            Interval.create_point(BigDecimal.to_string(factorial))
        )
        Set sum to Interval.add(sum, term)
    
    Note: Compute remainder bound using Lagrange form
    Set factorial to BigDecimal.multiply(factorial, BigDecimal.create_from_integer(terms), 50)
    Let max_x be Interval.abs_max(x_interval)
    Let remainder_bound be Interval.divide(
        Interval.exp(Interval.create_point(BigDecimal.to_string(max_x))),  Note: Upper bound on e^ξ
        Interval.create_point(BigDecimal.to_string(factorial))
    )
    Let remainder_term be Interval.multiply(
        remainder_bound,
        Interval.power(x_interval, terms)
    )
    
    Let result_with_error be Interval.add(sum, remainder_term)
    
    Return TaylorResult with:
        approximation: sum
        with_remainder_bound: result_with_error
        remainder_bound: remainder_term
        terms_used: terms

Let x_val be Interval.create_from_center_radius("1.0", "0.1")  Note: 1 ± 0.1
Let taylor_result be taylor_exp_with_bounds(x_val, 10)

Display "Taylor series for e^x with x ∈ [0.9, 1.1]:"
Display "  Approximation: " joined with Interval.to_string(taylor_result.approximation)
Display "  With error bound: " joined with Interval.to_string(taylor_result.with_remainder_bound)
Display "  Remainder bound: " joined with Interval.to_string(taylor_result.remainder_bound)

Note: Compare with built-in exp function
Let builtin_exp be Interval.exp(x_val)
Display "  Built-in exp: " joined with Interval.to_string(builtin_exp)
Let difference be Interval.subtract(taylor_result.with_remainder_bound, builtin_exp)
Display "  Difference: " joined with Interval.to_string(difference)
```

## Constraint Satisfaction

### Interval Constraint Propagation
```runa
Note: Solve systems of nonlinear constraints using interval propagation
Type called "Constraint":
    variables as Array[String]       Note: Variable names involved
    function as Process             Note: Constraint function
    gradient as Process             Note: Gradient for optimization

Process called "box_consistency_2b" that takes constraints as Array[Constraint], variable_boxes as Dictionary[String, Interval] returns ConstraintResult:
    Note: 2B-consistency algorithm for constraint propagation
    
    Let changed be true
    Let iterations be 0
    Let max_iterations be 100
    
    While changed and iterations < max_iterations:
        Set changed to false
        Set iterations to iterations + 1
        
        For Each constraint in constraints:
            For Each variable in constraint.variables:
                Let original_box be variable_boxes.get(variable)
                
                Note: Forward constraint propagation
                Let other_vars be constraint.variables.filter(v => v != variable)
                Let other_boxes be Dictionary[String, Interval]()
                
                For Each other_var in other_vars:
                    other_boxes.set(other_var, variable_boxes.get(other_var))
                
                Let projected_box be constraint.project_onto_variable(variable, other_boxes)
                Let intersected_box be Interval.intersect(original_box, projected_box)
                
                If Interval.width(intersected_box) < Interval.width(original_box):
                    variable_boxes.set(variable, intersected_box)
                    Set changed to true
                
                Note: Check for inconsistency
                If Interval.is_empty(intersected_box):
                    Return ConstraintResult with:
                        intervals: IntervalVector.from_dictionary(variable_boxes)
                        is_consistent: false
                        iterations: iterations
    
    Return ConstraintResult with:
        intervals: IntervalVector.from_dictionary(variable_boxes)
        is_consistent: true
        iterations: iterations

Note: Example: solve circle intersection
Let circle1_constraint be Constraint with:
    variables: Array[String](["x", "y"])
    function: Process that takes x as Interval, y as Interval returns Interval:
        Note: (x-2)² + (y-1)² = 4
        Let x_shifted be Interval.subtract(x, Interval.create_point("2"))
        Let y_shifted be Interval.subtract(y, Interval.create_point("1"))
        Return Interval.subtract(
            Interval.add(
                Interval.multiply(x_shifted, x_shifted),
                Interval.multiply(y_shifted, y_shifted)
            ),
            Interval.create_point("4")
        )

Let circle2_constraint be Constraint with:
    variables: Array[String](["x", "y"])
    function: Process that takes x as Interval, y as Interval returns Interval:
        Note: (x+1)² + (y-2)² = 9
        Let x_shifted be Interval.add(x, Interval.create_point("1"))
        Let y_shifted be Interval.subtract(y, Interval.create_point("2"))
        Return Interval.subtract(
            Interval.add(
                Interval.multiply(x_shifted, x_shifted),
                Interval.multiply(y_shifted, y_shifted)
            ),
            Interval.create_point("9")
        )

Let constraints be Array[Constraint]([circle1_constraint, circle2_constraint])
Let initial_boxes be Dictionary[String, Interval]()
initial_boxes.set("x", Interval.create_range("-5", "5"))
initial_boxes.set("y", Interval.create_range("-5", "5"))

Let constraint_result be box_consistency_2b(constraints, initial_boxes)

Display "Circle intersection constraint solving:"
Display "  Consistent: " joined with String(constraint_result.is_consistent)
Display "  Iterations: " joined with String(constraint_result.iterations)
If constraint_result.is_consistent:
    Display "  x ∈ " joined with Interval.to_string(constraint_result.intervals.get_component("x"))
    Display "  y ∈ " joined with Interval.to_string(constraint_result.intervals.get_component("y"))
```

### Branch and Bound Optimization
```runa
Note: Global optimization using interval branch-and-bound
Process called "interval_branch_bound" that takes objective as Process, constraints as Array[Constraint], search_box as IntervalVector, tolerance as BigDecimal returns OptimizationResult:
    Note: Global optimization with guaranteed bounds
    
    Let pending_boxes be PriorityQueue[IntervalVector]()  Note: Priority by lower bound
    pending_boxes.add(search_box)
    
    Let global_upper_bound be BigDecimal.create_from_string("1e100")
    Let best_box be IntervalVector.empty()
    Let certified_boxes be Array[IntervalVector]()
    
    While not pending_boxes.is_empty():
        Let current_box be pending_boxes.poll()
        
        Note: Evaluate objective function over box
        Let objective_interval be objective.evaluate_over_box(current_box)
        Let lower_bound be Interval.lower_bound(objective_interval)
        Let upper_bound be Interval.upper_bound(objective_interval)
        
        Note: Prune if lower bound exceeds current best
        If BigDecimal.compare(lower_bound, global_upper_bound) >= 0:
            Continue  Note: This box cannot contain global minimum
        
        Note: Update global upper bound
        If BigDecimal.compare(upper_bound, global_upper_bound) < 0:
            Set global_upper_bound to upper_bound
            Set best_box to current_box
        
        Note: Check for termination
        If BigDecimal.subtract(upper_bound, lower_bound) <= tolerance:
            certified_boxes.add(current_box)
            Continue
        
        Note: Branch: split largest component
        Let split_boxes be current_box.bisect_largest_component()
        
        For Each split_box in split_boxes:
            Note: Check constraints
            Let satisfies_constraints be true
            For Each constraint in constraints:
                If not constraint.is_consistent_with_box(split_box):
                    Set satisfies_constraints to false
                    Break
            
            If satisfies_constraints:
                pending_boxes.add(split_box)
    
    Return OptimizationResult with:
        global_minimum: Interval.create_range(String(global_lower_bound), String(global_upper_bound))
        minimizer_box: best_box
        upper_bound: global_upper_bound
        certified: certified_boxes.length > 0

Note: Minimize Rosenbrock function f(x,y) = 100(y-x²)² + (1-x)²
Let rosenbrock be Process that takes box as IntervalVector returns Interval:
    Let x be box.get_component(0)
    Let y be box.get_component(1)
    
    Let term1 be Interval.multiply(
        Interval.create_point("100"),
        Interval.multiply(
            Interval.subtract(y, Interval.multiply(x, x)),
            Interval.subtract(y, Interval.multiply(x, x))
        )
    )
    
    Let term2 be Interval.multiply(
        Interval.subtract(Interval.create_point("1"), x),
        Interval.subtract(Interval.create_point("1"), x)
    )
    
    Return Interval.add(term1, term2)

Let search_region be IntervalVector.create([
    Interval.create_range("-2", "2"),  Note: x ∈ [-2, 2]
    Interval.create_range("-2", "2")   Note: y ∈ [-2, 2]
])

Let optimization_result be interval_branch_bound(rosenbrock, Array[Constraint](), search_region, BigDecimal.create_from_string("1e-6"))

Display "Rosenbrock function global optimization:"
Display "  Global minimum ∈ " joined with Interval.to_string(optimization_result.global_minimum)
Display "  Minimizer box: " joined with IntervalVector.to_string(optimization_result.minimizer_box)
Display "  Certified result: " joined with String(optimization_result.certified)
```

## Numerical Integration

### Validated Integration
```runa
Note: Numerical integration with guaranteed error bounds
Process called "interval_simpson_rule" that takes f as Process, integration_interval as Interval, subdivisions as Integer returns IntegrationResult:
    Note: Simpson's rule with interval arithmetic for error bounds
    
    Let a be Interval.lower_bound(integration_interval)
    Let b be Interval.upper_bound(integration_interval)
    Let h be BigDecimal.divide(BigDecimal.subtract(b, a), BigDecimal.create_from_integer(subdivisions), 50)
    
    Let integral_sum be Interval.ZERO
    
    For i from 0 to subdivisions - 1:
        Let x0 be BigDecimal.add(a, BigDecimal.multiply(h, BigDecimal.create_from_integer(i), 50))
        Let x1 be BigDecimal.add(x0, BigDecimal.divide(h, BigDecimal.create_from_string("2"), 50))
        Let x2 be BigDecimal.add(x0, h)
        
        Note: Evaluate function at interval points to account for uncertainty
        Let f_x0 be f(Interval.create_point(BigDecimal.to_string(x0)))
        Let f_x1 be f(Interval.create_point(BigDecimal.to_string(x1)))
        Let f_x2 be f(Interval.create_point(BigDecimal.to_string(x2)))
        
        Note: Simpson's rule: (h/6)[f(x0) + 4f(x1) + f(x2)]
        Let simpson_term be Interval.multiply(
            Interval.divide(Interval.create_point(BigDecimal.to_string(h)), Interval.create_point("6")),
            Interval.add(
                f_x0,
                Interval.add(
                    Interval.multiply(Interval.create_point("4"), f_x1),
                    f_x2
                )
            )
        )
        
        Set integral_sum to Interval.add(integral_sum, simpson_term)
    
    Note: Estimate error using fourth derivative bound
    Let error_bound be estimate_simpson_error_bound(f, integration_interval, h)
    Let result_with_error be Interval.add(integral_sum, error_bound)
    
    Return IntegrationResult with:
        integral_value: integral_sum
        with_error_bound: result_with_error
        estimated_error: error_bound
        subdivisions_used: subdivisions

Note: Integrate x*sin(x) from 0 to π
Let integrand be Process that takes x as Interval returns Interval:
    Return Interval.multiply(x, Interval.sin(x))

Let integration_domain be Interval.create_range("0", "3.14159265358979323846")
Let integration_result be interval_simpson_rule(integrand, integration_domain, 1000)

Display "∫₀^π x·sin(x) dx with guaranteed bounds:"
Display "  Computed integral: " joined with Interval.to_string(integration_result.integral_value)
Display "  With error bound: " joined with Interval.to_string(integration_result.with_error_bound)
Display "  Error estimate: " joined with Interval.to_string(integration_result.estimated_error)

Note: Analytical result for comparison: ∫₀^π x·sin(x) dx = π
Let analytical_result = BigDecimal.create_from_string("3.14159265358979323846")
Display "  Analytical result: " joined with BigDecimal.to_string(analytical_result)
```

### Differential Equation Solving
```runa
Note: Solve ODEs with validated error bounds
Process called "interval_euler_method" that takes ode_function as Process, initial_condition as Interval, time_interval as Interval, step_size as BigDecimal returns ODESolution:
    Note: Euler method with interval arithmetic for IVP: y' = f(t,y), y(t0) = y0
    
    Let t_start be Interval.lower_bound(time_interval)
    Let t_end be Interval.upper_bound(time_interval)
    Let steps be Integer.ceiling(BigDecimal.divide(BigDecimal.subtract(t_end, t_start), step_size, 10))
    
    Let solution_points be Array[TimeValuePair]()
    Let current_t be t_start
    Let current_y be initial_condition
    
    solution_points.add(TimeValuePair with:
        time: current_t
        value: current_y
    )
    
    For i from 1 to steps:
        Let t_interval be Interval.create_point(BigDecimal.to_string(current_t))
        Let slope_interval be ode_function(t_interval, current_y)
        
        Note: Euler step: y_{n+1} = y_n + h * f(t_n, y_n)
        Let step_increment be Interval.multiply(
            Interval.create_point(BigDecimal.to_string(step_size)),
            slope_interval
        )
        
        Set current_y to Interval.add(current_y, step_increment)
        Set current_t to BigDecimal.add(current_t, step_size)
        
        solution_points.add(TimeValuePair with:
            time: current_t
            value: current_y
        )
    
    Return ODESolution with:
        solution_curve: solution_points
        final_value: current_y
        final_time: current_t
        guaranteed_bounds: true

Note: Solve y' = -y, y(0) = 1 (analytical solution: y = e^(-t))
Let exponential_decay be Process that takes t as Interval, y as Interval returns Interval:
    Return Interval.negate(y)

Let initial_value be Interval.create_from_measurement("1.0", "0.01")  Note: Slightly uncertain initial condition
Let time_span be Interval.create_range("0", "2")
Let ode_solution be interval_euler_method(exponential_decay, initial_value, time_span, BigDecimal.create_from_string("0.01"))

Display "ODE solution y' = -y, y(0) = 1±0.01:"
Display "  Final time: " joined with BigDecimal.to_string(ode_solution.final_time)
Display "  Final value: " joined with Interval.to_string(ode_solution.final_value)

Note: Compare with analytical solution at t=2: e^(-2) ≈ 0.1353
Let analytical_final be BigDecimal.create_from_string("0.1353352832366127")
Display "  Analytical y(2): " joined with BigDecimal.to_string(analytical_final)

Let contains_analytical be Interval.contains_point(ode_solution.final_value, analytical_final)
Display "  Contains analytical solution: " joined with String(contains_analytical)
```

## Set Operations and Comparisons

### Interval Set Operations
```runa
Note: Set-theoretic operations on intervals
Let interval1 be Interval.create_range("1.0", "5.0")
Let interval2 be Interval.create_range("3.0", "8.0")
Let interval3 be Interval.create_range("6.0", "10.0")

Let union_12 be Interval.union(interval1, interval2)
Let intersection_12 be Interval.intersect(interval1, interval2)
Let difference_12 be Interval.difference(interval1, interval2)

Display "Set operations on intervals:"
Display "  I₁ = " joined with Interval.to_string(interval1)
Display "  I₂ = " joined with Interval.to_string(interval2)
Display "  I₁ ∪ I₂ = " joined with Interval.to_string(union_12)
Display "  I₁ ∩ I₂ = " joined with Interval.to_string(intersection_12)

Note: Handle disjoint intervals
Let are_disjoint be Interval.are_disjoint(interval1, interval3)
Display "  I₁ and I₃ disjoint: " joined with String(are_disjoint)

If are_disjoint:
    Let disjoint_union be Interval.disjoint_union(interval1, interval3)
    Display "  I₁ ⊔ I₃ = " joined with IntervalUnion.to_string(disjoint_union)
```

### Containment and Comparison
```runa
Note: Interval containment and ordering relations
Let large_interval be Interval.create_range("0.0", "10.0")
Let small_interval be Interval.create_range("2.0", "4.0")
Let point_value be BigDecimal.create_from_string("3.5")

Let contains_interval be Interval.contains(large_interval, small_interval)
Let contains_point be Interval.contains_point(large_interval, point_value)
Let is_subset be Interval.is_subset(small_interval, large_interval)

Display "Containment relations:"
Display "  [0,10] contains [2,4]: " joined with String(contains_interval)
Display "  [0,10] contains 3.5: " joined with String(contains_point)
Display "  [2,4] ⊆ [0,10]: " joined with String(is_subset)

Note: Interval distance and separation
Let distance be Interval.distance(interval1, interval3)
Let hausdorff_distance be Interval.hausdorff_distance(interval1, interval2)

Display "Distance measures:"
Display "  Distance between I₁ and I₃: " joined with BigDecimal.to_string(distance)
Display "  Hausdorff distance I₁ and I₂: " joined with BigDecimal.to_string(hausdorff_distance)
```

## Error Handling

### Exception Types
The Interval module defines several specific exception types:

- **IntervalDomainError**: Operation outside function domain
- **IntervalDivisionByZero**: Division by interval containing zero
- **EmptyIntervalError**: Operation on empty interval
- **InconsistentConstraints**: Constraint system has no solution
- **ConvergenceError**: Numerical method failed to converge

### Error Handling Examples
```runa
Try:
    Let invalid_sqrt be Interval.sqrt(Interval.create_range("-2.0", "1.0"))
Catch Errors.IntervalDomainError as error:
    Display "Domain error: " joined with error.message
    Let positive_part be Interval.intersect(
        Interval.create_range("-2.0", "1.0"),
        Interval.create_range("0", "∞")
    )
    If not Interval.is_empty(positive_part):
        Let valid_sqrt be Interval.sqrt(positive_part)
        Display "Square root of positive part: " joined with Interval.to_string(valid_sqrt)

Try:
    Let empty_interval be Interval.create_empty()
    Let invalid_operation be Interval.add(empty_interval, interval1)
Catch Errors.EmptyIntervalError as error:
    Display "Empty interval error: " joined with error.message
    Display "Cannot perform arithmetic on empty intervals"
```

## Performance Optimization

### Efficient Interval Operations
```runa
Note: Optimize interval computations for performance
Let optimization_config be IntervalOptimizationConfig with:
    lazy_bound_computation: true
    precision_scaling: true
    caching_enabled: true
    parallel_operations: true

Interval.configure_optimization(optimization_config)

Note: Batch operations for multiple intervals
Let interval_array be Array[Interval]()
For i from 1 to 1000:
    interval_array.add(Interval.create_from_center_radius(String(i), "0.1"))

Let batch_sin_result be Interval.batch_sin(interval_array)
Let batch_statistics be Interval.compute_batch_statistics(interval_array)

Display "Batch operations completed:"
Display "  Processed intervals: " joined with String(interval_array.length)
Display "  Batch sin computed: " joined with String(batch_sin_result.length)
Display "  Mean width: " joined with BigDecimal.to_string(batch_statistics.mean_width)
```

### Memory Management
```runa
Note: Manage memory for large interval computations
Let memory_config be IntervalMemoryConfig with:
    precision_pooling: true
    bound_caching: true
    result_streaming: true
    garbage_collection_hints: true

Interval.configure_memory(memory_config)

Let memory_stats be Interval.get_memory_statistics()
Display "Interval memory usage:"
Display "  Active intervals: " joined with String(memory_stats.active_intervals)
Display "  Cached bounds: " joined with String(memory_stats.cached_bounds)
Display "  Memory allocated: " joined with String(memory_stats.bytes_allocated)
```

## Best Practices

### 1. Precision Management
```runa
Note: Guidelines for interval precision
Process called "recommend_interval_precision" that takes computation_type as String, input_precision as Integer returns Integer:
    If computation_type == "measurement_propagation":
        Return input_precision + 5  Note: Small buffer for uncertainty propagation
    Otherwise If computation_type == "global_optimization":
        Return input_precision + 20  Note: Need precision for convergence
    Otherwise If computation_type == "constraint_satisfaction":
        Return input_precision + 15  Note: Precision for consistency checking
    Otherwise:
        Return input_precision + 10  Note: Conservative default
```

### 2. Algorithm Selection  
```runa
Note: Choose appropriate interval methods
Process called "select_interval_method" that takes problem_type as String, dimension as Integer returns String:
    If problem_type == "constraint_satisfaction":
        If dimension <= 5:
            Return "2b_consistency"
        Otherwise:
            Return "hull_consistency"
    Otherwise If problem_type == "global_optimization":
        If dimension <= 10:
            Return "branch_and_bound"
        Otherwise:
            Return "evolutionary_interval"
    Otherwise:
        Return "standard_arithmetic"
```

### 3. Error Control
```runa
Note: Control numerical errors in interval computations
Process called "configure_error_control" that takes tolerance as BigDecimal returns ErrorControlConfig:
    Return ErrorControlConfig with:
        rounding_mode: "outward"  Note: Always round outward to preserve containment
        precision_tracking: true
        error_accumulation_limit: BigDecimal.multiply(tolerance, BigDecimal.create_from_string("0.1"))
        validation_checks: true
```

## Integration Examples

### With Other Precision Modules
```runa
Import "math/precision/interval" as Interval
Import "math/precision/bigdecimal" as BigDecimal
Import "math/precision/rational" as Rational

Note: Convert between precision types
Let rational_value be Rational.create(22, 7)  Note: π approximation
Let rational_error be Rational.create(1, 1000)  Note: ±0.001

Let interval_from_rational be Interval.create_from_rational_with_error(rational_value, rational_error)
Display "Rational with error as interval: " joined with Interval.to_string(interval_from_rational)

Note: High-precision interval bounds
Let precise_lower be BigDecimal.create_from_string("3.14159265358979323846264338327950288")
Let precise_upper be BigDecimal.create_from_string("3.14159265358979323846264338327950289")
Let precise_interval be Interval.create_from_bigdecimals(precise_lower, precise_upper)

Display "High-precision π interval: " joined with Interval.to_string(precise_interval)
```

### Scientific Applications
```runa
Note: Physics calculation with measurement uncertainty
Process called "calculate_pendulum_period" that takes length as Interval, gravity as Interval returns PendulumResult:
    Note: T = 2π√(L/g)
    Let two_pi be Interval.create_from_bigdecimal(
        BigDecimal.multiply(BigDecimal.create_from_string("2"), Constants.get_pi(50), 50)
    )
    
    Let length_over_gravity be Interval.divide(length, gravity)
    Let sqrt_term be Interval.sqrt(length_over_gravity)
    Let period be Interval.multiply(two_pi, sqrt_term)
    
    Let period_uncertainty be Interval.subtract(
        Interval.upper_bound(period),
        Interval.lower_bound(period)
    )
    
    Return PendulumResult with:
        period: period
        absolute_uncertainty: period_uncertainty
        relative_uncertainty: Interval.divide(period_uncertainty, Interval.midpoint(period))

Let pendulum_length be Interval.create_from_measurement("1.000", "0.005")  Note: 1m ± 5mm
Let local_gravity be Interval.create_from_measurement("9.807", "0.003")    Note: g ± 0.003 m/s²

Let pendulum_calculation be calculate_pendulum_period(pendulum_length, local_gravity)

Display "Pendulum period calculation:"
Display "  Period: " joined with Interval.to_string(pendulum_calculation.period) joined with " seconds"
Display "  Uncertainty: ±" joined with BigDecimal.to_string(pendulum_calculation.absolute_uncertainty) joined with " s"
Display "  Relative uncertainty: " joined with BigDecimal.to_string(pendulum_calculation.relative_uncertainty) joined with "%"
```

## Testing and Validation

### Interval Property Verification
```runa
Note: Test fundamental interval arithmetic properties
Process called "test_interval_properties" returns Boolean:
    Let all_tests_pass be true
    
    Note: Test containment property
    Let x be Interval.create_range("2.0", "3.0")
    Let y be Interval.create_range("1.5", "2.5")
    Let sum be Interval.add(x, y)
    
    Note: Check that x + y contains all possible sums
    Let min_sum be BigDecimal.create_from_string("3.5")  Note: 2.0 + 1.5
    Let max_sum be BigDecimal.create_from_string("5.5")  Note: 3.0 + 2.5
    
    If not (Interval.contains_point(sum, min_sum) and Interval.contains_point(sum, max_sum)):
        Display "Containment property test failed"
        Set all_tests_pass to false
    
    Note: Test subdistributivity: X ∩ (Y ∪ Z) ⊆ (X ∩ Y) ∪ (X ∩ Z)
    Let X be Interval.create_range("1.0", "4.0")
    Let Y be Interval.create_range("2.0", "3.0")
    Let Z be Interval.create_range("3.5", "5.0")
    
    Let Y_union_Z be Interval.union(Y, Z)
    Let left_side be Interval.intersect(X, Y_union_Z)
    
    Let X_cap_Y be Interval.intersect(X, Y)
    Let X_cap_Z be Interval.intersect(X, Z)
    Let right_side be Interval.union(X_cap_Y, X_cap_Z)
    
    If not Interval.is_subset(left_side, right_side):
        Display "Subdistributivity test failed"
        Set all_tests_pass to false
    
    Return all_tests_pass

Let property_tests_pass be test_interval_properties()
Display "Interval property tests: " joined with String(property_tests_pass)
```

The Interval module provides rigorous mathematical foundations for computing with uncertainty, enabling applications in scientific computing, engineering analysis, global optimization, and mathematical verification where guaranteed bounds and error control are essential.