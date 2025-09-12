Note: Math Statistics Bayesian Module

## Overview

The `math/statistics/bayesian` module provides comprehensive Bayesian statistical analysis capabilities including prior specification, posterior inference, Markov Chain Monte Carlo (MCMC) sampling, Bayesian hypothesis testing, and model comparison. It offers both conjugate analytical solutions and computational approaches for complex Bayesian modeling.

## Key Features

- **Prior Distributions**: Conjugate priors, non-informative priors, empirical Bayes
- **Posterior Inference**: Analytical and computational posterior estimation
- **MCMC Sampling**: Metropolis-Hastings, Gibbs sampling, Hamilton Monte Carlo
- **Bayesian Testing**: Bayes factors, credible intervals, posterior probabilities
- **Model Comparison**: Information criteria, cross-validation, model averaging
- **Hierarchical Models**: Multi-level modeling with hyperpriors
- **Sequential Analysis**: Online learning and updating

## Data Types

### BayesianAnalysis
Complete Bayesian analysis results:
```runa
Type called "BayesianAnalysis":
    prior_specification as Dictionary[String, Float]
    likelihood_function as String
    posterior_parameters as Dictionary[String, Float]
    posterior_samples as List[Float]
    credible_intervals as Dictionary[String, List[Float]]
    bayes_factor as Float
    model_evidence as Float
    convergence_diagnostics as Dictionary[String, Float]
```

### MCMCResults
MCMC sampling output and diagnostics:
```runa
Type called "MCMCResults":
    samples as List[List[Float]]
    parameter_names as List[String]
    chain_length as Integer
    burn_in as Integer
    thinning_interval as Integer
    acceptance_rate as Float
    effective_sample_size as List[Float]
    rhat_statistics as List[Float]
    trace_plots as Dictionary[String, List[Float]]
```

### BayesianComparison
Model comparison results:
```runa
Type called "BayesianComparison":
    model_names as List[String]
    log_marginal_likelihoods as List[Float]
    bayes_factors as Dictionary[String, Float]
    posterior_probabilities as List[Float]
    information_criteria as Dictionary[String, List[Float]]
    model_weights as List[Float]
```

## Prior Specification

### Conjugate Priors
```runa
Import "math/statistics/bayesian" as Bayesian

Note: Beta-Binomial conjugate analysis
Let successes be 45
Let trials be 100
Let alpha_prior be 2.0  Note: Beta prior parameters
Let beta_prior be 2.0

Let conjugate_analysis be Bayesian.beta_binomial_analysis(successes, trials, alpha_prior, beta_prior)

Display "Beta-Binomial Conjugate Analysis:"
Display "  Prior: Beta(" joined with String(alpha_prior) joined with ", " joined with String(beta_prior) joined with ")"
Display "  Data: " joined with String(successes) joined with "/" joined with String(trials) joined with " successes"
Display "  Posterior: Beta(" joined with String(conjugate_analysis.posterior_parameters["alpha"]) joined with ", " joined with String(conjugate_analysis.posterior_parameters["beta"]) joined with ")"

Note: Posterior summary statistics
Display "  Posterior mean: " joined with String(conjugate_analysis.posterior_parameters["mean"])
Display "  Posterior mode: " joined with String(conjugate_analysis.posterior_parameters["mode"])
Display "  Posterior variance: " joined with String(conjugate_analysis.posterior_parameters["variance"])

Note: Credible intervals
Let credible_95 be conjugate_analysis.credible_intervals["95%"]
Display "  95% Credible interval: [" joined with String(credible_95[0]) joined with ", " joined with String(credible_95[1]) joined with "]"
```

