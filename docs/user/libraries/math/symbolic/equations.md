# Symbolic Equation Solving

The Symbolic Equations module (`math/symbolic/equations`) provides comprehensive symbolic equation solving and analysis systems. This module enables solving linear and nonlinear equations, systems of equations, differential equations, and specialized mathematical equations using symbolic methods.

## Overview

The Symbolic Equations module offers powerful equation solving capabilities including:

- **Linear Systems**: Gaussian elimination, Cramer's rule, and matrix-based solving
- **Polynomial Equations**: Quadratic, cubic, quartic formulas and higher-degree solving
- **Transcendental Equations**: Symbolic and numerical hybrid approaches
- **Differential Equations**: ODE and PDE symbolic solution methods
- **Constraint Systems**: Multi-variable constraint satisfaction
- **Parametric Solutions**: Solutions with parameters and free variables
- **Equation Manipulation**: Transformation, substitution, and simplification

## Core Data Structures

### Equation Representation

```runa
Type called "Equation":
    left_side as String                    # Left-hand side expression
    right_side as String                   # Right-hand side expression
    equation_type as String               # linear, polynomial, transcendental, etc.
    variables as List[String]             # Variables in the equation
    parameters as List[String]            # Parameters (treated as constants)
    domain_constraints as Dictionary[String, String] # Variable domain restrictions
    equation_id as String                 # Unique identifier
```

### Solution Set Representation

```runa
Type called "EquationSolution":
    solutions as List[Dictionary[String, String]]    # Variable assignments
    solution_type as String              # exact, approximate, parametric
    free_parameters as List[String]      # Unconstrained parameters
    constraints as List[String]          # Additional solution constraints
    existence_conditions as List[String] # Conditions for solution existence
    multiplicity as Dictionary[String, Integer] # Solution multiplicities
    verification_status as String        # verified, unverified, failed
```

## Linear Equation Systems

### Single Linear Equations

```runa
Import "math/symbolic/equations" as Equations

Note: Solve simple linear equations
Let linear_eq be Equations.create_equation("3*x + 7 = 2*x - 5")
Let solution be Equations.solve_linear_equation(linear_eq, "x")

Display "Equation: " joined with Equations.equation_to_string(linear_eq)
Display "Solution: x = " joined with solution.solutions[0]["x"]

Note: Linear equations with parameters
Let parametric_linear be Equations.create_equation("a*x + b = c*x + d")
Let parametric_solution be Equations.solve_linear_equation(parametric_linear, "x")

Display "Parametric solution: x = " joined with parametric_solution.solutions[0]["x"]
Display "Existence condition: " joined with parametric_solution.existence_conditions[0]
```

### Systems of Linear Equations

```runa
Note: Solve system using matrix methods
Let system be [
    Equations.create_equation("2*x + 3*y - z = 1"),
    Equations.create_equation("x - 2*y + 4*z = -2"),
    Equations.create_equation("3*x + y + 2*z = 3")
]

Let matrix_solution be Equations.solve_linear_system(system, ["x", "y", "z"], Dictionary with:
    "method": "gaussian_elimination"
    "pivot_strategy": "partial"
)

Display "System solution:"
Display "x = " joined with matrix_solution.solutions[0]["x"]
Display "y = " joined with matrix_solution.solutions[0]["y"]
Display "z = " joined with matrix_solution.solutions[0]["z"]

Note: Analyze system properties
Let system_properties be Equations.analyze_linear_system(system)
Display "System rank: " joined with String(system_properties.coefficient_rank)
Display "Augmented rank: " joined with String(system_properties.augmented_rank)
Display "Solution type: " joined with system_properties.solution_classification
```

### Homogeneous Systems

