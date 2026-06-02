# Agent LLM Bridge

Minimal agent that connects JiuwenClaw messages to openjiuwen's LLM.

## ADDED Requirements

### Requirement: Agent single-turn chat

The system SHALL provide an `Agent` class with a `chat(query)` method that calls the LLM and returns the text response.

#### Scenario: Chat returns LLM response

- **WHEN** `agent.chat("What is 2+2?")` is called
- **THEN** the LLM is called with the query
- **AND** the response text is returned

#### Scenario: Chat with streaming

- **WHEN** `agent.chat_stream("Hello")` is called
- **THEN** tokens are yielded as they arrive from the LLM

### Requirement: WebChannel uses Agent instead of echo

The system SHALL replace WebChannel's echo behavior with real LLM calls via Agent.

#### Scenario: Chat request gets real response

- **WHEN** a client sends `chat.send` with query "What is Python?"
- **THEN** the response contains real LLM-generated text, not an echo
- **AND** the response includes `chat.final` event with the full answer
