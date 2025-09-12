# Sampling Methods

The Sampling Methods module (`math/probability/sampling`) provides comprehensive random sampling techniques including Monte Carlo methods, MCMC algorithms, and specialized sampling procedures for statistical computation and simulation.

## Overview

This module implements state-of-the-art sampling algorithms for generating random samples from probability distributions, enabling Monte Carlo estimation, simulation studies, and computational statistics.

## Key Features

### Random Number Generation
- **High-quality PRNGs**: Mersenne Twister, XORshift, PCG algorithms
- **Cryptographically secure RNGs**: For applications requiring unpredictability
- **Quasi-random sequences**: Low-discrepancy sequences for improved convergence
- **Parallel random streams**: Independent streams for parallel computation

### Basic Sampling Methods
- **Inverse Transform Sampling**: Using inverse CDFs for exact sampling
- **Rejection Sampling**: For complex distributions without closed-form inverses
- **Importance Sampling**: Variance reduction through importance weighting
- **Control Variates**: Using correlated variables to reduce variance

### Advanced Monte Carlo
- **Stratified Sampling**: Reducing variance through stratification
- **Latin Hypercube Sampling**: Space-filling designs for multidimensional sampling
- **Antithetic Variates**: Generating negatively correlated samples
- **Quasi-Monte Carlo**: Using low-discrepancy sequences

### MCMC Algorithms
- **Metropolis-Hastings**: General-purpose MCMC with adaptive proposals
- **Gibbs Sampling**: Coordinate-wise sampling for multivariate distributions
- **Slice Sampling**: Auxiliary variable methods for univariate sampling
- **Ensemble Methods**: Multiple chain algorithms like affine-invariant sampling

## Quick Start Example

```runa
Import "math/probability/sampling" as Sampling
Import "math/probability/distributions" as Distributions

Note: Basic random sampling
Let rng_config be Sampling.create_rng_config([
    ("algorithm", "mersenne_twister"),
    ("seed", 42),
    ("parallel_streams", 4)
])

Sampling.set_global_rng_config(rng_config)

Note: Sample from standard distributions
Let normal_samples be Sampling.normal(mean: 0.0, std_dev: 1.0, size: 1000)
Let exponential_samples be Sampling.exponential(rate: 2.0, size: 1000)
Let uniform_samples be Sampling.uniform(lower: 0.0, upper: 10.0, size: 1000)

Display "Generated samples:"
Display "  Normal mean: " joined with Sampling.sample_mean(normal_samples)
Display "  Normal std: " joined with Sampling.sample_std_dev(normal_samples)
Display "  Exponential mean: " joined with Sampling.sample_mean(exponential_samples)
Display "  Uniform mean: " joined with Sampling.sample_mean(uniform_samples)

Note: Monte Carlo estimation of π
Process called "unit_circle_indicator" that takes x as Float, y as Float returns Float:
    If x * x + y * y <= 1.0:
        Return 1.0
    Otherwise:
        Return 0.0

Let num_mc_samples be 1000000
Let inside_circle_count be 0.0

For i from 0 to num_mc_samples - 1:
    Let x be Sampling.uniform_single(-1.0, 1.0)
    Let y be Sampling.uniform_single(-1.0, 1.0)
    Set inside_circle_count to inside_circle_count + unit_circle_indicator(x, y)

Let pi_estimate be 4.0 * inside_circle_count / MathCore.int_to_float(num_mc_samples)
Let pi_error be MathCore.abs(pi_estimate - MathCore.get_pi())

Display "Monte Carlo π estimation:"
Display "  Estimate: " joined with pi_estimate
Display "  True value: " joined with MathCore.get_pi()
Display "  Error: " joined with pi_error
Display "  Samples used: " joined with num_mc_samples

Note: Importance sampling example
Process called "importance_target_function" that takes x as Float returns Float:
    Note: Target function: exp(-x²/2) for x in [0, 5]
    Return MathCore.exp(-x * x / 2.0)

Process called "importance_proposal_density" that takes x as Float returns Float:
    Note: Proposal: exponential(1) density for x > 0
    If x >= 0.0:
        Return MathCore.exp(-x)
    Otherwise:
        Return 0.0

Let importance_samples be Sampling.exponential(rate: 1.0, size: 10000)
Let importance_weights be create_empty_list()
Let weighted_sum be 0.0
Let weight_sum be 0.0

For x in importance_samples:
    If x <= 5.0:  Note: Only consider samples in [0, 5]
        Let target_value be importance_target_function(x)
        Let proposal_value be importance_proposal_density(x)
        Let weight be target_value / proposal_value
        
        Append weight to importance_weights
        Set weighted_sum to weighted_sum + x * weight
        Set weight_sum to weight_sum + weight

Let importance_estimate be weighted_sum / weight_sum
Display "Importance sampling estimate: " joined with importance_estimate

Note: Bootstrap resampling
Let original_data be normal_samples
Let bootstrap_means be create_empty_list()
Let num_bootstrap_samples be 1000

For bootstrap_iter from 0 to num_bootstrap_samples - 1:
    Let bootstrap_sample be Sampling.bootstrap_resample(original_data)
    Let bootstrap_mean be Sampling.sample_mean(bootstrap_sample)
    Append bootstrap_mean to bootstrap_means

Let bootstrap_mean_estimate be Sampling.sample_mean(bootstrap_means)
Let bootstrap_std_estimate be Sampling.sample_std_dev(bootstrap_means)
Let bootstrap_ci be Sampling.percentile_confidence_interval(bootstrap_means, confidence: 0.95)

Display "Bootstrap results:"
Display "  Mean estimate: " joined with bootstrap_mean_estimate
Display "  Standard error: " joined with bootstrap_std_estimate
Display "  95% CI: [" joined with bootstrap_ci.lower joined with ", " joined with bootstrap_ci.upper joined with "]"
```

