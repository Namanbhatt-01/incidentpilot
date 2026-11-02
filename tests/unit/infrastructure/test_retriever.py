from __future__ import annotations

from packages.infrastructure.knowledge.retriever import HybridRunbookRetriever


def test_hybrid_retriever_exact_keyword_and_semantic_matching() -> None:
    retriever = HybridRunbookRetriever()
    retriever.add_runbook(
        runbook_id="RB-001-orders-api-500.md",
        title="Orders API 500 Internal Server Error",
        content="When FAIL_MODE=http500 is active in orders-api, price_rule returns None causing TypeError in checkout calculation.",
    )
    retriever.add_runbook(
        runbook_id="RB-003-redis-cache-down.md",
        title="Redis Cache Eviction & Connection Starvation",
        content="When Redis container stops, price lookups fall through to Postgres, causing connection pool exhaustion.",
    )

    # Query matching exact error
    results = retriever.search("FAIL_MODE=http500 orders-api TypeError")
    assert len(results) > 0
    assert results[0].runbook_id == "RB-001-orders-api-500.md"
    assert results[0].score > 0.0
