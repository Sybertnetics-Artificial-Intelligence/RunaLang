# Tensor Calculus Operations

The Tensor Calculus module (`math/tensors/calculus`) provides comprehensive tensor calculus operations for curved spaces and general coordinate systems. This module extends vector calculus to arbitrary manifolds, implementing covariant derivatives, curvature analysis, and the mathematical framework essential for differential geometry and general relativity.

## Overview

The Tensor Calculus module offers powerful differential operations including:

- **Covariant Derivatives**: Parallel transport and connection-dependent differentiation
- **Christoffel Symbols**: Connection coefficients for curved spaces
- **Curvature Tensors**: Riemann, Ricci, and Weyl curvature analysis
- **Einstein Summation**: Automatic index summation conventions
- **Geodesic Equations**: Shortest path computations in curved space
- **Parallel Transport**: Vector transport along curves preserving inner products
- **Lie Derivatives**: Directional derivatives along vector fields

## Mathematical Foundation

### Covariant Derivatives

The covariant derivative extends ordinary partial derivatives to curved spaces:

- **Covariant Vector**: ∇ᵢTⱼ = ∂Tⱼ/∂xⁱ - Γᵏᵢⱼ Tₖ
- **Contravariant Vector**: ∇ᵢTʲ = ∂Tʲ/∂xⁱ + Γʲᵢₖ Tᵏ  
- **Mixed Tensor**: ∇ᵢTʲₖ = ∂Tʲₖ/∂xⁱ + ΓʲᵢₗTˡₖ - ΓˡᵢₖTʲₗ
- **Metric Compatibility**: ∇ᵢgⱼₖ = 0 (Levi-Civita connection)

### Christoffel Symbols

Connection coefficients defined by the metric tensor:

- **Definition**: Γᵏᵢⱼ = ½gᵏˡ(∂gᵢˡ/∂xʲ + ∂gⱼˡ/∂xⁱ - ∂gᵢⱼ/∂xˡ)
- **Symmetry**: Γᵏᵢⱼ = Γᵏⱼᵢ (torsion-free connection)
- **Transformation**: Non-tensor transformation under coordinate changes

## Core Data Structures

### Tensor Index Structure

```runa
Type called "TensorIndex":
    position as String          # "upper" or "lower"
    label as String            # Index identifier  
    range_size as Integer      # Index ranges from 0 to range_size-1
    coordinate_system as String # Coordinate system type
```

### Tensor Representation

```runa
Type called "Tensor":
    components as List[List[Float64]]    # Multi-dimensional component array
    indices as List[TensorIndex]         # Index structure information
    rank as Integer                      # Total number of indices
    dimension as Integer                 # Spacetime/space dimension
    coordinate_system as String          # Coordinate system used
    metric_compatible as Boolean         # Whether compatible with metric
    symmetries as List[String]           # Symmetry properties
```

### Metric Tensor Structure

```runa
Type called "MetricTensor":
    components as List[List[Float64]]    # Metric components gᵢⱼ
    dimension as Integer                 # Space/spacetime dimension
    signature as List[Integer]           # Metric signature (+1, -1, etc.)
    determinant as Float64               # det(g) for volume elements
    inverse_components as List[List[Float64]]  # Inverse metric g^ij
    coordinate_system as String          # Coordinate system
    is_riemannian as Boolean            # Positive definite vs Lorentzian
```

## Einstein Summation Convention

### Automatic Index Summation

```runa
Import "math/tensors/calculus" as TensorCalculus

Note: Define tensor components for Einstein summation
Let tensor_components = Dictionary with:
    "T": [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]
    "U": [[2.0, 0.0, 1.0], [1.0, 3.0, 0.0], [0.0, 2.0, 4.0]]
    "g": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]

Note: Simple contraction: T^i_j U^j_k (sum over j)
Let contraction_expression = "T^i_j U^j_k"
Let contracted_result = TensorCalculus.einstein_sum(contraction_expression, tensor_components)

Display "Einstein summation result:"
For i from 0 to 2:
    For k from 0 to 2:
        Display "  Component [" + String(i) + "," + String(k) + "]: " + String(contracted_result[i][k])

Note: More complex expression: g^ij T_i T_j (inner product)
Let inner_product_expr = "g^ij T_i T_j"
Let vector_T = [1.0, 2.0, 3.0]  # Convert for this expression
Let inner_product_components = Dictionary with:
    "g": tensor_components["g"]
    "T": vector_T

Let inner_product_result = TensorCalculus.einstein_sum_scalar(inner_product_expr, inner_product_components)
Display "Inner product result: " + String(inner_product_result)

Note: Trace operation: T^i_i (sum over repeated index)
Let trace_expression = "T^i_i"
Let trace_components = Dictionary with: "T": tensor_components["T"]
Let trace_result = TensorCalculus.einstein_sum_scalar(trace_expression, trace_components)
Display "Trace of tensor T: " + String(trace_result)
```

