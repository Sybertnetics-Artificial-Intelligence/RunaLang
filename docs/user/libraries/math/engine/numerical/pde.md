# Partial Differential Equations (PDE) Module

The `math/engine/numerical/pde` module provides comprehensive numerical methods for solving partial differential equations. This module supports elliptic, parabolic, and hyperbolic PDEs using finite difference, finite element, and spectral methods.

## Quick Start

```runa
Import "math/engine/numerical/pde" as PDE

Note: Solve 2D Laplace equation: ∇²u = 0
Let laplace_problem be PDE.LaplaceProblem:
    domain: PDE.Rectangle(width: 1.0, height: 1.0)
    grid_size: (101, 101)
    boundary_conditions: PDE.DirichletBC(
        left: 0.0,
        right: 1.0,
        bottom: 0.0,
        top: 0.0
    )

Let solution be PDE.solve_elliptic(laplace_problem, method: "finite_difference")
Display "Maximum solution value: " joined with solution.maximum()
```

## Core Concepts

### PDE Classification
- **Elliptic PDEs**: Steady-state problems (Laplace, Poisson equations)
- **Parabolic PDEs**: Time-dependent diffusion problems (Heat equation)
- **Hyperbolic PDEs**: Wave-like phenomena (Wave equation, transport)

### Numerical Methods
- **Finite Difference**: Discretize derivatives using difference approximations
- **Finite Element**: Variational formulation with basis functions
- **Spectral Methods**: Global polynomial approximations

### Boundary Conditions
- **Dirichlet**: Specify function values on boundary
- **Neumann**: Specify derivative values on boundary
- **Robin/Mixed**: Linear combination of function and derivative values

## API Reference

### Domain and Grid Definition

#### Rectangular Domains
```runa
Type called "Rectangle":
    width as Real
    height as Real
    origin as Tuple[Real, Real]

Process called "create_uniform_grid" that takes:
    domain as Rectangle,
    nx as Integer,
    ny as Integer
returns Grid2D:
    Note: Create uniform rectangular grid
```

#### Irregular Domains
```runa
Type called "Polygon":
    vertices as List[Tuple[Real, Real]]
    holes as List[List[Tuple[Real, Real]]]

Process called "create_triangular_mesh" that takes:
    domain as Polygon,
    max_element_size as Real
returns TriangularMesh:
    Note: Generate triangular mesh for finite element methods
```

### Boundary Condition Types

#### Dirichlet Boundary Conditions
```runa
Type called "DirichletBC":
    boundary_values as Dictionary[String, Real]
    boundary_functions as Dictionary[String, Process]

Process called "apply_dirichlet_bc" that takes:
    grid as Grid2D,
    bc as DirichletBC,
    solution_vector as List[Real]
returns List[Real]:
    Note: Apply Dirichlet boundary conditions to solution
```

#### Neumann Boundary Conditions
```runa
Type called "NeumannBC":
    boundary_derivatives as Dictionary[String, Real]
    boundary_flux_functions as Dictionary[String, Process]

Process called "apply_neumann_bc" that takes:
    grid as Grid2D,
    bc as NeumannBC,
    system_matrix as Matrix,
    rhs_vector as List[Real]
returns Tuple[Matrix, List[Real]]:
    Note: Modify system for Neumann boundary conditions
```

#### Robin Boundary Conditions
```runa
Type called "RobinBC":
    alpha_coefficients as Dictionary[String, Real]
    beta_coefficients as Dictionary[String, Real]
    boundary_values as Dictionary[String, Real]

Note: Robin BC: α*u + β*(∂u/∂n) = g on boundary
```

### Elliptic PDE Solvers

#### Laplace Equation
```runa
Type called "LaplaceProblem":
    domain as Rectangle
    grid_size as Tuple[Integer, Integer]
    boundary_conditions as DirichletBC

Process called "solve_laplace_2d" that takes:
    problem as LaplaceProblem,
    method as String
returns Matrix:
    Note: Solve ∇²u = 0 using specified numerical method
```

#### Poisson Equation
```runa
Type called "PoissonProblem":
    domain as Rectangle
    grid_size as Tuple[Integer, Integer]
    source_function as Process that takes Real, Real returns Real
    boundary_conditions as BoundaryCondition

Process called "solve_poisson_2d" that takes:
    problem as PoissonProblem,
    method as String
returns Matrix:
    Note: Solve ∇²u = f(x,y) using finite differences
```

#### General Elliptic PDEs
```runa
Process called "solve_elliptic_general" that takes:
    coefficients as Dictionary[String, Process],
    source_term as Process that takes Real, Real returns Real,
    domain as Domain,
    boundary_conditions as BoundaryCondition,
    method as String
returns PDESolution:
    Note: Solve general elliptic PDE: a*uxx + b*uxy + c*uyy + d*ux + e*uy + f*u = g
```

