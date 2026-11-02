from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import StrEnum

from packages.domain.events import DomainEvent, IncidentState
from packages.domain.fsm import IncidentStateMachine


class SeverityLevel(StrEnum):
    P1 = "P1"  # Critical revenue / outage
    P2 = "P2"  # Degraded performance / latency
    P3 = "P3"  # Minor / non-blocking


@dataclass
class RemediationPlan:
    plan_id: str
    incident_id: str
    action_type: str  # e.g., "rollback_deploy", "apply_patch", "restart_container"
    target_component: str
    patch_diff: str
    risk_summary: str
    rollback_action: str
    action_digest: str
    approved: bool = False
    approved_by: str | None = None
    created_at: float = field(default_factory=time.time)


@dataclass
class IncidentAggregate:
    """Root Aggregate managing the lifecycle of a production incident."""

    incident_id: str
    title: str
    reported_by: str
    created_at: float = field(default_factory=time.time)
    severity: SeverityLevel = SeverityLevel.P1
    fsm: IncidentStateMachine = field(default_factory=IncidentStateMachine)
    detected_evidence: list[str] = field(default_factory=list)
    root_cause_hypothesis: str | None = None
    runbook_citation: str | None = None
    remediation_plan: RemediationPlan | None = None
    events: list[DomainEvent] = field(default_factory=list)

    @property
    def state(self) -> IncidentState:
        return self.fsm.current_state

    def record_event(self, event: DomainEvent) -> None:
        self.events.append(event)
