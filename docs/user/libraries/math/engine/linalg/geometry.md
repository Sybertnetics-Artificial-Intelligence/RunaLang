# Computational Geometry

The Computational Geometry module (`math/engine/linalg/geometry`) provides geometric linear algebra operations essential for computer graphics, robotics, computer vision, and geometric computing. This module implements efficient algorithms for transformations, projections, coordinate systems, and geometric computations using linear algebra foundations.

## Quick Start

```runa
Import "math/engine/linalg/geometry" as Geometry
Import "math/engine/linalg/core" as LinAlg
Import "math/core/constants" as Constants

Note: 2D geometric transformations
Let point_2d be Geometry.create_point_2d(3.0, 4.0)
Let angle be Constants.get_pi() / 4  Note: 45 degrees

Note: Basic 2D transformations
Let rotation_matrix be Geometry.create_rotation_matrix_2d(angle)
Let translation_matrix be Geometry.create_translation_matrix_2d(2.0, 1.0)
Let scale_matrix be Geometry.create_scale_matrix_2d(1.5, 0.8)

Let rotated_point be Geometry.transform_point_2d(rotation_matrix, point_2d)
Let translated_point be Geometry.transform_point_2d(translation_matrix, point_2d)

Display "Original point: " joined with Geometry.point_to_string(point_2d)
Display "Rotated point: " joined with Geometry.point_to_string(rotated_point)

Note: 3D transformations
Let point_3d be Geometry.create_point_3d(1.0, 2.0, 3.0)
Let axis_vector be Geometry.normalize_vector_3d([1.0, 1.0, 0.0])
Let rotation_3d be Geometry.create_rotation_matrix_3d_axis_angle(axis_vector, angle)

Let rotated_3d be Geometry.transform_point_3d(rotation_3d, point_3d)
Display "3D rotated point: " joined with Geometry.point_to_string(rotated_3d)

Note: Homogeneous coordinates
Let homogeneous_point be Geometry.to_homogeneous_2d(point_2d)
Let combined_transform be LinAlg.matrix_multiply(translation_matrix, rotation_matrix)
let transformed_homogeneous be LinAlg.matrix_vector_multiply(combined_transform, homogeneous_point)
Let final_cartesian be Geometry.from_homogeneous_2d(transformed_homogeneous)

Display "Combined transformation result: " joined with Geometry.point_to_string(final_cartesian)
```

## 2D Geometric Transformations

### Basic 2D Transformations

```runa
Note: Rotation transformations
Let rotation_30_deg be Geometry.create_rotation_matrix_2d(Constants.get_pi() / 6)
Let rotation_90_deg be Geometry.create_rotation_matrix_2d(Constants.get_pi() / 2)
Let rotation_180_deg be Geometry.create_rotation_matrix_2d(Constants.get_pi())

Note: Translation transformations
Let translate_right be Geometry.create_translation_matrix_2d(5.0, 0.0)
Let translate_up be Geometry.create_translation_matrix_2d(0.0, 3.0)
Let translate_diagonal be Geometry.create_translation_matrix_2d(2.0, 2.0)

Note: Scale transformations
Let uniform_scale be Geometry.create_scale_matrix_2d(2.0, 2.0)
Let non_uniform_scale be Geometry.create_scale_matrix_2d(3.0, 0.5)
Let reflection_x be Geometry.create_scale_matrix_2d(1.0, -1.0)
Let reflection_y be Geometry.create_scale_matrix_2d(-1.0, 1.0)

Note: Shear transformations
Let shear_x be Geometry.create_shear_matrix_2d(0.5, 0.0)
Let shear_y be Geometry.create_shear_matrix_2d(0.0, 0.3)
Let shear_both be Geometry.create_shear_matrix_2d(0.2, 0.4)

Note: Test transformations on a set of points
Let test_points be [
    Geometry.create_point_2d(0.0, 0.0),
    Geometry.create_point_2d(1.0, 0.0),
    Geometry.create_point_2d(1.0, 1.0),
    Geometry.create_point_2d(0.0, 1.0)
]

Let transformed_points be Geometry.transform_points_2d(rotation_30_deg, test_points)

For i from 0 to 3:
    Let original be LinAlg.get_element(test_points, i)
    Let transformed be LinAlg.get_element(transformed_points, i)
    Display "Point " joined with i joined with ": " joined with Geometry.point_to_string(original) 
        joined with " -> " joined with Geometry.point_to_string(transformed)
```

### Composite Transformations

