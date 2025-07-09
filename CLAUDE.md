# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a **two-part monorepo** containing:

- **Runa programming language** - An AI-first universal translation platform with natural language syntax. The primary focus is currently on the `runa/` directory which contains the complete Runa language implementation.
- **Hermod** - An advanced AI-powered IDE and developer tools platform that will be built using Runa as its native language (planned for future development after Runa self-hosting is complete).

**Critical Constraint:** Both projects must remain cleanly separated and easily separable, as they will eventually be split into independent repositories with their own workflows, CI/CD, and release cycles.

## Monorepo Separation Strategy

**Future Separation Requirements:**
- Each project must have independent build systems and workflows
- Shared dependencies (if any) must be clearly documented and minimal
- Documentation should be project-specific where possible
- CI/CD pipelines must be designed to handle both projects independently
- Release cycles and versioning must be separate
- The eventual split should require minimal refactoring

**Current Development Approach:**
- Runa development takes priority (Phase 2.0 self-hosting)
- Hermod development is planned but not yet started
- All changes must maintain clean separation between projects
- Avoid cross-dependencies between Runa and Hermod codebases

## Claude-Specific Monorepo Guidelines

- **Respect separation:** Never create dependencies between Runa and Hermod. They must remain independent.
- **Clean separation:** Runa and Hermod code must remain completely separate and independently buildable.
- **Self-hosting first:** For Runa, prioritize features that move toward self-hosting capability.

## Commands for Development

### Testing Commands
Run tests from the project root directory:
```bash
# Run all tests (recommended)
python -m pytest runa/tests/ -v

# Run specific test suites
python -m pytest runa/tests/test_lexer.py -v           # Lexer tests (16 tests)
python -m pytest runa/tests/test_parser.py -v          # Parser tests (27 tests)
python -m pytest runa/tests/test_semantic.py -v        # Semantic analysis tests (7 tests)
python -m pytest runa/tests/test_compilation_pipeline.py -v  # End-to-end compilation tests
```

### Convenience Scripts
```bash
# Windows
.\runa-dev.bat test         # Run all tests
.\runa-dev.bat test-lexer   # Run lexer tests only
.\runa-dev.bat test-parser  # Run parser tests only
.\runa-dev.bat demo         # Run parser demonstration

# Unix/Linux/Mac
make test                   # Run all tests
make test-lexer             # Run lexer tests only
make test-parser            # Run parser tests only
make demo                   # Run parser demonstration
```

### Installation Commands
```bash
# Install in development mode
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"
```

### Running Individual Tests
```bash
# Run a specific test method
python -m pytest runa/tests/test_parser.py::TestRunaParser::test_function_call -v

# Run with coverage
python -m pytest runa/tests/ --cov=runa
```

## Architecture Overview

### Core Components

