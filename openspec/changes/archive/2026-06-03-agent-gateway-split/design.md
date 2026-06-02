## Context

The original jiuwenclaw runs AgentServer and Gateway as separate processes. They communicate via WebSocket using our Message schema.

```
Before:  Browser → WebChannel(WS:19000) → Agent.chat() (same process)

After:   Browser → WebChannel(WS:19000) → AgentClient → [WS] → AgentServer(WS:18092) → Agent.chat()
```

## Decisions

### Direct Message pass-through (no MessageHandler yet)

For this first step, AgentServer simply receives the query string, calls Agent.chat(), and returns the response. We don't introduce the full MessageHandler/Multi-route Gateway yet — that comes next.

### WebSocket, not HTTP

Following the original: bidirectional, streaming-native, multiplexable per session_id. Same Message JSON wire format we already defined.

### AgentServer wraps existing Agent class

No change to Agent internals. AgentServer is a thin WS wrapper around `Agent.chat()`.
