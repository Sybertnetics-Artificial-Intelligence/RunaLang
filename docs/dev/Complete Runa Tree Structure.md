# Complete Runa Tree Structure

## Overview
This document provides a comprehensive view of the complete Runa project tree structure, including all directories, files, and their purposes. The structure is organized to support both the Runa programming language development and the future Hermod AI system.

## Root Structure
```
MonoRepo/
├── docs/                           # Proprietary documentation (excluded from version control)
│   ├── CORE/                       # Core proprietary documentation
│   ├── CORE GUIDANCE DOCS/         # Development guidelines and plans
│   ├── current-runa-docs/          # Current Runa development documentation
│   ├── detailed-specs/             # Detailed specifications for both projects
│   ├── prompts-and-plans/          # Development prompts and plans
│   └── SyberCraftLLM Docs/         # LLM training and development documentation
├── runa/                           # Runa programming language project
│   ├── __init__.py                 # Python package initialization
│   ├── compiler/                   # Runa compiler implementation
│   ├── dev-tools/                  # Development tools and utilities
│   ├── docker/                     # Docker configuration files
│   ├── docker-compose.yml          # Docker Compose configuration
│   ├── Dockerfile                  # Docker container definition
│   ├── docs/                       # Public-facing documentation
│   ├── examples/                   # Example Runa programs
│   ├── fix_all_dataclass.py        # Utility script for dataclass fixes
│   ├── ide-plugins/                # IDE plugin implementations
│   ├── rt/                         # Runtime implementation
│   ├── rust/                       # Rust implementation components
│   ├── src/                        # Main source code
│   └── tests/                      # Test suites
└── hermod/                         # Hermod AI system (future development)
```

## Runa Project Structure