**runa/compiler/** - Complete compilation pipeline
- `lexer.py` - Natural language tokenizer (80+ token types, multi-word support)
- `parser.py` - Recursive descent parser with complete AST generation
- `semantic.py` - Semantic analyzer with symbol tables and type checking
- `ast_nodes.py` - 30+ AST node types with visitor pattern support
- `tokens.py` - Token definitions for natural language constructs
- `ir.py` - Intermediate representation with SSA-like form
- `ast_to_ir.py` - AST to IR transformation visitor
- `codegen/python_generator.py` - Python code generation

**runa/tests/** - Comprehensive test suite (50+ tests, 100% passing)
- All tests must be run from project root using `python -m pytest`
- Never run test files directly from the tests directory (causes import errors)

**runa/examples/** - Example Runa programs demonstrating syntax

### Language Features

**Natural Language Syntax** - Runa uses English-like programming constructs:
- Variables: `Let user name be "Alice"`
- Arithmetic: `price multiplied by 2 plus tax`
- Comparisons: `age is greater than 21`
- Control flow: `If condition: ... Otherwise: ...`
- Functions: `Calculate Total with price as 100 and tax as 0.08`
- Collections: `list containing 1, 2, 3, 4, 5`
- Multi-word identifiers: `user name`, `account balance`, `final total`

**Complete Compilation Pipeline** - Runa → Python compilation fully working:
```python
from runa.compiler import compile_runa_to_python

runa_code = '''
Let user name be "Alice"
Let age be 25
If age is greater than 18:
    Display "Adult user: " with message user name
'''

python_code = compile_runa_to_python(runa_code)
# Generates clean, executable Python code
```

**Self-Hosting Capabilities** - Runa can now compile itself:
```python
from runa.compiler import (
    compile_runa_to_runa,      # Round-trip translation
    compile_ir_to_runa,        # IR → Runa generation
    BidirectionalTranslator,   # Universal translation engine
    translate_to_runa,         # Convenience function
    translate_from_runa        # Convenience function
)

# Round-trip translation (preserves semantics)
original = 'Let x be 42'
regenerated = compile_runa_to_runa(original)

# Bidirectional translation between languages
translator = BidirectionalTranslator()
result = translator.translate(runa_code, SupportedLanguage.RUNA, SupportedLanguage.PYTHON)
```

**AI-to-AI Communication Protocol** - Ready for LLM integration:
```python
# Logic LLM → Runa specification → Coding LLM → Target language
logic_output = '''Process called "calculate tax" that takes amount as Float returns Float:
    Let tax rate be 0.08
    Return amount multiplied by tax rate'''

# Translate to any target language for execution
python_version = translate_from_runa(logic_output, "python")
javascript_version = translate_from_runa(logic_output, "javascript")

# Or use direct compilation functions
js_code = compile_runa_to_javascript(logic_output)
py_code = compile_runa_to_python(logic_output)
```

**Type System** - Advanced type inference with generics:
- Basic types: `Integer`, `String`, `Boolean`, `Float`
- Generic types: `List[Integer]`, `Dictionary[String, Integer]`
- Type inference from context and assignments
- Symbol table management with nested scopes

### Development Status

**Current Phase**: 2.1 UNIVERSAL TRANSLATION PLATFORM - Multi-Language Support
- ✅ Lexer: 16/16 tests (100%) - Natural language tokenization
- ✅ Parser: 27/27 tests (100%) - Complete AST generation
- ✅ Semantic Analysis: 7/7 tests (100%) - Symbol tables and type checking
- ✅ **Code Generation**: Python + JavaScript + Runa (self-hosting)
- ✅ **Self-Hosting**: Runa → IR → Runa round-trip translation working
- ✅ **Bidirectional Translation**: Universal ANY ↔ Runa ↔ ANY translation
- ✅ **AI-to-AI Communication**: Multi-language LLM integration ready
- ✅ **Language Expansion**: Modular generator architecture for easy addition

**Total Test Coverage**: 60+ tests, 98% passing

## Important Development Notes

### Common Pitfalls

**Import Errors**: Always run tests from the project root directory using pytest:
```bash
# ✅ CORRECT
python -m pytest runa/tests/test_lexer.py -v

# ❌ WRONG (causes ModuleNotFoundError)
cd runa/tests && python test_lexer.py
```

**Multi-word Identifiers**: Runa uses spaces in identifiers:
- `user name` not `user_name`
- `account balance` not `account_balance`
- `final total` not `final_total`

**Natural Language Operators**: Use word-based operators:
- `plus`, `minus`, `times`, `divided by`
- `is greater than`, `is less than or equal to`
- `is equal to`, `is not equal to`

### Testing Strategy

When making changes:
1. Run the full test suite to ensure no regressions
2. Add new tests for new features following existing patterns
3. Test files are well-documented with clear test names
4. Use pytest fixtures and parameterized tests where appropriate

### Code Generation

The Python code generator produces clean, readable Python:
- Multi-word identifiers converted to snake_case (`user name` → `user_name`)
- Natural language constructs translated to Python equivalents
- Helper functions automatically included for Runa built-ins
- Standard library imports added as needed

## Key Files to Understand

- `runa/compiler/__init__.py` - Main API exports and compilation functions
- `runa/compiler/lexer.py:80-150` - Multi-word token recognition logic
- `runa/compiler/parser.py:200-300` - Expression parsing with precedence
- `runa/compiler/semantic.py:50-100` - Symbol table and type inference
- `runa/compiler/codegen/runa_generator.py` - **NEW**: Runa code generation (self-hosting)
- `runa/compiler/bidirectional_translator.py` - **NEW**: Universal translation engine
- `runa/tests/test_compilation_pipeline.py` - End-to-end compilation tests
- `runa/tests/test_self_hosting.py` - **NEW**: Self-hosting and round-trip tests

## Documentation

Comprehensive documentation in `docs/current-runa-docs/RunaDevelopment/`:
- `RunaLanguageReference.md` - Complete language specification
- `RunaFormalGrammarSpecifications.md` - EBNF grammar
- `TypeSystem.md` - Advanced type system documentation
- `GettingStarted.md` - Beginner tutorial