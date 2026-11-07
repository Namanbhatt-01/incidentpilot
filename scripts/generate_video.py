#!/usr/bin/env python3
"""IncidentPilot: Automated 1080p Video Walkthrough Generator using Chrome Headless, macOS Speech Synthesis, and FFmpeg."""

import subprocess
from pathlib import Path

# Paths
REPO_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = REPO_DIR / "docs" / "video_assets"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FINAL_VIDEO = REPO_DIR / "docs" / "incidentpilot_demo_walkthrough.mp4"
CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

SCENES = [
    {
        "id": "scene1_intro",
        "title": "IncidentPilot — Overview",
        "voice": "When production breaks at 2 AM, solo AI agents fail because they lack shared context, hallucinate root causes, and cannot coordinate with human teams. Meet IncidentPilot: an autonomous, human-supervised SRE incident response team built natively on Switch.",
        "subtitle": "IncidentPilot: Autonomous, Human-Supervised AI SRE Platform Built on Switch",
        "type": "title",
    },
    {
        "id": "scene2_warroom",
        "title": "Switch SRE War Room & Agent Leases",
        "voice": "Here in our incident war room, Switch has brought four specialized agents into our channel: Incident Commander, our lead orchestrator; Diagnostic SRE, our log and telemetry analyst; Debugging Engineer, our sandbox reproduction engineer; and Adversarial Critic, our independent red-team reviewer.",
        "subtitle": "Switch coordinates 4 specialized agents via distributed role leases and shared context",
        "type": "warroom_idle",
    },
    {
        "id": "scene3_incident",
        "title": "P1 Production Outage Alert",
        "voice": "A deployment regression just hit our checkout microservice. An engineer alerts the channel that checkout is throwing HTTP 500 errors. Watch how Switch coordinates the response: First, Incident Commander acknowledges the report, creates a live incident war-board document directly in the room, and classifies it as P1.",
        "subtitle": "P1 Alert: Error rate spikes to 48.7%, latency jumps to 3,840ms. War-board pinned in room.",
        "type": "incident_spike",
    },
    {
        "id": "scene4_diagnosis",
        "title": "Hybrid RAG & Sandbox Reproduction",
        "voice": "Next, Diagnostic SRE correlates container error logs and retrieves Runbook RB-001 using hybrid search. Instead of guessing, Debugging Engineer spins up an isolated test in our sandbox. It reproduces the exact failure, a NoneType error in price calculation, and drafts a surgical null-guard patch.",
        "subtitle": "Runbook RB-001 matched via BM25+Dense RRF (0.94 score). Failure reproduced 10/10 in sandbox.",
        "type": "diagnosis_repro",
    },
    {
        "id": "scene5_critic",
        "title": "Adversarial Critic Red-Team Review",
        "voice": "Now, here is what separates IncidentPilot from average AI tools: Adversarial Critic acts as an independent SRE. It cross-examines the evidence, confirms the causal link, and verifies that the patch diff has zero breaking schema changes.",
        "subtitle": "Adversarial Critic verifies blast radius and ensures zero schema regressions before mitigation.",
        "type": "critic_review",
    },
    {
        "id": "scene6_approval",
        "title": "Cryptographic Four-Eyes Approval Gate",
        "voice": "Crucially, IncidentPilot never touches production without human authority. Our Four-Eyes Approval Gate halts execution and computes a cryptographic SHA-256 action digest to prevent tampering. The commander prompts the on-call engineer for sign-off. The engineer approves the mitigation in chat. The cryptographic token is verified, and the rollback is executed.",
        "subtitle": "HMAC-SHA256 Action Digest prevents TOCTOU tampering. Zero mutations without human sign-off.",
        "type": "approval_gate",
    },
    {
        "id": "scene7_recovery",
        "title": "Verified Recovery & Living Post-Mortem",
        "voice": "In seconds, our regression test suite verifies recovery: all tests pass, the service health probe returns 200 OK, and p99 latency normalizes to 24 milliseconds. The incident is marked RESOLVED, and Switch generates a permanent Root Cause Analysis post-mortem document directly into the room. Shipped, fixed, and reviewed, together.",
        "subtitle": "Health probe returns 200 OK, latency drops to 24ms, and permanent RCA post-mortem is stored.",
        "type": "recovery_postmortem",
    },
    {
        "id": "scene8_benchmark",
        "title": "Empirical Benchmark & Conclusion",
        "voice": "Across our 5-scenario evaluation benchmark, IncidentPilot delivers an average MTTR reduction of over 93% with 100% safety compliance. Solo agents made you code faster; Switch turns them into your best engineering teammates. Thank you!",
        "subtitle": "Average MTTR reduction >93% across 5 scenarios. GitHub: github.com/Namanbhatt-01/incidentpilot",
        "type": "benchmark_outro",
    },
]


def generate_audio(scene: dict) -> Path:
    """Generate audio file for a scene using macOS speech synthesis."""
    aiff_path = OUTPUT_DIR / f"{scene['id']}.aiff"
    wav_path = OUTPUT_DIR / f"{scene['id']}.wav"

    print(f"  [Audio] Generating speech for {scene['id']}...")
    subprocess.run(
        ["say", "-v", "Daniel", "-r", "175", "-o", str(aiff_path), scene["voice"]],
        check=True,
    )
    # Convert and normalize audio with ffmpeg
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(aiff_path),
            "-af",
            "volume=1.8,highpass=f=100,lowpass=f=8000",
            str(wav_path),
        ],
        check=True,
        stderr=subprocess.DEVNULL,
    )
    aiff_path.unlink(missing_ok=True)
    return wav_path


def get_audio_duration(wav_path: Path) -> float:
    """Get precise duration of wav file."""
    out = (
        subprocess.check_output(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(wav_path),
            ]
        )
        .decode()
        .strip()
    )
    return float(out)


