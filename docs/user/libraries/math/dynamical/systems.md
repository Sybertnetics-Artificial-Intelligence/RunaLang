# Dynamical Systems Analysis

The **systems** module provides comprehensive tools for analyzing dynamical systems, including stability analysis, phase space analysis, and invariant set computation. This module forms the foundation for understanding system behavior and forms the basis for bifurcation and chaos analysis.

## Overview

Dynamical systems theory studies the evolution of states over time via differential equations. The systems module provides tools for analyzing both continuous and discrete dynamical systems, with emphasis on stability, phase space structure, and invariant sets.

## Key Features

- **System Definition**: Support for both continuous and discrete dynamical systems
- **Stability Analysis**: Complete eigenvalue analysis and Lyapunov function computation
- **Phase Space Analysis**: Phase portrait generation with nullclines and flow fields
- **Equilibrium Detection**: Automated finding and classification of fixed points
- **Invariant Manifolds**: Computation of stable and unstable manifolds
- **High-Precision Computation**: All analysis uses Runa's precision arithmetic

## Mathematical Foundation

### Continuous Systems
For continuous systems: **dx/dt = f(x,t)**
- **Flows**: φᵗ: M → M define evolution on manifold M
- **Autonomous Systems**: f independent of time t
- **Phase Space**: State space with vector field defining dynamics

### Discrete Systems  
For discrete systems: **x_{n+1} = f(x_n)**
- **Maps**: f: M → M iterate the state space
- **Fixed Points**: Solutions to f(x) = x
- **Periodic Orbits**: Points with f^n(x) = x for some n

### Stability Theory
- **Linear Stability**: Eigenvalues of Jacobian matrix Df(x₀)
- **Lyapunov Functions**: V(x) with dV/dt < 0 along trajectories
- **Center Manifold Theory**: Analysis near critical eigenvalues

## Data Types

### Core System Definition

```runa
Type called "DynamicalSystem":
    continuous_system as Boolean           Note: True for ODEs, False for maps
    autonomous as Boolean                  Note: Time-independent systems
    dimension as Integer                   Note: Phase space dimension
    state_space_bounds as List[Tuple[Float64, Float64]]  Note: Domain bounds
    vector_field as Function              Note: System equations f(x,t)
    jacobian_function as Function         Note: Derivative matrix Df(x)
    parameters as Dictionary[String, Float64]  Note: System parameters
    conserved_quantities as List[Function]     Note: Integrals of motion
    symmetries as List[Function]              Note: Symmetry transformations
```

### Phase Space Structure

```runa
Type called "PhasePortrait":
    equilibrium_points as List[List[Float64]]     Note: Fixed points
    periodic_orbits as List[List[List[Float64]]]  Note: Closed orbits
    separatrices as List[List[List[Float64]]]     Note: Separating curves
    flow_direction_field as List[List[List[Float64]]]  Note: Vector field
    nullclines as List[List[List[Float64]]]       Note: Zero-velocity curves
    invariant_manifolds as List[List[List[Float64]]]   Note: Invariant sets
    basins_of_attraction as List[List[List[Float64]]]  Note: Attractor basins
    saddle_connections as List[List[List[Float64]]]    Note: Heteroclinic orbits
```

### Stability Analysis Results

```runa
Type called "StabilityAnalysis":
    equilibrium_point as List[Float64]           Note: Point being analyzed
    eigenvalues as List[Complex64]               Note: Jacobian eigenvalues
    eigenvectors as List[List[Complex64]]        Note: Corresponding eigenvectors
    stability_type as String                     Note: Classification
    lyapunov_function as Function                Note: Stability certificate
    stable_manifold_dimension as Integer         Note: Stable space dimension
    unstable_manifold_dimension as Integer       Note: Unstable space dimension
    center_manifold_dimension as Integer         Note: Critical space dimension
```

## System Creation and Analysis

### Creating Dynamical Systems

