from __future__ import annotations

from evals.metrics import BenchmarkResult, calculate_mttr_reduction


def test_benchmark_metrics_calculation() -> None:
    res = BenchmarkResult(
        scenario_id="bad-deploy",
        target_service="orders-api",
        baseline_mttr_seconds=1800.0,  # 30 mins human SRE manual
        autonomous_mttr_seconds=18.5,
        diagnosed_correctly=True,
        critic_approved=True,
        human_approval_enforced=True,
        verified_recovery=True,
    )
    reduction = calculate_mttr_reduction(res.baseline_mttr_seconds, res.autonomous_mttr_seconds)
    assert reduction > 90.0  # >90% MTTR reduction
    assert res.safety_score == 1.0  # 100% safety
