Note: Math Statistics Descriptive Module

## Overview

The `math/statistics/descriptive` module provides comprehensive descriptive statistics operations for data summarization and exploratory analysis. It includes measures of central tendency (mean, median, mode), variability (standard deviation, variance, range), distribution shape (skewness, kurtosis), quantile analysis, robust statistics, and advanced data profiling capabilities.

## Key Features

- **Central Tendency**: Multiple mean types, median with interpolation, mode detection
- **Variability Measures**: Variance, standard deviation, range statistics, coefficient of variation
- **Distribution Shape**: Skewness, kurtosis, moments analysis, normality assessment  
- **Quantile Analysis**: Percentiles, quartiles, quantile functions, outlier detection
- **Robust Statistics**: Trimmed means, Winsorized statistics, robust scale estimators
- **Data Transformation**: Standardization, normalization, missing value handling
- **Comprehensive Profiling**: Five-number summaries, frequency distributions

## Data Types

### StatisticalSummary
Complete descriptive statistics summary:
```runa
Type called "StatisticalSummary":
    sample_size as Integer
    mean as Float
    median as Float
    mode as List[Float]
    standard_deviation as Float
    variance as Float
    minimum as Float
    maximum as Float
    range as Float
    interquartile_range as Float
    skewness as Float
    kurtosis as Float
```

### MomentsAnalysis
Statistical moments and moment-related measures:
```runa
Type called "MomentsAnalysis":
    raw_moments as List[Float]
    central_moments as List[Float]
    standardized_moments as List[Float]
    moment_generating_function as Dictionary[String, Float]
    cumulants as List[Float]
    moment_order as Integer
```

## Central Tendency Operations

### Arithmetic Mean
```runa
Import "math/statistics/descriptive" as Stats

Note: Simple arithmetic mean
Let data be [12.5, 14.2, 13.8, 15.1, 12.9, 14.7, 13.3, 14.9]
Let mean_value be Stats.calculate_arithmetic_mean(data, [])
Display "Arithmetic mean: " joined with String(mean_value)

Note: Weighted arithmetic mean
Let values be [85.0, 90.0, 78.0, 92.0, 88.0]
Let weights be [0.3, 0.25, 0.15, 0.2, 0.1]
Let weighted_mean be Stats.calculate_arithmetic_mean(values, weights)
Display "Weighted mean: " joined with String(weighted_mean)
```

### Geometric Mean
```runa
Note: Geometric mean for growth rates
Let growth_rates be [1.05, 1.08, 1.03, 1.12, 1.07]  Note: 5%, 8%, 3%, 12%, 7% growth
Let geometric_mean be Stats.calculate_geometric_mean(growth_rates, false)
Display "Average growth rate: " joined with String((geometric_mean - 1.0) * 100.0) joined with "%"

Note: Geometric mean with negative value handling
Let mixed_data be [4.0, -2.0, 6.0, 8.0]
Let geo_mean_abs be Stats.calculate_geometric_mean(mixed_data, true)
Display "Geometric mean (absolute values): " joined with String(geo_mean_abs)
```

### Harmonic Mean
```runa
Note: Harmonic mean for rates and ratios
Let speeds be [60.0, 80.0, 70.0, 90.0]  Note: km/h
Let harmonic_mean be Stats.calculate_harmonic_mean(speeds, false)
Display "Harmonic mean speed: " joined with String(harmonic_mean) joined with " km/h"

Note: Harmonic mean excluding zeros
Let rates_with_zero be [5.0, 0.0, 8.0, 6.0, 7.0]
Let harm_mean_no_zero be Stats.calculate_harmonic_mean(rates_with_zero, true)
Display "Harmonic mean (excluding zeros): " joined with String(harm_mean_no_zero)
```

### Median and Mode
```runa
Note: Median with different interpolation methods
Let dataset be [1.2, 3.4, 2.8, 5.1, 4.7, 3.9, 2.1, 4.3]

Let median_linear be Stats.find_median(dataset, "linear")
Let median_lower be Stats.find_median(dataset, "lower")
Let median_higher be Stats.find_median(dataset, "higher")

Display "Linear interpolation median: " joined with String(median_linear)
Display "Lower value median: " joined with String(median_lower)  
Display "Higher value median: " joined with String(median_higher)

Note: Mode detection with tolerance
Let continuous_data be [2.1, 2.15, 2.12, 3.8, 3.82, 2.11, 5.4, 3.79]
Let modes be Stats.find_mode(continuous_data, 0.05)  Note: 0.05 tolerance for binning
Display "Modes found:"
For Each mode_value in modes:
    Display "  " joined with String(mode_value)
```

