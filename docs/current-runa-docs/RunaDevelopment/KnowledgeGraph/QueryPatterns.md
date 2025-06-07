# Query Patterns for Knowledge Graph Interaction

This guide explains how to effectively query and interact with the Runa knowledge graph to extract valuable insights from your codebase.

## Overview

A knowledge graph is only as useful as your ability to query it. Runa provides a powerful query system that allows you to extract meaningful information, discover patterns, and gain insights from the code knowledge graph. This guide covers the query patterns and techniques available for knowledge graph interaction.

## Basic Query Patterns

### Entity Queries

Retrieve entities based on various criteria:

```python
from runa.ai.knowledge_graph import knowledge_manager

# Get entity by ID
entity = knowledge_manager.get_entity_by_id("entity_123")

# Get entities by type
functions = knowledge_manager.get_entities_by_type("FUNCTION")

# Get entities by name pattern
validation_entities = knowledge_manager.get_entities_by_name_pattern("validate_*")

# Get entities by namespace
auth_entities = knowledge_manager.get_entities_by_namespace("auth")

# Get entities by tag
security_entities = knowledge_manager.get_entities_by_tag("security")

# Get entities with specific property value
entities = knowledge_manager.get_entities_by_property("complexity", "high")
```

### Relationship Queries

Retrieve relationships based on various criteria:

```python
# Get relationships by type
call_relationships = knowledge_manager.get_relationships_by_type("CALLS")

# Get relationships by source entity
outgoing = knowledge_manager.get_relationships_by_source("entity_123")

# Get relationships by target entity
incoming = knowledge_manager.get_relationships_by_target("entity_456")

# Get relationships between specific entities
direct_rels = knowledge_manager.get_relationships_between(
    source_id="entity_123", 
    target_id="entity_456"
)

# Get all relationships for an entity
all_rels = knowledge_manager.get_relationships_for_entity(
    entity_id="entity_123",
    direction="both"  # "incoming", "outgoing", or "both"
)
```

### Combined Queries

Combine entity and relationship queries for more powerful filters:

```python
# Get all functions that call a specific function
callers = knowledge_manager.get_entities_with_relationship_to(
    target_id="func_validate",
    relationship_type="CALLS",
    source_type="FUNCTION"
)

# Get all classes that implement a specific interface
implementers = knowledge_manager.get_entities_with_relationship_to(
    target_id="interface_storage",
    relationship_type="IMPLEMENTS",
    source_type="CLASS"
)

# Get all entities that a specific entity depends on
dependencies = knowledge_manager.get_entities_with_relationship_from(
    source_id="payment_processor",
    relationship_type="DEPENDS_ON"
)
```

## Advanced Query Patterns

### Path Queries

Find paths between entities in the knowledge graph:

```python
# Find all paths between two entities
paths = knowledge_manager.find_paths(
    source_id="entity_123",
    target_id="entity_456",
    max_depth=3,
    relationship_types=["CALLS", "DEPENDS_ON"]
)

# Find shortest path
shortest_path = knowledge_manager.find_shortest_path(
    source_id="entity_123",
    target_id="entity_456"
)

# Check if there's a path between entities
has_path = knowledge_manager.has_path(
    source_id="entity_123",
    target_id="entity_456",
    max_depth=5
)
```

### Structural Queries

Analyze the structure of the knowledge graph:

```python
# Find all leaf entities (no outgoing relationships)
leaves = knowledge_manager.find_leaf_entities(
    relationship_types=["CALLS", "DEPENDS_ON"]
)

# Find root entities (no incoming relationships)
roots = knowledge_manager.find_root_entities(
    relationship_types=["CALLS", "DEPENDS_ON"]
)

# Find entities with high fan-out (many outgoing relationships)
high_fanout = knowledge_manager.find_entities_by_relationship_count(
    direction="outgoing",
    relationship_type="CALLS",
    min_count=10
)

# Find entities with high fan-in (many incoming relationships)
high_fanin = knowledge_manager.find_entities_by_relationship_count(
    direction="incoming",
    relationship_type="CALLS",
    min_count=10
)
```

### Pattern Matching Queries

Find entity patterns that match specific structures:

```python
# Find all mediator patterns
mediators = knowledge_manager.find_pattern(
    pattern_type="MEDIATOR",
    min_confidence=0.8
)

# Find all adapter patterns
adapters = knowledge_manager.find_pattern(
    pattern_type="ADAPTER",
    min_confidence=0.8
)

# Find all observer patterns
observers = knowledge_manager.find_pattern(
    pattern_type="OBSERVER",
    min_confidence=0.8
)

# Define and find a custom pattern
custom_pattern = {
    "nodes": [
        {"id": "n1", "type": "CLASS"},
        {"id": "n2", "type": "CLASS"},
        {"id": "n3", "type": "INTERFACE"}
    ],
    "relationships": [
        {"source": "n1", "target": "n2", "type": "CALLS"},
        {"source": "n2", "target": "n3", "type": "IMPLEMENTS"}
    ]
}

matches = knowledge_manager.find_custom_pattern(
    pattern=custom_pattern,
    min_confidence=0.7
)
```

