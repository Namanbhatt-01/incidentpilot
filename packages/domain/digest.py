from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass


@dataclass(frozen=True)
class ActionDigest:
    """Computes deterministic cryptographic hash to defend against TOCTOU mutations."""

    action_type: str
    target_component: str
    patch_diff: str
    timestamp: float

    def compute_sha256(self) -> str:
        # Use canonical sorted JSON serialization to prevent delimiter collisions
        payload = json.dumps(
            {
                "action_type": self.action_type,
                "target_component": self.target_component,
                "patch_diff": self.patch_diff,
                "timestamp": self.timestamp,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def short_hash(self) -> str:
        return f"sha:{self.compute_sha256()[:8]}"