### Parabolic PDE Solvers

#### Heat Equation
```runa
Type called "HeatEquation":
    domain as Rectangle
    thermal_diffusivity as Real
    initial_condition as Process that takes Real, Real returns Real
    boundary_conditions as BoundaryCondition
    time_span as Tuple[Real, Real]

Process called "solve_heat_equation" that takes:
    problem as HeatEquation,
    spatial_grid_size as Tuple[Integer, Integer],
    time_step as Real,
    method as String
returns List[Matrix]:
    Note: Solve ∂u/∂t = α*∇²u using finite differences
```

#### Advection-Diffusion Equation
```runa
Type called "AdvectionDiffusion":
    domain as Rectangle
    velocity_field as Tuple[Process, Process]  Note: (vx, vy) functions
    diffusion_coefficient as Real
    initial_condition as Process that takes Real, Real returns Real
    boundary_conditions as BoundaryCondition

Process called "solve_advection_diffusion" that takes:
    problem as AdvectionDiffusion,
    spatial_discretization as SpatialDiscretization,
    time_discretization as TimeDiscretization,
    method as String
returns List[Matrix]:
    Note: Solve ∂u/∂t + v·∇u = D*∇²u
```

### Hyperbolic PDE Solvers

#### Wave Equation
```runa
Type called "WaveEquation":
    domain as Rectangle
    wave_speed as Real
    initial_displacement as Process that takes Real, Real returns Real
    initial_velocity as Process that takes Real, Real returns Real
    boundary_conditions as BoundaryCondition

Process called "solve_wave_equation" that takes:
    problem as WaveEquation,
    spatial_grid as Tuple[Integer, Integer],
    time_step as Real,
    final_time as Real,
    method as String
returns List[Matrix]:
    Note: Solve ∂²u/∂t² = c²*∇²u using finite differences
```

#### Transport Equation
```runa
Process called "solve_transport_1d" that takes:
    velocity as Real,
    initial_condition as Process that takes Real returns Real,
    domain as Tuple[Real, Real],
    boundary_condition as BoundaryCondition,
    grid_size as Integer,
    time_step as Real,
    final_time as Real,
    method as String
returns List[List[Real]]:
    Note: Solve ∂u/∂t + v*∂u/∂x = 0
```

### Finite Element Methods

#### Basis Functions
```runa
Type called "LinearTriangleElement":
    vertices as List[Tuple[Real, Real]]
    element_id as Integer

Process called "evaluate_basis_function" that takes:
    element as LinearTriangleElement,
    local_coordinates as Tuple[Real, Real],
    basis_index as Integer
returns Real:
    Note: Evaluate linear basis function on triangular element
```

#### Assembly Process
```runa
Process called "assemble_stiffness_matrix" that takes:
    mesh as TriangularMesh,
    coefficient_function as Process that takes Real, Real returns Real
returns Matrix:
    Note: Assemble global stiffness matrix for finite element method

Process called "assemble_mass_matrix" that takes:
    mesh as TriangularMesh
returns Matrix:
    Note: Assemble global mass matrix for time-dependent problems
```

### Spectral Methods

#### Fourier Spectral Method
```runa
Process called "fourier_spectral_solver" that takes:
    pde_coefficients as Dictionary[String, Process],
    boundary_conditions as PeriodicBC,
    domain as Rectangle,
    num_modes as Tuple[Integer, Integer]
returns Matrix:
    Note: Solve PDE using Fourier series expansion
```

#### Chebyshev Spectral Method
```runa
Process called "chebyshev_spectral_solver" that takes:
    pde_coefficients as Dictionary[String, Process],
    boundary_conditions as BoundaryCondition,
    domain as Rectangle,
    polynomial_degree as Integer
returns Matrix:
    Note: Solve PDE using Chebyshev polynomial expansion
```

## Practical Examples

### Steady-State Heat Conduction
```runa
Import "math/engine/numerical/pde" as PDE
Import "math/engine/numerical/core" as Numerical

Note: Solve heat conduction in a square plate
Note: Left side at 100°C, other sides at 0°C

Process called "zero_source" that takes x as Real, y as Real returns Real:
    Return 0.0

Let heat_problem be PDE.PoissonProblem:
    domain: PDE.Rectangle(width: 1.0, height: 1.0, origin: (0.0, 0.0))
    grid_size: (51, 51)
    source_function: zero_source
    boundary_conditions: PDE.DirichletBC(
        left: 100.0,
        right: 0.0,
        bottom: 0.0,
        top: 0.0
    )

Let temperature_field be PDE.solve_poisson_2d(heat_problem, method: "finite_difference")

Note: Extract temperature along centerline
Let centerline_temps be []
Let grid_y be Numerical.linspace(0.0, 1.0, 51)
For i from 0 to 50:
    centerline_temps.append(temperature_field[25][i])

Display "Temperature at center: " joined with temperature_field[25][25]
Display "Maximum temperature: " joined with Numerical.maximum(temperature_field)
```