```runa
Note: Build complex transformations by composition
Let transform_sequence be Geometry.create_transformation_sequence_2d()

Geometry.add_rotation(transform_sequence, Constants.get_pi() / 4)
Geometry.add_translation(transform_sequence, 2.0, 1.0)
Geometry.add_scale(transform_sequence, 1.5, 1.5)
Geometry.add_rotation(transform_sequence, -Constants.get_pi() / 8)

Let composite_matrix be Geometry.compose_transformations_2d(transform_sequence)

Note: Apply transformation hierarchy
Let local_transform be Geometry.create_rotation_matrix_2d(Constants.get_pi() / 6)
Let parent_transform be Geometry.create_translation_matrix_2d(5.0, 3.0)
Let world_transform be Geometry.combine_transforms_2d(parent_transform, local_transform)

Let test_point be Geometry.create_point_2d(1.0, 0.0)
Let world_point be Geometry.transform_point_2d(world_transform, test_point)

Display "Local to world transformation: " joined with Geometry.point_to_string(world_point)

Note: Inverse transformations
Let inverse_rotation be Geometry.inverse_rotation_2d(rotation_30_deg)
Let inverse_translation be Geometry.inverse_translation_2d(translate_right)
Let inverse_composite be Geometry.inverse_transformation_2d(composite_matrix)

Let round_trip_point be Geometry.transform_point_2d(inverse_composite, 
    Geometry.transform_point_2d(composite_matrix, test_point))

Let round_trip_error be Geometry.distance_2d(test_point, round_trip_point)
Display "Round-trip transformation error: " joined with round_trip_error
```

## 3D Geometric Transformations

### 3D Rotation Representations

```runa
Note: Euler angles (XYZ convention)
Let euler_x be Constants.get_pi() / 6  Note: 30 degrees
Let euler_y be Constants.get_pi() / 4  Note: 45 degrees  
Let euler_z be Constants.get_pi() / 3  Note: 60 degrees

Let rotation_from_euler be Geometry.create_rotation_matrix_3d_euler(euler_x, euler_y, euler_z, "xyz")

Note: Axis-angle representation
Let rotation_axis be Geometry.normalize_vector_3d([1.0, 2.0, 1.0])
Let rotation_angle be Constants.get_pi() / 3

Let rotation_from_axis_angle be Geometry.create_rotation_matrix_3d_axis_angle(rotation_axis, rotation_angle)

Note: Quaternion representation
Let quaternion be Geometry.create_quaternion_from_axis_angle(rotation_axis, rotation_angle)
Let rotation_from_quaternion be Geometry.quaternion_to_rotation_matrix(quaternion)

Note: Verify equivalence of representations
Let axis_angle_euler be Geometry.rotation_matrix_to_euler(rotation_from_axis_angle, "xyz")
Let quaternion_axis_angle be Geometry.quaternion_to_axis_angle(quaternion)

Display "Axis-angle converted to Euler: " joined with LinAlg.vector_to_string(axis_angle_euler)

Note: Quaternion operations
Let quaternion_a be Geometry.create_quaternion(0.7071, 0.0, 0.7071, 0.0)
Let quaternion_b be Geometry.create_quaternion(0.8660, 0.0, 0.0, 0.5)

Let quaternion_product be Geometry.quaternion_multiply(quaternion_a, quaternion_b)
Let quaternion_conjugate be Geometry.quaternion_conjugate(quaternion_a)
Let quaternion_norm be Geometry.quaternion_norm(quaternion_a)
Let quaternion_normalized be Geometry.quaternion_normalize(quaternion_a)

Display "Quaternion norm: " joined with quaternion_norm
```

### 3D Transformations and Coordinate Systems

```runa
Note: 3D transformations
Let translation_3d be Geometry.create_translation_matrix_3d(2.0, 3.0, 1.0)
Let scale_3d be Geometry.create_scale_matrix_3d(2.0, 1.5, 0.8)

Note: Look-at transformation for camera positioning
Let camera_position be Geometry.create_point_3d(5.0, 5.0, 5.0)
Let target_position be Geometry.create_point_3d(0.0, 0.0, 0.0)  
Let up_vector be Geometry.create_vector_3d(0.0, 1.0, 0.0)

Let look_at_matrix be Geometry.create_look_at_matrix(camera_position, target_position, up_vector)

Note: Create view frustum and projection matrices
Let perspective_matrix be Geometry.create_perspective_matrix(
    field_of_view: Constants.get_pi() / 4,
    aspect_ratio: 16.0 / 9.0,
    near_plane: 0.1,
    far_plane: 100.0
)

Let orthographic_matrix be Geometry.create_orthographic_matrix(
    left: -5.0,
    right: 5.0,
    bottom: -5.0,
    top: 5.0,
    near: 0.1,
    far: 100.0
)

Note: Transform point through full graphics pipeline
Let model_matrix be LinAlg.matrix_multiply(translation_3d, scale_3d)
Let view_matrix be look_at_matrix
Let projection_matrix be perspective_matrix

Let mvp_matrix be LinAlg.matrix_multiply(projection_matrix,
    LinAlg.matrix_multiply(view_matrix, model_matrix))

Let world_point be Geometry.create_point_3d(1.0, 1.0, 1.0)
Let clip_space_point be Geometry.transform_point_3d_homogeneous(mvp_matrix, world_point)
Let ndc_point be Geometry.perspective_divide(clip_space_point)

Display "NDC coordinates: " joined with Geometry.point_to_string(ndc_point)
```

## Coordinate System Transformations

### 2D Coordinate Systems

