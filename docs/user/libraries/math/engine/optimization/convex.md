# Convex Optimization

The Convex Optimization module (`math/engine/optimization/convex`) provides specialized algorithms for convex optimization problems, including linear programming, quadratic programming, semidefinite programming, and general convex optimization methods.

## Overview

This module implements state-of-the-art algorithms that exploit the mathematical structure of convex problems to achieve global optimality guarantees and polynomial-time complexity.

## Key Algorithms

### Linear Programming

#### Simplex Method
```runa
Import "math/engine/optimization/convex" as ConvexOpt

Note: Solve standard form LP: minimize c^T x subject to Ax = b, x ≥ 0
Let c_vector be LinAlg.create_vector([3.0, 2.0, 0.0, 0.0])  Note: Objective coefficients
Let A_matrix be LinAlg.create_matrix([
    [1.0, 1.0, 1.0, 0.0],  Note: Constraint matrix
    [2.0, 1.0, 0.0, 1.0]
])
Let b_vector be LinAlg.create_vector([4.0, 6.0])  Note: RHS

Let simplex_config be ConvexOpt.create_simplex_config([
    ("pivot_rule", "bland"),
    ("tolerance", 1e-8),
    ("max_iterations", 1000)
])

Let simplex_result be ConvexOpt.simplex_solve(
    c_vector,
    A_matrix,
    b_vector,
    simplex_config
)

Let optimal_solution be ConvexOpt.get_lp_solution(simplex_result)
Let optimal_value be ConvexOpt.get_lp_value(simplex_result)
Let dual_solution be ConvexOpt.get_dual_solution(simplex_result)

Display "LP Solution: " joined with LinAlg.vector_to_string(optimal_solution)
Display "Optimal value: " joined with optimal_value
Display "Dual solution: " joined with LinAlg.vector_to_string(dual_solution)
```

#### Interior Point Method for LP
```runa
Let ip_lp_config be ConvexOpt.create_interior_point_lp_config([
    ("barrier_parameter", 0.1),
    ("centering_parameter", 0.1),
    ("tolerance", 1e-8),
    ("max_iterations", 100)
])

Let ip_lp_result be ConvexOpt.interior_point_lp_solve(
    c_vector,
    A_matrix,
    b_vector,
    ip_lp_config
)

Let ip_solution be ConvexOpt.get_lp_solution(ip_lp_result)
Let ip_iterations be ConvexOpt.get_iterations(ip_lp_result)

Display "Interior Point LP Solution: " joined with LinAlg.vector_to_string(ip_solution)
Display "Converged in " joined with ip_iterations joined with " iterations"
```

### Quadratic Programming

#### Active Set Method
```runa
Note: Solve QP: minimize (1/2)x^T Q x + c^T x subject to Ax ≤ b, Aeq x = beq
Let Q_matrix be LinAlg.create_matrix([
    [2.0, 0.0],
    [0.0, 2.0]
])
Let c_qp_vector be LinAlg.create_vector([0.0, 0.0])

Let A_inequality be LinAlg.create_matrix([
    [1.0, 1.0],   Note: x1 + x2 ≤ 1
    [-1.0, 0.0],  Note: -x1 ≤ 0 (x1 ≥ 0)
    [0.0, -1.0]   Note: -x2 ≤ 0 (x2 ≥ 0)
])
Let b_inequality be LinAlg.create_vector([1.0, 0.0, 0.0])

Let active_set_config be ConvexOpt.create_active_set_config([
    ("tolerance", 1e-8),
    ("max_iterations", 100),
    ("feasibility_tolerance", 1e-8)
])

Let qp_result be ConvexOpt.active_set_qp_solve(
    Q_matrix,
    c_qp_vector,
    A_inequality,
    b_inequality,
    equality_matrix: None,
    equality_rhs: None,
    active_set_config
)

Let qp_solution be ConvexOpt.get_qp_solution(qp_result)
Let active_constraints be ConvexOpt.get_active_constraints(qp_result)
Let lagrange_multipliers be ConvexOpt.get_qp_multipliers(qp_result)

Display "QP Solution: " joined with LinAlg.vector_to_string(qp_solution)
Display "Active constraints: " joined with ConvexOpt.format_constraint_set(active_constraints)
Display "Lagrange multipliers: " joined with LinAlg.vector_to_string(lagrange_multipliers)
```

