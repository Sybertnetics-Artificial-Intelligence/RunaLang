# Creating a Custom LLM Provider

This guide explains how to implement a custom LLM provider to integrate additional AI models into the Runa framework.

## Overview

The Runa LLM integration system is designed to be extensible, allowing you to connect to any LLM API by implementing a custom provider. This is useful when you want to:

- Use an LLM API not already supported in Runa
- Implement a specialized provider with custom behavior
- Create a mock provider for testing purposes
- Integrate with an on-premises LLM deployment

## Basic Structure

Every LLM provider in Runa must extend the `LLMProvider` abstract base class and implement its required methods:

```python
from runa.ai.llm_integration import LLMProvider, LLMResponse, LLMPrompt, PromptType

class MyCustomProvider(LLMProvider):
    def __init__(self, api_key=None, **kwargs):
        super().__init__(api_key)
        # Additional initialization
        
    def get_available_models(self):
        # Return a list of available models
        return ["my-model-v1", "my-model-v2"]
        
    def generate(self, prompt):
        # Process the prompt and return a response
        if isinstance(prompt, str):
            prompt = LLMPrompt(content=prompt)
            
        # Call the actual API
        # ...
        
        return LLMResponse(
            content="Generated content",
            tokens_used={"prompt": 10, "completion": 20, "total": 30}
        )
```

## Complete Example

Here's a complete example of a custom provider that connects to a hypothetical "ExampleAI" API:

```python
import requests
from typing import Dict, List, Optional, Union

from runa.ai.llm_integration import (
    LLMProvider, 
    LLMPrompt, 
    LLMResponse, 
    PromptType
)

class ExampleAIProvider(LLMProvider):
    """Provider for ExampleAI API."""
    
    def __init__(self, api_key=None, api_url="https://api.example.ai/v1", **kwargs):
        super().__init__(api_key)
        self.api_url = api_url
        self.headers = {"Authorization": f"Bearer {api_key}"}
        self.default_model = kwargs.get("default_model", "example-v1")
        
    def get_available_models(self) -> List[str]:
        """Get a list of available models from ExampleAI."""
        try:
            response = requests.get(
                f"{self.api_url}/models",
                headers=self.headers
            )
            response.raise_for_status()
            return [model["id"] for model in response.json()["data"]]
        except Exception as e:
            print(f"Error fetching models: {str(e)}")
            # Return default models if API call fails
            return ["example-v1", "example-v2"]
    
    def generate(self, prompt: Union[str, LLMPrompt]) -> LLMResponse:
        """Generate a response from ExampleAI."""
        if isinstance(prompt, str):
            prompt = LLMPrompt(content=prompt)
            
        model = prompt.model or self.default_model
        temperature = prompt.temperature or 0.7
        
        try:
            response = requests.post(
                f"{self.api_url}/completions",
                headers=self.headers,
                json={
                    "model": model,
                    "prompt": prompt.content,
                    "temperature": temperature,
                    "max_tokens": prompt.max_tokens or 1000
                }
            )
            response.raise_for_status()
            result = response.json()
            
            return LLMResponse(
                content=result["choices"][0]["text"],
                tokens_used={
                    "prompt": result["usage"]["prompt_tokens"],
                    "completion": result["usage"]["completion_tokens"],
                    "total": result["usage"]["total_tokens"]
                }
            )
        except Exception as e:
            error_msg = f"Error generating completion: {str(e)}"
            print(error_msg)
            return LLMResponse(
                content=f"Error: {error_msg}",
                tokens_used={"prompt": 0, "completion": 0, "total": 0}
            )
    
    # Convenience methods for specific tasks
    
    def generate_code(self, requirements: str, context: str = "") -> LLMResponse:
        """Generate code based on requirements and context."""
        prompt = self._get_prompt_from_template(
            "code_generation",
            requirements=requirements,
            context=context
        )
        return self.generate(prompt)
    
    def complete_code(self, code: str, requirements: str = "", context: str = "") -> LLMResponse:
        """Complete the given code according to requirements."""
        prompt = self._get_prompt_from_template(
            "code_completion",
            code=code,
            requirements=requirements,
            context=context
        )
        return self.generate(prompt)
    
    def explain_code(self, code: str) -> LLMResponse:
        """Explain the given code."""
        prompt = self._get_prompt_from_template(
            "code_explanation",
            code=code
        )
        return self.generate(prompt)
    
    def extract_knowledge(self, code: str) -> LLMResponse:
        """Extract knowledge entities and relationships from code."""
        prompt = self._get_prompt_from_template(
            "knowledge_extraction",
            code=code
        )
        return self.generate(prompt)
    
    def _get_prompt_from_template(self, template_name: str, **kwargs) -> LLMPrompt:
        """Get a formatted prompt from a template."""
        from runa.ai.llm_integration import llm_manager
        
        template = llm_manager.get_template(template_name)
        if not template:
            raise ValueError(f"Template '{template_name}' not found")
            
        content = template.format(**kwargs)
        return LLMPrompt(
            content=content,
            prompt_type=template.prompt_type
        )
```

