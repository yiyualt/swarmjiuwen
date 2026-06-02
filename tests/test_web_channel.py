"""Tests for WebChannel — start, connect, echo."""

import asyncio
import json

import pytest
from websockets.asyncio.client import connect

from jiuwenclaw.channel.web_channel import WebChannel, WebChannelConfig
from jiuwenclaw.schema.message import Message, ReqMethod


TEST_PORT = 19001  # different from default to avoid conflicts


@pytest.fixture
async def web_channel():
    """Start a WebChannel on a test port."""
    config = WebChannelConfig(host="127.0.0.1", port=TEST_PORT, path="/ws")
    channel = WebChannel(config)
    task = asyncio.create_task(channel.start())
    await asyncio.sleep(0.1)  # let server start
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
async def test_send_req_and_receive_echo(web_channel):
    """Sending a req should echo back the query."""
    msg = Message.new_req(
        ReqMethod.CHAT_SEND,
        channel_id="web",
        session_id="sess-001",
        params={"query": "Hello, world!"},
    )
    async with connect(f"ws://127.0.0.1:{TEST_PORT}/ws") as ws:
        # Skip ack
        await ws.recv()

        # Send request
        await ws.send(msg.to_json())

        # Receive echo response
        raw = await asyncio.wait_for(ws.recv(), timeout=2)
        data = json.loads(raw)
        assert data["type"] == "res"
        assert data["ok"] is True
        assert data["payload"]["echo"] == "Hello, world!"


@pytest.mark.asyncio
async def test_invalid_json_returns_error(web_channel):
    """Invalid JSON should get an error response."""
    async with connect(f"ws://127.0.0.1:{TEST_PORT}/ws") as ws:
        await ws.recv()  # skip ack
        await ws.send("not json")
        raw = await asyncio.wait_for(ws.recv(), timeout=2)
        data = json.loads(raw)
        assert data["ok"] is False
        assert "error" in data


@pytest.mark.asyncio
async def test_multiple_clients(web_channel):
    """Multiple clients can connect simultaneously."""
    async def client():
        async with connect(f"ws://127.0.0.1:{TEST_PORT}/ws") as ws:
            await ws.recv()  # ack
            msg = Message.new_req(ReqMethod.CHAT_SEND, params={"query": "hi"})
            await ws.send(msg.to_json())
            raw = await asyncio.wait_for(ws.recv(), timeout=2)
            data = json.loads(raw)
            assert data["ok"] is True

    await asyncio.gather(client(), client(), client())
