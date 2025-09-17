# Tensor Operations

The Tensor Operations module (`math/engine/linalg/tensor`) provides comprehensive support for multi-dimensional array operations, tensor algebra, and advanced tensor computations. This module implements efficient algorithms for tensor manipulation, contraction, broadcasting, and specialized operations essential for machine learning, scientific computing, and multi-dimensional data analysis.

## Quick Start

```runa
Import "math/engine/linalg/tensor" as Tensor
Import "math/engine/linalg/core" as LinAlg

Note: Create tensors of different shapes
Let vector_tensor be Tensor.create_tensor_from_vector([1.0, 2.0, 3.0, 4.0])
Let matrix_tensor be Tensor.create_tensor_from_matrix([
    [1.0, 2.0, 3.0],
    [4.0, 5.0, 6.0]
])

Let tensor_3d be Tensor.create_tensor([2, 3, 4], "zeros")
Let random_tensor be Tensor.create_random_tensor([3, 4, 5], "normal", 0.0, 1.0)

Display "Vector tensor shape: " joined with Tensor.shape_to_string(Tensor.get_shape(vector_tensor))
Display "Matrix tensor shape: " joined with Tensor.shape_to_string(Tensor.get_shape(matrix_tensor))
Display "3D tensor shape: " joined with Tensor.shape_to_string(Tensor.get_shape(tensor_3d))

Note: Basic tensor operations
Let tensor_a be Tensor.create_random_tensor([2, 3, 4], "uniform", -1.0, 1.0)
Let tensor_b be Tensor.create_random_tensor([2, 3, 4], "uniform", -1.0, 1.0)

Let tensor_sum be Tensor.tensor_add(tensor_a, tensor_b)
Let tensor_product be Tensor.tensor_multiply(tensor_a, tensor_b)  Note: Element-wise
Let scalar_scaled be Tensor.tensor_scalar_multiply(tensor_a, 2.5)

Note: Tensor reductions
Let tensor_sum_all be Tensor.tensor_sum(tensor_a)
Let tensor_mean be Tensor.tensor_mean(tensor_a)
Let tensor_max be Tensor.tensor_max(tensor_a)

Display "Tensor sum: " joined with tensor_sum_all
Display "Tensor mean: " joined with tensor_mean
Display "Tensor max: " joined with tensor_max

Note: Axis-specific reductions
Let sum_axis_0 be Tensor.tensor_sum_axis(tensor_a, axis: 0)
Let mean_axis_1 be Tensor.tensor_mean_axis(tensor_a, axis: 1)

Display "Sum along axis 0 shape: " joined with Tensor.shape_to_string(Tensor.get_shape(sum_axis_0))
Display "Mean along axis 1 shape: " joined with Tensor.shape_to_string(Tensor.get_shape(mean_axis_1))
```

## Tensor Creation and Manipulation

### Tensor Construction

```runa
Note: Different tensor creation methods
Let zeros_tensor be Tensor.create_zeros([3, 4, 5])
Let ones_tensor be Tensor.create_ones([2, 6])
Let identity_tensor be Tensor.create_identity([4, 4])
Let diagonal_tensor be Tensor.create_diagonal([1.0, 2.0, 3.0, 4.0])

Note: Tensor from data
Let data_3d be [
    [
        [1.0, 2.0], 
        [3.0, 4.0]
    ],
    [
        [5.0, 6.0],
        [7.0, 8.0]
    ]
]

Let tensor_from_data be Tensor.create_tensor_from_data(data_3d)
Let tensor_shape be Tensor.get_shape(tensor_from_data)
Let tensor_ndim be Tensor.get_ndim(tensor_from_data)
Let tensor_size be Tensor.get_size(tensor_from_data)

Display "Tensor dimensions: " joined with tensor_ndim
Display "Total tensor size: " joined with tensor_size

Note: Special tensor patterns
Let arange_tensor be Tensor.arange(0.0, 24.0, 1.0)
Let reshaped_arange be Tensor.reshape(arange_tensor, [2, 3, 4])

Let linspace_tensor be Tensor.linspace(0.0, 1.0, 100)
Let meshgrid_result be Tensor.meshgrid(
    Tensor.linspace(-2.0, 2.0, 50),
    Tensor.linspace(-2.0, 2.0, 50)
)

Let x_grid be Tensor.get_meshgrid_x(meshgrid_result)
Let y_grid be Tensor.get_meshgrid_y(meshgrid_result)

Display "Meshgrid X shape: " joined with Tensor.shape_to_string(Tensor.get_shape(x_grid))
```

### Shape Manipulation

