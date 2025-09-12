# Probability and Statistics

The Probability and Statistics module (`math/probability`) provides comprehensive probabilistic modeling, statistical inference, and stochastic analysis capabilities for scientific computing, machine learning, and data analysis applications.

## Overview

This module contains six specialized submodules that work together to provide complete probability and statistics functionality:

### 🔧 Core Submodules

1. **[Distributions](distributions.md)** - Probability distribution functions
   - Continuous and discrete probability distributions
   - Probability density functions (PDF) and cumulative distribution functions (CDF)
   - Quantile functions and random variable generation
   - Parameter estimation and method of moments
   - Maximum likelihood estimation and goodness-of-fit tests

2. **[Bayesian Methods](bayesian.md)** - Bayesian statistical inference
   - Bayesian inference and posterior distributions
   - Prior specification and conjugate priors
   - Markov Chain Monte Carlo (MCMC) methods
   - Variational inference and approximate Bayesian computation
   - Hierarchical models and model selection

3. **[Stochastic Processes](stochastic.md)** - Time-dependent random processes
   - Stochastic differential equations and Itô calculus
   - Brownian motion and Wiener processes
   - Jump processes and Lévy processes
   - Stochastic integration and martingale theory
   - Financial modeling and risk analysis

4. **[Markov Processes](markov.md)** - Markov chains and processes
   - Discrete and continuous-time Markov chains
   - Transition matrices and steady-state analysis
   - Hidden Markov Models (HMMs)
   - Markov Decision Processes (MDPs)
   - Monte Carlo Markov Chain (MCMC) algorithms

5. **[Sampling Methods](sampling.md)** - Random sampling and Monte Carlo
   - Pseudo-random and quasi-random number generation
   - Monte Carlo methods and importance sampling
   - Rejection sampling and inverse transform sampling
   - Markov Chain Monte Carlo (MCMC) sampling
   - Bootstrap methods and resampling techniques

6. **[Information Theory](information.md)** - Information-theoretic measures
   - Entropy, mutual information, and divergences
   - Channel capacity and coding theory
   - Compression and error correction
   - Statistical learning theory connections
   - Minimum description length and model selection

## Quick Start Example

