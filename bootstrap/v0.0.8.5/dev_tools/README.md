# Runa Development Tools (v0.0.8.5)

## Overview

This directory contains user-facing development tools that consume the Runa compiler APIs. These tools provide the complete development experience for Runa programming.

## Architecture

The dev_tools follow a hybrid architecture:

- **Compiler APIs** (`../compiler/tools/`) - Core functionality and APIs
- **Dev Tools** (`./`) - User-facing tools that consume the APIs

## Tool Structure

Each tool follows a consistent structure:

```
tool_name/
├── main.runa      # Main entry point and orchestration
├── cli.runa       # Command line interface
├── config.runa    # Configuration management (if needed)
└── [specific].runa # Tool-specific functionality
```

## Available Tools

### Core Development Tools

| Tool | Purpose | Status |
|------|---------|--------|
| `runa_fmt/` | Code formatting and style enforcement | 🔧 Skeleton |
| `runa_lint/` | Code quality checking and linting | 🔧 Skeleton |
| `runa_test/` | Test execution and test management | 🔧 Skeleton |
| `runa_annotate/` | Runa Annotation System processing | 🔧 Skeleton |

### Build & Package Tools

| Tool | Purpose | Status |
|------|---------|--------|
| `runa_build/` | Build system and compilation orchestration | 🔧 Skeleton |
| `runa_package/` | Package management and dependency resolution | 🔧 Skeleton |

### Development Experience Tools

| Tool | Purpose | Status |
|------|---------|--------|
| `runa_debug/` | Runtime debugging and inspection | 🔧 Skeleton |
| `runa_profile/` | Performance profiling and analysis | 🔧 Skeleton |
| `runa_repl/` | Interactive REPL and experimentation | 🔧 Skeleton |
| `runa_init/` | Project initialization and scaffolding | 🔧 Skeleton |

### Translation Tools

| Tool | Purpose | Status |
|------|---------|--------|
| `runa_convert/` | Code translation (C ↔ Runa ↔ Python) | 🔧 Skeleton |
| `runa_translate/` | Natural language translation (English ↔ Spanish) | 🔧 Skeleton |

### Utility Tools

| Tool | Purpose | Status |
|------|---------|--------|
| `benchmark_runner/` | Performance benchmarking and testing | 🔧 Skeleton |

## Implementation Status

All tools are currently in skeleton form with:
- ✅ Directory structure created
- ✅ Main entry points defined
- ✅ CLI interfaces planned
- ✅ Tool-specific functionality outlined
- ⏳ Full implementation pending

## Usage

Once implemented, tools will be available as:

```bash
# Core development
runa fmt --check
runa lint --fix
runa test --verbose
runa annotate --validate

# Build and package
runa build --release
runa package install

# Development experience
runa debug --attach
runa profile --cpu
runa repl --interactive
runa init --template web

# Translation
runa convert --from c --to runa
runa translate --from en --to es
```

## Integration

These tools integrate with:
- **Compiler APIs** - Core functionality from `../compiler/tools/`
- **Language Server** - IDE integration via `../compiler/services/language_server/`
- **IDE Integration** - Editor support via `../compiler/services/ide_integration/`

## Future Enhancements

- **Plugin System** - Extensible tool architecture
- **Configuration Management** - Unified tool configuration
- **Performance Optimization** - Parallel tool execution
- **Cloud Integration** - Remote tool execution and caching
