# Agent Tools

Tool system that lets the agent read files, write files, and run commands.

## ADDED Requirements

### Requirement: ToolManager registry

The system SHALL provide a `ToolManager` that registers tools and executes them by name.

#### Scenario: Register and execute a tool

- **WHEN** `tool_manager.register(ReadFileTool())` is called
- **AND** `tool_manager.execute("read_file", {"path": "test.txt"})` is called
- **THEN** the tool executes and returns a `ToolResult`

#### Scenario: Unknown tool returns error

- **WHEN** `tool_manager.execute("nonexistent", {})` is called
- **THEN** a `ToolResult` with `success=False` is returned

### Requirement: ReadFileTool

The system SHALL provide a `read_file` tool that reads a file from the workspace.

#### Scenario: Read existing file

- **WHEN** `read_file` is called with `path="AGENT.md"`
- **THEN** the file content is returned

#### Scenario: Path outside workspace is rejected

- **WHEN** `read_file` is called with `path="../../../etc/passwd"`
- **THEN** an error is returned

### Requirement: WriteFileTool

The system SHALL provide a `write_file` tool that creates or overwrites a file.

#### Scenario: Write a new file

- **WHEN** `write_file` is called with `path="hello.txt"` and `content="Hello"`
- **THEN** the file is created in the workspace

### Requirement: CommandTool

The system SHALL provide a `command` tool that runs a shell command and returns stdout/stderr.

#### Scenario: Run a command

- **WHEN** `command` is called with `cmd="echo hello"`
- **THEN** stdout contains "hello"

### Requirement: Agent passes tools to LLM

The system SHALL pass registered tool schemas to the LLM on each request.

#### Scenario: LLM receives tool list

- **WHEN** Agent has 3 tools registered
- **AND** `chat()` is called
- **THEN** the LLM receives tool schemas in the invoke call