```runa
Note: Reshape operations
Let original_tensor be Tensor.create_random_tensor([24], "normal", 0.0, 1.0)

Let reshaped_2d be Tensor.reshape(original_tensor, [4, 6])
Let reshaped_3d be Tensor.reshape(original_tensor, [2, 3, 4])
Let reshaped_4d be Tensor.reshape(original_tensor, [1, 2, 3, 4])

Note: Squeeze and unsqueeze operations
Let tensor_with_ones be Tensor.create_random_tensor([1, 5, 1, 3], "uniform", 0.0, 1.0)
Let squeezed_tensor be Tensor.squeeze(tensor_with_ones)
Let unsqueezed_tensor be Tensor.unsqueeze(reshaped_2d, axis: 0)

Display "Original shape: " joined with Tensor.shape_to_string(Tensor.get_shape(tensor_with_ones))
Display "Squeezed shape: " joined with Tensor.shape_to_string(Tensor.get_shape(squeezed_tensor))
Display "Unsqueezed shape: " joined with Tensor.shape_to_string(Tensor.get_shape(unsqueezed_tensor))

Note: Transpose and permutation operations
Let tensor_4d be Tensor.create_random_tensor([2, 3, 4, 5], "normal", 0.0, 1.0)
Let transposed_tensor be Tensor.transpose(tensor_4d, axes: [0, 2, 1, 3])

Let permutation_axes be [3, 0, 2, 1]
Let permuted_tensor be Tensor.permute_axes(tensor_4d, permutation_axes)

Display "Original 4D shape: " joined with Tensor.shape_to_string(Tensor.get_shape(tensor_4d))
Display "Transposed shape: " joined with Tensor.shape_to_string(Tensor.get_shape(transposed_tensor))
Display "Permuted shape: " joined with Tensor.shape_to_string(Tensor.get_shape(permuted_tensor))

Note: Flatten and ravel operations
Let flattened_tensor be Tensor.flatten(tensor_4d)
Let raveled_tensor be Tensor.ravel(tensor_4d, order: "C")  Note: Row-major order

Display "Flattened shape: " joined with Tensor.shape_to_string(Tensor.get_shape(flattened_tensor))
```

## Broadcasting and Element-wise Operations

### Broadcasting Mechanics

```runa
Note: Understand broadcasting rules
Let small_tensor be Tensor.create_tensor([3, 1], "ones")
Let large_tensor be Tensor.create_random_tensor([2, 3, 5], "normal", 0.0, 1.0)

Let broadcast_compatible be Tensor.is_broadcast_compatible(small_tensor, large_tensor)
Display "Tensors are broadcast compatible: " joined with broadcast_compatible

If broadcast_compatible:
    Let broadcast_result be Tensor.broadcast_add(large_tensor, small_tensor)
    Display "Broadcast result shape: " joined with Tensor.shape_to_string(Tensor.get_shape(broadcast_result))

Note: Explicit broadcasting
Let broadcast_small be Tensor.broadcast_to(small_tensor, [2, 3, 5])
Let broadcast_shapes be Tensor.broadcast_shapes([[2, 3, 5], [3, 1], [1, 5]])

Display "Broadcast target shape: " joined with Tensor.shape_to_string(broadcast_shapes)

Note: Broadcasting with different operations
Let vector_1d be Tensor.create_tensor([5], "ones")
Let matrix_2d be Tensor.create_random_tensor([3, 5], "uniform", 0.0, 1.0)

Let broadcast_multiply be Tensor.broadcast_multiply(matrix_2d, vector_1d)
Let broadcast_divide be Tensor.broadcast_divide(matrix_2d, vector_1d)
Let broadcast_power be Tensor.broadcast_power(matrix_2d, vector_1d)

Note: Advanced broadcasting patterns
Let tensor_batch be Tensor.create_random_tensor([32, 64, 64, 3], "normal", 0.0, 1.0)  Note: Batch of images
Let normalization_stats be Tensor.create_random_tensor([3], "uniform", 0.5, 1.5)     Note: Per-channel stats

Let normalized_batch be Tensor.broadcast_divide(tensor_batch, normalization_stats)
Display "Normalized batch shape: " joined with Tensor.shape_to_string(Tensor.get_shape(normalized_batch))
```

### Element-wise Mathematical Operations

```runa
Note: Basic arithmetic operations
Let tensor_x be Tensor.create_random_tensor([3, 4], "uniform", -2.0, 2.0)
Let tensor_y be Tensor.create_random_tensor([3, 4], "uniform", -2.0, 2.0)

Let add_result be Tensor.tensor_add(tensor_x, tensor_y)
Let subtract_result be Tensor.tensor_subtract(tensor_x, tensor_y)
Let multiply_result be Tensor.tensor_multiply(tensor_x, tensor_y)
Let divide_result be Tensor.tensor_divide(tensor_x, tensor_y)

Note: Mathematical functions
Let abs_result be Tensor.tensor_abs(tensor_x)
Let sqrt_result be Tensor.tensor_sqrt(Tensor.tensor_abs(tensor_x))
Let exp_result be Tensor.tensor_exp(tensor_x)
Let log_result be Tensor.tensor_log(Tensor.tensor_abs(tensor_x))

Note: Trigonometric functions
Let sin_result be Tensor.tensor_sin(tensor_x)
Let cos_result be Tensor.tensor_cos(tensor_x)
Let tan_result be Tensor.tensor_tan(tensor_x)
Let arcsin_result be Tensor.tensor_arcsin(Tensor.tensor_clamp(tensor_x, -1.0, 1.0))

Note: Hyperbolic functions
Let sinh_result be Tensor.tensor_sinh(tensor_x)
Let cosh_result be Tensor.tensor_cosh(tensor_x)
Let tanh_result be Tensor.tensor_tanh(tensor_x)

Note: Rounding and clipping
Let rounded_tensor be Tensor.tensor_round(tensor_x)
Let floor_tensor be Tensor.tensor_floor(tensor_x)
Let ceil_tensor be Tensor.tensor_ceil(tensor_x)
Let clipped_tensor be Tensor.tensor_clamp(tensor_x, -1.0, 1.0)

Display "Original tensor range: [" joined with Tensor.tensor_min(tensor_x) 
    joined with ", " joined with Tensor.tensor_max(tensor_x) joined with "]"
Display "Clipped tensor range: [" joined with Tensor.tensor_min(clipped_tensor) 
    joined with ", " joined with Tensor.tensor_max(clipped_tensor) joined with "]"
```

