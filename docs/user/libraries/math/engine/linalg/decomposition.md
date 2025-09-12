# Matrix Decompositions

The Matrix Decompositions module (`math/engine/linalg/decomposition`) provides comprehensive matrix factorization algorithms for numerical linear algebra. This module implements state-of-the-art decomposition methods including LU, QR, Cholesky, SVD, and eigenvalue decompositions, essential for solving linear systems, optimization problems, and data analysis.

## Quick Start

```runa
Import "math/engine/linalg/decomposition" as Decomp
Import "math/engine/linalg/core" as LinAlg

Note: Create a symmetric positive definite matrix for demonstrations
Let matrix_a be LinAlg.create_matrix([
    [4.0, 2.0, 1.0],
    [2.0, 5.0, 3.0], 
    [1.0, 3.0, 6.0]
])

Note: LU Decomposition
Let lu_result be Decomp.lu_decomposition(matrix_a)
Let l_matrix be Decomp.get_l_matrix(lu_result)
Let u_matrix be Decomp.get_u_matrix(lu_result)
Let p_matrix be Decomp.get_permutation_matrix(lu_result)

Display "L matrix:" joined with LinAlg.matrix_to_string(l_matrix)
Display "U matrix:" joined with LinAlg.matrix_to_string(u_matrix)

Note: QR Decomposition
Let qr_result be Decomp.qr_decomposition(matrix_a)
Let q_matrix be Decomp.get_q_matrix(qr_result)
Let r_matrix be Decomp.get_r_matrix(qr_result)

Note: Eigenvalue Decomposition
Let eigen_result be Decomp.eigenvalue_decomposition(matrix_a)
Let eigenvalues be Decomp.get_eigenvalues(eigen_result)
Let eigenvectors be Decomp.get_eigenvectors(eigen_result)

Display "Eigenvalues: " joined with LinAlg.vector_to_string(eigenvalues)

Note: Singular Value Decomposition
Let svd_result be Decomp.singular_value_decomposition(matrix_a)
Let u_svd be Decomp.get_u_matrix(svd_result)
Let sigma be Decomp.get_singular_values(svd_result)
Let vt_svd be Decomp.get_vt_matrix(svd_result)

Display "Singular values: " joined with LinAlg.vector_to_string(sigma)
```

## LU Decomposition

### Basic LU Factorization

```runa
Note: Standard LU decomposition with partial pivoting
Let square_matrix be LinAlg.create_matrix([
    [2.0, 1.0, -1.0],
    [-3.0, -1.0, 2.0],
    [-2.0, 1.0, 2.0]
])

Let lu_decomp be Decomp.lu_decomposition(square_matrix)
Let lower_matrix be Decomp.get_l_matrix(lu_decomp)
Let upper_matrix be Decomp.get_u_matrix(lu_decomp)
Let pivot_matrix be Decomp.get_permutation_matrix(lu_decomp)

Note: Verify decomposition: P*A = L*U
Let pa_product be LinAlg.matrix_multiply(pivot_matrix, square_matrix)
Let lu_product be LinAlg.matrix_multiply(lower_matrix, upper_matrix)
Let verification_error be LinAlg.matrix_subtract(pa_product, lu_product)
Let error_norm be LinAlg.matrix_norm(verification_error, "frobenius")

Display "LU decomposition error: " joined with error_norm
```

### Advanced LU Methods

```runa
Note: Complete pivoting for maximum numerical stability
Let complete_pivot_lu be Decomp.lu_decomposition_complete_pivot(square_matrix)
Let row_permutation be Decomp.get_row_permutation(complete_pivot_lu)
Let col_permutation be Decomp.get_column_permutation(complete_pivot_lu)

Note: Block LU decomposition for large matrices
Let large_matrix be LinAlg.create_random_matrix(1000, 1000, "normal", 0.0, 1.0)
Let block_lu be Decomp.block_lu_decomposition(large_matrix, block_size: 256)

Note: Iterative refinement for improved accuracy
Let refined_lu be Decomp.lu_with_iterative_refinement(square_matrix, tolerance: 1e-12)
Let refinement_steps be Decomp.get_refinement_iterations(refined_lu)

Display "Refinement iterations: " joined with refinement_steps
```

## QR Decomposition

### Householder QR

