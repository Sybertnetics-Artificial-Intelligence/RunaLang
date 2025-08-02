# Data Science Module

The Runa Data Science module provides a comprehensive ecosystem for data analysis, manipulation, visualization, and processing pipelines. It offers a complete alternative to Python's data science stack while maintaining Runa's natural language syntax and type safety.

## Overview

The data science module consists of five integrated components:

- **DataFrames** - Core tabular data structures and operations
- **Statistical Analysis** - Comprehensive statistical analysis and hypothesis testing
- **Pandas Compatibility** - Seamless pandas API compatibility layer
- **Data Processing Pipelines** - Enterprise-grade workflow orchestration
- **Data Visualization** - Publication-quality plotting and charting

## Quick Start

```runa
Import "data_science/dataframes" as df
Import "data_science/analysis" as stats
Import "data_science/visualization" as viz

Note: Create a DataFrame from dictionary data
Let sales_data be Dictionary with:
    "product" as list containing "Widget A", "Widget B", "Widget C"
    "revenue" as list containing 15000.0, 23000.0, 18500.0
    "units_sold" as list containing 150, 230, 185

Let df_result be df.create_dataframe with data as sales_data
Match df_result:
    When df.DataFrameSuccess with data as sales_df:
        Note: Perform statistical analysis
        Let revenue_stats be stats.calculate_descriptive_statistics with 
            data as df.get_dataframe_column_values with df as sales_df and column as "revenue"
        
        Note: Create visualization
        Let chart_result be viz.create_bar_plot with 
            categories as df.get_dataframe_column_values with df as sales_df and column as "product"
            and values as df.get_dataframe_column_values with df as sales_df and column as "revenue"
        
        Display "Sales analysis completed successfully"
```

## Module Components

### DataFrames (`data_science/dataframes`)

The DataFrame module provides the foundational data structure for tabular data manipulation.

#### Core Data Types

```runa
Type DataFrame is Dictionary with:
    columns as List[String]
    index as List[Any]
    data as Dictionary[String, List[Any]]
    metadata as Dictionary[String, Any]

Type DataFrameResult is Union with:
    DataFrameSuccess with data as DataFrame
    DataFrameError with error as DataFrameErrorInfo
```

#### DataFrame Creation

```runa
Note: Create DataFrame from dictionary
Let student_data be Dictionary with:
    "name" as list containing "Alice", "Bob", "Charlie"
    "age" as list containing 20, 21, 19
    "gpa" as list containing 3.8, 3.2, 3.9

Let df_result be df.create_dataframe with 
    data as student_data 
    and columns as None 
    and index as None

Note: Create DataFrame from CSV string
Let csv_content be "name,score,grade\nAlice,95,A\nBob,87,B\nCharlie,92,A"
Let csv_df_result be df.read_dataframe_from_csv_string with csv_string as csv_content

Note: Create empty DataFrame with specified structure
Let empty_df be df.create_empty_dataframe with 
    columns as list containing "id", "value", "category"
    and index as None
```

#### DataFrame Operations

```runa
Note: Column selection and filtering
Let selected_columns be df.select_dataframe_columns with 
    df as student_df 
    and columns as list containing "name", "gpa"

Note: Row filtering
Let high_performers be df.filter_dataframe_rows with 
    df as student_df 
    and condition as "gpa > 3.5"

Note: Sorting
Let sorted_df be df.sort_dataframe with 
    df as student_df 
    and column as "gpa" 
    and ascending as false

Note: Statistical operations
Let df_stats be df.calculate_dataframe_statistics with df as student_df
Match df_stats:
    When df.StatisticsSuccess with data as stats_result:
        Display "Mean GPA: " with message stats_result["mean"]["gpa"]
        Display "Standard deviation: " with message stats_result["std"]["gpa"]
```

#### Data I/O Operations

```runa
Note: Export to CSV
Let csv_export_result be df.write_dataframe_to_csv_string with df as student_df
Let json_export_result be df.write_dataframe_to_json_string with df as student_df

Note: Import from various formats
Let parquet_df be df.read_dataframe_from_parquet_file with file_path as "data.parquet"
Let excel_df be df.read_dataframe_from_excel_file with file_path as "data.xlsx" and sheet_name as "Sheet1"
```

### Statistical Analysis (`data_science/analysis`)

Comprehensive statistical analysis capabilities including descriptive statistics, hypothesis testing, correlation analysis, and regression modeling.

