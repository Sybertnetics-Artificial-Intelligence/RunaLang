# Risk Module

The risk module provides comprehensive risk management capabilities including Value at Risk (VaR), Expected Shortfall, portfolio risk metrics, stress testing, and advanced risk modeling techniques essential for quantitative risk assessment and regulatory compliance.

## Overview

Risk management is fundamental to financial institutions and investment firms. This module provides sophisticated mathematical tools for measuring, monitoring, and managing various types of financial risks including market risk, credit risk, and operational risk.

## Mathematical Foundation

### Risk Measures Theory

The module implements various risk measures following established mathematical frameworks:

- **Value at Risk (VaR)**: Worst expected loss over a given time horizon at a specified confidence level
- **Expected Shortfall (ES)**: Average loss beyond the VaR threshold
- **Coherent Risk Measures**: Satisfy monotonicity, translation invariance, positive homogeneity, and subadditivity
- **Risk Attribution**: Decomposition of portfolio risk into constituent components

### Statistical Models

- **Parametric Methods**: Assume normal or t-distribution for returns
- **Historical Simulation**: Use historical data distribution
- **Monte Carlo Simulation**: Generate scenarios for complex portfolios
- **Extreme Value Theory**: Model tail risks and rare events

## Core Data Structures

### RiskMeasure

Represents a calculated risk metric:

```runa
Type called "RiskMeasure":
    measure_id as String                  Note: Unique identifier for the risk measure
    measure_type as String               Note: "VaR", "ES", "volatility", etc.
    confidence_level as Float            Note: Confidence level (e.g., 0.95, 0.99)
    time_horizon as Integer              Note: Time horizon in days
    risk_value as Float                  Note: Calculated risk value
    currency as String                   Note: Risk value currency
    calculation_method as String         Note: "parametric", "historical", "monte_carlo"
    calculation_date as Integer          Note: When risk was calculated
```

### PortfolioRisk

Comprehensive risk analysis for a portfolio:

```runa
Type called "PortfolioRisk":
    portfolio_id as String               Note: Portfolio identifier
    total_var as Float                   Note: Total portfolio VaR
    marginal_var as Dictionary[String, Float]  Note: Marginal VaR by asset
    component_var as Dictionary[String, Float]  Note: Component VaR by asset
    diversification_ratio as Float      Note: Diversification benefit ratio
    risk_attribution as Dictionary[String, Float]  Note: Risk contribution by asset
    correlation_matrix as List[List[Float]]  Note: Asset correlation matrix
```

## Basic Usage

### Value at Risk Calculation

```runa
Use math.financial.risk as Risk

Note: Calculate portfolio VaR using different methods
Let returns_data be [0.02, -0.01, 0.015, -0.008, 0.022, -0.012, 0.018]
Let portfolio_value be 1000000.0
Let confidence_level be 0.95
Let time_horizon be 1

Note: Parametric VaR (assumes normal distribution)
Let parametric_var be Risk.calculate_parametric_var(returns_data, portfolio_value, confidence_level, time_horizon)

Note: Historical VaR
Let historical_var be Risk.calculate_historical_var(returns_data, portfolio_value, confidence_level, time_horizon)

Note: Monte Carlo VaR
Let mc_simulations be 10000
Let monte_carlo_var be Risk.calculate_monte_carlo_var(returns_data, portfolio_value, confidence_level, time_horizon, mc_simulations)
```

### Expected Shortfall Calculation

```runa
Note: Calculate Expected Shortfall (Conditional VaR)
Let expected_shortfall be Risk.calculate_expected_shortfall(returns_data, portfolio_value, confidence_level, time_horizon)

Note: Compare VaR and ES
Let var_es_comparison be Risk.compare_var_and_es(parametric_var, expected_shortfall, confidence_level)
```

## Advanced Risk Models

### Parametric VaR Implementation

```runa
Note: Parametric VaR using normal distribution assumption
Process called "parametric_var_calculation" that takes returns as List[Float], portfolio_value as Float, confidence as Float, horizon as Integer returns Float:
    Note: Calculate portfolio return statistics
    Let mean_return be Risk.calculate_mean(returns)
    Let return_volatility be Risk.calculate_standard_deviation(returns)
    
    Note: Annualize volatility if needed
    Let daily_vol be return_volatility
    If horizon > 1:
        daily_vol = return_volatility * Risk.sqrt(Float.from_integer(horizon))
    
    Note: Calculate VaR using normal distribution
    Let z_score be Risk.normal_inverse_cdf(1.0 - confidence)
    Let var_return be mean_return + z_score * daily_vol
    
    Note: Convert to dollar VaR (positive value represents loss)
    let dollar_var be -var_return * portfolio_value
    
    Return Risk.max(dollar_var, 0.0)  Note: VaR should be positive
```