```runa
Note: QR decomposition using Householder reflections
Let rectangular_matrix be LinAlg.create_matrix([
    [1.0, 2.0, 3.0],
    [4.0, 5.0, 6.0],
    [7.0, 8.0, 9.0],
    [10.0, 11.0, 12.0]
])

Let qr_householder be Decomp.qr_decomposition_householder(rectangular_matrix)
Let q_orthogonal be Decomp.get_q_matrix(qr_householder)
Let r_upper be Decomp.get_r_matrix(qr_householder)

Note: Verify orthogonality of Q matrix
Let q_transpose be LinAlg.transpose(q_orthogonal)
Let qtq_product be LinAlg.matrix_multiply(q_transpose, q_orthogonal)
Let identity_check be LinAlg.is_identity_matrix(qtq_product, tolerance: 1e-10)

Display "Q matrix is orthogonal: " joined with identity_check
```

### Gram-Schmidt QR

```runa
Note: Classical and Modified Gram-Schmidt
Let gs_qr_classical be Decomp.qr_decomposition_gram_schmidt(rectangular_matrix, "classical")
Let gs_qr_modified be Decomp.qr_decomposition_gram_schmidt(rectangular_matrix, "modified")

Note: Compare numerical stability
Let classical_error be Decomp.compute_orthogonality_error(gs_qr_classical)
Let modified_error be Decomp.compute_orthogonality_error(gs_qr_modified)

Display "Classical GS orthogonality error: " joined with classical_error
Display "Modified GS orthogonality error: " joined with modified_error

Note: QR with column pivoting for rank-deficient matrices
Let rank_deficient be LinAlg.create_matrix([
    [1.0, 2.0, 3.0],
    [2.0, 4.0, 6.0],
    [3.0, 6.0, 9.0]
])

Let pivoted_qr be Decomp.qr_decomposition_pivoted(rank_deficient)
Let column_pivots be Decomp.get_column_permutation(pivoted_qr)
Let numerical_rank be Decomp.get_numerical_rank(pivoted_qr, tolerance: 1e-10)

Display "Numerical rank: " joined with numerical_rank
```

## Cholesky Decomposition

### Standard Cholesky Factorization

```runa
Note: Cholesky decomposition for positive definite matrices
Let positive_definite be LinAlg.create_matrix([
    [9.0, 3.0, 1.0],
    [3.0, 5.0, 2.0],
    [1.0, 2.0, 4.0]
])

Note: Check positive definiteness
Let is_pos_def be Decomp.is_positive_definite(positive_definite)

If is_pos_def:
    Let cholesky_result be Decomp.cholesky_decomposition(positive_definite)
    Let lower_cholesky be Decomp.get_cholesky_factor(cholesky_result)
    
    Note: Verify decomposition: A = L*L^T
    Let lt_matrix be LinAlg.transpose(lower_cholesky)
    Let reconstruction be LinAlg.matrix_multiply(lower_cholesky, lt_matrix)
    Let cholesky_error be LinAlg.matrix_norm(
        LinAlg.matrix_subtract(positive_definite, reconstruction), 
        "frobenius"
    )
    
    Display "Cholesky reconstruction error: " joined with cholesky_error
Otherwise:
    Display "Matrix is not positive definite - Cholesky decomposition not applicable"
```

### Modified Cholesky and LDLT

```runa
Note: LDLT decomposition for symmetric indefinite matrices
Let symmetric_indefinite be LinAlg.create_matrix([
    [2.0, 1.0, 0.0],
    [1.0, -1.0, 1.0],
    [0.0, 1.0, 3.0]
])

Let ldlt_result be Decomp.ldlt_decomposition(symmetric_indefinite)
Let l_ldlt be Decomp.get_l_matrix(ldlt_result)
Let d_diagonal be Decomp.get_d_matrix(ldlt_result)
Let permutation_ldlt be Decomp.get_permutation_matrix(ldlt_result)

Note: Modified Cholesky for indefinite matrices
Let modified_chol be Decomp.modified_cholesky(symmetric_indefinite)
Let regularization_added be Decomp.get_regularization_parameter(modified_chol)
Let modified_factor be Decomp.get_cholesky_factor(modified_chol)

Display "Regularization parameter: " joined with regularization_added

Note: Pivoted Cholesky for semidefinite matrices
Let semidefinite_matrix be LinAlg.create_matrix([
    [4.0, 2.0, 2.0],
    [2.0, 1.0, 1.0],
    [2.0, 1.0, 1.0]
])

Let pivoted_chol be Decomp.pivoted_cholesky(semidefinite_matrix, tolerance: 1e-12)
Let pivot_sequence be Decomp.get_pivot_sequence(pivoted_chol)
Let effective_rank be Decomp.get_effective_rank(pivoted_chol)

Display "Effective rank from pivoted Cholesky: " joined with effective_rank
```