## Tensor Contractions and Einstein Summation

### Basic Tensor Contractions

```runa
Note: Matrix-vector multiplication as tensor contraction
Let matrix_tensor be Tensor.create_random_tensor([4, 6], "normal", 0.0, 1.0)
Let vector_tensor be Tensor.create_random_tensor([6], "normal", 0.0, 1.0)

Let matvec_result be Tensor.tensor_contract(matrix_tensor, vector_tensor, axes: [1], [0])
Display "Matrix-vector result shape: " joined with Tensor.shape_to_string(Tensor.get_shape(matvec_result))

Note: Matrix-matrix multiplication  
Let matrix_a be Tensor.create_random_tensor([3, 4], "normal", 0.0, 1.0)
Let matrix_b be Tensor.create_random_tensor([4, 5], "normal", 0.0, 1.0)

Let matmul_result be Tensor.tensor_matmul(matrix_a, matrix_b)
Let contract_result be Tensor.tensor_contract(matrix_a, matrix_b, axes: [1], [0])

Display "Matrix multiplication shape: " joined with Tensor.shape_to_string(Tensor.get_shape(matmul_result))

Note: Batch matrix multiplication
Let batch_matrices_a be Tensor.create_random_tensor([10, 3, 4], "normal", 0.0, 1.0)
Let batch_matrices_b be Tensor.create_random_tensor([10, 4, 5], "normal", 0.0, 1.0)

Let batch_matmul_result be Tensor.tensor_batch_matmul(batch_matrices_a, batch_matrices_b)
Display "Batch matmul shape: " joined with Tensor.shape_to_string(Tensor.get_shape(batch_matmul_result))

Note: Tensor dot products and inner products
Let tensor_3d_a be Tensor.create_random_tensor([2, 3, 4], "normal", 0.0, 1.0)
Let tensor_3d_b be Tensor.create_random_tensor([2, 3, 4], "normal", 0.0, 1.0)

Let tensor_dot_product be Tensor.tensor_dot(tensor_3d_a, tensor_3d_b)
Let frobenius_inner_product be Tensor.tensor_inner_product(tensor_3d_a, tensor_3d_b)

Display "Tensor dot product: " joined with tensor_dot_product
Display "Frobenius inner product: " joined with frobenius_inner_product
```

### Einstein Summation Convention

```runa
Note: Einstein summation notation for tensor operations
Let tensor_i be Tensor.create_random_tensor([3], "normal", 0.0, 1.0)
Let tensor_j be Tensor.create_random_tensor([4], "normal", 0.0, 1.0)
Let tensor_ij be Tensor.create_random_tensor([3, 4], "normal", 0.0, 1.0)
Let tensor_ijk be Tensor.create_random_tensor([3, 4, 5], "normal", 0.0, 1.0)

Note: Basic Einstein sum operations
Let outer_product be Tensor.einsum("i,j->ij", [tensor_i, tensor_j])
Let trace_operation be Tensor.einsum("ii->", [tensor_ij])
Let diagonal_extraction be Tensor.einsum("ii->i", [tensor_ij])

Display "Outer product shape: " joined with Tensor.shape_to_string(Tensor.get_shape(outer_product))
Display "Trace result: " joined with trace_operation

Note: Matrix operations via Einstein summation
Let matrix_A be Tensor.create_random_tensor([4, 3], "normal", 0.0, 1.0)
Let matrix_B be Tensor.create_random_tensor([3, 5], "normal", 0.0, 1.0)

Let einsum_matmul be Tensor.einsum("ik,kj->ij", [matrix_A, matrix_B])
Let einsum_transpose be Tensor.einsum("ij->ji", [matrix_A])

Note: Advanced tensor contractions
Let tensor_4d_A be Tensor.create_random_tensor([2, 3, 4, 5], "normal", 0.0, 1.0)
Let tensor_4d_B be Tensor.create_random_tensor([5, 6, 2, 7], "normal", 0.0, 1.0)

Let complex_contraction be Tensor.einsum("abcd,efag->bcdefg", [tensor_4d_A, tensor_4d_B])
Display "Complex contraction shape: " joined with Tensor.shape_to_string(Tensor.get_shape(complex_contraction))

Note: Bilinear operations
Let bilinear_tensor be Tensor.create_random_tensor([3, 4, 5], "normal", 0.0, 1.0)
Let vector_u be Tensor.create_random_tensor([3], "normal", 0.0, 1.0)
Let vector_v be Tensor.create_random_tensor([5], "normal", 0.0, 1.0)

Let bilinear_form be Tensor.einsum("ijk,i,k->j", [bilinear_tensor, vector_u, vector_v])
Display "Bilinear form result shape: " joined with Tensor.shape_to_string(Tensor.get_shape(bilinear_form))
```

