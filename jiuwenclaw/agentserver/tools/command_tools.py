"""Command tool — run shell commands."""

from __future__ import annotations

import asyncio
import os
from pathlib import Path
from typing import Any

from jiuwenclaw.agentserver.tools.base import BaseTool, ToolResult


class CommandTool(BaseTool):
    """Execute a shell command and return its output."""

    name = "command"
    description = "Run a shell command and return stdout and stderr. Use for file operations, running scripts, or system queries."

    def __init__(self, workspace_dir: Path | None = None):
        self.workspace_dir = workspace_dir or Path.cwd()

    async def execute(self, cmd: str = "", **kwargs: Any) -> ToolResult:
        if not cmd:
            return ToolResult(success=False, error="No command provided")

        try:
            process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(self.workspace_dir),
            )
            stdout, stderr = await process.communicate()
            output = stdout.decode("utf-8", errors="replace")
            if stderr:
                output += "\n[stderr]\n" + stderr.decode("utf-8", errors="replace")
            return ToolResult(
                success=process.returncode == 0,
                output=output.strip() or "(no output)",
            )
        except Exception as e:
            return ToolResult(success=False, error=str(e))

    def _parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "cmd": {"type": "string", "description": "The shell command to execute"},
            },
            "required": ["cmd"],
        }
