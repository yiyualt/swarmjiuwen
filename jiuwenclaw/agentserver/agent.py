"""Agent — single-turn chat with memory, tools, and multi-turn React loop."""

from __future__ import annotations

import json
import logging
import sys
import time
from pathlib import Path
from typing import Any, AsyncIterator

# Wire up vendored openjiuwen so it's importable
_vendor_root = Path(__file__).resolve().parent.parent / "vendor" / "openjiuwen"
if str(_vendor_root) not in sys.path:
    sys.path.insert(0, str(_vendor_root))

from jiuwenclaw.config import get_config
from jiuwenclaw.agentserver.memory.manager import MemoryManager
from jiuwenclaw.agentserver.tools.tool_manager import ToolManager
from jiuwenclaw.agentserver.tools.memory_tools import RecallTool, RememberTool
from jiuwenclaw.agentserver.tools.file_tools import ReadFileTool, WriteFileTool
from jiuwenclaw.agentserver.tools.command_tools import CommandTool

_logger = logging.getLogger(__name__)
from openjiuwen.core.foundation.llm.model import Model
from openjiuwen.core.foundation.llm.schema.config import (
    ModelClientConfig,
    ModelRequestConfig,
)
from openjiuwen.core.foundation.llm.schema.message import (
    AssistantMessage,
    SystemMessage,
    ToolMessage,
    UserMessage,
)


class Agent:
    """Chat agent with memory, tools, and multi-turn React loop.

    Uses openjiuwen's Model for LLM calls. Implements a while loop
    so the LLM can chain multiple tool calls before giving a final answer.
    """

    def __init__(self, workspace_dir: Path | None = None):
        self.workspace_dir = workspace_dir or Path.cwd()
        self._model: Any = None
        self._memory = MemoryManager()
        self._tools = ToolManager()

        self._tools.register(RememberTool(self._memory))
        self._tools.register(RecallTool(self._memory))
        self._tools.register(ReadFileTool(self.workspace_dir))
        self._tools.register(WriteFileTool(self.workspace_dir))
        self._tools.register(CommandTool(self.workspace_dir))

        self._memory_context = self._memory.load()
        self._max_turns = 100

        # Session history: session_id → list of (role, content) tuples
        self._history: dict[str, list[dict]] = {}
        self._last_access: dict[str, float] = {}
        self._max_sessions = 50
        self._session_timeout = 3600  # 1 hour

    @property
    def memory(self) -> MemoryManager:
        return self._memory

    @property
    def tools(self) -> ToolManager:
        return self._tools

    def _get_model(self) -> Any:
        if self._model is not None:
            return self._model

        cfg = get_config()
        models = cfg.get("models", {})
        default = models.get("default", {})
        mcc = default.get("model_client_config", {})
        mobj = default.get("model_config_obj", {})

        self._model = Model(
            model_client_config=ModelClientConfig(
                api_key=mcc.get("api_key", ""),
                api_base=mcc.get("api_base", ""),
                client_provider=mcc.get("client_provider", "openai"),
                timeout=int(mcc.get("timeout", 1800)),
                max_retries=int(mcc.get("max_retries", 1)),
                verify_ssl=bool(mcc.get("verify_ssl", False)),
            ),
            model_config=ModelRequestConfig(
                temperature=mobj.get("temperature", 0.95),
            ),
        )
        return self._model

    def _build_system_message(self) -> str:
        parts = []
        if self._memory_context:
            parts.append(f"Memory (what you know about the user):\n{self._memory_context}")
        return "\n\n".join(parts)

    def _get_history(self, session_id: str) -> list:
        """Get history, evicting idle sessions if needed."""
        now = time.time()
        # Evict idle sessions
        stale = [s for s, t in self._last_access.items() if now - t > self._session_timeout]
        for s in stale:
            self._history.pop(s, None)
            self._last_access.pop(s, None)
        # LRU eviction if over capacity
        while len(self._history) >= self._max_sessions:
            oldest = min(self._last_access, key=lambda k: self._last_access[k])
            self._history.pop(oldest, None)
            self._last_access.pop(oldest, None)
        self._last_access[session_id] = now
        return self._history.setdefault(session_id, [])

    async def chat(self, query: str, session_id: str = "") -> str:
        model = self._get_model()
        cfg = get_config()
        model_name = cfg["models"]["default"]["model_client_config"].get("model_name", "")
        tool_schemas = self._tools.get_schemas() or None
        history = self._get_history(session_id) if session_id else []

        messages: list[Any] = []
        system = self._build_system_message()
        if system:
            messages.append(SystemMessage(content=system))
        # Inject history
        for h in history:
            if h["role"] == "user":
                messages.append(UserMessage(content=h["content"]))
            else:
                messages.append(AssistantMessage(content=h["content"]))
        messages.append(UserMessage(content=query))

        # ── React loop ──────────────────────────────────────────
        for _ in range(self._max_turns):
            response = await model.invoke(messages, model=model_name, tools=tool_schemas)

            # Check for tool calls
            tool_call = None
            if hasattr(response, "tool_calls") and response.tool_calls:
                tc = response.tool_calls[0]
                tool_call = {
                    "name": tc.function.name,
                    "params": json.loads(tc.function.arguments),
                    "id": getattr(tc, "id", ""),
                }

            if tool_call is None:
                # No tool call — final answer
                answer = response.content if hasattr(response, "content") else str(response)
                if session_id:
                    history.append({"role": "user", "content": query})
                    history.append({"role": "assistant", "content": answer})
                return answer

            # Execute tool and feed result back
            _logger.info("Tool call: %s(%s)", tool_call["name"], tool_call["params"])
            result = await self._tools.execute(tool_call["name"], tool_call["params"])

            messages.append(AssistantMessage(
                content=response.content or "",
                tool_calls=response.tool_calls if hasattr(response, "tool_calls") else None,
            ))
            messages.append(ToolMessage(
                content=result.output if result.success else f"Error: {result.error}",
                tool_call_id=tool_call["id"],
            ))

        return response.content if hasattr(response, "content") else str(response)

    async def chat_stream(self, query: str) -> AsyncIterator[str]:
        model = self._get_model()
        cfg = get_config()
        model_name = cfg["models"]["default"]["model_client_config"].get("model_name", "")
        messages: list[Any] = []
        system = self._build_system_message()
        if system:
            messages.append(SystemMessage(content=system))
        messages.append(UserMessage(content=query))

        async for chunk in model.stream(messages, model=model_name):
            if hasattr(chunk, "content") and chunk.content:
                yield chunk.content