### Index Validation and Analysis

```runa
Note: Validate Einstein summation expressions
Let valid_expressions = [
    "A^i B_i",           # Valid contraction
    "g^ij T_i T_j",      # Valid scalar
    "R^i_jkl R_i^jkl"    # Valid Riemann scalar
]

Let invalid_expressions = [
    "A^i B^i",           # Two upper indices
    "T_i T_j",           # Free indices don't match
    "g^ij T_i"           # Uncontracted index j
]

For Each expr in valid_expressions:
    Let validation = TensorCalculus.validate_einstein_expression(expr)
    Display "Expression '" + expr + "' is valid: " + String(validation.is_valid)
    If validation.is_valid:
        Display "  Free indices: " + String(validation.free_indices)
        Display "  Dummy indices: " + String(validation.dummy_indices)

For Each expr in invalid_expressions:
    Let validation = TensorCalculus.validate_einstein_expression(expr)
    Display "Expression '" + expr + "' is valid: " + String(validation.is_valid)
    If not validation.is_valid:
        Display "  Error: " + validation.error_message
```

## Christoffel Symbols and Connections

### Computing Connection Coefficients

```runa
Note: Define a curved space metric (spherical coordinates)
Let spherical_metric = TensorCalculus.create_metric_tensor(Dictionary with:
    "dimension": "3"
    "coordinate_system": "spherical"
    "components": [
        [1.0, 0.0, 0.0],                    # g_rr = 1
        [0.0, "r^2", 0.0],                  # g_θθ = r²  
        [0.0, 0.0, "r^2 * sin^2(theta)"]   # g_φφ = r²sin²θ
    ]
    "coordinates": ["r", "theta", "phi"]
    "symbolic": "true"
})

Note: Compute Christoffel symbols
Let christoffel_symbols = TensorCalculus.compute_christoffel_symbols(spherical_metric)

Display "Christoffel symbols in spherical coordinates:"
Display "  Γʳₜₜ = " + christoffel_symbols.components["Gamma^r_theta_theta"]
Display "  Γʳᵩᵩ = " + christoffel_symbols.components["Gamma^r_phi_phi"]
Display "  Γᵗᵣₜ = " + christoffel_symbols.components["Gamma^theta_r_theta"]
Display "  Γᵩᵣᵩ = " + christoffel_symbols.components["Gamma^phi_r_phi"]
Display "  Γᵩᵩₜ = " + christoffel_symbols.components["Gamma^phi_phi_theta"]

Note: Verify symmetry property: Γᵏᵢⱼ = Γᵏⱼᵢ
Let symmetry_check = TensorCalculus.verify_christoffel_symmetry(christoffel_symbols)
Display "Christoffel symbol symmetry verified: " + String(symmetry_check.is_symmetric)

Note: Check that Christoffel symbols are not tensors
Let coordinate_transform = TensorCalculus.create_coordinate_transformation(
    "spherical_to_cartesian",
    ["r", "theta", "phi"],
    ["x", "y", "z"]
)

Let transformed_christoffels = TensorCalculus.transform_christoffel_symbols(
    christoffel_symbols, 
    coordinate_transform
)

Note: Compare with direct computation in new coordinates
Let cartesian_metric = TensorCalculus.transform_metric(spherical_metric, coordinate_transform)
Let direct_christoffels = TensorCalculus.compute_christoffel_symbols(cartesian_metric)

Let tensor_comparison = TensorCalculus.compare_as_tensors(transformed_christoffels, direct_christoffels)
Display "Christoffel symbols transform as tensors: " + String(tensor_comparison.transforms_as_tensor)
Display "Additional transformation terms present: " + String(not tensor_comparison.transforms_as_tensor)
```

### Connection Properties

