# Linear Algebra Module

The `math/algebra/linear` module provides comprehensive linear algebraic structures and operations including vector spaces, linear transformations, eigenvalue computations, and advanced matrix decompositions. This module focuses on the algebraic aspects of linear algebra, complementing the numerical linear algebra engine.

## Quick Start

```runa
Import "math/algebra/linear" as Linear

Note: Create vector space and linear transformation
Let vector_space be Linear.create_vector_space(dimension: 3, field: "real")
Let transformation_matrix be [
    [2, -1, 0],
    [1, 1, -1],
    [0, 1, 2]
]

Let linear_map be Linear.create_linear_transformation(transformation_matrix)
Let eigenvalues be Linear.compute_eigenvalues(linear_map)
Let eigenvectors be Linear.compute_eigenvectors(linear_map)

Display "Eigenvalues: " joined with eigenvalues
Display "Number of eigenvectors: " joined with eigenvectors.length()
```

## Core Concepts

### Vector Spaces
A vector space is a collection of objects (vectors) with operations of addition and scalar multiplication that satisfy specific axioms.

### Linear Transformations
Mappings between vector spaces that preserve vector space operations (linearity).

### Eigenvalue Theory
Study of special vectors (eigenvectors) that are only scaled by linear transformations, with corresponding scaling factors (eigenvalues).

### Matrix Normal Forms
Canonical representations of matrices that reveal structural properties.

## API Reference

### Vector Space Construction

#### Basic Vector Spaces
```runa
Type called "VectorSpace":
    dimension as Integer
    field as Field
    basis as List[Vector]
    inner_product as Process
    is_finite_dimensional as Boolean

Process called "create_vector_space" that takes:
    dimension as Integer,
    field as String
returns VectorSpace:
    Note: Create finite-dimensional vector space over field

Process called "create_function_space" that takes:
    domain as Set[Any],
    codomain as Field,
    constraints as List[String]
returns VectorSpace:
    Note: Create infinite-dimensional function space
```

#### Vector Operations
```runa
Type called "Vector":
    components as List[Any]
    dimension as Integer
    field as Field

Process called "vector_addition" that takes:
    v1 as Vector,
    v2 as Vector
returns Vector:
    Note: Add two vectors component-wise

Process called "scalar_multiplication" that takes:
    scalar as Any,
    vector as Vector
returns Vector:
    Note: Multiply vector by scalar

Process called "dot_product" that takes:
    v1 as Vector,
    v2 as Vector
returns Any:
    Note: Compute inner product of vectors
```

### Linear Transformations

#### Transformation Construction
```runa
Type called "LinearTransformation":
    domain as VectorSpace
    codomain as VectorSpace
    matrix_representation as Matrix
    kernel as VectorSpace
    image as VectorSpace
    rank as Integer
    nullity as Integer

Process called "create_linear_transformation" that takes:
    matrix as Matrix,
    domain as VectorSpace,
    codomain as VectorSpace
returns LinearTransformation:
    Note: Create linear transformation from matrix representation

Process called "create_transformation_from_function" that takes:
    function as Process,
    domain as VectorSpace,
    codomain as VectorSpace
returns LinearTransformation:
    Note: Create linear transformation from function definition
```

#### Transformation Properties
```runa
Process called "compute_kernel" that takes transformation as LinearTransformation returns VectorSpace:
    Note: Compute null space (kernel) of linear transformation

Process called "compute_image" that takes transformation as LinearTransformation returns VectorSpace:
    Note: Compute range (image) of linear transformation

Process called "compute_rank" that takes transformation as LinearTransformation returns Integer:
    Note: Compute rank (dimension of image)

Process called "compute_nullity" that takes transformation as LinearTransformation returns Integer:
    Note: Compute nullity (dimension of kernel)
```

### Matrix Theory

#### Matrix Construction
```runa
Type called "Matrix":
    entries as List[List[Any]]
    rows as Integer
    columns as Integer
    field as Field
    is_square as Boolean

Process called "create_matrix" that takes:
    entries as List[List[Any]],
    field as Field
returns Matrix:
    Note: Create matrix with specified entries over field

Process called "create_identity_matrix" that takes:
    size as Integer,
    field as Field
returns Matrix:
    Note: Create identity matrix

Process called "create_zero_matrix" that takes:
    rows as Integer,
    columns as Integer,
    field as Field
returns Matrix:
    Note: Create zero matrix
```