### Historical Simulation VaR

```runa
Note: Historical simulation VaR using empirical distribution
Process called "historical_simulation_var" that takes returns as List[Float], portfolio_value as Float, confidence as Float, horizon as Integer returns Float:
    Let sorted_returns be Risk.sort_ascending(returns)
    Let num_observations be sorted_returns.size
    
    Note: Scale returns for time horizon if needed
    Let scaled_returns be List[Float].create()
    For return_value in sorted_returns:
        If horizon == 1:
            scaled_returns.add(return_value)
        Otherwise:
            Note: Simple scaling assumption (could use more sophisticated methods)
            scaled_returns.add(return_value * Risk.sqrt(Float.from_integer(horizon)))
    
    Note: Find VaR percentile
    Let percentile_position be (1.0 - confidence) * Float.from_integer(num_observations)
    Let lower_index be Integer.floor(percentile_position)
    Let upper_index be Integer.ceiling(percentile_position)
    
    Note: Interpolate if needed
    Let var_return be 0.0
    If lower_index == upper_index:
        var_return = scaled_returns[lower_index]
    Otherwise:
        Let weight be percentile_position - Float.from_integer(lower_index)
        var_return = (1.0 - weight) * scaled_returns[lower_index] + weight * scaled_returns[upper_index]
    
    Note: Convert to dollar VaR
    Let dollar_var be -var_return * portfolio_value
    Return Risk.max(dollar_var, 0.0)
```

### Monte Carlo VaR

```runa
Note: Monte Carlo VaR using scenario generation
Process called "monte_carlo_var_simulation" that takes returns as List[Float], portfolio_value as Float, confidence as Float, horizon as Integer, simulations as Integer returns Float:
    Let mean_return be Risk.calculate_mean(returns)
    Let return_volatility be Risk.calculate_standard_deviation(returns)
    
    Note: Generate simulated returns
    Let simulated_returns be List[Float].create()
    
    For simulation from 1 to simulations:
        Note: Generate random scenarios for the time horizon
        Let scenario_return be 0.0
        
        For day from 1 to horizon:
            Let random_normal be Risk.generate_standard_normal()
            Let daily_return be mean_return + return_volatility * random_normal
            scenario_return = scenario_return + daily_return
        
        simulated_returns.add(scenario_return)
    
    Note: Calculate VaR from simulated distribution
    Let sorted_simulations be Risk.sort_ascending(simulated_returns)
    Let percentile_index be Integer.floor((1.0 - confidence) * Float.from_integer(simulations))
    
    Let var_return be sorted_simulations[percentile_index]
    Let dollar_var be -var_return * portfolio_value
    
    Return Risk.max(dollar_var, 0.0)
```

## Portfolio Risk Analysis

### Component VaR Calculation

```runa
Note: Calculate component VaR for portfolio risk attribution
Process called "calculate_component_var" that takes asset_returns as Dictionary[String, List[Float]], portfolio_weights as Dictionary[String, Float], confidence as Float returns Dictionary[String, Float]:
    Let component_vars be Dictionary[String, Float].create()
    Let asset_names be portfolio_weights.keys()
    
    Note: Calculate portfolio returns
    Let portfolio_returns be Risk.calculate_portfolio_returns(asset_returns, portfolio_weights)
    Let portfolio_var be Risk.calculate_parametric_var(portfolio_returns, 1.0, confidence, 1)
    
    Note: Calculate marginal VaR for each asset
    For asset_name in asset_names:
        Let marginal_var be Risk.calculate_marginal_var(asset_name, asset_returns, portfolio_weights, confidence)
        Let portfolio_weight be portfolio_weights[asset_name]
        
        Note: Component VaR = Weight × Marginal VaR
        component_vars[asset_name] = portfolio_weight * marginal_var
    
    Note: Verify components sum to total VaR (Euler's theorem)
    Let component_sum be 0.0
    For asset_name in component_vars.keys():
        component_sum = component_sum + component_vars[asset_name]
    
    Note: Scale if necessary due to numerical errors
    If Risk.abs(component_sum - portfolio_var) > 0.001:
        Let scale_factor be portfolio_var / component_sum
        For asset_name in component_vars.keys():
            component_vars[asset_name] = component_vars[asset_name] * scale_factor
    
    Return component_vars
```

