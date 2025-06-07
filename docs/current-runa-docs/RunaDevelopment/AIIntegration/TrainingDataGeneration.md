# Training Data Generation in Runa

## Overview

Runa provides a comprehensive system for generating high-quality training data for machine learning models, particularly those focused on code understanding, generation, and enhancement. This capability enables developers to create custom AI models tailored to Runa programming patterns and domain-specific requirements.

## Core Features

### 1. Code Corpus Generation

Easily generate diverse code examples for model training:

```runa
# Create a code corpus generator
Let generator = CodeCorpusGenerator.create({
    "output_directory": "./training_data/",
    "file_format": "jsonl",
    "include_metadata": true
})

# Generate corpus from existing codebase
Let corpus = generator.from_codebase("./src/", {
    "file_extensions": [".runa"],
    "exclude_patterns": ["**/test/**", "**/example/**"],
    "sample_count": 10000
})

# Generate synthetic examples
Let synthetic_corpus = generator.generate_synthetic({
    "pattern_templates": ["function_calls", "conditional_logic", "loops"],
    "count": 5000,
    "diversity_level": 0.8
})

# Combine corpora
Let combined_corpus = generator.combine([corpus, synthetic_corpus])
```

### 2. Fine-tuning Dataset Preparation

Create datasets specifically designed for fine-tuning language models:

```runa
# Create a fine-tuning dataset generator
Let ft_generator = FineTuningDataGenerator.create()

# Generate instruction-following examples
Let instruct_dataset = ft_generator.create_instruction_dataset({
    "code_corpus": corpus,
    "instruction_templates": [
        "Write a function that {{task}}",
        "Create a process that {{task}} with {{parameters}}",
        "How would you implement {{feature}} in Runa?"
    ],
    "count": 2000
})

# Generate code completion examples
Let completion_dataset = ft_generator.create_completion_dataset({
    "code_corpus": corpus,
    "context_length": 200,
    "completion_length": 50,
    "count": 5000
})

# Export in model-specific format
ft_generator.export({
    "format": "jsonl",
    "output_file": "runa_finetune_data.jsonl",
    "include_datasets": [instruct_dataset, completion_dataset]
})
```

### 3. Data Augmentation and Transformation

Enhance and transform training data to improve model performance:

```runa
# Create a data augmenter
Let augmenter = DataAugmenter.create()

# Apply various augmentation techniques
Let augmented_data = augmenter.transform(corpus, [
    {"type": "variable_renaming", "probability": 0.5},
    {"type": "comment_variation", "probability": 0.3},
    {"type": "code_restructuring", "probability": 0.2},
    {"type": "style_variation", "probability": 0.4}
])

# Generate edge cases
Let edge_cases = augmenter.generate_edge_cases(corpus, {
    "error_patterns": true,
    "boundary_conditions": true,
    "unusual_inputs": true,
    "count": 1000
})
```

### 4. Quality Assessment and Filtering

Ensure high-quality training data through automated assessment:

```runa
# Create a quality assessor
Let assessor = DataQualityAssessor.create()

# Assess dataset quality
Let quality_report = assessor.evaluate(combined_corpus, {
    "metrics": ["diversity", "correctness", "completeness", "uniqueness"],
    "syntax_check": true,
    "lint_level": "moderate"
})

# Filter low-quality examples
Let filtered_corpus = assessor.filter(combined_corpus, {
    "min_quality_score": 0.7,
    "exclude_duplicates": true,
    "exclude_syntax_errors": true
})

# Print quality report
Print(quality_report.summary)
```

### 5. Dataset Splitting and Validation

Create appropriate splits for training, testing, and validation:

```runa
# Create a dataset splitter
Let splitter = DatasetSplitter.create()

# Split dataset
Let splits = splitter.split(filtered_corpus, {
    "train": 0.8,
    "validation": 0.1,
    "test": 0.1,
    "stratify_by": "complexity"
})

# Validate the distribution of features across splits
Let distribution_report = splitter.validate_distribution(splits, [
    "pattern_types", "complexity", "token_count"
])

# Export splits
splitter.export_splits(splits, "./dataset_splits/")
```

## Advanced Features

### 1. Domain-Specific Data Generation

Generate data for specific domains or applications:

```runa
# Create a domain-specific generator
Let domain_generator = DomainDataGenerator.create("financial_analysis")

# Load domain-specific templates and patterns
domain_generator.load_templates("./financial_templates/")

# Generate domain-specific examples
Let financial_examples = domain_generator.generate({
    "count": 1000,
    "include_domain_entities": true,
    "complexity_range": [1, 5]
})
```

### 2. Parallel and Incremental Generation

