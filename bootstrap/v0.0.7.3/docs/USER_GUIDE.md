# Copyright 2025 Sybertnetics Artificial Intelligence Solutions
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# Runa v0.0.7.3 Complete User Guide

> **Welcome to Runa v0.0.7.3!** This is your complete guide to using the Runa programming language compiler until the full language is ready for production.

## 🚀 Quick Start

### Prerequisites
- Linux/Unix environment (tested on Ubuntu/WSL2)
- GCC compiler
- Make utility

### Your First Runa Program

1. **Create a simple program** (`hello.runa`):
```runa
Process called "main" takes argc as Integer, argv as Integer returns Integer:
    Return 42
End Process
```

2. **Compile it**:
```bash
./runac hello.runa hello.s
```

3. **Link and build executable**:
```bash
gcc -o hello hello.s runtime_*.o -no-pie -lm
```

4. **Run it**:
```bash
./hello
echo "Exit code: $?"  # Should show: Exit code: 42
```

**🎉 Congratulations! You've just compiled and run your first Runa program!**

---

## 📚 Complete Language Reference

### Process (Function) Declaration

**Basic Syntax:**
```runa
Process called "function_name" takes param1 as Type, param2 as Type returns ReturnType:
    # Function body
    Return value
End Process
```

**Examples:**

**Simple function with no parameters:**
```runa
Process called "get_answer" returns Integer:
    Return 42
End Process
```

**Function with parameters:**
```runa
Process called "add" takes a as Integer, b as Integer returns Integer:
    Return a plus b
End Process
```

**Main function (program entry point):**
```runa
Process called "main" takes argc as Integer, argv as Integer returns Integer:
    # Your program logic here
    Return 0
End Process
```

### Variables and Assignment

**Declaring variables:**
```runa
Let variable_name be value
Let x be 10
Let name be "Hello World"
```

**Setting variables:**
```runa
Set variable_name to new_value
Set x to 20
Set name to "New Value"
```

### Data Types

| Type | Description | Example |
|------|-------------|---------|
| `Integer` | 64-bit signed integer | `42`, `-100`, `0` |
| `String` | Text data | `"Hello"`, `"World"` |
| Custom Types | User-defined structs | See Type Definitions below |

### Arithmetic Operations

| Operation | Syntax | Example |
|-----------|--------|---------|
| Addition | `a plus b` | `5 plus 3` → `8` |
| Subtraction | `a minus b` | `10 minus 4` → `6` |
| Multiplication | `a multiplied by b` | `6 multiplied by 7` → `42` |
| Division | `a divided by b` | `20 divided by 4` → `5` |
| Modulo | `a modulo b` | `10 modulo 3` → `1` |

**Example:**
```runa
Process called "calculate" returns Integer:
    Let x be 10
    Let y be 20
    Let sum be x plus y
    Let product be x multiplied by y
    Let result be sum plus product
    Return result
End Process
```

### Comparison Operations

| Operation | Syntax | Example |
|-----------|--------|---------|
| Less than | `a is less than b` | `5 is less than 10` |
| Greater than | `a is greater than b` | `15 is greater than 10` |
| Equal to | `a equals b` | `5 equals 5` |
| Not equal | `a is not equal to b` | `5 is not equal to 10` |

### Control Flow

**If Statements:**
```runa
If condition:
    # statements
Otherwise:
    # alternative statements
End If
```

**Example:**
```runa
Process called "max" takes a as Integer, b as Integer returns Integer:
    If a is greater than b:
        Return a
    Otherwise:
        Return b
    End If
End Process
```

**Nested If Statements:**
```runa
Process called "classify" takes x as Integer returns Integer:
    If x is greater than 0:
        If x is less than 10:
            Return 1  # Small positive
        Otherwise:
            Return 2  # Large positive
        End If
    Otherwise:
        Return 0  # Zero or negative
    End If
End Process
```

