# Channel Abstraction

The channel interface and WebSocket transport for browser access.

## ADDED Requirements

### Requirement: ChannelBase abstract class

The system SHALL define a `ChannelBase` ABC with `channel_id` (str), `start()` (async), and `stop()` (async).

#### Scenario: Channel has a unique id

- **WHEN** a WebChannel is created with `channel_id="web"`
- **THEN** `channel.channel_id` returns `"web"`

### Requirement: WebChannel WebSocket server

The system SHALL implement `WebChannel` that starts a WebSocket server on a configurable host:port.

#### Scenario: WebChannel accepts connections

- **WHEN** `WebChannel(host="127.0.0.1", port=19000, path="/ws")` is started
- **AND** a WebSocket client connects to `ws://127.0.0.1:19000/ws`
- **THEN** the connection is accepted

#### Scenario: WebChannel parses JSON into Message

- **WHEN** a client sends `{"type": "req", "id": "abc", "method": "chat.send", "params": {"query": "Hello"}}`
- **THEN** a `Message` is created with `type="req"`, `id="abc"`, `req_method=ReqMethod.CHAT_SEND`

#### Scenario: WebChannel echoes response (no agent)

- **WHEN** a client sends a `req` message
- **THEN** the WebChannel sends back a `res` message with `ok=True` and the same `id`
- **AND** the response payload contains the echoed query

#### Scenario: WebChannel stops gracefully

- **WHEN** `stop()` is called
- **THEN** the WebSocket server closes all connections and stops listening

### Requirement: ChannelManager registry

The system SHALL implement `ChannelManager` that registers channels and delivers messages.

#### Scenario: Register a channel

- **WHEN** `channel_manager.register_channel(web_channel)` is called
- **THEN** the channel is added to the registry

#### Scenario: Deliver message to a channel

- **WHEN** `channel_manager.send_to_channel("web", message)` is called
- **THEN** the message is delivered to the WebChannel for transmission
