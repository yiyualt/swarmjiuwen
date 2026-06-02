## Why

We're duplicating openjiuwen's React loop in `Agent.chat()` — manual tool call parsing, manual 2-round invoke, no multi-turn tool chaining. The vendor's `ReActAgent` already handles this correctly with full Think→Act→Observe, interrupt handling, and streaming. We should use it instead of rewriting it.

## What Changes

- Replace hand-rolled `Agent.chat()` with `ReActAgent.invoke()`
- Add `AgentCard` — identity card for the agent (name, description, abilities)
- Register tools as abilities on the AgentCard so ReActAgent can call them
- Remove `_parse_tool_call()` and manual tool-calling logic from Agent
- Keep the same external interface: `Agent.chat(query) -> str`

## Capabilities

### New Capabilities

- `react-agent-refactor`: Use vendor ReActAgent for full React loop with multi-turn tool chaining

### Modified Capabilities

<!-- None — external behavior unchanged, internal implementation replaced -->

## Impact

- **Modified file**: `jiuwenclaw/agentserver/agent.py` — replace chat() with ReActAgent
- **Removed code**: `_parse_tool_call()`, manual tool-call logic
- **External behavior unchanged**: `chat(query)` still returns a string
