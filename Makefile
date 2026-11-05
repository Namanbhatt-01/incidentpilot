.PHONY: help setup test test-unit test-integration lint format typecheck clean

VENV := .venv
PYTHON := $(VENV)/bin/python
PYTEST := $(VENV)/bin/pytest
RUFF := $(VENV)/bin/ruff
MYPY := $(VENV)/bin/mypy

help:
	@echo "IncidentPilot Developer Targets:"
	@echo "  make setup          - Initialize virtual environment & install dependencies"
	@echo "  make test           - Run all unit and integration tests"
	@echo "  make test-unit      - Run unit tests only"
	@echo "  make lint           - Run Ruff linter"
	@echo "  make format         - Run Ruff code formatter"
	@echo "  make typecheck      - Run Mypy strict type checking"
	@echo "  make chaos-500      - Inject HTTP 500 regression in sandbox"
	@echo "  make clean          - Remove temporary and build files"

setup:
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -e ".[dev]"

test:
	$(PYTEST) tests/unit tests/integration -v

test-unit:
	$(PYTEST) tests/unit -v

lint:
	$(RUFF) check packages tests sandbox evals

format:
	$(RUFF) format packages tests sandbox evals

typecheck:
	$(MYPY) packages

clean:
	rm -rf __pycache__ .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage

