# Numerical Differentiation

The Numerical Differentiation module (`math/engine/numerical/differentiation`) provides comprehensive algorithms for computing derivatives of functions numerically. This module implements finite difference methods, automatic differentiation (forward and reverse mode), symbolic differentiation, and specialized techniques for computing partial derivatives, gradients, and higher-order derivatives essential for optimization, scientific computing, and machine learning.

## Quick Start

```runa
Import "math/engine/numerical/differentiation" as Differentiation
Import "math/core/functions" as MathFunctions

Note: Define a test function
Process called "test_function" that takes x as Real returns Real:
    Return x * x * x + 2.0 * x * x - 5.0 * x + 1.0

Note: Exact derivative for comparison
Process called "exact_derivative" that takes x as Real returns Real:
    Return 3.0 * x * x + 4.0 * x - 5.0

Let test_point be 2.0

Note: Forward finite difference approximation
Let forward_diff be Differentiation.forward_difference(
    test_function,
    test_point,
    step_size: 1e-5
)

Note: Central finite difference approximation  
Let central_diff be Differentiation.central_difference(
    test_function,
    test_point,
    step_size: 1e-5
)

Note: Backward finite difference approximation
Let backward_diff be Differentiation.backward_difference(
    test_function,
    test_point,
    step_size: 1e-5
)

Let exact_value be exact_derivative(test_point)

Display "Derivative at x = " joined with test_point joined with ":"
Display "Forward difference: " joined with forward_diff joined with " (error: " 
    joined with Differentiation.abs(forward_diff - exact_value) joined with ")"
Display "Central difference: " joined with central_diff joined with " (error: " 
    joined with Differentiation.abs(central_diff - exact_value) joined with ")"
Display "Backward difference: " joined with backward_diff joined with " (error: " 
    joined with Differentiation.abs(backward_diff - exact_value) joined with ")"
Display "Exact value: " joined with exact_value

Note: Automatic differentiation (forward mode)
Let auto_diff_forward be Differentiation.automatic_differentiation_forward(
    test_function,
    test_point
)

Display "Automatic differentiation (forward): " joined with auto_diff_forward
    joined with " (error: " joined with Differentiation.abs(auto_diff_forward - exact_value) joined with ")"

Note: Richardson extrapolation for improved accuracy
Let richardson_diff be Differentiation.richardson_extrapolation_derivative(
    test_function,
    test_point,
    base_step_size: 1e-3,
    extrapolation_levels: 3
)

Display "Richardson extrapolation: " joined with richardson_diff
    joined with " (error: " joined with Differentiation.abs(richardson_diff - exact_value) joined with ")"
```

## Finite Difference Methods

### Basic Finite Difference Formulas

```runa
Note: Compare different finite difference orders
Let fd_test_point be 1.5
Let step_sizes be [1e-2, 1e-3, 1e-4, 1e-5, 1e-6]

Display "Finite difference accuracy analysis:"
Display "Step size | Forward | Central | Backward | Exact: " joined with exact_derivative(fd_test_point)

For h in step_sizes:
    Let forward_fd be Differentiation.forward_difference(test_function, fd_test_point, h)
    Let central_fd be Differentiation.central_difference(test_function, fd_test_point, h)  
    Let backward_fd be Differentiation.backward_difference(test_function, fd_test_point, h)
    
    Display h joined with " | " joined with forward_fd joined with " | " 
        joined with central_fd joined with " | " joined with backward_fd

Note: Higher-order finite difference formulas
Let high_order_forward be Differentiation.forward_difference_high_order(
    test_function,
    fd_test_point,
    step_size: 1e-4,
    order: 4
)

Let high_order_central be Differentiation.central_difference_high_order(
    test_function,
    fd_test_point,
    step_size: 1e-4,
    order: 4
)

Display "High-order finite differences:"
Display "4th-order forward: " joined with high_order_forward
Display "4th-order central: " joined with high_order_central

Note: Adaptive step size selection
Let adaptive_diff be Differentiation.adaptive_finite_difference(
    test_function,
    fd_test_point,
    target_accuracy: 1e-10,
    initial_step: 1e-3
)

Let final_step_size be Differentiation.get_final_step_size(adaptive_diff)
Let adaptive_derivative be Differentiation.get_derivative_value(adaptive_diff)
Let estimated_error be Differentiation.get_estimated_error(adaptive_diff)

Display "Adaptive finite difference:"
Display "Final step size: " joined with final_step_size
Display "Derivative: " joined with adaptive_derivative
Display "Estimated error: " joined with estimated_error
```

### Complex Step Differentiation