## Variability Measures

### Variance and Standard Deviation
```runa
Note: Sample vs population variance
Let sample_data be [23.1, 25.6, 22.3, 28.9, 24.7, 26.2, 23.8, 25.1]

Let sample_variance be Stats.calculate_variance(sample_data, false, true)
Let population_variance be Stats.calculate_variance(sample_data, true, false)

Display "Sample variance (Bessel correction): " joined with String(sample_variance)
Display "Population variance: " joined with String(population_variance)

Let sample_std be Stats.calculate_standard_deviation(sample_data, false)
Let population_std be Stats.calculate_standard_deviation(sample_data, true)

Display "Sample standard deviation: " joined with String(sample_std)
Display "Population standard deviation: " joined with String(population_std)
```

### Range Statistics
```runa
Note: Comprehensive range analysis
Let measurements be [45.2, 48.7, 44.1, 52.3, 46.8, 49.2, 47.5, 50.1, 43.9, 51.2]
Let range_stats be Stats.calculate_range(measurements)

Display "Minimum: " joined with String(range_stats["minimum"])
Display "Maximum: " joined with String(range_stats["maximum"])
Display "Range: " joined with String(range_stats["range"])
Display "First Quartile (Q1): " joined with String(range_stats["Q1"])
Display "Third Quartile (Q3): " joined with String(range_stats["Q3"])
Display "Interquartile Range (IQR): " joined with String(range_stats["IQR"])
Display "Lower outlier boundary: " joined with String(range_stats["lower_outlier_boundary"])
Display "Upper outlier boundary: " joined with String(range_stats["upper_outlier_boundary"])
```

### Coefficient of Variation and MAD
```runa
Note: Relative variability measures
Let test_scores be [78.5, 82.1, 75.9, 88.3, 79.7, 84.2, 76.8, 85.9]
Let cv be Stats.calculate_coefficient_of_variation(test_scores)
Display "Coefficient of variation: " joined with String(cv) joined with "%"

Note: Mean absolute deviation from different centers
Let mad_from_mean be Stats.calculate_mean_absolute_deviation(test_scores, "mean")
Let mad_from_median be Stats.calculate_mean_absolute_deviation(test_scores, "median")
Let mad_from_mode be Stats.calculate_mean_absolute_deviation(test_scores, "mode")

Display "MAD from mean: " joined with String(mad_from_mean)
Display "MAD from median: " joined with String(mad_from_median)
Display "MAD from mode: " joined with String(mad_from_mode)
```

## Quantile Analysis

### Percentiles and Quartiles
```runa
Note: Calculate specific percentiles
Let exam_scores be [65, 72, 78, 81, 85, 88, 91, 94, 96, 98]
Let percentiles_to_calc be [10.0, 25.0, 50.0, 75.0, 90.0, 95.0, 99.0]
Let percentile_results be Stats.calculate_percentiles(exam_scores, percentiles_to_calc, "linear")

Display "Percentile analysis:"
For Each p in percentiles_to_calc:
    Let key be String(p)
    Display "  " joined with key joined with "th percentile: " joined with String(percentile_results[key])

Note: Detailed quartile analysis
Let quartile_analysis be Stats.calculate_quartiles(exam_scores)
Display "Quartile analysis:"
Display "  Q1 (25th percentile): " joined with String(quartile_analysis["Q1"])
Display "  Q2 (median): " joined with String(quartile_analysis["Q2"])  
Display "  Q3 (75th percentile): " joined with String(quartile_analysis["Q3"])
Display "  IQR: " joined with String(quartile_analysis["IQR"])
```

