# Runa Language Reference

## Introduction

Runa is a revolutionary programming language designed to bridge human thought patterns with machine execution. Named after Norse runes that encoded knowledge and meaning, Runa features pseudocode-like syntax that resembles natural language while maintaining the precision needed for computational execution.

## Syntax and Structure

### Program Structure

A Runa program consists of a series of statements. Each statement typically occupies a single line, though complex statements may span multiple lines with proper indentation.

### Declarations and Assignments

Variables are declared using natural language constructs:

```
Let user name be "Alex"
Define preferred colors as list containing "blue", "green", "purple"
Set user age to 28
```

### Control Structures

Control flow in Runa uses minimal punctuation with human-readable keywords:

```
If user age is greater than 21:
    Set user status to "adult"
Otherwise:
    Set user status to "minor"
```

```
For each color in preferred colors:
    Display color with message "is a favorite color"
```

### Functions (Processes)

Functions in Runa are defined as "processes":

```
Process called "Calculate Total Price" that takes items and tax rate:
    Let subtotal be the sum of all prices in items
    Let tax amount be subtotal multiplied by tax rate
    Return subtotal plus tax amount
```

Functions are called using the "with" keyword:

```
Let final price be Calculate Total Price with:
    items as shopping cart items
    tax rate as 0.08
```

Or more concisely:

```
Let final price be Calculate Total Price with items as shopping cart items and tax rate as 0.08
```

### Display and Output

Output is handled through the Display statement:

```
Display "Hello, World!"
Display user name with message "has logged in"
```

## Advanced Type System

### Basic Types

- **String**: Text data enclosed in quotes
- **Integer**: Whole numbers (e.g., 1, -5, 42)
- **Float**: Floating-point numbers (e.g., 3.14, -0.5)
- **Boolean**: true or false values
- **List**: Ordered collections of items
- **Dictionary**: Key-value collections
- **Any**: Any value type
- **None**: The unit type

### Type Inference

Runa uses type inference to determine variable types:

```
Let age be 30  # Inferred as Integer
Let name be "Alex"  # Inferred as String
Let colors be list containing "red", "blue", "green"  # Inferred as List[String]
```

### Optional Type Annotations

Type annotations can be added for clarity:

```
Let age (Integer) be 30
Let name (String) be "Alex"
```

### Generic Types

Runa supports generic types for flexible, reusable code:

```
Type Pair[A, B] is Dictionary with:
    first as A
    second as B

Let point be Pair[Integer, Integer] with:
    first as 10
    second as 20
```

### Union Types

Union types represent values that could be one of several types:

```
Type Result is Integer OR String

Process called "safe_divide" that takes a as Integer and b as Integer returns Result:
    If b is equal to 0:
        Return "Cannot divide by zero"
    Otherwise:
        Return a divided by b
```

### Custom Type Definitions

Define custom types using the Type keyword:

```
Type Person is Dictionary with:
    name as String
    age as Integer
    email as String

Type UserRole is "admin" OR "user" OR "guest"
```

### Algebraic Data Types

Define variant types for complex data modeling:

```
Type Shape is
    | Circle with radius as Float
    | Rectangle with width as Float and height as Float
    | Triangle with base as Float and height as Float
```

## Pattern Matching

Runa includes powerful pattern matching capabilities:

```
Match user role:
    When "admin":
        Display "Full access granted"
    When "user":
        Display "Limited access granted"
    When _:
        Display "Access denied"
```

### Advanced Pattern Matching

```
Match shape:
    When Circle with radius as r:
        Return 3.14159 multiplied by r multiplied by r
    When Rectangle with width as w and height as h:
        Return w multiplied by h
    When Triangle with base as b and height as h:
        Return 0.5 multiplied by b multiplied by h
```

### List Pattern Matching

```
Match numbers:
    When list containing first and rest:
        Display "First element:" with message first
        Display "Remaining elements:" with message rest
    When list containing:
        Display "Empty list"
```

## Asynchronous Programming

Runa supports asynchronous programming with async/await:

```
Async Process called "Fetch Data" that takes url:
    Let response be await http get with url as url
    Return response

Async Process called "Process Multiple URLs" that takes urls:
    Let results be list containing
    For each url in urls:
        Let data be await Fetch Data with url as url
        Add data to results
    Return results
```

## Functional Programming

### Lambda Expressions

```
Let double be lambda x: x multiplied by 2
Let doubled numbers be Map over numbers using double
```

### Pipeline Operator

```
Let result be input data
    |> Process Data
    |> Filter Valid Items
    |> Transform Items
    |> Calculate Results
```

### Higher-Order Functions

```
Let numbers be list containing 1, 2, 3, 4, 5
Let evens be Filter numbers where lambda x: x modulo 2 is equal to 0
Let squares be Map over numbers using lambda x: x multiplied by x
Let sum be Reduce numbers using lambda acc and x: acc plus x
```

## Standard Library

### List Operations

```
Let colors be list containing "red", "blue", "green"
Let color count be length of colors
Let first color be colors at index 0
Let colors with yellow be colors with "yellow" added
```

### String Operations

```
Let greeting be "Hello, " followed by user name
Let name length be length of user name
Let uppercase name be user name converted to uppercase
```

### Mathematical Operations

```
Let total be price plus tax
Let discounted price be price multiplied by 0.9
Let average be sum of values divided by count of values
```

### I/O Operations

```
Let user input be input with prompt "Enter your name: "
Let file content be read file "data.txt"
Write content to file "output.txt"
```

## Error Handling

Runa provides a try-catch mechanism for error handling:

```
Try:
    Let content be read file "data.txt"
    Display content
Catch file error:
    Display "Could not read file" with message file error
```

### Result Types for Error Handling

```
Type Result[T] is T OR String

Process called "safe_operation" that takes value returns Result[Integer]:
    If value is greater than 0:
        Return value multiplied by 2
    Otherwise:
        Return "Invalid input: value must be positive"
```

## Modules and Imports

Runa supports modular programming:

```
Import module "math"
Import module "http" as "web"
Import function "Calculate Distance" from module "geometry"

Let circumference be math.PI multiplied by diameter
Let response be web.get with url as "https://api.example.com"
```

## AI-Specific Features

### Neural Network Definition

Runa includes specialized syntax for AI model definition:

```
Define neural network "ImageClassifier":
    Input layer accepts 224×224 RGB images
    Use convolutional layers starting with 32 filters
    Double filters at each downsampling
    Include residual connections
    Output layer has 10 classes with softmax activation
```

### Training Configuration

```
Configure training for ImageClassifier:
    Use dataset "flower_images" with 80/20 train/validation split
    Apply random horizontal flips and color shifts for augmentation
    Use Adam optimizer with learning rate 0.001
    Train for 50 epochs or until validation accuracy stops improving
    Save best model based on validation accuracy
```

### Model Usage

```
Let model be load neural network "ImageClassifier" from "models/classifier.model"
Let image be load image from "flower.jpg"
Let prediction be model predict with image as image
Display "Classification:" with message prediction
```

## Knowledge Integration

Runa allows direct integration with knowledge representations:

```
Let cancer treatments be knowledge.query("effective treatments for lung cancer")
For each treatment in cancer treatments:
    Display treatment.name with message treatment.effectiveness
```

## AI-to-AI Communication Annotations

Runa includes a comprehensive annotation system for AI-to-AI communication:

### Reasoning Annotations

```
@Reasoning:
    Using quicksort here because the dataset is small and partially ordered,
    making it more efficient than merge sort in this specific case.
@End_Reasoning

Process called "Sort Data" that takes data:
    # Implementation follows
```

### Implementation Blocks

```
@Implementation:
    Process called "Binary Search" that takes array and target:
        Let low be 0
        Let high be length of array minus 1
        
        While low is less than or equal to high:
            Let mid be (low plus high) divided by 2
            If array at index mid is equal to target:
                Return mid
            Otherwise if array at index mid is less than target:
                Set low to mid plus 1
            Otherwise:
                Set high to mid minus 1
        
        Return -1
@End_Implementation
```

### Uncertainty Representation

