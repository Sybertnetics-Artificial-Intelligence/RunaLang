Note: Math Statistics Inferential Module

## Overview

The `math/statistics/inferential` module provides comprehensive inferential statistics capabilities for hypothesis testing, confidence intervals, and statistical inference. It includes parametric and non-parametric tests, power analysis, assumption validation, and advanced statistical procedures for making evidence-based conclusions about populations from sample data.

## Key Features

- **Hypothesis Testing**: T-tests, z-tests, ANOVA, chi-square, proportion tests
- **Non-parametric Tests**: Wilcoxon, Mann-Whitney, Kruskal-Wallis, sign tests
- **Confidence Intervals**: Mean, proportion, difference of means, regression parameters
- **Power Analysis**: Sample size calculation, power computation, effect size determination
- **Correlation Analysis**: Pearson, Spearman, Kendall correlations with significance tests
- **Assumption Testing**: Normality, homogeneity, independence validation
- **Multiple Comparisons**: Bonferroni, Holm, FDR corrections

## Data Types

### HypothesisTest
Complete hypothesis test results:
```runa
Type called "HypothesisTest":
    test_name as String
    null_hypothesis as String
    alternative_hypothesis as String
    test_statistic as Float
    p_value as Float
    critical_value as Float
    degrees_of_freedom as Integer
    significance_level as Float
    test_result as String
    effect_size as Float
```

### ConfidenceInterval
Confidence interval with interpretation:
```runa
Type called "ConfidenceInterval":
    parameter_name as String
    point_estimate as Float
    confidence_level as Float
    lower_bound as Float
    upper_bound as Float
    margin_of_error as Float
    standard_error as Float
    interpretation as String
```

### PowerAnalysis
Statistical power analysis results:
```runa
Type called "PowerAnalysis":
    test_type as String
    effect_size as Float
    sample_size as Integer
    significance_level as Float
    statistical_power as Float
    required_sample_size as Integer
    minimum_detectable_effect as Float
```

## One-Sample Tests

### One-Sample T-Test
```runa
Import "math/statistics/inferential" as InfStats

Note: Test whether sample mean differs from population value
Let reaction_times be [245.2, 258.7, 241.3, 267.1, 249.8, 255.2, 243.9, 261.4, 238.7, 252.3]
Let population_mean be 250.0  Note: Expected reaction time
Let alpha be 0.05

Note: Two-sided test
Let t_test_result be InfStats.one_sample_t_test(reaction_times, population_mean, alpha, "two-sided")

Display "One-Sample T-Test Results:"
Display "  Null hypothesis: " joined with t_test_result.null_hypothesis
Display "  Alternative: " joined with t_test_result.alternative_hypothesis
Display "  Test statistic: t = " joined with String(t_test_result.test_statistic)
Display "  Degrees of freedom: " joined with String(t_test_result.degrees_of_freedom)
Display "  P-value: " joined with String(t_test_result.p_value)
Display "  Critical value: ±" joined with String(t_test_result.critical_value)
Display "  Decision: " joined with t_test_result.test_result joined with " null hypothesis"
Display "  Effect size (Cohen's d): " joined with String(t_test_result.effect_size)

Note: One-sided tests
Let greater_test be InfStats.one_sample_t_test(reaction_times, population_mean, alpha, "greater")
Let less_test be InfStats.one_sample_t_test(reaction_times, population_mean, alpha, "less")

Display "Greater than test p-value: " joined with String(greater_test.p_value)
Display "Less than test p-value: " joined with String(less_test.p_value)
```

### One-Sample Z-Test (Known Variance)
```runa
Note: Test with known population standard deviation
Let iq_scores be [105.2, 108.7, 101.3, 112.4, 99.8, 107.1, 103.9, 110.2]
Let known_population_mean be 100.0
Let known_population_std be 15.0

Let z_test_result be InfStats.one_sample_z_test(iq_scores, known_population_mean, known_population_std, 0.05)

Display "One-Sample Z-Test Results:"
Display "  Z-statistic: " joined with String(z_test_result.test_statistic)
Display "  P-value: " joined with String(z_test_result.p_value)
Display "  Critical value: ±" joined with String(z_test_result.critical_value)
Display "  Decision: " joined with z_test_result.test_result joined with " null hypothesis"
Display "  Standardized effect size: " joined with String(z_test_result.effect_size)
```

