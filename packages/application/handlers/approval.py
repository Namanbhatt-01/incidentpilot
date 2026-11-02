from __future__ import annotations

import time
import uuid
from dataclasses import dataclass

from packages.domain.digest import ActionDigest


class TOCTOUValidationError(ValueError):
    """Raised when live code or parameters mutated between check and use."""

    pass


@dataclass
class PendingApproval:
    approval_id: str
    incident_id: str
    action_type: str
    target_component: str
    patch_diff: str
    risk_summary: str
    action_digest: str
    created_at: float
    approved: bool = False
    approved_by: str | None = None
    approved_at: float | None = None


class ApprovalGateHandler:
    """Manages cryptographic Four-Eyes human approvals with TOCTOU defense."""

    def __init__(self) -> None:
        self._pending: dict[str, PendingApproval] = {}

    def create_request(
        self,
        incident_id: str,
        action_type: str,
        target_component: str,
        patch_diff: str,
        timestamp: float,
        risk_summary: str,
    ) -> PendingApproval:
        digest = ActionDigest(
            action_type=action_type,
            target_component=target_component,
            patch_diff=patch_diff,
            timestamp=timestamp,
        )
        approval_id = f"appr-{uuid.uuid4().hex[:6]}"
        pending = PendingApproval(
            approval_id=approval_id,
            incident_id=incident_id,
            action_type=action_type,
            target_component=target_component,
            patch_diff=patch_diff,
            risk_summary=risk_summary,
            action_digest=digest.compute_sha256(),
            created_at=timestamp,
        )
        self._pending[approval_id] = pending
        return pending

    def approve(
        self,
        approval_id: str,
        approved_by: str,
        current_patch_diff: str,
        current_timestamp: float,
    ) -> bool:
        if approval_id not in self._pending:
            return False

        pending = self._pending[approval_id]

        # Re-compute digest over live state to detect TOCTOU tampering
        current_digest = ActionDigest(
            action_type=pending.action_type,
            target_component=pending.target_component,
            patch_diff=current_patch_diff,
            timestamp=current_timestamp,
        ).compute_sha256()

        if current_digest != pending.action_digest:
            raise TOCTOUValidationError(
                f"TOCTOU integrity violation: live patch hash {current_digest[:8]} does not match approved {pending.action_digest[:8]}"
            )

        pending.approved = True
        pending.approved_by = approved_by
        pending.approved_at = time.time()
        return True
