# Bayesian Methods

The Bayesian Methods module (`math/probability/bayesian`) provides comprehensive Bayesian statistical inference capabilities including MCMC sampling, variational inference, model selection, and hierarchical modeling for principled uncertainty quantification.

## Overview

This module implements state-of-the-art Bayesian methods for statistical modeling, enabling full uncertainty quantification and principled decision-making under uncertainty.

## Key Features

### Bayesian Inference
- **Prior and Posterior Distributions**: Comprehensive prior specification and posterior computation
- **Conjugate Analysis**: Analytical posterior computation for conjugate prior-likelihood pairs
- **Non-conjugate Methods**: Numerical methods for complex posterior distributions
- **Credible Intervals**: Bayesian confidence intervals and highest density regions

### MCMC Sampling
- **Metropolis-Hastings**: Adaptive and specialized MH algorithms
- **Gibbs Sampling**: Systematic and random scan Gibbs samplers
- **Hamiltonian Monte Carlo**: Efficient sampling with gradient information
- **No-U-Turn Sampler (NUTS)**: Automatic tuning of HMC parameters

### Variational Inference
- **Mean-Field Approximation**: Factorized variational distributions
- **Structured Approximations**: Maintaining correlation structure in approximations
- **Automatic Differentiation Variational Inference (ADVI)**: Black-box variational inference
- **Normalizing Flows**: Flexible variational distributions

### Model Selection
- **Bayes Factors**: Model comparison using marginal likelihoods
- **Information Criteria**: WAIC, PSIS-LOO, and other Bayesian information criteria  
- **Cross-Validation**: Bayesian cross-validation for model assessment
- **Model Averaging**: Bayesian model averaging and ensemble methods

## Quick Start Example

