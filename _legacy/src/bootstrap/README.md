# Runa Bootstrap Compiler

## Purpose

This directory contains the **Stage 0 bootstrap compiler** for the Runa programming language, written in Rust. This is the **Genesis Compiler** - the permanent bootstrap key that ensures Runa can always be built from source on a new system.

## Architecture

- **Role**: Stage 0 compiler for bootstrapping the main Runa compiler
- **Language**: Rust (not Runa)
- **Purpose**: Compile the main Runa compiler (`runa/src/compiler/`) from source
- **Permanence**: This compiler is **never replaced** - it's the foundation

## Usage

```bash
# Build the bootstrap compiler
cargo build --release

# Use it to compile Runa source code
./target/release/runac your_program.runa
```

## Relationship to Main Compiler

- **Bootstrap Compiler** (this): Rust-based, compiles Runa code
- **Main Compiler** (`runa/src/compiler/`): Runa-based, self-hosted
- **Runtime** (`runa/src/runtime/`): VM and runtime environment

## Development Workflow

1. **New System Setup**: Use this bootstrap compiler to build the main Runa compiler
2. **Normal Development**: Use the main Runa compiler for all development
3. **Recovery**: If main compiler is corrupted, use this to rebuild it

## Important Notes

- This compiler is **legacy code** and should not be enhanced
- All new features go into the main Runa compiler
- This exists solely for bootstrapping and recovery
- Do not modify this unless absolutely necessary for bootstrapping 