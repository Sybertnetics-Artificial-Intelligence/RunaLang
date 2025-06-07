# Knowledge Graph Integration in Runa

This guide provides an overview of Runa's knowledge graph integration capabilities, allowing developers to connect their code to structured knowledge representations.

## What is the Knowledge Graph Integration?

The Knowledge Graph Integration in Runa enables:
- Automatic extraction of knowledge entities and relationships from code
- Connecting code components to external knowledge sources
- Semantic querying of codebase and documentation
- Reasoning about code at a higher level of abstraction

With these capabilities, Runa can understand not just the syntax of your code, but also its meaning and relationship to broader concepts and domains.

## Architecture Overview

The Knowledge Graph integration consists of several key components:

```
┌──────────────────┐     ┌───────────────────┐     ┌───────────────────┐
│                  │     │                   │     │                   │
│  Code Analysis   │────▶│  Entity Extraction │────▶│  Relationship     │
│  Components      │     │  Pipeline         │     │  Identification   │
│                  │     │                   │     │                   │
└──────────────────┘     └───────────────────┘     └───────────────────┘
          │                                                   │
          │                                                   ▼
          │                  ┌───────────────────┐     ┌───────────────────┐
          │                  │                   │     │                   │
          └─────────────────▶│  Knowledge Graph  │◀────│  External         │
                             │  Storage          │     │  Knowledge        │
                             │                   │     │  Sources          │
                             └───────────────────┘     │                   │
                                      │                └───────────────────┘
                                      ▼
                             ┌───────────────────┐
                             │                   │
                             │  Query Engine &   │
                             │  APIs             │
                             │                   │
                             └───────────────────┘
```

## Key Components

### 1. Entity Extraction

The entity extraction system identifies key concepts in your code:

```python
from runa.ai.knowledge_graph import knowledge_manager

# Extract entities from a code file
entities = knowledge_manager.extract_entities("src/my_module.runa")

# Extract entities from a code string
code_string = """
process calculate_area(radius: Number) returns: Number
    return 3.14159 * radius * radius
end
"""
entities = knowledge_manager.extract_entities_from_string(code_string)

# Print extracted entities
for entity in entities:
    print(f"Entity: {entity.name}, Type: {entity.type}, Confidence: {entity.confidence}")
```

Entity types include:
- Functions and methods
- Classes and types
- Variables and parameters
- Algorithms and patterns
- Domain concepts

### 2. Relationship Identification

The system identifies how entities relate to each other:

```python
# Get relationships between entities
relationships = knowledge_manager.get_relationships(entity1, entity2)

# Get all relationships for an entity
all_relationships = knowledge_manager.get_all_relationships(entity)

# Define a custom relationship
knowledge_manager.define_relationship(
    source_entity="calculate_area",
    relationship_type="implements",
    target_entity="circle_area_formula",
    metadata={"confidence": 0.95}
)
```

Common relationship types:
- `calls`: Function A calls Function B
- `imports`: Module A imports Module B
- `implements`: Class A implements Interface B
- `inherits_from`: Class A inherits from Class B
- `depends_on`: Component A depends on Component B
- `part_of`: Entity A is part of Domain B

### 3. Knowledge Graph Storage

The knowledge is stored in a flexible graph database:

```python
# Access the underlying graph database
graph_db = knowledge_manager.get_graph_db()

# Get statistics about the knowledge graph
stats = knowledge_manager.get_graph_stats()
print(f"Total entities: {stats['entity_count']}")
print(f"Total relationships: {stats['relationship_count']}")
print(f"Entity types: {stats['entity_types']}")
```

### 4. External Knowledge Sources

Connect to external knowledge sources:

```python
# Connect to an external knowledge graph
knowledge_manager.connect_external_source(
    name="domain_ontology",
    source_type="ontology",
    connection_string="https://example.com/ontology"
)

# Import knowledge from connected source
knowledge_manager.import_from_external(
    source_name="domain_ontology",
    filter_criteria={"domain": "finance"}
)

# List connected knowledge sources
sources = knowledge_manager.list_external_sources()
```

Supported external sources include:
- Domain-specific ontologies
- Public knowledge graphs
- Industry-standard terminologies
- Project-specific knowledge bases

### 5. Query Engine and APIs

Query the knowledge graph for insights:

```python
# Simple entity query
results = knowledge_manager.query("MATCH (e:Entity) WHERE e.name CONTAINS 'calculate' RETURN e")

# Find paths between entities
paths = knowledge_manager.find_paths(
    start_entity="UserAuthentication",
    end_entity="DatabaseConnection",
    max_depth=3
)

# Semantic query (natural language)
semantic_results = knowledge_manager.semantic_query(
    "Find all functions that implement sorting algorithms"
)

# Get recommendations based on an entity
recommendations = knowledge_manager.get_recommendations(
    entity="DataProcessor",
    recommendation_type="related_components",
    limit=5
)
```

## Integration with LLM Features

The Knowledge Graph integration works seamlessly with Runa's LLM capabilities:

```python
from runa.ai.llm_integration import llm_manager

# Generate code with knowledge graph context
code_response = llm_manager.generate(
    template_name="code_generation",
    requirements="Create a function to process financial transactions",
    knowledge_context=knowledge_manager.get_context_for_domain("finance")
)

# Explain code with knowledge graph enrichment
explanation = llm_manager.generate(
    template_name="code_explanation",
    code=my_code,
    enrich_with_knowledge=True
)

# Ask questions about the codebase with knowledge graph backing
answer = llm_manager.generate(
    template_name="code_query",
    question="How does the authentication system connect to the user database?",
    use_knowledge_graph=True
)
```

