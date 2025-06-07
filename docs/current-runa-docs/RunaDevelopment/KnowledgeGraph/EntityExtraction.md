# Entity Extraction in Knowledge Graph Integration

This guide provides a detailed explanation of how Runa extracts knowledge entities from code and transforms them into structured knowledge graph nodes.

## Overview

Entity extraction is the process of identifying and extracting meaningful entities from code that represent concepts, components, or domain knowledge. This is the foundation of building a useful knowledge graph that can enhance code understanding, generation, and reasoning.

## Entity Types

Runa's knowledge graph system supports the following built-in entity types:

| Entity Type | Description | Examples |
|-------------|-------------|----------|
| `FUNCTION` | Represents functions, methods, or processes | `calculate_total()`, `process_payment()` |
| `CLASS` | Represents classes, types, or data structures | `User`, `Transaction`, `DataProcessor` |
| `VARIABLE` | Represents variables, fields, or properties | `total_amount`, `user_id`, `is_active` |
| `MODULE` | Represents modules, packages, or namespaces | `auth_module`, `data_processing` |
| `PARAMETER` | Represents function parameters or arguments | `user_id` in `get_user(user_id)` |
| `RETURN_VALUE` | Represents function return values | Return value of `calculate_total()` |
| `ALGORITHM` | Represents algorithmic patterns or approaches | `quick_sort`, `breadth_first_search` |
| `DOMAIN_CONCEPT` | Represents domain-specific concepts | `investment_portfolio`, `risk_assessment` |
| `DESIGN_PATTERN` | Represents software design patterns | `singleton`, `factory`, `observer` |
| `API` | Represents APIs or interfaces | `user_authentication_api`, `data_access_layer` |

## Entity Properties

Each entity has a set of properties that describe it:

```python
entity = {
    "id": "func_123",                      # Unique identifier
    "name": "calculate_total",             # Display name
    "type": "FUNCTION",                    # Entity type
    "source_file": "src/finance.runa",     # Source file location
    "line_range": (15, 22),                # Line range in source
    "signature": "calculate_total(items: List[Item]) -> Number",  # Function/method signature
    "description": "Calculates the total price of all items",    # Description
    "namespace": "finance.calculations",   # Namespace/module
    "metadata": {                          # Additional metadata
        "complexity": "low",
        "visibility": "public",
        "test_coverage": 0.85
    },
    "confidence": 0.95,                    # Confidence score of extraction
    "annotations": ["@Pure", "@Tested"],   # Code annotations
    "tags": ["financial", "core"],         # Knowledge tags
    "created_at": "2023-08-15T10:30:00Z",  # Creation timestamp
    "updated_at": "2023-08-16T14:25:00Z"   # Last update timestamp
}
```

## Extraction Methods

### Automatic Extraction

The knowledge manager automatically extracts entities through several mechanisms:

```python
from runa.ai.knowledge_graph import knowledge_manager

# Extract from a single file
entities = knowledge_manager.extract_entities("src/finance.runa")

# Extract from an entire directory
entities = knowledge_manager.extract_entities_recursive("src/")

# Extract from a specific module
entities = knowledge_manager.extract_entities_from_module("finance.calculations")

# Extract from a code string
code = """
process calculate_tax(amount: Number, rate: Number) returns: Number
    return amount * (rate / 100)
end
"""
entities = knowledge_manager.extract_entities_from_string(code)

# Bulk extraction with progress reporting
def progress_callback(processed, total, current_file):
    print(f"Processed {processed}/{total} files. Current: {current_file}")

knowledge_manager.extract_all(
    root_dir="./",
    file_pattern="**/*.runa",
    progress_callback=progress_callback
)
```

### Manual Entity Definition

You can also manually define entities:

```python
from runa.ai.knowledge_graph import knowledge_manager, EntityType

# Create a function entity
knowledge_manager.create_entity(
    name="calculate_compound_interest",
    entity_type=EntityType.FUNCTION,
    properties={
        "signature": "calculate_compound_interest(principal: Number, rate: Number, time: Number) -> Number",
        "description": "Calculates compound interest over time",
        "namespace": "finance.calculations"
    }
)

# Create a domain concept entity
knowledge_manager.create_entity(
    name="CompoundInterestFormula",
    entity_type=EntityType.DOMAIN_CONCEPT,
    properties={
        "description": "Formula for calculating interest compounded over time",
        "formula": "A = P(1 + r/n)^(nt)",
        "domain": "finance"
    }
)
```

### Code Annotations for Entity Extraction

Use annotations in your code to explicitly define entities:

```
@KnowledgeEntity(type="ALGORITHM", name="BlackScholesModel")
@Description("Implementation of the Black-Scholes model for option pricing")
@Domain("finance.derivatives")
process price_option(strike: Number, spot: Number, 
                     volatility: Number, rate: Number, 
                     time: Number) returns: Number
    # Implementation
    # ...
end
```

