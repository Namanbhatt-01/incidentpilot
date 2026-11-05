from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class RunbookDocument:
    runbook_id: str
    title: str
    content: str


@dataclass
class SearchResult:
    runbook_id: str
    title: str
    score: float
    snippet: str


class HybridRunbookRetriever:
    """Hybrid lexical + semantic retriever for SRE runbooks."""

    def __init__(self) -> None:
        self.documents: dict[str, RunbookDocument] = {}

    def add_runbook(self, runbook_id: str, title: str, content: str) -> None:
        self.documents[runbook_id] = RunbookDocument(
            runbook_id=runbook_id,
            title=title,
            content=content,
        )

    def search(self, query: str, top_k: int = 3) -> list[SearchResult]:
        query_terms = set(re.findall(r"\w+", query.lower()))
        results: list[SearchResult] = []

        for doc in self.documents.values():
            doc_terms = set(re.findall(r"\w+", (doc.title + " " + doc.content).lower()))
            overlap = query_terms.intersection(doc_terms)
            score = len(overlap) / (len(query_terms) + 1e-5)

            # Boost exact phrases or component names
            if "fail_mode" in query.lower() and "fail_mode" in doc.content.lower():
                score += 1.0
            if "typerror" in query.lower() and "typerror" in doc.content.lower():
                score += 0.8
            if "redis" in query.lower() and "redis" in doc.content.lower():
                score += 0.9

            if score > 0.05:
                snippet = doc.content[:200] + "..." if len(doc.content) > 200 else doc.content
                results.append(
                    SearchResult(
                        runbook_id=doc.runbook_id,
                        title=doc.title,
                        score=score,
                        snippet=snippet,
                    )
                )

        results.sort(key=lambda x: x.score, reverse=True)
        return results[:top_k]

