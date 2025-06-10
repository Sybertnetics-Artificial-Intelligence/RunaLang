# Knowledge Graph Visualization in Runa

## Overview

Runa provides powerful visualization capabilities for knowledge graphs, enabling developers to create interactive, customizable graph visualizations for exploring relationships, understanding data structure, and presenting insights. The visualization system integrates seamlessly with Runa's knowledge graph features.

## Core Features

### 1. Basic Graph Visualization

Create simple visualizations of knowledge graphs:

```
# Create a knowledge graph visualizer
Let visualizer be KnowledgeGraphVisualizer.create with dictionary with:
    "layout_algorithm" as "force_directed"  # Options: force_directed, hierarchical, circular, grid
    "node_styling" as dictionary with:
        "size_attribute" as "importance"
        "color_attribute" as "type"
        "label_attribute" as "name"
    "edge_styling" as dictionary with:
        "width_attribute" as "strength"
        "color_attribute" as "relationship_type"

# Load and visualize a knowledge graph
Let kg be KnowledgeGraph.load with "./data/project_knowledge.kg"
Let visualization be visualizer.visualize with kg

# Display the visualization
Call visualization.show
```

### 2. Interactive Visualization

Create interactive visualizations with user controls:

```
# Create an interactive visualizer
Let interactive_viz be InteractiveKnowledgeGraphViz.create with dictionary with:
    "enable_pan_zoom" as true
    "enable_node_selection" as true
    "enable_context_menu" as true
    "enable_search" as true

# Configure interaction behaviors
Call interactive_viz.configure_interactions with dictionary with:
    "node_click_action" as "show_details"
    "node_hover_action" as "highlight_neighbors"
    "edge_click_action" as "show_relationship_info"
    "double_click_action" as "expand_subgraph"

# Create the interactive visualization
Let interactive_graph be interactive_viz.create_visualization with kg

# Add custom controls
Call interactive_graph.add_control with "node_filter" and dictionary with:
    "filter_by" as "node_type"
    "available_types" as kg.get_node_types
    "default_selection" as "all"

Call interactive_graph.add_control with "relationship_filter" and dictionary with:
    "filter_by" as "relationship_type"
    "available_types" as kg.get_relationship_types
```

### 3. Advanced Layout Algorithms

Use sophisticated layout algorithms for better visualization:

```
# Create a hierarchical layout
Let hierarchical_viz be HierarchicalGraphVisualizer.create with dictionary with:
    "root_nodes" as kg.find_root_nodes
    "hierarchy_attribute" as "level"
    "direction" as "top_down"  # Options: top_down, bottom_up, left_right, right_left

# Apply clustering before visualization
Let clustered_viz be ClusteredGraphVisualizer.create with dictionary with:
    "clustering_algorithm" as "community_detection"
    "cluster_colors" as list containing "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7"
    "show_cluster_boundaries" as true

# Create a time-based layout for temporal graphs
Let temporal_viz be TemporalGraphVisualizer.create with dictionary with:
    "time_attribute" as "timestamp"
    "animation_duration" as 5000  # milliseconds
    "show_timeline_control" as true
```

### 4. Custom Node and Edge Styling

Customize the appearance of graph elements:

```
# Define custom node styling based on attributes
Let node_styler be NodeStyler.create

Call node_styler.add_style_rule with dictionary with:
    "condition" as "node.type == 'Person'"
    "style" as dictionary with:
        "shape" as "circle"
        "color" as "#FF6B6B"
        "size" as "node.importance * 10"
        "label_font_size" as 12

Call node_styler.add_style_rule with dictionary with:
    "condition" as "node.type == 'Project'"
    "style" as dictionary with:
        "shape" as "rectangle"
        "color" as "#4ECDC4"
        "size" as 20
        "border_width" as 2

# Define custom edge styling
Let edge_styler be EdgeStyler.create

Call edge_styler.add_style_rule with dictionary with:
    "condition" as "edge.relationship_type == 'WORKS_ON'"
    "style" as dictionary with:
        "color" as "#45B7D1"
        "width" as "edge.strength * 3"
        "style" as "solid"

# Apply custom styling to visualizer
Call visualizer.apply_node_styler with node_styler
Call visualizer.apply_edge_styler with edge_styler
```

### 5. Multi-layer and Subgraph Visualization

