# Neural Network Operations

The Neural Operations module (`math/ai_math/neural_ops`) provides comprehensive neural network building blocks including activation functions, forward/backward propagation, weight initialization, batch normalization, dropout regularization, and fundamental layer operations. This module follows modern deep learning best practices with numerical stability and computational efficiency.

## Overview

This module implements the core mathematical operations required for deep neural networks, including:

- **Activation Functions**: ReLU, Sigmoid, Tanh, Softmax, GELU, Swish, and their derivatives
- **Layer Operations**: Linear transformations, convolutions, batch normalization
- **Weight Initialization**: Xavier/Glorot, He, and orthogonal initialization strategies
- **Regularization**: Dropout, layer normalization, gradient clipping
- **Pooling Operations**: Max pooling, average pooling, adaptive pooling

## Key Features

### Activation Functions
- **Numerically Stable**: Prevents overflow/underflow in extreme values
- **Differentiable**: Includes derivative computations for backpropagation
- **Configurable**: Parameters for customizing activation behavior

### Layer Operations
- **Batch Support**: Efficient batch processing for training
- **Memory Efficient**: Optimized memory usage for large tensors
- **GPU Ready**: Designed for parallel computation

### Weight Initialization
- **Gradient Flow**: Maintains healthy gradient flow in deep networks
- **Distribution Control**: Various initialization distributions available
- **Layer-Aware**: Appropriate initialization based on activation functions

## Core Types

### Activation Configuration
```runa
Type called "ActivationConfig":
    alpha as Float                    Note: Parameter for LeakyReLU, ELU
    beta as Float                     Note: Parameter for Swish, Mish
    temperature as Float              Note: Temperature for softmax
    axis as Integer                   Note: Axis for softmax computation
```

### Neural Layer Types
```runa
Type called "NeuralLayer":
    layer_type as String
    input_size as Integer
    output_size as Integer
    weights as Matrix[Float]
    biases as Vector[Float]
    activation as ActivationFunction

Type called "ConvolutionLayer":
    input_channels as Integer
    output_channels as Integer
    kernel_size as Tuple[Integer, Integer]
    stride as Tuple[Integer, Integer]
    padding as Tuple[Integer, Integer]
    weights as Tensor[Float]
    biases as Vector[Float]
```

## Activation Functions

### ReLU and Variants

#### ReLU (Rectified Linear Unit)
```runa
Import "math/ai_math/neural_ops" as NeuralOps

Let input_vector be Vector with components: ["2.5", "-1.0", "0.0", "3.2"], dimension: 4
Let relu_result be NeuralOps.relu_activation(input_vector)
Display "ReLU result: " joined with String(relu_result.components)
Note: Output: ["2.5", "0.0", "0.0", "3.2"]
```

**Mathematical Formula**: f(x) = max(0, x)

**Properties**:
- Non-saturating for positive inputs
- Computationally efficient
- Mitigates vanishing gradient problem
- Can suffer from "dying ReLU" problem

#### Leaky ReLU
```runa
Let alpha be 0.01  Note: Small slope for negative values
Let leaky_relu_result be NeuralOps.leaky_relu_activation(input_vector, alpha)
Display "Leaky ReLU result: " joined with String(leaky_relu_result.components)
Note: Output: ["2.5", "-0.01", "0.0", "3.2"]
```

**Mathematical Formula**: f(x) = max(αx, x) where α is small positive value

**Properties**:
- Prevents dying ReLU problem
- Small negative slope for negative inputs
- Better gradient flow than standard ReLU

### Sigmoid and Tanh

#### Sigmoid
```runa
Let sigmoid_result be NeuralOps.sigmoid_activation(input_vector)
Display "Sigmoid result: " joined with String(sigmoid_result.components)
Note: Output values in (0, 1) range, suitable for binary classification
```

**Mathematical Formula**: σ(x) = 1/(1 + e^(-x))

**Properties**:
- Output range: (0, 1)
- Suitable for binary classification
- Can suffer from vanishing gradient problem
- Numerically stable implementation with clipping

