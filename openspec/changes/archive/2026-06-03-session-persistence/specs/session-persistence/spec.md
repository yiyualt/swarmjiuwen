# Session Persistence

Save session history to disk so conversations survive restarts.

## ADDED Requirements

### Requirement: History saved to disk

The system SHALL save session history as JSON files after each response.

#### Scenario: History survives restart

- **WHEN** user chats in session "sess-1"
- **AND** AgentServer restarts
- **THEN** previous conversation history is loaded from disk

#### Scenario: New session has no history

- **WHEN** a session_id has never been used
- **THEN** no history file exists and an empty history is used
