## Why

Session history lives in memory. Restart AgentServer, lose all conversations. Save history as JSON files per session_id so conversations survive restarts.

## What Changes

- Add `save()` / `load()` methods to Agent — write/read `sessions/<session_id>/history.json`
- Auto-save after each chat() response
- Auto-load on first chat() for a session
- Clean up sessions dir on eviction

## Capabilities

- `session-persistence`: Session history saved to disk, survives restarts

## Impact

- **Modified file**: `jiuwenclaw/agentserver/agent.py` — save/load history
