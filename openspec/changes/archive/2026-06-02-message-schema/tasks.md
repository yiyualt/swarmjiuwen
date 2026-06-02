## 1. Package Setup

- [x] 1.1 Create `jiuwenclaw/` package with `__init__.py`, `pyproject.toml`
- [x] 1.2 Create `tests/` with `conftest.py` (no fixtures needed yet)

## 2. Message Schema

- [x] 2.1 Implement `schema/message.py` — `Message` dataclass, `ReqMethod`, `EventType`, `Mode` enums
- [x] 2.2 Implement `to_dict()`, `to_json()`, `from_dict()`, `from_json()`
- [x] 2.3 Implement factory helpers: `new_req()`, `new_res()`, `new_event()`

## 3. Tests

- [x] 3.1 Write `tests/test_message.py` covering all scenarios from the spec

## 4. Documentation

- [x] 4.1 Write `docs/jiuwenclaw/tutorials/getting-started.rst` — install, create a Message, serialize
- [x] 4.2 Write `docs/jiuwenclaw/examples/message-example.rst` — practical usage patterns
