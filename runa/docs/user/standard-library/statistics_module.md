# Statistics Module

The Statistics module provides comprehensive statistical functions for analyzing data, including descriptive statistics, probability distributions, hypothesis testing, and advanced data analysis tools.

## Overview

The Statistics module offers a complete set of statistical analysis functions with natural language syntax for basic operations and helper functions for advanced use cases.

## Basic Descriptive Statistics

### Central Tendency Measures

```runa
Note: Basic descriptive statistics use natural language syntax
:End Note

Let data be [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

Let avg be mean of data
Let med be median of data
Let mode_val be mode of data

Call print with message as "Mean: " plus avg
Call print with message as "Median: " plus med
Call print with message as "Mode: " plus mode_val
```

### Variability Measures

```runa
Let variance_val be variance of data
Let std_dev be standard deviation of data
Let sample_var be sample variance of data
Let sample_std be sample standard deviation of data

Call print with message as "Variance: " plus variance_val
Call print with message as "Standard Deviation: " plus std_dev
Call print with message as "Sample Variance: " plus sample_var
```

## Advanced Descriptive Statistics

### Alternative Mean Types

```runa
Let geometric_avg be geometric mean of data
Let harmonic_avg be harmonic mean of data

Let weights be [1, 2, 1, 2, 1, 2, 1, 2, 1, 2]
Let weighted_avg be weighted mean of data with weights as weights

Call print with message as "Geometric Mean: " plus geometric_avg
Call print with message as "Harmonic Mean: " plus harmonic_avg
Call print with message as "Weighted Mean: " plus weighted_avg
```

### Robust Statistics

```runa
Let trimmed_avg be trimmed mean of data with proportion as 0.1
Let winsorized_avg be winsorized mean of data with proportion as 0.1

Call print with message as "Trimmed Mean: " plus trimmed_avg
Call print with message as "Winsorized Mean: " plus winsorized_avg
```

### Percentiles and Quartiles

```runa
Let p25 be percentile of data at 25
Let p75 be percentile of data at 75
Let p90 be percentile of data at 90

Let quartiles_list be quartiles of data
Let iqr_val be interquartile range of data

Call print with message as "25th Percentile: " plus p25
Call print with message as "75th Percentile: " plus p75
Call print with message as "IQR: " plus iqr_val
```

## Distribution Shape

### Skewness and Kurtosis

```runa
Let skew_val be skewness of data
Let kurt_val be kurtosis of data

Call print with message as "Skewness: " plus skew_val
Call print with message as "Kurtosis: " plus kurt_val

If skew_val is greater than 0:
    Call print with message as "Distribution is right-skewed"
Otherwise if skew_val is less than 0:
    Call print with message as "Distribution is left-skewed"
Otherwise:
    Call print with message as "Distribution is symmetric"
```

## Correlation and Covariance

### Linear Relationships

```runa
Let x_values be [1, 2, 3, 4, 5]
Let y_values be [2, 4, 6, 8, 10]

Let cov_val be covariance of x_values and y_values
Let corr_val be correlation between x_values and y_values
Let rank_corr be rank correlation of x_values and y_values

Call print with message as "Covariance: " plus cov_val
Call print with message as "Correlation: " plus corr_val
Call print with message as "Rank Correlation: " plus rank_corr
```

## Data Transformation

### Standardization and Normalization

```runa
Let z_scores be z-score of data
Let normalized_data be normalize data
Let standardized_data be standardize data

Call print with message as "Z-scores: " plus z_scores
Call print with message as "Normalized: " plus normalized_data
Call print with message as "Standardized: " plus standardized_data
```

### Ranking Data

```runa
Let ranks be rank data
Call print with message as "Ranks: " plus ranks
```

## Outlier Detection

### Identifying Outliers

```runa
Let outliers_iqr be outliers of data with method as "iqr"
Let outliers_zscore be outliers of data with method as "zscore"

Call print with message as "Outliers (IQR method): " plus outliers_iqr
Call print with message as "Outliers (Z-score method): " plus outliers_zscore
```

## Frequency Analysis

### Frequency Distributions

```runa
Let freq_table be frequency table of data
Let rel_freq be relative frequency of data
Let cum_freq be cumulative frequency of data

Call print with message as "Frequency Table: " plus freq_table
Call print with message as "Relative Frequency: " plus rel_freq
Call print with message as "Cumulative Frequency: " plus cum_freq
```

## Confidence Intervals

### Estimating Population Parameters

