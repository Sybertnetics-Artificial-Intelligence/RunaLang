Note: Math Core Comparison Module

## Overview

The `math/core/comparison` module provides comprehensive mathematical comparison and ordering operations. It handles numerical comparisons with tolerance support, sorting algorithms, ranking systems, and statistical comparison methods for robust mathematical analysis.

## Key Features

- **Tolerance-Based Comparisons**: Handle floating-point precision issues
- **Multi-Value Operations**: Find min/max, nth smallest/largest elements
- **Sorting Algorithms**: Stable sorting with custom comparators
- **Ranking Systems**: Multiple ranking methods (standard, modified, dense)
- **Statistical Comparisons**: Distribution and variance testing
- **Fuzzy Logic**: Approximate and uncertainty-based comparisons
- **Performance Optimization**: Vectorized and parallel operations

## Data Types

### ComparisonResult
Represents the result of a comparison operation:
```runa
Type called "ComparisonResult":
    comparison_type as String      Note: Type of comparison performed
    operand_a as String           Note: First operand
    operand_b as String           Note: Second operand
    result as Boolean             Note: Comparison result
    confidence_level as Float     Note: Confidence in result
    tolerance_used as Float       Note: Tolerance applied
    comparison_method as String   Note: Method used
```

### OrderingResult
Contains sorting and ordering information:
```runa
Type called "OrderingResult":
    original_indices as List[Integer]  Note: Original position mapping
    sorted_values as List[String]      Note: Sorted values
    ordering_criteria as String        Note: Sort criteria used
    stability_preserved as Boolean     Note: Whether sort was stable
    comparison_count as Integer        Note: Number of comparisons made
```

### ToleranceConfiguration
Defines comparison tolerance settings:
```runa
Type called "ToleranceConfiguration":
    absolute_tolerance as String       Note: Absolute tolerance value
    relative_tolerance as String       Note: Relative tolerance percentage
    comparison_method as String        Note: Tolerance method
    significant_figures as Integer     Note: Significant figures to consider
```

## Basic Comparisons

### Simple Comparisons
```runa
Note: Basic numerical comparisons
Let a be "3.14159"
Let b be "3.14160"
Let precision be 10

Let is_less be Comparison.less_than(a, b, precision)
Let is_greater be Comparison.greater_than(a, b, precision)

Display "3.14159 < 3.14160: " joined with String(is_less)
Display "3.14159 > 3.14160: " joined with String(is_greater)
```

### Min/Max Operations
```runa
Note: Find minimum and maximum
Let min_val be Comparison.minimum("5.7", "3.2", 10)
Let max_val be Comparison.maximum("5.7", "3.2", 10)

Display "Minimum: " joined with min_val  Note: "3.2"
Display "Maximum: " joined with max_val  Note: "5.7"
```

### Tolerance-Based Equality
```runa
Note: Configure tolerance for floating-point comparisons
Let tolerance_config be ToleranceConfiguration with:
    absolute_tolerance: "0.001"
    relative_tolerance: "0.01"
    comparison_method: "combined"
    significant_figures: 6

Let equality_result be Comparison.equal_within_tolerance("3.14159", "3.14160", tolerance_config)
Display "Equal within tolerance: " joined with String(equality_result.result)
Display "Confidence: " joined with String(equality_result.confidence_level)
```

## Multi-Value Operations

### Array Min/Max
```runa
Note: Find minimum/maximum in arrays
Let values be ["5.2", "3.1", "7.8", "2.4", "6.9"]
Let options be Dictionary with: "precision": "10"

Let array_min be Comparison.minimum_of_array(values, options)
Let array_max be Comparison.maximum_of_array(values, options)

Display "Array minimum: " joined with array_min  Note: "2.4"
Display "Array maximum: " joined with array_max  Note: "7.8"

Note: Get both min and max in single pass
Let min_max_pair be Comparison.minimum_maximum_pair(values)
Display "Min: " joined with min_max_pair["minimum"]
Display "Max: " joined with min_max_pair["maximum"]
```

### Nth Smallest/Largest
```runa
Note: Find nth smallest/largest elements
Let data be ["10", "5", "8", "3", "7", "1", "9"]

Let third_smallest be Comparison.nth_smallest(data, 3, "quickselect")
Let second_largest be Comparison.nth_largest(data, 2, "quickselect")

Display "3rd smallest: " joined with third_smallest  Note: "5"
Display "2nd largest: " joined with second_largest   Note: "9"
```

## Sorting Operations