## Advanced Tensor Operations

### Tensor Decompositions

```runa
Import "math/engine/linalg/decomposition" as Decomp

Note: Higher-order SVD (HOSVD) for tensor decomposition
Let tensor_3d_data be Tensor.create_random_tensor([10, 15, 20], "normal", 0.0, 1.0)

Let hosvd_result be Tensor.higher_order_svd(tensor_3d_data, target_ranks: [5, 8, 10])
Let core_tensor be Tensor.get_hosvd_core(hosvd_result)
Let mode_matrices be Tensor.get_hosvd_modes(hosvd_result)

Display "HOSVD core shape: " joined with Tensor.shape_to_string(Tensor.get_shape(core_tensor))
Display "Number of mode matrices: " joined with LinAlg.vector_length(mode_matrices)

Note: CP (CANDECOMP/PARAFAC) decomposition
Let cp_decomp_result be Tensor.cp_decomposition(
    tensor_3d_data,
    rank: 5,
    max_iterations: 100,
    tolerance: 1e-6
)

Let cp_factors be Tensor.get_cp_factors(cp_decomp_result)
Let cp_reconstruction_error be Tensor.get_cp_reconstruction_error(cp_decomp_result)

Display "CP decomposition rank: " joined with LinAlg.vector_length(LinAlg.get_element(cp_factors, 0))
Display "CP reconstruction error: " joined with cp_reconstruction_error

Note: Tucker decomposition
Let tucker_result be Tensor.tucker_decomposition(
    tensor_3d_data,
    core_shape: [5, 7, 9],
    max_iterations: 50
)

Let tucker_core be Tensor.get_tucker_core(tucker_result)
Let tucker_factors be Tensor.get_tucker_factors(tucker_result)

Let reconstructed_tensor be Tensor.reconstruct_from_tucker(tucker_result)
Let tucker_compression_ratio be Tensor.compute_compression_ratio(tensor_3d_data, tucker_result)

Display "Tucker compression ratio: " joined with tucker_compression_ratio
```

### Tensor Networks

```runa
Note: Matrix Product State (MPS) representation
Let tensor_chain_data be [
    Tensor.create_random_tensor([2, 3], "normal", 0.0, 1.0),
    Tensor.create_random_tensor([3, 4, 5], "normal", 0.0, 1.0),
    Tensor.create_random_tensor([5, 6, 7], "normal", 0.0, 1.0),
    Tensor.create_random_tensor([7, 2], "normal", 0.0, 1.0)
]

Let mps_representation be Tensor.create_mps(tensor_chain_data)
Let mps_bond_dimensions be Tensor.get_mps_bond_dimensions(mps_representation)

Display "MPS bond dimensions: " joined with LinAlg.vector_to_string(mps_bond_dimensions)

Note: Tensor contraction networks
Let contraction_network be Tensor.create_contraction_network()

Tensor.add_tensor_to_network(contraction_network, "A", tensor_4d_A, indices: ["i", "j", "k", "l"])
Tensor.add_tensor_to_network(contraction_network, "B", tensor_4d_B, indices: ["l", "m", "i", "n"])

Let network_contraction_result be Tensor.contract_network(
    contraction_network,
    output_indices: ["j", "k", "m", "n"]
)

Display "Network contraction result shape: " 
    joined with Tensor.shape_to_string(Tensor.get_shape(network_contraction_result))

Note: Optimize contraction path
Let optimal_path be Tensor.optimize_contraction_path(
    contraction_network,
    optimization_method: "greedy"
)

Let contraction_cost be Tensor.estimate_contraction_cost(optimal_path)
Display "Estimated contraction cost: " joined with contraction_cost joined with " FLOPs"
```

### Sparse Tensors

