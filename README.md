# SyberSuite AI Development - MonoRepo

## Overview

This monorepo contains the complete SyberSuite AI ecosystem development, including:

- **Runa Programming Language**: A natural language programming language that serves as AI agents' native thought language
- **HermodIDE**: An AI agent embodied as an integrated development environment (IDE IS the agent)

## Project Structure

```
├── runa/                    # Runa Programming Language
│   ├── src/                 # Core language implementation
│   ├── tests/               # Comprehensive test suite
│   ├── examples/            # Language examples and tutorials
│   └── docs/                # Language-specific documentation
├── hermod-ide/              # HermodIDE Implementation
│   ├── src/                 # IDE and AI agent code
│   ├── tests/               # IDE test suite
│   └── docs/                # IDE-specific documentation
├── shared/                  # Shared utilities and libraries
├── docs/                    # Project documentation
├── tools/                   # Development and build tools
└── deploy/                  # Deployment configurations
```

## Development Status

- **Runa Language**: Phase 1 - Week 1 (In Progress)
- **HermodIDE**: Not Started (begins after Runa completion)

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+ (for IDE development)
- Git

### Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd MonoRepo

# Set up Python development environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements-dev.txt

# Run Runa tests
cd runa
python -m pytest tests/

# Build Runa
python setup.py build
```

## Contributing

See [Contributing Guidelines](CONTRIBUTING.md) for development standards and procedures.

## Architecture

- **Production-First Development**: No placeholders, complete implementations only
- **Zero Redundancy**: Reuse existing functions, create new only when necessary
- **95%+ Test Coverage**: Comprehensive testing required for all components
- **Enterprise Quality**: Security-first, performance-optimized code

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Documentation

- [Project Master Plan](docs/00-START-HERE/Project%20Master%20Plan.md)
- [Development Guidelines](docs/00-START-HERE/Development%20Guidelines%20and%20Prompt.md)
- [Runa Language Reference](docs/current-runa-docs/RunaDevelopment/RunaLanguageReference.md)
- [HermodIDE Architecture](docs/00-START-HERE/HermodIDE%20Architecture%20Guide.md) 