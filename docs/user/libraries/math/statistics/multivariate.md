Note: Math Statistics Multivariate Module

## Overview

The `math/statistics/multivariate` module provides comprehensive multivariate statistical analysis capabilities for complex multi-dimensional data. It includes principal component analysis, factor analysis, canonical correlation, discriminant analysis, cluster analysis, and multivariate hypothesis testing for understanding relationships and patterns in high-dimensional datasets.

## Key Features

- **Dimensionality Reduction**: PCA, Factor Analysis, Independent Component Analysis
- **Cluster Analysis**: K-means, hierarchical clustering, mixture models
- **Discriminant Analysis**: Linear and quadratic discriminant analysis
- **Canonical Correlation**: Relationship analysis between variable sets
- **Multivariate Tests**: MANOVA, Hotelling's T², multivariate normality
- **Distance Metrics**: Mahalanobis, Euclidean, Manhattan distances
- **Classification**: Multivariate classification and prediction methods

## Data Types

### MultivariateAnalysis
Base multivariate analysis structure:
```runa
Type called "MultivariateAnalysis":
    analysis_type as String
    data_matrix as List[List[Float]]
    sample_size as Integer
    num_variables as Integer
    covariance_matrix as List[List[Float]]
    correlation_matrix as List[List[Float]]
    eigenvalues as List[Float]
    eigenvectors as List[List[Float]]
    explained_variance as List[Float]
```

### PCAResult
Principal Component Analysis results:
```runa
Type called "PCAResult":
    principal_components as List[List[Float]]
    component_loadings as List[List[Float]]
    eigenvalues as List[Float]
    explained_variance_ratio as List[Float]
    cumulative_variance_ratio as List[Float]
    component_scores as List[List[Float]]
    biplot_coordinates as Dictionary[String, List[List[Float]]]
```

### ClusterAnalysis
Clustering analysis results:
```runa
Type called "ClusterAnalysis":
    cluster_method as String
    num_clusters as Integer
    cluster_assignments as List[Integer]
    cluster_centers as List[List[Float]]
    within_cluster_ss as List[Float]
    total_within_ss as Float
    between_cluster_ss as Float
    silhouette_scores as List[Float]
    cluster_quality_metrics as Dictionary[String, Float]
```

## Principal Component Analysis

### Standard PCA
```runa
Import "math/statistics/multivariate" as Multivariate

Note: Reduce dimensionality of correlated variables
Let data_matrix be [
    [2.5, 2.4, 3.1, 2.8, 1.9],  Note: 5 variables, 10 observations
    [0.5, 0.7, 1.2, 0.9, 0.3],
    [2.2, 2.9, 3.0, 2.7, 1.8],
    [1.9, 2.2, 2.8, 2.1, 1.6],
    [3.1, 3.0, 3.8, 3.2, 2.1],
    [2.3, 2.7, 2.9, 2.6, 1.7],
    [2.0, 1.6, 2.1, 1.8, 1.2],
    [1.0, 1.1, 1.7, 1.4, 0.8],
    [1.5, 1.6, 2.3, 2.0, 1.1],
    [1.1, 0.9, 1.5, 1.2, 0.7]
]

Let pca_result be Multivariate.principal_component_analysis(data_matrix, true, 3)

Display "Principal Component Analysis Results:"
Display "  Original variables: " joined with String(Length(data_matrix[0]))
Display "  Components extracted: " joined with String(Length(pca_result.explained_variance_ratio))
Display "  Sample size: " joined with String(Length(data_matrix))

Display "  Explained variance by component:"
For i from 0 to Length(pca_result.explained_variance_ratio) - 1:
    Display "    PC" joined with String(i + 1) joined with ": " joined with String(pca_result.explained_variance_ratio[i] * 100.0) joined with "% (eigenvalue = " joined with String(pca_result.eigenvalues[i]) joined with ")"

Display "  Cumulative variance explained:"
For i from 0 to Length(pca_result.cumulative_variance_ratio) - 1:
    Display "    First " joined with String(i + 1) joined with " components: " joined with String(pca_result.cumulative_variance_ratio[i] * 100.0) joined with "%"
```

