# Interpolation and Approximation

The Interpolation and Approximation module (`math/engine/numerical/interpolation`) provides comprehensive algorithms for fitting functions to data points, approximating complex functions, and constructing smooth curves and surfaces. This module implements classical polynomial interpolation, spline methods, multidimensional interpolation, and advanced approximation techniques essential for data analysis and numerical modeling.

## Quick Start

```runa
Import "math/engine/numerical/interpolation" as Interpolation
Import "math/core/functions" as MathFunctions

Note: Create sample data points
Let x_data be [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]
Let y_data be [1.0, 2.7183, 7.389, 20.086, 54.598, 148.413]  Note: Roughly e^x

Note: Linear interpolation (simplest method)
Let linear_interpolant be Interpolation.create_linear_interpolant(x_data, y_data)
Let interpolated_value be Interpolation.evaluate(linear_interpolant, 2.5)

Display "Linear interpolation at x=2.5: " joined with interpolated_value
Display "Actual e^2.5: " joined with MathFunctions.exp(2.5)

Note: Polynomial interpolation using Lagrange method
Let lagrange_interpolant be Interpolation.lagrange_interpolation(x_data, y_data)
Let lagrange_value be Interpolation.evaluate(lagrange_interpolant, 2.5)

Display "Lagrange interpolation at x=2.5: " joined with lagrange_value

Note: Cubic spline interpolation (smooth curve)
Let cubic_spline be Interpolation.cubic_spline_interpolation(
    x_data,
    y_data,
    boundary_conditions: "natural"
)

Let spline_value be Interpolation.evaluate(cubic_spline, 2.5)
Let spline_derivative be Interpolation.evaluate_derivative(cubic_spline, 2.5)

Display "Cubic spline at x=2.5: " joined with spline_value
Display "Cubic spline derivative at x=2.5: " joined with spline_derivative

Note: Compare interpolation methods
Let test_points be [0.5, 1.5, 2.5, 3.5, 4.5]

Display "Comparison at test points:"
For test_x in test_points:
    Let linear_val be Interpolation.evaluate(linear_interpolant, test_x)
    Let lagrange_val be Interpolation.evaluate(lagrange_interpolant, test_x)
    Let spline_val be Interpolation.evaluate(cubic_spline, test_x)
    Let exact_val be MathFunctions.exp(test_x)
    
    Display "x=" joined with test_x joined with ": Linear=" joined with linear_val 
        joined with ", Lagrange=" joined with lagrange_val 
        joined with ", Spline=" joined with spline_val 
        joined with ", Exact=" joined with exact_val
```

## Polynomial Interpolation

### Classical Polynomial Methods

```runa
Note: Lagrange polynomial interpolation
Let polynomial_x_data be [0.0, 1.0, 2.0, 3.0]
Let polynomial_y_data be [1.0, 4.0, 9.0, 16.0]  Note: y = x^2 + 3x + 1

Note: Lagrange form - explicit polynomial construction
Let lagrange_polynomial be Interpolation.lagrange_polynomial_explicit(
    polynomial_x_data,
    polynomial_y_data
)

Let polynomial_coefficients be Interpolation.get_polynomial_coefficients(lagrange_polynomial)
Display "Lagrange polynomial coefficients: " joined with 
    Interpolation.format_coefficients(polynomial_coefficients)

Note: Evaluate Lagrange polynomial at various points
Let evaluation_points be [0.5, 1.5, 2.5]
For eval_x in evaluation_points:
    Let lagrange_eval be Interpolation.evaluate_polynomial(lagrange_polynomial, eval_x)
    Let exact_eval be eval_x * eval_x + 3.0 * eval_x + 1.0
    Let error be Interpolation.abs(lagrange_eval - exact_eval)
    
    Display "x=" joined with eval_x joined with ": Lagrange=" joined with lagrange_eval
        joined with ", Exact=" joined with exact_eval joined with ", Error=" joined with error

Note: Newton divided difference interpolation
Let newton_interpolant be Interpolation.newton_divided_difference(
    polynomial_x_data,
    polynomial_y_data
)

Let divided_diff_table be Interpolation.get_divided_difference_table(newton_interpolant)
Display "Divided difference table:"
Display Interpolation.format_divided_difference_table(divided_diff_table)

Note: Newton forward difference (equispaced points)
Let equispaced_x be [0.0, 1.0, 2.0, 3.0, 4.0]
Let equispaced_y be [2.0, 3.0, 6.0, 11.0, 18.0]

Let newton_forward be Interpolation.newton_forward_difference(
    equispaced_x,
    equispaced_y
)

Let forward_diff_table be Interpolation.get_forward_difference_table(newton_forward)
Display "Forward difference table:"
Display Interpolation.format_forward_difference_table(forward_diff_table)

Note: Newton backward difference
Let newton_backward be Interpolation.newton_backward_difference(
    equispaced_x,
    equispaced_y
)

Note: Error analysis for polynomial interpolation
Let interpolation_error_analysis be Interpolation.analyze_polynomial_interpolation_error(
    polynomial_function: "exponential",  Note: e^x
    interpolation_points: polynomial_x_data,
    evaluation_interval: [0.0, 3.0],
    num_test_points: 100
)

Let max_error be Interpolation.get_maximum_interpolation_error(interpolation_error_analysis)
Let average_error be Interpolation.get_average_interpolation_error(interpolation_error_analysis)

Display "Maximum interpolation error: " joined with max_error
Display "Average interpolation error: " joined with average_error
```

### High-Degree Polynomial Issues