## Singular Value Decomposition (SVD)

### Full and Reduced SVD

```runa
Note: Full SVD decomposition
Let data_matrix be LinAlg.create_matrix([
    [1.0, 2.0, 3.0, 4.0],
    [5.0, 6.0, 7.0, 8.0],
    [9.0, 10.0, 11.0, 12.0]
])

Let full_svd be Decomp.singular_value_decomposition(data_matrix, "full")
Let u_full be Decomp.get_u_matrix(full_svd)
Let sigma_full be Decomp.get_singular_values(full_svd)
Let vt_full be Decomp.get_vt_matrix(full_svd)

Note: Reduced (economy) SVD for efficiency
Let reduced_svd be Decomp.singular_value_decomposition(data_matrix, "reduced")
Let u_reduced be Decomp.get_u_matrix(reduced_svd)
Let sigma_reduced be Decomp.get_singular_values(reduced_svd)
Let vt_reduced be Decomp.get_vt_matrix(reduced_svd)

Display "Number of singular values (full): " joined with LinAlg.vector_length(sigma_full)
Display "Number of singular values (reduced): " joined with LinAlg.vector_length(sigma_reduced)
```

### Specialized SVD Applications

```runa
Note: Truncated SVD for low-rank approximation
Let rank_k_approx be Decomp.truncated_svd(data_matrix, rank: 2)
Let approx_matrix be Decomp.reconstruct_from_truncated_svd(rank_k_approx)
Let approximation_error be LinAlg.matrix_norm(
    LinAlg.matrix_subtract(data_matrix, approx_matrix),
    "frobenius"
)

Display "Rank-2 approximation error: " joined with approximation_error

Note: Randomized SVD for large matrices
Let large_data be LinAlg.create_random_matrix(5000, 1000, "normal", 0.0, 1.0)
Let randomized_svd be Decomp.randomized_svd(
    large_data, 
    target_rank: 50,
    oversampling: 10,
    power_iterations: 2
)

Note: SVD-based pseudoinverse
Let pseudoinverse be Decomp.pseudoinverse_via_svd(data_matrix, tolerance: 1e-12)
Let moore_penrose_check be LinAlg.matrix_multiply(
    LinAlg.matrix_multiply(data_matrix, pseudoinverse),
    data_matrix
)
Let pseudoinverse_error be LinAlg.matrix_norm(
    LinAlg.matrix_subtract(data_matrix, moore_penrose_check),
    "frobenius"
)

Display "Pseudoinverse verification error: " joined with pseudoinverse_error
```

## Eigenvalue Decomposition

### Standard Eigenvalue Problems

```runa
Note: Eigenvalue decomposition for symmetric matrices
Let symmetric_matrix be LinAlg.create_matrix([
    [6.0, 2.0, 1.0],
    [2.0, 3.0, 1.0],
    [1.0, 1.0, 1.0]
])

Let symmetric_eigen be Decomp.symmetric_eigenvalue_decomposition(symmetric_matrix)
Let eigenvalues_sym be Decomp.get_eigenvalues(symmetric_eigen)
Let eigenvectors_sym be Decomp.get_eigenvectors(symmetric_eigen)

Note: Sort eigenvalues in descending order
Let sorted_eigen be Decomp.sort_eigenvalues(symmetric_eigen, "descending")
Let largest_eigenvalue be Decomp.get_largest_eigenvalue(sorted_eigen)
Let smallest_eigenvalue be Decomp.get_smallest_eigenvalue(sorted_eigen)

Display "Largest eigenvalue: " joined with largest_eigenvalue
Display "Smallest eigenvalue: " joined with smallest_eigenvalue

Note: General (non-symmetric) eigenvalue decomposition
Let general_matrix be LinAlg.create_matrix([
    [1.0, 2.0, 0.0],
    [0.0, 3.0, 4.0],
    [5.0, 6.0, 7.0]
])

Let general_eigen be Decomp.eigenvalue_decomposition(general_matrix)
Let complex_eigenvalues be Decomp.get_eigenvalues(general_eigen)
Let complex_eigenvectors be Decomp.get_eigenvectors(general_eigen)

Note: Check for complex eigenvalues
Let has_complex be Decomp.has_complex_eigenvalues(general_eigen)
Display "Matrix has complex eigenvalues: " joined with has_complex
```

