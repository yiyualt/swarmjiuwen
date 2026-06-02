"""Path utilities and YAML helpers for JiuwenClaw."""

from __future__ import annotations

import copy
import os
import re
from pathlib import Path
from typing import Any


# ── paths ────────────────────────────────────────────────────────

_raw_data_dir = os.environ.get("JIUWENCLAW_DATA_DIR", "").strip()
USER_WORKSPACE_DIR = (
    Path(_raw_data_dir).expanduser().resolve()
    if _raw_data_dir
    else Path.home() / ".jiuwenclaw"
)


def get_user_workspace_dir() -> Path:
    return USER_WORKSPACE_DIR


def get_config_dir() -> Path:
    return get_user_workspace_dir() / "config"


def get_config_file() -> Path:
    return get_config_dir() / "config.yaml"


def get_env_file() -> Path:
    return get_config_dir() / ".env"


def resolve_shipped_config_path() -> Path:
    return Path(__file__).resolve().parent / "resources" / "config.yaml"


# ── YAML helpers ──────────────────────────────────────────────────

def load_yaml_dict(path: Path) -> dict[str, Any]:
    """Load a YAML file as a dict. Returns {} if missing."""
    if not path.exists():
        return {}
    import yaml
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data if isinstance(data, dict) else {}


def merge_template_with_override(
    template: dict[str, Any],
    override: dict[str, Any],
) -> dict[str, Any]:
    """Deep-merge template defaults with user override. User wins."""
    out: dict[str, Any] = {}
    for key, tmpl_val in template.items():
        if key not in override:
            out[key] = copy.deepcopy(tmpl_val)
        elif isinstance(tmpl_val, dict) and isinstance(override.get(key), dict):
            out[key] = merge_template_with_override(tmpl_val, override[key])
        else:
            out[key] = override[key]
    for key, over_val in override.items():
        if key not in template:
            out[key] = copy.deepcopy(over_val)
    return out


# ── env var resolution ────────────────────────────────────────────

def resolve_env_vars(value: Any) -> Any:
    """Recursively resolve ``${VAR:-default}`` patterns."""
    if isinstance(value, str):
        pattern = r"\$\{([^:}]+)(?::-([^}]*))?\}"

        def _replace(match: re.Match) -> str:
            var_name = match.group(1)
            default = match.group(2)
            val = os.getenv(var_name)
            if val is not None and val != "":
                return val
            if default is not None:
                return default
            return ""

        return re.sub(pattern, _replace, value)
    if isinstance(value, dict):
        return {k: resolve_env_vars(v) for k, v in value.items()}
    if isinstance(value, list):
        return [resolve_env_vars(item) for item in value]
    return value
