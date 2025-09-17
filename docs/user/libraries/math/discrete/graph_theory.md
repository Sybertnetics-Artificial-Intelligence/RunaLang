# Graph Theory Module

The Graph Theory module provides comprehensive tools for modeling, analyzing, and manipulating graphs and networks. This module supports both theoretical graph operations and practical network analysis applications.

## Quick Start

```runa
Import "math/discrete/graph_theory" as GraphTheory

Note: Create a simple graph
Let graph be GraphTheory.create_graph()
Let node_a be GraphTheory.add_vertex(graph, "A")
Let node_b be GraphTheory.add_vertex(graph, "B") 
Let edge be GraphTheory.add_edge(graph, node_a, node_b, 5)

Note: Find shortest path
Let path be GraphTheory.shortest_path(graph, node_a, node_b)
Display "Shortest path: " joined with GraphTheory.path_to_string(path)
```

## Core Concepts

### Graph Representation

Graphs can be represented in multiple formats:
- **Adjacency Matrix**: Efficient for dense graphs
- **Adjacency List**: Memory-efficient for sparse graphs  
- **Edge List**: Simple representation for basic operations
- **Incidence Matrix**: Useful for theoretical analysis

### Graph Types

The module supports various graph types:
- **Simple Graphs**: No self-loops or multiple edges
- **Multigraphs**: Allow multiple edges between vertices
- **Directed Graphs**: Edges have direction
- **Weighted Graphs**: Edges have associated weights
- **Bipartite Graphs**: Vertices can be divided into two disjoint sets

## Graph Creation and Modification

### Basic Graph Operations

```runa
Import "math/discrete/graph_theory" as GT

Note: Create different types of graphs
Let undirected_graph be GT.create_undirected_graph()
Let directed_graph be GT.create_directed_graph()
Let weighted_graph be GT.create_weighted_graph()

Note: Add vertices
Let vertices be GT.add_vertices(undirected_graph, ["A", "B", "C", "D"])

Note: Add edges with various properties
Let edge1 be GT.add_edge(undirected_graph, "A", "B")
Let edge2 be GT.add_weighted_edge(weighted_graph, "A", "B", 3.5)
Let edge3 be GT.add_directed_edge(directed_graph, "A", "B")

Note: Remove elements
GT.remove_vertex(undirected_graph, "D")
GT.remove_edge(undirected_graph, "A", "B")
```

### Graph Properties Query

```runa
Note: Basic graph information
Let vertex_count be GT.vertex_count(graph)
Let edge_count be GT.edge_count(graph)
Let is_connected be GT.is_connected(graph)
Let is_cyclic be GT.has_cycle(graph)

Display "Graph has " joined with vertex_count joined with " vertices"
Display "Graph has " joined with edge_count joined with " edges"
Display "Is connected: " joined with is_connected
```

## Graph Traversal Algorithms

### Depth-First Search (DFS)

```runa
Note: Standard DFS traversal
Let dfs_order be GT.depth_first_search(graph, start_vertex)
Display "DFS traversal: " joined with GT.vertex_list_to_string(dfs_order)

Note: DFS with custom visitor function
Process called "visit_vertex" that takes vertex as String returns Nothing:
    Display "Visiting: " joined with vertex

Let dfs_result be GT.dfs_with_visitor(graph, start_vertex, visit_vertex)
```

### Breadth-First Search (BFS)

```runa
Note: Standard BFS traversal
Let bfs_order be GT.breadth_first_search(graph, start_vertex)
Display "BFS traversal: " joined with GT.vertex_list_to_string(bfs_order)

Note: BFS for shortest unweighted path
Let shortest_unweighted be GT.bfs_shortest_path(graph, "A", "D")
Display "Shortest unweighted path length: " joined with GT.path_length(shortest_unweighted)
```

## Shortest Path Algorithms

### Dijkstra's Algorithm

```runa
Note: Find shortest paths from single source
Let distances be GT.dijkstra(weighted_graph, source_vertex)
Let path_to_target be GT.dijkstra_path(weighted_graph, source_vertex, target_vertex)

Display "Distance to all vertices:"
GT.display_distance_table(distances)

Display "Path to target: " joined with GT.path_to_string(path_to_target)
```

### Floyd-Warshall Algorithm

```runa
Note: All-pairs shortest paths
Let all_distances be GT.floyd_warshall(weighted_graph)
Let path_matrix be GT.floyd_warshall_paths(weighted_graph)

Note: Query specific path
Let distance_ab be GT.get_distance(all_distances, "A", "B")
Let path_ab be GT.get_path(path_matrix, "A", "B")
```

### Bellman-Ford Algorithm

