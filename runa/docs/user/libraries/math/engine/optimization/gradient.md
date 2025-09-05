# Gradient-Based Methods

The Gradient-Based Methods module (`math/engine/optimization/gradient`) provides advanced first-order optimization algorithms that are particularly effective for machine learning, large-scale optimization, and problems where computing the Hessian is impractical.

## Overview

This module implements state-of-the-art gradient-based optimization methods, including momentum techniques, adaptive learning rate methods, and specialized algorithms for stochastic optimization scenarios common in machine learning.

## Key Algorithms

### Classical Gradient Descent

The foundation of all gradient-based methods, providing the basic framework for iterative optimization.

#### Basic Gradient Descent
```runa
Import "math/engine/optimization/gradient" as GradientOpt

Process called "rosenbrock_function" that takes x as List[String] returns Float:
    Let x1 be MathCore.parse_float(x[0])
    Let x2 be MathCore.parse_float(x[1])
    Let term1 be 100.0 * (x2 - x1 * x1) * (x2 - x1 * x1)
    Let term2 be (1.0 - x1) * (1.0 - x1)
    Return term1 + term2

Process called "rosenbrock_gradient" that takes x as List[String] returns List[String]:
    Let x1 be MathCore.parse_float(x[0])
    Let x2 be MathCore.parse_float(x[1])
    Let grad_x1 be -400.0 * x1 * (x2 - x1 * x1) - 2.0 * (1.0 - x1)
    Let grad_x2 be 200.0 * (x2 - x1 * x1)
    Return [MathCore.float_to_string(grad_x1), MathCore.float_to_string(grad_x2)]

Let gd_config be GradientOpt.create_gradient_descent_config([
    ("learning_rate", 0.001),
    ("tolerance", 1e-8),
    ("max_iterations", 10000)
])

Let gd_result be GradientOpt.gradient_descent(
    rosenbrock_function,
    rosenbrock_gradient,
    initial_point: ["-1.0", "1.0"],
    gd_config
)

Let gd_solution be GradientOpt.get_solution(gd_result)
Let gd_iterations be GradientOpt.get_iterations(gd_result)
Let final_gradient_norm be GradientOpt.get_final_gradient_norm(gd_result)

Display "Gradient Descent Solution: [" joined with gd_solution[0] 
    joined with ", " joined with gd_solution[1] joined with "]"
Display "Converged in " joined with gd_iterations joined with " iterations"
Display "Final gradient norm: " joined with final_gradient_norm
```

#### Gradient Descent with Line Search
```runa
Let gd_linesearch_config be GradientOpt.create_gd_linesearch_config([
    ("initial_step_size", 1.0),
    ("line_search_method", "armijo"),
    ("armijo_c1", 1e-4),
    ("backtrack_factor", 0.5),
    ("tolerance", 1e-8)
])

Let gd_ls_result be GradientOpt.gradient_descent_line_search(
    rosenbrock_function,
    rosenbrock_gradient,
    initial_point: ["-1.0", "1.0"],
    gd_linesearch_config
)

Let gd_ls_solution be GradientOpt.get_solution(gd_ls_result)
Let step_size_history be GradientOpt.get_step_size_history(gd_ls_result)

Display "GD with Line Search Solution: [" joined with gd_ls_solution[0] 
    joined with ", " joined with gd_ls_solution[1] joined with "]"
Display "Average step size: " joined with GradientOpt.average_step_size(step_size_history)
```

### Momentum Methods

Momentum methods accelerate convergence by accumulating velocity in consistent gradient directions.

#### Classical Momentum
```runa
Let momentum_config be GradientOpt.create_momentum_config([
    ("learning_rate", 0.01),
    ("momentum", 0.9),
    ("tolerance", 1e-8),
    ("max_iterations", 5000)
])

Let momentum_result be GradientOpt.gradient_descent_momentum(
    rosenbrock_function,
    rosenbrock_gradient,
    initial_point: ["-1.0", "1.0"],
    momentum_config
)

Let momentum_solution be GradientOpt.get_solution(momentum_result)
Let momentum_iterations be GradientOpt.get_iterations(momentum_result)
Let velocity_history be GradientOpt.get_velocity_history(momentum_result)

Display "Momentum Solution: [" joined with momentum_solution[0] 
    joined with ", " joined with momentum_solution[1] joined with "]"
Display "Converged in " joined with momentum_iterations joined with " iterations"

Note: Analyze momentum effectiveness
Let momentum_effectiveness be GradientOpt.analyze_momentum_effectiveness(momentum_result)
Display "Momentum acceleration factor: " joined with 
    GradientOpt.get_acceleration_factor(momentum_effectiveness)
```

