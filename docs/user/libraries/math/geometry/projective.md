# Projective Geometry Module

The `math/geometry/projective` module provides comprehensive tools for projective geometry including homogeneous coordinates, projective transformations, cross-ratios, conics, and camera models. This module is essential for computer vision, computer graphics, perspective drawing, and advanced geometric analysis.

## Quick Start

```runa
Import "math/geometry/projective" as Projective
Import "math/geometry/euclidean" as Euclidean

Note: Work with homogeneous coordinates
Let euclidean_point be Euclidean.create_point([3, 4])
Let homogeneous_point be Projective.euclidean_to_homogeneous(euclidean_point)
Let back_to_euclidean be Projective.homogeneous_to_euclidean(homogeneous_point)

Display "Original point: " joined with Euclidean.point_to_string(euclidean_point)
Display "Homogeneous: " joined with Projective.homogeneous_to_string(homogeneous_point)
Display "Back to Euclidean: " joined with Euclidean.point_to_string(back_to_euclidean)

Note: Create perspective projection
Let projection_matrix be Projective.perspective_projection_matrix(
    fov: 60.0,
    aspect_ratio: 16.0/9.0,
    near_plane: 0.1,
    far_plane: 100.0
)

Let world_point be Euclidean.create_point([2, 3, -5])
Let screen_point be Projective.project_point(projection_matrix, world_point)
Display "Projected point: " joined with Euclidean.point_to_string(screen_point)
```

## Core Concepts

### Homogeneous Coordinates
Extended coordinate system that includes points at infinity and provides unified treatment of affine and projective transformations.

### Projective Transformations
Linear transformations in projective space that preserve incidence relations and cross-ratios.

### Cross-Ratios
Projectively invariant quantities that measure the harmonic relationship between four collinear points.

### Conics and Quadrics
Geometric objects that remain well-defined under projective transformation.

### Camera Models
Mathematical descriptions of how 3D scenes project to 2D images.

## API Reference

### Homogeneous Coordinates

#### Coordinate Conversion
```runa
Type called "HomogeneousPoint":
    coordinates as List[Real]
    dimension as Integer

Process called "euclidean_to_homogeneous" that takes point as Point returns HomogeneousPoint:
    Note: Convert Euclidean point to homogeneous coordinates

Process called "homogeneous_to_euclidean" that takes hpoint as HomogeneousPoint returns Point:
    Note: Convert homogeneous point to Euclidean coordinates

Process called "point_at_infinity" that takes direction as Vector returns HomogeneousPoint:
    Note: Create point at infinity in given direction

Process called "is_at_infinity" that takes hpoint as HomogeneousPoint returns Boolean:
    Note: Check if homogeneous point is at infinity
```

#### Homogeneous Operations
```runa
Process called "homogeneous_distance" that takes:
    hpoint1 as HomogeneousPoint,
    hpoint2 as HomogeneousPoint
returns Real:
    Note: Compute projective distance (may be infinite)

Process called "normalize_homogeneous" that takes hpoint as HomogeneousPoint returns HomogeneousPoint:
    Note: Normalize homogeneous coordinates (scale last coordinate to 1)

Process called "homogeneous_midpoint" that takes:
    hpoint1 as HomogeneousPoint,
    hpoint2 as HomogeneousPoint
returns HomogeneousPoint:
    Note: Compute midpoint in homogeneous coordinates
```

### Projective Transformations

#### Transformation Matrices
```runa
Type called "ProjectiveTransformation":
    matrix as Matrix
    dimension as Integer
    is_affine as Boolean

Process called "create_projective_transformation" that takes matrix as Matrix returns ProjectiveTransformation:
    Note: Create projective transformation from matrix

Process called "identity_transformation" that takes dimension as Integer returns ProjectiveTransformation:
    Note: Create identity transformation

Process called "translation" that takes vector as Vector returns ProjectiveTransformation:
    Note: Create translation transformation (affine)

Process called "rotation" that takes:
    angle as Real,
    axis as Vector,
    center as Point
returns ProjectiveTransformation:
    Note: Create rotation transformation

Process called "scaling" that takes:
    factors as List[Real],
    center as Point
returns ProjectiveTransformation:
    Note: Create scaling transformation

Process called "perspective_transform" that takes:
    vanishing_points as List[HomogeneousPoint]
returns ProjectiveTransformation:
    Note: Create perspective transformation
```