```runa
Note: Runge's phenomenon demonstration
Let runge_function_x be []
Let runge_function_y be []

Note: Create points for Runge function: f(x) = 1/(1 + 25x^2)
For i from 0 to 10:
    Let x_val be -1.0 + (2.0 * i) / 10.0
    Let y_val be 1.0 / (1.0 + 25.0 * x_val * x_val)
    Interpolation.append_to_list(runge_function_x, x_val)
    Interpolation.append_to_list(runge_function_y, y_val)

Let high_degree_interpolant be Interpolation.lagrange_interpolation(
    runge_function_x,
    runge_function_y
)

Note: Evaluate at many points to see oscillations
Let oscillation_analysis be Interpolation.analyze_oscillations(
    high_degree_interpolant,
    evaluation_interval: [-1.0, 1.0],
    num_points: 200
)

Let max_oscillation_amplitude be Interpolation.get_max_oscillation_amplitude(oscillation_analysis)
Let oscillation_frequency be Interpolation.get_oscillation_frequency(oscillation_analysis)

Display "High-degree polynomial maximum oscillation: " joined with max_oscillation_amplitude
Display "Oscillation frequency near boundaries: " joined with oscillation_frequency

Note: Chebyshev points to reduce Runge phenomenon
Let chebyshev_points be Interpolation.generate_chebyshev_points(11, interval: [-1.0, 1.0])
Let chebyshev_y_values be []

For cheb_x in chebyshev_points:
    Let cheb_y be 1.0 / (1.0 + 25.0 * cheb_x * cheb_x)
    Interpolation.append_to_list(chebyshev_y_values, cheb_y)

Let chebyshev_interpolant be Interpolation.lagrange_interpolation(
    chebyshev_points,
    chebyshev_y_values
)

Let chebyshev_error_analysis be Interpolation.compare_interpolation_stability(
    uniform_interpolant: high_degree_interpolant,
    chebyshev_interpolant: chebyshev_interpolant,
    test_function: "runge_function",
    evaluation_interval: [-1.0, 1.0]
)

Let stability_improvement be Interpolation.get_stability_improvement_factor(chebyshev_error_analysis)
Display "Chebyshev points stability improvement: " joined with stability_improvement joined with "x"
```

### Hermite Interpolation

```runa
Note: Hermite interpolation - matching function values and derivatives
Let hermite_x_data be [0.0, 1.0, 2.0]
Let hermite_y_data be [1.0, 2.7183, 7.389]  Note: e^x values
Let hermite_dy_data be [1.0, 2.7183, 7.389]  Note: e^x derivative values

Let hermite_interpolant be Interpolation.hermite_interpolation(
    hermite_x_data,
    hermite_y_data,
    hermite_dy_data
)

Note: Evaluate Hermite interpolant and compare with exact function
Let hermite_test_points be [0.5, 1.5]
For test_x in hermite_test_points:
    Let hermite_val be Interpolation.evaluate(hermite_interpolant, test_x)
    Let hermite_deriv be Interpolation.evaluate_derivative(hermite_interpolant, test_x)
    Let exact_val be MathFunctions.exp(test_x)
    Let exact_deriv be MathFunctions.exp(test_x)
    
    Display "Hermite at x=" joined with test_x joined with ":"
    Display "  Value: " joined with hermite_val joined with " (exact: " joined with exact_val joined with ")"
    Display "  Derivative: " joined with hermite_deriv joined with " (exact: " joined with exact_deriv joined with ")"

Note: Higher-order Hermite interpolation
Let hermite_second_derivatives be [1.0, 2.7183, 7.389]  Note: e^x second derivatives

Let hermite_higher_order be Interpolation.hermite_interpolation_higher_order(
    hermite_x_data,
    hermite_y_data,
    derivatives: [hermite_dy_data, hermite_second_derivatives]
)

Let higher_order_accuracy be Interpolation.measure_interpolation_accuracy(
    hermite_higher_order,
    reference_function: "exponential",
    test_interval: [0.0, 2.0],
    num_test_points: 50
)

Display "Higher-order Hermite accuracy: " joined with higher_order_accuracy joined with " (RMS error)"
```

## Spline Interpolation

### Cubic Splines

```runa
Note: Natural cubic spline (zero second derivatives at endpoints)
Let spline_x_data be [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
Let spline_y_data be [0.0, 0.479, 0.841, 0.997, 0.909, 0.598, 0.141]  Note: Sin-like data

Let natural_spline be Interpolation.natural_cubic_spline(spline_x_data, spline_y_data)

Note: Clamped cubic spline (specified first derivatives at endpoints)
Let clamped_spline be Interpolation.clamped_cubic_spline(
    spline_x_data,
    spline_y_data,
    first_derivative_start: 1.0,
    first_derivative_end: -1.0
)

Note: Periodic cubic spline (for periodic data)
Let periodic_x_data be [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
Let periodic_y_data be [0.0, 0.866, 0.866, 0.0, -0.866, -0.866, 0.0]  Note: Roughly sin(πx/3)

Let periodic_spline be Interpolation.periodic_cubic_spline(periodic_x_data, periodic_y_data)

Note: Compare different spline boundary conditions
Let comparison_points be [0.25, 0.75, 1.25, 1.75, 2.25, 2.75]

Display "Spline comparison at test points:"
For test_x in comparison_points:
    Let natural_val be Interpolation.evaluate(natural_spline, test_x)
    Let clamped_val be Interpolation.evaluate(clamped_spline, test_x)
    
    Display "x=" joined with test_x joined with ": Natural=" joined with natural_val
        joined with ", Clamped=" joined with clamped_val

Note: Analyze spline smoothness
Let smoothness_analysis be Interpolation.analyze_spline_smoothness(
    natural_spline,
    evaluation_interval: [0.0, 3.0],
    smoothness_criteria: ["continuity", "first_derivative", "second_derivative"]
)

Let c0_continuous be Interpolation.is_c0_continuous(smoothness_analysis)
Let c1_continuous be Interpolation.is_c1_continuous(smoothness_analysis)
Let c2_continuous be Interpolation.is_c2_continuous(smoothness_analysis)

Display "Spline continuity: C0=" joined with c0_continuous 
    joined with ", C1=" joined with c1_continuous 
    joined with ", C2=" joined with c2_continuous
```

### B-Splines and NURBS