#### Descriptive Statistics

```runa
Note: Calculate comprehensive descriptive statistics
Let data_sample be list containing 12.5, 15.3, 18.7, 14.2, 16.8, 13.9, 17.4, 15.1, 16.3, 14.7

Let stats_result be stats.calculate_descriptive_statistics with data as data_sample
Match stats_result:
    When stats.AnalysisSuccess with data as descriptive_stats:
        Display "Mean: " with message descriptive_stats["mean"]
        Display "Median: " with message descriptive_stats["median"]
        Display "Standard Deviation: " with message descriptive_stats["std"]
        Display "Quartiles: " with message descriptive_stats["quartiles"]
        Display "Skewness: " with message descriptive_stats["skewness"]
        Display "Kurtosis: " with message descriptive_stats["kurtosis"]
```

#### Correlation Analysis

```runa
Note: Calculate correlation between variables
Let x_values be list containing 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0
Let y_values be list containing 2.1, 3.8, 6.2, 7.9, 9.8, 12.1, 13.9, 16.2, 17.8, 20.1

Let correlation_result be stats.calculate_correlation with 
    x_data as x_values 
    and y_data as y_values 
    and method as "pearson"

Match correlation_result:
    When stats.AnalysisSuccess with data as correlation_data:
        Display "Correlation coefficient: " with message correlation_data["correlation"]
        Display "P-value: " with message correlation_data["p_value"]
        Display "95% Confidence interval: " with message correlation_data["confidence_interval"]

Note: Multi-variable correlation matrix
Let variables be Dictionary with:
    "height" as list containing 165, 170, 175, 180, 185
    "weight" as list containing 60, 70, 75, 85, 95
    "age" as list containing 25, 30, 35, 40, 45

Let correlation_matrix_result be stats.correlation_analysis with 
    variables as variables 
    and variable_names as list containing "height", "weight", "age"
    and method as "pearson"
```

#### Hypothesis Testing

```runa
Note: One-sample t-test
Let sample_data be list containing 98.2, 99.1, 98.8, 99.5, 98.9, 99.2, 98.7, 99.0, 98.6, 99.3
Let population_mean be 98.6
Let alpha_level be 0.05

Let ttest_result be stats.one_sample_t_test with 
    sample as sample_data 
    and population_mean as population_mean 
    and alpha as alpha_level

Match ttest_result:
    When stats.StatisticalResult with data as test_results:
        Display "T-statistic: " with message test_results["t_statistic"]
        Display "P-value: " with message test_results["p_value"]
        Display "Significant: " with message test_results["is_significant"]

Note: Two-sample t-test
Let group_a be list containing 23.1, 24.2, 22.8, 23.9, 24.1
Let group_b be list containing 25.3, 26.1, 25.8, 26.0, 25.5

Let two_sample_result be stats.two_sample_t_test with 
    sample1 as group_a 
    and sample2 as group_b 
    and alpha as 0.05

Note: Chi-square test
Let observed_frequencies be list containing list containing 20, 30, 25, 15
Let expected_frequencies be list containing list containing 22.5, 27.5, 25.0, 17.5

Let chi_square_result be stats.chi_square_test with 
    observed as observed_frequencies 
    and expected as expected_frequencies 
    and alpha as 0.05
```

#### Regression Analysis

```runa
Note: Linear regression
Let x_predictor be list containing 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0
Let y_response be list containing 3.2, 5.1, 7.3, 9.0, 11.2, 13.1, 14.8, 17.2, 18.9, 21.1

Let regression_result be stats.linear_regression with 
    x_data as x_predictor 
    and y_data as y_response

Match regression_result:
    When stats.AnalysisSuccess with data as regression_data:
        Display "Slope: " with message regression_data["slope"]
        Display "Intercept: " with message regression_data["intercept"]
        Display "R-squared: " with message regression_data["r_squared"]
        Display "P-value: " with message regression_data["p_value"]
        Display "Confidence intervals: " with message regression_data["confidence_intervals"]

Note: Multiple regression
Let predictors be Dictionary with:
    "x1" as list containing 1.0, 2.0, 3.0, 4.0, 5.0
    "x2" as list containing 2.5, 3.2, 4.1, 4.8, 5.5
    "x3" as list containing 0.5, 1.2, 1.8, 2.3, 2.9

Let response_var be list containing 12.3, 18.7, 25.2, 31.8, 38.4

Let multiple_regression_result be stats.multiple_regression with 
    predictors as predictors 
    and response as response_var
```