```runa
Import "math/engine/linalg/sparse" as Sparse

Note: Create sparse tensors
Let sparse_indices be [
    [0, 1, 2],
    [1, 2, 0],
    [2, 0, 1],
    [0, 0, 0],
    [1, 1, 1]
]

Let sparse_values be [1.5, 2.3, -1.2, 3.7, -0.8]
Let sparse_shape be [3, 3, 3]

Let sparse_tensor be Tensor.create_sparse_tensor(sparse_indices, sparse_values, sparse_shape)

Display "Sparse tensor density: " joined with Tensor.compute_sparse_density(sparse_tensor)
Display "Sparse tensor nnz: " joined with Tensor.get_sparse_nnz(sparse_tensor)

Note: Sparse tensor operations
Let dense_conversion be Tensor.sparse_to_dense(sparse_tensor)
Let sparse_sum be Tensor.sparse_tensor_sum(sparse_tensor)

Note: Sparse tensor arithmetic
Let sparse_tensor_2 be Tensor.create_random_sparse_tensor([3, 3, 3], density: 0.2)
Let sparse_add_result be Tensor.sparse_tensor_add(sparse_tensor, sparse_tensor_2)
Let sparse_multiply_result be Tensor.sparse_tensor_multiply(sparse_tensor, sparse_tensor_2)

Note: Sparse-dense tensor operations
Let dense_tensor_small be Tensor.create_random_tensor([3, 3, 3], "normal", 0.0, 1.0)
Let sparse_dense_add be Tensor.sparse_dense_tensor_add(sparse_tensor, dense_tensor_small)
```

## Machine Learning Tensor Operations

### Neural Network Primitives

```runa
Note: Convolution operations
Let input_tensor be Tensor.create_random_tensor([1, 3, 32, 32], "normal", 0.0, 1.0)  Note: NCHW format
Let conv_kernel be Tensor.create_random_tensor([16, 3, 5, 5], "normal", 0.0, 1.0)   Note: Output, Input, H, W

Let conv_result be Tensor.conv2d(
    input_tensor,
    conv_kernel,
    stride: [1, 1],
    padding: [2, 2],
    dilation: [1, 1]
)

Display "Convolution output shape: " joined with Tensor.shape_to_string(Tensor.get_shape(conv_result))

Note: Pooling operations
Let max_pool_result be Tensor.max_pool2d(
    conv_result,
    kernel_size: [2, 2],
    stride: [2, 2],
    padding: [0, 0]
)

Let avg_pool_result be Tensor.avg_pool2d(
    conv_result,
    kernel_size: [2, 2],
    stride: [2, 2],
    padding: [0, 0]
)

Display "Max pool output shape: " joined with Tensor.shape_to_string(Tensor.get_shape(max_pool_result))

Note: Batch normalization computation
Let batch_input be Tensor.create_random_tensor([32, 64, 28, 28], "normal", 0.0, 1.0)
Let running_mean be Tensor.create_zeros([64])
Let running_var be Tensor.create_ones([64])
Let gamma be Tensor.create_ones([64])
Let beta be Tensor.create_zeros([64])

Let batch_norm_result be Tensor.batch_norm2d(
    batch_input,
    running_mean,
    running_var,
    gamma,
    beta,
    eps: 1e-5,
    momentum: 0.1,
    training: True
)

Let normalized_output be Tensor.get_batch_norm_output(batch_norm_result)
Let updated_mean be Tensor.get_updated_running_mean(batch_norm_result)
Let updated_var be Tensor.get_updated_running_var(batch_norm_result)

Display "Batch norm output shape: " joined with Tensor.shape_to_string(Tensor.get_shape(normalized_output))
```

### Activation Functions and Losses

```runa
Note: Common activation functions
Let logits_tensor be Tensor.create_random_tensor([32, 10], "normal", 0.0, 2.0)

Let relu_activation be Tensor.relu(logits_tensor)
Let leaky_relu_activation be Tensor.leaky_relu(logits_tensor, negative_slope: 0.01)
Let gelu_activation be Tensor.gelu(logits_tensor)
Let swish_activation be Tensor.swish(logits_tensor, beta: 1.0)

Let sigmoid_activation be Tensor.sigmoid(logits_tensor)
Let tanh_activation be Tensor.tanh(logits_tensor)
Let softmax_activation be Tensor.softmax(logits_tensor, axis: 1)

Display "Softmax sum check: " joined with Tensor.tensor_sum_axis(softmax_activation, axis: 1)

Note: Loss function computations
Let predictions be Tensor.create_random_tensor([100, 10], "uniform", 0.0, 1.0)
Let targets_one_hot be Tensor.create_random_tensor([100, 10], "bernoulli", 0.1)
Let targets_sparse be Tensor.create_random_tensor([100], "uniform_int", 0, 9)

Let cross_entropy_loss be Tensor.cross_entropy_loss(predictions, targets_one_hot)
Let sparse_cross_entropy_loss be Tensor.sparse_cross_entropy_loss(predictions, targets_sparse)

Let mse_predictions be Tensor.create_random_tensor([50, 1], "normal", 0.0, 1.0)
let mse_targets be Tensor.create_random_tensor([50, 1], "normal", 0.0, 1.0)
Let mse_loss be Tensor.mse_loss(mse_predictions, mse_targets)

Display "Cross entropy loss: " joined with cross_entropy_loss
Display "Sparse cross entropy loss: " joined with sparse_cross_entropy_loss
Display "MSE loss: " joined with mse_loss

Note: Attention mechanisms
Let query_tensor be Tensor.create_random_tensor([32, 64, 512], "normal", 0.0, 1.0)  Note: Batch, Seq, Hidden
Let key_tensor be Tensor.create_random_tensor([32, 64, 512], "normal", 0.0, 1.0)
Let value_tensor be Tensor.create_random_tensor([32, 64, 512], "normal", 0.0, 1.0)

Let attention_scores be Tensor.scaled_dot_product_attention(
    query_tensor,
    key_tensor,
    value_tensor,
    scale_factor: Tensor.tensor_scalar(1.0 / LinAlg.sqrt(512.0))
)

Display "Attention output shape: " joined with Tensor.shape_to_string(Tensor.get_shape(attention_scores))

Note: Multi-head attention
Let num_heads be 8
Let head_dim be 64

Let multihead_attention_result be Tensor.multi_head_attention(
    query_tensor,
    key_tensor, 
    value_tensor,
    num_heads: num_heads,
    head_dim: head_dim
)

Display "Multi-head attention shape: " joined with 
    Tensor.shape_to_string(Tensor.get_shape(multihead_attention_result))
```

