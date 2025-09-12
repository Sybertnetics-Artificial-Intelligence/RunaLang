# Reverse-Mode Automatic Differentiation

Reverse-mode automatic differentiation (also called backpropagation or reverse accumulation) efficiently computes gradients of scalar-valued functions with respect to many input variables. This is the foundational technique behind modern machine learning and deep neural networks.

## Overview

Reverse-mode AD works by building a computational graph during the forward pass, then traversing it in reverse order to accumulate gradients. For a function f: ℝⁿ → ℝ, reverse mode computes the full gradient ∇f in O(1) passes, making it highly efficient for functions with many inputs.

### Key Concepts

- **Computational Graph**: Directed acyclic graph representing function composition
- **Forward Pass**: Computing function values and building the graph
- **Backward Pass**: Traversing graph in reverse to accumulate gradients
- **Adjoint Variables**: Variables storing gradient information
- **Chain Rule**: Automatic application of the chain rule through graph traversal

## Core Data Structures

### AdjointVariable

The fundamental structure for reverse-mode differentiation:

```runa
Type called "AdjointVariable":
    value as Float                    Note: forward pass value
    adjoint as Float                  Note: accumulated gradient
    grad_fn as String                 Note: gradient function reference
    children as List[String]          Note: child variables in graph
    requires_grad as Boolean          Note: whether to compute gradients
```

**Usage Example:**
```runa
Note: Creating adjoint variables for f(x,y) = x²y
Let x be create_adjoint_variable(2.0, true)
Let y be create_adjoint_variable(3.0, true)
Let x_squared be adjoint_multiply(x, x)
Let result be adjoint_multiply(x_squared, y)

Note: result.value = 12.0, gradients computed on backward pass
```

### ComputationNode

Represents operations in the computational graph:

```runa
Type called "ComputationNode":
    operation as String               Note: operation type (add, mul, sin, etc.)
    inputs as List[String]            Note: input variable references
    output as String                  Note: output variable reference
    local_gradients as List[Float]    Note: local partial derivatives
    adjoint_contribution as Float     Note: gradient contribution
```

### BackwardPass

Manages the reverse traversal and gradient accumulation:

```runa
Type called "BackwardPass":
    topology_order as List[String]         Note: topological order for traversal
    gradient_functions as Dictionary[String, String]  Note: gradient computation functions
    intermediate_values as Dictionary[String, Float]  Note: cached forward values
    final_adjoints as Dictionary[String, Float]       Note: final gradient values
```

## Basic Operations and Gradient Rules

### Addition Backward Pass

```runa
Process called "add_backward" that takes output_adjoint as Float, input_adjoints as List[Float] returns List[Float]:
    Note: For z = x + y, ∂L/∂x = ∂L/∂z, ∂L/∂y = ∂L/∂z
    Let result be List[Float]
    For i from 0 to input_adjoints.size() - 1:
        Call result.append(output_adjoint)
    Return result
```

**Mathematical Principle:**
For addition z = x + y, the local gradients are:
- ∂z/∂x = 1
- ∂z/∂y = 1

### Multiplication Backward Pass

```runa
Process called "multiply_backward" that takes output_adjoint as Float, input_values as List[Float], input_adjoints as List[Float] returns List[Float]:
    Note: For z = x * y, ∂L/∂x = ∂L/∂z * y, ∂L/∂y = ∂L/∂z * x
    Let result be List[Float]
    If input_values.size() == 2:
        Call result.append(output_adjoint * input_values[1])  Note: ∂L/∂x
        Call result.append(output_adjoint * input_values[0])  Note: ∂L/∂y
    Otherwise:
        Note: Product rule for multiple variables
        For i from 0 to input_values.size() - 1:
            Let product be 1.0
            For j from 0 to input_values.size() - 1:
                If i != j:
                    Set product to product * input_values[j]
            Call result.append(output_adjoint * product)
    Return result
```

### Nonlinear Function Gradients

**Exponential:**
```runa
Process called "exp_backward" that takes output_adjoint as Float, input_value as Float, output_value as Float returns Float:
    Note: For z = exp(x), ∂z/∂x = exp(x) = z
    Return output_adjoint * output_value
```

