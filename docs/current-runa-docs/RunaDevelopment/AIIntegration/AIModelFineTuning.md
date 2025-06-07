# AI Model Fine-tuning in Runa

## Overview

Runa's AI Model Fine-tuning system provides a comprehensive framework for customizing and adapting pre-trained AI models to specific domains, tasks, or codebases. By fine-tuning models on domain-specific data, developers can significantly improve model performance for specialized use cases, while maintaining the generalization capabilities of the base models.

## Core Features

### 1. Model Preparation

Prepare pre-trained models for fine-tuning with Runa-specific adaptations:

```runa
# Load a pre-trained model for fine-tuning
Let model_loader = ModelLoader.create({
    "model_type": "llm",             # Options: llm, embedding, classifier
    "model_id": "runa-base-7b",      # Base model to fine-tune
    "device": "auto",                # Options: cpu, gpu, auto
    "quantization": "int8",          # Options: none, int8, int4
    "precision": "float16"           # Options: float32, float16, bfloat16
})

# Prepare model for fine-tuning
Let base_model = model_loader.load_for_fine_tuning({
    "adapter_type": "lora",          # Options: lora, qlora, prefix_tuning, full
    "trainable_components": ["attention", "mlp"],
    "freeze_embeddings": true,
    "rank": 8,                       # Only relevant for LoRA-based methods
    "alpha": 16                      # Scaling factor for LoRA
})

# Print model architecture summary
Print("Model architecture:")
Print(base_model.architecture_summary)

# Check GPU utilization and requirements
Let requirements = base_model.resource_requirements
Print("Memory required: " + requirements.memory + " GB")
Print("Recommended batch size: " + requirements.recommended_batch_size)
```

### 2. Dataset Configuration

Prepare and configure training data for model fine-tuning:

```runa
# Create a training dataset configurator
Let dataset_config = DatasetConfigurator.create({
    "format": "instruction",         # Options: instruction, completion, conversation, code
    "validation_split": 0.1,         # Percentage of data to use for validation
    "test_split": 0.05               # Percentage of data to use for testing
})

# Load training data from various sources
dataset_config.add_data_source("./training_data/code_examples/", {
    "format": "code",
    "recursive": true,
    "file_extensions": [".runa"]
})

dataset_config.add_data_source("./training_data/instructions.jsonl", {
    "format": "jsonl",
    "keys": {
        "input": "instruction",
        "output": "response"
    }
})

dataset_config.add_data_source("./training_data/conversations.json", {
    "format": "json",
    "keys": {
        "conversations": "messages",
        "user_key": "user",
        "assistant_key": "assistant"
    }
})

# Apply preprocessing steps
dataset_config.add_preprocessing_step("tokenize", {
    "tokenizer": base_model.tokenizer
})

dataset_config.add_preprocessing_step("filter_by_length", {
    "min_tokens": 10,
    "max_tokens": 2048
})

dataset_config.add_preprocessing_step("deduplicate", {
    "similarity_threshold": 0.9
})

# Generate final training datasets
Let datasets = dataset_config.prepare_datasets()
Print("Training examples: " + datasets.train.count)
Print("Validation examples: " + datasets.validation.count)
Print("Test examples: " + datasets.test.count)
```

### 3. Training Configuration

Set up the training parameters and hyperparameters:

```runa
# Create a training configurator
Let training_config = TrainingConfigurator.create({
    "training_objective": "supervised",  # Options: supervised, contrastive, reinforcement
    "optimization": {
        "optimizer": "adamw",
        "learning_rate": 2e-5,
        "weight_decay": 0.01,
        "lr_scheduler": "cosine",
        "warmup_steps": 100
    },
    "training_parameters": {
        "batch_size": 4,
        "gradient_accumulation_steps": 8,
        "epochs": 3,
        "max_steps": 1000,        # If specified, overrides epochs
        "early_stopping": {
            "patience": 3,
            "metric": "validation_loss",
            "min_delta": 0.01
        }
    },
    "mixed_precision": "fp16",    # Options: no, fp16, bf16
    "checkpointing": {
        "save_steps": 100,
        "keep_top_k": 3,
        "metric": "validation_loss"
    }
})

# Configure evaluation metrics
training_config.add_evaluation_metric("loss")
training_config.add_evaluation_metric("perplexity")
training_config.add_evaluation_metric("exact_match", {
    "normalize": true
})
training_config.add_evaluation_metric("code_evaluation", {
    "execution": true,
    "syntax_check": true
})

# Print training configuration summary
Print("Training configuration:")
Print(training_config.summary)
```

