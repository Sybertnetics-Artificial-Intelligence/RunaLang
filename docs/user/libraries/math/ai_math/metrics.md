# Machine Learning Evaluation Metrics

The Machine Learning Evaluation Metrics module (`math/ai_math/metrics`) provides comprehensive evaluation metrics for machine learning models including classification metrics (accuracy, precision, recall, F1, ROC-AUC), regression metrics (RMSE, R-squared, MAE), ranking metrics (NDCG, MAP), clustering metrics (silhouette, adjusted rand index), and advanced metrics for modern ML applications.

## Overview

This module implements essential evaluation metrics across all machine learning domains:

- **Classification Metrics**: Binary and multi-class classification evaluation
- **Regression Metrics**: Continuous value prediction assessment
- **Ranking Metrics**: Information retrieval and recommendation evaluation
- **Clustering Metrics**: Unsupervised learning quality assessment
- **Probabilistic Metrics**: Calibration and uncertainty evaluation
- **Fairness Metrics**: Bias detection and algorithmic fairness

## Key Features

### Comprehensive Coverage
- **All ML Tasks**: Classification, regression, clustering, ranking
- **Multiple Averaging**: Macro, micro, weighted averaging for multi-class
- **Statistical Testing**: Significance testing for metric comparisons

### Robust Implementation
- **Numerical Stability**: Handles edge cases and extreme values
- **Missing Values**: Appropriate handling of incomplete data
- **Confidence Intervals**: Bootstrap-based uncertainty estimation

### Performance Optimization
- **Vectorized Operations**: Efficient computation for large datasets
- **Incremental Updates**: Online metric computation
- **Parallel Processing**: Multi-threaded evaluation

## Core Types

### Metric Configuration
```runa
Type called "MetricConfig":
    average as String                 Note: macro, micro, weighted, binary
    labels as Optional[Vector[Integer]]  Note: Labels to include in average
    pos_label as Optional[Integer]    Note: Positive class label for binary
    zero_division as String           Note: warn, 0, 1 - behavior for zero division
    sample_weight as Optional[Vector[Float]]  Note: Sample weights

Type called "ConfusionMatrix":
    matrix as Matrix[Integer]         Note: Confusion matrix values
    labels as Vector[String]          Note: Class labels
    true_positives as Vector[Integer] Note: TP for each class
    false_positives as Vector[Integer] Note: FP for each class
    true_negatives as Vector[Integer] Note: TN for each class
    false_negatives as Vector[Integer] Note: FN for each class
```

## Classification Metrics

### Accuracy
```runa
Import "math/ai_math/metrics" as Metrics

Note: Basic accuracy computation
Let y_true be Vector with components: ["0", "1", "2", "1", "0"], dimension: 5
Let y_pred be Vector with components: ["0", "1", "1", "1", "0"], dimension: 5

Let accuracy be Metrics.accuracy_score(y_true, y_pred, true)
Display "Accuracy: " joined with String(accuracy)
Note: Output: 0.8 (4 out of 5 correct predictions)
```

**Mathematical Formula**: Accuracy = (TP + TN) / (TP + TN + FP + FN)

**Properties**:
- Range: [0, 1] where 1 is perfect
- Simple and intuitive
- Can be misleading with imbalanced classes

### Precision, Recall, and F1-Score
```runa
Note: Binary classification metrics
Let binary_true be Vector with components: ["0", "1", "1", "0", "1"], dimension: 5
Let binary_pred be Vector with components: ["0", "1", "0", "0", "1"], dimension: 5

Let precision be Metrics.precision_score(binary_true, binary_pred, pos_label: 1)
Let recall be Metrics.recall_score(binary_true, binary_pred, pos_label: 1)
Let f1 be Metrics.f1_score(binary_true, binary_pred, pos_label: 1)

Display "Precision: " joined with String(precision)
Display "Recall: " joined with String(recall)
Display "F1-Score: " joined with String(f1)
```

**Mathematical Formulas**:
- Precision = TP / (TP + FP)
- Recall = TP / (TP + FN)  
- F1 = 2 × (Precision × Recall) / (Precision + Recall)

**Use Cases**:
- **Precision**: When false positives are costly
- **Recall**: When false negatives are costly
- **F1**: Balanced measure of both

