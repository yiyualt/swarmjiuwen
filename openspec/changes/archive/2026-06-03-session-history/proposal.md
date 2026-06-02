## Why

Each `chat()` call is independent — the Agent forgets what was just said. Session history stores past messages per session_id so the LLM has conversation context for multi-turn dialogue.

## What Changes

- Add `_history: dict[str, list]` to Agent — per-session message storage
- Append user query and assistant response after each `chat()` call
- Include past messages in the LLM call for the same session
- Clean up old sessions after configurable timeout

## Capabilities

- `session-history`: Per-session conversation context for multi-turn dialogue

## Impact

- **Modified file**: `jiuwenclaw/agentserver/agent.py` — history dict + context injection
