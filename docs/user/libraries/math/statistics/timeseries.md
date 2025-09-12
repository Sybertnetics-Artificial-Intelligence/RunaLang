Note: Math Statistics Time Series Module

## Overview

The `math/statistics/timeseries` module provides comprehensive time series analysis capabilities including ARIMA modeling, seasonal decomposition, forecasting methods, spectral analysis, and advanced temporal data analysis techniques. It supports both univariate and multivariate time series with extensive diagnostic tools and forecasting validation.

## Key Features

- **ARIMA Modeling**: AutoRegressive Integrated Moving Average with seasonal variants
- **Decomposition**: Seasonal, trend, and remainder component separation
- **Forecasting**: Point forecasts, prediction intervals, accuracy metrics
- **Spectral Analysis**: Frequency domain analysis, periodogram, spectral density
- **State Space Models**: Kalman filtering, structural time series models
- **Cointegration**: Error correction models, Johansen cointegration test
- **Volatility Models**: GARCH family models for financial time series

## Data Types

### TimeSeriesData
Time series data structure with metadata:
```runa
Type called "TimeSeriesData":
    values as List[Float]
    timestamps as List[Integer]
    frequency as String
    seasonal_period as Integer
    missing_values as List[Integer]
    data_transformations as List[String]
    outlier_indices as List[Integer]
```

### ARIMAModel
Complete ARIMA model specification and results:
```runa
Type called "ARIMAModel":
    order as List[Integer]
    seasonal_order as List[Integer]
    coefficients as Dictionary[String, List[Float]]
    residuals as List[Float]
    fitted_values as List[Float]
    log_likelihood as Float
    aic as Float
    bic as Float
    standard_errors as Dictionary[String, List[Float]]
```

### ForecastResult
Forecasting results with uncertainty:
```runa
Type called "ForecastResult":
    point_forecasts as List[Float]
    forecast_intervals as List[List[Float]]
    forecast_errors as List[Float]
    forecast_horizon as Integer
    confidence_levels as List[Float]
    forecast_accuracy as Dictionary[String, Float]
```

## Time Series Preprocessing

### Stationarity Testing
```runa
Import "math/statistics/timeseries" as TimeSeries

Note: Test for unit roots and stationarity
Let ts_data be [10.2, 10.8, 11.1, 10.5, 9.8, 10.3, 11.2, 11.7, 12.1, 11.9, 11.4, 10.9, 11.8, 12.3, 12.7, 13.1]
Let test_methods be ["adf", "kpss", "pp"]

Let stationarity_results be TimeSeries.check_stationarity(ts_data, test_methods, 0.05)

Display "Stationarity Test Results:"
For Each method in test_methods:
    Let test_result be stationarity_results[method]
    Display "  " joined with method joined with " test:"
    Display "    Test statistic: " joined with String(test_result["test_statistic"])
    Display "    P-value: " joined with String(test_result["p_value"])
    Display "    Critical value (5%): " joined with String(test_result["critical_value_5pct"])
    Display "    Conclusion: " joined with test_result["conclusion"]

Note: Overall stationarity assessment
Let is_stationary be stationarity_results["adf"]["conclusion"] == "stationary" and stationarity_results["kpss"]["conclusion"] == "stationary"
Display "  Overall assessment: " joined with String(is_stationary) joined with " stationary"
```

### Differencing for Stationarity
```runa
Note: Apply differencing to achieve stationarity
Let non_stationary_data be [100, 102, 105, 108, 112, 116, 121, 126, 132, 138, 145, 152, 160, 168, 177, 186]

Note: First difference
Let first_diff be TimeSeries.difference_series(non_stationary_data, [1], [])
Display "Differencing Results:"
Display "  Original series length: " joined with String(Length(non_stationary_data))
Display "  First difference length: " joined with String(Length(first_diff))
Display "  First few differences: " joined with String(first_diff[0]) joined with ", " joined with String(first_diff[1]) joined with ", " joined with String(first_diff[2])

Note: Test stationarity after differencing
Let diff_stationarity be TimeSeries.check_stationarity(first_diff, ["adf"], 0.05)
Display "  Stationarity after differencing: " joined with diff_stationarity["adf"]["conclusion"]

Note: Seasonal differencing if needed
Let seasonal_data be [10, 15, 20, 12, 11, 16, 21, 13, 12, 17, 22, 14, 13, 18, 23, 15]
Let seasonal_diff be TimeSeries.difference_series(seasonal_data, [], [4])  Note: Quarterly seasonal pattern
Display "  Seasonal difference (lag 4): " joined with String(Length(seasonal_diff)) joined with " values"
```