```runa
Note: Cartesian to polar coordinates
Let cartesian_point be Geometry.create_point_2d(3.0, 4.0)
Let polar_coords be Geometry.cartesian_to_polar(cartesian_point)
Let radius be Geometry.get_polar_radius(polar_coords)
Let theta be Geometry.get_polar_angle(polar_coords)

Display "Polar coordinates: r=" joined with radius joined with ", θ=" joined with theta

Note: Polar to Cartesian coordinates
Let polar_point be Geometry.create_polar_point(5.0, Constants.get_pi() / 3)
Let cartesian_from_polar be Geometry.polar_to_cartesian(polar_point)

Display "Cartesian from polar: " joined with Geometry.point_to_string(cartesian_from_polar)

Note: Complex number representation
Let complex_point be Geometry.cartesian_to_complex(cartesian_point)
Let complex_magnitude be Geometry.complex_magnitude(complex_point)
Let complex_phase be Geometry.complex_phase(complex_point)

Note: Affine coordinate transformations
Let source_triangle be [
    Geometry.create_point_2d(0.0, 0.0),
    Geometry.create_point_2d(1.0, 0.0),
    Geometry.create_point_2d(0.0, 1.0)
]

Let target_triangle be [
    Geometry.create_point_2d(1.0, 1.0),
    Geometry.create_point_2d(3.0, 2.0),
    Geometry.create_point_2d(2.0, 4.0)
]

Let affine_transform be Geometry.compute_affine_transform_2d(source_triangle, target_triangle)
```

### 3D Coordinate Systems

```runa
Note: Cartesian to spherical coordinates
Let cartesian_3d be Geometry.create_point_3d(2.0, 3.0, 6.0)
Let spherical_coords be Geometry.cartesian_to_spherical(cartesian_3d)

Let spherical_radius be Geometry.get_spherical_radius(spherical_coords)
Let spherical_theta be Geometry.get_spherical_theta(spherical_coords)  Note: Azimuth
Let spherical_phi be Geometry.get_spherical_phi(spherical_coords)    Note: Polar angle

Display "Spherical: r=" joined with spherical_radius 
    joined with ", θ=" joined with spherical_theta 
    joined with ", φ=" joined with spherical_phi

Note: Cylindrical coordinates
Let cylindrical_coords be Geometry.cartesian_to_cylindrical(cartesian_3d)
Let cylindrical_rho be Geometry.get_cylindrical_rho(cylindrical_coords)
Let cylindrical_phi be Geometry.get_cylindrical_phi(cylindrical_coords)
Let cylindrical_z be Geometry.get_cylindrical_z(cylindrical_coords)

Note: Geographic coordinate systems
Let geodetic_point be Geometry.create_geodetic_point(
    latitude: 40.7128,   Note: New York City
    longitude: -74.0060,
    altitude: 10.0
)

Let ecef_coordinates be Geometry.geodetic_to_ecef(geodetic_point, "wgs84")
Let local_enu be Geometry.ecef_to_enu(ecef_coordinates, reference_point)

Display "ECEF coordinates: " joined with Geometry.point_to_string(ecef_coordinates)
```

## Projections and Camera Models

### Geometric Projections

```runa
Note: Parallel projection
Let parallel_projection_matrix be Geometry.create_parallel_projection(
    projection_direction: Geometry.normalize_vector_3d([1.0, 1.0, 1.0]),
    plane_normal: Geometry.create_vector_3d(0.0, 0.0, 1.0)
)

Note: Central projection (perspective)
Let projection_center be Geometry.create_point_3d(0.0, 0.0, 5.0)
Let image_plane_distance be 1.0

Let central_projection_matrix be Geometry.create_central_projection(
    projection_center,
    image_plane_distance
)

Note: Stereographic projection for sphere mapping
Let sphere_point be Geometry.create_point_3d(0.5, 0.5, 0.7071)  Note: Point on unit sphere
Let stereographic_projection be Geometry.stereographic_projection(sphere_point, "north_pole")

Display "Stereographic projection: " joined with Geometry.point_to_string(stereographic_projection)

Note: Map projections for geographic data
Let mercator_projection be Geometry.geographic_to_mercator(geodetic_point)
Let equirectangular_projection be Geometry.geographic_to_equirectangular(geodetic_point)

Note: Projective transformations
Let source_quad be [
    Geometry.create_point_2d(0.0, 0.0),
    Geometry.create_point_2d(1.0, 0.0),
    Geometry.create_point_2d(1.0, 1.0),
    Geometry.create_point_2d(0.0, 1.0)
]

Let target_quad be [
    Geometry.create_point_2d(0.1, 0.1),
    Geometry.create_point_2d(0.9, 0.2),
    Geometry.create_point_2d(0.8, 0.8),
    Geometry.create_point_2d(0.2, 0.7)
]

Let homography_matrix be Geometry.compute_homography(source_quad, target_quad)
```

### Camera Calibration and Models

