# Bifurcation Theory Analysis

The **bifurcation** module provides comprehensive tools for analyzing bifurcations in dynamical systems, including detection, classification, and normal form analysis. This module is essential for understanding how system behavior changes qualitatively as parameters vary.

## Overview

Bifurcation theory studies qualitative changes in the behavior of dynamical systems when parameters cross critical values. These changes can involve the creation, destruction, or change in stability of equilibria, periodic orbits, and other invariant sets.

## Key Features

- **Automatic Bifurcation Detection**: Systematic identification of bifurcation points
- **Bifurcation Classification**: Complete taxonomy of local and global bifurcations
- **Normal Form Analysis**: Canonical form computation for bifurcations
- **Continuation Methods**: Parameter continuation and branch following
- **Bifurcation Diagrams**: Comprehensive visualization of parameter-dependent behavior
- **Codimension Analysis**: Multi-parameter bifurcation studies

## Mathematical Foundation

### Local Bifurcations
- **Saddle-Node**: dx/dt = r + x² (fold bifurcation)
- **Transcritical**: dx/dt = rx - x² (exchange of stability)
- **Pitchfork**: dx/dt = rx - x³ (symmetry-breaking bifurcation)
- **Hopf**: Transition from equilibrium to limit cycle

### Global Bifurcations
- **Homoclinic**: Trajectory connects saddle to itself
- **Heteroclinic**: Trajectory connects different saddle points
- **Period-Doubling**: Route to chaos via cascade

### Theoretical Framework
- **Center Manifold Theory**: Local analysis near bifurcations
- **Normal Form Theory**: Universal unfolding of bifurcations
- **Poincaré-Bendixson Theory**: Planar system analysis

## Data Types

### Bifurcation Classification

```runa
Type called "BifurcationType":
    saddle_node as Boolean                    Note: Fold bifurcation
    transcritical as Boolean                  Note: Exchange of stability
    pitchfork_supercritical as Boolean        Note: Stable branch creation
    pitchfork_subcritical as Boolean          Note: Unstable branch creation
    hopf_supercritical as Boolean             Note: Stable limit cycle birth
    hopf_subcritical as Boolean               Note: Unstable limit cycle death
    period_doubling as Boolean                Note: Period-2 orbit creation
    homoclinic as Boolean                     Note: Saddle connection
    heteroclinic as Boolean                   Note: Saddle-to-saddle connection
    cusp as Boolean                           Note: Higher-order singularity
```

### Bifurcation Point Analysis

```runa
Type called "BifurcationPoint":
    parameter_value as Float64                Note: Critical parameter value
    bifurcation_type as BifurcationType       Note: Bifurcation classification
    stability_change as String                Note: Nature of stability change
    eigenvalues as List[Complex64]            Note: Jacobian eigenvalues
    normal_form_coefficients as List[Float64] Note: Canonical form parameters
    codimension as Integer                    Note: Parameter space dimension
    criticality as String                     Note: Supercritical/subcritical
    local_coordinates as List[Float64]        Note: Center manifold coordinates
```

### Bifurcation Diagram Structure

```runa
Type called "BifurcationDiagram":
    parameter_range as Tuple[Float64, Float64]     Note: Parameter interval
    branch_data as List[List[Float64]]             Note: Solution branches
    stability_info as List[String]                 Note: Stability classification
    bifurcation_points as List[BifurcationPoint]   Note: Critical points
    attractors as List[List[Float64]]              Note: Stable solutions
    repellers as List[List[Float64]]               Note: Unstable solutions
    continuation_method as String                  Note: Numerical method used
    resolution as Integer                          Note: Parameter discretization
```

## Local Bifurcation Analysis

### Saddle-Node Bifurcations