#### Matrix Operations
```runa
Process called "matrix_addition" that takes:
    A as Matrix,
    B as Matrix
returns Matrix:
    Note: Add two matrices

Process called "matrix_multiplication" that takes:
    A as Matrix,
    B as Matrix
returns Matrix:
    Note: Multiply two matrices

Process called "matrix_transpose" that takes matrix as Matrix returns Matrix:
    Note: Compute transpose of matrix

Process called "matrix_inverse" that takes matrix as Matrix returns Matrix:
    Note: Compute inverse of matrix (if it exists)
```

### Eigenvalue Theory

#### Eigenvalue Computation
```runa
Type called "Eigenvalue":
    value as Any
    multiplicity as Integer
    geometric_multiplicity as Integer
    eigenvectors as List[Vector]

Process called "compute_eigenvalues" that takes matrix as Matrix returns List[Eigenvalue]:
    Note: Compute all eigenvalues with multiplicities

Process called "compute_eigenvectors" that takes:
    matrix as Matrix,
    eigenvalue as Any
returns List[Vector]:
    Note: Compute eigenvectors for given eigenvalue

Process called "compute_characteristic_polynomial" that takes matrix as Matrix returns Polynomial:
    Note: Compute characteristic polynomial det(A - λI)

Process called "compute_minimal_polynomial" that takes matrix as Matrix returns Polynomial:
    Note: Compute minimal polynomial of matrix
```

#### Spectral Analysis
```runa
Process called "is_diagonalizable" that takes matrix as Matrix returns Boolean:
    Note: Check if matrix is diagonalizable

Process called "diagonalize" that takes matrix as Matrix returns Dictionary[String, Matrix]:
    Note: Diagonalize matrix: returns P, D such that A = PDP^(-1)

Process called "compute_jordan_normal_form" that takes matrix as Matrix returns Dictionary[String, Matrix]:
    Note: Compute Jordan canonical form

Process called "compute_spectral_radius" that takes matrix as Matrix returns Real:
    Note: Compute largest absolute value of eigenvalues
```

### Matrix Decompositions

#### Standard Decompositions
```runa
Process called "lu_decomposition" that takes matrix as Matrix returns Dictionary[String, Matrix]:
    Note: Compute LU decomposition with partial pivoting

Process called "qr_decomposition" that takes matrix as Matrix returns Dictionary[String, Matrix]:
    Note: Compute QR decomposition using Gram-Schmidt

Process called "singular_value_decomposition" that takes matrix as Matrix returns Dictionary[String, Matrix]:
    Note: Compute SVD: A = UΣV*

Process called "polar_decomposition" that takes matrix as Matrix returns Dictionary[String, Matrix]:
    Note: Decompose A = UP where U is unitary, P is positive
```

#### Specialized Decompositions
```runa
Process called "cholesky_decomposition" that takes matrix as Matrix returns Matrix:
    Note: Compute Cholesky decomposition for positive definite matrices

Process called "schur_decomposition" that takes matrix as Matrix returns Dictionary[String, Matrix]:
    Note: Compute Schur form: A = QTQ* where T is upper triangular

Process called "hessenberg_reduction" that takes matrix as Matrix returns Dictionary[String, Matrix]:
    Note: Reduce matrix to Hessenberg form
```

### Inner Product Spaces

#### Inner Product Operations
```runa
Type called "InnerProductSpace":
    vector_space as VectorSpace
    inner_product as Process that takes Vector, Vector returns Any
    norm as Process that takes Vector returns Real
    is_complete as Boolean

Process called "create_euclidean_space" that takes dimension as Integer returns InnerProductSpace:
    Note: Create Euclidean space with standard inner product

Process called "gram_schmidt_orthogonalization" that takes:
    vectors as List[Vector],
    inner_product_space as InnerProductSpace
returns List[Vector]:
    Note: Orthogonalize vectors using Gram-Schmidt process

Process called "compute_orthogonal_complement" that takes:
    subspace as VectorSpace,
    ambient_space as InnerProductSpace
returns VectorSpace:
    Note: Compute orthogonal complement of subspace
```

## Practical Examples