### 4. Model Fine-tuning Execution

Execute the fine-tuning process:

```runa
# Create a fine-tuning engine
Let fine_tuner = FineTuner.create({
    "model": base_model,
    "datasets": datasets,
    "training_config": training_config,
    "log_level": "info",        # Options: debug, info, warning, error
    "log_to": ["console", "./logs/fine_tuning.log"]
})

# Run the fine-tuning process
Print("Starting fine-tuning...")
Let fine_tuning_result = fine_tuner.train({
    "save_final_model": true,
    "output_dir": "./models/fine_tuned_runa_model/",
    "save_format": "auto"      # Options: auto, safetensors, pytorch
})

# Print training results
Print("Fine-tuning completed!")
Print("Final training loss: " + fine_tuning_result.metrics.final_training_loss)
Print("Final validation loss: " + fine_tuning_result.metrics.final_validation_loss)
Print("Training time: " + fine_tuning_result.training_time + " minutes")
Print("Peak memory usage: " + fine_tuning_result.peak_memory_usage + " GB")
```

### 5. Model Evaluation

Evaluate the fine-tuned model on test datasets:

```runa
# Create a model evaluator
Let evaluator = ModelEvaluator.create({
    "model": fine_tuning_result.model,
    "datasets": {
        "test": datasets.test,
        "custom": "./evaluation_data/custom_test_cases.jsonl"
    },
    "metrics": ["loss", "perplexity", "exact_match", "code_execution_success"]
})

# Run evaluation
Print("Evaluating fine-tuned model...")
Let evaluation_results = evaluator.evaluate()

# Print evaluation results
Print("Evaluation results:")
For dataset_name in evaluation_results.keys():
    Print("Dataset: " + dataset_name)
    Let dataset_results = evaluation_results[dataset_name]
    For metric_name in dataset_results.keys():
        Print("- " + metric_name + ": " + dataset_results[metric_name])

# Generate confusion matrix for classification tasks
If evaluation_results.contains("classification_metrics"):
    Let confusion = evaluator.generate_confusion_matrix()
    Print("Confusion matrix:")
    Print(confusion)
```

### 6. Model Export and Deployment

Export and prepare the fine-tuned model for deployment:

```runa
# Create a model exporter
Let exporter = ModelExporter.create({
    "model": fine_tuning_result.model,
    "output_format": "onnx",      # Options: onnx, pytorch, safetensors, runa_optimized
    "optimization_level": "o2",   # Options: o0 (none), o1, o2, o3 (aggressive)
    "quantization": "int8",       # Options: none, int8, int4, float16
    "metadata": {
        "name": "Runa-Specialized-7B",
        "version": "1.0.0",
        "description": "Fine-tuned Runa model for code generation",
        "author": "Runa Team",
        "license": "MIT"
    }
})

# Export the model
Print("Exporting model...")
Let export_result = exporter.export("./models/exported/runa_specialized/")

# Create a deployment package
Let deployment = exporter.create_deployment_package({
    "target": "api",           # Options: api, standalone, library, web
    "include_tokenizer": true,
    "include_sample_code": true,
    "compression": "zip"       # Options: none, zip, tar.gz
})

Print("Model exported successfully!")
Print("Exported model size: " + export_result.size + " MB")
Print("Deployment package created at: " + deployment.path)
```

## Advanced Features

### 1. Reinforcement Learning from Human Feedback (RLHF)

Fine-tune models based on human preferences and feedback:

