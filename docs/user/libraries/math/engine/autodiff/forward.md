# Forward-Mode Automatic Differentiation

Forward-mode automatic differentiation (also called forward accumulation or tangent-linear mode) computes derivatives alongside function evaluations using dual numbers. This approach is particularly efficient for functions with few inputs and many outputs.

## Overview

Forward-mode AD works by augmenting each variable with its derivative information and propagating these dual numbers through computations. For a function f(x), the derivative f'(x) is computed simultaneously with f(x) using dual number arithmetic.

### Key Concepts

- **Dual Numbers**: Numbers of the form a + b·ε where ε² = 0
- **Directional Derivatives**: Derivatives in specific directions
- **Multivariate Differentiation**: Computing partial derivatives for multiple variables
- **Higher-Order Derivatives**: Using nested dual numbers

## Core Data Structures

### DualNumber

The fundamental structure for forward-mode differentiation:

```runa
Type called "DualNumber":
    real as Float      Note: function value
    dual as Float      Note: derivative value
```

**Usage Example:**
```runa
Note: Representing f(x) = x² at x = 3 with dual number
Let x_dual be DualNumber with:
    real = 3.0      Note: x value
    dual = 1.0      Note: dx/dx = 1 (seed value)

Note: Computing f(x) = x² gives f'(x) = 2x
Let result be dual_multiply(x_dual, x_dual)
Note: result.real = 9.0, result.dual = 6.0
```

### MultiDual

For functions with multiple variables:

```runa
Type called "MultiDual":
    value as Float
    derivatives as List[Float]    Note: partial derivatives
    num_variables as Integer
```

**Usage Example:**
```runa
Note: For function f(x,y) = x²y at point (2,3)
Let x_multidual be MultiDual with:
    value = 2.0
    derivatives = [1.0, 0.0]    Note: seed for ∂/∂x
    num_variables = 2

Let y_multidual be MultiDual with:
    value = 3.0
    derivatives = [0.0, 1.0]    Note: seed for ∂/∂y
    num_variables = 2
```

### HyperDual

For computing second-order derivatives:

```runa
Type called "HyperDual":
    f as Float      Note: function value
    f_x as Float    Note: ∂f/∂x
    f_y as Float    Note: ∂f/∂y
    f_xy as Float   Note: ∂²f/∂x∂y
```

## Dual Number Arithmetic

### Basic Operations

**Addition:**
```runa
Process called "dual_add" that takes a as DualNumber, b as DualNumber returns DualNumber:
    Let result be DualNumber with:
        real = a.real + b.real
        dual = a.dual + b.dual
    Return result
```

**Multiplication:**
```runa
Process called "dual_multiply" that takes a as DualNumber, b as DualNumber returns DualNumber:
    Let result be DualNumber with:
        real = a.real * b.real
        dual = a.dual * b.real + a.real * b.dual
    Return result
```

### Mathematical Functions

Forward-mode AD extends to all elementary functions:

**Exponential:**
```runa
Note: For f(x) = e^x, f'(x) = e^x
Process called "dual_exp" that takes x as DualNumber returns DualNumber:
    Let exp_real be MathCore.exponential(x.real)
    Let result be DualNumber with:
        real = exp_real
        dual = x.dual * exp_real
    Return result
```

**Sine:**
```runa
Note: For f(x) = sin(x), f'(x) = cos(x)
Process called "dual_sin" that takes x as DualNumber returns DualNumber:
    Let result be DualNumber with:
        real = MathCore.sine(x.real)
        dual = x.dual * MathCore.cosine(x.real)
    Return result
```

## Practical Applications

### Computing Derivatives

**Single Variable:**
```runa
Note: Compute derivative of f(x) = x³ + 2x² - 5x + 1 at x = 2
Let x be DualNumber with:
    real = 2.0
    dual = 1.0    Note: seed derivative dx/dx = 1

Let x_squared be dual_multiply(x, x)
Let x_cubed be dual_multiply(x_squared, x)
Let term1 be x_cubed
Let term2 be dual_scalar_multiply(x_squared, 2.0)
Let term3 be dual_scalar_multiply(x, -5.0)
Let constant be create_dual_constant(1.0)

Let result be dual_add(dual_add(dual_add(term1, term2), term3), constant)
Note: result.real = f(2) = 8 + 8 - 10 + 1 = 7
Note: result.dual = f'(2) = 12 + 8 - 5 = 15
```

**Multiple Variables:**
```runa
Note: Compute gradient of f(x,y) = x²y + xy² at (1,2)
Let x be create_multidual(1.0, [1.0, 0.0], 2)  Note: seed for ∂/∂x
Let y be create_multidual(2.0, [0.0, 1.0], 2)  Note: seed for ∂/∂y

Let x_squared be multidual_multiply(x, x)
Let y_squared be multidual_multiply(y, y)
Let term1 be multidual_multiply(x_squared, y)
Let term2 be multidual_multiply(x, y_squared)
Let result be multidual_add(term1, term2)

Note: result.value = 1²·2 + 1·2² = 6
Note: result.derivatives[0] = ∂f/∂x = 2xy + y² = 8
Note: result.derivatives[1] = ∂f/∂y = x² + 2xy = 5
```