```runa
Note: Handle negative edge weights
Let bf_result be GT.bellman_ford(weighted_graph, source_vertex)

If GT.has_negative_cycle(bf_result):
    Display "Graph contains negative cycle"
Otherwise:
    Let distances be GT.get_distances(bf_result)
    GT.display_distance_table(distances)
```

## Minimum Spanning Tree

### Kruskal's Algorithm

```runa
Note: Find MST using Kruskal's algorithm
Let mst_kruskal be GT.kruskal_mst(weighted_graph)
Let mst_weight be GT.total_weight(mst_kruskal)

Display "MST weight (Kruskal): " joined with mst_weight
GT.display_edge_list(GT.get_edges(mst_kruskal))
```

### Prim's Algorithm

```runa
Note: Find MST using Prim's algorithm
Let mst_prim be GT.prim_mst(weighted_graph, start_vertex)
Let mst_weight_prim be GT.total_weight(mst_prim)

Display "MST weight (Prim): " joined with mst_weight_prim
```

## Graph Coloring

### Vertex Coloring

```runa
Note: Basic graph coloring
Let coloring be GT.greedy_vertex_coloring(graph)
Let chromatic_number be GT.chromatic_number(coloring)

Display "Chromatic number: " joined with chromatic_number
GT.display_coloring(coloring)

Note: Optimal coloring for specific cases
Let bipartite_coloring be GT.bipartite_coloring(graph)
If GT.is_valid_coloring(bipartite_coloring):
    Display "Graph is bipartite"
```

### Edge Coloring

```runa
Note: Color edges to avoid conflicts
Let edge_coloring be GT.edge_coloring(graph)
Let edge_chromatic_number be GT.edge_chromatic_number(edge_coloring)

Display "Edge chromatic number: " joined with edge_chromatic_number
```

## Network Flow Algorithms

### Maximum Flow

```runa
Note: Find maximum flow using Ford-Fulkerson
Let max_flow_value be GT.max_flow_ford_fulkerson(flow_network, source, sink)
Let flow_paths be GT.get_flow_paths(flow_network, source, sink)

Display "Maximum flow value: " joined with max_flow_value

Note: Edmonds-Karp implementation
Let ek_flow be GT.max_flow_edmonds_karp(flow_network, source, sink)
```

### Minimum Cut

```runa
Note: Find minimum cut
Let min_cut be GT.minimum_cut(flow_network, source, sink)
Let cut_capacity be GT.cut_capacity(min_cut)

Display "Minimum cut capacity: " joined with cut_capacity
GT.display_cut_vertices(GT.get_cut_vertices(min_cut))
```

## Graph Analysis and Metrics

### Centrality Measures

```runa
Note: Calculate various centrality metrics
Let degree_centrality be GT.degree_centrality(graph)
Let betweenness_centrality be GT.betweenness_centrality(graph)
Let closeness_centrality be GT.closeness_centrality(graph)
Let eigenvector_centrality be GT.eigenvector_centrality(graph)

Note: Display most central vertices
Let top_degree be GT.top_vertices_by_centrality(degree_centrality, 3)
Display "Top vertices by degree centrality:"
GT.display_centrality_ranking(top_degree)
```

### Clustering and Community Detection

```runa
Note: Analyze graph structure
Let clustering_coefficient be GT.clustering_coefficient(graph)
Let global_clustering be GT.global_clustering_coefficient(graph)

Display "Average clustering coefficient: " joined with clustering_coefficient

Note: Community detection
Let communities be GT.detect_communities(graph)
Display "Number of communities: " joined with GT.community_count(communities)
GT.display_communities(communities)
```

## Special Graph Types

### Trees and Forests

```runa
Note: Tree-specific operations
Let is_tree be GT.is_tree(graph)
Let is_forest be GT.is_forest(graph)

If is_tree:
    Let tree_diameter be GT.tree_diameter(graph)
    Let tree_center be GT.tree_center(graph)
    Display "Tree diameter: " joined with tree_diameter
    Display "Tree center: " joined with GT.vertex_list_to_string(tree_center)
```

### Complete and Regular Graphs

```runa
Note: Generate special graph types
Let complete_graph be GT.complete_graph(5)
Let cycle_graph be GT.cycle_graph(6)
Let wheel_graph be GT.wheel_graph(7)
Let regular_graph be GT.k_regular_graph(4, 3)

Note: Verify properties
Let is_complete be GT.is_complete_graph(complete_graph)
Let is_regular be GT.is_regular_graph(regular_graph)
```

## Graph Algorithms for Optimization

### Traveling Salesman Problem

```runa
Note: Solve TSP using various approaches
Let tsp_nearest_neighbor be GT.tsp_nearest_neighbor(weighted_complete_graph)
Let tsp_optimal_small be GT.tsp_dynamic_programming(weighted_complete_graph)

Display "TSP tour length (nearest neighbor): " joined with GT.tour_length(tsp_nearest_neighbor)
Display "TSP tour: " joined with GT.tour_to_string(tsp_nearest_neighbor)
```