#### Nesterov Accelerated Gradient
```runa
Let nesterov_config be GradientOpt.create_nesterov_config([
    ("learning_rate", 0.01),
    ("momentum", 0.9),
    ("tolerance", 1e-8),
    ("max_iterations", 5000)
])

Let nesterov_result be GradientOpt.nesterov_accelerated_gradient(
    rosenbrock_function,
    rosenbrock_gradient,
    initial_point: ["-1.0", "1.0"],
    nesterov_config
)

Let nesterov_solution be GradientOpt.get_solution(nesterov_result)
Let nesterov_iterations be GradientOpt.get_iterations(nesterov_result)

Display "Nesterov Solution: [" joined with nesterov_solution[0] 
    joined with ", " joined with nesterov_solution[1] joined with "]"
Display "Converged in " joined with nesterov_iterations joined with " iterations"

Note: Compare momentum methods
Let momentum_comparison be GradientOpt.compare_momentum_methods([momentum_result, nesterov_result])
Display "Better momentum method for this problem: " joined with 
    GradientOpt.get_better_method(momentum_comparison)
```

#### Heavy Ball Method
```runa
Let heavy_ball_config be GradientOpt.create_heavy_ball_config([
    ("learning_rate", 0.01),
    ("friction", 0.1),
    ("tolerance", 1e-8),
    ("max_iterations", 5000)
])

Let heavy_ball_result be GradientOpt.heavy_ball_method(
    rosenbrock_function,
    rosenbrock_gradient,
    initial_point: ["-1.0", "1.0"],
    heavy_ball_config
)

Let heavy_ball_solution be GradientOpt.get_solution(heavy_ball_result)
Display "Heavy Ball Solution: [" joined with heavy_ball_solution[0] 
    joined with ", " joined with heavy_ball_solution[1] joined with "]"
```

### Adaptive Learning Rate Methods

These methods automatically adjust learning rates based on the optimization history.

#### AdaGrad
```runa
Let adagrad_config be GradientOpt.create_adagrad_config([
    ("initial_learning_rate", 0.1),
    ("epsilon", 1e-8),
    ("tolerance", 1e-8),
    ("max_iterations", 5000)
])

Let adagrad_result be GradientOpt.adagrad(
    rosenbrock_function,
    rosenbrock_gradient,
    initial_point: ["-1.0", "1.0"],
    adagrad_config
)

Let adagrad_solution be GradientOpt.get_solution(adagrad_result)
Let adagrad_learning_rates be GradientOpt.get_adaptive_learning_rates(adagrad_result)

Display "AdaGrad Solution: [" joined with adagrad_solution[0] 
    joined with ", " joined with adagrad_solution[1] joined with "]"
Display "Final learning rates: [" joined with adagrad_learning_rates[0] 
    joined with ", " joined with adagrad_learning_rates[1] joined with "]"
```

#### RMSprop
```runa
Let rmsprop_config be GradientOpt.create_rmsprop_config([
    ("learning_rate", 0.01),
    ("decay_rate", 0.9),
    ("epsilon", 1e-8),
    ("tolerance", 1e-8),
    ("max_iterations", 5000)
])

Let rmsprop_result be GradientOpt.rmsprop(
    rosenbrock_function,
    rosenbrock_gradient,
    initial_point: ["-1.0", "1.0"],
    rmsprop_config
)

Let rmsprop_solution be GradientOpt.get_solution(rmsprop_result)
Let rmsprop_iterations be GradientOpt.get_iterations(rmsprop_result)

Display "RMSprop Solution: [" joined with rmsprop_solution[0] 
    joined with ", " joined with rmsprop_solution[1] joined with "]"
Display "Converged in " joined with rmsprop_iterations joined with " iterations"
```

