.PHONY: help install install-dev test lint format clean build docs serve-docs

PYTHON := python3
PIP := pip3
PACKAGE_NAME := lexlang

help:
	@echo "Available commands:"
	@echo "  install     - Install the package"
	@echo "  install-dev - Install development dependencies"
	@echo "  test        - Run tests"
	@echo "  lint        - Run linting"
	@echo "  format      - Format code"
	@echo "  clean       - Clean build artifacts"
	@echo "  build       - Build package"
	@echo "  docs        - Build documentation"
	@echo "  serve-docs  - Serve documentation locally"

install:
	$(PIP) install -e .

install-dev:
	$(PIP) install -e ".[dev]"
	$(PIP) install pre-commit
	pre-commit install

test:
	pytest tests/ -v --cov=$(PACKAGE_NAME) --cov-report=html --cov-report=term

lint:
	flake8 src/ tests/
	mypy src/
	black --check src/ tests/

format:
	black src/ tests/
	isort src/ tests/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build: clean
	$(PYTHON) -m build

docs:
	sphinx-build -b html docs/ docs/_build/

serve-docs:
	$(PYTHON) -m http.server 8000 --directory docs/_build/

docker-build:
	docker build -t $(PACKAGE_NAME):latest .

docker-run:
	docker run -p 8000:8000 $(PACKAGE_NAME):latest
