## Context

JiuwenClaw wraps an LLM agent with a multi-channel message bus. The Message schema is the shared vocabulary — every component (Web UI, CLI, Gateway, Agent) speaks it. This is the first piece built; everything else depends on it.

## Goals / Non-Goals

**Goals:**
- Define `Message` as a pure dataclass with no external dependencies
- Support three message types: `req` (client→agent), `res` (agent→client), `event` (agent push)
- JSON serialization round-trip with zero information loss
- Factory helpers for ergonomic message creation

**Non-Goals:**
- WebSocket transport (that's the channel layer)
- Message routing (that's the gateway)
- Session logic (that's the agent)
- Any I/O or networking

## Decisions

### 1. Dataclass over TypedDict

**Decision**: Use `@dataclass` with factory defaults.

**Why**: Dataclasses give us typed fields with defaults, easy `to_dict()`/`from_dict()`, and IDE autocomplete. TypedDict is lighter but lacks default factories and methods.

### 2. Enums with string values for ReqMethod and EventType

**Decision**: `ReqMethod.CHAT_SEND.value == "chat.send"`.

**Why**: The wire format is JSON strings. Using string-valued enums means `to_json` serializes naturally and `from_json` parses by matching against enum values.

### 3. Factory helpers on the class

**Decision**: `Message.new_req()`, `Message.new_res()`, `Message.new_event()` as `@classmethod`.

**Why**: Keeps construction ergonomic. `Message(type="req", req_method=...)` is verbose and error-prone. Factory methods set defaults correctly for each message type.

## Risks / Trade-offs

**[Risk] Schema evolves and breaks wire compatibility**
→ Mitigation: `connection.ack` includes `protocol_version` from day one. Future versions can negotiate.

**[Risk] JSON round-trip might lose type information**
→ Mitigation: Enum values serialize as strings; `from_dict` matches against all enum members. Unknown enum values produce `None` rather than crashing.
