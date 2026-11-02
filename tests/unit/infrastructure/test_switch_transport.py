from __future__ import annotations

from packages.infrastructure.switch.transport import SwitchEventEnvelope


def test_switch_event_envelope_parsing() -> None:
    raw_sse_data = {
        "type": "message",
        "room_id": "sre-incident-war-room",
        "sequence": 4813,
        "payload": {
            "addressed": True,
            "sender": "@sam:switch.local",
            "sender_name": "Sam",
            "body": "@sre-commander Checkout is returning 500s",
            "timestamp": 1700000000000,
        },
    }
    envelope = SwitchEventEnvelope.from_dict(raw_sse_data)
    assert envelope.type == "message"
    assert envelope.sequence == 4813
    assert envelope.room_id == "sre-incident-war-room"
    assert envelope.is_addressed is True
    assert "@sre-commander" in envelope.body


def test_switch_control_frame_detection() -> None:
    gap_frame = {
        "type": "gap",
        "room_id": "sre-incident-war-room",
        "from_sequence": 4800,
        "resumed_at": 4810,
        "reason": "buffer_overflow",
    }
    envelope = SwitchEventEnvelope.from_dict(gap_frame)
    assert envelope.is_control_frame is True
    assert envelope.type == "gap"
