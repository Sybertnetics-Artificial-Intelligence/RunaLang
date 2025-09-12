# Tensor Algebra Operations

The Tensor Algebra module (`math/tensors/algebra`) provides comprehensive tensor algebra operations and manipulations for multilinear algebra and differential geometry. This module implements the foundational operations for working with tensors as multilinear maps and provides the algebraic structure necessary for advanced mathematical computations.

## Overview

The Tensor Algebra module offers powerful tensor manipulation capabilities including:

- **Basic Tensor Operations**: Addition, scalar multiplication, and tensor composition
- **Tensor Products**: Outer products, inner products, and tensor contractions
- **Symmetry Operations**: Symmetrization, antisymmetrization, and permutation groups
- **Multilinear Algebra**: Operations on tensor spaces and their duals
- **Index Manipulation**: Raising and lowering indices using metric tensors
- **Advanced Operations**: Wedge products, Hodge duality, and exterior algebra

## Mathematical Foundation

### Tensor Spaces

Tensor spaces are constructed as tensor products of vector spaces and their duals:

- **Type (r,s) Tensors**: T^r_s(V) = V⊗...⊗V⊗V*⊗...⊗V* (r contravariant, s covariant indices)
- **Multilinear Maps**: Tensors as functions T: V*×...×V*×V×...×V → ℝ
- **Universal Property**: Tensor products satisfy the universal property in category theory
- **Dimension Formula**: dim(T^r_s(V)) = (dim V)^(r+s)

## Core Data Structures

### Tensor Space Definition

```runa
Type called "TensorSpace":
    base_vector_space_dimension as Integer    # Dimension of underlying vector space
    contravariant_degree as Integer          # Number of upper indices (r)
    covariant_degree as Integer             # Number of lower indices (s)
    total_dimension as Integer              # Total tensor space dimension
    basis_tensors as List[List[Integer]]    # Basis tensor index combinations
    scalar_field as String                  # Field over which tensors are defined
```

### Tensor Element Representation

```runa
Type called "TensorAlgebraElement":
    components as List[Float64]                           # Component values
    tensor_space as TensorSpace                          # Associated tensor space
    index_structure as List[String]                      # Index labeling
    symmetry_properties as List[String]                  # Symmetry constraints
    basis_representation as List[Tuple[List[Integer], Float64]]  # Basis expansion
```

## Basic Tensor Operations

### Tensor Addition

```runa
Import "math/tensors/algebra" as TensorAlgebra

Note: Create tensor space for (1,1) tensors in 3D
Let tensor_space = TensorAlgebra.create_tensor_space(Dictionary with:
    "base_dimension": "3"
    "contravariant_degree": "1"
    "covariant_degree": "1"
    "scalar_field": "real"
)

Note: Create two tensors for addition
Let tensor_a = TensorAlgebra.create_tensor(tensor_space, [
    "1.0", "2.0", "3.0",
    "4.0", "5.0", "6.0", 
    "7.0", "8.0", "9.0"
])

Let tensor_b = TensorAlgebra.create_tensor(tensor_space, [
    "0.5", "1.5", "2.5",
    "3.5", "4.5", "5.5",
    "6.5", "7.5", "8.5"
])

Note: Add tensors component-wise
Let sum_tensor = TensorAlgebra.tensor_addition(tensor_a, tensor_b)
Display "Tensor sum computed with " + String(Length(sum_tensor.components)) + " components"

Note: Verify associativity: (A + B) + C = A + (B + C)
Let tensor_c = TensorAlgebra.create_random_tensor(tensor_space)
Let left_associative = TensorAlgebra.tensor_addition(sum_tensor, tensor_c)
Let right_associative = TensorAlgebra.tensor_addition(tensor_a, TensorAlgebra.tensor_addition(tensor_b, tensor_c))
Let associativity_check = TensorAlgebra.tensors_equal(left_associative, right_associative, "1e-12")
Display "Associativity verified: " + String(associativity_check)
```

### Scalar Multiplication