```runa
Note: Verify metric compatibility: ∇ᵢgⱼₖ = 0
Let covariant_derivative_metric = TensorCalculus.covariant_derivative(
    spherical_metric.components,
    christoffel_symbols,
    Dictionary with: "tensor_type": "covariant_2"
)

Let metric_compatibility_check = TensorCalculus.is_zero_tensor(covariant_derivative_metric, "1e-12")
Display "Metric compatibility verified: ∇ᵢgⱼₖ = 0: " + String(metric_compatibility_check)

Note: Verify torsion-free condition: Γᵏᵢⱼ = Γᵏⱼᵢ  
Let torsion_tensor = TensorCalculus.compute_torsion_tensor(christoffel_symbols)
Let torsion_free_check = TensorCalculus.is_zero_tensor(torsion_tensor, "1e-12")
Display "Torsion-free connection verified: " + String(torsion_free_check)

Note: Compute connection determinant and volume element
Let connection_determinant = TensorCalculus.connection_determinant(christoffel_symbols)
let volume_element = TensorCalculus.compute_volume_element(spherical_metric)
Display "Volume element in spherical coordinates: " + volume_element.expression
```

## Covariant Derivatives

### Vector Field Derivatives

```runa
Note: Define vector fields in curved space
Let vector_field = TensorCalculus.create_tensor_field(Dictionary with:
    "type": "contravariant_vector"
    "dimension": "3"
    "components": ["V^r(r,θ,φ)", "V^θ(r,θ,φ)", "V^φ(r,θ,φ)"]
    "coordinate_system": "spherical"
    "symbolic": "true"
})

Note: Compute covariant derivative: ∇ⱼVⁱ = ∂Vⁱ/∂xʲ + ΓⁱⱼₖVᵏ
Let covariant_derivative_V = TensorCalculus.covariant_derivative(
    vector_field,
    christoffel_symbols,
    Dictionary with:
        "derivative_index": "covariant"
        "tensor_type": "contravariant_vector"
)

Display "Covariant derivative of vector field:"
Display "  ∇ᵣVʳ = " + covariant_derivative_V.components["nabla_r_V^r"]
Display "  ∇ₜVʳ = " + covariant_derivative_V.components["nabla_theta_V^r"]
Display "  ∇ᵩVᵗ = " + covariant_derivative_V.components["nabla_phi_V^theta"]

Note: Covector field derivatives  
Let covector_field = TensorCalculus.create_tensor_field(Dictionary with:
    "type": "covariant_vector"
    "dimension": "3" 
    "components": ["W_r(r,θ,φ)", "W_θ(r,θ,φ)", "W_φ(r,θ,φ)"]
    "coordinate_system": "spherical"
    "symbolic": "true"
})

Note: ∇ⱼWᵢ = ∂Wᵢ/∂xʲ - ΓᵏⱼᵢWₖ
Let covariant_derivative_W = TensorCalculus.covariant_derivative(
    covector_field,
    christoffel_symbols,
    Dictionary with: "tensor_type": "covariant_vector"
)

Display "Covariant derivative of covector field:"
Display "  ∇ᵣWᵣ = " + covariant_derivative_W.components["nabla_r_W_r"]
Display "  ∇ₜWᵣ = " + covariant_derivative_W.components["nabla_theta_W_r"]
```

### Tensor Field Derivatives

```runa
Note: Mixed tensor covariant derivatives
Let mixed_tensor_field = TensorCalculus.create_tensor_field(Dictionary with:
    "type": "mixed_tensor"
    "contravariant_degree": "1"
    "covariant_degree": "1"
    "dimension": "3"
    "components": [
        ["T¹₁", "T¹₂", "T¹₃"],
        ["T²₁", "T²₂", "T²₃"], 
        ["T³₁", "T³₂", "T³₃"]
    ]
    "symbolic": "true"
})

Note: ∇ₖTⁱⱼ = ∂Tⁱⱼ/∂xᵏ + ΓⁱₖₗTˡⱼ - ΓˡₖⱼTⁱˡ
Let mixed_covariant_derivative = TensorCalculus.covariant_derivative(
    mixed_tensor_field,
    christoffel_symbols,
    Dictionary with: "tensor_type": "mixed_1_1"
)

Display "Mixed tensor covariant derivative computed"
Display "Number of derivative components: " + String(mixed_covariant_derivative.total_components)

Note: Verify covariant derivative properties
Note: Leibniz rule: ∇ₖ(AB) = A∇ₖB + B∇ₖA for scalars A, B
Let scalar_A = TensorCalculus.create_scalar_field("f(r,θ,φ)")
Let scalar_B = TensorCalculus.create_scalar_field("g(r,θ,φ)")
Let product_field = TensorCalculus.multiply_scalar_fields(scalar_A, scalar_B)

Let derivative_product = TensorCalculus.covariant_derivative(product_field, christoffel_symbols)
Let product_of_derivatives = TensorCalculus.add_tensor_fields(
    TensorCalculus.multiply_tensor_fields(scalar_A, TensorCalculus.covariant_derivative(scalar_B, christoffel_symbols)),
    TensorCalculus.multiply_tensor_fields(scalar_B, TensorCalculus.covariant_derivative(scalar_A, christoffel_symbols))
)

Let leibniz_check = TensorCalculus.tensor_fields_equal(derivative_product, product_of_derivatives, "symbolic")
Display "Leibniz rule verified: " + String(leibniz_check)
```