```runa
Note: Pinhole camera model
Let camera_intrinsics be Geometry.create_camera_intrinsics(
    focal_length_x: 800.0,
    focal_length_y: 800.0,
    principal_point_x: 320.0,
    principal_point_y: 240.0,
    skew: 0.0
)

Let camera_extrinsics be Geometry.create_camera_extrinsics(
    rotation_matrix: rotation_from_euler,
    translation_vector: Geometry.create_vector_3d(1.0, 2.0, 3.0)
)

Let camera_matrix be Geometry.compute_camera_matrix(camera_intrinsics, camera_extrinsics)

Note: Project 3D point to image coordinates
Let world_point_3d be Geometry.create_point_3d(2.0, 3.0, 5.0)
Let image_coordinates be Geometry.project_point_to_image(camera_matrix, world_point_3d)

Display "Image coordinates: " joined with Geometry.point_to_string(image_coordinates)

Note: Distortion models
Let radial_distortion_coeffs be [0.1, -0.05, 0.01]
Let tangential_distortion_coeffs be [0.001, -0.002]

Let distorted_point be Geometry.apply_radial_distortion(
    image_coordinates, 
    camera_intrinsics,
    radial_distortion_coeffs
)

Let fully_distorted_point be Geometry.apply_tangential_distortion(
    distorted_point,
    camera_intrinsics,
    tangential_distortion_coeffs
)

Note: Stereo vision geometry
Let left_camera_matrix be camera_matrix
Let right_camera_matrix be Geometry.create_stereo_camera_matrix(
    camera_intrinsics,
    baseline: 0.1,
    rotation_offset: Geometry.create_identity_matrix_3d()
)

Let stereo_rectification be Geometry.compute_stereo_rectification(
    left_camera_matrix,
    right_camera_matrix
)

Let fundamental_matrix be Geometry.compute_fundamental_matrix(
    left_camera_matrix,
    right_camera_matrix
)
```

## Vector Spaces and Linear Transformations

### Vector Space Operations

```runa
Note: Vector space basis operations
Let basis_vectors_2d be [
    Geometry.create_vector_2d(1.0, 0.0),
    Geometry.create_vector_2d(0.0, 1.0)
]

Let basis_vectors_3d be [
    Geometry.create_vector_3d(1.0, 0.0, 0.0),
    Geometry.create_vector_3d(0.0, 1.0, 0.0),
    Geometry.create_vector_3d(0.0, 0.0, 1.0)
]

Note: Check if vectors form a basis
Let test_vectors be [
    Geometry.create_vector_3d(1.0, 2.0, 1.0),
    Geometry.create_vector_3d(2.0, 1.0, 0.0),
    Geometry.create_vector_3d(1.0, 0.0, 1.0)
]

Let is_basis be Geometry.is_linearly_independent(test_vectors)
Let determinant_check be Geometry.compute_determinant_3d(test_vectors)

Display "Vectors form a basis: " joined with is_basis
Display "Determinant: " joined with determinant_check

Note: Gram-Schmidt orthogonalization
Let orthogonal_vectors be Geometry.gram_schmidt_orthogonalization(test_vectors)
Let orthonormal_vectors be Geometry.normalize_vector_set(orthogonal_vectors)

Note: Change of basis transformations
Let old_basis be [
    Geometry.create_vector_2d(1.0, 0.0),
    Geometry.create_vector_2d(0.0, 1.0)
]

Let new_basis be [
    Geometry.create_vector_2d(1.0, 1.0),
    Geometry.create_vector_2d(-1.0, 1.0)
]

Let change_of_basis_matrix be Geometry.compute_change_of_basis_matrix(old_basis, new_basis)

Let vector_in_old_basis be Geometry.create_vector_2d(3.0, 2.0)
Let vector_in_new_basis be LinAlg.matrix_vector_multiply(change_of_basis_matrix, vector_in_old_basis)

Display "Vector in new basis: " joined with LinAlg.vector_to_string(vector_in_new_basis)
```

### Linear Transformations Analysis

```runa
Note: Analyze linear transformation properties
Let transformation_matrix be LinAlg.create_matrix([
    [2.0, 1.0],
    [1.0, 2.0]
])

Let is_invertible be Geometry.is_invertible_transformation(transformation_matrix)
Let preserves_orientation be Geometry.preserves_orientation(transformation_matrix)
Let scaling_factors be Geometry.compute_scaling_factors(transformation_matrix)

Display "Transformation is invertible: " joined with is_invertible
Display "Preserves orientation: " joined with preserves_orientation
Display "Scaling factors: " joined with LinAlg.vector_to_string(scaling_factors)

Note: Singular Value Decomposition for geometric analysis
Import "math/engine/linalg/decomposition" as Decomp

Let svd_result be Decomp.singular_value_decomposition(transformation_matrix, "full")
Let u_matrix be Decomp.get_u_matrix(svd_result)
Let singular_values be Decomp.get_singular_values(svd_result)
Let v_matrix be Decomp.get_vt_matrix(svd_result)

Note: Geometric interpretation of SVD components
Let rotation_1 be u_matrix
Let scaling_matrix be LinAlg.create_diagonal_matrix(singular_values)
Let rotation_2 be LinAlg.transpose(v_matrix)

Display "Principal stretching factors: " joined with LinAlg.vector_to_string(singular_values)

Note: Eigenvalue analysis for transformation properties
Let eigenvalue_result be Decomp.eigenvalue_decomposition(transformation_matrix)
Let eigenvalues be Decomp.get_eigenvalues(eigenvalue_result)
Let eigenvectors be Decomp.get_eigenvectors(eigenvalue_result)

Display "Eigenvalues: " joined with LinAlg.vector_to_string(eigenvalues)
```