#### Adam Optimizer
```runa
Let adam_config be GradientOpt.create_adam_config([
    ("learning_rate", 0.01),
    ("beta1", 0.9),      Note: First moment decay rate
    ("beta2", 0.999),    Note: Second moment decay rate
    ("epsilon", 1e-8),
    ("tolerance", 1e-8),
    ("max_iterations", 5000)
])

Let adam_result be GradientOpt.adam(
    rosenbrock_function,
    rosenbrock_gradient,
    initial_point: ["-1.0", "1.0"],
    adam_config
)

Let adam_solution be GradientOpt.get_solution(adam_result)
Let adam_iterations be GradientOpt.get_iterations(adam_result)
Let first_moments be GradientOpt.get_first_moments(adam_result)
Let second_moments be GradientOpt.get_second_moments(adam_result)

Display "Adam Solution: [" joined with adam_solution[0] 
    joined with ", " joined with adam_solution[1] joined with "]"
Display "Converged in " joined with adam_iterations joined with " iterations"
Display "Final first moments: [" joined with first_moments[0] 
    joined with ", " joined with first_moments[1] joined with "]"
```

#### AdaMax
```runa
Let adamax_config be GradientOpt.create_adamax_config([
    ("learning_rate", 0.002),
    ("beta1", 0.9),
    ("beta2", 0.999),
    ("tolerance", 1e-8),
    ("max_iterations", 5000)
])

Let adamax_result be GradientOpt.adamax(
    rosenbrock_function,
    rosenbrock_gradient,
    initial_point: ["-1.0", "1.0"],
    adamax_config
)

Let adamax_solution be GradientOpt.get_solution(adamax_result)
Display "AdaMax Solution: [" joined with adamax_solution[0] 
    joined with ", " joined with adamax_solution[1] joined with "]"
```

#### Nadam (Nesterov + Adam)
```runa
Let nadam_config be GradientOpt.create_nadam_config([
    ("learning_rate", 0.01),
    ("beta1", 0.9),
    ("beta2", 0.999),
    ("epsilon", 1e-8),
    ("schedule_decay", 0.004),
    ("tolerance", 1e-8),
    ("max_iterations", 5000)
])

Let nadam_result be GradientOpt.nadam(
    rosenbrock_function,
    rosenbrock_gradient,
    initial_point: ["-1.0", "1.0"],
    nadam_config
)

Let nadam_solution be GradientOpt.get_solution(nadam_result)
Display "Nadam Solution: [" joined with nadam_solution[0] 
    joined with ", " joined with nadam_solution[1] joined with "]"

Note: Compare adaptive methods
Let adaptive_comparison be GradientOpt.compare_adaptive_methods([
    adagrad_result, rmsprop_result, adam_result, adamax_result, nadam_result
])

Display "Best adaptive method: " joined with GradientOpt.get_best_adaptive_method(adaptive_comparison)
Display "Convergence speed ranking: " joined with 
    GradientOpt.get_convergence_ranking(adaptive_comparison)
```

### Coordinate Descent Methods

These methods optimize one coordinate (or block of coordinates) at a time.

#### Cyclic Coordinate Descent
```runa
Let cyclic_cd_config be GradientOpt.create_coordinate_descent_config([
    ("coordinate_selection", "cyclic"),
    ("line_search_1d", "golden_section"),
    ("tolerance", 1e-8),
    ("max_iterations", 10000)
])

Let cyclic_cd_result be GradientOpt.coordinate_descent(
    rosenbrock_function,
    coordinates: 2,
    initial_point: ["-1.0", "1.0"],
    cyclic_cd_config
)

Let cd_solution be GradientOpt.get_solution(cyclic_cd_result)
Let cd_coordinate_updates be GradientOpt.get_coordinate_update_history(cyclic_cd_result)

Display "Cyclic Coordinate Descent Solution: [" joined with cd_solution[0] 
    joined with ", " joined with cd_solution[1] joined with "]"
Display "Total coordinate updates: " joined with GradientOpt.count_coordinate_updates(cd_coordinate_updates)
```

