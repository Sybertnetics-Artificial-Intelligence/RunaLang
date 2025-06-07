# Knowledge Graph Visualization in Runa

## Overview

Runa provides powerful tools for visualizing knowledge graphs, allowing developers to create interactive, informative representations of complex graph data. These visualization capabilities help in data exploration, pattern recognition, and presenting insights from knowledge graphs.

## Core Visualization Features

### 1. Basic Graph Visualization

Create simple visualizations with minimal configuration:

```runa
# Import the visualization module
Import KnowledgeGraph.Visualization

# Create a simple visualization from a knowledge graph
Let kg = KnowledgeGraph.connect("my_graph")
Let viz = GraphVisualizer.create()
Let visual = viz.render(kg)

# Display the visualization
visual.display()
```

### 2. Customizable Visualizations

Fine-tune your visualizations with extensive configuration options:

```runa
Let viz = GraphVisualizer.create({
    # Layout algorithms
    "layout": "force_directed",  # Options: force_directed, circular, hierarchical, radial
    
    # Visual theme
    "theme": "dark",  # Options: light, dark, custom
    "custom_colors": {
        "background": "#f5f5f5",
        "nodes": ["#3366cc", "#dc3912", "#ff9900"],
        "edges": ["#666666", "#333333"]
    },
    
    # Node representation
    "node_size_property": "importance",  # Scale nodes based on a property
    "node_color_property": "category",   # Color nodes based on a property
    "node_label_property": "name",       # Property to use for labels
    
    # Edge representation
    "edge_width_property": "weight",     # Scale edges based on a property
    "edge_color_property": "type",       # Color edges based on relationship type
    "edge_arrow": true,                  # Show directional arrows
    
    # Interaction
    "interactive": true,                 # Enable user interaction
    "zoom_enabled": true,                # Allow zooming
    "pan_enabled": true,                 # Allow panning
    "tooltip_properties": ["name", "description", "created_date"]
})
```

### 3. Subgraph Visualization

Visualize specific parts of your knowledge graph:

```runa
# Visualize results from a query
Let results = kg.query("MATCH (p:Person)-[:KNOWS]->(friend) RETURN p, friend")
Let subgraph_viz = viz.render(results)

# Visualize specific entities and their relationships
Let entities = kg.get_entities(["entity1", "entity2", "entity3"])
Let neighborhood = kg.get_neighborhood(entities, {
    "max_distance": 2,
    "relationship_types": ["KNOWS", "WORKS_WITH"]
})
Let neighborhood_viz = viz.render(neighborhood)
```

### 4. Dynamic and Interactive Visualizations

Create visualizations that respond to user interactions:

```runa
# Create an interactive visualization
Let interactive_viz = GraphVisualizer.create({
    "interactive": true,
    "tooltip_enabled": true,
    "highlight_neighbors": true,  # Highlight connected nodes on hover
    "filter_panel": true,         # Add UI controls for filtering
    "search_enabled": true        # Add search functionality
})

# Add event handlers
Let visualization = interactive_viz.render(kg)
visualization.on_node_click(node => {
    Console.log("Selected node:", node.properties.name)
    # Fetch additional data about the node
    Let details = kg.get_entity_details(node.id)
    UI.panel("details").update(details)
})

# Add interactive filtering
visualization.add_filter("relationship_type", {
    "type": "multiselect",
    "options": ["KNOWS", "WORKS_WITH", "MANAGES"],
    "default": ["KNOWS", "WORKS_WITH"]
})
```

### 5. Time-Based Visualization

Visualize how knowledge graphs evolve over time:

```runa
# Create a time-series visualization
Let time_viz = GraphVisualizer.create({
    "time_based": true,
    "time_property": "timestamp",
    "time_interval": "months",
    "animation_speed": 500,  # ms per frame
    "show_timeline": true
})

# Render time-based visualization
Let time_visual = time_viz.render(historical_kg)

# Add time controls
time_visual.add_time_control({
    "type": "slider",
    "play_button": true,
    "speed_control": true
})
```

