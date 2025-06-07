# Relationship Identification in Knowledge Graph Integration

This guide explains how Runa identifies and manages relationships between knowledge entities in the knowledge graph.

## Overview

Relationship identification is the process of discovering and defining connections between entities in the knowledge graph. These relationships form the edges that connect entity nodes, creating a rich network of interconnected knowledge that can be traversed, queried, and analyzed.

## Built-in Relationship Types

Runa's knowledge graph system includes the following built-in relationship types:

| Relationship Type | Description | Example |
|-------------------|-------------|---------|
| `CALLS` | Function calls another function | `calculate_total` → `add_tax` |
| `IMPORTS` | Module imports another module | `auth_module` → `encryption_module` |
| `INHERITS_FROM` | Class inherits from another class | `PremiumUser` → `User` |
| `IMPLEMENTS` | Class implements an interface | `FileStorage` → `StorageInterface` |
| `CONTAINS` | Entity contains another entity | `UserManager` → `create_user` |
| `DEPENDS_ON` | Entity depends on another entity | `payment_process` → `card_validation` |
| `REFERENCES` | Entity references another entity | `calculate_risk` → `risk_factors` |
| `FOLLOWS` | Entity follows another in execution | `validate_input` → `process_data` |
| `CREATES` | Entity creates instances of another | `user_factory` → `User` |
| `MODIFIES` | Entity modifies another entity | `update_profile` → `user_data` |
| `USES` | Entity uses another entity | `rendering_engine` → `texture_library` |
| `ASSOCIATED_WITH` | General association between entities | `investment_calculator` → `financial_models` |
| `SIMILAR_TO` | Entities that are semantically similar | `validate_email` → `check_email_format` |
| `PART_OF` | Entity is part of a larger concept | `authentication` → `security_system` |
| `ALTERNATIVE_TO` | Entity is an alternative to another | `quick_sort` → `merge_sort` |
| `DERIVED_FROM` | Entity is derived from another | `enhanced_algorithm` → `base_algorithm` |
| `CONFLICTING_WITH` | Entities that may conflict | `global_state_modifier` → `thread_safety` |

## Relationship Properties

Each relationship has a set of properties that describe it:

```python
relationship = {
    "id": "rel_456",                    # Unique identifier
    "type": "CALLS",                    # Relationship type
    "source_id": "func_123",            # Source entity ID
    "target_id": "func_789",            # Target entity ID
    "source_file": "src/finance.runa",  # Source file location
    "line_number": 18,                  # Line number where the relationship is defined
    "cardinality": "many_to_one",       # Relationship cardinality
    "weight": 0.85,                     # Relationship strength/importance
    "directed": True,                   # Whether the relationship is directed
    "metadata": {                       # Additional metadata
        "call_count": 5,
        "conditional": True,
        "critical_path": False
    },
    "confidence": 0.92,                 # Confidence score of the relationship
    "created_at": "2023-08-15T10:30:00Z", # Creation timestamp
    "updated_at": "2023-08-16T14:25:00Z"  # Last update timestamp
}
```

## Identification Methods

### Automatic Relationship Identification

The knowledge manager can automatically identify relationships through several mechanisms:

```python
from runa.ai.knowledge_graph import knowledge_manager

# Identify relationships in a single file
relationships = knowledge_manager.identify_relationships("src/finance.runa")

# Identify relationships in an entire directory
relationships = knowledge_manager.identify_relationships_recursive("src/")

# Identify relationships between specific entities
relationships = knowledge_manager.identify_relationships_between(
    source_entity_ids=["func_123", "func_456"],
    target_entity_ids=["func_789", "class_101"]
)

# Identify all relationships for an entity
relationships = knowledge_manager.identify_relationships_for_entity("func_123")

# Bulk identification with progress reporting
def progress_callback(processed, total, current_file):
    print(f"Processed {processed}/{total} files. Current: {current_file}")

knowledge_manager.identify_all_relationships(
    root_dir="./",
    file_pattern="**/*.runa",
    progress_callback=progress_callback
)
```

### Manual Relationship Definition

You can also manually define relationships:

```python
from runa.ai.knowledge_graph import knowledge_manager, RelationshipType

# Create a simple relationship
knowledge_manager.create_relationship(
    source_id="func_123",
    target_id="func_789",
    relationship_type=RelationshipType.CALLS
)

# Create a relationship with detailed properties
knowledge_manager.create_relationship(
    source_id="class_101",
    target_id="interface_202",
    relationship_type=RelationshipType.IMPLEMENTS,
    properties={
        "weight": 0.9,
        "metadata": {
            "implementation_completeness": "full",
            "override_methods": ["method1", "method2"]
        }
    }
)

# Create multiple relationships at once
knowledge_manager.create_relationships([
    {
        "source_id": "module_303",
        "target_id": "module_404",
        "type": RelationshipType.IMPORTS
    },
    {
        "source_id": "func_123",
        "target_id": "class_101",
        "type": RelationshipType.USES
    }
])
```

