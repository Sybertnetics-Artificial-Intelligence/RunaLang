# Probability Distributions

The Probability Distributions module (`math/probability/distributions`) provides comprehensive support for probability distributions including continuous and discrete distributions, density functions, parameter estimation, and random variable generation.

## Overview

This module implements a wide range of probability distributions with efficient algorithms for probability density functions (PDFs), cumulative distribution functions (CDFs), quantile functions, and random sampling.

## Key Features

### Distribution Types
- **Continuous Distributions**: Normal, exponential, gamma, beta, uniform, Weibull, log-normal, and many more
- **Discrete Distributions**: Binomial, Poisson, geometric, negative binomial, hypergeometric
- **Multivariate Distributions**: Multivariate normal, Dirichlet, Wishart, copulas
- **Truncated Distributions**: Support for truncated versions of standard distributions

### Core Functions
- **Probability Density/Mass Functions**: Efficient evaluation of PDFs and PMFs
- **Cumulative Distribution Functions**: Both standard and complementary CDFs
- **Quantile Functions**: Inverse CDF computation with high accuracy
- **Random Sampling**: High-quality random number generation from distributions

### Parameter Estimation
- **Method of Moments**: Simple and fast parameter estimation
- **Maximum Likelihood Estimation**: Optimal parameter estimation with standard errors
- **Bayesian Parameter Estimation**: Full posterior distributions for parameters
- **Goodness-of-Fit Testing**: Chi-square, Kolmogorov-Smirnov, Anderson-Darling tests

## Quick Start Example

```runa
Import "math/probability/distributions" as Distributions

Note: Create various probability distributions
Let normal_dist be Distributions.create_normal_distribution([
    ("mean", 5.0),
    ("std_dev", 2.0)
])

Let gamma_dist be Distributions.create_gamma_distribution([
    ("shape", 2.0),
    ("rate", 1.5)
])

Let binomial_dist be Distributions.create_binomial_distribution([
    ("n", 20),
    ("p", 0.3)
])

Note: Evaluate probability functions
Let x_continuous be 4.5
Let x_discrete be 6

Display "Normal Distribution at x = " joined with x_continuous
Display "  PDF: " joined with Distributions.pdf(normal_dist, x_continuous)
Display "  CDF: " joined with Distributions.cdf(normal_dist, x_continuous)
Display "  Survival: " joined with Distributions.survival_function(normal_dist, x_continuous)

Display "Binomial Distribution at x = " joined with x_discrete
Display "  PMF: " joined with Distributions.pmf(binomial_dist, x_discrete)
Display "  CDF: " joined with Distributions.cdf(binomial_dist, x_discrete)

Note: Compute quantiles
Let quantile_levels be [0.025, 0.25, 0.5, 0.75, 0.975]
Display "Normal distribution quantiles:"
For q in quantile_levels:
    Let quantile_value be Distributions.quantile(normal_dist, q)
    Display "  Q(" joined with q joined with ") = " joined with quantile_value

Note: Generate random samples
Let sample_size be 1000
Let normal_samples be Distributions.sample(normal_dist, sample_size, seed: 42)
Let gamma_samples be Distributions.sample(gamma_dist, sample_size, seed: 43)

Display "Generated samples:"
Display "  Normal mean: " joined with compute_sample_mean(normal_samples)
Display "  Normal std: " joined with compute_sample_std(normal_samples)
Display "  Gamma mean: " joined with compute_sample_mean(gamma_samples)
Display "  Gamma std: " joined with compute_sample_std(gamma_samples)

Note: Parameter estimation from samples
Let estimated_normal be Distributions.fit_distribution(
    "normal",
    normal_samples,
    method: "maximum_likelihood"
)

Let estimated_params be Distributions.get_parameters(estimated_normal)
Display "Estimated normal parameters:"
Display "  Mean: " joined with estimated_params["mean"]
Display "  Std Dev: " joined with estimated_params["std_dev"]

Note: Goodness-of-fit testing
Let gof_result be Distributions.goodness_of_fit_test(
    normal_samples,
    normal_dist,
    test: "kolmogorov_smirnov"
)

Display "Goodness of fit test:"
Display "  Test statistic: " joined with Distributions.get_test_statistic(gof_result)
Display "  P-value: " joined with Distributions.get_p_value(gof_result)
Display "  Reject null: " joined with Distributions.reject_null_hypothesis(gof_result, alpha: 0.05)
```