#### Transformation Operations
```runa
Process called "apply_transformation" that takes:
    transform as ProjectiveTransformation,
    point as HomogeneousPoint
returns HomogeneousPoint:
    Note: Apply projective transformation to point

Process called "compose_transformations" that takes:
    transform1 as ProjectiveTransformation,
    transform2 as ProjectiveTransformation
returns ProjectiveTransformation:
    Note: Compose two projective transformations

Process called "inverse_transformation" that takes transform as ProjectiveTransformation returns ProjectiveTransformation:
    Note: Compute inverse transformation

Process called "transformation_type" that takes transform as ProjectiveTransformation returns String:
    Note: Classify transformation (affine, similarity, isometry, etc.)
```

### Lines and Conics in Projective Space

#### Projective Lines
```runa
Type called "ProjectiveLine":
    coefficients as List[Real]  Note: ax + by + cz = 0
    dimension as Integer

Process called "line_through_points" that takes:
    point1 as HomogeneousPoint,
    point2 as HomogeneousPoint
returns ProjectiveLine:
    Note: Create line through two points

Process called "line_intersection" that takes:
    line1 as ProjectiveLine,
    line2 as ProjectiveLine
returns HomogeneousPoint:
    Note: Find intersection of two lines (always exists in projective plane)

Process called "point_on_line" that takes:
    point as HomogeneousPoint,
    line as ProjectiveLine
returns Boolean:
    Note: Check if point lies on line

Process called "line_at_infinity" that takes dimension as Integer returns ProjectiveLine:
    Note: Get line at infinity for given dimension
```

#### Conics
```runa
Type called "ProjectiveConic":
    matrix as Matrix  Note: 3x3 symmetric matrix for x^T * C * x = 0
    type as String    Note: "ellipse", "parabola", "hyperbola", "degenerate"

Process called "conic_through_five_points" that takes points as List[HomogeneousPoint] returns ProjectiveConic:
    Note: Create conic through five points (unique in projective plane)

Process called "point_on_conic" that takes:
    point as HomogeneousPoint,
    conic as ProjectiveConic
returns Boolean:
    Note: Check if point lies on conic

Process called "tangent_line_to_conic" that takes:
    point as HomogeneousPoint,
    conic as ProjectiveConic
returns ProjectiveLine:
    Note: Compute tangent line to conic at point

Process called "conic_intersection" that takes:
    conic1 as ProjectiveConic,
    conic2 as ProjectiveConic
returns List[HomogeneousPoint]:
    Note: Find intersection points of two conics (up to 4 points)

Process called "dual_conic" that takes conic as ProjectiveConic returns ProjectiveConic:
    Note: Compute dual conic (envelope of tangent lines)
```

### Cross-Ratios

#### Four-Point Cross-Ratio
```runa
Process called "cross_ratio" that takes:
    point1 as HomogeneousPoint,
    point2 as HomogeneousPoint,
    point3 as HomogeneousPoint,
    point4 as HomogeneousPoint
returns Complex:
    Note: Compute cross-ratio (z1,z2;z3,z4) = (z1-z3)(z2-z4)/((z1-z4)(z2-z3))

Process called "harmonic_conjugate" that takes:
    point1 as HomogeneousPoint,
    point2 as HomogeneousPoint,
    point3 as HomogeneousPoint
returns HomogeneousPoint:
    Note: Find harmonic conjugate D such that (A,B;C,D) = -1

Process called "is_harmonic_range" that takes:
    point1 as HomogeneousPoint,
    point2 as HomogeneousPoint,
    point3 as HomogeneousPoint,
    point4 as HomogeneousPoint
returns Boolean:
    Note: Check if four points form harmonic range
```

