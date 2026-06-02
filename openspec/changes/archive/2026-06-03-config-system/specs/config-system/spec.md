# Config System

YAML template + sparse user override with environment variable resolution.

## ADDED Requirements

### Requirement: Template + override merging

The system SHALL ship a config template at `jiuwenclaw/resources/config.yaml` and merge it with the user's sparse override at `~/.jiuwenclaw/config/config.yaml`. User values win on conflict.

#### Scenario: User overrides a template value

- **WHEN** template has `react.window_round_num: 100`
- **AND** user config has `react.window_round_num: 50`
- **THEN** `get_config()` returns `react.window_round_num: 50`

#### Scenario: User doesn't set a template key

- **WHEN** template has `channels.web.port: 19000`
- **AND** user config has no `channels` key
- **THEN** `get_config()` returns `channels.web.port: 19000` (template default)

### Requirement: Environment variable resolution

The system SHALL resolve `${VAR:-default}` patterns in config values at load time.

#### Scenario: Env var with default fallback

- **WHEN** config has `api_key: ${API_KEY:-sk-default}`
- **AND** `API_KEY` env var is not set
- **THEN** the resolved value is `"sk-default"`

#### Scenario: Env var without default, set

- **WHEN** config has `api_key: ${API_KEY}`
- **AND** `API_KEY=sk-real` is set
- **THEN** the resolved value is `"sk-real"`

### Requirement: Path utilities

The system SHALL provide `get_config_dir()`, `get_config_file()`, `get_env_file()` returning paths under `~/.jiuwenclaw/`.

#### Scenario: Config file path

- **WHEN** `get_config_file()` is called
- **THEN** it returns `~/.jiuwenclaw/config/config.yaml`
