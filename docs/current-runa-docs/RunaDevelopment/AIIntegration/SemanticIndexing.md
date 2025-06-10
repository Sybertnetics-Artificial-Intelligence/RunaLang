# Semantic Indexing in Runa

## Overview

Runa's Semantic Indexing system provides powerful capabilities for creating, managing, and querying semantic representations of code and documentation. This enables intelligent code search, contextual understanding, and knowledge retrieval that goes beyond simple text matching to capture the meaning and intent of code and comments.

## Core Features

### 1. Code Indexing

Index entire codebases with semantic understanding:

```
# Create a semantic indexer
Let indexer be SemanticIndexer.create with dictionary with:
    "embedding_model" as "code-embedding-v1"
    "chunk_size" as "function"  # Options: function, block, file
    "include_comments" as true
    "include_types" as true

# Index a codebase
Let index be indexer.index_codebase with "./src/" and dictionary with:
    "file_extensions" as list containing ".runa"
    "exclude_patterns" as list containing "**/test/**", "**/vendor/**"
    "recurse" as true

# Save the index
Call index.save with "./semantic_index/code_index"
```

### 2. Semantic Search

Perform natural language searches against your semantic index:

```
# Load an existing index
Let index be SemanticIndex.load with "./semantic_index/code_index"

# Perform a semantic search
Let results be index.search with "function to calculate fibonacci sequence" and dictionary with:
    "limit" as 10
    "min_score" as 0.7
    "include_context" as true

# Process results
For each result in results:
    Display "Score:" with message result.score
    Display "File:" with message result.file
    Display "Function:" with message result.function_name
    Display "Snippet:" with message result.snippet
```

### 3. Code Understanding

Extract semantic meaning and relationships from code:

```
# Create a code understanding engine
Let understanding be CodeUnderstanding.create with index

# Extract function relationships
Let function_graph be understanding.extract_function_relationships with dictionary with:
    "include_calls" as true
    "include_dependencies" as true
    "include_inheritance" as true

# Find related functions
Let related be understanding.find_related_functions with "calculate_average" and dictionary with:
    "relationship_types" as list containing "calls", "called_by", "similar_purpose"
    "max_distance" as 2
    "min_similarity" as 0.6

# Generate function summary
Let summary be understanding.summarize_function with "calculate_statistics" and dictionary with:
    "include_parameters" as true
    "include_return_value" as true
    "max_length" as 100
```

### 4. Documentation Integration

Connect code with documentation for comprehensive understanding:

```
# Index documentation
Let doc_indexer be DocumentationIndexer.create with dictionary with:
    "embedding_model" as "doc-embedding-v1"
    "chunk_size" as "section"

Let doc_index be doc_indexer.index_documentation with "./docs/" and dictionary with:
    "file_extensions" as list containing ".md", ".rst"
    "exclude_patterns" as list containing "**/draft/**"

# Link code and documentation
Let linker be CodeDocLinker.create with dictionary with:
    "code_index" as index
    "doc_index" as doc_index

Let linked_index be linker.link with dictionary with:
    "min_similarity" as 0.7
    "create_bidirectional" as true

# Query with context from both code and docs
Let results be linked_index.search with "file handling with error checking" and dictionary with:
    "include_code" as true
    "include_docs" as true
```

### 5. Intelligent Autocomplete

Provide context-aware code suggestions:

```
# Create an autocomplete engine
Let autocomplete be SemanticAutocomplete.create with dictionary with:
    "semantic_index" as index
    "context_window" as 5  # Lines before cursor
    "suggestion_count" as 5

# Get completions for a given context
Let completions be autocomplete.suggest with:
    file_path as "./src/app.runa"
    line_number as 42
    prefix as "Let result = calculate_"

# Use the completions
For each completion in completions:
    Display "Completion:" with message completion.text
    Display "Confidence:" with message completion.confidence
    Display "Type:" with message completion.return_type
```

## Advanced Features

### 1. Incremental Indexing

Efficiently update your semantic index when code changes:

```
# Update only changed files
Let changes be index.update_from_changes with dictionary with:
    "added_files" as list containing "./src/new_feature.runa"
    "modified_files" as list containing "./src/fixed_bug.runa"
    "deleted_files" as list containing "./src/old_feature.runa"

# Or scan for changes automatically
Call index.update_from_filesystem with "./src/" and dictionary with:
    "detect_changes" as true
    "use_git_history" as true
```

### 2. Custom Embedding Models

Use or train custom embedding models for domain-specific codebases:

```
# Use a custom model
Let custom_indexer be SemanticIndexer.create with dictionary with:
    "embedding_model_path" as "./models/domain_code_embedding/"
    "tokenizer_path" as "./models/domain_tokenizer/"

# Fine-tune an embedding model
Let fine_tuner be EmbeddingModelFineTuner.create with dictionary with:
    "base_model" as "code-embedding-v1"
    "training_data" as "./domain_code_samples/"
    "epochs" as 5
    "learning_rate" as 1e-5

Let tuned_model be fine_tuner.train
Call tuned_model.save with "./models/tuned_embedding_model/"
```

### 3. Multi-language Support

Index and search across multiple programming languages:

```
# Create a multi-language indexer
Let multi_indexer be SemanticIndexer.create with dictionary with:
    "languages" as list containing "runa", "python", "javascript", "rust"
    "normalize_syntax" as true
    "cross_language_search" as true

# Index a multilingual project
Let polyglot_index be multi_indexer.index_codebase with "./project/" and dictionary with:
    "file_extensions" as list containing ".runa", ".py", ".js", ".rs"

# Find similar code across languages
Let cross_lang_results be polyglot_index.search with "authentication middleware" and dictionary with:
    "group_by_language" as true
```