**While Loops:**
```runa
While condition:
    # statements
    # (make sure to modify condition variables!)
End While
```

**Example (Factorial):**
```runa
Process called "factorial" takes n as Integer returns Integer:
    Let result be 1
    Let i be 1
    While i is less than n plus 1:
        Set result to result multiplied by i
        Set i to i plus 1
    End While
    Return result
End Process
```

### Type Definitions (Structs)

**Basic Syntax:**
```runa
Type called "TypeName":
    field1 as Type1,
    field2 as Type2,
    field3 as Type3
End Type
```

**Example:**
```runa
Type called "Point":
    x as Integer,
    y as Integer
End Type

Type called "Rectangle":
    top_left as Point,
    width as Integer,
    height as Integer
End Type
```

**Using Custom Types:**
```runa
Process called "calculate_area" returns Integer:
    Let rect be Rectangle
    Let point be Point

    # Set up point
    Set point.x to 10
    Set point.y to 20

    # Set up rectangle
    Set rect.top_left to point
    Set rect.width to 30
    Set rect.height to 40

    # Calculate area
    Let area be rect.width multiplied by rect.height
    Return area
End Process
```

---

## 🛠️ Complete Build Process

### Method 1: Manual Compilation (Recommended for Learning)

```bash
# Step 1: Compile Runa source to assembly
./runac your_program.runa your_program.s

# Step 2: Link with runtime and build executable
gcc -o your_program your_program.s runtime_*.o -no-pie -lm

# Step 3: Run your program
./your_program
```

### Method 2: One-Line Build

```bash
./runac program.runa program.s && gcc -o program program.s runtime_*.o -no-pie -lm && ./program
```

### Method 3: Build Script

Create `build_runa.sh`:
```bash
#!/bin/bash
if [ $# -lt 1 ]; then
    echo "Usage: $0 <program.runa> [output_name]"
    exit 1
fi

RUNA_FILE="$1"
OUTPUT="${2:-${RUNA_FILE%.runa}}"
ASM_FILE="${OUTPUT}.s"

echo "Compiling $RUNA_FILE..."
./runac "$RUNA_FILE" "$ASM_FILE" || exit 1

echo "Linking..."
gcc -o "$OUTPUT" "$ASM_FILE" runtime_*.o -no-pie -lm || exit 1

echo "✅ Build successful! Run with: ./$OUTPUT"
```

Make it executable and use:
```bash
chmod +x build_runa.sh
./build_runa.sh my_program.runa
```

---

## 🔧 Runtime Library Functions

Runa v0.0.7.3 includes a comprehensive runtime library. Here are the available functions:

### String Functions

```runa
# Get string length
Let len be string_length("Hello")  # Returns 5

# Get character at position
Let char be string_char_at("Hello", 1)  # Returns 'e'

# Extract substring
Let sub be string_substring("Hello World", 6, 5)  # Returns "World"

# String comparison
Let equal be string_equals("hello", "hello")  # Returns 1 (true)

# String concatenation
Let combined be string_concat("Hello", " World")  # Returns "Hello World"

# Convert string to integer
Let num be string_to_integer("42")  # Returns 42

# Convert integer to string
Let str be integer_to_string(42)  # Returns "42"

# Find substring
Let pos be string_find("Hello World", "World")  # Returns 6

# Replace text
Let new_str be string_replace("Hello World", "World", "Universe")
```

### File I/O Functions

```runa
# Read entire file
Let content be runtime_read_file("data.txt")

# Write to file
Let result be runtime_write_file("output.txt", "Hello World")

# Check if file exists
Let exists be runtime_file_exists("data.txt")  # Returns 1 if exists

# Get file size
Let size be runtime_file_size("data.txt")

# Advanced file operations
Let handle be runtime_file_open("data.txt", "r")
Let line be runtime_file_read_line(handle)
Let close_result be runtime_file_close(handle)
```

