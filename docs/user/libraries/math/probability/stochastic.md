# Stochastic Processes

The Stochastic Processes module (`math/probability/stochastic`) provides comprehensive support for modeling and analyzing time-dependent random processes, including stochastic differential equations, Brownian motion, and financial modeling applications.

## Overview

This module implements advanced stochastic process theory and numerical methods for simulating and analyzing random processes that evolve over time, essential for financial modeling, physics simulations, and engineering applications.

## Key Features

### Stochastic Differential Equations
- **Itô and Stratonovich Integrals**: Different stochastic integration conventions
- **Numerical SDE Solvers**: Euler-Maruyama, Milstein, Runge-Kutta methods
- **Jump-Diffusion Processes**: Processes with both continuous and discontinuous paths
- **Multidimensional SDEs**: Systems of coupled stochastic differential equations

### Standard Processes
- **Brownian Motion**: Standard and geometric Brownian motion
- **Ornstein-Uhlenbeck Process**: Mean-reverting processes with applications
- **Cox-Ingersoll-Ross Process**: Square-root diffusion processes
- **Jump Processes**: Poisson processes, compound Poisson, Lévy processes

### Financial Modeling
- **Black-Scholes Framework**: Stock price modeling and option pricing
- **Interest Rate Models**: Vasicek, CIR, Hull-White models
- **Volatility Models**: Heston, SABR, and local volatility models
- **Risk Management**: Value-at-Risk, Expected Shortfall calculations

## Quick Start Example

```runa
Import "math/probability/stochastic" as Stochastic
Import "math/probability/sampling" as Sampling

Note: Simulate Geometric Brownian Motion for stock price modeling
Let gbm_params be Stochastic.create_gbm_parameters([
    ("initial_value", 100.0),     Note: Initial stock price
    ("drift", 0.05),              Note: Expected return (5% annual)
    ("volatility", 0.2),          Note: Volatility (20% annual)
    ("time_horizon", 1.0),        Note: One year
    ("time_steps", 252)           Note: Daily time steps
])

Let num_paths be 10000
Let gbm_simulation be Stochastic.simulate_gbm(gbm_params, num_paths, seed: 42)

Let final_prices be Stochastic.get_final_values(gbm_simulation)
Let paths_data be Stochastic.get_all_paths(gbm_simulation)
Let time_grid be Stochastic.get_time_grid(gbm_simulation)

Display "Geometric Brownian Motion Simulation:"
Display "  Initial price: " joined with gbm_params.initial_value
Display "  Final price statistics:"
Display "    Mean: " joined with Sampling.sample_mean(final_prices)
Display "    Std Dev: " joined with Sampling.sample_std_dev(final_prices)
Display "    Min: " joined with Sampling.sample_min(final_prices)
Display "    Max: " joined with Sampling.sample_max(final_prices)

Note: Calculate percentiles
Let percentiles be [0.05, 0.25, 0.5, 0.75, 0.95]
Display "  Percentiles:"
For p in percentiles:
    Let percentile_value be Sampling.percentile(final_prices, p)
    Display "    " joined with (p * 100.0) joined with "%: " joined with percentile_value

Note: Ornstein-Uhlenbeck process for interest rate modeling
Let ou_params be Stochastic.create_ou_parameters([
    ("initial_value", 0.03),      Note: Initial interest rate (3%)
    ("mean_reversion_speed", 2.0), Note: Speed of reversion to long-term mean
    ("long_term_mean", 0.04),     Note: Long-term mean rate (4%)
    ("volatility", 0.01),         Note: Interest rate volatility (1%)
    ("time_horizon", 5.0),        Note: 5 years
    ("time_steps", 1260)          Note: Daily steps for 5 years
])

Let ou_simulation be Stochastic.simulate_ornstein_uhlenbeck(ou_params, num_paths, seed: 43)
Let ou_final_rates be Stochastic.get_final_values(ou_simulation)

Display "Ornstein-Uhlenbeck Process (Interest Rates):"
Display "  Initial rate: " joined with (ou_params.initial_value * 100.0) joined with "%"
Display "  Long-term mean: " joined with (ou_params.long_term_mean * 100.0) joined with "%"
Display "  Final rate statistics:"
Display "    Mean: " joined with (Sampling.sample_mean(ou_final_rates) * 100.0) joined with "%"
Display "    Std Dev: " joined with (Sampling.sample_std_dev(ou_final_rates) * 100.0) joined with "%"

Note: Jump-diffusion process (Merton model)
Let jump_params be Stochastic.create_merton_jump_parameters([
    ("gbm_drift", 0.05),
    ("gbm_volatility", 0.2),
    ("jump_intensity", 0.1),      Note: Average 0.1 jumps per year
    ("jump_mean", -0.05),         Note: Average jump size -5%
    ("jump_volatility", 0.15),    Note: Jump size volatility 15%
    ("initial_value", 100.0),
    ("time_horizon", 1.0),
    ("time_steps", 252)
])

Let jump_simulation be Stochastic.simulate_merton_jump_diffusion(
    jump_params, 
    num_paths: 5000, 
    seed: 44
)

Let jump_final_prices be Stochastic.get_final_values(jump_simulation)
Let jump_statistics be Stochastic.compute_jump_statistics(jump_simulation)

Display "Jump-Diffusion Process (Merton Model):"
Display "  Mean final price: " joined with Sampling.sample_mean(jump_final_prices)
Display "  Jump statistics:"
Display "    Average jumps per path: " joined with Stochastic.get_average_jumps_per_path(jump_statistics)
Display "    Jump probability: " joined with Stochastic.get_jump_probability(jump_statistics)

Note: Path-dependent option pricing using Monte Carlo
Process called "asian_option_payoff" that takes path as List[Float], strike as Float returns Float:
    Note: Arithmetic average Asian call option
    Let path_average be Sampling.sample_mean(path)
    Return MathCore.max(path_average - strike, 0.0)

Let strike_price be 100.0
Let asian_payoffs be create_empty_list()

Let all_paths be Stochastic.get_all_paths(gbm_simulation)
For path in all_paths:
    Let payoff be asian_option_payoff(path, strike_price)
    Append payoff to asian_payoffs

Let discount_rate be gbm_params.drift
Let discount_factor be MathCore.exp(-discount_rate * gbm_params.time_horizon)
Let asian_option_price be discount_factor * Sampling.sample_mean(asian_payoffs)
Let pricing_error be Sampling.sample_std_dev(asian_payoffs) * discount_factor / MathCore.sqrt(MathCore.int_to_float(num_paths))

Display "Asian Option Pricing:"
Display "  Strike price: " joined with strike_price
Display "  Option price: " joined with asian_option_price
Display "  Monte Carlo error: ±" joined with pricing_error
Display "  95% confidence interval: [" joined with (asian_option_price - 1.96 * pricing_error)
    joined with ", " joined with (asian_option_price + 1.96 * pricing_error) joined with "]"
```