```runa
# Create a RLHF configurator
Let rlhf_config = RLHFConfigurator.create({
    "supervised_model": fine_tuning_result.model,  # Already fine-tuned model
    "reward_model_type": "auto_create",            # Options: auto_create, existing
    "rl_algorithm": "ppo",                         # Options: ppo, dpo, kto
    "training_parameters": {
        "kl_penalty": 0.1,                         # KL divergence penalty coefficient
        "reward_scale": 0.1,                       # Reward scaling factor
        "ppo_epochs": 4,                           # Number of PPO epochs per batch
        "max_steps": 2000                          # Total PPO optimization steps
    }
})

# Add comparison data for training the reward model
rlhf_config.add_comparison_data("./feedback_data/comparisons.jsonl", {
    "format": "jsonl",
    "keys": {
        "prompt": "instruction",
        "better": "preferred_response",
        "worse": "rejected_response"
    }
})

# Create an RLHF trainer
Let rlhf_trainer = RLHFTrainer.create({
    "config": rlhf_config,
    "log_level": "info",
    "output_dir": "./models/rlhf_tuned/"
})

# Run RLHF training
Print("Starting RLHF training...")
Let rlhf_result = rlhf_trainer.train()

# Evaluate the RLHF-tuned model
Let rlhf_eval = ModelEvaluator.create({
    "model": rlhf_result.model,
    "datasets": datasets.test,
    "metrics": ["win_rate_vs_supervised", "human_eval"]
})

Let rlhf_eval_results = rlhf_eval.evaluate()
Print("RLHF model win rate vs supervised: " + rlhf_eval_results.win_rate_vs_supervised)
```

### 2. Domain Adaptation

Adapt models to specific programming domains or styles:

```runa
# Create a domain adaptation configurator
Let domain_config = DomainAdaptationConfigurator.create({
    "base_model": base_model,
    "domain": "systems_programming",    # Target domain
    "adaptation_method": "continued_pretraining",  # Options: continued_pretraining, domain_expert_tuning
    "training_parameters": {
        "learning_rate": 5e-6,
        "epochs": 1,
        "batch_size": 2
    }
})

# Add domain-specific data
domain_config.add_domain_data("./domain_data/systems_code/", {
    "recursive": true,
    "file_extensions": [".runa", ".c", ".rs"]
})

domain_config.add_domain_data("./domain_data/systems_docs.jsonl", {
    "format": "jsonl",
    "weight": 0.3  # Weight relative to code data
})

# Create a domain adaptation trainer
Let domain_adapter = DomainAdapter.create({
    "config": domain_config,
    "output_dir": "./models/domain_adapted/"
})

# Run domain adaptation
Print("Starting domain adaptation...")
Let domain_result = domain_adapter.adapt()

Print("Domain adaptation completed!")
Print("Perplexity on domain data before: " + domain_result.metrics.initial_domain_perplexity)
Print("Perplexity on domain data after: " + domain_result.metrics.final_domain_perplexity)
```

### 3. Model Merging and Ensembling

Combine multiple fine-tuned models to create more capable models:

```runa
# Load multiple fine-tuned models
Let model_loader = ModelLoader.create()

Let models = {
    "code_generation": model_loader.load("./models/code_gen_model/"),
    "documentation": model_loader.load("./models/documentation_model/"),
    "debugging": model_loader.load("./models/debugging_model/")
}

# Create a model merger
Let merger = ModelMerger.create({
    "base_model": "runa-base-7b",
    "merge_method": "slerp",      # Options: average, slerp, ties, task_arithmetic
    "merge_parameters": {
        "interpolation_weights": {
            "code_generation": 0.4,
            "documentation": 0.3,
            "debugging": 0.3
        },
        "merge_strategy": "layer_wise"  # Options: layer_wise, module_wise, task_wise
    }
})

# Add models to merge
For model_name in models.keys():
    merger.add_model(model_name, models[model_name])

# Execute the merge
Print("Merging models...")
Let merged_model = merger.merge()

# Evaluate the merged model
Let merged_eval = ModelEvaluator.create({
    "model": merged_model,
    "datasets": {
        "code_gen": "./evaluation_data/code_gen_tests.jsonl",
        "documentation": "./evaluation_data/documentation_tests.jsonl",
        "debugging": "./evaluation_data/debugging_tests.jsonl"
    }
})

Let merged_results = merged_eval.evaluate()
Print("Merged model performance:")
For dataset in merged_results.keys():
    Print(dataset + " score: " + merged_results[dataset].overall_score)
```

