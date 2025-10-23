# Contributing to Runa Programming Language

Thank you for your interest in contributing to Runa! This document provides guidelines for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Environment](#development-environment)
- [How to Contribute](#how-to-contribute)
- [Code Style Guidelines](#code-style-guidelines)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Areas We Need Help](#areas-we-need-help)
- [License Agreement](#license-agreement)

## Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.MD) before contributing.

## Getting Started

### Prerequisites

Runa is a self-hosting compiler with minimal external dependencies:

- **Assembler**: GNU `as` (we're building our own, but currently use system assembler)
- **Linker**: `gcc` or compatible linker
- **Supported Platforms**:
  - Linux (x86_64, ARM64, ARM32)
  - macOS/Darwin (x86_64, ARM64)
  - Windows (x86_64, ARM64)
  - BSD variants (FreeBSD, NetBSD, OpenBSD)
  - RISC-V (32/64-bit)
  - MIPS (32/64-bit)
  - PowerPC

### Clone the Repository

```bash
git clone https://github.com/Sybertnetics-Artificial-Intelligence/RunaLang.git
cd RunaLang
```

### Building Runa

The compiler uses a bootstrap process. The current development version is **v0.0.8.5**, and the first public release will be **v0.1.0**.

```bash
cd bootstrap/v0.0.8.5
# Build instructions will be added as build system stabilizes
```

**Note**: The build system is actively evolving. Check the version-specific README in `bootstrap/v0.0.8.5/` for current build instructions.

## Development Environment

### Recommended Setup

- **Editor**: Any text editor with syntax highlighting for similar languages (we're working on official Runa support)
- **Platform**: Development is supported on all platforms listed above
- **Version Control**: Git

### Project Structure

```
runa/
├── bootstrap/           # Bootstrap compiler versions
│   ├── v0.0.8.5/       # Current development version
│   ├── v0.0.9/         # Next version (in progress)
│   └── archived_*/     # Historical compiler versions
├── docs/               # Documentation
│   ├── dev/           # Developer documentation
│   └── user/          # User-facing documentation
├── CODE_OF_CONDUCT.MD
├── CONTRIBUTING.md
├── LICENSE.md
└── README.md
```

## How to Contribute

### Reporting Issues

- **Bugs**: Report via [GitHub Issues](https://github.com/Sybertnetics-Artificial-Intelligence/RunaLang/issues)
- **Feature Requests**: Open a discussion in [GitHub Discussions](https://github.com/Sybertnetics-Artificial-Intelligence/RunaLang/discussions)
- **Security Vulnerabilities**: Email security@sybertnetics.com (do not open public issues)

### Contributing Code

1. **Fork the repository** on GitHub
2. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** following our code style guidelines
4. **Write tests** for new functionality
5. **Commit your changes** with clear, descriptive messages
6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Open a Pull Request** against the `main` branch

## Code Style Guidelines

### Runa Code Style

Runa supports multiple syntax modes, but contributions should follow **Canon Mode** conventions:

#### Identifier Naming

**Canonical Form** (Preferred):
- Use spaced identifiers: `calculate area`, `user name`, `process data`
- Spaces and underscores are equivalent: `calculate area` ≡ `calculate_area`
- **Case sensitivity applies per word**:
  - `Calculate Area` ≡ `Calculate_Area` (same identifier)
  - `Calculate area` ≡ `Calculate_area` (same identifier)
  - `Calculate Area` ≠ `Calculate area` (different identifiers - "Area" vs "area")

**Non-Canonical Forms** (Avoid):
- camelCase: `calculateArea`
- PascalCase: `CalculateArea`

These are supported for interoperability but discouraged in Runa code. The auto-formatter will convert underscores to spaces.

#### Syntax Mode

- **Use Canon Mode** for all examples and library code
- Natural language operators: `multiplied by`, `is equal to`, `plus`
- Standard keywords: `Process`, `Type`, `If`, `Otherwise`, `For`, `While`, `Return`

Example:
```runa
Process called "calculate area" that takes width and height:
    Let area be width multiplied by height
    Return area
```

#### Comments and Documentation

- Use `Note:` for single-line comments
- Document public APIs thoroughly
- Include reasoning blocks for complex logic

### Formatting

- The Runa auto-formatter will handle spacing and normalization
- Indentation: 4 spaces (enforced by formatter)
- Line length: 100 characters recommended

## Testing

### Running Tests

Tests are located in the `tests/` directory within each bootstrap version:

```bash
cd bootstrap/v0.0.8.5/tests
./run_unit_tests.sh  # When available
```

### Writing Tests

- Write unit tests for all new functionality
- Place tests in the appropriate `tests/` directory
- Follow existing test patterns and naming conventions
- Ensure all tests pass before submitting a PR

### Test Coverage

We aim for comprehensive test coverage, especially for:
- Core compiler functionality
- Standard library functions
- Platform-specific code
- Edge cases and error handling

## Pull Request Process

### Before Submitting

1. **Ensure all tests pass**
2. **Run the auto-formatter** (when available)
3. **Update documentation** if you've changed APIs
4. **Write clear commit messages**:
   ```
   Add support for custom operators in lexer

   - Implemented operator precedence table
   - Added tests for operator parsing
   - Updated documentation
   ```

### PR Guidelines

- **One feature per PR**: Keep changes focused and atomic
- **Describe your changes**: Explain what and why, not just how
- **Reference issues**: Link to related issues or discussions
- **Be responsive**: Address review feedback promptly
- **Keep it clean**: Squash commits if requested

### Review Process

1. Maintainers will review your PR
2. Address any requested changes
3. Once approved, maintainers will merge your PR
4. Your contribution will be credited in release notes

## Areas We Need Help

### Open for Contributions

We welcome contributions in these areas:

#### Standard Libraries
- **Data structures**: Collections, algorithms, utilities
- **File I/O**: File system operations, parsing
- **Networking**: HTTP, WebSocket, TCP/UDP
- **Concurrency**: Actor patterns, async utilities
- **Math/Science**: Numerical computing, statistics
- **String processing**: Text manipulation, regex

#### Compiler Optimizations
- **Performance improvements**: Faster compilation, better codegen
- **Memory optimization**: Reduced allocator overhead
- **Platform-specific optimizations**: Architecture-specific improvements

#### Translation Modes
- **Language translators**: Runa ↔ other programming languages
- **Syntax converters**: Canon ↔ Developer mode tools
- **Documentation generators**: Code → natural language

#### Platform Support
- **Platform-specific testing**: Verify functionality on different OSes
- **Syscall implementations**: Platform-specific system calls
- **Calling conventions**: ABI compliance for all platforms

#### Documentation
- **Tutorials**: Beginner-friendly guides
- **Examples**: Real-world use cases
- **API documentation**: Library reference docs
- **Translation guides**: How to port code to/from Runa

### Restricted Areas (Internal Development Only)

The following core compiler components are maintained internally and **not open for external contributions** at this time:

- **Lexer**: Tokenization and lexical analysis
- **Parser**: Syntax parsing and AST generation
- **Code Generator**: Backend code generation

If you have suggestions for these components, please open a discussion rather than a PR.

**Note**: We may reconsider opening the core compiler to contributions in the future. Your feedback on this policy is welcome.

## License Agreement

### Understanding the RPLL

Runa is licensed under the **Runa Proprietary Limited License (RPLL)**. Please read [LICENSE.md](LICENSE.md) carefully before contributing.

### Contributor License Agreement

By contributing to this project, you agree that:

1. **You own the rights** to your contribution or have permission to contribute it
2. **You grant Sybertnetics AI** a perpetual, worldwide, non-exclusive, royalty-free license to use, modify, and distribute your contribution
3. **Your contribution is provided "as-is"** without warranties
4. **You understand** the RPLL terms and how they apply to the project

### Attribution

All contributors will be:
- Listed in project acknowledgments
- Credited in release notes for their contributions
- Recognized in the project's contributor graph

## Questions?

- **General questions**: [GitHub Discussions](https://github.com/Sybertnetics-Artificial-Intelligence/RunaLang/discussions)
- **Bug reports**: [GitHub Issues](https://github.com/Sybertnetics-Artificial-Intelligence/RunaLang/issues)
- **Security concerns**: security@sybertnetics.com
- **Code of Conduct violations**: conduct@sybertnetics.com
- **Discord**: [Join our community](https://discord.gg/dczenV2BJA)

---

**Thank you for helping build the future of programming!**

We're excited to have you contribute to Runa. Whether you're fixing a bug, adding a feature, writing documentation, or helping with translations, every contribution makes a difference.

*Runa™ is a trademark of Sybertnetics Artificial Intelligence*