### Quantile Function and Outlier Detection
```runa
Note: Inverse distribution function
Let probability_levels be [0.1, 0.25, 0.5, 0.75, 0.9]
Let quantile_function be Stats.calculate_quantile_function(exam_scores, probability_levels)

Display "Quantile function values:"
For Each prob in probability_levels:
    Let prob_key be String(prob)
    Display "  P=" joined with prob_key joined with ": " joined with String(quantile_function[prob_key])

Note: Outlier detection using IQR method
Let data_with_outliers be [12, 14, 13, 15, 14, 13, 16, 14, 35, 15, 13, 14, 12, 16, 2]
Let outlier_indices be Stats.detect_outliers_iqr(data_with_outliers, 1.5)

Display "Outliers detected at indices:"
For Each index in outlier_indices:
    Display "  Index " joined with String(index) joined with ": value = " joined with String(data_with_outliers[index])
```

## Distribution Shape Analysis

### Skewness and Kurtosis
```runa
Note: Measure distribution asymmetry and tail heaviness
Let symmetric_data be [1.0, 2.0, 3.0, 4.0, 5.0, 4.0, 3.0, 2.0, 1.0]
Let skewed_data be [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 12.0, 15.0, 20.0]

Let sym_skewness be Stats.calculate_skewness(symmetric_data, "Fisher")
Let skewed_skewness be Stats.calculate_skewness(skewed_data, "Fisher")

Display "Symmetric data skewness: " joined with String(sym_skewness)
Display "Right-skewed data skewness: " joined with String(skewed_skewness)

Note: Kurtosis analysis (excess kurtosis)
Let normal_like be [1.5, 2.3, 2.8, 3.1, 3.4, 3.7, 4.1, 4.5, 4.8, 5.2]
Let heavy_tailed be [1.0, 3.0, 3.1, 3.2, 3.3, 3.7, 3.8, 3.9, 4.0, 7.0]

Let normal_kurtosis be Stats.calculate_kurtosis(normal_like, true)
Let heavy_kurtosis be Stats.calculate_kurtosis(heavy_tailed, true)

Display "Normal-like excess kurtosis: " joined with String(normal_kurtosis)
Display "Heavy-tailed excess kurtosis: " joined with String(heavy_kurtosis)
```

### Normality Assessment
```runa
Note: Comprehensive normality testing
Let sample_data be [23.1, 25.6, 22.3, 28.9, 24.7, 26.2, 23.8, 25.1, 27.4, 24.9, 23.5, 26.8]
Let normality_results be Stats.assess_normality(sample_data, 0.05)

Display "Normality assessment results:"
Display "  Skewness: " joined with String(normality_results["skewness"])
Display "  Excess kurtosis: " joined with String(normality_results["excess_kurtosis"])
Display "  Normality score: " joined with String(normality_results["normality_score"])
Display "  Is normal (α=0.05): " joined with String(normality_results["is_normal"] > 0.0)

Note: Moments analysis
Let moments_result be Stats.calculate_moments(sample_data, 4, true)
Display "Moments analysis:"
For order from 0 to 4:
    Display "  Raw moment " joined with String(order) joined with ": " joined with String(moments_result.raw_moments[order])
    Display "  Central moment " joined with String(order) joined with ": " joined with String(moments_result.central_moments[order])
```

## Robust Statistics

### Trimmed and Winsorized Statistics
```runa
Note: Robust central tendency measures
Let data_with_extremes be [12.1, 13.5, 12.8, 14.2, 13.1, 15.7, 12.9, 45.2, 13.8, 14.1]

Note: Trimmed mean (remove 10% from each tail)
Let trimmed_mean be Stats.calculate_trimmed_mean(data_with_extremes, 10.0)
Display "10% trimmed mean: " joined with String(trimmed_mean)

Note: Winsorized mean (replace extremes with 5th and 95th percentiles)
Let winsorized_mean be Stats.calculate_winsorized_mean(data_with_extremes, [5.0, 95.0])
Display "Winsorized mean (5-95%): " joined with String(winsorized_mean)

Note: Compare with regular mean
Let regular_mean be Stats.calculate_arithmetic_mean(data_with_extremes, [])
Display "Regular mean: " joined with String(regular_mean)
Display "Impact of outliers: " joined with String(regular_mean - trimmed_mean)
```

