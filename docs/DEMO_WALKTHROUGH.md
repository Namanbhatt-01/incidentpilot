# IncidentPilot: 3-Minute Demo Video Walkthrough Script

This script is tailored specifically for the **Flip the Switch Hackathon** judging panel.
- **Target Duration**: 2:45 to 3:00 minutes.
- **Screen Layout**: Split screen — Left side: Team Chat (Mattermost / Switch Room), Right side: Terminal (Chaos injection & verification logs).

---

## Act 1: The Incident War Room & Squad Standing By (0:00 - 0:35)
- **Visual**: Show the Switch room `#sre-incident-war-room` in Mattermost.
- **Narrator**:
  > *"When production breaks at 2 AM, solo AI agents fail because they lack shared context, hallucinate root causes, and can't coordinate with human teams.
  > Meet **IncidentPilot**: an autonomous, human-supervised SRE incident response team built natively on Switch.
  > Here in our incident war-room, Switch has brought four specialized agents into our channel:
  > `@sre-commander`, our lead orchestrator; `@sre-diagnostician`, our log and telemetry analyst; `@sre-debugger`, our sandbox reproduction engineer; and `@sre-critic`, our independent adversarial reviewer."*

---

## Act 2: Production Incident & Empirical Reproduction (0:35 - 1:15)
- **Visual**: Right side terminal executes `./sandbox/chaos/inject.py bad-deploy`. Left side: Teammate Sam posts: `@sre-commander Checkout is failing with HTTP 500 errors! Can you investigate?`
- **Narrator**:
  > *"A deployment regression just hit our checkout microservice. Sam alerts the channel.
  > Watch how Switch coordinates the response:
  > First, `@sre-commander` acknowledges the report, creates a live incident war-board document directly in the room, and classifies it as P1.
  > Next, `@sre-diagnostician` correlates container error logs and retrieves Runbook RB-001 using hybrid search.
  > Instead of guessing, `@sre-debugger` spins up an isolated test in our sandbox. It reproduces the exact failure — a NoneType error in price calculation — and drafts a surgical null-guard patch."*

---

## Act 3: Adversarial Review & Four-Eyes Human Sign-Off (1:15 - 2:05)
- **Visual**: Show `@sre-critic` review in the chat thread, followed by the approval card.
- **Narrator**:
  > *"Now, here is what separates IncidentPilot from average AI vibe-coding:
  > `@sre-critic` acts as an adversarial SRE. It independently reviews the evidence, confirms the causal link, and verifies that the patch diff has zero breaking schema changes.
  > But IncidentPilot NEVER touches production without human authority.
  > Our Four-Eyes Approval Gate halts execution and computes a cryptographic SHA-256 action digest to prevent tampering.
  > Commander prompts Priya for sign-off.
  > Priya types: `@sre-commander approve`.
  > The cryptographic token is verified, and the patch is applied."*

---

## Act 4: Shipped, Fixed, and Knowledge Preserved (2:05 - 2:45)
- **Visual**: Terminal shows regression tests passing (`100% green`). Mattermost shows incident resolved and post-mortem generated.
- **Narrator**:
  > *"In seconds, our regression test suite verifies recovery: twelve tests pass, zero fail, and orders-api returns HTTP 200 OK.
  > The incident is marked RESOLVED, and Switch generates a permanent Root Cause Analysis post-mortem document directly into the room.
  > Shipped, fixed, and reviewed — together."*

---

## Act 5: Benchmark & Outro (2:45 - 3:00)
- **Visual**: Show `evals/scorecard.md` table on screen.
- **Narrator**:
  > *"Across our 5-scenario evaluation benchmark, IncidentPilot delivers an average MTTR reduction of over 98% with 100% safety compliance.
  > Solo agents made you code faster; Switch turns them into your best teammates.
  > Thank you!"*