### Mathematical Functions

```runa
# Basic arithmetic is built into the language syntax
# Advanced math functions available via runtime:

# Trigonometric functions
Let sine_val be runtime_sin(1.57)    # sin(π/2) ≈ 1
Let cosine_val be runtime_cos(0.0)   # cos(0) = 1

# Logarithmic functions
Let log_val be runtime_log(2.718)    # ln(e) ≈ 1
Let exp_val be runtime_exp(1.0)      # e^1 ≈ 2.718

# Square root
Let sqrt_val be runtime_sqrt(16)     # √16 = 4
```

---

## 📖 Example Programs

### 1. Calculator Program

```runa
Process called "add" takes a as Integer, b as Integer returns Integer:
    Return a plus b
End Process

Process called "multiply" takes a as Integer, b as Integer returns Integer:
    Return a multiplied by b
End Process

Process called "main" takes argc as Integer, argv as Integer returns Integer:
    Let x be 15
    Let y be 25

    Let sum be add(x, y)
    Let product be multiply(x, y)
    Let final_result be sum plus product

    Return final_result  # Should return 415 (40 + 375)
End Process
```

### 2. Fibonacci Calculator

```runa
Process called "fibonacci" takes n as Integer returns Integer:
    If n is less than 2:
        Return n
    Otherwise:
        Let a be 0
        Let b be 1
        Let i be 2
        While i is less than n plus 1:
            Let temp be a plus b
            Set a to b
            Set b to temp
            Set i to i plus 1
        End While
        Return b
    End If
End Process

Process called "main" takes argc as Integer, argv as Integer returns Integer:
    Let result be fibonacci(10)
    Return result  # Returns 55 (10th Fibonacci number)
End Process
```

### 3. Student Grade System

```runa
Type called "Student":
    math_score as Integer,
    english_score as Integer,
    science_score as Integer
End Type

Process called "calculate_average" takes student as Student returns Integer:
    Let total be student.math_score plus student.english_score plus student.science_score
    Let average be total divided by 3
    Return average
End Process

Process called "get_grade" takes average as Integer returns Integer:
    If average is greater than 89:
        Return 65  # ASCII for 'A'
    Otherwise:
        If average is greater than 79:
            Return 66  # ASCII for 'B'
        Otherwise:
            If average is greater than 69:
                Return 67  # ASCII for 'C'
            Otherwise:
                Return 70  # ASCII for 'F'
            End If
        End If
    End If
End Process

Process called "main" takes argc as Integer, argv as Integer returns Integer:
    Let student be Student
    Set student.math_score to 85
    Set student.english_score to 92
    Set student.science_score to 78

    Let avg be calculate_average(student)
    Let grade be get_grade(avg)

    Return grade  # Returns ASCII value of grade
End Process
```

### 4. File Processing Example

```runa
Process called "process_file" takes filename as String returns Integer:
    # Check if file exists
    Let exists be runtime_file_exists(filename)
    If exists equals 0:
        Return 1  # Error: file not found
    End If

    # Read file content
    Let content be runtime_read_file(filename)
    Let length be string_length(content)

    # Create output filename
    Let output_name be string_concat(filename, ".processed")

    # Write processed content
    Let processed be string_concat("Processed: ", content)
    Let write_result be runtime_write_file(output_name, processed)

    Return write_result
End Process

Process called "main" takes argc as Integer, argv as Integer returns Integer:
    Let result be process_file("input.txt")
    Return result
End Process
```

---

## 🧪 Testing Your Programs

### Available Test Files

The `tests/` directory contains many example programs you can study and run:

**Basic Examples:**
- `minimal.runa` - Simplest possible program
- `test_simple.runa` - Basic return value
- `test_arithmetic.runa` - Math operations

**Intermediate Examples:**
- `test_function.runa` - Function definition and calling
- `test_condition.runa` - If/else statements
- `test_loop.runa` - While loops

