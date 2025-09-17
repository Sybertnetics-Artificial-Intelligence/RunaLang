Note: Mathematical Plotting Module Guide

## Overview

The `math/visualization/plotting` module provides comprehensive 2D and 3D plotting capabilities for mathematical functions, data visualization, and advanced mathematical graphics. This module serves as the foundation for creating professional-quality mathematical plots with precise control over appearance and behavior.

## Key Features

- **Function Plotting**: Visualize mathematical functions y = f(x) and parametric curves
- **Data Visualization**: Create scatter plots, histograms, and statistical graphics
- **Multi-dimensional Plotting**: Support for 2D and basic 3D visualization
- **Mathematical Graphics**: Complex function visualization and domain coloring
- **Vector Field Visualization**: Display vector fields and flow patterns
- **High-Quality Output**: Export to multiple formats with publication-ready quality
- **Interactive Elements**: Support for zooming, panning, and dynamic updates

## Mathematical Foundation

The plotting module is built on solid mathematical principles:

- **Function Plots**: y = f(x) and parametric curves r(t) = [x(t), y(t)]
- **Multi-variable Functions**: z = f(x,y) as surface plots and contour maps
- **Implicit Functions**: F(x,y) = 0 and level curves F(x,y) = c
- **Vector Fields**: Visualization of F(x,y) = [P(x,y), Q(x,y)]
- **Complex Functions**: Domain coloring and Riemann surface visualization
- **Statistical Plots**: Histograms, scatter plots, regression analysis
- **Mathematical Transforms**: Fourier, Laplace, and integral transforms
- **Phase Portraits**: Solution curves for differential equations

## Core Data Types

### PlotAxis
Defines axis properties and appearance:
```runa
Type called "PlotAxis":
    label as String                    Note: Axis label text
    range as Tuple[Float64, Float64]  Note: [min, max] values
    tick_positions as List[Float64]   Note: Major tick locations
    tick_labels as List[String]       Note: Custom tick labels
    scale_type as String              Note: "linear", "log", "symlog"
    grid_visible as Boolean           Note: Show/hide grid lines
    axis_color as String              Note: Axis line color
```

### PlotSeries
Represents data series and visualization style:
```runa
Type called "PlotSeries":
    data_points as List[List[Float64]] Note: [x, y] or [x, y, z] coordinates
    series_type as String              Note: "line", "scatter", "bar", "area"
    color as String                    Note: RGB, HSV, or named color
    line_style as String               Note: "solid", "dashed", "dotted"
    marker_style as String             Note: "circle", "square", "triangle"
    label as String                    Note: Legend label
    visibility as Boolean              Note: Show/hide series
```

### PlotCanvas
Main plotting surface and configuration:
```runa
Type called "PlotCanvas":
    width as Float64                   Note: Canvas width in pixels
    height as Float64                  Note: Canvas height in pixels
    x_axis as PlotAxis                Note: X-axis configuration
    y_axis as PlotAxis                Note: Y-axis configuration
    background_color as String        Note: Canvas background
    title as String                   Note: Plot title
    legend_visible as Boolean         Note: Show/hide legend
    grid_style as String             Note: Grid appearance
```

## Basic Function Plotting

### Simple Function Plots
```runa
Import "math/visualization/plotting" as Plotting

Note: Create a basic function plot
Let canvas be Plotting.create_canvas(800.0, 600.0)
Let x_values be Plotting.generate_range(-10.0, 10.0, 0.1)
Let y_values be List[Float64]

Note: Calculate y = sin(x)
For Each x in x_values:
    Let sin_value be Trig.sine(String(x), "radians", 10)
    Add Float64(sin_value.function_value) to y_values

Note: Create series and plot
Let sine_series be PlotSeries with:
    data_points: Plotting.combine_xy(x_values, y_values)
    series_type: "line"
    color: "blue"
    label: "y = sin(x)"

Let plot_result be Plotting.plot_function(canvas, [sine_series])
```

