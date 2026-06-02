# Agent-Gateway Split

Split AgentServer from Gateway into separate processes communicating over WebSocket.

## ADDED Requirements

### Requirement: AgentServer runs as standalone WS server

The system SHALL provide `AgentWebSocketServer` that wraps Agent in a WebSocket server on port 18092.

#### Scenario: Gateway connects to AgentServer

- **WHEN** AgentWebSocketServer is started on port 18092
- **AND** a client connects via WebSocket
- **THEN** the connection is accepted

#### Scenario: AgentServer processes chat request

- **WHEN** a client sends `{"type": "req", "method": "chat.send", "params": {"query": "Hello"}}`
- **THEN** Agent.chat("Hello") is called
- **AND** the response is sent back as `{"type": "res", "ok": true, "payload": {"content": "..."}}`

### Requirement: AgentClient connects Gateway to AgentServer

The system SHALL provide `AgentClient` that connects to AgentServer via WebSocket and forwards requests.

#### Scenario: Gateway sends chat via AgentClient

- **WHEN** `agent_client.chat("Hello")` is called
- **THEN** a WebSocket message is sent to AgentServer
- **AND** the response is returned

### Requirement: app.py orchestrates both processes

The system SHALL provide `app.py` that starts AgentServer and Gateway as subprocesses.

#### Scenario: Both processes start via app.py

- **WHEN** `python -m jiuwenclaw.app` is executed
- **THEN** AgentServer starts on port 18092
- **AND** Gateway (WebChannel + AgentClient) starts on port 19000
