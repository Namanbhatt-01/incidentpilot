.PHONY: help setup test test-unit test-integration lint format typecheck clean

VENV := .venv
PYTHON := $(VENV)/bin/python
PYTEST := $(VENV)/bin/pytest
RUFF := $(VENV)/bin/ruff
MYPY := $(VENV)/bin/mypy

help:
	@echo "IncidentPilot Developer & Judge Targets:"
	@echo "  make demo           - Launch live target service & browser War Room on port 8000"
	@echo "  make sim            - Run interactive terminal War Room simulation for video"
	@echo "  make sim-auto       - Run automated terminal simulation (no prompt)"
	@echo "  make setup          - Initialize virtual environment & install dependencies"
	@echo "  make test           - Run all unit and integration tests"
	@echo "  make test-unit      - Run unit tests only"
	@echo "  make lint           - Run Ruff linter"
	@echo "  make format         - Run Ruff code formatter"
	@echo "  make typecheck      - Run Mypy strict type checking"
	@echo "  make clean          - Remove temporary and build files"

demo:
	./scripts/start_demo.sh

sim:
	$(PYTHON) scripts/demo_simulation.py

sim-auto:
	$(PYTHON) scripts/demo_simulation.py --auto-approve

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