```runa
Import "math/probability/distributions" as Distributions
Import "math/probability/sampling" as Sampling
Import "math/probability/bayesian" as Bayesian

Note: Create and work with probability distributions
Let normal_dist be Distributions.create_normal_distribution([
    ("mean", 0.0),
    ("std_dev", 1.0)
])

Let exponential_dist be Distributions.create_exponential_distribution([
    ("rate", 2.0)
])

Note: Evaluate probability density functions
Let x_values be [-2.0, -1.0, 0.0, 1.0, 2.0]
For x in x_values:
    Let pdf_value be Distributions.pdf(normal_dist, x)
    Let cdf_value be Distributions.cdf(normal_dist, x)
    Display "Normal PDF at x=" joined with x joined with ": " joined with pdf_value
    Display "Normal CDF at x=" joined with x joined with ": " joined with cdf_value

Note: Generate random samples
Let sample_size be 1000
Let normal_samples be Distributions.sample(normal_dist, sample_size, seed: 42)
Let exponential_samples be Distributions.sample(exponential_dist, sample_size, seed: 43)

Display "Generated " joined with normal_samples.length() joined with " normal samples"
Display "Sample mean: " joined with Sampling.sample_mean(normal_samples)
Display "Sample std dev: " joined with Sampling.sample_std_dev(normal_samples)

Note: Bayesian parameter estimation
Let observed_data be normal_samples

Note: Define prior distribution for the mean (assume known variance)
Let prior_mean be Distributions.create_normal_distribution([
    ("mean", 0.0),
    ("std_dev", 2.0)
])

Note: Compute posterior distribution
Let posterior_result be Bayesian.conjugate_normal_update([
    ("prior_mean_dist", prior_mean),
    ("known_variance", 1.0),
    ("observed_data", observed_data)
])

Let posterior_mean be Bayesian.get_posterior_mean(posterior_result)
Let posterior_variance be Bayesian.get_posterior_variance(posterior_result)
Let credible_interval be Bayesian.credible_interval(posterior_result, confidence: 0.95)

Display "Bayesian Results:"
Display "Posterior mean: " joined with posterior_mean
Display "Posterior variance: " joined with posterior_variance
Display "95% credible interval: [" joined with credible_interval.lower 
    joined with ", " joined with credible_interval.upper joined with "]"

Note: Hypothesis testing
Let null_hypothesis_mean be 0.0
Let bayes_factor be Bayesian.compute_bayes_factor([
    ("null_hypothesis", null_hypothesis_mean),
    ("alternative_model", posterior_result),
    ("observed_data", observed_data)
])

Display "Bayes factor: " joined with bayes_factor
If bayes_factor > 3.0:
    Display "Strong evidence against null hypothesis"
Otherwise If bayes_factor > 1.0:
    Display "Weak evidence against null hypothesis"  
Otherwise:
    Display "Evidence supports null hypothesis"

Note: Monte Carlo simulation
Import "math/probability/stochastic" as Stochastic

Note: Simulate a simple stochastic process (geometric Brownian motion)
Let gbm_params be Stochastic.create_gbm_parameters([
    ("drift", 0.05),
    ("volatility", 0.2),
    ("initial_value", 100.0)
])

Let time_horizon be 1.0
Let time_steps be 252  Note: Daily steps for one year
Let num_paths be 1000

Let simulation_result be Stochastic.simulate_geometric_brownian_motion([
    ("parameters", gbm_params),
    ("time_horizon", time_horizon),
    ("time_steps", time_steps),
    ("num_paths", num_paths),
    ("seed", 12345)
])

Let final_values be Stochastic.get_final_values(simulation_result)
Let path_statistics be Stochastic.compute_path_statistics(simulation_result)

Display "Monte Carlo Simulation Results:"
Display "Mean final value: " joined with Sampling.sample_mean(final_values)
Display "Standard deviation: " joined with Sampling.sample_std_dev(final_values)
Display "5th percentile: " joined with Sampling.percentile(final_values, 0.05)
Display "95th percentile: " joined with Sampling.percentile(final_values, 0.95)

Note: Information theory analysis
Import "math/probability/information" as Information

Let sample_data_1 be normal_samples
Let sample_data_2 be exponential_samples

Note: Compute information-theoretic measures
Let entropy_1 be Information.differential_entropy(sample_data_1, bins: 50)
Let entropy_2 be Information.differential_entropy(sample_data_2, bins: 50)

Display "Information Theory Results:"
Display "Entropy of normal samples: " joined with entropy_1
Display "Entropy of exponential samples: " joined with entropy_2

Let mutual_information be Information.mutual_information([
    ("data_x", sample_data_1),
    ("data_y", sample_data_2),
    ("bins_x", 25),
    ("bins_y", 25)
])

Display "Mutual information: " joined with mutual_information

Note: KL divergence between distributions
Let kl_divergence be Information.kl_divergence_continuous([
    ("distribution_p", normal_dist),
    ("distribution_q", exponential_dist),
    ("integration_bounds", (-5.0, 5.0)),
    ("tolerance", 1e-8)
])

Display "KL divergence D(Normal||Exponential): " joined with kl_divergence
```

## Key Features

### 🚀 Comprehensive Distribution Support
- **Continuous Distributions**: Normal, exponential, gamma, beta, uniform, and dozens more
- **Discrete Distributions**: Binomial, Poisson, geometric, negative binomial, hypergeometric
- **Multivariate Distributions**: Multivariate normal, Dirichlet, Wishart, copulas
- **Custom Distributions**: Framework for defining custom probability distributions

### 🧮 Advanced Statistical Methods
- **Classical Inference**: Hypothesis testing, confidence intervals, p-values
- **Bayesian Inference**: Prior/posterior analysis, credible intervals, model comparison
- **Non-parametric Methods**: Kernel density estimation, bootstrap, permutation tests
- **Robust Statistics**: M-estimators, trimmed means, resistant measures