## Geometric Algorithms

### Distance and Proximity

```runa
Note: Point-to-primitive distances
Let test_point be Geometry.create_point_2d(2.0, 3.0)
Let line_start be Geometry.create_point_2d(0.0, 0.0)
Let line_end be Geometry.create_point_2d(4.0, 0.0)

Let distance_to_line be Geometry.point_to_line_distance_2d(test_point, line_start, line_end)
Let closest_point_on_line be Geometry.closest_point_on_line_2d(test_point, line_start, line_end)

Display "Distance to line: " joined with distance_to_line
Display "Closest point on line: " joined with Geometry.point_to_string(closest_point_on_line)

Note: 3D distance calculations
Let point_3d_a be Geometry.create_point_3d(1.0, 2.0, 3.0)
Let point_3d_b be Geometry.create_point_3d(4.0, 6.0, 8.0)

Let euclidean_distance be Geometry.euclidean_distance_3d(point_3d_a, point_3d_b)
Let manhattan_distance be Geometry.manhattan_distance_3d(point_3d_a, point_3d_b)
Let chebyshev_distance be Geometry.chebyshev_distance_3d(point_3d_a, point_3d_b)

Display "Euclidean distance: " joined with euclidean_distance
Display "Manhattan distance: " joined with manhattan_distance
Display "Chebyshev distance: " joined with chebyshev_distance

Note: Plane-related calculations
Let plane_point be Geometry.create_point_3d(0.0, 0.0, 0.0)
Let plane_normal be Geometry.normalize_vector_3d([1.0, 1.0, 1.0])

Let plane_equation be Geometry.create_plane_equation(plane_point, plane_normal)
Let distance_to_plane be Geometry.point_to_plane_distance(point_3d_a, plane_equation)
Let projected_point be Geometry.project_point_onto_plane(point_3d_a, plane_equation)

Display "Distance to plane: " joined with distance_to_plane
Display "Projected point: " joined with Geometry.point_to_string(projected_point)
```

### Intersection and Collision Detection

```runa
Note: 2D line intersection
Let line_1_start be Geometry.create_point_2d(0.0, 0.0)
Let line_1_end be Geometry.create_point_2d(2.0, 2.0)
Let line_2_start be Geometry.create_point_2d(0.0, 2.0)
Let line_2_end be Geometry.create_point_2d(2.0, 0.0)

Let intersection_result be Geometry.line_line_intersection_2d(
    line_1_start, line_1_end,
    line_2_start, line_2_end
)

If Geometry.has_intersection(intersection_result):
    Let intersection_point be Geometry.get_intersection_point(intersection_result)
    Display "Lines intersect at: " joined with Geometry.point_to_string(intersection_point)
Otherwise:
    Display "Lines do not intersect"

Note: Circle-line intersection
Let circle_center be Geometry.create_point_2d(1.0, 1.0)
Let circle_radius be 1.5

Let circle_line_intersections be Geometry.circle_line_intersection_2d(
    circle_center, circle_radius,
    line_1_start, line_1_end
)

Let num_intersections be Geometry.get_intersection_count(circle_line_intersections)
Display "Number of circle-line intersections: " joined with num_intersections

Note: 3D ray-plane intersection
Let ray_origin be Geometry.create_point_3d(0.0, 0.0, 5.0)
Let ray_direction be Geometry.normalize_vector_3d([0.0, 0.0, -1.0])

Let ray_plane_intersection be Geometry.ray_plane_intersection_3d(
    ray_origin, ray_direction,
    plane_equation
)

If Geometry.ray_intersects_plane(ray_plane_intersection):
    Let intersection_3d be Geometry.get_ray_intersection_point(ray_plane_intersection)
    Let intersection_distance be Geometry.get_intersection_distance(ray_plane_intersection)
    
    Display "Ray intersects plane at: " joined with Geometry.point_to_string(intersection_3d)
    Display "Intersection distance: " joined with intersection_distance

Note: Sphere-ray intersection
Let sphere_center be Geometry.create_point_3d(2.0, 2.0, 2.0)
Let sphere_radius be 1.0

Let sphere_intersections be Geometry.ray_sphere_intersection_3d(
    ray_origin, ray_direction,
    sphere_center, sphere_radius
)

Let sphere_intersection_count be Geometry.get_intersection_count(sphere_intersections)
Display "Ray-sphere intersections: " joined with sphere_intersection_count
```

### Convex Hull and Geometric Properties

