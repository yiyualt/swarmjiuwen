## 1. Memory Manager

- [x] 1.1 Create `jiuwenclaw/agentserver/memory/` package with `__init__.py`
- [x] 1.2 Implement `memory/manager.py` — `MemoryManager` that reads MEMORY.md and daily_memory/*.md
- [x] 1.3 Create workspace `memory/` directories with MEMORY.md template in resources

## 2. Memory Tools

- [x] 2.1 Implement `tools/memory_tools.py` — `remember` and `recall` tools

## 3. Wire into Agent

- [x] 3.1 Update `agentserver/agent.py` — MemoryManager loads memory and injects into system prompt
- [x] 3.2 Register memory tools on the Agent so LLM can call them

## 4. Tests

- [x] 4.1 Write `tests/test_memory.py` — MemoryManager load, save, recall

## 5. Documentation

- [x] 5.1 Write `docs/jiuwenclaw/tutorials/memory.rst`
- [x] 5.2 Update `docs/index.rst`