```runa
Note: B-spline construction with uniform knots
Let control_points be [
    [0.0, 0.0],
    [1.0, 2.0],
    [2.0, 1.0],
    [3.0, 3.0],
    [4.0, 0.0]
]

Let bspline_degree be 3
Let uniform_knots be Interpolation.generate_uniform_knots(
    num_control_points: 5,
    degree: bspline_degree
)

Let bspline_curve be Interpolation.create_bspline_curve(
    control_points,
    uniform_knots,
    bspline_degree
)

Note: Evaluate B-spline curve at parameter values
Let parameter_values be [0.0, 0.25, 0.5, 0.75, 1.0]
Display "B-spline curve points:"
For t in parameter_values:
    Let curve_point be Interpolation.evaluate_bspline(bspline_curve, t)
    Display "t=" joined with t joined with ": (" joined with 
        Interpolation.get_point_x(curve_point) joined with ", " joined with
        Interpolation.get_point_y(curve_point) joined with ")"

Note: Non-uniform rational B-splines (NURBS)
Let weights be [1.0, 0.5, 1.0, 2.0, 1.0]  Note: Rational weights
Let nurbs_curve be Interpolation.create_nurbs_curve(
    control_points,
    uniform_knots,
    weights,
    bspline_degree
)

Note: Compare B-spline vs NURBS
Let nurbs_comparison_points be []
For t in parameter_values:
    Let bspline_point be Interpolation.evaluate_bspline(bspline_curve, t)
    Let nurbs_point be Interpolation.evaluate_nurbs(nurbs_curve, t)
    
    Let point_difference be Interpolation.compute_point_distance(bspline_point, nurbs_point)
    Interpolation.append_to_list(nurbs_comparison_points, point_difference)

Let max_difference be Interpolation.max_value(nurbs_comparison_points)
Display "Maximum B-spline vs NURBS difference: " joined with max_difference

Note: Knot insertion and curve refinement
Let refined_bspline be Interpolation.insert_knot(bspline_curve, knot_value: 0.5)
Let refined_control_points be Interpolation.get_refined_control_points(refined_bspline)

Display "Original control points: " joined with Interpolation.count_points(control_points)
Display "Refined control points: " joined with Interpolation.count_points(refined_control_points)

Note: Degree elevation
Let elevated_bspline be Interpolation.elevate_degree(bspline_curve, new_degree: 4)
Let elevated_smoothness be Interpolation.measure_curve_smoothness(elevated_bspline)

Display "Elevated B-spline degree: " joined with Interpolation.get_curve_degree(elevated_bspline)
Display "Curve smoothness measure: " joined with elevated_smoothness
```

### Spline Fitting and Approximation

```runa
Note: Least squares spline fitting to noisy data
Let noisy_x_data be [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]
Let noisy_y_data be [1.05, 1.18, 1.42, 1.58, 1.89, 2.12, 2.25, 2.48, 2.71, 2.89, 3.02]

Note: Fit with fewer knots than data points (smoothing spline)
Let smoothing_spline be Interpolation.least_squares_spline_fit(
    noisy_x_data,
    noisy_y_data,
    spline_degree: 3,
    num_knots: 6,
    regularization_parameter: 0.01
)

Let fitting_residuals be Interpolation.compute_fitting_residuals(
    smoothing_spline,
    noisy_x_data,
    noisy_y_data
)

Let rms_error be Interpolation.compute_rms_error(fitting_residuals)
Display "Smoothing spline RMS fitting error: " joined with rms_error

Note: Adaptive spline fitting with automatic knot placement
Let adaptive_spline be Interpolation.adaptive_spline_fit(
    noisy_x_data,
    noisy_y_data,
    tolerance: 0.1,
    max_knots: 10
)

Let final_knot_count be Interpolation.get_knot_count(adaptive_spline)
Let adaptive_rms_error be Interpolation.compute_fitting_error(adaptive_spline, noisy_x_data, noisy_y_data)

Display "Adaptive spline knots used: " joined with final_knot_count
Display "Adaptive spline RMS error: " joined with adaptive_rms_error

Note: Penalized spline smoothing
Let penalized_spline be Interpolation.penalized_spline_smoothing(
    noisy_x_data,
    noisy_y_data,
    smoothing_parameter: 0.1,
    penalty_order: 2  Note: Penalize second derivative roughness
)

Let smoothness_measure be Interpolation.compute_smoothness_measure(penalized_spline)
Let data_fidelity be Interpolation.compute_data_fidelity(penalized_spline, noisy_x_data, noisy_y_data)

Display "Penalized spline smoothness: " joined with smoothness_measure
Display "Penalized spline data fidelity: " joined with data_fidelity
```

## Multidimensional Interpolation

### Bivariate Interpolation

```runa
Note: 2D data interpolation - scattered data points
Let x_coords be [0.0, 1.0, 2.0, 0.0, 1.0, 2.0, 0.0, 1.0, 2.0]
Let y_coords be [0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0]
Let z_values be [1.0, 2.0, 5.0, 2.0, 3.0, 6.0, 5.0, 6.0, 9.0]  Note: z = x^2 + y^2 + 1

Note: Bilinear interpolation on regular grid
Let bilinear_interpolant be Interpolation.bilinear_interpolation_grid(
    x_grid: [0.0, 1.0, 2.0],
    y_grid: [0.0, 1.0, 2.0],
    z_grid: [[1.0, 2.0, 5.0], [2.0, 3.0, 6.0], [5.0, 6.0, 9.0]]
)

Let test_point_x be 0.5
Let test_point_y be 1.5
Let bilinear_result be Interpolation.evaluate_2d(bilinear_interpolant, test_point_x, test_point_y)
Let exact_result be test_point_x * test_point_x + test_point_y * test_point_y + 1.0

Display "Bilinear interpolation at (0.5, 1.5): " joined with bilinear_result
Display "Exact value: " joined with exact_result

Note: Bicubic interpolation for smoother surfaces
Let bicubic_interpolant be Interpolation.bicubic_interpolation_grid(
    x_grid: [0.0, 1.0, 2.0],
    y_grid: [0.0, 1.0, 2.0],
    z_grid: [[1.0, 2.0, 5.0], [2.0, 3.0, 6.0], [5.0, 6.0, 9.0]],
    boundary_conditions: "natural"
)

Let bicubic_result be Interpolation.evaluate_2d(bicubic_interpolant, test_point_x, test_point_y)
Display "Bicubic interpolation at (0.5, 1.5): " joined with bicubic_result

Note: Radial basis function interpolation for scattered data
Let rbf_interpolant be Interpolation.radial_basis_function_interpolation(
    x_coords,
    y_coords,
    z_values,
    rbf_type: "thin_plate_spline"
)

Let rbf_result be Interpolation.evaluate_rbf_2d(rbf_interpolant, test_point_x, test_point_y)
Display "RBF interpolation at (0.5, 1.5): " joined with rbf_result

Note: Compare 2D interpolation methods
Let interpolation_comparison be Interpolation.compare_2d_methods(
    x_data: x_coords,
    y_data: y_coords,
    z_data: z_values,
    methods: ["bilinear", "bicubic", "rbf_thin_plate", "rbf_gaussian"],
    test_points: [(0.5, 0.5), (1.5, 0.5), (0.5, 1.5), (1.5, 1.5)]
)

Display "2D interpolation method comparison:"
For method in ["bilinear", "bicubic", "rbf_thin_plate", "rbf_gaussian"]:
    Let method_accuracy be Interpolation.get_method_accuracy_2d(interpolation_comparison, method)
    Display "  " joined with method joined with ": RMS error = " joined with method_accuracy
```

