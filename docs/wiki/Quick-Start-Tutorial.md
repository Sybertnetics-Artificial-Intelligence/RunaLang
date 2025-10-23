# Quick Start Tutorial

Welcome to Runa! This tutorial will get you up and running with the basics of Runa programming in just a few minutes.

## Prerequisites

- Runa compiler installed (see [Installation Guide](Installation-Guide))
- A text editor or IDE
- Basic understanding of programming concepts

## Your First Program

Let's start with the classic "Hello, World!" program:

```runa
Note: A simple greeting program
Display "Hello, World!"
```

Save this as `hello.runa` and compile it:

```bash
runac hello.runa -o hello
./hello
```

Output:
```
Hello, World!
```

## Variables and Basic Operations

Runa uses the `Let` keyword to declare variables:

```runa
Note: Working with variables
Let name be "Alice"
Let age be 25
Let height be 5.6

Display "Name: " joined with name
Display "Age: " joined with age as text
Display "Height: " joined with height as text
```

## Arithmetic Operations

Runa uses natural language for operations:

```runa
Note: Basic arithmetic
Let x be 10
Let y be 5

Let sum be x plus y
Let difference be x minus y
Let product be x multiplied by y
Let quotient be x divided by y

Display "Sum: " joined with sum as text
Display "Difference: " joined with difference as text
Display "Product: " joined with product as text
Display "Quotient: " joined with quotient as text
```

## Conditional Logic

Use `If` and `Otherwise` for control flow:

```runa
Note: Checking if someone can vote
Let age be 18

If age is greater than or equal to 18:
    Display "You can vote!"
Otherwise:
    Display "You cannot vote yet."
```

## Multiple Conditions with When

For multiple conditions, use `When`:

```runa
Note: Grading system
Let score be 85

When score is greater than or equal to 90:
    Display "Grade: A"
When score is greater than or equal to 80:
    Display "Grade: B"
When score is greater than or equal to 70:
    Display "Grade: C"
When score is greater than or equal to 60:
    Display "Grade: D"
Otherwise:
    Display "Grade: F"
```

## Loops

### For Loop

```runa
Note: Counting from 1 to 5
For i in range from 1 to 5:
    Display i as text
```

### While Loop

```runa
Note: Countdown
Let count be 5

While count is greater than 0:
    Display count as text
    Let count be count minus 1

Display "Liftoff!"
```

## Functions (Processes)

Define reusable code with `Process`:

```runa
Note: Define a function to calculate area
Process called "calculate area" that takes width and height:
    Let area be width multiplied by height
    Return area

Note: Use the function
Let room area be calculate area with 10 and 12
Display "Room area: " joined with room area as text
```

## Working with Collections

### Lists

```runa
Note: Creating and using lists
Let fruits be list containing "apple", "banana", "cherry"

Display "First fruit: " joined with fruits at 0

Note: Add an item
Add "date" to fruits

Note: Iterate over the list
For each fruit in fruits:
    Display fruit
```

### Maps (Dictionaries)

```runa
Note: Creating a map
Let person be map with:
    "name" as "Bob"
    "age" as 30
    "city" as "New York"

Display "Name: " joined with person at "name"
Display "Age: " joined with person at "age" as text
```

## User Input

Get input from the user:

```runa
Note: Interactive greeting
Let user name be input with prompt "What is your name? "
Let greeting be "Hello, " joined with user name followed by "!"
Display greeting
```

## Putting It All Together

Here's a complete example that combines multiple concepts:

```runa
Note: Simple number guessing game
Process called "play game":
    Let secret number be 42
    Let attempts be 0
    Let max attempts be 5

    Display "I'm thinking of a number between 1 and 100!"

    While attempts is less than max attempts:
        Let guess be input with prompt "Enter your guess: " as integer
        Let attempts be attempts plus 1

        When guess is equal to secret number:
            Display "Congratulations! You guessed it in " joined with attempts as text joined with " attempts!"
            Return
        When guess is less than secret number:
            Display "Too low! Try again."
        Otherwise:
            Display "Too high! Try again."

    Display "Sorry, you've run out of attempts. The number was " joined with secret number as text

Note: Start the game
play game
```

## Syntax Modes

Runa supports two main syntax modes:

### Canon Mode (Default)
```runa
Let result be x multiplied by y
If result is greater than 100:
    Display "Large result!"
```

### Developer Mode
```runa
Let result be x * y
If result > 100:
    Display "Large result!"
```

Both are valid and compile to the same code! See [Syntax Modes](Syntax-Modes) for more details.

## Next Steps

Now that you know the basics, explore:

- [Variables and Data Types](Variables-and-Data-Types) - Deep dive into Runa's type system
- [Functions and Processes](Functions-and-Processes) - Advanced function features
- [Standard Library Overview](Standard-Library-Overview) - Built-in functionality
- [Code Examples](Business-Logic-Examples) - Real-world applications

## Common Mistakes

### 1. Forgetting "Let" for variables
```runa
# Wrong
x be 10

# Correct
Let x be 10
```

### 2. Case sensitivity in identifiers
```runa
# These are DIFFERENT variables:
Let Calculate Area be 10
Let Calculate area be 20
```

### 3. Mixing modes
```runa
# Don't mix Canon and Developer mode operators
Let x be y * z  # Mixed! Use either 'multiplied by' or '*'
```

## Getting Help

If you run into issues:

- Check the [FAQ](FAQ)
- Visit [Troubleshooting](Troubleshooting)
- Ask in [GitHub Discussions](https://github.com/Sybertnetics-Artificial-Intelligence/RunaLang/discussions)
- Join our [Discord community](https://discord.gg/sybertnetics-runa)

---

**Next**: [Variables and Data Types](Variables-and-Data-Types)
