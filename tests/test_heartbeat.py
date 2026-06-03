"""Tests for GatewayHeartbeatService."""

import asyncio

import pytest

from jiuwenclaw.gateway.heartbeat import GatewayHeartbeatService, HeartbeatConfig


class MockClient:
    """Records calls for verification."""
    def __init__(self):
        self.calls = []

    async def chat(self, query: str, session_id: str = "") -> str:
        self.calls.append(query)
        return "ok"

    async def disconnect(self):
        pass


@pytest.mark.asyncio
async def test_heartbeat_disabled_does_not_start():
    client = MockClient()
    hb = GatewayHeartbeatService(client, HeartbeatConfig(enabled=False))
    await hb.start()
    assert hb._task is None


@pytest.mark.asyncio
async def test_heartbeat_enabled_starts():
    client = MockClient()
    hb = GatewayHeartbeatService(
        client,
        HeartbeatConfig(enabled=True, interval_seconds=0.1),
    )
    await hb.start()
    assert hb._task is not None
    await asyncio.sleep(0.3)  # let it fire at least once
    await hb.stop()
    assert len(client.calls) >= 1


@pytest.mark.asyncio
async def test_heartbeat_stops_cleanly():
    client = MockClient()
    hb = GatewayHeartbeatService(
        client,
        HeartbeatConfig(enabled=True, interval_seconds=0.1),
    )
    await hb.start()
    await hb.stop()
    assert hb._task is None
