# LLM Integration Overview

## Introduction

Runa's LLM (Large Language Model) integration system provides seamless interaction with AI language models for code generation, completion, and analysis. This enables AI-powered development workflows and enhances Runa's capabilities as a language designed for AI-to-AI communication.

## Key Components

### LLM Manager

The central component of the LLM integration is the `LLMManager`, which:

- Manages connections to different LLM providers (OpenAI, Anthropic, etc.)
- Stores and retrieves prompt templates
- Provides a unified interface for generating responses

A global instance `llm_manager` is available to simplify integration throughout the codebase.

### Code Suggestion System

The Code Suggestion System provides intelligent, context-aware code completions:

- Analyzes code context to provide relevant suggestions
- Offers different types of completions (function, import, variable, etc.)
- Integrates with knowledge graph for enhanced suggestions
- Provides confidence scoring for suggestions

See the [Code Suggestion System documentation](./CodeSuggestion.md) for details.

### Prompt System

The prompt system consists of several key components:

1. **PromptType Enum**: Categorizes different types of prompts:
   - `CODE_GENERATION`: For generating Runa code from requirements
   - `CODE_COMPLETION`: For completing partial code
   - `CODE_EXPLANATION`: For explaining existing code
   - `INTENT_TO_CODE`: For converting natural language to code
   - `CODE_REVIEW`: For reviewing and suggesting improvements
   - `KNOWLEDGE_EXTRACTION`: For extracting knowledge from code
   - `KNOWLEDGE_LINKING`: For linking code to knowledge graph entities
   - `BRAIN_HAT_COMMUNICATION`: For AI-to-AI communication
   - `CUSTOM`: For user-defined prompt types

2. **PromptTemplate**: Creates structured prompts with placeholders:
   ```python
   template = PromptTemplate(
       template="# Generate code for: {task}\n{requirements}",
       prompt_type=PromptType.CODE_GENERATION
   )
   prompt = template.format(task="Fibonacci", requirements="Iterative solution")
   ```

3. **LLMPrompt**: Represents a complete prompt ready to send to an LLM:
   ```python
   prompt = LLMPrompt(
       content="Generate a function to calculate Fibonacci numbers",
       prompt_type=PromptType.CODE_GENERATION,
       model="gpt-4",
       temperature=0.7
   )
   ```

4. **LLMResponse**: Contains the response from an LLM:
   ```python
   response = provider.generate(prompt)
   print(f"Content: {response.content}")
   print(f"Tokens used: {response.tokens_used}")
   ```

### Provider System

The provider system connects to various LLM APIs:

1. **LLMProvider (Abstract Base Class)**: Defines the interface all providers must implement:
   - `generate(prompt)`: Generate a response from a prompt
   - `get_available_models()`: List available models

2. **OpenAIProvider**: Connects to OpenAI's API:
   ```python
   provider = OpenAIProvider(api_key="your-api-key")
   response = provider.generate_code("Create a function to sort a list")
   ```

## Standard Prompt Templates

Runa provides several standard prompt templates:

1. **Code Generation**:
   ```
   # Task: Generate Runa code for the following task
   
   ## Requirements
   {requirements}
   
   ## Additional Context
   {context}
   
   ## Generate complete, well-documented Runa code that implements the requirements:
   ```

2. **Code Completion**:
   ```
   # Task: Complete the following Runa code
   
   ## Context
   {context}
   
   ## Code to Complete
   ```
   {code}
   ```
   
   ## Complete the code according to the following requirements
   {requirements}
   
   ## Your completion should seamlessly continue from the existing code:
   ```

3. **Code Explanation**:
   ```
   # Task: Explain the following Runa code
   
   ## Code
   ```
   {code}
   ```
   
   ## Provide a clear, detailed explanation of how this code works:
   ```

4. **Knowledge Extraction**:
   ```
   # Task: Extract knowledge entities and relationships from the following Runa code
   
   ## Code
   ```
   {code}
   ```
   
   ## Extract and list all relevant knowledge entities and the relationships between them:
   ```

## Usage Examples

### Basic Code Generation

```python
from runa.ai.llm_integration import llm_manager

# Get the default provider
provider = llm_manager.get_provider()

# Generate code
response = provider.generate_code(
    requirements="Create a function to calculate factorial numbers",
    context="Handle non-negative integers only"
)

# Use the generated code
print(response.content)
```

### Code Suggestion System

```python
from runa.ai.llm_integration import SuggestionContext, CodeSuggestionEngine

# Create context for current cursor position
context = SuggestionContext(
    code_before_cursor="Let result = fibonacci(",
    code_after_cursor=")",
    file_path="example.rn"
)

# Create suggestion engine
engine = CodeSuggestionEngine()

# Get suggestions
suggestions = engine.get_suggestions(context)

# Use suggestions
for suggestion in suggestions:
    print(f"{suggestion.text} (confidence: {suggestion.confidence})")
```