### Parametric Curves
```runa
Note: Plot parametric curve r(t) = [cos(3t), sin(2t)]
Let t_values be Plotting.generate_range(0.0, 6.28, 0.05) Note: 0 to 2π
Let x_coords be List[Float64]
Let y_coords be List[Float64]

For Each t in t_values:
    Let x_val be Trig.cosine(String(3.0 * t), "radians", 10)
    Let y_val be Trig.sine(String(2.0 * t), "radians", 10)
    Add Float64(x_val.function_value) to x_coords
    Add Float64(y_val.function_value) to y_coords

Let lissajous_series be PlotSeries with:
    data_points: Plotting.combine_xy(x_coords, y_coords)
    series_type: "line"
    color: "red"
    line_style: "solid"
    label: "Lissajous curve"

Let parametric_plot be Plotting.plot_parametric(canvas, lissajous_series)
```

## Data Visualization

### Scatter Plots
```runa
Note: Create scatter plot from data
Let data_points be [
    [1.2, 3.4], [2.1, 4.7], [3.5, 6.2],
    [4.8, 8.1], [5.3, 9.6], [6.7, 11.2]
]

Let scatter_series be PlotSeries with:
    data_points: data_points
    series_type: "scatter"
    color: "green"
    marker_style: "circle"
    label: "Experimental data"

Let scatter_plot be Plotting.plot_scatter(canvas, scatter_series)
```

### Histograms
```runa
Note: Create histogram from dataset
Let dataset be [1.1, 2.3, 1.8, 3.2, 2.1, 1.9, 2.8, 3.5, 2.4, 1.7]
Let histogram_config be Dictionary[String, String] with:
    "bins": "10"
    "range": "auto"
    "density": "false"

Let hist_result be Plotting.create_histogram(dataset, histogram_config)
Let histogram_series be PlotSeries with:
    data_points: hist_result.bin_data
    series_type: "bar"
    color: "orange"
    label: "Data distribution"

Let hist_plot be Plotting.plot_histogram(canvas, histogram_series)
```

## Advanced Plotting Features

### Multi-Series Plots
```runa
Note: Plot multiple functions on same canvas
Let series_list be List[PlotSeries]

Note: Add sine function
Add sine_series to series_list

Note: Add cosine function
Let cos_values be List[Float64]
For Each x in x_values:
    Let cos_value be Trig.cosine(String(x), "radians", 10)
    Add Float64(cos_value.function_value) to cos_values

Let cosine_series be PlotSeries with:
    data_points: Plotting.combine_xy(x_values, cos_values)
    series_type: "line"
    color: "purple"
    line_style: "dashed"
    label: "y = cos(x)"

Add cosine_series to series_list

Let multi_plot be Plotting.plot_multiple_series(canvas, series_list)
```

### Contour Plots
```runa
Note: Create contour plot for z = f(x,y)
Process called "test_function" that takes x as Float64, y as Float64 returns Float64:
    Return x * x + y * y

Let x_grid be Plotting.generate_grid(-5.0, 5.0, 50)
Let y_grid be Plotting.generate_grid(-5.0, 5.0, 50)
Let z_values be Plotting.evaluate_function_2d(test_function, x_grid, y_grid)

Let contour_config be Dictionary[String, String] with:
    "levels": "10"
    "colormap": "viridis"
    "show_labels": "true"

Let contour_plot be Plotting.create_contour_plot(canvas, x_grid, y_grid, z_values, contour_config)
```