```runa
Let confidence_95 be confidence interval of data with confidence as 0.95
Let confidence_99 be confidence interval of data with confidence as 0.99

Call print with message as "95% CI: " plus confidence_95
Call print with message as "99% CI: " plus confidence_99
```

## Hypothesis Testing

### T-Test for Two Groups

```runa
Let group1 be [1, 2, 3, 4, 5]
Let group2 be [6, 7, 8, 9, 10]

Let t_result be t-test of group1 and group2
Call print with message as "T-statistic: " plus t_result["t_statistic"]
Call print with message as "Degrees of Freedom: " plus t_result["degrees_of_freedom"]
```

### Chi-Square Test

```runa
Let observed be [10, 15, 20, 25]
Let expected be [12, 12, 20, 26]

Let chi_result be chi-square test of observed and expected
Call print with message as "Chi-square: " plus chi_result["chi_square"]
Call print with message as "Degrees of Freedom: " plus chi_result["degrees_of_freedom"]
```

### Analysis of Variance (ANOVA)

```runa
Let groups be [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
Let anova_result be anova of groups

Call print with message as "F-statistic: " plus anova_result["f_statistic"]
Call print with message as "DF Between: " plus anova_result["df_between"]
Call print with message as "DF Within: " plus anova_result["df_within"]
```

## Linear Regression

### Simple Linear Regression

```runa
Let x_data be [1, 2, 3, 4, 5]
Let y_data be [2.1, 3.8, 6.2, 8.1, 10.3]

Let model be linear regression of x_data and y_data
Call print with message as "Slope: " plus model["slope"]
Call print with message as "Intercept: " plus model["intercept"]
Call print with message as "R-squared: " plus model["r_squared"]
```

### Making Predictions

```runa
Let prediction be predict with model as model and x as 6
Call print with message as "Prediction for x=6: " plus prediction
```

### Model Evaluation

```runa
Let predicted_values be list with
For each x in x_data:
    Let pred be predict with model as model and x as x
    Add pred to predicted_values

Let residuals_list be residuals of x_data and y_data and model
Let mae_val be mae of y_data and predicted_values
Let mse_val be mse of y_data and predicted_values
Let rmse_val be rmse of y_data and predicted_values
Let mape_val be mape of y_data and predicted_values
Let r2_val be r2 score of y_data and predicted_values

Call print with message as "MAE: " plus mae_val
Call print with message as "MSE: " plus mse_val
Call print with message as "RMSE: " plus rmse_val
Call print with message as "MAPE: " plus mape_val
Call print with message as "R² Score: " plus r2_val
```

## Data Analysis Workflow

### Complete Statistical Analysis

```runa
Note: Complete statistical analysis workflow
:End Note

Let dataset be [12, 15, 18, 22, 25, 28, 30, 35, 40, 45, 50, 55, 60, 65, 70]

Note: Descriptive statistics
:End Note
Let desc_stats be dictionary with
    "count" as length of dataset
    "mean" as mean of dataset
    "median" as median of dataset
    "std" as standard deviation of dataset
    "min" as minimum of dataset
    "max" as maximum of dataset
    "q1" as percentile of dataset at 25
    "q3" as percentile of dataset at 75
    "iqr" as interquartile range of dataset

Call print with message as "Descriptive Statistics: " plus desc_stats

Note: Distribution analysis
:End Note
Let skew_val be skewness of dataset
Let kurt_val be kurtosis of dataset
Let outliers_list be outliers of dataset with method as "iqr"

Call print with message as "Skewness: " plus skew_val
Call print with message as "Kurtosis: " plus kurt_val
Call print with message as "Outliers: " plus outliers_list

Note: Confidence interval
:End Note
Let ci be confidence interval of dataset with confidence as 0.95
Call print with message as "95% Confidence Interval: " plus ci
```

## Helper Functions

### Advanced Usage

```runa
Note: For advanced/AI-generated code, use helper functions
:End Note

Let result be calculate with data as values and statistic as "mean"
Let test_result be test hypothesis with data as values and test as "t_test"
```

## Error Handling

### Robust Statistical Analysis

```runa
Try:
    Let result be mean of empty_list
    Assert false  Note: Should not reach here
:End Note
Catch Error as e:
    Call print with message as "Error calculating mean: " plus e

Try:
    Let result be correlation of x_data and y_data
    Note: Continue with analysis
    :End Note
Catch Error as e:
    Call print with message as "Error calculating correlation: " plus e
```

## Performance Considerations

### Efficient Statistical Computations