## Advanced Features

### Custom Distribution Creation
```runa
Note: Define a custom distribution
Type called "CustomDistributionSpec":
    name as String
    pdf_function as Process
    cdf_function as Process
    quantile_function as Process
    parameter_names as List[String]
    parameter_constraints as Dictionary[String, Dictionary[String, Float]]

Process called "beta_prime_pdf" that takes x as Float, params as Dictionary[String, Float] returns Float:
    Note: Beta prime distribution PDF
    Let alpha be params["alpha"]
    Let beta be params["beta"]
    
    If x <= 0.0:
        Return 0.0
    Otherwise:
        Let numerator be MathCore.power(x, alpha - 1.0)
        Let denominator be MathCore.power(1.0 + x, alpha + beta)
        Let beta_function be GammaFunctions.beta(alpha, beta)
        Return numerator / (beta_function * denominator)

Process called "beta_prime_cdf" that takes x as Float, params as Dictionary[String, Float] returns Float:
    Note: Beta prime distribution CDF using regularized incomplete beta function
    Let alpha be params["alpha"]
    Let beta be params["beta"]
    
    If x <= 0.0:
        Return 0.0
    Otherwise:
        Let transformed_x be x / (1.0 + x)
        Return GammaFunctions.regularized_incomplete_beta(alpha, beta, transformed_x)

Let beta_prime_spec be CustomDistributionSpec with
    name: "BetaPrime",
    pdf_function: beta_prime_pdf,
    cdf_function: beta_prime_cdf,
    quantile_function: None,  Note: Will use numerical inversion
    parameter_names: ["alpha", "beta"],
    parameter_constraints: [
        ("alpha", [("min", 0.0), ("positive", True)]),
        ("beta", [("min", 0.0), ("positive", True)])
    ]

Let custom_beta_prime be Distributions.create_custom_distribution(
    beta_prime_spec,
    parameters: [("alpha", 2.0), ("beta", 3.0)]
)

Note: Use custom distribution like built-in distributions
Let custom_samples be Distributions.sample(custom_beta_prime, 500, method: "rejection_sampling")
Let custom_mean be Distributions.mean(custom_beta_prime)
Display "Custom Beta Prime mean: " joined with custom_mean
```

### Multivariate Distributions
```runa
Note: Work with multivariate distributions
Let multivariate_normal be Distributions.create_multivariate_normal([
    ("mean", [0.0, 1.0, 2.0]),
    ("covariance", [
        [1.0, 0.5, 0.2],
        [0.5, 2.0, 0.1],
        [0.2, 0.1, 1.5]
    ])
])

Note: Evaluate multivariate PDF
Let test_point be [0.5, 1.5, 2.2]
Let mv_pdf_value be Distributions.pdf(multivariate_normal, test_point)
Display "Multivariate normal PDF: " joined with mv_pdf_value

Note: Generate multivariate samples
Let mv_samples be Distributions.sample(multivariate_normal, 1000, seed: 44)
Display "Generated " joined with mv_samples.length() joined with " multivariate samples"

Note: Compute sample statistics
Let sample_mean_vector be Distributions.compute_sample_mean_vector(mv_samples)
Let sample_covariance_matrix be Distributions.compute_sample_covariance_matrix(mv_samples)

Display "Sample mean vector: " joined with vector_to_string(sample_mean_vector)
Display "Sample covariance matrix:"
Distributions.display_matrix(sample_covariance_matrix)

Note: Marginal and conditional distributions
Let marginal_indices be [0, 2]  Note: Extract dimensions 0 and 2
Let marginal_dist be Distributions.marginal_distribution(multivariate_normal, marginal_indices)

Let conditioning_indices be [1]
Let conditioning_values be [1.0]
Let conditional_dist be Distributions.conditional_distribution(
    multivariate_normal,
    conditioning_indices,
    conditioning_values
)
```