### Vector Field Visualization
```runa
Note: Visualize vector field F(x,y) = [P(x,y), Q(x,y)]
Process called "vector_field_x" that takes x as Float64, y as Float64 returns Float64:
    Return -y  Note: P(x,y) = -y

Process called "vector_field_y" that takes x as Float64, y as Float64 returns Float64:
    Return x   Note: Q(x,y) = x

Let field_grid be Plotting.generate_vector_grid(-3.0, 3.0, 15)
Let vector_data be Plotting.evaluate_vector_field_2d(
    vector_field_x,
    vector_field_y,
    field_grid
)

Let vector_config be Dictionary[String, String] with:
    "arrow_scale": "0.5"
    "arrow_color": "black"
    "density": "medium"

Let vector_plot be Plotting.plot_vector_field(canvas, vector_data, vector_config)
```

## Complex Function Visualization

### Domain Coloring
```runa
Note: Visualize complex function using domain coloring
Process called "complex_function" that takes z as ComplexNumber returns ComplexNumber:
    Note: f(z) = z^2
    Let real_squared be MathOps.multiply(z.real_part, z.real_part, 20)
    Let imag_squared be MathOps.multiply(z.imaginary_part, z.imaginary_part, 20)
    Let cross_term be MathOps.multiply("2", MathOps.multiply(z.real_part, z.imaginary_part, 20).result_value, 20)
    
    Let new_real be MathOps.subtract(real_squared.result_value, imag_squared.result_value, 20)
    Let new_imag be cross_term.result_value
    
    Return ComplexNumber with:
        real_part: new_real.result_value
        imaginary_part: new_imag
        precision: 20

Let complex_grid be Plotting.generate_complex_grid(-2.0, 2.0, -2.0, 2.0, 200)
Let domain_colors be Plotting.compute_domain_coloring(complex_function, complex_grid)

Let domain_config be Dictionary[String, String] with:
    "color_scheme": "hsv"
    "brightness_function": "modulus"
    "contour_lines": "true"

Let complex_plot be Plotting.plot_domain_coloring(canvas, domain_colors, domain_config)
```

## Statistical Plotting

### Box Plots
```runa
Note: Create box plot for statistical analysis
Let dataset_groups be Dictionary[String, List[Float64]] with:
    "Group A": [12.1, 14.3, 13.8, 15.2, 12.9, 14.1, 13.5]
    "Group B": [16.2, 18.1, 17.4, 19.3, 16.8, 17.9, 18.2]
    "Group C": [10.5, 11.2, 10.8, 11.9, 10.3, 11.4, 11.1]

Let boxplot_config be Dictionary[String, String] with:
    "show_outliers": "true"
    "notches": "true"
    "whisker_method": "iqr"

Let box_plot be Plotting.create_box_plot(canvas, dataset_groups, boxplot_config)
```

### Regression Analysis
```runa
Note: Plot data with regression line
Let regression_result be Plotting.calculate_linear_regression(data_points)

Let regression_series be PlotSeries with:
    data_points: regression_result.line_points
    series_type: "line"
    color: "red"
    line_style: "solid"
    label: "Linear fit (R² = " joined with String(regression_result.r_squared) joined with ")"

Let combined_series be [scatter_series, regression_series]
Let regression_plot be Plotting.plot_multiple_series(canvas, combined_series)
```

## Customization and Styling

### Axis Configuration
```runa
Note: Customize axis appearance
Let custom_x_axis be PlotAxis with:
    label: "Time (seconds)"
    range: [0.0, 10.0]
    scale_type: "linear"
    tick_positions: [0.0, 2.0, 4.0, 6.0, 8.0, 10.0]
    tick_labels: ["0", "2s", "4s", "6s", "8s", "10s"]
    grid_visible: true
    axis_color: "black"

Let custom_y_axis be PlotAxis with:
    label: "Amplitude"
    range: [-2.0, 2.0]
    scale_type: "linear"
    grid_visible: true
    axis_color: "black"

Let custom_canvas be PlotCanvas with:
    width: 1000.0
    height: 700.0
    x_axis: custom_x_axis
    y_axis: custom_y_axis
    background_color: "white"
    title: "Oscillatory Function Analysis"
    legend_visible: true
```

