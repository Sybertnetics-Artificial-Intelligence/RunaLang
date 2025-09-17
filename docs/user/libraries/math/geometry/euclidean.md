# Euclidean Geometry Module

The `math/geometry/euclidean` module provides comprehensive tools for classical Euclidean geometry including points, vectors, lines, planes, circles, polygons, and transformations in 2D and 3D space. This module forms the foundation for most geometric computations and computer graphics applications.

## Quick Start

```runa
Import "math/geometry/euclidean" as Euclidean

Note: Basic point and vector operations
Let point1 be Euclidean.create_point([2, 3, 1])
Let point2 be Euclidean.create_point([5, 7, 4])
Let vector1 be Euclidean.create_vector([1, 0, 2])

Let distance be Euclidean.distance(point1, point2)
Let midpoint be Euclidean.midpoint(point1, point2)
Let vector_length be Euclidean.magnitude(vector1)

Display "Distance: " joined with distance
Display "Midpoint: " joined with Euclidean.point_to_string(midpoint)
Display "Vector magnitude: " joined with vector_length
```

## Core Concepts

### Euclidean Space
The familiar geometry of flat space where the parallel postulate holds and distances are measured using the Pythagorean theorem.

### Points and Vectors
Points represent locations in space, while vectors represent displacements, directions, or quantities with magnitude and direction.

### Linear Objects
Lines and planes are fundamental linear geometric objects that extend infinitely.

### Curved Objects
Circles, spheres, and other curved objects defined by distance relationships.

### Transformations
Operations that move, rotate, scale, or otherwise modify geometric objects while preserving certain properties.

## API Reference

### Points and Vectors

#### Point Operations
```runa
Type called "Point":
    coordinates as List[Real]
    dimension as Integer

Process called "create_point" that takes coordinates as List[Real] returns Point:
    Note: Create point from coordinate list

Process called "distance" that takes:
    point1 as Point,
    point2 as Point
returns Real:
    Note: Compute Euclidean distance between points

Process called "midpoint" that takes:
    point1 as Point,
    point2 as Point
returns Point:
    Note: Compute midpoint between two points

Process called "centroid" that takes points as List[Point] returns Point:
    Note: Compute centroid (average position) of point set
```

#### Vector Operations
```runa
Type called "Vector":
    components as List[Real]
    dimension as Integer

Process called "create_vector" that takes components as List[Real] returns Vector:
    Note: Create vector from component list

Process called "magnitude" that takes vector as Vector returns Real:
    Note: Compute length/magnitude of vector

Process called "normalize" that takes vector as Vector returns Vector:
    Note: Return unit vector in same direction

Process called "dot_product" that takes:
    vector1 as Vector,
    vector2 as Vector
returns Real:
    Note: Compute dot product (scalar product)

Process called "cross_product" that takes:
    vector1 as Vector,
    vector2 as Vector
returns Vector:
    Note: Compute cross product (3D only)
```

#### Point-Vector Relationships
```runa
Process called "point_to_vector" that takes point as Point returns Vector:
    Note: Convert point to position vector from origin

Process called "vector_to_point" that takes vector as Vector returns Point:
    Note: Convert vector to point (endpoint from origin)

Process called "translate_point" that takes:
    point as Point,
    vector as Vector
returns Point:
    Note: Translate point by vector

Process called "vector_between_points" that takes:
    from_point as Point,
    to_point as Point
returns Vector:
    Note: Compute vector from first point to second point
```

### Lines and Rays

#### Line Representation
```runa
Type called "Line":
    point as Point
    direction as Vector
    type as String  Note: "line", "ray", "segment"

Process called "create_line" that takes:
    point as Point,
    direction as Vector
returns Line:
    Note: Create infinite line through point in direction

Process called "create_line_through_points" that takes:
    point1 as Point,
    point2 as Point
returns Line:
    Note: Create line passing through two points

Process called "create_ray" that takes:
    origin as Point,
    direction as Vector
returns Line:
    Note: Create ray starting at origin in direction

Process called "create_segment" that takes:
    point1 as Point,
    point2 as Point
returns Line:
    Note: Create line segment between two points
```