**Logarithm:**
```runa
Process called "log_backward" that takes output_adjoint as Float, input_value as Float returns Float:
    Note: For z = log(x), ∂z/∂x = 1/x
    If input_value <= 0.0:
        Throw Errors.InvalidArgument with "Logarithm gradient undefined for non-positive values"
    Return output_adjoint / input_value
```

**Trigonometric Functions:**
```runa
Process called "sin_backward" that takes output_adjoint as Float, input_value as Float returns Float:
    Note: For z = sin(x), ∂z/∂x = cos(x)
    Return output_adjoint * MathCore.cosine(input_value)

Process called "cos_backward" that takes output_adjoint as Float, input_value as Float returns Float:
    Note: For z = cos(x), ∂z/∂x = -sin(x)
    Return output_adjoint * (-MathCore.sine(input_value))
```

## Graph Construction and Management

### Building the Computation Graph

```runa
Process called "build_computation_graph" that takes function as String, inputs as List[AdjointVariable] returns ComputationGraph:
    Let graph be create_empty_computation_graph()
    Let node_counter be 0
    
    Note: Forward pass - build graph while computing values
    For input in inputs:
        Let input_node be GraphNode with:
            id = "input_" + node_counter.to_string()
            operation = "input"
            value = input.value
            gradient = 0.0
            parents = List[String]
            children = List[String]
            requires_grad = input.requires_grad
        
        Call add_node_to_graph(graph, input_node)
        Set node_counter to node_counter + 1
    
    Note: Build intermediate and output nodes through function evaluation
    Let output_nodes be evaluate_function_with_graph(function, inputs, graph)
    Set graph.output_nodes to output_nodes
    
    Return graph
```

### Topological Sorting

```runa
Process called "topological_sort" that takes graph as ComputationGraph returns List[String]:
    Note: Kahn's algorithm for topological ordering
    Let in_degree be Dictionary[String, Integer]
    Let queue be Collections.create_queue()
    Let result be List[String]
    
    Note: Initialize in-degrees
    For node_id in Collections.get_keys(graph.nodes):
        Let node be Collections.get_item(graph.nodes, node_id)
        Collections.set_item(in_degree, node_id, node.parents.size())
        If node.parents.size() == 0:
            Call queue.enqueue(node_id)
    
    Note: Process nodes in topological order
    While not queue.is_empty():
        Let current_id be queue.dequeue()
        Call result.append(current_id)
        
        Let current_node be Collections.get_item(graph.nodes, current_id)
        For child_id in current_node.children:
            Let current_in_degree be Collections.get_item(in_degree, child_id)
            Collections.set_item(in_degree, child_id, current_in_degree - 1)
            If current_in_degree - 1 == 0:
                Call queue.enqueue(child_id)
    
    Return result
```

## Gradient Computation

### Full Backward Pass

```runa
Process called "backward" that takes graph as ComputationGraph, loss_value as Float returns Dictionary[String, Float]:
    Note: Complete backward pass through computation graph
    Let topo_order be topological_sort(graph)
    Call Collections.reverse(topo_order)  Note: reverse for backward pass
    
    Note: Initialize output gradients
    For output_id in graph.output_nodes:
        Let output_node be Collections.get_item(graph.nodes, output_id)
        Set output_node.gradient to 1.0  Note: ∂L/∂L = 1
    
    Note: Backward pass through all nodes
    For node_id in topo_order:
        Let node be Collections.get_item(graph.nodes, node_id)
        
        If node.operation != "input":
            Call compute_node_gradients(graph, node)
    
    Note: Collect final gradients for input variables
    Let final_gradients be Dictionary[String, Float]
    For input_id in graph.input_nodes:
        Let input_node be Collections.get_item(graph.nodes, input_id)
        If input_node.requires_grad:
            Collections.set_item(final_gradients, input_id, input_node.gradient)
    
    Return final_gradients
```

### Node Gradient Computation

```runa
Process called "compute_node_gradients" that takes graph as ComputationGraph, node as GraphNode returns Nothing:
    Note: Compute gradients for a specific node
    Let parent_gradients be List[Float]
    Let parent_values be List[Float]
    
    Note: Collect parent information
    For parent_id in node.parents:
        Let parent_node be Collections.get_item(graph.nodes, parent_id)
        Call parent_values.append(parent_node.value)
        Call parent_gradients.append(0.0)  Note: to be updated
    
    Note: Compute local gradients based on operation
    Let local_grads be compute_local_gradients(node.operation, node.gradient, parent_values, node.value)
    
    Note: Accumulate gradients to parent nodes
    For i from 0 to node.parents.size() - 1:
        Let parent_id be node.parents[i]
        Let parent_node be Collections.get_item(graph.nodes, parent_id)
        Set parent_node.gradient to parent_node.gradient + local_grads[i]
```