### Normal-Normal Conjugate Analysis
```runa
Note: Bayesian inference for normal mean with known variance
Let observations be [102.3, 98.7, 105.2, 101.8, 99.4, 103.6, 100.9, 104.1]
Let known_sigma be 3.0
Let prior_mean be 100.0
Let prior_variance be 25.0

Let normal_analysis be Bayesian.normal_normal_analysis(observations, known_sigma, prior_mean, prior_variance)

Display "Normal-Normal Conjugate Analysis:"
Display "  Prior: N(" joined with String(prior_mean) joined with ", " joined with String(prior_variance) joined with ")"
Display "  Likelihood: N(μ, " joined with String(known_sigma * known_sigma) joined with ")"
Display "  Posterior: N(" joined with String(normal_analysis.posterior_parameters["mean"]) joined with ", " joined with String(normal_analysis.posterior_parameters["variance"]) joined with ")"

Note: Compare prior and posterior
Display "  Prior mean: " joined with String(prior_mean)
Display "  Sample mean: " joined with String(DescriptiveStats.calculate_arithmetic_mean(observations, []))
Display "  Posterior mean: " joined with String(normal_analysis.posterior_parameters["mean"])
Display "  Posterior precision gain: " joined with String(1.0 / normal_analysis.posterior_parameters["variance"] - 1.0 / prior_variance)
```

### Non-informative Priors
```runa
Note: Jeffreys prior for binomial proportion
Let jeffreys_analysis be Bayesian.jeffreys_binomial_analysis(successes, trials)

Display "Jeffreys Prior Analysis:"
Display "  Jeffreys prior: Beta(0.5, 0.5)"
Display "  Posterior: Beta(" joined with String(jeffreys_analysis.posterior_parameters["alpha"]) joined with ", " joined with String(jeffreys_analysis.posterior_parameters["beta"]) joined with ")"
Display "  Reference posterior mean: " joined with String(jeffreys_analysis.posterior_parameters["mean"])

Note: Compare with uniform prior
Let uniform_analysis be Bayesian.beta_binomial_analysis(successes, trials, 1.0, 1.0)
Display "  Uniform prior result: " joined with String(uniform_analysis.posterior_parameters["mean"])
Display "  Difference from Jeffreys: " joined with String(MathOps.absolute_value(String(jeffreys_analysis.posterior_parameters["mean"] - uniform_analysis.posterior_parameters["mean"])).result_value)
```

## MCMC Sampling

### Metropolis-Hastings Algorithm
```runa
Note: MCMC sampling for complex posterior
Let data_points be [2.3, 1.8, 3.2, 2.7, 1.9, 2.4, 3.1, 2.2, 2.8, 2.5]
Let model_config be Dictionary with:
    "likelihood": "normal"
    "prior_mean_mu": "0.0"
    "prior_var_mu": "100.0"
    "prior_shape_sigma": "1.0"
    "prior_rate_sigma": "1.0"

Let mcmc_config be Dictionary with:
    "n_samples": "10000"
    "burn_in": "2000"
    "thinning": "2"
    "proposal_sd_mu": "0.5"
    "proposal_sd_sigma": "0.2"

Let mcmc_results be Bayesian.metropolis_hastings_normal(data_points, model_config, mcmc_config)

Display "Metropolis-Hastings MCMC Results:"
Display "  Chain length: " joined with String(mcmc_results.chain_length)
Display "  Burn-in: " joined with String(mcmc_results.burn_in)
Display "  Effective samples: " joined with String(mcmc_results.chain_length - mcmc_results.burn_in)
Display "  Acceptance rate μ: " joined with String(mcmc_results.acceptance_rate)

Note: Posterior summaries from samples
Let mu_samples be mcmc_results.samples[0]  Note: Mean parameter samples
Let sigma_samples be mcmc_results.samples[1]  Note: Standard deviation samples

Let mu_posterior_mean be DescriptiveStats.calculate_arithmetic_mean(mu_samples, [])
Let sigma_posterior_mean be DescriptiveStats.calculate_arithmetic_mean(sigma_samples, [])

Display "  Posterior μ mean: " joined with String(mu_posterior_mean)
Display "  Posterior σ mean: " joined with String(sigma_posterior_mean)

Note: Credible intervals from samples
Let mu_ci be DescriptiveStats.calculate_percentiles(mu_samples, [2.5, 97.5], "linear")
Let sigma_ci be DescriptiveStats.calculate_percentiles(sigma_samples, [2.5, 97.5], "linear")

Display "  95% CI for μ: [" joined with String(mu_ci["2.5"]) joined with ", " joined with String(mu_ci["97.5"]) joined with "]"
Display "  95% CI for σ: [" joined with String(sigma_ci["2.5"]) joined with ", " joined with String(sigma_ci["97.5"]) joined with "]"
```