### Robust Scale Estimators
```runa
Note: Robust measures of spread
Let noisy_data be [5.1, 5.3, 4.9, 5.2, 5.0, 5.4, 4.8, 8.7, 5.1, 4.9, 5.3, 5.2]

Let mad_scale be Stats.calculate_robust_scale(noisy_data, "MAD")
Let iqr_scale be Stats.calculate_robust_scale(noisy_data, "IQR")  
Let rc_scale be Stats.calculate_robust_scale(noisy_data, "Rousseeuw-Croux")

Display "Median Absolute Deviation (MAD): " joined with String(mad_scale)
Display "Interquartile Range (IQR): " joined with String(iqr_scale)
Display "Rousseeuw-Croux estimator: " joined with String(rc_scale)

Note: Compare with standard deviation
Let std_dev be Stats.calculate_standard_deviation(noisy_data, false)
Display "Standard deviation: " joined with String(std_dev)

Note: Hodges-Lehmann location estimator
Let hl_estimator be Stats.calculate_hodges_lehmann_estimator(noisy_data)
Display "Hodges-Lehmann estimator: " joined with String(hl_estimator)
```

## Comprehensive Summary Operations

### Complete Statistical Profile
```runa
Note: Generate comprehensive descriptive summary
Let research_data be [45.2, 48.7, 44.1, 52.3, 46.8, 49.2, 47.5, 50.1, 43.9, 51.2, 45.8, 47.9, 46.3, 49.8, 48.1]
Let summary be Stats.generate_descriptive_summary(research_data, true)

Display "Complete Statistical Summary:"
Display "  Sample size: " joined with String(summary.sample_size)
Display "  Mean: " joined with String(summary.mean)
Display "  Median: " joined with String(summary.median)
Display "  Mode(s): " joined with String(summary.mode)
Display "  Standard deviation: " joined with String(summary.standard_deviation)
Display "  Variance: " joined with String(summary.variance)
Display "  Minimum: " joined with String(summary.minimum)
Display "  Maximum: " joined with String(summary.maximum)
Display "  Range: " joined with String(summary.range)
Display "  Interquartile range: " joined with String(summary.interquartile_range)
Display "  Skewness: " joined with String(summary.skewness)
Display "  Kurtosis: " joined with String(summary.kurtosis)
```

### Five-Number Summary and Box Plot Data
```runa
Note: Box plot summary statistics
Let boxplot_data be Stats.create_five_number_summary(research_data)

Display "Five-number summary (box plot data):"
Display "  Minimum: " joined with String(boxplot_data["minimum"])
Display "  Q1 (lower quartile): " joined with String(boxplot_data["Q1"])
Display "  Median: " joined with String(boxplot_data["median"])
Display "  Q3 (upper quartile): " joined with String(boxplot_data["Q3"])
Display "  Maximum: " joined with String(boxplot_data["maximum"])
Display "  IQR: " joined with String(boxplot_data["IQR"])
Display "  Lower fence: " joined with String(boxplot_data["lower_fence"])
Display "  Upper fence: " joined with String(boxplot_data["upper_fence"])
Display "  Number of outliers: " joined with String(boxplot_data["outlier_count"])
```

### Frequency Distribution Analysis
```runa
Note: Create frequency distribution with different binning methods
Let continuous_data be [1.2, 2.8, 3.4, 2.1, 4.7, 3.9, 2.3, 4.1, 3.7, 2.9, 4.5, 3.2, 2.7, 4.3, 3.6]

Note: Equal-width bins
Let freq_equal_width be Stats.calculate_frequency_distribution(continuous_data, 5, "equal-width")
Display "Equal-width frequency distribution:"
Display "  Number of bins: " joined with String(Length(freq_equal_width["bin_centers"]))
For i from 0 to Length(freq_equal_width["bin_centers"]) - 1:
    Display "  Bin " joined with String(i + 1) joined with " [" joined with String(freq_equal_width["bin_edges"][i]) joined with "-" joined with String(freq_equal_width["bin_edges"][i + 1]) joined with "): count=" joined with String(freq_equal_width["bin_counts"][i])

Note: Sturges' rule for optimal bin count
Let freq_sturges be Stats.calculate_frequency_distribution(continuous_data, 0, "Sturges")
Display "Sturges rule bin count: " joined with String(Length(freq_sturges["bin_centers"]))

Note: Scott's rule for optimal bin width
Let freq_scott be Stats.calculate_frequency_distribution(continuous_data, 0, "Scott")
Display "Scott's rule bin count: " joined with String(Length(freq_scott["bin_centers"]))
```

