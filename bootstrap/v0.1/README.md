# Runa v0.1 - Self-Hosting Compiler

This directory contains the Runa-Zero compiler written in Runa-Zero itself.

## Architecture

- **Language**: Pure Runa-Zero (no Rust dependencies)
- **Memory Management**: Simple bump allocator
- **Data Structures**: Fixed-size arrays instead of dynamic collections
- **Target**: Self-hosting compilation

## Bootstrap Process

1. **Stage 1**: Use v0.0 (Rust) to compile `src/compiler.runa` → `runac-v01`
2. **Stage 2**: Use `runac-v01` to compile itself → `runac-v01-stage2`
3. **Verification**: Both stages should be bit-for-bit identical

## Files

- `src/compiler.runa` - Main compiler entry point
- `src/memory.runa` - Memory management
- `src/lexer.runa` - Tokenization
- `src/parser.runa` - AST construction
- `src/codegen.runa` - Assembly generation
- `src/utils.runa` - String and array utilities

## Build

```bash
# Stage 1: Bootstrap with v0.0
../v0.0/target/release/runac src/compiler.runa -o runac-v01

# Stage 2: Self-compile
./runac-v01 src/compiler.runa -o runac-v01-stage2

# Verify
diff runac-v01 runac-v01-stage2
```