```runa
Note: Complex step method for high accuracy
Let complex_step_diff be Differentiation.complex_step_derivative(
    test_function,
    fd_test_point,
    imaginary_step: 1e-20
)

Display "Complex step derivative: " joined with complex_step_diff
Display "Complex step error: " joined with 
    Differentiation.abs(complex_step_diff - exact_derivative(fd_test_point))

Note: Complex step vs finite difference comparison
Let comparison_function_name be "exponential"

Process called "exponential_function" that takes x as Real returns Real:
    Return MathFunctions.exp(x)

Process called "exponential_derivative" that takes x as Real returns Real:
    Return MathFunctions.exp(x)

Let comparison_point be 0.5
Let fd_comparison be Differentiation.central_difference(
    exponential_function,
    comparison_point,
    step_size: 1e-8
)

Let complex_comparison be Differentiation.complex_step_derivative(
    exponential_function,
    comparison_point,
    imaginary_step: 1e-30
)

Let exact_exp_deriv be exponential_derivative(comparison_point)

Display "Exponential derivative comparison at x = " joined with comparison_point joined with ":"
Display "Finite difference: " joined with fd_comparison 
    joined with " (error: " joined with Differentiation.abs(fd_comparison - exact_exp_deriv) joined with ")"
Display "Complex step: " joined with complex_comparison
    joined with " (error: " joined with Differentiation.abs(complex_comparison - exact_exp_deriv) joined with ")"
Display "Exact: " joined with exact_exp_deriv

Note: Complex step for functions with noise
Process called "noisy_function" that takes x as Real returns Real:
    Let clean_value be MathFunctions.sin(x)
    Let noise be 1e-10 * Differentiation.random_normal(0.0, 1.0)
    Return clean_value + noise

Let noisy_fd be Differentiation.central_difference(noisy_function, comparison_point, 1e-6)
Let noisy_complex be Differentiation.complex_step_derivative(noisy_function, comparison_point, 1e-20)
Let true_derivative be MathFunctions.cos(comparison_point)

Display "Noisy function derivative comparison:"
Display "Finite difference: " joined with noisy_fd
    joined with " (error: " joined with Differentiation.abs(noisy_fd - true_derivative) joined with ")"
Display "Complex step: " joined with noisy_complex
    joined with " (error: " joined with Differentiation.abs(noisy_complex - true_derivative) joined with ")"
```

### Multi-Point Stencils

```runa
Note: Generate optimal finite difference stencils
Let stencil_3_point be Differentiation.generate_fd_stencil(
    stencil_points: [-1, 0, 1],
    derivative_order: 1,
    approximation_order: 2
)

Let stencil_5_point be Differentiation.generate_fd_stencil(
    stencil_points: [-2, -1, 0, 1, 2],
    derivative_order: 1,
    approximation_order: 4
)

Display "3-point stencil coefficients: " joined with 
    Differentiation.format_stencil_coefficients(stencil_3_point)
Display "5-point stencil coefficients: " joined with
    Differentiation.format_stencil_coefficients(stencil_5_point)

Note: Apply custom stencils
Let custom_stencil_result be Differentiation.apply_stencil(
    test_function,
    stencil_5_point,
    center_point: fd_test_point,
    step_size: 1e-4
)

Display "5-point stencil result: " joined with custom_stencil_result

Note: Non-uniform grid stencils
Let irregular_points be [0.0, 0.1, 0.3, 0.7, 1.0, 1.5]
Let irregular_stencil be Differentiation.generate_irregular_stencil(
    grid_points: irregular_points,
    evaluation_point: 0.7,
    derivative_order: 1
)

Let irregular_function_values be []
For point in irregular_points:
    Let value be test_function(point)
    Differentiation.append_to_vector(irregular_function_values, value)

Let irregular_derivative be Differentiation.apply_irregular_stencil(
    irregular_stencil,
    irregular_function_values
)

Display "Irregular grid derivative at x=0.7: " joined with irregular_derivative
Display "Exact derivative at x=0.7: " joined with exact_derivative(0.7)
```

## Higher-Order Derivatives

### Second and Higher Derivatives

```runa
Note: Second derivative approximations
Process called "second_derivative_exact" that takes x as Real returns Real:
    Return 6.0 * x + 4.0  Note: Second derivative of our test function

Let second_deriv_central be Differentiation.second_derivative_central(
    test_function,
    fd_test_point,
    step_size: 1e-4
)

Let second_deriv_exact_val be second_derivative_exact(fd_test_point)

Display "Second derivative at x = " joined with fd_test_point joined with ":"
Display "Central difference: " joined with second_deriv_central
Display "Exact: " joined with second_deriv_exact_val  
Display "Error: " joined with Differentiation.abs(second_deriv_central - second_deriv_exact_val)

Note: Higher-order derivatives using recursive differentiation
Let third_derivative be Differentiation.higher_order_derivative(
    test_function,
    fd_test_point,
    derivative_order: 3,
    step_size: 1e-3,
    method: "central"
)

Let fourth_derivative be Differentiation.higher_order_derivative(
    test_function,
    fd_test_point,
    derivative_order: 4,
    step_size: 1e-3,
    method: "central"
)

Display "Third derivative: " joined with third_derivative joined with " (exact: 6.0)"
Display "Fourth derivative: " joined with fourth_derivative joined with " (exact: 0.0)"

Note: Taylor series method for higher derivatives
Let taylor_derivatives be Differentiation.taylor_series_derivatives(
    test_function,
    fd_test_point,
    max_order: 5,
    step_size: 1e-4
)

Display "Taylor series derivatives:"
For order from 1 to 5:
    Let derivative_val be Differentiation.get_taylor_derivative(taylor_derivatives, order)
    Display "Order " joined with order joined with ": " joined with derivative_val

Note: Complex step for second derivatives
Let complex_second_derivative be Differentiation.complex_step_second_derivative(
    test_function,
    fd_test_point,
    real_step: 1e-5,
    imaginary_step: 1e-20
)

Display "Complex step second derivative: " joined with complex_second_derivative
Display "Complex step second derivative error: " joined with 
    Differentiation.abs(complex_second_derivative - second_deriv_exact_val)
```

### Derivative Arrays and Tensors

