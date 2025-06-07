# Semantic Indexing in Runa

## Overview

Runa's Semantic Indexing system provides powerful capabilities for creating, managing, and querying semantic representations of code and documentation. This enables intelligent code search, contextual understanding, and knowledge retrieval that goes beyond simple text matching to capture the meaning and intent of code and comments.

## Core Features

### 1. Code Indexing

Index entire codebases with semantic understanding:

```runa
# Create a semantic indexer
Let indexer = SemanticIndexer.create({
    "embedding_model": "code-embedding-v1",
    "chunk_size": "function",  # Options: function, block, file
    "include_comments": true,
    "include_types": true
})

# Index a codebase
Let index = indexer.index_codebase("./src/", {
    "file_extensions": [".runa"],
    "exclude_patterns": ["**/test/**", "**/vendor/**"],
    "recurse": true
})

# Save the index
index.save("./semantic_index/code_index")
```

### 2. Semantic Search

Perform natural language searches against your semantic index:

```runa
# Load an existing index
Let index = SemanticIndex.load("./semantic_index/code_index")

# Perform a semantic search
Let results = index.search("function to calculate fibonacci sequence", {
    "limit": 10,
    "min_score": 0.7,
    "include_context": true
})

# Process results
For result in results:
    Print("Score: " + result.score)
    Print("File: " + result.file)
    Print("Function: " + result.function_name)
    Print("Snippet: \n" + result.snippet)
```

### 3. Code Understanding

Extract semantic meaning and relationships from code:

```runa
# Create a code understanding engine
Let understanding = CodeUnderstanding.create(index)

# Extract function relationships
Let function_graph = understanding.extract_function_relationships({
    "include_calls": true,
    "include_dependencies": true,
    "include_inheritance": true
})

# Find related functions
Let related = understanding.find_related_functions("calculate_average", {
    "relationship_types": ["calls", "called_by", "similar_purpose"],
    "max_distance": 2,
    "min_similarity": 0.6
})

# Generate function summary
Let summary = understanding.summarize_function("calculate_statistics", {
    "include_parameters": true,
    "include_return_value": true,
    "max_length": 100
})
```

### 4. Documentation Integration

Connect code with documentation for comprehensive understanding:

```runa
# Index documentation
Let doc_indexer = DocumentationIndexer.create({
    "embedding_model": "doc-embedding-v1",
    "chunk_size": "section"
})

Let doc_index = doc_indexer.index_documentation("./docs/", {
    "file_extensions": [".md", ".rst"],
    "exclude_patterns": ["**/draft/**"]
})

# Link code and documentation
Let linker = CodeDocLinker.create({
    "code_index": index,
    "doc_index": doc_index
})

Let linked_index = linker.link({
    "min_similarity": 0.7,
    "create_bidirectional": true
})

# Query with context from both code and docs
Let results = linked_index.search("file handling with error checking", {
    "include_code": true,
    "include_docs": true
})
```

### 5. Intelligent Autocomplete

Provide context-aware code suggestions:

```runa
# Create an autocomplete engine
Let autocomplete = SemanticAutocomplete.create({
    "semantic_index": index,
    "context_window": 5,  # Lines before cursor
    "suggestion_count": 5
})

# Get completions for a given context
Let completions = autocomplete.suggest(
    file_path="./src/app.runa",
    line_number=42,
    prefix="Let result = calculate_"
)

# Use the completions
For completion in completions:
    Print("Completion: " + completion.text)
    Print("Confidence: " + completion.confidence)
    Print("Type: " + completion.return_type)
```

## Advanced Features

### 1. Incremental Indexing

Efficiently update your semantic index when code changes:

```runa
# Update only changed files
Let changes = index.update_from_changes({
    "added_files": ["./src/new_feature.runa"],
    "modified_files": ["./src/fixed_bug.runa"],
    "deleted_files": ["./src/old_feature.runa"]
})

# Or scan for changes automatically
index.update_from_filesystem("./src/", {
    "detect_changes": true,
    "use_git_history": true
})
```

### 2. Custom Embedding Models

Use or train custom embedding models for domain-specific codebases:

```runa
# Use a custom model
Let custom_indexer = SemanticIndexer.create({
    "embedding_model_path": "./models/domain_code_embedding/",
    "tokenizer_path": "./models/domain_tokenizer/"
})

# Fine-tune an embedding model
Let fine_tuner = EmbeddingModelFineTuner.create({
    "base_model": "code-embedding-v1",
    "training_data": "./domain_code_samples/",
    "epochs": 5,
    "learning_rate": 1e-5
})

Let tuned_model = fine_tuner.train()
tuned_model.save("./models/tuned_embedding_model/")
```

### 3. Multi-language Support

Index and search across multiple programming languages:

```runa
# Create a multi-language indexer
Let multi_indexer = SemanticIndexer.create({
    "languages": ["runa", "python", "javascript", "rust"],
    "normalize_syntax": true,
    "cross_language_search": true
})

# Index a multilingual project
Let polyglot_index = multi_indexer.index_codebase("./project/", {
    "file_extensions": [".runa", ".py", ".js", ".rs"]
})

# Find similar code across languages
Let cross_lang_results = polyglot_index.search(
    "authentication middleware", 
    {"group_by_language": true}
)
```

### 4. Semantic Diff and Evolution Tracking

Track semantic changes in your codebase over time:

```runa
# Create a semantic evolution tracker
Let evo_tracker = CodeEvolutionTracker.create({
    "semantic_index": index,
    "git_repository": "./",
    "track_interval": "commit"  # Options: commit, tag, release
})

# Analyze semantic evolution
Let evolution = evo_tracker.analyze_evolution("src/core/", {
    "start_point": "v1.0.0",
    "end_point": "v2.0.0"
})

# Get semantic diff between versions
Let diff = evo_tracker.semantic_diff(
    "function_a", 
    {"from_version": "v1.0.0", "to_version": "v2.0.0"}
)

# Visualize code evolution
Let viz = evo_tracker.visualize_evolution("src/core/auth.runa")
viz.save("auth_evolution.svg")
```

## Integration with Knowledge Graph and LLM

### Enhancing Knowledge Graphs with Semantic Code Information

```runa
# Create a knowledge graph from semantic index
Let kg_builder = KnowledgeGraphBuilder.create({
    "semantic_index": index,
    "entity_types": ["function", "class", "module"],
    "relationship_types": ["calls", "inherits", "imports", "similar_to"]
})

Let code_kg = kg_builder.build_graph()

# Enrich knowledge graph with semantic information
code_kg.add_entity_property("semantic_vector", index.get_all_vectors())
code_kg.add_relationship_property("semantic_similarity", index.get_all_similarities())

# Query the knowledge graph with semantic context
Let query_results = code_kg.query_with_semantics(
    "error handling in network code",
    {"max_path_length": 3}
)
```

### Enhancing LLMs with Semantic Code Context

```runa
# Connect semantic index with LLM
Let semantic_llm = LLM.connect_with_context("runa_assistant_model", {
    "semantic_index": index,
    "retrieval_strategy": "hybrid",  # hybrid combines keyword and semantic search
    "max_context_items": 5
})

# Get code-aware completions
Let completion = semantic_llm.complete_with_context(
    "Write a function to validate user input",
    {"project_context": true}
)

# Generate code with semantic awareness
Let code_generation = semantic_llm.generate_code_with_context(
    "Create a cache system consistent with our codebase",
    {"retrieve_similar_patterns": true}
)
```

## Example: Building a Semantic Code Search System

```runa
Process called "create_code_search_system":
    # Initialize the components
    Let indexer = SemanticIndexer.create({
        "embedding_model": "code-embedding-v1",
        "chunk_size": "function"
    })
    
    Let doc_indexer = DocumentationIndexer.create({
        "embedding_model": "doc-embedding-v1",
        "chunk_size": "section"
    })
    
    # 1. Index code and documentation
    Print("Indexing codebase...")
    Let code_index = indexer.index_codebase("./src/")
    
    Print("Indexing documentation...")
    Let doc_index = doc_indexer.index_documentation("./docs/")
    
    # 2. Link code and documentation
    Print("Linking code and documentation...")
    Let linker = CodeDocLinker.create({
        "code_index": code_index,
        "doc_index": doc_index
    })
    
    Let linked_index = linker.link()
    
    # 3. Create a knowledge graph from the semantic index
    Print("Building knowledge graph...")
    Let kg_builder = KnowledgeGraphBuilder.create({
        "semantic_index": linked_index
    })
    
    Let knowledge_graph = kg_builder.build_graph()
    
    # 4. Create a search API
    Print("Creating search API...")
    Let search_api = CodeSearchAPI.create({
        "semantic_index": linked_index,
        "knowledge_graph": knowledge_graph
    })
    
    # 5. Define search function
    Process called "semantic_search" that takes query:String, options:Dict = {}:
        Let default_options = {
            "limit": 10,
            "min_score": 0.6,
            "include_code": true,
            "include_docs": true,
            "include_graph": true
        }
        
        # Merge default options with provided options
        Let search_options = default_options.merge(options)
        
        # Perform search
        Let results = search_api.search(query, search_options)
        
        # Format and return results
        Return {
            "query": query,
            "results_count": results.count,
            "top_results": results.top(5),
            "related_concepts": results.related_concepts,
            "suggested_queries": results.suggested_queries
        }
    
    # 6. Save components for future use
    Print("Saving system components...")
    linked_index.save("./semantic_system/linked_index")
    knowledge_graph.save("./semantic_system/knowledge_graph")
    
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