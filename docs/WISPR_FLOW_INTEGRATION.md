# Voice-Driven SRE Operations: Wispr Flow Integration Architecture

*Integration guide for voice-enabled operations with IncidentPilot and Switch.*

---

## 1. Overview

In high-stress production outages (such as 2:00 AM PagerDuty incidents), typing long triage prompts and copying error tokens while inspecting live Grafana graphs causes context-switching and cognitive overload.

**IncidentPilot** is architected to accept voice-dictated commands via tools like **Wispr Flow**:
1. **Voice-Prompting the Incident Squad**: Dictating triage summaries directly into team chat (Mattermost, Slack, Discord).
2. **Hands-Free Mitigation Sign-Off**: Dictating human approval commands (`@sre-commander approve`) while hands remain on terminal diagnostics.
3. **Runbook & Room Instructions**: Creating room templates via natural conversational speech.

---

## 2. Voice Prompts Supported by IncidentPilot

| Operational Phase | Dictated Voice Command | Handling Agent | Target Implementation |
| :--- | :--- | :--- | :--- |
| **Room Briefing** | *"You are the incident war-room squad. Triage all incoming checkout reports, assign severity P1 to 500 errors, quote exact log lines, and require explicit human sign-off before applying any patch."* | Switch Room Engine | `switch/templates/incident-pilot.template.yaml` |
| **Emergency Triage** | *"Incident Commander, checkout is throwing HTTP 500 errors since the 09:40 deployment, investigate cart service and check database connections immediately."* | `@sre-commander` | `packages/application/handlers/triage.py` |
| **Hands-Free Sign-Off** | *"Incident Commander, approve patch token and execute verified rollback."* | `@sre-commander` | `packages/application/handlers/approval.py` |

---

## 3. Submitting for the "Code with Wispr" Side Track ($500)

If you actively use Wispr Flow on macOS to dictate prompts, runbooks, or commands during development:
1. Open the **Wispr Flow desktop app**.
2. Navigate to the **Insights** tab showing your personal words dictated and time saved.
3. Take a screenshot of your active Insights dashboard.
4. Save the screenshot and attach it to your submission form on the [WeMakeDevs Portal](https://www.wemakedevs.org/hackathons/switch/submit).

> **Note on Submission Hygiene**: Do not submit mock or synthetic scorecard metrics. Only submit an authentic screenshot from your active Wispr Flow client. If you did not use voice dictation during the build, leave the Code with Wispr side track unchecked.
