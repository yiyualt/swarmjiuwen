"""Agent — single-turn chat with memory and tools."""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from typing import Any, AsyncIterator

# Wire up vendored openjiuwen so it's importable
_vendor_root = Path(__file__).resolve().parent.parent / "vendor" / "openjiuwen"
if str(_vendor_root) not in sys.path:
    sys.path.insert(0, str(_vendor_root))

from jiuwenclaw.config import get_config
from jiuwenclaw.agentserver.memory.manager import MemoryManager
from jiuwenclaw.agentserver.tools.tool_manager import ToolManager

# Memory tools
from jiuwenclaw.agentserver.tools.memory_tools import RecallTool, RememberTool
# File tools
from jiuwenclaw.agentserver.tools.file_tools import ReadFileTool, WriteFileTool
# Command tool
from jiuwenclaw.agentserver.tools.command_tools import CommandTool

_logger = logging.getLogger(__name__)
from openjiuwen.core.foundation.llm.model import Model
from openjiuwen.core.foundation.llm.schema.config import (
    ModelClientConfig,
    ModelRequestConfig,
)
from openjiuwen.core.foundation.llm.schema.message import SystemMessage, UserMessage
            # Feed tool result back to LLM for final answer
from openjiuwen.core.foundation.llm.schema.message import (
    AssistantMessage,
    ToolMessage,
)

class Agent:
    """Single-turn chat agent with persistent memory and tools.

    Loads memory files into the system prompt. Passes tool schemas to the
    LLM so it can call tools (read_file, write_file, command, remember, recall).
    """

    def __init__(self, workspace_dir: Path | None = None):
        self.workspace_dir = workspace_dir or Path.cwd()
        self._model: Any = None
        self._memory = MemoryManager()
        self._tools = ToolManager()

        # Register all tools
        self._tools.register(RememberTool(self._memory))
        self._tools.register(RecallTool(self._memory))
        self._tools.register(ReadFileTool(self.workspace_dir))
        self._tools.register(WriteFileTool(self.workspace_dir))
        self._tools.register(CommandTool(self.workspace_dir))

        # Load memory on startup
        self._memory_context = self._memory.load()

    @property
    def memory(self) -> MemoryManager:
        return self._memory

    @property
    def tools(self) -> ToolManager:
        return self._tools

    def _get_model(self) -> Any:
        """Lazy-init the openjiuwen Model from current config."""
        if self._model is not None:
            return self._model

        cfg = get_config()
        models = cfg.get("models", {})
        default = models.get("default", {})
        mcc = default.get("model_client_config", {})

        client_config = ModelClientConfig(
            api_key=mcc.get("api_key", ""),
            api_base=mcc.get("api_base", ""),
            model_name=mcc.get("model_name", ""),
            client_provider=mcc.get("client_provider", "openai"),
            timeout=int(mcc.get("timeout", 1800)),
            max_retries=int(mcc.get("max_retries", 1)),
            verify_ssl=bool(mcc.get("verify_ssl", False)),
        )
        model_config = ModelRequestConfig(
            temperature=default.get("model_config_obj", {}).get("temperature", 0.95),
        )

        self._model = Model(
            model_client_config=client_config,
            model_config=model_config,
        )
        return self._model

    def _build_messages(self, query: str) -> list[Any]:
        """Build message list with memory context as system prompt."""
        messages: list[Any] = []

        if self._memory_context:
            messages.append(SystemMessage(
                content=f"You have access to persistent memory. The following is what you know about the user and past conversations:\n\n{self._memory_context}"
            ))

        messages.append(UserMessage(content=query))
        return messages

    def _parse_tool_call(self, response: Any) -> dict[str, Any] | None:
        """Extract a tool call from the LLM response."""
        content = response.content if hasattr(response, "content") else str(response)
        if not content:
            return None

        # Check for tool_calls in the response (OpenAI format)
        if hasattr(response, "tool_calls") and response.tool_calls:
            tc = response.tool_calls[0]
            return {"name": tc.function.name, "params": json.loads(tc.function.arguments)}

        return None

    async def chat(self, query: str) -> str:
        """Send a query to the LLM, execute any tool calls, return the response."""
        model = self._get_model()
        cfg = get_config()
        model_name = cfg["models"]["default"]["model_client_config"].get("model_name", "")
        messages = self._build_messages(query)

        tool_schemas = self._tools.get_schemas() or None

        response = await model.invoke(messages, model=model_name, tools=tool_schemas)

        # Check if LLM wants to call a tool
        tool_call = self._parse_tool_call(response)
        if tool_call:
            _logger.info("Tool call: %s(%s)", tool_call["name"], tool_call["params"])
            result = await self._tools.execute(tool_call["name"], tool_call["params"])

            messages.append(AssistantMessage(content=response.content or ""))
            messages.append(ToolMessage(
                content=result.output if result.success else f"Error: {result.error}",
                tool_call_id=getattr(response.tool_calls[0], "id", "") if hasattr(response, "tool_calls") and response.tool_calls else "",
            ))
            response = await model.invoke(messages, model=model_name, tools=tool_schemas)

        return response.content if hasattr(response, "content") else str(response)

    async def chat_stream(self, query: str) -> AsyncIterator[str]:
        """Send a query and yield tokens as they arrive."""
        model = self._get_model()
        cfg = get_config()
        model_name = cfg["models"]["default"]["model_client_config"].get("model_name", "")
        messages = self._build_messages(query)

        async for chunk in model.stream(messages, model=model_name):
            if hasattr(chunk, "content") and chunk.content:
                yield chunk.content