### Time-Dependent Diffusion
```runa
Note: Solve heat equation with initial temperature distribution
Process called "initial_temperature" that takes x as Real, y as Real returns Real:
    Let center_x be 0.5
    Let center_y be 0.5
    Let radius_squared be (x - center_x) * (x - center_x) + (y - center_y) * (y - center_y)
    If radius_squared < 0.1:
        Return 100.0
    Otherwise:
        Return 0.0

Let diffusion_problem be PDE.HeatEquation:
    domain: PDE.Rectangle(width: 1.0, height: 1.0)
    thermal_diffusivity: 0.1
    initial_condition: initial_temperature
    boundary_conditions: PDE.DirichletBC(
        left: 0.0, right: 0.0, bottom: 0.0, top: 0.0
    )
    time_span: (0.0, 1.0)

Let time_evolution be PDE.solve_heat_equation(
    diffusion_problem,
    spatial_grid_size: (41, 41),
    time_step: 0.001,
    method: "implicit_euler"
)

Note: Analyze temperature decay over time
For t from 0 to time_evolution.length() - 1:
    Let current_temp_field be time_evolution[t]
    Let max_temp be Numerical.maximum(current_temp_field)
    Let time_value be t * 0.001
    If t % 100 == 0:
        Display "t = " joined with time_value joined with ", max T = " joined with max_temp
```

### Wave Propagation
```runa
Note: Simulate wave in 2D membrane
Process called "initial_displacement" that takes x as Real, y as Real returns Real:
    Let amplitude be 1.0
    Let sigma be 0.1
    Let center_x be 0.5
    Let center_y be 0.5
    Let r_squared be (x - center_x) * (x - center_x) + (y - center_y) * (y - center_y)
    Return amplitude * Numerical.exp(-r_squared / (2.0 * sigma * sigma))

Process called "zero_velocity" that takes x as Real, y as Real returns Real:
    Return 0.0

Let wave_problem be PDE.WaveEquation:
    domain: PDE.Rectangle(width: 2.0, height: 2.0, origin: (0.0, 0.0))
    wave_speed: 1.0
    initial_displacement: initial_displacement
    initial_velocity: zero_velocity
    boundary_conditions: PDE.DirichletBC(
        left: 0.0, right: 0.0, bottom: 0.0, top: 0.0
    )

Let wave_solution be PDE.solve_wave_equation(
    wave_problem,
    spatial_grid: (101, 101),
    time_step: 0.001,
    final_time: 2.0,
    method: "leapfrog"
)

Note: Track energy conservation
Let initial_energy be PDE.calculate_wave_energy(wave_solution[0], wave_problem)
Let final_energy be PDE.calculate_wave_energy(wave_solution[-1], wave_problem)
Let energy_error be abs(final_energy - initial_energy) / initial_energy

Display "Energy conservation error: " joined with energy_error
```

### Finite Element Example
```runa
Note: Solve Poisson equation on L-shaped domain using finite elements
Let L_shape_vertices be [
    (0.0, 0.0), (1.0, 0.0), (1.0, 0.5), (0.5, 0.5),
    (0.5, 1.0), (0.0, 1.0), (0.0, 0.0)
]

Let L_domain be PDE.Polygon:
    vertices: L_shape_vertices
    holes: []

Let triangular_mesh be PDE.create_triangular_mesh(L_domain, max_element_size: 0.05)

Process called "source_term" that takes x as Real, y as Real returns Real:
    Return -2.0  Note: Constant source term

Let fe_problem be PDE.PoissonProblem:
    domain: L_domain
    mesh: triangular_mesh
    source_function: source_term
    boundary_conditions: PDE.DirichletBC(boundary_value: 0.0)  Note: Homogeneous Dirichlet

Let fe_solution be PDE.solve_poisson_fem(fe_problem)

Note: Post-process solution
Let solution_at_point be PDE.evaluate_fem_solution(fe_solution, point: (0.25, 0.25))
Display "Solution at (0.25, 0.25): " joined with solution_at_point

Let gradient_at_point be PDE.evaluate_fem_gradient(fe_solution, point: (0.25, 0.25))
Display "Gradient magnitude: " joined with Numerical.norm(gradient_at_point)
```

