# Getting Started with Runa

## Introduction

Welcome to Runa, a programming language designed to bridge human thought patterns with machine execution. This guide will help you get started with Runa programming, covering basic concepts and providing practical examples.

## Installation

*Note: The installation procedure will be finalized in Phase 5 of development.*

For development purposes, you can install Runa using:

```bash
# Future installation command will go here
pip install runa-lang
```

## Your First Runa Program

Let's start with the traditional "Hello, World!" program:

```
# hello_world.runa
Display "Hello, World!"
```

Run this program using:

```bash
runa hello_world.runa
```

## Basic Concepts

### Variables and Data Types

Runa uses natural language for variable declarations:

```
# Variables example
Let name be "Alex"
Let age be 28
Let is student be true
Let grades be list containing 85, 92, 78, 95
```

### Working with Variables

```
# Modify variables
Set age to 29
Set name to name followed by " Smith"

# Display variables
Display "Name:" with message name
Display "Age:" with message age
```

### Conditional Logic

```
# Age verification example
Let minimum age be 21

If age is greater than minimum age:
    Display "Access granted"
Otherwise:
    Display "Access denied"
    Display "Come back in" with message (minimum age minus age) followed by " years"
```

### Loops

```
# List iteration example
Let fruits be list containing "apple", "banana", "cherry", "date"

For each fruit in fruits:
    Display fruit

# Counting example
Let count be 1
While count is less than or equal to 5:
    Display count
    Set count to count plus 1
```

## Functions (Processes)

### Defining and Calling Functions

```
# Temperature conversion function
Process called "Convert Celsius to Fahrenheit" that takes celsius:
    Return (celsius multiplied by 9/5) plus 32

# Using the function
Let temperature celsius be 25
Let temperature fahrenheit be Convert Celsius to Fahrenheit with celsius as temperature celsius
Display temperature celsius followed by "°C equals" with message temperature fahrenheit followed by "°F"
```

### Functions with Multiple Parameters

```
# Rectangle area calculation
Process called "Calculate Rectangle Area" that takes width and height:
    Return width multiplied by height

Let area be Calculate Rectangle Area with width as 5 and height as 3
Display "The rectangle area is" with message area
```

## Working with Collections

### Lists

```
# List operations
Let numbers be list containing 10, 20, 30, 40, 50

# Accessing elements
Let first number be numbers at index 0
Let last number be numbers at index (length of numbers minus 1)

# Modifying lists
Add 60 to numbers
Remove value 30 from numbers

# Finding information
Let contains 40 be numbers contains 40
Let position of 20 be index of 20 in numbers
```

### Dictionaries

```
# Creating a dictionary
Let person be dictionary with:
    "name" as "Alex"
    "age" as 28
    "city" as "Seattle"

# Accessing dictionary values
Let person name be person["name"]
Let person city be person["city"]

# Modifying dictionaries
Set person["job"] to "Developer"
```

## Error Handling

```
# Reading a file safely
Try:
    Let content be read file "data.txt"
    Display content
Catch file error:
    Display "Error reading file:" with message file error
```

## Building a Simple Application

Let's build a simple temperature conversion application:

```
# temperature_converter.runa

Process called "Convert Celsius to Fahrenheit" that takes celsius:
    Return (celsius multiplied by 9/5) plus 32

Process called "Convert Fahrenheit to Celsius" that takes fahrenheit:
    Return (fahrenheit minus 32) multiplied by 5/9

# Main program
Display "Temperature Converter"
Display "------------------------"

Let choice be input with prompt "Convert from (C)elsius or (F)ahrenheit? "

If choice is equal to "C" or choice is equal to "c":
    Let celsius be convert to number(input with prompt "Enter temperature in Celsius: ")
    Let fahrenheit be Convert Celsius to Fahrenheit with celsius as celsius
    Display celsius followed by "°C equals" with message fahrenheit followed by "°F"
Otherwise if choice is equal to "F" or choice is equal to "f":
    Let fahrenheit be convert to number(input with prompt "Enter temperature in Fahrenheit: ")
    Let celsius be Convert Fahrenheit to Celsius with fahrenheit as fahrenheit
    Display fahrenheit followed by "°F equals" with message celsius followed by "°C"
Otherwise:
    Display "Invalid choice. Please enter C or F."
```

## AI Model Example

Here's an example of defining a simple image classifier:

```
# image_classifier.runa

Define neural network "FlowerClassifier":
    Input layer accepts 224×224 RGB images
    Use convolutional layers starting with 32 filters
    Double filters at each downsampling
    Include residual connections
    Output layer has 5 classes with softmax activation

Configure training for FlowerClassifier:
    Use dataset "flower_dataset" with 80/20 train/validation split
    Apply random horizontal flips for augmentation
    Use Adam optimizer with learning rate 0.001
    Train for 30 epochs or until validation accuracy stops improving
    Save best model based on validation accuracy

# Using the model
Let model be load neural network "FlowerClassifier" from "models/flower_classifier.model"
Let image be load image from "flower.jpg"
Let prediction be model predict with image as image
Display "This flower is most likely a" with message prediction[0].label
```

## Next Steps

Now that you've learned the basics of Runa, here are some suggestions for further exploration:

1. Explore the standard library functions
2. Learn about modules and code organization
3. Study more advanced features like knowledge integration
4. Check out the complete language reference documentation

Happy coding with Runa!