```runa
Note: Scalar multiplication preserves tensor structure
Let scalar = 3.14159
Let scaled_tensor = TensorAlgebra.scalar_multiplication(scalar, tensor_a)

Display "Original tensor norm: " + TensorAlgebra.tensor_norm(tensor_a)
Display "Scaled tensor norm: " + TensorAlgebra.tensor_norm(scaled_tensor)
Display "Scaling factor: " + String(scalar)

Note: Verify scalar multiplication properties
Let scalar1 = 2.5
Let scalar2 = 4.0
Let combined_scalar = scalar1 * scalar2

Note: Distributivity over tensor addition
Let distributive_left = TensorAlgebra.scalar_multiplication(scalar1, sum_tensor)
Let distributive_right = TensorAlgebra.tensor_addition(
    TensorAlgebra.scalar_multiplication(scalar1, tensor_a),
    TensorAlgebra.scalar_multiplication(scalar1, tensor_b)
)
Let distributivity_check = TensorAlgebra.tensors_equal(distributive_left, distributive_right, "1e-12")
Display "Distributivity verified: " + String(distributivity_check)

Note: Associativity of scalar multiplication
Let associative_left = TensorAlgebra.scalar_multiplication(combined_scalar, tensor_a)
Let associative_right = TensorAlgebra.scalar_multiplication(scalar1, TensorAlgebra.scalar_multiplication(scalar2, tensor_a))
Let scalar_associativity = TensorAlgebra.tensors_equal(associative_left, associative_right, "1e-12")
Display "Scalar associativity verified: " + String(scalar_associativity)
```

## Tensor Products and Contractions

### Tensor Products

```runa
Note: Outer product of tensors increases rank
Let vector_space_3d = TensorAlgebra.create_tensor_space(Dictionary with:
    "base_dimension": "3"
    "contravariant_degree": "1"
    "covariant_degree": "0"  
    "scalar_field": "real"
)

Let covector_space_3d = TensorAlgebra.create_tensor_space(Dictionary with:
    "base_dimension": "3"
    "contravariant_degree": "0"
    "covariant_degree": "1"
    "scalar_field": "real"
)

Let vector_u = TensorAlgebra.create_tensor(vector_space_3d, ["1.0", "2.0", "3.0"])
Let covector_v = TensorAlgebra.create_tensor(covector_space_3d, ["4.0", "5.0", "6.0"])

Note: Form tensor product u ⊗ v
Let outer_product = TensorAlgebra.tensor_product(vector_u, covector_v)
Display "Outer product rank: " + String(outer_product.tensor_space.contravariant_degree + outer_product.tensor_space.covariant_degree)
Display "Outer product dimensions: " + String(Length(outer_product.components))

Note: Verify tensor product properties
Let vector_w = TensorAlgebra.create_tensor(vector_space_3d, ["7.0", "8.0", "9.0"])
Let multilinearity_test = TensorAlgebra.tensor_product(
    TensorAlgebra.tensor_addition(vector_u, vector_w),
    covector_v
)
Let expected_multilinear = TensorAlgebra.tensor_addition(
    TensorAlgebra.tensor_product(vector_u, covector_v),
    TensorAlgebra.tensor_product(vector_w, covector_v)
)
Let multilinearity_check = TensorAlgebra.tensors_equal(multilinearity_test, expected_multilinear, "1e-12")
Display "Multilinearity verified: " + String(multilinearity_check)
```

### Tensor Contractions