```runa
Import "math/engine/linalg/core" as LinAlg

Note: Compute derivatives at multiple points efficiently
Let derivative_points be [0.5, 1.0, 1.5, 2.0, 2.5]
Let derivative_array be Differentiation.compute_derivative_array(
    test_function,
    derivative_points,
    step_size: 1e-5,
    method: "central"
)

Display "Derivative array:"
For i from 0 to (LinAlg.vector_length(derivative_points) - 1):
    Let point be LinAlg.get_element(derivative_points, i)
    Let deriv be LinAlg.get_element(derivative_array, i)
    Let exact be exact_derivative(point)
    Display "f'(" joined with point joined with ") = " joined with deriv 
        joined with " (exact: " joined with exact joined with ")"

Note: Hessian matrix computation for multivariate functions
Process called "multivariate_function" that takes variables as Vector returns Real:
    Let x be LinAlg.get_element(variables, 0)
    Let y be LinAlg.get_element(variables, 1)
    Return x * x * x + 2.0 * x * y * y - 3.0 * y * y * y

Let test_point_2d be LinAlg.create_vector([1.0, 2.0])

Let hessian_matrix be Differentiation.compute_hessian_matrix(
    multivariate_function,
    test_point_2d,
    step_size: 1e-5
)

Display "Hessian matrix at (1.0, 2.0):"
Display LinAlg.matrix_to_string(hessian_matrix)

Note: Exact Hessian for comparison
Let exact_hessian be LinAlg.create_matrix([
    [6.0, 8.0],      Note: ∂²f/∂x² = 6x, ∂²f/∂x∂y = 4y at (1,2)
    [8.0, -14.0]     Note: ∂²f/∂y∂x = 4y, ∂²f/∂y² = 4x - 18y at (1,2)
])

Display "Exact Hessian:"
Display LinAlg.matrix_to_string(exact_hessian)

Let hessian_error be LinAlg.matrix_norm(
    LinAlg.matrix_subtract(hessian_matrix, exact_hessian),
    "frobenius"
)

Display "Hessian approximation error (Frobenius norm): " joined with hessian_error
```

## Automatic Differentiation

### Forward Mode Automatic Differentiation

```runa
Note: Forward mode AD for single variable
Let ad_forward_system be Differentiation.create_forward_ad_system()

Note: Compute f(x) = x³ + 2x² - 5x + 1 and its derivative simultaneously
Let ad_input be Differentiation.create_ad_variable(2.0, 1.0)  Note: Value=2.0, derivative=1.0

Let ad_x_cubed be Differentiation.ad_power(ad_input, 3)
Let ad_2x_squared be Differentiation.ad_multiply(
    Differentiation.create_ad_constant(2.0),
    Differentiation.ad_power(ad_input, 2)
)
Let ad_5x be Differentiation.ad_multiply(
    Differentiation.create_ad_constant(5.0),
    ad_input
)
Let ad_constant be Differentiation.create_ad_constant(1.0)

Let ad_result be Differentiation.ad_add(
    Differentiation.ad_subtract(
        Differentiation.ad_add(ad_x_cubed, ad_2x_squared),
        ad_5x
    ),
    ad_constant
)

Let ad_function_value be Differentiation.get_ad_value(ad_result)
Let ad_derivative_value be Differentiation.get_ad_derivative(ad_result)

Display "Forward mode AD results:"
Display "Function value: " joined with ad_function_value joined with " (exact: " 
    joined with test_function(2.0) joined with ")"
Display "Derivative value: " joined with ad_derivative_value joined with " (exact: "
    joined with exact_derivative(2.0) joined with ")"

Note: Forward mode for multivariate functions
Process called "multivariate_ad_function" that takes x as ADVariable, y as ADVariable returns ADVariable:
    Let x_squared be Differentiation.ad_power(x, 2)
    Let y_squared be Differentiation.ad_power(y, 2) 
    Let xy be Differentiation.ad_multiply(x, y)
    Return Differentiation.ad_add(x_squared, Differentiation.ad_add(y_squared, xy))

Note: Compute partial derivatives
Let ad_x_input be Differentiation.create_ad_variable(3.0, 1.0)  Note: ∂/∂x
Let ad_y_input be Differentiation.create_ad_variable(4.0, 0.0)
Let partial_x_result be multivariate_ad_function(ad_x_input, ad_y_input)

Let ad_x_input_2 be Differentiation.create_ad_variable(3.0, 0.0)
Let ad_y_input_2 be Differentiation.create_ad_variable(4.0, 1.0)  Note: ∂/∂y
Let partial_y_result be multivariate_ad_function(ad_x_input_2, ad_y_input_2)

Display "Partial derivatives of f(x,y) = x² + y² + xy at (3,4):"
Display "∂f/∂x = " joined with Differentiation.get_ad_derivative(partial_x_result)
    joined with " (exact: " joined with (2.0 * 3.0 + 4.0) joined with ")"
Display "∂f/∂y = " joined with Differentiation.get_ad_derivative(partial_y_result)
    joined with " (exact: " joined with (2.0 * 4.0 + 3.0) joined with ")"
```

### Reverse Mode Automatic Differentiation

