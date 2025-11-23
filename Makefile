.PHONY: help install dev-install lint format test test-cov clean docs build

## Default target
help:
	@echo "NIFCLOUD SDK for Python - Development Commands"
	@echo ""
	@echo "Available targets:"
	@echo ""
	@echo "  install         Install dependencies"
	@echo "  dev-install     Install with development dependencies"
	@echo "  lint            Run linter, type checker, and security scanner"
	@echo "  format          Format code with ruff"
	@echo "  test            Run unit tests"
	@echo "  test-cov        Run tests with coverage report"
	@echo "  test-acceptance Run acceptance tests"
	@echo "  docs            Generate documentation"
	@echo "  docs-serve      Serve documentation locally"
	@echo "  clean           Remove generated files and cache"
	@echo "  build           Build distribution packages"
	@echo "  help            Show this help message"
	@echo ""

## Installation
install:
	@echo "Installing dependencies..."
	uv sync

dev-install:
	@echo "Installing with development dependencies..."
	uv sync

## Code Quality
lint:
	@echo "Linting code..."
	uv run ruff check .
	@echo "Type checking..."
	uv run mypy --ignore-missing-imports nifcloud
	@echo "Security scanning..."
	uv run bandit -r nifcloud -ll
	@echo "✅ Lint checks passed"

format:
	@echo "Formatting code..."
	uv run ruff check . --fix
	uv run ruff format .
	@echo "✅ Code formatted"

## Testing
test:
	@echo "Running unit tests..."
	uv run pytest tests/unit -v

test-cov:
	@echo "Running tests with coverage..."
	uv run pytest tests/unit --cov=nifcloud --cov-report=term-missing --cov-report=html
	@echo "✅ Coverage report generated: htmlcov/index.html"

test-acceptance:
	@echo "Running acceptance tests..."
	uv run pytest tests/acceptance/minimal -v

test-all: test test-acceptance
	@echo "✅ All tests passed"

## Documentation
docs:
	@echo "Building documentation..."
	cd docs && make html
	@echo "✅ Documentation built: docs/_build/html/index.html"

docs-serve:
	@echo "Serving documentation..."
	cd docs/_build/html && python -m http.server 8000

## Build
build:
	@echo "Building distribution packages..."
	uv build
	@echo "✅ Build complete: dist/"

## Cleanup
clean:
	@echo "Cleaning up..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf docs/_build/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name ".coverage*" -delete
	@echo "✅ Cleanup complete"

## Quick development workflow
dev: format lint test
	@echo "✅ Development check passed"

## Run pre-commit hooks
pre-commit:
	@echo "Running pre-commit hooks..."
	pre-commit run --all-files
	@echo "✅ Pre-commit hooks passed"

## Version
version:
	@python -c "import nifcloud; print(f'NIFCLOUD SDK version: {nifcloud.__version__}')"