#### Line Operations
```runa
Process called "point_on_line" that takes:
    line as Line,
    parameter as Real
returns Point:
    Note: Get point on line at parameter t

Process called "closest_point_on_line" that takes:
    line as Line,
    point as Point
returns Point:
    Note: Find closest point on line to given point

Process called "distance_point_to_line" that takes:
    point as Point,
    line as Line
returns Real:
    Note: Compute perpendicular distance from point to line

Process called "line_intersection" that takes:
    line1 as Line,
    line2 as Line
returns Point:
    Note: Find intersection point of two lines (if exists)
```

### Planes

#### Plane Representation
```runa
Type called "Plane":
    point as Point
    normal as Vector
    equation_coefficients as List[Real]  Note: ax + by + cz + d = 0

Process called "create_plane" that takes:
    point as Point,
    normal as Vector
returns Plane:
    Note: Create plane through point with normal vector

Process called "create_plane_from_points" that takes:
    point1 as Point,
    point2 as Point,
    point3 as Point
returns Plane:
    Note: Create plane through three non-collinear points

Process called "create_plane_from_equation" that takes coefficients as List[Real] returns Plane:
    Note: Create plane from equation ax + by + cz + d = 0
```

#### Plane Operations
```runa
Process called "distance_point_to_plane" that takes:
    point as Point,
    plane as Plane
returns Real:
    Note: Compute signed distance from point to plane

Process called "project_point_onto_plane" that takes:
    point as Point,
    plane as Plane
returns Point:
    Note: Project point orthogonally onto plane

Process called "plane_line_intersection" that takes:
    plane as Plane,
    line as Line
returns Point:
    Note: Find intersection of plane and line

Process called "plane_plane_intersection" that takes:
    plane1 as Plane,
    plane2 as Plane
returns Line:
    Note: Find intersection line of two planes
```

### Circles and Spheres

#### Circle Operations (2D)
```runa
Type called "Circle":
    center as Point
    radius as Real

Process called "create_circle" that takes:
    center as Point,
    radius as Real
returns Circle:
    Note: Create circle with given center and radius

Process called "circle_area" that takes circle as Circle returns Real:
    Note: Compute area of circle

Process called "circle_circumference" that takes circle as Circle returns Real:
    Note: Compute circumference of circle

Process called "point_in_circle" that takes:
    point as Point,
    circle as Circle
returns Boolean:
    Note: Check if point is inside circle

Process called "circle_circle_intersection" that takes:
    circle1 as Circle,
    circle2 as Circle
returns List[Point]:
    Note: Find intersection points of two circles
```

#### Sphere Operations (3D)
```runa
Type called "Sphere":
    center as Point
    radius as Real

Process called "create_sphere" that takes:
    center as Point,
    radius as Real
returns Sphere:
    Note: Create sphere with given center and radius

Process called "sphere_volume" that takes sphere as Sphere returns Real:
    Note: Compute volume of sphere

Process called "sphere_surface_area" that takes sphere as Sphere returns Real:
    Note: Compute surface area of sphere

Process called "point_in_sphere" that takes:
    point as Point,
    sphere as Sphere
returns Boolean:
    Note: Check if point is inside sphere

Process called "sphere_line_intersection" that takes:
    sphere as Sphere,
    line as Line
returns List[Point]:
    Note: Find intersection points of sphere and line
```

### Polygons

#### Polygon Construction
```runa
Type called "Polygon":
    vertices as List[Point]
    is_closed as Boolean
    dimension as Integer

Process called "create_polygon" that takes vertices as List[Point] returns Polygon:
    Note: Create polygon from vertex list

Process called "create_regular_polygon" that takes:
    center as Point,
    radius as Real,
    sides as Integer
returns Polygon:
    Note: Create regular polygon with given parameters

Process called "create_rectangle" that takes:
    bottom_left as Point,
    top_right as Point
returns Polygon:
    Note: Create axis-aligned rectangle
```

