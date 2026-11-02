from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from packages.domain.events import (
    IncidentDetectedEvent,
    ReproductionConfirmedEvent,
)


def test_domain_events_frozen_immutability() -> None:
    event = IncidentDetectedEvent(
        event_id="evt-001",
        incident_id="inc-100",
        timestamp=1700000000.0,
        raw_report="Checkout 500 error",
        reported_by="@user1",
        trace_id="trace-abc",
    )
    with pytest.raises(FrozenInstanceError):
        event.raw_report = "tampered report"  # type: ignore[misc]


def test_reproduction_event_fields() -> None:
    event = ReproductionConfirmedEvent(
        event_id="evt-002",
        incident_id="inc-100",
        timestamp=1700000000.0,
        test_target="sandbox/tests/test_orders_regression.py",
        failure_trace="HTTP 500 Internal Server Error",
        patch_diff="diff --git",
        action_digest="sha:12345678",
    )
    assert event.action_digest == "sha:12345678"
    assert event.test_target == "sandbox/tests/test_orders_regression.py"