## Advanced Features

### Custom SDE Solving
```runa
Note: Solve custom stochastic differential equation
Type called "SDESystem":
    drift_function as Process
    diffusion_function as Process
    dimension as Integer
    initial_conditions as List[Float]

Process called "custom_drift" that takes t as Float, x as List[Float] returns List[Float]:
    Note: Example: 2D system with coupling
    Let x1 be x[0]
    Let x2 be x[1]
    
    Let dx1_dt be -0.5 * x1 + 0.2 * x2
    Let dx2_dt be 0.3 * x1 - 0.8 * x2
    
    Return [dx1_dt, dx2_dt]

Process called "custom_diffusion" that takes t as Float, x as List[Float] returns List[List[Float]]:
    Note: Example: 2D diffusion matrix
    Let x1 be x[0]
    Let x2 be x[1]
    
    Note: Diffusion matrix (2x2 for 2D system with 2 noise sources)
    Let diffusion_matrix be [
        [0.1 * (1.0 + 0.5 * x1 * x1), 0.05],
        [0.02, 0.15 * (1.0 + 0.3 * x2 * x2)]
    ]
    
    Return diffusion_matrix

Let custom_sde be SDESystem with
    drift_function: custom_drift,
    diffusion_function: custom_diffusion,
    dimension: 2,
    initial_conditions: [1.0, -0.5]

Let sde_config be Stochastic.create_sde_solver_config([
    ("method", "milstein"),
    ("time_horizon", 2.0),
    ("time_steps", 2000),
    ("num_paths", 1000),
    ("tolerance", 1e-6)
])

Let custom_sde_result be Stochastic.solve_sde_system(custom_sde, sde_config, seed: 45)

Let final_states be Stochastic.get_final_states(custom_sde_result)
Let x1_final be Stochastic.extract_component(final_states, 0)
Let x2_final be Stochastic.extract_component(final_states, 1)

Display "Custom SDE System Results:"
Display "  Component 1 final values:"
Display "    Mean: " joined with Sampling.sample_mean(x1_final)
Display "    Std Dev: " joined with Sampling.sample_std_dev(x1_final)
Display "  Component 2 final values:"
Display "    Mean: " joined with Sampling.sample_mean(x2_final)
Display "    Std Dev: " joined with Sampling.sample_std_dev(x2_final)

Note: Correlation analysis
Let correlation be Sampling.sample_correlation(x1_final, x2_final)
Display "  Final correlation between components: " joined with correlation
```

