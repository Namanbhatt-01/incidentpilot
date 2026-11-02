from __future__ import annotations

import pytest

from packages.application.handlers.approval import (
    ApprovalGateHandler,
    PendingApproval,
    TOCTOUValidationError,
)
from packages.domain.digest import ActionDigest


def test_approval_gate_request_and_grant() -> None:
    gate = ApprovalGateHandler()
    digest = ActionDigest(
        action_type="apply_patch",
        target_component="orders-api",
        patch_diff="fix code diff",
        timestamp=1700000000.0,
    )
    req: PendingApproval = gate.create_request(
        incident_id="inc-101",
        action_type="apply_patch",
        target_component="orders-api",
        patch_diff="fix code diff",
        timestamp=1700000000.0,
        risk_summary="Low risk safe null-check",
    )
    assert req.approval_id.startswith("appr-")
    assert req.action_digest == digest.compute_sha256()
    assert req.approved is False

    # Sign off
    success = gate.approve(
        approval_id=req.approval_id,
        approved_by="@priya",
        current_patch_diff="fix code diff",
        current_timestamp=1700000000.0,
    )
    assert success is True
    assert req.approved is True
    assert req.approved_by == "@priya"


def test_approval_gate_toctou_violation_raises() -> None:
    gate = ApprovalGateHandler()
    req = gate.create_request(
        incident_id="inc-102",
        action_type="apply_patch",
        target_component="orders-api",
        patch_diff="original diff",
        timestamp=1700000000.0,
        risk_summary="Safe patch",
    )
    # Attempt approval with tampered diff
    with pytest.raises(TOCTOUValidationError) as exc_info:
        gate.approve(
            approval_id=req.approval_id,
            approved_by="@priya",
            current_patch_diff="malicious altered diff",
            current_timestamp=1700000000.0,
        )
    assert "TOCTOU integrity violation" in str(exc_info.value)
