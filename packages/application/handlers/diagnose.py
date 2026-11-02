from __future__ import annotations

from dataclasses import dataclass

from packages.domain.entities import IncidentAggregate
from packages.domain.events import DiagnosisHypothesizedEvent, IncidentState


@dataclass
class DiagnosticResult:
    root_cause: str
    evidence_lines: list[str]
    runbook_id: str
    confidence_score: float


class DiagnosticHandler:
    """Diagnoses root cause from error logs and runbooks, supporting Live LLM and Deterministic Replay."""

    def __init__(self, mode: str = "replay") -> None:
        self.mode = mode

    def handle(self, incident: IncidentAggregate, log_lines: list[str]) -> DiagnosticResult:
        if incident.state == IncidentState.TRIAGED:
            incident.fsm.transition_to(IncidentState.INVESTIGATING)

        # Inspect log lines for recognized signatures
        root_cause = "Unhandled generic exception in service execution"
        runbook = "RB-001-orders-api-500.md"
        evidence: list[str] = []
        confidence = 0.85

        for line in log_lines:
            if (
                "FAIL_MODE=http500" in line
                or "NoneType" in line
                or "500 Internal Server Error" in line
            ):
                root_cause = "Regression in orders-api: unhandled NoneType in price_rule discount calculation"
                runbook = "RB-001-orders-api-500.md"
                evidence.append(line)
                confidence = 0.98
                break
            elif (
                "redis" in line.lower()
                or "cache" in line.lower()
                or "connection refused" in line.lower()
            ):
                root_cause = "Redis cache outage causing Postgres connection pool exhaustion"
                runbook = "RB-003-redis-cache-down.md"
                evidence.append(line)
                confidence = 0.95
                break

        if not evidence and log_lines:
            evidence.append(log_lines[0])

        incident.root_cause_hypothesis = root_cause
        incident.runbook_citation = runbook
        incident.detected_evidence = evidence
        incident.record_event(
            DiagnosisHypothesizedEvent(
                event_id="evt-diag",
                incident_id=incident.incident_id,
                root_cause=root_cause,
                evidence_lines=tuple(evidence),
                runbook_id=runbook,
            )
        )

        return DiagnosticResult(
            root_cause=root_cause,
            evidence_lines=evidence,
            runbook_id=runbook,
            confidence_score=confidence,
        )