#### Cross-Ratio Invariance
```runa
Process called "verify_cross_ratio_invariance" that takes:
    points as List[HomogeneousPoint],
    transformation as ProjectiveTransformation
returns Boolean:
    Note: Verify cross-ratio is preserved under transformation

Process called "canonical_cross_ratio" that takes points as List[HomogeneousPoint] returns Complex:
    Note: Compute cross-ratio in canonical form
```

### Camera Models

#### Pinhole Camera
```runa
Type called "PinholeCamera":
    intrinsic_matrix as Matrix     Note: K matrix (focal length, principal point)
    extrinsic_matrix as Matrix     Note: [R|t] matrix (rotation and translation)
    projection_matrix as Matrix    Note: P = K[R|t] full projection matrix
    image_size as Tuple[Integer, Integer]

Process called "create_pinhole_camera" that takes:
    focal_length as Real,
    principal_point as Point,
    camera_position as Point,
    camera_orientation as Matrix,
    image_size as Tuple[Integer, Integer]
returns PinholeCamera:
    Note: Create pinhole camera model

Process called "project_world_to_image" that takes:
    camera as PinholeCamera,
    world_point as Point
returns Point:
    Note: Project 3D world point to 2D image coordinates

Process called "backproject_image_to_ray" that takes:
    camera as PinholeCamera,
    image_point as Point
returns Ray:
    Note: Backproject image point to 3D ray
```

#### Perspective Projection
```runa
Process called "perspective_projection_matrix" that takes:
    fov as Real,
    aspect_ratio as Real,
    near_plane as Real,
    far_plane as Real
returns Matrix:
    Note: Create perspective projection matrix for graphics pipeline

Process called "orthographic_projection_matrix" that takes:
    left as Real,
    right as Real,
    bottom as Real,
    top as Real,
    near as Real,
    far as Real
returns Matrix:
    Note: Create orthographic projection matrix

Process called "look_at_matrix" that takes:
    camera_position as Point,
    target_point as Point,
    up_vector as Vector
returns Matrix:
    Note: Create view transformation matrix
```

#### Camera Calibration
```runa
Process called "calibrate_camera" that takes:
    world_points as List[Point],
    image_points as List[Point]
returns PinholeCamera:
    Note: Calibrate camera from corresponding 3D-2D points

Process called "estimate_homography" that takes:
    source_points as List[Point],
    target_points as List[Point]
returns Matrix:
    Note: Estimate homography matrix between two planes

Process called "decompose_projection_matrix" that takes projection_matrix as Matrix returns Dictionary[String, Matrix]:
    Note: Decompose P = K[R|t] into intrinsic and extrinsic matrices
```

## Practical Examples

### Computer Vision Applications
```runa
Import "math/geometry/projective" as Projective
Import "math/geometry/euclidean" as Euclidean

Note: Camera calibration example
Let world_points be [
    Euclidean.create_point([0, 0, 0]),
    Euclidean.create_point([1, 0, 0]),
    Euclidean.create_point([0, 1, 0]),
    Euclidean.create_point([1, 1, 0]),
    Euclidean.create_point([0, 0, 1]),
    Euclidean.create_point([1, 0, 1]),
    Euclidean.create_point([0, 1, 1]),
    Euclidean.create_point([1, 1, 1])
]

Let observed_image_points be [
    Euclidean.create_point([320, 240]),
    Euclidean.create_point([420, 245]),
    Euclidean.create_point([315, 180]),
    Euclidean.create_point([415, 185]),
    Euclidean.create_point([350, 220]),
    Euclidean.create_point([450, 225]),
    Euclidean.create_point([345, 160]),
    Euclidean.create_point([445, 165])
]

Let calibrated_camera be Projective.calibrate_camera(world_points, observed_image_points)

Display "Camera calibration results:"
Display "  Focal length: " joined with calibrated_camera.intrinsic_matrix.entries[0][0]
Display "  Principal point: (" joined with calibrated_camera.intrinsic_matrix.entries[0][2] joined 
        with ", " joined with calibrated_camera.intrinsic_matrix.entries[1][2] joined with ")"

Note: Test projection accuracy
Let reprojection_errors be []
For i from 0 to world_points.length() - 1:
    Let projected be Projective.project_world_to_image(calibrated_camera, world_points[i])
    Let error be Euclidean.distance(projected, observed_image_points[i])
    reprojection_errors.append(error)

Let mean_error be Linear.sum(reprojection_errors) / reprojection_errors.length()
Display "Mean reprojection error: " joined with mean_error joined with " pixels"
```

