from __future__ import annotations

import time

from packages.domain.entities import IncidentAggregate


class RoomDocumentSync:
    """Renders and synchronizes live incident state into Switch Room Documents."""

    def render_warboard_document(self, incident: IncidentAggregate) -> str:
        elapsed = time.time() - incident.created_at
        patch_info = (
            f"Action: `{incident.remediation_plan.action_type}`\n"
            f"- Digest: `{incident.remediation_plan.action_digest[:16]}...`\n"
            f"- Risk: {incident.remediation_plan.risk_summary}\n"
            if incident.remediation_plan
            else "None yet"
        )

        return f"""# INCIDENT WAR-BOARD: {incident.incident_id.upper()}
- **Current State**: `{incident.state.value}`
- **Severity**: `{incident.severity.value}`
- **Elapsed Time**: {elapsed:.1f}s
- **Reported By**: {incident.reported_by}

## Hypothesis & Evidence
- **Root Cause**: {incident.root_cause_hypothesis or "Under Investigation"}
- **Runbook**: {incident.runbook_citation or "None cited"}

## Remediation & Safety
{patch_info}

---
*Updated automatically by IncidentPilot over Switch Agent Protocol.*
"""
