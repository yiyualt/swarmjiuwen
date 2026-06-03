## 1. Heartbeat

- [x] 1.1 Implement `gateway/heartbeat.py` — GatewayHeartbeatService with configurable interval
- [x] 1.2 Add heartbeat config to `resources/config.yaml`
- [x] 1.3 Wire heartbeat into `channel/web_channel.py` — start/stop with channel lifecycle

## 2. Startup

- [x] 2.1 Implement `start_services.py` — subprocess manager for AgentServer + Gateway
- [x] 2.2 Update `pyproject.toml` — add `jiuwenclaw-start` entry point

## 3. Tests

- [x] 3.1 Write `tests/test_heartbeat.py` — heartbeat triggers, respects enabled flag

## 4. Documentation

- [x] 4.1 Write `docs/jiuwenclaw/tutorials/heartbeat.rst`
- [x] 4.2 Update `docs/index.rst`