### Multi-Class Classification Report
```runa
Note: Comprehensive classification evaluation
Let multiclass_true be Vector with components: ["0", "1", "2", "1", "0", "2", "1", "0"], dimension: 8
Let multiclass_pred be Vector with components: ["0", "1", "1", "1", "0", "2", "2", "0"], dimension: 8

Let metric_config be MetricConfig with:
    average: "weighted"
    zero_division: "warn"

Let classification_report be Metrics.classification_report(multiclass_true, multiclass_pred, metric_config)

Display "Classification Report:"
Display "Overall Accuracy: " joined with String(classification_report.accuracy)

Let class_idx be 0
While class_idx < classification_report.precision.dimension:
    Let class_precision be classification_report.precision.components.get(class_idx)
    Let class_recall be classification_report.recall.components.get(class_idx)
    Let class_f1 be classification_report.f1_score.components.get(class_idx)
    Let class_support be classification_report.support.components.get(class_idx)
    
    Display "Class " joined with String(class_idx) joined with ":"
    Display "  Precision: " joined with class_precision
    Display "  Recall: " joined with class_recall  
    Display "  F1-Score: " joined with class_f1
    Display "  Support: " joined with String(class_support)
    
    Set class_idx to class_idx + 1

Display "Weighted Average:"
Display "  Precision: " joined with String(classification_report.weighted_avg.precision)
Display "  Recall: " joined with String(classification_report.weighted_avg.recall)
Display "  F1-Score: " joined with String(classification_report.weighted_avg.f1_score)
```

### Confusion Matrix
```runa
Note: Detailed error analysis
Let confusion_matrix be Metrics.confusion_matrix(multiclass_true, multiclass_pred)

Display "Confusion Matrix:"
Let i be 0
While i < confusion_matrix.matrix.rows:
    Let row_str be ""
    Let j be 0
    While j < confusion_matrix.matrix.columns:
        Let cell_value be confusion_matrix.matrix.entries.get(i).get(j)
        Set row_str to row_str joined with cell_value joined with "\t"
        Set j to j + 1
    Display row_str
    Set i to i + 1

Note: Per-class metrics from confusion matrix
Display "Per-class metrics from confusion matrix:"
Let class_idx be 0
While class_idx < confusion_matrix.labels.dimension:
    Let tp be confusion_matrix.true_positives.components.get(class_idx)
    Let fp be confusion_matrix.false_positives.components.get(class_idx)
    Let fn be confusion_matrix.false_negatives.components.get(class_idx)
    Let tn be confusion_matrix.true_negatives.components.get(class_idx)
    
    Display "Class " joined with confusion_matrix.labels.get(class_idx) joined with ":"
    Display "  TP: " joined with String(tp) joined with ", FP: " joined with String(fp)
    Display "  FN: " joined with String(fn) joined with ", TN: " joined with String(tn)
    
    Set class_idx to class_idx + 1
```

### ROC-AUC and Precision-Recall Curves
```runa
Note: ROC curve for binary classification
Let y_scores be Vector with components: ["0.1", "0.8", "0.7", "0.3", "0.9"], dimension: 5
Let y_binary be Vector with components: ["0", "1", "1", "0", "1"], dimension: 5

Let roc_curve be Metrics.roc_curve(y_binary, y_scores, pos_label: 1)

Display "ROC Curve Analysis:"
Display "AUC: " joined with String(roc_curve.auc)
Display "Number of thresholds: " joined with String(roc_curve.thresholds.dimension)

Note: Find optimal threshold using Youden's J statistic
Let best_threshold_idx be Metrics.find_optimal_roc_threshold(roc_curve)
Let best_threshold be roc_curve.thresholds.components.get(best_threshold_idx)
Let best_tpr be roc_curve.tpr.components.get(best_threshold_idx)
Let best_fpr be roc_curve.fpr.components.get(best_threshold_idx)

Display "Optimal threshold: " joined with best_threshold
Display "TPR at optimal: " joined with best_tpr
Display "FPR at optimal: " joined with best_fpr

Note: Precision-Recall curve
Let pr_curve be Metrics.precision_recall_curve(y_binary, y_scores, pos_label: 1)
Let pr_auc be Metrics.auc(pr_curve.recall, pr_curve.precision)

Display "Precision-Recall AUC: " joined with String(pr_auc)
```