### Marginal VaR Calculation

```runa
Note: Calculate marginal VaR using finite difference approximation
Process called "calculate_marginal_var_fd" that takes asset_name as String, asset_returns as Dictionary[String, List[Float]], portfolio_weights as Dictionary[String, Float], confidence as Float returns Float:
    Let epsilon be 0.001  Note: Small perturbation for finite difference
    
    Note: Calculate base portfolio VaR
    Let base_portfolio_returns be Risk.calculate_portfolio_returns(asset_returns, portfolio_weights)
    Let base_var be Risk.calculate_parametric_var(base_portfolio_returns, 1.0, confidence, 1)
    
    Note: Create perturbed weights (increase target asset by epsilon)
    Let perturbed_weights be Risk.copy_dictionary(portfolio_weights)
    perturbed_weights[asset_name] = perturbed_weights[asset_name] + epsilon
    
    Note: Renormalize weights to sum to 1
    Let total_weight be 0.0
    For weight_value in perturbed_weights.values():
        total_weight = total_weight + weight_value
    
    For asset_key in perturbed_weights.keys():
        perturbed_weights[asset_key] = perturbed_weights[asset_key] / total_weight
    
    Note: Calculate perturbed portfolio VaR
    Let perturbed_portfolio_returns be Risk.calculate_portfolio_returns(asset_returns, perturbed_weights)
    Let perturbed_var be Risk.calculate_parametric_var(perturbed_portfolio_returns, 1.0, confidence, 1)
    
    Note: Marginal VaR is the derivative approximation
    Let marginal_var be (perturbed_var - base_var) / epsilon
    
    Return marginal_var
```

## Expected Shortfall and Tail Risk

### Expected Shortfall Calculation

```runa
Note: Calculate Expected Shortfall (Conditional VaR)
Process called "calculate_expected_shortfall" that takes returns as List[Float], portfolio_value as Float, confidence as Float, horizon as Integer returns Float:
    Let sorted_returns be Risk.sort_ascending(returns)
    Let num_observations be sorted_returns.size
    
    Note: Find VaR threshold
    let var_percentile be (1.0 - confidence)
    Let threshold_index be Integer.floor(var_percentile * Float.from_integer(num_observations))
    
    Note: Calculate average of losses beyond VaR
    Let tail_losses be List[Float].create()
    For i from 0 to threshold_index:
        tail_losses.add(sorted_returns[i])
    
    Let mean_tail_loss be Risk.calculate_mean(tail_losses)
    
    Note: Scale for time horizon
    If horizon > 1:
        mean_tail_loss = mean_tail_loss * Risk.sqrt(Float.from_integer(horizon))
    
    Note: Convert to dollar Expected Shortfall
    Let dollar_es be -mean_tail_loss * portfolio_value
    
    Return Risk.max(dollar_es, 0.0)
```

### Extreme Value Theory Application

```runa
Note: Model tail risk using Generalized Pareto Distribution
Process called "extreme_value_tail_estimation" that takes returns as List[Float], threshold_percentile as Float returns Dictionary[String, Float]:
    Let evt_results be Dictionary[String, Float].create()
    Let sorted_returns be Risk.sort_ascending(returns)
    let num_observations be sorted_returns.size
    
    Note: Select threshold for tail modeling
    Let threshold_index be Integer.floor((1.0 - threshold_percentile) * Float.from_integer(num_observations))
    Let threshold_value be sorted_returns[threshold_index]
    
    Note: Extract exceedances (losses beyond threshold)
    Let exceedances be List[Float].create()
    For i from 0 to threshold_index:
        Let excess be threshold_value - sorted_returns[i]
        If excess > 0.0:
            exceedances.add(excess)
    
    Note: Fit Generalized Pareto Distribution parameters
    Let gpd_parameters be Risk.fit_generalized_pareto_distribution(exceedances)
    Let xi be gpd_parameters["shape"]  Note: Shape parameter
    Let beta be gpd_parameters["scale"]  Note: Scale parameter
    
    evt_results["threshold"] = threshold_value
    evt_results["shape_parameter"] = xi
    evt_results["scale_parameter"] = beta
    evt_results["tail_index"] = 1.0 / xi  Note: Tail heaviness measure
    
    Note: Estimate extreme quantiles using EVT
    Let extreme_quantiles be [0.999, 0.9995, 0.9999]
    For quantile_level in extreme_quantiles:
        Let extreme_var be Risk.calculate_evt_var(threshold_value, xi, beta, threshold_percentile, quantile_level)
        let quantile_key be "evt_var_" + String.from_float(quantile_level)
        evt_results[quantile_key] = extreme_var
    
    Return evt_results
```