Visualize complex graphs with multiple layers or focus on subgraphs:

```
# Create a multi-layer visualization
Let multi_layer_viz be MultiLayerGraphVisualizer.create

# Define layers based on relationship types
Call multi_layer_viz.add_layer with "collaboration" and dictionary with:
    "relationships" as list containing "WORKS_WITH", "COLLABORATES_ON"
    "color_scheme" as "blue_theme"
    "visible" as true

Call multi_layer_viz.add_layer with "hierarchy" and dictionary with:
    "relationships" as list containing "REPORTS_TO", "MANAGES"
    "color_scheme" as "red_theme"
    "visible" as false

# Create subgraph visualization
Let subgraph_viz be SubgraphVisualizer.create

# Extract and visualize a neighborhood around a specific node
Let neighborhood_graph be kg.extract_neighborhood with:
    center_node as "Alice Smith"
    max_distance as 2
    relationship_types as list containing "WORKS_ON", "KNOWS", "COLLABORATES_WITH"

Let neighborhood_viz be subgraph_viz.visualize_subgraph with neighborhood_graph
```

### 6. Export and Sharing

Export visualizations in various formats:

```
# Export static images
Call visualization.export_image with dictionary with:
    "format" as "png"  # Options: png, svg, pdf, jpg
    "filename" as "./exports/knowledge_graph.png"
    "width" as 1920
    "height" as 1080
    "dpi" as 300

# Export interactive HTML
Call interactive_graph.export_html with dictionary with:
    "filename" as "./exports/interactive_graph.html"
    "include_controls" as true
    "standalone" as true  # Include all dependencies

# Export data for external tools
Call visualization.export_data with dictionary with:
    "format" as "graphml"  # Options: graphml, gexf, json, csv
    "filename" as "./exports/graph_data.graphml"
    "include_styling" as true
```

## Advanced Visualization Features

### 1. Dynamic and Animated Visualizations

Create visualizations that change over time:

```
# Create an animated visualization showing graph evolution
Let animator be GraphAnimator.create with dictionary with:
    "frame_duration" as 1000  # milliseconds per frame
    "transition_type" as "smooth"  # Options: smooth, discrete, bounce

# Define animation keyframes
Let keyframes be list containing:
    dictionary with:
        "timestamp" as 0
        "graph_state" as kg.get_state_at_time with "2023-01-01"
    dictionary with:
        "timestamp" as 1000
        "graph_state" as kg.get_state_at_time with "2023-06-01"
    dictionary with:
        "timestamp" as 2000
        "graph_state" as kg.get_state_at_time with "2023-12-01"

Let animated_viz be animator.create_animation with:
    keyframes as keyframes
    animation_controls as true
```

### 2. 3D Visualization

Create three-dimensional graph visualizations:

```
# Create a 3D visualizer
Let viz_3d be Graph3DVisualizer.create with dictionary with:
    "layout_algorithm" as "force_directed_3d"
    "camera_controls" as dictionary with:
        "enable_rotation" as true
        "enable_zoom" as true
        "auto_rotate" as false
    "lighting" as dictionary with:
        "ambient_intensity" as 0.4
        "directional_intensity" as 0.8
        "shadows" as true

# Configure 3D-specific styling
Let sphere_nodes be viz_3d.create_node_style with dictionary with:
    "geometry" as "sphere"
    "material" as "phong"
    "size_multiplier" as 1.5

Let cylinder_edges be viz_3d.create_edge_style with dictionary with:
    "geometry" as "cylinder"
    "material" as "basic"
    "curve_factor" as 0.1

# Create and display 3D visualization
Let graph_3d be viz_3d.visualize with kg
Call graph_3d.show_in_browser
```

### 3. Real-time Collaborative Visualization

Enable multiple users to explore graphs together:

```
# Create a collaborative visualization session
Let collab_viz be CollaborativeGraphVisualizer.create with dictionary with:
    "session_id" as "project_exploration_session"
    "websocket_server" as "ws://localhost:8080/graph_session"
    "sync_viewport" as true
    "shared_selections" as true

# Configure collaboration features
Call collab_viz.enable_user_cursors with dictionary with:
    "show_user_names" as true
    "cursor_colors" as "auto_assign"

Call collab_viz.enable_shared_annotations with dictionary with:
    "allow_text_notes" as true
    "allow_drawing" as true
    "persist_annotations" as true

# Start collaborative session
Let session be collab_viz.start_session with kg
Call session.invite_users with list containing "user1@example.com", "user2@example.com"
```

