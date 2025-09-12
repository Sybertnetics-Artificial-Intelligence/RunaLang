Note: Complex Analysis Module

## Overview

The `math/analysis/complex` module provides comprehensive complex analysis functionality, including holomorphic function theory, contour integration, residue calculations, power and Laurent series, conformal mappings, and Riemann surface theory. This module enables advanced complex mathematical analysis in Runa.

## Key Features

- **Holomorphic Functions**: Analytic function analysis and Cauchy-Riemann equations
- **Contour Integration**: Complex line integrals and Cauchy's theorems
- **Residue Theory**: Pole analysis and residue theorem applications
- **Power Series**: Complex power series and Laurent expansions
- **Conformal Mappings**: Angle-preserving transformations and Riemann mapping
- **Entire Functions**: Analysis of functions holomorphic on entire complex plane

## Data Types

### ComplexFunction
Represents a complex-valued function with analytical properties:
```runa
Type called "ComplexFunction":
    domain as Dictionary[String, String]           Note: Function domain
    codomain as Dictionary[String, String]         Note: Function codomain
    real_part as Dictionary[String, String]        Note: Real component u(x,y)
    imaginary_part as Dictionary[String, String]   Note: Imaginary component v(x,y)
    is_holomorphic as Boolean                      Note: Analyticity property
    is_entire as Boolean                           Note: Entire function property
    is_meromorphic as Boolean                      Note: Meromorphic property
    singularities as List[Dictionary[String, String]] Note: Singular points
    poles as List[Dictionary[String, String]]      Note: Pole locations
    branch_points as List[String]                  Note: Branch point locations
```

### ContourIntegral
Represents a complex contour integral:
```runa
Type called "ContourIntegral":
    integrand as ComplexFunction                   Note: Function to integrate
    contour as Dictionary[String, String]          Note: Integration path
    parametrization as Dictionary[String, String]  Note: Contour parametrization
    integral_value as String                       Note: Integral result
    residues as Dictionary[String, String]         Note: Residue values
    winding_number as Integer                      Note: Winding number
    is_closed as Boolean                           Note: Closed contour property
```

### PowerSeries
Represents a complex power series:
```runa
Type called "PowerSeries":
    coefficients as List[String]                   Note: Series coefficients
    center as String                               Note: Expansion center
    radius_of_convergence as String               Note: Convergence radius
    convergence_disk as Dictionary[String, String] Note: Convergence region
    is_entire as Boolean                           Note: Entire function property
    analytic_continuation as Dictionary[String, String] Note: Continuation data
```

### LaurentSeries
Represents a Laurent series expansion:
```runa
Type called "LaurentSeries":
    positive_coefficients as List[String]          Note: Non-negative powers
    negative_coefficients as List[String]          Note: Negative powers
    center as String                               Note: Expansion center
    annulus_of_convergence as Dictionary[String, String] Note: Convergence annulus
    principal_part as Dictionary[String, String]   Note: Principal part
    regular_part as Dictionary[String, String]     Note: Regular part
```

### ConformalMap
Represents a conformal (angle-preserving) mapping:
```runa
Type called "ConformalMap":
    domain as Dictionary[String, String]           Note: Source domain
    codomain as Dictionary[String, String]         Note: Target domain
    mapping_function as ComplexFunction            Note: Mapping function
    inverse_function as ComplexFunction            Note: Inverse mapping
    is_bijective as Boolean                        Note: Bijective property
    preserves_angles as Boolean                    Note: Conformality
    jacobian as Dictionary[String, String]         Note: Jacobian determinant
```

### RiemannSurface
Represents a Riemann surface:
```runa
Type called "RiemannSurface":
    base_space as Dictionary[String, String]       Note: Base topological space
    covering_map as Dictionary[String, String]     Note: Covering projection
    branch_points as List[String]                  Note: Branching points
    sheets as List[Dictionary[String, String]]     Note: Surface sheets
    genus as Integer                               Note: Topological genus
    fundamental_group as Dictionary[String, String] Note: Fundamental group
```

## Holomorphic Function Analysis