### Jacobian Computation

For vector-valued functions f: ℝⁿ → ℝᵐ:

```runa
Note: Compute Jacobian of f(x,y) = [x²+y, xy, y²] at (2,3)
Process called "compute_jacobian_column" that takes inputs as List[MultiDual], function as String, column as Integer returns List[Float]:
    Note: Compute one column of Jacobian matrix
    Let seed_vector be Collections.create_list_with_size(inputs.size(), 0.0)
    Set seed_vector[column] to 1.0
    
    Let seeded_inputs be List[MultiDual]
    For i from 0 to inputs.size() - 1:
        Let seeded_input be MultiDual with:
            value = inputs[i].value
            derivatives = seed_vector
            num_variables = inputs.size()
        Call seeded_inputs.append(seeded_input)
    
    Let outputs be evaluate_function(function, seeded_inputs)
    Let jacobian_column be List[Float]
    For output in outputs:
        Call jacobian_column.append(output.derivatives[column])
    
    Return jacobian_column
```

### Directional Derivatives

Computing derivatives in specific directions:

```runa
Note: Compute directional derivative of f(x,y) = x²y in direction v = [3,4]
Let direction be [3.0, 4.0]
Let direction_norm be MathCore.sqrt(3.0*3.0 + 4.0*4.0)  Note: normalize direction
Let unit_direction be [3.0/direction_norm, 4.0/direction_norm]

Let x be create_multidual(2.0, [unit_direction[0], 0.0], 2)
Let y be create_multidual(1.0, [unit_direction[1], 0.0], 2)
Let result be multidual_multiply(multidual_multiply(x, x), y)

Note: Directional derivative = ∇f · v̂ = result.derivatives[0]
```

## Higher-Order Derivatives

### Second Derivatives with HyperDual Numbers

```runa
Note: Compute Hessian of f(x,y) = x³y + xy³
Process called "compute_hessian_hyperdual" that takes x_val as Float, y_val as Float, function as String returns List[List[Float]]:
    Let x be HyperDual with:
        f = x_val
        f_x = 1.0      Note: ∂x/∂x = 1
        f_y = 0.0      Note: ∂x/∂y = 0
        f_xy = 0.0     Note: ∂²x/∂x∂y = 0
    
    Let y be HyperDual with:
        f = y_val
        f_x = 0.0      Note: ∂y/∂x = 0
        f_y = 1.0      Note: ∂y/∂y = 1
        f_xy = 0.0     Note: ∂²y/∂x∂y = 0
    
    Let result be evaluate_hyperdual_function(function, x, y)
    
    Let hessian be Collections.create_matrix(2, 2, 0.0)
    Collections.set_matrix_element(hessian, 0, 0, result.f_xx)
    Collections.set_matrix_element(hessian, 0, 1, result.f_xy)
    Collections.set_matrix_element(hessian, 1, 0, result.f_xy)
    Collections.set_matrix_element(hessian, 1, 1, result.f_yy)
    
    Return hessian
```

### Taylor Series Computation

```runa
Note: Compute Taylor series of f(x) = sin(x) around x₀ = 0
Process called "compute_taylor_series" that takes function as String, center as Float, order as Integer returns TaylorSeries:
    Let coefficients be List[Float]
    Let x_dual be DualNumber with:
        real = center
        dual = 1.0
    
    For n from 0 to order:
        Let nth_derivative be compute_nth_derivative(function, x_dual, n)
        Let factorial_n be MathCore.factorial(n)
        Let coefficient be nth_derivative / factorial_n
        Call coefficients.append(coefficient)
    
    Let series be TaylorSeries with:
        coefficients = coefficients
        order = order
        variable_name = "x"
    
    Return series
```

## Advanced Features

### Automatic Function Composition

```runa
Note: Automatically differentiate composite functions
Process called "compose_functions" that takes outer as String, inner as String, input as DualNumber returns DualNumber:
    Let inner_result be evaluate_dual_function(inner, input)
    Let outer_result be evaluate_dual_function(outer, inner_result)
    Return outer_result

Note: Example: d/dx[sin(x²)] = cos(x²) · 2x
Let x be DualNumber with real=2.0, dual=1.0
Let composition be compose_functions("sin", "square", x)
Note: composition.dual contains the chain rule result
```

### Memory-Efficient Computation

```runa
Note: Streaming computation for large-scale problems
Process called "streaming_forward_ad" that takes function as String, inputs as Stream[DualNumber] returns Stream[DualNumber]:
    Let output_stream be Collections.create_stream()
    
    For input_batch in inputs:
        Let output_batch be evaluate_dual_function_batch(function, input_batch)
        Call output_stream.emit(output_batch)
    
    Return output_stream
```

### Error Analysis and Conditioning

