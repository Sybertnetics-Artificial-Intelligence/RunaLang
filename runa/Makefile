# Runa Development Makefile
# Provides convenient commands for development, testing, and maintenance

.PHONY: help test test-lexer test-parser clean install dev-install demo

# Default target
help:
	@echo "Runa Development Commands:"
	@echo ""
	@echo "  test         - Run all tests (lexer + parser)"
	@echo "  test-lexer   - Run only lexer tests"
	@echo "  test-parser  - Run only parser tests"
	@echo "  demo         - Run comprehensive parser demonstration"
	@echo "  clean        - Clean temporary files"
	@echo "  install      - Install Runa in development mode"
	@echo "  dev-install  - Install with development dependencies"
	@echo ""

# Test commands
test:
	python -m pytest runa/tests/ -v

test-lexer:
	python -m pytest runa/tests/test_lexer.py -v

test-parser:
	python -m pytest runa/tests/test_parser.py -v

# Development commands
demo:
	@echo "🚀 Running Runa Parser Demonstration..."
	@python -c "from runa.compiler import parse_runa_source; from collections import Counter; \
	source = open('runa/examples/parser_demo.runa').read(); \
	program = parse_runa_source(source); \
	print(f'✅ Parsed {len(program.statements)} statements'); \
	types = [type(s).__name__ for s in program.statements]; \
	counts = Counter(types); \
	print('Statement types:'); \
	[print(f'  {t}: {c}') for t, c in sorted(counts.items())]"

install:
	pip install -e .

dev-install:
	pip install -e ".[dev]"

# Maintenance commands
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 