#### Interior Point Method for QP
```runa
Let ip_qp_config be ConvexOpt.create_interior_point_qp_config([
    ("barrier_parameter", 1.0),
    ("reduction_factor", 0.1),
    ("tolerance", 1e-8),
    ("max_iterations", 50)
])

Let ip_qp_result be ConvexOpt.interior_point_qp_solve(
    Q_matrix,
    c_qp_vector,
    A_inequality,
    b_inequality,
    ip_qp_config
)

Let ip_qp_solution be ConvexOpt.get_qp_solution(ip_qp_result)
Let barrier_path be ConvexOpt.get_barrier_path(ip_qp_result)

Display "Interior Point QP Solution: " joined with LinAlg.vector_to_string(ip_qp_solution)
Display "Barrier iterations: " joined with ConvexOpt.count_barrier_iterations(barrier_path)
```

### Semidefinite Programming

#### SDPA Interior Point Method
```runa
Note: Solve SDP: minimize C • X subject to A_i • X = b_i, X ⪰ 0
Let C_sdp be LinAlg.create_symmetric_matrix([
    [1.0, 0.0],
    [0.0, 1.0]
])

Let A1_constraint be LinAlg.create_symmetric_matrix([
    [1.0, 0.0],
    [0.0, 0.0]
])
Let A2_constraint be LinAlg.create_symmetric_matrix([
    [0.0, 1.0],
    [1.0, 0.0]
])

Let constraint_matrices be [A1_constraint, A2_constraint]
Let constraint_rhs be LinAlg.create_vector([1.0, 0.0])

Let sdp_config be ConvexOpt.create_sdp_config([
    ("barrier_parameter", 1.0),
    ("tolerance", 1e-6),
    ("max_iterations", 100),
    ("eigenvalue_tolerance", 1e-10)
])

Let sdp_result be ConvexOpt.sdp_solve(
    C_sdp,
    constraint_matrices,
    constraint_rhs,
    sdp_config
)

Let X_optimal be ConvexOpt.get_sdp_solution(sdp_result)
Let sdp_value be ConvexOpt.get_sdp_value(sdp_result)
Let dual_variables be ConvexOpt.get_sdp_dual(sdp_result)

Display "SDP Solution X*:"
LinAlg.display_matrix(X_optimal)
Display "Optimal value: " joined with sdp_value
Display "Dual variables: " joined with LinAlg.vector_to_string(dual_variables)

Note: Verify positive semidefiniteness
Let eigenvalues be LinAlg.eigenvalues(X_optimal)
Let is_psd be ConvexOpt.verify_positive_semidefinite(eigenvalues)
Display "Solution is PSD: " joined with is_psd
```

### General Convex Optimization

#### Barrier Methods
```runa
Process called "convex_objective" that takes x as List[String] returns Float:
    Let x1 be MathCore.parse_float(x[0])
    Let x2 be MathCore.parse_float(x[1])
    Return x1 * x1 + x2 * x2  Note: Minimize sum of squares

Process called "inequality_constraints" that takes x as List[String] returns List[Float]:
    Let x1 be MathCore.parse_float(x[0])
    Let x2 be MathCore.parse_float(x[1])
    Return [
        1.0 - x1 - x2,   Note: x1 + x2 ≤ 1
        x1,              Note: x1 ≥ 0
        x2               Note: x2 ≥ 0
    ]

Let barrier_config be ConvexOpt.create_barrier_method_config([
    ("initial_barrier_parameter", 1.0),
    ("barrier_reduction_factor", 0.1),
    ("tolerance", 1e-8),
    ("max_barrier_iterations", 20),
    ("max_newton_iterations", 50)
])

Let barrier_result be ConvexOpt.barrier_method_solve(
    convex_objective,
    inequality_constraints,
    initial_point: ["0.1", "0.1"],
    barrier_config
)

Let barrier_solution be ConvexOpt.get_barrier_solution(barrier_result)
Let barrier_iterations be ConvexOpt.get_barrier_iterations(barrier_result)

Display "Barrier Method Solution: [" joined with barrier_solution[0] 
    joined with ", " joined with barrier_solution[1] joined with "]"
Display "Barrier iterations: " joined with barrier_iterations
```