### Pandas Compatibility (`data_science/pandas_compat`)

Seamless compatibility layer enabling pandas code migration to Runa.

#### DataFrame API Compatibility

```runa
Import "data_science/pandas_compat" as pd

Note: Create pandas-compatible DataFrame
Let data be Dictionary with:
    "A" as list containing 1, 2, 3, 4, 5
    "B" as list containing 10, 20, 30, 40, 50
    "C" as list containing 100, 200, 300, 400, 500

Let pandas_df be pd.DataFrame with 
    data as Some with value as data 
    and index as None 
    and columns as None 
    and dtype as None

Note: Method chaining (pandas-style)
Let processed_df be pandas_df.head with n as Some with value as 3
Set processed_df to processed_df.describe
Set processed_df to processed_df.sort_values with by as "A" and ascending as Some with value as false

Note: Statistical operations
Let summary_stats be pandas_df.describe
Let column_means be pandas_df.mean
Let correlation_matrix be pandas_df.corr with method as Some with value as "pearson"

Note: Data selection and filtering
Let column_subset be pandas_df.select_columns with columns as list containing "A", "C"
Let filtered_data be pandas_df.query with expression as "A > 2"
Let top_rows be pandas_df.head with n as Some with value as 10
```

#### Pandas Function Compatibility

```runa
Note: Data manipulation functions
Let merged_df be pd.merge with 
    left as df1 
    and right as df2 
    and on as Some with value as "id" 
    and how as Some with value as "inner"

Let concatenated_df be pd.concat with 
    objs as list containing df1, df2, df3 
    and axis as Some with value as 0 
    and ignore_index as Some with value as true

Let pivot_table be pd.pivot_table with 
    df as sales_data 
    and values as Some with value as "revenue" 
    and index as Some with value as "product" 
    and columns as Some with value as "quarter"

Note: Data I/O functions
Let csv_df be pd.read_csv with file_path as "data.csv" and sep as Some with value as ","
Let saved_result be pd.to_csv with df as processed_df and file_path as "output.csv"
```

### Data Processing Pipelines (`data_science/pipelines`)

Enterprise-grade data processing pipeline framework with DAG execution, dependency resolution, and comprehensive monitoring.

#### Pipeline Configuration

```runa
Import "data_science/pipelines" as pipelines

Note: Create pipeline configuration
Let pipeline_config be pipelines.PipelineConfiguration with:
    pipeline_id as "data_processing_pipeline"
    name as "Customer Data Processing Pipeline"
    description as Some with value as "ETL pipeline for customer analytics"
    timeout_seconds as 300
    retry_policy as pipelines.RetryPolicy with:
        max_retries as 3
        retry_delay_ms as 5000
        exponential_backoff as true
    resource_limits as Dictionary with:
        "memory_mb" as 1024
        "cpu_cores" as 2

Let pipeline_result be pipelines.create_pipeline with config as pipeline_config
```

#### Pipeline Node Definition

```runa
Note: Data source node
Let data_source_config be pipelines.NodeConfiguration with:
    node_id as "customer_data_source"
    name as "Customer Data Source"
    operation_type as "data_source"
    parameters as Dictionary with:
        "source_type" as "database"
        "connection_string" as "postgresql://localhost/customers"
        "query" as "SELECT * FROM customers WHERE created_date >= '2023-01-01'"
    timeout_seconds as 60
    dependencies as empty list

Note: Data transformation node
Let transform_config be pipelines.NodeConfiguration with:
    node_id as "data_cleaner"
    name as "Data Cleaning and Transformation"
    operation_type as "transform"
    parameters as Dictionary with:
        "transformations" as list containing "remove_duplicates", "fill_missing_values", "normalize_names"
        "missing_value_strategy" as "forward_fill"
    timeout_seconds as 120
    dependencies as list containing "customer_data_source"

Note: Analysis node
Let analysis_config be pipelines.NodeConfiguration with:
    node_id as "customer_analytics"
    name as "Customer Analytics"
    operation_type as "analysis"
    parameters as Dictionary with:
        "metrics" as list containing "customer_lifetime_value", "churn_probability", "segment_classification"
        "model_type" as "ensemble"
    timeout_seconds as 180
    dependencies as list containing "data_cleaner"

Note: Output node
Let output_config be pipelines.NodeConfiguration with:
    node_id as "results_export"
    name as "Export Results"
    operation_type as "data_sink"
    parameters as Dictionary with:
        "output_format" as "parquet"
        "destination" as "s3://analytics-bucket/customer-insights/"
        "partitioning" as list containing "year", "month"
    timeout_seconds as 90
    dependencies as list containing "customer_analytics"
```

