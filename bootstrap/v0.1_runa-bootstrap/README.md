# Runa Bootstrap Compiler v0.1

**Minimal bootstrap compiler to compile v0.2 pure-Runa compiler.**

## Purpose

This is a bare-bones Rust compiler that can parse and compile basic Runa programs. Its ONLY job is to compile the v0.2 self-hosting Runa compiler.

## Structure

- `src/main.rs` - CLI entry point
- `src/lexer.rs` - Tokenization 
- `src/parser.rs` - Parse to AST
- `src/codegen.rs` - LLVM code generation
- `src/types.rs` - Basic AST types

## Supported Runa Syntax

```runa
Process called "function_name" that takes param as Integer returns Integer:
    Let variable be 42
    Return variable + param
End Process
```

## Usage

```bash
cargo build --release
./target/release/runac input.runa -o output.o
```

## Dependencies

- Rust 1.70+
- LLVM 17
- Set `LLVM_SYS_170_PREFIX` if needed

## What This Does NOT Do

- Complex type system
- Memory management  
- Standard library
- Error recovery
- Optimization
- Debugging info

This is intentionally minimal. All advanced features belong in v0.2.