### Advanced Classification Metrics
```runa
Note: Additional classification metrics
Let matthews_cc be Metrics.matthews_corrcoef(y_binary, binary_pred)
Let cohen_kappa be Metrics.cohen_kappa_score(y_binary, binary_pred)
Let balanced_accuracy be Metrics.balanced_accuracy_score(multiclass_true, multiclass_pred)

Display "Matthews Correlation Coefficient: " joined with String(matthews_cc)
Display "Cohen's Kappa: " joined with String(cohen_kappa)
Display "Balanced Accuracy: " joined with String(balanced_accuracy)
```

**Matthews Correlation Coefficient**: 
- Range: [-1, 1] where 1 is perfect, 0 is random
- Good for imbalanced datasets
- Formula: (TP×TN - FP×FN) / √((TP+FP)(TP+FN)(TN+FP)(TN+FN))

## Regression Metrics

### Basic Regression Metrics
```runa
Note: Standard regression evaluation
Let y_true_reg be Vector with components: ["2.5", "1.8", "3.2", "2.1", "4.0"], dimension: 5
Let y_pred_reg be Vector with components: ["2.3", "1.9", "3.0", "2.2", "3.8"], dimension: 5

Let regression_metrics be Metrics.regression_metrics(y_true_reg, y_pred_reg)

Display "Regression Metrics:"
Display "MAE: " joined with String(regression_metrics.mae)
Display "MSE: " joined with String(regression_metrics.mse)
Display "RMSE: " joined with String(regression_metrics.rmse)
Display "R²: " joined with String(regression_metrics.r2_score)
Display "Adjusted R²: " joined with String(regression_metrics.adjusted_r2)
Display "MAPE: " joined with String(regression_metrics.mean_absolute_percentage_error) joined with "%"
```

**Mathematical Formulas**:
- MAE = (1/n) Σ |y_i - ŷ_i|
- MSE = (1/n) Σ (y_i - ŷ_i)²
- RMSE = √(MSE)
- R² = 1 - SS_res/SS_tot
- MAPE = (100/n) Σ |(y_i - ŷ_i)/y_i|

### Advanced Regression Metrics
```runa
Note: Additional regression evaluation metrics
Let max_error be Metrics.max_error(y_true_reg, y_pred_reg)
Let explained_variance be Metrics.explained_variance_score(y_true_reg, y_pred_reg)
Let median_absolute_error be Metrics.median_absolute_error(y_true_reg, y_pred_reg)

Display "Max Error: " joined with String(max_error)
Display "Explained Variance: " joined with String(explained_variance)
Display "Median Absolute Error: " joined with String(median_absolute_error)

Note: Custom quantile-based metrics
Let quantile_losses be Metrics.quantile_loss_metrics(y_true_reg, y_pred_reg, [0.1, 0.5, 0.9])
Display "10th Percentile Loss: " joined with String(quantile_losses.get(0))
Display "Median Loss (50th): " joined with String(quantile_losses.get(1))
Display "90th Percentile Loss: " joined with String(quantile_losses.get(2))
```

### Residual Analysis
```runa
Note: Analyze prediction residuals
Let residuals be Metrics.compute_residuals(y_true_reg, y_pred_reg)
Let residual_stats be Metrics.analyze_residuals(residuals)

Display "Residual Analysis:"
Display "Mean Residual: " joined with String(residual_stats.mean)
Display "Std Residual: " joined with String(residual_stats.std)
Display "Skewness: " joined with String(residual_stats.skewness)
Display "Kurtosis: " joined with String(residual_stats.kurtosis)

Note: Test residual normality
Let normality_test be Metrics.shapiro_wilk_test(residuals)
Display "Residuals Normality p-value: " joined with String(normality_test.p_value)

Note: Test heteroscedasticity
Let breusch_pagan_test be Metrics.breusch_pagan_test(residuals, y_pred_reg)
Display "Heteroscedasticity p-value: " joined with String(breusch_pagan_test.p_value)
```

## Ranking and Information Retrieval Metrics