```runa
Import "math/dynamical/systems" as DynamicalSystems

Process called "create_pendulum_system":
    Note: Simple pendulum: d²θ/dt² + (g/L)sin(θ) = 0
    Note: Convert to first-order system: dx₁/dt = x₂, dx₂/dt = -(g/L)sin(x₁)
    
    Let pendulum_equations be Function.create[
        inputs: ["state", "time"],
        body: {
            Let theta be state[0]
            Let omega be state[1]
            
            Let theta_dot be omega
            Let omega_dot be -(9.81/1.0) * MathOps.sine[theta]
            
            Return [theta_dot, omega_dot]
        }
    ]
    
    Let jacobian_function be Function.create[
        inputs: ["state"],
        body: {
            Let theta be state[0]
            Return [[0.0, 1.0], [-(9.81/1.0) * MathOps.cosine[theta], 0.0]]
        }
    ]
    
    Let pendulum_system be DynamicalSystems.create_system[
        continuous_system: true,
        autonomous: true,
        dimension: 2,
        state_space_bounds: [(-3.14159, 3.14159), (-10.0, 10.0)],
        vector_field: pendulum_equations,
        jacobian_function: jacobian_function,
        parameters: Dictionary.from_pairs[("g", 9.81), ("L", 1.0)]
    ]
    
    Return pendulum_system
```

### Finding Equilibrium Points

```runa
Process called "find_system_equilibria":
    Let system be create_pendulum_system[]
    
    Note: Find equilibrium points where f(x*) = 0
    Let equilibrium_points be DynamicalSystems.find_equilibrium_points[
        system,
        search_bounds: [(-3.14159, 3.14159), (-2.0, 2.0)],
        tolerance: 1e-10,
        max_iterations: 100
    ]
    
    Print("Found " + equilibrium_points.length.to_string[] + " equilibrium points:")
    For Each point in equilibrium_points:
        Print("  Equilibrium at: [" + point[0].to_string[] + ", " + point[1].to_string[] + "]")
    
    Return equilibrium_points
```

## Stability Analysis

### Linear Stability Analysis

```runa
Process called "analyze_equilibrium_stability":
    Let system be create_pendulum_system[]
    Let equilibrium be [0.0, 0.0]  Note: Stable equilibrium at bottom
    
    Let stability_analysis be DynamicalSystems.analyze_stability[
        system,
        equilibrium_point: equilibrium
    ]
    
    Print("Stability Analysis Results:")
    Print("  Equilibrium: [" + equilibrium[0].to_string[] + ", " + equilibrium[1].to_string[] + "]")
    Print("  Stability Type: " + stability_analysis.stability_type)
    Print("  Eigenvalues:")
    
    For Each eigenvalue in stability_analysis.eigenvalues:
        Let real_part be eigenvalue.real
        Let imag_part be eigenvalue.imaginary
        Print("    λ = " + real_part.to_string[] + " + " + imag_part.to_string[] + "i")
    
    Note: Classify stability based on eigenvalue location
    Let all_negative_real be true
    For Each eigenvalue in stability_analysis.eigenvalues:
        If eigenvalue.real >= 0.0:
            Let all_negative_real be false
            Break
    
    If all_negative_real:
        Print("  Classification: Asymptotically Stable")
    Otherwise:
        Print("  Classification: Unstable or Marginally Stable")
    
    Return stability_analysis
```

### Lyapunov Function Analysis

```runa
Process called "compute_lyapunov_function":
    Let system be create_pendulum_system[]
    Let equilibrium be [0.0, 0.0]
    
    Note: For pendulum, energy function V = ½mL²ω² + mgL(1 - cos(θ))
    Let lyapunov_function be Function.create[
        inputs: ["state"],
        body: {
            Let theta be state[0]
            Let omega be state[1]
            Let mass be 1.0
            Let length be 1.0
            Let gravity be 9.81
            
            Let kinetic_energy be 0.5 * mass * length * length * omega * omega
            Let potential_energy be mass * gravity * length * (1.0 - MathOps.cosine[theta])
            
            Return kinetic_energy + potential_energy
        }
    ]
    
    Note: Verify Lyapunov conditions: V > 0 and dV/dt < 0
    Let test_states be [
        [0.1, 0.1],
        [0.5, -0.3],
        [-0.2, 0.4]
    ]
    
    For Each state in test_states:
        Let energy_value be lyapunov_function.call[state]
        Let state_derivative be system.vector_field.call[state, 0.0]
        Let energy_derivative be NumericalDiff.directional_derivative[
            lyapunov_function, state, state_derivative
        ]
        
        Print("State: [" + state[0].to_string[] + ", " + state[1].to_string[] + "]")
        Print("  V(x) = " + energy_value.to_string[])
        Print("  dV/dt = " + energy_derivative.to_string[])
        
        If energy_derivative <= 0.0:
            Print("  Lyapunov condition satisfied")
        Otherwise:
            Print("  Lyapunov condition violated")
    
    Return lyapunov_function
```