```runa
Note: Solve homogeneous systems
Let homogeneous_system be [
    Equations.create_equation("2*x + 3*y - z = 0"),
    Equations.create_equation("x - y + 2*z = 0"),
    Equations.create_equation("3*x + 2*y + z = 0")
]

Let homogeneous_solution be Equations.solve_homogeneous_system(homogeneous_system, ["x", "y", "z"])

Display "Homogeneous system solution:"
If Length(homogeneous_solution.free_parameters) > 0:
    Display "Free parameters: " joined with StringOps.join(homogeneous_solution.free_parameters, ", ")
    Display "General solution:"
    For Each var in ["x", "y", "z"]:
        Display "  " joined with var joined with " = " joined with homogeneous_solution.solutions[0][var]
Otherwise:
    Display "Only trivial solution: x = y = z = 0"

Note: Find null space basis
Let null_space_basis be Equations.compute_null_space(homogeneous_system)
Display "Null space dimension: " joined with String(Length(null_space_basis))
For Each i, basis_vector in null_space_basis:
    Display "Basis vector " joined with String(i+1) joined with ": " joined with StringOps.join(basis_vector, ", ")
```

### Cramer's Rule

```runa
Note: Apply Cramer's rule for square systems
Let square_system be [
    Equations.create_equation("2*x + y = 5"),
    Equations.create_equation("x - 3*y = -1")
]

Let cramer_solution be Equations.solve_by_cramers_rule(square_system, ["x", "y"])

Display "Cramer's rule solution:"
Display "Main determinant: " joined with cramer_solution.main_determinant
Display "x determinant: " joined with cramer_solution.variable_determinants["x"]
Display "y determinant: " joined with cramer_solution.variable_determinants["y"]
Display "x = " joined with cramer_solution.solutions[0]["x"]
Display "y = " joined with cramer_solution.solutions[0]["y"]
```

## Polynomial Equations

### Quadratic Equations

```runa
Note: Solve quadratic equations
Let quadratic be Equations.create_equation("x^2 - 5*x + 6 = 0")
Let quad_solution be Equations.solve_quadratic(quadratic, "x")

Display "Quadratic equation: " joined with Equations.equation_to_string(quadratic)
Display "Solutions:"
For Each solution in quad_solution.solutions:
    Display "  x = " joined with solution["x"]

Note: Quadratic formula with parameters
Let parametric_quadratic be Equations.create_equation("a*x^2 + b*x + c = 0")
Let param_quad_solution be Equations.solve_quadratic(parametric_quadratic, "x")

Display "General quadratic solution: x = " joined with param_quad_solution.solutions[0]["x"]
Display "Discriminant: " joined with param_quad_solution.discriminant
```

### Cubic Equations

```runa
Note: Solve cubic equations using Cardano's formula
Let cubic be Equations.create_equation("x^3 - 6*x^2 + 11*x - 6 = 0")
Let cubic_solution be Equations.solve_cubic(cubic, "x")

Display "Cubic equation: " joined with Equations.equation_to_string(cubic)
Display "Solutions:"
For Each solution in cubic_solution.solutions:
    Display "  x = " joined with solution["x"]
    
Display "Nature of roots: " joined with cubic_solution.root_classification

Note: Depressed cubic form
Let depressed_form be Equations.depress_cubic(cubic, "x")
Display "Depressed cubic: " joined with Equations.equation_to_string(depressed_form.equation)
Display "Substitution used: " joined with depressed_form.substitution
```

### Quartic Equations

```runa
Note: Solve quartic equations using Ferrari's method
Let quartic be Equations.create_equation("x^4 - 4*x^3 + 6*x^2 - 4*x + 1 = 0")
Let quartic_solution be Equations.solve_quartic(quartic, "x")

Display "Quartic equation: " joined with Equations.equation_to_string(quartic)
Display "Solutions:"
For Each solution in quartic_solution.solutions:
    Display "  x = " joined with solution["x"]

Note: Resolvent cubic
Let resolvent = Equations.compute_resolvent_cubic(quartic, "x")
Display "Resolvent cubic: " joined with Equations.equation_to_string(resolvent.equation)
Display "Resolvent solutions: " joined with StringOps.join(resolvent.roots, ", ")
```

### Higher-Degree Polynomials