```runa
Note: Analyze numerical stability of derivatives
Process called "analyze_derivative_conditioning" that takes function as String, point as List[Float], perturbation as Float returns Dictionary[String, Float]:
    Let exact_derivatives be compute_forward_derivatives(function, point)
    Let perturbed_point be List[Float]
    
    For i from 0 to point.size() - 1:
        Set perturbed_point[i] to point[i] + perturbation
    
    Let perturbed_derivatives be compute_forward_derivatives(function, perturbed_point)
    Let condition_numbers be Dictionary[String, Float]
    
    For i from 0 to exact_derivatives.size() - 1:
        Let relative_error be MathCore.abs((perturbed_derivatives[i] - exact_derivatives[i]) / exact_derivatives[i])
        Let condition_number be relative_error / perturbation
        Collections.set_item(condition_numbers, "derivative_" + i.to_string(), condition_number)
    
    Return condition_numbers
```

## Integration with Optimization

### Gradient-Based Optimization

```runa
Note: Newton's method using forward-mode AD
Process called "newton_optimization" that takes function as String, initial_guess as List[Float], tolerance as Float returns List[Float]:
    Let current_point be initial_guess
    Let max_iterations be 100
    
    For iteration from 0 to max_iterations - 1:
        Let gradient be compute_forward_gradient(function, current_point)
        Let hessian be compute_forward_hessian(function, current_point)
        Let newton_step be solve_linear_system(hessian, gradient)
        
        For i from 0 to current_point.size() - 1:
            Set current_point[i] to current_point[i] - newton_step[i]
        
        Let gradient_norm be compute_vector_norm(gradient)
        If gradient_norm < tolerance:
            Break
    
    Return current_point
```

### Line Search with Derivatives

```runa
Note: Backtracking line search using exact derivatives
Process called "backtracking_line_search" that takes function as String, point as List[Float], direction as List[Float] returns Float:
    Let alpha be 1.0
    Let rho be 0.5
    Let c1 be 0.0001
    
    Let f0 be evaluate_function_scalar(function, point)
    Let grad0 be compute_forward_gradient(function, point)
    Let directional_derivative be compute_dot_product(grad0, direction)
    
    While true:
        Let new_point be List[Float]
        For i from 0 to point.size() - 1:
            Set new_point[i] to point[i] + alpha * direction[i]
        
        Let f_alpha be evaluate_function_scalar(function, new_point)
        Let armijo_condition be f0 + c1 * alpha * directional_derivative
        
        If f_alpha <= armijo_condition:
            Break
        
        Set alpha to alpha * rho
    
    Return alpha
```

## Best Practices and Performance Tips

### 1. Choose Forward Mode When

- **Few inputs, many outputs**: Forward mode scales with input dimension
- **Computing Jacobians**: Efficient for tall matrices (m >> n)
- **Real-time applications**: Lower memory overhead than reverse mode

### 2. Memory Management

```runa
Note: Reuse dual number objects to minimize allocations
Let dual_pool be Collections.create_object_pool(DualNumber, 1000)

Process called "efficient_dual_computation" that takes inputs as List[Float] returns List[Float]:
    Let dual_inputs be List[DualNumber]
    For input in inputs:
        Let dual_input be dual_pool.acquire()
        Set dual_input.real to input
        Set dual_input.dual to 1.0
        Call dual_inputs.append(dual_input)
    
    Let results be perform_computation(dual_inputs)
    
    Note: Return objects to pool
    For dual_input in dual_inputs:
        Call dual_pool.release(dual_input)
    
    Return extract_derivatives(results)
```

### 3. Numerical Stability

```runa
Note: Use numerically stable formulations
Process called "stable_log_sum_exp" that takes x as List[DualNumber] returns DualNumber:
    Let max_val be find_maximum_dual(x)
    Let shifted_exp_sum be create_dual_constant(0.0)
    
    For xi in x:
        Let shifted be dual_subtract(xi, max_val)
        Let exp_shifted be dual_exp(shifted)
        Set shifted_exp_sum to dual_add(shifted_exp_sum, exp_shifted)
    
    Let log_sum be dual_add(max_val, dual_log(shifted_exp_sum))
    Return log_sum
```

### 4. Vectorization and SIMD

```runa
Note: Vectorized dual number operations
Process called "vectorized_dual_multiply" that takes a as List[DualNumber], b as List[DualNumber] returns List[DualNumber]:
    If a.size() != b.size():
        Throw Errors.InvalidArgument with "Vector sizes must match"
    
    Let result be List[DualNumber]
    Let batch_size be 8  Note: SIMD width
    
    For i from 0 to a.size() step batch_size:
        Let end_idx be MathCore.min(i + batch_size, a.size())
        Let batch_result be simd_dual_multiply(a[i:end_idx], b[i:end_idx])
        Call result.extend(batch_result)
    
    Return result
```

Forward-mode automatic differentiation provides exact derivatives with minimal computational overhead for functions with few inputs. Its simplicity and numerical stability make it ideal for gradient-based optimization, sensitivity analysis, and real-time applications requiring derivative information.