#### Pipeline Execution

```runa
Note: Add nodes to pipeline
Let add_source_result be pipelines.add_pipeline_node with pipeline as customer_pipeline and node_config as data_source_config
Let add_transform_result be pipelines.add_pipeline_node with pipeline as customer_pipeline and node_config as transform_config
Let add_analysis_result be pipelines.add_pipeline_node with pipeline as customer_pipeline and node_config as analysis_config
Let add_output_result be pipelines.add_pipeline_node with pipeline as customer_pipeline and node_config as output_config

Note: Validate pipeline dependencies
Let validation_result be pipelines.validate_pipeline_dependencies with pipeline as customer_pipeline
If not validation_result["is_valid"] as Boolean:
    Display "Pipeline validation failed: " with message validation_result["error_message"]
    Return

Note: Execute pipeline
Let execution_context be Dictionary with:
    "run_id" as "customer_pipeline_2023_12_01"
    "environment" as "production"
    "notification_email" as "data-team@company.com"

Let execution_result be pipelines.execute_pipeline with 
    pipeline as customer_pipeline 
    and execution_context as Some with value as execution_context

Match execution_result:
    When pipelines.PipelineSuccess with data as pipeline_results and metadata as execution_metadata:
        Display "Pipeline executed successfully"
        Display "Execution time: " with message execution_metadata["total_execution_time_ms"]
        Display "Nodes completed: " with message execution_metadata["successful_nodes"]
        
        For each node_id, result in pipeline_results:
            Display "Node " with message node_id with message " completed with " with message result["output_records"] with message " records"
    
    When pipelines.PipelineError with error as pipeline_error and partial_results as partial_data:
        Display "Pipeline failed: " with message pipeline_error.message
        Display "Failed at node: " with message pipeline_error.node_id
        Display "Partial results available for " with message length of partial_data with message " nodes"
```

#### Pipeline Monitoring

```runa
Note: Monitor pipeline execution
Let monitoring_result be pipelines.get_pipeline_status with pipeline_id as "data_processing_pipeline"
Match monitoring_result:
    When pipelines.StatusSuccess with data as status_info:
        Display "Pipeline status: " with message status_info["current_status"]
        Display "Current node: " with message status_info["current_node"]
        Display "Progress: " with message status_info["completion_percentage"] with message "%"
        Display "Estimated completion: " with message status_info["estimated_completion_time"]

Note: Get execution history
Let history_result be pipelines.get_pipeline_execution_history with 
    pipeline_id as "data_processing_pipeline" 
    and limit as 10

Match history_result:
    When pipelines.HistorySuccess with data as executions:
        For each execution in executions:
            Display "Execution " with message execution["run_id"] with message ": " with message execution["status"]
            Display "  Duration: " with message execution["duration_ms"] with message "ms"
            Display "  Records processed: " with message execution["total_records"]
```

### Data Visualization (`data_science/visualization`)

Publication-quality data visualization with interactive features, multiple backends, and comprehensive chart types.

#### Basic Plotting