### Gibbs Sampling
```runa
Note: Gibbs sampling for hierarchical model
Let group_data be [
    [12.3, 13.1, 12.8, 13.5],  Note: Group 1
    [14.8, 15.3, 14.5, 15.7],  Note: Group 2
    [11.2, 11.8, 11.5, 12.1]   Note: Group 3
]

Let hierarchical_config be Dictionary with:
    "n_samples": "5000"
    "burn_in": "1000"
    "prior_mu0": "0.0"
    "prior_tau0": "0.01"
    "prior_alpha": "1.0"
    "prior_beta": "1.0"

Let gibbs_results be Bayesian.gibbs_hierarchical_normal(group_data, hierarchical_config)

Display "Gibbs Sampling Results (Hierarchical Model):"
Display "  Samples collected: " joined with String(gibbs_results.chain_length)
Display "  Parameters estimated:"

Note: Group means
For i from 0 to Length(group_data) - 1:
    Let group_mean_samples be gibbs_results.samples[i]
    Let group_mean_est be DescriptiveStats.calculate_arithmetic_mean(group_mean_samples, [])
    Display "    Group " joined with String(i + 1) joined with " mean: " joined with String(group_mean_est)

Note: Hyperparameters
Let overall_mean_samples be gibbs_results.samples[Length(group_data)]
Let between_var_samples be gibbs_results.samples[Length(group_data) + 1]

Display "    Overall mean (hyperparameter): " joined with String(DescriptiveStats.calculate_arithmetic_mean(overall_mean_samples, []))
Display "    Between-group variance: " joined with String(DescriptiveStats.calculate_arithmetic_mean(between_var_samples, []))
```

### Convergence Diagnostics
```runa
Note: Assess MCMC convergence
Let convergence_diagnostics be Bayesian.assess_mcmc_convergence(mcmc_results)

Display "MCMC Convergence Diagnostics:"
Display "  R-hat statistics (should be < 1.1):"
For i from 0 to Length(mcmc_results.parameter_names) - 1:
    Let param_name be mcmc_results.parameter_names[i]
    Let rhat_value be convergence_diagnostics.rhat_statistics[i]
    Let status be ""
    If rhat_value < 1.1:
        Set status to "✓ Converged"
    Otherwise:
        Set status to "✗ Poor convergence"
    Display "    " joined with param_name joined with ": " joined with String(rhat_value) joined with " " joined with status

Display "  Effective sample sizes:"
For i from 0 to Length(mcmc_results.parameter_names) - 1:
    Let param_name be mcmc_results.parameter_names[i]
    Let ess_value be convergence_diagnostics.effective_sample_size[i]
    Display "    " joined with param_name joined with ": " joined with String(ess_value)

Note: Monte Carlo standard error
Let mcse_results be Bayesian.monte_carlo_standard_error(mcmc_results)
Display "  Monte Carlo standard errors:"
For Each param, mcse in mcse_results:
    Display "    " joined with param joined with ": " joined with String(mcse)
```

## Bayesian Hypothesis Testing

### Bayes Factors
```runa
Note: Compare two competing hypotheses using Bayes factors
Let control_data be [12.3, 13.1, 12.8, 13.5, 12.9, 13.2, 12.7]
Let treatment_data be [14.8, 15.3, 14.5, 15.7, 14.9, 15.1, 14.6]

Note: H1: Treatment effect exists vs H0: No treatment effect
Let bayes_factor_analysis be Bayesian.bayes_factor_two_sample_normal(control_data, treatment_data, "two-sided")

Display "Bayesian Hypothesis Testing (Bayes Factors):"
Display "  H0: μ_treatment = μ_control (no effect)"
Display "  H1: μ_treatment ≠ μ_control (effect exists)"
Display "  Bayes Factor (BF10): " joined with String(bayes_factor_analysis.bayes_factor)

Note: Interpret Bayes factor
Let bf_interpretation be ""
If bayes_factor_analysis.bayes_factor > 100:
    Set bf_interpretation to "Extreme evidence for H1"
Otherwise if bayes_factor_analysis.bayes_factor > 30:
    Set bf_interpretation to "Very strong evidence for H1"
Otherwise if bayes_factor_analysis.bayes_factor > 10:
    Set bf_interpretation to "Strong evidence for H1"
Otherwise if bayes_factor_analysis.bayes_factor > 3:
    Set bf_interpretation to "Moderate evidence for H1"
Otherwise if bayes_factor_analysis.bayes_factor > 1:
    Set bf_interpretation to "Weak evidence for H1"
Otherwise if bayes_factor_analysis.bayes_factor > 0.33:
    Set bf_interpretation to "Weak evidence for H0"
Otherwise if bayes_factor_analysis.bayes_factor > 0.1:
    Set bf_interpretation to "Moderate evidence for H0"
Otherwise:
    Set bf_interpretation to "Strong evidence for H0"

Display "  Interpretation: " joined with bf_interpretation
Display "  Posterior probability of H1: " joined with String(bayes_factor_analysis.posterior_probability_h1)
Display "  Posterior probability of H0: " joined with String(1.0 - bayes_factor_analysis.posterior_probability_h1)
```