## Advanced Features

### Higher-Order Gradients

```runa
Process called "compute_hessian_vector_product" that takes function as String, inputs as List[Float], vector as List[Float] returns List[Float]:
    Note: Efficient Hessian-vector product using forward-over-reverse
    Let n be inputs.size()
    Let forward_seeds be List[List[Float]]
    
    For i from 0 to n - 1:
        Let seed be Collections.create_list_with_size(n, 0.0)
        Set seed[i] to vector[i]
        Call forward_seeds.append(seed)
    
    Note: Forward mode over reverse mode
    Let hvp be List[Float]
    For seed in forward_seeds:
        Let dual_inputs be create_dual_variables(inputs, seed)
        Let dual_gradient be compute_reverse_gradient_dual(function, dual_inputs)
        
        For i from 0 to n - 1:
            Call hvp.append(dual_gradient[i].dual)
    
    Return hvp
```

### Memory Management and Checkpointing

```runa
Process called "gradient_checkpointing" that takes graph as ComputationGraph, checkpoint_frequency as Integer returns Dictionary[String, Float]:
    Note: Trade computation for memory using checkpointing
    Let checkpoints be Dictionary[Integer, CheckpointState]
    Let segment_length be checkpoint_frequency
    
    Note: Forward pass with selective checkpointing
    For i from 0 to graph.execution_order.size() step segment_length:
        Let checkpoint be create_checkpoint(graph, i, i + segment_length)
        Collections.set_item(checkpoints, i, checkpoint)
    
    Note: Backward pass with recomputation
    Let gradients be Dictionary[String, Float]
    For checkpoint_idx in Collections.get_keys(checkpoints):
        Let checkpoint be Collections.get_item(checkpoints, checkpoint_idx)
        Let segment_gradients be recompute_segment_gradients(checkpoint)
        Call merge_gradients(gradients, segment_gradients)
    
    Return gradients
```

### Dynamic Computation Graphs

```runa
Process called "create_dynamic_graph" that returns DynamicGraphBuilder:
    Let builder be DynamicGraphBuilder with:
        current_context = Collections.create_stack()
        node_registry = Dictionary[String, GraphNode]
        tape = List[ComputationNode]
        gradient_tape = List[String]
        
    Return builder

Process called "record_operation" that takes builder as DynamicGraphBuilder, operation as String, inputs as List[String], output as String returns Nothing:
    Note: Record operation on dynamic tape
    Let node be ComputationNode with:
        operation = operation
        inputs = inputs
        output = output
        local_gradients = List[Float]
        adjoint_contribution = 0.0
    
    Call builder.tape.append(node)
    Call builder.gradient_tape.append(output)
```

## Machine Learning Applications

### Neural Network Layer Gradients

```runa
Process called "linear_layer_backward" that takes output_grad as List[Float], input_values as List[Float], weights as List[List[Float]], bias as List[Float] returns Dictionary[String, Any]:
    Note: Backward pass for linear layer: y = Wx + b
    Let input_grad be List[Float]
    Let weight_grad be Collections.create_matrix(weights.height(), weights.width(), 0.0)
    Let bias_grad be List[Float]
    
    Note: Input gradients: ∂L/∂x = W^T ∂L/∂y
    For i from 0 to input_values.size() - 1:
        Let grad_sum be 0.0
        For j from 0 to output_grad.size() - 1:
            Set grad_sum to grad_sum + weights[j][i] * output_grad[j]
        Call input_grad.append(grad_sum)
    
    Note: Weight gradients: ∂L/∂W = ∂L/∂y ⊗ x
    For i from 0 to weights.height() - 1:
        For j from 0 to weights.width() - 1:
            Collections.set_matrix_element(weight_grad, i, j, output_grad[i] * input_values[j])
    
    Note: Bias gradients: ∂L/∂b = ∂L/∂y
    Set bias_grad to output_grad
    
    Let result be Dictionary[String, Any]
    Collections.set_item(result, "input_grad", input_grad)
    Collections.set_item(result, "weight_grad", weight_grad)
    Collections.set_item(result, "bias_grad", bias_grad)
    
    Return result
```

