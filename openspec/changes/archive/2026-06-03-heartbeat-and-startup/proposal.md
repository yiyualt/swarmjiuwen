## Why

Two quality-of-life improvements matching the original architecture:
1. **Heartbeat**: Agent can be woken periodically to do background tasks
2. **start_services.py**: One command starts both processes instead of two terminals

## What Changes

### Heartbeat
- Add `gateway/heartbeat.py` — periodic timer that sends chat requests to Agent
- Configurable interval and target channel from config.yaml
- Works through existing AgentClient (no new WS connections)

### Startup
- Add `start_services.py` — `jiuwenclaw-start` CLI command
- Starts AgentServer + Gateway as subprocesses
- Graceful shutdown on Ctrl+C

## Capabilities

- `heartbeat-and-startup`: Periodic agent wake-up + one-command startup

## Impact

- **New file**: `jiuwenclaw/gateway/heartbeat.py`
- **New file**: `jiuwenclaw/start_services.py`
- **Modified file**: `pyproject.toml` — add `jiuwenclaw-start` entry point
- **Modified file**: `jiuwenclaw/resources/config.yaml` — heartbeat config
