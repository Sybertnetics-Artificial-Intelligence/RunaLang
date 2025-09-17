# Getting Started with Runa

## 5-Minute Quick Start Tutorial

This tutorial will get you up and running with Runa in just 5 minutes!

## Step 1: Installation (1 minute)

Make sure you have Python 3.8+ installed, then:

```bash
# Clone the repository
git clone https://github.com/sybertneticsaisolutions/runa
cd runa

# Install Runa
pip install -e .

# Test the installation
python -m runa.cli --help
```

You should see the Runa CLI help message.

## Step 2: Your First Program (1 minute)

Create a file called `greeting.runa`:

```runa
Let name be "World"
Display "Hello, " followed by name followed by "!"
```

Compile it:

```bash
python -m runa.cli compile greeting.runa -t python
```

Run it:

```bash
python greeting.py
```

Output: `Hello, World!`

## Step 3: Variables and Math (1 minute)

Create `calculator.runa`:

```runa
Let a be 10
Let b be 5

Let sum be a plus b
Let difference be a minus b
Let product be a multiplied by b
Let quotient be a divided by b

Display "Sum: " followed by sum
Display "Difference: " followed by difference  
Display "Product: " followed by product
Display "Quotient: " followed by quotient
```

Compile and run:

```bash
python -m runa.cli compile calculator.runa -t python
python calculator.py
```

## Step 4: Control Flow (1 minute)

Create `conditions.runa`:

```runa
Let score be 85

If score is greater than 90:
    Display "Grade: A"
Otherwise if score is greater than 80:
    Display "Grade: B"
Otherwise if score is greater than 70:
    Display "Grade: C"
Otherwise:
    Display "Grade: F"

For i from 1 to 5:
    Display "Count: " followed by i
```

Compile and run to see conditional logic and loops in action.

## Step 5: Functions (1 minute)

Create `functions.runa`:

```runa
Process called "greet person" that takes name as String returns String:
    Return "Hello, " followed by name followed by "!"

Process called "calculate area" that takes width as Integer and height as Integer returns Integer:
    Return width multiplied by height

Let greeting be Greet Person with name as "Alice"
Display greeting

Let area be Calculate Area with width as 10 and height as 5
Display "Area: " followed by area
```

Compile and run to see functions in action.

## What You've Learned

In just 5 minutes, you've learned:

How to install and use Runa  
Basic variable declaration and math  
Natural language syntax for operations  
Conditional statements (if/otherwise)  
Loops (for-range)  
Function definition and calling  

## Next Steps

Now that you've got the basics down:

1. **Explore More Features**: Check out the [User Guide](USER_GUIDE.md) for advanced features like:
   - Pattern matching
   - Error handling
   - Async/await
   - Modules and imports

2. **Try Examples**: Look at the [examples/](../examples/) directory for real-world Runa programs

3. **Learn the Type System**: Runa has a powerful type system with generics, unions, and optionals

4. **Build Something**: Create your own Runa project!

## Common Patterns

### Working with Lists

```runa
Let numbers be list containing 1, 2, 3, 4, 5
Let total be 0

For each number in numbers:
    Set total to total plus number

Display "Total: " followed by total
```

### Error Handling

```runa
Try:
    Let result be 10 divided by 0
Catch as error:
    Display "Error: " followed by error
```

### Pattern Matching

```runa
Let value be 42

Match value:
    Case 0:
        Display "Zero"
    Case x If x is greater than 0:
        Display "Positive"
    Case _:
        Display "Negative"
```

## Tips for Success

1. **Think in English**: Write code like you're explaining it to someone
2. **Use Descriptive Names**: `user_age` is better than `x`
3. **Leverage the Type System**: Use type annotations for clarity
4. **Start Simple**: Begin with basic programs and gradually add complexity

## Troubleshooting

**Compilation Error?**
- Check syntax against the examples
- Make sure all variable names are declared before use
- Verify proper indentation

**Runtime Error?**
- Look at the generated Python code to debug
- Use the `validate` command to check semantics

**Need Help?**
- Check the [User Guide](USER_GUIDE.md)
- Look at [examples/](../examples/)
- Ask questions in our community

## Ready for More?

You're now ready to explore Runa's full potential! Continue with:

- [User Guide](USER_GUIDE.md) - Complete language features
- [Language Reference](LANGUAGE_REFERENCE.md) - Detailed syntax
- [Examples](../examples/) - Real-world programs
- [Standard Library](../stdlib/) - Built-in functionality

Welcome to the Runa community! 🎉