### Linear System Analysis
```runa
Import "math/algebra/linear" as Linear

Note: Analyze homogeneous linear system
Let coefficient_matrix be Linear.create_matrix([
    [1, 2, -1, 0],
    [2, 4, 0, 1],
    [1, 2, 1, 2]
])

Let system_transformation be Linear.create_linear_transformation(coefficient_matrix)
Let solution_space be Linear.compute_kernel(system_transformation)
Let particular_solution be Linear.find_particular_solution(coefficient_matrix, [1, 2, 3])

Display "Solution space dimension: " joined with solution_space.dimension
Display "Particular solution exists: " joined with (particular_solution != null)

Note: Find basis for solution space
Let basis_vectors be Linear.find_basis(solution_space)
Display "Basis for solution space:"
For Each vector in basis_vectors:
    Display "  " joined with Linear.vector_to_string(vector)
```

### Eigenvalue Applications
```runa
Note: Analyze dynamical system
Let transition_matrix be Linear.create_matrix([
    [0.7, 0.2, 0.1],
    [0.1, 0.8, 0.1],
    [0.3, 0.1, 0.6]
])

Let eigenvalues be Linear.compute_eigenvalues(transition_matrix)
Let dominant_eigenvalue be Linear.find_dominant_eigenvalue(eigenvalues)
Let steady_state be Linear.compute_eigenvectors(transition_matrix, dominant_eigenvalue)[0]

Display "Dominant eigenvalue: " joined with dominant_eigenvalue.value
Display "Steady state vector: " joined with Linear.vector_to_string(steady_state)

Note: Check convergence properties
Let spectral_radius be Linear.compute_spectral_radius(transition_matrix)
Let converges be spectral_radius < 1.0
Display "System converges: " joined with converges
```

### Principal Component Analysis
```runa
Note: Perform dimensionality reduction using PCA
Let data_matrix be Linear.create_matrix([
    [2.5, 2.4],
    [0.5, 0.7],
    [2.2, 2.9],
    [1.9, 2.2],
    [3.1, 3.0],
    [2.3, 2.7],
    [2.0, 1.6],
    [1.0, 1.1],
    [1.5, 1.6],
    [1.1, 0.9]
])

Note: Compute covariance matrix
Let centered_data be Linear.center_data(data_matrix)
Let covariance_matrix be Linear.compute_covariance_matrix(centered_data)

Note: Find principal components
Let eigenvalue_decomposition be Linear.diagonalize(covariance_matrix)
Let principal_components be eigenvalue_decomposition["eigenvectors"]
Let explained_variance be eigenvalue_decomposition["eigenvalues"]

Display "Principal components computed"
Display "First PC explains " joined with (explained_variance[0] / Linear.sum(explained_variance) * 100) joined with "% of variance"
```

### Matrix Canonical Forms
```runa
Note: Compute Jordan normal form
Let matrix be Linear.create_matrix([
    [5, -6, -6],
    [-1, 4, 2],
    [3, -6, -4]
])

Let jordan_form be Linear.compute_jordan_normal_form(matrix)
Let jordan_matrix be jordan_form["jordan"]
Let transformation_matrix be jordan_form["transformation"]

Display "Jordan canonical form:"
Linear.display_matrix(jordan_matrix)

Note: Verify decomposition
Let reconstructed be Linear.matrix_multiplication(
    Linear.matrix_multiplication(transformation_matrix, jordan_matrix),
    Linear.matrix_inverse(transformation_matrix)
)

Let error be Linear.matrix_norm(Linear.matrix_subtraction(matrix, reconstructed))
Display "Reconstruction error: " joined with error
```

### Orthogonal Projections
```runa
Note: Project vector onto subspace
Let subspace_basis be [
    Linear.create_vector([1, 1, 0]),
    Linear.create_vector([0, 1, 1])
]

Let target_vector be Linear.create_vector([2, 3, 1])
Let euclidean_space be Linear.create_euclidean_space(3)

Note: Orthogonalize basis
Let orthogonal_basis be Linear.gram_schmidt_orthogonalization(
    subspace_basis,
    euclidean_space
)

Note: Compute projection
Let projection be Linear.orthogonal_projection(
    target_vector,
    orthogonal_basis,
    euclidean_space
)

Let projection_error be Linear.vector_norm(
    Linear.vector_subtraction(target_vector, projection)
)

Display "Projection: " joined with Linear.vector_to_string(projection)
Display "Projection error: " joined with projection_error
```