#### Hyperbolic Tangent
```runa
Let tanh_result be NeuralOps.tanh_activation(input_vector)
Display "Tanh result: " joined with String(tanh_result.components)
Note: Output values in (-1, 1) range, zero-centered
```

**Mathematical Formula**: tanh(x) = (e^x - e^(-x))/(e^x + e^(-x))

**Properties**:
- Output range: (-1, 1)
- Zero-centered output
- Better than sigmoid for hidden layers
- Still suffers from vanishing gradients

### Modern Activation Functions

#### GELU (Gaussian Error Linear Unit)
```runa
Let gelu_result be NeuralOps.gelu_activation(input_vector)
Display "GELU result: " joined with String(gelu_result.components)
Note: Smooth approximation with probabilistic interpretation
```

**Mathematical Formula**: GELU(x) = x × Φ(x) where Φ is the standard normal CDF
**Approximation**: GELU(x) ≈ x × σ(1.702x)

**Properties**:
- Smooth, differentiable everywhere
- Used in transformer architectures
- Better performance than ReLU in many cases

#### Swish (Self-Gated)
```runa
Let beta be 1.0  Note: Self-gating parameter
Let swish_result be NeuralOps.swish_activation(input_vector, beta)
Display "Swish result: " joined with String(swish_result.components)
Note: Self-gated activation with smooth properties
```

**Mathematical Formula**: f(x) = x × σ(βx) where σ is sigmoid

**Properties**:
- Self-gated activation
- Smooth and non-monotonic
- Good performance in deep networks

#### Softmax
```runa
Let logits be Vector with components: ["2.0", "1.0", "0.1"], dimension: 3
Let axis be 0  Note: Apply softmax along first dimension
Let softmax_result be NeuralOps.softmax_activation(logits, axis)
Display "Softmax result: " joined with String(softmax_result.components)
Note: Output sums to 1.0, suitable for multi-class classification
```

**Mathematical Formula**: σ(x_i) = e^(x_i) / Σ(e^(x_j))

**Properties**:
- Converts logits to probability distribution
- Output sums to 1.0
- Numerically stable with temperature scaling
- Used in multi-class classification

## Forward Propagation

### Linear Layer
```runa
Note: Dense/Fully-connected layer implementation
Let input be Vector with components: ["1.0", "2.0", "3.0"], dimension: 3
Let weights be LinAlg.create_matrix([
    ["0.5", "0.3", "0.2"],
    ["0.1", "0.8", "0.4"]
], "float")
Let bias be Vector with components: ["0.1", "-0.2"], dimension: 2

Let linear_output be NeuralOps.linear_forward(input, weights, bias)
Display "Linear output: " joined with String(linear_output.components)
Note: Computes y = Wx + b
```

**Mathematical Formula**: y = Wx + b

**Applications**:
- Dense layers in neural networks
- Output layers for classification/regression
- Basis for more complex architectures

### Convolution Layer
```runa
Note: 2D convolution for image processing
Let input_tensor be TensorOps.create_tensor(
    input_data, 
    [1, 3, 32, 32],  Note: [batch, channels, height, width]
    "float"
)

Let kernel_tensor be TensorOps.create_tensor(
    kernel_data,
    [16, 3, 3, 3],   Note: [out_channels, in_channels, kernel_h, kernel_w]
    "float"
)

Let conv_config be ConvolutionLayer with:
    input_channels: 3
    output_channels: 16
    kernel_size: Tuple with first: 3, second: 3
    stride: Tuple with first: 1, second: 1
    padding: Tuple with first: 1, second: 1

Let conv_output be NeuralOps.convolution_forward(input_tensor, kernel_tensor, conv_config)
Display "Convolution output shape: " joined with String(conv_output.shape)
```

**Mathematical Formula**: (I * K)[i,j] = ΣΣ I[i+m,j+n] × K[m,n]

**Applications**:
- Computer vision tasks
- Feature extraction from images
- Convolutional neural networks (CNNs)

## Batch Normalization