```runa
Import "math/probability/bayesian" as Bayesian
Import "math/probability/distributions" as Distributions
Import "math/probability/sampling" as Sampling

Note: Bayesian linear regression example
Let observed_x be [-2.0, -1.0, 0.0, 1.0, 2.0, 3.0]
Let observed_y be [1.2, 2.8, 3.1, 5.9, 7.8, 9.2]

Note: Define Bayesian linear model: y = α + βx + ε, ε ~ N(0,σ²)
Type called "LinearRegressionPriors":
    alpha_prior as Distribution
    beta_prior as Distribution  
    sigma_prior as Distribution

Let priors be LinearRegressionPriors with
    alpha_prior: Distributions.create_normal_distribution([("mean", 0.0), ("std_dev", 10.0)]),
    beta_prior: Distributions.create_normal_distribution([("mean", 0.0), ("std_dev", 10.0)]),
    sigma_prior: Distributions.create_inverse_gamma_distribution([("shape", 2.0), ("scale", 1.0)])

Note: Define likelihood function
Process called "linear_regression_log_likelihood" that takes params as Dictionary[String, Float], data as Dictionary[String, List[Float]] returns Float:
    Let alpha be params["alpha"]
    Let beta be params["beta"]
    Let sigma be params["sigma"]
    Let x_data be data["x"]
    Let y_data be data["y"]
    
    Let log_likelihood be 0.0
    For i from 0 to x_data.length() - 1:
        Let predicted_y be alpha + beta * x_data[i]
        Let residual be y_data[i] - predicted_y
        Let log_density be Distributions.log_pdf(
            Distributions.create_normal_distribution([("mean", 0.0), ("std_dev", sigma)]),
            residual
        )
        Set log_likelihood to log_likelihood + log_density
    
    Return log_likelihood

Let regression_data be [("x", observed_x), ("y", observed_y)]

Note: Create Bayesian model
Let bayesian_model be Bayesian.create_bayesian_model([
    ("parameter_names", ["alpha", "beta", "sigma"]),
    ("priors", [
        ("alpha", priors.alpha_prior),
        ("beta", priors.beta_prior), 
        ("sigma", priors.sigma_prior)
    ]),
    ("log_likelihood_function", linear_regression_log_likelihood),
    ("data", regression_data)
])

Note: MCMC sampling using NUTS
Let mcmc_config be Bayesian.create_nuts_config([
    ("num_samples", 2000),
    ("num_warmup", 1000),
    ("target_acceptance", 0.8),
    ("max_tree_depth", 10)
])

Let mcmc_result be Bayesian.nuts_sample(bayesian_model, mcmc_config)

Note: Extract posterior samples
Let posterior_samples be Bayesian.get_posterior_samples(mcmc_result)
Let alpha_samples be Bayesian.extract_parameter_samples(posterior_samples, "alpha")
Let beta_samples be Bayesian.extract_parameter_samples(posterior_samples, "beta")
Let sigma_samples be Bayesian.extract_parameter_samples(posterior_samples, "sigma")

Note: Posterior summary statistics
Display "Bayesian Linear Regression Results:"
Display "Alpha (intercept):"
Display "  Mean: " joined with Sampling.sample_mean(alpha_samples)
Display "  Std Dev: " joined with Sampling.sample_std_dev(alpha_samples)
Display "  95% Credible Interval: " joined with 
    Bayesian.credible_interval(alpha_samples, 0.95)

Display "Beta (slope):"
Display "  Mean: " joined with Sampling.sample_mean(beta_samples)
Display "  Std Dev: " joined with Sampling.sample_std_dev(beta_samples)
Display "  95% Credible Interval: " joined with 
    Bayesian.credible_interval(beta_samples, 0.95)

Display "Sigma (error std):"
Display "  Mean: " joined with Sampling.sample_mean(sigma_samples)
Display "  95% Credible Interval: " joined with 
    Bayesian.credible_interval(sigma_samples, 0.95)

Note: MCMC diagnostics
Let convergence_diagnostics be Bayesian.compute_mcmc_diagnostics(mcmc_result)
Display "MCMC Diagnostics:"
Display "  R-hat (alpha): " joined with Bayesian.get_r_hat(convergence_diagnostics, "alpha")
Display "  R-hat (beta): " joined with Bayesian.get_r_hat(convergence_diagnostics, "beta")
Display "  Effective sample size (alpha): " joined with 
    Bayesian.get_effective_sample_size(convergence_diagnostics, "alpha")

Note: Posterior predictive checking
Let new_x_values be [-3.0, -2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
Let posterior_predictions be Bayesian.posterior_predictive(
    bayesian_model,
    posterior_samples,
    new_data: [("x", new_x_values)]
)

Let prediction_mean be Bayesian.prediction_mean(posterior_predictions)
Let prediction_intervals be Bayesian.prediction_intervals(posterior_predictions, [0.5, 0.95])

Display "Posterior Predictions:"
For i from 0 to new_x_values.length() - 1:
    Let x be new_x_values[i]
    Let pred_mean be prediction_mean[i]
    Let interval_50 be prediction_intervals["0.5"][i]
    Let interval_95 be prediction_intervals["0.95"][i]
    
    Display "  x=" joined with x joined with ": mean=" joined with pred_mean 
        joined with ", 50%: [" joined with interval_50.lower joined with ", " joined with interval_50.upper 
        joined with "], 95%: [" joined with interval_95.lower joined with ", " joined with interval_95.upper joined with "]"
```

## Advanced Features