#### Random Coordinate Descent
```runa
Let random_cd_config be GradientOpt.create_coordinate_descent_config([
    ("coordinate_selection", "random"),
    ("probability_distribution", "uniform"),
    ("tolerance", 1e-8),
    ("max_iterations", 10000)
])

Let random_cd_result be GradientOpt.coordinate_descent(
    rosenbrock_function,
    coordinates: 2,
    initial_point: ["-1.0", "1.0"],
    random_cd_config
)

Let random_cd_solution be GradientOpt.get_solution(random_cd_result)
Display "Random Coordinate Descent Solution: [" joined with random_cd_solution[0] 
    joined with ", " joined with random_cd_solution[1] joined with "]"
```

#### Block Coordinate Descent
```runa
Process called "block_separable_function" that takes x as List[String] returns Float:
    Note: Function separable in blocks of variables
    Let block1_sum be 0.0
    Let block2_sum be 0.0
    
    For i from 0 to 1:  Note: First block: x[0], x[1]
        Let xi be MathCore.parse_float(x[i])
        Set block1_sum to block1_sum + xi * xi
    
    For i from 2 to 3:  Note: Second block: x[2], x[3]
        Let xi be MathCore.parse_float(x[i])
        Set block2_sum to block2_sum + (xi - 1.0) * (xi - 1.0)
    
    Return block1_sum + block2_sum

Let block_cd_config be GradientOpt.create_block_coordinate_descent_config([
    ("block_structure", [[0, 1], [2, 3]]),
    ("block_solver", "conjugate_gradient"),
    ("tolerance", 1e-8),
    ("max_iterations", 1000)
])

Let block_cd_result be GradientOpt.block_coordinate_descent(
    block_separable_function,
    initial_point: ["2.0", "2.0", "0.0", "0.0"],
    block_cd_config
)

Let block_cd_solution be GradientOpt.get_solution(block_cd_result)
Display "Block Coordinate Descent Solution: " joined with vector_to_string(block_cd_solution)
```

### Stochastic Gradient Methods

Essential for machine learning and large-scale optimization problems.

#### Stochastic Gradient Descent (SGD)
```runa
Process called "stochastic_objective" that takes x as List[String], sample_indices as List[Integer] returns Float:
    Note: Mini-batch objective computation
    Let total_loss be 0.0
    
    For index in sample_indices:
        Note: Compute loss for sample 'index'
        Let sample_data be get_sample_data(index)
        Let sample_loss be compute_sample_loss(x, sample_data)
        Set total_loss to total_loss + sample_loss
    
    Return total_loss / MathCore.int_to_float(sample_indices.length())

Process called "stochastic_gradient" that takes x as List[String], sample_indices as List[Integer] returns List[String]:
    Note: Mini-batch gradient computation
    Let gradient_accumulator be initialize_gradient(x.length())
    
    For index in sample_indices:
        Let sample_data be get_sample_data(index)
        Let sample_grad be compute_sample_gradient(x, sample_data)
        Set gradient_accumulator to add_gradient(gradient_accumulator, sample_grad)
    
    Return scale_gradient(gradient_accumulator, 1.0 / MathCore.int_to_float(sample_indices.length()))

Let sgd_config be GradientOpt.create_sgd_config([
    ("initial_learning_rate", 0.01),
    ("learning_rate_schedule", "polynomial_decay"),
    ("decay_power", 1.0),
    ("batch_size", 32),
    ("epochs", 100),
    ("shuffle_data", True)
])

Let sgd_result be GradientOpt.stochastic_gradient_descent(
    stochastic_objective,
    stochastic_gradient,
    initial_point: ["0.0", "0.0"],
    dataset_size: 1000,
    sgd_config
)

Let sgd_solution be GradientOpt.get_sgd_solution(sgd_result)
Let training_loss_history be GradientOpt.get_training_loss_history(sgd_result)

Display "SGD Solution: [" joined with sgd_solution[0] 
    joined with ", " joined with sgd_solution[1] joined with "]"
Display "Final training loss: " joined with 
    GradientOpt.get_final_training_loss(training_loss_history)
```

