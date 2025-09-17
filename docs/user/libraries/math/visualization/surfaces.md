Note: 3D Surface Plotting Module Guide

## Overview

The `math/visualization/surfaces` module provides comprehensive 3D surface visualization and volume rendering capabilities for advanced mathematical graphics. This module enables creation of sophisticated 3D visualizations including surface plots, contour maps, volume rendering, and complex mathematical surface analysis.

## Key Features

- **3D Surface Plotting**: Visualize functions z = f(x,y) and parametric surfaces
- **Volume Rendering**: Scalar field visualization with opacity mapping
- **Isosurface Extraction**: Level set visualization using marching cubes
- **Surface Analysis**: Curvature, normals, and differential geometry visualization
- **Advanced Lighting**: Phong shading, texture mapping, material properties
- **Multiple Projections**: Perspective and orthographic viewing modes
- **Interactive Navigation**: 3D rotation, zoom, and pan capabilities
- **High-Quality Export**: Publication-ready 3D graphics output

## Mathematical Foundation

The surfaces module implements advanced 3D mathematical visualization:

- **Surface Functions**: z = f(x,y) and parametric surfaces r(u,v) = [x(u,v), y(u,v), z(u,v)]
- **Level Surfaces**: F(x,y,z) = c for implicit surface definition  
- **Vector Field Visualization**: 3D streamlines and flow visualization
- **Surface Differential Geometry**: Curvature, normals, tangent planes
- **Volume Rendering**: Scalar field visualization with opacity mapping
- **Isosurface Extraction**: Marching cubes algorithm for level sets
- **Surface Lighting**: Phong shading model with ambient, diffuse, and specular components
- **Projective Geometry**: Mathematical projection and viewing transformations

## Core Data Types

### Surface3D
Represents a 3D surface mesh:
```runa
Type called "Surface3D":
    vertices as List[List[Float64]]           Note: 3D coordinate points [x,y,z]
    faces as List[List[Integer]]             Note: Triangular face vertex indices
    normals as List[List[Float64]]           Note: Surface normal vectors
    colors as List[List[Float64]]            Note: Vertex or face colors (RGB/RGBA)
    texture_coordinates as List[List[Float64]] Note: UV texture mapping coordinates
    material_properties as Dictionary[String, Float64] Note: Lighting properties
```

### Volume3D
Represents volumetric data for 3D visualization:
```runa
Type called "Volume3D":
    dimensions as List[Integer]               Note: Grid dimensions [nx, ny, nz]
    spacing as List[Float64]                 Note: Grid spacing [dx, dy, dz]
    origin as List[Float64]                  Note: Coordinate system origin
    scalar_data as List[List[List[Float64]]] Note: 3D scalar field values
    vector_data as List[List[List[List[Float64]]]] Note: 3D vector field (optional)
    metadata as Dictionary[String, String]   Note: Units, descriptions, etc.
```

### SurfaceViewer3D
Configuration for 3D visualization:
```runa
Type called "SurfaceViewer3D":
    camera_position as List[Float64]         Note: [x, y, z] camera location
    camera_target as List[Float64]           Note: [x, y, z] look-at point
    camera_up as List[Float64]               Note: [x, y, z] up vector
    field_of_view as Float64                 Note: Perspective FOV in degrees
    near_plane as Float64                    Note: Near clipping plane
    far_plane as Float64                     Note: Far clipping plane
    projection_type as String                Note: "perspective" or "orthographic"
    viewport_size as List[Integer]           Note: [width, height] in pixels
```

## Basic Surface Plotting