```runa
Import "math/dynamical/bifurcation" as Bifurcation
Import "math/dynamical/systems" as DynamicalSystems

Process called "analyze_saddle_node_example":
    Note: Standard saddle-node bifurcation: dx/dt = r + x²
    Let saddle_node_system be Function.create[
        inputs: ["state", "time", "parameter"],
        body: {
            Let x be state[0]
            Let r be parameter
            Return [r + x * x]
        }
    ]
    
    Note: Analyze bifurcation over parameter range
    Let diagram be Bifurcation.analyze_saddle_node_bifurcation[
        saddle_node_system,
        parameter_range: (-1.0, 1.0),
        initial_conditions: [0.0]
    ]
    
    Print("Saddle-Node Bifurcation Analysis:")
    Print("  Parameter Range: [-1.0, 1.0]")
    Print("  Bifurcation Points Found: " + diagram.bifurcation_points.length.to_string[])
    
    For Each bifurcation_point in diagram.bifurcation_points:
        Print("  Critical Parameter r* = " + bifurcation_point.parameter_value.to_string[])
        Print("  Normal Form Coefficients: " + bifurcation_point.normal_form_coefficients.to_string[])
        
        Note: For r < 0: two equilibria, for r > 0: no equilibria
        If bifurcation_point.parameter_value < 1e-10:
            Print("  Behavior: Two equilibria annihilate at r = 0")
    
    Return diagram
```

### Transcritical Bifurcations

```runa
Process called "analyze_transcritical_bifurcation":
    Note: Transcritical bifurcation: dx/dt = rx - x²
    Let transcritical_system be Function.create[
        inputs: ["state", "time", "parameter"],
        body: {
            Let x be state[0]
            Let r be parameter
            Return [r * x - x * x]
        }
    ]
    
    Let diagram be Bifurcation.analyze_transcritical_bifurcation[
        transcritical_system,
        parameter_range: (-2.0, 2.0),
        initial_conditions: [0.1]
    ]
    
    Print("Transcritical Bifurcation Analysis:")
    Print("  Equilibria Exchange Stability at r = 0")
    
    For Each bifurcation_point in diagram.bifurcation_points:
        Let normal_form be bifurcation_point.normal_form_coefficients
        Print("  At r* = " + bifurcation_point.parameter_value.to_string[])
        Print("  Normal form: dx/dt = " + normal_form[0].to_string[] + "x + " + normal_form[1].to_string[] + "x²")
        
        If normal_form[1] < 0.0:
            Print("  Supercritical: Stable nonzero branch for r > 0")
        Otherwise:
            Print("  Subcritical: Unstable nonzero branch for r > 0")
    
    Return diagram
```

### Pitchfork Bifurcations

```runa
Process called "analyze_pitchfork_bifurcation":
    Note: Pitchfork bifurcation: dx/dt = rx - x³
    Let pitchfork_system be Function.create[
        inputs: ["state", "time", "parameter"],
        body: {
            Let x be state[0]
            Let r be parameter
            Return [r * x - x * x * x]
        }
    ]
    
    Let diagram be Bifurcation.analyze_pitchfork_bifurcation[
        pitchfork_system,
        parameter_range: (-1.0, 2.0),
        initial_conditions: [0.1]
    ]
    
    Print("Pitchfork Bifurcation Analysis:")
    
    For Each bifurcation_point in diagram.bifurcation_points:
        Print("  Critical Point at r* = " + bifurcation_point.parameter_value.to_string[])
        
        If bifurcation_point.criticality == "supercritical":
            Print("  Supercritical: x = 0 destabilizes, ±√r stabilize for r > 0")
        Otherwise:
            Print("  Subcritical: x = 0 destabilizes, ±√r unstable for r > 0")
        
        Let normal_form be bifurcation_point.normal_form_coefficients
        Print("  Cubic coefficient: " + normal_form[2].to_string[])
    
    Return diagram
```

### Hopf Bifurcations