### Trend Removal
```runa
Note: Remove deterministic trends
Let trending_data be [5.2, 5.8, 6.1, 6.7, 7.2, 7.8, 8.1, 8.9, 9.2, 9.8, 10.1, 10.7, 11.3, 11.8, 12.2, 12.9]
Let detrend_result be TimeSeries.detrend_series(trending_data, "linear")

Display "Detrending Results:"
Display "  Method: Linear detrending"
Display "  Original mean: " joined with String(DescriptiveStats.calculate_arithmetic_mean(trending_data, []))
Display "  Detrended mean: " joined with String(DescriptiveStats.calculate_arithmetic_mean(detrend_result["detrended"], []))
Display "  Trend component (first few): " joined with String(detrend_result["trend"][0]) joined with ", " joined with String(detrend_result["trend"][1]) joined with ", " joined with String(detrend_result["trend"][2])

Note: Alternative detrending methods
Let polynomial_detrend be TimeSeries.detrend_series(trending_data, "polynomial")
Display "  Polynomial detrending applied"
Display "  Polynomial detrended mean: " joined with String(DescriptiveStats.calculate_arithmetic_mean(polynomial_detrend["detrended"], []))
```

## Seasonal Decomposition

### Classical Decomposition
```runa
Note: Decompose time series into trend, seasonal, and remainder
Let seasonal_ts be [12.1, 14.5, 16.8, 13.2, 11.8, 14.2, 16.5, 13.5, 12.3, 14.8, 17.1, 14.1, 13.0, 15.2, 17.8, 14.8, 13.5, 15.7, 18.2, 15.3]
Let seasonal_period be 4  Note: Quarterly pattern

Let decomposition be TimeSeries.seasonal_decomposition(seasonal_ts, seasonal_period, "additive")

Display "Seasonal Decomposition Results:"
Display "  Decomposition type: Additive (Y = Trend + Seasonal + Remainder)"
Display "  Seasonal period: " joined with String(seasonal_period)
Display "  Components extracted:"

Note: Display first few values of each component
Display "  Trend component (first 5): "
For i from 0 to 4:
    If i < Length(decomposition.trend):
        Display "    " joined with String(i + 1) joined with ": " joined with String(decomposition.trend[i])

Display "  Seasonal component (first cycle): "
For i from 0 to seasonal_period - 1:
    Display "    Season " joined with String(i + 1) joined with ": " joined with String(decomposition.seasonal[i])

Display "  Strength measures:"
Display "    Seasonal strength: " joined with String(decomposition.seasonal_strength)
Display "    Trend strength: " joined with String(decomposition.trend_strength)
```

### STL Decomposition
```runa
Note: Seasonal and Trend decomposition using Loess
Let stl_config be Dictionary with:
    "seasonal_window": "periodic"
    "trend_window": "7"
    "robust": "true"

Let stl_result be TimeSeries.stl_decomposition(seasonal_ts, seasonal_period, stl_config)

Display "STL Decomposition Results:"
Display "  Method: Seasonal and Trend decomposition using Loess"
Display "  Robust: " joined with String(stl_config["robust"])
Display "  Seasonal window: " joined with stl_config["seasonal_window"]
Display "  Trend window: " joined with stl_config["trend_window"]

Note: Compare seasonal components
Display "  Seasonal component comparison (first cycle):"
For i from 0 to seasonal_period - 1:
    Display "    Classical: " joined with String(decomposition.seasonal[i]) joined with ", STL: " joined with String(stl_result.seasonal[i])

Display "  Remainder statistics:"
Display "    Classical remainder std: " joined with String(DescriptiveStats.calculate_standard_deviation(decomposition.residual, false))
Display "    STL remainder std: " joined with String(DescriptiveStats.calculate_standard_deviation(stl_result.residual, false))
```