### Tensor Product Methods

```runa
Note: Tensor product splines for structured 3D data
Let x_1d_data be [0.0, 1.0, 2.0, 3.0]
Let y_1d_data be [0.0, 0.5, 1.0]
Let z_1d_data be [0.0, 1.0]

Note: Create 3D function data: f(x,y,z) = x*y + z*z
Let tensor_product_data be []
For k from 0 to 1:
    Let z_layer be []
    For j from 0 to 2:
        Let y_row be []
        For i from 0 to 3:
            Let x_val be Interpolation.get_element(x_1d_data, i)
            Let y_val be Interpolation.get_element(y_1d_data, j)
            Let z_val be Interpolation.get_element(z_1d_data, k)
            Let function_value be x_val * y_val + z_val * z_val
            Interpolation.append_to_list(y_row, function_value)
        Interpolation.append_to_list(z_layer, y_row)
    Interpolation.append_to_list(tensor_product_data, z_layer)

Let tensor_spline_3d be Interpolation.tensor_product_spline_3d(
    x_1d_data,
    y_1d_data,
    z_1d_data,
    tensor_product_data,
    spline_degrees: [3, 3, 3]
)

Let test_3d_point be [1.5, 0.25, 0.5]
Let tensor_result be Interpolation.evaluate_3d(tensor_spline_3d, test_3d_point)
Let exact_3d_result be 1.5 * 0.25 + 0.5 * 0.5

Display "Tensor product 3D interpolation at (1.5, 0.25, 0.5): " joined with tensor_result
Display "Exact 3D value: " joined with exact_3d_result

Note: Partial derivatives from tensor product splines
Let partial_dx be Interpolation.evaluate_partial_derivative_3d(tensor_spline_3d, test_3d_point, "x")
Let partial_dy be Interpolation.evaluate_partial_derivative_3d(tensor_spline_3d, test_3d_point, "y")
Let partial_dz be Interpolation.evaluate_partial_derivative_3d(tensor_spline_3d, test_3d_point, "z")

Display "Partial derivatives at test point:"
Display "  ∂f/∂x = " joined with partial_dx joined with " (exact: " joined with 0.25 joined with ")"
Display "  ∂f/∂y = " joined with partial_dy joined with " (exact: " joined with 1.5 joined with ")"
Display "  ∂f/∂z = " joined with partial_dz joined with " (exact: " joined with (2.0 * 0.5) joined with ")"
```

### Scattered Data Interpolation

```runa
Note: Interpolation of irregularly distributed data points
Let scattered_x be [0.1, 0.8, 1.2, 1.9, 0.3, 1.7, 0.6, 1.4]
Let scattered_y be [0.2, 0.1, 0.9, 0.7, 0.6, 0.3, 0.8, 0.5]
Let scattered_z be []

Note: Generate scattered data from known function
For i from 0 to (Interpolation.count_points(scattered_x) - 1):
    Let x_val be Interpolation.get_element(scattered_x, i)
    Let y_val be Interpolation.get_element(scattered_y, i)
    Let z_val be MathFunctions.sin(3.14159 * x_val) * MathFunctions.cos(3.14159 * y_val)
    Interpolation.append_to_list(scattered_z, z_val)

Note: Shepard's method (inverse distance weighting)
Let shepard_interpolant be Interpolation.shepard_interpolation(
    scattered_x,
    scattered_y,
    scattered_z,
    power_parameter: 2.0
)

Note: Natural neighbor interpolation
Let natural_neighbor_interpolant be Interpolation.natural_neighbor_interpolation(
    scattered_x,
    scattered_y,
    scattered_z
)

Note: Kriging interpolation (geostatistical method)
Let kriging_interpolant be Interpolation.kriging_interpolation(
    scattered_x,
    scattered_y,
    scattered_z,
    variogram_model: "exponential",
    nugget: 0.01,
    sill: 1.0,
    range_parameter: 0.5
)

Note: Compare scattered data methods
Let scattered_test_points be [(0.5, 0.4), (1.0, 0.6), (1.5, 0.2)]

Display "Scattered data interpolation comparison:"
For test_point in scattered_test_points:
    Let test_x be Interpolation.get_point_x(test_point)
    Let test_y be Interpolation.get_point_y(test_point)
    
    Let shepard_val be Interpolation.evaluate_2d(shepard_interpolant, test_x, test_y)
    Let nn_val be Interpolation.evaluate_2d(natural_neighbor_interpolant, test_x, test_y)
    Let kriging_val be Interpolation.evaluate_2d(kriging_interpolant, test_x, test_y)
    Let exact_val be MathFunctions.sin(3.14159 * test_x) * MathFunctions.cos(3.14159 * test_y)
    
    Display "Point (" joined with test_x joined with ", " joined with test_y joined with "):"
    Display "  Shepard: " joined with shepard_val joined with ", Error: " joined with 
        Interpolation.abs(shepard_val - exact_val)
    Display "  Natural neighbor: " joined with nn_val joined with ", Error: " joined with
        Interpolation.abs(nn_val - exact_val)
    Display "  Kriging: " joined with kriging_val joined with ", Error: " joined with
        Interpolation.abs(kriging_val - exact_val)
```

## Approximation Theory

### Chebyshev Approximation