### Hamiltonian and Eulerian Paths

```runa
Note: Find special paths
Let hamiltonian_path be GT.find_hamiltonian_path(graph)
Let eulerian_path be GT.find_eulerian_path(graph)

If GT.has_hamiltonian_path(hamiltonian_path):
    Display "Hamiltonian path: " joined with GT.path_to_string(hamiltonian_path)

If GT.has_eulerian_path(eulerian_path):
    Display "Eulerian path: " joined with GT.path_to_string(eulerian_path)
```

## Graph Isomorphism and Matching

### Graph Isomorphism

```runa
Note: Test if graphs are isomorphic
Let are_isomorphic be GT.are_isomorphic(graph1, graph2)
Let isomorphism_mapping be GT.find_isomorphism(graph1, graph2)

If are_isomorphic:
    Display "Graphs are isomorphic"
    GT.display_isomorphism_mapping(isomorphism_mapping)
```

### Maximum Matching

```runa
Note: Find maximum matching in bipartite graph
Let max_matching be GT.maximum_bipartite_matching(bipartite_graph)
Let matching_size be GT.matching_size(max_matching)

Display "Maximum matching size: " joined with matching_size
GT.display_matching(max_matching)

Note: General graph matching
Let general_matching be GT.maximum_matching_edmonds(graph)
```

## Advanced Graph Operations

### Graph Decomposition

```runa
Note: Decompose graph into components
Let connected_components be GT.connected_components(graph)
Let strongly_connected_components be GT.strongly_connected_components(directed_graph)

Display "Number of connected components: " joined with GT.component_count(connected_components)
GT.display_component_sizes(connected_components)
```

### Planarity Testing

```runa
Note: Test if graph is planar
Let is_planar be GT.is_planar(graph)
Let planar_embedding be GT.planar_embedding(graph)

If is_planar:
    Display "Graph is planar"
    Let faces be GT.get_faces(planar_embedding)
    Display "Number of faces: " joined with GT.face_count(faces)
```

## Performance Considerations

### Algorithm Complexity

Different algorithms have varying time complexities:
- **DFS/BFS**: O(V + E) - Linear in graph size
- **Dijkstra**: O((V + E) log V) - Efficient for sparse graphs
- **Floyd-Warshall**: O(V³) - Good for dense graphs
- **Maximum Flow**: O(VE²) - Depends on implementation

### Memory Usage

```runa
Note: Monitor graph memory usage
Let memory_usage be GT.get_memory_usage(large_graph)
Let vertex_memory be GT.vertex_memory_usage(large_graph)
Let edge_memory be GT.edge_memory_usage(large_graph)

Display "Total graph memory: " joined with memory_usage joined with " bytes"
```

## Error Handling

The module provides comprehensive error handling:

```runa
Import "core/error_handling" as ErrorHandling

Note: Handle graph operation errors
Let result be GT.add_edge_safe(graph, vertex1, vertex2)
If ErrorHandling.is_error(result):
    Let error be ErrorHandling.get_error(result)
    Display "Error adding edge: " joined with ErrorHandling.error_message(error)
Otherwise:
    Let edge be ErrorHandling.get_value(result)
    Display "Edge added successfully"
```

## Integration with Other Modules

### Mathematical Operations

```runa
Import "math/core/operations" as MathOps
Import "math/precision/rational" as Rational

Note: Use precise arithmetic for graph calculations
Let precise_weight be Rational.create_rational(3, 7)
Let precise_edge be GT.add_edge_with_rational_weight(graph, v1, v2, precise_weight)
```

### Data Visualization

```runa
Import "visualization/graph_plotting" as GraphPlot

Note: Visualize graph structures
Let layout be GraphPlot.spring_layout(graph)
Let plot be GraphPlot.create_graph_plot(graph, layout)
GraphPlot.save_plot(plot, "graph_visualization.png")
```

## Best Practices

### Graph Design
- Choose appropriate representation based on graph density
- Use directed graphs only when edge direction matters
- Consider memory constraints for very large graphs
- Validate graph properties before applying algorithms

### Algorithm Selection
- Use BFS for unweighted shortest paths
- Use Dijkstra for weighted shortest paths with non-negative weights
- Use Bellman-Ford when negative edges are possible
- Consider approximation algorithms for NP-hard problems

### Performance Optimization
- Cache results of expensive computations
- Use appropriate data structures for specific operations
- Consider parallel implementations for large graphs
- Profile algorithms on representative data

This module provides a comprehensive foundation for graph theory applications, from basic graph manipulation to advanced network analysis algorithms.