## Advanced Visualization Features

### 1. Graph Analytics Visualization

Visualize analytical insights from your knowledge graph:

```runa
# Calculate metrics
Let algorithms = GraphAlgorithms.create(kg)
Let centrality = algorithms.page_rank()
Let communities = algorithms.community_detection("louvain")

# Visualize with analytics
Let analytics_viz = GraphVisualizer.create({
    "node_size_property": "pagerank_score",
    "node_color_property": "community_id",
    "display_legend": true,
    "legend_title": "Communities"
})

# Combine graph with analytics results
Let enriched_graph = kg.enrich({
    "pagerank_score": centrality.scores,
    "community_id": communities.assignments
})

Let analytics_visual = analytics_viz.render(enriched_graph)
```

### 2. 3D Graph Visualization

Create three-dimensional visualizations for complex graphs:

```runa
# Create a 3D visualization
Let viz_3d = GraphVisualizer.create({
    "dimensions": 3,
    "layout": "force_directed_3d",
    "camera_controls": true,
    "node_geometry": "sphere",  # Options: sphere, cube, custom
    "edge_geometry": "line"     # Options: line, tube, arrow
})

Let visual_3d = viz_3d.render(kg)
```

### 3. Geo-Spatial Graph Visualization

Visualize knowledge graphs with geographical components:

```runa
# Create a geo-visualization
Let geo_viz = GraphVisualizer.create({
    "type": "geo",
    "map_style": "light",  # Options: light, dark, satellite, streets
    "lat_property": "latitude",
    "lng_property": "longitude",
    "region_property": "country",  # For choropleth maps
    "value_property": "importance"
})

Let geo_visual = geo_viz.render(geo_enriched_kg)
```

### 4. Custom Rendering Functions

Create custom visual representations for nodes and edges:

```runa
Let custom_viz = GraphVisualizer.create()

# Custom node renderer
custom_viz.set_node_renderer(node => {
    If node.type == "Person":
        Return {
            "shape": "circle",
            "radius": 5 + (node.properties.influence * 3),
            "color": gender_color_map[node.properties.gender],
            "icon": "user"
        }
    Else If node.type == "Organization":
        Return {
            "shape": "rectangle",
            "width": 20,
            "height": 15,
            "color": industry_color_map[node.properties.industry],
            "icon": "building"
        }
})

# Custom edge renderer
custom_viz.set_edge_renderer(edge => {
    Let thickness = Math.log(edge.properties.strength + 1)
    Let dash_pattern = edge.properties.confirmed ? "solid" : "dashed"
    
    Return {
        "width": thickness,
        "style": dash_pattern,
        "color": relationship_color_map[edge.type],
        "arrow_size": thickness * 2
    }
})
```

## Integration with Web and UI Components

### 1. Web Integration

Embed visualizations in web applications:

```runa
# Create a web-embeddable visualization
Let web_viz = GraphVisualizer.create({
    "target": "div#graph-container",
    "responsive": true,
    "height": "500px",
    "width": "100%"
})

# Export visualization for web embedding
Let html_component = web_viz.render(kg).to_html_component()
File.write("graph_component.html", html_component)

# Or embed directly into a Runa web app
UI.embed("graph-container", html_component)
```

### 2. Dashboard Integration

Create dashboards with multiple visualizations:

```runa
# Create a dashboard with multiple views
Let dashboard = Dashboard.create("Knowledge Graph Insights")

# Add multiple visualizations
dashboard.add_panel("Overview", overview_viz)
dashboard.add_panel("Communities", community_viz)
dashboard.add_panel("Important Entities", central_nodes_viz)
dashboard.add_panel("Geo Distribution", geo_viz)

# Configure layout
dashboard.set_layout([
    ["Overview", "Communities"],
    ["Important Entities", "Geo Distribution"]
])

# Add controls
dashboard.add_filter("Global Filter", {
    "type": "date_range",
    "affects": ["Overview", "Communities"]
})

# Display dashboard
dashboard.display()
```