```runa
Import "data_science/visualization" as viz

Note: Line plot
Let x_data be list containing 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
Let y_data be list containing 2, 4, 7, 8, 12, 15, 18, 22, 25, 30

Let line_plot_result be viz.create_line_plot with 
    x_data as x_data 
    and y_data as y_data 
    and config as None

Note: Scatter plot with customization
Let scatter_x be list containing 1.2, 2.5, 3.1, 4.8, 5.3, 6.7, 7.2, 8.9, 9.1, 10.4
Let scatter_y be list containing 3.1, 5.8, 6.2, 9.1, 10.5, 12.8, 14.2, 17.1, 18.3, 21.2
Let point_sizes be list containing 5.0, 8.0, 6.0, 10.0, 7.0, 9.0, 8.5, 11.0, 6.5, 12.0
Let point_colors be list containing "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7"

Let scatter_config be viz.create_default_plot_config
Set scatter_config.title to Some with value as "Sales Performance by Region"
Set scatter_config.x_label to Some with value as "Marketing Spend (thousands)"
Set scatter_config.y_label to Some with value as "Revenue (thousands)"

Let scatter_result be viz.create_scatter_plot with 
    x_data as scatter_x 
    and y_data as scatter_y 
    and sizes as Some with value as point_sizes 
    and colors as Some with value as point_colors 
    and config as Some with value as scatter_config

Note: Bar chart
Let categories be list containing "Q1", "Q2", "Q3", "Q4"
Let values be list containing 15000.0, 23000.0, 18500.0, 27000.0

Let bar_result be viz.create_bar_plot with 
    categories as categories 
    and values as values 
    and orientation as Some with value as "vertical" 
    and config as None

Note: Histogram
Let sample_data be list containing 12.3, 15.7, 14.2, 16.8, 13.9, 17.1, 15.4, 14.7, 16.2, 13.5, 18.1, 14.9, 15.8, 16.5, 13.2

Let histogram_result be viz.create_histogram with 
    data as sample_data 
    and bins as Some with value as 8 
    and config as None
```

#### Statistical Plotting

```runa
Note: Box plot for distribution comparison
Let group_a_data be list containing 23.1, 24.7, 22.8, 25.3, 23.9, 24.1, 22.5, 25.0, 23.6, 24.4
Let group_b_data be list containing 27.2, 28.1, 26.9, 28.7, 27.5, 28.3, 26.8, 29.1, 27.8, 28.0
Let group_c_data be list containing 21.5, 22.3, 21.8, 22.7, 21.2, 22.0, 21.9, 22.5, 21.6, 22.1

Let box_plot_groups be list containing group_a_data, group_b_data, group_c_data
Let group_labels be list containing "Control Group", "Treatment A", "Treatment B"

Let box_plot_result be viz.create_box_plot with 
    data_groups as box_plot_groups 
    and group_labels as Some with value as group_labels 
    and config as None

Note: Violin plot for density visualization
Let violin_result be viz.create_violin_plot with 
    data_groups as box_plot_groups 
    and group_labels as Some with value as group_labels 
    and config as None

Note: Heatmap for correlation matrix
Let correlation_matrix be list containing:
    list containing 1.0, 0.8, 0.3, 0.1,
    list containing 0.8, 1.0, 0.5, 0.2,
    list containing 0.3, 0.5, 1.0, 0.7,
    list containing 0.1, 0.2, 0.7, 1.0

Let variable_names be list containing "Height", "Weight", "Age", "Income"

Let heatmap_result be viz.create_heatmap with 
    data_matrix as correlation_matrix 
    and row_labels as Some with value as variable_names 
    and column_labels as Some with value as variable_names 
    and config as None
```

#### DataFrame Integration

```runa
Note: Plot directly from DataFrame
Let sales_df_result be df.create_dataframe with data as Dictionary with:
    "month" as list containing "Jan", "Feb", "Mar", "Apr", "May", "Jun"
    "sales" as list containing 15000, 18000, 22000, 19000, 25000, 28000
    "profit" as list containing 3000, 4200, 5500, 4100, 6800, 7200

Match sales_df_result:
    When df.DataFrameSuccess with data as sales_df:
        Let df_plot_result be viz.dataframe_plot with 
            df as sales_df 
            and x as Some with value as "month" 
            and y as Some with value as "sales" 
            and kind as Some with value as "line" 
            and config as None
        
        Note: Create correlation heatmap from DataFrame
        Let correlation_heatmap_result be viz.dataframe_correlation_heatmap with 
            df as sales_df 
            and config as None
```

#### Interactive and Animated Visualizations

