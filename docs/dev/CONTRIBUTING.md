# Contributing to Runa

Thank you for your interest in contributing to Runa! This document provides guidelines for contributing to the Runa programming language project.

## Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please be respectful and professional in all interactions.

## How to Contribute

### Reporting Issues

- Use the GitHub issue tracker to report bugs or suggest features
- Before creating a new issue, search existing issues to avoid duplicates
- Provide clear, detailed descriptions with steps to reproduce
- Include relevant code examples and error messages

### Submitting Changes

1. **Fork the repository** and create a feature branch
2. **Make your changes** following our coding standards
3. **Test your changes** thoroughly
4. **Submit a pull request** with a clear description

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git

### Getting Started

```bash
# Clone the repository
git clone https://github.com/sybertneticsaisolutions/runa.git
cd runa

# Install development dependencies
pip install -e .

# Run tests
python -m pytest runa/tests/
```

## Coding Standards

### Python Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write docstrings for all public functions and classes
- Maximum line length: 88 characters (Black formatter standard)

### Runa Language Features

- Use descriptive, natural language naming
- Follow existing patterns in the codebase
- Ensure backward compatibility when possible
- Document new language features thoroughly

### Testing

- Write unit tests for new functionality
- Maintain or improve test coverage
- Use descriptive test names
- Include both positive and negative test cases

### Documentation

- Update relevant documentation for changes
- Include examples in docstrings
- Update the language reference for new features
- Keep documentation clear and beginner-friendly

## Project Structure

```
runa/
├── compiler/           # Core compiler components
│   ├── lexer.py       # Tokenization
│   ├── parser.py      # Parsing
│   ├── semantic.py    # Semantic analysis
│   └── ast_nodes.py   # AST node definitions
├── stdlib/            # Standard library modules
│   ├── math.py        # Mathematical functions
│   ├── string.py      # String operations
│   ├── file.py        # File system operations
│   └── ...
├── tests/             # Test suite
└── examples/          # Example programs
```

## Types of Contributions

### Bug Fixes

- Fix reported issues
- Improve error handling
- Resolve edge cases
- Optimize performance

### New Features

- Language syntax enhancements
- Standard library additions
- Compiler improvements
- Development tools

### Documentation

- Tutorial improvements
- API documentation
- Code examples
- Translation to other languages

### Testing

- Increase test coverage
- Add integration tests
- Performance benchmarks
- Fuzzing tests

## Pull Request Process

1. **Create a descriptive branch name**: `feature/pattern-matching` or `fix/parser-error`
2. **Write clear commit messages**: Use imperative mood, be specific
3. **Include tests**: All new functionality must include tests
4. **Update documentation**: Reflect changes in relevant docs
5. **Keep PRs focused**: One feature or fix per pull request
6. **Respond to feedback**: Address review comments promptly

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code cleanup

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## Documentation
- [ ] Code comments updated
- [ ] Documentation updated
- [ ] Examples added/updated
```

## Release Process

### Version Numbers

We use semantic versioning (SemVer):
- Major: Breaking changes
- Minor: New features, backward compatible
- Patch: Bug fixes, backward compatible

### Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] Version number bumped
- [ ] Changelog updated
- [ ] Tagged release created

## Community Guidelines

### Communication

- Use clear, professional language
- Be constructive in feedback
- Ask questions when unsure
- Help others learn and grow

### Collaboration

- Respect different viewpoints
- Be open to feedback
- Share knowledge freely
- Acknowledge contributions

### Quality Standards

- Prioritize code quality over speed
- Test thoroughly before submitting
- Follow established patterns
- Document your work

## Getting Help

### Resources

- **Documentation**: Check existing docs first
- **Issues**: Search GitHub issues
- **Discussions**: Use GitHub discussions for questions
- **Code**: Review existing code for patterns

### Contact

- GitHub Issues: Technical problems
- GitHub Discussions: General questions
- Email: maintainers@sybertnetics.com (for sensitive matters)

## Recognition

We appreciate all contributors! Contributors will be:
- Listed in the project's contributor list
- Acknowledged in release notes
- Invited to contribute to project direction

## License

By contributing to Runa, you agree that your contributions will be licensed under the same license as the project.

## Frequently Asked Questions

**Q: I'm new to open source. How can I help?**
A: Start with documentation improvements, write examples, or tackle "good first issue" labeled items.

**Q: Can I add a new language feature?**
A: Yes! Discuss the feature first in an issue to ensure it aligns with project goals.

**Q: How do I run the test suite?**
A: Use `python -m pytest runa/tests/` to run all tests.

**Q: What if my pull request gets rejected?**
A: Don't worry! Use the feedback to improve and resubmit. All contributions are valuable learning experiences.

## Thank You

Your contributions help make Runa better for everyone. Whether it's reporting a bug, writing documentation, or adding features, every contribution matters!