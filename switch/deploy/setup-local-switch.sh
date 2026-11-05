#!/usr/bin/env bash
set -euo pipefail

echo "=========================================================="
echo " IncidentPilot - Local Switch Server & Mattermost Bootstrap"
echo "=========================================================="

export SWITCH_VERSION="latest"
export SWITCH_REGISTRY="ghcr.io"
export SWITCH_IMAGE_NAMESPACE="sandbox-quantum"

echo "Checking Docker daemon status..."
if ! docker info >/dev/null 2>&1; then
    echo "ERROR: Docker daemon is not running. Please start Docker."
    exit 1
fi

echo "Starting Switch local stack (PostgreSQL + Switch Core + Mattermost)..."
docker compose -f switch/deploy/docker-compose.switch.yml --profile collab up -d

echo ""
echo "Waiting for Switch Core to be healthy on http://localhost:8000/health..."
for i in {1..30}; do
    if curl -s http://localhost:8000/health >/dev/null 2>&1; then
        echo "Switch Core is ready!"
        break
    fi
    sleep 2
done

echo ""
echo "Switch Stack Status:"
echo "  - Switch Core API:  http://localhost:8000"
echo "  - Mattermost Chat:  http://localhost:8065"
echo ""
echo "Ready for IncidentPilot agents to connect."