```runa
Note: Chebyshev polynomial approximation
Process called "approximation_target_function" that takes x as Real returns Real:
    Return MathFunctions.exp(x)

Let chebyshev_approximation be Interpolation.chebyshev_approximation(
    approximation_target_function,
    approximation_interval: [-1.0, 1.0],
    polynomial_degree: 8
)

Let chebyshev_coefficients be Interpolation.get_chebyshev_coefficients(chebyshev_approximation)
Display "Chebyshev coefficients:"
For i from 0 to (Interpolation.count_coefficients(chebyshev_coefficients) - 1):
    Let coeff be Interpolation.get_coefficient(chebyshev_coefficients, i)
    Display "  T_" joined with i joined with ": " joined with coeff

Note: Evaluate Chebyshev approximation
Let chebyshev_test_points be [-0.8, -0.4, 0.0, 0.4, 0.8]
Display "Chebyshev approximation accuracy:"
For test_x in chebyshev_test_points:
    Let approx_val be Interpolation.evaluate_chebyshev(chebyshev_approximation, test_x)
    Let exact_val be MathFunctions.exp(test_x)
    Let error be Interpolation.abs(approx_val - exact_val)
    
    Display "x=" joined with test_x joined with ": Approx=" joined with approx_val
        joined with ", Exact=" joined with exact_val joined with ", Error=" joined with error

Note: Minimax approximation (Remez exchange algorithm)
Let remez_approximation be Interpolation.remez_approximation(
    approximation_target_function,
    approximation_interval: [-1.0, 1.0],
    polynomial_degree: 6,
    max_iterations: 50,
    tolerance: 1e-12
)

Let minimax_error be Interpolation.get_minimax_error(remez_approximation)
Let error_equioscillation_points be Interpolation.get_equioscillation_points(remez_approximation)

Display "Remez minimax error: " joined with minimax_error
Display "Equioscillation points: " joined with 
    Interpolation.format_point_list(error_equioscillation_points)
```

### Least Squares Approximation

```runa
Note: Weighted least squares polynomial fitting
Let fitting_x_data be [-2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0]
Let fitting_y_data be []
Let fitting_weights be []

Note: Generate data with varying noise levels
For x_val in fitting_x_data:
    Let true_value be x_val * x_val * x_val - 2.0 * x_val + 1.0
    Let noise_level be 0.1 * (1.0 + Interpolation.abs(x_val))
    Let noisy_value be true_value + Interpolation.random_normal(0.0, noise_level)
    Let weight be 1.0 / (noise_level * noise_level)  Note: Inverse variance weighting
    
    Interpolation.append_to_list(fitting_y_data, noisy_value)
    Interpolation.append_to_list(fitting_weights, weight)

Let weighted_ls_fit be Interpolation.weighted_least_squares_polynomial(
    fitting_x_data,
    fitting_y_data,
    fitting_weights,
    polynomial_degree: 3
)

Let ls_coefficients be Interpolation.get_polynomial_coefficients(weighted_ls_fit)
Display "Weighted least squares coefficients: " joined with 
    Interpolation.format_coefficients(ls_coefficients)

Note: Orthogonal polynomial least squares
Let orthogonal_ls_fit be Interpolation.orthogonal_polynomial_least_squares(
    fitting_x_data,
    fitting_y_data,
    fitting_weights,
    basis_type: "legendre",
    polynomial_degree: 3
)

Let orthogonal_coefficients be Interpolation.get_orthogonal_coefficients(orthogonal_ls_fit)
Display "Orthogonal polynomial coefficients: " joined with 
    Interpolation.format_coefficients(orthogonal_coefficients)

Note: Ridge regression for regularized fitting
Let ridge_fit be Interpolation.ridge_regression_polynomial(
    fitting_x_data,
    fitting_y_data,
    polynomial_degree: 8,
    regularization_parameter: 0.1
)

Let ridge_coefficients be Interpolation.get_polynomial_coefficients(ridge_fit)
Let coefficient_shrinkage be Interpolation.compute_coefficient_shrinkage(
    unregularized_fit: weighted_ls_fit,
    regularized_fit: ridge_fit
)

Display "Ridge regression coefficient shrinkage: " joined with coefficient_shrinkage
```

### Rational Approximation

```runa
Note: Padé approximation for rational functions
Process called "rational_target_function" that takes x as Real returns Real:
    Return MathFunctions.exp(x)

Let pade_approximation be Interpolation.pade_approximation(
    rational_target_function,
    expansion_point: 0.0,
    numerator_degree: 4,
    denominator_degree: 4
)

Let pade_numerator_coeffs be Interpolation.get_pade_numerator_coefficients(pade_approximation)
Let pade_denominator_coeffs be Interpolation.get_pade_denominator_coefficients(pade_approximation)

Display "Padé [4/4] approximation for exp(x):"
Display "Numerator coefficients: " joined with 
    Interpolation.format_coefficients(pade_numerator_coeffs)
Display "Denominator coefficients: " joined with
    Interpolation.format_coefficients(pade_denominator_coeffs)

Note: Evaluate Padé approximation
Let pade_test_points be [-0.5, -0.25, 0.0, 0.25, 0.5]
Display "Padé approximation accuracy:"
For test_x in pade_test_points:
    Let pade_val be Interpolation.evaluate_pade(pade_approximation, test_x)
    Let exact_val be MathFunctions.exp(test_x)
    Let relative_error be Interpolation.abs((pade_val - exact_val) / exact_val)
    
    Display "x=" joined with test_x joined with ": Padé=" joined with pade_val
        joined with ", Exact=" joined with exact_val 
        joined with ", Rel. Error=" joined with relative_error

Note: Rational least squares approximation
Let rational_ls_approximation be Interpolation.rational_least_squares(
    fitting_x_data,
    fitting_y_data,
    numerator_degree: 3,
    denominator_degree: 2,
    regularization: 0.001
)

Let rational_ls_accuracy be Interpolation.compute_approximation_error(
    rational_ls_approximation,
    fitting_x_data,
    fitting_y_data
)

Display "Rational least squares RMS error: " joined with rational_ls_accuracy
```

## Advanced Interpolation Techniques

### Adaptive and Hierarchical Methods

