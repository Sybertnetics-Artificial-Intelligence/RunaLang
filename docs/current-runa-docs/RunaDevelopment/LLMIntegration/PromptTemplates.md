# Working with Prompt Templates

This guide explains how to use, customize, and create prompt templates in the Runa LLM integration system.

## Overview

Prompt templates provide a standardized way to communicate with LLMs, helping ensure consistent results across different requests and providers. Runa's prompt template system offers:

- Pre-defined templates for common tasks
- Customization options for existing templates
- A framework for creating new templates
- Template management through the `LLMManager`

## Using Built-in Templates

Runa comes with several pre-defined templates for common tasks:

```python
from runa.ai.llm_integration import llm_manager

# Generate code using the built-in code generation template
response = llm_manager.generate(
    template_name="code_generation",
    requirements="Create a function that calculates the Fibonacci sequence",
    context="This is for a math library"
)

# Explain code using the built-in code explanation template
code_to_explain = """
process fibonacci(n: Number) returns: List<Number>
    if n <= 0 then
        return []
    end
    
    if n == 1 then
        return [0]
    end
    
    if n == 2 then
        return [0, 1]
    end
    
    sequence = [0, 1]
    
    for i in 3..n do
        sequence.append(sequence[i-3] + sequence[i-2])
    end
    
    return sequence
end
"""

explanation = llm_manager.generate(
    template_name="code_explanation",
    code=code_to_explain
)

print(explanation.content)
```

## Standard Built-in Templates

Runa provides the following built-in templates:

1. **Code Generation** (`code_generation`): Creates new code based on requirements
2. **Code Completion** (`code_completion`): Completes partially written code
3. **Code Explanation** (`code_explanation`): Explains what code does in natural language
4. **Knowledge Extraction** (`knowledge_extraction`): Extracts knowledge entities and relationships from code
5. **Bug Fixing** (`bug_fixing`): Identifies and fixes bugs in code
6. **Refactoring** (`refactoring`): Suggests code improvements
7. **Comment Generation** (`comment_generation`): Generates documentation comments for code

## Template Structure

Each prompt template consists of:

1. A name for identifying the template
2. A prompt type (from the `PromptType` enum)
3. A template string with placeholders for variables
4. Optional default parameters

## Creating Custom Templates

You can create custom templates for specific needs:

```python
from runa.ai.llm_integration import llm_manager, PromptTemplate, PromptType

# Create a custom template for generating test cases
test_case_template = PromptTemplate(
    name="test_case_generation",
    prompt_type=PromptType.CUSTOM,
    template="""
You are a test case generator for the Runa programming language.
Given the following code, generate {test_count} test cases that thoroughly test the functionality.
For each test case, provide the input values, expected output, and a brief description of what the test is checking.

CODE:
{code}

ADDITIONAL REQUIREMENTS:
{requirements}
    """,
    default_params={"test_count": 5, "requirements": "Include edge cases"}
)

# Register the custom template with the llm_manager
llm_manager.register_template(test_case_template)

# Use the custom template
function_code = """
process absolute_value(x: Number) returns: Number
    if x < 0 then
        return -x
    else
        return x
    end
end
"""

test_cases = llm_manager.generate(
    template_name="test_case_generation",
    code=function_code,
    test_count=3  # Override the default value
)

print(test_cases.content)
```

## Template Management

The `LLMManager` provides methods for managing templates:

```python
from runa.ai.llm_integration import llm_manager, PromptTemplate, PromptType

# List all available template names
template_names = llm_manager.get_template_names()
print(template_names)

# Get a specific template
code_gen_template = llm_manager.get_template("code_generation")
print(code_gen_template.template)

# Create a modified version of an existing template
original = llm_manager.get_template("code_explanation")
modified = PromptTemplate(
    name="detailed_code_explanation",
    prompt_type=original.prompt_type,
    template=original.template + "\n\nInclude a detailed analysis of time and space complexity.",
    default_params=original.default_params
)
llm_manager.register_template(modified)

# Remove a template
llm_manager.unregister_template("detailed_code_explanation")
```

## Direct Template Formatting

You can format a template directly without sending it to an LLM:

```python
from runa.ai.llm_integration import llm_manager

template = llm_manager.get_template("code_generation")
formatted_prompt = template.format(
    requirements="Create a function to sort a list",
    context="This will be used in a utility library"
)

print(formatted_prompt)
```

## Creating Advanced Templates

For more complex use cases, you can create templates with conditional sections:

```python
from runa.ai.llm_integration import PromptTemplate, PromptType

advanced_template = PromptTemplate(
    name="advanced_code_generation",
    prompt_type=PromptType.CODE_GENERATION,
    template="""
You are a code generator for the Runa programming language.

TASK: Generate code based on the requirements below.
REQUIREMENTS: {requirements}
{context_section}
{constraints_section}
{examples_section}

Your code should be clear, efficient, and follow Runa best practices.
    """,
    default_params={}
)

def format_advanced_template(requirements, context=None, constraints=None, examples=None):
    params = {"requirements": requirements}
    
    # Conditional sections based on provided parameters
    params["context_section"] = f"CONTEXT: {context}" if context else ""
    params["constraints_section"] = f"CONSTRAINTS: {constraints}" if constraints else ""
    params["examples_section"] = f"EXAMPLES: {examples}" if examples else ""
    
    return advanced_template.format(**params)

# Usage
formatted_prompt = format_advanced_template(
    requirements="Create a search function for sorted arrays",
    context="This will be used in a performance-critical application",
    constraints="Must be O(log n) time complexity",
    examples="For input [1, 3, 5, 7, 9] and target 5, return index 2"
)

print(formatted_prompt)
```

## Template Categories