### Posterior Probability Regions
```runa
Note: Region-based hypothesis testing
Let parameter_samples be mu_samples  Note: From previous MCMC
Let null_value be 2.5  Note: H0: μ = 2.5

Let posterior_prob_analysis be Bayesian.posterior_probability_regions(parameter_samples, null_value, "two-sided")

Display "Posterior Probability Region Analysis:"
Display "  H0: μ = " joined with String(null_value)
Display "  Posterior probability that μ = " joined with String(null_value) joined with ": " joined with String(posterior_prob_analysis.point_probability)
Display "  Posterior probability that μ > " joined with String(null_value) joined with ": " joined with String(posterior_prob_analysis.upper_tail_probability)
Display "  Posterior probability that μ < " joined with String(null_value) joined with ": " joined with String(posterior_prob_analysis.lower_tail_probability)

Note: Highest Posterior Density (HPD) interval
Let hpd_95 be Bayesian.highest_posterior_density_interval(parameter_samples, 0.95)
Display "  95% HPD interval: [" joined with String(hpd_95.lower_bound) joined with ", " joined with String(hpd_95.upper_bound) joined with "]"
Display "  Null value in HPD interval: " joined with String(null_value >= hpd_95.lower_bound and null_value <= hpd_95.upper_bound)
```

### Sequential Bayesian Testing
```runa
Note: Online Bayesian analysis with sequential data
Let sequential_data be [[12.3], [12.3, 13.1], [12.3, 13.1, 12.8], [12.3, 13.1, 12.8, 13.5]]
Let prior_params be Dictionary with: "alpha": "1.0", "beta": "1.0", "mu0": "12.0", "sigma0": "2.0"

Display "Sequential Bayesian Analysis:"
For i from 0 to Length(sequential_data) - 1:
    Let current_data be sequential_data[i]
    Let sequential_result be Bayesian.sequential_normal_analysis(current_data, prior_params)
    
    Display "  After " joined with String(Length(current_data)) joined with " observations:"
    Display "    Posterior mean: " joined with String(sequential_result.posterior_parameters["mean"])
    Display "    Posterior variance: " joined with String(sequential_result.posterior_parameters["variance"])
    Display "    95% credible interval: [" joined with String(sequential_result.credible_intervals["95%"][0]) joined with ", " joined with String(sequential_result.credible_intervals["95%"][1]) joined with "]"
    Display "    Posterior precision: " joined with String(1.0 / sequential_result.posterior_parameters["variance"])
```

## Model Selection and Comparison

### Information Criteria
```runa
Note: Compare models using Bayesian information criteria
Let model_configs be [
    Dictionary with: "type": "normal", "parameters": ["mean", "variance"],
    Dictionary with: "type": "t", "parameters": ["location", "scale", "df"],
    Dictionary with: "type": "skew_normal", "parameters": ["location", "scale", "shape"]
]

Let model_comparison_results be []
For Each model_config in model_configs:
    Let model_fit be Bayesian.fit_model(data_points, model_config)
    Call model_comparison_results.append(model_fit)

Let comparison_summary be Bayesian.compare_models(model_comparison_results)

Display "Bayesian Model Comparison:"
Display "  Model comparison results:"
For i from 0 to Length(model_configs) - 1:
    Let model_name be model_configs[i]["type"]
    Display "    " joined with model_name joined with " model:"
    Display "      Log marginal likelihood: " joined with String(comparison_summary.log_marginal_likelihoods[i])
    Display "      WAIC: " joined with String(comparison_summary.information_criteria["WAIC"][i])
    Display "      LOO-CV: " joined with String(comparison_summary.information_criteria["LOO"][i])
    Display "      Model weight: " joined with String(comparison_summary.model_weights[i])

Display "  Best model: " joined with comparison_summary.model_names[0] joined with " (highest weight)"
```

