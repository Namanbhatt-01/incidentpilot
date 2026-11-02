from __future__ import annotations

import hashlib
from dataclasses import dataclass


@dataclass(frozen=True)
class ActionDigest:
    """Computes deterministic cryptographic hash to defend against TOCTOU mutations."""

    action_type: str
    target_component: str
    patch_diff: str
    timestamp: float

    def compute_sha256(self) -> str:
        payload = f"{self.action_type}:{self.target_component}:{self.patch_diff}:{self.timestamp}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def short_hash(self) -> str:
        return f"sha:{self.compute_sha256()[:8]}"
