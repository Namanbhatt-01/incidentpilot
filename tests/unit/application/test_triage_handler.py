from __future__ import annotations

from packages.application.handlers.triage import TriageCommandHandler
from packages.domain.entities import SeverityLevel
from packages.domain.events import IncidentState


def test_triage_handler_checkout_500_classified_as_p1() -> None:
    handler = TriageCommandHandler()
    incident = handler.handle(
        raw_report="Checkout service failing with HTTP 500 on POST /orders",
        reported_by="@sam",
    )
    assert incident.severity == SeverityLevel.P1
    assert incident.state == IncidentState.TRIAGED
    assert "checkout" in incident.title.lower() or "orders" in incident.title.lower()


def test_triage_handler_latency_classified_as_p2() -> None:
    handler = TriageCommandHandler()
    incident = handler.handle(
        raw_report="API latency elevated to 1.5s on product catalog",
        reported_by="@alex",
    )
    assert incident.severity == SeverityLevel.P2
    assert incident.state == IncidentState.TRIAGED


def test_triage_handler_minor_classified_as_p3() -> None:
    handler = TriageCommandHandler()
    incident = handler.handle(
        raw_report="Typo in checkout confirmation email template",
        reported_by="@priya",
    )
    assert incident.severity == SeverityLevel.P3
    assert incident.state == IncidentState.TRIAGED