### Testing Holomorphicity
```runa
Import "math/analysis/complex" as ComplexAnalysis

Note: Create complex function f(z) = z²
Let quadratic_function be ComplexFunction with:
    domain: Dictionary with: "type": "disk", "center": "0+0i", "radius": "10"
    real_part: Dictionary with: "expression": "x^2 - y^2"
    imaginary_part: Dictionary with: "expression": "2*x*y"
    is_holomorphic: false  Note: Will be determined

Note: Test holomorphicity using Cauchy-Riemann equations
Let domain_region be Dictionary with: "type": "rectangle", "corners": ["-2-2i", "2+2i"]
Let holomorphic_test be ComplexAnalysis.test_holomorphicity(quadratic_function, domain_region)

Display "Function is holomorphic: " joined with String(holomorphic_test.is_holomorphic)
Display "Satisfies Cauchy-Riemann: " joined with String(holomorphic_test.cauchy_riemann_satisfied)
Display "Continuously differentiable: " joined with String(holomorphic_test.continuously_differentiable)

Note: Compute complex derivative
If holomorphic_test.is_holomorphic:
    Let derivative_result be ComplexAnalysis.complex_derivative(quadratic_function, "1+1i")
    Display "f'(1+i) = " joined with derivative_result.derivative_value
    Display "Derivative formula: " joined with derivative_result.derivative_expression
```

### Entire Function Analysis
```runa
Note: Analyze entire function e^z
Let exponential_function be ComplexFunction with:
    domain: Dictionary with: "type": "entire_plane"
    real_part: Dictionary with: "expression": "exp(x)*cos(y)"
    imaginary_part: Dictionary with: "expression": "exp(x)*sin(y)"
    is_entire: true
    is_holomorphic: true

Let entire_analysis be ComplexAnalysis.analyze_entire_function(exponential_function)
Display "Order of growth: " joined with entire_analysis.growth_order
Display "Type: " joined with entire_analysis.growth_type
Display "Maximum modulus: " joined with entire_analysis.maximum_modulus

Note: Liouville's theorem check
Let bounded_test be ComplexAnalysis.test_boundedness(exponential_function)
Display "Bounded entire function: " joined with String(bounded_test.is_bounded)
If bounded_test.is_bounded:
    Display "By Liouville's theorem: function is constant"
```

### Meromorphic Function Analysis
```runa
Note: Analyze rational function with poles
Let rational_function be ComplexFunction with:
    domain: Dictionary with: "type": "complex_plane_minus_poles"
    real_part: Dictionary with: "expression": "1/(x^2 + y^2)"
    imaginary_part: Dictionary with: "expression": "0"
    is_meromorphic: true
    poles: [Dictionary with: "location": "0+0i", "order": "1"]

Let meromorphic_analysis be ComplexAnalysis.analyze_meromorphic_function(rational_function)
Display "Number of poles: " joined with String(Length(meromorphic_analysis.pole_data))
Display "Pole orders: " joined with String(meromorphic_analysis.pole_orders)
Display "Essential singularities: " joined with String(Length(meromorphic_analysis.essential_singularities))

For Each pole in meromorphic_analysis.pole_data:
    Display "Pole at " joined with pole["location"] joined with " of order " joined with pole["order"]
```

## Contour Integration

### Basic Contour Integrals
```runa
Note: Integrate f(z) = 1/z around unit circle
Let reciprocal_function be ComplexFunction with:
    domain: Dictionary with: "type": "punctured_disk", "center": "0+0i", "radius": "2"
    real_part: Dictionary with: "expression": "x/(x^2 + y^2)"
    imaginary_part: Dictionary with: "expression": "-y/(x^2 + y^2)"

Let unit_circle_contour be Dictionary with:
    "type": "circle"
    "center": "0+0i"
    "radius": "1"
    "orientation": "counterclockwise"

Let contour_integral be ContourIntegral with:
    integrand: reciprocal_function
    contour: unit_circle_contour
    is_closed: true

Let integral_result be ComplexAnalysis.compute_contour_integral(contour_integral)
Display "∮ (1/z) dz = " joined with integral_result.integral_value
Display "Expected: 2πi = " joined with integral_result.theoretical_value
Display "Winding number: " joined with String(integral_result.winding_number)
```