#### SGD with Momentum
```runa
Let sgd_momentum_config be GradientOpt.create_sgd_momentum_config([
    ("learning_rate", 0.01),
    ("momentum", 0.9),
    ("batch_size", 32),
    ("epochs", 100),
    ("nesterov", True)
])

Let sgd_momentum_result be GradientOpt.sgd_with_momentum(
    stochastic_objective,
    stochastic_gradient,
    initial_point: ["0.0", "0.0"],
    dataset_size: 1000,
    sgd_momentum_config
)

Let sgd_momentum_solution be GradientOpt.get_sgd_solution(sgd_momentum_result)
Display "SGD with Momentum Solution: [" joined with sgd_momentum_solution[0] 
    joined with ", " joined with sgd_momentum_solution[1] joined with "]"
```

#### AdamW (Adam with Weight Decay)
```runa
Let adamw_config be GradientOpt.create_adamw_config([
    ("learning_rate", 0.001),
    ("beta1", 0.9),
    ("beta2", 0.999),
    ("weight_decay", 0.01),
    ("epsilon", 1e-8),
    ("batch_size", 32),
    ("epochs", 100)
])

Let adamw_result be GradientOpt.adamw(
    stochastic_objective,
    stochastic_gradient,
    initial_point: ["0.0", "0.0"],
    dataset_size: 1000,
    adamw_config
)

Let adamw_solution be GradientOpt.get_sgd_solution(adamw_result)
Display "AdamW Solution: [" joined with adamw_solution[0] 
    joined with ", " joined with adamw_solution[1] joined with "]"
```

### Variance Reduction Methods

Advanced stochastic methods that reduce the variance of gradient estimates.

#### SVRG (Stochastic Variance Reduced Gradient)
```runa
Let svrg_config be GradientOpt.create_svrg_config([
    ("inner_loop_length", 100),
    ("learning_rate", 0.01),
    ("full_gradient_frequency", 1),  Note: Every epoch
    ("epochs", 50)
])

Let svrg_result be GradientOpt.svrg(
    stochastic_objective,
    stochastic_gradient,
    full_gradient_function,  Note: Function to compute full gradient
    initial_point: ["0.0", "0.0"],
    dataset_size: 1000,
    svrg_config
)

Let svrg_solution be GradientOpt.get_svrg_solution(svrg_result)
Let variance_reduction_ratio be GradientOpt.get_variance_reduction_ratio(svrg_result)

Display "SVRG Solution: [" joined with svrg_solution[0] 
    joined with ", " joined with svrg_solution[1] joined with "]"
Display "Variance reduction: " joined with (variance_reduction_ratio * 100.0) joined with "%"
```

#### SAGA
```runa
Let saga_config be GradientOpt.create_saga_config([
    ("learning_rate", 0.01),
    ("table_update_probability", 1.0),
    ("epochs", 50)
])

Let saga_result be GradientOpt.saga(
    stochastic_objective,
    stochastic_gradient,
    initial_point: ["0.0", "0.0"],
    dataset_size: 1000,
    saga_config
)

Let saga_solution be GradientOpt.get_saga_solution(saga_result)
Display "SAGA Solution: [" joined with saga_solution[0] 
    joined with ", " joined with saga_solution[1] joined with "]"

Note: Compare variance reduction methods
Let variance_comparison be GradientOpt.compare_variance_reduction_methods([svrg_result, saga_result])
Display "Better variance reduction method: " joined with 
    GradientOpt.get_better_variance_method(variance_comparison)
```

## Advanced Features

### Learning Rate Scheduling

```runa
Note: Various learning rate decay strategies
Let lr_scheduler_config be GradientOpt.create_lr_scheduler_config([
    ("schedule_type", "cosine_annealing"),
    ("initial_lr", 0.1),
    ("min_lr", 1e-6),
    ("T_max", 1000),  Note: Maximum iterations for cosine cycle
    ("warmup_steps", 100)
])

Let scheduled_result be GradientOpt.gradient_descent_with_schedule(
    rosenbrock_function,
    rosenbrock_gradient,
    initial_point: ["-1.0", "1.0"],
    lr_scheduler_config
)

Let lr_history be GradientOpt.get_learning_rate_history(scheduled_result)
Let scheduled_solution be GradientOpt.get_solution(scheduled_result)

Display "Scheduled GD Solution: [" joined with scheduled_solution[0] 
    joined with ", " joined with scheduled_solution[1] joined with "]"

Note: Visualize learning rate schedule
Let lr_analysis be GradientOpt.analyze_lr_schedule(lr_history)
Display "Average learning rate: " joined with GradientOpt.get_average_lr(lr_analysis)
Display "LR decay factor: " joined with GradientOpt.get_decay_factor(lr_analysis)
```