### Graph Algorithm Queries

Apply graph algorithms to analyze the knowledge graph:

```python
# Find central entities using PageRank
central_entities = knowledge_manager.find_central_entities(
    algorithm="pagerank",
    entity_type="FUNCTION",
    limit=10
)

# Find communities using community detection
communities = knowledge_manager.find_communities(
    algorithm="louvain",
    min_community_size=3
)

# Find similar entities based on graph structure
similar_entities = knowledge_manager.find_similar_entities(
    entity_id="entity_123",
    similarity_metric="structural",
    min_similarity=0.7,
    limit=5
)

# Analyze dependency cycles
cycles = knowledge_manager.find_cycles(
    relationship_type="DEPENDS_ON",
    max_cycle_length=5
)
```

## Semantic Query Patterns

### Semantic Search

Search for entities based on natural language or semantic similarity:

```python
# Find entities by semantic description
validation_funcs = knowledge_manager.find_entities_by_description(
    description="functions that validate user input",
    entity_type="FUNCTION",
    min_similarity=0.7,
    limit=10
)

# Find entities similar to another entity
similar_entities = knowledge_manager.find_similar_entities_semantic(
    entity_id="entity_123",
    min_similarity=0.8,
    limit=5
)

# Find entities by code similarity
similar_code = knowledge_manager.find_entities_by_code_similarity(
    code_snippet="if user.is_authenticated() and user.has_permission('admin'):",
    entity_type="FUNCTION",
    min_similarity=0.7,
    limit=5
)
```

### Knowledge-Based Queries

Leverage the knowledge graph for more complex reasoning:

```python
# Find entities based on a natural language query
results = knowledge_manager.query_knowledge_graph(
    query="Find all functions that handle user authentication and call database operations",
    result_type="entities",
    limit=10
)

# Find relationships based on a natural language query
results = knowledge_manager.query_knowledge_graph(
    query="What depends on the user authentication module?",
    result_type="relationships",
    limit=10
)

# Ask a question about the codebase
answer = knowledge_manager.ask_knowledge_graph(
    question="What is the most critical component in the payment processing system?",
    context_entity_ids=["payment_processor", "transaction_handler"]
)
```

## Query Language Support

Runa supports several specialized query languages for knowledge graph interaction.

### Runa Knowledge Query Language (RKQL)

RKQL is a custom query language specifically designed for Runa's knowledge graph:

```python
# Execute an RKQL query
results = knowledge_manager.execute_rkql("""
    MATCH (f:FUNCTION) WHERE f.name =~ "validate_*"
    AND EXISTS (f)-[:CALLS]->(:FUNCTION {name: "log_error"})
    RETURN f
""")

# Define and save a named query
knowledge_manager.save_rkql_query(
    name="validation_functions_with_error_logging",
    query="""
        MATCH (f:FUNCTION) WHERE f.name =~ "validate_*"
        AND EXISTS (f)-[:CALLS]->(:FUNCTION {name: "log_error"})
        RETURN f
    """
)

# Execute a saved query
results = knowledge_manager.execute_saved_query(
    "validation_functions_with_error_logging"
)
```

### Cypher Support

For integration with Neo4j and other graph databases, Runa supports Cypher queries:

```python
# Execute a Cypher query
results = knowledge_manager.execute_cypher("""
    MATCH (f:Function)-[:CALLS]->(t:Function)
    WHERE f.name CONTAINS 'validate'
    RETURN f, t
""")

# Export the knowledge graph to Neo4j
knowledge_manager.export_to_neo4j(
    neo4j_uri="bolt://localhost:7687",
    username="neo4j",
    password="password"
)
```

### SPARQL Support

For semantic web integration, Runa supports SPARQL queries:

```python
# Execute a SPARQL query
results = knowledge_manager.execute_sparql("""
    PREFIX kg: <http://runa.ai/knowledge-graph/>
    SELECT ?function
    WHERE {
        ?function a kg:Function ;
                  kg:name ?name .
        FILTER(REGEX(?name, "validate_.*"))
    }
""")

# Export the knowledge graph to RDF
knowledge_manager.export_to_rdf(
    output_path="knowledge_graph.ttl",
    format="turtle"  # "turtle", "xml", "n3", etc.
)
```

## Parametrized Queries

Create and execute parametrized queries for reusability:

