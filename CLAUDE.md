# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a **two-part monorepo** containing:

- **Runa programming language** - An AI-first universal translation platform with natural language syntax supporting 50+ programming languages across 7 tiers. The primary focus is currently on the `runa/` directory which contains the complete Runa language implementation.
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
- Runa development takes priority (Phase 2.1 Universal Translation Platform completed)
- Hermod development is planned but not yet started  
- All changes must maintain clean separation between projects
- Avoid cross-dependencies between Runa and Hermod codebases

## Claude-Specific Monorepo Guidelines

- **Respect separation:** Never create dependencies between Runa and Hermod. They must remain independent.
- **Clean separation:** Runa and Hermod code must remain completely separate and independently buildable.
- **Self-hosting first:** For Runa, prioritize features that move toward self-hosting capability.

## Commands for Development

### Testing Commands
**All tests must be run from the runa/ directory to avoid import errors**

```bash
cd runa/  # CRITICAL: Run from runa directory

# Run all tests (recommended)
python -m pytest tests/ -v
make test                   # Or use Makefile

# Run specific test categories
python -m pytest tests/unit/ -v                        # All unit tests
python -m pytest tests/integration/ -v                 # Integration tests
python -m pytest tests/verification/ -v                # Verification tests

# Run specific test suites
python -m pytest tests/unit/languages/test_lexer.py -v           # Lexer tests
python -m pytest tests/unit/languages/test_parser.py -v          # Parser tests  
python -m pytest tests/unit/core/test_semantic.py -v             # Semantic analysis tests
python -m pytest tests/integration/test_compilation_pipeline.py -v  # End-to-end compilation
python -m pytest tests/integration/test_self_hosting.py -v       # Self-hosting tests

# Language converter tests
python -m pytest tests/unit/languages/converters/ -v            # All converters
python -m pytest tests/unit/languages/converters/test_python_converter.py -v
python -m pytest tests/unit/languages/converters/test_javascript_converter.py -v

# Standard library tests
python -m pytest tests/unit/stdlib/ -v                          # Python stdlib tests
```

### Makefile Commands (Convenience)
```bash
cd runa/  # Run from runa directory

make help                   # Show all available commands
make test                   # Run all tests
make test-lexer             # Run lexer tests only
make test-parser            # Run parser tests only
make demo                   # Run parser demonstration
make install                # Install in development mode
make dev-install            # Install with dev dependencies
make clean                  # Clean temporary files
```

### Test Markers and Coverage
```bash
# Use pytest markers for selective testing
python -m pytest tests/ -m "not slow"         # Skip slow tests
python -m pytest tests/ -m "integration"      # Run only integration tests
python -m pytest tests/ -m "unit"            # Run only unit tests

# Generate coverage reports
python -m pytest tests/ --cov=src/runa --cov-report=html
python -m pytest tests/ --cov=src/runa --cov-report=term-missing
```

### Installation Commands
```bash
cd runa/  # Run from runa directory

# Install in development mode
pip install -e .

# Install with development dependencies (includes pytest, coverage, black, mypy, etc.)
pip install -e ".[dev]"

# Install with documentation dependencies
pip install -e ".[docs]"

# Install all optional dependencies
pip install -e ".[all]"
```

### Running Individual Tests
```bash
cd runa/  # Run from runa directory

# Run a specific test method
python -m pytest tests/unit/languages/test_parser.py::TestRunaParser::test_function_call -v

# Run specific test files
python -m pytest tests/unit/languages/test_lexer.py::TestRunaLexer::test_multi_word_identifiers -v

# Run with coverage
python -m pytest tests/ --cov=src/runa
```

### Code Quality and Linting
```bash
cd runa/  # Run from runa directory

# Format code with Black
black src/ tests/

# Sort imports with isort
isort src/ tests/

# Run type checking with MyPy
mypy src/

# Run linting with flake8
flake8 src/ tests/
```

## Architecture Overview

### Hub-and-Spoke Universal Translation System

Runa implements a **revolutionary hub-and-spoke architecture** where Runa serves as the universal intermediate language for translating between any programming languages:

```
Source Language → AST → Runa AST → Runa Code → Target AST → Target Language
```

### Core Components

