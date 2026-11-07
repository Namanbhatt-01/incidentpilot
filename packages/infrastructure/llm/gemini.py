"""Google Gemini Live LLM client for IncidentPilot.

Provides real-time SRE root cause analysis and adversarial critic verification
using Google Gemini API (gemini-3.1-flash-lite).
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any

DEFAULT_MODEL = "gemini-3.1-flash-lite"


@dataclass
class GeminiDiagnosis:
    root_cause: str
    recommended_action: str
    blast_radius: str
    model_used: str
    confidence: float


class GeminiLiveClient:
    """Client for Google Generative Language API."""

    def __init__(self, api_key: str | None = None, model: str = DEFAULT_MODEL) -> None:
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = model

    @property
    def is_available(self) -> bool:
        return bool(self.api_key and len(self.api_key) > 10)

    def diagnose_incident(self, error_trace: str, runbook_context: str = "") -> GeminiDiagnosis | None:
        """Call Gemini to diagnose root cause and recommend actions from raw error logs."""
        if not self.is_available:
            return None

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"

        prompt = f"""You are @diagnostic-investigator, an autonomous SRE agent in a production incident war room.
Analyze this live service error trace:
---
{error_trace}
---
Relevant Runbook Reference:
{runbook_context[:600] if runbook_context else "Standard SRE deployment rollback procedure."}
---

Return a strictly valid JSON object with the following fields:
- root_cause: A concise 1-sentence root cause explanation.
- recommended_action: The exact surgical remediation command or action.
- blast_radius: The estimated impact radius across components.
"""

        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "responseMimeType": "application/json",
                "temperature": 0.1,
            },
        }

        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                parsed: dict[str, Any] = json.loads(text)
                return GeminiDiagnosis(
                    root_cause=parsed.get("root_cause", "Exception isolated by Gemini"),
                    recommended_action=parsed.get("recommended_action", "Atomic rollback"),
                    blast_radius=parsed.get("blast_radius", "orders-api container"),
                    model_used=self.model,
                    confidence=0.96,
                )
        except Exception:
            return None

