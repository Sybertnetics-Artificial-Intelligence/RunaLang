# Training Data Generation in Runa

## Overview

Runa provides a comprehensive system for generating high-quality training data for machine learning models, particularly those focused on code understanding, generation, and enhancement. This capability enables developers to create custom AI models tailored to Runa programming patterns and domain-specific requirements.

## Core Features

### 1. Code Corpus Generation

Easily generate diverse code examples for model training:

```
# Create a code corpus generator
Let generator be CodeCorpusGenerator.create with dictionary with:
    "output_directory" as "./training_data/"
    "file_format" as "jsonl"
    "include_metadata" as true

# Generate corpus from existing codebase
Let corpus be generator.from_codebase with "./src/" and dictionary with:
    "file_extensions" as list containing ".runa"
    "exclude_patterns" as list containing "**/test/**", "**/example/**"
    "sample_count" as 10000

# Generate synthetic examples
Let synthetic_corpus be generator.generate_synthetic with dictionary with:
    "pattern_templates" as list containing "function_calls", "conditional_logic", "loops"
    "count" as 5000
    "diversity_level" as 0.8

# Combine corpora
Let combined_corpus be generator.combine with list containing corpus, synthetic_corpus
```

### 2. Fine-tuning Dataset Preparation

Create datasets specifically designed for fine-tuning language models:

```
# Create a fine-tuning dataset generator
Let ft_generator be FineTuningDataGenerator.create

# Generate instruction-following examples
Let instruct_dataset be ft_generator.create_instruction_dataset with dictionary with:
    "code_corpus" as corpus
    "instruction_templates" as list containing:
        "Write a function that {{task}}"
        "Create a process that {{task}} with {{parameters}}"
        "How would you implement {{feature}} in Runa?"
    "count" as 2000

# Generate code completion examples
Let completion_dataset be ft_generator.create_completion_dataset with dictionary with:
    "code_corpus" as corpus
    "context_length" as 200
    "completion_length" as 50
    "count" as 5000

# Export in model-specific format
Call ft_generator.export with dictionary with:
    "format" as "jsonl"
    "output_file" as "runa_finetune_data.jsonl"
    "include_datasets" as list containing instruct_dataset, completion_dataset
```

### 3. Data Augmentation and Transformation

Enhance and transform training data to improve model performance:

```
# Create a data augmenter
Let augmenter be DataAugmenter.create

# Apply various augmentation techniques
Let augmented_data be augmenter.transform with corpus and list containing:
    dictionary with "type" as "variable_renaming" and "probability" as 0.5
    dictionary with "type" as "comment_variation" and "probability" as 0.3
    dictionary with "type" as "code_restructuring" and "probability" as 0.2
    dictionary with "type" as "style_variation" and "probability" as 0.4

# Generate edge cases
Let edge_cases be augmenter.generate_edge_cases with corpus and dictionary with:
    "error_patterns" as true
    "boundary_conditions" as true
    "unusual_inputs" as true
    "count" as 1000
```

### 4. Quality Assessment and Filtering

Ensure high-quality training data through automated assessment:

```
# Create a quality assessor
Let assessor be DataQualityAssessor.create

# Assess dataset quality
Let quality_report be assessor.evaluate with combined_corpus and dictionary with:
    "metrics" as list containing "diversity", "correctness", "completeness", "uniqueness"
    "syntax_check" as true
    "lint_level" as "moderate"

# Filter low-quality examples
Let filtered_corpus be assessor.filter with combined_corpus and dictionary with:
    "min_quality_score" as 0.7
    "exclude_duplicates" as true
    "exclude_syntax_errors" as true

# Print quality report
Display quality_report.summary
```

### 5. Dataset Splitting and Validation

Create appropriate splits for training, testing, and validation:

```
# Create a dataset splitter
Let splitter be DatasetSplitter.create

# Split dataset
Let splits be splitter.split with filtered_corpus and dictionary with:
    "train" as 0.8
    "validation" as 0.1
    "test" as 0.1
    "stratify_by" as "complexity"

# Validate the distribution of features across splits
Let distribution_report be splitter.validate_distribution with splits and list containing:
    "pattern_types", "complexity", "token_count"

# Export splits
Call splitter.export_splits with splits and "./dataset_splits/"
```