### Homography and Perspective Correction
```runa
Note: Correct perspective distortion in image
Let distorted_corners be [
    Euclidean.create_point([120, 180]),
    Euclidean.create_point([520, 150]),
    Euclidean.create_point([580, 380]),
    Euclidean.create_point([80, 420])
]

Let target_corners be [
    Euclidean.create_point([0, 0]),
    Euclidean.create_point([400, 0]),
    Euclidean.create_point([400, 300]),
    Euclidean.create_point([0, 300])
]

Let homography be Projective.estimate_homography(distorted_corners, target_corners)

Display "Homography matrix:"
For i from 0 to 2:
    Let row_str be ""
    For j from 0 to 2:
        row_str be row_str joined with homography.entries[i][j] joined with " "
    Display "  [" joined with row_str joined with "]"

Note: Apply perspective correction to test points
Let test_points be [
    Euclidean.create_point([200, 250]),
    Euclidean.create_point([350, 200]),
    Euclidean.create_point([450, 320])
]

Display "Perspective correction results:"
For Each test_point in test_points:
    Let homogeneous_test be Projective.euclidean_to_homogeneous(test_point)
    Let transformed_homogeneous be Projective.apply_transformation(
        Projective.create_projective_transformation(homography),
        homogeneous_test
    )
    Let corrected_point be Projective.homogeneous_to_euclidean(transformed_homogeneous)
    
    Display "  " joined with Euclidean.point_to_string(test_point) joined 
            with " → " joined with Euclidean.point_to_string(corrected_point)
```

### Cross-Ratio and Harmonic Division
```runa
Note: Analyze harmonic division in perspective drawing
Let A be Projective.euclidean_to_homogeneous(Euclidean.create_point([0, 0]))
Let B be Projective.euclidean_to_homogeneous(Euclidean.create_point([4, 0]))
Let C be Projective.euclidean_to_homogeneous(Euclidean.create_point([1, 0]))

Note: Find harmonic conjugate D such that (A,B;C,D) = -1
Let D be Projective.harmonic_conjugate(A, B, C)

Display "Harmonic division:"
Display "  A: " joined with Projective.homogeneous_to_string(A)
Display "  B: " joined with Projective.homogeneous_to_string(B)
Display "  C: " joined with Projective.homogeneous_to_string(C)
Display "  D (harmonic conjugate): " joined with Projective.homogeneous_to_string(D)

Note: Verify cross-ratio is -1
Let cross_ratio_value be Projective.cross_ratio(A, B, C, D)
Display "Cross-ratio (A,B;C,D): " joined with cross_ratio_value
Display "Is harmonic range: " joined with Projective.is_harmonic_range(A, B, C, D)

Note: Test invariance under projection
Let perspective_transform be Projective.create_projective_transformation(
    Linear.create_matrix([
        [2, 0, 1],
        [0, 3, 2],
        [0, 0, 1]
    ])
)

Let A_transformed be Projective.apply_transformation(perspective_transform, A)
Let B_transformed be Projective.apply_transformation(perspective_transform, B)
Let C_transformed be Projective.apply_transformation(perspective_transform, C)
Let D_transformed be Projective.apply_transformation(perspective_transform, D)

Let transformed_cross_ratio be Projective.cross_ratio(
    A_transformed, B_transformed, C_transformed, D_transformed
)

Display "Cross-ratio after transformation: " joined with transformed_cross_ratio
Display "Cross-ratio preserved: " joined with (abs(cross_ratio_value - transformed_cross_ratio) < 1e-10)
```