**Advanced Examples:**
- `test_struct.runa` - Custom types and field access
- `test_file_io.runa` - File reading and writing
- `test_comprehensive.runa` - Multiple language features

### Running Tests

```bash
# Run any test example:
./runac tests/test_function.runa test_output.s
gcc -o test_output test_output.s runtime_*.o -no-pie -lm
./test_output
echo "Exit code: $?"

# Batch test runner:
./tests/run_all_tests.sh
```

---

## 🚨 Common Issues and Solutions

### Issue: "undefined reference to sin/cos/etc"

**Problem:** Mathematical functions not linking properly.

**Solution:** Always include `-lm` flag:
```bash
gcc -o program program.s runtime_*.o -no-pie -lm
```

### Issue: "Segmentation fault"

**Problem:** Usually memory access issues or uninitialized variables.

**Debug steps:**
1. Check that all variables are properly initialized
2. Verify struct field assignments before use
3. Use smaller, simpler test cases to isolate the issue

### Issue: "Error" output with working exit code

**Problem:** This is normal! Runa programs often print "Error" but return the correct exit code.

**Verification:** Always check exit code:
```bash
./program; echo "Exit code: $?"
```

### Issue: Compilation errors

**Common fixes:**
- Ensure proper `End Process` and `End Type` statements
- Check spelling of keywords (`Process`, `Return`, `Integer`, etc.)
- Verify proper indentation and syntax
- Make sure all variables are declared with `Let` before use

---

## 💡 Best Practices

### 1. Code Organization

```runa
# Define types first
Type called "MyType":
    field1 as Integer,
    field2 as String
End Type

# Then helper functions
Process called "helper_function" takes param as Integer returns Integer:
    Return param plus 1
End Process

# Main function last
Process called "main" takes argc as Integer, argv as Integer returns Integer:
    # Your main logic
    Return 0
End Process
```

### 2. Error Handling

```runa
Process called "safe_divide" takes a as Integer, b as Integer returns Integer:
    If b equals 0:
        Return -1  # Error indicator
    Otherwise:
        Return a divided by b
    End If
End Process
```

### 3. Meaningful Variable Names

```runa
# Good:
Let student_count be 25
Let average_score be total_points divided by student_count

# Avoid:
Let x be 25
Let y be total divided by x
```

### 4. Comments for Complex Logic

```runa
Process called "complex_calculation" takes input as Integer returns Integer:
    # Calculate compound interest over 5 years
    Let principal be input
    Let rate be 5  # 5% annual interest
    Let years be 5

    Let i be 0
    While i is less than years:
        # A = P(1 + r/100)
        Let new_amount be principal plus (principal multiplied by rate divided by 100)
        Set principal to new_amount
        Set i to i plus 1
    End While

    Return principal
End Process
```

---

## 🎯 Next Steps

### For Learning Runa:
1. Start with the `test_simple.runa` example
2. Work through arithmetic and function examples
3. Try creating custom types and using them
4. Experiment with file I/O operations
5. Build a small project combining multiple features

### For Development Teams:
1. Create a shared library of common Runa utility functions
2. Establish coding standards for your team
3. Set up automated build scripts
4. Create test suites for your specific domain
5. Document your team's best practices

### Sample Project Ideas:
- **Text Processor:** Read files, count words, replace text
- **Calculator System:** Complex mathematical operations
- **Data Analyzer:** Process CSV-like data files
- **Game Logic:** Simple turn-based game mechanics
- **Utility Scripts:** File organization, data conversion

---

## 🔗 Additional Resources

- **Test Directory:** `tests/` - Many working examples
- **Runtime Headers:** `runtime_*.h` - Complete function documentation
- **Build Examples:** Look at existing `.s` files for assembly output patterns

---

**Happy Coding with Runa v0.0.7.3! 🎉**

*This compiler is stable and ready for development work. Use it confidently while the full Runa language continues development.*