# Session History

Per-session conversation context for multi-turn dialogue.

## ADDED Requirements

### Requirement: Agent remembers conversation history

The system SHALL store past messages per session_id and include them in subsequent LLM calls.

#### Scenario: Multi-turn conversation

- **WHEN** user says "My name is Alex" in session "sess-1"
- **AND** user says "What is my name?" in session "sess-1"
- **THEN** the LLM sees the previous message and responds "Your name is Alex"

#### Scenario: Separate sessions don't leak

- **WHEN** user says "I like Python" in session "sess-1"
- **AND** user starts a new chat in session "sess-2"
- **THEN** session "sess-2" has no knowledge of "I like Python"