## Performance and Memory Optimization

### Memory-Efficient Operations

```runa
Note: In-place tensor operations
Let large_tensor be Tensor.create_random_tensor([1000, 1000], "normal", 0.0, 1.0)

Note: Before in-place operations, check memory usage
Let initial_memory be Tensor.get_memory_usage()

Tensor.tensor_add_inplace(large_tensor, 1.0)  Note: Add scalar in-place
Tensor.tensor_multiply_inplace(large_tensor, 0.5)  Note: Scale in-place
Tensor.tensor_clamp_inplace(large_tensor, -2.0, 2.0)  Note: Clamp in-place

Let after_inplace_memory be Tensor.get_memory_usage()
Display "Memory usage change: " joined with (after_inplace_memory - initial_memory) joined with " bytes"

Note: Memory-mapped tensors for large datasets
Let memory_mapped_tensor be Tensor.create_memory_mapped_tensor(
    "large_dataset.dat",
    shape: [10000, 1000],
    dtype: "float32"
)

Note: Lazy evaluation and computation graphs
Let computation_graph be Tensor.create_computation_graph()

Let node_a be Tensor.add_input_node(computation_graph, "input_a", shape: [100, 200])
Let node_b be Tensor.add_input_node(computation_graph, "input_b", shape: [100, 200])
Let node_sum be Tensor.add_operation_node(computation_graph, "add", [node_a, node_b])
Let node_result be Tensor.add_operation_node(computation_graph, "relu", [node_sum])

Note: Execute computation graph with actual data
Let input_data_a be Tensor.create_random_tensor([100, 200], "normal", 0.0, 1.0)
Let input_data_b be Tensor.create_random_tensor([100, 200], "normal", 0.0, 1.0)

Let graph_inputs be Tensor.create_input_dictionary([
    ("input_a", input_data_a),
    ("input_b", input_data_b)
])

Let graph_result be Tensor.execute_computation_graph(computation_graph, graph_inputs)
Display "Graph execution result shape: " joined with 
    Tensor.shape_to_string(Tensor.get_shape(graph_result))
```

### Parallel and GPU Acceleration

```runa
Note: Configure parallel tensor operations
Tensor.set_num_threads(8)
Tensor.enable_parallel_reductions(True)

Let large_tensor_parallel be Tensor.create_random_tensor([5000, 5000], "normal", 0.0, 1.0)

Note: Parallel reductions
Let start_time be Tensor.get_current_time()
Let parallel_sum be Tensor.tensor_sum(large_tensor_parallel)
Let parallel_time be Tensor.get_current_time() - start_time

Tensor.set_num_threads(1)
Let start_time_sequential be Tensor.get_current_time()
Let sequential_sum be Tensor.tensor_sum(large_tensor_parallel)
Let sequential_time be Tensor.get_current_time() - start_time_sequential

Let speedup be sequential_time / parallel_time
Display "Parallel speedup: " joined with speedup joined with "x"

Note: GPU tensor operations (if available)
If Tensor.gpu_available():
    Tensor.set_default_device("gpu")
    
    Let gpu_tensor_a be Tensor.create_random_tensor([2000, 2000], "normal", 0.0, 1.0)
    Let gpu_tensor_b be Tensor.create_random_tensor([2000, 2000], "normal", 0.0, 1.0)
    
    Let gpu_start_time be Tensor.get_current_time()
    Let gpu_matmul_result be Tensor.tensor_matmul(gpu_tensor_a, gpu_tensor_b)
    Let gpu_time be Tensor.get_current_time() - gpu_start_time
    
    Note: Compare with CPU performance
    Tensor.set_default_device("cpu")
    
    Let cpu_tensor_a be Tensor.to_device(gpu_tensor_a, "cpu")
    Let cpu_tensor_b be Tensor.to_device(gpu_tensor_b, "cpu")
    
    Let cpu_start_time be Tensor.get_current_time()
    Let cpu_matmul_result be Tensor.tensor_matmul(cpu_tensor_a, cpu_tensor_b)
    Let cpu_time be Tensor.get_current_time() - cpu_start_time
    
    Let gpu_speedup be cpu_time / gpu_time
    Display "GPU speedup for matrix multiplication: " joined with gpu_speedup joined with "x"

Note: Mixed precision computations
Tensor.enable_mixed_precision(True)
Tensor.set_mixed_precision_scale(1024.0)

Let mixed_precision_tensor be Tensor.create_random_tensor([1000, 1000], "float16")
Let fp32_computation = Tensor.tensor_matmul(
    Tensor.to_dtype(mixed_precision_tensor, "float32"),
    Tensor.to_dtype(mixed_precision_tensor, "float32")
)

Let result_fp16 be Tensor.to_dtype(fp32_computation, "float16")
```