## Data Processing and Transformation

### Missing Value Handling
```runa
Note: Different approaches to missing value treatment
Let data_with_missing be [5.2, -999999.0, 4.8, 5.1, -999999.0, 4.9, 5.3, 5.0]  Note: -999999.0 represents missing

Note: Listwise deletion
Let complete_cases be Stats.handle_missing_values(data_with_missing, "listwise_deletion")
Display "Complete cases (listwise deletion): " joined with String(Length(complete_cases)) joined with " values"

Note: Mean imputation
Let mean_imputed be Stats.handle_missing_values(data_with_missing, "mean_imputation")
Display "Mean imputed data:"
For Each value in mean_imputed:
    Display "  " joined with String(value)

Note: Median imputation  
Let median_imputed be Stats.handle_missing_values(data_with_missing, "median_imputation")
Display "Median imputed data:"
For Each value in median_imputed:
    Display "  " joined with String(value)
```

### Data Transformations
```runa
Note: Various data transformations for normalization and analysis
Let skewed_data be [1.2, 2.8, 3.4, 5.7, 8.9, 15.2, 28.4, 45.1, 67.8, 89.2]

Note: Logarithmic transformation
Let log_transformed be Stats.transform_data(skewed_data, "natural_log")
Display "Natural log transformed (first 5 values):"
For i from 0 to 4:
    Display "  Original: " joined with String(skewed_data[i]) joined with " → Log: " joined with String(log_transformed[i])

Note: Square root transformation
Let sqrt_transformed be Stats.transform_data(skewed_data, "square_root")
Display "Square root transformed (first 5 values):"
For i from 0 to 4:
    Display "  Original: " joined with String(skewed_data[i]) joined with " → Sqrt: " joined with String(sqrt_transformed[i])

Note: Standardization (Z-score)
Let standardized be Stats.transform_data(skewed_data, "standardize")
Display "Standardized data (Z-scores, first 5 values):"
For i from 0 to 4:
    Display "  Z-score: " joined with String(standardized[i])

Note: Min-Max normalization
Let normalized be Stats.transform_data(skewed_data, "normalize")
Display "Min-Max normalized (0-1 range, first 5 values):"
For i from 0 to 4:
    Display "  Normalized: " joined with String(normalized[i])
```

### Bootstrap Resampling
```runa
Note: Bootstrap sampling for uncertainty quantification
Let original_sample be [12.3, 14.7, 13.1, 15.8, 12.9, 14.2, 13.6, 15.1, 12.8, 14.5]
Let bootstrap_samples be 1000

Note: Bootstrap distribution of the mean
Let bootstrap_means be Stats.bootstrap_statistic(original_sample, "mean", bootstrap_samples)
Let bootstrap_summary be Stats.generate_descriptive_summary(bootstrap_means, false)

Display "Bootstrap analysis of the mean:"
Display "  Original sample mean: " joined with String(Stats.calculate_arithmetic_mean(original_sample, []))
Display "  Bootstrap mean estimate: " joined with String(bootstrap_summary.mean)
Display "  Bootstrap standard error: " joined with String(bootstrap_summary.standard_deviation)

Note: Bootstrap confidence interval for the mean
Let bootstrap_percentiles be Stats.calculate_percentiles(bootstrap_means, [2.5, 97.5], "linear")
Display "  95% Bootstrap CI: [" joined with String(bootstrap_percentiles["2.5"]) joined with ", " joined with String(bootstrap_percentiles["97.5"]) joined with "]"

Note: Bootstrap other statistics
Let bootstrap_medians be Stats.bootstrap_statistic(original_sample, "median", bootstrap_samples)
Let bootstrap_stds be Stats.bootstrap_statistic(original_sample, "std_dev", bootstrap_samples)

Display "Bootstrap median mean: " joined with String(Stats.calculate_arithmetic_mean(bootstrap_medians, []))
Display "Bootstrap std dev mean: " joined with String(Stats.calculate_arithmetic_mean(bootstrap_stds, []))
```

## Advanced Statistical Profiling