### Cauchy's Theorem Applications
```runa
Note: Verify Cauchy's theorem for holomorphic function
Let holomorphic_func be ComplexFunction with:
    domain: Dictionary with: "type": "disk", "center": "0+0i", "radius": "5"
    real_part: Dictionary with: "expression": "x^3 - 3*x*y^2"
    imaginary_part: Dictionary with: "expression": "3*x^2*y - y^3"
    is_holomorphic: true

Let simple_contour be Dictionary with:
    "type": "rectangle"
    "vertices": ["-1-1i", "1-1i", "1+1i", "-1+1i"]
    "orientation": "counterclockwise"

Let cauchy_integral be ContourIntegral with:
    integrand: holomorphic_func
    contour: simple_contour
    is_closed: true

Let cauchy_result be ComplexAnalysis.apply_cauchy_theorem(cauchy_integral)
Display "Integral value: " joined with cauchy_result.integral_value
Display "Cauchy's theorem verification: " joined with String(cauchy_result.theorem_verified)
Display "Expected zero: " joined with String(cauchy_result.is_approximately_zero)
```

### Cauchy's Integral Formula
```runa
Note: Use Cauchy's integral formula to evaluate f(z₀)
Let polynomial_func be ComplexFunction with:
    domain: Dictionary with: "type": "entire_plane"
    real_part: Dictionary with: "expression": "x^2 - y^2 + 2*x - 1"
    imaginary_part: Dictionary with: "expression": "2*x*y + 2*y"
    is_holomorphic: true

Let evaluation_point be "1+1i"
Let surrounding_contour be Dictionary with:
    "type": "circle"
    "center": "1+1i"
    "radius": "0.5"
    "orientation": "counterclockwise"

Let cauchy_formula_result be ComplexAnalysis.cauchy_integral_formula(polynomial_func, evaluation_point, surrounding_contour)
Display "f(" joined with evaluation_point joined with ") = " joined with cauchy_formula_result.function_value
Display "Direct evaluation: " joined with cauchy_formula_result.direct_evaluation
Display "Integral formula result: " joined with cauchy_formula_result.integral_formula_value
Display "Values match: " joined with String(cauchy_formula_result.values_agree)
```

## Residue Theory

### Computing Residues
```runa
Note: Compute residue at simple pole
Let simple_pole_function be ComplexFunction with:
    poles: [Dictionary with: "location": "2+0i", "order": "1"]
    real_part: Dictionary with: "expression": "(x-2)/((x-2)^2 + y^2)"
    imaginary_part: Dictionary with: "expression": "-y/((x-2)^2 + y^2)"

Let pole_location be "2+0i"
Let residue_result be ComplexAnalysis.compute_residue(simple_pole_function, pole_location)
Display "Residue at z = " joined with pole_location joined with ": " joined with residue_result.residue_value
Display "Pole order: " joined with String(residue_result.pole_order)
Display "Computation method: " joined with residue_result.computation_method

Note: Compute residue at higher-order pole
Let higher_order_pole be ComplexFunction with:
    poles: [Dictionary with: "location": "0+0i", "order": "2"]
    real_part: Dictionary with: "expression": "1/(x^2 + y^2)^2"
    imaginary_part: Dictionary with: "expression": "0"

Let higher_residue = ComplexAnalysis.compute_residue(higher_order_pole, "0+0i")
Display "Residue at double pole: " joined with higher_residue.residue_value
Display "Used L'Hôpital rule: " joined with String(higher_residue.used_lhopital)
```

### Residue Theorem Applications
```runa
Note: Apply residue theorem for contour integration
Let rational_integrand be ComplexFunction with:
    poles: [
        Dictionary with: "location": "1+0i", "order": "1",
        Dictionary with: "location": "-1+0i", "order": "1"
    ]
    real_part: Dictionary with: "expression": "1/((x^2-1)^2 + y^2)"
    imaginary_part: Dictionary with: "expression": "0"

Let large_contour be Dictionary with:
    "type": "circle"
    "center": "0+0i"
    "radius": "3"
    "orientation": "counterclockwise"

Let residue_theorem_result be ComplexAnalysis.apply_residue_theorem(rational_integrand, large_contour)
Display "Sum of residues: " joined with residue_theorem_result.residue_sum
Display "Integral by residue theorem: " joined with residue_theorem_result.integral_value
Display "Individual residues:"
For Each residue_data in residue_theorem_result.individual_residues:
    Display "  At " joined with residue_data["location"] joined with ": " joined with residue_data["value"]

Note: Evaluate real integral using residues
Let real_integral_result be ComplexAnalysis.evaluate_real_integral_by_residues(
    "1/(1+x^4)", "-infinity", "infinity"
)
Display "∫_{-∞}^{∞} 1/(1+x⁴) dx = " joined with real_integral_result.integral_value
Display "Complex method verification: " joined with String(real_integral_result.method_verified)
```

