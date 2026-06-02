## 1. Config Engine

- [x] 1.1 Add dependencies: `ruamel.yaml`, `pyyaml`, `python-dotenv` to `pyproject.toml`
- [x] 1.2 Create `jiuwenclaw/resources/config.yaml` — shipped config template
- [x] 1.3 Create `jiuwenclaw/resources/.env.template` — environment variable template
- [x] 1.4 Implement `utils.py` — `merge_template_with_override()`, `resolve_env_vars()`, path helpers
- [x] 1.5 Implement `config.py` — `get_config()`, `get_config_raw()`

## 2. Tests

- [x] 2.1 Write `tests/test_config.py` — merge logic, env var resolution, path utilities

## 3. Documentation

- [x] 3.1 Write `docs/jiuwenclaw/tutorials/configuring-models.rst`
- [x] 3.2 Update `docs/index.rst` toctree
