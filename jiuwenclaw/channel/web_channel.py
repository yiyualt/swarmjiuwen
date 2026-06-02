"""WebChannel — WebSocket server for browser access.

Translates JSON frames ↔ Message objects. Currently echoes messages back
since there's no agent yet.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import Any

from jiuwenclaw.channel.base import ChannelBase
from jiuwenclaw.schema.message import EventType, Message
from jiuwenclaw.agentserver.agent import Agent

_logger = logging.getLogger(__name__)


@dataclass
class WebChannelConfig:
    """Configuration for the Web channel."""

    enabled: bool = True
    host: str = "127.0.0.1"
    port: int = 19000
    path: str = "/ws"

    @classmethod
    def from_config(cls) -> WebChannelConfig:
        """Create config from the JiuwenClaw config system."""
        from jiuwenclaw.config import get_config
        cfg = get_config()
        web = cfg.get("channels", {}).get("web", {})
        return cls(
            enabled=bool(web.get("enabled", True)),
            host=str(web.get("host", "127.0.0.1")),
            port=int(web.get("port", 19000)),
            path=str(web.get("path", "/ws")),
        )


class WebChannel(ChannelBase):
    """Web channel for browser access over WebSocket."""

    channel_id = "web"

    def __init__(self, config: WebChannelConfig | None = None):
        self.config = config or WebChannelConfig()
        self._server: Any = None
        self._clients: set[Any] = set()
        self._agent: Agent | None = None

    @property
    def agent(self) -> Agent:
        if self._agent is None:
            self._agent = Agent()
        return self._agent

    async def start(self) -> None:
        """Start the WebSocket server."""
        from websockets.asyncio.server import serve

        self._server = await serve(
            self._handle_connection,
            self.config.host,
            self.config.port,
        )
        _logger.info(
            "[WebChannel] listening on ws://%s:%s%s",
            self.config.host, self.config.port, self.config.path,
        )

    async def stop(self) -> None:
        """Stop the WebSocket server."""
        for client in list(self._clients):
            await client.close()
        self._clients.clear()
        if self._server:
            self._server.close()
            await self._server.wait_closed()
            self._server = None
        _logger.info("[WebChannel] stopped")

    async def broadcast(self, message: Message) -> None:
        """Send a message to all connected clients."""
        data = message.to_json()
        dead: set[Any] = set()
        for client in self._clients:
            try:
                await client.send(data)
            except Exception:
                dead.add(client)
        self._clients -= dead

    # ── internal ────────────────────────────────────────────────

    async def _handle_connection(self, websocket: Any) -> None:
        """Handle a single WebSocket connection."""
        self._clients.add(websocket)

        # Send connection acknowledgment
        ack = Message.new_event(
            EventType.CONNECTION_ACK,
            channel_id=self.channel_id,
            payload={"protocol_version": "1.0", "transport": self.channel_id},
        )
        await websocket.send(ack.to_json())

        try:
            async for raw in websocket:
                await self._handle_message(websocket, raw)
        except Exception:
            _logger.debug("[WebChannel] client disconnected", exc_info=True)
        finally:
            self._clients.discard(websocket)

    async def _handle_message(self, websocket: Any, raw: str | bytes) -> None:
        """Parse and echo an incoming message."""
        try:
            data = json.loads(raw if isinstance(raw, str) else raw.decode())
            msg = Message.from_dict(data)
        except (json.JSONDecodeError, Exception) as e:
            await websocket.send(json.dumps({
                "type": "res", "id": "", "ok": False,
                "error": f"invalid message: {e}",
            }))
            return

        _logger.debug("[WebChannel] received: type=%s method=%s", msg.type, msg.req_method)

        if msg.type != "req" or msg.req_method is None:
            return

        query = msg.params.get("query", msg.params.get("content", ""))
        if not query:
            res = Message.new_res(msg, ok=False, error="No query provided")
            await websocket.send(res.to_json())
            return

        try:
            answer = await self.agent.chat(query)

            # Send final event
            final = Message.new_event(
                EventType.CHAT_FINAL,
                channel_id=self.channel_id,
                session_id=msg.session_id,
                payload={"content": answer},
            )
            await websocket.send(final.to_json())

            # Send response
            res = Message.new_res(msg, ok=True, payload={"content": answer})
            await websocket.send(res.to_json())
        except Exception as e:
            _logger.exception("[WebChannel] agent call failed")
            res = Message.new_res(msg, ok=False, error=str(e))
            await websocket.send(res.to_json())