### Specialized Eigenvalue Methods

```runa
Note: Power method for dominant eigenvalue
Let dominant_eigen be Decomp.power_method(
    general_matrix,
    initial_vector: LinAlg.create_random_vector(3, "normal", 0.0, 1.0),
    max_iterations: 1000,
    tolerance: 1e-10
)

Let dominant_value be Decomp.get_dominant_eigenvalue(dominant_eigen)
Let dominant_vector be Decomp.get_dominant_eigenvector(dominant_eigen)
Let power_iterations be Decomp.get_iteration_count(dominant_eigen)

Display "Dominant eigenvalue (power method): " joined with dominant_value
Display "Power method iterations: " joined with power_iterations

Note: Inverse power method for smallest eigenvalue
Let smallest_eigen be Decomp.inverse_power_method(
    general_matrix,
    shift: 0.0,
    max_iterations: 1000,
    tolerance: 1e-10
)

Note: QR algorithm for all eigenvalues
Let qr_eigen be Decomp.qr_eigenvalue_algorithm(
    symmetric_matrix,
    max_iterations: 1000,
    tolerance: 1e-12
)

Let qr_convergence be Decomp.check_convergence(qr_eigen)
Display "QR algorithm converged: " joined with qr_convergence
```

### Generalized Eigenvalue Problems

```runa
Note: Generalized eigenvalue problem A*x = λ*B*x
Let matrix_b be LinAlg.create_matrix([
    [2.0, 1.0, 0.0],
    [1.0, 2.0, 1.0],
    [0.0, 1.0, 2.0]
])

Let generalized_eigen be Decomp.generalized_eigenvalue_decomposition(matrix_a, matrix_b)
Let gen_eigenvalues be Decomp.get_generalized_eigenvalues(generalized_eigen)
Let gen_eigenvectors be Decomp.get_generalized_eigenvectors(generalized_eigen)

Note: Verify generalized eigenvalue equation
Let first_eigenvalue be LinAlg.get_element(gen_eigenvalues, 0)
Let first_eigenvector be LinAlg.get_column(gen_eigenvectors, 0)

Let ax_product be LinAlg.matrix_vector_multiply(matrix_a, first_eigenvector)
Let bx_product be LinAlg.matrix_vector_multiply(matrix_b, first_eigenvector)
Let lambda_bx be LinAlg.vector_scalar_multiply(bx_product, first_eigenvalue)

Let verification_error be LinAlg.vector_norm(
    LinAlg.vector_subtract(ax_product, lambda_bx),
    "euclidean"
)

Display "Generalized eigenvalue verification error: " joined with verification_error
```

## Specialized Decompositions

### Schur Decomposition

```runa
Note: Real Schur form for general matrices
Let schur_decomp be Decomp.schur_decomposition(general_matrix)
Let orthogonal_q be Decomp.get_schur_q_matrix(schur_decomp)
Let upper_triangular_t be Decomp.get_schur_t_matrix(schur_decomp)

Note: Complex Schur form
Let complex_schur be Decomp.complex_schur_decomposition(general_matrix)
Let complex_q be Decomp.get_schur_q_matrix(complex_schur)
Let complex_t be Decomp.get_schur_t_matrix(complex_schur)

Note: Ordered Schur decomposition
Let ordered_schur be Decomp.ordered_schur_decomposition(
    general_matrix,
    ordering_criterion: "largest_real_part"
)
```

### Hessenberg Reduction

```runa
Note: Upper Hessenberg form (preprocessing for eigenvalue algorithms)
Let hessenberg_form be Decomp.hessenberg_reduction(general_matrix)
Let hessenberg_matrix be Decomp.get_hessenberg_matrix(hessenberg_form)
Let transformation_matrix be Decomp.get_transformation_matrix(hessenberg_form)

Note: Verify similarity transformation
Let similarity_check be LinAlg.matrix_multiply(
    transformation_matrix,
    LinAlg.matrix_multiply(general_matrix, LinAlg.transpose(transformation_matrix))
)
Let similarity_error be LinAlg.matrix_norm(
    LinAlg.matrix_subtract(hessenberg_matrix, similarity_check),
    "frobenius"
)

Display "Hessenberg similarity error: " joined with similarity_error
```

### Jordan Canonical Form

