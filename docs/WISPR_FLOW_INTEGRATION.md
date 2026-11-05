# Code with Wispr Flow: Voice-Driven SRE Operations

*Guide for the Code with Wispr Hackathon Side Track ($500 in Cash)*

---

## 1. Overview
Wispr Flow allows developers to speak prompts, room instructions, and documentation at 3x the speed of typing. In **IncidentPilot**, voice is used as a primary input mechanism for emergency SRE incident response:
1. **Voice-Prompting the Incident Squad**: Speaking incident triage reports during high-stress production outages.
2. **Dictating Runbooks & Room Instructions**: Creating room templates and runbooks via natural speech.
3. **Voice Approval of Production Patches**: Dictating sign-off commands into chat hands-free while inspecting terminal dashboards.

---

## 2. Voice Prompts Used in IncidentPilot Development

| Stage | Dictated Prompt (Wispr Flow) | Target Destination |
| :--- | :--- | :--- |
| **Room Briefing** | *"You are the incident war-room squad. Triage all incoming checkout reports, assign severity P1 to 500 errors, quote exact log lines, and require explicit human sign-off before applying any patch."* | `switch/templates/incident-pilot.template.yaml` |
| **Incident Trigger** | *"Incident Commander, checkout is throwing HTTP 500 errors since the 09:40 deployment, investigate cart service and check database connections immediately."* | Mattermost `#sre-incident-war-room` |
| **Human Sign-Off** | *"Incident Commander, approve patch token appr-8f3a1c and deploy to sandbox."* | Mattermost Channel |

---

## 3. Submission Scorecard Instructions
To submit for the **Code with Wispr ($500 cash)** side track:
1. Open the **Wispr Flow desktop app**.
2. Navigate to **Insights** tab.
3. Take a screenshot showing your words spoken and time saved during the hackathon.
4. Attach `wispr-scorecard.png` alongside your final project submission.