## Integration Examples

### Scientific Computing Applications

```runa
Import "physics/simulation" as Physics
Import "math/differential_equations" as DE

Note: Finite difference methods using tensors
Let spatial_grid be Tensor.linspace(0.0, 1.0, 100)
Let time_grid be Tensor.linspace(0.0, 1.0, 200)

Let grid_x, grid_t be Tensor.meshgrid(spatial_grid, time_grid)

Note: Initial condition for heat equation
Let initial_temperature be Tensor.tensor_sin(
    Tensor.tensor_scalar_multiply(grid_x, Constants.get_pi())
)

Note: Finite difference operators as tensor operations
Let dx be 1.0 / 99.0
Let dt be 1.0 / 199.0
Let alpha be 0.01  Note: Thermal diffusivity

Let laplacian_kernel be Tensor.create_tensor_from_data([
    [0.0, 1.0, 0.0],
    [1.0, -4.0, 1.0],
    [0.0, 1.0, 0.0]
])

Let temperature_evolution be Physics.solve_heat_equation_tensor(
    initial_temperature,
    laplacian_kernel,
    alpha,
    dx,
    dt,
    time_steps: 200
)

Display "Temperature field shape: " joined with 
    Tensor.shape_to_string(Tensor.get_shape(temperature_evolution))

Note: Spectral methods using FFT
Let wave_initial be Tensor.tensor_exp(
    Tensor.tensor_scalar_multiply(
        Tensor.tensor_power(
            Tensor.tensor_subtract(grid_x, Tensor.tensor_scalar(0.5)),
            2
        ),
        -50.0
    )
)

Let fft_wave be Tensor.fft(wave_initial)
Let spectral_derivative be Tensor.spectral_derivative(fft_wave, dx)
Let ifft_derivative be Tensor.ifft(spectral_derivative)

Display "Spectral derivative computed via FFT"
```

### Machine Learning Model Implementation

```runa
Import "ml/models" as Models
Import "ml/optimization" as Optimization

Note: Simple neural network using tensors
Let input_data be Tensor.create_random_tensor([1000, 784], "normal", 0.0, 1.0)  Note: MNIST-like data
Let target_labels be Tensor.create_random_tensor([1000], "uniform_int", 0, 9)

Note: Network parameters
Let w1 be Tensor.create_random_tensor([784, 128], "normal", 0.0, 0.1)
Let b1 be Tensor.create_zeros([128])
Let w2 be Tensor.create_random_tensor([128, 64], "normal", 0.0, 0.1)
Let b2 be Tensor.create_zeros([64])
Let w3 be Tensor.create_random_tensor([64, 10], "normal", 0.0, 0.1)
Let b3 be Tensor.create_zeros([10])

Note: Forward pass
Let hidden1 be Tensor.relu(
    Tensor.tensor_add(
        Tensor.tensor_matmul(input_data, w1),
        b1
    )
)

Let hidden2 be Tensor.relu(
    Tensor.tensor_add(
        Tensor.tensor_matmul(hidden1, w2),
        b2
    )
)

Let logits be Tensor.tensor_add(
    Tensor.tensor_matmul(hidden2, w3),
    b3
)

Let predictions be Tensor.softmax(logits, axis: 1)

Note: Loss computation
Let loss be Tensor.sparse_cross_entropy_loss(predictions, target_labels)
Display "Initial loss: " joined with loss

Note: Gradient computation (simplified automatic differentiation)
Let gradients be Tensor.compute_gradients(loss, [w1, b1, w2, b2, w3, b3])

Let learning_rate be 0.001
For param_index from 0 to 5:
    Let param be LinAlg.get_element([w1, b1, w2, b2, w3, b3], param_index)
    Let grad be LinAlg.get_element(gradients, param_index)
    
    Tensor.tensor_subtract_inplace(
        param,
        Tensor.tensor_scalar_multiply(grad, learning_rate)
    )

Display "Parameter update completed"
```

### Computer Vision Applications

