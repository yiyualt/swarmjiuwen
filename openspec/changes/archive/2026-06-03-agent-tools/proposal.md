## Why

Agent can chat and remember, but can't DO anything. It should read files, write files, and run commands. With tools, the agent becomes genuinely useful — it can inspect your codebase, create files, and execute shell commands.

## What Changes

- Add `ToolManager` — registry for tool registration, lookup, and execution
- Add `read_file` tool — read any file in the workspace
- Add `write_file` tool — create or overwrite files
- Add `command` tool — run shell commands in the workspace
- Wire tools into Agent so the LLM can call them (pass tool schemas to `model.invoke()`)
- Parse tool calls from LLM responses and execute them

## Capabilities

### New Capabilities

- `agent-tools`: ToolManager registry + read_file, write_file, command tools

### Modified Capabilities

<!-- None -->

## Impact

- **New file**: `jiuwenclaw/agentserver/tools/tool_manager.py`
- **New file**: `jiuwenclaw/agentserver/tools/file_tools.py`
- **New file**: `jiuwenclaw/agentserver/tools/command_tools.py`
- **Modified file**: `jiuwenclaw/agentserver/agent.py` — pass tools to LLM, execute tool calls
- **New docs**: tutorial + update index