### Function Surface z = f(x,y)
```runa
Import "math/visualization/surfaces" as Surfaces
Import "math/core/operations" as MathOps

Note: Define mathematical function
Process called "surface_function" that takes x as Float64, y as Float64 returns Float64:
    Note: z = sin(sqrt(x² + y²)) / sqrt(x² + y²) - sinc function
    Let r_squared be x * x + y * y
    If r_squared < 1e-10:
        Return 1.0  Note: Limit as r → 0
    Otherwise:
        Let r be MathOps.square_root(String(r_squared), 15)
        Let sin_r be Trig.sine(r.result_value, "radians", 15)
        Let result be MathOps.divide(sin_r.function_value, r.result_value, 15)
        Return Float64(result.result_value)

Note: Create surface mesh
Let x_range be [-10.0, 10.0]
Let y_range be [-10.0, 10.0]
Let resolution be [100, 100]

Let surface_mesh be Surfaces.create_function_surface(
    surface_function,
    x_range,
    y_range,
    resolution
)

Note: Configure viewing
Let viewer be SurfaceViewer3D with:
    camera_position: [15.0, 15.0, 10.0]
    camera_target: [0.0, 0.0, 0.0]
    camera_up: [0.0, 0.0, 1.0]
    field_of_view: 45.0
    projection_type: "perspective"

Let plot_result be Surfaces.plot_surface(surface_mesh, viewer)
```

### Parametric Surfaces
```runa
Note: Create parametric surface r(u,v) = [x(u,v), y(u,v), z(u,v)]
Process called "torus_surface" that takes u as Float64, v as Float64 returns List[Float64]:
    Note: Torus with major radius R=3, minor radius r=1
    Let R be 3.0
    Let r be 1.0
    
    Let cos_u be Trig.cosine(String(u), "radians", 15)
    Let sin_u be Trig.sine(String(u), "radians", 15)
    Let cos_v be Trig.cosine(String(v), "radians", 15)
    Let sin_v be Trig.sine(String(v), "radians", 15)
    
    Let x be (R + r * Float64(cos_v.function_value)) * Float64(cos_u.function_value)
    Let y be (R + r * Float64(cos_v.function_value)) * Float64(sin_u.function_value)
    Let z be r * Float64(sin_v.function_value)
    
    Return [x, y, z]

Let u_range be [0.0, 6.283185307]  Note: 0 to 2π
Let v_range be [0.0, 6.283185307]  Note: 0 to 2π
Let param_resolution be [80, 40]

Let torus_mesh be Surfaces.create_parametric_surface(
    torus_surface,
    u_range,
    v_range,
    param_resolution
)

Note: Apply material properties
Let torus_material be Dictionary[String, Float64] with:
    "ambient": 0.2
    "diffuse": 0.8
    "specular": 0.3
    "shininess": 32.0

Let torus_with_material be Surfaces.apply_material(torus_mesh, torus_material)
Let torus_plot be Surfaces.plot_surface(torus_with_material, viewer)
```

## Advanced Surface Features

### Contour and Level Curves
```runa
Note: Add contour lines to surface
Let contour_levels be [-0.5, -0.2, 0.0, 0.2, 0.5, 0.8]
Let contour_lines be Surfaces.generate_contour_lines(surface_mesh, contour_levels)

Let contour_config be Dictionary[String, String] with:
    "line_color": "black"
    "line_width": "2.0"
    "show_labels": "true"
    "label_format": "%.2f"

Let surface_with_contours be Surfaces.add_contour_lines(
    surface_mesh,
    contour_lines,
    contour_config
)
```

### Surface Analysis and Differential Geometry
```runa
Note: Compute surface properties
Let surface_analysis be Surfaces.analyze_surface_geometry(surface_mesh)

Note: Visualize mean curvature
Let curvature_colors be Surfaces.map_scalar_to_color(
    surface_analysis.mean_curvature,
    "blue_red",
    [-2.0, 2.0]
)

Let curvature_surface be Surfaces.apply_vertex_colors(surface_mesh, curvature_colors)

Note: Add normal vectors visualization
Let normal_vectors be Surfaces.compute_surface_normals(surface_mesh)
Let normal_visualization be Surfaces.create_normal_arrows(
    surface_mesh.vertices,
    normal_vectors,
    0.5  Note: Arrow length scale
)

Let surface_with_normals be Surfaces.add_vector_field(surface_mesh, normal_visualization)
```

## Volume Visualization

