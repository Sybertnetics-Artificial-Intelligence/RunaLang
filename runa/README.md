# Runa Programming Language

Runa is a revolutionary programming language designed to bridge human thought patterns with machine execution. Named after Norse runes that encoded knowledge and meaning, Runa features pseudocode-like syntax that resembles natural language while maintaining the precision needed for computational execution.

## Core Features

- **Natural Language Syntax**: Code that reads like English while maintaining computational precision
- **AI-Native Design**: Built specifically for AI systems to reason with and generate
- **Knowledge Integration**: Direct interface with knowledge graphs and semantic systems
- **Universal Code Generation**: Transpile to multiple target languages (Python, Java, C++, etc.)
- **Type System**: Strong, static typing with powerful type inference

## Getting Started

### Installation

```bash
# Once we have a package ready
pip install runa-lang
```

### Basic Example

```
# This is a Runa program
Let user name be "Alex"
Let user age be 28

If user age is greater than 21:
    Display user name with message "is an adult"
Otherwise:
    Display user name with message "is underage"

Process called "Calculate Total Price" that takes items and tax rate:
    Let subtotal be the sum of all prices in items
    Let tax amount be subtotal multiplied by tax rate
    Return subtotal plus tax amount
```

## Project Structure

- `src/` - Source code for the Runa language
  - `core/` - Core language functionality
  - `lexer/` - Lexical analysis
  - `parser/` - Syntax analysis and parsing
  - `ast/` - Abstract syntax tree definitions
  - `semantic/` - Semantic analysis
  - `type_system/` - Type checking and inference
  - `vm/` - Virtual machine implementation
- `tests/` - Test suite
- `docs/` - Documentation
- `examples/` - Example programs
- `tools/` - Development tools

## Development Status

Runa is currently in early development as part of the SyberSuite AI ecosystem. The roadmap includes:

1. Core language implementation
2. Standard library development
3. AI-specific features
4. Universal code generation
5. LLM integration and training data generation

## Contributing

Please refer to [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to the project.

## License

This project is licensed under the [MIT License](LICENSE). 