from __future__ import annotations

import re
import uuid

from packages.domain.entities import IncidentAggregate, SeverityLevel
from packages.domain.events import IncidentDetectedEvent, IncidentState, SeverityAssignedEvent


class TriageCommandHandler:
    """Classifies raw incident reports into structured incident aggregates with severity."""

    _P1_PATTERNS = [
        re.compile(r"50\d", re.IGNORECASE),
        re.compile(r"outage", re.IGNORECASE),
        re.compile(r"(checkout|payment|order).*(fail|error|crash|broken|down)", re.IGNORECASE),
        re.compile(r"(fail|error|crash|broken|down).*(checkout|payment|order)", re.IGNORECASE),
    ]

    _P2_PATTERNS = [
        re.compile(r"latency", re.IGNORECASE),
        re.compile(r"slow", re.IGNORECASE),
        re.compile(r"timeout", re.IGNORECASE),
        re.compile(r"degraded", re.IGNORECASE),
        re.compile(r"lag", re.IGNORECASE),
    ]

    def handle(self, raw_report: str, reported_by: str) -> IncidentAggregate:
        incident_id = f"inc-{uuid.uuid4().hex[:6]}"
        detected_event = IncidentDetectedEvent(
            event_id=f"evt-{uuid.uuid4().hex[:6]}",
            incident_id=incident_id,
            raw_report=raw_report,
            reported_by=reported_by,
        )

        # Severity Classification Logic
        severity = SeverityLevel.P3
        reason = "Minor / non-critical report"

        if any(p.search(raw_report) for p in self._P1_PATTERNS):
            severity = SeverityLevel.P1
            reason = "Direct impact on checkout/order fulfillment or server 500 error"
        elif any(p.search(raw_report) for p in self._P2_PATTERNS):
            severity = SeverityLevel.P2
            reason = "Degraded performance or high latency"

        incident = IncidentAggregate(
            incident_id=incident_id,
            title=f"Incident {incident_id.upper()}: {raw_report[:50]}...",
            reported_by=reported_by,
            severity=severity,
        )
        incident.record_event(detected_event)

        # Transition to TRIAGED
        incident.fsm.transition_to(IncidentState.TRIAGED)
        incident.record_event(
            SeverityAssignedEvent(
                event_id=f"evt-{uuid.uuid4().hex[:6]}",
                incident_id=incident_id,
                severity=severity.value,
                reasoning=reason,
            )
        )
        return incident