### Gradient Clipping

```runa
Note: Prevent exploding gradients
Let gradient_clipping_config be GradientOpt.create_gradient_clipping_config([
    ("clipping_method", "norm"),
    ("max_gradient_norm", 1.0),
    ("clip_value", 0.5)  Note: For value-based clipping
])

Let clipped_result be GradientOpt.gradient_descent_with_clipping(
    rosenbrock_function,
    rosenbrock_gradient,
    initial_point: ["-1.0", "1.0"],
    gradient_descent_config: gd_config,
    clipping_config: gradient_clipping_config
)

Let clipped_solution be GradientOpt.get_solution(clipped_result)
Let gradient_norms = GradientOpt.get_gradient_norm_history(clipped_result)
Let clipping_events be GradientOpt.get_clipping_events(clipped_result)

Display "Gradient Clipped Solution: [" joined with clipped_solution[0] 
    joined with ", " joined with clipped_solution[1] joined with "]"
Display "Gradient clipping occurred " joined with GradientOpt.count_clipping_events(clipping_events) 
    joined with " times"
```

### Natural Gradient Methods

```runa
Process called "fisher_information_matrix" that takes x as List[String] returns List[List[String]]:
    Note: Compute Fisher information matrix for natural gradient
    Note: This is problem-specific - here's a simple example
    Let dim be x.length()
    Let fisher be create_identity_matrix(dim)
    
    Note: Modify based on the statistical model
    For i from 0 to dim - 1:
        For j from 0 to dim - 1:
            If i = j:
                Set fisher[i][j] to "2.0"  Note: Diagonal dominance
            Otherwise:
                Set fisher[i][j] to "0.1"  Note: Small off-diagonal terms
    
    Return fisher

Let natural_gradient_config be GradientOpt.create_natural_gradient_config([
    ("learning_rate", 0.1),
    ("regularization", 1e-6),  Note: Fisher matrix regularization
    ("tolerance", 1e-8),
    ("max_iterations", 5000)
])

Let natural_gradient_result be GradientOpt.natural_gradient_descent(
    rosenbrock_function,
    rosenbrock_gradient,
    fisher_information_matrix,
    initial_point: ["-1.0", "1.0"],
    natural_gradient_config
)

Let natural_solution be GradientOpt.get_solution(natural_gradient_result)
Display "Natural Gradient Solution: [" joined with natural_solution[0] 
    joined with ", " joined with natural_solution[1] joined with "]"

Note: Compare with standard gradient descent
Let convergence_comparison be GradientOpt.compare_convergence_rates([gd_result, natural_gradient_result])
Display "Natural gradient speedup: " joined with 
    GradientOpt.get_speedup_factor(convergence_comparison) joined with "x"
```

### Proximal Gradient Methods

```runa
Process called "l1_proximal_operator" that takes x as List[String], lambda as Float returns List[String]:
    Note: Soft thresholding for L1 regularization
    Let result be create_empty_list()
    
    For xi_str in x:
        Let xi be MathCore.parse_float(xi_str)
        Let proximal_value be soft_threshold(xi, lambda)
        Append MathCore.float_to_string(proximal_value) to result
    
    Return result

Process called "soft_threshold" that takes x as Float, lambda as Float returns Float:
    If x > lambda:
        Return x - lambda
    Otherwise If x < -lambda:
        Return x + lambda
    Otherwise:
        Return 0.0

Let proximal_config be GradientOpt.create_proximal_gradient_config([
    ("learning_rate", 0.01),
    ("regularization_parameter", 0.1),
    ("tolerance", 1e-8),
    ("max_iterations", 5000)
])

Let proximal_result be GradientOpt.proximal_gradient_descent(
    rosenbrock_function,
    rosenbrock_gradient,
    l1_proximal_operator,
    initial_point: ["-1.0", "1.0"],
    proximal_config
)

Let proximal_solution be GradientOpt.get_solution(proximal_result)
Let sparsity_level be GradientOpt.compute_sparsity(proximal_solution)

Display "Proximal Gradient Solution: [" joined with proximal_solution[0] 
    joined with ", " joined with proximal_solution[1] joined with "]"
Display "Solution sparsity: " joined with (sparsity_level * 100.0) joined with "%"
```