### Activation Function Gradients

```runa
Process called "relu_backward" that takes output_grad as List[Float], input_values as List[Float] returns List[Float]:
    Note: ReLU gradient: ∂ReLU(x)/∂x = 1 if x > 0, else 0
    Let input_grad be List[Float]
    For i from 0 to input_values.size() - 1:
        If input_values[i] > 0.0:
            Call input_grad.append(output_grad[i])
        Otherwise:
            Call input_grad.append(0.0)
    Return input_grad

Process called "sigmoid_backward" that takes output_grad as List[Float], output_values as List[Float] returns List[Float]:
    Note: Sigmoid gradient: ∂σ(x)/∂x = σ(x)(1 - σ(x))
    Let input_grad be List[Float]
    For i from 0 to output_values.size() - 1:
        Let sigmoid_grad be output_values[i] * (1.0 - output_values[i])
        Call input_grad.append(output_grad[i] * sigmoid_grad)
    Return input_grad
```

### Loss Function Gradients

```runa
Process called "mean_squared_error_backward" that takes predictions as List[Float], targets as List[Float] returns List[Float]:
    Note: MSE gradient: ∂/∂ŷ[(ŷ - y)²] = 2(ŷ - y)
    Let gradients be List[Float]
    For i from 0 to predictions.size() - 1:
        Let gradient be 2.0 * (predictions[i] - targets[i]) / predictions.size()
        Call gradients.append(gradient)
    Return gradients

Process called "cross_entropy_backward" that takes predictions as List[Float], targets as List[Integer] returns List[Float]:
    Note: Cross-entropy gradient: ∂/∂ŷᵢ[-log(ŷᵢ)] = -1/ŷᵢ for target class
    Let gradients be Collections.create_list_with_size(predictions.size(), 0.0)
    For i from 0 to targets.size() - 1:
        Let target_class be targets[i]
        Let prediction be predictions[target_class]
        If prediction <= 0.0:
            Throw Errors.InvalidArgument with "Cross-entropy requires positive predictions"
        Set gradients[target_class] to -1.0 / prediction
    Return gradients
```

## Optimization Algorithms Using Reverse-Mode AD

### Stochastic Gradient Descent

```runa
Process called "sgd_step" that takes parameters as List[Float], gradients as List[Float], learning_rate as Float returns List[Float]:
    Note: SGD update: θ = θ - η∇θL
    Let updated_params be List[Float]
    For i from 0 to parameters.size() - 1:
        Let new_param be parameters[i] - learning_rate * gradients[i]
        Call updated_params.append(new_param)
    Return updated_params
```

### Adam Optimizer

```runa
Process called "adam_step" that takes parameters as List[Float], gradients as List[Float], m as List[Float], v as List[Float], beta1 as Float, beta2 as Float, learning_rate as Float, epsilon as Float, t as Integer returns Dictionary[String, Any]:
    Note: Adam optimization with bias correction
    Let updated_params be List[Float]
    Let updated_m be List[Float]
    Let updated_v be List[Float]
    
    For i from 0 to parameters.size() - 1:
        Note: Update biased first moment estimate
        Let m_new be beta1 * m[i] + (1.0 - beta1) * gradients[i]
        Call updated_m.append(m_new)
        
        Note: Update biased second moment estimate
        Let v_new be beta2 * v[i] + (1.0 - beta2) * gradients[i] * gradients[i]
        Call updated_v.append(v_new)
        
        Note: Compute bias-corrected estimates
        Let m_hat be m_new / (1.0 - MathCore.power(beta1, t))
        Let v_hat be v_new / (1.0 - MathCore.power(beta2, t))
        
        Note: Update parameters
        Let param_update be learning_rate * m_hat / (MathCore.sqrt(v_hat) + epsilon)
        Let new_param be parameters[i] - param_update
        Call updated_params.append(new_param)
    
    Let result be Dictionary[String, Any]
    Collections.set_item(result, "parameters", updated_params)
    Collections.set_item(result, "m", updated_m)
    Collections.set_item(result, "v", updated_v)
    
    Return result
```