## Phase Space Analysis

### Generating Phase Portraits

```runa
Process called "generate_system_phase_portrait":
    Let system be create_pendulum_system[]
    
    Note: Generate comprehensive phase portrait
    Let portrait be DynamicalSystems.generate_phase_portrait[
        system,
        x_range: (-3.0, 3.0),
        y_range: (-4.0, 4.0),
        grid_resolution: [50, 50],
        trajectory_length: 10.0,
        initial_conditions: [
            [0.1, 0.0],   Note: Small oscillation
            [2.0, 0.0],   Note: Large oscillation  
            [3.1, 0.0],   Note: Near separatrix
            [0.0, 3.0]    Note: Fast rotation
        ]
    ]
    
    Print("Phase Portrait Generated:")
    Print("  Equilibrium Points: " + portrait.equilibrium_points.length.to_string[])
    Print("  Periodic Orbits: " + portrait.periodic_orbits.length.to_string[])
    Print("  Separatrices: " + portrait.separatrices.length.to_string[])
    
    Return portrait
```

### Computing Invariant Manifolds

```runa
Process called "compute_invariant_manifolds":
    Note: Analyze saddle point with stable/unstable manifolds
    Let saddle_system be Function.create[
        inputs: ["state", "time"],
        body: {
            Let x be state[0]
            Let y be state[1]
            Return [x - x*y, -y + x*y]  Note: dx/dt = x(1-y), dy/dt = y(x-1)
        }
    ]
    
    Let system be DynamicalSystems.create_system[
        continuous_system: true,
        autonomous: true,
        dimension: 2,
        vector_field: saddle_system,
        parameters: Dictionary.empty[String, Float64][]
    ]
    
    Let saddle_point be [1.0, 1.0]
    
    Note: Compute stable and unstable manifolds
    Let manifolds be DynamicalSystems.compute_invariant_manifolds[
        system,
        equilibrium_point: saddle_point,
        manifold_length: 5.0,
        resolution: 100,
        integration_time: 20.0
    ]
    
    Print("Invariant Manifolds for Saddle Point [1.0, 1.0]:")
    Print("  Stable Manifold Branches: " + manifolds.stable_branches.length.to_string[])
    Print("  Unstable Manifold Branches: " + manifolds.unstable_branches.length.to_string[])
    
    Return manifolds
```

## Advanced Analysis

### Basin of Attraction Analysis

```runa
Process called "compute_attraction_basins":
    Note: Analyze system with multiple attractors
    Let multistable_system be Function.create[
        inputs: ["state", "time"],
        body: {
            Let x be state[0]
            Let y be state[1]
            Note: dx/dt = -x³ + x, dy/dt = -y
            Return [-x*x*x + x, -y]
        }
    ]
    
    Let system be DynamicalSystems.create_system[
        continuous_system: true,
        autonomous: true,
        dimension: 2,
        vector_field: multistable_system,
        parameters: Dictionary.empty[String, Float64][]
    ]
    
    Note: Compute basins of attraction for stable equilibria
    Let basins be DynamicalSystems.compute_basins_of_attraction[
        system,
        domain: [(-2.0, 2.0), (-2.0, 2.0)],
        grid_resolution: [100, 100],
        integration_time: 50.0,
        convergence_tolerance: 1e-6
    ]
    
    Print("Basin Analysis Results:")
    Print("  Number of Attractors: " + basins.attractors.length.to_string[])
    Print("  Basin Boundaries Computed: " + basins.boundary_points.length.to_string[])
    
    Return basins
```

### Poincaré Section Analysis

