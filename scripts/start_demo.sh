#!/usr/bin/env bash
set -euo pipefail

PORT="${PORT:-8000}"
HOST="${HOST:-127.0.0.1}"
BASE_URL="http://${HOST}:${PORT}"

echo "================================================================================"
echo "    🚨 IncidentPilot: Live Production Target & Switch War Room"
echo "================================================================================"
echo " Starting Orders API & Interactive SRE War Room on ${BASE_URL}..."

# Ensure venv exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    .venv/bin/pip install --upgrade pip
    .venv/bin/pip install -e ".[dev]"
fi

# Reset any lingering chaos state
.venv/bin/python -m sandbox.chaos.inject reset 2>/dev/null || true

# Start uvicorn in background
.venv/bin/uvicorn sandbox.services.orders_api.app:app --host "${HOST}" --port "${PORT}" &
SERVER_PID=$!

cleanup() {
    echo ""
    echo "Stopping IncidentPilot Live Server (PID: ${SERVER_PID})..."
    kill "${SERVER_PID}" 2>/dev/null || true
    .venv/bin/python -m sandbox.chaos.inject reset 2>/dev/null || true
    echo "Shutdown complete."
}
trap cleanup EXIT INT TERM

# Wait for server to come online
echo "Waiting for service to become ready..."
for i in {1..30}; do
    if curl -s "${BASE_URL}/health" >/dev/null 2>&1; then
        break
    fi
    sleep 0.2
done

echo ""
echo "================================================================================"
echo "  🎉 INCIDENTPILOT LIVE ENVIRONMENT READY FOR DEMO & VIDEO RECORDING"
echo "================================================================================"
echo "  🖥️  Interactive War Room Dashboard : ${BASE_URL}/"
echo "  📊  Live Prometheus Metrics Exporter: ${BASE_URL}/metrics"
echo "  📖  FastAPI Swagger API Docs        : ${BASE_URL}/docs"
echo "  🩺  Service Health Probe            : ${BASE_URL}/health"
echo "  📦  Transactional Endpoint          : POST ${BASE_URL}/orders"
echo "================================================================================"
echo " Press Ctrl+C to stop the server at any time."
echo ""

# Auto-open browser on macOS
if command -v open >/dev/null 2>&1; then
    open "${BASE_URL}/"
elif command -v xdg-open >/dev/null 2>&1; then
    xdg-open "${BASE_URL}/"
fi

# Keep running
wait "${SERVER_PID}"