### 4. Quantization and Optimization

Optimize models for deployment with various quantization techniques:

```runa
# Create a model optimizer
Let optimizer = ModelOptimizer.create({
    "model": fine_tuning_result.model,
    "optimization_targets": ["size", "latency"],  # Options: size, latency, throughput
    "target_hardware": "cpu"                     # Options: cpu, gpu, mobile, edge
})

# Analyze optimization potential
Let analysis = optimizer.analyze_optimization_potential()
Print("Optimization analysis:")
Print("Estimated size reduction: " + analysis.size_reduction_potential + "%")
Print("Estimated latency improvement: " + analysis.latency_improvement_potential + "%")
Print("Recommended quantization: " + analysis.recommended_quantization)

# Apply quantization
Let quantized_model = optimizer.quantize({
    "method": analysis.recommended_quantization,
    "calibration_dataset": datasets.validation.sample(100)
})

# Benchmark the optimized model
Let benchmark = optimizer.benchmark(quantized_model, {
    "test_inputs": datasets.test.sample(10),
    "iterations": 100,
    "warmup_iterations": 10
})

Print("Optimization results:")
Print("Original model size: " + benchmark.original_size + " MB")
Print("Optimized model size: " + benchmark.optimized_size + " MB")
Print("Size reduction: " + benchmark.size_reduction + "%")
Print("Average latency improvement: " + benchmark.latency_improvement + "%")
Print("Max accuracy loss: " + benchmark.accuracy_loss + "%")
```

## Example: Complete Fine-tuning Pipeline