### Scalar Field Rendering
```runa
Note: Create 3D scalar field data
Process called "scalar_field" that takes x as Float64, y as Float64, z as Float64 returns Float64:
    Note: 3D Gaussian: exp(-(x² + y² + z²))
    Let r_squared be x * x + y * y + z * z
    Let exponential be MathOps.exponential(String(-r_squared), 15)
    Return Float64(exponential.result_value)

Let volume_bounds be [[-3.0, 3.0], [-3.0, 3.0], [-3.0, 3.0]]
Let volume_resolution be [64, 64, 64]

Let volume_data be Surfaces.create_scalar_volume(
    scalar_field,
    volume_bounds,
    volume_resolution
)

Note: Configure volume rendering
Let volume_config be Dictionary[String, String] with:
    "transfer_function": "alpha_ramp"
    "color_map": "hot"
    "opacity_scale": "0.1"
    "sampling_rate": "2.0"

Let volume_render be Surfaces.render_volume(volume_data, volume_config, viewer)
```

### Isosurface Extraction
```runa
Note: Extract isosurfaces using marching cubes
Let isosurface_values be [0.1, 0.3, 0.5, 0.7]
Let isosurfaces be List[Surface3D]

For Each iso_value in isosurface_values:
    Let isosurface be Surfaces.extract_isosurface(volume_data, iso_value)
    
    Note: Color based on isosurface value
    Let surface_color be Surfaces.interpolate_color(
        iso_value,
        [0.0, 1.0],
        ["blue", "red"]
    )
    
    Let colored_isosurface be Surfaces.apply_uniform_color(isosurface, surface_color)
    Add colored_isosurface to isosurfaces

Let multi_isosurface_plot be Surfaces.plot_multiple_surfaces(isosurfaces, viewer)
```

## Vector Field Visualization

### 3D Streamlines
```runa
Note: Define 3D vector field
Process called "vector_field_3d" that takes x as Float64, y as Float64, z as Float64 returns List[Float64]:
    Note: Lorenz attractor-like field
    Let dx be 10.0 * (y - x)
    Let dy be x * (28.0 - z) - y
    Let dz be x * y - (8.0/3.0) * z
    Return [dx, dy, dz]

Note: Create seed points for streamlines
Let seed_points be [
    [1.0, 1.0, 1.0], [1.0, -1.0, 1.0], [-1.0, 1.0, 1.0], [-1.0, -1.0, 1.0]
]

Let streamline_config be Dictionary[String, String] with:
    "integration_method": "runge_kutta_4"
    "step_size": "0.01"
    "max_steps": "10000"
    "min_speed": "0.001"

Let streamlines be Surfaces.compute_streamlines(
    vector_field_3d,
    seed_points,
    streamline_config
)

Note: Visualize streamlines as tubes
Let tube_config be Dictionary[String, Float64] with:
    "radius": 0.05
    "segments": 8
    "color_by_speed": 1.0

Let streamline_tubes be Surfaces.create_streamline_tubes(streamlines, tube_config)
Let streamline_plot be Surfaces.plot_surface(streamline_tubes, viewer)
```

## Lighting and Materials

### Advanced Lighting Models
```runa
Note: Configure multiple light sources
Let light_sources be List[Dictionary[String, List[Float64]]]

Note: Key light
Let key_light be Dictionary[String, List[Float64]] with:
    "position": [10.0, 10.0, 15.0]
    "color": [1.0, 1.0, 1.0]
    "intensity": [0.8]
    "type": ["directional"]

Note: Fill light
Let fill_light be Dictionary[String, List[Float64]] with:
    "position": [-10.0, 5.0, 10.0]
    "color": [0.8, 0.9, 1.0]
    "intensity": [0.3]
    "type": ["point"]

Note: Rim light
Let rim_light be Dictionary[String, List[Float64]] with:
    "position": [0.0, -15.0, 5.0]
    "color": [1.0, 0.9, 0.8]
    "intensity": [0.4]
    "type": ["spot"]

Add key_light to light_sources
Add fill_light to light_sources
Add rim_light to light_sources

Let lighting_config be Dictionary[String, List[Float64]] with:
    "ambient_color": [0.1, 0.1, 0.1]
    "ambient_intensity": [0.2]

Let lit_surface be Surfaces.apply_lighting(surface_mesh, light_sources, lighting_config)
```