```runa
Note: Contraction reduces tensor rank by 2
Let rank_2_tensor = TensorAlgebra.create_tensor(tensor_space, [
    "1.0", "2.0", "3.0",
    "4.0", "5.0", "6.0",
    "7.0", "8.0", "9.0"
])

Note: Contract first upper index with first lower index  
Let contracted_tensor = TensorAlgebra.tensor_contraction(rank_2_tensor, [0, 0])
Display "Original tensor rank: 2"
Display "Contracted tensor rank: " + String(contracted_tensor.tensor_space.contravariant_degree + contracted_tensor.tensor_space.covariant_degree)
Display "Trace (contracted result): " + String(contracted_tensor.components[0])

Note: Multiple contractions for higher-rank tensors
Let rank_4_space = TensorAlgebra.create_tensor_space(Dictionary with:
    "base_dimension": "3"
    "contravariant_degree": "2"
    "covariant_degree": "2"
    "scalar_field": "real"
)

Let rank_4_tensor = TensorAlgebra.create_random_tensor(rank_4_space)
Let double_contraction = TensorAlgebra.multiple_contraction(rank_4_tensor, [
    [0, 2],  # Contract first upper with first lower
    [0, 0]   # Contract remaining upper with remaining lower (after first contraction)
])
Display "Rank 4 tensor fully contracted to scalar: " + String(double_contraction.components[0])
```

### Inner Products and Metrics

```runa
Note: Define metric tensor for inner products
Let metric_tensor = TensorAlgebra.create_metric_tensor(3, Dictionary with:
    "signature": "euclidean"  # Positive definite
    "components": [
        "1.0", "0.0", "0.0",
        "0.0", "1.0", "0.0", 
        "0.0", "0.0", "1.0"
    ]
})

Note: Compute inner product using metric
Let vector1 = TensorAlgebra.create_tensor(vector_space_3d, ["1.0", "2.0", "3.0"])
Let vector2 = TensorAlgebra.create_tensor(vector_space_3d, ["4.0", "5.0", "6.0"])

Let inner_product_result = TensorAlgebra.inner_product(vector1, vector2, metric_tensor)
Display "Inner product ⟨v₁,v₂⟩ = " + String(inner_product_result)

Note: Verify inner product properties
Let vector3 = TensorAlgebra.create_tensor(vector_space_3d, ["7.0", "8.0", "9.0"])
Let scalar_k = 2.5

Note: Linearity in first argument
Let linear_test1 = TensorAlgebra.inner_product(
    TensorAlgebra.tensor_addition(vector1, vector3), 
    vector2, 
    metric_tensor
)
Let expected_linear1 = TensorAlgebra.inner_product(vector1, vector2, metric_tensor) + 
                      TensorAlgebra.inner_product(vector3, vector2, metric_tensor)
Display "First argument linearity: " + String(abs(linear_test1 - expected_linear1) < 1e-12)

Note: Symmetry property
Let symmetry_test1 = TensorAlgebra.inner_product(vector1, vector2, metric_tensor)
Let symmetry_test2 = TensorAlgebra.inner_product(vector2, vector1, metric_tensor)
Display "Symmetry property: " + String(abs(symmetry_test1 - symmetry_test2) < 1e-12)
```

## Symmetry Operations

### Symmetrization and Antisymmetrization

```runa
Note: Symmetrize and antisymmetrize tensor indices
Let antisymmetric_space = TensorAlgebra.create_tensor_space(Dictionary with:
    "base_dimension": "3"
    "contravariant_degree": "0"
    "covariant_degree": "2"
    "scalar_field": "real"
)

Let general_tensor = TensorAlgebra.create_tensor(antisymmetric_space, [
    "1.0", "2.0", "3.0",
    "4.0", "5.0", "6.0",
    "7.0", "8.0", "9.0"
])

Note: Symmetrization: T_(ij) = ½(T_ij + T_ji)
Let symmetrized = TensorAlgebra.symmetrize_tensor(general_tensor, [0, 1])
Display "Symmetrized tensor components:"
For i from 0 to 8:
    Display "  Component " + String(i) + ": " + String(symmetrized.components[i])

Note: Antisymmetrization: T_[ij] = ½(T_ij - T_ji)  
Let antisymmetrized = TensorAlgebra.antisymmetrize_tensor(general_tensor, [0, 1])
Display "Antisymmetrized tensor components:"
For i from 0 to 8:
    Display "  Component " + String(i) + ": " + String(antisymmetrized.components[i])

Note: Verify decomposition: T = T_(ij) + T_[ij]
Let reconstructed = TensorAlgebra.tensor_addition(symmetrized, antisymmetrized)
Let decomposition_check = TensorAlgebra.tensors_equal(general_tensor, reconstructed, "1e-12")
Display "Symmetric + Antisymmetric decomposition verified: " + String(decomposition_check)

Note: Check properties of symmetrized tensor
Let symmetry_test = TensorAlgebra.check_symmetry(symmetrized, [0, 1])
Display "Symmetrized tensor is symmetric: " + String(symmetry_test.is_symmetric)

Let antisymmetry_test = TensorAlgebra.check_symmetry(antisymmetrized, [0, 1])
Display "Antisymmetrized tensor is antisymmetric: " + String(antisymmetry_test.is_antisymmetric)
```