```python
# Define a parametrized query
knowledge_manager.define_parametrized_query(
    name="functions_by_pattern_calling_specific_function",
    query="""
        MATCH (f:FUNCTION) WHERE f.name =~ $name_pattern
        AND EXISTS (f)-[:CALLS]->(:FUNCTION {name: $called_function})
        RETURN f
    """
)

# Execute the parametrized query
results = knowledge_manager.execute_parametrized_query(
    "functions_by_pattern_calling_specific_function",
    parameters={
        "name_pattern": "validate_.*",
        "called_function": "log_error"
    }
)
```

## Combining Query Results

Combine and manipulate query results for more complex analysis:

```python
# Union of two query results
result_a = knowledge_manager.get_entities_by_type("FUNCTION")
result_b = knowledge_manager.get_entities_by_tag("critical")
combined = knowledge_manager.union_results(result_a, result_b)

# Intersection of two query results
result_a = knowledge_manager.get_entities_by_type("FUNCTION")
result_b = knowledge_manager.get_entities_by_tag("security")
security_functions = knowledge_manager.intersect_results(result_a, result_b)

# Difference of two query results
result_a = knowledge_manager.get_entities_by_type("FUNCTION")
result_b = knowledge_manager.get_entities_by_tag("deprecated")
active_functions = knowledge_manager.difference_results(result_a, result_b)
```

## Query Optimization

Improve query performance for large knowledge graphs:

```python
# Enable query caching
knowledge_manager.configure_query_caching(
    enabled=True,
    max_cache_size=100,  # Maximum number of cached query results
    ttl=3600  # Cache time-to-live in seconds
)

# Create an index for faster queries
knowledge_manager.create_index(
    entity_type="FUNCTION",
    property_name="name"
)

# Explain query execution plan
plan = knowledge_manager.explain_query("""
    MATCH (f:FUNCTION)-[:CALLS]->(t:FUNCTION)
    WHERE f.name CONTAINS 'validate'
    RETURN f, t
""")
print(plan)

# Profile query execution
profile = knowledge_manager.profile_query("""
    MATCH (f:FUNCTION)-[:CALLS]->(t:FUNCTION)
    WHERE f.name CONTAINS 'validate'
    RETURN f, t
""")
print(f"Execution time: {profile['execution_time']} ms")
print(f"Entities processed: {profile['entities_processed']}")
```

## Query Result Processing

Process query results for further analysis or visualization:

```python
# Transform query results
functions = knowledge_manager.get_entities_by_type("FUNCTION")
function_names = knowledge_manager.transform_results(
    functions,
    lambda entity: entity["name"]
)

# Filter query results
all_functions = knowledge_manager.get_entities_by_type("FUNCTION")
complex_functions = knowledge_manager.filter_results(
    all_functions,
    lambda entity: entity.get("complexity", 0) > 7
)

# Sort query results
functions = knowledge_manager.get_entities_by_type("FUNCTION")
sorted_functions = knowledge_manager.sort_results(
    functions,
    key=lambda entity: entity.get("complexity", 0),
    reverse=True
)

# Group query results
all_functions = knowledge_manager.get_entities_by_type("FUNCTION")
functions_by_module = knowledge_manager.group_results(
    all_functions,
    key=lambda entity: entity.get("module", "unknown")
)
```

## Temporal Queries

Query the knowledge graph across different versions or time periods:

```python
# Get entity at a specific point in time
entity_history = knowledge_manager.get_entity_at_time(
    entity_id="entity_123",
    timestamp="2023-08-15T10:30:00Z"
)

# Get relationships at a specific point in time
relationship_history = knowledge_manager.get_relationships_at_time(
    entity_id="entity_123",
    relationship_type="CALLS",
    timestamp="2023-08-15T10:30:00Z"
)

# Track entity changes over time
entity_evolution = knowledge_manager.track_entity_evolution(
    entity_id="entity_123",
    start_time="2023-01-01T00:00:00Z",
    end_time="2023-12-31T23:59:59Z"
)

# Compare knowledge graph at different points in time
diff = knowledge_manager.compare_knowledge_graph(
    time_a="2023-01-01T00:00:00Z",
    time_b="2023-06-01T00:00:00Z"
)
```

## Query Result Export and Visualization

Export and visualize query results:

```python
# Export query results to JSON
results = knowledge_manager.get_entities_by_type("FUNCTION")
knowledge_manager.export_results(
    results,
    output_path="functions.json",
    format="json"
)

# Export query results to CSV
results = knowledge_manager.get_entities_by_property("complexity", "high")
knowledge_manager.export_results(
    results,
    output_path="complex_functions.csv",
    format="csv"
)

# Generate visualization from query results
results = knowledge_manager.find_paths(
    source_id="entity_123",
    target_id="entity_456",
    max_depth=3
)
knowledge_manager.visualize_results(
    results,
    output_path="path_visualization.html",
    visualization_type="path",
    title="Paths Between Entities"
)
```

