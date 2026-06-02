## Context

Hardcoded values (port 19000, paths, etc.) block real usage. Users must be able to set API keys, change ports, and toggle features without touching source code.

## Goals / Non-Goals

**Goals:**
- Ship a full config template in the package (never user-edited)
- Users write only changed keys to `~/.jiuwenclaw/config/config.yaml` (sparse override)
- At startup, merge template + override (user wins on conflict)
- Support `${VAR:-default}` syntax for env var injection
- Workspace path utilities for `~/.jiuwenclaw/`

**Non-Goals:**
- Hot reload (future)
- Config via Web UI (future)
- Multiple config profiles (future)

## Decisions

### Template + sparse override (not single user-owned file)

**Why**: When the package upgrades with new config keys, the template provides defaults automatically. Users don't need to manually merge new settings. This is the same pattern used by the reference implementation.

### ruamel.yaml for round-trip, pyyaml for safe load

**Why**: `ruamel.yaml` preserves comments and formatting when writing user overrides. `pyyaml` is used for safe loading of the template.

### `${VAR:-default}` syntax

**Why**: Standard shell-like syntax. Easy to understand. The reference implementation uses this exact pattern.