```runa
Process called "compute_poincare_section":
    Note: Analyze 3D system using Poincaré sections
    Let lorenz_system be Function.create[
        inputs: ["state", "time"],
        body: {
            Let x be state[0]
            Let y be state[1]
            Let z be state[2]
            Let sigma be 10.0
            Let rho be 28.0
            Let beta be 8.0/3.0
            
            Return [
                sigma * (y - x),
                x * (rho - z) - y,
                x * y - beta * z
            ]
        }
    ]
    
    Let system be DynamicalSystems.create_system[
        continuous_system: true,
        autonomous: true,
        dimension: 3,
        vector_field: lorenz_system,
        parameters: Dictionary.from_pairs[("sigma", 10.0), ("rho", 28.0), ("beta", 8.0/3.0)]
    ]
    
    Note: Define Poincaré section plane z = 27
    Let section_plane be Function.create[
        inputs: ["state"],
        body: { Return state[2] - 27.0 }
    ]
    
    Let poincare_map be DynamicalSystems.compute_poincare_section[
        system,
        section_definition: section_plane,
        initial_conditions: [[1.0, 1.0, 1.0]],
        integration_time: 1000.0,
        max_crossings: 1000
    ]
    
    Print("Poincaré Section Analysis:")
    Print("  Section Crossings: " + poincare_map.crossing_points.length.to_string[])
    Print("  Return Map Dimension: " + poincare_map.map_dimension.to_string[])
    
    Return poincare_map
```

## Error Handling

### Convergence and Numerical Issues

```runa
Process called "handle_numerical_errors":
    Try:
        Let system be create_problematic_system[]  Note: System with singularities
        Let equilibria be DynamicalSystems.find_equilibrium_points[
            system,
            search_bounds: [(-10.0, 10.0), (-10.0, 10.0)],
            tolerance: 1e-12,
            max_iterations: 1000
        ]
        
        For Each point in equilibria:
            Try:
                Let stability be DynamicalSystems.analyze_stability[system, point]
                Print("Stability analysis successful for point: " + point.to_string[])
            Catch error as Errors.NumericalInstability:
                Print("Numerical instability at equilibrium: " + point.to_string[])
                Print("Consider using different tolerance or method")
            Catch error as Errors.SingularMatrix:
                Print("Singular Jacobian at equilibrium: " + point.to_string[])
                Print("May indicate bifurcation point or degenerate case")
        
    Catch error as Errors.ConvergenceFailure:
        Print("Failed to find equilibrium points")
        Print("Try different initial guesses or larger search domain")
    Catch error as Errors.InvalidSystem:
        Print("System definition error")
        Print("Check vector field and Jacobian functions")
```

## Best Practices

### System Definition Guidelines

1. **Vector Field Consistency**: Ensure vector field and Jacobian are consistent
2. **Parameter Management**: Use parameter dictionaries for systematic studies
3. **Domain Specification**: Define appropriate state space bounds
4. **Precision Control**: Use high-precision arithmetic for sensitive systems

### Analysis Recommendations

1. **Multi-Scale Analysis**: Use different time scales for different phenomena
2. **Initial Condition Studies**: Test multiple starting points for completeness
3. **Parameter Sensitivity**: Analyze system behavior over parameter ranges
4. **Validation**: Compare analytical and numerical results where possible

### Performance Optimization

1. **Adaptive Methods**: Use adaptive integration for efficiency
2. **Parallel Computation**: Leverage parallel processing for parameter studies
3. **Memory Management**: Optimize storage for large trajectory datasets
4. **Caching**: Cache expensive computations like Jacobian evaluations

## Integration with Other Modules

- **Bifurcation Analysis**: Parameter-dependent stability changes
- **Chaos Theory**: Lyapunov exponents and strange attractors
- **Numerical Methods**: ODE solvers and root finding algorithms
- **Linear Algebra**: Eigenvalue problems and matrix decompositions
- **Optimization**: Parameter estimation and system identification

## See Also

- [Bifurcation Analysis Guide](bifurcation.md) - Parameter-dependent behavior analysis
- [Chaos Theory Guide](chaos.md) - Chaotic dynamics and complexity measures
- [Dynamical Module Overview](README.md) - Module introduction and quick start
- [ODE Solvers Documentation](../engine/numerical/README.md) - Integration methods
- [Linear Algebra Documentation](../algebra/README.md) - Matrix computations