### Proportion Test
```runa
Note: Test population proportion
Let survey_successes be 78  Note: People who prefer new product
Let survey_total be 150     Note: Total surveyed
Let null_proportion be 0.50  Note: 50% preference null hypothesis

Let prop_test_result be InfStats.one_sample_proportion_test(survey_successes, survey_total, null_proportion, 0.05)

Display "One-Sample Proportion Test Results:"
Display "  Sample proportion: " joined with String(Float(survey_successes) / Float(survey_total))
Display "  Null proportion: " joined with String(null_proportion)
Display "  Z-statistic: " joined with String(prop_test_result.test_statistic)
Display "  P-value: " joined with String(prop_test_result.p_value)
Display "  Decision: " joined with prop_test_result.test_result joined with " null hypothesis"
Display "  Effect size (Cohen's h): " joined with String(prop_test_result.effect_size)

Note: Check normal approximation assumptions
Let n be Float(survey_total)
Let np be n * null_proportion
Let nq be n * (1.0 - null_proportion)
Display "Normal approximation valid (np=" joined with String(np) joined with ", nq=" joined with String(nq) joined with "): " joined with String(np >= 5.0 and nq >= 5.0)
```

## Two-Sample Tests

### Independent Samples T-Test
```runa
Note: Compare means of two independent groups
Let control_group be [12.3, 14.2, 13.1, 15.8, 12.9, 14.5, 13.7, 15.1]
Let treatment_group be [16.2, 17.8, 15.9, 18.1, 16.7, 17.3, 16.4, 17.9, 15.8, 16.9]

Let independent_t_test be InfStats.independent_samples_t_test(control_group, treatment_group, "two-sided", true)

Display "Independent Samples T-Test Results:"
Display "  Control group mean: " joined with String(DescriptiveStats.calculate_arithmetic_mean(control_group, []))
Display "  Treatment group mean: " joined with String(DescriptiveStats.calculate_arithmetic_mean(treatment_group, []))
Display "  Mean difference: " joined with String(independent_t_test.test_statistic * independent_t_test.pooled_standard_error)
Display "  T-statistic: " joined with String(independent_t_test.test_statistic)
Display "  Degrees of freedom: " joined with String(independent_t_test.degrees_of_freedom)
Display "  P-value: " joined with String(independent_t_test.p_value)
Display "  Decision: " joined with independent_t_test.test_result joined with " null hypothesis"
Display "  Effect size (Cohen's d): " joined with String(independent_t_test.effect_size)
Display "  Equal variances assumed: " joined with String(independent_t_test.equal_variances)
```

### Paired Samples T-Test
```runa
Note: Test for difference in paired observations
Let before_treatment be [145.2, 138.7, 142.1, 148.9, 140.3, 144.6, 139.8, 147.2]
Let after_treatment be [132.1, 128.4, 131.7, 135.2, 129.8, 133.1, 128.9, 134.5]

Let paired_t_test be InfStats.paired_samples_t_test(before_treatment, after_treatment, "two-sided")

Display "Paired Samples T-Test Results:"
Display "  Mean before: " joined with String(DescriptiveStats.calculate_arithmetic_mean(before_treatment, []))
Display "  Mean after: " joined with String(DescriptiveStats.calculate_arithmetic_mean(after_treatment, []))
Display "  Mean difference: " joined with String(paired_t_test.mean_difference)
Display "  T-statistic: " joined with String(paired_t_test.test_statistic)
Display "  Degrees of freedom: " joined with String(paired_t_test.degrees_of_freedom)
Display "  P-value: " joined with String(paired_t_test.p_value)
Display "  Decision: " joined with paired_t_test.test_result joined with " null hypothesis"
Display "  Effect size (Cohen's d): " joined with String(paired_t_test.effect_size)

Note: Calculate the differences for inspection
Let differences be []
For i from 0 to Length(before_treatment) - 1:
    Call differences.append(before_treatment[i] - after_treatment[i])
Display "Average reduction: " joined with String(DescriptiveStats.calculate_arithmetic_mean(differences, []))
```

### Two-Sample Proportion Test
```runa
Note: Compare proportions between two groups
Let group1_successes be 45
Let group1_total be 100
Let group2_successes be 62
Let group2_total be 120

Let prop_comparison_test be InfStats.two_sample_proportion_test(group1_successes, group1_total, group2_successes, group2_total, 0.05)

Display "Two-Sample Proportion Test Results:"
Display "  Group 1 proportion: " joined with String(Float(group1_successes) / Float(group1_total))
Display "  Group 2 proportion: " joined with String(Float(group2_successes) / Float(group2_total))
Display "  Proportion difference: " joined with String(prop_comparison_test.proportion_difference)
Display "  Z-statistic: " joined with String(prop_comparison_test.test_statistic)
Display "  P-value: " joined with String(prop_comparison_test.p_value)
Display "  Decision: " joined with prop_comparison_test.test_result joined with " null hypothesis"
Display "  95% CI for difference: [" joined with String(prop_comparison_test.confidence_interval[0]) joined with ", " joined with String(prop_comparison_test.confidence_interval[1]) joined with "]"
```

## Non-Parametric Tests