## ARIMA Modeling

### Model Identification
```runa
Note: Identify ARIMA order using information criteria
Let stationary_ts be first_diff  Note: Use differenced data from earlier

Let arima_orders be TimeSeries.auto_arima_order_selection(stationary_ts, 3, 1, 3)

Display "ARIMA Order Selection Results:"
Display "  Best model order: ARIMA(" joined with String(arima_orders.p) joined with "," joined with String(arima_orders.d) joined with "," joined with String(arima_orders.q) joined with ")"
Display "  AIC: " joined with String(arima_orders.aic)
Display "  BIC: " joined with String(arima_orders.bic)
Display "  Log-likelihood: " joined with String(arima_orders.log_likelihood)

Display "  Model comparison:"
For Each candidate in arima_orders.candidate_models:
    Display "    ARIMA(" joined with String(candidate.p) joined with "," joined with String(candidate.d) joined with "," joined with String(candidate.q) joined with "): AIC=" joined with String(candidate.aic)
```

### ARIMA Estimation
```runa
Note: Estimate ARIMA model parameters
Let arima_model be TimeSeries.fit_arima(ts_data, [arima_orders.p, arima_orders.d, arima_orders.q], [0, 0, 0, 0])

Display "ARIMA Model Estimation Results:"
Display "  Model: ARIMA(" joined with String(arima_model.order[0]) joined with "," joined with String(arima_model.order[1]) joined with "," joined with String(arima_model.order[2]) joined with ")"
Display "  Convergence: " joined with String(arima_model.converged)
Display "  Log-likelihood: " joined with String(arima_model.log_likelihood)
Display "  AIC: " joined with String(arima_model.aic)
Display "  BIC: " joined with String(arima_model.bic)

Display "  Parameter estimates:"
If Length(arima_model.coefficients["ar"]) > 0:
    Display "    AR coefficients:"
    For i from 0 to Length(arima_model.coefficients["ar"]) - 1:
        Display "      φ" joined with String(i + 1) joined with ": " joined with String(arima_model.coefficients["ar"][i]) joined with " (SE: " joined with String(arima_model.standard_errors["ar"][i]) joined with ")"

If Length(arima_model.coefficients["ma"]) > 0:
    Display "    MA coefficients:"
    For i from 0 to Length(arima_model.coefficients["ma"]) - 1:
        Display "      θ" joined with String(i + 1) joined with ": " joined with String(arima_model.coefficients["ma"][i]) joined with " (SE: " joined with String(arima_model.standard_errors["ma"][i]) joined with ")"

If "const" in arima_model.coefficients:
    Display "    Constant: " joined with String(arima_model.coefficients["const"]) joined with " (SE: " joined with String(arima_model.standard_errors["const"]) joined with ")"
```

### Seasonal ARIMA
```runa
Note: SARIMA model for seasonal time series
Let sarima_model be TimeSeries.fit_arima(seasonal_ts, [1, 1, 1], [1, 1, 1, 4])  Note: SARIMA(1,1,1)(1,1,1)4

Display "Seasonal ARIMA Model Results:"
Display "  Model: SARIMA(" joined with String(sarima_model.order[0]) joined with "," joined with String(sarima_model.order[1]) joined with "," joined with String(sarima_model.order[2]) joined with ")(" joined with String(sarima_model.seasonal_order[0]) joined with "," joined with String(sarima_model.seasonal_order[1]) joined with "," joined with String(sarima_model.seasonal_order[2]) joined with ")" joined with String(sarima_model.seasonal_order[3])
Display "  Seasonal period: " joined with String(sarima_model.seasonal_order[3])
Display "  AIC: " joined with String(sarima_model.aic)
Display "  BIC: " joined with String(sarima_model.bic)

Display "  Seasonal parameters:"
If "seasonal_ar" in sarima_model.coefficients:
    Display "    Seasonal AR (Φ): " joined with String(sarima_model.coefficients["seasonal_ar"][0])
If "seasonal_ma" in sarima_model.coefficients:
    Display "    Seasonal MA (Θ): " joined with String(sarima_model.coefficients["seasonal_ma"][0])
```