## Registering Your Provider

After implementing your custom provider, you need to register it with the `llm_manager`:

```python
from runa.ai.llm_integration import llm_manager
from your_module import ExampleAIProvider

# Create an instance of your provider
example_provider = ExampleAIProvider(api_key="your-api-key")

# Register it with the llm_manager
llm_manager.register_provider("example_ai", example_provider)

# Optionally, set it as the default provider
llm_manager.set_default_provider("example_ai")
```

You can also register your provider in your module's `__init__.py` file:

```python
from runa.ai.llm_integration import llm_manager

try:
    from .example_provider import ExampleAIProvider
    
    # Register if API key is available
    import os
    api_key = os.environ.get("EXAMPLE_AI_API_KEY")
    if api_key:
        provider = ExampleAIProvider(api_key=api_key)
        llm_manager.register_provider("example_ai", provider)
        print("ExampleAI provider registered successfully")
except Exception as e:
    print(f"Warning: Failed to initialize ExampleAI provider: {str(e)}")
```

## Creating a Mock Provider

For testing or development purposes, you might want to create a mock provider that doesn't require an actual API:

```python
class MockLLMProvider(LLMProvider):
    """Mock LLM provider for testing and development."""
    
    def __init__(self, **kwargs):
        super().__init__(None)  # No API key needed
        self.responses = {
            PromptType.CODE_GENERATION: "Process called 'example' that takes x: Number returns: Number\n    Return x * 2",
            PromptType.CODE_COMPLETION: "    Return x * 2\nend",
            PromptType.CODE_EXPLANATION: "This code defines a process that doubles the input number.",
            PromptType.KNOWLEDGE_EXTRACTION: "Entities: Process('example'), Parameter('x'), Type('Number')\nRelationships: Process('example') TAKES Parameter('x'), Parameter('x') HAS_TYPE Type('Number')",
            PromptType.CUSTOM: "Custom response"
        }
        
    def get_available_models(self):
        return ["mock-model"]
        
    def generate(self, prompt):
        if isinstance(prompt, str):
            prompt = LLMPrompt(content=prompt)
            
        prompt_type = prompt.prompt_type or PromptType.CUSTOM
        content = self.responses.get(prompt_type, "Default mock response")
        
        # Simulate token usage
        tokens_used = {
            "prompt": len(prompt.content) // 4,
            "completion": len(content) // 4,
            "total": (len(prompt.content) + len(content)) // 4
        }
        
        return LLMResponse(
            content=content,
            tokens_used=tokens_used
        )
```

## Implementing Advanced Features

### Streaming Responses

To implement streaming for providers that support it:

```python
def generate_stream(self, prompt):
    """Generate a streaming response."""
    if isinstance(prompt, str):
        prompt = LLMPrompt(content=prompt)
        
    response = requests.post(
        f"{self.api_url}/completions",
        headers=self.headers,
        json={
            "model": prompt.model or self.default_model,
            "prompt": prompt.content,
            "stream": True
        },
        stream=True
    )
    
    for line in response.iter_lines():
        if line:
            # Parse the streamed data
            data = json.loads(line.decode('utf-8').replace('data: ', ''))
            if 'choices' in data and len(data['choices']) > 0:
                yield data['choices'][0]['text']
```

### Batch Processing

For efficiency when processing multiple prompts:

