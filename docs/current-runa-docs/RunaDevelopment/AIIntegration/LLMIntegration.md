# LLM Integration in Runa

## Overview

Runa provides robust integration with Large Language Models (LLMs), enabling developers to leverage the power of AI within their applications. This integration allows for code generation, natural language processing, and intelligent assistance directly within the Runa programming environment.

## Core Features

### 1. LLM Connection and Basic Interaction

Runa's `runa.ai.llm` module provides straightforward API for connecting to and interacting with language models:

```
Let model be LLM.connect with "model_name"
Let response be model.complete with "Your prompt here"
```

The LLM integration supports various model providers and can be configured for both local and cloud-based models.

### 2. Advanced Prompting Techniques

#### Prompt Templates

Create reusable prompt templates with variable placeholders:

```
Let template be PromptTemplate.create with:
    "Generate a {{language}} function that {{task}} with these requirements: {{requirements}}"

Let prompt be template.fill with dictionary with:
    "language" as "Runa"
    "task" as "sorts a list"
    "requirements" as "Must handle empty lists"
```

#### Few-Shot Learning

Improve model performance by providing examples:

```
Let examples be list containing:
    dictionary with "input" as "Sort [3, 1, 5, 2]" and "output" as "[1, 2, 3, 5]"
    dictionary with "input" as "Find max: [7, 2, 9, 4]" and "output" as "9"

Let few shot prompt be FewShotPrompt.create with:
    examples as examples
    prefix as "Solve this problem:"
    suffix as "{{input}}"
```

#### Chain-of-Thought Reasoning

Guide models through complex reasoning tasks:

```
Let response be model.complete with cot with "Your complex problem here"
Display response.reasoning  # See the step-by-step reasoning
Display response.answer     # Get the final answer
```

### 3. Code Generation and Execution

Runa provides specialized methods for code generation and safe execution:

```
# Generate code
Let code be model.complete as code with "Write a function to calculate factorial"

# Safely execute generated code
Let result be LLM.execute safely with code as code and dictionary with "n" as 5
```

The `CodeGenerator` class offers additional capabilities:

```
Let generator be CodeGenerator.create
Let generated code be generator.generate with "Description of desired code"
Let validation result be generator.validate with generated code
```

### 4. Model Evaluation

Evaluate and compare LLM performance using Runa's built-in tools:

```
Let evaluator be ModelEvaluator.create
Let test data be Dataset.load with "benchmark_dataset"
Let evaluation results be evaluator.evaluate with model as model and test data as test data
```

## Configuration

### Model Settings

Configure LLM behavior with custom settings:

```
Let model be LLM.connect with "model_name" and dictionary with:
    "temperature" as 0.7
    "max_tokens" as 1000
    "top_p" as 0.95
    "frequency_penalty" as 0.5
    "presence_penalty" as 0.5
```

### Provider Configuration

Set up connections to different LLM providers:

```
# Configure a provider
LLM.configure provider with "provider_name" and dictionary with:
    "api_key" as "your_api_key"
    "base_url" as "https://api.provider.com/v1"
    "default_model" as "provider-model-name"

# Then connect using that provider
Let model be LLM.connect with provider as "provider_name"
```

## Best Practices

1. **Prompt Engineering**: Craft clear, specific prompts for better results
2. **Model Selection**: Choose appropriate models for different tasks (code generation vs. text completion)
3. **Error Handling**: Always implement proper error handling when working with LLMs
4. **Content Safety**: Use content filtering options when generating user-facing content
5. **Performance Optimization**: Cache common responses for frequently used prompts

## Example: Building an LLM-powered Assistant

```
Process called "create_assistant":
    # Initialize assistant with specific capabilities
    Let assistant be Assistant.create with dictionary with:
        "name" as "RunaHelper"
        "description" as "Coding assistant for Runa developers"
        "capabilities" as list containing "code_generation", "documentation", "debugging"
    
    # Connect to preferred LLM
    Let model be LLM.connect with "runa_assistant_model"
    Call assistant.set_model with model
    
    # Configure assistant behavior
    Call assistant.configure with dictionary with:
        "code_style" as "idiomatic_runa"
        "verbosity" as "medium"
        "include_explanations" as true
    
    # Start interactive session
    Let session be assistant.start_session
    
    Return assistant
```

## References

- [Runa AI Module API Reference](https://runa-lang.org/docs/api/ai)
- [Prompt Engineering Guide](https://runa-lang.org/docs/guides/prompt-engineering)
- [LLM Model Compatibility List](https://runa-lang.org/docs/llm/compatibility)

For complete examples, see the [LLM Integration Examples](../../src/tests/examples/llm_integration_examples.runa) in the Runa codebase. 