### Material Properties and Textures
```runa
Note: Apply physically-based materials
Let pbr_material be Dictionary[String, Float64] with:
    "metallic": 0.0      Note: 0 = dielectric, 1 = metallic
    "roughness": 0.3     Note: 0 = mirror, 1 = completely rough  
    "base_color_r": 0.7
    "base_color_g": 0.2
    "base_color_b": 0.2
    "normal_strength": 1.0
    "emission_strength": 0.0

Note: Generate procedural texture
Let texture_function be Process that takes u as Float64, v as Float64 returns List[Float64]:
    Note: Checkerboard pattern
    Let u_check be Integer(u * 10.0) % 2
    Let v_check be Integer(v * 10.0) % 2
    If (u_check + v_check) % 2 = 0:
        Return [0.9, 0.9, 0.9]  Note: Light squares
    Otherwise:
        Return [0.1, 0.1, 0.1]  Note: Dark squares

Let textured_surface be Surfaces.apply_procedural_texture(surface_mesh, texture_function)
Let material_surface be Surfaces.apply_pbr_material(textured_surface, pbr_material)
```

## Interactive Features

### 3D Navigation and Controls
```runa
Note: Enable interactive 3D navigation
Let interaction_config be Dictionary[String, String] with:
    "rotation": "true"
    "zoom": "true"
    "pan": "true"
    "mouse_sensitivity": "1.0"
    "wheel_zoom_speed": "0.1"
    "auto_rotate": "false"

Let interactive_viewer be Surfaces.make_interactive(viewer, interaction_config)

Note: Add navigation controls UI
Let control_panel be Dictionary[String, String] with:
    "show_axes": "true"
    "show_grid": "true"
    "camera_controls": "true"
    "lighting_controls": "true"
    "material_controls": "true"

Let enhanced_interface be Surfaces.add_control_panel(interactive_viewer, control_panel)
```

### Real-time Parameter Updates
```runa
Note: Create parametric surface with adjustable parameters
Let parameter_ranges be Dictionary[String, List[Float64]] with:
    "amplitude": [0.1, 2.0]
    "frequency": [0.5, 5.0]
    "phase": [0.0, 6.283185307]

Process called "parametric_wave" that takes x as Float64, y as Float64, params as Dictionary[String, Float64] returns Float64:
    Let amplitude be params["amplitude"]
    Let frequency be params["frequency"]
    Let phase be params["phase"]
    
    Let r be MathOps.square_root(String(x*x + y*y), 15)
    Let wave_arg be frequency * Float64(r.result_value) + phase
    Let sin_wave be Trig.sine(String(wave_arg), "radians", 15)
    
    Return amplitude * Float64(sin_wave.function_value)

Let interactive_surface be Surfaces.create_parametric_interactive(
    parametric_wave,
    x_range,
    y_range,
    resolution,
    parameter_ranges
)
```

## Data Import and Export

### Mesh Data Import
```runa
Note: Import surface from standard mesh formats
Let imported_surface be Surfaces.import_mesh_file("complex_surface.obj")

Note: Validate and repair mesh
Let mesh_validation be Surfaces.validate_mesh(imported_surface)
If Length(mesh_validation.errors) > 0:
    Display "Mesh validation issues found:"
    For Each error in mesh_validation.errors:
        Display "  " joined with error.description
    
    Let repaired_mesh be Surfaces.repair_mesh(imported_surface, mesh_validation.errors)
    imported_surface = repaired_mesh

Note: Compute missing data
If Length(imported_surface.normals) = 0:
    imported_surface.normals = Surfaces.compute_vertex_normals(imported_surface)
```

### High-Quality Export
```runa
Note: Export 3D plots in various formats
Let export_config be Dictionary[String, String] with:
    "format": "png"
    "resolution": [3840, 2160]  Note: 4K resolution
    "anti_aliasing": "8x"
    "background": "transparent"
    "lighting_quality": "high"

Let high_res_export be Surfaces.export_3d_plot(plot_result, "surface_visualization.png", export_config)

Note: Export mesh data
Let mesh_export_config be Dictionary[String, String] with:
    "format": "obj"
    "include_normals": "true"
    "include_textures": "true"
    "precision": "6"

Let mesh_export be Surfaces.export_mesh(surface_mesh, "generated_surface.obj", mesh_export_config)

Note: Export for 3D printing
Let print_config be Dictionary[String, String] with:
    "format": "stl"
    "units": "millimeters"
    "scale_factor": "10.0"
    "ensure_manifold": "true"

Let printable_mesh be Surfaces.prepare_for_3d_printing(surface_mesh, print_config)
```