### Hierarchical Modeling
```runa
Note: Multi-level Bayesian model
Type called "HierarchicalModelSpec":
    group_level_priors as Dictionary[String, Distribution]
    individual_level_priors as Dictionary[String, Process] 
    likelihood_function as Process
    group_structure as Dictionary[String, List[String]]

Note: Example: Hierarchical normal model with group-specific means
Let hierarchical_data be load_grouped_data()  Note: Data with group indicators

Let hierarchical_spec be HierarchicalModelSpec with
    group_level_priors: [
        ("group_mean_hyperprior", Distributions.create_normal_distribution([("mean", 0.0), ("std_dev", 5.0)])),
        ("group_variance_hyperprior", Distributions.create_inverse_gamma_distribution([("shape", 2.0), ("scale", 1.0)])),
        ("within_group_variance_prior", Distributions.create_inverse_gamma_distribution([("shape", 2.0), ("scale", 1.0)]))
    ],
    individual_level_priors: [
        ("group_mean", Process called "group_mean_prior" that takes group_params as Dictionary returns Distribution:
            Let hyperprior_mean be group_params["group_mean_hyperprior"]
            Let hyperprior_variance be group_params["group_variance_hyperprior"]
            Return Distributions.create_normal_distribution([("mean", hyperprior_mean), ("std_dev", MathCore.sqrt(hyperprior_variance))])
        )
    ],
    likelihood_function: hierarchical_normal_likelihood,
    group_structure: extract_group_structure(hierarchical_data)

Let hierarchical_model be Bayesian.create_hierarchical_model(hierarchical_spec, hierarchical_data)

Note: Specialized MCMC for hierarchical models
Let hierarchical_mcmc be Bayesian.create_hierarchical_mcmc_config([
    ("algorithm", "gibbs_with_metropolis_within"),
    ("num_samples", 5000),
    ("num_warmup", 2000),
    ("update_group_parameters_first", True)
])

Let hierarchical_result be Bayesian.sample_hierarchical_model(
    hierarchical_model, 
    hierarchical_mcmc
)

Note: Extract group-level and individual-level parameters
Let group_level_samples be Bayesian.extract_group_level_samples(hierarchical_result)
Let individual_level_samples be Bayesian.extract_individual_level_samples(hierarchical_result)

Note: Shrinkage analysis
Let shrinkage_factors be Bayesian.compute_shrinkage_factors(
    hierarchical_result,
    group_level_samples,
    individual_level_samples
)

Display "Hierarchical Model Results:"
For group_name in shrinkage_factors.keys():
    Let shrinkage be shrinkage_factors[group_name]
    Display "  Group " joined with group_name joined with " shrinkage: " joined with shrinkage
```

### Variational Inference
```runa
Note: Variational Bayesian inference for faster approximation
Type called "VariationalConfig":
    approximation_family as String
    learning_rate as Float
    max_iterations as Integer
    convergence_tolerance as Float
    num_mc_samples as Integer

Let variational_config be VariationalConfig with
    approximation_family: "mean_field_gaussian",
    learning_rate: 0.01,
    max_iterations: 10000,
    convergence_tolerance: 1e-6,
    num_mc_samples: 100

Note: Automatic differentiation variational inference
Let advi_result be Bayesian.advi(bayesian_model, variational_config)

Let variational_parameters be Bayesian.get_variational_parameters(advi_result)
Let elbo_history be Bayesian.get_elbo_history(advi_result)

Display "Variational Inference Results:"
Display "  Final ELBO: " joined with elbo_history[-1]
Display "  Convergence achieved: " joined with Bayesian.converged(advi_result)

Note: Compare with MCMC results
Let vi_samples be Bayesian.sample_from_variational_approximation(
    advi_result,
    num_samples: 2000
)

Let vi_alpha_samples be Bayesian.extract_parameter_samples(vi_samples, "alpha")
Let vi_beta_samples be Bayesian.extract_parameter_samples(vi_samples, "beta")

Display "Comparison of MCMC vs VI:"
Display "  Alpha mean - MCMC: " joined with Sampling.sample_mean(alpha_samples)
Display "  Alpha mean - VI: " joined with Sampling.sample_mean(vi_alpha_samples)
Display "  Beta mean - MCMC: " joined with Sampling.sample_mean(beta_samples)
Display "  Beta mean - VI: " joined with Sampling.sample_mean(vi_beta_samples)

Note: Normalizing flows for more flexible approximations
Let nf_config be Bayesian.create_normalizing_flow_config([
    ("flow_type", "real_nvp"),
    ("num_layers", 4),
    ("hidden_dimensions", [32, 32])
])

Let nf_result be Bayesian.normalizing_flow_vi(bayesian_model, nf_config)
Let nf_samples be Bayesian.sample_from_flow(nf_result, 2000)
```