### Permutation Groups and Young Tableaux

```runa
Note: Work with permutation symmetries
Let rank_3_space = TensorAlgebra.create_tensor_space(Dictionary with:
    "base_dimension": "3"
    "contravariant_degree": "0"
    "covariant_degree": "3"
    "scalar_field": "real"
)

Let rank_3_tensor = TensorAlgebra.create_random_tensor(rank_3_space)

Note: Apply permutation to indices
Let permutation_123 = [0, 1, 2]  # Identity permutation
Let permutation_132 = [0, 2, 1]  # Swap last two indices
Let permutation_213 = [1, 0, 2]  # Swap first two indices

Let permuted_132 = TensorAlgebra.permute_tensor_indices(rank_3_tensor, permutation_132)
Let permuted_213 = TensorAlgebra.permute_tensor_indices(rank_3_tensor, permutation_213)

Note: Total symmetrization over all indices
Let totally_symmetric = TensorAlgebra.total_symmetrization(rank_3_tensor)
Display "Totally symmetric tensor created"

Note: Total antisymmetrization over all indices  
Let totally_antisymmetric = TensorAlgebra.total_antisymmetrization(rank_3_tensor)
Display "Totally antisymmetric tensor created"

Note: Young tableau symmetrization
Let young_tableau = [[0, 1], [2]]  # Mixed symmetry: symmetric in (0,1), independent in 2
Let young_symmetrized = TensorAlgebra.young_tableau_symmetrize(rank_3_tensor, young_tableau)
Display "Young tableau symmetrization applied"

Note: Verify Young symmetrizer properties
Let young_properties = TensorAlgebra.analyze_young_symmetry(young_symmetrized, young_tableau)
Display "Young symmetry analysis:"
Display "  Symmetric pairs: " + String(young_properties.symmetric_pairs)
Display "  Independent indices: " + String(young_properties.independent_indices)
```

## Advanced Tensor Operations

### Exterior Algebra and Wedge Products