```runa
Note: Jordan decomposition for defective matrices
Let defective_matrix be LinAlg.create_matrix([
    [2.0, 1.0, 0.0],
    [0.0, 2.0, 1.0],
    [0.0, 0.0, 2.0]
])

Let jordan_decomp be Decomp.jordan_canonical_form(defective_matrix)
Let jordan_matrix be Decomp.get_jordan_matrix(jordan_decomp)
Let similarity_transform be Decomp.get_similarity_matrix(jordan_decomp)

Note: Identify Jordan blocks
Let jordan_blocks be Decomp.identify_jordan_blocks(jordan_matrix)
Let block_sizes be Decomp.get_jordan_block_sizes(jordan_blocks)

Display "Jordan block sizes: " joined with LinAlg.vector_to_string(block_sizes)
```

## Numerical Considerations

### Condition Numbers and Stability

```runa
Import "core/error_handling" as ErrorHandling

Note: Monitor numerical stability of decompositions
Let condition_lu be Decomp.estimate_lu_condition_number(lu_decomp)
Let condition_qr be Decomp.estimate_qr_condition_number(qr_result)
Let condition_chol be Decomp.estimate_cholesky_condition_number(cholesky_result)

Display "LU condition number: " joined with condition_lu
Display "QR condition number: " joined with condition_qr

Note: Backward error analysis
Let backward_error_lu be Decomp.compute_backward_error(square_matrix, lu_decomp)
Let forward_error_lu be Decomp.compute_forward_error(square_matrix, lu_decomp)

If backward_error_lu > 1e-12:
    Display "Warning: Large backward error in LU decomposition"
    Let iteratively_refined be Decomp.refine_lu_decomposition(square_matrix, lu_decomp)
```

### Rank Detection and Handling

```runa
Note: Robust rank detection using SVD
Let rank_deficient_matrix be LinAlg.create_matrix([
    [1.0, 2.0, 3.0],
    [2.0, 4.0, 6.0],
    [1.0, 2.0, 3.0]
])

Let svd_rank be Decomp.svd_rank_detection(rank_deficient_matrix, tolerance: 1e-12)
Let numerical_nullity be Decomp.compute_numerical_nullity(rank_deficient_matrix, tolerance: 1e-12)

Display "Matrix rank: " joined with svd_rank
Display "Numerical nullity: " joined with numerical_nullity

Note: Null space computation
Let null_space be Decomp.compute_null_space(rank_deficient_matrix)
Let null_space_dimension be LinAlg.get_column_count(null_space)

Display "Null space dimension: " joined with null_space_dimension

Note: Range space computation
Let range_space be Decomp.compute_range_space(rank_deficient_matrix)
Let range_dimension be LinAlg.get_column_count(range_space)

Display "Range space dimension: " joined with range_dimension
```

## Performance and Memory Management

### Large-Scale Decompositions

```runa
Note: Block-based algorithms for large matrices
Let very_large_matrix be LinAlg.create_random_matrix(10000, 10000, "normal", 0.0, 1.0)

Note: Configure block size for optimal cache usage
Decomp.set_block_size(512)
Decomp.enable_parallel_decomposition(True)
Decomp.set_memory_limit(8 * 1024 * 1024 * 1024)  Note: 8GB limit

Let large_qr be Decomp.block_qr_decomposition(very_large_matrix)
Let large_svd be Decomp.incremental_svd(very_large_matrix, rank: 100)

Note: Out-of-core decompositions
Let out_of_core_svd be Decomp.out_of_core_svd(
    "huge_matrix_file.dat",
    target_rank: 50,
    memory_budget: 1024 * 1024 * 1024  Note: 1GB memory budget
)
```

### Incremental and Online Algorithms

```runa
Note: Incremental QR for streaming data
Let qr_state be Decomp.initialize_incremental_qr(initial_columns: 3)

Note: Process new columns one by one
For column_index from 0 to 9:
    Let new_column be LinAlg.create_random_vector(100, "normal", 0.0, 1.0)
    Decomp.update_incremental_qr(qr_state, new_column)
    
    Let current_q be Decomp.get_current_q_matrix(qr_state)
    Let current_r be Decomp.get_current_r_matrix(qr_state)
    
    Display "Processed column " joined with column_index joined with ", R matrix size: " 
        joined with LinAlg.get_row_count(current_r) joined with "x" 
        joined with LinAlg.get_column_count(current_r)

Note: Online SVD updates
Let streaming_svd be Decomp.initialize_streaming_svd(target_rank: 20)

For batch_index from 0 to 4:
    Let data_batch be LinAlg.create_random_matrix(100, 50, "normal", 0.0, 1.0)
    Decomp.update_streaming_svd(streaming_svd, data_batch)
    
    Let current_singular_values be Decomp.get_current_singular_values(streaming_svd)
    Display "Batch " joined with batch_index joined with " processed, largest singular value: " 
        joined with LinAlg.get_element(current_singular_values, 0)
```