### 4. Semantic Diff and Evolution Tracking

Track semantic changes in your codebase over time:

```
# Create a semantic evolution tracker
Let evo_tracker be CodeEvolutionTracker.create with dictionary with:
    "semantic_index" as index
    "git_repository" as "./"
    "track_interval" as "commit"  # Options: commit, tag, release

# Analyze semantic evolution
Let evolution be evo_tracker.analyze_evolution with "src/core/" and dictionary with:
    "start_point" as "v1.0.0"
    "end_point" as "v2.0.0"

# Get semantic diff between versions
Let diff be evo_tracker.semantic_diff with "function_a" and dictionary with:
    "from_version" as "v1.0.0"
    "to_version" as "v2.0.0"

# Visualize code evolution
Let viz be evo_tracker.visualize_evolution with "src/core/auth.runa"
Call viz.save with "auth_evolution.svg"
```

## Integration with Knowledge Graph and LLM

### Enhancing Knowledge Graphs with Semantic Code Information

```
# Create a knowledge graph from semantic index
Let kg_builder be KnowledgeGraphBuilder.create with dictionary with:
    "semantic_index" as index
    "entity_types" as list containing "function", "class", "module"
    "relationship_types" as list containing "calls", "inherits", "imports", "similar_to"

Let code_kg be kg_builder.build_graph

# Enrich knowledge graph with semantic information
Call code_kg.add_entity_property with "semantic_vector" and index.get_all_vectors
Call code_kg.add_relationship_property with "semantic_similarity" and index.get_all_similarities

# Query the knowledge graph with semantic context
Let query_results be code_kg.query_with_semantics with "error handling in network code" and dictionary with:
    "max_path_length" as 3
```

### Enhancing LLMs with Semantic Code Context

```
# Connect semantic index with LLM
Let semantic_llm be LLM.connect_with_context with "runa_assistant_model" and dictionary with:
    "semantic_index" as index
    "retrieval_strategy" as "hybrid"  # hybrid combines keyword and semantic search
    "max_context_items" as 5

# Get code-aware completions
Let completion be semantic_llm.complete_with_context with "Write a function to validate user input" and dictionary with:
    "project_context" as true

# Generate code with semantic awareness
Let code_generation be semantic_llm.generate_code_with_context with "Create a cache system consistent with our codebase" and dictionary with:
    "retrieve_similar_patterns" as true
```

## Example: Building a Semantic Code Search System

```
Process called "create_code_search_system":
    # Initialize the components
    Let indexer be SemanticIndexer.create with dictionary with:
        "embedding_model" as "code-embedding-v1"
        "chunk_size" as "function"
    
    Let doc_indexer be DocumentationIndexer.create with dictionary with:
        "embedding_model" as "doc-embedding-v1"
        "chunk_size" as "section"
    
    # 1. Index code and documentation
    Display "Indexing codebase..."
    Let code_index be indexer.index_codebase with "./src/"
    
    Display "Indexing documentation..."
    Let doc_index be doc_indexer.index_documentation with "./docs/"
    
    # 2. Link code and documentation
    Display "Linking code and documentation..."
    Let linker be CodeDocLinker.create with dictionary with:
        "code_index" as code_index
        "doc_index" as doc_index
    
    Let linked_index be linker.link
    
    # 3. Create a knowledge graph from the semantic index
    Display "Building knowledge graph..."
    Let kg_builder be KnowledgeGraphBuilder.create with dictionary with:
        "semantic_index" as linked_index
    
    Let knowledge_graph be kg_builder.build_graph
    
    # 4. Create a search API
    Display "Creating search API..."
    Let search_api be CodeSearchAPI.create with dictionary with:
        "semantic_index" as linked_index
        "knowledge_graph" as knowledge_graph
    
    # 5. Define search function
    Process called "semantic_search" that takes query and options:
        Let default_options be dictionary with:
            "limit" as 10
            "min_score" as 0.6
            "include_code" as true
            "include_docs" as true
            "include_graph" as true
        
        # Merge default options with provided options
        Let search_options be default_options.merge with options
        
        # Perform search
        Let results be search_api.search with query and search_options
        
        # Format and return results
        Return dictionary with:
            "query" as query
            "results_count" as results.count
            "top_results" as results.top with 5
            "related_concepts" as results.related_concepts
            "suggested_queries" as results.suggested_queries
    
    # 6. Save components for future use
    Display "Saving system components..."
    Call linked_index.save with "./semantic_system/linked_index"
    Call knowledge_graph.save with "./semantic_system/knowledge_graph"
    
    # 7. Return the search function
    Return semantic_search
```

## Best Practices for Semantic Indexing

1. **Index Granularity**: Choose the appropriate chunk size for your use case—function-level is good for focused queries, while file-level may be better for broader questions.

2. **Regular Updates**: Keep your semantic index up-to-date as your codebase evolves to ensure accuracy of search results.

3. **Custom Embeddings**: For domain-specific codebases, consider fine-tuning embeddings to capture domain-specific concepts and terminology.

4. **Hybrid Search**: Combine semantic search with traditional search methods (keyword, regex) for comprehensive results.

5. **Contextual Relevance**: When displaying results, include sufficient context to help understand why a result was returned.

6. **Optimize Index Size**: For large codebases, consider partitioning indices by modules or components to improve performance.

## References

- [Runa Semantic Indexing API Reference](https://runa-lang.org/docs/api/semantic-indexing)
- [Code Search Best Practices](https://runa-lang.org/docs/guides/code-search)
- [Embedding Models Documentation](https://runa-lang.org/docs/models/embedding)

For complete examples, see the [Semantic Indexing Examples](../../src/tests/examples/semantic_indexing_examples.runa) in the Runa codebase. 