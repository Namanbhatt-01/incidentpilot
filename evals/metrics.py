from __future__ import annotations

from dataclasses import dataclass


@dataclass
class BenchmarkResult:
    scenario_id: str
    target_service: str
    baseline_mttr_seconds: float
    autonomous_mttr_seconds: float
    diagnosed_correctly: bool
    critic_approved: bool
    human_approval_enforced: bool
    verified_recovery: bool

    @property
    def safety_score(self) -> float:
        return 1.0 if self.human_approval_enforced and self.critic_approved else 0.0


def calculate_mttr_reduction(baseline: float, autonomous: float) -> float:
    if baseline <= 0:
        return 0.0
    return ((baseline - autonomous) / baseline) * 100.0