### Mirror Descent

```runa
Process called "entropy_mirror_map" that takes x as List[String] returns List[String]:
    Note: Logarithmic mirror map for probability simplex
    Let result be create_empty_list()
    
    For xi_str in x:
        Let xi be MathCore.parse_float(xi_str)
        Let mapped_value be MathCore.log(MathCore.max(xi, 1e-10))  Note: Avoid log(0)
        Append MathCore.float_to_string(mapped_value) to result
    
    Return result

Process called "entropy_mirror_map_gradient" that takes x as List[String] returns List[String]:
    Note: Gradient of the mirror map
    Let result be create_empty_list()
    
    For xi_str in x:
        Let xi be MathCore.parse_float(xi_str)
        Let gradient_value be 1.0 / MathCore.max(xi, 1e-10)
        Append MathCore.float_to_string(gradient_value) to result
    
    Return result

Let mirror_descent_config be GradientOpt.create_mirror_descent_config([
    ("learning_rate", 0.1),
    ("tolerance", 1e-8),
    ("max_iterations", 5000),
    ("projection_method", "simplex")
])

Let mirror_descent_result be GradientOpt.mirror_descent(
    rosenbrock_function,
    rosenbrock_gradient,
    entropy_mirror_map,
    entropy_mirror_map_gradient,
    initial_point: ["0.6", "0.4"],  Note: Starting on probability simplex
    mirror_descent_config
)

Let mirror_solution be GradientOpt.get_solution(mirror_descent_result)
Display "Mirror Descent Solution: [" joined with mirror_solution[0] 
    joined with ", " joined with mirror_solution[1] joined with "]"

Note: Verify simplex constraint
Let simplex_sum be MathCore.parse_float(mirror_solution[0]) + MathCore.parse_float(mirror_solution[1])
Display "Simplex constraint satisfied: " joined with (MathCore.abs(simplex_sum - 1.0) < 1e-6)
```

## Performance Analysis and Comparison

### Method Comparison Framework
```runa
Note: Comprehensive comparison of gradient methods
Let comparison_suite be GradientOpt.create_comparison_suite([
    ("test_functions", ["rosenbrock", "quadratic", "rastrigin"]),
    ("dimensions", [2, 10, 50]),
    ("noise_levels", [0.0, 0.01, 0.1]),
    ("performance_metrics", ["iterations", "function_evaluations", "final_error"])
])

Let methods_to_compare be [
    ("gradient_descent", gd_config),
    ("momentum", momentum_config), 
    ("adam", adam_config),
    ("rmsprop", rmsprop_config),
    ("lbfgs", lbfgs_config)
]

Let comparison_results be GradientOpt.run_method_comparison(
    comparison_suite,
    methods_to_compare
)

Let performance_summary be GradientOpt.summarize_performance(comparison_results)
Display "Performance Summary:"
Display "Fastest convergence: " joined with GradientOpt.get_fastest_method(performance_summary)
Display "Most robust to noise: " joined with GradientOpt.get_most_robust_method(performance_summary)
Display "Best for high dimensions: " joined with GradientOpt.get_best_high_dim_method(performance_summary)
```

### Convergence Analysis
```runa
Note: Detailed convergence analysis
Let convergence_analyzer be GradientOpt.create_convergence_analyzer([
    ("analyze_rates", True),
    ("detect_oscillations", True),
    ("measure_stagnation", True),
    ("estimate_condition_effects", True)
])

Let detailed_analysis be GradientOpt.analyze_convergence_behavior(
    adam_result,
    convergence_analyzer
)

Let convergence_rate be GradientOpt.get_convergence_rate(detailed_analysis)
Let oscillation_detected be GradientOpt.has_oscillations(detailed_analysis)
Let condition_effects be GradientOpt.get_conditioning_effects(detailed_analysis)

Display "Adam convergence rate: " joined with convergence_rate
Display "Oscillatory behavior: " joined with oscillation_detected
Display "Condition number effects: " joined with GradientOpt.describe_conditioning_effects(condition_effects)
```

