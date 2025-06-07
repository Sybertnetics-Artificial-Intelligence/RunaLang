# Code Suggestion System

## Overview

The Code Suggestion System provides intelligent, context-aware code completions for Runa code using LLM integration and Knowledge Graph data. This system offers suggestions for various coding scenarios, including function calls, import statements, variable assignments, and more.

## Key Components

### SuggestionContext

The `SuggestionContext` class captures the current editing context for generating accurate suggestions:

```python
from runa.ai.llm_integration import SuggestionContext

context = SuggestionContext(
    code_before_cursor="Process called \"example\" that takes arr:\n    Let sorted_arr be quick_sort(",
    code_after_cursor=")\n    # Rest of function",
    file_path="example.rn",
    imports=["runa.stdlib.sorting"],
    use_knowledge_graph=True
)
```

Key features:
- Tracks code before and after the cursor position
- Maintains file metadata and imports
- Extracts the current line, surrounding context, and current function/block
- Configurable context size for LLM prompts

### Suggestion Class

The `Suggestion` class represents a single code suggestion with confidence levels:

```python
from runa.ai.llm_integration import Suggestion

suggestion = Suggestion(
    text="arr, reverse=False",
    confidence=0.8,
    metadata={"type": "function_parameter"}
)
```

Properties:
- `text`: The actual suggestion text
- `display_text`: Optional text for display (if different from insertion text)
- `replacement_range`: Optional range of text to replace
- `confidence`: Confidence score (0.0 to 1.0)
- `metadata`: Additional information about the suggestion

### CodeSuggestionEngine

The `CodeSuggestionEngine` generates context-aware code suggestions:

```python
from runa.ai.llm_integration import CodeSuggestionEngine, SuggestionContext

# Create engine
engine = CodeSuggestionEngine(
    knowledge_manager=knowledge_manager,  # Optional knowledge graph integration
    provider_name="openai",               # LLM provider to use
    max_suggestions=5,                    # Maximum suggestions to return
    confidence_threshold=0.3              # Minimum confidence threshold
)

# Get suggestions
suggestions = engine.get_suggestions(context)
```

Features:
- Determines suggestion type based on context
- Generates tailored suggestions for different code patterns
- Integrates with knowledge graph data when available
- Caches suggestions for performance

## Suggestion Types

The system supports various suggestion types:

### 1. Function Completion

Suggests parameters for function calls:

```
Process called "example" that takes arr:
    Let sorted_arr be quick_sort(|)  # Cursor position
```

Suggestions might include:
- `arr`
- `arr, reverse=False`
- `arr, start=0, end=None`

### 2. Import Completion

Suggests module names for import statements:

```
import runa.stdlib.|  # Cursor position
```

Suggestions might include:
- `sorting`
- `data`
- `io`
- `collections`

### 3. Variable Completion

Suggests values for variable assignments:

```
Let max_value = |  # Cursor position
```

Suggestions might include:
- `data.max()`
- `Math.max(data)`
- `max(data)`

### 4. Parameter Completion

Suggests parameters for function/process definitions:

```
Process called "calculate_statistics" that takes |  # Cursor position
```

Suggestions might include:
- `data: List`
- `data: List, options: Dict = None`
- `values: List`

### 5. Line Completion

Suggests completions for the current line:

```
If n <= 1:
    Return |  # Cursor position
```

Suggestions might include:
- `1`
- `n if n <= 1 else 1`
- `1 # Base case`

## Knowledge Graph Integration

The suggestion system can integrate with Runa's Knowledge Graph:

```python
# Create engine with knowledge graph
engine = CodeSuggestionEngine(
    knowledge_manager=knowledge_manager,
    use_knowledge_graph=True
)
```

Benefits:
- Enhanced suggestions based on semantic understanding
- Access to function signatures and parameter information
- Awareness of related programming concepts
- Domain-specific suggestions based on knowledge entities

## Usage Examples

### Basic Usage

```python
from runa.ai.llm_integration import SuggestionContext, CodeSuggestionEngine

# Create context
context = SuggestionContext(
    code_before_cursor="Let result = fibonacci(",
    code_after_cursor=")",
    file_path="example.rn"
)

# Create engine
engine = CodeSuggestionEngine()

# Get suggestions
suggestions = engine.get_suggestions(context)

# Display suggestions
for suggestion in suggestions:
    print(f"{suggestion.text} (confidence: {suggestion.confidence})")
```

### IDE Integration

```python
def on_editor_change(editor):
    """Handle editor change event."""
    # Get editor state
    code = editor.get_text()
    cursor_position = editor.get_cursor_position()
    
    # Split code at cursor
    code_before = code[:cursor_position]
    code_after = code[cursor_position:]
    
    # Create context
    context = SuggestionContext(
        code_before_cursor=code_before,
        code_after_cursor=code_after,
        file_path=editor.get_file_path(),
        imports=editor.get_imports(),
        use_knowledge_graph=True
    )
    
    # Get suggestions
    engine = get_suggestion_engine()  # Singleton or cached instance
    suggestions = engine.get_suggestions(context)
    
    # Display suggestions in IDE
    editor.show_suggestions(suggestions)
```

## Performance Considerations

The suggestion system uses several techniques to maintain good performance:

1. **Caching**: Suggestions are cached based on context to avoid redundant LLM calls
2. **Context Limiting**: Only relevant portions of code are sent to the LLM
3. **Confidence Filtering**: Low-confidence suggestions are filtered out
4. **Type-based Generation**: Different suggestion types use optimized prompts

## Customization

### Creating Custom Suggestion Providers

You can extend the system with custom suggestion providers:

```python
from runa.ai.llm_integration import CodeSuggestionEngine

class CustomSuggestionEngine(CodeSuggestionEngine):
    def _determine_suggestion_type(self, context):
        # Custom logic to determine suggestion type
        return "custom_type"
    
    def _generate_custom_type_suggestions(self, context):
        # Custom implementation for generating suggestions
        return [Suggestion(text="custom suggestion", confidence=0.9)]
```

### Using Different LLM Providers

The system works with any LLM provider registered with the `llm_manager`:

```python
# Register a custom provider
from runa.ai.llm_integration import llm_manager
llm_manager.register_provider("my_provider", MyCustomProvider())

# Use the provider for suggestions
engine = CodeSuggestionEngine(provider_name="my_provider")
```

## Best Practices

1. **Context Quality**: Provide as much relevant context as possible
2. **Balance Suggestions**: Limit to 3-5 high-quality suggestions
3. **Filter by Confidence**: Use the confidence threshold to show only good suggestions
4. **Knowledge Integration**: When available, use knowledge graph data for better suggestions
5. **Cache Management**: Clear the cache when files change significantly

## Next Steps

The Code Suggestion System will continue to evolve with:

1. **Local Models**: Support for running smaller models locally
2. **Project-Specific Learning**: Adaptation to project-specific coding patterns
3. **Enhanced Knowledge Integration**: Deeper integration with knowledge graph
4. **User Feedback Loop**: Learning from which suggestions are accepted or rejected 