"""GatewayHeartbeatService — periodic agent wake-up."""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass

_logger = logging.getLogger(__name__)


@dataclass
class HeartbeatConfig:
    """Heartbeat configuration."""

    enabled: bool = False
    interval_seconds: float = 60.0
    task: str = "Check for pending items and report status."
    target_channel: str = "web"


class GatewayHeartbeatService:
    """Periodically sends a chat message to wake up the Agent.

    Uses the AgentClient to send messages without creating new WS connections.
    """

    def __init__(self, agent_client, config: HeartbeatConfig | None = None):
        self._client = agent_client
        self.config = config or HeartbeatConfig()
        self._task: asyncio.Task | None = None

    async def start(self) -> None:
        if not self.config.enabled:
            _logger.info("[Heartbeat] disabled")
            return

        self._task = asyncio.create_task(self._loop())
        _logger.info(
            "[Heartbeat] started — interval=%ss task=%s",
            self.config.interval_seconds,
            self.config.task[:50],
        )

    async def stop(self) -> None:
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None
        _logger.info("[Heartbeat] stopped")

    async def _loop(self) -> None:
        while True:
            try:
                await asyncio.sleep(self.config.interval_seconds)
                _logger.info("[Heartbeat] waking agent...")
                await self._client.chat(self.config.task, session_id="heartbeat")
            except asyncio.CancelledError:
                break
            except Exception:
                _logger.exception("[Heartbeat] error")