### Component Loadings and Interpretation
```runa
Note: Interpret component meanings through loadings
Display "  Component loadings (correlations with original variables):"
For component from 0 to 2:
    Display "    PC" joined with String(component + 1) joined with " loadings:"
    For variable from 0 to Length(data_matrix[0]) - 1:
        Let loading_value be pca_result.component_loadings[component][variable]
        Let interpretation be ""
        If MathOps.absolute_value(String(loading_value)).result_value > "0.7":
            Set interpretation to "(high)"
        Otherwise if MathOps.absolute_value(String(loading_value)).result_value > "0.4":
            Set interpretation to "(moderate)"
        Otherwise:
            Set interpretation to "(low)"
        Display "      Var" joined with String(variable + 1) joined with ": " joined with String(loading_value) joined with " " joined with interpretation

Note: Kaiser criterion for component retention
Display "  Components with eigenvalue > 1 (Kaiser criterion): "
Let kaiser_components be 0
For Each eigenvalue in pca_result.eigenvalues:
    If eigenvalue > 1.0:
        Set kaiser_components to kaiser_components + 1
Display String(kaiser_components)
```

### Robust PCA
```runa
Note: PCA robust to outliers using principal component pursuit
Let robust_pca_result be Multivariate.robust_pca(data_matrix, 0.1, 100)

Display "Robust PCA Results:"
Display "  Low-rank component extracted"
Display "  Sparse component (outliers) detected"
Display "  Robust explained variance ratios:"
For i from 0 to 2:
    Display "    Robust PC" joined with String(i + 1) joined with ": " joined with String(robust_pca_result.explained_variance_ratio[i] * 100.0) joined with "%"

Note: Compare standard vs robust PCA
Display "  Comparison (first component):"
Display "    Standard PCA: " joined with String(pca_result.explained_variance_ratio[0] * 100.0) joined with "%"
Display "    Robust PCA: " joined with String(robust_pca_result.explained_variance_ratio[0] * 100.0) joined with "%"
Display "    Difference: " joined with String(MathOps.absolute_value(String(pca_result.explained_variance_ratio[0] - robust_pca_result.explained_variance_ratio[0])).result_value * 100.0) joined with "%"
```

### Kernel PCA
```runa
Note: Nonlinear dimensionality reduction
Let kernel_params be Dictionary with:
    "gamma": "0.1"
    "degree": "3"
    "coef0": "0.0"

Let kernel_pca_result be Multivariate.kernel_pca(data_matrix, "rbf", kernel_params, 3)

Display "Kernel PCA Results (RBF kernel):"
Display "  Kernel type: RBF (Radial Basis Function)"
Display "  Gamma parameter: " joined with String(kernel_params["gamma"])
Display "  Components extracted: " joined with String(Length(kernel_pca_result.explained_variance_ratio))
Display "  Nonlinear explained variance:"
For i from 0 to Length(kernel_pca_result.explained_variance_ratio) - 1:
    Display "    Kernel PC" joined with String(i + 1) joined with ": " joined with String(kernel_pca_result.explained_variance_ratio[i] * 100.0) joined with "%"
```

## Factor Analysis