## Advanced Features

### Multilinear Algebra
```runa
Type called "TensorSpace":
    base_space as VectorSpace
    rank as Integer
    dimension as Integer

Process called "tensor_product" that takes:
    v1 as Vector,
    v2 as Vector
returns Tensor:
    Note: Compute tensor product of vectors

Process called "exterior_product" that takes:
    v1 as Vector,
    v2 as Vector
returns ExteriorForm:
    Note: Compute exterior (wedge) product

Process called "compute_determinant_via_exterior" that takes matrix as Matrix returns Any:
    Note: Compute determinant using exterior algebra
```

### Matrix Groups
```runa
Process called "create_general_linear_group" that takes:
    dimension as Integer,
    field as Field
returns Group:
    Note: Create GL(n, F) - group of invertible matrices

Process called "create_special_linear_group" that takes:
    dimension as Integer,
    field as Field
returns Group:
    Note: Create SL(n, F) - matrices with determinant 1

Process called "create_orthogonal_group" that takes:
    dimension as Integer,
    field as Field
returns Group:
    Note: Create O(n, F) - orthogonal matrices
```

### Representation Theory
```runa
Process called "create_matrix_representation" that takes:
    group as Group,
    vector_space as VectorSpace
returns Dictionary[Any, Matrix]:
    Note: Create matrix representation of group

Process called "is_irreducible_representation" that takes representation as Dictionary[Any, Matrix] returns Boolean:
    Note: Check if representation is irreducible

Process called "compute_character" that takes representation as Dictionary[Any, Matrix] returns Dictionary[Any, Any]:
    Note: Compute character of representation
```

## Integration with Other Modules

### With Abstract Algebra
```runa
Import "math/algebra/abstract" as Abstract
Import "math/algebra/linear" as Linear

Note: Study linear transformations as ring elements
Let vector_space be Linear.create_vector_space(dimension: 3, field: "real")
Let endomorphism_ring be Abstract.create_endomorphism_ring(vector_space)

Let T1 be Linear.create_linear_transformation([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1]
])

Let T2 be Linear.create_linear_transformation([
    [0, 1, 0],
    [0, 0, 1],
    [1, 0, 0]
])

Let composition be Abstract.ring_multiplication(endomorphism_ring, T1, T2)
Let commutator be Abstract.ring_subtraction(
    endomorphism_ring,
    composition,
    Abstract.ring_multiplication(endomorphism_ring, T2, T1)
)

Display "Transformations commute: " joined with Linear.is_zero_transformation(commutator)
```

### With Numerical Methods
```runa
Import "math/engine/numerical/core" as Numerical
Import "math/algebra/linear" as Linear

Note: Compare exact and approximate eigenvalue computation
Let matrix be Linear.create_matrix([
    [4, -2, 1],
    [1, 1, -1],
    [0, 2, 3]
])

Note: Exact computation over rationals
Let exact_eigenvalues be Linear.compute_eigenvalues_exact(matrix)

Note: Numerical approximation
Let numerical_matrix be Numerical.matrix_from_rational(matrix)
Let approx_eigenvalues be Numerical.compute_eigenvalues_iterative(numerical_matrix)

Display "Exact eigenvalues: " joined with exact_eigenvalues
Display "Approximate eigenvalues: " joined with approx_eigenvalues
```

### With Polynomial Algebra
```runa
Import "math/algebra/polynomial" as Poly
Import "math/algebra/linear" as Linear

Note: Study matrix polynomials
Let matrix be Linear.create_matrix([
    [1, 2],
    [0, 3]
])

Let polynomial_ring be Poly.create_polynomial_ring(["t"], "real")
Let char_poly be Linear.compute_characteristic_polynomial(matrix)
Let min_poly be Linear.compute_minimal_polynomial(matrix)

Display "Characteristic polynomial: " joined with Poly.to_string(char_poly)
Display "Minimal polynomial: " joined with Poly.to_string(min_poly)
Display "Matrix satisfies minimal polynomial: " joined with Linear.verify_polynomial_relation(matrix, min_poly)
```

