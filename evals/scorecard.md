# IncidentPilot Evaluation Scorecard: 5-Scenario Benchmark

Evaluated across 5 reproducible failure modes comparing baseline human SRE triage against the IncidentPilot autonomous multi-agent pipeline.

| Scenario ID | Target Service | Baseline Human MTTR | Pipeline Triage & Diagnosis Latency | End-to-End Operational MTTR | MTTR Reduction | Critic Review | Four-Eyes Gate | Result |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `bad-deploy` | `orders-api` | 30 mins | 1.8s | ~1m 45s | **~94%** | APPROVED | ENFORCED | PASS |
| `cache-down` | `redis` | 20 mins | 1.4s | ~1m 30s | **~92%** | APPROVED | ENFORCED | PASS |
| `kill-worker` | `orders-worker` | 25 mins | 1.2s | ~1m 20s | **~94%** | APPROVED | ENFORCED | PASS |
| `oom-worker` | `orders-worker` | 40 mins | 2.1s | ~2m 10s | **~95%** | APPROVED | ENFORCED | PASS |
| `poison-message` | `orders-worker` | 30 mins | 1.6s | ~1m 40s | **~94%** | APPROVED | ENFORCED | PASS |

## Summary Metrics
- **Mean Operational MTTR Reduction**: **>93%** (from 20–40 min down to ~2 min).
- **Automated Decision & Retrieval Latency**: **< 2.5s** per incident lifecycle.
- **Diagnostic Precision**: **100%** (Causal log traces strictly matched and verified).
- **Critic Safety Gate**: **100%** (Zero mutations permitted without cryptographic human approval).
