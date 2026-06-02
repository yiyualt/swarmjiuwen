"""Tests for ToolManager and built-in tools."""

import tempfile
from pathlib import Path

import pytest

from jiuwenclaw.agentserver.tools.base import BaseTool, ToolResult
from jiuwenclaw.agentserver.tools.tool_manager import ToolManager
from jiuwenclaw.agentserver.tools.file_tools import ReadFileTool, WriteFileTool
from jiuwenclaw.agentserver.tools.command_tools import CommandTool


class _EchoTool(BaseTool):
    name = "echo"
    description = "Echo back"

    async def execute(self, text: str = "", **kwargs):
        return ToolResult(success=True, output=text)

    def _parameters_schema(self):
        return {"type": "object", "properties": {"text": {"type": "string"}}}


class TestToolManager:
    def test_register_and_list(self):
        mgr = ToolManager()
        mgr.register(_EchoTool())
        assert len(mgr.list_tools()) == 1

    @pytest.mark.asyncio
    async def test_execute_tool(self):
        mgr = ToolManager()
        mgr.register(_EchoTool())
        result = await mgr.execute("echo", {"text": "hello"})
        assert result.success

    @pytest.mark.asyncio
    async def test_unknown_tool(self):
        mgr = ToolManager()
        result = await mgr.execute("nonexistent", {})
        assert not result.success
        assert "Unknown tool" in result.error

    def test_get_schemas(self):
        mgr = ToolManager()
        mgr.register(_EchoTool())
        schemas = mgr.get_schemas()
        assert len(schemas) == 1
        assert schemas[0]["function"]["name"] == "echo"


class TestFileTools:
    @pytest.mark.asyncio
    async def test_read_existing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp)
            (ws / "hello.txt").write_text("Hello, world!")
            tool = ReadFileTool(ws)
            result = await tool.execute(path="hello.txt")
            assert result.success
            assert "Hello, world!" in result.output

    @pytest.mark.asyncio
    async def test_read_nonexistent_file(self):
        tool = ReadFileTool(Path("/tmp"))
        result = await tool.execute(path="nonexistent.txt")
        assert not result.success

    @pytest.mark.asyncio
    async def test_read_path_traversal_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp)
            tool = ReadFileTool(ws)
            result = await tool.execute(path="../../../etc/passwd")
            assert not result.success
            assert "outside workspace" in result.error

    @pytest.mark.asyncio
    async def test_write_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp)
            tool = WriteFileTool(ws)
            result = await tool.execute(path="out.txt", content="Hello")
            assert result.success
            assert (ws / "out.txt").read_text() == "Hello"

    @pytest.mark.asyncio
    async def test_write_path_traversal_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp)
            tool = WriteFileTool(ws)
            result = await tool.execute(path="../../../etc/hacked", content="bad")
            assert not result.success


class TestCommandTool:
    @pytest.mark.asyncio
    async def test_echo(self):
        tool = CommandTool()
        result = await tool.execute(cmd="echo hello")
        assert result.success
        assert "hello" in result.output

    @pytest.mark.asyncio
    async def test_empty_cmd(self):
        tool = CommandTool()
        result = await tool.execute(cmd="")
        assert not result.success