```runa
Note: Work with exterior algebra (antisymmetric tensors)
Let exterior_space = TensorAlgebra.create_exterior_space(3, 2)  # 2-forms on 3D space

Let oneform_α = TensorAlgebra.create_tensor(covector_space_3d, ["1.0", "2.0", "3.0"])
Let oneform_β = TensorAlgebra.create_tensor(covector_space_3d, ["4.0", "5.0", "6.0"])

Note: Compute wedge product α ∧ β
Let wedge_product = TensorAlgebra.wedge_product(oneform_α, oneform_β)
Display "Wedge product computed"
Display "Wedge product rank: " + String(wedge_product.tensor_space.covariant_degree)

Note: Verify wedge product properties
Let oneform_γ = TensorAlgebra.create_tensor(covector_space_3d, ["7.0", "8.0", "9.0"])

Note: Anticommutativity: α ∧ β = -β ∧ α
Let wedge_αβ = TensorAlgebra.wedge_product(oneform_α, oneform_β)
Let wedge_βα = TensorAlgebra.wedge_product(oneform_β, oneform_α)
Let anticommutative_test = TensorAlgebra.tensor_addition(wedge_αβ, wedge_βα)
Let is_zero = TensorAlgebra.is_zero_tensor(anticommutative_test, "1e-12")
Display "Anticommutativity verified: " + String(is_zero)

Note: Associativity: (α ∧ β) ∧ γ = α ∧ (β ∧ γ)
Let associative_left = TensorAlgebra.wedge_product(wedge_αβ, oneform_γ)
Let wedge_βγ = TensorAlgebra.wedge_product(oneform_β, oneform_γ)  
Let associative_right = TensorAlgebra.wedge_product(oneform_α, wedge_βγ)
Let associativity_verified = TensorAlgebra.tensors_equal(associative_left, associative_right, "1e-12")
Display "Associativity verified: " + String(associativity_verified)

Note: Linearity in both arguments
Let scalar_c = 3.0
Let linear_wedge = TensorAlgebra.wedge_product(
    TensorAlgebra.scalar_multiplication(scalar_c, oneform_α),
    oneform_β
)
Let expected_linear = TensorAlgebra.scalar_multiplication(scalar_c, wedge_product)
Let linearity_verified = TensorAlgebra.tensors_equal(linear_wedge, expected_linear, "1e-12")
Display "Linearity verified: " + String(linearity_verified)
```

### Hodge Duality

```runa
Note: Hodge star operation in 3D Euclidean space
Let hodge_metric = TensorAlgebra.create_metric_tensor(3, Dictionary with:
    "signature": "euclidean"
    "orientation": "positive"
})

Note: Hodge dual of a 1-form (gives 2-form in 3D)
Let hodge_dual_α = TensorAlgebra.hodge_star(oneform_α, hodge_metric)
Display "Hodge dual computed: 1-form → 2-form"

Note: Hodge dual of a 2-form (gives 1-form in 3D)
Let hodge_dual_wedge = TensorAlgebra.hodge_star(wedge_product, hodge_metric)
Display "Hodge dual computed: 2-form → 1-form"

Note: Double Hodge dual should give back original (up to sign in 3D)
Let double_hodge = TensorAlgebra.hodge_star(hodge_dual_wedge, hodge_metric)
Let double_hodge_comparison = TensorAlgebra.tensors_equal(
    double_hodge, 
    TensorAlgebra.scalar_multiplication(-1.0, wedge_product),  # -1 in 3D
    "1e-12"
)
Display "Double Hodge dual property verified: " + String(double_hodge_comparison)

Note: Volume form from Hodge dual of scalar
Let volume_form = TensorAlgebra.hodge_star_of_scalar(1.0, hodge_metric)
Display "Volume form created via Hodge dual"
Display "Volume form components: " + String(volume_form.components.length)
```

### Tensor Decompositions

```runa
Note: Decompose tensors into irreducible representations
Let general_rank2 = TensorAlgebra.create_tensor(tensor_space, [
    "1.0", "2.0", "3.0",
    "4.0", "5.0", "6.0",
    "7.0", "8.0", "9.0"
])

Note: Decompose into trace, traceless symmetric, and antisymmetric parts
Let irreducible_decomposition = TensorAlgebra.irreducible_decomposition(general_rank2, metric_tensor)

Let trace_part = irreducible_decomposition.trace_part
Let traceless_symmetric = irreducible_decomposition.traceless_symmetric_part  
Let antisymmetric_part = irreducible_decomposition.antisymmetric_part

Display "Irreducible decomposition completed:"
Display "  Trace part (scalar): " + String(trace_part.components[0])
Display "  Traceless symmetric part dimension: " + String(traceless_symmetric.components.length)
Display "  Antisymmetric part dimension: " + String(antisymmetric_part.components.length)

Note: Verify reconstruction
Let reconstructed_tensor = TensorAlgebra.tensor_addition(
    TensorAlgebra.tensor_addition(trace_part, traceless_symmetric),
    antisymmetric_part
)
Let reconstruction_verified = TensorAlgebra.tensors_equal(general_rank2, reconstructed_tensor, "1e-12")
Display "Reconstruction verified: " + String(reconstruction_verified)

Note: Check that parts are orthogonal under appropriate inner product
Let symmetric_antisymmetric_product = TensorAlgebra.tensor_inner_product(
    traceless_symmetric, 
    antisymmetric_part, 
    metric_tensor
)
Display "Symmetric-antisymmetric orthogonality: " + String(abs(symmetric_antisymmetric_product) < 1e-12)
```

