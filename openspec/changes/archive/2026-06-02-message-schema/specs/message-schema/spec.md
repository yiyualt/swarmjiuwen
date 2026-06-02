# Message Schema

The universal message envelope — the wire format connecting all JiuwenClaw components.

## ADDED Requirements

### Requirement: Message structure

The system SHALL define a `Message` dataclass with fields: `id` (str), `type` (str), `channel_id` (str), `session_id` (str), `params` (dict), `timestamp` (float), `ok` (bool), `req_method` (ReqMethod | None), `mode` (Mode), `is_stream` (bool), `stream_seq` (int), `stream_id` (str), `payload` (Any), `event_type` (EventType | None), `metadata` (dict).

#### Scenario: Create a request message

- **WHEN** `Message.new_req(ReqMethod.CHAT_SEND, channel_id="web", params={"query": "Hello"})` is called
- **THEN** a Message is created with `type="req"`, `req_method=ReqMethod.CHAT_SEND`, and `params={"query": "Hello"}`

#### Scenario: Create an event message

- **WHEN** `Message.new_event(EventType.CHAT_DELTA, payload={"content": "Hi"})` is called
- **THEN** a Message is created with `type="event"`, `event_type=EventType.CHAT_DELTA`

#### Scenario: Create a response from a request

- **WHEN** `Message.new_res(req, ok=True, payload={"answer": "Paris"})` is called
- **THEN** the response has the same `id` as the request and `type="res"`

### Requirement: ReqMethod enum

The system SHALL define `ReqMethod` with values: `CHAT_SEND` ("chat.send"), `CHAT_CANCEL` ("chat.cancel"), `CHAT_RESUME` ("chat.resume"), `SESSION_CREATE` ("session.create"), `SESSION_DELETE` ("session.delete"), `SESSION_LIST` ("session.list").

#### Scenario: Enum has string values

- **WHEN** `ReqMethod.CHAT_SEND.value` is accessed
- **THEN** it returns `"chat.send"`

### Requirement: EventType enum

The system SHALL define `EventType` with values: `CHAT_DELTA` ("chat.delta"), `CHAT_FINAL` ("chat.final"), `TASK_START` ("task.start"), `TASK_COMPLETE` ("task.complete"), `CONNECTION_ACK` ("connection.ack").

#### Scenario: Enum has string values

- **WHEN** `EventType.CHAT_DELTA.value` is accessed
- **THEN** it returns `"chat.delta"`

### Requirement: JSON round-trip

The system SHALL serialize a Message to JSON and deserialize back with zero information loss for all message types.

#### Scenario: Request message round-trip

- **WHEN** a request Message is serialized via `to_json()` and parsed back via `from_json()`
- **THEN** `id`, `type`, `channel_id`, `session_id`, `req_method`, `params` are all preserved

#### Scenario: Response message round-trip

- **WHEN** a response Message is serialized and parsed back
- **THEN** `ok`, `payload`, and the matching request `id` are preserved

#### Scenario: Event message round-trip

- **WHEN** an event Message is serialized and parsed back
- **THEN** `event_type` and `payload` are preserved
