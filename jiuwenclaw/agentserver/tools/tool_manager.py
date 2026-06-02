"""ToolManager — tool registration, lookup, and execution."""

from __future__ import annotations

import logging
from typing import Any

from jiuwenclaw.agentserver.tools.base import BaseTool, ToolResult

_logger = logging.getLogger(__name__)


class ToolManager:
    """Registers and executes agent tools."""

    def __init__(self):
        self._tools: dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        """Register a tool for the agent to call."""
        if not tool.name:
            raise ValueError("Tool must have a name")
        self._tools[tool.name] = tool
        _logger.debug("Registered tool: %s", tool.name)

    def list_tools(self) -> list[BaseTool]:
        """Return all registered tools."""
        return list(self._tools.values())

    def get_schemas(self) -> list[dict[str, Any]]:
        """Return OpenAI-compatible function schemas for all tools."""
        schemas = []
        for tool in self._tools.values():
            schemas.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool._parameters_schema(),
                },
            })
        return schemas

    def get_tool(self, name: str) -> BaseTool | None:
        """Look up a tool by name."""
        return self._tools.get(name)

    async def execute(self, name: str, params: dict[str, Any]) -> ToolResult:
        """Execute a tool by name."""
        tool = self._tools.get(name)
        if tool is None:
            return ToolResult(
                success=False,
                error=f"Unknown tool: {name}. Available: {list(self._tools.keys())}",
            )
        try:
            return await tool.execute(**params)
        except Exception as e:
            return ToolResult(success=False, error=str(e))