## Integration with Runa Development Workflow

### Code Dependency Visualization

```
# Visualize code dependencies and relationships
Let code_viz be CodeDependencyVisualizer.create

# Extract dependency graph from codebase
Let dependency_graph be code_viz.extract_dependencies with:
    source_path as "./src/"
    include_patterns as list containing "*.runa"
    dependency_types as list containing "imports", "function_calls", "class_inheritance"

# Create hierarchical visualization of code structure
Let code_visualization be code_viz.create_hierarchy_view with:
    graph as dependency_graph
    grouping_strategy as "by_module"
    show_external_dependencies as false

# Add interactivity for code exploration
Call code_visualization.add_code_preview with dictionary with:
    "show_on_hover" as true
    "syntax_highlighting" as true
    "max_lines" as 20
```

### Documentation and Knowledge Mapping

```
# Create a comprehensive knowledge map
Let knowledge_mapper be KnowledgeMapper.create

# Combine multiple knowledge sources
Let knowledge_sources be list containing:
    kg  # Main knowledge graph
    dependency_graph  # Code dependencies
    code_viz.extract_api_graph with "./api/"  # API relationships

Let comprehensive_graph be knowledge_mapper.merge_graphs with:
    graphs as knowledge_sources
    merge_strategy as "entity_matching"
    confidence_threshold as 0.8

# Create an explorable knowledge map
Let knowledge_map be knowledge_mapper.create_knowledge_map with:
    graph as comprehensive_graph
    map_type as "concept_map"
    enable_search as true
    enable_filtering as true
```

## Example: Creating a Project Overview Dashboard

```
Process called "create_project_dashboard":
    # Load project knowledge graph
    Let project_kg be KnowledgeGraph.load with "./project_knowledge.kg"
    
    # Create dashboard layout
    Let dashboard be GraphDashboard.create with dictionary with:
        "layout" as "grid"
        "columns" as 2
        "responsive" as true
    
    # Add team structure visualization
    Let team_subgraph be project_kg.filter_by_types with list containing "Person", "Team", "Role"
    Let team_viz be dashboard.add_panel with "team_structure" and dictionary with:
        "title" as "Team Structure"
        "visualization_type" as "hierarchical"
        "data" as team_subgraph
    
    # Add project timeline
    Let timeline_data be project_kg.filter_by_attribute with "timestamp"
    Let timeline_viz be dashboard.add_panel with "project_timeline" and dictionary with:
        "title" as "Project Timeline"
        "visualization_type" as "temporal"
        "data" as timeline_data
    
    # Add technology stack overview
    Let tech_subgraph be project_kg.filter_by_types with list containing "Technology", "Framework", "Tool"
    Let tech_viz be dashboard.add_panel with "tech_stack" and dictionary with:
        "title" as "Technology Stack"
        "visualization_type" as "clustered"
        "data" as tech_subgraph
    
    # Add real-time metrics
    Let metrics_panel be dashboard.add_panel with "metrics" and dictionary with:
        "title" as "Project Metrics"
        "visualization_type" as "metrics_overlay"
        "refresh_interval" as 30000  # 30 seconds
    
    # Configure interactivity between panels
    Call dashboard.link_panels with dictionary with:
        "selection_sync" as true
        "filter_sync" as true
        "highlight_sync" as true
    
    # Export dashboard
    Call dashboard.export_html with "./project_dashboard.html"
    
    Return dashboard
```

## Best Practices

1. **Performance Optimization**: For large graphs, use level-of-detail rendering and clustering to maintain performance.

2. **User Experience**: Provide clear navigation controls and context information to help users understand the visualization.

3. **Accessibility**: Ensure visualizations are accessible with proper color contrast and alternative text representations.

4. **Responsiveness**: Design visualizations that work well on different screen sizes and devices.

5. **Data Quality**: Ensure the underlying knowledge graph data is clean and well-structured for effective visualization.

## References

- [Runa Visualization API Documentation](https://runa-lang.org/docs/api/visualization)
- [Graph Visualization Examples](../../src/tests/examples/kg_visualization_examples.runa)
- [Interactive Dashboard Templates](../../templates/visualization/) 