## Performance Optimization

### Level of Detail (LOD)
```runa
Note: Create multiple detail levels for performance
Let lod_levels be [1.0, 0.5, 0.25, 0.1]  Note: Detail reduction factors
Let multi_lod_surface be Surfaces.create_lod_surface(surface_mesh, lod_levels)

Note: Automatic LOD selection based on viewing distance
Let adaptive_lod_config be Dictionary[String, Float64] with:
    "near_distance": 5.0
    "far_distance": 50.0
    "quality_preference": 0.8  Note: 0=performance, 1=quality

Let adaptive_surface be Surfaces.setup_adaptive_lod(multi_lod_surface, adaptive_lod_config)
```

### GPU Acceleration
```runa
Note: Enable GPU-accelerated rendering
Let gpu_config be Dictionary[String, String] with:
    "use_gpu": "true"
    "vertex_buffer_size": "1048576"  Note: 1MB
    "texture_memory": "512"          Note: 512MB
    "compute_shaders": "true"

Let gpu_accelerated_plot be Surfaces.enable_gpu_acceleration(plot_result, gpu_config)

Note: Parallel mesh generation
Let parallel_config be Dictionary[String, Integer] with:
    "thread_count": 8
    "chunk_size": 1000

Let parallel_surface be Surfaces.create_surface_parallel(
    surface_function,
    x_range,
    y_range,
    [400, 400],  Note: High resolution
    parallel_config
)
```

## Error Handling and Validation

### Robust Surface Generation
```runa
Try:
    Let surface_result be Surfaces.create_function_surface(
        problematic_function,
        x_range,
        y_range,
        resolution
    )
Catch Errors.MathematicalError as math_error:
    Display "Function evaluation failed: " joined with math_error.message
    Let fallback_function be create_fallback_function(math_error.problematic_inputs)
    Let surface_result be Surfaces.create_function_surface(fallback_function, x_range, y_range, resolution)
Catch Errors.MeshGenerationError as mesh_error:
    Display "Mesh generation failed: " joined with mesh_error.message
    Let reduced_resolution be [resolution[0] / 2, resolution[1] / 2]
    Let surface_result be Surfaces.create_function_surface(surface_function, x_range, y_range, reduced_resolution)
Catch Errors.RenderingError as render_error:
    Display "Rendering failed: " joined with render_error.message
    Let simple_config be create_basic_rendering_config()
    Let surface_result be Surfaces.plot_surface_fallback(surface_mesh, simple_config)
```

## Integration with Other Modules

### Mathematical Analysis
```runa
Import "math/analysis/multivariable" as Multivariable

Note: Visualize gradient vector field
Let gradient_field be Multivariable.compute_gradient(surface_function, x_range, y_range)
Let gradient_arrows be Surfaces.create_vector_field_3d(
    gradient_field.x_component,
    gradient_field.y_component,
    gradient_field.magnitude,  Note: Use magnitude as z-component
    [x_range, y_range, [0.0, 2.0]]
)

Let combined_plot be Surfaces.combine_surface_and_vectors(surface_mesh, gradient_arrows)
```

### Differential Equations
```runa
Import "math/engine/numerical/pde" as PDE

Note: Visualize PDE solution evolution
Let pde_solution be PDE.solve_heat_equation(
    initial_condition: "exp(-(x^2 + y^2))",
    boundary_conditions: "zero",
    domain: [[-2.0, 2.0], [-2.0, 2.0]],
    time_steps: 100,
    spatial_resolution: [50, 50]
)

Note: Create animated sequence of solution evolution
Let animation_frames be List[Surface3D]
For Each time_step in pde_solution.time_steps:
    Let solution_surface be Surfaces.create_data_surface(
        pde_solution.spatial_grid.x,
        pde_solution.spatial_grid.y,
        time_step.solution_values
    )
    Add solution_surface to animation_frames

Let pde_animation be Surfaces.create_surface_animation(animation_frames, 30.0)  Note: 30 FPS
```

## Common Applications