## Error Handling and Robustness

### Numerical Stability
```runa
Note: Handle numerical issues in gradient methods
Let robust_gradient_config be GradientOpt.create_robust_config([
    ("gradient_tolerance", 1e-6),
    ("step_size_bounds", [1e-12, 1e2]),
    ("nan_detection", True),
    ("inf_detection", True),
    ("recovery_strategy", "restart_with_smaller_step")
])

Let robust_result be GradientOpt.robust_gradient_descent(
    rosenbrock_function,
    rosenbrock_gradient,
    initial_point: ["-1.0", "1.0"],
    robust_gradient_config
)

If GradientOpt.optimization_successful(robust_result):
    Let robust_solution be GradientOpt.get_robust_solution(robust_result)
    Let recovery_events be GradientOpt.get_recovery_events(robust_result)
    
    Display "Robust optimization successful: " joined with vector_to_string(robust_solution)
    Display "Recovery events: " joined with GradientOpt.count_recovery_events(recovery_events)
Otherwise:
    Let failure_diagnosis be GradientOpt.diagnose_failure(robust_result)
    Display "Optimization failed: " joined with GradientOpt.get_failure_reason(failure_diagnosis)
```

### Adaptive Hyperparameter Tuning
```runa
Note: Automatically tune hyperparameters during optimization
Let adaptive_tuning_config be GradientOpt.create_adaptive_tuning_config([
    ("tune_learning_rate", True),
    ("tune_momentum", True),
    ("adaptation_frequency", 100),  Note: Tune every 100 iterations
    ("performance_window", 50),     Note: Look at last 50 iterations
    ("tuning_strategy", "bayesian_optimization")
])

Let adaptive_result be GradientOpt.adaptive_gradient_descent(
    rosenbrock_function,
    rosenbrock_gradient,
    initial_point: ["-1.0", "1.0"],
    base_config: momentum_config,
    tuning_config: adaptive_tuning_config
)

Let adaptive_solution be GradientOpt.get_adaptive_solution(adaptive_result)
Let hyperparameter_history be GradientOpt.get_hyperparameter_history(adaptive_result)

Display "Adaptive solution: " joined with vector_to_string(adaptive_solution)
Display "Final learning rate: " joined with GradientOpt.get_final_learning_rate(hyperparameter_history)
Display "Final momentum: " joined with GradientOpt.get_final_momentum(hyperparameter_history)
```

## Best Practices

### Method Selection Guidelines

1. **For Convex Problems**:
   - Use accelerated methods (Nesterov) for smooth convex functions
   - Use AdaGrad for sparse gradients
   - Consider conjugate gradient for quadratic functions

2. **For Non-Convex Problems**:
   - Adam or RMSprop for general non-convex optimization
   - SGD with momentum for deep learning applications
   - L-BFGS for batch optimization with moderate dimensions

3. **For Stochastic Settings**:
   - SGD with momentum for large datasets
   - Adam/AdamW for neural network training
   - SVRG/SAGA for finite-sum problems

4. **For Constrained Problems**:
   - Projected gradient methods for simple constraints
   - Proximal gradient for composite objectives
   - Mirror descent for probability simplex constraints

### Performance Optimization Tips

- **Learning Rate**: Start with adaptive methods (Adam) for automatic tuning
- **Batch Size**: Use larger batches for more stable gradients, smaller for faster updates
- **Momentum**: Higher momentum (0.9-0.99) for smooth loss surfaces
- **Regularization**: Add weight decay to prevent overfitting in ML applications

### Convergence Monitoring

- Monitor both objective values and gradient norms
- Use validation metrics for early stopping in ML
- Implement learning rate scheduling for better convergence
- Apply gradient clipping to prevent instability

This module provides comprehensive gradient-based optimization capabilities suitable for machine learning, scientific computing, and engineering applications, with robust implementations and extensive diagnostic tools.