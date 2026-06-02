"""Tests for AgentServer WebSocket round-trip."""

import asyncio
import json

import pytest
from websockets.asyncio.client import connect

from jiuwenclaw.schema.message import Message, ReqMethod

TEST_AGENT_PORT = 18093


class MockAgentWS:
    """Start a real AgentWebSocketServer on a test port."""

    def __init__(self):
        from jiuwenclaw.agentserver.agent_ws_server import AgentWebSocketServer
        self._server = AgentWebSocketServer(host="127.0.0.1", port=TEST_AGENT_PORT)

    async def start(self):
        self._task = asyncio.create_task(self._server.start())
        await asyncio.sleep(0.1)

    async def stop(self):
        await self._server.stop()
        self._task.cancel()
        try:
            await self._task
        except asyncio.CancelledError:
            pass


@pytest.fixture
async def agent_server():
    server = MockAgentWS()
    await server.start()
    yield
    await server.stop()


@pytest.mark.asyncio
async def test_agent_server_accepts_connection(agent_server):
    """AgentServer should accept WS connections."""
    async with connect(f"ws://127.0.0.1:{TEST_AGENT_PORT}") as ws:
        assert ws


@pytest.mark.asyncio
async def test_chat_returns_response(agent_server):
    """Sending chat.send should return a response."""
    msg = Message.new_req(
        ReqMethod.CHAT_SEND,
        channel_id="web",
        params={"query": "What is 2+2?"},
    )
    async with connect(f"ws://127.0.0.1:{TEST_AGENT_PORT}") as ws:
        await ws.send(msg.to_json())

        # Should receive chat.final event + res
        responses = []
        for _ in range(2):
            raw = await asyncio.wait_for(ws.recv(), timeout=5)
            responses.append(json.loads(raw))

        # At least one res
        res = [r for r in responses if r["type"] == "res"]
        assert len(res) >= 1, f"Expected res, got: {responses}"
