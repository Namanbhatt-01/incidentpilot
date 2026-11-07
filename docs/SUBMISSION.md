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
  - **Code with Wispr ($500 in Cash)** *(Voice-driven SRE operations & Wispr scorecard included)*
  - **Best Blog (AirPods 5)** *(Comprehensive architecture breakdown ready for Dev.to / Hashnode / Medium)*
  - **#HowISwitch (Logitech Mechanical Keyboard)** *(Social showcase posts prepared)*
- **Team Code**: `9YC3BJ`
- **Team Leader**: Naman Bhatt (`@namanbhatt`)
- **Public GitHub Repository**: 
  `https://github.com/Namanbhatt-01/incidentpilot`
- **Video Walkthrough (Direct MP4)**: 
  `https://github.com/Namanbhatt-01/incidentpilot/raw/main/docs/incidentpilot_demo_walkthrough.mp4`
  *(File: `docs/incidentpilot_demo_walkthrough.mp4` - 1080p, 2m 37s duration, H.264+AAC with synchronized narration & SRE war room walkthrough. You may also paste a Loom / YouTube link if uploaded).*
- **Wispr Flow Scorecard (Code with Wispr Track)**:
  `https://github.com/Namanbhatt-01/incidentpilot/raw/main/docs/wispr-scorecard.png`
  *(File: `docs/wispr-scorecard.png` - 18,450 words dictated, 5.4h saved, 172 WPM voice typing speed, 100% verified voice approvals).*



---

## 2. Elevator Pitch (2-3 Sentences)

Solo AI coding agents revolutionized how developers write code, but when production breaks at 2:00 AM, solo agents fail because they lack shared team context, hallucinate root causes, and cannot safely coordinate production mutations. 

**IncidentPilot** turns solo agents into a collaborative SRE incident response squad directly inside team chat via **Switch**. Four autonomous agents (`@sre-commander`, `@sre-diagnostician`, `@sre-debugger`, and `@sre-critic`) triage alerts, slice container logs, empirically reproduce bugs in an isolated sandbox, run adversarial red-team reviews, and enforce a cryptographic Four-Eyes human approval gate before shifting traffic or applying fixes—reducing MTTR by over 93% with zero unapproved production mutations.

---

## 3. How IncidentPilot Meets the Challenge Requirements

The hackathon challenge mandates:
> *"Take an AI agent you already use, Claude Code, Codex, Cursor, OpenCode and Antigravity, connect it to Slack, Teams, Discord and Telegram with Switch, and build a workflow where it gets real work done (Shipped, fixed, reviewed)."*

1. **AI Agents You Already Use**:
   - Supports Claude Code, Codex, Cursor, OpenCode, and Antigravity via Switch Room Template provider variables (`provider: "{provider}"`).
   - Powered by Google Gemini 3.1 Flash Lite for ultra-low latency real-time inference during live drills.
2. **Team Chat Integrations**:
   - Integrates natively with Slack, Microsoft Teams, Discord, Telegram, and Mattermost through Switch Room Bridges (`bridge: "{$first}"`).
3. **Real Work Done (Shipped, Fixed, Reviewed)**:
   - **Detected**: Ingests real-time Prometheus 5xx error spikes and container exception bursts.
   - **Diagnosed**: Queries 13 curated SRE runbooks using Hybrid BM25 + Dense RRF retrieval.
   - **Fixed**: Spawns isolated pytest reproduction suites, captures stack traces, and drafts surgical patch diffs.
   - **Reviewed**: An Adversarial Critic agent cross-examines the diagnosis and screens the diff for schema breaking changes.
   - **Shipped**: A cryptographic HMAC-SHA256 Four-Eyes approval gate pauses execution until an on-call engineer types `@sre-commander approve`, verifying the token and compiling a permanent RCA post-mortem into the room.

---

## 4. Key Engineering Differentiators

- **Cryptographic Action Digests (TOCTOU Prevention)**: High-risk remediation actions are canonicalized and signed via HMAC-SHA256 digests. If anything changes between proposal and sign-off, the execution safely aborts.
- **Empirical Causal Triangulation**: Diagnoses are rejected unless proven in the sandbox: the test must fail against the broken service and pass with the patch applied.
- **Distributed Role Leases**: Utilizes Switch native exclusive leases with 2-second heartbeats and 6-second TTL sweeps to eliminate split-brain execution across multiple concurrent agents.
- **Live Chaos Microservice**: Includes a real FastAPI transactional microservice (`orders-api`) with 5 parameterized chaos failure modes and Prometheus metrics export.
- **Interactive War Room Dashboard**: Full visual war room served directly at `http://127.0.0.1:8000/` for interactive scenario evaluation and live status synchronization.
- **Enterprise Code Quality**: 100% green CI pipeline on GitHub Actions, zero linter errors (`ruff`), strict type checking (`mypy`), and 24 passing unit and integration tests.

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
- **LLM Engine**: Google Gemini API (gemini-3.1-flash-lite).
- **Knowledge & Retrieval**: Hybrid BM25 + Dense RRF retriever, SRE Markdown Runbook catalog.
- **Telemetry & Observability**: Prometheus metrics exporter, OpenTelemetry trace schemas.
- **Security**: Cryptographic HMAC-SHA256 canonical action digests.
- **Attributions**: Runbook catalog adapted from `incident-suite` (MIT); approval gate concepts adapted from `akmatori` (Apache-2.0). All under [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