```runa
Note: Reverse mode AD (backpropagation)
Let reverse_ad_system be Differentiation.create_reverse_ad_system()

Note: Forward pass - build computational graph
Let rev_x be Differentiation.create_reverse_variable(2.0)
Let rev_y be Differentiation.create_reverse_variable(3.0)

Let rev_x_squared be Differentiation.reverse_multiply(rev_x, rev_x)
Let rev_y_cubed be Differentiation.reverse_multiply(
    Differentiation.reverse_multiply(rev_y, rev_y), 
    rev_y
)
Let rev_xy be Differentiation.reverse_multiply(rev_x, rev_y)
Let rev_result be Differentiation.reverse_add(
    rev_x_squared,
    Differentiation.reverse_add(rev_y_cubed, rev_xy)
)

Note: Backward pass - compute all derivatives
Differentiation.reverse_backward_pass(rev_result)

Let reverse_df_dx be Differentiation.get_reverse_gradient(rev_x)
Let reverse_df_dy be Differentiation.get_reverse_gradient(rev_y)

Display "Reverse mode AD results for f(x,y) = x² + y³ + xy at (2,3):"
Display "∂f/∂x = " joined with reverse_df_dx joined with " (exact: " 
    joined with (2.0 * 2.0 + 3.0) joined with ")"
Display "∂f/∂y = " joined with reverse_df_dy joined with " (exact: "
    joined with (3.0 * 3.0 * 3.0 + 2.0) joined with ")"

Note: Reverse mode efficiency for functions with many inputs
Let high_dimensional_inputs be []
For i from 0 to 99:
    Let input_val be i / 99.0
    Let reverse_var be Differentiation.create_reverse_variable(input_val)
    Differentiation.append_to_list(high_dimensional_inputs, reverse_var)

Note: Sum of squares function: f(x₁,...,x₁₀₀) = Σᵢ xᵢ²
Let sum_of_squares_result be Differentiation.create_reverse_constant(0.0)
For rev_input in high_dimensional_inputs:
    Let input_squared be Differentiation.reverse_multiply(rev_input, rev_input)
    Let sum_of_squares_result be Differentiation.reverse_add(sum_of_squares_result, input_squared)

Differentiation.reverse_backward_pass(sum_of_squares_result)

Display "Reverse mode gradient for 100-dimensional sum of squares:"
Display "∇f[0] = " joined with Differentiation.get_reverse_gradient(
    Differentiation.get_list_element(high_dimensional_inputs, 0))
Display "∇f[50] = " joined with Differentiation.get_reverse_gradient(
    Differentiation.get_list_element(high_dimensional_inputs, 50))
Display "∇f[99] = " joined with Differentiation.get_reverse_gradient(
    Differentiation.get_list_element(high_dimensional_inputs, 99))
```

### Higher-Order Automatic Differentiation

```runa
Note: Second-order forward mode AD
Let second_order_ad_input be Differentiation.create_second_order_ad_variable(
    value: 2.0,
    first_derivative: 1.0,
    second_derivative: 0.0
)

Note: Compute f(x) = x⁴ and its first and second derivatives
Let ad_x_fourth be Differentiation.second_order_ad_power(second_order_ad_input, 4)

Let so_function_value be Differentiation.get_second_order_value(ad_x_fourth)
Let so_first_derivative be Differentiation.get_second_order_first_derivative(ad_x_fourth)
Let so_second_derivative be Differentiation.get_second_order_second_derivative(ad_x_fourth)

Display "Second-order AD for f(x) = x⁴ at x = 2:"
Display "f(x) = " joined with so_function_value joined with " (exact: " 
    joined with (2.0 * 2.0 * 2.0 * 2.0) joined with ")"
Display "f'(x) = " joined with so_first_derivative joined with " (exact: "
    joined with (4.0 * 2.0 * 2.0 * 2.0) joined with ")"
Display "f''(x) = " joined with so_second_derivative joined with " (exact: "
    joined with (12.0 * 2.0 * 2.0) joined with ")"

Note: Mixed partial derivatives using forward-over-reverse mode
Process called "mixed_partial_function" that takes x as Real, y as Real returns Real:
    Return MathFunctions.sin(x * y) + x * x * y

Let mixed_partial_point_x be 1.0
Let mixed_partial_point_y be 2.0

Let mixed_partial_result be Differentiation.compute_mixed_partial_derivatives(
    mixed_partial_function,
    point: [mixed_partial_point_x, mixed_partial_point_y],
    max_order: 2
)

Display "Mixed partial derivatives of f(x,y) = sin(xy) + x²y at (1,2):"
Display "∂f/∂x = " joined with Differentiation.get_mixed_partial(mixed_partial_result, [1, 0])
Display "∂f/∂y = " joined with Differentiation.get_mixed_partial(mixed_partial_result, [0, 1])
Display "∂²f/∂x∂y = " joined with Differentiation.get_mixed_partial(mixed_partial_result, [1, 1])
Display "∂²f/∂x² = " joined with Differentiation.get_mixed_partial(mixed_partial_result, [2, 0])
Display "∂²f/∂y² = " joined with Differentiation.get_mixed_partial(mixed_partial_result, [0, 2])
```

## Partial Derivatives and Gradients

### Gradient Computation

```runa
Note: Gradient computation using finite differences
Process called "gradient_test_function" that takes variables as Vector returns Real:
    Let x be LinAlg.get_element(variables, 0)
    Let y be LinAlg.get_element(variables, 1)
    Let z be LinAlg.get_element(variables, 2)
    Return x * x + 2.0 * y * y + 3.0 * z * z + x * y + y * z

Let gradient_test_point be LinAlg.create_vector([1.0, 2.0, 3.0])

Let finite_diff_gradient be Differentiation.finite_difference_gradient(
    gradient_test_function,
    gradient_test_point,
    step_size: 1e-6
)

Display "Finite difference gradient at (1, 2, 3):"
Display LinAlg.vector_to_string(finite_diff_gradient)

Note: Exact gradient for comparison
Let exact_gradient be LinAlg.create_vector([
    2.0 * 1.0 + 2.0,        Note: ∂f/∂x = 2x + y
    4.0 * 2.0 + 1.0 + 3.0,  Note: ∂f/∂y = 4y + x + z  
    6.0 * 3.0 + 2.0         Note: ∂f/∂z = 6z + y
])

Display "Exact gradient:"
Display LinAlg.vector_to_string(exact_gradient)

Let gradient_error be LinAlg.vector_norm(
    LinAlg.vector_subtract(finite_diff_gradient, exact_gradient),
    "euclidean"
)
Display "Gradient error (Euclidean norm): " joined with gradient_error

Note: Gradient using automatic differentiation
Let ad_gradient be Differentiation.automatic_differentiation_gradient(
    gradient_test_function,
    gradient_test_point
)

Display "AD gradient:"
Display LinAlg.vector_to_string(ad_gradient)

Let ad_gradient_error be LinAlg.vector_norm(
    LinAlg.vector_subtract(ad_gradient, exact_gradient),
    "euclidean"
)
Display "AD gradient error: " joined with ad_gradient_error
```