#### Penalty Methods
```runa
Process called "equality_constraints" that takes x as List[String] returns List[Float]:
    Let x1 be MathCore.parse_float(x[0])
    Let x2 be MathCore.parse_float(x[1])
    Return [x1 + x2 - 1.0]  Note: x1 + x2 = 1

Let penalty_config be ConvexOpt.create_penalty_method_config([
    ("initial_penalty_parameter", 1.0),
    ("penalty_increase_factor", 10.0),
    ("tolerance", 1e-8),
    ("max_penalty_iterations", 10),
    ("unconstrained_solver", "bfgs")
])

Let penalty_result be ConvexOpt.penalty_method_solve(
    convex_objective,
    equality_constraints,
    inequality_constraints,
    initial_point: ["0.5", "0.5"],
    penalty_config
)

Let penalty_solution be ConvexOpt.get_penalty_solution(penalty_result)
Let penalty_violations be ConvexOpt.get_constraint_violations(penalty_result)

Display "Penalty Method Solution: [" joined with penalty_solution[0] 
    joined with ", " joined with penalty_solution[1] joined with "]"
Display "Final constraint violation: " joined with 
    ConvexOpt.max_violation(penalty_violations)
```

#### Augmented Lagrangian Method
```runa
Let augmented_lagrangian_config be ConvexOpt.create_augmented_lagrangian_config([
    ("initial_penalty_parameter", 1.0),
    ("penalty_increase_factor", 2.0),
    ("lagrange_multiplier_tolerance", 1e-6),
    ("constraint_tolerance", 1e-8),
    ("max_outer_iterations", 20)
])

Let al_result be ConvexOpt.augmented_lagrangian_solve(
    convex_objective,
    equality_constraints,
    inequality_constraints,
    initial_point: ["0.5", "0.5"],
    augmented_lagrangian_config
)

Let al_solution be ConvexOpt.get_al_solution(al_result)
Let al_multipliers be ConvexOpt.get_al_multipliers(al_result)
Let al_convergence = ConvexOpt.get_al_convergence_history(al_result)

Display "Augmented Lagrangian Solution: [" joined with al_solution[0] 
    joined with ", " joined with al_solution[1] joined with "]"
Display "Final multipliers: " joined with LinAlg.vector_to_string(al_multipliers)
```

### Subgradient Methods

```runa
Process called "nonsmooth_objective" that takes x as List[String] returns Float:
    Let x1 be MathCore.parse_float(x[0])
    Let x2 be MathCore.parse_float(x[1])
    Return MathCore.max([MathCore.abs(x1), MathCore.abs(x2)])  Note: L∞ norm

Process called "subgradient_oracle" that takes x as List[String] returns List[String]:
    Let x1 be MathCore.parse_float(x[0])
    Let x2 be MathCore.parse_float(x[1])
    
    Note: Subgradient of max{|x1|, |x2|}
    Let abs_x1 be MathCore.abs(x1)
    Let abs_x2 be MathCore.abs(x2)
    
    If abs_x1 > abs_x2:
        Let subgrad_x1 be MathCore.sign(x1)
        Let subgrad_x2 be 0.0
    Otherwise If abs_x2 > abs_x1:
        Let subgrad_x1 be 0.0
        Let subgrad_x2 be MathCore.sign(x2)
    Otherwise:
        Note: Non-unique subgradient case
        Let subgrad_x1 be MathCore.sign(x1)
        Let subgrad_x2 be MathCore.sign(x2)
    
    Return [MathCore.float_to_string(subgrad_x1), MathCore.float_to_string(subgrad_x2)]

Let subgradient_config be ConvexOpt.create_subgradient_config([
    ("step_size_rule", "diminishing"),
    ("initial_step_size", 1.0),
    ("tolerance", 1e-6),
    ("max_iterations", 10000)
])

Let subgradient_result be ConvexOpt.subgradient_method(
    nonsmooth_objective,
    subgradient_oracle,
    initial_point: ["2.0", "1.0"],
    subgradient_config
)

Let subgradient_solution be ConvexOpt.get_subgradient_solution(subgradient_result)
Let subgradient_convergence be ConvexOpt.get_subgradient_convergence(subgradient_result)

Display "Subgradient Method Solution: [" joined with subgradient_solution[0] 
    joined with ", " joined with subgradient_solution[1] joined with "]"
Display "Convergence rate: " joined with 
    ConvexOpt.estimate_convergence_rate(subgradient_convergence)
```