## Advanced Features

### 1. Domain-Specific Data Generation

Generate data for specific domains or applications:

```
# Create a domain-specific generator
Let domain_generator be DomainDataGenerator.create with "financial_analysis"

# Load domain-specific templates and patterns
Call domain_generator.load_templates with "./financial_templates/"

# Generate domain-specific examples
Let financial_examples be domain_generator.generate with dictionary with:
    "count" as 1000
    "include_domain_entities" as true
    "complexity_range" as list containing 1, 5
```

### 2. Parallel and Incremental Generation

Efficiently generate and manage large datasets:

```
# Create a parallel generator
Let parallel_generator be ParallelDataGenerator.create with dictionary with:
    "worker_count" as 8
    "batch_size" as 100

# Generate data in parallel
Let large_corpus be parallel_generator.generate with 1000000 and dictionary with:
    "template_directory" as "./templates/"
    "output_format" as "parquet"
    "incremental" as true
    "checkpoint_interval" as 10000
```

### 3. Training Data Versioning

Track and manage different versions of training data:

```
# Create a data versioner
Let versioner be DataVersioner.create with "./data_repository/"

# Version a dataset
Let version_id be versioner.commit with filtered_corpus and dictionary with:
    "version_name" as "v1.2.0"
    "description" as "Enhanced with financial domain examples"
    "metadata" as dictionary with:
        "source" as "mixed"
        "example_count" as filtered_corpus.count
        "generation_date" as Date.now()
```

## Example: Creating a Comprehensive Training Pipeline

```
Process called "create_training_data_pipeline":
    # Initialize components
    Let generator be CodeCorpusGenerator.create with dictionary with:
        "output_directory" as "./training_data/"
    Let augmenter be DataAugmenter.create
    Let assessor be DataQualityAssessor.create
    Let splitter be DatasetSplitter.create
    Let versioner be DataVersioner.create with "./data_repository/"
    
    # Step 1: Generate base corpus
    Display "Generating base corpus..."
    Let base_corpus be generator.from_codebase with "./src/" and dictionary with:
        "file_extensions" as list containing ".runa"
        "exclude_patterns" as list containing "**/test/**"
    
    # Step 2: Generate synthetic examples
    Display "Generating synthetic examples..."
    Let synthetic_corpus be generator.generate_synthetic with dictionary with:
        "pattern_templates" as list containing "function_calls", "conditionals", "loops", "error_handling"
        "count" as 10000
    
    # Step 3: Combine and augment
    Display "Augmenting data..."
    Let combined_corpus be generator.combine with list containing base_corpus, synthetic_corpus
    Let augmented_corpus be augmenter.transform with combined_corpus and list containing:
        dictionary with "type" as "variable_renaming" and "probability" as 0.4
        dictionary with "type" as "comment_variation" and "probability" as 0.3
        dictionary with "type" as "code_restructuring" and "probability" as 0.2
    
    # Step 4: Quality assessment and filtering
    Display "Assessing quality..."
    Let quality_report be assessor.evaluate with augmented_corpus
    Let filtered_corpus be assessor.filter with augmented_corpus and dictionary with:
        "min_quality_score" as 0.7
        "exclude_duplicates" as true
    
    # Step 5: Create dataset splits
    Display "Creating splits..."
    Let splits be splitter.split with filtered_corpus and dictionary with:
        "train" as 0.8
        "validation" as 0.1
        "test" as 0.1
        "stratify_by" as "complexity"
    
    # Step 6: Version and export the dataset
    Display "Versioning dataset..."
    Let version_id be versioner.commit with splits and dictionary with:
        "version_name" as "runa_code_corpus_v1"
        "description" as "Initial Runa code corpus for model training"
    
    # Step 7: Export in appropriate formats
    Display "Exporting datasets..."
    For each split_name in list containing "train", "validation", "test":
        Let output_file be "./final_dataset/" followed by split_name followed by ".jsonl"
        Call splits[split_name].export with output_file and "jsonl"
    
    Display "Training data generation pipeline completed!"
    Display "Version ID:" with message version_id
    Return splits
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