```runa
Process called "analyze_hopf_bifurcation":
    Note: 2D system with Hopf bifurcation
    Let hopf_system be Function.create[
        inputs: ["state", "time", "parameter"],
        body: {
            Let x be state[0]
            Let y be state[1]
            Let mu be parameter
            
            Note: dx/dt = μx - y - x(x² + y²), dy/dt = x + μy - y(x² + y²)
            Let r_squared be x * x + y * y
            Return [
                mu * x - y - x * r_squared,
                x + mu * y - y * r_squared
            ]
        }
    ]
    
    Let diagram be Bifurcation.analyze_hopf_bifurcation[
        hopf_system,
        parameter_range: (-1.0, 1.0),
        initial_conditions: [0.1, 0.1]
    ]
    
    Print("Hopf Bifurcation Analysis:")
    
    For Each bifurcation_point in diagram.bifurcation_points:
        Print("  Hopf Point at μ* = " + bifurcation_point.parameter_value.to_string[])
        
        Let eigenvalues be bifurcation_point.eigenvalues
        Let frequency be eigenvalues[0].imaginary
        Print("  Frequency at bifurcation: ω = " + frequency.to_string[])
        
        If bifurcation_point.criticality == "supercritical":
            Print("  Supercritical: Stable limit cycle emerges for μ > μ*")
            Print("  Limit cycle radius ≈ √(μ - μ*) for small μ - μ*")
        Otherwise:
            Print("  Subcritical: Unstable limit cycle exists for μ < μ*")
    
    Return diagram
```

## Continuation Methods and Branch Following

### Parameter Continuation

```runa
Process called "perform_parameter_continuation":
    Note: Van der Pol oscillator with parameter-dependent behavior
    Let van_der_pol be Function.create[
        inputs: ["state", "time", "parameter"],
        body: {
            Let x be state[0]
            Let y be state[1]
            Let epsilon be parameter
            
            Return [y, epsilon * (1.0 - x * x) * y - x]
        }
    ]
    
    Note: Continue solutions as epsilon varies
    Let continuation_result be Bifurcation.parameter_continuation[
        van_der_pol,
        parameter_range: (0.1, 5.0),
        initial_solution: [1.0, 0.0],
        continuation_method: "predictor_corrector",
        step_size: 0.05,
        max_steps: 100
    ]
    
    Print("Parameter Continuation Results:")
    Print("  Solution branches: " + continuation_result.branches.length.to_string[])
    Print("  Turning points: " + continuation_result.turning_points.length.to_string[])
    
    Note: Analyze limit cycle amplitude vs parameter
    For Each step in continuation_result.solution_curve:
        Let parameter_value be step.parameter
        Let amplitude be MathOps.maximum[MathOps.absolute[step.solution[0]], MathOps.absolute[step.solution[1]]]
        Print("  ε = " + parameter_value.to_string[] + ", Amplitude ≈ " + amplitude.to_string[])
    
    Return continuation_result
```

### Multi-Parameter Analysis

```runa
Process called "analyze_codimension_two_bifurcation":
    Note: System with two parameters exhibiting cusp bifurcation
    Let cusp_system be Function.create[
        inputs: ["state", "time", "parameters"],
        body: {
            Let x be state[0]
            Let alpha be parameters["alpha"]
            Let beta be parameters["beta"]
            
            Return [alpha + beta * x + x * x * x]
        }
    ]
    
    Note: Analyze bifurcations in two-parameter space
    Let codim2_analysis be Bifurcation.analyze_codimension_two[
        cusp_system,
        parameter_ranges: [("alpha", -1.0, 1.0), ("beta", -2.0, 2.0)],
        initial_conditions: [0.0],
        grid_resolution: [50, 50]
    ]
    
    Print("Codimension-2 Analysis Results:")
    Print("  Cusp point location: " + codim2_analysis.organizing_centers[0].to_string[])
    Print("  Saddle-node curves: " + codim2_analysis.bifurcation_curves.length.to_string[])
    
    Note: Identify organizing center (cusp point)
    Let cusp_point be codim2_analysis.organizing_centers[0]
    Print("  Cusp organizing center at (α*, β*) = (" + 
          cusp_point.parameters["alpha"].to_string[] + ", " +
          cusp_point.parameters["beta"].to_string[] + ")")
    
    Return codim2_analysis
```

## Global Bifurcation Analysis

### Homoclinic Bifurcations