```runa
Note: Attempt symbolic solutions for higher degrees
Let quintic be Equations.create_equation("x^5 - x - 1 = 0")
Let general_solution_attempt be Equations.attempt_symbolic_solution(quintic, "x")

If general_solution_attempt.has_symbolic_solution:
    Display "Symbolic solution found:"
    For Each solution in general_solution_attempt.solutions:
        Display "  x = " joined with solution["x"]
Otherwise:
    Display "No general symbolic solution available"
    Display "Reason: " joined with general_solution_attempt.impossibility_reason
    
    Note: Try special methods
    Let special_methods be Equations.try_special_polynomial_methods(quintic, "x")
    If Length(special_methods.applicable_methods) > 0:
        Display "Applicable special methods:"
        For Each method in special_methods.applicable_methods:
            Display "  " joined with method.name joined with ": " joined with method.description

Note: Rational root theorem
Let rational_candidates be Equations.rational_root_candidates("x^3 - 2*x^2 - 5*x + 6 = 0")
Display "Rational root candidates: " joined with StringOps.join(rational_candidates, ", ")

Let rational_roots be Equations.find_rational_roots("x^3 - 2*x^2 - 5*x + 6 = 0", rational_candidates)
Display "Actual rational roots: " joined with StringOps.join(rational_roots, ", ")
```

## Transcendental Equations

### Exponential Equations

```runa
Note: Solve exponential equations
Let exp_equation be Equations.create_equation("2^x = 8")
Let exp_solution be Equations.solve_exponential(exp_equation, "x")

Display "Exponential equation: " joined with Equations.equation_to_string(exp_equation)
Display "Solution: x = " joined with exp_solution.solutions[0]["x"]

Note: More complex exponential equations
Let complex_exp be Equations.create_equation("3^x - 2^x = 1")
Let complex_exp_solution be Equations.solve_transcendental(complex_exp, "x", Dictionary with:
    "method": "lambert_w"
    "symbolic_first": "true"
})

If complex_exp_solution.has_exact_solution:
    Display "Exact solution: x = " joined with complex_exp_solution.solutions[0]["x"]
Otherwise:
    Display "Approximate solution: x ≈ " joined with complex_exp_solution.approximate_solutions[0]["x"]
    Display "Method used: " joined with complex_exp_solution.method_used
```

### Logarithmic Equations

```runa
Note: Solve logarithmic equations
Let log_equation be Equations.create_equation("log(x) + log(x-1) = log(6)")
Let log_solution be Equations.solve_logarithmic(log_equation, "x")

Display "Logarithmic equation: " joined with Equations.equation_to_string(log_equation)
Display "Solution: x = " joined with log_solution.solutions[0]["x"]

Note: Check domain validity
Let domain_check be Equations.verify_logarithmic_domain(log_equation, log_solution)
Display "Solution satisfies domain constraints: " joined with String(domain_check.valid)

Note: Base conversion equations
Let base_conversion_eq be Equations.create_equation("log_2(x) = log_3(9)")
Let converted_solution be Equations.solve_with_base_conversion(base_conversion_eq, "x")

Display "Base conversion equation solution: x = " joined with converted_solution.solutions[0]["x"]
```

### Trigonometric Equations

```runa
Note: Solve trigonometric equations
Let trig_equation be Equations.create_equation("sin(x) = 1/2")
Let trig_solution be Equations.solve_trigonometric(trig_equation, "x", Dictionary with:
    "angle_mode": "radians"
    "general_solution": "true"
})

Display "Trigonometric equation: " joined with Equations.equation_to_string(trig_equation)
Display "General solution: x = " joined with trig_solution.general_form
Display "Principal solutions: " joined with StringOps.join(trig_solution.principal_values, ", ")

Note: Multiple angle equations
Let multiple_angle = Equations.create_equation("sin(2*x) + cos(x) = 0")
Let ma_solution be Equations.solve_trigonometric(multiple_angle, "x")

Display "Multiple angle equation solutions:"
For Each solution in ma_solution.solutions:
    Display "  x = " joined with solution["x"]
```

## Systems of Nonlinear Equations

### Polynomial Systems