## Model Diagnostics

### Residual Analysis
```runa
Note: Comprehensive residual diagnostics for ARIMA model
Let diagnostics be TimeSeries.arima_diagnostics(arima_model, ts_data)

Display "ARIMA Model Diagnostics:"
Display "  Residual statistics:"
Display "    Mean: " joined with String(diagnostics.residual_stats["mean"])
Display "    Standard deviation: " joined with String(diagnostics.residual_stats["std"])
Display "    Skewness: " joined with String(diagnostics.residual_stats["skewness"])
Display "    Kurtosis: " joined with String(diagnostics.residual_stats["kurtosis"])

Display "  Normality tests:"
Display "    Jarque-Bera p-value: " joined with String(diagnostics.normality_tests["jarque_bera"])
Display "    Shapiro-Wilk p-value: " joined with String(diagnostics.normality_tests["shapiro_wilk"])

Display "  Autocorrelation tests:"
Display "    Ljung-Box Q(10): " joined with String(diagnostics.autocorrelation_tests["ljung_box_10"])
Display "    Box-Pierce Q(10): " joined with String(diagnostics.autocorrelation_tests["box_pierce_10"])

Display "  Heteroscedasticity tests:"
Display "    ARCH test p-value: " joined with String(diagnostics.heteroscedasticity_tests["arch_test"])
```

### Information Criteria Comparison
```runa
Note: Compare different ARIMA specifications
Let model_orders_to_test be [[1, 1, 0], [1, 1, 1], [2, 1, 1], [1, 1, 2], [2, 1, 2]]
Let ic_comparison be []

Display "Information Criteria Comparison:"
Display "  Model           AIC       BIC      Log-Lik"
For Each order in model_orders_to_test:
    Let test_model be TimeSeries.fit_arima(ts_data, order, [0, 0, 0, 0])
    Display "  ARIMA(" joined with String(order[0]) joined with "," joined with String(order[1]) joined with "," joined with String(order[2]) joined with ")     " joined with String(test_model.aic) joined with "  " joined with String(test_model.bic) joined with "  " joined with String(test_model.log_likelihood)
    Call ic_comparison.append(test_model)

Note: Find best model by AIC
Let best_aic_index be 0
Let best_aic_value be ic_comparison[0].aic
For i from 1 to Length(ic_comparison) - 1:
    If ic_comparison[i].aic < best_aic_value:
        Set best_aic_value to ic_comparison[i].aic
        Set best_aic_index to i

Let best_order be model_orders_to_test[best_aic_index]
Display "  Best model by AIC: ARIMA(" joined with String(best_order[0]) joined with "," joined with String(best_order[1]) joined with "," joined with String(best_order[2]) joined with ")"
```

## Forecasting

### Point Forecasts and Intervals
```runa
Note: Generate forecasts with prediction intervals
Let forecast_horizon be 6
Let confidence_levels be [0.80, 0.95]

Let forecast_result be TimeSeries.forecast_arima(arima_model, ts_data, forecast_horizon, confidence_levels)

Display "ARIMA Forecasting Results:"
Display "  Forecast horizon: " joined with String(forecast_horizon) joined with " periods"
Display "  Confidence levels: " joined with String(confidence_levels)

Display "  Point forecasts:"
For i from 0 to Length(forecast_result.point_forecasts) - 1:
    Display "    Period " joined with String(i + 1) joined with ": " joined with String(forecast_result.point_forecasts[i])

Display "  95% Prediction intervals:"
For i from 0 to Length(forecast_result.forecast_intervals) - 1:
    Let interval_95 be forecast_result.forecast_intervals[i][1]  Note: Index 1 for 95% CI
    Display "    Period " joined with String(i + 1) joined with ": [" joined with String(interval_95[0]) joined with ", " joined with String(interval_95[1]) joined with "]"

Note: Forecast accuracy if holdout data available
If "forecast_accuracy" in forecast_result:
    Display "  Forecast accuracy metrics:"
    Display "    RMSE: " joined with String(forecast_result.forecast_accuracy["rmse"])
    Display "    MAE: " joined with String(forecast_result.forecast_accuracy["mae"])
    Display "    MAPE: " joined with String(forecast_result.forecast_accuracy["mape"]) joined with "%"
```