### Wilcoxon Signed-Rank Test
```runa
Note: Non-parametric alternative to one-sample t-test
Let non_normal_data be [2.1, 3.4, 1.8, 5.7, 2.9, 4.2, 1.5, 6.1, 3.8, 2.3, 4.7, 15.2]  Note: Contains outlier
Let hypothesized_median be 3.0

Let wilcoxon_test be InfStats.wilcoxon_signed_rank_test(non_normal_data, hypothesized_median, 0.05)

Display "Wilcoxon Signed-Rank Test Results:"
Display "  Sample median: " joined with String(DescriptiveStats.find_median(non_normal_data, "linear"))
Display "  Hypothesized median: " joined with String(hypothesized_median)
Display "  W-statistic: " joined with String(wilcoxon_test.test_statistic)
Display "  P-value: " joined with String(wilcoxon_test.p_value)
Display "  Decision: " joined with wilcoxon_test.test_result joined with " null hypothesis"
Display "  Effect size: " joined with String(wilcoxon_test.effect_size)
```

### Mann-Whitney U Test
```runa
Note: Non-parametric alternative to independent samples t-test
Let group_a be [23, 27, 21, 32, 25, 28, 24, 30]
Let group_b be [35, 42, 38, 45, 36, 40, 37, 44, 39, 41]

Let mann_whitney_test be InfStats.mann_whitney_u_test(group_a, group_b, "two-sided", 0.05)

Display "Mann-Whitney U Test Results:"
Display "  Group A median: " joined with String(DescriptiveStats.find_median(group_a, "linear"))
Display "  Group B median: " joined with String(DescriptiveStats.find_median(group_b, "linear"))
Display "  U-statistic: " joined with String(mann_whitney_test.test_statistic)
Display "  P-value: " joined with String(mann_whitney_test.p_value)
Display "  Decision: " joined with mann_whitney_test.test_result joined with " null hypothesis"
Display "  Effect size (r): " joined with String(mann_whitney_test.effect_size)

Note: Rank-biserial correlation interpretation
Let effect_magnitude be ""
If MathOps.absolute_value(String(mann_whitney_test.effect_size)).result_value < "0.1":
    Set effect_magnitude to "negligible"
Otherwise if MathOps.absolute_value(String(mann_whitney_test.effect_size)).result_value < "0.3":
    Set effect_magnitude to "small"
Otherwise if MathOps.absolute_value(String(mann_whitney_test.effect_size)).result_value < "0.5":
    Set effect_magnitude to "medium"
Otherwise:
    Set effect_magnitude to "large"

Display "Effect magnitude: " joined with effect_magnitude
```

### Kruskal-Wallis Test
```runa
Note: Non-parametric alternative to one-way ANOVA
Let group1 be [12, 15, 13, 18, 14]
Let group2 be [22, 25, 23, 28, 24, 26]
Let group3 be [31, 34, 32, 37, 33, 35, 36]
Let all_groups be [group1, group2, group3]

Let kruskal_wallis_test be InfStats.kruskal_wallis_test(all_groups, 0.05)

Display "Kruskal-Wallis Test Results:"
Display "  Number of groups: " joined with String(Length(all_groups))
Display "  H-statistic: " joined with String(kruskal_wallis_test.test_statistic)
Display "  Degrees of freedom: " joined with String(kruskal_wallis_test.degrees_of_freedom)
Display "  P-value: " joined with String(kruskal_wallis_test.p_value)
Display "  Decision: " joined with kruskal_wallis_test.test_result joined with " null hypothesis"

If kruskal_wallis_test.test_result == "reject":
    Display "  Significant differences found between groups"
    Note: Would typically follow up with post-hoc tests
```

## ANOVA (Analysis of Variance)

### One-Way ANOVA
```runa
Note: Compare means across multiple groups
Let method_a be [78.2, 82.1, 79.5, 83.7, 80.9, 81.3, 79.8]
Let method_b be [85.4, 88.2, 86.7, 89.1, 87.3, 86.9, 88.5]
Let method_c be [72.3, 75.8, 73.9, 76.2, 74.1, 75.5, 73.7]
Let anova_groups be [method_a, method_b, method_c]

Let one_way_anova be InfStats.one_way_anova(anova_groups, 0.05)

Display "One-Way ANOVA Results:"
Display "  F-statistic: " joined with String(one_way_anova.f_statistic)
Display "  Between-groups df: " joined with String(one_way_anova.df_between)
Display "  Within-groups df: " joined with String(one_way_anova.df_within)
Display "  P-value: " joined with String(one_way_anova.p_value)
Display "  Decision: " joined with one_way_anova.test_result joined with " null hypothesis"
Display "  eta-squared (η²): " joined with String(one_way_anova.eta_squared)

Note: ANOVA assumptions check
Let anova_assumptions be InfStats.check_anova_assumptions(anova_groups, 0.05)
Display "ANOVA Assumptions:"
Display "  Normality: " joined with String(anova_assumptions.normality_check["all_groups_normal"])
Display "  Homogeneity of variance: " joined with String(anova_assumptions.homogeneity_check["levene_p_value"] > 0.05)
Display "  Independence: assumed (check study design)"
```