### Advanced Financial Models
```runa
Note: Heston stochastic volatility model
Type called "HestonParameters":
    initial_price as Float
    initial_volatility as Float
    risk_free_rate as Float
    dividend_yield as Float
    kappa as Float          Note: Mean reversion speed of volatility
    theta as Float          Note: Long-term volatility level  
    sigma_v as Float        Note: Volatility of volatility
    correlation as Float    Note: Correlation between price and volatility

Let heston_params be HestonParameters with
    initial_price: 100.0,
    initial_volatility: 0.04,  Note: Initial variance (vol² = 0.2²)
    risk_free_rate: 0.03,
    dividend_yield: 0.01,
    kappa: 2.0,
    theta: 0.04,
    sigma_v: 0.3,
    correlation: -0.7

Let heston_config be Stochastic.create_heston_config([
    ("time_horizon", 1.0),
    ("time_steps", 252),
    ("num_paths", 50000),
    ("discretization_scheme", "full_truncation")
])

Let heston_simulation be Stochastic.simulate_heston_model(heston_params, heston_config, seed: 46)

Let heston_prices be Stochastic.get_price_paths(heston_simulation)
Let heston_volatilities be Stochastic.get_volatility_paths(heston_simulation)

Let final_prices_heston be Stochastic.get_final_prices(heston_simulation)
Let final_volatilities be Stochastic.get_final_volatilities(heston_simulation)

Display "Heston Stochastic Volatility Model:"
Display "  Final price statistics:"
Display "    Mean: " joined with Sampling.sample_mean(final_prices_heston)
Display "    Std Dev: " joined with Sampling.sample_std_dev(final_prices_heston)
Display "  Final volatility statistics:"
Display "    Mean: " joined with (MathCore.sqrt(Sampling.sample_mean(final_volatilities)) * 100.0) joined with "%"
Display "    Std Dev: " joined with (Sampling.sample_std_dev(final_volatilities) * 100.0) joined with "%"

Note: European option pricing with stochastic volatility
Let european_strike be 105.0
Let european_payoffs_heston be create_empty_list()

For final_price in final_prices_heston:
    Let payoff be MathCore.max(final_price - european_strike, 0.0)
    Append payoff to european_payoffs_heston

Let heston_option_price be MathCore.exp(-heston_params.risk_free_rate * heston_config.time_horizon) * 
    Sampling.sample_mean(european_payoffs_heston)

Display "  European call option price (K=" joined with european_strike joined with "): " joined with heston_option_price

Note: Compare with Black-Scholes price
Let bs_volatility be MathCore.sqrt(heston_params.theta)  Note: Use long-term vol for BS
Let bs_option_price be Stochastic.black_scholes_call_price([
    ("spot", heston_params.initial_price),
    ("strike", european_strike),
    ("time_to_expiry", heston_config.time_horizon),
    ("risk_free_rate", heston_params.risk_free_rate),
    ("volatility", bs_volatility)
])

Display "  Black-Scholes price (constant vol): " joined with bs_option_price
Display "  Stochastic vol premium: " joined with (heston_option_price - bs_option_price)
```