```runa
Note: Adaptive interpolation with error control
Process called "complex_target_function" that takes x as Real returns Real:
    Return MathFunctions.sin(10.0 * x) * MathFunctions.exp(-x * x)

Let adaptive_interpolation be Interpolation.adaptive_interpolation(
    complex_target_function,
    initial_interval: [-2.0, 2.0],
    target_tolerance: 1e-6,
    max_points: 100,
    refinement_strategy: "equidistributed_error"
)

Let final_interpolation_points be Interpolation.get_adaptive_points(adaptive_interpolation)
Let achieved_accuracy be Interpolation.get_achieved_accuracy(adaptive_interpolation)

Display "Adaptive interpolation used " joined with 
    Interpolation.count_points(final_interpolation_points) joined with " points"
Display "Achieved accuracy: " joined with achieved_accuracy

Note: Hierarchical basis interpolation
Let hierarchical_interpolation be Interpolation.hierarchical_basis_interpolation(
    complex_target_function,
    domain: [-2.0, 2.0],
    max_levels: 6,
    basis_type: "hat_functions"
)

Let hierarchy_levels be Interpolation.get_hierarchy_levels(hierarchical_interpolation)
Display "Hierarchical interpolation levels:"
For level from 0 to (Interpolation.count_levels(hierarchy_levels) - 1):
    Let level_points be Interpolation.get_level_points(hierarchy_levels, level)
    Let level_error be Interpolation.get_level_error(hierarchy_levels, level)
    
    Display "  Level " joined with level joined with ": " joined with
        Interpolation.count_points(level_points) joined with " points, error=" joined with level_error

Note: Sparse grid interpolation (for high-dimensional problems)
Process called "multidimensional_function" that takes variables as Vector returns Real:
    Let x be Interpolation.get_vector_element(variables, 0)
    Let y be Interpolation.get_vector_element(variables, 1)
    Let z be Interpolation.get_vector_element(variables, 2)
    Return x * x + y * y + z * z

Let sparse_grid_interpolation be Interpolation.sparse_grid_interpolation(
    multidimensional_function,
    dimension: 3,
    level: 4,
    grid_type: "clenshaw_curtis"
)

Let sparse_grid_points_count be Interpolation.get_sparse_grid_size(sparse_grid_interpolation)
Let full_grid_equivalent be Interpolation.compute_equivalent_full_grid_size(sparse_grid_interpolation)

Display "Sparse grid points: " joined with sparse_grid_points_count
Display "Equivalent full grid size: " joined with full_grid_equivalent
Display "Sparse grid reduction factor: " joined with (full_grid_equivalent / sparse_grid_points_count)
```

### Moving Least Squares

```runa
Note: Moving least squares for scattered data approximation
Let mls_scattered_x be [0.0, 0.3, 0.7, 1.0, 1.4, 1.8, 2.2, 2.5]
Let mls_scattered_y be [0.1, 0.8, 1.2, 0.9, 1.7, 2.1, 1.8, 2.3]
Let mls_scattered_values be []

For i from 0 to (Interpolation.count_points(mls_scattered_x) - 1):
    Let x_val be Interpolation.get_element(mls_scattered_x, i)
    Let y_val be Interpolation.get_element(mls_scattered_y, i)
    Let function_val be x_val * x_val + 0.5 * y_val + MathFunctions.sin(3.14159 * x_val * y_val)
    Interpolation.append_to_list(mls_scattered_values, function_val)

Let mls_approximation be Interpolation.moving_least_squares_2d(
    mls_scattered_x,
    mls_scattered_y,
    mls_scattered_values,
    polynomial_degree: 2,
    support_radius: 0.5,
    weight_function: "gaussian"
)

Note: Evaluate MLS approximation and derivatives
Let mls_test_point be [1.2, 1.5]
Let mls_value be Interpolation.evaluate_mls_2d(mls_approximation, mls_test_point)
Let mls_gradient be Interpolation.evaluate_mls_gradient_2d(mls_approximation, mls_test_point)

Display "MLS approximation at (1.2, 1.5): " joined with mls_value
Display "MLS gradient: (" joined with Interpolation.get_gradient_x(mls_gradient)
    joined with ", " joined with Interpolation.get_gradient_y(mls_gradient) joined with ")"

Note: Partition of unity method
Let pou_approximation be Interpolation.partition_of_unity_method(
    mls_scattered_x,
    mls_scattered_y,
    mls_scattered_values,
    patch_radius: 0.8,
    local_approximation: "quadratic_polynomial",
    weight_function: "wendland_c2"
)

Let pou_value be Interpolation.evaluate_pou_2d(pou_approximation, mls_test_point)
Display "Partition of Unity approximation: " joined with pou_value
```

## Error Analysis and Validation

### Interpolation Error Bounds

```runa
Note: Theoretical error analysis for polynomial interpolation
Let error_analysis_function be "exponential"  Note: f(x) = e^x
Let error_analysis_interval be [0.0, 1.0]
Let error_analysis_points be [0.0, 0.25, 0.5, 0.75, 1.0]

Let theoretical_error_bound be Interpolation.compute_theoretical_error_bound(
    function_type: error_analysis_function,
    interpolation_points: error_analysis_points,
    evaluation_interval: error_analysis_interval,
    derivative_bound: MathFunctions.exp(1.0)  Note: max|f^(n+1)| on [0,1]
)

Let observed_error_analysis be Interpolation.empirical_error_analysis(
    target_function: "exponential",
    interpolation_points: error_analysis_points,
    test_points: 100,
    evaluation_interval: error_analysis_interval
)

Let theoretical_max_error be Interpolation.get_theoretical_max_error(theoretical_error_bound)
Let observed_max_error be Interpolation.get_observed_max_error(observed_error_analysis)

Display "Theoretical maximum error bound: " joined with theoretical_max_error
Display "Observed maximum error: " joined with observed_max_error
Display "Error bound effectiveness: " joined with (observed_max_error / theoretical_max_error)

Note: Convergence rate analysis
Let convergence_study be Interpolation.convergence_rate_study(
    target_function: "exponential",
    interpolation_interval: [0.0, 1.0],
    point_counts: [5, 9, 17, 33, 65],
    point_distribution: "chebyshev"
)

Let convergence_rates be Interpolation.get_convergence_rates(convergence_study)
Display "Convergence rates by polynomial degree:"
For degree from 4 to 64 step 4:
    Let rate be Interpolation.get_convergence_rate_for_degree(convergence_rates, degree)
    Display "  n=" joined with degree joined with ": rate=" joined with rate
```