## Advanced Features

### Duality Analysis
```runa
Note: Analyze primal-dual relationships
Let duality_analyzer be ConvexOpt.create_duality_analyzer()

Let primal_problem be ConvexOpt.create_primal_problem([
    ("objective", convex_objective),
    ("equality_constraints", equality_constraints),
    ("inequality_constraints", inequality_constraints)
])

Let dual_problem be ConvexOpt.construct_dual_problem(duality_analyzer, primal_problem)
Let duality_gap_bound be ConvexOpt.compute_duality_gap_bound(primal_problem, dual_problem)

Display "Theoretical duality gap bound: " joined with duality_gap_bound

Note: Solve both primal and dual
Let primal_solution be ConvexOpt.solve_primal(primal_problem)
Let dual_solution be ConvexOpt.solve_dual(dual_problem)

Let actual_duality_gap be ConvexOpt.compute_duality_gap(primal_solution, dual_solution)
Display "Actual duality gap: " joined with actual_duality_gap

Let strong_duality be ConvexOpt.verify_strong_duality(primal_solution, dual_solution)
Display "Strong duality holds: " joined with strong_duality
```

### Sensitivity Analysis
```runa
Note: Analyze solution sensitivity to parameter changes
Let sensitivity_analyzer be ConvexOpt.create_sensitivity_analyzer([
    ("perturbation_size", 1e-6),
    ("parameters_to_analyze", ["objective_coefficients", "constraint_rhs"]),
    ("finite_difference_method", "central")
])

Let sensitivity_result be ConvexOpt.sensitivity_analysis(
    qp_result,
    sensitivity_analyzer,
    Q_matrix,
    c_qp_vector,
    A_inequality,
    b_inequality
)

Let objective_sensitivity be ConvexOpt.get_objective_sensitivity(sensitivity_result)
Let constraint_sensitivity be ConvexOpt.get_constraint_sensitivity(sensitivity_result)

Display "Sensitivity to objective changes: " joined with 
    LinAlg.vector_to_string(objective_sensitivity)
Display "Sensitivity to constraint RHS: " joined with 
    LinAlg.vector_to_string(constraint_sensitivity)
```

### Warm Starting
```runa
Note: Use previous solution as starting point for related problem
Let perturbed_c = LinAlg.add_vector(c_qp_vector, LinAlg.create_vector([0.1, -0.05]))

Let warm_start_config be ConvexOpt.create_warm_start_config([
    ("use_previous_solution", True),
    ("use_previous_multipliers", True),
    ("use_previous_active_set", True)
])

Let warm_started_result be ConvexOpt.active_set_qp_solve_warm_start(
    Q_matrix,
    perturbed_c,
    A_inequality,
    b_inequality,
    previous_result: qp_result,
    warm_start_config
)

Let warm_iterations be ConvexOpt.get_iterations(warm_started_result)
Let cold_start_iterations be ConvexOpt.get_iterations(qp_result)

Display "Warm start iterations: " joined with warm_iterations
Display "Cold start iterations: " joined with cold_start_iterations
Display "Speedup: " joined with (MathCore.int_to_float(cold_start_iterations) / 
    MathCore.int_to_float(warm_iterations)) joined with "x"
```

## Error Handling and Robustness