## Stress Testing and Scenario Analysis

### Historical Stress Testing

```runa
Note: Stress test portfolio using historical crisis scenarios
Process called "historical_stress_test" that takes portfolio_weights as Dictionary[String, Float], asset_returns as Dictionary[String, List[Float]], crisis_periods as List[Dictionary[String, Integer]] returns Dictionary[String, Float]:
    Let stress_results be Dictionary[String, Float].create()
    
    For crisis_period in crisis_periods:
        Let crisis_name be crisis_period["name"]
        Let start_date be crisis_period["start_date"]
        Let end_date be crisis_period["end_date"]
        
        Note: Extract returns during crisis period
        Let crisis_returns be Dictionary[String, List[Float]].create()
        For asset_name in portfolio_weights.keys():
            Let asset_crisis_returns be Risk.extract_returns_by_date_range(
                asset_returns[asset_name], 
                start_date, 
                end_date
            )
            crisis_returns[asset_name] = asset_crisis_returns
        
        Note: Calculate portfolio performance during crisis
        Let portfolio_crisis_returns be Risk.calculate_portfolio_returns(crisis_returns, portfolio_weights)
        let total_crisis_return be Risk.calculate_cumulative_return(portfolio_crisis_returns)
        
        stress_results[crisis_name + "_total_return"] = total_crisis_return
        stress_results[crisis_name + "_worst_day"] = Risk.minimum_value(portfolio_crisis_returns)
        stress_results[crisis_name + "_volatility"] = Risk.calculate_standard_deviation(portfolio_crisis_returns)
    
    Return stress_results
```

### Monte Carlo Stress Testing

```runa
Note: Generate stressed scenarios using Monte Carlo simulation
Process called "monte_carlo_stress_test" that takes portfolio_weights as Dictionary[String, Float], asset_correlations as List[List[Float]], stress_parameters as Dictionary[String, Float], simulations as Integer returns Dictionary[String, Float]:
    Let stress_test_results be Dictionary[String, Float].create()
    
    Note: Extract stress parameters
    Let volatility_multiplier be stress_parameters["volatility_multiplier"]
    Let correlation_increase be stress_parameters["correlation_increase"]
    Let fat_tail_parameter be stress_parameters["fat_tail_parameter"]
    
    Let portfolio_returns be List[Float].create()
    
    For simulation from 1 to simulations:
        Note: Generate correlated random shocks
        Let random_shocks be Risk.generate_correlated_shocks(asset_correlations, portfolio_weights.keys().size)
        
        Note: Apply stress adjustments
        Let stressed_shocks be List[Float].create()
        For i from 0 to random_shocks.size:
            Let base_shock be random_shocks[i]
            
            Note: Increase volatility
            Let stressed_shock be base_shock * volatility_multiplier
            
            Note: Add fat-tail behavior (use t-distribution)
            If Risk.abs(base_shock) > 2.0:  Note: In the tails
                stressed_shock = stressed_shock * fat_tail_parameter
            
            stressed_shocks.add(stressed_shock)
        
        Note: Calculate portfolio return for this scenario
        Let portfolio_return be 0.0
        Let asset_names be portfolio_weights.keys()
        For i from 0 to asset_names.size:
            Let asset_name be asset_names[i]
            portfolio_return = portfolio_return + portfolio_weights[asset_name] * stressed_shocks[i]
        
        portfolio_returns.add(portfolio_return)
    
    Note: Analyze stressed distribution
    stress_test_results["stressed_var_95"] = Risk.calculate_historical_var(portfolio_returns, 1.0, 0.95, 1)
    stress_test_results["stressed_var_99"] = Risk.calculate_historical_var(portfolio_returns, 1.0, 0.99, 1)
    stress_test_results["stressed_expected_shortfall"] = Risk.calculate_expected_shortfall(portfolio_returns, 1.0, 0.95, 1)
    stress_test_results["worst_case_loss"] = -Risk.minimum_value(portfolio_returns)
    stress_test_results["stress_volatility"] = Risk.calculate_standard_deviation(portfolio_returns)
    
    Return stress_test_results
```