### Basic Sorting
```runa
Note: Ascending sort
Let numbers be ["3.7", "1.2", "5.9", "2.1", "4.8"]
Let sort_options be Dictionary with: "stable": "true"

Let ascending_result be Comparison.sort_ascending(numbers, sort_options)
Display "Sorted ascending:"
For Each value in ascending_result.sorted_values:
    Display "  " joined with value

Note: Descending sort
Let descending_result be Comparison.sort_descending(numbers, sort_options)
Display "Sorted descending:"
For Each value in descending_result.sorted_values:
    Display "  " joined with value
```

### Custom Comparator Sorting
```runa
Note: Sort by string length
Let words be ["elephant", "cat", "butterfly", "dog", "ant"]
Let length_sorted be Comparison.sort_by_custom_comparator(words, "length", sort_options)

Display "Sorted by length:"
For Each word in length_sorted.sorted_values:
    Display "  " joined with word joined with " (length: " joined with String(Length(word)) joined with ")"))

Note: Alphabetical sorting
Let alpha_sorted be Comparison.sort_by_custom_comparator(words, "alphabetical", sort_options)
```

### Multi-Key Sorting
```runa
Note: Sort records by multiple keys
Let records be [
    Dictionary with: "name": "Alice", "age": "30", "salary": "50000",
    Dictionary with: "name": "Bob", "age": "25", "salary": "45000",
    Dictionary with: "name": "Charlie", "age": "30", "salary": "55000"
]

Let sort_keys be [
    Dictionary with: "key": "age", "direction": "ascending", "type": "numerical",
    Dictionary with: "key": "salary", "direction": "descending", "type": "numerical"
]

Let multi_sorted be Comparison.multi_key_sort(records, sort_keys)
```

### Partial Sorting
```runa
Note: Get top k elements without fully sorting
Let large_dataset be ["9", "3", "7", "1", "8", "5", "2", "6", "4"]
Let top_3 be Comparison.partial_sort(large_dataset, 3, "ascending")

Display "Top 3 smallest:"
For Each value in top_3:
    Display "  " joined with value
```

## Ranking Operations

### Value Ranking
```runa
Note: Rank values using different methods
Let scores be ["85", "92", "78", "92", "88", "95"]

Note: Standard ranking (1, 2, 2, 4, 5, 6)
Let standard_ranks be Comparison.rank_values(scores, "standard")

Note: Dense ranking (1, 2, 2, 3, 4, 5)
Let dense_ranks be Comparison.rank_values(scores, "dense")

Display "Standard ranking:"
For Each ranking in standard_ranks:
    Display "  Value: " joined with ranking.value joined with " Rank: " joined with String(ranking.rank)

Display "Dense ranking:"
For Each ranking in dense_ranks:
    Display "  Value: " joined with ranking.value joined with " Rank: " joined with String(ranking.rank)
    Display "    Percentile: " joined with String(ranking.percentile joined with "%"))
```

## Sign and Classification

### Number Classification
```runa
Note: Classify number properties
Let number be "42.0"
Let classification_criteria be Dictionary with: "tolerance": "0.001"

Let classification be Comparison.classify_number(number, classification_criteria)
Display "Number: " joined with number
Display "Positive: " joined with String(classification["positive"])
Display "Integer: " joined with String(classification["integer"])
Display "Even: " joined with String(classification["even"])
Display "Finite: " joined with String(classification["finite"])
```

### Sign Detection
```runa
Note: Sign operations
Let positive_num be "3.14"
Let negative_num be "-2.71"
Let zero_num be "0.000001"

Display "Sign of " joined with positive_num joined with ": " joined with String(Comparison.sign_function(positive_num))   Note: 1
Display "Sign of " joined with negative_num joined with ": " joined with String(Comparison.sign_function(negative_num))   Note: -1

Note: Zero detection with tolerance
Let tolerance_config be ToleranceConfiguration with:
    absolute_tolerance: "0.0001"
    relative_tolerance: "0.001"
    comparison_method: "absolute"

Let is_zero be Comparison.is_zero(zero_num, tolerance_config)
Display zero_num joined with " is zero (±0.0001: " joined with String(is_zero))
```

## Rounding and Precision

### Rounding Operations
```runa
Note: Various rounding modes
Let value be "3.14159"

Let half_up be Comparison.round_to_nearest(value, 2, "half-up")        Note: "3.14"
Let half_even be Comparison.round_to_nearest(value, 2, "half-even")    Note: "3.14"
Let toward_zero be Comparison.round_to_nearest(value, 2, "toward-zero") # "3.14"

Display "Half-up: " joined with half_up
Display "Half-even (banker's: " joined with half_even)
Display "Toward zero: " joined with toward_zero
```

