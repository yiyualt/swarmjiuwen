"""ChannelBase — abstract base class for all channels."""

from __future__ import annotations

from abc import ABC, abstractmethod


class ChannelBase(ABC):
    """Abstract base for all communication channels.

    Every channel translates between its native protocol and JiuwenClaw's
    Message format. The channel's job is translation — no routing logic.
    """

    channel_id: str = ""

    @abstractmethod
    async def start(self) -> None:
        """Start the channel. Called once at startup."""

    @abstractmethod
    async def stop(self) -> None:
        """Stop the channel. Called at shutdown."""
