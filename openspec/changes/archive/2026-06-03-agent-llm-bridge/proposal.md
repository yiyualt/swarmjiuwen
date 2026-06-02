## Why

WebChannel echoes. We have openjiuwen's LLM client in vendor — let's use it. The smallest step from echo to real AI: take a `chat.send` message, call the LLM, stream back the response. No React loop, no tools. Just one LLM call per request.

## What Changes

- Add `agentserver/agent.py` — `Agent` class that wraps openjiuwen's `Model` for simple chat completion
- Wire into WebChannel: replace echo with `Agent.chat(query)` call
- Stream the LLM response as `chat.delta` events, then `chat.final`
- Use FakeLLM in tests (no real API key needed)

## Capabilities

### New Capabilities

- `agent-llm-bridge`: Minimal agent that calls openjiuwen LLM for single-turn chat

### Modified Capabilities

<!-- None -->

## Impact

- **New file**: `jiuwenclaw/agentserver/__init__.py`, `jiuwenclaw/agentserver/agent.py`
- **Modified file**: `jiuwenclaw/channel/web_channel.py` — echo → LLM call
- **New test**: `tests/test_agent.py`
- **Update docs**: new tutorial