Efficiently generate and manage large datasets:

```runa
# Create a parallel generator
Let parallel_generator = ParallelDataGenerator.create({
    "worker_count": 8,
    "batch_size": 100
})

# Generate data in parallel
Let large_corpus = parallel_generator.generate(1000000, {
    "template_directory": "./templates/",
    "output_format": "parquet",
    "incremental": true,
    "checkpoint_interval": 10000
})
```

### 3. Training Data Versioning

Track and manage different versions of training data:

```runa
# Create a data versioner
Let versioner = DataVersioner.create("./data_repository/")

# Version a dataset
Let version_id = versioner.commit(filtered_corpus, {
    "version_name": "v1.2.0",
    "description": "Enhanced with financial domain examples",
    "metadata": {
        "source": "mixed",
        "example_count": filtered_corpus.count,
        "generation_date": Date.now()
    }
})

# List available versions
Let versions = versioner.list_versions()

# Load a specific version
Let previous_version = versioner.load("v1.1.0")
```

## Example: Creating a Comprehensive Training Pipeline

```runa
Process called "create_training_data_pipeline":
    # Initialize components
    Let generator = CodeCorpusGenerator.create({"output_directory": "./training_data/"})
    Let augmenter = DataAugmenter.create()
    Let assessor = DataQualityAssessor.create()
    Let splitter = DatasetSplitter.create()
    Let versioner = DataVersioner.create("./data_repository/")
    
    # Step 1: Generate base corpus
    Print("Generating base corpus...")
    Let base_corpus = generator.from_codebase("./src/", {
        "file_extensions": [".runa"],
        "exclude_patterns": ["**/test/**"]
    })
    
    # Step 2: Generate synthetic examples
    Print("Generating synthetic examples...")
    Let synthetic_corpus = generator.generate_synthetic({
        "pattern_templates": ["function_calls", "conditionals", "loops", "error_handling"],
        "count": 10000
    })
    
    # Step 3: Combine and augment
    Print("Augmenting data...")
    Let combined_corpus = generator.combine([base_corpus, synthetic_corpus])
    Let augmented_corpus = augmenter.transform(combined_corpus, [
        {"type": "variable_renaming", "probability": 0.4},
        {"type": "comment_variation", "probability": 0.3},
        {"type": "code_restructuring", "probability": 0.2}
    ])
    
    # Step 4: Quality assessment and filtering
    Print("Assessing quality...")
    Let quality_report = assessor.evaluate(augmented_corpus)
    Let filtered_corpus = assessor.filter(augmented_corpus, {
        "min_quality_score": 0.7,
        "exclude_duplicates": true
    })
    
    # Step 5: Create dataset splits
    Print("Creating splits...")
    Let splits = splitter.split(filtered_corpus, {
        "train": 0.8,
        "validation": 0.1,
        "test": 0.1
    })
    
    # Step 6: Version and export the dataset
    Print("Versioning dataset...")
    Let version_id = versioner.commit(splits, {
        "version_name": "runa_code_corpus_v1",
        "description": "Initial Runa code corpus for model training"
    })
    
    # Step 7: Export in appropriate formats
    Print("Exporting datasets...")
    For split_name in ["train", "validation", "test"]:
        Let output_file = "./final_dataset/" + split_name + ".jsonl"
        splits[split_name].export(output_file, "jsonl")
    
    Return {
        "version_id": version_id,
        "stats": {
            "total_examples": filtered_corpus.count,
            "train_examples": splits["train"].count,
            "validation_examples": splits["validation"].count,
            "test_examples": splits["test"].count,
            "quality_score": quality_report.overall_score
        }
    }
```

## Best Practices for Training Data Generation

1. **Balance Quality and Quantity**: Focus on generating high-quality examples rather than just maximizing quantity.

2. **Ensure Diversity**: Include a wide range of code patterns, styles, and use cases in your training data.

3. **Incorporate Real-World Examples**: Mix synthetic examples with real code from production systems when possible.

4. **Regular Updates**: Periodically refresh training data to include new patterns and practices.

5. **Version Control**: Maintain strict versioning of training datasets to ensure reproducibility of model training.

6. **Data Privacy**: When generating from existing codebases, ensure sensitive information is removed or anonymized.

## References

- [Runa Training Data Generation API Reference](https://runa-lang.org/docs/api/training-data)
- [Model Training Guide](https://runa-lang.org/docs/guides/model-training)
- [Data Augmentation Techniques](https://runa-lang.org/docs/guides/data-augmentation)

For complete examples, see the [Training Data Generation Examples](../../src/tests/examples/training_data_examples.runa) in the Runa codebase. 