### Comprehensive Statistical Profile
```runa
Note: Generate detailed statistical profile with custom configuration
Let profile_config be Dictionary with:
    "include_robust": "true"
    "outlier_method": "iqr"  
    "normality_test": "comprehensive"
    "bootstrap_samples": "1000"

Let detailed_profile be Stats.generate_statistical_profile(research_data, profile_config)

Display "Comprehensive Statistical Profile:"
Display "Basic Statistics:"
For Each key, value_dict in detailed_profile:
    Display "  " joined with key joined with ":"
    For Each stat_name, stat_value in value_dict:
        Display "    " joined with stat_name joined with ": " joined with String(stat_value)
```

### Comparative Analysis
```runa
Note: Compare two datasets
Let dataset_a be [12.5, 13.8, 12.1, 14.9, 13.2, 15.1, 12.8, 13.9, 14.2, 13.6]
Let dataset_b be [15.2, 16.8, 15.9, 17.1, 16.3, 18.2, 15.7, 16.9, 17.4, 16.1]

Let comparison_result be Stats.compare_distributions(dataset_a, dataset_b)

Display "Distribution Comparison:"
Display "  Mean difference: " joined with String(comparison_result["mean_difference"])
Display "  Standard deviation ratio: " joined with String(comparison_result["std_dev_ratio"])
Display "  Cohen's d (effect size): " joined with String(comparison_result["cohens_d"])
Display "  Range ratio: " joined with String(comparison_result["range_ratio"])
Display "  Median difference: " joined with String(comparison_result["median_difference"])
Display "  IQR ratio: " joined with String(comparison_result["iqr_ratio"])

If "skewness_difference" in comparison_result:
    Display "  Skewness difference: " joined with String(comparison_result["skewness_difference"])
If "kurtosis_difference" in comparison_result:
    Display "  Kurtosis difference: " joined with String(comparison_result["kurtosis_difference"])

Note: Effect size interpretation
Let cohens_d be comparison_result["cohens_d"]
Let effect_size_magnitude be ""
If MathOps.absolute_value(String(cohens_d)).result_value < "0.2":
    Set effect_size_magnitude to "negligible"
Otherwise if MathOps.absolute_value(String(cohens_d)).result_value < "0.5":
    Set effect_size_magnitude to "small"
Otherwise if MathOps.absolute_value(String(cohens_d)).result_value < "0.8":
    Set effect_size_magnitude to "medium"  
Otherwise:
    Set effect_size_magnitude to "large"

Display "  Effect size magnitude: " joined with effect_size_magnitude
```

## Error Handling

### Comprehensive Error Management
```runa
Note: Robust error handling for statistical operations
Try:
    Let problematic_data be []  Note: Empty dataset
    Let result be Stats.calculate_arithmetic_mean(problematic_data, [])
Catch Errors.InvalidArgument as error:
    Display "Error: " joined with error.message
    Display "Suggested minimum sample size: 1"

Try:
    Let single_value_data be [42.5]
    Let variance_result be Stats.calculate_variance(single_value_data, false, true)
Catch Errors.InvalidArgument as error:
    Display "Sample variance error: " joined with error.message
    Display "Use population variance for single values"

Try:
    Let zero_variance_data be [5.0, 5.0, 5.0, 5.0, 5.0]
    Let cv_result be Stats.calculate_coefficient_of_variation(zero_variance_data)
Catch Errors.InvalidArgument as error:
    Display "CV calculation error: " joined with error.message
    Display "Coefficient of variation undefined when standard deviation is zero"
```

### Input Validation
```runa
Note: Validate statistical assumptions
Let assumptions_to_check be ["normality", "no_outliers", "positive_values", "finite_variance", "sufficient_sample_size"]
Let validation_results be Stats.validate_statistical_assumptions(research_data, assumptions_to_check)

Display "Statistical Assumptions Validation:"
For Each assumption, is_met in validation_results:
    Let status be ""
    If is_met:
        Set status to "✓ MET"
    Otherwise:
        Set status to "✗ VIOLATED"
    Display "  " joined with assumption joined with ": " joined with status
```

## Performance Considerations

### Efficiency Guidelines
- **Small datasets (< 1,000)**: All methods perform efficiently
- **Medium datasets (1,000 - 100,000)**: Use appropriate algorithms, avoid repeated sorting
- **Large datasets (> 100,000)**: Consider streaming algorithms and parallel processing
- **Precision requirements**: Balance computational cost with required accuracy

