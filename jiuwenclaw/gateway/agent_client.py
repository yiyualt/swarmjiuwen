"""AgentClient — WS client that connects Gateway to AgentServer."""

from __future__ import annotations

import json
import logging
from typing import Any

from websockets.asyncio.client import connect

from jiuwenclaw.schema.message import Message, ReqMethod

_logger = logging.getLogger(__name__)


class AgentClient:
    """WebSocket client for the AgentServer.

    Connects to AgentServer (default ws://127.0.0.1:18092) and provides
    a `chat()` method that sends requests and returns responses.
    """

    def __init__(self, url: str = "ws://127.0.0.1:18092"):
        self.url = url
        self._ws: Any = None

    async def connect(self) -> None:
        """Connect to the AgentServer."""
        self._ws = await connect(self.url)
        _logger.info("[AgentClient] connected to %s", self.url)

    async def disconnect(self) -> None:
        """Disconnect from the AgentServer."""
        if self._ws:
            await self._ws.close()
            self._ws = None

    async def chat(self, query: str, session_id: str = "") -> str:
        """Send a chat request and return the response text.

        Raises RuntimeError if not connected.
        """
        if self._ws is None:
            raise RuntimeError("AgentClient not connected. Call connect() first.")

        msg = Message.new_req(
            ReqMethod.CHAT_SEND,
            channel_id="web",
            session_id=session_id,
            params={"query": query},
        )
        await self._ws.send(msg.to_json())

        # Read responses until we get the final res
        while True:
            raw = await self._ws.recv()
            data = json.loads(raw)

            if data.get("type") == "event":
                continue  # skip chat.final, only care about res

            if data.get("type") == "res":
                if data.get("ok"):
                    return data.get("payload", {}).get("content", "")
                raise RuntimeError(data.get("payload", {}).get("error", "Unknown error"))