### Jacobian Matrices

```runa
Note: Jacobian matrix computation
Process called "vector_function" that takes variables as Vector returns Vector:
    Let x be LinAlg.get_element(variables, 0)
    Let y be LinAlg.get_element(variables, 1)
    
    Let f1 be x * x + y * y
    Let f2 be x * y - 2.0 * x
    Let f3 be MathFunctions.sin(x) + MathFunctions.cos(y)
    
    Return LinAlg.create_vector([f1, f2, f3])

Let jacobian_test_point be LinAlg.create_vector([1.5, 2.5])

Let jacobian_matrix be Differentiation.compute_jacobian_matrix(
    vector_function,
    jacobian_test_point,
    step_size: 1e-7
)

Display "Jacobian matrix at (1.5, 2.5):"
Display LinAlg.matrix_to_string(jacobian_matrix)

Note: Exact Jacobian for verification
Let exact_jacobian be LinAlg.create_matrix([
    [2.0 * 1.5, 2.0 * 2.5],                    Note: [∂f₁/∂x, ∂f₁/∂y]
    [2.5 - 2.0, 1.5],                          Note: [∂f₂/∂x, ∂f₂/∂y]
    [MathFunctions.cos(1.5), -MathFunctions.sin(2.5)]  Note: [∂f₃/∂x, ∂f₃/∂y]
])

Display "Exact Jacobian:"
Display LinAlg.matrix_to_string(exact_jacobian)

Let jacobian_error be LinAlg.matrix_norm(
    LinAlg.matrix_subtract(jacobian_matrix, exact_jacobian),
    "frobenius"
)
Display "Jacobian error (Frobenius norm): " joined with jacobian_error

Note: Sparse Jacobian computation for large systems
Let sparse_jacobian_pattern be Differentiation.detect_jacobian_sparsity_pattern(
    vector_function,
    jacobian_test_point,
    sparsity_threshold: 1e-10
)

Let sparse_jacobian be Differentiation.compute_sparse_jacobian(
    vector_function,
    jacobian_test_point,
    sparsity_pattern: sparse_jacobian_pattern,
    method: "forward_mode_coloring"
)

Display "Sparse Jacobian computation completed"
Display "Sparsity ratio: " joined with Differentiation.get_sparsity_ratio(sparse_jacobian_pattern)
```

### Directional Derivatives

```runa
Note: Directional derivatives and gradients
Let direction_vector be LinAlg.create_vector([0.6, 0.8])  Note: Unit vector
Let normalized_direction be LinAlg.normalize_vector(direction_vector)

Let directional_derivative be Differentiation.directional_derivative(
    gradient_test_function,
    gradient_test_point,
    normalized_direction,
    step_size: 1e-6
)

Display "Directional derivative in direction (" joined with 
    LinAlg.get_element(normalized_direction, 0) joined with ", " joined with
    LinAlg.get_element(normalized_direction, 1) joined with ", " joined with
    LinAlg.get_element(normalized_direction, 2) joined with "):"
Display directional_derivative

Note: Verify using gradient dot product
Let computed_gradient be finite_diff_gradient
Let directional_from_gradient be LinAlg.dot_product(
    computed_gradient,
    LinAlg.create_vector([
        LinAlg.get_element(normalized_direction, 0),
        LinAlg.get_element(normalized_direction, 1),
        0.0  Note: Extend to 3D
    ])
)

Display "Directional derivative from gradient dot product: " joined with directional_from_gradient
Display "Difference: " joined with Differentiation.abs(directional_derivative - directional_from_gradient)

Note: Maximum directional derivative (steepest ascent)
Let steepest_ascent_direction be LinAlg.normalize_vector(computed_gradient)
Let max_directional_derivative be LinAlg.vector_norm(computed_gradient, "euclidean")

Display "Steepest ascent direction: " joined with LinAlg.vector_to_string(steepest_ascent_direction)
Display "Maximum directional derivative: " joined with max_directional_derivative
```

## Sensitivity Analysis

### Parameter Sensitivity

