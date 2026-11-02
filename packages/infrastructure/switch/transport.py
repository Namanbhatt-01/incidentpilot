from __future__ import annotations

import asyncio
import contextlib
import json
import logging
import uuid
from collections.abc import AsyncGenerator
from dataclasses import dataclass, field
from typing import Any, cast

import httpx

log = logging.getLogger("incidentpilot.switch.transport")


@dataclass
class SwitchEventEnvelope:
    type: str
    room_id: str
    sequence: int = 0
    bridge_id: str | None = None
    payload: dict[str, Any] = field(default_factory=dict)
    is_control_frame: bool = False

    @property
    def is_addressed(self) -> bool:
        return bool(self.payload.get("addressed", False))

    @property
    def body(self) -> str:
        return str(self.payload.get("body", ""))

    @property
    def sender(self) -> str:
        return str(self.payload.get("sender", ""))

    @property
    def sender_name(self) -> str:
        return str(self.payload.get("sender_name", ""))

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SwitchEventEnvelope:
        event_type = data.get("type", "unknown")
        control_frame_types = {
            "connection_state",
            "gap",
            "evicted",
            "subscription_changed",
            "room_released",
        }
        is_ctrl = event_type in control_frame_types
        return cls(
            type=event_type,
            room_id=data.get("room_id", ""),
            sequence=data.get("sequence", 0),
            bridge_id=data.get("bridge_id"),
            payload=data.get("payload", {}) if not is_ctrl else data,
            is_control_frame=is_ctrl,
        )


class SwitchTransport:
    """Wire client implementing Switch Agent Protocol (SSE down, HTTP ops up, 2s heartbeat)."""

    def __init__(self, bridge_url: str, agent_id: str, api_key: str) -> None:
        self.bridge_url = bridge_url.rstrip("/")
        self.agent_id = agent_id
        self.api_key = api_key
        self.connection_id = str(uuid.uuid4())
        self.cursor = 0
        self.is_connected = False
        self._running = False
        self._heartbeat_task: asyncio.Task[None] | None = None

    @property
    def headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-Switch-Connection-Id": self.connection_id,
        }

    async def _heartbeat_loop(self) -> None:
        """Beats every 2 seconds to retain room claims and connection liveness (6s server TTL)."""
        async with httpx.AsyncClient(base_url=self.bridge_url) as client:
            while self._running:
                try:
                    res = await client.post(
                        f"/agents/{self.agent_id}/connection/beat",
                        headers=self.headers,
                        json={"connection_id": self.connection_id, "cursor": self.cursor},
                        timeout=5.0,
                    )
                    if res.status_code == 200:
                        data = res.json()
                        self.cursor = data.get("cursor", self.cursor)
                    elif res.status_code in (404, 409):
                        log.warning(
                            "Heartbeat rejected with status %d; stream reconnection required",
                            res.status_code,
                        )
                except Exception as e:
                    log.warning("Heartbeat tick failed: %s", e)
                await asyncio.sleep(2.0)

    async def connect(self, rooms: list[str]) -> AsyncGenerator[SwitchEventEnvelope, None]:
        """Opens SSE event stream, launches heartbeat task, and yields parsed event envelopes."""
        self._running = True
        self._heartbeat_task = asyncio.create_task(self._heartbeat_loop())

        url = f"{self.bridge_url}/agents/{self.agent_id}/events"
        params = {
            "connection_id": self.connection_id,
            "scope": "all",
            "filter": "all",
            "rooms": ",".join(rooms),
        }

        async with (
            httpx.AsyncClient(timeout=None) as client,
            client.stream("GET", url, headers=self.headers, params=params) as response,
        ):
            self.is_connected = True
            async for line in response.aiter_lines():
                if not line:
                    continue
                if line.startswith("id: "):
                    with contextlib.suppress(ValueError):
                        self.cursor = int(line[4:])
                elif line.startswith("data: "):
                    try:
                        raw_data = json.loads(line[6:])
                        envelope = SwitchEventEnvelope.from_dict(raw_data)
                        yield envelope
                    except json.JSONDecodeError:
                        log.warning("Malformed SSE JSON line: %s", line)

    async def disconnect(self) -> None:
        self._running = False
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._heartbeat_task
        self.is_connected = False

    async def invoke_op(self, operation: str, **kwargs: Any) -> dict[str, Any]:
        """Calls POST /agents/{agent_id}/ops/{operation} with unnested arguments."""
        async with httpx.AsyncClient(base_url=self.bridge_url) as client:
            res = await client.post(
                f"/agents/{self.agent_id}/ops/{operation}",
                headers=self.headers,
                json=kwargs,
                timeout=10.0,
            )
            return cast(dict[str, Any], res.json())

    async def post_message(
        self, room_id: str, body: str, thread_id: str | None = None
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {"room_id": room_id, "body": body}
        if thread_id:
            payload["thread_id"] = thread_id
        return await self.invoke_op("post_message", **payload)

    async def create_room_document(
        self, room_id: str, name: str, content: str, instructions: str = ""
    ) -> dict[str, Any]:
        return await self.invoke_op(
            "create_room_document",
            room_id=room_id,
            name=name,
            content=content,
            instructions=instructions,
        )

    async def update_room_document(self, room_id: str, name: str, content: str) -> dict[str, Any]:
        return await self.invoke_op(
            "update_room_document",
            room_id=room_id,
            name=name,
            content=content,
        )