### 💾 High-Performance Computing
- **Vectorized Operations**: Efficient batch computation of distribution functions
- **Numerical Integration**: Adaptive quadrature for complex probability calculations
- **Optimized Sampling**: Fast random number generation with multiple algorithms
- **Parallel Processing**: Multi-threaded Monte Carlo and MCMC methods

### 🎯 Specialized Applications
- **Financial Modeling**: Risk analysis, portfolio optimization, derivatives pricing
- **Machine Learning**: Probabilistic models, uncertainty quantification, Bayesian ML
- **Scientific Computing**: Uncertainty propagation, experimental design, data analysis
- **Quality Control**: Statistical process control, reliability analysis, survival analysis

## Integration Architecture

The six submodules work synergistically to provide complete probability and statistics functionality:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Distributions   │────│   Bayesian       │────│   Stochastic    │
│                 │    │                  │    │                 │
│ PDF/CDF/Quantile│    │ MCMC Methods     │    │ SDE Solutions   │
│ Parameter Est   │    │ Prior/Posterior  │    │ Brownian Motion │
│ Goodness of Fit │    │ Model Selection  │    │ Jump Processes  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
        │                       │                       │
        └───────────────────────┼───────────────────────┘
                               │
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Markov        │────│    Sampling      │────│  Information    │
│                 │    │                  │    │                 │
│ Markov Chains   │    │ Monte Carlo      │    │ Entropy         │
│ Hidden Models   │    │ MCMC Sampling    │    │ Mutual Info     │
│ Decision Proc   │    │ Bootstrap        │    │ Divergences     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Performance Characteristics

### Distribution Computations
- **PDF/CDF Evaluation**: O(1) for most standard distributions with optimized implementations
- **Quantile Functions**: O(log n) using Newton-Raphson or bisection methods
- **Parameter Estimation**: O(n) for method of moments, O(n log n) for maximum likelihood
- **Random Sampling**: O(1) per sample for most distributions using efficient algorithms

### Monte Carlo Methods
- **Standard Monte Carlo**: O(1/√n) convergence rate for variance reduction
- **Quasi-Monte Carlo**: Better than O(1/√n) for smooth functions in low dimensions
- **MCMC Sampling**: Convergence depends on mixing time and problem dimensionality
- **Parallel Sampling**: Near-linear speedup with independent random number streams

### Bayesian Computation
- **Conjugate Updates**: O(n) for sufficient statistic computation
- **MCMC Algorithms**: O(n×d×k) where n=samples, d=dimensions, k=iterations
- **Variational Inference**: O(n×d×k) with faster convergence than MCMC
- **Model Selection**: O(m×n) where m=models, n=data points for information criteria

## Application Domains

### 🔬 Scientific Research
- **Experimental Design**: Power analysis, sample size determination, randomization
- **Data Analysis**: Hypothesis testing, regression analysis, survival analysis
- **Uncertainty Quantification**: Error propagation, sensitivity analysis, calibration
- **Climate Science**: Extreme value analysis, time series modeling, spatial statistics

### 💰 Financial Engineering
- **Risk Management**: Value at Risk (VaR), Expected Shortfall, stress testing
- **Derivatives Pricing**: Black-Scholes, Monte Carlo, finite difference methods
- **Portfolio Optimization**: Mean-variance optimization, risk parity, factor models
- **Algorithmic Trading**: Signal processing, regime detection, execution optimization

### 🤖 Machine Learning and AI
- **Probabilistic Models**: Bayesian networks, Gaussian processes, mixture models
- **Deep Learning**: Variational autoencoders, Bayesian neural networks, uncertainty estimation
- **Reinforcement Learning**: Policy gradients, Q-learning, multi-armed bandits
- **Natural Language Processing**: Topic models, sequence models, language generation

### 🏭 Quality Control and Reliability
- **Statistical Process Control**: Control charts, capability studies, process monitoring
- **Reliability Engineering**: Survival analysis, accelerated testing, maintenance optimization
- **Six Sigma**: Design of experiments, measurement system analysis, defect prediction
- **Supply Chain**: Demand forecasting, inventory optimization, risk assessment

## Theoretical Foundations