### Spectral Method Example
```runa
Note: Solve 2D Poisson equation using Fourier spectral method
Note: Periodic boundary conditions in both directions

Process called "periodic_source" that takes x as Real, y as Real returns Real:
    Let pi be 3.14159265358979323846
    Return Numerical.sin(2.0 * pi * x) * Numerical.sin(2.0 * pi * y)

Let spectral_problem be PDE.SpectralProblem:
    domain: PDE.Rectangle(width: 1.0, height: 1.0)
    source_function: periodic_source
    boundary_conditions: PDE.PeriodicBC()
    num_modes: (64, 64)

Let spectral_solution be PDE.fourier_spectral_solver(spectral_problem)

Note: Transform back to physical space
Let physical_solution be PDE.inverse_fourier_transform(spectral_solution)

Note: Verify analytical solution (if known)
Process called "analytical_solution" that takes x as Real, y as Real returns Real:
    Let pi be 3.14159265358979323846
    Let k_squared be 8.0 * pi * pi
    Return -Numerical.sin(2.0 * pi * x) * Numerical.sin(2.0 * pi * y) / k_squared

Let error_field be PDE.compute_solution_error(physical_solution, analytical_solution)
Let max_error be Numerical.maximum(error_field)
Display "Maximum error: " joined with max_error
```

## Advanced Features

### Adaptive Mesh Refinement
```runa
Process called "adaptive_refinement" that takes:
    current_mesh as TriangularMesh,
    solution as List[Real],
    error_estimator as Process,
    refinement_threshold as Real
returns TriangularMesh:
    Note: Refine mesh based on local error estimates
```

### Multigrid Solvers
```runa
Process called "multigrid_v_cycle" that takes:
    system_matrix as Matrix,
    rhs_vector as List[Real],
    initial_guess as List[Real],
    num_levels as Integer
returns List[Real]:
    Note: V-cycle multigrid iteration for fast solving
```

### Parallel Processing
```runa
Process called "parallel_pde_solve" that takes:
    problem as PDEProblem,
    num_processors as Integer,
    domain_decomposition as String
returns PDESolution:
    Note: Solve PDE using domain decomposition parallelization
```

## Integration with Other Modules

### With Linear Algebra
```runa
Import "math/engine/linalg/sparse" as Sparse
Import "math/engine/linalg/solvers" as Solvers

Note: Use sparse matrix storage for large PDE systems
Let sparse_system be Sparse.create_csr_matrix_from_fem_assembly(triangular_mesh)
Let solution be Solvers.conjugate_gradient_sparse(sparse_system, rhs_vector, tolerance: 1e-8)
```

### With Optimization
```runa
Import "math/engine/optimization" as Optimize

Note: PDE-constrained optimization
Process called "objective_function" that takes parameters as List[Real] returns Real:
    Let pde_solution be solve_pde_with_parameters(parameters)
    Return calculate_cost_function(pde_solution)

Let optimal_parameters be Optimize.minimize(
    objective_function,
    initial_guess: [1.0, 0.5, 0.1],
    method: "bfgs"
)
```

## Best Practices

### Stability Conditions
```runa
Note: Check CFL condition for explicit time stepping
Process called "check_cfl_condition" that takes:
    wave_speed as Real,
    grid_spacing as Real,
    time_step as Real
returns Boolean:
    Let cfl_number be wave_speed * time_step / grid_spacing
    Return cfl_number <= 1.0  Note: Must be ≤ 1 for stability
```

### Convergence Testing
```runa
Note: Grid convergence study
Process called "grid_convergence_study" that takes:
    problem as PDEProblem,
    grid_sizes as List[Integer]
returns List[Real]:
    Let errors be []
    For Each n in grid_sizes:
        Let solution be solve_pde_with_grid_size(problem, n)
        Let error be compute_solution_error(solution)
        errors.append(error)
    Return errors
```

### Memory Management
```runa
Note: For large 3D problems, use out-of-core methods
Process called "solve_large_3d_problem" that takes:
    problem as PDE3D,
    memory_limit as Integer
returns PDESolution:
    Note: Use disk storage for matrices that don't fit in memory
```

## Performance Considerations

- **Grid Size**: Balance accuracy vs computational cost
- **Time Step**: Stability constraints for explicit methods
- **Matrix Storage**: Use sparse formats for large problems  
- **Iterative Solvers**: Essential for very large systems
- **Parallel Computing**: Domain decomposition for scalability
- **Adaptive Methods**: Concentrate computational effort where needed

This module provides a comprehensive framework for solving partial differential equations numerically, supporting multiple discretization methods and a wide range of PDE types encountered in engineering and scientific applications.