## Index Raising and Lowering

### Metric Operations

```runa
Note: Raise and lower tensor indices using metric
Let contravariant_vector = TensorAlgebra.create_tensor(vector_space_3d, ["1.0", "2.0", "3.0"])

Note: Lower index using metric: v^i → v_i = g_ij v^j
Let covariant_vector = TensorAlgebra.lower_index(contravariant_vector, metric_tensor, 0)
Display "Index lowered: contravariant → covariant"

Note: Raise index using inverse metric: v_i → v^i = g^ij v_j
Let metric_inverse = TensorAlgebra.metric_inverse(metric_tensor)
Let raised_back = TensorAlgebra.raise_index(covariant_vector, metric_inverse, 0)

Note: Should recover original vector
Let roundtrip_verified = TensorAlgebra.tensors_equal(contravariant_vector, raised_back, "1e-12")
Display "Index raising/lowering roundtrip verified: " + String(roundtrip_verified)

Note: Work with non-trivial metrics
Let minkowski_metric = TensorAlgebra.create_metric_tensor(4, Dictionary with:
    "signature": "lorentzian"  # (-1, +1, +1, +1) or (+1, -1, -1, -1)
    "components": [
        "-1.0", "0.0", "0.0", "0.0",
        "0.0", "1.0", "0.0", "0.0",
        "0.0", "0.0", "1.0", "0.0", 
        "0.0", "0.0", "0.0", "1.0"
    ]
})

Let spacetime_vector_space = TensorAlgebra.create_tensor_space(Dictionary with:
    "base_dimension": "4"
    "contravariant_degree": "1"
    "covariant_degree": "0"
    "scalar_field": "real"
)

Let four_vector = TensorAlgebra.create_tensor(spacetime_vector_space, ["1.0", "2.0", "3.0", "4.0"])
Let four_covector = TensorAlgebra.lower_index(four_vector, minkowski_metric, 0)

Display "Minkowski metric operations:"
Display "  Four-vector components: " + String(four_vector.components)
Display "  Four-covector components: " + String(four_covector.components)

Note: Compute spacetime interval
Let spacetime_interval = TensorAlgebra.inner_product(four_vector, four_covector, minkowski_metric)
Display "  Spacetime interval: " + String(spacetime_interval)
```

## Tensor Calculus Integration

### Coordinate Transformations

```runa
Note: Transform tensors under coordinate changes
Let transformation_matrix = [
    [1.0, 0.5, 0.0],
    [0.0, 2.0, 1.0],
    [0.0, 0.0, 1.5]
]

Let inverse_transformation = TensorAlgebra.matrix_inverse(transformation_matrix)

Note: Transform contravariant tensor: T'^i = ∂x'^i/∂x^j T^j
Let transformed_contravariant = TensorAlgebra.transform_contravariant_tensor(
    contravariant_vector,
    transformation_matrix
)

Note: Transform covariant tensor: T'_i = ∂x^j/∂x'^i T_j  
Let transformed_covariant = TensorAlgebra.transform_covariant_tensor(
    covariant_vector,
    inverse_transformation
)

Display "Coordinate transformation applied"
Display "Original contravariant: " + String(contravariant_vector.components)
Display "Transformed contravariant: " + String(transformed_contravariant.components)

Note: Transform mixed tensor
Let mixed_tensor_space = TensorAlgebra.create_tensor_space(Dictionary with:
    "base_dimension": "3"
    "contravariant_degree": "1"
    "covariant_degree": "1"
    "scalar_field": "real"
)

Let mixed_tensor = TensorAlgebra.create_tensor(mixed_tensor_space, [
    "1.0", "0.5", "0.0",
    "0.5", "2.0", "1.0",
    "0.0", "1.0", "3.0"
])

Let transformed_mixed = TensorAlgebra.transform_mixed_tensor(
    mixed_tensor,
    transformation_matrix,
    inverse_transformation
)

Display "Mixed tensor transformation completed"
Display "Transformation preserves tensor character: " + String(
    TensorAlgebra.verify_tensor_transformation(mixed_tensor, transformed_mixed, transformation_matrix)
)
```