#### Polygon Properties
```runa
Process called "polygon_area" that takes polygon as Polygon returns Real:
    Note: Compute area using shoelace formula

Process called "polygon_perimeter" that takes polygon as Polygon returns Real:
    Note: Compute perimeter (sum of edge lengths)

Process called "polygon_centroid" that takes polygon as Polygon returns Point:
    Note: Compute centroid of polygon

Process called "point_in_polygon" that takes:
    point as Point,
    polygon as Polygon
returns Boolean:
    Note: Check if point is inside polygon using ray casting

Process called "polygon_convex" that takes polygon as Polygon returns Boolean:
    Note: Check if polygon is convex
```

### Transformations

#### Basic Transformations
```runa
Type called "Transform":
    matrix as Matrix
    translation as Vector
    type as String

Process called "create_translation" that takes vector as Vector returns Transform:
    Note: Create translation transformation

Process called "create_rotation_2d" that takes angle as Real returns Transform:
    Note: Create 2D rotation around origin

Process called "create_rotation_3d" that takes:
    axis as Vector,
    angle as Real
returns Transform:
    Note: Create 3D rotation around axis

Process called "create_scaling" that takes:
    factors as List[Real],
    center as Point
returns Transform:
    Note: Create scaling transformation
```

#### Transform Operations
```runa
Process called "apply_transform" that takes:
    transform as Transform,
    point as Point
returns Point:
    Note: Apply transformation to point

Process called "apply_transform_to_vector" that takes:
    transform as Transform,
    vector as Vector
returns Vector:
    Note: Apply transformation to vector

Process called "compose_transforms" that takes:
    transform1 as Transform,
    transform2 as Transform
returns Transform:
    Note: Compose two transformations

Process called "inverse_transform" that takes transform as Transform returns Transform:
    Note: Compute inverse transformation
```

## Practical Examples

### Basic Geometric Computations
```runa
Import "math/geometry/euclidean" as Euclidean

Note: Analyze triangle properties
Let triangle_vertices be [
    Euclidean.create_point([0, 0]),
    Euclidean.create_point([4, 0]),
    Euclidean.create_point([2, 3])
]

Let triangle be Euclidean.create_polygon(triangle_vertices)
Let area be Euclidean.polygon_area(triangle)
Let perimeter be Euclidean.polygon_perimeter(triangle)
Let centroid be Euclidean.polygon_centroid(triangle)

Display "Triangle area: " joined with area
Display "Triangle perimeter: " joined with perimeter
Display "Triangle centroid: " joined with Euclidean.point_to_string(centroid)

Note: Compute angles
Let angles be []
For i from 0 to 2:
    Let p1 be triangle_vertices[i]
    Let p2 be triangle_vertices[(i + 1) % 3]
    Let p3 be triangle_vertices[(i + 2) % 3]
    
    Let v1 be Euclidean.vector_between_points(p1, p2)
    Let v2 be Euclidean.vector_between_points(p1, p3)
    
    Let angle be Euclidean.angle_between_vectors(v1, v2)
    angles.append(angle)

Display "Triangle angles (degrees): " joined with angles
Let angle_sum be angles[0] + angles[1] + angles[2]
Display "Angle sum: " joined with angle_sum joined with " (should be ~180°)"
```

### 3D Geometric Operations
```runa
Note: Work with 3D geometric objects
Let cube_vertices be [
    Euclidean.create_point([0, 0, 0]),
    Euclidean.create_point([1, 0, 0]),
    Euclidean.create_point([1, 1, 0]),
    Euclidean.create_point([0, 1, 0]),
    Euclidean.create_point([0, 0, 1]),
    Euclidean.create_point([1, 0, 1]),
    Euclidean.create_point([1, 1, 1]),
    Euclidean.create_point([0, 1, 1])
]

Note: Compute bounding sphere
Let centroid be Euclidean.centroid(cube_vertices)
Let max_distance be 0.0
For Each vertex in cube_vertices:
    Let distance be Euclidean.distance(centroid, vertex)
    If distance > max_distance:
        max_distance be distance

Let bounding_sphere be Euclidean.create_sphere(centroid, max_distance)
Display "Bounding sphere center: " joined with Euclidean.point_to_string(centroid)
Display "Bounding sphere radius: " joined with max_distance

Note: Check which vertices are on sphere surface
Let vertices_on_sphere be 0
For Each vertex in cube_vertices:
    Let distance_to_center be Euclidean.distance(vertex, centroid)
    If abs(distance_to_center - max_distance) < 1e-10:
        vertices_on_sphere += 1

Display "Vertices on bounding sphere: " joined with vertices_on_sphere
```

