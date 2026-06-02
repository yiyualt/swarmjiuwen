## Why

We have `Message` — the vocabulary. Now we need a transport — something that moves messages between a user and (eventually) the agent. The Channel abstraction lets any communication platform (Web browser, CLI, Feishu, etc.) plug into JiuwenClaw by implementing a single interface. The first channel is WebChannel: a WebSocket server that browsers connect to.

## What Changes

- Add `ChannelBase` abstract class — `channel_id`, `start()`, `stop()`
- Add `WebChannel` — WebSocket server that translates JSON ↔ Message
- Add `ChannelManager` — registry that holds active channels and routes messages between them
- WebChannel echoes incoming messages back to the sender (no agent yet)
- Update docs: tutorial for connecting via browser, example of the echo loop

## Capabilities

### New Capabilities

- `channel-abstraction`: ChannelBase abstract contract, WebChannel for browser access, ChannelManager registry

### Modified Capabilities

<!-- None -->

## Impact

- **New file**: `jiuwenclaw/channel/__init__.py`, `jiuwenclaw/channel/base.py`
- **New file**: `jiuwenclaw/channel/web_channel.py`
- **New file**: `jiuwenclaw/gateway/channel_manager.py`
- **New dep**: `websockets` (added to pyproject.toml)
- **Update docs**: new tutorial + new example
