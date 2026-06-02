## Context

`Message` defines what flows. Channel defines how it flows. Every channel translates between its native protocol and JiuwenClaw's Message format.

For this version, there's no agent — the WebChannel echoes messages back, proving the transport works end-to-end.

## Goals / Non-Goals

**Goals:**
- `ChannelBase` with `channel_id`, async `start()`/`stop()`
- `WebChannel` that starts a WebSocket server, parses incoming JSON into `Message`, echoes it back
- `ChannelManager` that holds channels and delivers messages to the right one
- Browser testable: open DevTools, connect WebSocket, send JSON, see response

**Non-Goals:**
- Agent integration (future)
- Multiple channels running simultaneously (future)
- Authentication (future)
- Config-driven channel setup (future — ports are hardcoded for now)

## Decisions

### 1. ChannelBase is minimal

No message routing logic in the base class. Channels just translate formats. All routing happens in ChannelManager.

### 2. WebChannel echo mode

Without an agent, WebChannel echoes: receives a `req` → sends back a `res` with the same content. This proves the transport works. Replace with real agent routing later.

### 3. websockets library (not aiohttp, not FastAPI)

`websockets` is the simplest WebSocket library for Python. No framework overhead. The reference implementation uses it.

## Risks

- **[Risk] WebSocket server blocks the main thread** → Mitigation: `asyncio` event loop handles concurrent connections
- **[Risk] No agent means echo is boring** → Yes. That's the point. Prove transport first, add intelligence later.