```runa
Note: Sensitivity analysis for parametric functions
Process called "parametric_function" that takes x as Real, parameters as Vector returns Real:
    Let a be LinAlg.get_element(parameters, 0)
    Let b be LinAlg.get_element(parameters, 1)
    Let c be LinAlg.get_element(parameters, 2)
    Return a * x * x + b * x + c

Let nominal_parameters be LinAlg.create_vector([2.0, -1.0, 3.0])
Let evaluation_point be 1.5

Let sensitivity_matrix be Differentiation.parameter_sensitivity_analysis(
    parametric_function,
    evaluation_point,
    nominal_parameters,
    parameter_perturbations: [0.01, 0.01, 0.01]
)

Display "Parameter sensitivity at x = " joined with evaluation_point joined with ":"
For i from 0 to 2:
    Let sensitivity be LinAlg.get_element(sensitivity_matrix, i)
    Display "∂f/∂p" joined with i joined with " = " joined with sensitivity

Note: Uncertainty propagation through derivatives
Let parameter_uncertainties be LinAlg.create_vector([0.1, 0.05, 0.2])
Let sensitivity_vector be sensitivity_matrix

Let output_uncertainty be Differentiation.propagate_uncertainty(
    sensitivity_vector,
    parameter_uncertainties,
    correlation_matrix: LinAlg.create_identity_matrix(3)  Note: Uncorrelated parameters
)

Display "Output uncertainty (1-sigma): ± " joined with output_uncertainty

Note: Global sensitivity analysis using Sobol indices
Let sobol_analysis be Differentiation.sobol_sensitivity_analysis(
    parametric_function,
    evaluation_point,
    parameter_ranges: [
        [1.0, 3.0],   Note: Range for parameter a
        [-2.0, 0.0],  Note: Range for parameter b  
        [2.0, 4.0]    Note: Range for parameter c
    ],
    num_samples: 10000
)

Let first_order_indices be Differentiation.get_first_order_sobol_indices(sobol_analysis)
Let total_effect_indices be Differentiation.get_total_effect_indices(sobol_analysis)

Display "Sobol sensitivity indices:"
For i from 0 to 2:
    Let first_order be LinAlg.get_element(first_order_indices, i)
    Let total_effect be LinAlg.get_element(total_effect_indices, i)
    Display "Parameter " joined with i joined with ": S₁ = " joined with first_order
        joined with ", Sᵀ = " joined with total_effect
```

### Adjoint Sensitivity Method

```runa
Import "math/engine/numerical/ode" as ODE

Note: Adjoint sensitivity for ODE systems
Process called "ode_system_with_parameters" that takes t as Real, y as Vector, parameters as Vector returns Vector:
    Let y1 be LinAlg.get_element(y, 0)
    Let y2 be LinAlg.get_element(y, 1)
    Let k1 be LinAlg.get_element(parameters, 0)
    Let k2 be LinAlg.get_element(parameters, 1)
    
    Let dy1dt be -k1 * y1
    Let dy2dt be k1 * y1 - k2 * y2
    
    Return LinAlg.create_vector([dy1dt, dy2dt])

Process called "output_function" that takes y as Vector returns Real:
    Return LinAlg.get_element(y, 1)  Note: Interested in y₂(T)

Let ode_parameters be LinAlg.create_vector([0.5, 0.2])
Let initial_conditions be LinAlg.create_vector([10.0, 0.0])
Let time_span be [0.0, 10.0]

Let adjoint_sensitivity be Differentiation.adjoint_sensitivity_ode(
    ode_system_with_parameters,
    output_function,
    time_span,
    initial_conditions,
    ode_parameters
)

Let parameter_sensitivities be Differentiation.get_adjoint_sensitivities(adjoint_sensitivity)

Display "Adjoint sensitivities of y₂(T=10) with respect to parameters:"
Display "∂y₂(T)/∂k₁ = " joined with LinAlg.get_element(parameter_sensitivities, 0)
Display "∂y₂(T)/∂k₂ = " joined with LinAlg.get_element(parameter_sensitivities, 1)

Note: Compare with finite difference sensitivities
Let fd_sensitivity_k1 be Differentiation.finite_difference_parameter_sensitivity(
    ode_system_with_parameters,
    output_function,
    time_span,
    initial_conditions,
    ode_parameters,
    parameter_index: 0,
    step_size: 1e-6
)

Let fd_sensitivity_k2 be Differentiation.finite_difference_parameter_sensitivity(
    ode_system_with_parameters,
    output_function,
    time_span,
    initial_conditions,
    ode_parameters,
    parameter_index: 1,
    step_size: 1e-6
)

Display "Finite difference sensitivities:"
Display "∂y₂(T)/∂k₁ = " joined with fd_sensitivity_k1
Display "∂y₂(T)/∂k₂ = " joined with fd_sensitivity_k2

Display "Adjoint vs FD sensitivity differences:"
Display "Δ(∂y₂/∂k₁) = " joined with Differentiation.abs(
    LinAlg.get_element(parameter_sensitivities, 0) - fd_sensitivity_k1)
Display "Δ(∂y₂/∂k₂) = " joined with Differentiation.abs(
    LinAlg.get_element(parameter_sensitivities, 1) - fd_sensitivity_k2)
```

## Error Analysis and Optimization

### Truncation and Round-off Error Analysis

```runa
Note: Analyze finite difference truncation errors
Let truncation_analysis be Differentiation.analyze_truncation_error(
    test_function,
    exact_derivative,
    test_point: 1.0,
    step_sizes: [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8],
    methods: ["forward", "central", "backward"]
)

Display "Truncation error analysis:"
Let optimal_step_sizes be Differentiation.get_optimal_step_sizes(truncation_analysis)

For method in ["forward", "central", "backward"]:
    Let optimal_step be Differentiation.get_optimal_step_for_method(optimal_step_sizes, method)
    Let optimal_error be Differentiation.get_optimal_error_for_method(truncation_analysis, method)
    
    Display method joined with " difference:"
    Display "  Optimal step size: " joined with optimal_step
    Display "  Minimum error: " joined with optimal_error

Note: Machine precision effects
Let machine_precision_analysis be Differentiation.machine_precision_error_analysis(
    test_function,
    test_point: 1.0,
    step_range: [1e-16, 1e-1],
    num_steps: 50
)

Let step_size_recommendation be Differentiation.recommend_step_size(machine_precision_analysis)
Display "Recommended step size considering machine precision: " joined with step_size_recommendation

Note: Condition number analysis for differentiation
Let differentiation_condition_number be Differentiation.compute_differentiation_condition_number(
    test_function,
    test_point: 1.0,
    step_size: step_size_recommendation
)

Display "Differentiation condition number: " joined with differentiation_condition_number

If differentiation_condition_number > 1e10:
    Display "Warning: Differentiation is ill-conditioned"
    Display "Consider using higher-precision arithmetic or alternative methods"
```