## Curvature Tensors

### Riemann Curvature Tensor

```runa
Note: Compute Riemann curvature tensor
Note: Rⁱⱼₖₗ = ∂Γⁱⱼₗ/∂xᵏ - ∂Γⁱⱼₖ/∂xˡ + ΓⁱₘₖΓᵐⱼₗ - ΓⁱₘₗΓᵐⱼₖ
Let riemann_tensor = TensorCalculus.compute_riemann_tensor(christoffel_symbols, spherical_metric)

Display "Riemann curvature tensor computed"
Display "Non-zero components in spherical coordinates:"

Note: Display only non-zero components (many vanish by symmetry)
Let non_zero_components = TensorCalculus.find_nonzero_components(riemann_tensor, "1e-12")
For Each component in non_zero_components:
    Display "  " + component.index_string + " = " + component.value

Note: Verify Riemann tensor symmetries
Let symmetry_analysis = TensorCalculus.analyze_riemann_symmetries(riemann_tensor)

Display "Riemann tensor symmetry properties:"
Display "  Antisymmetric in last two indices: " + String(symmetry_analysis.antisymmetric_34)
Display "  Antisymmetric in first pair: " + String(symmetry_analysis.antisymmetric_12)
Display "  Symmetric under pair exchange: " + String(symmetry_analysis.symmetric_pairs)
Display "  First Bianchi identity satisfied: " + String(symmetry_analysis.first_bianchi)

Note: Check second Bianchi identity: ∇[ₐRᵇc]dₑ = 0
Let second_bianchi_check = TensorCalculus.verify_second_bianchi_identity(riemann_tensor, christoffel_symbols)
Display "Second Bianchi identity verified: " + String(second_bianchi_check)
```

### Ricci Tensor and Scalar

```runa
Note: Contract Riemann tensor to get Ricci tensor
Note: Rᵢⱼ = Rᵏᵢₖⱼ (contraction of first and third indices)
Let ricci_tensor = TensorCalculus.ricci_tensor_from_riemann(riemann_tensor)

Display "Ricci tensor components:"
For i from 0 to 2:
    For j from 0 to 2:
        Let component_value = ricci_tensor.components[i][j]
        If abs(component_value) > 1e-12:
            Display "  R_" + String(i) + String(j) + " = " + String(component_value)

Note: Compute Ricci scalar: R = gⁱʲRᵢⱼ
Let inverse_metric = TensorCalculus.compute_metric_inverse(spherical_metric)
Let ricci_scalar = TensorCalculus.ricci_scalar_from_ricci(ricci_tensor, inverse_metric)

Display "Ricci scalar R = " + String(ricci_scalar)

Note: For flat space, Riemann tensor should vanish
Let flat_metric = TensorCalculus.create_metric_tensor(Dictionary with:
    "dimension": "3"
    "coordinate_system": "cartesian"
    "signature": "euclidean"
    "components": [
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0], 
        [0.0, 0.0, 1.0]
    ]
})

Let flat_christoffels = TensorCalculus.compute_christoffel_symbols(flat_metric)
Let flat_riemann = TensorCalculus.compute_riemann_tensor(flat_christoffels, flat_metric)
Let is_flat = TensorCalculus.is_zero_tensor(flat_riemann, "1e-12")

Display "Flat space has zero curvature: " + String(is_flat)
```

### Einstein Tensor

```runa
Note: Compute Einstein tensor: Gᵢⱼ = Rᵢⱼ - ½gᵢⱼR
Let einstein_tensor = TensorCalculus.compute_einstein_tensor(ricci_tensor, ricci_scalar, spherical_metric)

Display "Einstein tensor components:"
For i from 0 to 2:
    For j from 0 to 2:
        Let component_value = einstein_tensor.components[i][j] 
        If abs(component_value) > 1e-12:
            Display "  G_" + String(i) + String(j) + " = " + String(component_value)

Note: Verify Einstein tensor properties
Note: Contracted Bianchi identity: ∇ⁱGᵢⱼ = 0
Let bianchi_verification = TensorCalculus.verify_contracted_bianchi_identity(einstein_tensor, christoffel_symbols)
Display "Contracted Bianchi identity satisfied: " + String(bianchi_verification)

Note: Einstein tensor is symmetric
Let symmetry_check = TensorCalculus.check_tensor_symmetry(einstein_tensor, [0, 1])
Display "Einstein tensor is symmetric: " + String(symmetry_check.is_symmetric)

Note: Trace relation: G = R - (d/2)R where d is dimension
Let einstein_trace = TensorCalculus.tensor_trace(einstein_tensor, inverse_metric)
Let expected_trace = ricci_scalar - (3.0/2.0) * ricci_scalar  # d=3
Let trace_relation_check = abs(einstein_trace - expected_trace) < 1e-12
Display "Einstein tensor trace relation verified: " + String(trace_relation_check)
```

