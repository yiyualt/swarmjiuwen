## Why

Every component in JiuwenClaw — channels, gateway, agent — needs a common language to communicate. Without a shared message format, each channel integration becomes a one-off adapter. The Message schema defines the universal wire format: three message types, a set of request methods, and a set of event types. This is the first and most fundamental building block.

## What Changes

- Add `Message` dataclass with `id`, `type`, `channel_id`, `session_id`, `params`, `payload`, and metadata fields
- Add `ReqMethod` enum — `CHAT_SEND`, `CHAT_CANCEL`, `CHAT_RESUME`, `SESSION_CREATE`, `SESSION_DELETE`, `SESSION_LIST`
- Add `EventType` enum — `CHAT_DELTA`, `CHAT_FINAL`, `TASK_START`, `TASK_COMPLETE`, `CONNECTION_ACK`
- Add `Mode` enum — `AGENT_PLAN`, `AGENT_EXEC`
- JSON serialization/deserialization round-trip
- Factory helpers: `Message.new_req()`, `Message.new_res()`, `Message.new_event()`

## Capabilities

### New Capabilities

- `message-schema`: The Message dataclass with ReqMethod, EventType, Mode enums — the wire format connecting all JiuwenClaw components

### Modified Capabilities

<!-- None — this is the first capability -->

## Impact

- **New file**: `jiuwenclaw/schema/message.py`
- **New file**: `tests/test_message.py`
- **New file**: `docs/jiuwenclaw/tutorials/getting-started.rst`
- **New file**: `docs/jiuwenclaw/examples/message-example.rst`
- **Dependencies**: none (pure Python, no external packages needed for the schema itself)