```runa
Process called "detect_homoclinic_bifurcation":
    Note: System with homoclinic orbit
    Let homoclinic_system be Function.create[
        inputs: ["state", "time", "parameter"],
        body: {
            Let x be state[0]
            Let y be state[1]
            Let c be parameter
            
            Return [y, -x + c * y - y * y * y]
        }
    ]
    
    Let homoclinic_analysis be Bifurcation.detect_homoclinic_bifurcation[
        homoclinic_system,
        parameter_range: (0.0, 2.0),
        saddle_point: [0.0, 0.0],
        search_radius: 5.0,
        integration_time: 100.0
    ]
    
    Print("Homoclinic Bifurcation Analysis:")
    
    For Each homoclinic_point in homoclinic_analysis.homoclinic_bifurcations:
        Print("  Homoclinic bifurcation at c* = " + homoclinic_point.parameter_value.to_string[])
        Print("  Orbit period: " + homoclinic_point.orbit_period.to_string[])
        Print("  Separatrix splitting: " + homoclinic_point.splitting_measure.to_string[])
        
        Note: Homoclinic bifurcations often lead to chaos
        If homoclinic_point.generates_chaos:
            Print("  Leads to chaotic dynamics")
    
    Return homoclinic_analysis
```

### Period-Doubling Cascades

```runa
Process called "analyze_period_doubling_cascade":
    Note: Logistic map: x_{n+1} = rx_n(1-x_n)
    Let logistic_map be Function.create[
        inputs: ["state", "parameter"],
        body: {
            Let x be state[0]
            Let r be parameter
            Return [r * x * (1.0 - x)]
        }
    ]
    
    Let cascade_analysis be Bifurcation.analyze_period_doubling_cascade[
        logistic_map,
        parameter_range: (2.8, 4.0),
        initial_condition: [0.5],
        max_period: 512,
        resolution: 1000
    ]
    
    Print("Period-Doubling Cascade Analysis:")
    Print("  Route to chaos via period-doubling bifurcations")
    
    Let bifurcation_points be cascade_analysis.period_doubling_points
    Print("  Period-doubling points found: " + bifurcation_points.length.to_string[])
    
    Note: Compute Feigenbaum constant δ ≈ 4.669...
    If bifurcation_points.length >= 3:
        Let r1 be bifurcation_points[0].parameter_value
        Let r2 be bifurcation_points[1].parameter_value
        Let r3 be bifurcation_points[2].parameter_value
        
        Let delta be (r1 - r2) / (r2 - r3)
        Print("  Feigenbaum constant δ ≈ " + delta.to_string[])
        Print("  Theoretical value: δ = 4.669201...")
    
    Note: Identify onset of chaos
    Let chaos_onset be cascade_analysis.chaos_threshold
    Print("  Chaos begins at r ≈ " + chaos_onset.to_string[])
    
    Return cascade_analysis
```

## Normal Form Analysis

### Computing Canonical Forms

```runa
Process called "compute_bifurcation_normal_forms":
    Note: General system near bifurcation point
    Let system_near_bifurcation be Function.create[
        inputs: ["state", "time", "parameters"],
        body: {
            Let x be state[0]
            Let y be state[1]
            Let mu be parameters["mu"]
            Let nu be parameters["nu"]
            
            Note: Generic 2D system with parameters
            Return [
                mu * x - y + nu * x * x - x * y * y,
                x + mu * y - x * x * y + nu * y * y * y
            ]
        }
    ]
    
    Note: Compute normal form near Hopf bifurcation
    Let normal_form_analysis be Bifurcation.compute_normal_form[
        system_near_bifurcation,
        bifurcation_type: "hopf",
        bifurcation_point: [0.0, 0.0],
        parameter_values: Dictionary.from_pairs[("mu", 0.0), ("nu", 0.0)],
        truncation_order: 3
    ]
    
    Print("Normal Form Analysis:")
    Print("  Bifurcation type: " + normal_form_analysis.bifurcation_type)
    Print("  Normal form order: " + normal_form_analysis.truncation_order.to_string[])
    
    Let coefficients be normal_form_analysis.normal_form_coefficients
    Print("  Linear coefficients: " + coefficients.linear.to_string[])
    Print("  Cubic coefficients: " + coefficients.cubic.to_string[])
    
    Note: Determine criticality from first Lyapunov coefficient
    Let lyapunov_coeff be coefficients.first_lyapunov_coefficient
    If lyapunov_coeff < 0.0:
        Print("  Supercritical Hopf: Stable limit cycle")
    Otherwise:
        Print("  Subcritical Hopf: Unstable limit cycle")
    
    Return normal_form_analysis
```

