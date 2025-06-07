# FeedbackAnnotation

## Overview

`FeedbackAnnotation` is a specialized annotation class designed for communication between AI systems, allowing them to provide structured feedback on code. This class is part of Runa's annotation system that enables AI-to-AI communication through code annotations.

## Class Definition

The `FeedbackAnnotation` class extends the base `AnnotationNode` class and specifically represents feedback suggestions between AI components:

```python
@dataclass
class FeedbackAnnotation(AnnotationNode):
    """Annotation for feedback between AI systems."""
    suggestion: str
    improvement_area: str
    priority: str = "medium"  # "high", "medium", "low"
```

## Parameters

- **suggestion** (required): A specific suggestion for improvement or change
- **improvement_area** (required): The area or aspect that needs improvement
- **priority** (optional): The importance level of the feedback, can be "high", "medium", or "low" (default: "medium")

Additionally, it inherits these parameters from `AnnotationNode`:
- **annotation_type**: Automatically set to `AnnotationType.FEEDBACK`
- **content**: The general content or description of the feedback
- **source_position**: Information about the source code position
- **metadata**: Additional metadata for the annotation

## Usage in Code

### Comment Format

Feedback annotations are typically added as comments in the Runa code:

```python
# @feedback(area="performance", priority="high"): The recursive approach causes excessive memory usage
```

### Manual Creation

While `FeedbackAnnotation` instances are typically created automatically by the parser, they can also be created manually:

```python
from runa.annotation_system import FeedbackAnnotation, AnnotationType

feedback = FeedbackAnnotation(
    annotation_type=AnnotationType.FEEDBACK,
    content="The recursive approach causes excessive memory usage",
    suggestion="Use an iterative approach instead",
    improvement_area="performance",
    priority="high"
)
```

## Integration with the Annotation System

The `FeedbackAnnotation` class is integrated with the rest of the annotation system:

1. **Parsing**: The `AnnotationParser` automatically detects and parses `@feedback` annotations in code comments
2. **Analysis**: The `AnnotationAnalyzer` processes feedback annotations to extract insights
3. **Generation**: The `AnnotationGenerator` can create properly formatted feedback comments from annotation objects

## Example

```python
# Original code with feedback annotation
Process called "fibonacci" that takes n:
    # @feedback(area="performance", priority="high"): This recursive implementation has exponential time complexity
    If n is less than or equal to 1:
        Return n
    Return fibonacci(n - 1) + fibonacci(n - 2)

# Improved code based on feedback
Process called "fibonacci" that takes n:
    # @feedback(area="performance", priority="low"): The iterative approach is more efficient
    Let a be 0
    Let b be 1
    
    If n is 0:
        Return 0
    
    For i from 2 to n inclusive:
        Let temp be a + b
        Set a to b
        Set b to temp
    
    Return b
```

## Best Practices

1. **Be specific**: Provide concrete suggestions rather than vague criticism
2. **Prioritize appropriately**: Use the priority parameter to indicate the importance
3. **Specify the area**: Categorize the feedback into specific areas like "performance", "readability", "security", etc.
4. **Link to knowledge**: When possible, reference established patterns or principles

## Related Classes

- `AnnotationNode`: The base class for all annotations
- `AnnotationType`: Enum defining the types of annotations
- `AnnotationParser`: Parser that creates annotation instances from comments
- `AnnotationAnalyzer`: Analyzes annotations and extracts insights
- `AnnotationGenerator`: Generates annotation comments from annotation objects
``` 