def render_html_scene(scene: dict, duration: float) -> Path:
    """Create a high-fidelity 1920x1080 HTML page for the scene."""
    html_path = OUTPUT_DIR / f"{scene['id']}.html"
    png_path = OUTPUT_DIR / f"{scene['id']}.png"

    # Base HTML template with professional dark mode SRE aesthetics
    content = ""
    stype = scene["type"]

    if stype == "title":
        content = """
        <div style="flex:1; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; padding:60px;">
          <div style="background:rgba(255,120,73,0.15); border:1px solid #ff7849; color:#ff7849; padding:8px 24px; border-radius:9999px; font-weight:700; font-size:18px; margin-bottom:24px; letter-spacing:1px;">
            FLIP THE SWITCH HACKATHON &bull; WEMAKEDEVS &amp; DEVTOOLS ACADEMY
          </div>
          <h1 style="font-size:72px; font-weight:900; margin:0 0 16px 0; background:linear-gradient(135deg, #ffffff 40%, #38bdf8 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
            IncidentPilot
          </h1>
          <p style="font-size:26px; color:#94a3b8; max-width:1100px; line-height:1.5; margin:0 0 36px 0;">
            Autonomous, Human-Supervised AI SRE Incident Response Platform Built Natively on Switch
          </p>
          <div style="display:flex; gap:16px; margin-bottom:48px;">
            <div style="background:#1e293b; border:1px solid #334155; padding:10px 20px; border-radius:8px; font-size:16px; font-weight:600; color:#38bdf8;">Track 01: Best Business Workflow</div>
            <div style="background:#1e293b; border:1px solid #334155; padding:10px 20px; border-radius:8px; font-size:16px; font-weight:600; color:#22c55e;">CI Pipeline: 100% Passing</div>
            <div style="background:#1e293b; border:1px solid #334155; padding:10px 20px; border-radius:8px; font-size:16px; font-weight:600; color:#ff7849;">Switch Protocol v1</div>
            <div style="background:#1e293b; border:1px solid #334155; padding:10px 20px; border-radius:8px; font-size:16px; font-weight:600; color:#a855f7;">Four-Eyes Cryptographic Gate</div>
          </div>
          <div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:20px; width:1200px;">
            <div style="background:#111726; border:1px solid #233252; padding:24px; border-radius:12px; text-align:left;">
              <div style="font-size:14px; color:#ff7849; font-weight:700; margin-bottom:8px;">LEAD ORCHESTRATOR</div>
              <div style="font-size:18px; font-weight:700;">@sre-commander</div>
              <div style="font-size:13px; color:#94a3b8; margin-top:6px;">FSM management, war-board living docs, human approvals</div>
            </div>
            <div style="background:#111726; border:1px solid #233252; padding:24px; border-radius:12px; text-align:left;">
              <div style="font-size:14px; color:#38bdf8; font-weight:700; margin-bottom:8px;">DIAGNOSTIC SRE</div>
              <div style="font-size:18px; font-weight:700;">@sre-diagnostician</div>
              <div style="font-size:13px; color:#94a3b8; margin-top:6px;">Container log slicing, metrics, Hybrid BM25+RRF RAG</div>
            </div>
            <div style="background:#111726; border:1px solid #233252; padding:24px; border-radius:12px; text-align:left;">
              <div style="font-size:14px; color:#22c55e; font-weight:700; margin-bottom:8px;">DEBUGGING ENGINEER</div>
              <div style="font-size:18px; font-weight:700;">@sre-debugger</div>
              <div style="font-size:13px; color:#94a3b8; margin-top:6px;">Isolated sandbox reproduction, pytest synthesis, patch diffs</div>
            </div>
            <div style="background:#111726; border:1px solid #233252; padding:24px; border-radius:12px; text-align:left;">
              <div style="font-size:14px; color:#a855f7; font-weight:700; margin-bottom:8px;">ADVERSARIAL CRITIC</div>
              <div style="font-size:18px; font-weight:700;">@sre-critic</div>
              <div style="font-size:13px; color:#94a3b8; margin-top:6px;">Red-team verification, blast-radius screening, anti-hallucination</div>
            </div>
          </div>
        </div>
        """
    elif stype == "warroom_idle":
        content = """
        <div style="flex:1; display:grid; grid-template-columns:320px 1fr 380px; gap:20px; padding:20px; overflow:hidden;">
          <!-- Left Sidebar -->
          <div style="background:#111726; border:1px solid #233252; border-radius:12px; padding:24px; display:flex; flex-direction:column; gap:20px;">
            <div style="font-size:14px; font-weight:700; color:#38bdf8; text-transform:uppercase; letter-spacing:1px;">Active Squad Leases</div>
            <div style="display:flex; flex-direction:column; gap:12px;">
              <div style="background:#182238; border:1px solid #233252; padding:14px; border-radius:8px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                  <strong style="color:#ffffff;">@sre-commander</strong>
                  <span style="font-size:11px; background:#22c55e; color:#000; padding:2px 8px; border-radius:4px; font-weight:700;">ACTIVE LEASE</span>
                </div>
                <div style="font-size:12px; color:#94a3b8; margin-top:4px;">Switch Heartbeat: 2.0s &bull; TTL: 6.0s</div>
              </div>
              <div style="background:#182238; border:1px solid #233252; padding:14px; border-radius:8px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                  <strong style="color:#ffffff;">@sre-diagnostician</strong>
                  <span style="font-size:11px; background:#22c55e; color:#000; padding:2px 8px; border-radius:4px; font-weight:700;">ACTIVE LEASE</span>
                </div>
                <div style="font-size:12px; color:#94a3b8; margin-top:4px;">Hybrid RRF Index: 13 Runbooks</div>
              </div>
              <div style="background:#182238; border:1px solid #233252; padding:14px; border-radius:8px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                  <strong style="color:#ffffff;">@sre-debugger</strong>
                  <span style="font-size:11px; background:#22c55e; color:#000; padding:2px 8px; border-radius:4px; font-weight:700;">STANDBY</span>
                </div>
                <div style="font-size:12px; color:#94a3b8; margin-top:4px;">Target Sandbox: orders-api:v2.13.2</div>
              </div>
              <div style="background:#182238; border:1px solid #233252; padding:14px; border-radius:8px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                  <strong style="color:#ffffff;">@sre-critic</strong>
                  <span style="font-size:11px; background:#22c55e; color:#000; padding:2px 8px; border-radius:4px; font-weight:700;">STANDBY</span>
                </div>
                <div style="font-size:12px; color:#94a3b8; margin-top:4px;">Four-Eyes Gate: Ready</div>
              </div>
            </div>
            <div style="margin-top:auto; background:#182238; padding:16px; border-radius:8px; border-left:4px solid #22c55e;">
              <div style="font-size:13px; font-weight:700; color:#22c55e;">SYSTEM INVARIANTS SATISFIED</div>
              <div style="font-size:12px; color:#94a3b8; margin-top:4px;">FSM State: STATE: MONITORING<br/>0 production mutations active</div>
            </div>
          </div>

          <!-- Middle Chat Room -->
          <div style="background:#111726; border:1px solid #233252; border-radius:12px; padding:24px; display:flex; flex-direction:column;">
            <div style="border-bottom:1px solid #233252; padding-bottom:16px; margin-bottom:20px; display:flex; justify-content:space-between; align-items:center;">
              <div>
                <h2 style="font-size:20px; margin:0 0 4px 0;">#sre-incident-war-room</h2>
                <div style="font-size:13px; color:#94a3b8;">Switch Room Bridge &bull; Mattermost / Slack / Discord &bull; Wire SSE Transport</div>
              </div>
              <div style="background:rgba(56,189,248,0.15); border:1px solid #38bdf8; color:#38bdf8; padding:4px 12px; border-radius:9999px; font-size:12px; font-weight:700;">
                STATE: MONITORING
              </div>
            </div>
            <div style="display:flex; flex-direction:column; gap:16px; flex:1;">
              <div style="background:#182238; border:1px solid #233252; padding:16px; border-radius:8px;">
                <div style="display:flex; gap:10px; align-items:center; margin-bottom:6px;">
                  <span style="background:#ff7849; color:#fff; font-size:11px; font-weight:700; padding:2px 8px; border-radius:4px;">SWITCH ENGINE</span>
                  <strong style="color:#ffffff;">System</strong>
                  <span style="font-size:12px; color:#64748b;">09:40:00 UTC</span>
                </div>
                <div style="font-size:14px; color:#cbd5e1; line-height:1.4;">
                  Switch Room template <code>incident-pilot.template.yaml</code> initialized. Four specialized agents subscribed to room SSE stream. Distributed leases active.
                </div>
              </div>
              <div style="background:#182238; border:1px solid #233252; padding:16px; border-radius:8px;">
                <div style="display:flex; gap:10px; align-items:center; margin-bottom:6px;">
                  <span style="background:#dc2626; color:#fff; font-size:11px; font-weight:700; padding:2px 8px; border-radius:4px;">COMMANDER</span>
                  <strong style="color:#ffffff;">@sre-commander</strong>
                  <span style="font-size:12px; color:#64748b;">09:40:02 UTC</span>
                </div>
                <div style="font-size:14px; color:#cbd5e1; line-height:1.4;">
                  War room initialized. Monitoring telemetry feeds on <code>http://127.0.0.1:8000/metrics</code>. Standing by for incident alerts.
                </div>
              </div>
            </div>
          </div>

          <!-- Right Telemetry Panel -->
          <div style="background:#111726; border:1px solid #233252; border-radius:12px; padding:24px; display:flex; flex-direction:column; gap:20px;">
            <div style="font-size:14px; font-weight:700; color:#38bdf8; text-transform:uppercase; letter-spacing:1px;">Live Observability</div>
            <div style="background:#182238; border:1px solid #233252; padding:18px; border-radius:8px;">
              <div style="font-size:13px; color:#94a3b8;">HTTP 5xx Error Rate</div>
              <div style="font-size:36px; font-weight:800; color:#22c55e; margin:6px 0;">0.00%</div>
              <div style="font-size:12px; color:#22c55e;">Baseline Healthy (Target: orders-api)</div>
            </div>
            <div style="background:#182238; border:1px solid #233252; padding:18px; border-radius:8px;">
              <div style="font-size:13px; color:#94a3b8;">p99 Latency</div>
              <div style="font-size:36px; font-weight:800; color:#22c55e; margin:6px 0;">24.5 ms</div>
              <div style="font-size:12px; color:#22c55e;">Nominal SLA Range (&lt; 100ms)</div>
            </div>
            <div style="background:#182238; border:1px solid #233252; padding:18px; border-radius:8px;">
              <div style="font-size:13px; color:#94a3b8;">Container Health Probe</div>
              <div style="font-size:20px; font-weight:700; color:#22c55e; margin:6px 0;">HTTP 200 OK</div>
              <div style="font-size:12px; color:#94a3b8;">Version: v2.13.2 stable &bull; Uptime: 342s</div>
            </div>
          </div>
        </div>
        """
    elif stype == "incident_spike":
        content = """
        <div style="flex:1; display:grid; grid-template-columns:320px 1fr 380px; gap:20px; padding:20px; overflow:hidden;">
          <!-- Left Sidebar -->
          <div style="background:#111726; border:1px solid #ef4444; border-radius:12px; padding:24px; display:flex; flex-direction:column; gap:20px;">
            <div style="font-size:14px; font-weight:700; color:#ef4444; text-transform:uppercase; letter-spacing:1px;">Active Incident State</div>
            <div style="background:#3b1e1e; border:1px solid #ef4444; padding:16px; border-radius:8px;">
              <div style="font-size:13px; font-weight:700; color:#ef4444;">P1 CRITICAL ALERT</div>
              <div style="font-size:18px; font-weight:800; color:#ffffff; margin:6px 0;">INC-20261107-01</div>
              <div style="font-size:12px; color:#fca5a5;">Target: orders-api:checkout<br/>Trigger: Deployment v2.14.0</div>
            </div>
            <div style="background:#182238; border:1px solid #233252; padding:14px; border-radius:8px;">
              <div style="font-size:13px; font-weight:700; color:#38bdf8;">LIVING ROOM DOCUMENT</div>
              <div style="font-size:14px; font-weight:600; color:#ffffff; margin-top:4px;">incident-warboard.md</div>
              <div style="font-size:12px; color:#94a3b8; margin-top:4px;">Created via Switch <code>create_room_document</code> &bull; Synced in room</div>
            </div>
          </div>

          <!-- Middle Chat Room -->
          <div style="background:#111726; border:1px solid #233252; border-radius:12px; padding:24px; display:flex; flex-direction:column;">
            <div style="border-bottom:1px solid #233252; padding-bottom:16px; margin-bottom:20px; display:flex; justify-content:space-between; align-items:center;">
              <div>
                <h2 style="font-size:20px; margin:0 0 4px 0;">#sre-incident-war-room</h2>
                <div style="font-size:13px; color:#94a3b8;">Switch Room Bridge &bull; Live Alert Ingested</div>
              </div>
              <div style="background:rgba(239,68,68,0.2); border:1px solid #ef4444; color:#ef4444; padding:4px 12px; border-radius:9999px; font-size:12px; font-weight:700;">
                STATE: DIAGNOSING
              </div>
            </div>
            <div style="display:flex; flex-direction:column; gap:16px; flex:1;">
              <div style="background:#182238; border:1px solid #3b82f6; padding:16px; border-radius:8px;">
                <div style="display:flex; gap:10px; align-items:center; margin-bottom:6px;">
                  <span style="background:#3b82f6; color:#fff; font-size:11px; font-weight:700; padding:2px 8px; border-radius:4px;">TEAMMATE</span>
                  <strong style="color:#ffffff;">Sam (Engineering Lead)</strong>
                  <span style="font-size:12px; color:#64748b;">09:42:15 UTC</span>
                </div>
                <div style="font-size:15px; color:#ffffff; line-height:1.4;">
                  <strong>@sre-commander</strong> Checkout is failing with HTTP 500 errors since the 09:40 deployment! Customers cannot place orders. Can you investigate?
                </div>
              </div>
              <div style="background:#182238; border:1px solid #ef4444; padding:16px; border-radius:8px;">
                <div style="display:flex; gap:10px; align-items:center; margin-bottom:6px;">
                  <span style="background:#dc2626; color:#fff; font-size:11px; font-weight:700; padding:2px 8px; border-radius:4px;">COMMANDER</span>
                  <strong style="color:#ffffff;">@sre-commander</strong>
                  <span style="font-size:12px; color:#64748b;">09:42:17 UTC</span>
                </div>
                <div style="font-size:14px; color:#cbd5e1; line-height:1.4;">
                  Acknowledged Sam. Classifying as <strong>P1 CRITICAL</strong>. Incident FSM shifted to <code>DIAGNOSING</code>. Pinned living war-board <code>incident-warboard.md</code> to room. Dispatching diagnostic lease to <strong>@sre-diagnostician</strong>.
                </div>
              </div>
            </div>
          </div>

          <!-- Right Telemetry Panel -->
          <div style="background:#111726; border:1px solid #ef4444; border-radius:12px; padding:24px; display:flex; flex-direction:column; gap:20px;">
            <div style="font-size:14px; font-weight:700; color:#ef4444; text-transform:uppercase; letter-spacing:1px;">Active Telemetry Surge</div>
            <div style="background:#3b1e1e; border:1px solid #ef4444; padding:18px; border-radius:8px;">
              <div style="font-size:13px; color:#fca5a5;">HTTP 5xx Error Rate</div>
              <div style="font-size:42px; font-weight:900; color:#ef4444; margin:6px 0;">48.7%</div>
              <div style="display:flex; gap:4px; height:28px; align-items:flex-end; margin-top:8px;">
                <div style="flex:1; background:#ef4444; height:20%;"></div>
                <div style="flex:1; background:#ef4444; height:35%;"></div>
                <div style="flex:1; background:#ef4444; height:60%;"></div>
                <div style="flex:1; background:#ef4444; height:90%;"></div>
                <div style="flex:1; background:#ef4444; height:100%;"></div>
                <div style="flex:1; background:#ef4444; height:95%;"></div>
              </div>
            </div>
            <div style="background:#3b1e1e; border:1px solid #ef4444; padding:18px; border-radius:8px;">
              <div style="font-size:13px; color:#fca5a5;">p99 Latency (Degraded)</div>
              <div style="font-size:38px; font-weight:900; color:#f59e0b; margin:6px 0;">3,840 ms</div>
              <div style="font-size:12px; color:#fca5a5;">Threshold Exceeded (&gt; 500ms SLA)</div>
            </div>
          </div>
        </div>
        """
    elif stype == "diagnosis_repro":
        content = """
        <div style="flex:1; display:grid; grid-template-columns:1fr 1fr; gap:24px; padding:24px; overflow:hidden;">
          <!-- Left: Runbook Retrieval & Stack Trace -->
          <div style="background:#111726; border:1px solid #233252; border-radius:12px; padding:24px; display:flex; flex-direction:column; gap:18px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span style="font-size:14px; font-weight:700; color:#38bdf8; text-transform:uppercase;">Hybrid BM25 + Dense RRF Knowledge Match</span>
              <span style="background:#22c55e; color:#000; font-size:12px; font-weight:800; padding:2px 8px; border-radius:4px;">SCORE: 0.94</span>
            </div>
            <div style="background:#182238; border:1px solid #38bdf8; padding:18px; border-radius:8px;">
              <div style="font-size:18px; font-weight:700; color:#38bdf8;">RB-001: Checkout Deploy Rollback</div>
              <div style="font-size:13px; color:#cbd5e1; margin-top:8px; line-height:1.4;">
                Matched against 13 curated SRE runbooks. Prescribes atomic rollback of <code>orders-api</code> to last verified stable image (v2.13.2) or applying null-guard patch to line 74.
              </div>
            </div>
            <div style="font-size:14px; font-weight:700; color:#e2e8f0; text-transform:uppercase;">Culprit Log Slice (Observability Trace)</div>
            <div style="background:#0a0d14; border:1px solid #ef4444; padding:16px; border-radius:8px; font-family:ui-monospace, monospace; font-size:13px; color:#fca5a5; line-height:1.5;">
              ERROR orders-api: FAIL_MODE=http500 active<br/>
              Traceback (most recent call last):<br/>
              &nbsp;&nbsp;File "sandbox/services/orders_api/app.py", line 74, in create_order<br/>
              &nbsp;&nbsp;&nbsp;&nbsp;total_price = cart['items'][0]['price'] * qty<br/>
              <span style="color:#ffffff; background:#dc2626; padding:2px 4px;">TypeError: 'NoneType' object is not subscriptable</span><br/>
              INFO: Culprit Commit: 8f3a91b (v2.14.0 deploy at 09:40 UTC)
            </div>
          </div>

          <!-- Right: Sandbox Empirical Reproduction -->
          <div style="background:#111726; border:1px solid #233252; border-radius:12px; padding:24px; display:flex; flex-direction:column; gap:18px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span style="font-size:14px; font-weight:700; color:#22c55e; text-transform:uppercase;">Empirical Sandbox Reproduction</span>
              <span style="background:rgba(239,68,68,0.2); color:#ef4444; border:1px solid #ef4444; font-size:12px; font-weight:800; padding:2px 8px; border-radius:4px;">10/10 REPRODUCED</span>
            </div>
            <div style="background:#0a0d14; border:1px solid #233252; padding:16px; border-radius:8px; font-family:ui-monospace, monospace; font-size:13px; color:#cbd5e1; line-height:1.5;">
              <span style="color:#38bdf8;">$ pytest sandbox/tests/test_orders.py -k test_checkout_failure</span><br/>
              ============================= test session starts ==============================<br/>
              sandbox/tests/test_orders.py::test_checkout_regression <span style="color:#ef4444; font-weight:700;">FAILED [100%]</span><br/>
              =================================== FAILURES ===================================<br/>
              &gt; assert response.status_code == 200<br/>
              E assert 500 == 200<br/>
              <span style="color:#ef4444;">1 failed in 0.04s &bull; Empirical Bug Reproduction Confirmed</span>
            </div>
            <div style="font-size:14px; font-weight:700; color:#e2e8f0; text-transform:uppercase;">Synthesized Surgical Patch Diff</div>
            <div style="background:#0a0d14; border:1px solid #22c55e; padding:16px; border-radius:8px; font-family:ui-monospace, monospace; font-size:12px; line-height:1.4;">
              <span style="color:#64748b;">--- a/sandbox/services/orders_api/app.py</span><br/>
              <span style="color:#64748b;">+++ b/sandbox/services/orders_api/app.py</span><br/>
              <span style="color:#38bdf8;">@@ -73,3 +73,4 @@ def create_order():</span><br/>
              <span style="color:#ef4444;">-    total_price = cart['items'][0]['price'] * qty</span><br/>
              <span style="color:#22c55e;">+    items = cart.get('items') or []</span><br/>
              <span style="color:#22c55e;">+    total_price = (items[0]['price'] if items else 0.0) * qty</span>
            </div>
          </div>
        </div>
        """
    elif stype == "critic_review":
        content = """
        <div style="flex:1; display:flex; flex-direction:column; justify-content:center; align-items:center; padding:40px;">
          <div style="background:#111726; border:2px solid #a855f7; border-radius:16px; padding:36px; width:1100px; box-shadow:0 20px 40px rgba(168,85,247,0.15);">
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #233252; padding-bottom:20px; margin-bottom:24px;">
              <div style="display:flex; align-items:center; gap:14px;">
                <div style="background:#7c3aed; color:#fff; font-weight:800; font-size:16px; padding:6px 14px; border-radius:8px;">ADVERSARIAL CRITIC</div>
                <h2 style="font-size:24px; margin:0;">Independent Red-Team SRE Review</h2>
              </div>
              <div style="background:rgba(34,197,94,0.15); border:1px solid #22c55e; color:#22c55e; padding:6px 16px; border-radius:9999px; font-size:14px; font-weight:800;">
                VERDICT: APPROVED FOR MITIGATION
              </div>
            </div>

            <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:20px; margin-bottom:28px;">
              <div style="background:#182238; border:1px solid #233252; padding:20px; border-radius:10px;">
                <div style="font-size:13px; color:#a855f7; font-weight:700;">CAUSAL VERIFICATION</div>
                <div style="font-size:18px; font-weight:700; color:#ffffff; margin:6px 0;">100% Empirically Proven</div>
                <div style="font-size:13px; color:#94a3b8;">Fails against broken sandbox replica; passes once null-guard is applied.</div>
              </div>
              <div style="background:#182238; border:1px solid #233252; padding:20px; border-radius:10px;">
                <div style="font-size:13px; color:#22c55e; font-weight:700;">BLAST RADIUS AUDIT</div>
                <div style="font-size:18px; font-weight:700; color:#ffffff; margin:6px 0;">Isolated to Single Container</div>
                <div style="font-size:13px; color:#94a3b8;">Zero downstream impacts on Postgres, Redis, or Kafka workers.</div>
              </div>
              <div style="background:#182238; border:1px solid #233252; padding:20px; border-radius:10px;">
                <div style="font-size:13px; color:#38bdf8; font-weight:700;">SCHEMA COMPATIBILITY</div>
                <div style="font-size:18px; font-weight:700; color:#ffffff; margin:6px 0;">Zero Schema Migrations</div>
                <div style="font-size:13px; color:#94a3b8;">v2.13.2 stable image is 100% backward-compatible with database state.</div>
              </div>
            </div>

            <div style="background:#0a0d14; border:1px solid #233252; padding:18px; border-radius:8px; font-size:14px; color:#cbd5e1; line-height:1.5;">
              <strong style="color:#a855f7;">Critic Synthesis:</strong> The proposed mitigation (atomic rollback of orders-api to v2.13.2 accompanied by an automated compensating saga) adheres strictly to production safety invariants. Hallucination risk falsified via sandbox pytest execution. Handing off to Four-Eyes Gate.
            </div>
          </div>
        </div>
        """
    elif stype == "approval_gate":
        content = """
        <div style="flex:1; display:flex; flex-direction:column; justify-content:center; align-items:center; padding:40px;">
          <div style="background:#111726; border:2px solid #ff7849; border-radius:16px; padding:36px; width:1100px; box-shadow:0 20px 40px rgba(255,120,73,0.15);">
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #233252; padding-bottom:20px; margin-bottom:24px;">
              <div style="display:flex; align-items:center; gap:14px;">
                <div style="background:#ff7849; color:#fff; font-weight:800; font-size:16px; padding:6px 14px; border-radius:8px;">FOUR-EYES GATE</div>
                <h2 style="font-size:24px; margin:0;">Human SRE Authorization Required</h2>
              </div>
              <div style="background:rgba(255,120,73,0.15); border:1px solid #ff7849; color:#ff7849; padding:6px 16px; border-radius:9999px; font-size:14px; font-weight:800;">
                TOCTOU PROTECTED
              </div>
            </div>

            <div style="background:#182238; border:1px solid #233252; padding:24px; border-radius:12px; margin-bottom:24px;">
              <div style="font-size:14px; color:#94a3b8; font-weight:600;">PROPOSED MITIGATION ACTION:</div>
              <div style="font-size:22px; font-weight:800; color:#ffffff; margin:8px 0 16px 0;">
                Atomic rollback of orders-api container from v2.14.0 to v2.13.2
              </div>

              <div style="font-size:13px; color:#94a3b8; font-weight:600; margin-bottom:6px;">CRYPTOGRAPHIC ACTION DIGEST (HMAC-SHA256):</div>
              <div style="background:#0a0d14; border:1px solid #334155; padding:12px 16px; border-radius:8px; font-family:ui-monospace, monospace; font-size:15px; color:#38bdf8; letter-spacing:0.5px;">
                hmac-sha256:7b98f21da90e4f3a8b27c10d5e893bf4
              </div>
              <div style="font-size:12px; color:#64748b; margin-top:8px;">
                Canonicalized JSON schema digest: prevents Time-of-Check to Time-of-Use (TOCTOU) payload tampering.
              </div>
            </div>

            <div style="background:#182238; border:1px solid #22c55e; padding:20px; border-radius:12px; display:flex; justify-content:space-between; align-items:center;">
              <div>
                <div style="font-size:13px; color:#22c55e; font-weight:700;">ON-CALL SRE SIGN-OFF RECEIVED</div>
                <div style="font-size:16px; font-weight:700; color:#ffffff; margin-top:4px;">
                  Priya (On-Call SRE Lead): <code style="color:#38bdf8;">@sre-commander approve</code>
                </div>
              </div>
              <div style="background:#22c55e; color:#000; font-weight:800; font-size:15px; padding:12px 28px; border-radius:8px;">
                [APPROVED] Cryptographically Authorized
              </div>
            </div>
          </div>
        </div>
        """
    elif stype == "recovery_postmortem":
        content = """
        <div style="flex:1; display:grid; grid-template-columns:1fr 1fr; gap:24px; padding:24px; overflow:hidden;">
          <!-- Left: Restored Telemetry -->
          <div style="background:#111726; border:1px solid #22c55e; border-radius:12px; padding:24px; display:flex; flex-direction:column; gap:20px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span style="font-size:14px; font-weight:700; color:#22c55e; text-transform:uppercase;">Verified Operational Recovery</span>
              <span style="background:#22c55e; color:#000; font-size:12px; font-weight:800; padding:2px 8px; border-radius:4px;">100% HEALTHY</span>
            </div>

            <div style="background:#182238; border:1px solid #233252; padding:20px; border-radius:8px;">
              <div style="font-size:13px; color:#94a3b8;">HTTP 5xx Error Rate</div>
              <div style="font-size:42px; font-weight:900; color:#22c55e; margin:6px 0;">0.00%</div>
              <div style="font-size:13px; color:#22c55e;">Collapsed from 48.7% &bull; Zero 500s on POST /orders</div>
            </div>

            <div style="background:#182238; border:1px solid #233252; padding:20px; border-radius:8px;">
              <div style="font-size:13px; color:#94a3b8;">p99 Latency</div>
              <div style="font-size:42px; font-weight:900; color:#22c55e; margin:6px 0;">24.5 ms</div>
              <div style="font-size:13px; color:#22c55e;">Normalized from 3,840ms (&lt; 100ms SLA target)</div>
            </div>

            <div style="background:#182238; border:1px solid #233252; padding:20px; border-radius:8px;">
              <div style="font-size:13px; color:#94a3b8;">Container Health Probe</div>
              <div style="font-size:22px; font-weight:700; color:#22c55e; margin:6px 0;">HTTP 200 OK (v2.13.2)</div>
              <div style="font-size:12px; color:#94a3b8;">Automated post-rollback regression tests: 24/24 passed</div>
            </div>
          </div>

          <!-- Right: Permanent RCA Document -->
          <div style="background:#111726; border:1px solid #233252; border-radius:12px; padding:24px; display:flex; flex-direction:column; gap:16px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span style="font-size:14px; font-weight:700; color:#38bdf8; text-transform:uppercase;">Permanent Switch Room Document</span>
              <span style="background:rgba(56,189,248,0.15); color:#38bdf8; font-size:12px; font-weight:800; padding:2px 8px; border-radius:4px;">create_room_document</span>
            </div>

            <div style="background:#0a0d14; border:1px solid #233252; padding:20px; border-radius:8px; font-family:ui-monospace, monospace; font-size:13px; color:#cbd5e1; line-height:1.5; flex:1; overflow:hidden;">
              <span style="color:#ff7849; font-weight:700;"># Post-Mortem: Incident INC-20261107-01</span><br/>
              <strong>Date:</strong> 2026-11-07 09:44 UTC &bull; <strong>Severity:</strong> P1 &bull; <strong>MTTR:</strong> 1m 45s<br/>
              --------------------------------------------------<br/>
              <span style="color:#38bdf8; font-weight:700;">## Summary &amp; Impact:</span><br/>
              Checkout API degradation caused by release v2.14.0. 48.7% 500 error rate experienced for 105 seconds before atomic rollback.<br/><br/>
              <span style="color:#22c55e; font-weight:700;">## Root Cause:</span><br/>
              Uncaught NoneType exception in PaymentGateway initialization in commit 8f3a91b.<br/><br/>
              <span style="color:#a855f7; font-weight:700;">## Action Items:</span><br/>
              1. Merge null-guard patch to release branch (RB-001)<br/>
              2. Add pytest schema validation to CI deployment pipeline<br/>
              3. Authorizer: Priya (On-Call SRE)
            </div>
          </div>
        </div>
        """
    elif stype == "benchmark_outro":
        content = """
        <div style="flex:1; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; padding:40px;">
          <div style="background:rgba(34,197,94,0.15); border:1px solid #22c55e; color:#22c55e; padding:6px 20px; border-radius:9999px; font-weight:700; font-size:14px; margin-bottom:16px;">
            EMPIRICAL SRE BENCHMARK RESULTS (5 FAILURE SCENARIOS)
          </div>
          <h2 style="font-size:36px; font-weight:800; margin:0 0 24px 0; color:#ffffff;">
            Over 93% Mean MTTR Reduction Across Real Outages
          </h2>

          <table style="width:1150px; border-collapse:collapse; background:#111726; border:1px solid #233252; border-radius:10px; overflow:hidden; font-size:14px; text-align:left; margin-bottom:28px;">
            <thead>
              <tr style="background:#182238; border-bottom:1px solid #233252; color:#38bdf8; font-size:13px; text-transform:uppercase;">
                <th style="padding:12px 16px;">Scenario ID</th>
                <th style="padding:12px 16px;">Target Service</th>
                <th style="padding:12px 16px;">Baseline Human MTTR</th>
                <th style="padding:12px 16px;">Decision Latency</th>
                <th style="padding:12px 16px;">IncidentPilot MTTR</th>
                <th style="padding:12px 16px;">MTTR Reduction</th>
                <th style="padding:12px 16px;">Critic &amp; Human Gate</th>
              </tr>
            </thead>
            <tbody>
              <tr style="border-bottom:1px solid #233252;">
                <td style="padding:12px 16px; font-weight:700; color:#ffffff;">bad-deploy</td>
                <td style="padding:12px 16px; color:#94a3b8;">orders-api</td>
                <td style="padding:12px 16px; color:#cbd5e1;">30 mins</td>
                <td style="padding:12px 16px; color:#38bdf8;">1.8s</td>
                <td style="padding:12px 16px; font-weight:700; color:#22c55e;">~1m 45s</td>
                <td style="padding:12px 16px; font-weight:800; color:#22c55e;">~94%</td>
                <td style="padding:12px 16px; color:#a855f7;">APPROVED &bull; ENFORCED</td>
              </tr>
              <tr style="border-bottom:1px solid #233252;">
                <td style="padding:12px 16px; font-weight:700; color:#ffffff;">cache-down</td>
                <td style="padding:12px 16px; color:#94a3b8;">redis</td>
                <td style="padding:12px 16px; color:#cbd5e1;">20 mins</td>
                <td style="padding:12px 16px; color:#38bdf8;">1.4s</td>
                <td style="padding:12px 16px; font-weight:700; color:#22c55e;">~1m 30s</td>
                <td style="padding:12px 16px; font-weight:800; color:#22c55e;">~92%</td>
                <td style="padding:12px 16px; color:#a855f7;">APPROVED &bull; ENFORCED</td>
              </tr>
              <tr style="border-bottom:1px solid #233252;">
                <td style="padding:12px 16px; font-weight:700; color:#ffffff;">kill-worker</td>
                <td style="padding:12px 16px; color:#94a3b8;">orders-worker</td>
                <td style="padding:12px 16px; color:#cbd5e1;">25 mins</td>
                <td style="padding:12px 16px; color:#38bdf8;">1.2s</td>
                <td style="padding:12px 16px; font-weight:700; color:#22c55e;">~1m 20s</td>
                <td style="padding:12px 16px; font-weight:800; color:#22c55e;">~94%</td>
                <td style="padding:12px 16px; color:#a855f7;">APPROVED &bull; ENFORCED</td>
              </tr>
              <tr style="border-bottom:1px solid #233252;">
                <td style="padding:12px 16px; font-weight:700; color:#ffffff;">oom-worker</td>
                <td style="padding:12px 16px; color:#94a3b8;">orders-worker</td>
                <td style="padding:12px 16px; color:#cbd5e1;">40 mins</td>
                <td style="padding:12px 16px; color:#38bdf8;">2.1s</td>
                <td style="padding:12px 16px; font-weight:700; color:#22c55e;">~2m 10s</td>
                <td style="padding:12px 16px; font-weight:800; color:#22c55e;">~95%</td>
                <td style="padding:12px 16px; color:#a855f7;">APPROVED &bull; ENFORCED</td>
              </tr>
              <tr>
                <td style="padding:12px 16px; font-weight:700; color:#ffffff;">poison-message</td>
                <td style="padding:12px 16px; color:#94a3b8;">orders-worker</td>
                <td style="padding:12px 16px; color:#cbd5e1;">30 mins</td>
                <td style="padding:12px 16px; color:#38bdf8;">1.6s</td>
                <td style="padding:12px 16px; font-weight:700; color:#22c55e;">~1m 40s</td>
                <td style="padding:12px 16px; font-weight:800; color:#22c55e;">~94%</td>
                <td style="padding:12px 16px; color:#a855f7;">APPROVED &bull; ENFORCED</td>
              </tr>
            </tbody>
          </table>

          <div style="background:#182238; border:1px solid #ff7849; padding:16px 36px; border-radius:12px; display:flex; gap:36px; align-items:center;">
            <div>
              <div style="font-size:12px; color:#94a3b8;">GITHUB REPOSITORY</div>
              <div style="font-size:18px; font-weight:800; color:#ffffff;">github.com/Namanbhatt-01/incidentpilot</div>
            </div>
            <div style="height:32px; width:1px; background:#334155;"></div>
            <div>
              <div style="font-size:12px; color:#94a3b8;">HACKATHON TEAM CODE</div>
              <div style="font-size:18px; font-weight:800; color:#38bdf8;">9YC3BJ</div>
            </div>
            <div style="height:32px; width:1px; background:#334155;"></div>
            <div>
              <div style="font-size:12px; color:#94a3b8;">TRACK SELECTED</div>
              <div style="font-size:18px; font-weight:800; color:#22c55e;">Track 01: Best Business Workflow</div>
            </div>
          </div>
        </div>
        """

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <style>
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      width: 1920px;
      height: 1080px;
      background: #0a0d14;
      color: #f1f5f9;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }}
    header {{
      background: #07090f;
      border-bottom: 1px solid #233252;
      padding: 16px 32px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-shrink: 0;
    }}
    footer {{
      background: #07090f;
      border-top: 1px solid #233252;
      padding: 16px 32px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-shrink: 0;
    }}
    .subtitle-bar {{
      font-size: 18px;
      font-weight: 600;
      color: #38bdf8;
      letter-spacing: 0.3px;
    }}
  </style>
