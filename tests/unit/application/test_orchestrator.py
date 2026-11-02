from __future__ import annotations

from packages.application.orchestrator import IncidentLifecycleManager
from packages.domain.events import IncidentState


def test_full_orchestration_lifecycle() -> None:
    manager = IncidentLifecycleManager(mode="replay")

    # 1. Process Alert
    log_sample = [
        "2026-11-02 10:00:00 [ERROR] orders-api: FAIL_MODE=http500 detected on POST /orders",
        "TypeError: 'NoneType' object is not subscriptable at app.py:74",
    ]
    result1 = manager.process_alert(
        raw_report="Checkout is failing with HTTP 500 errors!",
        reported_by="@sam",
        log_lines=log_sample,
    )
    assert result1.incident.state == IncidentState.AWAITING_APPROVAL
    assert result1.approval_request is not None
    assert result1.approval_request.approved is False
    assert result1.resolved is False

    # 2. Grant Human Approval & Remediate
    result2 = manager.execute_approved_remediation(
        incident=result1.incident,
        approval_id=result1.approval_request.approval_id,
        approved_by="@priya",
        simulated_test_pass=True,
    )
    assert result2.resolved is True
    assert result2.incident.state == IncidentState.RESOLVED
    assert result2.mttr_seconds > 0.0
    assert "Root Cause Analysis (RCA)" in result2.postmortem_markdown
