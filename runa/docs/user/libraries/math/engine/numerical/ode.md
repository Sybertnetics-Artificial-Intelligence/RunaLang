# Ordinary Differential Equations (ODE) Module

The `math/engine/numerical/ode` module provides comprehensive numerical methods for solving ordinary differential equations. This module supports initial value problems, boundary value problems, and systems of ODEs with various numerical integration schemes.

## Quick Start

```runa
Import "math/engine/numerical/ode" as ODE

Note: Define a simple ODE: dy/dx = -2*y + x
Process called "simple_ode" that takes x as Real, y as Real returns Real:
    Return -2.0 * y + x

Note: Solve with initial condition y(0) = 1
Let solution be ODE.solve_ivp(
    ode_function: simple_ode,
    initial_x: 0.0,
    initial_y: 1.0,
    final_x: 5.0,
    method: "runge_kutta_4",
    step_size: 0.1
)

Display "Solution at x=5: " joined with solution.final_value
```

## Core Concepts

### Initial Value Problems (IVP)
Solve ODEs of the form dy/dx = f(x, y) with initial condition y(x₀) = y₀.

### Boundary Value Problems (BVP)
Solve ODEs with conditions specified at multiple points in the domain.

### Systems of ODEs
Handle coupled systems of first-order differential equations.

### Adaptive Step Control
Automatically adjust step sizes based on error estimates for optimal accuracy and efficiency.

## API Reference

### Single-Step Methods

#### Euler Method
```runa
Process called "euler_step" that takes:
    ode_function as Process that takes Real, Real returns Real,
    x_current as Real,
    y_current as Real,
    step_size as Real
returns Real:
    Note: Forward Euler method: y_{n+1} = y_n + h*f(x_n, y_n)
```

#### Runge-Kutta Methods
```runa
Process called "runge_kutta_2" that takes:
    ode_function as Process that takes Real, Real returns Real,
    x_current as Real,
    y_current as Real,
    step_size as Real
returns Real:
    Note: Second-order Runge-Kutta method (midpoint rule)

Process called "runge_kutta_4" that takes:
    ode_function as Process that takes Real, Real returns Real,
    x_current as Real,
    y_current as Real,
    step_size as Real
returns Real:
    Note: Fourth-order Runge-Kutta method (classical RK4)
```

### Multi-Step Methods

#### Adams-Bashforth Methods
```runa
Process called "adams_bashforth_2" that takes:
    ode_function as Process that takes Real, Real returns Real,
    x_values as List[Real],
    y_values as List[Real],
    step_size as Real
returns Real:
    Note: Second-order Adams-Bashforth predictor

Process called "adams_bashforth_4" that takes:
    ode_function as Process that takes Real, Real returns Real,
    x_values as List[Real],
    y_values as List[Real],
    step_size as Real
returns Real:
    Note: Fourth-order Adams-Bashforth predictor
```

#### Adams-Moulton Methods
```runa
Process called "adams_moulton_2" that takes:
    ode_function as Process that takes Real, Real returns Real,
    x_values as List[Real],
    y_values as List[Real],
    predicted_y as Real,
    step_size as Real
returns Real:
    Note: Second-order Adams-Moulton corrector

Process called "adams_moulton_4" that takes:
    ode_function as Process that takes Real, Real returns Real,
    x_values as List[Real],
    y_values as List[Real],
    predicted_y as Real,
    step_size as Real
returns Real:
    Note: Fourth-order Adams-Moulton corrector
```

### Adaptive Methods

#### Runge-Kutta-Fehlberg
```runa
Process called "rkf45" that takes:
    ode_function as Process that takes Real, Real returns Real,
    x_current as Real,
    y_current as Real,
    step_size as Real,
    tolerance as Real
returns Dictionary[String, Real]:
    Note: Runge-Kutta-Fehlberg method with adaptive step control
    Note: Returns new_y, error_estimate, and suggested_step_size
```

