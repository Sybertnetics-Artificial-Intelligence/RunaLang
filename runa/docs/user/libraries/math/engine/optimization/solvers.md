# Linear and Quadratic Solvers

The Solvers module (`math/engine/optimization/solvers`) provides specialized algorithms for linear programming, quadratic programming, mixed-integer programming, and network optimization problems.

## Overview

This module implements production-quality solvers for structured optimization problems with polynomial-time guarantees and robust numerical implementations.

## Key Features

### Linear Programming Solvers
- Revised simplex method with advanced pivoting rules
- Dual simplex method for sensitivity analysis
- Interior point methods for large-scale problems
- Network simplex for transportation problems

### Quadratic Programming Solvers  
- Active set methods with warm-starting capabilities
- Interior point methods for convex QP
- Sequential quadratic programming for nonconvex QP
- Gradient projection methods for bound-constrained QP

### Mixed-Integer Programming
- Branch-and-bound with intelligent branching strategies
- Cutting plane methods for strengthening relaxations
- Heuristic methods for finding good solutions quickly
- Presolving and problem reduction techniques

### Specialized Problem Types
- Transportation and assignment problems
- Network flow optimization
- Shortest path and minimum spanning tree
- Maximum flow and minimum cut problems

## Quick Start Example

```runa
Import "math/engine/optimization/solvers" as Solvers

Note: Solve linear program: minimize 3x₁ + 2x₂ subject to constraints
Let lp_problem be Solvers.create_lp_problem([
    ("objective", [3.0, 2.0]),
    ("constraint_matrix", [
        [1.0, 1.0],  Note: x₁ + x₂ ≤ 4
        [2.0, 1.0]   Note: 2x₁ + x₂ ≤ 6
    ]),
    ("constraint_rhs", [4.0, 6.0]),
    ("constraint_types", ["<=", "<="]),
    ("variable_bounds", [(0.0, "inf"), (0.0, "inf")])
])

Let lp_result be Solvers.solve_lp(lp_problem, method: "interior_point")
Let solution be Solvers.get_solution(lp_result)
Let optimal_value be Solvers.get_objective_value(lp_result)

Display "LP Solution: [" joined with solution[0] joined with ", " joined with solution[1] joined with "]"
Display "Optimal value: " joined with optimal_value
```

## Best Practices

### Problem Formulation
- Use standard forms when possible for better numerical stability
- Scale variables and constraints to similar magnitudes
- Exploit sparsity patterns in constraint matrices
- Add regularization for ill-conditioned problems

### Solver Selection
- **Small dense problems**: Simplex method
- **Large sparse problems**: Interior point methods
- **Network problems**: Specialized network algorithms
- **Integer problems**: Branch-and-bound with presolving

This module provides industrial-strength optimization solvers suitable for operations research, supply chain optimization, and resource allocation problems.