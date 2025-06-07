# Contributing to SyberSuite AI Development

Welcome to the SyberSuite AI development project! This document provides comprehensive guidelines for contributing to the Runa Programming Language and HermodIDE development.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Development Philosophy](#development-philosophy)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Standards](#code-standards)
- [Testing Requirements](#testing-requirements)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)

## Code of Conduct

### Our Commitment

We are committed to creating a welcoming, inclusive, and productive environment for all contributors, regardless of background, experience level, gender, gender identity and expression, sexual orientation, disability, personal appearance, body size, race, ethnicity, age, religion, or nationality.

### Expected Behavior

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

### Unacceptable Behavior

- Trolling, insulting/derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information without explicit permission
- Other conduct which could reasonably be considered inappropriate in a professional setting

## Development Philosophy

### Production-First Development

**CRITICAL REQUIREMENT**: Every line of code must be production-ready from day one.

- ❌ **NO PLACEHOLDER CODE**: No "TODO", "FIXME", or incomplete implementations
- ❌ **NO MOCK DATA**: All data structures and APIs must be fully functional
- ❌ **NO TEMPORARY SOLUTIONS**: All code must be designed for production use
- ✅ **COMPLETE IMPLEMENTATIONS**: Every function, class, and module must be fully implemented

### Quality Standards

- **95%+ Test Coverage**: All new code must include comprehensive tests
- **Type Safety**: Full type annotations required for all Python code
- **Error Handling**: Comprehensive error handling for all edge cases
- **Performance**: Code must meet performance benchmarks
- **Security**: Security-first approach with input validation

### Zero Redundancy Principle

- **Reuse First**: Always check for existing functions before creating new ones
- **DRY Principle**: Don't repeat yourself - consolidate duplicate functionality
- **Refactor**: Continuously improve code organization and eliminate redundancy

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Git
- Code editor with Python support (VS Code recommended)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd MonoRepo
   ```

2. **Set up Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements-dev.txt
   ```

3. **Install Runa in development mode**
   ```bash
   cd runa
   pip install -e .[dev]
   ```

4. **Run tests to verify setup**
   ```bash
   pytest tests/ -v
   ```

5. **Set up pre-commit hooks**
   ```bash
   pre-commit install
   ```

## Development Workflow

### Branch Strategy

- **main**: Production-ready code only
- **develop**: Integration branch for new features
- **feature/\***: Individual feature development branches
- **fix/\***: Bug fix branches
- **hotfix/\***: Critical production fixes

### Feature Development Process

1. **Create feature branch from develop**
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/your-feature-name
   ```

2. **Implement feature following standards**
   - Write comprehensive tests first (TDD approach)
   - Implement feature with complete error handling
   - Add/update documentation
   - Ensure 95%+ test coverage

3. **Validate implementation**
   ```bash
   # Run all tests
   pytest tests/ -v --cov=src/runa --cov-fail-under=95
   
   # Check code quality
   black src/ tests/
   flake8 src/ tests/
   mypy src/runa/
   bandit -r src/runa/
   ```

4. **Commit changes**
   ```bash
   git add .
   git commit -m "feat: implement [feature description]"
   ```

5. **Push and create pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

### Commit Message Format

Use conventional commit format:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code formatting changes
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(lexer): add support for multi-word identifiers
fix(parser): handle empty function parameter lists
docs(api): update AST node documentation
test(vm): add performance benchmarks for instruction execution
```

## Code Standards

### Python Code Style

- **Formatting**: Use Black with 88-character line length
- **Import Organization**: Use isort with Black-compatible settings
- **Type Hints**: All functions must have complete type annotations
- **Docstrings**: All public functions, classes, and modules must have docstrings

### Code Quality Checklist

Before submitting code, ensure it passes all checks:

```bash
# Format code
black src/ tests/
isort src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/runa/

# Security analysis
bandit -r src/runa/

# Test coverage
pytest tests/ --cov=src/runa --cov-fail-under=95
```

### Performance Requirements

- **Lexer**: >10,000 tokens per second
- **Parser**: >1,000 statements per second  
- **VM**: >100,000 instructions per second
- **Compilation**: <100ms for typical programs

## Testing Requirements

### Test Categories

1. **Unit Tests**: Test individual functions and classes
2. **Integration Tests**: Test component interactions
3. **Performance Tests**: Benchmark critical paths
4. **Security Tests**: Validate input handling and security

### Test Structure

```python
def test_feature_functionality():
    """Test that the feature works correctly."""
    # Arrange
    input_data = create_test_input()
    
    # Act
    result = feature_function(input_data)
    
    # Assert
    assert result == expected_output
    assert result.is_valid()

def test_feature_error_handling():
    """Test that the feature handles errors appropriately."""
    with pytest.raises(ExpectedError):
        feature_function(invalid_input)
```

### Test Requirements

- **Coverage**: Minimum 95% line and branch coverage
- **Edge Cases**: Test all error conditions and boundary cases
- **Performance**: Include benchmark tests for critical functions
- **Fixtures**: Use pytest fixtures for common test data

## Documentation

### Documentation Requirements

- **Docstrings**: All public APIs must have comprehensive docstrings
- **Type Hints**: Complete type annotations for all functions
- **Examples**: Include usage examples in docstrings
- **Architecture**: Document design decisions and trade-offs

### Docstring Format

Use Google-style docstrings:

```python
def parse_expression(tokens: List[Token]) -> Expression:
    """Parse a sequence of tokens into an expression AST node.
    
    Args:
        tokens: List of tokens to parse
        
    Returns:
        Expression AST node representing the parsed expression
        
    Raises:
        ParseError: If tokens cannot be parsed as valid expression
        
    Examples:
        >>> tokens = tokenize("5 + 3")
        >>> expr = parse_expression(tokens)
        >>> expr.evaluate()
        8
    """
```

## Pull Request Process

### Before Submitting

1. **Ensure all tests pass**
2. **Verify 95%+ test coverage**
3. **Run all code quality checks**
4. **Update documentation**
5. **Add changelog entry if applicable**

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] All tests pass
- [ ] 95%+ test coverage maintained
- [ ] Performance benchmarks met

## Code Quality
- [ ] Code formatted with Black
- [ ] Imports organized with isort
- [ ] Type checking passes with mypy
- [ ] Security scan passes with bandit
- [ ] Linting passes with flake8

## Documentation
- [ ] Docstrings added/updated
- [ ] Examples included
- [ ] Architecture documented if applicable
```

### Review Process

1. **Automated Checks**: CI/CD pipeline runs all quality checks
2. **Code Review**: Two approvals required from core team members
3. **Testing**: Manual testing for complex features
4. **Merge**: Squash and merge to maintain clean history

## Issue Reporting

### Bug Reports

Use the bug report template:

```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- Runa version:
- Python version:
- Operating system:

## Additional Context
Any other relevant information
```

### Feature Requests

Use the feature request template:

```markdown
## Feature Description
Clear description of the proposed feature

## Motivation
Why is this feature needed?

## Proposed Implementation
How should this be implemented?

## Alternatives Considered
What other approaches were considered?

## Additional Context
Any other relevant information
```

## Development Phases

### Current Phase: Runa Language Development (Weeks 1-20)

Focus areas:
- Language core implementation
- Standard library development
- Performance optimization
- Documentation and examples

### Future Phases

- **Weeks 21-60**: Hermod Agent Development
- **Integration**: Runa + Hermod + IDE

## Getting Help

### Communication Channels

- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Development Team**: For architectural decisions and design reviews

### Resources

- [Project Master Plan](docs/00-START-HERE/Project%20Master%20Plan.md)
- [Development Guidelines](docs/00-START-HERE/Development%20Guidelines%20and%20Prompt.md)
- [Runa Language Reference](docs/current-runa-docs/RunaDevelopment/RunaLanguageReference.md)
- [Architecture Guide](docs/00-START-HERE/HermodIDE%20Architecture%20Guide.md)

## Recognition

We value all contributions to the project. Contributors will be recognized in:

- Contributor list in README
- Release notes for significant contributions
- Project documentation for major features

Thank you for contributing to the future of AI-assisted development! 🚀 