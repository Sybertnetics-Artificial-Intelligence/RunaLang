# Knowledge Graph Visualization in Runa

## Overview

Runa's Knowledge Graph visualization tools allow developers to explore and understand complex code relationships through interactive visual representations. This document covers the various visualization options available and how to implement them in your Runa applications.

## Basic Visualization

```runa
import runa.ai.knowledge_graph as kg
import runa.ai.visualization as viz

// Initialize the knowledge graph
let graph = kg.KnowledgeManager.get_instance()

// Create a basic visualization
let basic_view = viz.GraphVisualizer(graph)
basic_view.render("basic_graph.html")
```

## Visualization Types

### Dependency Graph

Visualize module dependencies across your codebase:

```runa
let dep_viz = viz.DependencyVisualizer(graph)
dep_viz.filter_by_module("core")
dep_viz.render("dependency_graph.html")
```

### Call Graph

Visualize function call relationships:

```runa
let call_viz = viz.CallGraphVisualizer(graph)
call_viz.set_root_function("main")
call_viz.set_depth(3)
call_viz.render("call_graph.html")
```

### Type Hierarchy

Visualize inheritance and composition relationships:

```runa
let type_viz = viz.TypeHierarchyVisualizer(graph)
type_viz.add_type("BaseClass")
type_viz.include_subtypes(true)
type_viz.render("type_hierarchy.html")
```

### Semantic Knowledge Map

Visualize semantic relationships between code concepts:

```runa
let semantic_viz = viz.SemanticMapVisualizer(graph)
semantic_viz.focus_on_concept("error handling")
semantic_viz.render("semantic_map.html")
```

## Customization Options

### Styling

```runa
let styled_viz = viz.GraphVisualizer(graph)
styled_viz.set_node_color("function", "#3498db")
styled_viz.set_node_size("class", 15)
styled_viz.set_edge_style("calls", {color: "#e74c3c", width: 2, dashed: true})
styled_viz.render("styled_graph.html")
```

### Layout Algorithms

```runa
let viz = viz.GraphVisualizer(graph)
// Available layouts: force, radial, hierarchical, circular
viz.set_layout("hierarchical")
viz.render("hierarchical_layout.html")
```

### Interactivity

```runa
let interactive_viz = viz.GraphVisualizer(graph)
interactive_viz.enable_zoom(true)
interactive_viz.enable_drag(true)
interactive_viz.enable_hover_details(true)
interactive_viz.enable_search(true)
interactive_viz.render("interactive_graph.html", {interactive: true})
```

## Advanced Features

### Filtering and Focus

```runa
let viz = viz.GraphVisualizer(graph)
// Focus on specific components
viz.filter_nodes(node => node.type == "class" || node.type == "function")
viz.filter_edges(edge => edge.type == "inherits" || edge.type == "calls")
viz.render("filtered_graph.html")
```

### Time-based Visualization

```runa
let evolution_viz = viz.EvolutionVisualizer(graph)
evolution_viz.set_timespan("2023-01-01", "2023-12-31")
evolution_viz.set_interval("month")
evolution_viz.render("code_evolution.html")
```

### Integration with IDE

```runa
// In your IDE extension/plugin
let ide_viz = viz.IDEIntegratedVisualizer(graph)
ide_viz.link_to_editor(true)  // Enable clicking on nodes to navigate to code
ide_viz.show_in_panel("knowledge_panel")
```

## Export Options

```runa
let viz = viz.GraphVisualizer(graph)
// Available formats: html, svg, png, json
viz.export("graph.svg")
viz.export("graph.png", {width: 1920, height: 1080})
viz.export_data("graph_data.json")
```

## Best Practices

1. **Start with high-level views** and then drill down into specific components
2. **Use filtering** to manage visual complexity for large codebases
3. **Color-code node types** consistently for better readability
4. **Add interactive features** for exploratory analysis
5. **Combine multiple visualization types** for comprehensive understanding

## Example: Comprehensive Code Analysis Dashboard

```runa
import runa.ai.knowledge_graph as kg
import runa.ai.visualization as viz
import runa.ui.dashboard as dash

// Initialize components
let graph = kg.KnowledgeManager.get_instance()
let dashboard = dash.Dashboard("Code Analysis")

// Add different visualization panels
let dep_panel = dashboard.add_panel("Dependencies")
let dep_viz = viz.DependencyVisualizer(graph)
dep_panel.set_content(dep_viz)

let call_panel = dashboard.add_panel("Call Graph")
let call_viz = viz.CallGraphVisualizer(graph)
call_panel.set_content(call_viz)

let type_panel = dashboard.add_panel("Type Hierarchy")
let type_viz = viz.TypeHierarchyVisualizer(graph)
type_panel.set_content(type_viz)

// Setup interactivity between panels
dashboard.link_selections(true)

// Render the dashboard
dashboard.render("analysis_dashboard.html")
```

## Troubleshooting

- **Performance issues with large graphs**: Use filtering or pagination
- **Visual clutter**: Adjust layout algorithm or reduce node/edge visibility
- **Browser compatibility**: Use Chrome or Firefox for best results
- **Export errors**: Check for valid file paths and permissions

## Conclusion

Knowledge Graph visualization is a powerful tool for understanding complex code relationships. By effectively utilizing these visualization techniques, developers can gain valuable insights into their codebase structure, dependencies, and semantic relationships. 