### Rolling Window Forecasting
```runa
Note: Assess forecast performance using rolling windows
Let train_size be 12
Let test_size be 4
Let rolling_config be Dictionary with:
    "window_size": String(train_size)
    "forecast_horizon": "1"
    "refit_frequency": "1"

Let rolling_results be TimeSeries.rolling_window_forecast(ts_data, [1, 1, 1], rolling_config)

Display "Rolling Window Forecast Results:"
Display "  Training window size: " joined with String(train_size)
Display "  Number of forecasts: " joined with String(Length(rolling_results.forecasts))
Display "  Forecast accuracy:"
Display "    RMSE: " joined with String(rolling_results.accuracy_metrics["rmse"])
Display "    MAE: " joined with String(rolling_results.accuracy_metrics["mae"])
Display "    Mean forecast: " joined with String(DescriptiveStats.calculate_arithmetic_mean(rolling_results.forecasts, []))
Display "    Mean actual: " joined with String(DescriptiveStats.calculate_arithmetic_mean(rolling_results.actuals, []))

Note: Forecast error analysis
Let forecast_errors be []
For i from 0 to Length(rolling_results.forecasts) - 1:
    Let error be rolling_results.actuals[i] - rolling_results.forecasts[i]
    Call forecast_errors.append(error)

Display "  Forecast error statistics:"
Display "    Mean error: " joined with String(DescriptiveStats.calculate_arithmetic_mean(forecast_errors, []))
Display "    Error std dev: " joined with String(DescriptiveStats.calculate_standard_deviation(forecast_errors, false))
```

## Spectral Analysis

### Periodogram Analysis
```runa
Note: Identify dominant frequencies in time series
Let periodogram_result be TimeSeries.compute_periodogram(ts_data, "bartlett")

Display "Periodogram Analysis Results:"
Display "  Window: Bartlett"
Display "  Frequency resolution: " joined with String(periodogram_result.frequency_resolution)
Display "  Number of frequencies: " joined with String(Length(periodogram_result.frequencies))

Display "  Dominant frequencies:"
Let sorted_power_indices be sort_by_power_descending(periodogram_result.power_spectrum)
For i from 0 to 4:  Note: Top 5 frequencies
    Let freq_index be sorted_power_indices[i]
    Let frequency be periodogram_result.frequencies[freq_index]
    Let power be periodogram_result.power_spectrum[freq_index]
    Let period be 1.0 / frequency
    Display "    Freq: " joined with String(frequency) joined with ", Power: " joined with String(power) joined with ", Period: " joined with String(period)

Note: Statistical significance of peaks
Display "  Significant peaks (Fisher's test):"
Let significance_test be TimeSeries.test_periodogram_peaks(periodogram_result, 0.05)
For Each peak in significance_test.significant_peaks:
    Display "    Frequency " joined with String(peak.frequency) joined with ": p-value = " joined with String(peak.p_value)
```

### Spectral Density Estimation
```runa
Note: Smooth spectral density estimation
Let spectral_config be Dictionary with:
    "method": "welch"
    "window": "hann"
    "overlap": "0.5"
    "nperseg": "8"

Let spectral_density be TimeSeries.estimate_spectral_density(ts_data, spectral_config)

Display "Spectral Density Estimation Results:"
Display "  Method: " joined with spectral_config["method"]
Display "  Window: " joined with spectral_config["window"]
Display "  Overlap: " joined with spectral_config["overlap"]

Display "  Peak frequencies in density estimate:"
Let density_peaks be TimeSeries.find_spectral_peaks(spectral_density.frequencies, spectral_density.density)
For Each peak in density_peaks:
    Display "    Frequency: " joined with String(peak.frequency) joined with ", Density: " joined with String(peak.density)
```