### Bayes Factor Model Comparison
```runa
Note: Pairwise model comparisons
Let pairwise_comparisons be Bayesian.pairwise_bayes_factors(model_comparison_results)

Display "Pairwise Bayes Factor Comparisons:"
For Each comparison in pairwise_comparisons:
    Display "  " joined with comparison.model1 joined with " vs " joined with comparison.model2 joined with ":"
    Display "    BF: " joined with String(comparison.bayes_factor)
    Display "    Evidence strength: " joined with comparison.evidence_interpretation
    Display "    Preferred model: " joined with comparison.preferred_model
```

### Model Averaging
```runa
Note: Bayesian model averaging for prediction
Let new_data_point be 2.8
Let model_averaged_prediction be Bayesian.bayesian_model_averaging(model_comparison_results, new_data_point)

Display "Bayesian Model Averaging Prediction:"
Display "  Input value: " joined with String(new_data_point)
Display "  Weighted prediction: " joined with String(model_averaged_prediction.prediction)
Display "  Prediction variance: " joined with String(model_averaged_prediction.prediction_variance)
Display "  95% prediction interval: [" joined with String(model_averaged_prediction.prediction_interval[0]) joined with ", " joined with String(model_averaged_prediction.prediction_interval[1]) joined with "]"

Display "  Model contributions:"
For i from 0 to Length(model_configs) - 1:
    Let model_name be model_configs[i]["type"]
    Let contribution = model_averaged_prediction.model_contributions[i]
    Display "    " joined with model_name joined with ": " joined with String(contribution)
```

## Hierarchical Bayesian Models

### Random Effects Model
```runa
Note: Hierarchical model with random effects
Let school_scores be [
    [85.2, 87.1, 84.3, 86.7, 85.9],  Note: School 1
    [78.4, 80.2, 77.8, 79.6, 78.9],  Note: School 2
    [92.1, 93.8, 91.5, 92.9, 93.2],  Note: School 3
    [88.7, 90.1, 87.9, 89.3, 88.6]   Note: School 4
]

Let hierarchical_model_config be Dictionary with:
    "model_type": "random_effects"
    "prior_overall_mean": "80.0"
    "prior_overall_variance": "100.0"
    "prior_between_variance_shape": "1.0"
    "prior_between_variance_rate": "1.0"
    "prior_within_variance_shape": "1.0"
    "prior_within_variance_rate": "1.0"

Let hierarchical_results be Bayesian.hierarchical_normal_model(school_scores, hierarchical_model_config)

Display "Hierarchical Bayesian Model Results:"
Display "  Overall mean (μ): " joined with String(hierarchical_results.hyperparameters["overall_mean"])
Display "  Between-group variance (τ²): " joined with String(hierarchical_results.hyperparameters["between_variance"])
Display "  Within-group variance (σ²): " joined with String(hierarchical_results.hyperparameters["within_variance"])

Display "  School-specific estimates (shrinkage applied):"
For i from 0 to Length(school_scores) - 1:
    Let school_mean be hierarchical_results.group_parameters[i]["mean"]
    Let raw_mean be DescriptiveStats.calculate_arithmetic_mean(school_scores[i], [])
    Let shrinkage be MathOps.absolute_value(String(raw_mean - school_mean)).result_value
    Display "    School " joined with String(i + 1) joined with ": " joined with String(school_mean) joined with " (shrinkage: " joined with String(shrinkage) joined with ")"
```

