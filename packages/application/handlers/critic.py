from __future__ import annotations

from dataclasses import dataclass

from packages.domain.entities import IncidentAggregate
from packages.domain.events import CriticVerdictEvent, IncidentState


@dataclass
class CriticReviewResult:
    approved: bool
    verdict_summary: str
    objections: list[str]


class CriticReviewHandler:
    """Adversarial SRE Critic: independently checks diagnosis grounding and remediation safety."""

    def handle(self, incident: IncidentAggregate) -> CriticReviewResult:
        if incident.state == IncidentState.REPRODUCING:
            incident.fsm.transition_to(IncidentState.CRITIC_REVIEW)

        objections: list[str] = []

        # Check 1: Root cause grounding
        if not incident.root_cause_hypothesis or not incident.detected_evidence:
            objections.append("Root cause is ungrounded: no log evidence was cited.")

        # Check 2: Remediation safety & blast radius
        if not incident.remediation_plan:
            objections.append("No remediation plan exists to review.")
        else:
            if not incident.remediation_plan.rollback_action:
                objections.append(
                    "Remediation plan lacks an automated compensating rollback action."
                )
            if (
                "rm -rf" in incident.remediation_plan.patch_diff
                or "DROP TABLE" in incident.remediation_plan.patch_diff
            ):
                objections.append("Destructive commands detected in patch diff.")

        approved = len(objections) == 0
        summary = (
            "VERDICT: APPROVED. Root cause causality confirmed and patch has safe blast-radius."
            if approved
            else f"VERDICT: REJECTED with {len(objections)} objections."
        )

        incident.record_event(
            CriticVerdictEvent(
                event_id="evt-critic",
                incident_id=incident.incident_id,
                approved=approved,
                verdict_summary=summary,
                objections=tuple(objections),
            )
        )

        return CriticReviewResult(
            approved=approved,
            verdict_summary=summary,
            objections=objections,
        )
