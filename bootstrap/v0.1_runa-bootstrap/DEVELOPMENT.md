# Development Guide - Runa Bootstrap Compiler v0.1

## Project Structure

```
src/
├── main.rs                    # CLI entry point
├── lib.rs                     # Library exports
├── compiler/                  # Compiler implementation
│   ├── mod.rs                # Compiler driver
│   ├── frontend/             # Frontend (lexer, parser, AST)
│   │   ├── lexer.rs         # Tokenization
│   │   ├── parser.rs        # Parsing to AST
│   │   ├── ast.rs           # Abstract Syntax Tree definitions
│   │   └── tests/           # Frontend tests
│   ├── middle/              # Middle-end (semantic analysis)
│   │   ├── semantic.rs      # Semantic analysis
│   │   ├── type_checker.rs  # Type checking
│   │   ├── symbol_table.rs  # Symbol table management
│   │   └── tests/           # Middle-end tests
│   └── backend/             # Backend (code generation)
│       ├── llvm.rs          # LLVM integration
│       ├── codegen.rs       # Code generation
│       ├── optimization.rs  # Optimization passes
│       └── tests/           # Backend tests
├── runtime/                 # Runtime support
│   ├── memory.rs           # Memory management
│   ├── gc.rs               # Garbage collection
│   ├── ffi.rs              # Foreign function interface
│   ├── platform.rs         # Platform abstraction
│   └── tests/              # Runtime tests
├── utils/                  # Utility modules
│   ├── diagnostics.rs      # Error reporting
│   ├── io.rs               # File I/O utilities
│   ├── strings.rs          # String manipulation
│   └── tests/              # Utility tests
tests/
├── integration/            # Integration tests
├── unit/                   # Unit tests
└── end_to_end/             # End-to-end tests
examples/                   # Example Runa programs
docs/                       # Additional documentation
```

## Development Workflow

### Prerequisites

1. **Rust** (1.70 or later)
2. **LLVM 17** with development headers
3. **Git** for version control

### Setting up LLVM

#### Ubuntu/Debian:
```bash
sudo apt-get install llvm-17-dev libllvm17 clang-17
export LLVM_SYS_170_PREFIX=/usr/lib/llvm-17
```

#### macOS:
```bash
brew install llvm@17
export LLVM_SYS_170_PREFIX=/opt/homebrew/opt/llvm@17
```

#### Building from Source:
```bash
git clone https://github.com/llvm/llvm-project.git
cd llvm-project
mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=Release -DLLVM_ENABLE_PROJECTS="clang" ../llvm
make -j$(nproc)
export LLVM_SYS_170_PREFIX=/path/to/llvm-project/build
```

### Building

```bash
# Build in debug mode
cargo build

# Build in release mode
cargo build --release

# Run tests
cargo test

# Run with verbose output
RUST_LOG=debug cargo run -- compile examples/hello_world.runa

# Cross-compile for specific target
cargo build --target x86_64-unknown-linux-gnu
```

### Testing

```bash
# Run all tests
cargo test

# Run specific test module
cargo test lexer_tests

# Run integration tests only
cargo test --test integration

# Run with test output
cargo test -- --nocapture
```

### Code Style

This project follows standard Rust conventions:

- Use `rustfmt` for formatting: `cargo fmt`
- Use `clippy` for linting: `cargo clippy`
- Follow the existing code patterns in the codebase
- Add tests for new functionality
- Update documentation for public APIs

### Adding New Features

1. **Frontend Changes**: Modify lexer, parser, or AST definitions
2. **Middle-end Changes**: Update semantic analysis or type checking
3. **Backend Changes**: Modify LLVM code generation
4. **Runtime Changes**: Update memory management or platform support

### Debugging

```bash
# Debug with GDB
cargo build
gdb target/debug/runac

# Debug LLVM IR generation
export RUST_LOG=debug
cargo run -- compile examples/hello_world.runa --emit-llvm-ir

# Verify LLVM module
llvm-dis output.bc -o output.ll
```

### Performance Profiling

```bash
# Profile with perf (Linux)
cargo build --release
perf record target/release/runac compile large_program.runa
perf report

# Profile with Instruments (macOS)
cargo build --release
xcrun xctrace record --template "Time Profiler" target/release/runac compile large_program.runa
```

### Cross-Platform Development

The bootstrap compiler supports multiple platforms. Test cross-compilation:

```bash
# Test all supported targets
for target in linux_x64 linux_arm64 windows_x64 macos_x64 macos_arm64 freebsd_x64; do
    cargo run -- compile examples/hello_world.runa --target $target -o test_$target
done
```

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make changes and add tests
4. Run full test suite: `cargo test`
5. Commit changes: `git commit -am "Add my feature"`
6. Push to branch: `git push origin feature/my-feature`
7. Create a Pull Request

### Common Issues

1. **LLVM not found**: Set `LLVM_SYS_170_PREFIX` environment variable
2. **Linking errors**: Ensure target platform libraries are available
3. **Test failures**: Check that LLVM version matches requirements
4. **Performance issues**: Use release builds for benchmarking

### Architecture Notes

This bootstrap compiler is designed to be:
- **Simple**: Focused on core functionality needed for v0.2
- **Correct**: Comprehensive error checking and validation
- **Fast**: Optimized compilation pipeline
- **Cross-platform**: Supports all target platforms from day one

The compiler is structured as a traditional three-phase compiler:
1. **Frontend**: Source → AST
2. **Middle-end**: AST → Typed AST (with semantic analysis)
3. **Backend**: Typed AST → Object code (via LLVM)

Each phase is designed to be modular and testable independently.