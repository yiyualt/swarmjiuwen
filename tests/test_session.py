"""Tests for session history — multi-turn context."""

import tempfile
from pathlib import Path

import pytest

from jiuwenclaw.agentserver.agent import Agent


@pytest.fixture
def agent():
    """Create an Agent with a temp workspace (no LLM needed for history tests)."""
    with tempfile.TemporaryDirectory() as tmp:
        agent = Agent(workspace_dir=Path(tmp))
        yield agent


class TestSessionHistory:
    def test_history_starts_empty(self, agent):
        history = agent._get_history("sess-1")
        assert history == []

    def test_sessions_are_isolated(self, agent):
        h1 = agent._get_history("sess-1")
        h2 = agent._get_history("sess-2")
        h1.append({"role": "user", "content": "I like Python"})
        assert len(h2) == 0

    def test_multiple_turns_in_same_session(self, agent):
        h = agent._get_history("sess-1")
        h.append({"role": "user", "content": "My name is Alex"})
        h.append({"role": "assistant", "content": "Got it, Alex!"})
        h.append({"role": "user", "content": "What is my name?"})

        assert len(h) == 3
        assert h[0]["content"] == "My name is Alex"
        assert h[2]["content"] == "What is my name?"

    def test_history_capped_at_max_sessions(self, agent):
        agent._max_sessions = 3
        for i in range(5):
            h = agent._get_history(f"sess-{i}")
            h.append({"role": "user", "content": f"msg-{i}"})

        assert len(agent._history) <= 3

    def test_save_and_load_history(self, agent):
        h = agent._get_history("sess-persist")
        h.append({"role": "user", "content": "My name is Alex"})
        h.append({"role": "assistant", "content": "Got it!"})
        agent._save_history("sess-persist")

        # Simulate restart — clear in-memory history
        agent._history.clear()
        agent._last_access.clear()

        # Load should find disk copy
        loaded = agent._get_history("sess-persist")
        assert len(loaded) == 2
        assert loaded[0]["content"] == "My name is Alex"
