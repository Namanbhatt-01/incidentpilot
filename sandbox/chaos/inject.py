"""Chaos injector CLI for the IncidentPilot Sandbox.

Usage:
    python -m sandbox.chaos.inject <scenario>     Inject a failure mode
    python -m sandbox.chaos.inject reset          Reset to clean healthy state
    python -m sandbox.chaos.inject scenarios      List all 5 available scenarios
    python -m sandbox.chaos.inject status         Check current failure state
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path

STATE_FILE = Path(__file__).parent / ".chaos_state.json"


@dataclass
class Scenario:
    id: str
    target_service: str
    failure_mode: str
    description: str
    expected_fix: str
    runbook_id: str


SCENARIOS: dict[str, Scenario] = {
    "bad-deploy": Scenario(
        id="bad-deploy",
        target_service="orders-api",
        failure_mode="http500",
        description="Recreates orders-api with FAIL_MODE=http500; 500 spike on POST /orders",
        expected_fix="apply_patch",
        runbook_id="RB-001-orders-api-500.md",
    ),
    "cache-down": Scenario(
        id="cache-down",
        target_service="redis",
        failure_mode="stopped",
        description="Stops Redis container; cache hit ratio collapses and DB connections starve",
        expected_fix="restart_container",
        runbook_id="RB-003-redis-cache-down.md",
    ),
    "kill-worker": Scenario(
        id="kill-worker",
        target_service="orders-worker",
        failure_mode="sigkill",
        description="Sends SIGKILL to consumer worker; Kafka consumer lag climbs monotonically",
        expected_fix="restart_container",
        runbook_id="RB-004-kafka-lag.md",
    ),
    "oom-worker": Scenario(
        id="oom-worker",
        target_service="orders-worker",
        failure_mode="memory_leak",
        description="Simulates unbounded buffer leak; worker repeatedly triggers container OOMKilled",
        expected_fix="rollback_deploy",
        runbook_id="RB-005-memory-oom.md",
    ),
    "poison-message": Scenario(
        id="poison-message",
        target_service="orders-worker",
        failure_mode="poison_pill",
        description="Injects malformed event into orders topic; consumer crashloops on partition offset",
        expected_fix="skip_offset",
        runbook_id="RB-006-poison-pill.md",
    ),
}


def get_state() -> dict[str, str]:
    if STATE_FILE.exists():
        try:
            data = json.loads(STATE_FILE.read_text())
            if isinstance(data, dict):
                return {str(k): str(v) for k, v in data.items()}
            return {"active_scenario": "none"}
        except Exception:
            return {"active_scenario": "none"}
    return {"active_scenario": "none"}


def set_state(scenario_id: str) -> None:
    STATE_FILE.write_text(json.dumps({"active_scenario": scenario_id}, indent=2))
    # Also set in environment for in-process testing
    os.environ["FAIL_MODE"] = (
        SCENARIOS[scenario_id].failure_mode if scenario_id in SCENARIOS else "none"
    )


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python -m sandbox.chaos.inject [scenario|reset|scenarios|status]")
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd == "scenarios":
        print("Available IncidentPilot Chaos Scenarios:")
        for s in SCENARIOS.values():
            print(f"  - {s.id:16} | Target: {s.target_service:14} | Fix: {s.expected_fix}")
            print(f"    Desc: {s.description}\n")
    elif cmd == "status":
        state = get_state()
        print(f"Current Sandbox Chaos State: {state.get('active_scenario', 'none')}")
    elif cmd == "reset":
        set_state("none")
        print("Sandbox reset to healthy baseline (FAIL_MODE=none).")
    elif cmd in SCENARIOS:
        set_state(cmd)
        sc = SCENARIOS[cmd]
        print(f"Injected chaos scenario: {sc.id}")
        print(f"  Target: {sc.target_service}")
        print(f"  Mode:   {sc.failure_mode}")
        print(f"  Desc:   {sc.description}")
    else:
        print(f"Unknown scenario '{cmd}'. Run 'python -m sandbox.chaos.inject scenarios' for list.")
        sys.exit(1)


if __name__ == "__main__":
    main()