### Meta-Analysis Model
```runa
Note: Bayesian meta-analysis
Let study_effects be [0.23, 0.31, 0.18, 0.42, 0.29, 0.35, 0.21]  Note: Effect sizes
Let study_variances be [0.04, 0.03, 0.05, 0.02, 0.04, 0.03, 0.05]  Note: Study variances

Let meta_analysis_config be Dictionary with:
    "model": "random_effects"
    "prior_overall_effect_mean": "0.0"
    "prior_overall_effect_variance": "1.0"
    "prior_heterogeneity_shape": "1.0"
    "prior_heterogeneity_rate": "1.0"

Let meta_analysis_results be Bayesian.bayesian_meta_analysis(study_effects, study_variances, meta_analysis_config)

Display "Bayesian Meta-Analysis Results:"
Display "  Pooled effect size: " joined with String(meta_analysis_results.pooled_effect)
Display "  95% credible interval: [" joined with String(meta_analysis_results.credible_interval[0]) joined with ", " joined with String(meta_analysis_results.credible_interval[1]) joined with "]"
Display "  Between-study heterogeneity (τ²): " joined with String(meta_analysis_results.heterogeneity)
Display "  I² statistic: " joined with String(meta_analysis_results.i_squared * 100.0) joined with "%"

Display "  Individual study weights:"
For i from 0 to Length(study_effects) - 1:
    Display "    Study " joined with String(i + 1) joined with ": " joined with String(meta_analysis_results.study_weights[i])

Note: Posterior probability of positive effect
Let prob_positive be meta_analysis_results.posterior_probabilities["positive_effect"]
Display "  P(effect > 0 | data): " joined with String(prob_positive)
```

## Advanced Bayesian Methods

### Variational Bayes
```runa
Note: Variational Bayes approximation for fast inference
Let vb_config be Dictionary with:
    "approximation_family": "mean_field"
    "max_iterations": "1000"
    "convergence_tolerance": "1e-6"
    "learning_rate": "0.01"

Let vb_results be Bayesian.variational_bayes_normal(data_points, vb_config)

Display "Variational Bayes Results:"
Display "  Iterations to convergence: " joined with String(vb_results.iterations)
Display "  Final ELBO: " joined with String(vb_results.evidence_lower_bound)
Display "  Approximate posterior parameters:"
Display "    μ mean: " joined with String(vb_results.variational_parameters["mu_mean"])
Display "    μ variance: " joined with String(vb_results.variational_parameters["mu_variance"])
Display "    σ shape: " joined with String(vb_results.variational_parameters["sigma_shape"])
Display "    σ rate: " joined with String(vb_results.variational_parameters["sigma_rate"])

Note: Compare with MCMC results
Display "  Comparison with MCMC:"
Display "    μ estimate (VB vs MCMC): " joined with String(vb_results.variational_parameters["mu_mean"]) joined with " vs " joined with String(mu_posterior_mean)
Display "    Computation time speedup: " joined with String(vb_results.computation_speedup) joined with "x"
```

### Approximate Bayesian Computation (ABC)
```runa
Note: ABC for likelihood-free inference
Let observed_summary_stats be Dictionary with:
    "mean": "2.45"
    "variance": "0.82"
    "skewness": "0.15"

Let abc_config be Dictionary with:
    "n_simulations": "100000"
    "tolerance": "0.1"
    "distance_metric": "euclidean"
    "summary_statistics": ["mean", "variance", "skewness"]

Let abc_results be Bayesian.abc_inference(observed_summary_stats, abc_config)

Display "Approximate Bayesian Computation Results:"
Display "  Accepted simulations: " joined with String(abc_results.n_accepted) joined with "/" joined with String(abc_config["n_simulations"])
Display "  Acceptance rate: " joined with String(Float(abc_results.n_accepted) / Float(abc_config["n_simulations"]) * 100.0) joined with "%"

Display "  Approximate posterior summaries:"
For Each param_name in abc_results.parameter_names:
    Let param_samples be abc_results.accepted_parameters[param_name]
    Let param_mean be DescriptiveStats.calculate_arithmetic_mean(param_samples, [])
    Let param_ci be DescriptiveStats.calculate_percentiles(param_samples, [2.5, 97.5], "linear")
    Display "    " joined with param_name joined with ": " joined with String(param_mean) joined with " [" joined with String(param_ci["2.5"]) joined with ", " joined with String(param_ci["97.5"]) joined with "]"
```

## Bayesian Decision Theory