### Code Annotations for Relationship Identification

Use annotations in your code to explicitly define relationships:

```
@RelationshipSource(type="DERIVED_FROM", target="BaseAlgorithm")
@Description("Enhanced version of the base algorithm with optimized performance")
process enhanced_algorithm(data: List[Number]) returns: Result
    # Implementation
    # ...
end

@KnowledgeRelationship(source="payment_processor", target="transaction_validator", type="DEPENDS_ON")
# This annotation defines a relationship outside of directly related code
```

Annotations that influence relationship identification:
- `@RelationshipSource(type, target)`: Defines a relationship where the current entity is the source
- `@RelationshipTarget(type, source)`: Defines a relationship where the current entity is the target
- `@KnowledgeRelationship(source, target, type)`: Defines a relationship between two entities from any context
- `@Override`: Indicates that a method overrides another, implying an INHERITS_FROM relationship
- `@DependsOn(entity_name)`: Indicates that the current entity depends on another
- `@UsedBy(entity_name)`: Indicates that the current entity is used by another

## Identification Pipeline

The relationship identification process follows these steps:

1. **Entity Preparation**: Retrieve entities between which relationships might exist
2. **Static Analysis**: Analyze code structure to identify explicit relationships
3. **Dynamic Analysis**: Analyze code behavior to identify implicit relationships
4. **Semantic Analysis**: Use semantic understanding to identify conceptual relationships
5. **Pattern Matching**: Apply pattern matching to identify common relationship patterns
6. **Confidence Scoring**: Assign confidence scores to each identified relationship
7. **Deduplication**: Merge or resolve duplicate relationships
8. **Storage**: Store relationships in the knowledge graph

```python
# Configure the identification pipeline
knowledge_manager.configure_relationship_identification(
    min_confidence=0.75,                # Minimum confidence score to keep a relationship
    identify_types=[                    # Relationship types to identify
        RelationshipType.CALLS,
        RelationshipType.DEPENDS_ON,
        RelationshipType.INHERITS_FROM
    ],
    max_relationships_per_entity=50,    # Maximum relationships per entity
    use_code_annotations=True,          # Use code annotations
    identify_implicit=True,             # Identify implicit relationships
    advanced_analysis=True,             # Use advanced analysis techniques
    context_sensitivity="high"          # Context sensitivity level
)
```

## Custom Relationship Identifiers

You can create custom relationship identifiers for domain-specific relationships:

```python
from runa.ai.knowledge_graph import knowledge_manager, RelationshipIdentifier

class FinancialDependencyIdentifier(RelationshipIdentifier):
    def __init__(self):
        super().__init__(
            target_type="FINANCIAL_DEPENDENCY",
            supported_file_extensions=[".runa", ".py"]
        )
    
    def identify(self, entities, file_path=None):
        # Custom identification logic for financial dependencies
        relationships = []
        # ... identification implementation ...
        return relationships

# Register the custom identifier
knowledge_manager.register_relationship_identifier(FinancialDependencyIdentifier())
```

## Training Custom Identifiers

For complex domains, you can train custom relationship identifiers:

```python
from runa.ai.knowledge_graph import knowledge_manager

# Define training examples
training_examples = [
    {
        "entities": [
            {"id": "entity1", "name": "Option", "type": "FINANCIAL_INSTRUMENT"},
            {"id": "entity2", "name": "StockPrice", "type": "DOMAIN_CONCEPT"}
        ],
        "relationships": [
            {"source_id": "entity1", "target_id": "entity2", "type": "DERIVED_FROM"}
        ],
        "code": "class Option:\n    def __init__(self, stock_price):\n        self.stock_price = stock_price"
    },
    # More examples...
]

# Train a custom identifier
knowledge_manager.train_custom_relationship_identifier(
    name="financial_relationships_identifier",
    relationship_type="FINANCIAL_DEPENDENCY",
    training_examples=training_examples,
    validation_split=0.2,
    epochs=10
)

# Use the trained identifier
knowledge_manager.identify_relationships(
    "src/trading.runa",
    use_identifiers=["financial_relationships_identifier"]
)
```

## Relationship Query and Management

Once relationships are identified, you can query and manage them:

```python
from runa.ai.knowledge_graph import knowledge_manager

# Get all relationships of a specific type
call_relationships = knowledge_manager.get_relationships_by_type(RelationshipType.CALLS)

# Get relationships with a specific source entity
outgoing_relationships = knowledge_manager.get_relationships_by_source("func_123")

# Get relationships with a specific target entity
incoming_relationships = knowledge_manager.get_relationships_by_target("func_789")

# Get relationships between specific entities
direct_relationships = knowledge_manager.get_relationships_between("func_123", "func_789")

# Get relationship by ID
relationship = knowledge_manager.get_relationship_by_id("rel_456")

# Update a relationship
knowledge_manager.update_relationship(
    relationship_id="rel_456",
    properties={
        "weight": 0.95,
        "metadata": {
            "critical_path": True
        }
    }
)

# Delete a relationship
knowledge_manager.delete_relationship("rel_456")
```

## Path Analysis

Analyze paths and connections between entities:

```python
from runa.ai.knowledge_graph import knowledge_manager

# Find all paths between two entities
paths = knowledge_manager.find_paths(
    source_id="func_123",
    target_id="func_789",
    max_depth=3,                          # Maximum path length
    relationship_types=[                  # Relationship types to consider
        RelationshipType.CALLS,
        RelationshipType.DEPENDS_ON
    ]
)

# Find the shortest path between two entities
shortest_path = knowledge_manager.find_shortest_path(
    source_id="func_123",
    target_id="func_789"
)

# Find all entities connected to an entity
connected_entities = knowledge_manager.find_connected_entities(
    entity_id="func_123",
    max_depth=2,
    direction="outgoing"                  # "outgoing", "incoming", or "both"
)

# Find strongly connected components
components = knowledge_manager.find_strongly_connected_components()

# Analyze dependency cycles
cycles = knowledge_manager.find_dependency_cycles()
```

## Graph Algorithms

Apply graph algorithms to analyze relationships:

```python
from runa.ai.knowledge_graph import knowledge_manager

# Find central entities using various centrality measures
central_entities = knowledge_manager.compute_centrality(
    algorithm="pagerank",                 # "pagerank", "betweenness", "closeness", etc.
    entity_type=EntityType.FUNCTION       # Optional filter by entity type
)

# Find communities using community detection
communities = knowledge_manager.detect_communities(
    algorithm="louvain",                  # "louvain", "label_propagation", etc.
    min_community_size=3                  # Minimum community size
)

# Analyze the impact of removing an entity
impact_analysis = knowledge_manager.analyze_removal_impact("func_123")

# Find similar entities based on relationship patterns
similar_entities = knowledge_manager.find_similar_entities(
    entity_id="func_123",
    similarity_metric="structural",       # "structural", "semantic", "hybrid"
    min_similarity=0.7                    # Minimum similarity score
)
```

## Batch Processing

For large codebases, batch processing is more efficient:

```python
from runa.ai.knowledge_graph import knowledge_manager

# Start a batch identification session
with knowledge_manager.batch_session() as batch:
    # Identify relationships in multiple files
    for file_path in file_list:
        batch.identify_relationships(file_path)
    
    # The changes will be committed at the end of the session
```

## Integration with Code Analysis

Relationship identification can leverage code analysis results:

```python
from runa.ai.knowledge_graph import knowledge_manager
from runa.analysis import code_analyzer

# Analyze code
analysis_result = code_analyzer.analyze("src/finance.runa")

# Identify relationships with analysis context
relationships = knowledge_manager.identify_relationships_with_analysis(
    "src/finance.runa", 
    analysis_context=analysis_result
)
```

## Relationship Quality and Inference

Improve the quality of relationships and infer new ones:

```python
from runa.ai.knowledge_graph import knowledge_manager

# Get relationship quality metrics
quality_metrics = knowledge_manager.get_relationship_quality()
print(f"Average confidence: {quality_metrics['average_confidence']}")
print(f"Coverage: {quality_metrics['coverage']}")

# Identify potential issues
issues = knowledge_manager.identify_relationship_issues()
for issue in issues:
    print(f"Issue: {issue['type']} in {issue['relationship_id']}")

# Improve relationship quality
knowledge_manager.improve_relationship_quality(
    relationship_ids=["rel_456", "rel_457"],
    improvements=["weights", "metadata"]
)

# Infer new relationships based on existing ones
inferred_relationships = knowledge_manager.infer_relationships(
    inference_rules=["transitive", "symmetric", "inverse"],
    min_inference_confidence=0.7
)
```

## Semantic Relationship Discovery

Discover relationships based on semantic understanding:

```python
from runa.ai.knowledge_graph import knowledge_manager

# Discover semantic relationships
semantic_relationships = knowledge_manager.discover_semantic_relationships(
    entity_ids=["func_123", "func_789"],
    semantic_model="code_bert",           # Model for semantic analysis
    min_semantic_similarity=0.8           # Minimum semantic similarity
)

# Discover relationships based on natural language descriptions
nl_relationships = knowledge_manager.discover_relationships_from_descriptions(
    entity_ids=["func_123", "func_789"]
)

# Discover domain-specific relationships
domain_relationships = knowledge_manager.discover_domain_relationships(
    domain="finance",
    relationship_patterns=[
        "asset_allocation",
        "risk_assessment"
    ]
)
```

