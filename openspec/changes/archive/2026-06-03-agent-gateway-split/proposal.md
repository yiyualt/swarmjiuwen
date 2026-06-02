## Why

Currently Agent lives inside WebChannel — same process. The original architecture splits them: AgentServer (LLM-heavy, port 18092) and Gateway (IO-heavy, port 19000/19001) communicate over WebSocket. This separation lets them scale independently and matches the production architecture.

## What Changes

- Add `agentserver/agent_ws_server.py` — WebSocket server wrapping Agent on port 18092
- Add `gateway/agent_client.py` — WebSocket client that connects Gateway to AgentServer
- Add `app_agentserver.py` — standalone AgentServer entry point
- Add `app.py` — orchestrates AgentServer and Gateway subprocesses
- Modify `channel/web_channel.py` — use AgentClient (WS) instead of direct Agent call

## Capabilities

### New Capabilities

- `agent-gateway-split`: AgentServer (WS:18092) ↔ Gateway (WS:19000) split architecture

## Impact

- **New file**: `agentserver/agent_ws_server.py`
- **New file**: `gateway/agent_client.py`
- **New file**: `app_agentserver.py`, `app.py`
- **Modified file**: `channel/web_channel.py` — Agent → AgentClient