## Performance Optimization

### Efficient Memory Management

```runa
Process called "create_gradient_tape" that takes initial_capacity as Integer returns GradientTape:
    Let tape be GradientTape with:
        operations = Collections.create_list_with_capacity(initial_capacity)
        memory_pool = create_memory_pool(initial_capacity)
        allocation_strategy = "linear"
        garbage_collection_threshold = initial_capacity * 2
    
    Return tape

Process called "optimize_computation_graph" that takes graph as ComputationGraph returns ComputationGraph:
    Note: Optimize graph for better cache locality and reduced memory usage
    Let optimized_graph be graph
    
    Note: Fuse compatible operations
    Call fuse_elementwise_operations(optimized_graph)
    
    Note: Reorder operations for better memory access patterns
    Call reorder_operations_for_locality(optimized_graph)
    
    Note: Eliminate redundant computations
    Call eliminate_common_subexpressions(optimized_graph)
    
    Return optimized_graph
```

### Vectorization and Parallelization

```runa
Process called "vectorized_backward_pass" that takes graph as ComputationGraph, batch_size as Integer returns Dictionary[String, List[Float]]:
    Note: Vectorized gradient computation for mini-batches
    Let batched_gradients be Dictionary[String, List[Float]]
    
    Note: Process operations in vectorized batches
    For node_id in reverse_topological_order(graph):
        Let node be Collections.get_item(graph.nodes, node_id)
        Let vectorized_grads be compute_vectorized_gradients(node, batch_size)
        Collections.set_item(batched_gradients, node_id, vectorized_grads)
    
    Return batched_gradients

Process called "parallel_gradient_computation" that takes graph as ComputationGraph, num_threads as Integer returns Dictionary[String, Float]:
    Note: Parallel gradient computation using graph partitioning
    Let partitions be partition_computation_graph(graph, num_threads)
    Let thread_results be List[Dictionary[String, Float]]
    
    Note: Process partitions in parallel
    For partition in partitions:
        Let partial_gradients be compute_partition_gradients(partition)
        Call thread_results.append(partial_gradients)
    
    Note: Merge results from all threads
    Let final_gradients be merge_parallel_gradients(thread_results)
    Return final_gradients
```

## Best Practices

### 1. Graph Construction Efficiency

```runa
Note: Minimize graph construction overhead
Process called "efficient_graph_builder" that takes estimated_nodes as Integer returns GraphBuilder:
    Let builder be GraphBuilder with:
        node_pool = create_object_pool(GraphNode, estimated_nodes)
        edge_pool = create_object_pool(GraphEdge, estimated_nodes * 2)
        hash_table = create_hash_table(estimated_nodes)
        
    Return builder
```

### 2. Numerical Stability

```runa
Note: Handle numerical edge cases in gradient computation
Process called "stable_softmax_backward" that takes output_grad as List[Float], softmax_output as List[Float] returns List[Float]:
    Note: Numerically stable softmax gradient computation
    Let n be softmax_output.size()
    Let input_grad be List[Float]
    
    For i from 0 to n - 1:
        Let grad_i be 0.0
        For j from 0 to n - 1:
            If i == j:
                Set grad_i to grad_i + output_grad[j] * softmax_output[i] * (1.0 - softmax_output[i])
            Otherwise:
                Set grad_i to grad_i - output_grad[j] * softmax_output[i] * softmax_output[j]
        Call input_grad.append(grad_i)
    
    Return input_grad
```

### 3. Memory-Efficient Training

```runa
Note: Gradient accumulation for large effective batch sizes
Process called "accumulate_gradients" that takes accumulated_grads as List[Float], new_grads as List[Float], accumulation_steps as Integer returns List[Float]:
    Let updated_grads be List[Float]
    For i from 0 to accumulated_grads.size() - 1:
        Let accumulated be accumulated_grads[i] + new_grads[i] / accumulation_steps
        Call updated_grads.append(accumulated)
    Return updated_grads
```

Reverse-mode automatic differentiation is the cornerstone of modern machine learning, providing efficient gradient computation for complex models with millions or billions of parameters. Its ability to compute full gradients in constant passes makes it indispensable for training deep neural networks and solving large-scale optimization problems.