#### Dormand-Prince
```runa
Process called "dopri5" that takes:
    ode_function as Process that takes Real, Real returns Real,
    x_current as Real,
    y_current as Real,
    step_size as Real,
    tolerance as Real
returns Dictionary[String, Real]:
    Note: Dormand-Prince method (5th order with 4th order error estimate)
```

### System Solvers

#### Vector ODE Systems
```runa
Type called "ODESystem":
    dimension as Integer
    state_vector as List[Real]
    derivative_function as Process that takes Real, List[Real] returns List[Real]

Process called "solve_system_rk4" that takes:
    system as ODESystem,
    initial_x as Real,
    final_x as Real,
    step_size as Real
returns List[List[Real]]:
    Note: Solve system of ODEs using 4th-order Runge-Kutta
```

### Boundary Value Problems

#### Shooting Method
```runa
Process called "shooting_method" that takes:
    ode_function as Process that takes Real, Real, Real returns Real,
    boundary_conditions as Dictionary[String, Real],
    x_span as Tuple[Real, Real],
    initial_guess as Real
returns Dictionary[String, Any]:
    Note: Solve BVP by converting to initial value problems
```

#### Finite Difference Method
```runa
Process called "finite_difference_bvp" that takes:
    ode_coefficients as Dictionary[String, Process],
    boundary_conditions as Dictionary[String, Real],
    x_span as Tuple[Real, Real],
    num_points as Integer
returns List[Real]:
    Note: Solve linear BVP using finite difference discretization
```

### High-Level Solvers

#### General IVP Solver
```runa
Process called "solve_ivp" that takes:
    ode_function as Process that takes Real, Real returns Real,
    initial_x as Real,
    initial_y as Real,
    final_x as Real,
    method as String,
    step_size as Real,
    tolerance as Real,
    max_steps as Integer
returns ODESolution:
    Note: High-level interface for solving initial value problems

Type called "ODESolution":
    x_values as List[Real]
    y_values as List[Real]
    final_value as Real
    num_steps as Integer
    success as Boolean
    message as String
```

## Practical Examples

### Exponential Decay
```runa
Import "math/engine/numerical/ode" as ODE
Import "math/engine/numerical/core" as Numerical

Note: Radioactive decay: dN/dt = -λ*N
Process called "decay_equation" that takes t as Real, N as Real returns Real:
    Let decay_constant be 0.693  Note: Half-life constant
    Return -decay_constant * N

Note: Solve with initial condition N(0) = 1000
Let decay_solution be ODE.solve_ivp(
    ode_function: decay_equation,
    initial_x: 0.0,
    initial_y: 1000.0,
    final_x: 10.0,
    method: "runge_kutta_4",
    step_size: 0.1
)

Display "Population after 10 time units: " joined with decay_solution.final_value
Display "Number of integration steps: " joined with decay_solution.num_steps
```

### Harmonic Oscillator
```runa
Note: Convert second-order ODE to system of first-order ODEs
Note: d²x/dt² + ω²x = 0 becomes: dx/dt = v, dv/dt = -ω²x

Process called "harmonic_system" that takes t as Real, state as List[Real] returns List[Real]:
    Let x be state[0]
    Let v be state[1]
    Let omega_squared be 4.0  Note: ω² = 4
    
    Let dx_dt be v
    Let dv_dt be -omega_squared * x
    
    Return [dx_dt, dv_dt]

Let oscillator_system be ODE.ODESystem:
    dimension: 2
    state_vector: [1.0, 0.0]  Note: Initial position x=1, velocity v=0
    derivative_function: harmonic_system

Let oscillation_solution be ODE.solve_system_rk4(
    oscillator_system,
    initial_x: 0.0,
    final_x: 10.0,
    step_size: 0.01
)

Note: Extract position and velocity trajectories
Let positions be []
Let velocities be []
For Each solution_point in oscillation_solution:
    positions.append(solution_point[0])
    velocities.append(solution_point[1])

Display "Maximum displacement: " joined with Numerical.maximum(positions)
Display "Period from numerical solution: " joined with calculate_period(positions)
```