## Visualization and Export

Visualize and export relationships:

```python
from runa.ai.knowledge_graph import knowledge_manager

# Export relationships to various formats
knowledge_manager.export_relationships(
    output_path="relationships.json",
    format="json",                         # "json", "csv", "graphml", "neo4j"
    include_entity_details=True
)

# Generate a visual graph representation
knowledge_manager.generate_relationship_graph(
    output_path="relationship_graph.html",
    layout="force_directed",               # Graph layout algorithm
    highlight_entity_ids=["func_123"],     # Entities to highlight
    filter_relationship_types=[            # Relationship types to include
        RelationshipType.CALLS,
        RelationshipType.DEPENDS_ON
    ]
)
```

## Best Practices for Relationship Identification

1. **Focus on Important Relationships**: Prioritize identification of critical relationships that impact understanding and maintenance
2. **Use Code Annotations**: Add explicit annotations for complex or non-obvious relationships
3. **Combine Static and Dynamic Analysis**: Use both static code analysis and runtime behavior analysis for complete relationship identification
4. **Consider Confidence Levels**: Pay attention to confidence scores and verify low-confidence relationships
5. **Validate Critical Paths**: Manually verify relationships in critical execution paths
6. **Maintain Relationship Hygiene**: Regularly review and clean up the relationship graph to remove outdated or incorrect relationships
7. **Use Domain Knowledge**: Incorporate domain-specific knowledge into relationship identification rules
8. **Balance Precision and Recall**: Adjust identification settings to achieve the right balance between precision and recall for your needs

## Troubleshooting Relationship Identification

Common issues and solutions:

1. **Missing relationships**
   - Lower the confidence threshold
   - Add explicit annotations for important relationships
   - Check for complex code patterns that might be missed by analyzers

2. **Incorrect relationships**
   - Review and adjust identification rules
   - Add explicit annotations to override automatic identification
   - Improve training data for custom identifiers

3. **Excessive relationships**
   - Increase the confidence threshold
   - Focus on specific relationship types
   - Filter out less important relationships

4. **Slow identification**
   - Use batch processing
   - Focus on specific parts of the codebase
   - Limit the relationship types being identified

5. **Relationship cycles**
   - Use the cycle detection tools to identify problematic dependencies
   - Refactor code to break unnecessary cycles
   - Add constraints to prevent problematic relationship patterns

## Advanced Configuration

Fine-tune relationship identification with advanced configuration:

```python
from runa.ai.knowledge_graph import knowledge_manager

# Detailed relationship identification configuration
knowledge_manager.configure_relationship_identification_advanced({
    "static_analysis": {
        "depth": "detailed",              # Analysis depth
        "framework_awareness": True,       # Framework-specific analysis
        "pattern_library": "extended",     # Pattern library to use
        "context_window": 5                # Context window size
    },
    "dynamic_analysis": {
        "enabled": True,                   # Enable dynamic analysis
        "sample_inputs": ["input1", "input2"], # Sample inputs for dynamic analysis
        "coverage_target": 0.7,            # Target code coverage
        "max_execution_time": 30           # Maximum execution time in seconds
    },
    "semantic_analysis": {
        "model_type": "large",             # Semantic model size
        "similarity_threshold": 0.75,      # Similarity threshold
        "domain_adaptation": True          # Domain-specific adaptation
    },
    "confidence_scoring": {
        "weightings": {                    # Weights for different analysis types
            "static": 0.5,
            "dynamic": 0.3,
            "semantic": 0.2
        },
        "threshold_adjustments": {         # Type-specific thresholds
            "CALLS": 0.8,
            "DEPENDS_ON": 0.7,
            "SIMILAR_TO": 0.85
        }
    },
    "deduplication": {
        "strategy": "merge_properties",    # Deduplication strategy
        "similarity_threshold": 0.9        # Similarity threshold for deduplication
    },
    "inference": {
        "enabled": True,                   # Enable relationship inference
        "rules": ["transitive", "inverse"], # Inference rules to apply
        "max_inference_depth": 2,          # Maximum inference depth
        "min_confidence": 0.7              # Minimum inference confidence
    }
})
```

## Conclusion

Relationship identification is a critical component of building a useful knowledge graph. By properly configuring and utilizing Runa's relationship identification capabilities, you can create a rich network of interconnected knowledge that enhances code understanding, enables powerful queries, and supports intelligent reasoning about your codebase.

For more information on how to work with identified relationships, see the following guides:
- [Query Patterns](./QueryPatterns.md)
- [Knowledge Graph Visualization](./Visualization.md)
- [Knowledge-Enhanced Code Generation](./CodeGeneration.md)
``` 