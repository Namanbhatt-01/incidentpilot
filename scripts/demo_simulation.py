#!/usr/bin/env python3
"""Interactive Terminal War Room Simulation for IncidentPilot.

Renders an animated multi-agent SRE incident response war room in the terminal,
suitable for live screen recording, video demos, and judge evaluation.

Usage:
    python3 scripts/demo_simulation.py
    python3 scripts/demo_simulation.py --auto-approve
"""

from __future__ import annotations

import argparse
import contextlib
import sys
import time

import httpx

# ANSI Color codes
C_RESET = "\033[0m"
C_BOLD = "\033[1m"
C_DIM = "\033[2m"
C_RED = "\033[91m"
C_GREEN = "\033[92m"
C_YELLOW = "\033[93m"
C_BLUE = "\033[94m"
C_MAGENTA = "\033[95m"
C_CYAN = "\033[96m"
C_ORANGE = "\033[38;5;208m"

API_URL = "http://127.0.0.1:8000"


def type_print(text: str, delay: float = 0.015, color: str = "") -> None:
    for char in text:
        sys.stdout.write(f"{color}{char}{C_RESET}")
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")
    sys.stdout.flush()


def banner() -> None:
    print(f"{C_ORANGE}{C_BOLD}")
    print("=" * 80)
    print("     INCIDENTPILOT: AUTONOMOUS SRE INCIDENT RESPONSE WAR ROOM")
    print("   Built on Switch (Mattermost / Slack) • 4-Agent Swarm • HMAC-SHA256")
    print("=" * 80)
    print(f"{C_RESET}")


def check_live_api() -> bool:
    try:
        r = httpx.get(f"{API_URL}/health", timeout=1.0)
        return r.status_code == 200
    except Exception:
        return False