```runa
Note: Batch normalization for training stability
Let batch_norm_config be BatchNormLayer with:
    num_features: 64
    epsilon: 1e-5
    momentum: 0.1
    gamma: Vector with components: gamma_values, dimension: 64  Note: Scale parameters
    beta: Vector with components: beta_values, dimension: 64   Note: Shift parameters
    running_mean: Vector with components: mean_values, dimension: 64
    running_var: Vector with components: var_values, dimension: 64

Let training_mode be true
Let normalized_output be NeuralOps.batch_normalize_forward(
    input_tensor, 
    batch_norm_config, 
    training_mode
)

Display "Batch normalized output computed"
```

**Mathematical Formula**: BN(x) = γ × ((x - μ) / √(σ² + ε)) + β

**Benefits**:
- Stabilizes training
- Allows higher learning rates
- Reduces internal covariate shift
- Provides regularization effect

## Weight Initialization

### Xavier/Glorot Initialization
```runa
Note: Xavier uniform initialization for sigmoid/tanh activations
Let layer_shape be Tuple with first: 256, second: 128  Note: [output_size, input_size]
Let gain be 1.0  Note: Gain factor for the initialization

Let xavier_weights be NeuralOps.xavier_uniform_init(layer_shape, gain)
Display "Xavier initialized weights shape: " joined with String(xavier_weights.rows) joined with "x" joined with String(xavier_weights.columns)
```

**Mathematical Formula**: U(-√(6/(fan_in + fan_out)), √(6/(fan_in + fan_out)))

**Use Cases**:
- Sigmoid and tanh activations
- Maintaining variance across layers
- Preventing vanishing/exploding gradients

### He Initialization
```runa
Note: He normal initialization for ReLU activations
Let he_weights be NeuralOps.he_normal_init(layer_shape, gain)
Display "He initialized weights shape: " joined with String(he_weights.rows) joined with "x" joined with String(he_weights.columns)
```

**Mathematical Formula**: N(0, √(2/fan_in))

**Use Cases**:
- ReLU and variants
- Accounts for ReLU's effect on variance
- Modern deep networks

### Orthogonal Initialization
```runa
Note: Orthogonal initialization for RNNs and deep networks
Let ortho_weights be NeuralOps.orthogonal_init(layer_shape, gain)
Display "Orthogonal initialized weights computed"
```

**Properties**:
- Preserves norms during forward/backward pass
- Helps with gradient flow in deep networks
- Good for recurrent neural networks

## Pooling Operations

### Max Pooling
```runa
Note: Max pooling for spatial downsampling
Let pool_kernel be Tuple with first: 2, second: 2
Let pool_stride be Tuple with first: 2, second: 2

Let max_pooled be NeuralOps.max_pool_2d(input_tensor, pool_kernel, pool_stride)
Display "Max pooled output shape: " joined with String(max_pooled.shape)
```

**Properties**:
- Provides translation invariance
- Reduces spatial dimensions
- Preserves important features

### Average Pooling
```runa
Note: Average pooling for smooth downsampling
Let avg_pooled be NeuralOps.avg_pool_2d(input_tensor, pool_kernel, pool_stride)
Display "Average pooled output shape: " joined with String(avg_pooled.shape)
```

**Properties**:
- Smoother downsampling
- Less aggressive than max pooling
- Good for final feature maps

### Adaptive Pooling
```runa
Note: Adaptive pooling produces fixed output size
Let output_size be Tuple with first: 7, second: 7
Let adaptive_pooled be NeuralOps.adaptive_avg_pool(input_tensor, output_size)
Display "Adaptive pooled output shape: " joined with String(adaptive_pooled.shape)
```

**Benefits**:
- Fixed output size regardless of input
- Useful for variable input sizes
- Common before classification layers

## Regularization

### Dropout
```runa
Note: Dropout for regularization during training
Let dropout_prob be 0.5
Let training_mode be true

Let dropout_result be NeuralOps.dropout_forward(input_tensor, dropout_prob, training_mode)
Let output_tensor be dropout_result.first
Let dropout_mask be dropout_result.second

Display "Dropout applied with probability " joined with String(dropout_prob)
```

**Properties**:
- Prevents overfitting
- Reduces co-adaptation of neurons
- Scale compensation during training