### Custom Prompt Template

```python
from runa.ai.llm_integration import PromptTemplate, PromptType, llm_manager

# Create a custom template
custom_template = PromptTemplate(
    template="""
    # Generate a {language} class for {entity}
    With properties: {properties}
    And methods: {methods}
    """,
    prompt_type=PromptType.CODE_GENERATION
)

# Register the template
llm_manager.register_template("class_generator", custom_template)

# Generate from template
response = llm_manager.generate_from_template(
    "class_generator",
    language="Runa",
    entity="Person",
    properties="name, age, email",
    methods="greet(), get_full_info()"
)
```

### Connecting to Different Providers

```python
from runa.ai.llm_integration import OpenAIProvider, llm_manager

# Register providers
openai_provider = OpenAIProvider(api_key="your-openai-key")
llm_manager.register_provider("openai", openai_provider, default=True)

# Use a specific provider
response = llm_manager.generate(
    "Generate a sorting function",
    provider="openai"
)
```

## Brain-Hat Communication

The LLM integration system supports Runa's Brain-Hat communication paradigm:

```python
from runa.ai.llm_integration import llm_manager

response = llm_manager.generate_from_template(
    "brain_hat",
    task_type="Enhance",
    context="Implementing a neural network module",
    brain_reasoning="""
    For a transformer model, attention heads should have dimension h/n
    to maintain computational efficiency, where h is hidden_size and
    n is num_heads.
    """,
    hat_implementation="""
    Process called "create_transformer" that takes config:
        Let attention_head_size be config.hidden_size / config.num_heads
        # Implement attention mechanism
    """
)
```

## Integration with Knowledge Graphs

The LLM integration system can work with Runa's knowledge graph system:

```python
from runa.ai.llm_integration import llm_manager
from runa.ai.knowledge_connectors import get_connector_for_uri

# Extract knowledge from code
code = "Process called 'quick_sort' that takes arr: ..."
knowledge_response = llm_manager.get_provider().extract_knowledge(code)

# Connect to knowledge graph
connector = get_connector_for_uri("ontology.ttl")
connector.connect()

# Convert extracted knowledge to entities and triples
# ... parsing logic ...

# Store in knowledge graph
connector.store_entity(entity)
connector.store_triple(triple)
```

## Configuration and Extension

### Adding New Providers

To add a new provider, extend the `LLMProvider` class:

```python
from runa.ai.llm_integration import LLMProvider, LLMResponse, LLMPrompt

class MyCustomProvider(LLMProvider):
    def __init__(self, api_key=None):
        super().__init__(api_key)
        # Custom initialization
    
    def generate(self, prompt):
        # Implementation
        return LLMResponse(...)
    
    def get_available_models(self):
        return ["my-model-1", "my-model-2"]

# Register the provider
llm_manager.register_provider("my_provider", MyCustomProvider())
```

### Adding New Prompt Templates

New prompt templates can be added as needed:

```python
from runa.ai.llm_integration import PromptTemplate, PromptType

refactoring_template = PromptTemplate(
    template="""
    # Task: Refactor the following Runa code
    
    ## Original Code
    ```
    {code}
    ```
    
    ## Refactoring Goals
    {goals}
    
    ## Refactored code:
    """,
    prompt_type=PromptType.CODE_GENERATION
)

llm_manager.register_template("refactoring", refactoring_template)
```

## Best Practices

1. **Use Templates**: Prefer using templates over raw prompts for consistency
2. **Handle Errors**: Always handle potential API errors gracefully
3. **Cache Results**: Consider caching responses for frequent/similar prompts
4. **Monitor Token Usage**: Track token usage to control costs
5. **Validate Outputs**: Verify generated code before executing or saving it
6. **Provide Context**: Include relevant context in prompts for better results
7. **Use Type Hinting**: Leverage Python's type hinting for better IDE support

## Documentation

For more detailed information, see these additional documents:

- [Code Suggestion System](./CodeSuggestion.md) - Intelligent code completions
- [Prompt Templates](./PromptTemplates.md) - Working with prompt templates
- [Brain-Hat Protocol](./BrainHatProtocol.md) - AI-to-AI communication
- [Knowledge Integration](./KnowledgeIntegration.md) - Using knowledge with LLMs

## Next Steps

The LLM integration system will continue to evolve with:

1. **Additional Providers**: Support for more LLM providers
2. **Better Caching**: Intelligent caching system for responses
3. **Fine-Tuning**: Tools for fine-tuning models on Runa code
4. **Streaming Responses**: Support for streaming API responses
5. **Advanced Context Management**: Better handling of context windows
```