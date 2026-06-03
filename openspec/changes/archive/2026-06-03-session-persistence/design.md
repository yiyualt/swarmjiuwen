## Context

History is currently a `_history: dict[str, list[dict]]` in Agent memory. Add JSON file backing at `~/.jiuwenclaw/agent/sessions/<session_id>/history.json`.

## Format

```json
[
  {"role": "user", "content": "My name is Alex"},
  {"role": "assistant", "content": "Got it!"}
]
```

## Flow

- On first `chat()` for a session: try loading from disk
- After each response: save to disk
- On eviction: delete session dir