## Performance Optimization

### Efficient Tensor Operations

```runa
Note: Configure performance settings for large tensors
Let performance_config = Dictionary with:
    "use_parallel_operations": "true"
    "thread_count": "8"
    "memory_optimization": "aggressive"
    "cache_intermediate_results": "true"
    "vectorize_operations": "true"

TensorAlgebra.configure_performance(performance_config)

Note: Benchmark tensor operations
Let large_tensor_space = TensorAlgebra.create_tensor_space(Dictionary with:
    "base_dimension": "100"
    "contravariant_degree": "2"
    "covariant_degree": "2"
    "scalar_field": "real"
)

Let large_tensor_a = TensorAlgebra.create_random_tensor(large_tensor_space)
Let large_tensor_b = TensorAlgebra.create_random_tensor(large_tensor_space)

Let benchmark_start = TensorAlgebra.get_time_microseconds()
Let large_sum = TensorAlgebra.tensor_addition(large_tensor_a, large_tensor_b)
Let benchmark_end = TensorAlgebra.get_time_microseconds()

Display "Large tensor addition benchmark:"
Display "  Tensor dimensions: " + String(large_tensor_space.total_dimension)
Display "  Computation time: " + String(benchmark_end - benchmark_start) + " μs"

Note: Memory usage optimization
Let memory_usage_before = TensorAlgebra.get_memory_usage()
Let large_contraction = TensorAlgebra.tensor_contraction(large_tensor_a, [0, 2])
Let memory_usage_after = TensorAlgebra.get_memory_usage()

Display "Memory usage optimization:"
Display "  Memory before: " + String(memory_usage_before) + " bytes"  
Display "  Memory after: " + String(memory_usage_after) + " bytes"
Display "  Memory efficiency: " + String(memory_usage_before > memory_usage_after)
```

## Error Handling

### Tensor Operation Validation

```runa
Try:
    Note: Attempt invalid tensor addition (incompatible spaces)
    Let incompatible_space = TensorAlgebra.create_tensor_space(Dictionary with:
        "base_dimension": "4"  # Different dimension
        "contravariant_degree": "1"
        "covariant_degree": "1"
        "scalar_field": "real"
    )
    
    Let incompatible_tensor = TensorAlgebra.create_random_tensor(incompatible_space)
    Let invalid_addition = TensorAlgebra.tensor_addition(tensor_a, incompatible_tensor)
    
Catch Errors.InvalidArgument as dim_error:
    Display "Tensor dimension error: " + dim_error.message
    Display "Expected dimension: " + String(tensor_a.tensor_space.base_vector_space_dimension)
    Display "Received dimension: " + String(incompatible_tensor.tensor_space.base_vector_space_dimension)

Try:
    Note: Attempt invalid contraction (indices out of range)
    Let invalid_contraction = TensorAlgebra.tensor_contraction(tensor_a, [5, 7])  # Invalid indices
    
Catch Errors.IndexError as index_error:
    Display "Index error: " + index_error.message
    Display "Available indices: 0 to " + String(tensor_a.tensor_space.contravariant_degree + tensor_a.tensor_space.covariant_degree - 1)

Try:
    Note: Attempt operation with singular metric
    Let singular_metric = TensorAlgebra.create_metric_tensor(3, Dictionary with:
        "components": [
            "1.0", "0.0", "0.0",
            "0.0", "1.0", "0.0",
            "0.0", "0.0", "0.0"  # Singular metric
        ]
    )
    
    Let singular_inverse = TensorAlgebra.metric_inverse(singular_metric)
    
Catch Errors.SingularMatrixError as singular_error:
    Display "Singular metric error: " + singular_error.message
    Display "Metric determinant: " + String(singular_error.determinant)
    Display "Cannot invert singular metric tensor"
```