```runa
Note: Solve polynomial systems
Let nonlinear_system be [
    Equations.create_equation("x^2 + y^2 = 25"),
    Equations.create_equation("x*y = 12")
]

Let system_solution be Equations.solve_polynomial_system(nonlinear_system, ["x", "y"], Dictionary with:
    "method": "groebner_basis"
    "ordering": "lexicographic"
})

Display "Polynomial system solutions:"
For Each solution in system_solution.solutions:
    Display "  (x, y) = (" joined with solution["x"] joined with ", " joined with solution["y"] joined with ")"

Note: Analyze solution geometry
Let geometric_analysis be Equations.analyze_solution_geometry(nonlinear_system)
Display "Intersection type: " joined with geometric_analysis.intersection_type
Display "Number of intersections: " joined with String(geometric_analysis.intersection_count)
```

### Mixed Systems

```runa
Note: Systems with different equation types
Let mixed_system be [
    Equations.create_equation("x^2 + y^2 = r^2"),    Note: Circle
    Equations.create_equation("y = m*x + b")         Note: Line
]

Let mixed_solution be Equations.solve_mixed_system(mixed_system, ["x", "y"], ["r", "m", "b"])

Display "Mixed system (circle-line intersection):"
Display "Solutions in terms of parameters:"
For Each solution in mixed_solution.solutions:
    Display "  x = " joined with solution["x"]
    Display "  y = " joined with solution["y"]

Note: Discriminant analysis
Let discriminant_analysis be Equations.analyze_intersection_discriminant(mixed_system)
Display "Discriminant: " joined with discriminant_analysis.discriminant
Display "Geometric interpretation: " joined with discriminant_analysis.interpretation
```

## Differential Equations

### First-Order ODEs

```runa
Note: Separable differential equations
Let separable_ode be Equations.create_differential_equation("dy/dx = y*sin(x)")
Let separable_solution be Equations.solve_separable_ode(separable_ode, "y", "x")

Display "Separable ODE: " joined with separable_ode.equation_string
Display "General solution: " joined with separable_solution.general_solution
Display "Integration constant: " joined with separable_solution.constants[0]

Note: Linear first-order ODEs
Let linear_ode = Equations.create_differential_equation("dy/dx + 2*y = 3*exp(-x)")
Let linear_solution be Equations.solve_linear_first_order(linear_ode, "y", "x")

Display "Linear first-order ODE solution:"
Display "Integrating factor: " joined with linear_solution.integrating_factor
Display "General solution: " joined with linear_solution.general_solution
```

### Second-Order ODEs

```runa
Note: Homogeneous linear second-order ODEs
Let homogeneous_ode = Equations.create_differential_equation("d²y/dx² - 3*dy/dx + 2*y = 0")
Let homo_solution be Equations.solve_homogeneous_linear_ode(homogeneous_ode, "y", "x", 2)

Display "Homogeneous second-order ODE: " joined with homogeneous_ode.equation_string
Display "Characteristic equation: " joined with homo_solution.characteristic_equation
Display "Characteristic roots: " joined with StringOps.join(homo_solution.characteristic_roots, ", ")
Display "General solution: " joined with homo_solution.general_solution

Note: Non-homogeneous ODEs with constant coefficients
Let nonhomogeneous_ode = Equations.create_differential_equation("d²y/dx² - 4*y = 2*exp(x)")
Let nonhomo_solution be Equations.solve_nonhomogeneous_linear_ode(nonhomogeneous_ode, "y", "x")

Display "Non-homogeneous solution:"
Display "Homogeneous part: " joined with nonhomo_solution.homogeneous_solution
Display "Particular solution: " joined with nonhomo_solution.particular_solution
Display "General solution: " joined with nonhomo_solution.general_solution
```

### Partial Differential Equations