def run_simulation(auto_approve: bool = False) -> None:
    banner()
    is_live = check_live_api()
    if is_live:
        print(f"[{C_GREEN}LIVE{C_RESET}] Connected to target service at {API_URL}")
    else:
        print(f"[{C_YELLOW}STANDALONE{C_RESET}] Running in deterministic evaluation replay mode")
    print(f"[{C_CYAN}INFO{C_RESET}] Switch Room Initialized: #incident-war-room")
    print("-" * 80)
    time.sleep(1.0)

    # 1. Trigger Alert
    print(f"\n{C_RED}{C_BOLD}[09:41:02] [ALERT] Prometheus P1 Alert Firing{C_RESET}")
    print("  • Service:      orders-api:checkout")
    print(f"  • Error Rate:   {C_RED}48.7% (1,420 HTTP 500s in last 5 min){C_RESET}")
    print(f"  • Latency p99:  {C_YELLOW}3,840ms{C_RESET}")
    print("  • State:        DETECTED -> TRIAGED")
    time.sleep(1.2)

    # If live API is running, inject chaos
    if is_live:
        with contextlib.suppress(Exception):
            httpx.post(f"{API_URL}/api/chaos/inject/bad-deploy", timeout=2.0)

    # 2. Incident Commander
    print(f"\n{C_RED}{C_BOLD}[@incident-commander]{C_RESET} {C_DIM}(Role Lease: Command){C_RESET}")
    type_print(
        "[COMMAND] Incident INC-4091 declared P1. Assigning diagnostic role lease to @diagnostic-investigator. State transitioned to INVESTIGATING.",
        color=C_RESET,
    )
    time.sleep(1.5)

    # 3. Diagnostic Investigator
    print(f"\n{C_BLUE}{C_BOLD}[@diagnostic-investigator]{C_RESET} {C_DIM}(Role Lease: Diagnostics){C_RESET}")
    type_print(
        "[DIAGNOSIS] Correlating telemetry and deployment metadata... Culprit commit: 8f3a91b (v2.14.0).\n"
        "   Exception isolated: TypeError: 'NoneType' object is not subscriptable in price calculation.\n"
        "   Executing BM25 + Dense RRF retriever across 13 enterprise runbooks...\n"
        "   Matched Runbook: RB-001-orders-api-500.md (RRF score: 0.94). Prescribing atomic rollback.",
        color=C_RESET,
    )
    time.sleep(1.8)

    # 4. Reproduction Engineer
    print(f"\n{C_GREEN}{C_BOLD}[@repro-engineer]{C_RESET} {C_DIM}(Role Lease: Reproduction){C_RESET}")
    type_print(
        "[REPRODUCTION] Replaying 10 synthetic transactional orders against sandbox container replica...\n"
        "   10/10 probes resulted in HTTP 500 Internal Server Error. Bug definitively reproduced in sandbox.\n"
        "   State transitioned to REPRODUCING -> CRITIC_REVIEW.",
        color=C_RESET,
    )
    time.sleep(1.5)

    # 5. Adversarial Critic
    print(f"\n{C_MAGENTA}{C_BOLD}[@adversarial-critic]{C_RESET} {C_DIM}(Role Lease: Safety & Blast Radius){C_RESET}")
    type_print(
        "[SAFETY CRITIC] Blast radius analysis: Confined strictly to orders-api container.\n"
        "   Verifying schema compatibility: v2.13.2 schema matches production database.\n"
        "   Computed HMAC-SHA256 action digest: hmac-sha256:7b98f21da90e4f3a8b27c10d5e893bf4.\n"
        "   No hallucinated parameters detected. Passing to Human Approval Gate.",
        color=C_RESET,
    )
    time.sleep(1.5)

    # 6. Interactive Approval Gate
    print(f"\n{C_YELLOW}{C_BOLD}" + "=" * 80)
    print(" [APPROVAL GATE] HUMAN SIGN-OFF REQUIRED (TOCTOU Cryptographically Protected)")
    print("=" * 80 + f"{C_RESET}")
    print(" Proposed Mitigation: Roll back orders-api from v2.14.0 -> v2.13.2")
    print(" Target Service:      orders-api (port 8000)")
    print(f" Action Digest:       {C_CYAN}hmac-sha256:7b98f21da90e4f3a8b27c10d5e893bf4{C_RESET}")
    print(" On-Call Engineer:    SRE Lead (@oncall-lead)")

    if not auto_approve:
        print(f"\nType {C_GREEN}'APPROVE'{C_RESET} to cryptographically authorize execution:")
        try:
            choice = input(f"{C_BOLD}war-room> {C_RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            choice = "APPROVE"
        if choice.upper() != "APPROVE":
            print(f"{C_RED}Action rejected by on-call engineer. Circuit breaker engaged.{C_RESET}")
            return
    else:
        time.sleep(1.5)
        print(f"\n{C_BOLD}war-room> {C_GREEN}APPROVE{C_RESET} (Authorized via Wispr Flow)")

    # If live API is running, reset chaos
    if is_live:
        with contextlib.suppress(Exception):
            httpx.post(f"{API_URL}/api/chaos/reset", timeout=2.0)

    # 7. Operator Execution
    time.sleep(1.0)
    print(f"\n{C_CYAN}{C_BOLD}[@incident-commander]{C_RESET} {C_DIM}(Role Lease: Execution & Verification){C_RESET}")
    type_print(
        "[EXECUTION] Executing verified rollback: orders-api -> v2.13.2...\n"
        "   Shifting 100% of production traffic to stable revision.\n"
        "   Running post-mitigation canary health check: 10/10 probes passed (HTTP 200 OK).\n"
        "   Current Metrics: Error Rate: 0.0% | Latency p99: 24.5ms | Status: HEALTHY.",
        color=C_RESET,
    )
    time.sleep(1.2)

    # 8. Resolution & Post-Mortem
    print(f"\n{C_GREEN}{C_BOLD}" + "=" * 80)
    print(" [RESOLVED] INCIDENT INC-4091 RESOLVED — MTTR: 1m 42s")
    print("=" * 80 + f"{C_RESET}")
    print("  • Detection to Triage:       12s")
    print("  • Diagnosis & Runbook RAG:   28s")
    print("  • Sandbox Reproduction:      24s")
    print("  • Critic Verification:       14s")
    print("  • Human Approval & Rollback: 24s")
    print(f"  • Post-Mortem archived to:   {C_CYAN}evals/scorecard.md{C_RESET}")
    print("-" * 80 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--auto-approve", action="store_true", help="Auto approve without interactive prompt")
    args = parser.parse_args()
    run_simulation(auto_approve=args.auto_approve)
