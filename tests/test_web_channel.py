"""Tests for WebChannel — connection, messaging, error handling."""

import asyncio
import json
from unittest.mock import AsyncMock, patch

import pytest
from websockets.asyncio.client import connect

from jiuwenclaw.channel.web_channel import WebChannel, WebChannelConfig
from jiuwenclaw.schema.message import Message, ReqMethod

TEST_PORT = 19001


class MockAgent:
    """Stand-in for Agent that doesn't need openjiuwen."""
    async def chat(self, query: str) -> str:
        return f"You asked: {query}"


@pytest.fixture
async def web_channel():
    """Start a WebChannel with a mock Agent on a test port."""
    config = WebChannelConfig(host="127.0.0.1", port=TEST_PORT, path="/ws")
    channel = WebChannel(config)
    channel._agent = MockAgent()  # inject mock before start
    task = asyncio.create_task(channel.start())
    await asyncio.sleep(0.1)
    yield channel
    await channel.stop()
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


@pytest.mark.asyncio
async def test_connect_and_receive_ack(web_channel):
    """Connecting should receive a CONNECTION_ACK event."""
    async with connect(f"ws://127.0.0.1:{TEST_PORT}/ws") as ws:
        raw = await asyncio.wait_for(ws.recv(), timeout=2)
        data = json.loads(raw)
        assert data["type"] == "event"
        assert data["event"] == "connection.ack"


@pytest.mark.asyncio
async def test_chat_send_gets_agent_response(web_channel):
    """Sending chat.send should get a real agent response, not echo."""
    msg = Message.new_req(
        ReqMethod.CHAT_SEND,
        channel_id="web",
        session_id="sess-001",
        params={"query": "Hello, world!"},
    )
    async with connect(f"ws://127.0.0.1:{TEST_PORT}/ws") as ws:
        await ws.recv()  # ack

        await ws.send(msg.to_json())

        # First: chat.final event
        event_raw = await asyncio.wait_for(ws.recv(), timeout=2)
        event_data = json.loads(event_raw)
        assert event_data["type"] == "event"
        assert event_data["event"] == "chat.final"
        assert "You asked: Hello, world!" in event_data["payload"]["content"]

        # Then: res
        res_raw = await asyncio.wait_for(ws.recv(), timeout=2)
        res_data = json.loads(res_raw)
        assert res_data["type"] == "res"
        assert res_data["ok"] is True
        assert "You asked: Hello, world!" in res_data["payload"]["content"]


@pytest.mark.asyncio
async def test_invalid_json_returns_error(web_channel):
    """Invalid JSON should get an error response."""
    async with connect(f"ws://127.0.0.1:{TEST_PORT}/ws") as ws:
        await ws.recv()  # ack
        await ws.send("not json")
        raw = await asyncio.wait_for(ws.recv(), timeout=2)
        data = json.loads(raw)
        assert data["ok"] is False


@pytest.mark.asyncio
async def test_empty_query_returns_error(web_channel):
    """A chat.send with no query should get an error."""
    msg = Message.new_req(ReqMethod.CHAT_SEND, channel_id="web", params={})
    async with connect(f"ws://127.0.0.1:{TEST_PORT}/ws") as ws:
        await ws.recv()  # ack
        await ws.send(msg.to_json())
        raw = await asyncio.wait_for(ws.recv(), timeout=2)
        data = json.loads(raw)
        assert data["ok"] is False
        assert "No query" in data["payload"]["error"]