```runa
Note: Interactive scatter plot with zoom and pan
Let interactive_config be viz.create_default_plot_config
Set interactive_config.interactive to true
Set interactive_config.backend to viz.ChartBackend.webgl_backend

Let plot_data be viz.PlotData with:
    x_values as list containing 1.0, 2.0, 3.0, 4.0, 5.0
    y_values as list containing 2.1, 4.3, 6.8, 8.2, 10.5
    labels as None
    colors as None
    sizes as None
    metadata as Dictionary with empty entries

Let interactive_result be viz.create_interactive_plot with 
    plot_type as viz.PlotType.scatter_plot 
    and data as plot_data 
    and config as interactive_config

Note: Animated plot with time series data
Let initial_data be viz.PlotData with:
    x_values as list containing 1, 2, 3, 4, 5
    y_values as list containing 10, 15, 12, 18, 14
    labels as None
    colors as None
    sizes as None
    metadata as Dictionary with empty entries

Let frame1_data be viz.PlotData with:
    x_values as list containing 1, 2, 3, 4, 5
    y_values as list containing 12, 18, 15, 22, 17
    labels as None
    colors as None
    sizes as None
    metadata as Dictionary with empty entries

Let frame2_data be viz.PlotData with:
    x_values as list containing 1, 2, 3, 4, 5
    y_values as list containing 15, 22, 18, 25, 20
    labels as None
    colors as None
    sizes as None
    metadata as Dictionary with empty entries

Let animation_frames be list containing frame1_data, frame2_data

Let animated_result be viz.create_animated_plot with 
    initial_data as initial_data 
    and animation_frames as animation_frames 
    and config as interactive_config
```

#### Dashboard Creation

```runa
Note: Create multi-plot dashboard
Let plot1_result be viz.create_line_plot with x_data as x_data and y_data as y_data and config as None
Let plot2_result be viz.create_bar_plot with categories as categories and values as values and orientation as None and config as None
Let plot3_result be viz.create_histogram with data as sample_data and bins as None and config as None

Match plot1_result:
    When viz.PlotSuccess with plot_object as line_plot:
        Match plot2_result:
            When viz.PlotSuccess with plot_object as bar_plot:
                Match plot3_result:
                    When viz.PlotSuccess with plot_object as histogram_plot:
                        Let dashboard_plots be list containing line_plot, bar_plot, histogram_plot
                        
                        Let dashboard_result be viz.create_dashboard with 
                            plots as dashboard_plots 
                            and layout as "grid" 
                            and config as None
                        
                        Match dashboard_result:
                            When viz.PlotSuccess with plot_object as dashboard:
                                Display "Dashboard created successfully"
```

#### Plot Export and Saving

```runa
Note: Save plots in various formats
Match line_plot_result:
    When viz.PlotSuccess with plot_object as created_plot:
        Let svg_save_result be viz.save_plot_as_svg with 
            plot as created_plot 
            and file_path as "sales_trend.svg"
        
        Let png_save_result be viz.save_plot_as_png with 
            plot as created_plot 
            and file_path as "sales_trend.png" 
            and width as Some with value as 1200 
            and height as Some with value as 800
        
        Let data_export_result be viz.export_plot_data_as_csv with 
            plot as created_plot 
            and file_path as "sales_data.csv"
        
        If svg_save_result and png_save_result and data_export_result:
            Display "All exports completed successfully"
        Else:
            Display "Some exports failed"
```

## Advanced Features

### Custom Plot Themes

```runa
Note: Create custom theme
Let custom_theme be viz.PlotTheme with:
    background_color as "#f8f9fa"
    grid_color as "#dee2e6"
    axis_color as "#495057"
    text_color as "#212529"
    line_width as 2.5
    font_family as "Arial, Helvetica, sans-serif"
    font_size as 14

Let custom_config be viz.PlotConfiguration with:
    title as Some with value as "Custom Styled Chart"
    x_label as Some with value as "X Axis"
    y_label as Some with value as "Y Axis"
    width as 1000
    height as 700
    theme as custom_theme
    color_scheme as viz.ColorScheme.plasma
    backend as viz.ChartBackend.svg_backend
    interactive as true
    show_grid as true
    show_legend as true
```

### Performance Optimization

```runa
Note: Large dataset handling with streaming
Let large_dataset_config be pipelines.NodeConfiguration with:
    node_id as "large_data_processor"
    name as "Large Dataset Processor"
    operation_type as "streaming_transform"
    parameters as Dictionary with:
        "chunk_size" as 10000
        "memory_limit_mb" as 512
        "parallel_processing" as true
        "optimization_level" as "high"
    timeout_seconds as 600
    dependencies as empty list

Note: Efficient statistical computation
Let streaming_stats_result be stats.streaming_descriptive_statistics with 
    data_source as "large_dataset.csv" 
    and chunk_size as 10000 
    and statistics as list containing "mean", "std", "quantiles"
```

### Error Handling and Validation

