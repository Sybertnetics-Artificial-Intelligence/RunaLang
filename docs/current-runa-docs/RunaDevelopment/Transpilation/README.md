# Runa Transpilation

Runa is designed as a "transpiled" language, meaning your Runa code is converted to other programming languages for execution. This approach allows Runa to leverage the ecosystems and performance characteristics of established languages while providing its unique, human-readable syntax and powerful features.

## Table of Contents

1. [Understanding Transpilation](#understanding-transpilation)
2. [Currently Supported Target Languages](#currently-supported-target-languages)
3. [Transpilation Process](#transpilation-process)
4. [Configuring Transpilation](#configuring-transpilation)
5. [Language-Specific Considerations](#language-specific-considerations)
6. [Extending Transpilation](#extending-transpilation)

## Understanding Transpilation

### What is Transpilation?

Transpilation is the process of converting source code from one programming language to another programming language at a similar level of abstraction. Unlike compilation to machine code or bytecode, transpilation produces human-readable code in the target language.

### Benefits of Transpilation in Runa

Runa's transpilation approach provides several advantages:

1. **Ecosystem Access**: Leverage libraries and frameworks from target languages
2. **Deployment Flexibility**: Deploy to any platform that supports the target language
3. **Performance Options**: Choose target languages based on performance needs
4. **Language Evolution**: Add new target languages without changing your Runa code
5. **Interoperability**: Easily interface with existing systems in various languages

### Transpilation vs. Interpretation

While Runa includes an interpreter for development and testing, transpilation offers several benefits for production use:

- **Higher Performance**: Transpiled code typically runs faster than interpreted code
- **Static Analysis**: Issues can be caught during the transpilation phase
- **Optimizations**: Target language compilers apply their own optimizations
- **No Runtime Dependency**: No need for the Runa runtime in production

## Currently Supported Target Languages

### Python

Python is the primary target language with full feature support. All Runa language constructs can be transpiled to Python code.

**Example:**

Runa code:
```
Process called calculate_sum(a, b)
    Let result = a + b
    Return result
End Process

Let total = calculate_sum(5, 10)
Print("The sum is: " + total)
```

Transpiled Python:
```python
def calculate_sum(a, b):
    result = a + b
    return result

total = calculate_sum(5, 10)
print("The sum is: " + str(total))
```

### JavaScript

JavaScript support includes most core Runa features with some limitations in advanced AI capabilities.

**Example:**

Runa code (same as above):
```
Process called calculate_sum(a, b)
    Let result = a + b
    Return result
End Process

Let total = calculate_sum(5, 10)
Print("The sum is: " + total)
```

Transpiled JavaScript:
```javascript
function calculate_sum(a, b) {
    const result = a + b;
    return result;
}

const total = calculate_sum(5, 10);
console.log("The sum is: " + total);
```

### Coming Soon

The following target languages are under development or planned:

- **C/C++**: For high-performance applications and systems programming
- **Java**: For enterprise applications and Android development
- **Rust**: For memory-safe systems programming
- **Go**: For efficient, concurrent server applications
- **TypeScript**: For type-safe web development

## Transpilation Process

### How Transpilation Works

The Runa transpilation process involves these steps:

1. **Lexical Analysis**: Source code is tokenized
2. **Parsing**: Tokens are parsed into an Abstract Syntax Tree (AST)
3. **Semantic Analysis**: The AST is checked for correctness
4. **Target-Specific AST Transformation**: The AST is transformed for the target language
5. **Code Generation**: Target language code is generated from the transformed AST
6. **Optimization**: Target-specific optimizations are applied
7. **Output**: Final transpiled code is produced

### Runtime Library

Most transpilation targets require a Runa runtime library that provides:

- Core functions and utilities
- Standard library implementations
- AI integration capabilities
- Platform-specific adaptations

These runtime components are included automatically when you transpile code.

## Configuring Transpilation

### Command-Line Options

Basic transpilation using the CLI:

```bash
# Transpile to Python (default)
runa compile my_program.runa

# Transpile to JavaScript
runa compile --target javascript my_program.runa

# Specify output file
runa compile --output my_program.py my_program.runa

# Apply specific optimizations
runa compile --optimize performance my_program.runa

# Include runtime libraries
runa compile --include-runtime my_program.runa

# Generate source maps
runa compile --source-maps my_program.runa
```

### Configuration File

You can set transpilation options in `runa.config.json`:

```json
{
  "transpilation": {
    "target": "python",
    "output_dir": "./build",
    "include_runtime": true,
    "source_maps": true,
    "optimization": "performance",
    "preserve_comments": true,
    "target_version": {
      "python": "3.9",
      "javascript": "es2020"
    }
  }
}
```

### Target-Specific Options

Each target language has its own set of options:

#### Python Options

```json
{
  "transpilation": {
    "target": "python",
    "python_options": {
      "version": "3.9",
      "async_style": "asyncio",
      "type_annotations": true,
      "use_dataclasses": true
    }
  }
}
```

#### JavaScript Options

```json
{
  "transpilation": {
    "target": "javascript",
    "javascript_options": {
      "module_system": "esm",
      "target_env": "node",
      "strict_mode": true,
      "typescript_declarations": true
    }
  }
}
```

## Language-Specific Considerations

### Python

Python transpilation provides excellent feature coverage with some considerations:

- **Python Version**: Minimum supported version is Python 3.8
- **Type Hints**: Generated code includes type annotations by default
- **Asynchronous**: Uses `asyncio` for asynchronous programming
- **AI Features**: Full support for all AI capabilities
- **Performance**: JIT compilation available for performance-critical code

### JavaScript

JavaScript transpilation has the following considerations:

- **ECMAScript**: Targets ES2020 by default
- **Modules**: Supports both ESM and CommonJS
- **Async**: Uses native Promises and async/await
- **Types**: Optional TypeScript declaration files
- **Browser vs Node**: Configure target environment
- **AI Limitations**: Some advanced AI features may require server-side execution

## Extending Transpilation

### Custom Target Languages

Runa's architecture supports adding new target languages through the transpiler extension system:

```python
# Example of registering a custom transpiler (Python API)
from runa.transpiler import register_target

def my_custom_transpiler(ast, options):
    # Generate code from the AST
    # ...
    return generated_code

register_target("my_language", my_custom_transpiler)
```

### Custom Transformations

You can also define custom AST transformations:

```python
# Example of registering a custom AST transformer
from runa.transpiler import register_transformer

def optimize_loops(ast, context):
    # Perform loop optimization
    # ...
    return modified_ast

register_transformer("optimize_loops", optimize_loops)
```

### Code Generation Templates

Runa uses a template-based code generation system that you can extend:

```
# Extend with custom templates (example path: templates/my_language/process.tmpl)
def {{name}}({{params}}) {
    {% for statement in body %}
    {{transpile(statement)}}
    {% endfor %}
    {% if has_return %}
    return {{transpile(return_value)}};
    {% endif %}
}
```

## Additional Resources

- [Python Transpiler Reference](./PythonTranspilation.md)
- [JavaScript Transpiler Reference](./JavaScriptTranspilation.md)
- [Transpilation API Documentation](../Reference/TranspilationAPI.md)
- [Building Custom Transpilers](./CustomTranspilers.md)
- [JIT Compilation Guide](./JITCompilation.md)
- [Performance Optimization Guide](./TranspilationOptimization.md) 