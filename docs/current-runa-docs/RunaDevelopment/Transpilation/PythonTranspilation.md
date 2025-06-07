# Python Transpilation in Runa

Python is the primary target language for Runa, offering the most complete feature support. This guide covers the specifics of transpiling Runa code to Python.

## Table of Contents

1. [Overview](#overview)
2. [Language Mappings](#language-mappings)
3. [Python-Specific Features](#python-specific-features)
4. [Configuration Options](#configuration-options)
5. [Performance Considerations](#performance-considerations)
6. [Interoperability](#interoperability)
7. [Advanced Features](#advanced-features)
8. [Troubleshooting](#troubleshooting)

## Overview

Python transpilation converts Runa source code to Python 3.8+ compatible code. The generated Python code maintains semantic equivalence while leveraging Python's ecosystem.

### Benefits of Python as a Target

- **Ecosystem Access**: Access to PyPI and thousands of Python libraries
- **Readability**: Python's clean syntax aligns well with Runa's design goals
- **AI & ML Support**: Excellent integration with Python's AI/ML ecosystem
- **Cross-Platform**: Works on all major operating systems
- **Community**: Large community and abundant resources

### Requirements

- Python 3.8 or higher installed
- Required Python packages (automatically installed with Runa):
  - `runalang-runtime`: Core runtime support
  - `typing_extensions`: Extended type hints
  - `asyncio`: Asynchronous programming support

## Language Mappings

### Basic Constructs

| Runa Construct | Python Equivalent |
|----------------|-------------------|
| `Process called name(params)` | `def name(params):` |
| `Let variable = value` | `variable = value` |
| `Constant NAME = value` | `NAME = value` |
| `If condition Then` | `if condition:` |
| `Otherwise If condition Then` | `elif condition:` |
| `Otherwise` | `else:` |
| `End If` | (indentation) |
| `For item in collection` | `for item in collection:` |
| `While condition` | `while condition:` |
| `Return value` | `return value` |
| `Break` | `break` |
| `Continue` | `continue` |
| `Print(value)` | `print(value)` |
| `Try...Catch...Finally` | `try:...except:...finally:` |

### Data Types

| Runa Type | Python Type |
|-----------|-------------|
| `Number` | `float` or `int` (context-dependent) |
| `Integer` | `int` |
| `Decimal` | `float` |
| `Text` | `str` |
| `Boolean` | `bool` |
| `List of Type` | `List[Type]` |
| `Map of KeyType to ValueType` | `Dict[KeyType, ValueType]` |
| `Optional Type` | `Optional[Type]` |
| `Any` | `Any` |
| `Null` | `None` |
| `Tuple(Type1, Type2, ...)` | `Tuple[Type1, Type2, ...]` |
| `Structure` | `dataclass` or `class` |

### Object-Oriented Programming

| Runa Construct | Python Equivalent |
|----------------|-------------------|
| `Structure called Name` | `@dataclass\nclass Name:` |
| `Method called name(self, params)` | `def name(self, params):` |
| `Property name of type Type` | `name: Type` |
| `Static Method called name(params)` | `@staticmethod\ndef name(params):` |
| `Inherit from BaseClass` | `class Name(BaseClass):` |

### Functional Programming

| Runa Construct | Python Equivalent |
|----------------|-------------------|
| `Map function over list` | `map(function, list)` or list comprehension |
| `Filter list by condition` | `filter(condition, list)` or list comprehension |
| `Reduce list using function` | `functools.reduce(function, list)` |
| `Lambda (params) => expression` | `lambda params: expression` |

### Error Handling

| Runa Construct | Python Equivalent |
|----------------|-------------------|
| `Try` | `try:` |
| `Catch error of ErrorType as name` | `except ErrorType as name:` |
| `Catch any error as name` | `except Exception as name:` |
| `Finally` | `finally:` |
| `Throw new ErrorType(message)` | `raise ErrorType(message)` |

### Asynchronous Programming

| Runa Construct | Python Equivalent |
|----------------|-------------------|
| `Async Process called name(params)` | `async def name(params):` |
| `Await expression` | `await expression` |
| `Promise of Type` | `Coroutine[Any, Any, Type]` |

## Python-Specific Features

### Type Annotations

By default, Runa adds Python type annotations to the transpiled code:

```
# Runa code
Process called add(a as Number, b as Number) returns Number
    Return a + b
End Process

# Transpiled Python
def add(a: float, b: float) -> float:
    return a + b
```

### Standard Library Mapping

Runa's standard library maps to Python's standard library where possible:

```
# Runa code
Let current_time = DateTime.now()
Let formatted_time = DateTime.format(current_time, "yyyy-MM-dd")

# Transpiled Python
import datetime
current_time = datetime.datetime.now()
formatted_time = current_time.strftime("%Y-%m-%d")
```

### Context Managers

Runa's `Using` statement maps to Python's context managers:

```
# Runa code
Using file = File.open("example.txt", "read") Do
    Let content = file.read_all()
    Print(content)
End Using

# Transpiled Python
with open("example.txt", "r") as file:
    content = file.read()
    print(content)
```

### Decorators

Runa's annotations map to Python decorators:

```
# Runa code
@Deprecated("Use new_function instead")
Process called old_function()
    Print("This function is deprecated")
End Process

# Transpiled Python
@deprecated("Use new_function instead")
def old_function():
    print("This function is deprecated")
```

## Configuration Options

### Python Version Targeting

You can specify the target Python version:

```bash
runa compile --target python --python-version 3.9 my_program.runa
```

In configuration file:

```json
{
  "transpilation": {
    "target": "python",
    "python_options": {
      "version": "3.9"
    }
  }
}
```

### Type Annotations

Control type annotation generation:

```json
{
  "transpilation": {
    "target": "python",
    "python_options": {
      "type_annotations": true,
      "from_future_annotations": true
    }
  }
}
```

### Style Options

Control code style in the output:

```json
{
  "transpilation": {
    "target": "python",
    "python_options": {
      "line_length": 88,
      "use_dataclasses": true,
      "docstrings": true,
      "docstring_style": "google"
    }
  }
}
```

### Import Management

Control import handling:

```json
{
  "transpilation": {
    "target": "python",
    "python_options": {
      "import_style": "grouped",
      "standard_lib_imports_first": true
    }
  }
}
```

## Performance Considerations

### JIT Compilation

Enable JIT compilation for performance-critical sections:

```
# Runa code
@JIT
Process called compute_intensive(data as List of Number) returns Number
    Let sum = 0
    For item in data
        sum = sum + item * item
    End For
    Return sum
End Process

# Transpiled Python with JIT
import numba
@numba.jit(nopython=True)
def compute_intensive(data):
    sum = 0
    for item in data:
        sum = sum + item * item
    return sum
```

### Parallelism

Runa's parallel constructs map to Python's multiprocessing or threading:

```
# Runa code
Let results = Parallel.map(process_item, items)

# Transpiled Python
from multiprocessing import Pool
with Pool() as pool:
    results = pool.map(process_item, items)
```

### Numpy Integration

Vectorized operations map to NumPy:

```
# Runa code
Let matrix_a = [[1, 2], [3, 4]]
Let matrix_b = [[5, 6], [7, 8]]
Let matrix_c = Matrix.multiply(matrix_a, matrix_b)

# Transpiled Python
import numpy as np
matrix_a = np.array([[1, 2], [3, 4]])
matrix_b = np.array([[5, 6], [7, 8]])
matrix_c = np.matmul(matrix_a, matrix_b)
```

## Interoperability

### Using Python Libraries

Runa provides direct access to Python libraries:

```
# Runa code
Import Python "requests" as http
Import Python "pandas" as pd

Process called fetch_data(url as Text) returns Any
    Let response = http.get(url)
    Let df = pd.DataFrame(response.json())
    Return df
End Process

# Transpiled Python
import requests as http
import pandas as pd

def fetch_data(url):
    response = http.get(url)
    df = pd.DataFrame(response.json())
    return df
```

### Native Python Code Blocks

Use inline Python code when needed:

```
# Runa code
Process called complex_calculation(data as List of Number) returns Number
    Python {
        import numpy as np
        result = np.fft.fft(data)
        magnitude = np.abs(result)
        return np.max(magnitude)
    }
End Process

# Transpiled Python
def complex_calculation(data):
    import numpy as np
    result = np.fft.fft(data)
    magnitude = np.abs(result)
    return np.max(magnitude)
```

## Advanced Features

### Metaprogramming

Runa's metaprogramming features map to Python's introspection capabilities:

```
# Runa code
Process called generate_getter_setter(class_obj as Type, property_name as Text)
    Reflect.add_method(
        class_obj,
        "get_" + property_name,
        Lambda (self) => Reflect.get_property(self, property_name)
    )
    Reflect.add_method(
        class_obj,
        "set_" + property_name,
        Lambda (self, value) => Reflect.set_property(self, property_name, value)
    )
End Process

# Transpiled Python
def generate_getter_setter(class_obj, property_name):
    setattr(class_obj, f"get_{property_name}", 
            lambda self: getattr(self, property_name))
    setattr(class_obj, f"set_{property_name}", 
            lambda self, value: setattr(self, property_name, value))
```

### AI Integration

Runa's AI features map to Python's AI libraries:

```
# Runa code
Import AI.MachineLearning as ML

Process called train_model(data as DataFrame, target as Text) returns Model
    Let model = ML.create_classifier("random_forest")
    model.train(data, target, validation_split=0.2)
    Return model
End Process

# Transpiled Python
from runa.ai.machine_learning import create_classifier

def train_model(data, target):
    model = create_classifier("random_forest")
    model.train(data, target, validation_split=0.2)
    return model
```

### Python-Specific Optimizations

Runa can apply Python-specific optimizations:

```
# Runa code
Process called process_large_dataset(filename as Text) returns Statistics
    Let data = File.read_lines(filename)
    Let numbers = Map Number.parse over data
    Let stats = Statistics.from_data(numbers)
    Return stats
End Process

# Transpiled Python (optimized)
def process_large_dataset(filename):
    from statistics import mean, stdev, median
    # Using generator expressions to save memory
    with open(filename, 'r') as f:
        numbers = (float(line.strip()) for line in f)
        # Efficient statistics computation using collections.Counter or numpy
        from numpy import array
        num_array = array(list(numbers))
        return {
            'mean': num_array.mean(),
            'median': median(num_array),
            'std_dev': num_array.std(),
            'min': num_array.min(),
            'max': num_array.max()
        }
```

## Troubleshooting

### Common Issues

#### Type Annotation Errors

**Issue**: Type annotations causing errors in older Python versions.

**Solution**: Add `from __future__ import annotations` or disable type annotations.

```json
{
  "transpilation": {
    "target": "python",
    "python_options": {
      "from_future_annotations": true
    }
  }
}
```

#### Module Not Found Errors

**Issue**: Missing Python dependencies.

**Solution**: Ensure all required dependencies are listed in `requirements.txt` or include them in the runtime library.

#### Performance Issues

**Issue**: Slow execution of computation-heavy code.

**Solution**: Use the `@JIT` annotation on compute-intensive processes or manually optimize the transpiled code.

#### Asynchronous Code Issues

**Issue**: Async functions not working as expected.

**Solution**: Ensure you're using the correct event loop and `await` all async operations.

### Debugging Transpiled Code

To debug the transpiled Python code:

1. Generate Python code with source maps:
   ```bash
   runa compile --source-maps my_program.runa
   ```

2. Use Python's debugging tools (pdb, IDE debuggers) on the transpiled code.

3. Add debug mode to see the relationship between Runa code and Python code:
   ```bash
   runa compile --debug-comments my_program.runa
   ```

   This adds comments showing the original Runa code:
   ```python
   # From Runa: Process called calculate_sum(a as Number, b as Number) returns Number
   def calculate_sum(a, b):
       # From Runa: Return a + b
       return a + b
   ```

### Get Help

If you're still having issues:

1. Check the [Python transpilation FAQ](../FAQ/PythonTranspilation.md)
2. Run the validator to check your Runa code for issues:
   ```bash
   runa validate my_program.runa
   ```
3. Reach out to the community via:
   - [GitHub Issues](https://github.com/runalang/runa/issues)
   - [Discord Community](https://discord.gg/runalang)
   - [StackOverflow with the 'runalang' tag](https://stackoverflow.com/questions/tagged/runalang) 