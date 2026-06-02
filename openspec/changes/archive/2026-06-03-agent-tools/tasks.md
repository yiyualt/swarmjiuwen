## 1. Tool Manager

- [x] 1.1 Implement `tools/tool_manager.py` — `ToolManager` with register, list, execute

## 2. Built-in Tools

- [x] 2.1 Implement `tools/file_tools.py` — `ReadFileTool`, `WriteFileTool`
- [x] 2.2 Implement `tools/command_tools.py` — `CommandTool`

## 3. Wire into Agent

- [x] 3.1 Register all tools (memory + file + command) on Agent init
- [x] 3.2 Pass tool schemas to LLM via `model.invoke(tools=...)`
- [x] 3.3 Parse tool calls from LLM response, execute, return result

## 4. Tests

- [x] 4.1 Write `tests/test_tools.py` — ToolManager, each tool, workspace path safety

## 5. Documentation

- [x] 5.1 Write `docs/jiuwenclaw/tutorials/tools.rst`
- [x] 5.2 Update `docs/index.rst`