### Layer Normalization
```runa
Note: Layer normalization for stable training
Let gamma be Vector with components: gamma_values, dimension: feature_size
Let beta be Vector with components: beta_values, dimension: feature_size
Let epsilon be 1e-6

Let layer_norm_output be NeuralOps.layer_normalize(input_tensor, gamma, beta, epsilon)
Display "Layer normalization applied"
```

**Mathematical Formula**: LN(x) = γ × ((x - μ) / σ) + β

**Benefits**:
- Normalizes across feature dimension
- Stable for RNNs and transformers
- Less dependent on batch size

### Gradient Clipping
```runa
Note: Gradient clipping to prevent exploding gradients
Let gradients be List[Tensor[Float]]()
Call gradients.add(grad_tensor_1)
Call gradients.add(grad_tensor_2)

Let max_norm be 5.0
Let clipped_gradients be NeuralOps.gradient_clipping(gradients, max_norm)

Let gradient_norm be NeuralOps.compute_gradient_norm(clipped_gradients)
Display "Gradient norm after clipping: " joined with String(gradient_norm)
```

**Benefits**:
- Prevents exploding gradients
- Stabilizes training
- Common in RNN training

## Backward Propagation

### Linear Layer Gradients
```runa
Note: Compute gradients for linear layer
Let grad_output be Vector with components: grad_values, dimension: output_size
Let linear_grads be NeuralOps.linear_backward(grad_output, input, weights)

Let grad_input be linear_grads.first
Let grad_weights be linear_grads.second  
Let grad_bias be linear_grads.third

Display "Linear layer gradients computed"
```

### Convolution Gradients
```runa
Note: Compute gradients for convolution layer
Let conv_grads be NeuralOps.convolution_backward(grad_output, input_tensor, kernel_tensor)

Let grad_input_tensor be conv_grads.first
Let grad_kernel_tensor be conv_grads.second

Display "Convolution gradients computed"
```

### Activation Derivatives
```runa
Note: Compute activation function derivatives
Let relu_derivative be NeuralOps.relu_derivative(input_vector)
Let sigmoid_derivative be NeuralOps.sigmoid_derivative(input_vector)

Note: For softmax, returns Jacobian matrix
Let softmax_jacobian be NeuralOps.softmax_derivative(logits, softmax_output)
Display "Activation derivatives computed"
```

## Performance Considerations

### Memory Optimization
- **In-place Operations**: When possible, operations modify tensors in-place
- **Memory Pooling**: Reuse memory buffers for temporary computations
- **Gradient Accumulation**: Accumulate gradients to reduce memory usage

### Numerical Stability
- **Overflow Protection**: All operations include overflow checking
- **Stable Algorithms**: Use numerically stable implementations
- **Epsilon Constants**: Small constants prevent division by zero

### Parallel Processing
- **Batch Operations**: Optimized for batch processing
- **Vectorization**: Operations work on entire tensors
- **Thread Safety**: Operations are designed to be thread-safe

## Common Patterns

### Building a Simple Neural Network
```runa
Note: Complete example of a simple feedforward network
Process called "simple_feedforward" that takes input as Vector[Float] returns Vector[Float]:
    Note: Input layer
    Let hidden_weights be NeuralOps.xavier_uniform_init(Tuple with first: 128, second: input.dimension, 1.0)
    Let hidden_bias be Vector with components: zeros_128, dimension: 128
    
    Note: Forward pass through hidden layer
    Let hidden_linear be NeuralOps.linear_forward(input, hidden_weights, hidden_bias)
    Let hidden_activated be NeuralOps.relu_activation(hidden_linear)
    
    Note: Apply dropout during training
    Let dropout_result be NeuralOps.dropout_forward(
        convert_vector_to_tensor(hidden_activated), 
        0.3, 
        true
    )
    Let hidden_dropped be convert_tensor_to_vector(dropout_result.first)
    
    Note: Output layer
    Let output_weights be NeuralOps.xavier_uniform_init(Tuple with first: 10, second: 128, 1.0)
    Let output_bias be Vector with components: zeros_10, dimension: 10
    
    Let output_linear be NeuralOps.linear_forward(hidden_dropped, output_weights, output_bias)
    Let output_softmax be NeuralOps.softmax_activation(output_linear, 0)
    
    Return output_softmax
```