## Power and Laurent Series

### Power Series Analysis
```runa
Note: Analyze geometric series
Let geometric_coefficients be ["1", "1", "1", "1", "1", "1"]
Let geometric_series be PowerSeries with:
    coefficients: geometric_coefficients
    center: "0+0i"
    radius_of_convergence: "1"

Let power_series_analysis be ComplexAnalysis.analyze_power_series(geometric_series)
Display "Radius of convergence: " joined with power_series_analysis.convergence_radius
Display "Convergence disk: |z| < " joined with power_series_analysis.convergence_radius
Display "Sum inside disk: " joined with power_series_analysis.sum_formula

Note: Find radius of convergence using ratio test
Let exponential_coefficients be ["1", "1", "0.5", "0.167", "0.042", "0.008"]
Let exp_series be PowerSeries with:
    coefficients: exponential_coefficients
    center: "0+0i"

Let convergence_analysis be ComplexAnalysis.find_radius_of_convergence(exp_series, "ratio_test")
Display "Ratio test radius: " joined with convergence_analysis.radius
Display "Root test radius: " joined with convergence_analysis.root_test_radius
Display "Method used: " joined with convergence_analysis.method
Display "Series represents: " joined with convergence_analysis.function_identification
```

### Laurent Series Expansion
```runa
Note: Expand function in Laurent series around singularity
Let laurent_function be ComplexFunction with:
    poles: [Dictionary with: "location": "0+0i", "order": "1"]
    real_part: Dictionary with: "expression": "(1 + x)/(x^2 + y^2)"
    imaginary_part: Dictionary with: "expression": "-y/(x^2 + y^2)"

Let expansion_center be "0+0i"
Let annulus_region be Dictionary with: "inner_radius": "0", "outer_radius": "1"

Let laurent_expansion be ComplexAnalysis.laurent_series_expansion(laurent_function, expansion_center, annulus_region)
Display "Principal part coefficients:"
For Each coeff, power in laurent_expansion.negative_coefficients:
    If coeff != "0":
        Display "  a_{" joined with String(power) joined with "} = " joined with coeff

Display "Regular part coefficients:"
For Each coeff, power in laurent_expansion.positive_coefficients:
    If coeff != "0":
        Display "  a_{" joined with String(power) joined with "} = " joined with coeff

Display "Residue (a_{-1}): " joined with laurent_expansion.residue
```

## Conformal Mappings

### Möbius Transformations
```runa
Note: Apply Möbius transformation
Let mobius_coefficients be Dictionary with:
    "a": "1"
    "b": "1"
    "c": "1"
    "d": "0"

Let mobius_map be ConformalMap with:
    domain: Dictionary with: "type": "extended_plane"
    mapping_function: ComplexFunction with:
        real_part: Dictionary with: "expression": "(x+1)/(x^2+y^2+1)"
        imaginary_part: Dictionary with: "expression": "y/(x^2+y^2+1)"

Let point_to_map be "1+1i"
Let mapped_point be ComplexAnalysis.apply_mobius_transformation(mobius_map, point_to_map)
Display "f(" joined with point_to_map joined with ") = " joined with mapped_point.mapped_value
Display "Transformation preserves angles: " joined with String(mapped_point.preserves_angles)

Note: Find transformation mapping three points
Let source_points be ["0+0i", "1+0i", "0+1i"]
Let target_points be ["1+0i", "-1+0i", "0+1i"]
Let determined_mobius be ComplexAnalysis.determine_mobius_transformation(source_points, target_points)
Display "Determined transformation coefficients:"
Display "  a = " joined with determined_mobius.coefficients["a"]
Display "  b = " joined with determined_mobius.coefficients["b"]  
Display "  c = " joined with determined_mobius.coefficients["c"]
Display "  d = " joined with determined_mobius.coefficients["d"]
```

### Riemann Mapping Theorem
```runa
Note: Find conformal mapping from unit disk to upper half-plane
Let unit_disk = Dictionary with: "type": "disk", "center": "0+0i", "radius": "1"
Let upper_half_plane = Dictionary with: "type": "half_plane", "boundary": "real_axis", "side": "upper"

Let riemann_mapping = ComplexAnalysis.construct_riemann_mapping(unit_disk, upper_half_plane)
Display "Mapping function: " joined with riemann_mapping.mapping_formula
Display "Is conformal: " joined with String(riemann_mapping.is_conformal)
Display "Is bijective: " joined with String(riemann_mapping.is_bijective)

Note: Test conformality by checking angle preservation
Let test_angle = "π/4"
Let angle_preservation_test = ComplexAnalysis.test_angle_preservation(riemann_mapping, "0.5+0.5i", test_angle)
Display "Original angle: " joined with test_angle
Display "Mapped angle: " joined with angle_preservation_test.mapped_angle
Display "Angle preserved: " joined with String(angle_preservation_test.angle_preserved)
```

### Schwarz-Christoffel Mapping
```runa
Note: Map upper half-plane to polygon
Let polygon_vertices = ["0+0i", "1+0i", "1+1i", "0+1i"]  Note: Unit square
Let interior_angles = ["π/2", "π/2", "π/2", "π/2"]

Let schwarz_christoffel = ComplexAnalysis.schwarz_christoffel_mapping(upper_half_plane, polygon_vertices, interior_angles)
Display "Mapping parameters:"
Display "  Prevertices: " joined with String(schwarz_christoffel.prevertices)
Display "  Scaling factor: " joined with schwarz_christoffel.scaling_factor
Display "  Translation: " joined with schwarz_christoffel.translation
Display "Mapping formula: " joined with schwarz_christoffel.mapping_expression
```

## Riemann Surfaces

### Constructing Riemann Surfaces
```runa
Note: Create Riemann surface for sqrt(z)
Let sqrt_branch_points = ["0+0i"]
Let sqrt_surface be RiemannSurface with:
    branch_points: sqrt_branch_points
    sheets: [
        Dictionary with: "sheet": "0", "description": "principal branch",
        Dictionary with: "sheet": "1", "description": "secondary branch"
    ]
    genus: 0

Let surface_construction = ComplexAnalysis.construct_riemann_surface(sqrt_surface, "sqrt(z)")
Display "Number of sheets: " joined with String(Length(surface_construction.sheet_data))
Display "Branch points: " joined with String(Length(surface_construction.branch_points))
Display "Genus: " joined with String(surface_construction.genus)

Note: Analyze covering properties  
Let covering_analysis = ComplexAnalysis.analyze_covering_map(sqrt_surface)
Display "Covering degree: " joined with String(covering_analysis.covering_degree)
Display "Ramification points: " joined with String(covering_analysis.ramification_points)
```

### Algebraic Function Theory
```runa
Note: Study algebraic function w² = z³ - z
Let algebraic_relation = Dictionary with:
    "equation": "w^2 = z^3 - z"
    "variables": ["z", "w"]
    "degree": "2"

Let algebraic_surface = ComplexAnalysis.construct_algebraic_riemann_surface(algebraic_relation)
Display "Algebraic equation: " joined with algebraic_surface.defining_equation
Display "Genus: " joined with String(algebraic_surface.genus)
Display "Branch points: " joined with String(algebraic_surface.branch_points)

Note: Compute genus using Riemann-Hurwitz formula
Let genus_calculation = ComplexAnalysis.compute_genus_riemann_hurwitz(algebraic_surface)
Display "Genus by Riemann-Hurwitz: " joined with String(genus_calculation.genus)
Display "Ramification data: " joined with String(genus_calculation.ramification_data)
```

## Advanced Topics