## Advanced Features

### Rejection Sampling
```runa
Note: Implement rejection sampling for custom distribution
Process called "custom_target_density" that takes x as Float returns Float:
    Note: Custom distribution: mixture of two normals
    Let weight1 be 0.7
    Let weight2 be 0.3
    
    Let normal1_pdf be Distributions.pdf(
        Distributions.create_normal_distribution([("mean", -2.0), ("std_dev", 0.8)]), 
        x
    )
    Let normal2_pdf be Distributions.pdf(
        Distributions.create_normal_distribution([("mean", 3.0), ("std_dev", 1.2)]), 
        x
    )
    
    Return weight1 * normal1_pdf + weight2 * normal2_pdf

Process called "proposal_density" that takes x as Float returns Float:
    Note: Use wider normal as proposal
    Return Distributions.pdf(
        Distributions.create_normal_distribution([("mean", 0.0), ("std_dev", 4.0)]), 
        x
    )

Let rejection_config be Sampling.create_rejection_sampling_config([
    ("target_density", custom_target_density),
    ("proposal_density", proposal_density),
    ("proposal_sampler", Process called "proposal_sampler" that takes nothing returns Float:
        Return Sampling.normal_single(0.0, 4.0)
    ),
    ("envelope_constant", 2.0),  Note: Upper bound on target/proposal ratio
    ("max_attempts_per_sample", 100)
])

Let rejection_samples be Sampling.rejection_sample(rejection_config, num_samples: 5000)
Let acceptance_rate be Sampling.get_rejection_acceptance_rate(rejection_config)

Display "Rejection sampling results:"
Display "  Generated samples: " joined with rejection_samples.length()
Display "  Acceptance rate: " joined with (acceptance_rate * 100.0) joined with "%"
Display "  Sample mean: " joined with Sampling.sample_mean(rejection_samples)
Display "  Sample std: " joined with Sampling.sample_std_dev(rejection_samples)
```