### Color Schemes and Themes
```runa
Note: Apply predefined color schemes
Let color_scheme be Plotting.get_color_scheme("scientific")
Let themed_series be Plotting.apply_color_scheme(series_list, color_scheme)

Note: Create custom theme
Let custom_theme be Dictionary[String, String] with:
    "background": "white"
    "grid_color": "lightgray"
    "text_color": "black"
    "primary_colors": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]

Let themed_plot be Plotting.apply_theme(canvas, custom_theme)
```

## Export and Output

### High-Quality Image Export
```runa
Note: Export plot to various formats
Let export_config be Dictionary[String, String] with:
    "format": "png"
    "resolution": "300"  Note: 300 DPI
    "width": "3000"      Note: pixels
    "height": "2000"     Note: pixels
    "transparent": "false"

Let export_result be Plotting.export_plot(plot_result, "mathematical_plot.png", export_config)

Note: Export as vector format
Let vector_config be Dictionary[String, String] with:
    "format": "svg"
    "text_as_paths": "false"
    "embed_fonts": "true"

Let svg_result be Plotting.export_plot(plot_result, "mathematical_plot.svg", vector_config)
```

### Interactive Features
```runa
Note: Add interactive capabilities
Let interactive_config be Dictionary[String, String] with:
    "zoom": "true"
    "pan": "true"
    "hover_info": "true"
    "click_callback": "point_info"

Let interactive_plot be Plotting.make_interactive(plot_result, interactive_config)

Note: Add animation timeline
Let animation_frames be Plotting.create_animation_sequence(
    parameter_ranges: ["t": [0.0, 6.28]],
    frame_count: 60,
    function_generator: animated_function
)
```

## Error Handling and Validation

### Input Validation
```runa
Try:
    Let validated_data be Plotting.validate_plot_data(data_points)
    Let plot_result be Plotting.plot_scatter(canvas, scatter_series)
Catch Errors.InvalidDataError as data_error:
    Display "Data validation failed: " joined with data_error.message
    Let suggestions be data_error.correction_suggestions
    For Each suggestion in suggestions:
        Display "  - " joined with suggestion
Catch Errors.RenderingError as render_error:
    Display "Rendering failed: " joined with render_error.message
    Let fallback_config be render_error.fallback_configuration
    Let fallback_plot be Plotting.plot_with_fallback(canvas, scatter_series, fallback_config)
```

### Performance Optimization
```runa
Note: Optimize for large datasets
Let optimization_config be Dictionary[String, String] with:
    "data_reduction": "true"
    "max_points": "10000"
    "simplification_tolerance": "0.01"
    "use_gpu": "true"

Let optimized_data be Plotting.optimize_dataset(large_dataset, optimization_config)
Let efficient_plot be Plotting.plot_optimized(canvas, optimized_data)
```

## Integration with Other Modules

### Mathematical Analysis Integration
```runa
Import "math/analysis/real" as RealAnalysis

Note: Plot function with critical points
Let function_analysis be RealAnalysis.analyze_function("x^3 - 3*x^2 + 2*x")
Let critical_points be function_analysis.critical_points
Let inflection_points be function_analysis.inflection_points

Note: Add annotations for critical points
Let annotations be List[Dictionary[String, String]]
For Each point in critical_points:
    Let annotation be Dictionary[String, String] with:
        "x": String(point.x)
        "y": String(point.y)
        "text": "Critical: " joined with point.classification
        "color": "red"
    Add annotation to annotations

Let annotated_plot be Plotting.add_annotations(plot_result, annotations)
```

### Statistical Integration
```runa
Import "math/statistics/descriptive" as Stats

Note: Plot with statistical overlays
Let stats_summary be Stats.compute_descriptive_statistics(dataset)

Let statistical_overlays be Dictionary[String, String] with:
    "mean_line": String(stats_summary.mean)
    "std_bands": String(stats_summary.standard_deviation)
    "median_line": String(stats_summary.median)

Let enhanced_plot be Plotting.add_statistical_overlays(plot_result, statistical_overlays)
```

