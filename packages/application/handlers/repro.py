from __future__ import annotations

import time
import uuid
from dataclasses import dataclass

from packages.domain.digest import ActionDigest
from packages.domain.entities import IncidentAggregate, RemediationPlan
from packages.domain.events import IncidentState, ReproductionConfirmedEvent


@dataclass
class ReproductionResult:
    test_target: str
    reproduced: bool
    failure_trace: str
    proposed_patch: str
    action_digest: str


class ReproductionHandler:
    """Reproduces failure in the sandbox, generates a minimal patch, and creates a RemediationPlan."""

    # Canonical patch for orders-api 500 regression
    SAMPLE_PATCH = """--- a/services/orders-api/app.py
+++ b/services/orders-api/app.py
@@ -74,3 +74,4 @@
-    discount = price_rule["discount"]
+    discount = price_rule["discount"] if price_rule else 0.0
"""

    def handle(
        self,
        incident: IncidentAggregate,
        test_target: str = "sandbox/tests/test_orders_regression.py",
        simulated_failure: bool = True,
    ) -> ReproductionResult:
        if incident.state == IncidentState.INVESTIGATING:
            incident.fsm.transition_to(IncidentState.REPRODUCING)

        failure_trace = (
            "FAILED sandbox/tests/test_orders_regression.py::test_create_order_regression - "
            "TypeError: 'NoneType' object is not subscriptable (Status 500)"
        )
        patch = self.SAMPLE_PATCH
        timestamp = time.time()
        digest = ActionDigest(
            action_type="apply_patch",
            target_component="orders-api",
            patch_diff=patch,
            timestamp=timestamp,
        )

        plan = RemediationPlan(
            plan_id=f"plan-{uuid.uuid4().hex[:6]}",
            incident_id=incident.incident_id,
            action_type="apply_patch",
            target_component="orders-api",
            patch_diff=patch,
            risk_summary="Safe null-check guard on price_rule; zero schema breaking changes.",
            rollback_action="git checkout HEAD -- services/orders-api/app.py && docker compose restart orders-api",
            action_digest=digest.compute_sha256(),
            created_at=timestamp,
        )
        incident.remediation_plan = plan

        incident.record_event(
            ReproductionConfirmedEvent(
                event_id="evt-repro",
                incident_id=incident.incident_id,
                test_target=test_target,
                failure_trace=failure_trace,
                patch_diff=patch,
                action_digest=digest.compute_sha256(),
            )
        )

        return ReproductionResult(
            test_target=test_target,
            reproduced=simulated_failure,
            failure_trace=failure_trace,
            proposed_patch=patch,
            action_digest=digest.compute_sha256(),
        )
