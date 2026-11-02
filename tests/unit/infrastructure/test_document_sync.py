from __future__ import annotations

from packages.domain.entities import IncidentAggregate, SeverityLevel
from packages.domain.events import IncidentState
from packages.infrastructure.switch.document_sync import RoomDocumentSync


def test_room_document_formatting() -> None:
    sync = RoomDocumentSync()
    incident = IncidentAggregate(
        incident_id="inc-777",
        title="Incident INC-777: Checkout failing",
        reported_by="@sam",
        severity=SeverityLevel.P1,
    )
    incident.fsm.transition_to(IncidentState.TRIAGED)
    doc_content = sync.render_warboard_document(incident)
    assert "# INCIDENT WAR-BOARD: INC-777" in doc_content
    assert "P1" in doc_content
    assert "TRIAGED" in doc_content
    assert "@sam" in doc_content