### Core Source Code (`runa/src/runa/`)
```
src/runa/
├── core/                           # Core language components
│   ├── __init__.py
│   ├── base_components.py          # Base language components
│   ├── config.py                   # Configuration management
│   └──other core files]
├── ir/                             # Intermediate Representation
│   ├── __init__.py
│   ├── definitions.py              # IR type definitions
│   └── runa_cfg_builder.py         # Control flow graph builder
├── languages/                      # Language translation tiers
│   ├── __init__.py
│   ├── runa/                       # Runa language implementation
│   ├── shared/                     # Shared language utilities
│   ├── tier1/                      # Tier 1 languages (Python, Java, JS, TS, C++, C#, SQL)
│   ├── tier2/                      # Tier 2anguages (Rust, Go, Swift, Kotlin, PHP, WASM, Scala)
│   ├── tier3/                      # Tier 3nguages (HTML, CSS, Shell, HCL, YAML, JSON, XML, Lua, TOML, INI, AssemblyScript)
│   ├── tier4/                      # Tier 4 languages (R, Julia, Matlab, GraphQL, Solidity + 9 blockchain languages)
│   ├── tier5/                      # Tier 5ges (LISP, Haskell, Erlang, Elixir, OCaml, Clojure, Assembly, LLVM IR, Starlark, Rholang)
│   ├── tier6/                      # Tier 6 languages (Objective-C, Visual Basic, COBOL, Ada, Perl, Fortran, Tcl)
│   └── tier7/                      # Tier7nguages (Nix, Make, CMake, Bazel, CUDA, OpenCL)
├── stdlib/                         # Standard Library Modules
│   ├── ai/                         # AI-specific modules (moved to top-level)
│   ├── argparse/                   # Command-line argument parsing
│   │   └── argparse.runa
│   ├── async/                      # Asynchronous programming
│   │   └── async.runa
│   ├── builtins/                   # Built-in functions and types
│   │   └── functions.runa
│   ├── calendar/                   # Calendar and date utilities
│   │   └── calendar.runa
│   ├── collections/                # Advanced data structures
│   │   ├── list.runa
│   │   ├── set.runa
│   │   ├── dict.runa
│   │   ├── deque.runa
│   │   ├── counter.runa
│   │   ├── heap.runa
│   │   ├── tree.runa
│   │   ├── graph.runa
│   │   ├── priority_queue.runa
│   │   ├── default_dict.runa
│   │   ├── chain_map.runa
│   │   └── ordered_dict.runa
│   ├── compress/                   # Compression utilities
│   │   └── compress.runa
│   ├── concurrent/                 # Concurrency utilities
│   │   └── concurrent.runa
│   ├── config/                     # Configuration management
│   │   └── config.runa
│   ├── csv/                        # CSV processing
│   │   └── csv.runa
│   ├── datetime/                   # Date and time utilities
│   │   └── datetime.runa
│   ├── decimal/                    # Decimal arithmetic
│   │   └── decimal.runa
│   ├── fractions/                  # Fraction arithmetic
│   │   └── fractions.runa
│   ├── http/                       # HTTP client and server
│   │   └── http.runa
│   ├── inspect/                    # Introspection utilities
│   │   └── inspect.runa
│   ├── io/                         # Input/Output utilities
│   │   ├── file.runa
│   │   └── io.runa
│   ├── json/                       # JSON processing
│   │   └── json.runa
│   ├── logging/                    # Logging utilities
│   │   └── logging.runa
│   ├── math/                       # Mathematical functions
│   │   ├── core.runa
│   │   └── ai_math.runa
│   ├── net/                        # Network utilities
│   │   └── net.runa
│   ├── os/                         # Operating system interface
│   │   └── os.runa
│   ├── site/                       # Site configuration
│   │   └── site.runa
│   ├── statistics/                 # Statistical functions
│   │   └── statistics.runa
│   ├── string/                     # String utilities
│   │   └── string.runa
│   ├── text/                       # Text processing
│   │   ├── regex.runa
│   │   └── text.runa
│   ├── time/                       # Time utilities
│   │   └── time.runa
│   ├── traceback/                  # Error traceback utilities
│   │   └── traceback.runa
│   ├── types/                      # Type system utilities
│   │   └── types.runa
│   └── uuid/                       # UUID generation
│       └── uuid.runa
├── ai/                             # AI System Modules (Top-level)
│   ├── agent/                      # Agent system
│   │   ├── core.runa
│   │   ├── registry.runa
│   │   └── lifecycle.runa
│   ├── intention/                  # Goal management
│   │   ├── core.runa
│   │   └── retry.runa
│   ├── memory/                     # Memory systems
│   │   ├── episodic.runa
│   │   ├── semantic.runa
│   │   ├── vector.runa
│   │   └── policies.runa
│   ├── reasoning/                  # Reasoning engine
│   │   ├── engine.runa
│   │   ├── rules.runa
│   │   └── contradictions.runa
│   ├── comms/                      # Communication
│   │   ├── messaging.runa
│   │   └── channels.runa
│   ├── protocols/                  # Interaction protocols
│   │   └── contracts.runa
│   ├── trust/                      # Trust management
│   │   └── scoring.runa
│   ├── context/                    # Context management
│   │   └── window.runa
│   ├── tools/                      # Tool registry
│   │   └── registry.runa
│   ├── strategy/                   # Strategy management
│   │   └── manager.runa
│   ├── meta/                       # Meta-cognition
│   │   └── confidence.runa
│   ├── prompt/                     # Prompt management
│   │   └── builder.runa
│   └── token/                      # Tokenization
│       └── tokenizer.runa
├── llm/                            # LLM Orchestration
│   ├── core.runa                   # Core LLM interface
│   ├── router.runa                 # Model routing
│   ├── chain.runa                  # Reasoning chains
│   ├── memory.runa                 # LLM memory
│   ├── agent.runa                  # LLM agent
│   ├── tools.runa                  # LLM tools
│   ├── evaluation.runa             # LLM evaluation
│   ├── embedding.runa              # LLM embeddings
│   └── graph.runa                  # LLM graph operations
├── train/                          # Neural Network Training
│   ├── nn/                         # Neural network layers
│   │   ├── layers.runa
│   │   └── attention.runa
│   ├── model/                      # Model configuration
│   │   ├── config.runa
│   │   └── builder.runa
│   ├── tokenizer/                  # Tokenization
│   │   └── bpe.runa
│   ├── dataset/                    # Dataset management
│   │   └── loader.runa
│   ├── train/                      # Training loop
│   │   └── loop.runa
│   ├── opt/                        # Optimizers
│   │   └── adamw.runa
│   ├── metrics/                    # Training metrics
│   │   └── scoring.runa
│   ├── distribute/                 # Distributed training
│   │   └── ddp.runa
│   ├── experiment/                 # Experiment tracking
│   │   └── tracking.runa
│   └── compile/                    # Model compilation
│       └── export.runa
└── tools/                          # Development Tools
    ├── __init__.py
    ├── ai/                         # AI development tools
    │   └── [AI tool files]
    ├── ci_cd/                      # CI/CD tools
    │   └──CI/CD files]
    ├── cli.py                      # Command-line interface
    ├── docgen/                     # Documentation generation
    │   └── [docgen files]
    ├── ide/                        # IDE integration
    │   └──IDE files]
    ├── lsp/                        # Language Server Protocol
    │   └──LSP files]
    ├── package/                    # Package management
    │   └── [package files]
    └── testing/                    # Testing utilities
        └── [testing files]
```