### Adaptive MCMC
```runa
Note: Adaptive Metropolis algorithm
Type called "AdaptiveMCMCConfig":
    target_acceptance_rate as Float
    adaptation_interval as Integer
    initial_step_size as Float
    min_step_size as Float
    max_step_size as Float

Process called "adaptive_metropolis_univariate" that takes log_density as Process, initial_value as Float, config as AdaptiveMCMCConfig, num_samples as Integer returns MCMCResult:
    Let samples be create_empty_list()
    Let current_value be initial_value
    Let current_log_density be log_density(current_value)
    Let step_size be config.initial_step_size
    Let acceptance_count be 0
    
    For iteration from 0 to num_samples - 1:
        Note: Propose new state
        Let proposed_value be current_value + Sampling.normal_single(0.0, step_size)
        Let proposed_log_density be log_density(proposed_value)
        
        Note: Compute acceptance probability
        Let log_acceptance_ratio be proposed_log_density - current_log_density
        Let acceptance_probability be MathCore.min(1.0, MathCore.exp(log_acceptance_ratio))
        
        Note: Accept or reject
        Let random_uniform be Sampling.uniform_single(0.0, 1.0)
        If random_uniform <= acceptance_probability:
            Set current_value to proposed_value
            Set current_log_density to proposed_log_density
            Set acceptance_count to acceptance_count + 1
        
        Append current_value to samples
        
        Note: Adapt step size
        If iteration % config.adaptation_interval = 0 and iteration > 0:
            Let recent_acceptance_rate be MathCore.int_to_float(acceptance_count) / MathCore.int_to_float(config.adaptation_interval)
            
            If recent_acceptance_rate < config.target_acceptance_rate:
                Set step_size to MathCore.max(step_size * 0.9, config.min_step_size)
            Otherwise:
                Set step_size to MathCore.min(step_size * 1.1, config.max_step_size)
            
            Set acceptance_count to 0  Note: Reset for next adaptation window
    
    Return MCMCResult with 
        samples: samples, 
        final_step_size: step_size,
        total_acceptance_rate: MathCore.int_to_float(acceptance_count) / MathCore.int_to_float(num_samples)

Note: Example usage
Process called "example_log_density" that takes x as Float returns Float:
    Note: Log density of N(2, 1.5²)
    Let mean be 2.0
    Let std_dev be 1.5
    Let normalized_x be (x - mean) / std_dev
    Return -0.5 * normalized_x * normalized_x - MathCore.log(std_dev * MathCore.sqrt(2.0 * MathCore.get_pi()))

Let adaptive_config be AdaptiveMCMCConfig with
    target_acceptance_rate: 0.44,
    adaptation_interval: 100,
    initial_step_size: 1.0,
    min_step_size: 0.01,
    max_step_size: 10.0

Let adaptive_result be adaptive_metropolis_univariate(
    example_log_density,
    initial_value: 0.0,
    adaptive_config,
    num_samples: 10000
)

Let adaptive_samples be Sampling.get_mcmc_samples(adaptive_result)
Let final_step_size be Sampling.get_final_step_size(adaptive_result)
Let acceptance_rate be Sampling.get_acceptance_rate(adaptive_result)

Display "Adaptive MCMC results:"
Display "  Final step size: " joined with final_step_size
Display "  Acceptance rate: " joined with (acceptance_rate * 100.0) joined with "%"
Display "  Sample mean: " joined with Sampling.sample_mean(adaptive_samples)
Display "  Sample std: " joined with Sampling.sample_std_dev(adaptive_samples)
```

### Quasi-Monte Carlo
```runa
Note: Low-discrepancy sequence sampling
Let sobol_sequence be Sampling.create_sobol_sequence([
    ("dimension", 2),
    ("scrambling", True),
    ("seed", 12345)
])

Let halton_sequence be Sampling.create_halton_sequence([
    ("dimension", 2),
    ("bases", [2, 3])
])

Note: Compare Monte Carlo vs Quasi-Monte Carlo integration
Process called "test_integrand" that takes point as List[Float] returns Float:
    Let x be point[0]
    Let y be point[1]
    Return MathCore.exp(-(x * x + y * y))

Let mc_num_samples be 10000
Let qmc_num_samples be 1000

Note: Standard Monte Carlo
Let mc_sum be 0.0
For i from 0 to mc_num_samples - 1:
    Let random_point be [Sampling.uniform_single(0.0, 1.0), Sampling.uniform_single(0.0, 1.0)]
    Set mc_sum to mc_sum + test_integrand(random_point)

Let mc_estimate be mc_sum / MathCore.int_to_float(mc_num_samples)

Note: Quasi-Monte Carlo
Let qmc_sum be 0.0
For i from 0 to qmc_num_samples - 1:
    Let qmc_point be Sampling.next_sobol_point(sobol_sequence)
    Set qmc_sum to qmc_sum + test_integrand(qmc_point)

Let qmc_estimate be qmc_sum / MathCore.int_to_float(qmc_num_samples)

Note: True integral value (for comparison)
Let true_integral be MathCore.get_pi() / 4.0 * (1.0 - MathCore.exp(-1.0))

Display "Monte Carlo vs Quasi-Monte Carlo:"
Display "  True integral: " joined with true_integral
Display "  MC estimate (" joined with mc_num_samples joined with " samples): " joined with mc_estimate
Display "  MC error: " joined with MathCore.abs(mc_estimate - true_integral)
Display "  QMC estimate (" joined with qmc_num_samples joined with " samples): " joined with qmc_estimate
Display "  QMC error: " joined with MathCore.abs(qmc_estimate - true_integral)
Display "  QMC efficiency gain: " joined with 
    (MathCore.abs(mc_estimate - true_integral) / MathCore.abs(qmc_estimate - true_integral))
```