### Exploratory Factor Analysis
```runa
Note: Identify latent factors underlying observed variables
Let factor_config be Dictionary with:
    "n_factors": "2"
    "rotation": "varimax"
    "extraction": "principal_axis"
    "max_iterations": "100"

Let efa_result be Multivariate.exploratory_factor_analysis(data_matrix, factor_config)

Display "Exploratory Factor Analysis Results:"
Display "  Number of factors: " joined with String(efa_result.n_factors)
Display "  Extraction method: " joined with factor_config["extraction"]
Display "  Rotation: " joined with factor_config["rotation"]
Display "  Converged: " joined with String(efa_result.converged)

Display "  Factor loadings (after rotation):"
For factor from 0 to efa_result.n_factors - 1:
    Display "    Factor " joined with String(factor + 1) joined with ":"
    For variable from 0 to Length(data_matrix[0]) - 1:
        Let loading be efa_result.factor_loadings[variable][factor]
        Display "      Var" joined with String(variable + 1) joined with ": " joined with String(loading)

Display "  Communalities (proportion of variance explained):"
For variable from 0 to Length(efa_result.communalities) - 1:
    Display "    Var" joined with String(variable + 1) joined with ": " joined with String(efa_result.communalities[variable])

Display "  Uniquenesses (unique variance):"
For variable from 0 to Length(efa_result.uniquenesses) - 1:
    Display "    Var" joined with String(variable + 1) joined with ": " joined with String(efa_result.uniquenesses[variable])
```

### Factor Score Computation
```runa
Note: Compute factor scores for observations
Let factor_scores be Multivariate.compute_factor_scores(data_matrix, efa_result, "regression")

Display "  Factor scores (first 5 observations):"
For obs from 0 to 4:
    Display "    Observation " joined with String(obs + 1) joined with ":"
    For factor from 0 to efa_result.n_factors - 1:
        Display "      Factor " joined with String(factor + 1) joined with ": " joined with String(factor_scores[obs][factor])
```

### Factor Model Fit
```runa
Note: Assess factor model adequacy
Display "  Model fit statistics:"
Display "    Chi-square: " joined with String(efa_result.goodness_of_fit["chi_square"])
Display "    Degrees of freedom: " joined with String(efa_result.goodness_of_fit["df"])
Display "    P-value: " joined with String(efa_result.goodness_of_fit["p_value"])
Display "    RMSEA: " joined with String(efa_result.goodness_of_fit["rmsea"])
Display "    CFI: " joined with String(efa_result.goodness_of_fit["cfi"])
Display "    TLI: " joined with String(efa_result.goodness_of_fit["tli"])

Note: Interpret fit indices
Let fit_adequate be efa_result.goodness_of_fit["rmsea"] < 0.08 and efa_result.goodness_of_fit["cfi"] > 0.95
Display "    Model fit adequate: " joined with String(fit_adequate)
```

## Cluster Analysis

### K-Means Clustering
```runa
Note: Partition data into k clusters
Let k_values be [2, 3, 4, 5]
Let kmeans_results be []

Display "K-Means Clustering Analysis:"
For Each k in k_values:
    Let kmeans_result be Multivariate.k_means_clustering(data_matrix, k, 100, 42)
    Call kmeans_results.append(kmeans_result)
    
    Display "  K = " joined with String(k) joined with ":"
    Display "    Converged: " joined with String(kmeans_result.converged)
    Display "    Iterations: " joined with String(kmeans_result.iterations)
    Display "    Total within-cluster SS: " joined with String(kmeans_result.total_within_ss)
    Display "    Average silhouette score: " joined with String(DescriptiveStats.calculate_arithmetic_mean(kmeans_result.silhouette_scores, []))

Note: Elbow method for optimal k
Display "  Elbow method (within-cluster SS):"
For i from 0 to Length(kmeans_results) - 1:
    Display "    K=" joined with String(k_values[i]) joined with ": WCSS=" joined with String(kmeans_results[i].total_within_ss)
```

### Hierarchical Clustering
```runa
Note: Build hierarchy of clusters using linkage criteria
Let linkage_methods be ["single", "complete", "average", "ward"]

Display "Hierarchical Clustering Results:"
For Each linkage in linkage_methods:
    Let hierarchical_result be Multivariate.hierarchical_clustering(data_matrix, linkage, "euclidean")
    
    Display "  Linkage: " joined with linkage
    Display "    Distance matrix computed"
    Display "    Dendrogram height range: " joined with String(hierarchical_result.min_height) joined with " to " joined with String(hierarchical_result.max_height)
    
    Note: Cut dendrogram at different heights
    Let cut_height be hierarchical_result.max_height * 0.6
    Let clusters_at_height be Multivariate.cut_dendrogram(hierarchical_result, cut_height)
    Display "    Clusters at 60% height: " joined with String(clusters_at_height.num_clusters)
```

