.PHONY: help install run test lint format build release clean

PYTHON ?= python
VENV := .venv

# Platform detection: use Scripts\ on Windows, bin/ elsewhere
ifeq ($(OS),Windows_NT)
    BIN := $(VENV)/Scripts
else
    BIN := $(VENV)/bin
endif

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

build: ## Build app with PyInstaller (detects macOS .app or Windows .exe)
ifeq ($(OS),Windows_NT)
	powershell -ExecutionPolicy Bypass -File scripts/build.ps1
else
	bash scripts/build.sh
endif

release: ## Trigger GitHub release workflow
	gh workflow run release.yml --repo Jasrags/scout-advancement
	@echo "Release triggered. Watch with: gh run watch"

clean: ## Remove build artifacts and caches
ifeq ($(OS),Windows_NT)
	powershell -Command "Remove-Item -Recurse -Force -ErrorAction SilentlyContinue build, dist, *.egg-info, .pytest_cache, .mypy_cache, .ruff_cache, .coverage; Get-ChildItem -Recurse -Directory -Filter __pycache__ | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue"
else
	rm -rf build/ dist/ *.egg-info
	rm -rf .pytest_cache .mypy_cache .ruff_cache .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
endif
