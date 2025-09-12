Note: Math Statistics Module

The Math Statistics module (`math/statistics`) provides comprehensive statistical analysis capabilities for data science, research, and analytical computing. This module offers descriptive statistics, inferential testing, regression analysis, multivariate techniques, Bayesian methods, and time series analysis with high-precision computation and robust error handling.

## Module Overview

The Math Statistics module consists of six specialized submodules, each focusing on different aspects of statistical analysis:

| Submodule | Description | Key Features |
|-----------|-------------|--------------|
| **[Descriptive](descriptive.md)** | Descriptive statistics and data summarization | Central tendency, variability, distribution shape, quantiles, outlier detection |
| **[Inferential](inferential.md)** | Hypothesis testing and statistical inference | T-tests, ANOVA, chi-square, non-parametric tests, confidence intervals |
| **[Regression](regression.md)** | Linear and nonlinear regression analysis | OLS, multiple regression, logistic, regularized methods, model diagnostics |
| **[Bayesian](bayesian.md)** | Bayesian statistical methods | Prior/posterior inference, MCMC sampling, Bayesian hypothesis testing |
| **[Multivariate](multivariate.md)** | Multivariate statistical analysis | PCA, factor analysis, canonical correlation, cluster analysis |
| **[Timeseries](timeseries.md)** | Time series analysis and forecasting | ARIMA, seasonal decomposition, spectral analysis, forecasting methods |

## Quick Start

### Basic Descriptive Statistics
```runa
Import "math/statistics/descriptive" as Stats

Note: Analyze a dataset
Let data be [23.1, 25.6, 22.3, 28.9, 24.7, 26.2, 23.8, 25.1, 27.4, 24.9]
Let summary be Stats.generate_descriptive_summary(data, true)

Display "Mean: " joined with String(summary.mean)
Display "Median: " joined with String(summary.median)
Display "Standard Deviation: " joined with String(summary.standard_deviation)
Display "Skewness: " joined with String(summary.skewness)
Display "Kurtosis: " joined with String(summary.kurtosis)
```

### Hypothesis Testing
```runa
Import "math/statistics/inferential" as InfStats

Note: Perform a t-test
Let sample1 be [12.3, 14.2, 13.1, 15.8, 12.9, 14.5, 13.7]
Let sample2 be [16.2, 17.8, 15.9, 18.1, 16.7, 17.3, 16.4]

Let ttest_result be InfStats.independent_samples_t_test(sample1, sample2, "two-tailed", true)
Display "T-statistic: " joined with String(ttest_result.test_statistic)
Display "P-value: " joined with String(ttest_result.p_value)
Display "Significant at α=0.05: " joined with String(ttest_result.p_value < 0.05)
```

### Simple Linear Regression
```runa
Import "math/statistics/regression" as Regression

Note: Fit regression model
Let x_values be [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
Let y_values be [2.1, 3.9, 6.2, 7.8, 10.1, 12.3, 14.0, 15.8]

Let model be Regression.simple_linear_regression(x_values, y_values)
Display "Slope: " joined with String(model.coefficients[0])
Display "Intercept: " joined with String(model.intercept)
Display "R-squared: " joined with String(model.r_squared)
Display "Model equation: y = " joined with String(model.intercept) joined with " + " joined with String(model.coefficients[0]) joined with "*x"
```

### Principal Component Analysis
```runa
Import "math/statistics/multivariate" as Multivariate

Note: Reduce dimensionality of dataset
Let data_matrix be [
    [2.5, 2.4, 3.1, 2.8],
    [0.5, 0.7, 1.2, 0.9],
    [2.2, 2.9, 3.0, 2.7],
    [1.9, 2.2, 2.8, 2.1],
    [3.1, 3.0, 3.8, 3.2]
]

Let pca_result be Multivariate.principal_component_analysis(data_matrix, true, 2)
Display "Explained variance ratios:"
For i from 0 to Length(pca_result.explained_variance_ratio) - 1:
    Display "PC" joined with String(i + 1) joined with ": " joined with String(pca_result.explained_variance_ratio[i] * 100.0) joined with "%"
```

### Time Series Analysis
```runa
Import "math/statistics/timeseries" as TimeSeries

Note: Analyze time series data
Let ts_data be [10.2, 10.8, 11.1, 10.5, 9.8, 10.3, 11.2, 11.7, 12.1, 11.9, 11.4, 10.9]
Let timestamps be [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

Note: Decompose seasonal pattern
Let decomposition be TimeSeries.seasonal_decomposition(ts_data, 4, "additive")
Display "Trend component extracted: " joined with String(Length(decomposition.trend)) joined with " values"
Display "Seasonal strength: " joined with String(decomposition.seasonal_strength)

Note: Check for stationarity
Let stationarity_tests be TimeSeries.check_stationarity(ts_data, ["adf"], 0.05)
Display "ADF test p-value: " joined with String(stationarity_tests["adf"]["p_value"])
```