### Conic Sections in Projective Plane
```runa
Note: Work with conics in projective geometry
Let five_points be [
    Projective.euclidean_to_homogeneous(Euclidean.create_point([1, 0])),
    Projective.euclidean_to_homogeneous(Euclidean.create_point([0, 1])),
    Projective.euclidean_to_homogeneous(Euclidean.create_point([-1, 0])),
    Projective.euclidean_to_homogeneous(Euclidean.create_point([0, -1])),
    Projective.euclidean_to_homogeneous(Euclidean.create_point([0.7, 0.7]))
]

Let conic be Projective.conic_through_five_points(five_points)

Display "Conic through five points created"
Display "Conic type: " joined with conic.type

Note: Find tangent lines at each point
Display "Tangent lines:"
For i from 0 to five_points.length() - 1:
    Let point be five_points[i]
    Let tangent be Projective.tangent_line_to_conic(point, conic)
    Display "  At point " joined with (i+1) joined with ": " joined with 
            tangent.coefficients[0] joined with "x + " joined with 
            tangent.coefficients[1] joined with "y + " joined with 
            tangent.coefficients[2] joined with "z = 0"

Note: Test pole-polar relationship
Let test_point be Projective.euclidean_to_homogeneous(Euclidean.create_point([2, 1]))
Let polar_line be Projective.polar_line(test_point, conic)
Let pole_of_line be Projective.pole_point(polar_line, conic)

Display "Pole-polar duality:"
Display "  Point: " joined with Projective.homogeneous_to_string(test_point)
Display "  Polar line: " joined with polar_line.coefficients
Display "  Pole of polar: " joined with Projective.homogeneous_to_string(pole_of_line)
```

### 3D Graphics Pipeline
```runa
Note: Complete 3D to 2D graphics pipeline
Let camera_position be Euclidean.create_point([5, 3, 8])
Let look_at_target be Euclidean.create_point([0, 0, 0])
Let up_vector be Linear.create_vector([0, 1, 0])

Note: Create view transformation
Let view_matrix be Projective.look_at_matrix(camera_position, look_at_target, up_vector)

Note: Create projection transformation
Let projection_matrix be Projective.perspective_projection_matrix(
    fov: 45.0,           Note: 45-degree field of view
    aspect_ratio: 1.33,  Note: 4:3 aspect ratio
    near_plane: 0.1,
    far_plane: 100.0
)

Note: Combine transformations
Let view_projection_matrix be Linear.matrix_multiplication(projection_matrix, view_matrix)

Note: Transform 3D objects
Let cube_vertices_3d be [
    Euclidean.create_point([-1, -1, -1]),
    Euclidean.create_point([1, -1, -1]),
    Euclidean.create_point([1, 1, -1]),
    Euclidean.create_point([-1, 1, -1]),
    Euclidean.create_point([-1, -1, 1]),
    Euclidean.create_point([1, -1, 1]),
    Euclidean.create_point([1, 1, 1]),
    Euclidean.create_point([-1, 1, 1])
]

Let screen_vertices be []
For Each vertex_3d in cube_vertices_3d:
    Note: Convert to homogeneous coordinates
    Let homogeneous_3d be Linear.create_vector([
        vertex_3d.coordinates[0],
        vertex_3d.coordinates[1],
        vertex_3d.coordinates[2],
        1.0
    ])
    
    Note: Apply view-projection transformation
    Let transformed_homogeneous be Linear.matrix_vector_multiply(view_projection_matrix, homogeneous_3d)
    
    Note: Perspective divide
    Let w be transformed_homogeneous.components[3]
    If abs(w) > 1e-6:
        Let screen_x be transformed_homogeneous.components[0] / w
        Let screen_y be transformed_homogeneous.components[1] / w
        Let screen_z be transformed_homogeneous.components[2] / w
        
        screen_vertices.append(Euclidean.create_point([screen_x, screen_y, screen_z]))
    Otherwise:
        Display "Warning: vertex at infinity"

Display "3D to 2D projection results:"
For i from 0 to screen_vertices.length() - 1:
    Display "  Vertex " joined with i joined with ": " joined with 
            Euclidean.point_to_string(screen_vertices[i])
```