### Ensemble Sampling
```runa
Note: Affine-invariant ensemble sampler
Type called "EnsembleConfig":
    num_walkers as Integer
    stretch_parameter as Float
    num_steps as Integer
    burnin_steps as Integer

Process called "affine_invariant_sample" that takes log_probability as Process, initial_ensemble as List[List[Float]], config as EnsembleConfig returns EnsembleResult:
    Let num_walkers be config.num_walkers
    Let num_dimensions be initial_ensemble[0].length()
    Let current_ensemble be copy_ensemble(initial_ensemble)
    
    Let all_samples be create_empty_list()
    Let acceptance_counts be create_zero_list(num_walkers)
    
    For step from 0 to config.num_steps - 1:
        For walker_index from 0 to num_walkers - 1:
            Note: Choose random walker from complementary ensemble
            Let other_walker_index be Sampling.random_integer(0, num_walkers - 1)
            While other_walker_index = walker_index:
                Set other_walker_index to Sampling.random_integer(0, num_walkers - 1)
            
            Let current_position be current_ensemble[walker_index]
            Let other_position be current_ensemble[other_walker_index]
            
            Note: Generate stretch move
            Let z be generate_stretch_factor(config.stretch_parameter)
            Let proposed_position be create_empty_list()
            
            For dim from 0 to num_dimensions - 1:
                Let new_coord be other_position[dim] + z * (current_position[dim] - other_position[dim])
                Append new_coord to proposed_position
            
            Note: Compute acceptance probability
            Let current_log_prob be log_probability(current_position)
            Let proposed_log_prob be log_probability(proposed_position)
            Let log_acceptance_ratio be (MathCore.int_to_float(num_dimensions) - 1.0) * MathCore.log(z) + 
                proposed_log_prob - current_log_prob
            
            Let acceptance_probability be MathCore.min(1.0, MathCore.exp(log_acceptance_ratio))
            
            Note: Accept or reject
            Let random_uniform be Sampling.uniform_single(0.0, 1.0)
            If random_uniform <= acceptance_probability:
                Set current_ensemble[walker_index] to proposed_position
                Set acceptance_counts[walker_index] to acceptance_counts[walker_index] + 1
        
        Note: Store samples after burnin
        If step >= config.burnin_steps:
            Append copy_ensemble(current_ensemble) to all_samples
    
    Return EnsembleResult with 
        samples: all_samples,
        acceptance_rates: compute_acceptance_rates(acceptance_counts, config.num_steps)

Note: Example: sampling from multivariate normal
Process called "multivariate_normal_log_prob" that takes x as List[Float] returns Float:
    Note: Standard multivariate normal log probability
    Let sum_squares be 0.0
    For xi in x:
        Set sum_squares to sum_squares + xi * xi
    
    Let num_dims be MathCore.int_to_float(x.length())
    Return -0.5 * sum_squares - 0.5 * num_dims * MathCore.log(2.0 * MathCore.get_pi())

Note: Initialize ensemble
Let num_walkers be 20
Let num_dimensions be 5
Let initial_ensemble be create_empty_list()

For walker from 0 to num_walkers - 1:
    Let initial_position be create_empty_list()
    For dim from 0 to num_dimensions - 1:
        Append Sampling.normal_single(0.0, 2.0) to initial_position
    Append initial_position to initial_ensemble

Let ensemble_config be EnsembleConfig with
    num_walkers: num_walkers,
    stretch_parameter: 2.0,
    num_steps: 5000,
    burnin_steps: 1000

Let ensemble_result be affine_invariant_sample(
    multivariate_normal_log_prob,
    initial_ensemble,
    ensemble_config
)

Let ensemble_samples be Sampling.flatten_ensemble_samples(ensemble_result)
Let ensemble_acceptance_rates be Sampling.get_ensemble_acceptance_rates(ensemble_result)

Display "Ensemble sampling results:"
Display "  Total samples: " joined with ensemble_samples.length()
Display "  Mean acceptance rate: " joined with 
    (Sampling.sample_mean(ensemble_acceptance_rates) * 100.0) joined with "%"

For dim from 0 to num_dimensions - 1:
    Let dim_samples be Sampling.extract_dimension(ensemble_samples, dim)
    Let dim_mean be Sampling.sample_mean(dim_samples)
    Let dim_std be Sampling.sample_std_dev(dim_samples)
    
    Display "  Dimension " joined with dim joined with ": mean=" joined with dim_mean 
        joined with ", std=" joined with dim_std
```