### Gaussian Mixture Models
```runa
Note: Model data as mixture of Gaussian distributions
Let gmm_config be Dictionary with:
    "n_components": "3"
    "covariance_type": "full"
    "max_iterations": "100"
    "tolerance": "1e-6"
    "initialization": "k_means"

Let gmm_result be Multivariate.gaussian_mixture_model(data_matrix, gmm_config)

Display "Gaussian Mixture Model Results:"
Display "  Number of components: " joined with String(gmm_result.n_components)
Display "  Covariance type: " joined with gmm_config["covariance_type"]
Display "  Converged: " joined with String(gmm_result.converged)
Display "  Log-likelihood: " joined with String(gmm_result.log_likelihood)
Display "  AIC: " joined with String(gmm_result.aic)
Display "  BIC: " joined with String(gmm_result.bic)

Display "  Component parameters:"
For component from 0 to gmm_result.n_components - 1:
    Display "    Component " joined with String(component + 1) joined with ":"
    Display "      Weight: " joined with String(gmm_result.weights[component])
    Display "      Mean: " joined with String(gmm_result.means[component])
    Note: Display only diagonal of covariance for brevity
    Display "      Covariance diagonal: " joined with String(gmm_result.covariance_matrices[component].diagonal)
```

## Discriminant Analysis

### Linear Discriminant Analysis
```runa
Note: Classification using linear discriminants
Let group_labels be [0, 0, 0, 1, 1, 1, 2, 2, 2, 2]  Note: Three groups
Let lda_result be Multivariate.linear_discriminant_analysis(data_matrix, group_labels)

Display "Linear Discriminant Analysis Results:"
Display "  Number of groups: " joined with String(lda_result.n_classes)
Display "  Number of discriminant functions: " joined with String(lda_result.n_discriminants)

Display "  Discriminant function eigenvalues:"
For i from 0 to Length(lda_result.eigenvalues) - 1:
    Let canonical_corr be MathOps.square_root(String(lda_result.eigenvalues[i] / (1.0 + lda_result.eigenvalues[i])), 15).result_value
    Display "    LD" joined with String(i + 1) joined with ": eigenvalue=" joined with String(lda_result.eigenvalues[i]) joined with ", canonical R=" joined with String(canonical_corr)

Display "  Group centroids (discriminant space):"
For group from 0 to lda_result.n_classes - 1:
    Display "    Group " joined with String(group) joined with ": " joined with String(lda_result.group_centroids[group])

Note: Classification accuracy
Let lda_predictions be Multivariate.predict_lda(lda_result, data_matrix)
Let correct_predictions be 0
For i from 0 to Length(group_labels) - 1:
    If lda_predictions.predicted_classes[i] == group_labels[i]:
        Set correct_predictions to correct_predictions + 1

Let accuracy be Float(correct_predictions) / Float(Length(group_labels))
Display "  Classification accuracy: " joined with String(accuracy * 100.0) joined with "%"
```

### Quadratic Discriminant Analysis
```runa
Note: QDA allows different covariance matrices per group
Let qda_result be Multivariate.quadratic_discriminant_analysis(data_matrix, group_labels)

Display "Quadratic Discriminant Analysis Results:"
Display "  Number of groups: " joined with String(qda_result.n_classes)
Display "  Equal covariance assumption: relaxed"

Display "  Group covariance matrices (determinants):"
For group from 0 to qda_result.n_classes - 1:
    Let det_cov be Multivariate.matrix_determinant(qda_result.group_covariances[group])
    Display "    Group " joined with String(group) joined with ": det(Σ) = " joined with String(det_cov)

Note: Compare LDA vs QDA accuracy
Let qda_predictions be Multivariate.predict_qda(qda_result, data_matrix)
Let qda_correct be 0
For i from 0 to Length(group_labels) - 1:
    If qda_predictions.predicted_classes[i] == group_labels[i]:
        Set qda_correct to qda_correct + 1

Let qda_accuracy be Float(qda_correct) / Float(Length(group_labels))
Display "  QDA accuracy: " joined with String(qda_accuracy * 100.0) joined with "%"
Display "  LDA vs QDA: " joined with String(lda_accuracy * 100.0) joined with "% vs " joined with String(qda_accuracy * 100.0) joined with "%"
```