### Regime-Switching Models
```runa
Note: Markov regime-switching model
Type called "RegimeSwitchingParameters":
    num_regimes as Integer
    regime_parameters as List[Dictionary[String, Float]]
    transition_matrix as List[List[Float]]
    initial_regime as Integer

Let regime_params be RegimeSwitchingParameters with
    num_regimes: 2,
    regime_parameters: [
        [("drift", 0.08), ("volatility", 0.15)],  Note: Bull market regime
        [("drift", -0.02), ("volatility", 0.35)]  Note: Bear market regime
    ],
    transition_matrix: [
        [0.95, 0.05],  Note: Bull to Bull: 95%, Bull to Bear: 5%
        [0.10, 0.90]   Note: Bear to Bull: 10%, Bear to Bear: 90%
    ],
    initial_regime: 0

Let regime_config be Stochastic.create_regime_switching_config([
    ("time_horizon", 3.0),
    ("time_steps", 780),  Note: Daily steps for 3 years
    ("num_paths", 10000),
    ("initial_value", 100.0)
])

Let regime_simulation be Stochastic.simulate_regime_switching_gbm(
    regime_params,
    regime_config,
    seed: 47
)

Let regime_final_prices be Stochastic.get_final_values(regime_simulation)
Let regime_transitions be Stochastic.get_regime_transitions(regime_simulation)
Let time_in_regimes be Stochastic.compute_time_in_regimes(regime_simulation)

Display "Regime-Switching Model Results:"
Display "  Final price statistics:"
Display "    Mean: " joined with Sampling.sample_mean(regime_final_prices)
Display "    Std Dev: " joined with Sampling.sample_std_dev(regime_final_prices)
Display "  Regime analysis:"
Display "    Average time in regime 0 (Bull): " joined with (time_in_regimes[0] * 100.0) joined with "%"
Display "    Average time in regime 1 (Bear): " joined with (time_in_regimes[1] * 100.0) joined with "%"
Display "    Average transitions per path: " joined with Sampling.sample_mean(regime_transitions)
```

### Risk Analysis and Stress Testing
```runa
Note: Value-at-Risk calculation using Monte Carlo
Process called "calculate_var_and_es" that takes returns as List[Float], confidence_level as Float returns Dictionary[String, Float]:
    Let sorted_returns be Sampling.sort_ascending(returns)
    Let var_index be MathCore.floor((1.0 - confidence_level) * MathCore.int_to_float(returns.length()))
    Let var_value be sorted_returns[var_index]
    
    Note: Expected Shortfall (Conditional VaR)
    Let es_sum be 0.0
    Let es_count be 0
    
    For i from 0 to var_index:
        Set es_sum to es_sum + sorted_returns[i]
        Set es_count to es_count + 1
    
    Let es_value be es_sum / MathCore.int_to_float(es_count)
    
    Return [("var", var_value), ("expected_shortfall", es_value)]

Note: Calculate portfolio returns
Let portfolio_returns be create_empty_list()
Let initial_portfolio_value be 1000000.0  Note: $1M portfolio

For i from 0 to final_prices_heston.length() - 1:
    Let final_value be (final_prices_heston[i] / heston_params.initial_price) * initial_portfolio_value
    Let portfolio_return be (final_value - initial_portfolio_value) / initial_portfolio_value
    Append portfolio_return to portfolio_returns

Let var_results_95 be calculate_var_and_es(portfolio_returns, 0.95)
Let var_results_99 be calculate_var_and_es(portfolio_returns, 0.99)

Display "Risk Analysis Results:"
Display "  95% Value-at-Risk: " joined with (var_results_95["var"] * 100.0) joined with "%"
Display "  95% Expected Shortfall: " joined with (var_results_95["expected_shortfall"] * 100.0) joined with "%"
Display "  99% Value-at-Risk: " joined with (var_results_99["var"] * 100.0) joined with "%"
Display "  99% Expected Shortfall: " joined with (var_results_99["expected_shortfall"] * 100.0) joined with "%"

Note: Stress testing scenarios
Let stress_scenarios be [
    ("market_crash", [("drift", -0.30), ("volatility", 0.60)]),
    ("high_volatility", [("drift", 0.05), ("volatility", 0.50)]),
    ("deflation", [("drift", -0.10), ("volatility", 0.25)])
]

Display "Stress Testing Results:"
For scenario in stress_scenarios:
    Let scenario_name be scenario[0]
    Let scenario_params be scenario[1]
    
    Let stress_gbm_params be Stochastic.create_gbm_parameters([
        ("initial_value", 100.0),
        ("drift", scenario_params["drift"]),
        ("volatility", scenario_params["volatility"]),
        ("time_horizon", 0.25),  Note: 3 months stress period
        ("time_steps", 63)
    ])
    
    Let stress_simulation be Stochastic.simulate_gbm(stress_gbm_params, 10000, seed: 48)
    Let stress_final_prices be Stochastic.get_final_values(stress_simulation)
    
    Let stress_returns be create_empty_list()
    For price in stress_final_prices:
        Let stress_return be (price - 100.0) / 100.0
        Append stress_return to stress_returns
    
    Let stress_var be calculate_var_and_es(stress_returns, 0.95)
    
    Display "  " joined with scenario_name joined with ":"
    Display "    95% VaR: " joined with (stress_var["var"] * 100.0) joined with "%"
    Display "    Expected Shortfall: " joined with (stress_var["expected_shortfall"] * 100.0) joined with "%"
```