### Copulas
```runa
Note: Model dependence structure with copulas
Let gaussian_copula be Distributions.create_gaussian_copula([
    ("correlation_matrix", [
        [1.0, 0.6],
        [0.6, 1.0]
    ])
])

Let clayton_copula be Distributions.create_clayton_copula([
    ("theta", 2.0),
    ("dimension", 2)
])

Note: Generate copula samples
Let copula_samples be Distributions.sample(gaussian_copula, 1000, seed: 45)

Note: Transform to marginal distributions
Let margin1 be Distributions.create_exponential_distribution([("rate", 1.0)])
Let margin2 be Distributions.create_gamma_distribution([("shape", 2.0), ("rate", 1.0)])

Let dependent_samples be Distributions.transform_copula_samples(
    copula_samples,
    marginal_distributions: [margin1, margin2]
)

Note: Compute rank correlation
Let kendall_tau be Distributions.kendall_correlation(dependent_samples)
Let spearman_rho be Distributions.spearman_correlation(dependent_samples)

Display "Copula-based dependence:"
Display "  Kendall's tau: " joined with kendall_tau
Display "  Spearman's rho: " joined with spearman_rho
```

### Distribution Families
```runa
Note: Work with parametric distribution families
Let exponential_family be Distributions.create_exponential_family([
    ("canonical_parameter_names", ["theta1", "theta2"]),
    ("sufficient_statistics", sufficient_stat_functions),
    ("log_partition_function", log_partition_function),
    ("carrier_measure", carrier_measure_function)
])

Note: Fit exponential family distribution
Let data_samples be load_sample_data()
Let mle_result be Distributions.fit_exponential_family(
    exponential_family,
    data_samples,
    method: "maximum_likelihood"
)

Let fitted_parameters be Distributions.get_fitted_parameters(mle_result)
Let parameter_uncertainties be Distributions.get_parameter_standard_errors(mle_result)

Display "Exponential family MLE results:"
For param_name in fitted_parameters.keys():
    Let param_value be fitted_parameters[param_name]
    Let param_se be parameter_uncertainties[param_name]
    Display "  " joined with param_name joined with ": " joined with param_value 
        joined with " ± " joined with param_se

Note: Model selection within family
Let model_variants be [
    Distributions.constrain_parameters(exponential_family, ["theta2"], [0.0]),
    exponential_family,
    Distributions.extend_family(exponential_family, ["theta3"])
]

Let model_selection_result be Distributions.model_selection(
    model_variants,
    data_samples,
    criterion: "aic"
)

Let best_model be Distributions.get_best_model(model_selection_result)
Let model_comparison_table be Distributions.get_comparison_table(model_selection_result)

Display "Model selection results:"
Display "Best model: " joined with Distributions.get_model_name(best_model)
Distributions.display_comparison_table(model_comparison_table)
```

### Extreme Value Analysis
```runa
Note: Analyze extreme values and tail behavior
Let extreme_data be extract_maxima_data(time_series_data, block_size: 30)

Note: Fit Generalized Extreme Value (GEV) distribution
Let gev_dist be Distributions.fit_distribution(
    "generalized_extreme_value",
    extreme_data,
    method: "maximum_likelihood"
)

Let gev_params be Distributions.get_parameters(gev_dist)
Display "GEV distribution parameters:"
Display "  Location (μ): " joined with gev_params["location"]
Display "  Scale (σ): " joined with gev_params["scale"]
Display "  Shape (ξ): " joined with gev_params["shape"]

Note: Compute return levels
Let return_periods be [10, 50, 100, 500, 1000]
Display "Return levels:"
For period in return_periods:
    Let return_probability be 1.0 - 1.0 / MathCore.int_to_float(period)
    Let return_level be Distributions.quantile(gev_dist, return_probability)
    Let confidence_interval be Distributions.return_level_confidence_interval(
        gev_dist, period, confidence: 0.95
    )
    
    Display "  " joined with period joined with "-year: " joined with return_level
        joined with " [" joined with confidence_interval.lower 
        joined with ", " joined with confidence_interval.upper joined with "]"

Note: Peaks over threshold analysis
Let threshold be compute_optimal_threshold(time_series_data, method: "mean_residual_life")
Let exceedances be extract_exceedances(time_series_data, threshold)

Let gpd_dist be Distributions.fit_distribution(
    "generalized_pareto",
    exceedances,
    method: "maximum_likelihood"
)

Note: Compute exceedance probabilities
Let high_quantiles be [0.99, 0.995, 0.999, 0.9995]
Display "High quantile estimates:"
For q in high_quantiles:
    Let quantile_estimate be Distributions.quantile(gpd_dist, q)
    Display "  Q(" joined with q joined with ") = " joined with quantile_estimate
```