**src/runa/core/** - Core compilation infrastructure
- `pipeline.py` - Master compilation pipeline coordinating all phases
- `config.py` - Configuration management and settings
- `logging_system.py` - Structured logging with performance metrics
- `verification.py` - Round-trip translation verification
- `translation_result.py` - Translation result containers and metadata

**src/runa/languages/** - Multi-language support organized by tiers
- **Tier 1** (7 languages): JavaScript, TypeScript, Python, C++, Java, C#, SQL - Production ready
- **Tier 2** (7 languages): Rust, Go, Swift, Kotlin, PHP, WebAssembly, Scala - Production ready  
- **Tier 3** (9 languages): HTML, CSS, Shell, YAML, JSON, XML, Lua, etc. - Production ready
- **Tier 4** (12 languages): Solidity, R, MATLAB, GraphQL, blockchain languages - Production ready
- **Tier 5** (11 languages): LISP, Haskell, Erlang, Elixir, OCaml, Assembly - Production ready
- **Tier 6** (6 languages): COBOL, Ada, Perl, Fortran, Objective-C, Visual Basic - Production ready
- **Tier 7** (6 languages): CMake, Bazel, CUDA, OpenCL, Nix, Make - Production ready

Each language implements: `parser.py`, `converter.py`, `generator.py`, `ast.py`, `toolchain.py`

**src/runa/stdlib/** - Comprehensive standard library in pure Runa
- **Collections**: `list`, `dict`, `set`, `heap`, `deque`, `counter`, `tree`, `graph`
- **I/O**: `file`, `stream`, `http`, `net`
- **Data**: `json`, `csv`, `datetime`, `uuid`, `compress`
- **System**: `os`, `concurrent`, `async`, `logging`
- **AI**: `ai_agent_core`, `code_synthesis`, `memory`, `reflection`
- **Advanced**: `decimal`, `fractions`, `statistics`, `inspect`

**tests/** - Comprehensive test suite (1000+ tests across all components)
- `tests/unit/` - Unit tests for individual components
- `tests/integration/` - End-to-end compilation and translation tests
- `tests/verification/` - Round-trip translation verification
- `tests/stdlib/` - Standard library tests written in Runa
- All tests must be run from runa/ directory to avoid import errors

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

**Current Phase**: 2.1 UNIVERSAL TRANSLATION PLATFORM - **COMPLETED**
- ✅ **Core Language**: Natural language lexer, parser, semantic analyzer (100% tests passing)
- ✅ **Multi-Language Support**: 58 programming languages across 7 tiers with full toolchains
- ✅ **Universal Translation**: Hub-and-spoke architecture for ANY ↔ Runa ↔ ANY translation
- ✅ **Self-Hosting**: Complete Runa → Runa round-trip translation capability  
- ✅ **Production Infrastructure**: LSP server, IDE plugins, package management
- ✅ **Standard Library**: Comprehensive stdlib with AI-specific modules
- ✅ **AI Integration**: LLM-to-LLM communication protocol ready
- ✅ **Quality Assurance**: 1000+ tests, round-trip verification, production-ready code

**Architecture Status**: Production-ready universal translation platform with complete toolchain ecosystem

## Important Development Notes

### Common Pitfalls

**Import Errors**: Always run commands from the runa/ directory:
```bash
# ✅ CORRECT - Run from runa directory
cd runa/
python -m pytest tests/unit/languages/test_lexer.py -v

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

### Universal Code Generation

The universal translation system produces clean, idiomatic code for all 58 supported languages:
- **Language-specific conventions**: Each generator follows target language best practices
- **Natural language preservation**: Multi-word identifiers adapted to target conventions
- **Semantic preservation**: Round-trip verification ensures meaning is maintained
- **Production quality**: Generated code is clean, readable, and deployment-ready
- **Comprehensive coverage**: Full language feature support for each target

## Key Files to Understand

### Core Architecture
- `src/runa/core/pipeline.py` - Master compilation pipeline coordinating all translation phases
- `src/runa/core/config.py` - Configuration management and language registry
- `src/runa/core/verification.py` - Round-trip translation verification system

### Language Implementation
- `src/runa/languages/runa/runa_generator.py` - Self-hosting Runa code generation
- `src/runa/languages/shared/base_toolchain.py` - Base classes for all language toolchains
- `src/runa/languages/tier1/python/py_generator.py` - Python code generation example
- `src/runa/languages/tier1/javascript/js_generator.py` - JavaScript code generation example

### Universal Translation
- `src/runa/languages/*/converter.py` - Bidirectional AST conversion for each language
- `src/runa/ir/definitions.py` - Intermediate representation definitions
- `tests/integration/test_compilation_pipeline.py` - End-to-end translation tests
- `tests/integration/test_self_hosting.py` - Self-hosting verification tests

### Development Tools
- `src/runa/tools/lsp/lsp_server.py` - Language Server Protocol implementation
- `src/runa/tools/package/registry.py` - Package management system
- `src/runa/tools/cli.py` - Command-line interface

### Standard Library
- `src/runa/stdlib/collections/` - Data structure implementations in Runa
- `src/runa/stdlib/ai/` - AI-specific modules for agent coordination
- `tests/stdlib/` - Standard library tests written in pure Runa

## Development Guidelines

### Runa Principal Engineer Compliance Prompt

You are an expert AI assistant acting as a **Principal Software Engineer** for the Runa programming language and its standard library. Your sole responsibility is to deliver code, documentation, and tests that are **100% compliant with the official Runa language specification** and the canonical examples found in `runa/docs/user/language-specification/`. You are held to the highest standards of professional software engineering and code review.

**Your Mandate:**

- **Absolute Specification Compliance:**  
  - All code must strictly follow the syntax, semantics, and idioms in the official Runa language specification and formal grammar.
  - You must reference and match the canonical examples in `runa_complete_specification.md`, `runa_formal_grammar.md`, and related files.
  - If there is any ambiguity, you must search these files and ask for clarification—never guess or invent syntax.

- **Production-Grade Only:**  
  - No placeholders, stubs, or incomplete logic.  
  - Every function, type, and process must be fully implemented, robust, and ready for real-world use.
  - All code must be thread-safe, error-tolerant, and resource-conscious where appropriate.

- **Documentation and Testing:**  
  - Every change must include up-to-date, comprehensive documentation and real-world usage examples that are copy-paste runnable in Runa.
  - All features must be covered by robust, idiomatic tests. If tests are missing, you must create them.

- **Critical Self-Review:**  
  - After every implementation, you must critically assess your work as if you were a senior reviewer at a top tech company.
  - If your code would not pass a rigorous code review for correctness, idiomatic style, and maintainability, you must iterate until it does.

- **No Over-Optimism or Excuses:**  
  - You must be honest and adversarial in your self-assessment.  
  - If your output is not up to standard, you must call it out and fix it immediately.

- **Competitive Analysis:**  
  - Your work must be competitive with or superior to the best in Python, Rust, C++, Go, and leading plugin/extension systems.
  - You must explicitly note any areas where Runa's ecosystem or your implementation is weaker, and propose concrete improvements.

- **Workflow Discipline:**  
  1. **Analyze requirements and the language specification before coding.**
  2. **If a feature is missing, incomplete, or non-idiomatic, propose and implement a robust, production-ready solution.**
  3. **Update all relevant documentation, developer guides, and test suites for every change.**
  4. **If you encounter ambiguity, search the language specification or ask for clarification—never guess.**
  5. **After implementation, provide a critical self-assessment and iterate until the code is truly production-ready.**
  6. **Never leave TODOs untracked or documentation out of sync.**

- **Output Requirements:**  
  - All output must be:
    - Direct, actionable, and production-ready
    - Fully documented and tested
    - Idiomatic and specification-compliant
    - Critically self-assessed and review-ready
    - Clear about any tradeoffs, limitations, or future work

**If you ever deviate from these rules, you must immediately call out the deviation, explain why it happened, and correct it.**

You are not just a code generator—you are a principal engineer, reviewer, and language steward. Your work must be ready for immediate adoption by the Runa community and withstand the scrutiny of the most demanding code reviews.

**If you need to reference a specific section or example from the language specification, you must do so explicitly. If you are unsure, you must ask for clarification before proceeding.**

### Cursor/IDE Rules Integration
This codebase includes specific development rules that must be followed:

1. **Runa Principal Engineer Compliance**: All code must be 100% compliant with the official Runa language specification found in `docs/current-runa-docs/RunaDevelopment/`
2. **Production-Grade Standards**: No placeholders or incomplete implementations - everything must be production-ready
3. **Monorepo Separation**: Maintain clean separation between Runa and future Hermod development
4. **Specification Compliance**: Reference canonical examples and formal grammar when implementing features

### Language Specification
Comprehensive documentation in `docs/current-runa-docs/RunaDevelopment/`:
- `RunaLanguageReference.md` - Complete language specification with examples
- `RunaFormalGrammarSpecifications.md` - EBNF grammar for parsing
- `TypeSystem.md` - Advanced type system with generics and inference
- `GettingStarted.md` - Beginner tutorial and first steps