Annotations that influence entity extraction:
- `@KnowledgeEntity(type, name)`: Defines an explicit entity
- `@Description(text)`: Provides a description for the entity
- `@Domain(domain_path)`: Assigns the entity to a domain
- `@Tags(tag1, tag2, ...)`: Adds knowledge tags to the entity
- `@Complexity(level)`: Specifies computational complexity
- `@See(entity_name)`: Links to a related entity

## Extraction Pipeline

The entity extraction process follows these steps:

1. **Parsing**: Code is parsed into an Abstract Syntax Tree (AST)
2. **Identification**: Potential entities are identified in the AST
3. **Classification**: Entities are classified by type
4. **Property Extraction**: Properties are extracted for each entity
5. **Deduplication**: Duplicate entities are merged or resolved
6. **Confidence Scoring**: Confidence scores are assigned to each entity
7. **Storage**: Entities are stored in the knowledge graph

```python
# Configure the extraction pipeline
knowledge_manager.configure_extraction(
    min_confidence=0.7,                # Minimum confidence score to keep an entity
    extract_types=[                    # Entity types to extract
        EntityType.FUNCTION,
        EntityType.CLASS,
        EntityType.DOMAIN_CONCEPT
    ],
    max_entities_per_file=100,         # Maximum entities per file
    extract_properties=True,           # Extract entity properties
    extract_descriptions=True,         # Extract natural language descriptions
    use_code_annotations=True,         # Use code annotations
    extract_deprecated=False,          # Skip deprecated entities
    advanced_nlp=True                  # Use advanced NLP for better extraction
)
```

## Custom Entity Extractors

You can create custom entity extractors for domain-specific entities:

```python
from runa.ai.knowledge_graph import knowledge_manager, EntityExtractor, EntityType

class FinancialInstrumentExtractor(EntityExtractor):
    def __init__(self):
        super().__init__(
            target_type="FINANCIAL_INSTRUMENT",
            supported_file_extensions=[".runa", ".py"]
        )
    
    def extract(self, code, file_path=None):
        # Custom extraction logic for financial instruments
        entities = []
        # ... extraction implementation ...
        return entities

# Register the custom extractor
knowledge_manager.register_entity_extractor(FinancialInstrumentExtractor())
```

## Training Custom Extractors

For complex domains, you can train custom extractors:

```python
from runa.ai.knowledge_graph import knowledge_manager

# Define training examples
training_examples = [
    {
        "code": "class Option(Asset): ...",
        "entities": [
            {"name": "Option", "type": "FINANCIAL_INSTRUMENT", "properties": {...}}
        ]
    },
    # More examples...
]

# Train a custom extractor
knowledge_manager.train_custom_extractor(
    name="financial_instruments_extractor",
    entity_type="FINANCIAL_INSTRUMENT",
    training_examples=training_examples,
    validation_split=0.2,
    epochs=10
)

# Use the trained extractor
knowledge_manager.extract_entities(
    "src/trading.runa",
    use_extractors=["financial_instruments_extractor"]
)
```

## Entity Query and Management

Once entities are extracted, you can query and manage them:

```python
from runa.ai.knowledge_graph import knowledge_manager

# Get all entities of a specific type
functions = knowledge_manager.get_entities_by_type(EntityType.FUNCTION)

# Get entities by name pattern
calculation_entities = knowledge_manager.get_entities_by_name_pattern("calculate_*")

# Get entities in a specific namespace
auth_entities = knowledge_manager.get_entities_by_namespace("auth.*")

# Get entities with specific tags
financial_entities = knowledge_manager.get_entities_by_tags(["financial", "core"])

# Get entity by ID
entity = knowledge_manager.get_entity_by_id("func_123")

# Update an entity
knowledge_manager.update_entity(
    entity_id="func_123",
    properties={
        "description": "Updated description",
        "tags": ["financial", "core", "updated"]
    }
)

# Delete an entity
knowledge_manager.delete_entity("func_123")
```

## Batch Processing

For large codebases, batch processing is more efficient:

```python
from runa.ai.knowledge_graph import knowledge_manager

# Start a batch extraction session
with knowledge_manager.batch_session() as batch:
    # Extract from multiple files
    for file_path in file_list:
        batch.extract_entities(file_path)
    
    # The changes will be committed at the end of the session
```

## Integration with Code Analysis

Entity extraction can leverage code analysis results:

```python
from runa.ai.knowledge_graph import knowledge_manager
from runa.analysis import code_analyzer

# Analyze code
analysis_result = code_analyzer.analyze("src/finance.runa")

# Extract entities with analysis context
entities = knowledge_manager.extract_entities_with_analysis(
    "src/finance.runa", 
    analysis_context=analysis_result
)
```

## Extraction from Documentation

Entities can also be extracted from documentation:

```python
from runa.ai.knowledge_graph import knowledge_manager

# Extract from documentation files
doc_entities = knowledge_manager.extract_from_documentation(
    "docs/api_reference.md",
    doc_type="markdown"
)

# Extract from inline documentation
code_with_docs = """
/**
 * Calculates compound interest over time.
 * 
 * @param principal The initial amount
 * @param rate The interest rate (percentage)
 * @param time The time period in years
 * @return The final amount after compound interest
 */
process calculate_compound_interest(principal: Number, rate: Number, time: Number) returns: Number
    # Implementation
    # ...
end
"""
entities = knowledge_manager.extract_entities_from_string(
    code_with_docs,
    extract_from_docs=True
)
```