### Floor and Ceiling
```runa
Note: Floor and ceiling operations
Let number be "3.7"

Let floor_val be Comparison.floor_function(number, 0)    Note: "3"
Let ceiling_val be Comparison.ceiling_function(number, 0) # "4"

Display "Floor of " joined with number joined with ": " joined with floor_val
Display "Ceiling of " joined with number joined with ": " joined with ceiling_val
```

### Significant Figures
```runa
Note: Round to significant figures
Let scientific_value be "123456.789"

Let sig_fig_3 be Comparison.round_to_significant_figures(scientific_value, 3)  Note: "123000"
Let sig_fig_5 be Comparison.round_to_significant_figures(scientific_value, 5)  Note: "123460"

Display "3 significant figures: " joined with sig_fig_3
Display "5 significant figures: " joined with sig_fig_5
```

## Range Operations

### Clamping
```runa
Note: Clamp values to range
Let value be "15"
Let clamped be Comparison.clamp_to_range(value, "5", "10")  Note: "10"
Display "15 clamped to [5, 10]: " joined with clamped

Note: Complex clamping with soft boundaries
Let bounds be Dictionary with:
    "minimum": "0"
    "maximum": "100"
    "softness": "0.1"

Let soft_clamped be Comparison.clamp_to_bounds("110", bounds, "soft")
```

### Range Validation
```runa
Note: Check if value is in range
Let test_value be "7.5"
Let inclusive_bounds be Dictionary with:
    "start": True
    "end": True

Let in_range be Comparison.is_in_range(test_value, "5.0", "10.0", inclusive_bounds)
Display test_value joined with " in [5.0, 10.0]: " joined with String(in_range)
```

### Wrapping
```runa
Note: Wrap values to range using modular arithmetic
Let angle be "450"  Note: degrees
Let wrapped_angle be Comparison.wrap_to_range(angle, "0", "360")
Display "450° wrapped to [0°, 360°: " joined with wrapped_angle joined with "°")  Note: "90°"
```

## Statistical Order Operations

### Percentiles and Quantiles
```runa
Note: Compute percentiles
Let dataset be ["1", "3", "5", "7", "9", "11", "13", "15", "17", "19"]

Let percentile_25 be Comparison.percentile(dataset, 25.0, "linear")
Let percentile_50 be Comparison.percentile(dataset, 50.0, "linear")  Note: median
Let percentile_75 be Comparison.percentile(dataset, 75.0, "linear")

Display "25th percentile: " joined with percentile_25
Display "50th percentile (median: " joined with percentile_50)
Display "75th percentile: " joined with percentile_75

Note: Compute quartiles
Let quartiles be Comparison.quartiles(dataset)
Display "Q1: " joined with quartiles["Q1"]
Display "Q2: " joined with quartiles["Q2"]
Display "Q3: " joined with quartiles["Q3"]

Note: Interquartile range
Let iqr be Comparison.interquartile_range(dataset)
Display "IQR: " joined with iqr
```

### Median with Different Methods
```runa
Note: Median computation for even-length arrays
Let even_data be ["2", "4", "6", "8"]
Let median_val be Comparison.median(even_data, "linear")
Display "Median of even dataset: " joined with median_val  Note: "5"
```

## Interval Operations

### Interval Comparisons
```runa
Note: Compare intervals
Let interval_a be Dictionary with: "start": "1", "end": "5"
Let interval_b be Dictionary with: "start": "3", "end": "7"

Let relationship be Comparison.compare_intervals(interval_a, interval_b)
Display "Interval relationship: " joined with relationship  Note: "overlapping"
```

### Interval Arithmetic
```runa
Note: Find intersection of ranges
Let ranges be [
    Dictionary with: "start": "2", "end": "8",
    Dictionary with: "start": "5", "end": "12",
    Dictionary with: "start": "3", "end": "10"
]

Let intersection be Comparison.range_intersection(ranges)
If intersection["empty"] equals "false":
    Display "Intersection: [" joined with intersection["start"] joined with ", " joined with intersection["end"] joined with "]"
Otherwise:
    Display "No intersection found"

Note: Find union of ranges
Let union_ranges be Comparison.range_union(ranges)
Display "Union results in " joined with String(Length(union_ranges) joined with " range(s):"))
For Each range in union_ranges:
    Display "  [" joined with range["start"] joined with ", " joined with range["end"] joined with "]"
```

## Fuzzy and Approximate Comparisons

### Fuzzy Equality
```runa
Note: Fuzzy comparison with membership values
Let val1 be "3.14"
Let val2 be "3.15"
Let fuzziness be 0.1

Let membership be Comparison.fuzzy_equal(val1, val2, fuzziness)
Display "Fuzzy equality membership: " joined with String(membership)  Note: 0.9
```