### Post-Hoc Tests
```runa
Note: Follow up significant ANOVA with pairwise comparisons
If one_way_anova.test_result == "reject":
    Let tukey_results be InfStats.tukey_hsd_test(anova_groups, 0.05)
    
    Display "Tukey HSD Post-Hoc Comparisons:"
    For Each comparison in tukey_results.pairwise_comparisons:
        Display "  " joined with comparison.group_labels joined with ": "
        Display "    Mean difference: " joined with String(comparison.mean_difference)
        Display "    95% CI: [" joined with String(comparison.confidence_interval[0]) joined with ", " joined with String(comparison.confidence_interval[1]) joined with "]"
        Display "    P-value: " joined with String(comparison.adjusted_p_value)
        Display "    Significant: " joined with String(comparison.is_significant)
```

## Correlation Analysis

### Pearson Correlation
```runa
Note: Linear correlation between continuous variables
Let height be [165.2, 172.8, 158.7, 180.1, 169.3, 175.6, 162.9, 177.4, 168.8, 171.2]
Let weight be [62.5, 75.3, 54.8, 82.7, 68.1, 78.9, 58.3, 80.2, 66.7, 73.4]

Let pearson_corr be InfStats.pearson_correlation_test(height, weight, 0.05)

Display "Pearson Correlation Results:"
Display "  Correlation coefficient (r): " joined with String(pearson_corr.correlation_coefficient)
Display "  T-statistic: " joined with String(pearson_corr.test_statistic)
Display "  Degrees of freedom: " joined with String(pearson_corr.degrees_of_freedom)
Display "  P-value: " joined with String(pearson_corr.p_value)
Display "  Decision: " joined with pearson_corr.test_result joined with " null hypothesis (ρ = 0)"
Display "  95% CI for r: [" joined with String(pearson_corr.confidence_interval[0]) joined with ", " joined with String(pearson_corr.confidence_interval[1]) joined with "]"

Note: Coefficient of determination
Let r_squared be pearson_corr.correlation_coefficient * pearson_corr.correlation_coefficient
Display "  Coefficient of determination (r²): " joined with String(r_squared)
Display "  Variance explained: " joined with String(r_squared * 100.0) joined with "%"
```

### Spearman Rank Correlation
```runa
Note: Monotonic correlation (non-linear relationships)
Let exam_rank be [1, 3, 2, 5, 4, 7, 6, 9, 8, 10]
Let performance_score be [92.5, 87.2, 89.8, 82.1, 85.3, 78.9, 80.5, 75.2, 77.1, 73.6]

Let spearman_corr be InfStats.spearman_correlation_test(exam_rank, performance_score, 0.05)

Display "Spearman Rank Correlation Results:"
Display "  Spearman's rho (ρₛ): " joined with String(spearman_corr.correlation_coefficient)
Display "  Test statistic: " joined with String(spearman_corr.test_statistic)
Display "  P-value: " joined with String(spearman_corr.p_value)
Display "  Decision: " joined with spearman_corr.test_result joined with " null hypothesis (ρₛ = 0)"
Display "  95% CI: [" joined with String(spearman_corr.confidence_interval[0]) joined with ", " joined with String(spearman_corr.confidence_interval[1]) joined with "]"
```

### Kendall's Tau
```runa
Note: Robust correlation measure for small samples
Let kendall_corr be InfStats.kendall_tau_test(height, weight, 0.05)

Display "Kendall's Tau Results:"
Display "  Kendall's tau (τ): " joined with String(kendall_corr.correlation_coefficient)
Display "  Z-statistic: " joined with String(kendall_corr.test_statistic)
Display "  P-value: " joined with String(kendall_corr.p_value)
Display "  Decision: " joined with kendall_corr.test_result joined with " null hypothesis (τ = 0)"
Display "  Concordant pairs: " joined with String(kendall_corr.concordant_pairs)
Display "  Discordant pairs: " joined with String(kendall_corr.discordant_pairs)
```

## Chi-Square Tests

### Goodness of Fit Test
```runa
Note: Test whether data follows expected distribution
Let observed_frequencies be [18, 22, 25, 20, 15]  Note: Five categories
Let expected_frequencies be [20.0, 20.0, 20.0, 20.0, 20.0]  Note: Equal expected

Let goodness_of_fit be InfStats.chi_square_goodness_of_fit_test(observed_frequencies, expected_frequencies, 0.05)

Display "Chi-Square Goodness of Fit Test:"
Display "  Chi-square statistic: " joined with String(goodness_of_fit.test_statistic)
Display "  Degrees of freedom: " joined with String(goodness_of_fit.degrees_of_freedom)
Display "  P-value: " joined with String(goodness_of_fit.p_value)
Display "  Decision: " joined with goodness_of_fit.test_result joined with " null hypothesis"
Display "  Effect size (Cramér's V): " joined with String(goodness_of_fit.effect_size)
```