### Scientific Visualization
```runa
Note: Visualize quantum mechanical wave function
Process called "hydrogen_wavefunction" that takes x as Float64, y as Float64, z as Float64 returns Float64:
    Note: 2p_z orbital wave function
    Let r be MathOps.square_root(String(x*x + y*y + z*z), 15)
    Let r_val be Float64(r.result_value)
    
    Note: Simplified 2p_z: z * exp(-r/2)
    Let exponential be MathOps.exponential(String(-r_val / 2.0), 15)
    Return z * Float64(exponential.result_value)

Let orbital_volume be Surfaces.create_scalar_volume(
    hydrogen_wavefunction,
    [[-8.0, 8.0], [-8.0, 8.0], [-8.0, 8.0]],
    [80, 80, 80]
)

Note: Show probability density isosurfaces
Let probability_density be Surfaces.compute_probability_density(orbital_volume)
Let isosurface_values be [0.01, 0.05, 0.1]
Let orbital_surfaces be Surfaces.extract_multiple_isosurfaces(probability_density, isosurface_values)
```

### Engineering Applications
```runa
Note: Finite element analysis visualization
Let fem_mesh be import_fem_results("stress_analysis.vtk")
Let stress_data be fem_mesh.scalar_data["von_mises_stress"]

Note: Create stress contour plot
Let stress_colors be Surfaces.map_stress_to_colors(
    stress_data,
    stress_limits: [0.0, 500.0],  Note: MPa
    color_map: "rainbow"
)

Let stress_surface be Surfaces.apply_vertex_colors(fem_mesh.surface, stress_colors)

Note: Add deformation visualization
Let displacement_scale be 10.0  Note: Exaggerate deformation
Let deformed_mesh be Surfaces.apply_displacement(
    fem_mesh.surface,
    fem_mesh.vector_data["displacement"],
    displacement_scale
)
```

### Educational Mathematics
```runa
Note: Interactive calculus visualization
Let partial_derivatives be Multivariable.compute_partial_derivatives(surface_function)

Note: Show tangent plane at clicked point
Process called "show_tangent_plane" that takes click_point as List[Float64]:
    Let tangent_plane be Multivariable.compute_tangent_plane(
        surface_function,
        click_point[0],
        click_point[1]
    )
    
    Let plane_surface be Surfaces.create_plane_surface(
        tangent_plane.point,
        tangent_plane.normal,
        extent: 2.0
    )
    
    Let educational_plot be Surfaces.add_temporary_surface(current_plot, plane_surface)
    Return educational_plot

Let interactive_calculus be Surfaces.add_click_handler(surface_plot, show_tangent_plane)
```

## Best Practices

### Surface Quality Guidelines
1. **Resolution**: Use appropriate mesh resolution for your application
2. **Normals**: Always compute or provide surface normals for proper lighting
3. **Topology**: Ensure mesh topology is correct (no holes, consistent winding)
4. **Materials**: Use physically plausible material properties
5. **Lighting**: Set up proper lighting for clear surface visualization

### Performance Optimization
```runa
Note: Optimize for interactive performance
Let performance_config be Dictionary[String, String] with:
    "target_fps": "30"
    "adaptive_quality": "true"
    "background_processing": "true"
    "memory_limit": "2048"  Note: MB

Let optimized_plot be Surfaces.optimize_for_interaction(surface_plot, performance_config)
```

### Code Organization
```runa
Note: Create reusable surface templates
Process called "create_analytical_surface" that takes func as Process, domain as List[List[Float64]] returns Surface3D:
    Let default_resolution be [100, 100]
    Let surface be Surfaces.create_function_surface(func, domain[0], domain[1], default_resolution)
    Let surface_with_normals be Surfaces.compute_vertex_normals(surface)
    Let material_surface be Surfaces.apply_default_material(surface_with_normals)
    Return material_surface
```

## Related Documentation

- **[Plotting Module](plotting.md)**: 2D plotting and basic visualization
- **[Animation Module](animation.md)**: Time-evolving and animated surfaces
- **[Graphing Module](graphing.md)**: Network and graph visualization
- **[Math Geometry](../geometry/README.md)**: Geometric computation and analysis
- **[Math Engine](../engine/README.md)**: Numerical computation backend
- **[Graphics 3D](../../../../app/graphics/3d/README.md)**: Low-level 3D graphics support

The surfaces module provides sophisticated 3D visualization capabilities essential for advanced mathematical analysis, scientific computing, and engineering applications in Runa.