You can organize templates into categories:

```python
from runa.ai.llm_integration import llm_manager, PromptTemplate, PromptType

# Create templates for different categories
code_templates = {
    "basic_function": PromptTemplate(
        name="basic_function",
        prompt_type=PromptType.CODE_GENERATION,
        template="Generate a basic function that {requirements}",
        default_params={}
    ),
    "class_definition": PromptTemplate(
        name="class_definition",
        prompt_type=PromptType.CODE_GENERATION,
        template="Generate a class definition that {requirements}",
        default_params={}
    )
}

test_templates = {
    "unit_test": PromptTemplate(
        name="unit_test",
        prompt_type=PromptType.CODE_GENERATION,
        template="Generate unit tests for {code}",
        default_params={}
    ),
    "integration_test": PromptTemplate(
        name="integration_test",
        prompt_type=PromptType.CODE_GENERATION,
        template="Generate integration tests for {code}",
        default_params={}
    )
}

# Register templates with category prefixes
for name, template in code_templates.items():
    llm_manager.register_template(template, category="code")

for name, template in test_templates.items():
    llm_manager.register_template(template, category="test")

# Get templates by category
code_template_names = llm_manager.get_template_names(category="code")
print(code_template_names)  # ["code.basic_function", "code.class_definition"]

# Use a categorized template
response = llm_manager.generate(
    template_name="code.basic_function",
    requirements="calculate the area of a circle"
)
```

## Template Versioning

You can maintain multiple versions of a template:

```python
from runa.ai.llm_integration import llm_manager, PromptTemplate, PromptType

# Create multiple versions of a template
template_v1 = PromptTemplate(
    name="refactoring",
    prompt_type=PromptType.REFACTORING,
    template="Refactor this code: {code}",
    default_params={}
)

template_v2 = PromptTemplate(
    name="refactoring",
    prompt_type=PromptType.REFACTORING,
    template="Refactor this code to improve readability and performance: {code}",
    default_params={}
)

# Register templates with version
llm_manager.register_template(template_v1, version="1.0")
llm_manager.register_template(template_v2, version="2.0")

# Set default version
llm_manager.set_default_template_version("refactoring", "2.0")

# Use specific version
response_v1 = llm_manager.generate(
    template_name="refactoring",
    version="1.0",
    code="function add(a, b) { return a + b; }"
)

# Use default version
response_default = llm_manager.generate(
    template_name="refactoring",
    code="function add(a, b) { return a + b; }"
)
```

## Chain-of-Thought Templates

For complex reasoning tasks, you can create chain-of-thought templates:

```python
from runa.ai.llm_integration import PromptTemplate, PromptType

cot_template = PromptTemplate(
    name="algorithm_design",
    prompt_type=PromptType.CUSTOM,
    template="""
You are an expert algorithm designer.

PROBLEM DESCRIPTION:
{problem}

Please solve this step by step:

1. First, understand the problem:
   - What are the inputs and outputs?
   - What are the constraints?
   - What are the edge cases?

2. Next, explore possible approaches:
   - What algorithms could potentially solve this?
   - What are the trade-offs for each approach?

3. Choose an approach and explain why:
   - Which approach is best for this problem?
   - What is the time and space complexity?

4. Finally, implement the solution in Runa:
   - Write clear, efficient code
   - Include comments explaining key parts

Now, solve the problem step by step.
    """,
    default_params={}
)

llm_manager.register_template(cot_template)
```

## Best Practices

1. **Be Specific**: Clearly define what you expect from the LLM in the template
2. **Include Context**: Provide information about how the code will be used
3. **Set Constraints**: Specify any limitations or requirements
4. **Give Examples**: Include examples when relevant
5. **Test Variations**: Try different template wordings to find what works best
6. **Version Control**: Keep track of changes to templates
7. **Reuse Components**: Create helper functions for common template patterns
8. **Review Outputs**: Regularly review outputs to refine templates

## Troubleshooting

Common issues when working with templates:

1. **Missing Parameters**: Ensure all placeholders in the template have corresponding parameters
2. **Template Too Vague**: Make templates specific enough to get consistent results
3. **Template Too Restrictive**: Don't over-constrain the model's creativity when beneficial
4. **Version Conflicts**: Be aware of which template version you're using
5. **Template Size**: Very large templates may consume tokens but not improve results

## Advanced Example: Multi-Step Code Generation

Here's how to use templates for a multi-step code generation process:

```python
from runa.ai.llm_integration import llm_manager

# Step 1: Generate a high-level design
design_template = llm_manager.get_template("high_level_design")
design_response = llm_manager.generate(
    template_name="high_level_design",
    requirements="Create a todo list application with the ability to add, complete, and delete tasks"
)

# Step 2: Generate code components based on the design
components = ["Task", "TaskList", "TaskManager"]
component_code = {}

for component in components:
    component_response = llm_manager.generate(
        template_name="component_implementation",
        component_name=component,
        design=design_response.content
    )
    component_code[component] = component_response.content

# Step 3: Generate integration code
integration_response = llm_manager.generate(
    template_name="component_integration",
    components=component_code
)

# Step 4: Generate tests
test_response = llm_manager.generate(
    template_name="test_suite",
    code=integration_response.content
)

print("Design:", design_response.content)
print("Component Code:", component_code)
print("Integration Code:", integration_response.content)
print("Tests:", test_response.content)
```

## Conclusion

Prompt templates are a powerful way to standardize and optimize your interactions with LLMs in Runa. By creating well-designed templates, you can achieve more consistent, higher-quality results while reducing token usage and improving the developer experience.

For more information, see the [LLM Integration Overview](./Overview.md) and [Creating Custom Providers](./CreateCustomProvider.md) documentation. 