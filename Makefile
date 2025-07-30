.PHONY: install test lint format clean run help

# Default target
help:
	@echo "Available targets:"
	@echo "  install     - Install dependencies"
	@echo "  test        - Run tests (when implemented)"
	@echo "  lint        - Run linting"
	@echo "  format      - Format code"
	@echo "  clean       - Clean up generated files"
	@echo "  run         - Run the application"

install:
	uv pip install -e ".[dev]"

test:
	@echo "Tests will be implemented. For now, testing basic functionality..."
	python cli.py test

lint:
	@echo "Linting (requires venv activation)..."
	@echo "Run: source .venv/bin/activate && make lint-real"

lint-real:
	flake8 src --max-line-length=88
	mypy src

format:
	@echo "Formatting (requires venv activation)..."
	@echo "Run: source .venv/bin/activate && make format-real"

format-real:
	black src
	isort src

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf dist
	rm -rf *.egg-info

run:
	@echo "Run the application:"
	@echo "  source .venv/bin/activate"
	@echo "  python -m src.email_parser.main"