### Maximum Principle
```runa
Note: Apply maximum modulus principle
Let bounded_domain = Dictionary with: "type": "disk", "center": "0+0i", "radius": "2"
Let harmonic_function = ComplexFunction with:
    domain: bounded_domain
    real_part: Dictionary with: "expression": "x^2 - y^2"
    is_holomorphic: true

Let maximum_principle_result = ComplexAnalysis.apply_maximum_principle(harmonic_function, bounded_domain)
Display "Maximum on boundary: " joined with String(maximum_principle_result.maximum_on_boundary)
Display "Maximum value: " joined with maximum_principle_result.maximum_value
Display "Maximum location: " joined with maximum_principle_result.maximum_location
Display "Interior critical points: " joined with String(Length(maximum_principle_result.interior_critical_points))
```

### Argument Principle
```runa
Note: Count zeros and poles using argument principle
Let rational_function = ComplexFunction with:
    poles: [Dictionary with: "location": "1+0i", "order": "1"]
    real_part: Dictionary with: "expression": "(x-1)/((x-1)^2 + y^2)"
    imaginary_part: Dictionary with: "expression": "-y/((x-1)^2 + y^2)"

Let enclosing_contour = Dictionary with:
    "type": "circle"
    "center": "0+0i"  
    "radius": "3"

Let argument_result = ComplexAnalysis.apply_argument_principle(rational_function, enclosing_contour)
Display "Number of zeros: " joined with String(argument_result.zero_count)
Display "Number of poles: " joined with String(argument_result.pole_count)
Display "Net change in argument: " joined with argument_result.argument_change
Display "Winding number: " joined with String(argument_result.winding_number)
```

## Error Handling

### Domain and Analyticity Errors
```runa
Try:
    Note: Invalid domain for holomorphic function
    Let invalid_domain = Dictionary with: "type": "disconnected_region"
    Let test_function = ComplexFunction with: domain: invalid_domain
    
    Let holomorphic_test = ComplexAnalysis.test_holomorphicity(test_function, invalid_domain)
Catch Errors.DomainError as error:
    Display "Domain error: " joined with error.message
    Display "Holomorphic functions require connected domains"

Try:
    Note: Contour integration with branch cut crossing
    Let branch_function = ComplexFunction with:
        branch_points: ["0+0i"]
        real_part: Dictionary with: "expression": "sqrt(x^2 + y^2) * cos(atan2(y,x)/2)"
    
    Let crossing_contour = Dictionary with: "crosses_branch_cut": true
    Let integral_result = ComplexAnalysis.compute_contour_integral_with_branch_cuts(branch_function, crossing_contour)
Catch Errors.BranchCutError as error:
    Display "Branch cut error: " joined with error.message
    Display "Contour crosses branch cut - result depends on sheet choice"
```

### Convergence and Singularity Errors
```runa
Try:
    Note: Power series outside radius of convergence
    Let divergent_point = "2+0i"
    Let unit_disk_series = PowerSeries with:
        center: "0+0i"
        radius_of_convergence: "1"
    
    Let evaluation_result = ComplexAnalysis.evaluate_power_series(unit_disk_series, divergent_point)
Catch Errors.ConvergenceError as error:
    Display "Convergence error: " joined with error.message
    Display "Point lies outside convergence disk"
    Display "Use analytic continuation instead"
```

## Performance Considerations

- **Holomorphicity Testing**: Cache Cauchy-Riemann computations for repeated evaluations
- **Contour Integration**: Use adaptive quadrature for complex integrals
- **Series Expansions**: Precompute coefficients for frequently used series
- **Conformal Mappings**: Use lookup tables for standard transformations

## Best Practices

1. **Domain Verification**: Always verify function domains before complex analysis
2. **Branch Cut Handling**: Carefully manage branch cuts in multi-valued functions
3. **Convergence Testing**: Check series convergence before evaluation
4. **Residue Computation**: Use appropriate methods based on pole order
5. **Contour Selection**: Choose integration paths to avoid singularities
6. **Numerical Stability**: Use high precision for sensitive calculations

## Related Documentation

- **[Math Analysis Real](real.md)**: Real analysis and foundational concepts  
- **[Math Core Operations](../core/operations.md)**: Complex number arithmetic
- **[Math Engine Numerical](../engine/numerical/README.md)**: Numerical methods
- **[Math Analysis Harmonic](harmonic.md)**: Fourier analysis and harmonic functions