```runa
Note: Comprehensive error handling example
Try:
    Let df_result be df.create_dataframe with data as potentially_invalid_data
    Match df_result:
        When df.DataFrameSuccess with data as valid_df:
            Let stats_result be stats.calculate_descriptive_statistics with 
                data as df.get_dataframe_column_values with df as valid_df and column as "values"
            
            Match stats_result:
                When stats.AnalysisSuccess with data as statistics:
                    Let viz_result be viz.create_histogram with 
                        data as df.get_dataframe_column_values with df as valid_df and column as "values"
                        and bins as None 
                        and config as None
                    
                    Match viz_result:
                        When viz.PlotSuccess with plot_object as histogram:
                            Display "Analysis pipeline completed successfully"
                        
                        When viz.PlotError with error as viz_error:
                            Display "Visualization failed: " with message viz_error.message
                
                When stats.AnalysisError with error as stats_error:
                    Display "Statistical analysis failed: " with message stats_error.message
        
        When df.DataFrameError with error as df_error:
            Display "DataFrame creation failed: " with message df_error.message

Catch error:
    Display "Unexpected error in analysis pipeline: " with message error as String
```

## Best Practices

### 1. Data Validation

Always validate input data before processing:

```runa
Process called "validate_dataset" that takes data as Dictionary[String, List[Any]] returns Boolean:
    Note: Validate dataset structure and content
    Try:
        If length of data is equal to 0:
            Return false
        
        Let first_column_length be 0
        Let column_count be 0
        
        For each column_name, column_data in data:
            If column_count is equal to 0:
                Set first_column_length to length of column_data
            Else:
                If length of column_data is not equal to first_column_length:
                    Return false
            
            Set column_count to column_count plus 1
        
        Return true
    
    Catch error:
        Return false
```

### 2. Memory Management

Handle large datasets efficiently:

```runa
Process called "process_large_dataset" that takes file_path as String returns DataProcessingResult:
    Note: Process large dataset with memory-efficient streaming
    Try:
        Let chunk_size be 10000
        Let total_processed be 0
        Let aggregated_stats be initialize_stats_accumulator
        
        Let streaming_result be df.read_dataframe_chunks with 
            file_path as file_path 
            and chunk_size as chunk_size
        
        Match streaming_result:
            When df.StreamingSuccess with chunks as data_chunks:
                For each chunk in data_chunks:
                    Let chunk_stats be stats.calculate_descriptive_statistics with 
                        data as df.get_dataframe_column_values with df as chunk and column as "target_column"
                    
                    Match chunk_stats:
                        When stats.AnalysisSuccess with data as chunk_statistics:
                            Set aggregated_stats to update_stats_accumulator with 
                                accumulator as aggregated_stats 
                                and new_stats as chunk_statistics
                            
                            Set total_processed to total_processed plus df.get_dataframe_shape with df as chunk["rows"]
        
        Return DataProcessingResult with:
            success as true
            records_processed as total_processed
            final_statistics as aggregated_stats
    
    Catch error:
        Return DataProcessingResult with:
            success as false
            error_message as error as String
```

### 3. Pipeline Design

Design robust, maintainable pipelines:

```runa
Process called "create_production_pipeline" returns PipelineResult:
    Note: Create production-ready data pipeline with comprehensive error handling
    Try:
        Let pipeline_config be pipelines.PipelineConfiguration with:
            pipeline_id as "production_analytics_pipeline"
            name as "Production Analytics Pipeline"
            description as Some with value as "End-to-end analytics pipeline with monitoring"
            timeout_seconds as 3600  Note: 1 hour timeout
            retry_policy as pipelines.RetryPolicy with:
                max_retries as 3
                retry_delay_ms as 30000  Note: 30 second delays
                exponential_backoff as true
            resource_limits as Dictionary with:
                "memory_mb" as 2048
                "cpu_cores" as 4
                "disk_space_mb" as 10240
        
        Let pipeline_result be pipelines.create_pipeline with config as pipeline_config
        Match pipeline_result:
            When pipelines.PipelineSuccess with data as production_pipeline:
                Note: Add comprehensive monitoring
                Let monitoring_config be create_monitoring_configuration with 
                    pipeline_id as production_pipeline.config.pipeline_id
                
                Let monitoring_result be pipelines.add_pipeline_monitoring with 
                    pipeline as production_pipeline 
                    and monitoring_config as monitoring_config
                
                Return PipelineResult with:
                    success as true
                    pipeline as production_pipeline
            
            When pipelines.PipelineError with error as pipeline_error:
                Return PipelineResult with:
                    success as false
                    error_message as pipeline_error.message
    
    Catch error:
        Return PipelineResult with:
            success as false
            error_message as "Failed to create production pipeline: " plus error as String
```

