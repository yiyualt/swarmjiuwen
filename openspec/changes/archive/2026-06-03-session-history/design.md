## Context

The original jiuwenclaw uses `session_manager.py` + `agent_manager.py` to manage per-session agent state. Our first step is much simpler: an in-memory dict of message lists.

## Decisions

### In-memory dict, not file persistence (yet)

Simple `_history: dict[str, list[dict]]` with `_last_access: dict[str, float]` for eviction. Files come later with session_manager.

### Append on each chat() call

After the LLM responds, append user message + assistant response to history. Next call prepends history to the message list.