### Uncertainty-Based Comparisons
```runa
Note: Compare with uncertainty bounds
Let approximation_bounds be Dictionary with:
    "uncertainty_a": "0.01"
    "uncertainty_b": "0.02"
    "confidence_level": "0.95"

Let approx_result be Comparison.approximate_compare("5.67", "5.69", approximation_bounds)
Display "Approximately equal: " joined with String(approx_result.result)
Display "Confidence: " joined with String(approx_result.confidence_level)
```

### Robust Comparisons
```runa
Note: Account for measurement noise
Let noise_model be Dictionary with:
    "noise_type": "gaussian"
    "noise_level": "0.05"
    "sigma": "0.02"

Let robust_result be Comparison.robust_comparison("10.0", "10.03", noise_model)
Display "Robust equality: " joined with String(robust_result.result)
```

## Statistical Comparisons

### Distribution Comparison
```runa
Note: Compare two data distributions
Let sample_a be ["5.1", "4.9", "5.3", "4.8", "5.0"]
Let sample_b be ["6.2", "5.8", "6.1", "6.0", "5.9"]

Let stat_comparison be Comparison.compare_distributions(sample_a, sample_b, "t-test")
Display "Test statistic: " joined with stat_comparison.comparison_statistic
Display "P-value: " joined with String(stat_comparison.p_value)
Display "Effect size: " joined with String(stat_comparison.effect_size)
```

### Variance Testing
```runa
Note: Compare variances between samples
Let variance_test be Comparison.compare_variances(sample_a, sample_b, "f-test")
Display "F-statistic: " joined with variance_test.comparison_statistic
Display "Test method: " joined with variance_test.test_method
```

## Performance Optimization

### Vectorized Operations
```runa
Note: Element-wise comparisons on arrays
Let array_a be ["1", "3", "5", "7", "9"]
Let array_b be ["2", "3", "4", "7", "8"]

Let comparison_results be Comparison.vectorized_comparison(array_a, array_b, "less_than")
Display "Element-wise less than results:"
For i from 0 to Length(comparison_results) - 1:
    Display "  " joined with array_a[i] joined with " < " joined with array_b[i] joined with ": " joined with String(comparison_results[i])
```

### Parallel Sorting
```runa
Note: Sort large arrays using parallel processing
Let large_array be generate_large_dataset(10000)
Let parallel_options be Dictionary with:
    "thread_count": "4"
    "direction": "ascending"

Let parallel_result be Comparison.parallel_sort(large_array, parallel_options)
Display "Parallel sort completed:"
Display "Algorithm: " joined with parallel_result.sorting_algorithm
Display "Comparisons: " joined with String(parallel_result.comparison_count)
```

## Lexicographic Ordering

### Sequence Comparison
```runa
Note: Compare sequences lexicographically
Let sequence_a be ["apple", "banana", "cherry"]
Let sequence_b be ["apple", "blueberry", "cherry"]

Let lex_result be Comparison.lexicographic_compare(sequence_a, sequence_b, "alphabetical")
Display "Lexicographic comparison: " joined with String(lex_result)  Note: -1 (a < b)
```

### Custom Priority Ordering
```runa
Note: Custom ordering with priority rules
Let ordering_rules be Dictionary with:
    "type": "custom_priority"
    "high": "1"
    "medium": "2"
    "low": "3"
    "reverse": "false"

Let priority_result be Comparison.custom_ordering_compare("medium", "high", ordering_rules)
Display "Priority comparison: " joined with String(priority_result)  Note: 1 (medium > high in priority)
```

## Error Handling

The comparison module provides comprehensive error handling:

```runa
Try:
    Let invalid_array be []
    Let min_empty be Comparison.minimum_of_array(invalid_array, Dictionary with: "precision": "10")
Catch Errors.InvalidOperation as error:
    Display "Error: " joined with error.message
    Let suggestion be SuggestionEngine.get_suggestion(error)
    Display "Suggestion: " joined with suggestion
```

## Performance Considerations

- **Tolerance Settings**: Use appropriate tolerance for floating-point comparisons
- **Algorithm Selection**: Choose optimal sorting algorithms for data size
- **Vectorization**: Use vectorized operations for large datasets
- **Parallel Processing**: Leverage parallel sorting for very large arrays

## Best Practices

1. **Always Use Tolerance**: For floating-point comparisons, always specify appropriate tolerance
2. **Stable Sorting**: Use stable sorting when order of equal elements matters
3. **Choose Right Algorithm**: Select appropriate algorithms based on data characteristics
4. **Handle Edge Cases**: Test with empty arrays, single elements, and identical values
5. **Performance Testing**: Benchmark operations with representative data sizes