### Test of Independence
```runa
Note: Test association between categorical variables
Let contingency_table be [
    [20, 15, 25],  Note: Row 1: Treatment A outcomes
    [30, 25, 20],  Note: Row 2: Treatment B outcomes  
    [15, 35, 30]   Note: Row 3: Treatment C outcomes
]

Let independence_test be InfStats.chi_square_independence_test(contingency_table, 0.05)

Display "Chi-Square Test of Independence:"
Display "  Chi-square statistic: " joined with String(independence_test.test_statistic)
Display "  Degrees of freedom: " joined with String(independence_test.degrees_of_freedom)
Display "  P-value: " joined with String(independence_test.p_value)
Display "  Decision: " joined with independence_test.test_result joined with " null hypothesis"
Display "  Cramér's V: " joined with String(independence_test.cramer_v)
Display "  Phi coefficient: " joined with String(independence_test.phi_coefficient)

Note: Expected frequencies for assumption checking
Display "Expected frequencies (all should be ≥ 5):"
For i from 0 to Length(independence_test.expected_frequencies) - 1:
    For j from 0 to Length(independence_test.expected_frequencies[0]) - 1:
        Display "  Cell [" joined with String(i) joined with "," joined with String(j) joined with "]: " joined with String(independence_test.expected_frequencies[i][j])
```

## Confidence Intervals

### Mean Confidence Intervals
```runa
Note: Confidence interval for population mean
Let sample_data be [45.2, 48.7, 44.1, 52.3, 46.8, 49.2, 47.5, 50.1, 43.9, 51.2]
Let confidence_level be 0.95

Let mean_ci be InfStats.confidence_interval_mean(sample_data, confidence_level)

Display "95% Confidence Interval for Mean:"
Display "  Point estimate: " joined with String(mean_ci.point_estimate)
Display "  Standard error: " joined with String(mean_ci.standard_error)
Display "  Margin of error: " joined with String(mean_ci.margin_of_error)
Display "  Lower bound: " joined with String(mean_ci.lower_bound)
Display "  Upper bound: " joined with String(mean_ci.upper_bound)
Display "  Interpretation: " joined with mean_ci.interpretation

Note: Different confidence levels
Let ci_90 be InfStats.confidence_interval_mean(sample_data, 0.90)
Let ci_99 be InfStats.confidence_interval_mean(sample_data, 0.99)

Display "Confidence interval comparison:"
Display "  90% CI: [" joined with String(ci_90.lower_bound) joined with ", " joined with String(ci_90.upper_bound) joined with "] (width: " joined with String(ci_90.upper_bound - ci_90.lower_bound) joined with ")"
Display "  95% CI: [" joined with String(mean_ci.lower_bound) joined with ", " joined with String(mean_ci.upper_bound) joined with "] (width: " joined with String(mean_ci.upper_bound - mean_ci.lower_bound) joined with ")"
Display "  99% CI: [" joined with String(ci_99.lower_bound) joined with ", " joined with String(ci_99.upper_bound) joined with "] (width: " joined with String(ci_99.upper_bound - ci_99.lower_bound) joined with ")"
```

### Proportion Confidence Intervals
```runa
Note: Confidence interval for population proportion
Let successes be 145
Let total_sample be 200
Let prop_ci be InfStats.confidence_interval_proportion(successes, total_sample, 0.95)

Display "95% Confidence Interval for Proportion:"
Display "  Sample proportion: " joined with String(prop_ci.point_estimate)
Display "  Lower bound: " joined with String(prop_ci.lower_bound)
Display "  Upper bound: " joined with String(prop_ci.upper_bound)
Display "  Margin of error: " joined with String(prop_ci.margin_of_error)
Display "  Interpretation: " joined with prop_ci.interpretation

Note: Wilson score interval (better for extreme proportions)
Let wilson_ci be InfStats.confidence_interval_proportion_wilson(successes, total_sample, 0.95)
Display "Wilson Score 95% CI: [" joined with String(wilson_ci.lower_bound) joined with ", " joined with String(wilson_ci.upper_bound) joined with "]"
```

### Difference of Means Confidence Interval
```runa
Note: CI for difference between two independent means
Let group1 be [23.4, 25.8, 22.1, 26.9, 24.3]
Let group2 be [28.7, 31.2, 29.5, 32.1, 30.4]

Let diff_means_ci be InfStats.confidence_interval_mean_difference(group1, group2, 0.95, true)

Display "95% CI for Difference of Means:"
Display "  Group 1 mean: " joined with String(DescriptiveStats.calculate_arithmetic_mean(group1, []))
Display "  Group 2 mean: " joined with String(DescriptiveStats.calculate_arithmetic_mean(group2, []))
Display "  Difference (Group 2 - Group 1): " joined with String(diff_means_ci.point_estimate)
Display "  95% CI for difference: [" joined with String(diff_means_ci.lower_bound) joined with ", " joined with String(diff_means_ci.upper_bound) joined with "]"
Display "  Interpretation: " joined with diff_means_ci.interpretation
```

## Power Analysis