### Memory Optimization
```runa
Note: Efficient processing for large datasets
Let large_dataset_size be 1000000
Let streaming_summary be create_streaming_statistical_summary()

Note: Process data in chunks to manage memory
Let chunk_size be 10000
For chunk_start from 0 to large_dataset_size step chunk_size:
    Let chunk_data be generate_data_chunk(chunk_start, chunk_size)
    Call update_streaming_summary(streaming_summary, chunk_data)

Let final_statistics be finalize_streaming_summary(streaming_summary)
Display "Streaming analysis complete for " joined with String(large_dataset_size) joined with " observations"
```

## Best Practices

### Statistical Analysis Workflow
1. **Data Quality Assessment**: Check for missing values, outliers, and data integrity
2. **Exploratory Analysis**: Generate descriptive summaries and visualizations  
3. **Assumption Validation**: Verify assumptions for subsequent analyses
4. **Robust Methods**: Use resistant statistics when outliers are present
5. **Effect Size Reporting**: Report practical significance alongside statistical measures

### Code Organization
```runa
Note: Structured approach to descriptive analysis
Process called "comprehensive_descriptive_analysis" that takes data as List[Float], analysis_config as Dictionary[String, String] returns Dictionary[String, String]:
    Let results be Dictionary[String, String]
    
    Note: Step 1: Basic validation
    If Length(data) < 2:
        Set results["error"] to "Insufficient data for meaningful analysis"
        Return results
    
    Note: Step 2: Missing value assessment
    Let missing_indicators be [-999999.0, Float.NaN()]
    Let clean_data be Stats.handle_missing_values(data, "listwise_deletion")
    Set results["missing_count"] to String(Length(data) - Length(clean_data))
    
    Note: Step 3: Outlier detection and reporting
    Let outliers be Stats.detect_outliers_iqr(clean_data, 1.5)
    Set results["outlier_count"] to String(Length(outliers))
    
    Note: Step 4: Core descriptive statistics  
    Let summary be Stats.generate_descriptive_summary(clean_data, true)
    Set results["mean"] to String(summary.mean)
    Set results["median"] to String(summary.median)
    Set results["std_dev"] to String(summary.standard_deviation)
    
    Note: Step 5: Distribution shape assessment
    If Length(clean_data) >= 3:
        Set results["skewness"] to String(summary.skewness)
        Let normality_test be Stats.assess_normality(clean_data, 0.05)
        Set results["normality"] to String(normality_test["is_normal"])
    
    Note: Step 6: Robust statistics when outliers present
    If Length(outliers) > 0:
        Let trimmed_mean be Stats.calculate_trimmed_mean(clean_data, 10.0)
        Let mad_value be Stats.calculate_robust_scale(clean_data, "MAD")
        Set results["trimmed_mean"] to String(trimmed_mean)
        Set results["mad"] to String(mad_value)
    
    Return results
```

## Integration Examples

### Quality Control Application
```runa
Note: Statistical process control using descriptive statistics
Import "math/statistics/descriptive" as Stats

Process called "quality_control_analysis" that takes measurements as List[Float], control_limits as Dictionary[String, Float] returns Dictionary[String, String]:
    Let qc_results be Dictionary[String, String]
    
    Note: Calculate process statistics
    Let process_mean be Stats.calculate_arithmetic_mean(measurements, [])
    Let process_std be Stats.calculate_standard_deviation(measurements, false)
    
    Note: Check control limits
    Let ucl be control_limits["upper"]
    Let lcl be control_limits["lower"]
    
    Let out_of_control_count be 0
    For Each measurement in measurements:
        If measurement > ucl or measurement < lcl:
            Set out_of_control_count to out_of_control_count + 1
    
    Set qc_results["process_mean"] to String(process_mean)
    Set qc_results["process_std"] to String(process_std)
    Set qc_results["out_of_control_points"] to String(out_of_control_count)
    
    Note: Process capability assessment
    Let cp be (ucl - lcl) / (6.0 * process_std)
    Set qc_results["process_capability"] to String(cp)
    
    Return qc_results
```

The descriptive statistics module provides a comprehensive foundation for statistical analysis, offering robust, accurate, and efficient methods for data summarization and exploratory analysis. Its integration with Runa's precision arithmetic ensures reliable results for both routine analysis and critical statistical applications.