```runa
Note: 2D convex hull computation
Let random_points_2d be [
    Geometry.create_point_2d(0.0, 3.0),
    Geometry.create_point_2d(1.0, 1.0),
    Geometry.create_point_2d(2.0, 2.0),
    Geometry.create_point_2d(4.0, 4.0),
    Geometry.create_point_2d(0.0, 0.0),
    Geometry.create_point_2d(1.0, 2.0),
    Geometry.create_point_2d(3.0, 1.0),
    Geometry.create_point_2d(3.0, 3.0)
]

Let convex_hull_2d be Geometry.compute_convex_hull_2d(random_points_2d, "graham_scan")
Let hull_area be Geometry.compute_polygon_area(convex_hull_2d)
Let hull_perimeter be Geometry.compute_polygon_perimeter(convex_hull_2d)

Display "Convex hull area: " joined with hull_area
Display "Convex hull perimeter: " joined with hull_perimeter
Display "Hull vertices: " joined with Geometry.get_vertex_count(convex_hull_2d)

Note: 3D convex hull
Let random_points_3d be Geometry.generate_random_points_3d(20, "unit_cube")
Let convex_hull_3d be Geometry.compute_convex_hull_3d(random_points_3d, "quickhull")

Let hull_volume be Geometry.compute_polyhedron_volume(convex_hull_3d)
Let hull_surface_area be Geometry.compute_polyhedron_surface_area(convex_hull_3d)

Display "3D convex hull volume: " joined with hull_volume
Display "3D convex hull surface area: " joined with hull_surface_area

Note: Point containment tests
Let test_point_2d be Geometry.create_point_2d(1.5, 1.5)
Let point_in_hull = Geometry.point_in_convex_polygon(test_point_2d, convex_hull_2d)

Let test_point_3d be Geometry.create_point_3d(0.5, 0.5, 0.5)
Let point_in_hull_3d be Geometry.point_in_convex_polyhedron(test_point_3d, convex_hull_3d)

Display "2D point in hull: " joined with point_in_hull
Display "3D point in hull: " joined with point_in_hull_3d
```

## Advanced Geometric Computations

### Voronoi Diagrams and Delaunay Triangulation

```runa
Note: Delaunay triangulation
Let point_set be Geometry.generate_random_points_2d(50, "unit_square")
Let delaunay_triangulation be Geometry.compute_delaunay_triangulation(point_set, "incremental")

Let triangle_count be Geometry.get_triangle_count(delaunay_triangulation)
Let edge_count be Geometry.get_edge_count(delaunay_triangulation)

Display "Delaunay triangulation: " joined with triangle_count joined with " triangles, " 
    joined with edge_count joined with " edges"

Note: Voronoi diagram (dual of Delaunay)
Let voronoi_diagram be Geometry.compute_voronoi_diagram(delaunay_triangulation)
Let voronoi_cells be Geometry.get_voronoi_cells(voronoi_diagram)

For cell_index from 0 to 9:  Note: First 10 cells
    Let cell_area be Geometry.compute_voronoi_cell_area(voronoi_diagram, cell_index)
    Display "Voronoi cell " joined with cell_index joined with " area: " joined with cell_area

Note: Nearest neighbor queries using Delaunay
Let query_point be Geometry.create_point_2d(0.5, 0.5)
Let nearest_neighbor be Geometry.find_nearest_neighbor(delaunay_triangulation, query_point)
Let k_nearest_neighbors be Geometry.find_k_nearest_neighbors(
    delaunay_triangulation, 
    query_point, 
    k: 5
)

Display "Nearest neighbor index: " joined with nearest_neighbor
Display "5-NN count: " joined with LinAlg.vector_length(k_nearest_neighbors)
```

### Geometric Optimization

```runa
Note: Minimum enclosing circle
Let circle_points be Geometry.generate_random_points_2d(30, "unit_square")
Let min_enclosing_circle be Geometry.compute_minimum_enclosing_circle(circle_points, "welzl")

Let circle_center be Geometry.get_circle_center(min_enclosing_circle)
Let circle_radius be Geometry.get_circle_radius(min_enclosing_circle)
Let supporting_points be Geometry.get_supporting_points(min_enclosing_circle)

Display "Minimum enclosing circle center: " joined with Geometry.point_to_string(circle_center)
Display "Minimum enclosing circle radius: " joined with circle_radius
Display "Supporting points: " joined with LinAlg.vector_length(supporting_points)

Note: Oriented bounding box
Let obb_points be circle_points
Let oriented_bounding_box be Geometry.compute_oriented_bounding_box_2d(obb_points)

Let obb_center be Geometry.get_obb_center(oriented_bounding_box)
Let obb_dimensions be Geometry.get_obb_dimensions(oriented_bounding_box)
Let obb_orientation be Geometry.get_obb_orientation(oriented_bounding_box)

Display "OBB center: " joined with Geometry.point_to_string(obb_center)
Display "OBB dimensions: " joined with LinAlg.vector_to_string(obb_dimensions)
Display "OBB orientation: " joined with obb_orientation joined with " radians"

Note: Minimum area enclosing rectangle
Let min_area_rect be Geometry.compute_minimum_area_rectangle(obb_points, "rotating_calipers")
Let rect_area be Geometry.get_rectangle_area(min_area_rect)

Display "Minimum area rectangle area: " joined with rect_area
```

### Geometric Interpolation and Curves