```runa
Process called "fine_tune_runa_assistant":
    # Step 1: Prepare data sources
    Print("Preparing data sources...")
    
    # Initialize data sources
    Let data_sources = DataSourceManager.create()
    
    # Add code examples
    data_sources.add_code_repository("./src/", {
        "file_extensions": [".runa"],
        "exclude_patterns": ["**/test/**", "**/examples/**"],
        "code_extraction": "function",  # Extract individual functions
        "include_comments": true,
        "min_tokens": 20,
        "max_tokens": 1024
    })
    
    # Add documentation
    data_sources.add_documentation("./docs/", {
        "file_extensions": [".md"],
        "chunk_size": "section",
        "min_tokens": 30,
        "max_tokens": 1024
    })
    
    # Add manual examples and human feedback
    data_sources.add_instruction_data("./training_data/instructions.jsonl")
    data_sources.add_conversation_data("./training_data/conversations.jsonl")
    data_sources.add_preference_data("./training_data/preferences.jsonl")
    
    # Step 2: Process and prepare training data
    Print("Processing training data...")
    Let training_data_processor = TrainingDataProcessor.create({
        "data_sources": data_sources,
        "output_format": "instruction",
        "deduplicate": true,
        "validation_split": 0.1,
        "test_split": 0.05
    })
    
    # Process and prepare the data
    Let processed_data = training_data_processor.process()
    
    Print("Training examples: " + processed_data.train.count)
    Print("Validation examples: " + processed_data.validation.count)
    Print("Test examples: " + processed_data.test.count)
    
    # Step 3: Prepare the base model
    Print("Loading base model...")
    Let model_loader = ModelLoader.create({
        "model_type": "llm",
        "model_id": "runa-base-7b"
    })
    
    Let base_model = model_loader.load_for_fine_tuning({
        "adapter_type": "lora",
        "trainable_components": ["attention", "mlp"],
        "freeze_embeddings": true
    })
    
    # Step 4: Configure training parameters
    Print("Configuring training parameters...")
    Let training_config = TrainingConfigurator.create({
        "training_objective": "supervised",
        "optimization": {
            "optimizer": "adamw",
            "learning_rate": 2e-5,
            "weight_decay": 0.01,
            "lr_scheduler": "cosine",
            "warmup_steps": 100
        },
        "training_parameters": {
            "batch_size": 4,
            "gradient_accumulation_steps": 8,
            "epochs": 3,
            "mixed_precision": "fp16"
        },
        "evaluation_metrics": ["loss", "perplexity", "exact_match"]
    })
    
    # Step 5: Initial supervised fine-tuning
    Print("Starting supervised fine-tuning...")
    Let fine_tuner = FineTuner.create({
        "model": base_model,
        "datasets": processed_data,
        "training_config": training_config,
        "output_dir": "./models/supervised_stage/"
    })
    
    Let supervised_result = fine_tuner.train()
    
    Print("Supervised fine-tuning completed!")
    Print("Final validation loss: " + supervised_result.metrics.final_validation_loss)
    
    # Step 6: RLHF fine-tuning
    Print("Starting RLHF fine-tuning...")
    Let rlhf_config = RLHFConfigurator.create({
        "supervised_model": supervised_result.model,
        "reward_model_type": "auto_create",
        "rl_algorithm": "ppo",
        "comparison_data": processed_data.preferences
    })
    
    Let rlhf_trainer = RLHFTrainer.create({
        "config": rlhf_config,
        "output_dir": "./models/rlhf_stage/"
    })
    
    Let rlhf_result = rlhf_trainer.train()
    
    Print("RLHF fine-tuning completed!")
    
    # Step 7: Quantize and export the model
    Print("Optimizing and exporting the model...")
    Let exporter = ModelExporter.create({
        "model": rlhf_result.model,
        "output_format": "onnx",
        "quantization": "int8",
        "optimization_level": "o2"
    })
    
    Let export_result = exporter.export("./models/final_runa_assistant/")
    
    # Step 8: Final evaluation
    Print("Running final evaluation...")
    Let evaluator = ModelEvaluator.create({
        "models": {
            "base": base_model,
            "supervised": supervised_result.model,
            "rlhf": rlhf_result.model
        },
        "datasets": {
            "test": processed_data.test,
            "held_out": "./evaluation_data/held_out_test.jsonl"
        },
        "metrics": ["win_rate", "exact_match", "code_execution_success"]
    })
    
    Let final_results = evaluator.evaluate_all()
    
    # Print final results
    Print("Final evaluation results:")
    For model_name in final_results.keys():
        Print("Model: " + model_name)
        Let model_results = final_results[model_name]
        For dataset_name in model_results.keys():
            Print("- Dataset: " + dataset_name)
            Let dataset_results = model_results[dataset_name]
            For metric_name in dataset_results.keys():
                Print("  - " + metric_name + ": " + dataset_results[metric_name])
    
    # Return final model and evaluation results
    Return {
        "final_model_path": export_result.path,
        "evaluation_results": final_results,
        "training_metrics": {
            "supervised": supervised_result.metrics,
            "rlhf": rlhf_result.metrics
        }
    }
```

## Best Practices for Model Fine-tuning

1. **Data Quality Over Quantity**: Focus on high-quality, diverse, and representative data rather than sheer volume.

2. **Start Small**: Begin with smaller models and datasets to iterate quickly before scaling up to larger models.

3. **Incremental Approach**: Use a multi-stage fine-tuning process (supervised fine-tuning followed by RLHF) for best results.

4. **Continuous Evaluation**: Regularly evaluate models during training on diverse test sets to catch overfitting or other issues early.

5. **Domain-Specific Adaptations**: For specialized applications, consider domain adaptation techniques before task-specific fine-tuning.

6. **Quantization Validation**: Always validate quantized models thoroughly to ensure accuracy hasn't degraded unacceptably.

7. **Version Control**: Maintain careful version control of both training data and model checkpoints to ensure reproducibility.

## References

- [Runa Model Fine-tuning API Reference](https://runa-lang.org/docs/api/model-fine-tuning)
- [Fine-tuning Best Practices Guide](https://runa-lang.org/docs/guides/model-fine-tuning)
- [RLHF Implementation Details](https://runa-lang.org/docs/guides/reinforcement-learning)

For complete examples, see the [Model Fine-tuning Examples](../../src/tests/examples/model_fine_tuning_examples.runa) in the Runa codebase. 