## Integration Examples

### Physics Applications

```runa
Note: Electromagnetic field tensor in relativity
Let electromagnetic_tensor_space = TensorAlgebra.create_tensor_space(Dictionary with:
    "base_dimension": "4"
    "contravariant_degree": "0"
    "covariant_degree": "2"
    "scalar_field": "real"
)

Note: F_μν = ∂A_ν/∂x^μ - ∂A_μ/∂x^ν (antisymmetric)
Let field_tensor_components = [
    "0.0", "-Ex", "-Ey", "-Ez",
    "Ex", "0.0", "Bz", "-By", 
    "Ey", "-Bz", "0.0", "Bx",
    "Ez", "By", "-Bx", "0.0"
]

Let electromagnetic_tensor = TensorAlgebra.create_tensor(electromagnetic_tensor_space, field_tensor_components)

Note: Verify antisymmetry
Let antisymmetry_check = TensorAlgebra.check_symmetry(electromagnetic_tensor, [0, 1])
Display "Electromagnetic tensor is antisymmetric: " + String(antisymmetry_check.is_antisymmetric)

Note: Compute electromagnetic stress-energy tensor
Let stress_energy = TensorAlgebra.electromagnetic_stress_energy_tensor(electromagnetic_tensor, minkowski_metric)
Display "Electromagnetic stress-energy tensor computed"

Note: Verify stress-energy tensor properties
Let trace_free_check = TensorAlgebra.tensor_trace(stress_energy, minkowski_metric)
Display "Stress-energy tensor trace: " + String(abs(trace_free_check) < 1e-12)
```

### Differential Geometry Applications

```runa
Note: Curvature tensor construction
Let curvature_space = TensorAlgebra.create_tensor_space(Dictionary with:
    "base_dimension": "4"
    "contravariant_degree": "1"
    "covariant_degree": "3"
    "scalar_field": "real"
)

Note: Create sample curvature tensor with proper symmetries
Let riemann_tensor = TensorAlgebra.create_riemann_tensor(minkowski_metric)

Note: Check Riemann tensor symmetries
Let symmetry_analysis = TensorAlgebra.analyze_riemann_symmetries(riemann_tensor)
Display "Riemann tensor symmetry analysis:"
Display "  R^i_jkl = -R^i_jlk: " + String(symmetry_analysis.antisymmetric_last_two)
Display "  R^i_jkl + R^i_klj + R^i_ljk = 0: " + String(symmetry_analysis.first_bianchi_identity)

Note: Contract to get Ricci tensor
Let ricci_tensor = TensorAlgebra.ricci_contraction(riemann_tensor)
Display "Ricci tensor computed via contraction"

Note: Compute Ricci scalar
Let ricci_scalar = TensorAlgebra.tensor_trace(ricci_tensor, TensorAlgebra.metric_inverse(minkowski_metric))
Display "Ricci scalar: " + String(ricci_scalar)
```

## Related Documentation

- **[Tensor Calculus](calculus.md)**: Covariant derivatives and differential operations
- **[Tensor Geometry](geometry.md)**: Applications to spacetime and general relativity
- **[Linear Algebra Engine](../engine/linalg/README.md)**: Matrix operations and decompositions  
- **[Symbolic Core](../symbolic/core.md)**: Symbolic tensor expressions
- **[Mathematical Analysis](../analysis/README.md)**: Analytical tensor operations

The Tensor Algebra module provides the foundational algebraic structure for all tensor operations in Runa. Its comprehensive implementation of multilinear algebra, symmetry operations, and tensor manipulations makes it essential for advanced mathematics, theoretical physics, and geometric applications.