## 1. Add save/load to Agent

- [x] 1.1 Add `_sessions_dir` config and `_save_history()` / `_load_history()` methods to Agent
- [x] 1.2 Load history on first chat() for a session (lazy, not at startup)
- [x] 1.3 Save history after each chat() response
- [x] 1.4 Clean up session dir on eviction

## 2. Tests

- [x] 2.1 Update `tests/test_session.py` — verify disk persistence survives restarts

## 3. Documentation

- [x] 3.1 Update `docs/jiuwenclaw/tutorials/session.rst` — mention persistence
