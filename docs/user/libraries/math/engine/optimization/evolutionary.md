# Evolutionary Optimization

The Evolutionary Optimization module (`math/engine/optimization/evolutionary`) provides population-based optimization algorithms inspired by natural evolution and swarm behavior.

## Overview

This module implements state-of-the-art evolutionary algorithms for global optimization, multi-objective optimization, and problems where gradient information is unavailable or unreliable.

## Key Algorithms

### Genetic Algorithms
- Selection methods (tournament, roulette, rank-based)
- Crossover operators (uniform, arithmetic, simulated binary)
- Mutation strategies (Gaussian, polynomial, differential)
- Niching and diversity preservation techniques

### Evolution Strategies
- (μ+λ) and (μ,λ) selection schemes  
- Self-adaptive parameter control
- Covariance Matrix Adaptation Evolution Strategy (CMA-ES)
- Natural Evolution Strategies (NES)

### Swarm Intelligence
- Particle Swarm Optimization (PSO)
- Ant Colony Optimization (ACO)
- Artificial Bee Colony (ABC)
- Firefly Algorithm and variants

### Multi-Objective Optimization
- NSGA-II and NSGA-III
- SPEA2 and MOEA/D
- Hypervolume-based algorithms
- Many-objective optimization methods

## Quick Start Example

```runa
Import "math/engine/optimization/evolutionary" as EvolutionaryOpt

Process called "rastrigin_function" that takes x as List[String] returns Float:
    Let sum be 0.0
    Let n be MathCore.int_to_float(x.length())
    
    For xi_str in x:
        Let xi be MathCore.parse_float(xi_str)
        Set sum to sum + xi * xi - 10.0 * MathCore.cos(2.0 * MathCore.get_pi() * xi)
    
    Return 10.0 * n + sum

Let ga_config be EvolutionaryOpt.create_genetic_algorithm_config([
    ("population_size", 100),
    ("generations", 500),
    ("crossover_rate", 0.8),
    ("mutation_rate", 0.1),
    ("selection_method", "tournament"),
    ("tournament_size", 3)
])

Let ga_result be EvolutionaryOpt.genetic_algorithm(
    rastrigin_function,
    dimension: 5,
    bounds: [(-5.12, 5.12)] * 5,
    ga_config
)

Let best_solution be EvolutionaryOpt.get_best_solution(ga_result)
Let best_fitness be EvolutionaryOpt.get_best_fitness(ga_result)

Display "GA Solution: " joined with vector_to_string(best_solution)
Display "Best fitness: " joined with best_fitness
```

## Best Practices

### Algorithm Selection
- **Genetic Algorithms**: Discrete optimization and combinatorial problems
- **Evolution Strategies**: Continuous optimization with self-adaptation
- **Particle Swarm**: Fast convergence on unimodal functions
- **Multi-objective methods**: Trade-off analysis and Pareto optimization

### Parameter Tuning
- Use adaptive parameter control when possible
- Balance exploration and exploitation
- Monitor population diversity
- Apply problem-specific knowledge in operators

This module provides robust global optimization capabilities for engineering design, machine learning hyperparameter tuning, and complex optimization landscapes.