### Model Selection and Comparison
```runa
Note: Compare multiple Bayesian models
Let model_candidates be create_empty_list()

Note: Model 1: Linear regression
Append bayesian_model to model_candidates

Note: Model 2: Polynomial regression (degree 2)
Let poly_model_2 be Bayesian.create_polynomial_bayesian_model([
    ("degree", 2),
    ("priors", polynomial_priors_degree_2),
    ("data", regression_data)
])
Append poly_model_2 to model_candidates

Note: Model 3: Polynomial regression (degree 3)
Let poly_model_3 be Bayesian.create_polynomial_bayesian_model([
    ("degree", 3),
    ("priors", polynomial_priors_degree_3),
    ("data", regression_data)
])
Append poly_model_3 to model_candidates

Note: Compute marginal likelihoods for Bayes factors
Let marginal_likelihood_config be Bayesian.create_marginal_likelihood_config([
    ("method", "bridge_sampling"),
    ("num_bridge_samples", 10000),
    ("num_mcmc_samples", 5000)
])

Let marginal_likelihoods be Bayesian.compute_marginal_likelihoods(
    model_candidates,
    marginal_likelihood_config
)

Note: Compute Bayes factors
Let bayes_factors be Bayesian.compute_bayes_factors(marginal_likelihoods, reference_model: 0)

Display "Model Comparison Results:"
Display "  Marginal log-likelihood (Model 1): " joined with marginal_likelihoods[0]
Display "  Marginal log-likelihood (Model 2): " joined with marginal_likelihoods[1]
Display "  Marginal log-likelihood (Model 3): " joined with marginal_likelihoods[2]

Display "  Bayes Factor (Model 2 vs Model 1): " joined with bayes_factors[1]
Display "  Bayes Factor (Model 3 vs Model 1): " joined with bayes_factors[2]

Note: Information criteria comparison
Let waic_scores be Bayesian.compute_waic(model_candidates)
Let loo_scores be Bayesian.compute_loo_cv(model_candidates)

Display "Information Criteria:"
For i from 0 to model_candidates.length() - 1:
    Display "  Model " joined with (i + 1) joined with " WAIC: " joined with waic_scores[i]
    Display "  Model " joined with (i + 1) joined with " LOO-CV: " joined with loo_scores[i]

Note: Model averaging
Let model_weights be Bayesian.compute_model_weights(marginal_likelihoods)
Let averaged_predictions be Bayesian.bayesian_model_averaging(
    model_candidates,
    model_weights,
    new_data: [("x", new_x_values)]
)

Display "Model Averaging:"
For i from 0 to model_weights.length() - 1:
    Display "  Model " joined with (i + 1) joined with " weight: " joined with model_weights[i]
```

### Custom MCMC Algorithms
```runa
Note: Implement custom MCMC sampler
Type called "CustomMCMCState":
    parameters as Dictionary[String, Float]
    log_posterior as Float
    acceptance_history as List[Boolean]
    adaptation_info as Dictionary[String, Float]

Process called "adaptive_metropolis_within_gibbs" that takes model as BayesianModel, config as MCMCConfig returns MCMCResult:
    Let num_samples be config.num_samples
    Let parameter_names be Bayesian.get_parameter_names(model)
    
    Note: Initialize state
    Let current_state be initialize_mcmc_state(model)
    Let samples be create_empty_matrix(num_samples, parameter_names.length())
    
    Note: Adaptive proposal covariances
    Let proposal_covariances be initialize_proposal_covariances(parameter_names)
    Let adaptation_window be 100
    
    For iteration from 0 to num_samples - 1:
        Note: Update each parameter using Metropolis-within-Gibbs
        For param_index from 0 to parameter_names.length() - 1:
            Let param_name be parameter_names[param_index]
            
            Note: Propose new value for this parameter
            Let current_param_value be current_state.parameters[param_name]
            Let proposal_std be MathCore.sqrt(proposal_covariances[param_name])
            Let proposed_param_value be current_param_value + SecureRandom.normal_float(0.0, proposal_std)
            
            Note: Create proposed state
            Let proposed_state be copy_mcmc_state(current_state)
            Set proposed_state.parameters[param_name] to proposed_param_value
            Set proposed_state.log_posterior to Bayesian.compute_log_posterior(model, proposed_state.parameters)
            
            Note: Compute acceptance probability
            Let log_acceptance_ratio be proposed_state.log_posterior - current_state.log_posterior
            Let acceptance_probability be MathCore.min(1.0, MathCore.exp(log_acceptance_ratio))
            
            Note: Accept or reject
            Let random_uniform be SecureRandom.uniform_float()
            If random_uniform <= acceptance_probability:
                Set current_state to proposed_state
                Append True to current_state.acceptance_history
            Otherwise:
                Append False to current_state.acceptance_history
        
        Note: Store sample
        For param_index from 0 to parameter_names.length() - 1:
            Let param_name be parameter_names[param_index]
            Let param_value be current_state.parameters[param_name]
            LinAlg.set_matrix_element(samples, iteration, param_index, param_value)
        
        Note: Adapt proposal covariances
        If iteration % adaptation_window = 0 and iteration > 0:
            For param_index from 0 to parameter_names.length() - 1:
                Let param_name be parameter_names[param_index]
                Let recent_accepts be count_recent_acceptances(
                    current_state.acceptance_history, 
                    param_index, 
                    adaptation_window
                )
                Let acceptance_rate be MathCore.int_to_float(recent_accepts) / MathCore.int_to_float(adaptation_window)
                
                Note: Adapt based on acceptance rate
                If acceptance_rate < 0.2:
                    Set proposal_covariances[param_name] to proposal_covariances[param_name] * 0.9
                Otherwise If acceptance_rate > 0.5:
                    Set proposal_covariances[param_name] to proposal_covariances[param_name] * 1.1
    
    Return MCMCResult with samples: samples, acceptance_rates: compute_final_acceptance_rates(current_state)
```