### Stiff ODE Example
```runa
Note: Van der Pol oscillator (stiff for large μ)
Process called "van_der_pol" that takes t as Real, state as List[Real] returns List[Real]:
    Let x be state[0]
    Let y be state[1]
    Let mu be 10.0  Note: Stiffness parameter
    
    Let dx_dt be y
    Let dy_dt be mu * (1.0 - x * x) * y - x
    
    Return [dx_dt, dy_dt]

Note: Use stiff solver with adaptive stepping
Let stiff_solution be ODE.solve_ivp(
    ode_function: van_der_pol,
    initial_x: 0.0,
    initial_y: [2.0, 0.0],
    final_x: 20.0,
    method: "dopri5",  Note: Good for stiff problems
    tolerance: 1e-6,
    max_steps: 10000
)

If stiff_solution.success:
    Display "Van der Pol solution converged successfully"
    Display "Total integration steps: " joined with stiff_solution.num_steps
Otherwise:
    Display "Integration failed: " joined with stiff_solution.message
```

### Boundary Value Problem
```runa
Note: Solve y'' - 2y' + y = 0 with y(0) = 0, y(1) = 1
Note: Convert to first-order system: y' = z, z' = 2z - y

Process called "bvp_system" that takes x as Real, y as Real, z as Real returns Real:
    Return 2.0 * z - y

Let boundary_conditions be Dictionary[String, Real]:
    "left_boundary": 0.0   Note: y(0) = 0
    "right_boundary": 1.0  Note: y(1) = 1

Let bvp_solution be ODE.shooting_method(
    ode_function: bvp_system,
    boundary_conditions: boundary_conditions,
    x_span: (0.0, 1.0),
    initial_guess: 1.0  Note: Initial guess for y'(0)
)

If bvp_solution["success"]:
    Display "BVP solution found"
    Display "Boundary derivative: " joined with bvp_solution["initial_derivative"]
Otherwise:
    Display "BVP solution failed to converge"
```

## Advanced Features

### Error Control and Diagnostics
```runa
Note: Configure solver with detailed error monitoring
Let advanced_config be Dictionary[String, Any]:
    "method": "rkf45"
    "absolute_tolerance": 1e-8
    "relative_tolerance": 1e-6
    "max_step_size": 0.1
    "min_step_size": 1e-12
    "error_norm": "euclidean"
    "safety_factor": 0.9

Let monitored_solution be ODE.solve_ivp_advanced(
    ode_function: complex_ode,
    initial_conditions: initial_state,
    time_span: (0.0, 100.0),
    configuration: advanced_config
)

Display "Integration statistics:"
Display "  Total function evaluations: " joined with monitored_solution.num_evaluations
Display "  Average step size: " joined with monitored_solution.average_step_size
Display "  Maximum error estimate: " joined with monitored_solution.max_error
```

### Event Detection
```runa
Note: Detect when solution crosses zero (root finding during integration)
Process called "event_function" that takes t as Real, y as List[Real] returns Real:
    Return y[0]  Note: Detect when first component crosses zero

Let event_config be Dictionary[String, Any]:
    "event_function": event_function
    "direction": "both"  Note: Detect both up and down crossings
    "terminal": False   Note: Continue integration after event

Let solution_with_events be ODE.solve_ivp_with_events(
    ode_function: oscillatory_system,
    initial_x: 0.0,
    initial_y: [1.0, 0.0],
    final_x: 20.0,
    method: "dopri5",
    event_config: event_config
)

Display "Number of zero crossings detected: " joined with solution_with_events.events.count()
For Each event in solution_with_events.events:
    Display "Zero crossing at t = " joined with event.time
```

