.PHONY: help install run test lint format build release clean

PYTHON ?= python
VENV := .venv
BIN := $(VENV)/bin

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Create venv and install dependencies
	$(PYTHON) -m venv $(VENV)
	$(BIN)/pip install --upgrade pip
	$(BIN)/pip install -e ".[dev]"

run: ## Launch the GUI
	$(BIN)/python -m src.main

test: ## Run tests with coverage (80% gate on src/core)
	$(BIN)/python -m pytest --cov=src/core --cov-report=term-missing --cov-fail-under=80

lint: ## Run linter, format check, and type checker
	$(BIN)/ruff check src/ tests/
	$(BIN)/ruff format --check src/ tests/
	$(BIN)/mypy src/

format: ## Auto-format code with ruff
	$(BIN)/ruff format src/ tests/
	$(BIN)/ruff check --fix src/ tests/

build: ## Build macOS .app with PyInstaller
	bash scripts/build.sh

release: ## Trigger GitHub release workflow
	gh workflow run release.yml --repo Jasrags/scout-advancement
	@echo "Release triggered. Watch with: gh run watch"

clean: ## Remove build artifacts and caches
	rm -rf build/ dist/ *.egg-info
	rm -rf .pytest_cache .mypy_cache .ruff_cache .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