## Advanced Time Series Methods

### State Space Models
```runa
Note: Kalman filter for state space modeling
Let state_space_config be Dictionary with:
    "state_dimension": "2"
    "observation_dimension": "1"
    "process_noise": "0.1"
    "observation_noise": "0.2"

Let kalman_result be TimeSeries.kalman_filter(ts_data, state_space_config)

Display "Kalman Filter Results:"
Display "  State dimension: " joined with state_space_config["state_dimension"]
Display "  Observation dimension: " joined with state_space_config["observation_dimension"]
Display "  Log-likelihood: " joined with String(kalman_result.log_likelihood)

Display "  State estimates (last 5 periods):"
Let n_states be Length(kalman_result.filtered_states)
For i from n_states - 5 to n_states - 1:
    Display "    Period " joined with String(i + 1) joined with ": " joined with String(kalman_result.filtered_states[i])

Display "  Model fit statistics:"
Display "    AIC: " joined with String(kalman_result.aic)
Display "    Innovation variance: " joined with String(kalman_result.innovation_variance)
```

### Vector Autoregression (VAR)
```runa
Note: Multivariate time series modeling
Let multivariate_ts be [
    [10.2, 15.5], [10.8, 16.1], [11.1, 15.8], [10.5, 15.2], [9.8, 14.9],
    [10.3, 15.4], [11.2, 16.2], [11.7, 16.8], [12.1, 17.1], [11.9, 16.9],
    [11.4, 16.4], [10.9, 15.9], [11.8, 16.7], [12.3, 17.3], [12.7, 17.7]
]

Let var_model be TimeSeries.fit_var(multivariate_ts, 2, true)

Display "Vector Autoregression Results:"
Display "  VAR order (lags): " joined with String(var_model.order)
Display "  Number of variables: " joined with String(Length(multivariate_ts[0]))
Display "  Sample size: " joined with String(Length(multivariate_ts))
Display "  Include constant: true"

Display "  Model fit:"
Display "    Log-likelihood: " joined with String(var_model.log_likelihood)
Display "    AIC: " joined with String(var_model.aic)
Display "    BIC: " joined with String(var_model.bic)

Display "  Coefficient matrix (Variable 1 equation):"
For lag from 1 to var_model.order:
    Display "    Lag " joined with String(lag) joined with " coefficients: " joined with String(var_model.coefficients["var1"]["lag" joined with String(lag)])
```

### Cointegration Analysis
```runa
Note: Test for long-run equilibrium relationships
Let cointegration_result be TimeSeries.johansen_cointegration_test(multivariate_ts, 1, "constant")

Display "Johansen Cointegration Test Results:"
Display "  Deterministic trend: " joined with "constant"
Display "  Maximum lag order: 1"

Display "  Trace test:"
Display "    Null: r = 0, Statistic: " joined with String(cointegration_result.trace_statistics[0]) joined with ", Critical (5%): " joined with String(cointegration_result.trace_critical_values[0])
Display "    Null: r ≤ 1, Statistic: " joined with String(cointegration_result.trace_statistics[1]) joined with ", Critical (5%): " joined with String(cointegration_result.trace_critical_values[1])

Display "  Maximum eigenvalue test:"
Display "    Null: r = 0, Statistic: " joined with String(cointegration_result.max_eigen_statistics[0]) joined with ", Critical (5%): " joined with String(cointegration_result.max_eigen_critical_values[0])
Display "    Null: r = 1, Statistic: " joined with String(cointegration_result.max_eigen_statistics[1]) joined with ", Critical (5%): " joined with String(cointegration_result.max_eigen_critical_values[1])

Display "  Number of cointegrating vectors: " joined with String(cointegration_result.cointegrating_rank)

If cointegration_result.cointegrating_rank > 0:
    Display "  Cointegrating vector (normalized): " joined with String(cointegration_result.cointegrating_vectors[0])
```

