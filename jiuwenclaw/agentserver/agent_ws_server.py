"""AgentWebSocketServer — standalone WS server wrapping Agent on port 18092."""

from __future__ import annotations

import json
import logging
from typing import Any

from jiuwenclaw.agentserver.agent import Agent
from jiuwenclaw.schema.message import EventType, Message

_logger = logging.getLogger(__name__)


class AgentWebSocketServer:
    """WebSocket server that exposes Agent to the Gateway.

    Listens on port 18092. Gateway connects as a client and sends
    `chat.send` requests. The server calls Agent.chat() and returns
    the response.
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 18092):
        self.host = host
        self.port = port
        self._server: Any = None
        self._agent = Agent()

    async def start(self) -> None:
        from websockets.asyncio.server import serve

        self._server = await serve(self._handle, self.host, self.port)
        _logger.info("[AgentServer] listening on ws://%s:%s", self.host, self.port)

    async def stop(self) -> None:
        if self._server:
            self._server.close()
            await self._server.wait_closed()
        _logger.info("[AgentServer] stopped")

    async def _handle(self, websocket: Any) -> None:
        _logger.info("[AgentServer] Gateway connected")
        try:
            async for raw in websocket:
                await self._on_message(websocket, raw)
        except Exception:
            _logger.debug("[AgentServer] Gateway disconnected", exc_info=True)

    async def _on_message(self, websocket: Any, raw: str | bytes) -> None:
        try:
            data = json.loads(raw if isinstance(raw, str) else raw.decode())
            msg = Message.from_dict(data)
        except Exception:
            return

        if msg.type != "req" or not msg.req_method:
            return

        query = msg.params.get("query", msg.params.get("content", ""))

        try:
            answer = await self._agent.chat(query, msg.session_id)

            # chat.final event
            event = Message.new_event(
                EventType.CHAT_FINAL,
                session_id=msg.session_id,
                payload={"content": answer},
            )
            await websocket.send(event.to_json())

            # response
            res = Message.new_res(msg, ok=True, payload={"content": answer})
            await websocket.send(res.to_json())

        except Exception as e:
            _logger.exception("[AgentServer] chat failed")
            res = Message.new_res(msg, ok=False, error=str(e))
            await websocket.send(res.to_json())