```
Let sorting algorithm be ?[QuickSort, MergeSort, HeapSort] with confidence 0.8

Process called "Choose Algorithm" that takes data size:
    If data size is less than 100:
        Return ?InsertionSort  # Lower confidence for this choice
    Otherwise:
        Return QuickSort with data as data
```

### Task Specifications

```
@Task:
    objective: "Create a web scraper for financial data"
    constraints: ["Must respect robots.txt", "Rate-limited to 1 request/second"]
    input_format: "URL list"
    output_format: "CSV with date, price, volume columns"
    target_language: "Python"
    priority: "Efficiency"
@End_Task
```

### Knowledge References

```
@KnowledgeReference:
    concept: "Transformer Architecture"
    reference_id: "arxiv:1706.03762"
    version: "as of 2023-10"
@End_KnowledgeReference

Process called "Build Transformer" that takes config:
    # Implementation based on referenced paper
```

### Verification Blocks

```
@Verify:
    Assert mean is greater than or equal to minimum value in data
    Assert mean is less than or equal to maximum value in data
    Assert standard_deviation is greater than or equal to 0
@End_Verify

Process called "Calculate Statistics" that takes data:
    # Statistical calculations with built-in verification
```

## Operator Precedence

Operators in Runa follow this precedence (highest to lowest):
1. Function calls and member access
2. Type assertions and conversions
3. Unary operators (not, negation)
4. Multiplication and division
5. Addition and subtraction
6. Comparison operators (is greater than, is equal to, etc.)
7. Type checking (is of type)
8. Logical AND
9. Logical OR
10. Pipeline operator (|>)

## Scoping Rules

1. **Block-level scoping**: Variables declared within a block are only accessible within that block and its nested blocks
2. **Function-level scoping**: Parameters are accessible throughout the function body
3. **Global scope**: Top-level declarations are accessible throughout the program
4. **No variable shadowing**: Inner scopes cannot redefine variables from outer scopes
5. **Lexical scoping**: Inner functions can access variables from their containing function
6. **Type scope**: Generic type parameters are scoped to their definition

## Memory Management

Runa uses automatic memory management:
- Garbage collection handles memory cleanup
- Reference counting for immediate cleanup of large objects
- No manual memory management required
- Deterministic cleanup for resources (files, network connections)

## Concurrency Model

Runa's concurrency is built on the async/await model:
- Cooperative multitasking
- Event loop for I/O operations
- No shared mutable state between async tasks
- Message passing for communication between tasks

## Performance Considerations

- Type annotations can improve performance
- Generic types have no runtime overhead
- Pattern matching is optimized by the compiler
- Functional constructs are optimized for performance
- AI-specific operations can utilize hardware acceleration

## Best Practices

1. **Use type annotations for complex functions**
2. **Prefer pattern matching over multiple if-else chains**
3. **Use async/await for I/O-bound operations**
4. **Leverage the type system for domain modeling**
5. **Use annotations for AI-to-AI communication**
6. **Structure code with clear separation of concerns**
7. **Prefer functional constructs where appropriate**

---

This document serves as a comprehensive reference for the Runa programming language, covering all core features, advanced language constructs, AI-specific capabilities, and the AI-to-AI communication system. For practical examples and tutorials, please refer to the "Getting Started with Runa" guide.

## Quick Reference Examples

### Variable Declaration and Basic Operations
```
Let user name be "Alex"
Let user age be 28
Set user name to user name followed by " Smith"
```

### Control Flow
```
If user age is greater than 21:
    Display "Access granted"
Otherwise:
    Display "Access denied"
    Display "Come back in" with message (21 minus user age) followed by " years"
```

### Function Definition
```
Process called "Calculate Area" that takes width and height returns Float:
    Return width multiplied by height
```

### Pattern Matching
```
Match response status:
    When 200:
        Display "Success"
    When 404:
        Display "Not found"
    When status If status is greater than or equal to 500:
        Display "Server error"
    When _:
        Display "Unknown status"
```

### Asynchronous Operations
```
Async Process called "Fetch User Data" that takes user_id:
    Let user be await database.get_user with id as user_id
    Let permissions be await database.get_permissions with user as user
    Return dictionary with:
        "user" as user
        "permissions" as permissions
```