### Probability Theory
- **Measure Theory**: σ-algebras, probability measures, random variables
- **Limit Theorems**: Law of large numbers, central limit theorem, convergence concepts
- **Martingale Theory**: Stopping times, optional sampling, martingale convergence
- **Stochastic Processes**: Filtrations, adapted processes, predictable processes

### Statistical Theory
- **Estimation Theory**: Sufficiency, efficiency, consistency, asymptotic normality
- **Hypothesis Testing**: Neyman-Pearson lemma, power functions, multiple comparisons
- **Decision Theory**: Loss functions, risk functions, minimax and Bayes procedures
- **Information Theory**: Fisher information, Kullback-Leibler divergence, entropy

### Computational Statistics
- **Monte Carlo Theory**: Variance reduction, importance sampling, control variates
- **MCMC Theory**: Detailed balance, ergodicity, convergence diagnostics
- **Optimization**: EM algorithm, Newton-Raphson, quasi-Newton methods
- **Numerical Analysis**: Quadrature, root finding, linear algebra for statistics

## Advanced Features

### Custom Distribution Framework
```runa
Note: Define custom probability distribution
Type called "CustomDistribution":
    name as String
    parameter_names as List[String]
    parameter_values as Dictionary[String, Float]
    support_type as String  Note: "continuous" or "discrete"
    support_bounds as Dictionary[String, Float]

Process called "custom_pdf" that takes x as Float, params as Dictionary[String, Float] returns Float:
    Note: Define custom probability density function
    Let alpha be params["alpha"]
    Let beta be params["beta"]
    
    Note: Example: Beta-like distribution with custom shape
    If x < 0.0 or x > 1.0:
        Return 0.0
    Otherwise:
        Let numerator be MathCore.power(x, alpha - 1.0) * MathCore.power(1.0 - x, beta - 1.0)
        Let beta_function be GammaFunctions.beta(alpha, beta)
        Return numerator / beta_function

Let custom_dist be Distributions.create_custom_distribution([
    ("name", "CustomBeta"),
    ("pdf_function", custom_pdf),
    ("parameters", [("alpha", 2.5), ("beta", 1.5)]),
    ("support_bounds", [("lower", 0.0), ("upper", 1.0)])
])

Note: Use custom distribution like built-in distributions
Let custom_samples be Distributions.sample(custom_dist, 1000, method: "rejection_sampling")
Let custom_mean be Distributions.mean(custom_dist)
Let custom_variance be Distributions.variance(custom_dist)
```

### Advanced MCMC Implementation
```runa
Note: Implement sophisticated MCMC algorithm
Type called "MCMCConfiguration":
    algorithm as String
    num_samples as Integer
    burn_in as Integer
    thinning as Integer
    adaptation_period as Integer
    target_acceptance_rate as Float

Process called "adaptive_metropolis_hastings" that takes target_log_density as Process, initial_state as List[Float], config as MCMCConfiguration returns MCMCResult:
    Let samples be create_empty_matrix(config.num_samples, initial_state.length())
    Let current_state be initial_state
    Let proposal_covariance be create_identity_matrix(initial_state.length())
    Let acceptance_count be 0
    
    Note: Adaptation parameters
    Let adaptation_rate be 0.01
    Let target_rate be config.target_acceptance_rate
    
    For iteration from 0 to config.num_samples - 1:
        Note: Propose new state
        Let proposal be sample_multivariate_normal(current_state, proposal_covariance)
        
        Note: Compute acceptance probability
        Let current_log_density be target_log_density(current_state)
        Let proposal_log_density be target_log_density(proposal)
        Let log_acceptance_prob be proposal_log_density - current_log_density
        
        Note: Accept or reject
        Let random_uniform be SecureRandom.uniform_float()
        If MathCore.log(random_uniform) <= log_acceptance_prob:
            Set current_state to proposal
            Set acceptance_count to acceptance_count + 1
        
        Note: Store sample
        LinAlg.set_matrix_row(samples, iteration, current_state)
        
        Note: Adapt proposal covariance during adaptation period
        If iteration < config.adaptation_period and iteration % 100 = 0:
            Let current_acceptance_rate be MathCore.int_to_float(acceptance_count) / MathCore.int_to_float(iteration + 1)
            Let adaptation_factor be 1.0 + adaptation_rate * (current_acceptance_rate - target_rate)
            Set proposal_covariance to LinAlg.scalar_multiply_matrix(proposal_covariance, adaptation_factor)
    
    Let final_acceptance_rate be MathCore.int_to_float(acceptance_count) / MathCore.int_to_float(config.num_samples)
    
    Return MCMCResult with samples: samples, acceptance_rate: final_acceptance_rate
```

