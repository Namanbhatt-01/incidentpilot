from __future__ import annotations

import time
from dataclasses import dataclass
from enum import StrEnum


class IncidentState(StrEnum):
    DETECTED = "DETECTED"
    TRIAGED = "TRIAGED"
    INVESTIGATING = "INVESTIGATING"
    REPRODUCING = "REPRODUCING"
    CRITIC_REVIEW = "CRITIC_REVIEW"
    AWAITING_APPROVAL = "AWAITING_APPROVAL"
    REMEDIATING = "REMEDIATING"
    VERIFYING = "VERIFYING"
    RESOLVED = "RESOLVED"
    ABORTED = "ABORTED"


@dataclass(frozen=True)
class DomainEvent:
    event_id: str
    incident_id: str
    timestamp: float = time.time()


@dataclass(frozen=True)
class IncidentDetectedEvent(DomainEvent):
    raw_report: str = ""
    reported_by: str = ""
    trace_id: str = ""


@dataclass(frozen=True)
class SeverityAssignedEvent(DomainEvent):
    severity: str = "P1"
    reasoning: str = ""


@dataclass(frozen=True)
class DiagnosisHypothesizedEvent(DomainEvent):
    root_cause: str = ""
    evidence_lines: tuple[str, ...] = ()
    runbook_id: str = ""


@dataclass(frozen=True)
class ReproductionConfirmedEvent(DomainEvent):
    test_target: str = ""
    failure_trace: str = ""
    patch_diff: str = ""
    action_digest: str = ""


@dataclass(frozen=True)
class CriticVerdictEvent(DomainEvent):
    approved: bool = False
    verdict_summary: str = ""
    objections: tuple[str, ...] = ()


@dataclass(frozen=True)
class HumanApprovalRequestedEvent(DomainEvent):
    approval_id: str = ""
    action_digest: str = ""
    risk_summary: str = ""


@dataclass(frozen=True)
class HumanApprovalGrantedEvent(DomainEvent):
    approval_id: str = ""
    approved_by: str = ""
    action_digest: str = ""


@dataclass(frozen=True)
class RemediationVerifiedEvent(DomainEvent):
    tests_passed: int = 0
    tests_failed: int = 0
    healthy: bool = False


@dataclass(frozen=True)
class IncidentResolvedEvent(DomainEvent):
    resolved_at: float = 0.0
    mttr_seconds: float = 0.0
    postmortem_doc_id: str = ""