### Infeasibility Detection
```runa
Note: Handle infeasible problems gracefully
Let infeasible_A be LinAlg.create_matrix([
    [1.0, 1.0],
    [1.0, 1.0]
])
Let infeasible_b be LinAlg.create_vector([1.0, 2.0])  Note: Inconsistent system

Let infeasibility_result be ConvexOpt.detect_infeasibility(
    infeasible_A,
    infeasible_b,
    tolerance: 1e-8
)

If ConvexOpt.is_infeasible(infeasibility_result):
    Let infeasibility_certificate be ConvexOpt.get_infeasibility_certificate(infeasibility_result)
    Display "Problem is infeasible"
    Display "Farkas certificate: " joined with LinAlg.vector_to_string(infeasibility_certificate)
    
    Note: Suggest minimum norm correction
    Let minimum_correction be ConvexOpt.compute_minimum_infeasibility_correction(
        infeasible_A,
        infeasible_b
    )
    Display "Minimum correction to RHS: " joined with LinAlg.vector_to_string(minimum_correction)
Otherwise:
    Display "Problem appears feasible"
```

### Unboundedness Detection
```runa
Let unbounded_c be LinAlg.create_vector([-1.0, -1.0])  Note: Minimize -x1 - x2
Let unbounded_A be LinAlg.create_matrix([[1.0, -1.0]])  Note: x1 - x2 = 0
Let unbounded_b be LinAlg.create_vector([0.0])

Let unboundedness_result be ConvexOpt.detect_unboundedness(
    unbounded_c,
    unbounded_A,
    unbounded_b
)

If ConvexOpt.is_unbounded(unboundedness_result):
    Let unbounded_direction be ConvexOpt.get_unbounded_direction(unboundedness_result)
    Display "Problem is unbounded"
    Display "Unbounded direction: " joined with LinAlg.vector_to_string(unbounded_direction)
Otherwise:
    Display "Problem appears bounded"
```

## Performance Optimization

### Presolving
```runa
Let presolve_config be ConvexOpt.create_presolve_config([
    ("eliminate_fixed_variables", True),
    ("eliminate_redundant_constraints", True),
    ("detect_implied_bounds", True),
    ("scale_problem", True)
])

Let presolved_problem be ConvexOpt.presolve_problem(
    c_vector,
    A_matrix,
    b_vector,
    presolve_config
)

Let reduction_statistics be ConvexOpt.get_presolve_statistics(presolved_problem)
Display "Variables eliminated: " joined with 
    ConvexOpt.get_eliminated_variables(reduction_statistics)
Display "Constraints eliminated: " joined with 
    ConvexOpt.get_eliminated_constraints(reduction_statistics)

Let presolved_result be ConvexOpt.simplex_solve_presolved(presolved_problem, simplex_config)
Let original_solution be ConvexOpt.transform_solution_to_original(presolved_result, presolved_problem)
```

### Parallel Processing
```runa
Let parallel_config be ConvexOpt.create_parallel_config([
    ("num_threads", 4),
    ("parallel_matrix_operations", True),
    ("parallel_constraint_evaluation", True)
])

ConvexOpt.enable_parallel_processing(parallel_config)

Let parallel_result be ConvexOpt.interior_point_qp_solve_parallel(
    Q_matrix,
    c_qp_vector,
    A_inequality,
    b_inequality,
    ip_qp_config
)

Let parallel_speedup be ConvexOpt.measure_parallel_speedup(parallel_result)
Display "Parallel speedup: " joined with parallel_speedup joined with "x"
```

## Best Practices

### Problem Formulation
- Ensure strict convexity for unique solutions
- Use appropriate scaling for numerical stability
- Exploit problem structure (sparsity, separability)
- Verify constraint qualifications for duality

### Algorithm Selection
- **Linear Programming**: Interior point for large dense problems, simplex for small problems
- **Quadratic Programming**: Interior point for large problems, active set for warm starting
- **General Convex**: Barrier methods for smooth problems, subgradient for non-smooth
- **Semidefinite Programming**: Specialized SDP solvers for matrix optimization

### Numerical Considerations
- Monitor condition numbers and scaling
- Use regularization for ill-conditioned problems
- Implement iterative refinement for high accuracy
- Handle degeneracy and near-degeneracy carefully

This module provides comprehensive convex optimization capabilities with theoretical guarantees and robust numerical implementations suitable for operations research, machine learning, and engineering applications.