### Documentation (`runa/docs/`)
```
docs/
├── api/                            # API documentation
│   ├── compiler/                   # Compiler API
│   │   └── core.md
│   ├── lsp/                        # LSP API
│   │   └── core.md
│   └── README.md
├── dev/                            # Development documentation
│   ├── Runa Standard Library Manifesto.md
│   └── Complete Runa Tree Structure.md
└── user/                           # User documentation
    ├── guides/                     # User guides
    │   ├── GETTING_STARTED.md
    │   ├── LANGUAGE_TIERS.md
    │   └── USER_GUIDE.md
    ├── language-specification/     # Language specification
    │   ├── runa_annotation_system.md
    │   ├── runa_complete_specification.md
    │   ├── runa_field_method_access.md
    │   └──other spec files]
    ├── standard-library/           # Standard library documentation
    │   ├── ai_agent_core_module.md
    │   ├── argparse_module.md
    │   ├── async_module.md
    │   └── [other module docs]
    └── README.md
```

### Examples (`runa/examples/`)
```
examples/
├── advanced/                       # Advanced examples
│   └── deque_example.runa
├── basic/                          # Basic examples
│   ├── basic_program.runa
│   ├── calculator.runa
│   ├── counter_example.runa
│   └── [other basic examples]
├── intermediate/                   # Intermediate examples
│   ├── functions.runa
│   ├── heap_example.runa
│   └── pattern_matching.runa
├── package_examples/               # Package examples
│   └── runa.toml
├── projects/                       # Project examples
├── README.md
├── showcases/                      # Showcase examples
└── templates/                      # Template examples
```

### Tests (`runa/tests/`)
```
tests/
├── __init__.py
├── integration/                    # Integration tests
│   ├── __init__.py
│   ├── test_compilation_pipeline.py
│   └── test_self_hosting.py
├── proof_of_concept/               # Proof of concept tests
│   ├── __init__.py
│   ├── outputs/                    # Test outputs by tier
│   │   ├── tier1/
│   │   ├── tier2/
│   │   ├── tier3/
│   │   ├── tier4/
│   │   ├── tier5/
│   │   ├── tier6/
│   │   └── tier7/
│   ├── README.md
│   ├── reports/                    # Test reports
│   ├── test_framework.py
│   └── other PoC files]
├── stdlib/                         # Standard library tests
│   ├── test_ai_agent_core.runa
│   ├── test_argparse.runa
│   ├── test_async.runa
│   └── [other stdlib tests]
├── unit/                           # Unit tests
│   ├── __init__.py
│   ├── ai/                         # AI unit tests
│   │   ├── learning/
│   │   │   └── [learning test files]
│   │   └── memory/
│   │       └── [memory test files]
│   ├── core/                       # Core unit tests
│   │   ├── __init__.py
│   │   ├── test_semantic_types.py
│   │   └── test_semantic.py
│   ├── languages/                  # Language unit tests
│   │   ├── __init__.py
│   │   ├── converters/
│   │   │   └── [converter test files]
│   │   ├── test_lexer.py
│   │   └── [other language tests]
│   ├── stdlib/                     # Standard library unit tests
│   │   ├── test_compress.py
│   │   ├── test_concurrent.py
│   │   ├── test_http.py
│   │   └── [other stdlib unit tests]
│   └── tools/                      # Tools unit tests
│       └── __init__.py
└── verification/                   # Verification tests
    ├── __init__.py
    └── test_phase_1_fixes.py
```