## Canonical Correlation Analysis

### Canonical Correlation
```runa
Note: Analyze relationships between two sets of variables
Let X_set be [
    [2.5, 2.4],  Note: First variable set
    [0.5, 0.7],
    [2.2, 2.9],
    [1.9, 2.2],
    [3.1, 3.0],
    [2.3, 2.7],
    [2.0, 1.6],
    [1.0, 1.1]
]

Let Y_set be [
    [3.1, 2.8, 1.9],  Note: Second variable set
    [1.2, 0.9, 0.3],
    [3.0, 2.7, 1.8],
    [2.8, 2.1, 1.6],
    [3.8, 3.2, 2.1],
    [2.9, 2.6, 1.7],
    [2.1, 1.8, 1.2],
    [1.7, 1.4, 0.8]
]

Let cca_result be Multivariate.canonical_correlation_analysis(X_set, Y_set)

Display "Canonical Correlation Analysis Results:"
Display "  X variables: " joined with String(Length(X_set[0]))
Display "  Y variables: " joined with String(Length(Y_set[0]))
Display "  Canonical correlations: " joined with String(Length(cca_result.canonical_correlations))

Display "  Canonical correlations:"
For i from 0 to Length(cca_result.canonical_correlations) - 1:
    Display "    CC" joined with String(i + 1) joined with ": " joined with String(cca_result.canonical_correlations[i])
    
    Note: Statistical significance
    Let wilks_lambda be cca_result.significance_tests["wilks_lambda"][i]
    Let p_value be cca_result.significance_tests["p_values"][i]
    Display "      Wilks' Λ: " joined with String(wilks_lambda) joined with " (p = " joined with String(p_value) joined with ")"

Display "  Canonical loadings:"
Display "    X set loadings (first canonical variate):"
For i from 0 to Length(cca_result.canonical_loadings_x[0]) - 1:
    Display "      X" joined with String(i + 1) joined with ": " joined with String(cca_result.canonical_loadings_x[0][i])
    
Display "    Y set loadings (first canonical variate):"
For i from 0 to Length(cca_result.canonical_loadings_y[0]) - 1:
    Display "      Y" joined with String(i + 1) joined with ": " joined with String(cca_result.canonical_loadings_y[0][i])
```

### Redundancy Analysis
```runa
Note: Assess shared variance between variable sets
Display "  Redundancy analysis:"
Display "    Variance in X explained by Y: " joined with String(cca_result.redundancy_analysis["x_explained_by_y"])
Display "    Variance in Y explained by X: " joined with String(cca_result.redundancy_analysis["y_explained_by_x"])
Display "    Total redundancy: " joined with String(cca_result.redundancy_analysis["total_redundancy"])
```

## Multivariate Normality and Testing

### Multivariate Normality Tests
```runa
Note: Test multivariate normal distribution assumption
Let normality_tests be Multivariate.test_multivariate_normality(data_matrix, 0.05)

Display "Multivariate Normality Tests:"
Display "  Mardia's test:"
Display "    Skewness statistic: " joined with String(normality_tests.mardia_skewness["statistic"])
Display "    Skewness p-value: " joined with String(normality_tests.mardia_skewness["p_value"])
Display "    Kurtosis statistic: " joined with String(normality_tests.mardia_kurtosis["statistic"])
Display "    Kurtosis p-value: " joined with String(normality_tests.mardia_kurtosis["p_value"])

Display "  Henze-Zirkler test:"
Display "    HZ statistic: " joined with String(normality_tests.henze_zirkler["statistic"])
Display "    HZ p-value: " joined with String(normality_tests.henze_zirkler["p_value"])

Display "  Royston test:"
Display "    W statistic: " joined with String(normality_tests.royston["statistic"])
Display "    W p-value: " joined with String(normality_tests.royston["p_value"])

Let is_multivariate_normal be normality_tests.overall_conclusion
Display "  Overall conclusion (α=0.05): " joined with String(is_multivariate_normal)
```

