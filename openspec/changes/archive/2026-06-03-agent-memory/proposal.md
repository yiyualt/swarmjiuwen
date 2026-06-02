## Why

Every chat is amnesia. The agent forgets everything between requests. Memory lets it remember facts across sessions — user name, preferences, project context — by storing them as Markdown files in the workspace and loading them into the system prompt.

## What Changes

- Add `agentserver/memory/manager.py` — `MemoryManager` that reads/writes `memory/MEMORY.md` and `memory/daily_memory/` files
- Load memory content into Agent's system prompt before each `chat()` call
- Save facts to memory when the user asks the agent to remember something
- Add `memory_tools.py` — `remember` and `recall` tools the agent can call
- Agent writes to `USER.md` when it learns about the user

## Capabilities

### New Capabilities

- `agent-memory`: File-based persistent memory with MEMORY.md, daily files, and USER.md

### Modified Capabilities

<!-- None -->

## Impact

- **New file**: `jiuwenclaw/agentserver/memory/__init__.py`, `jiuwenclaw/agentserver/memory/manager.py`
- **New file**: `jiuwenclaw/agentserver/tools/memory_tools.py`
- **Modified file**: `jiuwenclaw/agentserver/agent.py` — load memory into system prompt
- **New docs**: tutorial + update index
