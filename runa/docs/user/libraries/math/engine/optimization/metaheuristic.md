# Metaheuristic Methods

The Metaheuristic Methods module (`math/engine/optimization/metaheuristic`) provides advanced global optimization algorithms that combine local search with global exploration strategies.

## Overview

This module implements sophisticated metaheuristic algorithms for complex optimization problems with multiple local optima, discrete variables, and challenging constraint landscapes.

## Key Algorithms

### Simulated Annealing
- Adaptive cooling schedules (geometric, logarithmic, adaptive)
- Neighborhood structures and move operators
- Reheating and restart strategies
- Parallel simulated annealing variants

### Tabu Search
- Short-term and long-term memory structures
- Aspiration criteria and tabu tenure management
- Intensification and diversification strategies
- Reactive tabu search with parameter adaptation

### Variable Neighborhood Search
- Variable neighborhood descent (VND)
- Variable neighborhood search (VNS)
- General variable neighborhood search (GVNS)
- Skewed variable neighborhood search

### Hybrid Methods
- Memetic algorithms combining evolution and local search
- Greedy randomized adaptive search procedures (GRASP)
- Iterated local search with perturbation operators
- Multi-start local search with clustering

## Quick Start Example

```runa
Import "math/engine/optimization/metaheuristic" as MetaOpt

Process called "ackley_function" that takes x as List[String] returns Float:
    Let n be MathCore.int_to_float(x.length())
    Let sum_sq be 0.0
    Let sum_cos be 0.0
    
    For xi_str in x:
        Let xi be MathCore.parse_float(xi_str)
        Set sum_sq to sum_sq + xi * xi
        Set sum_cos to sum_cos + MathCore.cos(2.0 * MathCore.get_pi() * xi)
    
    Let term1 be -20.0 * MathCore.exp(-0.2 * MathCore.sqrt(sum_sq / n))
    Let term2 be -MathCore.exp(sum_cos / n)
    
    Return term1 + term2 + 20.0 + MathCore.get_e()

Let sa_config be MetaOpt.create_simulated_annealing_config([
    ("initial_temperature", 100.0),
    ("cooling_schedule", "adaptive"),
    ("cooling_rate", 0.95),
    ("min_temperature", 1e-6),
    ("max_iterations", 10000)
])

Let sa_result be MetaOpt.simulated_annealing(
    ackley_function,
    dimension: 10,
    bounds: [(-32.768, 32.768)] * 10,
    sa_config
)

Let sa_solution be MetaOpt.get_sa_solution(sa_result)
Let sa_value be MetaOpt.get_sa_value(sa_result)

Display "Simulated Annealing Solution: " joined with vector_to_string(sa_solution)
Display "Best value: " joined with sa_value
```

## Best Practices

### Algorithm Selection
- **Simulated Annealing**: Single-objective problems with continuous variables
- **Tabu Search**: Combinatorial optimization and discrete problems
- **Variable Neighborhood Search**: Problems with natural neighborhood structures
- **Hybrid Methods**: Complex problems requiring both global and local search

### Parameter Tuning
- Use adaptive parameter control mechanisms
- Balance intensification and diversification
- Implement effective stopping criteria
- Monitor search progress and adjust strategies

This module provides powerful global optimization tools for complex engineering problems, combinatorial optimization, and multi-modal function optimization.