### Precision and Recall at K
```runa
Note: Ranking evaluation metrics
Let relevant_items be Vector with components: ["1", "3", "5", "7"], dimension: 4  Note: True relevant items
Let retrieved_items be Vector with components: ["1", "2", "3", "4", "5"], dimension: 5  Note: Retrieved items (ranked)

Let precision_at_k be Metrics.precision_at_k(relevant_items, retrieved_items, k: 3)
Let recall_at_k be Metrics.recall_at_k(relevant_items, retrieved_items, k: 3)

Display "Precision@3: " joined with String(precision_at_k)
Display "Recall@3: " joined with String(recall_at_k)

Note: Compute for multiple k values
Let k_values be [1, 3, 5, 10]
Let precision_at_k_values be Metrics.precision_at_k_multi(relevant_items, retrieved_items, k_values)
Let recall_at_k_values be Metrics.recall_at_k_multi(relevant_items, retrieved_items, k_values)

Let i be 0
While i < k_values.length:
    Let k be k_values.get(i)
    Let prec_k be precision_at_k_values.get(i)
    Let rec_k be recall_at_k_values.get(i)
    
    Display "P@" joined with String(k) joined with ": " joined with String(prec_k)
    Display "R@" joined with String(k) joined with ": " joined with String(rec_k)
    Set i to i + 1
```

### NDCG (Normalized Discounted Cumulative Gain)
```runa
Note: NDCG for ranking quality with relevance scores
Let relevance_scores be Vector with components: ["3", "1", "2", "0", "1"], dimension: 5  Note: True relevance (0-3)
Let predicted_ranking be Vector with components: ["0", "2", "1", "4", "3"], dimension: 5  Note: Predicted item order

Let ndcg_at_3 be Metrics.ndcg_score(relevance_scores, predicted_ranking, k: 3)
Let ndcg_at_5 be Metrics.ndcg_score(relevance_scores, predicted_ranking, k: 5)

Display "NDCG@3: " joined with String(ndcg_at_3)
Display "NDCG@5: " joined with String(ndcg_at_5)

Note: Detailed NDCG computation breakdown
Let dcg_at_3 be Metrics.dcg_score(relevance_scores, predicted_ranking, k: 3)
Let idcg_at_3 be Metrics.ideal_dcg_score(relevance_scores, k: 3)

Display "DCG@3: " joined with String(dcg_at_3)
Display "Ideal DCG@3: " joined with String(idcg_at_3)
```

**Mathematical Formula**: NDCG@k = DCG@k / IDCG@k

Where DCG@k = rel₁ + Σᵢ₌₂ᵏ (relᵢ / log₂(i+1))

### Mean Average Precision (MAP)
```runa
Note: MAP for multiple queries
Let query_results be List[QueryResult]()

Note: Query 1
Let query1_relevant be Vector with components: ["1", "3", "5"], dimension: 3
Let query1_retrieved be Vector with components: ["1", "2", "3", "4", "5", "6"], dimension: 6
Call query_results.add(QueryResult with relevant: query1_relevant, retrieved: query1_retrieved)

Note: Query 2  
Let query2_relevant be Vector with components: ["2", "4"], dimension: 2
Let query2_retrieved be Vector with components: ["1", "2", "3", "4"], dimension: 4
Call query_results.add(QueryResult with relevant: query2_relevant, retrieved: query2_retrieved)

Let map_score be Metrics.mean_average_precision(query_results)
Display "Mean Average Precision: " joined with String(map_score)

Note: Individual query AP scores
Let query_idx be 0
While query_idx < query_results.length:
    Let query_result be query_results.get(query_idx)
    Let ap_score be Metrics.average_precision(query_result.relevant, query_result.retrieved)
    Display "Query " joined with String(query_idx + 1) joined with " AP: " joined with String(ap_score)
    Set query_idx to query_idx + 1
```

### Mean Reciprocal Rank (MRR)
```runa
Note: MRR for question answering and search
Let query_rankings be List[Vector[Integer]]()

Note: Rankings where first relevant item position matters
Call query_rankings.add(Vector with components: ["2"], dimension: 1)  Note: Relevant item at position 2
Call query_rankings.add(Vector with components: ["1"], dimension: 1)  Note: Relevant item at position 1
Call query_rankings.add(Vector with components: ["4"], dimension: 1)  Note: Relevant item at position 4

Let mrr_score be Metrics.mean_reciprocal_rank(query_rankings)
Display "Mean Reciprocal Rank: " joined with String(mrr_score)
```

**Mathematical Formula**: MRR = (1/|Q|) Σᵢ (1/rankᵢ) where rankᵢ is position of first relevant item

