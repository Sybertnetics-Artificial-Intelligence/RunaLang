# Runa Version Comparison Chart
## Quick Reference: What's in Each Version?

**Legend:**
- ✅ Complete
- 🔄 In Progress
- 📋 Planned
- ❌ Not Included

---

## Core Language Features

| Feature | v0.0.7.5 | v0.0.8 | v0.0.9 | v0.1.0 | v0.2.0 | v0.3.0 | v1.0 |
|---------|----------|--------|--------|--------|--------|--------|------|
| **Variables & Arithmetic** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Conditionals (If/Otherwise)** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Loops (While)** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Functions/Processes** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Recursion** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Strings** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Lists** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Structs/Types** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **File I/O** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Modules/Imports** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Inline Assembly** | ❌ | 🔄 | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Generics** | ❌ | ❌ | ❌ | ❌ | ❌ | 📋 | ✅ |
| **Pattern Matching** | ❌ | ❌ | ❌ | ❌ | ❌ | 📋 | ✅ |
| **Result Types** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Ownership System** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Concurrency** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

---

## Compiler Features

| Feature | v0.0.7.5 | v0.0.8 | v0.0.9 | v0.1.0 | v0.2.0 | v0.3.0 | v1.0 |
|---------|----------|--------|--------|--------|--------|--------|------|
| **Self-Hosting** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Assembly Output (.s)** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Requires `as` (GNU Assembler)** | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Requires `ld` (GNU Linker)** | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Native Object Files (.o)** | ❌ | ❌ | 🔄 | ✅ | ✅ | ✅ | ✅ |
| **Custom Linker** | ❌ | ❌ | 🔄 | ✅ | ✅ | ✅ | ✅ |
| **Optimization Level 0** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Optimization Level 1-3** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Profile-Guided Optimization** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Link-Time Optimization** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **SIMD Auto-Vectorization** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Debug Info (DWARF)** | ❌ | ❌ | ❌ | ❌ | ❌ | 📋 | ✅ |

---

## Standard Library

| Feature | v0.0.7.5 | v0.0.8 | v0.0.9 | v0.1.0 | v0.2.0 | v0.3.0 | v1.0 |
|---------|----------|--------|--------|--------|--------|--------|------|
| **Basic I/O (print, read)** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **String Utils** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **List Operations** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **File I/O** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Hash Tables** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Dynamic Arrays** | ❌ | ❌ | ❌ | ❌ | 📋 | ✅ | ✅ |
| **Sets** | ❌ | ❌ | ❌ | ❌ | 📋 | ✅ | ✅ |
| **Queues/Stacks** | ❌ | ❌ | ❌ | ❌ | 📋 | ✅ | ✅ |
| **Regex** | ❌ | ❌ | ❌ | ❌ | 📋 | ✅ | ✅ |
| **JSON Parsing** | ❌ | ❌ | ❌ | ❌ | 📋 | ✅ | ✅ |
| **HTTP Client** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Networking** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Math Library** | ❌ | ❌ | ❌ | ❌ | 📋 | ✅ | ✅ |
| **Time/Date** | ❌ | ❌ | ❌ | ❌ | 📋 | ✅ | ✅ |
| **Cryptography** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

---

## Tooling & Ecosystem

| Feature | v0.0.7.5 | v0.0.8 | v0.0.9 | v0.1.0 | v0.2.0 | v0.3.0 | v1.0 |
|---------|----------|--------|--------|--------|--------|--------|------|
| **Compiler Binary** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Package Manager** | ❌ | ❌ | ❌ | ❌ | 📋 | ✅ | ✅ |
| **Build System** | ❌ | ❌ | ❌ | ❌ | 📋 | ✅ | ✅ |
| **VS Code Extension** | ❌ | ❌ | ❌ | ❌ | ❌ | 📋 | ✅ |
| **Language Server (LSP)** | ❌ | ❌ | ❌ | ❌ | ❌ | 📋 | ✅ |
| **Debugger (GDB compat)** | ❌ | ❌ | ❌ | ❌ | ❌ | 📋 | ✅ |
| **Profiler** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Package Repository** | ❌ | ❌ | ❌ | ❌ | ❌ | 📋 | ✅ |
| **CI/CD Templates** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

---

## Syntax Modes

| Feature | v0.0.7.5 | v0.0.8 | v0.0.9 | v0.1.0 | v0.2.0 | v0.3.0 | v1.0 |
|---------|----------|--------|--------|--------|--------|--------|------|
| **Canonical (English)** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Developer (Concise)** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | 📋 |
| **Viewer (Read-only)** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | 📋 |
| **Mixed Mode** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | 📋 |
| **Auto-Conversion** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | 📋 |

**Note:** Dual syntax system may be v1.1+ depending on priorities.

---

## Performance Benchmarks

| Metric | v0.0.7.5 | Target v0.1.0 | Target v1.0 |
|--------|----------|---------------|-------------|
| **vs C (GCC -O2)** | 2-4x slower | 2-3x slower | 0.8-1.2x (match) |
| **vs Rust (-O)** | 2-4x slower | 2-3x slower | 0.8-1.2x (match) |
| **vs Python** | 6-18x faster | 10-20x faster | 20-50x faster |
| **vs Java (JIT)** | 1-1.5x faster | 1.5-2x faster | 2-3x faster |
| **Compiler Size** | 198 KB | ~250 KB | ~500 KB |
| **Compilation Speed** | Baseline | 1.2x slower | 2x slower |

---

## Platform Support

| Platform | v0.0.7.5 | v0.1.0 | v1.0 |
|----------|----------|--------|------|
| **Linux x86-64** | ✅ | ✅ | ✅ |
| **Windows x86-64** | ❌ | ❌ | 📋 |
| **macOS x86-64** | ❌ | ❌ | 📋 |
| **macOS ARM64** | ❌ | ❌ | 📋 |
| **Linux ARM64** | ❌ | ❌ | 📋 |
| **WebAssembly** | ❌ | ❌ | 📋 |

---

## Documentation

| Document | v0.0.7.5 | v0.1.0 | v1.0 |
|----------|----------|--------|------|
| **Language Specification** | ✅ | ✅ | ✅ |
| **Compiler Architecture** | ❌ | 📋 | ✅ |
| **Standard Library Reference** | ❌ | 📋 | ✅ |
| **Tutorial Series** | ❌ | 📋 | ✅ |
| **Cookbook** | ❌ | ❌ | ✅ |
| **Contributing Guide** | ❌ | 📋 | ✅ |
| **API Documentation** | ❌ | ❌ | ✅ |

---

## Key Milestones

### v0.0.7.5 ✅ (Current)
**"Self-Hosting Achieved"**
- Compiler written in Runa compiles itself
- Bootstrap test passes (Stage 2 = Stage 3 = Stage 4)
- Performance competitive with Python
- 198KB binary size

### v0.1.0 🎯
**"Beta Release - Toolchain Independence"**
- No external dependencies (no `as`, no `ld`)
- Native object file generation
- Custom linker
- Ready for early adopters

### v1.0.0 🎯
**"Production Release"**
- Feature-complete language
- Performance matches C/Rust
- Comprehensive standard library
- Rich tooling ecosystem
- Active community
- Production-ready

---