### Hotelling's T² Test
```runa
Note: Multivariate one-sample test
Let hypothesized_mean be [2.0, 2.0, 2.5, 2.0, 1.5]
Let hotelling_result be Multivariate.hotelling_t2_one_sample(data_matrix, hypothesized_mean, 0.05)

Display "Hotelling's T² Test (one-sample):"
Display "  Null hypothesis: μ = " joined with String(hypothesized_mean)
Display "  T² statistic: " joined with String(hotelling_result.t2_statistic)
Display "  F statistic: " joined with String(hotelling_result.f_statistic)
Display "  Degrees of freedom: " joined with String(hotelling_result.df1) joined with ", " joined with String(hotelling_result.df2)
Display "  P-value: " joined with String(hotelling_result.p_value)
Display "  Decision: " joined with hotelling_result.test_result joined with " null hypothesis"
```

### MANOVA
```runa
Note: Multivariate analysis of variance
Let group_factor be [0, 0, 0, 1, 1, 1, 1, 2, 2, 2]  Note: Three groups
Let manova_result be Multivariate.manova(data_matrix, group_factor, 0.05)

Display "MANOVA Results:"
Display "  Number of groups: " joined with String(manova_result.n_groups)
Display "  Number of dependent variables: " joined with String(Length(data_matrix[0]))

Display "  Test statistics:"
Display "    Wilks' Lambda: " joined with String(manova_result.wilks_lambda)
Display "    Pillai's Trace: " joined with String(manova_result.pillai_trace)
Display "    Hotelling-Lawley Trace: " joined with String(manova_result.hotelling_lawley_trace)
Display "    Roy's Greatest Root: " joined with String(manova_result.roy_greatest_root)

Display "  F approximations:"
Display "    Wilks' Λ F: " joined with String(manova_result.f_statistics["wilks"]) joined with " (p = " joined with String(manova_result.p_values["wilks"]) joined with ")"
Display "    Pillai's F: " joined with String(manova_result.f_statistics["pillai"]) joined with " (p = " joined with String(manova_result.p_values["pillai"]) joined with ")"

Display "  Overall conclusion: " joined with manova_result.test_result
```

## Distance and Similarity Measures

### Distance Matrices
```runa
Note: Compute various distance measures
Let distance_metrics be ["euclidean", "manhattan", "chebyshev", "mahalanobis"]

Display "Distance Measures Between Observations:"
For Each metric in distance_metrics:
    Let distance_matrix be Multivariate.compute_distance_matrix(data_matrix, metric)
    
    Display "  " joined with metric joined with " distances (first few pairs):"
    For i from 0 to 2:
        For j from i + 1 to 3:
            Display "    Obs" joined with String(i + 1) joined with "-Obs" joined with String(j + 1) joined with ": " joined with String(distance_matrix[i][j])

Note: Mahalanobis distance interpretation
Let mahalanobis_distances be Multivariate.compute_distance_matrix(data_matrix, "mahalanobis")
Display "  Mahalanobis distance statistics:"
Let all_mahal_distances be []
For i from 0 to Length(data_matrix) - 1:
    For j from i + 1 to Length(data_matrix) - 1:
        Call all_mahal_distances.append(mahalanobis_distances[i][j])

Let mean_mahal be DescriptiveStats.calculate_arithmetic_mean(all_mahal_distances, [])
Let std_mahal be DescriptiveStats.calculate_standard_deviation(all_mahal_distances, false)
Display "    Mean distance: " joined with String(mean_mahal)
Display "    Std deviation: " joined with String(std_mahal)
```

## Multidimensional Scaling