```python
def batch_generate(self, prompts):
    """Generate responses for multiple prompts in batch."""
    results = []
    for prompt in prompts:
        results.append(self.generate(prompt))
    return results
```

### Caching

To implement caching for frequently used prompts:

```python
import hashlib
import json
import os
import pickle

class CachingLLMProvider(LLMProvider):
    """An LLM provider wrapper that implements caching."""
    
    def __init__(self, base_provider, cache_dir=".llm_cache"):
        super().__init__(None)
        self.provider = base_provider
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        
    def get_available_models(self):
        return self.provider.get_available_models()
        
    def generate(self, prompt):
        # Create a cache key from the prompt
        if isinstance(prompt, LLMPrompt):
            cache_key = hashlib.md5(
                json.dumps({
                    "content": prompt.content,
                    "model": prompt.model,
                    "temperature": prompt.temperature
                }).encode()
            ).hexdigest()
        else:
            cache_key = hashlib.md5(str(prompt).encode()).hexdigest()
            
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.pkl")
        
        # Check if we have a cached response
        if os.path.exists(cache_file):
            with open(cache_file, 'rb') as f:
                return pickle.load(f)
                
        # Generate a new response
        response = self.provider.generate(prompt)
        
        # Cache the response
        with open(cache_file, 'wb') as f:
            pickle.dump(response, f)
            
        return response
```

## Best Practices

1. **Error Handling**: Always implement robust error handling to avoid crashes when API calls fail.

2. **Token Tracking**: Accurately track and report token usage to help manage costs.

3. **Rate Limiting**: Implement rate limiting to avoid exceeding API quotas.

4. **Timeout Handling**: Set appropriate timeouts for API calls and handle timeouts gracefully.

5. **Configuration Flexibility**: Make your provider configurable with reasonable defaults.

6. **Documentation**: Document your provider's features, limitations, and required environment variables.

7. **Testing**: Create unit tests for your provider, using mocks for API calls.

8. **Versioning**: Handle API version changes gracefully, either through configuration or automatic detection.

## Testing Your Provider

Here's an example of how to test your custom provider:

```python
import unittest
from unittest.mock import patch, MagicMock

from your_module import ExampleAIProvider
from runa.ai.llm_integration import LLMPrompt, PromptType

class TestExampleAIProvider(unittest.TestCase):
    
    def setUp(self):
        self.provider = ExampleAIProvider(api_key="test-key")
        
    @patch('requests.get')
    def test_get_available_models(self, mock_get):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": [{"id": "example-v1"}, {"id": "example-v2"}]
        }
        mock_get.return_value = mock_response
        
        # Call the method
        models = self.provider.get_available_models()
        
        # Assert the result
        self.assertEqual(models, ["example-v1", "example-v2"])
        
    @patch('requests.post')
    def test_generate(self, mock_post):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"text": "Generated code"}],
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 5,
                "total_tokens": 15
            }
        }
        mock_post.return_value = mock_response
        
        # Create a prompt
        prompt = LLMPrompt(
            content="Generate code",
            prompt_type=PromptType.CODE_GENERATION
        )
        
        # Call the method
        response = self.provider.generate(prompt)
        
        # Assert the result
        self.assertEqual(response.content, "Generated code")
        self.assertEqual(response.tokens_used["total"], 15)
```

## Troubleshooting

Common issues when implementing custom providers:

1. **API Key Issues**: Ensure API keys are correctly configured and accessible.

2. **API URL Changes**: Keep API URLs updated as services evolve.

3. **Response Parsing Errors**: Handle different response formats gracefully.

4. **Network Connectivity**: Add retries for transient network issues.

5. **Token Counting**: Verify token counting logic matches the provider's actual counts.

6. **Temperature Scaling**: Ensure temperature values are properly scaled for the specific API.

7. **Model Availability**: Check that requested models are actually available in the API.

8. **Input Formatting**: Format inputs according to the specific expectations of each provider.

## Conclusion

By implementing a custom LLM provider, you can extend Runa's capabilities to work with any AI model or service that provides an API. This flexibility allows you to choose the best model for your specific needs or to integrate with proprietary models in enterprise environments.

For more information, refer to the [LLM Integration Overview](./Overview.md) document and the source code for existing providers in the `runa.ai.llm_integration` package. 