## Performance Optimization

### Parallel Stochastic Simulation
```runa
Note: Parallel simulation of multiple stochastic processes
Let parallel_stochastic_config be Stochastic.create_parallel_config([
    ("num_threads", 8),
    ("paths_per_thread", 10000),
    ("load_balancing", "dynamic"),
    ("memory_optimization", True)
])

Let parallel_gbm_result be Stochastic.parallel_simulate_gbm(
    gbm_params,
    parallel_stochastic_config,
    seed: 49
)

Let parallel_simulation_time be Stochastic.get_simulation_time(parallel_gbm_result)
Let parallel_final_prices be Stochastic.get_final_values(parallel_gbm_result)

Display "Parallel Stochastic Simulation:"
Display "  Total paths: " joined with parallel_final_prices.length()
Display "  Simulation time: " joined with parallel_simulation_time joined with "ms"
Display "  Throughput: " joined with 
    (MathCore.int_to_float(parallel_final_prices.length()) / parallel_simulation_time * 1000.0)
    joined with " paths/second"
```

### Memory-Efficient Path Storage
```runa
Note: Stream processing for large-scale simulations
Let streaming_config be Stochastic.create_streaming_config([
    ("buffer_size", 1000),
    ("path_storage", "compressed"),
    ("statistics_only", True)  Note: Only store statistics, not full paths
])

Let streaming_simulator be Stochastic.create_streaming_simulator(gbm_params, streaming_config)

Let running_statistics be Stochastic.initialize_running_statistics()
Let total_paths_processed be 0

Loop:
    Let path_batch be Stochastic.simulate_next_batch(streaming_simulator, batch_size: 1000)
    If Stochastic.is_simulation_complete(path_batch):
        Break
    
    Note: Update running statistics without storing paths
    Stochastic.update_running_statistics(running_statistics, path_batch)
    Set total_paths_processed to total_paths_processed + path_batch.length()
    
    If total_paths_processed % 50000 = 0:
        Display "Processed " joined with total_paths_processed joined with " paths..."

Let final_streaming_stats be Stochastic.finalize_statistics(running_statistics)

Display "Memory-Efficient Streaming Simulation:"
Display "  Total paths processed: " joined with total_paths_processed
Display "  Mean final value: " joined with Stochastic.get_mean(final_streaming_stats)
Display "  Standard deviation: " joined with Stochastic.get_std_dev(final_streaming_stats)
Display "  Memory usage: " joined with Stochastic.get_peak_memory_usage(streaming_simulator) joined with "MB"
```

## Best Practices

### SDE Numerical Methods
1. **Step Size Selection**: Choose time steps to balance accuracy and computational cost
2. **Scheme Selection**: Use Euler-Maruyama for simple problems, Milstein for higher accuracy
3. **Stability Analysis**: Monitor numerical stability, especially for stiff systems
4. **Convergence Testing**: Verify convergence by comparing different step sizes

### Financial Modeling
1. **Parameter Calibration**: Calibrate models to market data regularly
2. **Model Validation**: Use out-of-sample testing and backtesting
3. **Risk Management**: Implement comprehensive scenario analysis and stress testing  
4. **Computational Efficiency**: Use variance reduction techniques for pricing

### Simulation Design
1. **Random Number Quality**: Use high-quality RNGs with proper seeding
2. **Antithetic Variables**: Implement variance reduction when beneficial
3. **Parallel Processing**: Design simulations to scale across multiple cores
4. **Memory Management**: Consider memory usage for large-scale simulations

This module provides comprehensive capabilities for modeling and analyzing stochastic processes, enabling sophisticated financial modeling, risk analysis, and scientific simulation applications.