### Sample Size Calculation
```runa
Note: Determine required sample size for desired power
Let desired_power be 0.80  Note: 80% power
Let effect_size be 0.5     Note: Medium effect size (Cohen's d = 0.5)
Let alpha_level be 0.05    Note: 5% significance level

Let power_analysis be InfStats.power_analysis_t_test("two-sample", effect_size, 0, alpha_level, desired_power)

Display "Power Analysis for Two-Sample T-Test:"
Display "  Effect size (Cohen's d): " joined with String(power_analysis.effect_size)
Display "  Significance level (α): " joined with String(power_analysis.significance_level)
Display "  Desired power (1-β): " joined with String(power_analysis.statistical_power)
Display "  Required sample size per group: " joined with String(power_analysis.required_sample_size)

Note: Power calculation for existing sample size
Let existing_n be 25
Let achieved_power_analysis be InfStats.power_analysis_t_test("two-sample", effect_size, existing_n, alpha_level, 0.0)

Display "Power with n=" joined with String(existing_n) joined with " per group: " joined with String(achieved_power_analysis.statistical_power)
```

### Minimum Detectable Effect
```runa
Note: What effect size can be detected with given sample size?
Let fixed_sample_size be 30
Let mde_analysis be InfStats.minimum_detectable_effect_t_test("two-sample", fixed_sample_size, alpha_level, desired_power)

Display "Minimum Detectable Effect Analysis:"
Display "  Sample size per group: " joined with String(fixed_sample_size)
Display "  Minimum detectable effect size: " joined with String(mde_analysis.minimum_detectable_effect)
Display "  With 80% power and α=0.05"

Note: Effect size interpretation
Let mde_value be mde_analysis.minimum_detectable_effect
Let effect_interpretation be ""
If mde_value < 0.2:
    Set effect_interpretation to "very small"
Otherwise if mde_value < 0.5:
    Set effect_interpretation to "small"
Otherwise if mde_value < 0.8:
    Set effect_interpretation to "medium"
Otherwise:
    Set effect_interpretation to "large"

Display "  Effect size interpretation: " joined with effect_interpretation
```

## Multiple Comparisons Correction

### Bonferroni Correction
```runa
Note: Adjust p-values for multiple testing
Let raw_p_values be [0.032, 0.018, 0.067, 0.049, 0.021, 0.078, 0.043]
Let family_alpha be 0.05

Let bonferroni_results be InfStats.bonferroni_correction(raw_p_values, family_alpha)

Display "Bonferroni Multiple Comparisons Correction:"
Display "  Number of tests: " joined with String(Length(raw_p_values))
Display "  Family-wise error rate (FWER): " joined with String(family_alpha)
Display "  Adjusted alpha per test: " joined with String(bonferroni_results.adjusted_alpha)

Display "  Results:"
For i from 0 to Length(raw_p_values) - 1:
    Let is_significant be bonferroni_results.adjusted_p_values[i] < family_alpha
    Display "    Test " joined with String(i + 1) joined with ": p=" joined with String(raw_p_values[i]) joined with " → adjusted p=" joined with String(bonferroni_results.adjusted_p_values[i]) joined with " (" joined with String(is_significant) joined with ")"

Display "  Significant tests: " joined with String(bonferroni_results.significant_count) joined with "/" joined with String(Length(raw_p_values))
```

### Holm-Bonferroni Method
```runa
Note: Less conservative step-down method
Let holm_results be InfStats.holm_bonferroni_correction(raw_p_values, family_alpha)

Display "Holm-Bonferroni Correction:"
Display "  Significant tests: " joined with String(holm_results.significant_count) joined with "/" joined with String(Length(raw_p_values))
Display "  Step-down procedure results:"

For i from 0 to Length(raw_p_values) - 1:
    Let step be holm_results.step_order[i]
    Let critical_value be holm_results.critical_values[i]
    Display "    Step " joined with String(step) joined with ": p=" joined with String(raw_p_values[i]) joined with ", critical=" joined with String(critical_value) joined with " (" joined with String(holm_results.decisions[i]) joined with ")"
```

### False Discovery Rate (FDR)
```runa
Note: Control expected proportion of false discoveries
Let fdr_results be InfStats.benjamini_hochberg_fdr(raw_p_values, 0.05)

Display "False Discovery Rate (Benjamini-Hochberg):"
Display "  FDR level: 5%"
Display "  Significant discoveries: " joined with String(fdr_results.significant_count) joined with "/" joined with String(Length(raw_p_values))
Display "  Critical p-value: " joined with String(fdr_results.critical_p_value)

For i from 0 to Length(raw_p_values) - 1:
    Display "    Test " joined with String(i + 1) joined with ": p=" joined with String(raw_p_values[i]) joined with " → q-value=" joined with String(fdr_results.q_values[i]) joined with " (" joined with String(fdr_results.discoveries[i]) joined with ")"
```

## Assumption Testing