## Performance Optimization

### Vectorized Operations
```runa
Note: Efficient vectorized distribution computations
Let x_values be generate_range(-3.0, 3.0, step: 0.1)

Note: Vectorized PDF evaluation
Let pdf_start_time be get_current_time()
Let pdf_values be Distributions.pdf_vectorized(normal_dist, x_values)
Let pdf_end_time be get_current_time()

Display "Vectorized PDF computation:"
Display "  " joined with x_values.length() joined with " evaluations in " 
    joined with (pdf_end_time - pdf_start_time) joined with "ms"

Note: Compare with individual evaluations
Let individual_start_time be get_current_time()
Let individual_pdf_values be create_empty_list()
For x in x_values:
    Let pdf_val be Distributions.pdf(normal_dist, x)
    Append pdf_val to individual_pdf_values
Let individual_end_time be get_current_time()

Display "Individual PDF computation:"
Display "  " joined with x_values.length() joined with " evaluations in " 
    joined with (individual_end_time - individual_start_time) joined with "ms"

Let speedup be (individual_end_time - individual_start_time) / (pdf_end_time - pdf_start_time)
Display "Vectorization speedup: " joined with speedup joined with "x"
```

### High-Performance Sampling
```runa
Note: Optimize random sampling for large datasets
Let large_sample_size be 1000000

Note: Configure high-performance random number generator
Let rng_config be Distributions.create_rng_config([
    ("algorithm", "mersenne_twister"),
    ("seed", 12345),
    ("buffer_size", 10000),
    ("vectorized", True)
])

Distributions.set_global_rng_config(rng_config)

Note: Parallel sampling
Let parallel_sample_start be get_current_time()
Let parallel_samples be Distributions.sample_parallel(
    normal_dist,
    large_sample_size,
    num_threads: 8,
    chunk_size: 10000
)
Let parallel_sample_end be get_current_time()

Display "Parallel sampling results:"
Display "  Generated " joined with parallel_samples.length() joined with " samples"
Display "  Time: " joined with (parallel_sample_end - parallel_sample_start) joined with "ms"
Display "  Rate: " joined with (MathCore.int_to_float(large_sample_size) / 
    MathCore.int_to_float(parallel_sample_end - parallel_sample_start)) * 1000.0 
    joined with " samples/second"

Note: Memory-efficient streaming sampling
Let streaming_sampler be Distributions.create_streaming_sampler(
    normal_dist,
    buffer_size: 1000
)

Let processed_count be 0
Loop:
    Let sample_batch be Distributions.next_batch(streaming_sampler, batch_size: 100)
    If Distributions.is_empty_batch(sample_batch):
        Break
    
    Note: Process batch
    process_sample_batch(sample_batch)
    Set processed_count to processed_count + sample_batch.length()
    
    If processed_count >= large_sample_size:
        Break

Display "Streaming sampling processed " joined with processed_count joined with " samples"
```

## Error Handling and Validation

