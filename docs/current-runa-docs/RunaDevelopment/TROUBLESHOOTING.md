# Troubleshooting Guide for Runa

This document provides solutions for common issues you might encounter when using the Runa programming language.

## Installation Issues

### Package Not Found

If you encounter a "Package not found" error when running Runa:

```bash
runa: command not found
```
Make sure you've installed the package correctly:

```bash
pip install -e .
```
Or check if the Python scripts directory is in your PATH.
### Dependencies Missing
If you see errors about missing dependencies:
```bash
ImportError: No module named 'ply'
```
Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Syntax Errors
### Indentation Errors
Runa uses significant indentation like Python. Make sure your indentation is consistent:
```
# Incorrect
If x is greater than 10:
Display "x is greater than 10"  # Missing indentation

# Correct
If x is greater than 10:
    Display "x is greater than 10"
```

### Missing Colon

Block statements must end with a colon:
```
# Incorrect
If x is greater than 10
    Display "x is greater than 10"

# Correct
If x is greater than 10:
    Display "x is greater than 10"
```

### Process (Function) Definition
Process definitions require specific syntax:
```
# Incorrect
Process add that takes a and b:
    Return a plus b

# Correct
Process called "add" that takes a and b:
    Return a plus b
```

## Semantic Errors

### Undefined Variables
Make sure variables are defined before use:
```
# This will cause an error
Display x  # x is not defined

# Correct approach
Let x be 10
Display x
```

### Function call Syntax
Functions must be called with the correct syntax:
```
# Incorrect
add(a, b)

# Correct
add with a and b
```

### Type Errors
While Runa has type inference, type mismatches can still occur:
```
# This might cause an error at runtime
Let x be "hello"
Let y be x plus 5  # Trying to add a string and a number
```

## Runtime Errors

### Division by Zero
Handle potential division by zero:
```
# Safe approach
If divisor is not equal to 0:
    Let result be dividend divided by divisor
Otherwise:
    Let result be 0
```

### Index Out of Range
Make sure list indices are valid:
```
# Safe approach
If index is less than length of my_list:
    Let item be my_list at index index
Otherwise:
    Display "Index out of range"
```

## Command Line Issues

### REPL Not Working
If the REPL doesn't start or behaves unexpectedly:

1. Make sure your terminal supports interactive input
2. Check if Python's readline module is available on your system
3. Try running with python -m runa.cli repl instead of just runa repl

### File Not Found
If you get a "File not found" error:
```
Error: File 'myprogram.runa' does not exist
```

Make sure:

1. The file exists in the current directory
2. You've spelled the filename correctly
3. You have read permissions for the file

### Getting Help
If you encounter an issue not covered in this guide:

1. Check the Runa documentation
2. Look for similar issues in the project repository
3. Create a new issue with a detailed description of the problem