### Normality Tests
```runa
Note: Test normality assumption for parametric tests
Let potentially_normal be [12.1, 13.8, 12.5, 14.2, 13.1, 12.9, 14.5, 13.3, 12.7, 14.1, 13.6, 12.8]
Let clearly_skewed be [1.2, 2.8, 3.1, 4.7, 8.9, 15.3, 23.7, 45.2, 67.1, 89.4]

Let normality_normal be InfStats.test_normality(potentially_normal, 0.05)
Let normality_skewed be InfStats.test_normality(clearly_skewed, 0.05)

Display "Normality Test Results:"
Display "Potentially normal data:"
Display "  Shapiro-Wilk W: " joined with String(normality_normal.shapiro_wilk["statistic"])
Display "  Shapiro-Wilk p-value: " joined with String(normality_normal.shapiro_wilk["p_value"])
Display "  Anderson-Darling A: " joined with String(normality_normal.anderson_darling["statistic"])
Display "  Anderson-Darling p-value: " joined with String(normality_normal.anderson_darling["p_value"])
Display "  Overall normality (α=0.05): " joined with String(normality_normal.is_normal)

Display "Clearly skewed data:"
Display "  Shapiro-Wilk p-value: " joined with String(normality_skewed.shapiro_wilk["p_value"])
Display "  Overall normality: " joined with String(normality_skewed.is_normal)
```

### Homogeneity of Variance Tests
```runa
Note: Test equal variances assumption
Let variance_groups be [
    [12.3, 13.1, 12.8, 13.5, 12.9, 13.2, 12.7],
    [14.8, 15.3, 14.5, 15.7, 14.9, 15.1, 14.6],
    [11.2, 11.8, 11.5, 12.1, 11.6, 11.9, 11.4]
]

Let levene_test be InfStats.levene_test(variance_groups, 0.05)
Let bartlett_test be InfStats.bartlett_test(variance_groups, 0.05)

Display "Homogeneity of Variance Tests:"
Display "Levene's test (robust to non-normality):"
Display "  F-statistic: " joined with String(levene_test.test_statistic)
Display "  P-value: " joined with String(levene_test.p_value)
Display "  Equal variances: " joined with String(levene_test.test_result == "fail to reject")

Display "Bartlett's test (assumes normality):"
Display "  Chi-square statistic: " joined with String(bartlett_test.test_statistic)
Display "  P-value: " joined with String(bartlett_test.p_value)
Display "  Equal variances: " joined with String(bartlett_test.test_result == "fail to reject")
```

### Comprehensive Assumption Checking
```runa
Note: Check all assumptions for t-test
Let group1_test be [23.4, 25.8, 22.1, 26.9, 24.3, 25.1, 23.7, 26.2]
Let group2_test be [28.7, 31.2, 29.5, 32.1, 30.4, 29.8, 31.5, 30.2]

Let assumption_results be InfStats.check_t_test_assumptions(group1_test, group2_test, 0.05)

Display "T-Test Assumptions Check:"
Display "  Normality (Group 1): " joined with String(assumption_results.normality_check["group1_normal"])
Display "  Normality (Group 2): " joined with String(assumption_results.normality_check["group2_normal"])
Display "  Homogeneity of variance: " joined with String(assumption_results.homogeneity_check["equal_variances"])
Display "  Independence: " joined with assumption_results.independence_check["assessment"]
Display "  All assumptions met: " joined with String(assumption_results.assumptions_met)
Display "  Recommendation: " joined with assumption_results.recommendation

If not assumption_results.assumptions_met:
    Display "  Alternative tests suggested:"
    For Each alternative in assumption_results.alternative_tests:
        Display "    - " joined with alternative
```

## Error Handling and Diagnostics

### Comprehensive Error Management
```runa
Note: Handle various statistical errors gracefully
Try:
    Let insufficient_data be [5.2]
    Let t_result be InfStats.one_sample_t_test(insufficient_data, 5.0, 0.05, "two-sided")
Catch Errors.InvalidArgument as error:
    Display "Sample size error: " joined with error.message
    Display "Minimum required for t-test: 2 observations"

Try:
    Let zero_variance be [10.0, 10.0, 10.0, 10.0, 10.0]
    Let impossible_test be InfStats.one_sample_t_test(zero_variance, 5.0, 0.05, "two-sided")
Catch Errors.InvalidArgument as error:
    Display "Zero variance error: " joined with error.message
    Display "Consider if all values are truly identical"

Try:
    Let invalid_alpha be 1.5
    Let bad_alpha_test be InfStats.one_sample_t_test([1, 2, 3], 2.0, invalid_alpha, "two-sided")
Catch Errors.InvalidArgument as error:
    Display "Invalid alpha: " joined with error.message
    Display "Alpha must be between 0 and 1 (typically 0.05)"
```