```runa
Note: Linear interpolation between points
Let start_point be Geometry.create_point_2d(0.0, 0.0)
Let end_point be Geometry.create_point_2d(4.0, 3.0)

Let interpolated_points be []
For t from 0.0 to 1.0 step 0.1:
    Let lerp_point be Geometry.linear_interpolation_2d(start_point, end_point, t)
    LinAlg.append(interpolated_points, lerp_point)

Note: Bezier curves
Let control_points be [
    Geometry.create_point_2d(0.0, 0.0),
    Geometry.create_point_2d(1.0, 2.0),
    Geometry.create_point_2d(3.0, 2.0),
    Geometry.create_point_2d(4.0, 0.0)
]

Let bezier_curve_points be Geometry.compute_bezier_curve(control_points, num_samples: 20)
Let curve_length be Geometry.compute_curve_length(bezier_curve_points)

Display "Bezier curve length: " joined with curve_length

Note: B-spline curves
Let spline_control_points be [
    Geometry.create_point_2d(0.0, 0.0),
    Geometry.create_point_2d(1.0, 1.0),
    Geometry.create_point_2d(2.0, 1.0),
    Geometry.create_point_2d(3.0, 0.0),
    Geometry.create_point_2d(4.0, -1.0)
]

Let knot_vector be [0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 3.0, 3.0]
Let degree be 2

Let bspline_curve be Geometry.compute_bspline_curve(
    spline_control_points,
    knot_vector,
    degree,
    num_samples: 50
)

Note: Curve analysis
Let curvature_values be Geometry.compute_curve_curvature(bspline_curve)
Let max_curvature be LinAlg.max_element(curvature_values)
Let max_curvature_index be LinAlg.argmax(curvature_values)

Display "Maximum curvature: " joined with max_curvature 
    joined with " at parameter " joined with max_curvature_index
```

## Integration Examples

### Computer Graphics Applications

```runa
Import "graphics/rendering" as Rendering

Note: 3D model transformation pipeline
Let model_vertices be Rendering.load_model_vertices("cube.obj")
Let model_faces be Rendering.load_model_faces("cube.obj")

Note: Apply model transformations
Let model_transform be LinAlg.matrix_multiply(
    translation_3d,
    LinAlg.matrix_multiply(rotation_from_euler, scale_3d)
)

Let transformed_vertices be Geometry.transform_vertices_3d(model_transform, model_vertices)

Note: Lighting calculations using geometry
Let light_position be Geometry.create_point_3d(5.0, 5.0, 5.0)
Let vertex_normals be Geometry.compute_vertex_normals(transformed_vertices, model_faces)

Let lighting_intensities be []
For vertex_index from 0 to (LinAlg.vector_length(transformed_vertices) - 1):
    Let vertex_pos be LinAlg.get_element(transformed_vertices, vertex_index)
    Let vertex_normal be LinAlg.get_element(vertex_normals, vertex_index)
    
    Let light_direction be Geometry.normalize_vector_3d(
        LinAlg.vector_subtract(light_position, vertex_pos)
    )
    
    Let intensity be Geometry.dot_product_3d(vertex_normal, light_direction)
    Let clamped_intensity be LinAlg.max(0.0, intensity)
    
    LinAlg.append(lighting_intensities, clamped_intensity)

Let average_lighting be LinAlg.mean(lighting_intensities)
Display "Average lighting intensity: " joined with average_lighting
```

### Robotics Applications

```runa
Import "robotics/kinematics" as Kinematics

Note: Robot arm forward kinematics
Let joint_angles be [Constants.get_pi() / 6, Constants.get_pi() / 4, -Constants.get_pi() / 3]
Let link_lengths be [1.0, 0.8, 0.6]

Let dh_parameters be Kinematics.create_dh_parameters([
    [0.0, 0.0, link_lengths[0], joint_angles[0]],
    [Constants.get_pi() / 2, 0.0, link_lengths[1], joint_angles[1]], 
    [0.0, 0.0, link_lengths[2], joint_angles[2]]
])

Let transformation_matrices be []
For i from 0 to 2:
    Let dh_params be LinAlg.get_element(dh_parameters, i)
    Let transform be Kinematics.dh_transformation_matrix(dh_params)
    LinAlg.append(transformation_matrices, transform)

Let end_effector_transform be LinAlg.matrix_multiply(
    LinAlg.get_element(transformation_matrices, 0),
    LinAlg.matrix_multiply(
        LinAlg.get_element(transformation_matrices, 1),
        LinAlg.get_element(transformation_matrices, 2)
    )
)

Let end_effector_position be Geometry.extract_translation_3d(end_effector_transform)
Let end_effector_orientation be Geometry.extract_rotation_3d(end_effector_transform)

Display "End effector position: " joined with Geometry.point_to_string(end_effector_position)

Note: Path planning with geometric constraints
Let start_configuration be Geometry.create_point_3d(0.0, 0.0, 0.0)
Let goal_configuration be Geometry.create_point_3d(2.0, 1.5, 1.0)

Let workspace_obstacles be [
    Geometry.create_sphere_obstacle(Geometry.create_point_3d(1.0, 0.5, 0.5), 0.3),
    Geometry.create_box_obstacle(
        Geometry.create_point_3d(1.5, 1.0, 0.2),
        Geometry.create_vector_3d(0.4, 0.4, 0.4)
    )
]

Let collision_free_path be Kinematics.plan_collision_free_path(
    start_configuration,
    goal_configuration,
    workspace_obstacles,
    "rrt_star"
)

Let path_length be Geometry.compute_path_length_3d(collision_free_path)
Display "Planned path length: " joined with path_length
```