## Geodesic Equations

### Geodesic Computation

```runa
Note: Compute geodesic equations: d²xᵏ/dτ² + Γᵏᵢⱼ(dxⁱ/dτ)(dxʲ/dτ) = 0
Let geodesic_equations = TensorCalculus.derive_geodesic_equations(christoffel_symbols)

Display "Geodesic equations in spherical coordinates:"
Display "  d²r/dτ² = " + geodesic_equations.components["d2r_dtau2"]
Display "  d²θ/dτ² = " + geodesic_equations.components["d2theta_dtau2"]
Display "  d²φ/dτ² = " + geodesic_equations.components["d2phi_dtau2"]

Note: Solve geodesic with initial conditions
Let initial_conditions = Dictionary with:
    "r_0": "1.0"      # Initial radial coordinate
    "theta_0": "π/2"  # Initial polar angle
    "phi_0": "0.0"    # Initial azimuthal angle
    "dr_dtau_0": "0.0"      # Initial radial velocity
    "dtheta_dtau_0": "0.0"  # Initial polar velocity  
    "dphi_dtau_0": "1.0"    # Initial azimuthal velocity

Let geodesic_solution = TensorCalculus.solve_geodesic(
    geodesic_equations,
    initial_conditions,
    Dictionary with:
        "parameter_range": "[0, 2π]"
        "integration_method": "runge_kutta_4"
        "step_size": "0.01"
)

Display "Geodesic solution computed"
Display "Trajectory points: " + String(Length(geodesic_solution.trajectory))

Note: Verify geodesic properties
Let arc_length = TensorCalculus.compute_arc_length(geodesic_solution.trajectory, spherical_metric)
let proper_time = TensorCalculus.compute_proper_time(geodesic_solution.trajectory, spherical_metric)

Display "Arc length along geodesic: " + String(arc_length)
Display "Proper time parameter: " + String(proper_time)

Note: Check that geodesic extremizes distance
Let varied_path = TensorCalculus.create_varied_path(geodesic_solution.trajectory, "small_perturbation")
Let varied_length = TensorCalculus.compute_arc_length(varied_path, spherical_metric)
Let extremality_check = arc_length < varied_length
Display "Geodesic extremizes arc length: " + String(extremality_check)
```

### Geodesic Deviation

```runa
Note: Geodesic deviation equation measures tidal forces
Note: D²ηᵃ/Dτ² = Rᵃᵦᶜᵈ uᵇ uᶜ ηᵈ where η is deviation vector
Let reference_geodesic = geodesic_solution
Let deviation_vector_initial = TensorCalculus.create_tensor([0.01, 0.0, 0.0])  # Small radial deviation

Let geodesic_deviation_eq = TensorCalculus.derive_geodesic_deviation_equation(
    riemann_tensor,
    reference_geodesic
)

Let deviation_solution = TensorCalculus.solve_geodesic_deviation(
    geodesic_deviation_eq,
    deviation_vector_initial,
    reference_geodesic,
    Dictionary with:
        "parameter_range": "[0, 2π]"
        "integration_method": "adaptive"
)

Display "Geodesic deviation computed"
Display "Maximum deviation: " + String(TensorCalculus.max_deviation(deviation_solution))

Note: Analyze tidal effects
Let tidal_tensor = TensorCalculus.compute_tidal_tensor(riemann_tensor, reference_geodesic.four_velocity)
Display "Tidal tensor computed - describes relative acceleration of nearby geodesics"

Note: In flat space, deviation should remain constant
Let flat_deviation = TensorCalculus.solve_geodesic_deviation_flat(
    deviation_vector_initial,
    reference_geodesic
)
let deviation_constancy_check = TensorCalculus.is_constant_vector(flat_deviation, "1e-12")
Display "Flat space deviation remains constant: " + String(deviation_constancy_check)
```

## Parallel Transport

### Vector Transport Along Curves