### GARCH Models
```runa
Note: Model conditional heteroscedasticity
Let returns_data be [0.02, -0.01, 0.03, -0.02, 0.04, -0.03, 0.05, -0.01, 0.02, -0.02, 0.03, -0.04, 0.06, -0.02, 0.01]

Let garch_model be TimeSeries.fit_garch(returns_data, [1, 1], "normal")

Display "GARCH(1,1) Model Results:"
Display "  Distribution: Normal"
Display "  Convergence: " joined with String(garch_model.converged)
Display "  Log-likelihood: " joined with String(garch_model.log_likelihood)
Display "  AIC: " joined with String(garch_model.aic)

Display "  Parameters:"
Display "    ω (omega): " joined with String(garch_model.parameters["omega"]) joined with " (SE: " joined with String(garch_model.standard_errors["omega"]) joined with ")"
Display "    α (alpha): " joined with String(garch_model.parameters["alpha"]) joined with " (SE: " joined with String(garch_model.standard_errors["alpha"]) joined with ")"
Display "    β (beta): " joined with String(garch_model.parameters["beta"]) joined with " (SE: " joined with String(garch_model.standard_errors["beta"]) joined with ")"

Note: Volatility forecasting
Let volatility_forecast be TimeSeries.forecast_garch_volatility(garch_model, 5)
Display "  Volatility forecasts (next 5 periods):"
For i from 0 to Length(volatility_forecast.conditional_volatility) - 1:
    Display "    Period " joined with String(i + 1) joined with ": " joined with String(volatility_forecast.conditional_volatility[i])
```

## Model Selection and Comparison

### Automatic Model Selection
```runa
Note: Compare multiple forecasting methods
Let model_types be ["arima", "ets", "tbats", "neural_network"]
Let comparison_config be Dictionary with:
    "train_ratio": "0.8"
    "forecast_horizon": "4"
    "cross_validation": "true"
    "information_criterion": "aic"

Let model_comparison be TimeSeries.compare_forecast_methods(ts_data, model_types, comparison_config)

Display "Forecast Method Comparison:"
Display "  Training data: " joined with String(model_comparison.train_size) joined with " observations"
Display "  Test data: " joined with String(model_comparison.test_size) joined with " observations"

Display "  Model performance (test set):"
For Each model_name in model_types:
    Let model_results be model_comparison.model_results[model_name]
    Display "    " joined with model_name joined with ":"
    Display "      RMSE: " joined with String(model_results.rmse)
    Display "      MAE: " joined with String(model_results.mae)
    Display "      MAPE: " joined with String(model_results.mape) joined with "%"
    Display "      AIC: " joined with String(model_results.aic)

Display "  Best model: " joined with model_comparison.best_model joined with " (lowest RMSE)"
```

### Cross-Validation
```runa
Note: Time series cross-validation with expanding window
Let cv_config be Dictionary with:
    "initial_window": "10"
    "horizon": "2"
    "period": "1"
    "method": "expanding"

Let cv_results be TimeSeries.time_series_cross_validation(ts_data, [1, 1, 1], cv_config)

Display "Time Series Cross-Validation Results:"
Display "  Method: " joined with cv_config["method"] joined with " window"
Display "  Initial window: " joined with cv_config["initial_window"]
Display "  Forecast horizon: " joined with cv_config["horizon"]
Display "  Number of folds: " joined with String(cv_results.n_folds)

Display "  Cross-validation metrics:"
Display "    Mean RMSE: " joined with String(cv_results.mean_rmse) joined with " ± " joined with String(cv_results.std_rmse)
Display "    Mean MAE: " joined with String(cv_results.mean_mae) joined with " ± " joined with String(cv_results.std_mae)
Display "    Mean MAPE: " joined with String(cv_results.mean_mape) joined with "% ± " joined with String(cv_results.std_mape) joined with "%"

Display "  Individual fold performance:"
For fold from 1 to cv_results.n_folds:
    Display "    Fold " joined with String(fold) joined with ": RMSE = " joined with String(cv_results.fold_rmse[fold - 1])
```

## Error Handling and Validation

