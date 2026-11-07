from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field


@dataclass
class TraceSpan:
    name: str
    trace_id: str
    span_id: str
    parent_span_id: str | None = None
    start_time: float = field(default_factory=time.time)
    end_time: float | None = None
    attributes: dict[str, str] = field(default_factory=dict)

    def finish(self) -> None:
        self.end_time = time.time()


class IncidentTracer:
    """W3C TraceContext compliant span collector for incident investigations."""

    def __init__(self, service_name: str = "incidentpilot") -> None:
        self.service_name = service_name
        self.spans: list[TraceSpan] = []

    def start_span(
        self, name: str, trace_id: str | None = None, parent_span_id: str | None = None
    ) -> TraceSpan:
        t_id = trace_id or uuid.uuid4().hex
        s_id = uuid.uuid4().hex[:16]
        span = TraceSpan(
            name=name,
            trace_id=t_id,
            span_id=s_id,
            parent_span_id=parent_span_id,
            attributes={"service.name": self.service_name},
        )
        self.spans.append(span)
        return span
