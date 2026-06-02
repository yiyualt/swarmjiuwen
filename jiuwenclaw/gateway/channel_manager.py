"""ChannelManager — registry for active channels.

Routes outgoing messages to the correct channel by ``channel_id``.
"""

from __future__ import annotations

import logging

from jiuwenclaw.channel.base import ChannelBase
from jiuwenclaw.schema.message import Message

_logger = logging.getLogger(__name__)


class ChannelManager:
    """Holds active channels and routes messages between them."""

    def __init__(self):
        self._channels: dict[str, ChannelBase] = {}

    def register_channel(self, channel: ChannelBase) -> None:
        """Add a channel to the registry."""
        if not channel.channel_id:
            raise ValueError("Channel must have a channel_id")
        self._channels[channel.channel_id] = channel
        _logger.info("[ChannelManager] registered channel: %s", channel.channel_id)

    def unregister_channel(self, channel_id: str) -> None:
        """Remove a channel from the registry."""
        self._channels.pop(channel_id, None)
        _logger.info("[ChannelManager] unregistered channel: %s", channel_id)

    def get_channel(self, channel_id: str) -> ChannelBase | None:
        """Look up a channel by id."""
        return self._channels.get(channel_id)

    def list_channels(self) -> list[str]:
        """Return all registered channel ids."""
        return list(self._channels.keys())

    async def send_to_channel(self, channel_id: str, message: Message) -> bool:
        """Deliver a message to a specific channel. Returns True if delivered."""
        channel = self._channels.get(channel_id)
        if channel is None or not hasattr(channel, "broadcast"):
            return False
        await channel.broadcast(message)  # type: ignore[union-attr]
        return True