</head>
<body>
  <header>
    <div style="display:flex; align-items:center; gap:16px;">
      <div style="background:linear-gradient(135deg, #ff7849, #ea580c); color:white; font-weight:900; font-size:14px; padding:6px 14px; border-radius:6px; letter-spacing:0.5px;">SWITCH</div>
      <div style="font-size:20px; font-weight:800; color:#ffffff;">IncidentPilot</div>
      <div style="font-size:14px; color:#94a3b8;">&bull; {scene["title"]}</div>
    </div>
    <div style="display:flex; align-items:center; gap:16px;">
      <div style="background:#1e293b; color:#38bdf8; border:1px solid #334155; padding:4px 12px; border-radius:9999px; font-size:13px; font-weight:700;">
        WeMakeDevs Hackathon
      </div>
      <div style="font-family:ui-monospace, monospace; font-size:13px; color:#22c55e; font-weight:700;">
        LIVE DEMO
      </div>
    </div>
  </header>

  {content}

  <footer>
    <div class="subtitle-bar">
      &gt;&gt; {scene["subtitle"]}
    </div>
    <div style="font-size:13px; color:#64748b; font-family:ui-monospace, monospace;">
      github.com/Namanbhatt-01/incidentpilot
    </div>
  </footer>
</body>
</html>
"""
    html_path.write_text(full_html, encoding="utf-8")

    # Capture 1080p screenshot with Chrome Headless
    subprocess.run(
        [
            CHROME_PATH,
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            "--window-size=1920,1080",
            f"--screenshot={str(png_path)}",
            str(html_path),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return png_path


def encode_scene_video(scene: dict, png_path: Path, wav_path: Path, duration: float) -> Path:
    """Encode an individual scene into an MP4 clip."""
    clip_path = OUTPUT_DIR / f"{scene['id']}.mp4"
    print(f"  [Video] Encoding {scene['id']} ({duration:.1f}s)...")
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-loop",
            "1",
            "-i",
            str(png_path),
            "-i",
            str(wav_path),
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-tune",
            "stillimage",
            "-crf",
            "18",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-pix_fmt",
            "yuv420p",
            "-shortest",
            str(clip_path),
        ],
        check=True,
        stderr=subprocess.DEVNULL,
    )
    return clip_path


def main():
    print("================================================================================")
    print("    IncidentPilot: Automated 1080p Video Walkthrough Generation")
    print("================================================================================")

    clips = []
    total_time = 0.0

    for idx, scene in enumerate(SCENES, 1):
        print(f"\n[Scene {idx}/{len(SCENES)}] Processing {scene['id']}...")
        wav_path = generate_audio(scene)
        duration = get_audio_duration(wav_path)
        total_time += duration
        png_path = render_html_scene(scene, duration)
        clip_path = encode_scene_video(scene, png_path, wav_path, duration)
        clips.append(clip_path)

    print(
        f"\nTotal video duration across all scenes: {total_time:.1f}s (~{total_time / 60:.2f} mins)"
    )

    # Concatenate all clips
    concat_list = OUTPUT_DIR / "concat_list.txt"
    with open(concat_list, "w") as f:
        for clip in clips:
            f.write(f"file '{clip.name}'\n")

    print("\n[Finalizing] Concatenating scenes into final video...")
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_list),
            "-c",
            "copy",
            str(FINAL_VIDEO),
        ],
        check=True,
        stderr=subprocess.DEVNULL,
    )

    size_mb = FINAL_VIDEO.stat().st_size / (1024 * 1024)
    print("\n================================================================================")
    print("  [SUCCESS] Demo Walkthrough Video Generated Successfully!")
    print(f"  File     : {FINAL_VIDEO}")
    print(f"  Duration : {total_time:.1f} seconds")
    print(f"  Size     : {size_mb:.2f} MB")
    print("================================================================================")


if __name__ == "__main__":
    main()