### Cross-Validation and Model Selection

```runa
Note: Cross-validation for interpolation method selection
Let cv_data_x be []
Let cv_data_y be []

Note: Generate synthetic dataset
For i from 0 to 49:
    Let x_val be i / 49.0 * 2.0 * 3.14159
    Let y_val be MathFunctions.sin(x_val) + 0.1 * Interpolation.random_normal(0.0, 1.0)
    Interpolation.append_to_list(cv_data_x, x_val)
    Interpolation.append_to_list(cv_data_y, y_val)

Let interpolation_methods be [
    ("linear", []),
    ("cubic_spline", ["natural", "clamped"]),
    ("polynomial", [3, 5, 7, 9]),
    ("rbf", ["gaussian", "thin_plate_spline"])
]

Let cross_validation_results be Interpolation.k_fold_cross_validation(
    cv_data_x,
    cv_data_y,
    methods: interpolation_methods,
    k_folds: 5,
    error_metric: "rmse"
)

Display "Cross-validation results (RMSE):"
For method_result in cross_validation_results:
    Let method_name be Interpolation.get_method_name(method_result)
    Let cv_error be Interpolation.get_cv_error(method_result)
    Let cv_std be Interpolation.get_cv_standard_deviation(method_result)
    
    Display "  " joined with method_name joined with ": " joined with cv_error 
        joined with " ± " joined with cv_std

Let best_method be Interpolation.get_best_method(cross_validation_results)
Display "Best method by cross-validation: " joined with best_method

Note: Information criteria for model selection
Let information_criteria_analysis be Interpolation.information_criteria_analysis(
    cv_data_x,
    cv_data_y,
    polynomial_degrees: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    criteria: ["aic", "bic", "aicc"]
)

Let aic_best_degree be Interpolation.get_best_degree_by_criterion(information_criteria_analysis, "aic")
Let bic_best_degree be Interpolation.get_best_degree_by_criterion(information_criteria_analysis, "bic")

Display "Best polynomial degree (AIC): " joined with aic_best_degree
Display "Best polynomial degree (BIC): " joined with bic_best_degree
```

## Performance Optimization

### Computational Efficiency

```runa
Note: Performance comparison of interpolation methods
Let performance_test_sizes be [100, 500, 1000, 5000]
Let performance_methods be ["linear", "cubic_spline", "lagrange", "newton_divided_difference"]

Let performance_benchmark be Interpolation.benchmark_interpolation_methods(
    methods: performance_methods,
    data_sizes: performance_test_sizes,
    evaluation_points: 1000,
    repetitions: 10
)

Display "Performance benchmark results (average time in ms):"
For method in performance_methods:
    Display "Method: " joined with method
    For size in performance_test_sizes:
        Let construction_time be Interpolation.get_construction_time(performance_benchmark, method, size)
        Let evaluation_time be Interpolation.get_evaluation_time(performance_benchmark, method, size)
        
        Display "  n=" joined with size joined with ": construction=" joined with construction_time
            joined with "ms, evaluation=" joined with evaluation_time joined with "ms"

Note: Memory usage analysis
Let memory_analysis be Interpolation.analyze_memory_usage(
    methods: performance_methods,
    data_sizes: performance_test_sizes
)

For method in performance_methods:
    Let memory_complexity be Interpolation.get_memory_complexity(memory_analysis, method)
    Let memory_constant be Interpolation.get_memory_constant(memory_analysis, method)
    
    Display method joined with " memory usage: O(" joined with memory_complexity
        joined with "), constant=" joined with memory_constant
```

### Numerical Stability Optimization

```runa
Note: Stability-optimized interpolation
Let stability_test_data_x be [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
Let stability_test_data_y be []

Note: Create data with different condition numbers
For x_val in stability_test_data_x:
    Let y_val be 1.0 / (1.0 + 25.0 * (x_val - 0.5) * (x_val - 0.5))  Note: Runge function
    Interpolation.append_to_list(stability_test_data_y, y_val)

Let stability_comparison be Interpolation.compare_numerical_stability(
    stability_test_data_x,
    stability_test_data_y,
    methods: ["lagrange", "newton_barycentric", "chebyshev_barycentric"],
    perturbation_levels: [1e-14, 1e-12, 1e-10, 1e-8]
)

Display "Numerical stability comparison:"
For method in ["lagrange", "newton_barycentric", "chebyshev_barycentric"]:
    Let stability_measure be Interpolation.get_stability_measure(stability_comparison, method)
    Let condition_estimate be Interpolation.get_condition_estimate(stability_comparison, method)
    
    Display "  " joined with method joined with ": stability=" joined with stability_measure
        joined with ", condition=" joined with condition_estimate

Note: Stabilized polynomial evaluation
Let stabilized_evaluation be Interpolation.create_stabilized_evaluator(
    interpolation_points: stability_test_data_x,
    interpolation_values: stability_test_data_y,
    evaluation_method: "barycentric_with_scaling"
)

Let stability_improvement be Interpolation.measure_stability_improvement(
    standard_evaluator: lagrange_interpolant,
    stabilized_evaluator: stabilized_evaluation,
    test_points: 50,
    perturbation_level: 1e-12
)

Display "Stabilized evaluation improvement factor: " joined with stability_improvement
```

## Integration Examples

### With Numerical Differentiation