### Parameter Validation
```runa
Note: Comprehensive parameter validation
Process called "validate_distribution_parameters" that takes dist_type as String, params as Dictionary[String, Float] returns ValidationResult:
    Match dist_type:
        Case "normal":
            If not params.has_key("mean"):
                Return ValidationResult.Invalid with "Normal distribution requires 'mean' parameter"
            If not params.has_key("std_dev"):
                Return ValidationResult.Invalid with "Normal distribution requires 'std_dev' parameter"
            If params["std_dev"] <= 0.0:
                Return ValidationResult.Invalid with "Standard deviation must be positive"
        
        Case "gamma":
            If not params.has_key("shape"):
                Return ValidationResult.Invalid with "Gamma distribution requires 'shape' parameter"
            If not params.has_key("rate") and not params.has_key("scale"):
                Return ValidationResult.Invalid with "Gamma distribution requires 'rate' or 'scale' parameter"
            If params["shape"] <= 0.0:
                Return ValidationResult.Invalid with "Shape parameter must be positive"
            If params.has_key("rate") and params["rate"] <= 0.0:
                Return ValidationResult.Invalid with "Rate parameter must be positive"
            If params.has_key("scale") and params["scale"] <= 0.0:
                Return ValidationResult.Invalid with "Scale parameter must be positive"
        
        Case "binomial":
            If not params.has_key("n"):
                Return ValidationResult.Invalid with "Binomial distribution requires 'n' parameter"
            If not params.has_key("p"):
                Return ValidationResult.Invalid with "Binomial distribution requires 'p' parameter"
            If params["n"] <= 0.0 or params["n"] != MathCore.floor(params["n"]):
                Return ValidationResult.Invalid with "n must be a positive integer"
            If params["p"] < 0.0 or params["p"] > 1.0:
                Return ValidationResult.Invalid with "p must be between 0 and 1"
        
        Default:
            Return ValidationResult.Invalid with "Unknown distribution type: " joined with dist_type
    
    Return ValidationResult.Valid

Note: Safe distribution creation with validation
Process called "create_distribution_safely" that takes dist_type as String, params as Dictionary[String, Float] returns Result[Distribution]:
    Let validation_result be validate_distribution_parameters(dist_type, params)
    
    If not ValidationResult.is_valid(validation_result):
        Return Result.Error with ValidationResult.get_error_message(validation_result)
    
    Try:
        Let distribution be Distributions.create_distribution(dist_type, params)
        Return Result.Success with distribution
    Catch numerical_error:
        Return Result.Error with "Numerical error creating distribution: " joined with numerical_error.message
    Catch overflow_error:
        Return Result.Error with "Parameter overflow: check parameter values"
```

### Numerical Stability
```runa
Note: Handle numerical edge cases
Process called "robust_pdf_evaluation" that takes dist as Distribution, x as Float returns Float:
    Note: Robust PDF evaluation with overflow protection
    Try:
        Let log_pdf_value be Distributions.log_pdf(dist, x)
        
        Note: Check for extreme values
        If log_pdf_value < -700.0:  Note: exp(-700) ≈ 0 in double precision
            Return 0.0
        Otherwise If log_pdf_value > 700.0:  Note: exp(700) would overflow
            Return MathCore.positive_infinity()
        Otherwise:
            Return MathCore.exp(log_pdf_value)
    
    Catch overflow_error:
        Return MathCore.positive_infinity()
    Catch underflow_error:
        Return 0.0
    Catch domain_error:
        Return MathCore.nan()

Note: Stable quantile computation
Process called "robust_quantile" that takes dist as Distribution, p as Float returns Float:
    If p < 0.0 or p > 1.0:
        Throw Errors.InvalidArgument with "Quantile probability must be between 0 and 1"
    
    If p = 0.0:
        Return Distributions.support_lower_bound(dist)
    Otherwise If p = 1.0:
        Return Distributions.support_upper_bound(dist)
    
    Note: Use different methods based on distribution characteristics
    If Distributions.has_closed_form_quantile(dist):
        Return Distributions.quantile_closed_form(dist, p)
    Otherwise:
        Note: Use robust numerical inversion
        Return Distributions.quantile_numerical_inversion(
            dist, p,
            method: "brent",
            tolerance: 1e-12,
            max_iterations: 100
        )
```

## Best Practices

### Distribution Selection Guidelines
1. **Data Characteristics**: Match distribution properties to data characteristics
2. **Parameter Interpretation**: Understand the meaning and identifiability of parameters
3. **Support Constraints**: Ensure distribution support matches data range
4. **Computational Efficiency**: Consider computational cost for large-scale applications

### Parameter Estimation
1. **Sample Size**: Ensure adequate sample sizes for reliable parameter estimates
2. **Method Selection**: Use MLE for large samples, method of moments for quick estimates
3. **Regularization**: Consider regularization for high-dimensional parameter spaces
4. **Uncertainty Quantification**: Always report parameter uncertainty (confidence intervals)

### Model Validation
1. **Goodness-of-Fit**: Use multiple test statistics for comprehensive validation
2. **Residual Analysis**: Examine residuals for systematic patterns
3. **Cross-Validation**: Use out-of-sample validation when possible
4. **Sensitivity Analysis**: Test robustness to parameter changes

This module provides the foundation for all probabilistic modeling in Runa, supporting everything from basic statistical analysis to complex stochastic modeling applications.