## Architecture and Design

### High-Precision Statistical Computing
All statistical operations support arbitrary precision arithmetic and robust numerical methods:

- **BigDecimal Integration**: High-precision calculations for critical statistical tests
- **Numerical Stability**: Numerically stable algorithms (Welford's method, etc.)
- **Error Propagation**: Statistical error estimation and confidence intervals
- **Robust Methods**: Resistant estimators and outlier detection

### Comprehensive Statistical Framework
The module provides a complete statistical analysis ecosystem:

```runa
Note: End-to-end statistical workflow
Import "math/statistics/descriptive" as Desc
Import "math/statistics/inferential" as Inf
Import "math/statistics/regression" as Reg

Let raw_data be load_dataset("research_data.csv")

Note: 1. Exploratory data analysis
Let summary be Desc.generate_statistical_profile(raw_data, Dictionary with: "include_robust": "true")
Let outliers be Desc.detect_outliers_iqr(raw_data, 1.5)

Note: 2. Data preprocessing  
Let cleaned_data be Desc.handle_missing_values(raw_data, "median_imputation")
Let transformed_data be Desc.transform_data(cleaned_data, "standardize")

Note: 3. Statistical testing
Let normality be Desc.assess_normality(transformed_data, 0.05)
If not normality["is_normal"]:
    Display "Data is not normally distributed, using non-parametric tests"

Note: 4. Model fitting and validation
Let model be Reg.multiple_linear_regression(predictors, response, true)
Let diagnostics be Reg.regression_diagnostics(model, "comprehensive")
```

## Statistical Methods Coverage

### Descriptive Statistics
- **Central Tendency**: Arithmetic, geometric, harmonic means; median; mode
- **Variability**: Variance, standard deviation, range, IQR, coefficient of variation
- **Distribution Shape**: Skewness, kurtosis, moments analysis, normality testing
- **Robust Statistics**: Trimmed means, Winsorized statistics, MAD, Hodges-Lehmann

### Inferential Statistics
- **Parametric Tests**: T-tests, ANOVA, F-tests, Z-tests
- **Non-parametric Tests**: Mann-Whitney U, Wilcoxon, Kruskal-Wallis, chi-square
- **Correlation Analysis**: Pearson, Spearman, Kendall correlations
- **Confidence Intervals**: Bootstrap, analytical, exact methods

### Regression Analysis
- **Linear Models**: Simple/multiple regression, polynomial regression
- **Regularized Methods**: Ridge, Lasso, Elastic Net regression
- **Logistic Regression**: Binary and multinomial classification
- **Model Diagnostics**: Residual analysis, influence measures, multicollinearity

### Advanced Methods
- **Bayesian Statistics**: Prior specification, posterior inference, credible intervals
- **Multivariate Analysis**: PCA, factor analysis, discriminant analysis
- **Time Series**: ARIMA modeling, seasonal decomposition, forecasting
- **Resampling Methods**: Bootstrap, permutation tests, cross-validation

## Data Structures and Types

### Statistical Results
```runa
Type called "StatisticalTest":
    test_statistic as Float
    p_value as Float
    critical_value as Float
    degrees_of_freedom as Float
    effect_size as Float
    confidence_interval as List[Float]
    test_assumptions as Dictionary[String, Boolean]
    diagnostic_info as Dictionary[String, Float]

Type called "ModelFit":
    coefficients as List[Float]
    standard_errors as List[Float]
    fit_statistics as Dictionary[String, Float]
    residuals as List[Float]
    predictions as List[Float]
    diagnostics as Dictionary[String, List[Float]]
```

## Performance and Scalability

### Computational Efficiency
- **Algorithm Selection**: Automatic optimal algorithm selection based on data characteristics
- **Parallel Processing**: Multi-threaded statistical computations
- **Memory Management**: Efficient handling of large datasets
- **Numerical Optimization**: Fast convergence for iterative methods

### Benchmarking Results
```runa
Note: Performance benchmarks (1M observations)
Let benchmark_data be generate_benchmark_dataset(1000000)

Note: Descriptive statistics timing
Let desc_time be Desc.benchmark_descriptive_operations(benchmark_data)
Display "Mean calculation: " joined with String(desc_time["mean"]) joined with " ms"
Display "Standard deviation: " joined with String(desc_time["std_dev"]) joined with " ms"

Note: Regression timing
Let reg_time be Reg.benchmark_regression_performance(benchmark_data)
Display "Linear regression fit: " joined with String(reg_time["simple_regression"]) joined with " ms"
```

## Integration with Other Modules

### Math Engine Dependencies
- **Linear Algebra**: Matrix operations, eigenvalue decomposition, SVD
- **Numerical Methods**: Root finding, optimization, integration
- **Probability Distributions**: PDF, CDF, quantile functions
- **Fourier Analysis**: Spectral analysis, time-frequency methods

### Data Processing Pipeline
```runa
Note: Integrated statistical workflow
Import "math/statistics/descriptive" as Desc
Import "math/engine/linalg/core" as LinAlg
Import "math/probability/distributions" as Prob

Process called "comprehensive_analysis" that takes data as List[Float] returns Dictionary[String, Dictionary[String, Float]]:
    Let results be Dictionary[String, Dictionary[String, Float]]
    
    Note: Descriptive analysis
    Let desc_results be Desc.generate_statistical_profile(data, Dictionary with: "robust": "true")
    Set results["descriptive"] to desc_results["basic_statistics"]
    
    Note: Distribution fitting
    Let normal_fit be Prob.fit_normal_distribution(data)
    Set results["distribution_fit"] to normal_fit
    
    Note: Outlier analysis
    Let outlier_info be Desc.detect_outliers_iqr(data, 1.5)
    Set results["outliers"] to Dictionary with: "count": String(Length(outlier_info))
    
    Return results
```

## Common Use Cases

### Quality Control Analysis
```runa
Note: Statistical process control
Import "math/statistics/descriptive" as Stats
Import "math/statistics/inferential" as Tests

Let process_data be [98.2, 99.1, 98.7, 99.3, 98.9, 99.0, 98.5, 99.2, 98.8, 99.1]
Let control_limits be Stats.calculate_control_limits(process_data, "x_bar", 3.0)

Display "Upper Control Limit: " joined with String(control_limits["ucl"])
Display "Center Line: " joined with String(control_limits["center_line"])  
Display "Lower Control Limit: " joined with String(control_limits["lcl"])

Note: Check for special causes
Let out_of_control be Stats.detect_control_violations(process_data, control_limits)
If Length(out_of_control) > 0:
    Display "Process out of control at points: " joined with String(out_of_control)
```

### A/B Testing Framework
```runa
Note: A/B test statistical analysis
Let control_group be [0.12, 0.15, 0.13, 0.11, 0.14, 0.12, 0.16, 0.13, 0.12, 0.15]
Let treatment_group be [0.18, 0.21, 0.19, 0.17, 0.20, 0.18, 0.22, 0.19, 0.18, 0.21]

Let ab_test_result be Tests.ab_test_analysis(control_group, treatment_group, "conversion_rate")

Display "Control mean: " joined with String(ab_test_result.control_mean)
Display "Treatment mean: " joined with String(ab_test_result.treatment_mean)
Display "Lift: " joined with String(ab_test_result.relative_lift * 100.0) joined with "%"
Display "Statistical significance: " joined with String(ab_test_result.is_significant)
Display "Confidence interval: [" joined with String(ab_test_result.confidence_interval[0]) joined with ", " joined with String(ab_test_result.confidence_interval[1]) joined with "]"
```

### Financial Risk Analysis
```runa
Note: Portfolio risk analysis
Import "math/statistics/multivariate" as Multi
Import "math/statistics/timeseries" as TS

Let returns_data be [
    [0.02, -0.01, 0.03, 0.01],  Note: Asset 1 returns
    [0.01, 0.02, -0.01, 0.02],  Note: Asset 2 returns  
    [-0.01, 0.01, 0.02, 0.01],  Note: Asset 3 returns
    [0.03, 0.01, -0.02, 0.02]   Note: Asset 4 returns
]

Note: Calculate portfolio risk metrics
Let covariance_matrix be Multi.compute_sample_covariance_matrix(returns_data)
Let correlation_matrix be Multi.compute_correlation_matrix(returns_data)

Note: Portfolio optimization (equal weights)
Let weights be [0.25, 0.25, 0.25, 0.25]
Let portfolio_variance be Multi.calculate_portfolio_variance(weights, covariance_matrix)
Let portfolio_vol be MathOps.square_root(String(portfolio_variance), 15).result_value

Display "Portfolio volatility: " joined with String(Float(portfolio_vol) * 100.0) joined with "%"
```

### Clinical Trial Analysis
```runa
Note: Clinical trial statistical analysis
Let baseline_scores be [65, 68, 62, 71, 66, 69, 63, 70, 67, 64]
Let followup_scores be [72, 75, 69, 78, 73, 76, 70, 77, 74, 71]

Note: Paired t-test for before/after comparison
Let paired_test be Tests.paired_samples_t_test(baseline_scores, followup_scores, "two-tailed")

Display "Mean improvement: " joined with String(paired_test.mean_difference)
Display "95% CI for difference: [" joined with String(paired_test.confidence_interval[0]) joined with ", " joined with String(paired_test.confidence_interval[1]) joined with "]"
Display "Effect size (Cohen's d): " joined with String(paired_test.effect_size)
Display "Clinical significance: " joined with String(paired_test.mean_difference > 5.0)  Note: Minimum clinically important difference
```

## Error Handling and Validation

### Comprehensive Error Checking
```runa
Try:
    Let analysis_result be perform_statistical_analysis(data)
Catch Errors.InsufficientDataError as error:
    Display "Insufficient data for analysis: " joined with error.message
    Display "Minimum required: " joined with String(error.minimum_required)
Catch Errors.AssumptionViolationError as error:
    Display "Statistical assumption violated: " joined with error.assumption
    Display "Suggested alternative: " joined with error.alternative_method
Catch Errors.ConvergenceError as error:
    Display "Algorithm failed to converge: " joined with error.message
    Display "Iterations completed: " joined with String(error.iterations)
```

### Input Validation
```runa
Process called "validate_statistical_inputs" that takes data as List[Float], test_type as String returns Dictionary[String, Boolean]:
    Let validation_results be Dictionary[String, Boolean]
    
    Note: Check sample size requirements
    Set validation_results["sufficient_sample_size"] to Length(data) >= get_minimum_sample_size(test_type)
    
    Note: Check for missing values
    Set validation_results["no_missing_values"] to not contains_missing_values(data)
    
    Note: Check numerical validity
    Set validation_results["all_finite"] to all_values_finite(data)
    
    Return validation_results
```

## Best Practices

### Statistical Analysis Workflow
1. **Exploratory Data Analysis**: Always start with descriptive statistics and visualization
2. **Assumption Checking**: Validate statistical assumptions before applying tests
3. **Effect Size Reporting**: Report both statistical significance and practical significance
4. **Multiple Comparisons**: Apply appropriate corrections for multiple testing
5. **Cross-Validation**: Use resampling methods to assess model generalizability

### Code Examples
```runa
Note: Best practice statistical workflow
Process called "robust_statistical_analysis" that takes data as List[Float], alpha as Float returns Dictionary[String, String]:
    Let results be Dictionary[String, String]
    
    Note: Step 1: Data quality assessment
    Let missing_count be count_missing_values(data)
    If missing_count > 0:
        Set data to handle_missing_values(data, "median_imputation")
        Set results["data_preprocessing"] to "Missing values imputed using median"
    
    Note: Step 2: Outlier detection and handling
    Let outliers be Desc.detect_outliers_iqr(data, 1.5)
    If Length(outliers) > 0:
        Set results["outlier_analysis"] to "Found " joined with String(Length(outliers)) joined with " outliers"
        Let winsorized_data be Desc.calculate_winsorized_mean(data, [5.0, 95.0])
    
    Note: Step 3: Distribution assessment
    Let normality_test be Desc.assess_normality(data, alpha)
    Set results["normality_check"] to "Normally distributed: " joined with String(normality_test["is_normal"])
    
    Note: Step 4: Descriptive statistics with confidence intervals
    Let summary be Desc.generate_descriptive_summary(data, true)
    Let bootstrap_ci be Desc.bootstrap_statistic(data, "mean", 1000)
    Let ci_bounds be Desc.calculate_percentiles(bootstrap_ci, [2.5, 97.5], "linear")
    
    Set results["mean_estimate"] to String(summary.mean)
    Set results["mean_ci"] to "[" joined with String(ci_bounds["2.5"]) joined with ", " joined with String(ci_bounds["97.5"]) joined with "]"
    
    Return results
```

## Performance Guidelines

### Memory and Computational Efficiency
- **Large Datasets**: Use streaming algorithms for datasets > 1M observations
- **Parallel Processing**: Leverage multi-core processing for computationally intensive analyses
- **Precision Trade-offs**: Balance numerical precision with computational speed
- **Algorithm Selection**: Choose appropriate algorithms based on data characteristics

## Related Documentation

- **[Math Core](../core/README.md)**: Fundamental mathematical operations and precision arithmetic
- **[Math Engine](../engine/README.md)**: Advanced numerical methods and linear algebra
- **[Math Probability](../probability/README.md)**: Probability distributions and random sampling
- **[Math Analysis](../analysis/README.md)**: Mathematical analysis and calculus methods

## Support and Community

For questions, bug reports, or feature requests related to statistical analysis:

1. **Documentation**: Consult the detailed submodule guides for specific functionality
2. **Examples**: Review the comprehensive examples in each guide
3. **Validation**: Use built-in diagnostic tools to verify results
4. **Performance**: Benchmark operations with representative data sizes

The Math Statistics module provides a complete statistical analysis framework suitable for research, data science, quality control, and advanced analytics applications. Its integration with Runa's high-precision arithmetic and numerical engines ensures reliable and accurate statistical computations.