```runa
Note: For large datasets, consider sampling
:End Note

Let large_dataset be list with 10000 elements
Let sample_size be 1000

If length of large_dataset is greater than sample_size:
    Let sample be random sample of large_dataset with size as sample_size
    Let sample_stats be mean of sample
    Call print with message as "Sample mean: " plus sample_stats
Otherwise:
    Let full_stats be mean of large_dataset
    Call print with message as "Full dataset mean: " plus full_stats
```

## API Reference

### Basic Statistics

- `mean(data: List[Number]) -> Number`: Arithmetic mean
- `median(data: List[Number]) -> Number`: Median
- `mode(data: List[Number]) -> Number`: Mode
- `variance(data: List[Number]) -> Number`: Population variance
- `stdev(data: List[Number]) -> Number`: Population standard deviation
- `sample_variance(data: List[Number]) -> Number`: Sample variance
- `sample_stdev(data: List[Number]) -> Number`: Sample standard deviation

### Advanced Statistics

- `geometric_mean(data: List[Number]) -> Number`: Geometric mean
- `harmonic_mean(data: List[Number]) -> Number`: Harmonic mean
- `weighted_mean(data: List[Number], weights: List[Number]) -> Number`: Weighted mean
- `trimmed_mean(data: List[Number], proportion: Number) -> Number`: Trimmed mean
- `winsorized_mean(data: List[Number], proportion: Number) -> Number`: Winsorized mean

### Percentiles and Quartiles

- `percentile(data: List[Number], p: Number) -> Number`: Percentile
- `quartiles(data: List[Number]) -> List[Number]`: Quartiles
- `iqr(data: List[Number]) -> Number`: Interquartile range

### Distribution Shape

- `skewness(data: List[Number]) -> Number`: Skewness
- `kurtosis(data: List[Number]) -> Number`: Kurtosis

### Correlation and Covariance

- `covariance(x: List[Number], y: List[Number]) -> Number`: Covariance
- `correlation(x: List[Number], y: List[Number]) -> Number`: Pearson correlation
- `rank_correlation(x: List[Number], y: List[Number]) -> Number`: Spearman correlation
- `rank_data(data: List[Number]) -> List[Integer]`: Rank data

### Data Transformation

- `z_score(data: List[Number]) -> List[Number]`: Z-scores
- `normalize(data: List[Number]) -> List[Number]`: Min-max normalization
- `standardize(data: List[Number]) -> List[Number]`: Standardization
- `outliers(data: List[Number], method: String) -> List[Number]`: Outlier detection

### Frequency Analysis

- `frequency_table(data: List[Number]) -> Dictionary[Number, Integer]`: Frequency table
- `relative_frequency(data: List[Number]) -> Dictionary[Number, Number]`: Relative frequency
- `cumulative_frequency(data: List[Number]) -> Dictionary[Number, Number]`: Cumulative frequency

### Confidence Intervals

- `confidence_interval(data: List[Number], confidence: Number) -> List[Number]`: Confidence interval

### Hypothesis Testing

- `t_test(data1: List[Number], data2: List[Number]) -> Dictionary[String, Number]`: T-test
- `chi_square_test(observed: List[Number], expected: List[Number]) -> Dictionary[String, Number]`: Chi-square test
- `anova(groups: List[List[Number]]) -> Dictionary[String, Number]`: ANOVA

### Linear Regression

- `linear_regression(x: List[Number], y: List[Number]) -> Dictionary[String, Number]`: Linear regression
- `predict(model: Dictionary[String, Number], x: Number) -> Number`: Make prediction
- `residuals(x: List[Number], y: List[Number], model: Dictionary[String, Number]) -> List[Number]`: Calculate residuals

### Model Evaluation

- `mae(actual: List[Number], predicted: List[Number]) -> Number`: Mean absolute error
- `mse(actual: List[Number], predicted: List[Number]) -> Number`: Mean squared error
- `rmse(actual: List[Number], predicted: List[Number]) -> Number`: Root mean squared error
- `mape(actual: List[Number], predicted: List[Number]) -> Number`: Mean absolute percentage error
- `r2_score(actual: List[Number], predicted: List[Number]) -> Number`: R-squared score

## Testing

The Statistics module includes comprehensive tests covering:

- Basic descriptive statistics
- Advanced statistical measures
- Correlation and covariance calculations
- Data transformation and normalization
- Outlier detection methods
- Frequency analysis
- Confidence interval calculations
- Hypothesis testing procedures
- Linear regression analysis
- Model evaluation metrics
- Error handling scenarios
- Performance with large datasets

## Examples

See the `examples/basic/statistical_analysis.runa` file for complete working examples of all Statistics module features. 