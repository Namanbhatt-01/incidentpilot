from __future__ import annotations

from packages.domain.digest import ActionDigest


def test_action_digest_deterministic_hash() -> None:
    digest1 = ActionDigest(
        action_type="apply_patch",
        target_component="orders-api",
        patch_diff="--- a/app.py\n+++ b/app.py\n@@ -1 +1 @@",
        timestamp=1700000000.0,
    )
    digest2 = ActionDigest(
        action_type="apply_patch",
        target_component="orders-api",
        patch_diff="--- a/app.py\n+++ b/app.py\n@@ -1 +1 @@",
        timestamp=1700000000.0,
    )
    assert digest1.compute_sha256() == digest2.compute_sha256()
    assert digest1.short_hash() == digest2.short_hash()
    assert digest1.short_hash().startswith("sha:")


def test_action_digest_mutation_detection_toctou() -> None:
    original = ActionDigest(
        action_type="apply_patch",
        target_component="orders-api",
        patch_diff="safe diff",
        timestamp=1700000000.0,
    )
    tampered = ActionDigest(
        action_type="apply_patch",
        target_component="orders-api",
        patch_diff="malicious altered diff",
        timestamp=1700000000.0,
    )
    assert original.compute_sha256() != tampered.compute_sha256()
