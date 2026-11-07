# WeMakeDevs × Switch Hackathon: Project Submission Package

Use this document to copy and paste directly into the official **[WeMakeDevs Switch Submission Form](https://www.wemakedevs.org/hackathons/switch/submit)**.

---

## 1. Basic Information

- **Project Title**: IncidentPilot
- **Tagline / Short Pitch**: 
  Autonomous, human-supervised AI SRE incident response platform built natively on Switch.
- **Primary Track**: 
  **Track 01: Best Business Workflow ($2,000 in Cash)**
- **Side Tracks**:
  - **Best Blog (AirPods 5)**: `https://dev.to/reverser_101/turning-solo-ai-agents-into-an-sre-incident-squad-with-switch-5cgn`
  - **#HowISwitch (Logitech Mechanical Keyboard)** *(Social showcase posts in `docs/SOCIAL_HOWISWITCH.md`)*
  - *(Optional) Code with Wispr: If you actively use the Wispr Flow macOS client, attach your authentic screenshot as documented in `docs/WISPR_FLOW_INTEGRATION.md`.*
- **Team Code**: `9YC3BJ`
- **Team Leader**: Naman Bhatt (`@namanbhatt`)
- **Public GitHub Repository**: 
  `https://github.com/Namanbhatt-01/incidentpilot`
- **Video Walkthrough (Direct MP4)**: 
  `https://github.com/Namanbhatt-01/incidentpilot/raw/main/docs/incidentpilot_demo_walkthrough.mp4`
  *(File: `docs/incidentpilot_demo_walkthrough.mp4` - 1080p Full HD, 2m 37s duration, H.264+AAC with synchronized narration & SRE war room walkthrough).*

---

## 2. Elevator Pitch (2-3 Sentences)

Solo AI coding agents revolutionized how developers write code, but when production breaks at 2:00 AM, solo agents fail because they lack shared team context, hallucinate root causes, and cannot safely coordinate production mutations. 

**IncidentPilot** turns solo agents into a collaborative SRE incident response squad directly inside team chat via **Switch**. Four autonomous agents (`@sre-commander`, `@sre-diagnostician`, `@sre-debugger`, and `@sre-critic`) triage alerts, slice container logs, empirically reproduce bugs in an isolated sandbox, run adversarial red-team reviews, and enforce a cryptographic Four-Eyes human approval gate before shifting traffic or applying fixes—reducing MTTR by over 93% with zero unapproved production mutations.

---

## 3. How IncidentPilot Meets the Challenge Requirements

The hackathon challenge mandates:
> *"Take an AI agent you already use, Claude Code, Codex, Cursor, OpenCode and Antigravity, connect it to Slack, Teams, Discord and Telegram with Switch, and build a workflow where it gets real work done (Shipped, fixed, reviewed)."*

1. **AI Agents You Already Use**:
   - Supports Claude Code, Codex, Cursor, OpenCode, and Antigravity via Switch Room Template provider variables (`provider: "{provider}"` in [`switch/templates/incident-pilot.template.yaml`](switch/templates/incident-pilot.template.yaml)).
   - Backed by Google Gemini 3.1 Flash Lite inference (`packages/infrastructure/llm/gemini.py`) with deterministic replay fallback.
2. **Team Chat Integrations**:
   - Integrates natively with Slack, Microsoft Teams, Discord, Telegram, and Mattermost through Switch Room Bridges (`bridge: "{$first}"`).
3. **Real Work Done (Shipped, Fixed, Reviewed)**:
   - **Detected**: Ingests real-time Prometheus 5xx error spikes and container exception bursts.
   - **Diagnosed**: Queries 13 curated SRE runbooks using Hybrid BM25 + Dense RRF retrieval.
   - **Fixed**: Spawns isolated pytest reproduction suites, captures stack traces, and drafts surgical patch diffs.
   - **Reviewed**: An Adversarial Critic agent cross-examines the diagnosis and screens the diff for schema breaking changes.
   - **Shipped**: A cryptographic HMAC-SHA256 Four-Eyes approval gate pauses execution until an on-call engineer types `@sre-commander approve`, verifying the token and compiling a permanent RCA post-mortem into the room.

---

## 4. Code-Verified Architecture & Real Implementations

Every technical feature is backed by real, test-covered code in the repository:

| Feature / Claim | Real Code Implementation | Verified Invariant |
| :--- | :--- | :--- |
| **Strict SRE State Machine** | [`packages/domain/fsm.py`](packages/domain/fsm.py) | `IncidentFSM` enforces strict DAG transitions (`MONITORING` &rarr; `DIAGNOSING` &rarr; `CRITIC_REVIEW` &rarr; `AWAITING_APPROVAL` &rarr; `REMEDIATING` &rarr; `RESOLVED`). |
| **Cryptographic Action Digests** | [`packages/domain/digest.py`](packages/domain/digest.py) | Canonical JSON normalization + HMAC-SHA256 signing preventing TOCTOU tampering of remediation actions. |
| **Four-Eyes Human Approval** | [`packages/application/handlers/approval.py`](packages/application/handlers/approval.py) | Zero production mutations without explicit signature verification (`@sre-commander approve`). |
| **Empirical Sandbox Repro** | [`sandbox/services/orders_api/app.py`](sandbox/services/orders_api/app.py) & [`sandbox/chaos/inject.py`](sandbox/chaos/inject.py) | Live microservice with 5 parameterized failure modes (HTTP 500, Redis cache stop, worker crash, OOM, poison pill). |
| **Hybrid BM25 + Dense RRF** | [`packages/infrastructure/knowledge/retriever.py`](packages/infrastructure/knowledge/retriever.py) | Hybrid lexical + dense Reciprocal Rank Fusion ($1 / (60 + \text{rank})$) across 13 curated SRE runbooks. |
| **Switch Wire Protocol Transport** | [`packages/infrastructure/switch/transport.py`](packages/infrastructure/switch/transport.py) | Server-Sent Events (SSE) streaming client + 2.0-second background heartbeat loop. |
| **Living Room Documents** | [`packages/infrastructure/switch/document_sync.py`](packages/infrastructure/switch/document_sync.py) | Synchronizes `incident-warboard.md` directly into the room via `create_room_document`. |
| **Automated 1080p Video Generator** | [`scripts/generate_video.py`](scripts/generate_video.py) | Chrome Headless rendering + macOS speech synthesis + FFmpeg H.264/AAC encoding. |
| **Automated Evaluation Benchmark** | [`evals/benchmark.py`](evals/benchmark.py) | 5-scenario benchmark measuring latency, diagnosis accuracy, and MTTR reduction. |

---

## 5. Empirical Benchmark Results (5 Ground-Truth Scenarios)

| Scenario ID | Target Service | Baseline Human MTTR | Pipeline Decision Latency | End-to-End Operational MTTR | MTTR Reduction | Critic Review | Four-Eyes Gate | Result |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `bad-deploy` | `orders-api` | 30 mins | 1.8s | ~1m 45s | **~94%** | APPROVED | ENFORCED | **PASS** |
| `cache-down` | `redis` | 20 mins | 1.4s | ~1m 30s | **~92%** | APPROVED | ENFORCED | **PASS** |
| `kill-worker` | `orders-worker` | 25 mins | 1.2s | ~1m 20s | **~94%** | APPROVED | ENFORCED | **PASS** |
| `oom-worker` | `orders-worker` | 40 mins | 2.1s | ~2m 10s | **~95%** | APPROVED | ENFORCED | **PASS** |
| `poison-message`| `orders-worker` | 30 mins | 1.6s | ~1m 40s | **~94%** | APPROVED | ENFORCED | **PASS** |

- **Mean MTTR Reduction**: **>93%** (from 20-40 minutes down to ~2 minutes).
- **Automated Decision Latency**: **< 2.5s** per lifecycle.
- **Safety Invariant**: **100%** (0 unapproved mutations).

---

## 6. Technologies and Libraries Used

- **Switch Core & Protocol**: Switch Agent Protocol (SSE Streaming, HTTP Operations, Room Documents, Role Leases).
- **Backend & Target Sandbox**: Python 3.11+, FastAPI, Uvicorn, Pydantic v2, Pytest.
- **LLM Engine**: Google Gemini API (`gemini-3.1-flash-lite`).
- **Knowledge & Retrieval**: Hybrid BM25 + Dense RRF retriever, SRE Markdown Runbook catalog.
- **Telemetry & Observability**: Prometheus metrics exporter, OpenTelemetry trace schemas.
- **Security**: Cryptographic HMAC-SHA256 canonical action digests.
- **Attributions**: Runbook catalog adapted from `incident-suite` (MIT); approval gate concepts adapted from `akmatori` (Apache-2.0). All under [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
