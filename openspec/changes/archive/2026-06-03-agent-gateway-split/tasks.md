## 1. AgentServer WS

- [x] 1.1 Implement `agentserver/agent_ws_server.py` — WS server wrapping Agent on port 18092
- [x] 1.2 Implement `app_agentserver.py` — standalone entry point

## 2. AgentClient (Gateway side)

- [x] 2.1 Implement `gateway/agent_client.py` — WS client to AgentServer

## 3. Wire together

- [x] 3.1 Modify `channel/web_channel.py` — use AgentClient instead of direct Agent
- [x] 3.2 Implement `app.py` — start AgentServer + Gateway as subprocesses

## 4. Tests

- [x] 4.1 Write `tests/test_agent_ws.py` — AgentServer WS round-trip

## 5. Documentation

- [x] 5.1 Write `docs/jiuwenclaw/tutorials/architecture.rst`
- [x] 5.2 Update `docs/index.rst`
