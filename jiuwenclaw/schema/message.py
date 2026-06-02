"""Universal message envelope for JiuwenClaw.

Three message types::

    req     Client → Agent request ("do something")
    res     Agent → Client response ("here's the result")
    event   Agent → Client push ("something happened")
"""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ReqMethod(Enum):
    """Actions a client can request."""

    CHAT_SEND = "chat.send"
    CHAT_CANCEL = "chat.cancel"
    CHAT_RESUME = "chat.resume"
    SESSION_CREATE = "session.create"
    SESSION_DELETE = "session.delete"
    SESSION_LIST = "session.list"


class EventType(Enum):
    """Events the agent can push to clients."""

    CHAT_DELTA = "chat.delta"
    CHAT_FINAL = "chat.final"
    TASK_START = "task.start"
    TASK_COMPLETE = "task.complete"
    CONNECTION_ACK = "connection.ack"


class Mode(Enum):
    """Agent execution mode."""

    AGENT_PLAN = "agent_plan"
    AGENT_EXEC = "agent_exec"

    @classmethod
    def from_raw(cls, raw: Any, default: Mode | None = None) -> Mode:
        """Parse a raw value into a Mode, with fallback."""
        if isinstance(raw, Mode):
            return raw
        if isinstance(raw, str):
            for mode in cls:
                if mode.value == raw.lower().strip():
                    return mode
        return default or cls.AGENT_PLAN


@dataclass
class Message:
    """Universal message envelope.

    Every interaction in JiuwenClaw flows through a Message. Channels
    translate their native formats into Messages; the Gateway routes
    them; the Agent processes them.
    """

    id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    type: str = "req"
    channel_id: str = ""
    session_id: str = ""
    params: dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    ok: bool = True
    req_method: ReqMethod | None = None
    mode: Mode = Mode.AGENT_PLAN
    is_stream: bool = False
    stream_seq: int = 0
    stream_id: str = ""
    payload: Any = None
    event_type: EventType | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    # ── serialization ──────────────────────────────────────────

    def to_dict(self) -> dict[str, Any]:
        """Convert to a JSON-serializable dictionary."""
        result: dict[str, Any] = {
            "id": self.id,
            "type": self.type,
            "channel_id": self.channel_id,
            "session_id": self.session_id,
            "params": self.params,
            "timestamp": self.timestamp,
            "ok": self.ok,
            "mode": self.mode.value,
            "is_stream": self.is_stream,
        }
        if self.req_method is not None:
            result["method"] = self.req_method.value
        if self.event_type is not None:
            result["event"] = self.event_type.value
        if self.stream_seq:
            result["stream_seq"] = self.stream_seq
        if self.stream_id:
            result["stream_id"] = self.stream_id
        if self.payload is not None:
            result["payload"] = self.payload
        if self.metadata:
            result["metadata"] = self.metadata
        return result

    def to_json(self) -> str:
        """Serialize to a JSON string."""
        return json.dumps(self.to_dict(), ensure_ascii=False)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Message:
        """Deserialize from a dictionary."""
        # Parse req_method from "method" field
        req_method = None
        method_raw = data.get("method")
        if method_raw:
            for rm in ReqMethod:
                if rm.value == method_raw:
                    req_method = rm
                    break

        # Parse event_type from "event" field
        event_type = None
        event_raw = data.get("event")
        if event_raw:
            for et in EventType:
                if et.value == event_raw:
                    event_type = et
                    break

        return cls(
            id=str(data.get("id", uuid.uuid4().hex[:12])),
            type=str(data.get("type", "req")),
            channel_id=str(data.get("channel_id", "")),
            session_id=str(data.get("session_id", "")),
            params=data.get("params") if isinstance(data.get("params"), dict) else {},
            timestamp=float(data.get("timestamp", time.time())),
            ok=bool(data.get("ok", True)),
            req_method=req_method,
            mode=Mode.from_raw(data.get("mode", "agent_plan")),
            is_stream=bool(data.get("is_stream", False)),
            stream_seq=int(data.get("stream_seq", 0)),
            stream_id=str(data.get("stream_id", "")),
            payload=data.get("payload"),
            event_type=event_type,
            metadata=data.get("metadata") if isinstance(data.get("metadata"), dict) else {},
        )

    @classmethod
    def from_json(cls, raw: str) -> Message:
        """Deserialize from a JSON string."""
        return cls.from_dict(json.loads(raw))

    # ── factory helpers ─────────────────────────────────────────

    @classmethod
    def new_req(
        cls,
        method: ReqMethod,
        *,
        channel_id: str = "",
        session_id: str = "",
        params: dict[str, Any] | None = None,
        mode: Mode = Mode.AGENT_PLAN,
        is_stream: bool = True,
        metadata: dict[str, Any] | None = None,
    ) -> Message:
        """Create a ``req`` message."""
        return cls(
            type="req",
            channel_id=channel_id,
            session_id=session_id,
            params=params or {},
            req_method=method,
            mode=mode,
            is_stream=is_stream,
            metadata=metadata or {},
        )

    @classmethod
    def new_res(
        cls,
        req: Message,
        *,
        ok: bool = True,
        payload: Any = None,
        error: str = "",
    ) -> Message:
        """Create a ``res`` message in response to a request."""
        p = dict(payload or {})
        if not ok and error:
            p["error"] = error
        return cls(
            id=req.id,
            type="res",
            channel_id=req.channel_id,
            session_id=req.session_id,
            ok=ok,
            payload=p,
            is_stream=False,
        )

    @classmethod
    def new_event(
        cls,
        event_type: EventType,
        *,
        channel_id: str = "",
        session_id: str = "",
        payload: Any = None,
        metadata: dict[str, Any] | None = None,
    ) -> Message:
        """Create an ``event`` message."""
        return cls(
            type="event",
            channel_id=channel_id,
            session_id=session_id,
            event_type=event_type,
            payload=payload,
            metadata=metadata or {},
        )
