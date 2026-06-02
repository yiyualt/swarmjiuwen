"""Memory tools — remember and recall facts."""

from __future__ import annotations

from typing import Any

from jiuwenclaw.agentserver.tools.base import BaseTool, ToolResult


class RememberTool(BaseTool):
    """Save a fact to persistent memory."""

    name = "remember"
    description = "Save an important fact to persistent memory. Use this when the user shares something worth remembering across sessions."

    def __init__(self, memory_manager: Any = None):
        self._memory = memory_manager

    def set_memory(self, manager: Any) -> None:
        self._memory = manager

    async def execute(self, content: str = "", **kwargs: Any) -> ToolResult:
        if not content:
            return ToolResult(success=False, error="No content to remember")
        if self._memory is None:
            return ToolResult(success=False, error="Memory manager not available")
        try:
            self._memory.remember(content)
            self._memory.update_user(content)
            return ToolResult(success=True, output=f"Remembered: {content}")
        except Exception as e:
            return ToolResult(success=False, error=str(e))

    def _parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "content": {"type": "string", "description": "The fact to remember"},
            },
            "required": ["content"],
        }


class RecallTool(BaseTool):
    """Search persistent memory for facts."""

    name = "recall"
    description = "Search persistent memory for facts about the user or past conversations."

    def __init__(self, memory_manager: Any = None):
        self._memory = memory_manager

    def set_memory(self, manager: Any) -> None:
        self._memory = manager

    async def execute(self, query: str = "", **kwargs: Any) -> ToolResult:
        if not query:
            return ToolResult(success=False, error="No search query provided")
        if self._memory is None:
            return ToolResult(success=False, error="Memory manager not available")
        try:
            results = self._memory.recall(query)
            return ToolResult(success=True, output=results)
        except Exception as e:
            return ToolResult(success=False, error=str(e))

    def _parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query for memory"},
            },
            "required": ["query"],
        }