```runa
Note: Parallel transport preserves inner products and angles
Let curve_parameterization = TensorCalculus.create_parameterized_curve(Dictionary with:
    "parameter": "t"
    "coordinates": ["r(t)", "θ(t)", "φ(t)"]
    "parameter_range": "[0, 1]"
    "coordinate_system": "spherical"
})

Let initial_vector = TensorCalculus.create_tensor([1.0, 0.5, 0.0])  # Initial vector to transport
Let transport_equation = TensorCalculus.derive_parallel_transport_equation(
    christoffel_symbols,
    curve_parameterization
)

Note: DVⁱ/Dt + Γⁱⱼₖ Vʲ (dxᵏ/dt) = 0
Let transported_vector = TensorCalculus.solve_parallel_transport(
    transport_equation,
    initial_vector,
    curve_parameterization,
    Dictionary with: "integration_method": "runge_kutta_4"
)

Display "Parallel transport completed"
Display "Initial vector magnitude: " + String(TensorCalculus.vector_magnitude(initial_vector, spherical_metric))
Display "Final vector magnitude: " + String(TensorCalculus.vector_magnitude(transported_vector.final_vector, spherical_metric))

Note: Verify magnitude preservation
Let magnitude_preserved = abs(
    TensorCalculus.vector_magnitude(initial_vector, spherical_metric) - 
    TensorCalculus.vector_magnitude(transported_vector.final_vector, spherical_metric)
) < 1e-12
Display "Vector magnitude preserved: " + String(magnitude_preserved)

Note: Parallel transport around closed curve (holonomy)
Let closed_curve = TensorCalculus.create_closed_curve(Dictionary with:
    "curve_type": "circle"
    "radius": "1.0"
    "center": [1.0, π/2, 0.0]
    "coordinate_system": "spherical"
})

Let holonomy_transport = TensorCalculus.parallel_transport_closed_curve(
    initial_vector,
    closed_curve,
    christoffel_symbols
)

Let holonomy_angle = TensorCalculus.compute_holonomy_angle(
    initial_vector,
    holonomy_transport.final_vector,
    spherical_metric
)

Display "Holonomy angle around closed curve: " + String(holonomy_angle) + " radians"
Display "Curvature detected through holonomy: " + String(abs(holonomy_angle) > 1e-12)
```

### Connection and Curvature Relationship

```runa
Note: Curvature as obstruction to parallel transport
Note: [∇ᵢ, ∇ⱼ]Vᵏ = RᵏₗᵢⱼVˡ (commutator gives curvature)

Let test_vector_field = TensorCalculus.create_tensor_field(Dictionary with:
    "type": "contravariant_vector"
    "components": ["V^r", "V^θ", "V^φ"] 
    "symbolic": "true"
})

Note: Compute commutator of covariant derivatives
Let commutator_result = TensorCalculus.compute_covariant_derivative_commutator(
    test_vector_field,
    christoffel_symbols,
    [0, 1]  # Commute ∇_r and ∇_θ
)

Note: Compare with Riemann tensor contraction
Let riemann_contraction = TensorCalculus.contract_riemann_with_vector(
    riemann_tensor,
    test_vector_field,
    [0, 1]  # Same indices as commutator
)

Let commutator_riemann_equality = TensorCalculus.tensor_fields_equal(
    commutator_result, 
    riemann_contraction,
    "symbolic"
)
Display "Commutator equals Riemann contraction: " + String(commutator_riemann_equality)
Display "This verifies [∇ᵢ, ∇ⱼ]Vᵏ = RᵏₗᵢⱼVˡ"
```

## Lie Derivatives

### Directional Derivatives Along Vector Fields

