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

## Type System

### Basic Types

- **String**: Text data enclosed in quotes
- **Number**: Numeric values, including integers and floating-point
- **Boolean**: true or false values
- **List**: Ordered collections of items
- **Dictionary**: Key-value collections

### Type Inference

Runa uses type inference to determine variable types:

```
Let age be 30  # Inferred as Number
Let name be "Alex"  # Inferred as String
Let colors be list containing "red", "blue", "green"  # Inferred as List of Strings
```

### Optional Type Annotations

Type annotations can be added for clarity:

```
Let age (Integer) be 30
Let name (String) be "Alex"
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

## Modules and Imports

Runa supports modular programming:

```
Import module "math"
Import function "Calculate Distance" from module "geometry"

Let circumference be math.PI multiplied by diameter
```

## AI-Specific Features

Runa includes specialized syntax for AI model definition:

```
Define neural network "ImageClassifier":
    Input layer accepts 224×224 RGB images
    Use convolutional layers starting with 32 filters
    Double filters at each downsampling
    Include residual connections
    Output layer has 10 classes with softmax activation
```

And for training configuration:

```
Configure training for ImageClassifier:
    Use dataset "flower_images" with 80/20 train/validation split
    Apply random horizontal flips and color shifts for augmentation
    Use Adam optimizer with learning rate 0.001
    Train for 50 epochs or until validation accuracy stops improving
    Save best model based on validation accuracy
```

## Knowledge Integration

Runa allows direct integration with knowledge representations:

```
Let cancer treatments be knowledge.query("effective treatments for lung cancer")
For each treatment in cancer treatments:
    Display treatment.name with message treatment.effectiveness
```

## Operator Precedence

Operators in Runa follow this precedence (highest to lowest):
1. Function calls and member access
2. Unary operators (not, negation)
3. Multiplication and division
4. Addition and subtraction
5. Comparison operators
6. Logical AND
7. Logical OR

## Scoping Rules

1. Block-level scoping: Variables declared within a block are only accessible within that block and its nested blocks
2. Function-level scoping: Parameters are accessible throughout the function body
3. Global scope: Top-level declarations are accessible throughout the program
4. No variable shadowing: Inner scopes cannot redefine variables from outer scopes
5. Lexical scoping: Inner functions can access variables from their containing function

---

This document serves as a reference for the Runa programming language. For practical examples and tutorials, please refer to the "Getting Started with Runa" guide.