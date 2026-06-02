## Context

We have `BaseTool` and `ToolResult` from the memory feature. Now we add file and command tools, plus a `ToolManager` to register them.

The openjiuwen `Model.invoke()` accepts `tools` — a list of tool schemas (JSON Schema function definitions). When the LLM decides to call a tool, it returns a tool call in the response. We parse that, execute the tool, and feed the result back.

## Goals / Non-Goals

**Goals:**
- `ToolManager.register()` + `ToolManager.execute()`
- `ReadFileTool` — read files in workspace (path-constrained)
- `WriteFileTool` — create/overwrite files in workspace
- `CommandTool` — run shell commands (subprocess)
- Agent passes tool schemas to LLM
- When LLM returns a tool call, execute it and return result

**Non-Goals:**
- Multi-turn React loop (future — this is single tool execution per request)
- Tool permissions/sandboxing (future)
- Web search tools (future)

## Decisions

### Workspace-constrained paths

ReadFileTool and WriteFileTool only access files under the workspace directory. Path traversal (e.g. `../../etc/passwd`) is blocked.

### Single tool execution per request

For now, the LLM can call one tool per request. If it needs to chain tools, the user must send another message. This avoids the complexity of a full React loop.

### Tool schemas as JSON Schema

Tools expose `to_schema()` returning OpenAI-compatible function definitions. The LLM uses these to decide when to call a tool.
