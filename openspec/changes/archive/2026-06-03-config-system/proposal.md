## Why

Right now ports, paths, and settings are hardcoded. Users need a way to configure JiuwenClaw without editing source code. The Config system uses a YAML template + sparse user override pattern: the package ships a full template with defaults, and users write only the keys they want to change in `~/.jiuwenclaw/config/config.yaml`.

## What Changes

- Add `jiuwenclaw/resources/config.yaml` — shipped template with all defaults
- Add `jiuwenclaw/resources/.env.template` — environment variable template
- Add `jiuwenclaw/config.py` — `get_config()` merges template + user override, resolves `${VAR:-default}`
- Add `jiuwenclaw/utils.py` — `merge_template_with_override()`, path utilities for `~/.jiuwenclaw/`
- Add tutorial: configuring JiuwenClaw

## Capabilities

### New Capabilities

- `config-system`: YAML template + sparse override merging, `${VAR:-default}` env var resolution

### Modified Capabilities

<!-- None -->

## Impact

- **New file**: `jiuwenclaw/config.py`
- **New file**: `jiuwenclaw/utils.py`
- **New file**: `jiuwenclaw/resources/config.yaml`
- **New file**: `jiuwenclaw/resources/.env.template`
- **New dep**: `ruamel.yaml` (round-trip YAML), `pyyaml` (safe load), `python-dotenv`
- **Update docs**: new tutorial