## Entity Enrichment

After extraction, entities can be enriched with additional information:

```python
from runa.ai.knowledge_graph import knowledge_manager

# Enrich entities with NLP-derived information
knowledge_manager.enrich_entities(
    entity_ids=["func_123", "func_124"],
    enrichment_type="nlp_analysis"
)

# Enrich with external knowledge
knowledge_manager.enrich_with_external_knowledge(
    entity_ids=["func_123"],
    external_source="finance_ontology"
)

# Automatic enrichment for all entities
knowledge_manager.auto_enrich_all(
    enrichment_types=["nlp_analysis", "code_metrics", "usage_statistics"]
)
```

## Quality Measurement and Improvement

Measure and improve entity extraction quality:

```python
from runa.ai.knowledge_graph import knowledge_manager

# Get extraction quality metrics
quality_metrics = knowledge_manager.get_extraction_quality()
print(f"Average confidence: {quality_metrics['average_confidence']}")
print(f"Coverage: {quality_metrics['coverage']}")

# Identify potential issues
issues = knowledge_manager.identify_extraction_issues()
for issue in issues:
    print(f"Issue: {issue['type']} in {issue['entity_id']}")

# Improve entity quality
knowledge_manager.improve_entity_quality(
    entity_ids=["func_123", "func_124"],
    improvements=["descriptions", "properties"]
)
```

## Best Practices for Entity Extraction

1. **Start with Core Components**: Begin by extracting entities from your core codebase components
2. **Use Annotations for Clarity**: Add explicit annotations to complex or non-obvious entities
3. **Configure Confidence Thresholds**: Adjust confidence thresholds to balance precision and recall
4. **Create Domain-Specific Extractors**: For specialized domains, create custom extractors
5. **Review and Refine**: Regularly review extracted entities and refine the extraction process
6. **Combine Automatic and Manual**: Use automatic extraction as a base, then manually refine important entities
7. **Consider Documentation**: Extract entities from documentation in addition to code
8. **Maintain Consistency**: Ensure consistent naming and categorization of entities

## Troubleshooting Entity Extraction

Common issues and solutions:

1. **Low quality entities**
   - Increase the minimum confidence threshold
   - Add more explicit annotations
   - Check for code style inconsistencies

2. **Missing entities**
   - Lower the confidence threshold
   - Expand the types of entities being extracted
   - Add explicit annotations for important entities

3. **Duplicate entities**
   - Tune the deduplication settings
   - Use consistent naming conventions
   - Add namespaces to disambiguate entities

4. **Slow extraction**
   - Use batch processing
   - Extract only necessary entity types
   - Limit extraction to relevant files or modules

5. **Incorrect entity types**
   - Add explicit type annotations
   - Create custom extractors for specialized types
   - Improve training data for custom extractors

## Advanced Configuration

Fine-tune extraction with advanced configuration:

```python
from runa.ai.knowledge_graph import knowledge_manager

# Detailed extraction configuration
knowledge_manager.configure_extraction_advanced({
    "parsing": {
        "max_file_size": 1000000,         # Maximum file size to parse
        "timeout_seconds": 30,             # Parsing timeout
        "parser_type": "incremental"       # Parser type (standard, incremental, robust)
    },
    "identification": {
        "sensitivity": "high",             # Identification sensitivity
        "context_window": 5,               # Context window size
        "heuristics_level": "aggressive"   # Heuristics level
    },
    "classification": {
        "model_type": "neural",            # Classification model type
        "threshold_adjustments": {         # Type-specific thresholds
            "FUNCTION": 0.7,
            "CLASS": 0.8,
            "DOMAIN_CONCEPT": 0.6
        }
    },
    "property_extraction": {
        "depth": "detailed",               # Property extraction depth
        "infer_descriptions": True,        # Infer missing descriptions
        "max_properties": 20               # Maximum properties per entity
    },
    "deduplication": {
        "strategy": "smart_merge",         # Deduplication strategy
        "similarity_threshold": 0.85,      # Similarity threshold
        "merge_behavior": "keep_best"      # Merge behavior
    },
    "storage": {
        "batch_size": 100,                 # Storage batch size
        "index_properties": ["name", "namespace", "tags"] # Properties to index
    }
})
```

## Conclusion

Entity extraction is the foundation of a useful knowledge graph. By properly configuring and utilizing Runa's entity extraction capabilities, you can create a rich knowledge representation of your codebase that enables intelligent code understanding, generation, and reasoning.

For more information on how to work with extracted entities, see the following guides:
- [Relationship Identification](./RelationshipIdentification.md)
- [Query Patterns](./QueryPatterns.md)
- [Knowledge Graph Visualization](./Visualization.md)
``` 