## Advanced Features

### Projective Transformations Classification
```runa
Process called "classify_projective_transformation" that takes transform as ProjectiveTransformation returns Dictionary[String, Boolean]:
    Let matrix be transform.matrix
    
    Note: Check various properties
    Let is_translation be Projective.is_translation(matrix)
    Let is_rotation be Projective.is_rotation(matrix)
    Let is_scaling be Projective.is_scaling(matrix)
    Let is_similarity be Projective.is_similarity(matrix)
    Let is_affine be Projective.is_affine(matrix)
    Let is_perspective be not is_affine
    
    Note: Compute fixed points and lines
    Let fixed_points be Projective.compute_fixed_points(matrix)
    Let fixed_lines be Projective.compute_fixed_lines(matrix)
    
    Return Dictionary[String, Boolean]:
        "translation": is_translation
        "rotation": is_rotation
        "scaling": is_scaling
        "similarity": is_similarity
        "affine": is_affine
        "perspective": is_perspective
        "num_fixed_points": fixed_points.length()
        "num_fixed_lines": fixed_lines.length()
```

### Bundle Adjustment
```runa
Process called "bundle_adjustment" that takes:
    cameras as List[PinholeCamera],
    world_points as List[Point],
    observations as List[List[Point]]  Note: [camera][point] -> image point
returns Dictionary[String, Any]:
    Note: Simultaneously optimize camera parameters and 3D point positions
    
    Process called "reprojection_error_function" that takes parameters as List[Real] returns Real:
        Note: Compute total reprojection error for optimization
        
    Let initial_parameters be Projective.pack_bundle_parameters(cameras, world_points)
    Let optimized_parameters be Optimize.levenberg_marquardt(
        reprojection_error_function,
        initial_parameters,
        max_iterations: 100
    )
    
    Let optimized_cameras, optimized_points be Projective.unpack_bundle_parameters(optimized_parameters)
    
    Return Dictionary[String, Any]:
        "cameras": optimized_cameras
        "points": optimized_points
        "final_error": optimized_parameters.final_error
```

### Epipolar Geometry
```runa
Process called "compute_fundamental_matrix" that takes:
    points1 as List[Point],
    points2 as List[Point]
returns Matrix:
    Note: Compute fundamental matrix F such that p2^T * F * p1 = 0

Process called "compute_essential_matrix" that takes:
    fundamental_matrix as Matrix,
    camera1 as PinholeCamera,
    camera2 as PinholeCamera
returns Matrix:
    Note: Compute essential matrix E = K2^T * F * K1

Process called "epipolar_line" that takes:
    point as Point,
    fundamental_matrix as Matrix,
    image_index as Integer
returns ProjectiveLine:
    Note: Compute epipolar line corresponding to point in other image

Process called "triangulate_point" that takes:
    point1 as Point,
    point2 as Point,
    camera1 as PinholeCamera,
    camera2 as PinholeCamera
returns Point:
    Note: Triangulate 3D point from corresponding image points
```