### Rust Implementation (`runa/rust/`)
```
rust/
├── Cargo.lock                      # Rust dependency lock file
├── Cargo.toml                      # Rust project configuration
├── README.md                       # Rust implementation README
├── runa-common/                    # Common Rust components
│   ├── Cargo.toml
│   └── src/
│       ├── ast.rs                  # Abstract Syntax Tree
│       ├── bytecode.rs             # Bytecode representation
│       └── lib.rs                  # Library entry point
├── runa-rt/                        # Runtime implementation
│   ├── Cargo.toml
│   └── src/
│       ├── concurrency.rs          # Concurrency primitives
│       ├── ffi.rs                  # Foreign Function Interface
│       ├── lib.rs                  # Runtime library
│       └── os/                     # Operating system interface
│           ├── console.rs          # Console I/O
│           ├── file.rs             # File I/O
│           ├── mod.rs              # OS module
│           └── system/             # System utilities
│               └── [system files]
├── runac/                          # Runa compiler
│   ├── Cargo.toml
│   └── src/
│       ├── codegen.rs              # Code generation
│       ├── disassembler.rs         # Bytecode disassembler
│       ├── lexer.rs                # Lexical analysis
│       └── runac/                  # Compiler submodule
│           └── Cargo.toml
├── target/                         # Rust build artifacts
│   ├── CACHEDIR.TAG
│   ├── debug/                      # Debug build artifacts
│   │   ├── deps/                   # Dependencies
│   │   ├── examples/               # Example binaries
│   │   ├── incremental/            # Incremental compilation
│   │   └── [other debug files]
│   └── [other target directories]
└── tests/                          # Rust tests
    ├── basic/                      # Basic tests
    │   ├── simple_test.runa
    │   ├── test_basic.runa
    │   ├── test_complex.runa
    │   └── [other basic tests]
    ├── malformed/                  # Malformed input tests
    │   └── test_malformed.runa
    ├── README.md
    └── test_harness.rs             # Test harness
```

### IDE Plugins (`runa/ide-plugins/`)
```
ide-plugins/
├── intellij/                       # IntelliJ IDEA plugin
│   ├── build.gradle                # Gradle build configuration
│   └── src/
│       ├── main/
│       │   ├── java/               # Java source code
│       │   └── resources/          # Plugin resources
│       └── [other IntelliJ files]
└── vscode/                         # Visual Studio Code extension
    ├── language-configuration.json # Language configuration
    ├── package.json                # Extension manifest
    ├── snippets/                   # Code snippets
    │   └── runa.json
    ├── src/
    │   └── extension.ts            # Extension source
    ├── syntaxes/                   # Syntax highlighting
    │   └── runa.tmLanguage.json
    └── tsconfig.json               # TypeScript configuration
```

### Docker Configuration (`runa/docker/`)
```
docker/
├── deployment.yml                  # Deployment configuration
├── init-db.sql                     # Database initialization
├── nginx.conf                      # Nginx configuration
└── [other Docker files]
```

## Key Features of the Structure

### 1. **Modular Design**
- Clear separation between core language, standard library, AI modules, and tools
- Each module is self-contained with its own documentation and tests
- Easy to maintain and extend individual components

### 2. **Multi-Language Support**
- 65+ programming languages supported across 7 tiers
- Each tier focuses on specific language families and use cases
- Comprehensive translation pipeline from Runa to target languages

### 3. **AI-First Architecture**
- AI modules are top-level, not buried in stdlib
- Dedicated LLM orchestration and training frameworks
- Agent-centric design with memory, reasoning, and communication systems

### 4prehensive Testing**
- Unit tests for individual components
- Integration tests for complete pipelines
- Proof of concept tests for language translation
- Standard library tests for all modules

### 5. **Development Tools**
- IDE plugins for IntelliJ and VS Code
- CLI tools for development workflow
- Documentation generation
- Package management utilities

### 6. **Production Ready**
- Docker containerization
- CI/CD pipeline support
- Comprehensive error handling
- Performance optimization tools

## Future Expansion

The structure is designed to support:
- **Hermod AI System**: Separate top-level directory for the AI system
- **Additional Language Tiers**: Easy addition of new language support
- **Advanced AI Features**: Expandable AI modules and capabilities
- **Enterprise Features**: Security, monitoring, and deployment tools
- **Community Contributions**: Clear contribution guidelines and tools

This structure provides a solid foundation for both the Runa programming language and the future Hermod AI system, with clear separation of concerns and comprehensive tooling for development, testing, and deployment. 