## Correlation and Dependency Modeling

### Dynamic Conditional Correlation

```runa
Note: Estimate time-varying correlations using DCC model
Process called "dynamic_conditional_correlation" that takes asset_returns as Dictionary[String, List[Float]], dcc_parameters as Dictionary[String, Float] returns List[List[List[Float]]]:
    Let asset_names be asset_returns.keys()
    Let num_assets be asset_names.size
    Let num_periods be asset_returns[asset_names[0]].size
    
    Note: DCC parameters
    Let alpha be dcc_parameters["alpha"]  Note: Short-term persistence
    Let beta be dcc_parameters["beta"]    Note: Long-term persistence
    
    Note: Standardize returns using GARCH volatility
    Let standardized_returns be Dictionary[String, List[Float]].create()
    For asset_name in asset_names:
        Let garch_volatilities be Risk.estimate_garch_volatility(asset_returns[asset_name])
        Let standardized be List[Float].create()
        
        For t from 0 to num_periods:
            Let raw_return be asset_returns[asset_name][t]
            Let volatility be garch_volatilities[t]
            standardized.add(raw_return / volatility)
        
        standardized_returns[asset_name] = standardized
    
    Note: Initialize correlation matrices
    Let correlation_matrices be List[List[List[Float]]].create()
    Let unconditional_corr be Risk.calculate_correlation_matrix(standardized_returns)
    
    Note: Initialize Q matrix (latent correlation process)
    Let Q_matrices be List[List[List[Float]]].create()
    Q_matrices.add(unconditional_corr)
    
    Note: Iterate through time periods
    For t from 1 to num_periods:
        Note: Get standardized returns at time t-1
        Let returns_t_minus_1 be List[Float].create()
        For asset_name in asset_names:
            returns_t_minus_1.add(standardized_returns[asset_name][t - 1])
        
        Note: Update Q matrix using DCC equation
        Let Q_t be Risk.update_dcc_q_matrix(Q_matrices[t - 1], returns_t_minus_1, unconditional_corr, alpha, beta)
        Q_matrices.add(Q_t)
        
        Note: Convert Q to correlation matrix
        Let R_t be Risk.normalize_to_correlation(Q_t)
        correlation_matrices.add(R_t)
    
    Return correlation_matrices
```

## Risk Backtesting

### VaR Backtesting

```runa
Note: Backtest VaR model accuracy using historical data
Process called "var_backtest_analysis" that takes actual_returns as List[Float], predicted_vars as List[Float], confidence_level as Float returns Dictionary[String, Float]:
    Let backtest_results be Dictionary[String, Float].create()
    
    If actual_returns.size != predicted_vars.size:
        backtest_results["error"] = 1.0
        Return backtest_results
    
    let num_observations be actual_returns.size
    Let violations be 0
    Let violation_dates be List[Integer].create()
    
    Note: Count VaR violations (actual loss exceeds predicted VaR)
    For i from 0 to num_observations:
        Let actual_loss be -actual_returns[i]  Note: Convert return to loss
        Let predicted_var be predicted_vars[i]
        
        If actual_loss > predicted_var:
            violations = violations + 1
            violation_dates.add(i)
    
    Note: Calculate violation rate and expected rate
    Let violation_rate be Float.from_integer(violations) / Float.from_integer(num_observations)
    Let expected_violation_rate be 1.0 - confidence_level
    
    backtest_results["violation_count"] = Float.from_integer(violations)
    backtest_results["violation_rate"] = violation_rate
    backtest_results["expected_violation_rate"] = expected_violation_rate
    
    Note: Kupiec test for proportion of failures
    Let lr_pof be Risk.kupiec_likelihood_ratio_test(violations, num_observations, expected_violation_rate)
    backtest_results["kupiec_lr_statistic"] = lr_pof
    backtest_results["kupiec_p_value"] = Risk.chi_square_p_value(lr_pof, 1)
    
    Note: Christoffersen independence test
    Let independence_test be Risk.christoffersen_independence_test(violation_dates, num_observations)
    backtest_results["independence_p_value"] = independence_test
    
    Note: Average severity of violations
    If violations > 0:
        Let violation_severities be List[Float].create()
        For violation_date in violation_dates:
            Let actual_loss be -actual_returns[violation_date]
            Let predicted_var be predicted_vars[violation_date]
            violation_severities.add(actual_loss - predicted_var)
        
        backtest_results["average_violation_severity"] = Risk.calculate_mean(violation_severities)
        backtest_results["max_violation_severity"] = Risk.maximum_value(violation_severities)
    Otherwise:
        backtest_results["average_violation_severity"] = 0.0
        backtest_results["max_violation_severity"] = 0.0
    
    Return backtest_results
```