### Stochastic Differential Equations
```runa
Note: Solve stochastic differential equation using Euler-Maruyama method
Process called "euler_maruyama_solve" that takes drift_function as Process, diffusion_function as Process, initial_value as Float, time_horizon as Float, num_steps as Integer, num_paths as Integer returns SDEResult:
    Let dt be time_horizon / MathCore.int_to_float(num_steps)
    Let sqrt_dt be MathCore.sqrt(dt)
    
    Let paths be create_empty_matrix(num_paths, num_steps + 1)
    
    For path_index from 0 to num_paths - 1:
        Let current_value be initial_value
        LinAlg.set_matrix_element(paths, path_index, 0, current_value)
        
        For step_index from 0 to num_steps - 1:
            Let current_time be MathCore.int_to_float(step_index) * dt
            
            Note: Compute drift and diffusion terms
            Let drift_term be drift_function(current_time, current_value)
            Let diffusion_term be diffusion_function(current_time, current_value)
            
            Note: Generate random increment
            Let random_normal be SecureRandom.normal_float(0.0, 1.0)
            
            Note: Euler-Maruyama update
            Let drift_increment be drift_term * dt
            Let diffusion_increment be diffusion_term * sqrt_dt * random_normal
            
            Set current_value to current_value + drift_increment + diffusion_increment
            LinAlg.set_matrix_element(paths, path_index, step_index + 1, current_value)
    
    Return SDEResult with paths: paths, time_grid: create_time_grid(0.0, time_horizon, num_steps)

Note: Example: Ornstein-Uhlenbeck process
Process called "ou_drift" that takes t as Float, x as Float returns Float:
    Let theta be 2.0  Note: Mean reversion speed
    Let mu be 1.0     Note: Long-term mean
    Return theta * (mu - x)

Process called "ou_diffusion" that takes t as Float, x as Float returns Float:
    Return 0.5  Note: Constant volatility

Let ou_simulation be euler_maruyama_solve(
    ou_drift,
    ou_diffusion,
    initial_value: 0.0,
    time_horizon: 2.0,
    num_steps: 1000,
    num_paths: 500
)
```

## Error Handling and Robustness

### Numerical Stability
```runa
Note: Handle numerical issues in probability computations
Process called "robust_log_sum_exp" that takes log_values as List[Float] returns Float:
    Note: Numerically stable computation of log(sum(exp(x_i)))
    If log_values.length() = 0:
        Return MathCore.negative_infinity()
    
    Let max_log_value be MathCore.max_list(log_values)
    
    If MathCore.is_infinite(max_log_value) and max_log_value < 0.0:
        Return MathCore.negative_infinity()
    
    Let sum_exp be 0.0
    For log_val in log_values:
        Let shifted_log_val be log_val - max_log_value
        Set sum_exp to sum_exp + MathCore.exp(shifted_log_val)
    
    Return max_log_value + MathCore.log(sum_exp)

Process called "check_distribution_parameters" that takes dist as Distribution returns ValidationResult:
    Note: Validate distribution parameters
    Let parameter_names be Distributions.get_parameter_names(dist)
    Let parameter_values be Distributions.get_parameter_values(dist)
    Let constraints be Distributions.get_parameter_constraints(dist)
    
    For param_name in parameter_names:
        Let param_value be parameter_values[param_name]
        Let param_constraints be constraints[param_name]
        
        If param_constraints.has_key("min") and param_value < param_constraints["min"]:
            Return ValidationResult.Invalid with "Parameter " joined with param_name 
                joined with " below minimum: " joined with param_value
        
        If param_constraints.has_key("max") and param_value > param_constraints["max"]:
            Return ValidationResult.Invalid with "Parameter " joined with param_name 
                joined with " above maximum: " joined with param_value
        
        If param_constraints.has_key("positive") and param_constraints["positive"] and param_value <= 0.0:
            Return ValidationResult.Invalid with "Parameter " joined with param_name 
                joined with " must be positive: " joined with param_value
    
    Return ValidationResult.Valid
```

