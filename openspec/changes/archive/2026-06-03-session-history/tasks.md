## 1. Add history to Agent

- [x] 1.1 Add `_history` and `_last_access` dicts to Agent.__init__
- [x] 1.2 Include history messages in chat() before the current query
- [x] 1.3 Append user + assistant messages to history after each chat()
- [x] 1.4 Evict idle sessions (>1 hour since last access, max 50 sessions)

## 2. Tests

- [x] 2.1 Write `tests/test_session.py` — multi-turn context, session isolation

## 3. Documentation

- [x] 3.1 Write `docs/jiuwenclaw/tutorials/session.rst`
- [x] 3.2 Update `docs/index.rst`