## Error Handling and Validation

### Data Quality Checks

```runa
Note: Comprehensive data validation for risk calculations
Process called "validate_risk_data" that takes returns_data as List[Float] returns Dictionary[String, Boolean]:
    Let validation_results be Dictionary[String, Boolean].create()
    
    Note: Check for sufficient data points
    validation_results["sufficient_data"] = returns_data.size >= 250  Note: At least 1 year of daily data
    
    Note: Check for missing or invalid values
    Let valid_data_points be 0
    For return_value in returns_data:
        If not Risk.is_nan(return_value) and Risk.is_finite(return_value):
            valid_data_points = valid_data_points + 1
    
    validation_results["data_completeness"] = Float.from_integer(valid_data_points) / Float.from_integer(returns_data.size) > 0.95
    
    Note: Check for extreme outliers
    Let mean_return be Risk.calculate_mean(returns_data)
    let std_dev be Risk.calculate_standard_deviation(returns_data)
    Let outlier_threshold be 10.0  Note: 10 standard deviations
    
    Let outlier_count be 0
    For return_value in returns_data:
        If Risk.abs(return_value - mean_return) > outlier_threshold * std_dev:
            outlier_count = outlier_count + 1
    
    validation_results["reasonable_outliers"] = outlier_count <= 5  Note: At most 5 extreme outliers
    
    Note: Check for constant returns (indicates data issues)
    Let unique_values be Risk.count_unique_values(returns_data)
    validation_results["sufficient_variation"] = unique_values > 10
    
    Note: Overall data quality assessment
    validation_results["overall_quality"] = validation_results["sufficient_data"] and
                                           validation_results["data_completeness"] and
                                           validation_results["reasonable_outliers"] and
                                           validation_results["sufficient_variation"]
    
    Return validation_results
```

### Risk Measure Validation

```runa
Note: Validate calculated risk measures for reasonableness
Process called "validate_risk_measures" that takes risk_measure as RiskMeasure returns Dictionary[String, Boolean]:
    Let validation be Dictionary[String, Boolean].create()
    
    Note: VaR should be positive
    validation["positive_var"] = risk_measure.risk_value > 0.0
    
    Note: Confidence level should be reasonable
    validation["valid_confidence"] = risk_measure.confidence_level > 0.5 and risk_measure.confidence_level < 1.0
    
    Note: Time horizon should be reasonable
    validation["valid_horizon"] = risk_measure.time_horizon > 0 and risk_measure.time_horizon <= 252
    
    Note: Risk value shouldn't be unreasonably large
    validation["reasonable_magnitude"] = risk_measure.risk_value < 1000000000.0  Note: $1B max
    
    Note: Method should be recognized
    Let valid_methods be ["parametric", "historical", "monte_carlo", "extreme_value"]
    validation["valid_method"] = Risk.list_contains(valid_methods, risk_measure.calculation_method)
    
    validation["overall_valid"] = validation["positive_var"] and
                                 validation["valid_confidence"] and
                                 validation["valid_horizon"] and
                                 validation["reasonable_magnitude"] and
                                 validation["valid_method"]
    
    Return validation
```

## Related Documentation

- **[Options](options.md)** - Options pricing and risk management
- **[Portfolio](portfolio.md)** - Portfolio optimization and risk-return analysis
- **[Time Series](time_series.md)** - Financial time series analysis and volatility modeling
- **[Fixed Income](fixed_income.md)** - Bond portfolio risk management
- **[Derivatives](derivatives.md)** - Derivative instruments risk assessment