```runa
Note: Solve PDEs using separation of variables
Let heat_pde = Equations.create_partial_differential_equation("∂u/∂t = α²*(∂²u/∂x²)")
Let pde_solution be Equations.solve_pde_separation(heat_pde, "u", ["x", "t"], Dictionary with:
    "boundary_conditions": [
        "u(0, t) = 0",
        "u(L, t) = 0"
    ],
    "initial_condition": "u(x, 0) = f(x)",
    "separation_assumption": "u(x,t) = X(x)*T(t)"
})

Display "Heat equation solution:"
Display "Separated form: " joined with pde_solution.separated_equations["X"]
Display "Time evolution: " joined with pde_solution.separated_equations["T"]  
Display "General solution: " joined with pde_solution.general_solution

Note: Wave equation
Let wave_pde = Equations.create_partial_differential_equation("∂²u/∂t² = c²*(∂²u/∂x²)")
Let wave_solution be Equations.solve_wave_equation(wave_pde, "u", ["x", "t"])

Display "Wave equation d'Alembert solution: " joined with wave_solution.dalembert_form
Display "Standing wave solutions: " joined with wave_solution.standing_wave_form
```

## Constraint Systems

### Optimization with Constraints

```runa
Note: Lagrange multiplier method
Let objective be "x^2 + y^2"
Let constraint = Equations.create_equation("x + y = 1")

Let lagrange_system be Equations.setup_lagrange_multipliers(
    objective, 
    [constraint], 
    ["x", "y"]
)

Let constrained_solution be Equations.solve_lagrange_system(lagrange_system)

Display "Constrained optimization:"
Display "Objective: minimize " joined with objective
Display "Subject to: " joined with Equations.equation_to_string(constraint)
Display "Critical point: (" joined with constrained_solution.solutions[0]["x"] joined with ", " joined with constrained_solution.solutions[0]["y"] joined with ")"
Display "Lagrange multiplier: λ = " joined with constrained_solution.solutions[0]["λ"]

Note: Multiple constraints
Let multi_constraint_system be [
    Equations.create_equation("x + y + z = 1"),
    Equations.create_equation("x^2 + y^2 = 2")
]

Let multi_lagrange = Equations.setup_lagrange_multipliers(
    "x*y*z",
    multi_constraint_system,
    ["x", "y", "z"]
)

Let multi_solution be Equations.solve_lagrange_system(multi_lagrange)
Display "Multi-constraint solution found: " joined with String(multi_solution.has_solution)
```

### Inequality Constraints

```runa
Note: Systems with inequalities
Let inequality_system be [
    Equations.create_inequality("x^2 + y^2 <= 9"),
    Equations.create_inequality("x + y >= 1"),
    Equations.create_inequality("x >= 0"),
    Equations.create_inequality("y >= 0")
]

Let feasible_region be Equations.analyze_feasible_region(inequality_system, ["x", "y"])

Display "Feasible region analysis:"
Display "Region type: " joined with feasible_region.region_type
Display "Bounded: " joined with String(feasible_region.is_bounded)
Display "Vertices: " joined with StringOps.join(feasible_region.vertices, "; ")

Note: Linear programming
Let linear_objective be "3*x + 2*y"
Let lp_solution be Equations.solve_linear_program(
    linear_objective,
    inequality_system,
    ["x", "y"],
    "maximize"
)

Display "Linear programming solution:"
Display "Optimal point: (" joined with lp_solution.optimal_point["x"] joined with ", " joined with lp_solution.optimal_point["y"] joined with ")"
Display "Optimal value: " joined with lp_solution.optimal_value
```

## Diophantine Equations

### Linear Diophantine Equations

```runa
Note: Solve linear Diophantine equations
Let diophantine = Equations.create_equation("15*x + 10*y = 5")
Let diophantine_solution be Equations.solve_linear_diophantine(diophantine, ["x", "y"])

Display "Linear Diophantine equation: " joined with Equations.equation_to_string(diophantine)
If diophantine_solution.has_integer_solutions:
    Display "Particular solution: x = " joined with diophantine_solution.particular_solution["x"]
    Display "                     y = " joined with diophantine_solution.particular_solution["y"]
    Display "General solution: x = " joined with diophantine_solution.general_solution["x"]
    Display "                  y = " joined with diophantine_solution.general_solution["y"]
Otherwise:
    Display "No integer solutions exist"
    Display "GCD condition: gcd(15,10) = " joined with diophantine_solution.gcd joined with " does not divide 5"
```

