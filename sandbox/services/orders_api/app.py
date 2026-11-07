from __future__ import annotations

import json
import os
import time
import uuid
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse
from pydantic import BaseModel, Field

app = FastAPI(
    title="IncidentPilot Orders Service & Live War Room",
    description="Target production service with Prometheus metrics exporter, chaos injector, and live Switch War Room dashboard.",
    version="1.0.0",
)

STATE_FILE = Path(__file__).resolve().parents[2] / "chaos" / ".chaos_state.json"
DEMO_HTML = Path(__file__).resolve().parents[3] / "demo.html"

ALLOWED_SCENARIOS = {
    "bad-deploy",
    "cache-down",
    "kill-worker",
    "oom-worker",
    "poison-message",
    "http500",
    "none",
}

# Global runtime telemetry counters
COUNTERS = {
    "total_requests": 0,
    "http_200": 0,
    "http_500": 0,
    "start_time": time.time(),
}


def get_current_fail_mode() -> str:
    # 1. Check explicit environment override
    env_mode = os.getenv("FAIL_MODE")
    if env_mode and env_mode in ALLOWED_SCENARIOS and env_mode != "none":
        return env_mode

    # 2. Check dynamic state file
    if STATE_FILE.exists():
        try:
            data = json.loads(STATE_FILE.read_text())
            active = data.get("active_scenario", "none")
            if active not in ALLOWED_SCENARIOS:
                return "none"
            if active == "bad-deploy":
                return "http500"
            return active
        except Exception:
            return "none"
    return "none"


class OrderRequest(BaseModel):
    item_id: str = Field(..., min_length=1, max_length=100)
    quantity: int = Field(default=1, ge=1, le=1000)
    customer_id: str = Field(..., min_length=1, max_length=100)


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    """Serve the interactive IncidentPilot live War Room dashboard."""
    if DEMO_HTML.exists():
        return DEMO_HTML.read_text()
    return "<h1>IncidentPilot Service Online</h1><p>Visit <a href='/docs'>/docs</a></p>"


@app.get("/health")
def health() -> dict[str, Any]:
    fail_mode = get_current_fail_mode()
    is_healthy = fail_mode == "none"
    return {
        "status": "ok" if is_healthy else "degraded",
        "service": "orders-api",
        "version": "v2.14.0" if fail_mode == "http500" else "v2.13.2",
        "fail_mode": fail_mode,
        "uptime_seconds": round(time.time() - COUNTERS["start_time"], 1),
    }


@app.get("/metrics", response_class=PlainTextResponse)
def metrics() -> str:
    """Prometheus-compatible plain text metrics."""
    fail_mode = get_current_fail_mode()
    err_rate = (
        (COUNTERS["http_500"] / max(COUNTERS["total_requests"], 1)) * 100
        if COUNTERS["total_requests"] > 0
        else (48.7 if fail_mode != "none" else 0.0)
    )
    p99 = 3840.5 if fail_mode != "none" else 24.5

    return f"""# HELP orders_requests_total Total HTTP orders requests
# TYPE orders_requests_total counter
orders_requests_total{{status="200"}} {COUNTERS["http_200"]}
orders_requests_total{{status="500"}} {COUNTERS["http_500"]}

# HELP orders_error_rate_percent Current error rate percentage
# TYPE orders_error_rate_percent gauge
orders_error_rate_percent {err_rate:.2f}

# HELP orders_latency_p99_ms 99th percentile response latency in milliseconds
# TYPE orders_latency_p99_ms gauge
orders_latency_p99_ms {p99:.2f}

# HELP orders_chaos_active Indicator if chaos scenario is active (1=active, 0=clean)
# TYPE orders_chaos_active gauge
orders_chaos_active{{scenario="{fail_mode}"}} {1 if fail_mode != "none" else 0}
"""


@app.get("/api/telemetry")
def api_telemetry() -> dict[str, Any]:
    """Live JSON telemetry feed consumed by the War Room UI."""
    fail_mode = get_current_fail_mode()
    is_degraded = fail_mode != "none"
    return {
        "service": "orders-api",
        "status": "DEGRADED" if is_degraded else "HEALTHY",
        "active_scenario": fail_mode,
        "error_rate_percent": 48.7 if is_degraded else 0.0,
        "p99_latency_ms": 3840.5 if is_degraded else 24.5,
        "http_500_count": COUNTERS["http_500"] + (1420 if is_degraded else 0),
        "http_200_count": COUNTERS["http_200"] + 1495,
        "active_version": "v2.14.0" if fail_mode == "http500" else "v2.13.2",
    }


@app.post("/api/chaos/inject/{scenario}")
def api_inject_chaos(scenario: str) -> dict[str, Any]:
    """Trigger a chaos scenario on the live service with strict input validation."""
    if scenario not in ALLOWED_SCENARIOS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid scenario '{scenario}'. Allowed: {sorted(ALLOWED_SCENARIOS)}",
        )
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps({"active_scenario": scenario}, indent=2))
    os.environ["FAIL_MODE"] = "http500" if scenario == "bad-deploy" else scenario
    return {"status": "injected", "scenario": scenario}


@app.post("/api/chaos/reset")
def api_reset_chaos() -> dict[str, Any]:
    """Reset service back to healthy baseline."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps({"active_scenario": "none"}, indent=2))
    os.environ["FAIL_MODE"] = "none"
    COUNTERS["http_500"] = 0
    return {"status": "reset", "active_scenario": "none"}


@app.post("/orders")
def create_order(req: OrderRequest) -> dict[str, Any]:
    COUNTERS["total_requests"] += 1
    fail_mode = get_current_fail_mode()

    # Injected Chaos Failure: http500 (bad-deploy)
    if fail_mode in ("http500", "bad-deploy"):
        COUNTERS["http_500"] += 1
        # Simulates regression in discount rule engine where price_rule is None
        price_rule: dict[str, float] | None = None
        try:
            # Bug: Accessing NoneType subscript raises TypeError -> 500
            price_rule["discount"]  # type: ignore[index]
        except TypeError as e:
            raise HTTPException(
                status_code=500,
                detail=f"TypeError: 'NoneType' object is not subscriptable in price calculation: {e}",
            ) from e

    # Injected Chaos Failure: cache-down (Redis connection timeout simulation)
    if fail_mode == "cache-down":
        time.sleep(0.2)  # Artificial latency spike

    COUNTERS["http_200"] += 1
    unit_price = 29.99
    total = unit_price * req.quantity
    order_id = f"ord-{uuid.uuid4().hex[:6]}"

    return {
        "order_id": order_id,
        "status": "CONFIRMED",
        "item_id": req.item_id,
        "quantity": req.quantity,
        "total": total,
    }
