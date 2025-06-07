# Runa Development Documentation

This directory contains documentation for developers who want to work on the Runa language itself, contribute to its development, or understand its internal architecture.

## Overview

The Runa development documentation provides insights into:

- **Language Architecture**: The structure and design of the Runa language
- **Compiler Implementation**: How the Runa compiler works
- **VM Implementation**: The internals of the Runa Virtual Machine
- **Contributing Guidelines**: How to contribute to the Runa project
- **Testing and Validation**: Testing framework for language features

## Key Documents

- [Bytecode Format](BytecodeFormat.md) - Detailed specification of the Runa bytecode format
- [Compiler Architecture](CompilerArchitecture.md) - Technical details of the compiler infrastructure
- [Grammar Definition](GrammarDefinition.md) - Formal definition of the Runa grammar
- [VM Implementation](VMImplementation.md) - Internals of the Runa Virtual Machine
- [Contributing Guidelines](Contributing.md) - How to contribute to Runa development

## Language Architecture

Runa's architecture consists of several key components:

- **Lexer/Parser**: Converts source code to an abstract syntax tree (AST)
- **Type Checker**: Performs static type analysis
- **Semantic Analyzer**: Validates program semantics
- **Intermediate Representation**: Language-neutral representation of programs
- **Code Generator**: Produces bytecode or target language code
- **Runtime System**: Executes compiled Runa programs

```
┌───────────────────────┐
│    Runa Source Code   │
└───────────┬───────────┘
            ▼
┌───────────────────────┐
│     Lexer/Parser      │
└───────────┬───────────┘
            ▼
┌───────────────────────┐
│  Abstract Syntax Tree │
└───────────┬───────────┘
            ▼
┌───────────────────────┐
│      Type Checker     │
└───────────┬───────────┘
            ▼
┌───────────────────────┐
│   Semantic Analyzer   │
└───────────┬───────────┘
            ▼
┌───────────────────────┐
│      Intermediate     │
│     Representation    │
└───────────┬───────────┘
            ▼
┌────────────┴────────────┐
│                         │
▼                         ▼
┌─────────────┐    ┌─────────────┐
│   Bytecode  │    │  Transpiled │
│  Generator  │    │     Code    │
└──────┬──────┘    └──────┬──────┘
       │                  │
       ▼                  ▼
┌─────────────┐    ┌─────────────┐
│   RunaVM    │    │   Target    │
│  Execution  │    │  Language   │
└─────────────┘    └─────────────┘
```

## Building Runa

### Prerequisites

- C++17 compatible compiler (GCC 7+, Clang 5+, MSVC 2019+)
- CMake 3.12 or higher
- Python 3.7 or higher
- LLVM 10.0 or higher (optional, for JIT compilation)

### Build Instructions

```bash
# Clone the repository
git clone https://github.com/runalang/runa.git
cd runa

# Create build directory
mkdir build
cd build

# Configure CMake
cmake ..

# Build
cmake --build .

# Run tests
ctest
```

### Directory Structure

```
runa/
├── src/
│   ├── compiler/      # Compiler implementation
│   ├── runtime/       # Runtime system
│   ├── vm/            # Virtual machine implementation
│   ├── stdlib/        # Standard library implementation
│   └── tools/         # Development tools
├── include/           # Public headers
├── libs/              # Third-party libraries
├── tests/             # Test suite
├── docs/              # Documentation
└── examples/          # Example programs
```

## Contributing

We welcome contributions to Runa! Here's how you can help:

- **Bug Reports**: Report issues through the issue tracker
- **Feature Requests**: Suggest new features or improvements
- **Documentation**: Improve existing docs or add new ones
- **Code Contributions**: Submit pull requests for bug fixes or features

All contributors should follow our [Code of Conduct](CodeOfConduct.md) and [Contributing Guidelines](Contributing.md).

## Development Workflow

1. **Fork the Repository**: Create your own fork of the Runa repository
2. **Create a Branch**: Make your changes in a new branch
3. **Develop and Test**: Implement your changes and add tests
4. **Submit a Pull Request**: Push your branch and create a PR
5. **Code Review**: Address feedback from project maintainers
6. **Merge**: Once approved, your PR will be merged

## Testing

Runa uses a comprehensive testing framework:

- **Unit Tests**: Test individual components
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete program execution
- **Benchmark Tests**: Measure performance metrics

Run the test suite with:

```bash
cd build
ctest
```

## Version Control

Runa uses Git for version control with the following conventions:

- **Branches**: Use feature/ for features, bugfix/ for bug fixes
- **Commits**: Use conventional commit messages
- **Tags**: Versions are tagged as v1.2.3

## See Also

- [Runtime Documentation](../Runtime/README.md) - Information on the Runa runtime system
- [Integration Documentation](../Integration/README.md) - Guide to embedding and integrating Runa
- [API Reference](../API/README.md) - API documentation for Runa libraries 