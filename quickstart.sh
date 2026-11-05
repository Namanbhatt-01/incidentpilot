#!/usr/bin/env bash
set -euo pipefail

echo "=========================================================="
echo "    🚀 IncidentPilot: 1-Click Judge & Evaluation Runner"
echo "=========================================================="

MODE="${1:---offline}"

if [ "$MODE" == "--live" ]; then
    echo "Mode: LIVE LLM (Calling Gemini / OpenAI)"
    export ENGINE_MODE="live"
else
    echo "Mode: DETERMINISTIC OFFLINE REPLAY (Zero API Key / Fast)"
    export ENGINE_MODE="replay"
fi

# 1. Setup Virtual Environment if missing
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    .venv/bin/pip install --upgrade pip
    .venv/bin/pip install -e ".[dev]"
fi

echo ""
echo "Step 1: Running Unit & Contract Test Suite..."
.venv/bin/pytest tests/unit sandbox/tests tests/integration -q

echo ""
echo "Step 2: Simulating Chaos Failure Mode (bad-deploy / HTTP 500)..."
.venv/bin/python -m sandbox.chaos.inject bad-deploy

echo ""
echo "Step 3: Running Automated 5-Scenario Evaluation Benchmark..."
.venv/bin/python -m evals.benchmark

echo ""
echo "Step 4: Resetting Chaos State..."
.venv/bin/python -m sandbox.chaos.inject reset

echo ""
echo "=========================================================="
echo " ✅ IncidentPilot Verification Complete!"
echo " Results saved to evals/scorecard.md"
echo "=========================================================="