### Adaptive Step Size Selection

```runa
Note: Richardson extrapolation with adaptive refinement
Let richardson_adaptive be Differentiation.richardson_extrapolation_adaptive(
    test_function,
    test_point: 2.0,
    initial_step: 1e-2,
    target_accuracy: 1e-12,
    max_levels: 6
)

Let richardson_result be Differentiation.get_richardson_result(richardson_adaptive)
Let richardson_error_estimate be Differentiation.get_richardson_error_estimate(richardson_adaptive)
Let richardson_levels_used be Differentiation.get_richardson_levels_used(richardson_adaptive)

Display "Richardson extrapolation results:"
Display "Derivative estimate: " joined with richardson_result
Display "Error estimate: " joined with richardson_error_estimate
Display "Extrapolation levels used: " joined with richardson_levels_used

Note: Adaptive step size with error control
Let adaptive_step_controller be Differentiation.create_adaptive_step_controller([
    ("initial_step", 1e-3),
    ("min_step", 1e-15),
    ("max_step", 1e-1),
    ("safety_factor", 0.9),
    ("step_increase_factor", 2.0),
    ("step_decrease_factor", 0.5)
])

Let controlled_derivative be Differentiation.adaptive_step_differentiation(
    test_function,
    test_point: 1.5,
    target_tolerance: 1e-10,
    step_controller: adaptive_step_controller
)

Let final_step_used be Differentiation.get_final_step_size(controlled_derivative)
Let achieved_accuracy be Differentiation.get_achieved_accuracy(controlled_derivative)
Let step_adjustments be Differentiation.get_step_adjustment_count(controlled_derivative)

Display "Adaptive step size results:"
Display "Final step size: " joined with final_step_used
Display "Achieved accuracy: " joined with achieved_accuracy  
Display "Number of step adjustments: " joined with step_adjustments
```

### Parallel and High-Performance Differentiation

```runa
Note: Parallel gradient computation
Let large_dimension_function_parallel be LinAlg.create_random_quadratic_function(100)
Let large_test_point be LinAlg.create_random_vector(100, "normal", 0.0, 1.0)

Let parallel_gradient be Differentiation.compute_gradient_parallel(
    large_dimension_function_parallel,
    large_test_point,
    step_size: 1e-6,
    num_threads: 8
)

Let sequential_start_time be Differentiation.get_current_time()
Let sequential_gradient be Differentiation.finite_difference_gradient(
    large_dimension_function_parallel,
    large_test_point,
    step_size: 1e-6
)
Let sequential_time be Differentiation.get_current_time() - sequential_start_time

Let parallel_start_time be Differentiation.get_current_time()
Let parallel_result be parallel_gradient
Let parallel_time be Differentiation.get_current_time() - parallel_start_time

Let speedup be sequential_time / parallel_time
Display "Parallel gradient computation:"
Display "Sequential time: " joined with sequential_time joined with " seconds"
Display "Parallel time: " joined with parallel_time joined with " seconds"
Display "Speedup: " joined with speedup joined with "x"

Note: GPU-accelerated automatic differentiation
If Differentiation.gpu_available():
    Differentiation.set_device("gpu")
    
    Let gpu_gradient_start = Differentiation.get_current_time()
    Let gpu_gradient be Differentiation.compute_gradient_gpu(
        large_dimension_function_parallel,
        large_test_point,
        method: "forward_mode_ad"
    )
    Let gpu_time be Differentiation.get_current_time() - gpu_gradient_start
    
    Let gpu_speedup be sequential_time / gpu_time
    Display "GPU acceleration:"
    Display "GPU time: " joined with gpu_time joined with " seconds"
    Display "GPU speedup: " joined with gpu_speedup joined with "x"
    
    Differentiation.set_device("cpu")
```

## Integration Examples

### With Optimization Algorithms

```runa
Import "math/engine/numerical/optimization" as Optimization

Note: Gradient-based optimization using numerical differentiation
Process called "optimization_objective" that takes variables as Vector returns Real:
    Let x be LinAlg.get_element(variables, 0)
    Let y be LinAlg.get_element(variables, 1)
    Return (x - 3.0) * (x - 3.0) + (y + 1.0) * (y + 1.0) + MathFunctions.sin(x * y)

Let optimization_start_point be LinAlg.create_vector([0.0, 0.0])

Note: Use numerical gradient for optimization
Let optimization_with_numerical_gradient be Optimization.gradient_descent(
    optimization_objective,
    optimization_start_point,
    gradient_method: "numerical_central_difference",
    step_size: 1e-5,
    learning_rate: 0.01,
    max_iterations: 1000,
    tolerance: 1e-6
)

Let optimal_point be Optimization.get_optimal_point(optimization_with_numerical_gradient)
Let optimal_value be Optimization.get_optimal_value(optimization_with_numerical_gradient)
Let optimization_iterations be Optimization.get_iteration_count(optimization_with_numerical_gradient)

Display "Optimization results using numerical gradients:"
Display "Optimal point: " joined with LinAlg.vector_to_string(optimal_point)
Display "Optimal value: " joined with optimal_value
Display "Iterations: " joined with optimization_iterations

Note: Compare with automatic differentiation
Let optimization_with_ad be Optimization.gradient_descent(
    optimization_objective,
    optimization_start_point,
    gradient_method: "automatic_differentiation",
    learning_rate: 0.01,
    max_iterations: 1000,
    tolerance: 1e-6
)

Let ad_optimal_point be Optimization.get_optimal_point(optimization_with_ad)
Let ad_iterations be Optimization.get_iteration_count(optimization_with_ad)

Display "Optimization with AD - Iterations: " joined with ad_iterations
Display "Point difference: " joined with LinAlg.vector_norm(
    LinAlg.vector_subtract(optimal_point, ad_optimal_point), "euclidean")
```

### With Machine Learning Applications

```runa
Import "ml/neural_networks" as NeuralNet

Note: Backpropagation using automatic differentiation
Let neural_network be NeuralNet.create_simple_network([
    ("input_size", 10),
    ("hidden_layers", [20, 15]),
    ("output_size", 5),
    ("activation", "relu")
])

Let training_input be LinAlg.create_random_matrix(100, 10)  Note: 100 samples, 10 features
Let training_output be LinAlg.create_random_matrix(100, 5)   Note: 100 samples, 5 outputs

Note: Compute gradients for network weights using backpropagation
Let network_gradients be Differentiation.backpropagation_gradients(
    neural_network,
    training_input,
    training_output,
    loss_function: "mean_squared_error"
)

Let weight_gradient_norms be []
Let bias_gradient_norms be []

For layer_index from 0 to (NeuralNet.get_layer_count(neural_network) - 1):
    Let weight_grad be Differentiation.get_weight_gradient(network_gradients, layer_index)
    Let bias_grad be Differentiation.get_bias_gradient(network_gradients, layer_index)
    
    Let weight_norm be LinAlg.matrix_norm(weight_grad, "frobenius")
    Let bias_norm be LinAlg.vector_norm(bias_grad, "euclidean")
    
    Differentiation.append_to_list(weight_gradient_norms, weight_norm)
    Differentiation.append_to_list(bias_gradient_norms, bias_norm)

Display "Neural network gradient norms:"
For layer_index from 0 to (Differentiation.list_length(weight_gradient_norms) - 1):
    Let w_norm be Differentiation.get_list_element(weight_gradient_norms, layer_index)
    Let b_norm be Differentiation.get_list_element(bias_gradient_norms, layer_index)
    
    Display "Layer " joined with layer_index joined with ": ||∇W|| = " joined with w_norm
        joined with ", ||∇b|| = " joined with b_norm

Note: Gradient checking for backpropagation validation
Let gradient_check_result be Differentiation.gradient_check_neural_network(
    neural_network,
    training_input,
    training_output,
    computed_gradients: network_gradients,
    finite_difference_step: 1e-5,
    tolerance: 1e-5
)

Let gradient_check_passed be Differentiation.gradient_check_passed(gradient_check_result)
Let max_gradient_error be Differentiation.get_max_gradient_error(gradient_check_result)

Display "Gradient check results:"
Display "Check passed: " joined with gradient_check_passed
Display "Maximum gradient error: " joined with max_gradient_error
```

## Best Practices

### Method Selection Guidelines

```runa
Note: Decision matrix for differentiation method selection
Let differentiation_method_selector be Differentiation.create_method_selector([
    ("function_properties", [
        ("smoothness", ["smooth", "non_smooth", "discontinuous"]),
        ("noise_level", ["noise_free", "low_noise", "high_noise"]),
        ("computational_cost", ["cheap", "moderate", "expensive"])
    ]),
    ("accuracy_requirements", [
        ("precision", ["single", "double", "quad", "arbitrary"]),
        ("tolerance", [1e-6, 1e-10, 1e-14])
    ]),
    ("computational_constraints", [
        ("function_evaluations", ["unlimited", "limited", "severely_limited"]),
        ("memory", ["abundant", "moderate", "constrained"]),
        ("time", ["not_critical", "important", "critical"])
    ])
])

Let method_recommendation be Differentiation.recommend_differentiation_method(
    differentiation_method_selector,
    problem_characteristics: [
        ("smoothness", "smooth"),
        ("noise_level", "low_noise"),
        ("computational_cost", "expensive"),
        ("precision", "double"),
        ("tolerance", 1e-10),
        ("function_evaluations", "limited"),
        ("memory", "moderate"),
        ("time", "important")
    ]
)

Display "Recommended differentiation method:"
Display Differentiation.format_method_recommendation(method_recommendation)
```

### Numerical Stability and Accuracy

```runa
Note: Best practices implementation
Let best_practices_checker be Differentiation.create_best_practices_checker([
    ("step_size_selection", "automatic"),
    ("error_estimation", "enabled"),
    ("method_validation", "enabled"),
    ("precision_monitoring", "enabled")
])

Let best_practices_analysis be Differentiation.analyze_differentiation_setup(
    best_practices_checker,
    function: test_function,
    point: 2.0,
    method: "central_difference",
    step_size: 1e-5
)

Let practice_violations be Differentiation.get_practice_violations(best_practices_analysis)
Let improvement_suggestions be Differentiation.get_improvement_suggestions(best_practices_analysis)

Display "Best practices analysis:"
If Differentiation.has_violations(practice_violations):
    Display "Practice violations found:"
    For violation in practice_violations:
        Display "  - " joined with Differentiation.describe_violation(violation)
    
    Display "Improvement suggestions:"
    For suggestion in improvement_suggestions:
        Display "  - " joined with Differentiation.describe_suggestion(suggestion)
Otherwise:
    Display "All best practices followed"

Let quality_score be Differentiation.compute_quality_score(best_practices_analysis)
Display "Overall quality score: " joined with quality_score joined with "/100"
```

The Numerical Differentiation module provides comprehensive, accurate, and efficient algorithms for computing derivatives across all scales of scientific computing, with robust error analysis, adaptive methods, and integration with optimization and machine learning applications.