### Line and Plane Intersections
```runa
Note: Find intersection of line and plane
Let plane be Euclidean.create_plane(
    point: Euclidean.create_point([0, 0, 1]),
    normal: Euclidean.create_vector([0, 0, 1])
)

Let line be Euclidean.create_line(
    point: Euclidean.create_point([2, 3, 5]),
    direction: Euclidean.create_vector([1, -1, -2])
)

Let intersection be Euclidean.plane_line_intersection(plane, line)
If intersection != null:
    Display "Intersection point: " joined with Euclidean.point_to_string(intersection)
    
    Note: Verify point is on plane
    Let distance_to_plane be Euclidean.distance_point_to_plane(intersection, plane)
    Display "Distance to plane (should be ~0): " joined with distance_to_plane
Otherwise:
    Display "Line and plane do not intersect (parallel)"

Note: Find intersection of two planes
Let plane2 be Euclidean.create_plane(
    point: Euclidean.create_point([1, 0, 0]),
    normal: Euclidean.create_vector([1, 0, 0])
)

Let intersection_line be Euclidean.plane_plane_intersection(plane, plane2)
Display "Intersection line direction: " joined with Euclidean.vector_to_string(intersection_line.direction)
```

### Circle and Arc Operations
```runa
Note: Work with circles and compute intersections
Let circle1 be Euclidean.create_circle(
    center: Euclidean.create_point([0, 0]),
    radius: 3.0
)

Let circle2 be Euclidean.create_circle(
    center: Euclidean.create_point([4, 0]),
    radius: 2.0
)

Let intersections be Euclidean.circle_circle_intersection(circle1, circle2)
Display "Circle intersection points: " joined with intersections.length()

For Each intersection_point in intersections:
    Display "  " joined with Euclidean.point_to_string(intersection_point)
    
    Note: Verify point is on both circles
    Let dist1 be Euclidean.distance(intersection_point, circle1.center)
    Let dist2 be Euclidean.distance(intersection_point, circle2.center)
    Display "    Distances to centers: " joined with dist1 joined with ", " joined with dist2

Note: Compute arc length
Let start_angle be 0.0
Let end_angle be 1.57  Note: π/2 radians (90 degrees)
Let arc_length be circle1.radius * (end_angle - start_angle)
Display "Quarter circle arc length: " joined with arc_length
```

### Geometric Transformations
```runa
Note: Apply sequence of transformations
Let original_points be [
    Euclidean.create_point([1, 0]),
    Euclidean.create_point([0, 1]),
    Euclidean.create_point([-1, 0]),
    Euclidean.create_point([0, -1])
]

Note: Create transformation sequence
Let translation be Euclidean.create_translation(Euclidean.create_vector([2, 3]))
Let rotation be Euclidean.create_rotation_2d(angle: 0.785)  Note: 45 degrees
Let scaling be Euclidean.create_scaling(factors: [2.0, 1.5], center: Euclidean.create_point([0, 0]))

Let combined_transform be Euclidean.compose_transforms(
    translation,
    Euclidean.compose_transforms(rotation, scaling)
)

Note: Apply transformation to all points
Let transformed_points be []
For Each point in original_points:
    Let transformed be Euclidean.apply_transform(combined_transform, point)
    transformed_points.append(transformed)

Display "Original points transformed:"
For i from 0 to original_points.length() - 1:
    Display "  " joined with Euclidean.point_to_string(original_points[i]) joined 
            with " → " joined with Euclidean.point_to_string(transformed_points[i])

Note: Verify transformation properties
Let determinant be Euclidean.transformation_determinant(combined_transform)
Display "Transformation determinant: " joined with determinant
Display "Area scaling factor: " joined with abs(determinant)
```

## Advanced Features