## Export and Sharing

Export visualizations to various formats:

```runa
# Export to image formats
visual.export("graph.png")
visual.export("graph.svg")

# Export to interactive formats
visual.export("graph.html")  # Self-contained HTML
visual.export("graph.json")  # Data for custom rendering

# Print high-quality version
visual.print({
    "dpi": 300,
    "size": "A4",
    "orientation": "landscape"
})

# Share visualization
Let share_url = visual.share({
    "public": true,
    "editable": false,
    "expiry": "30d"
})
```

## Example: Building a Knowledge Graph Explorer Application

```runa
Process called "create_kg_explorer_app":
    # Initialize knowledge graph
    Let kg = KnowledgeGraph.connect("research_knowledge")
    
    # Create visualization components
    Let main_view = GraphVisualizer.create({
        "interactive": true,
        "layout": "force_directed",
        "node_size_property": "importance",
        "node_color_property": "type",
        "theme": "light"
    })
    
    Let detail_view = GraphVisualizer.create({
        "layout": "hierarchical",
        "direction": "LR",
        "node_label_property": "name",
        "edge_label_property": "relationship"
    })
    
    # Set up application UI
    Let app = Application.create("Knowledge Explorer")
    app.add_view("main", main_view.render(kg))
    app.add_view("details", detail_view)
    app.add_panel("info", Panel.create())
    
    # Add interaction handlers
    app.get_view("main").on_node_click(node => {
        Let neighborhood = kg.get_neighborhood(node.id, { "max_distance": 1 })
        app.get_view("details").update(neighborhood)
        
        Let info = kg.get_entity_details(node.id)
        app.get_panel("info").update(format_entity_info(info))
    })
    
    # Add search functionality
    app.add_search_box(query => {
        Let results = kg.search(query)
        app.get_view("main").highlight_nodes(results.map(r => r.id))
        Return results.map(r => r.properties.name)
    })
    
    # Start the application
    app.start()
    
    Return app

# Helper function for formatting entity information
Process called "format_entity_info"(info):
    Let formatted = "<div class='entity-info'>"
    formatted += "<h2>" + info.name + "</h2>"
    formatted += "<p class='entity-type'>" + info.type + "</p>"
    
    formatted += "<h3>Properties</h3>"
    formatted += "<ul>"
    For prop in info.properties:
        formatted += "<li><strong>" + prop.key + ":</strong> " + prop.value + "</li>"
    formatted += "</ul>"
    
    formatted += "<h3>Relationships</h3>"
    formatted += "<ul>"
    For rel in info.relationships:
        formatted += "<li><strong>" + rel.type + ":</strong> " + rel.target_name + "</li>"
    formatted += "</ul>"
    
    formatted += "</div>"
    Return formatted
```

## Best Practices for Knowledge Graph Visualization

1. **Focus on Clarity**: Limit the number of nodes and edges displayed at once to prevent visual overload.

2. **Use Visual Hierarchy**: Size and color nodes based on importance to guide users' attention.

3. **Interactive Filtering**: Provide ways for users to filter and focus on subsets of the graph.

4. **Consistent Visual Language**: Maintain consistent visual encoding (colors, shapes) throughout your visualizations.

5. **Context First**: Start with overview visualizations before diving into details.

6. **Performance Consideration**: For large graphs, use techniques like clustering, sampling, or progressive loading.

## References

- [Runa Visualization API Reference](https://runa-lang.org/docs/api/visualization)
- [Knowledge Graph Visualization Guide](https://runa-lang.org/docs/guides/kg-visualization)
- [Interactive Visualization Examples](https://runa-lang.org/examples/visualization-gallery)

For complete visualization examples, see the [Knowledge Graph Visualization Examples](../../src/tests/examples/kg_visualization_examples.runa) in the Runa codebase. 