### Projective Invariants
```runa
Process called "compute_projective_invariants" that takes:
    points as List[HomogeneousPoint],
    lines as List[ProjectiveLine]
returns Dictionary[String, Real]:
    Note: Compute quantities preserved under projective transformation
    
    Let cross_ratios be []
    If points.length() >= 4:
        For i from 0 to points.length() - 4:
            Let cr be Projective.cross_ratio(
                points[i], points[i+1], points[i+2], points[i+3]
            )
            cross_ratios.append(cr)
    
    Return Dictionary[String, Real]:
        "cross_ratios": cross_ratios
        "num_intersection_points": Projective.count_intersection_points(lines)
```

## Integration with Other Modules

### With Linear Algebra
```runa
Import "math/algebra/linear" as Linear
Import "math/geometry/projective" as Projective

Note: Use SVD for robust estimation
Process called "robust_homography_estimation" that takes:
    source_points as List[Point],
    target_points as List[Point]
returns Matrix:
    Note: Use SVD to solve homography estimation robustly
    
    Let A_matrix be []
    For i from 0 to source_points.length() - 1:
        Let x1 be source_points[i].coordinates[0]
        Let y1 be source_points[i].coordinates[1]
        Let x2 be target_points[i].coordinates[0]
        Let y2 be target_points[i].coordinates[1]
        
        A_matrix.append([x1, y1, 1, 0, 0, 0, -x2*x1, -x2*y1, -x2])
        A_matrix.append([0, 0, 0, x1, y1, 1, -y2*x1, -y2*y1, -y2])
    
    Let A be Linear.create_matrix(A_matrix)
    Let svd be Linear.singular_value_decomposition(A)
    
    Note: Solution is last column of V (smallest singular value)
    Let h_vector be svd["V"].get_column(8)
    Let homography be Linear.create_matrix([
        [h_vector[0], h_vector[1], h_vector[2]],
        [h_vector[3], h_vector[4], h_vector[5]],
        [h_vector[6], h_vector[7], h_vector[8]]
    ])
    
    Return homography
```

### With Optimization
```runa
Import "math/engine/optimization" as Optimize
Import "math/geometry/projective" as Projective

Note: Non-linear camera calibration refinement
Process called "refine_camera_calibration" that takes:
    initial_camera as PinholeCamera,
    world_points as List[Point],
    image_points as List[Point]
returns PinholeCamera:
    
    Process called "calibration_objective" that takes parameters as List[Real] returns Real:
        Let camera be Projective.unpack_camera_parameters(parameters)
        Let total_error be 0.0
        
        For i from 0 to world_points.length() - 1:
            Let projected be Projective.project_world_to_image(camera, world_points[i])
            Let error be Euclidean.distance_squared(projected, image_points[i])
            total_error += error
        
        Return total_error
    
    Let initial_parameters be Projective.pack_camera_parameters(initial_camera)
    Let optimized_parameters be Optimize.minimize(
        calibration_objective,
        initial_guess: initial_parameters,
        method: "bfgs"
    )
    
    Return Projective.unpack_camera_parameters(optimized_parameters.solution)
```

### With Computer Graphics
```runa
Import "math/graphics/rendering" as Rendering
Import "math/geometry/projective" as Projective

Note: Integrate projective geometry with graphics pipeline
Process called "perspective_correct_interpolation" that takes:
    screen_triangle as List[Point],
    world_triangle as List[Point],
    attributes as List[List[Real]],
    pixel_coord as Point
returns List[Real]:
    
    Note: Compute barycentric coordinates in screen space
    Let barycentric_screen be Rendering.barycentric_coordinates(pixel_coord, screen_triangle)
    
    Note: Convert to perspective-correct barycentric coordinates
    Let w_values be []
    For Each world_point in world_triangle:
        Let homogeneous be Projective.world_to_clip_coordinates(world_point)
        w_values.append(homogeneous.coordinates[3])
    
    Let corrected_barycentric be []
    Let total_weight be 0.0
    For i from 0 to 3:
        Let weight be barycentric_screen[i] / w_values[i]
        corrected_barycentric.append(weight)
        total_weight += weight
    
    Note: Normalize corrected barycentric coordinates
    For i from 0 to 3:
        corrected_barycentric[i] /= total_weight
    
    Note: Interpolate attributes using corrected coordinates
    Let interpolated_attributes be []
    For attr_index from 0 to attributes[0].length() - 1:
        Let interpolated_value be 0.0
        For vertex_index from 0 to 3:
            interpolated_value += corrected_barycentric[vertex_index] * attributes[vertex_index][attr_index]
        interpolated_attributes.append(interpolated_value)
    
    Return interpolated_attributes
```

