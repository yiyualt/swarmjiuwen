## Context

openjiuwen's `ReActAgent` provides a production-quality React loop. Using it means we get multi-turn tool chaining, interrupt handling, and proper session management for free.

## Goals / Non-Goals

**Goals:**
- Replace our `chat()` with `ReActAgent.invoke()`
- Create minimal AgentCard with name, description, and tool abilities
- Keep existing tool registration — tools stay the same
- Same external API: `Agent.chat(query) -> str`

**Non-Goals:**
- Session persistence (future)
- Streaming via ReActAgent (future)
- Custom rails/middleware (future)

## Decisions

### ReActAgent.invoke() takes dict input

`invoke({"query": "Hello"})` returns `{"output": "response", "result_type": "answer"}`. We wrap this to return just the output string.

### Tools registered as Abilities on AgentCard

ReActAgent's `AbilityManager` handles tool registration. We migrate our ToolManager tools to Ability registrations on the AgentCard.