## Bifurcation Diagram Construction

### Complete Diagram Generation

```runa
Process called "generate_comprehensive_bifurcation_diagram":
    Note: Duffing oscillator with rich bifurcation structure
    Let duffing_system be Function.create[
        inputs: ["state", "time", "parameters"],
        body: {
            Let x be state[0]
            Let v be state[1]
            Let gamma be parameters["gamma"]  Note: Damping
            Let alpha be parameters["alpha"]  Note: Linear stiffness
            Let beta be parameters["beta"]    Note: Nonlinear stiffness
            Let f be parameters["f"]          Note: Forcing amplitude
            Let omega be parameters["omega"]  Note: Forcing frequency
            
            Return [
                v,
                -gamma * v - alpha * x - beta * x * x * x + f * MathOps.cosine[omega * state[2]]
            ]
        }
    ]
    
    Note: Generate bifurcation diagram varying forcing amplitude
    Let comprehensive_diagram be Bifurcation.generate_bifurcation_diagram[
        duffing_system,
        primary_parameter: "f",
        parameter_range: (0.0, 2.0),
        fixed_parameters: Dictionary.from_pairs[
            ("gamma", 0.1),
            ("alpha", -1.0),
            ("beta", 1.0),
            ("omega", 1.0)
        ],
        initial_conditions: [[0.1, 0.1, 0.0]],
        transient_time: 100.0,
        sampling_time: 100.0,
        resolution: 500
    ]
    
    Print("Comprehensive Bifurcation Diagram:")
    Print("  Parameter range: [0.0, 2.0]")
    Print("  Bifurcation points detected: " + comprehensive_diagram.bifurcation_points.length.to_string[])
    Print("  Periodic windows: " + comprehensive_diagram.periodic_windows.length.to_string[])
    Print("  Chaotic regions: " + comprehensive_diagram.chaotic_regions.length.to_string[])
    
    Note: Identify major bifurcation types
    For Each bifurcation in comprehensive_diagram.bifurcation_points:
        Print("  f = " + bifurcation.parameter_value.to_string[] + 
              ": " + bifurcation.bifurcation_type.to_string[])
    
    Return comprehensive_diagram
```

## Error Handling and Validation

### Numerical Robustness

```runa
Process called "robust_bifurcation_analysis":
    Try:
        Let sensitive_system be create_stiff_system[]  Note: Numerically challenging system
        
        Let diagram be Bifurcation.analyze_saddle_node_bifurcation[
            sensitive_system,
            parameter_range: (-0.1, 0.1),
            initial_conditions: [1e-6],
            tolerance: 1e-14,
            adaptive_stepping: true
        ]
        
        Note: Validate results using multiple methods
        Let validation_diagram be Bifurcation.validate_bifurcation_analysis[
            diagram,
            alternative_method: "arc_length_continuation",
            cross_check_tolerance: 1e-10
        ]
        
        If validation_diagram.consistency_check:
            Print("Bifurcation analysis validated successfully")
        Otherwise:
            Print("Warning: Inconsistent results between methods")
            Print("Recommend using higher precision or different approach")
        
    Catch error as Errors.NumericalInstability:
        Print("Numerical instability detected")
        Print("Recommendation: Reduce parameter step size or increase precision")
    
    Catch error as Errors.BifurcationDetectionFailure:
        Print("Failed to detect bifurcation points")
        Print("Try different initial conditions or parameter range")
    
    Catch error as Errors.ContinuationFailure:
        Print("Parameter continuation failed")
        Print("May indicate fold point or discontinuous branch")
```