## Computational Geometry Applications

### Geometric Transformations
```runa
Note: 3D rotation transformations
Let rotation_x be Linear.create_rotation_matrix("x", angle: 1.57)  Note: π/2 radians
Let rotation_y be Linear.create_rotation_matrix("y", angle: 1.57)
Let rotation_z be Linear.create_rotation_matrix("z", angle: 1.57)

Let combined_rotation be Linear.matrix_multiplication(
    rotation_z,
    Linear.matrix_multiplication(rotation_y, rotation_x)
)

Let test_vector be Linear.create_vector([1, 0, 0])
Let rotated_vector be Linear.apply_transformation(combined_rotation, test_vector)

Display "Original vector: " joined with Linear.vector_to_string(test_vector)
Display "Rotated vector: " joined with Linear.vector_to_string(rotated_vector)
```

### Affine Transformations
```runa
Note: Create affine transformation (rotation + translation)
Let rotation_matrix be Linear.create_rotation_matrix("z", angle: 0.785)  Note: 45 degrees
Let translation_vector be Linear.create_vector([2, 3])

Let affine_transform be Linear.create_affine_transformation(
    linear_part: rotation_matrix,
    translation: translation_vector
)

Let points be [
    Linear.create_vector([0, 0]),
    Linear.create_vector([1, 0]),
    Linear.create_vector([1, 1]),
    Linear.create_vector([0, 1])
]

Let transformed_points be []
For Each point in points:
    Let transformed be Linear.apply_affine_transformation(affine_transform, point)
    transformed_points.append(transformed)

Display "Transformed square vertices:"
For Each point in transformed_points:
    Display "  " joined with Linear.vector_to_string(point)
```

## Best Practices

### Numerical Stability
```runa
Note: Check condition number before inversion
Process called "safe_matrix_inverse" that takes matrix as Matrix returns Matrix:
    Let condition_number be Linear.compute_condition_number(matrix)
    If condition_number > 1e12:
        Display "Warning: Matrix is ill-conditioned"
        Return Linear.pseudoinverse(matrix)
    Otherwise:
        Return Linear.matrix_inverse(matrix)
```

### Basis Selection
```runa
Note: Choose appropriate basis for computations
Process called "optimize_basis" that takes vector_space as VectorSpace returns List[Vector]:
    Let standard_basis be Linear.standard_basis(vector_space)
    Let condition_numbers be []
    
    For Each basis_vector in standard_basis:
        Let gram_matrix be Linear.compute_gram_matrix([basis_vector])
        condition_numbers.append(Linear.compute_condition_number(gram_matrix))
    
    If Linear.maximum(condition_numbers) > 1e6:
        Return Linear.gram_schmidt_orthogonalization(standard_basis)
    Otherwise:
        Return standard_basis
```

### Memory Efficiency
```runa
Note: Use sparse representations for large matrices
Process called "choose_representation" that takes matrix as Matrix returns Matrix:
    Let sparsity be Linear.compute_sparsity_ratio(matrix)
    If sparsity > 0.8:
        Return Linear.convert_to_sparse(matrix)
    Otherwise:
        Return matrix
```

### Error Analysis
```runa
Note: Propagate uncertainty through linear operations
Process called "error_aware_multiplication" that takes:
    A as Matrix,
    A_error as Matrix,
    B as Matrix,
    B_error as Matrix
returns Dictionary[String, Matrix]:
    Let result be Linear.matrix_multiplication(A, B)
    Let error_bound be Linear.matrix_addition(
        Linear.matrix_multiplication(A_error, B),
        Linear.matrix_multiplication(A, B_error)
    )
    
    Return Dictionary[String, Matrix]:
        "result": result
        "error_bound": error_bound
```

## Performance Considerations

- **Field Choice**: Computations over rationals are exact but slower than floating-point
- **Matrix Size**: Use specialized algorithms for large matrices (> 1000×1000)
- **Sparsity**: Exploit sparse structure when possible
- **Parallel Computation**: Many linear algebra operations can be parallelized
- **Memory Access**: Consider cache-friendly algorithms for dense matrices

This module provides comprehensive linear algebraic tools that integrate seamlessly with both abstract algebraic structures and numerical computation methods, making it ideal for both theoretical work and practical applications.