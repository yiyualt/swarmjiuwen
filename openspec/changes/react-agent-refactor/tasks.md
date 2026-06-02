## 1. Create AgentCard

- [x] 1.1 Create AgentCard with name "JiuwenClaw", description, and tool abilities in `agent.py`

## 2. Refactor Agent

- [x] 2.1 Replace `_get_model()` — use ReActAgentConfig to configure the model
- [x] 2.2 Replace `chat()` — call `ReActAgent(config=..., card=...).invoke({"query": query})`
- [x] 2.3 Remove `_parse_tool_call()` — no longer needed
- [x] 2.4 Remove manual tool-calling logic from `chat()` — ReActAgent handles it
- [x] 2.5 Keep memory injection working — set as system prompt

## 3. Tests

- [x] 3.1 Update `tests/` — ensure Agent still returns strings

## 4. Verify

- [x] 4.1 Run existing test suite — all tests still pass
- [ ] 4.2 Run 05send_llm.py — real LLM still works