## Advanced Applications

### Biological System Example

```runa
Process called "analyze_predator_prey_bifurcations":
    Note: Rosenzweig-MacArthur predator-prey model
    Let predator_prey_system be Function.create[
        inputs: ["state", "time", "parameters"],
        body: {
            Let N be state[0]  Note: Prey density
            Let P be state[1]  Note: Predator density
            Let r be parameters["r"]    Note: Prey growth rate
            Let K be parameters["K"]    Note: Carrying capacity
            Let a be parameters["a"]    Note: Attack rate
            Let h be parameters["h"]    Note: Handling time
            Let e be parameters["e"]    Note: Conversion efficiency
            Let d be parameters["d"]    Note: Predator death rate
            
            Let consumption be (a * N) / (1.0 + a * h * N)
            
            Return [
                r * N * (1.0 - N / K) - consumption * P,
                e * consumption * P - d * P
            ]
        }
    ]
    
    Note: Analyze bifurcations as carrying capacity varies
    Let ecological_diagram be Bifurcation.generate_bifurcation_diagram[
        predator_prey_system,
        primary_parameter: "K",
        parameter_range: (5.0, 50.0),
        fixed_parameters: Dictionary.from_pairs[
            ("r", 1.0), ("a", 1.0), ("h", 0.1), ("e", 0.75), ("d", 0.5)
        ],
        initial_conditions: [[10.0, 2.0]],
        resolution: 200
    ]
    
    Print("Predator-Prey Bifurcation Analysis:")
    Print("  Ecological interpretation of bifurcations:")
    
    For Each bifurcation in ecological_diagram.bifurcation_points:
        Let K_critical be bifurcation.parameter_value
        
        If bifurcation.bifurcation_type.hopf_supercritical:
            Print("  K = " + K_critical.to_string[] + ": Onset of population cycles")
            Print("  Ecological meaning: Predator-prey oscillations emerge")
        
        If bifurcation.bifurcation_type.saddle_node:
            Print("  K = " + K_critical.to_string[] + ": Extinction threshold")
            Print("  Ecological meaning: Minimum viable population size")
    
    Return ecological_diagram
```

## Best Practices

### Analysis Guidelines

1. **Parameter Range Selection**: Choose ranges that capture full bifurcation structure
2. **Resolution Control**: Balance computational cost with accuracy requirements
3. **Multiple Initial Conditions**: Test different starting points for completeness
4. **Validation**: Cross-check results with analytical theory when available

### Numerical Considerations

1. **Precision Management**: Use high precision near bifurcation points
2. **Step Size Adaptation**: Employ adaptive methods for parameter continuation
3. **Convergence Monitoring**: Check for proper convergence in iterative methods
4. **Stability Assessment**: Verify numerical stability throughout parameter range

### Interpretation Strategies

1. **Physical Meaning**: Connect mathematical bifurcations to system behavior
2. **Parameter Significance**: Understand the role of each bifurcation parameter
3. **Robustness Testing**: Assess sensitivity to parameter perturbations
4. **Experimental Validation**: Compare theoretical predictions with observations

## Integration with Other Modules

- **Dynamical Systems**: Foundation for stability and flow analysis
- **Chaos Theory**: Analysis of chaotic regions in bifurcation diagrams  
- **Numerical Methods**: ODE solvers and continuation algorithms
- **Optimization**: Parameter estimation and model fitting
- **Statistical Analysis**: Uncertainty quantification in bifurcation points

## See Also

- [Dynamical Systems Guide](systems.md) - Foundation stability analysis
- [Chaos Theory Guide](chaos.md) - Chaotic behavior analysis
- [Dynamical Module Overview](README.md) - Module introduction and examples
- [Numerical Methods Documentation](../engine/numerical/README.md) - Continuation algorithms
- [Optimization Documentation](../optimization/README.md) - Parameter estimation