## Performance Guidelines

### Memory Optimization
- **Data Reduction**: Use `optimize_dataset()` for large datasets (>10,000 points)
- **Streaming**: Process data in chunks for very large datasets
- **Caching**: Cache expensive function evaluations
- **Precision**: Use appropriate precision levels (avoid unnecessary high precision)

### Rendering Optimization
- **GPU Acceleration**: Enable GPU rendering for complex plots
- **Level of Detail**: Use adaptive detail levels for interactive plots
- **Batch Operations**: Group multiple plot operations together
- **Lazy Evaluation**: Defer expensive calculations until needed

## Common Use Cases

### Scientific Data Visualization
```runa
Note: Experimental data with error bars
Let experimental_data be load_experimental_dataset("temperature_measurements.csv")

Let error_bar_series be PlotSeries with:
    data_points: experimental_data.measurements
    series_type: "scatter"
    error_bars: experimental_data.uncertainties
    color: "blue"
    marker_style: "circle"
    label: "Temperature measurements"

Let scientific_plot be Plotting.plot_with_error_bars(canvas, error_bar_series)
```

### Educational Mathematics
```runa
Note: Interactive function exploration
Let function_explorer be Plotting.create_interactive_explorer(
    function_template: "a*sin(b*x + c) + d",
    parameters: ["a": [-2.0, 2.0], "b": [0.1, 5.0], "c": [0.0, 6.28], "d": [-1.0, 1.0]],
    x_range: [-10.0, 10.0]
)

Let educational_interface be Plotting.add_parameter_sliders(function_explorer)
```

### Engineering Applications
```runa
Note: Frequency response plotting
Let frequencies be Plotting.generate_log_range(0.1, 1000.0, 1000)
Let magnitude_response be calculate_magnitude_response(system_transfer_function, frequencies)
Let phase_response be calculate_phase_response(system_transfer_function, frequencies)

Note: Create Bode plot
Let bode_plot be Plotting.create_bode_plot(
    frequencies: frequencies,
    magnitude: magnitude_response,
    phase: phase_response,
    title: "System Frequency Response"
)
```

## Best Practices

### Plot Design Principles
1. **Clarity**: Use clear labels, legends, and titles
2. **Contrast**: Ensure good color contrast for accessibility
3. **Simplicity**: Avoid cluttered plots with too many elements
4. **Consistency**: Use consistent styling across related plots
5. **Scale**: Choose appropriate axis scales and ranges

### Code Organization
```runa
Note: Organize plotting code in reusable functions
Process called "create_standard_plot" that takes data as List[List[Float64]], title as String returns PlotResult:
    Let canvas be create_standard_canvas()
    Let series be create_data_series(data)
    Let plot be Plotting.plot_scatter(canvas, series)
    Let formatted_plot be apply_standard_formatting(plot, title)
    Return formatted_plot

Note: Use configuration objects for complex plots
Let plot_config be PlotConfiguration with:
    canvas_size: [1200.0, 800.0]
    color_scheme: "scientific"
    export_format: "png"
    interactive: true
    
Let automated_plot be Plotting.create_configured_plot(data, plot_config)
```

## Related Documentation

- **[Animation Module](animation.md)**: Animated and time-evolving plots
- **[Surfaces Module](surfaces.md)**: 3D surface and volume visualization
- **[Graphing Module](graphing.md)**: Graph theory and network visualization
- **[Math Statistics](../statistics/README.md)**: Statistical plotting functions
- **[Math Engine](../engine/README.md)**: Numerical computation backend
- **[Graphics 2D](../../../../app/graphics/2d/README.md)**: Low-level 2D graphics support

The plotting module provides the essential foundation for mathematical visualization in Runa, offering both simplicity for basic plots and power for advanced scientific visualization needs.