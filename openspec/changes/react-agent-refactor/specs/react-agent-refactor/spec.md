# React Agent Refactor

Replace hand-rolled tool calling with openjiuwen's ReActAgent.

## ADDED Requirements

### Requirement: Agent uses ReActAgent for chat

The system SHALL use openjiuwen's `ReActAgent.invoke()` for processing chat messages instead of manual model.invoke() with tool parsing.

#### Scenario: Chat returns LLM response

- **WHEN** `agent.chat("What is 2+2?")` is called
- **THEN** ReActAgent.invoke() is called
- **AND** the response "4" (or similar) is returned as a string

#### Scenario: Agent calls tools via ReActAgent

- **WHEN** user asks "Read config.py"
- **THEN** ReActAgent automatically calls read_file tool
- **AND** returns a response that includes the file contents

### Requirement: Backward compatible

The system SHALL maintain the same `Agent.chat(query) -> str` interface.

#### Scenario: Same API as before

- **WHEN** `agent.chat("Hello")` is called
- **THEN** a string response is returned (same type signature as before)