### Computer Vision Applications

```runa
Import "vision/geometry" as VisionGeometry

Note: Epipolar geometry for stereo vision
Let left_camera_intrinsics be camera_intrinsics
Let right_camera_intrinsics be camera_intrinsics
Let stereo_baseline be 0.12  Note: 12cm baseline

Let essential_matrix be VisionGeometry.compute_essential_matrix(
    left_camera_matrix,
    right_camera_matrix
)

Let fundamental_matrix_stereo be VisionGeometry.compute_fundamental_matrix_from_essential(
    essential_matrix,
    left_camera_intrinsics,
    right_camera_intrinsics
)

Note: Triangulation for 3D reconstruction
Let left_image_point be Geometry.create_point_2d(320.0, 240.0)
Let right_image_point be Geometry.create_point_2d(310.0, 240.0)

Let triangulated_point_3d be VisionGeometry.triangulate_point(
    left_image_point,
    right_image_point,
    left_camera_matrix,
    right_camera_matrix
)

Let reprojection_error_left be VisionGeometry.compute_reprojection_error(
    triangulated_point_3d,
    left_image_point,
    left_camera_matrix
)

Display "Triangulated 3D point: " joined with Geometry.point_to_string(triangulated_point_3d)
Display "Left camera reprojection error: " joined with reprojection_error_left

Note: Homography estimation for plane tracking
Let template_corners be [
    Geometry.create_point_2d(0.0, 0.0),
    Geometry.create_point_2d(100.0, 0.0),
    Geometry.create_point_2d(100.0, 100.0),
    Geometry.create_point_2d(0.0, 100.0)
]

Let detected_corners be [
    Geometry.create_point_2d(50.0, 60.0),
    Geometry.create_point_2d(180.0, 45.0),
    Geometry.create_point_2d(195.0, 170.0),
    Geometry.create_point_2d(65.0, 185.0)
]

Let plane_homography be Geometry.compute_homography(template_corners, detected_corners)
Let homography_decomposition be VisionGeometry.decompose_homography(
    plane_homography,
    camera_intrinsics
)

Let possible_poses be VisionGeometry.get_possible_poses(homography_decomposition)
Display "Number of possible poses: " joined with LinAlg.vector_length(possible_poses)
```

## Best Practices

### Numerical Stability in Geometric Computing

```runa
Note: Handle numerical precision issues
Let epsilon_tolerance be 1e-10

Let nearly_zero_determinant be Geometry.compute_determinant_2d([
    [1.0, 2.0],
    [1.0000000001, 2.0000000002]
])

If LinAlg.abs(nearly_zero_determinant) < epsilon_tolerance:
    Display "Matrix is numerically singular"
    Let regularized_matrix be Geometry.add_regularization_2d(test_matrix, epsilon_tolerance)

Note: Robust geometric predicates
Let robust_orientation_test be Geometry.robust_orientation_test(
    point_a, point_b, point_c,
    use_exact_arithmetic: True
)

Let robust_incircle_test be Geometry.robust_incircle_test(
    point_a, point_b, point_c, point_d,
    use_exact_arithmetic: True
)

Note: Handle degenerate cases
Let degenerate_triangle = [
    Geometry.create_point_2d(0.0, 0.0),
    Geometry.create_point_2d(1.0, 1.0),
    Geometry.create_point_2d(2.0, 2.0)  Note: Collinear points
]

Let triangle_area_robust be Geometry.compute_triangle_area_robust(degenerate_triangle)
Let is_degenerate be Geometry.is_degenerate_triangle(degenerate_triangle, epsilon_tolerance)

Display "Triangle is degenerate: " joined with is_degenerate
```

### Performance Optimization

```runa
Note: Vectorized geometric operations
Let point_cloud be Geometry.generate_random_points_3d(10000, "unit_sphere")

Note: Batch transform all points efficiently
Let batch_transformed_points be Geometry.batch_transform_points_3d(
    model_transform,
    point_cloud
)

Note: Parallel geometric computations
Geometry.enable_parallel_processing(thread_count: 8)

Let parallel_distances be Geometry.compute_pairwise_distances_parallel(
    point_cloud,
    chunk_size: 1000
)

Note: Spatial data structures for fast queries
Let spatial_index be Geometry.create_spatial_index(point_cloud, "kdtree")

Let range_query_result be Geometry.range_query(
    spatial_index,
    query_center: Geometry.create_point_3d(0.0, 0.0, 0.0),
    query_radius: 0.5
)

Let nearest_k_result be Geometry.k_nearest_neighbors_query(
    spatial_index,
    query_point: Geometry.create_point_3d(0.2, 0.3, 0.1),
    k: 10
)

Display "Points in range: " joined with LinAlg.vector_length(range_query_result)
Display "K-NN query result count: " joined with LinAlg.vector_length(nearest_k_result)
```

The Computational Geometry module provides essential geometric linear algebra operations that form the foundation for computer graphics, robotics, computer vision, and scientific visualization applications, enabling efficient and numerically stable geometric computations.