### Quadratic Diophantine Equations

```runa
Note: Pell's equation
Let pell_equation = Equations.create_equation("x^2 - D*y^2 = 1")
Let pell_solution be Equations.solve_pell_equation("D", Dictionary with:
    "find_fundamental": "true"
    "generate_solutions": "10"
})

Display "Pell equation x² - Dy² = 1:"
Display "Fundamental solution: (" joined with pell_solution.fundamental_solution["x"] joined with ", " joined with pell_solution.fundamental_solution["y"] joined with ")"
Display "First few solutions:"
For Each i, solution in pell_solution.solutions:
    If i < 5:
        Display "  (" joined with solution["x"] joined with ", " joined with solution["y"] joined with ")"

Note: Pythagorean triples
Let pythagorean = Equations.create_equation("x^2 + y^2 = z^2")
Let pythagorean_triples be Equations.generate_pythagorean_triples(Dictionary with:
    "max_value": "100"
    "primitive_only": "true"
})

Display "Primitive Pythagorean triples (z ≤ 100):"
For Each triple in pythagorean_triples:
    Display "  (" joined with triple["x"] joined with ", " joined with triple["y"] joined with ", " joined with triple["z"] joined with ")"
```

## Advanced Equation Types

### Functional Equations

```runa
Note: Solve functional equations
Let functional_eq = Equations.create_functional_equation("f(x + y) = f(x) + f(y)")
Let functional_solution be Equations.solve_functional_equation(functional_eq, "f")

Display "Functional equation: " joined with functional_eq.equation_string
Display "General solution: f(x) = " joined with functional_solution.general_form
Display "Regularity assumptions: " joined with StringOps.join(functional_solution.assumptions, ", ")

Note: Recurrence relations
Let recurrence = Equations.create_recurrence_relation("a(n) = 2*a(n-1) + 3*a(n-2)")
Let recurrence_solution be Equations.solve_linear_recurrence(recurrence, "a", Dictionary with:
    "initial_conditions": ["a(0) = 1", "a(1) = 2"]
})

Display "Recurrence relation solution:"
Display "Characteristic equation: " joined with recurrence_solution.characteristic_equation
Display "General solution: a(n) = " joined with recurrence_solution.general_solution
Display "With initial conditions: a(n) = " joined with recurrence_solution.particular_solution
```

### Matrix Equations

```runa
Note: Solve matrix equations
Let matrix_equation = Equations.create_matrix_equation("A*X + X*B = C")
Let sylvester_solution be Equations.solve_sylvester_equation(matrix_equation, "X")

Display "Sylvester equation A*X + X*B = C"
If sylvester_solution.has_unique_solution:
    Display "Unique solution exists"
    Display "Solution method: " joined with sylvester_solution.method
Otherwise:
    Display "No unique solution"
    Display "Solvability condition: " joined with sylvester_solution.solvability_condition

Note: Eigenvalue equations
Let eigenvalue_eq = Equations.create_equation("A*v = λ*v")
Let eigenvalue_solution be Equations.solve_eigenvalue_equation(eigenvalue_eq, ["v", "λ"])

Display "Eigenvalue problem solution:"
Display "Characteristic polynomial: " joined with eigenvalue_solution.characteristic_polynomial
Display "Eigenvalues: " joined with StringOps.join(eigenvalue_solution.eigenvalues, ", ")
```

## Solution Verification

### Automatic Verification

```runa
Note: Verify solutions automatically
Let equation = Equations.create_equation("x^3 - 6*x^2 + 11*x - 6 = 0")
Let solutions = Equations.solve_polynomial(equation, "x")

For Each solution in solutions.solutions:
    Let verification = Equations.verify_solution(equation, solution)
    Display "Solution x = " joined with solution["x"]
    Display "Verification: " joined with String(verification.is_valid)
    Display "Substitution result: " joined with verification.substitution_result
    Display "Error: " joined with verification.error_estimate
```

### Precision Control