```runa
Note: Lie derivative measures change along flow of vector field
Let vector_field_X = TensorCalculus.create_vector_field(Dictionary with:
    "components": ["∂/∂φ", "0", "0"]  # Rotation vector field
    "coordinate_system": "spherical"
    "symbolic": "true"
})

Let tensor_field_T = TensorCalculus.create_tensor_field(Dictionary with:
    "type": "covariant_vector"
    "components": ["T_r", "T_θ", "T_φ"]
    "symbolic": "true"
})

Note: Lie derivative: £_X T_μ = X^ν ∂T_μ/∂x^ν + T_ν ∂X^ν/∂x^μ
Let lie_derivative = TensorCalculus.lie_derivative(tensor_field_T, vector_field_X)

Display "Lie derivative computed:"
Display "  £_X T_r = " + lie_derivative.components["LieD_X_T_r"]
Display "  £_X T_θ = " + lie_derivative.components["LieD_X_T_θ"]  
Display "  £_X T_φ = " + lie_derivative.components["LieD_X_T_phi"]

Note: For metric tensor, Lie derivative gives Killing equation
Let lie_derivative_metric = TensorCalculus.lie_derivative(spherical_metric, vector_field_X)
Let is_killing = TensorCalculus.is_zero_tensor(lie_derivative_metric, "symbolic")

Display "Vector field X is Killing: " + String(is_killing)
If is_killing:
    Display "X generates isometries (rotations preserve metric)"

Note: Lie bracket of vector fields
Let vector_field_Y = TensorCalculus.create_vector_field(Dictionary with:
    "components": ["∂/∂θ", "0", "0"]  # Polar direction
    "coordinate_system": "spherical"  
    "symbolic": "true"
})

Let lie_bracket = TensorCalculus.lie_bracket(vector_field_X, vector_field_Y)
Display "Lie bracket [X,Y] computed:"
Display "  Components: " + String(lie_bracket.components)

Note: Jacobi identity: [X,[Y,Z]] + [Y,[Z,X]] + [Z,[X,Y]] = 0
Let vector_field_Z = TensorCalculus.create_vector_field(Dictionary with:
    "components": ["∂/∂r", "0", "0"]
    "symbolic": "true"
})

Let jacobi_verification = TensorCalculus.verify_jacobi_identity(vector_field_X, vector_field_Y, vector_field_Z)
Display "Jacobi identity satisfied: " + String(jacobi_verification)
```

## Advanced Applications

### General Relativity Tensors

```runa
Note: Schwarzschild metric for black hole spacetime
Let schwarzschild_metric = TensorCalculus.create_metric_tensor(Dictionary with:
    "dimension": "4"
    "coordinate_system": "schwarzschild"  
    "signature": "lorentzian"
    "components": [
        ["-(1-2M/r)", "0", "0", "0"],
        ["0", "1/(1-2M/r)", "0", "0"],
        ["0", "0", "r^2", "0"],
        ["0", "0", "0", "r^2*sin^2(theta)"]
    ]
    "coordinates": ["t", "r", "theta", "phi"]
    "symbolic": "true"
})

Let schwarzschild_christoffels = TensorCalculus.compute_christoffel_symbols(schwarzschild_metric)
Let schwarzschild_riemann = TensorCalculus.compute_riemann_tensor(schwarzschild_christoffels, schwarzschild_metric)
Let schwarzschild_ricci = TensorCalculus.ricci_tensor_from_riemann(schwarzschild_riemann)
Let schwarzschild_scalar = TensorCalculus.ricci_scalar_from_ricci(schwarzschild_ricci, TensorCalculus.compute_metric_inverse(schwarzschild_metric))

Display "Schwarzschild spacetime analysis:"
Display "  Ricci scalar R = " + String(schwarzschild_scalar)
Display "  Vacuum solution (R = 0): " + String(abs(schwarzschild_scalar) < 1e-12)

Note: Compute Weyl tensor (conformal curvature)
Let weyl_tensor = TensorCalculus.compute_weyl_tensor(schwarzschild_riemann, schwarzschild_ricci, schwarzschild_scalar, schwarzschild_metric)
Display "  Weyl tensor computed (describes tidal effects)"

Note: Kretschmann scalar (curvature invariant)
Let kretschmann_scalar = TensorCalculus.kretschmann_invariant(schwarzschild_riemann, TensorCalculus.compute_metric_inverse(schwarzschild_metric))
Display "  Kretschmann scalar K = " + String(kretschmann_scalar)
```

### Cosmological Applications

```runa
Note: Friedmann-Lemaître-Robertson-Walker (FLRW) metric
Let flrw_metric = TensorCalculus.create_metric_tensor(Dictionary with:
    "dimension": "4"
    "coordinate_system": "flrw"
    "signature": "lorentzian"
    "components": [
        ["-1", "0", "0", "0"],
        ["0", "a(t)^2/(1-k*r^2)", "0", "0"],
        ["0", "0", "a(t)^2*r^2", "0"],
        ["0", "0", "0", "a(t)^2*r^2*sin^2(theta)"]
    ]
    "coordinates": ["t", "r", "theta", "phi"]
    "symbolic": "true"
})

Let flrw_einstein = TensorCalculus.compute_einstein_tensor_from_metric(flrw_metric)
Display "FLRW Einstein tensor computed for cosmological models"

Note: Extract Friedmann equations from Einstein tensor
Let friedmann_equations = TensorCalculus.extract_friedmann_equations(flrw_einstein)
Display "Friedmann equations:"
Display "  First: " + friedmann_equations.first_friedmann
Display "  Second: " + friedmann_equations.second_friedmann  
Display "  Continuity: " + friedmann_equations.continuity_equation

Note: Analyze cosmological parameters
Let cosmological_analysis = TensorCalculus.analyze_flrw_cosmology(flrw_metric, friedmann_equations)
Display "Cosmological analysis:"
Display "  Hubble parameter: " + cosmological_analysis.hubble_parameter
Display "  Deceleration parameter: " + cosmological_analysis.deceleration_parameter
Display "  Critical density: " + cosmological_analysis.critical_density
```