## Clustering Metrics

### Internal Clustering Metrics
```runa
Note: Clustering evaluation without ground truth
Let data_points be Matrix with entries: [
    ["1.0", "2.0"],      Note: Data point coordinates
    ["1.5", "2.1"],
    ["5.0", "6.0"],
    ["5.2", "6.1"],
    ["9.0", "10.0"],
    ["9.1", "9.8"]
]

Let cluster_labels be Vector with components: ["0", "0", "1", "1", "2", "2"], dimension: 6

Note: Silhouette analysis
Let silhouette_score be Metrics.silhouette_score(data_points, cluster_labels)
Let silhouette_samples be Metrics.silhouette_samples(data_points, cluster_labels)

Display "Average Silhouette Score: " joined with String(silhouette_score)
Display "Individual Silhouette Scores:"
Let point_idx be 0
While point_idx < silhouette_samples.dimension:
    Let point_silhouette be silhouette_samples.components.get(point_idx)
    Display "  Point " joined with String(point_idx) joined with ": " joined with point_silhouette
    Set point_idx to point_idx + 1

Note: Other internal metrics
Let calinski_harabasz be Metrics.calinski_harabasz_score(data_points, cluster_labels)
Let davies_bouldin be Metrics.davies_bouldin_score(data_points, cluster_labels)

Display "Calinski-Harabasz Score: " joined with String(calinski_harabasz)
Display "Davies-Bouldin Score: " joined with String(davies_bouldin)
```

### External Clustering Metrics
```runa
Note: Clustering evaluation with ground truth
Let true_labels be Vector with components: ["0", "0", "1", "1", "2", "2"], dimension: 6
Let predicted_labels be Vector with components: ["0", "0", "1", "2", "2", "2"], dimension: 6

Let ari_score be Metrics.adjusted_rand_index(true_labels, predicted_labels)
Let ami_score be Metrics.adjusted_mutual_info_score(true_labels, predicted_labels)
Let nmi_score be Metrics.normalized_mutual_info_score(true_labels, predicted_labels)
Let homogeneity be Metrics.homogeneity_score(true_labels, predicted_labels)
Let completeness be Metrics.completeness_score(true_labels, predicted_labels)
Let v_measure be Metrics.v_measure_score(true_labels, predicted_labels)

Display "External Clustering Metrics:"
Display "Adjusted Rand Index: " joined with String(ari_score)
Display "Adjusted Mutual Information: " joined with String(ami_score)
Display "Normalized Mutual Information: " joined with String(nmi_score)
Display "Homogeneity: " joined with String(homogeneity)
Display "Completeness: " joined with String(completeness)
Display "V-Measure: " joined with String(v_measure)
```

**Adjusted Rand Index**:
- Range: [-1, 1] where 1 is perfect clustering
- Adjusts for chance grouping
- Good for comparing different numbers of clusters

## Probabilistic and Calibration Metrics

### Calibration Assessment
```runa
Note: Model calibration evaluation
Let y_prob be Vector with components: ["0.1", "0.8", "0.7", "0.3", "0.9"], dimension: 5  Note: Predicted probabilities
Let y_true_binary be Vector with components: ["0", "1", "1", "0", "1"], dimension: 5

Let calibration_curve be Metrics.calibration_curve(y_true_binary, y_prob, n_bins: 5)

Display "Calibration Analysis:"
Display "Number of bins: " joined with String(calibration_curve.bin_boundaries.dimension - 1)

Let bin_idx be 0
While bin_idx < calibration_curve.fraction_of_positives.dimension:
    Let mean_pred_prob be calibration_curve.mean_predicted_value.components.get(bin_idx)
    Let fraction_pos be calibration_curve.fraction_of_positives.components.get(bin_idx)
    Let count be calibration_curve.bin_counts.components.get(bin_idx)
    
    Display "Bin " joined with String(bin_idx) joined with ":"
    Display "  Mean Predicted: " joined with mean_pred_prob
    Display "  Fraction Positive: " joined with fraction_pos
    Display "  Count: " joined with String(count)
    
    Set bin_idx to bin_idx + 1

Note: Calibration metrics
Let brier_score be Metrics.brier_score_loss(y_true_binary, y_prob)
Let reliability_score be Metrics.reliability_score(calibration_curve)
Let resolution_score be Metrics.resolution_score(calibration_curve)

Display "Brier Score: " joined with String(brier_score)
Display "Reliability: " joined with String(reliability_score)
Display "Resolution: " joined with String(resolution_score)
```