## Setting Up Knowledge Graph Integration

To set up and configure the knowledge graph:

```python
from runa.ai.knowledge_graph import knowledge_manager, EntityType

# Initialize and configure the knowledge graph
knowledge_manager.initialize(
    storage_path="./knowledge_store",
    extraction_level="detailed",  # Options: basic, standard, detailed
    auto_extract=True  # Automatically extract from new code
)

# Configure entity extraction settings
knowledge_manager.configure_extraction(
    min_confidence=0.7,
    extract_types=[
        EntityType.FUNCTION,
        EntityType.CLASS,
        EntityType.DOMAIN_CONCEPT
    ],
    max_entities_per_file=100
)

# Configure relationship identification
knowledge_manager.configure_relationships(
    min_confidence=0.6,
    max_distance=3,
    identify_indirect=True
)
```

## Custom Entity Types and Relationships

Define custom entities and relationships for your domain:

```python
from runa.ai.knowledge_graph import knowledge_manager, EntityType, RelationshipType

# Define a custom entity type
knowledge_manager.define_entity_type(
    name="FINANCIAL_INSTRUMENT",
    properties=["name", "risk_level", "market_type"],
    parent_type=EntityType.DOMAIN_CONCEPT
)

# Define a custom relationship type
knowledge_manager.define_relationship_type(
    name="CALCULATES_RISK_FOR",
    properties=["confidence", "risk_model"],
    source_types=["FUNCTION"],
    target_types=["FINANCIAL_INSTRUMENT"]
)

# Create an entity of the custom type
knowledge_manager.create_entity(
    name="StockOption",
    entity_type="FINANCIAL_INSTRUMENT",
    properties={
        "risk_level": "high",
        "market_type": "derivatives"
    }
)
```

## Visualization

Visualize the knowledge graph:

```python
# Generate visualization for a subset of the graph
knowledge_manager.visualize(
    entities=["AuthenticationService", "UserDatabase"],
    include_relationships=True,
    max_distance=2,
    output_file="auth_system.html"
)

# Generate a full graph visualization
knowledge_manager.visualize_full_graph(
    filter_criteria={"domain": "security"},
    output_file="security_components.html"
)
```

## Code Annotations for Knowledge Graph

You can use annotations to explicitly link code to knowledge graph entities:

```
@KnowledgeDomain("finance")
@Implements("black_scholes_model")
process calculate_option_price(strike: Number, spot: Number, 
                             volatility: Number, interest_rate: Number, 
                             time_to_expiry: Number) returns: Number
    # Implementation of Black-Scholes option pricing model
    # ...
end
```

The supported annotations include:
- `@KnowledgeDomain(domain_name)`: Associates code with a knowledge domain
- `@Implements(concept_name)`: Indicates that code implements a specific concept
- `@RelatesTo(entity_name, relationship_type)`: Establishes a custom relationship
- `@KnowledgeTag(tag_name)`: Tags code with a specific knowledge tag

## Exporting and Importing Knowledge

Share knowledge between projects:

```python
# Export the entire knowledge graph
knowledge_manager.export_graph("project_knowledge.json")

# Export a subset of the knowledge graph
knowledge_manager.export_graph(
    "auth_knowledge.json",
    filter_criteria={"domain": "authentication"}
)

# Import knowledge from a file
knowledge_manager.import_graph("imported_knowledge.json")

# Merge with existing knowledge
knowledge_manager.import_graph(
    "additional_knowledge.json",
    merge_strategy="update_existing"  # Options: replace, update_existing, keep_existing
)
```

## Security and Privacy

Configure security for sensitive knowledge:

```python
# Set access controls
knowledge_manager.set_access_control(
    entity_filter={"domain": "security"},
    access_level="restricted",
    allowed_roles=["security_engineer", "senior_developer"]
)

# Configure privacy settings
knowledge_manager.configure_privacy(
    anonymize_sensitive=True,
    encryption_level="high",
    privacy_tags=["PII", "CREDENTIALS"]
)
```

## Best Practices

1. **Start Small**: Begin with a focused subset of your codebase
2. **Iterative Refinement**: Gradually improve your knowledge graph over time
3. **Domain-Specific Customization**: Define entities and relationships relevant to your domain
4. **Connect External Knowledge**: Integrate domain-specific ontologies and knowledge sources
5. **Use Annotations**: Explicitly annotate code when automatic extraction is insufficient
6. **Maintain Quality**: Regularly review and validate extracted knowledge
7. **Integrate with Workflow**: Use the knowledge graph as part of your development process

## Troubleshooting

Common issues and their solutions:

1. **Low-quality entity extraction**
   - Increase minimum confidence threshold
   - Use more explicit annotations
   - Provide domain-specific training examples

2. **Missing relationships**
   - Decrease minimum confidence for relationships
   - Increase maximum relationship distance
   - Add explicit relationship annotations

3. **Performance issues**
   - Limit extraction to specific entity types
   - Use incremental updates instead of full reprocessing
   - Optimize query patterns

4. **Integration issues with external sources**
   - Verify connection parameters
   - Check for schema compatibility
   - Use mapping functions to align external concepts

## Conclusion

The Knowledge Graph integration in Runa enables a deeper understanding of code beyond syntax and structure. By connecting code components to knowledge entities and relationships, Runa can reason about code at a conceptual level, providing intelligent assistance, better code generation, and enhanced documentation.

For more information on specific knowledge graph features, see the following guides:
- [Entity Extraction](./EntityExtraction.md)
- [Query Patterns](./QueryPatterns.md)
- [External Knowledge Integration](./ExternalSources.md)
- [Domain-Specific Customization](./DomainCustomization.md) 