### Geometric Measurements
```runa
Process called "triangle_quality_metrics" that takes vertices as List[Point] returns Dictionary[String, Real]:
    Let sides be []
    For i from 0 to 2:
        Let side_length be Euclidean.distance(vertices[i], vertices[(i+1) % 3])
        sides.append(side_length)
    
    Let area be Euclidean.polygon_area(Euclidean.create_polygon(vertices))
    Let perimeter be sides[0] + sides[1] + sides[2]
    
    Note: Quality metrics
    Let aspect_ratio be Linear.maximum(sides) / Linear.minimum(sides)
    Let inradius be area / (perimeter / 2.0)
    Let circumradius be (sides[0] * sides[1] * sides[2]) / (4.0 * area)
    Let regularity be inradius / circumradius  Note: 0.5 for equilateral triangle
    
    Return Dictionary[String, Real]:
        "area": area
        "perimeter": perimeter
        "aspect_ratio": aspect_ratio
        "regularity": regularity
        "inradius": inradius
        "circumradius": circumradius
```

### Geometric Predicates
```runa
Process called "robust_geometric_predicates" that takes points as List[Point] returns Dictionary[String, Boolean]:
    Note: Implement robust geometric predicates for exact computation
    
    Process called "orientation_test" that takes:
        p1 as Point,
        p2 as Point,
        p3 as Point
    returns Integer:
        Note: Return +1 for counterclockwise, -1 for clockwise, 0 for collinear
        Let determinant be (p2.coordinates[0] - p1.coordinates[0]) * (p3.coordinates[1] - p1.coordinates[1]) -
                          (p3.coordinates[0] - p1.coordinates[0]) * (p2.coordinates[1] - p1.coordinates[1])
        
        Let epsilon be 1e-12  Note: Tolerance for numerical errors
        If abs(determinant) < epsilon:
            Return 0
        Otherwise If determinant > 0:
            Return 1
        Otherwise:
            Return -1
    
    Let p1 be points[0]
    Let p2 be points[1] 
    Let p3 be points[2]
    
    Let orientation be orientation_test(p1, p2, p3)
    Let are_collinear be (orientation == 0)
    Let counterclockwise be (orientation > 0)
    
    Return Dictionary[String, Boolean]:
        "collinear": are_collinear
        "counterclockwise": counterclockwise
        "clockwise": not counterclockwise and not are_collinear
```

### Coordinate System Conversions
```runa
Process called "cartesian_to_polar" that takes point as Point returns Dictionary[String, Real]:
    Let x be point.coordinates[0]
    Let y be point.coordinates[1]
    
    Let r be Euclidean.magnitude(Euclidean.create_vector([x, y]))
    Let theta be Math.atan2(y, x)
    
    Return Dictionary[String, Real]:
        "r": r
        "theta": theta

Process called "cartesian_to_spherical" that takes point as Point returns Dictionary[String, Real]:
    Let x be point.coordinates[0]
    Let y be point.coordinates[1] 
    Let z be point.coordinates[2]
    
    Let r be Euclidean.magnitude(Euclidean.create_vector([x, y, z]))
    Let theta be Math.atan2(y, x)  Note: Azimuthal angle
    Let phi be Math.acos(z / r)    Note: Polar angle from z-axis
    
    Return Dictionary[String, Real]:
        "r": r
        "theta": theta
        "phi": phi

Process called "spherical_to_cartesian" that takes:
    r as Real,
    theta as Real,
    phi as Real
returns Point:
    Let x be r * Math.sin(phi) * Math.cos(theta)
    Let y be r * Math.sin(phi) * Math.sin(theta)
    Let z be r * Math.cos(phi)
    
    Return Euclidean.create_point([x, y, z])
```

## Integration with Other Modules

### With Linear Algebra
```runa
Import "math/algebra/linear" as Linear
Import "math/geometry/euclidean" as Euclidean

Note: Use linear algebra for geometric computations
Let points_matrix be Linear.create_matrix([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

Note: Apply matrix transformation to points
Let transformation_matrix be Linear.create_matrix([
    [0, -1, 0],
    [1,  0, 0],
    [0,  0, 1]
])

Let transformed_matrix be Linear.matrix_multiplication(transformation_matrix, points_matrix)
Display "Points transformed using linear algebra"
```