### Loss Functions and Decision Rules
```runa
Note: Bayesian decision analysis with loss functions
Let posterior_samples be mu_samples  Note: Use previous posterior samples
Let decision_options be [2.0, 2.5, 3.0]  Note: Possible actions
Let loss_function_type be "quadratic"  Note: (θ - a)²

Let decision_analysis be Bayesian.bayesian_decision_analysis(posterior_samples, decision_options, loss_function_type)

Display "Bayesian Decision Analysis:"
Display "  Loss function: " joined with loss_function_type
Display "  Expected losses:"
For i from 0 to Length(decision_options) - 1:
    Display "    Action a=" joined with String(decision_options[i]) joined with ": " joined with String(decision_analysis.expected_losses[i])

Display "  Optimal action: " joined with String(decision_analysis.optimal_action)
Display "  Minimum expected loss: " joined with String(decision_analysis.minimum_expected_loss)

Note: Sensitivity analysis
Let alternative_loss_analysis be Bayesian.bayesian_decision_analysis(posterior_samples, decision_options, "absolute")
Display "  Alternative loss function (absolute):"
Display "    Optimal action: " joined with String(alternative_loss_analysis.optimal_action)
Display "    Minimum expected loss: " joined with String(alternative_loss_analysis.minimum_expected_loss)
```

### Value of Information
```runa
Note: Calculate expected value of sample information
Let current_posterior be normal_analysis  Note: Use existing posterior
Let sample_sizes be [5, 10, 20, 50]
Let sampling_cost_per_observation be 100.0

Display "Value of Information Analysis:"
For Each n in sample_sizes:
    Let evsi_result be Bayesian.expected_value_sample_information(current_posterior, n, sampling_cost_per_observation, loss_function_type)
    
    Display "  Sample size n=" joined with String(n) joined with ":"
    Display "    EVSI: $" joined with String(evsi_result.expected_value)
    Display "    Sampling cost: $" joined with String(evsi_result.sampling_cost)
    Display "    Net value: $" joined with String(evsi_result.net_value)
    Display "    Optimal to sample: " joined with String(evsi_result.should_sample)
```

## Model Diagnostics and Validation

### Posterior Predictive Checks
```runa
Note: Check model adequacy using posterior predictions
Let ppc_config be Dictionary with:
    "n_posterior_samples": "1000"
    "test_statistics": ["mean", "variance", "min", "max", "skewness"]

Let ppc_results be Bayesian.posterior_predictive_check(data_points, mcmc_results, ppc_config)

Display "Posterior Predictive Checks:"
For Each test_stat in ppc_config["test_statistics"]:
    Let observed_stat be ppc_results.observed_statistics[test_stat]
    Let posterior_pred_stats be ppc_results.posterior_predictive_statistics[test_stat]
    
    Let ppc_p_value be ppc_results.bayesian_p_values[test_stat]
    Display "  " joined with test_stat joined with ":"
    Display "    Observed: " joined with String(observed_stat)
    Display "    Posterior predictive mean: " joined with String(DescriptiveStats.calculate_arithmetic_mean(posterior_pred_stats, []))
    Display "    Bayesian p-value: " joined with String(ppc_p_value)
    
    Let adequacy_assessment be ""
    If ppc_p_value > 0.05 and ppc_p_value < 0.95:
        Set adequacy_assessment to "✓ Adequate fit"
    Otherwise:
        Set adequacy_assessment to "⚠ Potential model inadequacy"
    Display "    Assessment: " joined with adequacy_assessment
```

### Cross-Validation
```runa
Note: Leave-one-out cross-validation for model assessment
Let loo_cv_results be Bayesian.leave_one_out_cross_validation(data_points, model_configs[0])

Display "Leave-One-Out Cross-Validation:"
Display "  LOO estimate: " joined with String(loo_cv_results.loo_estimate)
Display "  Standard error: " joined with String(loo_cv_results.standard_error)
Display "  Effective number of parameters: " joined with String(loo_cv_results.p_loo)
Display "  LOO-IC: " joined with String(loo_cv_results.looic)

Note: Pareto k diagnostic
Let high_k_observations be 0
For Each k_value in loo_cv_results.pareto_k_values:
    If k_value > 0.7:
        Set high_k_observations to high_k_observations + 1

Display "  Pareto k diagnostics:"
Display "    Observations with k > 0.7: " joined with String(high_k_observations) joined with "/" joined with String(Length(data_points))
If high_k_observations > 0:
    Display "    ⚠ Some observations have high influence (consider robust models)"
Otherwise:
    Display "    ✓ All observations have reasonable influence"
```

