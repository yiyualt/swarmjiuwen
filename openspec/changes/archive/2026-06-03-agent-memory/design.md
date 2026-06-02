## Context

The agent currently has no persistent state between requests. The original jiuwenclaw stores memory as Markdown files under `~/.jiuwenclaw/agent/jiuwenclaw_workspace/memory/`.

## Goals / Non-Goals

**Goals:**
- `MemoryManager` reads `MEMORY.md` and `daily_memory/` files on load
- Memory content is injected into the system prompt
- `USER.md` is updated when the agent learns about the user
- Two tools: `remember` (explicit save), `recall` (search memory)
- Works across sessions (files survive restarts)

**Non-Goals:**
- Vector embeddings / semantic search (future)
- Memory summarization/compaction (future)
- Memory expiration (future)

## Decisions

### File-based memory (Markdown)

**Why**: Transparent, editable by the user, git-friendly. Matches the original design. No database dependency.

### Simple injection into system prompt

Memory content is prepended to the system prompt as a "Memory" section. No complex retrieval — the full memory is loaded. OK for now since memory is small.

### Tools: remember + recall

The agent can call `remember` to save a fact and `recall` to search memory. These are registered as openjiuwen tools so the LLM can decide when to use them.
