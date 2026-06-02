# Agent Memory

File-based persistent memory that bridges conversations across sessions.

## ADDED Requirements

### Requirement: MemoryManager loads memory files

The system SHALL provide a `MemoryManager` that reads `MEMORY.md` and files from `daily_memory/` on initialization.

#### Scenario: Memory loaded on start

- **WHEN** `MEMORY.md` exists in the workspace memory directory
- **THEN** its content is loaded and available via `memory_manager.get_context()`

#### Scenario: Empty memory when no files exist

- **WHEN** the memory directory is empty
- **THEN** `memory_manager.get_context()` returns an empty string

### Requirement: Memory is injected into system prompt

The system SHALL include memory content in the agent's system prompt before each LLM call.

#### Scenario: Memory appears in chat context

- **WHEN** memory contains "User's name is Alex, prefers Python"
- **AND** a new chat session starts
- **THEN** the system prompt includes "User's name is Alex, prefers Python"

### Requirement: Remember tool saves facts

The system SHALL provide a `remember` tool that appends facts to a daily memory file.

#### Scenario: Agent remembers a fact

- **WHEN** the agent calls `remember(content="User's favorite color is blue")`
- **THEN** a file `daily_memory/YYYY-MM-DD.md` is created/appended with that fact

### Requirement: Recall tool searches memory

The system SHALL provide a `recall` tool that searches all memory files for a query.

#### Scenario: Agent recalls a fact

- **WHEN** the agent calls `recall(query="favorite color")`
- **THEN** memory files are searched and matching lines are returned

### Requirement: USER.md updated automatically

The system SHALL append facts to `USER.md` when the agent learns about the user.

#### Scenario: User tells the agent their name

- **WHEN** user says "My name is Alex"
- **AND** the agent decides to remember this
- **THEN** `USER.md` is updated with "- Name: Alex"