## Computational Efficiency

### Parallel MCMC
```runa
Note: Run multiple MCMC chains in parallel
Let parallel_mcmc_config be Bayesian.create_parallel_mcmc_config([
    ("num_chains", 4),
    ("samples_per_chain", 2500),
    ("warmup_per_chain", 1000),
    ("num_threads", 4)
])

Let parallel_mcmc_result be Bayesian.parallel_mcmc_sample(
    bayesian_model,
    parallel_mcmc_config
)

Note: Combine chains and compute diagnostics
Let combined_samples be Bayesian.combine_mcmc_chains(parallel_mcmc_result)
Let between_chain_diagnostics be Bayesian.between_chain_diagnostics(parallel_mcmc_result)

Display "Parallel MCMC Results:"
Display "  Total samples: " joined with Bayesian.get_total_samples(combined_samples)
Display "  R-hat values:"
For param_name in parameter_names:
    Let r_hat be Bayesian.get_r_hat(between_chain_diagnostics, param_name)
    Display "    " joined with param_name joined with ": " joined with r_hat
```

### GPU-Accelerated Sampling
```runa
Note: Use GPU for massively parallel sampling
Let gpu_mcmc_config be Bayesian.create_gpu_mcmc_config([
    ("device", "cuda"),
    ("num_parallel_chains", 1024),
    ("samples_per_chain", 1000),
    ("block_size", 256)
])

If Bayesian.gpu_available():
    Let gpu_mcmc_result be Bayesian.gpu_parallel_mcmc(
        bayesian_model,
        gpu_mcmc_config
    )
    
    Let gpu_samples be Bayesian.get_gpu_samples(gpu_mcmc_result)
    Display "GPU MCMC completed: " joined with gpu_samples.length() joined with " total samples"
Otherwise:
    Display "GPU not available, falling back to CPU"
    Let cpu_result be Bayesian.nuts_sample(bayesian_model, mcmc_config)
```

## Best Practices

### Prior Specification
1. **Informative vs Non-informative**: Use domain knowledge to specify informative priors when available
2. **Prior Predictive Checks**: Simulate from prior predictive distribution to validate prior choices
3. **Sensitivity Analysis**: Test robustness of conclusions to prior specification
4. **Hierarchical Priors**: Use hierarchical priors to share information across groups

### MCMC Implementation
1. **Convergence Diagnostics**: Always check multiple convergence diagnostics (R-hat, effective sample size)
2. **Warm-up Period**: Use adequate warm-up to reach stationary distribution
3. **Thinning**: Thin chains only if memory is limited (generally not recommended)
4. **Multiple Chains**: Run multiple chains from different starting values

### Model Validation
1. **Posterior Predictive Checks**: Validate models using posterior predictive distributions
2. **Cross-Validation**: Use out-of-sample validation for model assessment
3. **Residual Analysis**: Examine residuals for systematic model inadequacies
4. **Sensitivity Analysis**: Test robustness to modeling assumptions

This module provides comprehensive Bayesian statistical capabilities for principled uncertainty quantification and statistical inference across scientific and engineering applications.