### Comprehensive Error Management
```runa
Note: Handle time series analysis errors
Try:
    Let insufficient_ts be [1.0, 2.0]  Note: Too short for ARIMA
    Let failed_arima be TimeSeries.fit_arima(insufficient_ts, [2, 1, 2], [0, 0, 0, 0])
Catch Errors.InsufficientData as error:
    Display "Time series length error: " joined with error.message
    Display "ARIMA models require sufficient data points for parameter estimation"

Try:
    Let non_convergent_order be [5, 2, 5]  Note: Over-parameterized
    Let failed_model be TimeSeries.fit_arima(ts_data, non_convergent_order, [0, 0, 0, 0])
Catch Errors.ConvergenceError as error:
    Display "Model convergence error: " joined with error.message
    Display "Consider reducing model complexity or increasing iterations"

Try:
    Let invalid_forecast_horizon be 100  Note: Too many periods ahead
    Let failed_forecast be TimeSeries.forecast_arima(arima_model, ts_data, invalid_forecast_horizon, [0.95])
Catch Errors.InvalidParameter as error:
    Display "Forecast horizon error: " joined with error.message
    Display "Forecast horizon should not exceed series length"
```

### Time Series Validation Framework
```runa
Process called "validate_time_series_analysis" that takes data as List[Float], analysis_type as String returns Dictionary[String, String]:
    Let validation_results be Dictionary[String, String]
    
    Note: Basic data validation
    Set validation_results["series_length"] to String(Length(data))
    Set validation_results["min_value"] to String(DescriptiveStats.calculate_range(data)["minimum"])
    Set validation_results["max_value"] to String(DescriptiveStats.calculate_range(data)["maximum"])
    
    Note: Check for missing values
    Let has_missing be check_missing_values_ts(data)
    Set validation_results["complete_series"] to String(not has_missing)
    
    Note: Stationarity assessment
    Let stationarity_check be TimeSeries.check_stationarity(data, ["adf"], 0.05)
    Set validation_results["stationary"] to String(stationarity_check["adf"]["conclusion"] == "stationary")
    
    Note: Seasonality detection
    Let seasonal_test be TimeSeries.test_seasonality(data, [4, 12])
    Set validation_results["seasonal_pattern"] to String(seasonal_test.has_seasonality)
    If seasonal_test.has_seasonality:
        Set validation_results["seasonal_period"] to String(seasonal_test.detected_period)
    
    Note: Analysis-specific validation
    If analysis_type == "arima":
        Let min_length be 20
        Set validation_results["sufficient_for_arima"] to String(Length(data) >= min_length)
        
        If not Boolean(validation_results["stationary"]):
            Set validation_results["needs_differencing"] to "true"
        Otherwise:
            Set validation_results["needs_differencing"] to "false"
    
    Otherwise if analysis_type == "seasonal_decomposition":
        Let min_cycles be 2
        Let seasonal_period be 4  Note: Default assumption
        If seasonal_test.has_seasonality:
            Set seasonal_period to seasonal_test.detected_period
        
        Let sufficient_for_decomp be Length(data) >= (min_cycles * seasonal_period)
        Set validation_results["sufficient_for_decomposition"] to String(sufficient_for_decomp)
        Set validation_results["min_required_length"] to String(min_cycles * seasonal_period)
    
    Note: Generate recommendations
    Let recommendations be []
    If has_missing:
        Call recommendations.append("Handle missing values before analysis")
    If analysis_type == "arima" and not Boolean(validation_results["stationary"]):
        Call recommendations.append("Apply differencing to achieve stationarity")
    If seasonal_test.has_seasonality and analysis_type == "arima":
        Call recommendations.append("Consider seasonal ARIMA (SARIMA) model")
    
    Set validation_results["recommendations"] to String(recommendations)
    Set validation_results["validation_complete"] to "true"
    
    Return validation_results

Note: Example validation
Let ts_validation be validate_time_series_analysis(ts_data, "arima")
Display "Time Series Analysis Validation:"
For Each key, value in ts_validation:
    Display "  " joined with key joined with ": " joined with value
```

<function_calls>
<invoke name="TodoWrite">
<parameter name="todos">[{"content": "Create guide for timeseries.runa", "status": "completed", "activeForm": "Creating guide for timeseries.runa"}]