### Training Loop Integration
```runa
Note: Integration with training loops
Process called "training_step" that takes model_params as List[Matrix[Float]], input_batch as Tensor[Float], targets as Tensor[Float] returns List[Matrix[Float]]:
    Note: Forward pass
    Let predictions be forward_pass(input_batch, model_params)
    
    Note: Compute loss and gradients
    Let loss be compute_loss(predictions, targets)
    Let gradients be backward_pass(loss, model_params)
    
    Note: Clip gradients if needed
    Let clipped_grads be NeuralOps.gradient_clipping(gradients, 5.0)
    
    Return clipped_grads
```

## Best Practices

### Activation Function Selection
- **ReLU**: Default choice for hidden layers
- **Leaky ReLU**: When dying ReLU is a problem
- **GELU/Swish**: For transformer architectures
- **Sigmoid/Tanh**: Avoid in deep networks (vanishing gradients)

### Weight Initialization
- **He initialization**: For ReLU and variants
- **Xavier initialization**: For sigmoid/tanh activations
- **Orthogonal**: For RNNs and very deep networks

### Regularization Strategy
- **Dropout**: 0.2-0.5 for hidden layers, lower for input
- **Batch normalization**: After linear layers, before activation
- **Layer normalization**: For RNNs and transformers
- **Gradient clipping**: Essential for RNN training

### Numerical Considerations
- **Check for overflows**: All operations include overflow detection
- **Use stable implementations**: Especially for softmax and sigmoid
- **Monitor gradients**: Watch for vanishing/exploding gradients

## Error Handling

```runa
Note: Comprehensive error handling example
Try:
    Let result be NeuralOps.linear_forward(input, weights, bias)
    Display "Forward pass successful"
Catch Errors.InvalidArgument as arg_error:
    Display "Invalid argument: " joined with arg_error.message
Catch Errors.ComputationError as comp_error:
    Display "Computation error: " joined with comp_error.message
    Display "Consider reducing precision or checking for numerical instability"
Catch Errors.MathematicalError as math_error:
    Display "Mathematical error: " joined with math_error.message
```

## Testing and Validation

### Gradient Checking
```runa
Note: Numerical gradient checking for verification
Process called "gradient_check" that takes layer as NeuralLayer, input as Vector[Float], epsilon as Float returns Boolean:
    Note: Compute analytical gradients
    Let analytical_grads be compute_analytical_gradients(layer, input)
    
    Note: Compute numerical gradients
    Let numerical_grads be compute_numerical_gradients(layer, input, epsilon)
    
    Note: Compare gradients
    Let relative_error be compute_relative_error(analytical_grads, numerical_grads)
    
    Return relative_error < 1e-5
```

### Unit Testing
```runa
Note: Unit test for activation functions
Process called "test_relu_properties":
    Let test_input be Vector with components: ["2.0", "-1.0", "0.0"], dimension: 3
    Let relu_output be NeuralOps.relu_activation(test_input)
    
    Note: Test ReLU properties
    Assert relu_output.components.get(0) == "2.0"  Note: Positive values unchanged
    Assert relu_output.components.get(1) == "0.0"  Note: Negative values set to zero
    Assert relu_output.components.get(2) == "0.0"  Note: Zero remains zero
    
    Display "ReLU tests passed"
```

## Related Documentation

- **[AI Math Optimization](optimization.md)**: Optimization algorithms for training
- **[AI Math Loss Functions](loss_functions.md)**: Loss functions and regularization
- **[AI Math Attention](attention.md)**: Attention mechanisms and transformers
- **[Linear Algebra Core](../engine/linalg/core.md)**: Matrix and vector operations
- **[Math Core Operations](../core/operations.md)**: Basic mathematical operations

The Neural Operations module provides the essential building blocks for implementing modern deep learning architectures with numerical stability, computational efficiency, and comprehensive error handling.