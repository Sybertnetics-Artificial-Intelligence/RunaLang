# Runa Runtime Documentation

This directory contains documentation about the Runa runtime system, including the Runa Virtual Machine (RunaVM) and related components.

## Overview

The Runa runtime system is responsible for executing Runa programs. It includes several key components:

- **Runa Virtual Machine (RunaVM)**: The core execution engine that runs Runa bytecode
- **Bytecode Compiler**: Translates Runa source code to bytecode
- **Memory Management**: Automated memory management with garbage collection
- **Concurrency System**: Lightweight tasks and parallel execution capabilities
- **Standard Library**: Core libraries and functionalities available to all Runa programs

## Key Documents

- [RunaVM](RunaVM.md) - Comprehensive documentation of the Runa Virtual Machine
- [Memory Management](MemoryManagement.md) - Details of the garbage collection and memory system
- [Concurrency Model](ConcurrencyModel.md) - Explanation of Runa's task-based concurrency
- [Performance Optimization](PerformanceOptimization.md) - Techniques for optimizing Runa program performance
- [Debugging](Debugging.md) - Tools and techniques for debugging Runa programs

## Tools

The Runa runtime includes several command-line tools:

- `runavm` - The Runa Virtual Machine executable for running bytecode
- `runa compile` - The compiler for translating source to bytecode
- `runa run` - Convenience tool for compiling and executing in one step
- `runa debug` - Debugger for Runa programs
- `runa profile` - Profiling tool for performance analysis

## Configuration

The runtime behavior can be configured through:

- Command-line arguments to the runavm executable
- Environment variables (RUNAVM_*)
- Configuration files (runavm.json)

## Platform Support

The Runa runtime supports:

- **Windows**: 10 and newer (x86_64, ARM64)
- **macOS**: 10.15+ (x86_64, Apple Silicon) 
- **Linux**: Most modern distributions
- **Web Browsers**: Via WebAssembly
- **Mobile**: iOS and Android (through embedded mode)

## System Requirements

Minimum requirements:
- 64-bit processor
- 4 GB RAM (8 GB recommended)
- 100 MB disk space

## See Also

- [Integration Documentation](../Integration/README.md) - Information on embedding Runa in applications
- [Development Guide](../Development/README.md) - Resources for Runa language developers
- [API Reference](../API/README.md) - API documentation for Runa libraries 