## Integrating Queries With Code Analysis

Combine knowledge graph queries with code analysis for deeper insights:

```python
from runa.analysis import code_analyzer

# Analyze code quality using the knowledge graph
quality_issues = knowledge_manager.analyze_code_quality(
    entity_ids=["entity_123", "entity_456"],
    quality_metrics=["complexity", "maintainability"]
)

# Find potential bugs using graph patterns
potential_bugs = knowledge_manager.find_bug_patterns(
    pattern_library="standard",  # "standard", "security", "performance"
    min_confidence=0.7
)

# Analyze impact of code changes
impact_analysis = knowledge_manager.analyze_change_impact(
    changed_entities=["entity_123"],
    impact_depth=3
)

# Analyze architectural conformance
conformance_issues = knowledge_manager.analyze_architectural_conformance(
    architecture_rules=[
        "UI_LAYER should not CALL DATABASE_LAYER directly",
        "SECURITY_MODULE must be CALLED_BY all EXTERNAL_API functions"
    ]
)
```

## Query Scheduling and Automation

Schedule recurring queries for monitoring and reporting:

```python
# Schedule a recurring query
knowledge_manager.schedule_query(
    name="daily_complexity_report",
    query="""
        MATCH (f:FUNCTION) 
        WHERE f.complexity > 10
        RETURN f.name, f.complexity
    """,
    schedule="daily",  # "hourly", "daily", "weekly", "monthly"
    time="08:00",
    output_format="csv",
    output_path="reports/complexity_report_{date}.csv",
    notify_email="developer@example.com"
)

# List scheduled queries
scheduled_queries = knowledge_manager.list_scheduled_queries()

# Remove a scheduled query
knowledge_manager.remove_scheduled_query("daily_complexity_report")
```

## Query-Driven Insights

Generate insights from knowledge graph queries:

```python
# Generate code insights report
insights = knowledge_manager.generate_code_insights(
    entity_types=["FUNCTION", "CLASS"],
    metrics=["complexity", "coupling", "centrality"],
    output_format="html",
    output_path="reports/code_insights.html"
)

# Find potential refactoring opportunities
refactoring_opps = knowledge_manager.find_refactoring_opportunities(
    opportunity_types=["extract_method", "move_method", "replace_conditional"],
    min_confidence=0.7
)

# Find knowledge gaps
knowledge_gaps = knowledge_manager.find_knowledge_gaps(
    gap_types=["missing_documentation", "complex_undocumented_code"],
    min_confidence=0.7
)

# Generate architectural overview
architecture = knowledge_manager.generate_architectural_overview(
    level="module",  # "module", "component", "layer"
    output_format="svg",
    output_path="reports/architecture.svg"
)
```

## Best Practices for Knowledge Graph Queries

1. **Start with Specific Queries**: Begin with specific, targeted queries rather than broad ones
2. **Limit Result Sets**: Use limits or filters to avoid retrieving too many results at once
3. **Leverage Indexes**: Create indexes for frequently queried properties
4. **Use Parametrized Queries**: Create reusable parametrized queries for common query patterns
5. **Combine Different Query Types**: Mix and match different query types for more powerful insights
6. **Cache Common Queries**: Enable caching for frequently executed queries
7. **Optimize Complex Queries**: Review and optimize the performance of complex queries
8. **Use the Right Query Language**: Choose the query language that best fits your needs
9. **Process Results in Batches**: For large result sets, process results in batches
10. **Version Your Queries**: Maintain versions of important queries as your knowledge graph evolves

## Troubleshooting Queries

Common issues and solutions:

1. **Slow query performance**
   - Create indexes for frequently queried properties
   - Limit the query scope
   - Optimize the query structure
   - Use batch processing for large result sets

2. **No results when expected**
   - Check entity and relationship types for typos
   - Verify property names and values
   - Ensure the knowledge graph contains the expected data
   - Use less restrictive filters

3. **Too many results**
   - Add more specific filters
   - Limit the result set size
   - Use more specific entity or relationship types

4. **Memory issues with large result sets**
   - Use pagination or batch processing
   - Limit the properties returned for each entity
   - Filter results before retrieving full entity details

5. **Inconsistent query results**
   - Check if the knowledge graph is being updated concurrently
   - Verify the query is deterministic
   - Use explicit ordering when needed

## Conclusion

Effective querying is key to unlocking the value of the knowledge graph. By mastering these query patterns, you can extract meaningful insights, discover patterns, and gain a deeper understanding of your codebase.

For more information on related topics, see these guides:
- [Relationship Identification](./RelationshipIdentification.md)
- [Knowledge Graph Visualization](./Visualization.md)
- [Knowledge-Enhanced Code Generation](./CodeGeneration.md) 