## Error Handling and Best Practices

### Robust Error Management
```runa
Note: Handle common Bayesian analysis errors
Try:
    Let insufficient_mcmc be Dictionary with: "n_samples": "10", "burn_in": "5"
    Let bad_mcmc_result be Bayesian.metropolis_hastings_normal(data_points, model_config, insufficient_mcmc)
Catch Errors.InsufficientSamples as error:
    Display "MCMC error: " joined with error.message
    Display "Recommended minimum samples: 1000"
    Display "Recommended burn-in: 20% of total samples"

Try:
    Let improper_prior be Dictionary with: "alpha": "-1.0", "beta": "2.0"
    Let bad_conjugate be Bayesian.beta_binomial_analysis(10, 20, Float(improper_prior["alpha"]), Float(improper_prior["beta"]))
Catch Errors.InvalidPrior as error:
    Display "Prior specification error: " joined with error.message
    Display "Beta parameters must be positive"

Try:
    Let extreme_bayes_factor be Bayesian.bayes_factor_two_sample_normal([1.0], [100.0], "two-sided")
Catch Errors.NumericalInstability as error:
    Display "Numerical error: " joined with error.message
    Display "Consider using log Bayes factors for extreme values"
```

### Analysis Workflow Template
```runa
Process called "comprehensive_bayesian_analysis" that takes data as List[Float], analysis_config as Dictionary[String, String] returns Dictionary[String, String]:
    Let results be Dictionary[String, String]
    
    Note: Step 1: Prior specification
    Let prior_type be analysis_config["prior_type"]
    If prior_type == "informative":
        Set results["prior_info"] to "Used informative prior based on domain expertise"
    Otherwise if prior_type == "non_informative":
        Set results["prior_info"] to "Used non-informative Jeffreys prior"
    Otherwise:
        Set results["prior_info"] to "Used weakly informative prior"
    
    Note: Step 2: Model fitting
    Let model_type be analysis_config["model_type"]
    Let fitting_method be analysis_config["fitting_method"]
    
    If fitting_method == "conjugate":
        Let conjugate_result be perform_conjugate_analysis(data, model_type, prior_type)
        Set results["posterior_mean"] to String(conjugate_result.posterior_parameters["mean"])
        Set results["computational_method"] to "Analytical (conjugate)"
    Otherwise:
        Let mcmc_result be perform_mcmc_analysis(data, model_type, prior_type)
        Set results["posterior_mean"] to String(DescriptiveStats.calculate_arithmetic_mean(mcmc_result.samples[0], []))
        Set results["computational_method"] to "MCMC sampling"
        
        Note: Step 3: Convergence assessment
        Let convergence be assess_convergence(mcmc_result)
        Set results["convergence_ok"] to String(convergence.all_converged)
        If not convergence.all_converged:
            Set results["warning"] to "MCMC chains did not converge - increase samples"
    
    Note: Step 4: Model validation
    Let validation_results be validate_model(data, results)
    Set results["model_adequate"] to String(validation_results.passes_checks)
    Set results["validation_info"] to validation_results.summary
    
    Note: Step 5: Inference summary
    Set results["analysis_complete"] to "true"
    Set results["recommendation"] to generate_recommendations(results)
    
    Return results

Note: Example comprehensive analysis
Let research_data be [2.3, 2.8, 2.1, 3.2, 2.7, 2.9, 2.4, 3.1, 2.6, 2.8]
Let analysis_config be Dictionary with:
    "prior_type": "weakly_informative"
    "model_type": "normal"
    "fitting_method": "mcmc"
    "credible_level": "0.95"

Let comprehensive_results be comprehensive_bayesian_analysis(research_data, analysis_config)

Display "Comprehensive Bayesian Analysis Summary:"
For Each key, value in comprehensive_results:
    Display "  " joined with key joined with ": " joined with value
```

The Bayesian statistics module provides a complete framework for Bayesian inference, from simple conjugate analyses to complex hierarchical models and computational methods. Its integration with MCMC diagnostics and model validation ensures reliable and interpretable Bayesian analyses for research and decision-making applications.