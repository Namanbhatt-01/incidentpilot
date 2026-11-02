from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from packages.application.orchestrator import IncidentLifecycleManager
from packages.domain.events import IncidentState
from sandbox.services.orders_api.app import app

client = TestClient(app)


def test_incident_e2e_reproduce_patch_and_verify(monkeypatch: pytest.MonkeyPatch) -> None:
    # 1. Simulate failure mode active in sandbox
    monkeypatch.setenv("FAIL_MODE", "http500")
    bad_res = client.post(
        "/orders", json={"item_id": "item-999", "quantity": 1, "customer_id": "cust-1"}
    )
    assert bad_res.status_code == 500

    # 2. Trigger IncidentPilot Orchestration
    manager = IncidentLifecycleManager(mode="replay")
    alert_result = manager.process_alert(
        raw_report="Production incident: orders-api returning 500 on checkout",
        reported_by="@monitor",
        log_lines=[
            "2026-11-02 [CRITICAL] orders-api: FAIL_MODE=http500 detected",
            "TypeError: 'NoneType' object is not subscriptable",
        ],
    )
    assert alert_result.incident.state == IncidentState.AWAITING_APPROVAL
    assert alert_result.approval_request is not None

    # 3. Simulate Human Sign-Off & Fix Application
    monkeypatch.setenv("FAIL_MODE", "none")  # Simulate applied patch/rollback
    resolve_result = manager.execute_approved_remediation(
        incident=alert_result.incident,
        approval_id=alert_result.approval_request.approval_id,
        approved_by="@priya",
        simulated_test_pass=True,
    )
    assert resolve_result.resolved is True
    assert resolve_result.incident.state == IncidentState.RESOLVED

    # 4. Verify Sandbox is now healthy
    healthy_res = client.post(
        "/orders", json={"item_id": "item-999", "quantity": 1, "customer_id": "cust-1"}
    )
    assert healthy_res.status_code == 200
    assert healthy_res.json()["status"] == "CONFIRMED"
