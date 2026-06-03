# Heartbeat and Startup

Periodic agent wake-up and one-command startup.

## ADDED Requirements

### Requirement: Heartbeat sends periodic messages

The system SHALL provide `GatewayHeartbeatService` that sends a chat request to Agent at a configurable interval.

#### Scenario: Heartbeat triggers agent

- **WHEN** heartbeat is enabled with `every: 60` and `target: web`
- **THEN** every 60 seconds, a chat message is sent to Agent via AgentClient

#### Scenario: Heartbeat is disabled by default

- **WHEN** config has `heartbeat.enabled: false`
- **THEN** the heartbeat timer does not start

### Requirement: One-command startup

The system SHALL provide `jiuwenclaw-start` that starts AgentServer + Gateway as subprocesses.

#### Scenario: Start both processes

- **WHEN** `jiuwenclaw-start` is executed
- **THEN** AgentServer starts on port 18092
- **AND** Gateway (WebChannel) starts on port 19000

#### Scenario: Graceful shutdown on Ctrl+C

- **WHEN** Ctrl+C is pressed
- **THEN** both subprocesses are terminated gracefully