### Test Selection Guidance
```runa
Process called "recommend_statistical_test" that takes sample1 as List[Float], sample2 as List[Float], analysis_type as String returns String:
    Let recommendation be ""
    
    Note: Check sample sizes
    If Length(sample1) < 30 or Length(sample2) < 30:
        Set recommendation to "Small sample sizes detected. "
    
    Note: Check normality
    Let norm_check1 be InfStats.test_normality(sample1, 0.05)
    Let norm_check2 be InfStats.test_normality(sample2, 0.05)
    
    If analysis_type == "compare_means":
        If norm_check1.is_normal and norm_check2.is_normal:
            Note: Check equal variances
            Let variance_check be InfStats.levene_test([sample1, sample2], 0.05)
            If variance_check.test_result == "fail to reject":
                Set recommendation to recommendation joined with "Use independent samples t-test (equal variances)"
            Otherwise:
                Set recommendation to recommendation joined with "Use Welch's t-test (unequal variances)"
        Otherwise:
            Set recommendation to recommendation joined with "Use Mann-Whitney U test (non-parametric)"
    
    Return recommendation

Note: Example usage
Let data_group_1 be [12.3, 14.5, 13.2, 15.8, 12.9]  
Let data_group_2 be [18.7, 19.2, 17.5, 20.1, 18.3]
Let test_recommendation be recommend_statistical_test(data_group_1, data_group_2, "compare_means")
Display "Recommended test: " joined with test_recommendation
```

## Best Practices and Guidelines

### Statistical Analysis Workflow
```runa
Process called "complete_inferential_analysis" that takes sample_data as List[Float], comparison_data as List[Float], analysis_config as Dictionary[String, String] returns Dictionary[String, String]:
    Let results be Dictionary[String, String]
    Let alpha be Float(analysis_config["alpha"])
    
    Note: Step 1: Exploratory data analysis
    Let desc1 be DescriptiveStats.generate_descriptive_summary(sample_data, true)
    Let desc2 be DescriptiveStats.generate_descriptive_summary(comparison_data, true)
    Set results["sample1_mean"] to String(desc1.mean)
    Set results["sample2_mean"] to String(desc2.mean)
    
    Note: Step 2: Assumption testing
    Let assumptions be InfStats.check_t_test_assumptions(sample_data, comparison_data, alpha)
    Set results["assumptions_met"] to String(assumptions.assumptions_met)
    
    Note: Step 3: Test selection and execution
    If assumptions.assumptions_met:
        Let t_test be InfStats.independent_samples_t_test(sample_data, comparison_data, "two-sided", true)
        Set results["test_used"] to "Independent t-test"
        Set results["test_statistic"] to String(t_test.test_statistic)
        Set results["p_value"] to String(t_test.p_value)
        Set results["effect_size"] to String(t_test.effect_size)
    Otherwise:
        Let mann_whitney be InfStats.mann_whitney_u_test(sample_data, comparison_data, "two-sided", alpha)
        Set results["test_used"] to "Mann-Whitney U test"
        Set results["test_statistic"] to String(mann_whitney.test_statistic)
        Set results["p_value"] to String(mann_whitney.p_value)
        Set results["effect_size"] to String(mann_whitney.effect_size)
    
    Note: Step 4: Confidence interval
    Let ci be InfStats.confidence_interval_mean_difference(sample_data, comparison_data, 0.95, assumptions.assumptions_met)
    Set results["ci_lower"] to String(ci.lower_bound)
    Set results["ci_upper"] to String(ci.upper_bound)
    
    Note: Step 5: Interpretation
    Let is_significant be Float(results["p_value"]) < alpha
    Set results["significant"] to String(is_significant)
    Set results["interpretation"] to generate_interpretation(results, alpha)
    
    Return results

Process called "generate_interpretation" that takes analysis_results as Dictionary[String, String], alpha as Float returns String:
    Let interpretation be ""
    Let p_value be Float(analysis_results["p_value"])
    Let effect_size be Float(analysis_results["effect_size"])
    
    If p_value < alpha:
        Set interpretation to "Statistically significant difference found (p < " joined with String(alpha) joined with "). "
    Otherwise:
        Set interpretation to "No statistically significant difference found (p ≥ " joined with String(alpha) joined with "). "
    
    Note: Effect size interpretation
    Let effect_magnitude be ""
    If MathOps.absolute_value(String(effect_size)).result_value < "0.2":
        Set effect_magnitude to "negligible"
    Otherwise if MathOps.absolute_value(String(effect_size)).result_value < "0.5":
        Set effect_magnitude to "small"
    Otherwise if MathOps.absolute_value(String(effect_size)).result_value < "0.8":
        Set effect_magnitude to "medium"
    Otherwise:
        Set effect_magnitude to "large"
    
    Set interpretation to interpretation joined with "Effect size is " joined with effect_magnitude joined with " (" joined with String(effect_size) joined with ")."
    
    Return interpretation
```

The inferential statistics module provides a comprehensive framework for statistical hypothesis testing and inference, ensuring reliable and interpretable results for research and data analysis applications. Its integration with assumption testing and effect size calculations promotes best practices in statistical analysis.