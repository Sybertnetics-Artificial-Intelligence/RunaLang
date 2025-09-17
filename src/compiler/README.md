# Runa Static Compiler

The Runa static compiler transforms Runa source code into AOTT-ready bytecode for execution by the tiered execution system.

## Architecture

This compiler follows a clean pipeline:
```
Source Code → Lexer → Parser → Semantic Analysis → IR → Bytecode
```

## Directory Structure

- `bootstrap/` - Minimal Rust bootstrap compiler (5% of compiler)
- `frontend/` - Lexing, parsing, semantic analysis (Runa)
- `middle/` - IR transformations and static analysis (Runa)
- `backend/` - AOTT-ready bytecode generation (Runa)
- `driver/` - Build orchestration and compilation pipeline (Runa)
- `tools/` - Development tools (formatter, linter, etc.)

## Key Features

- **AOTT-Ready Output**: Generates bytecode with profiling hooks and deoptimization metadata
- **Self-Hosting**: 95% implemented in Runa itself
- **Static Analysis**: Comprehensive analysis for optimization hints
- **Clean Separation**: Pure static compilation - no runtime concerns

## Integration Points

- **Input**: Runa source files (`.runa`)
- **Output**: AOTT bytecode with metadata
- **Used by**: AOTT system for Tier 0 execution

## Development Status

🚧 **Under Construction** - Fresh implementation as part of AOTT architecture rewrite.

See `../../docs/plans/RUNA_AOTT_ARCHITECTURE_PLAN.md` for full architectural context.