## Performance Optimization

### Efficient Curvature Computations

```runa
Note: Optimize tensor calculus for large-dimensional spaces
Let performance_config = Dictionary with:
    "symbolic_computation": "true"
    "parallel_christoffel": "true"
    "sparse_tensor_representation": "true"
    "cache_intermediate_results": "true"
    "dimension_threshold_for_optimization": "10"

TensorCalculus.configure_performance(performance_config)

Note: Benchmark curvature tensor computation
Let high_dim_metric = TensorCalculus.create_random_metric(10, "riemannian")
Let benchmark_start = TensorCalculus.get_time_microseconds()

Let high_dim_christoffels = TensorCalculus.compute_christoffel_symbols(high_dim_metric)
Let high_dim_riemann = TensorCalculus.compute_riemann_tensor(high_dim_christoffels, high_dim_metric)

Let benchmark_end = TensorCalculus.get_time_microseconds()
Display "High-dimensional curvature computation:"
Display "  Dimension: 10"
Display "  Computation time: " + String(benchmark_end - benchmark_start) + " μs"
Display "  Riemann components computed: " + String(high_dim_riemann.total_components)

Note: Memory usage optimization
Let memory_usage = TensorCalculus.analyze_memory_usage(high_dim_riemann)
Display "  Memory usage: " + String(memory_usage.total_bytes) + " bytes"
Display "  Sparsity ratio: " + String(memory_usage.sparsity_ratio)
```

## Error Handling

### Tensor Calculus Validation

```runa
Try:
    Note: Attempt computation with singular metric
    Let singular_metric = TensorCalculus.create_metric_tensor(Dictionary with:
        "dimension": "3"
        "components": [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0]  # Singular
        ]
    })
    
    Let singular_christoffels = TensorCalculus.compute_christoffel_symbols(singular_metric)
    
Catch Errors.SingularMetricError as singular_error:
    Display "Singular metric error: " + singular_error.message
    Display "Metric determinant: " + String(singular_error.determinant)
    Display "Cannot compute connection for singular metric"

Try:
    Note: Attempt invalid covariant derivative
    Let incompatible_tensor = TensorCalculus.create_tensor_field(Dictionary with:
        "dimension": "4"  # Dimension mismatch
        "type": "contravariant_vector"
    })
    
    Let invalid_derivative = TensorCalculus.covariant_derivative(incompatible_tensor, christoffel_symbols)
    
Catch Errors.DimensionMismatchError as dim_error:
    Display "Dimension mismatch: " + dim_error.message
    Display "Tensor dimension: " + String(dim_error.tensor_dimension)
    Display "Connection dimension: " + String(dim_error.connection_dimension)

Try:
    Note: Attempt geodesic with invalid initial conditions
    Let invalid_conditions = Dictionary with:
        "r_0": "-1.0"  # Invalid radial coordinate
        "theta_0": "3*π"  # Outside valid range
    
    Let invalid_geodesic = TensorCalculus.solve_geodesic(geodesic_equations, invalid_conditions)
    
Catch Errors.InvalidInitialConditionsError as ic_error:
    Display "Invalid initial conditions: " + ic_error.message
    Display "Constraint violations: " + String(ic_error.constraint_violations)
```

## Related Documentation

- **[Tensor Algebra](algebra.md)**: Algebraic operations and tensor spaces
- **[Tensor Geometry](geometry.md)**: Spacetime applications and general relativity
- **[Differential Geometry](../geometry/differential.md)**: Manifold theory and smooth structures
- **[Symbolic Calculus](../symbolic/calculus.md)**: Symbolic differentiation and integration
- **[Linear Algebra Engine](../engine/linalg/README.md)**: Matrix operations for tensor components

The Tensor Calculus module provides the mathematical framework essential for differential geometry, general relativity, and advanced physics applications. Its comprehensive implementation of covariant derivatives, curvature analysis, and geometric operations makes it indispensable for theoretical physics and geometric modeling applications.