## Performance Optimization

### Parallel Sampling
```runa
Note: Parallel independent sampling
Let parallel_config be Sampling.create_parallel_config([
    ("num_threads", 8),
    ("samples_per_thread", 10000),
    ("independent_seeds", True)
])

Let parallel_normal_samples be Sampling.parallel_normal(
    mean: 0.0,
    std_dev: 1.0,
    parallel_config
)

Display "Parallel sampling generated " joined with parallel_normal_samples.length() joined with " samples"

Note: Parallel MCMC chains
Let parallel_mcmc_config be Sampling.create_parallel_mcmc_config([
    ("num_chains", 4),
    ("samples_per_chain", 10000),
    ("different_starting_points", True)
])

Let parallel_mcmc_result be Sampling.parallel_adaptive_metropolis(
    example_log_density,
    parallel_mcmc_config
)

Let all_mcmc_samples be Sampling.combine_mcmc_chains(parallel_mcmc_result)
Let chain_diagnostics be Sampling.mcmc_chain_diagnostics(parallel_mcmc_result)

Display "Parallel MCMC results:"
Display "  Total samples: " joined with all_mcmc_samples.length()
Display "  R-hat diagnostic: " joined with Sampling.get_r_hat(chain_diagnostics)
Display "  Effective sample size: " joined with Sampling.get_effective_sample_size(chain_diagnostics)
```

### Memory-Efficient Sampling
```runa
Note: Streaming sampling for large datasets
Let streaming_sampler be Sampling.create_streaming_sampler([
    ("distribution", "normal"),
    ("parameters", [("mean", 0.0), ("std_dev", 1.0)]),
    ("buffer_size", 1000),
    ("total_samples", 1000000)
])

Let running_sum be 0.0
Let running_count be 0
Let sample_batches_processed be 0

Loop:
    Let sample_batch be Sampling.next_streaming_batch(streaming_sampler)
    If Sampling.is_stream_complete(sample_batch):
        Break
    
    Note: Process batch without storing all samples
    For sample in sample_batch:
        Set running_sum to running_sum + sample
        Set running_count to running_count + 1
    
    Set sample_batches_processed to sample_batches_processed + 1
    
    If sample_batches_processed % 100 = 0:
        Display "Processed " joined with running_count joined with " samples so far"

Let streaming_mean be running_sum / MathCore.int_to_float(running_count)
Display "Streaming sampling mean: " joined with streaming_mean
Display "Total samples processed: " joined with running_count
```

## Best Practices

### Random Number Generation
1. **Seed Management**: Use proper seeding for reproducibility
2. **Stream Independence**: Use independent streams for parallel computation
3. **Quality Assessment**: Periodically test RNG quality with statistical tests
4. **Cryptographic Security**: Use cryptographically secure RNGs when necessary

### Monte Carlo Methods
1. **Variance Reduction**: Implement importance sampling, control variates when beneficial
2. **Convergence Monitoring**: Monitor convergence of Monte Carlo estimates
3. **Sample Size**: Use adaptive sample sizes based on desired precision
4. **Stratification**: Use stratified sampling for improved efficiency

### MCMC Implementation
1. **Initialization**: Use overdispersed starting values for multiple chains
2. **Adaptation**: Implement adaptive tuning during burn-in period
3. **Diagnostics**: Always check convergence with multiple diagnostics
4. **Thinning**: Avoid unnecessary thinning (usually not beneficial)

This module provides the computational foundation for all sampling-based statistical methods, enabling efficient and reliable random sampling across scientific and engineering applications.