```runa
Import "vision/processing" as Vision

Note: Image tensor operations
Let image_batch be Tensor.create_random_tensor([32, 3, 224, 224], "uniform", 0.0, 1.0)  Note: Batch of RGB images

Note: Image normalization
Let mean_values be Tensor.create_tensor_from_data([0.485, 0.456, 0.406])  Note: ImageNet means
Let std_values be Tensor.create_tensor_from_data([0.229, 0.224, 0.225])   Note: ImageNet stds

Let normalized_images be Tensor.broadcast_divide(
    Tensor.broadcast_subtract(image_batch, mean_values),
    std_values
)

Note: Edge detection using convolution
Let sobel_x_kernel be Tensor.create_tensor_from_data([
    [[-1.0, 0.0, 1.0],
     [-2.0, 0.0, 2.0],
     [-1.0, 0.0, 1.0]]
])

Let sobel_y_kernel be Tensor.create_tensor_from_data([
    [[-1.0, -2.0, -1.0],
     [0.0,  0.0,  0.0],
     [1.0,  2.0,  1.0]]
])

Let edges_x be Tensor.conv2d(
    Tensor.tensor_mean_axis(normalized_images, axis: 1, keepdims: True),  Note: Convert to grayscale
    sobel_x_kernel,
    padding: [1, 1]
)

Let edges_y be Tensor.conv2d(
    Tensor.tensor_mean_axis(normalized_images, axis: 1, keepdims: True),
    sobel_y_kernel,
    padding: [1, 1]
)

Let edge_magnitude be Tensor.tensor_sqrt(
    Tensor.tensor_add(
        Tensor.tensor_power(edges_x, 2.0),
        Tensor.tensor_power(edges_y, 2.0)
    )
)

Display "Edge detection completed, output shape: " joined with 
    Tensor.shape_to_string(Tensor.get_shape(edge_magnitude))

Note: Feature pyramid construction
Let feature_pyramid_levels be []
Let current_features be normalized_images

For level from 0 to 3:
    LinAlg.append(feature_pyramid_levels, current_features)
    
    Let pooled_features be Tensor.avg_pool2d(
        current_features,
        kernel_size: [2, 2],
        stride: [2, 2]
    )
    
    Let current_features be pooled_features
    
    Display "Pyramid level " joined with level joined with " shape: " joined with 
        Tensor.shape_to_string(Tensor.get_shape(current_features))
```

## Best Practices and Optimization

### Memory Management

```runa
Note: Efficient memory usage patterns
Let tensor_memory_monitor be Tensor.create_memory_monitor()

Tensor.enable_memory_tracking(tensor_memory_monitor)

Let efficient_operations be Tensor.create_tensor([1000, 1000], "zeros")

Note: Prefer in-place operations when possible
Tensor.tensor_add_inplace(efficient_operations, 1.0)
Tensor.tensor_multiply_inplace(efficient_operations, 0.9)

Note: Use views instead of copies when possible
Let tensor_view be Tensor.create_view(efficient_operations, [500, 2000])
Let tensor_slice be Tensor.slice(efficient_operations, [100:900, 100:900])

Note: Clean up intermediate tensors
Tensor.deallocate_tensor(tensor_view)

Let memory_report be Tensor.get_memory_report(tensor_memory_monitor)
Display "Peak memory usage: " joined with Tensor.get_peak_memory_usage(memory_report) joined with " MB"
Display "Current memory usage: " joined with Tensor.get_current_memory_usage(memory_report) joined with " MB"
```

### Performance Optimization Guidelines

```runa
Note: Optimize tensor operations order
Let optimization_tensor_a be Tensor.create_random_tensor([100, 500], "normal", 0.0, 1.0)
Let optimization_tensor_b be Tensor.create_random_tensor([500, 200], "normal", 0.0, 1.0)
Let optimization_tensor_c be Tensor.create_random_tensor([200, 50], "normal", 0.0, 1.0)

Note: Efficient: (A @ B) @ C
Let efficient_result be Tensor.tensor_matmul(
    Tensor.tensor_matmul(optimization_tensor_a, optimization_tensor_b),
    optimization_tensor_c
)

Note: Less efficient: A @ (B @ C) for these shapes
Let less_efficient_result be Tensor.tensor_matmul(
    optimization_tensor_a,
    Tensor.tensor_matmul(optimization_tensor_b, optimization_tensor_c)
)

Note: Batch operations when possible
Let batch_vectors be Tensor.create_random_tensor([1000, 100], "normal", 0.0, 1.0)
Let transformation_matrix be Tensor.create_random_tensor([100, 50], "normal", 0.0, 1.0)

Let batch_transformed be Tensor.tensor_matmul(batch_vectors, transformation_matrix)

Note: Avoid unnecessary data type conversions
Tensor.set_default_dtype("float32")  Note: Use consistent precision
Let consistent_tensor be Tensor.create_random_tensor([500, 500], "normal", 0.0, 1.0)

Note: Profile tensor operations
Let profiler be Tensor.create_profiler()
Tensor.start_profiling(profiler)

Let profiled_operation be Tensor.tensor_matmul(consistent_tensor, consistent_tensor)

Tensor.stop_profiling(profiler)
Let profiling_report be Tensor.get_profiling_report(profiler)

Display "Operation time: " joined with Tensor.get_operation_time(profiling_report) joined with " ms"
Display "Memory bandwidth utilization: " joined with 
    Tensor.get_bandwidth_utilization(profiling_report) joined with "%"
```

<function_calls>
<invoke name="TodoWrite">
<parameter name="todos">[
  {
    "content": "Create comprehensive user documentation for math/engine/linalg module with 6 submodules and README",
    "status": "completed",
    "activeForm": "Creating comprehensive user documentation for math/engine/linalg module"
  }
]