### Log-Loss and Cross-Entropy
```runa
Note: Probabilistic classification metrics
Let y_true_multiclass be Vector with components: ["0", "1", "2", "1", "0"], dimension: 5
Let y_prob_multiclass be Matrix with entries: [
    ["0.8", "0.1", "0.1"],    Note: Probabilities for each class
    ["0.2", "0.6", "0.2"],
    ["0.1", "0.2", "0.7"],
    ["0.3", "0.5", "0.2"],
    ["0.9", "0.05", "0.05"]
]

Let log_loss be Metrics.log_loss(y_true_multiclass, y_prob_multiclass)
Let cross_entropy be Metrics.cross_entropy_loss(y_true_multiclass, y_prob_multiclass)

Display "Log Loss: " joined with String(log_loss)
Display "Cross Entropy: " joined with String(cross_entropy)

Note: Per-class log loss
Let per_class_log_loss be Metrics.per_class_log_loss(y_true_multiclass, y_prob_multiclass)
Let class_idx be 0
While class_idx < per_class_log_loss.dimension:
    Let class_loss be per_class_log_loss.components.get(class_idx)
    Display "Class " joined with String(class_idx) joined with " Log Loss: " joined with class_loss
    Set class_idx to class_idx + 1
```

## Fairness and Bias Metrics

### Demographic Parity
```runa
Note: Fairness evaluation across protected groups
Let sensitive_attribute be Vector with components: ["0", "1", "0", "1", "0"], dimension: 5  Note: 0=Group A, 1=Group B
Let y_pred_fair be Vector with components: ["1", "1", "0", "1", "0"], dimension: 5  Note: Model predictions

Let demographic_parity be Metrics.demographic_parity_difference(y_pred_fair, sensitive_attribute)
Let equalized_odds be Metrics.equalized_odds_difference(y_true, y_pred_fair, sensitive_attribute)

Display "Demographic Parity Difference: " joined with String(demographic_parity)
Display "Equalized Odds Difference: " joined with String(equalized_odds)

Note: Statistical parity by group
Let group_statistics be Metrics.compute_group_statistics(y_true, y_pred_fair, sensitive_attribute)

Display "Group Statistics:"
For Each group_id, stats in group_statistics:
    Display "Group " joined with String(group_id) joined with ":"
    Display "  Positive Rate: " joined with String(stats.positive_rate)
    Display "  True Positive Rate: " joined with String(stats.tpr)
    Display "  False Positive Rate: " joined with String(stats.fpr)
    Display "  Accuracy: " joined with String(stats.accuracy)
```

### Individual Fairness Metrics
```runa
Note: Individual fairness assessment
Let similarity_matrix be Matrix with entries: similarity_data  Note: Pairwise similarity between individuals
Let prediction_distances be Matrix with entries: pred_distance_data  Note: Prediction differences

Let individual_fairness be Metrics.individual_fairness_score(similarity_matrix, prediction_distances)
Let lipschitz_constant be Metrics.estimate_lipschitz_constant(similarity_matrix, prediction_distances)

Display "Individual Fairness Score: " joined with String(individual_fairness)
Display "Estimated Lipschitz Constant: " joined with String(lipschitz_constant)
```

## Advanced Metrics and Analysis

### Bootstrap Confidence Intervals
```runa
Note: Uncertainty estimation for metrics
Let bootstrap_config be BootstrapConfig with:
    n_bootstrap_samples: 1000
    confidence_level: 0.95
    random_seed: 42

Let metric_confidence be Metrics.bootstrap_metric_confidence(
    y_true,
    y_pred,
    "accuracy",
    bootstrap_config
)

Display "Accuracy Confidence Interval:"
Display "Point Estimate: " joined with String(metric_confidence.point_estimate)
Display "95% CI: [" joined with String(metric_confidence.ci_lower) joined with ", " joined with String(metric_confidence.ci_upper) joined with "]"
Display "Standard Error: " joined with String(metric_confidence.standard_error)
```