## Applications in Art and Architecture

### Perspective Drawing
```runa
Note: Classical perspective construction
Process called "one_point_perspective" that takes:
    vanishing_point as Point,
    horizon_line as ProjectiveLine,
    objects as List[Polygon]
returns List[Polygon]:
    
    Let perspective_objects be []
    
    For Each object in objects:
        Let perspective_vertices be []
        For Each vertex in object.vertices:
            Note: Draw line from vertex to vanishing point
            Let perspective_line be Projective.line_through_points(
                Projective.euclidean_to_homogeneous(vertex),
                Projective.euclidean_to_homogeneous(vanishing_point)
            )
            
            Note: Intersect with appropriate depth plane
            Let depth_plane be Projective.create_line_at_depth(vertex.coordinates[2])
            Let perspective_vertex be Projective.line_intersection(perspective_line, depth_plane)
            
            perspective_vertices.append(Projective.homogeneous_to_euclidean(perspective_vertex))
        
        perspective_objects.append(Computational.create_polygon(perspective_vertices))
    
    Return perspective_objects

Display "One-point perspective transformation applied to " joined with objects.length() joined with " objects"
```

### Anamorphic Projections
```runa
Note: Create anamorphic art that appears correct from specific viewpoint
Process called "create_anamorphic_projection" that takes:
    original_image as ImageData,
    viewing_angle as Real,
    surface_plane as Plane
returns ImageData:
    
    Let anamorphic_transform be Projective.compute_anamorphic_transformation(
        viewing_angle,
        surface_plane
    )
    
    Return Projective.apply_transformation_to_image(original_image, anamorphic_transform)
```

## Best Practices

### Numerical Stability
```runa
Note: Handle numerical issues in homogeneous coordinates
Process called "robust_homogeneous_normalization" that takes hpoint as HomogeneousPoint returns HomogeneousPoint:
    Let max_coord be 0.0
    For Each coord in hpoint.coordinates:
        If abs(coord) > max_coord:
            max_coord be abs(coord)
    
    If max_coord < 1e-15:
        Display "Warning: near-zero homogeneous coordinates"
        Return hpoint
    
    Let normalized_coords be []
    For Each coord in hpoint.coordinates:
        normalized_coords.append(coord / max_coord)
    
    Return HomogeneousPoint:
        coordinates: normalized_coords
        dimension: hpoint.dimension

Process called "condition_number_check" that takes matrix as Matrix returns Boolean:
    Let condition_number be Linear.condition_number(matrix)
    If condition_number > 1e12:
        Display "Warning: ill-conditioned projection matrix"
        Return False
    Return True
```

### Degeneracy Handling
```runa
Note: Handle degenerate cases in projective geometry
Process called "safe_line_intersection" that takes:
    line1 as ProjectiveLine,
    line2 as ProjectiveLine
returns HomogeneousPoint:
    Let intersection be Projective.line_intersection(line1, line2)
    
    If Projective.is_at_infinity(intersection):
        Display "Lines are parallel - intersection at infinity"
        Return intersection
    
    If Linear.vector_magnitude(intersection.coordinates) < 1e-15:
        Display "Warning: degenerate intersection"
        Return null
    
    Return intersection
```

This module provides comprehensive tools for projective geometry, essential for computer vision, computer graphics, and mathematical applications requiring perspective and projective analysis.