### Classical MDS
```runa
Note: Recover coordinate representation from distances
Let mds_result be Multivariate.classical_multidimensional_scaling(data_matrix, 2)

Display "Classical Multidimensional Scaling Results:"
Display "  Original dimensions: " joined with String(Length(data_matrix[0]))
Display "  Reduced dimensions: 2"
Display "  Eigenvalues of coordinate matrix:"
For i from 0 to Length(mds_result.eigenvalues) - 1:
    Display "    Dim " joined with String(i + 1) joined with ": " joined with String(mds_result.eigenvalues[i])

Display "  Proportion of variance explained:"
Let total_eigenvalue_sum be 0.0
For Each eigenvalue in mds_result.eigenvalues:
    Set total_eigenvalue_sum to total_eigenvalue_sum + eigenvalue
    
For i from 0 to 1:  Note: First 2 dimensions
    Let proportion be mds_result.eigenvalues[i] / total_eigenvalue_sum
    Display "    Dim " joined with String(i + 1) joined with ": " joined with String(proportion * 100.0) joined with "%"

Display "  Stress (goodness of fit): " joined with String(mds_result.stress)
```

### Non-metric MDS
```runa
Note: MDS preserving rank order of distances
Let nonmetric_mds_result be Multivariate.nonmetric_multidimensional_scaling(data_matrix, 2, 100)

Display "Non-metric MDS Results:"
Display "  Converged: " joined with String(nonmetric_mds_result.converged)
Display "  Iterations: " joined with String(nonmetric_mds_result.iterations)
Display "  Final stress: " joined with String(nonmetric_mds_result.stress)
Display "  Stress interpretation: "
If nonmetric_mds_result.stress < 0.05:
    Display "    Excellent fit"
Otherwise if nonmetric_mds_result.stress < 0.1:
    Display "    Good fit"
Otherwise if nonmetric_mds_result.stress < 0.2:
    Display "    Fair fit"
Otherwise:
    Display "    Poor fit"
```

## Advanced Multivariate Methods

### Correspondence Analysis
```runa
Note: Analyze categorical data relationships
Let contingency_table be [
    [20, 25, 30],  Note: Cross-tabulation of categorical variables
    [15, 35, 20],
    [30, 20, 25],
    [25, 30, 15]
]

Let ca_result be Multivariate.correspondence_analysis(contingency_table)

Display "Correspondence Analysis Results:"
Display "  Dimensions extracted: " joined with String(ca_result.n_dimensions)
Display "  Total inertia: " joined with String(ca_result.total_inertia)

Display "  Dimension contributions:"
For i from 0 to ca_result.n_dimensions - 1:
    Display "    Dim " joined with String(i + 1) joined with ": " joined with String(ca_result.eigenvalues[i] / ca_result.total_inertia * 100.0) joined with "%"

Display "  Row coordinates:"
For i from 0 to Length(ca_result.row_coordinates) - 1:
    Display "    Row " joined with String(i + 1) joined with ": " joined with String(ca_result.row_coordinates[i])

Display "  Column coordinates:"
For i from 0 to Length(ca_result.column_coordinates) - 1:
    Display "    Col " joined with String(i + 1) joined with ": " joined with String(ca_result.column_coordinates[i])
```

### Independent Component Analysis
```runa
Note: Find statistically independent components
Let ica_config be Dictionary with:
    "n_components": "3"
    "algorithm": "fastICA"
    "max_iterations": "200"
    "tolerance": "1e-4"

Let ica_result be Multivariate.independent_component_analysis(data_matrix, ica_config)

Display "Independent Component Analysis Results:"
Display "  Algorithm: " joined with ica_config["algorithm"]
Display "  Converged: " joined with String(ica_result.converged)
Display "  Iterations: " joined with String(ica_result.iterations)

Display "  Component independence measures:"
For i from 0 to ica_result.n_components - 1:
    Display "    IC" joined with String(i + 1) joined with " kurtosis: " joined with String(ica_result.component_kurtosis[i])
    Display "    IC" joined with String(i + 1) joined with " negentropy: " joined with String(ica_result.component_negentropy[i])

Note: Compare ICA vs PCA
Display "  ICA vs PCA comparison:"
Display "    ICA finds independent sources"
Display "    PCA finds uncorrelated components"
Display "    ICA components may have non-Gaussian distributions"
```