### Statistical Significance Testing
```runa
Note: Compare two models' performance
Let model1_predictions be Vector with components: model1_preds, dimension: test_size
Let model2_predictions be Vector with components: model2_preds, dimension: test_size

Let comparison_result be Metrics.mcnemar_test(y_true, model1_predictions, model2_predictions)

Display "McNemar's Test Results:"
Display "Statistic: " joined with String(comparison_result.statistic)
Display "P-value: " joined with String(comparison_result.p_value)
Display "Significant difference: " joined with String(comparison_result.p_value < 0.05)

Note: Permutation test for metric difference
Let permutation_test be Metrics.permutation_test_metric_difference(
    y_true,
    model1_predictions,
    model2_predictions,
    "f1_score",
    n_permutations: 1000
)

Display "Permutation Test P-value: " joined with String(permutation_test.p_value)
```

### Cross-Validation Metrics
```runa
Note: Cross-validation performance evaluation
Let cv_config be CrossValidationConfig with:
    n_folds: 5
    shuffle: true
    random_state: 42
    stratified: true

Let cv_scores be Metrics.cross_validate_metrics(
    model,
    X_data,
    y_data,
    ["accuracy", "f1_score", "precision", "recall"],
    cv_config
)

Display "Cross-Validation Results:"
For Each metric_name, scores in cv_scores:
    Let mean_score be compute_mean(scores)
    Let std_score be compute_std(scores)
    
    Display metric_name joined with ":"
    Display "  Mean: " joined with String(mean_score) joined with " (±" joined with String(std_score) joined with ")"
    Display "  Individual folds: " joined with String(scores)
```

## Metric Selection Guidelines

### Classification Task Guidelines
```runa
Note: Metric selection based on problem characteristics
Process called "recommend_classification_metrics" that takes problem_type as String, class_balance as String, cost_sensitive as Boolean returns List[String]:
    Let recommended_metrics be List[String]()
    
    If class_balance == "balanced":
        Call recommended_metrics.add("accuracy")
        Call recommended_metrics.add("f1_score")
    Otherwise:
        Call recommended_metrics.add("balanced_accuracy")
        Call recommended_metrics.add("f1_score")
        Call recommended_metrics.add("roc_auc")
    
    If cost_sensitive:
        If problem_type == "medical_diagnosis":
            Call recommended_metrics.add("recall")  Note: Minimize false negatives
            Call recommended_metrics.add("sensitivity")
        Otherwise if problem_type == "spam_detection":
            Call recommended_metrics.add("precision")  Note: Minimize false positives
            Call recommended_metrics.add("specificity")
    
    Call recommended_metrics.add("confusion_matrix")
    Call recommended_metrics.add("classification_report")
    
    Return recommended_metrics
```

### Regression Task Guidelines
```runa
Process called "recommend_regression_metrics" that takes target_scale as String, outliers_present as Boolean returns List[String]:
    Let recommended_metrics be List[String]()
    
    If outliers_present:
        Call recommended_metrics.add("median_absolute_error")
        Call recommended_metrics.add("quantile_loss")
    Otherwise:
        Call recommended_metrics.add("rmse")
        Call recommended_metrics.add("mae")
    
    Call recommended_metrics.add("r2_score")
    
    If target_scale == "percentage" or target_scale == "ratio":
        Call recommended_metrics.add("mean_absolute_percentage_error")
    
    Call recommended_metrics.add("residual_analysis")
    
    Return recommended_metrics
```

## Performance Optimization

### Efficient Metric Computation
```runa
Note: Optimized metric computation for large datasets
Process called "compute_metrics_efficiently" that takes y_true as Vector[Integer], y_pred as Vector[Integer], metrics as List[String] returns Dictionary[String, Float]:
    Let results be Dictionary[String, Float]()
    
    Note: Compute confusion matrix once and derive multiple metrics
    Let cm be Metrics.confusion_matrix(y_true, y_pred)
    
    For Each metric_name in metrics:
        If metric_name == "accuracy":
            Let accuracy be Metrics.accuracy_from_confusion_matrix(cm)
            Set results[metric_name] to accuracy
        Otherwise if metric_name == "precision":
            Let precision be Metrics.precision_from_confusion_matrix(cm)
            Set results[metric_name] to precision
        Otherwise if metric_name == "recall":
            Let recall be Metrics.recall_from_confusion_matrix(cm)
            Set results[metric_name] to recall
        Otherwise if metric_name == "f1_score":
            Let precision be Metrics.precision_from_confusion_matrix(cm)
            Let recall be Metrics.recall_from_confusion_matrix(cm)
            Let f1 be 2.0 * (precision * recall) / (precision + recall)
            Set results[metric_name] to f1
    
    Return results
```