### With Calculus
```runa
Import "math/analysis/calculus" as Calculus
Import "math/geometry/euclidean" as Euclidean

Note: Compute geometric properties using calculus
Process called "curve_length" that takes:
    parametric_function as Process,
    t_start as Real,
    t_end as Real
returns Real:
    Process called "speed_function" that takes t as Real returns Real:
        Let point be parametric_function(t)
        Let derivative be Calculus.derivative(parametric_function, t)
        Return Euclidean.magnitude(derivative)
    
    Return Calculus.definite_integral(speed_function, t_start, t_end)

Note: Example: length of quarter circle
Process called "quarter_circle" that takes t as Real returns Point:
    Return Euclidean.create_point([Math.cos(t), Math.sin(t)])

Let arc_length be curve_length(quarter_circle, 0, 1.57)
Display "Quarter circle arc length: " joined with arc_length
```

### With Numerical Methods
```runa
Import "math/engine/numerical/rootfinding" as RootFind
Import "math/geometry/euclidean" as Euclidean

Note: Find intersection using numerical methods
Process called "implicit_curve_intersection" that takes:
    curve1_equation as Process,
    curve2_equation as Process,
    initial_guess as Point
returns Point:
    Process called "system_equations" that takes variables as List[Real] returns List[Real]:
        Let point be Euclidean.create_point(variables)
        Return [curve1_equation(point), curve2_equation(point)]
    
    Let solution be RootFind.newton_method_system(
        system_equations,
        initial_guess.coordinates,
        tolerance: 1e-10
    )
    
    Return Euclidean.create_point(solution)

Note: Example: find intersection of circle and parabola
Process called "circle_equation" that takes point as Point returns Real:
    Let x be point.coordinates[0]
    Let y be point.coordinates[1]
    Return x*x + y*y - 4.0  Note: Circle with radius 2

Process called "parabola_equation" that takes point as Point returns Real:
    Let x be point.coordinates[0]
    Let y be point.coordinates[1]
    Return y - x*x  Note: Parabola y = x²

Let intersection_point be implicit_curve_intersection(
    circle_equation,
    parabola_equation,
    initial_guess: Euclidean.create_point([1.0, 1.0])
)

Display "Intersection found at: " joined with Euclidean.point_to_string(intersection_point)
```

## Performance Optimization

### Efficient Distance Computations
```runa
Note: Avoid square root when only comparing distances
Process called "distance_squared" that takes:
    point1 as Point,
    point2 as Point
returns Real:
    Let sum_of_squares be 0.0
    For i from 0 to point1.coordinates.length() - 1:
        Let diff be point1.coordinates[i] - point2.coordinates[i]
        sum_of_squares += diff * diff
    Return sum_of_squares

Process called "closest_point_fast" that takes:
    target as Point,
    candidates as List[Point]
returns Point:
    Let closest_point be candidates[0]
    Let min_distance_sq be distance_squared(target, closest_point)
    
    For Each candidate in candidates[1:]:
        Let dist_sq be distance_squared(target, candidate)
        If dist_sq < min_distance_sq:
            min_distance_sq be dist_sq
            closest_point be candidate
    
    Return closest_point
```

### Batch Operations
```runa
Note: Process multiple geometric objects efficiently
Process called "batch_transform_points" that takes:
    points as List[Point],
    transform as Transform
returns List[Point]:
    Let transformed_points be []
    Let matrix be transform.matrix
    Let translation be transform.translation
    
    For Each point in points:
        Note: Apply matrix transformation
        Let transformed_coords be []
        For i from 0 to point.coordinates.length() - 1:
            Let new_coord be 0.0
            For j from 0 to matrix.columns - 1:
                new_coord += matrix.entries[i][j] * point.coordinates[j]
            new_coord += translation.components[i]
            transformed_coords.append(new_coord)
        
        transformed_points.append(Euclidean.create_point(transformed_coords))
    
    Return transformed_points
```

This module provides the foundational geometric tools needed for computer graphics, robotics, CAD applications, and mathematical visualization, forming the basis for more advanced geometric computations in other modules.