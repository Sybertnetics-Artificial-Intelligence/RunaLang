# Runa Bootstrap Compiler (v0.1)

This is the first-stage bootstrap compiler for the Runa programming language, written in Rust.

## Purpose

The v0.1 bootstrap compiler serves as the foundation for the Runa self-hosting pipeline:

1. **v0.1 (This)**: Rust-based compiler that can compile basic Runa code
2. **v0.2**: Pure Runa compiler with zero external dependencies (compiled by v0.1)  
3. **v0.3+**: Self-hosted Runa compilers (compiled by v0.2)

## Architecture

### Frontend (`src/compiler/frontend/`)
- **Lexer**: Tokenizes Runa source code
- **Parser**: Builds Abstract Syntax Trees (ASTs)
- **AST**: Core data structures representing Runa programs

### Middle-end (`src/compiler/middle/`)
- **Semantic Analysis**: Type checking, scope resolution, symbol table management
- **Type Checker**: Ensures type safety and inference
- **Symbol Table**: Manages variable, function, and type definitions

### Backend (`src/compiler/backend/`)
- **LLVM Integration**: Uses LLVM for code generation and optimization
- **Code Generation**: Converts ASTs to LLVM IR
- **Optimization**: Applies performance optimizations

### Runtime Support (`src/runtime/`)
- **Memory Management**: Basic allocator and garbage collection
- **Platform Interface**: OS abstraction layer
- **FFI Support**: Foreign function interface for system calls

### Utilities (`src/utils/`)
- **Diagnostics**: Error reporting and source location tracking
- **I/O**: File reading and writing utilities
- **String Handling**: String manipulation and interning

## Cross-Platform Support

The bootstrap compiler supports cross-compilation for:
- **Linux**: x86_64, ARM64
- **Windows**: x86_64, ARM64  
- **macOS**: x86_64, ARM64 (Apple Silicon)
- **FreeBSD**: x86_64, ARM64
- **OpenBSD**: x86_64, ARM64
- **NetBSD**: x86_64, ARM64

## Building

```bash
# Build the compiler
cargo build --release

# Run tests
cargo test

# Build for specific target
cargo build --release --target x86_64-unknown-linux-gnu
```

## Usage

```bash
# Compile a Runa program
./target/release/runac input.runa -o output

# Check syntax without compilation
./target/release/runac input.runa --check

# Cross-compile for different platform
./target/release/runac input.runa -o output --target linux_x64
```

## Testing

The project includes comprehensive test coverage:

- **Unit Tests**: Located in `tests/` subdirectories within each module
- **Integration Tests**: Located in `tests/integration/`
- **End-to-End Tests**: Located in `tests/end_to_end/`

## Development

This compiler follows strict coding standards:
- No placeholder implementations
- Complete algorithms and logic
- Production-ready code quality
- Comprehensive error handling

## Next Steps

Once v0.1 is complete, it will be used to compile the v0.2 pure-Runa compiler, beginning the self-hosting process.