```runa
Import "math/engine/numerical/differentiation" as Differentiation

Note: Interpolation-based differentiation
Let derivative_test_data_x be [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
Let derivative_test_data_y be []

For x_val in derivative_test_data_x:
    Let y_val be MathFunctions.sin(3.14159 * x_val)
    Interpolation.append_to_list(derivative_test_data_y, y_val)

Let interpolation_for_derivatives be Interpolation.cubic_spline_interpolation(
    derivative_test_data_x,
    derivative_test_data_y,
    boundary_conditions: "natural"
)

Note: Compare interpolation-based derivatives with finite differences
Let comparison_points be [0.1, 0.3, 0.5, 0.7, 0.9]

Display "Derivative comparison:"
For test_x in comparison_points:
    Let spline_derivative be Interpolation.evaluate_derivative(interpolation_for_derivatives, test_x)
    Let finite_diff_derivative be Differentiation.finite_difference_derivative(
        function_data: [(test_x - 0.1, MathFunctions.sin(3.14159 * (test_x - 0.1))),
                       (test_x, MathFunctions.sin(3.14159 * test_x)),
                       (test_x + 0.1, MathFunctions.sin(3.14159 * (test_x + 0.1)))],
        point_index: 1,
        method: "central"
    )
    Let exact_derivative be 3.14159 * MathFunctions.cos(3.14159 * test_x)
    
    Display "x=" joined with test_x joined with ":"
    Display "  Spline: " joined with spline_derivative 
        joined with ", Error: " joined with Interpolation.abs(spline_derivative - exact_derivative)
    Display "  Finite diff: " joined with finite_diff_derivative
        joined with ", Error: " joined with Interpolation.abs(finite_diff_derivative - exact_derivative)
```

### With Optimization Problems

```runa
Import "math/engine/numerical/optimization" as Optimization

Note: Interpolation-based surrogate optimization
Process called "expensive_objective_function" that takes x as Real returns Real:
    Note: Simulate an expensive function evaluation
    Return -(x - 0.6) * (x - 0.6) + 0.8 + 0.1 * MathFunctions.sin(20.0 * x)

Note: Build initial surrogate model with few expensive evaluations
Let initial_sample_points be [0.0, 0.25, 0.5, 0.75, 1.0]
Let initial_function_values be []

For x_val in initial_sample_points:
    Let f_val be expensive_objective_function(x_val)
    Interpolation.append_to_list(initial_function_values, f_val)

Let surrogate_model be Interpolation.radial_basis_function_interpolation(
    initial_sample_points,
    [], Note: No y-coordinates for 1D problem  
    initial_function_values,
    rbf_type: "gaussian"
)

Note: Optimize surrogate model to find next evaluation point
Let surrogate_optimization be Optimization.maximize_scalar(
    function: "surrogate_model",
    bounds: [0.0, 1.0],
    method: "golden_section"
)

Let next_sample_point be Optimization.get_maximizer(surrogate_optimization)
Let next_function_value be expensive_objective_function(next_sample_point)

Display "Next sample point suggested by surrogate: " joined with next_sample_point
Display "Function value at suggested point: " joined with next_function_value

Note: Update surrogate model with new data
Let updated_sample_points be initial_sample_points
Interpolation.append_to_list(updated_sample_points, next_sample_point)
Let updated_function_values be initial_function_values
Interpolation.append_to_list(updated_function_values, next_function_value)

Let updated_surrogate be Interpolation.radial_basis_function_interpolation(
    updated_sample_points,
    [],
    updated_function_values,
    rbf_type: "gaussian"
)

Let surrogate_accuracy be Interpolation.validate_surrogate_model(
    updated_surrogate,
    expensive_objective_function,
    validation_points: 20,
    evaluation_interval: [0.0, 1.0]
)

Display "Updated surrogate model accuracy (RMSE): " joined with surrogate_accuracy
```

## Best Practices

### Method Selection Guidelines

```runa
Note: Decision tree for interpolation method selection
Let method_selector be Interpolation.create_method_selector([
    ("data_characteristics", [
        ("regularity", ["regular_grid", "irregular_scattered"]),
        ("dimensionality", [1, 2, 3, "high_dimensional"]),
        ("noise_level", ["noise_free", "low_noise", "high_noise"]),
        ("data_size", ["small", "medium", "large"])
    ]),
    ("requirements", [
        ("smoothness", ["c0", "c1", "c2", "c_infinity"]),
        ("derivative_evaluation", ["not_needed", "first_order", "higher_order"]),
        ("computational_efficiency", ["construction", "evaluation", "both"]),
        ("memory_constraints", ["unlimited", "limited", "severely_limited"])
    ])
])

Let method_recommendation be Interpolation.recommend_interpolation_method(
    method_selector,
    problem_characteristics: [
        ("regularity", "irregular_scattered"),
        ("dimensionality", 2),
        ("noise_level", "low_noise"),
        ("data_size", "medium"),
        ("smoothness", "c1"),
        ("derivative_evaluation", "first_order"),
        ("computational_efficiency", "evaluation"),
        ("memory_constraints", "limited")
    ]
)

Display "Method recommendation:"
Display Interpolation.format_recommendation(method_recommendation)
```

### Quality Assessment

```runa
Note: Comprehensive interpolation quality assessment
Let quality_assessor be Interpolation.create_quality_assessor([
    ("accuracy_metrics", ["max_error", "rms_error", "relative_error"]),
    ("smoothness_metrics", ["continuity_order", "derivative_bounds", "oscillation_measure"]),
    ("stability_metrics", ["condition_number", "perturbation_sensitivity"]),
    ("efficiency_metrics", ["construction_cost", "evaluation_cost", "memory_usage"])
])

Let quality_assessment be Interpolation.assess_interpolation_quality(
    quality_assessor,
    interpolation_method: cubic_spline,
    test_data: [cv_data_x, cv_data_y],
    reference_function: "sine_with_noise"
)

Display "Interpolation quality assessment:"
Let accuracy_score be Interpolation.get_accuracy_score(quality_assessment)
Let smoothness_score be Interpolation.get_smoothness_score(quality_assessment)
Let stability_score be Interpolation.get_stability_score(quality_assessment)
Let efficiency_score be Interpolation.get_efficiency_score(quality_assessment)

Display "  Accuracy score: " joined with accuracy_score joined with "/100"
Display "  Smoothness score: " joined with smoothness_score joined with "/100"  
Display "  Stability score: " joined with stability_score joined with "/100"
Display "  Efficiency score: " joined with efficiency_score joined with "/100"

Let overall_score be Interpolation.compute_overall_quality_score(quality_assessment)
Display "Overall quality score: " joined with overall_score joined with "/100"
```

The Interpolation and Approximation module provides comprehensive tools for fitting functions to data and constructing smooth approximations, enabling accurate data modeling, function reconstruction, and numerical analysis across diverse scientific and engineering applications.