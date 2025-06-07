# Knowledge Graph Connectors

## Overview

Runa provides a robust system for connecting to various knowledge graph backends, allowing seamless integration between code and knowledge. This document explains the available connectors, how to use them, and how to integrate knowledge graphs with Runa code.

## Available Connectors

Runa currently supports the following knowledge graph backends:

1. **RDF/OWL Connector** - For working with standard RDF triplestores and OWL ontologies
2. **Neo4j Connector** - For working with Neo4j graph databases

Each connector implements a common interface defined by the base `KnowledgeGraphConnector` class, ensuring consistent behavior regardless of the backend technology.

## Using Connectors

### Creating a Connector

You can create connectors directly or using the factory functions:

```python
# Direct instantiation
from runa.ai.knowledge_connectors import RDFConnector, Neo4jConnector

# RDF connector
rdf_connector = RDFConnector(graph_uri="ontology.ttl")

# Neo4j connector
neo4j_connector = Neo4jConnector(uri="bolt://localhost:7687", database="neo4j")

# Using the factory
from runa.ai.knowledge_connectors import create_connector, get_connector_for_uri

# Create based on type
rdf_connector = create_connector("rdf", uri="ontology.ttl")
neo4j_connector = create_connector("neo4j", uri="bolt://localhost:7687", database="neo4j")

# Create based on URI format
connector = get_connector_for_uri("bolt://localhost:7687")  # Neo4j connector
connector = get_connector_for_uri("ontology.ttl")          # RDF connector
```

### Connecting to a Knowledge Graph

After creating a connector, you need to connect to the graph:

```python
# For Neo4j, you typically need credentials
connected = neo4j_connector.connect(username="neo4j", password="password")

# For RDF, you might be loading from a file or connecting to a SPARQL endpoint
connected = rdf_connector.connect()

if connected:
    print("Successfully connected to knowledge graph")
else:
    print("Failed to connect to knowledge graph")
```

### Managing Knowledge Entities and Triples

Knowledge in Runa is represented as entities and triples:

```python
from runa.ai.knowledge import KnowledgeEntity, KnowledgeTriple

# Create an entity
entity = KnowledgeEntity(
    entity_id="algorithm:quicksort",
    entity_type="Algorithm",
    properties={
        "name": "QuickSort",
        "description": "A divide-and-conquer sorting algorithm",
        "complexity": "O(n log n) average case"
    }
)

# Create a triple (relationship)
triple = KnowledgeTriple(
    subject_id="algorithm:quicksort",
    predicate="uses",
    object_id="concept:divide_and_conquer",
    confidence=0.95,
    metadata={"context": "typical implementations"}
)

# Store them in the graph
connector.store_entity(entity)
connector.store_triple(triple)

# You can also import multiple at once
connector.import_knowledge([entity1, entity2], [triple1, triple2])
```

### Querying the Knowledge Graph

Connectors provide various ways to query the graph:

```python
# Using native query language (SPARQL for RDF, Cypher for Neo4j)
results = rdf_connector.query_knowledge_graph("""
    SELECT ?algorithm ?name
    WHERE {
        ?algorithm rdf:type <http://runa-lang.org/ontology#Algorithm> .
        ?algorithm <http://runa-lang.org/ontology#name> ?name .
    }
""", query_type="sparql")

# Using structured queries
entity_results = connector.query_knowledge_graph({
    "entity_id": "algorithm:quicksort"
})

relation_results = connector.query_knowledge_graph({
    "subject": "algorithm:quicksort"
})

search_results = connector.query_knowledge_graph({
    "name_similar_to": "sort",
    "type": "Algorithm"
})
```

### Exporting Knowledge

You can export all knowledge from a graph:

```python
entities, triples = connector.export_knowledge()
print(f"Exported {len(entities)} entities and {len(triples)} triples")

# For RDF connectors, you can also save to a file
rdf_connector.save_to_file("exported_knowledge.ttl", format="turtle")
```

## RDF/OWL Connector

The RDF connector is specifically designed for working with semantic web technologies:

### Supported Formats

- Turtle (.ttl)
- RDF/XML (.rdf, .xml)
- N3 (.n3)
- N-Triples (.nt)
- JSON-LD (.jsonld)

### Namespace Management

```python
# Add custom namespaces
rdf_connector.add_namespace("ex", "http://example.org/")
rdf_connector.add_namespace("alg", "http://example.org/algorithms#")
```

## Neo4j Connector

The Neo4j connector provides integration with Neo4j graph databases:

### Connection Parameters

- `uri`: Neo4j connection URI (e.g., "bolt://localhost:7687")
- `database`: Neo4j database name (default: "neo4j")
- `username`: Username for authentication
- `password`: Password for authentication

### Cypher Queries

```python
results = neo4j_connector.query_knowledge_graph("""
    MATCH (a:Algorithm)-[:USES]->(c:Concept)
    RETURN a.name as algorithm, c.name as concept
""", query_type="cypher")
```

## Integrating with Runa Code

Knowledge graphs can be integrated with Runa code through annotations:

### 1. Creating Knowledge Annotations

```python
from runa.annotation_system import KnowledgeAnnotation, AnnotationType

# Create a knowledge annotation
annotation = KnowledgeAnnotation(
    annotation_type=AnnotationType.KNOWLEDGE,
    content="A divide-and-conquer sorting algorithm",
    entity_id="algorithm:quicksort",
    relation_type="implements",
    metadata={"function": "quick_sort"}
)
```

### 2. Adding Annotations to Code

```python
from runa.annotation_system import AnnotationGenerator

# Original Runa code
runa_code = """
Process called "quick_sort" that takes arr:
    # Implementation...
"""

# Create an annotation generator
generator = AnnotationGenerator()

# Generate annotated code
enhanced_code = generator.generate_annotations_for_code(runa_code, [annotation])

# The result will include knowledge annotations as comments
```

### 3. Automatic Code Enhancement

You can automatically enhance Runa code with knowledge from a graph:

```python
# Load knowledge from graph
entities, triples = connector.export_knowledge()

# Create annotations based on knowledge
annotations = []
for entity in entities:
    if entity.entity_type == "Algorithm":
        annotations.append(
            KnowledgeAnnotation(
                annotation_type=AnnotationType.KNOWLEDGE,
                content=entity.properties.get("description", ""),
                entity_id=entity.entity_id,
                relation_type="implements",
                metadata={"function": entity.properties.get("name", "")}
            )
        )

# Enhance code with annotations
enhanced_code = generator.generate_annotations_for_code(runa_code, annotations)
```

## Complete Example

```python
from runa.ai.knowledge import KnowledgeEntity, KnowledgeTriple
from runa.ai.knowledge_connectors import RDFConnector
from runa.annotation_system import KnowledgeAnnotation, AnnotationType, AnnotationGenerator

# Create a connector
connector = RDFConnector()
connector.connect()

# Create entities and triples
entities = [
    KnowledgeEntity(
        entity_id="algorithm:quicksort",
        entity_type="Algorithm",
        properties={
            "name": "QuickSort",
            "description": "A divide-and-conquer sorting algorithm"
        }
    )
]

triples = [
    KnowledgeTriple(
        subject_id="algorithm:quicksort",
        predicate="uses",
        object_id="concept:divide_and_conquer"
    )
]

# Import knowledge
connector.import_knowledge(entities, triples)

# Query the graph
results = connector.query_knowledge_graph({
    "entity_id": "algorithm:quicksort"
})

# Create annotations
annotations = [
    KnowledgeAnnotation(
        annotation_type=AnnotationType.KNOWLEDGE,
        content="A divide-and-conquer sorting algorithm",
        entity_id="algorithm:quicksort",
        relation_type="implements",
        metadata={"function": "quick_sort"}
    )
]

# Generate annotated code
runa_code = """
Process called "quick_sort" that takes arr:
    # Implementation...
"""

generator = AnnotationGenerator()
enhanced_code = generator.generate_annotations_for_code(runa_code, annotations)
```

## Best Practices

1. **Use Consistent Entity IDs**: Adopt a consistent scheme for entity IDs (e.g., "domain:entity_name")
2. **Add Metadata**: Include relevant metadata in both entities and triples
3. **Set Confidence Levels**: Use confidence levels to indicate the certainty of triples
4. **Close Connections**: Always close connections when you're done with them
5. **Handle Errors**: Wrap connector operations in try-except blocks to handle errors gracefully
6. **Use the Factory**: When possible, use the connector factory to create appropriate connectors

## Next Steps

The knowledge graph connectivity system will continue to evolve with:

1. **Additional Connectors**: Support for more backends like GraphDB, Stardog, etc.
2. **Reasoning Integration**: Built-in reasoning capabilities with rule engines
3. **Visualization Tools**: Graphical visualization of knowledge graphs
4. **Automatic Annotation**: More sophisticated automatic annotation generation 