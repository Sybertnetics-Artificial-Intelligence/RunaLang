# Contributing to Runa

Thank you for your interest in contributing to the Runa programming language! This document provides guidelines and instructions for contributing to the project.

## Development Philosophy

Runa follows these core development principles:

1. **Production-First Development**: Every line of code must be production-ready. No temporary, mock, placeholder, or "TODO" code.
2. **Zero Redundancy Principle**: Reuse existing functions and components whenever possible. Create new code only when no suitable existing solution exists.
3. **Current Functionality Preservation**: All existing system capabilities must be maintained during development.

## Code Quality Standards

- **Full Implementation**: Every function, class, and module must be completely implemented.
- **Error Handling**: Comprehensive error handling for all edge cases.
- **Input Validation**: Validate all inputs and parameters.
- **Documentation**: Complete docstrings and inline comments.
- **Testing**: Unit tests for all new code (95%+ coverage target).

## Getting Started

### Setting Up Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/sybertnetics/runa.git
   cd runa
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

### Development Workflow

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes, following our coding standards.

3. Run tests:
   ```bash
   pytest
   ```

4. Run linters:
   ```bash
   black .
   flake8
   mypy .
   ```

5. Commit your changes with a descriptive message:
   ```bash
   git commit -m "feat: Add support for X feature"
   ```

6. Push to your branch:
   ```bash
   git push origin feature/your-feature-name
   ```

7. Create a pull request.

## Pull Request Process

1. Ensure your code passes all tests and linting checks.
2. Update documentation to reflect any changes.
3. Include test cases for new functionality.
4. Your PR will be reviewed by core contributors.
5. Address any feedback or requested changes.
6. Once approved, your PR will be merged.

## Code Style Guidelines

- Follow PEP 8 for Python code.
- Use clear, descriptive variable and function names.
- Add comprehensive docstrings to all functions, classes, and modules.
- Include type hints for all function parameters and return values.

## Testing Guidelines

- Write unit tests for all new code.
- Aim for at least 95% test coverage.
- Test edge cases and error conditions.
- Make sure tests are deterministic and don't rely on external resources.

## Documentation Guidelines

- Update the relevant documentation for any changes you make.
- Document both the "what" and the "why" of your code.
- Provide examples for complex functionality.

## Reporting Issues

If you find a bug or have a suggestion for improvement:

1. Check if the issue already exists in the issue tracker.
2. If not, open a new issue with a descriptive title and detailed information.
3. Include steps to reproduce for bugs, or clear descriptions for feature requests.

## Community Guidelines

- Be respectful and considerate in all communications.
- Welcome newcomers and help them get started.
- Focus on constructive feedback and solutions.

Thank you for contributing to Runa! 