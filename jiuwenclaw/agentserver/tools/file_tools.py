"""File tools — read and write workspace files."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from jiuwenclaw.agentserver.tools.base import BaseTool, ToolResult


class ReadFileTool(BaseTool):
    """Read a file from the workspace."""

    name = "read_file"
    description = "Read the contents of a file in the workspace."

    def __init__(self, workspace_dir: Path | None = None):
        self.workspace_dir = workspace_dir or Path.cwd()

    async def execute(self, path: str = "", **kwargs: Any) -> ToolResult:
        if not path:
            return ToolResult(success=False, error="No file path provided")

        file_path = (self.workspace_dir / path).resolve()
        workspace = self.workspace_dir.resolve()

        if not str(file_path).startswith(str(workspace)):
            return ToolResult(success=False, error="Path is outside workspace")

        if not file_path.exists():
            return ToolResult(success=False, error=f"File not found: {path}")

        try:
            content = file_path.read_text(encoding="utf-8")
            return ToolResult(success=True, output=content, metadata={"path": path})
        except Exception as e:
            return ToolResult(success=False, error=str(e))

    def _parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Relative path to the file"},
            },
            "required": ["path"],
        }


class WriteFileTool(BaseTool):
    """Create or overwrite a file in the workspace."""

    name = "write_file"
    description = "Create or overwrite a file in the workspace with the given content."

    def __init__(self, workspace_dir: Path | None = None):
        self.workspace_dir = workspace_dir or Path.cwd()

    async def execute(self, path: str = "", content: str = "", **kwargs: Any) -> ToolResult:
        if not path:
            return ToolResult(success=False, error="No file path provided")

        file_path = (self.workspace_dir / path).resolve()
        workspace = self.workspace_dir.resolve()

        if not str(file_path).startswith(str(workspace)):
            return ToolResult(success=False, error="Path is outside workspace")

        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding="utf-8")
            return ToolResult(
                success=True,
                output=f"File written: {path} ({len(content)} bytes)",
                metadata={"path": path, "size": len(content)},
            )
        except Exception as e:
            return ToolResult(success=False, error=str(e))

    def _parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Path to write the file"},
                "content": {"type": "string", "description": "Content to write"},
            },
            "required": ["path", "content"],
        }