```runa
Note: Control precision in verification
Let precision_config = Dictionary with:
    "symbolic_verification": "true"
    "numerical_tolerance": "1e-50"
    "exact_arithmetic": "true"

Let high_precision_verification = Equations.verify_solution_precise(
    equation, 
    solutions.solutions[0], 
    precision_config
)

Display "High-precision verification:"
Display "Symbolic result: " joined with high_precision_verification.symbolic_result
Display "Exact match: " joined with String(high_precision_verification.exact_match)
```

## Error Handling

### Equation Solving Errors

```runa
Try:
    Let problematic_equation = Equations.create_equation("0*x = 5")
    Let impossible_solution = Equations.solve_linear_equation(problematic_equation, "x")
    
Catch Errors.InconsistentEquationError as inconsistent_error:
    Display "Inconsistent equation: " joined with inconsistent_error.message
    Display "Left side simplifies to: " joined with inconsistent_error.simplified_left
    Display "Right side simplifies to: " joined with inconsistent_error.simplified_right
    Display "Conclusion: No solution exists"

Catch Errors.IndeterminateEquationError as indeterminate_error:
    Display "Indeterminate equation: " joined with indeterminate_error.message
    Display "Infinitely many solutions exist"
    Display "General form: " joined with indeterminate_error.general_solution
```

### Domain and Range Validation

```runa
Try:
    Let domain_restricted = Equations.create_equation("log(x-2) = 3")
    Let solution_with_domain = Equations.solve_equation_with_domain_check(domain_restricted, "x")
    
    Display "Solution: x = " joined with solution_with_domain.solutions[0]["x"]
    Display "Domain check passed: " joined with String(solution_with_domain.domain_valid)
    
Catch Errors.DomainViolationError as domain_error:
    Display "Domain violation: " joined with domain_error.message
    Display "Invalid value: " joined with domain_error.invalid_value
    Display "Required domain: " joined with domain_error.required_domain
```

## Performance Optimization

### Algorithm Selection

```runa
Note: Choose optimal algorithms based on equation characteristics
Let equation_analyzer = Equations.create_equation_analyzer()
Let analysis = equation_analyzer.analyze_equation("x^5 - 2*x^3 + x - 1 = 0")

Display "Equation analysis:"
Display "Degree: " joined with String(analysis.degree)
Display "Type: " joined with analysis.equation_type
Display "Recommended methods: " joined with StringOps.join(analysis.recommended_methods, ", ")

Let optimized_solution = Equations.solve_with_optimal_method(equation, analysis.recommended_methods[0])
Display "Solution using " joined with analysis.recommended_methods[0] joined with ":"
Display "Computation time: " joined with String(optimized_solution.computation_time) joined with " ms"
```

### Parallel Solving

```runa
Note: Solve large systems in parallel
Let large_system = Equations.generate_random_linear_system(1000, 1000)
Let parallel_config = Dictionary with:
    "enable_parallel": "true"
    "thread_count": "8"
    "block_size": "100"

Let parallel_solution = Equations.solve_linear_system_parallel(large_system, parallel_config)
Display "Large system solved in parallel: " joined with String(parallel_solution.success)
Display "Solution time: " joined with String(parallel_solution.elapsed_time) joined with " seconds"
Display "Threads used: " joined with String(parallel_solution.threads_used)
```

## Related Documentation

- **[Symbolic Core](core.md)**: Expression representation and manipulation
- **[Symbolic Algebra](algebra.md)**: Algebraic operations and polynomial manipulation  
- **[Symbolic Calculus](calculus.md)**: Differential equation solving methods
- **[Linear Algebra Engine](../engine/linalg/README.md)**: Matrix operations and decompositions
- **[Numerical Root Finding](../engine/numerical/rootfinding.md)**: Numerical equation solving methods
- **[Optimization Engine](../engine/optimization/README.md)**: Constrained optimization algorithms

The Symbolic Equations module provides comprehensive equation solving capabilities ranging from simple linear equations to complex differential equations and constraint systems. Its symbolic approach enables exact solutions while providing fallback numerical methods for cases where symbolic solutions are not available.