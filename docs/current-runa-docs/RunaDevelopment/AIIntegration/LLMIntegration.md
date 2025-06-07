# LLM Integration in Runa

## Overview

Runa provides robust integration with Large Language Models (LLMs), enabling developers to leverage the power of AI within their applications. This integration allows for code generation, natural language processing, and intelligent assistance directly within the Runa programming environment.

## Core Features

### 1. LLM Connection and Basic Interaction

Runa's `runa.ai.llm` module provides straightforward API for connecting to and interacting with language models:

```runa
Let model = LLM.connect("model_name")
Let response = model.complete("Your prompt here")
```

The LLM integration supports various model providers and can be configured for both local and cloud-based models.

### 2. Advanced Prompting Techniques

#### Prompt Templates

Create reusable prompt templates with variable placeholders:

```runa
Let template = PromptTemplate.create(
    "Generate a {{language}} function that {{task}} with these requirements: {{requirements}}"
)

Let prompt = template.fill({
    "language": "Runa",
    "task": "sorts a list",
    "requirements": "Must handle empty lists"
})
```

#### Few-Shot Learning

Improve model performance by providing examples:

```runa
Let examples = [
    {"input": "Sort [3, 1, 5, 2]", "output": "[1, 2, 3, 5]"},
    {"input": "Find max: [7, 2, 9, 4]", "output": "9"}
]

Let few_shot_prompt = FewShotPrompt.create(
    examples,
    prefix="Solve this problem:",
    suffix="{{input}}"
)
```

#### Chain-of-Thought Reasoning

Guide models through complex reasoning tasks:

```runa
Let response = model.complete_with_cot("Your complex problem here")
Print(response.reasoning)  # See the step-by-step reasoning
Print(response.answer)     # Get the final answer
```

### 3. Code Generation and Execution

Runa provides specialized methods for code generation and safe execution:

```runa
# Generate code
Let code = model.complete_as_code("Write a function to calculate factorial")

# Safely execute generated code
Let result = LLM.execute_safely(code, {"n": 5})
```

The `CodeGenerator` class offers additional capabilities:

```runa
Let generator = CodeGenerator.create()
Let generated_code = generator.generate("Description of desired code")
Let validation_result = generator.validate(generated_code)
```

### 4. Model Evaluation

Evaluate and compare LLM performance using Runa's built-in tools:

```runa
Let evaluator = ModelEvaluator.create()
Let test_data = Dataset.load("benchmark_dataset")
Let evaluation_results = evaluator.evaluate(model, test_data)
```

## Configuration

### Model Settings

Configure LLM behavior with custom settings:

```runa
Let model = LLM.connect("model_name", {
    "temperature": 0.7,
    "max_tokens": 1000,
    "top_p": 0.95,
    "frequency_penalty": 0.5,
    "presence_penalty": 0.5
})
```

### Provider Configuration

Set up connections to different LLM providers:

```runa
# Configure a provider
LLM.configure_provider("provider_name", {
    "api_key": "your_api_key",
    "base_url": "https://api.provider.com/v1",
    "default_model": "provider-model-name"
})

# Then connect using that provider
Let model = LLM.connect_with_provider("provider_name")
```

## Best Practices

1. **Prompt Engineering**: Craft clear, specific prompts for better results
2. **Model Selection**: Choose appropriate models for different tasks (code generation vs. text completion)
3. **Error Handling**: Always implement proper error handling when working with LLMs
4. **Content Safety**: Use content filtering options when generating user-facing content
5. **Performance Optimization**: Cache common responses for frequently used prompts

## Example: Building an LLM-powered Assistant

```runa
Process called "create_assistant":
    # Initialize assistant with specific capabilities
    Let assistant = Assistant.create({
        "name": "RunaHelper",
        "description": "Coding assistant for Runa developers",
        "capabilities": ["code_generation", "documentation", "debugging"]
    })
    
    # Connect to preferred LLM
    Let model = LLM.connect("runa_assistant_model")
    assistant.set_model(model)
    
    # Configure assistant behavior
    assistant.configure({
        "code_style": "idiomatic_runa",
        "verbosity": "medium",
        "include_explanations": true
    })
    
    # Start interactive session
    Let session = assistant.start_session()
    
    Return assistant
```

## References

- [Runa AI Module API Reference](https://runa-lang.org/docs/api/ai)
- [Prompt Engineering Guide](https://runa-lang.org/docs/guides/prompt-engineering)
- [LLM Model Compatibility List](https://runa-lang.org/docs/llm/compatibility)

For complete examples, see the [LLM Integration Examples](../../src/tests/examples/llm_integration_examples.runa) in the Runa codebase. 