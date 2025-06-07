# Knowledge Graph Integration in Runa

## Overview

Runa's knowledge graph integration capabilities allow developers to connect their applications with graph-based knowledge representations. This enables semantic reasoning, complex relationship modeling, and intelligent data exploration within Runa applications.

## Core Features

### 1. Knowledge Graph Connection

Runa provides a simple API to connect to various knowledge graph systems:

```runa
# Connect to a knowledge graph store
Let kg = KnowledgeGraph.connect("graph_name", {
    "endpoint": "https://kg.example.com/sparql",
    "credentials": credentials,
    "format": "RDF"
})
```

Supported knowledge graph formats include RDF, Property Graphs, and Runa's native Knowledge Format (RKF).

### 2. Graph Querying

#### Basic Queries

Execute SPARQL or Cypher queries depending on your graph type:

```runa
# SPARQL query for RDF graphs
Let results = kg.query("""
    SELECT ?entity ?name
    WHERE {
        ?entity rdf:type ex:Person .
        ?entity ex:name ?name .
    }
""")

# Cypher query for property graphs
Let results = kg.query("""
    MATCH (p:Person)-[:KNOWS]->(friend)
    RETURN p.name, friend.name
""")
```

#### Query Builder

Construct queries programmatically:

```runa
Let query = kg.query_builder()
    .match("Person", "p")
    .with_property("name")
    .connected_to("KNOWS", "friend")
    .return("p.name", "friend.name")
    .build()

Let results = kg.execute(query)
```

### 3. Graph Data Management

#### Adding Entities and Relationships

```runa
# Add a new entity
Let person = kg.create_entity("Person", {
    "name": "Jane Smith",
    "age": 28,
    "occupation": "Data Scientist"
})

# Create relationships
Let relation = kg.create_relationship(
    person,
    "WORKS_FOR", 
    company,
    {
        "since": Date.create(2022, 1, 15),
        "role": "Senior Data Scientist"
    }
)
```

#### Batch Operations

```runa
# Batch import from data structures
Let entities = [/* list of entity objects */]
Let relationships = [/* list of relationship objects */]

kg.batch_import({
    "entities": entities,
    "relationships": relationships,
    "on_conflict": "merge"
})
```

### 4. Semantic Reasoning

Perform inference and reasoning over your knowledge graph:

```runa
# Define inference rules
Let rules = [
    "IF (Person A)-[:PARENT_OF]->(Person B) AND (Person B)-[:PARENT_OF]->(Person C) THEN (Person A)-[:GRANDPARENT_OF]->(Person C)"
]

# Apply reasoning
Let reasoner = kg.create_reasoner(rules)
Let inferred_graph = reasoner.apply()

# Query inferred relationships
Let grandparents = kg.query("MATCH (g)-[:GRANDPARENT_OF]->(c) RETURN g.name, c.name")
```

### 5. Graph Integration with LLMs

Combine knowledge graphs with LLMs for enhanced capabilities:

```runa
# Load relevant subgraph based on query
Let context = kg.extract_context("What do we know about quantum computing?")

# Enhance LLM prompt with knowledge graph data
Let model = LLM.connect("model_name")
Let response = model.complete_with_context("Explain quantum computing applications", context)
```

## Knowledge Graph Visualization

Runa provides tools to visualize and explore knowledge graphs:

```runa
# Create a visualization of a subgraph
Let viz = GraphVisualizer.create({
    "layout": "force_directed",
    "theme": "light",
    "node_size_property": "importance",
    "edge_color_property": "relationship_type"
})

# Render a specific query result
Let visual = viz.render(query_results)

# Export or display
visual.save("knowledge_graph.svg")
# or
visual.display()  # Opens interactive visualization
```

## Data Integration

### Importing External Data

```runa
# Import from various sources
Let importer = KGImporter.create()

# From structured data
Let graph_data = importer.from_csv("data.csv", {
    "entity_columns": ["name", "type"],
    "relationship_mapping": {"from": "col1", "type": "col2", "to": "col3"}
})

# From unstructured text
Let extracted_graph = importer.from_text("document.txt", {
    "extract_entities": true,
    "extract_relationships": true,
    "confidence_threshold": 0.7
})

kg.merge(graph_data)
```

### Exporting Graph Data

```runa
# Export to various formats
Let exporter = kg.create_exporter()
exporter.to_rdf("output.ttl", "turtle")
exporter.to_json("output.json")
exporter.to_csv("nodes.csv", "edges.csv")
```

## Advanced Features

### Graph Embeddings

Generate vector representations of entities and relationships:

```runa
# Create embeddings from knowledge graph
Let embedder = GraphEmbedder.create("transE")
Let embeddings = embedder.generate(kg)

# Use for similarity search
Let similar_entities = embeddings.find_similar(entity_id, top_k=5)
```

### Graph Algorithms

Apply various graph algorithms:

```runa
Let algorithms = GraphAlgorithms.create(kg)

# Centrality measures
Let centrality = algorithms.page_rank()
Let communities = algorithms.community_detection("louvain")
Let path = algorithms.shortest_path(entity1, entity2)
```

## Example: Building a Knowledge-Enabled Application

```runa
Process called "create_knowledge_system":
    # Connect to knowledge sources
    Let kg = KnowledgeGraph.connect("domain_knowledge")
    Let model = LLM.connect("runa_knowledge_model")
    
    # Create knowledge processor
    Let processor = KnowledgeProcessor.create({
        "knowledge_graph": kg,
        "language_model": model,
        "reasoning_enabled": true
    })
    
    # Set up extraction pipeline
    Let pipeline = processor.create_pipeline([
        "entity_extraction",
        "relationship_identification",
        "fact_verification",
        "knowledge_integration"
    ])
    
    # Process new information
    Process called "process_document"(text):
        Let extracted_knowledge = pipeline.process(text)
        Let verification_results = processor.verify_facts(extracted_knowledge)
        
        # Only add verified knowledge
        Let verified_items = verification_results.filter(item => item.confidence > 0.85)
        kg.add_knowledge(verified_items)
        
        Return verified_items
    
    Return {
        "processor": processor,
        "process_document": process_document
    }
```

## References

- [Runa Knowledge Graph API Reference](https://runa-lang.org/docs/api/knowledge-graph)
- [Graph Query Language Guide](https://runa-lang.org/docs/guides/graph-queries)
- [Knowledge Modeling Best Practices](https://runa-lang.org/docs/guides/knowledge-modeling)

For complete examples of knowledge graph integration, see the [Knowledge Graph Examples](../../src/tests/examples/knowledge_graph_examples.runa) in the Runa codebase. 