## Error Handling and Validation

### Comprehensive Error Management
```runa
Note: Handle multivariate analysis errors
Try:
    Let insufficient_data be [[1.0, 2.0], [3.0, 4.0]]  Note: Only 2 observations
    Let failed_pca be Multivariate.principal_component_analysis(insufficient_data, true, 2)
Catch Errors.InsufficientData as error:
    Display "Sample size error: " joined with error.message
    Display "Need more observations than variables for reliable analysis"

Try:
    Let singular_data be [[1.0, 2.0], [1.0, 2.0], [1.0, 2.0]]  Note: No variance
    Let failed_analysis be Multivariate.principal_component_analysis(singular_data, true, 1)
Catch Errors.SingularMatrix as error:
    Display "Singularity error: " joined with error.message
    Display "Check for constant variables or perfect multicollinearity"

Try:
    Let invalid_clusters be Multivariate.k_means_clustering(data_matrix, 50, 100, 42)  Note: k > n
Catch Errors.InvalidParameter as error:
    Display "Parameter error: " joined with error.message
    Display "Number of clusters cannot exceed number of observations"
```

### Model Validation Framework
```runa
Process called "validate_multivariate_analysis" that takes data as List[List[Float]], analysis_type as String returns Dictionary[String, String]:
    Let validation_results be Dictionary[String, String]
    
    Note: Basic data validation
    Let n_obs be data.size()
    Let n_vars be data[0].size()
    Set validation_results["sample_size"] to String(n_obs)
    Set validation_results["variables"] to String(n_vars)
    
    Note: Check sample size adequacy
    Let min_sample_ratio be 5.0  Note: 5:1 obs-to-variables ratio
    Let adequate_sample be Float(n_obs) >= (Float(n_vars) * min_sample_ratio)
    Set validation_results["adequate_sample"] to String(adequate_sample)
    
    Note: Check for missing values
    Let has_missing be check_missing_values(data)
    Set validation_results["no_missing"] to String(not has_missing)
    
    Note: Test multivariate assumptions if needed
    If analysis_type == "pca" or analysis_type == "factor_analysis":
        Let normality_check be Multivariate.test_multivariate_normality(data, 0.05)
        Set validation_results["multivariate_normal"] to String(normality_check.overall_conclusion)
        
        Note: Check sampling adequacy for factor analysis
        If analysis_type == "factor_analysis":
            Let kmo_result be Multivariate.kaiser_meyer_olkin_test(data)
            Set validation_results["kmo_adequate"] to String(kmo_result.overall_kmo > 0.5)
            Set validation_results["kmo_value"] to String(kmo_result.overall_kmo)
    
    Note: Generate recommendations
    Let recommendations be []
    If not adequate_sample:
        Call recommendations.append("Increase sample size (min 5:1 ratio)")
    If has_missing:
        Call recommendations.append("Address missing values before analysis")
    If analysis_type == "factor_analysis" and Float(validation_results["kmo_value"]) < 0.6:
        Call recommendations.append("Consider data suitability for factor analysis")
    
    Set validation_results["recommendations"] to String(recommendations)
    Set validation_results["validation_complete"] to "true"
    
    Return validation_results

Note: Example validation
Let validation_results be validate_multivariate_analysis(data_matrix, "pca")
Display "Multivariate Analysis Validation:"
For Each key, value in validation_results:
    Display "  " joined with key joined with ": " joined with value
```

The multivariate statistics module provides comprehensive tools for analyzing complex multi-dimensional data relationships, from dimensionality reduction to clustering and classification. Its integration with validation procedures and diagnostic tools ensures reliable and interpretable multivariate analyses for research and data science applications.