## Context

openjiuwen provides `Model.ainvoke(messages, config)` for single-turn LLM completion. We need the thinnest possible wrapper that connects a JiuwenClaw `chat.send` Message to an LLM response.

## Goals / Non-Goals

**Goals:**
- `Agent.chat(query)` → LLM → text response
- Stream `chat.delta` events for each token, then `chat.final`
- Read model config from our config system
- WebChannel uses Agent instead of echo

**Non-Goals:**
- React loop (multi-turn tool calling) — future
- Tool execution — future
- Session/memory — future

## Decisions

### Agent is a simple function, not a stateful class (yet)

No session state, no message history. Each `chat()` call is independent. This keeps the first version trivially testable.

### FakeLLM in tests, real Model in production

Tests use the same FakeLLM pattern from conftest.py. The real agent uses openjiuwen's `Model` with our config.