## Integration with Other Modules

### With Linear Algebra
```runa
Import "math/engine/linalg/core" as LinAlg
Import "math/engine/numerical/ode" as ODE

Note: Solve large system of ODEs using sparse matrices
Process called "large_linear_system" that takes t as Real, y as List[Real] returns List[Real]:
    Let A be LinAlg.sparse_matrix_from_file("system_matrix.dat")
    Return LinAlg.sparse_matrix_vector_multiply(A, y)

Let large_system_solution be ODE.solve_system_adaptive(
    system_function: large_linear_system,
    initial_state: initial_vector,
    time_span: (0.0, 1.0),
    method: "implicit_euler"  Note: Good for large stiff systems
)
```

### With Root Finding
```runa
Import "math/engine/numerical/rootfinding" as RootFind
Import "math/engine/numerical/ode" as ODE

Note: Find periodic solutions using shooting method
Process called "periodic_condition" that takes period as Real returns Real:
    Let solution be ODE.solve_ivp(
        ode_function: limit_cycle_ode,
        initial_x: 0.0,
        initial_y: initial_guess,
        final_x: period,
        method: "runge_kutta_4"
    )
    Return solution.final_value - initial_guess  Note: Periodic condition

Let period_estimate be RootFind.brent_method(
    periodic_condition,
    lower_bound: 1.0,
    upper_bound: 10.0,
    tolerance: 1e-10
)

Display "Estimated period: " joined with period_estimate
```

## Best Practices

### Choosing Integration Methods
1. **Euler Method**: Only for educational purposes or very simple problems
2. **RK4**: Good general-purpose method for smooth problems
3. **RKF45/DOPRI5**: Adaptive methods for problems requiring high accuracy
4. **Adams Methods**: Efficient for smooth problems when function evaluations are expensive
5. **Implicit Methods**: Essential for stiff problems

### Step Size Selection
```runa
Note: Estimate appropriate step size
Process called "estimate_step_size" that takes:
    ode_function as Process that takes Real, Real returns Real,
    initial_x as Real,
    initial_y as Real,
    tolerance as Real
returns Real:
    Note: Use local truncation error to estimate step size
    Let f0 be ode_function(initial_x, initial_y)
    Let test_step be 0.01
    Let y1 be initial_y + test_step * f0
    Let f1 be ode_function(initial_x + test_step, y1)
    Let error_estimate be 0.5 * test_step * test_step * (f1 - f0)
    Return (tolerance / error_estimate) ^ 0.5 * test_step
```

### Memory Management for Long Integrations
```runa
Note: For very long time integrations, use checkpointing
Process called "long_integration_with_checkpoints" that takes:
    ode_function as Process that takes Real, Real returns Real,
    initial_conditions as Dictionary[String, Real],
    final_time as Real,
    checkpoint_interval as Real
returns ODESolution:
    Note: Break integration into chunks to manage memory
```

### Validation and Verification
```runa
Note: Always validate ODE solutions when possible
Process called "validate_solution" that takes solution as ODESolution returns Boolean:
    Note: Check conservation laws, known invariants, or analytical solutions
    Let energy_initial be calculate_energy(solution.y_values[0])
    Let energy_final be calculate_energy(solution.y_values[-1])
    Let energy_conservation_error be abs(energy_final - energy_initial) / energy_initial
    Return energy_conservation_error < 1e-6
```

## Performance Considerations

- **Function Evaluation Cost**: Adams methods minimize function evaluations
- **Memory Usage**: Explicit methods use less memory than implicit methods
- **Stiffness**: Implicit methods are essential for stiff problems
- **Accuracy Requirements**: Higher-order methods provide better accuracy per step
- **Adaptive vs Fixed Step**: Adaptive methods are more efficient for varying smoothness

This module provides a comprehensive toolkit for solving ordinary differential equations numerically, supporting everything from simple initial value problems to complex systems with event detection and error control.