## Integration Examples

### Machine Learning Applications

```runa
Import "ml/preprocessing" as MLPrep
Import "ml/dimensionality_reduction" as DimRed

Note: PCA using SVD
Let data_matrix be LinAlg.create_matrix_from_csv("dataset.csv")
Let centered_data be MLPrep.center_columns(data_matrix)
Let pca_svd be Decomp.singular_value_decomposition(centered_data, "reduced")

Let principal_components be Decomp.get_vt_matrix(pca_svd)
Let explained_variance be Decomp.compute_explained_variance_ratio(pca_svd)

Display "First 3 PCs explain " joined with (LinAlg.sum(LinAlg.get_subvector(explained_variance, 0, 3)) * 100) joined with "% of variance"

Note: Linear discriminant analysis using generalized eigenvalues
Let within_scatter be DimRed.compute_within_class_scatter(data_matrix, class_labels)
Let between_scatter be DimRed.compute_between_class_scatter(data_matrix, class_labels)

Let lda_eigen be Decomp.generalized_eigenvalue_decomposition(between_scatter, within_scatter)
Let discriminant_directions be Decomp.get_generalized_eigenvectors(lda_eigen)
```

### Signal Processing Applications

```runa
Import "signal/analysis" as Signal

Note: Spectral decomposition for signal analysis
Let signal_matrix be Signal.create_hankel_matrix(time_series_data, window_size: 100)
Let signal_svd be Decomp.singular_value_decomposition(signal_matrix, "full")

Let signal_components be Decomp.separate_signal_components(signal_svd, noise_threshold: 0.01)
Let denoised_signal be Decomp.reconstruct_denoised_signal(signal_components)

Note: Toeplitz matrix eigenvalue decomposition
Let autocorr_matrix be Signal.compute_autocorrelation_matrix(time_series_data, lags: 50)
Let toeplitz_eigen be Decomp.symmetric_eigenvalue_decomposition(autocorr_matrix)

Let spectral_density be Decomp.estimate_spectral_density(toeplitz_eigen)
Display "Dominant frequency component: " joined with Signal.find_peak_frequency(spectral_density)
```

## Best Practices

### Algorithm Selection Guide

```runa
Note: Choose optimal decomposition based on matrix properties
Let matrix_properties be Decomp.analyze_matrix_properties(input_matrix)

If Decomp.is_symmetric(matrix_properties) and Decomp.is_positive_definite(matrix_properties):
    Display "Recommendation: Use Cholesky decomposition for optimal efficiency"
    Let recommended_decomp be Decomp.cholesky_decomposition(input_matrix)

Otherwise If Decomp.is_symmetric(matrix_properties):
    Display "Recommendation: Use symmetric eigenvalue decomposition"
    Let recommended_decomp be Decomp.symmetric_eigenvalue_decomposition(input_matrix)

Otherwise If Decomp.is_tall_thin(matrix_properties):
    Display "Recommendation: Use QR decomposition for least squares problems"
    Let recommended_decomp be Decomp.qr_decomposition(input_matrix)

Otherwise:
    Display "Recommendation: Use LU decomposition with partial pivoting"
    Let recommended_decomp be Decomp.lu_decomposition(input_matrix)
```

### Error Handling and Robustness

```runa
Note: Robust decomposition with fallback strategies
Let robust_result be Decomp.robust_matrix_decomposition(
    potentially_ill_conditioned_matrix,
    primary_method: "cholesky",
    fallback_methods: ["ldlt", "lu_complete_pivot"],
    conditioning_threshold: 1e12
)

If ErrorHandling.is_success(robust_result):
    Let final_decomposition be ErrorHandling.get_result(robust_result)
    Display "Successful decomposition using " joined with Decomp.get_method_used(final_decomposition)
Otherwise:
    Let error_info be ErrorHandling.get_error_info(robust_result)
    Display "All decomposition methods failed: " joined with ErrorHandling.get_error_message(error_info)
```

The Matrix Decompositions module provides essential numerical linear algebra tools for factorizing matrices into simpler, more computationally tractable forms, enabling efficient solutions to a wide range of mathematical and scientific computing problems.