### Convergence Diagnostics
```runa
Note: MCMC convergence diagnostics
Process called "gelman_rubin_diagnostic" that takes chains as List[Matrix] returns Float:
    Note: Compute potential scale reduction factor (R-hat)
    Let num_chains be chains.length()
    Let chain_length be LinAlg.get_matrix_rows(chains[0])
    
    Note: Compute within-chain and between-chain variances
    Let chain_means be create_empty_list()
    Let chain_variances be create_empty_list()
    
    For chain in chains:
        Let chain_values be LinAlg.matrix_to_vector(chain)
        Let chain_mean be Sampling.sample_mean(chain_values)
        Let chain_var be Sampling.sample_variance(chain_values)
        
        Append chain_mean to chain_means
        Append chain_var to chain_variances
    
    Let overall_mean be Sampling.sample_mean(chain_means)
    Let within_chain_variance be Sampling.sample_mean(chain_variances)
    
    Let between_chain_variance be 0.0
    For chain_mean in chain_means:
        Let deviation be chain_mean - overall_mean
        Set between_chain_variance to between_chain_variance + deviation * deviation
    Set between_chain_variance to between_chain_variance / MathCore.int_to_float(num_chains - 1)
    
    Note: Compute potential scale reduction factor
    Let marginal_variance be ((MathCore.int_to_float(chain_length) - 1.0) / MathCore.int_to_float(chain_length)) * within_chain_variance + between_chain_variance
    
    Let r_hat be MathCore.sqrt(marginal_variance / within_chain_variance)
    
    Return r_hat

Note: Check convergence
Let r_hat_value be gelman_rubin_diagnostic(mcmc_chains)
If r_hat_value > 1.1:
    Display "Warning: MCMC chains have not converged (R-hat = " joined with r_hat_value joined with ")"
    Display "Consider running more iterations or checking the model"
Otherwise:
    Display "MCMC convergence achieved (R-hat = " joined with r_hat_value joined with ")"
```

## Best Practices

### Distribution Selection
1. **Understand Your Data**: Choose distributions based on data characteristics and domain knowledge
2. **Parameter Estimation**: Use maximum likelihood for large samples, Bayesian methods for small samples
3. **Model Validation**: Always validate distribution assumptions with goodness-of-fit tests
4. **Computational Efficiency**: Use conjugate priors when possible for analytical tractability

### Bayesian Analysis
1. **Prior Selection**: Use informative priors when domain knowledge is available
2. **MCMC Diagnostics**: Always check convergence with multiple diagnostic tools
3. **Model Comparison**: Use cross-validation and information criteria for model selection
4. **Uncertainty Communication**: Report full posterior distributions, not just point estimates

### Monte Carlo Methods
1. **Sample Size**: Use convergence diagnostics rather than arbitrary sample sizes
2. **Variance Reduction**: Implement importance sampling and control variates when beneficial
3. **Parallel Computing**: Use independent random number streams for parallel sampling
4. **Reproducibility**: Always set random seeds for reproducible results

## Getting Started

1. **Start with Standard Distributions**: Begin with well-understood distributions like normal and exponential
2. **Understand Your Problem**: Identify whether you need descriptive statistics or inferential methods
3. **Choose Appropriate Methods**: Select classical or Bayesian approaches based on your context
4. **Validate Results**: Always validate statistical results with simulation and cross-validation
5. **Consider Computational Cost**: Balance accuracy with computational efficiency
6. **Document Assumptions**: Clearly document all modeling assumptions and limitations

Each submodule provides detailed documentation, comprehensive API coverage, and practical examples for robust probability and statistics computing in scientific, engineering, and business applications.

The Probability and Statistics module represents the computational foundation for uncertainty quantification, statistical inference, and data-driven decision making across all domains of quantitative analysis.