## Integration Examples

### Complete Data Science Workflow

```runa
Process called "complete_data_science_workflow" that takes data_source as String returns WorkflowResult:
    Note: Complete end-to-end data science workflow
    Try:
        Note: 1. Data Loading and Validation
        Let raw_data_result be df.read_dataframe_from_csv_file with file_path as data_source
        Match raw_data_result:
            When df.DataFrameSuccess with data as raw_df:
                Note: 2. Data Cleaning and Preprocessing
                Let cleaned_data_result be perform_data_cleaning with df as raw_df
                Match cleaned_data_result:
                    When DataCleaningSuccess with data as clean_df:
                        Note: 3. Exploratory Data Analysis
                        Let eda_result be perform_exploratory_analysis with df as clean_df
                        Match eda_result:
                            When EDASuccess with data as eda_insights:
                                Note: 4. Statistical Analysis
                                Let stats_result be perform_comprehensive_analysis with df as clean_df
                                Match stats_result:
                                    When stats.AnalysisSuccess with data as statistical_results:
                                        Note: 5. Visualization Dashboard
                                        Let dashboard_result be create_analysis_dashboard with 
                                            df as clean_df 
                                            and stats as statistical_results 
                                            and insights as eda_insights
                                        
                                        Match dashboard_result:
                                            When viz.PlotSuccess with plot_object as dashboard:
                                                Note: 6. Report Generation
                                                Let report_result be generate_analysis_report with 
                                                    data as clean_df 
                                                    and analysis as statistical_results 
                                                    and visualizations as dashboard
                                                
                                                Return WorkflowResult with:
                                                    success as true
                                                    dataframe as clean_df
                                                    analysis_results as statistical_results
                                                    dashboard as dashboard
                                                    report as report_result
        
        Return WorkflowResult with:
            success as false
            error_message as "Workflow failed at data loading stage"
    
    Catch error:
        Return WorkflowResult with:
            success as false
            error_message as "Unexpected workflow error: " plus error as String
```

## Performance Considerations

### Memory Usage

- Use streaming operations for large datasets
- Implement chunking for data processing
- Clear intermediate results when not needed
- Monitor memory usage in pipeline execution

### Computational Efficiency

- Leverage vectorized operations where possible
- Use appropriate data types for columns
- Implement parallel processing for independent operations
- Cache frequently accessed computed results

### Visualization Performance

- Use appropriate backends for different use cases
- Implement data sampling for large datasets in visualizations  
- Optimize SVG generation for complex plots
- Use progressive rendering for interactive visualizations

## Migration Guide

### From Pandas

The pandas compatibility layer provides seamless migration:

```runa
Note: Pandas code
import pandas as pd
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
result = df.head(2).describe()

Note: Equivalent Runa code
Import "data_science/pandas_compat" as pd
Let df be pd.DataFrame with data as Some with value as Dictionary with "A" as list containing 1, 2, 3 and "B" as list containing 4, 5, 6
Let result be df.head with n as Some with value as 2.describe
```

### From R

Statistical analysis functions provide R-like functionality:

```r
# R code
data <- c(1, 2, 3, 4, 5)
result <- t.test(data, mu = 3)
```

```runa
Note: Equivalent Runa code
Import "data_science/analysis" as stats
Let data be list containing 1.0, 2.0, 3.0, 4.0, 5.0
Let result be stats.one_sample_t_test with sample as data and population_mean as 3.0 and alpha as 0.05
```

## Conclusion

The Runa Data Science module provides a comprehensive, production-ready ecosystem for data analysis and processing. Its natural language syntax, type safety, and integrated design make it an excellent choice for both beginners and experienced data scientists.

Key advantages:

- **Natural Language Syntax**: Intuitive, readable code that expresses intent clearly
- **Type Safety**: Compile-time error detection and prevention
- **Integrated Ecosystem**: Seamless integration between all components
- **Production Ready**: Enterprise-grade features and reliability
- **Performance**: Optimized for both small and large-scale data processing
- **Compatibility**: Easy migration from existing Python/pandas workflows

For more examples and advanced usage patterns, see the comprehensive test suite in `tests/unit/stdlib/test_data_science.runa`.