### Incremental Metric Updates
```runa
Note: Online metric computation for streaming data
Let incremental_accuracy be Metrics.create_incremental_accuracy_tracker()

Process called "update_metrics_online" that takes new_true as Integer, new_pred as Integer:
    Call Metrics.update_incremental_tracker(incremental_accuracy, new_true, new_pred)
    
    Let current_accuracy be Metrics.get_current_accuracy(incremental_accuracy)
    Let sample_count be Metrics.get_sample_count(incremental_accuracy)
    
    If sample_count % 1000 == 0:
        Display "Accuracy after " joined with String(sample_count) joined with " samples: " joined with String(current_accuracy)
```

## Testing and Validation

### Metric Implementation Tests
```runa
Note: Unit tests for metric correctness
Process called "test_metric_implementations":
    Note: Test accuracy with known values
    Let perfect_true be Vector with components: ["1", "0", "1", "0"], dimension: 4
    Let perfect_pred be Vector with components: ["1", "0", "1", "0"], dimension: 4
    Let perfect_accuracy be Metrics.accuracy_score(perfect_true, perfect_pred, true)
    
    Assert perfect_accuracy == 1.0
    
    Note: Test with no correct predictions
    Let wrong_pred be Vector with components: ["0", "1", "0", "1"], dimension: 4
    Let zero_accuracy be Metrics.accuracy_score(perfect_true, wrong_pred, true)
    
    Assert zero_accuracy == 0.0
    
    Display "Accuracy tests passed"
    
    Note: Test F1 score properties
    Let binary_true be Vector with components: ["1", "1", "0", "0"], dimension: 4
    Let binary_pred be Vector with components: ["1", "0", "1", "0"], dimension: 4
    
    Let precision be Metrics.precision_score(binary_true, binary_pred, pos_label: 1)
    Let recall be Metrics.recall_score(binary_true, binary_pred, pos_label: 1)
    Let f1 be Metrics.f1_score(binary_true, binary_pred, pos_label: 1)
    
    Let expected_f1 be 2.0 * (precision * recall) / (precision + recall)
    Assert Math.abs(f1 - expected_f1) < 1e-10
    
    Display "F1 score tests passed"
```

### Edge Case Handling Tests
```runa
Process called "test_edge_cases":
    Note: Test with all predictions same class
    Let uniform_true be Vector with components: ["0", "1", "0", "1"], dimension: 4
    Let uniform_pred be Vector with components: ["0", "0", "0", "0"], dimension: 4
    
    Note: Should handle gracefully without division by zero
    Let precision_uniform be Metrics.precision_score(uniform_true, uniform_pred, pos_label: 1)
    Let recall_uniform be Metrics.recall_score(uniform_true, uniform_pred, pos_label: 1)
    
    Display "Precision with no positive predictions: " joined with String(precision_uniform)
    Display "Recall with no positive predictions: " joined with String(recall_uniform)
    
    Note: Test with empty inputs (should raise appropriate error)
    Try:
        Let empty_true be Vector with components: [], dimension: 0
        Let empty_pred be Vector with components: [], dimension: 0
        Let empty_accuracy be Metrics.accuracy_score(empty_true, empty_pred, true)
    Catch Errors.InvalidArgument as error:
        Display "Correctly caught empty input error: " joined with error.message
    
    Display "Edge case tests passed"
```

## Related Documentation

- **[AI Math Neural Ops](neural_ops.md)**: Neural network operations for model building
- **[AI Math Loss Functions](loss_functions.md)**: Loss functions used during training
- **[Math Statistics](../statistics/README.md)**: Statistical methods for evaluation
- **[Math Probability](../probability/README.md)**: Probability distributions for metrics
- **[Math Core Operations](../core/operations.md)**: Basic mathematical operations

The Machine Learning Evaluation Metrics module provides comprehensive tools for assessing model performance across all machine learning domains, enabling rigorous evaluation and comparison of different approaches.